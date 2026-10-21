# 야타용왕 fx kit — API (`az_fx_api.md`)

Generator `tools/build_mboss_az_fx.py` (painters `tools/mboss_az_fx_paint.py`, manifest
`tools/mboss_az_fx_manifest.json`), owner S1-FX (`wip/az-fx`). This file lives in `tools/az_fx_api.md`; the scratchpad
copy `az/az_fx_api.md` is identical. §0 below is the day-0 contract (`az/contract/fx.md`) verbatim — names and
arguments there are binding; §13 on describe the implementation and the visuals, with the tables read from the
generator. Build:

    python3 tools/build_mboss_az_fx.py --resourcepack <unpacked RP> [--datapack <dp root>]    # or --skip-rp

Current build: 492 functions under `F:mboss/azhdaha/fx/`, 105 sprites (568,064 atlas px of the
600,000 budget), 42 presets + 15 element families, 78 sound recipes +
13 family members, 14 props + 5 prop families,
17 glyphs in `rlk:mboss_az`, 26 demos.

---------------------------------------------------------------------------------------------------

# §0 — the day-0 contract (`az/contract/fx.md`, verbatim)

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
  other two), ambient presets skipped from 40 live fx cards, trail presets (`boulders`, `tail_lane`, `dust`; `K.TRAIL`) from
  36 (`K.TSOFT`, AZ fix round STATE-14: the hit-tick impact / bolt / eruption visuals always find room under the 64 cap).
- Pairing rule (plan rule 1): every damaging decal is called in the same tick as its framework hazard with the same
  `tell` and size (`#hzQuiet 1`, `#hzSfx 0`); the fill's leading edge reaches the rim on call + tell (the strike tick),
  where every card of the shape flashes, then stays `hold` ticks.

## 2. Card engine

| function | args | does |
|---|---|---|
| `fx/card` | `{kind, pos, rot, bb, roll, spin, s0, s1, move, life, fade, col}` | fg kit §2.1 |
| `fx/e/cardf` (internal) | the fast card (AZ fix round STATE-2): `K.card` / `K.cardx` emit it whenever roll, spin, life, fade, dly, dur, hit and col2 are constants; the generator does `e/make`'s clamps and stage arithmetic, so a card costs about 25 commands instead of 63 (same entity, stages, tags and cap) | — |
| `fx/cardx` | `card` args with vector `s0` / `s1` + `{off, dly, dur, hit, col2}` | fg kit §2.2 |
| `fx/look` | `{kind, col}` | as `@s` (a module item_display): the kind's model + tint, full bright |
| `fx/clear` | — | every kit card (fx, telegraphs, lanes, waves, rims, fields), counts zeroed |
| `fx/uninstall` | — | §0.4 |
| `fx/test/{kinds,tele,presets,sounds,hud,props,stage,stop}`, `fx/test/demo/<name>` | — | the fg kit's test set; demos per §5 pattern on the stand-in anchor |

## 3. Telegraphs (`fx/tele/*`, macros; visual only)

| function | args (tenths, ticks) | cards | drawn at | used by |
|---|---|---|---|---|
| `tele/disc` | `{r, tell, el, nd, hold}` | 2 | floor point | all |
| `tele/disc_o` | the same arguments; outline only (the rim, no progress fill; plan Change note 1 "keep (trim)", I2 requests Rpa-2 / Rpb-1 / Rpl-3); Python `tele_disc(..., fill=0)` | 1 | floor point | outline-only disc rows without a footage shape |
| `tele/crack_o`, `tele/chev_o`, `tele/swirl_o` | `tele/disc_o`'s arguments; the shaped keep outlines of plan Change note 1 (AZ fix round FID-4): the gold zig-zag crack ring (sprite `t_crack`), the gold chevron ring (`t_chev`), the water-swirl field outline (`t_swirl`); Python `tele_disc(..., fill=0, style='crack' / 'chev' / 'swirl')` | 1 | floor point | P4 landing rings, P9 rock rings, the P1 Hydro geyser |
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
| `tele/heptagram_o` `tele/hexagram_o` `tele/starseal_o` `tele/seal8_o` | the same arguments as the plain seal; the seal art + rim, no progress fill (Change note 1 "keep (trim)", I2 request Rpt-3); Python `tele_<seal>(..., fill=0)` | 2 | floor centre | 41, 46, 45, 32 (every keep row uses these) |
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
| U+E820 / U+E821 | "점프!" big cue (title line) / jump chevron |
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
| `hud/cue_jump`, `hud/cue_end` | the "점프!" cue on the title line (12 t) |
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
| `slide_lift`, `slide_wave`, `slide_wave6`, `jump_cue` | T1 (+ the "점프!" bell) |
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
`K.SOFT 40`, `K.TSOFT 36`, `K.FCAP 16`, `K.FN` (= `rlk:mboss/azhdaha/fx/`), `K.FONT`, `K.OWNED_DIRS`, `K.OWNED_FILES`. Python builders
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

---------------------------------------------------------------------------------------------------

# Implementation and visuals (§13 on)

## 13. Notes on §0 as built

- **Family dispatchers** (`fx/p/<family> {el, …}`, `fx/prop/<family> {el}`, `fx/snd/<family> {el}`,
  `fx/hud/banner_* {el}`): the macro sets `#akPe mb` to `el`, clamps it with a literal score test (1..5 / 3..5 families
  → Geo 5, 1..4 families → `return 0`), then picks the member with **one static line per element**
  (`execute if score #akPe mb matches k run return run function …/<family>/k {args}`). No function name is ever built
  from a macro value, so check_refs / lint_mc / check_macro see every target and a missing member can never be named
  (§1, decision 10). The Python builders route a `'$(..)'` placeholder element through the dispatcher:
  `K.fxe('crown', '$(g)')` → `function …/p/crown {el:$(g)}` (likewise `K.snde`, `K.prope`, `K.hude`); an int element
  still calls the member directly (`K.fxe('crown', 3)` → `…/p/crown/3`).
- **`with storage`**: every macro takes `function … with storage <ns> <path>` arguments (ints for `el`, `nd`, sizes,
  ticks). Sizes are tenths of a block, so a runtime size is an int score `store`d into the storage compound.
- **Extras beyond §0** (additive, nothing renamed): glyph U+E807 `safe` (the safe-circle icon for hint lines),
  preset `p/fire_field {r}` (an ambient flame spot for 33's field rim, not counted as a field card), prop `elump` (the
  element lump of 31 / 33 projectiles), `K.brand_badge(el)` (the "◈낙인" third badge), `fx/test/pair {leg, tail, ph}`
  (sets the demo elements), `K.tele(shape, **args)` (the generic builder behind every `K.tele_*`).
- **Storage keys** of `rlk:azkit` (all removed by `fx/uninstall`): `a` (card args), `t` (telegraph args), `w` (wave /
  lane args), `pr` (preset args after the tenths conversion), `hud`, `ax` (per-kind spin axes), `dm` (demo elements),
  `fd` (field args).
- **Fake players** `#ak*` (objective `mb`), all reset by `fx/uninstall`: `#akN #akTN #akFN` (live counts), `#akNow`
  (stage clock), `#akInit` + the constants `#akK2 #akMinus1 #akK10 #akK15 #akK150 #akK300 #akK1000`, the card
  arguments `#akRoll #akSpin #akLife #akFade #akDly #akDur #akHit #akTel`, telegraph scratch `#akT*`, `#akPe` (family
  element), `#akPar` (2-t particle phase), `#akWw<id> #akWh<id>` (wave widths / holds, id 0-7) and the wave scratch
  `#akWd #akWid #akWl`, `#akA #akB #akC2` (engine scratch), `#akHudV` (HUD), the test / demo clocks `#akMT #akDemo #akDT`.

## 14. Card engine

The fg kit's engine (`S:mb3/fg_fx_api.md` §2) renamed `fk` → `ak`: one `item_display` per card, summoned with scale 0,
its stage snapshots on the item (`custom_data.akS` show, `akG` main interpolation, `akF` fade, `akC` the hit colour).
The stage clock is `time query gametime` + 1 (the fg first-tick fix: a card made in the tick's functions shows on the
next client frame, not one tick late). Scores per card: `akS` show tick, `akG` go tick, `akH` hit tick, `akK` fade
tick, `akD` death tick. `fx/e/world` (a `schedule … 1t replace` chain started by the first card, no tick hook) ages every
card (`fx/e/age`: show → go → hit recolour → fade → kill), refreshes the three counts and emits the safe-beam particle
columns every 2 t; it stops itself when no card is left. A dead / reviving player (`dead=1`, `rnDie≥1`) clears
everything (`fx/clear`).

| planes | local frame (display axes: +x left, +y up, +z forward) |
|---|---|
| `face` | a vertical quad in x-y (billboards use it) |
| `flat` | a floor quad in x-z (telegraphs, fields, cracks) |
| `cross` | two vertical quads (x-y and z-y) |
| `band` | a flat strip plus a 0.5-b wall on its far edge (fronts) |
| `box` | a cuboid with the texture on all six faces (`slab` 1.0 × 0.27 × 0.4, `stele` 0.7 × 2.0 × 0.24 at scale 1) |
| `prism` | eight 1.5-b walls on a 1-b octagon (the seal prism) |

`spin` turns about local y for `flat cross band box prism` and about z for `face`. Caps: `card` / `cardx` skip while
`#akN ≥ 64`; telegraph calls skip when `#akTN ≥ 34` (so a shape of ≤ 6 cards never half-draws
under the 40 cap); the field pool has its own `#akFN < 16`; ambient presets skip from `#akN ≥ 40`.

### 14.1 Kinds (105 sprites, `rlk:mboss/az_kit/<kind>`)

