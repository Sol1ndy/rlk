# lane VB (round V: the boss in the fight) — progress

Branch `wip/v-boss` (from `origin/wip/v` d7e7cf013), worktree `<S>/cb/wt_vb`, pack copy `<S>/rp_vb` (from `<S>/rp_fin`).
Contract: `v_brief.md` §3 "VB" (1-6) + §4. Scratch: `<S>/vb/` (before / after strips, the debug datapacks, logs).

## How to build / run
```bash
S=<scratchpad>; WT=$S/cb/wt_vb/roguelike; cd $WT
node tools/build_scarlet_rig.mjs --resourcepack $S/rp_vb [--debug-dp $S/vb/dbg --debug-clips <fight clips>]   # also writes tools/scarlet_blade_track.json
python3 tools/build_mboss_hr_fx.py --resourcepack $S/rp_vb && bash tools/dev/regen_all.sh .
bash $S/vb/simcopy.sh        # the suites' copy: $S/vb/sim (hr1_progress.md "How to run")
cd $S/vb/sim/hr/tests && python3 pat_p1.py $WT ...
python3 -I tools/dev/sim/hr/vb/fightcam.py $WT --dbg $S/vb/dbg --rp $S/rp_vb strip --clip a3 --event h1 --dist 7 --field p1 -o x.jpg
python3 -I tools/dev/sim/hr/vb/windups.py $WT
```
Clip authoring: `node tools/build_scarlet_rig.mjs --resourcepack <throwaway rp> --datapack <scratch dp> --only a,b` (40 s) writes
`<scratch dp>/blade_track.json`; `windups.py <wt> --track <that>`.

## Done (see the commits)
- the blade track sidecar `tools/scarlet_blade_track.json` (rig build), `tools/mboss_scarlet/blade.py` (swing analysis, the path /
  head / slash cards, the target line), kit sprites `sw_path sw_head sw_arc_0..2`, the blade look `edge`
- p1.py / p_ghost.py: every hit draws from the track; the hand-placed crescents are gone; dash-short 2.0 b, landings 1.4 b short,
  leaps 3.4 b, the gauntlet stations, the dive's reappearance in view (g_dive 22 t)
- clips: the wind-ups (see windups.py)

## Next
see the end of this file (kept current)
