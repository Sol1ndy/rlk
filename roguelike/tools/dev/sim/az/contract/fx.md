# Day-0 contract: the 야타용왕 FX / audio / HUD kit, call list (`fx.md` = `az_fx_api.md` §0 skeleton)

Owner: **S1-FX** (`wip/az-fx` from `wip/fg`@aa8cd73, merges M0 later; on call as S2-FX). Readers: S1-MOD (`api.K`, the
hook wiring at I1), every S2 author (through `api.K` / `Gen`), S1-ARENA (prop names), I1-WIRE. Binding inputs:
`S:az/plan.md` §0 rules 1-8, §1.4 N1 / N2 / N6, §2.4 (the deliverable table, **frozen at S1 start by this file**), §2.6,
§4.4, §4.10-§4.11, §5 (every fx / sound row). Model: the field-generator kit (`T:build_mboss_fg_fx.py`,
`S:mb3/fg_fx_api.md`): this kit is that engine copied and renamed, with the extensions listed here. `S:az/az_fx_api.md`
(the full API doc) starts from this file as its §0; later sections describe the visuals; the names and arguments below
do not change without a request (`S:az/requests/*.md`, served the same day).

---------------------------------------------------------------------------------------------------

## 0. Ownership, prefixes, hooks

### 0.1 Paths

