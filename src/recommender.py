import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Points for each rule in the Algorithm Recipe (see README "How a song gets its score")
ENERGY_POINTS = 4.0
VALENCE_POINTS = 3.0
MOOD_POINTS = 2.0
GENRE_POINTS = 1.5
ACOUSTIC_POINTS = 1.0

NUMERIC_FIELDS = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for this user, best match first."""
        prefs = asdict(user)
        return sorted(self.songs, key=lambda song: score_song(prefs, asdict(song))[0], reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a short sentence listing why this song scored the way it did."""
        _, reasons = score_song(asdict(user), asdict(song))
        return ", ".join(reasons) if reasons else "no strong match"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in NUMERIC_FIELDS:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def closeness(value: float, target: float) -> float:
    """Return 1.0 when value equals target, dropping toward 0 as they move apart."""
    return max(0.0, 1.0 - abs(value - target))

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    if user_prefs.get("target_energy") is not None:
        points = ENERGY_POINTS * closeness(song["energy"], user_prefs["target_energy"])
        score += points
        reasons.append(f"energy {song['energy']:.2f} vs your {user_prefs['target_energy']:.2f} (+{points:.2f})")

    if user_prefs.get("target_valence") is not None:
        points = VALENCE_POINTS * closeness(song["valence"], user_prefs["target_valence"])
        score += points
        reasons.append(f"valence {song['valence']:.2f} vs your {user_prefs['target_valence']:.2f} (+{points:.2f})")

    if song["mood"] == user_prefs.get("favorite_mood"):
        score += MOOD_POINTS
        reasons.append(f"mood match: {song['mood']} (+{MOOD_POINTS:.1f})")

    if song["genre"] == user_prefs.get("favorite_genre"):
        score += GENRE_POINTS
        reasons.append(f"genre match: {song['genre']} (+{GENRE_POINTS:.1f})")

    if user_prefs.get("likes_acoustic") is not None:
        fit = song["acousticness"] if user_prefs["likes_acoustic"] else 1.0 - song["acousticness"]
        points = ACOUSTIC_POINTS * fit
        score += points
        label = "acoustic" if user_prefs["likes_acoustic"] else "not acoustic"
        reasons.append(f"{label} fit (+{points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
