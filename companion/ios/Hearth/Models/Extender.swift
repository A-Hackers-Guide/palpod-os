import Foundation

/// A paired Hearth Ember ($8,999 extender).
struct Extender: Codable, Identifiable, Hashable, Sendable {
    let id: String
    let name: String
    let room: String?
    let serial: String
    let firmwareVersion: String
    let online: Bool
    let signalRssi: Int?

    enum CodingKeys: String, CodingKey {
        case id, name, room, serial, online
        case firmwareVersion = "firmware_version"
        case signalRssi = "signal_rssi"
    }
}
