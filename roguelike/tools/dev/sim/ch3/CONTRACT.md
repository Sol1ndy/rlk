# Chapter-3 regular mobs (Sumeru) — shared contract (lead, 10-29)

User asked for chapter-3 mobs in the Sumeru concept and approved the lead's proposal: all 7 mobs, rainforest/desert
weighting, the healer support. Standing rules from chapter 2 hold: NO elemental immunity / resistance / element-gated
shield on any mob; no tutorial/hint text; chapter-1/2 mobs are not mixed into chapter 3.

Chapter 2 was built the same way and is on the release branch: read `roguelike/tools/build_ch2_mobs.py`, `tools/ch2mob/`
(common.py, swarm.py, rig.py, poses.py, elite.py, elite_lib.py), README §5-1 / §5-2, and reuse that framework (brain husk
`rlk_cmb` + display rig + lure, cm/hit_pl, stun/freeze cancel, health bars, level scaling, swarm hit feel, death fling,
multi-kill cue, `rlk_c2lite` reward skip, safe-ground walker, haste). Import helpers from `ch2mob` rather than copying
them; if you must change a ch2 helper, keep ch2 output byte-identical (run build_ch2_mobs.py and confirm `git diff`
shows no change under ch2 files).

Two worktrees in parallel, the lead merges (S = /tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad):
- A = S/ch3/wt_a, branch wip/ch3-swarm, RP S/ch3/rp_a: framework + routing + fu/fp/em/sb (swarm) + cw (healer).
- B = S/ch3/wt_b, branch wip/ch3-elite, RP S/ch3/rp_b: cs, rv, pc (elites).

## Ids (fixed; must not clash with ch1 sw ar fm im sh cn or ch2 ns sl ss sp dr kr nj cc ci)
| id | mob | owner |
|---|---|---|
| fu | 둥실 버섯 (one mob; group spawner g_fu = 5-7) | A |
| fp | 포자 주머니 (left by a dead fu; hittable object, not a room mob) | A |
| em | 에르미타 단검 용병 (one; g_em = 3-4) | A |
| sb | 모래 전갈 새끼 (one; g_sb = 6-8) | A |
| cw | 에르미타 맑은물 술사 (healer) | A |
| cs | 성수 전갈 | B |
| rv | 성수 붉은 독수리 | B |
| pc | 원시 정령 기계·재구성자 | B |

