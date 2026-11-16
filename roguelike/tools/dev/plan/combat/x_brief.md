# Round X — bodies colliding in the 홍련 fight (lead, 11-16)

The user (verbatim): 「홍련 보스전에서 여전히 몸이 서로 부딪히는 문제가 있어. 영상은 아직 안 찍었는데 곧 올릴테니 원인 파악하고 있어봐」
("In the 홍련 boss fight the bodies still bump into each other. I'll upload a video soon; find the cause meanwhile.")
The investigation (simulator runs, bytecode, the t3 / t4 recordings; tools and logs in `$S/cb/collide/`,
`S` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`) found, ranked:

1. **Fight — her stop points are stale and nothing checks the live body.** Dash-throughs (A9, HCUT, BLUE, KCUT: stop
   2.0 b before the spot locked 7 t before the hit, `p1.py:442–450`, `DASH_SHORT` `p1.py:130`), dives (A4, A10, Q's dive:
   1.4 b, `p1.py:132, 159–167`), MX's streak (1.6 b, `p_ghost.py:799`), Q's lunge (≤ 2.0 b, `p_ghost.py:915`), TRI's
   lunge (1.5 b from the start position, `p1.py:611`) are all aimed at where the player WAS. A player walking toward her
   during a mid-range wind-up ends inside her: measured with the real dodge set and a walking player (0.216 b/t, stops
   1.5 b from her): A9 / HCUT / BLUE / KCUT 0.49–0.74 b closest, 9 ticks < 0.6 b; **MX 0.09 b, 20–22 ticks < 0.6 b
   (~1.1 s merged)**; Q 0.61; A10 0.72; holding W through her 0.02 b. `core/cam_ok` (`p1.py:146–152`) does not guard
   the body in the game: it measures against the eyes of `@a[tag=player]`, the tiny rider ~2.36 b above the avatar's
   feet (seat), so it passes with her standing on the avatar; in the tests the player IS the body (eye 1.62), which is
   why round W's `dodgecam` (a player that never walks) found nothing.
2. **Nothing separates the bodies.** The avatar is a vehicle (the F5 seat rides it) so vanilla push never moves it
   (26.3 `Entity.push`), her husk is NoAI (all her motion is scripted `tp`), 홍련 does not turn on the framework's body
   push `#mbPushOn`, and the only player-side body check is the cartwheel's `player/dodge/clear2` (#dgMv 2). Walking,
   the twist, the lunge-step, the back-step, knockback and skills pass through her.
3. **Cutscene — the repel's R2–R6 is still body to body** (ticks 33–101): R4 (t50–69: the cuts at 56 / 62 and the
   actor passing her right side at 0.5 b) is 0.30–0.72 b torso to torso, neither declared contact nor checked
   (`test_contact` checks gaps only on 8 lock spans, `test_contact.py:159–160`); t33–35 0.92–1.53 b. Round W changed
   only `REPEL_F` (R0/R1). t4 51.53–54.12 s shows it. Every other sequence is ≥ 1.66 b.
