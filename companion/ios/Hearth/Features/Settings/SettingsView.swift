import SwiftUI

struct SettingsView: View {
    @EnvironmentObject var session: SessionModel

    var body: some View {
        NavigationStack {
            ZStack {
                HearthColors.void.ignoresSafeArea()
                List {
                    Section {
                        NavigationLink("About Hearth", destination: AboutView())
                            .foregroundStyle(HearthColors.bone)
                        NavigationLink("Advanced", destination: AdvancedView())
                            .foregroundStyle(HearthColors.bone)
                    }
                    .listRowBackground(HearthColors.slate)

                    Section {
                        Button(role: .destructive) {
                            KeychainStore().wipe()
                            session.stage = .discovery
                        } label: {
                            Text("Sign out & forget this Hearth")
                                .foregroundStyle(HearthColors.ember)
                        }
                    }
                    .listRowBackground(HearthColors.slate)
                }
                .insetGroupedList()
                .scrollContentBackground(.hidden)
            }
            .navigationTitle("Settings")
        }
    }
}
