import Foundation

/// A remote-desktop-controllable device paired with the Hearth. Matches
/// the JSON shape returned by `GET /api/remote/devices`.
struct RemoteDevice: Codable, Identifiable, Hashable, Sendable {
    let id: String
    let name: String
    let kind: Kind
    /// If `nil`, the device is view-only. If non-nil, control has been
    /// granted until that instant (server clock).
    let grantedUntil: Date?
    let lastSeen: Date?

    enum Kind: String, Codable, Sendable {
        case desktop, laptop, tv, tablet, phone, other
    }

    enum CodingKeys: String, CodingKey {
        case id, name, kind
        case grantedUntil = "granted_until"
        case lastSeen = "last_seen"
    }

    var isControlGranted: Bool {
        guard let until = grantedUntil else { return false }
        return until > Date()
    }

    var remainingSeconds: Int {
        guard let until = grantedUntil else { return 0 }
        return max(0, Int(until.timeIntervalSinceNow))
    }
}
