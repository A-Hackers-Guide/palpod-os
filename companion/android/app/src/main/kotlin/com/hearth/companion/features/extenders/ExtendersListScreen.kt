package com.hearth.companion.features.extenders

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
import com.hearth.companion.models.Extender
import com.hearth.companion.uistyle.HearthColors

@Composable
fun ExtendersListScreen(app: HearthApp) {
    var embers by remember { mutableStateOf<List<Extender>>(emptyList()) }
    var selected by remember { mutableStateOf<Extender?>(null) }

    LaunchedEffect(Unit) {
        runCatching { app.buildClient()!!.api.extenders().extenders }
            .onSuccess { embers = it }
    }

    if (selected != null) {
        ExtenderDetailScreen(selected!!, onBack = { selected = null })
        return
    }

    Column(Modifier.fillMaxSize().background(HearthColors.Void).padding(20.dp)) {
        Text("Embers", color = HearthColors.Bone,
            style = MaterialTheme.typography.displayMedium)
        Text("Paired Hearth Ember extenders.",
            color = HearthColors.BoneDim,
            modifier = Modifier.padding(top = 4.dp, bottom = 16.dp))

        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(10.dp),
            contentPadding = PaddingValues(vertical = 4.dp),
        ) {
            items(embers, key = { it.id }) { e ->
                Surface(
                    color = HearthColors.VoidLift,
                    shape = RoundedCornerShape(14.dp),
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { selected = e },
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.padding(16.dp),
                    ) {
                        Surface(
                            color = if (e.online) HearthColors.Pal else HearthColors.BoneDim,
                            shape = CircleShape,
                            modifier = Modifier.size(10.dp).clip(CircleShape),
                        ) {}
                        Column(Modifier.padding(start = 12.dp).weight(1f)) {
                            Text(e.room, color = HearthColors.Bone)
                            Text("${e.model} · ${e.firmware}",
                                color = HearthColors.BoneDim,
                                style = MaterialTheme.typography.labelLarge)
                        }
                        Text(
                            if (e.online) "ONLINE" else "OFFLINE",
                            color = if (e.online) HearthColors.Pal else HearthColors.BoneDim,
                            style = MaterialTheme.typography.labelSmall,
                        )
                    }
                }
            }
        }
    }
}
