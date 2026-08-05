package com.hearth.companion

import android.app.Application
import com.hearth.companion.core.DiscoveryService
import com.hearth.companion.core.HearthClient
import com.hearth.companion.core.KeystoreStore
import com.hearth.companion.core.WebSocketClient

/**
 * Application-scoped service locator. Everything is lazy and holds only
 * process-lifetime state; no persistent workers, no boot receivers, no
 * scheduled uploads.
 */
class HearthApp : Application() {

    val store: KeystoreStore by lazy { KeystoreStore(this) }

    val discovery: DiscoveryService by lazy { DiscoveryService(this) }

    /**
     * Rebuilt whenever pairing state changes so the SPKI pin and JWT are
     * pulled fresh from the encrypted store.
     */
    fun buildClient(): HearthClient? {
        val base = store.baseUrl() ?: return null
        return HearthClient(
            baseUrl = base,
            spkiPin = store.spkiPin(),
            jwt = store.jwt(),
        )
    }

    fun buildWebSocketClient(): WebSocketClient? =
        buildClient()?.let { WebSocketClient(it.okHttp()) }
}
