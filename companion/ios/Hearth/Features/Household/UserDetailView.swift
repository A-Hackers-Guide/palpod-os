import SwiftUI

struct UserDetailView: View {
    let user: HouseholdUser
    @EnvironmentObject var session: SessionModel
    @State private var axes: PersonalityAxes = .defaults
    @State private var loaded = false
    @State private var error: String?

    var body: some View {
        ZStack {
            HearthColors.void.ignoresSafeArea()
            ScrollView {
                VStack(spacing: 20) {
                    VStack(alignment: .leading, spacing: 8) {
                        Text(user.role.rawValue.uppercased()).sectionHeader()
                        Text(user.displayName)
                            .font(HearthType.display(30))
                            .foregroundStyle(HearthColors.bone)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)

                    section("Recognition") {
                        row("Face", user.faceEnrolled ? "Enrolled" : "Not enrolled",
                            color: user.faceEnrolled ? HearthColors.halo : HearthColors.boneDim)
                        row("Voice", user.voiceEnrolled ? "Enrolled" : "Not enrolled",
                            color: user.voiceEnrolled ? HearthColors.halo : HearthColors.boneDim)
                    }

                    VStack(alignment: .leading, spacing: 8) {
                        Text("Personality").sectionHeader()
                        PersonalitySlidersView(axes: $axes) { new in
                            Task { await save(new) }
                        }
                    }

                    VoicePresetPicker(current: user.voicePresetId)

                    if let error {
                        Text(error).font(HearthType.body(13)).foregroundStyle(HearthColors.ember)
                    }
                }
                .padding(20)
            }
        }
        .task { await load() }
    }

    private func section<Content: View>(_ title: String, @ViewBuilder content: () -> Content) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(title).sectionHeader()
            VStack(spacing: 0) { content() }
                .background(HearthColors.slate)
                .clipShape(RoundedRectangle(cornerRadius: 12))
        }
    }

    private func row(_ label: String, _ value: String, color: Color) -> some View {
        HStack {
            Text(label).font(HearthType.body(14)).foregroundStyle(HearthColors.bone)
            Spacer()
            Text(value).font(HearthType.spec(12)).foregroundStyle(color)
        }
        .padding(14)
    }

    @MainActor
    private func load() async {
        guard let client = session.client, !loaded else { return }
        do { axes = try await client.personality(userId: user.id) ; loaded = true }
        catch { self.error = error.localizedDescription }
    }

    @MainActor
    private func save(_ new: PersonalityAxes) async {
        guard let client = session.client else { return }
        do { try await client.updatePersonality(userId: user.id, axes: new) }
        catch { self.error = error.localizedDescription }
    }
}
