# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I used Claude Code (in agent mode in VS Code) to do Challenge 1: add 5 or more new song details to the dataset and make the scoring use them. I also had it do the other optional challenges in the same run: scoring modes, a diversity penalty, and a table for the output.

**Prompts used:**

- "let's do phase 5 and optional" (with screenshots of the Phase 5 and Optional Extensions instructions)
- Earlier, for the dataset: "add more songs, so the dataset is enough for the experiment" and "also add like afrobeats and other stuff, i will let you know if you are on the right track"

**What did the agent generate or change?**

- `data/songs.csv`: added 5 new columns to all 62 songs: `popularity` (0 to 100), `release_decade`, `mood_tags` (like "euphoric;playful"), `speechiness` (how much rapping or talking), and `instrumentalness` (how much of the song has no vocals)
- `src/recommender.py`:
  - `load_songs` now reads the new columns.
  - `score_song` gives points for the new details, but only if the user asks for them.
  - Added the scoring modes and the diversity penalty.
- `src/main.py`:
  - Added an "Afrobeats Night Out" profile that uses all the new details.
  - Results now print as a table.
  - Added the `--mode`, `--diverse`, and `--profile` options.
- `README.md` and `model_card.md`: wrote up the new features and pasted in the new output.
- Commands it ran: `pytest` (2 passed), `python -m src.main` with different options, and a check that compared the new results with the old ones.

**What did you verify or fix manually?**

- The agent checked that all 8 older profiles still got the exact same songs and scores as before. Because the new details only count when you ask for them, nothing old changed.
- The new numbers (popularity, decade, mood tags, and so on) are AI guesses for made-up songs. I looked over the afrobeats and hip hop rows to make sure they matched how those genres feel to me.
- I read the "Afrobeats Night Out" results to check that they made sense: *Owambe Party* first, then reggaeton and other afrobeats songs.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

The **Strategy pattern**. Each scoring mode is its own "strategy," a set of points for each rule. The scorer can swap them in and out without changing its code.

**How did AI help you brainstorm or implement it?**

The course asked for at least two ranking strategies (like "Genre-First" or "Energy-Focused") and suggested the Strategy pattern. My scoring already worked by giving points per rule, so the AI suggested the simplest version of the pattern: keep one scoring function, and make each mode an object that holds its own set of points. That way, adding a new mode is just adding one new line, not writing a whole new scoring function. It also made my earlier experiments (like doubling energy) easier, because a weight change is just a new mode.

**How does the pattern appear in your final code?**

- `ScoringMode` in `src/recommender.py` is the strategy. It holds the points for energy, valence, mood, genre, acoustic, and the new details.
- `BALANCED`, `GENRE_FIRST`, `MOOD_FIRST`, and `ENERGY_FOCUSED` are the 4 strategies, and `MODES` maps each name to its strategy.
- `score_song(user_prefs, song, mode)` and `recommend_songs(..., mode=...)` take a strategy and use its points. They don't care which one it is.
- In `src/main.py`, `--mode genre-first` (for example) picks which strategy to use.
