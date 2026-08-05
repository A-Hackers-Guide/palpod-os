package com.hearth.companion.core

import android.content.Context
import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

/**
 * Android-Keystore-backed encrypted key/value store for the pairing JWT,
 * SPKI pin, base URL, and session CSRF token. AES-256-GCM at rest with the
 * master key held in the hardware-backed Keystore where available.
 *
 * Nothing here goes to disk in plaintext, nothing is backed up (see
 * `data_extraction_rules.xml`), and there is no accessor that returns raw
 * secrets to code outside :app/core.
 */
class KeystoreStore(context: Context) {

    private val prefs: SharedPreferences by lazy {
        val masterKey = MasterKey.Builder(context.applicationContext)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .setUserAuthenticationRequired(false)
            .build()
        EncryptedSharedPreferences.create(
            context.applicationContext,
            PREFS_NAME,
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM,
        )
    }

    fun saveHearth(baseUrl: String, jwt: String, spkiPin: String, deviceId: String) {
        prefs.edit()
            .putString(KEY_BASE_URL, baseUrl)
            .putString(KEY_JWT, jwt)
            .putString(KEY_SPKI, spkiPin)
            .putString(KEY_DEVICE_ID, deviceId)
            .apply()
    }

    fun clear() { prefs.edit().clear().apply() }

    fun baseUrl(): String? = prefs.getString(KEY_BASE_URL, null)
    fun jwt(): String? = prefs.getString(KEY_JWT, null)
    fun spkiPin(): String? = prefs.getString(KEY_SPKI, null)
    fun deviceId(): String? = prefs.getString(KEY_DEVICE_ID, null)

    fun saveCsrf(csrf: String) = prefs.edit().putString(KEY_CSRF, csrf).apply()
    fun csrf(): String? = prefs.getString(KEY_CSRF, null)

    fun isPaired(): Boolean = jwt() != null && spkiPin() != null && baseUrl() != null

    private companion object {
        const val PREFS_NAME = "hearth_secure_prefs"
        const val KEY_BASE_URL = "base_url"
        const val KEY_JWT = "jwt"
        const val KEY_SPKI = "spki"
        const val KEY_DEVICE_ID = "device_id"
        const val KEY_CSRF = "csrf"
    }
}
