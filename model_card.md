# 🎧 Model Card: VibeMatch 1.0

## 1. Model Name  

**VibeMatch 1.0.** It finds songs that match the *vibe* you're in the mood for, mostly based on energy instead of genre.

---

## 2. Intended Use  

**Goal:** VibeMatch tries to guess which songs from a small catalog a person will like, based on the taste they describe. Then it explains why it picked each song.

**What it's for:**
- A classroom project to learn how music recommenders work
- Trying out different listener types and seeing how the results change
- Testing how changing the points (weights) changes what gets recommended

**What it assumes about the user:** that they can describe what they want (a favorite genre, a mood, and how much energy, from 0 to 1), that they have one favorite genre and one mood, and that their taste doesn't change while they listen.

**What it's NOT for:**
- Real users or a real music app. The songs are made up and the numbers are estimates.
- Deciding what music is "good," or anything like charts or paying artists
- Filtering music for kids. It doesn't look at lyrics at all.
- Learning what you like over time. It never sees what you play or skip.

---

## 3. How the Model Works  

Every song starts at 0 points and earns more the better it fits you:

- **Energy (up to 4 points):** the closer the song's energy is to what you want, the more points. A perfect match gets all 4. A song that's a little off gets a bit less, and a song that's way off gets almost nothing.
- **Happy or sad sound (up to 3 points):** same idea, using valence (how happy the song sounds).
- **Mood match (2 points):** if the song's mood is the one you picked.
- **Genre match (1.5 points):** if the song is your favorite genre.
- **Acoustic fit (up to 1 point):** more points for acoustic songs if you like acoustic, or for electronic songs if you don't.

Then it sorts all the songs from most points to least and shows you the top 5, with a list of where each song's points came from.

**What I changed from the starter idea:** The course suggested genre 2 points, mood 1 point, plus energy. I flipped that around. Energy counts the most, mood counts more than genre, and I added valence. I did this because I think a song feels chill or hype because of its energy, not its genre. A slow rap song can be just as chill as lofi.

**Extras I added later:**
- **4 scoring modes** that change the points: balanced, genre-first, mood-first, energy-focused.
- **A diversity penalty** so the same artist doesn't show up twice.
- **5 more song details** (popularity, decade, mood tags, rap/talking, instrumental) that only count if you ask for them.

---

## 4. Data  

- **62 songs.** The starter file had 10. I added 52 more with AI help.
- **19 genres,** each with at least 3 songs: pop, lofi, rock, afrobeats, hip hop, ambient, jazz, synthwave, indie pop, amapiano, drill, folk, country, r&b, classical, reggaeton, dancehall, metal, and liquid dnb.
- **10 moods:** sad (14 songs), happy (9), chill (7), relaxed (7), energetic (6), intense (5), moody (4), focused (4), romantic (3), and angry (3).
- **Each song has:** genre, mood, energy, tempo, valence, danceability, acousticness, popularity, release decade, mood tags, speechiness, and instrumentalness.

**Limits of the data:**
- The songs and artists are made up. The numbers are estimates of what each genre usually sounds like, not measured from real audio.
- The moods are uneven. Sad listeners get 14 songs to pick from, but romantic and angry listeners only get 3.
- Each song has only one genre and one mood, but real songs can be more than one thing.
- There's no lyrics, language, or listening history. That's a big part of real taste that's missing.

---

## 5. Strengths  

- **It gets the vibe right across genres.** My chill hip hop profile got chill lofi, pop, and dnb songs, and no hype rap songs. That's how I actually think about music.
- **Opposite listeners get opposite results.** The happy pop fan and the chill lofi fan had zero songs in common.
- **It handles tricky combos.** "High energy but sad" found *Dancing Alone*, a sad song you can still dance to.
- **It explains itself.** Every song shows exactly where its points came from, so you can see why it was picked.
- **It doesn't break on unknown genres.** A k-pop fan still got happy songs with the right energy.
- **Different listeners can pick a mode.** Genre-first works for genre-loyal fans, and balanced works for vibe listeners like me.

---

## 6. Limitations and Bias 

**The biggest weakness I found: genre counts so little that genre fans get songs from other genres.** I gave genre only 1.5 points on purpose, because I think energy is what makes a vibe. But when I tested a "Deep Intense Rock" fan, only 2 of the top 5 songs were rock. Drill, dancehall, and hip hop took spots 2, 3, and 4, even though there are 4 rock songs in the catalog. Those songs just had the right energy and the "intense" mood, and that was enough to beat a genre match. This works for someone like me who cares about the vibe, but a person who only listens to rock would feel like the app isn't listening to them.

Other problems I found:

- **Capital letters used to break matching (now fixed).** When I first tested it, typing "Hip Hop" instead of "hip hop" made the genre and mood checks fail without any warning. The system fell back on energy only, and a sad country song (*Whiskey Letters*) tied for #1 for a chill hip hop fan. I fixed it so the system ignores capital letters and extra spaces. It still can't match different spellings like "hip-hop" with a dash.
- **The acoustic preference barely matters.** It's only worth up to 1 point. When I tested an "acoustic metalhead", the system ignored the acoustic part and gave them electric metal songs that are almost 0% acoustic.
- **Genres that aren't in the catalog fail quietly.** A k-pop fan gets happy songs from other genres. That's not bad, but the system never tells them there's no k-pop.
- **Some moods have way more songs.** There are 14 sad songs but only 3 romantic and 3 angry ones, so sad listeners get much better choices.
- **Filter bubble.** The system only finds songs close to what you already said you like. It will never surprise you with something different that you'd end up loving.

