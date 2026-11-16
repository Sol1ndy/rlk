# 아펩의 오아시스 파수꾼 (Guardian of Apep's Oasis): model anatomy and modelling spec for a display-entity rig

Chapter-3 end boss. Phase 1 = 종막 오아시스 파수꾼, phase 2 = 소생 단계 (protect the 「오아시스의 심장」 against 6 organism kinds),
phase 3 = 기원 오아시스 파수꾼. Binding RES from the user (wiki.md): the Warden in phases 1 and 3 has **Dendro RES 30 %**,
the organisms **Dendro RES 20 %**, everything else 10 %; the 양육 buff (+9900 %) is a "can't be damaged" mechanic, not a model
state. Nothing in the model depends on RES; it is restated only because the brief asks for the wiki to be read first.

Sources:
* `src/wiki.md` and `src/img/11..15` (stat tables, the phase-1 wiki picture `13.webp`, the organism table `14.png`, the basic
  organism portrait `15.png`).
* `src/v1..v6.mp4` (1920x1080, 60 fps, gappy screen recordings with editor captions), `src/w1.mp4` (500x300, 종말의 여파),
  `src/w2.mp4` (600x320, phase 2→3 cut-scene).
* My own frames: full-res JPEGs in `understand/model_work/full/<v>_f<frame>.jpg` (≈ 170 frames), 4-5 fps thumbs in
  `model_work/thumbs/`, overview sheets in `model_work/sheets/`, crops and measurement grids in `model_work/crops/`
  (`g_*` / `m_*` / `z_*` grids carry full-res pixel coordinates). Palette evidence: `model_work/palette.json` +
  `palette_proof.jpg` (k-means per sampled box), final ramps `model_work/palette_final.json`. Rig plan:
  `model_work/rig_plan.json`.
* Scripts (all in `understand/model_tools/`): `grab.sh` (frame grab), `mont.py` (labelled montage), `tsheet.py` (thumb
  sheets), `grid.py` (pixel-grid crops), `palette.py`, `palette_final.py`, `sheetlib.py` + `sheet01..07.py`, `sheet10.py`,
  `rig_plan.py`.
* The analysts' reports `understand/v1.md` (phase 1), `v2.md` (phase 1 + phase-2 opening) and `v4.md` (organisms) were
  read and cross-checked; v3/v5/v6 reports did not exist yet, so the phase-3 sizes are mine alone (§1).
* Rig rules: `S:az/understand/rigtech.md` (the Azhdaha scale probe: 44-48 parts, cap 56, reach = 1.5 x scale, hit proxies,
  atlas ≤ 1.2 M px per chapter boss); the shared libraries `mboss_model_lib.mjs` / `mboss_paint_lib.mjs` /
  `mboss_rig_*.mjs` on wip/fg; fieldgen and butterfly `model.md` as the templates.

Frame notation: `v2 f2076` = 60 fps frame 2076 of v2 (34.6 s, tick 692; tick = f / 3). `w1 15.8 s` / `w2_0012` = 25 fps
clips (thumb index n = 0.2 s steps from 0). **PH** = player height (Barbara, 1.7 m used as the ruler by all reports).
**b** = Minecraft blocks.

Conventions (same as the Guardian, butterfly and fieldgen studies):
* "her right / her left" = the Warden's own sides; in a front view her right is screen-left.
* **Rig space**: +X = boss left, +Y up, −Z forward; origin on the floor under the thorax centre. **1 m = 1 b** (§1).

---------------------------------------------------------------------------------------------------

## 0. Key findings and corrections to the brief

* **It is a six-limbed beast plus a tail, not "very long thin limbs".** Phase 1 has
  * **2 long pale arms** (5-6 m, shoulder → claw) that end in **3-lobed pale claws** with a square gold gem and a gold cone
    on the back. In idle they are planted far out to the sides (stance 10-11 m, `v2 f2076`); they rise in attacks
    (`v2 f417`, `v2 f2040`). These are what the wiki picture reads as "very long thin limbs".
  * **4 massive legs** (≈ 1.1 m thick, "elephant legs"), dark armoured at the top, **pale bark at the bottom**, each ending
    in a **5-petal hand/foot** (3 front petals + 2 side, ≈ 1.5-2.0 m across) with a gold cone at the wrist.
  * **Shoulder leaf flaps** (1.5-2 m, 2 per side) and **long dark drapes/ribbons** hanging from the cowl to the ground.
  * A **≈ 7 m twisted-ribbon tail** (two helical bands, pale + dark) ending in a curled hook.
  * The wiki's "gold crystal spikes stick up from the ground" are the **wrist cones of the flat petal hands**, not separate
    ground crystals.
* **The head is a hood/cowl seen from above.** From the front you see a dome of dark slate leaf-plates with: a tall crown
  crystal, a mid-face crystal, a small gold V/chevron and two pale-gold crescent marks (`v2 f2076`). Only when the boss
  rears up do you see the face underneath: a **pale closed flower-bud "skull"** with no eyes (v2.md §4.1).
* **The "core" of phase 1 is a belly sac, not a window in the head.** A glowing yellow-green translucent bulb hangs under the
  thorax between the front legs, cupped by pale lobes and a pale ribcage (`v2 f2040`, lit in `v2 f417`). It looks like a
  big basic organism. A **gold leaf sprig + small lime seed bulb** sit on the hood top (`v1 f255`).
* **Square gold gems** sit in raised dark frames on each **shoulder** (top of the front legs) and on the **back of each arm
  claw**. In profile the shoulder gem reads like an eye (`v1 f315`, `v2 f870`).
* **Phase 3 is the same skeleton re-skinned and reared up** (sheet 04):
  * it stands as an upright **serpent/naga** (trunk out of the ground, hood ≈ 8.5 m up);
  * lime leaf plates replace the dark slate, the back turns bottle green, **emerald** crystals replace the gold on the
    hood and back;
  * the glow moves from the belly to the **face** (a gold-lime flower rosette fills the hood opening) and to **gold veins
    down the chest** to a yellow navel glow;
  * new growths: a lilac-grey collar ruff, long lime "hair" strands, **white-bud vines** (lily-of-the-valley) draped over
    the arms and hips, broad leaf blades on every limb, and a jagged leaf crest on the hood.
  * Phase 3 shows **3 pairs of leaf hands**: the long arms (raised high), the shoulder flaps grown into mid arms, and the 4
    legs spread on the ground as a leaf skirt.
* **The Heart of the Oasis is one egg prop with two shapes.** It lands as an **upright golden egg** (2.0 m x 1.7 m, `v2 f2358`),
  squashes and leans into a **root cradle** (4-5 dark roots with glowing sprout tips) where it reads as a lying lemon
  ≈ 2.0 m tall x 2.5-3.0 m long (`v2 f2418`, `v4`, `v5 f198`). When the bulb leaves, the cradle stays as a pedestal
  (`v2 f2340`). **Phase 2 is played on the same field** as phase 1 (v3/v4: the Heart sits on the grass); the dark golden cave
  is only the w2 cut-scene.
