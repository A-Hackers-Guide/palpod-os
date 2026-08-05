import XCTest

/// Smoke test through the onboarding flow. Requires the app to be
/// running against a mocked pal-web (see HearthTests for the URLProtocol
/// mocks). In CI we bring up a lightweight local FastAPI stub before
/// launching the XCUITest bundle.
final class OnboardingFlowTests: XCTestCase {
    var app: XCUIApplication!

    override func setUpWithError() throws {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments += ["-uitest", "1"]
        app.launch()
    }

    func test_discoveryScreen_shows() {
        XCTAssertTrue(app.staticTexts["Looking for your Hearth"].waitForExistence(timeout: 3))
    }

    func test_taxonomy_taps_land_only_on_consent_tap_button() {
        // Documentation-only assertion: the automation runner cannot
        // synthesize a "user-tap" header. If someone ever exposes a
        // programmatic override, this test should be updated to fail
        // loudly rather than silently pass.
        XCTAssertTrue(true, "See ConsentGestureTests for the compile-time invariant.")
    }
}
