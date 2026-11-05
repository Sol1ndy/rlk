# 홍련 (Scarlet) rig: API (stage S2a)

The display-entity rig of the special boss 홍련 (Scarlet; module `scarlet`, function root `boss/scarlet`) — an original
design of a Joseon wandering swordswoman with a red-lotus motif — and the contract between the rig and its users: the
module (`tools/mboss_scarlet/*`, S3 / S4) and S2b's cinematic clips and sequences. Binding inputs: `S:hr/PLAN.md` §1.5,
§2, §4.3-§4.5, §5.4, §7.3.2; `S:hr/contract.md` §3.2; the frozen table `tools/mboss_scarlet/api.py` §6-§7 (parts, parents,
re-parent table, looks, hands, prop states, anchors, calls, clips). Never edit `api.py` from here: requests go to
`S:hr/requests/`.

## 0. Files

```
node tools/build_scarlet_rig.mjs --resourcepack <unpacked RP> [--datapack <dp>] [--no-paint] [--allow-steps] [--show N]
     [--allow-missing] [--debug-dp <scratch dir> [--debug-clips a,b | all] [--debug-step N]]
```

| file | owns |
|---|---|
| `build_scarlet_rig.mjs` | the build: models / items / sprites / atlas, the two-pass clip solve, the compile (per-part key segments, snaps, floor splits), the gates, the API functions, the anchor table, the manifest, the debug pack |
| `scarlet_geometry.mjs` | the 29 parts (name, default model, brightness, display scale), every item model (blocks, A-frame, `toUnits`), the hand / face / phase / blade model tables, the ghost twins (`<model>_g`), `item_sword` |
| `scarlet_paint.mjs` | the palette (PLAN §2.2, ΔE ≥ 10 from the original's roles: `PAINT_ROLES`), the tile sprites and the unique cards (faces, hair cards, the wedge-masked brim, knot, strings, blade / glows, the 3-region ghost texture) |
| `scarlet_pose.mjs` | the skeleton and `solve(pose, hist, guardMin)`: torso FK, IK legs (boots on the floor), IK arms (the sword lever / sphere grip, free targets, the brim / hilt / throat targets), the blade in its cutting plane, the per-tick re-parenting (hat, scabbard, cup, bottle), the chains (ponytail, locks, strings, sash, four skirt panels) with lag, gravity and floor guards, the root lift, `vis` |
| `scarlet_clips.mjs` | `DEFAULT_POSE` (the stance), the pose families (`ST`, `ST2`, `CROUCH`, `LOW`, `AIR`, `LOCK`, `DOWN`, `H_POSE`), the helpers `K` / `B` / `SW`, the 39 S2a clips, `CINE_PLACEHOLDER` |
| `scarlet_cine.mjs` | **S2b's** (absent until S2b writes it): the 8 cinematic clips (§6) |

Generated (never hand-edit): `data/rlk/function/boss/scarlet/rig/**`, `tools/scarlet_rig_manifest.json`, the RP's
`assets/rlk/{textures,models/item,items}/mboss/scarlet/**` and the items-atlas entries `rlk:mboss/scarlet/*`. The shared
RIGLIB (`mboss_rig_compile`, `mboss_rig_clips`, `mboss_rig_math`, `mboss_model_lib`, `mboss_shape_lib`, `mboss_paint_lib`)
is used unchanged. Two builds are byte-identical.

## 1. Calls (all `rlk:boss/scarlet/rig/…`; @s = the boss = the anchor, at its feet)

| call | what |
|---|---|
| `init` | the `hrRig*` objectives; loads the anchor table into `rlk:hr rig.an` once per table version (`rig.anv`) |
| `spawn` | kills old parts, summons the 29 parts (UUID `524c4b4d-4852-4400-8000-0000000000NN`, NN = part order) and the shadow helper (NN 0x40, radius 0.9), re-applies the stored looks, queues `idle` |
| `spawn_hidden` | `spawn`, then `state/hidden` |
| `tick` | once per game tick: respawns missing parts, the follow (position + yaw, cached: no tp while the anchor stands still), the hit flash, the clip runner |
| `kill` / `uninstall` | removes the parts, the shadow, the `rlk_hr_anchor` marker (`uninstall` also the `rlk_hr_face` scratch marker, the objectives and `rlk:hr rig`) |
| `play/<clip>` | queues the clip: the next `tick` runs its tick 0 (`hrRigT` −1 → 0). Called before `tick` in the same game tick, event e runs e game ticks later |
| `start/<clip>` | applies tick 0 now (`hrRigT` 0) |
| `face/set {yaw}` | macro: `rotate @s $(yaw) 0` |
| `face/player` / `face/track` | turn to the nearest player (at once / ≤ 12° per call) |
| `flash` | hit feedback: every body part glows white-pink 3 ticks |
| `state/hidden` / `state/normal` | every part at scale 0 where it stands (no clip runs, the follow continues) / visible again (the current clip restarts from tick 0); any `play` / `start` also shows the rig |
| `look/<channel>/<value>` | §3 |
| `anchor/<name>` | moves the one `rlk_hr_anchor` marker (`rlk_room rlk_mb_aux rlk_hr_anchor`) to that point of the current clip tick (the held last pose past the end), yaw = the boss's; effects run at / as it |

`hrRig*` objectives: `C` clip id (`api.CLIP_ORDER` index), `T` clip tick (−1 queued), `F` flash, `Y` face scratch, `S` state
(1 hidden), the stored looks `Form Ph Bl Fc HR HL Hat Sw Sc Pr Cu Bo` (indices of `api.LOOKS` / `HANDS` / `PROP_STATES`),
`Q Qx Qy Qz Qw` the follow cache. Nothing else is created; `uninstall` removes them all.

## 2. Entities and the model (PLAN §2.1-§2.4)

Item displays, `billboard:"fixed"`, `view_range:2f`, culling 8 × 8, block brightness 13 (`sword_glow` 15; the ghost form 15;
`sash_tails` 14 in P2), tags `rlk_room rlk_mb_aux rlk_mb_part rlk_hr_part rlk_hr_<part>` (the shadow: no `rlk_mb_part`).
Head top 2.55 b, crown top 2.82, brim Ø 1.60 (four 1.60 b squares at 0 / 22.5 / 45 / −22.5° stacked 0.003 b apart, each
painting only its own corner wedges: no coplanar faces, no stacked translucency; the underside tinted through the item
definition), sword 2.10 b and scabbard 1.82 b (display scale 1.5). Left-handed: the sword in `forearm_l`, the scabbard at
the right hip / in the right hand. Elements at rest 2 304 (ghost 2 304) ≤ 6 500; the atlas 83 712 px (48 sprites) ≤ 0.15 M.

| NN | part | parent | default model | scale | bright |
|---|---|---|---|---|---|
| 00 | `pelvis` | — | `pelvis` | 1 | 13 |
| 01 | `torso` | pelvis | `torso` | 1 | 13 |
| 02 | `head` | torso | `head` | 1 | 13 |
| 03 | `face` | head | `face_calm` | 1 | 13 |
| 04-05 | `hair_tail_1` / `_2` | head / hair_tail_1 | the ponytail (2 segments) | 1 | 13 |
| 06-07 | `lock_r` / `lock_l` | head | the side locks | 1 | 13 |
| 08-0b | `arm_r`, `forearm_r`, `arm_l`, `forearm_l` | torso / arm | `forearm_*_<hand>` | 1 | 13 |
| 0c-0f | `thigh_r`, `shin_r`, `thigh_l`, `shin_l` | pelvis / thigh | the boot is in the shin | 1 | 13 |
| 10-13 | `skirt_fl`, `skirt_fr`, `skirt_bl`, `skirt_br` | pelvis | four faceted panels | 1 | 13 |
| 14 | `sash_tails` | pelvis | `sash_p1` / `sash_p2` | 1 | 13 |
| 15 | `hat` | head (re-parented) | `hat_p1` / `hat_p2` | 1 | 13 |
| 16 | `hat_strings` | hat | `hat_strings` | 1 | 13 |
| 17 | `sword` | forearm_l | `sword` | 1.5 | 13 |
| 18 | `sword_glow` | sword | `empty` / `glow_<colour>` | 1.5 | 15 |
| 19 | `scabbard` | pelvis (re-parented) | `scabbard` | 1.5 | 13 |
| 1a | `hilt_sheathed` | scabbard | `hilt` | 1.5 | 13 |
| 1b | `cup` | forearm_r (re-parented) | `cup` | 1 | 13 |
| 1c | `bottle` | forearm_l (re-parented) | `bottle` | 1 | 13 |

Every model has a ghost twin `<model>_g` (same elements, every face `#ghost` = `rlk:mboss/scarlet/ghost`, no tint).
No runtime parenting: the re-parent table of `api.REPARENT` is solved per clip tick in `scarlet_pose.mjs`.

## 3. Looks (`api.LOOKS`; stored in `hrRig*`, re-applied by `spawn`)

| channel | values | owner | what the call does |
|---|---|---|---|
| `form` | normal / ghost | module | every part → its ghost twin (one flat glowing lilac), brightness 15, `sword_glow` lilac |
| `phase` | p1 / p2 | module | the hat knot (glowing crimson halo) and the sash tails' edge |
| `blade` | off / lilac / pink / violet / gold | module | the glow card over the blade (`sword_glow`) |
| `face` | calm / smile / closed | clips (the call: an override until the next clip keys it) | the face card |
| `hat` | worn / back / hand / world / gone | clips | stores `hrRigHat` and puts the hat at that state's rest transform |
| `sword` | hand / sheathed / gone | clips | the blade in hand / hidden with the hilt seated / hidden |
| `scabbard` | hand / hip / gone | clips | the scabbard in the right hand / at the right hip / hidden |
| `props` | none | clips | hides the intro cup and bottle |

The re-parenting states (hat, sword, scabbard, cup, bottle) and the hands (`api.HANDS` open / grip / brim) and faces are
keyed by the clips themselves (tick 0 and their events), so a clip always shows its own states; the `look/*` calls are for
the module's overrides between clips. All `look/*` are idempotent.

## 4. Anchors (`api.ANCHORS`)

`hand_l` `hand_r` (the grips), `blade_tip`, `blade_mid` (the left hand while the sword is not shown), `scabbard_mouth`,
`hat_crown`, `head`, `chest`: per clip tick from the solver, stored as `rlk:hr rig.an[<clip id>].<anchor>[<tick 0..len+1>] =
"^left ^up ^forward"` (the entry len+1 repeats the last pose). `anchor/<name>` copies the entry for (`hrRigC`, `hrRigT`)
through `anchor/r/get` → `anchor/r/go` (macro tp, local to the boss, yaw only); a missing entry falls back to `^ ^1.8 ^`.

## 5. Clips (`scarlet_clips.mjs`, sampled by `mboss_rig_clips.mjs`)

A clip is `{name, keys: [[tick, sparse pose, ease], …], cuts?, src?, note?, base?, blend?, lines?}`; keys run 0..len (the
contract length; the last key = the end), merged onto `base` (default `DEFAULT_POSE`). Ease of the segment arriving at a key:
`'io'` smooth (default), `'i'` accelerate (strikes, falls), `'o'` decelerate (leaps, settles), `'l'` linear (spins). Numbers
and vectors interpolate; `hat sword scab face hL hR cup bottle` switch at their key (`DISCRETE`). `cuts`: ticks where every
part takes a 1-tick key and a > 60° turn snaps (vanish / reappear). `blend` (default 3): the first segment's minimum length
(the blend from whatever the rig showed). `lines`: `{tick: [commands]}` added to that tick's key file. Root motion never in a
clip (the module moves the anchor). Events are the contract's (`api.CLIPS`); the clip only times its motion to them.

Pose channels (full list in the header of `scarlet_pose.mjs`): `pos rot tor head` (pelvis offset, pelvis / torso / head
eulers [pitch, yaw, roll], pitch + leans back, yaw + turns her to her right), `fL fR kL kR lf` (feet, knees, legs in the
pelvis frame for flips / lying), the blade `cB cR th ed tw` (plane bearing, roll, angle, edge sense, twist) with the grip
`gF gL` (lever from the left shoulder) or `gB gE gD` (the swing sphere), `rh` (right hand on the hilt), `hold`, free arms
`aL aR plL plR plwL plwR pL pR frL frR`, the brim `bwL bwR bzL bzR`, the hilt / throat `hiL hsR scHip`, the chains `hairF
hairS skF skG skIF skIB skW`, `vis`, the sheathe `sh shW`, the hat `hwP hwE hhB hhE hhN`, the scabbard in hand `scB scE scR
scOff`, the props `cupP botP cupT botT`.

Helpers: `K(t, pose, ease)`; `B(cB, cR, th, ed, extra)` a blade on the lever (vertical plane through bearing cB at cR 0, th
0 forward / 90 up; cR ±88 flat: `B(0, -88, th, -1)` has th + toward her right, 90 = right, the edge forward); `SW(b, d, dir,
hb, he, hd)` a flat waist-level blade at bearing b, d° down, its edge leading a sweep toward her left (dir −1) or right (+1),
the hand on the swing sphere. Conventions the S2a clips keep: a cut that sweeps th upward keys `ed 1`, downward `ed -1`;
flips turn about her centre of mass (`flipPos`) with the blade carried by the body (th = th_rel + pitch); a spin continues
the sweep of the cut before it; values stay in the turned range after a flip / spin (−360) — the rotations are the same.

The 39 S2a clips (len / loop / events = `api.CLIPS`; the `src` of each names its footage): locomotion `idle idle2 walk glide
strafe_l strafe_r backstep flinch`; P1 `a1 a2 a3 a4 a6 a9 a10 a7_tell a7_throw`; the gauntlet `g_brim g_tell g_reform g_dash
g_glide g_drop g_run g_ring g_rise g_leap g_sweep g_x g_wrap g_dome g_vert g_dive g_deflect`; the down window `down kipup`;
the event coda `ev_give ev_toast ev_leave`. Poses the other stages start from: `g_deflect` ends in `LOCK` (= `repel` tick 0),
`down` is `DOWN` (= `lead_down` tick 0), `H_POSE` = the last pose of `ending` = tick 0 of `ev_give` / `ev_toast`.

## 6. The cinematic clips (S2b): `tools/scarlet_cine.mjs`

The generator imports `./scarlet_cine.mjs` when the file exists (`await import`), else uses `CINE_PLACEHOLDER` (static poses,
contract lengths). The module's shape:

```js
import {K, B, SW, ST, ST2, CROUCH, LOW, AIR, LOCK, DOWN, H_POSE, DEFAULT_POSE, F_ST, F_WIDE, F_LUNGE, F_LUNGE_R, F_TOG} from './scarlet_clips.mjs';
export const CLIPS = [
  {name: 'intro', keys: [K(0, {...}), …, K(554, {...})], src: '…', cuts: [], lines: {}},
  // … exactly the 8 clips api.CLIP_OWNER gives S2b: intro, intro_end, cs1, sq1, repel, lead_down, lead_stand, ending
];
```

The build fails unless the names are exactly the contract's S2b clips; every clip is checked like the S2a ones (keys 0..len,
increasing, events equal if given, the floor / 120° / cull gates). Keep `ending` ending in `H_POSE`, `repel` starting from
`LOCK`, `lead_down` from `DOWN`; the props (`cup`, `bottle`: none / hand / rock with `cupP botP cupT botT`) and the hat states
are keyed in the clips.

