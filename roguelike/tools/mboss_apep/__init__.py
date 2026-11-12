"""아펩의 오아시스 파수꾼 (Apep), the chapter-3 boss (plan S:ap/plan.md; contract S:ap/ap_contract.md): module generator
package (plan 3.5).

api        the stable contract (ids, scores, DMG / REV tables, ranges, texts, the rig / org manifests, Pattern / TL / Gen,
           the kit stand-in K); frozen at AP-I1, changed by request only; the requests of the pattern stages applied at AP-I2 (ap_contract 0.11)
core       the 17 hooks + prep, the phase machine (E -> P1 -> T1 -> P2 -> CS -> P3 -> D), RES, pools / floor / titles,
           proxies per form / stance, capsules, body park, bars, music, pause / reload / cleanup / uninstall per phase,
           the services, the main slot, the yaw and px-set drivers, tests (AP-CORE)
ai         zones (mv/local), bands, facing, crawl / walk, clamps, the BACK dwell and rim rules, weights, cooldowns,
           no-repeat, chains, the Q2 schedule, anti-stall (AP-CORE)
p1 seq     P1-P6, R, (M sounds); E, D             (AP-P1)
p3         Q1, Q3, Q3s, Q4, Q5                     (AP-P3)
aftermath  Q2 종말의 여파                           (AP-P3)
revival    T1, the Heart, waves, failure, phase-2 HUD, CS   (AP-REV)
org        the organism runtime, walls             (AP-REV)
"""
PATTERN_MODULES = ('p1', 'p3', 'aftermath')
SERVICE_MODULES = ('seq', 'revival', 'org')
