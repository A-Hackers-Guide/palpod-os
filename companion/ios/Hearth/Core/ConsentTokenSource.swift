import Foundation

/// `ConsentTokenSource` is the one and only module that can produce the
/// `X-Consent-Origin: user-tap` header value.
///
/// The invariant is enforced at the type level: the sole vending method
/// takes a `ConsentGesture`, which cannot be constructed anywhere except
/// inside the SwiftUI action closure of `ConsentTapButton` (see
/// `ConsentGesture.swift`). Because `ConsentGesture` requires an
/// `_TapWitness` whose initializer is `fileprivate` to that file, no
/// other Swift code can forge a gesture, and therefore no other Swift
/// code can obtain the header. Reflection paths (`Mirror`, `KeyPath`,
/// `unsafeBitCast`) all bottom out at the same access-controlled init.
public enum ConsentTokenSource {
    public struct Header: Sendable, Equatable {
        public let name: String
        public let value: String
    }

    /// Returns the required `X-Consent-Origin` header for a
    /// grant-control call. Callers must also send `X-CSRF-Token` from
    /// the paired-session cookie; that's the `HearthClient`'s job.
    public static func header(for gesture: ConsentGesture) -> Header {
        // Touching `witness` is technically unnecessary at runtime, but
        // it prevents a future refactor from silently marking `gesture`
        // unused and letting the optimizer discard it. It also documents
        // the load-bearing role of the parameter.
        _ = gesture.witness
        return Header(name: "X-Consent-Origin", value: "user-tap")
    }

    /// The literal wire value, provided for tests. NOT usable for
    /// bypass: this returns the literal string but the actual outbound
    /// header on `HearthClient` is only attached when a `ConsentGesture`
    /// is supplied to `grantControl(...)`.
    public static let expectedHeaderValue = "user-tap"
    public static let expectedHeaderName = "X-Consent-Origin"
}
