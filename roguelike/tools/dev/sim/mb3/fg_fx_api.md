# 실험성 역장 발생 장치 FX / audio / HUD kit — API (`fg_fx_api.md`)

Generator: `tools/build_mboss_fg_fx.py` (+ `tools/mboss_fg_fx_paint.py`, the stdlib sprite painters, and
`tools/mboss_fg_fx_stub_rig.py`, the removable stub rig), branch `wip/fg-fx` (from `wip/bf` f2ab515). It is the butterfly
kit (`bf_fx_api.md`) copied and renamed, with the field generator's own sprites, telegraphs, sounds, HUD and presets, and
with the butterfly engine's first-tick bug fixed (§2.3).
Manifest written on every run: `tools/mboss_fg_fx_manifest.json` (kinds, presets, props, sounds, glyphs, owned paths,
caps, objectives, tags, telegraph colours, the rig mode, demos).

```
python3 tools/build_mboss_fg_fx.py --resourcepack <unpacked RP>      # datapack + RP (about 20 s, sprite painting)
python3 tools/build_mboss_fg_fx.py --skip-rp                         # datapack only
```

The kit draws; it never decides gameplay. Hits, hazards (`rlk:mboss/hz/*`), projectiles (`rlk:mboss/pj/*`), the low
gravity, the hit count and every timing stay in the module core. Every function below is visual / audio only and safe
to call any time (intro, fight, death shell, a test). Prefixes: fake players `#fk*` (objective `mb`), objectives
`fkS fkG fkH fkK fkD`, entity tags `rlk_fk*`, storage `rlk:fgkit`, font `rlk:mboss_fg` (U+E700-E7FF), item models
`rlk:mboss/fg_kit/*`. None of them collide with the butterfly kit (`#bk*`, `rlk_bk*`, `rlk:bfkit`, U+E600-E6FF) or with
the module core's `#fg*` / `rlk_fg*`.

## 0. Ownership, hooks, integration

| what | path | owner |
|---|---|---|
| card engine entry points | `F:mboss/fieldgen/fx/{card,cardx,look,clear,uninstall}` | this kit |
| internals, presets, telegraphs, sounds, HUD, props, tests, demos | `F:mboss/fieldgen/fx/{e,p,tele,snd,hud,prop,test}/**` | this kit |
| stub rig (only while the real rig manifest is missing) | `F:mboss/fieldgen/fx/rig_stub/**` | this kit (removable, §9) |
| the core's own fx files | any other name under `F:mboss/fieldgen/fx/` | module core (left alone) |
| sprites / models / item definitions | `assets/rlk/{textures,models/item,items}/mboss/fg_kit/<kind>` + atlas entries `rlk:mboss/fg_kit/*` in `assets/minecraft/atlases/items.json` | this kit |
| HUD font | `assets/rlk/font/mboss_fg.json`, `assets/rlk/textures/font/mboss_fg/*` (U+E700-E7FF) | this kit |
| rig (never written) | `F:mboss/fieldgen/rig/**`, its RP files | rig generator (`wip/fg-rig`) |

`F:` = `data/rlk/function/`. The kit's cleaner only touches its owned paths (manifest `owned`), so a kit rebuild never
deletes the core's files, and the butterfly kit (`F:mboss/butterfly/fx/**`, `tools/build_mboss_bf_fx.py`,
`tools/mboss_bf_fx_paint.py`, `tools/mboss_bf_fx_manifest.json`) is not changed (checked byte for byte by the harness).

**Integration notes for the core (read these):**

1. **The module's `clean()`** (copied from `tools/mboss_butterfly/core.py`, which deletes every file under the module
   folder except `rig/`) must also spare the kit's paths: `fx/{card,cardx,look,clear,uninstall}.mcfunction` and
   `fx/{e,p,tele,snd,hud,prop,test,rig_stub}/**` (manifest `owned`). Run the kit generator after the core generator (or
   in any order once `clean()` spares them).
2. **No `rlk:tick` / `rlk:load` hook is needed.** Cards are aged by `fx/e/world`, which `fx/card` schedules
   (`schedule … 1t replace`) and which re-schedules itself while any card lives. Objectives are created on the first
   card. After a `/reload` the schedule simply continues; nothing to re-init.
