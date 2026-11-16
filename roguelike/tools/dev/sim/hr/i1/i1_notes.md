# I1a notes (lead's integration step; `WT` = HR/wt_hr, branch `wip/hr`)

## 1. Worktree
- `git -C /home/user/rlk worktree add HR/wt_hr -b wip/hr wip/hr-d0` → base 5d2c3ac (11-05; `df -h /` 1.5 GB free before, 1.3 GB after).

## 2. Merges (each `git merge --no-ff`, in the brief's order)
| # | branch | head | merge commit | git conflicts |
|---|---|---|---|---|
| 1 | `wip/hr-s4` (S1 1945bce → S3 eb3e271 → S4 d65ea28) | d65ea28 | 5f93747 | none |
| 2 | `wip/hr-s2b` (S2a 0c88e7f → S2b fb97b3b) | fb97b3b | e1fd22a | none |
| 3 | `wip/hr-sr` | ad912ff | 0ae9bf8 | none |

Path overlap check before merging (`git diff --name-only 5d2c3ac <branch>`): s4 ∩ s2b = 0, s4 ∩ sr = 0, s2b ∩ sr = 0 files,
so no textual conflict was possible. The merged tree is not yet consistent as generated output: the S3/S4 outputs were built
against the stub rig (`rig_stub/**` 138 files, stand-in sequences `core/sq/**` 28 files) and without `seq.py`'s services;
step 4's regeneration replaces them (generated files are never hand-edited).

## 3. RP
- `cp -r S:ar/rp_i1 HR/rp_hr` (48 MB), then from `R:` `node tools/build_scarlet_rig.mjs --resourcepack HR/rp_hr`: 29 parts, 47 clips
  (0 stand-ins; cine from `tools/scarlet_cine.mjs`), 2109 key files, 22 050 keys, 2629 rig functions (6.57 MB), 78 models, 48 sprites
  0.084 M px, elements at rest 2304 (8.5 s). The datapack side (`boss/scarlet/rig/**`, `tools/scarlet_rig_manifest.json`) came out
  byte-identical to the merged commit (`git status` clean).
