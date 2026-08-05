package com.hearth.companion.features.settings

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
import com.hearth.companion.uistyle.HearthColors

@Composable
fun AboutScreen(onBack: () -> Unit) {
    Column(Modifier.fillMaxSize().background(HearthColors.Void).padding(20.dp)) {
        Row(Modifier.fillMaxWidth()) {
            TextButton(onClick = onBack) { Text("Back", color = HearthColors.Pal) }
        }
        Text("Hearth Companion", color = HearthColors.Bone,
            style = MaterialTheme.typography.displayMedium)
        Text("For Hearth Home, Inc.",
            color = HearthColors.BoneDim,
            modifier = Modifier.padding(vertical = 6.dp))
        Text(
            "This companion runs entirely on your LAN. There is no third-party SDK on this device. There is no analytics, no crash reporter, no push notification service, no cloud sync. Every request goes to your Hearth over TLS with a pinned certificate that you saw the fingerprint of at pair time.",
            color = HearthColors.BoneDim,
            modifier = Modifier.padding(top = 12.dp),
            style = MaterialTheme.typography.bodyMedium,
        )
    }
}
