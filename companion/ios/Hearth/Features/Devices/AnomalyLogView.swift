import SwiftUI

struct AnomalyLogView: View {
    let client: HearthClient
    let sessionId: String
    @State private var anomalies: [SessionAnomaly] = []
    @State private var loading = false
    @State private var error: String?

    var body: some View {
        NavigationStack {
            ZStack {
                HearthColors.void.ignoresSafeArea()
                List(anomalies) { anom in
                    HStack(alignment: .top, spacing: 12) {
                        Circle().fill(color(for: anom.severity)).frame(width: 8, height: 8).padding(.top, 6)
                        VStack(alignment: .leading, spacing: 4) {
                            Text(anom.kind)
                                .font(HearthType.spec(12))
                                .foregroundStyle(HearthColors.pal)
                            Text(anom.message)
                                .font(HearthType.body(13))
                                .foregroundStyle(HearthColors.bone)
                            Text(anom.at.formatted(date: .abbreviated, time: .standard))
                                .font(HearthType.spec(10))
                                .foregroundStyle(HearthColors.boneDim)
                        }
                    }
                    .listRowBackground(HearthColors.slate)
                }
                .listStyle(.plain)
                .scrollContentBackground(.hidden)
                if loading { ProgressView().tint(HearthColors.pal) }
            }
            .navigationTitle("Audit log")
        }
        .task { await refresh() }
    }

    @MainActor
    private func refresh() async {
        loading = true
        defer { loading = false }
        do { anomalies = try await client.anomalies(sessionId: sessionId) }
        catch { self.error = error.localizedDescription }
    }

    private func color(for s: SessionAnomaly.Severity) -> Color {
        switch s {
        case .info: return HearthColors.pal
        case .warn: return HearthColors.halo
        case .critical: return HearthColors.ember
        }
    }
}