4. **Gauntlet stations** are fixed 10–14 t ahead from the player's old position (`p_ghost.py:369, 676–690`; `side` 2.2 b
   at +35°, `d2e` 1.6 b at +45°, `over` 1.3 b ahead and 2.5 b up, `land` 2 b ahead): with a walking player G1 0.28 b
   for 20 ticks (D2 into A8.4), 0.03 b at A8.3 (directly over the avatar's head); G2 0.28 b for 15 ticks. Seen in t3
   148–157 s, 177–186 s and t4 13–20 s, 43 s.
5. **Player-side moves with no body check**: the lunge-step (1.6 b in 5 t), the twist (0.4 b toward the view = toward
   her), 아를레키노's E (`char/arlecchino/skill_dash`: 1.4 b in front of the target), 클로린드's lunge (`player/nudge`),
   spot-centred disc knockback "away from the origin" (`mboss/hz/init`: pushes a player who stepped in further toward
   her, ≤ 0.6 b).
6. **The G1 fail**: `ult/fail60` pushes the player 3 b toward the arena start while she glides to `land` 2 b ahead of the
   camera; facing the entrance, the push carries the player through her (t3 159.67–160.92 s).
7. Visual only: her hat brim (Ø 1.32 b at 1.98 b) covers the avatar's head within ~0.9 b; t3 94.0 s is occlusion.

## Rulings — lane XB (one lane: boss, player side and the repel)
1. **A body rule, everywhere in her fight**: her body and the player's avatar (`@e[tag=rlk_body]`; the stand-in rig and
   the mannequin follow it) never come closer than **1.4 b** centre to centre on the floor, except declared contact
   (Q's grab, a hit's own frame is not contact — sector / disc hits land at ≥ 1.4 b fine). Enforce it from both sides:
   - *her moves*: every arrival (dash-through, dives, MX's streak, Q's lunge, TRI's lunge, the gauntlet glides and
     stations, the G1 / G2 dives, `land`, the recovery walk) is checked against the **live** body when the move starts
     and on every glide tick; she stops at ≥ 1.6 b along her path (shorter glide; the hazard still covers the locked
     spot, so the attack's reach and fairness do not change). One shared helper for all of them. `cam_ok` gets a body
     clause measured from the avatar's feet (not the camera rider's eyes) in addition to its camera-line clause.
   - *a soft separation*: when the avatar is within the rule while neither is in a scripted contact, move the avatar
     out radially (≤ 0.25 b/t, collision-checked, never into a wall or off the arena, never during the beat's held ticks
     or a locked sequence), or use the framework's `#mbPushOn` capsule if it does the same with less code — pick one
     and say why. The player must never be pushed *through* her.
   - *the player's moves*: the dodge set's `player/dodge/clear` covers the lunge-step and the twist (and the back-step);
     아를레키노's E stops ≥ 1.6 b from a boss body; 클로린드's lunge (`player/nudge`) the same; spot-centred discs push
     along the line from her to the player when she is the source (`kbdir`), not "away from the origin" into her.
   - *the G1 fail*: push away from her landing point (and land her where the pushed player is not).
2. **Gauntlet stations** are re-checked against the live player when the glide starts and every tick (≥ 1.6 b, else
   the next candidate); `d2e` ≥ 2.0 b; A8.3 beside the player, not over their head. The re-timed cut ticks of round W
   (`test_metro` 33/33, `chainparry` 624/624) must not move.
3. **The repel cutscene**: re-stage R2–R6 so the figures keep a swordfighter's distance except the declared contact
   rows (the grab, the hilt strike, the hook, the throw, the kick): R4's cuts at sword reach (her stagger farther out,
   or the actor steps back before cutting), the pass-by ≥ 0.9 b to the side, t33–35's step-in not into her. Replace
   `test_contact`'s 8-span gap rule with: every tick of every two-figure clip ≥ 1.5 b torso to torso, except declared
   contact rows ≥ 0.25 b (no interpenetration even in contact). Render the repel's shots after the change and look.
4. **Tests that would have caught this**: the simulator's camera player at seat height (2.11 / 2.36 / 2.85 for the three
   camera settings) where the camera matters; `dodgecam` (or a new section) with walking, sprinting (the 11-16 out-of-
   combat sprint does not apply in her fight, but a W-holding player does), W-lunging and dodging players, every
   pattern of both phases and both gauntlets and the G1 / G2 fail: gate = no tick below the body rule outside declared
   contact. Put the investigation's `collide_run.py` / `g1fail_run.py` / `cine_gap.py` into the repo's suites where
   they belong.
5. Balance: hit ticks, damage, shapes and weights stay; re-run test_bal_hr and the quick hrfair (and the full one if a
   stop distance changes what a pattern reaches); `test_metro`, `chainparry`, `test_vi`, `test_wi` stay green.

Owner of everything above for this round (her module, the core helpers it needs, the player's dodge / nudge / 아를레키노
E, the repel staging and the actor's clip for it, the tests). Gates, rules, saving and the final report as in
`h_common.md` / `v_brief.md` §4, with the trailer of `w_brief.md` §5. Base `origin/wip/x`; branch `wip/x-body`; worktree
`$S/cb/wt_xb`; pack copy `cp -r $S/rp_rel4 $S/rp_xb`; progress file `xb_progress.md`. A recording from the user may
arrive while you work — the lead forwards it.
