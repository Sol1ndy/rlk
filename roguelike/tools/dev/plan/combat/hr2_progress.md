# lane H2 (홍련 rebuild: cutscenes, camera, control lock) — progress

Branch `wip/combat-hr2` (from `origin/wip/combat` c7dcc4fbf), worktree `<S>/cb/wt_hr2`, pack copy `<S>/rp_hr2`
(`<S>` = the scratchpad of `h_common.md`). Contract: `hr_design.md` (§8 wins), `hr_brief.md` 「조작 잠금 · 카메라」.
Owner of FN-cam (`build_mboss_core.py`, `mboss_lib.py`), the RIGLIB look target (`mboss_rig_compile.mjs`),
`tools/mboss_scarlet/{seq,cam}.py`, `view/tick`'s guard, the suites `hr/tests/{test_cam,test_seq}.py` + `hr/h2/**`.

## Steps
- [x] **FN-cam** (§5.2): the framework lock. Gates below.
- [x] **RIGLIB look target** (§5.4): `writeFace({target})`, 홍련 = `@e[tag=rlk_body,limit=1]`.
- [ ] merge `H1 interface` (15fad96a9), `cam.py` + `seq.py` (`CONTRACT = 2`), `test_seq.py`, shot sheets.

## FN-cam as built
| piece | what |
|---|---|
| request | `#mbCam mb` 1 from the module's tick + `#mbCamId mb` 1 / 2; `mboss/main` zeroes `#mbCam` at its top (so does `cleanup_fight`, `init`) |
| `rlk:tick` (hand file) | right after `mboss/main`: `#mbCam` 1 → `mboss/cam/hold` as the tagged player; else `mboss/cam/release` as every player carrying `rlk_mb_camh`. The two-player guard at the top releases too |
| `mboss/cam/spawn` | at the execution position, idempotent: two **marker armour stands** `rlk_mb_cam1` / `rlk_mb_cam2` (+ `rlk_mb_cam`, `rlk_room`, `rlk_mb_aux`, `rlk_pet`), invisible, no gravity, `camera_distance` 0. Eye offset measured from the jar: `ArmorStand.MARKER_DIMENSIONS = fixed(0, 0)` → eye height 0: **the stand's position is the eye point** (`mboss_lib.CAM_EYE = 0.0`) |
| `mboss/cam/hold` (+ `hold_in`) | first tick: tag `rlk_mb_camh`, the game mode kept as a tag (`rlk_mb_cgS` / `rlk_mb_cgC`; neither = adventure), the avatar's place into `rlk:mboss camret` (a `/reload` removes the avatar), sprint FOV modifier off, the crosshair title blanked unless an overlay is up, `gamemode spectator`. Every tick: `spectate` the live stand |
| `mboss/cam/release` (+ `back`, `ret`) | no-op without the tag (idempotent): un-spectate, the stored game mode, the tags and `camret` gone; unless dead / in the selection space: the player to the avatar (no avatar: the stored point, as offsets from the origin so a whole x / z is not block-centred, +0.02 b), `rotate` to the boss as seen from the seat, the avatar turned to her, `view/ride_mount` at once when the seat exists and the player is not sneaking; `char/cine/stop` when lane H3's file exists (the generator looks for it) |
| `mboss/cam/kill` | both stands |
| `view/tick` (hand file) | one line after the housekeeping (vBig, fresh, the G menu, the burst camera): a held player's view rests (no avatar move / aim / re-seat) |
| `lvup/tick` (hand file) | one line: a held player's sneak press is no F5 sneak-tap (CS1's skip = Shift held; without it a pending pick played the in-combat deny) |
| explicit releases | `cleanup_fight` (first line: before the module cleanup and before `mboss/won` moves the player out), `mboss/init` (before the helper entities die), `rlk:tick`'s two-player guard; `mboss/uninstall` through its `cleanup` |

Rules the hold follows beyond the design text (each covered by `test_cam.py`):
- the live stand missing (killed) → `release` at once (never a free spectator); the lock comes back when the stands do.
- developer mode (the player is the body, no avatar) → never locked: the cutscene plays from the player's own eyes.
- a request with no fight (`#mbLive` 0) → dropped and released.

Costs (per tick): `mboss/main` +1, `rlk:tick` +2 in every tick; a held tick 12, the first held tick 30, the release 29.

## Gates (FN-cam + look target, before the H1 merge)
- `test_cam.py` 96 checks pass (static / hold / paths / stand / idem / cost / ident).
- `test_special_hr.py` pass, `ident_hr.py` pass (group `LANE_H2` added), `check_mboss_pack` 0, `regen_all.sh` ×2 clean.
- loadcheck `h2a`: 0 function load failures (26.3 parses `spectate`, `rotate … facing`, the stand NBT, the macro).
- rig: `build_scarlet_rig.mjs` rewrites only `rig/face/{player,track}` (+ `rig_bytes` in the manifest); tachy / guardian /
  fieldgen rigs rebuilt with the changed RIGLIB: no file changes; the pack copy stays byte-identical to `rp_base`.

## Decisions / deviations
- `view/tick`'s guard is not the only hand-file change: `rlk:tick` (3 lines) and `lvup/tick` (1 line) too (see the table).
- A dead player or one in the selection space is released without being moved (those flows own the player's place).

## Requests to other lanes
- (none yet)

## Pack files
None added or changed.

## Only a person in the game can check
(list grows with `seq.py`; for FN-cam alone)
- the view while held: no hotbar / hearts, the camera exactly where the stand is, no F5 pull-back, smooth pans (client
  interpolation of the stand: 3 ticks), a hard cut without a visible glide (the idle stand is placed 4 t early).
- Shift held in a skip window: the flicker between the stand and the free spectator view.
- the hand-back: back on the F5 seat behind the avatar in the same tick, facing her, no "F5" chat hint again.
- `/reload` and a relog inside a cutscene: game mode back, standing where the cutscene began.
