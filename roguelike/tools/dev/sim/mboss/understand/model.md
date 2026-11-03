# Corrupted Guardian (파수꾼・타락 / 개안자 "Nihilita") — modelling spec for a display-entity rig

Sources: `src/ref.png` (500x399 render), the 2244x1789 render inside `src/guide.pdf` (p.2, extracted to
`modelwork/pdf/img-003.jpg`), the boss icon (`modelwork/pdf/img-002.jpg`), m1–m4 frames (1920x1080, 60 fps),
and the per-video reports `understand/m1.md … m4.md`.
Frame notation: `m2 f1085` = 60 fps frame 1085 of m2 = 18.083 s = tick 361.7 (tick = s x 20 = f / 3).
Annotated sheets are in `understand/model/` (list in §12). Working crops and the scripts live in
`scratchpad/mboss/modelwork/` and `scratchpad/mboss/modeltools/`.

Conventions used below (the same as `tools/build_raiden_rig.mjs`):
* "her right / her left" = the boss's own sides. In a front view her right is screen-left.
* Rig authoring space: +X = her left, +Y = up, -Z = forward (the poser mirrors z at the end, as in Raiden's `posed()`).
* **BH** = boss height from the foot bottom to the top of the head crest. **b** = Minecraft blocks.

---------------------------------------------------------------------------------------------------

## 0. Corrections to the task brief

* **The shield and the wing are both on her LEFT.** There is **one** big wing, and the gold winged
  pauldron/shield is its "wrist". The spear is in her **RIGHT** hand, and that arm is the corrupted red-black one.
  This is consistent across ref.png, the PDF render and every in-game front view (m2 f600, m2 f1085, m1 f1330,
  m1 f1060) and back view (m3 f1530, m1 f1419). The brief's "shield on her right" is wrong.
* Her head has **no human face**. It is a white winged crest framing a red 4-point diamond with **one** glowing
  eye (boss icon, `08_head_halo.png`).
* She has **legs**, but they are thin columns of dark voxel cubes, mostly hidden by the skirt. She **never walks**.
  She hovers, glides and flies (§4).

## 1. Overall size and proposed scale

Measured in-game (see `02_scale_proportions_m2_f1085.png`):

| measurement | value | source |
|---|---|---|
| boss foot bottom to crest top | 450 px, against the player's 300 px (Clorinde, hat included) | m2 f1085 (18.08 s, t361.7) |
| ratio boss/player after ≈1.08 depth correction | **1.6 (body), 1.85 with the halo** (≈1.75 / 2.0 against the player without the hat) | m2 f1085; m1 f1060 gives 1.6 / 1.8 |
| spear length | **1.45 BH** (1.4–1.5) | m2 f600, m2 f1000, ref |
| shield | 0.47 x 0.40 BH, centre 0.47 BH out from the neck | m2 f1085, m1 f1330 |
| wing primaries | ≈0.8 BH long; the wing assembly spans 1.2–1.4 BH from the shoulder | m1 f1330, m3 f1530 |
| idle hover (feet above the floor) | 0.1–0.2 BH | m1 (0.3–0.5 m), m3 f1622 |
| chaos hover | feet ≈1.0 BH up | m3 f1740 |

**Proposal: BH = 3.0 b.**
* With the halo spike, the head reaches 3.42 b. The idle hover adds 0.35 b, so the silhouette top is about
  **3.75 b** above the floor, about 2x the 1.8 b player. That matches the measured 1.6–1.85x body ratio, with the
  hover on top, and she clearly looms.
* The 4.35 b spear gives about 3.2 b of reach in front of the hand. This fits the measured AoEs: the slam ring
  r ≈ 5 b about 3.5 b in front, and the 360° swings at r 5–6 b.
* She is the same size class as the armoured Narukami rig (body scale 1.58 x 1.8 + 1.05 lift ≈ 3.9 b top), so
  existing camera and arena choices (r ≈ 23 b arenas) work unchanged.
* A smaller BH (2.5) would weaken the "looming" read and make the spear's reach look short. A larger BH (3.5+)
  pushes the wing and halo out of the third-person frame at melee range.
* Gameplay hurtbox (not visual): about 1.2 b wide x 3.0 b tall, centred on the torso and skirt. It excludes the
  wing and the spear. It rises with the hover.

Landmark heights (b above the foot bottom; add the 0.35 b hover for world height):

| landmark | BH | b |
|---|---|---|
| halo top spike tip | 1.14 | 3.42 |
| crest top (horn-feather tips) | 1.00 | 3.00 |
| halo ring centre (behind the head) | 0.95 | 2.85 |
| eye / face diamond | 0.91 | 2.74 |
| chin / neck | 0.87 | 2.61 |
| shoulder joints | 0.80 | 2.40 |
| gold crown-belt (red star) | 0.59 | 1.78 |
| skirt front-panel hem | 0.10–0.13 | 0.3–0.4 |
| ankle / top of the foot cubes | 0.10 | 0.30 |
| foot bottom | 0 | 0 |

Widths: halo ring outer r 0.11 BH (0.33 b); head with crest side-wings 0.2 BH (0.6 b); shoulders 0.26 BH
(0.78 b); waist 0.12 BH (0.36 b); skirt at the hips 0.45 BH (1.35 b, hip wings included); skirt hem
0.55 BH (1.65 b).

## 2. Silhouette

* **Front:** a narrow white vertical column (skirt panels) under a tiny dark-red torso. A huge gold-and-white
  fan (shield + wing) sits up and out to her left. A long gold diagonal (the spear) crosses to her right, and a
  gold halo with a tall spike sits above the head (`13_front34_m1_f1060.png`).
* It is strongly asymmetric. Her left half reads gold/white and massive. Her right half reads as a thin
  crimson-black voxel arm plus the gold spear line.
* **Back:** the same fan from behind. The shield is double-sided (the eye shows on the back too). Voxel legs show
  between the skirt panels (`04_back_view_m3_f1530.png`).
* **Side:** the halo is a flat ring in the body's frontal plane, nearly edge-on from the side. The wing and its
  shield also lie roughly in the frontal plane, so from the side the silhouette is thin
  (`05_side_back34_m3_f1300.png`). That is why flat stacked cards suit this model.

## 3. Part list

### 3.1 Head, face, crest (`08_head_halo.png`)
* **Head core:** a small dark crimson-black head (0.26 x 0.30 x 0.26 b) on a neck of dark-red voxel cubes.
* **Face:** a 4-point diamond (dark red `#B8402A` to orange) with **one eye**: a pale-yellow ring and dot
  (`#F8F2A8`), glowing.
* **Crest:** white feathers with grey outlines:
  - 2 tall inner horn-feathers rising from the brow to 3.00 b, slightly curved outward;
  - 2 outer side-wings (3 feathers each) sweeping out-and-up, 0.6 b total width;
  - a gold trim line under the diamond.
* **No hair.** The "white hair/veil" in the m1 report is the crest feathers plus the collar plates.

### 3.2 Halo / crown (`08_head_halo.png`, sheets 03 and 13)
* **Shape:** a thin gold-white ring (outer r 0.33 b, ring width ≈0.04 b) with an inner faint ring and a hot core
  glow. A **tall top spike** (≈0.5 b, `#F3D978`) and 2 short lower spikes at about 4 and 8 o'clock sit on the
  ring. 6–8 thin rays come off it.
* **Placement:** centred 0.11 b above the eye and 0.12 b behind the head. It lies in the frontal plane and
  follows the head.
* **Glow:** always lit. It **blazes** in groggy and at the chaos start (glow card x1.5–2, `#F7E2A6` core
  `#FEEAC3`). The red cross sigil hides it during chaos (that is FX, not rig).

### 3.3 Torso (`03_front_body_m2_f0600.png`)
* **Chest:** small and slim, 0.55 b wide, 0.5 b tall. A red/black core with gold edge trims.
* **Collar:** jagged white/black zig-zag feather-plates (like a ruff) with small black 4-point stars, and a
  **red ring "eye" gem** on the collar's left.
* **Left shoulder:** a gold plate from which the shield bracket starts.
* **Waist:** 0.36 b, ending in the **gold crown-belt**: a V-shape with up-pointing spikes and a red 4-point
  star at the front (at 1.78 b).

### 3.4 Arms
| | RIGHT arm (spear arm) | LEFT arm (shield side) |
|---|---|---|
| look | **corrupted**: a jagged voxel arm in crimson/black (`#A93B27` / `#812E21` / `#5F1D13` / `#2A1418`) with glowing red cracks (`#FF5A3C`); cubes peel off the shoulder | slim; a white upper arm, then a **gold gauntlet** forearm with an amber glow strip (`#F2AB76` / `#E4833C`, hot `#FBDFD4`) |
| hand | red **claw** with long red talons; holds the spear (fist), or open claw when casting (the pull) | gold claw hand with long fingers; usually open and hanging, joins the shaft for two-hand moves |
| segment lengths | upper 0.50 b, forearm 0.48 b, hand 0.25 b; thickness 0.20 b (bulky, irregular) | upper 0.48 b, forearm 0.46 b, hand 0.25 b; thickness 0.14 b (gauntlet 0.18 b) |

### 3.5 Lower body: skirt, legs, hover (`09_skirt_legs_cubes.png`)
* **Tabard:** hangs from the belt. White feathers with **three red 4-point stars** across the top.
* **2 long front panels:** layered white feathers with jagged notches. They reach the ankle (hem 0.3–0.4 b).
  A slit between them shows the legs.
* **2 hip feather-wings:** one per side, 4–5 feathers fanning out and down, ≈0.6 b long, starting just under
  the belt.
* **2 outer flared panels:** long feathers that flare outward at the hem, like hakama spikes, out to ±0.8 b.
* **A back panel.**
* **One long S-curved tail streamer** from her LEFT hip. It is ≈1.8 b long and nearly reaches the floor
  (m1 f340, m1 f1060). A small gold hip ornament with a red eye sits at its root.
* **Legs:** yes. Each leg is a column of **5–6 stacked dark voxel cubes**. Each cube is ≈0.18 b, slightly offset
  and turned (glitchy), with faces `#481E1C` / `#330F21` and red-orange glowing edges and rune circles
  (`#EE485A`, `#FC5454`).
* **Feet:** a pair of larger dark cubes (0.24 b) turned 45°, carrying a red rune ring (m2 f1085, m1 f340).
* **Below the feet:** loose cubes trail and fall (ref).
* **Hover:** she never walks.
  - Idle: feet 0.3–0.5 b above the floor, legs dangling, a slow bob.
  - She moves by gliding and dashing. Long moves use a leap, an arcing flight and a landing.
  - She touches the floor only in groggy, and briefly after landings.

### 3.6 The wing — one, on her LEFT (`10_wing.png`)
* **Mounting:** it hangs from under the shield. Its root is a gold joint with a black 4-point star at about
  (+0.75, 2.25, +0.15) b, roughly in the frontal plane.
* **Three tiers:**
  1. **Coverts:** 6–8 short rounded feathers, cream with a gold tint (`#F6E6C2` / `#E6CC94`), 0.4–0.6 b, under
     the shield.
  2. **Secondaries:** 7–9 white feathers, 1.2–1.5 b.
  3. **Primaries:** 6–8 long blade-like white feathers, **2.0–2.4 b**. Pointed tips with a slight S-curve, grey
     outline (`#6E6370`), soft grey shading.
* **Fan angles:**
  - Idle: the fan hangs down-and-out about 20–40° from vertical, with the primary tips ≈0.6 b above the floor.
  - Guard: the fan opens to ≈60–70° total and the primaries lift up to ≈+25° above horizontal (m2 f300).
  - Get-up: it spreads to its widest, 1.2–1.4 BH span (m3 f1530).
  - Groggy: it droops low and sideways (m3 f1148, f1300).
* Both faces are white; the back is the same design, slightly greyer.

### 3.7 The gold winged pauldron / shield — her LEFT (`07_shield_detail.png`)
* **Bracket:** a **gold bracket arm** (2 round joints, ≈1.05 b) carries it from the left shoulder. Shield centre
  ≈(+1.35, 2.65, +0.05) b at rest, roughly level with the neck.
* **Size and pose:** 1.4 x 1.2 b. A long frame spike points up-out-forward. The shield is tilted ≈30° (its
  spike leans toward her head).
* **Design: the "eye" of 개안자:**
  - an outer almond "eyelid" frame in gold;
  - an inner 4-point star frame in gold;
  - a **gem** with a white core and orange bezel (`#FFF6E2` / `#F2A060`) on a dark maroon field (`#4A1703`),
    with an amber "iris" crescent (`#F7BC5C`);
  - 4 blade-feather spikes along the trailing edge.
* The back shows the same eye mirrored, so it is double-sided.
* **Element state:** when an element is recorded, the **gem and field glow in that element's colour** (Electro
  violet `#E484FC` in m2 f1085). In guard mode the whole shield glows gold.
