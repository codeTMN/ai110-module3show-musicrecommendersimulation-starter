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


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # Starter example profile
    pop_happy = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }

    # My taste profile (see README "My taste profile")
    chill_hip_hop = {
        "favorite_genre": "hip hop",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "target_valence": 0.5,
        "likes_acoustic": False,
    }

    print_recommendations("Pop / happy (default)", pop_happy, songs)
    print_recommendations("Chill hip hop (mine)", chill_hip_hop, songs)


if __name__ == "__main__":
    main()
