# Review A (player side) — lead rulings (11-11). Findings: `findings_A.json`. Fix lane: `wip/combat-fix`.

| id | ruling |
|---|---|
| A-01 | Fix. (1) An ignored press pushes the lock a full `#parGap` (so mashing faster than the gap never re-arms). (2) **Whiff streak**: a press whose window ran out unused, followed within 40 t by another accepted press that is also unused, lengthens the lock: 12 → 24 → 36 t (cap); any parry (tier 1-3) resets the streak and keeps the short chain lock (hit + `#parChain`). Targets, measured with the reviewer's loops: blind pressing at every regular period 1-40 t and at irregular gaps → ≤ 10 % of strikes perfect-parried and ≥ 70 % of the unparried damage taken; a player who presses at h − 1 for every hit of a chain with gaps ≥ 10 t is never refused; one too-early or too-late press costs at most the next hit. Tune the numbers to meet the targets; constants in `load.mcfunction`. |
| A-02 | Fix (the reset before the call). Add the dynamic test. |
| A-03 | Fix: the afterimage must not show a death: one tick before its end `Glowing:0b` and moved out of sight, removed on the next tick (or a display-entity afterimage). Nothing visible after its 8 t. |
| A-04 | Fix: a perfect parry consumes the volley group too (`grp_mark` when `#parT` is 3), so tier 3 ≥ tier 2 ≥ tier 1. A dodge still does not. README 3 and the suites that pin the rule follow. |
| A-05 | Fix (effects are not aged in their spawn tick). |
| A-06 | Fix (the afterimage faces as the body did). |
| A-07 | Fix (the stamps are initialised before the first input; a stranded `rlk_dgo` is cleared). |
| A-08 | Fix (F and a right-click in one tick: both act). |
| A-09 | Fix (the crosshair returns in the tick the overlay ends). |
| A-10 | Fix the README / comment lines, except the 홍련 section (lane H rewrites it). (a): keep the behaviour (the use-item path stamps one tick later, the window stays 3 full ticks), correct the sentence. |
| A-11 | Add the missing dynamic checks (A-01, A-02, A-05, A-07, A-08) and run the pre-pass and `mboss/near_all` in at least one boss world loop. |
| A-12 | Dodge without timing: the cooldown is **18 t** after a dodge that avoided nothing and **12 t** after one that avoided an attack (loose or perfect) — set 18 at the start, refund 6 when it avoids. 질주's reduction is −20 % as its lore says (fix the rounding). Energy stays: only a perfect dodge of a real hit pays. Measure the reviewer's loop again and report. |