* **Groggy pose B:** the bracket swings the shield **in front of her body** like a guard (m3 f1450).

### 3.8 Red accents
* Red 4-point stars: one at the belt, three on the tabard.
* The face diamond.
* The red ring gem on the collar.
* The spear-ring gem and the butt star.
* The whole corrupted right arm, the neck voxels, and the leg and foot cubes with their red runes.

### 3.9 Floating red/black cubes (`14_cubes.png`)
* **Body cubes (rig parts):**
  - small **solid** dark-crimson cubes, 0.12–0.25 b, with a lit top face;
  - they peel off the right shoulder and neck, orbit the corrupted arm, hang by the legs and fall below the feet;
  - always present; they drift slowly and are replaced.
* **FX cubes (not rig):** hollow wireframe cubes with glowing red edges, 0.4–0.8 b, led by a gold cube. They are
  used in chaos streams, the pull cage, the flight trail and the fail-spear assembly. Build them with the
  pattern FX.

### 3.10 The spear (Geo) (`06_spear_detail.png`)
**Length 1.45 BH = 4.35 b.** Its head lies in one plane. Fractions are measured from the tip (0) to the butt (1):

| fraction | part | size | colour |
|---|---|---|---|
| 0–0.36 | leaf **blade**, long and narrow, a white-hot core with gold flanks | max width 0.22 b at f≈0.3 | `#FFF8DE` core, `#F9E7A6` / `#F0C878`, edge `#D99A4E` |
| 0.33–0.38 | 2 **back-swept barbs** (toward the butt) | span 0.85 b | orange-brown `#B96B22` with gold edges |
| 0.39–0.52 | an oval **ring** framing a **red/black 4-point star gem** with a white glint | ring Ø 0.6 b, gem 0.35 b | gold `#DC9256`; gem `#C83A28` / `#5A0F0A`, glint `#FFF4E0` |
| 0.52–0.54 | **collar** | 0.18 b | gold |
| 0.54→0.73 | **crescent**: two **mirrored swept-back wing-blades** grow from the collar, curve out to ±0.48 b, then hook back inward. The tips sit at f≈0.73, either side of the hand. | span ≈1.0 b | pale gold, 1 notch each |
| 0.54–0.92 | thin gold **shaft** | Ø 0.07 b | `#C9A35E` |
| **0.74** | **grip** (corrupted right hand) | | |
| 0.92–1.0 | **butt finial:** red 4-point star | 0.3 b | `#D8553A` |
| ≈1.03 | a small red star floating past the butt | 0.12 b | |

