# 홍련 (Scarlet, special boss) — D0 contract (frozen)

Branch `wip/hr-d0`, head **5d2c3ac** = the D0 commit `52b86b9` (parent `35b82e5`, the 11-03 handover head of
`claude/exciting-pascal-ek1vuy`) + the D0 fixes commit `5d2c3ac` (FN-f names, ownership hand-overs; §7). Every stage
that starts from D0 branches from **5d2c3ac**.
Design: `HR/PLAN.md` (§ numbers below refer to it; §9.0 is the D0 scope, §9.1-9.7 the stages). Source of truth for every
number / name: **`tools/mboss_scarlet/api.py`** (import it; never copy values). This file is the prose around it. Changes
only through a request file `HR/requests/<stage>.md` (what, why, who is affected); the lead applies requests at
integration (I1) and logs them in §7.
`S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`, `HR` = `S:hr`, `R:` = `<worktree>/roguelike`,
`F:` = `R:data/rlk/function`, `T:` = `R:tools`, `RP:` = a resource-pack copy's `assets/rlk/...`.
User decisions at D0: none beyond the plan; the eight questions of PLAN §0.1 are open and the build proceeds with their
defaults (each one switch in `api.py`: `EVENT['buff_scope']` `'run'`, registry `picks 1`, `EVENT['item_pm']` 500, registry
`w` 10 / `minCh` 1, `P2_KIT` `'footage'`, `PIP_RULE` / `ULT60_LETHAL` false / `ULT5_LETHAL` true / `WARN_TEXT`,
`INTRO_SKIP` true / `END_PROFILE` `'std'`). **Question 8, the Minecraft EULA consent: given by the user on 2026-11-05 and
recorded in README 0-2 2 ② / 0-8 (commit 0d65e87).** Stages launched before that (S1, S2a, S3, S4, SR, S2b, S1K) were told
not to start the local test server and report "loadcheck pending"; the lead runs `tools/dev/loadcheck.sh` on each stage
branch as it reports, and at I1 / V / the release (§5 gate 1).

## 0. What D0 committed
| file | content |
|---|---|
| `T:mboss_registry.json` | entry `scarlet` (n 21, `kind:"special"`, `fn:"boss/scarlet"`, **`enabled:false`**, `w` 10, `minCh` 1 `maxCh` 99, 홍련 / 월하곡 / `#E8466A`, `el` 3, `hp` 250 `xp` 0 `atk` 12 `lvAdd` 1 `dmgMul` 135 `goldMul` 6 `sap` 1 `picks` 1 `lvup` 1, `scale` 1.35, `hit {w:1.2,h:2.9}`, `intro` 650, `death` 1164, `deathSnd` false, arena / theme `hr_field`, `res {"*":10}`, `phases [100]`, music 1 / 3 `music.overworld.cherry_grove` **len 0** (S1 measures the pool), music 2 `music.nether.crimson_forest` 6076, icon vanilla `minecraft:iron_sword` until I1) + **`arenas.hr_field` = `api.ARENA_SPEC`** (n 5, centre 880 201 8, r 28 / walk 25 / safe 23, start 880.5 201 31.5 facing north, box 832..928 × 190..250 × −40..56 = 49 chunks, looks `moon` `crimson` `dark`, oob 198..236) + two `_doc` lines. `winWord` / `rwHook` / `poof` are **not** in the entry yet: S1 adds them together with their validation (PLAN §8) |
| `T:mboss_lib.py` | **unchanged** (a disabled special may already name an arena, `load_registry`) |
| `T:mboss_scarlet/__init__.py` | package doc + ownership |
| `T:mboss_scarlet/api.py` | the frozen API (sections 1-9 + 9b, see §2-§3); `python3 tools/mboss_scarlet/api.py --write-stub` (lead only) and `--check` (self-checks) |
| `T:mboss_scarlet/stub_rig_manifest.json` | the D0 rig manifest (schema 1, source stub, from `--write-stub`): 29 parts (name, nn, parent, uuid, tag) + the re-parent table + shadow 0x40, 47 clips (id = order, len, loop, events, owner S2a / S2b), look channels, hands, prop states, 8 anchors, 43 calls + the macro call |
| `T:mboss_scarlet/{seq,p_ghost,reward}.py` | empty stubs (`SERVICES = []`, `PATTERNS = []`, `SERVICES = []`) owned by S2b / S4 / S3 from now on |
| generated (declared D0 outputs) | `F:mboss/ar/hr_field/**` (17 files, core), `F:mboss/arena/hr_field/**` (6 **stub** functions — `ensure` stamps `hr_field@0:stub`, `build` / `clear` / `done` / `rebuild` / `sweep` no-ops — until S1K's theme exists, `build_mboss_arena.py`), and the 26 lines `#mbAr 5` / `hr_field` adds to 22 dispatchers (21 core: `mboss/ar/{box_absorb,clamp,clamp_step,clampw,clampw_step,ensure,fl_off,fl_on,full_rim,leash,loaded,marker,ok,oob,sweep,test,tp_in}`, `mboss/cb/remove`, `mboss/cleanup`, `mboss/fight_vars` (`#mbArW10 250`, `#mbArS10 230`), `mboss/uninstall`; 1 arena generator: `mboss/arena/clear_all`). Once S1K's theme exists the unchanged arena generator also adds the `hr_field` lines of `mboss/arena/job_tick` (1) and `mboss/arena/abort` (2): S1K's outputs (§1) |
Checked at D0 (all in the worktree `HR/wt_d0`):
- every registry-reading Python generator — `regen_all.sh` (core, arena, cboss rooms, proto, cproto, spproto, guardian,
  butterfly, fieldgen, az / ap / tk / kn kits `--skip-rp`, azhdaha, apep, rift, tachy, arlecchino) + the bf / fg kits
  `--skip-rp` — regenerates **byte-identical** outputs apart from the declared D0 outputs above (`git diff` of the
  generated files: 26 added lines, all naming `hr_field` / `#mbAr 5`, none removed); a second and a third run change
  nothing. The JS rigs read only their own registry entries (unchanged); the ch2 / ch3 mob generators do not read it.
- `check_mboss_pack.py` → `4 enabled mid-boss module(s), 4 chapter boss module(s), 2 special boss module(s), 7 arena(s),
  0 problem(s).`
- the four checkers vs the 35b82e5 tree (`HR/tools/checkers.sh`): `check_nbtpath` 0 invalid; `mb/lint_mc` (every function
  folder) 193 339 = 193 339, 0 new; `check_refs` 66 → 67 missing refs and `check_macro` 3356 → 3360: the +1 / +4 are the
  arena template's known false positives (`full_rim`'s macro-built `rlk:mboss/hz/p/c/$(kp)` path and the `with storage`
  macro calls of `tp_in`), now also in the new `mboss/ar/hr_field/{full_rim,tp_in}` — exactly the lines every arena
  (`fl_ruins`, `tk_lift`, …) already has. No new kind of finding.
- `python3 tools/mboss_scarlet/api.py --check`: the import-time self-checks (every clip event tick < its length; every
  HITS clip / event exists; every script cut: lock = strike − 7, made ≥ 12 t before, strikes on exactly one move contact;
  9 counting cuts per gauntlet; judge = `g_dive` + its hit; every LINES id placed in LINE_AT and every LINE_AT id a line;
  clip `l<id>` events = LINE_AT ticks; the §9.0-9.1 files each owned exactly once; output prefixes disjoint; kit sprites
  = 237 568 px ≤ 260 000; 104 sound recipes) + `check_manifest` on the stub (and on the manifest in use) + every sound id
  in `tools/dev/sim/rd/tests/sound_ids.txt`. The lines 1-25 were extracted from PLAN §3.0 by a script (not retyped) and
  each was found verbatim in `HR/wiki/w1.txt` / `w2.txt` or the footage notes; the 47 clips and both gauntlet scripts were
  compared with PLAN §2.5 / §4.5 by parsers (equal).
- **loadcheck: pending the user's EULA consent** (not run; PLAN §0.1 question 8, README 0-2 2 ②, 0-8).

