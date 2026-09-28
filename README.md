# AI Cricket Commentator

A retrieval-augmented (RAG) AI commentator that narrates a T20 cricket match ball by ball, using an LLM grounded in match context that grows live as the game unfolds.

Built around a fictional 2026 T20 World Cup final (India vs. New Zealand) using a real ball-by-ball data file, but the pipeline works for any match in the same format.

## Why I built this

During the real India vs. New Zealand T20 World Cup final, Ravi Shastri called the winning moment live on air — and for one second, said the ninth wicket had fallen instead of the tenth. He corrected himself immediately, but it stuck with me: even the best commentator in the world can lose track of the count in the adrenaline of the moment.

That made me want to see whether an AI, given the same ball-by-ball data and enough context about everything that came before it, would get it right. This project is the result — full write-up here: [I Vibe Coded an AI to Commentate the Moment Ravi Shastri Almost Missed](https://medium.com/@avinashviji16/i-vibe-coded-an-ai-to-commentate-the-moment-ravi-shastri-almost-missed-6fca37d7789d).

## How it works

```
knowledge_base.py  --static facts (pre-match + 1st innings)-->  rag_engine.py
                                                                       |
                                                          FAISS semantic search
                                                                       |
cricket_simulator.py --ball-by-ball JSON--> event + match state ------+
                                                                       |
                                                          retrieved context
                                                                       v
                                                        commentary_generator.py
                                                                       |
                                                               OpenAI API call
                                                                       v
                                                              live commentary
```

**Static memory** — [knowledge_base.py](cric-rag/knowledge_base.py) holds 69 hand-written facts about the tournament, venue, and first-innings play: what an AI commentator would already know walking into the second innings.

**Dynamic memory** — as the second innings is simulated, [rag_engine.py](cric-rag/rag_engine.py)'s FAISS index grows in real time: every wicket and boundary is embedded and added, so later commentary can reference things that "just happened" a few overs ago.

**Selective retrieval** — not every ball triggers a RAG lookup. Only wickets, boundaries, new batters, and the first ball of each over pull context; routine dot balls and singles skip retrieval entirely, keeping the commentary relevant and the API usage down.

**Episodic memory** — the last 6 lines of generated commentary are fed back into every prompt so the narration builds on itself instead of repeating facts or restating the score.

**Golden moment** — the final wicket of the innings gets a dedicated prompt path: full context, present tense, "let it breathe" instructions instead of the terse 1–2 sentence routine-ball format.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
```

## Run

```bash
cd cric-rag
python cricket_simulator.py
```

Overs 0–15 only generate commentary for wickets and boundaries; overs 16+ narrate every ball, mirroring how a broadcast tightens up during a run chase.

## Example output (illustrative)

```
[BOUNDARY] Over 3.4 | Lockie Ferguson to Tim Seifert
SIX | Score: 28/0 | Need: 228 off 106 balls
Commentary:
Seifert gets under it and it's gone -- over deep midwicket for six! Ferguson
under pressure early, and Seifert is looking to make this powerplay count.
----------------------------------------------------------------------

[WICKET] Over 16.2 | Jasprit Bumrah to Daryl Mitchell
WICKET (bowled) | Score: 189/6 | Need: 67 off 22 balls
Commentary:
Bumrah again! That yorker was unplayable -- Mitchell had no answer, and India
smell the finish line now with New Zealand's big-match man back in the hut.
----------------------------------------------------------------------
```

## Tech

- Python
- FAISS (`IndexFlatL2`) for semantic retrieval
- `sentence-transformers` (`all-MiniLM-L6-v2`) for embeddings
- OpenAI API for commentary generation

## Data

`cric-rag/1512773.json` is real ball-by-ball data in Cricsheet format; the surrounding match context (teams, target, tournament stakes) is fictional scenario-setting written for this project.
