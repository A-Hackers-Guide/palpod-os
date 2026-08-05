package com.hearth.companion.features.onboarding

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
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.hearth.companion.HearthApp
import com.hearth.companion.core.DiscoveredHearth
import com.hearth.companion.uistyle.HearthColors
import kotlinx.coroutines.flow.collectLatest

@Composable
fun DiscoveryScreen(app: HearthApp, onSelect: (host: String, port: Int) -> Unit) {
    val found by produceState(initialValue = emptyList<DiscoveredHearth>()) {
        val seen = mutableMapOf<String, DiscoveredHearth>()
        runCatching {
            app.discovery.browse().collectLatest { d ->
                seen[d.name] = d
                value = seen.values.toList()
            }
        }
    }
    Column(
        Modifier.fillMaxSize().background(HearthColors.Void).padding(24.dp)
    ) {
        Text(
            "Find your Hearth",
            color = HearthColors.Bone,
            style = androidx.compose.material3.MaterialTheme.typography.displayMedium,
        )
        Text(
            "We're listening on your local network for a Hearth advertising itself as _hearth._tcp.",
            color = HearthColors.BoneDim,
            modifier = Modifier.padding(top = 8.dp),
        )
        if (found.isEmpty()) {
            Column(
                Modifier.fillMaxSize(),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally,
            ) {
                CircularProgressIndicator(color = HearthColors.Pal)
                Text("Listening…", color = HearthColors.BoneDim, modifier = Modifier.padding(top = 16.dp))
            }
        } else {
            LazyColumn(
                Modifier.fillMaxSize().padding(top = 24.dp),
                contentPadding = PaddingValues(vertical = 8.dp),
            ) {
                items(found, key = { it.name }) { d ->
                    Surface(
                        color = HearthColors.VoidLift,
                        shape = RoundedCornerShape(14.dp),
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 6.dp)
                            .clickable { onSelect(d.host, d.port) },
                    ) {
                        Column(Modifier.padding(16.dp)) {
                            Text(d.name, color = HearthColors.Bone, fontWeight = FontWeight.Medium)
                            Text(
                                "${d.host}:${d.port}",
                                color = HearthColors.BoneDim,
                                style = androidx.compose.material3.MaterialTheme.typography.labelLarge,
                                modifier = Modifier.padding(top = 4.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}