**Update after the optional extensions:** The new **genre-first** mode fixes the rock fan problem. With it, 4 of the top 5 songs are rock. But the default mode is still my balanced recipe, so a rock fan who doesn't know to switch modes still gets mixed results. The new **diversity penalty** also stops the same artist from showing up twice, which happened for the metal fan (two *Ironclad* songs).

---

## 7. Evaluation  

### Profiles I tested

I tested 4 normal listeners and 4 "edge case" listeners that were made to trick the system:

| Profile | What it wants | Top song |
|---|---|---|
| High-Energy Pop | pop, happy, energy 0.85, happy-sounding | Sunrise City (pop) |
| Chill Lofi | lofi, chill, energy 0.35, likes acoustic | Library Rain (lofi) |
| Deep Intense Rock | rock, intense, energy 0.9, darker sound | Storm Runner (rock) |
| Chill Hip Hop (mine) | hip hop, chill, energy 0.35 | Late Night Verses (hip hop) |
| Edge: high energy but sad | pop, sad, energy 0.9, sad-sounding | Dancing Alone (pop) |
| Edge: acoustic metalhead | metal, angry, energy 0.95, likes acoustic | Breaking Point (metal) |
| Edge: genre not in catalog | k-pop, happy, energy 0.75 | Rooftop Lights (indie pop) |
| Edge: capital letters | "Hip Hop", "Chill", energy 0.35 | Before the fix: Library Rain and Whiskey Letters (sad country), tied. After: Late Night Verses (hip hop) |

For each one I checked if the top 5 matched the vibe the profile asked for, and if the reasons made sense.

### Does it feel right?

For my own profile (Chill Hip Hop), yes. *Late Night Verses* is #1, and the rest are chill lofi, pop, and dnb songs. None of them are hype rap songs like *Crown Up*. That matches how I think about music: a chill song is chill because of its energy, not its genre.

**Why did *Late Night Verses* come first?** It's the only song that gets points from every rule. Its energy (0.38) is almost exactly what I asked for (+3.88), its valence is almost exactly right (+2.94), it matches my mood (+2.0) and my genre (+1.5), and it isn't acoustic (+0.70). That adds up to 11.02. The #2 song, *Sunday Sheets*, is close on everything except genre, so it loses about 2 points.

### Comparing profiles

- **High-Energy Pop vs Chill Lofi:** These two have no songs in common. Pop gets fast, upbeat songs (energy 0.74 to 0.82), and lofi gets slow, calm songs (energy 0.28 to 0.42). This makes sense, because energy is my biggest rule, and these two users want opposite energy.
- **Chill Lofi vs Chill Hip Hop:** 4 of the 5 songs are the same, just in a different order. Both want chill songs at energy 0.35, so the genre bonus only decides who goes first. The one difference: the lofi fan gets *Spacewalk Thoughts* because they like acoustic, and the hip hop fan gets *Drift Current* because they don't.
- **High-Energy Pop vs Deep Intense Rock:** Both want high energy, but the pop fan gets happy songs and the rock fan gets darker, intense ones. Mood and valence are what split these two apart.
- **Deep Intense Rock vs Chill Hip Hop:** *Crown Up* is a hip hop song, but it shows up for the **rock** fan, not the hip hop fan. It has the intense energy the rock fan wants, and it's way too intense for a chill listener. This is my "energy over genre" idea working.
- **High-Energy Pop vs High energy but sad:** Same genre and almost the same energy, but changing the mood from happy to sad changes the whole list. The only pop song left is *Dancing Alone*, a sad dance song, and the rest are sad metal, drill, rock, and hip hop.
- **Chill Hip Hop vs Capital letters:** These ask for the same thing, but at first, typing "Hip Hop" with capitals made the genre and mood checks fail. *Late Night Verses* dropped from #1 to #4, and a sad country song tied for first. That one surprised me the most, so I fixed it. Now the system lowercases words before comparing them, and *Late Night Verses* is back at #1 with an all-chill top 5. The scores are lower than my normal profile only because this profile doesn't set valence or acoustic.
- **Acoustic metalhead vs Deep Intense Rock:** Both get loud, high-energy songs. The "likes acoustic" setting barely changed anything, because it's worth so few points.

### Why does *Gym Hero* show up for "Happy Pop" fans?

In my normal system it doesn't. But when I turned off the mood rule as an experiment, *Gym Hero* jumped to #2 for the High-Energy Pop fan. Here's why, in plain words: *Gym Hero* is a pop song with high energy and a fairly happy sound, so it scores well on genre, energy, and valence. The only thing wrong with it is that it's an *intense* workout song, not a *happy* one. Without the mood rule, the system can't see that difference, so it thinks *Gym Hero* is almost perfect. The mood rule is what keeps it out.

### Experiments I ran

1. **Weight shift (energy doubled to 8.0, genre cut in half to 0.75):** Mostly the same songs came back, just in a slightly different order. It made results **different, not more accurate**. For the "high energy but sad" profile it got worse: sad metal beat the sad pop song, and angry metal songs (not sad ones) got into the top 5.
2. **Turning off the mood rule:** This made things clearly **worse**. Hype songs like *Gym Hero* showed up for happy listeners, and sad and intense songs (*Gone Too Soon*, *Crown Up*) got into my chill hip hop list. Mood is doing a lot of important work.

### Scoring modes (optional extension)

I added 4 modes you can switch between with `--mode`:

| Mode | What it cares about most |
|---|---|
| balanced (default) | energy 4.0, valence 3.0, mood 2.0, genre 1.5 |
| genre-first | genre 5.0, then energy 2.0 |
| mood-first | mood 5.0, valence 3.0, mood tags count double |
| energy-focused | energy 8.0, genre only 0.5 |

