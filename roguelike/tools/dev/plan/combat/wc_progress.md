# Round W, lane WC (cutscenes) — progress

Branch `wip/w-cam` (from `origin/wip/w` 540f5f68c, merged f4187dbd3 for w_brief §4–§5), worktree `<S>/cb/wt_wc`, pack copy
`<S>/rp_wc` (from `<S>/rp_rel3`, the 11-12 release pack); `<S>` = the scratchpad of `w_brief.md`. Contract: `w_brief.md` §2 "WC"
1–4 and §4 "WC, added" 5–7, `v_brief.md` §3 "VC" + §4, `h_common.md`. Commit trailer: w_brief §5 (Opus 5.5).
Recordings: `<S>/cb/video3/t3.mp4` (second playtest), `t4.mp4` (the "third cutscene"). My frame grabs: `<S>/cb/video3/wc/`.
Scratch: `<S>/cb/wc/` (scripts `suite.sh`, `fullregen.sh`, `regen.sh`, `dbg.sh`, `shots.sh`, `fr.py`, probes `pr_*.mjs`; sheets `a_*` =
before, `b_*` = after).

## Steps
- [x] diagnose: drinking (CS1 S9 + intro I6–I10), the petal cut (S11), the top-down shot (S5), the stray text (all from t3 / t4)
- [x] the stray text: texts only on the LIVE camera (`mboss/cam/text`, storage `rlk:mboss camtx`), re-applied at every cut
- [x] FOV 90 as the reference for the camera texts (line 36 px glyphs at 90, hint moved to the top right); test_cam T1 / T2 at 70 / 90 / 110
- [x] S5 from above: 6.5 b up, the stage axis across the picture, both figures whole at 70 / 90 / 110; S5b the waiting actor
- [x] two-figure framing check (`framing.two_figure_bad`, `cam.Shot.full`), every two-figure shot of cs1 / intro / repel / ending
- [x] the petal: falls 46 t with a sway, cut by her level draw at 647 (her clip's draw raised), halves fall on (two half-card models, no new texture)
- [x] the CS1 drink rebuilt (solver channels `lipL` / `botW` / `botH`: the bottle's rim at her mouth, the bottle tilting with her head), S9b profile shot
- [ ] the intro's cup drink (I9 600–664) and the pour (I6) checked / rebuilt
- [ ] suites: test_seq P (petal speed / size / blade / face), D (rim to mouth), F5 (two figures), X (stray text); test_cine rows
- [ ] §4.5 bodies apart in every lock / clash (gap check on the two rigs' boxes)
- [ ] §4.6 the aerial duel replaced by close blade clashes with sparks
- [ ] forwarded review findings (`review/w/findings_cine.json`)
- [ ] docs (README 홍련 section, hr_design), final gates, push

## What was wrong (diagnosis)
- **Stray text** (w_brief §4.7): every camera carried a line and a hint text_display, and `cam_line` wrote the line on BOTH cameras.
  The idle camera stands somewhere in the world (prepared PRE ticks before its cut at the next shot's place, or left where the
  last shot ended), often inside the live shot's view: its billboard text, 0.3 b before ITS eye, then shows in the live
  picture as a small text in the world (t3 / t4: "small and far away at her upper right"). Fix: the text lives in storage
  `rlk:mboss camtx`; `mboss/cam/text` writes it on the live camera's two texts (tags `rlk_mb_camx1` / `_camx2`) and blanks the
  idle camera's; `cam.Track.lines()` calls it at every cut, `cam/kill` blanks the store (a skip's new cameras start empty).
- **Top-down shot** (S5, CS1 180–219): eye ST(0, 5, 4.5) straight down with screen-up = the stage forward: at FOV 90 the picture
  covers 10 b along the axis, the figures stood at f 0 and f 9 → both on / outside the top and bottom edges (t3 117–118 s: only
  ground).
- **Petal** (S11): summoned at 610 hanging still 1.5 b before the lens at her waist, the kit's slow rock its only motion; 0.8-b card
  at 1.5 b → small; her blade swept low along the ground and never passed it; the halves drifted for 15 t.
- **CS1 drink** (S9 458–492): the bottle was tipped by the forearm's frame with the arm out to the side (aL [140, 55, .5]): the base
  pointed at the lens beside her ear, the rim never at her mouth (0.2–0.35 b off), the head turned away; before it a 22° nod hid
  her face under the brim.

## Checkpoint 1 (gates)
Full regeneration (README 0-4 order, `<S>/cb/wc/fullregen.sh`) twice: same tree / pack hashes. check_mboss_pack 0; rplint 0; atlas 13.108 M
(unchanged: the half petals reuse the kit's texture); loadcheck `wc_a` 0 failures, `Done (`. test_cam ALL; ev_dry 82/82; test_cine 159/159;
test_contact 94/94; test_actor 158/158; test_flow 40/40; test_rig 162/162; test_vi 208/208; ident_hr ALL. test_seq: all but **F5 repel60 /
repel5 / ending** (the two-figure framing check, new: R0's first two ticks and E2's first ticks have her head at the edge at FOV 70 /
90; E6 the aerial duel) - those shots are rebuilt by §4.5 / §4.6, next.

## Pack files (added by `tools/build_blank_tex.py`; nothing else of the pack changes)
`assets/rlk/items/hr_cine/petal_half_a.json`, `petal_half_b.json`, `assets/rlk/models/item/hr_cine/petal_half_a.json`, `petal_half_b.json`
(the kit's `petal_big_0` texture on two half cards: no new texture, no atlas growth).

## Requests to other lanes
- none yet.
