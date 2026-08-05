package com.hearth.companion.models

import kotlinx.serialization.Serializable

@Serializable
data class User(
    val id: String,
    val display_name: String,
    val face_recognition_enabled: Boolean = false,
    val voice_recognition_enabled: Boolean = false,
    val avatar_glyph: String = "person",
    val is_household_admin: Boolean = false,
    val voice_preset: String = "hearth-neutral",
)
