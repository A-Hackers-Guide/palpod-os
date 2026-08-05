import SwiftUI

struct DeviceRow: View {
    let device: RemoteDevice
    @State private var now = Date()
    private let ticker = Timer.publish(every: 1, on: .main, in: .common).autoconnect()

    var body: some View {
        HStack(alignment: .center, spacing: 14) {
            Image(systemName: iconName(for: device.kind))
                .font(.system(size: 22))
                .foregroundStyle(HearthColors.pal)
                .frame(width: 34)

            VStack(alignment: .leading, spacing: 3) {
                Text(device.name)
                    .font(HearthType.body(16, weight: .semibold))
                    .foregroundStyle(HearthColors.bone)
                Group {
                    if device.isControlGranted {
                        Text("Granted • \(formatRemaining()) left")
                            .foregroundStyle(HearthColors.halo)
                    } else {
                        Text("View-only")
                            .foregroundStyle(HearthColors.boneDim)
                    }
                }
                .font(HearthType.spec(12))
            }

            Spacer()

            if device.isControlGranted {
                CountdownDot(remaining: device.remainingSeconds)
            }
        }
        .padding(.vertical, 8)
        .onReceive(ticker) { now = $0 }
    }

    private func formatRemaining() -> String {
        let secs = device.remainingSeconds
        let m = secs / 60, s = secs % 60
        return String(format: "%d:%02d", m, s)
    }

    private func iconName(for kind: RemoteDevice.Kind) -> String {
        switch kind {
        case .desktop: return "desktopcomputer"
        case .laptop:  return "laptopcomputer"
        case .tv:      return "tv"
        case .tablet:  return "ipad"
        case .phone:   return "iphone"
        case .other:   return "square.stack.3d.up"
        }
    }
}

struct CountdownDot: View {
    let remaining: Int
    var body: some View {
        Circle()
            .fill(HearthColors.halo)
            .frame(width: 10, height: 10)
            .overlay(
                Circle()
                    .stroke(HearthColors.halo.opacity(0.3), lineWidth: 8)
                    .scaleEffect(1 + min(0.6, CGFloat(remaining) / 3600))
            )
    }
}
