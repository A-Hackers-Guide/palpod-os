package com.hearth.companion.models

import kotlinx.serialization.Serializable

@Serializable
data class ControlGrant(
    val device_id: String,
    val granted_at: String,
    val expires_at: String,
    val minutes: Int,
    val rolling_24h_used_minutes: Int,
    val rolling_24h_cap_minutes: Int = 240,
)