* **Grip:** in game the right hand holds the shaft at **f≈0.74**, nestled between the crescent tips (m3 f1148,
  m2 f1085, m1 f1060). The PDF render holds it lower (0.57). Follow the game.
* **Glow:**
  - The blade and crescent always glow softly gold.
  - During attacks a gold energy streak runs along the shaft and blade (core `#FCF5AE`, mid `#CDB37E`,
    edge `#9D8650`; m1 f40).
  - When an element is recorded, the whole spear is enchanted in that colour (Electro violet in m2).
  - In chaos she uses red, gold and blue giant spears; those are separate FX props (m4).

## 4. Colour palette

`12_palette.png` holds the full swatch sheet. Key hexes:

| group | hexes |
|---|---|
| feathers | white `#F7EEEC`, light `#EBDFDB`, shade `#CFC3C1`, deep `#A69A99`, outline `#6E6370`, sky-bounce `#B9C2D8` |
| coverts (gold-tint feathers) | `#F6E6C2`, `#E6CC94`, `#C9A86E` |
| gold armour | hi `#FAE3BE`, lit `#E2B885`, mid `#BF9B6C`, dark `#9C7347`, deep `#5E3A1C`, line `#2E1608` |
| spear | core `#FFF8DE`, lit `#F9E7A6`, mid `#F0C878`, edge `#D99A4E`, barb `#B96B22`, shaft `#C9A35E`; gem `#C83A28` / `#5A0F0A`; butt star `#D8553A` |
| shield eye (Geo) | core `#FFF6E2`, bezel `#F2A060`, iris `#F7BC5C`, field `#4A1703` |
| corrupted arm / neck | `#A93B27`, `#812E21`, `#5F1D13`, `#2A1418`, cracks `#FF5A3C` |
| voxel legs / body cubes | faces `#481E1C` / `#330F21` / `#782824`, edges `#EE485A`, runes `#FC5454` (FX lead cube `#E4CC54`) |
| red ornaments | star `#C21F2A`, dark `#6E0001`, face `#B8402A`, eye `#F8F2A8` |
| halo | core `#FEEAC3`, ring `#F7E2A6`, spike `#F3D978`, glow `#EAD561` |
| Geo FX | `#E4B43C`, highlight `#FCE484`, white rim `#FCFCE4` |
| left gauntlet glow | `#FBDFD4`, `#F2AB76`, `#E4833C` |
| element record tints | Electro `#E484FC`, Pyro `#FF8A4C`, Hydro `#5CC8FF`, Cryo `#A2FEFD`, Geo `#E4B43C` (Electro and Cryo were measured in m2/m3; Pyro and Hydro were not observed and are proposed) |
| chaos red (FX) | `#C21F2A`, `#AE1120`, rim `#6E0001`, haze `#C43F55` |