## 1. Ownership (write / delete only your own; tests and scratch under `HR/<stage>/`, `HR/tests/`)
Machine form: `api.OWN_FILES` (patterns, with exclusions) + `api.FILES_9_1` (every file / tree §9.0-9.1 names, each owned
exactly once — asserted at import), `api.HANDOVER` / `api.STAGE_BASE` (below) and `api.OWN` / `api.OWN_GEN` (output
prefixes under `F:boss/scarlet/`). Every stage also owns its scratch folder `HR/<stage>/**` (readme fragments included),
its renders `HR/renders/<prefix>_*` (`s1k_` `s2_` `s2b_` `s3_` `s4_` `sr_`), its RP copy `HR/rp_<stage>/**` and its request
file `HR/requests/<stage>.md`.
**Hand-overs** (`api.HANDOVER`; PLAN §9.1 / §9.3 make these paths sequential, never shared at the same time): the creator
owns the path until its report, the taker — which branches from the creator's head (`api.STAGE_BASE`) — from its own
start. `HR/tests/lib/**`: S1 creates it (the `R:tools/dev/sim/az/tests_cm/lib` sims unchanged + md5s in `README.md` + the
generic `hrsim.py`), S3 takes it over and extends `hrsim.py`; every other stage only reads it and keeps its own helpers in
`HR/<stage>/`. `HR/tests/test_rig.py`, `T:scarlet_rig_manifest.json`, `F:boss/scarlet/rig/**` and the RP `mboss/scarlet`
files: S2a creates them, S2b takes them over (adds the cinematic checks; commits what S2a's unchanged generator
regenerates from `scarlet_cine.mjs`, never S2a's sources).
| stage | base | repository files | generated outputs |
|---|---|---|---|
| **lead** (D0 / I1 / V) | — | `T:mboss_scarlet/{__init__,api}.py`, `stub_rig_manifest.json`, this file, `HR/stage_briefs.md`, `HR/requests/` (applies them), README / RP README edits (I1, V), `tools/dev/regen_all.sh` lines (I1) | registry `enabled` true + the gate icon model (I1) |
| **S1** framework | `wip/hr-d0` | `T:build_mboss_core.py`, `T:mboss_lib.py`, `T:mboss_registry.json` (the §7 fields `winWord` / `rwHook` / `poof` = `api.FN_FIELDS` and the measured music length only), `T:check_mboss_pack.py`; `HR/tests/test_special_hr.py`, `HR/tests/lib/**` (creates it; S3 takes it over); `HR/s1/**` | everything the core writes: `F:mboss/**` except `F:mboss/arena/**` and the module trees, `F:boss/test/**` (incl. the new FN-f `F:mboss/bars_off` / `bars_on`) |
| **S1K** kit + arena | `wip/hr-d0` | new `T:build_mboss_hr_fx.py` (`--skip-rp`), `T:mboss_hr_fx_paint.py`, `T:mboss_hr_fx_manifest.json` (generated), new `T:mboss_arena_hr_field.py`; `HR/tests/test_kit.py`, `test_arena_hr.py`; `HR/s1k/**`, `HR/renders/s1k_*`, `HR/rp_s1k` | `F:boss/scarlet/fx/**` (incl. §7's `ev_*`), RP `textures` / `models/item` / `items` `mboss/hr_kit/**` + atlas entries, font `rlk:mboss_hr` (`font/mboss_hr.json` + `textures/font/mboss_hr/**`), `F:mboss/arena/hr_field/**` and the `hr_field` lines of `F:mboss/arena/{job_tick,abort}` (both through the unchanged `build_mboss_arena.py`) |
| **S2a** rig | `wip/hr-d0` | new `T:build_scarlet_rig.mjs`, `T:scarlet_{pose,geometry,paint,clips}.mjs`, `T:scarlet_rig_manifest.json` (generated), `T:scarlet_rig_api.md`; `HR/tests/test_rig.py` (S2b takes it over); `HR/s2a/**`, `HR/renders/s2_*`, `HR/rp_s2a` | `F:boss/scarlet/rig/**`, RP `textures` / `models/item` / `items` `mboss/scarlet/**` (rig models, the ghost model `rlk:mboss/scarlet/ghost`, the item / thrown-sword model `rlk:mboss/scarlet/item_sword`, F-I: its slot icon `rlk:mboss/scarlet/item_sword_icon` and the item definition's `display_context` select); the 39 clips owned `S2a` in `api.CLIP_OWNER` |
| **S2b** sequences | `wip/hr-s2a` | new `T:scarlet_cine.mjs` (the 8 clips owned `S2b`: `intro` `intro_end` `cs1` `sq1` `repel` `lead_down` `lead_stand` `ending`; S2a's generator imports it), `T:mboss_scarlet/seq.py`; `HR/tests/ev_dry.py` (+ `test_rig.py`, taken over from S2a); `HR/s2b/**`, `HR/renders/s2b_*`, `HR/rp_s2b` | `F:boss/scarlet/seq/**` (written by S3's generator from `seq.py`); taken over from S2a: the rig outputs / manifest / RP files S2a's unchanged generator rebuilds from `scarlet_cine.mjs` |
| **S3** core + AI + P1 + shield + event logic | `wip/hr-s1` | new `T:build_mboss_scarlet.py`, `T:mboss_scarlet/{core,ai,shield,p1,s3lib,reward}.py`; `HR/tests/test_scarlet.py`, `pat_p1.py`, `test_reward.py`, `HR/tests/lib/**` (taken over from S1); `HR/s3/**`, `HR/renders/s3_*` | `F:boss/scarlet/**` except `rig/`, `fx/`, `seq/`, `g/`, `p/{a8,a13,r1,r2,r3}/` = the prefixes `api.OWN['S3']`: the 17 hooks + `test/help`, `init`, `reward` (FN-b hook), `core/ ai/ shield/ ult/ hud/ ev/ test/ rig_stub/`, `p/<key>/` for `api.P1`; and it writes S4's / S2b's outputs through their Writers |
| **S4** ghost patterns | `wip/hr-s3` | `T:mboss_scarlet/p_ghost.py`; `HR/tests/pat_ghost.py`; `HR/s4/**`, `HR/renders/s4_*` | `F:boss/scarlet/p/{r1,r2,r3,a8,a13}/**` and `F:boss/scarlet/g/**` (`g/cut/**`, `g/disc/**`, reappear helpers) = `api.OWN['S4']` (written by S3's generator) |
| **SR** reward item + buff | `wip/hr-d0` | the hand-maintained files of PLAN §7.4.6 / §7.5.2: lines in `F:items/**` (`register`, `build_rarbuckets`, `tune/b10`, `hook/{on_hit,stat_buffs,tick_player,on_cast_burst}`, optional `enh_add`), new `F:items/mythic/sword_hwamu/**`, `F:items/proc/hw_*`, `F:player/{take_damage,dash_iframe,reset_one,update_item,update_item_macro}`, new `F:player/hr_moon/apply`, `F:codex/labels`, new `F:snd/f422`-`f429` (keys `#k352`-`#k359`), `F:load`, `F:uninstall`, `R:items.md`; `HR/tests/test_hwamu.py`, `test_moon.py`; `HR/sr/**`, `HR/renders/sr_*` | (hand files only; no generator). F3 (C4): + `F:items/hook/on_dash` (the `hw_dash` line, HR-09) and the pack-wide lines of `F:view/{tick,ride_tick,sel_xhair}` (HR-08) and `F:lvup/tick` (HR-34) — `ident_hr.py`'s allow-list group "F3 review fixes (pack-wide lines)" |
Shared-file edits outside this table are forbidden; if one is needed, write a request. Read-only for everyone: the player
avatar files (`T:build_player_rig.mjs`, `T:player_motion/**`, `F:char/**`; `F:player/**` except SR's listed files), every
other boss's sources and outputs, `T:build_mboss_arena.py`, `tools/dev/**` (the lead adds the `regen_all.sh` lines at I1).
Shared README / RP README text: stages write fragments `HR/<stage>/readme_*.md` (and `rp_readme_*.md`); only the lead
edits `R:README.md` and the RP README (I1 / V).

## 2. Names (api §1, §5, §6, §9b)
- **Module**: id `scarlet`, n 21, root `F:boss/scarlet/` (`api.NS` = `rlk:boss/scarlet/`), name / sub / colour 홍련 / 월하곡 /
  `#E8466A` (`api.TITLE`, shown by `mboss_lib.title(*api.TITLE)` at `intro_end` `draw`). Arena `hr_field`, `#mbAr 5`.
- **Scores**: objective **`hr`** (dummy; S3's `init` creates, `uninstall` removes). Fake players: core `api.CORE_FP` (`#ph
  #pat #pt #done #clk #rigc #rigt #sq #sqdone #hud #fl #tst #lock #last #last2 #rear #far #dec #rec #hits #a6cd #pips #gres
  #gk #down #skip #warn #inv #hrLook`); a pattern `#<key>_<x>`; the ghost helpers `#g_<x>`; sequences `#sq_<x>` (incl. the
  signal `#sq_sig`); the event `#hrEv #hrEvDone #hrEvDrop` (`api.EV_FP`). Rig objectives `hrRig*` (S2a), kit `hrFx*`
  (S1K), the buff `hrMoon` (SR, per player; `#hrMoonAtk / #hrMoonCrit / #hrMoonSpd / #hrMoonRun tmp`). The module cleanup
  resets every fake player of objective hr (`reset * hr`) but the event scores, which it saves to `#hrEvK #hrEvDoneK
  #hrEvDropK tmp` and restores (F3, HR-05).
- **I1 (request s3-5)**: S3's own fake players are folded into `api.CORE_FP` (same order; `s3lib.FP` = `api.CORE_FP`):
  the temporaries `#t #t2 #t3 #t4 #t5 #cn1 #cn1000`, the constants `#c<n>` (`api.CORE_CONSTS` 2 3 5 10 64 100 577 1000 36000),
  `#fl60 #fl5 #flw #sqn #sqh #shb #kip #grs #rvw #a6q #ctr #flq #h1-#h4 #pipoff #lk #skp #rp`, the AI's `#ai_*` and its
  per-pattern `#ai_w<key>` / `#cd_<key>` (F1: `#ai_nn` an empty pick in a row, `#ai_bs` the backstep's mid pick pending,
  `#ai_tmc` the module clock of a kept tail's last move tick; all in `api.CORE_FP`; `#grs` takes 4 = the judged A8 fail → P2,
  5 = a lethal fail pending); and S3's extra tags + the rig's shadow into `api.TAGS` (`shadow` `rlk_hr_shadow`,
  `pip` `rlk_hr_pip`, `lock` `rlk_hr_lock`, `probe` `rlk_hr_dp`, `a9s`, `pl8`, `near`, `deco_moon_halo` / `deco_lotus` /
  `deco_seat_rock`); every generated output stayed byte-identical. Stage-private tags not in `api.TAGS` (each dies with its
  stage's cancel or with a contract tag it also carries): S4 `rlk_hr_disc`, `rlk_hr_cnt`, `rlk_hr_gsp`, `rlk_hr_gdn`, `rlk_hr_gln` (F1: a new disc lock
  marker, transient; the lock marker itself carries `rlk_hr_lock` + `rlk_hr_p` + `rlk_hr_p_<r2|a13>`); S2b
  `rlk_hr_sqp`, `rlk_hr_sqh`, `rlk_hr_ev_sword`, `rlk_hr_ev_orb`; S3's transient `rlk_hr_dnew`, `rlk_hr_pipnew`.
- **Tags** (`api.TAGS`): `rlk_hr_part` (+ `rlk_hr_<part>`, shadow `rlk_hr_shadow`), `rlk_hr_anchor`, `rlk_hr_fx`,
  `rlk_hr_deco` (decor props), `rlk_hr_p` + `rlk_hr_p_<key>` (pattern markers), `rlk_hr_cut` (cut markers),
  `rlk_hr_ghost` (the body in ghost form), `rlk_hr_down`, `rlk_hr_stage` (a sequence's staging marker), `rlk_hr_ev` (event
  entities). Everything spawned in the world also carries `rlk_room rlk_mb_aux`.
- **Storage** `rlk:hr`: `core.*` (S3), `rig.*` (S2a), `seq.*` (S2b), `fx.*` (S1K), `g.*` (S4), `ev.*` (S3; `ev.force` =
  `"item"` / `"buff"`, `ev.sx` = the item's stars for the coda title / chat record, removed by `ev/reset`); the module
  cleanup removes `core.*` and `seq.*` (F3, HR-33 / HR-05).
- **UUIDs**: rig parts `524c4b4d-4852-4400-8000-0000000000NN` (NN hex 00-1c = `api.PARTS` order), shadow `…40`.
- **Resource ids** (lowercase only): `rlk:mboss/scarlet/*` (S2a: rig, `ghost`, `item_sword`; F-I:
  `item_sword_icon`), `rlk:mboss/hr_kit/*` (S1K:
  kit, `gate_icon`), font `rlk:mboss_hr` (U+EC00-ECFF; overlays U+EC10-EC15 `black negative pinkwhite red_tint magenta
  white`, `vig` U+EC16), bossbar `rlk:hr_warn`. Item `sword_hwamu` (「화무십일홍」, score `it_sword_hwamu`, model
  `rlk:mboss/scarlet/item_sword`), buff 「월하대작」.
- **Test ids** (`boss/test/pattern {id:N}`, `api.TEST_IDS`; `test/help` prints `api.TEST_HELP_NAMES`): 1 A1 · 2 A2 · 3 A3 ·
  4 A4 + A5 · 5 A6 · 6 A9 · 7 A10 · 11 R1 · 12 R2 · 13 R3 · 20 CS1 → SQ1 → A8 · 21 A8 now (5/5) · 22 A8 with 0 pips · 23 A8
  fail · 24 CS2 only · 25 down window · 26 `lead_stand {g:a13}` + A13 · 27 A13 now · 28 A13 with 0 pips (→ CS3 → kill →
  CS4 → the coda) · 29 A13 fail (instant death; in a test → `mboss/test/defeat`) · 30 intro replay (P1 / P2 only) · 31 look
  `dark` on / off ·
  32 look `crimson` · 33 P2 now · 34 HP = 5 % floor + 1 · 35 intro skip at tick 100 (P1 / P2 only) · 80 HP = next floor + 1 · 90 next
  event random · 91 next event 화무십일홍 · 92 next event 월하대작 · 99 hold. `test/lock {id}` for `api.LOCK_IDS` (1-7, 11-13).
- **Lines**: `api.LINES` 1-25 (verbatim, PLAN §3.0), placed by `api.LINE_AT` (where, tick, ticks on screen); colour
  `#F2D0E8`; shown only through the kit `fx/hud/line {id}`. 24 / 25 only in the event coda (`EVENT['lines']`). F2 (HR-16):
  `api.LINE_MAX_PX` 192, `api.LINE_PAGES` {5, 22, 24: two pages each} — a line wider than 192 font px is typed as its pages
  in order inside the same hold; the pages joined with one space == `api.LINES[id]` (`_check_contract` asserts it).
- **On-screen text** (rule 10-21): the name and sub, the 25 lines, the warning banner `api.WARN_TEXT` (A13 only by
  default), the intro's skip prompt `api.SKIP_TEXT` + `api.SKIP_HINT`, 「도전 성공」 (`api.WIN_WORD`), §7's item / buff names,
  numbers and notices (`api.EV_TEXT`), system notices. No pattern names, no tips.

## 3. Interfaces
### 3.1 Framework ↔ module (S1 → S3 / §7)
- Special path as 타키 (rift → `sp/*`, chapter mode `#mbMode 1`, `#mbKind 2`; 17 hooks + `test/help`, no `prep`), dispatched
  by `#mbId 21` once I1 enables her. Body: husk `scale 1.0`, click shield `hit {w:1.2,h:2.4}` (S2d), no proxies. Floors via
  `#mbFloor` (`api.FLOOR_P1` 600 ‰ in P1, `api.FLOOR_ULT` 50 ‰ from CS1 0), invulnerability `rlk_mb_inv`, `cine`,
  `true_hit` / `true_pct`, `pl_dot`, `push_ring`, `mv/*`, music through `api.music(ph)` (= `mboss_lib.music`).
- **FN-a** `winWord` (special only, ≤ 12 chars): her record gets `winWord:"도전 성공"`; `sp/reward` line 8 split into the
  guarded 처치 line (today's text) + the `winWord` line; `test/swon` + new `test/swon_msg_w` (PLAN §7.1.3 verbatim).
- **FN-b** `rwHook`: `mboss_lib.SPECIAL_OPT_HOOKS = {'rwHook': 'reward'}`; for an **enabled** entry with the flag, one
  literal line `api.RW_HOOK_LINE` (`execute if data storage rlk:mboss cur{id:"scarlet"} as @a[tag=player,limit=1] run
  function rlk:boss/scarlet/reward`) after `sp/lvup` and before `#spPk` (+ the comment line); `check_mboss_pack` asserts it.
  Hook contract: `boss/scarlet/reward`, not a macro, @s = the player, not positioned, once per kill (PLAN §7.1.4).
- **FN-c** `poof:false` → record `poof:0b` → `death_finish` skips its poof particle for that entry.
- **FN-e** the cherry-grove pool measured into `mboss_lib.MUSIC_TRACKS`; music 1 `len` = `music_len`, music 3 stays 0.
- **FN-f** `#mbBarOff mb` (zeroed by `fight_vars` / `cleanup_fight`; `mboss/world` skips `mboss/bars` while it is 1);
  `mboss_lib.bars(on)` returns **one line**: `api.BARS_FNS[on]` = `function rlk:mboss/bars_off` / `function
  rlk:mboss/bars_on`, two **new** core functions: `bars_off` = `scoreboard players set #mbBarOff mb 1` + `function
  rlk:mboss/bars_hide`, `bars_on` = `scoreboard players set #mbBarOff mb 0` + `function rlk:mboss/bars_show`. The existing
  `mboss/bars_hide` / `bars_show` (called by `death_start`, `pause_tick`, `cleanup_fight`, `init`, `main`, `tick`,
  `start_go`, `mboss/bars`) stay **byte-identical**: if they set the flag, a death pause would leave every boss's bars hidden
  for the rest of its fight (`mboss/bars`, the only re-show, is skipped while the flag is 1). The module only uses
  `api.bars(on)` (`''` until S1 lands) and never the framework-private `#mbBar`.
- F2 (HR-29, V2R-02) / F-I (f2-8): the spawn hook → `bars(0)` (again at `core/intro/begin`), `core/intro/done` → `bars(1)`;
  `mboss/start_go` shows the bars only `unless score #mbBarOff mb matches 1` (its closing `bars_show`; for every other boss
  `fight_vars` has just zeroed the flag, so nothing changes there; `check_mboss_pack` FN-f pins that one line); the
  module's `bars` hook first runs `mboss/bars_ramp` while `#mbSt 1` and `#mbT ..29` (the HP bar fills at control).
  Sequences `intro` / `cs1` / `ending` / `event` set `hudHold 2` on the player at start and every tick and blank the
  actionbar at start; `fx/hud/skip {s:5}` no longer zeroes `hudHold` (it runs out by itself).
- 타키 / spproto module outputs and records stay byte-identical; every other boss unchanged.

### 3.2 Rig (S2a / S2b → S3 / S4 / S2b)
- Calls `api.RIG_CALLS`: `rig/{init,spawn,spawn_hidden,tick,kill,uninstall,flash,state/normal,state/hidden,face/player,
  face/track}`, macro `rig/face/set {yaw}`, `rig/look/form/{normal,ghost}`, `look/phase/{p1,p2}`,
  `look/hat/{worn,back,hand,world,gone}`, `look/sword/{hand,sheathed,gone}`, `look/blade/{off,lilac,pink,violet,gold}`,
  `look/scabbard/{hand,hip,gone}`, `look/face/{calm,smile,closed}`, `look/props/none`, `rig/anchor/{hand_l,hand_r,
  blade_tip,blade_mid,scabbard_mouth,hat_crown,head,chest}` (moves the one `rlk_hr_anchor` marker), `rig/play/<clip>` /
  `rig/start/<clip>` for every `api.CLIPS` key (47) — through `api.rig()` / `api.play()` / `api.start()` only.
  Semantics (Raiden / Apep / 타키): `play` = tick 0 at the next `rig/tick`, event *e* on the *e*-th `rig/tick`, play
  replaces the running clip; the rig never moves the anchor except `face/*`, never reads module scores, never goes below
  the floor; `state/hidden` scales parts to 0 in place. The module calls only `form`, `phase`, `blade` and `state`; clips
  key hat / sword / scabbard / face / hands / props at their own events.
- `api.CLIPS` = PLAN §2.5 with every event tick < len; a clip's end is its length (`api.ev(clip, 'end')`), not an event.
  Two event names the table repeats are numbered: `walk` / `strafe_*` `step1` `step2`, `ending` `rise2` (268).
- Manifest `T:scarlet_rig_manifest.json` = the stub's schema + transforms / models / budgets / sprites; `api.check_manifest`
  must pass. Until it exists `api.rig()` points at S3's `rig_stub/**` (every call name; `play/<clip>` and `start/<clip>`
  set `#rigc hr` to the clip id).

### 3.3 Kit (S1K → S2b / S3 / S4 / SR)
- Only through `api.K` (`p`, `prop`, `hud` / `ovl`, `snd`, `fixed`) with the names and macro args of `api.KIT_PRESETS`
  (50 incl. §7's 8 `ev_*`), `api.KIT_PROPS` (`disc`, `petal_big {look}`, `moon_halo {look}`, `lotus {look}`,
  `seat_rock {look}`; `look` a quoted name; V2, HR-52: the seat stone's bottle / cup leave with `look:"bare"` at once and
  with a killed stone within 10 t (`fx/e/stay_t`, not the per-tick prop chain), so the module re-looks the stone `bare`
  before it kills it), `api.KIT_SOUNDS` (104 recipes, `api.KIT_SOUND_RECIPES` = the plan's vanilla
  events / volumes / pitches), `api.KIT_HUD` (`line {id}`, `ovl {g,in,hold,out}`, `warn {on}`, `skip {s}`, `clear`),
  `api.KIT_FIXED`; values in tenths of a block / degrees / ticks; `c` 1 lilac, 2 pink-magenta, 3 yellow, 4 crimson, 5 white.
  `K` returns `''` while `T:mboss_hr_fx_manifest.json` is missing → wrap with `api.lines(...)`.
- Caps: fx cards 96, ambient 48 (the ager kills the oldest); `afterimage` ≤ 4 alive, fading over 6 t. Sprites =
  `api.KIT_SPRITES` (237 568 px, the kit generator asserts ≤ 0.26 M); overlays and `vig` are font glyphs (not in the items
  atlas). Glyph roots empty and unstyled, every component names its font, the font ends with `minecraft:default`.
- Kit wiring by S3: `cleanup` → `fx/clear` + `fx/hud/clear`; `pause` / `death_start` → `fx/clear` (CS4 then starts its own
  effects; kept cards stay); `uninstall` → `fx/uninstall` (cards, objectives, the warn bossbar).
- `scarlet_line`'s `roll` > 0 rises toward the player's right (+13° in CS1 C8 and in the instant deaths); its low end stays
  ≥ 0.25 b over the floor at any call height (the card slides along its own length, `fx/e/clamp_sline`; it still crosses
  the executor point) (F2, HR-44).
- F2 (HR-41 / HR-42): every preset is level: the executor's pitch is ignored (cards and `^` lines run `rotated ~ 0`);
  `qi_arc`'s `pitch` is its absolute elevation (the floor clamp counts only it); only `qi_line` follows the executor's pitch
  (the A8.9 dive), clamped at every pitch with the sine table (its end 0.32 b over the floor).
- F2 (HR-12): planes across the aim: `qi_vert` (yaw 0 = the plane perpendicular to the executor's facing, bulging to its
  right; 180 to its left), `qi_fan` (bulging to its left), `qi_line` (the facing turned 90° right, pitch kept) — a caller
  that wants the line along an aim turns first: `… facing entity <x> feet rotated ~-90 ~ run …/qi_line` (A10's dive line,
  F-I f2-7); `qi_arc` / `qi_wedge` with |roll| 20..160 use the face kinds `qi_arcf_0..3` / `qi_wedgef` (same sprites) and
  are rolled in the screen plane; their particle bursts sit on the shape in both modes (the crescent's rim at 0.8 of its
  reach, the wedge's point: flat along the aim, face up the rolled screen-plane axis; `fx/e/rollv`); |roll| < 20 or > 160
  stay flat.
- F2 (HR-32): `qi_band {len,yaw,pitch,roll,sw}`: sw = the forward sweep in tenths (its leading streak × 1.04).
- F2 (HR-17 / HR-23): `api.KIT_FIXED` + `keep_on` / `keep_off` (cards made between carry `api.KIT_KEEP_TAG` =
  `rlk_hr_fx_keep`: `fx/clear` and the ager's dead / revive clears skip them; the module's cleanup and `fx/uninstall` remove
  them) and `follow_on` / `follow_off` (@s = the lead: cards made between follow its x / z each ager tick at their own
  height over it; objective `hrFxY`). `fx/clear` also ends an open keep / follow.
- F2 (HR-30): while a line is up, `fx/hud/ovl` fades are opacity-step glyphs U+EC20..U+EC37 (four per overlay, font
  `rlk:mboss_hr`), re-sent each tick at full title alpha; the kit's init storage is `fx{init:2b}` (an older world re-runs
  `e/init`).
- F2 (HR-45): first-person anchors (no avatar: `@a[tag=rlk_body]` is the player): the module's player-anchored calls branch
  on it — the 홍련일섬 line at the eye + 1.2 b, the deflect's `clash_gold` 1.8 b out on the view ray, the `light_column`
  1.8 b ahead (level), A8.5's X 1.2 b ahead of the cut spot.

### 3.4 Arena (S1K → all)
- `api.arena_look('moon'|'crimson'|'dark')` = a **request** line (`#hrLook hr` = `api.LOOK_ID`); the core turns a pending
  request into `api.look_job(look)` (= `function rlk:mboss/arena/hr_field/look/<look>`) at the first tick with
  `#mbArBuild 0`; both return `''` until S1K's `T:mboss_arena_hr_field.py` exists. The framework's `ensure` restores
  `moon` at the next fight. V2 (HR-51): `core/look/go` starts no job when storage `rlk:mboss built_hr_field` already reads
  `"hr_field@<ver>:<look>"` (the decor re-look and the served request stay; a job drops the stamp when it starts, so a job
  cut by a reload runs again).
- The theme implements `look_lines(look)` with **absolute spans** (every cell any look changes, block-exact from any
  source look), 4 real slices per job; `dark`'s real slices land 3 t apart (`api.DARK_SLICES` −17 / −14 / −11 / −8 of T0,
  the job called at −18) through two empty padding slices after each real one. `api.DARK_LIGHT` false = fallback B.
- Decor points: `api.deco()` = the theme's `DECO` dict when it defines one (same shape), else `api.DECO_DEFAULT` (moon halo
  1 b in front of the moon `api.MOON_POS` (889, 218, −34), 8 lotus points on the pond, the seat `api.SEAT_POS`).
  `api.MOON_BEARING` 12°, elevation 22°; "north" = −z.

### 3.5 Patterns and sequences (S3 core ↔ S3 p1 / S4 / S2b)
- `api.Pattern` / `api.Service` (docstrings = the runtime contract); writers `api.Writer(owner, api.OWN[owner])`. The core
  includes only patterns present in `p1.PATTERNS + p_ghost.PATTERNS` and sequences in `seq.SERVICES` / `reward.SERVICES`;
  missing ones fall back to a stand-in (pattern skipped; sequence = wait the clip length, titles / music at its events,
  `seq/intro/skip` included).
- Hit ticks from `api.ev`, shapes / tiers / kb from `api.HITS` (shape vocabulary in its comment; `pdisc` = at the player's
  spot), tiers `api.DMG` (T1 29, T2 42, T3 56, T4 71 %, TC 37 = the counting cuts of A8 / A13: F1, HR-19), Electro 1U, every hazard `#hzQuiet 1`, **no floor decal**. Tells
  ≥ `api.TELL_MIN` 12 t (≥ `TELL_BIG` 20 for big / undodgeable / yellow), chain hits ≥ `COMBO_GAP` 10 t apart, aims lock
  `LOCK_LEAD` 7 t before the hit; end points via `mv/ok` + leash inside `api.MOVE_R` 22.5 with the fallback on the
  player → C line ≤ 21 b (`FALLBACK_R`).
- Scripted patterns: `api.SCRIPTS` (`a8`, `a13`, `r1`, `r2`, `r3`) rows `(t, step, clip, cut)` — the clip's start on the
  pattern clock (T0 = 0), the cut `(made, lock, strike, tier, kb)`; rows with t < 0 are SQ1's / the lead-ins'. Cuts only
  through `api.cut(made, lock, strike, tier, kb, count)` → `g/cut/make {s,t,dmg,kb,n}` / `g/cut/aim {s}` /
  `g/cut/lock {s}` (S4 implements; the lock calls `shield/cut {s}` when n = 1). Discs only through `api.disc(kb)` →
  `g/disc/throw {kb}` (one `pj/launch` per `api.DISC` + one kit card), aimed at the lock marker `g/disc/lock` placed 7 t
  before each release (`api.DISC_LOCK`; a throw without one locks at once; F1, HR-15). `api.BOLTS`, `api.REAPPEAR` (F1: D2
  +55 / D4 −55, HR-27), `api.JUDGE_T` (194 / 258), `api.REPEL_T` (206 / 270).
- F1 (HR-14 / HR-18): P1-kit pattern ends `api.PAT_END` (8-12 t after the last hit; A6 keeps `A6_TRIGGER['next']`); the
  AI recovery `api.RECOVER` P1 12-20 / P2 10-16. A pattern's kept tail moves her through `ai/tail` (the recovery's move
  choice and clip: `ai/move_pick` on `core/fp`'s last sample, ≤ 4 t old — no extra `ai/sample`, so the rear / far dwell
  counts stay as they are; the stamp `#ai_tmc`) and `ai/tail_step` (one `ai/step` each later tick; the pattern turns her
  itself): P1-kit tails from `api.TAIL_MOVE` = 4 t after the last hit (A4 its landing), R1 / R3 from the solid row, R2
  from 4 t after its last release. `ai/rec_start` keeps a tail's move when it stepped on this or the last tick and still
  fits the band (`ai/tail_keep`). A flinch replays the move clip (`ai/play_move`, the far fallback's approach glide
  included).
- Sequences never call core functions: they signal through **`#sq_sig hr`** = `api.SIG` (`hp1` `hp2` `hp3` at `repel`'s
  `api.COUNTER_EV` flash 24 / land 75 / kick 102; `refill` at the lead-ins' `refill` event); the core reads it right after
  `seq/<name>/tick`, applies it and resets it to 0 (HP steps `api.COUNTER_PM` = {60: (15, 15, 15), 5: (15, 15, 'kill')} ‰
  of `mhpM` through `mboss/true_hit`, `'kill'` = `true_pct 100`; refill = `shield/arm`). `repel {at:60|5}`,
  `lead_stand {g:"a8"|"a13"}` (`api.SEQ_ARGS`); the core calls `seq/intro/skip` after `api.SKIP_HOLD` t of sneak
  (`rlk:in_sneak`) inside `api.SKIP_WINDOW`, showing the prompt with `K.hud('skip', s=…)`.
- The core starts every sequence and owns: invulnerability (also `rlk_mb_inv` while the body carries `rlk_hr_ghost`, which
  S4's ghost moves set and clear), `cine`, the phase switch, floors, the bars (`api.bars(0)` at CS1 0, `api.bars(1)` +
  `shield/arm` at SQ1 0), the under bar (`#buSub` = pips, `api.BU_SHIELD`; the down timer, `api.BU_DOWN`), the death finish,
  the look requests outside sequences, decor-prop spawning, pause / reload (PLAN §3.8). A sequence owns its clips, sounds,
  kit effects / props, lines, titles, overlays, push rings, the look requests inside it (`dark` at the SQ1 / lead-in
  `dark` event), the warning banner on at that event when the gauntlet's fail is lethal (`ULT60_LETHAL` / `ULT5_LETHAL`),
  the body moves (`mboss/mv/*` + `mv/ok`) and the music line of its `music` event (`api.MUSIC_AT`). S4's gauntlet turns the
  banner off and requests `crimson` at the judge; its `cancel` does both too.

### 3.6 Shield (S3 → S4; PLAN §5)
`api.shield(call, **a)` with `api.SHIELD_CALLS`: `shield/arm` (5/5 + the under bar), `shield/cut {s}` (register a counting
cut's strike tick s, store its lock point; the pip check at s and s + 1: `dashInvT` 1..6 at s or 1..5 at s + 1, feet
within `api.PIP_R` 6.2 b of the lock point, one pip per cut, any direction — `api.PIP_RULE` `'timed_dash'`),
`shield/judge` (→ `#gres hr` 1 deflect / 2 fail), `ult/fail60` (`FAIL60_PM` 500 ‰ non-lethal + `push_ring(2.5, 3)`),
`ult/fatal` (@s = the player; skipped while `rnDie ≥ 1`; through i-frames and shields; Ronova's revive applies),
`shield/off`. Counting cuts: the nine of each gauntlet (`api.CUT_IDS`); discs and the dive never count.

### 3.7 Event, reward, item, buff (S3 ↔ S2b ↔ S1 ↔ SR; PLAN §7)
- Roll at `death_start` (`ev/roll`), staging `seq/event` (S2b, 120 t from H = `ending`'s end, `api.EV_T`: line E4-E52,
  leave E34-E40, grant **E56**, black E110), grant / title only through `api.ev_apply()` / `api.ev_title()` (`''` while
  `reward.SERVICES` is empty), the FN-b hook `boss/scarlet/reward` (cut coda, pending drop, chat record), `#hrEv` 0 / 1
  item / 2 buff, `#hrEvDone`, `#hrEvDrop` (kept by `cleanup`: saved around its `reset * hr`, F3), test override `rlk:hr ev.force` (tests 90-92),
  event entities tagged `rlk_hr_ev`; F3: `ev/stars` (rlk:items stars[<the item's star>] → `ev.sx`). `api.EVENT`: `item_pm` 500, `buff_scope` `'run'`, `item_enh` 1, `lines` True,
  `len` 120. Registry `death` 1164 = H 1042 + 120 + 2.
- SR's names: `api.ITEM_ID` `sword_hwamu`, `api.ITEM_MODEL`, `api.BUFF_OBJ` `hrMoon`, `api.BUFF_FP`, `api.BUFF_VALUES`
  (run 20 / 10 / 10, forever 8 / 4 / 4), `api.ITEM_SND` `snd/f422`-`f429` (`#k352`-`#k359`), the `vig` glyph
  (`api.VIG` U+EC16 in `rlk:mboss_hr`), `api.EV_TEXT` (every §7.3.3 / §7.5.2 string verbatim).
  F3 (HR-11 / HR-33 / HR-35): `api.BUFF_SCOPE_WORDS` (run 이번 런 동안 / 이번 런, forever 영구히 / 영구),
  `api.EV_CHAT_BUFF_HEAD`; `api.EV_TEXT` adds `item_name` (the display name), `buff_stats` (the three numbers), `buff_ab`
  (the actionbar number); `item_title` is now `화무십일홍 ★☆☆`, `item_sub` `[ MYTHIC ] 신화 아이템을 얻었습니다`,
  `buff_sub` the first two numbers. The scope is load's `#hrMoonRun` (reset_one, update_item) + `api.EVENT['buff_scope']`
  (the chat words).
  F-I (HR-03): the item `api.ITEM_MODEL`'s definition selects on `display_context`: gui / fixed / ground → the slot icon
  `rlk:mboss/scarlet/item_sword_icon` (the rig generator's, drawn in GUI px: long parts ≥ 2 GUI px wide), the hands and
  `item_display` none (the coda's thrown prop) → the rig model; the manifest's `item_sword.icon` names it.

### 3.8 No cross-stage reference before it exists
A missing function fails the whole server load. `api.rig`, `api.K`, `api.arena_look`, `api.look_job`, `api.bars`,
`api.ev_apply()`, `api.ev_title()` return the right line or `''`; sequences reach the core only through `#sq_sig`; the
core reaches S4 / S2b only through the PATTERNS / SERVICES they ship. S4 calls S3's `shield/*` and `ult/*` directly (S4
branches from S3).

## 4. Standing rules (every stage; README 0-6 + this boss)
- Never hand-edit generated outputs: change the generator, regenerate; generators own their paths, clean their own stale
  files, write deterministically (run twice → identical).
- Real-game traps: no negative literals in `scoreboard players add/remove`; text components never inherit a glyph font
  (empty unstyled root, `font` on every component, the kit font ends with `minecraft:default`); resource ids lowercase
  `[a-z0-9_.-/]`; nothing below the floor; no teleport into blocks (destinations through `mv/ok` / safe-floor checks);
  held props point the right way seen from the side; big swings keyed every tick (≤ 120° per tick); one display card per
  projectile, facing its flight; `summon` does not take the execute rotation (rotate after summoning).
- Telegraphs (10-20): no floor decal anywhere (the footage shows none); quiet tells ≥ 12 t, ≥ 20 t for big / undodgeable /
  yellow; no tips (10-21): on-screen text only as §2. Vanilla sounds only. No element immunity.
- Originality (PLAN §1.5, §2.2, §6.2): the rig and the arena are an original design; names stay neutral (`scarlet` /
  `hr`); never name a part, texture, model, function or file after the original game's costume or level pieces; no
  glyph monoliths, no stairway or pair of masses framing the moon. Lines only verbatim from `api.LINES`.
- **EULA**: the consent is recorded (2026-11-05, README 0-8). Stages launched before it keep their brief's rule (no local
  server; "loadcheck pending" in the report); the lead runs loadcheck per stage branch (one real server at a time, the
  `.lock` in the server folder) and at I1 / V / the release.
- Git: work only in your worktree `HR/wt_<s>` on `wip/hr-<s>`; never push; never touch `/home/user/rlk` other than through
  `git worktree` commands; commit messages end with exactly
  `<세션이 정해 준 trailer>`
  (no model name anywhere else: commits, code, docs).
- Disk (≈ 1.7 GB free at D0): `df -h /` ≥ 800 MB before a worktree, an RP copy or a snapshot; at most two stage worktrees
  at once (≈ 260 MB each); RP copies only for S2a / S2b / S1K (`cp -r S:ar/rp_i1 HR/rp_<s>`, ≈ 48 MB, the 11-03 RP, never
  hard links); delete render intermediates and scratch; renders ≤ 640 px jpg.

## 5. Gates (each stage before hand-off; all at I1 / V — PLAN §9.5, README 0-5)
1. **loadcheck** (`RLK_DEV=$DEV bash tools/dev/loadcheck.sh <wt>/roguelike hr_<s>` → `0 function load failure(s)`, exit 0;
   the consent is recorded since 2026-11-05, README 0-8). Stages launched before the consent report it as pending; the
   lead runs it on their branches.
2. `python3 -I tools/dev/rplint.py <RP>` → 0 problems (S1K, S2a, S2b).
3. Regenerate twice → byte-identical (and the RP hash equal for RP stages): `bash HR/tools/regen_d0.sh <wt>/roguelike`
   (every registry-reading Python generator + the bf / fg kits) then your own generator(s); `git status` shows only your
   files; `python3 tools/check_mboss_pack.py` → 0 problems.
4. Static rules (§4) + `python3 tools/mboss_scarlet/api.py --check` green.
5. Budgets: this boss ≤ 0.43 M items-atlas px (rig ≤ 0.15 M, kit ≤ 0.26 M, gate icon ≤ 0.005 M, §7 0 px) and the stitched
   atlas ≤ 13.2 M (`python3 -I tools/dev/atlas_px.py <RP>`); model elements at rest ≤ 6 500; average commands per fight
   tick ≤ Apep's ≈ 830 (target ≤ 600, look-job spikes ≤ 5 k).
6. The stage's suites green; every other generator's output unchanged except the stage's own files. S1, SR, I1 and V also
   run `tools/dev/sim/az/tests_cm/run_all.sh` (from a copy outside the datapack, `R:tools/dev/sim/README.md` §1) and the
   four checkers (`bash HR/tools/checkers.sh <wt>/roguelike`, baseline = the 35b82e5 results in
   `HR/tools/base_35b82e5/`): no new failure or finding beyond the instances §0 lists.

**The I1 `ident.py` allow-list** (every other boss / mob output must be byte-identical with 35b82e5 except these):
- D0's arena lines (measured, §0): `F:mboss/ar/{box_absorb,clamp,clamp_step,clampw,clampw_step,ensure,fl_off,fl_on,
  full_rim,leash,loaded,marker,ok,oob,sweep,test,tp_in}`, `F:mboss/arena/clear_all`, `F:mboss/cb/remove`,
  `F:mboss/cleanup`, `F:mboss/fight_vars`, `F:mboss/uninstall`; new trees `F:mboss/ar/hr_field/**`,
  `F:mboss/arena/hr_field/**` (stub until S1K, then the theme's slices).
- The FN outputs (S1): `F:mboss/sp/reward`, `F:mboss/test/swon`, `F:mboss/test/swon_msg_w` (new),
  `F:mboss/death_finish`, `F:mboss/register`, `F:mboss/world`, `F:mboss/fight_vars`, `F:mboss/cleanup_fight`, and the
  new `F:mboss/bars_off` / `F:mboss/bars_on` (FN-f; `bars_hide` / `bars_show` unchanged).
- Every `F:mboss/**` file that gains an n 21 line when I1 enables her — **measured at I1a** (11-05, `enabled:true` + the
  core; = S1's measurement, request s1-4): **26 changed** — `d/*` (18: the 17 hooks + `test_help`, incl. the uninstall
  dispatch `d/uninstall`), `register`, `sp/gate`, `sp/prep`, `sp/reward` (the FN-b hook line; also an FN output above),
  `test/help_pattern`, `test/help_rift_id`, `test/help_special`, `test/help_special_ch` — and **3 new**: `cb/inc/scarlet`,
  `sp/g/scarlet`, `sp/pp/scarlet`. (The `ar/*` / `arena/clear_all` dispatchers, `fight_vars` and `mboss/uninstall` gain their
  `hr_field` lines at D0 already, listed above; the D0 verification counted 25 + 3 without `sp/reward`, PLAN §9.5 named only
  `test/help_special`.) S1K's theme (I1b) adds the `hr_field` lines of `arena/job_tick` / `arena/abort`. The new module tree
  `F:boss/scarlet/**`. (Checked by `HR/tests/ident_hr.py`, I1.)
- The SR hand files (§1 SR row).

## 6. Deviations from PLAN §9.0 frozen at D0 (and why)
- `COUNTER_PM` = `{60: (15, 15, 15), 5: (15, 15, 'kill')}`: §9.0's summary writes `(10, 10, 'kill')` for 5 %, but §3.4
  (the HP column of the counter cinematic: −1.5 % at 24 and at 75 for both), §4.6 step 5 ("−1.5 %, −1.5 %, the lethal true
  hit at 102") and §4.8 ("−3 % + the kill") all give 15 / 15; the footage 5.2 → 3.5 → 2.3 % agrees with 15 / 15.
- Clip `end` events: §2.5 lists `end` = the clip length for most clips; `api.CLIPS` keeps every event < len (the clip end
  is its length, `api.ev(clip, 'end')`); `api.CLIPS_PLAN` keeps the table as written (with `end`), asserted equal to len.
- Repeated event names get numbered (a dict key is unique): `walk` / `strafe_l` / `strafe_r` `step` → `step1` / `step2`;
  `ending` `rise` at 268 → `rise2` (`rise` stays at 28).
- The registry entry leaves out `winWord` / `rwHook` / `poof` (PLAN §8's own header: S1 adds them with their validation;
  `api.FN_FIELDS` freezes their values); icon model vanilla until I1 (§8 table).
- Added because the stages need them and §9.0 does not name them: the sequence → core signal `#sq_sig` / `api.SIG` (so
  S2b never calls S3's functions), `api.look_job`, `api.deco()` + `DECO_DEFAULT` (decor points S3 spawns and S1K may
  override), the shield builder `api.shield` + `SHIELD_CALLS`, `api.disc` → `g/disc/throw`, the cut call names
  `g/cut/{make,aim,lock}`, `api.KIT_SOUND_RECIPES` (104 sound names designed from the plan's §3-§5 / §7 sound cells),
  `api.REAPPEAR`, `api.PH`, the FN call names `api.BARS_FNS` / `api.RW_HOOK_LINE`, `api.HANDOVER` / `api.STAGE_BASE`.
- FN-f: PLAN FE-6 / §9.1 say `bars(on)` emits "the flag + `bars_hide` / `bars_show`"; the contract keeps one line per
  call through two new wrappers `mboss/bars_off` / `bars_on` (flag + the existing function), so `bars_hide` /
  `bars_show` themselves never change (§3.1).
- Kit macro args are exactly `api.KIT_PRESETS` (§9.2's signatures). The plan's per-move cells abbreviate them: pass every
  arg (0 where a cell leaves one out, e.g. A2 `qi_arc {r:36,yaw:0,pitch:0,roll:35,c:1}`, A3 `qi_vert {h:34,yaw:…,c:1}`,
  A8.8 `qi_vert {h:34,yaw:0,c:2}` — yaw 0 now stands it across the player's facing; it sits 1.5 b to their right and 1.5 b
  ahead of the cut spot, F2), and `qi_band` takes no `c` (§4.5 A8.2 writes `qi_band {len:70,pitch:35,c:1}`; the band is
  always lilac — call it `{len:70,yaw:0,pitch:35,roll:0,sw:25}`).
- R1 / R3: the `solid` script row (R1 62, R3 46: PLAN "hittable at 62", "reforms 37-46") is when S4 removes
  `rlk_hr_ghost`; the `g_reform` clip's own `solid` event (its tick 4) is only visual.
- The deflect: S3's `shield/judge` plays the success staging of PLAN §5.4 (`clash_gold` + `light_column` + sounds +
  `g_deflect`); S4's gauntlet then lifts the darkness (`arena_look('crimson')`), turns the banner off, sets `#done` at
  `api.REPEL_T`, and on a fail runs its branch (A8 `ult/fail60` + `g_reform`, A13 the `FAIL5_T` staging + `ult/fatal`).

## 7. Change log
- D0 (52b86b9, 11-04): as §0 and §6. (The lead records accepted requests here at I1.)
- D0 fixes (5d2c3ac, 11-04, the adversarial D0 verification; no generated output changed: regenerated twice, identical,
  `check_mboss_pack` 0 problems, the four checkers as §0, `api.py --check` green):
  - `api.BARS_FNS` was `function rlk:mboss/bars_hide` / `bars_show` with S1 told to make those set / clear
    `#mbBarOff`: both already exist and are called by `death_start`, `pause_tick`, `cleanup_fight`, `init`, `main`, `tick`,
    `start_go` and `mboss/bars` — a death pause would have hidden every boss's bars for the rest of its fight. Now the new
    wrappers `mboss/bars_off` / `bars_on` (§3.1, §5 allow-list, S1 brief); a self-check keeps the old names out.
  - Ownership: `HR/tests/lib/**` was S3's while S1's brief creates it (vendored sims + `hrsim.py`) → S1 creates, S3 takes
    over; `HR/tests/test_rig.py` and the regenerated rig outputs were S2a's while S2b's brief edits / commits them →
    S2a → S2b hand-over (`api.HANDOVER`, checked against `api.STAGE_BASE`); the `hr_field` lines S1K's theme makes the
    unchanged arena generator add to `mboss/arena/{job_tick,abort}` were nobody's → S1K; RP patterns now name the real
    paths (`textures` / `models/item` / `items`, the font json and `textures/font/mboss_hr/**`); scratch `HR/<stage>/**`
    (the `rp_readme_*` fragments were unowned), renders `HR/renders/<prefix>_*` (S2a / S2b had no names), RP copies
    `HR/rp_<stage>`, the lead's `regen_all.sh` lines and README (§1).
  - The I1 allow-list gained `mboss/test/help_pattern`, `help_rift_id`, `help_special_ch` (measured; §5).
  - Comments in `api.py`: the `rise2` rename, `BRIM_T` (SQ1 only), the R1 / R3 `solid` row (§6).
  - Documents: §0 names the arena generator's `clear_all` apart from the 21 core dispatchers; §6 records the kit-args,
    `solid` and deflect clarifications; the briefs name every render, the hand-overs, the new base 5d2c3ac and when the lead
    removes a worktree; `HR/tools/regen_d0.sh` makes its path absolute (with a relative `<wt>/roguelike` its closing
    `git status` failed after its own `cd`).
- 11-05 (lead): the user gave the Minecraft EULA consent ("eula 동의"); README 0-2 2 ② / 0-8 record it (commit 0d65e87 on
  `claude/exciting-pascal-ek1vuy`, pushed). Header, §4 and §5 gate 1 updated; the stage helpers `regen_d0.sh` /
  `checkers.sh` use per-worktree scratch folders (S1 request 6).
- 11-05 (lead): loadcheck on the real 26.3 server (`HR/lc/run_lc.sh`, results `HR/lc/<tag>.txt`): the work branch 0d65e87,
  `wip/hr-s1` 1945bce and `wip/hr-s2a` 0c88e7f each → `0 function load failure(s)`, exit 0, `Loaded 1870 advancements`.
- 11-05 (lead): loadcheck `wip/hr-s4` d65ea28, `wip/hr-sr` ad912ff, `wip/hr-s2b` fb97b3b → 0 failures each, `Loaded 1870
  advancements`. I1 is split: I1a (S1+S3+S4, S2a+S2b, SR) now, I1b after S1K (`HR/i1_brief.md`).
- 11-05 (lead): S1K reported (`wip/hr-s1k` 1d2e877); loadcheck → 0 failures, `Loaded 1870 advancements`.
- 11-05 (lead, **I1a** on `wip/hr` in `HR/wt_hr`; S1K / I1b later; notes `HR/i1/i1_notes.md`): merges `--no-ff` of
  `wip/hr-s4` (5f93747), `wip/hr-s2b` (e1fd22a), `wip/hr-sr` (0ae9bf8), no conflicts; the rig built into `HR/rp_hr` (pack hash
  08625cee… = S2b's; `HR/rp_s2b` removed); regenerated with the real rig / sequences (508725e: `rig_stub/**`, `core/sq/**` gone,
  `seq/**` 234; `regen_all.sh` gains the guarded `build_mboss_hr_fx.py --skip-rp` and `build_mboss_scarlet.py` lines);
  `scarlet.enabled` true (21e853f: 26 + 3 `F:mboss` files, §5); the requests (66dafec). Contract changes:
  - `seq.py` (S2b): `lead_stand`'s start dispatched `g` as a string-valued `$function …/g/$(g)`, which `check_mboss_pack`
    resolves only as a numeric family (1 problem on the merged tree) → stored in `rlk:hr seq.g` and two static calls.
  - s3-5: S3's fake players / tags folded into `api.CORE_FP` (+ `api.CORE_CONSTS`) / `api.TAGS` (§2), output-neutral.
  - s4-2: `api.DISC['speed']` 1.8 → **1.75** (exactly 7 framework sub-steps; 1.8 flew 2.0 b/t); `g/disc/throw` `spd:17`.
  - s3-10: a sequence restarted by the resume hook or `/reload` holds its clock one tick (`#sq -1`): the first module tick
    shows clip tick 0 at `#sq 0` (the start and its tick 1 used to run before the first `rig/tick`).
  - s1-4: §5's enabling list = the measured 26 + 3. s1-1: `test_m0diff` `NEW_FAKE` += `#mbBarOff`.
  - Accepted deviations recorded (informational requests): S4's cut hz options `kbdir 1` (s4-4: the kb-3 cuts push along her
    line, not away from the cut's centre); S4's dive landings (s4-5: deflect 1.2 b in front of the player, A8 fail on the
    impact point while the push ring moves the player ≈ 3 b, A13 / lethal fail 2 b in front); SR's game-time deadline timers
    (sr-7), items.md `6초 / 2초 / 10초` (sr-8), `hw_clear` keeping both cooldowns, the 홍련일섬 ICD spent with no target, the
    `translate` + `fallback` buff line (sr-9). Declined: s3-1 (A9 lock 21 vs clip `lock` 22, inside the 6-8 t rule), s1-5
    (`dead_voxel` 6076 kept). Deferred: kit / arena items to I1b, sr-2 (`vBig` outside F5) to R.
- 11-05 (lead, the user's request): the body of the rig wears the user's 64×64 Minecraft skin (`HR/skin/scarlet_skin_64.png`,
  slim 3-px arms (S2d round 2: this line said "classic arms"; the skin paints only 3 + 3 arm columns), outer layers), as the pack's 아를레키노 / 나루카미 rigs use skins; the props (hat, sword, scabbard, cup,
  bottle, `item_sword`) keep S2a's own shapes, recoloured to sit with the skin. PLAN §1.5's originality rule now covers what
  we design ourselves (props, kit, arena); the body is the user's asset. Stage S2c (`wip/hr-s2c` from 66dafec) does the
  re-skin without changing parts, pivots, anchors or clips.
- 11-05 (lead, **I1b** on `wip/hr`, notes `HR/i1/i1_notes.md` §12-§13): merges `--no-ff` of the work branch
  `claude/exciting-pascal-ek1vuy` 0d65e87 (3d2370e: README EULA record only, so the work branch can fast-forward to `wip/hr`)
  and `wip/hr-s1k` 1d2e877 (a0a7dff), no conflicts (0 shared paths); the kit built into `HR/rp_hr` (its 177 kit files hash
  the same as `HR/rp_s1k`'s; `HR/rp_s1k` removed); regenerated with the kit and the theme (5e6c963: only `F:boss/scarlet/**`
  changes, 1139 → later 1145 module functions); registry `icon.model` `rlk:mboss/hr_kit/gate_icon` (00e6489, the item stays
  `minecraft:iron_sword`; only `F:mboss/register` changes); the requests and lead decisions (78e827f). Contract changes:
  - s1k-1 (S4 `p_ghost.py`): the A13 fail's `scarlet_line` `yaw:90` (across the player's view, as CS1 C8); was `yaw:0`.
  - s1k-2 (S3 `core.py`): `core/amb` from `core/fight`: `fx/p/ambient_p1` every 10 t at each player in P1, `fx/p/ambient_p2`
    every 6 t in P2, the down window and the gauntlets (`#ph` 4 / 6 / 7 / 9), none in a sequence (PLAN §6.3 / §6.4).
  - s1k-3 + s2b-4: `api.KIT_PROPS['moon_halo']` looks `p1 p2 off` + **`p1b` `p2b`** = the same sprites 1.2 x brighter. A
    `custom_model_data` tint only multiplies (white = the sprite as painted), so the base looks `p1` / `p2` now carry the tint
    0xD4D4D4 (212 / 255) and the bright looks white (kit `PROPS` rows with a third tint element, `HALO_BRIGHT` / `HALO_TINT`);
    the default halo is therefore 17 % darker than S1K built it. `seq.py`: the bright look of the arena's current look
    (`rlk:mboss look_hr_field` moon -> `p1b`, crimson -> `p2b`) over CS0 E3 (112-146) and the CS4 gaze (690-780), back after,
    also in `seq/intro/skip` and the intro / ending `cancel`.
  - I1b finding (S3 `core.py`): the decor props never followed the arena look (nothing re-looked them after the spawn: the halo
    stayed `p1`, the lotus `bud`, through P2 and the darkness). `core/look/go` now re-looks them with the job: moon `p1` / `bud`,
    crimson `p2` / `bloom`, dark `off` / `bloom` (PLAN §6.3-6.5 "kit props"); `core/deco_re` spawns the lotus of the phase.
  - Lead decision 1 (the intro's end distance): `api.SEAT_POS` (884.5, 201, 0) -> **(884, 201, 5)** (+ the theme's copy
    `mboss_arena_hr_field.SEAT_POS`; the seat clearing moved with it): 5.0 b nearer `start` on the same `start` -> moon line
    (0.06 b off it), 26.73 b from `start`, 5 b from C (PLAN §3.1's "≈ 8 b north of C" no longer holds). The walk keeps its legs
    (1.2 b / 8 t = 0.15 b/t, 17 legs) but a leg now runs while she is more than 7 b away (`seq.py` `m/leg`: `#mbDist ..70`, was
    `..81`, which stopped her anywhere in 7.0-8.1 b and would have left her 7.53 b away). A player who stays at `start` meets her
    6.33 b away (test_scarlet I2: 6.34 b; the skip 6.34-6.50 b); I2 compares the whole end state again (`I2_NEAR_OPEN` false).
    Nothing of the arena sits within 1.8 b of the new seat; render `HR/renders/i1b_intro_open.jpg` (the opening from `start`).
  - Lead decision 2: the `tp … facing entity … eyes` lint line stays an accepted false positive; no `lint_mc` change.
  - s1k-6: the dark look measured on the real server (`HR/i1/tools/darkcheck.sh`, a copy of loadcheck on the same `.lock`):
    every slice tick ≤ 8.6 ms alone, whole look jobs ≤ 23.5 ms, the build 61.4 ms -> `api.DARK_LIGHT` stays true (no fallback B).
  - Verified, nothing to change: s1k-4 / s4-3 (the disc dressing), s1k-5 / sr-6 (`vig` edge-only: centre half alpha 0, outer band
    0.54), s3-7 (`arena/job_tick` has the `hr_field` line; `arjob` stays set until the job's `done`), s1k-8 / s1k-9 (informational).
  - Suites (HR/tests -> `R:tools/dev/sim/hr/tests`): `lib/hrsim.py` resolves `#rlk:dash_pass` / `#rlk:cm_pass` from the
    datapack's tag files (the vendored `cmsim` let only air / light through, so `mv/ok` refused every grass cell of the real
    arena in the sim); `test_kit` scans the merged tree's own module for the kit calls; `test_hwamu` reads PLAN / the wiki from
    `$HR_DOCS` or beside the suite and skips those checks without them; `test_scarlet` `cost` (Z1 / Z2) counts the arena
    look job's slice ticks apart, held to §5 gate 5's look-job limit (≤ 5 k; measured max 3 442 with the kit counted — the
    first I1b figure 3 263 had the kit stubbed, see the next entry), every other fight tick ≤ 3000 as before (2 198 with the
    kit counted; first measured 956 with it stubbed).
- 11-05 (lead, **I1b verification round 1** on `wip/hr`, notes `HR/i1/i1_notes.md` §14): the tick cost is measured with the kit
  running for real (`hrsim.kit_on`: `test_scarlet` `cost` had stubbed every `rlk:boss/scarlet/fx/**` call, so the card ager and
  the presets' bodies were never counted): fight average 505 (≤ 600), every look-job slice tick ≤ 5 k (3 442). With the kit
  counted one tick went over the 3000 per fight tick: CS1 #sq 171, S2b's `leaves_dark {n:40}` (2 915 commands for its 40 cards,
  3 598 in the tick). Contract changes:
  - Kit `fx/p/leaves_dark {n}` (S1K's `build_mboss_hr_fx.py`): **n < 0 = the last -n of the 40 leaves** (each card line now
    `execute unless score #n2 hrFx matches <k-39>..<k>`); a positive n is unchanged (the first n: `{n:8}` / `{n:24}` / `{n:40}`
    make the same cards as before). `api.KIT_PRESETS['leaves_dark']` keeps its one argument `n`.
  - S2b's `seq.py` CS1 C8: `leaves_dark {n:20}` at slash + 2 (#sq 171) and `{n:-20}` at slash + 3 (#sq 172) instead of
    `{n:40}` at 171: the same 40 cards (positions, turns, models), the second half one tick later. The highest fight tick
    without a look-job slice is now 2 198 (#sq 172): `test_scarlet` Z1 / Z2's per-tick bounds (≤ 3000 per fight tick, the
    look-job slice ticks ≤ 5 k as §5 gate 5) hold with the kit counted, so the cost rule the I1b report proposed stands as is.
- 11-05 (lead, **I1b verification round 2** on `wip/hr`, notes `HR/i1/i1_notes.md` §15): the seat was written `884 201 5`
  (`mboss_lib.num` drops `.0`), and the game block-centres an absolute x / z written without a decimal point in summon / tp /
  execute positioned / facing (+0.5; never y) while mcsim reads it as written: in game the rock and her seated start stood at
  (884.5, 201, 5.5), 26.31 b from `start`, the walk ending ≈ 5.91 b from a player there — not the 26.73 b / 6.33 b measured
  above (still ≤ 7 b, still clear of the decor). Contract changes:
  - New `api.xyz(p, nd=4)`: an absolute point for those commands, x and z always with a decimal point (`884.0 201 5.0`).
  - S3's `core.py` (`spawn`, `core/deco` / `core/deco_seat` for the seat rock, `core/replay/start`) and S2b's `seq.py`
    (`rock()` / `rock_kill()`: `seq/intro/k/{24,52,206,630}`, `seq/intro/skip`) write `api.SEAT_POS` through it: 9 command
    lines, so the game now uses `api.SEAT_POS` itself, as the theme's seat clearing, the suites, the opening render and the
    figures above do (26.73 b, 6.33 b; nearest non-air cell 2.12 b). `test_scarlet` K3b checks every such line.
  - Not changed (for the lead): the moon halo (`core/deco`, `core/deco_re`: `summon … 889 218 -33`, 3 lines) and the moon
    target in S2b's CS4 (`facing 889 218 -34`: the landing toward the moon `seq/ending/m/land` 12 lines, the turn
    `seq/ending/turn_moon` 1) have whole x / z too: in game the halo card stands 0.5 b east of the disc's centre and 1.5 b
    (not 1 b) in front of its face, and the CS4 aim toward the moon is off by 0.8° of yaw from C, at most 2.0° anywhere on the
    walk disc. `api.xyz` would put both on their points.

### 11-05 — S2d: her body at the player's size and proportions (lead)
- The user (11-05, after S2c's sheets): "팔다리가 너무 기괴하게 긴데 그냥 플레이어 크기랑 똑같게해". Her body becomes exactly the
  player avatar's body of this pack (`tools/build_player_rig.mjs`: its slim 3-px arms — S2d round 2; rounds 0-1 used classic
  4-px arms on the false premise that the user's skin was classic —, 1 skin px = 1/16 b, height 2.00 b,
  display scale 1), wearing the user's skin unchanged; PLAN §2's "≈ 1.4 × the player" is superseded. The 47 clips keep
  their names, lengths, timing and events and are retargeted to the new skeleton; the props keep their shapes, resized.
- Authorized contract changes (S2d records the values here): `api.BOSS` scale / hit box (a player-size body), `api.HEIGHT`,
  `HAT_TOP`, `BRIM_D` (measured), any rig dimension the module reads. Gameplay hazard geometry and timings do not change.
- S2d's values (`wip/hr-s2c`; `api.py` is the contract, the rig builder asserts each against its own build):
  - registry `scale` 1.35 → **1.0**, `hit` {w 1.2, h 2.9} → **{w 1.2, h 2.4}** (`T:mboss_registry.json`; h − the idle-loop hull top
    2.329 incl. the hat = 0.071, asserted in [0.05, 0.12]); `api.py:39` the pin → `(1.0, {'w': 1.2, 'h': 2.4})`.
  - `HEIGHT, HAT_TOP, BRIM_D` 2.55, 2.82, 1.60 → **2.00, 2.30, 1.32** (the idle-t0 head base top 1.984 within 0.02; the idle-t0
    `hat_crown` anchor 2.302 within 0.01; 2 × the brim radius 0.66). `SWORD_LEN, SCABBARD_LEN, SHADOW_R` 2.10, 1.82, 0.9 → **1.94,
    1.52, 0.6**. New `ITEM_SWORD_LEN, ITEM_SWORD_SCALE = 2.03, 1.375` (`item_sword`'s length at its display scale; seq.py's
    thrown sword reads both). The stub manifest regenerated (`api.py --write-stub`); `core.py` prose (husk 1.0, shield 1.2 × 2.4).
  - Fix round 1 (11-05, the verifiers' findings): the worn hat sits on the head (the brim 0.502 above the neck, level; was 0.567
    tilted −6°, which floated it 4-9 cm over the head's top) → `HAT_TOP` 2.36 → 2.30 and the hit box h 2.5 → 2.4 (the hull top
    2.413 → 2.329); the intro rise moves her off the seat stone (seq.py `SEAT_RISE` 0.4 / `SEAT_ASIDE` 1.1 glides; the stone
    request s2d-2 unchanged).
  - Fix round 2 (11-05, the verifiers' second round): the user's skin is a SLIM skin, so the arms are the avatar's own slim arms
    (`P1_SPECS`: 3 × 12 × 4 px, shoulder pivots ±0.34375 instead of ±0.375; nothing stretched, every face on the skin's own
    columns); no contract value changes (HEIGHT 2.00, HAT_TOP 2.30, hit 1.2 × 2.4, BRIM_D 1.32, the sword / scabbard / item
    lengths as above). The crown's top is the drum's own 16-gon (no square lid corners). The rig's feet step with the intro's
    1.1-b aside glide (`scarlet_retarget.mjs` patch ASIDE; seq.py unchanged). A player who stays at `start` meets her 6.76 b away
    at the intro's end (the skip 6.50-6.76 b; I2's limit 7.05; the 6.33 b above is I1b's measure before S2d's rise / aside glides).
  - Fix round 3 (11-05, the verifiers' third round): rig-only, no contract value changes. The elbow is a hinge (the forearm
    takes the upper arm's front through the elbow); `g_dive` (played from the hidden rig after g_vert's 'gone') takes the rig's
    own `blend: 1` (the whole body shows at t1; its length, events and name unchanged); what ships stays near the solved frame
    after every first key (a build gate); the core.py stand-in anchors follow the built idle-t0 ones (no generated output).
  - Unchanged: `api.HITS`, ranges, `DISC`, `LEAP_H`, `SEAT_POS`, timings, `PARTS`, `LOOKS`, `ANCHORS`, every clip / event / call.
  - The rig manifest gains `skeleton`, `dims`, `support` (per clip: the S2a contact truth `low_ref`, the seat / lie / kneel / feet /
    touch / air / ghost / held / free-right-hand spans, the root weight `w_root`, cuts, the last-resort lifts, the hat pushes clear
    of her head `hat_push`, the hand contacts) and `retarget` (factors, the declared
    patches, bounds, slopes, the per-clip correction table) — the suites read them; `item_sword.toss_offset` (seq.py's toss summon).
  - Couplings: WT's seq.py / s3lib.py / p1.py / p_ghost.py / core.py heights (design §6.1); WH-only files: `HR/requests/s2d.md`.

### 11-05 — I2: the player-size body merged into `wip/hr` (lead)
- 11-05 (lead, **I2** on `wip/hr`, notes `HR/i1/i1_notes.md` §16): merge `--no-ff` of `wip/hr-s2c` 4e46cd7 (S2c fb4c16e + S2d
  c070a59 … 4e46cd7: her body is the player avatar's body wearing the user's skin, 2.00 b, display scale 1, the 47 clips retargeted)
  into 4c81817 (merge commit 254c329; the requests, the regenerated tree and the docs f3231fe). One source conflict, `core.py`'s
  `spawn` comment (both sides kept: S2d's "husk scale 1.0 / shield 1.2 x 2.4" with I1b's `api.xyz(seat)`), and 82 generated files
  (`F:boss/scarlet/p/**`, `seq/event/**`, the intro's tick buckets, `spawn`, `F:mboss/register`: either side, then regenerated).
  `api.py`, `seq.py`, `p_ghost.py` and the registry merged with both sides' hunks (S2d's size couplings above; I1b's `api.xyz`, the seat
  (884.0, 201, 5.0), the walk rule `..70`, the halo `p1b` / `p2b` looks and restores, `core/amb`, `core/look/go`, the CS1 `leaves_dark`
  split); the rig sources are S2d's. The rebuilt rig (`boss/scarlet/rig/**`, the manifest) equals 4e46cd7 byte for byte, and `RP`'s
  `mboss/scarlet/**` equal `HR/rp_s2c`'s. S2d's requests (`HR/requests/s2d.md`), dispositions:
  - s2d-1 **applied**: the kit's afterimage sprite is the player-size figure (`mboss_hr_fx_paint.AI_S` 2.65: brim at 2.00 ± 0.035,
    \|x\| < 0.66; crown 2.00-2.31; square head; two legs; slim arms from ±0.344) and its card `s0` / `s1` 2.8 → 2.65 (`api.KIT_SPRITES`
    and the sprite size unchanged; S3's call at the body + 1.2 and `AI_CLAMP` kept). RP: `hr_kit/afterimage.png` is the only kit
    file that changed.
  - s2d-2 **applied**: the kit's seat stone `SEAT` rock (0, 0.12, −0.185) × (1.2, 0.24, 0.64) (top 0.24 b = her thighs' underside, 0.135 b
    in front of her anchor to 0.505 b behind), bottle (0.42, 0.24, −0.15) 0.42, cup (−0.42, 0.24, −0.15) 0.26 (were 1.5 × 0.75 × 1.1 b,
    top 0.75 b); the display's local +Z is its facing, so the stone stands behind her heels (no z negation; = the rig's `SUP`);
    `test_kit` seat items ≥ 0.19 b over the display; the arena's `SEAT_CLEAR` 1.8 kept.
  - s2d-3 **applied**: the kit's preset docs name the new call heights (17 presets, ≈ × 0.78); `test_kit` `HEIGHT` (19 rows) and
    `VARIANTS` (qi_fan `h` 13, qi_vert 19).
  - s2d-4 **applied** (optional, cosmetic): blink_bubble 1.4 / 2.4, ghost_burst 1.7 / 1.6, ghost_flash 1.9, star4 1.3, qi_ribbon 1.2 / 1.5,
    ghost_trail 2.8 / 3.1, ev_leave spread (0.5, 0.95, 0.5), leaves_swirl dust (1.0, 0.8, 1.0); `yellow_tell` kept (a gameplay tell).
  - s2d-5 **applied**: `test_rig` = S2d's; `ev_dry` = I1b's + S2d's edits (`seq.S0` / `seq.SWORD_R`, the S23 toss-offset check; a
    three-way `git merge-file`, no conflict); `test_kit` as s2d-2 / s2d-3; `HR/tests` == `R:tools/dev/sim/hr/tests` afterwards. The
    intro's end distance re-measured (test_scarlet `skip`): **6.76 b** from a player who stays at `start` (the skip 6.50-6.76 b; I2's
    limit 7.05) — I1b's 6.33 b plus S2d's rise / aside glides.
  - s2d-6 **applied** (README 「홍련」: hit 1.2 × 2.4, scale 1.0, the stone 1.2 × 0.24 × 0.64 b, the rise / aside walk, ≈ 6.8 b, the
    shadow 0.6, S2d's rig item, the stone's top 0.24 b; the RP README from `HR/s2d/rp_readme_rig.md`).
  - s2d-7 **applied** (the merge recipe; `ANCHOR_OFF`, `g_dive` `blend: 1`, `HIP_DIR` came with the merge).
  New numbers (I1b 4c81817 → I2): registry `scale` 1.35 → 1.0, `hit` 1.2 × 2.9 → 1.2 × 2.4; rig 2 629 → 2 600 functions (5.70 MB),
  22 050 → 18 800 keys / 2 109 → 2 084 key files, 78 → 62 models, 48 sprites 83 712 px → 27 + the skin 47 872 px, elements at rest
  2 304 → 224; module 1 145 → 1 149 functions (`seq/**` 457 → 461: the rise / aside moves); `F:boss/scarlet/**` 4 203 → 4 178; stitched
  atlas 12.955 → 12.919 M (1 478 → 1 458 sources); RP 89b6c70ce9e351811df7fb05443efd11e15bb053 (4 733 files); the fight cost (kit running) average 505 → 502, the highest tick without a look-job slice 2 198 → 2 189
  (CS1 #sq 172), the slice ticks 3 442 → 3 444 (≤ 5 k). Gates (i1_notes §16.5): regenerate twice (tree 48615482 = HEAD, RP
  89b6c70c both passes), `check_mboss_pack` 0, `api.py --check`, every 홍련 suite (test_rig --rebuild 152, ev_dry 68, test_scarlet
  144, pat_p1 341, pat_ghost 186, special 93, reward 51, hwamu 258, moon 50, kit 10 594, arena 89, ident_hr, gen_check_hr 28),
  run_all = I1b's 40 step lines, the checkers 0 unclassified, rplint 0, loadcheck `hr_i2` 0 failures / 1870 advancements.

### 11-05 — F1: the review's gameplay fixes (lane F1, `wip/hr-f1` from 4c81817; merged at F-I)
- HR-01 / HR-07 / HR-06 (core): `#grs` 4 (the judged A8 fail → P2 at once) and 5 (a lethal gauntlet past its last
  counting cut with pips left: the fail pending → `core/g/fail_now` at the resume / reload once the player is back and
  alive → the revive path); `core/g/pause` keeps the first pause's `#grs` when a /reload follows; tests 30 / 35 refuse
  outside P1 / P2; `#pipoff` cleared in `core/g/end` / `core/g/pause`.
- HR-04: `core/fp` starts neither the counter nor A6 while `#fl` is reserved; `ai/phase` drops both flags.
- The P1 pressure package (HR-13 / HR-14 / HR-18 F part / HR-25 / HR-26 / HR-38): `api.PAT_END` (A1 24, A2 22, A3 79,
  A4 46, A9 40, A10 32), R1 / R3 end 67 / 49, `RECOVER` P1 12-20 / P2 10-16, `WEIGHTS` P1 near A1 10 · A2 10 · A10 20,
  `TRIGGER_ONLY` ('a6',), `COOLDOWN` A9 160 / 140 · A10 180 / 150 · A6 400 / 400 (`A6_TRIGGER['cd']` too), the backstep
  + mid pick after two empty picks, the counter / rear rules only in the near band, the flinch replays the move clip,
  every tail kept turns her to the player and from `TAIL_MOVE` 4 t after the last hit (A4 its landing, R1 / R3 the
  solid row, R2 4 t after its last release) walks / strafes as the recovery (`ai/tail`, `ai/tail_step`; the recovery
  keeps the move: `ai/tail_keep`, `#ai_tmc`); a flinch replays the move clip (the approach glide too). Tiers T1-T4
  untouched (S5).
- HR-19: `DMG['TC']` 37, the 18 counting rows of `A8_SCRIPT` / `A13_SCRIPT` on `('TC', KB_CUT)`.
- HR-15: `api.DISC_LOCK`, `g/disc/lock`; HR-27: `REAPPEAR` D2 55 / D4 −55; HR-22: A2's blade glow; HR-28: A4 / A10 trails.
- Names: `#ai_nn #ai_bs #ai_tmc` in `CORE_FP`; `api.TAIL_MOVE`; tag `rlk_hr_gln`.

### 11-05 — F2: the review's kit / sequence / arena / text fixes (lane F2, `wip/hr-f2` from 4c81817; merged at F-I)
- HR-02: the dying one-shot facing is `rotate` (the player toward her eyes from their own eyes, the avatar `rlk_av` toward
  her feet), no `tp`, no `view/sync`. HR-12: `qi_vert` / `qi_fan` / `qi_line` stand across the aim, `qi_arc` / `qi_wedge`
  with |roll| 20..160 rolled in the screen plane (face kinds `qi_arcf_0..3` / `qi_wedgef`, the same sprites; 5 + 5 RP
  files), the callers per the footage (A3 h1 / h3 / h4, A5's line from 5 b on her left, A8.3 2 b ahead, A8.8 1.5 b right /
  ahead), contract §6's A8.8 `yaw:0` corrected. HR-16: `api.LINE_MAX_PX` 192, `api.LINE_PAGES` (5, 22, 24). HR-17: the
  kit's keep switch (`keep_on` / `keep_off`, `api.KIT_KEEP_TAG`) on the instant deaths' line / petals / bolts and CS3's
  kick. HR-23: the follow switch (`follow_on` / `follow_off`, objective `hrFxY`) on the A13 / R2 / A10 yellow tells, A6's
  bubble, A4's ribbon. HR-24: A9's streak `K.pw('qi_cut', core.a9)` (new `api.K.pw`). HR-29: no boss bar in CS0 (her
  spawn hook and `core/intro/begin` `bars(0)`, `intro/done` `bars(1)` + the 30-t `bars_ramp`), `hudHold 2` through CS0 /
  CS1 / CS4 / the coda. HR-30: overlay fades as opacity-step glyphs U+EC20-EC37 while a line is up (font `rlk:mboss_hr`
  31 glyphs). HR-32: `qi_band` gains `sw` (`api.KIT_PRESETS`; A8.2 25, CS4 E1b her distance + 1 b). HR-41 / HR-42: level
  presets (absolute pitch; `core/amb1` / `amb2` `rotated ~ 0`). HR-43: `coarse_dirt` under opaque covers / full water in
  every look (23 280 cells). HR-44: `scarlet_line` floor-safe at any call height. HR-45: first-person anchors
  (`@a[tag=rlk_body]`). HR-46: CS0's wind at the player. LF-01: the moon halo summoned at exact x / z (`api.xyz`); LF-02:
  the ending's moon facing at exact x / z. Kit functions 429 → 446.
- F2 round 1: the HUD-off sequences blank the actionbar at start (`seq.HUD_BLANK`); her spawn hook turns the bars off
  (`start_go` guarded by `#mbBarOff`: the F-I request f2-8); face-mode `qi_arc` / `qi_wedge` bursts on the shape
  (`fx/e/rollv` / `rollf`); `qi_line` callers along an aim turn by −90 (f2-7, applied at F-I); the fight cost with the kit
  running at 3c69fcc: average 510, max without a look-job slice 2 291, slice ticks max 3 475 (≤ 600 / 3 000 / 5 000).

### 11-05 — F3: the review's item / reward / framework fixes (lane F3, `wip/hr-f3` from 4c81817; merged at F-I)
- 11-05 — F3 (review fixes HR-05, HR-08, HR-09, HR-10, HR-11, HR-33, HR-34, HR-35, HR-39 game part): cleanup resets
  objective hr whole but the event scores (+ storage seq); vBig counted down in every view (view/tick; ride_tick /
  sel_xhair no longer count); 검신합일's dodge only inside the dash's own i-frames, never at an rlk_mb_inv body; the
  sword's state and cooldowns reset per run (hw_reset); the buff scope one switch (#hrMoonRun + buff_scope, numbers from
  the scores everywhere); the coda item title 「화무십일홍 ★☆☆」 in the item's own star colours with 「[ MYTHIC ]」 on the
  subtitle, the buff subtitle two numbers + the third on the actionbar (widths ≤ 106 / ≤ 192 font px); no F5 sneak-tap
  during a boss intro. sr-2 settled. New names: `#hrMoonRun tmp`, `#hrEvK #hrEvDoneK #hrEvDropK tmp`, storage `ev.sx`,
  `ev/stars`, `items/proc/hw_dash` / `hw_reset`, `#hwDashEnd`; `api.BUFF_SCOPE_WORDS`, `api.EV_CHAT_BUFF_HEAD`, `EV_TEXT`
  `item_name` / `buff_stats` / `buff_ab`. Pack-wide hand-file lines (contract §1 SR row, `ident_hr` group "F3 review
  fixes"): `F:view/{tick,ride_tick,sel_xhair}`, `F:lvup/tick`, `F:items/hook/on_dash`.

### 11-06 — F-I: the review-fix lanes F1 / F2 / F3 merged into `wip/hr` (lead)
- 11-05/06 (lead, **F-I** on `wip/hr`, notes `HR/i1/i1_notes.md` §17): merges `--no-ff` into f3231fe (I2) of `wip/hr-f3` cbe4dc2
  (98a5fc2), `wip/hr-f1` 67504a7 (d17c331), `wip/hr-f2` 3c69fcc (55850a0); every side's source and suite hunks kept (the
  conflicts: README ×5, the kit generator's four preset docs, `p1.py` ×4, `p_ghost.py`, `seq.py`, `pat_p1` ×4, `pat_ghost` ×2,
  `test_kit`, `test_scarlet`; F2's call lines at S2d's heights), generated conflicts (30) taken from either side and
  regenerated. Contract changes of this step (beside the F1 / F2 / F3 entries above, which F-I applied):
  - **The body change under the lanes**: A10's dive `qi_line` from her body + 0.8 and turned `rotated ~-90 ~` (F1 request 2
    + f2-7; `qi_line` runs across its executor's facing since HR-12); the A3 / A5 / A9 / A7 call lines at S2d's heights.
    `test_kit`'s `view` camera looks at her chest at the module's default effect height on S2d's body (1.0 b, was S2a's 1.3);
    A1's fan F5 floor 250 → 165 px (S2d's 1.3-b fan); the `qi_wedge {roll:90}` test variant at r 28. TAIL_MOVE 4 kept
    (the hand-over turns ≤ 56°/t on S2d's rig; §4.1).
  - **f2-8** (framework, §3.1 FN-f): `mboss/start_go`'s closing `bars_show` → `execute unless score #mbBarOff mb matches 1 run
    function rlk:mboss/bars_show` (`T:build_mboss_core.py`); `check_mboss_pack`'s FN-f rule allows exactly that line in
    `start_go` (any other `#mbBarOff` line there fails); `ident_hr` allows `F:mboss/start_go` (group "F-I review fixes").
    Every other boss: `fight_vars` zeroes the flag earlier in `start_go`, so `bars_show` runs as before.
  - **HR-03** (§1 S2a row, §2 ids, §3.7): `rlk:mboss/scarlet/item_sword`'s item definition selects on `display_context`:
    gui / fixed / ground → the new slot icon `rlk:mboss/scarlet/item_sword_icon` (the rig generator's `ICON`: drawn in GUI px,
    long parts ≥ 2 GUI px wide, rig sprites only, 0 px; lit front), every other context (the hands, the coda's
    `item_display` none) → the rig model; the rig model's guard card on its guard plate; the manifest's `item_sword.icon`;
    63 rig models.
  - **HR-31** (PLAN §3.7 E1): `seq.SEAM_CUT` = ovl `white` in 0 hold 2 out 1 at CS4 tick 0: the hat's move from the repel's
    DOWN over her face runs under it.
  - **5b**: A3 h4's crescent stays 2.0 b ahead (at 3-4 b it stands behind a player at the 2.4-b chain stop: 0 px in first
    person).
  - Tests: test_rig + 10 (HR-03 ×9, the CS3 → CS4 seam), ev_dry + 1 (the seam), test_scarlet + 3 (C3: objective hr only the
    event scores after each cleanup path, f3 r5); test_reward leaves the coda's blank actionbar (F2's `seq.HUD_BLANK`) out of
    the buff's actionbars (F2 × F3, found in the gate).
  New numbers (I2 f3231fe → F-I): module 1 149 → 1 144 functions (S3 275 → 284, S4 413 → 399, `seq/**` 461); `F:boss/scarlet/**`
  4 178 → 4 190; kit 429 → 446 functions, 31 glyphs; rig 62 → 63 models (2 600 functions, 18 800 keys unchanged); RP
  27d6ae57b4d3dce641b34dfe246a0008715778a4 (4 769 files); stitched atlas 12.919 M (1 458 sources, unchanged); the fight cost (kit running) average 502 →
  535, the highest tick without a look-job slice 2 189 → 2 282 (CS1 #sq 172), the slice ticks 3 444 → 3 477 (≤ 600 / 3 000 / 5 000).
  Gates (i1_notes §17.6): regenerate twice (tree = HEAD, RP 27d6ae57 both passes), `check_mboss_pack` 0, `api.py --check`,
  every 홍련 suite (test_rig --rebuild 162, ev_dry 78, test_scarlet 188, pat_p1 387, pat_ghost 205, special 98, reward 61, hwamu 283, moon 55, kit 13 435, arena 93, ident_hr, gen_check_hr 28), run_all = I2's 40 step lines (README 0-9's known failures only; macro + 8 classified), the checkers 0 unclassified (vs I2: macro + 10, lint + 1 — instances of known kinds from the lanes; F2-4's accepted `tp` line gone), rplint 0, loadcheck `hr_fi` 0 failures / 1870
  advancements.

### 11-06 — V2: the small R-late part 2 findings HR-48, HR-50 … HR-55 (lane V2, `wip/hr-v2` from 3741fc4)
- 11-06 (lane **V2**, notes `HR/v/v2_progress.md`; the lead's decisions of 11-06 in `HR/review/findings.md`):
  - **HR-48** (§3.3 kit calls; PLAN §4.3 A1): A1's hit crescent `qi_arc {r:40,…,roll:-25,c:1}` (`p1.A1_ROLL`: it stands across
    her aim as A2's roll 35 does; flat it showed ≥ 1 500 card px on one tick of seven in first person), the fan `qi_fan
    {h:16,c:2}` at her body + 1.1, 1.2 b ahead (was h 13 at + 0.85). `test_kit` `view`: A1's sites need their floor on ≥ 3 of
    the 7 ticks in F5 and in first person (crescent 1 500 / 1 500, the fan 250 in F5 = F2's floor back, 1 500 in first
    person); the other contact effects keep the maximum (A3 h1 / h3 reach 1 500 on 2 F5 ticks, A4's line on 1: for the lead).
  - **HR-50** (§5 gate 5): `test_scarlet` `cost` also runs the down window (by its timer with the kipup; a 5 % floor hit in it →
    `lead_down`), the A8 fail → P2, the A13 instant death → Ronova's revive → the stance → `lead_stand` → A13, a 20-t pause and a
    /reload (its own `mboss/init` chain counted as a tick) right after A8's judge (from CS1, the dark arena), in P2 and in the down
    window; Z2 covers them, Z5 checks they are all reached.
  - **HR-51** (§3.4): `core/look/go` starts no arena job when `built_hr_field` already reads `hr_field@<ver>:<look>` (the decor
    re-look and the served request stay). Z4: no look job on an arena already in that look in any cost world.
  - **HR-52** (§3.3 `seat_rock`): the seat stone's bottle / cup left the kit's per-tick prop chain `fx/e/anim` (their own check
    `fx/e/stay_t` every 10 t); `core/intro/done`, `core/replay/end`, `core/deco_seat` re-look the stone `bare` before they kill
    it (`core.seat_gone`). Z6: `fx/e/anim` runs on 0 of 639 CS0 ticks (602 before, ~39 commands each).
  - **HR-53**: PLAN §3.1 — the intro walk ends 6.76 b (the skip 6.50-6.76 b) from a player at `start`.
  - **HR-54**: README 0-9 lists the other bosses' `cmsim.py` copies that let only air / light through `#rlk:dash_pass` (not
    ported). **HR-55**: `test_arena_hr` 1e's second interpreter runs with `-B` (1f checks it).
  New numbers (F-I 3741fc4 → V2): kit 446 → 447 functions (`fx/e/stay_t`); `F:boss/scarlet/**` 4 190 → 4 191; module 1 144
  unchanged; RP unchanged (27d6ae57). The fight cost, now over the fight states above (5 834 ticks): average 500 (kit 67;
  P1 559, P2 524, A8 553, A13 574, A8 fail 531, A13 fail 489, down 315, lead_down 461, pause 361, reload 420), the highest tick
  without a look-job slice 2 278 (CS1 #sq 172; a /reload chain ≤ 2 068), the 82 slice ticks avg 1 765, max 3 475 (CS1 #sq 174)
  (≤ 600 / 3 000 / 5 000). The same gate on 3741fc4: average 507, 2 282, 106 slice ticks, max 3 642 (the resume after a pause
  on A8's judge re-ran crimson; D6 measured 3 672 on the test-21 path) — F-I's 535 / 2 282 / 3 477 covered a subset. CS0
  average 325 → 287.
  Gates (`HR/v/v2_progress.md`): regenerate twice (`regen_d0.sh` ×2, tree identical, only V2's files changed), `check_mboss_pack`
  0, `api.py --check`, every 홍련 suite (test_rig --rebuild 162, ev_dry 78, test_scarlet 192 (+ L6, Z4, Z5, Z6), pat_p1 387,
  pat_ghost 205 (J7 rewritten for HR-51), special 98, reward 61, hwamu 283, moon 55, kit 13 585, arena 94 (+ 1f), ident_hr,
  gen_check_hr 28), rplint 0 (the RP copy test_rig rebuilt = 27d6ae57), loadcheck `hr_v2` 0 failures / 1870 advancements.

### 11-06 — S5: the balance pass (on `wip/hr` from 3741fc4; commits ed2e175 (fight) + 005f00a (item / buff, README))
- 11-06 (stage **S5**, notes `HR/s5/progress.md`; the lead's decisions HR-13 / 14 / 18 point 5, HR-19, HR-20 / 21 / 39, HR-36 /
  37 / 40): numbers only, no clip / line / look / behaviour change.
  - **Fight** (`api.py`, PLAN §4.1 / §4.2 / §4.3 / §4.4 / §4.7 / §4.8 / §8): `WEIGHTS` P1 near A9 25 → 40, A10 20 → 40;
    `COOLDOWN` A10 180 / 150 → 120 / 100 (P2 = P1 × 0.85; A9 160 / 140 and A6 400 / 400 kept); `RECOVER` P1 12-20 → 8-16
    (P2 10-16 kept); `DMG` T3 56 → 62 (T1 / T2 / T4 / TC 29 / 42 / 71 / 37 kept); registry `scarlet.hp` 250 → 260
    (`F:mboss/register` regenerated). `TRACK`, `TAIL_MOVE`, `PAT_END` unchanged (tracking was measured and rejected).
  - **Item / buff** (SR's hand files, PLAN §7.0 / §7.3 / §7.4 / §7.5 / §7.6): `F:items/tune/b10` `#hwCtrCdT` 40 → 80 (★ 104 /
    96 / 88 / 80 t), `#hwSlCoef` 849 → 500 (250 / 334 / 417 / 500 %); `F:load` `#hrMoonAtk` 20 → 27; `api.BUFF_VALUES['run']`
    (27, 10, 10) and `api.EV_TEXT` buff_stats / buff_sub / chat_buff / status at +27 % (the generated texts are score
    components: no generated file changed); `items.md` (쿨타임 4초, 500 %); the tooltip follows the constants.
  - Suites that pin them: `pat_p1` F11, `pat_ghost` G1 (R1 / R3 T3 62), `test_hwamu` (the counter cooldown and the slash
    coefficient read from b10), `test_moon` (× (1 + `BUFF_VALUES` run) instead of × 1.20).
  - The probe (`HR/review/bal`, not shipped): hrfair 1.2 (re-vendored `lib/hrsim.py`, the ranged walker's guard, the body's
    `rlk_mb_inv` on every event), batch / run_hr / analyze (ERR markers and exit codes, T9 at Lv5 / 10 / 15), reward_ev (the
    game's counter rule, dense rooms `room/roomfair.py`, G2 in eight readings); results PLAN §4.8 / §7.4.7.

### 11-06 — V1: HR-47 / HR-49 in the rig (lane V1, `wip/hr-v1` from 3741fc4; recorded at V-I)
- 11-06 (lane **V1**, notes `HR/v/v1_progress.md`; the lead's decisions of 11-06 in `HR/review/findings.md`): rig sources and
  outputs only (§3.2: `PARTS`, `LOOKS`, `ANCHORS`, every clip's length / loop / events / calls unchanged; no module change).
  - **HR-47**: `scarlet_pose.mjs` step 9b guards `gripClear` (the sword grip moves with the blade translated, its rotation = the
    attack direction kept), `handClearL` / `handClearR` (a free hand, the two-hand right fist, the hand-held scabbard), `scabFwd`
    (the hip scabbard's mouth forward through a draw); the builder plans one direction per tick over a clip and stops on a fist /
    hilt / guard sample ≥ 0.01 b inside her head or torso as shipped (manifest `retarget.clips[*].clear`); retarget patches
    `A10-HIGH`, `DRAW-E`, `IAI` ramp-out 161-164.
  - **HR-49**: retarget patches `WALK` (stance slide 58 → 48 %, the swing foot lifted 0.063 b) and `STRAFE-L` / `STRAFE-R` (lifted
    side steps, slide 92 → 41 %); `api.WALK_SPEED` and the clips' lengths / events unchanged.
  - test_rig 162 → 164 (`clear`, `gait`; both fail on 3741fc4). Rig 2 600 → 2 640 functions (5.72 MB), keys 18 800 → 18 881 / key
    files 2 084 → 2 119; elements at rest 224; RP unchanged (27d6ae57).

### 11-06 — V-I: V1 and V2 merged into `wip/hr`, the release gates, the stamp, the docs (lead)
- 11-06 (lead, **V-I** on `wip/hr` from S5's 005f00a, notes `HR/v/vi_progress.md`): merges `--no-ff` of `wip/hr-v1` 93ef7ae (66f64f5,
  no conflict: S5 touched none of the rig's inputs) and `wip/hr-v2` c12cdbc (bb80f5c; one conflict, README's `boss/scarlet/**`
  count, both sides kept: 4 231; `pat_ghost` merged S5's G1 and V2's J7 without a conflict). Regenerating (the rig into RP, the
  module, the kit, `regen_d0.sh`, `regen_all.sh`) changed nothing, twice; no other boss's output differs from 0d65e87.
  `ident_hr` allows the datapack `pack.mcmeta` (the release build stamp, README 0-5 step 3; aa363ae). Build stamp c77e5d1
  (`빌드 11-06 홍련 · 특수 보스`; RP `pack.mcmeta` · README §6 outside git). The plan / contract / briefs / requests / findings /
  the S5 probe's README and logs / i1_notes copied to the repository's `tools/dev/sim/hr/` (the trailer lines → `<세션이 정해 준 trailer>`).
  Gates on bb80f5c: regenerate twice (tree identical, RP 27d6ae57 both passes), `check_mboss_pack` 0, `api.py --check`, every 홍련
  suite (test_rig --rebuild 164, ev_dry 78, special 98, test_scarlet 192, pat_p1 387, pat_ghost 205, reward 61, hwamu 283, moon 55,
  kit 13 585, arena 94, ident_hr, gen_check_hr 28); the fight cost 5 834 ticks avg 500 (kit 68; P1 563, P2 521, A8 553, A13 574,
  A8 fail 531, A13 fail 489, down 315, lead_down 461, pause 360, reload 420), the highest tick without a slice 2 279 (CS1 #sq 172),
  82 slice ticks avg 1 765 max 3 474 (≤ 600 / 3 000 / 5 000); `run_all` the same 40 step lines as F-I / S5 (README 0-9's known
  failures only); `ar/tests` (run_all.sh: test_cm_ar 65, test_arena_fl 46 — its first run since 11-03 —, test_kit 8 928;
  test_arlecchino, pat_p1, pat_p2, kit_dry, test_rig 67) all green; the checkers vs 35b82e5 (= 0d65e87's datapack) 0 unclassified
  (vs F-I: refs / macro / nbt identical, lint + 81 rig uuid targets from V1); rplint 0; atlas 12.919 M (1 458); elements 224;
  loadcheck `rel_1106` and after the stamp `rel_1106b` 0 failures / 1870 advancements. Release RP hash
  b3df6a5f0476cb71426fad61e8c5d3878aac4878 (4 769 files).
