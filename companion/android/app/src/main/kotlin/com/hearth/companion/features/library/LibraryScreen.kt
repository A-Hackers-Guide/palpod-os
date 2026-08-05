package com.hearth.companion.features.library

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.hearth.companion.HearthApp
import com.hearth.companion.models.MediaItem
import com.hearth.companion.uistyle.HearthColors

@Composable
fun LibraryScreen(app: HearthApp) {
    var items by remember { mutableStateOf<List<MediaItem>>(emptyList()) }
    var picked by remember { mutableStateOf<MediaItem?>(null) }

    LaunchedEffect(Unit) {
        runCatching { app.buildClient()!!.api.library().items }
            .onSuccess { items = it }
    }

    if (picked != null) {
        ItemDetailScreen(app, picked!!, onBack = { picked = null })
        return
    }

    Column(Modifier.fillMaxSize().background(HearthColors.Void).padding(20.dp)) {
        Text("Library", color = HearthColors.Bone,
            style = MaterialTheme.typography.displayMedium)
        Text("Plex, Jellyfin, Audiobookshelf, xTeVe, Steam — all in one place.",
            color = HearthColors.BoneDim,
            modifier = Modifier.padding(top = 4.dp, bottom = 16.dp))

        val grouped = items.groupBy { it.source }
        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(20.dp),
            contentPadding = PaddingValues(vertical = 4.dp),
        ) {
            grouped.forEach { (source, entries) ->
                item(key = "hdr-$source") {
                    Text(source.uppercase(), color = HearthColors.Pal,
                        style = MaterialTheme.typography.labelLarge)
                }
                items(entries, key = { it.id }) { entry ->
                    Surface(
                        color = HearthColors.VoidLift,
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { picked = entry },
                    ) {
                        Column(Modifier.padding(14.dp)) {
                            Text(entry.title, color = HearthColors.Bone)
                            entry.subtitle?.let {
                                Text(it, color = HearthColors.BoneDim,
                                    style = MaterialTheme.typography.labelLarge,
                                    modifier = Modifier.padding(top = 2.dp))
                            }
                        }
                    }
                }
            }
        }
    }
}
