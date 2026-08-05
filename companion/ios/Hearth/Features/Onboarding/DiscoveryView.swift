import SwiftUI

struct DiscoveryView: View {
    @EnvironmentObject var session: SessionModel
    @StateObject private var discovery = DiscoveryService()

    var body: some View {
        ZStack {
            HearthColors.void.ignoresSafeArea()
            VStack(spacing: 24) {
                VStack(spacing: 8) {
                    Text("HEARTH")
                        .font(HearthType.spec(11))
                        .tracking(3.6)
                        .foregroundStyle(HearthColors.boneDim)
                    Text("Looking for your Hearth")
                        .font(HearthType.display(30))
                        .foregroundStyle(HearthColors.bone)
                }
                .padding(.top, 60)

                if discovery.isSearching && discovery.found.isEmpty {
                    ProgressView()
                        .tint(HearthColors.pal)
                        .scaleEffect(1.4)
                        .padding(.top, 40)
                    Text("On the same Wi-Fi as your Hearth?")
                        .font(HearthType.body(14))
                        .foregroundStyle(HearthColors.boneDim)
                } else {
                    List(discovery.found) { hearth in
                        Button {
                            session.stage = .pairing(host: hearth)
                        } label: {
                            HStack {
                                VStack(alignment: .leading, spacing: 4) {
                                    Text(hearth.displayName)
                                        .font(HearthType.body(17, weight: .medium))
                                        .foregroundStyle(HearthColors.bone)
                                    Text("\(hearth.host):\(hearth.port)")
                                        .font(HearthType.spec(12))
                                        .foregroundStyle(HearthColors.boneDim)
                                }
                                Spacer()
                                Image(systemName: "chevron.right")
                                    .foregroundStyle(HearthColors.pal)
                            }
                            .padding(.vertical, 6)
                        }
                        .listRowBackground(HearthColors.slate)
                    }
                    .listStyle(.plain)
                    .scrollContentBackground(.hidden)
                }

                Spacer()

                if let error = discovery.lastError {
                    Text(error)
                        .font(HearthType.body(13))
                        .foregroundStyle(HearthColors.ember)
                        .padding()
                }

                Text("Nothing leaves the house.")
                    .font(HearthType.spec(10))
                    .tracking(1.6)
                    .foregroundStyle(HearthColors.halo)
                    .padding(.bottom, 30)
            }
        }
        .onAppear { discovery.start() }
        .onDisappear { discovery.stop() }
    }
}
