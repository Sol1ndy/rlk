# S1K requests (wip/hr-s1k; for the lead at I1 / V and the stages named)

None of these blocks S1K's hand-over; no contract value changes (`api.py` untouched). Loadcheck pending the user's EULA consent
(S1K never started the local test server; the lead runs `tools/dev/loadcheck.sh` on `wip/hr-s1k`).

1. **S4 / I1 — the A13 fail's red line runs along the player's view, not across it.** `p/a13/fail` (wip/hr-s4) calls
   `scarlet_line {len:600,yaw:0,roll:13}` `rotated as` the player: `yaw` is an offset from the execute rotation (as every kit
   preset), so `yaw:0` lays the 60-b line along the player's facing (seen end-on: a dot / a short vertical stroke). CS1 C8
   (S2b's `seq/cs1` k169) uses `yaw:90` = across the view, the + end on the player's right, rising 13° there (PLAN §3.2 C8,
   the 5 % instant death "the same red line"). Fix: `yaw:90` in S4's call (one value).
2. **S3 / I1 — the arena ambience is never called periodically.** PLAN §6.3 / §6.4: the module calls `fx/p/ambient_p1` every
   10 t near the player in P1 and `fx/p/ambient_p2` every 6 t in P2 (crimson spores, the pink mote, a firefly per 20 t; both
   at the player). In the merged build (S3 + S4 + S2b's seq.py, kit on) `ambient_p1` is called once (seq/intro start) and
   `ambient_p2` never. Suggest: in the module tick, `execute if score #ph hr matches <P1> if score #gt hr matches ..` every
   10 t `at @a[tag=player]` → `K.p('ambient_p1')`, every 6 t in P2 / the down / the gauntlets → `K.p('ambient_p2')` (both
   go to the kit's ambient pool, cap 48; `ambient_p2` is particles only).
3. **S2b — answers to requests/s2b.md 4.**
   - `scarlet_line {len, yaw, roll}` and `qi_band {len, yaw, pitch, roll}` read `yaw` / `pitch` / `roll` relative to the
     execute rotation. `scarlet_line {yaw:90, roll:13}` at the player's chest `facing entity <her> feet rotated ~ 0` = across
     the player's view, the + end on the player's right, rising 13° toward it ✓. `qi_band`'s long axis runs across the aim
     (its left / right) and the band sweeps 2.5 b along the aim: at her chest facing the player with `yaw:0` it is an upright
     band between her and the player sweeping toward the player (E1b "sweeps … from her across the player") ✓ — no change.
   - `petal_big`: the prop changes only the display's transformation (the slow rock is a left-rotation interpolation), so
     seq.py's per-tick re-aim (the entity Rotation) and the drift keep working ✓.
   - `moon_halo` brightening (CS0 E3, CS4 gaze): not possible without a contract change (`api.KIT_PROPS['moon_halo']` =
     `p1 / p2 / off`). If the lead adds a look (e.g. `p1b`), the kit adds it in one table row (`PROPS` in
     `build_mboss_hr_fx.py`: the same sprite with a brighter tint, ≈ +20 % via `custom_model_data` colour); open for I1.
4. **S4 — answer to requests/s4.md 3 (the disc card is the projectile).** `fx/prop/disc` on the item display S4 launched:
   (a) the 30°/t spin is a left-rotation interpolation (a quarter per 3 t, `fx/e/anim`), the two frames swap via
   `item_model`; the entity Rotation is never touched (the flight stays straight); (b) flat in its own frame (scale 1.4 =
   the 2.8-b hazard diameter, `api.DISC['hr']`); (c) the display gets only the anim tags `rlk_hr_fxa` / `rlk_hr_fxa_d` — not
   `rlk_hr_fx`, so `fx/clear` (pause) and the ager never kill it; `fx/uninstall` only removes the anim tags (S4 / S3 kill
   their projectiles). On a marker instead the kit puts one follower display on it (removed with the marker).
5. **SR — answer to requests/sr.md 6.** `vig` (U+EC16) is edge-only with a clear centre (144 × 81 texture, height 144,
   ascent 69: advance ≈ 256 like the six overlays); see `HR/renders/s1k_overlays.jpg`.
6. **Lead (I1 / loadcheck) — measure the dark look's light swap.** The `dark` job's last real slice (T0 − 8) re-lights the
   walk: the y-206 light layer 15 → 6 (1 976 cells) and the foot grid 15 → 9 (95 cells), plus the dome skin / decor
   lights → 0 in its first three slices (PLAN §6.5 risk: ≈ 49 chunks). If the hitch is too long, set `api.DARK_LIGHT =
   False` (fallback B: the dome / moon / lanterns only) **and** `DARK_LIGHT = False` in `tools/mboss_arena_hr_field.py`
   (the theme copies the constant — stdlib only — and `test_arena_hr.py` 1b asserts they are equal), then regenerate.
7. **Lead (README / RP README).** Fragments: `HR/s1k/readme_kit.md` (the kit / arena rows and the generation order of the 홍련
   section) and `HR/s1k/rp_readme_kit.md` (the `hr_kit` folder row, the font row `rlk:mboss_hr`, the generator row).
8. **Informational (PLAN §6.6 estimates vs. the build).** The union of cells any look changes is 23 376 (PLAN ≈ 16 k: the dome
   shell is larger and the skin light stripes and decor lights are included); the jobs are 7 092 (moon) / 7 262 (crimson) /
   6 691 (dark) commands in 4 real slices of ≤ 2 518 (limit 8 000), as boxes of equal blocks (absolute fills, block-exact
   from any source look). The build is 21 slices of ≤ 4 941 commands. 298 hidden spawn-proofing lights (level 7, the same in
   every look) keep every spawnable cell outside the walk at block light ≥ 1 even in `dark`; the walk floor is ≥ 12 / ≥ 6.
9. **Informational (kit calls).** `test_kit.py`'s calls section builds the merged module (wip/hr-s4 tools + wip/hr-s2b's
   seq.py + the kit manifest) in a temp copy: all 520 kit calls name an existing kit function with exactly its args.
