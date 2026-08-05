package com.hearth.companion.features.household

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.hearth.companion.HearthApp
import com.hearth.companion.models.PersonalityAxes
import com.hearth.companion.models.PersonalityAxis
import com.hearth.companion.models.User
import com.hearth.companion.uistyle.HearthColors
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

@Composable
fun PersonalitySlidersScreen(app: HearthApp, user: User) {
    var axes by remember { mutableStateOf(PersonalityAxes()) }
    val scope = rememberCoroutineScope()
    val saveJobHolder = remember { arrayOfNulls<Job>(1) }

    LaunchedEffect(user.id) {
        runCatching { app.buildClient()!!.api.personality(user.id) }
            .onSuccess { axes = it }
    }

    Column(Modifier.padding(vertical = 8.dp)) {
        Text("Personality", color = HearthColors.Bone,
            style = MaterialTheme.typography.titleLarge)
        Text("How Hearth responds when this person speaks or is on-screen.",
            color = HearthColors.BoneDim,
            modifier = Modifier.padding(vertical = 6.dp))

        PersonalityAxis.values().forEach { axis ->
            Text(axis.displayName, color = HearthColors.Pal,
                style = MaterialTheme.typography.labelLarge,
                modifier = Modifier.padding(top = 14.dp, bottom = 4.dp))
            Row(Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween) {
                Text(axis.leftLabel, color = HearthColors.BoneDim,
                    style = MaterialTheme.typography.labelSmall)
                Text(axis.rightLabel, color = HearthColors.BoneDim,
                    style = MaterialTheme.typography.labelSmall)
            }
            Slider(
                value = axes.value(axis),
                onValueChange = { v ->
                    axes = axes.set(axis, v)
                    saveJobHolder[0]?.cancel()
                    saveJobHolder[0] = scope.launch {
                        delay(400)
                        runCatching {
                            val client = app.buildClient()!!
                            val csrf = app.store.csrf() ?: return@runCatching
                            client.api.updatePersonality(user.id, axes, csrf)
                        }
                    }
                },
                colors = SliderDefaults.colors(
                    thumbColor = HearthColors.Pal,
                    activeTrackColor = HearthColors.Pal,
                    inactiveTrackColor = HearthColors.Line,
                ),
            )
        }
    }
}
