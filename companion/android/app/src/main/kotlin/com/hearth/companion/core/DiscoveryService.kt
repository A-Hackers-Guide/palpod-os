package com.hearth.companion.core

import android.content.Context
import android.net.nsd.NsdManager
import android.net.nsd.NsdServiceInfo
import android.os.Build
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow

data class DiscoveredHearth(
    val name: String,
    val host: String,
    val port: Int,
    val serviceType: String,
)

/**
 * mDNS/DNS-SD discovery for _hearth._tcp.local.
 *
 * Emits a [Flow] of [DiscoveredHearth] as services come and go on the LAN.
 * The flow is cold — starting collection registers the browse; cancelling
 * collection unregisters.
 */
class DiscoveryService(context: Context) {

    private val nsd = context.getSystemService(Context.NSD_SERVICE) as NsdManager
    private val serviceType = "_hearth._tcp."

    fun browse(): Flow<DiscoveredHearth> = callbackFlow {
        val listener = object : NsdManager.DiscoveryListener {
            override fun onStartDiscoveryFailed(serviceType: String, errorCode: Int) {
                close(IllegalStateException("mDNS discovery failed: $errorCode"))
            }
            override fun onStopDiscoveryFailed(serviceType: String, errorCode: Int) { }
            override fun onDiscoveryStarted(serviceType: String) { }
            override fun onDiscoveryStopped(serviceType: String) { }
            override fun onServiceLost(serviceInfo: NsdServiceInfo) { }
            override fun onServiceFound(serviceInfo: NsdServiceInfo) {
                resolve(serviceInfo) { host, port ->
                    trySend(
                        DiscoveredHearth(
                            name = serviceInfo.serviceName,
                            host = host,
                            port = port,
                            serviceType = serviceInfo.serviceType,
                        )
                    )
                }
            }
        }
        nsd.discoverServices(serviceType, NsdManager.PROTOCOL_DNS_SD, listener)
        awaitClose {
            runCatching { nsd.stopServiceDiscovery(listener) }
        }
    }

    private fun resolve(info: NsdServiceInfo, onResolved: (String, Int) -> Unit) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
            nsd.registerServiceInfoCallback(
                info,
                { it.run() },
                object : NsdManager.ServiceInfoCallback {
                    override fun onServiceInfoCallbackRegistrationFailed(errorCode: Int) { }
                    override fun onServiceUpdated(serviceInfo: NsdServiceInfo) {
                        val host = serviceInfo.hostAddresses.firstOrNull()?.hostAddress ?: return
                        onResolved(host, serviceInfo.port)
                    }
                    override fun onServiceLost() { }
                    override fun onServiceInfoCallbackUnregistered() { }
                }
            )
        } else {
            @Suppress("DEPRECATION")
            nsd.resolveService(info, object : NsdManager.ResolveListener {
                override fun onResolveFailed(serviceInfo: NsdServiceInfo, errorCode: Int) { }
                @Suppress("DEPRECATION")
                override fun onServiceResolved(serviceInfo: NsdServiceInfo) {
                    val host = serviceInfo.host?.hostAddress ?: return
                    onResolved(host, serviceInfo.port)
                }
            })
        }
    }
}
