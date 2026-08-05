import SwiftUI

/// The load-bearing consent UI.
///
/// This is the ONLY sheet that hosts `ConsentTapButton`s. Each button
/// mints a `ConsentGesture` — see `ConsentGesture.swift` for the
/// full argument that this is the only path in the codebase that can do
/// so. `HearthClient.grantControl(deviceId:gesture:)` demands one at the
/// type level. Together these enforce that no `/grant-control` request
/// ever leaves the device without a physical tap on this sheet.
struct GrantControlSheet: View {
    let device: RemoteDevice
    let client: HearthClient
    let onDismiss: () -> Void

    @State private var busy = false
    @State private var error: String?
    @State private var success: ControlGrant?

    var body: some View {
        ZStack {
            HearthColors.void.ignoresSafeArea()
            VStack(spacing: 20) {
                Text("GRANT CONTROL")
                    .sectionHeader()
                Text("Let Hearth control")
                    .font(HearthType.display(24))
                    .foregroundStyle(HearthColors.bone)
                Text(device.name)
                    .font(HearthType.display(30))
                    .foregroundStyle(HearthColors.pal)

                Text("Choose a duration. Tap the button to grant.")
                    .font(HearthType.body(13))
                    .foregroundStyle(HearthColors.boneDim)
                    .multilineTextAlignment(.center)
                    .padding(.horizontal, 32)

                VStack(spacing: 14) {
                    ForEach([15, 30, 60], id: \.self) { minutes in
                        // === THE ONLY ConsentTapButton IN THE APP. ===
                        // Every button below is a real SwiftUI tap.
                        // Its action closure is the only construction
                        // site of `_TapWitness`, and therefore the only
                        // construction site of `ConsentGesture`.
                        ConsentTapButton(
                            deviceId: device.id,
                            durationMinutes: minutes,
                            label: "\(minutes) minutes"
                        ) { gesture in
                            Task { await performGrant(with: gesture) }
                        }
                        .disabled(busy)
                    }
                }
                .padding(.horizontal, 24)

                if busy { ProgressView().tint(HearthColors.pal) }

                if let error {
                    Text(error)
                        .font(HearthType.body(13))
                        .foregroundStyle(HearthColors.ember)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, 24)
                }

                if let grant = success {
                    Text("Granted until \(grant.expiresAt.formatted(date: .omitted, time: .shortened))")
                        .font(HearthType.spec(12))
                        .foregroundStyle(HearthColors.halo)
                }

                Spacer()

                Button("Cancel") { onDismiss() }
                    .buttonStyle(HearthSecondaryButton())
                    .padding(.horizontal, 24)
                    .padding(.bottom, 30)
            }
            .padding(.top, 24)
        }
    }

    @MainActor
    private func performGrant(with gesture: ConsentGesture) async {
        busy = true
        error = nil
        defer { busy = false }
        do {
            let grant = try await client.grantControl(deviceId: device.id, gesture: gesture)
            self.success = grant
            try? await Task.sleep(nanoseconds: 700_000_000)
            onDismiss()
        } catch {
            self.error = error.localizedDescription
        }
    }
}
