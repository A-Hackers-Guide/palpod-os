import SwiftUI

// `@main` is applied only when building for iOS. Under SPM (macOS host,
// library target used for syntax verification) it would collide with
// `runner.swift`'s test entry point, which also owns `_main`.
#if os(iOS)
@main
#endif
struct HearthApp: App {
    @StateObject private var session = SessionModel()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environmentObject(session)
                .preferredColorScheme(.dark)
                .tint(HearthColors.pal)
        }
    }
}

/// Top-level session state. Holds the pairing status and injects the
/// `HearthClient` throughout the view tree once a Hearth is discovered
/// and the user has authenticated.
@MainActor
final class SessionModel: ObservableObject {
    enum Stage {
        case discovery
        case pairing(host: DiscoveredHearth)
        case login(client: HearthClient)
        case ready(client: HearthClient)
    }

    @Published var stage: Stage = .discovery

    /// The one and only place a HearthClient is retained. Views read
    /// this via `.client(from:)` helpers.
    var client: HearthClient? {
        switch stage {
        case .login(let c), .ready(let c): return c
        default: return nil
        }
    }
}

struct RootView: View {
    @EnvironmentObject var session: SessionModel

    var body: some View {
        switch session.stage {
        case .discovery:
            DiscoveryView()
        case .pairing(let host):
            QRPairView(host: host)
        case .login(let client):
            LoginView(client: client)
        case .ready:
            MainTabView()
        }
    }
}

struct MainTabView: View {
    var body: some View {
        TabView {
            DevicesListView()
                .tabItem { Label("Devices", systemImage: "display") }
            UsersView()
                .tabItem { Label("Household", systemImage: "person.3") }
            LibraryView()
                .tabItem { Label("Library", systemImage: "square.stack") }
            ExtendersListView()
                .tabItem { Label("Embers", systemImage: "flame") }
            SettingsView()
                .tabItem { Label("Settings", systemImage: "gearshape") }
        }
    }
}
