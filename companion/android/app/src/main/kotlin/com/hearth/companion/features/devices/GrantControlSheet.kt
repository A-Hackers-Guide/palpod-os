package com.hearth.companion.features.devices

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.hearth.companion.HearthApp
import com.hearth.companion.core.ConsentGesture
import com.hearth.companion.core.ConsentTokenSource
import com.hearth.companion.core.GrantRequest
import com.hearth.companion.core.consentClickable
import com.hearth.companion.models.RemoteDevice
import com.hearth.companion.uistyle.HearthColors
import kotlinx.coroutines.launch

/**
 * The consent surface.
 *
 * Three duration buttons; the tap is the load-bearing consent event. The
 * button's Modifier is [consentClickable], which is the *only* production
 * call site that mints a [ConsentGesture]. That gesture is then handed to
 * [ConsentTokenSource.consume], which is the only producer of the
 * `X-Consent-Origin: user-tap` header string. No other code path in the
 * app calls `grantControl`, and no code path in the app calls
 * `ConsentGesture.mint()` outside `consentClickable`.
 */
@Composable
fun GrantControlSheet(
    app: HearthApp,
    device: RemoteDevice,
    onGranted: () -> Unit,
    onDismiss: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    var status by remember { mutableStateOf<String?>(null) }

    Column(
        Modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp, vertical = 20.dp),
    ) {
        Text(
            "Grant control of ${device.label}?",
            color = HearthColors.Bone,
            style = MaterialTheme.typography.headlineLarge,
        )
        Text(
            "You'll be able to move the cursor, type, and interact — for the window you pick. Hearth logs everything and revokes control automatically when the window ends. 30-second cooldown between grants; 240-minute rolling 24-hour cap.",
            color = HearthColors.BoneDim,
            style = MaterialTheme.typography.bodyMedium,
            modifier = Modifier.padding(top = 8.dp, bottom = 20.dp),
        )
        Row(
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            modifier = Modifier.fillMaxWidth(),
        ) {
            DurationButton("15 min", surface = "grant-15m", modifier = Modifier.weight(1f)) { gesture ->
                submitGrant(app, device, 15, gesture, scope, onGranted) { status = it }
            }
            DurationButton("30 min", surface = "grant-30m", modifier = Modifier.weight(1f)) { gesture ->
                submitGrant(app, device, 30, gesture, scope, onGranted) { status = it }
            }
            DurationButton("60 min", surface = "grant-60m", modifier = Modifier.weight(1f)) { gesture ->
                submitGrant(app, device, 60, gesture, scope, onGranted) { status = it }
            }
        }
        Spacer(Modifier.height(12.dp))
        TextButton(onClick = onDismiss) {
            Text("Cancel", color = HearthColors.BoneDim)
        }
        status?.let {
            Text(
                it,
                color = HearthColors.Ember,
                modifier = Modifier.padding(top = 10.dp),
                style = MaterialTheme.typography.labelLarge,
            )
        }
    }
}

@Composable
private fun DurationButton(
    label: String,
    surface: String,
    modifier: Modifier = Modifier,
    onConsent: (ConsentGesture) -> Unit,
) {
    Box(
        modifier = modifier
            .height(56.dp)
            .clip(RoundedCornerShape(12.dp))
            .background(HearthColors.Pal)
            .consentClickable(surface = surface, onConsent = onConsent),
        contentAlignment = Alignment.Center,
    ) {
        Text(
            label,
            color = HearthColors.Void,
            style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.SemiBold),
        )
    }
}

private fun submitGrant(
    app: HearthApp,
    device: RemoteDevice,
    minutes: Int,
    gesture: ConsentGesture,
    scope: kotlinx.coroutines.CoroutineScope,
    onGranted: () -> Unit,
    onError: (String) -> Unit,
) {
    when (val consent = ConsentTokenSource.consume(gesture)) {
        is ConsentTokenSource.Result.Stale -> onError("Tap timed out; try again.")
        is ConsentTokenSource.Result.Replay -> onError("Duplicate tap detected.")
        is ConsentTokenSource.Result.Ok -> {
            scope.launch {
                runCatching {
                    val client = app.buildClient() ?: error("Not paired")
                    val csrf = app.store.csrf() ?: error("No session")
                    client.api.grantControl(
                        id = device.id,
                        consentOrigin = consent.headerValue,
                        nonce = consent.nonce,
                        csrf = csrf,
                        body = GrantRequest(minutes),
                    )
                    onGranted()
                }.onFailure { onError(it.message ?: "Grant failed") }
            }
        }
    }
}
