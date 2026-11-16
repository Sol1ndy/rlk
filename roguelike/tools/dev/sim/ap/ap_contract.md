# 아펩의 오아시스 파수꾼 (Apep) — module contract (`ap_contract.md`)

Status: **§0 = the day-0 interfaces** (stage AP-SPEC, 2026-10-19; binding plan `S:ap/plan.md` v1 §3.9 and the AP-SPEC
row of §10). §0 is written once and afterwards only **extended by request** (`S:ap/requests/<stage>.md`, the request
protocol of §0.11); nothing in it is renamed or re-ticked without a dated change note in plan §14 and in §0.12 here.
AP-CORE appends §1 onwards (core ↔ pattern / org / revival / kit / rig) at its first commit; every later stage appends
its own section.

| short | meaning |
|---|---|
| `S:` | `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad` |
| `DP` | `/home/user/rlk/roguelike` |
| `M0` | release branch `claude/exciting-pascal-ek1vuy` at **99bc097** (build stamp of the `wip/fg` merge 63b37b6, plan §0 "M0"); every name below was grepped on it (read-only) |
| `RIGLIB` | **039b911** on the same branch, right above M0: `T:mboss_shape_lib.mjs` + the `mboss_rig_compile.mjs` extras (`tol.tp`, per-rig culling, per-state follow lists, `follow_y`, the static-anchor skip, `fitTrack`). **Park (FN-25 NEW) is not in it** (§0.4.7) |
| `T:` / `F:` / `AP:` | `DP/tools/` / `DP/data/rlk/function/` / `F:mboss/apep/` |
| `cm.md`, `theme.md`, `fx.md`, `manifest.md`, `s2.md` | the Azhdaha day-0 contracts in `S:az/contract/` (read 2026-10-19 02:07 UTC; last change cm.md 2026-10-18 23:03 UTC) |
| `FN-n` | an item of `S:ap/framework_needs.md` |
| ticks / units | played ticks (after RETIME); blocks; Minecraft yaw degrees (+ = clockwise seen from above, 0 = facing +z / south); at the framework boundary tenths of a block (cm.md §0) |

Contents: 0.1 what day 0 fixes · 0.2 alignment with Azhdaha · 0.3 names · 0.4 rig manifest schema · 0.5 org manifest
schema · 0.6 theme interface (FN-3) · 0.7 kit call list · 0.8 pattern ids and test ids · 0.9 stubs and validator ·
0.10 deliberate differences from Azhdaha · 0.11 decisions, requests, open items · 0.12 change notes · 0.13 the
10-20 telegraph rule · **1 module interfaces (AP-CORE)**: 1.1 layout and ownership · 1.2 the tick · 1.3 patterns and the
slot · 1.4 Gen · 1.5 services · 1.6 required files · 1.7 AI · 1.8 test ids · 1.9 scores · 1.10 stand-ins · 1.11 decisions.

---------------------------------------------------------------------------------------------------

## 0.1 What day 0 fixes, and for whom

| item (plan §3.9) | file(s) | the real thing is written by | read by |
|---|---|---|---|
| 1 rig manifest schema | §0.4, `S:ap/spec/rig_manifest.schema.json` | AP-R1 … AP-RC2 (`T:mboss_apep_rig_manifest.json`) | the framework (proxies, capsules, px sets: cm.md §9), AP-CORE (`api.py`, `stub_rig.py`), patterns through `api.py` |
| 2 org manifest schema | §0.5, `S:ap/spec/org_manifest.schema.json` | AP-ORG1 / ORG2 (`T:mboss_apep_org_manifest.json`) | AP-CORE (`api.py`, `stub_org.py`), AP-REV (`revival.py`, `org.py`), AP-P1 (stalk props), AP-P3 (domes) |
| 3 kit call list | `S:ap/ap_fx_api.md` §0 (summary in §0.7) | AP-FX | every module author through `api.K` |
| 4 theme interface | §0.6 | AP-ARENA (`T:mboss_arena_ap_oasis.py`) | the chapter-mode arena / room generators (cm.md §6, theme.md §3), AP-CORE (props, points), AP-REV / AP-P3 (points) |
| 5 names, test ids, stubs | §0.3, §0.8, §0.9; `S:ap/spec/stub_rig_manifest.json`, `stub_org_manifest.json`, `make_stubs.py`, `validate.py` | AP-SPEC (stubs) → AP-CORE copies them into `T:mboss_apep/` | everyone |

Done when (plan §10): the stub manifests validate against the schemas: `python3 -I S:ap/spec/validate.py` → exit 0
(§0.9).

---------------------------------------------------------------------------------------------------

## 0.2 Alignment with the Azhdaha day-0 contracts

Apep is the second client of the chapter mode (AZ-CM). Everything Apep shares with Azhdaha uses Azhdaha's schema and
names; this file only adds what Azhdaha does not have.

| Azhdaha contract | Apep use |
|---|---|
| `cm.md` (framework: registry v2, routing, `cb/*`, per-arena functions and sliced jobs, pools / floor / title, RES, proxies, music, bars, cleanup, helpers §13, UUIDs §14) | **adopted as is** (cm.md: "Apep adopts it as is"). Its §17.2 "Adopt" rows are applied here (§0.3.6, §0.4.6, §0.6, §0.10 rows A1-A9) |
| `manifest.md` (rig manifest schema v1) | **the base of §0.4**: same top-level keys, the same clip record, the same frames, units and px-key rules; Apep only **adds** keys (`"apep": 1` marks the extras; the framework ignores them) |
| `theme.md` (theme-module interface) | **the base of §0.6**: same required / optional names, the same `props()` record and `entrance_layout()` dict; Apep fills `look_lines(look)` (optional there, required here) |
| `fx.md` (kit conventions) | **the base of `ap_fx_api.md` §0**: same engine entry points, argument names and order, `nd`, stacked `tele/wedge` swept sweeps, wave ids, safe rims, the mask wash, no rig calls, no kit-owned boss-bar lines; deliberate differences in `ap_fx_api.md` §0.13 |
| `s2.md` (core ↔ pattern authors) | the **model** for AP-CORE's §1 (`api.Pattern`, `Gen`, `TL`, `p/<key>/{start,tick,cancel}`, the request protocol); here only the pattern ids / keys and test ids are fixed (§0.8) |

Where Apep's binding plan used a name that AZ-CM settled differently, the AZ-CM name wins (rows A1-A9 of §0.10). Every
place where Apep deliberately differs is listed in §0.10 (rows D1-D24).

---------------------------------------------------------------------------------------------------

## 0.3 Names (plan §3.6, grounded on M0)

Every prefix below was checked free on M0 99bc097 (`git grep` over the repository: no `#ap*`, `#apq`, `rlk_mb_ap_*`,
`rlk_ap_om_*`, `apRig*`, `apK apS apShd apOC apOI apSock apTok`, `#wk*`, `wkS`, `rlk_wk*`, `rlk:apkit`, `mboss_ap`,
`rlk_mb_arena_prop`, `rlk_mb_ar_*` or U+E900 in any file; the `apT` / `apL` hits are substrings of `vMapT` / `vMapL`).

### 0.3.1 Function namespaces (`rlk:mboss/apep/**`)

| path | owner | content |
|---|---|---|
| `AP:<hook>` | AP-CORE (generated) | the 17 `L.HOOKS` (`spawn intro_tick tick on_hit aux_hit incoming pause resume death_start death_tick cleanup reload bars hz_vis pj_end test uninstall`) + `prep` (`L.CHAPTER_HOOKS`, cm.md §5.3) |
| `AP:rig/**` | rig generator `T:build_mboss_apep_rig.mjs` | the rig API (§0.4.9), debug poses `AP:rig/ap_dbg/<clip>/<t>` |
| `AP:om/**` | org generator `T:build_mboss_apep_org.mjs` | `om/<kind>/c/<clip>/k/<t>` key functions, the per-kind dispatch on `apOI` / `apOC`, object spawns (§0.5.4) |
| `AP:fx/{card,cardx,look,clear,uninstall}`, `AP:fx/{e,p,tele,dress,snd,hud,prop,test}/**` | kit `T:build_mboss_ap_fx.py` | `ap_fx_api.md` §0.1 |
| `AP:p/<key>/**` | the pattern module of that key (§0.8) | `start`, `tick`, `cancel` + declared hooks (s2.md §3 shape) |
| `AP:org/**`, `AP:heart/**`, `AP:wall/**` | AP-REV (`org.py`, `revival.py`) | organism runtime, Heart events `heart/add {v}` / `heart/sub {v}`, nesting walls |
| `AP:dome/**` | AP-P3 (`aftermath.py`) | 종말의 여파 domes |
| `AP:seq/**` | AP-P1 (`seq.py`) | E, D |
| `AP:ai/**`, `AP:arena/**`, every other `AP:` path | AP-CORE | deciders; `arena/props/<look>`, `arena/props_kill` (theme props, §0.6.6) |

The module generator `T:build_mboss_apep.py` owns `AP:**` minus `AP:rig/**`, `AP:om/**` and the kit's owned paths, and
cleans only what it owns (the fieldgen / Azhdaha `foreign()` rule, plan §3.5).

### 0.3.2 Entity tags

