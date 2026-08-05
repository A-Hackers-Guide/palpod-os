package com.hearth.companion.features.household

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Face
import androidx.compose.material.icons.outlined.RecordVoiceOver
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import com.hearth.companion.HearthApp
import com.hearth.companion.models.User
import com.hearth.companion.uistyle.HearthColors

@Composable
fun UsersScreen(app: HearthApp) {
    var users by remember { mutableStateOf<List<User>>(emptyList()) }
    var selected by remember { mutableStateOf<User?>(null) }

    LaunchedEffect(Unit) {
        runCatching { app.buildClient()!!.api.users().users }
            .onSuccess { users = it }
    }

    if (selected != null) {
        UserDetailScreen(app, selected!!, onBack = { selected = null })
        return
    }

    Column(Modifier.fillMaxSize().background(HearthColors.Void).padding(20.dp)) {
        Text("Household", color = HearthColors.Bone,
            style = MaterialTheme.typography.displayMedium)
        Text("Face + voice recognition profiles and personalized personality.",
            color = HearthColors.BoneDim,
            modifier = Modifier.padding(top = 4.dp, bottom = 16.dp))

        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(10.dp),
            contentPadding = PaddingValues(vertical = 4.dp),
        ) {
            items(users, key = { it.id }) { u ->
                Surface(
                    color = HearthColors.VoidLift,
                    shape = RoundedCornerShape(14.dp),
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { selected = u },
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.padding(16.dp),
                    ) {
                        Surface(
                            color = HearthColors.Ink,
                            shape = CircleShape,
                            modifier = Modifier.size(40.dp),
                        ) {}
                        Column(Modifier.padding(start = 12.dp).weight(1f)) {
                            Text(u.display_name, color = HearthColors.Bone)
                            Row {
                                if (u.face_recognition_enabled) {
                                    Icon(Icons.Outlined.Face, contentDescription = "Face",
                                        tint = HearthColors.Pal, modifier = Modifier.size(14.dp))
                                }
                                if (u.voice_recognition_enabled) {
                                    Icon(Icons.Outlined.RecordVoiceOver, contentDescription = "Voice",
                                        tint = HearthColors.Pal, modifier = Modifier
                                            .padding(start = 6.dp).size(14.dp))
                                }
                            }
                        }
                        if (u.is_household_admin) {
                            Text("ADMIN", color = HearthColors.Halo,
                                style = MaterialTheme.typography.labelSmall)
                        }
                    }
                }
            }
        }
    }
}
