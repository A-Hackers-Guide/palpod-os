import SwiftUI

/// Small shims so the shared source tree compiles cleanly on macOS host
/// (`swift build`) as well as iOS. Real behaviour is iOS-only; on other
/// platforms these are no-ops.
extension View {
    @ViewBuilder
    func navBarTitleInline() -> some View {
#if os(iOS)
        self.navigationBarTitleDisplayMode(.inline)
#else
        self
#endif
    }

    @ViewBuilder
    func insetGroupedList() -> some View {
#if os(iOS)
        self.listStyle(.insetGrouped)
#else
        self.listStyle(.inset)
#endif
    }
}
