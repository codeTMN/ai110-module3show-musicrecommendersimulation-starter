import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict, field

FLOAT_FIELDS = {"energy", "tempo_bpm", "valence", "danceability", "acousticness",
                "speechiness", "instrumentalness"}
INT_FIELDS = {"id", "popularity", "release_decade"}

# Diversity penalty (Challenge 3): points taken off a song when the top list already has
# a song by the same artist, or already has MAX_PER_GENRE songs from the same genre.
ARTIST_PENALTY = 2.0
GENRE_PENALTY = 1.0
MAX_PER_GENRE = 2

@dataclass(frozen=True)
class ScoringMode:
    """A set of weights the scorer can swap in (Strategy pattern)."""
    name: str
    description: str
    energy: float
    valence: float
    mood: float
    genre: float
    acoustic: float
    tags: float = 0.75          # per matching mood tag, up to 2 tags
    decade: float = 1.0
    popularity: float = 1.0
    speechiness: float = 1.5
    instrumentalness: float = 1.0

BALANCED = ScoringMode("balanced", "My main recipe: energy first, then valence, mood, genre",
                       energy=4.0, valence=3.0, mood=2.0, genre=1.5, acoustic=1.0)
GENRE_FIRST = ScoringMode("genre-first", "For listeners who mostly stick to one genre",
                          energy=2.0, valence=1.5, mood=1.5, genre=5.0, acoustic=1.0)
MOOD_FIRST = ScoringMode("mood-first", "For picking music to match a feeling",
                         energy=2.0, valence=3.0, mood=5.0, genre=1.0, acoustic=0.5, tags=1.5)
ENERGY_FOCUSED = ScoringMode("energy-focused", "For workouts or sleep, where intensity is all that matters",
                             energy=8.0, valence=2.0, mood=1.0, genre=0.5, acoustic=0.5)

MODES = {mode.name: mode for mode in (BALANCED, GENRE_FIRST, MOOD_FIRST, ENERGY_FOCUSED)}

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
    popularity: int = 0
    release_decade: int = 0
    mood_tags: List[str] = field(default_factory=list)
    speechiness: float = 0.0
    instrumentalness: float = 0.0

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
    favorite_tags: Optional[List[str]] = None
    preferred_decade: Optional[int] = None
    target_popularity: Optional[int] = None
    target_speechiness: Optional[float] = None
    target_instrumentalness: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song], mode: ScoringMode = BALANCED, diverse: bool = False):
        self.songs = songs
        self.mode = mode
        self.diverse = diverse

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for this user, best match first."""
        by_id = {song.id: song for song in self.songs}
        ranked = recommend_songs(asdict(user), [asdict(song) for song in self.songs],
                                 k=k, mode=self.mode, diverse=self.diverse)
        return [by_id[song["id"]] for song, _, _ in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a short sentence listing why this song scored the way it did."""
        _, reasons = score_song(asdict(user), asdict(song), self.mode)
        return "; ".join(reasons) if reasons else "no strong match"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in row:
                if key in INT_FIELDS:
                    row[key] = int(row[key])
                elif key in FLOAT_FIELDS:
                    row[key] = float(row[key])
            row["mood_tags"] = [tag for tag in row.get("mood_tags", "").split(";") if tag]
            songs.append(row)
    return songs

def closeness(value: float, target: float, spread: float = 1.0) -> float:
    """Return 1.0 when value equals target, dropping to 0 once they are `spread` apart."""
    return max(0.0, 1.0 - abs(value - target) / spread)

def score_song(user_prefs: Dict, song: Dict, mode: ScoringMode = BALANCED) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    def add(points: float, reason: str) -> None:
        nonlocal score
        score += points
        reasons.append(f"{reason} (+{points:.2f})")

    if user_prefs.get("target_energy") is not None:
        add(mode.energy * closeness(song["energy"], user_prefs["target_energy"]),
            f"energy {song['energy']:.2f} vs your {user_prefs['target_energy']:.2f}")

    if user_prefs.get("target_valence") is not None:
        add(mode.valence * closeness(song["valence"], user_prefs["target_valence"]),
            f"valence {song['valence']:.2f} vs your {user_prefs['target_valence']:.2f}")

    if song["mood"] == user_prefs.get("favorite_mood"):
        add(mode.mood, f"mood match: {song['mood']}")

    if song["genre"] == user_prefs.get("favorite_genre"):
        add(mode.genre, f"genre match: {song['genre']}")

    if user_prefs.get("likes_acoustic") is not None:
        fit = song["acousticness"] if user_prefs["likes_acoustic"] else 1.0 - song["acousticness"]
        add(mode.acoustic * fit, "acoustic fit" if user_prefs["likes_acoustic"] else "not acoustic fit")

    # Advanced features (Challenge 1): each one only counts if the user sets it
    if user_prefs.get("favorite_tags"):
        shared = [tag for tag in song.get("mood_tags", []) if tag in user_prefs["favorite_tags"]][:2]
        if shared:
            add(mode.tags * len(shared), f"mood tags: {' / '.join(shared)}")

    if user_prefs.get("preferred_decade") is not None and song.get("release_decade") == user_prefs["preferred_decade"]:
        add(mode.decade, f"from the {song['release_decade']}s")

    if user_prefs.get("target_popularity") is not None:
        add(mode.popularity * closeness(song.get("popularity", 0), user_prefs["target_popularity"], spread=100),
            f"popularity {song.get('popularity', 0)} vs your {user_prefs['target_popularity']}")

    if user_prefs.get("target_speechiness") is not None:
        add(mode.speechiness * closeness(song.get("speechiness", 0.0), user_prefs["target_speechiness"], spread=0.4),
            f"rap/spoken words {song.get('speechiness', 0.0):.2f} vs your {user_prefs['target_speechiness']:.2f}")

    if user_prefs.get("target_instrumentalness") is not None:
        add(mode.instrumentalness * closeness(song.get("instrumentalness", 0.0), user_prefs["target_instrumentalness"]),
            f"instrumental {song.get('instrumentalness', 0.0):.2f} vs your {user_prefs['target_instrumentalness']:.2f}")

    return score, reasons

def diversity_penalty(song: Dict, picked: List[Dict]) -> Tuple[float, List[str]]:
    """Return the points to take off a song (and why) given the songs already picked."""
    penalty = 0.0
    reasons = []
    if any(other["artist"] == song["artist"] for other in picked):
        penalty += ARTIST_PENALTY
        reasons.append(f"artist already in list (-{ARTIST_PENALTY:.2f})")
    if sum(other["genre"] == song["genre"] for other in picked) >= MAX_PER_GENRE:
        penalty += GENRE_PENALTY
        reasons.append(f"already {MAX_PER_GENRE} {song['genre']} songs in list (-{GENRE_PENALTY:.2f})")
    return penalty, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    mode: ScoringMode = BALANCED, diverse: bool = False) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song, mode)) for song in songs]

    if not diverse:
        ranked = sorted(scored, key=lambda item: item[1], reverse=True)[:k]
        return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked]

    # Diverse mode: pick one song at a time, re-checking penalties against what's already picked
    picked = []
    remaining = scored
    while remaining and len(picked) < k:
        chosen_songs = [song for song, _, _ in picked]
        candidates = []
        for song, score, reasons in remaining:
            penalty, penalty_reasons = diversity_penalty(song, chosen_songs)
            candidates.append((song, score - penalty, reasons + penalty_reasons))
        best = max(candidates, key=lambda item: item[1])
        picked.append(best)
        remaining = [item for item in remaining if item[0] is not best[0]]
    return [(song, score, "; ".join(reasons)) for song, score, reasons in picked]