Sprites are painted by `mboss_az_fx_paint.py` (stdlib only, deterministic), sides multiples of 16 and ≤ 512,
full-bright, tinted through `custom_model_data.colors[0]` (`16777215` = the painted colours). "Neutral" sprites are
white / grey and take the element tint; element sprites carry their own colours.

| kind | plane | px | look |
|---|---|---|---|
| `glow` | face | 64x64 | soft white glow disc |
| `glint` | face | 32x32 | white 4-point glint |
| `mote` | face | 16x16 | soft mote (embers, motes, frost glints) |
| `streak` | face | 128x16 | long thin streak along a |
| `ripple` | flat | 128x128 | ripple / shock ring (unit radius) |
| `spark` | face | 32x32 | spark star |
| `beam` | cross | 32x128 | light beam / column, foot at b 0 |
| `vortex` | flat | 64x64 | absorb vortex swirl (unit radius) |
| `cracks` | flat | 128x128 | radial floor cracks (unit radius) |
| `crackfan` | flat | 64x64 | crack fan from the apex forward, about +-32 degrees |
| `blade` | face | 32x64 | translucent crystal blade |
| `dust` | face | 64x64 | dust puff (toon cloud) |
| `arc` | face | 64x32 | electric arc |
| `crystal` | cross | 64x128 | arena crystal cluster, foot at b 0 |
| `water` | flat | 128x128 | shallow-water sheet tile (seamless) |
| `boulder` | face | 32x32 | dark boulder / rubble chunk |
| `slab` | box | 32x32 | rock slab with a gold crack rim (box 1 x 0.27 x 0.4) |
| `mound` | face | 64x32 | dust mound, foot at b 0 |
| `cone` | face | 32x64 | stone cone, foot at b 0 |
| `leaf` | face | 16x16 | orange tail leaf |
| `gold_leaf` | face | 16x16 | gold leaf |
| `splash` | face | 64x64 | water splash crown, foot at b 0 |
| `geyser` | cross | 32x128 | water geyser column, foot at b 0 |
| `orb` | face | 64x64 | 격류 범람 Hydro orb |
| `flame` | face | 32x64 | flame tongue, root at b 0 |
| `fire_dome` | face | 64x32 | impact fire dome (half dome, pivot at the base) |
| `lava` | face | 32x32 | molten rock lump |
| `meteor` | face | 64x96 | 운석 meteor: molten head at the bottom, flame trail up |
| `smoke` | face | 64x64 | smoke / steam puff |
| `ice_spike` | cross | 32x64 | ice crystal spike, foot at b 0 |
| `frost` | face | 32x32 | frost mist puff |
| `icicle` | cross | 16x64 | ice lance, tip at +b |
| `ice_sphere` | face | 64x64 | 쏟아지는 천화 spiky ice sphere |
| `bolt` | face | 32x128 | lightning bolt, foot at b 0 |
| `shell` | face | 64x64 | 번개의 가루 shell |
| `spike_geo` | cross | 32x128 | Geo 천동만상 spike, tip at +b |
| `spike_cryo` | cross | 32x128 | Cryo dark spike, tip at +b |
| `spike_electro` | cross | 32x128 | Electro spike, tip at +b |
| `stele` | box | 32x64 | intro seal stele (box 0.7 x 2 x 0.24) |
| `prism` | prism | 64x64 | intro seal prism (8 walls, radius 1, height 1.5) |
| `gate_icon` | face | 64x64 | gate label icon |
| `cure_burst` | face | 64x64 | cleanse burst sphere |
| `sigil_pyro` | face | 64x64 | absorb sigil (pyro) |
| `glyph_pyro` | face | 64x64 | stele / arrival glyph (pyro) |
| `front_pyro` | band | 64x64 | wave front band segment (pyro) |
| `sigil_hydro` | face | 64x64 | absorb sigil (hydro) |
| `glyph_hydro` | face | 64x64 | stele / arrival glyph (hydro) |
| `front_hydro` | band | 64x64 | wave front band segment (hydro) |
| `sigil_electro` | face | 64x64 | absorb sigil (electro) |
| `glyph_electro` | face | 64x64 | stele / arrival glyph (electro) |
| `front_electro` | band | 64x64 | wave front band segment (electro) |
| `sigil_cryo` | face | 64x64 | absorb sigil (cryo) |
| `glyph_cryo` | face | 64x64 | stele / arrival glyph (cryo) |
| `front_cryo` | band | 64x64 | wave front band segment (cryo) |
| `sigil_geo` | face | 64x64 | absorb sigil (geo) |
| `glyph_geo` | face | 64x64 | stele / arrival glyph (geo) |
| `front_geo` | band | 64x64 | wave front band segment (geo) |
| `rune_pyro` | face | 64x64 | brand rune (pyro) |
| `shard_pyro` | face | 32x64 | 응결 결정 (pyro) |
| `rune_hydro` | face | 64x64 | brand rune (hydro) |
| `shard_hydro` | face | 32x64 | 응결 결정 (hydro) |
| `rune_electro` | face | 64x64 | brand rune (electro) |
| `shard_electro` | face | 32x64 | 응결 결정 (electro) |
| `rune_cryo` | face | 64x64 | brand rune (cryo) |
| `shard_cryo` | face | 32x64 | 응결 결정 (cryo) |
| `t_rim` | flat | 128x128 | telegraph rim, unit radius |
| `t_rim_s` | flat | 64x64 | thick telegraph rim (r <= 2.5) |
| `t_ring` | flat | 192x192 | thin travelling ring (fronts, halo) |
| `t_fill` | flat | 128x128 | telegraph progress fill, unit radius |
| `t_bar` | flat | 16x64 | lane rail / cap bar |
| `t_lane` | flat | 64x64 | lane progress fill, unit length |
| `t_frame` | flat | 32x128 | strip outline (field pool) |
| `t_sf15` | flat | 32x128 | 15-degree slice fill |
| `t_sf30` | flat | 64x128 | 30-degree slice fill |
| `t_sa30` | flat | 64x128 | 30-degree slice arc rim |
| `t_nd` | flat | 64x64 | undodgeable 回 mark (tinted red-amber) |
| `t_ndj` | flat | 64x64 | undodgeable + jump chevron mark |
| `t_hept` | flat | 192x192 | 서리 습격 heptagram {7/2} + 大巛 rune |
| `t_hex` | flat | 128x128 | 번개 가시 hexagram + 번개 rune |
| `t_star` | flat | 128x128 | 얼음 가시 star seal + rune |
| `t_seal8` | flat | 128x128 | 운석 seal: two squares + 火 runes |
| `t_mask` | flat | 128x128 | 벼락 습격 violet strike wash |
| `t_safe` | flat | 64x64 | 벼락 습격 safe circle (rim + glyph) |
| `t_crater` | flat | 64x64 | B3 crater (also the crater prop) |
| `t_wall` | face | 64x32 | dust wall on a flank strip rail |
| `t_gcircle` | flat | 128x128 | intro seal gold floor glyph circle |
| `t_sa15` | flat | 32x128 | 15-degree slice arc rim |
| `t_sa15l` | flat | 32x128 | 15-degree slice arc rim + edge l |
| `t_sa15r` | flat | 32x128 | 15-degree slice arc rim + edge r |
| `t_sa15b` | flat | 32x128 | 15-degree slice arc rim + edge b |
| `t_bo25` | flat | 32x128 | annular 15-degree fill, inner 0.25 (outer band) |
| `t_bi25` | flat | 32x128 | annular 15-degree fill, inner 0.25 (inner band) |
| `t_bo50` | flat | 32x128 | annular 15-degree fill, inner 0.5 (outer band) |
| `t_bi50` | flat | 32x128 | annular 15-degree fill, inner 0.5 (inner band) |
| `t_bo71` | flat | 32x128 | annular 15-degree fill, inner 0.7071 (outer band) |
| `t_bi71` | flat | 32x128 | annular 15-degree fill, inner 0.7071 (inner band) |
| `t_bo84` | flat | 32x128 | annular 15-degree fill, inner 0.8409 (outer band) |
| `t_bi84` | flat | 32x128 | annular 15-degree fill, inner 0.8409 (inner band) |
| `fld1` | flat | 64x64 | lingering field disc (pyro) |
| `fld2` | flat | 64x64 | lingering field disc (hydro) |
| `fld3` | flat | 64x64 | lingering field disc (electro) |
| `fld4` | flat | 64x64 | lingering field disc (cryo) |
| `fld5` | flat | 64x64 | lingering field disc (geo) |
| `fst3` | flat | 32x128 | lingering strip (electro) |
| `fst4` | flat | 32x128 | lingering strip (cryo) |

## 15. Telegraphs

