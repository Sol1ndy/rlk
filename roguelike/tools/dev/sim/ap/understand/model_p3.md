# 아펩의 오아시스 파수꾼: phase-3 model update (기원 form, crawl form, organisms, Heart, corrected part plan)

This is an addendum to `understand/model.md`. That study was written before the phase-3 footage analyses (`v5.md`,
`v6w.md`) and before the organism study (`v4.md`). This file replaces model.md wherever the two disagree:
* model.md §1.2 (phase-3 sizes);
* §2 "P3 upright";
* §4 (phase-3 parts and the P1/P3 table);
* §6 (organism sizes and colours);
* §7.2 (phase-3 palette);
* §9 (part table, rest poses, proxies).

Phase 1 (§3, §7.1) stays as written.

Binding numbers (wiki.md): the Warden in phases 1 and 3 has Dendro RES 30 %, the organisms have Dendro RES 20 %, and
everything else is 10 %. The 양육 "+9900 %" is a mechanic (the target cannot be damaged), not a model state. The model does
not depend on any of this.

Notation:
* `v6 f480` is 60 fps frame 480 of v6. `w1 f127` and `w2 f436` are 25 fps frames.
* b = Minecraft block (1 m = 1 b), H = phase-3 height to the hood top.
* Rig space: +X = the boss's left, +Y up, −Z forward, origin on the floor at the anchor.
* Her left/right are the boss's own sides.

## Files

| what | where (all under `S:ap/understand/`, S = the scratchpad) |
|---|---|
| this report | `model_p3.md` |
| annotated sheets | `model_p3/01_p3_upright_parts.jpg`, `02_p3_crawl_parts.jpg`, `03_p3_stances_sequences.jpg`, `04_p1_vs_p3_mapping.jpg`, `05_p3_proportions.jpg`, `06_p3_palette.png`, `07_organisms.jpg`, `08_heart.jpg`, `09_rig_skeleton.png`, `10_best_reference_frames.jpg` |
| my full-res frames (extracted frame-accurately with ffmpeg `select=eq(n,N)`) | `model_p3_work/full/<v>_f<NNNN>.png`. There are 269 frames: v5 73, v6 55, w1 29, w2 38, v4 46, v3 11, v2 11, v1 6 |
| crops, grids, check sheets | `model_p3_work/crops/` (`g_*` = 50/100 px grids in full-frame pixels, `z_*` = zooms), `model_p3_work/s_*.jpg`, `ov_*.jpg` |
| data | `model_p3_work/palette_p3.json` (ramps + sources), `model_p3_work/rig_plan_p3.json` (part table + joints) |
| tools | `model_p3_tools/`: `grab.py` (frame-exact grab), `sheetlib.py` / `annot.py` (sheets, markers, legends), `crop.py` (grid crops), `pal.py` (k-means palette in a box), `dehaze.py`, `size_fit.py` (pinhole sizes), `rig_joints.py` (both rest poses), `rig_plan.py` (part table → JSON), `s01..s09_*.py` (rebuild every sheet) |

---------------------------------------------------------------------------------------------------

## 0. Key findings and corrections to model.md

1. **Phase 3 has two stances on one body.**
   * **Crawl form**: the phase-1 hunched six-limbed body, re-skinned. It moves, burrows, fires shells and swings the tail.
   * **Upright form**: thorax vertical, the hood swung back, the glowing face shown, three arm pairs spread. It casts
     생명의 나선, idles, and casts 종말의 여파.

   The change is a continuous 0.7 s (14 t) unfold in one take (`v6 f522→f600`, sheet 03 row 1), and the fold back takes
   0.35 s (`v6 f756→f804`). So both stances must be poses of **one rig**; a rig swap cannot play that unfold (§5).
2. **The six phase-3 arms are the six phase-1 limbs** (sheet 04). model.md §4 had this wrong: it read the middle arms as
   grown shoulder flaps and the lower pair as a leaf skirt on the ground.
   * **A**, the phase-1 long arms, become the raised "antler" arms.
   * **B**, the phase-1 front legs, become the middle arms with the big lobed leaf hands.
   * **C**, the phase-1 rear legs, become the lower arms. They leave the waist and reach down to the water with curled
     leaf hands.
   * The phase-1 mantle flaps stay mantle plates on the shoulders and back.
3. **The "trunk/skirt" is the abdomen hanging down** as a dark-teal robe stem, ending in a flared hem on the water
   (`v6 f480`, sheet 01 items 10-12). Upright, the pelvis (waist) is 3.1 b up, the thorax points up from it, the abdomen
   points down from it, and the tail root sits under the back of the waist. The tail lies on the ground behind and coils
   (`v5 f1875`, `f1908`).
4. **The face is an oval glowing mask**, about 1.9 × 1.6 b (0.22 H). It carries a gold lily/sprig emblem and a lime leaf
   scarf under the chin (`v6 f480`, `v5 f1074`, zooms `model_p3_work/crops/z_*_face.jpg`). It is not the "Ø 1.4 flower
   rosette" of model.md. It turns **orange-gold** while 종말의 여파 charges (`w1 f127`).
   * In the crawl form the same hood carapace closes over the face and points forward and down (`v6 f90`, `f165`).
   * In phase 1 the face under the cowl is the pale bud-skull (model.md §3.1).
5. **The crown is a fan of 8-10 gold leaves with a glowing yellow bud**, the phase-1 sprig grown large.
   * It sits on the hood's front edge (`v5 f450`, `w2 f436`).
   * Upright, the hood swings back, so the fan frames the top of the face.
6. **Chest: a gold segmented sternum** (6-8 chevrons, 2.2 × 0.8 b, with a diamond at the top and the navel glow at the
   bottom). It is flanked by pale grey curved rib-blades, the phase-1 pale bark plates (`v6 f480`, zoom
   `z_v6_0480_chest.jpg`). The phase-1 belly bulb is gone in phase 3.
7. **Back (upright)**: glossy bottle-green plates (`v5 f1908`, `f1875`, sheet 01 B).
   * Emerald diamonds sit at the upper back (1.0 b) and the lower back at the waist (0.8 b).
   * Small emeralds sit at both brows and on the hood.
   * The dorsal side of the B arms carries the dark carapace.
8. **Tail**: twisted two-band ribbon in **pale grey-white + dark green**. model.md had mint; the mint was haze. It is
   9.1 b in the rig, the same length as phase 1 (§1).
