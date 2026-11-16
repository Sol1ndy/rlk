# 달빛 환영 나비 FX / audio / HUD kit — API (`bf_fx_api.md`)

Generator: `tools/build_mboss_bf_fx.py` (+ `tools/mboss_bf_fx_paint.py`, the stdlib sprite painters), branch `wip/bf-fx`,
integrated with the module core on `wip/bf` (the core calls it everywhere; notes 1, 3 and 6 below are done there). The
fx polish of `wip/bf-fxpolish` (5b41287: repainted sprites, richer preset visuals and sound recipes; names, arguments,
kinds, extents, texture sizes, caps and card counts unchanged) is merged on `wip/bf`; §3, §6 and §7 describe it. The
tables of §6 and §7 are printed from the generator itself (`scratchpad/mb2/integ2/tools/fxapi_tables.py <dp> 6|7`).
Module authors reach it through `tools/mboss_butterfly/api.py`: `api.K` = this module, `Gen.fx / snd / kcard / tele_* /
kprop / khud` = §8's builders (`kcard` also takes `'#RRGGBB'` or `(r, g, b)` colours).
Manifest written on every run: `tools/mboss_bf_fx_manifest.json` (kinds, presets, props, sounds, glyphs, owned paths, caps).

```
python3 tools/build_mboss_bf_fx.py --resourcepack <unpacked RP>      # datapack + RP (about 18 s, sprite painting)
python3 tools/build_mboss_bf_fx.py --skip-rp                         # datapack only
```

The kit draws; it never decides gameplay. Hits, hazards (`rlk:mboss/hz/*`), projectiles (`rlk:mboss/pj/*`), timings
and the debuff logic stay in the module core. Every function below is visual / audio only and safe to call any time
(during the intro, the fight, the death shell or a test).

## 0. Ownership, hooks, integration

| what | path | owner |
|---|---|---|
| card engine entry points | `F:mboss/butterfly/fx/{card,cardx,look,clear,uninstall}` | this kit |
| internals, presets, telegraphs, sounds, HUD, props, tests | `F:mboss/butterfly/fx/{e,p,tele,snd,hud,prop,test}/**` | this kit |
| the core's own fx files | `F:mboss/butterfly/fx/death_*`, `fx/groggy`, … (any other name under `fx/`) | module core (left alone) |
| sprites / models / item definitions | `assets/rlk/{textures,models/item,items}/mboss/bf_kit/<kind>` + atlas entries `rlk:mboss/bf_kit/*` | this kit |
| HUD font | `assets/rlk/font/mboss_bf.json`, `assets/rlk/textures/font/mboss_bf/*` (U+E600-E6FF) | this kit |
| rig (not touched) | `F:mboss/butterfly/rig/**`, `assets/rlk/*/mboss/butterfly/*` | rig generator |

**Integration notes for the core (read these):**

1. **`clean()` of `tools/mboss_butterfly/core.py` deletes every file under `F:mboss/butterfly/` except `rig/`.** It must also
   spare the kit's paths: `fx/{card,cardx,look,clear,uninstall}.mcfunction` and `fx/{e,p,tele,snd,hud,prop,test}/**`
   (listed under `owned` in `tools/mboss_bf_fx_manifest.json`). The kit's own cleaner only touches those paths, so the
   core's `fx/death_*` / `fx/groggy` survive a kit rebuild.
2. **No `rlk:tick` / `rlk:load` hook is needed.** Cards are aged by `fx/e/world`, which `fx/card` schedules
   (`schedule … 1t replace`) and which re-schedules itself while any card lives. Objectives are created on the first card.