| tag(s) | on | notes |
|---|---|---|
| `rlk_room rlk_mb_aux` | every entity the module, the org runtime or a pattern creates, **except** arena props | every cleanup path removes them (`init` kills every `rlk_mb_aux`, plan §7.2) |
| `rlk_mb_apep_part`, `rlk_mb_ap_<part>` | rig parts (49 names, §0.4.3) | `rlk_mb_ap_shadow` on the shadow helper |
| `rlk_mb_ap_org` + `rlk_mb_ap_<kind>` | organism husks (`aux/spawn`; `rlk_mob`, never `rlk_zmob`) | kinds `basic nurt guard nest destr pred` (§0.5.2) |
| `rlk_ap_om_<display>` | organism passengers (models) | + `rlk_room rlk_mb_aux`; key functions select `execute on passengers if entity @s[tag=rlk_ap_om_<display>]` |
| `rlk_mb_ap_heart` | the Heart **marker** only (centre; not `rlk_mob`) | its displays carry `rlk_mb_ap_heart_bulb`, `…_heart_cradle`, `…_heart_arms`, `…_heart_tips`, `…_vine_hand`, `…_vine_stem_<k>` |
| `rlk_mb_ap_dome` + `rlk_mb_hzsafe` (`mbHzSG` = the cast's group) | a dome **marker** (FN-14, cm.md §13.6) | displays `rlk_mb_ap_dome_shell`, `rlk_mb_ap_dome_decor` |
| `rlk_mb_ap_wall` | a 둥지 wall **group marker** (records its barrier blocks, plan §7.6.7) | blade displays `rlk_mb_ap_wall_blade` |
| `rlk_mb_ap_stalk`, `rlk_mb_ap_stalk_low / _high / _tip` | 생명의 손 stalk root marker / displays | |
| `rlk_mb_ap_seed` | the death seed prop | |
| `rlk_mb_ap_pat` + `rlk_mb_ap_p<id>…` | everything a pattern creates (markers, props) | s2.md §12 analogue; rig part, kind and object names never start with `p<digit>` |
| `rlk_mb_ap_lock`, `rlk_mb_ap_kept` | pattern lock markers (`lockp` / `lockb` / re-tagged `lockv`, `keep`) | the framework's `rlk_mb_lock` is removed when a module keeps a marker (cm.md §13.1) |
| `rlk_mb_arena_prop rlk_mb_ar_ap_oasis rlk_mb_ap_ar_<group>` | arena props (`props(look)`, §0.6.6) | **no `rlk_room`, no `rlk_mb_aux`**; the framework kills `rlk_mb_arena_prop` in `cleanup_aux` and `reload` (cm.md §12) |
| `rlk_wk*` | kit cards (`ap_fx_api.md` §0.1) | + `rlk_room rlk_mb_aux` |
| framework | `rlk_mb_body`, `rlk_mb_big`, `rlk_mb_inv`, `rlk_mb_pxinv`, `rlk_mb_noshield`, `rlk_mb_px`, `rlk_mb_px_<proxy>`, `rlk_mb_hzsafe`, `rlk_mb_resel`, `rlk_mb_broken` | cm.md; never written by name outside the documented calls |

### 0.3.3 Scores, objectives, storage

**Fake players (`mb`), the core's** (plan §3.6): `#apPh` (1, 15 = T1, 2, 25 = CS, 3, 9 = death; 0 = entrance), `#apTot`
(mirror of `#mbTot`), `#apHt` (‱), `#apWave`, `#apClk` (stage clock), `#apTo` (time-out state), `#apFail` (strikes),
`#apAftCd`, `#apAftN`, `#apAft1`, `#apLast`, `#apZone`, `#apBand`, `#apBackT`, `#apChain`, `#apStance` (0 CROUCH,
1 UPRIGHT), `#apPark`, `#apTr` (transition queued, plan §7.2). **Reserved for AP-CORE by AP-SPEC**: `#apPT` (the main
pattern clock = the clip tick, s2.md `#azPT` analogue), `#apPid` (the running pattern id). **Pattern scratch**:
`#apq<id><name>` (e.g. `#apq5A`; the AZ prefix is `#aq<id>`, so the two never meet); a pattern's storage
`rlk:mboss ap.p<id>.*`.

**Entity objectives** (created by the module's `init`, removed by `uninstall`): `apK` (kind 1-6), `apS` (state), `apT`
(state clock), `apL` (link id), `apShd` (shield pool), `apOC` / `apOI` (org clip clock / clip id), `apSock` (Heart
socket 0-2, −1 none), `apTok` (attack token); rig `apRig*` (§0.4.3: `apRigC apRigT apRigF apRigY apRigState apRigForm
apRigStance apRigFace apRigCore apRigGlow apRigTint apRigBright apRigHands apRigPark`). Framework objectives Apep writes:
`mbRes0..8` on organisms (+ `rlk_mb_resel`, FN-7 / cm.md §8), `mbHzSG` on dome markers.

**Storage**: `rlk:mboss ap.*` (the module; removed by its `cleanup` / `uninstall`), `rlk:mboss cprep.apep.{gate,title,
sub}` (written by `AP:prep`, cm.md §3.3), `rlk:apkit` (kit), `rlk:mboss built_ap_oasis` (the framework's arena stamp
`"ap_oasis@<ver>:<look>"`, cm.md §6.4 — **the current look is read from it**, §0.10 A2).

### 0.3.4 UUID blocks (`524c4b4d-4150-…`, "AP")

| block | ints | content |
|---|---|---|
| rig `524c4b4d-4150-4400-8000-0000000000NN` | `[I;1380731725,1095779328,-2147483648,NN]` | parts `0x00-0x37` (49 used, append-only name table), shadow `0x40`, proxies `0x41-0x50` (11 used: `0x41-0x4B`, `pxBase 65`), props `0x51-0xFF` (none at day 0) |
| objects `524c4b4d-4150-4800-8000-0000000000NN` | `[I;1380731725,1095780352,-2147483648,NN]` | Heart bulb `0x00`, cradle `0x01`, arms `0x02`, tips `0x03`, vine hand `0x04`, vine stem `0x05-0x08`; domes `0x10-0x15` (dome k: shell `0x10 + 2k`, decor `0x11 + 2k`); stalks `0x20-0x2B` (stalk k: low `0x20 + 3k`, high `0x21 + 3k`, tip `0x22 + 3k`); seed `0x30` |
| arena props `524c4b4d-4150-4100-8000-0000000000NN` | `[I;1380731725,1095778560,-2147483648,NN]` | §0.6.6: water tiles `0x00-0x0F`, pond props `0x10-0x3F`, bank crystals `0x40-0x5F`, entrance crystals none (they are `rlk_room` entities of `prep`) |

Organisms and wall blades are multi-instance (no fixed UUIDs). The Azhdaha block is `…415a-4400…`, cproto `…4350-4400…`
(cm.md §14).

### 0.3.5 Kit, font, models

Kit prefixes `#wk*` (objective `mb`), objectives `wkS wkG wkH wkK wkD`, tags `rlk_wk*`, storage `rlk:apkit`, font
`rlk:mboss_ap` **U+E900-E9FF** (FN-28; checked against `hud`, `minimap`, `bossbar`, `mboss_gd`, `mboss_bf`, `mboss_fg`,
`mboss_az`). Item models: rig `rlk:mboss/apep/<model>` (`assets/rlk/{items,models/item,textures}/mboss/apep/`), org
`rlk:mboss/apep_om/<model>` (`…/mboss/apep_om/`), kit `rlk:mboss/ap_kit/<kind>` (`…/mboss/ap_kit/`); atlas entries
appended to `assets/minecraft/atlases/items.json` by each generator's merge only.

### 0.3.6 Registry entries (data-only; plan §3.7 + the cm.md §17.2 "Adopt" rows)

```json
{ "id": "apep", "n": 11, "enabled": true, "kind": "chapter", "ch": [3], "w": 0, "minCh": 3, "maxCh": 3, "route": false,
  "name": "아펩의 오아시스 파수꾼", "sub": "종막 오아시스 파수꾼", "color": "#C9C452", "el": 7,
  "hp": 290, "xp": 40, "atk": 12, "lvAdd": 0, "dmgMul": 150, "goldMul": 1, "sap": 0, "picks": 0,
  "scale": 2.0, "hit": {"w": 2.6, "h": 3.6}, "intro": 110, "death": 140, "deathSnd": false,
  "arena": "ap_oasis", "theme": "ap_oasis", "px": true, "pxBase": 65, "shield": true,
  "res": {"7": 30, "*": 10}, "phases": [53, 47],
  "music": {"1": {"ev": "minecraft:music.overworld.deep_dark", "len": 0},
            "2": {"ev": "minecraft:music.nether.soul_sand_valley", "len": 0},
            "3": {"ev": "minecraft:music.overworld.lush_caves", "len": 0}},
  "icon": {"item": "minecraft:pitcher_plant", "model": "minecraft:pitcher_plant"} }
```

```json
"ap_oasis": {"n": 2, "theme": "ap_oasis", "ver": 1, "cx": 440, "cy": 201, "cz": 8, "r": 29, "walk": 26, "safe": 24,
             "start": {"x": 440.5, "y": 201.0, "z": 24.5, "yaw": 180.0, "pitch": 0.0},
             "box": {"x0": 396, "y0": 190, "z0": -36, "x1": 484, "y1": 250, "z1": 52},
             "looks": ["withered", "lush"], "oob": {"y0": 198, "y1": 217}, "sweep": {"y0": 201, "y1": 202}}
```

- `enabled: true` from the AP-CORE commit that adds `T:build_mboss_apep.py` (an enabled chapter entry without its module
  fails the pack check, cm.md §2.4); `route: false` until AP-I2 (`test/chapter {id:"apep"}` works before).
- `n` 11 and arena `n` 2 are the numbers AZ-CM reserves for Apep (cm.md §2.3 / §2.4). `px`, `pxBase`, `shield` are the
  cm.md §17.2 FN-1 "Adopt" row; `shield: true` keeps the torso click shield `hit` beside the 11 proxies.
- `sweep {201, 202}` makes `cb/won`, `mboss/cleanup` and `cb/remove` run `arena/ap_oasis/sweep` (cm.md §2.3, FN-26).
- `oob` 198..217 is the framework default `cy − 3 … cy + 16`, written out.
- `hp` 290 may move inside 270-320 by the fairness pass; music `len` values are measured by the chapter-mode stage
  (FN-23) and written by request.
- Arena boxes on M0 + AZ-CM do not overlap (plaza x 176..223, `az_cavern` x 280..360, `cp_test` x 524..556, the dungeon
  square −64..63; `ap_oasis` x 396..484).

### 0.3.7 Generator files (plan §3.5) and order

Order (cm.md §1.2 extended by plan §3.5): core → arena (plaza, cp_test, az_cavern, **ap_oasis**) → `build_cboss_rooms.py`
→ proto → cproto → rig generators (Guardian, butterfly, fieldgen, azhdaha, **apep rig**, **apep org**) → guardian → bf
kit → butterfly → fg kit → fieldgen → az kit → azhdaha → **ap kit** → **apep** → `check_mboss_pack.py`. The core reads
the committed Apep manifests (cm.md §1.2: a commit that changes a manifest also commits the regenerated `F:mboss/px/**`).

---------------------------------------------------------------------------------------------------

## 0.4 Rig manifest schema (`S:ap/spec/rig_manifest.schema.json`)

= **Azhdaha manifest v1** (manifest.md §1-§7: keys, shapes, frames, units, the clip record, px keys) **+ the Apep
extras** (plan R4-R22). JSON Schema 2020-12; the cross-reference rules the schema cannot express are in `validate.py`
(§0.9) and are part of the contract.

### 0.4.1 Files and merge (manifest.md §1)

| file | writer | `source` |
|---|---|---|
| `T:mboss_apep_rig_manifest.json` | `T:build_mboss_apep_rig.mjs` (AP-R1 … AP-RC2) | `"rig"` |
| `T:mboss_apep/stub_rig_manifest.json` | AP-CORE's `stub_rig.py`, **byte-identical** to `S:ap/spec/stub_rig_manifest.json` (or regenerated by the same code) | `"stub"` |

The framework reads the real file only when it has `"schema": 1, "source": "rig"`, else the stub, and merges per clip
exactly as `api.py` does (cm.md §9.2): real clips first, stub clips for names the real file lacks (`api.FALLBACKS`,
printed; the AP-I2 build asserts it is empty); global keys (`proxies`, `uuids`, `states`, `capsules`, `runtime`) from the
real file when present. Stub clip ids for merged fallbacks are ≥ 1000 (cm.md §9.2).

### 0.4.2 Frames, units, ticks (manifest.md §2, unchanged)

- **Rig frame** (+x the boss's left, +y up, **+z back**): only `skeleton.joints`, `skeleton.joints_by_stance`,
  `rest_extents`, clip `extents`, `cull_overhang`, `parts[].reach`.
- **Local frame** for every gameplay field (`rest_anchors`, `stances.rest_anchors`, `anchors`, `tracks`, `px`,
  `capsules`, `proxies.rest`, `proxies.rest_by_stance`): **x = s** (+ the boss's left), y up, **z = f** (+ forward,
  toward the hood), blocks, origin = the anchor on the floor (the body husk; module position + yaw only, plan R2).
  `local = (rig.x, rig.y, −rig.z)`; `^x ^y ^z` from the anchor is literally the value.
- Ticks are played ticks; 0 = the tick the clip starts = the pattern clock tick. Yaw in Minecraft degrees.
- No horizontal root travel and no root yaw inside clips (R16); vertical travel (`pelvis.y`) is in the clip; the module
  moves and turns the anchor.

### 0.4.3 Top level

AZ v1 keys (same meaning; Apep values):

| key | Apep content |
|---|---|
| `schema` | 1 |
| `boss` | `"apep"` |
| `source` | `"rig"` / `"stub"` |
| `runtime` | `{"ns": "rlk:mboss/apep/rig/", "clip_obj": "apRigC", "tick_obj": "apRigT", "state_obj": "apRigState", "form_obj": "apRigForm", "stance_obj": "apRigStance", "face_obj": "apRigFace", "core_obj": "apRigCore", "glow_obj": "apRigGlow", "tint_obj": "apRigTint", "bright_obj": "apRigBright", "hands_obj": "apRigHands", "park_obj": "apRigPark"}` (anchor objectives; the framework uses `clip_obj` / `tick_obj`) |
| `functions` | the rig API as full function ids (§0.4.9) |
| `parts` | 49 records `name region uuid idx tag model brightness scale elements` (AZ) **+ `parent`, `tol_tp`, optional `brightness_p3`, `reach`**; ≤ 56 (R4) |
| `shadow` | `{uuid: block + "40", idx: 64, tag: "rlk_mb_ap_shadow", shadow_radius: 4.5, shadow_strength: 0.8}` (R6) |
| `uuids` | `{block: "524c4b4d-4150-4400-8000-0000000000", ints: [1380731725, 1095779328, -2147483648], parts: {name: idx}, shadow: 64, proxies: {name: idx}, props: {}}` |
| `skeleton` | `joints` (CROUCH, rig frame), `scale_H` (4.4), **+ `joints_by_stance {CROUCH, UPRIGHT}` and `bones {name: {parent, pose_only}}`** (R2: `root pelvis clav_a_l clav_a_r hood_hinge` are pose-only) |
| `rest_anchors` | local, **CROUCH** (the P1 spawn stance): `pelvis thorax shoulder head hood_front hood_top crown face core tail_root tail_tip hand_a_l hand_a_r hand_b_l hand_b_r hand_c_l hand_c_r` (= `stances.rest_anchors.CROUCH`) |
| `torso_hw` | 1.5 (CROUCH; per stance in `stances.torso_hw`) |
| `proxies` | `layout` (11 records `name part point w top_margin tail_only idx uuid flash`, + optional `plan`), `rest` (= CROUCH), **+ `rest_by_stance {CROUCH, UPRIGHT}`, `coverage`** (§0.4.6) |
| `states` | the framework px sets (§0.4.6) |
| `capsules` | push boxes (§0.4.6) |
| `flash_groups` | `head body front rear tail arms` (R7) → parts (every part in exactly one group) |
| `looks` | look channels `form face core core_glow tint bright` (§0.4.7), each `{objective, ids, functions, parts?, brightness?, also?, colors?, forms?, item_pattern?}` (the R1 channel record of Azhdaha) |
| `tinted_items` | `{item: {model, tint}}` (R12 constant-tint item definitions) |
| `clips` | §0.4.4 |
| `culling` | `{"width": 30, "height": 16, "view_range": 3}` (R6) |
| `rest_extents` | optional R1 bookkeeping |
| `budgets` | `parts`, `part_cap` 56, `models`, `hand_models`, `atlas_px`, `atlas_budget` 900000, `elements_shown_rest {p1, p3}`, `elements_budget {p1: 7000, p3: 8000}`, `regions {region: {parts, px}}` |
| `objectives` | `{apRig*: description}` (every runtime / channel objective listed) |
| `textures` | number of ledger sprites |
| `fallbacks` | stub only: every clip name |

Apep extras (top level): `apep` (1), `stances`, `hands`, `park`, `sprites`, `elements` (§0.4.7-§0.4.8).

**Part names and idx** (append-only table, plan R4 order; regions `head body limbs hands tail`): 0 `abdomen`, 1 `hem_a`,
2 `hem_b`, 3 `chest`, 4 `shoulders`, 5 `core`, 6 `crys_low`, 7 `crys_back`, 8 `neck`, 9 `head`, 10 `face`, 11 `hood`,
12 `crown`, 13 `hair_l_1`, 14 `hair_r_1`, 15 `hair_l_2`, 16 `hair_r_2`, 17 `mantle_l_a`, 18 `mantle_r_a`,
19 `mantle_l_b`, 20 `mantle_r_b`, 21 `a_up_l`, 22 `a_up_r`, 23 `a_lo_l`, 24 `a_lo_r`, 25 `a_hand_l`, 26 `a_hand_r`,
27 `b_up_l`, 28 `b_up_r`, 29 `b_lo_l`, 30 `b_lo_r`, 31 `b_hand_l`, 32 `b_hand_r`, 33 `c_up_l`, 34 `c_up_r`, 35 `c_lo_l`,
36 `c_lo_r`, 37 `c_hand_l`, 38 `c_hand_r`, 39-45 `tail_1` … `tail_7`, 46 `tail_tip`, 47 `beads_l`, 48 `beads_r`. Plan
R2 / R4 write `A_up`, `clav_A`, `px_A_l`: in the manifest, tags and functions every name is lower case with an `_l` /
`_r` suffix (Azhdaha's `paw_l` style). Seven spare slots `0x31-0x37` (R4).

### 0.4.4 Clip record

AZ v1 fields (manifest.md §4, same rules): `id name len authored loop next mirror_of retime events anchors tracks px yaw
hidden root_z state` (+ bookkeeping `extents cull_overhang keyFiles keys`, optional `note`).

| field | Apep rule |
|---|---|
| `name` | the 36 plan §6.3 names (§0.4.10); other names only as `dbg_<name>` (ignored by the module and the checks) |
| `events` | `{name: played tick}`, `0 ≤ t ≤ len`; repeated names numbered `name_1 … name_k` (manifest.md D6: `step_1 … step_4`, `hit_1 …`); the plan's `raise` stays `raise` |
| `retime` | `[[authored, played], …]` from `[0, 0]` to `[authored, len]`, monotone, `[]` when authored = len (plan §6.3 knots) |
| `mirror_of` | always null (Apep has no mirrored clips) |
| `hidden` | inclusive `[t0, t1, "all"]` spans (the whole body burrows; plan §6.3 writes half-open `[a, b]` with −1 = to the end: `[a, b) → [a, b − 1]`) |
| `root_z` | always `[]` (no tail-only state; the root sinks straight down, R9 `follow_y`) |
| `state` | rig visibility switches `[[t, "normal" | "burrowed"]]` at the hidden-span edges (`functions.state.*`) |
| `px` | `{"lerp": true, "keys": {"<t>": {proxy: [x, z, top]}}}`, all 11 proxies in every key, keys at 0 and len − 1 and at every stance-move start / end and hidden-span edge; `top` 0 = hidden (every key inside a hidden span) |
| `yaw` | null or dense cumulative deltas, one per played tick (§0.4.5) |
| `tracks` | `tail_root`, `tail_tip` dense, local, before the yaw schedule (§0.4.5) |
| `anchors` | `{event: {point: [x, y, z]}}` local, at that event's tick (§0.4.5) |

Apep fields (required on every clip unless marked optional):

| field | shape | meaning; who applies it |
|---|---|---|
| `form` | `"p1"` / `"p3"` / `"any"` | the form look the clip is authored for |
| `stance` | `{start, end}` (`CROUCH` / `UPRIGHT`) | the stance at tick 0 and after the last tick |
| `stance_events` | `[[t, STANCE]]` | the tick a stance change completes (`crouch_p3` t7, `stand_p3` t13, …); **the rig** writes `apRigStance` there |
| `px_sets` | `[[t, set]]`, first entry at t 0 | the framework px set from that tick (§0.4.6); **the core** calls `function rlk:mboss/px/state {set:"<set>"}` on those ticks (a set equal to the current one is skipped) |
| `look_events` | `[[t, channel, look]]` | look swaps inside the clip (`tint`, `face`, `core`, `core_glow`, `form`, `bright`); **the rig's clip keys** apply them and write the channel objective |
| `hand_events` | `[[t, set]]` or `[[t, part, variant]]` | R8 hand-model swaps with the 0.9 → 1 scale pulse (`hands.pulse`); **the rig's clip keys** apply them |
| `keyed_pitch` | optional `[t0, t1]` | ticks whose root pitch is keyed (the `move_strike_p3` hoop 49-61, R16) |
| `scale_in` | optional `[t0, t1, from]` | the R12 scale-in (`emerge_on_p1` 1-4 from 0.85) |
| `blend_in`, `blend_out` | optional ticks | pose blend into / out of the clip (`revival` → `idle_p3` 6, `death` 6) |

A clip played alone (a test, `ap_dbg`) therefore shows its own looks, hands, stance and visibility; the module calls
`look/*`, `hands/*`, `stance/*`, `bright/*` only outside clips (spawn, reload, the CS form swap, unpark). The module
reads the current state from the objectives, never from its own copies.

### 0.4.5 Yaw schedules, tracks, anchors

- **Yaw** (manifest.md §4.5 rules): `yaw[t]` = the cumulative anchor-yaw delta the module applies at played tick t
  (Minecraft degrees). Signs are a convention: the module mirrors a schedule for the other side. Required (R16) for
  `turn_p1_step`, `turn_p3`, `rotation`, `hands`, `combo_c`, `aftermath`, `tail_p1x2`, `tail_p3`, `move_strike_p3`;
  null elsewhere. Binding knots (`validate.YAW_KNOTS`, ±1°, constant before the first knot):

  | clip | knots (t → cumulative °) | from |
  |---|---|---|
  | `turn_p1_step` | 0 → 0, 9 → −90 | 90° in 10 t (§6.3) |
  | `turn_p3` | 0 → 0, 19 → 114 | **a loop: a rate**, 6°/t (plan §7.3 "turns ≤ 6°/t"); the module applies the per-tick delta while the remaining turn lasts (D7) |
  | `rotation` | 32 → 0, 34 → −4, 36 → −14, 38 → −36, 40 → −66, 56 → −306, 58 → −330, 60 → −346, 62 → −356, 64 → −360, linear (fix 10-22f: was 47 → 0, 71 → 360 smooth) | the whirl 32-64 into and over the strike at 40 (§5) |
  | `hands` | 5 → 0, 27 → 360 | swirl 5-27 |
  | `combo_c` | 5 → 0, 15 → 360 | spin 5-15 |
  | `aftermath` | 18 → 0, 36 → 360 | whirl 18-36 |
  | `move_strike_p3` | 66 → 0, 72 → 360 | sweep yaw 66-72 |
  | `tail_p1x2` | 27 → 0, 35 → 200, 51 → 200, 59 → 0 | 8 swept ticks × 25° per swing (§8.1 P5), swing 2 reversed |
  | `tail_p3` | 13 → 0, 21 → 200, 24 → 200, 36 → 0, 45 → −17, 51 → −204, 53 → −230, 57 → −230, 86 → −360 (AP-FIX RV-01: was 13 → 0, 21 → 200, 45 → 200, 53 → 0) | §8.3 Q4 (swing 1 t14-21, swing 2 t46-53 across the post-lunge front) |

- **Tracks** (manifest.md §4.3): `tail_root` and `tail_tip`, one entry per played tick, local, before the yaw
  schedule. Required for `tail_p1x2` and `tail_p3` (the swept wedges of plan §7.11 rule 3: `api.wedges()` composes track
  × yaw for each swept tick and emits the `hz/sector` wedge and the matching `tele/wedge` from the same numbers). The
  `move_strike_p3` whip is a 360° disc (`hz/disc r 12`), so no track. Fix 10-22f: `rotation` carries `hand_a_r` (the
  striking right A claw tip; `validate.SWING_TRACKS`), from which `p1.py` asserts the swing contact (§5).
- **Anchors** (manifest.md §4.1 shape), required (`validate.ANCHORS`):

  | clip | event → points |
  |---|---|
  | `entrance_p1` | `touch` → `hand_a_r` (the A claw at the hanging Heart) |
  | `burrow_strike` | `burst` → `impact` |
  | `hands` | `plunge` → `impact` |
  | `glow_slams` | `slam1`, `slam2`, `slam3` → `impact` |
  | `rotation` | `crash` → `impact`, `hand_a_r` (fix 10-22f) |
  | `tail_p1x2`, `tail_p3` | `cock` → `tail_tip`; `swing1`, `swing2` → `tail_root` |
  | `combo_a`, `combo_c` | `hit` → `impact` |
  | `combo_b`, `combo_d` | `slam` → `impact` (4.8 b / 7.2 b ahead, §8.1 P6) |
  | `move_strike_p3` | `burst`, `slam` → `impact`; `sweep` → `tail_root` |
  | `aftermath` | `charge`, `blast` → `core` |
  | `shells` | `launch`, `ball` → `ball` (the charge ball over the crown, + 1.5 b) |
  | `surface_p3` | `launch` → `muzzle` (the flat shot's origin) |
  | `spikes` | `column`, `summon` → `crown` |

  Floor points have y 0. `api.anchor(clip, event, point)` is the only way patterns and the kit get positions on the
  boss (`ap_fx_api.md` §0.2).

### 0.4.6 Proxies, px sets, capsules

- **Layout** (R7; idx `0x41 + position`, `mbPart` = position + 1): `head` (part `head`, flash `head`), `chest` (`chest`,
  `body`), `abd` (`abdomen`, `rear`), `tail_a` (`tail_3`, `tail`), `tail_b` (`tail_6`, `tail`), `a_l` / `a_r`
  (`a_hand_*`, `arms`), `b_l` / `b_r` (`b_hand_*`, `front`), `c_l` / `c_r` (`c_hand_*`, `rear`). The plan's `px_` prefix
  is dropped (Azhdaha style; `plan` keeps `px_<name>`). One interaction width per proxy = **max** of the two stance
  widths of R7 (D2).
- **Columns** `[x, z, top]` local; `proxies.rest_by_stance.{CROUCH, UPRIGHT}` hold the R7 tables (ground point, top =
  the column height); clip keys interpolate between them over the stance moves (R7 "the unfold slides the columns").
  `proxies.coverage` = `{within: 3.0, target: 1.0, poses: [CROUCH, UPRIGHT, HOOP, CROUCH_OVER]}` (the R7 merge gate).
- **States** = the framework px sets (cm.md §9.4; record `{px, vis, inv, capsules}` exactly as manifest.md §6.2). All
  eight are required:

  | set | px | vis | inv | capsules | used |
  |---|---|---|---|---|---|
  | `p1` | all 11 | `normal` | false | `sac`, `hips` | phase 1 (CROUCH) |
  | `p3u` | all 11 (UPRIGHT columns) | `normal` | false | `stem` | phase 3 upright |
  | `p3c` | all 11 (CROUCH columns) | `normal` | false | `sac`, `hips` | phase 3 crawl |
  | `burrowed` | none | null | true | none | every short burrow (P1, P3, R, T1 sink, Q1, Q3s) together with husk scale 0.1 + `rlk_mb_noshield` (FN-13) |
  | `aloft` | `head`, `chest` (tops 10) | `normal` | false | none | the Q2 hover (`aftermath` 84-175) |
  | `parked` | none | null | true | none | phase 2 (R10) |
  | `inv` | none | null | true | none | the framework's spawn set; the entrance E and the CS `revival` |
  | `dead` | none | null | true | none | `death_start` (framework) |

  `vis` is null where the clips switch the visibility themselves (`burrowed` sinks visibly before it hides). `burrowed`
  is a px set **and** a rig visibility state (`functions.state.burrowed`); the two are independent (D1).
  `stances.px_set` = `{p1: {CROUCH: p1}, p3: {CROUCH: p3c, UPRIGHT: p3u}}`. Every tick inside a hidden span has an
  `inv: true` set without proxies (validator).
- **Capsules** (FN-21, cm.md §13.5) in the AZ box form: `f0 ≤ f ≤ f1, |s| < hw` (local, blocks), optional `px` /
  `top_max`; Apep keeps the plan R11 column as `col {f, r}` (f0 = f − r, f1 = f + r, hw = r): `sac` (f 0.0..2.0, hw 1.0;
  the belly sac + thorax column r 1.0 around f +1.0), `hips` (f −2.2..0.2, hw 1.2), `stem` (f −1.4..1.4, hw 1.4; the
  UPRIGHT robe stem). Legs, arms and tail stay walk-through (R11). The module requests the push per tick
  (`#mbPushOn 1`) only in the non-hidden, non-moving states.

### 0.4.7 Stances, hands, looks, park

- **`stances`** = `{objective: apRigStance, ids: {CROUCH: 0, UPRIGHT: 1}, default: {p1: CROUCH, p3: UPRIGHT},
  rest_anchors: {CROUCH, UPRIGHT}, torso_hw: {CROUCH: 1.5, UPRIGHT: 1.3}, heights (hood top 4.4 / crown 5.0 / length 15;
  hood top 8.5 / face 6.0-7.85), transitions: {stand_p3: CROUCH → UPRIGHT, crouch_p3: UPRIGHT → CROUCH}, px_set}`. Phase-3
  crawl = CROUCH with the p3 looks (R1).
- **`hands`** (R8) = `{objective: apRigHands, parts: [a_hand_l, a_hand_r, b_hand_l, b_hand_r, c_hand_l, c_hand_r],
  variants: {part: {variant: model}}, sets: {set: {part: variant}}, ids: {set: id}, functions: {set: "…/hands/<set>",
  part: "…/hand/<part>/<variant>"}, pulse: {from: 0.9, to: 1.0, ticks: 2}}`. Variants: A `p1_planted p1_raised p3_fork`,
  B `p1_open p1_curl p3_curl p3_open`, C `p1_open p1_curl p3_curl` (20 hand models). Sets: `p1_rest` (planted / open /
  open), `p1_lift` (raised / curl / curl), `p3_open` (fork / open / curl), `p3_curl` (fork / curl / curl). The plan's
  "hands `open`" / "`curl`" in phase-3 clips = `p3_open` / `p3_curl`.
- **`looks`** channels (R12; ids per channel, functions `…/look/<channel>/<look>`): `form` `p1 p3` (`parts` = every
  non-hand, non-face, non-core part's model per form; `also` = the face / core / hands / tint the form swap sets);
  `face` `p1_bud p3_idle p3_charge p3_dim hidden` (`hidden` = scale 0); `core` `p1_bulb p3_sternum`; `core_glow` `idle
  lit` (core brightness 12 / 15); `tint` `none p1_dark p1_brown withered p3_dim` (`colors`, `forms`, constant-tint item
  definitions `item_pattern "{model}_t{id}"`, `tintindex 0` on every painted face, the untinted-face count is a builder
  check); `bright` `13 15` (the `p3_lit` charge: every part 15; functions `…/bright/13`, `…/bright/15`). **No body look
  swap inside `stand_p3` / `crouch_p3`** (R12): only hand and face events there.
- **`park`** (R10) = `{objective: apRigPark, px_set: parked, shadow: false, tick: "skip", respawn: "keeps scale 0 while
  the flag is set", reapply: [form, stance, looks, hands, follow]}`. RIGLIB at 039b911 has the static-anchor follow skip
  but **no park flag** (FN-25 NEW): the Apep rig builder writes `rig/park` / `rig/unpark` itself on top of the skip and
  makes its own respawn check honour `apRigPark` (FN-25's documented fallback); no shared rig library is edited (R20).

### 0.4.8 Budgets, sprite ledger, element counts

- **`sprites`** (R13) = `{budget: 900000, total, regions: {region: px}, ledger: [{name, region (head body limbs hands
  tail shared), w, h (multiples of 16, ≤ 512), px = w × h, px_per_b, use: "unique" | "tinted", forms: "p1" | "p3" |
  "both", parts?}], planned, densities: {face: 64, crown: 64, b_hand: 64, hood: 48, default: 32}}`. `planned: true` only
  in the stub (a planning ledger, 0.37 M px); the real manifest lists the painted sprites (`planned: false`).
  `total` = Σ ledger = `budgets.atlas_px` ≤ 900 000; `textures` = the ledger length; `budgets.regions[r].px` = the
  region sums.
- **`elements`** (R14) = `{budget: {p1: 7000, p3: 8000}, visible_rest: {p1, p3}, per_region: {region: {p1, p3}},
  per_part?, densest}`. Zeros only in the stub; the real manifest fails with a 0 count.
- `budgets.parts` = the part count, `part_cap` 56, `hand_models` = Σ variants.

### 0.4.9 Rig API (`functions`; plan R22; all `rlk:mboss/apep/rig/…`, @s = the anchor, at it)

| key | function(s) |
|---|---|
| `init`, `spawn`, `tick`, `kill`, `uninstall`, `look_apply` | as Azhdaha R1 (`look_apply` re-applies every channel from the objectives) |
| `play` | `play/<clip>` for every clip (36) |
| `face` | `face/player`, `face/track` (≤ 2°/call), `face/set {yaw}` |
| `state` | `state/normal`, `state/burrowed` (visibility) |
| `flash` | `flash/<head|body|front|rear|tail|arms>` (3-t outline of one group; the framework's last hit proxy → its `flash`) |
| `park`, `unpark` | `park`, `unpark` (§0.4.7) |
| `stance` | `stance/crouch`, `stance/upright` (snap to the rest pose of a stance; outside clips) |
| `hands` / `hand` | `hands/<set>` / `hand/<part>/<variant>` |
| `look` | `look/<channel>/<look>` for `form face core core_glow tint` |
| `bright` | `bright/13`, `bright/15` |

The rig owns no proxy runtime (`px/*` is the framework's, cm.md §9.3), never moves or turns the anchor, and reads no
module score except its own `apRig*`. Anchors / hidden spans / yaw schedules / px tracks / capsules are data (this
manifest), read by `api.py` and the framework.

### 0.4.10 The binding clip table (from `stub_rig_manifest.json`)

Plan §6.3 converted to manifest v1 (events numbered, hidden inclusive, the px sets of §0.4.6). **Binding from D0**: the
names, `len`, `authored`, loop / next, `events` and `hidden` below (`validate.py --against`), the yaw knots of §0.4.5,
the anchors of §0.4.5. AP-RC1 / RC2 may add keys, events with new names by request, and `dbg_*` clips; they never change
these values without a change note.

| id | clip | form | len / authored | loop / next | hidden (incl.) | px sets | events (played) |
|---|---|---|---|---|---|---|---|
| 0 | `entrance_p1` | p1 | 110 | idle_p1 | [0,3] | inv → p1 110 | pool 0 hood 16 reach 31 touch 47 flash 60 embers 63 heart_up 70 crouch 91 roar 100 end 110 |
| 1 | `idle_p1` | p1 | 60 | loop | — | p1 | — |
| 2 | `turn_p1` | p1 | 20 | loop | — | p1 | step_1 0 step_2 5 step_3 10 step_4 15 |
| 3 | `turn_p1_step` | p1 | 10 | idle_p1 | — | p1 | step_1 0 step_2 5 |
| 4 | `crawl_p1` | p1 | 16 | loop | — | p1 | stepA 0 stepB 8 |
| 5 | `crawl_stop_p1` | p1 | 32 | idle_p1 | — | p1 | plant 8 open 16 end 32 |
| 6 | `walk_p1` | p1 | 36 | loop | — | p1 | step_1 0 step_2 9 step_3 18 step_4 27 |
| 7 | `burrow_strike` | p1 | 82 / 94 | idle_p1 | [22,43] | p1 → burrowed 6 → p1 44 | tell 0 dive 4 inv 6 sink 8 hide 22 travel 23 lock 32 burst 44 rise 49 loom 52 yawlock 52 sweep 64 sweep_end 71 land 77 end 82 |
| 8 | `sink_p1` | p1 | 17 / 18 | hold | [14,16] | p1 → burrowed 4 | tell 0 sink 4 chunks 8 hide 14 |
| 9 | `emerge_on_p1` | p1 | 24 | rotation | [0,0] | burrowed → p1 4 | show 1 solid 4 settle 12 end 24 |
| 10 | `burrow_in_p1` | p1 | 23 / 30 | hold | [21,22] | p1 → burrowed 5 | tell 0 inv 5 dive 5 sink 6 hide 21 |
| 11 | `emerge_crown_p1` | p1 | 40 | idle_p1 | [0,4] | burrowed → p1 11 | glow 0 crown 5 hood 10 targetable 11 out 21 end 40 |
| 12 | `hands` | p1 | 140 / 160 | idle_p1 | — | p1 | spread 0 swirl 5 raise 27 plunge 30 lock 33 legs 36 lines 40 slam1 62 slam2 69 slam3 75 slam4 82 sink 83 stand 100 pull 108 flower 118 fold 128 end 140 |
| 13 | `glow_slams` | p1 | 131 / 160 | idle_p1 | — | p1 | wind 0 coil 23 column 36 slam1 47 rear2 65 slam2 70 leap 77 apex 83 dive 90 slam3 101 settle 121 end 131 |
| 14 | `rotation` | p1 | 130 / 135 | idle_p1 | — | p1 | arms 0 rear 10 disc 16 swing 32 spin 34 full 40 crash 40 flash 52 spin_end 64 rise 85 stand 100 end 130 (fix 10-22f; was full 39 spin 47 flash 57 spin_end 71) |
| 15 | `tail_p1x2` | p1 | 127 / 141 | idle_p1 | — | p1 | turn 0 raise 8 cock 23 swing1 28 end1 37 cock2 48 swing2 52 end2 59 rise 86 end 127 |
| 16 | `combo_a` | p1 | 29 | hold | — | p1 | tell 0 swing 10 hit 14 |
| 17 | `combo_b` | p1 | 44 / 48 | hold | — | p1 | rear 0 high 12 slam 17 |
| 18 | `combo_c` | p1 | 20 | hold | — | p1 | twist 0 spin 5 hit 10 |
| 19 | `combo_d` | p1 | 77 / 84 | hold | — | p1 | rear 0 tall 20 lunge 22 slam 27 recover 43 |
| 20 | `combo_end` | p1 | 20 | idle_p1 | — | p1 | — |
| 21 | `sink_revive` | p1 | 60 | hold | [45,59] | p1 → burrowed 6 → parked 46 | stagger 0 flicker 4 sink 20 chunks 30 hide 45 park 46 end 60 |
| 22 | `revival` | p3 | 160 | idle_p3 | [0,59] | inv → p3u 118 | burst 60 splash 60 reach 88 flash2 96 reveal 100 end 160 |
| 23 | `idle_p3` | p3 | 60 | loop | — | p3u | — |
| 24 | `turn_p3` | p3 | 20 | loop | — | p3u | step_1 0 step_2 5 step_3 10 step_4 15 |
| 25 | `walk_p3` | p3 | 32 | loop | — | p3c | step_1 0 step_2 8 step_3 16 step_4 24 |
| 26 | `crouch_p3` | p3 | 8 | hold | — | p3u → p3c 6 | closed 6 end 8 |
| 27 | `stand_p3` | p3 | 14 | idle_p3 | — | p3c → p3u 10 | open 10 end 14 |
| 28 | `move_strike_p3` | p3 | 92 / 100 | idle_p3 | [16,41] | p3u → burrowed 8 → p3c 44 → p3u 85 | fold 0 mound 8 inv 8 hide 16 trail 16 lock 32 show 42 burst 44 hoop 44 roll 49 slam 61 tail 65 sweep 69 rise 71 stand 85 end 92 |
| 29 | `aftermath` | p3 | 224 / 240 | idle_p3 | — | p3c → aloft 84 → p3u 176 | charge 0 whirl 18 land 40 field 40 pillar1 44 pillar2 48 pillar3 52 dome1 54 dome2 58 dome3 62 rise 76 ticks 80 aloft 84 rain 134 blast 156 descend 162 window_end 176 pop 189 burst 190 end 224 |
| 30 | `shells` | p3 | 113 / 140 | idle_p3 | — | p3u | hunch 0 ring 10 lit 14 lock1 33 launch 35 ball 36 hit1 45 cool 48 lock2 79 lock3 82 hit2 93 hit3 96 end 113 |
| 31 | `sink_p3` | p3 | 20 | hold | [12,19] | p3u → burrowed 8 | fold 0 inv 8 sink 8 hide 12 end 20 |
| 32 | `surface_p3` | p3 | 40 | stand_p3 | — | burrowed → p3c 0 | show 0 splash 0 charge 0 launch 10 hit 12 recover 12 end 40 |
| 33 | `tail_p3` | p3 | 87 / 100 | idle_p3 | — | p3c → p3u 57 | crouch 0 cock 3 swing1 14 rise 24 coil 36 lunge 36 swing2 46 rise2 57 end 87 |
| 34 | `spikes` | p3 | 72 / 84 | idle_p3 | — | p3u | curl 4 rise 10 column 14 summon 19 lockA 37 fireA 42 lockB 43 fireB 48 hitA 49 blades 52 hitB 55 skim 64 recover 65 end 72 |
| 35 | `death` | p3 | 120 | hold | [118,119] | dead | hit 0 flicker 8 droop 30 kneel 55 fall 70 land 82 wither 85 sink 100 gone 118 end 120 |

RETIME knots, stance moves, looks and hand events per clip are in the stub (from plan §6.3; e.g. `stand_p3`: face
`p3_idle` 4, B hands `p3_open` 5 (left) / 8 (right), stance UPRIGHT 13, px `p3u` 10). Notes on conversions:
`turn_p1_step` keeps `step_1 0`, `step_2 5` (the plan's "step 0/5/10/15" fits only twice in 10 t); `surface_p3`'s plan
span `[0,0]` is empty (visible from tick 0); combos hold their last pose (the module chains `combo_a → b → c → d`, then
`combo_end` unless the last is `d`).

---------------------------------------------------------------------------------------------------

## 0.5 Org manifest schema (`S:ap/spec/org_manifest.schema.json`)

New (Azhdaha has no organisms); written in the conventions of manifest v1 (top-level `schema` / `boss` / `source` /
`runtime`, events `{name: one played tick}` with numbered repeats, `0 ≤ t ≤ len`, `next` null = hold, unique clip ids).

### 0.5.1 Files and top level

| file | writer | `source` |
|---|---|---|
| `T:mboss_apep_org_manifest.json` | `T:build_mboss_apep_org.mjs` (AP-ORG1 / ORG2) | `"org"` |
| `T:mboss_apep/stub_org_manifest.json` | AP-CORE's `stub_org.py`, byte-identical to `S:ap/spec/stub_org_manifest.json` | `"stub"` (dropped at AP-I1) |

| key | content |
|---|---|
| `schema` 1, `boss` `"apep"`, `source`, `manifest` `"org"` | |
| `runtime` | `{ns: "rlk:mboss/apep/om/", kind_obj: "apK", clip_obj: "apOI", tick_obj: "apOC"}` |
| `uuids` | `{block: "524c4b4d-4150-4800-8000-0000000000", ints: [1380731725, 1095780352, -2147483648]}` (fixed objects, §0.3.4) |
| `objectives` | `apK apS apT apOC apOI` required (+ `apL apShd apSock apTok`) |
| `passenger` | `{ride_y: 2.0, tag_prefix: "rlk_ap_om_", tags: ["rlk_room", "rlk_mb_aux"], face: "rotate", key}`: models ride the aux husk ≈ 2 b up and translate down to the feet; facing by `rotate` on the passengers (a `tp` would dismount them) |
| `spawn` | `{marker_ticks: 20, scale_in: {ticks: 4, from: 0.85}, untargetable_until: "solid"}` (plan §5.1, §7.6.3) |
| `kinds` | §0.5.2 (all six required) |
| `objects` | §0.5.3 (`heart dome wall stalk seed` required) |
| `budgets` | `{px_total: 200000, organism_elements: 500, heart_elements: 800, px}` (plan §5.4) |

### 0.5.2 Kinds and displays

Kind record: `id` (= `apK`), `name` (Korean), `tag` (`rlk_mb_ap_<key>`), `size` (blocks, free form), `hover_y` (the
model's height above the husk feet while flying), `hp_bar_y` (the HP-bar y offset, blocks; FN-29 `#auxHbY` takes tenths),
`shield {w, h}` (the click shield, blocks; FN-29 `#auxShW` / `#auxShH`), `displays`, `clips`, `budget {elements, px}`,
`elements`, `px`.

| key | apK | 한국어 | displays (looks) | HP bar / shield | budget |
|---|---|---|---|---|---|
| `basic` | 1 | 기본 | `bulb` (bell, bag, buffed, bag_buffed, dying), `crown` (closed, open), `shield` overlay (on) | +1.6 / 1.2 × 1.6 | 350 el, 12 k px |
| `nurt` | 2 | 양육 | `stalk`, `cap` (idle, tilt), `orb` (15), `ring` overlay (the immune cylinder) | +2.8 / 1.4 × 2.6 | 450, 16 k |
| `guard` | 3 | 수호 | `spire` (spire, bud, wisp; mid pivot), `orb` (15) | +3.0 / 1.4 × 3.0 | 450, 16 k |
| `nest` | 4 | 둥지 | `cap`, `wing_l`, `wing_r`; hover 1.0 | +2.2 / 1.6 × 2.2 | 400, 12 k |
| `destr` | 5 | 파괴 | `shell` (normal, husk), `face` (15) | +1.6 / 1.3 × 1.3 | 300, 8 k |
| `pred` | 6 | 포식성 | `body` (fish, fish_flare, bud, pod, face), `jaw`, `fin`, `core` (15); hover 1.2 | +2.2 / 1.6 × 1.6 | 500, 20 k |

Display record: `name` (unique per kind), `tag` (`rlk_ap_om_<name>`), `model` (= `looks[default_look]`), `looks {look:
model}`, `default_look`, `brightness` (14; cores 15), `scale`, `pivot` (`feet` | `mid` | `centre`), `offset [x, y, z]`
(the translation from the passenger point: −2 + the pivot height), `overlay` (true = only present in some states). Looks
are model swaps (`item_model`); forms such as the basic's bell / bag are looks of one display. `bag_buffed` is AP-SPEC's
addition (a buffed ranged basic lies as a bag).

### 0.5.3 Objects

| object | kind | displays (idx) | extra keys |
|---|---|---|---|
| `heart` | `single` (tag `rlk_mb_ap_heart` = the marker) | `heart_bulb` 0x00 (idle, egg_gold, egg_green, withered, blaze; br 15), `heart_cradle` 0x01 (pedestal, full; mid, ≤ 2.2), `heart_arms` 0x02, `heart_tips` 0x03 (15), `vine_hand` 0x04 (idle, wrap), `vine_stem_0..3` 0x05-0x08 | `marker {tags, not}`, `egg {scale: 0.7, pitch: 0, land_ticks: 6}`, **`footprint`** |
| `dome` | `fixed_set`, `count` 3, `radius` 4.5 | `dome_shell` [0x10, 0x12, 0x14] (two-sided, alpha ≤ 0.35), `dome_decor` [0x11, 0x13, 0x15] (cutout) | |
| `wall` | `multi`, `max` 15 | `wall_blade` | `blocks {block: "minecraft:barrier", y: [201, 202], place: "replace air"}` |
| `stalk` | `fixed_set`, `count` 4, `height` [5.5, 6.0] | `stalk_low` [0x20, 0x23, 0x26, 0x29], `stalk_high` [0x21, …], `stalk_tip` [0x22, …] | |
| `seed` | `single` | `seed` 0x30 (15) | |

Fixed display record: `name`, `idx` (single) or `idxs` (one per instance), `uuid` (= block + idx, single only), `tag`
(`rlk_mb_ap_<name>`), `model`, `looks`, `default_look`, `brightness`, `scale`, `pivot`.

**Heart footprint** (`objects.heart.footprint`; read by `revival.py` / `org.py`, never typed by hand):

| key | value | rule |
|---|---|---|
| `centre` | the theme's `POINTS['heart']` (= the arena centre) | |
| `bulb_box` | `{l: 3.2, w: 2.6, h: 2.3, centre_y: 1.6, yaw: 0}` | the lying lemon, blocks above the floor |
| `root_radius` | 2.5 | |
| `sockets` | `[{id: 0, bearing: 0, r: 3.4}, {id: 1, bearing: 120, r: 3.4}, {id: 2, bearing: 240, r: 3.4}]` | the 3 melee sockets (`apSock`) |
| `wait_ring` | 4.5 | basics without an attack slot wait here |
| `destr_stop` | `{r: 2.6, bearings: [60, 180, 300]}` | off the socket bearings |
| `wall_exclusion` | 4.6 | no barrier block inside |
| `bolt_end` | `{r: 1.5, from: "bulb_box"}` | a ranged bolt ends (= a Heart hit) within 1.5 b of the bulb box |
| `swirl_r`, `hang` | 3.5; `{entrance_y: 9.0, canopy_y: 20.0, lowered_y: 3.0}` | the gold swirl decal; the vine-hand heights above the floor |

Order rule (validator): `root_radius < socket r < wait_ring ≤ wall_exclusion`, `destr_stop.r < socket r`. **Bearings**
are compass bearings around the centre, the `az_cavern` convention (0 = north −z, 90 = east +x, 180 = south +z = the
arrival, clockwise seen from above): point = (cx + r sin b, cz − r cos b); yaws stay Minecraft's (0 faces +z). Socket 0
is north of the Heart (away from the arrival), the 파괴 stop at 180° is on the arrival side.

### 0.5.4 Clips and the runtime

Clip record `{id, name, len, loop, next, events, displays?, note?}`; ids unique over the whole file (`apOI`); `next`
names a clip of the same owner. The org generator writes `AP:om/<owner>/c/<clip>/k/<t>` (key functions running `execute
on passengers if entity @s[tag=rlk_ap_om_<display>] run data merge …` as the husk) and a per-owner dispatch on `apOI` /
`apOC`; fixed objects animate by UUID. Organism clocks run in the module tick (`org/tick` → the kind's state machine on
`apS` / `apT`); a clip is started by setting `apOI` / `apOC 0`.

### 0.5.5 The binding org clip table (from `stub_org_manifest.json`; plan §5.1-§5.3)

| owner (apK) | clip (id): len, loop / next, events |
|---|---|
| basic (1) | `org_spawn` (0): 20, → basic_bob · `basic_bob` (1): 24, loop · `basic_melee` (2): 14, → basic_bob; hit 10 · `basic_lie` (3): 10, hold; bag 10 · `basic_ranged` (4): 20, hold; open 0 fire 12 · `org_die` (5): 10, hold; gone 10 |
| nurt (2) | `nurt_idle` (6): 40, loop · `nurt_buff` (7): 20, → nurt_idle; tilt 0 tethers 8 · `nurt_die` (8): 17, hold; gone 17 |
| guard (3) | `guard_idle` (9): 60, loop · `guard_cast` (10): 30, → guard_idle; collapse 0 bud 7 regrow 16 regrow_end 24 shields 30 · `guard_die` (11): 17, hold; gone 17 |
| nest (4) | `nest_fly` (12): 14, loop · `nest_cast` (13): 12, → nest_fly; walls 12 · `nest_blink` (14): 6, → nest_fly; out 0 in 3 · `org_die` (15): 12, hold; gone 12 |
| destr (5) | `destr_roll` (16): 32, loop · `destr_fuse` (17): 56, → destr_suck; pulse_1 0 pulse_2 9 pulse_3 18 pulse_4 27 pulse_5 36 fast 36 · `destr_suck` (18): 5, → destr_blast · `destr_blast` (19): 1, hold; blast 1 · `org_die` (20): 10, hold; gone 10 |
| pred (6) | `pred_swim` (21): 16, loop · `pred_swallow` (22): 24, → pred_bud; eat 12 bud 14 · `pred_bud` (23): 20, loop · `pred_inflate` (24): 10, → pred_burst · `pred_burst` (25): 10, → pred_swim; hit 0 fish 2 · `pred_bite` (26): 6, → pred_swim; open 0 hit 4 · `pred_bite_chain` (27): 38, → pred_swim; hit_1 4 hit_2 10 hit_3 16 hit_4 22 · `org_die` (28): 12, hold; gone 12 |
| heart | `heart_hang` (29): 80, loop · `heart_up` (30): 30, → heart_hang · `heart_lower` (31): 50, hold · `heart_drop` (32): 30, → heart_idle; land 6 beam 6 beam_end 16 · `heart_idle` (33): 40, loop · `heart_hit` (34): 6, → heart_idle · `heart_gain` (35): 8, → heart_idle · `heart_wither` (36): 30, hold · `heart_blaze` (37): 24, hold · `heart_lift` (38): 46, hold · `cradle_rise` (39): 20, hold · `cradle_sink` (40): 10, hold |
| dome | `dome_rise` (41): 10, → dome_idle · `dome_idle` (42): 40, loop · `dome_pop` (43): 6, hold |
| wall | `wall_rise` (44): 5, hold · `wall_fade` (45): 8, hold |
| stalk | `leg_rise` (46): 10, hold · `leg_slam` (47): 6, hold; hit 4 · `leg_sink` (48): 10, hold |
| seed | — |

Binding from D0: names, lengths, loop / next, events (`validate.py org … --against`). The `next` chains are AP-SPEC's
reading of plan §5 / §7.6 (spawn and attacks fall back to the kind's loop; the 파괴 fuse 56 + suck 5 = blast at contact
+ 61, §8.2 O7). The 포식성 bite chain clip's hits at 4 / 10 / 16 / 22 are the 6-t spacing of §8.2 O6b; the module starts
it 8 t before the first sector strike.

---------------------------------------------------------------------------------------------------

## 0.6 Theme interface (FN-3): `T:mboss_arena_ap_oasis.py`

The **theme.md interface unchanged** (§2 names, §3 emission by the chapter-mode generator, §4 the `props()` record, §5
`entrance_layout()`), filled with plan §4. AP-ARENA owns the file (and `S:ap/arenarender/**`,
`S:ap/tests_arena/test_ap_arena.py`); the framework's arena generator and room generator import it; nothing else.

### 0.6.1 Names

| name | required | Apep value / rule |
|---|---|---|
| `THEME`, `AID` | yes | `'ap_oasis'`, `'ap_oasis'` |
| `SENTINEL` | yes | `((440, 193, 8), 'minecraft:packed_mud')`: a block of the solid fill under the centre, **identical in both looks** (AP-ARENA may change the block type, not the position, with a commit note) |
| `POINTS` | yes | §0.6.3 |
| `arena_layout(look=None)` | yes | every non-air block of the box for `look` (`None` = `'withered'`), block strings with states; importable for offline top / iso renders of both looks (§4.2) |
| `slices()` | yes | build slices: inclusive boxes, pairwise disjoint, union = the registry box exactly, each ≤ 32 768 blocks, ≤ 40 (suggested: 16 y-slabs of 4 layers, 89 × 89 × 4 = 31 684 blocks, the last one 1 layer) |
| `props(look=None)` | yes | §0.6.6 |
| `entrance_layout()` | yes | §0.6.7 |
| `look_lines(look)` | **yes for Apep** (optional in theme.md) | §0.6.5 |
| `CHECK` | yes for Apep | `{'cx': 440, 'cy': 201, 'cz': 8, 'r': 29, 'walk': 26, 'safe': 24, 'box': dict(BOX), 'start': dict(START)}` (the registry's own shapes, as `az_cavern`): the generator asserts equality with the registry |
| `render_hints()` | optional | camera presets |

Plain Python 3, stdlib only (may import `mboss_lib` for `num`), deterministic (seeded noise), no side effects on import,
never writes files (theme.md §1).

### 0.6.2 Constants (module-level, importable)

| constant | value | plan |
|---|---|---|
| `CX`, `CY`, `CZ` | 440, 201, 8 (a block corner; floor blocks at y 200, stand height 201) | §4.1 |
| `BOX`, `START` | `{'x0': 396, 'y0': 190, 'z0': -36, 'x1': 484, 'y1': 250, 'z1': 52}`, `{'x': 440.5, 'y': 201.0, 'z': 24.5, 'yaw': 180.0, 'pitch': 0.0}` | §4.1, §3.7 |
| `RAD`, `WALK`, `SAFE` | 29, 26, 24 (`az_cavern` names) | §3.7 |
| `LOOKS` | `['withered', 'lush']` (`[0]` = the default restored by `ensure`) | §4.2 |
| `GEOMETRY` | `'day1'` / `'full'` (as `az_cavern`; §0.6.9) | |
| `FLOOR_Y`, `SOLID_Y0` | 200, 192: **full opaque blocks only, solid y 192..200 inside r 26** (the root sinks to y 195, hidden parts to ≈ y 193); no mud, slabs, carpets, glass, leaves, water or supported decor inside the disc | §4.1, R9 |
| `RIM` | `(26, 29)`: the root / rock bank (`leaf_litter`, dry grass, dead bushes only here, on supporting blocks) | §4.1 |
| `BARRIER` | `{'r0': 27, 'r1': 28, 'y0': 201, 'y1': 215}`: the invisible rim wall, never touched by a sweep (`arena/ap_oasis/sweep` covers r ≤ 25.5, y 201..202 only) | §4.1, FN-26 |
| `CLEAR_Y` | `(201, 224)`: inside r 26 only air and the `light` layer (the Q2 hover reaches ≈ y 215, culling height 16) | R6 |
| `CANOPY_Y` | `(225, 250)`; `SHAFT_R` 8 (open over the centre) | §4.1 |
| `LIGHT_Y`, `LIGHT` | 206, `{'withered': 12, 'lush': 14}` (`minecraft:light[level=N]` over the disc) | §4.1 |
| `WATER_Y`, `DECAL_Y_MIN` | 201.005 (the lush water sheet), 201.035 (kit decals at or above) | §4.1 |
| `MAX_LOOK_SLICES`, `SLICE_MS` | 24, 20 (ms target per slice on a server) | §4.2 |

### 0.6.3 `POINTS` (absolute world coordinates; compass bearings as §0.5.3; helper names as `az_cavern`: `cell_polar`, `polar_point`, `yaw_facing`)

| key | value | read by |
|---|---|---|
| `spawn` | `(440.0, 201.0, 8.0, 0.0)` (the anchor; yaw 0 faces south, toward the arrival) | `AP:spawn` |
| `centre`, `heart` | `(440.0, 201.0, 8.0)` | the Heart marker, the cradle, the Q2 walk target, the CS |
| `arrival` | `(440.5, 201.0, 24.5, 180.0)` (= registry `start`; r 16) | renders, checks |
| `org_spawn` | 8 × `(x, 201.0, z)` on r 12 at compass bearings 22.5° + 45°k (k = 0..7): (444.59, −3.09), (451.09, 3.41), (451.09, 12.59), (444.59, 19.09), (435.41, 19.09), (428.91, 12.59), (428.91, 3.41), (435.41, −3.09) | `revival.py` (§7.6.3) |
| `nurt_spawn` | 8 × r 7, same bearings: (442.68, 1.53), (446.47, 5.32), (446.47, 10.68), (442.68, 14.47), (437.32, 14.47), (433.53, 10.68), (433.53, 5.32), (437.32, 1.53) | `revival.py` (양육 points) |
| `ember_twig` | `(432.6, 203.5, −19.6)` (a bank twig at r ≈ 28.6, just outside the barrier ring, compass 345°, in the arriving player's view behind the boss; AP-ARENA may move it ≤ 3 b with a note, never into the barrier cells) | CS t64 `p/ember_arc` |
| `water_tiles` | 16 × `(x, 201.005, z)`, z-major as `az_cavern` (for z in −13, 1, 15, 29: for x in 419, 433, 447, 461): 14 b tiles covering r ≤ 26 | `props('lush')` |
| `pond_props` | lily pads / bell flowers / bulb flowers beyond r 22 (AP-ARENA, ≤ 48) | `props('lush')` |
| `bank_crystals` | gold crystal spikes on the bank r 26-29 (AP-ARENA, ≤ 16) | `props()` (both looks) |
| `trees` | 8-10 × `(x, z, r)` trunk centres at r 30-38 | renders |
| `motes` | ≤ 12 ambient points (optional) | the kit haze presets |

### 0.6.4 Layout rules (checked by `test_ap_arena.py`)

Plan §4.1 table, verbatim as rules: the walk disc (cell centre distance ≤ 26) **full opaque blocks** from y 192 to y 200
(floor top 201) — moss-green cells 2-4 b of `moss_block` split by `packed_mud` / `rooted_dirt` / `dark_oak_wood` veins
flush in the floor, `pale_moss_block` only at r 24-26; the floor **identical in both looks**; the bank, the barrier
wall, the giant trees r 30-38 (`jungle_log`, `mangrove_log`, `pale_oak_log`, `mangrove_roots` buttresses arching over
the rim only above y 207), shelf mushrooms and froglight bulbs at their feet; the canopy y 225-250 with the sky shaft
r ≤ 8; no biome-tinted leaves; **leaves always `persistent=true`** (a `fill` of non-persistent leaves decays); no real
water inside the disc; the `light` layer at y 206. Every block key inside the box; nothing outside it; no markers,
entities, scores or forceloads from the theme (theme.md §3.4).

### 0.6.5 `look_lines(look)` (the look swap, FN-3)

- Returns `[[str]]`: one inner list = one tick (slice); **≤ 24 slices**, each ≤ 8 000 commands and every `fill` ≤ 32 768
  blocks; the commands turn **any** built look into `look` (idempotent `fill x0 y0 z0 x1 y1 z1 <new> replace <old>`
  boxes: canopy leaf and glass types, bank decor, the light level). The floor never changes. AP-ARENA checks with
  `lint_mc` whether `replace <filter> strict` parses on the pack's format 121; plain `replace` otherwise (the swapped
  blocks are full blocks or persistent leaves, so neighbour updates do nothing).
- Emitted by the chapter-mode arena generator as `F:mboss/arena/ap_oasis/look/<look>` + `l/<look>/<i>` (theme.md §3.3);
  the job's last slice stamps `built_ap_oasis = "ap_oasis@<ver>:<look>"`; `ensure` (from `prep`) restores `withered`;
  `cb/start` waits for a running job (gate "준비 중", cm.md §5.4-§5.5).
- The module runs `function rlk:mboss/arena/ap_oasis/look/lush` at CS t24 (inside the 40-t white-out): ≤ 24 slices end
  by t48 < t64. A reload mid-CS jumps to "phase 3 ready" and calls it again (idempotent).
- `S:ap/arenarender/` measures each slice's command count and, once on a server, its ms (target ≤ 20 ms).

### 0.6.6 `props(look)` (per-fight display props)

- Records exactly as theme.md §4.1: `{'name', 'kind', 'group', 'pos', 'yaw', 'pitch', 'scale', 'el', 'uuid'}` with
  `kind` ∈ the kit props `water_sheet`, `lily_pad`, `bell_flower`, `bulb_flower`, `bank_crystal` (`ap_fx_api.md` §0.7),
  `group` ∈ `water`, `pond`, `crystal`, `el` = **7** (an int: one fixed Dendro look; theme.md's `'fight'` is for
  Azhdaha's runtime element), `uuid` = the low byte in the **Apep arena-prop block** (§0.3.4: water `0x00-0x0F`, pond
  `0x10-0x3F`, crystals `0x40-0x5F`).
- `props('withered')` = the bank crystals; `props('lush')` = the crystals + 16 `water_sheet` tiles (scale 14, pitch 0,
  at `POINTS['water_tiles']`) + the pond props. A record present in both looks has the same `name`, `uuid`, `kind`,
  `pos`, and is **kept across the swap**: the module's look switch kills the props of the old look that the new look
  lacks (by UUID) and spawns the new look's missing ones.
- The module spawns them as `item_display` entities with `fx/prop/<kind>` (the kit sets model, tint, brightness),
  tags `rlk_mb_arena_prop rlk_mb_ar_ap_oasis rlk_mb_ap_ar_<group>` (**no `rlk_room`, no `rlk_mb_aux`**), UUID from the
  record: the withered set at fight start (≥ 40 t after the forceload, "none alive" guard), the lush set in the CS
  white-out; re-made by its `reload` from the current look (the stamp); killed by cleanup (the framework kills
  `rlk_mb_arena_prop`; the module's `cleanup` / `uninstall` also kill `@e[tag=rlk_mb_ar_ap_oasis]`). Entity budget:
  ≤ 80 props (the arena count gate ≤ 400, FN-27).
- `test_ap_arena.py` checks every `kind` against `T:mboss_ap_fx_manifest.json` `props` (skipped with a warning before
  AP-I1 when the kit manifest is absent), unique names / UUIDs, the water tiles covering r ≤ 26 at y 201.005.

### 0.6.7 `entrance_layout()` (the chapter-3 domain entrance)

- Exactly the theme.md §5 dict `{'cur', 'blocks', 'clear', 'gate', 'glyphs', 'stele_glow'}` (the same key set as
  `az_cavern`, so the room generator and its checks need nothing new). Apep has no rolled elements, so **`glyphs` holds
  the prop spots of the gold-green gate crystals**: `{'crystal_w': (-3.5, 201.0, 12.5, 0.0), 'crystal_e': (3.5, 201.0,
  12.5, 0.0)}` (x, y, z, yaw; the module's `prep` summons them as `rlk_room` entities with `fx/prop/gate_crystal`, as
  Azhdaha's `prep` does its glyph props); `stele_glow` = the particle point of the crystal glow (e.g. (0.0, 203.5,
  12.5)).
- `cur`: exactly the key sets and value conventions of `F:room/raiden/layout` (theme.md §5); zone 1 = kind 0 (the
  player's spawn), zone 2 = **kind 9** with the gate; one door. Recommended geometry = theme.md's: zone 1 x −6..5,
  z 24..39 (spawn (0, 33) yaw 180), the door x −2..1, z 23..24, zone 2 x −10..9, z 4..23 (cx 0, cz 14, cy 201), the gate
  at (0, 201, 14), crystals at (±3.5, 201, 12.5) facing south. Everything inside x / z −64..63, y 199..230. AP-ARENA may
  start from S1-ARENA's `az_cavern` `entrance_layout()` (`wip/az-arena` c8000fa: `FOYER`, `HALL`, `GATE`, `DOOR`,
  `_cell`, `_zone`) and change only the blocks and the spots.
- Blocks (plan §3.8, §4.3): a sandstone / mud-brick oasis gate (`cut_sandstone`, `mud_bricks`, `smooth_sandstone`),
  moss and rooted-dirt accents. The generator (`build_cboss_rooms.py`) adds `boss_id:"apep"`, `cboss:1b`, `fn:"cboss_apep"`
  to every zone and writes `F:room/cboss/apep/{layout,build}`.
- Gate (written by `AP:prep` into `cprep.apep.gate`, cm.md §3.3): `item` / `model` = the registry icon
  `minecraft:pitcher_plant`; `item2` = `minecraft:emerald`, `model2` = `rlk:mboss/ap_kit/gate_crystal`; `l1` "아펩의
  오아시스 파수꾼" (`#C9C452`, bold), `l2` "내성: 풀 30% · 그 외 10%", `l3` "챕터 3 보스"; `title` / `sub` = the registry
  name / sub.

### 0.6.8 Tests and renders (AP-ARENA)

`S:ap/tests_arena/test_ap_arena.py` (no game): every §0.6.4 rule on `arena_layout()` of both looks; `slices()` disjoint,
covering the box, ≤ 32 768 each, ≤ 40; the reference emitter (theme.md §3) ≤ 8 000 commands per slice; `look_lines`
≤ 24 slices, every fill ≤ 32 768, applying it to either look's layout gives the target layout exactly (both directions),
the floor and `SENTINEL` unchanged; the rim barrier never inside the sweep span; `CHECK` = the registry entry; `POINTS`
keys present and inside the walk disc where they must be; `props()` per look (§0.6.6); `entrance_layout()` key sets,
zone / cell / door conventions, bounds, `gate` = zone 2 centre; determinism (two imports, equal layouts). Renders: top
/ iso of both looks and the entrance into `S:ap/arenarender/**`.

### 0.6.9 Day-1 version

AP-ARENA's first commit has the full interface with simple geometry (flat `moss_block` floor y 200 over solid
`packed_mud` y 192..199 inside r 26, a `mossy_cobblestone` bank 26-29, the barrier wall, the light layer, a flat canopy
of `pale_oak_leaves[persistent=true]` ↔ `azalea_leaves[persistent=true]` at y 230 outside the shaft as the look diff),
every `POINTS` key, `SENTINEL`, `slices()`, `look_lines()`, `props()`, `entrance_layout()`; later commits change only
blocks (names, points and props keep their keys).

---------------------------------------------------------------------------------------------------

## 0.7 Kit call list (`S:ap/ap_fx_api.md` §0)

The frozen kit names and macro arguments for every preset / telegraph / prop / sound / HUD element plan §8 uses are in
`ap_fx_api.md` §0 (§0.4 telegraphs, §0.5 the dressing pool, §0.6 presets, §0.7 props, §0.8 sound recipes, §0.9 HUD,
§0.10 the Python API `K.*`, §0.11 the per-pattern call index, §0.12 the hook lines, §0.13 the differences from the fg and
Azhdaha kits). Summary of what module authors rely on:

- Executor = the event point (floor y 201) rotated as the aim; macro sizes in tenths, `K.*` builders take blocks.
- Every damaging decal is called in the same tick as its hazard with the same size and `tell` (`#hzQuiet 1`, `#hzSfx
  0`); no ground decal is larger than its hazard (plan §7.11 rule 1).
- `el` 7 (Dendro, default), 20 gold (phase-1 telegraphs), 22 target, 23 olive (the P4 disc), 24 field (Q2); `nd` 0 on
  every §8 decal.
- Swept sweeps: one `tele/wedge` per swept tick, stacked by the host from `api.wedges()` (the same data as the
  `hz/sector` wedges).
- Hooks (wired at AP-I1): `uninstall` → `fx/uninstall`; `cleanup` → `fx/clear` + `fx/hud/clear` + `fx/dress/clear`;
  `pause` → `fx/tele/clear` + `fx/hud/flash_end` + `fx/hud/banner_end`; phase-2 `reload` → `fx/dress/redraw`;
  `death_start` → `fx/tele/clear` + `fx/hud/clear`.
- Until AP-I1 `api.K` is a no-op set with the same signatures.

---------------------------------------------------------------------------------------------------

## 0.8 Pattern ids, keys and test ids (plan §12.2)

Pattern ids are the `test/pattern {id}` ids wherever plan §12.2 has one (s2.md §12: "your pattern id runs your pattern
now"); keys name `AP:p/<key>/**`. Binding from D0 (AP-CORE builds the `api.Pattern` records from this table).

| id | key | plan | kind | clip(s) | module (owner) |
|---|---|---|---|---|---|
| 1 | `burrow` | P1 잠복 돌진 | normal | `burrow_strike` | `p1.py` (AP-P1) |
| 2 | `hands` | P2 생명의 손 | normal | `hands` (+ org stalks) | `p1.py` |
| 3 | `glow` | P3 발광하는 파수꾼 | normal | `burrow_in_p1` → `emerge_crown_p1` → `glow_slams` | `p1.py` |
| 4 | `wither` | P4 초목이 시든 풍경 | normal | `rotation` (opener R when the player is > 9 b away) | `p1.py` |
| 5 | `tail` | P5 생명의 꼬리 (two swings) | normal | `tail_p1x2` | `p1.py` |
| 6 | `combo` | P6 근접 콤보 (2-4 hits) | normal | `combo_a` … `combo_d`, `combo_end` | `p1.py` |
| 7 | `reloc` | R burrow-relocate | opener of 4 | `sink_p1` → `emerge_on_p1` | `p1.py` |
| 10 | `move` | M crawl / walk / step-turn | service (ai.py picks it) | `crawl_p1`, `crawl_stop_p1`, `walk_p1`, `turn_p1`, `turn_p1_step` | `p1.py` (sounds, steps); AP-CORE decides |
| 31 | `mstrike` | Q1 이동 돌진 | normal | `move_strike_p3` | `p3.py` (AP-P3) |
| 32 | `aftermath` | Q2 종말의 여파 | scheduled | (`crouch_p3` + `walk_p3` approach) `aftermath` | `aftermath.py` (AP-P3) |
| 33 | `shells` | Q3 증폭의 풀 | normal | `shells` | `p3.py` |
| 34 | `tail3` | Q4 생명의 꼬리 (phase 3) | normal | (`crouch_p3` [+ `walk_p3`] opener) `tail_p3` | `p3.py` |
| 35 | `spiral` | Q5 생명의 나선 | normal | `spikes` | `p3.py` |
| 36 | `surface` | Q3s 수면 포격 | chain (30 % after 33) | `sink_p3` → `surface_p3` → `stand_p3` | `p3.py` |
| 20 | `t1` | T1 소생 단계 진입 | service | `sink_revive` (+ org `cradle_rise`, `heart_lower`, `heart_drop`) | `revival.py` (AP-REV) |
| 40 | `fail` | 「소생 실패」 | service | — (org `heart_wither`) | `revival.py` |
| 60 | `cs` | CS 2→3 | service | `revival` (+ org `heart_blaze`, `heart_lift`) | `revival.py` |
| 61 | `stance` | stance change | service | `crouch_p3` / `stand_p3` | AP-CORE |
| 50 | `entrance` | E | service | `entrance_p1` (+ org `heart_hang`, `heart_up`) | `seq.py` (AP-P1) |
| 51 | `death` | D | service | `death` | `seq.py` |

Organism attacks O1-O7 are `org.py` states, not patterns. Pattern-owned names: §0.3.2 / §0.3.3 (`#apq<id>`,
`ap.p<id>`, `rlk_mb_ap_p<id>`).

**Test ids** (`/function rlk:mboss/test/pattern {id:N}`, core-routed; `test/lock {id:N}` repeats a pattern):

| id | action | id | action |
|---|---|---|---|
| 1-6 | P1-P6 (6: rolled length; 5 = the double tail) | 8 | R + P4 |
| 9 | P6 with 4 hits | 20 | enter T1 → phase 2 |
| 21 / 22 | Heart +25 % / −25 % | 23 | spawn 4 basics |
| 24 / 25 / 26 / 27 / 28 | spawn one 수호 / 둥지 / 양육 / 포식성 / 파괴 | 29 | force the time-out |
| 30 | skip to phase 3 through the CS | 31-35 | Q1, Q2 (first, non-lethal cast), Q3, Q4, Q5 |
| 36 | Q3s | 37 | Q2 as a later (lethal) cast |
| 40 / 41 | failure strike 1 / 2 | 60 | the CS only |
| 61 | stance toggle (`crouch_p3` / `stand_p3`) | 99 | idle (Azhdaha's convention); any other id prints the help |

Framework commands (cm.md §5.9): `test/chapter {id:"apep"}` (= `test/chapter_ch {id:"apep",ch:3}`, L18), `test/kill`,
`test/abort`, `test/lock`, `test/level`, `test/stop`, `test/lose`. Phase-dependent ids (31-37, 61 in phase 1; 1-9 in
phase 3; 21-29, 40-41 outside phase 2) first jump to the phase they need, as the plan's suites expect (AP-CORE
documents the jump in its §1).

---------------------------------------------------------------------------------------------------

## 0.9 Stubs and validator (`S:ap/spec/`)

| file | content |
|---|---|
| `rig_manifest.schema.json`, `org_manifest.schema.json` | JSON Schema 2020-12 (§0.4, §0.5) |
| `make_stubs.py` | `python3 -I make_stubs.py` writes both stubs from plan §6.3 / §5 (deterministic: two runs, same bytes) |
| `stub_rig_manifest.json` | 36 clips, 49 parts, 11 proxies, 8 px sets, 3 capsules, 20 hand models, the planning sprite ledger (0.37 M px), zero element counts |
| `stub_org_manifest.json` | 6 kinds, 5 objects, 49 clips, the Heart footprint |
| `validate.py` | `python3 -I validate.py` (both stubs + the cross-name check), `validate.py rig FILE [--against FROZEN]`, `validate.py org FILE [--against FROZEN]`, `validate.py names RIG ORG`; exit 0 / 1 |

`validate.py` = schema (jsonschema when importable, else a built-in subset with the same verdicts on these schemas) +
the semantic rules: rig — UUID = block + idx, tags `rlk_mb_ap_<part>`, the bone tree and parents, proxies at
`0x41 + position` with known flash groups, every proxy in every px key and rest table, the eight px sets (`burrowed`,
`parked`, `inv`, `dead` without proxies), state / capsule / look / hand / objective cross-references, capsule boxes
(`f0 < f1`, matching `col`), the 36 clip names (extras only `dbg_*`), `play` for every clip, events in 0..len, RETIME
knots, required anchors, dense tracks and yaw, the binding yaw knots, hidden spans (top 0 and an `inv` set on every
hidden tick), stance / px-set / look / hand events, the sprite-ledger sums, element and atlas budgets (real manifests:
no zero counts, `planned: false`); org — kind ids 1..6, tags, display tags and default looks, the plan §5 clip names,
`next` within the owner, unique clip ids, fixed-object UUIDs and `idxs` counts, budgets, the footprint order and
bearings; names — rig tags never collide with org / module tags. `--against` compares names, lengths, authored, loop /
next, events and hidden spans with the frozen file.

Who runs it: AP-SPEC (now), AP-R1 / RC1 / RC2 (`rig T:mboss_apep_rig_manifest.json --against
S:ap/spec/stub_rig_manifest.json`), AP-ORG1 / ORG2 (`org … --against S:ap/spec/stub_org_manifest.json`), AP-CORE
(copies the stubs to `T:mboss_apep/`; `S:ap/tests/check_ap_manifest.py` = this script with the paths of the real
manifests, in `run_all.sh` from AP-I1).

---------------------------------------------------------------------------------------------------

## 0.10 Deliberate differences from Azhdaha, and plan names superseded by AZ-CM

**A. Plan text superseded by adopting the AZ-CM name** (cm.md §17.2; Apep's suites grep these names):

| # | plan said | adopted (AZ-CM) |
|---|---|---|
| A1 | arena prop tag `rlk_mb_ar_ap` (§3.6, §4.2) | `rlk_mb_ar_ap_oasis` (`rlk_mb_ar_<aid>`) |
| A2 | the current look in `rlk:mboss arena.ap_oasis.look` (§4.2) | read from the stamp `built_ap_oasis = "ap_oasis@<ver>:<look>"` |
| A3 | the module `incoming` calls `mboss/floor` (§7.2, FN-5) | the module only sets `#mbFloor`; the framework calls `mboss/floor` after `incoming` |
| A4 | `mv/local` → `#mvF` / `#mvS` in tenths (draft) | `#mbLf` / `#mbLs` in milliblocks |
| A5 | barrier safety sweep `sweep_barrier` (FN-26) | `arena/<aid>/sweep {y0,y1}`, run by `cb/won` / `cleanup` / `cb/remove` via the arena entry's `sweep` |
| A6 | px state calls `px/state/<name>` (FN-8) | the macro `px/state {set:"<name>"}`; the sets `inv` and `dead` are required |
| A7 | ‰ hazards `#hzPm` + `#hzLethal` (FN-15) | `#hzPm` + `#hzPmL` (lethal 0/1, default 1); reserved in AZ-CM, built on request |
| A8 | registry entry without `px` / `pxBase` / `shield` (§3.7) | `"px": true, "pxBase": 65, "shield": true` added |
| A9 | push ring "within 8 b → 12 b" | `push/ring {r:80,to:120,kb:…}` (tenths) |

**D. Deliberate differences** (Apep keeps its own rule; reason):

| # | item | Azhdaha | Apep | why |
|---|---|---|---|---|
| D1 | px set names | `normal jump inv tail_only dead`; `burrowed` only a rig vis state | `p1 p3u p3c burrowed aloft parked inv dead`; `burrowed` is also a px set (no proxies, inv, `vis` null) | plan R7 names; the vis state stays separate because the body sinks visibly before it hides |
| D2 | proxy width | one `w` per proxy | one `w` per proxy = max of the two stance widths of R7 | the framework has one interaction width; a generous width only helps the hitter |
| D3 | capsules | boxes, `head` gated by `px` / `top_max` | boxes + the plan column `col {f, r}`; no gated capsule | plan R11 columns, same runtime record |
| D4 | clip extras | — | `form`, `stance`, `stance_events`, `px_sets`, `look_events`, `hand_events`, optional `keyed_pitch`, `scale_in`, `blend_in`, `blend_out` | two forms, two stances, hand variants (R8, R12) |
| D5 | hidden spans / root z | `body` / `tail` / `all`, `root_z` for the tail pillar | always `all`, `root_z` always empty | the whole body burrows straight down (R9) |
| D6 | mirrors | 6 mirrored clips | none (`mirror_of` null); the module mirrors yaw signs | the plan has no mirrored clips |
| D7 | yaw on a loop | loops have `yaw` null | `turn_p3` carries a rate schedule (6°/t) | plan R16 lists `turn_p3` among the yaw schedules |
| D8 | part idx | from `0x01` | from `0x00` (`0x00-0x37`) | plan R4 slots |
| D9 | `budgets.elements_shown_rest` | an int | `{p1, p3}` | per-form gate (R14) |
| D10 | look channels | `legs`, `tail` (+ `petrify`, `glow`) | `form face core core_glow tint bright` (same channel record) | R12 |
| D11 | park | — | `park` key + `rig/park` / `unpark` in Apep's own builder output | FN-25 park is not in RIGLIB 039b911 |
| D12 | rig manifest extras | — | `apep`, `stances`, `hands`, `park`, `sprites`, `elements`, `skeleton.bones / joints_by_stance`, `proxies.rest_by_stance / coverage`, part `parent / tol_tp / brightness_p3 / reach` | plan §3.9 item 1 |
| D13 | org manifest | — | new file and schema (§0.5) | organisms, Heart, domes, walls, stalks |
| D14 | registry `shield` / `scale` | `shield` false, `scale` 0.1 | `shield` true, `scale` 2.0 (husk 0.1 only while hidden, FN-13) | plan §3.7 torso click shield beside the proxies |
| D15 | theme `look_lines` | optional (the generator diffs) | required, ≤ 24 slices, `fill … replace` boxes | plan §4.2 (the CS white-out budget) |
| D16 | theme props | `el: 'fight'`, `uuid` in the boss block, `rlk_mb_aux` on props, group tag `rlk_mb_<boss>_ap_<group>` (s2.md: `rlk_mb_az_ap_*`) | `el: 7`, `uuid` in the Apep arena-prop block, no `rlk_mb_aux`, group tag `rlk_mb_ap_ar_<group>`, props kept across the look swap by UUID | one element; FN-3 (cm.md §12 makes `rlk_mb_aux` optional); `rlk_mb_ap_ap_*` would read badly |
| D17 | theme points / constants | `az_cavern` keys | `ap_oasis` keys (§0.6.3), `CHECK` given | each theme chooses its own keys (theme.md §4.2) |
| D18 | `entrance_layout()` | `glyphs` = the two element-glyph spots on the stele | same key set; `glyphs` = the two gate-crystal spots `crystal_w` / `crystal_e` | no rolled elements; no new key for the room generator |
| D19 | kit conventions | `el` = `#elem` 0-5, sector 7.5° steps, element families, field pool | `el` 7 + styles 20 / 22 / 23 / 24, any-degree sector, no element families, dressing + flood pools, `hud/title`, `hud/whiteout`, prefix `#wk` | `ap_fx_api.md` §0.13 |
| D20 | pattern scratch prefix | `#aq<id>` | `#apq<id>` | inside Apep's `#ap*` space; never meets `#aq` |
| D21 | test ids | Azhdaha's table | plan §12.2 + 99 idle | different patterns |
| D22 | music | phases 1-2 (`"2"` reused in phase 3) | three tracks `"1" "2" "3"` | plan Q17 |
| D23 | RES | `{"0":30,"5":30,"*":10}` + the rolled pair | `{"7":30,"*":10}`; organisms `mbRes7 20`, rest 10 via `#auxResEl 7 / #auxResElV 20` + `#auxRes 10` | plan U2 |
| D24 | object / entity tags | `rlk_mb_az_*` | object tag on the object's marker only, display tags `rlk_mb_ap_<display>` | one selector per object kind (`@e[tag=rlk_mb_ap_heart]` = the marker) |

---------------------------------------------------------------------------------------------------

## 0.11 Decisions (D0), requests, open items

Decisions taken here (binding; reasons in the rows above):

1. The stubs are the frozen clip / event contract (§0.4.10, §0.5.5); AP-RC1 / AP-ORG1 validate `--against` them.
2. Who applies clip data: the rig applies `stance_events`, `look_events`, `hand_events` and visibility `state`; the core
   applies `px_sets` (framework `px/state`) and the yaw schedules (anchor turns); patterns read anchors / tracks via
   `api.py` only.
3. Burrows use the px set `burrowed`; the entrance and the CS revival use `inv`; phase 2 uses `parked`.
4. Capsules are AZ boxes with the plan column kept as `col`.
5. Pattern ids = test ids where the plan has one; services 50 / 51 for E / D.
6. The look state is the stamp; props survive the look swap by UUID.
7. Org `next` chains as in §0.5.5.
8. Theme constants and points as §0.6.2-§0.6.3 (positions AP-ARENA may refine only where the row says so).
9. Kit names frozen in `ap_fx_api.md` §0 (AP-FX adds names only by request).

Request protocol (s2.md §13 shape): `S:ap/requests/<stage>.md` (`core`, `p1`, `p3`, `rev`, `fx`, `rig`, `org`,
`arena`), append-only entries `## R<stage>-<n> <type>: <title>` with what / why / needed by and `status: open | done
<commit> | rejected (<reason>)`; served the same day by the owner of the file; nobody edits another stage's file.

Open items for other owners (none blocks AP-R1 / AP-ORG1 / AP-FX / AP-ARENA):

| # | for | item |
|---|---|---|
| O1 | S1-CM (while `wip/az-cm` is open; else AP-FW) | build the reserved FN-15 `#hzPm` / `#hzPmL` (Q2 ticks 30 ‰, blast 800 ‰), FN-29 `#auxShW` / `#auxShH` / `#auxHbY`, FN-30 `mv/step_flat`; until then Apep's documented fallbacks (FN-14 option b, `data merge`, a module stepper) |
| O2 | S1-CM | cm.md §9.5 says px bodies are husks at scale 0.1 without a shield; §2.2 lets `shield: true` keep the click shield. Apep relies on §2.2 (`px` + `shield` + `scale 2.0`): a cproto variant with `shield: true` in `test_px.py` would cover it |
| O3 | S1-CM | the music `len` of the three Apep events (FN-23), by request into the registry |
| O4 | AP-R1 | RIGLIB is at 039b911 on the release branch: AP-R1 can import `T:mboss_shape_lib.mjs` directly (no temporary `apep_shape.mjs`, R20) if it branches from 039b911 |
| O5 | AP-ARENA | check `fill … replace <filter> strict` on pack format 121 (§0.6.5) |
| O6 | AP-CORE | the phase jumps of the test ids (§0.8) and `#apPT` / `#apPid` in its §1 |
| O7 | AP-CORE (first commit) | re-read `S:az/contract/` after Azhdaha's D0 adversarial pass (in progress at 02:20 UTC; no file changed since 2026-10-18 23:03 UTC) and carry any renamed shared name into §0.10 by a change note |

---------------------------------------------------------------------------------------------------

## 0.12 Change notes

- **2026-10-19 (AP-SPEC, D0)**: §0 written. Completed the earlier partial attempt: capsules as AZ boxes (the partial
  stub had zero-length boxes), the px set `burrowed`, the required eight px sets, `turn_p1_step`'s −90° reached at t9,
  `turn_p3`'s rate schedule, staggered B-hand events in `stand_p3`, the entrance A-claw raise / plant, org `next`
  chains; validator checks for clip names, px sets, capsules, hidden-tick sets, anchors and yaw knots. Aligned with the
  Azhdaha day-0 contracts as of 2026-10-18 23:03 UTC (re-checked at 2026-10-19 02:20 UTC, unchanged) and with
  S1-ARENA's committed `az_cavern` theme (`wip/az-arena` c8000fa): compass bearings, the `CHECK` / `BOX` / `START`
  dict shapes, z-major water tiles, the `entrance_layout()` key set (Apep's gate crystals ride in `glyphs`).

- **2026-10-21 (AP-CORE, `wip/ap`)**: §1 written (module interfaces). The registry entry went in as §0.3.6 with the
  measured music re-pick periods (6870 / 6376 / 6881, AP-FW `L.music_len`) instead of `len 0`; enabled true, route false.
  The stub manifest the core writes for the framework points the rig API at the stand-in `AP:rig_stub/**` (§1.10); the
  in-memory stub and every clip / event / id of §0.4.10 are unchanged. Q3s has `phase 3` (§1.11.5). O6 is answered by §1.8,
  O7: `S:az/contract/` re-read, no shared name changed.

- **2026-10-22 (fix 10-22f, user feedback on the real game)**: the `rotation` clip re-keyed (events, yaw knots, the
  `hand_a_r` track: §0.4.5, §0.4.10, the frozen stub and `validate.py` follow; a D0 change); Q2 runs on two clocks (the
  field and the domes on the pattern clock, §5). Details §5.

## 0.13 10-20 Telegraph rule (user, 2026-10-20) — pointer

`plan.md` §14 "10-20 Telegraph rule (user)" is binding: a hazard (boss or organism) gets a ground decal only where the
footage shows one. *keep*: P1's shadow glide (no gold ring), P2's crack strips (no fill), P4's disc, Q1's leaf-pad trail +
rosette ring, Q3 shell 1's target disc, Q3s's leaf ring and shell disc, and the Q2 field / dome mechanic. Every other §8
hazard (P1 sweep, P2 plunge, P3 slams and carpet pre-fill, P5 / Q4 wedge lanes, P6, Q1 slam + sweep, Q3 shells 2-3, Q5
landings + blades, O1, O2, O4 spots, O6a, O6b, O7) calls no kit decal: `#hzQuiet 1`, the impact preset at the hit tick,
the readable tell from the clip / prop named in the note. §0.7's pairing line ("every damaging decal …", plan §7.11 rule 1)
and the `pat_*` decal == hazard checks apply to *keep* rows only; the ≥ 10 t floor (U4, §7.11 rule 2) counts from the
motion tell for the rest (`TABLE` fields `tele`, `tell_src`). `api.wedges()` still builds the `hz/sector` wedges; it no
longer emits the `tele/wedge` stack. No tick, size or coefficient changes.

---------------------------------------------------------------------------------------------------

# 1. Module interfaces (AP-CORE, 2026-10-21; `wip/ap`)

Written by AP-CORE with its first commits on `wip/ap` (from `wip/cm-ap` f1908f3 = AZ-CM b255669 + AP-FW). The code is the
reference: `T:mboss_apep/api.py` (the contract module: every name below), `core.py`, `ai.py`. Frozen at AP-I1; changes
by request (§0.11), each with a change note in §0.12. Paths `AP:` = `F:mboss/apep/`.

## 1.1 Package layout and ownership

| file | content | owner |
|---|---|---|
| `T:build_mboss_apep.py` | entry: `mboss_apep.core.build()` | AP-CORE |
| `mboss_apep/api.py` | ids, registry / arena / theme / rig / org manifests (merge + stand-ins), DMG / DMG_PM / REV / ORG_PM / WAVES / NURTURE_MODE tables, AI constants, texts, `Pattern`, `Gen`, `TL`, `stub_pattern`, `K` (the kit or `KitStub`), `wedges`, selectors | AP-CORE (AP-FIX: the balance values only) |
| `mboss_apep/core.py` | the 17 hooks + prep, the phase machine, the main slot, services, px-set / yaw drivers, push request, HUD / bars, props, tests, kit stand-ins `AP:kstub/**` | AP-CORE |
| `mboss_apep/ai.py` | §1.7 | AP-CORE (weights through `WEIGHT_OVERRIDE` by AP-FIX) |
| `mboss_apep/stub_rig.py` / `stub_rig_rt.py` / `stub_org.py` | the D0 stubs (ids 1000 + k) and the stand-in rig `AP:rig_stub/**` | AP-CORE; dropped at AP-I2 / AP-I1 |
| `mboss_apep/p1.py` | patterns 1-7 + `AP:p/move/fx` | AP-P1 (stub by AP-CORE) |
| `mboss_apep/seq.py` | `AP:seq/**` (E, D) | AP-P1 (stub) |
| `mboss_apep/p3.py` | patterns 31, 33-36 | AP-P3 (stub) |
| `mboss_apep/aftermath.py` | pattern 32 + `AP:dome/**` | AP-P3 (stub) |
| `mboss_apep/revival.py` | services 20, 40, 60 + `AP:rev/**`, `AP:heart/**` | AP-REV (stub) |
| `mboss_apep/org.py` | `AP:org/**`, `AP:wall/**` | AP-REV (stub) |

`api.OWN` enforces it at build time (`Gen.w` asserts the writer may write the path): p1 owns `p/{burrow,hands,glow,wither,
tail,combo,reloc}/**` + `p/move/fx`; seq `seq/**`; p3 `p/{mstrike,shells,tail3,spiral,surface}/**`; aftermath
`p/aftermath/**` + `dome/**`; revival `p/{t1,fail,cs}/**` + `rev/**` + `heart/**`; org `org/**` + `wall/**`; the core
everything else under `AP:` except `rig/**` (the rig generator), `om/**` (the org generator) and the kit's owned paths
(`fx/{e,p,tele,dress,snd,hud,prop,test}/**`, `fx/{card,cardx,look,clear,uninstall}`, + the kit manifest's `owned`). The
core's `clean()` deletes every file under `AP:` it owns and did not write (so any generator order gives the same bytes).
Every module file has `emit(g)` and a `PATTERNS` list (may be empty); the build imports `p1 p3 aftermath` then
`seq revival org` (`__init__.PATTERN_MODULES`, `SERVICE_MODULES`), then the core.

## 1.2 The module tick (hook `tick`, @s = body, `#mbSt 1`)

Order: `#apFc` += 1 (the fight clock; frozen while paused) → the hit flash (`#apFlash` = `#mbPart` of the last hit →
the rig flash of that proxy's group) → phase 1: `ev/tick` (the floor → T1 queue) and `ai/ring` (the BACK dwell sample
every 10 t) → phase 2: `rev/tick` (the stage) → phases 1 / 3, slot empty, no cine: `ai/state` (idle tracking, leash,
the decision) → `p/run` (the main slot) → `yaw/tick` (while a yaw clip plays) → `push/req` → `hud/tick` → the rig tick
(`rig/tick`, or `rig_stub/tick`; + `rig_stub/chain` while clips fall back) → `pxs/tick` (the px set of the clip tick
now shown; copies `apRigStance` into `#apStance`) → `#apNoPush 0`. `intro_tick` (E) and `death_tick` (D) run the seq
module's tick with `#apPT = #mbT - 1`, then the rig and px drivers.

## 1.3 Patterns (`api.Pattern`) and the main slot

`Pattern(id, key, label, kind, clip=None, phase=None, weight=None, cooldown=0, first_after=0, lead=0, recover=20,
max_len=200, length=None, last_hit=None, chain=None, opener=None, gates=(), hooks=())` (docstring in api.py). Kinds:
`normal` (AI-picked by weight), `scheduled` (Q2: forced when due), `chain` (Q3s: only as a chain), `opener` (R: before its
host), `service` (main-slot services: 10 move, 20 T1, 40 fail, 60 CS, 61 stance), `seq` (50 E / 51 D: no slot). Every
non-seq pattern writes `AP:p/<key>/{start,tick,cancel}`; declared `hooks` (`pause resume reload vis pj_end`) write the
same-named files. The build asserts the §0.8 ids / kinds exist (`core.NEED`), unique ids / keys, the files.

Slot scores (mb): `#apPid` the running id (0 idle), `#apPNew 1` = start this tick, `#apPT` the pattern clock (−lead+1 ..
0 = its first clip's tick 0 ..), `#apPLen` the expected end (HUD, fairness sim; `Gen.set_len`), `#apPMax` = max_len,
`#apPEnd` (set by `p/end`), `#apPRel` (set by `p/release`). Life of a pattern: `p/begin` (clock −lead, the first clip
`p.clip` played by the core at clock 0, then `start`) → `tick` every tick with `#apPT` → the pattern calls
`Gen.end()` (or reaches max_len) → `p/finish`: the kept / lock markers killed, `ai/pat_done` (the opener hand-over
`#apNext`, `#apCool` = recover, `#apCdE<id>` = `#apFc` + cooldown counted from the END, `#apPatN` / `#apP3N` / Q2
counters, the chain roll, the rest px set of the form). During a lead the core pre-turns the body (`mv/turn`, 3 deg/t
phase 1, 6 deg/t phase 3). `Gen.release()` = the dangerous part is over: with a queued transition (`#apTr 1`) the core
ends the pattern there (its `cancel` cleans the tail) and T1 starts at the next decision. `cancel` must be idempotent
and work from any executor (tests, reload, death, the phase jumps call it); pattern entities carry `rlk_mb_ap_p<id>`
(`Gen.keep(tag)` keeps a lock marker under such a tag) and `rlk_room rlk_mb_aux`. Pattern-owned names: `#apq<id>...`
(mb), storage `rlk:mboss ap.p<id>`. Chains: `chain={id: pct}` rolled after the pattern ends unless it ran as a chain
(`#apChainRun`), the chain starting `max(0, last_hit + 20 − length)` t after the end (plan 7.4: ≥ 20 t after the last
hit). Openers: `opener=(id, dist b)`: when the player is farther the opener runs first and hands over through `#apNext`.
`#apArg` = a test argument (P6 hits; 0 = roll); `#apAft1` 0 = the next Q2 is the first (non-lethal), 1 = lethal.

Stub helper `api.stub_pattern(g, p, tick=[(t, line)], end=None)` (AP-CORE's frames): start / tick / cancel that play the
clips at their clocks and end at `p.length`. The pattern stages replace the stubs file by file (same keys, ids, clocks).

## 1.4 `Gen` (the writer handed to every `emit(g)`)

Files: `w(rel, lines)`, `pw(key, name, lines)`, `has(rel)`, `fn(rel)` (a `function AP:rel` line). Rig (through the core's
wrappers): `play(clip)` (= `AP:play/<clip>`: the rig's play + the clip's yaw schedule armed; `#apYawS -1` before it
mirrors the yaw; `turn_p3` is a rate loop and not yaw-driven: turn with `mv/turn {max:6}`), `flash(group)`,
`face(player|track)` (head only; the rig never turns the anchor), `hands(set)`, `rig_look(channel, look)`, `bright(13|15)`,
`stance('crouch'|'stand')` (= `play/crouch_p3|stand_p3`). Slot: `end()`, `release()`, `set_len(t)`, `at(t | (t0, t1),
cmd, clock)`, `every(n, cmd, start, clock)` (n in `Gen.MODULI` = 2 3 4 5 6 7 8 10 20 40; `#apK<n>`). Core services:
`svc(name)` (§1.5), `px(set)` (the px set; `burrowed` / `parked` also hide the husk: scale 0.1 + `rlk_mb_noshield`).
Positions: `lockp()` (the floor under the player, clamped r 25.3), `lockb(d)` (d b from the player toward the boss,
clamped r 14), `lockv(lead)` (the framework predictive lock re-tagged `rlk_mb_ap_lock`), `keep(tag)`, `clamp(kind)`
(walk 25.3, idle 14, burst1 18, burst3 16, glide 16), `move_to(sel, spd)` (one glide step inside r 16, yaw kept),
`tp_to(sel)` (the anchor to the floor point of a marker; the anchor never enters blocks: the clip sinks the body).
Hazards / projectiles with the module defaults (Dendro el 7, **quiet** = no framework outline, no framework sound;
reactions kept): `hz_opts(**kw)`, `pj_opts(**kw)`, `hz_disc ring sector line full aim resize mask extend safe_new`,
`pj_launch pj_steer pl_dot GRP_NEW tag_last_hz`; `decal('keep', *kit lines)` = a kit ground decal, allowed only for the
*keep* rows of the 10-20 telegraph rule (§0.13). Misc: `kit` (= `K`), `sound(event, vol, pitch)` (vanilla only),
`particle(...)`, `line(text, colour, hold)` (the sub-line typer). `TL(g, key)` builds per-tick timelines with a dispatch
tree; `api.wedges(clip, t0, t1, reach)` the swept tail wedges.

## 1.5 Core services (`AP:svc/<name>`, idempotent, any executor; `Gen.svc(name)`)

`park` / `unpark` (R10: the body 30 b above the centre, NoLeash, px `parked`, the rig parked / back at the centre on the
floor, px `inv`), `centre_hidden`, `cine_on` / `cine_off`, `music_1..3` / `music_stop`, `title_p1` / `title_heart` /
`title_p3`, `px_rest` (p1 / p3u / p3c by the phase and `#apStance`), `phase_1` / `phase_t1` / `phase_2` / `phase_cs` /
`phase_3` (set `#apPh`; phase 1 also the 1 % floor, phase 2 floor 0 + `#apTr 0`, phase 3 floor 0 + the Q2 clock reset),
`repool_p3` (47 %), `floor_p1` / `floor_0`, `look_p1` / `look_p3` (the rig form), `arena_lush` (the arena look job when
the theme exists + the lush props) / `arena_withered`, `heal_cs` (25 % max HP through `player/heal`), `push_ring_cs`
(8 → 12 b), `req_cs` / `req_fail` (cancel the slot, start service 60 / 40 now; no-op while it runs), `lose`
(`cb/lose`), `targetable` / `untargetable`, `lib_clear` (framework libraries + the kit telegraphs), `hud_now`.

## 1.6 Files the service modules provide (`api.REQ_FILES`; the build asserts them)

- seq: `seq/entrance/{setup,tick,done}` (setup as the new body at `intro/setup`; tick with `#apPT` 0..109; done at the end
  of E or a reload / test skip, idempotent), `seq/death/{start,tick}`.
- revival: `rev/{start,tick,ready,reload,pause,resume,clear,bars,hud}`, `heart/{add,sub}` (macros `{v}`: progress ±v,
  clamped 0..10000; the stage tick starts the CS / failure), `heart/{p1_hang,p1_up,p1_respawn,clear}`; the core also calls
  `rev/test_timeout` (test 29). `rev/tick` runs as the body every phase-2 tick and must return while `#apPid ≥ 1`
  (a fail / CS service runs); `rev/bars` sets the bossui scores (`#buHp`, `#buMax`, `#buHpCol 10`, `#buNoNum 1`,
  `#buSub*`); `rev/hud` the name extras and the sub-line, and clears `#apHudQ`. Services 20 / 40 / 60 own their timelines
  and call the core services; 20 ends with `svc/phase_2` + `rev/start`, 60 with `svc/phase_3`.
- org: `org/aux_hit` (inside the `aux_hit` hook after the immunity line), `org/clear`, `org/freeze`, `wall/clear` (the
  recorded walls + `arena/ap_oasis/sweep {y0:201,y1:202}`); the core also calls `org/spawn_<kind>` (tests 23-28,
  positioned) and routes `hz_vis` ids 70-79 to `org/vis` and `pj_end` props tagged `rlk_mb_ap_opj` to `org/pj_end` when
  those files exist.
- aftermath: `dome/clear`.

## 1.7 AI (`ai.py`)

Decision order: test request (`#apReq`) > `test/lock` (`#mbLock`) > queued T1 (`#apTr 1`, phase 1) > a pending chain
(phase 3) > Q2 due (phase 3: first after `Q2_FIRST_AFTER` = 1 phase-3 pattern; then `#apFc ≥ #apAftCd` (= the last end
+ 900, or a cancel + 300) and ≥ 3 other patterns) > phase 1: anti-stall (BACK for 3 decisions while P5 cools → a
180-degree crab-turn), the rim rule (anchor beyond r 12, player BACK → P1 50 % if off cooldown, else the turn), the BACK
rule (≥ 2 of the last 3 samples, every 10 t, in BACK → 75 % P5 off cooldown; the first one types the hint) > a move
(phase 1, never two in a row: far band 40 % crab crawl, mid band 15 % side walk) > the weighted pick > fallback (phase 1
a crab-turn step, else idle 10 t). Zones (`#apZone` 1 FRONT 2 SIDE 3 UNDER 4 BACK, plan 7.3; SIDE also takes the forward
diagonals outside the cone), bands (`#apBand`), the weight column (`#apCol`: phase 1 front_near / front_mid /
front_far / side_under / back; phase 3 near / mid / far), `#apF` / `#apS` (mb), `#apDist` (tenths), `#apWide`
(|dyaw| > 60), `#apRim`, `#apCFree`. Weights: `Pattern.weight[column]` (0-9) or `ai.WEIGHT_OVERRIDE`; cooldowns
(`#apCdE<id>`), `first_after` (`#apPatN`), no immediate repeat (`#apLast`; moves set `#apLastMv`), gates `side_rear`
(SIDE with f < 0 only) and `centre_free` (the player farther than 5 b from the centre). Idle: phase 1 tracks ≤ 3 deg/t
within 60 degrees, beyond it a crab-turn step (service 10 kind 3) unless the player is BACK; phase 3 tracks ≤ 3 deg/t;
the leash back inside r 14 at 0.13 b/t. Service 10 kinds (`#apMvK`): 1 crawl (≤ 40 t at 0.25 b/t toward the player, then
`crawl_stop_p1`), 2 side walk (`#apMvD` ±1, 40 t at 0.12 b/t), 3 a step (`turn_p1_step`, mirrored by side), 4 two steps.

## 1.8 Test ids (the phase jumps of §0.8)

`test/pattern {id}` runs as the body after `intro/done` (E skipped). Phase-1 ids (1-6, 8 = `#apReq 7` + `#apNext 4`,
9 = P6 with `#apArg 4`, 20 T1) first jump to "phase 1 ready" (`ph/ready_1`: stage gone, unparked, p1 look CROUCH, pool
53 %, floor 1 %, music 1); phase-2 ids (21-29, 40, 41, 23-28 spawns, 30 / 60 the CS) to "phase 2 ready" (`ph/ready_2`:
parked, Heart, progress 2700, the stage from wave 1); phase-3 ids (31-37, 61) to "phase 3 ready" (`ph/ready_3`: lush,
pool 47 %, p3 UPRIGHT at the centre). Every test first cuts whatever runs (`ph/cut`: libraries, the slot, domes, the
queued transition, the cine). 32 sets `#apAft1 0` (a first, non-lethal Q2), 37 `#apAft1 1`; 40 / 41 set `#apFail` 0 / 1
and the progress 0; 99 idles; any other id prints `test/help`.

## 1.9 Scores and storage of the core (mb unless noted)

Phase `#apPh` (0 E, 1, 15 T1, 2, 25 CS, 3, 9 D), `#apTr` (1 queued, 2 running), `#apFc`, `#apCool`, `#apTot` (= `#mbTot`
at the end of E; organism pools are ‰ of it), `#apPx` (the px set index of `api.STATES`), `#apHide`, `#apStance`
(0 CROUCH 1 UPRIGHT, from the rig's `apRigStance`), `#apPark`, `#apFlash`, `#apNoPush` (a pattern sets 1 to suppress
the body push this tick), `#apHudQ`, the slot / AI scores above, `#apYaw*`. Revival stage (rev/clear resets): `#apHt`
(‱), `#apWave`, `#apClk`, `#apWT`, `#apTo` / `#apToT` (time-out), `#apFail`, `#apStage`, `#apAlive`, `#apSlots`,
`#apOArg`, `#apOrgN`, `#apHtP`. Entity objectives (`ai/consts`): `apK apS apT apL apShd apOC apOI apSock apTok`.
Storage `rlk:mboss ap` (`ap.yw` the yaw schedules ×100, `ap.ya`, pattern keys `ap.p<id>`). Rig objectives `apRig*`
(manifest `objectives`). The core zeroes its fake players at spawn and cleanup (`ai/vars`).

## 1.10 The stand-ins and how they switch (AP-I1 / AP-I2)

- Rig: `api.MAN` = the real manifest (`T:mboss_apep_rig_manifest.json`, schema 1, source rig) merged per clip with the
  stub (ids ≥ 1000 for the names it lacks; `FALLBACKS`). `api.rig_fn(name)` names `AP:rig/<name>` when that file exists,
  else `AP:rig_stub/<name>`; `play_fn` likewise per clip. The JSON the core writes for the framework
  (`T:mboss_apep/stub_rig_manifest.json`) is the D0 stub with its API paths on `AP:rig_stub/**` (the framework's px
  compiler calls the manifest's `functions.state.*`); `ap/tests/spec_check.sh` proves the rest equals the D0 contract.
  The core applies `px_sets` (from `apRigC` / `apRigT` after the rig tick) and the yaw schedules; the rig applies state,
  stance, look and hand events and must keep `apRigC` / `apRigT` / `apRigStance` as the stand-in does.
- Kit: `api.K` = `import build_mboss_ap_fx` when it imports, else `KitStub` (the §0.10 signatures; each call is an
  empty `AP:kstub/<path>` written by the core for the paths used). The kit hook lines of §0.12 are AP-I1's.
- Org models: `T:mboss_apep_org_manifest.json` (source org) else `stub_org.py`'s; the stub runtime shows one item display
  per organism (`rlk_mb_ap_om`, linked by `apOI`).
- Theme: `mboss_arena_ap_oasis` when it imports, else `api._THEME_FALLBACK` (POINTS of §0.6.3, the 16 lush water tiles
  only); without the theme `svc/arena_lush` swaps only the props (the stub arena has no look job).

## 1.11 Decisions of AP-CORE

1. The registry entry is **enabled** with `route: false` (§0.3.6 / cm.md §2.4: `test/chapter {id:"apep"}` needs the
   entry in `creg` / `cbyid`, and runs stay on Raiden until AP-I2). Music `len` = the AP-FW measured re-pick periods
   6870 / 6376 / 6881 (≥ the longest track of each pool) instead of §0.3.6's 0.
2. `NURTURE_MODE 'A'`: the 양육 itself is immune while it holds ≥ 1 link (tag `rlk_mb_ap_imm`; the core's `aux_hit` sets
   `#dmg 0` for any tagged organism → aux/take shows "면역"). 'B' would tag the buffed basics instead.
3. The anchor never sinks: burrows move it with `Gen.tp_to` on the floor while the clip hides the body (plan 7.2).
4. The crab-turn step only for a player outside BACK; idle tracking stops beyond 60 degrees (a BACK player stays BACK for
   the BACK rule). Moves never follow a move.
5. Q3s (36) is a phase-3 chain pattern (`phase=3`): it counts for the Q2 schedule like the others.

---------------------------------------------------------------------------------------------------

# 2. AP-I1 freeze (2026-10-21; `wip/ap` in `S:ap/wt_core`, I1 commit **d15e500**)

I1 commits on `wip/ap` (first parent): merges 403b6bc (release), 724393f (org), daf072c (fx), c543a60 (arena), 72148c0
(rig), da9e4e5 (r3b); c096344 (RC2 probes re-derived), 4797f69 (regenerated merged tree), 6395bb6 (the `boss/<id>`
move, its own commit), d15e500 (the wire). The pattern branches start from d15e500.

From here on `api.py` and `core.py` (and `ai.py`) belong to the integrator; the pattern stages AP-P1 (`p1.py seq.py`),
AP-P3 (`p3.py aftermath.py`) and AP-REV (`revival.py org.py`) own only their files and ask for everything else in
`S:ap/requests/<stage>.md` (protocol §0.11: append-only `## R<stage>-<n> <type>: <title>`, what / why / needed by,
status). `S:ap/i1_notes.md` is the hand-over for those three stages.

## 2.1 What is merged

| branch | commit | what |
|---|---|---|
| release `claude/exciting-pascal-ek1vuy` | fef7e90 | chapter mode, Azhdaha released + fixed, Raiden rework (`boss/raiden`, own kit), tip removal, kit-font fallback, real-game fixes |
| `wip/cm-ap` (AP-FW) | f1908f3 | was already the base of `wip/ap` |
| `wip/ap-org` | d3417c6 | organisms, Heart, domes, walls, stalks, seed (`AP:om/**`, `T:mboss_apep_org_manifest.json`) |
| `wip/ap-fx` | 5e7834f | the kit (`AP:fx/**`, font `rlk:mboss_ap`) |
| `wip/ap-arena` | 75b05e1 | the `ap_oasis` theme and the Sumeru gate |
| `wip/ap-rig` + `wip/ap-r3b` | 443e5d8 + f357c7f | the rig (R3 + RC1 + RC2 clips, R3b model fixes); RC2's floor probes re-derived for the R3b petal feet |

## 2.2 Function roots (user 10-21): `AP:x` = `F:boss/apep/x`

- The registry entry carries `"fn": "boss/apep"` (Azhdaha `"boss/azhdaha"`); `mboss_lib.fn_root(b)` / `fn_root_of(id)`
  give the root, default `mboss/<id>`. `api.ROOT` = `boss/apep`, `api.NS` = `rlk:boss/apep/`, `api.FDIR`; the kit's
  `K.FN` = `rlk:boss/apep/fx/`; the rig `rlk:boss/apep/rig/`, the org models `rlk:boss/apep/om/`. Always build paths
  from `NS` / `F(...)` / `K.FN`; never type `rlk:boss/apep/` or `rlk:mboss/apep/` by hand.
- Unchanged: every entity tag (`rlk_mb_ap_*`, `rlk_mb_apep_part`), score (`mb`, `apK apS apT apOC apOI …`), storage
  (`rlk:mboss ap`, `rlk:apkit`) and resource-pack path (`rlk:mboss/apep/<model>`, `rlk:mboss/apep_om/…`,
  `rlk:mboss/ap_kit/…`, font `rlk:mboss_ap`). The framework (`mboss/cb`, `mboss/px/apep`, `mboss/hz` …) stays in mboss/.
- Test commands: `/function rlk:boss/test/<cmd>` for `chapter {id}`, `chapter_ch {id,ch}`, `pattern {id}`, `lock {id}`,
  `kill`, `abort`, `lose`, `level {lv}`, `stop` — aliases of `rlk:mboss/test/<cmd>` (same arguments).
- The D0 spec (`S:ap/spec/*.schema.json`, the stub manifests, `make_stubs.py`) now names `rlk:boss/apep/...`
  (backups `*.pre_bossroot`).

## 2.3 The real parts and the stand-ins left

- **Rig**: the real manifest, **0 clip fallbacks**; `AP:rig_stub/**` is no longer written (`api.stub_rig_needed()`
  false). `stub_rig.py` / `stub_rig_rt.py` and `T:mboss_apep/stub_rig_manifest.json` stay until AP-I2 (plan §10), and the
  framework's px compiler still merges it per clip (all clips come from the real file).
- **Kit**: `api.K` = `build_mboss_ap_fx` unconditionally (`KIT` True); `KitStub` and `AP:kstub/**` are gone. The kit's
  Python API (§0.10, `ap_fx_api.md` §10) is the only way to make kit calls; its fixed functions are called as
  `f'function {K.FN}clear'`, `…uninstall`, `…tele/clear`, `…dress/redraw`.
- **Org**: `api.ORG` = the real manifest (asserts `source == "org"`); `stub_org.py` and `stub_org_manifest.json` are
  deleted. The organism **runtime** (`org.py`) is still AP-CORE's working stub (one vanilla item display per organism,
  `rlk_mb_ap_om`, following by `tp`): AP-REV replaces it with the real models (`om/<kind>/spawn` as the aux husk,
  `om/tick` / `om/objects_tick`, `om/face` after a turn — requests/org.md RORG-1..3).
- **Theme**: `mboss_arena_ap_oasis` (both looks, 24-tick look swap, 64 lush / 12 withered props, the gate crystals);
  `api.THEME_STUBBED` False.

## 2.4 Kit hook lines (ap_fx_api §0.12), as wired

`uninstall` → `fx/uninstall`; `cleanup` (and the fight end / abort through it) → `fx/clear` + `fx/hud/clear` +
`fx/dress/clear`; `pause` → `fx/tele/clear` + `fx/hud/flash_end` + `fx/hud/banner_end`; `resume` → nothing;
`reload` in phase 2 (`rl/p2`) → `fx/dress/redraw` at the arena centre (`api.CENTRE`); `death_start` → `fx/tele/clear` +
`fx/hud/clear`; the phase-2 name-line badges and the failure mark are `K.badge(kind, True)` (`rev/hud`). The kit font
`rlk:mboss_ap` now ends with a `reference` provider to `minecraft:default` (as the az / bf / fg kits), so a text list may
start with a kit glyph.

## 2.5 No-tips rule (user 10-21, binding)

No in-game advice telling the player how to act — no HUD sub-line, banner, title, chat or door text — except warnings of
instant-kill mechanics and prompts the real game shows for Apep. Removed at I1: `TXT['fail_hint']` (the 20-s "수호 →
강화된 기본 → 파괴 순서로 처치하세요" after a failure, plan §3.4) and `TXT['back_hint']` (the first BACK-rule P5 line);
`api.REV['fail_hint_t']` is gone. Kept: `p2_goal` 「마물을 처치해서 소생 진행도를 올리세요」 and the Q2 banner
「소생의 찬가 보호막 안으로 들어가서 종말의 여파를 막아내세요」 (both in the footage: v2 39.6 s, v3, v5 18.2 s, w1), the
instant-kill warnings `fail_line` 「다시 한 번 실패하면 쓰러집니다」 and `q2_lethal`, and the neutral lines (names, titles,
phase messages, numbers, the 「!」 time-out warning). Not to be built: plan Q10's "first-cast hint" of the homing
wheels and any other first-time hint; the footage captions (`v3` / `v4` uploader captions) are not game prompts.

## 2.6 What changed in the frozen names (§1)

- `api.KitStub`, `api.SO`, `api.ORG_STUBBED`, `api.ORG_STUB_FILE`, `core.SO_emit`, `core.Core.stubs` are gone; `api.ROOT`
  is new. Everything else of §1 holds.
- Harness: the apsim world runs the **real** rig and kit functions (they are not in AzSim's stubbed prefixes), so the
  real rig parts carry `rlk_mb_apep_part` (`rlk_mb_aps` was the stand-in's tag); pattern tests read clip plays from
  `s.calls_log` (`play/<clip>`) or the rig scores `apRigC` / `apRigT`.

---------------------------------------------------------------------------------------------------

# 3. AP-I2 integrate (2026-10-21; `wip/ap` in `S:ap/wt_core`, I2 commit **f588262**)

I2 commits on `wip/ap` (first parent): merges 06faa32 (`wip/ap-p1` c47ab3b), 9f5b77e (`wip/ap-p3` d2e6262), 31b6111
(`wip/ap-rev` e599e69), each with its generated outputs regenerated by `build_mboss_apep.py` (conflicts only in the generated
`p/resume_d` and `pj_end`); then f588262 (requests, the stub rig dropped, route, README). Pattern files are the integrator's
from here on (AP-REVIEW reads, AP-FIX writes by finding); plan §14 "AP-I2 integrate" is the change note.

## 3.1 What changed in the frozen names (§1, §2)

- `api`: the stub rig is gone (`STUB`, `merge`, `STUB_MANIFEST`, `REAL_CLIPS`, `RIG_STUBBED`, `REAL_RIG`, `stub_rig_needed`,
  `fallback_list`); `CLIP_NAMES` is the D0 list (§0.4.10) asserted against the real manifest; `FALLBACKS` / `EV_FALLBACKS`
  stay (empty); `rig_fn` / `play_fn` assert the rig's function exists; `rig_tick_lines()` = `rig/tick` only. New:
  `Gen.yaw_rebase()` (`AP:yaw/rebase`), `wedges(clip, t0, t1, reach, swept=False, near=3.0, extra=1.5)`.
- `core`: new `AP:obj/tick` (the org objects' clips, every module tick incl. `intro_tick` / `death_tick`, before the stage
  and the slot), `AP:yaw/rebase`, `AP:hud/bar_q2` + `bar_q2g` (the Q2 countdown while `#apPid 32`, `#apq32` ≤ 188);
  `push/req` not in phase 2; `uninstall` kills `@e[tag=rlk_ap_om]`; `SR_emit` gone (no stub manifest written).
- Kit (`ap_fx_api` §16): `tele/disc_o`, `tele/crack_o`, `p/o1_hit`, `p/flood_part`; `K.tele_disc(..., fill)`,
  `K.tele_crack(..., fill)`.
- Registry: `apep` `route: true` (chapter 3; Azhdaha 1; Raiden 2 and 4+).
- Revival: `heart/tick` gone (the core steps the Heart); `heart/p1_up` = `om/heart/play/heart_up` (+ `rlk_mb_ap_hup`).
- Perf (visual only): `org/burst_all` bursts two organisms at once and queues the rest (`rlk_mb_ap_burstq` markers, in
  `MODULE_TAGS`) for `org/burst_q` (two per tick, called by `p/fail/tick` and `p/cs/tick`); P3's `pj_end`: a wheel that ran out
  fizzles (`spark` + dust), a hit pops (`wheel_pop`).

## 3.2 Requests

Served: RP1-1, RP1-2, RP1-3 (+ Q4), RP1-4 (plan note), RP1-5, RP3-1, RP3-2, RP3-3, RP3-4, RP3-6, RREV-1, RREV-2, RREV-3,
RREV-4, RREV-5 (the push request only), RREV-6, RREV-7 (plan note), RI1-1, RORG-3. Informational: RP3-7, RP3-8, RREV-8.
Open for AP-REVIEW / AP-FIX: RP3-5 (`tail_p3` swing 2's reach), RREV-5's framework proxy poll of the parked body, RRIG-5.
Every request file has an "AP-I2 status" section.

## 3.3 Tests (scratchpad, not in git)

`lib/apsim.py` has `revsim.py` folded in (installed at import); `run_all.sh` runs `pat_p1` / `pat_p3` / `pat_rev` beside
`test_apep` / `test_e2e_apep`; `spec_check.sh` validates the real rig / org manifests and that no stub rig is left;
`test_apep.py` (route, no stub rig, the real Heart, spawn markers + emergence, uninstall of the AP-ORG displays, the Q2
countdown 11f); `test_e2e_apep.py` (the shipped route + the lose variant); new `soak_ap.py` (the perf probe: a whole natural
chapter-3 fight; ticks ≤ 3000, phase 2 at the cap ≤ 800 average, ≤ 400 entities). Backups `*.pre_i2`.

## 3.4 Gates (measured)

- **Rebuild ×2** (the documented order with every RP builder into `S:ap/rp_ap`, `S:ap/i2/rebuild.sh`): two passes give the same
  datapack + manifests hash (7673377…) and pack hash (dc00251…).
- **`run_all.sh`** (the one full run, 13 min 48 s, on the tree before the perf fixes below): Apep part green but `ap_fx` (the
  kit test's call list / demos did not know `flood_part` / `o1_hit`: the test and the kit demos updated, 3904 checks OK). cm
  part: `test_chapter` and every M0 suite green; `test_m0diff`, the cm `gen_check` (9: the core's `boss/test/` aliases are
  hard-linked paths for it) and the cm `ident` (vs 22ba247) fail **identically on the I1 commit d15e500** (run there): the
  release's tip removal and the `boss/<id>` move, not this stage; the validators re-judged by `vjudge.py` (Apep classes on
  `boss/apep/` + the I1 tree's findings as a baseline, `S:ap/tests/baseline_i1/`): refs / macro / lint 0 other.
- After the run, re-run on the final tree: `pat_p1` (100), `pat_p3` (125), `pat_rev` (117), `test_apep` (every section across
  the runs, incl. 11f), `test_e2e_apep` (12, incl. the lose variant), `gen_check`, `ident_i1`, `spec_check`, `test_boss_alias`,
  `test_ap_fx`: all green.
- **Atlas gate** (`S:ap/i2/atlas_gate.py S:ap/rp_ap`): 11.541 M custom px (Apep 1.271, Azhdaha 1.686, Raiden 2.763, the rest
  5.822) ≤ 15.8 M.
- **Perf probe** (`soak_ap.py`, a whole natural chapter-3 fight on the shipped route): the worst tick 2763 (Q5 t49) ≤ 3000;
  phase 2 at the cap 709 commands per tick on average over 413 t ≤ 800; a failure strike at the cap 2089; ≤ 241 entities;
  no kit card skipped. Per pattern: `pat_p1` B1 ≤ 2554, `pat_p3` 11a ≤ 2713 (Q2's blast tick 1883 with the sliced flood).
- **Load check** (`S:mcsrv/loadcheck.sh`): 0 function load failures. No negative `scoreboard players add|remove` amount.
- **Storyboards** on the real rig: `S:ap/renders/i2_{burrow,hands,glow,wither,tail,combo,q1,q3,q3s,q4,q5,q2}.jpg` and
  `i2_rev_{t1,stage,walls,cs}.jpg` (scripts `S:ap/i2/render_i2_{p1,p3,rev}.py`).

# 4. AP-FIX + AP-VERIFY (2026-10-22; `wip/ap` in `S:ap/wt_core`, head **0f4c88e**)

## 4.1 What changed in the frozen names (§0, §1)

- §0.4.5 yaw knots of `tail_p3`: 13 → 0, 21 → 200, 24 → 200, 36 → 0, 45 → −17, 51 → −204, 53 → −230, 57 → −230, 86 → −360
  (RV-01; `S:ap/spec/validate.py` follows). Events, lengths, RETIME unchanged.
- New: `api.CS_HEAL_T` (80), the CS hooks `p/cs/rise` (t32) and `p/cs/resume`, `p/fail/warn`, the kit sound `fx/snd/q3_lock`.
- `api.DMG` / `api.REV` hold the AP-FIX values (plan §9.3 / §9.5); `Q4['lunge_gap']` 4.0 (p3.py).
- Nothing else in §0-§3 moved; the hook list, the tags, the scores, the storage and the RP paths are unchanged.

## 4.2 Commits

2a2dd58 (merge of the release head 46ae53a), f9e9e22 (core: RV-06, RV-13, RV-12 part), 82943f2 (rig: RV-01), 5c1eed4 (kit +
arena: RV-05, RV-08), 6a811e4 (kit: q3_lock), d57f9ab (patterns: RV-02, RV-01 lunge gap, RV-07, RV-10, RV-09), 8833dc7
(balance: RV-03 / RV-04), f36ceff (kit demo), 0f4c88e (the build stamp " · 빌드 10-22b 아펩").

## 4.3 Gates (measured on the final tree)

- **Rebuild ×2** (`S:ap/i2/rebuild.sh`, RP = a fresh copy of the release pack `S:rd/rp` + every builder): identical
  (datapack+json 6293c3ae…, RP dc002510…); `git status` clean after both. `check_raiden_pack` against `S:ap/rp_ap`: 178 models,
  0 problems.
- **`run_all.sh`** (tag vfy, the one full run, 794 s for the Apep part after 13 min of the cm part): the Apep part green
  (pat_p1 100, pat_p3 127, pat_rev 119, test_apep incl. the fix section, test_e2e_apep, gen_check, ident_i1 now vs the merged
  release 46ae53a with the build-stamp line allowed, spec_check, boss_alias, ap_org 268, ap_fx 3908, ap_arena, ap_rig 146);
  the cm part green except test_m0diff / gen_check 9 / ident vs 22ba247, whose failure lines are identical to the I2 run
  (the release's tip removal and the boss/<id> move); `test_chapter` green; the validators re-judged by `vjudge.py` 0 other
  (the class now also covers `mboss/arena/ap_oasis/**` and the release's `boss/raiden/**` `with storage` calls).
- **Azhdaha quick set**: `test_e2e_azhdaha.py` pair 0: 26 checks, 0 failures; `test_wire_az.py`: 44 / 46, the two failures
  are H2 / H3, which expect chapter 1 to be the only routed chapter boss (now `cb/route` also has the Apep chapter-3 line).
- **Raiden quick** (`S:rd/tests/test_raiden.py -k quick`): ALL OK.
- **`check_mboss_pack`** 0 problems; **atlas gate** 11.541 M px ≤ 15.8 M.
- **Soak** (`soak_ap.py`): worst tick 2654 ≤ 3000, phase 2 at the cap 709 ≤ 800, ≤ 243 entities, no kit card skipped.
- **Load check** (`S:mcsrv/loadcheck.sh`, tag ap_vfy): 0 function load failures; the log has only the offline
  services-discovery warnings.
- **Fairness** (`S:ap/balance/analysis.txt`): 30 of 34 plan §9.7 rows (plan change notes "AP-FIX + AP-VERIFY").
- **Renders**: `S:ap/renders/final_sheet.jpg`, the storyboards `S:ap/renders/vfy_{burrow,hands,wither,q1,q3,q4,q2}.jpg`,
  `i2_q4.jpg` (RV-01).

# 5. Fix 10-22f (user feedback, 2026-10-22; build " · 빌드 10-22f 아펩 패턴 수정")

## 5.1 P4 초목이 시든 풍경: the swing lands on the full fill

- Measured before (HEAD 377688c; the compiled poses, `S:fix1022/tools/measure_p4.mjs`; the user's clip
  `S:ap/user_refs/ingame_1022.mp4`): the disc decal made at t16 (tell 24) fills t17 → t40; the hazard strikes at t40; the
  crash drops the right A claw onto the floor at t40 (a vertical drop, 0°/t of sweep), then the body lay still 40-47 and the
  spin (yaw 47-71, smoothstep) only got going at 49-50 (≥ 8°/t from t50, 22°/t at 59): the sweeping limb passed the front
  (the player's bearing) at t63, 23 t after the hit and the full fill. In the clip: fill on the rim at frame 31 (60 fps),
  the crash 29-31, the hurt flash 33-34, the visible spin from frame ≈ 66 (≈ 12 t later).
- Now: the whirl starts at 32 (yaw schedule above, to the boss's left), the right A arm winds out (`CRASH_WIND` at 36,
  over the spot the crash plants it on) and comes down through the front: floor contact (claw tip ≤ 0.35 b) at t40, 7°
  right of the facing, sweeping 15°/t (1.8 b/t at r 6.9); it then drags round the floor to t64 (one whole turn). The
  fill full tick (t16 + 24), the hit (t40) and the contact (t40) are one tick (`p1.py` asserts it from the track; pat_p1
  P4h / P4i check it in the sim). Hazard `hz/disc r 9 tell 24`, active over the whirl: **24 t** (was 31), the decal hold
  24; spin trails every 3 t 34-64, the flash at 52. Hit tick, size, coefficient, KB, the 23-t fill: unchanged.

## 5.2 Q2 종말의 여파: the field from the banner, random domes further apart

- Two clocks: `#apPT` (B0 = the banner) and `#apq32` (the clip; `#apq32S` = 8 + n). At B0: the banner, the footprints,
  the wash (r 26, fills over 20 t, held to clip t176) and the field ring (r 3 → 26 in 20 t) at the arena centre, and
  the field-tick mask: `q2_tick` **20 ‰** max HP (was 30), never lethal, re-armed **every 10 t** (was 15) from `#apPT 20`
  to the tick before the blast (`#hzAct = #apq32S + 136`); 15 ticks (no walk) to 20 (the 50-t walk) = **30-40 % max HP**
  for a player who never enters a dome (was ≤ 5 ticks × 3 % from clip t80).
- Domes on the pattern clock: light pillars `#apPT` 24 / 28 / 32, formed **34 / 38 / 42** (was clip 54 / 58 / 62);
  dome 0 is the player's (nearest the band's player) and forms first; so the ticks at 20 and 30 find nobody inside (the
  chip before the shield, user 10-22). Domes stand ≥ 122 t before the blast (U4 ≥ 85).
- Footprints: one of 12 precomputed layouts per 3-b band of the player's distance (`aftermath.LAYOUTS`, 9 bands),
  picked by `random value 0..11`, in the frame at the centre facing the player. Rules (`layout_ok`): centres 7-17.4 b
  from the centre (the dome edge ≤ 21.9 b: inside the walk radius 26, clear of every arena prop, the innermost a lily pad
  corner at 21.99 b), pairwise **14-30 b** (table 14.0-29.9; was ≥ 9, 9.0-30.5 in practice), never near-equilateral
  (the three distances not within 15 %, the angles not all 60 ± 10°), the player's dome ≤ 9 b from any player position
  of the band inside the walk radius (≤ 9.3 b at the barrier 26.6 b).
- Unchanged: the banner text (the allowed instant-kill warning), the blast (800 ‰, t156-175, first cast non-lethal +
  `q2_lethal`), the heal (1 % / 20 t, clip t54-174), the pop t189, the no-tips rule.

## 5.3 Gates (measured on the fixed tree)

- pat_p1 102 ok, pat_p3 131 ok, test_apep (build p3 ai tests pause reload px budget fix) 46 ok, test_e2e_apep 15 ok,
  test_ap_rig 146 ok, test_ap_fx 3908 ok, spec_check ok, test_boss_alias ok.
- Rebuild ×2 (`S:ap/i2/rebuild.sh`, RP `S:ap/rp_ap`): identical (datapack+json a27b5866…, rp 0ec6b12c…), the RP unchanged
  by the fix; `check_mboss_pack` 0 problems.
- Load check (`S:mcsrv/loadcheck.sh`, tag ap_q2): 0 function load failures; `rplint` on `S:ap/rp_ap`: 0 problems.
- Fairness: plan change notes "Fix 10-22f" item 4.

