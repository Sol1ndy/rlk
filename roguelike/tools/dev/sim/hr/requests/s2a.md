# S2a requests (wip/hr-s2a = 0c88e7f; for S2b, S3 / S4 and the lead at I1 / V)

None of these blocks S2a's hand-over or another stage; no contract value changes (`api.py` untouched).

1. **Loadcheck pending the user's EULA consent (lead).** The local test server was never started (PLAN §0.1 question 8);
   every static gate ran (rplint 0, two builds identical, regen_d0 → only S2a's files, check_mboss_pack 0, `api.py --check`,
   atlas 12.713 M ≤ 13.2 M, the four checkers, `test_rig.py` 76/76 with `--rebuild`). Run the rig's loadcheck at I1 once consent is recorded.
2. **Checker baseline: new instances of two known kinds, all in S2a's declared outputs `F:boss/scarlet/rig/**` (I1).**
   `mb/lint_mc` "bad target '<uuid>'" × 10 778 (every key / look line addresses its part by UUID, the kind the base already has
   192 713 times for the other rigs) and `check_macro` "rlk:boss/scarlet/rig/anchor/r/get needs ['a', 'c', 't'] / anchor/r/go
   needs ['p'] but called without args" × 9 (`function … with storage rlk:hr rig.q`, the shape of arlecchino's 7 + 1 in the
   base). `check_refs` / `check_nbtpath`: nothing new from the rig (the 2 refs + 5 macro lines of `F:mboss/ar/hr_field/*` are
   D0's, present at 5d2c3ac).
3. **For S2b — the cinematic clips (`tools/scarlet_cine.mjs`, shape in `tools/scarlet_rig_api.md` §6).** `export const CLIPS =
   [8 clip objects]` with exactly the names `api.CLIP_OWNER` gives S2b; import the helpers / pose families from
   `./scarlet_clips.mjs` (`K B SW ST ST2 CROUCH LOW AIR LOCK DOWN H_POSE DEFAULT_POSE F_*`). The S2a clips hand over in these
   poses: `g_deflect` ends in `LOCK` (= `repel` tick 0), `down` is `DOWN` (= `lead_down` tick 0), `ev_give` / `ev_toast` start
   in `H_POSE` (= the last pose of `ending`, PLAN §3.7 H). The same gates apply to the cine clips (floor at every compiled tick,
   ≤ 120°/t, cull); `lines: {tick: [commands]}` adds commands to a tick's key file (e.g. a look call). `ev_give` hides the
   sword and the scabbard at its `toss` (30): the event's thrown-sword display takes over at `anchor/hand_r` with
   `rlk:mboss/scarlet/item_sword` at scale 1.5 (`item_display:"none"`; the scabbard runs along the model's (+X, +Y) diagonal,
   API §7).
4. **For S3 / S4 — clip ends the module should know.** `g_tell` (4), `g_x` (14), `g_leap` (17), `g_vert` (18) end vanished
   (`vis` 0: every part at scale 0 about her body centre, not the `state/hidden` flag): play the next clip or call
   `state/hidden` there. `g_brim` holds 6-14 (loop), `down` loops 0-40, `kipup` ends standing with the hat worn and the blade
   low. `a4` / `g_leap` / `g_vert` / `g_dive` raise her in the clip (a flip about her centre, up to +1.6 b): the module's
   own lift is added on top. Clip events are played ticks: `play/<clip>` before `rig/tick` in the same game tick runs event e
   e game ticks later.
5. **Suite move (V).** `S:hr/tests/test_rig.py` reads `HR/tests/lib/mcsim.py` (vendored, unchanged; S3 owns `lib/`) and the
   paths of S2a's worktree / RP by default (`--dp`, `--rp` or `HR_DP` / `HR_RP` override): S2b points it at its own tree.
