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
| `play/<clip>` | any time | Starts `<clip>` from tick 0 at the next `tick` (the same game tick when `tick` runs later). The first key segment blends from the current pose over at least 3 t (`blend`; 2 for `run_h`, 4 for `glide_b`, 10 for `death`). |
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
`transform` → butterfly at 4, `release` → human at 92, `revert` → human at 37; `death` is human from tick 0 (the
wings, ribbons and chest glow shrink away over its 10 t blend, in step with the body). The module never needs `form/*`
around these clips; `form/*` are for reloads, tests and a groggy that starts in butterfly form.

**Facing.** No clip turns the whole body away for good: `groggy_h` and `turn_h` carry no root yaw, because the module
turns the anchor itself (`groggy/begin` faces it away from the player, `recover` turns it back with `mv/turn` 9°/t).
Spins inside a clip (`kick_jump`, `dash_kick`, `wing_barrage`, `release`) end on whole turns, so the body faces the
anchor yaw again when the clip ends.

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
| 01 | `pelvis` | pelvis | 1 | hips (a smooth turned solid flaring out of the waist, rounded crotch), navy tasset blades and steel fins |
| 02 | `torso` | torso | 1 | waist and chest under the mane (smooth elliptic turned solid, lavender belly band, periwinkle swirls) |
| 03 | `collar` | collar | 1 | white fur mane: front bib, sides, the hood and the royal-blue capelet tips at the back |
| 04 | `head` | head | 1 | faceted steel helm-mask, a smooth slate helmet dome behind it, crown, cheek blades |
| 05 | `head_glow` | head_glow | 1 | coral eyes and the lime chevron (brightness 15) |
| 06 | `crest` | crest | 1 | the two antennae (thin periwinkle rods) and the lime lyre streamers (one card each) |
| 07, 08 | `fan_r`, `fan_l` | fan_r, fan_l | 1.25 | navy shoulder plates with lime spiral eyes and the side-blade fans |
| 09-0e | `thigh_r`, `shin_r`, `foot_r`, `thigh_l`, `shin_l`, `foot_l` | same names | 1 | digitigrade legs: thigh, shin with white knee spike and blue fur boot, hoof (cream, with claws) |
| 0f, 11 | `hand_r_a`, `hand_l_a` | crescent_r, crescent_l (tell: crescent_tell_*) | 1 / .82 | the floating crescent hands (big one at her right) |
| 10, 12 | `hand_r_b`, `hand_l_b` | shard_r, shard_l | 1 / .72 | the blade links of the crescent chains |
| 13 | `flakes` | flakes | 1 | the floating moon flakes behind her shoulders (0.2-0.4 b behind the spine: behind the forewing plates in butterfly form) |
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
v2 f2070). The hook tips are ±3.1 b out and 6.0 b over the floor; the hindwing blade tips are ±2.75 b out at 3.0 b.
A forewing card reaches 2.9 b from its root and 2.7 b up, so rolling it up past about 25° brings its upper inner
edge across the midline: the raised, closed, cupped and wrapped poses of §6.1 lean the tops back or sweep them
forward instead, and every clip keeps the two wing sets apart and out of the body (§8). In butterfly form the four
diamond `flakes` over the shoulders are at scale 0 (the forewings sweep through their place on every beat); they
fade out during `transform` (4-6) and come back with the human form.

## 3. Looks

- `bfRigLook`: 0 dendro (default), 1 pyro, 2 flat. The 10 look parts (`fwing_*`, `fwglow_*`, `hwing_*`, `tendril_*`)
  swap between `<part>_dendro`, `<part>_pyro` and `<part>_flat`.
  - **dendro**: lime frames and scroll plates, white-mint / lime membranes, opal shimmer, violet rims, blue blade tips.
  - **pyro**: membranes, hindwing blades and ribbons in orange-gold `#FAD77C` → magenta `#C680A2`; the steel and
    navy stay.
  - **flat**: one flat bright lime (`#B6E35A` family) without detail, for the transformation and the shatter.
