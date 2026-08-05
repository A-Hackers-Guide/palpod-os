# Hearth Companion — Android

Jetpack Compose companion app for the Hearth $95k luxury home AI + media
server. Discovers the Hearth over mDNS, pairs by QR, then talks to it over
TLS-pinned HTTPS on the LAN.

**Nothing leaves the house.** No Firebase, Analytics, Crashlytics, Sentry,
FCM, or any other third-party network SDK is on the classpath. The
`AndroidManifest.xml` requests only what's needed for LAN discovery + the
camera for QR pairing.

## Building

Requires:
- Android Studio Ladybug (2024.2.1) or newer, or CLI Gradle 8.9
- AGP 8.7.2 · Kotlin 2.0.21 · Compose BOM 2024.10.01
- `ANDROID_HOME` pointing at a stock Android SDK with API 34 platform +
  build-tools 34.0.0

```
./gradlew :app:assembleDebug
./gradlew :app:testDebugUnitTest       # ConsentGestureTest, HearthClientTest
./gradlew :app:connectedDebugAndroidTest  # OnboardingFlowTest (needs emulator)
```

The included `gradlew` shim delegates to a system-installed Gradle 8.9+;
run `gradle wrapper --gradle-version 8.9` once inside this directory to
generate the real wrapper JAR before shipping.

## Non-negotiable boundaries

1. **`ConsentTokenSource` is the ONLY producer of the `X-Consent-Origin:
   user-tap` header value.** Everywhere else in the codebase, the string
   `"user-tap"` appears only in doc comments and a single interceptor
   assertion. A `grep` for `user-tap` is a legitimate audit tool — if it
   shows up in a new file, that file is wrong.

2. **`ConsentTokenSource.consume(gesture: ConsentGesture)` requires a
   `ConsentGesture`, whose constructor is `private` and whose sole
   internal factory is only reachable through `Modifier.consentClickable`
   in `core/ConsentGesture.kt`.** The clickable's lambda is invoked by
   Compose's own pointer pipeline after a real touch release on a real
   composed UI node. Nothing else in the app — no ViewModel constructor,
   no push handler (there is no push handler), no deep-link intent
   handler, no background worker — can mint one.

3. **The `HearthApi.grantControl` Retrofit method is the sole method that
   accepts an `X-Consent-Origin` header parameter, and a client-side
   `ConsentInterceptor` throws if that header ever appears on any OTHER
   path.** If a future refactor ever accidentally hardcodes the string,
   the request fails at the client before hitting the wire, and the
   `HearthClientTest.interceptor refuses X-Consent-Origin on non-grant
   path` test catches it in CI.

4. **TLS pinning is applied at runtime after pairing.** The SPKI SHA-256
   pin is delivered by the Hearth in its `POST /api/pair` response and
   cross-checked against the QR-code fingerprint. It's persisted to
   Keystore-backed EncryptedSharedPreferences via `KeystoreStore`.

5. **No auto-backup.** `data_extraction_rules.xml` and
   `android:allowBackup="false"` prevent the JWT and SPKI pin from
   flowing to Google Drive.

## File layout

Everything is under `app/src/main/kotlin/com/hearth/companion/`.

- `core/` — client, discovery, keystore, consent primitives, WebSocket
- `models/` — server DTOs (kotlinx-serialization)
- `features/onboarding/` — discovery / QR pair / login
- `features/devices/` — remote-desktop devices, the GrantControlSheet,
  the WebSocket session view, the audit-log screen
- `features/household/` — users, personality sliders, voice preset
- `features/library/` — unified Plex / Jellyfin / Audiobookshelf / xTeVe /
  Steam library
- `features/extenders/` — Hearth Ember rooms
- `features/settings/` — about, advanced, unpair
- `uistyle/` — Compose Material3 theme with the PAL palette
