# cricket_simulator.py
# AI Cricket Commentator — T20 World Cup 2026 Final
# Second innings: New Zealand chasing 256
# Features:
#   - Reads real ball-by-ball JSON
#   - Selective RAG (wickets, boundaries, over starts, new batters)
#   - Commentary history (last 6 balls) for narrative continuity
#   - Dynamic RAG layer (live facts added after key events)
#   - Golden moment handling (10th wicket)

import json
import os
import textwrap

from rag_engine import CricketRAGEngine
from commentary_generator import generate_commentary

# -- LOAD REAL MATCH DATA ------------------------------------------------------
MATCH_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "1512773.json")

try:
    with open(MATCH_DATA_PATH, "r") as f:
        match_data = json.load(f)
except FileNotFoundError:
    raise SystemExit(f"Match data file not found: {MATCH_DATA_PATH}")
except json.JSONDecodeError as e:
    raise SystemExit(f"Match data file is not valid JSON: {e}")

try:
    second_innings = match_data["innings"][1]
    TARGET = second_innings["target"]["runs"]  # 256
except (KeyError, IndexError) as e:
    raise SystemExit(f"Match data is missing expected second-innings fields: {e}")

if second_innings["team"] != "New Zealand":
    raise SystemExit(
        f"Expected second innings to be New Zealand, got {second_innings['team']!r}"
    )

# -- MATCH STATE ---------------------------------------------------------------
state = {
    "batting_team": "New Zealand",
    "bowling_team": "India",
    "score": "0/0",
    "over": 0,
    "ball": 0,
    "target": TARGET,
    "runs_needed": TARGET,
    "run_rate": 0.0,
    "required_rate": 0.0,
    "wickets": 0,
    "total_runs": 0,
    "balls_bowled": 0,
    "legal_balls": 0,
}


# -- CLASSIFY EVENT ------------------------------------------------------------
def classify_event(delivery: dict) -> str:
    if "wickets" in delivery:
        wicket = delivery["wickets"][0]
        kind = wicket["kind"]
        fielders = wicket.get("fielders", [])
        catcher = fielders[0]["name"] if fielders else None

        if catcher:
            return f"wicket ({kind}, caught by {catcher})"
        return f"wicket ({kind})"

    runs = delivery["runs"]["batter"]
    extras = delivery.get("extras", {})
    if "wides" in extras:   return "wide"
    if "noballs" in extras: return "no ball"
    if runs == 6:           return "SIX"
    if runs == 4:           return "FOUR"
    if runs == 0:           return "dot ball"
    return f"{runs} run{'s' if runs > 1 else ''}"


# -- UPDATE STATE --------------------------------------------------------------
def update_state(state: dict, delivery: dict, over_num: int, ball_num: int) -> dict:
    state["over"] = over_num
    state["ball"] = ball_num
    state["total_runs"] += delivery["runs"]["total"]

    extras = delivery.get("extras", {})
    is_legal = "wides" not in extras and "noballs" not in extras
    if is_legal:
        state["legal_balls"] += 1

    if "wickets" in delivery:
        state["wickets"] += 1

    state["score"] = f"{state['total_runs']}/{state['wickets']}"
    state["runs_needed"] = TARGET - state["total_runs"]

    overs_done = state["legal_balls"] / 6
    balls_remaining = 120 - state["legal_balls"]
    state["run_rate"] = round(state["total_runs"] / overs_done, 2) if overs_done > 0 else 0
    state["required_rate"] = round((state["runs_needed"] / balls_remaining) * 6, 2) if balls_remaining > 0 else 99

    return state


# -- SELECTIVE RAG TRIGGER -----------------------------------------------------
def needs_rag(event: str, state: dict, new_batter: bool) -> bool:
    if "wicket" in event:              return True  # wicket ball
    if new_batter:                     return True  # new batter walked in
    if event in ["SIX", "FOUR"]:       return True  # boundaries
    if state["legal_balls"] % 6 == 0:  return True  # first ball of each over
    return False  # dot/single/wide -- skip


# -- BUILD RETRIEVAL QUERY -----------------------------------------------------
def build_query(delivery: dict, event: str, state: dict,
                new_batter: bool, is_golden: bool) -> str:
    batter = delivery["batter"]
    bowler = delivery["bowler"]
    runs_needed = state["runs_needed"]
    balls_left = 120 - state["legal_balls"]

    # Golden moment -- fetch big picture context
    if is_golden:
        return "India winning World Cup third title historic moment champions Ahmedabad"

    # New batter -- focus on who just walked in
    if new_batter:
        return f"{batter} batting for New Zealand, {bowler} bowling, NZ {state['score']}"

    # Wicket -- focus on the dismissal matchup
    if "wicket" in event:
        return f"{bowler} bowling to {batter}, wicket, NZ {state['score']}, {runs_needed} needed, pressure"

    # Boundary -- focus on the attacking shot
    if event in ["SIX", "FOUR"]:
        return f"{batter} hit {event} off {bowler}, NZ {state['score']}, {runs_needed} needed"

    # Over start -- general match situation
    return f"{bowler} bowling, NZ {state['score']}, need {runs_needed} off {balls_left} balls"