- Clips can show the flat look for a while without touching `bfRigLook` (`look/temp_flat`, `bfRigFlat` 1):
  `transform` 3-14, `release` 87-92, `revert` 32-37, `death` 0-10. When it ends the clip calls `look_apply`, so a
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
| `prop/cocoon` | `cocoon` ×3 (fixed), `cocoon_halo` ×3 (billboard centre) | The entrance cocoon, 4 b tall: a turned diamond of two wrapped slate-green wing plates (lime leading edges crossing in an X, a diamond window over the glowing lime bud inside, engraved scrolls, a scalloped rim), two ram's-horn scrolls at the widest corners and a lime crystal spike at the bottom; the halo glows behind it. Its origin is the cocoon's centre: summon it about 2.15 b above the floor. The module clears it at the burst (79). |
| `prop/pod` | `pod` ×2.5 | The wrapped wing pod (코코볼 ball, the 달빛 해제 wrap): an egg of the four folded wings, forewings over the front (sculpted lime scroll plates, opal lobes, steel spars) and hindwings over the back (navy spiral eyes, blades), over a glowing core that shows in the front and back seams; the hindwing blade tips stick out below the sides; 3.5 b tall, r 1.4 b, centred on the execution point. |
| `prop/orb` | `orb` ×1, `ring` ×1 twice (tilted) | The 달빛 축복 orb: a 1.7 b lime glass sphere and two gyroscope rings; spin the rings with transformation keys. |

## 5. Body travel versus clip motion

- The rig follows the anchor. **Horizontal travel is the module's job** (`mv/*` on the body): every key of every clip
  has the root at x = z = 0 (the build fails otherwise), so the clips never double the module's moves or snap back
  at the end. Leans, spins and heights stay in the clips.
- Heights: the human stance sits 0.06 b low with the knees a little bent; jumps and flips lift the hips up to
  +1.55 b (`kick_combo` backflip), +2.55 b (`kick_jump` spiral and somersault) and +2.6 b (`vacuum` backflip). The
  butterfly hovers with the toes 1.2 b up (root +1.13 b, the `idle_b` bob ±0.12 b), climbs to +3.0 b (`wing_strike`
  flutter), swoops down to +0.75 b (`release`), whirls at +3.05 b and hovers at +2.1-2.3 b after the blast.
