import Foundation
import Security

/// Small wrapper around the iOS Keychain for the two secrets we hold:
///   * the long-lived JWT issued after pairing
///   * the CSRF token used to co-authorize control grants
///
/// Notes:
///   * We use `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` so the
///     token survives reboots but does not sync to iCloud Keychain and
///     is not readable while the device is locked.
///   * We never put JWTs in `UserDefaults` — that's the reason this
///     wrapper exists.
public struct KeychainStore {
    public enum Key: String {
        case jwt = "com.hearthhome.hearth.jwt"
        case csrf = "com.hearthhome.hearth.csrf"
        case pinnedCert = "com.hearthhome.hearth.pinned_cert"
    }

    public init() {}

    public func set(_ data: Data, for key: Key) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key.rawValue,
        ]
        // Delete any existing item — Keychain add is not idempotent.
        SecItemDelete(query as CFDictionary)

        let addQuery: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key.rawValue,
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly,
        ]
        let status = SecItemAdd(addQuery as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.osStatus(status)
        }
    }

    public func setString(_ value: String, for key: Key) throws {
        guard let data = value.data(using: .utf8) else {
            throw KeychainError.encoding
        }
        try set(data, for: key)
    }

    public func data(for key: Key) -> Data? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key.rawValue,
            kSecReturnData as String: kCFBooleanTrue as Any,
            kSecMatchLimit as String: kSecMatchLimitOne,
        ]
        var out: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &out)
        guard status == errSecSuccess else { return nil }
        return out as? Data
    }

    public func string(for key: Key) -> String? {
        data(for: key).flatMap { String(data: $0, encoding: .utf8) }
    }

    public func delete(_ key: Key) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key.rawValue,
        ]
        SecItemDelete(query as CFDictionary)
    }

    public func wipe() {
        for k in [Key.jwt, .csrf, .pinnedCert] { delete(k) }
    }
}

public enum KeychainError: Error, Equatable {
    case osStatus(OSStatus)
    case encoding
}
