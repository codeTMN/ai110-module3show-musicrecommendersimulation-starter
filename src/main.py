"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, score_song


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a profile's top k songs with their scores and reasons."""
    print("=" * 60)
    print(f"Profile: {name}")
    print("  " + ", ".join(f"{key}={value}" for key, value in user_prefs.items()))
    print("=" * 60)

    for rank, (song, score, _) in enumerate(recommend_songs(user_prefs, songs, k=k), start=1):
        print(f"{rank}. {song['title']} by {song['artist']}  ({song['genre']}, {song['mood']})")
        print(f"   Score: {score:.2f}")
        for reason in score_song(user_prefs, song)[1]:
            print(f"   - {reason}")
        print()


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
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
