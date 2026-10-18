# Moonlit Illusion Butterfly (달빛 환영 나비 · 달빛의 화신) rig: API contract

This is the contract between the rig and the mid-boss module (`tools/mboss_butterfly/`, see `bf_contract.md` §9).
The module reads clips, events, parts, looks, props and objectives from the manifest, so retimed keys reach it on
the next module build.

Generator: `tools/build_mboss_butterfly_rig.mjs`, with `butterfly_paint.mjs` (textures), `butterfly_geometry.mjs`
(item models), `butterfly_pose.mjs` (skeleton, attachments, pose solver) and `butterfly_clips.mjs` (poses and clips).
It is built on the shared mid-boss libraries, as the Corrupted Guardian is: `mboss_rig_math.mjs`, `mboss_paint_lib.mjs`
(also the SDF `Grid` painter: polygons, strokes, bevels, light, tone ramps), `mboss_model_lib.mjs` (also
`mirrorModel`, `cardY`, `shiftModel`), `mboss_rig_clips.mjs` and `mboss_rig_compile.mjs` (also the per-tick
`extraLines` hook that carries the form and look switches inside the clips).

```
node tools/build_mboss_butterfly_rig.mjs --resourcepack <unpacked RP> [--datapack <dp>] [--no-paint | --paint a,b] [--debug-dp <scratch dir>] [--allow-steps]
```

- It owns and rewrites `data/rlk/function/mboss/butterfly/rig/**`. Never hand-edit those files.
- In the RP it writes:
  - `assets/rlk/textures/mboss/butterfly/*.png` (+ `fwg_*.png.mcmeta`), registered in `assets/minecraft/atlases/items.json`;
  - `assets/rlk/models/item/mboss/butterfly/*.json` (57 models);
  - `assets/rlk/items/mboss/butterfly/*.json`.
  Stale files of the three folders and stale atlas entries are removed.
- The manifest is `tools/mboss_butterfly_rig_manifest.json`.
- `--paint a,b` repaints only the named sprites; `--no-paint` keeps the textures on disk.
- `--debug-dp <scratch dir>` also writes the exact per-tick poses (`bf_dbg/<clip>/<t>`, `bf_dbg/rest_h`,
  `bf_dbg/rest_b`) and a copy of the rig for the offline renderer. It never writes into the real pack.

All functions below are `rlk:mboss/butterfly/rig/...`. Unless a line says otherwise, **@s is the rig anchor** (the
boss body). Call them `as` the anchor and `at` it.

## 1. Calls

