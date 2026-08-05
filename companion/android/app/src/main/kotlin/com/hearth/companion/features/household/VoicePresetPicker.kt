package com.hearth.companion.features.household

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import com.hearth.companion.models.User
import com.hearth.companion.uistyle.HearthColors

private val presets = listOf(
    "hearth-neutral" to "Neutral",
    "hearth-warm" to "Warm",
    "hearth-vintage" to "Vintage BBC",
    "hearth-pal" to "PAL",
)

@Composable
fun VoicePresetPicker(user: User) {
    var chosen by remember { mutableStateOf(user.voice_preset) }
    Column {
        Text("Voice", color = HearthColors.Pal,
            style = MaterialTheme.typography.labelLarge,
            modifier = Modifier.padding(bottom = 8.dp))
        Row(
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            modifier = Modifier.fillMaxWidth(),
        ) {
            presets.forEach { (id, label) ->
                val selected = chosen == id
                Column(
                    modifier = Modifier
                        .weight(1f)
                        .clip(RoundedCornerShape(10.dp))
                        .background(if (selected) HearthColors.Pal else HearthColors.Ink)
                        .clickable { chosen = id }
                        .padding(vertical = 14.dp),
                    horizontalAlignment = androidx.compose.ui.Alignment.CenterHorizontally,
                ) {
                    Text(
                        label,
                        color = if (selected) HearthColors.Void else HearthColors.Bone,
                        style = MaterialTheme.typography.labelLarge,
                    )
                }
            }
        }
    }
}