* **The organisms are not all ground-standing pods** (sheet 06):
  * 기본 has 2 poses: the wiki "sac" (petals up) and the in-game **bell** (dome up with a sprout, petals down as a skirt);
  * 둥지 **hovers 0.5-1.5 m and flaps** its two arched sepal limbs like wings;
  * 포식성 has **3 forms**: fish (leaf shark with a cyan eye), bud (the wiki picture), and an inflated double-lobed pod;
  * 파괴's "yellow beak" is a glowing round open front with a short yellow cone in it;
  * 수호 never moves;
  * 양육 stands on an always-on glowing ground ring.
* **Scale: 1 m = 1 b.** This is a chapter boss and must dwarf the mid-bosses (Guardian 3.0 b, butterfly 2.8 b). P1 is
  4.5 b tall and 14 b long; P3 is 8.5 b tall. Both fit the proposed Apep arena (walk r 26, az `chapter.md`).

## 1. Sizes against the player (cross-checked)

Methods:
* **v1.md** fitted a ground plane with the camera solved from repeated thorn wheels.
* **v2.md** compared parts at the same depth as the player, plus a ground plane with a 45° vertical FOV.
* **Mine**: same-depth comparisons on `v2 f960` (petal foot next to the player), `v2 f2040` / `f2076` (front views with the
  player under the hood), `v3 f300` (Heart + basics + nurturing at one depth), and rough ground-plane fits for phase 3 on
  `v6 f495` and `v5 f2265`. Overlays: `07_proportions_measured.jpg`, grids `model_work/crops/m_*.jpg`.

### 1.1 Phase 1 (종막)

| item | v1.md | v2.md | mine | **use (b)** |
|---|---|---|---|---|
| hump / hood top, idle crouch | 4.3 (3.9-4.6) | 4.6 (4.2-5.0) | — | **4.5** |
| crown crystal tip, idle | 4.7 | 5.0 | 4.9 reared (`v2 f2040`, 2.9 PH) | **5.0** |
| head-low front crouch, crown tip | — | 3.7 | — | 3.8 (pose) |
| half-stand / upright on buried hands | 4.7 / 5.1 | — | — | pose |
| arms-up (hands) | — | 6.8 | — | pose |
| full rear-up / arms raised as a flower / spiral column | 9.3 / 8-9 | 7-8 | — | poses, 7.5-9 |
| hood (cowl) width incl. flares | ≈ 2 (dome) | 3.3 | 3.1+ (`v2 f2076`, 1.84 PH, player in front) | **3.3** |
| shoulder width incl. leaf flaps | — | 5.0 | — | 5.0 |
| stance, arm claw to arm claw | 8.1 (hand span) | 10-11 | — | **10.6** |
| front feet apart | — | 4.6 | — | 4.8 |
| long arm, shoulder → claw tip | — | 5-6 | — | **6.2** (2.8 + 2.6 + 0.8) |
| leg thickness (forelimb) | 1.1 | — | — | 1.1 → 0.7 at the wrist |
| petal hand / foot across | 2.0 | 1.5 | 1.7-2.0 (`v2 f960`: foot = player height) | **1.8**; petal 0.8 x 0.45 |
| tail (body → hook) | ≥ 6 | 7 (5-9) | — | **7.5** |
| nose → tail tip | ≈ 13 (11-16) | ≈ 16 (14-19) | — | **14** |
| crown crystal | 0.8-1.0 | 0.5-0.6 | — | 0.8 |
| other crystals (cones, wrist, spine) | 0.5-0.9 | 0.25-0.6 | — | 0.35 (wrist) - 0.6 (spine) |
| belly core / sac | 1.2-1.6 | — | — | Ø 1.4 |
| one shoulder flap / drape | mantle leaf 4.5-5 x 2-2.7 (v1 counts the arms as mantle) | flaps 1.5-2 | — | flap 1.8, drape 3.5 (cowl → ground) |

### 1.2 Phase 3 (기원), my estimates

There is no analyst report yet, so the error bars are wide.

| item | estimate | **use (b)** |
|---|---|---|
| hood top, upright idle | ≥ 5.2-5.6 m raw (3.0-3.3 PH; a hard lower bound, since the boss stands behind the player); ground-plane fits on `v6 f495` and `v5 f2265` give 8-11 m | **8.5** (crest and shards 9.0) |
| upper leaf-arm span, tip to tip | ≈ 1.2 x the boss height | **≈ 10** |
| mid leaf arms (grown flaps) | ≈ 3.5 m each | 3.5 |
| lower leaf hands on the ground | 2.5-3 m each, lime with a grey edge | 2.6 |
| tail | ≥ 8 m; it coils 1.5 turns round the trunk in `v6 f300` | **8.4** |
| face rosette | ≈ 1.4 m Ø | 1.4 |
| emerald crystals | hood sides 0.6, hood shards 0.4-0.7, back diamonds 0.8-1.0 | as listed |

### 1.3 Phase 2 objects

| object | best estimate | source | **use (b)** |
|---|---|---|---|
| Heart egg, arrival (upright) | 2.0 tall x 1.7 wide | v2.md §2 (`v2 f2358`) | 2.0 x 1.7 |
| Heart in the cradle (squashed, leaning) | 2.0 tall x 3.0 long (v4.md); 1.2 PH x 1.8 PH (mine, `v3 f300`) | v4.md §3, mine | bulb 2.0 x 2.6, leaning 60-70° |
| root cradle top / sprout tips | 2.8-3.2 / 3.5-4.0 | v4.md | 3.0 / 3.8 |
| nest of roots + petal clumps | 3.5-4 across; ground swirl r 2.5-3.5 | v2.md, v4.md | 3.8; ring r 3 |
| 기본 basic | 1.0 tall, bulb Ø 0.8, skirt Ø 0.9 | v4.md (fit), mine | 1.0 |
| 양육 nurturing | ≈ 1.8 (1.7-1.9 x a basic at the same depth, `v3 f300`); ring Ø ≈ 2 | mine | 1.8 |
| 수호 guarding | spire 2.4; orb Ø 0.35, 0.6 above the tip | v4.md | 2.4 + orb |
| 둥지 nesting | 2.2 span x 1.3 tall, hovers 0.5-1.5 up | v4.md | 2.2 x 1.3 |
| 파괴 destruction | ball Ø 1.2 + 0.2 spikes + 0.4 beak | v4.md | Ø 1.2 |
| 포식성 predatory | bud 2.1 x 1.6 (hovers 0.2); fish 2.5 long x 1.3; pod 3.5 x 1.8 | v4.md | as listed |

**Scale decision: 1 m = 1 b, unscaled.**
* The fieldgen and butterfly studies kept their bosses near 3 b; a chapter boss should feel twice as big.
* At 1:1 the P1 crouch is 4.5 b, which puts the hood at the third-person camera height. The belly core (1.6 b) is
  melee-reachable under the body, the arms span 10.6 b, and the body is 14 b long in an r 26 arena (0.55 r).
* P3 at 8.5 b towers like the cut-scene. If the camera clips, scale only the phase-3 rest pose (trunk parts) down to
  7.5 b; nothing else depends on it.

## 2. Silhouette

* **P1 idle / walk** (`v2 f2076`, `v1 f1110`, `v2 f870`): a low, wide, hunched spider-crab.
  * A domed dark cowl sits on a humped back with a gold crown crystal.
  * 4 pale-footed legs stand close under the body, and 2 long pale arms reach far out to the sides with 3-lobed claws.
  * Dark ribbons hang down between the legs; a long twisted tail trails behind on the ground.
  * Gold dots everywhere: crown, mid-face, shoulders, wrists, claws, spine.
