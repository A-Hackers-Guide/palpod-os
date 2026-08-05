import Foundation

/// Three-axis personality slider values. Every axis is a Float in [0,1].
/// The server clamps out-of-range values but we clamp on the way out too so
/// the UI never posts nonsense.
struct PersonalityAxes: Codable, Equatable, Sendable {
    /// 0 = reserved, 1 = chatty.
    var reservedToChatty: Float
    /// 0 = formal, 1 = casual.
    var formalToCasual: Float
    /// 0 = serious, 1 = playful.
    var seriousToPlayful: Float

    static let defaults = PersonalityAxes(
        reservedToChatty: 0.5,
        formalToCasual: 0.5,
        seriousToPlayful: 0.5
    )

    enum CodingKeys: String, CodingKey {
        case reservedToChatty = "reserved_to_chatty"
        case formalToCasual = "formal_to_casual"
        case seriousToPlayful = "serious_to_playful"
    }

    /// Returns a copy with every axis constrained to [0,1].
    func clamped() -> PersonalityAxes {
        PersonalityAxes(
            reservedToChatty: min(max(reservedToChatty, 0), 1),
            formalToCasual: min(max(formalToCasual, 0), 1),
            seriousToPlayful: min(max(seriousToPlayful, 0), 1)
        )
    }
}

/// The labels the UI shows at each end of an axis.
struct AxisLabels {
    let leftEnd: String
    let rightEnd: String
}

extension PersonalityAxes {
    static let reservedChattyLabels = AxisLabels(leftEnd: "Reserved", rightEnd: "Chatty")
    static let formalCasualLabels = AxisLabels(leftEnd: "Formal", rightEnd: "Casual")
    static let seriousPlayfulLabels = AxisLabels(leftEnd: "Serious", rightEnd: "Playful")
}
