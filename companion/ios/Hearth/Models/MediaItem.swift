import Foundation

/// Unified media library item, spanning Plex/Jellyfin/Audiobookshelf/xTeVe/Steam.
struct MediaItem: Codable, Identifiable, Hashable, Sendable {
    let id: String
    let title: String
    let source: Source
    let kind: Kind
    let year: Int?
    let durationSeconds: Int?
    let posterPath: String?
    let watched: Bool

    enum Source: String, Codable, Sendable {
        case plex, jellyfin, audiobookshelf, xTeVe = "xteve", steam
    }

    enum Kind: String, Codable, Sendable {
        case movie, episode, series, audiobook, liveChannel = "live_channel", game
    }

    enum CodingKeys: String, CodingKey {
        case id, title, source, kind, year, watched
        case durationSeconds = "duration_seconds"
        case posterPath = "poster_path"
    }
}

/// The target of a `POST /api/play` call.
struct PlayTarget: Codable, Identifiable, Hashable, Sendable {
    let id: String
    let displayName: String
    let kind: Kind

    enum Kind: String, Codable, Sendable {
        case hearth, ember
    }

    enum CodingKeys: String, CodingKey {
        case id, kind
        case displayName = "display_name"
    }
}
