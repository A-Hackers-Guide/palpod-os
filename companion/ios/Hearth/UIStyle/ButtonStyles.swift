import SwiftUI

/// Primary CTA. Filled `pal` cyan on `void`.
struct HearthPrimaryButton: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(HearthType.body(16, weight: .semibold))
            .foregroundStyle(HearthColors.void)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 14)
            .background(
                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .fill(HearthColors.pal.opacity(configuration.isPressed ? 0.75 : 1.0))
            )
    }
}

/// Secondary — outlined bone.
struct HearthSecondaryButton: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(HearthType.body(16, weight: .medium))
            .foregroundStyle(HearthColors.bone)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 14)
            .background(
                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .stroke(HearthColors.bone.opacity(configuration.isPressed ? 0.4 : 0.7), lineWidth: 1)
            )
    }
}

// NOTE: The visual style for the consent tap button lives inside
// `Core/ConsentGesture.swift` as a nested `fileprivate struct Style`, so
// it can only be attached to the sanctioned `ConsentTapButton` View.
// Defining a public ButtonStyle here would let any Button borrow the
// same look and read as "grant control" without going through the
// consent-gesture flow — that would be a design leak.
