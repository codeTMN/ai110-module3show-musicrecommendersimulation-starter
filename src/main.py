"""
Command line runner for the Music Recommender Simulation.

Examples:
    python -m src.main                          # all profiles, balanced mode
    python -m src.main --mode genre-first       # switch scoring mode
    python -m src.main --diverse                # turn on the diversity penalty
    python -m src.main --profile "Chill Lofi"   # run just one profile
"""

import argparse
import textwrap

from src.recommender import load_songs, recommend_songs, MODES


PROFILES = {
    # Normal listeners
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "target_valence": 0.8,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "target_valence": 0.4,
        "likes_acoustic": False,
    },
    "Chill Hip Hop (mine)": {
        "favorite_genre": "hip hop",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "target_valence": 0.5,
        "likes_acoustic": False,
    },
    # Edge cases: profiles meant to trick the scoring
    "Edge: high energy but sad": {
        "favorite_genre": "pop",
        "favorite_mood": "sad",
        "target_energy": 0.9,
        "target_valence": 0.2,
    },
    "Edge: acoustic metalhead": {
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 0.95,
        "likes_acoustic": True,
    },
    "Edge: genre not in catalog": {
        "favorite_genre": "k-pop",
        "favorite_mood": "happy",
        "target_energy": 0.75,
    },
    "Edge: capital letters": {
        "favorite_genre": "Hip Hop",
        "favorite_mood": "Chill",
        "target_energy": 0.35,
    },
    # Uses the advanced features (popularity, decade, mood tags, speechiness, instrumentalness)
    "Afrobeats Night Out (advanced)": {
        "favorite_genre": "afrobeats",
        "favorite_mood": "energetic",
        "target_energy": 0.8,
        "target_valence": 0.85,
        "likes_acoustic": False,
        "favorite_tags": ["euphoric", "playful"],
        "preferred_decade": 2020,
        "target_popularity": 80,
        "target_speechiness": 0.1,
        "target_instrumentalness": 0.0,
    },
}


def format_table(headers: list, rows: list) -> str:
    """Draw an ASCII table where each cell is a list of lines."""
    widths = [max(len(line) for cell in [[h]] + [row[i] for row in rows] for line in cell)
              for i, h in enumerate(headers)]
    border = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def draw(cells: list) -> list:
        height = max(len(cell) for cell in cells)
        return ["| " + " | ".join((cell[n] if n < len(cell) else "").ljust(w)
                                  for cell, w in zip(cells, widths)) + " |"
                for n in range(height)]

    lines = [border, *draw([[h] for h in headers]), border]
    for row in rows:
        lines += draw(row) + [border]
    return "\n".join(lines)


def print_recommendations(name: str, user_prefs: dict, songs: list, mode, diverse: bool, k: int = 5) -> None:
    """Print a profile's top k songs as a table with scores and reasons."""
    print(f"Profile: {name}   (mode: {mode.name}{', diverse' if diverse else ''})")
    print(textwrap.fill(", ".join(f"{key}={value}" for key, value in user_prefs.items()),
                        width=100, initial_indent="  ", subsequent_indent="  "))

    rows = []
    for rank, (song, score, explanation) in enumerate(
            recommend_songs(user_prefs, songs, k=k, mode=mode, diverse=diverse), start=1):
        reasons = [line for reason in explanation.split("; ") for line in textwrap.wrap(reason, 44)]
        rows.append([[str(rank)], [song["title"], f"by {song['artist']}"],
                     [song["genre"], song["mood"]], [f"{score:.2f}"], reasons])

    print(format_table(["#", "Song", "Genre / Mood", "Score", "Why"], rows))
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument("--mode", choices=MODES, default="balanced", help="scoring mode to use")
    parser.add_argument("--diverse", action="store_true", help="penalize repeat artists and genres")
    parser.add_argument("--profile", choices=PROFILES, help="run only this profile")
    args = parser.parse_args()

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    print(f"Mode: {args.mode} - {MODES[args.mode].description}\n")

    for name, user_prefs in PROFILES.items():
        if args.profile is None or args.profile == name:
            print_recommendations(name, user_prefs, songs, MODES[args.mode], args.diverse)


if __name__ == "__main__":
    main()
