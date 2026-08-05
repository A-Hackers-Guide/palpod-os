import XCTest
@testable import HearthCore

final class PersonalityAxisTests: XCTestCase {
    func test_clamped_pinsOutOfRange() {
        let a = PersonalityAxes(reservedToChatty: -0.4, formalToCasual: 1.7, seriousToPlayful: 0.3).clamped()
        XCTAssertEqual(a.reservedToChatty, 0, accuracy: 0.001)
        XCTAssertEqual(a.formalToCasual, 1, accuracy: 0.001)
        XCTAssertEqual(a.seriousToPlayful, 0.3, accuracy: 0.001)
    }

    func test_defaults_areCentered() {
        XCTAssertEqual(PersonalityAxes.defaults.reservedToChatty, 0.5, accuracy: 0.001)
        XCTAssertEqual(PersonalityAxes.defaults.formalToCasual, 0.5, accuracy: 0.001)
        XCTAssertEqual(PersonalityAxes.defaults.seriousToPlayful, 0.5, accuracy: 0.001)
    }

    func test_codableRoundtrip_usesSnakeCase() throws {
        let a = PersonalityAxes(reservedToChatty: 0.2, formalToCasual: 0.7, seriousToPlayful: 0.9)
        let data = try JSONEncoder().encode(a)
        let json = String(data: data, encoding: .utf8)!
        XCTAssertTrue(json.contains("reserved_to_chatty"))
        XCTAssertTrue(json.contains("formal_to_casual"))
        XCTAssertTrue(json.contains("serious_to_playful"))

        let decoded = try JSONDecoder().decode(PersonalityAxes.self, from: data)
        XCTAssertEqual(decoded, a)
    }
}

final class PairPayloadTests: XCTestCase {
    func test_parsesValidURL() {
        let url = URL(string: "hearth://pair?token=abc123&fingerprint=deadbeef")!
        let p = PairPayload(url: url)
        XCTAssertEqual(p?.token, "abc123")
        XCTAssertEqual(p?.fingerprint, "deadbeef")
    }

    func test_rejectsWrongScheme() {
        let url = URL(string: "https://pair?token=abc&fingerprint=x")!
        XCTAssertNil(PairPayload(url: url))
    }

    func test_rejectsMissingToken() {
        let url = URL(string: "hearth://pair?fingerprint=x")!
        XCTAssertNil(PairPayload(url: url))
    }
}