What I saw when I compared them:

- **Deep Intense Rock in genre-first mode:** 4 of the top 5 are now rock songs (*Storm Runner*, *No More Lies*, *Open Highway*, *Paper Walls*). This is the mode a rock-only fan would want.
- **High-Energy Pop in genre-first mode:** It got worse for this user. *Gym Hero* (intense) and *Dancing Alone* (sad) jumped in just because they're pop. So no single mode is best for everyone. It depends on what kind of listener you are.
- **Chill Hip Hop in genre-first mode:** It pulled in *Crown Up*, a hype rap song, which goes against how I listen. Balanced and mood-first both kept my list all chill.
- **Energy-focused and mood-first** mostly gave the same songs as balanced in a different order, for all three profiles.

### Diversity penalty (optional extension)

With `--diverse`, a song loses 2 points if its artist is already in the list, and 1 point if 2 songs from its genre are already in the list.

- **Acoustic metalhead:** *Ashes Fall* got pushed out because *Ironclad* already had *Breaking Point* at #1. *Swing Shift* (jazz) took its spot.
- **Deep Intense Rock in genre-first + diverse:** *Paper Walls* dropped out. Its band was already in the list and there were already 2 rock songs, so it lost 3 points.
- **Most profiles didn't change at all,** because their top 5 already had different artists. The penalty only steps in when it's needed.

### Advanced features (optional extension)

I added 5 new song details: **popularity** (0 to 100), **release decade**, **mood tags** (like "euphoric" or "nostalgic"), **speechiness** (how much rapping or talking), and **instrumentalness** (how much of the song has no vocals). They only count if the user asks for them, so none of the older profiles changed. I tested them with an "Afrobeats Night Out" profile: popular, 2020s, euphoric and playful, a little rap, and full vocals. *Owambe Party* came first with 17.04 points because it matched almost every rule.

### Full output for every profile

These come from `python -m src.main` (balanced mode, no diversity penalty).

<details>
<summary><b>High-Energy Pop</b></summary>

```
Profile: High-Energy Pop   (mode: balanced)
  favorite_genre=pop, favorite_mood=happy, target_energy=0.85, target_valence=0.8,
  likes_acoustic=False
+---+------------------+--------------+-------+-----------------------------------+
| # | Song             | Genre / Mood | Score | Why                               |
+---+------------------+--------------+-------+-----------------------------------+
| 1 | Sunrise City     | pop          | 11.08 | energy 0.82 vs your 0.85 (+3.88)  |
|   | by Neon Echo     | happy        |       | valence 0.84 vs your 0.80 (+2.88) |
|   |                  |              |       | mood match: happy (+2.00)         |
|   |                  |              |       | genre match: pop (+1.50)          |
|   |                  |              |       | not acoustic fit (+0.82)          |
+---+------------------+--------------+-------+-----------------------------------+
| 2 | Calor Total      | reggaeton    | 9.54  | energy 0.82 vs your 0.85 (+3.88)  |
|   | by Fuego Sur     | happy        |       | valence 0.88 vs your 0.80 (+2.76) |
|   |                  |              |       | mood match: happy (+2.00)         |
|   |                  |              |       | not acoustic fit (+0.90)          |
+---+------------------+--------------+-------+-----------------------------------+
| 3 | Open Highway     | rock         | 9.40  | energy 0.80 vs your 0.85 (+3.80)  |
|   | by Steel Avenue  | happy        |       | valence 0.75 vs your 0.80 (+2.85) |
|   |                  |              |       | mood match: happy (+2.00)         |
|   |                  |              |       | not acoustic fit (+0.75)          |
+---+------------------+--------------+-------+-----------------------------------+
| 4 | Island Bounce    | dancehall    | 9.37  | energy 0.74 vs your 0.85 (+3.56)  |
|   | by Yard Vibes    | happy        |       | valence 0.83 vs your 0.80 (+2.91) |
|   |                  |              |       | mood match: happy (+2.00)         |
|   |                  |              |       | not acoustic fit (+0.90)          |
+---+------------------+--------------+-------+-----------------------------------+
| 5 | Rooftop Lights   | indie pop    | 9.26  | energy 0.76 vs your 0.85 (+3.64)  |
|   | by Indigo Parade | happy        |       | valence 0.81 vs your 0.80 (+2.97) |
|   |                  |              |       | mood match: happy (+2.00)         |
|   |                  |              |       | not acoustic fit (+0.65)          |
+---+------------------+--------------+-------+-----------------------------------+
```

</details>
<details>
<summary><b>Chill Lofi</b></summary>

