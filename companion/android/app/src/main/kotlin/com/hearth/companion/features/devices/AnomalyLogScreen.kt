package com.hearth.companion.features.devices

import androidx.compose.foundation.background
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
import com.hearth.companion.core.AnomalyLog
import com.hearth.companion.uistyle.HearthColors

@Composable
fun AnomalyLogScreen(app: HearthApp, sessionId: String) {
    var rows by remember { mutableStateOf<List<AnomalyLog>>(emptyList()) }
    LaunchedEffect(sessionId) {
        runCatching { app.buildClient()!!.api.anomalies(sessionId) }
            .onSuccess { rows = it }
    }
    Column(Modifier.fillMaxSize().background(HearthColors.Void).padding(20.dp)) {
        Text("Audit trail", color = HearthColors.Bone, style = MaterialTheme.typography.displayMedium)
        Text(
            "Every input event on this session. Anomalies flagged in amber.",
            color = HearthColors.BoneDim,
            modifier = Modifier.padding(bottom = 12.dp),
        )
        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(6.dp),
            contentPadding = PaddingValues(vertical = 4.dp),
        ) {
            items(rows, key = { it.ts + it.kind }) { entry ->
                Surface(
                    color = HearthColors.VoidLift,
                    shape = RoundedCornerShape(10.dp),
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Column(Modifier.padding(12.dp)) {
                        Text(entry.kind.uppercase(), color = HearthColors.Halo,
                            style = MaterialTheme.typography.labelSmall)
                        Text(entry.detail, color = HearthColors.Bone,
                            style = MaterialTheme.typography.bodyMedium)
                        Text(entry.ts, color = HearthColors.BoneDim,
                            style = MaterialTheme.typography.labelSmall)
                    }
                }
            }
        }
    }
}
