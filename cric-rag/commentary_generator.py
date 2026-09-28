# commentary_generator.py
# AI Cricket Commentator -- prompt builder + OpenAI API
# Features:
#   - Energetic commentator persona (no specific person)
#   - Commentary history (episodic memory -- last 6 balls)
#   - Retrieved context (semantic memory -- FAISS facts)
#   - Golden moment -- real situation, LLM figures it out

import os

from openai import OpenAI, OpenAIError

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Export it before running, e.g.\n"
        "  export OPENAI_API_KEY=sk-..."
    )

client = OpenAI()  # reads OPENAI_API_KEY from environment

COMMENTATOR_PERSONA = """You are a live cricket commentator at a T20 World Cup Final.
Your style:
- Energetic, passionate, and vivid
- Build tension naturally across deliveries
- Celebrate big moments with full intensity
- Reference player history and match context naturally when relevant
- Speak in the present tense -- this is happening RIGHT NOW
- You don't repeat what you have already said -- you build on it
"""

def build_prompt(state: dict, delivery: dict, event: str,
                 retrieved_context: list[str],
                 commentary_history: list[str],
                 is_golden: bool) -> str:

    batter      = delivery["batter"]
    bowler      = delivery["bowler"]
    runs_needed = state["runs_needed"]
    balls_left  = 120 - state["legal_balls"]

    # -- EPISODIC MEMORY BLOCK -------------------------------------------------
    if commentary_history:
        history_text  = "\n".join(f"  {line}" for line in commentary_history)
        history_block = f"""
=== LAST {len(commentary_history)} BALLS (your recent commentary) ===
{history_text}

Build naturally on this narrative. Do not repeat facts or phrases already used above.
"""
    else:
        history_block = ""

    # -- CONTEXT BLOCK ---------------------------------------------------------
    if retrieved_context:
        context_text  = "\n".join(f"- {fact}" for fact in retrieved_context)
        context_block = f"""
=== RETRIEVED CONTEXT ===
{context_text}
"""
    else:
        context_block = ""

    # -- GOLDEN MOMENT ---------------------------------------------------------
    if is_golden:
        win_by = state["target"] - state["total_runs"] - 1
        return f"""{COMMENTATOR_PERSONA}
{history_block}
=== MATCH SITUATION ===
Batting: {state['batting_team']} | Bowling: {state['bowling_team']}
Score: {state['score']} | Over: {state['over']}.{state['ball']}
Target was: {state['target']} | India win by: {win_by} runs
Venue: Narendra Modi Stadium, Ahmedabad -- 86,000 fans

=== THIS DELIVERY ===
Bowler: {bowler}
Batter: {batter}
Outcome: {event}
{context_block}
This is the moment the entire match has built to. Let it breathe.
Start with the delivery. Then the reaction. Then the weight of what just happened.
and Make it memorable.
Use ONLY the exact scores and numbers from the match situation above. Do not calculate or invent any figures.
"""

    # -- STANDARD BALL ---------------------------------------------------------
    return f"""{COMMENTATOR_PERSONA}
{history_block}
=== MATCH SITUATION ===
Batting: {state['batting_team']} | Bowling: {state['bowling_team']}
Score: {state['score']} | Over: {state['over']}.{state['ball']}
Target: {state['target']} | Need: {runs_needed} off {balls_left} balls
Required Rate: {state['required_rate']} | Current Rate: {state['run_rate']}

=== THIS DELIVERY ===
Bowler: {bowler}
Batter: {batter}
Outcome: {event}
{context_block}
Generate ONE commentary call. 1-2 sentences max for routine balls.
Be specific to these players. Match energy to the situation — dot balls are tense, not explosive.
Use ONLY the exact scores and numbers from the match situation above. Do not calculate or invent any figures.
"""

def generate_commentary(state: dict, delivery: dict, event: str,
                        retrieved_context: list[str],
                        commentary_history: list[str],
                        is_golden: bool = False) -> str:

    prompt = build_prompt(
        state, delivery, event,
        retrieved_context,
        commentary_history,
        is_golden
    )

    try:
        response = client.responses.create(
            model="gpt-5-mini-2025-08-07",
            input=prompt
        )
    except OpenAIError as e:
        print(f"  [WARN] Commentary generation failed ({e}); using fallback line.")
        return f"{bowler} to {batter} -- {event}."

    return response.output_text.strip()
