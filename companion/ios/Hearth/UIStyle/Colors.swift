import SwiftUI

/// Hearth palette tokens. Names match the CSS custom properties used on the
/// marketing site and pal-web dashboard so cross-surface consistency is a
/// find-and-replace rather than a re-derivation.
enum HearthColors {
    /// Deep near-black ground. `--void`.
    static let void = Color(red: 0x0a / 255.0, green: 0x0a / 255.0, blue: 0x0c / 255.0)

    /// Slightly-lifted panel ground, used for cards and rows over `void`.
    static let slate = Color(red: 0x15 / 255.0, green: 0x17 / 255.0, blue: 0x1c / 255.0)

    /// Signature cyan — the accent every interactive control lands on. `--pal`.
    /// `#4FC3F7`
    static let pal = Color(red: 0x4f / 255.0, green: 0xc3 / 255.0, blue: 0xf7 / 255.0)

    /// Amber for status: countdown chips, "granted", warm accents. `--halo`.
    /// `#d4a256`
    static let halo = Color(red: 0xd4 / 255.0, green: 0xa2 / 255.0, blue: 0x56 / 255.0)

    /// Warm off-white for body text on dark grounds. `--bone`.
    /// `#e8e5de`
    static let bone = Color(red: 0xe8 / 255.0, green: 0xe5 / 255.0, blue: 0xde / 255.0)

    /// Muted bone for secondary text and captions.
    static let boneDim = Color(red: 0xe8 / 255.0, green: 0xe5 / 255.0, blue: 0xde / 255.0).opacity(0.55)

    /// Red used sparingly for destructive states and anomaly flags.
    static let ember = Color(red: 0xe2 / 255.0, green: 0x5a / 255.0, blue: 0x4c / 255.0)
}
