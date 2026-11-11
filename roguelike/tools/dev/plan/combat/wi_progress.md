# Round W, lane WI (the integration of lanes WC / WP / WB) — progress and report

Branch `wip/w-int` (from `origin/wip/w` 02a162a03), worktree `<S>/cb/wt_wi`, pack `<S>/rp_wi` (from `<S>/rp_rel3`, the 11-12 release
pack); `<S>` = the scratchpad of `w_brief.md`. Contract: the lead's brief for lane WI, `w_brief.md`, the three lanes' progress files
(`wc_progress.md`, `wp_progress.md`, `wb_progress.md`). The release entries (README 0-1, 0-10, the build stamp, the pack's version
line) are the lead's and are NOT written. Scratch `<S>/wi/` (`fullregen.sh <rounds>`, `suites.sh <tag> <dir:suite> …`, logs in
`out/`, a trial merge worktree `wt_try` + `rp_try` while lane WB was still working).

## Steps
- [x] merges (merge commits): `wip/w-cam` c9a427f4e (no conflict), `wip/w-player` 47ad3b270 (no conflict: README auto-merged)
- [x] regeneration of the WC + WP merge in README 0-4 order, twice: `git status` empty after both rounds (the merged generated
      outputs are what the merged generators write); pack hash `c0ec234180ecf02d` both rounds; `diff -rq rp_rel3 rp_wi` = WC's four
      `hr_cine` half-petal files + WP's `cb/tint.png` and 31 `_hot` sprites
- [x] seams found on the WC + WP merge and fixed (below): the cartwheel's stand-in rig without a beat, a dodge in flight into a lock
- [x] T3-09 (WB -> lead): her damage numbers smaller and beside her (below)
- [ ] `wip/w-boss` final head (lane WB is re-timing G1 / G2): fetch, merge, regenerate twice
- [ ] seam tests on the final tree (`tools/dev/sim/hr/tests/test_wi.py` + `test_vi.py`), hrfair 2.0, budgets, gates, docs

## Merge notes
| merge | conflicts | resolution |
|---|---|---|
| `wip/w-cam` c9a427f4e | none | |
| `wip/w-player` 47ad3b270 | none (README auto-merged) | |

## What the seams showed (fixed here)
1. **The cartwheel's stand-in rig never played without a beat** (lane WP; found by `test_wi dodgelock`). A mannequin character's
   (루미네, 클로린드, 로노바, 네페르) double dodge starts the stand-in rig `lite/f` (`char/motion/dash2` -> `lite/start_f`: plActive 1,
   the mannequin hidden with infinite invisibility), but `rlk:tick` ran `lite/tick` only inside `player/def/beat/post`, i.e. while a
   beat runs. A plain cartwheel (no perfect dodge) left a frozen stand-in figure at the cartwheel's start and the avatar invisible
   until the next dodge / beat. Fix: `rlk:tick` runs `lite/tick` at the same place when no beat runs (one gated line).
2. **A dodge in flight when a locked sequence starts kept moving the hidden avatar** (lane WP x lane WC; `test_wi dodgelock`):
   player/tick's move line runs before the fight tick, so the twist / lunge-step / back-step / cartwheel went on for up to 5 ticks
   under the actor (the hand-back puts the player at the avatar's place: up to 1.6 b off where the lock took them; the mannequin's
   crouch and the cartwheel's stand-in rig carried into the lock). Fix: `player/tick` -> `player/dodge/cut` while the player carries
   the hold tag `rlk_mb_camh`: no move, the crouch stood up, the stand-in rig stopped (not while a beat runs: the beat ends itself
   one tick into the lock, round V); the avatar it shows is hidden again by `char/cine/tick` later in the same tick.
3. **test_cam D1** read only the round V groups of `ident_hr.py`: lane WP's round W files failed it on the merged tree; it reads the
   round V and round W groups now (the integration's own group `LANE_WI` added to `ident_hr.py`).

## T3-09 (WB -> lead): the player's damage numbers over her
Measured (`test_wi dmgnum`, the fight camera 8 b from her: the player 4 b in front of her + the F5 camera 4 b behind the eyes; FOV 90,
1080p; the font's advances x 0.025 b x the display scale): a normal number (`combat/text_normal_macro`, scale 1.35) "259" ≈ 41 px
wide, a crit (`text_crit_macro`, 1.9, ✧✦ … ✦✧ bold) ≈ 215 px, spawned on her chest / head (± 0.8 b, 1.6–2.6 b up) and rising 1.9 b
in 16 t (the review: up to ~150 px over her). A small change in the number code, so done: on her body (`rlk_mb_scarlet`) the two
number lines of `combat/apply` are skipped and `combat/text_normal_side` shows the number at 2/3 size (0.9 / crit 1.2 without the
outer ✧: ≈ 27 / 99 px), beside her as seen from the player (1.1–1.5 b off the her -> player line, left or right at random) at
shoulder / head height (1.9–2.4 b); life and rise unchanged. Every other target keeps the old numbers. Cost: one self-tag test per
hit (`test_m0diff` A: named apart as `LANE_WI_CMD` 0.2). The function names start with `text_normal` / `text_crit` on purpose: the
suites' worlds stub those prefixes as leaves (azsim `LEAF_PREFIX`), as they do the old numbers. Smoke / flames of the player's
skills over her: not touched (each character's own effect files; listed in Open).