9. **Size: hood top 8.5 b upright** (my fit 8.6-9.9 m; v5.md 10.4 m; v6w.md 8 m; §1). The phase-1 bone lengths produce
   this height with no rescale (`09_rig_skeleton.png`; bone lengths agree within 0.15 b between the stances). The A
   tips reach 10.4 b, the B span is 10.4 b and the C span 7.8 b. The crawl form is the phase-1 crouch (hood 4.4-5 b,
   15 b nose to tail tip).
10. **Organisms** (v3.md + v4.md + my frames; sheet 07): several model.md §6 numbers were wrong.
    * The basic (기본) is 1.15 b and **neutral cream-grey**, not mint. It has a second, lying "bag" form for ranged
      shots.
    * 양육 is 2.4 b, not 1.8 b. While it buffs, a **translucent green cylinder** (r 1.3, h 0.5) stands around it.
    * 수호 is a **4.4 b** spire. I measured `v3 f2088`: 4.0-4.8 m. The v4 figure of 2.4 m is its closed bud.
    * The 포식성 (predatory) has a fish form, a bud form, an inflated pod and a closed "face".
11. **Heart**: one lemon bulb lying in a root cradle with **two tall root arms** (≈ 4 b) tipped by glowing leaf-flames
    (`v3 f0`, `v4 f1650`). It arrives as an upright egg held by a vine hand (`v2 f2200-f2418`). In the cut-scene it is a
    golden egg that turns green (`w2`). See §8.
12. **Part plan** (§6):
    * one superset rig of **46 parts** (P1 shows 44, P3 shows 46), plus 2 reserve slots (48), under the 56 cap;
    * one item-model look per form (`p1` / `p3`) on every part;
    * the two stances are poses;
    * **11 hit proxies** remapped per stance;
    * organisms are small separate item-model rigs of 1-3 displays each.

---------------------------------------------------------------------------------------------------

## 1. Sizes and proportions (sheet 05)

Method (`model_p3_tools/size_fit.py`): a pinhole ground-plane fit, as in v5.md (vertical FOV 45°, f = 1303 px).
* The camera height comes from the player. I use Barbara's true height, 1.55 m, instead of the 1.7 m ruler of the reports;
  this removes their ≈ +10 % bias.
* The horizon is not visible. I bracket y_h between 440 and 467: v5.md fitted 467-469 from two ground circles, and
  y_h 495 would put the far shore beyond 60 m.

| item | v5 f1074 (y_h 440 / 467) | v5 f2250 | v6w.md | v5.md | **rig (b)** |
|---|---|---|---|---|---|
| hood top (H) | 9.0 / 9.9 | 8.6 / 9.3 | 8 (7-9) | 10.4 | **8.5** |
| face top / chin | 8.8 / 6.3 | 7.7 / 6.2 | mask 1.8 tall | mask 2.8 | face 6.0-7.85 (mask 1.9 × 1.6) |
| shoulders (A/B roots) | 5.5 | 5.4 | — | — | **5.3** |
| waist (C roots) | 3.2 | 3.0 | — | — | **3.1** |
| B span (leaf-hand tip to tip) | 11.6 / 12.8 | 10.1 / 11.0 | 10 | 13.8-14.3 | **10.4** |
| C span | 8.5 / 9.3 | 7.6 / 8.3 | — | 10.3 | **7.8** |
| A tips (raised) | out of frame | — | 8.8 | ≥ 12 | **10.4** |
| stem base (robe at the water) | 2.3 / 2.6 | — | skirt ring Ø 7 | 3.2 | hem Ø 2.6, leaf ring Ø 6.5 (fx) |
| hood + hair width | 4.0 / 4.4 | — | 3 | 4.8-5.0 | 3.4 |
| crawl form: hood top / body | — | — | 5-6 / 12-14 + tail | — | the P1 crouch: 4.4 (crown 5.0) / 15 nose → tail tip |

Proportions as fractions of H, for the builder:
* chin 0.72, face top 0.91;
* shoulders 0.62, waist 0.36;
* stem base width 0.27, mask height 0.22, hood width 0.40;
* B span 1.2, C span 0.9, A tips 1.2.

**Why 8.5 b.** The fits give 8.6-9.9 m with the true player height, and the phase-1 skeleton stood up gives exactly 8.5 b
(§6.2). A larger P3 would need rescaled bones, which breaks the one-rig unfold. At 8.5 b the boss towers over the 1.8 b
player at the 4-6 b fighting distances (it fights 2-12 m from the player in v6). It fits the culling box (height 12) and the
r 26 walk disc.

## 2. Phase 3, upright form (sheet 01; best frames `v6 f480`, `v5 f1074`, `v5 f2250`, `v5 f588`, `v5 f1908`)

Silhouette: a candelabra or tree-spirit from the front. A dark hooded head carries a glowing gold-lime face over a gold
chest. Three arm pairs fan out:
* A, thin, raised like antlers;
* B, long and horizontal, with huge yellow leaf hands;
* C, curling down to the water.

A dark robe stem stands on the water, and a striped tail trails behind. From behind it reads as a dark armoured insect
with emeralds down the spine.

Numbers below match `01_p3_upright_parts.jpg`.

### 2.1 Head
1. **Face mask**:
   * shape: an oval, 1.9 × 1.6 b, slightly domed, from y 6.0 to 7.85;
   * colour: emissive gold-lime (`p3_face`);
   * markings: a gold lily/sprig emblem in the upper half (three symmetric leaves round a drop) and a pair of leaf
     shapes framing the lower half, with darker lime vein lines;
   * states: idle lit; charging orange-gold (`p3_face_charge`, `w1 f127`); dimmed when hit hard or dying (proposal).
