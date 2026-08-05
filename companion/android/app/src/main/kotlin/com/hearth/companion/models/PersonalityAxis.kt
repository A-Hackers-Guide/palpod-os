package com.hearth.companion.models

import kotlinx.serialization.Serializable

enum class PersonalityAxis(val displayName: String, val leftLabel: String, val rightLabel: String) {
    Reserve("Cadence", "Reserved", "Chatty"),
    Register("Register", "Formal", "Casual"),
    Levity("Levity", "Serious", "Playful"),
}

@Serializable
data class PersonalityAxes(
    /** 0f (reserved) .. 1f (chatty) */
    val reserved_chatty: Float = 0.5f,
    /** 0f (formal) .. 1f (casual) */
    val formal_casual: Float = 0.5f,
    /** 0f (serious) .. 1f (playful) */
    val serious_playful: Float = 0.5f,
) {
    fun value(axis: PersonalityAxis): Float = when (axis) {
        PersonalityAxis.Reserve -> reserved_chatty
        PersonalityAxis.Register -> formal_casual
        PersonalityAxis.Levity -> serious_playful
    }

    fun set(axis: PersonalityAxis, v: Float): PersonalityAxes = when (axis) {
        PersonalityAxis.Reserve -> copy(reserved_chatty = v)
        PersonalityAxis.Register -> copy(formal_casual = v)
        PersonalityAxis.Levity -> copy(serious_playful = v)
    }
}
