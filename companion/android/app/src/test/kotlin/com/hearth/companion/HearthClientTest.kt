package com.hearth.companion

import com.hearth.companion.core.GrantRequest
import com.hearth.companion.core.HearthClient
import com.hearth.companion.core.LoginRequest
import kotlinx.coroutines.runBlocking
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test

class HearthClientTest {

    private lateinit var server: MockWebServer
    private lateinit var client: HearthClient

    @Before fun setUp() {
        server = MockWebServer().also { it.start() }
        client = HearthClient(baseUrl = server.url("/").toString(), spkiPin = null, jwt = "test-jwt")
    }

    @After fun tearDown() { server.shutdown() }

    @Test fun `login round-trips csrf`() = runBlocking {
        server.enqueue(
            MockResponse().setBody("""{"csrf":"c-123","user":"mark"}""")
        )
        val resp = client.api.login(LoginRequest("hunter2"))
        assertEquals("c-123", resp.csrf)
        assertEquals("mark", resp.user)
    }

    @Test fun `grantControl sends the consent header`() = runBlocking {
        server.enqueue(
            MockResponse().setBody(
                """{"grant":{"device_id":"d","granted_at":"t0","expires_at":"t1","minutes":15,"rolling_24h_used_minutes":15}}"""
            )
        )
        client.api.grantControl(
            id = "d",
            consentOrigin = "user-tap",
            nonce = "deadbeef",
            csrf = "c-123",
            body = GrantRequest(15),
        )
        val req = server.takeRequest()
        assertEquals("user-tap", req.getHeader("X-Consent-Origin"))
        assertEquals("deadbeef", req.getHeader("X-Consent-Nonce"))
        assertEquals("c-123", req.getHeader("X-CSRF-Token"))
        assertEquals("Bearer test-jwt", req.getHeader("Authorization"))
    }

    @Test fun `interceptor refuses X-Consent-Origin on non-grant path`() = runBlocking {
        server.enqueue(MockResponse().setBody("""{"users":[]}"""))
        // If someone manually built a request with the header outside the
        // grant path, the interceptor throws. We simulate that by adding an
        // interceptor test — since we can't add headers to Retrofit calls
        // without modifying the interface, we build a raw request instead.
        val ok = client.okHttp()
        val req = okhttp3.Request.Builder()
            .url(server.url("/api/users"))
            .addHeader("X-Consent-Origin", "user-tap")
            .build()
        val threw = runCatching { ok.newCall(req).execute().use { } }.exceptionOrNull()
        assertTrue(
            "expected IllegalArgumentException from ConsentInterceptor, got $threw",
            threw is IllegalArgumentException
        )
    }
}
