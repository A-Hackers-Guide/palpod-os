package com.hearth.companion.features.settings

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
import com.hearth.companion.uistyle.HearthColors

@Composable
fun AdvancedScreen(app: HearthApp, onBack: () -> Unit) {
    Column(Modifier.fillMaxSize().background(HearthColors.Void).padding(20.dp)) {
        Row(Modifier.fillMaxWidth()) {
            TextButton(onClick = onBack) { Text("Back", color = HearthColors.Pal) }
        }
        Text("Advanced", color = HearthColors.Bone,
            style = MaterialTheme.typography.displayMedium)

        Spacer(Modifier.height(16.dp))
        KeyValue("Hearth base", app.store.baseUrl() ?: "—")
        KeyValue("Device id", app.store.deviceId() ?: "—")
        KeyValue("SPKI pin", (app.store.spkiPin() ?: "—").take(24) + "…")
    }
}

@Composable
private fun KeyValue(k: String, v: String) {
    Column(Modifier.padding(vertical = 8.dp)) {
        Text(k, color = HearthColors.Pal, style = MaterialTheme.typography.labelSmall)
        Text(v, color = HearthColors.Bone, style = MaterialTheme.typography.labelLarge)
    }
}
