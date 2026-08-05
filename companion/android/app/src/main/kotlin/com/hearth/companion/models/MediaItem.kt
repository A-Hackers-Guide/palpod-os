package com.hearth.companion.models

import kotlinx.serialization.Serializable

enum class MediaSource { Plex, Jellyfin, Audiobookshelf, XTeVe, Steam }

@Serializable
data class MediaItem(
    val id: String,
    val title: String,
    val subtitle: String? = null,
    val kind: String, // movie, show, album, book, game, channel
    val source: String, // plex|jellyfin|audiobookshelf|xteve|steam
    val runtime_seconds: Int? = null,
    val year: Int? = null,
    val artwork_ref: String? = null, // local ref only, never a CDN URL
)