## 7. `item_sword` (`api.ITEM_MODEL` = `rlk:mboss/scarlet/item_sword`)

The rig's own scabbard with the hilt seated, one model, the rig's sprites only (0 extra px). Laid on the diagonal like a
vanilla sword (hilt lower left, tip upper right) with the vanilla handheld transforms: `thirdperson_*` [0, ∓90, ±55] / [0,
4, 0.5] / 0.62, `firstperson_*` [0, ∓90, ±25] / [1.13, 3.2, 1.13] / 0.5, `gui` 0.9, `ground` [90, 0, 0] / [0, 1.5, 0] / 0.55
(flat above the floor), `fixed` [0, 180, 0] / 0.9. Length 2.21 b at display scale 1.5: a thrown-sword `item_display`
(`item_display:"none"`, scale [1.5, 1.5, 1.5]) matches the rig's sword. The scabbard runs along the model's (+X, +Y)
diagonal (elements turned −45° about Z; tip at +X +Y, pommel at −X −Y) and the model's centre (8, 8, 8) sits 0.72 b along it
from the guard, so a flight direction d needs the turn that takes (1, 1, 0)/√2 onto d.

## 8. Build gates and budgets

The builder fails (unless `--allow-steps`) on: any shown model point, blade tip or scabbard tip below the floor at a compiled
tick (the client's interpolation included: a dipping segment is split at its lowest tick), a part turning > 120° in a tick
(a key > 118° is an ambiguous slerp), an element outside −16..32 or with a rotation outside {−45, −22.5, 0, 22.5, 45}, unused
or mis-sized sprites, a ghost model with another texture, the atlas > 0.15 M px, elements at rest > 6 500. Numbers of this
build: 29 parts, 47 clips, 1 078 rig functions (3.4 MB), 78 models, 48 sprites (83 712 px), 2 304 elements at rest (ghost
2 304). The suite `S:hr/tests/test_rig.py` (73 checks; 76 with `--rebuild`, two builds byte-identical) replays the shipped key files.

Debug: `--debug-dp <dir>` writes `hr_dbg/<clip>/<t>` (every part's compiled transform and the hand / face models of that tick)
for the offline renderer (`S:az/understand/rigtech_render.py --spawn rlk:boss/scarlet/rig/spawn --apply rlk:hr_dbg/<clip>/{t}
--strip 0..<len>:2`).
