package com.hearth.companion.core

import java.util.Collections

/**
 * The single production point of the `X-Consent-Origin: user-tap` header value.
 *
 * Every path that calls `POST /api/remote/devices/{id}/grant-control` must
 * first go through [consume]. There is no other way inside this app to
 * produce the header string `"user-tap"` — everywhere else it appears is
 * either a comment, a doc string, or a compile-time constant in this file.
 *
 * The token you pass in must be a [ConsentGesture], which — see that class
 * for the full argument — can only be minted inside a Compose clickable
 * lambda on a consent-bearing UI control.
 *
 * We additionally guard against:
 *   * Replay: [seenNonces] is a bounded LRU that rejects duplicate nonces.
 *   * Stale taps: gestures older than [ConsentGesture.MAX_AGE_MS] are
 *     rejected, so a UI that mints one and then defers the request across
 *     a network reconnect must re-collect consent.
 */
object ConsentTokenSource {
    /** The literal header value POSTed to the Hearth. Do not export. */
    private const val HEADER_VALUE = "user-tap"

    /** Bounded LRU of used nonces. 4096 is >>10x the plausible peak of taps
     * in a MAX_AGE window and still trivially cheap to keep in memory. */
    private val seenNonces: MutableSet<String> = Collections.synchronizedSet(
        Collections.newSetFromMap(object : LinkedHashMap<String, Boolean>(4096, 0.75f, true) {
            override fun removeEldestEntry(eldest: Map.Entry<String, Boolean>?): Boolean = size > 4096
        })
    )

    sealed class Result {
        data class Ok(val headerValue: String, val nonce: String) : Result()
        data object Stale : Result()
        data object Replay : Result()
    }

    /**
     * Consume a fresh [ConsentGesture] and return the outbound header value.
     *
     * @param gesture the token minted inside a `consentClickable { … }` lambda
     * @param now clock hook for tests; production callers must omit
     */
    fun consume(gesture: ConsentGesture, now: Long = System.currentTimeMillis()): Result {
        val age = now - gesture.mintedAtMs
        if (age < 0 || age > ConsentGesture.MAX_AGE_MS) return Result.Stale
        if (!seenNonces.add(gesture.nonce)) return Result.Replay
        return Result.Ok(headerValue = HEADER_VALUE, nonce = gesture.nonce)
    }

    /**
     * Used only by unit tests to reset the replay cache. Marked `internal`
     * so it's inaccessible to feature modules and to the release build's
     * consumers.
     */
    internal fun resetForTest() = seenNonces.clear()
}