| function | macro args | Python |
|---|---|---|
| `tele/disc` | {r, tell, el, nd, hold} | `K.tele_disc` |
| `tele/ring` | {r0, r, tell, el, nd, hold} | `K.tele_ring` |
| `tele/sector` | {r, a, tell, el, nd, hold} | `K.tele_sector` |
| `tele/wedge` | {r0, r1, a0, a1, tell, el, nd, hold} | `K.tele_wedge` |
| `tele/line` | {len, w, back, tell, el, nd, hold} | `K.tele_line` |
| `tele/lane_side` | {len, w, back, tell, el, hold} | `K.tele_lane_side` |
| `tele/wave` | {id, r0, r1, w, tell, dur, el, nd, hold} | `K.tele_wave` |
| `tele/wave_to` | {id, r, dur} | `K.tele_wave_to` |
| `tele/wave_end` | {id} | `K.tele_wave_end` |
| `tele/mline` | {id, len, w, back, tell, el, nd, hold} | `K.tele_mline` |
| `tele/mline_aim` | {id} | `K.tele_mline_aim` |
| `tele/mline_turn` | {id, d} | `K.tele_mline_turn` |
| `tele/mline_end` | {id} | `K.tele_mline_end` |
| `tele/heptagram` | {r, tell, el, hold} | `K.tele_heptagram` |
| `tele/hexagram` | {r, tell, el, hold} | `K.tele_hexagram` |
| `tele/starseal` | {r, tell, el, hold} | `K.tele_starseal` |
| `tele/seal8` | {r, tell, el, hold} | `K.tele_seal8` |
| `tele/mask_wash` | {r, tell, hold} | `K.tele_mask_wash` |
| `tele/safe_rim` | {id, r, tell, hold} | `K.tele_safe_rim` |
| `tele/safe_beam` | {id} | `K.tele_safe_beam` |
| `tele/safe_end` | {id} | `K.tele_safe_end` |
| `tele/crater` | {r, tell, hold} | `K.tele_crater` |
| `tele/halo` | {r, h, tell, el, hold} | `K.tele_halo` |
| `tele/glyph_circle` | {r, tell, hold} | `K.tele_glyph_circle` |
| `tele/field` | {id, r, el, life} | `K.tele_field` |
| `tele/strip` | {id, len, w, yaw, el, life} | `K.tele_strip` |
| `tele/field_end` | {id} | `K.tele_field_end` |
| `tele/field_clear` | — | `K.tele_field_clear` |
| `tele/clear` | — | `K.tele_clear` |

### 15.1 Palettes and the undodgeable look

| el | name | rim | fill | flash |
|---|---|---|---|---|
| 0 | physical | #E5304A | #FF6474 | #FFB8C4 |
| 1 | Pyro | #C8461E | #FF8A3D | #FFD2A0 |
| 2 | Hydro | #1E6FC8 | #4FB8FF | #CDEBFF |
| 3 | Electro | #6A3FC8 | #C58BFF | #EEDDFF |
| 4 | Cryo | #3AA6C0 | #9FE8F5 | #E8FBFF |
| 5 | Geo | #D27A0C | #F0A93A | #FFE8A0 |
| 6 | Geo | #D27A0C | #F0A93A | #FFE8A0 |
| 7 | Geo | #D27A0C | #F0A93A | #FFE8A0 |
| 8 | Geo | #D27A0C | #F0A93A | #FFE8A0 |

Rims use the rim colour, fills the fill colour (translucent painted fills), and every card of a shape turns to the
flash colour on the hit tick. `nd 1`: the rims turn `#FF5A1E` and a 回 card (`t_nd`: a 回 glyph inside a diamond,
white core and dark outline, tinted `#FF5A1E`) sits at the decal centre (lines / lanes: one every ~4 b; waves: four riding the front; wedges: one per ~4 b of
a union). `nd 2`: the 回 card carries the jump chevron (`t_ndj`), and on waves the chevrons point outward. Safe
circles are green (`#2FCF5E`, flash `#B8FFC8`), the 42 wash violet (Electro).

### 15.2 Shapes (cards, growth, layering)

Layering above the floor point: water sheet +0.005 (arena), field pool fill +0.03 / rim +0.033, mask wash +0.03, attack
fills +0.035, rims +0.045, wave rings +0.048 / +0.05, glyph and 回 cards +0.05.

- **disc** `{r, tell, el, nd, hold}`: rim card at r (`t_rim`; `t_rim_s`, a thicker line, for r ≤ 2.5 b), fill
  card (`t_fill`) growing 0 → r over the tell; 2 cards (+1 with nd).
- **ring** `{r0, r, …}`: outer and inner rims and a progress ring (`t_ring`) growing r0 → r; 3 cards (+1 with nd on the
  band straight ahead).
- **sector** `{r, a, …}`: `a` (half-angle) snaps to 7.5° steps; n15 = round(a / 7.5) slices of 15° (`t_sf15` fill +
  `t_sa15` rim; the outermost slices use `t_sa15l` / `t_sa15r` / `t_sa15b` with the radial edges). n15 > 13: 30° slices
  (`t_sf30` / `t_sa30`) and two edge bars (`t_bar`). `a ≥ 175`: a disc. ≤ 26 cards.
- **wedge** `{r0, r1, a0, a1, …}` (the P7 union, §3.1): span Δ = a1 − a0 (1..180) drawn as m = ⌈Δ / 15⌉ slices of the
  15° textures squeezed to Δ / m (x-scale k = span / 15 per slice, never smaller than the nominal angle), 30° slices
  beyond 105°. Rims are the arc-only `t_sa15` / `t_sa30` (no radial edges), so consecutive wedges of a union join
  without seams. **Annular** (r0 > 0): two band fills per slice, the outer `t_bo<ρ>` with the leading edge, the inner
  `t_bi<ρ>` plain, ρ ∈ {0.25, 0.5, 0.7071, 0.8409} chosen from q = r0 / r1 (q ≤ 0.062 draws from the apex); limits
  r0 / r1 ∈ [0.0625, 0.84] and Δ ≤ 105 for annular wedges. The 回 card sits at the mid angle and mid radius unless
  another 回 card is within 3.9 b. ≤ 14 cards for r0 = 0.
- **line** `{len, w, back, …}`: −back..len along the aim (negative back starts beyond the point), two rails (`t_bar`),
  two caps, a lane fill (`t_lane`) growing toward the far end; 5 cards (+ 回 every ~4 b with nd).
- **lane_side** `{len, w, back, tell, el, hold}`: a line in the nd 1 look plus a standing dust wall (`t_wall`) on the
  **outer rail = the executor's left (+x)**: run the left flank's strip rotated as the body axis, the right flank's
  rotated 180° from its front end. 5 cards + 回 cards.
- **wave** `{id, r0, r1, w, tell, dur, …}`: a disc fills to r0 over the tell and flashes on the strike tick; from the end
  of the strike tick the front ring (`t_ring`) travels r0 → r1 in dur ticks with the band edge w behind it, so the
  drawn front equals the hazard front r0 + spd × (T − strike) every tick; it then stays `hold` ticks. **wave_to**
  `{id, r, dur}` merges new targets into the live ring, band edge and riding 回 cards (`data merge entity`,
  `start_interpolation 0`) and extends the life to now + dur + hold + 1 — call it at each linear segment boundary of an
  eased front. **wave_end** `{id}` removes it; calling `wave` with a live id replaces it. 4 cards (8 with nd).
- **mline** `{id, len, w, back, …}`: a line whose cards all sit on the pivot with their offsets in their own
  transformation (`teleport_duration 1`, tag `rlk_ak_ml<id>`), so `mline_aim {id}` (run rotated as the new aim) or
  `mline_turn {id, d}` (+ = clockwise from above) turns the whole lane smoothly; `mline_end {id}` removes it.
- **heptagram / hexagram / starseal / seal8** `{r, tell, el, hold}`: the seal art (`t_hept` {7/2} with meander tips and
  the 大巛 rune, `t_hex` with the 번개 rune, `t_star` {8/3} with the ❄ rune, `t_seal8` two squares with the 火 runes)
  pops in at r, the progress fill grows 0 → r, a rim marks the hit radius; 3 cards. Default `el`: 4 / 3 / 4 / 1.
- **mask_wash** `{r, tell, hold}`: one violet card (`t_mask`, 128 px) growing 0.3 r → r. **safe_rim** `{id, r, tell,
  hold}`: one green card (`t_safe`, ring + shield glyph), tag `rlk_ak_sr<id>`; **safe_beam** `{id}` adds a particle
  column emitted by the ager every 2 t; **safe_end** `{id}`. A 42 round = 1 wash + 5 rims = 6 cards.
- **crater** `{r, tell, hold}`: the rubble crater (`t_crater`) grows 0.4 r → r with a dark Geo rim; 2 cards.
  **halo** `{r, h, tell, el, hold}`: a thin ring h above the landing spot shrinking 2 r → r, flashing on impact; 1 card.
  **glyph_circle** `{r, tell, hold}`: the intro's gold floor glyph circle (`t_gcircle`) growing 0.6 r → r with a gold
  rim and an inner ring; 3 cards; decor only.
- **clear**: every attack telegraph, lane, wave, rim, wash, crater, halo and glyph circle; fx cards and the field pool
  stay.

### 15.3 Field pool

`tele/field {id, r, el, life}`: a painted element fill (`fld1` Pyro fire ring with embers, `fld2` Hydro pool with
ripples, `fld3` Electro crackle, `fld4` Cryo frost seal with the 大巛 rune, `fld5` Geo cracks) + a tinted rim, at
+0.03 / +0.033; `tele/strip {id, len, w, yaw, el, life}`: Electro `fst3` / Cryo `fst4` (other elements a tinted
`t_lane`) + a `t_frame` outline, from the executing point along the absolute world yaw (`execute rotated $(yaw) 0`).
Tagged `rlk_ak_fp` + `rlk_ak_f<id>`; counted in `#akFN` only (never in `#akN` / `#akTN`); calling an id again redraws
it; `tele/clear` leaves the pool alone; `field_end {id}` / `field_clear` remove it.

## 16. Presets

Sizes in tenths of a block, ticks as ints (`K.fx` / `K.fxe` take blocks and convert). Every preset converts its args
once into storage `pr` (floats plus derived placeholders `<arg>_<pct>` / `<arg>_m<pct>` = ± pct % of a size,
`<arg>_p<k>` = a tick + k) and runs its worker `fx/p/e/<name>` (`fx/p/e/<name>_<el>` for family members) with that
storage. Card counts are the cards one call makes (all expire within 120 t).