2. **Crown**:
   * a fan of 8-10 gold leaves (#EEDE92 → #8F7D3E) radiating round the top and back of the face;
   * a glowing yellow bud in the middle (#F5F9A7, emissive);
   * this is the phase-1 crown sprig (`v1 f255`) grown into a fan (`v5 f450`, `w2 f436`).
3. **Hood**:
   * bottle-green carapace plates with lime rims;
   * upright, it is swung back behind the face like a raised hood, with a dark peak 0.6 b above the face top (8.5 b);
   * it is the same plate that closes over the face in the crawl form (§3).
4. **Emeralds**: one cut crystal at each brow (0.4 b) and 2-4 small shards along the hood rim (`v5 f1074`, `v6 f480`).
5. **Hair**:
   * 2 + 2 long strands from the hood sides down over the shoulders to the chest and waist (2.8 b);
   * dark bottle green with a lime streak;
   * the phase-1 drapes.
6. **Scarf and collar**: a lime leaf scarf wrapping the chin and throat over a grey-green collar.

### 2.2 Torso (the ventral side faces forward when upright)
7. **Gold sternum**: a segmented plate, 2.2 × 0.8 b, from the collar to the navel.
   * It has 6-8 chevron ribs and a diamond at the top.
   * It is emissive pale gold (`p3_sternum`) and brightens in charges.
8. **Rib-blades**: pale grey curved blades curling round the chest from the back, dark-outlined, with wood-grain swirls
   (the phase-1 pale bark plates).
9. **Navel**: a gold glow at the waist (part of the sternum display).
10. **Robe = abdomen**:
    * dark teal (`p3_robe`) with olive-gold curl inlay;
    * it hangs from the waist (3.1 b) to the water as a 2.3-2.6 b wide stem.
11. **Robe emblems**: white diamond emblems on the robe front (`v6 f480` y 615).
12. **Hem**: pointed dark flaps flaring onto the water. A ring of glowing leaves (Ø 6.5-7.5) lies on the water round the
    stem (fx, v6w.md).

### 2.3 Arms (A, B, C; sheet 04 shows each one's phase-1 counterpart)
13. **A, upper arms**:
    * from behind the shoulders (5.5 b), curving up and out like antlers to 10.4 b;
    * thin pale shell clad in lime leaf blades, ending in forked leafy tips;
    * they wave slowly in idle.
14. **Cones**:
    * gold cones (`p3_cone_gold`) at the A and B elbows and the A tips;
    * cream cones (`p3_cone`) at the C hands.
15. **B, middle arms**:
    * from the shoulders (5.0 b), held out sideways and a little forward;
    * pale shell + lime leaf cladding on the front, dark carapace on the back (`v5 f1908`).
16. **B hand**: the big lobed leaf hand, 2.2 b long, the dominant shape of the silhouette.
    * Three to five broad rounded lobes in butter-yellow (`p3_leafhand`) lie over a white-grey under-leaf.
    * The under-leaf sticks out beyond the lobes as a pointed fin (`v6 f480` zoom `z_v6_0480_rhand.jpg`).
17. **C, lower arms**: from the waist (3.0 b) out and down to the water, pale shell + leaf cladding.
18. **C hand**: curled leaf hand (1.5 b) resting just above the water.
    * It carries a square-spiral glyph on the leaf (`v5 f588`) and a cream cone.
19. **Bead vines**: thin vines with rows of small white leaflets (`p3_beads`), hanging from the shoulders and the B upper
    arms, 1.5-2 b long. These are model.md's "white-bud vines".

### 2.4 Back and tail
20. **Dorsal plates**: glossy bottle green, near-black rims, lime line highlights.
21. **Upper-back emerald**: a diamond, 1.0 b, between the shoulder blades.
22. **Lower-back emerald**: 0.8 b, at the waist.
23. **Mantle plates**: dark carapace plates on the shoulders and upper back (the phase-1 flaps, 2 per side).
24. **Tail**:
    * the root is under the back of the waist;
    * it lies on the ground behind and coils (`v5 f1875`, `f1908`);
    * a twisted two-band ribbon, about 1 b thick at the root: a pale grey-white band with dark band lines (segmented,
      v6w.md) spirals round a dark-green band;
    * 9.1 b in the rig.

## 3. Phase 3, crawl form (sheet 02; best frames `v6 f165`, `v6 f90`, `v6 f99`, `v6 f528`, `v5 f396`, `v5 f450`)

This is the phase-1 body plan with the phase-3 materials (sheet 04).
1. **Hood**:
   * a long bottle-green carapace pointing forward and down, covering the face;
   * near-black rims, lime line highlights;
   * the phase-1 cowl, sharper.
2. **Square gems** in raised dark frames, on the hood front and on both shoulders: lime-gold in the fight (`v6 f90`),
   bright gold in the cut-scene (`v5 f450`). In phase 1 these were the gold gems that read as "eyes".
3. **Emerald spikes** on the hood, shoulders and spine. These sit where the phase-1 gold cones were, and the crystal
   sites are the same.
4. **Dorsal plates**: glossy bottle green with lime rims.
5. **Limbs**: pale grey shell plates with wood-grain swirls (as phase 1) under lime leaf cladding.
6. **Leaf hands**: curled like fiddleheads, with yellow tips and cream cones. In the crawl the B and C hands are the feet.
7. **Tail**: twisted ribbon. It lies coiled on the water, or arches over the back like a scorpion's (`v6 f165`).
8. **Underside**: pale grey cracked scale plates.
9. **Crown**: the gold sprig and glowing bud sit on the hood front and top.
10. **Bead vines**: hang from the shoulders and arms (`v6 f90`).
11. **Back emeralds**: as in the upright form.

Also seen:
* lime leaf plates with darker line patterns on the hood's rear/top (12);
* grey peel patches of the old pale bark (13, `v5 f450`).

Gait (`v5 f1176-f1260`): the boss walks on B and C as a spider with the hips ≈ 3.3 m up; A stays raised; the tail lashes.

## 4. Stances and transforms the rig must reach (sheet 03)

| transform | frames | what moves | rig requirement |
|---|---|---|---|
| crawl → upright unfold, 14 t | `v6 f522-f600` | Thorax pitches up ≈ 90° about the waist. The abdomen swings down to vertical. The hood hinges back ≈ 110° and shows the face. A rises; B opens sideways; C swings down and out. Mantle plates fold back, hair falls. | `hood` is a separate hinged part (§6); thorax pitch range 0 → −95°; abdomen bend 0 → +100° |
| upright → hunch → sink, 7 t + 5-12 t | `v6 f756-f804`, `v5 f738-f816` | head down, arms forward, body sinks into a leaf mound | root sinks below the opaque floor (rigtech §4) |
| arc / hoop (이동 돌진) | `v5 f909-f951` | body arched into a ring, hood leading, emeralds along the back, tail following | spine as a ring: thorax and abdomen pitch ±60° each, tail chain closes the ring |
| belly-flop + 360° tail sweep | `v5 f960-f975` | flat body, tail whips round on the ground | tail chain yaw; whole-body yaw on the anchor |
| S-coil rear (생명의 꼬리) | `v6 f282-f333` | tall S of thorax + abdomen, tail high, lunge | abdomen and thorax opposite pitch, tail S |
| curled BALL | `v5 f1470` (in the air during 종말의 여파), `v5 f2094` (after the shell launch) | all limbs and plates wrapped into a sphere | limbs folded in; mantle + hood closed; pelvis lift (hover) |
| body loop | `w1 f87-f105` | rears and loops over into a ring, then lands | as the hoop |
| crouch over the player | `v5 f1086-f1140` | half-upright, mantle spread like an umbrella, B hands planted | mantle plates spread ±60° yaw |
| charge glow | `v5 f2016-f2082` (증폭의 풀), `v6 f558` (생명의 나선), `w1 f127` (종말의 여파) | the whole body lit lime-white, a ball of light above the head; orange face in 종말의 여파 | per-part brightness 13 → 15 and face/core looks (§6.4) |

## 5. Phase 1 versus phase 3, and the one-rig decision (sheet 04)

| region | phase 1 (종막) | phase 3 crawl (기원) | phase 3 upright | shared? |
|---|---|---|---|---|
| skeleton | hunched six-limbed crouch | same | same bones, thorax vertical, abdomen down | **yes**, same lengths |
| hood | dark slate cowl, gold crown cone, mid-face cone, V, crescents | bottle-green carapace, lime rims, lime-gold front gem, emerald spikes | the same carapace swung back behind the face | geometry similar, new look |
| face | closed pale bud-skull, hidden | hidden under the hood | glowing oval mask | one part, three looks |
| crown | gold leaf sprig + seed bulb, crown cone | gold sprig + bud | gold leaf fan + bud framing the face | one part, two looks |
| gems | gold square gems on hood front + shoulders | lime-gold, same sites | same | sites shared |
| crystals | gold cones on spine, shoulders, wrists | emerald spikes | emerald back diamonds, brows | sites shared; emissive part |
| chest / belly | pale ribcage + translucent belly bulb | pale belly scales | gold sternum + rib-blades | `core` part: bulb ↔ sternum |
| limbs A/B/C | pale shell arms, dark-to-pale legs, petal feet, 3-lobe claws | + lime leaf cladding, curled leaf hands | arms: antler / big leaf hands / curled hands | same bones; new looks; hands change most |
| mantle | 2 dark flaps per side | dark carapace plates | folded back on the shoulders | yes |
| drapes / hair | dark robe ribbons to the ground | dark-green strands | hair strands to the waist | yes |
| abdomen + hem | rear body + belly ribbons | same | robe stem + hem on the water | yes |
| tail | pale + slate ribbon | pale grey + dark green ribbon | same, lying behind | yes |
| new in P3 | — | — | bead vines, leaf scarf | 2 extra parts (beads) |
| glow | belly bulb, crown seed, crescents | crown bud, emeralds | face, sternum, navel, crown bud, emeralds | `face`, `core`, `crown`, `crys_back` at brightness 15 |

**Decision: one superset rig, two looks (`p1`, `p3`), two rest stances (`CROUCH`, `UPRIGHT`).**
* **The bones are the same.** Every phase-3 part maps to a phase-1 part. The bone lengths of the two stances agree
  within 0.15 b (`rig_joints.py` check printed in this study; `09_rig_skeleton.png`).
* **The unfold is continuous.** The crawl ↔ upright change happens on camera in 14 t (unfold) and 7 t (fold). A rig swap
  cannot play that; a pose blend can.
* **Two rigs cost more.** They would mean two summons, two UUID blocks, two compiled clip sets and two proxy maps, and a
  visible pop at every stance change.
* **The P1 → P3 swap hides behind the cut-scene.** Every part changes item model at once while the screen is white
  (mechanics §2.9), so the geometry of each look can differ freely (item-model swap = new model).
* **The cost is small.** 2 P3-only parts (bead vines) sit at scale 0 in phase 1, and the face mask stays hidden under the
  hood in the crawl.

## 6. Corrected part plan

Rules (rigtech, az plan R1-R11):
* `item_display` with `item_display:"none"`, `teleport_duration 1`;
* joint at the model origin; coordinates −16..32, so reach ≤ 1.5 × scale per axis;
* single-axis element rotations;
* mirrored right side;
* culling box `width:30f,height:12f` on every part (A tips reach 10.4 b);
* `view_range 3`;
* textures ≤ 1.2 M px for the rig;
* whole-body yaw and travel on the anchor, `tol.t` 0.03 b on long parts.

### 6.1 Parts (46 + 2 reserve; data: `model_p3_work/rig_plan_p3.json`, numbers on `09_rig_skeleton.png`)

Scale = the reach + 10 % headroom, divided by 1.5. Brightness: 13 for the hide, 15 for glows.

| # | part | parent | P1 look | P3 look | reach / scale | br |
|---|---|---|---|---|---|---|
| 1 | `abdomen` | pelvis | rear body plates, pale belly scales | robe stem: dark-teal front panel, gold curl inlay, white diamonds; green back | 2.1 / 1.6 | 13 |
| 2 | `hem` | abdomen | 2-3 dark belly ribbons | robe hem flaps on the water | 1.9 / 1.4 | 13 |
| 3 | `thorax` | pelvis | hump plates, bark side plates, ribcage, shoulder hooks + gem frames | lime chest plates + pale rib-blades, bottle back, shoulder gems | 2.7 / 2.0 | 13 |
| 4 | `core` | thorax | translucent belly bulb Ø 1.4 + seed | gold sternum (6-8 chevrons) + navel | 1.2 / 0.9 | 15 |
| 5 | `crys_back` | thorax (pivot at the waist) | gold spine + shoulder cones | emerald upper/lower-back diamonds + shoulder spikes | 2.8 / 2.1 | 15 (P1 14) |
| 6 | `neck` | thorax | dark plate neck | neck + grey-green collar | 1.0 / 0.8 | 13 |
| 7 | `head` | neck | skull base | skull base + lime leaf scarf | 1.4 / 1.1 | 13 |
| 8 | `face` | head | closed bud-skull + crescents | glowing mask 1.9 × 1.6 + emblem; looks `idle` / `charge` / `dim` | 2.0 / 1.5 | 15 |
| 9 | `hood` | head (hinge) | slate cowl, ear flares, mid-face cone, V | bottle carapace + lime rims + front gem; swings back when upright | 2.8 / 2.1 | 13 |
| 10 | `crown` | hood | gold crown cone + sprig + seed bulb | gold leaf fan + bud + brow emeralds + hood shards | 1.7 / 1.3 | 15 |
| 11-14 | `hair_l_1/_r_1`, `hair_l_2/_r_2` | head → hair_1 | drapes, 2 segments to the ground | hair, 2 segments to the waist | 1.6 / 1.2 | 13 |
| 15-18 | `mantle_l/r_a`, `mantle_l/r_b` | thorax | dark shoulder flaps, pale undersides | dark carapace plates, lime rims | 2.2 / 1.7, 2.0 / 1.5 | 13 |
| 19-24 | `A_up/lo/hand_l/r` | thorax → chain | long arm: pale shell; 3-lobe claw + gem + cone | antler arm: shell + leaf cladding + gold elbow cone; leafy tip + gold cone | 2.6 / 2.0, 2.8 / 2.1, 1.3 / 1.0 | 13 |
| 25-30 | `B_up/lo/hand_l/r` | thorax → chain | front leg: dark armour → pale bark; 5-petal foot Ø 1.8 + cone | middle arm: shell + cladding, dorsal carapace; big lobed leaf hand 2.2 | 2.0 / 1.5, 2.0 / 1.5, 2.4 / 1.8 | 13 |
| 31-36 | `C_up/lo/hand_l/r` | pelvis → chain | rear leg; 5-petal foot Ø 1.5 + cone | lower arm; curled leaf hand 1.5 + spiral glyph + cream cone | 1.9 / 1.4, 2.1 / 1.6, 1.6 / 1.2 | 13 |
| 37-43 | `tail_1..7` | abdomen → chain | twisted ribbon, pale + slate | twisted ribbon, pale grey + dark green | 1.5 / 1.1 | 13 |
| 44 | `tail_tip` | tail_7 | curled hook + leaf curl | thin whip + pale leaf tip | 1.3 / 1.0 | 13 |
| 45-46 | `beads_l/r` | B_up | scale 0 | white leaflet strings on a vine (dangling, secondary motion) | 2.1 / 1.6 | 14 |
| 47 (reserve) | `core_shell` | thorax | translucent bulb shell split from the seed glow (depth order) | navel halo | 1.2 / 0.9 | 14 |
| 48 (reserve) | `crys_hood` | hood | mid-face cone split from the crown | brow emeralds split from the crown | 1.6 / 1.2 | 15 |

Counts:

| form | visible parts |
|---|---|
| phase 1 | **44** |
| phase 3 (both stances) | **46** |
| reserve | 2 |
| cap | 56 |

The remaining 8 slots under the cap are for later care, for example a second tail-ribbon layer or per-hand glow.

Changes against model.md §9.2:
* `hood` is split from `head` so it can hinge back.
* `crown` and `crys_back` are separate emissive parts.
* `hem` is new: the P1 belly ribbons and the P3 robe hem.
* The tail has 7 + tip, not 6 + tip.
* `collar` is folded into the `neck` and `head` P3 looks.
* `vine_l/r` became `beads_l/r` (dangling).
* `flap_a/b` (P3 "mid leaf arms") are dropped as a concept: the P3 middle arms are limb B.

Detail goes into elements and textures (rigtech TL;DR 1-2). The densest models are `face`, `crown`, `B_hand` (P3),
`hood` and `thorax`.

### 6.2 Rest poses (rig space, b; `model_p3_tools/rig_joints.py`)

| joint | CROUCH (P1 + P3 crawl) | UPRIGHT (P3) |
|---|---|---|
| pelvis (waist) | (0, 2.8, 1.0) | (0, 3.1, 0.2) |
| tail root | (0, 2.4, 2.9) | (0, 1.2, 0.5) |
| thorax base / shoulder | (0, 3.1, 0.0) / (0, 3.4, −1.2) | (0, 4.2, 0.0) / (0, 5.3, −0.1) |
| head / hood centre | (0, 3.4, −1.9) / (0, 3.6, −2.7), hood front (0, 3.0, −4.0) | (0, 6.0, −0.3) / (0, 7.7, −0.1) |
| hood top / crown | 4.4 / 5.0 | 8.5 / 7.9 (fan centre) |
| face centre | (0, 2.9, −3.3), hidden | (0, 6.9, −0.9) |
| core | belly bulb (0, 1.7, −1.0) | sternum centre (0, 4.4, −0.7) |
| A (root → elbow → wrist → tip) | (1.6, 3.7, −0.9) → (3.4, 2.6, −1.6) → (4.8, 0.6, −2.4) → (5.3, 0.15, −2.6) | (1.1, 5.5, 0.1) → (2.3, 7.4, 0.2) → (3.6, 9.65, 0.0) → (3.8, 10.4, −0.2) |
| B | (1.3, 2.9, −1.4) → (2.3, 2.0, −2.4) → (2.4, 0.4, −3.0) → (2.5, 0.15, −3.6) | (1.2, 5.0, −0.4) → (2.8, 5.1, −0.9) → (4.4, 5.6, −1.0) → (5.2, 6.2, −1.0) |
| C | (1.2, 2.6, 1.3) → (2.6, 2.2, 1.9) → (2.9, 0.4, 2.5) → (3.0, 0.15, 3.0) | (1.1, 3.0, −0.3) → (2.6, 2.4, −0.8) → (3.5, 0.7, −0.9) → (3.9, 0.15, −0.8) |
| tail (9 points) | (0, 2.4, 2.9) → (0, 1.5, 3.6) → (0, 0.6, 4.5) → (0, 0.25, 5.6) → (0.3, 0.2, 6.7) → (0.7, 0.2, 7.8) → (1.2, 0.2, 8.8) → (1.5, 0.2, 9.9) → (1.6, 0.2, 10.9) | (0, 1.2, 0.5) → (0, 0.3, 1.3) → (0, 0.2, 2.4) → (0.6, 0.2, 3.4) → (1.6, 0.2, 4.1) → (2.7, 0.2, 4.2) → (3.6, 0.2, 3.5) → (4.0, 0.2, 2.4) → (3.9, 0.2, 1.4) (coiled behind) |
| mantle a / b | (1.4, 3.9, −0.6) → (3.0, 3.4, 0.4) / (1.2, 3.8, 0.3) → (2.6, 3.1, 1.3) | (1.2, 5.6, 0.6) → (1.9, 3.7, 1.2) / (0.9, 5.2, 0.7) → (1.3, 3.2, 1.2) |
| hair (drapes) | (1.2, 3.2, −2.4) → (1.5, 1.6, −2.7) → (1.7, 0.2, −2.8) | (0.8, 7.4, −0.6) → (1.0, 6.0, −1.0) → (1.1, 4.6, −1.0) |
| hem | (0, 2.0, 0.8) → (0, 0.3, 1.0) | (0, 2.6, −0.5) → (0, 0.15, −0.7) |
| beads | — | (1.4, 5.5, −0.3) → (2.0, 3.5, −0.6) |

Bone lengths (crouch / upright): A 2.2 / 2.3, 2.6 / 2.3, 0.7 / 0.9; B 1.7, 1.7, 0.7 / 1.0; C 1.6 / 1.7, 1.9;
tail 9.1 b in 8 segments of ≈ 1.15 b. The hands differ because the P3 leaf hands are bigger models; the bones are equal.

### 6.3 Hit proxies (rigtech §3.3; ground columns, one HP pool; off while burrowed)

| proxy | CROUCH ground point (x, z) · w × h | UPRIGHT ground point · w × h |
|---|---|---|
| `px_head` | hood front (0, −3.4) · 2.4 × 4.5 | stem front under the face (0, −0.7) · 2.8 × 8.5 |
| `px_chest` | thorax (0, 0) · 3.0 × 5.0 | stem back (0, +0.5) · 2.6 × 6.5 |
| `px_abd` | abdomen (0, +2.0) · 2.6 × 4.0 | tail root (0, +1.3) · 2.0 × 2.5 |
| `px_tail_a` / `px_tail_b` | tail 3-4 (0.2, +6.0) / tail 6-7 (1.3, +9.3) · 1.8 × 2.0 | tail coil (1.6, +4.1) / (3.8, +2.4) · 1.8 × 1.5 |
| `px_A_l/r` | arm claws (±5.3, −2.6) · 1.8 × 2.5 | moved to the B elbows (±2.8, −0.9) · 1.6 × 6.0 (the A tips at 10 b are out of reach) |
| `px_B_l/r` | front petal feet (±2.5, −3.6) · 1.8 × 3.0 | under the leaf hands (±4.6, −1.0) · 2.2 × 6.8 |
| `px_C_l/r` | rear feet (±3.0, +3.0) · 1.6 × 3.0 | curled hands (±3.7, −0.8) · 1.8 × 2.5 |

The proxies follow the stance through the same per-clip proxy track as Azhdaha. During the unfold they slide between
the two columns over its 14 t.

### 6.4 Looks and glow states

* **Item-model looks per part**: `p1`, `p3`.
* **Face looks**: `p1_bud`, `p3_idle`, `p3_charge` (orange-gold, `w1 f127`) and `p3_dim`, all brightness 15.
* **Core looks**: `p1_bulb` and `p3_sternum`.
* **Brightness as a channel.** Per-entity brightness is a merge, not a texture.
  * `p3_lit` (the 증폭의 풀 / 생명의 나선 charge, whole body lime-white) = body parts 13 → 15 with `face` / `core` held at
    15, plus fx: the ball of light above the head is a kit card.
  * After firing, the parts drop back to 13. Seen: the post-launch "dark carapace" BALL (`v5 f2094`).
* **`dim` / withered (death, proposal)**: constant-tint item definitions on the P3 models. This needs `tintindex 0` on the
  painted faces and no new sprites (the Guardian method).
* **Burrow**: root under the opaque floor, then parts at scale 0 (rigtech §4). The leaf mound, leaf pads and rosette are
  kit fx.

### 6.5 Textures (estimate; sides multiples of 16, ≤ 512)

| set | sprites (examples) | px |
|---|---|---|
| P1 look | model.md §9.4 list | ≈ 0.22 M |
| P3 look | `hood` 160×128, `face` + `face_charge` 128×128 each, `chest` 128×128, `back` 128×128, `robe` 128×128, `leafhand_B` 128×128, `crown` 128×64, `ribs` 128×64, `hem` 128×64, `hand_C` 128×64, `sternum` 64×128, `hair`, `mantle_a/b`, `limb_A/B/C`, `tail` 64×128 each, `gem`, `scarf`, `tip_A`, `beads` 64×64, `bud`, `emerald`, `cones` ≤ 32×64 | ≈ 0.27 M |
| organisms + Heart | §8-§9 | ≈ 0.18 M |
| total | | ≈ **0.67 M ≤ 1.2 M** |

Densities:
* 64 px/b on the face, the crown and the B hands;
* 48 px/b on the hood;
* 32 px/b elsewhere.

## 7. Palette (sheet `06_p3_palette.png`, data `model_p3_work/palette_p3.json`)

How the colours were sampled:
* I took k-means clusters (`pal.py`) on boxes of my full-res frames.
* In-fight samples were de-hazed as (c − 0.15·haze) / 0.85, with haze #8CC89A for the phase-3 lake (measured on the sky
  and water) and #A89A4A for phase 2.
* The cut-scene close-ups (`v5 f396`, `f450`) are nearly haze-free and anchor the hues.
* The white balance is close to neutral: Barbara's white dress samples #E8F1F2 / #EBECF5 with a slight cool cast.

Ramps, hi → deep:

| key | use | ramp |
|---|---|---|
| `p3_bottle` | hood carapace, dorsal plates, mantle | `#8DB878 #5E8C4E #436F39 #2F5A2E #1E4426 #12301B` |
| `p3_rim` | lime rims and line highlights | `#E2F7A0 #C3EA7C #A0D45E #7EB548 #5E9238 #416E28` |
| `p3_lime` | leaf plates and cladding, scarf | `#E6EE98 #CFDC7C #B2C25C #91A444 #6C7B2F #4A5A18` |
| `p3_leafhand` | B leaf hands, A tips, C hands | `#F0EDB0 #DCDA8C #C5C770 #A7AE55 #808A3A #5A6326` |
| `p3_pale` | shell limbs, rib-blades, under-leaves, belly scales, grey peel | `#E8EAE2 #D3D6CB #BBC0B2 #9EA597 #7C8478 #5A6258` |
| `p3_line` | cel outlines, veins, wood-grain | `#7A8A3C #5E6E28 #4A5A1E #3A4716 #2A3410 #1A2209` |
| `p3_emerald` | emerald crystals (glow) | `#E2FF9C #BCF53E #8FE23E #5CC72E #3A991A #1F6614` |
| `p3_face` | face mask idle (emissive) | `#FBFCC8 #EEF29A #D8E27A #B9C95A #96A840 #6E7F2A` |
| `p3_face_charge` | face while charging 종말의 여파 | `#FFF2B8 #F8DC6A #EEC048 #D99A4C #B0703A #7A4A22` |
| `p3_sternum` | gold sternum, chevrons, navel (emissive) | `#FCFCC4 #F4F2A0 #DCDC74 #BABB52 #94963A #686A24` |
| `p3_crown` | gold crown leaves | `#F6E9AE #EEDE92 #D9C47A #BBA45E #8F7D3E #5F5226` |
| `p3_bud` | crown bud (emissive) | `#FAFDD0 #F5F9A7 #E7EF8A #D3E169 #A9C24A #7CA041` |
| `p3_gem` | square gems (hood front, shoulders) | `#FFFBB0 #FEF585 #F9F04B #F3DA49 #E2C439 #A8902C` |
| `p3_cone` | cream cones | `#F7F3C4 #F2EFB1 #E2D79C #CEC58B #B0A570 #857B4E` |
| `p3_cone_gold` | gold cones (A/B elbows, A tips) | `#FBF8A8 #F4F07A #E9E042 #D3C93A #AFA230 #7C7222` |
| `p3_robe` | robe/abdomen (inlay #C9C27A / #7F8345, diamond #F2F4EE) | `#5E7E68 #476C55 #34503F #263D33 #1A2B25 #101B17` |
| `p3_hair` | hair strands (first 2 = lime streak) | `#B8E084 #8DBC5D #5F8C40 #3A6229 #234519 #132E0F` |
| `p3_tail` | tail: pale (first 3) + dark green (last 3) | `#E2E5DC #C9CEC2 #A9B1A2 #5C6A5E #3E4C43 #28332C` |
| `p3_beads` | bead leaflets (first 3) + vine (last 3) | `#F6FAF4 #E2EDE0 #C3D3BF #6E9A58 #4C7340 #30502C` |

Changes against model.md §7.2:
* `p3_under` (lilac-grey) becomes the neutral `p3_pale`; the "lilac" was the camera's cool cast on pale grey.
* `p3_tail` mint becomes pale grey-white.
* `p3_emerald` is shifted toward yellow-green.
* `p3_sternum`, `p3_crown`, `p3_gem`, `p3_robe`, `p3_hair`, `p3_rim`, `p3_leafhand` and `p3_face_charge` are new.

Phase-2 fixes:
* `org_bell` (mint) becomes **`org_bell_v2`** `#F0EFE6 #DDDAD0 #C3C1B4 #A6A69A #87887C #66685E` (`v3 f900`, `v4 f2310`
  de-hazed).
* A green egg look, **`egg_green`**, is added: `#F0F5A0 #E0E973 #B0C950 #7FAB4D #658F4E #3F6A34` (`w2 f280`).

## 8. Heart of the Oasis (sheet 08)

**One prop, 3 displays + 1 temporary.** The source sizes disagree: v4.md gives 2.0 × 3.0 and v3.md 3.8 × 2.8 × 3 with the
cradle. I compromise between them below.

1. **`heart_bulb`**: a translucent glowing lemon seed lying on its side, 3.2 long × 2.6 wide × 2.3 tall.
   * Surface: 5-7 soft vertical ribs, a big white-yellow specular band at the upper left, an inner darker swirl, floating
     motes (`v3 f0`, `v4 f1650`).
   * Material: emissive, alpha ≈ 0.85.
   * Looks: `idle` (`heart_bulb` ramp of model.md), `egg_gold` and `egg_green` (cut-scene).
   * Arrival: an **upright egg** 2.2 × 1.8 (`v2 f2358`), so pitch 0° → 65-90°; it squashes on landing.
2. **`heart_cradle`**: 4-6 knobbly dark-brown roots gripping the bulb from below like fingers, feet splayed 1.5-2 b into
   the turf.
   * Plus **two tall root arms**, one on each side, curling outward and then over the bulb to ≈ 4.0-4.3 b (`v3 f270`,
     `v4 f1650`).
   * Colours: `heart_root` ramp (#7A6E3E … #1E1B10; v3 lit #928234).
   * Without the bulb this is the **pedestal** (`v2 f2340`), with grey smoke puffs at its base.
3. **`heart_tips`**: glowing yellow leaf-flame sprouts at brightness 15 on the root arms (≈ 4 b) and the shorter roots
   (2-3 b), swaying.
4. **`vine_hand`** (phase-2 entry only): a dark vine "hand" of 5-7 curling tendrils that lowers the egg from the canopy
   (`v2 f2200`). The w2 cut-scene uses the same hand to wrap the egg before it turns green (`w2 f230-f280`).

The **gold swirl ring** (r ≈ 3.5) on the ground is a kit decal and is always on in phase 2.

The **floor under the Heart** differs by stage:
* phase 2 in v5 is orange-red cracked earth with dark veins (`v5 f198`), the "ley-line disorder" look;
* phase 2 in v3/v4 is moss cells with root veins.

So the floor look is set by the stage, not by the Heart.

## 9. Organisms: forms, states, displays (sheet 07)

General:
* Every organism is an item-model rig riding its framework aux husk as a passenger (mechanics §2.5).
* They are seen in a heavy yellow haze; paint them ≈ 10-15 % less yellow than sampled.
* Glowing cores and orbs are at brightness 15, the rest at 14.
* Translucent shells use alpha 0.8-0.9 with alpha 0 at the sprite borders.
* Spawn: a white wireframe "ghost" dome for 4-6 t, then solid (kit + a `ghost` look).
* The white silhouettes with name tags in v3/v4 are the uploader's Elemental Sight, not a game state.

| organism | size (b) | forms / states seen | displays (look list) | corrections vs model.md §6 |
|---|---|---|---|---|
| **기본 basic** | **bell 1.15** (1.35 with the stem), Ø 0.9; **bag** lying 1.43 × 1.31 | **bell**: pale cream-grey dome, faint large facets, curled olive stem, 5-6 lobed skirt feet; walks and melees (`v3 f900`). **bag**: the same bulb lying on its side, drawstring neck, crown of 4-5 jagged pale petals. Its crown opens with a lime glow to spit the bolt (`v3 f996`). **shielded** (수호): wrapped in 2-4 translucent yellow-green leaf panes / a 1.3 b green bubble with a leaf crown on top (`v4 f186`). **buffed** (양육): brighter sheen, tethers land on the dome top | 1: `basic` (`bell`, `bag`, `bag_open`, `ghost`) + 1 overlay `shield` (green bubble + panes, only while shielded) | was 1.0 b and mint; the bag form was a "sac" with petals up; the in-game colour is neutral cream-grey |
| **양육 nurturing** | **2.4** | an S-curved stalk of dark-teal leaf ribbon with thin white rims; a cream hood-leaf curling over the top like a bent tulip; the glowing orb in the curl; a gold crystal shard on the back; pale fronds at the foot. A **translucent green cylinder** r 1.3, h 0.5 stands round it while it buffs (immune). Tethers = particles. It self-destructs into a green-yellow spark burst (`v3 f1300`, `f1240`) | 3: `body`, `orb` (br 15, pulse), `ring` (translucent, only while buffing) | was 1.8 b with a "glowing ground ring"; the ring is a raised cylinder wall |
| **수호 guarding** | **spire 4.4** (my fit of `v3 f2088`: 4.0-4.8; v3.md 4.6); **closed bud ≈ 2** (`v4 f560`, the source of v4's 2.4) | **spire**: 2-3 pale grey-white leaf ribbons wound in a helix to split points. A dark-teal sepal sheath with a scalloped hem of grey-blue lobes at the base, a gold cut crystal at the front, a glowing orb (Ø 0.4) hovering 0.6-0.8 above the tip. **bud**: collapses into a hooded bud with a glowing slit to cast. **death**: red ember burst → a black twisted two-horned wisp, 17 t (`v4 f384`, `f396`) | 2: `spire` (`spire`, `bud`, `wisp`), `orb` (br 15, bob) | was 2.4 b |
| **둥지 nesting** | 2.2 × 1.3, hovers 0.5-1.5 | a dark-teal pointed cap with a spike and a thorn fringe. A glowing yellow orb "eye" in a pale ring under the cap. Two long pale grey-teal arched sepal wings with cream curled tips (`v4 f900`, `f840`). **fly**: the wings flap V ↔ wide arch. **cast**: curls into a vertical loop. The **walls** are 3 groups of 3-5 translucent yellow-green leaf blades, 2.5-3 tall, round the player (`v4 f768`, `f798`) | 3: `cap` (+ orb, br 15), `wing_l`, `wing_r`; walls = 1 display per group (prop) | as model.md (confirmed) |
| **파괴 destruction** | Ø 1.2 (+ 0.2 spikes, 0.4 beak) | a dark teal-black armoured sphere with 8-12 dark cone spikes and pale grey bands. Its open front holds a **glowing pale-yellow disc** and a short yellow cone (`v4 f1140`). **fuse**: the disc pulses (`f1200`). **blast**: star flash → green translucent dome r 3 → a **blackened split husk** flung aside (`v4 f1320`, `f1332`) | 2: `shell` (`normal`, `husk`), `face` (br 15, pulse scale) | as model.md (confirmed) |
| **포식성 predatory** | fish 2.5 long × 1.3; bud 2.1 × 1.6; pod 3.5 × 1.8 | **fish**: a leaf-shark with a cream hood, wavy grey stripes and 2 big grey horns + 1 small; a translucent green bowl and fins with yellow-green edges; a yellow gem on the long fin; a round eye with a dark-teal ring, black pupil and cyan rim (`v4 f2070`, `f2400`). **rear/scoop** to swallow a basic (`f1818`). **bud**: a diamond of cream hood + star-shaped green bowl + yellow core, hovering over a gold swirl (`f1920`). **pod**: a tall double-lobed clam, the upper lobe opening, the core in the lower lobe (`f1956`). **bite**: spikes flare round the head (`f2130`). **closed face**: a dark-green dome with a grey horn and a yellow diamond "mouth" gem (`f2175`) | 3: `hood`, `bowl`, `core` (looks `fish`, `fish_flare`, `bud`, `pod`, `face`; the fish = hood + bowl turned 90°) | as model.md plus the `fish_flare` look |

Props in the phase-2 kit:
* the walls;
* the destruction dome;
* the shield panes (see the basic's `shield` overlay);
* the tethers and bolts (particles).

## 10. Phase-3 props that touch the model (for completeness)

* **소생의 찬가 보호막 (dome shelter)**: a translucent lime hemisphere (`v5 f1590`, `w1 f184`, `w1 f330`).
  * Its inside is patterned with vines and leaf sprigs, the rim at the base is bright, and a small sprout sits on top.
  * Its radius is 3-3.5 b (v5.md said 5-6, v6w.md 3). It is drawn as 1 `item_display` per dome at brightness 14, plus a
    light-pillar card for the tell and a pop burst.
  * mechanics §3.4 uses r 3.5.
* **Charge ball** above the head (증폭의 풀) and **seed-orbs** (생명의 나선, Ø 0.6-0.8 with a spiral glyph): kit cards, not
  rig parts.

## 11. Uncertainties and proposals

* **P3 height**: 8.5 b is the low end of 8.6-9.9 m. If the third-person camera at about 4 b shows too little of the face in
  close fights, do not rescale. Lower the UPRIGHT pose instead: thorax pitched 10° back, waist 2.8 b, which gives a hood
  top of ≈ 8.0.
* **Crown fan from the front**: in the in-fight front views the fan is mostly hidden behind the mask and reads as a sprig
  emblem plus the hood peak. The full fan is seen from behind in the cut-scene (`w2 f436`). Build the fan; at normal
  distances it shows only as a gold halo.
* **Bead vines**: whether they hang from the arms or the shoulders varies between frames. I attach them to `B_up`, with a
  pendulum for secondary motion.
* **Crawl-form hood front gem**: lime-gold in the fight and gold in the cut-scene close-up. Use `p3_gem` with brightness 14.
* **Heart size**: the v3 and v4 fits differ by ±0.6 b. The 3.2 × 2.6 × 2.3 bulb + 4.2 b root arms sits in the middle.
* **Death**: not in the footage. The proposal of model.md §10 stands: kneel, the face dims (`p3_dim`), the leaf hands
  curl, scale-out with a burst of white leaflets.
* **Phase-1 face**: unchanged from model.md, the bud skull painted on the `face` P1 look.

## 12. Best reference frames per part (`10_best_reference_frames.jpg`; full res in `model_p3_work/full/`)

| part / view | frames |
|---|---|
| upright front, all parts | **v6 f480**, v5 f1074, v5 f2250, w1 f395 |
| upright 3/4, arm layering | **v5 f588** (cut-scene), v6 f576 |
| upright back, emeralds, tail | **v5 f1908**, v5 f1875, v5 f1860 |
| face mask, emblem, scarf | **v6 f480** (`z_v6_0480_face.jpg`), v5 f1074 (`z_v5_1074_face.jpg`), w1 f127 (orange) |
| crown fan + bud | **v5 f450**, w2 f436 |
| chest sternum, rib-blades, robe | **v6 f480** (`z_v6_0480_chest.jpg`) |
| B / C leaf hands | **v6 f480** (`z_v6_0480_rhand.jpg`), v5 f588 |
| crawl form | **v6 f165** (broadside), **v6 f90** (head), v6 f99 (rear), v6 f528 (front), v5 f396 (hood close) |
| stance changes | v6 f522-f600 (unfold), v6 f756-f804 (fold), v5 f909-f1032 (arc/flop/rise), v6 f282-f333 (S-coil), v5 f1470 (BALL) |
| Heart | v3 f0, v4 f1650, v3 f270 (scale), v2 f2200-f2418 (arrival), w2 f0-f300 (egg) |
| organisms | v3 f900 / f996 (basic), v3 f1300 (nurturing), v3 f2088 / f2148 (guarding), v4 f900 / f840 (nesting), v4 f1140-f1332 (destruction), v4 f2070 / f2400 / f1920 / f1956 / f2175 (predatory) |
