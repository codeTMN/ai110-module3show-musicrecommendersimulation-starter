# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version recommends songs based on the *vibe* of the music, not just the genre. You tell it what kind of music you like (your favorite genre, your mood, how much energy you want, and whether you want happy or sad songs), and it gives every song a score. The songs with the highest scores are your recommendations, and each one comes with a short reason why it was picked.

---

## How The System Works

### How real apps do it

Apps like Spotify and YouTube mostly learn from what people *do*. They track what you play, skip, save, replay, and add to playlists. Then they look for other people who listen like you and suggest songs those people love that you haven't heard yet. This is called **collaborative filtering**. They also look at the songs themselves, such as how fast, loud, happy, or acoustic a song sounds, and suggest songs that sound like the ones you already like. This is called **content-based filtering**. Big apps mix both, because each one covers the other's weak spots. For example, a brand new song has no plays yet, so only its sound can be used to recommend it.

### What my version does

My recommender only uses **content-based filtering**, because my data has song details but no listening history from real users. The main idea behind my design is that **energy is what makes a song feel chill or hype, not the genre**. A slow, laid-back rap song feels chill to me even though rap is usually called a high-energy genre. I also think a sad acoustic song and a happy acoustic song feel completely different, so my system checks how happy or sad a song sounds (valence) too.

### Features each `Song` uses

- `genre`: the style of music (pop, afrobeats, hip hop, folk, and more)
- `mood`: a simple label for the feeling (chill, happy, sad, intense, and more)
- `energy`: how intense the song feels, from 0 (very calm) to 1 (very intense)
- `valence`: how happy the song sounds, from 0 (sad) to 1 (happy)
- `acousticness`: how acoustic the song is, from 0 (electronic) to 1 (acoustic)

The data also has `tempo_bpm` and `danceability`, but I don't use them in the score. In this dataset they mostly go up and down with energy, so they would just count the same thing twice.

### What the `UserProfile` stores

- `favorite_genre`: the genre the user likes most
- `favorite_mood`: the mood they want right now
- `target_energy`: how much energy they want (0 to 1)
- `target_valence`: how happy or sad they want the music (0 to 1). This one is optional.
- `likes_acoustic`: whether they prefer acoustic songs (yes or no)

### How a song gets its score

Every song starts at 0 and earns points:

| Rule | Points |
|---|---|
| Energy is close to what the user wants | up to 4.0 |
| Valence is close to what the user wants | up to 3.0 |
| Mood matches | +2.0 |
| Genre matches | +1.5 |
| Acousticness fits what the user likes | up to 1.0 |

For energy and valence, the song gets more points the **closer** it is to what the user wants. It does not get more points just for having a bigger number. The math is `1 - |song value - user target|`. So if you want energy 0.4, a song at 0.4 gets full points, a song at 0.6 gets a bit less, and a song at 0.9 gets a lot less. Energy gets the most points because it matters most to me. Genre gets the fewest because two songs from different genres can still share the same vibe.

### How songs are picked

1. Score every song in the list using the rules above.
2. Sort the songs from highest to lowest score.
3. Return the top songs (5 by default) along with the reasons each one scored well.

Scoring decides how good one song is for you. Ranking compares all the songs and picks the best ones. Keeping these two steps separate means I can change the points without breaking the sorting, or change how songs are picked without touching the math.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