3. Lines for the module hooks:
   - `uninstall`: `function rlk:mboss/butterfly/fx/uninstall` (kills cards, removes objectives `bkS bkG bkH bkK bkD`, storage `rlk:bfkit`, the schedule).
   - `cleanup`: `function rlk:mboss/butterfly/fx/clear` + `function rlk:mboss/butterfly/fx/hud/clear`.
   - `pause`: `function rlk:mboss/butterfly/fx/tele/clear` + `function rlk:mboss/butterfly/fx/hud/flash_end` (the frozen hazards keep their framework markers; the decals would otherwise run on and flash early). A dead or reviving player clears every card by itself (like Navia's cards).
   - `death_start`: `function rlk:mboss/butterfly/fx/tele/clear`.
   - Boss-bar lines (`hud/extra`, `hud/sub` of the core): end them with `function rlk:mboss/butterfly/fx/hud/put_extra` / `put_sub` (§5).
4. Cards carry `rlk_room` + `rlk_mb_aux`, so `cleanup_aux`, the arena sweep, room clears and `rlk:uninstall` remove them too.
5. Fake players live in objective `mb` under the prefix `#bk*` (none collide with the core's `#bf*`); entity tags `rlk_bk*`.
6. The core's former small tinted engine (`F:mboss/butterfly/tc/**`, RP `mboss/bf_fx/*`, `Gen.tcard`) was migrated to
   this kit and removed on `wip/bf`.

## 1. Conventions

- **Executor context.** Every call draws relative to the executing position and rotation. Run it `at`/`positioned` the
  event point and `rotated` as the aim (yaw; pitch 0 unless stated): e.g.
  `execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/p/kick_rise` from the body tick, or
  `execute positioned <floor point> rotated ~ 0 run …` for decals. Floor points are at the floor top (y 201 in the plaza).
- **Display frame** (as Navia's cards): every card is summoned with its own rotation (`rot`) and `right_rotation` free for
  the spin; local axes are **+x = left, +y = up, +z = forward** of that rotation. `move` and `^x ^y ^z` use the same axes.
- **Card coordinates.** `face` kinds lie in the local XY plane (they face forward, or the camera with a billboard);
  `flat` kinds lie in the local XZ plane (horizontal for `rot "~ 0"`, +b = forward); `seg` kinds are face quads pushed
  0.94 forward (dome segments). A painted card's **+a is the local −x (the right)**, +b is up (face) or forward (flat).
- **Crescents** (`cres_*`, flat) are Navia's swing-plane ribbon: pivot at the card origin, the arc ±80° around forward at
  radius 0.48 × size, the thick bright **head at the left**, the tail fading to the right. Positive `spin` turns the
  head-first way (right-to-left). `rot "~ -90"` + `roll 90` stands a crescent in her sagittal plane (arc over her head);
  `rot "~-90 0"` / `"~90 0"` + `roll 90` give the "(" / ")" pair beside her.
- **Radial trick.** A fixed face card with `rot "~<yaw> <90 − elevation>"` has its local +y pointing outward along that
  yaw / elevation, so `move:"0f,<d>f,0f"` flies it outward with its long axis (shard, blade, streak) along the flight.
- **Billboards**: `fixed` (world-oriented), `center` (camera-facing), `vertical` (turns about Y only), `horizontal`.
  `move` on a billboard is in the camera frame (use small vertical moves only).
- **Units**: blocks, ticks, degrees, colours as RGB ints (`16777215` = white = the painted colours unchanged).
  Telegraph sizes are in **tenths of a block** like the framework hazards (`r:35` = 3.5 blocks).
- **Tint** = `minecraft:custom_model_data` colour 0 of the card's item, multiplied into the texture. Painted kinds keep the
  video colours under white; neutral kinds (white / near white) take any colour. The telegraph textures bake their dark
  outline, which stays dark under every tint.
- **Stages** (gametime, counted from the call tick T): visible from T (or hidden until `T + dly`), main interpolation
  `s0 → s1`, `move`, `spin` over `dur` ticks starting at `T + dly + 1` (default: until the fade), tint → `col2` at `T + hit`,
  shrink to nothing over the last `fade` ticks, removed at `T + dly + life`.
  Phase (review fix perf-2): the ager is a `schedule ... 1t` that runs at the end of the **same** server tick as the
  call (ServerLevel.tickTime raises the game time first), so `fx/e/make` counts every stage from game time + 1. The
  main interpolation therefore starts one tick after the summon (the client gets the start state first; merged in the
  summon tick it would never animate), a telegraph flashes on the strike tick and a card lives exactly `life` ticks.
  The suites model this order (`bfsim.run_sched`, `fxtests/test_fx_engine.FxSim.tick`; fix FX-7).
- **Caps**: at most **64** live fx cards (further `card` calls are skipped silently) and **40** live telegraph cards
  (telegraph calls are skipped from 34 on, so a shape is never half drawn). The two are counted apart, so busy fx never
  hide a telegraph.

## 2. Card engine

### `rlk:mboss/butterfly/fx/card` (macro)

| arg | type | meaning |
|---|---|---|
| `kind` | string | a kind of §3 |
| `pos` | string | summon point: `"^x ^y ^z"`, `"~x ~y ~z"` or absolute |
| `rot` | string | rotation of the card: `"~ ~"` = the executor's, `"~30 -90"` = turned 30° to the executor's right and pitched straight up (relative yaw, absolute pitch) |
| `bb` | string | `fixed` / `center` / `vertical` / `horizontal` |
| `roll` | int deg | `left_rotation` about the local z (forward) axis, constant |
| `spin` | int deg | turn about the card normal over the main interpolation, −170..170 |
| `s0`, `s1` | float | start / end size (uniform scale; for crescents the radius is 0.48 × size, for face kinds the size is the width) |
| `move` | string | end translation `"dx f,dy f,dz f"` in the display frame, e.g. `"0f,1.2f,0f"` |
| `life` | int ticks | total life (≥ 2) |
| `fade` | int ticks | shrink-out at the end (≤ life − 2) |
| `col` | int | tint (RGB), `16777215` = none |

### `rlk:mboss/butterfly/fx/cardx` (macro)

Every option: `card`'s args with `s0` / `s1` as vector strings (`"1.2f,3f,1.2f"`) plus

| arg | meaning |
|---|---|
| `dly` | ticks hidden (scale 0) before the card appears at `s0` |
| `dur` | ticks of the main interpolation (`0` = up to the fade) |
| `hit` | ticks after the call when the tint becomes `col2` (`-1` = never) |
| `col2` | second tint (`-1` = none) |

### Others

| function | args | does |
|---|---|---|
| `fx/look` | `{kind, col}` | as `@s` (an item_display the module owns): the kind's item model, tint, full bright; keeps its transformation |
| `fx/prop/<name>` | – | as `@s`: a complete look (item, tint, billboard, scale / transformation) — see §2.1 |
| `fx/clear` | – | kill every kit card (fx + telegraphs), zero the counts |
| `fx/tele/clear` | – | kill the telegraph decals only |
| `fx/uninstall` | – | cards, objectives, storage `rlk:bfkit`, the scheduled ager |
| `fx/test/kinds` | – | every fx kind in rows in front of the executor (`execute as @p at @s rotated ~ 0 run …`) |
| `fx/test/tele` | – | one telegraph of each shape (tell 40) |
| `fx/test/dome` | – | the release dome r 6, 8 blocks ahead |
| `fx/test/presets`, `fx/test/sounds` | – | clickable chat lists |
| `fx/test/hud` | – | both badges, actionbar notice, pop |

### 2.1 Prop looks (`fx/prop/<name>`, as `@s` = the prop)

| prop | look |
|---|---|
| `prop/fire` | B2 fire crescent: `fire_claw`, billboard `center`, 1.4 blocks |
| `prop/vblade` | H4 vacuum blade: `cres_lime` standing **across** the flight (the plane of the `#pjShape 1` hit line; cyclic turn x→y, y→z, z→x, chord ×4.4, bulge ×6.8, translation (−1.9, 1.02, 0)): 4 tall from its lower tip 0.9 below the prop (the pj hit row on the floor) to 3.1 above it, x −1.33..+1.33 (hit hr 1.5), thick head on top; fly the prop 0.9 above the floor. (Before the integration it was rolled 90° about z, i.e. edge-on to the player it flies at, tip 0.22 above the floor; measured by `scratchpad/mb2/integ/vblade_check.py`, views `renders/integ_vblade.png`.) |
| `prop/orb` | B4 orb fallback (if the rig has no orb prop): `sphere` tinted `#D2FA8E`, 1.7 across, billboard |
| `prop/orb_ring` | gyroscope ring (`gyro`, fixed, 2.2 across); turn it each tick from the module (e.g. `rotation` / transformation) |
| `prop/dew` | 달빛 이슬 heal orb: `dew_orb`, billboard, 0.9 across |

Keep `teleport_duration:1` on moving props (the pj library moves them every tick).

## 3. Kinds (sprites)

Atlas added by the kit: **834 560 px** (≤ 1 M), 40 sprites (27 fx + 13 telegraph), every side ≤ 256 and a multiple of 16 (checked by the
generator). Item models `rlk:mboss/bf_kit/<kind>`; every item definition has the `custom_model_data` tint (default white).

| kind | plane | px | extent at scale 1 (blocks) | colour | use |
|---|---|---|---|---|---|
| `cres_lime` | flat | 256x128 | a -0.5..0.5, b 0..0.5 | painted | lime energy crescent ribbon (swing plane, head at the left): a thick ribbon with a white-hot rim, a second energy line, a teal under-ribbon, a wispy broken tail and leaf-blade feathers trailing from the inner edge (kicks, the vacuum blade) |
| `cres_cyan` | flat | 256x128 | a -0.5..0.5, b 0..0.5 | painted | cyan-white crescent ribbon, the same build with crystal-shard feathers (cocoon burst, wind crescents) |
| `cres_fire` | flat | 256x128 | a -0.5..0.5, b 0..0.5 | painted | fire crescent / flame sheet: an orange-gold ribbon with a white-hot rim, a pink under-ribbon and flame-lick feathers, fading to magenta |
| `fire_claw` | face | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | camera-facing fire crescent projectile: a golden hook with a white-hot head and flame licks in a pink haze |
| `star4` | face | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | lime 4-point star flare, white core (no grey halo) |
| `glint` | face | 64x64 | a -0.5..0.5, b -0.5..0.5 | neutral (tint it) | clean white 4-point glint (tint it) |
| `burst` | face | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | lime-white starburst of 24 jagged spikes |
| `glow` | face | 64x64 | a -0.5..0.5, b -0.5..0.5 | neutral (tint it) | soft clean white glow disc, no hard halo rim (tint it) |
| `mote` | face | 32x32 | a -0.5..0.5, b -0.5..0.5 | neutral (tint it) | clean white moonlight mote (tint it) |
| `streak` | face | 256x32 | a -0.5..0.5, b -0.0625..0.0625 | neutral (tint it) | long thin clean white streak along a (tint it) |
| `leaf` | face | 32x32 | a -0.5..0.5, b -0.5..0.5 | neutral (tint it) | leaf / petal flake (tint lime or amber) |
| `bfly` | face | 64x64 | a -0.5..0.5, b -0.5..0.5 | neutral (tint it) | small clean white butterfly outline glyph (tint it) |
| `disc_lime` | flat | 256x256 | a -0.5..0.5, b -0.5..0.5 | painted | Dendro disc decal: a 3-arm lime vortex, bright rim |
| `ripple` | face | 256x256 | a -0.5..0.5, b -0.5..0.5 | neutral (tint it) | ripple / wind ring of tapered wind arcs (near white, tint it) |
| `gyro` | face | 256x256 | a -0.5..0.5, b -0.5..0.5 | painted | comet-lit lime gyroscope ring with beads |
| `sphere` | face | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | translucent light sphere, limb-brightened, with light rays |
| `dome_lo` | seg | 128x112 | a -0.42..0.42, b -0.36..0.36 | painted | saturated dome shell segment with long swirl bands, lower band (ground ring) |
| `dome_hi` | seg | 128x112 | a -0.42..0.42, b -0.36..0.36 | painted | saturated dome shell segment with long swirl bands, upper band (narrow top) |
| `fan_fire` | flat | 256x128 | a -0.5..0.5, b 0..0.5 | painted | 180-degree floor fan of radial flame tongues around a scorched, ember-flecked centre |
| `flame_tongue` | face | 64x128 | a -0.25..0.25, b 0..1 | painted | vertical flame tongue with a forked tip in a pink haze, pivot at its root |
| `flame_puff` | face | 64x64 | a -0.5..0.5, b -0.5..0.5 | painted | soft flame trail puff (no rim) |
| `blade` | face | 64x128 | a -0.25..0.25, b 0..1 | painted | long thin radial lance (the orb-burst spikes, ground blades), pivot at its root |
| `shard` | face | 64x128 | a -0.25..0.25, b -0.5..0.5 | painted | faceted white / cyan crystal shard with a glow |
| `cure_beam` | face | 64x192 | a -0.25..0.25, b 0..1.5 | painted | pale-gold spire-lens beam, pivot at its foot |
| `cure_burst` | face | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | white-gold burst of gold smoke with a double gold ring |
| `cure_emblem` | face | 128x192 | a -0.5..0.5, b -0.75..0.75 | painted | gold emblem in glowing lines: spire, star, scroll arms, crescent |
| `dew_orb` | face | 128x128 | a -0.5..0.5, b -0.5..0.5 | painted | "달빛 이슬" moon-dew heal orb with a teal rim (reads on the marble) |

Since the fx polish every energy sprite is composited in layers: a soft saturated halo whose alpha fades out before the
item shader's 0.1 alpha cut, a streaked translucent body, a near-white core and a thin darker under-tone (teal for
Dendro, mauve for Pyro, dark gold for the cure), so it reads on the white marble as well as on the pink floor and in the
dark cave; the neutral sprites are clean white (no grey halos, no hard halo rims) so a tint shows true. The telegraph
and HUD painters are unchanged. Comparison sheets: `scratchpad/mb2/renders/fxpolish_*.png`.

Telegraph kinds (neutral, unit radius / length: the scale is the size in blocks): `t_rim` (r ≥ 2.6), `t_rim_s` (thick, r ≤ 2.5),
`t_fill`, `t_sec30/45/60/90` (rims), `t_secf30/45/60/90` (fills), `t_bar` (rails / caps), `t_lane` (lane fill).

Hex sources (understand/v1-v4.md): lime crescents #EDF9DA / #E5FBC8 / #D7F899 / #BFF191 / #8DCA85 with the teal underlay
#297272; cyan #F9FDFC / #BAF3E3 / #78D8D1 / #39B4C1; fire #F9E38E / #F8D486 / #F4BA33 / #EB9F26 / #CC6976 → magenta
#C680A2; flare #F8FCE7 / #D8F2BC / #AEE76F; disc #C2ECB0 / #A6E282 / #84C75D; gyro #DCFA9A / #ADE87F / #91CF7E / #26666A;
dome #77D04C / #9FED6B / #C2F999 / #F1FDD9; flame #F09A5F / #F7CC9C / #A46076 / #8C5436, scorch #585542 / #EDC30B;
blades #B4EB68 / #80BD77 / #EAFDD9 / #2C686D; cure #F4EDC9 / #FFF8F3 / #E0DD9C / #D5DD81; 달빛 고치 #8C525C / #D06A60 /
#E8858A.

## 4. Ground telegraphs (`fx/tele/*`, macros)

> **Telegraph rule (10-20):** the butterfly's patterns draw none of these any more: a ground telegraph only where the
> reference footage shows one, and her footage shows none (`S:tele/bf/audit.md`; B3's flame trail keeps its red ember
> line, a plain floor card that lives up to its flare and that B3's own `p/sweep/pause` / `resume` drop and lay again
> around a pause). The API, sprites and `tele/clear` (pause / death safety net) stay.

All four are **visual only**: pair each with the framework hazard of the same shape, made in the same tick with the same
`tell`, and set `#hzQuiet mb 1` before it so the framework particles do not double the decal. The fill's bright edge
reaches the rim exactly on **call tick + tell**, the tick `hz/*` strikes (fill interpolation from T+1 over tell−1 ticks);
on that tick every card of the shape flashes (tint → flash colour), then it stays `hold` ticks and disappears.

| function | args (tenths of a block, ticks) | cards | drawn at |
|---|---|---|---|
| `tele/disc` | `{r, tell, el, hold}` | 2 (fill + rim; thick rim when r ≤ 2.5) | the floor point |
| `tele/ring` | `{r0, r, tell, el, hold}` | 3 (outer + inner rim, a progress ring travelling r0 → r) | the floor point |
| `tele/sector` | `{r, a, tell, el, hold}` — `a` = half-angle; snaps to 30 / 45 / 60 / 90, `a ≥ 136` draws a disc | 2 | the apex, rotated = aim |
| `tele/line` | `{len, w, back, tell, el, hold}` — covers −back..len along the aim, w wide (`hz/line` + `#hzBack`) | 5 (2 rails, 2 caps, the lane fill) | the start point, rotated = aim |

`el` picks the colours (rim / fill / flash): **7 Dendro** `#3FBE16 / #7BE639 / #EEFF6A`, **1 Pyro** `#FF5612 / #FF8A2A /
#FFE04A`, **0 physical** `#E5304A / #FF6474 / #FFB8C4` (any other value draws Dendro). Rims: a 0.035 r dark outline, a
saturated 0.04 r band and a thin dark inner line; fills: 26-44 % translucent with a bright leading edge between two dark
lines — readable on the white marble and on the pink star (renders `fx_telegraphs_*.png`). Layering: fills at floor +0.03,
rims at +0.045.

Example (H2 disc, impact 10 t after the lock at the player's position):
```
execute positioned <P> run scoreboard players set #hzQuiet mb 1
execute positioned <P> run function rlk:mboss/hz/disc {r:25,tell:10,dmg:140}
execute positioned <P> run function rlk:mboss/butterfly/fx/tele/disc {r:25,tell:10,el:7,hold:3}
```
Python: `tele_disc(2.5, 10, el=7, hold=3)`, `tele_ring(r0, r, tell, …)`, `tele_sector(r, half_angle, tell, …)`,
`tele_line(length, width, tell, el=7, hold=3, back=0)` (blocks in, tenths out).

## 5. HUD (font `rlk:mboss_bf`)

| codepoint | glyph | size (texture px → GUI height, ascent) |
|---|---|---|
| U+E600 | 달빛 고치 badge: maroon #8C525C disc, salmon-red #D06A60 rim, salmon #ED928C double-hook S swirl, dark outline | 36 → 9, 8 |
| U+E601 | 달빛 축복 받음 badge: dark-gold disc, gold rim #E0DD9C / #C9A23E, gold-white 4-point star + crescent moon | 36 → 9, 8 |
| U+E602 / U+E603 | the same two, big (title pops) | 96 → 24, 18 |
| U+E604 | moon-dew drop icon (hint lines) | 28x36 → 9, 8 |
| U+E610-E613 | flat full-screen flashes: white (0.92), lime #B6FC9D (0.62), gold #F4EDC9 (0.55), maroon #8C525C (0.45) | 16x9 → 144, 69 |
| U+E6F0 | space −1 | |

The generator refuses to write the font when any of these codepoints is used by another font of the resource pack
(checked against every `assets/*/font/*.json`; today: `rlk:hud` E100-E101, `rlk:minimap` E300-E3F2, `rlk:bossbar`
E400-E438, `rlk:mboss_gd` E500-E5F1).

| function | does |
|---|---|
| `hud/coc_on`, `hud/coc_off` | flag + rebuild: the 달빛 고치 badge on the boss-bar lines |
| `hud/buff_on`, `hud/buff_off` | flag + rebuild: the 달빛 축복 받음 badge |
| `hud/clear` | both off (fight end, death, abort, uninstall) |
| `hud/put_extra` | append `rlk:bfkit hud.ex[]` (two spaces + badge per active flag) to `rlk:mboss extra` — call at the end of the core's line-1 build; equivalent component: `{nbt:"hud.ex[]",storage:"rlk:bfkit",interpret:true,separator:""}` |
| `hud/put_sub` | append `rlk:bfkit hud.sub[]` (badge + "달빛 고치 — 회복 <P>/<T>%" + dew icon, and/or badge + "달빛 축복 받음 (치명타 +15% · 치명타 피해 +50%)") to `rlk:mboss sub` — call after the core's own sub-line text. `<P>` / `<T>` are score components of the fake players `#bkCureP` / `#bkCureT` in `mb` (the cure meter and its target in % of max HP): the module sets them (core `coc/meter`), the boss bar re-reads them every tick |
| `hud/ab_coc`, `hud/ab_buff` | one-shot actionbar notice (badge + numbers: "체력 15% 회복하면 해제 · 피해 −50% · …" / "치명타 +15% · 치명타 피해 +50%") for every player, holding the HUD 40 t (`hudHold`) |
| `hud/ab_cure` | one-shot actionbar notice after a heal that filled the cure meter but not to its target: badge + "달빛 고치 — 회복 <P>/<T>%" (the same score components), 40 t |
| `hud/pop_coc`, `hud/pop_buff` | the big badge on the title line for 1.2 s (`vBig` rests the F5 crosshair title) |
| `hud/flash_white`, `flash_lime`, `flash_gold`, `flash_maroon` | full-screen flat flash on the title line (any view mode) |
| `hud/flash_end` | drop a title overlay at once |

The core's current `hud/extra` / `hud/sub` use text characters (◖꩜◗, ✦) for the badges; replacing those lines with the two
`put_*` calls (and `coc_on/off`, `buff_on/off` where `#bfCoc` / `#bfBuff` change) gives the glyphs.

## 6. Sound recipes (`fx/snd/<name>`, no args)

Each recipe plays its layers at the executing position for `@a[tag=player]`, source `hostile`, with the per-layer
minimum volume of `mboss_lib.min_volume` (the Guardian's `L.sound`: layers ≤ 0.25 fade out past their range, louder ones
keep a third of their volume, at most 0.4). Vanilla events only; no creature voices (no roars, cries or mob ambient
sounds; wing flaps, wind, fire, crystal and beacon sounds only). Python: `snd('kick_impact')`. Since the fx polish the
main recipes are one-tick layer stacks shaped as a transient, a low pitched-down body, a tail and a quiet sparkle (kicks,
wing flaps, the Pyro switch, the fire crescents, the flame fan, the orb charge / burst, the release charge, wrap and
detonation); `cure_chime` is an A-major chord (pitch 1.19 / 1.5 / 1.78).

| recipe | use | layers (event volume pitch; minVolume = mboss_lib.min_volume) |
|---|---|---|
| `snd/cocoon_glow` | Cocoon core brightens (entrance t57+, transformation start): rising glassy shimmer. | block.beacon.power_select 0.8 1.4; block.amethyst_block.resonate 0.7 1.2; block.respawn_anchor.charge 0.35 1.6; block.conduit.activate 0.3 1.8 |
| `snd/cocoon_burst` | Cocoon bursts into crystal shards (entrance about t79): bright shatter + wind. | block.amethyst_cluster.break 1 1; block.glass.break 0.8 1.3; entity.breeze.wind_burst 0.9 1.2; block.amethyst_block.chime 0.8 1.5; block.amethyst_block.chime 0.6 1.9; entity.firework_rocket.twinkle 0.4 1.4 |
| `snd/cocoon_tail` | Glittering tail of the burst (2-8 t after cocoon_burst). | block.amethyst_block.chime 0.6 1.7; block.amethyst_block.chime 0.45 2; entity.firework_rocket.twinkle_far 0.35 1.6 |
| `snd/land` | Soft landing (entrance t90, revert landing, backflip landings). | block.moss.break 0.8 0.9; entity.iron_golem.step 0.4 1.4; entity.breeze.land 0.5 0.9 |
| `snd/kick_whoosh` | Burst-run / kick wind-up whoosh with a leafy crack (H1 hit 1 lead-in): bright air attack, a rising swish and a glint tick on top. | entity.breeze.wind_burst 0.55 1.5; entity.player.attack.sweep 0.45 1.6; item.trident.riptide_1 0.3 1.9; block.azalea_leaves.break 0.55 1.25; block.amethyst_block.chime 0.22 1.9 |
| `snd/kick_impact` | Kick crescent lands (H1 hits, H3 kick): a thump transient, a big low airy swoosh (pitched down so it rings longer), a leafy crackle and a short airy tail. | entity.player.attack.strong 0.55 0.9; entity.player.attack.sweep 1 0.75; entity.breeze.wind_burst 0.9 0.95; block.big_dripleaf.tilt_down 0.6 0.9; block.azalea.break 0.75 0.85; block.azalea_leaves.break 0.65 1.15; item.trident.riptide_1 0.3 1.7 |
| `snd/crescent_fly` | A crescent wave travels (H1 ground wave, B1 trailing crescent). | entity.phantom.swoop 0.6 1.4; item.trident.riptide_1 0.35 1.6; block.azalea_leaves.hit 0.5 1.2 |
| `snd/shard_tell` | Arm shard glows lime (H2 tell, the chain glow): shimmer chime. | block.amethyst_block.chime 0.8 1.6; block.beacon.ambient 0.5 1.8; block.amethyst_cluster.hit 0.4 1.9 |
| `snd/sweep` | 360-degree low sweep kick (H2): thump then a whirling swish and leaf debris. | entity.player.attack.sweep 1 1.1; block.moss.break 0.7 0.9; entity.breeze.whirl 0.45 1.4; entity.breeze.charge 0.4 1.5; entity.iron_golem.attack 0.3 1.6; block.cherry_leaves.break 0.4 1.2 |
| `snd/spiral_jump` | Spiral jump (H2): rising whirl and a low rumble. | entity.breeze.charge 0.8 1.1; entity.breeze.jump 0.6 1; item.elytra.flying 0.15 1.6 |
| `snd/disc_kick` | Orb kicked down as the Dendro disc (H2 star flash + kick): bright sparkle and a crack. | block.conduit.activate 0.4 1.8; entity.firework_rocket.twinkle 0.6 1.4; entity.player.attack.strong 0.7 1.2; entity.breeze.shoot 0.6 1.3 |
| `snd/disc_impact` | Dendro disc hits the floor (H2 impact): boom with a leafy crackle. | entity.generic.explode 0.4 1.4; entity.breeze.wind_burst 0.8 0.8; block.azalea_leaves.break 0.8 1; block.moss.break 0.8 0.9 |
| `snd/dash_charge` | Mote charge before the dash (H3): rustling glittery shimmer. | block.azalea_leaves.break 0.35 1.6; block.amethyst_block.chime 0.5 1.8; entity.breeze.charge 0.6 1.4 |
| `snd/dash` | Dash lunge (H3, burst-runs): short airy whoosh. | entity.breeze.jump 0.8 1.3; item.trident.riptide_1 0.5 1.5; block.moss.place 0.5 1 |
| `snd/dash_kick` | Dash kick impact + ring (H3): deep thump, a bright air pop, a leafy burst and a crackling low tail. | entity.player.attack.strong 0.6 0.85; entity.breeze.wind_burst 1 1; item.mace.smash_ground 0.6 1.3; entity.wind_charge.wind_burst 0.5 1.2; block.azalea_leaves.break 0.8 1.1; block.cherry_leaves.break 0.6 1.3; block.cherry_sapling.place 0.6 0.8; entity.player.attack.sweep 0.8 0.7 |
| `snd/vacuum_glint` | Vacuum blade tell glint (H4): sharp crystalline ping. | block.amethyst_cluster.hit 0.8 1.8; block.note_block.chime 0.35 2; entity.firework_rocket.twinkle 0.3 1.9 |
| `snd/vacuum_blade` | Foot stomp + blade rise (H4): whoosh and leafy roar. | entity.breeze.wind_burst 1 1; item.trident.riptide_2 0.8 1.2; block.big_dripleaf.tilt_down 0.7 1; entity.phantom.swoop 0.5 1.4 |
| `snd/vacuum_pass` | The blade rushes past (H4 travel): hiss and a low thump. | entity.phantom.swoop 0.7 1.4; item.trident.riptide_1 0.4 1.3; block.azalea_leaves.break 0.5 1.2 |
| `snd/transform_glow` | Transformation: the cocoon sheath glows and the folded wings open. | block.beacon.power_select 0.9 1.6; block.respawn_anchor.charge 0.5 1.6; block.amethyst_block.resonate 0.6 1.4 |
| `snd/transform_swell` | Light sphere + ripple rings + wings unfurl: broad airy swell. | entity.ender_dragon.flap 0.8 1.5; entity.breeze.wind_burst 0.8 0.8; block.amethyst_block.resonate 0.9 1; block.beacon.activate 0.6 1.8 |
| `snd/debuff` | 달빛 고치 lands on the player (with the light sphere): curse-like chime burst. | item.totem.use 0.45 1.4; block.beacon.deactivate 0.6 1.5; block.respawn_anchor.deplete 0.6 1.6; entity.illusioner.prepare_mirror 0.5 1.2 |
| `snd/flap_big` | Big wing flap (B3 tell, B5 flight, the glide settle): a deep whump, the membrane body, a low air push and a soft rustle. | entity.ender_dragon.flap 0.75 1.35; entity.phantom.flap 0.55 0.75; entity.breeze.wind_burst 0.3 0.7; item.armor.equip_elytra 0.35 1.3 |
| `snd/flap_small` | Small hover flap (every 13-20 t in butterfly form; quiet): a soft flap and a feathery flutter. | entity.phantom.flap 0.3 1.55; entity.parrot.fly 0.22 1.2 |
| `snd/wing_dive` | Bank + dive before the wing strike (B1), the release swoop (B5): a high flap, the swoop and a rushing air tail. | entity.ender_dragon.flap 0.5 1.75; entity.phantom.swoop 0.8 1.25; item.trident.riptide_2 0.35 1.4; entity.phantom.flap 0.3 1.1 |
| `snd/wing_strike` | Wing edge hits and sweeps on (B1): solid hit then a long airy swish with leaf crackle. | entity.player.attack.strong 0.5 0.95; entity.player.attack.sweep 1 0.8; entity.breeze.wind_burst 0.9 1; block.azalea_leaves.break 0.7 1; item.trident.riptide_1 0.5 1.6; entity.phantom.swoop 0.35 1.5 |
| `snd/pyro_switch` | Wings turn Pyro (1 t swap, 5-12 t before B2 / B3): a soft fire whump, a glassy shimmer as the wing glass recolours, a bright hiss and a crackling tail. | item.firecharge.use 0.55 1.35; block.fire.ambient 0.7 1.3; block.respawn_anchor.set_spawn 0.3 1.6; block.amethyst_block.resonate 0.3 1.8; entity.blaze.shoot 0.22 1.7; block.campfire.crackle 0.5 1.2 |
| `snd/dendro_switch` | Wings turn back to Dendro (before B1 / B4 / B5). | block.amethyst_block.resonate 0.6 1.4; block.azalea_leaves.place 0.6 1 |
| `snd/fire_cres_launch` | Wing swing throws the fire crescents (B2, each swing): a low whoosh attack, the roaring flame burst, a wing whump, air and a crackling tail. | entity.player.attack.sweep 0.9 0.65; entity.blaze.shoot 0.85 0.85; item.firecharge.use 0.75 0.75; entity.ender_dragon.flap 0.5 1.4; entity.breeze.wind_burst 0.45 1.3; block.fire.ambient 0.7 1.4; block.campfire.crackle 0.6 1 |
| `snd/fire_cres_fly` | Crescents turn and dive (B2): crackling hiss with an airy streak. | block.fire.ambient 0.7 1.5; block.campfire.crackle 0.45 1.4; entity.blaze.burn 0.25 1.4; item.trident.riptide_1 0.3 1.6 |
| `snd/fire_cres_land` | A fire crescent lands (B2, per landing): a sharp pop and crack, a fire puff and a short hiss. | block.lava.pop 0.55 1.1; entity.generic.burn 0.6 1.2; entity.firework_rocket.blast 0.5 0.8; item.firecharge.use 0.35 1.3; block.fire.extinguish 0.3 1.6 |
| `snd/flame_slam` | Wing slam (B3 slam): low thump. | entity.ender_dragon.flap 0.9 0.9; entity.generic.explode 0.4 1.6; item.mace.smash_ground 0.5 0.9 |
| `snd/flame_fan` | 180-degree flame eruption (B3): crackling roar, a low boom under it and a long crackling rumble. | entity.blaze.shoot 1 0.8; item.firecharge.use 0.9 0.6; block.fire.ambient 1 1; entity.generic.explode 0.35 0.7; entity.blaze.burn 0.4 0.9; block.campfire.crackle 0.8 0.8; block.lava.pop 0.45 0.9 |
| `snd/flame_trail` | Flame line under the low glide (B3 trail, every 4-6 t; quiet). | block.fire.ambient 0.45 1.2; entity.blaze.burn 0.15 1.5 |
| `snd/orb_charge` | Wing-wrap core charge (B4 before each orb): a thin rising sparkle over a quiet hum. | block.beacon.power_select 0.5 1.85; block.conduit.activate 0.4 1.6; block.amethyst_block.resonate 0.5 1.8; block.enchantment_table.use 0.45 1.5; block.respawn_anchor.charge 0.25 1.9; block.amethyst_block.chime 0.22 2 |
| `snd/orb_launch` | Orb released (B4 t19 / t46): soft launch whir. | entity.breeze.shoot 0.8 1.2; block.amethyst_block.chime 0.6 1.4; item.trident.riptide_1 0.4 1.8; block.beacon.ambient 0.5 2 |
| `snd/orb_fly` | Orb flight loop (every 10-12 t while it homes; quiet). | block.beacon.ambient 0.35 2; block.amethyst_block.step 0.2 1.8 |
| `snd/orb_burst` | Orb bursts into radial ground blades (B4): an airy boom, a low thump, a leafy crackle and a glassy sparkle tail. | entity.breeze.wind_burst 1 0.95; entity.wind_charge.wind_burst 0.6 0.8; entity.generic.explode 0.4 1.5; block.azalea_leaves.break 1 0.9; block.cherry_leaves.break 0.5 1.2; block.big_dripleaf.tilt_down 0.6 0.9; block.moss.break 0.6 0.8; block.amethyst_block.chime 0.35 1.6 |
| `snd/cocoon_ball` | Wings curl into the ball (B4 t30-42): swirling rustle. | item.elytra.flying 0.25 1.4; block.moss.place 0.6 1; entity.breeze.charge 0.4 1.5 |
| `snd/release_swoop` | 달빛 해제 fold + swoop (B5 start): low swoosh. | entity.phantom.swoop 1 1; entity.ender_dragon.flap 0.8 1.2 |
| `snd/release_whirl` | 달빛 해제 whirl / cup (B5): airy swishes. | item.trident.riptide_1 0.5 1.3; entity.player.attack.sweep 0.4 1.6; entity.player.attack.sweep 0.35 1.9 |
| `snd/release_charge` | 달빛 해제 charge (flare, X glint, ring cage): rising hum + sparkle; call 2-3 times rising. | block.respawn_anchor.charge 0.9 1.4; block.beacon.activate 0.8 1.6; entity.warden.sonic_charge 0.35 1.8; block.beacon.power_select 0.6 1.4; block.enchantment_table.use 0.5 1.2 |
| `snd/release_wrap` | 달빛 해제 wings wrap into the pod (E-9): pressure builds. | block.respawn_anchor.charge 0.8 1.8; entity.breeze.inhale 0.7 1.2; block.conduit.activate 0.5 1.4; entity.illusioner.prepare_mirror 0.4 1.6 |
| `snd/release_boom` | 달빛 해제 detonation (E): a broadband boom pitched down for a long body, an airy blast, the sonic crack, a falling beacon tone, crystal and leaf crackle and a low glassy tail. | entity.generic.explode 1.6 0.65; entity.dragon_fireball.explode 1 0.8; entity.breeze.wind_burst 1.2 0.55; entity.warden.sonic_boom 0.6 1.4; entity.firework_rocket.large_blast 0.7 0.7; block.beacon.deactivate 0.8 1.3; block.amethyst_cluster.break 0.9 0.8; block.azalea_leaves.break 1 0.75; block.amethyst_block.chime 0.5 0.6 |
| `snd/wing_shatter` | Wings shrink, go flat lime and shatter (B5 E+38 / death). | block.amethyst_cluster.break 0.7 1.5; block.glass.break 0.4 1.6; entity.illusioner.mirror_move 0.6 1.4; block.beacon.deactivate 0.5 1.8 |
| `snd/groggy` | Groggy starts (after the revert landing): spent, deflating cue. | block.respawn_anchor.deplete 0.6 1.2; block.beacon.deactivate 0.4 0.9 |
| `snd/chain_reform` | Crescent chain re-forms at her side (after the groggy turn): plates clink into place. | block.chain.place 0.8 0.8; block.amethyst_block.place 0.6 1.2; block.amethyst_block.chime 0.5 1.5 |
| `snd/dew_spawn` | A 달빛 이슬 heal orb appears. | block.amethyst_block.chime 0.6 1.8; block.bubble_column.upwards_inside 0.3 1.6; entity.experience_orb.pickup 0.25 0.7 |
| `snd/cure_chime` | 달빛 고치 removed by a heal: bright rising chime burst (beam, burst, emblem): an A-major chord of note-block bell and chimes (pitch 1.19 / 1.5 / 1.78) and amethyst chimes over the beacon swell, with a sparkle and a shimmering tail. | block.beacon.activate 0.75 1.6; entity.player.levelup 0.35 1.5; block.amethyst_block.chime 0.9 1.19; block.amethyst_block.chime 0.8 1.5; block.note_block.bell 0.45 1.19; block.note_block.chime 0.5 1.5; block.note_block.chime 0.4 1.78; entity.experience_orb.pickup 0.3 1.2; block.amethyst_block.resonate 0.5 1.5 |
| `snd/death` | Death: stagger, the wings shatter, she kneels and dissolves (no voices). | block.amethyst_cluster.break 1 0.9; block.beacon.deactivate 0.9 1; entity.breeze.wind_burst 0.8 0.7; block.amethyst_block.resonate 0.8 0.6; block.respawn_anchor.deplete 0.6 1.2 |
| `snd/death_motes` | Death tail: the last motes rise. | block.amethyst_block.chime 0.6 2; entity.firework_rocket.twinkle 0.4 1.8; block.beacon.ambient 0.4 1.6 |

## 7. Presets (`fx/p/<name>`)

Ready-made bundles of cards + particles for every event of plan.md. Non-macro unless args are listed. "Cards" = fx cards
per call (all expire within 30 t; checked by the mcsim suite). The last column lists what a call draws: the card kinds
(§3) and the particle types (`dust_color_transition` = the lime-to-teal / gold-to-mauve fading dust the fx polish added,
`end_rod` = sparkle). The fx polish kept every card count (peaks unchanged: B2 44 / 41, B5 31, entrance 20, B3 17, H1 12,
cure 11) and changed the looks: taller kick crescents and thinner blades, a fuller B3 flame wall, tilted B2 flame sheets,
a tall landing flame streak, a red-pink glide trail, whiter orb-kick wind arcs, bigger wing-shatter shards, a salmon
debuff glow.

| preset | args | cards | what / where (executor context) | layers: cards (kind ×n, tint) and particles |
|---|---|---|---|---|
| `p/cocoon_disc` | `life` | 2 | Entrance: the glowing lime floor disc under the cocoon (at the floor point). {life} | disc_lime, glow; dust |
| `p/cocoon_glow` | - | 4 | Entrance / transformation: the cocoon core brightens (glow ramp, 18 t). At the core. | glow, star4, streak ×2; end_rod, dust |
| `p/whiteout` | - | 2 | Entrance whiteout / big flash: a white-yellow glow ball (8 t). At the core. | glow, sphere |
| `p/cocoon_burst` | - | 17 | Entrance t79: crystal shard star, two lime wing crescents, cyan wind ring. At the core. | burst, glow, cres_lime ×2, ripple, shard ×12; end_rod, wax_off, dust |
| `p/motes` | - | 6 | Moonlight motes rising around the point (idle sparkle, charge, death). 6 cards. | mote ×6 |
| `p/land` | - | 1 | Landing: a mint ripple on the floor, drifting leaves, moss dust. At the floor point. | ripple; cherry_leaves, dust, composter |
| `p/glint` | - | 1 | A small white-lime glint (tells, foot sparkles). Billboard. | glint |
| `p/kick_rise` | - | 3 | H1 hit 1: the tall rising flip-kick crescent (sagittal, sweeping up and back) + ground splash. At her feet, rotated as her (yaw). | cres_lime, burst, glow; dust, dust_color_transition, end_rod, cherry_leaves |
| `p/kick_axe` | - | 3 | H1 hit 2: the huge diagonal axe-kick crescent from above-behind down to the floor ahead (r about 5). At her feet, rotated as the kick. | cres_lime ×2, burst; explosion, dust_color_transition, end_rod |
| `p/ground_wave` | - | 9 | H1 hit 2 ground wave: lime blades erupt one after another along 6 blocks ahead, plus a streak on the floor. At the floor point, rotated as the line. | streak, blade ×8; dust, composter |
| `p/shard_tell` | - | 2 | H2 tell: one arm shard glows into a lime crescent blade (13 t). At the shard. | star4, glow; dust |
| `p/sweep` | - | 2 | H2 360-degree low sweep (r 3, active 6 t): two knee-high lime crescents turning around her. At her feet. | cres_lime ×2; sweep_attack, dust |
| `p/spiral_jump` | - | 2 | H2 spiral jump: two lime spiral ribbons wind up around her. At her feet. | cres_lime ×2; dust |
| `p/orb_star` | - | 2 | H2 star flash at the orb (and any white 4-point flash). Billboard. | star4, glow; end_rod |
| `p/orb_kick` | - | 3 | H2 orb burst as it is kicked down: lime starburst and two white wind crescents circling it. | burst, cres_cyan ×2; end_rod |
| `p/disc_fall` | `h` | 1 | H2 the Dendro disc drops {h} blocks onto the floor point in 3 t (call at the floor point; the disc starts h above). | disc_lime |
| `p/disc_impact` | - | 3 | H2 disc impact (r 2.5): lime disc splash, burst, ripple, dust puffs and leaves. At the floor point. | disc_lime, burst, ripple; dust ×2, cherry_leaves, composter |
| `p/dash_charge` | - | 9 | H3 mote charge (10 t): motes converge on her and a faint floor glow. At her feet. | glow, glint ×8 |
| `p/dash_streak` | - | 2 | H3 dash: a 5.5-block speed streak along the dash path. At her start point, rotated along the dash. | streak ×2; dust |
| `p/kick_burst` | - | 13 | H3 kick + Dendro ring r 3.5: white-lime burst at the foot, flung blades, a floor ripple and the all-around crescent ring. At her feet. | burst, glow, ripple, cres_lime ×2, blade ×8; explosion, dust |
| `p/vac_crouch` | - | 1 | H4 crouch: the kicking leg glows lime (9 t). At the foot. | glow; dust |
| `p/vac_glint` | - | 3 | H4 tell: a green spike flares behind her, a horizontal cyan-white glint line and a 4-point flare at the foot. At the foot, rotated as her. | blade, streak, star4 |
| `p/vac_stomp` | - | 2 | H4 stomp: yellow-green ground flare at the foot as the blade rises. At the floor point. | burst, glow; dust |
| `p/vac_trail` | - | 1 | H4 travelling blade, every 2 t at the blade prop: small blades and leaves left behind, a dark-green scar. At the prop (floor height). | blade; dust ×2, cherry_leaves |
| `p/tf_sheath` | - | 1 | Transformation: the green vertical glow sheath wraps her lower body. At her chest. | glow; dust |
| `p/tf_sphere` | - | 3 | Transformation: core flash, then the light sphere r 2.5 (6 t). At her chest. | sphere, glow, star4 |
| `p/tf_ripples` | - | 11 | Transformation: concentric ripple rings r 4-5 (a floor ring and two vertical arcs) and radial speed lines. At her chest; the floor ring is drawn 1.6 below. | ripple ×3, streak ×8 |
| `p/wing_band` | - | 1 | B1 hit: the bright yellow-green ground slash band along the wing path (r 4 arc on the floor). At the floor under her, rotated as the strike. | cres_lime; dust |
| `p/wing_flare` | - | 1 | B1 trailing vertical crescent flare (2-3 b) at the end of the arc. At the wing tip. | cres_lime; cherry_leaves |
| `p/pyro_switch` | - | 2 | Wings turn Pyro: a magenta-pink rim glow pulse around her (1 t swap). At her chest. | glow ×2; small_flame |
| `p/dendro_switch` | - | 1 | Wings turn back to Dendro: a lime glow pulse. At her chest. | glow; dust |
| `p/fire_swing` | - | 3 | B2 swing: a giant flame sheet in the swing plane (r 4) with white wind streaks. At her chest, rotated as the swing (roll the plane with an execute rotated / the diagonal variant). | cres_fire ×2, streak; flame, small_flame, dust_color_transition |
| `p/fire_swing_d` | - | 2 | B2 swing, diagonal plane (upper-left to lower-right). At her chest, rotated as her. | cres_fire ×2; flame, dust_color_transition |
| `p/fire_spawn` | - | 1 | B2: a fire crescent appears in the air (small puff + embers). At the crescent. | flame_puff; small_flame |
| `p/fire_trail` | - | 1 | B2 / B3: a short flame puff left behind a moving fire crescent (call every 1-2 t at the prop). | flame_puff; small_flame |
| `p/fire_land` | - | 5 | B2 crescent landing: fire splash r 1.2 with a 2.5-block vertical flame streak. At the floor point. | flame_tongue ×3, flame_puff, glow; lava, flame (2 radial tongues since the fix round, was 4: FX-2) |
| `p/flame_slam` | - | 2 | B3 slam: two vertical flame crescents rise at the wing tips. At her chest, rotated as her. | cres_fire ×2; flame |
| `p/flame_fan` | - | 15 | B3 eruption: the 180-degree front flame fan r 4.5, 2.5 tall (t28-32) with a scorched floor sheet. At the floor under her, rotated as her. | fan_fire, flame_tongue ×14; flame, lava, large_smoke |
| `p/flame_trail` | - | 2 | B3 low glide: a flame line on the floor (call every 2 t at the wing-tip floor point). | flame_puff, flame_tongue; small_flame |
| `p/orb_charge` | - | 5 | B4 wing-wrap charge (14 t): a lime core grows at her chest with converging streaks. | glow, star4, streak ×3 |
| `p/orb_launch` | - | 2 | B4 orb release: a lime ring flash and sparkle where the orb leaves her. At the orb. | ripple, glint |
| `p/orb_burst` | - | 13 | B4 orb burst r 2.5-3: starburst, radial V-shaped ground blades, a floor ripple, leaves. At the floor under the orb. | burst, glow, ripple, blade ×10; cherry_leaves, composter, dust |
| `p/cocoon_ball` | - | 1 | B4 wing ball (12 t): a lime glow inside the ball. At its centre. | glow; dust |
| `p/rel_fold` | - | 4 | B5 fold: small lime butterfly glyphs float up around her (20 t). At her chest. | bfly ×4 |
| `p/rel_flare` | - | 5 | B5 whirl: the pulsing lime 4-point star flare at her side with converging lines (call 2-3 times over the 20 t whirl). At the flare point. | star4, glow, streak ×3 |
| `p/rel_slashes` | - | 4 | B5 whirl: thin lime slash streaks whip around her (4 cards). At her chest. | streak ×4 |
| `p/rel_ground_flash` | - | 2 | B5 E-18: a lime mist cone bursts from the floor under her. At the floor point. | glow, burst; cloud |
| `p/rel_xglint` | - | 3 | B5 E-16: two long cyan-white lines cross through her chest as an X (8 blocks each). At her chest (camera-facing). | streak ×2, glint |
| `p/rel_cage` | - | 3 | B5 E-15..-10: the gyroscope ring cage r 4 (three spinning lime rings). At her chest. | gyro ×3 |
| `p/rel_pod` | - | 4 | B5 E-9..-1: the white-lime core glow grows inside the wrapped pod with inward streaks. At her chest. | glow, streak ×3 |
| `p/rel_dome` | `r` | 19 | B5 detonation E: white flash, then the lime dome grows to radius {r} blocks in 5 t (16 shell segments + cap) and lingers, with a floor shock ring. At the floor under her. | glow ×2, dome_lo ×8, dome_hi ×8, ripple; explosion, end_rod, cherry_leaves |
| `p/rel_tendrils` | - | 8 | B5 E+7: long lime flame-like tendrils stream out radially as she re-emerges. At her chest. | streak ×8 |
| `p/embers` | - | 6 | After the blast: amber ember petals and lime motes drift down (E+10..+34). Around her chest. | leaf ×6 |
| `p/wing_shatter` | - | 11 | B5 E+38 / death: the shrunken lime wings break into shards (12 cards). At her back. | glow, shard ×10; cherry_leaves, dust |
| `p/chain_reform` | - | 4 | After the groggy turn: lime streaks converge on her side as the crescent chain re-forms (18 t). At the chain point. | glow, streak ×3 |
| `p/coc_apply` | - | 3 | 달빛 고치 applied: a maroon swirl ring closes on the player and a salmon glow. At the player's feet. | ripple, glow, bfly; dust |
| `p/cure` | - | 11 | 달빛 고치 removed (about 20 t): gold beam down (6 t), gold burst + ring (5 t), gold emblem with sparkles (9 t). At the player's feet. | cure_beam, glint ×7, cure_burst, ripple, cure_emblem; end_rod, wax_on |
| `p/dew_spawn` | - | 2 | A 달빛 이슬 orb appears: a cyan-lime floor ripple, a glow and motes. At the orb's floor point. | ripple, glow; end_rod |
| `p/dew_pulse` | - | 3 | Idle pulse of a 달빛 이슬 orb (call every 20 t at the orb): a soft ring on the floor and two rising motes, so it reads on the marble. | ripple, mote ×2 |
| `p/death_motes` | - | 10 | Death: rising moonlight motes and crystal shards (call every 10-20 t of the 100 t death). Around her chest. | mote ×7, shard ×3 |

Python: `fx('kick_rise')`, `fx('rel_dome', r=10.0)`, `fx('disc_fall', h=3.0)`, `fx('cocoon_disc', life=80)`.

## 8. Python API (`tools/build_mboss_bf_fx.py`)

```python
import build_mboss_bf_fx as K          # tools/ is on sys.path in the module generators
K.card(kind, pos='~ ~ ~', rot='~ ~', bb='fixed', roll=0, spin=0, s0=0.0, s1=1.0, move=(0, 0, 0), life=8, fade=0,
       col=K.WHITE, dly=0, dur=0, hit=-1, col2=-1)   # -> 'function rlk:mboss/butterfly/fx/card {...}' (cardx when needed)
K.tele_disc(r, tell, el=7, hold=3); K.tele_ring(r0, r, tell, el=7, hold=3)
K.tele_sector(r, half_angle, tell, el=7, hold=3); K.tele_line(length, width, tell, el=7, hold=3, back=0.0)
K.snd(name); K.fx(name, **args); K.look(kind, col=K.WHITE); K.prop(name); K.hud(name)
K.KINDS, K.PRESETS, K.SOUNDS, K.PROPS, K.GLYPHS, K.glyph('coc')        # tables; glyph() = the literal character
K.WHITE, K.LIME, K.LIME_PALE, K.LIME_DEEP, K.MINT, K.CYAN, K.OPAL, K.GOLD, K.GOLD_PALE, K.AMBER, K.FIRE, K.MAGENTA,
K.ORANGE, K.MAROON, K.SALMON, K.TELE_COL                                  # RGB ints
K.CAP, K.TCAP                                                             # 64 / 40
```
Card macro values may be placeholders inside a macro preset (`life='$(life)'`, `s1='$(r)'`, `move=(0, '-$(h)', 0)`).

## 9. Usage per pattern (plan.md)

The clip ticks in this section are plan.md's first timeline (written before the rig). The patterns read the real rig's
events from `tools/mboss_butterfly_rig_manifest.json` (bf_contract.md §9; e.g. `kick_jump` orb 45 / kick 52 / impact 55 /
land 59, `wing_strike` dive 8, `wing_barrage` swings 5 / 31 / 69 / 94, `flap_dive` dive 20 / glide 33, `coco` ball 30 /
ball_open 42, `release` snap 52, `death` shatter 10 / kneel 30 / dissolve 50); the calls per event are unchanged.

Notation: `t` = the pattern clock (= the clip tick of plan.md's rig table); **feet** = `execute at @s rotated as @s
rotated ~ 0 run …` from the body (human form: on the floor); **chest** = feet + `positioned ~ ~1.6 ~` (human) or
`~ ~2.8 ~` (hovering butterfly, toes at +1.2); **floor** = a floor point (y = the floor top) `rotated` as the aim;
**P** = a position locked from the player; **prop** = `execute as <prop> at @s rotated as @s run …`. `K.` = the Python
helpers of §8 (they return the function lines). Every hit line keeps its framework hazard (`hz/*` with `#hzQuiet 1`) or
prop; only the fx are shown. Telegraph `tell` = the hit tick − the call tick (≥ 10 t, plan.md).

### Entrance (clip `entrance`, 106 t; nameplate t57, burst t79, land t90)
| t | where | calls |
|---|---|---|
| 0 | floor under the cocoon | `K.fx('cocoon_disc', life=80)` |
| 0, 20, 40 | cocoon core | `K.fx('motes')` |
| 61 | cocoon core | `K.fx('cocoon_glow')`, `K.snd('cocoon_glow')` |
| 71 | cocoon core | `K.fx('whiteout')` (+ `K.hud('flash_white')` for the whiteout on screen) |
| 79 | cocoon core | `K.fx('cocoon_burst')`, `K.snd('cocoon_burst')`; t81 `K.snd('cocoon_tail')` |
| 90 | feet | `K.fx('land')`, `K.snd('land')` |

### H1 달빛 발차기 (`kick_combo`, 51 t; hit1 8, hit2 40)
| t | where | calls |
|---|---|---|
| close-in run (≥ 2 t before t0) | feet | `K.tele_sector(4.0, 45, tell=10 + run ticks)` — hit 1's front arc, called as the run starts so the tell is ≥ 10 t; `K.snd('kick_whoosh')`, `K.snd('dash')` |
| 6 | foot | `K.fx('glint')` |
| 8 | feet | `K.fx('kick_rise')`, `K.snd('kick_impact')` |
| 15 | feet | `K.fx('land')` (backflip landing) |
| 28 | feet (kick yaw) | `K.tele_sector(5.0, 90, 12)` + `K.tele_line(6, 2, 12)` (hit 2 arc r 5 + the 6 x 2 wave) |
| 38 | kicking foot | `K.fx('glint')` |
| 40 | feet (kick yaw) | `K.fx('kick_axe')`, `K.fx('ground_wave')`, `K.snd('kick_impact')`, `K.snd('crescent_fly')` |
| 46 | feet | `K.fx('land')`, `K.snd('land')` |

### H2 달빛 점프 (`kick_jump`, 65 t; tell 0-13, sweep 13-19, jump 33, disc 40, land 55)
| t | where | calls |
|---|---|---|
| 0 | the glowing arm shard | `K.fx('shard_tell')`, `K.snd('shard_tell')` |
| 0 | feet | `K.tele_disc(3.0, 13)` (the 360° low sweep r 3) |
| 13 | feet | `K.fx('sweep')`, `K.snd('sweep')` |
| 33 | feet | `K.fx('spiral_jump')`, `K.snd('spiral_jump')` |
| 40 | floor at P (locked) | `K.tele_disc(2.5, 10)` (impact t50) |
| 46 | the orb (her raised foot) | `K.fx('orb_star')`, `K.fx('orb_kick')`, `K.snd('disc_kick')` |
| 47 | floor at P | `K.fx('disc_fall', h=3.0)` (falls in 3 t) |
| 50 | floor at P | `K.fx('disc_impact')`, `K.snd('disc_impact')` |
| 55 | feet | `K.fx('land')`, `K.snd('land')` |

### H3 달빛 돌진 (`dash_kick`, 50 t; dash 10-12, kick 15)
| t | where | calls |
|---|---|---|
| 0 | feet | `K.fx('dash_charge')`, `K.snd('dash_charge')` |
| 0 | floor at the dash end point (locked) | `K.tele_disc(3.5, 15)` (kick + Dendro ring r 3.5) |
| 10 | feet (dash yaw) | `K.fx('dash_streak')`, `K.snd('dash')` |
| 15 | feet | `K.fx('kick_burst')`, `K.snd('dash_kick')` |

### H4 광폭한 진공 (`vacuum`, 41 t; blade 17, backflip 17-38)
| t | where | calls |
|---|---|---|
| 0 | kicking foot | `K.fx('vac_crouch')` |
| 7 | floor at her foot, rotated along the locked line | `K.tele_line(<to the arena edge>, 3.0, 10)` (the blade leaves at t17; the lane stays the blade's path) |
| 9 | kicking foot | `K.fx('vac_glint')`, `K.snd('vacuum_glint')` |
| 15 | floor at the foot | `K.fx('vac_stomp')` |
| 17 | the pj prop (0.9 above the floor, facing the line) | `K.prop('vblade')` on the prop, `K.snd('vacuum_blade')` |
| 17+ every 2 t | prop | `K.fx('vac_trail')`; once when within 4 b of the player: `K.snd('vacuum_pass')` |
| 38 | feet | `K.fx('land')`, `K.snd('land')` |

### Transformation (`transform`, 30 t; wings open 4-12, sphere 6) + 달빛 고치
| t | where | calls |
|---|---|---|
| 0 | chest | `K.fx('tf_sheath')`, `K.snd('transform_glow')` |
| 6 | chest | `K.fx('tf_sphere')`, `K.snd('transform_swell')` |
| 6 | the player's feet (as the debuff lands) | `K.fx('coc_apply')`, `K.snd('debuff')`, `K.hud('coc_on')`, `K.hud('ab_coc')`, `K.hud('pop_coc')`, optional `K.hud('flash_maroon')` |
| 6 | each 달빛 이슬 spot (floor) | `K.fx('dew_spawn')`, `K.snd('dew_spawn')`; as the orb display: `K.prop('dew')` |
| 8 | chest | `K.fx('tf_ripples')` |
| every 20 t while orbs live | each orb | `K.fx('dew_pulse')` |
| butterfly form, every 13-20 t | chest | `K.snd('flap_small')` |

### B1 우아한 날개 (`wing_strike`, 55 t; hit 15)
| t | where | calls |
|---|---|---|
| −8 (if the wings are Pyro) | chest | `K.fx('dendro_switch')`, `K.snd('dendro_switch')` |
| 0 | floor under her, rotated along the dive | `K.tele_sector(4.0, 60, 15)` (front arc r 4) |
| 0 | chest | `K.snd('flap_big')` |
| 8 | chest | `K.snd('wing_dive')` |
| 15 | floor under her (strike yaw) | `K.fx('wing_band')`, `K.snd('wing_strike')` |
| 18 | the trailing wing tip | `K.fx('wing_flare')` |
| 24-52 | chest | `K.snd('flap_small')` every 8 t |

### B2 화염 날개의 습격 (`wing_barrage`, 117 t; swings 0 / 26 / 64 / 89)
| t | where | calls |
|---|---|---|
| −8 | chest | `K.fx('pyro_switch')`, `K.snd('pyro_switch')` |
| each swing s | chest (swing yaw) | `K.fx('fire_swing')` (s 0, 64) / `K.fx('fire_swing_d')` (s 26, 89), `K.snd('fire_cres_launch')` |
| s+2..6 | each new crescent prop | `K.prop('fire')`, `K.fx('fire_spawn')` |
| from s+2, every 2 t | each crescent prop | `K.fx('fire_trail')` (every 3 t if two volleys overlap) |
| when a crescent locks its dive target P_k (≥ 10 t before it lands) | floor at P_k | `K.tele_disc(1.2, <land − now>, el=1)`, `K.snd('fire_cres_fly')` (once per volley) |
| landing | floor at P_k | `K.fx('fire_land')`, `K.snd('fire_cres_land')` |

### B3 날개 휩쓸개 (`flap_dive`, 59 t; slam 26, fan active 28-32)
| t | where | calls |
|---|---|---|
| −8 | chest | `K.fx('pyro_switch')`, `K.snd('pyro_switch')` |
| 0, 10 | chest | `K.snd('flap_big')` |
| 14 | floor under her slam point (her yaw) | `K.tele_sector(4.5, 90, 14, el=1)` (strike t28) |
| 21 | chest | `K.snd('wing_dive')` |
| 26 | chest | `K.fx('flame_slam')`, `K.snd('flame_slam')` |
| 28 | floor under her (her yaw) | `K.fx('flame_fan')`, `K.snd('flame_fan')` |
| 36-43, every 2 t | the floor under each wing tip | `K.fx('flame_trail')`; every 4 t `K.snd('flame_trail')` |

### B4 달빛 축복 (`coco`, 76 t; orb1 19, orb2 46)
| t | where | calls |
|---|---|---|
| −5 | chest | `K.fx('dendro_switch')`, `K.snd('dendro_switch')` |
| 5, 32 | chest | `K.fx('orb_charge')`, `K.snd('orb_charge')` |
| 19, 46 | the new orb | rig orb prop (or `K.prop('orb')` + a `K.prop('orb_ring')` child), `K.fx('orb_launch')`, `K.snd('orb_launch')` |
| every 11 t while it flies | orb | `K.snd('orb_fly')` |
| when its fuse has 10 t left (or it is within 2 b of the player) | floor under the orb | `K.tele_disc(2.8, 10)` |
| burst | floor under the orb | `K.fx('orb_burst')`, `K.snd('orb_burst')` |
| 30 | ball centre | `K.fx('cocoon_ball')`, `K.snd('cocoon_ball')` |

### B5 달빛 해제 (`release`, 96 t; detonation E = 53, revert 92)
| t | where | calls |
|---|---|---|
| 0 | chest | `K.fx('rel_fold')`, `K.snd('release_swoop')`; the typed caption "달빛 해제" is the core's `line/say` |
| 4 | chest | `K.snd('wing_dive')` |
| 13 | floor under her | `K.tele_disc(10.0, 40)` (E = 53: dodge by > 10 b or a dash) |
| 13, 20, 27 | the flare point at her side | `K.fx('rel_flare')`; t13 / t25 `K.snd('release_charge')` |
| 15, 25 | chest | `K.fx('rel_slashes')`, `K.snd('release_whirl')` |
| 35 (E−18) | floor under her | `K.fx('rel_ground_flash')` |
| 37 (E−16) | chest | `K.fx('rel_xglint')`, `K.snd('release_charge')` |
| 38 (E−15) | chest | `K.fx('rel_cage')` |
| 44 (E−9) | chest | `K.fx('rel_pod')`, `K.snd('release_wrap')` |
| 53 (E) | floor under her | `K.fx('rel_dome', r=10.0)`, `K.snd('release_boom')`, `K.hud('flash_white')`; t55 `K.hud('flash_lime')` |
| 60 (E+7) | chest | `K.fx('rel_tendrils')` |
| 63, 75 | chest | `K.fx('embers')` |
| 91 (E+38) | her back | `K.fx('wing_shatter')`, `K.snd('wing_shatter')` |
| 96 (E+43) | feet | `K.fx('land')`, `K.snd('land')` |

### Groggy (300 t), turn (24 t), chain re-form (18 t)
| t | where | calls |
|---|---|---|
| groggy start | feet | `K.snd('groggy')` |
| every 40 t | chest | `K.fx('motes')` |
| chain re-form start | the chain point at her left side | `K.fx('chain_reform')`, `K.snd('chain_reform')` |
| a new 달빛 이슬 during the groggy (still debuffed) | its spot | as in the transformation row |

### 달빛 고치 removed by a heal (the core's cure tick, as / at the healed player)
`K.fx('cure')` at the player's feet (beam 0-8 t, burst + gold ring from 6 t, emblem + sparkles from 11 t), `K.snd('cure_chime')`,
`K.hud('coc_off')`, `K.hud('buff_on')`, `K.hud('ab_buff')`, `K.hud('pop_buff')`, optional `K.hud('flash_gold')`.
At the fight end / death / abort / uninstall: `K.hud('clear')` (+ `fx/clear`).

### Death (`death`, 100 t)
| t | where | calls |
|---|---|---|
| 0 | her back (wings shown) | `K.fx('wing_shatter')` (butterfly form only), `K.snd('death')`, `fx/tele/clear` |
| 10, 25, 40, 55, 70, 85 | chest (rising as she dissolves) | `K.fx('death_motes')` |
| 90 | chest | `K.snd('death_motes')` |

## 10. Budgets

| moment (measured by `fxtests/peaks.py`, mcsim) | peak fx cards (cap 64) | telegraph cards (cap 40) |
|---|---|---|
| entrance (disc + motes + glow + burst) | 20 at t79 | 0 |
| H1 (kick_rise, kick_axe + ground_wave) | 12 at t40 | 7 (sector 2 + line 5) |
| B2, two volleys 26 t apart, 5 crescents each, trails every 2 t / 3 t | 44 / 41 at the first landings | up to 20 (2 x 5 markers) |
| B3 (slam, eruption, glide trails) | 17 at t28 | 2 |
| B5 (whole timeline of §9) | 31 at E+10 | 2 (until E+3) |
| cure | 11 | 0 |
| **in a real fight** (review fix FX-2): 3 orbit fights of 7000 t in the vanilla tick order (`S:mb2/integ3/peak.py`) | 53 / 43 / 45, always in B2 (the worst: swing 4 + its landings + a cure from a dew orb) | 20 / 18 / 20 |

No card or telegraph call is refused by the caps in those fights (the suites now count refused calls instead of a peak
that could not fail). What keeps it so: the decorative cards (the dew orbs' idle pulses, B2's flame tails) give way
from 48 live fx cards; the 3 dew orbs pulse 7 t apart; `fire_land` has 5 cards.

The card engine itself costs, per tick and only while cards live: one `@e[type=item_display,tag=rlk_bk]` pass with 2-5
score comparisons per card and at most one NBT merge per card per stage (no per-tick teleports). Telegraphs need no
ticking beyond that (client interpolation draws the fill).

## 11. Verification

- `scratchpad/mb2/fxtests/test_fx_engine.py <worktree>/roguelike` (mcsim): the SNBT of every summoned card parses;
  card / cardx stage ticks (show, go, hit, fade, kill), the fill reaching the rim on the hit tick, sector snapping and
  the disc fallback, the Pyro tints, ring / line card counts and the lane origin with `back`, both caps, telegraphs drawn
  while the fx cap is full, `clear`, the dead-player clear, every preset (runs, ≤ 64 cards, all expire, no scheduled
  ager left), every sound layer, HUD extra / sub / flags / titles, every prop look, `tele/clear`, `uninstall`.
- Validators on the worktree datapack: `check_refs` (no missing reference from the kit), `check_nbtpath` (0 invalid),
  `tools/check_mboss_pack.py` (0 problems; the kit uses no named dynamic function references), `check_macro` (only its
  known false positives on `function … with storage` calls, the same as `fx/nv/card`; every such call is exercised by
  the mcsim suite, which fails on a missing macro key).
- Renders (`scratchpad/mb2/fxrender/render_fx.py`, a ray caster that parses the generated presets and telegraph macros
  and draws them on the plaza floor of `tools/build_mboss_arena.py`): `scratchpad/mb2/renders/fx_sprites_marble.png`,
  `fx_sprites_pink.png` (every sprite on both floors), `fx_telegraphs_top.png` (every shape at 35 % / 75 % / hit−1 /
  hit, on marble and on the pink star), `fx_telegraphs_view.png` (player-eye views), `fx_presets.png` (22 presets),
  `fx_hud.png` (badges on the boss-bar lines, the actionbar notice, the pops).
