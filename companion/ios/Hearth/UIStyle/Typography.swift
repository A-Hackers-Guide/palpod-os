import SwiftUI
#if canImport(UIKit)
import UIKit
#endif

/// Type ramp. Bodoni for editorial/display, SF Mono for spec/technical detail,
/// SF for body. We fall back to system serif/mono when the Bodoni face is not
/// bundled on the device.
enum HearthType {
    static func display(_ size: CGFloat) -> Font {
        // Bodoni is present in the iOS system font list (BodoniSvtyTwoITCTT-Book).
        // Fallback to `.serif` design keeps the layout intact if it ever isn't.
#if canImport(UIKit) && os(iOS)
        if let uiFont = UIFont(name: "BodoniSvtyTwoITCTT-Book", size: size) {
            return Font(uiFont)
        }
#endif
        return .system(size: size, weight: .regular, design: .serif)
    }

    static func spec(_ size: CGFloat) -> Font {
        .system(size: size, weight: .regular, design: .monospaced)
    }

    static func body(_ size: CGFloat = 15, weight: Font.Weight = .regular) -> Font {
        .system(size: size, weight: weight, design: .default)
    }
}

/// Small view-modifier convenience for section headers.
struct SectionHeader: ViewModifier {
    func body(content: Content) -> some View {
        content
            .font(HearthType.spec(11))
            .textCase(.uppercase)
            .tracking(1.4)
            .foregroundStyle(HearthColors.boneDim)
    }
}

extension View {
    func sectionHeader() -> some View { modifier(SectionHeader()) }
}
