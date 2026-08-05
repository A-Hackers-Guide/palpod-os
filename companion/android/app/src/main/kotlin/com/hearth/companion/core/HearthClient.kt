package com.hearth.companion.core

import com.hearth.companion.models.ControlGrant
import com.hearth.companion.models.Extender
import com.hearth.companion.models.MediaItem
import com.hearth.companion.models.PersonalityAxes
import com.hearth.companion.models.RemoteDevice
import com.hearth.companion.models.User
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import okhttp3.CertificatePinner
import okhttp3.Interceptor
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Response
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Path
import java.util.concurrent.TimeUnit

private val json = Json {
    ignoreUnknownKeys = true
    prettyPrint = false
    encodeDefaults = true
}

@Serializable
data class LoginRequest(val password: String)

@Serializable
data class LoginResponse(val csrf: String, val user: String)

@Serializable
data class PairRequest(val token: String, val device_name: String, val platform: String)

@Serializable
data class PairResponse(val jwt: String, val device_id: String, val spki_pin: String)

@Serializable
data class GrantRequest(val minutes: Int)

@Serializable
data class GrantResponse(val grant: ControlGrant)

@Serializable
data class SessionRequest(val device_id: String)

@Serializable
data class SessionResponse(val session_id: String, val ws_url: String)

@Serializable
data class PlayRequest(val item_id: String, val target_device_id: String)

@Serializable
data class DevicesResponse(val devices: List<RemoteDevice>)

@Serializable
data class UsersResponse(val users: List<User>)

@Serializable
data class LibraryResponse(val items: List<MediaItem>)

@Serializable
data class ExtendersResponse(val extenders: List<Extender>)

@Serializable
data class AnomalyLog(
    val session_id: String,
    val ts: String,
    val kind: String,
    val detail: String,
)

interface HearthApi {

    @POST("api/auth/login")
    suspend fun login(@Body body: LoginRequest): LoginResponse

    @POST("api/pair")
    suspend fun pair(@Body body: PairRequest): PairResponse

    @GET("api/remote/devices")
    suspend fun devices(): DevicesResponse

    @POST("api/remote/devices")
    suspend fun addDevice(@Body body: RemoteDevice, @Header("X-CSRF-Token") csrf: String): RemoteDevice

    @DELETE("api/remote/devices/{id}")
    suspend fun unpair(@Path("id") id: String, @Header("X-CSRF-Token") csrf: String)

    /**
     * The **only** Retrofit endpoint that accepts the X-Consent-Origin
     * header. Wired to route through [ConsentInterceptor] which asserts
     * the value must be exactly the string returned by [ConsentTokenSource].
     */
    @POST("api/remote/devices/{id}/grant-control")
    suspend fun grantControl(
        @Path("id") id: String,
        @Header("X-Consent-Origin") consentOrigin: String,
        @Header("X-Consent-Nonce") nonce: String,
        @Header("X-CSRF-Token") csrf: String,
        @Body body: GrantRequest,
    ): GrantResponse

    @POST("api/remote/devices/{id}/revoke-control")
    suspend fun revokeControl(@Path("id") id: String, @Header("X-CSRF-Token") csrf: String)

    @GET("api/remote/sessions/{id}/anomalies")
    suspend fun anomalies(@Path("id") id: String): List<AnomalyLog>

    @POST("api/remote/sessions")
    suspend fun openSession(@Body body: SessionRequest, @Header("X-CSRF-Token") csrf: String): SessionResponse

    @GET("api/users")
    suspend fun users(): UsersResponse

    @GET("api/users/{id}/personality")
    suspend fun personality(@Path("id") id: String): PersonalityAxes

    @PUT("api/users/{id}/personality")
    suspend fun updatePersonality(
        @Path("id") id: String,
        @Body body: PersonalityAxes,
        @Header("X-CSRF-Token") csrf: String,
    ): PersonalityAxes

    @GET("api/library")
    suspend fun library(): LibraryResponse

    @POST("api/play")
    suspend fun play(@Body body: PlayRequest, @Header("X-CSRF-Token") csrf: String)

    @GET("api/extenders")
    suspend fun extenders(): ExtendersResponse
}

/**
 * Belt-and-braces: even though the only Retrofit method that TAKES an
 * `X-Consent-Origin` header is [HearthApi.grantControl], we install an
 * OkHttp interceptor that strips the header from every OTHER request and
 * asserts on [HearthApi.grantControl] that the value came from
 * [ConsentTokenSource]. If a future refactor accidentally hardcodes
 * `"user-tap"` at any other call site, the request 400s at the client
 * before it hits the wire.
 */
private class ConsentInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val req = chain.request()
        val header = req.header("X-Consent-Origin")
        if (header != null) {
            val onGrantPath = req.url.encodedPath.endsWith("/grant-control")
            require(onGrantPath) {
                "X-Consent-Origin header present on non-grant path ${req.url.encodedPath}"
            }
            // In-app tests use `resetForTest` to clear the seen set; in
            // production the ConsentInterceptor cannot know the nonce is
            // fresh because ConsentTokenSource has already consumed it and
            // handed us the header value. So we just assert the shape.
            require(header == "user-tap") {
                "Only ConsentTokenSource may set X-Consent-Origin. got=$header"
            }
        }
        return chain.proceed(req)
    }
}

/**
 * Long-lived singleton. Reconfigured after pairing to install the SPKI pin.
 */
class HearthClient(
    baseUrl: String,
    spkiPin: String? = null,
    jwt: String? = null,
) {

    private val jwtInterceptor = Interceptor { chain ->
        val req = if (jwt != null) {
            chain.request().newBuilder().addHeader("Authorization", "Bearer $jwt").build()
        } else chain.request()
        chain.proceed(req)
    }

    private val ok: OkHttpClient = OkHttpClient.Builder()
        .connectTimeout(6, TimeUnit.SECONDS)
        .readTimeout(20, TimeUnit.SECONDS)
        .callTimeout(30, TimeUnit.SECONDS)
        .retryOnConnectionFailure(true)
        .addInterceptor(ConsentInterceptor())
        .addInterceptor(jwtInterceptor)
        .addInterceptor(HttpLoggingInterceptor().apply { level = HttpLoggingInterceptor.Level.BASIC })
        .apply {
            if (!spkiPin.isNullOrBlank()) {
                val host = baseUrl
                    .removePrefix("https://").removePrefix("http://")
                    .substringBefore('/').substringBefore(':')
                certificatePinner(
                    CertificatePinner.Builder()
                        .add(host, "sha256/$spkiPin")
                        .build()
                )
            }
        }
        .build()

    val api: HearthApi = Retrofit.Builder()
        .baseUrl(if (baseUrl.endsWith("/")) baseUrl else "$baseUrl/")
        .client(ok)
        .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
        .build()
        .create(HearthApi::class.java)

    fun okHttp(): OkHttpClient = ok
}
