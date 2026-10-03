# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

**The biggest weakness I found: genre counts so little that genre fans get songs from other genres.** I gave genre only 1.5 points on purpose, because I think energy is what makes a vibe. But when I tested a "Deep Intense Rock" fan, only 2 of the top 5 songs were rock. Drill, dancehall, and hip hop took spots 2, 3, and 4, even though there are 4 rock songs in the catalog. Those songs just had the right energy and the "intense" mood, and that was enough to beat a genre match. This works for someone like me who cares about the vibe, but a person who only listens to rock would feel like the app isn't listening to them.

Other problems I found:

- **Capital letters break matching.** If someone types "Hip Hop" instead of "hip hop", the genre and mood checks fail without any warning. The system falls back on energy only, and a sad country song (*Whiskey Letters*) tied for #1 for a chill hip hop fan.
- **The acoustic preference barely matters.** It's only worth up to 1 point. When I tested an "acoustic metalhead", the system ignored the acoustic part and gave them electric metal songs that are almost 0% acoustic.
- **Genres that aren't in the catalog fail quietly.** A k-pop fan gets happy songs from other genres. That's not bad, but the system never tells them there's no k-pop.
- **Some moods have way more songs.** There are 14 sad songs but only 3 romantic and 3 angry ones, so sad listeners get much better choices.
- **Filter bubble.** The system only finds songs close to what you already said you like. It will never surprise you with something different that you'd end up loving.

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
| Edge: capital letters | "Hip Hop", "Chill", energy 0.35 | Library Rain (lofi) and Whiskey Letters (country), tied |

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
- **Chill Hip Hop vs Capital letters:** These ask for the same thing, but typing "Hip Hop" with capitals made the genre and mood checks fail. *Late Night Verses* dropped from #1 to #4, and a sad country song tied for first. That one surprised me the most.
- **Acoustic metalhead vs Deep Intense Rock:** Both get loud, high-energy songs. The "likes acoustic" setting barely changed anything, because it's worth so few points.

### Why does *Gym Hero* show up for "Happy Pop" fans?

In my normal system it doesn't. But when I turned off the mood rule as an experiment, *Gym Hero* jumped to #2 for the High-Energy Pop fan. Here's why, in plain words: *Gym Hero* is a pop song with high energy and a fairly happy sound, so it scores well on genre, energy, and valence. The only thing wrong with it is that it's an *intense* workout song, not a *happy* one. Without the mood rule, the system can't see that difference, so it thinks *Gym Hero* is almost perfect. The mood rule is what keeps it out.

### Experiments I ran

1. **Weight shift (energy doubled to 8.0, genre cut in half to 0.75):** Mostly the same songs came back, just in a slightly different order. It made results **different, not more accurate**. For the "high energy but sad" profile it got worse: sad metal beat the sad pop song, and angry metal songs (not sad ones) got into the top 5.
2. **Turning off the mood rule:** This made things clearly **worse**. Hype songs like *Gym Hero* showed up for happy listeners, and sad and intense songs (*Gone Too Soon*, *Crown Up*) got into my chill hip hop list. Mood is doing a lot of important work.

### Full output for every profile

<details>
<summary><b>High-Energy Pop</b></summary>

```
============================================================
Profile: High-Energy Pop
  favorite_genre=pop, favorite_mood=happy, target_energy=0.85, target_valence=0.8, likes_acoustic=False
============================================================
1. Sunrise City by Neon Echo  (pop, happy)
   Score: 11.08
   - energy 0.82 vs your 0.85 (+3.88)
   - valence 0.84 vs your 0.80 (+2.88)
   - mood match: happy (+2.0)
   - genre match: pop (+1.5)
   - not acoustic fit (+0.82)

2. Calor Total by Fuego Sur  (reggaeton, happy)
   Score: 9.54
   - energy 0.82 vs your 0.85 (+3.88)
   - valence 0.88 vs your 0.80 (+2.76)
   - mood match: happy (+2.0)
   - not acoustic fit (+0.90)

3. Open Highway by Steel Avenue  (rock, happy)
   Score: 9.40
   - energy 0.80 vs your 0.85 (+3.80)
   - valence 0.75 vs your 0.80 (+2.85)
   - mood match: happy (+2.0)
   - not acoustic fit (+0.75)

4. Island Bounce by Yard Vibes  (dancehall, happy)
   Score: 9.37
   - energy 0.74 vs your 0.85 (+3.56)
   - valence 0.83 vs your 0.80 (+2.91)
   - mood match: happy (+2.0)
   - not acoustic fit (+0.90)

5. Rooftop Lights by Indigo Parade  (indie pop, happy)
   Score: 9.26
   - energy 0.76 vs your 0.85 (+3.64)
   - valence 0.81 vs your 0.80 (+2.97)
   - mood match: happy (+2.0)
   - not acoustic fit (+0.65)
```

</details>
<details>
<summary><b>Chill Lofi</b></summary>

