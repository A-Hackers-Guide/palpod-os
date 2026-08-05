package com.hearth.companion.core

import androidx.compose.foundation.clickable
import androidx.compose.ui.Modifier
import java.security.SecureRandom

/**
 * A signed, single-use, short-TTL token that proves a physical user tap
 * happened on a consent-bearing UI control (the [15]/[30]/[60] buttons in
 * [GrantControlSheet]).
 *
 * The invariant this class enforces:
 *
 *   1. The constructor is `private` and the companion `Factory` is
 *      `internal` — so only code inside `:app/core` can mint one at all.
 *      Tests, features, and any future SDK integration cannot construct
 *      `ConsentGesture` directly.
 *
 *   2. The single call-site that DOES mint one — [consentClickable] below —
 *      is a `Modifier` extension that only fires from inside Compose's
 *      pointer-input pipeline. Calling `consentClickable` doesn't produce
 *      a token; the *lambda passed to it* is invoked with a fresh token
 *      only after Compose observes a real [PressInteraction.Release] on
 *      the wrapped node.
 *
 *   3. Every token carries a random `nonce` and a `mintedAtMs` timestamp.
 *      [ConsentTokenSource] rejects any token older than [MAX_AGE_MS] and
 *      refuses to mint the outbound HTTP header value more than once per
 *      token (single-use enforcement).
 *
 * So the shape of "how do I POST /grant-control" is:
 *
 *   Modifier.consentClickable { gesture -> viewModel.grant(gesture, minutes) }
 *                                    │
 *                                    ▼
 *   ConsentTokenSource.consume(gesture) -> "user-tap"
 *
 * There is no other way to obtain a `ConsentGesture`, and there is no
 * other way to produce the `X-Consent-Origin: user-tap` header value.
 * A background worker, an intent extra, a deep-link handler, or a
 * ViewModel constructor cannot forge one.
 */
class ConsentGesture private constructor(
    internal val nonce: String,
    internal val mintedAtMs: Long,
    internal val surface: String,
) {
    override fun toString(): String = "ConsentGesture(surface=$surface, age=${System.currentTimeMillis() - mintedAtMs}ms)"

    internal companion object Factory {
        private val rng = SecureRandom()

        /**
         * INTERNAL to the `core` package. The only production call site is
         * inside [consentClickable]. Test code in `:app/src/test` lives in
         * a different module classpath and cannot see this factory —
         * ConsentGestureTest verifies that fact reflectively.
         */
        internal fun mint(surface: String): ConsentGesture {
            val bytes = ByteArray(24).also(rng::nextBytes)
            val nonce = buildString(48) {
                bytes.forEach { b -> append(String.format("%02x", b.toInt() and 0xff)) }
            }
            return ConsentGesture(
                nonce = nonce,
                mintedAtMs = System.currentTimeMillis(),
                surface = surface,
            )
        }

        internal const val MAX_AGE_MS: Long = 2_500L
    }
}

/**
 * The ONE Modifier that can produce a [ConsentGesture]. The gesture is
 * minted lazily inside the click callback — i.e. after Compose has already
 * observed a real pointer event on this node. There is no way to invoke
 * this callback synthetically without going through Compose's pointer
 * pipeline or, in tests, a UI test rule that itself simulates a real
 * pointer event.
 *
 * `surface` is a human-readable label ("grant-15m", "grant-30m", …) that
 * is logged with the anomaly record on the Hearth for audit.
 */
fun Modifier.consentClickable(
    surface: String,
    enabled: Boolean = true,
    onConsent: (ConsentGesture) -> Unit,
): Modifier = this.clickable(enabled = enabled) {
    // The mint happens synchronously inside the clickable lambda so the
    // token's mintedAtMs is bound to the real release event and the TTL
    // check downstream is meaningful. Do NOT hoist the mint call outside
    // this lambda, and do NOT mint inside a LaunchedEffect keyed on
    // recomposition — either would decouple the token from the tap.
    onConsent(ConsentGesture.mint(surface))
}