### 16.1 Element families (`fx/p/<name>/<el>`, el 1..5; dispatcher `fx/p/<name> {el, …}`)

| family | args | cards Pyro / Hydro / Electro / Cryo / Geo | does |
|---|---|---|---|
| `p/impact/<el>` | — | 8 / 7 / 7 / 10 / 12 | Impact burst at the floor point: Geo crystal-blade crown, Hydro splash, Pyro flame dome, Cryo ice spikes, Electro bolt and arcs; a flash and a shock ripple. |
| `p/cracks/<el>` | r | 5 / 3 / 4 / 5 / 5 | Crack fan along the executor yaw over radius {r} (tenths): glowing cracks in the element colour (Geo gold, Hydro white-cyan, Pyro lava, Cryo frost, Electro violet) with debris. At the impact point, rotated as the crack line. |
| `p/crown/<el>` | — | 11 / 11 / 11 / 11 / 11 | Blade crown burst (P1 / the blade crowns): 10 element blades erupting out-and-up (Geo gold crystal, Hydro water, Pyro flame, Cryo ice, Electro violet crystal). At the floor point. |
| `p/dust_ring/<el>` | r | 9 / 9 / 9 / 9 / 9 | Ring of element dust around the point at radius {r} (tenths): Geo khaki dust, Hydro spray, Pyro embers and smoke, Cryo frost, Electro sparks; a ripple out to r. |
| `p/slab_throw/<el>` | — | 3 / 3 / 3 / 3 / 3 | Slab / boulder throw streaks (at the slab, rotated along the throw): speed streaks behind it and a trail in the element (Geo grit, Hydro water, Pyro embers, Cryo frost, Electro sparks). |
| `p/footfall/<el>` | — | 3 / 2 / 2 / 2 / 2 | Footfall at a planted foot (walk / turn plant events, plan §2.6): Geo dust, Hydro splash, Pyro flame splash, Cryo frost, Electro sparks. |
| `p/brand_rune/<el>` | — | 1 / 1 / 1 / 1 / 1 | The brand rune over the player's chest (call every 4 t at the chest): the element rune card (Pyro ")火(", Hydro "ccc / \|\|\|", Electro square rune, Cryo "大巛"; Geo draws its sigil), life 5 t. |
| `p/vortex/<el>` | t | 3 / 3 / 3 / 3 / 3 | Absorb vortex for {t} ticks around the body: a floor vortex spinning in, a smaller one at the chest, the element particles drawn inward (v4 A water vortex, v5 A Pyro swirl, v6 A Electro orb, v7 C Cryo). |
| `p/recolour/<el>` | r, t | 3 / 3 / 3 / 3 / 3 | The recolour wave from the boss outward to {r} (tenths) over {t} ticks (absorb bursts, plan §2.6): an element ripple and a glow band sweeping the floor. |
| `p/sigils/<el>` | — | 6 / 6 / 6 / 6 / 6 | Sigil cards around the body for the absorb (火 / 水 / ⚡ / ❄ / Geo emblem): six sigils rising and turning at 3-6 b (v5 A, v5 §4.2). |
| `p/front/<el>` | r0, r1, w, dur | 12 / 12 / 12 / 12 / 12 | The 3-D wave front (N10) moving with tele/wave: 12 band segments (element strip + wall: Geo dust and slabs, Hydro water wall, Pyro fire wall, Cryo frost, Electro sparks) travel from {r0} to {r1} in {dur} ticks keeping {w} deep (tenths / ticks). Call it on the tick BEFORE the strike (the fg wave_band rule). At the floor centre. |
| `p/dig/<el>` | — | 6 / 5 / 7 / 5 / 7 | B3 dig in place: dust mounds and debris with the element (Geo slabs, Hydro water, Pyro embers, Cryo ice puffs, Electro violet slabs). At the body's floor point. |
| `p/flank_blades/<el>` | len | 6 / 6 / 6 / 6 / 6 | P6 element blades out-and-up along a flank strip of length {len} (tenths) from the point along the executor's forward axis, leaning to its left (+x, the outer side): Geo gold blades, Hydro water jets, Pyro flames, Cryo ice spikes, Electro violet crystals. |
| `p/spike_line/<el>` | len | 6 / 6 / 6 / 6 / 6 | P8 spike line along the aim, length {len} (tenths): six element spikes bursting from the floor one after another (Geo gold blades, Hydro jets, Pyro flames, Cryo ice spikes, Electro crystals). |
| `p/shard_rain/<el>` | r, t | 8 / 8 / 8 / 8 / 8 | Absorb-2 cosmetic shard rain over radius {r} (tenths) for {t} ticks: falling element shards (Geo gold, Hydro drops, Pyro embers, Cryo icicles, Electro bolts) spread over the window. At the arena centre. |

### 16.2 Named presets

