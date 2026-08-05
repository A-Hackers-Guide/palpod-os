import Foundation

/// REST client for the Hearth pal-web FastAPI backend.
///
/// Design notes:
///   * Uses async/await; no third-party networking libraries.
///   * TLS pinning via `URLSessionDelegate` against the self-signed cert
///     captured during pairing.
///   * The `grantControl` method REQUIRES a `ConsentGesture`. That
///     parameter is not just for documentation — it is the only way to
///     obtain the `X-Consent-Origin: user-tap` header through
///     `ConsentTokenSource`. See `ConsentGesture.swift` for the type-level
///     enforcement.
actor HearthClient {
    nonisolated let baseURL: URL
    private let session: URLSession
    private let keychain: KeychainStore
    private let decoder: JSONDecoder
    private let encoder: JSONEncoder

    init(baseURL: URL, keychain: KeychainStore = KeychainStore()) {
        self.baseURL = baseURL
        self.keychain = keychain

        let dec = JSONDecoder()
        dec.dateDecodingStrategy = .iso8601
        self.decoder = dec

        let enc = JSONEncoder()
        enc.dateEncodingStrategy = .iso8601
        self.encoder = enc

        let cfg = URLSessionConfiguration.ephemeral
        cfg.httpCookieAcceptPolicy = .always
        cfg.httpShouldSetCookies = true
        cfg.tlsMinimumSupportedProtocolVersion = .TLSv12
        cfg.waitsForConnectivity = false
        // Nothing leaves the house — do not use the URL cache.
        cfg.urlCache = nil
        cfg.requestCachePolicy = .reloadIgnoringLocalCacheData

        let ks = keychain
        let delegate = TLSPinningDelegate(pinProvider: { ks.data(for: .pinnedCert) })
        self.session = URLSession(configuration: cfg, delegate: delegate, delegateQueue: nil)
    }

    /// The URL session — exposed so companion views (WebSocket) inherit the pinning delegate.
    nonisolated var urlSession: URLSession { session }

    // MARK: - Auth

    struct LoginResponse: Decodable, Sendable {
        let csrfToken: String
        enum CodingKeys: String, CodingKey { case csrfToken = "csrf_token" }
    }

    func login(password: String) async throws -> LoginResponse {
        struct Body: Encodable { let password: String }
        let resp: LoginResponse = try await request(
            path: "/api/auth/login",
            method: "POST",
            body: Body(password: password),
            authenticated: false
        )
        try keychain.setString(resp.csrfToken, for: .csrf)
        return resp
    }

    // MARK: - Remote devices

    func devices() async throws -> [RemoteDevice] {
        try await request(path: "/api/remote/devices", method: "GET")
    }

    func pairDevice(name: String, kind: RemoteDevice.Kind) async throws -> RemoteDevice {
        struct Body: Encodable { let name: String; let kind: RemoteDevice.Kind }
        return try await request(
            path: "/api/remote/devices",
            method: "POST",
            body: Body(name: name, kind: kind)
        )
    }

    func unpair(deviceId: String) async throws {
        _ = try await requestRaw(
            path: "/api/remote/devices/\(deviceId)",
            method: "DELETE"
        )
    }

    // MARK: - Control grant (the load-bearing method)

    enum GrantError: Error, LocalizedError {
        case durationOutOfRange
        case cooldownActive
        case rollingCapExceeded
        case server(status: Int, body: String)

        var errorDescription: String? {
            switch self {
            case .durationOutOfRange: return "Duration must be between 1 and 60 minutes."
            case .cooldownActive:     return "Please wait 30 seconds between control grants."
            case .rollingCapExceeded: return "You have hit the 240-minute rolling 24h cap."
            case .server(let s, let b): return "Server \(s): \(b)"
            }
        }
    }

    /// Grant time-boxed control of `deviceId` to the Hearth.
    ///
    /// This method DEMANDS a `ConsentGesture`. The gesture parameter is
    /// the only path through which `ConsentTokenSource.header(for:)` can
    /// produce the `X-Consent-Origin: user-tap` header. See
    /// `ConsentGesture.swift` for the full argument.
    ///
    /// The method also verifies at runtime that the gesture's device id
    /// matches the `deviceId` we're posting to, catching mis-wired UIs.
    func grantControl(
        deviceId: String,
        gesture: ConsentGesture
    ) async throws -> ControlGrant {
        precondition(
            gesture.deviceId == deviceId,
            "ConsentGesture device id (\(gesture.deviceId)) does not match target (\(deviceId)). This is a programmer error in the calling view."
        )
        guard (1...60).contains(gesture.durationMinutes) else {
            throw GrantError.durationOutOfRange
        }

        struct Body: Encodable { let minutes: Int }
        let consent = ConsentTokenSource.header(for: gesture)
        let csrf = keychain.string(for: .csrf) ?? ""

        var extraHeaders: [String: String] = [
            consent.name: consent.value,
            "X-CSRF-Token": csrf,
        ]
        // Include a lightweight fingerprint of the gesture for the audit
        // log so a leaked or replayed body is distinguishable server-side.
        extraHeaders["X-Consent-Fingerprint"] = String(
            format: "%llx", UInt64(gesture.capturedAt.timeIntervalSince1970 * 1000)
        )

        do {
            return try await request(
                path: "/api/remote/devices/\(deviceId)/grant-control",
                method: "POST",
                body: Body(minutes: gesture.durationMinutes),
                extraHeaders: extraHeaders
            )
        } catch let ClientError.server(status, body) {
            switch status {
            case 409:  throw GrantError.cooldownActive
            case 429:  throw GrantError.rollingCapExceeded
            default:   throw GrantError.server(status: status, body: body)
            }
        }
    }

    func revokeControl(deviceId: String) async throws {
        _ = try await requestRaw(
            path: "/api/remote/devices/\(deviceId)/revoke-control",
            method: "POST"
        )
    }

    func openSession(deviceId: String) async throws -> RemoteSession {
        struct Body: Encodable { let device_id: String }
        return try await request(
            path: "/api/remote/sessions",
            method: "POST",
            body: Body(device_id: deviceId)
        )
    }

    func anomalies(sessionId: String) async throws -> [SessionAnomaly] {
        try await request(path: "/api/remote/sessions/\(sessionId)/anomalies", method: "GET")
    }

    // MARK: - Users / personality

    func users() async throws -> [HouseholdUser] {
        try await request(path: "/api/users", method: "GET")
    }

    func personality(userId: String) async throws -> PersonalityAxes {
        try await request(path: "/api/users/\(userId)/personality", method: "GET")
    }

    func updatePersonality(userId: String, axes: PersonalityAxes) async throws {
        _ = try await requestRaw(
            path: "/api/users/\(userId)/personality",
            method: "PUT",
            body: axes.clamped()
        )
    }

    // MARK: - Library / play

    func library() async throws -> [MediaItem] {
        try await request(path: "/api/library", method: "GET")
    }

    func play(itemId: String, target: PlayTarget) async throws {
        struct Body: Encodable { let item_id: String; let target_id: String }
        _ = try await requestRaw(
            path: "/api/play",
            method: "POST",
            body: Body(item_id: itemId, target_id: target.id)
        )
    }

    func extenders() async throws -> [Extender] {
        try await request(path: "/api/extenders", method: "GET")
    }

    // MARK: - Pairing

    struct PairResponse: Decodable, Sendable {
        let jwt: String
        let pinnedCert: String  // base64 DER
        enum CodingKeys: String, CodingKey {
            case jwt
            case pinnedCert = "pinned_cert"
        }
    }

    func pair(token: String, fingerprint: String) async throws -> PairResponse {
        struct Body: Encodable { let token: String; let fingerprint: String }
        let resp: PairResponse = try await request(
            path: "/api/pair",
            method: "POST",
            body: Body(token: token, fingerprint: fingerprint),
            authenticated: false
        )
        try keychain.setString(resp.jwt, for: .jwt)
        if let certData = Data(base64Encoded: resp.pinnedCert) {
            try keychain.set(certData, for: .pinnedCert)
        }
        return resp
    }

    // MARK: - Request plumbing

    enum ClientError: Error {
        case badURL
        case server(status: Int, body: String)
        case decoding(Error)
    }

    private func request<T: Decodable>(
        path: String,
        method: String,
        body: (some Encodable)? = Optional<Empty>.none,
        authenticated: Bool = true,
        extraHeaders: [String: String] = [:]
    ) async throws -> T {
        let (data, _) = try await requestRaw(
            path: path,
            method: method,
            body: body,
            authenticated: authenticated,
            extraHeaders: extraHeaders
        )
        do { return try decoder.decode(T.self, from: data) }
        catch { throw ClientError.decoding(error) }
    }

    @discardableResult
    private func requestRaw(
        path: String,
        method: String,
        body: (some Encodable)? = Optional<Empty>.none,
        authenticated: Bool = true,
        extraHeaders: [String: String] = [:]
    ) async throws -> (Data, HTTPURLResponse) {
        guard let url = URL(string: path, relativeTo: baseURL) else { throw ClientError.badURL }
        var req = URLRequest(url: url)
        req.httpMethod = method
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        req.setValue("application/json", forHTTPHeaderField: "Accept")

        if authenticated, let jwt = keychain.string(for: .jwt) {
            req.setValue("Bearer \(jwt)", forHTTPHeaderField: "Authorization")
        }
        // Attach CSRF token to every mutating authenticated request.
        // grantControl passes its own X-CSRF-Token in extraHeaders; the loop
        // below runs AFTER this block so it wins.
        if authenticated, method != "GET" {
            if let csrf = keychain.string(for: .csrf), !csrf.isEmpty {
                req.setValue(csrf, forHTTPHeaderField: "X-CSRF-Token")
            }
        }
        for (k, v) in extraHeaders { req.setValue(v, forHTTPHeaderField: k) }

        if let body = body {
            req.httpBody = try encoder.encode(body)
        }

        let (data, response) = try await session.data(for: req)
        guard let http = response as? HTTPURLResponse else {
            throw ClientError.server(status: -1, body: "not http")
        }
        guard (200..<300).contains(http.statusCode) else {
            let text = String(data: data, encoding: .utf8) ?? ""
            throw ClientError.server(status: http.statusCode, body: text)
        }
        return (data, http)
    }

    private struct Empty: Encodable {}
}

