import SwiftUI
import MetalKit

/// A live view-only (or granted-control) session onto a remote device.
/// Streams frames via WebSocket, renders them to a Metal-backed view, and
/// forwards touch input as `WebSocketClient.InputEvent`s.
struct SessionView: View {
    let session: RemoteSession
    let device: RemoteDevice

    @EnvironmentObject var appSession: SessionModel
    @StateObject private var ws: WebSocketClient
    @State private var dragStart: CGPoint?

    init(session: RemoteSession, device: RemoteDevice, client: HearthClient, keychain: KeychainStore = KeychainStore()) {
        self.session = session
        self.device = device
        // Compose wss:// URL from the authenticated baseURL + wsPath returned by openSession.
        // Reuse `client.urlSession` so the same TLS pinning delegate applies to the handshake.
        let base = client.baseURL
        var comps = URLComponents(url: base, resolvingAgainstBaseURL: false)!
        comps.scheme = base.scheme == "https" ? "wss" : "ws"
        comps.path = session.wsPath
        let wsURL = comps.url ?? URL(string: "wss://" + (base.host ?? "hearth.local") + session.wsPath)!
        _ws = StateObject(wrappedValue: WebSocketClient(
            url: wsURL,
            jwt: keychain.string(for: .jwt),
            session: client.urlSession
        ))
    }

    var body: some View {
        ZStack {
            HearthColors.void.ignoresSafeArea()
            VStack(spacing: 0) {
                header
                framePane
                controlBar
            }
        }
        .onAppear {
            let dev = device
            ws.gate = { dev.isControlGranted }
            ws.connect()
        }
        .onDisappear { ws.disconnect() }
    }

    private var header: some View {
        HStack {
            Text(device.name)
                .font(HearthType.body(15, weight: .medium))
                .foregroundStyle(HearthColors.bone)
            Spacer()
            Circle()
                .fill(ws.isConnected ? HearthColors.halo : HearthColors.ember)
                .frame(width: 8, height: 8)
            Text(ws.isConnected ? "LIVE" : "OFFLINE")
                .font(HearthType.spec(10))
                .tracking(1.4)
                .foregroundStyle(HearthColors.boneDim)
        }
        .padding(12)
        .background(HearthColors.slate)
    }

    private var framePane: some View {
        ZStack {
            Rectangle().fill(HearthColors.void)
            if let frame = ws.lastFrame {
                Text("Frame \(frame.payload.count) B @ \(frame.receivedAt.formatted(date: .omitted, time: .standard))")
                    .font(HearthType.spec(11))
                    .foregroundStyle(HearthColors.boneDim)
            } else {
                ProgressView().tint(HearthColors.pal)
            }
        }
        .gesture(
            DragGesture(minimumDistance: 0)
                .onChanged { g in
                    guard device.isControlGranted else { return }
                    Task {
                        await ws.send(.mouseMove(x: Double(g.location.x), y: Double(g.location.y)))
                    }
                }
                .onEnded { g in
                    guard device.isControlGranted else { return }
                    Task {
                        await ws.send(.mouseClick(button: 0, pressed: true))
                        try? await Task.sleep(nanoseconds: 40_000_000)
                        await ws.send(.mouseClick(button: 0, pressed: false))
                    }
                }
        )
    }

    private var controlBar: some View {
        HStack {
            if device.isControlGranted {
                Label("Control granted", systemImage: "hand.tap")
                    .font(HearthType.spec(11))
                    .foregroundStyle(HearthColors.halo)
            } else {
                Label("View-only", systemImage: "eye")
                    .font(HearthType.spec(11))
                    .foregroundStyle(HearthColors.boneDim)
            }
            Spacer()
        }
        .padding(12)
        .background(HearthColors.slate)
    }
}