**What glows** (display brightness 15 and/or a translucent glow card):
* always: the halo, the eye, the shield gem, the spear blade and crescent, the left gauntlet strip, the red runes
  and cracks on the voxel parts;
* during attacks: the spear energy streak;
* in guard mode: a gold aura on the whole body, the shield and the spear, plus small gold square motes;
* after a record: the element tint on the shield eye and the spear;
* in groggy and at the chaos start: the blazing halo.

## 5. Articulation needed by the patterns

Times are from the per-video reports. "Must move" lists the joints that carry the pose; small secondary motion
(bob, cloth lag) is listed separately.

| pattern | key poses (source) | must move |
|---|---|---|
| idle hover | spear low-diagonal, tip to her right-front-down, butt up across the chest; wing hanging; slow bob (m1 f0, m4 f469) | root y bob (±0.05 b / 40 t); wing tiers breathe ±5°; skirt and tail sway; body cubes drift |
| 1 thrust x2 | wind-up: spear level, cocked back, torso yawed −30°, wing flares up (m1 f40, 0.67 s). Lunge: root translates forward, right arm extends. Thrust 2: hop back into the air, then a dive with the **whole body pitched** nose-down (m1 f170, 2.83 s) | root position **and pitch**; torso yaw; right arm (shoulder, elbow); spear aim; wing raise |
| 2 javelin | twirl, back-leap, overhead wind-up; release (7.63 s); empty hands; the spear returns along the line; overhead catch, lower and twirl (m1 5.3–9.5 s) | **detach the spear** (world-space prop); empty-hand pose; overhead arm; catch |
| 3 melee slam | spear raised overhead with two hands (m1 f712, 11.87 s), stab down; the spear **stays stuck in the ground** (m1 f790) for 1.1 s; pull-out; twirl | two-hand grip (left hand onto the shaft); torso pitch +30°; **spear left planted** (prop) while she hovers by it; twirl about the shaft centre |
| 4 pull + 2 swings | open-claw cast (right hand); then wind-up with the spear level forward and the torso twisted (m1 f1390); two **360° swings** (m1 f1419): root yaw spin with the arm extended, the spear level | root yaw 360°; right arm extension; spear level at waist height; wing swings with the spin |
| 5 fly-slam | spear vertical, glint (m1 f1599); ascent out of view; descend and slam, spear vertical point-down; spikes; pull and twirl | root flies (y +6 b, fast); spear vertical in two hands; legs and skirt trail |
| 6 guard mode | baton **twirl** in front (m2 0.7–1.5 s); pose with the spear diagonal up-right, wing **raised and opened**, shield glowing (m2 f300); then the end swing: spear behind the right shoulder, 180–210° horizontal sweep | spear spin about the shaft centre (hand slides to mid-shaft); wing open/raise; shield glow and eye tint; torso wind-up and sweep |
| 7 chaos | leap and arcing flight to the centre (body leaning forward, wing swept back); rise 3 b; hover with the **arms up and the spear horizontal behind the shoulders** (m3 f1740); fail: twist with the wing swept across the front (m4 1.0 s) | root flight, pitch +20–35°; both hands on the spear behind the head; wing spread; legs and skirt trail back |
| groggy (11 s) | fall; **pose A**: the spear planted head-down at her right, corrupted hand on the shaft top, body slumped, wing drooped, halo blazing (m3 f1148). **Pose B**: head bowed, torso folded forward, **shield swung in front** (m3 f1450). **Get-up**: wing spreads wide, she lifts off (m3 f1530) | the spear left planted (prop); torso pitch +35–45°; head pitch +30°; **bracket yaw ≈+110–130° and pitch** (shield to the front); wing droop/spread; root lower to the floor |
| entrance | appears; the spear **plants into the ground** (the spear hit deals damage); pull-out; idle | spear prop drop/plant; hand reaches to the planted spear |
| death | not in the footage. Proposal: groggy-A slump, then a dissolve into red cubes + gold motes (like Raiden's death shards) | torso/head slump; per-part shrink; cube burst FX |

Joint list (DOF):
* **root:** position + full rotation (yaw, pitch, roll). Raiden's poser already rotates the rig about the hip.
* **torso:** pitch, yaw, roll.
* **head:** pitch, yaw. The halo follows the head.
* **right arm:** shoulder (3), elbow (1–2), wrist (3).
* **left arm:** shoulder (3), elbow (1–2), wrist (3).
* **bracket:** 3-DOF ball at the left shoulder. The shield rides on the bracket's end with its own 2-DOF tilt.
* **wing:** root (3) plus one opening angle per tier (coverts, secondaries, primaries, each about the root).
* **skirt:** front-panel group pitch, outer group pitch/roll, tail streamer pitch/yaw.
* **legs:** 2 x (pitch, roll) at the hips. The feet are rigid with the legs.
* **spear:** 6-DOF. Attached to the right-hand grip by default, optionally driven by two hands, or **detached**
  (hidden in the rig and replaced by a world prop).

Recommended rig method (from Raiden's auxiliary arms):
* Author the arms by **joint positions** (sh / el / wr) and orient each segment with `aimDown`. Scale the segment
  along its length so the hands stay glued to the spear in two-hand poses. Clamp the stretch to ±10%.
* Author the spear frame as `bq(tip, edge)`, with the blade plane as the "edge" axis.
* Slerp the rotation keys.
* Apply the contact-tick retime exactly as in `build_raiden_rig.mjs`.

## 6. Display entities and construction plan

All parts are `minecraft:item_display` with `item_display:"none"` and an `item_model` from the new
`rlk:guardian/*` set. Element coordinates stay within −16..32. Element rotations are single-axis, in 22.5° steps
within ±45°. Size comes from the display `transformation.scale`. Pivot = model [8,8,8]. 1 model unit = scale/16 b.

| # | display | content | build | scale | pivot (rig b, rest) | bright |
|---|---|---|---|---|---|---|
| 1 | `pelvis` | belt (gold V, spikes), red belt star, tabard top with 3 red stars, hip ornament | painted boxes + alpha plates | 1.0 | (0, 1.78, 0) | 13 |
| 2 | `skirt_front` | 2 long front panels (layered feathers) | 2 stacked alpha cards (z ±0.2) per panel + 1 crossed card | 1.25 | belt (0, 1.78, −0.08) | 13 |
| 3 | `skirt_outer` | 2 outer flared panels + back panel + 2 hip wings | alpha cards: side panels as `cardX` turned ±22.5°, hip wings as `card` turned ±45° about Y | 1.25 | (0, 1.75, 0) | 13 |
| 4 | `tail` | left-hip S-streamer | 2 stacked alpha cards (S painted in the sprite) | 1.5 | (+0.22, 1.70, +0.05) | 13 |
| 5–6 | `leg_r`, `leg_l` | 5–6 voxel cubes + a 45° foot-cube pair | boxes (some turned 22.5°/45° about Y), textures `gd_vox` / `gd_vox_rune` | 1.2 | hips (∓0.10, 1.60, 0) | 15 (runes) / 12 |
| 7 | `torso` | chest core, gold trims, zig-zag collar plates, collar ring gem, left shoulder plate | boxes + alpha plates | 1.0 | waist (0, 1.85, 0) | 13 |
| 8 | `head` | head core, crest (2 horns + 2 side wings), face diamond | small boxes; crest as `card` + `cardX` crossed alpha cards | 1.0 | neck (0, 2.61, 0) | 13 |
| 9 | `eye` | eye ring + dot + diamond glow | plate + translucent glow plate | 1.0 | = head | 15 |
| 10 | `halo` | ring + top spike + 2 lower spikes + rays | 1 alpha-cut `plate` (both faces) + 1 thin ring box core for edge views | 1.0 | head + (0, 0.24, +0.12) | 15 |
| 11 | `halo_glow` | radial glow + rays (translucent) | 1–2 gradient cards; scale-animated for blaze | 1.0–2.0 | = halo | 15 |
| 12–14 | `r_upper`, `r_fore`, `r_hand` | corrupted voxel arm; claw hand models `fist` / `open` / `claw` | jittered boxes (`gd_corrupt` with crack texture); talons as thin boxes | 1.0 | sh (−0.33, 2.42, 0) | 12 (cracks: texture) |
| 15–17 | `l_upper`, `l_fore`, `l_hand` | white sleeve; gold gauntlet with amber strip; gold claw (`open` / `grip`) | painted boxes (`gd_gold`, `gd_gauntlet`) | 1.0 | sh (+0.33, 2.42, 0) | 13 / l_fore 15 |
| 18 | `bracket` | gold arm, 2 round joints, black 4-point star | painted boxes + 2 plates | 1.0 | (+0.30, 2.50, +0.08) | 13 |
| 19 | `shield` | eye shield | 3 stacked alpha cards `gd_shield` (z 7.6/8.0/8.4) + 1 thin painted core box (edge views) | 1.0 | shield centre (+1.35, 2.65, +0.05) | 14 |
| 20 | `shield_eye` | gem + maroon field + iris | 2 plates (front/back) slightly proud of the shield; **constant item tint per element** (`shield_eye_geo` / `electro` / `pyro` / `hydro` / `cryo`) | 1.0 | = shield | 15 |
| 21–23 | `wing_cov`, `wing_sec`, `wing_pri` | the 3 feather tiers | 2 stacked alpha cards each (z ±0.25 units) + 1 `cardX` spine card on the primaries | 2.0 | wing root (+0.75, 2.25, +0.15) | 13 |
| 24 | `spear` | the spear (§3.10) | head on 3 stacked alpha cards (`gd_spear_head`, z 7.64/8/8.36) + crossed `cardX` for the edge view; shaft as `fitting` boxes (`gd_shaft`); collar boxes; ring gem `plate` both faces; butt star crossed cards; orbit star plate | **2.2** | grip at model y=8 | 15 |
| 25 | `spear_glow` | energy streak / enchant aura | translucent cards along the blade and shaft; **item tints** geo/electro/pyro/hydro/cryo/red | 2.2 | = spear | 15 |
| 26–28 | `spear_trail_1..3` | afterimages for thrusts and swings | translucent trail cards (Raiden `blade_trail` style), tapered | 2.2 | sampled at t−0.55n | 15 |
| 29–31 | `cubes_a` (right shoulder/arm), `cubes_b` (legs/below the feet), `cubes_c` (neck) | clusters of 4–6 solid voxel cubes | boxes, textures `gd_vox` | 1.0 | attached to arm / pelvis / torso | 13 |

**Total: 31 displays** (Raiden: 52). Optional extras:
* a guard-mode body aura card (gold);
* a separate `gauntlet_glow` card if brightness 15 on `l_fore` looks too flat.

Separate props that use the same models but are not rig-tagged (like Raiden's `target_slam` hand), so the rig
`tp` does not drag them:
* `spear_prop`: javelin flight, planted spear in the slam, groggy and entrance;
* `giant_spear` (scale ≈5–6, tinted red/gold/blue; m4) for the chaos fail slams.

### 6.1 Spear model coordinates (scale 2.2, 7.27 units per block, grip at y=8, tip toward +Y, blade plane XY)
| part | y (model units) | x half-width |
|---|---|---|
| tip | 31.4 | 0 |
| blade (f 0–0.36) | 31.4 → 20.0 | max 0.8 |
| barbs | 21.0 → 19.4 | 3.1 |
| ring (gem inside) | 19.1 → 15.0 | 2.2 (gem 1.3) |
| collar | 15.0 → 14.3 | 0.65 |
| crescent blades | 14.3 → 8.4 (tips at x ±3.0, y≈8.6; max out ±3.5 at y≈12) | 3.5 |
| shaft | 14.3 → 2.3 | 0.25 |
| grip | 8.0 | |
| butt star | 2.3 → −0.2 | 1.1 |
| orbit star | ≈ −1.2 | 0.45 |

### 6.2 Other model extents (units = 16/scale per block)
* **Wing, scale 2.0 (8 units/b), root at [8,8,8], authored hanging along −Y and fanning toward +X (her left):**
  - primaries card x 6→22, y 8→−11 (2.4 b);
  - secondaries x 6→18, y 8→−4;
  - coverts x 5→13, y 10→3.
* **Shield, scale 1.0:** card x −3.2→19.2, y −1.6→17.6 (1.4 x 1.2 b), centred on the pivot.
* **Skirt, scale 1.25 (12.8 units/b):**
  - front panels y 8→−10.9 (1.48 b), each 0.24 b wide;
  - outer panels flare to x ±10;
  - hip wings to x ±9.6.
* **Legs, scale 1.2 (13.3 units/b):** hip y 8 → foot bottom −13.3.

### 6.3 Textures to paint
Write a new `tools/guardian_paint.mjs`:
* reuse `weapon_paint.mjs` (`paint`, `ramp`, `fbm`, `star4`, `png`, alpha cut at 0.5, 4x supersampling);
* write to `assets/rlk/textures/guardian/<name>.png` and append to `atlases/items.json`;
* sizes are multiples of 16, with at least ~64 px per block for anything seen at melee range.

Sprites:

| sprite | size | notes |
|---|---|---|
| `gd_spear_head` | 128x512 | blade + barbs + ring frame + collar + crescent, one alpha-cut silhouette; ring hole transparent |
| `gd_spear_gem` | 64x64 | red/black 4-point star, white glint |
| `gd_spear_star` | 64x64 | butt star |
| `gd_shaft` | 16x128 | gold with fine bands |
| `gd_shield` | 256x224 | frame, star frame, spikes; the eye area painted dark, the eye overlay goes on top |
| `gd_shield_eye` | 128x128 | gem + iris + field painted in **near-white / grey luminance** so a constant item tint gives the element colour; the Geo variant tint is orange |
| `gd_wing_pri` | 256x352 | |
| `gd_wing_sec` | 192x256 | |
| `gd_wing_cov` | 128x128 | cream-gold |
| `gd_skirt_front` | 64x256 | |
| `gd_skirt_side` | 96x256 | |
| `gd_hip_wing` | 128x96 | |
| `gd_tail` | 96x320 | |
| `gd_crest` | 128x128 | |
| `gd_collar` | 128x64 | |
| `gd_halo` | 256x256 | ring + spikes + rays; cutout core |
| `gd_halo_glow` | 256x256 | translucent; follow `build_raiden_fx_textures.py` rules: alpha ≥ 0.1 writes depth, keep the halo tight, fade to 0 before the border |
| `gd_spear_glow`, `gd_spear_trail_a/b` | 128x512 | translucent, white-gold core |
| `gd_gold`, `gd_gold_trim`, `gd_gauntlet` | 32x32 / 64x64 | brushed gold; gauntlet with an amber strip |
| `gd_corrupt` | 32x32 | crimson/black voxel with glowing red cracks |
| `gd_vox`, `gd_vox_rune` | 32x32 | dark face, 1–2 px red-orange glowing edge; rune circle |
| `gd_redstar` | 64x64 | 4-point star, red |
| `gd_face` | 64x64 | diamond + eye |
| `gd_white` | 32x32 | sleeve / feather base |

Feather painter notes (adapt `skWing` from `weapon_paint.mjs`):
* each feather is a curved lanceolate shape with a white rachis line, faint barbs slanting to the tip and a
  grey-violet outline (`#6E6370`);
* shading goes from white to `#CFC3C1` on the trailing vane;
* the skirt panels get **jagged notches** along the edges (the in-game look);
* the coverts are rounded scales in cream-gold;
* the primaries have pointed tips with a slight S-bend;
* the tiers overlap, so leave alpha gaps between feathers for a feathery silhouette.

### 6.4 Rendering rules carried over from the repo
* Glows are separate displays with `brightness:{block:15,sky:15}` (as Raiden's `*_fx` and the halo). Body parts
  use 12–13.
* Vanilla model elements also accept `light_emission` (0–15) per element. Verify it in 26.3 before relying on it
  for the eye, runes and gauntlet strip inside a normally lit display; the fallback is the separate display above.
* Translucent sprites sort by quad centroid and write depth where alpha ≥ 0.1. Keep glow cards behind solid
  cards, with tight halos (see the header of `build_raiden_fx_textures.py`).
* Element recolouring uses constant item-definition tints (`tints:[{type:"minecraft:constant",value}]`, as
  Raiden's `tinted()`), so one sprite serves five elements plus chaos red.
* Display `width`/`height` 16 and `view_range` 2.5 avoid culling the 4 b spear and wing (Raiden's spawn line).
* Rig parts are teleported with the boss yaw each tick. Pitch and roll come from the poser's root rotation.
  Detached spear props must not carry the rig-part tag.

## 7. Model-linked sounds

Audio is analysed in `15_motion_sounds_spec.png` (air band > 6 kHz, peak-onset markers) and in the per-video
reports. Use vanilla compositions; the BGM masks any idle hum, and there are no audible voice lines in m1–m4.

| motion | onsets (s / f60 / tick) | character | vanilla composition |
|---|---|---|---|
| spear twirl to idle | m1 13.60, 13.74 (f816/824, t272/274.8), tail 14.72 | airy whoosh pulses, air +9.7 dB, light low thump | `item.trident.riptide_1` (p 1.4, quiet) + `entity.player.attack.sweep` (p 0.7) per half-turn |
| guard-entry baton twirl | m2 0.99, 1.415, 1.625 (f59/85/97.5, t19.8/28.3/32.5) | whooshes every ≈0.2–0.4 s, air +13.6 dB | `item.trident.riptide_1` (p 0.8) + low-pitch `entity.player.attack.sweep`, one per half-turn |
| take-off / leap (fly-slam, chaos) | m1 26.97, 27.24 (f1618/1634, t539.4/544.8) | rising whoosh burst, air +14.5 dB | `entity.ender_dragon.flap` (p 1.3) + `item.trident.riptide_3` |
| wing spread on get-up | m3 25.95 (f1557, t519) | soft mid/high whoosh, air +12.9 dB | `entity.phantom.flap` x2 (p 0.7) + `item.armor.equip_elytra` |
| glide / approach | m4 6.35–6.45, 7.35–7.5 | quiet low/mid swells | `entity.phantom.flap` (p 0.7, v 0.4) |
| spear return / catch | m1 8.55–9.16 | soft whoosh + low whoomp | `item.trident.return` (p 0.8) |
| body cubes shedding (ambient) | none audible | — | optional sparse `block.chain.place` / `block.amethyst_block.hit` (p 1.6, v 0.2) |

## 8. Default (rest) pose in rig space (b, +X = her left, −Z forward, foot bottom at y = 0)

* **root / hip:** (0, 1.78, 0). World y = floor + 0.35 hover. Bob +0.05 at t20 of a 40 t loop.
* **head:** neck (0, 2.61, 0), head pitch −5°.
* **right arm:** sh (−0.33, 2.42, 0), el (−0.45, 2.00, −0.08), wr (−0.42, 1.62, −0.32).
* **spear:** tip direction (−0.50, −0.45, −0.74) normalised (to her right-front-down). The butt crosses the
  chest toward the left shoulder. Blade plane vertical.
* **left arm:** sh (+0.33, 2.42, 0), el (+0.42, 2.00, +0.02), wr (+0.45, 1.62, −0.05), claw open and relaxed.
* **bracket:** (+0.30, 2.50, +0.08) → shield centre (+1.35, 2.65, +0.05). The shield faces forward, tilted
  −30° about Z (spike toward her head).
* **wing root:** (+0.75, 2.25, +0.15). Tiers (outward from straight down, in the frontal plane): coverts 45°,
  secondaries 32°, primaries 24°, each yawed 10° backward.
* **skirt:** panels vertical; the tail streamer hangs at (+0.22, 1.70, +0.05) with a 15° outward roll.
* **legs:** at x ±0.10, 3° apart, feet hanging relaxed.

Pose deltas for the key states:
* **Guard:** wing tiers 70° / 85° / 105°; bracket raised +15°; spear tip direction (−0.6, +0.6, −0.5).
* **Flight:** root pitch +25° forward; wing yaw +40° back; legs +30° back; skirt_front pitch +20° back.
* **Groggy A:** root lowered to the feet on the floor; torso +35°; head +30°; wing tiers 20° / 15° / 10°;
  spear prop planted at (−0.55, 0, −0.35).
* **Groggy B:** torso +45°; head +35°; bracket yaw +120° so the shield sits in front of the chest, facing forward
  and down.

## 9. Things not visible in the footage (proposed)

* **Entrance:** not in m1–m4. The PDF says she appears by planting the spear into the ground and the falling spear
  deals damage. Proposal: drop the `spear_prop` from about 8 b up onto the arena centre (point down, 3 t fall,
  Geo impact). Fade the rig in beside it over 10 t (scale 0 → 1 with gold cubes). She grabs the spear (hand to
  the shaft at f 0.74) and pulls it out (8 t), then twirls to idle.
* **Death:** see §5.
* **Pyro and Hydro record tints:** taken from the Genshin element colours; not observed.

## 10. Rejected alternatives

* **Player-skin cuboids** (Raiden's normal-form body): her parts are feathers, plates and voxels, not humanoid
  limbs, so sprite cards and voxel boxes match better. They also cost fewer elements.
* **One big static mesh per pose:** the patterns need independent wing, shield and spear motion and a detachable
  spear.
* **Full 3D feathers from boxes:** too many elements, and the silhouette is planar anyway. Use stacked alpha
  cards, the same approach as Skirk's guard wings and Navia's halberd head.

## 11. Open checks for the builder

* Confirm `light_emission` in 26.3 item models (§6.4).
* The wing primaries at scale 2.0 reach about 3 b from the root. In guard and get-up poses, check the wing tip
  height against the arena dome and the camera.
* The spear trail cards must not hide the halo glow behind them (translucent sort). Keep the trails thin.

## 12. Annotated sheets in `understand/model/`

| file | content |
|---|---|
| `01_ref_parts_annotated.png` | ref.png with every part labelled |
| `02_scale_proportions_m2_f1085.png` | landmark heights in BH and b, player comparison |
| `03_front_body_m2_f0600.png` | straight front: halo, crest, collar, arms, belt, skirt layers |
| `04_back_view_m3_f1530.png` | back: double-sided shield, wing, voxel legs |
| `05_side_back34_m3_f1300.png` | 3/4 back-side: edge-on halo, wing tiers, planted spear |
| `06_spear_detail.png` | spear fractions, crescent, ring, barbs, grip (render + 2 game frames) |
| `07_shield_detail.png` | shield structure, Electro-tinted eye, back face |
| `08_head_halo.png` | crest/face from the boss icon, blazing halo |
| `09_skirt_legs_cubes.png` | skirt layers, tail streamer, voxel legs and feet |
| `10_wing.png` | wing tiers, idle vs guard fan |
| `11_pose_reference.jpg` | 12 key poses with s/f/tick |
| `12_palette.png` | swatches with hex |
| `13_front34_m1_f1060.png` | front 3/4 at melee range: the overall read |
| `14_cubes.png` | body cubes vs FX cubes |
| `15_motion_sounds_spec.png` | spectrograms with onsets for the twirl, take-off, get-up and guard twirl |
| `ref_*_x3/x4.png` | upscaled ref crops (head/torso, wing/shield, spear, skirt) |
