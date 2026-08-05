package com.hearth.companion.models

import kotlinx.serialization.Serializable
import java.time.Duration
import java.time.Instant

@Serializable
data class RemoteDevice(
    val id: String,
    val label: String,
    val platform: String,
    val paired_at: String,
    val view_only: Boolean = true,
    val granted_until_ts: String? = null,
    val last_seen_ts: String? = null,
) {
    /** Parsed grant expiry as an Instant, or null if never granted / unparseable. */
    val grantedUntil: Instant?
        get() = granted_until_ts?.let { runCatching { Instant.parse(it) }.getOrNull() }

    /** True iff grant window has not yet elapsed. The single source of truth for
     * client-side input gating. Time-based; recompute every call — do not cache. */
    val isControlActive: Boolean
        get() = grantedUntil?.isAfter(Instant.now()) == true

    /** Seconds until expiry, clamped to [0, ∞). */
    val remainingSeconds: Long
        get() = grantedUntil?.let {
            Duration.between(Instant.now(), it).seconds.coerceAtLeast(0L)
        } ?: 0L
}
