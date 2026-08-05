import Foundation
import Network

/// A Hearth we found on the local network via Bonjour.
public struct DiscoveredHearth: Identifiable, Hashable, Sendable {
    public let id: String              // Bonjour "name" — unique per Hearth
    public let host: String            // resolved hostname (e.g. pod.palpod.local)
    public let port: Int
    public let displayName: String     // human-friendly, from TXT record if provided

    public var baseURL: URL? {
        URL(string: "https://\(host):\(port)")
    }
}

/// Browses for `_hearth._tcp.local.` services on the LAN. Wraps
/// `NWBrowser` (the modern replacement for `NetServiceBrowser`).
@MainActor
public final class DiscoveryService: ObservableObject {
    @Published public private(set) var found: [DiscoveredHearth] = []
    @Published public private(set) var isSearching = false
    @Published public private(set) var lastError: String?

    private var browser: NWBrowser?

    public init() {}

    public func start() {
        guard browser == nil else { return }
        isSearching = true
        let params = NWParameters()
        params.includePeerToPeer = false
        let b = NWBrowser(for: .bonjour(type: "_hearth._tcp", domain: nil), using: params)

        b.stateUpdateHandler = { [weak self] state in
            guard let self else { return }
            Task { @MainActor in
                switch state {
                case .failed(let e): self.lastError = e.localizedDescription; self.isSearching = false
                case .cancelled:     self.isSearching = false
                default: break
                }
            }
        }

        b.browseResultsChangedHandler = { [weak self] results, _ in
            guard let self else { return }
            var next: [DiscoveredHearth] = []
            for r in results {
                if case let .service(name, _, _, _) = r.endpoint {
                    // Attempt to resolve host:port from the browse result's
                    // interfaces; we'll refine once the user picks one.
                    let host = "\(name).local"
                    let port = 8000
                    next.append(DiscoveredHearth(
                        id: name,
                        host: host,
                        port: port,
                        displayName: name
                    ))
                }
            }
            Task { @MainActor in self.found = next }
        }

        b.start(queue: .main)
        self.browser = b
    }

    public func stop() {
        browser?.cancel()
        browser = nil
        isSearching = false
    }
}
