import SwiftUI

struct LoginView: View {
    let client: HearthClient
    @EnvironmentObject var session: SessionModel
    @State private var password = ""
    @State private var error: String?
    @State private var busy = false

    var body: some View {
        ZStack {
            HearthColors.void.ignoresSafeArea()
            VStack(spacing: 20) {
                Spacer()
                Text("Hearth")
                    .font(HearthType.display(40))
                    .foregroundStyle(HearthColors.bone)
                Text("Device password")
                    .sectionHeader()

                SecureField("", text: $password)
                    .textFieldStyle(.plain)
                    .font(HearthType.body(18))
                    .foregroundStyle(HearthColors.bone)
                    .padding(14)
                    .background(HearthColors.slate)
                    .clipShape(RoundedRectangle(cornerRadius: 10))
                    .padding(.horizontal, 24)
                    .textContentType(.password)
                    .submitLabel(.go)
                    .onSubmit { Task { await tryLogin() } }

                if let error {
                    Text(error)
                        .font(HearthType.body(13))
                        .foregroundStyle(HearthColors.ember)
                        .padding(.horizontal, 24)
                }

                Button {
                    Task { await tryLogin() }
                } label: {
                    if busy { ProgressView().tint(HearthColors.void) }
                    else    { Text("Unlock") }
                }
                .buttonStyle(HearthPrimaryButton())
                .padding(.horizontal, 24)
                .disabled(password.isEmpty || busy)

                Spacer()
                Text("Nothing leaves the house.")
                    .font(HearthType.spec(10))
                    .tracking(1.6)
                    .foregroundStyle(HearthColors.halo)
                    .padding(.bottom, 30)
            }
        }
    }

    @MainActor
    private func tryLogin() async {
        busy = true
        defer { busy = false }
        do {
            _ = try await client.login(password: password)
            session.stage = .ready(client: client)
        } catch {
            self.error = error.localizedDescription
        }
    }
}
