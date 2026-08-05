package com.hearth.companion.core

import android.annotation.SuppressLint
import android.content.Context
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.content.ContextCompat
import androidx.lifecycle.LifecycleOwner
import com.google.mlkit.vision.barcode.BarcodeScanning
import com.google.mlkit.vision.barcode.common.Barcode
import com.google.mlkit.vision.common.InputImage
import java.util.concurrent.Executors

/**
 * Parsed hearth://pair?token=<t>&fingerprint=<sha256> payload.
 */
data class PairPayload(val token: String, val fingerprint: String, val host: String?, val port: Int?) {
    companion object {
        fun parseOrNull(raw: String): PairPayload? {
            if (!raw.startsWith("hearth://pair")) return null
            val uri = android.net.Uri.parse(raw)
            val token = uri.getQueryParameter("token") ?: return null
            val fp = uri.getQueryParameter("fingerprint") ?: return null
            val host = uri.getQueryParameter("host")
            val port = uri.getQueryParameter("port")?.toIntOrNull()
            return PairPayload(token, fp, host, port)
        }
    }
}

/**
 * CameraX + ML Kit barcode scanner. Emits [PairPayload] when the QR
 * decoded is a hearth://pair URI and rejects everything else silently
 * so we don't act on adversarial QR codes.
 */
class QRScanner(private val context: Context) {

    private val executor = Executors.newSingleThreadExecutor()
    private val scanner = BarcodeScanning.getClient()

    fun bind(
        lifecycleOwner: LifecycleOwner,
        previewView: PreviewView,
        onPair: (PairPayload) -> Unit,
    ) {
        val providerFuture = ProcessCameraProvider.getInstance(context)
        providerFuture.addListener({
            val provider = providerFuture.get()
            val preview = Preview.Builder().build().also {
                it.setSurfaceProvider(previewView.surfaceProvider)
            }
            val analysis = ImageAnalysis.Builder()
                .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                .build()
            analysis.setAnalyzer(executor) { proxy ->
                @SuppressLint("UnsafeOptInUsageError")
                val media = proxy.image
                if (media == null) { proxy.close(); return@setAnalyzer }
                val image = InputImage.fromMediaImage(media, proxy.imageInfo.rotationDegrees)
                scanner.process(image)
                    .addOnSuccessListener { barcodes ->
                        for (b in barcodes) {
                            if (b.format == Barcode.FORMAT_QR_CODE) {
                                val raw = b.rawValue ?: continue
                                PairPayload.parseOrNull(raw)?.let(onPair)
                            }
                        }
                    }
                    .addOnCompleteListener { proxy.close() }
            }

            provider.unbindAll()
            provider.bindToLifecycle(
                lifecycleOwner,
                CameraSelector.DEFAULT_BACK_CAMERA,
                preview,
                analysis,
            )
        }, ContextCompat.getMainExecutor(context))
    }

    fun close() {
        executor.shutdown()
        scanner.close()
    }
}
