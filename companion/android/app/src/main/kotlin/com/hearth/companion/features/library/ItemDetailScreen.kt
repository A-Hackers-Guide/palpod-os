package com.hearth.companion.features.library

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.hearth.companion.HearthApp
import com.hearth.companion.models.MediaItem
import com.hearth.companion.uistyle.HearthColors

@Composable
fun ItemDetailScreen(app: HearthApp, item: MediaItem, onBack: () -> Unit) {
    Column(Modifier.fillMaxSize().background(HearthColors.Void).padding(20.dp)) {
        Row(Modifier.fillMaxWidth()) {
            TextButton(onClick = onBack) { Text("Back", color = HearthColors.Pal) }
        }
        Text(item.title, color = HearthColors.Bone,
            style = MaterialTheme.typography.displayMedium)
        item.subtitle?.let {
            Text(it, color = HearthColors.BoneDim,
                modifier = Modifier.padding(vertical = 6.dp))
        }
        Text(
            "${item.source.uppercase()} · ${item.kind}${item.year?.let { " · $it" } ?: ""}",
            color = HearthColors.Halo,
            style = MaterialTheme.typography.labelLarge,
            modifier = Modifier.padding(bottom = 20.dp),
        )
        Spacer(Modifier.height(8.dp))
        PlayTargetPicker(app, item)
    }
}
