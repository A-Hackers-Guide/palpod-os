package com.hearth.companion.features.settings

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.hearth.companion.HearthApp
import com.hearth.companion.uistyle.HearthColors

@Composable
fun SettingsScreen(app: HearthApp) {
    var page by remember { mutableStateOf<String?>(null) }
    when (page) {
        "about" -> AboutScreen(onBack = { page = null })
        "advanced" -> AdvancedScreen(app, onBack = { page = null })
        else -> Column(
            Modifier.fillMaxSize().background(HearthColors.Void).padding(20.dp)
        ) {
            Text("Settings", color = HearthColors.Bone,
                style = MaterialTheme.typography.displayMedium)
            Text(
                "Nothing leaves the house. No analytics, no crash reports, no cloud sync.",
                color = HearthColors.BoneDim,
                modifier = Modifier.padding(vertical = 12.dp),
            )
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                SettingsRow("About Hearth Companion") { page = "about" }
                SettingsRow("Advanced") { page = "advanced" }
                SettingsRow("Unpair this Hearth", tint = HearthColors.Ember) {
                    app.store.clear()
                }
            }
        }
    }
}

@Composable
private fun SettingsRow(
    label: String,
    tint: androidx.compose.ui.graphics.Color = HearthColors.Bone,
    onClick: () -> Unit,
) {
    Surface(
        color = HearthColors.VoidLift,
        shape = RoundedCornerShape(12.dp),
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() },
    ) {
        Text(label, color = tint,
            modifier = Modifier.padding(16.dp),
            style = MaterialTheme.typography.titleMedium)
    }
}
