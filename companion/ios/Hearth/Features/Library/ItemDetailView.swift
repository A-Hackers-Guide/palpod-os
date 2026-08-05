import SwiftUI

struct ItemDetailView: View {
    let item: MediaItem
    @State private var showTargets = false

    var body: some View {
        ZStack {
            HearthColors.void.ignoresSafeArea()
            ScrollView {
                VStack(spacing: 20) {
                    RoundedRectangle(cornerRadius: 12)
                        .fill(HearthColors.slate)
                        .aspectRatio(2/3, contentMode: .fit)
                        .frame(maxWidth: 260)
                        .overlay(
                            Text(String(item.title.prefix(1)))
                                .font(HearthType.display(60))
                                .foregroundStyle(HearthColors.boneDim)
                        )
                    VStack(spacing: 6) {
                        Text(item.source.rawValue.uppercased())
                            .sectionHeader()
                        Text(item.title)
                            .font(HearthType.display(28))
                            .foregroundStyle(HearthColors.bone)
                            .multilineTextAlignment(.center)
                        if let year = item.year {
                            Text(String(year))
                                .font(HearthType.spec(12))
                                .foregroundStyle(HearthColors.boneDim)
                        }
                    }
                    Button {
                        showTargets = true
                    } label: {
                        Label("Play on…", systemImage: "play.fill")
                    }
                    .buttonStyle(HearthPrimaryButton())
                    .padding(.horizontal, 20)
                }
                .padding(20)
            }
        }
        .navBarTitleInline()
        .sheet(isPresented: $showTargets) {
            PlayTargetPicker(item: item)
                .presentationDetents([.medium])
        }
    }
}
