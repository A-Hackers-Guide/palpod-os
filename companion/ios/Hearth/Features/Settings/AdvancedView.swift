import SwiftUI

struct AdvancedView: View {
    @EnvironmentObject var session: SessionModel
    @AppStorage("hearth.logLevel") private var logLevel: String = "info"

    var body: some View {
        ZStack {
            HearthColors.void.ignoresSafeArea()
            List {
                Section("Logging") {
                    Picker("Log level", selection: $logLevel) {
                        Text("Silent").tag("silent")
                        Text("Errors").tag("error")
                        Text("Info").tag("info")
                        Text("Debug").tag("debug")
                    }
                }
                .listRowBackground(HearthColors.slate)

                Section("Network") {
                    row("Base URL", session.client?.baseURL.absoluteString ?? "—")
                    row("TLS pinning", KeychainStore().data(for: .pinnedCert) == nil ? "Not pinned" : "Pinned")
                    row("JWT", KeychainStore().string(for: .jwt) == nil ? "Absent" : "Stored")
                }
                .listRowBackground(HearthColors.slate)

                Section("Consent") {
                    row("Header source", "\(ConsentTokenSource.expectedHeaderName): \(ConsentTokenSource.expectedHeaderValue)")
                    row("Enforcement", "Type-level (see ConsentGesture.swift)")
                }
                .listRowBackground(HearthColors.slate)
            }
            .insetGroupedList()
            .scrollContentBackground(.hidden)
        }
        .navigationTitle("Advanced")
    }

    private func row(_ k: String, _ v: String) -> some View {
        HStack {
            Text(k).font(HearthType.body(14)).foregroundStyle(HearthColors.bone)
            Spacer()
            Text(v).font(HearthType.spec(11)).foregroundStyle(HearthColors.boneDim).multilineTextAlignment(.trailing)
        }
    }
}