* **P1 arms-up / rear-up** (`v2 f417`, `v2 f2040`, `v2 f480`, `v1 f1560`): the arms rise high and wide like a "Y", and the
  belly bulb glows between the front legs. In the rear-up the pale underside shows: a ribcage of pale swirled plates, the
  inner faces of the arms, the flower-bud face.
* **P1 spiral column** (`v1 f2238`, 발광): the arms and flaps wind up into one twisted vertical ring, 8-9 m tall.
* **P1 burrowed**: only a dark leaf-shaped pool and a translucent shadow; nothing of the rig shows (v1.md §3.A).
* **P3 upright** (`v6 f495`, `v5 f2265`, `w1 15.8 s`):
  * a tall green serpent on its trunk with a hooded face that glows gold-lime;
  * three pairs of leaf hands (raised, sideways, on the ground);
  * hair strands framing the face, white-bud vines, and the dark tail ribbon coiling out behind.
  * It reads as "a tree-spirit naga with a flower face".
* **P3 back** (`v5 f1875`): glossy bottle-green plated back with 2 large emerald diamonds (upper and lower back) and the
  twisted tail.

## 3. Phase 1 part list (sheets 01, 02)

Numbers match `01_p1_parts_annotated.jpg` and `02_p1_closeups.jpg`.

