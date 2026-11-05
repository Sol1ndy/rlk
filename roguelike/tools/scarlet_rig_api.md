# 홍련 (Scarlet) rig: API (stages S2a, S2b; the skin S2c; the player-size body S2d)

The display-entity rig of the special boss 홍련 (Scarlet; module `scarlet`, function root `boss/scarlet`) and the contract
between the rig and its users: the module (`tools/mboss_scarlet/*`, S3 / S4) and S2b's cinematic clips and sequences.
**S2c (11-05, the user's request "마인크래프트 스킨을 이용해서 만들라고. 아를이나 라이덴처럼"):** the body wears the user's own
Minecraft skin (`tools/scarlet_skin.mjs`, 64 × 64 slim (3-px arms) with the outer layers; its pixels as given); what the rig makes
itself — the hat (a white 백립-style gat), its bead strings, the sash tails, the sword, the scabbard, the hilt, the cup, the
bottle, `item_sword` — keeps S2a's shapes in colours matched to the skin.
**S2d (11-05, the user's request "팔다리가 너무 기괴하게 긴데 그냥 플레이어 크기랑 똑같게해"):** the body is exactly this pack's
player avatar (`tools/build_player_rig.mjs`: its boxes, skin faces, proportions and joints, 1 skin px = 1/16 b, display scale
1; head top 2.00 b) wearing the same skin unchanged; the props are resized to it; the 47 clips (S2a's and S2b's source motion)
are **retargeted** to the avatar's skeleton at build time (`tools/scarlet_retarget.mjs`, §9). Parts, anchors, looks, calls,
clip names / lengths / events are unchanged. Binding inputs: `S:hr/s2d/design.md`; `S:hr/PLAN.md` §1.5,
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
| `scarlet_skin.mjs` | S2c: the user's skin, embedded (base64, bytes, sha1; generated once from the user's PNG — do not edit); the builder writes it unchanged as `textures/mboss/scarlet/skin.png` (`rlk:mboss/scarlet/skin`) |
| `scarlet_geometry.mjs` | the 29 parts (name, default model, brightness, display scale), every item model (blocks, A-frame, `toUnits`): S2d the avatar's body boxes (`BODY_SPECS`, `bodyModels`, `SKIN_MAP`: the avatar's two boxes per model, the torso / pelvis split at body row 9), the face overlays (`FACE_FX`), the hidden parts (`HIDDEN`: the hair slabs, locks, skirt panels), the props at the new sizes (`HAT`, `STRINGS`, `SASH`, `SWORD`, `SCAB`, `CUP`, `BOTTLE`, `ITEM_SWORD`, `MODEL_SCALE`); the hand / face / phase / blade model tables, the ghost twins (`<model>_g`), `item_sword` |
| `scarlet_paint.mjs` | the props' palette (matched to the skin; the hat and the gold keep ΔE ≥ 10 from the original's roles: `PAINT_ROLES`, the body roles `'skin'`), the tile sprites and the unique cards (the wedge-masked brim, knot, strings, sash tails, blade / glows, `face_fx`, the 3-region ghost texture); the skin is never painted here |
| `scarlet_pose.mjs` | S2d: the avatar's skeleton `SK` (§9.1) and `solve(pose, hist, plan, ctx)` on the retargeted pose: the root contacts (seat, lying rest with the incline / chin tip / rock grid, kneel), IK legs clamped to the reach (no stretch; the boot loop, the planted-feet drop), the hip scabbard (two-axis floor guard, closeY), the hand targets (stone, brim, hilt, throat, lips, the hat hand-overs), IK arms (the turn / fold rate limits), the prop closure, the reach assists, the blade-body guard (push, turn), `groundSword`, the hat states with their hand-over blends and the flying hat's clearance, the strings / sash / cup / bottle, the support pass (S2a's contact truth), the anchors and the per-tick extras (`_guard`, `_contacts`, `_support`, `_lift`) |
| `scarlet_retarget.mjs` | S2d: the retarget of a source sample (factors, the channel table, the derived weights `wLie` `wSeat`), the declared `PATCHES`, `overlay` (patches, the hat hand-overs, the re-anchored world-hat flights), the world-hat spots, `refCore` (S2a's own contact truth), `hipDirChannels`, `bladeChannels`, `faceSpot`; CLI `--dump <clip|all>` (the source and retargeted angle channels per tick) |
| `scarlet_clips.mjs` | `DEFAULT_POSE` (the stance), the pose families (`ST`, `ST2`, `CROUCH`, `LOW`, `AIR`, `LOCK`, `DOWN`, `H_POSE`), the helpers `K` / `B` / `SW`, the 39 S2a clips, `CINE_PLACEHOLDER` |
| `scarlet_cine.mjs` | **S2b's** (absent until S2b writes it): the 8 cinematic clips (§6); S2d: `HIP_DIR = hipDirChannels()` (the hip ↔ hand hand-over key from the skeleton) |

Generated (never hand-edit): `data/rlk/function/boss/scarlet/rig/**`, `tools/scarlet_rig_manifest.json`, the RP's
`assets/rlk/{textures,models/item,items}/mboss/scarlet/**` and the items-atlas entries `rlk:mboss/scarlet/*`. The shared
RIGLIB (`mboss_rig_compile`, `mboss_rig_clips`, `mboss_rig_math`, `mboss_model_lib`, `mboss_shape_lib`, `mboss_paint_lib`)
is used unchanged. Two builds are byte-identical.

## 1. Calls (all `rlk:boss/scarlet/rig/…`; @s = the boss = the anchor, at its feet)

| call | what |
|---|---|
| `init` | the `hrRig*` objectives; loads the anchor table into `rlk:hr rig.an` once per table version (`rig.anv`) |
| `spawn` | kills old parts, summons the 29 parts (UUID `524c4b4d-4852-4400-8000-0000000000NN`, NN = part order) and the shadow helper (NN 0x40, radius 0.6 = `api.SHADOW_R`), re-applies the stored looks, queues `idle` |
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
S2d: head top 2.00 b (`api.HEIGHT`; the idle-t0 head 1.98), crown top 2.30 (`api.HAT_TOP`), brim Ø 1.32 (`api.BRIM_D`: four 1.32 b
squares at 0 / 22.5 / 45 / −22.5° stacked 0.003 b apart, each painting only its own corner wedges inside the ring of radius
0.66: no coplanar faces, no stacked translucency; the underside tinted through the item definition), crown Ø 0.50 × 0.30
(a 16-facet drum; its top the same 16-gon: an annulus of 16 quads over a centre square, S2d round 2);
worn, the hat sits level on the head: the brim 0.502 above the neck (`SK.brim`, `SK.brimTilt` 0), the crown's bottom 0.013 over
the head's top,
sword 1.94 b (`api.SWORD_LEN`: the blade tip 1.60 from the grip centre, the pommel −0.34) and scabbard 1.52 b
(`api.SCABBARD_LEN`; both at display scale 1.5). Left-handed: the sword in `forearm_l`, the scabbard at the right hip / in
the right hand. Elements at rest 224 (ghost 224) ≤ 6 500; 62 models; the atlas 47 872 px (27 painted sprites + the 4 096-px
skin) ≤ 0.15 M. The boss entity: husk `scale 1.0`, click shield `hit {w 1.2, h 2.4}` (the idle-loop hull top 2.33 incl. the hat).

**The body (S2d): the player avatar's.** One skin pixel is 1/16 b in every direction, exactly as `build_player_rig.mjs`'s
avatar: the head 8 × 8 × 8 px (0.5 b), the body 8 × 12 × 4 split at body row 9 into the torso (rows 0-9, pivot at the seam)
and the pelvis (rows 9-12, pivot at the hip line), the avatar's slim 3-px arms (the user's skin is slim; upper arm rows 0-6,
forearm with the hand 6-12; `arlecchino_geometry.mjs` P1_SPECS = `build_player_rig.mjs`'s specs, S2d round 2) and legs
(thigh 0-6, shin 6-12), each model two boxes: the base layer and the outer
layer (0.5 px on the head, 0.25 px elsewhere, inflated on all six sides). The 15 body models equal the avatar's elements
exactly (`test_rig.py` `body`); `skin.map` in the manifest lists every model's region and rows. Hidden (model `empty`, one
fixed scale-0 transform keyed at a clip's tick 0): `hair_tail_1` `hair_tail_2` (the skin's own back hair reads as the
player model's), `lock_r` `lock_l`, `skirt_fl` `skirt_fr` `skirt_bl` `skirt_br`. The hands are the arm's lower end (the three
hand models are one box). Faces: `calm` shows the skin's own face (no overlay), `smile` narrows the eyes and adds a thin mouth,
`closed` lays eyelids over both eyes (`face_fx`, 0.003 b in front of the face).

| NN | part | parent | default model | scale | bright |
|---|---|---|---|---|---|
| 00 | `pelvis` | — | `pelvis` | 1 | 13 |
| 01 | `torso` | pelvis | `torso` | 1 | 13 |
| 02 | `head` | torso | `head` | 1 | 13 |
| 03 | `face` | head | `face_calm` | 1 | 13 |
| 04-05 | `hair_tail_1` / `_2` | head / hair_tail_1 | `empty` (hidden: S2d, the skin's back hair) | 1 | 13 |
| 06-07 | `lock_r` / `lock_l` | head | `empty` (hidden: in the skin) | 1 | 13 |
| 08-0b | `arm_r`, `forearm_r`, `arm_l`, `forearm_l` | torso / arm | `forearm_*_<hand>` | 1 | 13 |
| 0c-0f | `thigh_r`, `shin_r`, `thigh_l`, `shin_l` | pelvis / thigh | the boot is in the shin | 1 | 13 |
| 10-13 | `skirt_fl`, `skirt_fr`, `skirt_bl`, `skirt_br` | pelvis | `empty` (hidden: the skin's legs show) | 1 | 13 |
| 14 | `sash_tails` | pelvis | `sash_p1` / `sash_p2` | 1 | 13 |
| 15 | `hat` | head (re-parented) | `hat_p1` / `hat_p2` | 1 | 13 |
| 16 | `hat_strings` | hat | `hat_strings` | 1 | 13 |
| 17 | `sword` | forearm_l | `sword` | 1.5 | 13 |
| 18 | `sword_glow` | sword | `empty` / `glow_<colour>` | 1.5 | 15 |
| 19 | `scabbard` | pelvis (re-parented) | `scabbard` | 1.5 | 13 |
| 1a | `hilt_sheathed` | scabbard | `hilt` | 1.5 | 13 |
| 1b | `cup` | forearm_r (re-parented) | `cup` | 1 | 13 |
| 1c | `bottle` | forearm_l (re-parented) | `bottle` | 1 | 13 |

Every model has a ghost twin `<model>_g` (same elements, every face `#ghost` = `rlk:mboss/scarlet/ghost`, no tint; a skin face
shows the whole ghost gradient, so every box of the ghost body glows alike).
No runtime parenting: the re-parent table of `api.REPARENT` is solved per clip tick in `scarlet_pose.mjs`.

## 3. Looks (`api.LOOKS`; stored in `hrRig*`, re-applied by `spawn`)

| channel | values | owner | what the call does |
|---|---|---|---|
| `form` | normal / ghost | module | every part → its ghost twin (one flat glowing lilac), brightness 15, `sword_glow` lilac |
| `phase` | p1 / p2 | module | the hat knot (glowing crimson halo) and the sash tails' edge |
| `blade` | off / lilac / pink / violet / gold | module | the glow card over the blade (`sword_glow`) |
| `face` | calm / smile / closed | clips (the call: an override until the next clip keys it) | the face overlay (calm: none, the skin's face) |
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
clip (the module moves the anchor). Events are the contract's (`api.CLIPS`); the clip only times its motion to them. S2d: the
clips stay in S2a's units (the source motion: feet, planted hands, grip distances for S2a's 2.55-b figure); the builder
retargets every sample onto the avatar's skeleton (§9.2) before it solves.

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
(flat above the floor), `fixed` [0, 180, 0] / 0.9. S2d: length 2.03 b at display scale 1.375 (`api.ITEM_SWORD_LEN`,
`api.ITEM_SWORD_SCALE`; 23.62 model units, within 1 % of S2c's 23.57, so the handheld transforms still frame it): a
thrown-sword `item_display` (`item_display:"none"`, scale [1.375, 1.375, 1.375]) matches the rig's scabbard with the hilt.
The scabbard runs along the model's (+X, +Y) diagonal (elements turned −45° about Z; tip at +X +Y, pommel at −X −Y), so a
flight direction d needs the turn that takes (1, 1, 0)/√2 onto d. The manifest's `item_sword.toss_offset` = the item's
centre from the right grip at the toss (ev_give 29, the last tick the scabbard is in her hand; ^left ^up ^forward): seq.py
summons the thrown sword there.

## 8. Build gates and budgets

The builder fails (unless `--allow-steps`) on: any shown model point, blade tip or scabbard tip below the floor at a compiled
tick (the client's interpolation included: a dipping segment is split at its lowest tick), a part turning > 120° in a tick
(a key > 118° is an ambiguous slerp), the blade more than 1 cm inside her torso / pelvis / head / upper arms / thighs / shins
at a clip event (as shipped; the hands hold the hilt and the scabbard by design), an element outside −16..32 or with a
rotation outside {−45, −22.5, 0, 22.5, 45}, unused or mis-sized sprites, a damaged embedded skin, a ghost model with another
texture, the atlas > 0.15 M px, elements at rest > 6 500; S2d: a correction guard at its bound (§9.4), a world-hat value that
is neither a rest spot nor in a flight, a contract value (`api.HEIGHT` ± 0.02, `HAT_TOP` / `SWORD_LEN` / `SCABBARD_LEN` /
`ITEM_SWORD_*` ± 0.01, `BRIM_D`, the registry hit h − the idle hull top outside [0.05, 0.12]) off the build's own measure.
Inside a run of ≥ 4 consecutive authored key ticks (the swings, spins, draws, flips) every moving part keys each tick; a
planted foot's shin keys where its interpolation would lift the sole > 0.006. S2d round 2: a one-shot clip blends in from the
previous clip's pose over the same ticks for every part (each part's first key ends at the first clip event from tick 2, else
at the clip's blend; no dense / event / re-key split inside it, and the riders — head / face / hat / strings, the sword arm /
sword / glow — end their first keys together); an event re-key splits the part the blade entered with its riders and the
sword arm; while the hat is worn, head / face / hat key together wherever the shipped brim comes within 0.001 b of the head's
top corners (a gate), and the right forearm / the cup wherever the cup sinks > 0.03 b into the shipped fist. Numbers of the S2d build: 29 parts, 47 clips,
2 602 rig functions (5.69 MB), 18 761 keys in 2 086 key files, 62 models, 27 painted sprites + the skin (47 872 px), 224
elements at rest (ghost 224). The suite `S:hr/tests/test_rig.py` (146 checks with the S2d sections; `--rebuild` + 3: two
builds byte-identical) replays the shipped key files; on a manifest without the S2d blocks the new sections are skipped.

## 9. S2d: the skeleton, the retarget, the solver

### 9.1 The skeleton (`SK`; rig frame +X her left, +Y up, −Z forward, blocks; the manifest `skeleton`)
The hip line 0.765625 above the floor at pos 0 (the pelvis pivot; 0.74 at rest), the hip joints ±0.125 on it, the seam (the
torso pivot) 0.1875 above it, the neck base 0.5625 above the seam (0.75 above the hip line), the shoulders (±0.34375, 0.4375)
from the seam, upper arm 0.25 + forearm 0.34375 (to the grip point), thigh 0.375 + shin 0.390625 (to the outer layer's sole).
The IK is clamped to the reach (no stretch). The world hat's spots, the stone (top 0.24, front −0.135, back 0.505, half-width
0.6) and its item spots are in the rig frame turned by her yaw.

### 9.2 The retarget (`scarlet_retarget.mjs`; per sample; the source clips are untouched except `HIP_DIR`)
Angles kept; the pelvis offset × k(lf) (S_LEG = 0.765625 / 1.18 = 0.6488 while she stands, 1 while the legs ride the pelvis);
the soles about the hip joint × S_LEG; the grip distances × S_ARM = 0.59375 / 0.82 = 0.7241 (the far root of the reach
equation when the plain scaling folds the grip into the shoulder) and the lock rule; the planted hands × S_LEG; `scOff` ×
S_SCAB = 0.8352; the world hat to its rest spots (side, leg, face) or a re-anchored flight (repel 60-75, ending 26-39; arc ×
K_ARC 0.8264). Derived weights `wLie` (the DOWN / LY family), `wSeat` (the intro seat), `wKnee` / `wLip` (patches).
Declared patches (`PATCHES`, the only angle changes; `--dump` proves it): `KNEEL-K` (kipup 6-12) and `KNEEL-L` (lead_down
5-11) the floor pickup of the hat on the right knee, `KNEEL-K-B` (kipup 3-16) / `KNEEL-L-B` (lead_down 1-17: out over 6
ticks after the kneel) the sword out at her left through the kip and the kneel, `IAI` (cs1 104-161) tor yaw
+14 / head −14 for the cross-draw reach, `SIP` (intro 66-94) the cup at her lips, `SH0` (ending 297-326) the sheathe entry
on the scabbard's axis (the builder's probe `SH0'`), `ASIDE` (intro 226-246, round 2) the feet step with seq.py's 1.1-b
glide aside off the seat stone (four 0.55-b side steps, the stance sole kept on its world spot, the swing sole lifted
<= 0.08 b over its planted height: `fLiftL` / `fLiftR`). The face spot of the world hat (LY) is parallel to her face, its front
toward her feet (as the flight that lifts it at 27: no spin), the smallest lift / tilt that clears her forearms.

### 9.3 The solver's contacts (`scarlet_pose.mjs` `solve`)
`refCore` replays each source sample on S2a's own skeleton: what touched the floor there (`low_ref` < 0.012) touches here,
what was airborne (≥ 0.05) stays up (≥ min(S_LEG × its height, 0.12)). The seat rests the thighs on the stone (hip line 0.385);
the lying rest puts the lowest of pelvis / torso / head / legs at 0.002 with the incline / chin tip / rock chosen on a 1° grid
(gaps ≤ 0.06), and the sword arm rests on the floor beside her hip (lifted off over the 3 ticks before a kip's launch: guard
`armUp`); the kneel puts the right knee on the floor (one tick after the patch's full weight: the bend plane turns 40° / t; the
hips hold their height until it lands); the planted feet's soles at 0.002-0.004 (a bisecting boot loop; a foot the touch rule
lifted is re-planted). Hand targets: the stone items (refined with the solved forearm), the brim hold, the floor hat, the hilt,
the throat, the lips, the hat hand-overs; an arm whose segment would swing > 60° in a tick takes the bend plane (round the shoulder -> grip line)
with the smallest swing, and every limb segment rolls ≤ 35° / t about itself (round 2); the blade-body guard through draws too
(and the free right forearm); the hip
scabbard yaws out of the hanging right arm (`scabArm`); the hand-held hat, its hand-overs and the worn / back swings keep out
of her head and torso (`hatClear`: pushed out along the nearest box face, the right hand following as far as it reaches), the
strings (their painted strands, the loop and the strand below it: round 2) lag the hat by ≤ 30°, ease their gravity pull /
lag, then turn (`strHead`, its sense kept through a swing over her head), out of the head; the worn hat is not floor-turned
(the support lift carries it with her); the seated sash clears the stone's top
(`sashSeat`); the flying world hat is pushed out of her body; the support pass: the touch rule (weight 1 − wSeat) and the air
rule (the airborne height × (1 − wRoot) + 0.002 × wRoot: a full lying / kneeling / seated root stays on its support), then the
last-resort lift.

### 9.4 Correction guards and planning (`GUARD_BOUND`, `GUARD_SLOPE`; the manifest `retarget.bounds` / `slopes`)
Pass 1 measures every guard; pass 2 (and 3 when a guard outgrows its plan) applies the plan = the per-tick values dilated by
the guard's slope (degrees / t, or cm / t for drop, bPush, close, hatBackZ, hatPush, hatClear; percent / t for armUp; loops
dilate circularly; the vector guards keep the direction of their largest tick). A planned value at its bound is a build error.
The manifest `support` (per clip: `low_ref`, the root weight `w_root`, the seat / lie (every full lying root) / kneel / feet /
touch / air / ghost / held / free_r spans, cuts, lifts, `hat_push`, the hand contacts) and
`retarget.clips` (passes, the largest correction per guard, contact distance per kind, stretch, blade residue, support moves)
are the suites' inputs.

Debug: `--debug-dp <dir>` writes `hr_dbg/<clip>/<t>` (every part's compiled transform and the hand / face models of that tick)
for the offline renderer (`S:az/understand/rigtech_render.py --spawn rlk:boss/scarlet/rig/spawn --apply rlk:hr_dbg/<clip>/{t}
--strip 0..<len>:2`).