```
Profile: Chill Lofi   (mode: balanced)
  favorite_genre=lofi, favorite_mood=chill, target_energy=0.35, likes_acoustic=True
+---+--------------------+--------------+-------+----------------------------------+
| # | Song               | Genre / Mood | Score | Why                              |
+---+--------------------+--------------+-------+----------------------------------+
| 1 | Library Rain       | lofi         | 8.36  | energy 0.35 vs your 0.35 (+4.00) |
|   | by Paper Lanterns  | chill        |       | mood match: chill (+2.00)        |
|   |                    |              |       | genre match: lofi (+1.50)        |
|   |                    |              |       | acoustic fit (+0.86)             |
+---+--------------------+--------------+-------+----------------------------------+
| 2 | Midnight Coding    | lofi         | 7.93  | energy 0.42 vs your 0.35 (+3.72) |
|   | by LoRoom          | chill        |       | mood match: chill (+2.00)        |
|   |                    |              |       | genre match: lofi (+1.50)        |
|   |                    |              |       | acoustic fit (+0.71)             |
+---+--------------------+--------------+-------+----------------------------------+
| 3 | Spacewalk Thoughts | ambient      | 6.64  | energy 0.28 vs your 0.35 (+3.72) |
|   | by Orbit Bloom     | chill        |       | mood match: chill (+2.00)        |
|   |                    |              |       | acoustic fit (+0.92)             |
+---+--------------------+--------------+-------+----------------------------------+
| 4 | Sunday Sheets      | pop          | 6.20  | energy 0.40 vs your 0.35 (+3.80) |
|   | by Mira Vale       | chill        |       | mood match: chill (+2.00)        |
|   |                    |              |       | acoustic fit (+0.40)             |
+---+--------------------+--------------+-------+----------------------------------+
| 5 | Late Night Verses  | hip hop      | 6.18  | energy 0.38 vs your 0.35 (+3.88) |
|   | by Kay Mellow      | chill        |       | mood match: chill (+2.00)        |
|   |                    |              |       | acoustic fit (+0.30)             |
+---+--------------------+--------------+-------+----------------------------------+
```

</details>
<details>
<summary><b>Deep Intense Rock</b></summary>

```
Profile: Deep Intense Rock   (mode: balanced)
  favorite_genre=rock, favorite_mood=intense, target_energy=0.9, target_valence=0.4,
  likes_acoustic=False
+---+--------------------+--------------+-------+-----------------------------------+
| # | Song               | Genre / Mood | Score | Why                               |
+---+--------------------+--------------+-------+-----------------------------------+
| 1 | Storm Runner       | rock         | 11.12 | energy 0.91 vs your 0.90 (+3.96)  |
|   | by Voltline        | intense      |       | valence 0.48 vs your 0.40 (+2.76) |
|   |                    |              |       | mood match: intense (+2.00)       |
|   |                    |              |       | genre match: rock (+1.50)         |
|   |                    |              |       | not acoustic fit (+0.90)          |
+---+--------------------+--------------+-------+-----------------------------------+
| 2 | Back Block         | drill        | 9.60  | energy 0.85 vs your 0.90 (+3.80)  |
|   | by Grime Unit      | intense      |       | valence 0.35 vs your 0.40 (+2.85) |
|   |                    |              |       | mood match: intense (+2.00)       |
|   |                    |              |       | not acoustic fit (+0.95)          |
+---+--------------------+--------------+-------+-----------------------------------+
| 3 | Bad Mind           | dancehall    | 9.41  | energy 0.88 vs your 0.90 (+3.92)  |
|   | by Rudie King      | intense      |       | valence 0.55 vs your 0.40 (+2.55) |
|   |                    |              |       | mood match: intense (+2.00)       |
|   |                    |              |       | not acoustic fit (+0.94)          |
+---+--------------------+--------------+-------+-----------------------------------+
| 4 | Crown Up           | hip hop      | 9.20  | energy 0.88 vs your 0.90 (+3.92)  |
|   | by Blaze Carter    | intense      |       | valence 0.62 vs your 0.40 (+2.34) |
|   |                    |              |       | mood match: intense (+2.00)       |
|   |                    |              |       | not acoustic fit (+0.94)          |
+---+--------------------+--------------+-------+-----------------------------------+
| 5 | No More Lies       | rock         | 9.12  | energy 0.90 vs your 0.90 (+4.00)  |
|   | by The Static Kids | angry        |       | valence 0.30 vs your 0.40 (+2.70) |
|   |                    |              |       | genre match: rock (+1.50)         |
|   |                    |              |       | not acoustic fit (+0.92)          |
+---+--------------------+--------------+-------+-----------------------------------+
```

</details>
<details>
<summary><b>Chill Hip Hop (mine)</b></summary>

```
Profile: Chill Hip Hop (mine)   (mode: balanced)
  favorite_genre=hip hop, favorite_mood=chill, target_energy=0.35, target_valence=0.5,
  likes_acoustic=False
+---+-------------------+--------------+-------+-----------------------------------+
| # | Song              | Genre / Mood | Score | Why                               |
+---+-------------------+--------------+-------+-----------------------------------+
| 1 | Late Night Verses | hip hop      | 11.02 | energy 0.38 vs your 0.35 (+3.88)  |
|   | by Kay Mellow     | chill        |       | valence 0.52 vs your 0.50 (+2.94) |
|   |                   |              |       | mood match: chill (+2.00)         |
|   |                   |              |       | genre match: hip hop (+1.50)      |
|   |                   |              |       | not acoustic fit (+0.70)          |
+---+-------------------+--------------+-------+-----------------------------------+
| 2 | Sunday Sheets     | pop          | 8.95  | energy 0.40 vs your 0.35 (+3.80)  |
|   | by Mira Vale      | chill        |       | valence 0.65 vs your 0.50 (+2.55) |
|   |                   |              |       | mood match: chill (+2.00)         |
|   |                   |              |       | not acoustic fit (+0.60)          |
+---+-------------------+--------------+-------+-----------------------------------+
| 3 | Drift Current     | liquid dnb   | 8.90  | energy 0.50 vs your 0.35 (+3.40)  |
|   | by Glass Harbor   | chill        |       | valence 0.60 vs your 0.50 (+2.70) |
|   |                   |              |       | mood match: chill (+2.00)         |
|   |                   |              |       | not acoustic fit (+0.80)          |
+---+-------------------+--------------+-------+-----------------------------------+
| 4 | Library Rain      | lofi         | 8.84  | energy 0.35 vs your 0.35 (+4.00)  |
|   | by Paper Lanterns | chill        |       | valence 0.60 vs your 0.50 (+2.70) |
|   |                   |              |       | mood match: chill (+2.00)         |
|   |                   |              |       | not acoustic fit (+0.14)          |
+---+-------------------+--------------+-------+-----------------------------------+
| 5 | Midnight Coding   | lofi         | 8.83  | energy 0.42 vs your 0.35 (+3.72)  |
|   | by LoRoom         | chill        |       | valence 0.56 vs your 0.50 (+2.82) |
|   |                   |              |       | mood match: chill (+2.00)         |
|   |                   |              |       | not acoustic fit (+0.29)          |
+---+-------------------+--------------+-------+-----------------------------------+
```