/// Placeholder for the session response the WS handshake uses.
struct RemoteSession: Decodable, Identifiable, Sendable {
    let id: String
    let deviceId: String
    let wsPath: String
    enum CodingKeys: String, CodingKey {
        case id
        case deviceId = "device_id"
        case wsPath = "ws_path"
    }
}

// MARK: - TLS pinning delegate

/// Rejects the connection unless the server presents the exact cert we
/// captured during pairing. Falls back to the system trust store only if
/// we have not paired yet (during pairing itself, before the cert is in
/// the keychain). That transient window is the reason `pair()` is called
/// over the same session — the operator scans the QR to confirm the
/// fingerprint out of band.
final class TLSPinningDelegate: NSObject, URLSessionDelegate, URLSessionTaskDelegate, @unchecked Sendable {
    private let pinProvider: () -> Data?
    init(pinProvider: @escaping () -> Data?) { self.pinProvider = pinProvider }

    func urlSession(_ session: URLSession,
                    task: URLSessionTask,
                    didReceive challenge: URLAuthenticationChallenge,
                    completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        self.urlSession(session, didReceive: challenge, task: task, completionHandler: completionHandler)
    }

    func urlSession(_ session: URLSession,
                    didReceive challenge: URLAuthenticationChallenge,
                    completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        self.urlSession(session, didReceive: challenge, task: nil, completionHandler: completionHandler)
    }

