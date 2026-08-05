import Foundation

/// A household member. Face/voice profiles live on the Hearth; the app
/// only sees status booleans and never touches raw biometrics.
struct HouseholdUser: Codable, Identifiable, Hashable, Sendable {
    let id: String
    let displayName: String
    let role: Role
    let faceEnrolled: Bool
    let voiceEnrolled: Bool
    let voicePresetId: String?

    enum Role: String, Codable, Sendable {
        case owner, adult, teen, child, guestUser = "guest"
    }

    enum CodingKeys: String, CodingKey {
        case id, role
        case displayName = "display_name"
        case faceEnrolled = "face_enrolled"
        case voiceEnrolled = "voice_enrolled"
        case voicePresetId = "voice_preset_id"
    }
}