</details>
<details>
<summary><b>Edge: high energy but sad</b></summary>

```
Profile: Edge: high energy but sad   (mode: balanced)
  favorite_genre=pop, favorite_mood=sad, target_energy=0.9, target_valence=0.2
+---+--------------------+--------------+-------+-----------------------------------+
| # | Song               | Genre / Mood | Score | Why                               |
+---+--------------------+--------------+-------+-----------------------------------+
| 1 | Dancing Alone      | pop          | 9.40  | energy 0.70 vs your 0.90 (+3.20)  |
|   | by Mira Vale       | sad          |       | valence 0.30 vs your 0.20 (+2.70) |
|   |                    |              |       | mood match: sad (+2.00)           |
|   |                    |              |       | genre match: pop (+1.50)          |
+---+--------------------+--------------+-------+-----------------------------------+
| 2 | Ashes Fall         | metal        | 8.45  | energy 0.80 vs your 0.90 (+3.60)  |
|   | by Ironclad        | sad          |       | valence 0.15 vs your 0.20 (+2.85) |
|   |                    |              |       | mood match: sad (+2.00)           |
+---+--------------------+--------------+-------+-----------------------------------+
| 3 | Quiet Before       | drill        | 7.60  | energy 0.55 vs your 0.90 (+2.60)  |
|   | by South Ends      | sad          |       | valence 0.20 vs your 0.20 (+3.00) |
|   |                    |              |       | mood match: sad (+2.00)           |
+---+--------------------+--------------+-------+-----------------------------------+
| 4 | Paper Walls        | rock         | 7.30  | energy 0.55 vs your 0.90 (+2.60)  |
|   | by The Static Kids | sad          |       | valence 0.30 vs your 0.20 (+2.70) |
|   |                    |              |       | mood match: sad (+2.00)           |
+---+--------------------+--------------+-------+-----------------------------------+
| 5 | Gone Too Soon      | hip hop      | 7.20  | energy 0.45 vs your 0.90 (+2.20)  |
|   | by Kay Mellow      | sad          |       | valence 0.20 vs your 0.20 (+3.00) |
|   |                    |              |       | mood match: sad (+2.00)           |
+---+--------------------+--------------+-------+-----------------------------------+
```

</details>
<details>
<summary><b>Edge: acoustic metalhead</b></summary>

```
Profile: Edge: acoustic metalhead   (mode: balanced)
  favorite_genre=metal, favorite_mood=angry, target_energy=0.95, likes_acoustic=True
+---+--------------------+--------------+-------+----------------------------------+
| # | Song               | Genre / Mood | Score | Why                              |
+---+--------------------+--------------+-------+----------------------------------+
| 1 | Breaking Point     | metal        | 7.48  | energy 0.96 vs your 0.95 (+3.96) |
|   | by Ironclad        | angry        |       | mood match: angry (+2.00)        |
|   |                    |              |       | genre match: metal (+1.50)       |
|   |                    |              |       | acoustic fit (+0.02)             |
+---+--------------------+--------------+-------+----------------------------------+
| 2 | Granite Throne     | metal        | 7.47  | energy 0.94 vs your 0.95 (+3.96) |
|   | by Stone Legion    | angry        |       | mood match: angry (+2.00)        |
|   |                    |              |       | genre match: metal (+1.50)       |
|   |                    |              |       | acoustic fit (+0.01)             |
+---+--------------------+--------------+-------+----------------------------------+
| 3 | No More Lies       | rock         | 5.88  | energy 0.90 vs your 0.95 (+3.80) |
|   | by The Static Kids | angry        |       | mood match: angry (+2.00)        |
|   |                    |              |       | acoustic fit (+0.08)             |
+---+--------------------+--------------+-------+----------------------------------+
| 4 | Ashes Fall         | metal        | 4.95  | energy 0.80 vs your 0.95 (+3.40) |
|   | by Ironclad        | sad          |       | genre match: metal (+1.50)       |
|   |                    |              |       | acoustic fit (+0.05)             |
+---+--------------------+--------------+-------+----------------------------------+
| 5 | Stomp and Holler   | country      | 4.12  | energy 0.80 vs your 0.95 (+3.40) |
|   | by Barn Fire       | energetic    |       | acoustic fit (+0.72)             |
+---+--------------------+--------------+-------+----------------------------------+
```

</details>
<details>
<summary><b>Edge: genre not in catalog</b></summary>

