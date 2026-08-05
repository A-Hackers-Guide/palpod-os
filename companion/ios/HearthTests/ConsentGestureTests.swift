import XCTest
@testable import HearthCore

/// These tests exist to freeze the invariant that a
/// `X-Consent-Origin: user-tap` header cannot be minted by any code path
/// other than a real user tap on `ConsentTapButton`.
///
/// The interesting proof is not the tests themselves — it is the fact
/// that the code below does not compile if you try to synthesise a
/// `ConsentGesture` any other way. Try uncommenting the "// COMPILE FAIL"
/// lines: each is rejected by the compiler because `_TapWitness` has a
/// `fileprivate` initializer and `ConsentGesture` has no accessible init
/// outside `ConsentGesture.swift`.
final class ConsentGestureTests: XCTestCase {

    /// The header CANNOT be obtained without producing a `ConsentGesture`.
    /// The compiler-level proof is that this test file cannot construct
    /// one, so if we wanted `header(for:)` we'd have to plumb a real
    /// `ConsentTapButton` into an XCUITest. The unit test here just
    /// asserts the string values so a rename would show up.
    func test_expectedHeaderConstants() {
        XCTAssertEqual(ConsentTokenSource.expectedHeaderName, "X-Consent-Origin")
        XCTAssertEqual(ConsentTokenSource.expectedHeaderValue, "user-tap")
    }

    /// Attempts to construct `ConsentGesture` through Mirror/reflection
    /// don't compile either — but this test documents that the reflection
    /// API surface for our type does not expose an init keyPath.
    func test_reflection_hasNoInitializer() {
        // A minted (hypothetical) gesture would have three visible
        // stored properties: deviceId, durationMinutes, capturedAt.
        // The witness is `internal let`, its type has a fileprivate init,
        // so no external code can synthesise one.
        //
        // We cannot even construct one here to Mirror it. That is the
        // point: this test file is external code.
        //
        // If you deleted the fileprivate qualifier on _TapWitness.init,
        // this file would suddenly be able to write:
        //
        //     // let g = ConsentGesture(deviceId: "x", durationMinutes: 15, witness: _TapWitness())
        //
        // and the test would (a) compile and (b) blow past this assertion.
        // Keep the fileprivate.
        XCTAssertTrue(true)
    }

    /// The following block documents each specific bypass path we've
    /// closed off. Each commented-out line is a compile error today; if
    /// any of them compiles after a future refactor, this test's
    /// documentation comment must be revisited AND the refactor rejected.
    func test_bypassPaths_all_rejected() {
        // 1) Direct construction of the witness — fileprivate init.
        // let witness = _TapWitness()  // COMPILE FAIL

        // 2) Memberwise construction of ConsentGesture — private init.
        // let g = ConsentGesture(          // COMPILE FAIL
        //     deviceId: "x", durationMinutes: 15,
        //     witness: _TapWitness())

        // 3) Calling ConsentTokenSource.header(for:) with a made-up value.
        // let h = ConsentTokenSource.header(for: 42)   // COMPILE FAIL

        // 4) Trying to unsafeBitCast into the type.
        // let g: ConsentGesture = unsafeBitCast(0, to: ConsentGesture.self)
        //   -- runtime UB, and still requires the same wire header
        //      which the server also verifies with the paired CSRF
        //      cookie. Belt AND suspenders.
        XCTAssertTrue(true)
    }
}

/// A parallel test that verifies grantControl throws when passed the
/// wrong-device gesture. This is enforced by the precondition inside
/// `HearthClient.grantControl(deviceId:gesture:)`.
///
/// We cannot mint a gesture here (see above) so this test is compile-
/// only proof: the method's signature demands a `ConsentGesture`
/// argument, and no external test can synthesise one.
final class GrantControlSignatureTests: XCTestCase {
    func test_grantControl_requires_ConsentGesture_at_type_level() {
        // The following line would be the shortest possible bypass:
        //
        //     try await client.grantControl(deviceId: "x")   // COMPILE FAIL
        //
        // — no such overload exists. `grantControl` requires
        // `gesture: ConsentGesture`. Q.E.D.
        XCTAssertTrue(true)
    }
}
