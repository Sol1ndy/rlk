# lane H1c (홍련 rebuild: what the fight looks like) — progress

Branch `wip/combat-hr1c` (from `origin/wip/combat` c7dcc4fbf; merged: `origin/wip/combat` 6522feef5 and
`origin/wip/combat-hr1` c1e53b116 = lane H1's finished fight core with its interface commit 15fad96a9), worktree `<S>/cb/wt_hr1c`, pack
copy `<S>/rp_hr1c` (`<S>` = the scratchpad of `h_common.md`). Contract: `hr_design.md` §2.1-§2.3, §5.4, §8.2-§8.6. Owner of
the 12 new fight clips in `tools/scarlet_clips.mjs` and of the H1 block of `tools/build_mboss_hr_fx.py`.

## Done
- **The 12 fight clips** (`tools/scarlet_clips.mjs`, section "the rebuilt fight kit"; H1's `PF(...)` stand-in block removed,
  its `CINE_PLACEHOLDER` kept): `grog_in d4 tri rings ult hcut blue kcut mx nb q_grab q_air` with the contract's names,
  lengths and event ticks (`api.CLIPS`; `q_grab` has §8.2's `star 8`). Per clip the comment above it gives the beats.
  What each swing is, for H1's effects (her frame: + = her right):
  | clip | motion at the hit ticks |
  |---|---|
  | `grog_in` | arms flung wide 2, knees buckle 3, topples backward with the feet still down, the hat leaves her head 6, arcs up at her right and lands on DOWN's spot 10, `DOWN` 10-12 (= `down` 0); `blend 2` (the snap out of any pose is the hit) |
  | `d4` | coil right, one turn to her left with the blade flat at chest height 9-15 (h1 14); rising vertical fan 32-35 (h2 34); two-handed vertical cut 42-45 (h3 44); flat forehand left → right across her front 52-56 (h4 54) |
  | `tri` | thrust at full reach (h0 14); three descending crescents: upper right → lower left (h1 38), upper left → lower right (h2 48), upper right → lower left with a lunging step (h3 60). Planes tilted 58° / 58° / 52° from the vertical |
  | `rings` | one body turn per ring with the blade flat at chest height, alternating: r1 to her left, r2 to her right, r3 left, r4 right, r5 left. A turn runs h − 5 … h + 1, the coil for the next ring is reached at h + 4 |
  | `ult` | iai stance (the blade laid back along the hip scabbard, right hand on its throat) 8-21, the draw across her front 22-25 (cut1 24), held out at her left 26-43 (the edge turned over at star2 34), the cut back across 43-48 (cut2 46), the blade back at the hip 56 |
  | `hcut` | long low stance, the blade trailing low at her left; the flat forehand cut at knee-waist height from her left across her front 24-28 (cut 26) |
  | `blue` | upright, the blade presented high out at her left (4-10), drawn into a thrust chamber beside her left cheek (15), the thrust at full reach (hit 22) |
  | `kcut` | sprinter's crouch, the blade hidden behind her (tip over her back); flat whip from behind her left across her front 19-22 (cut 22), up to her right 23, a return cut down across 25-29 |
  | `mx` | low crouch, the blade low behind her left; the X in two strokes round its tick: rising lower left → upper right 13-15, turned over above her 16, falling upper left → lower right 17-20; swirl up over her right (cue 21), one turn to her left with the blade flat (dome 28) |
  | `nb` | hangs bowed over the player; b1 from her upper right down to her left front (its plane 30° left of her aim), b2 from her upper left down to her right front (30° right), b3 a straight two-handed chop; lands low 46 |
  | `q_grab` | sinks, the open right hand reaching out (the blade low at her left); flies flat with the arm stretched ahead 16-19; the hand closes before her (grab 20) and holds 21 (the module branches at `api.Q_AIR_T0` = 21: `q_air` 0 is this pose); 21-34 = the miss (snatches at air, straightens) |
  | `q_air` | both arms heave up (throw 0-2), diagonal cut from her upper right (beam 22), rises a little with the blade reversed straight down before her chest in both hands (cue 31), comes down behind it (hit 38, land 40); second leap: the blade thrust straight up, the free arm spread (52-71), brought down to point at the player (pillar 74), lands 84 |
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
  - sounds `parry_cue flash_blue ult_cut1 ult_cut2 sky_pillar` (+ H1's `kcut_go`): recipes are `api.KIT_SOUND_RECIPES`
    (equal to §2.1-§2.2); the kit writes `fx/snd/<name>`.
- **Fitted to lane H1's calls** (its finished core, merged here; `pat_p1` / `pat_p2` / `pat_ghost` / `test_scarlet` /
  `test_gauge` pass on the merged tree):
  - `ult_web` / `ult_burst` are laid over the floor whatever the caller's height (H1 calls them at her body, 1.2 b up);
    `ult_web` draws the world only, the `web` overlay is the module's `fx/hud/ovl` call (H1 calls it beside the preset).
  - `qi_beam` has three forms by the call: aimed (P-q: `facing` the lock from the air → along the facing), level from
    ≥ 2.5 b (35° down), and level from lower = **the ground band of P-n, centred on the executor** (H1 calls it at the lock
    point 0.6 b up, turned along the band; the hazard line runs len / 2 each way through the lock), laid 1.35 b over the
    floor at full width.
- **Tools / suites** (new or changed, all under `tools/dev/sim/hr/`):
  - `tests/test_clips_h1c.py` (new): the 12 clips as shipped — contract, joins with the stance clips / `q_grab` → `q_air` /
    `grog_in` → `down`, no root motion, airborne spans (§8.5), the blade at every hit tick against its hazard's shape, the
    blade readable from the F5 lens at every cue / flash tick.
  - `tests/test_rig.py`: the clip count of the rebuilt contract (59). `tools/scarlet_retarget.mjs --dump all` skips a
    clip outside the contract.
  - `tests/test_kit.py`: counts for the rebuilt contract (50 + 6 presets, 104 + 5 sounds + `kcut_go` once declared),
    heights / variants for the six presets, the `web` glyph size, a new section `hr1c` (the yellow sizes, the cue,
    flash_blue's timing, the web lines at any caller height, the burst, the sky mark = lines only, the pillar, the beam's
    three forms and floor clamp, the sound recipes, no new sprite px, no particle that needs options written without
    them); the pitch section knows the aimed beam.
  - `s1k/render/render_hr.py` (new): effect strips of the kit from the F5 camera (the hr kit had no renderer in the repo).

## Gates (the merged tree = H1's final head + this lane, 11-11)
- Builds: rig 59 clips, 0 stand-ins, 8 cinematic placeholders (H2c's); kit 56 presets, 110 sounds, 36 glyphs;
  `regen_all.sh` 0 failures; `check_mboss_pack.py` 0 problems; `api.py --check` ok.
- `test_clips_h1c.py` 297 / 297.
- `test_kit.py` 15 074 / 15 082. Its pins of the 11-06 fight are rebased on the rebuilt module (the sound count, the
  flashes between `follow_on` / `follow_off`, the dash streaks on `core.dash`, tri's thrust streak, kcut's three lines
  through the lock at `api.KCUT_YAW`, the deflect's effects found in the repel sequence's start). The 8 failures left
  are one finding, not a pin: see Requests (the deflect in first person).
- `test_rig.py` (run statement by statement: its cinematic section raises on the 11-06 rows): 142 passed, 12 failed, none
  in the 12 fight clips: the 8 cinematic placeholders (× 6 checks), `seq.py` (`lead60`), the intro seat (× 2), the skin
  file that is not in the container, the dump's clip count 56 of 59 (`lead60 lead5 lead_re` have no source yet). Its clip
  count is 59 now; `scarlet_retarget.mjs --dump all` skips a clip the contract dropped (it raised on `sq1`).
- Lane H1's suites on the merged tree: `pat_p1` 529 / 529, `pat_p2` 67 / 67, `pat_ghost` 65 / 65, `test_scarlet` 47 / 47,
  `test_gauge` 22 / 22. `ident_hr` passes.
- `gen_check_hr.py --rp` (run to its end, about an hour: seven rig builds): see the final report for its result.
- Real server: `loadcheck.sh` 0 function load failures. Pack: `rplint.py` 0, `atlas_px.py` 12 919 040 px (unchanged).

## Decisions / deviations
- `yellow_tell` at Ø 2.0: the size rides on `{t}` (t ≥ 100) so `api.KIT_PRESETS['yellow_tell'] = ['t']` and every existing
  call stay valid; no API change needed from H1.
- `qi_beam`: the design says "the `qi_band` sprite, pitched 35°". Built on the `light_column` sprite (crossed quads, seen
  from every side; `qi_band` is a single sheet, edge-on to the player it is aimed at); the pitch follows the caller's aim,
  35° only for a level call in the air; the P-n band is the centred ground form (above).
- `ult_web`: the 12 world lines are kept low and thin (0.5-2.4 b over the floor where they pass the executor, 0.16 b
  wide): a line near the F5 lens would fill the screen; the screen-space web is the overlay.
- `sky_pillar {r}`: the column is 1.25 r wide (3 b at r 24), the shock ring on the floor has radius r: the pillar lands on
  the player, 3.5 b before the lens. No `flash` particle (26.x wants a colour, and a flash at the player whites the view).
- "iai stance" of `ult` / `mx`: the blade is laid along the hip scabbard, not sheathed (the fight clips' `a9` convention);
  a real sheathe / draw needs the cinematic clips' patches.
- `kcut`: the right hand reaches down but does not touch the floor (the player-size arm is 0.3 b short from that crouch).
- `blue`: the blade is presented high and out to her left (not upright before her face: there it crosses the brim).
- `mx`: the two strokes of the X fall on ticks 13-15 and 17-20 round `x 16` (≤ 120°/t does not allow both inside 14-16).
- `q_air` 30-35: she hangs 0.3 b higher in the clip while the blade points straight down (the rig keeps every blade over
  the clip's floor; the pelvis stays on the anchor's axis, so no root motion in the plane).

## Requests to other lanes
- **H1 (core)**: (1) kcut's big yellow: the size rides on `{t}`: pass `yellow_tell {t:110}` (100 + the ticks; today
  `{t:10}` = the plain Ø 1.6). No contract change. (2) `rings` in P1 has four rings but plays on to `RINGS_END[1]` = 54:
  the clip's fifth turn starts at 49, so 5 ticks of a ring-less spin show. Play the stance at clip tick 49 in P1 (the
  `ult` start at 50 already blends from the coil). (3) The deflect in first person: the 11-06 judge drew its gold
  starburst and light column twice (`unless entity @a[tag=rlk_body]` at the body; `if entity …` 1.8 b before the eyes);
  the repel stand-in of `core.py` (1173-1175) has only the first form: in first person the starburst is 1462 / 626 / 0 /
  0 px and the column 0 px at looks up 30-85° (`test_kit`'s 8 failures; HR-45 / VF2-1-03). H1's stand-in or H2's real
  repel sequence needs the first-person lines back.
- **H2 / H2c**: the `gold` glyph goes next to part 1 of the H1 block (after the `GLYPHS` literal, before its assert); both
  blocks add one `GLYPHS[...]` line there, so the merge may ask to keep both lines. `test_rig.py`'s cinematic section
  (the `WANT` / `HANDOVER` rows with `sq1`, `lead_down`, `lead_stand`) is theirs to rebase with the 8 cinematic clips;
  `test_kit.py` checks CS3's kick flash between `keep_on` / `keep_off` once a sequence calls it.

## Pack files (added / changed in `<S>/rp_hr1c`; all regenerated by the two generators)
- `assets/rlk/font/mboss_hr.json` (5 providers more), `assets/rlk/textures/font/mboss_hr/web.png`, `web_1.png` … `web_4.png`.
- Rig: `assets/rlk/{models/item,items}/mboss/scarlet/**` rewritten with the same bytes (no model changed).
- No change to `assets/minecraft/atlases/items.json` or to `textures/mboss/hr_kit/**`.

## Next
- Nothing open. After the merges at HI: regenerate (rig → kit → `regen_all.sh`), rerun `test_clips_h1c.py`, `test_kit.py`.