```
Profile: Edge: genre not in catalog   (mode: balanced)
  favorite_genre=k-pop, favorite_mood=happy, target_energy=0.75
+---+------------------+--------------+-------+----------------------------------+
| # | Song             | Genre / Mood | Score | Why                              |
+---+------------------+--------------+-------+----------------------------------+
| 1 | Rooftop Lights   | indie pop    | 5.96  | energy 0.76 vs your 0.75 (+3.96) |
|   | by Indigo Parade | happy        |       | mood match: happy (+2.00)        |
+---+------------------+--------------+-------+----------------------------------+
| 2 | Island Bounce    | dancehall    | 5.96  | energy 0.74 vs your 0.75 (+3.96) |
|   | by Yard Vibes    | happy        |       | mood match: happy (+2.00)        |
+---+------------------+--------------+-------+----------------------------------+
| 3 | Lagos Sunset     | afrobeats    | 5.88  | energy 0.72 vs your 0.75 (+3.88) |
|   | by Ayo Rhythm    | happy        |       | mood match: happy (+2.00)        |
+---+------------------+--------------+-------+----------------------------------+
| 4 | Open Highway     | rock         | 5.80  | energy 0.80 vs your 0.75 (+3.80) |
|   | by Steel Avenue  | happy        |       | mood match: happy (+2.00)        |
+---+------------------+--------------+-------+----------------------------------+
| 5 | Sunrise City     | pop          | 5.72  | energy 0.82 vs your 0.75 (+3.72) |
|   | by Neon Echo     | happy        |       | mood match: happy (+2.00)        |
+---+------------------+--------------+-------+----------------------------------+
```

</details>
<details>
<summary><b>Edge: capital letters</b></summary>

```
Profile: Edge: capital letters   (mode: balanced)
  favorite_genre=Hip Hop, favorite_mood=Chill, target_energy=0.35
+---+--------------------+--------------+-------+----------------------------------+
| # | Song               | Genre / Mood | Score | Why                              |
+---+--------------------+--------------+-------+----------------------------------+
| 1 | Late Night Verses  | hip hop      | 7.38  | energy 0.38 vs your 0.35 (+3.88) |
|   | by Kay Mellow      | chill        |       | mood match: chill (+2.00)        |
|   |                    |              |       | genre match: hip hop (+1.50)     |
+---+--------------------+--------------+-------+----------------------------------+
| 2 | Library Rain       | lofi         | 6.00  | energy 0.35 vs your 0.35 (+4.00) |
|   | by Paper Lanterns  | chill        |       | mood match: chill (+2.00)        |
+---+--------------------+--------------+-------+----------------------------------+
| 3 | Sunday Sheets      | pop          | 5.80  | energy 0.40 vs your 0.35 (+3.80) |
|   | by Mira Vale       | chill        |       | mood match: chill (+2.00)        |
+---+--------------------+--------------+-------+----------------------------------+
| 4 | Spacewalk Thoughts | ambient      | 5.72  | energy 0.28 vs your 0.35 (+3.72) |
|   | by Orbit Bloom     | chill        |       | mood match: chill (+2.00)        |
+---+--------------------+--------------+-------+----------------------------------+
| 5 | Midnight Coding    | lofi         | 5.72  | energy 0.42 vs your 0.35 (+3.72) |
|   | by LoRoom          | chill        |       | mood match: chill (+2.00)        |
+---+--------------------+--------------+-------+----------------------------------+
```

</details>
<details>
<summary><b>Afrobeats Night Out (advanced)</b></summary>

```
Profile: Afrobeats Night Out (advanced)   (mode: balanced)
  favorite_genre=afrobeats, favorite_mood=energetic, target_energy=0.8, target_valence=0.85,
  likes_acoustic=False, favorite_tags=['euphoric', 'playful'], preferred_decade=2020,
  target_popularity=80, target_speechiness=0.1, target_instrumentalness=0.0
+---+-------------------+--------------+-------+--------------------------------------------+
| # | Song              | Genre / Mood | Score | Why                                        |
+---+-------------------+--------------+-------+--------------------------------------------+
| 1 | Owambe Party      | afrobeats    | 17.04 | energy 0.86 vs your 0.80 (+3.76)           |
|   | by Ayo Rhythm     | energetic    |       | valence 0.88 vs your 0.85 (+2.91)          |
|   |                   |              |       | mood match: energetic (+2.00)              |
|   |                   |              |       | genre match: afrobeats (+1.50)             |
|   |                   |              |       | not acoustic fit (+0.88)                   |
|   |                   |              |       | mood tags: euphoric / playful (+1.50)      |
|   |                   |              |       | from the 2020s (+1.00)                     |
|   |                   |              |       | popularity 81 vs your 80 (+0.99)           |
|   |                   |              |       | rap/spoken words 0.10 vs your 0.10 (+1.50) |
|   |                   |              |       | instrumental 0.00 vs your 0.00 (+1.00)     |
+---+-------------------+--------------+-------+--------------------------------------------+
| 2 | Perreo Hasta Ya   | reggaeton    | 15.30 | energy 0.85 vs your 0.80 (+3.80)           |
|   | by Fuego Sur      | energetic    |       | valence 0.80 vs your 0.85 (+2.85)          |
|   |                   |              |       | mood match: energetic (+2.00)              |
|   |                   |              |       | not acoustic fit (+0.88)                   |
|   |                   |              |       | mood tags: euphoric / playful (+1.50)      |
|   |                   |              |       | from the 2020s (+1.00)                     |
|   |                   |              |       | popularity 88 vs your 80 (+0.92)           |
|   |                   |              |       | rap/spoken words 0.14 vs your 0.10 (+1.35) |
|   |                   |              |       | instrumental 0.00 vs your 0.00 (+1.00)     |
+---+-------------------+--------------+-------+--------------------------------------------+
| 3 | Lagos Sunset      | afrobeats    | 14.86 | energy 0.72 vs your 0.80 (+3.68)           |
|   | by Ayo Rhythm     | happy        |       | valence 0.86 vs your 0.85 (+2.97)          |
|   |                   |              |       | genre match: afrobeats (+1.50)             |
|   |                   |              |       | not acoustic fit (+0.80)                   |
|   |                   |              |       | mood tags: euphoric / playful (+1.50)      |
|   |                   |              |       | from the 2020s (+1.00)                     |
|   |                   |              |       | popularity 85 vs your 80 (+0.95)           |
|   |                   |              |       | rap/spoken words 0.09 vs your 0.10 (+1.46) |
|   |                   |              |       | instrumental 0.00 vs your 0.00 (+1.00)     |
+---+-------------------+--------------+-------+--------------------------------------------+
| 4 | Rush Hour Rollers | liquid dnb   | 13.56 | energy 0.88 vs your 0.80 (+3.68)           |
|   | by Bass Theory    | energetic    |       | valence 0.72 vs your 0.85 (+2.61)          |
|   |                   |              |       | mood match: energetic (+2.00)              |
|   |                   |              |       | not acoustic fit (+0.95)                   |
|   |                   |              |       | mood tags: euphoric (+0.75)                |
|   |                   |              |       | from the 2020s (+1.00)                     |
|   |                   |              |       | popularity 51 vs your 80 (+0.71)           |
|   |                   |              |       | rap/spoken words 0.05 vs your 0.10 (+1.31) |
|   |                   |              |       | instrumental 0.45 vs your 0.00 (+0.55)     |
+---+-------------------+--------------+-------+--------------------------------------------+
| 5 | Stomp and Holler  | country      | 12.91 | energy 0.80 vs your 0.80 (+4.00)           |
|   | by Barn Fire      | energetic    |       | valence 0.78 vs your 0.85 (+2.79)          |
|   |                   |              |       | mood match: energetic (+2.00)              |
|   |                   |              |       | not acoustic fit (+0.28)                   |
|   |                   |              |       | mood tags: playful (+0.75)                 |
|   |                   |              |       | popularity 57 vs your 80 (+0.77)           |
|   |                   |              |       | rap/spoken words 0.06 vs your 0.10 (+1.35) |
|   |                   |              |       | instrumental 0.03 vs your 0.00 (+0.97)     |
+---+-------------------+--------------+-------+--------------------------------------------+
```