| function | when | what |
|---|---|---|
| `init` | load (idempotent) | Adds the objectives (§7). |
| `spawn` | once, as/at the anchor | Kills old parts and summons the 30 parts in the rest pose of the stored form (`bfRigForm`, human by default) at the anchor's position and yaw. Queues that form's idle (`idle_h` / `idle_b`). Re-applies the stored wing look and crescent tell. |
| `spawn_hidden` | instead of `spawn`, before the entrance | The same in human form, but every part starts at scale 0 and `entrance` is queued; play it in the same tick. |
| `tick` | **every game tick**, after the AI: `execute as <anchor> at @s run function rlk:mboss/butterfly/rig/tick` | Respawns the parts if they are missing (the rig restarts in its form's idle). The parts follow the anchor position and yaw (`teleport_duration` 1). Advances the clip, applies its keys and form/look switches, counts the flash down. |
| `play/<clip>` | any time | Starts `<clip>` from tick 0 at the next `tick` (the same game tick when `tick` runs later). The first key segment blends from the current pose over at least 3 t (`blend`; 2 for `run_h`, 4 for `glide_b`, 6 for `death`). |
| `kill` | cleanup | `kill @e[type=item_display,tag=rlk_mb_butterfly_part]`. Props are separate (`prop/clear`). |
| `uninstall` | optional | `kill`, `prop/clear`, the face marker and the objectives (the module may remove the objectives itself). |
| `form/human` | instant | `bfRigForm` 1, every part snaps to the human rest pose (wings, glow overlays, tendrils and core at scale 0), `idle_h` queued. |
| `form/butterfly` | instant | `bfRigForm` 2, the hovering butterfly rest pose (toes 1.2 b up, wings spread), `idle_b` queued. |
| `look/dendro`, `look/pyro`, `look/flat` | element state | Stores the wing look (`bfRigLook` 0/1/2) and swaps the item models of the 10 look parts (§3). |
| `look_apply` | after a manual score change | Re-applies `bfRigLook` and `bfRigTell`. |
| `tell/on`, `tell/off` | optional pattern tells | The two big crescents (`hand_r_a`, `hand_l_a`) glow lime / go back to navy (`bfRigTell`, kept over a respawn). |
| `flash` | on a body hit (optional) | Pale lime outline (`Glowing`, `#F2FFD0`) on the solid parts for 3 t (`flash_tick`, `flash_off`). |
| `face/player` | as needed | Instant yaw toward the nearest non-spectator player. |
| `face/track` | each tick while tracking | Turns at most 12° per call toward the nearest player (yaws normalised into [-180°, 180°); temporary marker `rlk_mb_bf_face`). |
| `face/set {yaw:<deg>}` | macro | Sets the anchor yaw. |
| `prop/cocoon`, `prop/pod`, `prop/orb` | patterns | Free props at the execution position and yaw (§4). |
| `prop/clear` | cleanup | Kills every prop (`rlk_mb_bf_prop`). |

`transform`, `release`, `revert` and `death` switch the form themselves at the right tick (manifest `forms`):
`transform` → butterfly at 4, `release` → human at 92, `revert` → human at 39; `death` is human from tick 0 (the
wings shrink away over its 6 t blend). The module never needs `form/*` around these clips; `form/*` are for reloads,
tests and a groggy that starts in butterfly form.

## 2. Entities, tags, cost

- 30 `item_display` parts (budget 34) with **fixed UUIDs** `524c4b4d-4246-4c00-8000-0000000000NN`
  (int array `[I;1380731725,1111903232,-2147483648,NN]`), NN = 01..1e in the order below.
- Per tick: 30 `tp <uuid>` (follow) and the keys of the parts whose interpolation segment starts on that tick.
  No selectors on the hot path, no macros.
- One butterfly rig at a time; a second `spawn` kills the first.
- Tags on every part: `rlk_room`, `rlk_mb_aux`, `rlk_mb_part`, `rlk_mb_butterfly_part`, `rlk_mb_bf_<part>`.
  Alias tags for the module's fx anchors: `rlk_mb_bf_body` (on `torso`), `rlk_mb_bf_hand_r` (on `hand_r_a`),
  `rlk_mb_bf_hand_l` (on `hand_l_a`). The manifest lists them as `{name, tag, alias_of}`.
- `view_range` 2.5, `width`/`height` 16, brightness 12-15 (sky 15).

| NN | part | model (dendro look) | scale | what |
|---|---|---|---|---|
| 01 | `pelvis` | pelvis | 1 | hips, navy hip plates and lime fins |
| 02 | `torso` | torso | 1 | waist and chest under the mane |
| 03 | `collar` | collar | 1 | white fur mane: front bib, sides, the hood and the royal-blue capelet tips at the back |
| 04 | `head` | head | 1 | faceted steel helm-mask, crown, side plates, cheek blades |
| 05 | `head_glow` | head_glow | 1 | coral eyes and the lime chevron (brightness 15) |
| 06 | `crest` | crest | 1 | the two antennae and the lime lyre streamers |
| 07, 08 | `fan_r`, `fan_l` | fan_r, fan_l | 1.25 | navy shoulder plates with lime spiral eyes and the side-blade fans |
| 09-0e | `thigh_r`, `shin_r`, `foot_r`, `thigh_l`, `shin_l`, `foot_l` | same names | 1 | digitigrade legs: thigh, shin with white knee spike and blue fur boot, hoof (cream, with claws) |
| 0f, 11 | `hand_r_a`, `hand_l_a` | crescent_r, crescent_l (tell: crescent_tell_*) | 1 / .82 | the floating crescent hands (big one at her right) |
| 10, 12 | `hand_r_b`, `hand_l_b` | shard_r, shard_l | 1 / .72 | the blade links of the crescent chains |
| 13 | `flakes` | flakes | 1 | the floating moon flakes behind her |
| 14, 15 | `fwing_l`, `fwing_r` | fwing_*_dendro | 3.5 (half-size model) | forewings: steel spar with a curled hook, lime baroque scroll plate with spiral eye, iridescent opal lobes in lime rims, violet trailing rim |
| 16, 17 | `fwglow_l`, `fwglow_r` | fwglow_*_dendro | 3.5 | translucent holographic shimmer over the forewing lobes (animated, brightness 15) |
| 18, 19 | `hwing_l`, `hwing_r` | hwing_*_dendro | 2.4 (half-size model) | hindwings: lime scroll lobe with raised volute, long blade with a glowing blue tip |
| 1a-1d | `tendril_ul`, `tendril_ur`, `tendril_ll`, `tendril_lr` | tendril_*_dendro | 1.1 / 1.55 | ribbon tendrils hanging beside the chest, outside the body |
| 1e | `core` | core | 1 | the chest light (transform, coco, release) |

The wing-side parts, the overlays, the tendrils and the core are at scale 0 in human form.

**Two separate wing sets.** Each side's forewing and hindwing pivot at their own root on the upper back, 0.42 b
beside the spine (`butterfly_pose.mjs` ATTACH). Their cards start further out (`butterfly_geometry.mjs` WING_FIT:
the card is shifted outward and modelled at half size, so PART_SCALE is doubled). In the hovering rest pose the
inner edges of the two forewings are about 0.6 b from the spine at head height and lean outward as they rise, so
open space shows between the wings, around the head and the crest, from the front and from the back (the PDF render,
v2 f2070). No wing plate crosses the midline. The hook tips are ±3.1 b out and 6.0 b over the floor; the hindwing
blade tips are ±2.75 b out at 3.0 b. A wing euler turns the whole set about its root, so flaps keep them apart;
poses that raise a wing far past vertical (`WINGS_V`, `WINGS_POD`) can still bring the tips together on purpose.

## 3. Looks

- `bfRigLook`: 0 dendro (default), 1 pyro, 2 flat. The 10 look parts (`fwing_*`, `fwglow_*`, `hwing_*`, `tendril_*`)
  swap between `<part>_dendro`, `<part>_pyro` and `<part>_flat`.
  - **dendro**: lime frames and scroll plates, white-mint / lime membranes, opal shimmer, violet rims, blue blade tips.
  - **pyro**: membranes, hindwing blades and ribbons in orange-gold `#FAD77C` → magenta `#C680A2`; the steel and
    navy stay.
  - **flat**: one flat bright lime (`#B6E35A` family) without detail, for the transformation and the shatter.
- Clips can show the flat look for a while without touching `bfRigLook` (`look/temp_flat`, `bfRigFlat` 1):
  `transform` 3-12, `release` 87-92, `revert` 34-39, `death` 0-6. When it ends the clip calls `look_apply`, so a
  look set by the module during the clip wins afterwards.
- **Iridescence**: each forewing lobe is a painted base card plus a translucent overlay card (`fwglow_*`, two cards 0.03 b in
  front of and behind it, brightness 15). The overlay texture `fwg_<look>` is an 8-frame vertical strip with
  `{"animation":{"frametime":4,"interpolate":true}}`, so the shimmer slides through the rainbow every 1.6 s. Frame 0
  alone is a complete static look if a client does not animate item-atlas sprites.

## 4. Props (free `item_display`s, not rig parts)

Each call summons at the execution position, turned to the execution yaw. Tags: `rlk_room`, `rlk_mb_aux`,
`rlk_mb_bf_prop`, `rlk_mb_bf_prop_<kind>`, and for that call only `rlk_mb_bf_prop_new`. `tick` never moves them.

| function | displays | notes |
|---|---|---|
| `prop/cocoon` | `cocoon` ×3 (fixed), `cocoon_halo` ×3 (billboard centre) | The entrance cocoon, 3.8 b tall: a navy-green kite of wrapped wing plates with two curled navy horns, crossing lime seams, a glowing lime window and a lime spike at the bottom; the halo glows behind it. Its origin is the cocoon's centre: summon it about 2.15 b above the floor. The module clears it at the burst (79). |
| `prop/pod` | `pod` ×2.5 | The wrapped wing pod (코코볼 ball, the 달빛 해제 wrap): 8 lime leaf panels with white-mint lobes in navy frames, seam glow, shoulder-plate caps; 3.4 b tall, r 1.4 b, centred on the execution point. |
| `prop/orb` | `orb` ×1, `ring` ×1 twice (tilted) | The 달빛 축복 orb: a 1.7 b lime glass sphere and two gyroscope rings; spin the rings with transformation keys. |

## 5. Body travel versus clip motion

- The rig follows the anchor. **Horizontal travel is the module's job** (`mv/*` on the body); the clips have no
  horizontal root offsets, so they never double the module's moves or snap back at the end.
- Heights are in the clips: the butterfly hovers with the toes 1.2 b up (root +1.13 b), the `idle_b` bob is about ±0.1 b,
  jumps, flips and climbs go up to about +4.2 b (`flap_dive`), the release whirl and blast hover at +3.0-3.4 b.
- Root spins (`kick_combo` backflip, `kick_jump` spins, `vacuum` backflip, `wing_barrage` swings, `release`
  tumbles) turn about the hip pivot (1.5 b up) and end on whole turns.

## 6. Clips (ticks at 20/s; events are clip ticks; `then` = the clip that follows by itself)

Ids follow the module's stub manifest. Event names and ticks follow plan.md "Stage-2 decisions" Q2 (the spec's §3
retimes); `kick_jump` keeps `disc` as an alias of `orb`. The extra events are hints for fx. **No clip carries
horizontal root travel** (plan.md Q1): the root's x/z offset is 0 in every key, so the module moves the body.