```
============================================================
Profile: Chill Lofi
  favorite_genre=lofi, favorite_mood=chill, target_energy=0.35, likes_acoustic=True
============================================================
1. Library Rain by Paper Lanterns  (lofi, chill)
   Score: 8.36
   - energy 0.35 vs your 0.35 (+4.00)
   - mood match: chill (+2.0)
   - genre match: lofi (+1.5)
   - acoustic fit (+0.86)

2. Midnight Coding by LoRoom  (lofi, chill)
   Score: 7.93
   - energy 0.42 vs your 0.35 (+3.72)
   - mood match: chill (+2.0)
   - genre match: lofi (+1.5)
   - acoustic fit (+0.71)

3. Spacewalk Thoughts by Orbit Bloom  (ambient, chill)
   Score: 6.64
   - energy 0.28 vs your 0.35 (+3.72)
   - mood match: chill (+2.0)
   - acoustic fit (+0.92)

4. Sunday Sheets by Mira Vale  (pop, chill)
   Score: 6.20
   - energy 0.40 vs your 0.35 (+3.80)
   - mood match: chill (+2.0)
   - acoustic fit (+0.40)

5. Late Night Verses by Kay Mellow  (hip hop, chill)
   Score: 6.18
   - energy 0.38 vs your 0.35 (+3.88)
   - mood match: chill (+2.0)
   - acoustic fit (+0.30)
```

</details>
<details>
<summary><b>Deep Intense Rock</b></summary>

```
============================================================
Profile: Deep Intense Rock
  favorite_genre=rock, favorite_mood=intense, target_energy=0.9, target_valence=0.4, likes_acoustic=False
============================================================
1. Storm Runner by Voltline  (rock, intense)
   Score: 11.12
   - energy 0.91 vs your 0.90 (+3.96)
   - valence 0.48 vs your 0.40 (+2.76)
   - mood match: intense (+2.0)
   - genre match: rock (+1.5)
   - not acoustic fit (+0.90)

2. Back Block by Grime Unit  (drill, intense)
   Score: 9.60
   - energy 0.85 vs your 0.90 (+3.80)
   - valence 0.35 vs your 0.40 (+2.85)
   - mood match: intense (+2.0)
   - not acoustic fit (+0.95)

3. Bad Mind by Rudie King  (dancehall, intense)
   Score: 9.41
   - energy 0.88 vs your 0.90 (+3.92)
   - valence 0.55 vs your 0.40 (+2.55)
   - mood match: intense (+2.0)
   - not acoustic fit (+0.94)

4. Crown Up by Blaze Carter  (hip hop, intense)
   Score: 9.20
   - energy 0.88 vs your 0.90 (+3.92)
   - valence 0.62 vs your 0.40 (+2.34)
   - mood match: intense (+2.0)
   - not acoustic fit (+0.94)

5. No More Lies by The Static Kids  (rock, angry)
   Score: 9.12
   - energy 0.90 vs your 0.90 (+4.00)
   - valence 0.30 vs your 0.40 (+2.70)
   - genre match: rock (+1.5)
   - not acoustic fit (+0.92)
```

</details>
<details>
<summary><b>Chill Hip Hop (mine)</b></summary>

```
============================================================
Profile: Chill Hip Hop (mine)
  favorite_genre=hip hop, favorite_mood=chill, target_energy=0.35, target_valence=0.5, likes_acoustic=False
============================================================
1. Late Night Verses by Kay Mellow  (hip hop, chill)
   Score: 11.02
   - energy 0.38 vs your 0.35 (+3.88)
   - valence 0.52 vs your 0.50 (+2.94)
   - mood match: chill (+2.0)
   - genre match: hip hop (+1.5)
   - not acoustic fit (+0.70)

2. Sunday Sheets by Mira Vale  (pop, chill)
   Score: 8.95
   - energy 0.40 vs your 0.35 (+3.80)
   - valence 0.65 vs your 0.50 (+2.55)
   - mood match: chill (+2.0)
   - not acoustic fit (+0.60)

3. Drift Current by Glass Harbor  (liquid dnb, chill)
   Score: 8.90
   - energy 0.50 vs your 0.35 (+3.40)
   - valence 0.60 vs your 0.50 (+2.70)
   - mood match: chill (+2.0)
   - not acoustic fit (+0.80)

4. Library Rain by Paper Lanterns  (lofi, chill)
   Score: 8.84
   - energy 0.35 vs your 0.35 (+4.00)
   - valence 0.60 vs your 0.50 (+2.70)
   - mood match: chill (+2.0)
   - not acoustic fit (+0.14)

5. Midnight Coding by LoRoom  (lofi, chill)
   Score: 8.83
   - energy 0.42 vs your 0.35 (+3.72)
   - valence 0.56 vs your 0.50 (+2.82)
   - mood match: chill (+2.0)
   - not acoustic fit (+0.29)
```

</details>
<details>
<summary><b>Edge: high energy but sad</b></summary>