</details>

**Extra runs for the extensions:**

<details>
<summary><b>Deep Intense Rock (genre-first mode)</b></summary>

```
Profile: Deep Intense Rock   (mode: genre-first)
  favorite_genre=rock, favorite_mood=intense, target_energy=0.9, target_valence=0.4,
  likes_acoustic=False
+---+--------------------+--------------+-------+-----------------------------------+
| # | Song               | Genre / Mood | Score | Why                               |
+---+--------------------+--------------+-------+-----------------------------------+
| 1 | Storm Runner       | rock         | 10.76 | energy 0.91 vs your 0.90 (+1.98)  |
|   | by Voltline        | intense      |       | valence 0.48 vs your 0.40 (+1.38) |
|   |                    |              |       | mood match: intense (+1.50)       |
|   |                    |              |       | genre match: rock (+5.00)         |
|   |                    |              |       | not acoustic fit (+0.90)          |
+---+--------------------+--------------+-------+-----------------------------------+
| 2 | No More Lies       | rock         | 9.27  | energy 0.90 vs your 0.90 (+2.00)  |
|   | by The Static Kids | angry        |       | valence 0.30 vs your 0.40 (+1.35) |
|   |                    |              |       | genre match: rock (+5.00)         |
|   |                    |              |       | not acoustic fit (+0.92)          |
+---+--------------------+--------------+-------+-----------------------------------+
| 3 | Open Highway       | rock         | 8.53  | energy 0.80 vs your 0.90 (+1.80)  |
|   | by Steel Avenue    | happy        |       | valence 0.75 vs your 0.40 (+0.98) |
|   |                    |              |       | genre match: rock (+5.00)         |
|   |                    |              |       | not acoustic fit (+0.75)          |
+---+--------------------+--------------+-------+-----------------------------------+
| 4 | Paper Walls        | rock         | 8.25  | energy 0.55 vs your 0.90 (+1.30)  |
|   | by The Static Kids | sad          |       | valence 0.30 vs your 0.40 (+1.35) |
|   |                    |              |       | genre match: rock (+5.00)         |
|   |                    |              |       | not acoustic fit (+0.60)          |
+---+--------------------+--------------+-------+-----------------------------------+
| 5 | Back Block         | drill        | 5.77  | energy 0.85 vs your 0.90 (+1.90)  |
|   | by Grime Unit      | intense      |       | valence 0.35 vs your 0.40 (+1.42) |
|   |                    |              |       | mood match: intense (+1.50)       |
|   |                    |              |       | not acoustic fit (+0.95)          |
+---+--------------------+--------------+-------+-----------------------------------+
```

</details>
<details>
<summary><b>Deep Intense Rock (genre-first mode + diverse)</b></summary>