| preset | args (tenths / ticks) | cards | ambient | does |
|---|---|---|---|---|
| `p/geyser` | — | 3 |  | P1 Hydro geyser (the chin addon): a water column erupting with spray and a ripple. At the floor point. |
| `p/blade_trail` | — | 1 | yes | Hydro water-blade trail (at the blade prop, every 2 t): a short water streak and spray. |
| `p/lump_trail` | — | 2 | yes | Pyro lump trail (at a flying lump, every 2 t): a flame lick and smoke. |
| `p/meteor_big` | h | 3 |  | 32 big meteor fall: the molten meteor drops from {h} (tenths) above onto the floor point in 6 t with a flame trail and a darkening floor glow. |
| `p/meteor_small` | h | 2 |  | 32 small meteor fall from {h} (tenths) in 4 t with a short flame trail. |
| `p/fire_dome` | r | 9 |  | 32 meteor impact: a fire dome of radius {r} (tenths) with flame tongues, a flash and a fire ring. At the floor point. |
| `p/frost_burst` | r | 12 |  | Cryo frost burst of radius {r} (tenths; Cryo rings, 41 bursts): a ring of ice spikes, frost mist and a white flash. At the floor point. |
| `p/ice_wall` | — | 4 |  | P7 Cryo ice-wall piece (on the swept arc): three tall ice spikes in a short row along the executor's left-right axis, frost. At the floor point, rotated along the arc. |
| `p/hail` | r | 3 | yes | Hail falling in a field of radius {r} (tenths; ambient, call every 5-10 t): three ice pellets, snow. |
| `p/bolt` | — | 3 |  | A single Electro sky bolt onto the floor point: the bolt, a flash, a spark and a scorch ripple. |
| `p/bolt_round` | r | 12 |  | 42 floor-wide crackle over radius {r} (tenths): two waves of six bolts 8 t apart at spread points. At the arena centre. |
| `p/shell_dive` | — | 5 |  | 44 shell impact: a violet dome flash, arcs and a crackle ring. At the floor point. |
| `p/icicle_trail` | — | 2 | yes | Icicle / lance trail (at the icicle, every 2 t; 41, 43): frost motes and a pale streak. |
| `p/ice_sphere` | — | 2 | yes | 43 ice-sphere aura (at the sphere prop, every 4-6 t): frost glints and snow around it. |
| `p/orb_ribbon` | — | 2 | yes | 31 orb ribbon (at an orb, every 2 t): a water ribbon streak and a drop. |
| `p/spark_column` | h | 4 |  | 44 tell: a violet spark column {h} (tenths) tall from the tail tip with crawling arcs. At the tip, foot of the column. |
| `p/stele_shatter` | — | 9 |  | E a seal stele shatters: red-brown chunks flung out, dust and a gold crack flash. At the stele foot. |
| `p/prism_shatter` | — | 14 |  | E the seal prism shatters (t112): gold glass blades burst outward from the prism, a white flash and a gold ring. At the prism centre (floor). |
| `p/seal_reform` | — | 9 |  | D the seal re-forms around the dying body: gold glass blades converging inward, a gold glow and rising motes. At the body's floor point. |
| `p/petrify_pulse` | — | 3 |  | D petrify pulse (the rig turns to stone): a grey-gold ripple and dust. At the body's floor point. |
| `p/splash` | — | 2 |  | Water step splash (Hydro walk, water-sheet impacts): a small splash and ripple. |
| `p/splash_wall` | r | 10 |  | P5b Hydro splash wall at the ring edge of radius {r} (tenths): ten water walls rising around the paw point. |
| `p/dust` | — | 3 |  | P9 dust puff (rock rings, rush trails): three khaki dust clouds. At the floor point. |
| `p/rock_rain` | r | 6 |  | P9 rock rain: six rocks falling from above within radius {r} (tenths), dust. At the floor point. |
| `p/mound` | — | 3 |  | P9 / B3 dust mound plume at the dig / surfacing point. |
| `p/light_shaft` | — | 2 |  | P9 gold light shaft over a rock-ring marker (8 b tall). |
| `p/gold_plume` | — | 7 |  | P4 gold plume (the back flares and the spikes launch): a gold column up, rising glints, dust. At the back (launch point). |
| `p/shard_fall` | h | 2 |  | P4 falling spike shard (the last 4 t before a landing): a dark gold shard dropping from {h} (tenths) with a glowing streak. |
| `p/dust_wall` | len | 5 |  | P6 dust walls along a strip of length {len} (tenths) from the point along the executor's forward axis: five rising cream-gold walls. |
| `p/boulders` | — | 5 |  | P7 boulders thrown up along the swept arc (five rocks fanning out from the point). |
| `p/tail_lane` | — | 4 |  | P7 / P8 tail lane: dust and grit kicked along the tail's path (a streak and puffs along the executor's forward axis, 6 b). |
| `p/leaf_burst` | — | 10 |  | P8 orange leaf burst (the tail's leaves scatter at the impact): ten leaves flung out and up. |
| `p/cones` | — | 5 |  | P8 planted stone cones along the line (five cones from 2 to 12 b, staying 60 t). At the tail root, rotated as the line. |
| `p/skid` | — | 4 |  | P3 skid gouge: a crack fan behind the stop point, dust and slabs kicked forward. |
| `p/dust_trail` | — | 2 | yes | P3 gallop dust (ambient, every 4 t of the run at the body): two dust puffs. |
| `p/shock_dome` | r | 3 |  | Roar shock dome of radius {r} (tenths): a floor ring and a camera-facing ring expanding (v6 roar shock domes, v7 C). |
| `p/emerge_spikes` | r | 12 |  | B3 emergence: an earth-spike cluster of radius {r} (tenths) bursting out of the floor with dust. At the surfacing point. |
| `p/glyph_glow` | — | 2 | yes | Entrance stele / arrival glyph glow (ambient, every 10 t at a glyph): a soft glow and motes. |
| `p/gold_leaves` | — | 12 |  | E the intro roar (t120): twelve gold leaves flung radially from the head height. |
| `p/gold_motes` | — | 3 | yes | Drifting gold motes (arena ambience; ambient, every 20 t at a mote point): three slow motes. |
| `p/cure` | — | 4 |  | The brand cleanse (butterfly-style cure fx, about 16 t): a pale-gold beam down, a white-gold burst and glints. At the player's feet. |
| `p/fire_field` | r | 1 | yes | Fire-field ambience (ambient; every 10-20 t at a live fire field of radius {r} tenths): flames, lava pops and embers over the field (33). |

## 17. Props (`fx/prop/<name>`, as `@s` = a module-owned item_display)

A prop function `data merge`s the item (model + tint), billboard, full brightness, view range and — for props with a
scale — the transformation. **The arena_crystal, water_sheet and glyph families keep the module's transformation**
(the theme record's scale / rotation): they set the item and brightness only. Moving props: keep
`teleport_duration:1` on the entity.

| prop | kind | tint | billboard | scale | look / use |
|---|---|---|---|---|---|
| `prop/seal_stele` | `stele` | #FFFFFF | fixed | [1.6f,1.6f,1.6f] | Intro seal stele (6 at r 8 around the spawn): a dark red-brown carved tablet with glowing gold cracks, 1.1 x 3.2 x 0.4 b standing on the prop (box kind, pivot at its centre: spawn it 1.6 b up). |
| `prop/seal_chunk` | `stele` | #FFFFFF | fixed | [0.9f,0.3f,1.4f] | Seal stele chunk (shatter pieces): a 0.6 b block of the stele stone. |
| `prop/seal_prism` | `prism` | #FFFFFF | fixed | [6f,6f,6f] | Intro seal prism (UUID 0x80): an eight-walled translucent gold glyph prism, radius 6 b, 9 b tall, standing on the prop. |
| `prop/gate_icon` | `gate_icon` | #FFFFFF | vertical | [1f,1f,1f] | The gate label icon (registry icon.model; also the item model rlk:mboss/az_kit/gate_icon), 1 b, turning to the viewer. |
| `prop/orb` | `orb` | #FFFFFF | center | [2.6f,2.6f,2.6f] | 격류 범람 Hydro orb (31): a water sphere 2.6 b across (hz r 1.3), camera-facing; pair with p/orb_ribbon every 2 t. |
| `prop/meteor_big` | `meteor` | #FFFFFF | vertical | [3.6f,3.6f,3.6f] | 운석 낙하 big meteor (32): molten head with a flame trail up, 3.6 b, upright. |
| `prop/meteor_small` | `meteor` | #FFFFFF | vertical | [1.7f,1.7f,1.7f] | 운석 낙하 small meteor (32), 1.7 b, upright. |
| `prop/lump` | `lava` | #FFFFFF | center | [1f,1f,1f] | Pyro molten lump (P1 / P2 / P5 extras), 1 b, camera-facing; pair with p/lump_trail. |
| `prop/elump` | `crystal` | #C58BFF | fixed | [1.4f,1.4f,1.4f] | Electro crystal lump (46), a violet crystal cluster 1.4 b. |
| `prop/shell` | `shell` | #FFFFFF | center | [1.2f,1.2f,1.2f] | 번개의 가루 shell (44): a violet sphere with the square glyph, 1.2 b, camera-facing. |
| `prop/icicle` | `icicle` | #FFFFFF | fixed | kept | Ice lance / icicle (41, 43): tip along the prop's facing (local +z; aim it with tp ... facing), 1.6 b long. |
| `prop/ice_sphere` | `ice_sphere` | #FFFFFF | center | [2.2f,2.2f,2.2f] | 쏟아지는 천화 spiky ice sphere (43), 2.2 b, camera-facing; pair with p/ice_sphere. |
| `prop/cone` | `cone` | #FFFFFF | vertical | [2f,2f,2f] | Planted stone cone (P8), 2 b tall, foot at the prop, upright. |
| `prop/crater` | `t_crater` | #FFFFFF | fixed | [7.5f,1f,7.5f] | B3 crater at the floor cut (UUID 0x81): the rubble crater, radius 7.5 b, flat at the prop (spawn it 0.03 b over the floor). |
| `prop/arena_crystal/<el>` (1..5) | 1: `crystal` #FF7A3A, 2: `crystal` #5EC4FF, 3: `crystal` #B07CFF, 4: `crystal` #A8F2FF, 5: `crystal` #F2C25A |  | kept | kept | Arena crystal cluster in the element look (plan §2.6; theme.md §6.3): pale crystals tinted geo gold / Pyro / Hydro / Electro / Cryo. Keeps the module's transformation (the theme record's scale). |
| `prop/water_sheet/<el>` (1..5) | 1: `water` #FF8A5A, 2: `water` #5AB8F0, 3: `water` #A884F0, 4: `water` #B4F0FF, 5: `water` #C8B080 |  | kept | kept | The 14-b shallow-water tile at y 201.005 in the element look (about 40 % alpha). Keeps the module's transformation (the theme record's scale 14). |
| `prop/glyph/<el>` (1..5) | 1: `glyph_pyro` #FFFFFF, 2: `glyph_hydro` #FFFFFF, 3: `glyph_electro` #FFFFFF, 4: `glyph_cryo` #FFFFFF, 5: `glyph_geo` #FFFFFF |  | kept | kept | Entrance stele / arrival glyph: flame, water curl, bolt, snowflake, Geo emblem (the item models rlk:mboss/az_kit/glyph_<pyro\|hydro\|electro\|cryo\|geo>). Keeps the module's transformation. |
| `prop/spike/<el>` (3..5) | 3: `spike_electro` #FFFFFF, 4: `spike_cryo` #FFFFFF, 5: `spike_geo` #FFFFFF |  | fixed | [2.5f,2.5f,2.5f] | 천동만상 spike (P4 Geo / 45 Cryo / 46 Electro): 2.5 b, tip up at scale 1 (pitch the prop to plant it point first). |
| `prop/shard/<el>` (1..4) | 1: `shard_pyro` #FFFFFF, 2: `shard_hydro` #FFFFFF, 3: `shard_electro` #FFFFFF, 4: `shard_cryo` #FFFFFF |  | center | [1f,1f,1f] | 응결 결정 (the brand shield pickup, plan §4.10-4): a gold-amber crystal with the brand element inside, 1 b, camera-facing. |

Model frames the arena records rely on (S1-ARENA, `az/requests/arena.md` item 4; kept stable):

- `arena_crystal/<el>` (`crystal`, cross plane): base at the display origin, growing along local +y, ≤ 1 b tall per
  scale unit; hanging records use scale `(s, −s, −s)` (a 180° turn about x) with `pos` at the tip.
- `water_sheet/<el>` (`water`, flat plane): a horizontal 1 × 1 plane centred on the origin (scale 14 = one 14-b tile),
  drawn at the record's y 201.005, about 40 % alpha. It is already horizontal: no left_rotation.
- `glyph/<el>` (`glyph_<el>`, face plane): a vertical plane centred on the origin facing the record's yaw (yaw 180 = the
  plane faces −z), about 1 b per scale unit.
- Every card and prop is full bright (`brightness {sky:15, block:15}`): the cavern's floor-level block light is 3-4.

## 18. HUD (font `rlk:mboss_az`, U+E800-E8FF)

| codepoint | K.glyph name | texture | height | ascent | look |
|---|---|---|---|---|---|
| U+E800 | `badge` | 36x36 | 8 | 7 | painted |
| U+E801 | `brand` | 36x36 | 9 | 8 | painted |
| U+E802 | `el_pyro` | 36x36 | 9 | 8 | painted |
| U+E803 | `el_hydro` | 36x36 | 9 | 8 | painted |
| U+E804 | `el_electro` | 36x36 | 9 | 8 | painted |
| U+E805 | `el_cryo` | 36x36 | 9 | 8 | painted |
| U+E806 | `el_geo` | 36x36 | 9 | 8 | painted |
| U+E807 | `safe` | 36x36 | 9 | 8 | painted |
| U+E810 | `fl_white` | 16x9 | 144 | 69 | flat #FFFFFF alpha 0.92 |
| U+E811 | `fl_gold` | 16x9 | 144 | 69 | flat #F9DFAD alpha 0.55 |
| U+E812 | `fl_amber` | 16x9 | 144 | 69 | flat #E6A55F alpha 0.45 |
| U+E813 | `fl_violet` | 16x9 | 144 | 69 | flat #8F64E8 alpha 0.45 |
| U+E820 | `jump` | 128x64 | 32 | 22 | painted |
| U+E821 | `chevron` | 36x36 | 9 | 8 | painted |
| U+E822 | `hui` | 36x36 | 9 | 8 | painted |
| U+E840 | `orn_l` | 64x32 | 8 | 7 | painted |
| U+E841 | `orn_r` | 64x32 | 8 | 7 | painted |
| U+E8F0 | `sp_neg1` |  |  |  | space −1 |
| U+E8F1 | `sp_two` |  |  |  | space +2 |
| U+E8F2 | `sp_one` |  |  |  | space +1 |

- **Banners** `hud/banner_tr|ab|ab2|brand/<el>` (el 1..4: 불 / 물 / 번개 / 얼음): one actionbar line with the
  ornaments U+E840 / U+E841 and the element icon, held with `hudHold` 60 / 60 / 80 / 100 t so the regular actionbar HUD
  does not overwrite it. **No sound** (the caller plays `snd/msg_chime` or an absorb recipe). `hud/banner_end` drops it.
- **Cue** `hud/cue_jump`: the "점프!" glyph (U+E820, 128 × 64 painted, height 32) on the title line for 12 t
  (`title times 0 9 3`), with the chevron subtitle; it sets `vBig 14` so the F5 crosshair title rests meanwhile.
  `hud/cue_end` drops it.
- **Flashes** `hud/flash_white|gold|amber|violet`: a full-screen glyph (U+E810-E813, height 144) on the title line
  (`title times 0 2 5`); `hud/flash_end`; `hud/clear` = everything off.
- **Name / sub lines** are the core's: `K.badge(el, lit)` → `◈물` dim `#707070` until lit, then the element colour;
  `K.brand_badge(el)` → `◈낙인` in the element colour; `K.glyph(name)` → the character (use it with font `rlk:mboss_az`).
- The generator refuses to write the font if any codepoint of U+E800-E8FF is defined in another
  `assets/*/font/*.json` (Apep's kit uses U+E900-E9FF).

## 19. Sound recipes (`fx/snd/<name>`; vanilla events only)

Each layer is `playsound <event> hostile @a[tag=player] ~ ~ ~ <volume> <pitch> <minVolume>` with the mboss_lib
per-layer minimum-volume rule; pitches 0.5-2.0; no player / villager voices. Family dispatchers: `snd/footfall {el}`
(out of range → Geo), `snd/absorb_vortex|absorb_burst {el}` (out of range → nothing).

| recipe | row | layers (event volume/pitch) |
|---|---|---|
| `snd/chin_rear` | P1 rear-up (t0..t10): a deep roar and growl. | entity.ravager.roar 1/0.6; entity.ender_dragon.growl 0.5/0.7 |
| `snd/chin_impact` | P1 impact t35: heavy smash, boom and crystal crack. | item.mace.smash_ground_heavy 1/0.5; entity.generic.explode 1/0.5; block.amethyst_cluster.break 1/0.6 |
| `snd/jump_takeoff` | P2 take-off t6: a heave and a whoosh. | entity.ravager.attack 1/0.5; item.trident.riptide_3 0.5/0.5 |
| `snd/jump_land` | P2 landing t21: smash, boom, anvil. | item.mace.smash_ground_heavy 1/0.6; entity.generic.explode 1/0.6; block.anvil.land 0.5/0.5 |
| `snd/jump_wave2` | P2 second ground wave t32: deep crack and falling stone. | block.deepslate.break 1/0.5; block.pointed_dripstone.land 1/0.6 |
| `snd/charge_growl` | P3 growl and coil (t0): roar + growl. | entity.ravager.roar 1/0.6; entity.ender_dragon.growl 0.5/0.8 |
| `snd/charge_gallop` | P3 gallop step (every 4 t of the run): heavy steps and gravel. | entity.ravager.step 1/0.5; entity.iron_golem.step 1/0.5; block.gravel.break 1/0.6 |
| `snd/charge_skid` | P3 skid stop: gravel scrape and grind. | block.gravel.hit 1/0.5; block.grindstone.use 1/0.5 |
| `snd/spikes_bristle` | P4 bristle (t0, gold glow): charge hum. | entity.breeze.charge 1/0.6; block.respawn_anchor.charge 1/0.7 |
| `snd/spikes_launch` | P4 launch t14: four rockets of spikes. | entity.blaze.shoot 1/0.5; entity.firework_rocket.launch 1/0.6; entity.firework_rocket.launch 0.8/0.65; entity.firework_rocket.launch 0.7/0.55; entity.firework_rocket.launch 0.6/0.7 |
| `snd/spikes_land` | P4 spike landing: crack, dripstone thud, crystal. | entity.generic.explode 0.5/1.2; block.pointed_dripstone.land 1/1; block.amethyst_cluster.break 1/0.8 |
| `snd/spikes_explode` | P4 planted spike explodes: boom and crystal. | entity.generic.explode 1/1; block.amethyst_block.break 1/1 |
| `snd/stomp_slam` | P5 / P5b paw slam: boom, golem thud, crystal. | entity.generic.explode 1/0.6; entity.iron_golem.damage 1/0.5; block.amethyst_block.break 1/1 |
| `snd/stomp_wave` | P5 / P5b ground wave: deplete thrum and a sonic charge. | block.respawn_anchor.deplete 1/0.6; entity.warden.sonic_charge 0.3/1.4 |
| `snd/feint_sway` | P6 sway (call twice): heartbeat and a heavy step. | entity.warden.heartbeat 1/0.6; block.deepslate.step 1/1 |
| `snd/feint_burst` | P6 flank eruption t22: boom, crystal, basalt. | entity.generic.explode 1/0.9; block.amethyst_block.break 1/0.6; block.basalt.break 1/0.8; block.basalt.break 1/0.9; block.basalt.break 0.9/1; block.basalt.break 0.8/0.7 |
| `snd/whip_raise` | P7 tail raise: a low rumble. | entity.warden.ambient 0.4/0.6 |
| `snd/whip_sweep` | P7 sweep t23: a wind burst and a riptide whoosh. | entity.breeze.wind_burst 1/0.6; item.trident.riptide_3 0.6/0.7 |
| `snd/whip_erupt` | P7 end-line eruption t33: boom and crystal. | entity.generic.explode 1/1; block.amethyst_cluster.break 1/1 |
| `snd/tslam_raise` | P8 tail raised high: dripping lava tick and a rumble. | block.pointed_dripstone.drip_lava 1/1; entity.warden.ambient 0.6/0.8 |
| `snd/tslam_impact` | P8 impact t39: boom, anvil, three dripstone thuds, leaves. | entity.generic.explode 1/0.6; block.anvil.land 0.5/0.5; block.pointed_dripstone.land 1/0.9; block.pointed_dripstone.land 0.9/1.1; block.pointed_dripstone.land 0.8/0.8; block.cherry_leaves.break 1/0.7 |
| `snd/burrow_dive` | P9 dive: digging and roots tearing. | entity.warden.dig 1/0.8; block.rooted_dirt.break 1/0.6 |
| `snd/burrow_loop` | P9 underground loop (every 30 t): muffled digging. | entity.warden.dig 0.4/0.6 |
| `snd/burrow_ring` | P9 rock-ring marker: rising charge and a chime. | block.respawn_anchor.charge 0.5/1.4; block.amethyst_block.chime 1/0.8 |
| `snd/burrow_rock` | P9 rock lands: smash and crystal. | item.mace.smash_ground_heavy 1/0.8; block.amethyst_cluster.break 1/0.8 |
| `snd/burrow_rush` | P9 surfacing rush / emergence: emerge, roar, boom. | entity.warden.emerge 1/0.9; entity.ravager.roar 0.6/0.6; entity.generic.explode 1/0.7 |
| `snd/slide_lift` | T1 lift (fore + hind paw rise): heavy step and deepslate. | entity.ravager.step 1/0.5; block.deepslate.step 1/0.6 |
| `snd/slide_wave` | T1 waves 1-5: a wide boom (volume 2 = heard across the arena), basalt, crystal, falling stone. | entity.generic.explode 2/0.5; block.basalt.break 1/0.6; block.amethyst_cluster.break 1/0.7; block.pointed_dripstone.land 1/0.8; block.pointed_dripstone.land 0.9/1; block.pointed_dripstone.land 0.8/0.7 |
| `snd/slide_wave6` | T1 wave 6 (the whole arena): the wave layers + the warden emerging. | entity.generic.explode 2/0.5; block.basalt.break 1/0.6; block.amethyst_cluster.break 1/0.7; block.pointed_dripstone.land 1/0.8; entity.warden.emerge 1/0.8 |
| `snd/jump_cue` | The "점프!" bell (wave - 8). | block.note_block.bell 1/1.2 |
| `snd/absorb_roar` | Absorb roar (roar_rear): growl and roar. | entity.ender_dragon.growl 1/0.55; entity.ravager.roar 1/0.5 |
| `snd/roar_ring` | One roar shock-dome ring. | entity.warden.sonic_boom 0.25/1.6 |
| `snd/msg_chime` | The transition message: resonating bell and a charge. | block.bell.resonate 1/0.6; block.respawn_anchor.charge 1/0.5 |
| `snd/b3_sink` | B3 sink: dig and gravel. | entity.warden.dig 1/0.8; block.gravel.break 1/0.5; block.gravel.break 0.9/0.6; block.gravel.break 0.8/0.55 |
| `snd/b3_rise` | B3 tail rises: emerge and dripstone. | entity.warden.emerge 1/1; block.pointed_dripstone.break 1/0.6 |
| `snd/b3_emerge` | B3 emergence burst t388: boom, emerge, basalt. | entity.generic.explode 1/0.6; entity.warden.emerge 1/0.8; block.basalt.break 1/0.8; block.basalt.break 1/0.9; block.basalt.break 0.9/0.7; block.basalt.break 0.8/1 |
| `snd/orb_spawn` | 31 orbs appear / pass: a riptide swirl and a splash. | item.trident.riptide_1 1/0.8; entity.dolphin.splash 1/1 |
| `snd/orb_loop` | 31 orb loop (every 20-40 t): whirlpool and conduit hum. | block.bubble_column.whirlpool_ambient 1/1; block.conduit.ambient 1/1.4 |
| `snd/orb_hit` | 31 orb hits a player: a splash. | entity.player.splash 1/1 |
| `snd/meteor_glyph` | 32 seal glyph: charge and beacon. | block.respawn_anchor.charge 1/0.7; block.beacon.activate 1/0.6 |
| `snd/meteor_fall` | 32 meteor falling. | entity.blaze.shoot 1/0.5 |
| `snd/meteor_impact` | 32 big meteor impact: boom, dragon fireball, sizzle. | entity.generic.explode 1/0.6; entity.dragon_fireball.explode 1/1; block.fire.extinguish 1/1 |
| `snd/meteor_small` | 32 small meteor: a blast and a light boom. | entity.firework_rocket.blast 1/0.6; entity.generic.explode 0.4/1.1 |
| `snd/fire_loop` | 33 fire field loop (every 20 t): fire and crackle. | block.fire.ambient 1/1; block.campfire.crackle 1/1 |
| `snd/frost_draw` | 41 star drawn: resonance and a thin beacon. | block.amethyst_block.resonate 1/1.4; block.beacon.activate 0.3/1.8 |
| `snd/frost_icicle` | 41 icicle thrown and shattering. | item.trident.throw 1/0.6; block.glass.break 1/0.6 |
| `snd/frost_burst` | 41 burst: powder snow breaking and a light boom. | block.powder_snow.break 1/1; block.powder_snow.break 0.9/0.8; block.powder_snow.break 0.8/1.2; entity.generic.explode 0.3/1.6 |
| `snd/bolt_marker` | 42 round markers (48 t before): high charge and a select tone. | block.respawn_anchor.charge 0.5/1.6; block.beacon.power_select 0.4/1.8 |
| `snd/bolt_strike` | 42 strike: thunder, bolt impacts (call again over 20 t for the 6-8 impacts), crystal. | entity.lightning_bolt.thunder 0.8/1; entity.lightning_bolt.impact 1/1.1; entity.lightning_bolt.impact 1/1.3; block.amethyst_cluster.break 1/1 |
| `snd/safe_chime` | 42 the player is inside a safe circle: a bright chime. | block.amethyst_block.chime 1/1.6; block.note_block.bell 0.6/1.8 |
| `snd/sphere_form` | 43 sphere forms: select tone and chimes. | block.beacon.power_select 1/1.6; block.amethyst_block.chime 1/1.2; block.amethyst_block.chime 1/1.5; block.amethyst_block.chime 1/1.8 |
| `snd/sphere_loop` | 43 sphere loop: conduit hum. | block.conduit.ambient 1/1.6 |
| `snd/lance` | 43 lance: riptide whoosh, glass and a light boom. | item.trident.riptide_1 1/1.6; block.glass.break 1/1; entity.generic.explode 0.4/1.4 |
| `snd/shell_spawn` | 44 shell spawn: spell cast and resonance. | entity.evoker.cast_spell 1/1.6; block.amethyst_block.resonate 1/1.4 |
| `snd/shell_hover` | 44 shells hovering: high beacon hum. | block.beacon.ambient 1/1.8 |
| `snd/shell_dive` | 44 shell dives: a swoop. | entity.phantom.swoop 0.4/1.6 |
| `snd/shell_impact` | 44 shell impact: bolt impact and a light boom. | entity.lightning_bolt.impact 0.6/1.3; entity.generic.explode 0.35/1.5 |
| `snd/ice_launch` | 45 launch: three breeze shots and dripstone. | entity.breeze.shoot 1/0.7; entity.breeze.shoot 0.9/0.75; entity.breeze.shoot 0.8/0.65; block.pointed_dripstone.break 1/1 |
| `snd/ice_land` | 45 dark spike lands. | item.trident.hit_ground 1/0.5; block.basalt.break 1/0.6 |
| `snd/ice_erupt` | 45 ice eruption. | block.amethyst_cluster.place 1/0.6; block.glass.break 1/0.8 |
| `snd/hail` | 45 hail ticking (quiet). | block.powder_snow.step 0.2/1.5; block.glass.hit 0.2/1.5 |
| `snd/hex_draw` | 46 hexagram drawn: spawn-point set and enchanting. | block.respawn_anchor.set_spawn 1/1.6; block.enchantment_table.use 1/1.2 |
| `snd/hex_bolt` | 46 bolt before a lump: thin thunder. | entity.lightning_bolt.thunder 0.25/1.6 |
| `snd/hex_impact` | 46 lump impact: dripstone, crystal, bolt. | block.pointed_dripstone.land 1/0.5; block.amethyst_block.break 1/0.8; entity.lightning_bolt.impact 0.5/1 |
| `snd/intro_drone` | E sealed drone (loop every 40 t). | block.respawn_anchor.ambient 1/0.5 |
| `snd/intro_thump` | E heartbeat thump of the sealed body. | entity.ravager.step 1/0.5 |
| `snd/stele_break` | E a seal stele shatters. | block.deepslate_bricks.break 1/0.6; block.deepslate_bricks.break 0.9/0.55; block.deepslate_bricks.break 0.8/0.65; entity.generic.explode 0.4/0.8 |
| `snd/seal_shatter` | E the seal prism shatters (t112). | block.glass.break 1/0.6; block.amethyst_block.break 1/0.7; block.beacon.deactivate 1/1 |
| `snd/intro_roar` | E the roar (t120). | entity.ender_dragon.growl 1/0.6; entity.ravager.roar 1/0.5; entity.warden.roar 0.6/0.8 |
| `snd/death_sting` | D music cut with a sting. | block.beacon.deactivate 1/0.6 |
| `snd/death_fall` | D the body falls (chin t34 / tail t66 / head t92). | entity.iron_golem.death 1/0.5; entity.ravager.death 1/0.6 |
| `snd/death_seal` | D the seal re-forms. | block.amethyst_block.resonate 1/1 |
| `snd/brand_apply` | Brand applied: a searing tone and a crystal tick. | block.respawn_anchor.set_spawn 0.6/1.4; block.fire.extinguish 0.4/1.6; block.amethyst_block.hit 1/0.8 |
| `snd/brand_tick` | A brand DoT tick (quiet). | block.amethyst_block.step 0.4/1.4; block.fire.extinguish 0.2/2 |
| `snd/cleanse` | The brand is cleansed (butterfly-style cure chime). | block.amethyst_block.chime 1/1.4; block.beacon.power_select 0.8/1.8; block.note_block.chime 0.8/1.6 |
| `snd/shard_spawn` | 응결 결정 sheds from the back. | block.amethyst_cluster.place 1/1.2; block.beacon.activate 0.4/1.6 |
| `snd/shard_pick` | 응결 결정 picked up (the shield). | block.amethyst_block.resonate 1/1.6; entity.experience_orb.pickup 0.8/0.8; block.beacon.power_select 0.7/1.4 |
| `snd/hint` | A first-time hint line. | block.note_block.pling 0.6/1.2 |
| `snd/absorb_vortex/1` | T2 Pyro swirl. | item.firecharge.use 1/1; entity.blaze.shoot 1/0.6 |
| `snd/absorb_vortex/2` | T2 Hydro vortex. | block.bubble_column.whirlpool_ambient 1/1; entity.player.splash.high_speed 1/0.7 |
| `snd/absorb_vortex/3` | T3 Electro charge. | block.beacon.ambient 1/0.6; item.trident.thunder 0.4/1.4 |
| `snd/absorb_vortex/4` | T3 Cryo gather. | block.amethyst_block.chime 1/1; block.powder_snow.step 1/1 |
| `snd/absorb_burst/1` | T2 Pyro burst. | entity.ghast.shoot 1/0.5; block.lava.pop 1/1; block.lava.pop 1/0.8; block.lava.pop 1/1.2 |
| `snd/absorb_burst/2` | T2 Hydro burst. | block.conduit.activate 1/0.8; block.beacon.power_select 1/0.6 |
| `snd/absorb_burst/3` | T3 Electro discharge. | entity.lightning_bolt.impact 1/1; entity.lightning_bolt.thunder 0.8/0.8 |
| `snd/absorb_burst/4` | T3 Cryo burst. | block.glass.break 1/0.6; entity.player.hurt_freeze 1/1; entity.generic.explode 1/1.2 |
| `snd/footfall/1` | Pyro footfall: a flame splash on the step. | entity.ravager.step 0.5/0.5; block.fire.ambient 0.4/1.2; item.firecharge.use 0.2/1.6 |
| `snd/footfall/2` | Hydro footfall: a splash. | entity.ravager.step 0.5/0.5; entity.player.splash 0.4/0.8 |
| `snd/footfall/3` | Electro footfall: sparks. | entity.ravager.step 0.5/0.5; block.amethyst_block.step 0.6/1.4; entity.lightning_bolt.impact 0.1/2 |
| `snd/footfall/4` | Cryo footfall: frost crunch. | entity.ravager.step 0.5/0.5; block.powder_snow.step 0.8/0.8 |
| `snd/footfall/5` | Geo footfall: heavy stone step. | entity.ravager.step 0.5/0.5; block.deepslate.step 0.6/0.6 |

## 20. Python API (`import build_mboss_az_fx as K`; nothing written on import)

Every builder returns one command string (no leading `$`; prefix `$` yourself when an argument is a `$(..)`
placeholder) and asserts that its name exists. Sizes in **blocks** (converted to tenths), ticks as ints, strings pass
through unchanged (placeholders).

| builder | emits |
|---|---|
| `K.card(kind, pos, rot, bb, roll, spin, s0, s1, move, life, fade, col)` / `K.cardx(…, dly, dur, hit, col2, off)` | `fx/e/cardf` (constant stage numbers), else `fx/card` / `fx/cardx` |
| `K.tele_disc(r, tell, el=5, nd=0, hold=3)`, `K.tele_ring(r0, r, tell, el=5, nd=0, hold=3)`, `K.tele_sector(r, a, tell, el=5, nd=0, hold=3)` | `fx/tele/…` |
| `K.tele_wedge(r0, r1, a0, a1, tell, el=5, nd=1, hold=3)` | `fx/tele/wedge` (note `nd=1` default: the P7 union) |
| `K.tele_line(length, w, tell, el=5, nd=0, hold=3, back=0)`, `K.tele_lane_side(length, w, tell, el=5, hold=3, back=0)` | |
| `K.tele_wave(wid, r0, r1, w, tell, dur, el=5, nd=0, hold=2)`, `K.tele_wave_to(wid, r, dur)`, `K.tele_wave_end(wid)` | |
| `K.tele_mline(mid, length, w, tell, el=5, nd=0, hold=0, back=0)`, `K.tele_mline_aim(mid)`, `K.tele_mline_turn(mid, d)`, `K.tele_mline_end(mid)` | |
| `K.tele_heptagram / hexagram / starseal / seal8(r, tell, el=4 / 3 / 4 / 1, hold=3)` | |
| `K.tele_mask_wash(r, tell, hold=3)`, `K.tele_safe_rim(sid, r, tell, hold=3)`, `K.tele_safe_beam(sid)`, `K.tele_safe_end(sid)` | |
| `K.tele_crater(r, tell, hold)`, `K.tele_halo(r, h, tell, el=1, hold=2)`, `K.tele_glyph_circle(r, tell, hold)` | |
| `K.tele_field(fid, r, el, life)`, `K.tele_strip(fid, length, w, yaw, el, life)`, `K.tele_field_end(fid)`, `K.tele_field_clear()`, `K.tele_clear()` | |
| `K.tele(shape, **args)` | any `fx/tele/<shape>` with `K.TELE_ARGS[shape]` |
| `K.fx(name, **args)` | `fx/p/<name>` (a family name needs `el=`: its dispatcher) |
| `K.fxe(name, el, **args)` | `fx/p/<name>/<el>` (int el; 0 / 6-8 → 5) or the dispatcher for a `'$(..)'` el |
| `K.snd(name)`, `K.snde(name, el)` | `fx/snd/<name>`, the member or the dispatcher |
| `K.prop(name)`, `K.prope(name, el)` | `fx/prop/<name>` (as @s), the member or the dispatcher |
| `K.look(kind, col)` | `fx/look {kind, col}` (as @s) |
| `K.hud(name, **args)`, `K.hude(name, el)` | `fx/hud/<name>`, the banner member or dispatcher |
| `K.glyph(name)`, `K.gl(name, extra)`, `K.badge(el, lit)`, `K.brand_badge(el)` | strings / text components |

Tables `K.KINDS K.PRESETS K.EPRESETS K.AMBIENT K.SOUNDS K.SFAM K.PROPS K.PFAM K.GLYPHS K.TELE_ARGS K.TELE_COL K.DEMOS`;
constants `K.CAP 64`, `K.TCAP 40`, `K.TSKIP 6`, `K.FCAP 16`, `K.SOFT 40`, `K.FN`, `K.FONT`, `K.STO`,
`K.OWNED_DIRS`, `K.OWNED_FILES`, `K.ATLAS_BUDGET`; `K.preset_cards(name, el=None)` (cards one call makes),
`K.TEST_ARGS` (the test values of every preset argument).

## 21. In-game tests and demos

`/function rlk:mboss/azhdaha/fx/test/<x>` as the player (`execute as @p at @s rotated ~ 0 run …`): `kinds` (every sprite
on a grid), `tele` (one telegraph of each shape and palette), `presets` (a clickable chat list), `sounds` (clickable),
`hud` (banners, cue, flashes in sequence), `props` (every prop look on a row), `stage` (the demo anchor, a vanilla
marker tagged `rlk_ak_demo` 12 b ahead facing the player), `stop`, `pair {leg, tail, ph}` (the demo elements, storage
`dm`), `demo/<name>`:

| demo | pattern | ticks |
|---|---|---|
| `test/demo/p1` | P1 갈라지는 봉인의 땅 (chin slam) | 65 |
| `test/demo/p2` | P2 바위 분쇄 충돌 (jump slam) | 53 |
| `test/demo/p3` | P3 바위 용왕의 돌진 (charge) | 70 |
| `test/demo/p4` | P4 천동만상 (back spikes) | 90 |
| `test/demo/p5` | P5 산명곡응 (foot stomp) | 63 |
| `test/demo/p5b` | P5b 산명곡응 – 연속 발구르기 | 85 |
| `test/demo/p6` | P6 성동격서 (side feint) | 50 |
| `test/demo/p7` | P7 교활한 통수 (tail whip, the wedge union) | 64 |
| `test/demo/p7ice` | P7 Cryo ice wall (annular wedges) | 50 |
| `test/demo/p8` | P8 꼬리찍기 (rear tail slam) | 100 |
| `test/demo/p9` | P9 잠복 돌진 (burrow charge, shortened) | 160 |
| `test/demo/t1` | T1 파멸의 산사태 (landslide) | 203 |
| `test/demo/t2` | T2 absorb 1 + roar | 140 |
| `test/demo/t3` | T3 absorb 2 + roar | 110 |
| `test/demo/b3` | B3 phase-3 burrow (shortened) | 190 |
| `test/demo/m31` | 31 격류 범람 (orb ribbons) | 62 |
| `test/demo/m32` | 32 운석 낙하 (meteors) | 100 |
| `test/demo/m33` | 33 화염 잠식 (fire field) | 165 |
| `test/demo/m41` | 41 서리 습격 (frost circles) | 70 |
| `test/demo/m42` | 42 벼락 습격 (lightning round) | 90 |
| `test/demo/m43` | 43 쏟아지는 천화 (ice sphere) | 120 |
| `test/demo/m44` | 44 번개의 가루 (shells) | 130 |
| `test/demo/m45` | 45 천동만상 – 얼음 가시 | 180 |
| `test/demo/m46` | 46 천동만상 – 번개 가시 | 140 |
| `test/demo/e` | E intro | 150 |
| `test/demo/d` | D death | 140 |

## 22. Tests, harness, renders

- `S:az/fxtests/test_az_fx.py <worktree roguelike> [<RP>]` — every §0 name callable (mcsim, `azfxsim.FxSim`: the card
  engine, stage merges, `data merge entity`, schedules in vanilla order), palettes and nd looks, disc / ring / sector /
  wedge / line / wave / mline geometry and timing (fill reaches the rim on the hit tick, sector 7.5° steps, wedge unions
  without gaps incl. annular), the field pool and the caps, every preset / family / dispatcher (el 0, 7, 9), sounds
  (vanilla, no voices, pitch range, min volume), HUD (font, no collision, banners), props, sprites (sides, atlas ≤ 0.6 M
  px), demos, static function names, uninstall, and **the worst concurrent timeline of each element pair** (phase 3
  fields + strip + 45/46 + emitter + P1, phase 2, transition 2, B3) with zero skipped attack-telegraph calls.
- `S:az/fxtests/run_kit.sh <worktree roguelike>` — test_az_fx, the kit build twice (datapack and RP: no change), the fg /
  bf kits and every non-kit file untouched, `kit_baseline.py --check` (every validator finding of the kit is of an
  accepted false-positive class), then the M0 suites.
- `S:az/fxtests/m0/` — the M0 suites (copy of `S:mb3/tests` + `test_az_fx` + `S:mb2/tests/test_fixes.py`; `gen_check.py`
  with the az kit in every generator order and its RP build twice; `ident.py` against M0 99bc097 and "only the kit's
  files changed" against 039b911); `baseline/` = the M0 baselines + `S:az/fxtests/baseline/*_kit.txt`.
- Renders `S:az/fxrender/render_az.py <wt> <RP> <out>` (the kit run in the same mcsim harness, cards ray-cast from the
  RP's own model JSON on the `az_cavern` floor): `sprites_floor.png`, `sprites_water.png`, `tele_elements.png`,
  `tele_nd.png`, `tele_eye.png`, `tele_seals.png`, `tele_field.png`, `presets_1.png`, `presets_2.png`, `family_*.png`,
  `props.png`, `hud.png`, `hud_glyphs.png`, `demo_*.png`, `compare_footage.png`.

## 23. Known limits

- Pixel-art sprites: a card scaled far beyond its texel density shows its texels (glows and smoke are 64 px, the wash
  128 px for that reason); MC samples item textures nearest-neighbour.
- `tele/sector` beyond ±97.5° and `tele/wedge` beyond 105° use 30° slices (coarser arcs); annular wedges are limited to
  r0 / r1 ∈ [0.0625, 0.84] and Δ ≤ 105° (the P7 Cryo ice wall stays inside).
- `#akTN` is incremented by every telegraph card as it is made (and recounted by the ager each tick), so several shapes
  made in the same tick are counted against the cap as they are drawn; the skip threshold (34 of 40) leaves room for
  one whole shape (≤ 6 cards); bigger shapes (sector ≤ 26, wedge ≤ 14 cards) can pass 40 only when called near the
  threshold, which the pair timelines of `test_az_fx` §15 never reach.
