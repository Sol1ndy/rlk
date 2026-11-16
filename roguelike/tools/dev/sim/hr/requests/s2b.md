# S2b requests (wip/hr-s2b = fb97b3b; for S1K, S3 and the lead at I1 / V)

None of these blocks S2b's hand-over or another stage; no contract value changes (`api.py` untouched, S2a's sources untouched).

1. **Loadcheck pending the user's EULA consent (lead).** The local test server was never started. Every static gate ran:
   `rplint` 0 on `HR/rp_s2b` (RP hash `08625ceee52c79cb91d03294851d0a099df18315`, unchanged from S2a: the clips change no model),
   two rig builds byte-identical, `regen_d0.sh` twice → only `tools/mboss_scarlet/seq.py`, `tools/scarlet_cine.mjs`,
   `tools/scarlet_rig_manifest.json` and `F:boss/scarlet/rig/**` (idempotent), `check_mboss_pack` 0, `api.py --check` ok, the four
   checkers, `test_rig.py --rebuild` 86/86, `ev_dry.py` 62/62. Run the loadcheck of the rig + `seq/**` at I1 once consent is recorded.
2. **Checker baseline (I1).** Against S2a's `0c88e7f`: `check_refs` / `check_macro` / `check_nbtpath` nothing new; `mb/lint_mc`
   "bad target '<uuid>'" × 11 546 more, all in the cinematic key files `F:boss/scarlet/rig/c/<cine clip>/k/*` (the declared rig
   outputs; S2a's known kind, already 203 491 times in the base). `seq/**` is not on this branch (S3's generator writes it).
3. **For S3 — running `seq.SERVICES` (contract §3.5 / §3.7).**
   - Build: `for s in seq.SERVICES: s.build(W)` with `W = api.Writer('S2b', api.OWN['S2b'])`; each writes only `seq/<s.name>/`.
     `s.clip` = `api.SEQ_CLIPS[name]`, `s.args` = `api.SEQ_ARGS.get(name, {})`, `s.events` = the clip events it keys on.
   - Start: `scoreboard players set #sq hr 0`, then `function rlk:boss/scarlet/seq/<name>/start` as and at the body
     (`husk rlk_mb_body`), before `rig/tick` in the same game tick. Macro starts: `repel {at:60}` / `{at:5}`,
     `lead_stand {g:"a8"}` / `{g:"a13"}`; the others take no arguments.
   - Tick: every tick `#sq hr` += 1, `seq/<name>/tick` (as and at the body), then read `#sq_sig hr`, apply it and reset it to 0
     (1 / 2 / 3 = hp1 / hp2 / hp3 at `repel` 24 / 75 / 102; 4 = refill at `lead_down` 29 / `lead_stand` 18), then `rig/tick`.
     Done when `#sqdone hr` = 1 (the start sets it to 0).
   - Intro skip: after `api.SKIP_HOLD` t of sneak during `#sq` < `api.SKIP_T` (554), call `seq/intro/skip` (as and at the body),
     then set `#sq hr` 553; the next tick (554) plays `intro_end` with line 11 on the black.
   - Ending → event: at `#sqdone` of `ending` (1042) start `seq/event` in the same tick (`#sq` 0, `start`); it ends at 120.
   - Cancel: `seq/<name>/cancel` (no executor needed, idempotent) on abort, phase switch, death and reload; it kills only the
     sequence's own entities (`rlk_hr_stage`, `rlk_hr_sqp`, `rlk_hr_sqh`, `rlk_hr_ev`, all also `rlk_room rlk_mb_aux`). A
     reload in the middle of a sequence needs the same cleanup (or a `cancel` call) from the core's reload path.
   - The seat rock (S3's decor prop, `api.deco()['seat_rock']`): the intro re-looks it by position (within 0.6 b, tag
     `rlk_hr_deco`): `bare` at 24 (the bottle leaves it), `bottle` at 52, `set` at the cup-down (206), killed at the tuck (630) and
     by the skip. Spawn it with look `bottle` at intro start; its top is at knee height (≈ 0.75 b: the seated pose puts the
     pelvis 0.40 b down).
   - Distance at intro start: the walk legs (0.15 b/t) run while she is ≥ 8.2 b from the player and stop at ≤ 7 b; nearer than
     that she turns to the player and walks in place for the clip's walk. Put the player ≥ 10 b from the seat at entry
     (PLAN §3.1 stages ≈ 30 b).
4. **For S1K (kit).**
   - `moon_halo`: CS0 E3 (the cup raised to the moon, 112-146) and CS4 (the gaze, 690-780) brighten the halo by ≈ 20 % in the plan;
     the contract has no means for it (the prop's looks are `p1` / `p2` / `off`), so `seq.py` only plays the chime there. A
     `bright` look (one per phase) would let `seq.py` add it in one line each.
   - `scarlet_line {len, yaw, roll}`: `seq.py` calls it at the player's chest (y + 1.3) `facing entity <her> feet rotated ~ 0`
     with `yaw:90, roll:13` = perpendicular to her → player, rising 13° toward the player's right (PLAN §3.2 C8, cutscenes.md §3
     shot 11). Please confirm the preset reads `yaw` / `roll` relative to the execute rotation; `qi_band {len:120}` is called
     the same way at her chest height (y + 1.1) facing the player with `yaw:0, pitch:0, roll:0` (along her → player, CS4 E1b).
   - `petal_big` looks `whole` / `cut` / `split`: `seq.py` summons the card (`item_display`, `teleport_duration:1`), rotates it to
     face the player's eyes, then calls the look; the card is re-aimed every tick while it drifts.
5. **Fidelity note (lead, for the README).** The CS4 sheathe starts with the blade's tip 0.38 b inside the scabbard: the
   1.93 b sword cannot sit on the scabbard's axis with the tip at the mouth inside her arm span (hands at most 2.14 b apart),
   so the blade is brought onto the axis already entering (304-306, two ticks) and slid in 306-318. S2a's held-props gate
   (`test_rig.py`) holds at every tick.
