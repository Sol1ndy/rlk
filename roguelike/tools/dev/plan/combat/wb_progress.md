# lane WB (round W: the boss in the fight) — progress

Branch `wip/w-boss` (from `origin/wip/w` 2613c47f0, + the brief's §4 / §5 merged), worktree `<S>/cb/wt_wb`, pack copy
`<S>/rp_wb` (from `<S>/rp_rel3`, the 11-12 release pack). Contract: `w_brief.md` §2 "WB" + §3 + §5 (the trailer
`Claude Opus 5.5`). Scratch `<S>/wb/` (`dbg/` = the rig's debug frames for fightcam, `before/`, `after/` strips, logs).

## Status
- [x] read the briefs, the round V lane (vb_progress), the integration (vi_progress), t3's overview sheets, the fight review
      (`review/w/findings_fight.json`: T3-06 / 08 / 09 / 11 are this lane's)
- [x] the rig track sidecar carries `f0` (the sword's first key ends there: the blend-in before it) and `sp` / `sq` (the sword part's
      translation / rotation as the client shows them each tick) and the top-level `blade` [bladeLo, tip]: `build_scarlet_rig.mjs`
- [x] `blade.py`: round V's path / head / target line / tall mark / static lines and their run-time (`core/sw/aim|march|head`) removed;
      the trail (band, pieces, ribbon, wave) generated from the shown sword
- [x] p1.py / p_ghost.py / core.py / shield.py / s3lib.py wired (every pattern, both gauntlets, the ghost form); the fight hook's ride
      line; core/pp stops it, core/pat_end + core/g/end take what is left; core/cam_ok + core/cam_clear (T3-06)
- [x] kit sprites / models: sw_rib_0..2, sw_quad_0..2 new; sw_arc_0..2 repainted (a wedge with a chord rim: ribbon + ink + faint fill,
      T3-11); sw_path gone; sw_head kept (the flashes' star); models sw_band, sw_rib_k, sw_fan_k (wedge + rim wall), sw_quad_k
- [x] test_blade rewritten (347 checks), test_vi beatpat on the trail, test_kit's sprite pin; all hr suites pass (test_vi rerun)
- [ ] fightcam: trail measure at 4 / 7 / 10 b both fields (FOV 90); before / after strips
- [ ] full gates (regen twice, loadcheck, gen_check_hr, hrfair quick), docs (README 홍련, hr_design), final push

## Design (decided)
Nothing is drawn where the blade is going. The trail is generated from the blade the rig SHOWS on the pattern clock
(`blade.Shown`: the clips a pattern plays at their pattern ticks, the blend-in before `f0` from the pose shown before):
- **band**: one lance card on the blade (0.26 b, from 22 % of the blade to the tip), riding her, sent each pattern tick to the
  blade's pose of the next tick with one tick of interpolation (= the rig's own key timing): the trail's head, on every tick
  from the first known pose to the end of the last follow-through.
- **pieces**: per pattern tick t the surface the blade sweeps t -> t + 1 (a sector `sw_fan` when it turns about a point of its
  own line, <= 40 deg each; a strip `sw_quad` when it moves sideways). Summoned at t - 1 with NO width on the blade's line of t,
  opened at t with one tick of interpolation: its leading edge moves with the blade (never ahead); ridden 2 ticks, then left in
  the world where it was swept; fading frames at +3 / +5, gone at +7 (w_brief: ~6-8 t). A swing's pieces ([a, b] of a hit)
  are whiter and carry a taller rim wall: round V's slash IS the trail's brightest stretch (one effect; the slash sectors are
  replaced by these pieces).
- **ribbon**: where her body carries the blade (dashes, lunges, dives, gauntlet approaches, A8.3's leap): a band from where
  her hand was when the move began, grown each tick to the hand's place of the PREVIOUS tick (one step behind her model: never
  ahead, at any clock speed).
- **wave**: a dash-through's struck line and kcut's crossing lines (they reach beyond her blade) flash ON the hit tick only.
- Colour: the hit the blade is on its way to: white-gold #FFE9A8 (parryable), the flash colour (unparriable); a swing mixed
  55 % to white.
- The band and the pieces carry `rlk_mb_part` (lane VP's beat: held ticks, the slow motion's interpolation stretch, the
  rocked-back tilt treat them as her rig's parts); the ribbon / wave do not (their origin is not at her feet).
- The core's hook rides the cards after `rig/tick` (at the rig's pelvis: identical to the model, also after `follow_now`);
  core/pp kills the band and fades the pieces, core/pat_end kills what is left.

## Decisions / deviations
(filled as the work goes)

## How to run
See vb_progress.md "How to build / run" (same tools); the debug frames for fightcam:
`node tools/build_scarlet_rig.mjs --resourcepack $S/rp_wb --debug-dp $S/wb/dbg --debug-clips $(cat $S/vb/fight_clips.txt)`.