| what | path | owner |
|---|---|---|
| card engine entry points | `AZ:fx/{card,cardx,look,clear,uninstall}` | this kit |
| internals, telegraphs, presets, sounds, HUD, props, tests, demos | `AZ:fx/{e,p,tele,snd,hud,prop,test}/**` | this kit |
| any other name under `AZ:fx/` | — | module core (left alone by the kit's cleaner) |
| generator, painters, manifest | `T:build_mboss_az_fx.py`, `T:mboss_az_fx_paint.py`, `T:mboss_az_fx_manifest.json` (`owned`, kinds, presets, props, sounds, glyphs, caps, objectives, tags, palettes) | this kit |
| sprites / models / item definitions | `assets/rlk/{textures,models/item,items}/mboss/az_kit/<kind>` + atlas entries `rlk:mboss/az_kit/*` appended to `assets/minecraft/atlases/items.json` by the generator's merge | this kit |
| HUD font | `assets/rlk/font/mboss_az.json`, `assets/rlk/textures/font/mboss_az/*` (**U+E800-E8FF**) | this kit |
| tests, renders | `S:az/fxtests/**` (`test_az_fx.py`, `run_kit.sh`), `S:az/fxrender/**` | this kit |
| never written | `AZ:rig/**` (rig), every other `AZ:**` path (module), every other kit | — |

`AZ:` = `F:mboss/azhdaha/`. The kit's cleaner touches only its owned paths (manifest `owned`); the module's `foreign()`
spares them, also while the kit is absent (plan §1.5).

### 0.2 Prefixes (no collision with the core's `#az*` / `rlk_mb_az_*` / `rlk:mboss az`, the fg kit's `#fk*`, the bf kit's `#bk*`)

Fake players `#ak*` (objective `mb`); objectives `akS akG akH akK akD` (the fg kit's `fk*` roles); entity tags `rlk_ak`
(every card), `rlk_ak_t` (attack telegraphs), `rlk_ak_f<k>` (field pool id k), `rlk_ak_ml<k>` / `rlk_ak_ml<k>c` (moving
lanes), `rlk_ak_wv<k>` (wave rings), `rlk_ak_sr<k>` (safe rims), `rlk_ak_demo`; storage `rlk:azkit`; font `rlk:mboss_az`;
item models `rlk:mboss/az_kit/*`. Every card also carries `rlk_room` + `rlk_mb_aux` (every cleanup path removes it).
Apep's kit takes U+E900-E9FF and checks this font.

### 0.3 The kit never

Decides gameplay, makes hazards or projectiles, counts hits, moves the body, calls the rig (`AZ:rig/**`), or reads the
rig manifest. The demos (`fx/test/*`) use a vanilla stand-in anchor tagged `rlk_ak_demo`.

### 0.4 Hooks the module core wires (at I1-WIRE; plan §7.3)

| module hook / event | kit calls |
|---|---|
| `uninstall` | `fx/uninstall` (cards, demo anchor, objectives, `#ak*`, `rlk:azkit`, schedules) |
| `cleanup`, fight end, abort | `fx/clear` + `fx/hud/clear` |
| `pause` | `fx/tele/clear` + `fx/tele/field_clear` + `fx/hud/flash_end` (the module redraws its field table on resume: `tele/field` / `tele/strip` with the same ids and the remaining life) |
| `death_start` | `fx/tele/clear` + `fx/tele/field_clear` + `fx/hud/clear` |
| a cancelled pattern | `fx/tele/clear` is the core's; a pattern ends its own lanes / waves / rims (`mline_end`, `wave_end`, `safe_end`) |
| HUD lines | the core composes `extra[]` / `sub[]` from `K.glyph()` / `K.badge()` strings (the kit owns no boss-bar line) |

No `rlk:tick` / `rlk:load` hook: cards are aged by `fx/e/world` (a `1t` schedule chain started by the first card, as the
fg kit, with its first-tick fix). A dead or reviving player clears every card by itself.

## 1. Conventions (the fg kit's §1 unless changed here)

- Executor context: position = the event point (floor points at the floor top, y 201 in `az_cavern`), rotation = the aim
  (yaw; pitch 0 unless stated). Planes `face flat cross band box`, billboards, the radial trick, stages and `off` exactly
  as the fg kit.
- Units: blocks, ticks, degrees, RGB ints (`16777215` = untinted). **Telegraph and field sizes in tenths of a block**
  like the framework hazards.
- **`el`** = `#elem` numbering. Palettes (rim / fill / flash, starting values; S1-FX tunes them on the cavern floor and the
  water sheet): 0 physical `#E5304A/#FF6474/#FFB8C4`, 1 Pyro `#C8461E/#FF8A3D/#FFD2A0`, 2 Hydro `#1E6FC8/#4FB8FF/#CDEBFF`,
  3 Electro `#6A3FC8/#C58BFF/#EEDDFF`, 4 Cryo `#3AA6C0/#9FE8F5/#E8FBFF`, 5 Geo `#D27A0C/#F0A93A/#FFE8A0` (default); 6-8
  draw Geo.
- **`nd`** (undodgeable look, plan rule 6): 0 normal; 1 = the shared undodgeable look (a red-amber rim `#FF5A1E` + the
  kit's 回 glyph card at the decal centre, along lines every 4 b); 2 = undodgeable + low band (jumpable): 1 + a jump
  chevron. Every `#hzNoDodge` decal uses `nd ≥ 1`.
- Layering above the floor top: water sheet +0.005 (arena prop), field pool +0.03, attack fills +0.035, rims +0.045,
  wave rings +0.048 / +0.05, mask wash +0.03 (≥ 0.025 b clear of the water sheet everywhere).
- Every macro accepts `with storage` arguments (ints for `el`, `nd`, sizes, ticks), so the module can pass the runtime
  element (`#azE` → storage → macro, plan N1).
- **Element families out of range** (`fx/p/<name>/<el>`, `fx/prop/<name>/<el>`, `fx/hud/*/<el>`, `fx/snd/*/<el>`): the
  family dispatcher checks `el` with literal score tests **before** its `$function …/$(el)` line, so a missing member is
  never called (a macro line naming a missing function aborts the whole function). An `el` outside the family's range
  runs the family's default member: Geo (5) for the 1..5 and 3..5 families, nothing (a silent no-op) for the 1..4
  families (banners, absorb sounds, shards). `test_az_fx.py` calls every dispatcher with `el` 0 and 9.
- Caps: ≤ **64** live fx cards (further `card` calls skipped), ≤ **40** live attack-telegraph cards (telegraph calls
  skipped from 34 on, so a shape is never half drawn), **16** field-pool cards (own pool, never counted against the
  other two), ambient presets skipped from 40 live fx cards.
- Pairing rule (plan rule 1): every damaging decal is called in the same tick as its framework hazard with the same
  `tell` and size (`#hzQuiet 1`, `#hzSfx 0`); the fill's leading edge reaches the rim on call + tell (the strike tick),
  where every card of the shape flashes, then stays `hold` ticks.

## 2. Card engine

| function | args | does |
|---|---|---|
| `fx/card` | `{kind, pos, rot, bb, roll, spin, s0, s1, move, life, fade, col}` | fg kit §2.1 |
| `fx/cardx` | `card` args with vector `s0` / `s1` + `{off, dly, dur, hit, col2}` | fg kit §2.2 |
| `fx/look` | `{kind, col}` | as `@s` (a module item_display): the kind's model + tint, full bright |
| `fx/clear` | — | every kit card (fx, telegraphs, lanes, waves, rims, fields), counts zeroed |
| `fx/uninstall` | — | §0.4 |
| `fx/test/{kinds,tele,presets,sounds,hud,props,stage,stop}`, `fx/test/demo/<name>` | — | the fg kit's test set; demos per §5 pattern on the stand-in anchor |

## 3. Telegraphs (`fx/tele/*`, macros; visual only)

| function | args (tenths, ticks) | cards | drawn at | used by |
|---|---|---|---|---|
| `tele/disc` | `{r, tell, el, nd, hold}` | 2 | floor point | all |
| `tele/ring` | `{r0, r, tell, el, nd, hold}` | 3 | floor point | P2, P5 outlines |
| `tele/sector` | `{r, a, tell, el, nd, hold}` — `a` = half-angle 1..180, drawn in **7.5° steps** (a fan of 15° cards), `a ≥ 175` = a disc | ≤ 26 | apex, rotated = aim | P1 crack fan |
| `tele/wedge` | `{r0, r1, a0, a1, tell, el, nd, hold}` — annular sector between `a0 < a1` (degrees relative to the executor's yaw, Minecraft sense: + = clockwise from above; `a1 − a0` ≤ 180), radii `r0..r1` | ≤ 14 | apex, rotated = reference yaw | P7 swept wedges (§3.1) |
| `tele/line` | `{len, w, back, tell, el, nd, hold}` (−back..len along the aim; negative `back` starts beyond the point) | 5 | start point, rotated = aim | P3, P8, strips |
| `tele/lane_side` | `{len, w, back, tell, el, hold}` (always the `nd 1` look + a dust-wall edge on the outer rail) | 5 | start point, rotated = axis | P6 flank strips |
| `tele/wave` | `{id, r0, r1, w, tell, dur, el, nd, hold}` (id 0-7): the fill to `r0` over `tell`, then the front ring travels `r0 → r1` over `dur` with the band edge `w` behind | 4 | floor centre | N10 fronts (P2, P5, P5b, T1, Cryo rings) |
| `tele/wave_to` | `{id, r, dur}`: retarget a live ring from its current radius to `r` over `dur` ticks (eased fronts as linear segments) | – | anywhere | N10 knots |
| `tele/wave_end` | `{id}` | – | anywhere | |
| `tele/mline` | `{id, len, w, back, tell, el, nd, hold}` (id 0-7), `tele/mline_aim {id}`, `tele/mline_turn {id, d}`, `tele/mline_end {id}` | 5 | pivot, rotated = aim | P3 lane following the player until t14 |
| `tele/heptagram` | `{r, tell, el, hold}` star {7/2}, meander tips, central rune (`r` = circumradius) | ≤ 6 | floor centre | 41 |
| `tele/hexagram` | `{r, tell, el, hold}` + the 번개 rune | ≤ 5 | floor centre | 46 |
| `tele/starseal` | `{r, tell, el, hold}` white star seal + rune | ≤ 4 | floor centre | 45 |
| `tele/seal8` | `{r, tell, el, hold}` two squares + 火 runes | ≤ 5 | floor centre | 32 |
| `tele/mask_wash` | `{r, tell, hold}` one floor-wide violet card over radius `r` | 1 | arena centre | 42 |
| `tele/safe_rim` | `{id, r, tell, hold}` (id 0-5) green rim with the glyph on the same card | 1 | safe-circle centre | 42 (round 1 = 1 wash + 5 rims = 6 cards, the §10 / plan §2.4 cap) |
| `tele/safe_beam` | `{id}` a particle column on rim `id` (lives with the rim) | 0 | — | 42 |
| `tele/safe_end` | `{id}` | – | — | 42 |
| `tele/crater` | `{r, tell, hold}` rubble ring at the floor cut | 2 | floor centre | B3 |
| `tele/halo` | `{r, h, tell, el, hold}` an air ring `h` above the landing spot | 1 | landing floor point | 32 small meteors |
| `tele/glyph_circle` | `{r, tell, hold}` the gold floor glyph circle of the intro seal (decor, never paired with a hazard; plan §2.2 "intro dressing", §5 E) | ≤ 4 | floor centre (the spawn) | E (`seq.py`) |
| `tele/clear` | — attack telegraphs, lanes, waves, rims (not the field pool) | | | core |

### 3.1 The P7 union

The whip's decal is the union of its per-tick swept wedges (plan §5 P7, rule 1): at t0 the host calls one `tele/wedge`
per swept tick k (positioned at that tick's tail root, rotated to the reference yaw, `a0..a1` = the tail-line angles of
ticks k−1 and k, `r0 0`, `r1 120`, `nd 1`), each with `tell` = its sweep tick (k − 0: the decal and its `hz/sector` are
made together at t0 with the same tell, ≥ 20) and the same `hold`. The kit draws exactly the given wedges, so the union of
decals equals the union of hazards by construction (the module's static check, plan §8.3-1). The paired hazard of one
wedge is one framework `hz/sector {r:120, a:⌈(a1 − a0) / 2⌉, …}` at the same tail root, aimed at reference yaw +
(a0 + a1) / 2 (`#hzR0 0`, `#hzNoDodge 1`, all wedges one volley group): M0's sector is symmetric about its aim with an
integer half-angle, so the half-angle rounds up (the hazard is never smaller than its decal). Budget: ≤ 9 wedges × ≤ 2
cards for 115°.

## 4. Field pool (N6; separate cap 16 cards = 8 fields)

| function | args | does |
|---|---|---|
| `tele/field` | `{id, r, el, life}` (id 0-7, r tenths, life ticks) | a lingering field disc (fill + rim) at the floor point; calling an id again redraws it (refresh, resume) |
| `tele/strip` | `{id, len, w, yaw, el, life}` | a lingering strip from the executing point along the **absolute** world yaw `yaw` (int degrees) |
| `tele/field_end` | `{id}` | remove field id now |
| `tele/field_clear` | — | every field card (pause, death; the module redraws from its table on resume) |

Families and caps are the module's (fire ≤ 4, hail ≤ 2, strip ≤ 1; ids allocated by the module's field table).

## 5. Presets (`fx/p/<name>`)

### 5.1 Element families (`fx/p/<name>/<el>`, el **1..5** contiguous; the dispatcher `fx/p/<name> {el, …}` passes the other args)

| name | args | does |
|---|---|---|
| `impact` | — | impact burst (crystal / water / flame / ice / spark) at the floor point |
| `cracks` | `{r}` | crack fan along the executor yaw |
| `crown` | — | blade crown burst |
| `dust_ring` | `{r}` | dust / spray / embers / frost / sparks ring |
| `slab_throw` | — | slab / boulder throw streaks (at the slab, rotated along the throw) |
| `footfall` | — | footfall at a planted foot (Geo dust, Hydro splash, Pyro flame splash, Cryo frost, Electro sparks) |
| `brand_rune` | — | the brand rune over the player's chest (called every 4 t) |
| `vortex` | `{t}` | absorb vortex for `t` ticks around the body |
| `recolour` | `{r, t}` | the recolour wave from the boss outward to `r` (tenths) over `t` ticks |
| `sigils` | — | sigil cards (火 / 水 / ⚡ / ❄ / Geo) |
| `front` | `{r0, r1, w, dur}` | the 3-D wave front (streaks + slabs + dust / water / fire walls) moving with `tele/wave` (call 1 t before the strike, fg `wave_band` rule) |
| `dig` | — | B3 dig in place (mounds / water / ember / ice puffs / violet slabs) |
| `flank_blades` | `{len}` | P6 blades out-and-up along a flank strip |
| `spike_line` | `{len}` | P8 spike line along the aim |
| `shard_rain` | `{r, t}` | absorb-2 cosmetic shard rain / bolts |

### 5.2 Named presets (plan §2.4 list + the §5 rows)

| name | args | rows |
|---|---|---|
| `geyser` | — | P1 Hydro |
| `blade_trail` | — | Hydro blades (at the blade prop, every 2 t) |
| `lump_trail` | — | Pyro lumps |
| `meteor_big` / `meteor_small` | `{h}` | 32 falls (at the floor point, starting `h` up) |
| `fire_dome` | `{r}` | 32 impacts |
| `frost_burst` | `{r}` | Cryo rings, 41 |
| `ice_wall` | — | P7 Cryo wall piece |
| `hail` | `{r}` | hail fields (ambient) |
| `bolt` / `bolt_round` | — / `{r}` | Electro bolts / 42 floor-wide crackle (two waves 8 t apart) |
| `shell_dive` | — | 44 |
| `icicle_trail` | — | 41, 43 |
| `ice_sphere` | — | 43 aura at the sphere prop |
| `orb_ribbon` | — | 31 (at an orb, every 2 t) |
| `spark_column` | `{h}` | 44 tell |
| `stele_shatter`, `prism_shatter`, `seal_reform`, `petrify_pulse` | — | E, D |
| `splash`, `splash_wall` | — / `{r}` | water steps, P5b |
| `dust`, `rock_rain`, `mound`, `light_shaft` | — / `{r}` / — / — | P9, B3 |
| `gold_plume`, `shard_fall` | — / `{h}` | P4 |
| `dust_wall` | `{len}` | P6 |
| `boulders`, `tail_lane`, `leaf_burst`, `cones` | — | P7, P8 |
| `skid`, `dust_trail` | — | P3 |
| `shock_dome` | `{r}` | roar dome rings |
| `emerge_spikes` | `{r}` | B3 emergence |
| `glyph_glow`, `gold_leaves`, `gold_motes` | — | entrance stele (every 10 t), intro roar, ambience (ambient) |
| `cure` | — | the brand cleanse (butterfly-style cure fx) |

Python: `K.fx(name, **args)` (static), `K.fxe(name, el, **args)` (a family member `fx/p/<name>/<el>`).

## 6. Props (`fx/prop/<name>`, as `@s` = a module item_display; families `fx/prop/<name>/<el>`)

| prop | looks | use |
|---|---|---|
| `arena_crystal/<el>` | 1..5 | arena crystals (theme.md §6.3) |
| `water_sheet/<el>` | 1..5 | the 14-b water tiles at y 201.005 (~40 % alpha, element-tinted) |
| `glyph/<el>` | 1..5 | entrance stele + arrival glyphs (snowflake / bolt / flame / water curl / Geo) |
| `seal_stele`, `seal_chunk`, `seal_prism` | — | intro seal (E), death `seal_reform` |
| `gate_icon` | — | the gate label icon |
| `orb`, `meteor_big`, `meteor_small`, `lump`, `shell`, `icicle`, `ice_sphere`, `cone`, `crater` | — | §5 |
| `spike/<el>` | **3..5** (Electro, Cryo, Geo) | P4 / 45 / 46 spikes |
| `shard/<el>` | 1..4 | 응결 결정 (gold-amber with the element colour inside) |

Item models usable outside the kit (`minecraft:item_model`): `rlk:mboss/az_kit/gate_icon` (registry `icon.model`),
`rlk:mboss/az_kit/glyph_pyro`, `glyph_hydro`, `glyph_cryo`, `glyph_electro`, `glyph_geo` (the `k_cboss` icons:
`cprep.azhdaha.gate.model` / `model2`). Keep `teleport_duration:1` on moving props.

## 7. HUD (font `rlk:mboss_az`)

| codepoint | glyph |
|---|---|
| U+E800 | badge ◈ (white; tinted by the component colour) — name line |
| U+E801 | brand badge |
| U+E802-E806 | element mini-icons Pyro, Hydro, Electro, Cryo, Geo (sub-line) |
| U+E810-E813 | full-screen flashes white, gold, amber, violet (title line) |
| U+E821 | jump chevron (the U+E820 "점프!" title cue was removed: user 10-21, no jump prompt) |
| U+E822 | 回 mark (hint lines) |
| U+E840 / U+E841 | banner ornaments left / right |
| U+E8F0-E8F2 | spaces −1 / +2 / +1 |

The generator refuses to write the font when a codepoint collides with any `assets/*/font/*.json` (E100 hud, E300
minimap, E400 bossbar, E500 gd, E600 bf, E700 fg; Apep E900).

| function | does |
|---|---|
| `hud/banner_tr/<el>` (1..4) | transition message "야타용왕이 곧 {물} 원소의 힘을 흡수합니다…" (actionbar 60 t) |
| `hud/banner_ab/<el>` (1..4) | "{물} 원소 흡수" |
| `hud/banner_ab2/<el>` (1..4) | "{번개} 원소 흡수" + "원소를 추가로 하나 더 흡수합니다" |
| `hud/banner_brand/<el>` (1..4) | "야타용왕의 {물} 원소 공격에 맞고 보호막이 없으면 계속 {물} 원소 피해를 받습니다" |
| `hud/banner_end` | drop a banner early |
| `hud/flash_white`, `flash_gold`, `flash_amber`, `flash_violet`, `hud/flash_end` | title-line flashes |
| `hud/clear` | every banner / cue / flash off |

Element names: 1 불, 2 물, 3 번개, 4 얼음, 5 바위. Python: `K.glyph(name)`, `K.badge(el, lit)` (a text-component SNBT for
the name line: dim `#707070` until lit, then Pyro `#FF8A3D`, Hydro `#4FB8FF`, Electro `#C58BFF`, Cryo `#9FE8F5`), `K.FONT`.

## 8. Sound recipes (`fx/snd/<name>`, no args; vanilla events only; layers = the plan §5 rows)

| recipes | row |
|---|---|
| `chin_rear`, `chin_impact` | P1 |
| `jump_takeoff`, `jump_land`, `jump_wave2` | P2 |
| `charge_growl`, `charge_gallop`, `charge_skid` | P3 |
| `spikes_bristle`, `spikes_launch`, `spikes_land`, `spikes_explode` | P4 |
| `stomp_slam`, `stomp_wave` | P5 / P5b |
| `feint_sway`, `feint_burst` | P6 |
| `whip_raise`, `whip_sweep`, `whip_erupt` | P7 |
| `tslam_raise`, `tslam_impact` | P8 |
| `burrow_dive`, `burrow_loop`, `burrow_ring`, `burrow_rock`, `burrow_rush` | P9 |
| `slide_lift`, `slide_wave`, `slide_wave6` | T1 |
| `absorb_vortex/<el>`, `absorb_burst/<el>` (1..4), `absorb_roar`, `roar_ring`, `msg_chime` | T2, T3, the message |
| `b3_sink`, `b3_rise`, `b3_emerge` | B3 |
| `orb_spawn`, `orb_loop`, `orb_hit` | 31 |
| `meteor_glyph`, `meteor_fall`, `meteor_impact`, `meteor_small` | 32 |
| `fire_loop` | 33 |
| `frost_draw`, `frost_icicle`, `frost_burst` | 41 |
| `bolt_marker`, `bolt_strike`, `safe_chime` | 42 |
| `sphere_form`, `sphere_loop`, `lance` | 43 |
| `shell_spawn`, `shell_hover`, `shell_dive`, `shell_impact` | 44 |
| `ice_launch`, `ice_land`, `ice_erupt`, `hail` | 45 |
| `hex_draw`, `hex_bolt`, `hex_impact` | 46 |
| `intro_drone`, `intro_thump`, `stele_break`, `seal_shatter`, `intro_roar` | E |
| `death_sting`, `death_fall`, `death_seal` | D |
| `brand_apply`, `brand_tick`, `cleanse`, `shard_spawn`, `shard_pick`, `hint` | brand (§4.10), hints |
| `footfall/<el>` (1..5) | footfalls (§2.6) |

Python: `K.snd(name)`, `K.snde(name, el)`. Single extra layers stay `g.sound(event, vol, pitch)` in the module.

## 9. Python API (`import build_mboss_az_fx as K`; no files written on import)

`K.card(...)`, `K.tele_disc(r, tell, el=5, nd=0, hold=3)`, `K.tele_ring(r0, r, …)`, `K.tele_sector(r, a, …)`,
`K.tele_wedge(r0, r1, a0, a1, tell, el, nd, hold)`, `K.tele_line(len, w, tell, el, nd, hold, back)`,
`K.tele_lane_side(...)`, `K.tele_wave(id, r0, r1, w, tell, dur, el, nd, hold)`, `K.tele_wave_to(id, r, dur)`,
`K.tele_wave_end(id)`, `K.tele_mline(...)`, `K.tele_mline_aim/turn/end`, `K.tele_heptagram/hexagram/starseal/seal8(r,
tell, el, hold)`, `K.tele_mask_wash(r, tell, hold)`, `K.tele_safe_rim(id, r, tell, hold)`, `K.tele_safe_beam(id)`,
`K.tele_safe_end(id)`, `K.tele_crater(r, tell, hold)`, `K.tele_halo(r, h, tell, el, hold)`,
`K.tele_glyph_circle(r, tell, hold)`, `K.tele_field(id, r, el,
life)`, `K.tele_strip(id, len, w, yaw, el, life)`, `K.tele_field_end(id)`; `K.fx`, `K.fxe`, `K.snd`, `K.snde`, `K.prop(name)`,
`K.prope(name, el)`, `K.look(kind, col)`, `K.hud(name)`, `K.hude(name, el)`, `K.glyph`, `K.badge`; tables `K.KINDS`,
`K.PRESETS`, `K.EPRESETS`, `K.SOUNDS`, `K.PROPS`, `K.GLYPHS`, `K.AMBIENT`, `K.TELE_COL`; constants `K.CAP 64`, `K.TCAP 40`,
`K.SOFT 40`, `K.FCAP 16`, `K.FN` (= `rlk:mboss/azhdaha/fx/`), `K.FONT`, `K.OWNED_DIRS`, `K.OWNED_FILES`. Python builders
take blocks and convert to tenths; every builder asserts that its name exists. Until I1 the module's `api.K` is a no-op
set with the same signatures (plan §1.5).

## 10. Deliverables (plan §2.4) and test cases (`S:az/fxtests/test_az_fx.py`)

| kind | items | test case |
|---|---|---|
| telegraph | `disc ring sector wedge line wave(+_to,_end) mline(+aim,turn,end)` | shapes, sizes, every `el` palette, `nd` 1 / 2 looks, fill reaches the rim on the hit tick, sector 7.5° steps |
| telegraph | `lane_side` | undodgeable look |
| telegraph | `wedge` (the P7 union of §3.1) | union of the given wedges = their angular / radial bounds (no gaps between consecutive ticks) |
| telegraph | `heptagram hexagram starseal seal8 crater halo glyph_circle` | callable, card counts |
| telegraph | `mask_wash` + `safe_rim` + `safe_beam` + `safe_end` | ≤ 6 cards per 42 round |
| field pool | `field strip field_end field_clear` | never counted against the attack cap; redraw by id; **zero skipped attack-telegraph calls** on each pair's worst concurrent timeline (fields at cap + a strip + the phase-3 spike variant + a bg emitter + P1 / P4) |
| presets | §5.1 families × 5 elements, §5.2 | callable, card counts = manifest, all expire |
| props | §6 | models + sprite rules; the item models of §6 resolve |
| HUD | §7 glyphs and functions | glyphs present, no codepoint collision, banners per element |
| sounds | §8 | vanilla events only, no voices, pitch range |
| budgets | ≤ 64 fx / 40 attack telegraph / 16 field cards at the worst concurrent timeline of each pair; atlas ≤ **0.6 M px**; sprite sides multiples of 16, ≤ 512 | measured per timeline |

Green = `test_az_fx` + the M0 suites (plan §7.4). Renders in `S:az/fxrender/**` (sprites on the cavern floor and the
water sheet, telegraphs per palette and `nd`, presets, HUD).

## 11. Shared edits

None besides the atlas list (`assets/minecraft/atlases/items.json`: append only, through the generator's merge) and the
font collision check. The kit never edits hand-written files, the registry, the framework or the module.

## 12. Decisions (D0)

1. **Per-element presets, props, banners and sounds are numeric families** (`…/<el>`, contiguous ranges 1..5 / 1..4 /
   3..5) with a macro dispatcher, so runtime-element calls pass the pack check (`$(el)` suffix families only).
2. **`el` uses `#elem` numbering**; 6-8 draw Geo; violet is Electro's palette (the mask wash), green is the safe rim's own.
3. **`nd` levels 0 / 1 / 2** (normal / undodgeable / undodgeable + jump chevron).
4. **`wedge_union {id}` is realised as stacked `tele/wedge` calls by the host** (one per swept tick, §3.1) instead of a
   baked shape: no rig-manifest read in the kit, decal = hazard by construction.
5. **Waves get ids (0-7) and `wave_to` / `wave_end`**, so eased fronts are drawn as linear segments that match the
   hazard's per-tick resize (N10) and a cancel can end one ring.
6. **Field pool: 8 field ids × 2 cards = 16 cards**; strips take an absolute yaw so the module can redraw them from its
   table.
7. **`tele/halo` takes a height `h`**; **`tele/starseal`** added for 45's star fields (named in plan §5 45 fx).
8. **No kit stub rig and no rig calls** (unlike the fg kit): looks, flashes and glows are the module's rig calls.
9. **No kit-owned boss-bar lines**: the core composes the name / sub lines from `K.glyph` / `K.badge`. This departs from
   plan §7.3 (I1-WIRE: "HUD lines → `fx/hud/put_extra` / `put_sub`", the fg / bf kit pattern): there is no `hud/put_*`,
   I1-WIRE wires nothing for the HUD lines (S1-MOD's core builds them with `api.K` from day 1); a numbered plan change
   note records it.
10. **Family dispatchers never call a missing member** (§1): out-of-range `el` → Geo or a no-op.
11. **`tele/safe_rim` is one card** (rim + glyph), so a 42 round stays within the plan's 6-card budget.
12. **`tele/glyph_circle`** added (the intro's floor glyph circle named by plan §2.2 / §5 E but missing from §2.4).

## 13. 10-20 Telegraph rule (user, 2026-10-20) — pointer

Plan "Change notes" → **Change note 1**: ground telegraphs only where the footage shows one. The kit stays as built; its
callers now use only `tele/disc` as a rim without the progress fill (P4 landings, P9 rings, the Hydro geyser swirl),
`seal8` / `heptagram` / `starseal` without the fill, `hexagram`, `mask_wash` + `safe_rim` / `safe_end` (no `safe_beam`),
`crater`, `halo`, `glyph_circle`, the field pool and, optionally, the `tele/wave` ring as a front's own visual (no pre-strike
fill). Left without a caller: `tele/sector`, `tele/wedge` (§3.1), `tele/ring`, `tele/line`, `tele/lane_side`, `tele/mline*`,
`tele/safe_beam`, the `nd 1 / 2` look and the sprites listed in the note. The §1 pairing rule ("every damaging decal …")
holds for the *keep* rows; for the others the module plays the impact preset at the hit tick instead of the decal flash.
S2-FX: a no-fill option on `disc` / the seals (or rim-only calls) is the one kit change the rule needs (to be filed
under `S:az/requests/` when S2 starts).
