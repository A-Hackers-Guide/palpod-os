package com.hearth.companion.uistyle

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.staticCompositionLocalOf

val LocalHearthColors = staticCompositionLocalOf { HearthColors }

private val DarkColors = darkColorScheme(
    primary = HearthColors.Pal,
    onPrimary = HearthColors.Void,
    secondary = HearthColors.Halo,
    onSecondary = HearthColors.Void,
    tertiary = HearthColors.Ember,
    background = HearthColors.Void,
    onBackground = HearthColors.Bone,
    surface = HearthColors.VoidLift,
    onSurface = HearthColors.Bone,
    surfaceVariant = HearthColors.Ink,
    onSurfaceVariant = HearthColors.BoneDim,
    outline = HearthColors.Line,
    error = HearthColors.Ember,
)

@Composable
fun HearthTheme(content: @Composable () -> Unit) {
    CompositionLocalProvider(LocalHearthColors provides HearthColors) {
        MaterialTheme(
            colorScheme = DarkColors,
            typography = HearthTypography,
            content = content,
        )
    }
}