3. Lines for the module hooks:
   - `uninstall`: `function rlk:mboss/fieldgen/fx/uninstall` (kills cards and the demo anchor, removes the objectives,
     every `#fk*` fake player, storage `rlk:fgkit`, the three schedules; in stub mode also the stub rig).
   - `cleanup` / fight end / abort: `function rlk:mboss/fieldgen/fx/clear` + `function rlk:mboss/fieldgen/fx/hud/clear`
     (+ `hud/banner_end` if the field banner may still show).
   - `pause`: `function rlk:mboss/fieldgen/fx/tele/clear` + `function rlk:mboss/fieldgen/fx/hud/flash_end` (frozen
     hazards keep their framework markers; the decals would otherwise run on and flash early).
   - `death_start`: `function rlk:mboss/fieldgen/fx/tele/clear` + `hud/meter_close` + `hud/lowg_off`.
   - A pattern cancelled by the break (20 hits): `fx/tele/clear`, `tele/mline_end {id}` for the live lanes (or rely
     on `tele/clear`), `hud/banner_end`.
   - Boss-bar lines (`hud/extra`, `hud/sub` of the core): end them with `fx/hud/put_extra` / `fx/hud/put_sub` (§5).
   - A dead or reviving player clears every card by itself (`dead=1` or `rnDie≥1`, like the butterfly's).
4. Cards carry `rlk_room` + `rlk_mb_aux`, so `cleanup_aux`, the arena sweep, room clears and `rlk:uninstall` remove them
   too.
5. **The rig.** The kit calls the rig API only from `hud/e/stage<1-3>` (`crack/<n>`) and from the demos
   (`spawn`, `tick`, `kill`, `form/<f>`, `play/<clip>`). `RIG()` is `rlk:mboss/fieldgen/rig/` when
   `tools/mboss_fieldgen_rig_manifest.json` exists, else the stub `rlk:mboss/fieldgen/fx/rig_stub/`; rerun the kit
   generator after the rig is merged (§9).
6. **Butterfly core bugs not copied** (mb2 `review/core_findings.json`): the only kit-side one, the card ager's first
   tick (perf-2), is fixed here (§2.3). Kept markers, `g.release` and the blade reach are module-core matters; the kit
   keeps no markers of its own outside the demo anchor (`rlk_fk_demo`, killed by `test/stop` and `uninstall`).

## 1. Conventions

- **Executor context.** Every call draws relative to the executing position and rotation. Run it `at`/`positioned` the
  event point and `rotated` as the aim (yaw; pitch 0 unless stated): e.g.
  `execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/p/ports_glow` from the
  body (the husk on the floor under the axis), or `execute positioned <floor point> rotated ~ 0 run …` for decals.
  Floor points are at the floor top (y 201 in the plaza).
- **Heights above the body / floor** (rest poses, model.md §8): ring centre cruise / laser / tower **4.5**, field **5.8**
  (core −1.96 → **3.84**), core-up ring 5.0 + core 2.8 = **7.8**, deployed 5.6, dormant 2.15; the hub top about 5.2;
  the medallions (C3) about ±2.8 left / right at 2.5; the spike tips ±4.5 at the ring height. Read them from the rig
  manifest when it exists.
- **Display frame**: every card is summoned with its own rotation (`rot`) and `right_rotation` free for the spin; local
  axes are **+x = left, +y = up, +z = forward** of that rotation. `off`, `move` and `^x ^y ^z` use the same axes.
- **Planes** (how a kind's quad lies in the display frame; a painted card's **+a is the local −x (the right)**):
  - `face`: the local XY plane (faces forward, or the camera with a billboard); +b = up.
  - `flat`: the local XZ plane (horizontal for `rot "~ 0"`), +b = forward.
  - `cross`: two crossed vertical quads (XY and ZY) sharing the b axis = local +y: beams, columns, missiles read from
    every side without a billboard. Pitch the card to point the b axis (`rot "~ -90"` lays it forward).
  - `band`: a flat strip (b −1..0, the texture's top half) plus a vertical wall on its front edge
    (0.5 tall at scale 1, the bottom half): the wave ring's burning strip and its standing flame wall.
  - `box`: a cuboid of half extents (0.5, 0.135, 0.2) at scale 1, the full texture on all six faces (the slabs).
  - Spin axis: z for `face`, y for `flat` / `cross` / `band` / `box`.
- **Radial trick.** A fixed face card with `rot "~<yaw> <90 − elevation>"` has its local +y pointing outward along that
  yaw / elevation, so `move:"0f,<d>f,0f"` flies it outward with its long axis (shard, streak) along the flight.
- **Billboards**: `fixed` (world-oriented), `center` (camera-facing), `vertical` (turns about Y only), `horizontal`.
  `move` on a billboard is in the camera frame (use small vertical moves only).
- **Units**: blocks, ticks, degrees, colours as RGB ints (`16777215` = white = the painted colours unchanged).
  Telegraph sizes and the `wave_band` preset are in **tenths of a block** like the framework hazards (`r:28` = 2.8 b).
- **Tint** = `minecraft:custom_model_data` colour 0 of the card's item, multiplied into the texture. Painted kinds keep the
  footage colours under white; neutral kinds (`glow`, `glint`, `mote`, `streak`, `ripple`) take any colour. Telegraph
  textures bake their dark outline, which stays dark under every tint.
- **Stages** (server ticks, counted from the call tick T): visible from T (or hidden until `T + dly`), main
  interpolation `s0 → s1`, `off → off + move`, `spin` over `dur` ticks, sent at the end of server tick `T + dly + 1`
  (default `dur`: until the fade), tint → `col2` at `T + hit`, shrink to nothing over the last `fade` ticks, removed at
  `T + dly + life`.
- **Caps**: at most **64** live fx cards (further `card` calls are skipped silently) and **40** live telegraph cards
  (telegraph calls are skipped from 34 on, so a shape is never half drawn). The two are counted apart, so busy fx never
  hide a telegraph. **Ambient presets** (marked in §7: pebbles, glitch, field_idle, laser_spot, trails, debris, …) are
  skipped from **40** live fx cards on, keeping room for the hits' own fx.

## 2. Card engine

### 2.1 `rlk:mboss/fieldgen/fx/card` (macro)

| arg | type | meaning |
|---|---|---|
| `kind` | string | a kind of §3 |
| `pos` | string | summon point: `"^x ^y ^z"`, `"~x ~y ~z"` or absolute |
| `rot` | string | rotation of the card: `"~ ~"` = the executor's, `"~30 -90"` = turned 30° to the executor's right and pitched straight up (relative yaw, absolute pitch) |
| `bb` | string | `fixed` / `center` / `vertical` / `horizontal` |
| `roll` | int deg | `left_rotation` about the local z (forward) axis, constant |
| `spin` | int deg | turn about the plane's spin axis over the main interpolation, −170..170 |
| `s0`, `s1` | float | start / end size (uniform scale) |
| `move` | string | end translation `"dx f,dy f,dz f"` in the display frame, e.g. `"0f,1.2f,0f"` |
| `life` | int ticks | total life (≥ 2) |
| `fade` | int ticks | shrink-out at the end (≤ life − 2) |
| `col` | int | tint (RGB), `16777215` = none |

### 2.2 `rlk:mboss/fieldgen/fx/cardx` (macro)

Every option: `card`'s args with `s0` / `s1` as vector strings (`"1.2f,3f,1.2f"`) plus

| arg | meaning |
|---|---|
| `off` | static start translation `"x f,y f,z f"` (display frame); `move` is then the **absolute** end translation (the Python `card()` adds `off + move` for numbers) — a card can start and travel away from its pivot, e.g. the wave band segments `off (0,0,r0) → (0,0,r1)` or the moving-line cards |
| `dly` | ticks hidden (scale 0) before the card appears at `s0` |
| `dur` | ticks of the main interpolation (`0` = up to the fade) |
| `hit` | ticks after the call when the tint becomes `col2` (`-1` = never) |
| `col2` | second tint (`-1` = none) |

### 2.3 The first-tick fix (perf-2)

The ager (`fx/e/world`) is a `1t` schedule, so it runs at the **end of the same server tick** in which `card` was
called, with `gametime` already one higher. The butterfly kit counts its stages from the call's `gametime`, so a card's
main interpolation (`fkG`) is merged in the spawn tick itself, together with the summon: the client never sees the
start state and the card pops to `s1` (mb2 `core_findings.json`, perf-2). Here `fx/e/make` stores
`gametime + 1` as the card's clock, so the main interpolation is merged one server tick after the summon and the client
animates `s0 → s1`. `test_fg_fx.py` §1 checks it (`card: the main interpolation is never merged in the spawn server
tick`). The butterfly kit still has the bug (not touched here, see §13).

### 2.4 Others

| function | args | does |
|---|---|---|
| `fx/look` | `{kind, col}` | as `@s` (an item_display the module owns): the kind's item model, tint, full bright; keeps its transformation |
| `fx/prop/<name>` | – | as `@s`: a complete look (item, tint, billboard, scale / transformation) — §2.5 |
| `fx/clear` | – | kill every kit card (fx + telegraphs), zero the counts |
| `fx/tele/clear` | – | kill the telegraph decals only (moving lines included) |
| `fx/uninstall` | – | cards, demo anchor, objectives, `#fk*`, storage `rlk:fgkit`, schedules (and the stub rig in stub mode) |
| `fx/test/kinds` | – | every fx kind in rows in front of the executor (`execute as @p at @s rotated ~ 0 run …`) |
| `fx/test/tele` | – | one telegraph of each shape and palette, the wave ring and a moving line that turns for 84 t |
| `fx/test/presets`, `fx/test/sounds` | – | clickable chat lists (every preset 6 b ahead; every recipe) |
| `fx/test/hud` | – | the meter at 12/20 with a fresh count, the low-gravity flag and the field banner (run it during a fight to see the lines) |
| `fx/test/stage`, `fx/test/demo/<name>`, `fx/test/stop` | – | the demo anchor with the rig (real or stub) and 11 pattern demos (§9) |

### 2.5 Prop looks (`fx/prop/<name>`, as `@s` = the prop)

| prop | look |
|---|---|
| `prop/bomb` | C1 bomb: the camera-facing gold bomb, 0.9 across (vertical billboard, so a falling bomb stays upright). |
| `prop/missile` | C4 drill missile: nose along the prop's facing (local +z; aim it with tp ... facing), 1.3 long. |
| `prop/slab` | C6 / F2 glowing slab: a box 2.2 x 0.6 x 0.9 b (length along local x), full bright rim. |
| `prop/pebble` | Floating pebble (field ambience), 0.35 across. |
| `prop/chunk` | Floor chunk / rock, 0.6 across. |
| `prop/laser_core` | C3 beam core: hangs from the prop along local -y (pitch the prop down the beam: rotation pitch = beam pitch - 90), 0.45 wide; set scale y = the beam length. |
| `prop/laser_glow` | C3 beam glow sleeve: as laser_core, 1 b wide; scale x / z 0.5 -> 1.0 -> 0.5 for the bloom. |
| `prop/column` | Gold column standing on the prop (local +y), 1.1 wide; set scale y = the height. |
| `prop/ousia_col` | Violet Ousia column hanging from the prop (local -y), 1 wide; set scale y = the length. |
| `prop/charge` | Gravity-wave charge sphere look, 2 across (camera-facing). |
| `prop/muzzle` | Laser muzzle ring, 0.8 across (camera-facing). |
| `prop/bubble0` | Core bubble overlay, crack stage 0 (meter counts 0-4), 2.4 across, camera-facing; swap stages with this prop as the meter climbs. |
| `prop/bubble1` | Core bubble overlay, crack stage 1 (meter counts 5-9), 2.4 across, camera-facing; swap stages with this prop as the meter climbs. |
| `prop/bubble2` | Core bubble overlay, crack stage 2 (meter counts 10-14), 2.4 across, camera-facing; swap stages with this prop as the meter climbs. |
| `prop/bubble3` | Core bubble overlay, crack stage 3 (meter counts 15-19), 2.4 across, camera-facing; swap stages with this prop as the meter climbs. |

Keep `teleport_duration:1` on moving props (the pj library moves them every tick). The beam props (`laser_core`,
`laser_glow`, `column`, `ousia_col`) are `cross` kinds: they read from every side and only need their pitch and the
length in scale y.

## 3. Kinds (sprites)

Atlas added by the kit: **929 280 px** (≤ 1 M), 55 sprites (41 fx + 14 telegraph), every side ≤ 256 and a multiple of 16
(checked by the generator). Item models `rlk:mboss/fg_kit/<kind>`; every item definition has the `custom_model_data`
tint (default white). Model coordinates stay inside −16..32 (checked; the warp pillar is 1.5 tall at scale 1 for that).

| kind | plane | px | extent at scale 1 (blocks) | colour | use |
|---|---|---|---|---|---|
| `bomb` | face | 64x64 | a -0.5..0.5, b -0.5..0.5 | painted | gold bomb: dark core, glowing equator ring and ports, warm halo |
| `bomb_burst` | face | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | gold spiky bomb burst with dark flecks |
| `missile` | cross | 32x112 | a -0.14..0.14, b -0.5..0.5 | painted | gold drill missile, nose at +b, hot nose glow, exhaust |
| `smoke` | face | 64x64 | a -0.5..0.5, b -0.5..0.5 | painted | blue-white missile smoke puff |
| `column` | cross | 64x256 | a -0.5..0.5, b 0..1 | painted | gold light column / beam, foot at b 0, 1 block tall at scale 1 |
| `laser_core` | cross | 32x128 | a -0.5..0.5, b -1..0 | painted | laser beam core, from the muzzle (b 0) along -b |
| `laser_glow` | cross | 64x128 | a -0.5..0.5, b -1..0 | painted | laser beam glow sleeve, along -b |
| `muzzle` | face | 64x64 | a -0.5..0.5, b -0.5..0.5 | painted | laser muzzle ring with a hot centre |
| `scorch` | flat | 64x64 | a -0.5..0.5, b -0.5..0.5 | painted | floor scorch with a glowing gold centre |
| `slam_ring` | flat | 256x256 | a -1..1, b -1..1 | painted | slam shock ring (unit radius): gold band, dust fringe, flecks |
| `dust` | face | 64x64 | a -0.5..0.5, b -0.5..0.5 | painted | tan dust puff |
| `gold_shard` | face | 64x128 | a -0.25..0.25, b -0.5..0.5 | painted | gold crystal shard |
| `glass_shard` | face | 64x128 | a -0.25..0.25, b -0.5..0.5 | painted | white-gold bubble glass shard (the break) |
| `wave_band` | band | 256x128 | a -0.5..0.5, b -1..0 | painted | gravity-wave band segment: gold-fire strip + flame wall |
| `charge_sphere` | face | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | gravity-wave charge sphere with orbit swirls |
| `flare_dome` | face | 128x64 | a -0.5..0.5, b 0..0.5 | painted | burst flare dome (half dome, pivot at the base centre) |
| `fire_disc` | flat | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | filled fire disc (wave start, flame band) |
| `erupt_disc` | flat | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | dark eruption disc with an amber rim and gold cracks |
| `erupt_burst` | face | 128x128 | a -0.5..0.5, b 0..1 | painted | gold eruption burst with floor chunks, pivot at the floor |
| `chunk` | face | 32x32 | a -0.5..0.5, b -0.5..0.5 | painted | floor chunk / rock with an orange crack |
| `pebble` | face | 32x32 | a -0.5..0.5, b -0.5..0.5 | painted | floating pebble (low-gravity cue) |
| `spike_fan` | face | 128x128 | a -0.5..0.5, b 0..1 | painted | floor-burst crystal-spike fan, pivot at the floor |
| `slab` | box | 64x64 | a -0.5..0.5, b -0.135..0.135 | painted | glowing floor slab (box 1 x 0.27 x 0.4 at scale 1) |
| `ousia_col` | cross | 64x256 | a -0.5..0.5, b -1..0 | painted | violet Ousia column hanging from b 0 along -b |
| `glitch` | face | 64x128 | a -0.25..0.25, b -0.5..0.5 | painted | violet glitch streak |
| `warp_pillar` | face | 64x192 | a -0.25..0.25, b 0..1.5 | painted | white-cyan warp pillar, pivot at the floor, 1.5 tall at scale 1 |
| `warp_bloom` | face | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | white-cyan warp bloom |
| `bubble0` | face | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | core bubble, crack stage 0 |
| `bubble1` | face | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | core bubble, crack stage 1 |
| `bubble2` | face | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | core bubble, crack stage 2 |
| `bubble3` | face | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | core bubble, crack stage 3 |
| `crack_ring` | flat | 256x256 | a -1..1, b -1..1 | painted | gold crack ring (unit radius) |
| `crack_glint` | face | 64x64 | a -0.5..0.5, b -0.5..0.5 | painted | per-hit crack glint |
| `spark` | face | 64x64 | a -0.5..0.5, b -0.5..0.5 | painted | gold spark star |
| `arc` | face | 128x64 | a -0.5..0.5, b -0.25..0.25 | painted | electric gold arc |
| `flame` | face | 64x128 | a -0.25..0.25, b 0..1 | painted | gold flame tongue, pivot at its root |
| `glow` | face | 64x64 | a -0.5..0.5, b -0.5..0.5 | neutral (tint it) | soft white glow disc (tint it) |
| `glint` | face | 64x64 | a -0.5..0.5, b -0.5..0.5 | neutral (tint it) | white 4-point glint (tint it) |
| `mote` | face | 32x32 | a -0.5..0.5, b -0.5..0.5 | neutral (tint it) | soft mote (tint it) |
| `streak` | face | 256x32 | a -0.5..0.5, b -0.0625..0.0625 | neutral (tint it) | long thin streak along a (tint it) |
| `ripple` | face | 256x256 | a -0.5..0.5, b -0.5..0.5 | neutral (tint it) | ripple / shock ring (near white, tint it) |

Telegraph textures (flat, neutral, tinted by the palette): `t_rim` (256², unit radius), `t_rim_s` (thick rim for
r ≤ 2.5), `t_ring` (thin travelling wave ring), `t_fill` (progress fill, unit radius), `t_bar` (lane rail / cap),
`t_lane` (lane fill, unit length), `t_sec30/45/60/90` + `t_secf30/45/60/90` (sector rims and fills).

Colours (from the footage notes, `research v1..v4.md`): brass `#E8C46A` (registry), charge gold `#F5CF88` / `#FDF3AA` /
`#FDFBD1`, deep gold `#E2AE66`, amber `#E6A55F`, orange `#D29253`, lift flare `#F0D19C`, crack gold `#F6DD8E`, rim flare
`#FDF4CD`; violet `#8775EE` / `#6C64E3` / `#CCB7E2` (the field, Ousia column, glitch); warp white-cyan `#C2E1F5` /
`#DFF6FB`; dust `#CAA376` / `#E4BA87`; smoke `#E2E8EC`; the wave fire ramps white-gold → gold → `#D29253` → `#8C4A2A`.
Python names: `K.BRASS, K.GOLD, K.GOLD_PALE, K.GOLD_WHITE, K.GOLD_DEEP, K.AMBER, K.ORANGE, K.FLARE, K.VIOLET,
K.VIOLET_DEEP, K.VIOLET_PALE, K.CYAN, K.CYAN_PALE, K.DUST, K.DUST_PALE, K.CRACK_GOLD, K.RIM_PALE, K.SMOKE, K.WHITE`.

## 4. Ground telegraphs (`fx/tele/*`, macros)

All are **visual only**: pair each with the framework hazard of the same shape, made in the same tick with the same
`tell`, and set `#hzQuiet mb 1` before it so the framework particles do not double the decal. The fill's bright edge
reaches the rim exactly on **call tick + tell**, the tick `hz/*` strikes (fill interpolation from T+1 over tell−1
ticks); on that tick every card of the shape flashes (tint → flash colour), then it stays `hold` ticks and disappears.
Every damaging hit of the plan has `tell ≥ 10`.

**Telegraph rule (10-20, user: "보스의 모든 공격에 바닥의 예고를 보여줄 필요는 없어. 영상에 없다면 그냥 보스의 동작을 보고
회피해야")**: the module draws a ground decal only where the reference footage shows a marker on the floor before the hit
(audit scratchpad `tele/fg/audit.md`): C5 지면 충격 `tele/rim` (palette 6) + `tele/dark`, F1 감소 영역 `tele/dark`, the C1 /
C2 slam's late base flare `p/column_base`. Every other hazard is still quiet (`#hzQuiet 1`) but has no decal; it is read
from the device's motion and sound. The other shapes below stay in the kit's API (and `fx/test/tele`).

| function | args (tenths of a block, ticks) | cards | drawn at |
|---|---|---|---|
| `tele/disc` | `{r, tell, el, hold}` | 2 (fill + rim; thick rim when r ≤ 2.5) | the floor point |
| `tele/rim` | `{r, tell, el, hold}` — `tele/disc` without the fill / progress edge (10-20) | 1 (static rim; thick when r ≤ 2.5; flashes on call + tell) | the floor point |
| `tele/dark` | `{r0, r, grow, tell, hold}` — the dark floor disc (`erupt_disc`: darker floor, amber rim, gold cracks), radius r0 → r over `grow` ticks from call + 1, held to call + tell + hold + 1; painted colours, no flash (10-20) | 1 | the floor point |
| `tele/ring` | `{r0, r, tell, el, hold}` | 3 (outer + inner rim, a progress ring travelling r0 → r) | the floor point |
| `tele/sector` | `{r, a, tell, el, hold}` — `a` = half-angle; snaps to 30 / 45 / 60 / 90, `a ≥ 136` draws a disc | 2 | the apex, rotated = aim |
| `tele/line` | `{len, w, back, tell, el, hold}` — covers −back..len along the aim, w wide (`hz/line` + `#hzBack`); a **negative** `back` starts the lane beyond the point | 5 (2 rails, 2 caps, the lane fill) | the start point, rotated = aim |
| `tele/wave` | `{r0, r1, w, tell, dur, el, hold}` — the expanding wave ring (§4.1) | 4 | the floor centre |
| `tele/mline` | `{id, len, w, back, tell, el, hold}` — a moving line (§4.2), id 0-7 | 5 | the pivot, rotated = aim |
| `tele/mline_aim` | `{id}` — turn lane `id` to the executing yaw | – | run rotated as the new aim |
| `tele/mline_turn` | `{id, d}` — turn lane `id` by `d` degrees (+ = clockwise from above) | – | anywhere |
| `tele/mline_end` | `{id}` — remove lane `id` now | – | anywhere |

`el` picks the colours (rim / fill / flash): **5 Geo** `#D27A0C / #F0A93A / #FFE8A0` (the default, every cruise
pattern), **9 the field's violet** `#7046DC / #A288F2 / #ECE2FF` (the field patterns: waves, 감소 영역), **0 physical**
`#E5304A / #FF6474 / #FFB8C4`, **6 the pale-gold rim** `#EFC566 / #F6DC96 / #FDF4CD` (C5 지면 충격's footage rim, `tele/rim`;
10-20); any other value draws Geo. Rims: a dark outline, a saturated band and a thin dark inner
line; fills: translucent with a bright leading edge between two dark lines — readable on the white marble and on the
pink star (renders `fx_telegraphs_*.png`, `fx_tele_textures_*.png`). Layering: fills at floor +0.03, rims at +0.045,
wave rings at +0.048 / +0.05.

### 4.1 The wave ring (「인력 충격파」)

Over the tell (the charge) a disc decal fills to `r0`, the start radius of the front, and flashes on the strike tick.
From the strike the **front ring travels r0 → r1 in dur ticks** (a constant `(r1 − r0) / dur` b/t: 2.5 → 21 in 34 t =
0.55 b/t) with a second ring `w` behind it (the band's inner edge), then both stay `hold` ticks. The rings are shown on
the tick before the strike and their interpolation is sent at the end of the strike tick, so the drawn front equals the
hazard front `r0 + spd × (t − strike)` on every tick (checked in the suite). Pair it with
`hz/ring {r0:0, r:<r0>, tell}` (+ `#hzNoDodge 1`, the low band 0-0.7 b) and `hz/resize` each tick after the strike
(`r = r0 + spd × k`, inner `r − w`). The fire band preset `p/wave_band` draws the same front in 3-D — **call it on the
tick before the strike** so it moves in the same tick as the decal (it is a plain card; checked by the suite).

```
# t0 = the charge start, strike = t0 + 24
execute positioned <arena centre> run function rlk:mboss/fieldgen/fx/tele/wave {r0:25,r1:210,w:25,tell:24,dur:34,el:9,hold:2}
# strike - 1:  ... run function rlk:mboss/fieldgen/fx/p/wave_band {r0:25,r1:210,w:25,dur:34}
```
Python: `K.tele_wave(2.5, 21.0, 2.5, 24, 34)` (blocks in, tenths out). For the < 50 % HP triple front, call
`tele_wave` once per front with `tell = 10` for the 2nd / 3rd (9 t apart, their decal starts 10 t before each).

### 4.2 Moving lines (C3 laser lanes)

`tele/mline` draws a `tele/line` whose five cards all sit on the **pivot** (the executing point, e.g. the device axis on
the floor) with their offsets in their own translation, `teleport_duration 1` and the tag `rlk_fk_ml<id>`
(`rlk_fk_ml<id>c` for the two caps, which are turned 90°). Turning the cards about the pivot turns the whole lane
smoothly:

- `tele/mline_aim {id}` run `rotated as` the re-aimed hazard marker (after `hz/aim`) snaps the lane to that yaw;
- `tele/mline_turn {id, d}` adds `d` degrees (two counter-rotating beams: `d:5` and `d:-5` every tick);
- `tele/mline_end {id}` removes it (beam off, pattern cancelled); `tele/clear` removes every lane.

The fill reaches the far end on call + tell (the beams fire), then the lane stays in the flash colour for `hold` ticks
(set `hold` = the firing time, 133 t for C3, or end it with `mline_end`). A lane that should cover only the floor under a
beam from r 2.8 to r 5.8 is `{len:58, back:-28}`. Python: `K.tele_mline(0, 5.8, 0.8, 24, hold=133, back=-2.8)`,
`K.tele_mline_aim(0)`, `K.tele_mline_turn(0, 5)`, `K.tele_mline_end(0)`.

## 5. HUD (font `rlk:mboss_fg`)

| codepoint | glyph | size (texture px → GUI height, ascent) |
|---|---|---|
| U+E700 | field badge: violet hex lens with a gold core and orbit (meter / name line) | 36 → 9, 8 |
| U+E701 / E702 / E703 | meter pip empty (dark violet slanted gem), full (gold), flash (white) — pixel glyphs | 8x14 → 7, 7 |
| U+E704 | break pop: cracked bubble burst (title line) | 96 → 24, 18 |
| U+E705 / U+E706 | low-gravity icon (an up arrow over a floating stone), small / big | 36 → 9, 8 / 96 → 24, 18 |
| U+E710-E713 | flat full-screen flashes: white (0.92), gold `#F9DFAD` (0.55), violet `#6C64E3` (0.45), amber `#E6A55F` (0.45) | 16x9 → 144, 69 |
| U+E720-E729, U+E72A | the "N/20" digits 0-9 and "/" (outlined gold pixel digits) | 7x9 → 9, 8 |
| U+E7F0 / E7F1 / E7F2 | spaces −1 / +2 (the gap between pip groups of 5) / +1 | |

The generator refuses to write the font when any of its codepoints is used by another font of the resource pack
(checked against every `assets/*/font/*.json`; today `rlk:hud` E100-E101, `rlk:minimap` E300-E3F2, `rlk:bossbar`
E400-E438, `rlk:mboss_gd` E500-E5F1, `rlk:mboss_bf` E600-E6FF).

| function | does |
|---|---|
| `hud/meter_open` | the field opened: `#fkM` = 0, the meter (0/20) joins the lines |
| `hud/meter_close` | the field closed (break, end, death, abort): the meter leaves the lines |
| `hud/meter` | redraw from `#fkM mb` (0-20, set by the module), no flash; `hud/meter_n {n}` = the same with an argument |
| `hud/meter_hit` | **one count, all its feedback** (with `#fkM mb` = the new count): the newest pip flashes white for 4 t, `p/meter_glint` at the executing position, `snd/meter_tick` + a chime note rising with the count (2^((k−10)/12)), and on 5 / 10 / 15 crack stage 1 / 2 / 3: `p/bubble_crack`, `snd/bubble_crack` and `<RIG>crack/<n>` as `@s` |
| `hud/hint_on`, `hud/hint_off` | the first-field hint "코어를 공격해 역장을 깨뜨리세요" after the meter |
| `hud/lowg_on`, `hud/lowg_off` | the low-gravity icon on the name line |
| `hud/groggy_on`, `hud/groggy_off` | " · 그로기" on the name line |
| `hud/clear` | every flag off (fight end, death, abort, uninstall) |
| `hud/put_extra` | append `rlk:fgkit hud.ex[]` (" · 역장" + badge, the low-gravity icon, " · 그로기") to `rlk:mboss extra` — call at the end of the core's line-1 build; equivalent component `{nbt:"hud.ex[]",storage:"rlk:fgkit",interpret:true,separator:""}` |
| `hud/put_sub` | append `rlk:fgkit hud.sub[]` (badge, "역장", 20 pips in groups of 5, the "12/20" glyphs, the hint) to `rlk:mboss sub` — call after the core's own sub-line text |
| `hud/banner_field` | field +57: the actionbar banner "중력이 감소하고 점프 능력이 향상됩니다" (중력 / 점프 red `#FC5050`, bold) with the low-gravity icon for 4 s (`hudHold 80`), `pop_lowg`, `snd/field_banner` |
| `hud/banner_end` | drop the banner early (cancel, break) |
| `hud/ab_lowg` | one-shot actionbar notice (2 s): low gravity and what it means (점프 강화 · 낙하 피해 감소 · 충격파는 점프로 피하기) |
| `hud/pop_break`, `hud/pop_lowg` | the big glyph on the title line (`vBig` rests the F5 crosshair title) |
| `hud/flash_white`, `flash_gold`, `flash_violet`, `flash_amber` | full-screen flat flash on the title line (any view mode) |
| `hud/flash_end` | drop a title overlay at once |

**Meter protocol** (the count itself is the core's: on_hit hook, no reactions / DoTs / item procs, at most one per 6 t):

1. Field unfold: `hud/meter_open` (+ `hud/hint_on` on the first field), `hud/lowg_on` when low gravity starts,
   `<RIG>crack/0` (the clean bubble).
2. Each counted hit: set `#fkM mb` to the new count, then
   `execute as <body> at <body> positioned ~ ~3.84 ~ run function rlk:mboss/fieldgen/fx/hud/meter_hit`
   (as the rig anchor — the body — so the crack call reaches the rig; positioned at the core so the glint sits on the
   bubble). The kit does not count; `meter_hit` clamps the value to 1..20.
3. At 20 (the break): `hud/meter_close`, `hud/lowg_off`, `hud/hint_off`, `hud/banner_end`, the break presets (§10),
   `<RIG>crack/4` at the burst; `hud/groggy_on` … `hud/groggy_off` around the 200 t groggy.
4. The field ends unbroken: `hud/meter_close`, `hud/lowg_off`.

The kit's lines change from a schedule too (the pip flash ends 4 t after a count): each rebuild bumps `#fkHudV mb`, so a
core that rebuilds its boss-bar lines only on change must also rebuild when `#fkHudV` changed. The violet **under-bar**
with the hits out of 20 (plan.md) is the core's own boss-bar line, not the kit's; the kit only gives the sub-line and
the name-line flags. Renders: `fx_hud.png` (the lines at 0 / 7 / 12 with the flash / 20, the banner, the pops).

## 6. Sound recipes (`fx/snd/<name>`, no args)

Vanilla sound events only, mechanical / brass (anvil, chain, piston, beacon, respawn anchor, amethyst, trial spawner,
vault, crafter, copper, breeze charge, …); no creature voices (checked against a voice list: `.ambient` except block
ambients, `.hurt`, `.death`, `.roar`, `.growl`, villagers, witches, ghasts, …), pitch 0.5-2. Played `hostile` to `@a[tag=player]` at the executing position with the shared `minVolume` rule.

| recipe | use | layers (event volume pitch; minVolume = mboss_lib.min_volume) |
|---|---|---|
| `snd/awake_clank` | Activation clank (entrance E0): a sharp metallic clank with a bright tail. | block.vault.activate 0.9 0.8; block.iron_trapdoor.close 0.8 0.7; entity.zombie.attack_iron_door 0.35 1.4; block.anvil.place 0.3 1.6; block.beacon.activate 0.3 1.3 |
| `snd/unfold` | Pods unfold and the crown assembles (entrance +8..+30): low thumps and gear clicks. | block.piston.extend 0.8 0.8; block.crafter.craft 0.7 0.9; block.chain.place 0.7 0.9; block.copper_trapdoor.open 0.6 0.8 |
| `snd/gear_click` | Crown gear clicks (call 2-3 times while the crown assembles; quiet). | block.crafter.craft 0.6 1.25; block.copper_bulb.turn_on 0.4 1.5; block.chain.hit 0.35 1.4 |
| `snd/eye_open` | The eye opens and the core drum turns (entrance +32..+64): a low mechanical groan and a click. | block.vault.open_shutter 0.9 0.9; block.grindstone.use 0.3 0.6; block.beacon.power_select 0.4 1.6; block.amethyst_block.resonate 0.4 1.2 |
| `snd/rise_hum` | The device rises to cruise height (entrance +64..+94; also field lift-offs): whirring hum. | block.beacon.ambient 0.9 1.4; block.conduit.ambient 0.6 1.2; entity.minecart.riding 0.3 1.6; entity.breeze.whirl 0.4 0.7 |
| `snd/bomb_port` | Underside bomb ports light up (C1 +10): shutters and a rising charge. | block.vault.open_shutter 0.6 1.3; block.respawn_anchor.charge 0.4 1.8; block.dispenser.dispense 0.4 0.7 |
| `snd/bomb_drop` | A bomb leaves a port (C1, every 2-4 t; quiet). | block.dispenser.launch 0.55 0.8; entity.tnt.primed 0.15 1.6 |
| `snd/bomb_fall` | Falling whistle of a bomb (C1, once per volley group). | item.trident.riptide_1 0.25 2; entity.firework_rocket.launch 0.3 1.6 |
| `snd/bomb_burst` | A bomb bursts on the floor (C1, per landing): short crack and crystal. | entity.generic.explode 0.35 1.5; block.amethyst_cluster.break 0.6 0.8; block.basalt.break 0.5 1.1; entity.firework_rocket.blast 0.3 0.9 |
| `snd/column_tell` | Gold slam column projects to the floor (C1 / C2, 13 t tell): rising hum. | block.respawn_anchor.charge 0.8 1; block.beacon.power_select 0.7 0.8; block.beacon.activate 0.4 1.5 |
| `snd/plunge` | The device plunges core first (C1 / C2, 3-4 t): whoosh and a hydraulic drop. | entity.breeze.wind_burst 0.7 0.6; item.trident.riptide_3 0.4 0.8; block.piston.contract 0.6 0.6 |
| `snd/slam` | Slam impact r 5 (C1 / C2): heavy boom, anvil and debris. | entity.generic.explode 1 0.7; item.mace.smash_ground_heavy 0.8 0.8; block.anvil.land 0.6 0.5; block.heavy_core.place 0.7 0.7; block.amethyst_cluster.break 0.6 0.7 |
| `snd/pods_drop` | The medallions dock and drop beside the core (C3 +0..+4): clank. | block.chain.place 0.8 0.9; block.piston.contract 0.7 0.8; block.vault.close_shutter 0.5 1.2 |
| `snd/laser_charge` | Laser spark charge (C3, 18 t): bright rising whine. | block.beacon.activate 0.8 1.8; block.amethyst_block.resonate 0.7 1.5; block.respawn_anchor.charge 0.5 1.7; entity.guardian.attack 0.3 1.8 |
| `snd/laser_fire` | The two beams fire (C3 +24): hissing burst. | block.beacon.power_select 0.8 1.4; entity.warden.sonic_boom 0.3 1.9; entity.blaze.shoot 0.5 1.4; item.trident.thunder 0.2 2 |
| `snd/laser_loop` | Beam loop (C3, every 10 t while firing, at the floor spots): hum and crackle. | block.beacon.ambient 0.7 2; block.fire.ambient 0.5 1.6; block.campfire.crackle 0.4 1.4 |
| `snd/laser_stop` | Beams off and pods retract (C3 end): power-down. | block.beacon.deactivate 0.8 1.2; block.piston.contract 0.6 0.9; block.fire.extinguish 0.3 1.6 |
| `snd/tip_flare` | Spike-tip flare (C4 tell 1; also the next-pattern tell): crackle. | entity.breeze.charge 0.7 1.4; block.respawn_anchor.charge 0.6 1.6; block.amethyst_block.chime 0.5 1.6 |
| `snd/missile_vent` | Top vents open with the vertical gold shaft (C4 tell 2): roaring hiss. | block.blastfurnace.fire_crackle 0.9 0.9; entity.blaze.shoot 0.7 0.7; block.vault.open_shutter 0.6 0.8; block.fire.ambient 0.8 0.9 |
| `snd/missile_launch` | A drill missile launches (C4, per missile). | entity.firework_rocket.launch 0.7 0.9; entity.breeze.shoot 0.4 0.8 |
| `snd/missile_dive` | Missiles turn over and dive (C4, once per volley group): falling whistle. | item.trident.riptide_1 0.45 1.8; entity.phantom.swoop 0.35 1.6 |
| `snd/missile_impact` | A missile hits the floor (C4, per impact): crack and boom. | entity.generic.explode 0.4 1.4; block.amethyst_cluster.break 0.6 0.9; block.deepslate.break 0.5 1 |
| `snd/core_flip` | The core flips (C5 lift, the field core flip, groggy recover): clank and whoosh. | block.vault.open_shutter 0.8 0.9; entity.breeze.wind_burst 0.5 0.8; block.crafter.craft 0.5 0.8 |
| `snd/core_spark` | Gold spark on the core (C5 tell 1): dense crackle. | block.respawn_anchor.charge 0.7 1.3; block.amethyst_block.chime 0.6 1.6; block.amethyst_block.chime 0.5 1.9; entity.blaze.burn 0.2 1.6 |
| `snd/core_lift` | The core lifts with a gold flare (C5 +5, "번쩍"): bright flare. | block.beacon.activate 0.8 1.4; block.respawn_anchor.set_spawn 0.5 0.6; entity.firework_rocket.twinkle 0.3 1.2 |
| `snd/up_beam` | Upward gold beam from the raised core (C5 +29..+40): rising crackle. | block.beacon.ambient 0.8 1.6; entity.warden.sonic_charge 0.4 1.4; block.conduit.activate 0.6 1.2 |
| `snd/column_down` | The column switches down to the floor centre (C5 +41): zap. | item.trident.thunder 0.3 1.8; entity.breeze.wind_burst 0.6 0.6; block.amethyst_cluster.break 0.6 0.7 |
| `snd/blast` | Full-area gravity blast (C5 +48): big broadband boom, rocks launched. | entity.generic.explode 1.2 0.6; entity.warden.sonic_boom 0.6 0.8; entity.dragon_fireball.explode 0.6 0.9; block.basalt.break 0.8 0.8; block.pointed_dripstone.land 0.6 0.9 |
| `snd/rocks_hover` | Rocks hover after the blast (C5 +54..+77, every 6-10 t; quiet): low rumble. | block.amethyst_block.resonate 0.4 0.6; block.gravel.fall 0.4 0.7; entity.ravager.step 0.25 0.5 |
| `snd/dip` | Dip and roll toward the player (C6 +0): whoosh. | entity.breeze.whirl 0.8 0.8; block.chain.step 0.5 0.8 |
| `snd/vent_flare` | Vent flare, the medallions flung up (C6 +12): roaring hiss. | block.blastfurnace.fire_crackle 0.8 1; entity.blaze.shoot 0.6 0.6; block.beacon.power_select 0.5 1.4 |
| `snd/tower_up` | The tower telescopes up (C6 +20, 18 t): ratchet clicks. | block.crafter.craft 0.8 1; block.vault.open_shutter 0.6 1.1; block.iron_trapdoor.open 0.6 0.9; block.piston.extend 0.6 1.2 |
| `snd/flame_charge` | The flame band flares under the ring (C6 charge, 17 t): rising roar. | item.firecharge.use 0.8 0.7; block.respawn_anchor.charge 0.6 1.3; block.fire.ambient 0.9 0.9; block.campfire.crackle 0.5 0.9 |
| `snd/floor_burst` | A floor burst erupts (C6 / F2, per burst): crystal crack and thump. | block.amethyst_cluster.break 0.9 0.8; entity.generic.explode 0.3 1.4; block.stone.break 0.8 0.6; block.tuff.break 0.6 0.8 |
| `snd/slab_lift` | A slab tears out and rises (C6 / F2, after each burst; quiet): grinding rise. | block.piston.extend 0.35 0.6; block.grindstone.use 0.3 0.5; block.deepslate.break 0.4 0.7 |
| `snd/slab_throw` | A slab is flung at the player (C6 / F2, per throw): heavy whoosh. | entity.breeze.shoot 0.7 0.7; item.trident.throw 0.7 0.6; entity.wind_charge.throw 0.4 0.6 |
| `snd/slab_impact` | A slab lands (C6 / F2): crash. | entity.generic.explode 0.5 0.9; block.anvil.land 0.4 0.6; block.stone.break 0.8 0.7; block.deepslate.break 0.6 0.8 |
| `snd/revert` | The tower collapses back into the ring (C6 end): clunk. | block.piston.contract 0.7 0.9; block.chain.place 0.7 1; block.crafter.craft 0.5 1.1 |
| `snd/halo_flip` | The halo flips upright before the warp (field +0): whoosh. | entity.breeze.whirl 0.8 0.8; block.vault.close_shutter 0.5 1 |
| `snd/warp_out` | Warp-out flash (field +13): bright zap and a low whoomp. | entity.enderman.teleport 0.8 0.6; entity.illusioner.mirror_move 0.7 1; block.beacon.deactivate 0.5 1.6; entity.breeze.wind_burst 0.4 1.2 |
| `snd/glitch` | Violet glitch crackle (field +14..+33 over the old spot, field idle; quiet). | block.sculk.charge 0.6 1.2; block.respawn_anchor.ambient 0.4 1.8; entity.evoker.prepare_summon 0.2 1.6 |
| `snd/warp_in` | Warp-in at the arena centre (field +34). | entity.enderman.teleport 0.8 0.8; block.beacon.activate 0.7 1.2; entity.illusioner.mirror_move 0.6 0.8; entity.warden.sonic_charge 0.3 1.6 |
| `snd/field_unfold` | The stack unfolds into the field form (field +35..+51): springs and chains. | block.vault.open_shutter 0.7 0.7; block.piston.extend 0.7 0.7; block.chain.place 0.6 0.8; block.respawn_anchor.set_spawn 0.6 0.7 |
| `snd/field_hum` | Low-gravity field drone (every 40 t while the field is up; quiet). | block.conduit.ambient 0.5 0.6; block.beacon.ambient 0.4 0.6 |
| `snd/field_banner` | The banner "중력이 감소하고 점프 능력이 향상됩니다" appears (field +57). | block.respawn_anchor.set_spawn 0.7 0.7; block.beacon.power_select 0.5 0.6; block.amethyst_block.resonate 0.5 0.5 |
| `snd/wave_charge` | 「인력 충격파」 charge, start (24 t / 40 t): rising airy hiss. | block.beacon.power_select 0.7 0.7; block.conduit.activate 0.6 1; block.respawn_anchor.charge 0.5 1; entity.warden.sonic_charge 0.3 1.6 |
| `snd/wave_charge2` | 「인력 충격파」 charge, the last 10 t: higher. | block.beacon.power_select 0.7 1.4; block.respawn_anchor.charge 0.6 1.5; block.amethyst_block.resonate 0.5 1.6 |
| `snd/wave_beam` | 「인력 충격파」 1-tick beam core -> floor: thump and zap. | item.trident.thunder 0.3 1.6; block.beacon.deactivate 0.6 0.6; entity.breeze.wind_burst 0.5 0.9 |
| `snd/wave_burst` | 「인력 충격파」 burst flare dome: boom and roar. | entity.generic.explode 0.7 0.7; entity.dragon_fireball.explode 0.4 1; block.fire.ambient 0.8 0.8; item.firecharge.use 0.6 0.6 |
| `snd/wave_ring` | 「인력 충격파」 front travelling (every 2-3 t at the front point nearest the player; quiet): rumble. | block.fire.ambient 0.3 1; block.lava.pop 0.25 0.9; entity.ravager.step 0.25 0.5 |
| `snd/erupt_tell` | 감소 영역 dark discs appear (F1, per event; quiet). | block.respawn_anchor.charge 0.4 1.6; block.sculk_sensor.clicking 0.4 0.8; block.gravel.hit 0.3 0.6 |
| `snd/erupt` | 감소 영역 gold eruption (F1, per event): crack and gravel burst. | block.basalt.break 0.9 0.9; block.pointed_dripstone.land 0.6 1; block.pointed_dripstone.land 0.5 1.3; entity.generic.explode 0.4 1.4; block.deepslate.break 0.6 0.7 |
| `snd/debris_land` | Debris settles after an eruption or the blast (quiet). | block.gravel.fall 0.3 0.8; block.stone.fall 0.25 0.8 |
| `snd/meter_tick` | A break-meter count (each counted hit): crystalline ping on brass (hud/meter_hit adds a note that rises with the count). | block.amethyst_block.hit 0.9 1.4; block.chain.hit 0.5 1.2 |
| `snd/bubble_crack` | The core bubble cracks a stage further (counts 5, 10, 15). | block.glass.break 0.6 1.6; block.sniffer_egg.crack 0.7 1.2; block.amethyst_cluster.break 0.5 1.4 |
| `snd/break_glow` | The bubble lights up before the burst (break +0..+5). | block.beacon.activate 0.7 1.6; block.respawn_anchor.charge 0.6 1.9; block.amethyst_block.resonate 0.6 1.8 |
| `snd/break_burst` | The bubble bursts: the field is broken (break +5). | block.respawn_anchor.deplete 0.9 0.8; block.glass.break 1 0.8; block.amethyst_cluster.break 1 0.8; entity.generic.explode 0.5 1.2; block.beacon.deactivate 0.7 0.8 |
| `snd/groggy_wobble` | Tilt and damped wobble (break +5..+34): metallic groan. | block.anvil.place 0.4 0.5; block.chain.step 0.6 0.6; block.heavy_core.place 0.4 0.6; block.respawn_anchor.deplete 0.4 0.6 |
| `snd/groggy_spark` | Slow sparks while groggy (every 30-40 t; quiet). | block.copper_bulb.turn_off 0.3 1.4; entity.blaze.burn 0.2 1.8; block.amethyst_block.step 0.3 1.6 |
| `snd/recover` | Re-level and core flip back to cruise (groggy end): clockwork. | block.piston.contract 0.7 0.9; block.crafter.craft 0.7 1; block.chain.place 0.7 1; block.vault.activate 0.5 1.1; block.beacon.power_select 0.4 1.2 |
| `snd/lift_off` | Lift-off pulse when the field ends unbroken (field end +23). | entity.breeze.wind_burst 0.8 0.7; block.beacon.activate 0.6 1.2 |
| `snd/pack_up` | Lances deploy and the device packs into the compact form (field end): mechanical whirr. | block.piston.extend 0.6 1.3; item.spyglass.use 0.5 0.8; block.chain.place 0.6 0.9; block.vault.close_shutter 0.6 0.9 |
| `snd/death` | Death: the seam flickers out and the stack collapses (no voices). | block.beacon.deactivate 1 0.7; block.respawn_anchor.deplete 0.8 0.6; block.vault.deactivate 0.8 0.8; block.chain.break 0.6 0.7 |
| `snd/death_fall` | Halo, pods and ring hit the floor (death). | block.anvil.land 0.7 0.6; block.heavy_core.place 0.8 0.5; block.chain.fall 0.6 0.8; block.copper.fall 0.5 0.8 |
| `snd/death_fade` | The device scales out with gold sparks (death tail). | block.amethyst_block.chime 0.6 1.4; entity.firework_rocket.twinkle 0.4 1.2; block.beacon.deactivate 0.5 1.6 |

## 7. Presets (`fx/p/<name>`)

Ready-made bundles of cards + particles for every event of plan.md. Non-macro unless args are listed. "Cards" = fx cards
per call (all expire within the preset's life; checked by the mcsim suite). Ambient presets are skipped from 40 live fx
cards on (§1).

| preset | args | cards | what / where (executor context) |
|---|---|---|---|
| `p/spark` | - | 1 | A small gold spark burst (tells, clicks, impacts). Billboard. |
| `p/flash` | - | 1 | A white-gold glow flash (any bright moment). Billboard. |
| `p/dust_puff` | - | 2 | A tan dust puff on the floor (landings, scrapes). At the floor point. |
| `p/awake` | - | 4 | Entrance E0 activation: gold flare and electric arcs at the top hub, small ring lights. At the hub. |
| `p/unfold` | - | 8 | Entrance +8..+14: the four pods unfold under the ring (sparks and dust at each pod). At the ring centre, rotated as the device. |
| `p/crown_flare` | - | 3 | Entrance +12..+30: a gold flare as the crown assembles (call 2-3 times). At the hub top. *(ambient: skipped from 40 live cards)* |
| `p/eye_open` | - | 2 | Entrance +38: the red-gold eye opens (glint and glow). At the eye. |
| `p/rise` | - | 4 | Entrance +64..+94 (and other lift-offs): a soft gold ground ring and dust under the rising device. At the floor point under it. |
| `p/ports_glow` | - | 0 | C1 +10: gold dust under the ring as the bomb ports light up. At the ring centre, rotated as the device. The rig's charge look lights the ports themselves and the module adds one glow card (`K.card('glow')`) on each of its rig's 8 port anchors, for 4 t (2 t and a 2 t fade: the still cards are gone 2 t into the run glide) (fix round FID-3: the old fixed ring of 8 glow cards sat at r 1.9 inside the ring hole, 0.7-1.4 b from the rig's ports). |
| `p/bomb_drop` | h | 2 | C1: a bomb falls {h} blocks from its port onto the floor point in 5 t with a short gold streak (call at the floor point; the bomb starts h above). |
| `p/bomb_burst` | - | 3 | C1 bomb burst r 1.3: gold spiky burst, scorch mark, dust and sparks. At the floor point. |
| `p/column_tell` | h | 3 | C1 / C2 slam tell (13 t): the gold column from the face-down core to the floor, a floor glow and a base flare. At the floor point under the core; {h} = the core height above the floor. (The module uses `column_base` since the fix round: the rig draws the column under the moving device.) |
| `p/column_base` | - | 1 | C1 / C2 slam point: the late base flare where the rig's gold column meets the floor (the footage's flare at the column foot, v1 9.10); the module calls it 12 t into the slam, 5 t before the impact. At the floor point. (10-20: the 15 t floor glow and the end rods were dropped; fix round FID-5.) |
| `p/plunge` | - | 6 | C1 / C2 plunge (3-4 t): speed lines streaming up past the dropping device. At the ring centre. |
| `p/slam` | - | 18 | C1 / C2 slam impact r 5: gold crystal-shard burst, shock ring, flash, dust ring. At the floor point. |
| `p/pods_drop` | - | 2 | C3 +0..+4: a medallion drops beside the core (clank sparks). At the medallion. |
| `p/laser_charge` | - | 5 | C3 spark charge (18 t): gold glints spin on a pod, an arc and a growing glow (call 3-4 times). At the medallion. |
| `p/aim_line` | len | 1 | C3 +22: a thin white aim line flickers from the muzzle along the beam for 2 t ({len} = the beam length). At the muzzle, rotated as the beam (yaw and pitch). |
| `p/laser_fire` | len | 3 | C3 +24 fire: the muzzle ring and the beam bloom (about 1 b wide for 3 t, {len} = the beam length). At the muzzle, rotated as the beam. |
| `p/laser_spot` | - | 2 | C3 beam floor spot (call every 2-3 t at each spot): scorch, a gold glow and sparks. *(ambient: skipped from 40 live cards)* |
| `p/laser_end` | - | 2 | C3 beams off: a power-down spark and smoke at the muzzle. |
| `p/tip_flare` | - | 4 | C4 tell 1 (8 t; also the next-pattern tell): a gold 4-point starburst with electric arcs. At a spike tip. |
| `p/vent_shaft` | - | 4 | C4 tell 2 (13 t): the vertical gold light shaft vents up from the hub, vent flames. At the hub top. |
| `p/missile_launch` | - | 2 | C4 launch (each missile): vent flame and smoke puffs. At the vent. |
| `p/missile_trail` | - | 1 | C4 smoke trail puff left behind a missile (call every 3 t at the missile prop). *(ambient: skipped from 40 live cards)* |
| `p/missile_impact` | - | 3 | C4 impact r 1.5: gold crystal-spike burst, a floor glow and dust. At the floor point. |
| `p/core_spark` | - | 3 | C5 tell 1: a gold spark on the core with arcs. At the core. |
| `p/core_lift` | - | 6 | C5 +5 "번쩍": a gold flame burst around the core as it lifts. At the core. |
| `p/up_beam` | - | 4 | C5 +29..+40: the upward gold beam from the raised core with crawling arcs. At the core. |
| `p/rim_flare` | r | 2 | C5 +36..+41: the rim at the final radius {r} flares bright (last warning). At the floor centre. (10-20: the ripples are drawn at the scale 2 r through the internal `p/e/rim_flare` (storage `rlk:fgkit fl`); the 1 b ripple sprite drew them at r / 2 before.) |
| `p/column_down` | h | 2 | C5 +41..+44: the gold column down from the core through the violet pendulum glow. At the floor point under the core; {h} = the core height. |
| `p/floor_hit` | - | 10 | C5 +44: the column hits the floor centre: gold crystal-shard burst. At the floor centre. |
| `p/blast` | r | 4 | C5 +48 full-area blast over radius {r}: a white-gold flash over the disc, the jagged gold crack ring at the rim, a shock ring (pair with p/rocks). At the floor centre. |
| `p/rocks` | - | 12 | C5 +48..+77: about a dozen floor rocks launched across the disc hover, then drift down. At the floor centre (spread r 2-11). |
| `p/dip` | - | 3 | C6 +0: the dip and roll toward the player (dust kicked up and two speed lines). At the floor point under the device, rotated as it. |
| `p/vent_flare` | - | 4 | C6 +12 (8 t): the vent flare bursts up from the top centre as the medallions are flung. At the hub top. |
| `p/tower_up` | - | 7 | C6 +20 (18 t): gold sparks race up the telescoping tower. At the ring centre. |
| `p/flame_band` | - | 8 | C6 charge (17 t): the horizontal gold flame band flares and pulses under the ring (Ø 4.5 -> 8 b) with standing flame licks. At the ring underside. |
| `p/floor_burst` | - | 8 | C6 / F2 floor burst r 1.8: a gold crystal-spike fan, rock chips and a white dust ring. At the floor point. |
| `p/slab_rise` | - | 5 | C6 / F2: a slab tears out of the floor (gold rim glow, dust, chips). At the floor point. |
| `p/slab_throw` | - | 3 | C6 / F2 throw: white-gold streaks as the slab is flung. At the slab, rotated along the throw. |
| `p/slab_trail` | - | 1 | C6 / F2: a short white-gold streak behind a flying slab (call every 2 t at the slab prop, rotated along its flight). *(ambient: skipped from 40 live cards)* |
| `p/slab_impact` | - | 7 | C6 / F2: a slab crashes onto the floor (dust, chunks, a gold glow). At the floor point. |
| `p/revert` | - | 3 | C6 end: the tower folds back (sparks and a small dust ring). At the ring centre. |
| `p/halo_flip` | - | 4 | Field +0..+12: the halo flips upright (whirling gold streaks). At the halo. |
| `p/warp_out` | - | 6 | Field +13 warp-out: the 1-2 frame white-cyan pillar where the device was, glitch streaks start, gold dust on the floor. At the floor point under it. |
| `p/glitch` | - | 3 | Field +14..+33: violet glitch streaks drift up and out over the old spot (call every 4-5 t). At the old spot (floor). *(ambient: skipped from 40 live cards)* |
| `p/warp_in` | - | 3 | Field +34 warp-in at the arena centre: a white-cyan bloom and a violet ring. At the core. |
| `p/warp_pillar` | - | 2 | A white-cyan warp pillar standing on the floor (warp-in, the field arrival). At the floor point. |
| `p/field_unfold` | - | 6 | Field +35..+51: the violet column grows under the core, violet tendrils whip out, a violet glow. At the core. |
| `p/field_idle` | - | 1 | Field idle (every 10-20 t): violet crackle under the core. At the core. *(ambient: skipped from 40 live cards)* |
| `p/pebbles` | - | 6 | Field (every 20 t around the player): pebbles float up slowly, the low-gravity cue (r 1.5-5 around, never at the eyes). At the player's feet. *(ambient: skipped from 40 live cards)* |
| `p/gold_streaks` | - | 5 | Field charge cue: gold streaks rise from the floor around the device (r 2-6). At the floor point under it. *(ambient: skipped from 40 live cards)* |
| `p/wave_charge` | t | 4 | 「인력 충격파」 charge: the yellow sphere grows around the lower core over {t} ticks with a glow and arcs (24 t, the third 40 t). At the core. |
| `p/wave_pulse` | - | 4 | 「인력 충격파」 charge pulse (call every 8 t of the charge): streaks converge on the sphere and a glint flares. At the core. |
| `p/wave_beam` | h | 2 | 「인력 충격파」 the 1-2 tick vertical gold beam core -> floor with a floor splash ({h} = the core height). At the floor point under the core. |
| `p/wave_burst` | - | 4 | 「인력 충격파」 burst: the white-gold flare dome (4 b wide, 2 b tall), then the filled fire disc r 1.8 (5 t) where the ring starts. At the floor point. |
| `p/wave_band` | r0, r1, w, dur | 16 | 「인력 충격파」 the expanding gold-fire ring: 16 band segments (flat burning strip + standing flame wall) travel from radius {r0} to {r1} in {dur} ticks keeping the band {w} deep (tenths of a block / ticks, like the hazards). Call it on the tick BEFORE the strike: it then starts moving in the strike tick, with the tele/wave front and the hz/ring front. At the floor centre. |
| `p/wave_fire` | r | 0 | 「인력 충격파」 flames and embers on the travelling front at radius {r} blocks (particles only; call every 3 t with the front radius). At the floor centre. |
| `p/erupt_tell` | - | 0 | F1 감소 영역: the dark dust settling over a zone as its dark disc appears (10-20: the disc itself is the decal `tele/dark` r 0.8 → 2.8 over 6 t, at the zone's true radius; the old card drew r 1.4). At the zone floor point. |
| `p/slab_glint` | - | 2 | C6 / F2 throw tell (10 t before the throw, at the lock): a gold glow and a white-gold glint on the hovering slab itself, not on the floor (10-20: the throw lanes are gone). At the slab. |
| `p/erupt` | - | 9 | F1 eruption r 2.8: the gold burst mound with floor chunks, a crack ring, flung rocks and dust. At the zone floor point. |
| `p/debris` | - | 5 | After an eruption: a few chunks hover 0.3-2.5 b over the zone, then drift down. At the zone floor point. *(ambient: skipped from 40 live cards)* |
| `p/meter_glint` | - | 2 | Break meter: the crack glint on the bubble at each count. At the core. |
| `p/bubble_crack` | - | 5 | Break meter stage (counts 5, 10, 15): a big crack flash, glass flakes and a glow. At the core. |
| `p/bubble_glow` | - | 2 | Break +0..+5: the cracked bubble lights up white-gold before it bursts. At the core. |
| `p/break_burst` | - | 15 | Break +5: the bubble bursts: a white flash, flying glass shards, a big crack glint and a thin ring. At the core. |
| `p/break_ring` | - | 2 | Break +5: the horizontal gold spark ring expands at floor level (r 9 in 9 t). At the floor point under the core. |
| `p/groggy_sparks` | - | 2 | Groggy (every 30-40 t): slow sparks drip from the slumped core with a wisp of smoke. At the core. *(ambient: skipped from 40 live cards)* |
| `p/sink_dust` | - | 5 | Break +34: the device sinks low (dust ring under it). At the floor point under it. |
| `p/recover` | - | 4 | Groggy end: re-level and the core flips to the top (a gold ring flash and sparks). At the core. |
| `p/lift_off` | - | 5 | Field end (unbroken) +23: the lift-off pulse under the device (white-gold burst, r 3 ring, dust). At the floor point under it. |
| `p/pack_up` | - | 3 | Field end: sparks as the lances dock and the device packs into the compact form. At the ring centre, rotated as the device. |
| `p/death_flicker` | - | 2 | Death: one flicker of the dying seam (call 3 times, 4-6 t apart). At the core. |
| `p/death_fall` | - | 9 | Death: the ring lands tilted on the floor (dust ring, chunks). At the floor point under it. |
| `p/death_fade` | - | 8 | Death tail (every 10-15 t while it scales out): gold motes and sparks rise. Around the core. *(ambient: skipped from 40 live cards)* |

Python: `K.fx('slam')`, `K.fx('bomb_drop', h=3.8)`, `K.tele_dark(3.5, 12.0, 41, 26)` (was the preset `dark_disc`, removed 10-20),
`K.fx('wave_band', r0=25, r1=210, w=25, dur=34)` (tenths / ticks), `K.fx('wave_charge', t=24)`.

## 8. Python API (`tools/build_mboss_fg_fx.py`)

```python
import build_mboss_fg_fx as K          # tools/ is on sys.path in the module generators
K.card(kind, pos='~ ~ ~', rot='~ ~', bb='fixed', roll=0, spin=0, s0=0.0, s1=1.0, move=(0, 0, 0), life=8, fade=0,
       col=K.WHITE, dly=0, dur=0, hit=-1, col2=-1, off=None)   # -> 'function rlk:mboss/fieldgen/fx/card {...}' (cardx when needed)
K.tele_disc(r, tell, el=5, hold=3); K.tele_ring(r0, r, tell, el=5, hold=3)
K.tele_sector(r, half_angle, tell, el=5, hold=3); K.tele_line(length, width, tell, el=5, hold=3, back=0.0)
K.tele_wave(r0, r1, w, tell, dur, el=9, hold=2)
K.tele_mline(mid, length, width, tell, el=5, hold=0, back=0.0); K.tele_mline_aim(mid); K.tele_mline_turn(mid, d)
K.tele_mline_end(mid)
K.snd(name); K.fx(name, **args); K.look(kind, col=K.WHITE); K.prop(name); K.hud(name, **args)
K.KINDS, K.PRESETS, K.SOUNDS, K.PROPS, K.GLYPHS, K.AMBIENT, K.METER_PITCH, K.TELE_COL   # tables
K.glyph('badge'), K.pips(12, flash=True), K.digits('12/20')                            # literal HUD strings
K.part / K.dust / K.dust_fade / K.flash / K.blockp                                     # vanilla particle lines
K.CAP, K.TCAP, K.SOFT                                                                  # 64 / 40 / 40
K.RIG()                                                                                # the rig function prefix in use
```
Card macro values may be placeholders inside a macro preset (`life='$(life)'`, `s1='$(r)'`, `move=(0, '-$(h)', 0)`;
with placeholders give the absolute end as `move` and the start as `off`). Every builder asserts its name exists.

## 9. Stub rig and demos

`tools/mboss_fg_fx_stub_rig.py` writes `F:mboss/fieldgen/fx/rig_stub/**` with the whole rig API the task fixed
(`init, spawn, tick, kill, uninstall, play/<19 clips>, form/<7 forms>, look/<5 looks>, crack/<0..4>, face/player,
face/track, flash, prop/clear`): clips only keep time (lengths, loops and `next` as the clip list), forms move a crude
vanilla stand-in (sandstone ring, gold core, the kit's bubble overlay, amethyst halo, two gold spikes, a lightning-rod
pendulum, the kit's violet column) to the rest heights of model.md §8; `crack/<k>` swaps the bubble overlay to
`bubble<k>` (4 hides it). Its parts carry `rlk_fk_rs` (never the real rig's tags), objectives `fkRsC fkRsT fkRsF fkRsL
fkRsY fkRsK`.

**Removal:** once `wip/fg-rig` is merged (`tools/mboss_fieldgen_rig_manifest.json` present), rerun the kit generator:
it calls `rlk:mboss/fieldgen/rig/…`, no longer imports the stub module, and removes `fx/rig_stub/` (an owned path). Then
delete `tools/mboss_fg_fx_stub_rig.py`. Before that, check the real rig's `crack/<n>` runs as the anchor (the body), as
the stub's does.

**Done (FGI2, wip/fg):** the rig is merged; the kit generator was rerun (`rig real`: `K.RIG()` = `rlk:mboss/fieldgen/rig/`,
`fx/rig_stub/` removed), `tools/mboss_fg_fx_stub_rig.py` is deleted and the generator now asserts the rig manifest
(`build_datapack`). The real rig's `crack/<n>` runs as the anchor (`scoreboard players set @s fgRigCrack <n>` + the bubble
model swap in the field look), so `hud/meter_hit` as the body cracks it; the module core's `KIT_CRACKS` is true and the
core only cracks a stage the kit skipped. `test_fg_fx.py` logs the real rig's calls (not run: fixed-UUID parts) and
checks the crack calls as calls of `rig/crack/1..3` as the body (stub-era version: `test_fg_fx.pre_rig.py`). The demos
(`test/stage` etc.) now spawn and play the real rig. Clip lengths in the section 10 headings are still the first stub's;
the module reads the real ones (fg_contract.md section 18 has the table).

Demos (`execute as @p at @s rotated ~ 0 run function rlk:mboss/fieldgen/fx/test/stage`, then
`…/fx/test/demo/<name>`): `entrance, bombs, laser, missiles, blast, rocks, field, waves, erupt, break, death`. Each sets
the rig form, plays the clip and fires the kit calls of §10 at the plan's ticks around the anchor 9 b ahead.
`test/stop` removes the anchor and the rig.

## 10. Usage per pattern (plan.md)

Notation: `t` = the pattern clock (the clip tick); **body** = `execute as <body> at @s rotated as @s rotated ~ 0 run …`
(the husk on the floor under the axis); **ring** / **hub** / **core** = body + `positioned ~ ~<h> ~` at the heights of
§1; **floor** = a floor point (y = the floor top) `rotated` as the aim; **P** = a position locked from the player;
**prop** = `execute as <prop> at @s rotated as @s run …`. `K.` = the Python helpers of §8. Every hit keeps its framework
hazard (`hz/*` with `#hzQuiet 1`) or projectile; only the fx are shown. Telegraph `tell` = hit tick − call tick ≥ 10.
Clip lengths in the headings are the stub's (the clip list of the task); the real rig manifest's event ticks rule —
move a row with its event, not with the absolute tick. Since the telegraph rule (10-20) the module no longer calls the
`tele_disc` / `tele_line` / `tele_wave` / `tele_mline*` rows below (only C5's rim + dark disc, F1's dark disc and the
slam's base flare remain; the C6 / F2 throws get `p/slab_glint` on the slab instead of a lane).

### Entrance (`entrance`, 130 t; untargetable until about t94)
| t | where | calls |
|---|---|---|
| 0 | hub (dormant, about 2.2 up) | `K.fx('awake')`, `K.snd('awake_clank')` |
| 8 | ring centre | `K.fx('unfold')`, `K.snd('unfold')` |
| 14, 22 | hub top | `K.fx('crown_flare')`; `K.snd('gear_click')` at 20, 30 |
| 38 | eye (core) | `K.fx('eye_open')`, `K.snd('eye_open')` |
| 64 | floor under it | `K.fx('rise')`, `K.snd('rise_hum')` (the rise to cruise height, about 2.9 b) |

### C1 일점 상쇄 / 폭격 (`bomb_run`, 97 t) and C2 내려찍기 (`slam`, 45 t)
| t | where | calls |
|---|---|---|
| 10 | ring centre | `K.fx('ports_glow')`, `K.snd('bomb_port')` |
| each drop − 5 (≥ 10 t lead) | the bomb's predicted floor point | `K.tele_disc(1.3, impact − t)` (+ `hz/disc` same tell) |
| each drop (every 2-3 t, 20 bombs over 45 t) | its floor point | `K.fx('bomb_drop', h=<port height>)`, `K.snd('bomb_drop')`; `K.snd('bomb_fall')` once per volley group of 4 |
| each impact (drop + 5-6) | the floor point | `K.fx('bomb_burst')`, `K.snd('bomb_burst')` (every 2nd bomb is enough) |
| T0 (finisher / C2 start) | floor under the face-down core | `K.fx('column_tell', h=4.6)`, `K.snd('column_tell')`, `K.tele_disc(5.0, 13 + plunge)` (the module since the fix round: `K.fx('column_base')` at the locked point 3 t in, the rig's column under the device) |
| T0 + 13 | ring centre | `K.fx('plunge')`, `K.snd('plunge')` |
| T0 + 16 (the strike) | floor | `K.fx('slam')`, `K.snd('slam')` |
A real bomb prop (if the core flies one instead of `bomb_drop`): `K.prop('bomb')`.

### C3 코어 / 레이저 빔 (`laser`, 174 t)
| t | where | calls |
|---|---|---|
| 0 | each medallion | `K.fx('pods_drop')`; `K.snd('pods_drop')` at the ring |
| 0 | pivot (floor under the axis), rotated as each beam | `K.tele_mline(0, 5.8, 0.8, 24, hold=133, back=-2.8)` and `K.tele_mline(1, …)` (the lanes of the two beams) |
| 4, 9, 14, 19 | each medallion | `K.fx('laser_charge')`; `K.snd('laser_charge')` at 4 |
| 22 | muzzle, rotated as the beam | `K.fx('aim_line', len=<beam length>)` |
| 24 | muzzle | `K.fx('laser_fire', len=…)`, `K.snd('laser_fire')`; the beam props `K.prop('laser_core')` + `K.prop('laser_glow')` (scale y = length; glow x / z 0.5 → 1.0 → 0.5) |
| 25-157, every tick | – | re-aim the hazards (`hz/aim`), then `K.tele_mline_aim(id)` rotated as each, or `K.tele_mline_turn(0, 5)` / `(1, -5)` |
| every 2-3 t | each floor spot | `K.fx('laser_spot')`; `K.snd('laser_loop')` every 10 t |
| 157 | muzzles | `K.fx('laser_end')`, `K.snd('laser_stop')`, `K.tele_mline_end(0)`, `K.tele_mline_end(1)` |

### C4 바위 폭탄 / 미사일 (`missiles`, 73 t)
| t | where | calls |
|---|---|---|
| 0 | both spike tips | `K.fx('tip_flare')`, `K.snd('tip_flare')` |
| 8 | hub top | `K.fx('vent_shaft')`, `K.snd('missile_vent')` |
| 25-39 (10 launches over 14 t) | the vent | `K.fx('missile_launch')`, `K.snd('missile_launch')`; the projectile `K.prop('missile')` (aim with `tp … facing`) |
| every 3 t of a flight | the missile prop | `K.fx('missile_trail')` |
| at the dive | – | `K.snd('missile_dive')` once per volley group |
| late lock, ≥ 10 t before each impact | P | `K.tele_disc(1.5, impact − t)` |
| impact | floor | `K.fx('missile_impact')`, `K.snd('missile_impact')` |

### C5 지면 충격 / 중력 폭발 (`coreup`, 110 t; blast +48)
| t | where | calls |
|---|---|---|
| 0 | core (7.8 up in core-up) | `K.fx('core_spark')`, `K.snd('core_spark')`; `K.snd('core_flip')` at the flip |
| 3 | arena centre floor | `K.tele_disc(12.0, 45)` (R = 1.7 D, clamped inside the arena; strike +48) |
| 5 | core | `K.fx('core_lift')`, `K.snd('core_lift')` (+ `K.hud('flash_gold')` if wanted) |
| 7 | floor centre | `K.tele_dark(3.5, 12.0, 41, 26)` (the darker floor grows to R by +33; 10-20: a decal, and `tele_rim(12.0, 45)` at 3 replaces the `tele_disc`) |
| 29 | core | `K.fx('up_beam')`, `K.snd('up_beam')` |
| 36 | floor centre | `K.fx('rim_flare', r=12.0)` |
| 41 | floor centre | `K.fx('column_down', h=7.8)`, `K.snd('column_down')` |
| 44 | floor centre | `K.fx('floor_hit')` |
| 48 | floor centre | `K.fx('blast', r=12.0)`, `K.fx('rocks')`, `K.snd('blast')`; `K.snd('rocks_hover')` at 54, 64; `K.snd('debris_land')` at 77 |

### C6 파쇄 / 바위 날리기 (`tower_throw`, 157 t) and F2 (field form, without the tower build-up)
| t | where | calls |
|---|---|---|
| 0 | floor under it, rotated as it | `K.fx('dip')`, `K.snd('dip')` |
| 12 | hub top | `K.fx('vent_flare')`, `K.snd('vent_flare')` |
| 20 | ring centre | `K.fx('tower_up')`, `K.snd('tower_up')` |
| 40 | ring underside | `K.fx('flame_band')`, `K.snd('flame_charge')` |
| burst − 10 (8 bursts 6 t apart, walking onto the player) | P | `K.tele_disc(1.8, 10)` |
| each burst | floor | `K.fx('floor_burst')`, `K.snd('floor_burst')`; burst + 2 `K.fx('slab_rise')`, `K.snd('slab_lift')` |
| throw − 10 (4-6 throws 8 t apart) | the slab's floor point, rotated at the player | `K.tele_line(<reach>, 1.6, 10)` |
| each throw | the slab, rotated along the throw | `K.fx('slab_throw')`, `K.snd('slab_throw')`; the projectile `K.prop('slab')`; `K.fx('slab_trail')` every 2 t |
| each landing | floor | `K.fx('slab_impact')`, `K.snd('slab_impact')` |
| end (15 t) | ring centre | `K.fx('revert')`, `K.snd('revert')` |

### Field: warp and unfold (`warp_out` 34 t → `warp_in_field` 23 t → `field_idle`)
| t | where | calls |
|---|---|---|
| 0 | halo (ring + 1.6) | `K.fx('halo_flip')`, `K.snd('halo_flip')` |
| 13 | floor under the old spot | `K.fx('warp_out')`, `K.snd('warp_out')` (+ `K.hud('flash_white')` optional) |
| 14, 19, 24, 29 | old spot (floor) | `K.fx('glitch')`; `K.snd('glitch')` at 16 |
| 34 | arena centre: core (3.84) / floor | `K.fx('warp_in')`, `K.snd('warp_in')`; `K.fx('warp_pillar')` at the floor |
| 35 | core | `K.fx('field_unfold')`, `K.snd('field_unfold')`; `K.hud('meter_open')`, `K.hud('lowg_on')`, `<RIG>crack/0` |
| 57 | – | `K.hud('banner_field')` (+ `K.hud('hint_on')` the first field) |
| 57, then every 20 t | each player's feet | `K.fx('pebbles')` |
| 60 | floor under it | `K.fx('gold_streaks')` |
| every 10-20 t of the field | core | `K.fx('field_idle')`; `K.snd('field_hum')` every 40 t |

### 「인력 충격파」 ×3 (`wave`, 60 t each; gaps 68 / 83 t; the 3rd charges 40 t; < 50 % HP: 3 fronts 9 t apart)
| t (strike S = t0 + tell) | where | calls |
|---|---|---|
| t0 | core | `K.fx('wave_charge', t=<tell>)`, `K.snd('wave_charge')`; `K.fx('wave_pulse')` every 8 t |
| t0 | arena centre floor | `K.tele_wave(2.5, 21.0, 2.5, <tell>, 34)` (+ `hz/ring`, `#hzNoDodge`, `hz/resize` from S) |
| S − 10 | core | `K.snd('wave_charge2')` |
| S − 1 | floor centre | `K.fx('wave_band', r0=25, r1=210, w=25, dur=34)` (moves from S, with the decal and the hazard) |
| S | floor centre | `K.fx('wave_beam', h=3.84)`, `K.snd('wave_beam')` |
| S + 1 | floor centre | `K.fx('wave_burst')`, `K.snd('wave_burst')` |
| S + 3k (k = 0..11) | floor centre | `K.fx('wave_fire', r=2.5 + 0.55 × 3k)`; `K.snd('wave_ring')` every 3 t at the front point nearest the player |
| triple: S + 9, S + 18 | floor centre | each extra front: `K.tele_wave(2.5, 21, 2.5, 10, 34)` 10 t before, `wave_band` 1 t before |

### F1 감소 영역 (`field_erupt`, 30 t; 9 events 11-50 t apart, 1-4 discs each)
| t | where | calls |
|---|---|---|
| 0 | each zone floor point (2-8 b from the player) | `K.fx('erupt_tell')`, `K.tele_dark(0.8, 2.8, 15, 6)` (10-20: was `K.tele_disc(2.8, 15, 9)`); `K.snd('erupt_tell')` once |
| 15 | each zone | `K.fx('erupt')`; `K.snd('erupt')` once |
| 18 | each zone | `K.fx('debris')`; `K.snd('debris_land')` at 40 |

### Field end, unbroken (`field_end`, 102 t): the closing waves as above, then
| t | where | calls |
|---|---|---|
| 0 | – | `K.hud('meter_close')`, `K.hud('lowg_off')` |
| 23 | floor under it | `K.fx('lift_off')`, `K.snd('lift_off')`, `K.snd('rise_hum')` |
| pack-up | ring centre | `K.fx('pack_up')`, `K.snd('pack_up')` |

### Break (20 hits; `break`, 34 t), groggy (`groggy`, 200 t), recover (`recover`, 15 t)
| t | where | calls |
|---|---|---|
| each count | as the body, at the core | `#fkM` = count, `K.hud('meter_hit')` (stages at 5 / 10 / 15) |
| 0 (count 20) | – | cancel: `fx/tele/clear`, `K.hud('banner_end')`, `K.hud('meter_close')`, `K.hud('lowg_off')`, `K.hud('hint_off')` |
| 0 | core | `K.fx('bubble_glow')`, `K.snd('break_glow')` |
| 5 | core / floor under it | `K.fx('break_burst')`, `K.fx('break_ring')`, `K.snd('break_burst')`, `K.hud('pop_break')`, `K.hud('flash_gold')`, `<RIG>crack/4` |
| 14 | ring | `K.snd('groggy_wobble')` |
| 34 | floor under it | `K.fx('sink_dust')`; `K.hud('groggy_on')` |
| groggy, every 30-40 t | core (about 3.0 up) | `K.fx('groggy_sparks')`, `K.snd('groggy_spark')` |
| recover | core | `K.hud('groggy_off')`, `K.fx('recover')`, `K.snd('recover')`, `K.snd('core_flip')` |

### Death (`death`, 110 t; mechanical sounds only)
| t | where | calls |
|---|---|---|
| 0, 5, 10 | core | `K.fx('death_flicker')`; `K.snd('death')` at 0; `fx/tele/clear`, `K.hud('meter_close')`, `K.hud('lowg_off')` |
| 50 | floor under it | `K.fx('death_fall')`, `K.snd('death_fall')` |
| 70, 85, 100 | core | `K.fx('death_fade')`; `K.snd('death_fade')` at 85 |

## 11. Budgets

Measured by `fxtests/test_fg_fx.py` §16 (mcsim; the timelines above with every card and decal; each non-ambient preset
must spawn all its cards, ambient skips are counted):

| moment | peak fx cards (cap 64) | telegraph cards (cap 40) | ambient calls skipped |
|---|---|---|---|
| C1 bombs + slam | 32 | 16 | 0 |
| C3 lasers | 24 | 10 | 0 |
| C4 missiles | 35 | 20 | 0 |
| C5 gravity blast | 27 | 2 | 0 |
| C6 rocks | 30 | 14 | 0 |
| field waves x3 (triple third) + pebbles | 59 | 10 | 2 |
| F1 eruptions | 47 | 14 | 8 |
| break | 19 | 0 | 0 |
| entrance | 12 | 0 | 0 |
| field warp | 14 | 0 | 0 |

The card engine costs, per tick and only while cards live: one `@e[type=item_display,tag=rlk_fk]` pass with a few score
comparisons per card and at most one NBT merge per card per stage. Telegraphs need no ticking beyond that (client
interpolation draws the fills and the wave front); moving lines cost one teleport per card per re-aim.

## 12. Verification

- `scratchpad/mb3/fxtests/test_fg_fx.py <worktree>/roguelike` (mcsim, 1198 checks): every summoned card's SNBT
  parses; card / cardx stage ticks (show, go, hit, fade, kill) and the first-tick fix; `off`; the fill reaching the rim on
  the hit tick; sector snapping and the disc fallback; the three palettes; ring, line (negative `back`), wave (front in
  sync with the hazard every tick; band edge; violet default), moving line (caps tag, aim / turn / end); `wave_band`
  geometry and its sync when called at strike − 1; both caps and telegraphs drawn while the fx cap is full; `clear`;
  the dead-player clear; every preset (runs, card count = the manifest, all expire); every sound layer (vanilla, no
  voices, pitch range, the meter notes); HUD (pips, "12/20", the 4 t flash end, `#fkHudV`, crack stages calling the rig
  as a non-player, 20/20 clamp, flags, `put_*`, titles, banner); every prop look; the stub rig; every demo; the pattern
  budgets; `uninstall`.
- `scratchpad/mb3/fxtests/run_kit.sh <worktree>/roguelike` (with `RP=<unpacked RP>`), the harness of
  `mb2/tests/run_all.sh`: the suite above; the butterfly kit suite `mb2/fxtests/test_fx_engine.py` unchanged and green on
  this tree; idempotency (the generator twice: datapack and RP hashes stable) and the butterfly kit / module files
  byte-identical to f2ab515; validators compared with the f2ab515 baseline by `vcheck.py`: `check_refs`, `check_macro`
  (from the datapack root), `check_nbtpath` (0 invalid), `tools/check_mboss_pack.py` (0 problems), `lint_mc`. The kit's
  only new validator findings are the butterfly kit's known false-positive classes, listed in
  `fxtests/baseline/{macro,lint}_kit.txt` (`function … with storage` read as a call without args; `time query`,
  `execute store … if entity` without `run`, macro placeholders in `fx/e/spawn`); every such call runs in the suite.
- Renders (`scratchpad/mb3/fxrender/render_fg.py`, the mb2 ray caster extended for the cross / band / box planes, `off`,
  the wave ring and moving lines; plaza floor of `tools/build_mboss_arena.py`), in `scratchpad/mb3/renders/`:
  `fx_sprites_marble.png`, `fx_sprites_pink.png` (every fx sprite on both floors), `fx_tele_textures_marble.png`,
  `fx_tele_textures_pink.png`, `fx_telegraphs_top.png` (every shape and palette at 35 % / 75 % / hit − 1 / hit),
  `fx_telegraphs_view.png` (player-eye views), `fx_wave.png` (the wave ring and band over time),
  `fx_presets.png` (the presets), `fx_moments.png` (key moments of the patterns), `fx_hud.png` (the HUD mock-up).

## 13. Later: one shared engine

The butterfly and field generator kits are two near-identical generators (`build_mboss_bf_fx.py`,
`build_mboss_fg_fx.py`). A later refactor should move the common parts — `Writer` and the owned-path cleaner, `card()` /
`cardx`, `engine()` (make / spawn / born / world / age / show / go / hit / fade / axes), `telegraphs()` (disc / ring /
sector / line / mline / wave), the plane model writer (face / flat / seg / cross / band / box), the atlas budget, the
font builder with the collision check, `min_volume` / sound lines, the prop writer and the FxSim test base — into one
`tools/mboss_fx_engine.py` parameterised by namespace, fake-player prefix, tag, storage, font name / codepoint range and
palettes, leaving each boss with its painters, kinds, presets, sounds and HUD lines. Doing it regenerates the butterfly
kit with this kit's engine: it gets the perf-2 first-tick fix (its cards currently pop to `s1` in the spawn tick), `off`,
the new planes and telegraphs and the ambient soft cap, but its outputs are no longer byte-identical and the stage
ticks in `mb2/fxtests/test_fx_engine.py` shift by one tick. Schedule it after both modules are merged, as its own
change; until then the butterfly kit is deliberately untouched.
