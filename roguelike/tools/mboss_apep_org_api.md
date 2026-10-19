# Apep phase-2 objects: API (AP-ORG1)

The six 증식 생명체 organisms, the Heart of the Oasis, the 소생의 찬가 domes, the 둥지 wall blades, the 생명의 손 stalks
and the death seed of 아펩의 오아시스 파수꾼 (plan §5, §7.6; `ap_contract.md` §0.3 / §0.5). Everything here is generated;
edit the generator, never the outputs.

## 1. Files and build

| file | role |
|---|---|
| `tools/build_mboss_apep_org.mjs` | the generator: paints the sprites, writes models / item definitions, compiles the clips into key functions, writes `AP:om/**` and the manifest |
| `tools/apep_org_geometry.mjs` | models (authored in blocks with `mboss_shape_lib` / `mboss_model_lib`) and the structure table `ORG` (owners → displays, joints, scales, looks, tinted items) |
| `tools/apep_org_paint.mjs` | palettes, the shared 2D shapes `SH`, every sprite painter, tile / wrap registrations |
| `tools/apep_org_clips.mjs` | the clip tables (frozen names, lengths, loop / next, events: `ap_contract.md` §0.5.5), the Heart's hang heights and spawn states |
| `tools/mboss_apep_org_manifest.json` | the org manifest (validates against `S:ap/spec/org_manifest.schema.json`; `validate.py --against` the day-0 stub) |
| `data/rlk/function/mboss/apep/om/**` | the runtime (1673 files) |
| RP `assets/rlk/{models/item,items,textures}/mboss/apep_om/` | 43 models, 51 item definitions, 81 sprites (0.117 M px) |

```
node tools/build_mboss_apep_org.mjs --resourcepack <unpacked RP> [--datapack <pack>] [--no-paint] [--debug-dp <dir>] [--dump <frames.json>]
```

`--debug-dp` writes `rlk:om_dbg/<owner>/<clip>/<t>` (every display posed at tick t), `.../rest/<display>/<look>` and
`.../heart/state/<state>` for the renderer; `--dump` writes every display's transform per tick (the test's reference).
The build checks element bounds (-16..32), sprite references, two-sided cards, untinted faces on tinted looks, per-tick
rotation steps (< 100° outside look cuts), budgets, and the total px (≤ 200 000). Idempotent (two builds, no diff).

## 2. Organisms: the runtime

An organism is the framework's aux husk (`aux/spawn`) with the model displays riding it as passengers (`ride_y` 2.0: the
husk's passenger point). Every model passenger carries `rlk_room rlk_mb_aux rlk_ap_om rlk_ap_om_<display>`, culling
off (width / height 0). The husk holds the clip state: `apK` (kind id), `apOI` (clip id), `apOC` (the tick applied at
the next `tick` call). All functions run **as the husk**.

| function | does |
|---|---|
| `om/init` | creates `apK apS apT apOC apOI` (idempotent) |
| `om/<kind>/spawn` | summons the kind's displays on the husk (`~ ~2 ~`), mounts them, turns them to the husk yaw, sets `apK` and starts the spawn clip (`spawn.clips`; the first 4 t are the 0.85 → 1 scale-in) |
| `om/tick` | the per-tick step of any organism (dispatch on `apK`, ≤ 3 checks) = `om/<kind>/tick` |
| `om/<kind>/play/<clip>` | play `<clip>` from tick 0 at the next tick (interpolated from the current pose) |
| `om/<kind>/start/<clip>` | apply tick 0 now (no blend) and continue from tick 1 |
| `om/<kind>/look/<display>/<look>` | swap a display's model (item_model) now |
| `om/face` | turn every model passenger to the husk's yaw (a `tp` would dismount them); call after turning the husk |
| `om/<kind>/bars` | FN-29 fallback: move the `rlk_hb_*` HP-bar passengers to `hp_bar_y` |
| `om/basic/shield/on\|off`, `om/nurt/ring/on\|off` | the 수호 shield overlay on a 기본 / the immune cylinder round a 양육 |
| `om/pred/form/<fish\|bud\|pod\|face>` | the 포식성 body look plus the jaw / fin visibility of that form, without a clip |
| `om/<kind>/kill`, `om/kill` | remove the model passengers (the husk stays) |

