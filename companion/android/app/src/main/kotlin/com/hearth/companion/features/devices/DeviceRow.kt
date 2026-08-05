package com.hearth.companion.features.devices

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Circle
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.hearth.companion.models.RemoteDevice
import com.hearth.companion.uistyle.HearthColors

@Composable
fun DeviceRow(device: RemoteDevice, onGrantTap: () -> Unit) {
    Surface(
        color = HearthColors.VoidLift,
        shape = RoundedCornerShape(14.dp),
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onGrantTap() },
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 14.dp),
        ) {
            Icon(
                Icons.Outlined.Circle,
                contentDescription = null,
                tint = statusColor(device),
                modifier = Modifier.size(10.dp).clip(CircleShape),
            )
            Spacer(Modifier.size(12.dp))
            Column(Modifier.weight(1f)) {
                Text(device.label, color = HearthColors.Bone, fontWeight = FontWeight.Medium)
                Text(
                    statusLine(device),
                    color = HearthColors.BoneDim,
                    style = MaterialTheme.typography.labelLarge,
                    modifier = Modifier.padding(top = 2.dp),
                )
            }
            Text(
                if (device.isControlActive) "CONTROL" else "VIEW",
                color = if (device.isControlActive) HearthColors.Ember else HearthColors.Pal,
                style = MaterialTheme.typography.labelSmall,
            )
        }
    }
}

private fun statusColor(d: RemoteDevice): Color = when {
    d.isControlActive -> HearthColors.Ember
    d.last_seen_ts != null -> HearthColors.Pal
    else -> HearthColors.BoneDim
}

private fun statusLine(d: RemoteDevice): String = when {
    d.isControlActive -> "Control granted until ${d.granted_until_ts}"
    d.last_seen_ts != null -> "${d.platform} · online"
    else -> "${d.platform} · offline"
}
