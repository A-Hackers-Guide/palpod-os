import SwiftUI

struct PlayTargetPicker: View {
    let item: MediaItem
    @EnvironmentObject var session: SessionModel
    @Environment(\.dismiss) var dismiss
    @State private var extenders: [Extender] = []
    @State private var error: String?

    var body: some View {
        ZStack {
            HearthColors.void.ignoresSafeArea()
            VStack(spacing: 12) {
                Text("Play on").sectionHeader().padding(.top, 12)
                Text(item.title)
                    .font(HearthType.display(20))
                    .foregroundStyle(HearthColors.bone)

                Button {
                    Task {
                        await play(target: PlayTarget(id: "hearth-main", displayName: "Hearth", kind: .hearth))
                    }
                } label: {
                    Label("Hearth main", systemImage: "flame.fill")
                }
                .buttonStyle(HearthPrimaryButton())
                .padding(.horizontal, 20)

                ForEach(extenders) { ext in
                    Button {
                        Task {
                            await play(target: PlayTarget(id: ext.id, displayName: ext.name, kind: .ember))
                        }
                    } label: {
                        Label(ext.name + (ext.room.map { " • \($0)" } ?? ""),
                              systemImage: "flame")
                    }
                    .buttonStyle(HearthSecondaryButton())
                    .padding(.horizontal, 20)
                    .disabled(!ext.online)
                }

                if let error {
                    Text(error).font(HearthType.body(13)).foregroundStyle(HearthColors.ember)
                }
                Spacer()
            }
        }
        .task { await loadExtenders() }
    }

    @MainActor
    private func loadExtenders() async {
        guard let client = session.client else { return }
        do { extenders = try await client.extenders() } catch {}
    }

    @MainActor
    private func play(target: PlayTarget) async {
        guard let client = session.client else { return }
        do {
            try await client.play(itemId: item.id, target: target)
            dismiss()
        } catch {
            self.error = error.localizedDescription
        }
    }
}
