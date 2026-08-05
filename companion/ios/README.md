# Hearth iOS companion

SwiftUI app for controlling a Hearth ($95k fully-offline luxury home AI +
media server) from an iPhone or iPad on the same Wi-Fi.

## Setup

Requires Xcode 15+ and iOS 16+.

### Option A: open the Xcode project

```
open Hearth.xcodeproj
```

Select the `Hearth` scheme, pick an iPhone simulator, hit Run. There are
no third-party package dependencies to resolve — nothing to `pod install`
or `spm resolve`.

### Option B: pure SPM (syntax check only)

`Package.swift` is provided so the source tree can be compiled without
Xcode on any Mac:

```
swift build --target HearthCore
```

This validates syntax and semantics of everything under `Hearth/` as a
library. It cannot produce an `.ipa` — for that you need Xcode.

### Option C: importing sources into a fresh project

If the checked-in `project.pbxproj` fails to open in your Xcode version,
create a new project via *File → New → Project → iOS → App*, SwiftUI +
Swift, deployment target iOS 16, and:

  1. Delete the generated `ContentView.swift` and `<Name>App.swift`.
  2. Drag the `Hearth/Core`, `Hearth/Models`, `Hearth/Features`, and
     `Hearth/UIStyle` folders into the project, choosing "Create
     groups" and adding to the app target.
  3. Drag `Hearth/HearthApp.swift`, `Hearth/Info.plist`, and
     `Hearth/Assets.xcassets` in the same way.
  4. In the target's Info tab, set the Info.plist path to the bundled
     one and remove auto-generation.
  5. Repeat for `HearthTests/` and `HearthUITests/`.

## Non-negotiable boundaries

These aren't guidelines — they're structural. If you break one and try to
land a PR, the code will not compile.

### 1. Consent grants require a physical user tap

`POST /api/remote/devices/{id}/grant-control` must carry
`X-Consent-Origin: user-tap`. This app enforces that at the *type* level:

  * `ConsentGesture` (in `Hearth/Core/ConsentGesture.swift`) has no
    public initializer. It cannot be constructed except by passing a
    `_TapWitness`.
  * `_TapWitness` has a `fileprivate` initializer. The only line in the
    entire codebase that calls it lives inside the SwiftUI `Button`
    action closure of `ConsentTapButton` — which is only rendered inside
    `GrantControlSheet`.
  * `ConsentTokenSource.header(for:)` (in
    `Hearth/Core/ConsentTokenSource.swift`) takes a `ConsentGesture`
    parameter. There is no other way to obtain the header value.
  * `HearthClient.grantControl(deviceId:gesture:)` takes a
    `ConsentGesture` as a mandatory argument. There is no overload
    without one.

If you delete the `fileprivate` on `_TapWitness.init`, tests in
`HearthTests/ConsentGestureTests.swift` will start compiling their
commented-out bypass lines and blow past their assertions.

### 2. No third-party SDK dependencies

`Package.swift` declares zero `.package(url:...)` entries. `pbxproj`
declares zero `XCRemoteSwiftPackageReference`. Nothing to phone home.

Specifically banned by policy:
  * Firebase, Crashlytics
  * Segment, Amplitude, PostHog
  * Sentry, Bugsnag
  * Any push service other than local notifications driven by our own
    WebSocket

### 3. TLS pinning

`Core/HearthClient.swift` sets a `URLSessionDelegate` that rejects any
server whose leaf cert isn't the one we captured during pairing (stored
in Keychain as `com.hearthhome.hearth.pinned_cert`). The only relaxation
is during pairing itself, when we haven't captured a cert yet — and even
then only to `.local` / `localhost` hostnames.

### 4. Secrets go in the Keychain, not UserDefaults

`Core/KeychainStore.swift` is the only sanctioned store for the JWT and
CSRF token. `UserDefaults` is used only for user preferences (log level,
theme).

## Directory layout

```
Hearth.xcodeproj/           # Xcode project
Hearth/
  HearthApp.swift           # @main
  Info.plist                # Bonjour + camera usage + no-encryption
  Assets.xcassets/          # accent color + app-icon placeholder
  Core/                     # networking, discovery, keychain, consent
  Models/                   # Codable payloads
  Features/                 # SwiftUI views, one folder per tab
  UIStyle/                  # Colors / Typography / ButtonStyles
HearthTests/                # unit tests (with URLProtocol mocks)
HearthUITests/              # XCUITests
Package.swift               # SPM fallback (library target)
```

## Style tokens

Grounds are dark. `--pal` cyan (#4FC3F7) is the sole interactive accent.
`--halo` amber (#d4a256) marks status and countdowns. `--bone` (#e8e5de)
is body text. Bodoni serif for editorial display, SF Mono for spec, SF
for body. See `UIStyle/Colors.swift` and `UIStyle/Typography.swift`.