- Grounded human keys plant the hooves with a leg IK, so crouches, landings and steps never sink into the floor;
  the hooves stay where the anchor is (the module's moves slide them with the body). `run_h` plants each hoof from
  its landing ahead of the hips to its push-off behind them.
- Knees never fold past about 165° (tucks included) and never bend backward past straight.
- Root spins and flips turn about the hip pivot (1.5 b up) and end on whole turns: `kick_combo` backflip (8-16),
  `kick_jump` sweep (13-19), two spiral turns (33-44) and forward somersault (44-52), `dash_kick` ring turn (16-22),
  `vacuum` backflip (18-38), `wing_barrage` four spins, `release` two cartwheels (18-30).

## 6. Clips (ticks at 20/s; events are clip ticks; `then` = the clip that follows by itself)

Ids follow the module's stub manifest. Event names and ticks follow plan.md "Stage-2 decisions" Q2 and the headers of
the `mb2/spec/*.md` pattern specs; `kick_jump` keeps `disc` as an alias of `orb`, `vacuum` `tell` as an alias of
`glint`, `release` `xglint` / `cage` as aliases of `glint` / `rings` (the stub names). The other events are hints for
fx and anchors (manifest `anchors[event]`). The poses come from the footage key frames (v1-v4, model.md sheets 05,
08, 09) and the per-tick timelines of the specs.

**Wind-up retime** (user tuning "선딜 좀 줄이고", as the Guardian's): the keys stay authored on the spec timelines and
`RETIME` (`butterfly_clips.mjs`) plays the ten damaging clips with about 25 % shorter wind-ups: piecewise-linear knots
[authored tick, played tick] from [0, 0] to [authored length, played length], keys and events mapped and rounded half
up (the build stops if two keys collide or a segment would slow the clip down; the rig compiler also refuses a part
turning more than 120° per tick, which is why the H2 spiral-jump spin 33-45 and the B5 swoop stay 1:1). The strikes
and their follow-throughs sit on 1:1 segments; only the wind-ups are compressed and the recoveries after the last hit
are shifted. The manifest carries `retime` and `authoredLen`; the module maps its own authored ticks with `api.rt`.
The table below is the **authored** timeline; the played lengths and events are:

| clip | played len (authored) | played events |
|---|---|---|
| `kick_combo` | 43 (51) | run 0, plant 5, **hit1 8**, backflip 9, land1 16, hop 19, hop2 22, leap 25, swirl 28, **hit2 32**, land 36 |
| `kick_jump` | 52 (65) | tell 0, **sweep 10**, sweep_end 16, jump 22, orb 34 (= disc), kick 39, **impact 42**, land 46 |
| `dash_kick` | 46 (50) | charge 0, dash 6, dash_end 8, **kick 11**, ring 15 |
| `vacuum` | 37 (41) | crouch 0, tell 5 (= glint), stomp 12, **blade 13**, backflip 13, land 34 |
| `transform` | 29 (30) | glow 0, open 3, **sphere 5**, rings 8, spread 11 (butterfly from 3) |
| `wing_strike` | 51 (55) | bank 0, dive 4, **hit 11** |
| `wing_barrage` | 95 (117) | **swing1 4, swing2 24, swing3 52, swing4 72** |
| `flap_dive` | 52 (59) | rise 0, **dive 13**, slam 19, fan 21, glide 26 |
| `coco` | 64 (76) | wrap 3, **orb1 14**, ball 22, ball_open 30, **orb2 34** |
| `release` | 83 (96) | fold 0, swoop 3, climb 7, whirl 14, cup 23, flash 26, glint 28, rings 28, wrap 33, snap 39, **detonation 40**, hover 50, shrink 74, flat 74, shatter 78, revert 79, land 83 (human from 79) |

| clip | id | len | then | events | motion |
|---|---|---|---|---|---|
| `idle_h` | 0 | 40 | loop | | Fighting stance (v1 f560): knees a little bent, torso 12-14° forward, slow breathing, a weight shift from hip to hip; crescents and flakes bob, the crest sways. |
| `step_h` | 1 | 16 | loop | | Two light steps in place, hooves lifted 0.3 b, a dip on each contact and a lean over the stance leg (the module moves the anchor 0.1-0.15 b/t in any direction). |
| `run_h` | 2 | 8 | loop | | Burst-run: two bounding strides, body 30° forward, fans swept back, crescents trailing behind; each hoof lands ahead of the hips (2, 6), is pushed back under her (3, 7) and leaves the floor behind her (4, 0), with a short flight between. |
| `back_h` | 3 | 12 | idle_h | | Backing off: two steps, each hoof set down behind, torso a little more upright. |
| `turn_h` | 4 | 24 | idle_h | | After groggy: steps round from the drooped groggy stance into the fighting stance while the module turns the anchor; crescents still hidden for `chain_reform`. |
| `kick_combo` | 5 | 51 | idle_h | run 0, plant 5, **hit1 8**, backflip 9, land1 16, hop 22, hop2 28, leap 32, swirl 36, **hit2 40**, land 44 | H1 (v1 9.87-12.40 s): burst-run with the right knee chambered from 2, plant and chamber (5), the kick whips up to vertical with the crescent locked on the shin and the body leaning back (hit1 8), carried over into a backflip (apex +1.55 b at 12, lands 16), two sideways hops with the kicking leg stretched back and the body coiled (22, 28), leap (32) into a horizontal flying kick (34), the leg raised overhead (36-38), the diagonal axe kick down to her front-right (hit2 40), landing crouch (44). |
| `kick_jump` | 6 | 65 | idle_h | tell 0, **sweep 13**, sweep_end 19, jump 33, orb 45 (= disc), kick 52, **impact 55**, land 59 | H2 (v1 25.33-28.60 s, v4): three crescent pieces line up vertically at her left by 6, the tail blade passing in front of the mane (tell; the module adds `tell/on`), the 360° low sweep pivoting on the right hoof with the left leg straight out at knee height (13-19), recovery, the spiral jump with two rising turns (33-44), the orb at her raised right foot as she tips into a forward somersault (45-51), the axe kick down (52), landing (59). |
| `dash_kick` | 7 | 50 | idle_h | charge 0, dash 10, dash_end 12, **kick 15**, ring 19 | H3 (v2 2.95-6.47 s): gathering crouch (0-8), coil side-on with the right leg cocked (9), dash low and stretched (10-12, the module moves 5-6 b), the high side kick straight out to her right with the crescent on the shin (15), one full turn with the leg out for the ring (16-21), landing (22), recovery. |
| `vacuum` | 8 | 41 | idle_h | crouch 0, tell 9 (= glint), stomp 16, **blade 17**, backflip 17, land 38 | H4 (v2 12.80-16.60 s): low cat-like crouch (0-9), rear-up with the right leg high (13-14), the stomp (16), a slow high backflip from 18 (apex +2.6 b at 27), landing crouch (38). |
| `groggy_h` | 9 | 40 | loop | | Groggy (v4): slack stance, torso 6° forward, head low, fans drooped, crescents hidden, a slow sway; the module keeps the anchor turned away. |
| `entrance` | 10 | 106 | idle_h | nameplate 57, glow 61, whiteout 71, **burst 79**, land 90, stand 106 | Hidden (scale 0) until the burst; revealed curled 3.6 b up with the crescents scattered, the drop with a slight tumble (80-89), the wide landing crouch with the crescents spread (90), standing by 106. Use `spawn_hidden` + `prop/cocoon`. |
| `transform` | 11 | 30 | idle_b | glow 0, open 4, **sphere 6**, rings 9, spread 12 | Human → butterfly (v2 24.10-24.70 s): sinks and rises in the sheath (core), the folded flat-lime panels behind the shoulders at 4 (form switch), core flash 5, sphere 6, the wings unfold 4-12 while she lifts into the hover, flung wide at 12, element look from 14, a big flap (18-21) into the `idle_b` phase. |
| `idle_b` | 12 | 22 | loop | | Hover flap: forewing ±14°, hindwing 2.5 t late at 60 %, ribbons 4-6 t late, body bob ±0.12 b rising on the downstroke, legs and fans trail the beat. |
| `glide_b` | 13 | 16 | loop | | Gliding: body 16° forward, wings held swept back 30° with a small flutter, legs trailing, ribbons streaming. |
| `wing_strike` | 14 | 55 | idle_b | bank 0, dive 8, **hit 15** | B1 (v2 35.20-37.92 s): lift with one big flap (0-7), bank to 80° with the left wing hanging as a blade (8-11), swoop 1 b off the floor (13-15) with the wing edge sweeping through (hit 15), pull-up and climb to +3 b (17-27), fluttering rolls and quick flaps (31-49), back to the hover. |
| `wing_barrage` | 15 | 117 | idle_b | **swing1 5, swing2 31, swing3 69, swing4 94** | B2 (v3 4.30-10.70 s; call `look/pyro` first): each swing has a 5 t wind-up (body turned 75° away, one wing swept back and raised, the other low) and one full turn with the wings flung wide (the crescents at s+2..s+6); swings 1 and 3 spin on a 26° diagonal, 2 and 4 flat; alternating directions; hover flaps between. |
| `flap_dive` | 16 | 59 | idle_b | rise 0, **dive 20**, slam 26, fan 28, glide 33 | B3 (v3 10.70-14.60 s; pyro): V-up and lean back (tell), big downstroke and upstroke, the rise with the wings closed above her (15-19), the head-first dart dive (20-25), the slam forward-down (26), the fan (28-32), a low glide banked to her right (33-43), settling flaps. |
| `coco` | 17 | 76 | idle_b | wrap 5, **orb1 19**, ball 30, ball_open 42, **orb2 46** | B4 (v3 20.22-24.20 s): wings to flat (0-4), cupped forward round the chest core (wrap 5-16), snap open (18) and orb 1 (19), the ball: the wings wrapped round her curled body with the crescents tucked (30-42), open (43-44), orb 2 from her side with a twist (46), recovery. |
| `release` | 18 | 96 | idle_h | fold 0, swoop 5, climb 9, whirl 18, cup 31, flash 35, glint 37 (= xglint), rings 38 (= cage), wrap 44, snap 52, **detonation 53**, hover 63, shrink 87, flat 87, shatter 91, revert 92, land 96 | B5 (v3 32.83-38.28 s, v4 replay): wings closed up (fold), the dart swoop (5-8), climb (9-15), two cartwheels with the wings flung and flicking (18-30), cup (31), flash/X glint/ring cage (35-43), the pod wrap while she sinks (44-51), snap open (52), the detonation flung wide with the ribbons streaming (53), hover +2.2 b with slow beats (63-87), the wings shrink and go flat lime (87-90), shatter (91), human form (92) drops and lands (96). |
| `revert` | 19 | 43 | idle_h | shrink 30, flat 32, shatter 36, revert 37, land 43 | Butterfly → human without the blast (S3 §D): rising hover with slow flaps, shrink (30), flat (32), shatter (36), human (37), landing (43). Not used by the core. |
| `death` | 20 | 100 | hold | stagger 0, **shatter 10**, **kneel 30**, **dissolve 50**, gone 100 (spec S4) | From either form: staggers back while the wings go flat lime and shrink away with the 10 t blend (shatter 10), staggers forward, the knees buckle (20), sinks to one knee (30), the crescents and flakes fade (30-64), then scales out about her hips while rising 0.6 b (50-100). Call `kill` after 100. |
| `chain_reform` | 21 | 18 | idle_h | stack 6 | The four crescent plates fly in from around her and stack into a vertical chain at her left (stack 6: the thud), a small flourish, then they take their idle places. |

### 6.1 Wing poses

The clips mix a small library of wing poses (`butterfly_clips.mjs` W_*; her left side, the right mirrors). Each
pose and every frame between them was checked against the other wing set and the body with the textures' alpha
(`gap` = the closest approach of the two wing sets):

| pose | used in | gap |
|---|---|---|
| `W_REST` spread hover; `W_UP` / `W_DOWN` flap extremes | idle, flutters | 1.47 b; ≈ 0.8 b |
| `W_V` raised V, faces to the front, tips 7 b up | big flaps (transform, B1, B3, B5) | 0.60 b |
| `W_CLOSED` closed up above her head (crest leans back, crescents tucked in front) | B3 rise, B5 fold | 0.43 b |
| `W_SNAP` snap downstroke (the hindwing stays under the forewing) | big flaps | |
| `W_FLAT`, `W_GLIDE` swept back | B1 bank, glides | 0.62 b |
| `W_CUP` cupped forward round the chest | B4 wrap, B5 cup | 0.62 b |
| `W_POD` wrapped round her: forewing hooks over her head, hindwing blades under her | B4 ball, B5 wrap | 0.16 b |
| `W_FOLD` folded panels behind the shoulders at 0.4 scale | transform | |
| `W_FLUNG` flung wide, ribbons out | B4 open, B5 detonation | 1.7 b |
| `W_DART` swept back over her back | B3 dive, B5 swoop | 0.65 b |
| `W_SLAM` forward and down | B3 slam | |

Flat cards hinged beside the spine cannot close a shell in front of her without cutting through each other or the
mane, so the pod and the ball frame her from both sides, above and below with the front open (as v4 f420/f440 from
the front). The closed shell of the footage is the `prop/pod` (r 1.4 b): if the module shows it, summon it at the
core anchor at `ball` / `wrap` and clear it at `ball_open` / `snap`; the wrapped wings sit inside its silhouette
from the side and frame it from the front.

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

The generator refuses to write a rig that fails these (`--allow-steps` turns them into warnings):

- **Rotation per tick and per key:** no part turns more than 120° between two ticks or within one interpolation
  segment (blend-ins included). Large one-tick steps are also solved at the half tick (warning when the client's
  slerp leaves the authored path by more than 35°). The clips build with no warning.
- **Alignment:** no horizontal root travel in any key (root x = z = 0), no visible hoof below the floor (2 cm), no
  wing tip under the floor, every event inside its clip.
- **Keys:** the first key at tick 0, the last at the clip length, `next` must name a clip.
- **Parts** ≤ 34; **item models** within −16..32 (element rotations are single-axis multiples of 22.5° by
  construction).
- **Atlas:** ≤ 2 M px in all (now 72 sprites, 1.33 M px), every side a multiple of 16, ≤ 512 px wide and
  ≤ 1024 px tall (the 8-frame strips).
- Compiled: 22 clips, 835 key files and 14 284 part keys. A part gets a key only where the client's lerp/slerp
  would drift from the authored pose by more than 0.012 b, 0.5-3° (per part) or 1.5 % scale.
- Wing contacts are checked offline (not in the build: they need the textures' alpha): every tick of the butterfly
  clips is clean of left-right wing crossings, wing-body crossings beyond 0.45 b from the wing roots, wing-appendage
  crossings (fans, crest, crescents, tendrils) and fore/hindwing crossings beyond 0.7 b from the roots.

## 9. The model

- Height 2.8 b from hoof to helm (BH), single superset rig for both forms; right-side models are mirrored copies of
  the left (no negative scales). Coordinates: +X her left, +Y up, −Z her front (the item models face −Z, the display
  transformations mirror Z).
- Textures are painted procedurally in `butterfly_paint.mjs` from the `model.md` palettes: signed-distance shapes,
  bevelled height fields lit from the upper left, tone ramps, groove/ridge reliefs, fur clumps (`furPainter`) for the
  mane and boots. The membranes are marbled white-mint → lime with the violet trailing rim; the hindwing blade tips
  and the eyes are brightness 15.
- The round parts (torso, pelvis, thighs, fur-boot cores, hooves, helmet dome, mane core, the cocoon, the pod and the
  orb) are smooth turned solids (`butterfly_geometry.mjs` smooth3): 16-facet elliptic rings whose radius steps are
  small, each ring reaching into its wider neighbour instead of closing on a ledge disc, under wrap textures that
  carry the light (front-lit, lilac-shaded backs), so no section seams show. The profiles are `BODY` / `PROPS` in
  `butterfly_paint.mjs`; the boots' fur cards are painted on the same profiles.
- Legs are digitigrade (hip, knee, hock, hoof, a slight A-stance) with an FK chain per side; the crescent hands
  float on paths relative to the torso; the two wing sets pivot on the upper back beside the spine and the ribbon
  tendrils hang beside the chest (torso frame).

## 10. Not in the rig (module / fx code)

- Particles, tinted fx cards (crescent slashes, star flares, sphere bursts, the X glint, the ring cage), decals and
  hazards; screen effects; sounds (vanilla only).
- Moving the props (orb flight, the pod, the cocoon burst).
