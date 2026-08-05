import Foundation

/// Server response for `POST /api/remote/devices/{id}/grant-control`.
struct ControlGrant: Codable, Sendable {
    let deviceId: String
    let expiresAt: Date
    let sessionId: String
    /// Rolling 24h control minutes already used, out of the 240-minute cap.
    let usedMinutesLast24h: Int

    enum CodingKeys: String, CodingKey {
        case deviceId = "device_id"
        case expiresAt = "expires_at"
        case sessionId = "session_id"
        case usedMinutesLast24h = "used_minutes_last_24h"
    }
}

/// Anomaly / audit event from `GET /api/remote/sessions/{id}/anomalies`.
struct SessionAnomaly: Codable, Identifiable, Sendable {
    let id: String
    let sessionId: String
    let kind: String
    let message: String
    let severity: Severity
    let at: Date

    enum Severity: String, Codable, Sendable { case info, warn, critical }

    enum CodingKeys: String, CodingKey {
        case id, kind, message, severity, at
        case sessionId = "session_id"
    }
}
