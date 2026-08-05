package com.hearth.companion.features.library

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
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import com.hearth.companion.HearthApp
import com.hearth.companion.core.PlayRequest
import com.hearth.companion.models.Extender
import com.hearth.companion.models.MediaItem
import com.hearth.companion.uistyle.HearthColors
import kotlinx.coroutines.launch

@Composable
fun PlayTargetPicker(app: HearthApp, item: MediaItem) {
    var embers by remember { mutableStateOf<List<Extender>>(emptyList()) }
    var status by remember { mutableStateOf<String?>(null) }
    val scope = rememberCoroutineScope()

    LaunchedEffect(Unit) {
        runCatching { app.buildClient()!!.api.extenders().extenders }
            .onSuccess { embers = it }
    }

    Column {
        Text("Play on…", color = HearthColors.Pal,
            style = MaterialTheme.typography.labelLarge,
            modifier = Modifier.padding(bottom = 8.dp))
        embers.filter { it.online }.forEach { e ->
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 4.dp)
                    .clip(RoundedCornerShape(10.dp))
                    .background(HearthColors.VoidLift)
                    .clickable {
                        scope.launch {
                            runCatching {
                                val client = app.buildClient()!!
                                val csrf = app.store.csrf() ?: error("No session")
                                client.api.play(PlayRequest(item.id, e.id), csrf)
                                status = "Playing on ${e.room}"
                            }.onFailure { status = it.message }
                        }
                    }
                    .padding(14.dp),
            ) {
                Column(Modifier.weight(1f)) {
                    Text(e.room, color = HearthColors.Bone)
                    Text(e.model, color = HearthColors.BoneDim,
                        style = MaterialTheme.typography.labelLarge)
                }
                Text("PLAY", color = HearthColors.Pal,
                    style = MaterialTheme.typography.labelSmall)
            }
        }
        status?.let {
            Text(it, color = HearthColors.Halo,
                modifier = Modifier.padding(top = 12.dp),
                style = MaterialTheme.typography.labelLarge)
        }
    }
}
