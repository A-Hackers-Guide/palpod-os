import Foundation
import Combine

/// Minimal `URLSessionWebSocketTask` wrapper for the `/ws/remote/{sid}`
/// endpoint. Streams incoming frames (video + control-state) up to
/// SwiftUI, and lets input events flow the other way.
///
/// The server refuses input frames when the grant window has expired,
/// but we also gate on the app side against the local `grantedUntil`
/// clock — nothing in the app UI hands input events to `send(input:)`
/// unless the countdown chip is green.
public final class WebSocketClient: NSObject, ObservableObject {
    public struct Frame: Sendable {
        public let payload: Data
        public let receivedAt: Date
    }

    public enum InputEvent: Codable, Sendable {
        case mouseMove(x: Double, y: Double)
        case mouseClick(button: Int, pressed: Bool)
        case scroll(dx: Double, dy: Double)
        case key(scan: Int, pressed: Bool, modifiers: Int)
        case text(String)

        enum CodingKeys: String, CodingKey { case type, x, y, button, pressed, dx, dy, scan, modifiers, text }
        enum Kind: String, Codable { case move, click, scroll, key, text }

        public func encode(to encoder: Encoder) throws {
            var c = encoder.container(keyedBy: CodingKeys.self)
            switch self {
            case let .mouseMove(x, y):
                try c.encode(Kind.move, forKey: .type); try c.encode(x, forKey: .x); try c.encode(y, forKey: .y)
            case let .mouseClick(button, pressed):
                try c.encode(Kind.click, forKey: .type); try c.encode(button, forKey: .button); try c.encode(pressed, forKey: .pressed)
            case let .scroll(dx, dy):
                try c.encode(Kind.scroll, forKey: .type); try c.encode(dx, forKey: .dx); try c.encode(dy, forKey: .dy)
            case let .key(scan, pressed, modifiers):
                try c.encode(Kind.key, forKey: .type); try c.encode(scan, forKey: .scan); try c.encode(pressed, forKey: .pressed); try c.encode(modifiers, forKey: .modifiers)
            case let .text(s):
                try c.encode(Kind.text, forKey: .type); try c.encode(s, forKey: .text)
            }
        }

        public init(from decoder: Decoder) throws {
            let c = try decoder.container(keyedBy: CodingKeys.self)
            let kind = try c.decode(Kind.self, forKey: .type)
            switch kind {
            case .move:   self = .mouseMove(x: try c.decode(Double.self, forKey: .x), y: try c.decode(Double.self, forKey: .y))
            case .click:  self = .mouseClick(button: try c.decode(Int.self, forKey: .button), pressed: try c.decode(Bool.self, forKey: .pressed))
            case .scroll: self = .scroll(dx: try c.decode(Double.self, forKey: .dx), dy: try c.decode(Double.self, forKey: .dy))
            case .key:    self = .key(scan: try c.decode(Int.self, forKey: .scan), pressed: try c.decode(Bool.self, forKey: .pressed), modifiers: try c.decode(Int.self, forKey: .modifiers))
            case .text:   self = .text(try c.decode(String.self, forKey: .text))
            }
        }
    }

    @Published public private(set) var isConnected = false
    @Published public private(set) var lastFrame: Frame?
    @Published public private(set) var lastError: String?

    private var task: URLSessionWebSocketTask?
    private let url: URL
    private let jwt: String?
    private let session: URLSession
    /// Predicate consulted at every `send(_:)`. Return false to drop the event
    /// and (when strict) also tear the socket down. Defaults to always-on so
    /// pre-grant callers still function; SessionView installs a real gate.
    public var gate: @Sendable () -> Bool = { true }

    public init(url: URL, jwt: String?, session: URLSession = .shared) {
        self.url = url
        self.jwt = jwt
        self.session = session
    }

    public func connect() {
        var req = URLRequest(url: url)
        if let jwt { req.setValue("Bearer \(jwt)", forHTTPHeaderField: "Authorization") }
        let t = session.webSocketTask(with: req)
        self.task = t
        t.resume()
        Task { @MainActor in self.isConnected = true }
        receive()
    }

    public func disconnect() {
        task?.cancel(with: .goingAway, reason: nil)
        task = nil
        Task { @MainActor in self.isConnected = false }
    }

    /// Send an input event. The caller is responsible for checking that
    /// control has actually been granted; the server will also reject
    /// mis-timed events but this belt-and-suspenders reduces useless
    /// round-trips.
    public func send(_ event: InputEvent) async {
        // The load-bearing gate: no input event leaves this method unless the
        // caller's supplied predicate approves. Callers can no longer forget
        // the check — it lives at the send boundary itself.
        guard gate() else {
            // Grant window expired mid-session: close the socket entirely so a
            // late-arriving event can't sneak through a re-opened window.
            self.disconnect()
            return
        }
        guard let task else { return }
        do {
            let data = try JSONEncoder().encode(event)
            try await task.send(.data(data))
        } catch {
            await MainActor.run { self.lastError = error.localizedDescription }
        }
    }

    private func receive() {
        task?.receive { [weak self] result in
            guard let self else { return }
            switch result {
            case .failure(let error):
                Task { @MainActor in
                    self.isConnected = false
                    self.lastError = error.localizedDescription
                }
            case .success(let msg):
                switch msg {
                case .data(let d):
                    Task { @MainActor in self.lastFrame = Frame(payload: d, receivedAt: Date()) }
                case .string:
                    // Control channel messages (grant-expired, anomaly-detected, etc.)
                    // are handled elsewhere; ignored here.
                    break
                @unknown default:
                    break
                }
                self.receive()
            }
        }
    }
}
