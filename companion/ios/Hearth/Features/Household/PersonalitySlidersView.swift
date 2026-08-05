import SwiftUI

struct PersonalitySlidersView: View {
    @Binding var axes: PersonalityAxes
    var onCommit: (PersonalityAxes) -> Void

    var body: some View {
        VStack(spacing: 20) {
            axisSlider(
                value: $axes.reservedToChatty,
                labels: PersonalityAxes.reservedChattyLabels
            )
            axisSlider(
                value: $axes.formalToCasual,
                labels: PersonalityAxes.formalCasualLabels
            )
            axisSlider(
                value: $axes.seriousToPlayful,
                labels: PersonalityAxes.seriousPlayfulLabels
            )
        }
        .padding(16)
        .background(HearthColors.slate)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    private func axisSlider(
        value: Binding<Float>,
        labels: AxisLabels
    ) -> some View {
        VStack(spacing: 6) {
            HStack {
                Text(labels.leftEnd)
                    .font(HearthType.spec(11))
                    .foregroundStyle(HearthColors.boneDim)
                Spacer()
                Text(labels.rightEnd)
                    .font(HearthType.spec(11))
                    .foregroundStyle(HearthColors.boneDim)
            }
            Slider(value: value, in: 0...1) { editing in
                if !editing { onCommit(axes.clamped()) }
            }
            .tint(HearthColors.pal)
        }
    }
}
