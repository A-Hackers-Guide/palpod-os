import SwiftUI

struct DeviceDetailView: View {
    let device: RemoteDevice
    @State private var showGrantSheet = false
    @State private var showAnomalies = false
    @State private var activeSession: RemoteSession?
    @EnvironmentObject var session: SessionModel
    @State private var error: String?

    var body: some View {
        ZStack {
            HearthColors.void.ignoresSafeArea()
            ScrollView {
                VStack(spacing: 20) {
                    header

                    if device.isControlGranted {
                        grantedCard
                    } else {
                        viewOnlyCard
                    }

                    Button {
                        Task { await openSession() }
                    } label: {
                        Label("Open live view", systemImage: "play.rectangle")
                    }
                    .buttonStyle(HearthPrimaryButton())

                    Button {
                        showAnomalies = true
                    } label: {
                        Label("Audit log", systemImage: "list.bullet.rectangle")
                    }
                    .buttonStyle(HearthSecondaryButton())

                    if let error {
                        Text(error)
                            .font(HearthType.body(13))
                            .foregroundStyle(HearthColors.ember)
                    }
                }
                .padding(24)
            }
        }
        .navigationTitle(device.name)
        .sheet(isPresented: $showGrantSheet) {
            if let client = session.client {
                GrantControlSheet(device: device, client: client) { showGrantSheet = false }
                    .presentationDetents([.medium])
            }
        }
        .sheet(item: $activeSession) { rs in
            if let client = session.client {
                SessionView(session: rs, device: device, client: client)
            }
        }
        .sheet(isPresented: $showAnomalies) {
            if let client = session.client, let sess = activeSession {
                AnomalyLogView(client: client, sessionId: sess.id)
            }
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(device.kind.rawValue.uppercased())
                .sectionHeader()
            Text(device.name)
                .font(HearthType.display(30))
                .foregroundStyle(HearthColors.bone)
            if let last = device.lastSeen {
                Text("Last seen \(last.formatted(.relative(presentation: .named)))")
                    .font(HearthType.spec(12))
                    .foregroundStyle(HearthColors.boneDim)
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }

    private var viewOnlyCard: some View {
        VStack(spacing: 12) {
            Text("View-only")
                .font(HearthType.body(17, weight: .semibold))
                .foregroundStyle(HearthColors.bone)
            Text("The Hearth can watch this screen but cannot control it until you grant control.")
                .font(HearthType.body(13))
                .foregroundStyle(HearthColors.boneDim)
                .multilineTextAlignment(.center)
            Button("Grant control") { showGrantSheet = true }
                .buttonStyle(HearthPrimaryButton())
        }
        .padding(20)
        .background(HearthColors.slate)
        .clipShape(RoundedRectangle(cornerRadius: 14))
    }

    private var grantedCard: some View {
        VStack(spacing: 12) {
            HStack(spacing: 8) {
                Circle().fill(HearthColors.halo).frame(width: 10, height: 10)
                Text("Control granted")
                    .font(HearthType.body(17, weight: .semibold))
                    .foregroundStyle(HearthColors.bone)
            }
            if let until = device.grantedUntil {
                Text("Until \(until.formatted(date: .omitted, time: .shortened))")
                    .font(HearthType.spec(13))
                    .foregroundStyle(HearthColors.halo)
            }
            Button("Revoke now", role: .destructive) {
                Task { await revoke() }
            }
            .buttonStyle(HearthSecondaryButton())
        }
        .padding(20)
        .background(HearthColors.slate)
        .clipShape(RoundedRectangle(cornerRadius: 14))
    }

    @MainActor
    private func openSession() async {
        guard let client = session.client else { return }
        do { activeSession = try await client.openSession(deviceId: device.id) }
        catch { self.error = error.localizedDescription }
    }

    @MainActor
    private func revoke() async {
        guard let client = session.client else { return }
        do { try await client.revokeControl(deviceId: device.id) }
        catch { self.error = error.localizedDescription }
    }
}
