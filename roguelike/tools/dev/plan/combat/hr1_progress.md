# lane H1 (홍련 rebuild: the fight) — progress

Branch `wip/combat-hr1` (from `origin/wip/combat` c7dcc4fbf), worktree `<S>/cb/wt_hr1`, pack copy `<S>/rp_hr1`
(`<S>` = the scratchpad of `h_common.md`). Contract: `hr_design.md` (§8 wins). Owner of
`tools/mboss_scarlet/{api,ai,p1,p_ghost,core,shield,s3lib}.py`, `tools/build_mboss_scarlet.py`, FN-bal, the pattern /
gauntlet / gauge / balance suites and `hrfair` 2.0.

## Steps
- [x] **H1 interface** (the first commit): §5.1 in `api.py`, the rig contract of 59 clips, FN-bal, the sequence wiring of
      the core on the new sequence set. Gates: module builds, `regen_all.sh` clean twice, `check_mboss_pack` 0,
      `api.py --check` ok, loadcheck `hr1_if` 0, rplint 0, atlas 12.919 M (pack byte-identical to `rp_base`).
- [ ] state machine (§1.1), gauge (§1.2), balance + groggy (§1.3-1.4), interrupts (§1.5)
- [ ] patterns §2.1-2.2 (P1 kit, P2 adds, `ult`), parry cue, flashes
- [ ] AI (weights, bands, far / rear rules, `rings` → `ult` at a full gauge)
- [ ] gauntlets G1 / G2, judge, fails, banner (§2.4)
- [ ] test ids (§5.1), suites (§6.1), `hrfair` 2.0 and the first T1-T13 table (§6.4)

## What the interface commit holds (for the other lanes)
Final at once (use them from `api`):
- New names: `GAUGE`, `GAUGE_FP`, `BAL`, `PP_FLINCH`, `CUE_LEAD` / `CUE_KIT` / `CUE_SND`, `FLASH`, `FLASH_SND`,
  `PURPLE_LEAD`, `YELLOW_MIN`, `NP_OWN`, `BAL_OFF`, `STAGE_FMAX`, `CS0_P0` / `CS0_BEARING` / `CS0_WALK_BACK` /
  `CS0_END_DIST`, `SKIP`, `CONTACT` (+ `CONTACT_TOL`), `ACTOR_CLIPS`, `ACTOR_LIMIT`, `ACTOR_CALLS`, `ACTOR_CLOCK`,
  `CAM_REQ` / `CAM_ID`, helpers `actor()`, `actor_clock()`, `actor_ready()`, `cam_req()`, `cam_ready()`.
- The sequence / cinematic contract: `SEQS`, `SEQ_LEN`, `SEQ_ARGS`, `SEQ_CLIPS`, `SEQ_EXTRA` (+ `cs1` skip), `LINE_AT`,
  `MUSIC_AT`, `SKIP_T`, `SKIP_WINDOW`, `END_H`, `COUNTER_EV`, `WARN_TEXT`, `PH[3] = lead60`; `CLIPS_PLAN` with 59 clips
  (the 12 new fight clips `CLIP_OWNER 'H1'`, the 8 cinematic clips `'H2'`), `CINE_CLIPS`, `NEW_FIGHT_CLIPS`,
  `UNUSED_CLIPS`; registry `intro` 1450 / `death` 1494.
- Kit: `KIT_PRESETS_HR` (6), `OVERLAYS_HR` (`gold` 0xEC17, `web` 0xEC18), `KIT_SPRITES_HR` (`flash_blue` 1 × 64 × 64),
  5 sounds in `KIT_SOUND_RECIPES` (`parry_cue`, `flash_blue`, `ult_cut1`, `ult_cut2`, `sky_pillar`: the kit generator
  already writes `fx/snd/<name>` for them).
- FN-bal: `#mbBalOff mb` (`bal/boss/may` + `fight_vars` / `cleanup_fight`).

Still the 11-06 values until H1's build commits (H1-internal): `HITS`, `WEIGHTS`, `COOLDOWN`, `MID_MAX`, `FAR_RULE`,
`PAT_END`, the gauntlet scripts, `CUT_IDS`, `BOLTS`, `JUDGE_T` / `REPEL_T`, `FAIL*_T`, `P1` / `P2`, `TEST_IDS`,
`PIP_RULE`, the names §5.1 removes.

## Requests to other lanes (how your part is picked up)
- **H2 (`seq.py`)**: put `CONTRACT = 2` on a line of its own in the rewritten `seq.py`. Until that line exists
  `build_mboss_scarlet.py` does not import the file and every sequence runs as the core stand-in `core/sq/<name>`
  (the build prints `stand-in sequences (core/sq): …`). `seq/cs1/skip` is expected like `seq/intro/skip`
  (`api.SEQ_EXTRA`). The core starts `lead60` with the shield already 5/5 (`refill` at its tick 0 is the core's);
  `lead5` / `lead_re` signal `refill` through `#sq_sig` at their beat.
- **H2 / H2c (`scarlet_cine.mjs`)**: nothing to mark. `build_scarlet_rig.mjs` now takes a cinematic clip from the file
  when its last key = the contract's length, else builds the static placeholder of `scarlet_clips.CINE_PLACEHOLDER`
  (printed as `note: placeholder clips …`; the manifest marks `placeholder: true`); clips the contract no longer has
  (`sq1`, `lead_down`, `lead_stand`) are ignored. Owners `S2b` / `H2` = cinematic file, `S2a` / `H1` = `scarlet_clips.mjs`.
- **H1c (`scarlet_clips.mjs`)**: the 12 placeholders are one marked block at the end (`// STAND-IN (H1)`, `PF(...)`):
  delete it when the real clips are in (your file wins whole at the merge).
- **H1c / H2c (kit)**: `api.KIT_PRESETS` / `api.OVERLAYS` / `api.KIT_SPRITES` gain an H-lane name as soon as
  `build_mboss_hr_fx.py` contains `@preset('<name>'` / `api.OVERLAYS['<name>']` / a sprite group `'<name>': [`
  (`api.kit_declares`), so the generator's own equality asserts hold in every branch. If `flash_blue` needs another
  sprite shape than 1 × 64 × 64, or another preset / sound is needed, tell H1 (api.py is H1's).
- **H3**: `api.actor*()` turn on when `tools/player_motion/cine/manifest.json` exists.

## Decisions / deviations
- §8.4 "additively": the pattern contract stays as built until the patterns are rebuilt; the sequence contract was
  switched at once (the four waiting lanes need its numbers), with `seq.py` (11-06) left untouched and ignored by the
  marker rule above, so no lane gets a merge conflict from H1 in its own files.
- `build_scarlet_rig.mjs` (no owner in §8.3) got the owner mapping and the placeholder fallback above (about 20 lines in
  its clip block; H2's look-target option is elsewhere in the file).
- FN-bal's two zeroing lines are in `build_mboss_core.py` (H2's file for FN-cam): next to the `#mbBarOff` zeroing in
  `fight_vars` and `cleanup_fight`.

## Pack files
None added or changed so far (`diff -rq rp_base rp_hr1` is empty after the rig and kit generators).