- Hashes vs `HR/rp_s2b`: whole pack **08625ceee52c79cb91d03294851d0a099df18315** on both (= S2b's reported hash); the 204
  `assets/rlk/**/mboss/scarlet/**` files hash 6609c88abed5133a31a1ba3e46584848de1a3a21 on both; `diff -rq` empty.
  `HR/rp_s2b` removed (`rm -rf`).

## 4. Regeneration (commit 508725e)
- Order: rig (step 3, `--resourcepack HR/rp_hr`) → `bash HR/tools/regen_d0.sh R:` (= `regen_all.sh`: core → arena → cboss_rooms →
  proto → cproto → spproto → guardian → butterfly → fieldgen → az_fx → azhdaha → ap_fx → apep → rift → tk_fx → tachy → kn_fx →
  arlecchino → check, + bf / fg kits `--skip-rp`) → `python3 tools/build_mboss_scarlet.py` → `check_mboss_pack.py`.
- Module: `mboss scarlet: 917 functions (S3 270, S4 413, seq 234); patterns a1 a2 a3 a4 a6 a9 a10 r1 r2 r3 a8 a13; 166 stale
  removed` (= `rig_stub/**` 138 + `core/sq/**` 28; `core/gs/**` was already gone on wip/hr-s4). Notes left: kit missing, arena
  theme missing (S1K, I1b). Changed module outputs (`F:boss/scarlet`, `git diff --no-renames --name-status 0ae9bf8 508725e`):
  121 modified (every `api.rig` call `rig_stub/…` → `rig/…`, stand-in `core/sq/…` → `seq/…`: 98 rig only, 20 sequence only,
  3 both, nothing else), 234 added (`seq/**`), 166 deleted; the commit's other two modified files are the sources
  `T:mboss_scarlet/seq.py` and `T:dev/regen_all.sh` (123 modified in all; corrected in verification round 1, m1).
- **Conflict found by the gate (generator fix, I1):** `check_mboss_pack` → 1 problem: `boss/scarlet/seq/lead_stand/start:4 no
  functions for dynamic reference function rlk:boss/scarlet/seq/lead_stand/g/$(g)`. The pack checker (S1's, shared by every
  boss) resolves a `$(…)` function reference only as a numeric family `<ref><n>` (every other dynamic reference in the scanned
  trees is numeric: `hz/p/c/$(k)`, `pj/h/$(hr)`, `arlecchino/fx/hud/l/$(id)`); S2b's string arg `g` ("a8" / "a13") was the only
  exception and was invisible on S2b's / S4's branches (`seq/**` is written by S3's generator, absent there). Fixed in the
  generator `T:mboss_scarlet/seq.py` (not by weakening the shared checker): `start` stores the arg (`$data modify storage
  rlk:hr seq.g set value "$(g)"`, S2b's `seq.*` key, removed by S3's `uninstall`) and calls `g/a8` / `g/a13` through two static
  `execute if data storage rlk:hr seq{g:"…"} run function …` lines — the same `#sq_g` values, now checkable by
  `check_mboss_pack` and `check_refs`. → 0 problems.
- `T:dev/regen_all.sh`: after the Arlecchino pair, `[ -f tools/build_mboss_hr_fx.py ] && run tools/build_mboss_hr_fx.py
  --skip-rp` and `[ -f tools/build_mboss_scarlet.py ] && run tools/build_mboss_scarlet.py` (PLAN §9.1; the kit line is a no-op
  until S1K merges).
- Second full regeneration (`regen_d0.sh`, now incl. the module): `git status` and `git diff` hash identical (c1b1110f…).
  `check_mboss_pack` 0 problems (4 mid, 4 chapter, 2 special, 7 arenas); `api.py --check` ok.

## 5. Enable her (commit 21e853f)
Registry `scarlet.enabled` → true (icon unchanged: `minecraft:iron_sword` / model `minecraft:iron_sword` until I1b); the entry's
`_doc` sentence "I1 turns enabled on." → "Enabled since I1 (I1a): rift weight 10; the icon model stays vanilla … until the kit's
gate icon (I1b)." Regenerated (`regen_d0.sh`): **26 changed + 3 new `F:mboss` files, nothing else** (= S1's measurement):
- changed: `mboss/d/{aux_hit,bars,cleanup,death_start,death_tick,hz_vis,incoming,intro_tick,on_hit,pause,pj_end,reload,resume,
  spawn,test,test_help,tick,uninstall}` (18), `mboss/register`, `mboss/sp/gate`, `mboss/sp/prep`, `mboss/sp/reward`,
  `mboss/test/{help_pattern,help_rift_id,help_special,help_special_ch}`;
- new: `mboss/cb/inc/scarlet`, `mboss/sp/g/scarlet`, `mboss/sp/pp/scarlet`.
All on the contract §5 allow-list (`d/*` incl. the uninstall dispatch, `register`, `sp/gate`, `sp/prep`, `sp/reward` (FN output),
the four `test/help_*`, the three new files). 29 lines added, 4 removed — the removed ones are `register`'s `sreg` / `sbyid`
lines (rewritten with her record appended; the 타키 / spproto records are byte-identical substrings of the new lines) and
`#spN mb 2 → 3`, `#spRoll mb 1 → 2`. `sp/reward`: `sp/lvup` line 14, the hook (`api.RW_HOOK_LINE`) line 16 exactly once, `#spPk`
line 17. Her record ends `…,winWord:"도전 성공",poof:0b,…`. `check_mboss_pack`: 4 mid, 4 chapter, **3 special**, 7 arenas, 0
problems. (Contract §5's wording is corrected to this list under request s1-4, §6.)

## 6. Requests (every item of `HR/requests/{s1,s2a,s2b,s3,s4,sr}.md`)
Dispositions: **applied** (what / where / how verified), **verified** (checked on the merged tree, nothing to change), **I1b**
(needs S1K), **R / F / S5 / V** (why), **declined** (why), **no action** (informational, nothing to change). Generator
changes are in commit "Scarlet I1a: requests …" (§9); suite changes live in `HR/tests` (not in the repository until I1b
moves them).

| id | item | disposition |
|---|---|---|
| s1-1 | `test_m0diff` B: `#mbBarOff` | **applied**: added to `NEW_FAKE` in `R:tools/dev/sim/az/tests_cm/test_m0diff.py` (comment names FN-f); failure set at the run_all gate = README 0-9's (§8) |
| s1-2 | check_macro `mboss/test/swon:3` (with storage) | **applied**: accepted in `HR/i1/checker_accept.md` (known kind) |
| s1-3 | `test_special_hr` ident + R2b after I1 | **applied** (lead's decision): skipped while her entry is enabled (`SC_ENABLED`); also adapted the S1-era "disabled tree" checks: R13 disables her explicitly, the enable section diffs a forced-DISABLED variant against the tree (E4 / E8 / E9 / E10); `HR/tests/ident_hr.py` replaces ident |
| s1-4 | contract §5 wording | **applied**: §5 now lists the measured 26 changed + 3 new (incl. `sp/reward`) |
| s1-5 | FN-e `dead_voxel` 6075.95 t vs 6076 | **declined** (no change): 6076 ≥ the real length, never cuts a track; lowering it would break Arlecchino's `music_len` |
| s1-6 | stage helpers' shared scratch paths | **no action**: done by the lead on 11-05 before I1 (contract §7, per-worktree folders) |
| s2a-1 | loadcheck of the rig | **verified**, nothing to change: the lead's loadcheck of `wip/hr-s2a` 0c88e7f (0 failures, `HR/lc/s2a.txt`) + the I1a loadcheck `hr_i1a` (0 failures, §8) |
| s2a-2 | checker baseline (rig `bad target` lint, anchor `with storage` macro) | **applied**: accepted (`checker_accept.md`) |
| s2a-3 | for S2b: the cine clip format | **no action**: delivered by S2b; the merged rig builds 0 stand-ins |
| s2a-4 | for S3 / S4: clips that end vanished | **no action**: S4 calls `state/hidden` at those ends (s4-6); pat_ghost green |
| s2a-5 | suite move | **I1b** (the suites move; `test_rig.py` takes `--dp` / `--rp`) |
| s2b-1 | loadcheck of rig + `seq/**` | **verified**, nothing to change: the lead's loadcheck of `wip/hr-s2b` fb97b3b (0 failures, `HR/lc/s2b.txt`) + the I1a loadcheck `hr_i1a` (0 failures, §8; `seq/**` first exists on the merged tree) |
| s2b-2 | checker baseline (+11 546 `bad target` in `rig/c/<cine>/k/*`) | **applied**: accepted |
| s2b-3 | running `seq.SERVICES` (S3) | **verified both ways** (§6a) + **fixed**: `seq.py` `lead_stand` string dispatch (§4), the restart clock (s3-10) |
| s2b-4 | for S1K: `moon_halo` bright, `scarlet_line` / `qi_band` frame, `petal_big` | **I1b** |
| s2b-5 | the CS4 sheathe note | **I1b** (README section merge) |
| s3-1 | A9 lock 21 vs clip `lock` 22 | **declined** (lead's decision): both inside the 6-8 t lock rule, nothing gameplay-visible |
| s3-2 | S1's ident on later trees | **applied** = s1-3 |
| s3-3 | check_macro `p/a9/k/27`, `test/help` | **applied**: accepted |
| s3-4 | SR's names / calls | **verified** (§6b) + **applied**: `test_reward.py` section `real` runs the event against SR's real files |
| s3-5 | fold S3's tags / fake players into the contract | **applied**: `api.CORE_FP` (+ `api.CORE_CONSTS`) / `api.TAGS`; `s3lib.FP` = `api.CORE_FP` (same order), `LOCK_T` / `PROBE_T` / `shield.PIP_T` / `core.TAGS_ALL` read `api.TAGS`; all 47 856 function files byte-identical (hash list before / after), `api.py --check` ok, the stub manifest unchanged; contract §2 lists them + the stage-private tags |
| s3-6 | S2b: banner on `#warn`, `#sq_sig` | **verified** (§6a) |
| s3-7 | S1K: look jobs keep `arjob`, `job_tick` line | **I1b** |
| s3-8 | CS4 distance (real `seq/ending`) | **applied**: `test_scarlet.py` section `cs4` (C41): test 28 → CS3 → kill → CS4 on the full core path, player pinned, distance over ending ticks 300-1041 within 3.5-6 b |
| s3-9 | command counts | **re-measured** (§8 cost) |
| s3-10 | resume ordering | **fixed** (`core.py`): a sequence (re)started by the resume hook or `/reload` (`core/re/{cs1,sq1,g,lead}`) holds its clock one tick (`#sq -1`), so the first module tick shows clip tick 0 at `#sq 0` (S2b's clock contract); new `core/re/lead_go`; `test_scarlet` R6 / R8 expect `#sq -1`, new R8b / R10b / R11b check `#sq` = `hrRigT` every tick after the restarts |
| s4-1 | `test_scarlet` P8 + B1 kit5 | **applied**: P8 exempts the ghost windows (body tagged `rlk_hr_ghost`), new P8b (ghost form in P2 always invulnerable); B1 kit5 waits for the revive stance (`#rvw` / lead) when `ULT5_LETHAL` is false |
| s4-2 | disc speed | **applied**: `api.DISC['speed']` 1.75 (7 sub-steps; `g/disc/throw` `spd:17`), `p_ghost.py`'s comment formula and `pat_ghost.py` D3 use the flown `ceil(speed / 0.25) · 0.25`; contract §7 |
| s4-3 | S1K: the disc card | **I1b** |
| s4-4 | cut hz options (`kbdir 1`) | **no action**: recorded in contract §7 (informational) |
| s4-5 | landings after the dive | **no action**: recorded in contract §7 (PLAN §5.5 text) |
| s4-6 | clip ends | **no action** (informational) |
| s4-7 | checker baseline | **applied**: accepted (no S4 line) |
| s4-8 | tick cost | **re-measured** (§8) |
| s4-9 | core interplay (double darkness lift / banner off) | **no action**: idempotent by design |
| sr-1 | README fragments, suites move | **I1b** |
| sr-2 | `vBig` counts down only in F5 | **R** (facts: `vBig` decremented only in `view/ride_tick:13` and `view/sel_xhair:3`, set in every view; in 1st person / shoulder view it stays ≥ 1 after the first big title, so the 홍련일섬 vignette shows only in F5; fix = a per-tick decrement outside SR's files) |
| sr-3 | m0diff budget +0.01-0.02 | **no action**: README 0-9 known failure (numbers in §8) |
| sr-4 | the calls S3 makes | **verified** = s3-4 |
| sr-5 | `item_sword` must be in the RP | **verified**: `HR/rp_hr` has `items/mboss/scarlet/item_sword.json` (→ `rlk:item/mboss/scarlet/item_sword`); the pack ships with the datapack (release note, V) |
| sr-6 | S1K: `vig` edge-only | **I1b** |
| sr-7 / sr-8 / sr-9 | deadline timers, items.md `6초`, small decisions | **no action**: recorded in contract §7 (accepted deviations) |
| sr-10 | gate-run notes | **no action** (informational) |
| S1K's own | — | **I1b** |

### 6a. Sequence wiring, both ways (s3-6 / s2b-3 / s3-10)
| point | core side (S3, generated) | sequence side (S2b) | verdict |
|---|---|---|---|
| start args | `core/seq/repel_{60,5}` → `seq/repel/start {at:60|5}`; `core/seq/lead_stand_{a8,a13}` → `{g:"a8"|"a13"}`; each sets `#sqn`, `#sq 0`, `#sqdone 0`, `#sq_sig 0` first | `start` takes exactly `api.SEQ_ARGS` | ok (+ the `g/$(g)` dispatch fixed, §4) |
| tick order | module `tick`: `core/fight` → `core/seq/tick` (`#sq += 1` → `seq/<n>/tick` → `core/sig` if `#sq_sig ≥ 1` → stop unless `#mbSt 1` → `core/seq/end` at `#sqdone`) → `rig/tick` | clip tick e shows when `#sq` = e | ok |
| `#sq_sig` beats | `core/sig`: 4 → `shield/arm`; 1/2/3 → `#gk` 1: 15/15/15 ‰, `#gk` 2: 15/15/`core/kill`; reset to 0 | `repel/k/24` 1, `k/75` 2, `k/102` 3; `lead_down/k/29` 4; `lead_stand/k/18` 4 (= `api.COUNTER_EV`, the `refill` events) | ok |
| banner | `#warn` = `ULT60_LETHAL` (SQ1, `lead/a8`, `g/start/a8`) / `ULT5_LETHAL` (`lead/a13`, `lead/down`, `g/start/a13`) | `fx/hud/warn {on:1}` at the `dark` event (sq1 42, lead_down 64, lead_stand 52, gated by `#sq_g` 8/13) from the same two switches; `{on:0}` in every start | equivalent to `#warn` for all four switch combinations (dry kit-on build, `HR/i1/tools/warn_dry.py`); contract §3.5 places it at `dark` (S3's note said brim) — no change |
| intro skip | `core/skip_go`: `seq/intro/skip`, then `#sq 553`; next `intro_tick` → 554 | `intro/k/554` plays `intro_end` + line 11 | ok |
| ending → event | `death_tick`: `seq/ending/tick`; at `#sqdone` → `core/seq/event` (`#sq 0`, `start`) in the same tick | `ending` sets `#sqdone` at 1042 | ok |
| cancel | abort: `cleanup` cancels all 8; death: `death_start` → `core/stop_all` by `#sqn`; `/reload`: `core/re/{cs1,sq1,repel}` cancel, `core/intro/reload` cancels the intro, the lead-ins restart (their markers already died with every `rlk_mb_aux` in `mboss/init:184`); forced switches (tests) → `core/force` → `stop_all` | every `seq/**` summon carries `rlk_room rlk_mb_aux`; `cancel` kills `rlk_hr_stage` / `sqh` / `sqp` / `ev` | ok (a finished sequence keeps its one staging marker until the next start / cleanup: S2b's design) |
| seat rock | `core/deco`: summon at `api.deco()['seat_rock']` = `SEAT_POS` (884.5 201 0, the floor), rotated to the moon, then `fx/prop/seat_rock {look:"bottle"}`; `deco_seat` for the replay | the intro re-looks it by position (≤ 0.6 b) | look ok; the knee-height model is the kit's prop → **I1b** (no prop without the kit) |
| entry distance | arena start 880.5 201 31.5 | seat 884.5 201 0 | 31.75 b ≥ 10 b ok |
| resume / reload ordering | before I1: the restart's start and its tick 1 ran before the first `rig/tick` → `#sq` one ahead of the shown clip tick for the whole restarted sequence (S3 saw 69 lead-in records) | contract: `#sq` = shown clip tick | **fixed** (s3-10): `#sq -1` after the restarts; tests R8b / R10b / R11b |

### 6b. S3's event calls vs SR's files (s3-4 / sr-4)
`ev/item` = `#enh tmp 0` + `items/enh_get {id:"sword_hwamu"}` + `execute if score #enh tmp matches ..0 run items/enh_add {id}`
(star raised by `enh_add` before the item is built), the capacity check exactly as `F:root/give:4-5` (`#ol tmp` ← `rlk:pinv order`;
`>= @s invCap` → `#hrEvDrop 1`), else `items/give {id}`; the hook: `execute if score #hrEvDrop hr matches 1 at
@e[tag=rlk_body,limit=1] run function rlk:items/drop {id:"sword_hwamu"}`; `ev/buff` = `scoreboard players set @s hrMoon 1`;
`ev/title`'s buff numbers = score components of `#hrMoonAtk / #hrMoonCrit / #hrMoonSpd tmp`, set by SR's `load` (lines 678-680:
20 / 10 / 10). All as sr-4 describes; `reward.py` unchanged. New `test_reward.py` section `real` (SR's SNBT reader for this
section only): X0 def registered (model / rarity), X1 the real give once as the player (custom_data id, `item_model`, ★☆☆),
X2 the real `enh_add` (enh 1, enhL 1), X3 / X4 full at `invCap` 9 / 18: no give, the real drop at the body (rlk_ditem +
rlk_daura, +0.35 b, its `rlk:ditems` record, one notice), never lost / doubled, X5 buff (`hrMoon` 1, subtitle from load's
constants verbatim), X6 / X7 the duplicate rules on SR's scores.

## 7. New I1 suites (`HR/tests`)
- `ident_hr.py <roguelike> [--base 35b82e5]`: every file under `data/`, every generated manifest of `tools/`, `items.md`,
  `pack.mcmeta` hashed as git blobs vs `git ls-tree -r 35b82e5`; changed / new / gone files must be on the allow-list
  (contract §5 + SR's hand files of §1 + `F:boss/scarlet/**` + this boss's manifests incl. D0's `stub_rig_manifest.json`);
  prints the allowed changes by group. Merged tree: 47 907 files in scope (44 301 at the base); changed 69, new 3 606, gone 0 —
  §5 D0 arena lines 22 changed + 23 new, FN outputs 6 + 3, enabling her 24 + 3, `F:boss/scarlet/**` 3 547 new, SR 17 + 28,
  manifests 2 new; **nothing outside the allow-list**.
- `gen_check_hr.py <roguelike> --rp <RP>`: real copies (no hard links) of data / tools / pack.mcmeta + the pack under
  `HR/tests/tmp/gch_*`; G0 copy = tree; G1 every generator (core, arena, rig, [kit], scarlet, check) twice: the first run
  reproduces the tree, the second changes nothing; G2 each run writes only its owned paths (bytes + mtime of every other file);
  G5 the rig's RP side twice = the given pack; G3 `F:boss/scarlet` wiped, documented and reverse order → the tree; G4 strays
  in each owner's folders spared by the others and removed by the owner. **25 / 25** (5 min 10 s).
- Changed suites (I1 adaptations, each marked "I1" in the file): `lib/hrsim.py` (+ `lib/README.md`), `ev_dry.py`, `pat_p1.py`,
  `pat_ghost.py`, `test_special_hr.py`, `test_scarlet.py` (+ sections `cs4`, the extended `cost`), `test_reward.py` (+ `real`).

## 8. Gates (I1a, final tree)
- **Regenerate twice** (rig into `HR/rp_hr` + `regen_d0.sh` = `regen_all.sh` incl. the module + bf / fg kits): `git status`
  empty after each pass; `check_mboss_pack`: 4 mid, 4 chapter, 3 special, 7 arenas, **0 problems**; RP hash
  **08625ceee52c79cb91d03294851d0a099df18315** both passes; `api.py --check` ok (29 parts + shadow, 47 clips / 280 events,
  12 hit tables, 25 lines, 50 presets, 104 sounds, 237 568 kit px, 115 owned paths).
- **rplint** `HR/rp_hr`: **0 problems**. **atlas_px**: stitched items atlas **12.713 M** px (1425 sources) ≤ 13.2 M.
- **Checkers** vs 35b82e5 (`HR/tools/checkers.sh`, out `HR/i1/out/checkers`): refs 44 → 44 lines (new 2: D0's `full_rim:3` +
  the count 66 → 67), macro 3357 → 3375 (new 21: S2a anchors 9, D0 arena 4, SR dmg_calc 2, S1 swon 2, S3 a9 1 + help 1, SR
  update_item shift 1, count 1; gone 3), nbt 0 new, lint 193 340 → 215 670 (new 22 332: rig `bad target` 22 324 (S2a / S2b),
  SR's `time` 3 / sidebar 1 / display 1 / shift 1, the count 1, and **one new kind**: `seq/ending/start:4` `tp … facing
  entity … eyes`, valid syntax lint_mc does not parse). All classified, 0 unclassified; list in `HR/i1/checker_accept.md`.
- **Tick cost** (test_scarlet `cost`, strict count: an `execute … run X` counts X too; real rig / sequences / gauntlets, kit
  and theme still absent):

  | part | ticks | avg | max |
  |---|---|---|---|
  | P1 | 1500 | 430 | 946 |
  | P2 | 1500 | 439 | 947 |
  | A8 | 194 | 391 | 822 |
  | A13 | 258 | 414 | 827 |
  | CS1 | 212 | 256 | 499 |
  | SQ1 | 60 | 297 | 683 |
  | repel (CS2 + CS3) | 205 | 362 | 495 |
  | lead_stand | 69 | 317 | 395 |
  | **fight state** (P1 + P2 + A8 + A13 + the fight-state sequences) | 3998 | **414** | **947** |
  | intro (intro state) | 639 | 302 | 737 |
  | ending CS4 (death state) | 1042 | 229 | 641 |
  | event coda (death state) | 122 | 196 | 337 |

  Target ≤ 600 average: met (414); Apep ≈ 830 hard: met. S3 measured 352 with the stand-ins, S4 359; the real rig and
  sequences add ≈ 60-80 per tick. The kit (I1b) will add its card ager / effects: re-measure at I1b.

(The three gate items below stood after §10's decision list until verification round 1, which moved them here, §11.)
- **Loadcheck** (`RLK_DEV=S: bash R:tools/dev/loadcheck.sh R: hr_i1a`, head 66dafec): `loadcheck hr_i1a: 0 function load
  failure(s)`, exit 0, `Loaded 1870 advancements`, `Starting minecraft server version 26.3` + `Done (1.678s)` (log
  `S:mcsrv/hr_i1a.log`). The new lint kind's function (`seq/ending/start`) loads.
- **run_all** (`R:tools/dev/sim` copied to `HR/i1/sim`, outside the datapack; the vcheck baselines `lint.txt` / `macro.txt`
  added from `S:az/tests_cm/baseline` as SR did; log `HR/i1/out/run_all_i1a.log`, 366 s; the per-step outputs the log names,
  `HR/i1/sim/az/tests_cm/out/i1a_*`, now in `HR/i1/out/run_all_i1a/`, and the copy deleted: verification round 1, m4,
  §11): 34 suites ok (test_chapter,
  test_fw_az, test_fw_ap, the 23 old-path M0 suites, **gen_check**); failures = README 0-9's list only:
  - `test_m0diff`: 40 failures, **names identical to the D0 base run** (`HR/i1/out/m0diff_names/{base,s1,i1a}.txt`); with
    `#mbBarOff` in `NEW_FAKE` (s1-1) the B details no longer name it (S1's run: 16 mentions, now 0, as on the base). Budget
    (README 0-9, unchanged question): proto +6.59, guardian +5.94, butterfly +6.71, fieldgen +6.99 per tick (= SR's run:
    its `take_damage` / `dash_iframe` lines, sr-3).
  - `test_px` 4e (18); `ident` 10 (the stale 22ba247 pins).
  - The validator steps against the old pre-Apep baselines: refs 29 / 6 new (= SR's run), lint 6767 / 2959 new (= SR's run),
    macro 3097 / 519 new (SR's run 3085 / 507: +12 = S1's `swon` 1 + S3's 2 + S2a's anchors 9, all classified in
    `checker_accept.md`); check_nbtpath 0; check_mboss_pack 0. (The authoritative checker gate is `checkers.sh` vs 35b82e5 above.)
  - `gen_check` **passes**: README 0-9's "gen_check 9" item (fixed 11-03, not re-verified then) can be removed.
- **Suites** (final run on head 66dafec, `HR/i1/run_suites.sh final`, logs `HR/i1/out/final/*.log`; `--dp` / argv = `WT`
  roguelike, `--rp` = `HR/rp_hr`): **all green** — `test_rig.py --rebuild` 86 / 86; `ev_dry.py` 62 / 62; `test_special_hr.py`
  93 ok (S1's 121 minus the skipped `ident` 27 + R2b); `test_scarlet.py` 139 ok (S3's 131 + P8b, R8b, R10b × 2, R11b × 2, C41,
  Z2); `pat_p1.py` 341; `test_reward.py` 51 (41 + `real` 10); `pat_ghost.py` 186; `test_hwamu.py` 258 / 258; `test_moon.py`
  50 / 50; `ident_hr.py` pass (47 907 files); `gen_check_hr.py` 25 / 25. ≈ 1 290 checks.

## 9. Commits on `wip/hr` (never pushed; trailer as the brief)
5f93747 / e1fd22a / 0ae9bf8 the three `--no-ff` merges; 508725e regeneration with the real rig and sequences + `seq.py` dispatch
fix + `regen_all.sh` lines; 21e853f `scarlet.enabled` true; **66dafec** the requests (head). `WT` (`HR/wt_hr`) and `RP`
(`HR/rp_hr`) are kept for I1b. Suite changes and the new suites live in `HR/tests` (I1b moves them into the repository).

## 10. For I1b and for the lead
I1b (after S1K): merge `wip/hr-s1k` (`--no-ff`); regenerate (kit `--skip-rp` via `regen_all.sh`, the theme via
`build_mboss_arena.py`, then the module); the kit into `HR/rp_hr`, compare with `HR/rp_s1k`, then remove it; registry icon model
→ `rlk:mboss/hr_kit/gate_icon`; the deferred requests s2b-4, s3-7, s4-3, sr-6, S1K's own; README 0-4 (the data-pack order line
gains the module, the RP block the rig + kit commands), the section 「홍련 (`boss/scarlet/`)」 from the fragments (S1 / S2a /
S2b / S3 / S4 / SR; s2b-5, sr-1); move the suites (s2a-5, sr-1: `HR/tests` → `R:tools/dev/sim/hr/tests`, `HR/sr/srsim.py` →
`hr/sr/`, keep `HERE.parent / 'sr'`, the PLAN / wiki paths); re-run every gate incl. `test_kit.py`, `test_arena_hr.py`, the
budgets, look-job counts, the cost table with the kit, `gen_check_hr.py` (it picks up `build_mboss_hr_fx.py` when present),
loadcheck `hr_i1`; run_all from a fresh copy of the merged tree's `R:tools/dev/sim` (I1a's copy is deleted; recipe in §11
m4), deleted afterwards; the seat rock's knee height with the kit's `seat_rock` model (§6a); `test_scarlet` I2 once the lead
has decided item 1 below.
For the lead's decision:
1. **The intro's end distance** (PLAN §3.1; **open**): the real walk (0.15 b/t legs, E6-E9) covers ≈ 21 b, so a player who
   stays at `start` (31.75 b from the seat) is met ≈ 11.4 b away (11.36 b measured), while the skip stands her ≤ 7 b ("E10's
   end pose"; 6.50 b measured). Options: faster legs (she walks 136 ticks: ≈ 0.18 b/t reach 7 b from `start`), or the skip
   standing her at the walk's reachable distance, or keep (a moving player is usually met nearer). Until the decision,
   `test_scarlet` I2 compares the skip's end state with the full intro's except the distance and checks the skip's ≤ 7 b: the
   switch `I2_NEAR_OPEN = True` in `HR/tests/test_scarlet.py`, the check's label says "OPEN, lead decision 1" and the `skip`
   section prints both distances (`OPEN I2 …`). After the decision: set it to False (I2 compares every key again, `near`
   included; on today's tree that fails 5 / 5 on `near` alone) and fit I2's `st['near']` to the option taken; if the walk and
   the skip are kept as they are, leave the switch on and replace "OPEN" in the label with the decision (§11 m3).
2. **New checker kind**: `boss/scarlet/seq/ending/start:4` `tp … facing entity … eyes` (valid syntax; lint_mc's `tp` table
   lacks it): accepted at I1a; optionally teach `tools/dev/sim/mb/lint_mc.py` the shape.
3. **sr-2** (`vBig` only counts down in F5): deferred to R; the fix is outside SR's files (a per-tick decrement).
4. `wip/hr` starts from D0 (5d2c3ac), i.e. 35b82e5 + D0: the work branch's 0d65e87 (README 0-2 / 0-8 EULA record) is not in
   it; merging `wip/hr` back will meet I1b's README edits in chapter 0.
5. FYI (no change): S2b's sequences gate the banner from the same switches as `#warn` and place it at the `dark` beat
   (contract §3.5), not S3's "brim"; a finished sequence keeps its one `rlk_hr_stage` marker until the next start / cleanup.

## 11. Verification round 1 (11-05: issues m1-m4, all minor; no blocker / major)
All four were notes / suite / scratch matters: nothing in the repository changed, so there is no new commit and `wip/hr`
stays at **66dafec** (`WT` clean). Loadcheck on it again (from `R:`, `RLK_DEV=S: bash tools/dev/loadcheck.sh R: hr_i1a_f1`):
`loadcheck hr_i1a_f1: 0 function load failure(s)`, exit 0, `Loaded 1870 advancements`, `Done (1.199s)` (log
`S:mcsrv/hr_i1a_f1.log`). This round's logs: `HR/i1/out/fix_r1/`.

| id | issue | result |
|---|---|---|
| m1 | §4's "123 modified" counted the two source files | **fixed** (§4): 121 modified module outputs (+ `T:mboss_scarlet/seq.py` and `T:dev/regen_all.sh`, 123 in all), 234 added, 166 deleted: `git diff --no-renames --name-status 0ae9bf8 508725e` with and without the `F:boss/scarlet` filter; each of the 121 differs from its 0ae9bf8 version only by `rig_stub/` → `rig/` (98), `core/sq/` → `seq/` (20) or both (3), checked file by file |
| m2 | s2a-1 / s2b-1 "applied" here, "Verified, no change needed" in the I1a report | **fixed** (§6): both rows now read **verified**, nothing to change (the report's label: the lead's branch loadchecks `HR/lc/s2a.txt` / `HR/lc/s2b.txt` + `hr_i1a`); "verified" added to §6's legend (s2b-3, s3-4, s3-6, sr-4, sr-5 already used it) |
| m3 | `test_scarlet` I2 leaves her distance out of the skip-vs-full-intro end state | **open**, lead decision 1 (§10): no decision is recorded (contract §7, the brief and the requests unchanged since I1a), so I2's comparison is not restored yet. Made explicit in `HR/tests/test_scarlet.py`: the switch `I2_NEAR_OPEN = True` (its comment gives the restore step for each option), I2's label "(her distance apart: OPEN, lead decision 1)", and the `skip` section prints `OPEN I2 … the full intro ends 11.36 b from the player who stays at the start, the skip 6.50-6.50 b`; the old comment's "i1_notes §8" now points at §10. Runs on `WT`: `test_scarlet.py R: skip` all ok (`test_scarlet_skip.log`); the same section with the switch False (in memory) fails I2 5 / 5 with `same = {'near': True}` and nothing else (`test_scarlet_skip_restored.log`), so the relaxation hides exactly this one item; the whole suite 139 ok, all passed (= the I1a final run; cost unchanged: fight avg 414, max 947; `test_scarlet.log`; the `skip` run above is on the final file, after a comment-only edit) |
| m4 | the run_all copy `HR/i1/sim` (14 MB) left in place | **fixed**: its per-step outputs `az/tests_cm/out/i1a_*` (80 files, 6.5 MB, named by the log's last line) moved to `HR/i1/out/run_all_i1a/`, then `rm -rf HR/i1/sim` (the copy differed from `R:tools/dev/sim` only by those outputs and the two baselines, byte-identical to `S:az/tests_cm/baseline/{lint,macro}.txt`). For I1b: `cp -a R:tools/dev/sim HR/i1/sim && cp S:az/tests_cm/baseline/{lint,macro}.txt HR/i1/sim/az/tests_cm/baseline/ && bash HR/i1/sim/az/tests_cm/run_all.sh R: i1b > HR/i1/out/run_all_i1b.log 2>&1` (no `RP`, as at I1a), then `rm -rf HR/i1/sim` (also in `progress.md`) |

Also in this round: the loadcheck / run_all / suites gate items, which had landed after §10's decision list, moved back
into §8 (the request rows cite them as §8; text unchanged except run_all's note on the moved outputs).

## 12. I1b (11-05; brief "I1b — steps" + the lead's decisions on S1K's requests and on I1a's open points)

### 12.1 Merges (`git merge --no-ff`, in the lead's order)
| # | branch | head | merge commit | conflicts |
|---|---|---|---|---|
| 4 | `claude/exciting-pascal-ek1vuy` (the work branch; README 0-2 2 ② / 0-8 EULA record only) | 0d65e87 | 3d2370e | none (README only, untouched on `wip/hr`) |
| 5 | `wip/hr-s1k` (S1K kit + arena theme) | 1d2e877 | a0a7dff | none (0 shared paths: S1K 486 files vs `wip/hr` 3 653 since 5d2c3ac) |
The work branch can now fast-forward to `wip/hr` (0d65e87 is an ancestor).

### 12.2 Kit into the RP, comparison, removal (step 2)
- From `R:` `python3 tools/build_mboss_hr_fx.py --resourcepack HR/rp_hr`: 427 functions (429 after 12.4's two halo looks), 50 presets, 5 props, 104 sounds, 53 textures
  (0.242 M px: sprites 237 568 + gate icon 4 096), 7 glyphs; the datapack side byte-identical to the merge (`git status` empty).
- Against `HR/rp_s1k` (S1K's hash 5b4c402a…): the 177 kit files (`font/mboss_hr.json`, `items|models/item|textures mboss/hr_kit/**`,
  `textures/font/mboss_hr/**`) hash 8386b600… on both; `items.json` has rp_s1k's 1 430 sources and the rig's 48 (`rlk:mboss/scarlet/*`),
  the rig's at index 1377-1424 **before** the kit's 53 at 1425-1477 (the rig was in `HR/rp_hr` first; "+ the rig's 48" here said
  appended until verification round 1, m5, §14); `diff -rq` shows only the rig folders and the atlas. Whole pack after the kit
  67c4190c… (4 785 files).
  `HR/rp_s1k` removed.
- Registry `scarlet.icon` = `{item: minecraft:iron_sword, model: rlk:mboss/hr_kit/gate_icon}` (+ the `_doc` sentence); regenerated:
  only `F:mboss/register` (her record's gate model in `sreg` and `sbyid`). Commit 00e6489.

### 12.3 Regeneration with the kit and the theme (step 1; commit 5e6c963)
`bash HR/tools/regen_d0.sh R:` (= `regen_all.sh`, incl. `build_mboss_hr_fx.py --skip-rp` and `build_mboss_scarlet.py`, + bf / fg kits):
the module sees the kit manifest and the theme: 1 139 functions (S3 272, S4 413, `seq` 454; was 918) — kit calls, look jobs, decor
props; only `F:boss/scarlet/**` changed (217 modified, 15 deleted, 236 new; the 15 = 14 re-cut sequence bucket files `seq/*/b/*`
and `p/a6/k/12`, which held only its comment while its line-12 call now sits in `p/a6/tick` — the commit message's "15 sequence
bucket files re-cut" is corrected here, verification round 1, m5, §14); the arena outputs were S1K's
committed ones (unchanged); `check_mboss_pack` 4 mid / 4 chapter / 3 special / 7 arenas / 0 problems; `api.py --check` ok; a second
full run: the same tree (8fdfdce4).

### 12.4 Requests and decisions (step 3 + the lead's decisions; commit 78e827f)
| id | item | disposition |
|---|---|---|
| s1k-1 | A13 fail `scarlet_line` along the view | **applied**: `p_ghost.py` `yaw=90` (+ its comment); `p/a13/fail:7` now `{len:600,yaw:90,roll:13}` |
| s1k-2 | ambience never called periodically | **applied** (`core.py`): `core/amb` after `core/state` in `core/fight`: `#t = #clk`; `#ph 1` → `core/amb1` (`#t %= #c10`, at 0 `execute at @a[tag=player] run function …/fx/p/ambient_p1`); `#ph 4..9` minus 5 / 8 (A8, down, P2, A13) → `core/amb2` (`#t2 6`, `%=`, `ambient_p2`); none in a sequence; written only with the kit on. Cost re-measured (§13) |
| s1k-3 + s2b-4 | brighter halo for CS0 E3 / CS4 | **applied**: `api.KIT_PROPS['moon_halo']` + `p1b` `p2b`; kit `PROPS` rows carry a tint (`HALO_BRIGHT` 1.2, `HALO_TINT` = round(255 / 1.2) · 0x010101 = 0xD4D4D4 on `p1` / `p2`, white on `p1b` / `p2b`: a `custom_model_data` tint only multiplies, so "brighter" needs the base below white — the default halo is 17 % darker than S1K built it, **for the lead's eye**); `seq.py` `halo(bright)` reads the arena record `rlk:mboss look_hr_field` (moon → p1b / crimson → p2b, back to p1 / p2; dark: untouched) at intro 112 / 146 and ending 690 / 780, and restores in `seq/intro/skip`, `seq/intro/cancel`, `seq/ending/cancel`; contract §7. The kit's prop demo runs 140 t for the halo's five looks |
| s2b-4 (rest) | `scarlet_line` / `qi_band` orientation, `petal_big` looks | **confirmed** by S1K (s1k-3: `yaw` / `pitch` / `roll` relative to the execute rotation, so S2b's CS1 C8 `yaw:90, roll:13` and CS4 E1b `qi_band {yaw:0}` read as planned; `petal_big` changes only the transformation, so `seq.py`'s per-tick re-aim and drift hold); nothing to change, `ev_dry` / `test_kit` green on the merged tree |
| (found) | decor props never followed the look | **fixed** (`core.py`): before, only the spawn (p1 / bud) and `core/deco_re` (halo by phase) set them, so the halo stayed white-blue and the lotus buds through P2 and the darkness (PLAN §6.4 / §6.5 "kit props" rows: p2 / bloom, off). `core/look/go` re-looks halo + lotus with each job (`DECO_LOOK`: moon p1 / bud, crimson p2 / bloom, dark off / bloom); `core/deco_re` spawns the lotus of the phase |
| s1k-4 / s4-3 | the disc card | **verified** on the merged tree: `test_kit` props (two frames swapped, quarter turns per 3 t by `left_rotation` interpolation with `interpolation_duration:3`, the entity's Rotation untouched, dressed in place, the anim chain stops with the last prop; `fx/clear` keeps props and followers) — green |
| s1k-5 / sr-6 | `vig` edge-only | **verified**: `textures/font/mboss_hr/vig.png` 144 × 81: centre half alpha 0 (max 0.016), outer 10 % band mean 0.54; `test_kit` rp section (glyph sizes, U+EC16, font ends with `minecraft:default`) green |
| s1k-6 | the dark look's light swap | **measured** on the real server (12.5 below): no slice tick near 100 ms → `DARK_LIGHT` stays true |
| s1k-7 | README fragments | **applied** in step 4 (12.6) |
| s1k-8 / s1k-9 | job sizes / kit calls (informational) | **no action**; re-measured (`test_arena_hr` 4d / 5b): look jobs moon 7 094 · crimson 7 263 · dark 6 692 world commands in their 4 real slices (max 2 518 ≤ 8 000; + the last slice's `done` call), union 23 378 cells, build 21 slices max 4 943 (S1K: dark 6 691, build 4 941: the seat clearing moved, 12.4.1); kit calls: `test_kit` calls section on the merged tree's own module |
| s3-7 | `job_tick` line, `arjob` during jobs | **verified**: `mboss/arena/job_tick` has `…arjob{aid:"hr_field"} … run function rlk:mboss/arena/hr_field/tick`; `arjob` is removed only by the job's last slice (`done`) / `abort` (2 `hr_field` lines) |
| s2a-5 / sr-1 | suites move | **applied** in step 5 (12.7) |
| s2b-5 | CS4 sheathe note | **applied** in the README section (칼 꽂기) |
| decision 1 | the intro's end distance | **applied** (12.4.1) |
| decision 2 | `tp … facing entity … eyes` lint | **no change**: stays accepted (`HR/i1/checker_accept.md`) |
| decision 5 | README 0-9 gen_check 9 | **applied**: dropped with the reason (12.6) |
| sr-2 | `vBig` only counts down in F5 | stays with R (I1a §6 facts) |

#### 12.4.1 Lead decision 1 (the intro's end distance)
- `api.SEAT_POS` (884.5, 201, 0) → **(884, 201, 5)**, the theme's copy `mboss_arena_hr_field.SEAT_POS` too (S3's spawn, the intro replay's
  tp, `api.deco()['seat_rock']` → the theme's `DECO`, S2b's `rock()` all read them): 5.02 b nearer `start` on the `start` → moon line
  (0.06 b off it; the old seat was 0.09 b off), 26.73 b from `start` (was 31.75), 5.0 b from C. (Verification round 2, §15: the
  figures of this item were the simulator's until then — the commands wrote the seat `884 201 5`, which the game block-centres to
  (884.5, 201, 5.5): 26.31 b from `start`, the walk ending ≈ 5.91 b, the nearest non-air cell 2.00 b. Since round 2 they write
  `884.0 201 5.0` (`api.xyz`), so the game uses (884, 201, 5) and the figures here hold in game.)
- The walk: S2b's leg ran while she was ≥ 8.2 b away (`#mbDist ..81` → no leg), so it stops anywhere in 7.0-8.1 b: from 26.73 b the
  16th leg leaves 7.53 b and no 17th leg runs (the lead's "≈ 5 b" alone would have ended at 7.53 b > 7). The leg now runs while she
  is more than 7 b away (`..70`, the skip's `near7` rule): 17 legs (the clip's two walk windows, 312-392 and 444-484) end 6.33 b from a
  player at `start`. Speed and legs unchanged (1.2 b / 8 t).
- Nothing of the arena on the spot: within 1.8 b of (884, 5) no block at y 201-205 in any look (grass / light-grid cells nearest at
  2.1 b); the floor under it mycelium / pale moss (crimson nylium / nether wart in P2). The seat clearing (`SEAT_CLEAR` 1.8: no grass,
  no grid light) moved with it: `l/{moon,crimson}/3`, `l/dark/9`, `s/3` changed (+ one grass cell re-rolled at (862, 201, −2)).
- Knee height: the stone's top 0.75 b (kit `SEAT['rock']`, 1.5 × 0.75 × 1.1, translation 0.375) under her seated pelvis 0.96 b
  (`scarlet_cine.mjs` `SEAT`: "sitting at her knee height (the stone's top ~0.75 b)").
- The opening still reads: `HR/renders/i1b_intro_open.jpg` (`HR/i1/tools/intro_render.py`: S1K's voxel renderer + the real rig at intro
  ticks 0 / 20 from the rig's debug pack (`HR/i1/dbg`, deleted after), composited with an alpha matte, from the player's eyes at `start`, yaw 180, pitch
  −9, fov 70): she sits under the moon, back to the player, 19 px tall (D0's seat 16 px) — the far figure under the moon of the opening
  wide (the footage tile below it).
- `test_scarlet` I2 restored (`I2_NEAR_OPEN = False`, every key incl. `near`): the full intro ends 6.34 b, the skip 6.34-6.50 b. In the
  sim this needed `hrsim`'s tag fix (12.7): with the vendored `cmsim`, `mv/ok` refused every grass cell, the walk stopped after 5 legs
  (20.73 b) — a sim-only artefact (the game lets dry grass through `#rlk:dash_pass`).

### 12.5 s1k-6: the dark look on the real server
`HR/i1/tools/darkcheck.sh` (a copy of `tools/dev/loadcheck.sh`: the same env, server dir, `.lock`, java kill; backs up `world` and
`server.properties` and restores both; `pause-when-empty-seconds` 0 for the run since no player joins), on the merged tree (the requests
applied): 26.3 server, console through the stdin FIFO, `forceload add 832 -40 928 56`, the arena build, then each real slice run alone
followed by > 100 idle ticks and `/tick query` (P99 of the last 100 ticks = the max = that slice's tick), then the whole look jobs.
Log `HR/i1/out/darkcheck_server.log` (+ `darkcheck_1.txt`): 0 function load failures, `Loaded 1870 advancements`.

| what | P99 (ms) |
|---|---|
| idle (after start) | 9.9 (avg 5.2) |
| build (21 slices) | 61.4 |
| `dark` slices alone: 0 / 3 / 6 / 9 (9 = the walk light layer 15 → 6, foot grid 15 → 9) | 3.9 / 8.6 / 4.3 / 2.9 |
| `moon` slices alone: 0 / 1 / 2 / 3 (3 re-lights 6 → 15) | 3.3 / 4.1 / 2.8 / 6.9 |
| whole jobs: dark (from moon) / moon / crimson / dark (from crimson) / moon | 17.2 / 4.7 / 5.6 / 22.1 / 23.5 |
The whole-job windows include the forceload churn (the job's `done` drops the arena's forceload outside a run, the script re-adds it
before the next job), so they are upper bounds. No tick near 100 ms → **`DARK_LIGHT` stays true** (no fallback B). The client's
re-light / chunk redraw cannot be measured on a headless server: the README section names it as the thing to watch in game.

### 12.6 README and RP README (step 4; the lead's decisions on the README)
`R:README.md` (the handover document, in its own Korean style; 0-1, 0-10 and the RP README's §6 row are left for the release):
- **0-3**: `boss/{…,tachy,scarlet}/`; the generator table: `mboss_arena_{…,hr_field,…}.py`, a new row `build_mboss_scarlet.py`
  (`mboss_scarlet/`) + `build_mboss_hr_fx.py` + `build_scarlet_rig.mjs` (+ `scarlet_cine.mjs`) → `boss/scarlet/**`, RP `mboss/scarlet` ·
  `hr_kit`, font `mboss_hr`.
- **0-4**: the data-pack order line gains `→ hr_fx(--skip-rp) → scarlet →`; the RP block gains `node tools/build_scarlet_rig.mjs
  --resourcepack $RP` and `python3 tools/build_mboss_hr_fx.py --resourcepack $RP` (after `build_rift.py`: the arrival tear uses the rift
  models).
- **0-8**: the moved suites `sim/hr/tests/` (13, what each covers) and the sims `sim/hr/tests/lib` · `sim/hr/s1k/lib` · `sim/hr/sr`.
- **0-9** (decision 5): the "gen_check 9" item dropped from the known-failure line, with the reason written there (the 11-03 fix of
  `REAL_DP` / `cmsim.variant`, passing at I1a's and I1b's `run_all`); the same note in `tools/dev/sim/README.md` 3-2.
- **특수 보스 / 균열** (S1's fragment + what enabling her changes): 타키 and 홍련 both enabled (w 10 each; "타키뿐" → both), picks
  per entry, the title with `winWord`, `#spN` 3 · `#spRoll` 2, the four FN bullets (`winWord`, `rwHook`, `poof`, `bars_off` / `bars_on`), the
  cherry-grove pool line, `rift_id {id:"scarlet"}`, the `swon_msg_w` test message, the S1 core-file list.
- **6절 아이템** (SR, sr-1): the 등급 규칙 exception line; the [ MYTHIC ] 화무십일홍 entry (육참골단 · 검신합일 · 홍련일섬, timers,
  ★★★ line, sounds). **조절 지점**: the `#hrMoonAtk` / `#hrMoonCrit` / `#hrMoonSpd` row.
- **New section 「홍련 (`boss/scarlet/`, 특수 보스 · `tools/build_mboss_scarlet.py`)」** after 아를레키노 (from S3's draft + S1K / S2a / S2b / S4 /
  SR fragments, brought to the merged tree): 플레이어용 요약 · 진행 · 패턴 (R1-R3, A8 / A13 rows from S4, the P1 / P2 weights) · 자영 연참 ·
  화면 · 연출 · 시퀀스 (incl. the seat 5 b nearer, the halo, s2b-5's sheathe note) · 보상 · 이벤트 (SR's table rows) · 모습 · 효과 · 경기장
  (rig, `item_sword`, kit, arena + the real-server dark-look numbers) · 시험 명령 · 파일 · 생성 순서 (generators, order, state, cost, suites; the
  plan / contract docs stay in the scratchpad until the release).
`HR/rp_hr/README.md` (the RP README that ships; S2a's and S1K's fragments): fonts 10 → 11 with the `rlk:mboss_hr` row, the
`…/mboss/<id>/` row gains `scarlet` and `hr_kit`, §3 names `build_scarlet_rig.mjs` among the folder-clearing rigs and gains the row
`build_mboss_hr_fx.py` + `build_scarlet_rig.mjs`, §4 the budget line (홍련 0.33 M: `scarlet` 0.084 + `hr_kit` 0.242; total 12.955 M).

### 12.7 The suites into the repository (step 5; s2a-5 / sr-1)
`HR/i1/tools/move_suites.sh`: `HR/<x>` → `R:tools/dev/sim/hr/<x>`, so every `HERE.parent / …` path the suites use still resolves:
`hr/tests/` (the 13 suites + `lib/` = `hrsim.py` + the four vendored sims (md5s unchanged, `lib/README.md`)), `hr/s1k/lib/`
(`mcsim` `fgsim` `azsim` `cmsim` copies + `hrfxsim.py`: test_kit / test_arena_hr), `hr/s1k/vanilla/data/minecraft/tags/block/`
(the 22 vanilla 26.3 block-tag files test_arena_hr resolves: the four `supports_*` tags, `#rlk:dash_pass`'s vanilla tags and their
nesting; 4.8 KB, like `rd/tests/sound_ids.txt`), `hr/sr/srsim.py` (test_hwamu / test_moon / test_reward `real`). 896 KB in all;
`tools/dev/sim/.gitignore` already keeps `tmp/` `out/` `__pycache__/` out. `HR/tests` stays as the scratch copy (a concurrent review
may read it; the repository copy is the one to edit from now on). Path notes (also in `tools/dev/sim/README.md` 3-4): `ev_dry.py` /
`test_rig.py` keep their scratch defaults (`--dp` / `--rp` given), `test_special_hr` / `ident_hr` read the base commit from
`/home/user/rlk`, `test_kit`'s calls section scans a merged tree's own module (else builds `wip/hr-s4` + `wip/hr-s2b`, local only),
`test_hwamu` reads `PLAN.md` / `wiki/w2.txt` from `$HR_DOCS` or beside the suite and skips those checks without them (the saved wiki
never goes into the repository, README 0-7; the plan joins `tools/dev/sim/hr/` at the release).
Suite adaptations made at I1b (each marked "I1b" in the file): `lib/hrsim.py` block tags; `test_kit` calls on the merged tree + tinted
looks + the halo ratio; `test_scarlet` I2 restored + the look stub's `hr_field/tick` no-op (the real `job_tick` now dispatches to the
theme's tick after a `/reload`: the stub `arjob` has no `i` → KeyError in the sim) + the cost split (Z1 / Z2: the look job's slice
ticks ≤ 5 k, §13); `pat_ghost` F9 (`#hrLook` through `api.arena_look`)
and J8 (`scarlet_line` `yaw:90`); `test_hwamu` docs lookup.

## 13. Gates (I1b, final tree: 7cc4a0c, tree 645bc43f; the head c3ce75a after it only rewraps one README line)
- **Regenerate twice** (`HR/i1/tools/gate_regen.sh 1` / `2`, logs `HR/i1/out/gate/`: `build_mboss_hr_fx.py --resourcepack HR/rp_hr`, `node
  tools/build_scarlet_rig.mjs --resourcepack HR/rp_hr`, `bash HR/tools/regen_d0.sh R:` = `regen_all.sh` incl. the kit `--skip-rp` and
  the module + bf / fg kits): `git status` **empty after each pass**, the tree (`write-tree` of everything) **645bc43f** = HEAD's tree both
  times; RP whole pack **62e15a3f8c3cf6fde51542ca216099a58b0de426** (4 785 files) before and after both passes. A third pass on
  the head c3ce75a after the suites (whose `test_rig --rebuild` rewrites `rig/**`): status empty, tree af1476a7 = HEAD's, RP
  62e15a3f…. The RP hash differs from 12.2's 67c4190c… only by `README.md` (12.6): with the old README swapped back in, the list
  hashes to 67c4190c… again.
  Kit: 429 functions, 50 presets, 5 props, 104 sounds, 5 HUD calls, 25 lines, 53 textures (0.242 M px), 7 glyphs; rig: 29 parts,
  47 clips (0 stand-ins), 2 109 key files / 22 050 keys, 2 629 functions, 78 models, 48 sprites; module 1 145 functions
  (`boss/scarlet/**` 4 203 = rig 2 629 + kit 429 + module 1 145).
- **check_mboss_pack**: 4 mid, 4 chapter, 3 special, 7 arenas, **0 problems**. **`api.py --check`** ok (29 parts + shadow, 47 clips /
  280 events, 12 hit tables, 25 lines, 50 presets, 104 sounds, 237 568 kit px, 115 owned paths).
- **rplint** `HR/rp_hr`: **0 problems**. **atlas_px**: stitched items atlas **12 954 880 px (12.955 M)** from 1 478 sources ≤ 13.2 M.
  This boss's sprites (sum of the atlas sources under `mboss/scarlet/` and `mboss/hr_kit/`): rig **83 712** (48) ≤ 0.15 M, kit
  **237 568** (52) ≤ 0.26 M, gate icon **4 096** (1) ≤ 0.005 M; 325 376 in all ≤ 0.43 M.
- **Look-job command counts** (`test_arena_hr` 4d / 5b; limits 8 000 per slice, 32 768 blocks per fill): `moon` 7 094 commands in
  4 real slices [2 340, 2 340, 1 549, 865], `crimson` 7 263 [2 518, 2 496, 1 469, 780], `dark` 6 692 in 4 real slices 3 t apart
  [2 215, 0, 0, 2 228, 0, 0, 1 469, 0, 0, 780] (+ the last slice's `done` call: the files hold 7 095 / 7 264 / 6 693 lines); the
  build 21 slices, max 4 943, 24 726 in all. In the fight (test_scarlet `cost`, the kit counted since verification round 1, §14):
  the 44 slice ticks avg 1 856, max 3 442 ≤ 5 k (§5 gate 5; the first I1b figures 1 721 / 3 263 had the kit stubbed). On the real
  server (12.5): every slice ≤ 8.6 ms alone.
- **Checkers** vs 35b82e5 (`HR/tools/checkers.sh R: HR/i1/out/checkers_final`, after the suites' `test_rig --rebuild` had finished:
  a first run during it read a half-written `rig/**`; byte-identical to the run on 78e827f, `checkers_b`, which
  `HR/i1/checker_accept_b.md` was made from and which was then deleted): refs 44 → 44 (new 3: the kit's
  `hud/line → hud/l/` macro path, D0's `hr_field/full_rim:3`, the count; gone 3), macro 3 357 → 3 436 (new 82: kit `with storage`
  calls 56, rig anchors 9, D0 arena 4, the theme's `done with storage arjob` 4, SR dmg_calc 2, S1 swon 2, kit `hud/l` 1, S3 A9 1 +
  help 1, SR line shift 1, the count 1; gone 3), nbt 0 new, lint 193 340 → 215 716 (new 22 378: cinematic keys `bad target` 11 778,
  rig `bad target` 10 546, kit `time query gametime` 32, kit `execute … store / if function` without `run` 9, `stopsound` 3 (a base kind
  ×28; the wind stop, written with the kit on), SR `time` 3, kit macro summon 1 + macro positioned 1, I1's `tp … facing entity …
  eyes` 1 (decision 2: stays accepted), SR sidebar 1 / display 1 / if items 1, the count 1; gone 2). **0 unclassified**
  (`HR/i1/tools/chk_classify_b.py`, list `HR/i1/checker_accept_b.md`; I1a's `checker_accept.md` kept).
- **run_all** (on 78e827f's tree: the datapack has not changed since, the later commits touch only `README.md` and `tools/dev/sim`;
  `R:tools/dev/sim` copied to `HR/i1/sim` with the vcheck baselines `lint.txt` / `macro.txt` as at I1a; log `HR/i1/out/run_all_i1b.log`,
  999 s; the step outputs moved to `HR/i1/out/run_all_i1b/`, the copy deleted): the same result as
  I1a's. **34 steps ok** (as I1a): test_chapter, test_fw_az, test_fw_ap, the 28 old-path M0 suites (mb3 6, mb3bf 4, mb3fx 1, mb2 5,
  mb2fx 1, int 11; I1a's §8 called them "the 23"), **gen_check** (GENERATOR CHECKS PASSED), check_nbtpath 0, check_mboss_pack 0.
  Failures = README 0-9's list only:
  - `test_m0diff` 40 failures, **the same 40 names as the D0 base run** (sorted: `HR/i1/out/m0diff_names/i1b.txt` = `base.txt`); budget
    numbers unchanged (proto +6.59, butterfly +6.71, fieldgen +6.99 per tick; README 0-9's open question).
  - `test_px` 4e (18); `ident` 10 (the stale 22ba247 pins).
  - vs the old pre-Apep baselines: refs 30 findings / 7 new (I1a 29 / 6: + `boss/scarlet/fx/hud/line → hud/l/`, the kit's macro-built
    path, the kind `boss/arlecchino/fx/hud/line` has), macro 3 153 / 575 new (I1a 3 097 / 519: + 56 = the kit's `with storage` calls
    under `boss/scarlet/fx/**` (57 lines) and the theme's 4 `done with storage arjob` lines, both kinds accepted above), lint 6 767 /
    2 959 new (= I1a).
- **Suites** — all 13 from the repository's copy (`R:tools/dev/sim` copied to `HR/i1/sim_final`, deleted after; run in its `hr/tests`
  with `HR_DOCS=HR`; `--dp` / argv = `R:`, `--rp` = `HR/rp_hr`; `HR_DOCS=… SUITES_DIR=… bash HR/i1/run_suites_b.sh final_b`, logs
  `HR/i1/out/final_b/`): **all green** — `test_rig.py --rebuild` 86 / 86 (119 s); `ev_dry.py` 62 / 62; `test_special_hr.py` 93 ok
  (ident + R2b skipped as at I1a: `ident_hr` covers them); `test_scarlet.py` 139 ok (I2 compares the whole end state: full intro
  6.34 b, the skip 6.34-6.50 b; Z1 / Z2 cost; 1 137 s); `pat_p1.py` 341; `test_reward.py` 51 (+ `real`); `pat_ghost.py` 186;
  `test_hwamu.py` 258 / 258 (no check skipped: `HR_DOCS`); `test_moon.py` 50 / 50; **`test_kit.py` 10 546 / 10 546**; **`test_arena_hr.py`
  89 / 89**; `ident_hr.py` pass (48 611 files in scope, 44 301 at 35b82e5: changed 71 / new 4 310, all in the allow-list or this boss's
  outputs; SR hand files changed 17 / new 28); `gen_check_hr.py` 28 / 28 (I1a 25: + the kit's datapack and RP sides). ≈ 11 930 checks
  (10 546 of them `test_kit`'s). The runs during the work used the scratch copies in `HR/tests` (b2-b4 on 78e827f: the
  `test_scarlet` look stub / cost split and `pat_ghost` F9 / J8 fixes came from them); the repository copy is byte-identical to them.
- **Tick cost** (`test_scarlet.py cost`, strict count as I1a; **restated in verification round 1**, §14 M1: the first I1b figures
  ran the theme's look jobs and the decor props but **stubbed the kit** — `ScSim.call` returned 1 for every `rlk:boss/scarlet/fx/**`
  call, so only the module's call line counted and the card ager never ran — although this item said "now with the kit". Now every
  world of the section runs the kit for real (`hrsim.kit_on`: the presets' cards, the card ager they schedule, the cull, the HUD
  tickers, scheduled functions in vanilla's order), after CS1's 40 dark leaves were split over two ticks (§14); log
  `HR/i1/out/fix_b1_suites2/test_scarlet.log`):

  | part | ticks | avg (the kit's own) | max | max without the slice ticks | first I1b, kit stubbed: avg / max |
  |---|---|---|---|---|---|
  | P1 | 1500 | 516 (75) | 1 357 | 1 357 | 441 / 900 |
  | P2 | 1500 | 489 (38) | 3 396 (a look-job slice) | 1 316 | 451 / 3 263 |
  | A8 | 194 | 550 (112) | 3 128 (slice) | 1 690 | 438 / 2 925 |
  | A13 | 258 | 571 (119) | 3 129 (slice) | 1 690 | 452 / 2 926 |
  | CS1 | 212 | 450 (144) | 3 442 (slice) | 2 198 (#sq 172: the second half of the leaves) | 306 / 2 885 |
  | SQ1 | 60 | 477 (41) | 2 757 (slice) | 1 487 | 436 / 2 655 |
  | repel (CS2 + CS3) | 205 | 444 (39) | 3 215 (slice) | 1 083 | 405 / 2 942 |
  | lead_stand | 69 | 599 (49) | 3 131 (slice) | 1 240 | 550 / 2 935 |
  | **fight state** | 3 998 | **505** (66) | 3 442 | **2 198** | 438 / 3 263 (956 without slices) |
  | the 44 look-job slice ticks | 44 | 1 856 | 3 442 (≤ 5 k) | — | 1 721 / 3 263 |
  | intro (intro state) | 639 | 368 (69) | 911 | 911 | 299 / 739 |
  | ending CS4 (death state) | 1 042 | 262 (28) | 903 | 903 | 234 / 665 |
  | event coda (death state) | 122 | 219 (15) | 505 | 505 | 204 / 343 |

  Average ≤ 600: met (505); Apep ≈ 830: met; every fight tick but the look-job slice ticks ≤ 3000: met (2 198; before the leaves split
  3 598 at CS1 #sq 171, the review's figure; §14). Z1 / Z2 hold those bounds, Z3 that the kit really ran (kit commands in every
  10-tick window of P1 and on ≥ 80 % of its ticks).
- **Loadcheck** (`RLK_DEV=S: bash R:tools/dev/loadcheck.sh R: hr_i1`, head 7cc4a0c): `loadcheck hr_i1: 0 function load failure(s)`,
  exit 0, `Loaded 1870 advancements`, `Starting minecraft server version 26.3` + `Done (1.507s)` (log `S:mcsrv/hr_i1.log`, output
  `HR/i1/out/loadcheck_hr_i1.txt`).

### 13.1 Commits on `wip/hr` (I1b; never pushed; trailer as the brief)
3d2370e / a0a7dff the two `--no-ff` merges; 5e6c963 regeneration with the kit and the theme; 00e6489 the gate icon; 78e827f the
requests + decision 1; eae34a8 the README; 7cc4a0c the suites into `tools/dev/sim/hr` + the sim README; **c3ce75a** a README line
that began with `#FF3A55)` rewrapped (head). `WT` (`HR/wt_hr`) and `RP` (`HR/rp_hr`, whole pack 62e15a3f…) stay. The work branch
`claude/exciting-pascal-ek1vuy` (0d65e87) is an ancestor of
`wip/hr`, so it can fast-forward. Scratch outside the repository (not committed): this file, `progress.md`, `HR/contract.md` §7,
`HR/rp_hr/README.md`, the renders `HR/renders/i1b_*.jpg`, the tools in `HR/i1/tools/`.

### 13.2 For the lead
- **Halo base dimmed** (s1k-3 + s2b-4): a `custom_model_data` tint only multiplies, so `p1b` / `p2b` = +20 % needs `p1` / `p2` at
  0xD4D4D4: the default halo is 17 % darker than S1K built it (`HR/renders/i1b_halo_looks.jpg`). The alternative is a second,
  brighter sprite pair (2 × 96² = +18 432 px: the kit would be 256 000 of its 260 000) — for the lead's eye.
- **Decision 1 needed the walk rule too**: the seat 5 b nearer alone ends the walk at 7.53 b (the old leg rule stopped her anywhere
  in 7.0-8.1 b); the leg now runs while she is > 7 b away (17 legs, 6.33 b). Speed and clip unchanged. PLAN §3.1's seat text
  ("≈ 8 b north of C") is stale (contract §7 records the new seat); PLAN is in the scratchpad until the release.
- **Decor props follow the look** (I1b finding, `core/look/go`): before, the halo stayed `p1` and the lotus `bud` through P2 and the
  darkness. Fixed per PLAN §6.3-6.5's "kit props" rows; confirm in game with the arena looks.
- **Cost rule** (restated in verification round 1, §14): Z1 / Z2 hold the arena look-job slice ticks to contract §5 gate 5's ≤ 5 k
  (3 442) and every other fight tick to ≤ 3000 (2 198), both now with the kit running for real; the first report's 956 / 3 263 had
  the kit stubbed, and with it counted one CS1 tick reached 3 598 until its 40 leaves were split over two ticks (§14). Average 505
  ≤ 600. Before the theme existed in the merged tree no slice ran in the sim.
- **The client side of the dark look** (re-light, chunk redraw) cannot be measured headless: the README's 홍련 section names it as
  the thing to watch in game; the server side is ≤ 8.6 ms per slice (12.5).
- **RP hash** for the release: 62e15a3f… (the RP README edit; 67c4190c… with the old README).
- **S2c** (`wip/hr-s2c` fb4c16e, the skin) is not merged here: after it, rerun the rig into `RP`, `test_rig --rebuild`, regen × 2,
  the renders and the RP hash.
- `test_hwamu`'s PLAN / wiki checks need `HR_DOCS=<scratchpad>/hr` until the plan moves into `tools/dev/sim/hr/` (the final run used
  it: no check skipped).
- The vendored `cmsim` of the other suites still lets only air / light through `#rlk:dash_pass` (the hrsim fix is local to
  `hr/tests/lib`): other bosses' sims refuse plant cells the game lets through — not changed here (outside this boss).
- Open as before: README 0-9's m0diff budget question (+6.59 / +6.71 / +6.99 per tick), `test_px` 4e, `ident` 10.

## 14. I1b verification round 1 (11-05: M1 major, m1-m5 minor)
Head before: c3ce75a; **commit bd8c52d** (one commit on `wip/hr`, never pushed, the brief's trailer; tree 5479542e). Every issue was
real; all are fixed at their source (generators, suites, README, notes), regenerated and re-gated below. Logs: `HR/i1/out/fix_b1/` (probes, cost runs, gate passes, checkers), `HR/i1/out/fix_b1_suites{,2}/` (the 13
suites), `HR/i1/out/run_all_i1b_f1.log` (+ `run_all_i1b_f1/`); probes and calibration in `HR/i1/fix_b1/`.

| id | issue | result |
|---|---|---|
| M1 | the cost gate stubbed the kit (`ScSim.call` returned 1 for every `rlk:boss/scarlet/fx/**` call: only the module's call line counted, the ager never ran) though §13 / README / contract / the report said "with the kit"; counted, one CS1 tick reaches ≈ 3.6 k > the 3000 per tick | **fixed**: the harness runs the kit for real (14.1), the CS1 burst is split at the source (14.2), the numbers restated (14.3) |
| m1 | README: the intro walk legs "12틱" | **fixed**: "8틱 다리 1.2칸, 0.15칸/틱" (`seq.py` `m/leg`: `glide(8)` every 8 t; the generated `seq/intro/m/leg` `mboss/mv/glide {t:8}`) |
| m2 | README: the whole look jobs "17–24 ms" | **fixed**: "4.7–23.5 ms" (= `darkcheck_1.txt`: 17.2 / 4.7 / 5.6 / 22.1 / 23.5 ms P99; §12.5) |
| m3 | README: two RP orders for this boss (0-4: rig → kit; the 홍련 section: kit → rig) | **fixed**: the 홍련 section now says `build_rift.py` → `build_scarlet_rig.mjs` → `build_mboss_hr_fx.py`, "0-4 리소스팩 묶음의 순서: 새 팩에서는 이 순서가 `items.json` 소스 순서와 팩 해시를 정한다" (the shipped atlas: rig 1377-1424 before kit 1425-1477, checked on `HR/rp_hr`) |
| m4 | no suite asserted `core/amb`'s cadence, `core/look/go`'s prop looks, `seq.py`'s `p1b` / `p2b` switches | **fixed**: `test_scarlet` P14 / P15 / L5, `ev_dry` 5 halo checks (14.4); each caught a mutation of the behaviour it covers |
| m5 | wording: (a) §12.2 "+ the rig's 48" (appended) — the rig's sit before the kit's; (b) §12.3 / 5e6c963 "15 sequence bucket files re-cut" — 14 buckets + `p/a6/k/12`; (c) `progress.md` "kit 241 664 px" mixed in the gate icon | **fixed**: (a) §12.2 now gives the indexes; (b) §12.3 lists the 15 (`git diff --name-status --no-renames a0a7dff 5e6c963`: 14 `seq/*/b/*` + `p/a6/k/12`, which at a0a7dff held only `# A6 pattern tick 12`; its call is `p/a6/tick:5`); the commit message stays (history is not rewritten), §12.3 carries the correction; (c) `progress.md`: kit 237 568 px sprites, with the gate icon 241 664 |

### 14.1 The kit counted (`tools/dev/sim/hr/tests/lib/hrsim.py`, `test_scarlet.py` `cost`)
- `hrsim.kit_on(s)`: `ScSim.kit_real` runs `rlk:boss/scarlet/fx/**` for real, as azsim runs its KITS (the default stays the stub that
  only logs `s.kitl`); the kit's one engine call `view/ttl_blank` runs for real too (the engine stubs had made it empty); the two
  harness fixes the kit needs, as in its own harness `hr/s1k/lib/mcsim.py`: typed arrays `[I; …]` in SNBT values, `execute summon
  <type>` (the summoned entity runs the rest, rotation 0 0). `kit_on` also sets `s.sched_vanilla`: `world_sc` runs the scheduled
  functions after the tick's functions at gametime t + 1 in the same world tick (vanilla's `tickTime`; fgsim's `run_sched` ran
  them a world tick later), `s.t` and the logs staying at the world tick. New logs: `s.kit_hist` (the kit's own commands per world
  tick), `s.kitx` / `kit_ex(s, sub)` (each kit call's executor tags, caller, `#ph hr`).
- Calibration (`HR/i1/fix_b1/calib.py`, `calls.py`): every distinct static kit call of the module (243, the uninstall apart), run
  once in `hrfxsim.FxSim` (the kit's harness) and in `ScSim` + `kit_on`: the same commands for the call (22 710 in all) and for its
  60-tick tail (75 552), 0 differences (`calib_fx.json` = `calib_sc.json`). Vanilla order (`probe_vanilla.py`): a call made in a
  tick costs the call + the ager's first pass in that tick (`leaves_dark {n:40}` 2 915 + 295 = 3 210, `ambient_p1` 73 + 22, as
  FxSim's call + first `tick()`), the tails the same. Single calls as the review measured: `leaves_dark {n:40}` 2 915, `{n:8}` 617,
  `ambient_p2` 8, `ambient_p1` 110 with the kit's one-time init (73 without).
- `test_scarlet.py` `cost`: every world it measures is `world(..., kit=True)` (`H.kit_on`); the table gives per part the average,
  the maximum, the maximum without the look-job slice ticks and the kit's share, and the five highest non-slice ticks with their
  place (sequence + `#sq`, or pattern + `#pt`); Z1 / Z2 as before (average ≤ 600, every fight tick ≤ 3000 but the slice ticks ≤
  5 k); new Z3: the kit really ran (kit commands in every 10-tick window of P1 and on ≥ 80 % of its ticks).
- Before the source fix, on the same seeds / mover / dasher / test ids (`HR/i1/out/fix_b1/cost_before_vanilla.log`, a hard-linked
  copy of the tree with HEAD's three generated files): fight state average 505, P1 516 · P2 489 · A8 550 · A13 571 · CS1 449 · SQ1
  477 · repel 444 · lead_stand 599; the non-slice maximum **3 598 at CS1 #sq 171** (the kit 3 353) = the review's figure; Z2
  FAIL. (With fgsim's schedule order the same tick read 3 202, the ager's pass landing a tick later: `cost_before.log`.)

### 14.2 The source fix: CS1's 40 dark leaves over two ticks
- Kit (S1K's `tools/build_mboss_hr_fx.py`, preset `leaves_dark {n}`): **n < 0 = the last -n of the 40 leaves**; each card line is now
  `execute unless score #n2 hrFx matches <k-39>..<k> run …cardx {…}` (was `if … matches <k+1>..`). A positive n is unchanged:
  `{n:8}`, `{n:24}`, `{n:40}`, `{n:0}` make the same cards as HEAD's file in the kit's harness, and `{n:20}` + `{n:-20}`,
  `{n:10}` + `{n:-30}`, `{n:-40}` make exactly the 40 of `{n:40}` (positions, turns, models; `HR/i1/fix_b1/probe_leaves.py`).
  `api.KIT_PRESETS['leaves_dark']` keeps its one argument; the preset's doc (manifest) names the new case.
- S2b's `tools/mboss_scarlet/seq.py` CS1 C8: `leaves_dark {n:20}` at slash + 2 (#sq 171), `{n:-20}` at slash + 3 (#sq 172), was
  `{n:40}` at 171: the same 40 leaves, the second half 1 t later (each leaf keeps its own 0-9 t show delay).
- Regenerated (`HR/i1/tools/gate_regen_f1.sh`, a copy of the I1b gate script logging to `out/fix_b1/gate`): changed outputs
  `fx/p/leaves_dark`, `seq/cs1/k/171`, `seq/cs1/k/172`, `tools/mboss_hr_fx_manifest.json` (the preset doc); RP unchanged
  (62e15a3f…, 4 785 files). Passes 2 and 3 on the final sources: the same tree (03869843) and RP; `check_mboss_pack` 0 problems;
  `api.py --check` ok. `test_kit`: + a variant `{n:-20}` in the preset sweep and the split check (`{n:20}` + `{n:-20}` = the 40 of
  `{n:40}`, `{n:8}` the first 8, `{n:0}` none).
- After (`HR/i1/out/fix_b1/cost_after.log`): fight state average 505 (the kit 66), the non-slice maximum **2 198** (CS1 #sq 172;
  #sq 171 2 022), the 44 slice ticks average 1 856, maximum 3 442; Z1 / Z2 / Z3 ok. The cost rule proposed in the I1b report
  (decision 4: every fight tick ≤ 3000 but the look-job slice ticks ≤ 5 k) holds with the kit counted; no spike needs accepting.

### 14.3 Restated
§13's cost item (table: the kit's share, the maximum without slices, the first I1b figures beside), §13's look-job line, §13.2's
cost rule; README 「홍련」 상태 줄 (평균 505, 그중 효과 도구 66, 조각 틱 뺀 최대 2198 · 나누기 전 3598, 조각 틱 1856 / 3442);
contract §7 (the I1b entry's numbers + the round-1 entry: the kit's `leaves_dark` n < 0, `seq.py`'s split); `tools/dev/sim/README.md`
(the `test_scarlet` / `ev_dry` / `test_kit` rows, the hrsim bullet) and `hr/tests/lib/README.md` (the round-1 paragraph).

### 14.4 The new assertions (m4)
- `test_scarlet` `phases` P14: through the whole deflect chain, `ambient_p2` from `core/amb2` at the player every 6 t in A8 (206 t),
  the down window (220), P2 (89) and A13 (270) — `#ph` read at each call (`kitx`), never in CS1 / SQ1 / CS2 / the lead-in / CS3 /
  the death, one call per beat; no ambient call but `core/amb1` / `amb2`'s and S2b's intro start (its E0 staging `ambient_p1`).
  P15: a 300-tick P1 stretch: `ambient_p1` every 10 t (30 calls), no `ambient_p2`.
- `test_scarlet` `look` L5: each look job started by `core/look/go` re-looks, in its tick and from `look/go` itself, the halo (1
  call: crimson `p2`, dark `off`) and the 8 lotus (crimson / dark `bloom`); the moon row (no fight request asks for moon) is served
  directly: halo `p1`, lotus `bud` ×8.
- `ev_dry` halo: the tick files carry the halo lines exactly at intro 112 (`p1b` / `p2b` by the arena look record) and 146 (`p1` /
  `p2`), ending 690 / 780, and the same restore in `seq/intro/skip`, `seq/intro/cancel`, `seq/ending/cancel` — nowhere else; runs in
  its mcsim world with a halo entity: the intro under moon → 112 `p1b`, 146 `p1`; crimson → `p2b` / `p2`; dark → none; the skip and
  the intro cancel at 121 (inside the window) → `p1` at 121; the ending cancel at 701 → `p2`; the whole ending (crimson) → 690
  `p2b`, 780 `p2`.
- Mutations (hard-linked tree copies, removed): P1 ambience every 6 t → P15 FAIL; ambience in CS2 → P14 FAIL; crimson lotus `bud`
  (`core.py` `DECO_LOOK`) → L5 FAIL; no restore at 146 (`seq.py`) → 2 ev_dry halo checks FAIL.

### 14.5 Gates (the final tree of this round)
- **Regenerate** (`HR/i1/tools/gate_regen_f1.sh`: kit `--resourcepack HR/rp_hr`, the rig, `regen_d0.sh` = `regen_all.sh` incl. the kit
  `--skip-rp` and the module + bf / fg kits): pass 1 after the generator edits changed exactly `fx/p/leaves_dark`, `seq/cs1/k/171`,
  `seq/cs1/k/172` and `tools/mboss_hr_fx_manifest.json`; passes 2 and 3 on the final sources: the same tree **03869843** (every file
  incl. this round's edits) and RP **62e15a3f8c3cf6fde51542ca216099a58b0de426** (4 785 files, unchanged from §13) before and after
  each pass; `check_mboss_pack` 4 mid / 4 chapter / 3 special / 7 arenas / **0 problems**; `api.py --check` ok (29 parts + shadow,
  47 clips / 280 events, 12 hit tables, 25 lines, 50 presets, 104 sounds, 237 568 kit px, 115 owned paths). The RP did not change, so
  rplint 0 / atlas 12.955 M / the budgets of §13 stand.
- **Checkers** (`HR/tools/checkers.sh R: HR/i1/out/fix_b1/checkers`): refs / macro / nbt / lint byte-identical to §13's
  `checkers_final` (0 unclassified; the duplicate outputs then deleted, `checkers.log` kept).
- **Suites** — all 13 from a copy of `R:tools/dev/sim` (`HR/i1/sim_f1`, deleted after; `HR_DOCS=HR`; logs `HR/i1/out/fix_b1_suites/`
  (test_rig, alone first) and `fix_b1_suites2/`): **all green** — `test_rig.py --rebuild` 86 / 86; `ev_dry.py` **67 / 67** (62 + 5
  halo); `test_special_hr.py` 93 ok; `test_scarlet.py` **143 ok** (139 + P14, P15, L5, Z3; the cost table of §13; I2: the full intro
  6.34 b, the skip 6.34-6.50 b); `pat_p1.py` 341; `test_reward.py` 51; `pat_ghost.py` 186; `test_hwamu.py` 258 / 258; `test_moon.py`
  50 / 50; `test_kit.py` **10 594 / 10 594** (10 546 + 48: the `{n:-20}` sweep, the split check, CS1's second call site);
  `test_arena_hr.py` 89 / 89; `ident_hr.py` pass (48 611 files in scope, changed 71 / new 4 310 = §13); `gen_check_hr.py` 28 / 28.
  `test_scarlet phases` again on the final file (a tidy-up of `amb_cadence`'s caller filter after the copy was taken): all ok.
- **run_all** (a fresh copy of `R:tools/dev/sim` in `HR/i1/sim` + the vcheck baselines, deleted after; log
  `HR/i1/out/run_all_i1b_f1.log`, 696 s; outputs `HR/i1/out/run_all_i1b_f1/`): the same 40 step lines as §13's run (34 ok incl.
  `gen_check` GENERATOR CHECKS PASSED, `check_nbtpath` 0, `check_mboss_pack` 0); failures = README 0-9's list: `test_m0diff` 40 (the
  FAIL lines byte-identical to §13's run, the names = the D0 base's, `HR/i1/out/m0diff_names/i1b_f1.txt`), `test_px` 4e, `ident` 10,
  refs 30 / 7 new, macro 3 153 / 575 new, lint 6 767 / 2 959 new vs the old baselines (= §13).
- **Commit and loadcheck**: bd8c52d (`README.md`, the kit generator + its manifest, `seq.py`, the three regenerated functions, the
  suites and their READMEs; 13 files). A fourth regeneration pass on it: `git status` empty, the tree = HEAD's (5479542e), RP
  62e15a3f…. Loadcheck (from `R:`, `RLK_DEV=S: bash tools/dev/loadcheck.sh R: hr_i1b_f1`): `loadcheck hr_i1b_f1: 0 function load
  failure(s)`, exit 0, `Loaded 1870 advancements`, `Starting minecraft server version 26.3` + `Done (0.634s)` (log
  `S:mcsrv/hr_i1b_f1.log`, output `HR/i1/out/fix_b1/loadcheck_hr_i1b_f1.txt`).
- Scratch: the suite / run_all copies (`HR/i1/sim_f1`, `HR/i1/sim`), the mutation trees and the duplicate checker outputs are
  deleted; kept: the probes and calibration (`HR/i1/fix_b1/`, 92 KB), the logs (`HR/i1/out/fix_b1*`, `run_all_i1b_f1*`), the gate
  script copy `HR/i1/tools/gate_regen_f1.sh`. `WT` clean, `RP` unchanged.

## 15. I1b verification round 2 (11-05: m1, m2 minor; no blocker / major)
Head before: bd8c52d; **commit 4c81817** (one commit on `wip/hr`, never pushed, the brief's trailer; tree 9ac7fe78). Both issues were
real; both are fixed at their source. Logs: `HR/i1/out/fix_b2/` (gate passes, hooks runs, checkers, loadcheck),
`HR/i1/out/fix_b2_suites/` (the 13 suites), `HR/i1/out/run_all_i1b_f2.log` (+ `run_all_i1b_f2/`); probes in `HR/i1/fix_b2/`.

| id | issue | result |
|---|---|---|
| m1 | decision 1's distances (26.73 b, 6.33 / 6.34 b) are the simulator's: the commands wrote the seat `884 201 5`, the game block-centres it to (884.5, 201, 5.5) | **fixed** by the issue's first option (15.1): the commands write `884.0 201 5.0`, so the game uses `api.SEAT_POS` itself and the recorded figures hold in game; no figure needed restating |
| m2 | `tools/dev/sim/README.md` §2: the suites behind the fixed `variant()` / `light_copy()` "not run yet" | **fixed** (15.2): they ran at the 11-05 I1 `run_all`; only `ar/tests/test_arena_fl.py` is still not run |

### 15.1 m1: the seat written exactly
- Confirmed first: `mboss_lib.num(884.0)` = `884`; Minecraft's coordinate parser adds 0.5 to an absolute x / z without a decimal point
  (summon / tp / execute positioned / facing; never y); mcsim's `coords()` takes `float(t)` (the `tools/dev/sim/README.md` mcsim
  row already lists "정수 summon / tp 좌표의 +0.5 보정 없음"). `probe_seat.py` (`probe_seat.txt`), per look (moon / crimson / dark):

  | seat | from `start` | walk end (17 × 1.2 b) | floor under the stone | nearest non-air (y 201-205) | nearest grass |
  |---|---|---|---|---|---|
  | (884.0, 5.0) = `api.SEAT_POS` (sim, docs, theme clearing, render) | 26.73 b | 6.33 b | 4 cells, all mycelium (P1) / crimson nylium | 2.12 b, light (885, 201, 3) | 2.12 b (moon) |
  | (884.5, 5.5) = what `884 201 5` gave in game | 26.31 b | 5.91 b | 9 cells, mycelium + pale moss / nylium + wart | 2.00 b, light (884, 201, 7) | 2.24 b (moon) |

  The issue's figures are right; the lead's ≤ 7 b and the clearance held either way.
- Fix (option 1, at the generators): new `api.xyz(p, nd=4)` writes an absolute point with x and z always carrying a decimal point (y
  as `L.num`; self-check in `_check_contract`). S3's `core.py`: `spawn` (comment + `execute positioned … rotated … run function
  rlk:mboss/body`), the seat rock of `core/deco` / `core/deco_seat` (`one(…, exact=True)`), `core/replay/start`'s tp; S2b's `seq.py`
  `rock()` / `rock_kill()` (`seq/intro/k/{24,52,206,630}`, `seq/intro/skip`). Regenerated: exactly those 9 command lines + the spawn
  comment changed (`884 201 5` → `884.0 201 5.0`), nothing else; the RP untouched. Why option 1 and not restating the figures: the
  theme's seat clearing (`SEAT_CLEAR` round `SEAT_POS`), `test_arena_hr` 9d, the opening render (`HR/renders/i1b_intro_open.jpg`, her rig
  at `api.SEAT_POS`), `test_scarlet` I2 / K3 and every recorded figure already use (884, 201, 5); now the game does too, and the stone
  stands on four uniform floor cells in the middle of its clearing.
- Regression check: `test_scarlet` `hooks` **K3b** — every command line of `F:boss/scarlet` that places or finds the seat (summon / tp
  / positioned / facing at `api.SEAT_POS`) writes x / z with a decimal point, and the four core sites + the skip are among them (9
  lines now). K3 (her simulated position) cannot see the difference; K3b can: on a hard-linked tree copy with HEAD's 9 files swapped
  in (links removed before writing), K3b FAILS at all 9 lines while K3 still passes (`test_scarlet_hooks_mut.log`; copy deleted). K3b
  also prints the other whole-x / z points (15.4).
- Docs: README 「홍련」 CS0 bullet (the seat's parenthesis: `api.SEAT_POS` (884, 201, 5), 명령에는 `884.0 201 5.0`(`api.xyz` …); the
  bullet rewrapped, text otherwise unchanged); `tools/dev/sim/README.md` 3-4 `test_scarlet` row (K3b); `test_scarlet.py` doc + I2 comment;
  contract §7 (round-2 entry: `api.xyz`, the 9 lines, the halo / moon note); §12.4.1 above (a note: its figures were the simulator's
  until round 2 and hold in game since).

### 15.2 m2: the sim README sentence
`tools/dev/sim/README.md` §2 「11-03 에 고친 곳」, last bullet: "… 나머지 가운데 `az/tests_cm` 의 `test_chapter` · `test_fw_ap` · `test_px` ·
`gen_check` 는 11-05 홍련 I1 의 `run_all`(I1a · I1b · I1b 검증 1차, 1절대로 데이터팩 밖 사본에서)에서 돌았다: `test_chapter` · `test_fw_ap` ·
`gen_check` 통과, `test_px` 는 알려진 4e 하나만 실패(3-2). 아직 돌리지 않은 것은 `ar/tests/test_arena_fl.py` 하나다(다음 릴리스 게이트에서
돌린다)." Evidence: `run_all_i1a.log`, `run_all_i1b.log`, `run_all_i1b_f1.log` lines 2 / 3 / 5 / 34 (`ok cm_test_chapter`, `FAIL cm_test_px
… ['4e …']`, `ok cm_test_fw_ap`, `ok gen_check … GENERATOR CHECKS PASSED`); `test_arena_fl` runs only from `ar/tests/run_all.sh`, which
no I1 run used (no log names it). The cmsim md5s the bullet quotes still hold (f81cdc23 ×2, 7de1dd2c). No other README in
`tools/dev/sim` says a suite is not run yet.

### 15.3 Gates (the final tree of this round)
- **Regenerate** (`HR/i1/tools/gate_regen_f2.sh`, round 1's script logging to `out/fix_b2/gate`: kit `--resourcepack HR/rp_hr`, the rig,
  `regen_d0.sh` = `regen_all.sh` incl. the kit `--skip-rp` and the module + bf / fg kits): pass 1 after the generator edits changed
  exactly the 9 seat files (`spawn`, `core/deco`, `core/deco_seat`, `core/replay/start`, `seq/intro/k/{24,52,206,630}`, `seq/intro/skip`;
  10 lines); passes 1 / 2 ran while the suite and the READMEs were still being edited, passes 3 and 4 on the final sources give the
  same tree **9ac7fe78** (every file incl. this round's edits), pass 5 on the commit: `git status` empty, the tree = HEAD's. RP
  **62e15a3f8c3cf6fde51542ca216099a58b0de426** (4 785 files) before and after every pass; `check_mboss_pack` 4 mid / 4 chapter / 3 special /
  7 arenas / **0 problems** in each; `api.py --check` ok (29 parts + shadow, 47 clips / 280 events, 12 hit tables, 25 lines, 50
  presets, 104 sounds, 237 568 kit px, 115 owned paths). The RP did not change, so rplint 0 / atlas 12.955 M / the budgets of §13 stand.
- **Checkers** (`HR/tools/checkers.sh R: HR/i1/out/fix_b2/checkers`, 53 s, after `test_rig --rebuild` had finished): refs 44 → 44 (new 3 /
  gone 3), macro 3 357 → 3 436 (new 82 / gone 3), nbt 0 new, lint 193 340 → 215 716 (new 22 378 / gone 2) — all four outputs
  **byte-identical** to §13's `checkers_final` (0 unclassified; no checker reports the seat lines in either form).
- **Suites** — all 13 from a copy of `R:tools/dev/sim` (`HR/i1/sim_f2`, deleted after; `HR_DOCS=HR`; logs `HR/i1/out/fix_b2_suites/`):
  **all green** — `test_rig.py --rebuild` 86 / 86; `ev_dry.py` 67 / 67; `test_special_hr.py` 93 ok; `test_scarlet.py` **144 ok** (143 + K3b;
  I2: the full intro 6.34 b, the skip 6.34-6.50 b; every `cost` line identical to round 1's: fight average 505, the kit 66, the maximum
  without slice ticks 2 198, the 44 slice ticks 1 856 / 3 442); `pat_p1.py` 341; `test_reward.py` 51; `pat_ghost.py` 186; `test_hwamu.py`
  258 / 258; `test_moon.py` 50 / 50; `test_kit.py` 10 594 / 10 594; `test_arena_hr.py` 89 / 89; `ident_hr.py` pass (48 611 files in scope,
  changed 71 / new 4 310 / gone 0 = §13); `gen_check_hr.py` 28 / 28. The counts equal round 1's but for K3b. Also `test_scarlet hooks` on the
  tree (`fix_b2/test_scarlet_hooks.log`, 16 ok) and on the mutation of 15.1 (`test_scarlet_hooks_mut.log`: 15 ok, K3b FAIL).
- **run_all** (a fresh copy of `R:tools/dev/sim` in `HR/i1/sim` + the vcheck baselines, deleted after; log `HR/i1/out/run_all_i1b_f2.log`,
  643 s; outputs `HR/i1/out/run_all_i1b_f2/`): the 40 step lines identical to round 1's (34 ok incl. `cm_test_chapter`, `cm_test_fw_ap`,
  `gen_check` GENERATOR CHECKS PASSED, `check_nbtpath` 0, `check_mboss_pack` 0); failures = README 0-9's list: `test_m0diff` 40 (the FAIL
  lines byte-identical to round 1's, `HR/i1/out/m0diff_names/i1b_f2.txt`; normalised, the same 40 check names as the D0 base), `test_px`
  4e, `ident` 10, refs 30 / 7 new, macro 3 153 / 575 new, lint 6 767 / 2 959 new vs the old baselines (= §13 / §14).
- **Commit and loadcheck**: **4c81817** (15 files: `api.py`, `core.py`, `seq.py`, the 9 regenerated functions, `test_scarlet.py`, `README.md`,
  `tools/dev/sim/README.md`; tree 9ac7fe78). Loadcheck (from `R:`, `RLK_DEV=S: bash tools/dev/loadcheck.sh R: hr_i1b_f2`): `loadcheck
  hr_i1b_f2: 0 function load failure(s)`, exit 0, `Loaded 1870 advancements`, `Starting minecraft server version 26.3` + `Done (0.734s)`
  (log `S:mcsrv/hr_i1b_f2.log`, output `HR/i1/out/fix_b2/loadcheck_hr_i1b_f2.txt`): the `884.0 201 5.0` lines load.
- Scratch: the suite / run_all copies (`HR/i1/sim_f2`, `HR/i1/sim`), the mutation copy and the duplicate checker outputs
  (= `checkers_final`; `checkers.log` kept) are deleted, as are this round's draft and rewrap helpers; kept: the probes (`HR/i1/fix_b2/probe_seat.py` / `.txt`, `probe_moon.py` / `.txt`), the logs (`HR/i1/out/fix_b2*`,
  `run_all_i1b_f2*`), the gate script copy `HR/i1/tools/gate_regen_f2.sh`. `WT` clean, `RP` unchanged.

### 15.4 For the lead (not changed in this round)
The same whole-x / z form appears at two more points of `F:boss/scarlet` (K3b's info line; `probe_moon.py` / `probe_moon.txt`):
- the moon halo, `summon … 889 218 -33` in `core/deco` and `core/deco_re` (3 lines): designed 1 b in front of the moon disc's centre
  (`api.MOON_POS` (889, 218, −34) on the disc's south face; the theme builds the disc round that block corner), in game at (889.5, 218,
  −32.5): 0.5 b east of the centre and 1.5 b in front;
- the moon target of CS4, `facing 889 218 -34` (`seq/ending/m/land` 12 candidate lines, `seq/ending/turn_moon` 1): the aim is off by
  0.8° of yaw from C, at most 2.0° anywhere on the walk disc (≤ 0.36 b over the landing's 10 b).
Both would sit exactly on their points with the same helper (`one(…, exact=True)` for the halo, `api.xyz(mp, 3)` in `seq.py`'s two
`facing` lines). Not in this round's list, and the halo's offset is a look matter (the disc against the card) best confirmed in game or
on a render, so it is left for the lead.

## 16. I2 (11-05; brief `HR/i2_brief.md`): the player-size body (S2c skin + S2d) merged into `wip/hr`
`wip/hr` 4c81817 (I1b + its two verification rounds) + `wip/hr-s2c` **4e46cd7** (S2c fb4c16e on 66dafec = the I1a head, then S2d
c070a59 / 6feefb6 / c048830 / 10e4467 / 4e46cd7: her body is this pack's player avatar body wearing the user's skin
`HR/skin/scarlet_skin_64.png` unchanged, height 2.00 b, display scale 1, the 47 clips retargeted). Scratch of this step: `S:i2/`
(scripts `apply_req.py`, `gate_regen.sh`, `run_suites.sh`, `readme_edit.py`, the render tools `render/`; logs `logs/`, suite
outputs `out/`).

### 16.1 The merge (`git merge --no-ff wip/hr-s2c`)
Both sides since 66dafec: S2c + S2d changed 2 716 paths (2 697 under `F:boss/scarlet/**`, mostly `rig/**`; the rig sources; the
module sources `api.py` · `core.py` · `seq.py` · `s3lib.py` · `p1.py` · `p_ghost.py` · `stub_rig_manifest.json`; the registry;
`F:mboss/register`), I1b changed the kit / arena / README / sim sources and `api.py` · `core.py` · `seq.py` · `p_ghost.py` · the
registry. **83 unmerged paths**:

| path(s) | kind | resolution |
|---|---|---|
| `T:mboss_scarlet/core.py` :113-114 (the `spawn` comment) | source, both sides | **both**: S2d's prose (`husk scale 1.0, click` / `shield 1.2 x 2.4`) with I1b round 2's `{api.xyz(seat)}`; the command line under it was I1b's already (S2d left it alone); everything else in `core.py` auto-merged (I1b's `core/amb`, `AMB_EVERY`, `DECO_LOOK`, `one(..., exact=True)`, `core/deco_re` bloom, `core/look/go` re-looks, the replay `tp` through `api.xyz`; S2d's `ANCHOR_OFF` of fix round 3 and the stand-in tick particle) |
| `F:boss/scarlet/p/**` 52 (a1 2, a2 1, a3 5, a4 3, a6 1, a8 9, a9 3, a10 1, a13 18, r1 2, r2 5, r3 2), `seq/event/k/*` 14, `seq/intro/tick`, `spawn`, `F:mboss/register` (UU 68) | generated | S2d's side (`git checkout --theirs`), then regenerated (16.3) |
| `F:boss/scarlet/seq/intro/b/*` (AU 4 · UA 4 · DD 4 · DU 1: the intro's tick buckets renamed on both sides) | generated | S2d's file where it has one, else `git rm`; regenerated — the merged intro has new bucket names (`146_251`, `252_261`, `262_320`, `328_398`, `402_510`, `554_636`, `20_118`) |

Auto-merged and checked hunk by hunk (both sides present): `api.py` (S2d: the `BOSS` pin `(1.0, {w 1.2, h 2.4})`, `HEIGHT, HAT_TOP,
BRIM_D` 2.00 / 2.30 / 1.32, `SWORD_LEN, SCABBARD_LEN, SHADOW_R` 1.94 / 1.52 / 0.6, `ITEM_SWORD_LEN, ITEM_SWORD_SCALE` 2.03 / 1.375; I1b:
`SEAT_POS` (884.0, 201.0, 5.0), `xyz()` + its `_check_contract` assert, `KIT_PROPS['moon_halo']` p1b / p2b), `seq.py` (S2d: `me()` y 1.1,
`SEAT_RISE` / `SEAT_ASIDE` + the `rise` / `aside` moves at `stand` / `stand + 12`, the CS0 draw arc r 17, CS1 petal heights 1.74, repel
dust ring r 12 + petal burst 0.3, CS4 `petals_wind` 0.8, `SWORD_R` / `S0 = S1 = ITEM_SWORD_SCALE` / `TOSS_OFF`; I1b: `rock()` /
`rock_kill()` through `api.xyz`, `halo()` + its four calls and three restores, the walk-leg rule `..70`, the CS1 `leaves_dark` {n:20} /
{n:-20}), `p_ghost.py` (S2d: `at_body` 0.95 and the 13 call heights; I1b: the A13 fail's `scarlet_line yaw:90`), the registry (S2d:
`scale` 1.0, `hit` {1.2, 2.4}; I1b: the gate icon model + its comment). Rig sources (`scarlet_{skin,geometry,paint,pose,clips,
retarget}.mjs`, `scarlet_cine.mjs`, `build_scarlet_rig.mjs`, `scarlet_rig_api.md`), `scarlet_rig_manifest.json`, `stub_rig_manifest.json`,
`p1.py`, `s3lib.py`: byte-identical to 4e46cd7 (only S2d changed them). Kit / arena / README / sim README / contract: I1b's (S2d did
not touch them in the repository; its requests carry their changes, 16.2).

### 16.2 The requests `HR/requests/s2d.md` (generators and suites only; script `S:i2/apply_req.py`, exact text, each once)
| # | file : line (4c81817) | old → new | disposition |
|---|---|---|---|
| s2d-1 | `T:mboss_hr_fx_paint.py` :513-570 `paint_afterimage` / `paint_inside`; `T:build_mboss_hr_fx.py` :964 | the S2a silhouette (2.8 b, brim 2.47, ellipse head, long hair, robe / skirt, long arms) → the player-size figure of the request (`AI_S = 2.65`; brim y 2.00 ± 0.035, \|x\| < 0.66; crown 2.00-2.31, \|x\| < 0.25; square head 1.49-2.02; torso 0.74-1.50; two legs 0-0.75; slim arms from ±0.344, 1.40, half-width 0.11; the sword line from the left hand); the card `s0` / `s1` 2.8 → 2.65; docstrings | **applied** as written (rim / colour code, the 64 × 128 sprite, its box and `api.KIT_SPRITES` unchanged; `AI_CLAMP` and S3's call at the body + 1.2 kept). RP: `hr_kit/afterimage.png` is the only kit file that changed (looked at: `S:i2/afterimage_x4.png`) |
| s2d-2 | `T:build_mboss_hr_fx.py` :1339-1341 `SEAT`, :1332-1334 the `seat_rock` doc; `T:dev/sim/hr/tests/test_kit.py` :506 | rock (0, .375, 0) × (1.5, .75, 1.1) → (0, .12, −.185) × (1.2, .24, .64); bottle (.45, .75, .05) 0.5 → (.42, .24, −.15) 0.42; cup (−.4, .75, .2) 0.42 → (−.42, .24, −.15) 0.26; doc "1.2 x 0.24 x 0.64 b, its top 0.24 b … (under her thighs, behind her heels)"; test `+ 0.7` → `+ 0.19`; `SEAT_CLEAR` 1.8 kept | **applied**. The z sign checked rather than rendered: the stone is an `item_display` (`item_display:"none"`, a full block model) whose `translation` is in its own frame, and a display's local +Z is its facing (the renderer turns it by −yaw: yaw 0 faces +Z, south), the kit turns it to her facing (toward the moon) and the items use `^x ^y ^z` (^z forward): the stone spans 0.135 b in front of her anchor to 0.505 b behind, the items 0.15 b behind on her left / right = the rig's `SUP` (rig frame: forward −Z, `front −.135 back .505`, items z +.15) that `test_rig`'s seat-stone checks use — no negation. The check sheet's intro row (16.7) shows the rig's stand-in stone of the same `SUP` |
| s2d-3 | `T:build_mboss_hr_fx.py` docs (:750 … :1196, 17 presets); `test_kit.py` :383-392 `HEIGHT`, :396 / :399 `VARIANTS` | the call heights × ≈ 0.78 as listed (qi_arc 1.0, qi_ring 0.8 / 1.55 + the vanish 0.8, qi_vert 0.15, qi_fan 0.85, qi_wedge 1.0 / 0.85, qi_ribbon 1.0, qi_line 0.95 / 0.8, qi_cut 0.8, yellow_tell 1.0, ghost_burst 0.8-1.1, ghost_trail 0.45-0.95, ghost_flash 0.95, blink_bubble 1.0, shield_refill 1.1, petals_wind 0.8, leaves_swirl 1.1); `HEIGHT` 19 rows; `VARIANTS` qi_fan `h` 16 → 13, qi_vert 24 → 19 | **applied** (test_kit 10 594 / 10 594) |
| s2d-4 | `T:build_mboss_hr_fx.py` sizes (optional) | blink_bubble 1.8 / 3.0 → 1.4 / 2.4; ghost_burst 2.2 / 2.0 → 1.7 / 1.6; ghost_flash 2.4 → 1.9; star4 1.7 → 1.3 (+ doc); qi_ribbon 1.5 / 1.9 → 1.2 / 1.5; ghost_trail 3.6 / 4.0 → 2.8 / 3.1; ev_leave spread (.6, 1.2, .6) → (.5, .95, .5) (+ doc); leaves_swirl dust (1.2, 1.0, 1.2) → (1.0, 0.8, 1.0) | **applied** (cosmetic, the effects that enclose her body follow it; `yellow_tell` kept: a gameplay tell) |
| s2d-5 | suites | test_rig: S2d's `HR/tests/test_rig.py` (the repository copy had not changed since 7cc4a0c = S2d's base); ev_dry: S2d's three edits + its "S23 toss offset" block applied to the repository copy by `git merge-file` (base = 7cc4a0c's copy, ours = 4c81817's, theirs = `HR/tests`): 0 conflicts, I1b's halo checks kept; test_kit: s2d-2 / s2d-3; then `HR/tests` ← the repository copy for ev_dry / test_kit / test_scarlet / `lib/hrsim.py` / `lib/README.md` / test_rig (the old `HR/tests` files kept in `S:i2/hrtests_before/`) | **applied**; `HR/tests` == `T:dev/sim/hr/tests` (every file); test_scarlet `skip` re-run: full intro **6.76 b**, the skip 6.50-6.76 b (S2d's estimate 6.75-6.76; ≤ 7.05) |
| s2d-6 | README 「홍련」 | the eight edits (hit box, the stone, the rise / aside walk, ≈ 6.8 b, the shadow, the rig item → `HR/s2d/readme_rig.md`, the stone's top) | **applied** (16.6) |
| s2d-7 | merge notes | `core.py` :113-114 conflict, generated conflicts → either side + regenerate, `ANCHOR_OFF`, `g_dive` `blend: 1`, `HIP_DIR` | **applied** as the recipe (16.1, 16.3): no conflict marker left; the rebuilt rig and manifest = 4e46cd7 byte for byte |

### 16.3 Regeneration (README 0-4 order; `S:i2/gate_regen.sh`: `node tools/build_scarlet_rig.mjs --resourcepack HR/rp_hr` →
`python3 tools/build_mboss_hr_fx.py --resourcepack HR/rp_hr` → `bash HR/tools/regen_d0.sh R:`)
- Pass 1 (merge resolution + requests): the rig tree `boss/scarlet/rig/**` (2 600 functions) and `T:scarlet_rig_manifest.json` equal
  4e46cd7 byte for byte; `RP`'s `assets/rlk/**/mboss/scarlet/**` (153 files) equal `HR/rp_s2c`'s; the skin `textures/mboss/scarlet/skin.png`
  is byte-identical to `HR/skin/scarlet_skin_64.png` (sha1 7f9726be…); the atlas holds the same 28 `rlk:mboss/scarlet/*` ids as `rp_s2c`
  (order differs: `rp_hr` keeps its kit entries first and the builder re-adds its own at their old places, `skin` last; README 0-9's
  order note), 1 458 sources (1 478 − S2a's 48 + 28). The kit: of `RP`'s 177 kit files (`**/hr_kit/**`, font `mboss_hr`) only
  `textures/mboss/hr_kit/afterimage.png` changed (s2d-1); everything else in `RP` but `mboss/scarlet/**`, the atlas and README.md is
  identical to 62e15a3f. regen_d0: exit 0, `check_mboss_pack` 0; outside `F:boss/scarlet/**` only `F:mboss/register` (scarlet's
  `scale:1d` / `hit:{w:1.2f,h:2.4f}`). The intro's tick buckets are new (rise / aside events); `seq/**` 457 → 461.
- Pass 2 (same tree): worktree = index, tree **dddce7a7** both passes, RP aeab03c2 both (before the RP README edit).
- Passes 3 / 4 on the head f3231fe (after the container restart killed the first pass 3 inside the rig build, which had deleted
  1 415 `rig/**` files of the worktree; the rerun restored them): status empty, tree **48615482 = HEAD's** both passes, RP
  **89b6c70ce9e351811df7fb05443efd11e15bb053** (4 733 files) both passes, `check_mboss_pack` 0.

### 16.4 Suites (three-way: the repository copy at 4c81817, `HR/tests` before I2, S2d's — S2d's commit carries no suite)
| file | 4c81817 repo | `HR/tests` before | result (both copies now) |
|---|---|---|---|
| `test_rig.py` | = 7cc4a0c (df7cc18b) | S2d's (4c047dad; its base = df7cc18b) | S2d's |
| `ev_dry.py` | I1b round 1 (281f337f: + halo) | S2d's edits on 7cc4a0c's | `git merge-file`, 0 conflicts: both |
| `test_kit.py`, `lib/hrsim.py`, `lib/README.md` | I1b round 1 (kit_on, split check …) | 7cc4a0c's | repo's + s2d-2 / s2d-3 (test_kit) |
| `test_scarlet.py` | I1b rounds 1 / 2 (K3b, P14, P15, L5, Z1-Z3) | 7cc4a0c's | repo's |
| the other 12 files | — | = repo | unchanged |
`HR/tests` == `R:tools/dev/sim/hr/tests` file for file (the old `HR/tests` copies in `S:i2/hrtests_before/`); `HR/s1k/lib` and `HR/sr`
equal the repository's `hr/s1k`, `hr/sr`, so the runs from `HR/tests` (`S:i2/run_suites.sh`, `HR_DOCS=HR`, logs `S:i2/out/q1`, `q2`)
are the repository copy's.

### 16.5 Gates (merged tree; the suites / checkers / run_all ran before the two commits on the same tools and datapack — the
commits added only README / sim README text — and the regeneration passes 3 / 4 and loadcheck on the head f3231fe)
| gate | I1b 4c81817 | S2d 4e46cd7 | **I2 f3231fe** |
|---|---|---|---|
| regenerate twice | tree 9ac7fe78, RP 62e15a3f (4 785) | RP e947829b (its tree) | tree **48615482** = HEAD both passes, RP **89b6c70c** (4 733) both |
| `check_mboss_pack` / `api.py --check` | 0 / ok | 0 / ok | **0 / ok** |
| `test_rig.py --rebuild` | 86 | 152 | **152** (two builds byte-identical) |
| `ev_dry.py` | 67 | 63 | **68** (67 + S2d's S23 toss offset) |
| `test_special_hr.py` | 93 | — | **93** |
| `test_scarlet.py` (all sections) | 144 | sections only | **144**; skip: full intro **6.76 b**, skip 6.50-6.76 b (I1b 6.34 / 6.34-6.50) |
| cost (kit running): fight avg / max no-slice / slices max | 505 / 2 198 / 3 442 | 429 / 948 (no kit) | **502 / 2 189 / 3 444** (P1 514, P2 486, A8 547, A13 568, CS1 449, SQ1 477, repel 442, lead_stand 598; intro 370 / 904, ending 261 / 893, event 218 / 507; kit avg 66) |
| `pat_p1.py` / `pat_ghost.py` | 341 / 186 | — | **341 / 186** |
| `test_reward.py` | 51 | — | **51** |
| `test_hwamu.py` / `test_moon.py` | 258 / 50 | — | **258 / 50** |
| `test_kit.py` / `test_arena_hr.py` | 10 594 / 89 | — | **10 594 / 89** |
| `ident_hr.py` / `gen_check_hr.py` | pass / 28 | pass / 25 | **pass** (48 586 in scope, changed 71, new 4 285) / **28** |
| `run_all.sh` (copy, JOBS 2, 1 163 s) | 40 step lines | — | **the same 40 lines byte for byte** (m0diff 40, px 4e, ident 10, refs 30 / 7, macro 3 153 / 575, lint 6 767 / 2 959: README 0-9's) |
| checkers vs 35b82e5 | refs 44, macro 3 436, nbt 1, lint 215 716 | — | refs / macro / nbt **identical to I1b**; lint 212 466 (only the rig / cine `bad target '<uuid>'` instances, 22 324 → 19 074); **0 unclassified** (`S:i2/out/checkers_classify.txt`) |
| rplint | 0 | 0 | **0** |
| stitched atlas | 12.955 M (1 478) | 12.677 M (its pack) | **12.919 M** (1 458) ≤ 13.2 M |
| this boss's px (rig / kit / gate icon) | 83 712 / 237 568 / 4 096 | 47 872 / — | **47 872** (27 + skin) / **237 568** / **4 096** = 289 536 ≤ 0.43 M |
| elements at rest | 2 304 | 224 | **224** ≤ 6 500 |
| loadcheck | hr_i1b_f2: 0, 1870 adv. | hr_s2d_f3: 0 | **hr_i2: 0 failures, exit 0, `Loaded 1870 advancements`**, 26.3, `Done (1.219s)` |
Rig: 29 parts, 47 clips, 2 084 key files / 18 800 keys, 2 600 functions (5.70 MB), 62 models; module 1 149 (S3 275, S4 413, `seq/**` 461);
`F:boss/scarlet/**` 4 178; kit 429 functions (unchanged count).

### 16.6 Docs
- README 「홍련」 (`S:i2/readme_edit.py`, exact text): the opening paragraph (husk scale 1.0, click 1.2 × 2.4; the body is the user's
  skin on the player avatar body, the props / kit / arena ours), CS0 (the low stone 1.2 × 0.24 × 0.64 b with its top 0.24 b; the rise
  0.4 b toward the moon and the 1.1-b step aside, feet stepping; ≈ 6.8 b, the skip 6.5-6.8 b), the sheathe paragraph (S2a's 1.93 / 2.14 /
  0.38 b replaced by S2d's `SH0`), the rig item = `HR/s2d/readme_rig.md` + where the skin lives (S2c's sentence: `tools/scarlet_skin.mjs`
  base64 → RP `textures/mboss/scarlet/skin.png`, atlas `rlk:mboss/scarlet/skin`) and the design sentences the old item carried
  (left-handed, the brim's four squares, no original costume piece), the kit's stone line (top 0.24 b = her thighs' underside, hip
  0.385 b), the files item (module 1 149, `boss/scarlet/**` 4 178, the rig builder's sources / outputs / manifest blocks /
  `scarlet_retarget.mjs --dump`, the `test_rig` checks), the cost line (16.5). 0-3's generator row names `scarlet_skin.mjs` /
  `scarlet_retarget.mjs`; 0-4's RP block gains a comment line under the rig (the skin file and its atlas id — new in `RP` since I1b's
  S2a rig, S2d adds no file over S2c). 0-9 unchanged (nothing new known).
- RP README (`HR/rp_hr/README.md`, from `HR/s2d/rp_readme_rig.md`): §2's `scarlet` row (the avatar boxes + the user's skin), §3's hr
  row (27 sprites + the skin = 47 872 px, 62 models), a note block after §3's table (the rig builder's filter-then-push, the 15 body
  models = the avatar's, the skin bytes, the brim / crown, and the kit's redrawn afterimage), §4's budget line (홍련 0.29 M:
  `scarlet` 0.048 + `hr_kit` 0.242; 12.919 M after I2). Not the version log (no release).
- `R:tools/dev/sim/README.md` 3-4: the `test_rig` (S2c / S2d checks, 152 with `--rebuild`), `ev_dry` (the thrown sword's scale /
  radius and toss offset, 68) and `test_kit` (the call heights, the seat items) rows.
- Contract §7: the I2 entry (the merge, the dispositions, the numbers).

### 16.7 Render
`HR/renders/i2_check.jpg` (640 × 884; `S:i2/render/`: S2d's `b.sh` / `r.sh` / `pose.mjs` / `u1.py` pointed at `WT` and `RP`, the debug
pack built by `b.sh` — the build left the tree and `RP` unchanged — and deleted after): rest front / side / back / ¾ beside the player
avatar, the P2 knot and sash, the ghost form, the five hat states (worn on the head), the iaido stance and the guard, and an I2 row:
the intro seated on the stone (the rig's stand-in stone of `SUP`, the frame s2d-2's kit stone matches: under her thighs, behind her
heels, the bottle on her left). The skin shows on every normal-form panel.

### 16.8 Commits on `wip/hr` (never pushed; trailer as the brief)
**254c329** the merge (the resolution + the regenerated tree; the request paths — the kit's two sources, its manifest, `fx/**`, the
three suites — still at 4c81817, so the merge commit is the merge alone), **f3231fe** the requests, the suites and the README / sim
README (head; tree 48615482). Outside the repository: `HR/rp_hr` (whole pack 89b6c70c…, its README), this file, `progress.md`,
contract §7, the render. Afterwards `HR/wt_s2c` removed (`git worktree remove`; the branch `wip/hr-s2c` kept) and `HR/rp_s2c` deleted.

### 16.9 For the lead
- **The merge commit is not separately gate-checked**: 254c329's kit outputs are 4c81817's and its suites the old ones (`test_rig`
  86-check copy against the new rig would fail); the head f3231fe is the checked state.
- **s2d-4 applied though optional** (the kit effects that surround her body × 0.78): revert by request if the bigger S2a-size bursts
  were preferred in game.
- **The intro's end distance is now 6.76 b** (I1b's 6.33 b + S2d's 0.4-b rise and 1.1-b step aside; the skip 6.50-6.76 b): inside
  PLAN §3.1's ≤ 7 b and I2's 7.05 limit, but 0.24 b of margin.
- Unchanged and still open (R-late part 2): S2d's residuals (the kneel's knee hinge 47-54° at lead_down 6-8 / kipup 7-9, arm turns up to
  108°/t, the hat layer 0.02 b over the brim's inner ring, C3 hat over her head at lead_down 41-43 / lead_stand 30-31, ending 25-26, walk
  skating); I1b's open items (§15.4: the halo / CS4 moon points written with whole x / z; README 0-9's m0diff budget question).
- The cost: 505 → 502 average; the per-tick bounds hold (2 189 ≤ 3 000, look-job slices 3 444 ≤ 5 k).

## 17. F-I (11-05/06; brief `HR/fi_brief.md`): the three review-fix lanes merged into `wip/hr`
`wip/hr` **f3231fe** (I2: I1b + S2d's 2.00-b player-size body) + the fix lanes, each branched from 4c81817 (the I1b head) and
committed after its round-1 verifier fixes: `wip/hr-f3` **cbe4dc2** (items / reward / framework: HR-05, 08, 09, 10, 11, 33,
34, 35, HR-39's game part), `wip/hr-f1` **67504a7** (gameplay: HR-01/04/06/07, the P1 pressure package HR-13/14/18/25/26/38,
HR-15/19/22/27/28), `wip/hr-f2` **3c69fcc** (kit / sequences / arena / text: HR-02/12/16/17/23/24/29/30/32/41-46, LF-01/02),
in that order (`git merge --no-ff`); then the lanes' F-I requests, HR-03 and HR-31 (the two findings left for F-I), F1's /
F2's open points, the docs. Scratch of this step: `S:fi/` (merge resolutions `res/`, docs scripts `docs/`, the icon renderer
`icon/`, the tail probe `tails/`, suite / regen logs `out/`, `logs/`).

### 17.1 The merges
| merge | commit | conflicts | resolution |
|---|---|---|---|
| f3 cbe4dc2 | **98a5fc2** | none (core.py cleanup, api.py §9b, README, five suites auto-merged) | every F3 hunk = `git diff 4c81817 wip/hr-f3` line for line (checked per file); the module regenerates to the merged files unchanged |
| f1 67504a7 | **d17c331** | README ×3; generated ×5 (`cleanup`, `p/a9/tick`, `p/a13/k/198`, `p/r2/k/36`, `37`) | README: the opening paragraph keeps S2d's body text + F1's TC tier ("자영 연참의 베기만 따로 37 %"); the module count and the cost line keep I2's, restated after the F-I regeneration (17.6). Generated: F1's side, then `build_mboss_scarlet.py` from the merged sources (the cleanup = F3's `reset * hr` form: F1's three new `CORE_FP` names need no line). Sources (`api.py`, `core.py`, `ai.py`, `p1.py`, `p_ghost.py`) and the suites `pat_p1` / `pat_ghost` / `test_scarlet` auto-merged: F1's hunks present unchanged (`S:fi/res/sides.py`) |
| f2 3c69fcc | **55850a0** | sources ×9 files / 21 hunks; generated ×25 | below; generated (`fx/p/**` 15, `p/**` 9, `T:mboss_hr_fx_manifest.json`): F2's side, then `regen_d0.sh` from the merged sources (`check_mboss_pack` 0) |

The f2 source hunks (resolver `S:fi/res/resolve.py` + one resolution file per source in `S:fi/res/`; afterwards every side's
added lines checked present unless a hunk replaced them on purpose, `S:fi/res/sides.py`):
| file | hunks | resolution (every side kept) |
|---|---|---|
| `T:build_mboss_hr_fx.py` | 4 preset docs (`qi_vert`, `qi_fan`, `qi_wedge`, `qi_line`) | F2's across-the-aim text with S2d's call heights (A3 the body + 0.15, A1 + 0.85, A3 h5 + 1.0 / A7 + 0.85, A5 + 0.95, A8.9 + 0.8); the `qi_wedge` conv / pre (F2's burst point) unchanged |
| `T:mboss_scarlet/p1.py` | 4 | F1's `trail()` / `tail()` **and** F2's `follow()`; A3's `qi_vert`: F2's per-hit `ahead` / `yaw` with S2d's `^0.15` and `h 27`; A5's line: F2's `^5 … ^1.5`, `len 100` at S2d's `0.95`; A9's streak: F2's `K.pw('qi_cut', core.a9)` at S2d's `0.8` |
| `T:mboss_scarlet/p_ghost.py` | 1 | the A7 yellow tell at S2d's `at_body(1.0)` between F2's `follow_on` / `follow_off` |
| `T:mboss_scarlet/seq.py` | 1 | the repel petals at S2d's `~0.3` with F2's kept kick flash (`keep_on` / `keep_off`) |
| `pat_p1.py` | 4 | the docstring sections `f1` + `fx`, `SECTIONS` `…, 'f1', 'fx'`, F1's `sec_f1` then F2's `sec_fx`, `main()`'s dict both |
| `pat_ghost.py` | 2 | `SECTIONS` `…, 'f1', 'kept'`; F1's `sec_f1` (+ helpers) then F2's `sec_kept` |
| `test_kit.py` | 1 | `HEIGHT`: S2d's rows + F2's `scarlet_line (1.3, 1.62)`; `VARIANTS`: F2's added variants with S2d's `qi_fan h 13`, `qi_vert h 19` |
| `test_scarlet.py` | 1 | `rec()` keeps F1's `rvw=` and F2's `hold=` |
| `README.md` | 2 | CS0's wind at the player (F2 HR-46) on S2d's rise / aside text; the cost line restated later |
No duplicate top-level definitions in the merged suites (AST check). One interaction of two lanes showed only in the gate
(17.6): F3's test_reward HR-35 / HR-11 buff checks read every actionbar of the coda, and F2's round 1 blanks the actionbar
once at the coda's start (`seq.HUD_BLANK`), so their list began with `''` (2 FAIL on the merged tree; F3 had proved its
check on F2's 547480d, before that blank). test_reward now leaves the empty actionbar out (it is F2's; ev_dry checks it):
61 / 61. The merge commits are the resolutions + the regenerated
tree; the kit's RP side was built after the merges (17.3), so 55850a0's `RP` is still I2's (89b6c70c).

### 17.2 The body change under the lanes (brief step 3)
The lanes built and tested on S2a's 2.55-b body; `wip/hr` has S2d's 2.00-b body (hit 1.2 × 2.4, `HEIGHT` 2.00, `HAT_TOP` 2.30;
s2d-1 … s2d-4: every call height at her body × ≈ 0.78, the afterimage sprite, the seat stone). Every lane change that places
something at her body, re-checked:
| lane change | on the 2.00-b body | change at the source |
|---|---|---|
| F2 HR-12 qi call heights (A3 `qi_vert`, A5 line, A9 streak, A7 tell; the kit docs) | the conflicts (17.1) resolved at S2d's heights | as 17.1 |
| F2 HR-12 `view` checks (`test_kit`) | the camera "looks at her chest" = the module's default effect height at her body (F2: 1.3 b = S2a's `s3lib.fx` default): with S2d's 1.0-b default the A1 hit crescent (flat, at 1.0) showed 521 px in first person (≥ 1 500) | `test_kit`: `CHEST = 1.0` (S2d's × 0.78 of 1.3; F5 pitch 28.4°, first person 14.5°, were 22.6 / 7.6): A1's crescent 2 317 px FP, every contact effect ≥ 1 500 both views |
| F2 A1 fan (F5 floor 250 px, `test_kit`) | S2d's fan is h 13 (was 16; s2d-3): 189 px in F5 | `test_kit`: the floor scales with its area, 250 × (13 / 16)² = **165** (S2d's smaller fan, not a new defect; for the lead, 17.9) |
| F2's `qi_wedge {roll:90}` test variant (`test_kit` presets) | at S2d's lowest wedge call (A7 at the body + 0.85) the face-mode wedge's lower corner reached 0.05 b under the floor (r 36 = the test default; no module call uses roll 90: A3 h5 r 46 roll 40 at 1.0, A7 r 14 roll 30 at 0.85 stay ≥ 0.26 b over it) | the variant's reach × 0.78 (r 28), as S2d scaled `qi_fan` / `qi_vert` (s2d-3) |
| F2 HR-17 the death line / petals / bolts (kept cards) | at the player (`at_player(1.3)`, eye 1.62): the player's body, unchanged; CS3's kick flash at her `head` anchor (the rig's anchor follows her body) | none |
| F2 HR-23 followers (A13 / R2 / A10 tells, A6 bubble, A4 ribbon) | they keep the lead's x / z and their own height over her: the heights are S2d's call heights (A7 tell 1.0, the others the kit default 1.0) | none |
| F2 HR-45 first-person anchors | the player's eye / view ray / avatar chest: the player's body | none |
| F1 HR-28 A10 dive line (`qi_line … ~ ~1.0 ~ facing entity <lock>`) | S2d's rule puts body lines at 0.8 (the A9 / A8.9 lines); F2's HR-12 turns every `qi_line` 90° (f2-7) | `p1.py` `build_a10`: `positioned ~ ~0.8 ~ facing entity <lock> feet rotated ~-90 ~` (F1 request 2 + f2-7) |
| F1 HR-28 trails (`trail()` at `~ ~1.2 ~`) | the same height as the P2 `afterimage()`, which S2d kept at 1.2 (the 2.65-b card, `AI_CLAMP`) | none (F1 request 2's rule: equal to `afterimage()`) |
| F1 HR-15 the disc lock | a floor marker at the player's feet; the disc at `api.DISC` y 0.9 over the floor (blade rows 0-1.65) | none |
| F1 HR-27 D2 / D4 at ±55° | her body is shorter: inside the F5 view as before (pat_ghost f1 passes) | none |
| F1 HR-14 tails (`TAIL_MOVE` 4) | 5a below | none |

**5a — the tail move on S2d's rig** (`S:fi/tails/tail_probe.py`, out `S:fi/tails/probe.txt`): for each kept tail (A1 18, A2 16,
A3 73, A4 38, A9 32, A10 26, R1 = `g_reform` 7, R3 = `g_reform` 9) the move clip the recovery plays (walk / strafe_l /
strafe_r / P2 glide) replayed from its shipped key files starting at the attack clip's shown pose (the client blends from
it). Largest per-tick part turn over the hand-over: ≤ 50°/t into a walk / strafe (A9's sword), ≤ 56°/t into the P2 glide
(A3's left arm) — the glide's own entry from idle is 57°/t, the attack clips' own swings 75-109°/t, the rig's snap
threshold 60°/t; shifts ≤ 0.27 b/t. No pose pops: `api.TAIL_MOVE` stays 4. Render `HR/renders/fi_tails.jpg` (A2 → strafe,
A3 → glide, A9 → strafe, R1 → glide; the hand-over tick and +1 / 2 / 3 / 5 t; debug pack built by the rig builder's
`--debug-dp`, deleted after).

**5b — A3 h4's crescent**: at 3.0 / 3.5 b ahead (where line(5.0, 1.8) reaches) it stands behind a player at the 2.4-b chain
stop: first person 0 px (F5 3 319 / 4 123 px, vs 2 259 at 2.0 b), so F2's `view` check fails; **kept at 2.0 b** (F2's
choice: still before that player). PLAN §4.3 A3 says so.

### 17.3 The requests (`HR/f/f<n>_requests.md`, the F-I items)
| # | disposition |
|---|---|
| F1 1 (api hunks = the contract change) | **applied**: contract §7 F1 entry (verbatim from `f1_doc_changes.md`) + the F-I entry |
| F1 2 (A10 dive line 1.0 → 0.8; `trail()` = `afterimage()`) | **applied** with f2-7 (17.2); `trail()` unchanged (S2d kept `afterimage()` at 1.2) |
| F1 3 (README counts / cost after the merge) | **applied** (17.6: module 1 144, `boss/scarlet/**` 4 190, the cost line) |
| F1 4 (the suites' run copy) | **applied**: `HR/tests` ← the repository's suites after every suite change (`S:fi/sync_tests.sh`; `HR/tests == R:tools/dev/sim/hr/tests`) |
| F1 5 (names: `#ai_nn #ai_bs #ai_tmc`, `#grs` 4 / 5, `rlk_hr_gln`) | **applied** (contract §2); cleanup: F3's `reset * hr` resets them (no line needed) |
| F1 6 / 7 (S5: re-measure T1 / T2 / T9, G1-G3; the probe's disc lock / attribution) | for S5 (not F-I) |
| F1 8 (F2 changing `afterimage`) | checked: F2 did not change `afterimage`'s `len` or pool; pat_p1 f1 F7 / F10 pass in the gate |
| F1 9 (HR-14: "walk / strafe" as written) | **applied**: PLAN §4.1 / §4.3 / §4.4 and contract §3.5 as F1 wrote them |
| F1 10 (the tail move over the clips' follow-through) | checked on S2d's rig (5a): no pop |
| f2-1 / f2-2 / f2-10 (merge notes: F2's suite sections and fx call lines) | **applied** (17.1) |
| f2-3 (the kit's RP files into `RP`) | **applied**: `build_mboss_hr_fx.py --resourcepack HR/rp_hr`: + 5 item models / 5 item definitions (`qi_arcf_0..3`, `qi_wedgef`), 24 glyph PNGs, `font/mboss_hr.json` (31 glyphs); the kit's RP tree = `HR/rp_f2`'s but `afterimage.png` (S2d's s2d-1); rplint 0 |
| f2-4 (the accepted lint line `seq/ending/start:4 tp shape …` gone) | **confirmed, changed**: gone in the F-I checker run (17.6); `checker_accept_b.md` gains a dated F-I note saying so instead of deleting the I1a / I1b record's rows |
| f2-5 / f2-9 (cost, info) | restated with this tree's cost run (17.6) |
| f2-6 (`rlk_body` / `rlk_av` with S2d) | checked: S2d did not change the view system (`F:view/**` untouched by S2c / S2d); F2's anchors pass `test_kit view` on the merged tree |
| f2-7 (A10's dive `qi_line` turned by `rotated ~-90 ~`) | **applied** (`p1.py`; generated `p/a10/k/20`); test_kit `qline` (every module `qi_line` by its aim) passes |
| f2-8 (`start_go` bars guard) | **applied, changed**: `T:build_mboss_core.py` `w('start_go')`: `execute unless score #mbBarOff mb matches 1 run function rlk:mboss/bars_show` (+ a comment line). `check_mboss_pack` refused it (FN-f: "only bars_off / bars_on / fight_vars / cleanup_fight / world may touch #mbBarOff"), so its FN-f rule now pins that one line in `start_go` (`HR_FN_LINES['mboss/start_go']`, and any other `#mbBarOff` line there is a problem). `ident_hr`: `F:mboss/start_go` in its own group "F-I review fixes (pack-wide lines)" (not inside "contract §5 FN outputs (S1)", which mirrors the contract's list). test_scarlet B3b runs on the real file ("guarded"). Other bosses: `fight_vars` (start_go line 7) zeroes the flag, so `bars_show` runs as before (run_all, 17.6) |
| f3 r1 (shared-file hunks; ident_hr's F3 group) | **applied** (auto-merged; the group kept) |
| f3 r2 (the buff's actionbar under F2's HUD hold) | **confirmed**: test_reward `words` (the hold as behaviour, a coda run with the real `player/hud/tick`) passes on the merged tree |
| f3 r3 (reward_ev's counter rule) | for S5 |
| f3 r4 (in-game watch list) | **applied**: README 0-9 「홍련 — 게임에서 확인할 것」 |
| f3 r5 (test_scarlet cleanup check) | **applied**: test_scarlet `cleanup` C3 (after won / abort / cleanup objective hr holds only `api.EV_FP`, storage `rlk:hr` no `seq`) |
| f3 r6 (HR-35 buff wording) | for the lead (unchanged: two numbers on the subtitle, the third on the actionbar) |
| f3 r7 (PLAN / contract text) | **applied** (17.5) |

### 17.4 HR-03 and HR-31
- **HR-03** (the item icon; lead decision 11-05). `T:scarlet_geometry.mjs`: `itemSwordIcon()` / `ICON` = the same sheathed
  sword drawn in model px = GUI px (in `IN_UNITS`, no ghost twin): along the slot's diagonal (−45° about z, 20 px long,
  14.1 px across each way, inside 16 × 16), pommel 2.4 / grip 2.0 / guard bar 5.2 (2.4 deep) / mouth collar 2.8 / scabbard
  2.4 (its decorated `scab` face toward the camera) / crimson cord 2.8 / middle band 2.8 / chape 2.6 GUI px wide; rig sprites
  only (0 new px). `T:build_scarlet_rig.mjs`: the icon model's display = the vanilla generated item's (`gui` as drawn,
  `fixed` 180°, `ground` half size + 2 px up), `gui_light front`; `items/mboss/scarlet/item_sword.json` = `minecraft:select`
  on `minecraft:display_context`: `["gui","fixed","ground"]` → `item_sword_icon`, fallback `item_sword` (the hands, the coda's
  `item_display` none); the manifest's `item_sword.icon` block (model, contexts, display, dims). The stray guard card:
  `itemSword()`'s `cardY('guard', …)` takes the item's shift `s` (S2d's −0.51 b; the card was at model y 7.98, now 2.05 on
  the plate's top 2.04). 63 models (was 62). test_rig (+9): the guard card on the plate; the select; the icon's textures
  (rig sprites) / transforms (= the manifest) / `gui_light`; at GUI × 2 every lit row but the two end corners ≥ 2 px (3-10),
  ≥ 100 px (200), one 8-connected piece — the rig model printed for comparison (30 px, 1 px per row); inside / spanning the
  slot; long parts ≥ 2 GUI px; points like a vanilla sword; the dropped icon upright over the floor. Render
  `HR/renders/fi_icon.jpg` (the icon at 16 / 32 / 64 px, × 8 / × 4 / × 2 and native, beside the rig model; `S:fi/icon/
  icon_render.py`: textured, pixel-centre sampling as the GUI draws items). On f3231fe the select check, the row check (the
  rig model's 1 px rows) and the guard check (7.98 vs the plate's 1.86-2.04) fail.
- **HR-31** (the CS3 → CS4 seam; lead decision: a hard cut at CS4 tick 0). `seq.py`: `SEAM_CUT = ('white', 0, 2, 1)`,
  `s.at(0, K.ovl(*SEAM_CUT))` in `build_ending` → `seq/ending/start` ends with `fx/hud/ovl {g:"white",in:0,hold:2,out:1}`:
  fully white over ticks 0-1 while the hat's 1-t interpolation from the repel's DOWN (beside her, 1.58 b from the ending's
  tick-0 hat crown on S2d's rig) to over her face runs; nothing else of the ending's staging before tick 16. White = the
  lethal kick's impact (the original's cut has no flash; the decision allowed black or white; the kept kick flash cards
  outlive the 3 t). test_rig (+1): `SEAM` repel 102 → ending 0: every anchor within its hand-over TOL but the hat (and the
  head, which settles 0.152 b into LY's chin-up rest: allowed ≤ 0.25 there), the hat only under a hard cut at the ending's
  tick 0 (ovl white / black, in 0, hold ≥ 2); ev_dry (+1): the cut at tick 0 = `seq.SEAM_CUT`, no other effect in ticks 1-3.

### 17.5 Docs
- `HR/PLAN.md` (backup `S:fi/docs_before/PLAN.md`; scripts `S:fi/docs/{f1,f2,f3,fi_plan}.py`, exact text, each once): F1's
  §3.8 / §4.1 / §4.3 (A1 A2 A3 A4 A6 A9 A10) / §4.4 (preface, R1-R3) / §4.5 (the TC tier, D2 / D4, A7's lock) / §4.6 / §4.7
  (table, counter, rear, no empty band) / §4.8 / §5.3 / §5.6 / §9.2 items; F2's 1-16, 22, 23, 25 (A10's line turned −90° and
  at 0.8 b with F1's text); F3's P1-P13; F-I: §4.1's tail note (5a), §4.3 A3 h4 (5b), §3.7 E1's hard cut (HR-31), §7.4.1 /
  §7.3.2 / open point (8) (HR-03).
- `HR/contract.md` (backup `S:fi/docs_before/contract.md`; `S:fi/docs/{contract_sec,c7_lanes}.py`): §1 (F3 C4; the icon in
  S2a's RP row), §2 (F1's names and test ids, F2 17, F3 C1 / C2, the icon id), §3.1 (F2 18 / 22 / 23 + f2-8 as applied),
  §3.3 (F2 19 / 24), §3.5 (F1), §3.7 (F3 C3; HR-03), §6 (F2 20); §7: the F1, F2 and F3 entries and the F-I entry.
- README (WT): the 「홍련」 section (f2-8 as applied, CS4's opening cut, the item's icon, 63 models, the module / file counts,
  the cost line), 0-9's new 「홍련 — 게임에서 확인할 것」 list (F3 r4's three points, I1b's halo / lotus looks, F2's
  first-person anchors and overlay steps, the icon, the seam); `tools/dev/sim/README.md` 3-4 rows (test_rig, ev_dry, test_kit,
  test_scarlet); the RP README (`HR/rp_hr/README.md`: the font row U+EC20-EC37, the kit's face models, the icon; backup
  `S:fi/docs_before/rp_README.md`).

### 17.6 Gates (the merged tree: suites / checkers / run_all / loadcheck on faeaf9c's datapack and tools — b3533f0 changes only
test_reward, rerun; the docs commit only README / sim README text — and the regeneration passes 3 / 4 on the head)
| gate | I2 f3231fe | F1 67504a7 | F2 3c69fcc | F3 cbe4dc2 | **F-I** |
|---|---|---|---|---|---|
| regenerate twice | tree 48615482, RP 89b6c70c (4 733) | tree c5147dca | 99c64c0a / RP 78b0929d | ae945e7d | passes 1 / 2 on faeaf9c: tree **ffc727c8** = HEAD, RP 71521082 (4 769) both; passes 3 / 4 on the head 3741fc4: tree **f5d573ad** = HEAD, RP **27d6ae57b4d3dce641b34dfe246a0008715778a4** (4 769 files, after the RP README edit) both |
| `check_mboss_pack` / `api.py --check` | 0 / ok | 0 / ok | 0 / ok | 0 / ok | **0 / ok** |
| `test_rig.py --rebuild` | 152 | 86 | 86 | 86 | **162** (152 + HR-03 ×9 + the seam) |
| `ev_dry.py` | 68 | 67 | 76 | 67 | **78** |
| `test_special_hr.py` | 93 | 93 | 93 | 98 | **98** |
| `test_scarlet.py` (all sections) | 144 | 176 | 153 | 144 | **188** (144 + F1 32 + F2 9 + C3 ×3); B3b "guarded" (the real `start_go`) |
| cost: fight avg / max no-slice / slices max | 502 / 2 189 / 3 444 | 532 / 2 198 / 3 442 | 510 / 2 291 / 3 475 | 505 / 2 198 / 3 442 | **535 / 2 282 / 3 477** (kit 81; P1 559 · P2 524 · A8 552 · A13 574, CS1 457, SQ1 478, repel 445, lead_stand 600; the highest tick without a slice CS1 #sq 172 (kit 2 011), the 44 slice ticks avg 1 846; intro 325 / 911, ending 263 / 923, event 220 / 523) |
| `pat_p1.py` / `pat_ghost.py` | 341 / 186 | 381 / 201 | 347 / 190 | 341 / 186 | **387 / 205** |
| `test_reward.py` | 51 | 51 | 51 | 61 | **61 (after F-I's merge fix, 17.1; 59 / 61 before)** |
| `test_hwamu.py` / `test_moon.py` | 258 / 50 | 258 / 50 | 258 / 50 | 283 / 55 | **283 / 55** |
| `test_kit.py` / `test_arena_hr.py` | 10 594 / 89 | 10 608 / 89 | 13 422 / 93 | 10 594 / 89 | **13 435 / 93** |
| `ident_hr.py` / `gen_check_hr.py` | pass / 28 | pass / 28 | pass / 28 | pass / 28 | **pass / 28** |
| `run_all.sh` | 40 step lines (README 0-9's) | — | — | the same 40 | **the same 40 step lines as I2 (34 ok; `test_m0diff` the same 40 failure names and per-tick figures (+6.59 / +5.94 / +6.71 / +6.99), its "new fake players" detail + `#hrMoonRun` (F3); `ident` the same 10 (4a: 1 615 → 1 620 changed engine files = F3's `view/{tick,ride_tick,sel_xhair}`, `lvup/tick`, `items/hook/on_dash`); refs 30 / 7; macro 3 153 / 575 → 3 161 / 583 (+ 8: F2's kit / module storage macro calls, the classified kind); lint 6 767 / 2 959; README 0-9's known failures only; 476 s, JOBS 2, copy `S:fi/sim` + the vcheck baselines, log `S:fi/out/run_all_fi.log`, step outputs `S:fi/out/run_all_fi/`)** |
| checkers vs 35b82e5 | refs 44, macro 3 436, nbt 1, lint 212 466; 0 unclassified | — | — | — | refs 44 (missing refs 66 → 68: the summary line), macro **3 446** (+10: the kit's storage macro calls 56 → 64, A9's streak and CS4's band with storage, F2), nbt 1, lint **212 467** (+1: F3's two `time query gametime` in `hw_ctr_q` / `hw_dash`, two base findings shifted by F3's view lines; gone: F2-4's `seq/ending/start:4 tp shape` and two old line numbers); **0 unclassified** (`HR/i1/tools/chk_classify_fi.py` = chk_classify_b + 5 F-I kinds; `S:fi/out/checkers_classify.txt`) |
| rplint | 0 | 0 (rp_f1) | 0 (rp_f2) | — | **0** |
| stitched atlas | 12.919 M (1 458) | — | — | — | **12.919 M** (1 458; the kit's face models and the icon add no sprite) |
| loadcheck | hr_i2: 0, 1870 | hr_f1_r1: 0 | hr_f2_r1: 0 | hr_f3: 0 | **hr_fi: 0 failures, exit 0, `Loaded 1870 advancements`**, 26.3, `Done (1.286s)` (`S:fi/out/loadcheck_hr_fi.txt`, `S:mcsrv/hr_fi.log`) |
Module 1 144 functions (S3 284 · S4 399 · `seq/**` 461; I2 1 149: S3 275 · S4 413 · 461); `F:boss/scarlet/**` 4 190 (I2 4 178);
kit 446 functions; rig 2 600 functions, 63 models.

### 17.7 Renders
`HR/renders/fi_icon.jpg` (HR-03: the slot icon at 16 / 32 / 64 px, magnified and native, over the vanilla slot grey, beside the
rig model it replaces in the slot), `HR/renders/fi_tails.jpg` (5a: A2 → strafe, A3 → glide, A9 → strafe, R1 → glide; the
hand-over tick and +1 / 2 / 3 / 5 t on S2d's rig).

### 17.8 Commits on `wip/hr` (never pushed; trailer as the brief)
**98a5fc2** merge f3, **d17c331** merge f1, **55850a0** merge f2 (each the resolution + the regenerated module / datapack; the
kit's RP side after), **bbe3002** the requests (A10's line, the `start_go` guard + `check_mboss_pack` FN-f + `ident_hr`, C3) and
the body-change test adjustments, **faeaf9c** HR-03 / HR-31, **b3533f0** test_reward's merge fix (17.1), **3741fc4** README /
sim README (head). Outside the repository:
`HR/rp_hr` (the kit's RP files, the icon, its README), `HR/PLAN.md`, `HR/contract.md` (§1-§3, §6, §7 F1 / F2 / F3 / F-I),
this file, `progress.md`, the renders. Afterwards `HR/wt_f1`, `wt_f2`, `wt_f3` removed (`git worktree remove`; the branches
kept), `HR/rp_f1`, `rp_f2`, `rp_f3` deleted, `S:fi/render/dbg` and the run_all copy deleted.

### 17.9 For the lead
- **A1's fan floor**: S2d's player-size fan (h 13 at the body + 0.85) shows 189 px from the default F5 camera; F-I scaled F2's
  250-px floor with the fan's area (165) instead of enlarging it. If the fan should read bigger, it is `p1.py` A1's `h=13`
  (S2d's s2d-3) — a look call, not changed here.
- **The view camera's chest**: `test_kit` now models "the player looks at her chest" at 1.0 b (S2d's × 0.78 of S2a's 1.3, the
  module's default effect height); her avatar torso spans 0.74-1.50 b, so a player may look a little higher. At 1.1 b the A1
  hit crescent drops to 1 044 px in first person (< 1 500): if the lead prefers a higher chest, A1's flat crescent wants
  raising (`fx_arc` h for A1) — open.
- **f2-8 touched the framework check**: `check_mboss_pack`'s FN-f rule now allows the one guard line in `start_go`; the
  contract's FN-f text (§3.1) says so.
- **HR-31's flash is white** (the lethal kick's impact; the decision allowed black or white): `seq.SEAM_CUT` is one tuple.
- **5b**: A3 h4 stays 2.0 b ahead (17.2).
- Open as before: S5's numbers (F1 6 / 7, f3 r3, HR-18 / 20 / 21 / 36 / 37 / 39 tool part / 40), f3 r6 (the buff wording), S2d's residuals (§16.9), README 0-9's m0diff budget question.
