package com.hearth.companion.features.devices

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.hearth.companion.HearthApp
import com.hearth.companion.models.RemoteDevice
import com.hearth.companion.uistyle.HearthColors

@Composable
fun DevicesListScreen(app: HearthApp) {
    var devices by remember { mutableStateOf<List<RemoteDevice>>(emptyList()) }
    var error by remember { mutableStateOf<String?>(null) }
    var sheetFor by remember { mutableStateOf<RemoteDevice?>(null) }
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)

    LaunchedEffect(Unit) {
        runCatching { app.buildClient()!!.api.devices().devices }
            .onSuccess { devices = it }
            .onFailure { error = it.message }
    }

    Column(
        Modifier.fillMaxSize().background(HearthColors.Void).padding(horizontal = 20.dp, vertical = 24.dp)
    ) {
        Text(
            "Devices",
            color = HearthColors.Bone,
            style = MaterialTheme.typography.displayMedium,
        )
        Text(
            "Households paired with this Hearth for remote-desktop viewing and control.",
            color = HearthColors.BoneDim,
            style = MaterialTheme.typography.bodyMedium,
            modifier = Modifier.padding(top = 4.dp, bottom = 16.dp),
        )
        error?.let {
            Text(it, color = HearthColors.Ember, modifier = Modifier.padding(bottom = 12.dp))
        }
        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(10.dp),
            contentPadding = PaddingValues(vertical = 4.dp),
        ) {
            items(devices, key = { it.id }) { d ->
                DeviceRow(d, onGrantTap = { sheetFor = d })
            }
        }
    }

    val target = sheetFor
    if (target != null) {
        ModalBottomSheet(
            onDismissRequest = { sheetFor = null },
            sheetState = sheetState,
            containerColor = HearthColors.VoidLift,
        ) {
            GrantControlSheet(
                app = app,
                device = target,
                onGranted = { sheetFor = null },
                onDismiss = { sheetFor = null },
            )
        }
    }
}