```
============================================================
Profile: Edge: high energy but sad
  favorite_genre=pop, favorite_mood=sad, target_energy=0.9, target_valence=0.2
============================================================
1. Dancing Alone by Mira Vale  (pop, sad)
   Score: 9.40
   - energy 0.70 vs your 0.90 (+3.20)
   - valence 0.30 vs your 0.20 (+2.70)
   - mood match: sad (+2.0)
   - genre match: pop (+1.5)

2. Ashes Fall by Ironclad  (metal, sad)
   Score: 8.45
   - energy 0.80 vs your 0.90 (+3.60)
   - valence 0.15 vs your 0.20 (+2.85)
   - mood match: sad (+2.0)

3. Quiet Before by South Ends  (drill, sad)
   Score: 7.60
   - energy 0.55 vs your 0.90 (+2.60)
   - valence 0.20 vs your 0.20 (+3.00)
   - mood match: sad (+2.0)

4. Paper Walls by The Static Kids  (rock, sad)
   Score: 7.30
   - energy 0.55 vs your 0.90 (+2.60)
   - valence 0.30 vs your 0.20 (+2.70)
   - mood match: sad (+2.0)

5. Gone Too Soon by Kay Mellow  (hip hop, sad)
   Score: 7.20
   - energy 0.45 vs your 0.90 (+2.20)
   - valence 0.20 vs your 0.20 (+3.00)
   - mood match: sad (+2.0)
```

</details>
<details>
<summary><b>Edge: acoustic metalhead</b></summary>

```
============================================================
Profile: Edge: acoustic metalhead
  favorite_genre=metal, favorite_mood=angry, target_energy=0.95, likes_acoustic=True
============================================================
1. Breaking Point by Ironclad  (metal, angry)
   Score: 7.48
   - energy 0.96 vs your 0.95 (+3.96)
   - mood match: angry (+2.0)
   - genre match: metal (+1.5)
   - acoustic fit (+0.02)

2. Granite Throne by Stone Legion  (metal, angry)
   Score: 7.47
   - energy 0.94 vs your 0.95 (+3.96)
   - mood match: angry (+2.0)
   - genre match: metal (+1.5)
   - acoustic fit (+0.01)

3. No More Lies by The Static Kids  (rock, angry)
   Score: 5.88
   - energy 0.90 vs your 0.95 (+3.80)
   - mood match: angry (+2.0)
   - acoustic fit (+0.08)

4. Ashes Fall by Ironclad  (metal, sad)
   Score: 4.95
   - energy 0.80 vs your 0.95 (+3.40)
   - genre match: metal (+1.5)
   - acoustic fit (+0.05)

5. Stomp and Holler by Barn Fire  (country, energetic)
   Score: 4.12
   - energy 0.80 vs your 0.95 (+3.40)
   - acoustic fit (+0.72)
```

</details>
<details>
<summary><b>Edge: genre not in catalog</b></summary>

```
============================================================
Profile: Edge: genre not in catalog
  favorite_genre=k-pop, favorite_mood=happy, target_energy=0.75
============================================================
1. Rooftop Lights by Indigo Parade  (indie pop, happy)
   Score: 5.96
   - energy 0.76 vs your 0.75 (+3.96)
   - mood match: happy (+2.0)

2. Island Bounce by Yard Vibes  (dancehall, happy)
   Score: 5.96
   - energy 0.74 vs your 0.75 (+3.96)
   - mood match: happy (+2.0)

3. Lagos Sunset by Ayo Rhythm  (afrobeats, happy)
   Score: 5.88
   - energy 0.72 vs your 0.75 (+3.88)
   - mood match: happy (+2.0)

4. Open Highway by Steel Avenue  (rock, happy)
   Score: 5.80
   - energy 0.80 vs your 0.75 (+3.80)
   - mood match: happy (+2.0)

5. Sunrise City by Neon Echo  (pop, happy)
   Score: 5.72
   - energy 0.82 vs your 0.75 (+3.72)
   - mood match: happy (+2.0)
```

</details>
<details>
<summary><b>Edge: capital letters</b></summary>

```
============================================================
Profile: Edge: capital letters
  favorite_genre=Hip Hop, favorite_mood=Chill, target_energy=0.35
============================================================
1. Library Rain by Paper Lanterns  (lofi, chill)
   Score: 4.00
   - energy 0.35 vs your 0.35 (+4.00)

2. Whiskey Letters by Cass Holloway  (country, sad)
   Score: 4.00
   - energy 0.35 vs your 0.35 (+4.00)

3. Coffee Shop Stories by Slow Stereo  (jazz, relaxed)
   Score: 3.92
   - energy 0.37 vs your 0.35 (+3.92)

4. Late Night Verses by Kay Mellow  (hip hop, chill)
   Score: 3.88
   - energy 0.38 vs your 0.35 (+3.88)

5. Slow Motion Love by Nia Soul  (r&b, romantic)
   Score: 3.88
   - energy 0.38 vs your 0.35 (+3.88)
```

</details>

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