- Spawn entries `rlk:cm/spawn/<id>` (+ A's `g_fu`, `g_em`, `g_sb`), same convention as ch1/ch2; `/function rlk:cm/test
  {t:"<id>"}` works for all.
- Function roots `cm/<id>/...`; shared ch3 code under `cm/c3/` (A). B never writes outside `cm/{cs,rv,pc}/**`,
  `cm/spawn/{cs,rv,pc}`, its generator modules, its rig/texture generator and its own RP assets.

## Generators (never hand-edit generated outputs)
- Entry `roguelike/tools/build_ch3_mobs.py` (A) with package `tools/ch3mob/` (A: common.py, swarm.py, rig/poses as
  needed). It imports `ch3mob.elite` (B) if present and calls `elite.build(w)` (`w('cm/cs/tick', text)` = path under
  data/rlk/function without `.mcfunction`), and `ch3mob.elite_lib.install_hooks(<fn root>)` (idempotent) for B's
  shared-file lines. Stale cleanup: only the ch3 ids' folders, `cm/c3/**` and the ch3 spawn files.
  B: until A's entry is in your tree use a local runner `tools/build_ch3_elite_only.py` (the lead deletes it at merge) and
  keep the shared hook lines OUT of your commit (ship them in `elite_lib.HOOKS`, as ch2's B did).
- Shared-file hook insertion (cm/tick, vis, flash, clean, combat/apply, room/mob_* …) must be idempotent and coexist
  with ch2's lines: running build_ch2_mobs.py and build_ch3_mobs.py in either order, twice, gives identical output.
- Rigs/skins: A `tools/build_ch3_swarm_rigs.mjs`, B `tools/build_ch3_elite_rigs.mjs`; atlas filter-then-push by id;
  lowercase ids; texture budget ≤ 0.4 M px each (items atlas ≈ 11.65 M; client limit ~15.5 M).

## Shared behaviour
- Healer (cw): heals every cm brain (any chapter's, incl. B's elites) within 8 b by 10 % max HP every 2 s while
  channelling, never above max (`mhpC`/`mhpM`), with visible water ribbons to each healed mob; a hit interrupts it for
  3 s. B needs nothing special for this.
- Core-exposed multiplier (pc): while pc carries tag `rlk_c3_core`, every hit on it deals ×1.5 (all damage sources, no
  element condition). B ships the combat hook line in `elite_lib.HOOKS` (the lead/A's entry installs it).
- Burrowed mobs (sb, cs underground) are untargetable and take no damage (tag them so player AoE/auto-aim skip them), are
  not counted as "alive above ground" for multi-kill, and must never hold the room open forever (they surface on a timer).
- Flying mob (rv): stays inside the room box, never above the room's ceiling height / below the floor, never through
  walls; dives only along a path checked clear.
- Telegraphs: every attack has a visible tell ≥ the listed time (glow/pose/sound); allowed floor/ground cues: sand mounds
  (sb/cs), the vulture's dive shadow line, the construct's slam ring. Nothing undodgeable.
- Real-game rules: no negative add/remove literals; no teleports into blocks; nothing below the floor; walls/doors never
  broken; no glyph-font inheritance; vanilla sounds only.

## Roster (raw, level 1; first drafts)
A — swarm (ch2 swarm hit feel):
1. fu 둥실 버섯: HP 6, packs of 5-7 floating ~1 b up, drifting toward the player; inflate 0.5 s → body bump 10. On death
   leaves fp for 3 s: fp is hit by any player attack → bursts r 3 dealing 12 + 30 % of each mob's max HP? (tune so one
   pop kills a fu pack, hurts others) to MOBS only, never the player. fp never counts as a room mob, gives no reward.
2. em 에르미타 단검 용병: HP 10, groups of 3-4 orbit the player at ~4 b; two at a time crouch 0.6 s then dash-stab 14
   (converging to the centre, so they bunch after the stab).
3. sb 모래 전갈 새끼: HP 4, groups of 6-8 burrowed; they surface together in a ring around the player (sand mound 0.8 s
   tell), bite 8, stay up 2 s, re-burrow, repeat. Desert rooms (in rainforest rooms they are not spawned).
7. cw 에르미타 맑은물 술사: HP 22, keeps 7-10 b away; healing channel (above).
B — elites (normal hit feel):
4. cs 성수 전갈 (desert): HP 80. Burrow-travel fast with a visible sand trail → trail stops + mound shakes 0.6 s →
   erupts under the player's last spot with an uppercut 18 (punish window 1.2 s after surfacing). Above ground: pincer
   2-hit combo (0.5 s tell, 10 + 12), tail stab (0.8 s tail-charge tell, 20, short range line).
5. rv 성수 붉은 독수리 (desert, sometimes rainforest): HP 55, flies. Rise + shriek, 0.7 s aim with a ground shadow line,
   straight dive 18 → crashes, grounded 1.5 s (punish). Fire-feather fan (0.6 s wing-spread tell, 5 feathers ±30°, 7
   each, Pyro).
6. pc 원시 정령 기계·재구성자 (rainforest-weighted): HP 75. Scatter into cubes → reform beside the player (0.5 s cube glow
   at the target spot) → hammer slam r 2.5 (0.7 s raised-arm tell + slam ring, 18) or cube spin r 3 (0.8 s tell, 14).
   After 2 reforms: 1.5 s overheated, core exposed (`rlk_c3_core`, ×1.5 damage taken).

## Routing (A)
- Chapter 3 rooms use ONLY the ch3 roster; chapters 4+ keep today's behaviour (ch1 roster). Chapter 1/2 unchanged.
  `#mobTmp` keeps its meaning.
- Room biome: README §(room themes) — ch3 zones are rainforest or desert by zone data `sd` (1 = desert). Composition by
  map order: 1-2 → rainforest: 2 fu packs; desert: sb group + em group. 3-4 → rainforest: fu + em + pc; desert: sb + em
  + (cs or rv). 5-6 → as 3-4 plus cw and a second elite (rainforest: pc + rv; desert: cs + rv). Scale counts with the
  existing room rule (threat comparable to ch2 at the same map order, adjusted for level).
- B's ids are called through a macro (`$function rlk:cm/spawn/$(id)`) so A's tree loads without B's files.
