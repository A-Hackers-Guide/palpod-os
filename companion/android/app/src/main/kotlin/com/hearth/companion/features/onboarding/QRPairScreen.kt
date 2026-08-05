package com.hearth.companion.features.onboarding

import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.camera.view.PreviewView
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
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
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.content.ContextCompat
import com.hearth.companion.HearthApp
import com.hearth.companion.core.HearthClient
import com.hearth.companion.core.PairPayload
import com.hearth.companion.core.PairRequest
import com.hearth.companion.core.QRScanner
import com.hearth.companion.uistyle.HearthColors
import kotlinx.coroutines.launch

@Composable
fun QRPairScreen(app: HearthApp, host: String, port: Int, onPaired: () -> Unit) {
    val ctx = LocalContext.current
    val lifecycle = LocalLifecycleOwner.current
    var granted by remember {
        mutableStateOf(
            ContextCompat.checkSelfPermission(ctx, Manifest.permission.CAMERA)
                == PackageManager.PERMISSION_GRANTED
        )
    }
    val perm = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted = it }

    LaunchedEffect(Unit) { if (!granted) perm.launch(Manifest.permission.CAMERA) }

    val scope = rememberCoroutineScope()
    var status by remember { mutableStateOf("Point the camera at the QR code shown in the Hearth setup screen.") }

    Column(
        Modifier.fillMaxSize().background(HearthColors.Void).padding(24.dp)
    ) {
        Text("Pair with Hearth", color = HearthColors.Bone, style = MaterialTheme.typography.displayMedium)
        Text("Discovered at $host:$port", color = HearthColors.BoneDim, modifier = Modifier.padding(top = 4.dp))
        Text(status, color = HearthColors.BoneDim, modifier = Modifier.padding(vertical = 16.dp))

        if (granted) {
            Surface(
                color = HearthColors.Ink,
                shape = RoundedCornerShape(16.dp),
                modifier = Modifier.fillMaxWidth().size(320.dp),
            ) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    val scanner = remember { QRScanner(ctx) }
                    AndroidView(
                        factory = { c ->
                            PreviewView(c).also { pv ->
                                scanner.bind(lifecycle, pv) { payload ->
                                    status = "QR received — completing pair…"
                                    scope.launch { runCatching {
                                        completePair(app, host, port, payload) {
                                            status = it
                                        }
                                        onPaired()
                                    }.onFailure { status = "Pair failed: ${it.message}" } }
                                }
                            }
                        },
                        modifier = Modifier.fillMaxSize(),
                    )
                }
            }
        } else {
            Button(
                onClick = { perm.launch(Manifest.permission.CAMERA) },
                colors = ButtonDefaults.buttonColors(containerColor = HearthColors.Pal, contentColor = HearthColors.Void),
            ) { Text("Grant camera access") }
        }
    }
}

private suspend fun completePair(
    app: HearthApp,
    host: String,
    port: Int,
    payload: PairPayload,
    log: (String) -> Unit,
) {
    val base = "https://$host:$port"
    val client = HearthClient(baseUrl = base)
    log("Pairing with $host…")
    val resp = client.api.pair(
        PairRequest(
            token = payload.token,
            device_name = android.os.Build.MODEL,
            platform = "android",
        )
    )
    // Verify the fingerprint we saw in the QR matches the pin the Hearth
    // returned. The Hearth signs its response with the same key.
    require(resp.spki_pin == payload.fingerprint) {
        "Fingerprint mismatch — refusing to trust this Hearth"
    }
    app.store.saveHearth(base, resp.jwt, resp.spki_pin, resp.device_id)
    log("Paired.")
}
