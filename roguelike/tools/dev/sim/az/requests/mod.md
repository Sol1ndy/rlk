# Requests and notes from S1-MOD (the Azhdaha module core, `tools/mboss_azhdaha/`, branch wip/az-mod)

Each item: what, why, exact names, and the local stub in place meanwhile. wip/az-mod is on wip/az-cm fd88e33 (AZ-CM
commit 2, merged in ee1e038) with `azhdaha.enabled = true` (cm.md 2.4) and builds / tests green against it
(S:az/tests_mod/run_all.sh).

## To S1-CM (framework, cm.md)

Items 1, 2 and 4 are DONE in wip/az-cm fd88e33; the module's stand-ins step aside on their own (no edit needed).

1. DONE (fd88e33). ~~The px runtime for azhdaha~~: the core compiles `F:mboss/px/azhdaha/**` from the committed
   `tools/mboss_azhdaha/stub_rig_manifest.json`; the module's marked no-op stubs (`core.px_target_stubs()`, written only
   where the file is absent or still the stub) are no longer written. The e2e suite now lands one hit through a live
   proxy (12 interactions `rlk_mb_px`, `px.set` normal in the fight, tail_only in the B3 window).
2. DONE (fd88e33). ~~`px/state {set}` lines for azhdaha~~: `px/state` carries the `#mbId mb matches 10` lines, so
   `api.FW_PER_BOSS` now resolves to the real `px/state` and `AZ:cmstub/px_state` is gone (the core's clean removed it).
3. `push/ring {r,to,kb}` is real since fd88e33; the module calls it with the cm.md 13.5 arguments at the intro blast and
   both absorbs (`{r:80,to:85,kb:4}`). Nothing to change.
4. DONE (fd88e33). ~~A missing theme leaves the entrance without `cb/prep`~~: the built-in default entrance runs
   `cb/prep` at its kind-9 zone (zid 2). The tests' WORKAROUND no longer triggers (they now lay the boss map out from the
   generated `room/cboss/azhdaha/layout` and use its kind-9 zone record and id).
5. Nothing else needed from the registry: the `azhdaha` entry as committed (+ `enabled: true`) is what the module
   reads (hp 260, atk 12, dmgMul 140, intro 160, death 140, res 0 / 5 / * , phases [100], music 1 / 2). `route` stays
   false until VERIFY (cm.md 2.4).

## To S1-FX (kit, fx.md)

6. The core calls these 107 kit paths (every one exists in fx.md; today they are empty `AZ:kstub/<path>` files, the
   first call's arguments in a comment): `hud/banner_{ab/1-2, ab2/3-4, brand/1-2, tr/1-4, end}`, `hud/{clear,cue_jump,
   flash_end,flash_white}`, `p/{brand_rune/1-4, cure, dig/1-5, emerge_spikes, front/1-5, gold_leaves, petrify_pulse,
   prism_shatter, recolour/1-4, seal_reform, shard_rain/3-4, shock_dome, stele_shatter, vortex/1-2}`,
   `prop/{arena_crystal/1-5, glyph/1-4, seal_prism, seal_stele, shard/1-4, water_sheet/1-5}`, `snd/{absorb_burst/1-4,
   absorb_roar, absorb_vortex/1-4, b3_emerge, b3_rise, b3_sink, brand_apply, brand_tick, cleanse, death_fall, death_seal,
   death_sting, intro_drone, intro_roar, intro_thump, jump_cue, msg_chime, seal_shatter, shard_pick, shard_spawn,
   slide_lift, slide_wave, slide_wave6, stele_break}`, `tele/{clear, crater, disc, field, field_clear, field_end,
   glyph_circle, ring, strip, wave}`, `clear`, `uninstall`. The list is `ls F:mboss/azhdaha/kstub` on wip/az-mod.
   Checked against the real kit (wip/az-fx 35adb2e overlaid on a scratch copy, `build_mboss_az_fx.py --skip-rp` then the
   module): the module builds with it, every kit call resolves (check_refs 0 missing from the module), check_mboss_pack 0,
   lint_mc 0 new in module files. One fix was ours (wip/az-mod 38242b7): the brand badge is `K.brand_badge(el)` per
   brand element (the core had called `K.badge(9, True)`). Nothing to change in the kit.

## To S1-HARN / I2a (harness)

7. azsim / azfair names confirmed against the module: `#azPat #azPh #azTr #azBur #azLeg #azTail`, `azBrT` / `azBrE`
   (+ `azBrS` stacks, `azBrC` tick clock), `rlk_az_shard`, test ids 90-93 / 60 / 62, `#mbId` 10; no separate anchor
   entity (the body husk is the anchor, `anchor_tag` absent). `load_zone()` on the committed stub manifest gives the
   module's own 3.6 / 3.0 / 9.0 / -4.8 / 3.5. `azsim.chapter_entry` needs item 4 (or the same WORKAROUND) to reach a gate.
