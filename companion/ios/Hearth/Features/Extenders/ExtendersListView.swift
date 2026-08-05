import SwiftUI

struct ExtendersListView: View {
    @EnvironmentObject var session: SessionModel
    @State private var extenders: [Extender] = []
    @State private var error: String?

    var body: some View {
        NavigationStack {
            ZStack {
                HearthColors.void.ignoresSafeArea()
                List(extenders) { ext in
                    NavigationLink { ExtenderDetailView(extender: ext) } label: {
                        HStack {
                            Image(systemName: "flame.fill")
                                .foregroundStyle(ext.online ? HearthColors.halo : HearthColors.boneDim)
                            VStack(alignment: .leading, spacing: 3) {
                                Text(ext.name)
                                    .font(HearthType.body(16, weight: .medium))
                                    .foregroundStyle(HearthColors.bone)
                                Text(ext.room ?? "Unassigned")
                                    .font(HearthType.spec(11))
                                    .foregroundStyle(HearthColors.boneDim)
                            }
                            Spacer()
                            Circle()
                                .fill(ext.online ? HearthColors.halo : HearthColors.boneDim)
                                .frame(width: 8, height: 8)
                        }
                    }
                    .listRowBackground(HearthColors.slate)
                }
                .listStyle(.plain)
                .scrollContentBackground(.hidden)
                .refreshable { await load() }
            }
            .navigationTitle("Embers")
        }
        .task { await load() }
    }

    @MainActor
    private func load() async {
        guard let client = session.client else { return }
        do { extenders = try await client.extenders() }
        catch { self.error = error.localizedDescription }
    }
}