# -- GOLDEN MOMENT DETECTION ---------------------------------------------------
def is_golden_moment(delivery: dict, state: dict) -> bool:
    return "wickets" in delivery and state["wickets"] == 10


# -- MAIN SIMULATION -----------------------------------------------------------
def run():
    global state

    print("=" * 70)
    print("  AI CRICKET COMMENTATOR -- T20 WORLD CUP 2026 FINAL")
    print("  New Zealand chasing 256 | Narendra Modi Stadium, Ahmedabad")
    print("=" * 70)

    rag = CricketRAGEngine()
    initial_fact_count = len(rag.facts)

    commentary_history = []  # rolling last 6 commentary lines
    current_batters = set()  # tracks who has already batted
    bowler_wickets = {}  # live wicket count per bowler

    for over_data in second_innings["overs"]:
        over_num = over_data["over"]
        ball_num = 0

        for delivery in over_data["deliveries"]:
            extras = delivery.get("extras", {})
            is_legal = "wides" not in extras and "noballs" not in extras
            if is_legal:
                ball_num += 1

            # 1. Update match state
            state = update_state(state, delivery, over_num, ball_num)
            event = classify_event(delivery)

            # 2. Detect new batter
            batter = delivery["batter"]
            new_batter = batter not in current_batters
            if new_batter:
                current_batters.add(batter)

            # 3. Detect golden moment
            is_golden = is_golden_moment(delivery, state)

            # 4. Decide whether to generate commentary
            # Overs 0-15: only wickets and boundaries
            # Overs 16+:  every ball (full simulation)
            full_simulation = over_num >= 16
            should_commentate = is_golden or full_simulation

            # Always update dynamic layer regardless of commentary
            bowler = delivery["bowler"]
            if "wicket" in event:
                bowler_wickets[bowler] = bowler_wickets.get(bowler, 0) + 1
                player_out = delivery["wickets"][0]["player_out"]
                kind = delivery["wickets"][0]["kind"]
                rag.add_live_fact(
                    f"{bowler} has taken {bowler_wickets[bowler]} wicket(s) in this innings. NZ {state['score']}.")
                rag.add_live_fact(
                    f"{player_out} was dismissed {kind} by {bowler}. NZ {state['score']}.")
            if event in ["SIX", "FOUR"]:
                rag.add_live_fact(
                    f"{batter} hit a {event} off {bowler}. NZ are {state['score']}, needing {state['runs_needed']} more.")

            if not should_commentate:
                continue

            # 5. Selective RAG -- only retrieve when meaningful
            retrieved_context = []
            if is_golden or needs_rag(event, state, new_batter):
                query = build_query(delivery, event, state, new_batter, is_golden)
                retrieved_context = rag.retrieve(query, top_k=4)

            # 6. Generate commentary
            try:
                commentary = generate_commentary(
                    state, delivery, event,
                    retrieved_context,
                    commentary_history,
                    is_golden
                )
            except Exception as e:
                print(f"  [WARN] Skipping commentary for over {over_num}.{ball_num}: {e}")
                continue

            # 7. Update commentary history (rolling last 6)
            history_entry = f"Over {over_num}.{ball_num} | {event} | {commentary}"
            commentary_history.append(history_entry)
            commentary_history = commentary_history[-6:]

            # 8. Print output
            if is_golden:
                marker = "[GOLDEN MOMENT]"
            elif "wicket" in event:
                marker = "[WICKET]"
            elif event in ["SIX", "FOUR"]:
                marker = "[BOUNDARY]"
            else:
                marker = "[BALL]"

            print(f"\n{marker} Over {over_num}.{ball_num} | {delivery['bowler']} to {batter}")
            print(
                f"{event.upper()} | Score: {state['score']} | Need: {state['runs_needed']} off {120 - state['legal_balls']} balls")

            print(f"Commentary:")
            print(textwrap.fill(commentary,width=100))
            print("-" * 70)

    print("\n" + "=" * 70)
    print(f"  FINAL: New Zealand {state['score']} all out (chasing 256)")
    print(f"  INDIA WIN THE T20 WORLD CUP 2026 BY 96 RUNS")
    print(f"  Knowledge base grew from {initial_fact_count} to {len(rag.facts)} facts during innings")
    print("=" * 70)


if __name__ == "__main__":
    run()