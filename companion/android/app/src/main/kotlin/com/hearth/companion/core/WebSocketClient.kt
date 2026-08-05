package com.hearth.companion.core

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.asSharedFlow
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import okio.ByteString

sealed class WsEvent {
    data class Text(val payload: String) : WsEvent()
    data class Binary(val payload: ByteArray) : WsEvent() {
        override fun equals(other: Any?): Boolean =
            other is Binary && payload.contentEquals(other.payload)
        override fun hashCode(): Int = payload.contentHashCode()
    }
    data class Closing(val code: Int, val reason: String) : WsEvent()
    data class Closed(val code: Int, val reason: String) : WsEvent()
    data class Failure(val cause: Throwable) : WsEvent()
}

/**
 * OkHttp WebSocket wrapper. Opens the socket eagerly and returns the
 * handle synchronously along with a hot [Flow] of [WsEvent]. The remote-
 * desktop tab uses this for frame delivery and input-event upload; the
 * WS payload distinction between "just watching" and "in control" is
 * enforced server-side based on the current grant window.
 */
class WebSocketClient(private val ok: OkHttpClient) {

    fun connect(url: String, jwt: String): Pair<WebSocket, Flow<WsEvent>> {
        val req = Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer $jwt")
            .build()

        val events = MutableSharedFlow<WsEvent>(replay = 0, extraBufferCapacity = 64)

        val listener = object : WebSocketListener() {
            override fun onMessage(webSocket: WebSocket, text: String) {
                events.tryEmit(WsEvent.Text(text))
            }
            override fun onMessage(webSocket: WebSocket, bytes: ByteString) {
                events.tryEmit(WsEvent.Binary(bytes.toByteArray()))
            }
            override fun onClosing(webSocket: WebSocket, code: Int, reason: String) {
                events.tryEmit(WsEvent.Closing(code, reason))
            }
            override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                events.tryEmit(WsEvent.Closed(code, reason))
            }
            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                events.tryEmit(WsEvent.Failure(t))
            }
        }

        val ws = ok.newWebSocket(req, listener)
        return Pair(ws, events.asSharedFlow())
    }
}
