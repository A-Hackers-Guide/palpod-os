// swift-tools-version:5.9
// Package.swift is provided as a fallback so the source tree can be compiled
// on any Mac with `swift build` for syntax verification, even without Xcode.
// The primary integration is the Xcode project at Hearth.xcodeproj/.
import PackageDescription

let package = Package(
    name: "Hearth",
    platforms: [
        .iOS(.v16),
        .macOS(.v13) // allows `swift build` to at least resolve non-iOS-only APIs
    ],
    products: [
        .library(name: "HearthCore", targets: ["HearthCore"]),
    ],
    targets: [
        .target(
            name: "HearthCore",
            path: "Hearth",
            exclude: [
                "Info.plist",
                "Assets.xcassets",
            ],
            sources: [
                "Core",
                "Models",
                "UIStyle",
                "Features",
                "HearthApp.swift",
            ]
        ),
        .testTarget(
            name: "HearthTests",
            dependencies: ["HearthCore"],
            path: "HearthTests"
        ),
    ]
)
