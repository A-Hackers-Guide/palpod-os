import SwiftUI

struct VoicePresetPicker: View {
    let current: String?
    @State private var selection: String?

    // Voice presets live on the Hearth. This UI is a picker over the
    // stable named identifiers; the actual TTS models never leave the
    // house.
    private let presets: [(id: String, label: String)] = [
        ("hearth.warm.f",  "Warm F"),
        ("hearth.warm.m",  "Warm M"),
        ("hearth.crisp.f", "Crisp F"),
        ("hearth.crisp.m", "Crisp M"),
        ("hearth.narrator", "Narrator"),
    ]

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Voice preset").sectionHeader()
            Picker("", selection: Binding(
                get: { selection ?? current ?? presets.first!.id },
                set: { selection = $0 }
            )) {
                ForEach(presets, id: \.id) { p in
                    Text(p.label).tag(p.id)
                }
            }
            .pickerStyle(.segmented)
        }
        .padding(14)
        .background(HearthColors.slate)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}
