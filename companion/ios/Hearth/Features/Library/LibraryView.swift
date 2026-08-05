import SwiftUI

struct LibraryView: View {
    @EnvironmentObject var session: SessionModel
    @State private var items: [MediaItem] = []
    @State private var filter: MediaItem.Source? = nil
    @State private var query = ""

    private let cols = [GridItem(.flexible()), GridItem(.flexible()), GridItem(.flexible())]

    var body: some View {
        NavigationStack {
            ZStack {
                HearthColors.void.ignoresSafeArea()
                ScrollView {
                    sourceStrip
                        .padding(.horizontal, 16).padding(.top, 6)
                    LazyVGrid(columns: cols, spacing: 12) {
                        ForEach(filtered) { item in
                            NavigationLink { ItemDetailView(item: item) } label: {
                                LibraryTile(item: item)
                            }
                        }
                    }
                    .padding(16)
                }
                .searchable(text: $query, prompt: "Search library")
            }
            .navigationTitle("Library")
        }
        .task { await load() }
    }

    private var filtered: [MediaItem] {
        items
            .filter { filter == nil ? true : $0.source == filter! }
            .filter { query.isEmpty ? true : $0.title.localizedCaseInsensitiveContains(query) }
    }

    private var sourceStrip: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                sourceChip(nil, "All")
                sourceChip(.plex, "Plex")
                sourceChip(.jellyfin, "Jellyfin")
                sourceChip(.audiobookshelf, "Books")
                sourceChip(.xTeVe, "Live")
                sourceChip(.steam, "Games")
            }
        }
    }

    private func sourceChip(_ src: MediaItem.Source?, _ label: String) -> some View {
        Button {
            filter = src
        } label: {
            Text(label)
                .font(HearthType.spec(11))
                .tracking(1.2)
                .padding(.horizontal, 12).padding(.vertical, 6)
                .foregroundStyle(filter == src ? HearthColors.void : HearthColors.bone)
                .background(filter == src ? HearthColors.pal : HearthColors.slate)
                .clipShape(Capsule())
        }
    }

    @MainActor
    private func load() async {
        guard let client = session.client else { return }
        do { items = try await client.library() }
        catch { /* soft-fail */ }
    }
}

struct LibraryTile: View {
    let item: MediaItem
    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            RoundedRectangle(cornerRadius: 6)
                .fill(HearthColors.slate)
                .aspectRatio(2/3, contentMode: .fit)
                .overlay(
                    Image(systemName: iconName)
                        .font(.system(size: 24))
                        .foregroundStyle(HearthColors.boneDim)
                )
            Text(item.title)
                .font(HearthType.body(11, weight: .medium))
                .foregroundStyle(HearthColors.bone)
                .lineLimit(2)
        }
    }

    private var iconName: String {
        switch item.kind {
        case .movie:       return "film"
        case .episode,
             .series:      return "tv"
        case .audiobook:   return "book"
        case .liveChannel: return "antenna.radiowaves.left.and.right"
        case .game:        return "gamecontroller"
        }
    }
}
