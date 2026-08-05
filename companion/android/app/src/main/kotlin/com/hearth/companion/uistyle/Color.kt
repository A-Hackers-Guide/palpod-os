package com.hearth.companion.uistyle

import androidx.compose.ui.graphics.Color

/**
 * Hearth palette. Mirrors the iOS PAL tokens 1:1.
 *
 *   --void: near-black ground (#0A0B0D)
 *   --pal:  the cyan accent (#7CE6E4)
 *   --halo: warm amber for status/countdown (#F0B667)
 *   --bone: warm off-white body text (#EAE6DE)
 */
object HearthColors {
    val Void = Color(0xFF0A0B0D)
    val VoidLift = Color(0xFF14161A)      // one step above ground for cards
    val Ink = Color(0xFF1B1E24)           // sunken surfaces / inputs
    val Pal = Color(0xFF7CE6E4)
    val PalDim = Color(0xFF3F8B8A)
    val Halo = Color(0xFFF0B667)
    val HaloDim = Color(0xFF7A5F3A)
    val Bone = Color(0xFFEAE6DE)
    val BoneDim = Color(0xFF8E8B84)
    val Ember = Color(0xFFE85D5D)         // control-active / warning
    val Line = Color(0xFF2C3038)
}
