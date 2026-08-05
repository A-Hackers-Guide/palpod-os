import SwiftUI

struct ExtenderDetailView: View {
    let extender: Extender

    var body: some View {
        ZStack {
            HearthColors.void.ignoresSafeArea()
            ScrollView {
                VStack(spacing: 20) {
                    Image(systemName: "flame.fill")
                        .font(.system(size: 60))
                        .foregroundStyle(extender.online ? HearthColors.halo : HearthColors.boneDim)
                        .padding(.top, 30)
                    Text(extender.name)
                        .font(HearthType.display(30))
                        .foregroundStyle(HearthColors.bone)

                    VStack(spacing: 0) {
                        row("Room",     extender.room ?? "—")
                        Divider().overlay(HearthColors.void)
                        row("Serial",   extender.serial)
                        Divider().overlay(HearthColors.void)
                        row("Firmware", extender.firmwareVersion)
                        Divider().overlay(HearthColors.void)
                        row("Status",   extender.online ? "Online" : "Offline",
                            valueColor: extender.online ? HearthColors.halo : HearthColors.ember)
                        if let rssi = extender.signalRssi {
                            Divider().overlay(HearthColors.void)
                            row("Signal", "\(rssi) dBm")
                        }
                    }
                    .background(HearthColors.slate)
                    .clipShape(RoundedRectangle(cornerRadius: 12))
                    .padding(.horizontal, 20)

                    Spacer()
                }
            }
        }
        .navBarTitleInline()
    }

    private func row(_ label: String, _ value: String, valueColor: Color = HearthColors.bone) -> some View {
        HStack {
            Text(label).font(HearthType.body(14)).foregroundStyle(HearthColors.boneDim)
            Spacer()
            Text(value).font(HearthType.spec(12)).foregroundStyle(valueColor)
        }
        .padding(14)
    }
}
