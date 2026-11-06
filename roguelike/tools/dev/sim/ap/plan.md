# 아펩의 오아시스 파수꾼 (Guardian of Apep's Oasis) — binding plan (chapter-3 end boss)

Status: **binding, v1 (2026-10-19)**. It supersedes `S:ap/plan_draft.md`. Every critique issue and its decision is in
`S:ap/plan_ledger.md`. The shared chapter-mode hooks Apep needs are listed once, with exact names, in
`S:ap/framework_needs.md` (items `FN-n`). Later changes to this file need a dated note in §14.

## 0. Sources and shorthand

| short | meaning |
|---|---|
| `S:` | `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad` |
| `DP` | `/home/user/rlk/roguelike` (main line; today `5556c79`) |
| `M0` | main after the `wip/fg` merge (`wip/merge-fg` `63b37b6`, QUEUE item 2) |
| `AZ-CM` | the Azhdaha chapter-mode stage (`S1-CM` on `wip/az-cm`, reviewed, merged into main; `S:az/plan_ledger.md` ST-1, AP-2 … AP-8). Apep builds on it |
| `AZL` | `S:az/plan_ledger.md` |
| `FN-n` | an item of `S:ap/framework_needs.md` |
| `F:x` / `AP:x` | `DP/data/rlk/function/x.mcfunction` / `F:mboss/apep/x` |
| `WIKI`, `V1`…`V5`, `V6W` | `S:ap/src/wiki.md`, `S:ap/understand/v1.md` … `v5.md`, `v6w.md` |
| `MD`, `MP3`, `MO`, `ME` | `understand/model.md`, `model_p3.md` (replaces `MD` wherever they disagree), `motion.md`, `mechanics.md` |
| `CH`, `RT` | `S:az/understand/chapter.md`, `rigtech.md` |
| `t` / `b` / `‱` | ticks (20/s) / blocks / basis points of the Heart progress |
| ticks | all ticks below are **played** ticks (after the −25 % wind-up rule); footage ticks are written `fNN` |
| `#hzY1 7` | a hazard band that ends 0.7 b above the feet: a vanilla jump clears it on ticks 2-9 |

---------------------------------------------------------------------------------------------------

## 1. User requirements (binding)

| # | rule | where |
|---|---|---|
| U1 | **Chapter-3 end boss** on the framework's chapter mode (AZ-CM). Azhdaha keeps chapter 1, Raiden chapters 2 and 4+. | §3 |
| U2 | **RES: the boss (phases 1 and 3) Dendro 30 %, the organisms Dendro 20 %, every other element and Physical 10 %.** The 양육 buff (+9900 %) is a mechanic: "buffed organisms can't be damaged". | §7.1 |
| U3 | **The model gets great care** (big boss): high part and element budgets, both forms and the stance change on one rig, organisms as real small models, render sheets against the footage, and **renders sent to the user when the model is done** (the standing rule of the earlier bosses). | §2, §5, §10 |
| U4 | **Wind-ups about 25 % shorter than the footage** (rig `RETIME` knots + pattern ticks; `tell_rt(t) = max(10, round(0.75 t))`); strikes and follow-throughs keep full speed; **every damaging hit has ≥ 10 t of readable telegraph**; the 초목이 시든 풍경 disc fill (23 t) and the 종말의 여파 dome window (≥ 85 t) are never shortened. | §6, §8 |
| U5 | **Attack areas about 20 % bigger** than the footage (×1.2). Safe areas (domes) are never shrunk. | §8 |
| U6 | **No FOV zoom**: no Slowness, no movement-speed modifier, no camera control on the player. Cut-scenes use HUD overlays and the cine flag. | §7.5, §7.7 |
| U7 | **Shared swing rules unchanged** (half walk speed, no jump while swinging). The module never touches swing, jump or speed; its only movement obstacle is the 둥지 walls (blocks). | §7.6.7 |
| U8 | **Balance within about 20 % of the target** with the fairness simulator. | §9.7 |
| U9 | **Korean UI text** everywhere (titles, sub-lines, banners, hints, test messages). | §7, §8 |
| U10 | **Vanilla sounds only**; generators in `tools/`; never hand-edit generated outputs. | §8, §10 |
| U11 | Guardian, butterfly, fieldgen and Azhdaha outputs stay **byte-identical** except the intended shared edits (`ident.py`). | §12 |

---------------------------------------------------------------------------------------------------

## 2. Rig decisions (binding for stages AP-R1 … AP-RC)

**R1 Scale.** 1 m = 1 b (`MP3` §1).
- Phase 1 (종막) crouch: hood top 4.4 b, crown tip 5.0 b, hood width 3.3 b, arm-claw span 10.6 b, **15 b nose → tail tip**
  (tail 9.1 b).
- Phase 3 (기원) upright: **hood top 8.5 b**; waist 3.1, shoulders 5.3, face 6.0-7.85 (mask 1.9 × 1.6), A tips 10.4, B span
  10.4, C span 7.8, hem Ø 2.6, hood + hair width 3.4, B leaf hand 2.2.
- Phase-3 crawl = the CROUCH stance with the phase-3 look (hood 4.4-5.0, 15 b long).
- Camera fallback (if the shoulder view at 4-6 b clips the P3 face): **pose only** (thorax pitched 10° back, waist 2.8,
  hood ≈ 8.0). Never rescale bones.

**R2 Skeleton** (one superset rig for both forms and both stances; pose-only bones cost no entity):

```
root (anchor: module position + yaw only)
└─ pelvis  (pose-only bone = the waist)
   ├─ abdomen ─ hem_a ─ hem_b          P1 rear body + belly ribbons | P3 robe stem + hem flaps on the water
   ├─ tail_1 … tail_7 ─ tail_tip       9.1 b in both forms (7 × ≈ 1.15 b + tip)
   ├─ C_up ─ C_lo ─ C_hand  ×2         P1 rear legs | P3 lower arms
   └─ chest ─ shoulders                thorax split in two (S-coil, hoop, spiral column)
       ├─ core                         P1 belly sac + seed | P3 gold sternum + navel        (on chest)
       ├─ crys_low                     P1 lower spine cones | P3 lower-back emerald          (on chest)
       ├─ crys_back                    P1 gold spine + shoulder cones | P3 upper-back emerald + shoulder spikes
       ├─ clav_A (pose-only) ─ A_up ─ A_lo ─ A_hand  ×2      P1 long arms | P3 raised "antler" arms
       ├─ B_up ─ B_lo ─ B_hand  ×2      P1 front legs | P3 middle arms with the big leaf hands (+ beads on B_up)
       ├─ mantle_a ─ mantle_b  ×2       a chain, not siblings
       └─ neck ─ head
            ├─ face                    P1 bud-skull + crescents | P3 glowing mask
            ├─ hair_1 ─ hair_2  ×2     P1 drapes to the ground | P3 hair to the waist
            └─ hood_hinge (pose-only) ─ hood ─ crown      hood swings back ≈ 110° upright; crown fan rides it
```

- Limb mapping per form (corrects `MD` §4; `MP3` §0.2): A = P1 long arms → P3 upper arms; B = P1 front legs → P3 middle
  arms; C = P1 rear legs → P3 lower arms; mantle = P1 shoulder flaps → P3 carapace plates; hair = P1 drapes → P3 hair;
  abdomen + hem = P1 rear body → P3 robe stem.
- The unfold (crawl → upright, 14 t, `v6 f522-f600`) and the fold (7 t, `v6 f756-f804`) are pose blends of this tree.
- **AP-R1 first identifies the "umbrella" pieces of `v5 f1104`** (mantle vs the A / B arms seen from below) and only then
  freezes the mantle model and its scale (≥ 1.7 if they are the mantle).

**R3 One rigid skeleton.** Author every attachment offset once, in its parent's frame, from the CROUCH pose (the
better-measured stance). Reach UPRIGHT by joint angles only. Where the footage shows an attachment move, a pose-only
bone carries it: `clav_A` (≈ 0.9 b, yaw 0 → ≈ 45°, brings the A roots from 1.6 to 1.1 b out), `hood_hinge` (at the
back-top of the skull, so the swing-back puts the hood peak at 8.4-8.6 b), the `hem_a → hem_b` chain (folds in the
crawl, hangs straight upright). No non-uniform scale on painted parts. The builder prints a residual table against the
`MP3` §6.2 UPRIGHT targets; every joint ≤ 0.25 b.

**R4 Part table: 49 parts (hard cap 56), slots `0x00-0x37`.** Scale = (reach + 10 %) / 1.5. Brightness 13 for hide, 15 for
glows. Phase 1 shows 47 parts (beads at scale 0), phase 3 shows 49.

| # | part | parent | P1 (종막) content | P3 (기원) content | reach → scale | br |
|---|---|---|---|---|---|---|
| 1 | `abdomen` | pelvis | rear body plates, pale belly scales | robe stem front panel (dark teal, olive-gold curl inlay, white diamonds), green back | 2.1 → 1.6 | 13 |
| 2 | `hem_a` | abdomen | dark belly ribbons (upper) | lower robe + hem flaps | 1.9 → 1.4 | 13 |
| 3 | `hem_b` | hem_a | ribbon tips | hem flare on the water | 1.4 → 1.1 | 13 |
| 4 | `chest` | pelvis | ribcage (5-6 rib slabs), belly shell, pale bark side plates | lower chest plates + pale rib-blades | 2.0 → 1.5 | 13 |
| 5 | `shoulders` | chest | hump plates (cowl continuation), shoulder hooks with square gold gems in raised frames | lime chest plates, bottle-green back, gold square shoulder plates | 2.7 → 2.0 | 13 |
| 6 | `core` | chest | belly sac Ø 1.4: near-opaque glass shell + opaque emissive seed, **one model** | gold sternum 2.2 × 0.8 (6-8 chevrons, top diamond) + navel glow | 1.2 → 0.9 | 15 |
| 7 | `crys_low` | chest | lower spine cones | lower-back emerald (0.8 b) | 1.4 → 1.1 | 14 / 15 |
| 8 | `crys_back` | shoulders | gold spine ridge + shoulder cones | upper-back emerald diamond (1.0 b) + shoulder spikes | 2.0 → 1.5 | 14 / 15 |
| 9 | `neck` | shoulders | dark plate neck | neck + grey-green collar | 1.0 → 0.8 | 13 |
| 10 | `head` | neck | skull base | skull base + lime leaf scarf | 1.4 → 1.1 | 13 |
| 11 | `face` | head | closed pale bud-skull + 2 pale-gold crescents | oval mask 1.9 × 1.6, gold lily emblem, lime vein lines | 2.0 → 1.5 | 15 |
| 12 | `hood` | hood_hinge (head) | dark slate cowl (3 plate rows), ear flares, mid-face cone, gold V | bottle-green carapace, lime rims, lime-gold front gem; swings back ≈ 110° upright | 2.8 → 2.1 | 13 |
| 13 | `crown` | hood | gold crown cone + leaf sprig + lime seed bulb | fan of 8-10 gold leaves + glowing bud + brow emeralds + hood shards | 1.7 → 1.3 | 15 |
| 14-17 | `hair_l_1 / r_1`, `hair_l_2 / r_2` | head → hair_1 | dark robe ribbons, 2 segments to the ground | hair strands to the waist (dark bottle green, lime streak) | 1.6 → 1.2 | 13 |
| 18-21 | `mantle_l_a / r_a`, `mantle_l_b / r_b` | shoulders → mantle_a | dark shoulder flaps, pale undersides | dark carapace plates, lime rims | 2.2 → 1.7, 2.0 → 1.5 | 13 |
| 22-27 | `A_up`, `A_lo`, `A_hand` ×2 | clav_A → chain | pale shell arm, inner leaf-scale rows; 3-lobe claw + square gem + gold cone | antler arm: shell + lime leaf cladding + gold elbow cone; forked leafy tip + gold cone | 2.6 → 2.0, 2.8 → 2.1, 1.3 → 1.0 | 13 |
| 28-33 | `B_up`, `B_lo`, `B_hand` ×2 | shoulders → chain | front leg, dark armour → pale bark; 5-petal hand Ø 1.8 + cream cone | middle arm, shell + cladding, dorsal carapace; big lobed butter-yellow leaf hand 2.2 with the white-grey under-leaf fin | 2.0 → 1.5, 2.0 → 1.5, 2.4 → 1.8 | 13 |
| 34-39 | `C_up`, `C_lo`, `C_hand` ×2 | pelvis → chain | rear leg; 5-petal foot Ø 1.5 + cone | lower arm; curled leaf hand 1.5 + square-spiral glyph + cream cone | 1.9 → 1.4, 2.1 → 1.6, 1.6 → 1.2 | 13 |
| 40-46 | `tail_1` … `tail_7` | pelvis → chain | twisted two-band ribbon, pale + slate | twisted ribbon, pale grey-white + dark green | 1.5 → 1.1 | 13 |
| 47 | `tail_tip` | tail_7 | curled hook + pale leaf curl | thin whip + pale leaf tip | 1.3 → 1.0 | 13 |
| 48-49 | `beads_l / r` | B_up | scale 0 | white leaflet strings on a vine (pendulum) | 2.1 → 1.6 | 14 |

Seven spare slots (≤ 56) stay for later care (a second tail ribbon, per-hand glow) only if the renders show the need.

**R5 Bounds.** Every part passes `checkBounds` (reach ≤ 1.5 × scale per axis) in every pose of every clip.

**R6 Culling and range.** `width:30f, height:16f` on every part (the 종말의 여파 hover with raised A arms reaches ≈ 13-14 b),
`view_range 3`. The builder prints each clip's extents and warns on any overhang. Shadow helper (empty model,
`shadow_radius 4.5`, strength 0.8) at slot `0x40`.

**R7 Hit proxies** (data in the rig manifest; the framework generates `px/*`, FN-8). 11 interaction ground columns in
slots `0x41-0x50` (≤ 16):

| proxy | CROUCH (P1, P3 crawl): ground point (x, z) · w × h | UPRIGHT (P3): ground point · w × h |
|---|---|---|
| `px_head` | hood front (0, −3.4) · 2.4 × 4.5 | under the face (0, −0.7) · 2.8 × 8.5 |
| `px_chest` | thorax (0, 0) · 3.0 × 5.0 | stem back (0, +0.5) · 2.6 × 6.5 |
| `px_abd` | abdomen (0, +2.0) · 2.6 × 4.0 | tail root (0, +1.3) · 2.0 × 2.5 |
| `px_tail_a` / `px_tail_b` | tail 3-4 (0.2, +6.0) / tail 6-7 (1.3, +9.3) · 1.8 × 2.0 | tail coil (1.6, +4.1) / (3.8, +2.4) · 1.8 × 1.5 |
| `px_A_l / r` | arm claws (±5.3, −2.6) · 1.8 × 2.5 | at the B elbows (±2.8, −0.9) · 1.6 × 6.0 (the A tips at 10 b are out of reach) |
| `px_B_l / r` | front petal feet (±2.5, −3.6) · 1.8 × 3.0 | under the leaf hands (±4.6, −1.0) · 2.2 × 6.8 |
| `px_C_l / r` | rear feet (±3.0, +3.0) · 1.6 × 3.0 | curled hands (±3.7, −0.8) · 1.8 × 2.5 |

- Per-clip proxy tracks (AZ manifest schema); the unfold slides the columns between the two tables over its 14 t.
- States (any names, from the manifest): `p1`, `p3u`, `p3c`, `burrowed` (none + `rlk_mb_inv`), `aloft` (Q2 hover:
  `px_head` and `px_chest` with h 10, the rest off), `parked` (none), `dead`.
- **Coverage gate** before merge (`RT` §5.5 tool): 100 % of the outline within 3.0 b of a proxy for CROUCH, UPRIGHT, the
  hoop and the crouch-over pose.
- One HP pool, one hit per attack (`#atkSeq`), hit flash only on the hit proxy's part group
  (`flash/<head|body|front|rear|tail|arms>`).

**R8 Hands change shape with the stance** (one display shows one model, so a "petal open 0..1" channel is impossible).
Discrete model variants (same sprites, no atlas cost): P1 B / C `open` (planted starfish) / `curl` (lifted ≥ 0.3 b);
P1 A `planted` / `raised`; P3 B `curl` / `open` (the big lobed leaf); P3 C `curl`; P3 A `fork` — about 24 hand models.
Swapped at fixed events (`stand_p3` t5-8 while the arms unroll, `crouch_p3` t2, P1 lifts) with a 0.9 → 1 scale pulse on
the swap tick. The hands have their own region file `apep_hands.mjs` and their own refiner; ≈ 400-600 elements per P3 B
hand at 64 px/b.