### 3.1 Hood / cowl (head)
* **Dome**: overlapping dark slate leaf-plates in 3-4 rows (#47504A / #39413B, bevel highlight #7E8572), each plate with a
  thin lighter rim. The dome flares into 2 pointed side "ears", 3.3 b wide over the ears; it is 2.5-3 b long, and its top
  is at 4.3-4.5 b in idle.
* **Crystals**:
  * **crown**: lemon-gold cone, 0.8 b, leaning 10-20° forward (#FCEB6A → #A8902C);
  * **brow / mid-face**: a second cone, 0.4 b, on the face plate;
  * a small **gold V/chevron** under the mid-face cone.
* **Crescents**: 2 pale-gold crescent strokes on the face plate, either side of the V (emissive-ish paint).
* **Gold leaf sprig + seed bulb** on the crown: 2-3 branched sprigs of cream-gold leaves around a small glowing lime bud
  (`v1 f255`), 0.6-0.8 b tall.
* **Face** (only in the rear-up): a pale closed flower-bud skull inside the cowl, no eyes (v2.md). It can be painted on
  the hood's underside faces.

### 3.2 Thorax, hump, belly
* **Hump**: the back is covered by large dark plates continuing the cowl. A ridge of **3-5 gold cones** (0.4-0.6 b) runs
  along the spine and shoulders.
* **Shoulder plates**: the dark plate over each front leg curls forward into a **hook**. A **square gold gem** sits in a
  raised dark frame on it, with a pale-lime crescent seam under it (`v1 f315`, `v2 f870`).
* **Pale bark side plates** (shoulder/flank): cream-grey with darker wood-grain contour swirls and a dark outline
  (#E2DCC8 → #7E7A64).
* **Belly / ribcage**: interlocking pale swirled plates (5-6 rib pairs) with dark gaps (`v2 f480`).
* **Belly core** (weak-spot look): a Ø 1.4 b translucent yellow-green bulb with a seed inside, cupped by pale drooping
  lobes and a pale cracked belly shell (`v2 f2040`, `v2 f417`).
  * Glow states: idle soft (#CBDB99); wind-ups and half-stand bright (#E2F4BA, bloom); dark when burrowed.

### 3.3 Long arms (2)
* Pale bark arms, 2.8 b upper + 2.6 b lower, 0.6-0.8 b thick, made of overlapping pale shell plates with dark contour
  rims (a beetle leg / folded leaf).
* The inner faces carry rows of cream leaf-scales with dark wedges and veins (`v1 f255`).
* **Claw**: 3 broad pale lobed fingers (≈ 0.8 b), a square gold gem on the back of the hand, and a gold cone near the
  wrist.
* Poses: planted far out (idle), raised high (arms-up), wound together (spiral column), swung (melee combo).

### 3.4 Legs (4) and petal hands/feet
* Upper legs are dark armoured, covered by the hanging dark plates, so the leg reads **dark at the top, fading to pale bark
  at the foot** (gradient #39413B → #B9B49C).
* **Petal hand/foot** (`v1 f315`, `v1 f290`): 5 broad pointed petals (3 front, 2 side), each 0.8 x 0.45 b with a raised
  centre vein, a turned-up tip and a dark outline. They splay flat on the ground like a starfish.
* A **cream-gold cone** (0.35 b, #F1D68B) stands on the back of each hand/foot.
* Front pair: wrists at x ±2.4, z −3.2 (feet 4.8 b apart). Rear pair: wider and further back (x ±3.0, z +2.9).

### 3.5 Shoulder flaps and drapes
* **Flaps**: 2 per side, pointed dark leaf flaps, 1.5-2 b, radiating from the shoulders like a collar; pale undersides.
* **Drapes**: long dark green-black ribbons (≈ 3.5 b) hanging from the cowl sides to the ground. In the upright emerge pose
  they splay over the ground in 4-6 directions.

### 3.6 Tail
* ≈ 7.5 b, base Ø 0.7 → 0.3 b. It is a **twisted two-band ribbon**: a pale band (#C9C6B4 / #B0AE9C) and a dark slate band
  (#4B5348) spiral round each other (`v2 f1125`, `v2 f1245`).
* It ends in a **curled hook** with a small pale leaf curl. It lies on the ground behind the body and lifts into an S for
  생명의 꼬리.

## 4. Phase 3 part list (sheet 03) and every difference from phase 1 (sheet 04)

| part | phase 1 (종막) | phase 3 (기원) |
|---|---|---|
| stance | low crouch, hood 4.5 b | upright serpent, hood 8.5 b; the abdomen + thorax stand vertical out of the ground |
| hood | dark slate dome, gold crown/mid-face crystals, V, crescents | **lime + dark green** hood (#86AE45 / #2F6143) with a **jagged leaf crest** curling forward; **emerald cut crystal** on each side (0.6 b) and 4-6 emerald shards along the hood top/back (`v6 f105`); grey "peel" patches of the old pale plates remain (`v5 f450`) |
| face | closed flower-bud skull, hidden; sprig + seed bulb on top | **glowing gold-lime flower rosette** fills the hood opening (Ø 1.4 b, #F8F894 → #A9BC3C), leaves radiating; the sprig and a bright lime seed bulb remain on the crown |
| neck | short, hidden | a **collar ruff** of pale lilac-grey petals (#C4C3CC) under the face |
| chest / belly | pale ribcage, belly bulb core | lime + pale grey leaf plates with **glowing gold vertical veins** down the centre to a **yellow navel glow** (`w1 15.8 s`, `v6 f495`); no separate bulb |
| back | dark plates + gold cones | **glossy bottle green** (#245038, high-contrast highlights) with 2 big **emerald diamonds** (upper back 1.0 b, lower back 0.8 b) |
| long arms | pale shell arms, 3-lobed claws, raised in attacks | the same lengths, clad in **broad lime leaf blades** (grey-lilac undersides #C4C3CC), **lobed leaf hands** (5 lobes); held raised and out (Y) in idle |
| shoulder flaps | 1.5-2 b dark flaps | grown into **mid leaf arms** (≈ 3.5 b) held sideways |
| legs + hands | dark/pale legs, 5-petal pale hands, gold cones | the legs splay out on the ground as a **leaf skirt** of 4 big lime leaf hands (2.6 b) with a grey edge; the cones stay but turn **pale cream** (#E3D9B0) |
| drapes | dark robe ribbons to the ground | **lime / dark green hair strands** from the hood to the waist |
| new growth | — | **white-bud vines**: thin dark green vines with rows of small white bell buds (lily-of-the-valley, #F6F8EE), draped over both arms and both hips |
| tail | pale + slate ribbon, 7.5 b | **mint + dark green** ribbon (#A6DDA7 / #3E5246), ≥ 8 b, coils round the trunk in 생명의 꼬리 |
| glow | belly bulb (yellow-green) | face rosette + chest veins + navel (gold-lime); emerald crystals glow green |
| stage / tint | yellow-olive withered field | bright teal-green lake field |

* **Glow states (P3)**:
  * idle: the face and veins are steadily lit;
  * 종말의 여파 charge (`w1 4.6-6.2 s`): the whole body brightens and a green ring spreads from the base;
  * in the blast (`w1 11-12.6 s`): white-lime;
  * after (`w1 15-16 s`): back to idle.
  * The emerald crystals are always lit.

## 5. Heart of the Oasis, golden egg, pedestal (sheet 05)

* **Bulb**:
  * shape: a translucent glowing yellow-lime seed, lemon/onion shape;
  * surface: soft vertical ribs (5-7, visible in the phantom outline), a big soft white-yellow specular band at the upper
    left, an inner darker swirl, floating motes inside;
  * colours: #EEF27A / #D8DC58 / #BFC446, rim lighter;
  * **arrival**: upright egg 2.0 x 1.7 b with a vertical light beam (`v2 f2358`);
  * **in play**: squashed and leaning 60-70° in the cradle, 2.0 tall x 2.6 long (`v2 f2418`, `v5 f198`, `v4`).
* **Root cradle**:
  * 4-5 thick dark brown roots (Ø 0.4-0.5 b, #4A4226 / #3A341E, bark highlight #7A6E3E) rise from a gnarled mound and curl
    up round the back and sides of the bulb like fingers holding a fruit;
  * the back roots arch higher than the bulb, to ≈ 3.0 b;
  * each root ends in a **glowing yellow sprout / leaf flame** (#FAED5E, emissive), up to 3.8 b;
  * a ring of pale petal clumps sits round the nest base.
* **Ground**: a golden swirl / ring decal round the base, r ≈ 3 b, always on in phase 2 (fx).
* **Pedestal** (no bulb, `v2 f2340`): the cradle alone, with pale grey smoke/fungus puffs round the base when the bulb
  leaves. In phase 3 it can stay as the arena-centre prop.
* **Golden egg in the cut-scene (w2)**:
  * an upright bright gold egg (#FEEB71 → #856E31) standing in a shallow puddle with small crystals in a dark golden cave
    (0.0-2.2 s);
  * it rises into the canopy (8.0 s) and a **green vine hand** of 5-7 curling tendrils grips it (9.2 s);
  * it bursts in green light (10.8 s), then shows the lake arena, and the Warden of Oasis Prime emerges in a burst of
    leaves (16.8-18.8 s).
  * Only the egg and the vine hand are model work; everything else is fx or camera.
* Model it as **one prop with 3 displays**:
  * `heart_bulb`: a translucent `knob()` + an inner glow card, brightness 15, scale-animated for the arrival squash;
  * `heart_cradle`: 5 roots as tapered box chains + the mound;
  * `heart_tips`: 5 glow sprout cards, brightness 15.
  * Pitch the bulb from 0° (arrival) to 65° (cradle).

## 6. The 6 organisms as small separate models (sheet 06)

General rules:
* All organisms are pale/translucent plant forms with a **glowing yellow-lime core** (#FAFF7B / #E3F062, brightness 15)
  and dark teal accents (#3E5F5A).
* They are seen through a heavy yellow haze; de-tint the samples by ≈ 10 %.
* Translucency: alpha 0.8-0.9 on the shells (cut-out alpha at 0.5 is not enough; use translucent render sprites), alpha 0
  at the sprite borders.

| # | organism | shape and parts | size (b) | displays | glow |
|---|---|---|---|---|---|
| 1 | **기본** basic | Two poses. **Bell** (in play): smooth milky white-mint translucent dome (5-6 faint vertical panels), a short hooked sprout on top (olive tip), the bottom flaring into a skirt of 4-5 pointed petal tips on the ground; it hops and slides. **Sac** (wiki portrait / rolling, `v3 f990`): an onion bulb lying on its side with 4-5 pale petals as a crown and the seed showing. | 1.0 tall, bulb Ø 0.8 | 1: `basic` (looks `bell`, `sac`, `buffed`) + the core inside one model | seed / core (lime) |
| 2 | **양육** nurturing | A twisting stalk of **dark teal-blue + pale bands spiralling up**, a pale grey-white folded petal cap leaning forward like a hood, a glowing orb held in the twist, pale translucent leaf wings unfolding at the sides, a cream skirt at the foot, on a **glowing lime ground ring** (Ø ≈ 2). Buff: green beams to up to 3 basics (fx). | 1.8 | 2: `body`, `ring` (br 15) | orb, ring |
| 3 | **수호** guarding | A spire of 2-3 pale grey-white leaf ribbons twisting up into a split point (a flame / DNA twist), teal inner faces; a dark teal base sheath with a scalloped hem of 4-5 grey-blue lobes; a cut gold-yellow crystal on the base front; a glowing yellow-green orb (Ø 0.35) floating 0.6 above the tip. Never moves. | 2.4 + orb | 2: `spire`, `orb` (br 15, bob) | orb |
| 4 | **둥지** nesting | A dark teal pointed cap with a spike on top and a fringe of small thorns; a glowing yellow orb "eye" with a pale ring under the cap; **two long pale grey-teal arched sepal limbs** spreading like wings, cream curled tips. Hovers 0.5-1.5; flaps (V ↔ wide arch, 0.6-0.8 s); tell pose = the limbs curl up into a vertical loop. Walls are a separate prop (3 groups of 3-5 lime leaf blades, 1.5-3 tall, r 3-4). | 2.2 x 1.3 | 3: `cap` (+orb), `wing_l`, `wing_r` | orb |
| 5 | **포식성** predatory | **Fish**: leaf-shark, pale cream back with wavy grey stripes, 2 big + 1 small grey back cones, dark olive-teal underside, translucent leaf fins with yellow-green edges, a round eye (dark teal ring, black pupil, cyan rim). **Bud** (wiki): a diamond, grey horn on top, cream petal hood with grey streaks, translucent green star-shaped lower bowl, yellow core between, bottom spike; hovers over a gold swirl. **Pod**: tall double-lobed pale-mint gourd with wavy petal edges, core in the lower lobe. **Closed face** between bites: a dark green dome with a yellow diamond "mouth" gem. | fish 2.5 long; bud 2.1 x 1.6; pod 3.5 x 1.8 | 3 shared: `hood`, `bowl`, `core`; looks `fish` / `bud` / `pod` / `face` per part (the fish is `hood`+`bowl` turned 90°, the pod is both scaled 1.6 on Y) | core, eye |
| 6 | **파괴** destruction | A dark teal-black armoured sphere (#3A4A44) with 8-12 black/teal cone spikes (0.2) and pale grey bands between the plates; an open round front with a **glowing pale-yellow face disc** and a short yellow cone "beak" (0.4); rolls on its side toward the Heart; fuse = the face pulses every 9 t; blast = green dome r 3 (fx) + a blackened husk. | Ø 1.2 | 2: `shell` (looks `normal`, `husk`), `face` (br 15, pulse scale) | face |

* **Shared spawn marker** (v2.md): a pale wireframe hologram dome, 0.8-1 b wide x 0.4 b tall, before each organism appears
  (fx).
* **Shields from 수호**: 2-4 tall translucent yellow-green leaf panes per basic (1.3 x 0.55 b), or a green bubble (v3
  phantom view) (fx/prop).
* **Buffed basic** (양육): a green aura + a lime ring under it; use a `buffed` look on `basic`.

## 7. Colour palette (sheet `08_palette.png`, data `model_work/palette_final.json`)

Ramps are listed hi → deep. Evidence: `model_work/palette.json` + `palette_proof.jpg` (k-means per box) and point samples;
v1.md, v2.md and v4.md samples agree within a few steps. The P1 stage casts a strong yellow-olive haze and the P2 stage a
yellow haze, so paint those ramps ≈ 10 % less yellow than sampled (done below). P3 is lit by neutral green-white light,
so its leaf greens are close to true.

### 7.1 Phase 1

| key | material | ramp |
|---|---|---|
| `p1_slate` | hood + mantle outer plates, hump, leg tops | `#7E8572 #5E665C #47504A #39413B #2C332E #1D231F` |
| `p1_bark` | arms, legs (lower), hands/feet, flaps under, belly, side plates | `#E2DCC8 #CFC9B2 #B9B49C #9F9A82 #7E7A64 #5A5745` |
| `p1_line` | outlines, veins, wood-grain contours (cel outline) | `#696D4F #5A6459 #4A4C3C #3E3D30 #2C2B20 #1A1A12` |
| `p1_gold` | crown / mid-face / spine crystals (lemon gold) | `#FFF9B0 #FCEB6A #EED64C #D2BA3A #A8902C #6E5A12` |
| `p1_cone` | wrist / claw cones (cream gold) | `#FEF2AB #F1D68B #DDBF7A #C4A86A #A08A55 #6F5F38` |
| `p1_gem` | square shoulder / claw gems (look lit) | `#FFFFA0 #FEFD61 #F8EC55 #EAD849 #D8C546 #B8A242` |
| `p1_sprig` | gold leaf sprig on the crown | `#F4E3A0 #ECD585 #D6BE71 #AC9C69 #8B7A47 #62532C` |
| `p1_core` | belly bulb glass + seed (emissive) | `#F4FBE4 #E2F4BA #CBDB99 #AEB877 #808C53 #394435` |
| `p1_seam` | crescent seams / plate bevel highlights | `#F2F0C8 #E2E2B0 #C8CC94 #A7AE78 #848C5C #5E6542` |
| `p1_tail` | tail bands: pale (first 3) + dark (last 3) | `#C9C6B4 #B0AE9C #8A8874 #4B5348 #3B4236 #282D21` |

### 7.2 Phase 3

| key | material | ramp |
|---|---|---|
| `p3_lime` | leaf plates, leaf arms, leaf hands, hood | `#E0EE9C #C4DC7E #A6C85E #86AE45 #648C30 #43661E` |
| `p3_under` | leaf undersides, collar ruff (lilac-grey) | `#DCDAE0 #C4C3CC #A9AAB3 #8F9199 #71747C #52565C` |
| `p3_bottle` | back, hood inner, trunk, vines (bottle green) | `#7FA684 #4E7A55 #2F6143 #245038 #1B3F2B #122C1E` |
| `p3_emerald` | emerald crystals | `#E6FFB0 #B4F56A #82E042 #4FBF2E #2F9224 #1A5E1A` |
| `p3_face` | face rosette, chest veins, navel (gold-lime emissive) | `#FFFFD0 #F8F894 #E8EC6A #CDD84E #A9BC3C #7E922C` |
| `p3_buds` | white bell buds (first 3) + vine (last 3) | `#F6F8EE #DDE6D6 #B9C8B4 #5F8A5C #48634C #2E4430` |
| `p3_cone` | pale thorn cones on the leaf hands | `#F2ECCC #E3D9B0 #CFC59A #B0A47A #8E8460 #645C40` |
| `p3_tail` | tail bands: mint (first 3) + dark (last 3) | `#C8EEC6 #A6DDA7 #8AC08E #586A5C #3E5246 #283A30` |

### 7.3 Phase 2

| key | material | ramp |
|---|---|---|
| `heart_bulb` | Heart bulb (translucent, emissive) | `#FBFFC0 #EEF27A #D8DC58 #BFC446 #A0A23A #6E7030` |
| `heart_root` | root cradle, mound | `#7A6E3E #5E5430 #4A4226 #3A341E #2B2716 #1E1B10` |
| `heart_tip` | sprout tips, ground swirl (emissive) | `#FFFBB0 #FAED5E #E6D852 #D9CB50 #BAAF47 #8E8634` |
| `egg` | cut-scene golden egg | `#FFF6B0 #FEEB71 #F7DD60 #E7CE51 #D0B949 #856E31` |
| `org_bell` | basic bell / sac (alpha ≈ 0.85) | `#F2F5EC #DCE3D4 #C3CDBC #A9B5A3 #8D9987 #6E7A6A` |
| `org_teal` | dark teal parts (nurturing ribbon, guarding base, nesting cap) | `#6F9A92 #4F7A72 #3E5F5A #2F4A48 #223836 #162624` |
| `org_pale` | pale ribbons, sepals, caps | `#EEF0E6 #D6DCCD #BCC6B6 #A1AE9C #85927F #687462` |
| `org_core` | organism cores / orbs (emissive) | `#FFFFD8 #FAFF7B #E3F062 #CED94E #ACB83A #7E8A2A` |
| `pred_hood` | predatory hood / fish back | `#ECEAC4 #D9D59E #BDB986 #9E9A70 #7D7533 #5A5424` |
| `pred_fin` | predatory bowl / fins / pod (translucent) | `#E4F6CE #C4E8A6 #ABC39F #899D80 #687D5E #4A5A40` |
| `pred_eye` | fish eye ring (cyan rim, glow) | `#D6FFFB #A0DDD9 #5FB0AC #2E7579 #1A4A4C #0A1A1A` |
| `destr` | destruction shell + pale bands | `#C9CCB8 #8E9478 #4E5B52 #3A4A44 #2A3633 #1A2220` |
| `destr_face` | destruction face disc / fuse | `#FFFFF0 #FEFFCA #FDFFB2 #FBFF9F #E8ED9D #CDCD52` |

### 7.4 Glow states and fx colours

| state | ramp / note |
|---|---|
| P1 belly core idle → wind-up | `p1_core` at 60 % brightness → full + bloom card (scale 1 → 1.3) in the half-stand, arms-up and 발광 |
| P1 burrow | the body tints brown and dissolves into root chunks (v2.md). Do it with fx (root-chunk cards, `#5C5A2E` pool) and a 4-6 t scale-out, not a third look |
| P1 gold burst / thorn-wheel rim | `#FFFDDA #FAFCDF #F0F2BB #D0D495 #B3B587 #8E9264` |
| P1 burrow pool / ground shadow | `#5C5A2E #45481E #3F3C15 #2D2A04 #1E1C02 #100F00` |
| P2 nurturing buff, shield panes, destruction dome | `#F4FFC0 #E2F174 #C8F060 #BECF4C #A8BC3F #7E9030`, alpha 0.4-0.6 |
| P3 face / veins idle → 종말의 여파 charge | `p3_face` steady → white-lime `#FFFFF0` peak during the blast |
| P3 종말의 여파 field + protective domes | `#E8FFD0 #BFF59A #96E36A #6FCB4A #4FA536 #2F7224` |

**What glows (brightness 15)**:
* P1: the belly bulb and seed, the crown seed bulb, the crescents. The gold crystals and gems are painted with lit colours
  at brightness 14; they are not emissive in the footage.
* P3: the face rosette, the chest veins, the navel, the emerald crystals.
* Heart: the bulb and the sprout tips.
* Organisms: every core and orb, the nurturing ring, the destruction face.

## 8. Geometry versus paint at Minecraft resolution

Rule of thumb: anything ≥ 0.25 b that breaks the silhouette or catches light at 4-12 b is geometry; anything flatter is
paint. Paint at **32 px/b** for large plates, limbs and the tail, and **48-64 px/b** for the hood, face, gems, claws and the
organism cores, where the player looks. The atlas budget is ≤ 1.2 M px for the rig with both looks (rigtech §7), so each
look gets ≈ 0.55 M px.

| feature | geometry | paint |
|---|---|---|
| hood dome | 6-10 overlapping plate boxes in 3 rows, each turned ±22.5° about X so the rows step like feathers; 2 ear flares (boxes at ±45° about Z) | plate bevel highlight stripe, thin pale rims, the dark outline |
| crown / mid-face / spine / wrist / claw cones | 3-4 stacked shrinking boxes turned 45° about Y (diamond section), or `lathe(n 4)`; a dark base collar box | 2-tone facets (lit / shade) |
| square gems | a raised dark frame (4 thin boxes) + an inset gem box proud 0.05 b | lit gradient + white glint |
| V chevron, crescents, crescent seams | — | paint on the face plate / shoulder plate (P1 crescents also on `face_glow`) |
| sprig + seed bulb | 2-3 thin crossed cards (alpha leaves) + a small box bulb | leaf veins |
| belly bulb | `knob()` sphere Ø 1.4 (translucent) + a seed box inside + 3-4 pale lobe slabs drooping over it | glass gradient, seed texture |
| ribcage / belly shell | 5-6 curved rib slabs (boxes at ±22.5°) under the thorax | the swirl patterns |
| wood-grain swirls on pale plates, vein lines, leaf-scale rows, chest scales, petal centre veins | — | paint (outlined with `p1_line`) |
| legs, arms | 3-4 stacked tapered boxes per segment (round-ish taper); 2-3 overlapping shell-plate boxes on the arms | dark → pale gradient on the legs; plate rims |
| petal hand/foot | 5 petal slabs (0.15 b thick) per hand; tips turned up 22.5° by a second slab | centre vein, outline |
| arm claw | 3 lobed finger slabs + a palm box | — |
| shoulder flaps, drapes, leaf arms (P3), leaf hands (P3), hair strands | **two back-to-back alpha cards** + a 0.1 b spine box (so they read edge-on), split into 2 segments for the long ones | the leaf shape (alpha), veins, pale underside on the back card |
| tail twist | each segment = 2 cards crossed at 90° along the segment axis + a thin core box; roll each segment +45° relative to the previous one in the pose, so the bands spiral | diagonal band stripes |
| P3 crest, emerald crystals | crest = 1 alpha card with a jagged edge; crystals = boxes turned 45° about one axis (diamond prisms), 2 crossed for the back diamonds | facet gradient |
| P3 face rosette | a 6-8 petal card fan on `face_glow` + a centre box | radiating leaf lines |
| P3 collar ruff | 8 petal cards in a ring (alpha) | — |
| P3 chest veins, navel | — | painted on `core_glow` cards over the chest (brightness 15) |
| P3 white-bud vines | a thin box chain (0.08 b) + bud cubes (0.15 b) in rows | — |
| P3 grey peel patches | — | paint |
| Heart bulb | translucent `knob()` + inner glow card; roots = tapered box chains; sprouts = glow cards | specular band, ribs |
| organisms | §6: 1-3 displays each; shells as `knob()` / slabs; wings and ribbons as alpha cards | facets, stripes |

## 9. Display entities and construction plan (sheet `09_rig_breakdown.png`, `model_work/rig_plan.json`)

### 9.1 Rules
* Shared libraries and rules apply (rigtech §1):
  * `item_display` with `item_display:"none"`;
  * the joint at the model origin;
  * coordinates −16..32, so reach ≤ 1.5 x scale b;
  * single-axis element rotations of ±22.5° / ±45°;
  * mirrored right-hand models (`mirrorModel`);
  * `teleport_duration` 1 and clips compiled by `createRigCompiler`.
* **Superset rig**: P1 and P3 use the same parts. P3 is a new pose + an item-model look swap (`look: p1 | p3`) per part;
  P3-only growths sit at scale 0 in P1.
* Culling: the boss is 14 b long, so use `width:30f, height:12f` on every part (rigtech TL;DR 3).
* **Hit proxies** (rigtech TL;DR 4): about 11 interaction entities on the bones:
  * hood, thorax, abdomen, belly core;
  * 4 feet;
  * 2 arm claws;
  * the tail middle.
  * In P3: the face, the chest, the trunk base, 4 leaf hands, the tail.
  * One HP pool. Proxies are off while burrowed.

### 9.2 Part table (42 + 2 optional = 44)

Pivots are P1 crouch idle, rig space, in blocks. Units = the farthest model point from the pivot (must be ≤ 24).

| # | part | content | build | scale | reach (b) | pivot (P1) | bright |
|---|---|---|---|---|---|---|---|
| 1 | `thorax` | hump plates, spine cones, shoulder side plates, ribcage + belly shell; P3: chest leaf plates, bottle back, back diamonds | boxes + slabs | 2.0 | 2.6 | (0, 3.0, 0) | 13 |
| 2 | `abdomen` | rear body between the thorax and the tail; P3 lower trunk | tapered boxes | 1.6 | 1.6 | (0, 2.6, 1.6) | 13 |
| 3 | `neck` | short dark plate neck | boxes | 1.4 | 1.2 | (0, 3.4, −1.6) | 13 |
| 4 | `hood` | cowl dome, flares, crown/mid-face cones, V, sprig, shoulder hooks; P3 crest, emerald hood crystals and shards, collar ruff | plate boxes, cards | 2.0 | 2.6 | (0, 3.5, −2.2) | 13 |
| 5 | `face_glow` | P1 crescents + crown seed bulb; P3 face rosette | cards | 2.0 | 1.0 | = hood | 15 |
| 6 | `core_glow` | P1 belly bulb + seed + bloom card; P3 chest veins + navel cards | knob + cards | 1.6 | 0.9 | (0, 1.6, −1.2) | 15 |
| 7-8 | `arm_up_l/_r` | upper long arm, shell plates | tapered boxes | 1.8 | 2.8 | (±1.6, 3.6, −0.8) | 13 |
| 9-10 | `arm_lo_l/_r` | lower long arm | tapered boxes | 1.8 | 2.6 | (±3.4, 2.6, −1.6) | 13 |
| 11-12 | `claw_l/_r` | 3-lobe claw + square gem + cone; P3 5-lobe leaf hand | slabs | 1.2 | 1.3 | (±4.8, 0.6, −2.4) | 13 |
| 13-14 | `fore_up_l/_r` | shoulder-to-elbow, dark plates, square gem frame | boxes | 1.6 | 1.6 | (±1.4, 3.2, −1.6) | 13 |
| 15-16 | `fore_lo_l/_r` | elbow-to-wrist, dark → pale | tapered boxes | 1.6 | 2.0 | (±2.3, 2.2, −2.6) | 13 |
| 17-18 | `fhand_l/_r` | 5-petal hand + cone; P3 lime leaf hand + pale cone | slabs | 1.2 | 1.3 | (±2.4, 0.4, −3.2) | 13 |
| 19-24 | `rear_up / rear_lo / rfoot` x2 | as the front, slightly smaller | as above | 1.4 / 1.4 / 1.1 | 1.6 / 2.0 / 1.2 | hip (±1.3, 2.8, 1.2) | 13 |
| 25-28 | `flap_a/_b` x2 | P1 dark shoulder leaf flaps (1.8 b); P3 mid leaf arms (3.5 b, 2 segments) | 2 alpha cards + a spine box | 1.6 | 2.2 | (±1.5, 4.0, −0.4) | 13 |
| 29-32 | `drape_a/_b` x2 | P1 dark robe ribbons (2 segments to the ground); P3 lime hair strands | alpha cards | 1.4 | 1.9 | (±1.2, 3.2, −2.2) | 13 |
| 33-38 | `tail_1..6` | twisted ribbon segments, 1.2 b (P3 1.4 b via scale) | crossed cards + core box | 1.3 | 1.4 | root (0, 2.4, 2.4) | 13 |
| 39 | `tail_tip` | curled hook + leaf curl | cards | 1.0 | 0.8 | end of tail_6 | 13 |
| 40-41 | `vine_l/_r` | P3 white-bud vines (scale 0 in P1) | thin boxes + bud cubes | 1.5 | 2.0 | upper arm | 13 |
| 42 | `collar` | P3 collar ruff (scale 0 in P1); it can merge into `hood` if the budget is tight | petal cards | 1.4 | 1.0 | = neck | 13 |
| 43 | (opt) `core_shell` | translucent glass bulb separate from the glow, so the shell can be 14 while the seed is 15 | knob | 1.6 | 0.9 | = core_glow | 14 |
| 44 | (opt) `gem_glow` | P3 emerald crystals at brightness 15 | boxes | 2.0 | 2.5 | = thorax / hood | 15 |

Notes:
* **Burrow** (잠복 돌진, 이동 돌진, the phase-2 entry): sink the root below the opaque floor and scale the parts to 0 under
  it; the pool and shadow are props (rigtech TL;DR 6).
* **Spiral column / arms raised as a flower** are poses of the arm and flap chains; no extra parts are needed.
* **Long parts and tolerances**: the arms (6 b) and the tail (8 b) need per-part `tol.t` scaling (0.03-0.035 b) and the
  whole-body yaw on the anchor (rigtech TL;DR 5).

### 9.3 Rest poses (rig space, b; full joint lists in `rig_plan.json`)

| joint | P1 crouch idle | P3 upright idle |
|---|---|---|
| hood top / crown tip | 4.3 / 5.0, hood centre z −2.6 | 8.5 / 9.0, hood centre (0, 7.6, −0.6) |
| thorax | centre (0, 3.0, 0), hump top 4.5, belly 1.8 | vertical, y 2.2-5.6, z −0.8..0.6 |
| belly core / face glow | core (0, 1.6, −1.2) | face (0, 7.8, −1.4); navel (0, 4.2, −1.0) |
| long arms | shoulder (±1.6, 3.6, −0.8) → elbow (±3.4, 2.6, −1.6) → wrist (±4.8, 0.6, −2.4) → claw on the floor (±5.3, 0.15, −2.6) | raised: shoulder (±1.2, 5.4, −0.2) → (±2.8, 6.2, −0.4) → (±4.2, 6.6, −0.6) → hand tip (±4.9, 7.1, −0.6) |
| front legs | (±1.4, 3.2, −1.6) → (±2.3, 2.2, −2.6) → (±2.4, 0.4, −3.2), hand (±2.5, 0.15, −3.7) | splayed: (±1.0, 2.0, −0.6) → (±2.4, 1.4, −1.6) → (±3.4, 0.4, −2.2), leaf hand flat (±3.8, 0.15, −2.5) |
| rear legs | (±1.3, 2.8, 1.2) → (±2.6, 2.4, 1.8) → (±2.9, 0.4, 2.4), foot (±3.0, 0.15, 2.9) | (±1.0, 1.6, 0.8) → (±2.4, 1.2, 1.2) → (±3.4, 0.4, 1.4), (±3.8, 0.15, 1.7) |
| flaps | (±1.5, 4.0, −0.4) → (±3.2, 3.4, 0.1) | mid arms (±1.2, 4.4, 0) → (±3.7, 3.9, −0.4) |
| drapes | cowl sides (±1.2, 3.2, −2.2) → the ground (±1.7, 0.2, −2.7) | hair (±0.9, 6.8, −0.7) → waist (±1.2, 4.0, −1.0) |
| tail | root (0, 2.4, 2.4), on the ground from z 4.5 to 9.9 | root (0, 0.6, 1.0), on the ground to z 8.8 (coils in attacks) |

### 9.4 Textures (a new `apep_paint.mjs` on `mboss_paint_lib.mjs`; 4x supersampling, sides multiples of 16, ≤ 512)

Each sprite exists twice (`_p1`, `_p3`) unless marked. Estimates are per look.

| sprite | size | notes |
|---|---|---|
| `ap_hood_plate`, `ap_hood_face` | 128x64, 128x128 | plate rows with bevel stripes; face plate with V + crescents (P1) or the bud skull underside; P3 lime plates with grey peel |
| `ap_crest` (P3), `ap_sprig` (shared) | 128x64, 64x64 | alpha leaf crest; alpha gold sprig |
| `ap_crystal_gold` (P1), `ap_crystal_emerald` (P3), `ap_cone_cream` | 32x64 each | 2-tone facets |
| `ap_gem` (P1) | 32x32 | square gem + dark frame |
| `ap_thorax_top`, `ap_thorax_side`, `ap_ribs` | 128x128, 128x64, 128x64 | hump plates; pale side plates with wood-grain swirls; ribcage swirls; P3 chest leaf plates + back bottle green |
| `ap_limb` | 64x128 | dark → pale gradient with plate rims (legs); P3 lime leaf cladding |
| `ap_arm` | 64x128 | pale shell plates + inner leaf-scale rows; P3 leaf blades |
| `ap_petal`, `ap_claw` | 64x64 each | petal with vein + outline; 3-lobe claw; P3 lobed leaf hand |
| `ap_flap`, `ap_drape` | 64x128 each | alpha leaf flap (dark out, pale in); dark ribbon; P3 lime leaf arm / hair strand |
| `ap_tail` | 64x128 | diagonal 2-band helix stripes + the hook card |
| `ap_core_p1`, `ap_face_p3`, `ap_veins_p3` | 64x64, 128x128, 64x128 | emissive (`paintT`, alpha 0 at the borders) |
| `ap_vine`, `ap_bud`, `ap_collar` (P3 only) | 64x16, 16x16, 128x64 | — |

That is ≈ 0.21 M px per look and ≈ 0.45 M px for the rig, well under the 1.2 M px chapter budget, so the hood, face and
hands can go to 64 px/b.

Props and kit (outside the rig):
* Heart: `heart_bulb` 128x128, `heart_root` 64x128, `heart_tip` 32x64.
* Organisms: ≈ 14 sprites of 64-128 px.
* Total ≈ 0.15 M px.

## 10. Not visible or uncertain (proposed)

* **P3 size**: no same-depth reference. If the third-person camera at 4 b clips the hood, lower the P3 rest pose to 7.5 b.
* **P1 face** (the closed bud skull): only glimpsed in v2's upright frames (v2.md zooms). Paint it on the hood underside;
  no extra part.
* **Exact count of P1 shoulder flaps** (2 vs 3 per side): 2 per side is enough for the silhouette.
* **Back of P1** (never clean): assume the hump plates continue the cowl with a gold spine ridge (`v1 f720`, `v2 f870`).
* **Organisms from behind**: assume radial symmetry for basic, guarding and destruction; nesting and predatory have a
  front (orb / eye).
* **Death**: not in the footage. Proposal: P3 sinks to its knees, the face glow fades, the leaf hands wilt and close
  (curl their pose), the emerald crystals dim, then a scale-out with a burst of white-bud petals (fx).

## 11. Open checks for the builder

* Translucent shells (belly bulb, Heart, organisms): keep alpha 0 at the sprite borders and check the depth order against
  the glow cards (fieldgen bubble rule).
* Cones built as 45° diamond stacks must read as cones from above; check them at 4-8 b.
* The tail helix: check that the 45° per-segment roll does not flicker at the clip blends; tail segments are symmetric
  every 180°.
* P3 vines on the arms: they must follow the arm chain. Parent them to `arm_up` in the pose (offset in arm space) or make
  them part of the `arm_up` P3 model if the budget is tight.
* Heart: the arrival squash (scale 1 → 1.15 x 0.85 → 1) and the 0° → 65° lean must not clip into the roots.

## 12. Annotated sheets in `understand/model/`

| file | content |
|---|---|
| `01_p1_parts_annotated.jpg` | phase 1: front reared (v2 f2040), side (v2 f870), tail swipe (v2 f1245), the best clean front (v2 f2076) and arms-up (v2 f417), 27 numbered parts + legend |
| `02_p1_closeups.jpg` | phase-1 close-ups: hood from above with the sprig (v1 f255), gem + crescent + petal foot (v1 f315), 3/4 crouch (v1 f285), underside ribcage (v2 f480) |
| `03_p3_parts_annotated.jpg` | phase 3: front upright (v6 f495), back (v5 f1875), side close (v6 f105), head close (v5 f450), serpent coil (v6 f300), 25 numbered parts |
| `04_p1_vs_p3.jpg` | 9 matched views of phase 1 and phase 3 + the list of every change |
| `05_heart_and_egg.jpg` | Heart close (v5 f198), glowing (v3 f30), pedestal (v2 f2340), with the player (v3 f300), and the w2 egg sequence |
| `06_organisms.jpg` | all 6 organisms in every form seen, numbered, with sizes |
| `07_proportions_measured.jpg` | measurement overlays (P1 front, foot vs player, P3 front, Heart vs player, phantom view) + the size summary |
| `08_palette.png` | 35 recommended ramps (P1, P3, P2, fx/glow) with their sources |
| `09_rig_breakdown.png` | P1 crouch and P3 upright joint schematics (side + front, 1 b grid, 1.8 b player) + the part legend |
| `10_best_reference_frames.jpg` | the 30 best frames below as a contact sheet |

### 12.1 Best reference frames per part

| part / view | frames |
|---|---|
| P1 whole silhouette, front | **v2 f2076** (clean, player for scale), v1 f1110 (far), v2 f2040 (reared) |
| P1 side | **v2 f870**, v1 f720, v2 f1125 (with the tail) |
| P1 3/4 and textures (plates, limb armour, crystals) | **v1 f290**, v1 f285 |
| P1 hood from above, sprig, seed bulb | **v1 f255**; v1.md `k_f0090` (intro hood close-up) |
| P1 shoulder gem, crescent seam, petal foot close | **v1 f315** |
| P1 belly core lit | **v2 f417** (arms-up), v1 f1068 (half-stand), v2 f2040 |
| P1 underside / ribcage / arm inner faces | **v2 f480**, v1 f1560 (arms raised as a flower) |
| P1 spiral column | v1 f2238 |
| P1 long arms and claws | v2 f2076 (planted), v2 f417 (raised), v2 f960 (close) |
| P1 tail | **v2 f1125**, v2 f1245, v1 f2010 (v1.md) |
| P3 front | **v6 f495**, v5 f2265, v5 f720, w1 15-16 s |
| P3 back | **v5 f1875** |
| P3 side, hood crystals, emerald | **v6 f105** |
| P3 head close (crest, sprig, lime plates, peel, gem) | **v5 f450** (cut-scene) |
| P3 tail coil | v6 f300, v5 f1875 |
| P3 glow states (종말의 여파) | w1 4.6-16 s |
| Heart close | **v5 f198**; arrival v2 f2358; cradle v2 f2418, v3 f30; pedestal v2 f2340 |
| Golden egg + vine hand | w2 0.0-10.8 s (`w2_0001`, `w2_0012`, `w2_0041`, `w2_0047`) |
| basic | wiki `15.png` (sac), v3 f300 (bells), v3 f990 (sac rolling) |
| nurturing | **v3 f1260**, v3 f300 |
| guarding | **v3 f2160**, v3 f2040 (phantom silhouette) |
| nesting | **v4 f840** (real colour), v4 f810, v4 f630 (silhouette), v4 f765 (walls) |
| predatory | **v4 f1920** (bud), **v4 f2400** (fish), v4 f2205 (closed face), v4 f1956 (pod) |
| destruction | **v4 f1185**, v4 f1200, v4 f1320 (blast) |
