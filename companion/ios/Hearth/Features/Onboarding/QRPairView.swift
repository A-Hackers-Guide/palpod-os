import SwiftUI

struct QRPairView: View {
    let host: DiscoveredHearth
    @EnvironmentObject var session: SessionModel
    @State private var error: String?
    @State private var pairing = false

    var body: some View {
        ZStack {
            HearthColors.void.ignoresSafeArea()
#if canImport(AVFoundation) && canImport(UIKit) && os(iOS)
            QRScanner { url in
                Task { await handleURL(url) }
            }
            .ignoresSafeArea()
#endif
            VStack {
                Spacer()
                VStack(spacing: 16) {
                    Text("Scan the pairing QR")
                        .font(HearthType.display(24))
                        .foregroundStyle(HearthColors.bone)
                    Text("Open the Hearth Embers → Setup screen on your Hearth to display it.")
                        .font(HearthType.body(14))
                        .foregroundStyle(HearthColors.boneDim)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, 40)

                    if pairing {
                        ProgressView().tint(HearthColors.pal)
                    }
                    if let error {
                        Text(error)
                            .font(HearthType.body(13))
                            .foregroundStyle(HearthColors.ember)
                    }

                    Button("Cancel") {
                        session.stage = .discovery
                    }
                    .buttonStyle(HearthSecondaryButton())
                    .padding(.horizontal, 24)
                }
                .padding(24)
                .background(HearthColors.slate.opacity(0.9))
            }
        }
    }

    @MainActor
    private func handleURL(_ url: URL) async {
        guard let payload = PairPayload(url: url) else {
            error = "That QR isn't a Hearth pairing code."
            return
        }
        guard let baseURL = host.baseURL else {
            error = "Couldn't resolve \(host.host)."
            return
        }
        pairing = true
        defer { pairing = false }
        let client = HearthClient(baseURL: baseURL)
        do {
            _ = try await client.pair(token: payload.token, fingerprint: payload.fingerprint)
            session.stage = .login(client: client)
        } catch {
            self.error = error.localizedDescription
        }
    }
}