| clip | id | len | then | events | notes |
|---|---|---|---|---|---|
| `idle_h` | 0 | 40 | loop | | Standing idle: breathing sway; the crescents and flakes bob; the crest sways. |
| `step_h` | 1 | 16 | loop | | Short strafing step (0.1-0.15 b/t; the module moves the anchor). |
| `run_h` | 2 | 8 | loop | | Burst-run (0.6-0.8 b/t for about 5 t): body 30° forward, fans swept back, crescents trailing. |
| `back_h` | 3 | 12 | idle_h | | Backing off at walking pace. |
| `turn_h` | 4 | 24 | idle_h | | After groggy: turns from her back (root yaw 180, the `groggy_h` facing) to the anchor facing. |
| `kick_combo` | 5 | 51 | idle_h | run 0, **hit1 8**, backflip 10, hop 22, leap 34, **hit2 40** | H1 달빛 발차기: run in, rising flip kick at 8, backflip, sideways-hop wind-up, flying leap, axe kick at 40, landing. |
| `kick_jump` | 6 | 65 | idle_h | tell 0, **sweep 13**, sweep_end 19, jump 33, orb 45 (= disc), kick 52, **impact 55**, land 59 | H2 달빛 점프: the crescent chain lines up at her left (tell 0-13), 360° low sweep 13-19, spiral jump at 33, the orb forms at 45, kicked down at 52, impact 55, landing 59. |
| `dash_kick` | 7 | 50 | idle_h | charge 0, dash 10, dash_end 12, **kick 15**, ring 19 | H3 달빛 돌진: charge 0-10, dash 10-12 (the module moves the anchor 5-6 b), lunge kick at 15, the ring at 19. |
| `vacuum` | 8 | 41 | idle_h | crouch 0, tell 9, stomp 16, **blade 17**, backflip 17, land 38 | H4 광폭한 진공: crouch, glint, the stomp at 16 launches the vertical blade at 17, backflip 17-38. |
| `groggy_h` | 9 | 40 | loop | | Groggy: motionless with her back turned (root yaw 180), fans drooped, crescents hidden. |
| `entrance` | 10 | 106 | idle_h | nameplate 57, glow 61, whiteout 71, **burst 79**, land 90, stand 106 | Hidden (scale 0) until the burst; she drops from 4 b, lands at 90 and stands by 106. Use `spawn_hidden` + `prop/cocoon`. |
| `transform` | 11 | 30 | idle_b | glow 0, open 4, **sphere 6**, rings 9, spread 12 | Human → butterfly: core glow, folded flat-lime wings at 4 (form switch), the light sphere at 6, wings unfold 4-12, hover lift. |
| `idle_b` | 12 | 22 | loop | | Hover flap: forewing leads, hindwing lags 2-3 t, ribbons lag 4 t; body rises on the downstroke. |
| `glide_b` | 13 | 16 | loop | | Gliding travel: body pitched forward, wings swept back, legs trailing. |
| `wing_strike` | 14 | 55 | idle_b | bank 0, dive 12, **hit 15** | B1 우아한 날개: bank and climb 0-9, dive 12-15, wing-edge arc at 15, climb and flutter. |
| `wing_barrage` | 15 | 117 | idle_b | **swing1 5, swing2 31, swing3 69, swing4 94** | B2 화염 날개의 습격 (call `look/pyro` first): a 5 t wind-up, then four spinning wing swings. |
| `flap_dive` | 16 | 59 | idle_b | rise 0, dive 22, **slam 26**, fan 28, glide 34 | B3 날개 휩쓸개 (pyro): flaps and a rise to +4.2 b, head-first dive 22-26, wing slam at 26, flame fan 28-32, low glide. |
| `coco` | 17 | 76 | idle_b | wrap 5, **orb1 19**, ball 30, ball_open 42, **orb2 46** | B4 달빛 축복: wings wrap forward, orb 1 at 19 (`prop/orb`), the ball 30-42 (`prop/pod`), orb 2 at 46. |
| `release` | 18 | 96 | idle_h | swoop 0, whirl 28, cup 31, flash 35, glint 37, rings 38, wrap 44, **detonation 53**, hover 56, shrink 87, flat 87, shatter 91, revert 92, land 96 | B5 달빛 해제: swoop, climb, two tumbles 12-28, cup, ground flash, X glint, ring cage, the pod wrap 44-52, detonation at 53, hover, the wings go flat lime and shrink (87) and shatter (91), human at 92, landing at 96. |
| `revert` | 19 | 43 | idle_h | shrink 30, flat 34, shatter 38, revert 39, land 43 | Butterfly → human without the blast. |
| `death` | 20 | 100 | hold | stagger 0, shatter 6, kneel 24, dissolve 40, gone 100 | From either form: stagger, the wings shrink away (flat lime) by 6, she kneels, the crescents and flakes fade, she scales out by 100. Call `kill` after 100. |
| `chain_reform` | 21 | 18 | idle_h | | The crescent chain re-forms after groggy. |