```
Profile: Deep Intense Rock   (mode: genre-first, diverse)
  favorite_genre=rock, favorite_mood=intense, target_energy=0.9, target_valence=0.4,
  likes_acoustic=False
+---+--------------------+--------------+-------+--------------------------------------+
| # | Song               | Genre / Mood | Score | Why                                  |
+---+--------------------+--------------+-------+--------------------------------------+
| 1 | Storm Runner       | rock         | 10.76 | energy 0.91 vs your 0.90 (+1.98)     |
|   | by Voltline        | intense      |       | valence 0.48 vs your 0.40 (+1.38)    |
|   |                    |              |       | mood match: intense (+1.50)          |
|   |                    |              |       | genre match: rock (+5.00)            |
|   |                    |              |       | not acoustic fit (+0.90)             |
+---+--------------------+--------------+-------+--------------------------------------+
| 2 | No More Lies       | rock         | 9.27  | energy 0.90 vs your 0.90 (+2.00)     |
|   | by The Static Kids | angry        |       | valence 0.30 vs your 0.40 (+1.35)    |
|   |                    |              |       | genre match: rock (+5.00)            |
|   |                    |              |       | not acoustic fit (+0.92)             |
+---+--------------------+--------------+-------+--------------------------------------+
| 3 | Open Highway       | rock         | 7.53  | energy 0.80 vs your 0.90 (+1.80)     |
|   | by Steel Avenue    | happy        |       | valence 0.75 vs your 0.40 (+0.98)    |
|   |                    |              |       | genre match: rock (+5.00)            |
|   |                    |              |       | not acoustic fit (+0.75)             |
|   |                    |              |       | already 2 rock songs in list (-1.00) |
+---+--------------------+--------------+-------+--------------------------------------+
| 4 | Back Block         | drill        | 5.77  | energy 0.85 vs your 0.90 (+1.90)     |
|   | by Grime Unit      | intense      |       | valence 0.35 vs your 0.40 (+1.42)    |
|   |                    |              |       | mood match: intense (+1.50)          |
|   |                    |              |       | not acoustic fit (+0.95)             |
+---+--------------------+--------------+-------+--------------------------------------+
| 5 | Bad Mind           | dancehall    | 5.67  | energy 0.88 vs your 0.90 (+1.96)     |
|   | by Rudie King      | intense      |       | valence 0.55 vs your 0.40 (+1.27)    |
|   |                    |              |       | mood match: intense (+1.50)          |
|   |                    |              |       | not acoustic fit (+0.94)             |
+---+--------------------+--------------+-------+--------------------------------------+
```

</details>
<details>
<summary><b>Edge: acoustic metalhead (diverse)</b></summary>

```
Profile: Edge: acoustic metalhead   (mode: balanced, diverse)
  favorite_genre=metal, favorite_mood=angry, target_energy=0.95, likes_acoustic=True
+---+--------------------+--------------+-------+----------------------------------+
| # | Song               | Genre / Mood | Score | Why                              |
+---+--------------------+--------------+-------+----------------------------------+
| 1 | Breaking Point     | metal        | 7.48  | energy 0.96 vs your 0.95 (+3.96) |
|   | by Ironclad        | angry        |       | mood match: angry (+2.00)        |
|   |                    |              |       | genre match: metal (+1.50)       |
|   |                    |              |       | acoustic fit (+0.02)             |
+---+--------------------+--------------+-------+----------------------------------+
| 2 | Granite Throne     | metal        | 7.47  | energy 0.94 vs your 0.95 (+3.96) |
|   | by Stone Legion    | angry        |       | mood match: angry (+2.00)        |
|   |                    |              |       | genre match: metal (+1.50)       |
|   |                    |              |       | acoustic fit (+0.01)             |
+---+--------------------+--------------+-------+----------------------------------+
| 3 | No More Lies       | rock         | 5.88  | energy 0.90 vs your 0.95 (+3.80) |
|   | by The Static Kids | angry        |       | mood match: angry (+2.00)        |
|   |                    |              |       | acoustic fit (+0.08)             |
+---+--------------------+--------------+-------+----------------------------------+
| 4 | Stomp and Holler   | country      | 4.12  | energy 0.80 vs your 0.95 (+3.40) |
|   | by Barn Fire       | energetic    |       | acoustic fit (+0.72)             |
+---+--------------------+--------------+-------+----------------------------------+
| 5 | Swing Shift        | jazz         | 4.02  | energy 0.78 vs your 0.95 (+3.32) |
|   | by Brass Alley     | energetic    |       | acoustic fit (+0.70)             |
+---+--------------------+--------------+-------+----------------------------------+
```

</details>


---

## 8. Future Work  

1. **Make the text matching smarter.** I already fixed capital letters. Next I'd handle different spellings ("hip-hop", "R&B" vs "r and b") and group similar genres into families, so "hip hop" and "drill" or "pop" and "indie pop" get partial credit.
2. **Learn the weights instead of guessing them.** Right now I picked the points by hand. A real app would learn them from what people skip, replay, and save, and mix in collaborative filtering ("people like you also liked") so it can surprise you.
3. **Make the acoustic setting a number instead of yes or no,** and give it more weight. Right now it's too weak to matter.

---

## 9. Personal Reflection  

**Biggest learning moment:** I learned that every weight I pick is really a choice about whose taste matters. Putting energy first worked great for me, because I listen by vibe. But when I tested a rock fan, they got drill and dancehall songs. My own preference was built into the system, and it made it worse for a different kind of listener. That's when I understood why real apps can't just pick one rule for everyone.

**How AI helped, and when I double-checked it:** AI helped me research how Spotify and YouTube work, make 52 new songs, write the code, and run experiments fast. But I had to check its work. The song numbers are AI guesses, so I had to think about whether they matched how those genres actually feel to me. The README described a `target_valence` setting before the code had it, so the docs and the code had to be matched up. AI also wrote some sentences in my voice, like saying the results "feel right," so I had to make sure they were actually true for me.

**What surprised me:** It's just adding up points, a few small math steps per song, but the results really feel like recommendations. Seeing the reasons next to each song makes it feel smart. I was also surprised how much the mood rule mattered. When I turned it off, a workout song showed up for a happy pop fan.

**What I'd try next:** I'd add fake listening history (likes and skips) for a few users and try collaborative filtering. Then I'd mix it with my vibe score, so the system can recommend songs I'd never think to ask for.