**R9 Burrow.** The root sinks to **−6 b** under the opaque floor (the floor hides it, `RT` §4.1); fully buried parts go to
scale 0 (hidden spans in the manifest); straight descents use the `follow_y` offset. Builder check: **every visible part's
top ≤ −0.1 b at each hidden-span start**. The P3 upright always folds (`crouch_p3`) before sinking. While hidden the body
carries `rlk_mb_inv`, proxies `burrowed`, husk scale 0.1 and `rlk_mb_noshield` (AZ's burrow rule, FN-13); the module shows
the shadow / leaf-pad props on the hidden anchor.

**R10 Park.** `rig/park` (parts scale 0, no follow keys, proxies `parked`, shadow off, rig tick skipped) and `rig/unpark`
(re-apply form, stance, looks, follow). Used from T1 t45 to CS t32 (≈ 100 s). A rig respawn (reload) honours the park
flag. Built on RIGLIB's static-anchor follow skip (FN-25).

**R11 Solidity and underside.** Capsules per stance in the manifest (the framework push, FN-21): CROUCH — sac + thorax
column r 1.0 around f +1.0 and the hips r 1.2 around f −1.0 (legs, arms and tail stay walk-through); UPRIGHT — the robe
stem r 1.4. The P1 underside is modelled for views from below: rib slabs and belly-shell faces that face down and are
painted; no open box bottoms.

**R12 Looks.**
- Form looks per part (item-model swap of every part at the CS white-out): `p1`, `p3`.
- Face: `p1_bud`, `p3_idle`, `p3_charge` (orange-gold, `w1 f127`), `p3_dim`, `hidden` (scale 0 at `crouch_p3`'s close
  tick; a br-15 mask would glow through plate gaps in the crawl).
- Core: `p1_bulb`, `p3_sternum`.
- Tints (constant-tint item definitions, the Guardian method; `tintindex 0` on every painted face, the builder counts
  untinted faces per look): `p1_dark` (burrow, #2D2A04-ish), `p1_brown` (root-chunk sink, #605D37), `withered` (death),
  `p3_dim`.
- Brightness channel 13 ↔ 15 = the `p3_lit` charge (증폭의 풀, 생명의 나선, 종말의 여파): no extra sprites.
- The `ghost` dissolve of `MO` is replaced by a 4 t scale-in 0.85 → 1 plus white-green motes.
- **No body look swap inside `stand_p3` / `crouch_p3`**: only the R8 hand variants and the face show / hide.

**R13 Textures: rig ≤ 0.9 M px for both looks.** Materials both looks share are grey-value sprites tinted per look
(`tintindex 0`): pale shell limbs, rib-blades / bark plates, the two-band tail, hump / dorsal plates, the mantle. New
phase-3 sprites only for phase-3-unique features: face mask + charge, crown fan, sternum, B / C leaf hands (open + curl),
leaf cladding, robe + hem, beads, emeralds. Densities: 64 px/b face, crown, B hands; 48 px/b hood; 32 px/b elsewhere.
Sides multiples of 16, ≤ 512. The manifest carries a per-region sprite ledger (sprite, px, px/b, unique / tinted). The
global atlas gate is FN-27.

**R14 Elements.** Visible at rest: P1 ≤ 7 k, P3 ≤ 8 k (printed per form in the manifest; the densest models are the face,
crown, B hands, hood and shoulders).

**R15 Palette.** Phase 1: `MD` §7.1. Phase 3: `MP3` §7 ramps (`p3_bottle`, `p3_rim`, `p3_lime`, `p3_leafhand`, `p3_pale`
— not lilac, `p3_line`, `p3_emerald`, `p3_face`, `p3_face_charge`, `p3_sternum`, `p3_crown`, `p3_bud`, `p3_gem`, `p3_cone`,
`p3_cone_gold`, `p3_robe`, `p3_hair`, `p3_tail` pale + green — not mint, `p3_beads`), de-hazed as in `MP3`.

**R16 Tolerances and yaw.** `tol.tp` 0.03 b on arms, tail, hair, mantle, hem; 0.012 b on hood, hands, face. No horizontal
root travel and no root yaw inside clips; the module moves and turns the anchor. Spins and sweeps export **anchor-yaw
schedules** (`turn_p1_step`, `turn_p3`, `rotation` spin, `hands` swirl, `combo_c` spin, `aftermath` whirl, the tail
swings of `tail_p1x2`, `tail_p3`, `move_strike_p3`). The 이동 돌진 hoop's 360° pitch cannot ride the anchor: it is keyed
(the builder prints its keys per tick; fallback a wheel pose with a short roll plus the kit's arc trail). Vertical travel
(`pelvis.y`) is in the clip.

**R17 Secondary motion** (`MO` §3): pendulum sims on mantle, hair, hem and beads (lag 2-4 t, damping 0.85, fling in spins);
travelling-sine tail idle (±6°, 60 t, 8 t lag per segment); spine breathing; core glow 9 ↔ 12.

**R18 Camera views.** Renders from the player's camera points (3.5 / 4.5 / 6 b back, 0.5-1.5 b above the head) in UNDER
and BACK; cards below 2.5 b (hem, hair tips, tail cards) have one-sided outer faces so the camera inside the hip / tail
region does not fill the screen.

**R19 Files and names.**
- `tools/build_mboss_apep_rig.mjs` (entry: PARTS, budget check 56, UUIDs, RP write, compile, API, proxies, capsules,
  residual print, manifest).
- `tools/apep_pose.mjs` (PART_SCALE, FK, foot IK for planted hands, proxy points, capsules, stance rest poses CROUCH /
  UPRIGHT).
- `tools/apep_clips.mjs` (DEFAULT_POSE, the P1 poses of `MO` §5, the P3 pose glossary of §6.2, CLIPS, RETIME, events,
  hidden spans, yaw schedules, px tracks, hand / face events).
- `tools/apep_geometry.mjs` and `tools/apep_paint.mjs` (thin aggregators), `tools/apep_materials.mjs`.
- Regions: `apep_head.mjs` (neck, head, face, hood, crown, hair), `apep_body.mjs` (abdomen, hem, chest, shoulders, core,
  crys_low, crys_back, mantle), `apep_limbs.mjs` (A / B / C up and lo, beads), `apep_hands.mjs` (all hands and their
  variants), `apep_tail.mjs` (tail_1-7, tip).
- `tools/mboss_apep_rig_api.md`, `tools/mboss_apep_rig_manifest.json`.
- Namespace `rlk:mboss/apep/rig`; tags `rlk_mb_apep_part`, `rlk_mb_ap_<part>`; objectives `apRig*`; debug poses
  `ap_dbg/<clip>/<t>`.

**R20 Shared rig libraries.** Apep consumes the RIGLIB stage (FN-25: `tools/mboss_shape_lib.mjs`, `tol.tp`, px track
compile, culling / view range per rig, `follow_y`, static-anchor follow skip, per-state follow lists, shadow helper, park).
Until RIGLIB is on main, AP-R1 uses a temporary copy `apep_shape.mjs`, switched to the shared lib at AP-R3 with Apep's own
outputs byte-identical before and after. **No Apep branch edits a shared rig library.**

**R21 Render sheets** (`S:az/understand/rigtech_render.py`; references from `MP3` §12):
- P1 crouch front / side / 3-4 / top vs `MD` 01, 02, 04 and `v2 f2076` / `f870`; P1 rear-up and underside from the
  player's eye 1 b outside the capsule.
- P3 upright front / side / back vs `v6 f480`, `v5 f1074`, `v5 f588`, `v5 f1908`, `w2 f436`.
- P3 crawl vs `v6 f165`, `f90`, `f99`, `f528`.
- The unfold strip `stand_p3` t 0 / 4 / 8 / 11 / 14 next to `v6 f522` / `f540` / `f558` / `f576` / `f600` (`MP3` sheet 03).
- Hands (every variant), each look and tint, the burrow cut line, proxies + capsules overlay, the camera-inside views (R18),
  the R3 residual table.

**R22 Rig API** (the module's contract): `spawn`, `tick`, `park` / `unpark`, `play/<clip>`, `face/*`, `look/<form | face |
core | tint>`, `hands/<set>`, `bright/<13 | 15>`, `flash/<group>`, anchors per event (impact point, crown top for the charge
ball, tail root / tip, face, hands), yaw schedules, hidden spans, px states + tracks + capsules (data), shadow.

---------------------------------------------------------------------------------------------------

## 3. Architecture

### 3.1 Fight flow

```
chapter-3 boss map: room/pick/boss -> mboss/cb/route (registry "ch":[3]) -> domain entrance (Sumeru oasis gate)
  entrance build -> mboss/cb/prep {id:apep}: ap_oasis ensure + look "withered" (sliced; cb/start waits on the done flag)
  gate click -> mboss/cb/start {id:"apep"} -> tp_in (arrival r 16) -> E entrance (110 t, untargetable)
  -> PHASE 1 종막 오아시스 파수꾼 (pool 53 %, floor 1 %)            P1-P6, R, M
       floor reached -> next decision point -> T1 소생 단계 진입 (136 t; body parked, cradle rises, Heart lowered)
  -> PHASE 2 소생 단계 (objective 「오아시스의 심장」 2700 -> 10000 ‱; organisms; time-out at 100 s)
       0 ‱ first time  -> 「소생 실패」 (25 % max HP, non-lethal; restart at 2700 from wave 1)
       0 ‱ second time -> mboss/cb/lose (death path: run over, or test/defeat)
       10000 ‱ -> CS 2→3 cut-scene (192 t; white-out: look "lush", repool 47 %, heal 25 %)
  -> PHASE 3 기원 오아시스 파수꾼 (fresh pool 47 %; upright / crawl stances)  Q1, Q3 (+Q3s), Q4, Q5, scheduled Q2
  -> D death (120 t) -> mboss/cb/won (chapter rewards, tp_out, next-chapter object)
player death anywhere -> framework pause -> respawn routing (run/fail or test/defeat), unchanged
```

### 3.2 What Apep takes from the chapter mode

AZ-CM implements the chapter mode once for both bosses (AZL ST-1, AP-2 … AP-8). `S:ap/framework_needs.md` is the exact
list (MUST FN-1 … FN-13: AP-CORE cannot start without them; SHOULD FN-14 … FN-28: a module fallback exists; CAN FN-29 …
FN-32). Names follow AZL AP-3: `mboss/title {title,sub,color}`, `#mbDotPct` (‰ of max HP), registry
`"music": {"<ph>": {ev,len}}` + `mboss/music/set {ph}`, `mbHzNR` / `mbPjNR` + one-shot `#mbNoRx`, `mboss/repool {pct}` +
`#mbTot` + registry `phases`, proxy state sets from the manifest, `mv/lockv`, `mv/local`, `push/capsule`, `push/ring`,
`cine/start|end`, per-entity `mbRes0..8`, `#pjNoDodge`, `#buHpCol`, arena entries with `theme` + `looks`, themes discovered
from the registry, font U+E900 for Apep.

### 3.3 What stays in the Apep module

| piece | where |
|---|---|
| the two forms, the two stances, pools / floor / titles, the phase machine (E → P1 → T1 → P2 → CS → P3 → D), deciders | `core.py`, `ai.py` |
| patterns P1-P6, R, M, E, D | `p1.py`, `seq.py` |
| patterns Q1, Q3, Q3s, Q4, Q5, stance changes | `p3.py` |
| Q2 종말의 여파 (field, domes, blast, schedule) | `aftermath.py` |
| T1, the Heart objective, waves, spawn points, stage clock, time-out, failure strikes, phase-2 HUD, CS | `revival.py` |
| the organism runtime and the six kinds (AI, attacks, links, shields, swallow, walls, rolling bomb), `aux_hit` branch | `org.py` |
| body park during phase 2, the Heart / dome / wall props' placement | `revival.py`, `aftermath.py`, `org.py` |

### 3.4 What failure means in our roguelike (Q2)

A Heart at 0 % fails the domain in Genshin; here a death ends the run. One slip in a 6-minute chapter-3 fight should not
end a run, and should not cascade into a phase-3 death either:

| event | result |
|---|---|
| **1st time the progress reaches 0** | 「소생 실패」 (≈ 60 t): the Heart withers (dark look), a Dendro shock ring r 0 → 26; every organism bursts with no progress; walls cleared; the player takes **25 % max HP, non-lethal, undodgeable, no reaction** (`pl_dot` 250 ‰, `#mbDotLethal 0`, `#mbNoRx 1`); progress back to **2700**, wave index back to **1**, the stage clock and the time-out reset; red line "다시 한 번 실패하면 쓰러집니다"; for the next 20 s the sub-line shows "수호 → 강화된 기본 → 파괴 순서로 처치하세요"; a "⚠" badge stays for the rest of the stage |
| **2nd time in the same fight** | `mboss/cb/lose` (FN-9): the normal death path |
| Ronova's once-per-map revive after the lose | the stage restarts at 2700 from wave 1 once more (the module sees a living player with `#apFail 2`) |
| player death by damage in phase 2 | as everywhere: framework pause → respawn routing |

### 3.5 Module file layout (generators in `tools/`)

| file | content | owner stage |
|---|---|---|
| `tools/build_mboss_apep.py` | entry; writes `AP:**` except the rig, org-model and kit subtrees; owned dirs for `clean()` | AP-CORE |
| `tools/mboss_apep/__init__.py` | layout doc; `PATTERN_MODULES = ('p1','p3','aftermath')`, services `('seq','revival','org')` | AP-CORE |
| `tools/mboss_apep/api.py` | **stable contract**: ids, scores, the coefficient table `DMG` (with raw values, §9.3), the phase-2 table `REV` (§7.6.2), ranges, colours, Korean texts, the rig clip table and anchors from `mboss_apep_rig_manifest.json`, the org table from `mboss_apep_org_manifest.json` (Heart footprint, sockets), `Pattern`, `TL`, `Gen` helpers (locks, `keep`, clamps per form, `wedges()` for swept sectors, `tell_rt`, `rt(clip,t)`), kit builders `api.K` (optional until I1, no-op fallbacks) | AP-CORE (frozen at I1; changes by request) |
| `tools/mboss_apep/core.py` | the 17 hooks + `prep`; RES at spawn; pools / floor / titles; phase machine; proxies per form / stance; capsules; music; bars; pause / reload / cleanup / uninstall per phase (§7.2); tests; generated dispatchers | AP-CORE |
| `tools/mboss_apep/ai.py` | zones (`mv/local`), bands, turning / crawl / walk, clamps, the BACK dwell rule, weights, cooldowns, no-repeat, chains, the Q2 schedule, anti-stall | AP-CORE |
| `tools/mboss_apep/p1.py`, `seq.py` | P1-P6, R, M; E, D | AP-P1 |
| `tools/mboss_apep/p3.py`, `aftermath.py` | Q1, Q3, Q3s, Q4, Q5, stance changes; Q2 | AP-P3 |
| `tools/mboss_apep/revival.py`, `org.py` | T1, Heart, waves, failure, phase-2 HUD, CS; organisms, walls | AP-REV |
| `tools/mboss_apep/stub_rig.py` + `stub_rig_manifest.json`, `stub_org.py` + `stub_org_manifest.json` | stand-ins with the §6 / §5 names, lengths, events, footprints (removed at I2 / I1) | AP-CORE |
| rig files (R19) | the boss rig | AP-R1 / R2 / R3 / RC |
| `tools/build_mboss_apep_org.mjs`, `apep_org_geometry.mjs`, `apep_org_paint.mjs`, `apep_org_clips.mjs`, `tools/mboss_apep_org_api.md`, `tools/mboss_apep_org_manifest.json` | organisms, Heart, vine hand, domes, wall blades, summoned stalks, seed prop (`AP:om/**`) | AP-ORG1 / ORG2 |
| `tools/build_mboss_ap_fx.py`, `tools/mboss_ap_fx_paint.py`, `tools/mboss_ap_fx_manifest.json`, `S:ap/ap_fx_api.md` | the fx / audio / HUD kit (`AP:fx/**`, font `rlk:mboss_ap`) | AP-FX |
| `tools/mboss_arena_ap_oasis.py` | the arena theme + entrance room (FN-3 interface) | AP-ARENA |
| `S:ap/ap_contract.md` | core ↔ pattern / org / revival / kit / rig contract; §0 = day-0 interfaces (§3.9) | AP-SPEC, then AP-CORE; appended by each stage |

Generator order (README "등록 · 모듈", extended by AZ-CM): core → arena (themes from the registry, `ap_oasis` included) →
cboss rooms → proto / cproto → rig generators (Guardian, butterfly, fieldgen, Azhdaha, **Apep rig**, **Apep org**) →
guardian → bf kit → butterfly → fg kit → fieldgen → az kit → azhdaha → **ap kit** → **apep** → `check_mboss_pack.py`.
Two runs give no diff; reverse order and module wipes rebuild the same.

### 3.6 Runtime names, UUIDs, font

- Functions `rlk:mboss/apep/**` (`rig/`, `om/`, `fx/`, `p/<key>/`, `org/`, `heart/`, `dome/`, `wall/`, `seq/`, `ai/`).
- Tags `rlk_mb_ap_*` (`rlk_mb_ap_org`, `rlk_mb_ap_<kind>`, `rlk_mb_ap_heart`, `rlk_mb_ap_dome`, `rlk_mb_ap_wall`); rig
  `rlk_mb_apep_part`, `rlk_mb_ap_<part>`; arena props `rlk_mb_arena_prop rlk_mb_ar_ap` (never `rlk_room`).
- Scores in `mb`: `#apPh` (1, 15 = T1, 2, 25 = CS, 3, 9 = death), `#apTot`, `#apHt` (‱), `#apWave`, `#apClk`, `#apTo`,
  `#apFail`, `#apAftCd`, `#apAftN`, `#apAft1` (first Q2 done), `#apLast`, `#apZone`, `#apBand`, `#apBackT` (BACK dwell),
  `#apChain`, `#apStance` (0 crouch, 1 upright), `#apPark`. Objectives `apK` (kind), `apS` (state), `apT` (state clock),
  `apL` (link id), `apShd` (shield pool), `apOC` / `apOI` (org clip clock / id), `apSock` (Heart socket), `apTok` (attack
  token); rig `apRig*`.
- UUID blocks:
  - rig `524c4b4d-4150-4400-8000-0000000000NN` (`[I;1380731725,1095779328,-2147483648,NN]`): parts `0x00-0x37`, shadow
    `0x40`, proxies `0x41-0x50`;
  - objects `524c4b4d-4150-4800-8000-0000000000NN` (`…,1095780352,…`): Heart bulb `0x00`, cradle `0x01`, arms `0x02`,
    tips `0x03`, vine hand `0x04`, vine stem `0x05-0x08`, domes `0x10-0x15` (3 × shell + decor), summoned stalks
    `0x20-0x2B` (4 × 3), seed prop `0x30`;
  - arena props `524c4b4d-4150-4100-8000-0000000000NN` (`…,1095778560,…`): water tiles, lily pads, bulb flowers, bank
    crystal spikes (per-fight entities, FN-3);
  - organisms and wall blades are multi-instance (no fixed UUIDs).
- Kit font `rlk:mboss_ap` at **U+E900-E9FF** (AZL AP-8); the build checks it against `hud`, `bossbar`, `minimap`,
  `mboss_gd`, `mboss_bf`, `mboss_fg`, `mboss_az`.

### 3.7 Registry entry (data-only, Apep's own key)

```json
{ "id": "apep", "n": 11, "kind": "chapter", "ch": [3], "w": 0, "minCh": 3, "maxCh": 3, "route": false,
  "name": "아펩의 오아시스 파수꾼", "sub": "종막 오아시스 파수꾼", "color": "#C9C452", "el": 7,
  "hp": 290, "xp": 40, "atk": 12, "lvAdd": 0, "dmgMul": 150, "goldMul": 1, "sap": 0, "picks": 0,
  "scale": 2.0, "hit": {"w": 2.6, "h": 3.6}, "intro": 110, "death": 140, "deathSnd": false,
  "arena": "ap_oasis", "res": {"7": 30, "*": 10}, "phases": [53, 47],
  "music": {"1": {"ev": "minecraft:music.overworld.deep_dark", "len": 0},
            "2": {"ev": "minecraft:music.nether.soul_sand_valley", "len": 0},
            "3": {"ev": "minecraft:music.overworld.lush_caves", "len": 0}},
  "icon": {"item": "minecraft:pitcher_plant", "model": "minecraft:pitcher_plant"} }
```

- Chapter entries follow AZ's rule (AZL F1): they live in `creg` / `cbyid`, and `route: false` keeps player routing to
  Apep off until AP-I2; `test/chapter {id:"apep"}` works from AP-CORE on.
- `hp` 290 is the start value (§9.6); the fairness pass may move it within 270-320.
- `hit` is the body's own click shield (torso only); the proxies carry the rest.
- Music events and lengths per AZ's schema (FN-23, stereo `music.*` events in the `record` category; `len` measured by
  the chapter-mode stage; `len 0` = play once). Q17.
- Arena entry (FN-3): `"ap_oasis": {"theme": "ap_oasis", "ver": 1, "cx": 440, "cy": 201, "cz": 8, "r": 29, "walk": 26,
  "safe": 24, "start": {"x": 440.5, "y": 201.0, "z": 24.5, "yaw": 180.0}, "looks": ["withered", "lush"]}`.

### 3.8 Chapter-3 routing

- `room/pick/boss` → the generated `mboss/cb/route`: `#chapter 3` → `mboss/cb/layout {id:"apep"}` (from the registry `ch`;
  no generator edit). The zones carry `data.boss_id:"apep"`, `data.cboss:1b`.
- Level: the boss map `#mapIdx 5` in chapter 3 → **L18**. Theme Sumeru (`#th 5`).
- Domain entrance (`entrance_layout()` of the theme): a sandstone / mud-brick oasis gate (`cut_sandstone`, `mud_bricks`,
  `smooth_sandstone`, gold-green crystal displays) with the gate object; gate label "아펩의 오아시스 파수꾼 — 내성: 풀 30% ·
  그 외 10%".
- Win → `mboss/cb/won` (×15 gold × chapter, 2 sapphires, 40 XP, next-chapter object); lose → FN-9.

### 3.9 Day-0 interfaces (stage AP-SPEC, before the content stages start)

`S:ap/ap_contract.md` §0, written once and then only extended by request:
1. **Rig manifest schema**: AZ's manifest v1 schema (clips, lengths, events, RETIME, hidden spans, yaw schedules, per-tick
   px tracks, anchors) + Apep extras: `stances` (CROUCH / UPRIGHT), `hands` (variant sets and swap events), `capsules`
   per state, `park`, per-region sprite ledger, element counts.
2. **Org manifest schema**: kinds → displays, looks / forms, clips with events, passenger offsets, HP-bar offsets,
   click-shield sizes, footprints (the Heart bulb box, root radius, sockets, the 파괴 stop, wall exclusion radius).
3. **Kit call list** (`ap_fx_api.md` §0 skeleton): every preset / telegraph / prop / sound / HUD name with macro args that
   §8 uses.
4. **Theme interface** (FN-3): `arena_layout()`, `entrance_layout()`, `look_lines(look)`, `props(look)`, constants.
5. **Names**: §3.6, the test ids (§12.2), the stub manifests.

---------------------------------------------------------------------------------------------------

## 4. Arena `ap_oasis` (theme module `tools/mboss_arena_ap_oasis.py`)

Reference: a round **forest lake ringed by giant trees** under a canopy of huge translucent veined leaves (`V1` §5.4,
`V2` §1, `V3` §6.5, `V5` §4.6, w2 S4). Phase 1 is withered and olive-yellow, phase 3 lush teal-green. Phase 2 is played
on the same field (no second arena).

### 4.1 Layout

| ring / item | spec |
|---|---|
| centre / box | (440, 201, 8), stand height 201. Box ±44 (x 396..484, z −36..52), y 190..250. Forceloaded on demand (FN-12). |
| walk disc r ≤ 26 | **full opaque blocks only**: solid from y 192 to the floor top y 200 everywhere inside r 26 (the rig root sinks to −6 b = y 195, hidden parts down to ≈ y 193). No mud (14/16 collision), slabs, carpets, glass, leaves, water or supported decor inside the disc. |
| floor (both looks) | moss-green cells 2-4 b of `moss_block`, split by dark root / crack veins of `packed_mud`, `rooted_dirt` and `dark_oak_wood` flush in the floor; `pale_moss_block` only at r 24-26 (`V1` §5.4, `V4` §4.7). The olive haze of phase 1 comes from lighting and particles. |
| rim bank 26 < r ≤ 29 | low root / rock bank 1-3 high (`mossy_cobblestone`, `rooted_dirt`, `mangrove_roots`); `leaf_litter`, dry grass and dead bushes only here, on supporting blocks; an invisible **barrier wall at r 27..28, y 201..215** (never touched by any wall cleanup). |
| giant trees r 30-38 | 8-10 trunks 4-6 b wide (`jungle_log`, `mangrove_log`, `pale_oak_log` cores, `mangrove_roots` buttresses). Buttress roots arch inward over the rim only above y 207. Shelf mushrooms (`brown_mushroom_block` / `mushroom_stem`) and glowing bulbs (`ochre_froglight` / `verdant_froglight`) at their feet. |
| canopy y 225-250 | broad leaf panels arching over the rim; withered `pale_oak_leaves` + `yellow_stained_glass` "veined leaf" windows; lush `azalea_leaves` / `flowering_azalea_leaves` + `lime_stained_glass`. A sky shaft r ≤ 8 stays open over the centre (the light shaft and the Heart's hanging place in phase 1). No biome-tinted leaves. |
| lush water look | per-fight display props (FN-3, arena-prop UUID block): 4 × 4 water-sheet tiles of 14 b (one sprite, ≈ 40 % alpha) at **y 201.005** over r ≤ 26; lily-pad and bell-flower displays beyond r 22. Telegraph decals sit at y ≥ 201.035 and are cutout or emissive (translucent sorting is per entity). Real water never inside the disc. |
| phase-2 dressing | kit decals only (Q18): the Heart's gold swirl ring r 3.5, 6-8 pulsing orange-gold ley-line crack strips from the centre to r 14 ("지맥 이상"), drifting gold motes; removed at the CS. |
| Heart spot | the centre. The cradle rises there in T1; the centre is clear in phase 1. |
| organism spawn points | 8 points on r 12 (azimuth 22.5° + 45°·k); 양육 points on r 7 on the same bearings. Marked by nothing until used. |
| player arrival | (440.5, 201, 24.5), yaw 180 (r 16 from the centre; `V1` E ends with the boss 12-15 m away) |
| lighting | an invisible `light` layer at y 206 over the disc: level 12 (withered), 14 (lush; in the look diff). Every display has a fixed `brightness`. |
| haze | kit ambient particles: olive `dust` drift (withered), `spore_blossom_air` + `happy_villager` glints (lush). Fog off (Q11). |
| bank props | gold crystal spikes on the bank r 26-29 (per-fight displays, brightness 15). |

### 4.2 Looks and the swap (FN-3)

- The theme exports `look_lines(look)`: the **diff** between `withered` and `lush` as `fill … replace` boxes ≤ 32 768 blocks
  (canopy leaf and glass types, bank decor, the light layer); the floor itself does not change.
- `look/lush` runs in ≤ 24 slices inside the CS white-out (40 t), one per tick; the generator measures each slice on a
  server (target ≤ 20 ms); a done flag.
- The build stamp stays `ap_oasis@<ver>`; the current look lives in `rlk:mboss arena.ap_oasis.look`. The withered restore
  runs from `prep` (entrance build); `cb/start` waits on its done flag (gate shows "준비 중").
- Props of each look are per-fight entities with fixed UUIDs (`props(look)`), spawned at fight start (withered set) or in
  the white-out (lush set), killed by cleanup; tagged `rlk_mb_arena_prop rlk_mb_ar_ap`.
- `arena_layout()` and `entrance_layout()` are importable for offline top / iso renders of both looks.

### 4.3 Entrance room

Chapter-3 Sumeru theme: sandstone / mud-brick oasis gate, gold-green crystal displays, the gate object (oact 16) and its
label (§3.8). Built from `entrance_layout()` by the chapter mode's room generator.

---------------------------------------------------------------------------------------------------

## 5. Models besides the rig (AP-ORG; `MP3` §8-§10, `MO` §7)

Organisms are multi-instance item-display rigs riding their framework aux husk as passengers. Animation key functions run
`execute on passengers if entity @s[tag=rlk_ap_om_<part>] run data merge …`; facing uses `rotate` on the passengers (a
`tp` would dismount them); every model translates down ≈ 2 b from the passenger point to the feet. Sampling uses
`mboss_rig_clips.mjs`; a small emitter in `build_mboss_apep_org.mjs` writes `AP:om/<kind>/c/<clip>/k/<t>` and a per-kind
dispatch on `apOI` / `apOC`. Shells stay near-opaque (alpha ≥ 0.9) with opaque emissive cores, so one-entity sorting never
matters; translucent overlays (the shield bubble) are rim-only and low alpha.

### 5.1 Organisms

| kind | size (b) | displays | looks / forms | clips (len t) | elements | sprite px | br | HP-bar y / click shield |
|---|---|---|---|---|---|---|---|---|
| 기본 basic | bell 1.15 (1.35 with the stem), Ø 0.9; bag lying 1.43 × 1.31 | `bulb`, `crown`, overlay `shield` (only while shielded) | bulb `bell` / `bag` / `buffed` (brighter sheen) / `dying`; crown `closed` / `open`; shield = 2-4 cutout leaf panes 1.3 × 0.55 + a low-alpha bubble rim + a yellow 3-leaf crown | `org_spawn` 20, `basic_bob` 24 L, `basic_melee` 14 (hit 10), `basic_lie` 10 (bell → bag), `basic_ranged` 20 (crown open 0-12, fire 12), `org_die` 10 | ≤ 350 | ≤ 12 k | 14 (core 15) | +1.6 / 1.2 × 1.6 |
| 양육 nurturing | 2.4 | `stalk` (S-curved dark-teal ribbon), `cap` (cream hood-leaf), `orb` (15, pulse), `ring` (translucent cylinder r 1.3, h 0.5, only while immune) | cap `idle` / `tilt`; ring on / off | `nurt_idle` 40 L, `nurt_buff` 20 (cap tilts 0-8, tethers from 8), `nurt_die` 17 | ≤ 450 | ≤ 16 k | 14 / 15 | +2.8 / 1.4 × 2.6 |
| 수호 guarding | spire 4.4 (closed bud ≈ 2); orb Ø 0.4 hovering 0.6-0.8 above the tip | `spire` (mid-height pivot), `orb` (15, bob) | spire `spire` / `bud` / `wisp` | `guard_idle` 60 L, `guard_cast` 30 (collapse 0-7, bud 7-16, regrow 16-24, shields 30), `guard_die` 17 | ≤ 450 | ≤ 16 k | 14 / 15 | +3.0 (beside the base) / 1.4 × 3.0 (the orb at ≈ 5 b is out of reach) |
| 둥지 nesting | 2.2 × 1.3, hovers 0.5-1.5 | `cap` (+ orb, 15), `wing_l`, `wing_r` | — | `nest_fly` 14 L, `nest_cast` 12 (walls 12), `nest_blink` 6 (out 0, in 3), `org_die` 12 | ≤ 400 | ≤ 12 k | 14 / 15 | +2.2 / 1.6 × 2.2 |
| 파괴 destruction | Ø 1.2 (+ 0.2 spikes, 0.4 beak) | `shell`, `face` (15, pulse scale) | shell `normal` / `husk` | `destr_roll` 32 L, `destr_fuse` 56, `destr_suck` 5, `destr_blast` 1, `org_die` 10 | ≤ 300 | ≤ 8 k | 14 / 15 | +1.6 / 1.3 × 1.3 |
| 포식성 predatory | fish 2.5 × 1.3; bud 2.1 × 1.6; pod 3.5 × 1.8 | `body`, `jaw`, `fin`, `core` (15) | body `fish` / `fish_flare` / `bud` / `pod` (its own model, no Y stretch) / `face` | `pred_swim` 16 L (fin yaw ±25°, body ±8° with 3 t lag), `pred_swallow` 24 (eat 12, bud 14), `pred_bud` 20 L, `pred_inflate` 10, `pred_burst` 10 (hit 0, fish 2), `pred_bite` 6 (jaw open 0-3, hit 4), `pred_bite_chain` 38 (hits 4/10/16/22), `org_die` 12 | ≤ 500 | ≤ 20 k | 14 / 15 | +2.2 / 1.6 × 1.6 |

Colours: `MP3` §7 phase-2 fixes (`org_bell_v2` neutral cream-grey for the basic, not mint) and `MP3` §9 descriptions;
paint ≈ 10-15 % less yellow than sampled (phase-2 haze). Spawn: a 20 t white wireframe marker (kit) + a 4 t scale-in.

### 5.2 The Heart of the Oasis (single, fixed UUIDs)

| display | spec |
|---|---|
| `heart_bulb` | a translucent glowing lemon seed lying on its side, **3.2 × 2.6 × 2.3**, 5-7 soft ribs, a white-yellow specular band, an inner swirl; emissive, alpha ≈ 0.85, brightness 15. Looks `idle`, `egg_gold`, `egg_green` (`MP3` ramp), `withered`, `blaze`. **Arrival egg = the same model at scale 0.7, pitch 0 (upright)**; it scales to 1.0 and pitches to lying over the 6 t landing squash. |
| `heart_cradle` | 4-6 knobbly dark-brown root fingers + a mound, feet splayed 1.5-2 b; look `pedestal` (pale petal clumps + 3 gold sprouts, `v2 k_f2304`); mid-height pivot, scale ≤ 2.2 |
| `heart_arms` | two tall root arms curling over the bulb to 4.0-4.3 b; mid-height pivots, scale ≤ 2.2 |
| `heart_tips` | glowing leaf-flame sprouts (15) on the arms and the short roots, swaying |
| `vine_hand` + `vine_stem` | a dark vine "hand" of 5-7 curling tendrils + a 3-4 card stem from the shaft rim; it holds the egg in the entrance (9 b up, the boss touches it), draws it up into the canopy (y + 20) for phase 1, lowers it in T1, and wraps it in the CS |
| footprint (manifest) | bulb box, root radius 2.5; **3 melee sockets at r 3.4** (0°, 120°, 240°), wait ring r 4.5, **파괴 stop r 2.6** off the socket bearings, wall exclusion r ≤ 4.6. `revival.py` / `org.py` read them from the manifest. |
| clips | `heart_hang` 80 L, `heart_up` 30, `heart_lower` 50, `heart_drop` 30 (land 6, beam 6-16), `heart_idle` 40 L, `heart_hit` 6, `heart_gain` 8, `heart_wither` 30, `heart_blaze` 24, `heart_lift` 46, `cradle_rise` 20, `cradle_sink` 10 |
| budget | ≤ 800 elements, ≤ 40 k px |

### 5.3 Domes, walls, summoned stalks, seed

| object | spec |
|---|---|
| 소생의 찬가 보호막 dome ×3 | a hemisphere r 4.5: a **two-sided** shell (inward lathe, low alpha ≤ 0.35) + a cutout decor display (vine / leaf-sprig pattern inside, bright base rim, light seam, sprout on top; `MP3` §10); brightness 14; scale ≥ 3.3; clips `dome_rise` 10, `dome_idle` L, `dome_pop` 6 |
| wall blade (≤ 15, multi-instance) | one translucent yellow-green leaf blade 2.5-3 b tall with a darker midrib and two cutout "windows"; clips `wall_rise` 5, `wall_fade` 8 |
| summoned stalk ×4 (생명의 손) | 3 displays each (`stalk_low`, `stalk_high`, hooked tip + small gold cone): a pale grey, dark-veined, hooked stalk **5.5-6 b tall**, ≈ 1 b thick (`v1 f1320`); clips `leg_rise` 10, `leg_slam` 6 (hit 4), `leg_sink` 10 |
| seed prop | a small glowing golden seed left at the death spot (cosmetic; removed by cleanup) |
| kit props (AP-FX, not AP-ORG) | thorn wheels (pale green carpet wheels; **gold-orange homing wheels with a red 4-point flare**), seed orbs, leaf pads, rosette petals, light pillars, flood tiles, charge ball |

### 5.4 Budgets

| set | cap |
|---|---|
| rig, both looks | ≤ 0.9 M px, ≤ 7 k / 8 k visible elements (R13, R14) |
| organisms + Heart + domes + walls + stalks + seed | ≤ 0.2 M px; ≤ 500 elements per organism, Heart ≤ 800 |
| kit (AP-FX) | ≤ 0.35 M **new** px; generic rings, discs and card masks are referenced from the fg kit's textures (a read-only dependency the kit build checks), only Apep shapes are painted |
| global | custom items-atlas sum ≤ 15.8 M px with both chapter bosses built (FN-27); otherwise Q27 |

---------------------------------------------------------------------------------------------------

## 6. Clips (`apep_clips.mjs`)

### 6.1 Rules and builder checks

- Authored at footage speed; `RETIME` knots `[authored, played]` speed up wind-ups only. All events below are played ticks.
- No root x / z travel and no root yaw in clips; anchor yaw only through exported schedules (R16).
- Builder checks: events inside the clip; retimed events monotonic; petals and hands never below the floor outside hidden
  spans; P3 upright hood top ≤ 9.0 and **the face visible** (hood hinge ≥ 100° in UPRIGHT); `stand_p3` / `crouch_p3` are
  continuous blends with no body look swap (only the R8 / R12 hand and face events); every visible part top ≤ −0.1 b at
  each hidden-span start; per-clip extents inside the culling box; keys per tick printed per clip (budget: ≤ 49 parts × 1
  key per tick, average ≤ 15 keys / t over a clip).

### 6.2 P3 pose glossary (deliverable of AP-R3, before AP-RC)

The `MO` §5 P3 poses use the superseded "trunk + skirt" body. AP-R3 writes a new glossary on the R2 skeleton with joint
angles: UPRIGHT, CRAWL (= CROUCH with P3 looks), HUNCH (`v6 f780`), MOUND (`v5 f816`), HOOP / wheel (`v5 f930-f951`,
`w1 f96`), SCOIL (`v6 f306`), CURL / BALL (`v5 f1470`, `f2094`), V (`v6 f558-f600`), CROUCH_OVER (the umbrella,
`v5 f1086-f1140`), BELLY_FLOP (`v5 f960`), DEATH_KNEEL. The AP-RC key-pose renders compare against `MP3` sheet 03 for P3;
the `MO` key sheets stay for P1.

### 6.3 Clip table

| clip | authored | RETIME knots | played | next | hidden | looks / hands / brightness | events (played) |
|---|---|---|---|---|---|---|---|
| `entrance_p1` | 110 | — | 110 | idle_p1 | [0,4] | tint `p1_dark` 0 → `p1` 30 | pool 0, hood 16, reach 31, touch 47, flash 60, embers 63, heart_up 70, crouch 91, roar 100, end 110 |
| `idle_p1` | 60 | — | 60 | loop | | | — |
| `turn_p1` / `turn_p1_step` | 20 / 10 | — | 20 / 10 | loop / idle | | yaw schedule (step: 90° in 10 t) | step 0/5/10/15 |
| `crawl_p1` / `crawl_stop_p1` | 16 / 32 | — | 16 / 32 | loop / idle | | hands `curl` on lifts | stepA 0, stepB 8 / plant 8, open 16, end 32 |
| `walk_p1` | 36 | — | 36 | loop | | | step 0/9/18/27 |
| `burrow_strike` | 94 | [0,0] [28,22] [50,44] [76,64] [94,82] | 82 | idle_p1 | [22,44] | `p1_dark` 6, `p1` 44 | tell 0, dive 4, inv 6, sink 8, hide 22, travel 23, lock 32, burst 44, rise 49, loom 52, yawlock 52, sweep 64, sweep_end 71, land 77, end 82 |
| `sink_p1` (relocate) | 18 | [0,0] [5,4] [18,17] | 17 | hold hidden | [14,−1] | `p1_brown` 4 | tell 0, sink 4, chunks 8, hide 14 |
| `emerge_on_p1` | 24 | — | 24 | rotation | [0,1] | scale-in 1-4 | show 1, solid 4, settle 12, end 24 |
| `burrow_in_p1` | 30 | [0,0] [30,23] | 23 | hold hidden | [21,−1] | `p1_dark` 6 | tell 0, inv 5, dive 5, sink 6, hide 21 |
| `emerge_crown_p1` | 40 | — | 40 | idle_p1 | [0,5] | `p1_dark` 5 → `p1` 20 | glow 0, crown 5, hood 10, targetable 11, out 21, end 40 |
| `hands` | 160 | [0,0] [40,30] [82,62] [102,82] [160,140] | 140 | idle_p1 | | swirl yaw 360° over 5-27 | spread 0, swirl 5, raise 27, plunge 30, lock 33, legs 36, lines 40, slam1 62, slam2 69, slam3 75, slam4 82, sink 83, stand 100, pull 108, flower 118, fold 128, end 140 |
| `glow_slams` | 160 | [0,0] [48,36] [59,47] [89,70] [130,101] [160,131] | 131 | idle_p1 | | core 15 in the wind-up | wind 0, coil 23, column 36, slam1 47, rear2 65, slam2 70, leap 77, apex 83, dive 90, slam3 101, settle 121, end 131 |
| `rotation` | 135 | [0,0] [21,16] [135,130] | 130 | idle_p1 | | spin yaw 360° over 47-71 | arms 0, rear 10, disc 16, full 39, crash 40, spin 47, flash 57, spin_end 71, rise 85, stand 100, end 130 |
| `tail_p1x2` | 141 | [0,0] [37,28] [46,37] [66,52] [73,59] [141,127] | 127 | idle_p1 | | sweep yaw 28-35 and 52-59 | turn 0, raise 8, cock 23, swing1 28, end1 37, cock2 48, swing2 52, end2 59, rise 86, end 127 |
| `combo_a` / `combo_b` / `combo_c` / `combo_d` / `combo_end` | 29 / 48 / 20 / 84 / 20 | — / [0,0] [18,14] [48,44] / — / [0,0] [29,22] [84,77] / — | 29 / 44 / 20 / 77 / 20 | chained by the module | | `combo_c` spin yaw 360° over 5-15 | a: tell 0, swing 10, hit 14 · b: rear 0, high 12, slam 17 · c: twist 0, spin 5, hit 10 · d: rear 0, tall 20, lunge 22, slam 27, recover 43 |
| `sink_revive` | 60 | — | 60 | hold, then `park` | [45,−1] | `p1_brown` 20 | stagger 0, flicker 4, sink 20, chunks 30, hide 45, park 46, end 60 |
| `revival` | 160 | — | 160 | idle_p3 (blend 6) | [0,60] | form `p3`, face `p3_idle`, core `p3_sternum` at 0; hands `open` 104 | burst 60, splash 60, reach 88, flash2 96, reveal 100, end 160 |
| `idle_p3` / `turn_p3` | 60 / 20 | — | 60 / 20 | loop | | | — / step 0/5/10/15 |
| `walk_p3` (crawl gait) | 32 | — | 32 | loop | | | step 0/8/16/24 |
| `crouch_p3` (UPRIGHT → CROUCH) | 8 | — | 8 | hold | | hands `curl` 2, face `hidden` 6 | closed 6, end 8 (`v6` 7 t) |
| `stand_p3` (CROUCH → UPRIGHT) | 14 | — | 14 | idle_p3 | | face shown 4, hands `open` 5-8 | open 10, end 14 (`v6` 14 t) |
| `move_strike_p3` | 100 | [0,0] [22,16] [52,44] [100,92] | 92 | idle_p3 | [16,42] | starts UPRIGHT (fold 0-7), ends UPRIGHT | fold 0, mound 8, inv 8, hide 16, trail 16, lock 32, show 42, burst 44, hoop 44, roll 49 (pitch keyed 49-61), slam 61, tail 65, sweep 69 (yaw 66-72), rise 71, stand 85, end 92 |
| `aftermath` | 240 | [0,0] [52,40] [84,68] [172,156] [240,224] | 224 | idle_p3 | | bright 15 at 0; face `p3_charge` 18 → `p3_idle` 189; starts CROUCH, ends UPRIGHT | charge 0, whirl 18 (yaw 360° over 18-36), land 40, field 40, pillar1 44, pillar2 48, pillar3 52, dome1 54, dome2 58, dome3 62, rise 76, ticks 80, aloft 84, rain 134, blast 156, descend 162, window_end 176, pop 189, burst 190, end 224 |
| `shells` | 140 | [0,0] [46,35] [56,45] [120,93] [123,96] [140,113] | 113 | idle_p3 | | bright 15 at 14-35, 13 from 48 | hunch 0, ring 10, lit 14, lock1 33, launch 35, ball 36, hit1 45, cool 48, lock2 79, lock3 82, hit2 93, hit3 96, end 113 |
| `sink_p3` (Q3s) | 20 | — | 20 | hold hidden | [12,−1] | starts UPRIGHT (fold 0-7) | fold 0, inv 8, sink 8, hide 12, end 20 |
| `surface_p3` (Q3s) | 40 | — | 40 | (stand_p3) | [0,0] | crawl stance; bright 15 at 0-10 | show 0, splash 0, charge 0, launch 10, hit 12, recover 12, end 40 |
| `tail_p3` | 100 | [0,0] [14,11] [18,15] [58,45] [62,49] [100,87] | 87 | idle_p3 | | starts CROUCH, ends UPRIGHT (stand 57-87) | crouch 0, cock 3, swing1 14 (yaw 14-21), rise 24, coil 36, lunge 36, swing2 46 (yaw 46-53), rise2 57, end 87 |
| `spikes` | 84 | [0,0] [49,37] [54,42] [84,72] | 72 | idle_p3 | | bright 15 at 10-48 | curl 4, rise 10, column 14, summon 19, lockA 37, fireA 42, lockB 43, fireB 48, hitA 49, blades 52, hitB 55, skim 64, recover 65, end 72 |
| `death` | 120 | — | 120 | — (blend 6) | [118,−1] | face `p3_dim` 30, hands `curl` 55, tint `withered` 85 | hit 0, flicker 8, droop 30, kneel 55, fall 70, land 82, wither 85, sink 100, gone 118, end 120 |

Removed from the draft: `tail_p1` (single swing, unsourced), `move_strike_p3s` (misread clip), `tail_flick_p3`.
The summoned-stalk clips belong to the org manifest (§5.3).

---------------------------------------------------------------------------------------------------

## 7. Mechanics

### 7.1 Resistances (U2)

| entity | Dendro | others | how |
|---|---|---|---|
| Warden, phases 1 and 3 | 30 | 10 | registry `"res": {"7":30,"*":10}` → the body's per-element scores (FN-7), applied before the module `on_hit` |
| organisms (all 6) | 20 | 10 | per-entity `mbRes7 20`, the rest 10, set right after `aux/spawn` (FN-7). Fallback without FN-7 for aux: `#auxRes 10` + `aux_hit` ×8/9 on Dendro (at least 1) |
| 양육 while it holds ≥ 1 link | immune | immune | `aux_hit` branch: `#dmg 0`, `#mbAuxDone 1`, "면역" popup (reading A, Q1) |
| shielded basic (수호) | the shield pool absorbs first | | `aux_hit`: pool `apShd` = 5 × the basic's max HP; Pyro ×1.5 against the pool |

True damage (tests) bypasses RES. Reactions and DoTs re-enter `combat/apply` with their own element, so they are covered.
The gate label prints "내성: 풀 30% · 그 외 10%". A Nefer (Dendro) player deals ×0.70 instead of ×0.90: intended
counter-pick pressure.

### 7.2 HP layout, phase flow, reload

| item | value | how |
|---|---|---|
| total pool | ≈ 7235 at L18 (hp 290; the build prints the exact value) | `#mbTot` at spawn (FN-4); `#apTot` mirrors it |
| P1 pool | 53 % ≈ 3835 | `mboss/repool {pct:53}` at spawn |
| P1 floor | 1 % of the P1 pool ≈ 38 HP | the module `incoming` sets `#mbFloor` and calls `mboss/floor` (FN-5); reaching it sets `#apTr 1`; a running pattern ends at its `release`, then T1 runs at the next decision point; a popup "…" at most every 10 t while clamped |
| P2 | no boss damage; the body is **parked 30 b above the centre** (NoGravity, `rlk_mb_inv`, rig parked, `#mbNoLeash 1`), keeps `rlk_zmob` so the zone cannot clear, and stays the bars carrier | §7.5; bow arrows and aim assist would otherwise hit an invisible body at the Heart for ≈ 100 s |
| P3 pool | 47 % ≈ 3400 | `repool {pct:47}` inside the CS white-out; floor 0 → normal death → chapter clear |
| organism pools | ‰ of `#apTot` (never of the current pool) | §9.4 |

- `test/level` re-applies the current phase's split through `repool` (FN-4).
- Short burrows (P1 잠복 돌진 / 발광 / R / T1 sink, Q1, Q3s): `rlk_mb_inv`, proxies `burrowed`, husk scale 0.1 +
  `rlk_mb_noshield` (FN-13); the anchor never enters blocks.

Reload, pause and cleanup per phase (`init` kills every `rlk_mb_aux` and `reload` resets `#mbNoLeash`, so the module
rebuilds everything from scores):

| phase | `/reload` | pause | cleanup / uninstall |
|---|---|---|---|
| E | skip to the end of E (boss in idle, the Heart drawn up) | freezes | kills all Apep entities and props |
| P1 | rig respawn (look `p1`, CROUCH), proxies `p1`, the drawn-up Heart prop, cancel the pattern → idle | freezes (framework) | as above |
| T1 | jump to "phase 2 ready": park the body, cradle + Heart in place, wave 1 | freezes | as above |
| P2 | keep `#apHt`, the wave index, the stage clock, the strikes; respawn the Heart displays; clear walls (recorded + safety sweep); respawn the current wave (markers 20 t); park again with `#mbNoLeash 1` | walls cleared (re-cast later); organisms freeze (NoAI husks, the module tick does not run) | kills organisms, walls, Heart |
| CS | jump to "phase 3 ready": lush look ensured, pool 47 %, title, rig `p3` UPRIGHT at the centre, unparked | freezes | as above |
| P3 | rig respawn (`p3`, UPRIGHT), cancel the pattern; a running Q2 is cancelled (domes removed, cooldown 300 t) | freezes; a running Q2 is cancelled on resume the same way | kills domes and props |
| D | finish the death (`cb/won`) | freezes | — |

### 7.3 Targeting, zones, facing, locomotion, clamps

- **Body frame** (FN-20 `mv/local`): f along the facing from the anchor (the thorax base), s sideways.

  | zone (P1 and P3 crawl) | condition (b) | meaning |
  |---|---|---|
  | FRONT | f ≥ 3.0 and \|s\| ≤ 4 + 0.6 (f − 3.0) | before the hood (front 4.0) and the front hands (the wiki's safe spot) |
  | SIDE | \|s\| > 3 and −3 ≤ f < 3.0 | beside the long arms (claws at ±5.3) |
  | UNDER | \|s\| ≤ 3 and −3 ≤ f < 3.0, outside the capsules | the ring between the capsules (R11) and the legs |
  | BACK | f < −3 | behind the hips / along the tail (to f −12) |

  Bands from the anchor: P1 near ≤ 7.5 (the 초목 disc r 9 covers it), mid 7.5-14, far > 14. P3 upright: bands only (near
  ≤ 6, mid 6-14, far > 14); no BACK rule (the tail coils round the stem).
- **Facing.** The anchor yaw is the facing. P1: idle tracking `mv/turn {max:3}`; a crab-turn step (`turn_p1_step`, 90° in
  10 t) when |Δyaw| > 60° at idle; front patterns (P1 sweep, P2 aim, P6) pre-turn up to 10 t (`Pattern.lead`). P3:
  tracking 3°/t, turns ≤ 6°/t. Patterns lock their yaw at their lock tick.
- **Locomotion.** P1 crab crawl (`crawl_p1`) ≤ 0.25 b/t for ≤ 40 t when the player is far, or after P1 lands far from the
  centre; side walk 0.12 b/t (`walk_p1`) when mid. P3 upright never walks; it repositions in the crawl stance only as the
  opener of Q4 (player > 8 b: `crouch_p3` + `walk_p3` ≤ 30 t at 0.2 b/t) and before Q2 (to the centre at 0.4 b/t, ≤ 50 t).
- **Clamps** (anchor destinations per form, separate from hazard locks): P1 idle ≤ 14 b from the centre (the 12 b of tail
  behind stays inside walk 26), burst / emergence points ≤ 18, glides end ≤ 16, then the leash brings it back at 0.13 b/t;
  P3 idle ≤ 14, burst points ≤ 16. Locked ground targets clamp to the walk disc (r 25.3).
- **Anti-stall.** If the player stays in BACK for ≥ 3 decisions while P5 is cooling down, the next decision is a 180°
  crab-turn.

### 7.4 Pattern choice

Decision order at each pattern boundary (template `fgcore:492-589`):

```
test request > lock > transition queued (#apTr) > chain pending (P3) > 종말의 여파 due (P3)
  > BACK rule (P1) > weighted pick by zone and band, no immediate repeat (#apLast), cooldowns > fallback
```

- **BACK rule (P1):** counts only if the player was in BACK for ≥ 20 of the last 30 t (`#apBackT`, sampled every 10 t);
  then 75 % → P5 if it is off its 200 t cooldown. **Rim rule:** if the anchor is beyond r 12 and the player is BACK, the
  boss prefers a crab-turn or P1 for that decision (a player between the tail and the rim could not walk out). First
  BACK tail of the fight shows "꼬리 뒤는 위험합니다 — 정면에 서세요".

Phase-1 weights (0 = never):

| pattern | FRONT near | FRONT mid | FRONT far | SIDE / UNDER | BACK (the other 25 %) | rules |
|---|---|---|---|---|---|---|
| P1 잠복 돌진 | 1 | 3 | 4 | 2 | 2 | cooldown 400 t |
| P2 생명의 손 | 1 | 3 | 3 | 2 | 2 | — |
| P3 발광하는 파수꾼 | 2 | 2 | 2 | 2 | 2 | cooldown 700 t; first allowed after 3 patterns |
| P4 초목이 시든 풍경 | 4 | 2 | 2 (+ R) | 4 | 2 | R first when the player is > 9 b away |
| P5 생명의 꼬리 | 0 | 0 | 0 | 1 (SIDE with f < 0) | rule | always two swings (Q8) |
| P6 근접 콤보 | 4 | 1 | 0 | 1 | 0 | length 2 / 3 / 4 hits, weights 3 / 4 / 3 |

Phase-3 weights: Q1 near 1 / mid 2 / far 3; Q3 near 1 / mid 3 / far 3; Q4 near 3 / mid 2 / far 1 (the reposition opener
when > 8 b); Q5 2 / 2 / 2.

- **Chains** (`V5` M2, `V6W` take 3): after Q5, 40 % → Q1; after Q3, 30 % → Q3s (the surfacing shot). A chain starts ≥ 20 t
  after the previous pattern's last hit (one dash recharge); never two chains in a row.
- **Q2 schedule:** first use after the first P3 pattern; then due when ≥ 900 t of fight time have passed since the last one
  **and** ≥ 3 other patterns ran in between; forced at the next decision point when due. Expected 2-3 uses per fight.
- **Recover** (idle punish window) per pattern in §8.

### 7.5 T1 소생 단계 진입 (136 t; `ME` §2.2, `V2` H)

| t | event | implementation |
|---|---|---|
| 0 | sub-line "종막 오아시스 파수꾼이 땅속으로 숨어듭니다…"; `mboss/cine/start` (FN-22) | `line/say` |
| 0-45 | rig `sink_revive` where the boss stands (stagger, core flicker, splay, sinks as root chunks with gold glints) | rig + kit root-chunk burst |
| 6 | `rlk_mb_inv`, proxies `burrowed`, husk scale 0.1 + `rlk_mb_noshield`, `#mbNoLeash 1`; `lib_clear` (hazards, pj, pull, mv of phase 1) | framework |
| 45 | `rig/park`; the body is parked 30 b above the centre | R10, §7.2 |
| 45-65 | the **cradle rises** at the centre (pedestal look: pale petal clumps + 3 gold sprouts; root-chunk fx), the gold swirl decal appears | `cradle_rise` |
| 50-100 | the Heart (egg look, scale 0.7, upright) is lowered by the vine hand from y + 20 to y + 3, swaying 1-2 b | `heart_lower` (`V2` 35.4-38.3 s) |
| 100-106 | the egg drops into the cradle; it scales 0.7 → 1.0 and pitches to lying through the squash; green-gold light beam 10 t; the cradle switches to its full look | `heart_drop` + kit beam |
| 106 | HUD swap: title 「오아시스의 심장」 (FN-6), the gold progress bar ramps 0 → 27 % in 10 t; music → 2 (FN-23) | FN-24 |
| 108 | "마물을 처치해서 소생 진행도를 올리세요" (sub-line + actionbar, 100 t); `cine/end` | |
| 116-136 | wave-1 spawn markers (pale wireframe domes) | kit decal |
| 136 | wave 1 emerges; the stage clock starts | §7.6 |

### 7.6 Phase 2 — the revival stage, tuned for one player

#### 7.6.1 The Heart of the Oasis (objective)

- Marker `rlk_mb_ap_heart` (tags `rlk_room rlk_mb_aux`) at the centre + the §5.2 displays. **Not `rlk_mob`**: player
  attacks never touch it.
- Progress `#apHt` in ‱, clamp 0..10000; ≥ 10000 → CS (§7.7); ≤ 0 → failure strike (§3.4).
- Events `heart/add {v}` / `heart/sub {v}`: gain = `heart_gain` sparkle + `block.amethyst_block.chime` (pitch rising with
  progress); loss = `heart_hit` flinch + red-gold motes + `block.amethyst_block.hit` p 0.6 v 0.4. The bossui's white
  recent-loss trail shows losses by itself.
- Hits on the Heart are **module events**: a melee basic subtracts at its strike tick; a ranged bolt when the module ends it
  within 1.5 b of the Heart. A player in the bolt's path takes the bolt and the Heart is spared (body-blocking).

#### 7.6.2 The economy (`api.REV`, one table the balance fixer tunes)

| knob | value | wiki / footage | why |
|---|---|---|---|
| start / win | 2700 / 10000 ‱ | ~27 % (measured 25.3 %) | kept |
| basic kill / any other kill | **+325 / +1400** | +1.75 % / +11 % | a party clears a wave in one AoE burst; one player kills 4-5 s per basic. Solo version of the same wave value |
| basic hit on the Heart / buffed hit | −60 / −120 | −0.6 % / −1.2 % | kept (the visible drain and the idle fail) |
| 파괴 blast | −1400 | −14 % | kept |
| **attack slots** | at most **3 basics damage the Heart at once** (the 3 cradle sockets for melee; a ranged basic in its firing loop counts too); the others wait on r 4.5 or lie idle | `v3` B / D: three basics hug the cradle | bounds the drain for slow players, still felt by fast ones |
| cap | **6** organisms alive (a due wave waits; time-out spawns ignore the cap) | — | the forced waves were the spiral's amplifier; also the command budget |
| wave clock | next wave when the previous has ≤ 1 alive, or **30 s** after it | — | |
| time-out | **100 s** into the stage: warning, then 1 파괴 per **30 s**, at most **1 alive** | the wiki's punisher | pressure without a loop |

Re-simulated with the critic's phase-2 model (`S:ap/plan_work/var_rev2.py`, config W7 at hp 320; 20 seeds per row): the
idle agent fails in ≈ 40 s; the plan agent wins 20 / 20 with every build from 0.6× sword DPS up (sword ×0.6 ≈ 168 s,
catalyst ≈ 183 s, item-less sword ≈ 105 s, bow ≈ 106 s, sword ×1.75 ≈ 65 s, bow ×2.5 ≈ 36 s); the hint-ignoring agent wins
20 / 20 (sword) and 19 / 20 (bow). The real `apfair.py` confirms or retunes (§9.7).

#### 7.6.3 Waves, spawn points, time-out

| wave | content |
|---|---|
| 1 | 4 basics (2 melee, 2 ranged) at the stage start (T1 t136) |
| 2 | 4 basics + 수호 |
| 3 | 4 basics + 둥지 |
| 4 | 4 basics + 양육 |
| 5 | 4 basics + 포식성 (it swallows one) |
| 6+ | 4 basics + 1 special from a shuffle bag {수호, 둥지, 양육, 포식성}; from wave 7 two specials |
| time-out | 파괴 only (Q7: the wiki's punisher; test id 28 teaches it) |

- Spawn points: the 8 points on r 12; never closer than 4 b to the player; a wave spreads over 3-4 points. 수호 and 파괴
  spawn at the point whose distance from the player is nearest 10 b; 둥지 at the point nearest the player; 포식성 at the
  farthest; 양육 on the r 7 point of the bearing nearest the basics' cluster (5-6 b from the cradle basics).
- Each spawn = a 20 t wireframe marker + a 10 t emergence; untargetable until solid.
- Warning: title "!" + "오아시스의 심장이 위험합니다" (gold / red) + sub-line "파괴의 증식 생명체가 나타납니다";
  `event.raid.horn` at low volume. The under-bar shows the time left to the warning (gold), then red.
- Expected length (hp 290): item-less sword ≈ 95-110 s, typical chapter-3 items (×1.75) ≈ 55-65 s.
- Drain if ignored: 3 slots hitting every 40-50 t ≈ 0.9 %/s → 27 % lasts ≈ 35-45 s.

#### 7.6.4 The organism runtime (`org.py`, on the framework `aux`)

| part | rule |
|---|---|
| entity | `aux/spawn` husk (`rlk_mob`, overhead HP bar, boss level, never `rlk_zmob`), tags `rlk_mb_ap_org rlk_mb_ap_<kind>`, `apK` = kind 1-6; model passengers from AP-ORG tagged `rlk_room rlk_mb_aux` so every cleanup path removes them |
| HP / RES | `#auxHp` = `#apTot` × ‰ / 1000 (§9.4); per-entity RES (FN-7) |
| passengers | facing by `rotate` on the passengers; models translate ≈ −2 b to the feet; the 5 HP-bar displays get the kind's y offset by `data merge` after spawn; the click shield gets the kind's size (FN-29, else `data merge` on the `rlk_mshield` after its first tick) |
| tick | `execute as @e[type=husk,tag=rlk_mb_ap_org] at @s run function rlk:mboss/apep/org/tick` → dispatch on `apK` → the kind's state machine on `apS` / `apT` |
| movement | module stepping (FN-30 or a module copy): face the target, `tp ^ ^ ^v`, y snapped to 201, clamp to the walk disc and outside the Heart footprint; steps may alternate ticks (the husk interpolates over 3 t) |
| attacks | framework `hz/*` and `pj` with the organism as `@s` (knockback source), so the fairness sim sees them |
| kills | the module tick reads `rlk_mb_broken` → progress, death clip, energy particles (`function rlk:char/particles {n:1,el:7}`; 파괴 n 4), then `kill` (passengers first). Aux kills pay no XP / gold / heal orbs. Never `true_hit` an organism (it would run the reward path); every "loses 40 %" / "self-destructs" is module-side `mhpC` + the module break |
| pause / reload / cleanup | §7.2; `cleanup` / `death_start` / CS / failure kill every organism (`cleanup_aux`) |
| budget | ≈ 9 entities per organism (≤ 54 at the cap) + Heart 9 + walls ≤ 15; **≤ 800 commands / t average** at the cap including `mob/tick`, bars and kit (measured by the real-engine probe, §12) |

#### 7.6.5 AI per organism kind (timings ours)

| kind | behaviour |
|---|---|
| 기본 basic | Assigned melee or ranged at spawn (wave 1: 2 + 2; later 50 / 50). Walks at **0.12 b/t** (bell look, bobbing). **Melee** goes to a free cradle socket (r 3.4; others wait on r 4.5) and, holding an attack slot, attacks every **40 t**. **Ranged** stops on **r 11-13**, lies down (bag look) and, holding a slot, fires every **50 t**. Never chases the player (the Heart is the first priority). |
| 수호 guarding | Immobile. Cast 30 t (`guard_cast`); shields every basic within r 10 at the cast and every basic that finishes emerging within r 10 while it lives; recasts every 240 t on unshielded basics in range. First-time hint "수호의 증식 생명체를 먼저 처치하세요". Death (17 t) removes every shield at once. |
| 둥지 nesting | Hovers 1 b up and keeps 4-8 b from the player at 0.15 b/t, flapping; blinks to 5 b from the player when > 12 b away (6 t, kit flash). Casts walls every **160 t** (first 60 t after spawn), never while a 파괴 is within 6 b of the Heart or fusing, and never during a 포식성 bite chain. No attack. |
| 양육 nurturing | **Stationary** on its r 7 spawn point (`v3` §3.C). Link tell 20 t; links **up to 3** basics within r 10 (nearest first): they get the `buffed` look, Heart hits −120 and the buffed coefficients of §8.2. **Immune while ≥ 1 link holds** ("면역"; reading A, Q1; the translucent cylinder shows it). Each linked basic that dies or is swallowed costs it **40 % of its max HP** (module `mhpC`, the module break); the 3rd breaks it ("자멸", +1400). Re-links a free slot to a new basic in range every 80 t. With no link and no basic in range it is plainly damageable. First-time hint "강화된 기본 증식 생명체를 처치하면 양육의 증식 생명체가 자멸합니다". |
| 포식성 predatory | Fish swims at 0.15 b/t, 1-1.5 b up, to the nearest basic; **swallows** it at ≤ 1.5 b (`pred_swallow`: rear 0-6, scoop 6-12, the basic removed at 12 with no progress; a buffed one costs its 양육 40 %); bud 20 t (core lit); **inflate 10 t (tell) → burst**; then circles the player at 3-5 b for 40-60 t; **chain 1** (4 bites at +12 / +18 / +24 / +30, each sector locked and drawn 10 t before its strike, lunge 1.5 b each) → 14 t → **one single bite** (tell 10) → 12 t → **chain 2** → single bites every 60 t. With no basic to swallow it skips the burst and bites at ×0.7. First-time hint "포식성 증식 생명체가 연속으로 물어뜯습니다 — 거리를 벌리세요". |
| 파괴 destruction | Rolls to the Heart at **0.10 b/t** (≈ 95 t from r 12); stops against the Heart at r 2.6 (off the socket bearings); **fuse 56 t** (face pulses every 9 t, every 4 t in the last 20 t; `entity.creeper.primed` p 1.4 at contact), suck-in 5 t, **blast at contact + 61**. Killed before: +1400 + energy particles n 4. First-time hint "파괴의 증식 생명체가 심장에 닿기 전에 처치하세요". |

#### 7.6.6 Links, shields, buffs, swallow

- A basic is at most one of: free, shielded (수호), buffed (양육). A shielded basic can still be linked (both looks); the
  hint order (수호 first) solves it.
- **Shield pool** `apShd` = **5 × the basic's max HP**; absorbs before HP; **Pyro ×1.5** against it (a Pyro player still
  kills the 수호 faster than one shield); the number shows sky-blue (the module takes the number with `#mbAuxDone 1`) +
  `item.shield.block` p 1.6 v 0.4; the overlay display (§5.1) pops when the pool breaks.
- **Buff links** are stored as `apL` on each linked basic. A killed or swallowed linked basic sends one "link lost" event
  to its 양육.
- **Swallow** hands the basic to the predator: killed silently (no progress, a gulp, no burst) and its link event fires.

#### 7.6.7 Nesting walls (barrier blocks)

- Cast: tell 12 t (`nest_cast`: limbs curl into a vertical loop); the wall spots are locked at the tell start and drawn as
  kit decals at once. Default: **3 groups 120° apart at r 4.2 around the locked feet**, each 3 leaf blades over a 60° arc,
  2.5 b tall; variant (30 %): one arc of 3 blades 3.6 b ahead of the player's facing ("3 at once in front").
- Blocks: `minecraft:barrier` at y 201 and 202 under each blade, placed with **`replace air` only**. At the rise tick the
  module skips every block that intersects the player's body box (x ± 0.3, z ± 0.3, y 0..1.8) plus 1 b of margin, every
  block within 1 b of an organism, and every block inside the Heart's wall-exclusion radius. At least two 60° gaps stay;
  only inside the walk disc; only in phase 2.
- **Each blade group's marker records its blocks**; the dissolve clears exactly those. A safety-net sweep from the chapter
  mode (FN-26: per-row span table limited to r ≤ 25.5, y 201..202, never a rectangle) runs in `pause`, `reload`,
  `cleanup`, `death_start`, `uninstall`, the CS, a failure strike, `cb/won` and `room/remove`. The rim barrier is never
  touched.
- Life 40 t, dissolve 8 t (`wall_fade` + motes). **No damage.** Barrier is not in `#rlk:dash_pass`, so walls stop
  movement, dashes, knockback and **player arrows**; framework projectiles fly through (`#rlk:cm_pass`); the camera
  passes (`#rlk:view_pass`).
- Fallback without blocks ("soft walls": push the body out of blade boxes) only if barrier collision breaks the
  shoulder-view avatar in game (Q15).

#### 7.6.8 Phase-2 HUD (Korean)

| line | content |
|---|---|
| 1 name (`rlk:mboss`) | "「오아시스의 심장」" (gold) + badges of the specials alive (e.g. "  ◆수호" in its colour) + "  4웨이브" |
| 2 bossui (`rlk:mboss_state`) | the progress bar: `#buHp` = `#apHt` / 10, `#buMax` 1000, gold `#EDCF63` (`#buHpCol`), numbers off (`#buNoNum`; fallback `#buMax 100`) (FN-24); under-bar = time to the warning (gold), red after it |
| 3 sub (`rlk:mboss_sub`) | "마물을 처치해서 소생 진행도를 올리세요" → "소생 진행도 47%" + first-time hints + "⚠" after a failure strike |
| title / actionbar | stage start, warning, 「소생 실패」 + "다시 한 번 실패하면 쓰러집니다", success "오아시스의 심장이 소생했습니다" |

### 7.7 CS — the 2→3 cut-scene (192 t; w2, `V5` CS)

| t | event | implementation |
|---|---|---|
| 0 | progress reaches 10000: every organism wilts (green pulse ring r 0 → 26 over 20 t; they burst, no progress); walls cleared; `lib_clear`; `cine/start`; sub-line "오아시스의 심장이 소생했습니다" | FN-22 |
| 0-24 | the Heart blazes; the egg lifts out of the cradle dripping gold (`heart_lift`) | AP-ORG |
| 24-64 | **white-out** (kit full-screen white glyph on the title line, 40 t; no Blindness, no FOV change): arena look → `lush` in ≤ 24 slices + the lush props; cradle and ley-line decals removed; the body unparked to the centre at root −6 (hidden), `repool {pct:47}`, rig look `p3`, stance UPRIGHT; players within 8 b of the centre pushed out to 12 b (`push/ring`, FN-21) | FN-3, FN-4 |
| 32 | rig `revival` starts while hidden (its hidden span 0-60 = CS t32-92) | rig |
| 64-76 | white fades; the egg hangs high over the centre (y + 10); **the 「불씨」 ember**: a spark arcs from a twig on the bank into the egg (kit card + `block.fire.ambient` p 1.6 v 0.3) | w2 S2 |
| 76-84 | the vine hand wraps the egg; it turns green (`egg_green`) with green lightning ribbons; **green flash at t80: the player heals 25 % max HP** through `mboss/player_heal` ("오아시스의 심장이 생명을 나눕니다"; Q25) | w2 S3-S4 |
| 92 | the Warden **bursts out of the water** at the centre in a leaf splash (`revival` burst); the orb fades into it | rig + kit |
| 120-132 | `revival` reach (t120) / flash2 (t128) / reveal (t132); title "기원 오아시스 파수꾼" / "「불씨」를 받아 소생한 생명" (FN-6) at t132; bars refill over 30 t; music → 3 | FN-23 |
| 150 | targetable, proxies `p3u`; `cine/end` | |
| 192 | `revival` ends (→ `idle_p3`); first P3 decision | core |

A reload mid-CS jumps to "phase 3 ready" (§7.2).

### 7.8 Phase 3: stances, 종말의 여파 schedule, domes

- Start: `#apPh 3`, pool 47 %, title swap, RES unchanged, floor 0, proxies `p3u`, stance UPRIGHT.
- **Stances**: UPRIGHT for idle, Q3, Q5, Q2's cast; CROUCH (crawl) inside Q1, Q3s, Q4, the walks. `crouch_p3` (8 t) /
  `stand_p3` (14 t) play between; proxies rebind (`p3u` ↔ `p3c`) on the stance events; the face hides in the crawl.
- **Domes (the shelter)** — 3 per cast, **r 4.5** (never shrunk, U5; the sim may raise it to 5.0). Each dome = a marker
  `rlk_mb_hzsafe` (`mbHzSG` = the cast's safe group, FN-14) + `rlk_mb_ap_dome` + the §5.3 displays + a rim decal + a 10 t
  light-pillar tell. **Footprints (pale rim rings) appear with the banner**, before the walk.
- **Placement** (fix 10-22f, user 10-22: random, not an equilateral triangle, further apart; was A on θ at 7 b, B / C at
  ±120° on r 14 or B near a far player, ≥ 9 b apart): at the banner, one of 12 precomputed layouts of the player's 3-b
  distance band (`aftermath.LAYOUTS`, `random value`), in the frame at C facing the player: centres 7-17.4 b from C (the
  dome edge ≤ 21.9 b, clear of every arena prop and inside the walk radius), **14-30 b apart**, never near-equilateral
  (the three distances not within 15 % of each other, the angles not all 60 ± 10°), the player's dome (dome 0, forming
  first) ≤ 9 b from the player anywhere inside the walk radius (≤ 9.3 b at the barrier).
- **Damage outside every dome** (FN-14 / FN-15 mask hazards: Dendro, `#hzNoDodge`, `#hzNR`): (fix 10-22f) the field is
  laid at the banner and **ticks 2 % max HP every 10 t from 20 t after the banner** to the tick before the blast (15-20
  ticks = 30-40 % max HP for a player who never enters a dome; non-lethal), the domes forming 34 / 38 / 42 t after the
  banner, so the first two ticks find nobody inside (was 3 % every 15 t, t80-155, ≤ 5 ticks); the **blast 80 % max HP**
  with a 20 t active window (lethal; **the first cast of each fight cannot kill**). Shields absorb as usual. Inside a
  dome: nothing, and **1 % max HP healed every 20 t** ("소생의 찬가"; Q25).
- Fallback without FN-14 / FN-15 (option b): one `dmg 0` mask hazard for the fairness agent to read + the module's dome test
  (Raiden's horizontal `dome_contains`) calling `pl_dot` at the tick and blast ticks.
- The wiki quirk (the domes vanish early when the boss is knocked down) is skipped: we have no poise system.

### 7.9 Death

`death_start`: `lib_clear`, domes removed, `cine/start`, bars hidden, music stopped; rig `death` 120 t; then a small
glowing golden seed prop at the spot (cosmetic, removed in cleanup); the chapter clear follows (`cb/won`).

### 7.10 Dodge rules, undodgeables, reactions, jump bands

- Dash i-frames (`dashInvT 6`, 2 charges, 20 t recharge, ≥ 5 t between dashes) dodge every hazard except the
  **undodgeable set**: the homing thorn wheels (`#pjNoDodge`, chip damage), the 종말의 여파 ticks / blast (the dome is the
  answer), the 소생 실패 wither. 생명의 꼬리 is "hard", not undodgeable. A dodged hazard is spent; a dodged member of a
  volley group does not disarm the group.
- Hazards test the feet in a height band (default −0.5 … +3.5 b). **Every hazard documented as jumpable uses `#hzY1 7`**
  (the 발광 wheel carpet, the 이동 돌진 tail sweep, the 생명의 나선 blades, 근접 콤보 hit 3); a moving front's band passes
  a standing player in ≤ 3 ticks.
- Every boss and organism hit is Dendro: a Hydro-aura player gets Bloom, Pyro gives Burning (as the butterfly). Skipped
  (`#hzNR` / `#mbNoRx`) only for the 종말의 여파 hits and the failure wither (Q13).

### 7.11 Global pattern rules (checked by `pat_*` static tests)

1. **Telegraph honesty**: every ground decal has exactly its hazard's size and time; bursts or splashes larger than the
   hazard are airborne-only fx (no ground decal beyond the hazard).
2. **Telegraph floor**: ≥ 10 t for every damaging hit; lock-on telegraphs use `tell_rt(t) = max(10, round(0.75 t))`.
3. **Fast sweeps are per-tick swept wedges**: on each tick of a sweep a `hz/sector` covers exactly the angle swept that tick
   (from the manifest's tail track × the exported yaw schedule), all in one volley group: one hit at most, at the tick the
   wedge reaches the player. A grid of standing players over the lane must all be hit once.
4. **Dash budget**: in any 40 t window at most 2 hits may be dash-only (tell < (escape distance + 0.3) / 0.216 t and not
   jumpable), ≥ 6 t apart; every other hit is walk-escapable or jumpable at `#hzY1 7`.
5. **Burst groups**: the merges listed per pattern in §8; gates in §9.7.
6. **Projectile speeds** are multiples of 0.25 b/t (`pj/tick` steps); life = ⌈distance / speed⌉ + 2; landings that matter
   are hazards with their own decal.
7. **Locks**: `lockv {lead}` (FN-19) ignores samples with `dashMoveT > 0` and caps the measured speed at sprint
   (0.28 b/t); `lockp` = the position at the lock tick; `lockb` = a point relative to the player.
8. **Chains** start ≥ 20 t after the previous pattern's last hit.

---------------------------------------------------------------------------------------------------

## 8. Pattern spec rows

Per pattern: trigger, timeline (played ticks from the pattern start), hazards (shape, size ×1.2 of the footage, tell,
height band, group, coefficient in % of the registry atk / 100, flags), dodge, telegraph and fx, vanilla sounds, helpers.
Every boss hit is Dendro (el 7). Kit preset names are proposals for AP-FX (`ap_fx_api.md` §0). Coefficients are the
starting values; the fairness pass sets the final ones (§9.7). Raw values per coefficient are in §9.2.

### 8.0 Wind-up and area summary (U4, U5)

| pattern | wind-up footage → ours (t) | telegraph of each hit (ours, t) | area footage → ours (b) |
|---|---|---|---|
| P1 잠복 돌진 | tell + dive + sink 28 → 22; burst → sweep 26 → 20 | burst 12 (footage 6), sweep 12 | burst r 3.5 → 4.2; sweep 9 × 3 → 10.8 × 3.6 |
| P2 생명의 손 | spread + swirl + raise 40 → 30 | plunge 30, strips 22 / 29 / 35 / 42 | splash r 3.5 → 4.2; strips 7 × 2.5 → 8.4 × 3.0; stalk ring r 5.5 → 6.6 |
| P3 발광하는 파수꾼 | coil wind-up 48 → 36 (+ the footage's 60 t idle turn → 10); slam gaps 30 → 23, 41 → 31 | 30 / 23 / 31; carpet front visible | slam r 4.5 → 5.4 (blade rays r 7.2 airborne); carpet r 12 → 14.4 |
| P4 초목이 시든 풍경 | arms + rear 21 → 16; **disc fill 23 kept** | 24 | r 7.5 → 9.0 |
| P5 생명의 꼬리 | raise + cock 37 → 28; swing gap 29 → 24 | 14 / 13 (lanes) | r 9.5 → 11.4, h 2.5 → 3.0 |
| P6 근접 콤보 | 10 → 10 (floor), 18 → 14, 5 → 10 (decal), 29 → 22 | 10 / 14 / 10 / 22 | 130° r 6 → 156° r 7.2; r 5.5 → 6.6 ×2; ring r 6 → 7.2 |
| Q1 이동 돌진 | sink 22 → 16 | burst 12, slam 15, sweep 21 | burst r 3 (`v6` surfacing) → 4.2 (= P1 burst); slam r 4.2; sweep r 10 → 12 |
| Q2 종말의 여파 | charge 52 (v5) / 101 (w1) → 40 | footprints from the banner (≥ 156 t), domes formed ≥ 130 / 126 / 122 t before the blast (fix 10-22f; was 102 / 98 / 94) | domes r 4.5 (not shrunk) |
| Q3 증폭의 풀 | launch 46 → 35; shell 1 → shells 2 / 3 gap 64 / 67 → 48 / 51 | 12 / 14 / 14 | beam 3 → 3.6; bursts r 2.5 → 3.0 |
| Q3s 수면 포격 | surface → shot 4 → 10 (floor) + 2 t flight | splash 10, shell 12 | splash r 3 → 3.6; burst r 2.5 → 3.0 |
| Q4 생명의 꼬리 | cock 14 → 11; swing gap 42 → 32 | 12 / 14 (lanes) | reach 10 → 12 |
| Q5 생명의 나선 | to the glint 49 → 37 | 12 / 12 / 12 | spike r 1.75 → 2.0; cluster r 4.5 → 5.6 (scatter 3.6 + spike 2.0); blades 2.2 wide |
| organisms | basic ranged crown 12; 수호 cast 39 → 30; 포식성 inflate 8 → 10 (floor) | ≥ 10 each | basic cone r 2.6 → 3.1; bites r 2.2 → 2.6; bursts r 3 → 3.6; walls r 3.5 → 4.2 |

### 8.1 Phase 1 (종막 오아시스 파수꾼)

#### E — entrance (`V1` E 0-107)
- Trigger: fight start. Untargetable 0-110 (`rlk_mb_inv`). Title fade-in at t30.
- Timeline: the boss rises at the centre from a dark leaf pool 0-31; the Heart (egg look) hangs 9 b above the centre in the
  vine hand; the right A arm reaches up 31-47 and touches it at t47; **flash t60** on the bulb; golden leaf embers 63-80;
  the vine draws the Heart up into the canopy (y + 20) over 70-100 (`heart_up`); crouch + roar 91-107.
- No hazards. fx: `burrow_pool` (dark olive leaf pool 6-8 b), black leaf flakes, the bulb flash, golden leaf embers.
- Sounds: emergence `entity.warden.emerge` p 0.8 + `block.rooted_dirt.break` ×n + `block.azalea_leaves.break`; flash
  `block.amethyst_block.chime` + `block.beacon.power_select` p 1.5; Heart up `block.vine.step` + `block.amethyst_block.resonate`
  p 1.2; roar `entity.ravager.roar` p 1.3 v 0.6.

#### P1 잠복 돌진 (`V1` A, `MO` §6.3)
- Weights §7.4; cooldown 400 t.
- Timeline: rear 0-4; dive 4-8; sink 8-22 (`rlk_mb_inv`, proxies `burrowed`, husk 0.1 at 6); underground 22-44: the shadow
  prop glides toward `lockv {lead:10}` at ≤ 0.7 b/t and stops 2-3 b beside the predicted point; **t32 lock fixed + gold ring
  decal r 4.2**; the hidden body `tp`s under the lock (clamped r ≤ 18); **burst t44**; erupt 44-49; loom 49-61 (yaw locked
  toward the player at t52, lane decal from t52); **sweep t64**; the body glides 7 b along the facing 64-71 (ends ≤ 16 b from
  the centre); land 71-77; recover to t122 (punish window 45 t).
- Hazards: burst `hz/disc r 4.2 tell 12` at the lock, height 0-4, KB 3 outward, **1.2**; sweep `hz/line len 10.8 w 3.6
  tell 12` from the body along the facing locked at t52, height 0-3, **1.4**; separate groups.
- Dodge: step out of the ring or dash at the burst; leave the lane or dash at the sweep (2 dash-only hits 20 t apart).
- fx: `burrow_pool`, `shadow_glide`, `ring_gold` (= the burst disc), `gold_burst` (flash + radial crystal blades, airborne),
  black leaf debris + pale ghost-leaf spray, `slash_band` (white-gold streak 1-2.5 b high along the lane),
  `spine_afterimage` (pale ribs along the sweep path, 10 t).
- Sounds: dive / sink `entity.warden.dig` p 0.9 + `block.rooted_dirt.break` + `block.mud.break`; travel `entity.warden.dig`
  p 1.2 quiet every 7 t + `block.gravel.step` p 0.5; ring `block.beacon.activate` p 1.5 v 0.4; burst `entity.warden.emerge`
  p 1.4 + `block.amethyst_cluster.break` + `entity.generic.explode` p 1.3 v 0.4; sweep `entity.player.attack.sweep` p 0.5 +
  `entity.breeze.wind_burst` p 0.6; land `entity.ravager.step` + `block.moss.fall`.
- Helpers: `rlk_mb_inv`, px states, FN-19 `lockv`, `keep`, `mv/glide`, `mv/face`, `hz/disc`, `hz/line`.

#### R — burrow-relocate (`V2` B; the opener of P4 when the player is > 9 b away)
- Timeline: tell 0-4 (crouch lower), sink 4-14 (`sink_p1`, brown root chunks with gold glints; `rlk_mb_inv` at 4), hidden
  14-18, `tp` to `lockb` **2 b in front of the player** facing them (anchor clamp ≤ 14), `emerge_on_p1` 18-42 (scale-in +
  motes). No damage. (Footage re-emerges on the player; the 2 b offset avoids spawning the body inside the player and the
  r 9 disc covers both.)
- Sounds: sink `block.rooted_dirt.break` p 0.6 ×3 + `entity.warden.dig` p 1.1; emerge `entity.warden.emerge` p 1.3 v 0.6 +
  `block.azalea.place`.

#### P2 생명의 손 (`V1` H, `MO` §6.4)
- Weights §7.4.
- Timeline: spread 0-5; swirl tell 5-27 (yaw schedule 360°); raise 27-30; **plunge t30**; lock t33 (`lockv {lead:6}`); four
  **summoned stalks** (§5.3) rise t36-46 around the lock (2 near at ±60°, 2 far at ±140° from the boss → lock axis, on
  r 6.6); crack-line telegraphs from t40; **slams t62 / 69 / 75 / 82** (R-L-L-R, footage spacing 7 / 6 / 7 kept); stalks
  sink 83-100; upright on buried hands 100-108; pull-out + flower rear 108-128; fold 128-140; recover to t160.
- Hazards: plunge `hz/disc r 4.2 tell 30` at the body, **0.8**; each stalk's strip `hz/line len 8.4 w 3.0` from its root
  through the lock (+1 b), tells 22 / 29 / 35 / 42, height 0-2.5, **1.0**; volley groups {slam 1, slam 2} and
  {slam 3, slam 4} (≤ 2 hits).
- Dodge: leave the crossing point after the lock (3 b strips are walk-escapable); dash a line.
- fx: `swirl_wisps` (pale-green spirals, leaves whirl), plunge white-gold flash + `splinter_splash`, the stalk props,
  `crack_lines` (white-gold glowing lines root → lock; = the strips), slam arc trail + flash + green splinters.
- Sounds: swirl `entity.breeze.whirl` p 0.7 + `block.azalea_leaves.break` p 0.8 every 3 t + `block.beacon.ambient` p 1.6;
  plunge `entity.warden.dig` p 0.7 + `entity.evoker_fangs.attack` + `block.rooted_dirt.break`; stalks rise
  `block.hanging_roots.break` + `entity.warden.emerge` p 1.5 v 0.5; lines `block.sculk_sensor.clicking` p 1.6; slams
  `entity.iron_golem.attack` p 0.6 + `entity.generic.explode` p 1.5 v 0.3 + `block.big_dripleaf.break`; flower
  `entity.ravager.roar` p 1.2 v 0.6 + `block.azalea_leaves.break`; fold `entity.ravager.step`.
- Helpers: `lockv`, `keep`, `hz/disc`, `hz/line`, `grp_new`, the org stalk props.

#### P3 발광하는 파수꾼 (`V1` G + `V2` G, `MO` §6.5)
- Weights §7.4; cooldown 700 t; first allowed after 3 patterns. "Moves near the centre and slams 3 times."
- Timeline: rear 0-5; dive / sink 5-23 (`burrow_in_p1`); the shadow glides to the centre 23-39 (hidden); gold glow decal at
  the centre 39-44; `emerge_crown_p1` 44-84 (targetable from t55); turn to the player 84-94; `glow_slams` from t94: wind-up
  0-36 (footage 48); **slam 1 t141**; re-rear; **slam 2 t164**; leap 171-177; dive 184; **slam 3 t195**; settle to t225;
  recover to t245.
- Hazards:
  - slams `hz/disc r 5.4` at the centre, height 0-4: slam 1 decal t111 → tell 30, **1.1**; slam 2 decal from slam 1
    (tell 23), **1.1**; slam 3 decal from slam 2 (tell 31), **1.3**; separate groups. The gold blade rays (r 7.2) are
    airborne fx only.
  - per slam a **wheel carpet**: `hz/ring` front r 3 → 14.4 at 0.8 b/t (`hz/resize_s`, `#hzQuiet`, `#hzY1 7` jumpable, band
    1.0 b), **0.3**, with 18-20 pale-green wheel props riding the front.
  - per slam **2 homing wheels**: `pj` sphere hr 1.0 (wheel Ø 2) riding the front for 6 t at 0.75 b/t, then homing for
    16 t at **0.5 b/t** with `pj/steer {max:8}` (turn radius 3.6 b), life 22 t, then a pop (fx r 1.5);
    **`#pjNoDodge 1`** (FN-18); **0.15** each.
  - groups per slam: {carpet, wheel 1} and {wheel 2}: ≤ 2 thorn hits per slam, ≤ 6 per cast.
- Dodge: leave r 5.4 or dash the slams; jump or dash the carpet; the homing wheels ignore i-frames and out-speed a sprint —
  a wide sideways dash when a wheel is 1.5-2 b away makes it miss, or take the chip.
- Readability: homing wheels are **gold-orange** (rim and core) with a **red 4-point flare** and a looping
  `block.amethyst_block.resonate` p 1.6 + `entity.blaze.burn` p 1.8 v 0.3; carpet wheels stay pale green. First cast in a
  run: sub-line + actionbar "유도 가시 바퀴는 대시 무적으로 피할 수 없습니다 — 달려서 떼어 내거나 옆으로 크게 비키세요".
- fx: as P1's burrow; `gold_glow` ground; crown / hood emergence debris; `spiral_wisps` + core glow 15 in the wind-up;
  `gold_burst` + `blade_burst` (airborne); `thorn_wheel` / `thorn_wheel_homing` props; homing spark trail; wheel pop sparks.
- Sounds: emerge `entity.warden.emerge` p 1.1; glow `block.beacon.activate` p 1.5 v 0.4 + `block.sculk_catalyst.bloom`;
  wind-up `block.bamboo.break` p 0.6 + `entity.breeze.idle_air`; slams `entity.warden.attack_impact` +
  `entity.generic.explode` p 0.7 v 0.5 + `block.big_dripleaf.break`; wheels spawn `block.amethyst_cluster.place` ×3, roll
  `block.azalea_leaves.step` p 0.6 every 4 t, hit `entity.player.hurt_sweet_berry_bush` + `block.amethyst_cluster.break`.
- Helpers: `hz/disc`, `hz/ring` + `hz/resize_s` (fieldgen front), `pj/launch`, `pj/steer`, FN-18, `grp_new`, kit props.

#### P4 초목이 시든 풍경 (`V2` R, `MO` §6.6)
- Weights §7.4 (+ R when the player is > 9 b away).
- Timeline: arms 0-4; ARMSUP 4-10; LEAN 10-19; **disc decal appears at t16 and fills to the rim at t40** (23 t, never
  shorter); (fix 10-22f, user 10-22: the fill and the swing did not match) the whirl starts at 32 (yaw schedule, to the
  boss's left), the right A arm winds out at 36 and the **strike lands at t40**: the claw sweeps down through the front
  onto the floor (15°/t) as the fill reaches the rim; the whirl carries on over the ground to t64 (one turn); the hazard
  stays active over the whirl (`#hzAct 24`); sprawl / push-up 64-100; stand 100-125 (punish window); recover to t130.
  (Was: crash 40-47 as a drop, spin 47-71 starting 7 t after the hit.)
- Hazard: `hz/disc r 9.0 tell 24 act 24`, KB 4 outward, height 0-3, one hit, **1.3** (0.85 since AP-FIX).
- Dodge: leave r 9 before t40, or **dash on the full fill** (the dodge consumes the hazard; caption "범위가 완전히 꽉 찼을 때
  대시하면 피할 수 있다").
- fx: belly core bright; `rot_disc` (pale olive fill from the centre, rim #FCF9ED); spin spark trails white-gold → pale
  green, splashes, mid-spin flash.
- Sounds: arms / rear `entity.breeze.wind_burst` p 0.6 v 0.5 + `block.azalea_leaves.break`; disc hum `block.beacon.ambient`
  p 1.4 v 0.4 + `block.sculk_sensor.clicking`; crash + spin `entity.ravager.attack` p 0.6 + `entity.player.attack.sweep`
  p 0.5 ×3 + `entity.generic.splash`.
- Helpers: `hz/disc` + `#hzAct`, the kit filling disc.

#### P5 생명의 꼬리 — always two swings (`V2` T, `MO` §6.7; "used when the player is behind it")
- Trigger: the BACK rule (dwell, §7.4) or SIDE with f < 0 (weight 1).
- Timeline (`tail_p1x2`): a small turn ≤ 40° so the tail root faces the player 0-8; tail S-raise 8-23; **cock cue t23**
  (`entity.creaking.activate` p 1.4 + `item.trident.riptide_1` p 0.6 + a white tail-tip flash: "dash now"); **swing 1
  wedges t28-35**; recoil + coil 37-52; **swing 2 wedges t52-59** (reverse); rise to t127; recover to t142.
- Hazards: each swing = 8 per-tick `hz/sector` wedges (25° each, r 11.4 from the tail root, height 0-3) from the exported
  yaw schedule, one volley group; lane decal over the whole arc (swing 1 from t14, tell 14; swing 2 from t39, tell 13);
  KB 4; swing 1 **1.3**, swing 2 **1.4**.
- Dodge: a timed dash through the band, step in front of the head, or range > 11.4 b.
- fx: tail S-raise; white-gold arc trail; screen flash on a hit.
- Sounds: turn / raise `entity.breeze.idle_air` p 0.7; swings `entity.player.attack.sweep` p 0.6 + `item.trident.throw` p 0.5;
  hit `entity.player.attack.knockback`.
- Helpers: `api.wedges()`, `mv/turn`, FN-20 zones.

#### P6 근접 콤보 (2-4 hits; `V2` C, `MO` §6.8)
- Trigger: FRONT near (4), mid / SIDE (1). Pre-turn ≤ 10 t. Length roll 2 / 3 / 4 (weights 3 / 4 / 3); segments a → b → c →
  d, `combo_end` unless the last one is d.
- Timeline (cumulative, 4 hits): a: arm-back tell 0-10, **hit 1 t14**, recover to t29; b: rear 29-43, **hit 2 t46**,
  recover to t73; c: twist 73-78 (spin yaw schedule), **hit 3 t83** (decal at t73), recover to t93; d: tallest rear 93-115,
  lunge 115-120 (the body glides 2.5 b), **hit 4 t120**, recover to t170.
- Hazards: hit 1 `hz/sector r 7.2 half-angle 78° tell 10`, height 0-1.8, **1.0**; hit 2 `hz/disc r 6.6` centred 4.8 b ahead,
  tell 14, **1.2**; hit 3 `hz/disc r 7.2` around the body, **`#hzY1 7` (jumpable low spin)**, tell 10, **0.9**; hit 4
  `hz/disc r 6.6` centred 7.2 b ahead, tell 22, **1.4**.
- Dodge: keep distance (caption "거리를 벌리는 것이 낫다"), jump the spin, or dash each.
- fx: arm-sweep arc + ground furrow; double-slam radial burst + dark debris + white-gold ground cracks; spin ring of gold
  sparks; leap slam biggest flash + black / gold debris.
- Sounds: sweep `entity.player.attack.sweep` p 0.7 + `block.grass.break`; slams `entity.warden.sonic_boom` p 1.6 v 0.5 +
  `entity.generic.explode` p 0.7 + `block.mud.break` ×4; spin `entity.player.attack.sweep` ×2 p 0.6 / 0.8.
- Helpers: `hz/sector`, `hz/disc`, `mv/glide`, `Pattern.lead`.

#### M — crawl / walk (locomotion, no damage)
- `crawl_p1` 0.25 b/t ≤ 40 t, `crawl_stop_p1` into a half-stand with the core lit (`V1` M); `walk_p1` 0.12 b/t.
- Sounds: crawl `entity.camel.step` p 0.6 + `block.moss_carpet.step` + `block.azalea_leaves.step`; walk
  `entity.warden.step` p 0.8.

### 8.2 Phase-2 organisms' attacks (all Dendro; areas ×1.2)

| id | attack | timeline | hazard | coef | Heart | dodge | fx / sounds |
|---|---|---|---|---|---|---|---|
| O1 | 기본 melee | every 40 t while holding an attack slot: lean tell 0-10, **strike t10** | `hz/sector r 3.1 half 27° tell 10` aimed at the Heart from the tell start (a player in the cone is hit) | **0.25** (buffed 0.30) | −60 (−120) | step out / dash | squash-lean; `entity.slime.attack` p 1.2 + `block.big_dripleaf.tilt_down`; Heart `block.amethyst_block.hit` p 0.6 v 0.4 |
| O2 | 기본 ranged | every 50 t while holding a slot: pivot 0-3, crown glow 3-5, crown open 5-12 + a thin aim lane decal to the Heart (tell 12), **launch t12** | `pj` sphere hr 0.7 at **0.75 b/t**, straight at y + 1.6, life ⌈d / 0.75⌉ + 2; the module ends it within 1.5 b of the Heart (= the Heart hit); `pj_end` 4 (hit the player) spares the Heart | **0.34** (buffed 0.42) | −60 (−120) | body-block on purpose, or avoid | crown flares, green comet trail bowing ≤ 0.5 b; `block.big_dripleaf.tilt_up` p 1.4, `entity.breeze.charge` p 1.6 v 0.4, `entity.breeze.shoot` p 1.3; hit `block.moss.break` p 1.3 |
| O3 | 수호 shield cast | collapse 0-7, bud 7-16, regrow 16-24, **shields t30**; recast every 240 t | none (shield pool on basics, §7.6.6) | — | — | kill the 수호 first | collapse / regrow; shields pop with a yellow 3-leaf crown flash; `block.bamboo.break` p 0.8 v 0.5, `block.mangrove_roots.place` p 0.7, `block.beacon.activate` p 1.6 v 0.5, pop `block.amethyst_block.resonate` p 1.4 + `item.shield.block` p 1.6 v 0.4; death `block.chorus_flower.death` + `entity.slime.death` p 0.7 + red embers + black wisp |
| O4 | 둥지 walls | tell 0-12 (loop pose, spot decals), **walls t12**, stand 40 t, dissolve 8 t; every 160 t; blink 6 t when > 12 b | barriers (§7.6.7) | — | — | walk through a gap; no damage | walls rise `block.big_dripleaf.place` ×3 p 0.7 + `block.azalea.place` + `block.amethyst_cluster.place` p 1.2; dissolve `block.azalea_leaves.break` + `block.beacon.deactivate` p 2.0 v 0.3; flap `entity.phantom.flap` p 1.5 v 0.3 |
| O5 | 양육 link | tell 0-20 (cap tilts), tethers from t8; re-link every 80 t | none; immunity + buffs (§7.6.5) | — | buffed hits −120 | kill the buffed basics | 3 wavy tether beams (dust #D4E784) refreshed every 2 t, the translucent cylinder; `block.beacon.ambient` p 1.8 v 0.2 every 40 t; self-destruct `block.azalea_leaves.break` + `entity.allay.death` p 1.3 + `block.amethyst_cluster.break` |
| O6a | 포식성 burst | swallow 0-12, bud 12-32, inflate 32-42 (tell, burst decal), **burst t42** | `hz/disc r 3.6 tell 10` | **0.35** | — | dash / step out | gulp `entity.generic.eat` p 0.6 + `entity.slime.squish`; bud `block.beacon.power_select` p 1.5 v 0.4; inflate `entity.puffer_fish.blow_up` p 0.8; burst `entity.puffer_fish.blow_out` + `block.amethyst_cluster.break` p 1.4 + `entity.firework_rocket.blast` p 0.8 v 0.5 |
| O6b | 포식성 bites | after circling 40-60 t: **chain 1** = 4 bites at +12 / +18 / +24 / +30 (each sector locked at the player and drawn 10 t before its strike, lunge 1.5 b each); 14 t; **one single bite** (tell 10); 12 t; **chain 2**; then single bites every 60 t | per bite `hz/sector r 2.6 half 24° tell 10`, own group | chain **0.67 / 0.34 / 0.20 / 0.13** (raw 12 / 6 / 3 / 2 ≈ `V4` 2.0 : 1.0 : 0.6 : 0.4); single **0.34**; un-empowered ×0.7 | — | keep > 4 b away or dash | white-yellow bite flash; `entity.evoker_fangs.attack` p 1.3 + `entity.ravager.attack` p 1.6 v 0.4 (+ `entity.player.attack.crit` on the first); swim `entity.dolphin.swim` p 1.2 |
| O7 | 파괴 blast | roll ≈ 95 t, contact → fuse 56 t (decal from contact), suck 5 t, **blast at contact + 61** | `hz/disc r 3.6 tell 61` at the ball | **0.67** | −1400 | kill it before contact, or leave r 3.6 | fuse pulses + ring; `entity.armadillo.roll` p 0.8 every 8 t; `entity.creeper.primed` p 1.4; `entity.breeze.inhale` p 0.8; blast `entity.generic.explode` p 0.8 + `entity.warden.sonic_boom` p 1.6 v 0.3; green dome 12 t + husk flung 2-3 b |

Kill feedback: basic `block.azalea_leaves.break` + `entity.slime.squish_small` + a pale-green burst; specials their death
clips.

### 8.3 Phase 3 (기원 오아시스 파수꾼)

Phase-3 coefficients include a ×1.25 bump over phase 1 (Genshin ATK 19,031 / 11,419 = 1.67, damped; Q19).

#### Q1 이동 돌진 (`V5` M; caption "바닥에서 빠르게 튀어 올라 꼬리를 휘두른다")
- Weights §7.4; chained after Q5 (40 %).
- Timeline (`move_strike_p3`): fold 0-7, mound / sink 8-16 (`rlk_mb_inv` + `burrowed` + husk 0.1 at 8); underground 16-42:
  the leaf-pad trail glides to `lockv {lead:10}` at ≤ 0.8 b/t; **t32 lock + rosette decal r 4.2** (the outer leaf petals are
  airborne fx); the hidden body `tp`s there (clamp r ≤ 16); **burst t44**; hoop 44-49; roll 49-61 (the body glides 4 b
  toward the player); **slam t61**; the tail lands 65; **tail sweep t69**; rise 71-92 (UPRIGHT); recover to t112.
- Hazards: burst `hz/disc r 4.2 tell 12`, **1.4**; slam `hz/disc r 4.2` at the roll end, tell 15 (decal from t46), and the
  tail sweep `hz/disc r 12 tell 21` (decal from t48) with **`#hzY1 7`** (the low 360° ground whip, jumpable), **one volley
  group, 1.5**.
- Dodge: leave the rosette or dash; then jump the whip (one dash + one jump; the slam is walk-escapable from outside its
  disc).
- fx: leaf mound + spray, `leaf_pads` trail (2-3 b translucent pads), `rosette` (8-12 glowing leaves; the ground ring = r 4.2),
  burst flash white-lime + leaf spray, hoop arc trail, belly-flop splash, `sweep_ring` (leaf blades, core #E0F996, rim
  #A2CA6C), light sprouts at the rise.
- Sounds: sink `entity.warden.dig` p 1.2 + `block.mud.break` + `entity.player.splash.high_speed` p 0.6; trail
  `block.big_dripleaf.tilt_down` p 0.8 + `block.lily_pad.place` every 4 t; rosette `block.flowering_azalea.place` +
  `block.spore_blossom.place` p 0.6; burst `entity.warden.emerge` p 1.3 v 0.6 + `entity.generic.splash` +
  `block.big_dripleaf.break`; slam / sweep `entity.generic.explode` p 1.4 v 0.4 + `entity.player.attack.sweep` p 0.6 +
  `entity.generic.splash`; rise `block.big_dripleaf.tilt_up` + `block.vine.step`.
- Helpers: `rlk_mb_inv`, px states, `lockv`, `mv/glide`, `hz/disc` (`#hzY1`).

#### Q2 종말의 여파 (`w1`, `V5` W; scheduled §7.4; domes §7.8)
- **Banner B0** (before anything moves): "**소생의 찬가 보호막** 안으로 들어가서 종말의 여파를 막아내세요" (the first phrase
  red #C36E5A, the rest white); the 3 dome footprints appear; the under-bar becomes a two-segment countdown (red to the
  blast, then gold to the dome pop).
- Approach: from B0 the boss walks to the centre in the crawl stance at 0.4 b/t, ≤ 50 t (skipped when it is within 2 b).
- Fix 10-22f (user 10-22): at B0 the field is laid (the wash and a ring front r 3 → 26 over 20 t at the centre) and
  ticks from B0 + 20; dome pillars (10 t tells) at **B0 + 24 / 28 / 32** → domes formed **B0 + 34 / 38 / 42** (dome 0 =
  the player's first), on the pattern clock, before and during the walk (was clip t44-52 → t54-62).
- Timeline (`aftermath`, t0 = the walk's end): charge / curl 0-18 (brightness 15); whirl 18-36 (yaw schedule 360°; face
  `p3_charge`); land 40: a field ring pulse r 3 → 26 (visual); the boss rises aloft 76-84 (proxies `aloft`);
  light columns rain 134-156; **blast t156**, active to t176; the flood fx 156-180; descend / stand 162-224; **domes pop
  t189** (banner off, sub-line "보호막이 사라질 때까지 기다리세요" from the blast to the pop); recover to t240.
- Hazards (FN-14 mask in the cast's safe group; FN-15 ‰ damage; all Dendro, `#hzNoDodge`, `#hzNR`):
  - field ticks (fix 10-22f): mask, `#hzPm 20` (2 % max HP), non-lethal, `#hzRearm 10`, made at B0 with tell 20, active
    to the tick before the blast (`#hzAct = #apq32S + 136`; 15-20 ticks);
  - **blast**: mask, `#hzPm 800` (80 % max HP), lethal, `#hzAct 20` (t156-176, tested every tick, one hit); **the first
    cast of each fight is non-lethal** (`#hzLethal 0`) and is followed by the red line "다음 종말의 여파는 치명적입니다 —
    보호막 안에 머무르세요".
  - Inside a formed dome: no hit, and +1 % max HP every 20 t (t54-189).
- Dodge: be inside any dome from t156 to t176 (and early to skip ticks: the two ticks before the domes stand are the
  price of the field). The player's dome is ≤ 9 b away at the banner (≤ 9.3 b at the barrier).
- fx: kit banner; amber face; crouch splash; whirling leaves; `field_ring` (flat translucent yellow-green wave) + floor
  glitter; `light_pillar`; dome rise; `beam_rain` columns; white-out flash (`hud/flash_white`, 6 t); `flood` (yellow tiles
  that skip the dome cells); dome pop flash + shards; green burst at the boss.
- Sounds: banner `block.respawn_anchor.set_spawn` p 0.7 + `entity.elder_guardian.curse` p 1.4 v 0.4; charge
  `block.conduit.activate` p 0.8 + `block.beacon.power_select` p 0.6, whirl `entity.breeze.whirl`; release
  `entity.warden.sonic_charge` p 1.4 + `entity.breeze.wind_burst` p 0.6; field loop `block.bubble_column.upwards_ambient` +
  `block.sculk.spread` p 1.4; tick `entity.player.hurt_sweet_berry_bush`; dome `block.beacon.activate` p 1.8 +
  `block.amethyst_block.chime` ×3 + `block.respawn_anchor.charge` p 1.6; rain `block.beacon.power_select` p 1.8 v 0.5; blast
  `entity.warden.sonic_boom` p 0.8 + `entity.dragon_fireball.explode` p 0.7 + `entity.lightning_bolt.thunder` p 1.5 v 0.4;
  pop `block.glass.break` p 1.5 v 0.5 + `block.amethyst_cluster.break` + `block.bubble_column.bubble_pop`.
- Helpers: FN-14 / FN-15 (or the option-b fallback), `rlk_mb_hzsafe` markers, `hz/ring` + `hz/resize_s` (visual front),
  `mboss/player_heal` for the dome heal (so item heal hooks see it), kit banner. No cine flag (the player must act).

#### Q3 증폭의 풀 (3 shells; `V5` S; caption "세 번의 포격 / 첫 번째 포격 속도가 유난히 빠르다")
- Stance UPRIGHT (`stand_p3` first if crawled).
- Timeline (`shells`): hunch 0-10; **target ring r 3.6 follows the player's feet as they were 6 t earlier**, moved every 2 t,
  from t10; charge 14-33 (brightness 15, light ball over the crown); **t33 the ring stops = lock 1**; one launch t35 (all
  three shells go up); **impact 1 t45** (the fast vertical beam); ball 36-44; cool t48 (brightness 13): the boss idles unlit
  with arms open (punish window); **lock 2 t79** (`lockv {lead:8}`) and **lock 3 t82** (`lockp`), rings r 3.0; **impacts
  t93 / t96** (shells 2 / 3 drop steeply from high); recover to t113.
- Hazards: shell 1 `hz/disc r 3.6 tell 12` (beam column 3 b wide; the leaf-blade splash is airborne fx), KB 2, **1.5**;
  shells 2 / 3 `hz/disc r 3.0 tell 14` each, **one volley group, 1.3**.
- Dodge: keep moving (the ring lags 6 t, so a walker leaves it in time) or dash at the lock; shells 2 / 3 land 3 t apart, so
  one dash covers both.
- Chain: 30 % → Q3s (≥ 20 t after t96).
- fx: `target_ring` (pale disc #C1E6A8 following), body lime glow, light ball over the crown, launch flash, shell 1
  `beam_column` 3 b wide (#FDFBBD) + airborne leaf splash + spores; shells 2-3 yellow streaks from high + burst r 3.
- Sounds: charge `block.respawn_anchor.charge` p 1.5 + `block.beacon.ambient`; launch `entity.breeze.shoot` p 0.8 +
  `item.crossbow.shoot` p 0.5; impact 1 `entity.generic.explode` p 1.2 + `block.beacon.deactivate` p 1.5 +
  `block.big_dripleaf.break`; impacts 2-3 `entity.dragon_fireball.explode` p 1.4 v 0.5.
- Helpers: the late-lock template (`fgcruise:441-533`), `lockp`, `lockv`, `hz/disc`, `grp_new`.

#### Q3s 수면 포격 — the surfacing shot (chain after Q3; `V5` M2 + `V6W` take 1)
- Timeline: `sink_p3` 0-20 (fold 0-7, `rlk_mb_inv` + `burrowed` + husk 0.1 at 8, hidden 12); underground 20-36: a short
  leaf-pad trail to a point 8-10 b from the player on the boss → player line (clamp r ≤ 14); **t26 leaf-ring decal r 3.6**
  at the surfacing point; **t36 surface** in the crawl stance (`surface_p3`): splash; t36 `lockp` ring r 3.0 at the player;
  charge 36-46 (body lit; footage 4 t, our floor 10); launch t46 (a flat fast streak); **impact t48**; recover 48-76;
  `stand_p3` 76-90.
- Hazards: surfacing splash `hz/disc r 3.6 tell 10`, **0.8**; shell `hz/disc r 3.0 tell 12`, **1.3**; separate groups.
- Dodge: step off the ring when it appears; the splash only matters for a player standing at the surfacing point.
- fx: leaf mound, leaf pads, leaf ring, surfacing splash, body charge glow, horizontal light band (the shot), landing light
  column + burst r 3.
- Sounds: sink as Q1; surface `block.mud.break` + `entity.player.splash` p 0.6 + `block.azalea_leaves.break`; charge
  `block.respawn_anchor.charge` p 1.5 v 0.6 + `block.amethyst_block.resonate` p 1.6; launch `entity.breeze.shoot` p 0.8 +
  `item.trident.riptide_1` p 1.4 v 0.5; impact `entity.generic.explode` p 1.3 v 0.5 + `block.beacon.activate` p 1.8 +
  `block.cherry_leaves.break`.

#### Q4 생명의 꼬리, phase 3 (2 swings; `V6W` §2.2; caption "꼬리를 2회 후려친다")
- Weights §7.4. Opener: when the player is > 8 b away, `crouch_p3` + `walk_p3` ≤ 30 t at 0.2 b/t toward them; otherwise
  `crouch_p3` (8 t) when upright.
- Timeline (`tail_p3`): crouch / cock 0-11; **swing 1 wedges t14-21** (fast + spin); rise into the S-coil 24-36; lunge 3-4 b
  toward the player 36-40 (module glide); **swing 2 wedges t46-53** (reverse, low); rise 57-87 (UPRIGHT); recover to t105.
- Hazards: swing 1 per-tick `hz/sector` wedges (25° each, r 12, height 0-3) in one group, lane from t2 (tell 12), **1.5**;
  swing 2 the same reversed, lane from t32 (tell 14), height 0-2 (not jumpable), **1.6**; KB 4.
- Dodge: timed dash, or range > 12 b; standing at the body during swing 2 is unsafe (the lunge).
- fx: green crescent trails (#A4D6AC / #BFE682 / #EBF898), glitter shower, tail-tip flash.
- Sounds: as P5 + `block.azalea_leaves.fall` ×3; rear / lunge `entity.creaking.activate` p 0.6 + `entity.ravager.step` p 0.6;
  swing 2 + `block.amethyst_cluster.step` ×4 + `item.bone_meal.use`.
- Helpers: `api.wedges()`, `mv/glide`.

#### Q5 생명의 나선 (`V6W` §2.3; caption "가시를 여러 개 소환하고 한꺼번에 날린다 / 회피가 다소 난해한 편")
- Weights 2 / 2 / 2; 40 % chain into Q1. Stance UPRIGHT.
- Timeline (`spikes`): curl 4, rise 10, V + light column 14, **12-14 seed-orbs summoned 19-32**, spread ±7 b sideways and
  3-10 b up around the body; **glint / lock A t37** (`lockp`, no lead): 6 landing discs r 2.0 scattered within r 3.6 of A
  (tell 12); the orbs fly at t42 and **land t49**; **lock B t43** (`lockp` at that tick): 6 more discs, fly t48, **land t55**;
  late leaf blades: 2 low lanes locked at t52 across the player's spot, **skim t64**; recover to t72 (+ idle).
- Hazards: the landings are `hz/disc r 2.0` with their decals (the orbs are visual projectiles on double-helix trails, no
  hitbox); volleys A and B **one volley group, 1.2**; blades 2 × `hz/line len 14 w 2.2 tell 12 #hzY1 7` (jumpable), one
  group, **0.6**.
- Dodge: leave the scatter (≈ r 5.6 including the disc radius) or dash for A, then again for B (6 t apart); jump the blades.
- fx: charge streaks, unfold, `seed_orb` (glowing yellow-green balls with a spiral glyph, bobbing), 4-point star flares at
  the glint, double-helix ribbon trails (two sine strands, dust #E7F99F → #8BCAAA), star bursts + upthrust crystal / leaf
  spikes on impact, skimming pale-yellow leaf blades.
- Sounds: unfold `entity.breeze.charge` p 1.2 + `block.big_dripleaf.tilt_up` p 0.6 + `block.amethyst_block.chime` ×3; orbs
  `block.amethyst_cluster.place` each + `block.beacon.ambient` p 1.8 v 0.3; flares `block.beacon.power_select` p 1.8 v 0.5;
  launch `entity.arrow.shoot` p 0.6 ×6 + `item.trident.throw` p 1.4 v 0.4; impacts `entity.generic.explode` p 1.6 v 0.3 +
  `block.amethyst_cluster.break` p 0.8 + `block.pointed_dripstone.land`; blades `entity.breeze.wind_burst` p 1.2 +
  `block.cherry_leaves.fall`.
- Helpers: `lockp`, `hz/disc`, `hz/line`, `grp_new`, kit props (visual orbs).

### 8.4 Sequences

- **T1** §7.5. Sounds: sink as P1; cradle rise `block.rooted_dirt.break` + `block.mangrove_roots.place` p 0.7; Heart lowering
  `block.amethyst_block.resonate` p 1.2 + `block.spore_blossom.break`; egg lands `block.honey_block.fall` p 0.6 +
  `block.beacon.power_select` p 1.4 + `block.amethyst_block.chime`; HUD `ui.toast.in` p 1.2; spawn markers
  `block.chorus_flower.grow` + `block.sculk_shrieker.place` p 1.5.
- **CS** §7.7. Sounds: completion `block.respawn_anchor.set_spawn` p 1.3 + `block.amethyst_block.chime`; ember
  `block.fire.ambient` p 1.6 v 0.3; flash `block.beacon.activate` + `entity.lightning_bolt.thunder` p 2.0 v 0.3; heal
  `block.amethyst_block.resonate` p 1.4; emergence `entity.warden.emerge` p 0.8 + `block.azalea_leaves.break` burst; reveal
  `block.beacon.activate` p 0.7.
- **D death** (proposal; `MO` §6.17): 120 t: hood snaps back, face / core flicker 8-30, droop 30-55, kneel 55-70, topple
  onto the water 70-82 (splash), wither 85, sink / dissolve into leaves with a burst of white leaflets 100-118; a glowing
  golden seed prop remains. Sounds: `block.big_dripleaf.break` p 0.5, `block.beacon.deactivate` p 0.6 at the face fade,
  `block.azalea_leaves.break` bursts, `entity.generic.splash` at 82, `block.respawn_anchor.deplete` p 0.8 at the sink,
  `block.amethyst_block.chime` for the seed. No creature vocals.

---------------------------------------------------------------------------------------------------

## 9. Numbers

### 9.1 Registry and pools (L18; reference player item-less Lv15: HP 268, def 38, atk 38)

| item | value |
|---|---|
| registry | hp 290 (start; knob 270-320), atk 12, dmgMul 150, xp 40, goldMul 1, sap 0, picks 0, lvAdd 0 (§3.7) |
| total HP | ≈ 7235 (`F:mob/level_apply`; the build prints it) |
| P1 / P3 pools | ≈ 3835 / 3400 (53 / 47 %, Genshin 667,805 / 593,605) |
| P1 floor | 1 % of the P1 pool ≈ 38 HP |
| rewards | chapter boss: gold 2..4 × chapter 3 × 15 = 90-180, 2 sapphires, 40 XP, the 5 % heal-orb roll on the kill; organisms nothing but energy particles |

### 9.2 Hit grid (raw = ⌊atk × coef% × dmgMul / 10000⌋ = ⌊0.18 × coef%⌋, then level and defence)

`mboss/hurt` multiplies atk × coef × dmgMul once and divides once, so the raw step is 0.18 per coefficient point whatever
the atk / dmgMul split; coefficients are picked on this grid. HP ≈ 2.83 × raw against the reference player.

| coef | 0.15 | 0.25 | 0.30 | 0.34 | 0.42 | 0.6 | 0.67 | 0.8 | 0.9 | 1.0 | 1.1 | 1.2 | 1.3 | 1.4 | 1.5 | 1.6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| raw | 2 | 4 | 5 | 6 | 7 | 10 | 12 | 14 | 16 | 18 | 19 | 21 | 23 | 25 | 27 | 28 |
| HP | 6 | 11 | 14 | 17 | 20 | 28 | 34 | 40 | 45 | 51 | 54 | 59 | 65 | 71 | 76 | 79 |
| % of 268 | 2 | 4 | 5 | 6 | 7 | 11 | 13 | 15 | 17 | 19 | 20 | 22 | 24 | 26 | 28 | 30 |

### 9.3 Coefficients (starting values; the balance fixer tunes `api.DMG`)

**AP-FIX values (2026-10-22, the one balance pass; Change notes "AP-FIX + AP-VERIFY"; these replace the starting values
below in `api.DMG`):** P1 burst 1.08, sweep 1.25; P2 plunge 0.67, strips 0.85; P3 unchanged; P4 0.85; P5 unchanged; P6 0.55 /
0.67 / 0.5 / 0.77; Q1 burst 0.56, slam + sweep 0.6; Q3 shell 1 0.52, shells 2 + 3 0.45; Q3s splash 0.32, shell 0.52; Q4 0.52 +
0.56; Q5 volleys 0.48, blades 0.24 (the x1.25 phase-3 bump is inside these); organisms unchanged.

| pattern | hits (coef) | groups / max per cast |
|---|---|---|
| P1 잠복 돌진 | burst 1.2, sweep 1.4 | 2 |
| P2 생명의 손 | plunge 0.8, strips 4 × 1.0 | {1,2} {3,4}: ≤ 3 |
| P3 발광하는 파수꾼 | slams 1.1 / 1.1 / 1.3; per slam carpet 0.3 or wheel 1 0.15, wheel 2 0.15 | ≤ 3 slams + ≤ 6 thorn hits |
| P4 초목이 시든 풍경 | 1.3 | 1 |
| P5 생명의 꼬리 | 1.3 + 1.4 | 2 |
| P6 근접 콤보 | 1.0 / 1.2 / 0.9 / 1.4 | 2-4 |
| Q1 이동 돌진 | burst 1.4; slam + sweep 1.5 | 2 |
| Q2 종말의 여파 | ticks 2 % max HP every 10 t from B0 + 20 (15-20; fix 10-22f, was 3 % ≤ 5); blast 80 % max HP (first cast non-lethal) | — |
| Q3 증폭의 풀 | shell 1 1.5; shells 2 + 3 1.3 | 2 |
| Q3s 수면 포격 | splash 0.8, shell 1.3 | 2 |
| Q4 생명의 꼬리 | 1.5 + 1.6 | 2 |
| Q5 생명의 나선 | volleys A + B 1.2; blades 0.6 | 2 |
| organisms | basic melee 0.25 (buffed 0.30), ranged 0.34 (buffed 0.42); 포식성 burst 0.35, chains 0.67 / 0.34 / 0.20 / 0.13 ×2, single 0.34, un-empowered ×0.7; 파괴 0.67 | — |
| 소생 실패 (1st) | 25 % max HP, non-lethal | — |

Phase-3 rows include the ×1.25 bump; if the sim lands above the band the bump drops to ×1.1 first (Q19).

### 9.4 Organisms (HP ‰ of `#apTot` ≈ 7235; RES Dendro 20 / rest 10; wiki ratios on a 17 ‰ basic)

| kind | ‰ | HP | single-target kill, item-less sword (≈ 45 HP/s) | progress | moves |
|---|---|---|---|---|---|
| 기본 basic | 17 | 123 | 2.7 s | +325 | 0.12 b/t |
| 수호 guarding | 34 | 246 (+ shields 5 × 123 per basic; Pyro ×1.5) | 5.5 s | +1400 | immobile |
| 파괴 destruction | 21 | 152 | 3.4 s | +1400 (blast −1400) | 0.10 b/t |
| 포식성 predatory | 26 | 188 | 4.2 s | +1400 | 0.15 b/t |
| 둥지 nesting | 26 | 188 | 4.2 s | +1400 | 0.15 b/t, blink |
| 양육 nurturing | 34 | 246 | immune while linked; dies after 3 linked losses | +1400 | immobile |

### 9.5 The Heart (`api.REV`)

**AP-FIX values (2026-10-22):** basic kill +300, special kill +1300, basic hit −54, buffed −108 (the rest as below).

Start 2700 ‱, win 10000; basic kill +325, special kill +1400; basic hit −60, buffed −120; 파괴 blast −1400; 3 attack
slots; cap 6; wave clock 30 s or ≤ 1 alive; time-out 100 s, then 1 파괴 per 30 s, ≤ 1 alive; failure strikes 2 (1st =
25 % max HP non-lethal + restart at 2700 from wave 1).

### 9.6 Fight length (estimates at hp 290)

| piece | item-less Lv15 sword | typical chapter-3 items (≈ ×1.75 DPS) |
|---|---|---|
| E + T1 + CS | ≈ 22 s | ≈ 22 s |
| P1 (pure DPS ≈ 102 s + ≈ 35 % downtime: burrows, untargetable emergences) | ≈ 138 s | ≈ 79 s |
| P2 | ≈ 95-110 s | ≈ 55-65 s |
| P3 (pure DPS ≈ 91 s + ≈ 40 % downtime incl. 2-3 종말의 여파) | ≈ 127 s | ≈ 73 s |
| **total** | **≈ 6.3-6.6 min** | **≈ 3.8-4.0 min** |

Healing inside the fight (Q25): the CS heal 25 % max HP, the dome heal 1 % per 20 t; nothing from organisms.

### 9.7 Fairness-sim targets (U8)

Harness `apfair.py` on AZ's sim of record (Lv15 item-less, HP 268, def 38, atk 38, vs L18), 3 seeds × 3 min per policy, the
Guardian on the same harness as calibration (Lv4 item-less vs L4: 160 / 116 / 96 % max HP per minute for stand / melee
walk / ranged walk).

| measure | target | accept |
|---|---|---|
| P1 HP loss per minute in % of max HP, stand / melee walk / ranged walk | **0.9 ×** the Guardian's | 0.72-1.08 × |
| P3 the same | 0.9 × | 0.72-1.08 × |
| whole fight (P1 + P2 + P3) HP lost, per agent | ≤ 1.2 × Azhdaha's whole fight for the same agent (until AZ's numbers exist: ≤ 2.5 × the Guardian's) | gate |
| worst 40 t window, melee walk and ranged walk | ≤ 45 % max HP | gate |
| all hits of one cast, stand agent (casts ≤ 120 t; longer casts: worst 60 t) | ≤ 60 % max HP (the Q2 blast excluded) | gate |
| dash-only hits per 40 t (static check) | ≤ 2, ≥ 6 t apart | gate |
| undodgeable share of damage, walker | ≤ 25 % | gate |
| perfect dasher (sprints / side-dashes homing wheels) | ≤ 0.3 × the Guardian's walker | gate |
| positional teaching (P1): FRONT-mid melee walker vs BACK melee walker | ≥ 25 % less loss | gate |
| 종말의 여파, walk-to-nearest-dome agent | 0 blast hits, ≤ 3 ticks per cast (the 2 pre-dome ticks + 1; fix 10-22f, was ≤ 2), 0 deaths / 9 seeds | gate |
| 종말의 여파, late agent (moves at dome 1 + 40 t) / early leaver (leaves at the blast) | late: 0 deaths; early leaver: survives from full HP | gate |
| human jump model (press within ±2 t of the ideal tick) | every documented jump dodge succeeds | gate |
| P2 stage length, plan agent: item-less sword / items ×1.75 / strongest (bow ×2.5) | 85-120 s / 50-75 s / ≥ 30 s | band |
| P2 failures: every character at ≥ 0.6 × sword DPS, plan agent | 0 / 9 seeds | gate |
| P2 failures: the "nearest target, ignores hints" agent, item-less sword | ≤ 1 / 9 | gate |
| P2 idle agent | Heart at 0 in 30-45 s | band |
| P2 HP loss per minute (mostly 포식성) | ≤ 0.8 × the P1 rate | gate |
| one 포식성 bite chain on a standing player | ≤ 30 % max HP | gate |
| full fight, item-less sword agent | ≤ 6.5 min | gate (hp knob) |
| `apfair` P2 module vs `S:ap/plan_work/p2sim_rev.py` (config W7) | stage length within 15 % | validation |

Agent extensions: attack the nearest vulnerable proxy (never the anchor); walk to the nearest dome at the banner and stay
until the pop; sprint away from or side-dash the homing wheels; phase-2 priorities (수호 > buffed basics > 파괴 before
contact > basics at the Heart); body-block bolts when on the way; jump the `#hzY1 7` bands when not swinging; walls as
collision. Knob order for the fixer: `api.DMG` per pattern → the P3 bump → recover windows → `api.REV` → `hp`. Note: the
execute engraving and the hood item read `mhpC / mhpM`, so they fire near the end of both pools.

---------------------------------------------------------------------------------------------------

## 10. Stages (parallel git worktrees, strict file ownership)

Worktrees `S:ap/wt_<name>/roguelike`, RP sandboxes `S:ap/rp_<name>`. "Green" per stage: FX = `test_ap_fx` + the M0 suites;
ARENA = `test_ap_arena` + the M0 suites; ORG = `test_ap_org` + the M0 suites; RIG = `test_ap_rig` + `check_ap_manifest` +
identity; CORE and later = `run_all.sh`.

| stage | branch / worktree | owns (only these) | needs | done when |
|---|---|---|---|---|
| **AP-SPEC** (day 0) | none | `S:ap/ap_contract.md` §0, `S:ap/spec/{rig,org}_manifest.schema.json`, `S:ap/ap_fx_api.md` §0 (call list), the theme interface note | this plan | the stub manifests validate against the schemas (§3.9) |
| **AP-R1** rig block-out, both forms and stances | `wip/ap-rig` from M0 (+ RIGLIB when merged), `wt_rig`, `rp_rig` | R19 files (block-outs), temporary `apep_shape.mjs` | AP-SPEC | R2 tree with pose bones; 49 parts within R4 / R5; CROUCH and UPRIGHT with the R3 residual table ≤ 0.25 b; the `v5 f1104` mantle identification; `stand_p3` / `crouch_p3` blend stubs; hand variants blocked out; looks and tints (untinted-face check); proxies + coverage gate; capsules; burrow + park test; R6 extents; R21 sheets; Guardian / butterfly / fieldgen / Azhdaha identity |
| **AP-R2** region refiners ×5 (parallel) | `wip/ap-rig-<head\|body\|limbs\|hands\|tail>` from AP-R1, own sandboxes | one region file each; pose, builder, aggregators, clips and materials frozen | AP-R1 | per-region sheets (P1 + P3) vs `MP3` 01-05 and the §12 frames; per-region budgets and sprite ledger |
| **AP-R3** rig integration | `wip/ap-rig` | merges R2; aggregators, materials, builder; the RIGLIB switch; the P3 pose glossary (§6.2) | AP-R2 | the full R21 render set per form, look and stance; critique list closed; budgets (≤ 56 parts, ≤ 0.9 M px, R14); identity; **renders sent to the user** together with AP-ORG2 (U3) |
| **AP-RC1** clips v1 | `wip/ap-rig` (from the frozen AP-R1 skeleton; runs beside R2 / R3) | `apep_clips.mjs`, the manifest's clip section | AP-R1, §6 | every §6.3 clip blocked out with its names, lengths, events, RETIME, hidden spans, yaw schedules, px tracks, hand / face events; builder clip checks green; manifest v1 for AP-I2 |
| **AP-RC2** clip polish | `wip/ap-rig` | same files; names, lengths and event ticks frozen | AP-R3, AP-RC1 | key poses vs `MP3` sheet 03 (P3) and the `MO` kp sheets (P1); the unfold strip; checks green |
| **AP-ORG1** objects block-out | `wip/ap-org` from M0, `wt_org`, `rp_org` | the org files (§3.5) | AP-SPEC | every §5 object with looks, clips, key functions and the manifest (footprints, offsets, shield sizes); budgets; key functions run on passengers in the harness |
| **AP-ORG2** objects polish | `wip/ap-org` | same | AP-ORG1 | renders at 3 b and 8 b vs `MP3` 07 / 08 and the `v3` / `v4` frames; dome inside / outside; Heart arrival / play / pedestal; renders to the user with AP-R3 |
| **AP-FX** kit | `wip/ap-fx` from M0, `wt_fx`, `rp_fx` | `tools/build_mboss_ap_fx.py`, `tools/mboss_ap_fx_paint.py`, `tools/mboss_ap_fx_manifest.json`, `S:ap/ap_fx_api.md`, `S:ap/fxtests/**`, `S:ap/fxrender/**` | AP-SPEC | every §8 preset / telegraph / prop / sound / HUD element of the call list; Dendro palettes; the gold-orange homing wheel; the banner with the red phrase; white-out; badges; gold bar glyphs if FN-24 lacks; renders; kit suite green; ≤ 0.35 M new px; fg-kit sprite references checked |
| **AP-ARENA** theme | `wip/ap-arena` from M0, `wt_arena` | `tools/mboss_arena_ap_oasis.py`, `S:ap/arenarender/**` | AP-SPEC (theme interface) | `arena_layout()` of both looks rendered (top / iso); opaque floor y 192-200 inside r 26; look diffs as fill boxes ≤ 32 768 in ≤ 24 slices; `props(look)`; `entrance_layout()` rendered; plugged into AZ-CM's generator at AP-I1 |
| **AP-FW** (only for gaps) | `wip/cm-ap` from main after AZ-CM, `wt_cmap` | the shared files of any FN item AZ-CM did not deliver, with cproto test cases and identity | AZ-CM | reviewed like CM-REVIEW, merged into main before AP-CORE relies on it. If AZ's CM branch is still open, the request goes to its owner instead (one owner per shared file) |
| **AP-CORE** module core | `wip/ap` from main (AZ-CM + AP-FW), `wt_core` | `tools/build_mboss_apep.py`, `tools/mboss_apep/{__init__,api,core,ai,stub_rig,stub_org}.py` + stub manifests, **stubs** of `p1 p3 aftermath revival org seq` (ownership passes at I1), Apep registry entries, `S:ap/ap_contract.md`, `S:ap/tests/{apsim.py,test_apep.py,test_e2e_apep.py,run_all.sh,gen_check.py,ident.py,vcheck.py,baseline/}`, `S:ap/balance/**` (agent skeleton) | AZ-CM (+ AP-FW) | lifecycle E → P1 → T1 → P2 → CS → P3 → D with stub patterns; RES; pools / floor / titles; deciders; proxies and capsules per form / stance; body park; bars; music; §7.2 per phase; test ids; harness extensions; suites green |
| **AP-I1** wire | `wip/ap` | merge commits; kit hooks (uninstall → `fx/uninstall`; cleanup → `fx/clear` + `fx/hud/clear`; pause → `fx/tele/clear` + `fx/hud/flash_end`; death_start → `fx/tele/clear`; HUD lines → kit); `api.K` switched to the kit; stub org dropped; the theme plugged in; contract freeze | CORE, ORG1, FX, ARENA | `run_all.sh` green; rebuild ×2 no diff |
| **AP-P1** / **AP-P3** / **AP-REV** | `wip/ap-p1` / `wip/ap-p3` / `wip/ap-rev` from I1 | `p1.py seq.py` + `S:ap/tests/pat_p1.py` / `p3.py aftermath.py` + `pat_p3.py` / `revival.py org.py` + `pat_rev.py`; renders `S:ap/renders/<stage>_*`; core / api changes only through `S:ap/requests/<stage>.md` | AP-I1 | per-pattern suites green on the stub rig manifest (each `pat_*.py` exports `TABLE`); telegraph renders |
| **AP-I2** integrate | `wip/ap` | merge commits; the real rig manifest (stub rig dropped); requests applied; registry `route: true`; README Apep section | RC1 (RC2 when ready), P1, P3, REV | rebuild ×2 no diff; `run_all.sh` green; identity; storyboards per pattern on the real rig; RP built into `S:ap/rp_ap` |
| **AP-REVIEW** (5 parallel, read-only) | — | `S:ap/review/<area>/findings.json` + repro scripts | AP-I2 | state / lifecycle (every phase × pause, reload, cleanup, uninstall); fidelity vs footage; fairness (`apfair`, §9.7); perf / budgets (commands per tick, entities, atlas, DP size); model (renders vs references, incl. the user's feedback) |
| **AP-FIX** | `wip/ap` | by finding: core → rig → kit → patterns, then **one balance fixer** with write access to `api.DMG`, `api.REV`, the AI weights and the pattern files | AP-REVIEW | every confirmed finding fixed with a regression test; §9.7 holds |
| **AP-VERIFY** | read-only, then small fixes | — | AP-FIX | rebuild idempotency; `run_all.sh`; identity; the wind-up / area before-after table re-derived from the generated functions; final renders; the fairness re-run; merge into main (after Azhdaha's merge), build stamp, RP zip, renders to the user |

---------------------------------------------------------------------------------------------------

## 11. Dependencies on the Azhdaha chapter mode, and merge order

1. **M0**: main after the `wip/fg` merge (QUEUE item 2).
2. **RIGLIB** (AZL AP-5, one owner, `wip/riglib` from M0) → main early. AP-R1 consumes it; until then the temporary
   `apep_shape.mjs` (R20).
3. **AZ-CM**: AZ `S1-CM` (`wip/az-cm`, with the chapter-mode proto boss `cproto` and the generic `test_chapter.py`) →
   CM-REVIEW → main. `S:ap/framework_needs.md` is Apep's input to it: every MUST item, and the SHOULD items AZL already
   accepted (AP-2 … AP-8), with the names given there.
4. **Now, from M0, in parallel**: AP-SPEC (first), AP-R1 → {AP-R2 ×5, AP-RC1} → AP-R3 → AP-RC2; AP-ORG1 → AP-ORG2; AP-FX;
   AP-ARENA. These add new files only, so they never conflict with AZ's branches.
5. **After AZ-CM is on main**: AP-FW (only for gaps) → AP-CORE. If AZ-CM slips, the content stages continue and AP-CORE
   waits; nobody forks `build_mboss_core.py`.
6. AP-I1 (CORE + ORG + FX + ARENA) → AP-P1 ‖ AP-P3 ‖ AP-REV → AP-I2 (+ RIG) → AP-REVIEW → AP-FIX → AP-VERIFY.
7. `wip/ap` merges into main **after the Azhdaha module's merge** (whichever boss lands second rebases; their module files
   are disjoint; the registry JSON holds one key each). Identity baselines are taken on M0 + RIGLIB + AZ-CM.

FN items each Apep stage relies on:

| stage | FN items |
|---|---|
| AP-CORE | FN-1 … FN-13 (MUST); FN-20, FN-21, FN-22, FN-23, FN-24 for the lifecycle and HUD |
| AP-P1 | FN-18 (`#pjNoDodge`), FN-19 (`lockv`), FN-20 (`mv/local`), FN-21 (capsules) |
| AP-P3 | FN-14 (mask + safe group), FN-15 (‰ hazards), FN-16 (`pl_dot`), FN-17 (no-reaction), FN-19, FN-21 (`push/ring`), FN-22 (cine) |
| AP-REV | FN-7 (aux RES), FN-16, FN-17, FN-22, FN-23, FN-24, FN-26 (barrier safety sweep), FN-29, FN-30 |
| AP-ARENA | FN-3 (theme interface, looks) |
| AP-R* | FN-25 (RIGLIB), FN-8 (the px schema) |
| AP-FX | FN-28 (font allocation), FN-27 (atlas gate) |

Parallelism: 4 CPUs, ≤ 2 agents per workflow, several workflows (QUEUE note).

---------------------------------------------------------------------------------------------------

## 12. Tests

### 12.1 Harness

`S:ap/tests/apsim.py` on AZ's real-engine harness (S1-HARN) with: passengers (`ride`, `execute on passengers | vehicle`),
`rotate`, a block map with `fill` / `setblock` and barrier collision for the agent, a per-tick command counter,
parameterized level and pools (L18, ≈ 7235 HP) and a Lv15 player, interaction proxies (AZ). Rig / org stubs while
unmerged, with call logging.

### 12.2 Test ids (`test/pattern {id}`)

| id | action | id | action |
|---|---|---|---|
| 1-6 | P1-P6 (5 = the double tail) | 8 | R + P4 |
| 9 | P6 with 4 hits | 20 | enter T1 / phase 2 |
| 21 / 22 | Heart +25 % / −25 % | 23-28 | spawn one basic ×4 / 수호 / 둥지 / 양육 / 포식성 / 파괴 |
| 29 | force the time-out | 30 | skip to phase 3 (through the CS) |
| 31-35 | Q1, Q2 (first cast), Q3, Q4, Q5 | 36 | Q3s |
| 37 | Q2 as a later (lethal) cast | 40 / 41 | failure strike 1 / 2 |
| 60 | CS only | 61 | stance toggle (`crouch_p3` / `stand_p3`) |
| — | framework: `test/kill`, `test/abort`, `test/lock`, `test/level`, `test/stop`, `test/chapter {id:"apep"}`, `test/chapter_ch {id,ch}` | | |

### 12.3 Suites

| suite | owner | covers |
|---|---|---|
| `test_apep.py` | AP-CORE | routing for chapter 3 (Azhdaha 1, Raiden 2 and 4+, the route flag); entrance untargetable; RES (body Dendro ×0.70, others ×0.90; organisms ×0.80 / ×0.90; reactions use their element; true damage bypass); pools 53 / 47 and the 1 % floor; transition at the next decision; titles / bars per phase; proxies per form and stance (`p1`, `p3u`, `p3c`, `burrowed`, `aloft`, `parked`); capsule push; body park (the arrow box test misses it); one hit per swing via proxies; deciders (zones, bands, BACK dwell, rim rule, cooldowns, no repeat, chains + 20 t gap, Q2 schedule); §7.2 pause / reload / cleanup / uninstall in every phase; `test/level` re-split; chapter clear and lose paths |
| `pat_p1.py` | AP-P1 | per pattern (`TABLE`): hazard kinds, sizes (×1.2), tells ≥ 10, played ticks vs the manifest, groups, coefficients and raw values, decal == hazard, jumpable ⇒ `mbHzY1 ≤ 7`, dash-only ≤ 2 per 40 t, wedge sweeps hit a grid of standing players exactly once, homing wheels vs a dashing agent (hit) and a side-dashing agent (miss), quantized pj speeds, the 23 t disc fill, the double tail, combo lengths, burrow inv / proxies / husk scale, anchor clamps |
| `pat_p3.py` | AP-P3 | Q1-Q5 and Q3s likewise; stance changes and proxy rebinding; Q2: dome count / spacing / placement (dome A at 7 b; nearest dome ≤ 9 b at the banner), footprints at the banner, the mask in the safe group (inside any dome safe, outside hit), ticks non-lethal and ≤ 5, the blast 80 % lethal, the first cast non-lethal + its line, the 20 t window (leaving at t160 is hit, at t180 not), the dome heal, dome windows ≥ 85 t, reload / pause cancel |
| `pat_rev.py` | AP-REV | `REV` arithmetic per event; 3 attack slots; cap 6 and the 30 s wave clock; time-out at 100 s and the 파괴 cadence; spawn rules; shield pool 5× + Pyro ×1.5; 양육 reading A and the B switch; −40 % per linked loss; swallow → no progress + link loss; 파괴 killed vs blast; bite order; walls (recorded blocks, `replace air`, never in the player's box + 1 b, ≥ 2 gaps, never during a fuse or chain, cleared exactly on timeout / pause / reload / cleanup / death / CS / failure, the rim barrier intact); bolt body-block and the 1.5 b Heart end; aux kills pay nothing; failure strike 1 (25 % non-lethal, wave 1, the hint) and 2 (lose); the Ronova edge; reload in every stage state; the command budget at the cap |
| `test_e2e_apep.py` | AP-CORE, extended by AP-I2 | chapter-3 run → entrance → gate (waits for the look restore) → arena → E → P1 → T1 → P2 → CS (look swap, heal) → P3 → kill → ×15 gold + 2 sapphires + 40 XP, no boxes → next-chapter object; a lose variant (two Heart failures) |
| `test_ap_rig.py` + `check_ap_manifest` | AP-R1 … RC2 | R5 bounds, R3 residuals, R4 counts, R6 extents, R7 coverage, R9 hidden tops, R12 untinted faces, R13 / R14 budgets, the §6.1 clip checks, park |
| `test_ap_org.py` | AP-ORG | models, budgets, key functions on passengers, footprints vs sockets |
| `test_ap_arena.py` | AP-ARENA | layout, opaque floor depth, look diffs (boxes ≤ 32 768, ≤ 24 slices), stamp + look storage, props per look, the rim barrier never inside a sweep span |
| `test_ap_fx.py` | AP-FX | kit functions, sound recipes, HUD glyphs, the homing-wheel look, budgets |
| `test_chapter.py` | AZ-CM (cproto) | the framework side, run unchanged on Apep's branch |
| perf probe | AP-CORE, AP-REVIEW | commands per tick over the worst timelines (P2 at the cap ≤ 800 average; any tick ≤ 3000); arena entity count ≤ 400 |
| atlas gate | AP-I2 | the custom items-atlas sum with both chapter bosses ≤ 15.8 M px |

### 12.4 Fairness sim

`S:ap/balance/apfair.py` + `batch.py` (copies of AZ's sim of record), presets `apbase`, `apdash`, `appos`, `apttk`,
`aprev` (phase 2 only), `apaft` (Q2 only), plus the Guardian calibration run; output `S:ap/balance/analysis.txt` with the
§9.7 table filled. The P2 module is validated against `S:ap/plan_work/p2sim_rev.py` (W7) first.

### 12.5 Renders and in-game checks

Rig sheets (R21), org / Heart / dome sheets, kit sheets, telegraph renders per pattern, integration storyboards. In game
once: barrier walls vs the shoulder-view avatar; passengers staying mounted after `tp`; the look-swap slices inside the
white-out (ms per slice); the P3 face vs the camera at 4-6 b (R1 fallback); decals over the water sheet; music loop
lengths; the parked body ignored by arrows and aim assist.

### 12.6 `S:ap/tests/run_all.sh`

Same shape as `S:mb3/tests/run_all.sh`: the Apep suites, the chapter / Azhdaha suites, the fieldgen / butterfly / Guardian
/ framework suites, `gen_check.py` (generator order, idempotency, reverse order, module wipes; with `RP=` every RP build
twice), `ident.py` (Guardian / butterfly / fieldgen / Azhdaha / proto / cproto outputs byte-identical to their baselines),
the validators (`check_refs`, `check_macro`, `check_nbtpath`, `tools/check_mboss_pack.py`, `lint_mc`) against a baseline
(`vcheck.py`). Three jobs at a time; one line per step; exit 1 on any failure.

---------------------------------------------------------------------------------------------------

## 13. Open questions (defaults apply unless the user says otherwise)

| # | question | default |
|---|---|---|
| Q1 | 양육: who is immune? | **Reading A**: the 양육 itself while it holds ≥ 1 link (img/14.png row "양육의 증식 생명체 버프 중", the v3 caption "막강한 저항을 얻는다 / 강화된 기본 증식 생명체를 처치하면 자멸한다", v3 25.6-25.7 s); buffed basics are killable and each costs the 양육 40 %. `NURTURE_MODE` keeps reading B. Confirm with the user. |
| Q2 | What does a Heart failure cost? | Two strikes: the 1st = 25 % max HP non-lethal + restart at 2700 from wave 1; the 2nd = death (run over). |
| Q3 | 종말의 여파 lethality | Blast 80 % max HP, lethal, 20 t window; **the first cast of each fight cannot kill**; ticks 2 % per 10 t from the banner + 20 t, non-lethal (fix 10-22f; was 3 % per 15 t from t80); domes r 4.5. |
| Q4 | Phase-3 upright size | 8.5 b; pose-lowered fallback ≈ 8.0 if the camera hides the face. |
| Q5 | Phase-2 progress values | **Kills +325 / +1400** (wiki +1.75 % / +11 %) with 3 attack slots and cap 6; Heart hits and the 파괴 blast as the wiki. One player cannot AoE-clear like a Genshin party. |
| Q6 | Phase-2 time-out | 100 s, then 1 파괴 per 30 s, at most 1 alive. |
| Q7 | 파괴 in the regular waves | **No** (wiki: the time-out punisher); test id 28 shows it. |
| Q8 | Phase-1 tail | Always two swings (`V2` §T; the wiki gives no count). |
| Q9 | Combo length | 2 / 3 / 4 hits with weights 3 / 4 / 3. |
| Q10 | "Undodgeable" thorn wheels | I-frames do not help (`#pjNoDodge`); 0.5 b/t homing with 8°/t (faster than a sprint), life 22 t; a wide side-dash can still make one miss; small damage (0.15); distinct gold-orange look + first-cast hint. |
| Q11 | Fog / sky colour per look | Off; optional datapack biomes later (needs a world restart). |
| Q12 | Cinematic camera for the CS | Off (white-out + titles; U6). |
| Q13 | Player-side reactions to boss hits | Kept (Bloom / Burning, as the butterfly), except the 종말의 여파 hits and the failure wither. |
| Q14 | Organism rewards | None (aux), energy particles only (파괴 n 4, others n 1). |
| Q15 | Barrier walls vs soft walls | Barriers (stop movement, dashes, knockback and player arrows); soft walls only if the avatar breaks in game. |
| Q16 | Shape library | RIGLIB's `mboss_shape_lib.mjs` (AZL AP-5). |
| Q17 | Music | On: phase 1 `music.overworld.deep_dark`, phase 2 `music.nether.soul_sand_valley`, phase 3 `music.overworld.lush_caves` (stereo `music.*` events, AZ's schema); off = delete the field. |
| Q18 | Phase-2 floor look | Decals only (ley-line strips + the Heart swirl), no block swap. |
| Q19 | Phase-3 damage bump | ×1.25 to start, ×1.1 if the sim lands above the band. |
| Q20 | The Heart in phase 1 | Hangs 9 b up in the entrance (the boss touches it), then is drawn up into the canopy; lowered in T1. |
| Q21 | CS length | 192 t (9.6 s) with the ember beat; the egg hangs as the orb (no water drop). |
| Q22 | Ronova revive after the 2nd failure | The stage restarts at 2700 from wave 1 once more. |
| Q23 | Organism cap | 6 alive. |
| Q24 | Phase split | Re-pool (two bars, 53 / 47 %) instead of one pool with a floor at 47 %. |
| Q25 | Healing inside the fight | CS heal 25 % max HP ("오아시스의 심장이 생명을 나눕니다") + the dome heal 1 % per 20 t; no heal orbs from organisms. |
| Q26 | The v6 surfacing shot | Kept as Q3s, a 30 % chain after 증폭의 풀 (our reading of `v5` M2 + `v6` take 1). |
| Q27 | Atlas room | If the global gate (≤ 15.8 M custom px with both chapter bosses) fails at AP-I2: halve the largest Raiden `fxg` ring sprites (a small separate task, visual check) — needs the user's OK; the alternative is an 8192 × 4096 atlas. |
| Q28 | Model sign-off timing | Renders to the user when AP-R3 + AP-ORG2 finish; clip block-out continues on the frozen skeleton; feedback becomes a change note. |
| Q29 | Hp | 290 to start; the fairness pass may move it within 270-320 (full fight ≤ 6.5 min item-less). |

---------------------------------------------------------------------------------------------------

## 14. Change notes

- **v1, 2026-10-19**: written from `plan_draft.md`, `understand/model_p3.md` and the four critiques; every decision in
  `S:ap/plan_ledger.md`. Main changes from the draft: the merged skeleton and part table (49 parts, hood hinge, robe stem,
  hand variants, P1 capsules); organisms and Heart from `model_p3`; 종말의 여파 as one 80 % blast with a window, the first
  cast non-lethal, ticks from t80, domes r 4.5 with footprints at the banner; the short 이동 돌진 deleted and the v6 surfacing
  shot added as Q3s; one-launch 증폭의 풀; faster, distinct, chip-damage homing wheels on quantized pj speeds; the solo
  revival economy (attack slots, cap 6, +325 / +1400, wiki-ratio HP, softer first failure); swept wedges, `#hzY1 7`
  jumps, the dash-budget and burst gates; the body parked in phase 2; recorded wall blocks; the look swap generated from
  theme diff lists; texture caps with tint sharing and a global atlas gate; hp 290; renders to the user when the model is
  done.

- **10-20 Telegraph rule (user), 2026-10-20** (binding for AP-P1, AP-P3, AP-REV, AP-FX on call, the `pat_*` tests).
  User (verbatim): "역장 발생 장치의 계수를 많이 올려야될 것 같아. 그리고 이건 공통된 얘긴데 보스의 모든 공격에 바닥의
  예고를 보여줄 필요는 없어. 영상에 없다면 그냥 보스의 동작을 보고 회피해야 하는 거니까 그대로 구현해줘." (The first
  sentence is the field generator's damage, done in the repo; the second is a rule for every boss, this note.)

  **The rule.** A hazard (boss or organism) gets a ground telegraph (decal, outline, ring, line, glow, crack, shadow,
  charging circle on the floor before the hit) **only when the reference footage shows one** before that hit (*keep*:
  shaped and timed like the footage, trimmed toward it where ours shows clearly more). Otherwise (*none*: no marker in
  the footage, the attack not in the footage, or ambiguous footage) there is no pre-hit ground telegraph: no kit decal,
  no framework outline (`#hzQuiet 1` stays on every hazard). Not telegraphs, so they stay: motion and wind-up clips,
  sounds, fx on the body (core glow, tail-tip flash, crown flare), projectiles / props visibly in flight or in the air,
  the attack's own visual at / after the hit (slash bands, bursts, the thorn-wheel carpet, the Q2 field and flood),
  HUD banners / sub-lines / hints, and mechanic markers the footage shows (Q2 domes, spawn markers, the Heart swirl).
  With the decal gone the kit's strike flash goes too, so every *none* row shows its impact preset at the hit tick
  (all §8 rows name one except O1: add a small hit fx there). No damage, size or timing changes.

  **What changes.** §7.11 rule 1 (telegraph honesty), rule 6's "landings that matter … with their own decal", the
  `ap_contract.md` §0.7 pairing line and the `pat_*` "decal == hazard" checks (§12.3) apply **only to *keep* rows**; P1's
  shadow and nothing else is a position marker exempt from the size match. U4 / §7.11 rule 2 (**≥ 10 t**, `tell_rt`) is
  measured from the decal for *keep* rows and **from the motion tell** (first distinguishable clip pose + sound, or the
  visible projectile / prop precursor) for *none* rows; §8.0's "telegraph of each hit" column reads that way. `TABLE`s
  get `tele` = `'keep'` | `'none'` and `tell_src` (the clip event / prop that starts the readable tell). §7.11 rule 3's
  per-tick `hz/sector` wedges stay (they are the hazard); only the matching `tele/wedge` stack goes. The fairness sim
  (§12.4) keeps its timings; its "first readable tick" per hazard becomes the decal tick or the motion-tell tick.

  | pattern / hazard | ground telegraph | footage evidence (video s) | keep: shape and timing / none: what the player reads |
  |---|---|---|---|
  | P1 burst r 4.2 | **keep**: the shadow (trim: no gold ring) | V1 A 7.75-8.80 (`sheet_burrow1`): a dark boss-shaped shadow glides under the grass and stops by the player; the burst comes out of its head; no ring | `shadow_glide` reaches the lock by t32 (12 t) with its head on the burst centre; the `tele_disc(4.2, 12, el 20)` ring is dropped |
  | P1 sweep lane | none | V1 A 9.35-10.43: towers over the player and turns; the slash streak is the hit | loom 49-61 + yaw lock t52 (12 t), `slash_band` |
  | P2 plunge r 4.2 | none | V1 H 18.95-20.62: spread, swirl, hands raised, flash at the plunge | swirl 5-27 + raise → t30 |
  | P2 stalk strips | **keep** (trim) | V1 H 22.00-22.55 (`k_f1344`): thin white-gold crack lines from each stalk toward the middle, 11-34 t before the slams | `tele/crack` crack strip + rails, tells 22 / 29 / 35 / 42 as planned, no `t_lane` progress fill |
  | P3 slams r 5.4 | none | V1 G 33.50-37.57 (`sheet_rear`), 38.90-39.10 (`sheet_slam2_full20`): coil / re-rear, flash only at the slam | spiral coil (36 t), **requirement**: slam 2's re-rear visible ≥ 10 t (footage 6-7 t), slam 3's leap |
  | P3 carpet front, homing wheels | none (the wheels are the hazard) | V1 G 37.57-38.55, V2 G 1.12-2.20 | wheel props + `wheel_carpet`; `tele/wave` (its pre-fill disc) dropped |
  | P4 disc r 9.0 | **keep** | V2 R 7.80-8.95 (`k_f0480`, `sheet_rot_disc`): pale rim circle filling from the centre 23 t; wiki "a range is shown, then it rotates" | as planned (fill 23 t, `el 23`) |
  | P5 tail swings (wedge lanes) | none | V2 T 16.00-17.95 (`sheet_tail_a`): turn, S-raise, cock; the arc trail only during the swing | S-raise t8, cock cue t23 + tail-tip flash, swing t28; recoil / coil 37-52 for swing 2 |
  | P6 combo hits 1-4 | none | V2 C 24.45-31.25 (`sheet_combo_c` 28.00-29.95): arm-back, rears, twist; furrow / cracks / spark ring come with or after the hits | arm-back 10 / rear 14 / twist 10 / tallest rear 22 |
  | Q1 burst r 4.2 | **keep** (trim) | V5 M 14.0-15.03: leaf-pad trail on the water, then a leaf rosette (Ø 14-16 m) 12 t before the burst | leaf-pad trail + the rosette's leaf ring at r 4.2 (outer petals airborne), no progress fill |
  | Q1 slam r 4.2 + tail sweep r 12 (jumpable) | none | V5 M 15.30-16.25: arc, belly-flop, the sweep ring is the hit | hoop 44-49 + roll 49-61 → slam t61, sweep t69 (one group); **concern**: the sweep is 8 t after the slam (20 t after the roll starts) |
  | Q2 field + domes + blast | mechanic: stays | V5 W 21.70-30.00, w1 2.5 | as planned; the banner footprints are ours (they mark safety, not a hit; footage light columns ≈ 76-97 t before the blast); the user may say otherwise |
  | Q3 shell 1 r 3.6 | **keep** | V5 S 33.30-33.80 (`k_f1998`, `zoom_disc_f2004`): a pale disc pops under the player before the charge (medium confidence it is the lock marker) | the pale target disc (`t_target`) following to the lock as planned, held to the impact, no progress fill |
  | Q3 shells 2 / 3 r 3.0 | none | V5 S 37.50-38.55 (own crops: only lily-pad floor curves; yellow streaks drop steeply) | **requirement**: the two shells visible high over their points from the locks (≥ 14 t) |
  | Q3s surfacing splash r 3.6 | **keep** (trim) | V5 M2 38.8-39.55 + V6W take 1 0.60-0.75: leaf-pad trail and a leaf splash at the surfacing spot | leaf-pad trail + leaf ring, no progress fill |
  | Q3s shell r 3.0 | **keep** | V5 39.60-39.85 (`zoom_disc_f2382`): the pale disc under the player after the sink | pale target disc at the player (12 t) |
  | Q4 tail swings | none | V6W 2.2 3.10-5.65: coil + spin, rear + lunge; the crescent only during the swing | cock 0-11 + tip flash → t14; rise + lunge → t46 |
  | Q5 landings r 2.0 (2 × 6) | none | V6W 2.3 11.00-12.25 (`sheet20fps_t3_spikes`): star flares on the orbs, helix trails, impacts; no floor markers | orb flare at each lock + the visible flight (12 t) |
  | Q5 leaf blades | none | V6W 12.50-12.80: blades skim in | **requirement**: blades visible from the lock (t52) before the skim (t64) |
  | O1 basic melee cone | none | V3 B 14.90-16.92: the bells lean into the Heart | lean 10 t; add a small hit fx |
  | O2 bolt aim lane | none | V3 B 16.30-17.50: crown flare, comet trail | crown flare + the bolt in flight |
  | O4 wall spots (no damage) | none | V4 C 11.70-12.37: loop pose, walls burst in one frame | loop pose 12 t |
  | O6a burst r 3.6 | none (uncertain) | V4 E 31.20-32.65 (`k_f1872`, `k_f1920`): a gold swirl under the hovering bud, which drifts before bursting (not the burst area) | inflate 10 t; the swirl stays as the bud's own glow, moving with it |
  | O6b bites | none | V4 E 35.58-38.65: lunges with a bite flash | **requirement**: a chain-start pose ≥ 10 t; single bites a 10-t lunge prep |
  | O7 blast r 3.6 | none | V4 D 19.00-21.80 (`k_f1200`, `k_f1290`): pulsing fuse, glow arc on the ball, no ground ring; the dome is the blast | fuse pulses 56 t + white-hot pre-blast 5 t + sounds |
  | E, R, T1 spawn markers, Heart swirl / ley lines, failure strike, CS | no hazard telegraph | — | unchanged |

  **Built kit assets (`wip/ap-fx`, read only here) left without a user:** `tele/sector` and `tele/wedge` with the 40 slice
  pieces (`t_pf* t_pa* t_pas* t_pe*`), `tele/line` (its geometry lives on inside `tele/crack`), `tele/wave` /
  `wave_end`, `tele/wall_spot` + `t_wall`, the `el 20` gold telegraph palette (every phase-1 user is *none* except P2's
  fixed-gold crack), `t_jump` (already unused: `nd 0` everywhere), the `tele_*` demos and test cases of those shapes.
  Still used: `tele/disc` (P4 with its fill, Q1, Q3 L1, Q3s), `tele/crack`, `tele/mring*`, `mask_wash`, `safe_rim` /
  `safe_end`, `tele/clear`, the dressing pool. Nothing is deleted now.

  **Fairness concerns** (no change made): Q1's tail sweep 8 t after the slam; Q3 shells 2 / 3 and Q5's blades depend on
  the required air cues; P3 slam 2's re-rear must be stretched to 10 t; O1's cone at the Heart and O6b's chains rely on
  poses only; the P5 / Q4 tail swings (the "hard" pattern) now show no area, only the raise, cock cue and tip flash.

- **AP-I1 freeze, 2026-10-21** (`wip/ap`, `S:ap/wt_core`; details `S:ap/ap_contract.md` §2, hand-over `S:ap/i1_notes.md`).
  1. Merged into `wip/ap`: the release line fef7e90 (chapter mode, Azhdaha released, Raiden rework under `boss/raiden`,
     tip removal, kit-font fallback, real-game fixes), `wip/ap-org` d3417c6, `wip/ap-fx` 5e7834f, `wip/ap-arena` 75b05e1,
     `wip/ap-rig` 443e5d8 (RC2) + `wip/ap-r3b` f357c7f; RC2's floor probes re-derived (only the P1 lower legs changed).
  2. **Chapter bosses live under `boss/<id>`** (user 10-21: "왜 boss 아니고 mboss에 넣어놨냐 이건 중간보스가 아닌데"): registry
     `"fn"` roots, `mboss_lib.fn_root`; Apep `F:boss/apep`, Azhdaha `F:boss/azhdaha`; tags, scores, storage and RP paths
     unchanged; test aliases `rlk:boss/test/<cmd>`. Every `AP:x` / `F:mboss/apep/x` of this plan now reads `F:boss/apep/x`.
  3. Wired: the real rig manifest (0 fallbacks, no `rig_stub/**`; the stub manifest file stays until I2), `api.K` = the kit
     (KitStub gone), the stub org dropped (the org runtime stays a stub until AP-REV), the theme, the kit hook lines of
     `ap_fx_api` §0.12 (+ the phase-2 reload redraw), the kit font's default fallback.
  4. No-tips rule (user 10-21): §3.4's 20-s failure hint, the first BACK P5 hint and Q10's first-cast hint are dropped;
     kept: the real game's 「마물을 처치해서 소생 진행도를 올리세요」 and the Q2 banner, and the instant-kill warnings.
  5. Next: AP-P1 ‖ AP-P3 ‖ AP-REV from `wip/ap` at the I1 commit **d15e500** (branches `wip/ap-p1`, `wip/ap-p3`,
     `wip/ap-rev`).

- **AP-I2 integrate, 2026-10-21** (`wip/ap` f588262, `S:ap/wt_core`; contract §3, the request files' AP-I2 status sections).
  1. Merged into `wip/ap` (all `--no-ff`, generated outputs never hand-merged: each merge regenerated with
     `build_mboss_apep.py`): `wip/ap-p1` c47ab3b, `wip/ap-p3` d2e6262 (conflict only in the generated `p/resume_d`),
     `wip/ap-rev` e599e69 (conflict only in the generated `pj_end`).
  2. **The stub rig is dropped**: `stub_rig.py`, `stub_rig_rt.py` and `tools/mboss_apep/stub_rig_manifest.json` deleted; `api`
     reads only the real rig manifest, keeps the 36 D0 clip names (§6.3, contract §0.4.10) as a list and asserts them, and
     `rig_fn` / `play_fn` assert that the rig wrote the function (no `rig_stub/**` fallback). The framework px compiler now
     reads the real manifest alone (its output `mboss/px/apep/**` is byte-identical).
  3. **Registry `route: true`** for `apep`: chapter 3's boss map is Apep; chapter 1 stays Azhdaha, 2 and 4+ Raiden
     (`mboss/cb/route`, `cb/peek`, `register` regenerated). README: the Apep section rewritten (the fight described
     neutrally, the floor-telegraph patterns listed, no advice).
  4. Requests applied (each with a test; details in contract §3):
     - RP1-1 / RP3-1: `Gen.yaw_rebase()` = `AP:yaw/rebase` (`#apYaw0 = Rotation x 100 - sign x schedule[#apYawT + 1]`);
       P5's back turn and Q1's surfacing turn call it (no pattern writes `#apYaw0` any more).
     - RP1-2 / RP3-4 / RREV-1 (RORG-3): the core's `AP:obj/tick` steps every org object's clips once per module tick (E,
       phases 1-3, D; frozen while paused), each object only while its displays exist (Heart bulb, dome shell, stalk,
       wall blade tags), **before** the stage and the main slot: a clip played at T shows key 0 at T + 1 (the semantics
       the revival and aftermath code already had). Dropped: P2's own `om/stalk/tick` span, aftermath's `om/dome/tick`,
       revival's `heart/tick` (and its calls in `rev/tick`, T1, the failure strike, the CS) and the `om/wall/tick` line of
       `wall/tick`. P2 plays each `leg_slam` 5 t (was 4) before its slam so the stalk's hit key still lands on the slam
       tick. `heart/p1_up` plays the real `heart_up` clip (then the `heart_hang` sway) instead of the 30-t interpolation.
     - RP1-3: `api.wedges(clip, t0, t1, reach, swept=True)` (P1's widening moved into the api, identical wedges for P5);
       **Q4 uses it too**: `tail_p3`'s bare wedges missed 28 / 116 sample points of the swept lanes (swing 1 / 2), 0 with
       `swept`.
     - RI1-1 / RP1-5 / RP3-6: kit `tele/disc_o` (the static rim alone, flashing on the hit; `K.tele_disc(..., fill=0)`) and
       `tele/crack_o` (rails, caps and the white-gold crack line at full length, no lane fill; `K.tele_crack(..., fill=0)`).
       Switched: P2's strips and their resume macro (`crack_o`); Q1's leaf ring, Q3 shell 1's held disc, Q3s's leaf ring
       and target disc, and their resume redraws (`disc_o`). P4 keeps its filling disc (the footage fills it); Q3's moving
       target ring (`tele/mring`) is already a rim.
     - RREV-6: kit preset `o1_hit` (a small pale-green flash, leaf bits) at the O1 strike (the vanilla stand-in removed).
     - RP3-2: the Q2 two-segment countdown on the under-bar (core `hud/bar_q2`): bossui code 2 (#FF8A3D, the warm red the
       under-bar palette has) from the banner to the blast t156, code 8 (gauge gold) to the pop t189.
     - RP3-3: kit preset `flood_part {life, part}` (every third cell of `p/flood`'s grid); Q2 draws it on t156 / 157 / 158
       (life 24 / 23 / 22, same end): the blast tick drops from 3373 to 1883 commands in the sim.
     - RREV-2: AP-REV's `revsim.py` folded into `S:ap/tests/lib/apsim.py` (installed at import; `revsim.py` is a shim).
     - RREV-3: `test_apep.py` (intro 3c / 3d on the real Heart, stage 7c-7g / reload 15a-15d with spawn markers and the
       emergence, `mod_ents` with the AP-ORG tags), `test_e2e_apep.py` (the shipped route; + the lose variant of §12.3:
       two Heart failures).
     - RREV-4: `uninstall` kills `@e[tag=rlk_ap_om]` (every AP-ORG display).
     - RREV-5 (part): the core's `push/req` is skipped in phase 2 (the body is parked; 21 commands per tick). The framework
       proxy poll of the parked body stays (a framework file) for AP-FIX.
     - RP3-8, RREV-8, RP3-7: informational, no change (`#mbHitEv` is still never cleared by the core).
     - Not served (left for AP-REVIEW / the rig owner, as filed): RP3-5 (`tail_p3` swing 2 never sweeps the front).
     - Perf found by the new natural-fight probe (`S:ap/tests/soak_ap.py`), visual-only fixes: P3's homing wheels that run out
       fizzle (the one-card `spark` + gold-orange dust; a hit still pops with `wheel_pop`): slam 1's wheels run out on t163,
       slam 2's carpet tick (3108 commands); `org/burst_all` (the failure strike, the CS wilt) bursts two organisms at once
       and queues the rest two per tick (`org/burst_q` from the services' ticks; 3021 commands with four organisms).
  5. Decisions the pattern stages took inside the plan's latitude (no tick, size or coefficient change; the rows of
     §8.1-§8.3 / §7.5-§7.7 read with these):
     - P1 (RP1-4.1): the shadow glides at the predictive lock (lead 10, re-aimed at t23 / 26 / 29) as fast as the distance
       needs to be on the lock at t32 (12 t before the burst; "≤ 0.7 b/t" cannot reach a player > ~6 b away); the anchor
       stops with the rig's burst anchor (3.13 b ahead) on the lock; `p1_ring` stays at t32 (sound).
     - P2 (RP1-4.2): the plunge disc on the rig's `hands` plunge anchor (4.22 b ahead); the stalks 6.6 b from the lock at
       ±60° (near) and ±140° (far) of lock → boss, slams R-L-L-R = near right, far left, near left, far right (v1 H); a root
       beyond r 25.3 steps toward the lock; strips 3-4 made at t41 (tells 34 / 41): the per-tick budget.
     - P3 (RP1-4.3): the slams on the rig's slam anchor (4.22 b ahead of the anchor parked at the centre); the carpet and the
       wheels start there; the blade rays 1 t after each slam (perf); the two homing wheels leave the carpet front at ±12°
       of the player's bearing and steer (8°/t) from their 2nd tick while riding 0.75 b/t for 6 t, then 0.5 b/t (v1 G); a
       wheel reaches a standing player up to ~14 b out; both may hit (2 × 0.15).
     - P5 (RP1-4.4): the pre-swing turn puts the back toward the player; swing 1 sweeps the start frame's front (−61 …
       +89°), swing 2 its back (−94 … −227°); a second tip flash + cue at cock 2 (t48) marks swing 2 (readable from the
       recoil t37, 15 t).
     - P6 (RP1-4.5): hit 4's disc 7.2 b ahead of where the 2.5-b lunge glide (inside r 16) ends.
     - Revival (RREV-7): every spawn = a 20-t kit spawn marker, then the husk untargetable 10 t (emergence); tests 23-28
       spawn at once; the wave clock and the alive count include pending spawns; the due check every 8 t (at once for the
       stage's first wave); spawn points: basics 4 distinct r 12 points ≥ 4 b from the player, 수호 / 파괴 the point nearest
       10 b from the player (8-12, else 6-14, else any), 둥지 the nearest, 포식성 the farthest, 양육 the r 7 point nearest a
       basic of its wave; the shuffle bag refills when all four are drawn. Basics: melee to the wait ring r 4.5, a slot +
       the lowest free socket (r 3.4 round the cradle) asked every 10 t, the first lean 20 t after reaching the socket,
       then every 40 t; ranged stop at r 12.6, lie down (10 t), a slot every 10 t, the first bolt 20 t later; the bolt ends
       in the Heart box (the bulb box + 1.5 b), a hit on the player ends it, a dodged bolt flies on. 수호: first cast on
       becoming solid, a pool break passes the rest of the hit to the HP, a basic becoming solid within r 10 is shielded, two
       수호 keep the shields when one dies. 양육: first cast on becoming solid, re-links every 80 t. 포식성: un-empowered
       without prey (no burst, bites × 0.7); before each chain / single bite a dash to 2 b (1.5 b/t, 2 t); the chain clip
       4 t before bite 1; a single bite readable 12 t ahead (sector 10 t). 파괴: to the nearest of three stops, the blast disc
       made at contact (61 t tell), tumbles 2.5 b away during `org_die`; killed before the blast = no hazard. 둥지 walls:
       three groups at the player's facing + 0 / 120 / 240°, r 4.2 round the locked feet, blades at −20 / 0 / +20° of
       each 60° arc, barrier cells every 5°; the 30 % variant one arc at r 3.6 ahead; a cell is skipped inside the player's
       box + 1 b, within 1.5 b of an organism, within 5.31 b of the Heart or beyond r 25; blocks go at the dissolve (life
       40), blades 8 t later. The failure after a lose: the service keeps running and restarts the stage at t60 (the Ronova
       edge); no wither after the lose; the ⚠ is the kit badge U+E907. The Heart: `heart_gain` / `heart_hit` only while
       the stage runs; the CS kills the cradle / arms / sprouts at t30 and the whole Heart at t92; the stage markers are
       made at T1 t106 / phase-2 ready and removed at the white-out.
  6. Gates (contract §3.4): rebuild ×2 no diff (datapack + `S:ap/rp_ap`); `run_all.sh` (the one full run of this stage)
     with `tests_cm/test_chapter.py`; identity; the atlas gate (custom items atlas with both chapter bosses and the
     reworked Raiden); the perf probe; the real-server load check; storyboards `S:ap/renders/i2_*`. `S:ap/rp_ap` is now the
     release pack `S:rd/rp` + the Apep rig, org models, kit and boss bar.
  7. No-tips (unchanged texts): `q2_lethal`'s second clause and the time-out lines stay listed as **unsure** for the user
     (RP3-7, RREV-8).

- **AP-FIX + AP-VERIFY, 2026-10-22** (`wip/ap`, `S:ap/wt_core`; review `S:ap/review/findings.json`: 0 blockers, 3 major,
  6 minor, 5 notes; contract §4).
  1. **Release head merged first**: 46ae53a (Raiden 10-22a..c, the Plane of Euthymia arena) into `wip/ap` (2a2dd58, clean:
     Raiden files, the README and the stamp only).
  2. **Fixes, in the plan's order, each with a regression test** (scratchpad suites; backups `*.pre_fix`):
     - core (f9e9e22): RV-06 the two entrance gate crystals wear the kit's `fx/prop/gate_crystal` (foot on the floor;
       test_apep 21a); RV-13 a `/reload` in the CS before t80 runs `svc/heal_cs` once (`api.CS_HEAL_T`; 21d); RV-12 (optional
       part) `hz_vis` computes nothing when no pattern routes (21e). The framework proxy poll of the parked body stays (a
       framework file; no budget problem).
     - rig (82943f2): RV-01 / RP3-5 `tail_p3` yaw knots [13,0] [21,200] [24,200] [36,0] [45,−17] [51,−204] [53,−230]
       [57,−230] [86,−360] (was [13,0] [21,200] [45,200] [53,0]): the body unwinds to face the player during the S-coil,
       lunges facing them, and swing 2 carries the tail line from about +75 to −70° across the front (v6w 2.2). Events,
       lengths, RETIME and poses unchanged; `api.wedges(swept)` regenerates the lanes. Contract §0.4.5's knot table and
       `S:ap/spec/validate.py` follow (a D0 contract change). Grid: swing 2 hits 12 of 15 points (was 1). Render
       `S:ap/renders/i2_q4.jpg`.
     - kit + arena (5c1eed4, 6a811e4): RV-05 the 파괴 fuse ring is a camera-facing card on the ball, not a flat ripple under
       it (pat_rev 8c2); RV-08 inside the barrier ring the lush look maps dead bush / tall dry grass to lily of the valley /
       pink petals (no collision, not biome-tinted), azaleas stay beyond the barrier (test_ap_arena L: no reachable cell
       turns colliding at a swap); the kit gains `fx/snd/q3_lock` (beacon.power_select + breeze.charge) for RV-02.
     - patterns (d57f9ab): RV-02 Q3 shells 2 / 3: at each lock the q3_lock sound at the point, the shell slides to 5 b over
       it (4 t, was 10 b) and falls onto it (9 t), the streak from 2.9 b; 14 t from the lock to the hit, no floor decal
       (pat_p3 3e / 3e2 / 3f). RV-01 (pattern side): the Q4 lunge stops 4 b short of the player (0.5-b steps, ≤ 3.5 b), so a
       player 5-8 b in front ends 4-4.5 b in front of the lunge end and swing 2 hits it once (5g; without it the lunged-at
       player stood inside the root zone). RV-07 the body and the rig stay parked under the white-out until t32 (`p/cs/rise`:
       unpark + p3 look + UPRIGHT + the revival clip in one tick; 21b: no part shows at t24-90). RV-10 the CS resume hook
       re-sends the white-out with the ticks left and the green flash (21c). RV-09 the lose shows 「소생 실패」 alone; the
       "다시 한 번 실패하면 쓰러집니다" warning only on strike 1 (pat_rev 10f2).
     - balance (8833dc7), the one pass (below).
  3. **The fairness harness (RV-03)**: `S:ap/balance/apfair.py` is azfair's agent (vendored unchanged as `azfair_core.py`)
     on the AP harness world, with the Apep parts (organism targets and the plan priorities, the "nearest" agent skipping
     immune 양육, melee cleave, the walls as collision, the Q2 dome / late / early agents, FRONT-mid / BACK policies);
     `batch.py` presets `gd apbase apdash appos apttk aprev apaft`; `analyze.py` writes `S:ap/balance/analysis.txt`. The
     Guardian calibration on this harness reproduces `S:az/harness/guardian_m0.txt` seed by seed (159.6 / 119.8 / 100.7 %
     max HP per minute). Before the pass: P1 1.05 / 1.45 / 0.98×, P3 2.29 / 2.06 / 2.58× the Guardian (stand / melee walk /
     ranged walk), the P6 combo 85 % of max HP in one cast, the worst 40 t window 55-59 %.
  4. **The balance pass** (`api.DMG` ×100): P1 108 / 125, P2 67 / 85, P4 85, P6 55 / 67 / 50 / 77, Q1 56 / 60, Q3 52 / 45, Q3s
     32 / 52, Q4 52 / 56, Q5 48 / 24; P3, P5 and the organisms unchanged. `api.REV`: basic kill +300, special +1300, basic hit
     −54, buffed −108. AI weights unchanged (§9.3 / §9.5 carry the values). §9.7 after the pass (analysis.txt, 30 of 34 rows):

     | row | value | target | |
     |---|---|---|---|
     | P1 stand / melee walk / ranged walk vs the Guardian | 0.83 / 1.00 / 0.78× | 0.72-1.08× | ok |
     | P3 the same | 1.03 / 0.75 / 0.88× | 0.72-1.08× | ok |
     | whole fight HP lost, melee walk sword / ranged walk bow | 467 / 348 % of max HP | ≤ 334 / 252 | **not met** |
     | worst 40 t window, walkers | 43.7 % | ≤ 45 % | ok |
     | one cast, stand agent (Q2 blast excluded) | 56.7 % | ≤ 60 % | ok |
     | undodgeable share, walkers | 4.4 % | ≤ 25 % | ok |
     | perfect dasher P1 / P3 | ≤ 17.1 / 0.0 %/min | ≤ 35.9 | ok |
     | positional (FRONT-mid vs BACK melee walker) | 86.4 vs 80.7 (front 7 % more) | ≥ 25 % less | **not met** |
     | Q2 dome walker: blast hits / ticks / deaths (18 casts, 9 seeds) | 0 / 0 / 0 | 0 / ≤ 2 / 0 | ok |
     | Q2 late agent deaths / early leaver deaths | 0 / 0 | 0 / 0 | ok |
     | P2 length: sword / items ×1.75 / bow ×2.5 | 100.4 / 56.3 / 29.3 s | 85-120 / 50-75 / ≥ 30 | bow ×2.5 0.7 s short |
     | P2 failures: sword / bow / catalyst (0.64×) / nearest | 0 / 0 / 0 / 0 of 9 | 0 / 0 / 0 / ≤ 1 | ok |
     | P2 idle agent: the Heart at 0 | 42.3 s | 30-45 s | ok |
     | P2 HP loss vs P1 | 15.1 vs 120.1 %/min | ≤ 0.8× | ok |
     | full fight, item-less sword | 5.95 min | ≤ 6.5 | ok |
     | apfair P2 vs p2sim_rev W7 | 100.4 vs 105 s (−4.4 %) | ±15 % | ok |

     Not met, for the plan owner: (a) the whole-fight gate cannot hold together with the per-phase band at the fight length
     this plan sets (P1 + P3 ≈ 4 min at the 0.72× floor already gives ≈ 360 % for the walker); (b) the positional row: the
     FRONT-mid melee walker stands in the same zone and band as the ranged walker, so weights that spare FRONT-mid also drop
     the ranged row below 0.72×; P1 잠복 돌진 (a dash check) is most of both; the BACK walker escapes P5 because the agent reads
     the quiet wedges from their make tick (AZ FAIR-4 / FAIR-21); (c) bow ×2.5 is spawn-cadence bound (four waves either
     way). The P3 coefficients are now small (≈ 0.5); the alternative (longer recover windows in P3) is a pattern change.
  5. **Not changed**: RV-11 `q2_lethal`'s second clause "— 보호막 안에 머무르세요" stays (unsure under the no-tips rule; listed
     for the user with RP3-7 / RREV-8); RV-12's framework proxy poll; RV-14 RRIG-5 (a lowered crawl pose) and the §12.5
     in-game checklist (needs a client): open.
  6. **AP-VERIFY gates**: see contract §4.3.

- **Fix 10-22f (user feedback on the real game), 2026-10-22** (build " · 빌드 10-22f 아펩 패턴 수정"; contract §5).
  User (verbatim): "아펩의 '초목이 시든 풍경' 패턴이 어색해. 바닥에 예고 원이 차오르는 거랑 보스가 휘두르는 모션이랑 안 맞아."
  and "'종말의 여파' 패턴은 보호막에 들어가기 전부터 장판이 깔리면서 조금씩 딜이 들어와야 하고, 보호막이 생성되는 위치는 일정
  범위 안에서 랜덤이어야 해.(정삼각형이 되지 않도록) 그리고 보호막 사이 거리를 좀 늘려". Clip `S:ap/user_refs/ingame_1022.mp4`.
  1. **P4** (§8.1): measured before: the fill full at t40 = the hit, the crash a vertical drop of the A claw at t40 (0°/t),
     the spin from 47 (visible ≈ 50), the sweeping claw at the player's side at t63 (+23 t); in the clip the hurt flash comes
     with the full fill while the visible swing starts ≈ 12 t later. Now the whirl (32-64) and the `CRASH_WIND` key (36) bring
     the claw down through the front at t40, 15°/t: fill full = hit = contact (±0 t); act 31 → 24; the rest unchanged.
     The `rotation` row of §6.3 / contract §0.4.10 (events, yaw knots, the `hand_a_r` track) changed: a D0 change, the
     frozen stub and `validate.py` follow.
  2. **Q2** (§7.8, §8.3, §9.3, Q3): the field from the banner (ticks 2 % / 10 t from B0 + 20, never lethal, 15-20 ticks =
     30-40 % for a player who never enters a dome), the domes on the pattern clock (B0 + 34 / 38 / 42, the player's first;
     two ticks before any dome), random layouts from a table (centres 7-17.4 b, 14-30 b apart, never near-equilateral, the
     player's dome ≤ 9 b; ≤ 9.3 at the barrier). §9.7's dome-agent gate becomes ≤ 3 ticks (the two pre-dome ticks + 1).
  3. Tests (scratchpad, backups `*.pre_1022`): pat_p1 P4a-P4i, pat_p3 Q2 / place (7a-7r, 8a-8c), test_apep 14d / 15f,
     test_e2e_apep 6a-6c; renders `S:ap/renders/fix1022_{p4_sync,p4_timing,q2_layouts,q2_field}.png`.
  4. Fairness (`S:ap/balance/analysis.txt`, labels b1022 / aft1022 + the untouched P2 `fin` and the previous whole-fight runs):
     Q2 dome agent 0 blast hits / 2 ticks per cast / 0 deaths (3.7 % max HP per cast); late agent 0 deaths (≤ 7 ticks,
     ≤ 13.1 %); early leaver 0 deaths (83.6 %). P4 per minute: melee walk 28.5 → 23.2, stand / back / front unchanged.
     The one-cast row now excludes the Q2 blast properly (45.1 %, P6). New FAIL: P3 stand 186.5 %/min = 1.17× (was 1.03×;
     band ≤ 1.08×): the stand agent never enters a dome and eats the whole field. Not tuned (the user's DoT as asked);
     1 % per 10 t would bring it back to ≈ 1.07×.