The clips are a first pass that times the body against the events (the key poses are placeholders for the separate
clips step); retune keys in `butterfly_clips.mjs` and the manifest and the module follow on the next build.

## 7. Manifest and objectives

- `parts`: `{name, uuid, tag, model, brightness, scale, look}` per part, then the alias entries `{name, tag, alias_of}`.
- `clips`: `{id, name, len, loop, next, events, keyFiles, keys, note, form: {start, end, switch?}, anchors}`.
  `anchors[event]` holds fx anchor points at that event tick (hoof tips `foot_l/r`, forewing hook tips `fwtip_l/r`,
  hindwing blade tips `hwtip_l/r`, `core`, `head`, the big crescents `hand_r_a`/`hand_l_a`) in rig coordinates,
  blocks from the anchor (x her left, y up, −z her front): the body-frame position is `^x ^y ^-z`.
- `forms`: `{clip: [tick, form]}` for the clips that switch the form themselves.
- `form_states`: per form its id, idle clip, rest anchors and toe height (human 0, butterfly 1.2 b).
- `looks` (`dendro`, `pyro`, `flat`), `look_ids`, `look_parts`, `props` (function, tag, displays, note),
  `objectives`, `textures`, `atlas_px`.

| objective | holder | meaning |
|---|---|---|
| `bfRigC` | anchor | current clip id |
| `bfRigT` | anchor | tick within the clip (-1 = queued by `play`) |
| `bfRigF` | anchor | hit flash countdown |
| `bfRigY` | fake players | `face/track` scratch |
| `bfRigForm` | anchor | 1 human, 2 butterfly |
| `bfRigLook` | anchor | wing look 0 dendro, 1 pyro, 2 flat |
| `bfRigFlat` | anchor | 1 while a clip shows the temporary flat look |
| `bfRigTell` | anchor | 1 while the crescents glow |

