import SwiftUI

struct UsersView: View {
    @EnvironmentObject var session: SessionModel
    @State private var users: [HouseholdUser] = []
    @State private var loading = false
    @State private var error: String?

    var body: some View {
        NavigationStack {
            ZStack {
                HearthColors.void.ignoresSafeArea()
                List(users) { user in
                    NavigationLink { UserDetailView(user: user) } label: {
                        HStack(spacing: 12) {
                            Circle()
                                .fill(HearthColors.slate)
                                .frame(width: 44, height: 44)
                                .overlay(
                                    Text(String(user.displayName.prefix(1)))
                                        .font(HearthType.display(20))
                                        .foregroundStyle(HearthColors.pal)
                                )
                            VStack(alignment: .leading, spacing: 3) {
                                Text(user.displayName)
                                    .font(HearthType.body(16, weight: .medium))
                                    .foregroundStyle(HearthColors.bone)
                                HStack(spacing: 8) {
                                    enrolledChip("Face", on: user.faceEnrolled)
                                    enrolledChip("Voice", on: user.voiceEnrolled)
                                }
                            }
                        }
                        .padding(.vertical, 4)
                    }
                    .listRowBackground(HearthColors.slate)
                }
                .listStyle(.plain)
                .scrollContentBackground(.hidden)
                .refreshable { await load() }
            }
            .navigationTitle("Household")
        }
        .task { await load() }
    }

    private func enrolledChip(_ label: String, on: Bool) -> some View {
        Text(label)
            .font(HearthType.spec(10))
            .padding(.horizontal, 6).padding(.vertical, 2)
            .foregroundStyle(on ? HearthColors.void : HearthColors.boneDim)
            .background(on ? HearthColors.halo : HearthColors.slate.opacity(0.6))
            .clipShape(Capsule())
    }

    @MainActor
    private func load() async {
        guard let client = session.client else { return }
        loading = true
        defer { loading = false }
        do { users = try await client.users() }
        catch { self.error = error.localizedDescription }
    }
}
