package com.hearth.companion.features.devices

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.unit.dp
import com.hearth.companion.HearthApp
import com.hearth.companion.core.SessionRequest
import com.hearth.companion.core.WsEvent
import com.hearth.companion.models.RemoteDevice
import com.hearth.companion.uistyle.HearthColors
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.collectLatest
import okhttp3.WebSocket
import android.graphics.BitmapFactory

/**
 * Renders the WebSocket frame stream inside a Compose Canvas. Input
 * events (taps, drags, key) are emitted back over the same WebSocket
 * but only the server decides whether to APPLY them — it consults the
 * grant window server-side. So even if the app misbehaves and sends
 * inputs during view-only, they're dropped by the pal-web guard.
 */
@Composable
fun SessionScreen(app: HearthApp, device: RemoteDevice, onClose: () -> Unit) {
    var frame by remember { mutableStateOf<ImageBitmap?>(null) }
    var status by remember { mutableStateOf("connecting…") }
    var ws by remember { mutableStateOf<WebSocket?>(null) }

    // Live-recomputed grant status. `RemoteDevice.isControlActive` is
    // time-based (parses granted_until_ts); this state re-fires every 500 ms
    // so we can slam the WS shut the tick after expiry.
    val controlActive by produceState(initialValue = device.isControlActive, device) {
        while (true) {
            value = device.isControlActive
            delay(500)
        }
    }
    val remaining by produceState(initialValue = device.remainingSeconds, device) {
        while (true) {
            value = device.remainingSeconds
            delay(500)
        }
    }

    // If grant expires mid-session, tear the socket down client-side.
    LaunchedEffect(controlActive) {
        if (!controlActive) {
            ws?.close(1000, "grant-expired")
            ws = null
        }
    }

    LaunchedEffect(device.id) {
        runCatching {
            val client = app.buildClient() ?: error("Not paired")
            val csrf = app.store.csrf() ?: error("No session")
            val session = client.api.openSession(SessionRequest(device.id), csrf)
            val wsClient = app.buildWebSocketClient()!!
            val (handle, events) = wsClient.connect(session.ws_url, app.store.jwt()!!)
            ws = handle
            status = "streaming"
            events.collectLatest { ev ->
                when (ev) {
                    is WsEvent.Binary -> {
                        val bmp = BitmapFactory.decodeByteArray(ev.payload, 0, ev.payload.size)
                        if (bmp != null) frame = bmp.asImageBitmap()
                    }
                    is WsEvent.Text -> status = ev.payload
                    is WsEvent.Closed -> status = "closed: ${ev.reason}"
                    is WsEvent.Failure -> status = "failed: ${ev.cause.message}"
                    is WsEvent.Closing -> status = "closing"
                }
            }
        }.onFailure { status = it.message ?: "error" }
    }

    Column(Modifier.fillMaxSize().background(HearthColors.Void)) {
        Row(Modifier.fillMaxWidth().padding(16.dp)) {
            Text(device.label, color = HearthColors.Bone, modifier = Modifier.weight(1f))
            if (controlActive) {
                val mm = remaining / 60
                val ss = remaining % 60
                Text(
                    "CONTROL %d:%02d".format(mm, ss),
                    color = HearthColors.Ember,
                    style = MaterialTheme.typography.labelSmall,
                )
            } else {
                Text("VIEW-ONLY", color = HearthColors.Bone.copy(alpha = 0.5f), style = MaterialTheme.typography.labelSmall)
            }
            Text(status, color = HearthColors.Pal, style = MaterialTheme.typography.labelSmall)
            TextButton(onClick = onClose) { Text("Close", color = HearthColors.Bone) }
        }
        Box(Modifier.fillMaxSize()) {
            Canvas(
                modifier = Modifier.fillMaxSize()
                    .pointerInput(device.id, controlActive) {
                        detectTapGestures { offset ->
                            // The load-bearing client-side gate: no input event
                            // ever leaves this closure while the grant window is
                            // closed. Server enforces the same rule, but this
                            // saves a round-trip AND handles the case where the
                            // network to pal-web is down.
                            if (!controlActive) return@detectTapGestures
                            ws?.send("""{"kind":"tap","x":${offset.x},"y":${offset.y}}""")
                        }
                    }
                    .pointerInput(device.id, controlActive) {
                        detectDragGestures { _, drag ->
                            if (!controlActive) return@detectDragGestures
                            ws?.send("""{"kind":"drag","dx":${drag.x},"dy":${drag.y}}""")
                        }
                    }
            ) {
                val bmp = frame ?: return@Canvas
                drawImage(bmp)
            }
        }
    }
}