Loops wrap; a clip with `next` hands over to it (`next`'s tick 0 is fitted from the held pose); others hold their last
pose (`apOC` stops at len + 1). Look changes inside a clip cut the interpolation (the new model appears in place).
Variants: a clip's look switch keeps a 기본's variant (`bag` keeps `buffed` → `bag_buffed`; `dying` keeps the bag form).

### 2.1 Clip tables

**basic** (기본, `apK` 1; displays: `bulb` (bell/bag/buffed/bag_buffed/dying/bag_dying), `crown` (closed/open), `shield` (on); 308 el, 12032 px)

| id | clip | t | then | events | note |
|---|---|---|---|---|---|
| 0 | `org_spawn` | 20 | basic_bob | - | emergence pop 0.85 -> 1.06 -> 1 (the spawn scale-in) |
| 1 | `basic_bob` | 24 | loop | - | two hop-slides: squash 0.92 / stretch 1.1, up 0.15 |
| 2 | `basic_melee` | 14 | basic_bob | hit 10 | lean back 0-5, bump 0.4 forward, hit 10, settle |
| 3 | `basic_lie` | 10 | hold | bag 10 | bell -> bag: tips forward 0-9, the bag model at 10 (cut), crown out |
| 4 | `basic_ranged` | 20 | hold | open 0, fire 12 | bag: squash 0-3, crown glow 3, petals open 5-12, launch 12, recoil, close 14-20 |
| 5 | `org_die` | 10 | hold | gone 10 | dying look (the bag keeps its form), squash, shrink to nothing |

**nurt** (양육, `apK` 2; displays: `stalk` (idle), `cap` (idle/tilt), `orb` (on), `ring` (on); 84 el, 12800 px)

| id | clip | t | then | events | note |
|---|---|---|---|---|---|
| 6 | `nurt_idle` | 40 | loop | - | stalk sway, the hood nods with a lag, the orb breathes |
| 7 | `nurt_buff` | 20 | nurt_idle | tilt 0, tethers 8 | the hood tilts toward the targets 0-8 and opens (tilt), the orb flares at 8 |
| 8 | `nurt_die` | 17 | hold | gone 17 | the orb bursts, the ring goes, the stalk droops and the hood falls, shrink to nothing |

**guard** (수호, `apK` 3; displays: `spire` (spire/bud/wisp), `orb` (on); 296 el, 15104 px)

| id | clip | t | then | events | note |
|---|---|---|---|---|---|
| 9 | `guard_idle` | 60 | loop | - | the orb bobs and turns; the spire sways a little |
| 10 | `guard_cast` | 30 | guard_idle | collapse 0, bud 7, regrow 16, regrow_end 24, shields 30 | collapse 0-7, bud 7-16 (glowing slit), regrow 16-24, the orb flares at the shields |
| 11 | `guard_die` | 17 | hold | gone 17 | shudder, the black wisp at 3 (red embers: kit), fades up |

**nest** (둥지, `apK` 4; displays: `cap` (idle), `wing_l` (idle), `wing_r` (idle); 342 el, 9216 px)

| id | clip | t | then | events | note |
|---|---|---|---|---|---|
| 12 | `nest_fly` | 14 | loop | - | wings flap V (up 28) <-> wide arch (down 14), the body bobs |
| 13 | `nest_cast` | 12 | nest_fly | walls 12 | the wings curl up into a vertical loop round the orb, the body rises |
| 14 | `nest_blink` | 6 | nest_fly | out 0, in 3 | out 0-2 (the module moves the husk at 3), back in 3-6 |
| 15 | `org_die` | 12 | hold | gone 12 | the wings droop, it falls to the ground and shrinks |

**destr** (파괴, `apK` 5; displays: `shell` (normal/husk), `face` (on); 410 el, 4608 px)

| id | clip | t | then | events | note |
|---|---|---|---|---|---|
| 16 | `destr_roll` | 32 | loop | - | rolls on its side (face to the left), one turn per 32 t |
| 17 | `destr_fuse` | 56 | destr_suck | pulse_1 0, pulse_2 9, pulse_3 18, pulse_4 27, pulse_5 36, fast 36 | upright, face to the Heart; pulses every 9 t, every 4 t from 36 |
| 18 | `destr_suck` | 5 | destr_blast | - | shrinks white-hot |
| 19 | `destr_blast` | 1 | hold | blast 1 | flash; the split husk at 1 (the module then plays org_die) |
| 20 | `org_die` | 10 | hold | gone 10 | the blackened split husk tumbles back to the ground and fades |

**pred** (포식성, `apK` 6; displays: `body` (fish/fish_flare/bud/pod/face), `jaw` (idle), `fin` (idle), `core` (on); 478 el, 16640 px)

| id | clip | t | then | events | note |
|---|---|---|---|---|---|
| 21 | `pred_swim` | 16 | loop | - | tail fin yaw +-25, body +-8 with a 3 t lag, a slow bob |
| 22 | `pred_swallow` | 24 | pred_bud | eat 12, bud 14 | rears 0-6, scoops 6-12 (eat), closes into the bud at 14 |
| 23 | `pred_bud` | 20 | loop | - | spins 45 degrees per loop (8-fold), bobs over the gold swirl; the core pulses |
| 24 | `pred_inflate` | 10 | pred_burst | - | the pod grows from the ground (its own model) over 8 t |
| 25 | `pred_burst` | 10 | pred_swim | hit 0, fish 2 | the pod bursts (hit 0), the fish again at 2 |
| 26 | `pred_bite` | 6 | pred_swim | open 0, hit 4 | jaw open 0-3 with the spikes flared, snap 4 (the module lunges the husk) |
| 27 | `pred_bite_chain` | 38 | pred_swim | hit_1 4, hit_2 10, hit_3 16, hit_4 22 | 4 snaps 6 t apart (the module starts it 8 t before the first sector strike) |
| 28 | `org_die` | 12 | hold | gone 12 | the core flashes out, the fish sinks to the ground nose first and shrinks |

**heart** (single; displays: `heart_bulb` (idle/egg_gold/egg_green/withered/blaze), `heart_cradle` (pedestal/full), `heart_arms` (idle), `heart_tips` (idle), `vine_hand` (idle/wrap), `vine_stem_0` (idle), `vine_stem_1` (idle), `vine_stem_2` (idle), `vine_stem_3` (idle); 773 el, 18176 px)

| id | clip | t | then | events | note |
|---|---|---|---|---|---|
| 29 | `heart_hang` | 80 | loop | - | the egg hangs in the canopy (hang canopy_y), swaying [heart_bulb, vine_hand, vine_stem_0, vine_stem_1, vine_stem_2, vine_stem_3] |
| 30 | `heart_up` | 30 | heart_hang | - | drawn up from the entrance height (9 b) into the canopy [heart_bulb, vine_hand, vine_stem_0, vine_stem_1, vine_stem_2, vine_stem_3] |
| 31 | `heart_lower` | 50 | hold | - | lowered from the canopy to the lowered height, swaying 1-2 b and calming [heart_bulb, vine_hand, vine_stem_0, vine_stem_1, vine_stem_2, vine_stem_3] |
| 32 | `heart_drop` | 30 | heart_idle | land 6, beam 6, beam_end 16 | released at 0, falls 0-5, lands 6 (pitches to lying, 0.7 -> 1, squash), settles; the hand rises away; the cradle full at 6 [heart_bulb, vine_hand, vine_stem_0, vine_stem_1, vine_stem_2, vine_stem_3, heart_cradle, heart_tips] |
| 33 | `heart_idle` | 40 | loop | - | the bulb breathes 1.00 <-> 1.03, the sprouts sway [heart_bulb, heart_tips] |
| 34 | `heart_hit` | 6 | heart_idle | - | a flinch [heart_bulb, heart_tips] |
| 35 | `heart_gain` | 8 | heart_idle | - | a bright swell [heart_bulb, heart_tips] |
| 36 | `heart_wither` | 30 | hold | - | the withered look at 0, sags and shrinks a little, the sprouts droop [heart_bulb, heart_tips] |
| 37 | `heart_blaze` | 24 | hold | - | blazes (CS 0-24): bright look, swelling pulses [heart_bulb, heart_tips] |
| 38 | `heart_lift` | 46 | hold | - | golden egg lifts out of the cradle (0-30) to hang cs_y, the vine hand comes down 20-40 and wraps at 40 [heart_bulb, vine_hand, vine_stem_0, vine_stem_1, vine_stem_2, vine_stem_3] |
| 39 | `cradle_rise` | 20 | hold | - | the cradle (pedestal look), arms and sprouts rise out of the ground [heart_cradle, heart_arms, heart_tips] |
| 40 | `cradle_sink` | 10 | hold | - | back into the ground [heart_cradle, heart_arms, heart_tips] |

**dome** (fixed_set; displays: `dome_shell` (idle), `dome_decor` (idle); 474 el, 14336 px)

| id | clip | t | then | events | note |
|---|---|---|---|---|---|
| 41 | `dome_rise` | 10 | dome_idle | - | grows up from the footprint, a small overshoot [dome_shell, dome_decor] |
| 42 | `dome_idle` | 40 | loop | - | a faint breath [dome_shell, dome_decor] |
| 43 | `dome_pop` | 6 | hold | - | swells and pops (shards: kit) [dome_shell, dome_decor] |

**wall** (multi; displays: `wall_blade` (idle); 3 el, 5376 px)

| id | clip | t | then | events | note |
|---|---|---|---|---|---|
| 44 | `wall_rise` | 5 | hold | - | shoots up from the ground [wall_blade] |
| 45 | `wall_fade` | 8 | hold | - | shrinks into the ground (motes: kit) [wall_blade] |

**stalk** (fixed_set; displays: `stalk_low` (idle), `stalk_high` (idle), `stalk_tip` (idle); 336 el, 7680 px)

| id | clip | t | then | events | note |
|---|---|---|---|---|---|
| 46 | `leg_rise` | 10 | hold | - | bursts up from below the floor, leaning back from the lock, the upper segments whip [stalk_low, stalk_high, stalk_tip] |
| 47 | `leg_slam` | 6 | hold | hit 4 | slams forward onto the ground toward the lock (hit 4), a bounce [stalk_low, stalk_high, stalk_tip] |
| 48 | `leg_sink` | 10 | hold | - | sinks back through the floor [stalk_low, stalk_high, stalk_tip] |


### 2.2 Model notes (vs model_p3 sheet 07)

| kind | model |
|---|---|
| 기본 | bell 1.15 b (1.35 with the curled stem): an egg-shaped 8-facet dome (faint diamond facets painted in), a flared skirt cut into 8 rounded feet. Bag: a level pear (belly behind, neck forward) that the bag clips pitch 20° up (`BAG_POSE`), drawstring ring, crown of jagged petals (closed / open with the lime glow). Looks are tints of two grey-value models: bell / buffed / dying, bag / bag_buffed / bag_dying |
| 양육 | 2.4 b: two dark-teal leaf ribbons with pale rims twisting round each other in an S (a panel per segment, the azimuth stepping 22.5°), broad basal leaves, pale fronds on the ground, a gold shard; the cream hood leaf bent over the top like a drooping tulip (strips along an arc + curled cheeks; `tilt` = lifted open); the orb in the curl; the translucent ring r 1.3 h 0.5 |
| 수호 | spire 4.4 b: two pale ribbons in a double helix converging to points, out of a teal lobed sheath with the gold gem; bud ≈ 2 b: a teal pointed hood over a pale drape flaring to a wavy hem; wisp (death); the orb bobbing above |
| 둥지 | the dark-teal pointed cap with the orb eye in its pale ring, two broad arched pale wings with leafy ends (child displays: flaps, the wall-casting loop) |
| 파괴 | Ø 1.2 armoured ball (10 latitude bands, grey-green plates with pale seams, 13 cone spikes), the open front with the glowing face disc and a short beak; `husk` = the blackened split shell |
| 포식성 | fish 2.5 b: a leaf-shaped cream hood with wavy grey stripes (pointed snout, keel ridge), 2 + 1 grey horns, cyan-rimmed eyes, the translucent green bowl jaw with sepals and the long front fin + gem, the tail fin, the glowing core; `fish_flare` adds 14 flared spikes; bud (a cream ogive over a green star bowl), pod (3.5 b double-lobed clam), face (the closed round face) are their own models |

## 3. Objects

Objects are fixed displays (no husk). Every display holds its own `apOI` / `apOC` (`apOI` -1 = stopped); the object's
`tick` runs every display with a running clip. `om/objects_tick` steps them all (any executor, once per tick while any
exists). Fixed displays use the block UUIDs `524c4b4d-4150-4800-8000-0000000000NN` (`[I;1380731725,1095780352,-2147483648,NN]`).

| object | displays (UUID NN) | functions |
|---|---|---|
| Heart (`single`) | marker `rlk_mb_ap_heart` (centre); `heart_bulb` 00, `heart_cradle` 01, `heart_arms` 02, `heart_tips` 03, `vine_hand` 04, `vine_stem_0..3` 05-08 | `om/heart/spawn/<entrance\|canopy\|play>` (kills any old Heart first), `om/heart/play/<clip>`, `om/heart/look/<display>/<look>`, `om/heart/tick`, `om/heart/kill` |
| domes (`fixed_set` 3) | `dome_shell` 10 / 12 / 14, `dome_decor` 11 / 13 / 15 | `om/dome/spawn {i:0..2}` at the dome spot (plays `dome_rise`), `om/dome/play {i, clip}`, `om/dome/i<k>/kill`, `om/dome/kill_all` |
| walls (`multi`, ≤ 15) | `wall_blade` (no UUID) | `om/wall/spawn` one blade at the execution point (tag `rlk_ap_om_new` until the next spawn: tag it into its group), `om/wall/play/<clip>` as the blade, `om/wall/kill_all` |
| stalks (`fixed_set` 4) | `stalk_low` 20+3k, `stalk_high` 21+3k, `stalk_tip` 22+3k | `om/stalk/spawn {i:0..3}`, `om/stalk/play {i, clip}`, `om/stalk/kill_all` |
| seed (`single`) | `seed` 30 | `om/seed/spawn`, `om/seed/kill` |

`om/kill_all` removes every object display, the Heart marker and every organism model.

Markers owned by the callers (`ap_contract.md` §0.3): the dome marker `rlk_mb_ap_dome` + `rlk_mb_hzsafe` (`mbHzSG` = the
cast's group, FN-14) and the wall group marker `rlk_mb_ap_wall` (its barrier blocks) are summoned by the casting module;
`om/dome/spawn` / `om/wall/spawn` dress them. Summon the dome marker and the displays at the floor point (y 201): the
kit's `p/flood` skips cells by the marker's 3D distance (`requests/fx.md` RFX-3).

### 3.1 The Heart

States (`om/heart/spawn/<state>`): `entrance` (the upright egg held by the vine hand at the entrance height, the cradle
under the floor), `canopy` (hanging in the canopy, phase 1), `play` (lying in the full cradle, phase 2). Hang heights are
the egg's lowest point above the floor: entrance 9, canopy 20, lowered 3, cut-scene 10. The bulb is one grey-value model
tinted per look: `idle` (lemon), `egg_gold`, `egg_green`, `withered` (brightness 10), `blaze`; the arrival egg is the
same model at pose scale 0.7, pitched upright. The cradle (`pedestal` = the empty cradle with pale petal clumps and gold
sprouts; `full`), the two tall root arms curling over the bulb (≈ 4.3 b) plus two side roots, and the glow tips on their
ends are knobbly root tubes (boxes along smoothed polylines, single-axis 22.5° steps). The vine hand's six vine fingers
hug the egg (`wrap` = tighter, further down); four stem segments stretch from the canopy anchor to the wrist.

Footprint (manifest `objects.heart.footprint`): bulb box 3.2 × 2.6 × 2.3 (centre y 1.6), root radius 2.5, sockets at
bearings 0 / 120 / 240 r 3.4, wait ring 4.5, 파괴 stops r 2.6 at 60 / 180 / 300, wall exclusion 4.6, swirl r 3.5.

The objects' clip tables are in §2.1 (after the organisms).

## 4. Budgets

Per organism ≤ 500 elements (max over a display's looks, summed over displays), the Heart ≤ 800, all org sprites ≤ 200 000
px (plan §5.4). Current: see the build's table (`basic 308`, `nurt 84`, `guard 296`, `nest 342`, `destr 410`, `pred 478`,
`heart 773`, `dome 474`, `wall 3`, `stalk 336`, `seed 4` elements; 0.117 M px).

## 5. Tests and renders

- `S:ap/orgtests/test_ap_org.py` (mcsim, outside the repo): spawns every kind on a husk, runs the key functions on the
  passengers, rebuilds the client interpolation and compares it with `--dump` frames; looks, variants, overlays, bars,
  forms, Heart states / chains, domes, stalks, walls, seed, kill paths, the manifest (`validate.py --against`), budgets,
  footprint.
- Renders at 3 b and 8 b (player eye 1.62) beside the model_p3 sheet / v3 / v4 frame crops: `S:ap/orgwork/r1/`
  (`tools/r1.py` there).

## 6. Limits

- Lofts are stepped (single-axis 22.5° rotations): round bodies show fine terraces; ledges are painted darker for the
  game's up-face light. Renders use the MC light model; the game's translucency and full-bright (Heart, orbs, glow) are
  approximated.
- `ride_y` 2.0 assumes the husk's passenger point; a framework change there moves every organism model.
- The bag's 20° pitch lives in the clips (`BAG_POSE`); `org_die` of a bag starts from the level rest pose.
