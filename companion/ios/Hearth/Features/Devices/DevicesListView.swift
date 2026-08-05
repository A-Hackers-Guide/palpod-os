import SwiftUI

@MainActor
final class DevicesViewModel: ObservableObject {
    @Published var devices: [RemoteDevice] = []
    @Published var error: String?
    @Published var loading = false

    private let client: HearthClient
    init(client: HearthClient) { self.client = client }

    func refresh() async {
        loading = true
        defer { loading = false }
        do { devices = try await client.devices() }
        catch { self.error = error.localizedDescription }
    }
}

struct DevicesListView: View {
    @EnvironmentObject var session: SessionModel
    @StateObject private var vm: DevicesViewModel

    init() {
        // The environmentObject can't be read here; use a placeholder VM
        // and rehydrate in .task once we can reach the session.
        let placeholder = HearthClient(baseURL: URL(string: "http://placeholder.invalid")!)
        _vm = StateObject(wrappedValue: DevicesViewModel(client: placeholder))
    }

    var body: some View {
        NavigationStack {
            ZStack {
                HearthColors.void.ignoresSafeArea()
                content
            }
            .navigationTitle("Devices")
#if os(iOS)
            .toolbarBackground(HearthColors.void, for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
#endif
        }
        .task { await refreshIfClient() }
    }

    @ViewBuilder private var content: some View {
        if vm.loading && vm.devices.isEmpty {
            ProgressView().tint(HearthColors.pal)
        } else if vm.devices.isEmpty {
            VStack(spacing: 12) {
                Image(systemName: "display.trianglebadge.exclamationmark")
                    .font(.system(size: 44))
                    .foregroundStyle(HearthColors.boneDim)
                Text("No paired devices yet.")
                    .font(HearthType.body(15))
                    .foregroundStyle(HearthColors.boneDim)
            }
        } else {
            List(vm.devices) { device in
                NavigationLink {
                    DeviceDetailView(device: device)
                } label: {
                    DeviceRow(device: device)
                }
                .listRowBackground(HearthColors.slate)
            }
            .listStyle(.plain)
            .scrollContentBackground(.hidden)
            .refreshable { await refreshIfClient() }
        }
    }

    private func refreshIfClient() async {
        guard let client = session.client else { return }
        // Reseat VM's client if we're still on the placeholder.
        let live = DevicesViewModel(client: client)
        vm.devices = []
        vm.error = nil
        // Hand off — we intentionally never expose the placeholder in UI.
        await live.refresh()
        vm.devices = live.devices
        vm.error = live.error
    }
}
