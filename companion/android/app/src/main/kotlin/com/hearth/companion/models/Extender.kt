package com.hearth.companion.models

import kotlinx.serialization.Serializable

@Serializable
data class Extender(
    val id: String,
    val room: String,
    val model: String = "Hearth Ember",
    val firmware: String,
    val online: Boolean,
    val last_seen_ts: String? = null,
    val paired_at: String,
)