## 8. Build checks and budgets

The generator refuses to write a rig that fails these (`--allow-steps` turns the rotation checks into warnings):

- **Rotation per tick and per key:** no part turns more than 120° between two ticks or within one interpolation
  segment (blend-ins included). Large one-tick steps are also solved at the half tick (warning when the client's
  slerp leaves the authored path by more than 35°).
- **Keys:** the first key at tick 0, the last at the clip length, `next` must name a clip.
- **Parts** ≤ 34; **item models** within −16..32 (element rotations are single-axis multiples of 22.5° by
  construction).
- **Atlas:** ≤ 2 M px in all (now 54 sprites, 1.06 M px), every side a multiple of 16, ≤ 512 px wide and
  ≤ 1024 px tall (the 8-frame strips).
- Compiled: 22 clips, about 760 key files and 10 350 part keys. A part gets a key only where the client's lerp/slerp
  would drift from the authored pose by more than 0.012 b, 0.5-3° (per part) or 1.5 % scale.

## 9. The model

- Height 2.8 b from hoof to helm (BH), single superset rig for both forms; right-side models are mirrored copies of
  the left (no negative scales). Coordinates: +X her left, +Y up, −Z her front (the item models face −Z, the display
  transformations mirror Z).
- Textures are painted procedurally in `butterfly_paint.mjs` from the `model.md` palettes: signed-distance shapes,
  bevelled height fields lit from the upper left, tone ramps, groove/ridge reliefs, fur clumps (`furPainter`) for the
  mane and boots. The membranes are marbled white-mint → lime with the violet trailing rim; the hindwing blade tips
  and the eyes are brightness 15.
- Legs are digitigrade (hip, knee, hock, hoof, a slight A-stance) with an FK chain per side; the crescent hands
  float on paths relative to the torso; the two wing sets pivot on the upper back beside the spine and the ribbon
  tendrils hang beside the chest (torso frame).

## 10. Not in the rig (module / fx code)

- Particles, tinted fx cards (crescent slashes, star flares, sphere bursts, the X glint, the ring cage), decals and
  hazards; screen effects; sounds (vanilla only).
- Moving the props (orb flight, the pod, the cocoon burst).