7b. The M0 suites `S:mb3/tests/run_all.sh` on wip/az-mod: every mcsim suite passes, check_nbtpath / check_mboss_pack 0;
   vcheck's "new" findings in module files are only the accepted classes (macro: `function ... with storage` calls read
   as "called without args"; lint: `time query gametime`), the rest are wip/az-cm's (`ar/*/full_rim`, `ar/*/tp_in`,
   `arena/cp_test/*`, `music/*`, `px/dup|hit`) for its baseline. Two harness notes. (a) `gen_check.py`'s chain has no `build_cboss_rooms.py` / `build_mboss_azhdaha.py`, so the core's clean removes
   the five marked px stubs (item 1) and they show as "gone"; S:az/tests_mod/gen_check_az.py runs the az chain (green).
   (Measured on wip/az-cm 51fc332; since fd88e33 the core compiles `px/azhdaha/*` itself, so this diff is gone.) (b) `ident.py` pins `REPO = S:mb3/wt_core`, which no
   longer exists; pointed at any worktree of the repo it passes (IDENTITY CHECKS PASSED on wip/az-mod).

7c. **`azsim.py selftest` fails 'chapter entry on cproto' against wip/az-cm fd88e33** (harness, not the pack; cproto
   and azhdaha alike). Two fixes, both proven by `S:az/tests_mod/harn_selftest_local.py` (the same selftest with them as
   marked local stubs: 0 failures): (1) `azsim.chapter_entry` puts the entrance marker at zid 9, but the generated
   entrance runs `mboss/cb/prep` only at its kind-9 zone's zid (`room/cboss/<id>/build`: `execute if score @s zid
   matches 2 at @s run function rlk:mboss/cb/prep` for the default entrance) - build the marker from the kind-9 record of
   `room/cboss/<id>/layout` (`rlk:room cur.zones[]`, zid = its `id`, data = the record); (2) the framework's proxy poll
   (`execute as <uuid> if data entity @s attack run function rlk:combat/input/poll_attack`, `px/<id>/poll`) needs the
   interaction click NBT modelled: `if|unless data entity <sel> attack|interaction[.<path>]` tests e.data and
   `data remove entity <sel> attack|interaction` removes it (S1-CM's `tests_cm/lib/cmsim.py` does exactly this; mcsim
   answers "true" and then raises `KeyError: 'attack'` in `poll_attack`). The S1-MOD suites carry the same two rules
   locally (`azt.CountSim`, `azt.entrance`).
   **Done** (after the AZ-CM merge d5185ec on wip/az): both fixes are in `S:az/harness/azsim.py` (`chapter_entry` from
   the layout, `attack` / `interaction` in e.data); `azsim.py selftest` 0 failures, no longer KNOWN. The same azsim
   change models `data modify storage .. set from entity <sel> Pos|Rotation` (AZ-CM PERF-4 `mv/plpos`; mcsim stored
   None and every ai/sample, mv/local, hz/hit_mask call raised TypeError) and adds `azsim.moved(s)` (cmsim's helper:
   `#mbPlG -1` after an in-tick test teleport); `azt.place_player` calls it.

## To S2 authors

8. s2.md 16 lists the names the core added (services 27 / 28 / 30, `#azReq*`, `#azQ4`, the core-typed lines and
   message, the brand objectives, `az.subx`, `api.REQ_HOOKS`, `ai.FIELD_AREA_WHEN`, the lower-case bg functions, the local
   stubs). The empty pattern stubs keep the binding lengths; replace their emit bodies and keep the records' ids / keys.

## Answers to requests/arena.md (S1-ARENA -> S1-MOD)

9. Item 6 (moved points): `api._THEME_FALLBACK` copies no glyph / crystal / stele-glow points (s2.md 5.1: the fallback
   has no entrance glyphs and no crystals), and with the theme present the core reads `entrance_layout()` / `props()`
   from the module, so nothing to refresh. Checked on a scratch copy with wip/az-arena 174aeef + the kit: core -> arena ->
   cboss rooms -> module build, no theme warning, 765 functions, check_mboss_pack 0, the module validators 0.
10. Item 8 (water sheet orientation): done in wip/az-mod 38242b7: the 90 deg x rotation applies only while the kit is
   absent (the vanilla pane stand-in); with the kit (`api.KIT`) the `az_kit/water` plane is summoned unrotated.
