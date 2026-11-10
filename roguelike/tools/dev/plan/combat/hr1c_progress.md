# lane H1c (홍련 rebuild: what the fight looks like) — progress

Branch `wip/combat-hr1c` (from `origin/wip/combat` c7dcc4fbf, merged `origin/wip/combat-hr1` 15fad96a9 = the H1 interface
commit), worktree `<S>/cb/wt_hr1c`, pack copy `<S>/rp_hr1c` (`<S>` = the scratchpad of `h_common.md`). Contract:
`hr_design.md` §2.1-§2.3, §5.4, §8.2-§8.6. Owner of the 12 new fight clips in `tools/scarlet_clips.mjs` and of the H1 block
of `tools/build_mboss_hr_fx.py`.

## Done
- **The 12 fight clips** (`tools/scarlet_clips.mjs`, section "the rebuilt fight kit"; H1's `PF(...)` stand-in block removed,
  its `CINE_PLACEHOLDER` kept): `grog_in d4 tri rings ult hcut blue kcut mx nb q_grab q_air` with the contract's names,
  lengths and event ticks (`api.CLIPS`; `q_grab` has §8.2's `star 8`). Per clip the comment above it gives the beats.
  What each swing is, for H1's effects (her frame: + = her right):
  | clip | motion at the hit ticks |
  |---|---|
  | `grog_in` | arms flung wide 2, knees buckle 3, topples backward, the hat leaves her head 6 and lands on DOWN's spot 10, `DOWN` 12 (= `down` 0); `blend 2` (the snap out of any pose is the hit) |
  | `d4` | coil right, one turn to her left with the blade flat at chest height 9-15 (h1 14); rising vertical fan 32-35 (h2 34); two-handed vertical cut 42-45 (h3 44); flat forehand left → right across her front 52-56 (h4 54) |
  | `tri` | thrust at full reach (h0 14); three descending crescents: upper right → lower left (h1 38), upper left → lower right (h2 48), upper right → lower left with a lunging step (h3 60). Planes tilted 58° / 58° / 52° from the vertical |
  | `rings` | one body turn per ring with the blade flat at chest height, alternating: r1 to her left, r2 to her right, r3 left, r4 right, r5 left. A turn runs h − 5 … h + 1, the coil for the next ring is reached at h + 4 |
  | `ult` | iai stance (the blade laid back along the hip scabbard, right hand on its throat) 8-21, the draw across her front 22-25 (cut1 24), held out at her left 26-43 (the edge turned over at star2 34), the cut back across 43-48 (cut2 46), the blade back at the hip 56 |
  | `hcut` | long low stance, the blade trailing low at her left; the flat forehand cut at knee-waist height from her left across her front 24-28 (cut 26) |
  | `blue` | upright, the blade presented high out at her left (4-10), drawn into a thrust chamber beside her left cheek (15), the thrust at full reach (hit 22) |
  | `kcut` | sprinter's crouch, the blade hidden behind her (tip over her back); flat whip from behind her left across her front 19-22 (cut 22), up to her right 23, a return cut down across 25-29 |
  | `mx` | low crouch, the blade low behind her left; the X in two strokes round its tick: rising lower left → upper right 13-15, turned over above her 16, falling upper left → lower right 17-20; swirl up over her right (cue 21), one turn to her left with the blade flat (dome 28) |
  | `nb` | hangs bowed over the player; b1 from her upper right down to her left front (its plane 30° left of her aim), b2 from her upper left down to her right front (30° right), b3 a straight two-handed chop; lands low 46 |
  | `q_grab` | sinks, the open right hand reaching out (the blade low at her left); flies flat with the arm stretched ahead 16-19; the hand closes before her (grab 20); 20-34 = the miss (snatches at air, straightens) |
  | `q_air` | both arms heave up (throw 0-2), diagonal cut from her upper right (beam 22), the blade reversed point down before her in both hands (cue 31), comes down behind it (hit 38, land 40); second leap: the blade thrust straight up, the free arm spread (52-71), brought down to point at the player (pillar 74), lands 84 |
- **`tools/scarlet_retarget.mjs`**: one line, `HAT_FLIGHTS.grog_in` (the hat's flight 6-10 from her head to DOWN's leg spot).
  The file has no owner in §8.3 and the declared flights live there; the line stands apart from the `HAT_FLIGHTS` literal so
  H2c's edits of the `repel` / `ending` rows merge cleanly.
- **The H1 block of the kit** (`tools/build_mboss_hr_fx.py`, two marked parts + the demo rows in `_demos()`):
  - part 1 (after `GLYPHS`): the `web` overlay glyph U+EC18 (256 × 144 px, 15 cut lines with cyan / red fringes, tinted
    facets; opacity steps follow the base overlays').
  - part 2 (before the presets' contract assert): `flash_blue {t}`, `ult_web {t}`, `ult_burst`, `sky_mark`,
    `sky_pillar {r}`, `qi_beam {len}`. **No new sprite**: the blue sphere is `blink_bubble` tinted, lines / beams / columns
    are the `light_column` sprite (kinds `qline`, `col_face`, `light_column`); the items atlas does not grow (0 of the
    22 432 px; `flash_blue`'s planned 4 096 px are not used, so `api.KIT_SPRITES_HR` stays undeclared).
  - existing presets at new sizes: `yellow_tell {t}` with **t ≥ 100 = the big tell** (Ø 2.0 b, flare 5 b) for t − 100 ticks
    (kcut: `{t:106}`); `glint {c:2}` = the parry cue: three crossed sparkles to 1.8 b for 7 t (the other colours unchanged);
    `qi_ring` needs nothing new (rendered at r 26 / 30 chest height and r 45 c 2 knee height).
  - sounds `parry_cue flash_blue ult_cut1 ult_cut2 sky_pillar`: recipes are in `api.KIT_SOUND_RECIPES` (H1's interface
    commit, equal to §2.1-§2.2); the kit writes `fx/snd/<name>`.
- **Tools / suites** (new or changed, all under `tools/dev/sim/hr/`):
  - `tests/test_clips_h1c.py` (new): the 12 clips as shipped — contract, joins with the stance clips / `q_grab` → `q_air` /
    `grog_in` → `down`, no root motion, airborne spans (§8.5), the blade at every hit tick against its hazard's shape, the
    blade readable from the F5 lens at every cue / flash tick.
  - `tests/test_kit.py`: counts for the rebuilt contract (50 + 6 presets, 104 + 5 sounds), heights / variants for the six
    presets, the `web` glyph size, a new section `hr1c` (the yellow sizes, the cue, flash_blue's timing, the web lines and
    overlay, the burst, the sky mark = lines only, the pillar, the beam's pitch rule and floor clamp, the sound recipes, no
    new sprite px); the module scan runs whenever `boss/scarlet/core` exists.
  - `s1k/render/render_hr.py` (new): effect strips of the kit from the F5 camera (the hr kit had no renderer in the repo).

## Decisions / deviations
- `yellow_tell` at Ø 2.0: the size rides on `{t}` (t ≥ 100) so `api.KIT_PRESETS['yellow_tell'] = ['t']` and every existing
  call stay valid; no API change needed from H1.
- `qi_beam`: the design says "pitched 35°". The preset follows the executor's rotation when it looks down ≥ 10° (a caller
  that aims it with `facing`), and draws 35° down when called level from ≥ 2.5 b over the floor; its length is cut so the
  2.6-b body ends over the floor. Built on the `light_column` sprite (crossed quads, seen from every side) instead of the
  `qi_band` sprite (a single sheet: edge-on to the player it is aimed at).
- `ult_web`: the 12 world lines are kept low and thin (0.5-2.4 b up where they pass the executor, 0.16 b wide): a line near
  the F5 lens would fill the screen; the screen-space web is the overlay.
- `sky_pillar {r}`: the column is 1.25 r wide (3 b at r 24), the shock ring on the floor has radius r: the pillar lands on
  the player, 3.5 b before the lens.
- "iai stance" of `ult` / `mx`: the blade is laid along the hip scabbard, not sheathed (the fight clips' `a9` convention);
  a real sheathe / draw needs the cinematic clips' patches.
- `kcut`: the right hand reaches down but does not touch the floor (the player-size arm is 0.3 b short from that crouch).
- `blue`: the blade is presented high and out to her left (not upright before her face: there it crosses the brim).
- `mx`: the two strokes of the X fall on ticks 13-15 and 17-20 round `x 16` (≤ 120°/t does not allow both inside 14-16).

## Requests to other lanes
- **H1**: (1) kcut's big yellow: `K.p('yellow_tell', t=106)`. (2) `rings` in P1 has four rings: play the next clip (the
  stance or `ult`) by clip tick 49 — the fifth turn starts there (the clip's 47-49 is the coil, so a start of `ult` at 50
  blends from it). (3) `qi_beam`: call it at her blade / chest in the air, either rotated `facing` the lock or level.
  (4) `ult_web {t:20}` / `ult_burst` / `sky_mark` / `sky_pillar` take the floor point (the lock) as executor; `sky_mark`
  lies across the executor's facing. (5) `flash_blue {t:15}` at clip tick 0 between `follow_on` / `follow_off`: yellow 0-4,
  blue 4-19. (6) `test_rig.py` still holds the 47-clip contract and the 11-06 cinematic events (it stops at its cine
  section): H1 / H2 update it; until then `tests/test_clips_h1c.py` covers the new fight clips.
- **H2c**: the `gold` glyph goes next to part 1 of the H1 block (after the `GLYPHS` literal, before its assert); both
  blocks add one `GLYPHS[...]` line there, so the merge may ask to keep both lines.
- **lead**: `test_kit.py` fails 3 checks only because H2's sequences are stand-ins (`calls: … kick flash kept`, `calls: 300
  kit calls`, `view: 3 player-anchored effects`).

## Pack files (added / changed in `<S>/rp_hr1c`; all regenerated by the two generators)
- `assets/rlk/font/mboss_hr.json` (5 providers more), `assets/rlk/textures/font/mboss_hr/web.png`, `web_1.png` … `web_4.png`.
- Rig: `assets/rlk/{models/item,items}/mboss/scarlet/**` rewritten with the same bytes (no model changed).
- No change to `assets/minecraft/atlases/items.json` or to `textures/mboss/hr_kit/**`.

## Next
- Nothing open. After the merges at HI: regenerate (rig → kit → `regen_all.sh`), rerun `test_clips_h1c.py`, `test_kit.py`.
