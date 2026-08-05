import SwiftUI

struct AboutView: View {
    var body: some View {
        ZStack {
            HearthColors.void.ignoresSafeArea()
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    Text("HEARTH")
                        .font(HearthType.spec(11))
                        .tracking(3.6)
                        .foregroundStyle(HearthColors.boneDim)
                    Text("Nothing leaves the house.")
                        .font(HearthType.display(28))
                        .foregroundStyle(HearthColors.bone)

                    Group {
                        para("The Hearth is a fully-offline luxury home AI and media server. Your voice, your face, your library, and every request stay on the box in your closet.")
                        para("This app is a thin control surface. It talks only to your Hearth, over your local network, and only after you've paired it in person.")
                    }

                    VStack(alignment: .leading, spacing: 8) {
                        Text("THIRD-PARTY SDKs BUNDLED IN THIS APP")
                            .sectionHeader()
                        Text("None.")
                            .font(HearthType.display(24))
                            .foregroundStyle(HearthColors.halo)
                        Text("No analytics. No crash reporters. No cloud sync. No push service. No account.")
                            .font(HearthType.body(13))
                            .foregroundStyle(HearthColors.boneDim)
                    }
                    .padding(14)
                    .background(HearthColors.slate)
                    .clipShape(RoundedRectangle(cornerRadius: 12))

                    VStack(alignment: .leading, spacing: 4) {
                        Text("Version 1.0.0 (1)")
                            .font(HearthType.spec(12))
                            .foregroundStyle(HearthColors.boneDim)
                        Text("Hearth Home, Inc.")
                            .font(HearthType.spec(12))
                            .foregroundStyle(HearthColors.boneDim)
                    }
                    .padding(.top, 20)
                }
                .padding(20)
                .frame(maxWidth: .infinity, alignment: .leading)
            }
        }
        .navigationTitle("About")
    }

    private func para(_ s: String) -> some View {
        Text(s)
            .font(HearthType.body(14))
            .foregroundStyle(HearthColors.bone)
            .lineSpacing(4)
    }
}