    private func urlSession(_ session: URLSession,
                            didReceive challenge: URLAuthenticationChallenge,
                            task: URLSessionTask?,
                            completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
              let serverTrust = challenge.protectionSpace.serverTrust else {
            completionHandler(.performDefaultHandling, nil)
            return
        }

        // Read the pin FRESH each challenge so a post-init pair() write is honored.
        let pinnedCert = pinProvider()
        // If we don't have a pinned cert yet, allow ONLY the local pairing path.
        // Any request to a path other than /api/pair on an unpinned socket is rejected.
        guard let pinnedCert else {
            let host = challenge.protectionSpace.host
            let path = task?.currentRequest?.url?.path ?? task?.originalRequest?.url?.path ?? ""
            let isLocalHost = host.hasSuffix(".local") || host == "127.0.0.1" || host == "localhost"
            let isPairPath = path == "/api/pair"
            if isLocalHost && isPairPath {
                completionHandler(.useCredential, URLCredential(trust: serverTrust))
            } else {
                completionHandler(.cancelAuthenticationChallenge, nil)
            }
            return
        }

        // Compare presented leaf cert against the pinned one.
        var certs: CFArray?
        if #available(iOS 15.0, *) {
            certs = SecTrustCopyCertificateChain(serverTrust)
        }
        let count = certs.map { CFArrayGetCount($0) } ?? 0
        guard count > 0,
              let leaf = (certs.flatMap { CFArrayGetValueAtIndex($0, 0) })
                  .map({ Unmanaged<SecCertificate>.fromOpaque($0).takeUnretainedValue() })
        else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }
        let leafData = SecCertificateCopyData(leaf) as Data
        if leafData == pinnedCert {
            completionHandler(.useCredential, URLCredential(trust: serverTrust))
        } else {
            completionHandler(.cancelAuthenticationChallenge, nil)
        }
    }
}
