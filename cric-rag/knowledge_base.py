# knowledge_base.py
# Static RAG layer — pre-match context + FIRST INNINGS facts
# Used to generate commentary for the SECOND INNINGS (NZ chase)
#
# This is what an AI Ravi Shastri would know sitting down to commentate
# the second innings — everything that happened before and during India's batting.

FACTS = [

    # ══ TOURNAMENT CONTEXT ════════════════════════════════════════════════
    "The 2026 ICC Men's T20 World Cup final is between India and New Zealand at Narendra Modi Stadium, Ahmedabad.",
    "India are the defending T20 World Cup champions, having won the 2024 title.",
    "New Zealand have never won a T20 World Cup title in their history.",
    "New Zealand have lost four consecutive ICC white-ball finals before this one.",
    "India have won the T20 World Cup in 2007 and 2024 — tonight they chase a historic third title.",
    "New Zealand won the toss and chose to bowl first.",
    "The 2023 ODI World Cup final was also played at this very ground — India lost to Australia that day.",
    "Tonight India have a chance to erase that Ahmedabad heartbreak forever.",
    "86,000 fans packed Narendra Modi Stadium for the final — overwhelmingly pro-India.",
    "India are playing their first T20 World Cup final on home soil.",

    # ══ FIRST INNINGS — INDIA BATTING SUMMARY ════════════════════════════
    "India posted 255 for 5 in their 20 overs — the highest total ever in a T20 World Cup final.",
    "New Zealand need 256 runs to win the T20 World Cup — the highest ever chase in a T20 World Cup final.",
    "India scored 88 runs in the powerplay without losing a wicket — an explosive start.",
    "Sanju Samson and Abhishek Sharma put on 88 runs for the first wicket in the powerplay.",

    # ══ FIRST INNINGS — ABHISHEK SHARMA ══════════════════════════════════
    "Abhishek Sharma was dismissed for a rapid score caught by Tim Seifert off Rachin Ravindra in over 7.",
    "Abhishek Sharma attacked Jacob Duffy mercilessly in over 5 — hitting 4, 6, 4, 2, 4 in that over alone.",
    "Abhishek Sharma hit Lockie Ferguson for a four and a six in over 3 during the powerplay.",
    "Abhishek Sharma's dismissal brought Ishan Kishan to the crease.",

    # ══ FIRST INNINGS — SANJU SAMSON ═════════════════════════════════════
    "Sanju Samson batted through the powerplay and deep into the innings — the anchor of India's total.",
    "Sanju Samson hit three consecutive sixes off Rachin Ravindra in over 13 — an extraordinary sequence.",
    "Sanju Samson hit two sixes off Lockie Ferguson in over 11 as India accelerated.",
    "Sanju Samson was finally dismissed by James Neesham in over 15 after a magnificent innings.",
    "Sanju Samson was part of the 2024 World Cup squad but didn't play a single game — this innings was his redemption.",

    # ══ FIRST INNINGS — ISHAN KISHAN ═════════════════════════════════════
    "Ishan Kishan came in at number three and played a brilliant innings alongside Samson.",
    "Ishan Kishan hit three sixes in over 11 — two off Ferguson and one earlier.",
    "Ishan Kishan hit a six off Mitchell Santner in over 14.",
    "Ishan Kishan was dismissed by James Neesham in over 15 — part of a stunning hat-trick over.",

    # ══ FIRST INNINGS — NEESHAM'S DEVASTATING OVER (15) ══════════════════
    "James Neesham took three wickets in over 15 — dismissing Samson, Ishan Kishan and Suryakumar Yadav.",
    "Suryakumar Yadav was dismissed for a duck by Neesham in over 15 — caught by Rachin Ravindra.",
    "India collapsed from 201/1 to 202/4 in a single Neesham over — the match suddenly alive.",
    "James Neesham was the most dangerous bowler for New Zealand — finishing with multiple wickets.",

    # ══ FIRST INNINGS — HARDIK PANDYA & DEATH OVERS ══════════════════════
    "Hardik Pandya came in after the three-wicket collapse and steadied the innings with Tilak Varma.",
    "Hardik Pandya hit a six off Matt Henry in over 18 before being dismissed shortly after.",
    "Tilak Varma held his nerve throughout the death overs alongside Hardik and then Shivam Dube.",

    # ══ FIRST INNINGS — SHIVAM DUBE'S FINISH ════════════════════════════
    "Shivam Dube finished the innings in explosive style — hitting 4, 6, 6, 4, 0, 4 in the final over.",
    "Shivam Dube smashed 24 runs off Neesham in the last over to take India past 250.",
    "India's last over produced 24 runs — turning a good total into a truly mammoth one.",

    # ══ FIRST INNINGS — NZ BOWLING ════════════════════════════════════════
    "Matt Henry was expensive in the powerplay — conceding multiple wides and being hit for sixes.",
    "Lockie Ferguson was hit for 20 runs in over 3 — four wides cost him dearly.",
    "Jacob Duffy conceded 20 runs in over 5 as Abhishek Sharma dominated.",
    "Mitchell Santner was the most economical New Zealand bowler — keeping things tight in the middle overs.",
    "Glenn Phillips bowled just one over and was taken off after being hit.",

    # ══ NZ PLAYERS — BATTING (pre-innings context) ════════════════════════
    "Tim Seifert is New Zealand's most explosive opener — known for aggressive starts against pace.",
    "Tim Seifert has scored the most fifty-plus scores for NZ in T20 World Cup history.",
    "Finn Allen is New Zealand's power-hitter at the top — capable of changing a match in one over.",
    "Rachin Ravindra is a dangerous left-handed batsman who has been in excellent form this tournament.",
    "Glenn Phillips is NZ's middle-order match-winner — can hit sixes at will.",
    "Daryl Mitchell performs under pressure in ICC knockouts — a big-match player.",
    "Mitchell Santner is NZ's captain — leads from the front and bats usefully in the lower order.",
    "James Neesham is a dangerous lower-order hitter — just proved it with the ball, can do it with the bat too.",

    # ══ INDIA BOWLERS (second innings context) ════════════════════════════
    "Jasprit Bumrah is the best T20 death bowler in the world — his yorker is virtually unplayable.",
    "Jasprit Bumrah is India's all-time leading wicket-taker in T20 World Cups.",
    "Jasprit Bumrah is a right-arm fast bowler known for his unorthodox bowling action.",
    "Axar Patel is a left-arm orthodox spinner — India's vice-captain bowling on his home ground.",
    "Varun Chakravarthy is a right-arm mystery spinner whose variations trouble every batting lineup.",
    "Arshdeep Singh is a left-arm fast-medium bowler — effective with the new ball and at death.",
    "Hardik Pandya is a right-arm medium-fast all-rounder.",
    "Abhishek Sharma is a left-arm orthodox spinner who also opens the batting for India.",
    "Jasprit Bumrah has taken at least two wickets in every T20 World Cup knockout match he has played.",
    "Axar Patel is India's vice-captain and a reliable left-arm spinner on this Ahmedabad ground — his home venue.",
    "Varun Chakravarthy's mystery spin has troubled every batting lineup in this tournament.",
    "Arshdeep Singh has been effective with the new ball throughout the tournament.",
    "Hardik Pandya is a genuine wicket-taking all-rounder — already proved it with the bat today.",

    # ══ HEAD-TO-HEAD & MATCH PRESSURE ════════════════════════════════════
    "India and New Zealand have met three times in T20 World Cup history — India have won all three.",
    "New Zealand are known for punching above their weight in ICC tournaments.",
    "256 is a daunting target in T20 cricket — only twice has a team successfully chased more than 240 in a T20I.",
    "New Zealand need to bat through 20 overs without a collapse — their biggest vulnerability in ICC finals.",
    "India are heavy favorites — but NZ have shown they can chase under pressure.",
    "The Ahmedabad pitch is expected to assist spin in the second innings as dew settles.",
]

if __name__ == "__main__":
    print(f"Total facts in knowledge base: {len(FACTS)}")
    for i, fact in enumerate(FACTS, 1):
        print(f"{i}. {fact}")