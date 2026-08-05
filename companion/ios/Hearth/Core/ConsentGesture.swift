import SwiftUI

// MARK: - The load-bearing consent primitive
//
// This file is the entire enforcement surface for the "no control grant
// without a physical user tap" invariant. It uses Swift access-control to
// make bypass structurally impossible:
//
//  1. `ConsentGesture` has NO public initializer. Its only initializer
//     takes a `_TapWitness`.
//  2. `_TapWitness` has a `fileprivate` initializer. Nothing outside this
//     file can construct one — including `@testable import`, subclasses,
//     extensions in other files, or Mirror-based reflection.
//
// The ONLY place in the codebase that constructs a `_TapWitness` is the
// Button action closure of `ConsentTapButton` below, which is a SwiftUI
// Button wired to a real touch. Therefore the ONLY way to obtain a
// `ConsentGesture` is for the user to physically tap that Button.
//
// `ConsentTokenSource.header(for:)` (in a separate file) demands a
// `ConsentGesture` at the type level, so the `X-Consent-Origin: user-tap`
// header is not synthesisable outside this file.

/// A record that a user physically tapped a specific grant duration for a
/// specific device. Cannot be constructed except by the SwiftUI tap
/// closure inside `ConsentTapButton` in this same file.
public struct ConsentGesture: Sendable {
    public let deviceId: String
    public let durationMinutes: Int
    public let capturedAt: Date

    /// The witness this instance carries. Its type is fileprivate; there
    /// is no way to synthesize one outside this file.
    internal let witness: _TapWitness

    fileprivate init(deviceId: String, durationMinutes: Int, witness: _TapWitness) {
        self.deviceId = deviceId
        self.durationMinutes = durationMinutes
        self.capturedAt = Date()
        self.witness = witness
    }
}

/// A zero-size witness type whose sole purpose is to be un-constructible
/// outside this file. Its type is `internal` so `ConsentTokenSource`
/// (same module, different file) can name it in a signature, but its
/// initializer is `fileprivate` so ONLY this file can create one.
struct _TapWitness: Sendable {
    fileprivate init() {}
}

// MARK: - The single UI affordance that mints a ConsentGesture

/// A SwiftUI Button whose action closure is the only place in the app that
/// constructs a `ConsentGesture`. Consumers hand it the device id,
/// duration, and a closure to receive the freshly-minted gesture.
///
/// Note: the action closure below is the sole physical location where
/// `_TapWitness()` is called. Every other line in the codebase is
/// forbidden by the access-control rules above from constructing one.
public struct ConsentTapButton: View {
    private let deviceId: String
    private let durationMinutes: Int
    private let label: String
    private let onConsent: (ConsentGesture) -> Void

    public init(
        deviceId: String,
        durationMinutes: Int,
        label: String,
        onConsent: @escaping (ConsentGesture) -> Void
    ) {
        self.deviceId = deviceId
        self.durationMinutes = durationMinutes
        self.label = label
        self.onConsent = onConsent
    }

    public var body: some View {
        Button {
            // === THE ONE CONSTRUCTION SITE. ===
            //
            // A real UIKit touch drove SwiftUI to invoke this closure.
            // Anything else that wanted to fire this — say, a synthesised
            // AccessibilityAction — would show up as a hit on this exact
            // line in a stack trace. Auditors: put a breakpoint here.
            let witness = _TapWitness()
            let gesture = ConsentGesture(
                deviceId: deviceId,
                durationMinutes: durationMinutes,
                witness: witness
            )
            onConsent(gesture)
        } label: {
            Text(label)
        }
        .buttonStyle(ConsentTapButton.Style())
    }

    /// Nested style so callers don't have to import `UIStyle/ButtonStyles.swift`
    /// to render the correct visual.
    fileprivate struct Style: ButtonStyle {
        func makeBody(configuration: Configuration) -> some View {
            configuration.label
                .font(HearthType.display(28))
                .foregroundStyle(HearthColors.void)
                .frame(maxWidth: .infinity, minHeight: 72)
                .background(
                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                        .fill(HearthColors.pal.opacity(configuration.isPressed ? 0.75 : 1.0))
                        .shadow(color: HearthColors.pal.opacity(0.35),
                                radius: configuration.isPressed ? 4 : 16, y: 8)
                )
                .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
                .animation(.easeOut(duration: 0.12), value: configuration.isPressed)
        }
    }
}
