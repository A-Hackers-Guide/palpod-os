package com.hearth.companion.features.household

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
import com.hearth.companion.models.User
import com.hearth.companion.uistyle.HearthColors

@Composable
fun UserDetailScreen(app: HearthApp, user: User, onBack: () -> Unit) {
    Column(Modifier.fillMaxSize().background(HearthColors.Void).padding(20.dp)) {
        Row(Modifier.fillMaxWidth()) {
            TextButton(onClick = onBack) { Text("Back", color = HearthColors.Pal) }
        }
        Text(user.display_name, color = HearthColors.Bone,
            style = MaterialTheme.typography.displayMedium)
        Spacer(Modifier.height(16.dp))
        VoicePresetPicker(user)
        Spacer(Modifier.height(20.dp))
        PersonalitySlidersScreen(app, user)
    }
}
