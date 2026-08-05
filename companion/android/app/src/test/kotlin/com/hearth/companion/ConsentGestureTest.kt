package com.hearth.companion

import com.hearth.companion.core.ConsentGesture
import com.hearth.companion.core.ConsentTokenSource
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test
import java.lang.reflect.Modifier as JModifier

/**
 * Verifies the shape of the consent primitives.
 *
 * These aren't "does the network work" tests; they're structural
 * invariants of the ConsentGesture / ConsentTokenSource design that a
 * well-meaning future refactor could accidentally break.
 */
class ConsentGestureTest {

    @Before fun reset() { ConsentTokenSource.resetForTest() }

    @Test fun `ConsentGesture primary constructor is private`() {
        val ctors = ConsentGesture::class.java.declaredConstructors
        assertTrue(
            "ConsentGesture should have exactly one constructor",
            ctors.size == 1
        )
        val c = ctors[0]
        assertTrue(
            "ConsentGesture constructor must be private, was: ${JModifier.toString(c.modifiers)}",
            JModifier.isPrivate(c.modifiers)
        )
    }

    @Test fun `ConsentGesture has no public mint method — only Factory-internal`() {
        val factoryClass = ConsentGesture::class.java.classes
            .single { it.simpleName == "Factory" }
        val mint = factoryClass.declaredMethods.single { it.name == "mint" }
        assertTrue(
            "Factory.mint must not be public, was: ${JModifier.toString(mint.modifiers)}",
            !JModifier.isPublic(mint.modifiers)
        )
    }

    @Test fun `ConsentTokenSource rejects stale tokens`() {
        // Reflectively mint a token then pretend a lot of time has passed.
        val gesture = mintReflectively("grant-15m")
        val result = ConsentTokenSource.consume(
            gesture,
            now = System.currentTimeMillis() + 60_000L,
        )
        assertEquals(ConsentTokenSource.Result.Stale, result)
    }

    @Test fun `ConsentTokenSource rejects replay`() {
        val gesture = mintReflectively("grant-30m")
        val first = ConsentTokenSource.consume(gesture)
        assertTrue(first is ConsentTokenSource.Result.Ok)
        val second = ConsentTokenSource.consume(gesture)
        assertEquals(ConsentTokenSource.Result.Replay, second)
    }

    @Test fun `two mints produce different nonces`() {
        val a = mintReflectively("grant-15m")
        val b = mintReflectively("grant-15m")
        assertNotEquals(a.nonce, b.nonce)
    }

    @Test fun `ConsentTokenSource header value is exactly user-tap`() {
        val gesture = mintReflectively("grant-60m")
        val ok = ConsentTokenSource.consume(gesture) as ConsentTokenSource.Result.Ok
        assertEquals("user-tap", ok.headerValue)
        assertNotNull(ok.nonce)
    }

    /**
     * Test-only helper. Uses the same `internal` factory that
     * `Modifier.consentClickable` uses in production; the point of the
     * structural tests above is to prove nothing OUTSIDE the `core`
     * package can reach it. From this test module we can only reach it
     * via reflection — which is exactly what an adversarial refactor
     * would have to do, and the tests up top catch that shape change.
     */
    private fun mintReflectively(surface: String): ConsentGesture {
        val factoryClass = ConsentGesture::class.java.classes
            .single { it.simpleName == "Factory" }
        val factoryInstance = ConsentGesture::class.java
            .getDeclaredField("Factory").get(null)
        val mint = factoryClass.declaredMethods.single { it.name == "mint" }
        mint.isAccessible = true
        return mint.invoke(factoryInstance, surface) as ConsentGesture
    }
}
