package com.hearth.companion.features.extenders

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.hearth.companion.models.Extender
import com.hearth.companion.uistyle.HearthColors

@Composable
fun ExtenderDetailScreen(e: Extender, onBack: () -> Unit) {
    Column(Modifier.fillMaxSize().background(HearthColors.Void).padding(20.dp)) {
        Row(Modifier.fillMaxWidth()) {
            TextButton(onClick = onBack) { Text("Back", color = HearthColors.Pal) }
        }
        Text(e.room, color = HearthColors.Bone,
            style = MaterialTheme.typography.displayMedium)
        Text(e.model, color = HearthColors.BoneDim,
            modifier = Modifier.padding(top = 4.dp))
        Text(
            "Firmware ${e.firmware} · paired ${e.paired_at}",
            color = HearthColors.Halo,
            style = MaterialTheme.typography.labelLarge,
            modifier = Modifier.padding(top = 16.dp),
        )
        Text(
            if (e.online) "Online" else "Offline (last seen ${e.last_seen_ts ?: "unknown"})",
            color = if (e.online) HearthColors.Pal else HearthColors.BoneDim,
            style = MaterialTheme.typography.labelLarge,
            modifier = Modifier.padding(top = 6.dp),
        )
    }
}
