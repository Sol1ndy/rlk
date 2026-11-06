# 달빛 환영 나비 (title 달빛의 화신) — modelling spec for a display-entity rig

Sources:
* `src/guide.pdf`: p.1 has the boss icon (626x626, extracted to `understand/model_work/pdf/img-000.jpg`); p.2 has the
  butterfly-form render (1011x783, `understand/model_work/pdf/img-001.jpg`) and the lore text; p.3 has the pattern list.
  400 dpi page rasters: `understand/model/guide-1.png`, `guide-2.png` and `guide-3.png`.
* v1–v4 (1920x1080, 60 fps). My own frames are in `understand/model_work/full/` (full-res PNG), crops and grids are in
  `understand/model_work/crops/`, and the scripts are in `understand/model_tools/`.
* The per-video reports `understand/v1.md`, `v2.md` and `v4.md` (v3.md was not written yet when I finished) were used
  for the replay maps, the timings and their own model notes.

Frame notation: `v2 f480` is 60 fps frame 480 of v2 = 8.000 s = tick 160 (tick = f / 3).
**R** marks a frame inside a 0.5x slow-motion replay of the guide video. Replays are fine for shape, but their
timings must be halved.
* v1: replays are 13.35–21.20 s and 31.30–38.18 s.
* v2: replays are f397–744, f1005–1356, f1629–2100 and from f2298 on.
* v4: f42–686 is a replay of real v3 32.76–38.23 s.
* v3: take the real-time ranges from v3.md (unknown to me).

Conventions (the same as the Corrupted Guardian study, `mboss/understand/model.md`):
* "her right / her left" = the boss's own sides. In a front view her right is screen-left.
* Rig space: +X = her left, +Y = up, −Z = forward. The origin is on the ground under the hip centre.
* **BH** = boss height, from the hoof sole to the helmet crown, standing, without the antennae or streamers.
  **b** = Minecraft blocks.

---------------------------------------------------------------------------------------------------

## 0. Key findings and corrections to the brief

* **The human form has NO wings, not even folded ones** (v1, v2 f0–1440, v4 f698–1878). What reads as "folded wings"
  is a set of persistent navy parts:
  - an upright **shoulder plate** with a lime spiral "eye" on each shoulder;
  - a **side-blade fan** of 4–6 long navy blades on each side, spreading out from under the collar;
  - **floating crescent plates and shards** that act as her hands.

  The real wings appear only during the transformation. They are folded for about 0.1 s behind the shoulders, flash,
  and unfold fully in ≈0.4 s (v2 24.25–24.70 s, sheet 09 row 3). At the end of the butterfly phase (달빛 해제) they
  shrink and shatter (sheet 09 row 4). In the rig the wing displays exist all the time and sit at scale 0 in human form.
* **Head (icon):**
  - a dark slate/steel-blue faceted **helmet-mask** pointing down like a beak;
  - a lime chevron "V" on the brow;
  - angular **cheek blades**;
  - **two eyes** at the sides of the beak. The brief's "red eyes" are pink-coral rings (#E3807C) with a cream-yellow
    hot core (#FFDAA8) and a violet halo (#C5BAFC). They are not pure red.
* **Naming:** the brief's "yellow-green crest blades" are the two broad lime flame-shaped **streamers**. Their tips
  turn dark olive in game. In front of them sit two thin periwinkle **antennae**. Both sway (sheets 02 and 04).
* **There is no tail.** The lower body is a pair of long **digitigrade legs** with shaggy fur boots and cream hooves.
  The lime **ribbon tendrils** belong to the butterfly form. They hang from a spiral "eye" curl at each hip and act as
  hindwing tails.
* **Arms:**
  - thin white upper arms, mostly buried in the fur;
  - the "hands" are **chains of floating navy crescent plates** with lime "C" inlays and violet tips (v1 §7.1.7,
    v2 §5.1, v4 k_f1702);
  - during kicks the big crescent locks onto the kicking shin as a blade.
* **Wings per side in butterfly form:**
  - forewing: steel spar with a curled hook tip, a lime baroque scroll frame and 2 iridescent membrane lobes;
  - hindwing: lime spiral scroll lobe and a long blade with a glowing blue tip;
  - ribbon tendril;
  - the side-blade fan, which stays from the human form.

  So "four wings" means 2 forewings and 2 hindwings.
* **Iridescence:** in game the membranes read as **pale white → mint → lime with cyan/periwinkle/violet edges** and
  lime swirl lines. The PDF render is more rainbow-holographic (cyan, teal-green, cream, pink-violet). Pyro mode
  (화염 날개, v2 f2276+, v3) recolours every membrane gold/orange/magenta. The frames keep their colour.
* **Scale:** the boss is **≈1.6x the player** (helmet crown), so BH = 2.8 b.
  - Forewing span: ≈3–4 BH in game. The PDF render draws the wings relatively smaller (≈2 BH).
  - **Recommended forewing span: 3.2 BH = 9 b** (§1).
* Gameplay note from v1's 기본 정보 caption: "불, 풀 원소 저항 70%". The user asked to **remove** the fire and grass
  resistances. This has no effect on the model.

## 1. Overall size and proposed scale

| measurement | value | source |
|---|---|---|
| boss crown / player height | 1.55 (horizon 250) – 1.65 (300) – 1.77 (350); 1.54 at v2 f180 | v2 f236 ground-plane estimate (sheet 13) |
| same, other reports | 1.46–1.70 body, 1.71–1.95 with antennae | v1.md §1 (v1 f1724, f480) |
| **BH (crown, standing)** | **≈1.6 x 1.8 b = 2.9 b → use 2.8 b** | reports used 2.6–2.7 m against a 1.7 m player; MC player is 1.8 b |
| streamer tips / antenna tips | 1.26 BH / 1.16 BH | v2 f480 (sheet 03) |
| forewing span (hook to hook) | **3.6 BH** (3.3–3.95 depending on the part BH is normalised to) in the far front view; this is an upper bound because the camera is below and the wings are cupped toward it | v4 f600 R (sheet 06) |
| forewing span, other estimates | ≈3 H in game (front); 2.3 H PDF | v2.md §5.3; PDF 1.8–2.3 BH by my normalisation |
| hindwing span (blade tip to tip) | 3.0 BH (upper bound), ≈0.8x the forewing span | v4 f600 R; PDF ratio 0.76 |
| ribbon tendrils | ≈0.6–0.9 BH long, tips 0.5–0.6 BH out from the axis, 0.05–0.27 BH above the toes | v2.md, v4.md, v4 f600 R |
| butterfly hover | toes 1.0–1.5 m above the floor; climbs to 4–6 m between attacks; swoops to 0.5–1 m | v2.md §3, v4.md §3 |
| cocoon (entrance) | 1.35 BH tall x 0.45–0.6 BH wide, spike tip 0.1–0.3 m above the floor | v1.md §1 |
| wrapped pod (달빛 해제) | ≈1.2 BH tall x 1 BH wide | v4.md 7.3 |

**Proposal: BH = 2.8 b.**
* The crown sits at 2.8 b and the streamer tips at 3.5 b, against the 1.8 b player. That is a looming 1.6x, the same
  class as the Guardian (3.0 b) and Raiden rigs, so existing arenas and cameras work.
* Butterfly form:
  - Forewing span **3.2 BH = 9.0 b**. This is the measured span minus ~12%, so the wing tips stay inside the
    third-person frame at 4–6 b.
  - Hindwing span 2.6 BH = 7.3 b.
  - Hover: toes at **+1.2 b**, so the forewing tops reach ≈6.7 b above the ground.
* Gameplay hurtbox (not visual): ≈1.0 b wide x 2.8 b tall around the body. It rises with the hover. Wings, crescents
  and tendrils are not hurtboxes.

Landmark heights, human form, standing (measured on v2 f480, sheet 03):

| landmark | BH | b |
|---|---|---|
| streamer tips (dark olive) | 1.26 | 3.52 |
| antenna tips | 1.16 | 3.25 |
| helmet crown (crown spike) | 1.00 | 2.80 |
| eyes (beak sides) | 0.90 | 2.53 |
| chin / mask point | 0.86 | 2.41 |
| shoulder line, top of the collar | 0.83 | 2.31 |
| collar bottom (front tufts) | 0.67 | 1.89 |
| waist (narrowest) | 0.57 | 1.61 |
| crotch / hip joints | 0.47 | 1.33 |
| knee, top of the fur boot | 0.32 | 0.89 |
| ankle cuff | 0.10 | 0.28 |
| hoof sole | 0 | 0 |

Widths:
* fur collar 0.60 BH (1.68 b);
* shoulder plates and side fans tip to tip 0.87 BH front, ≈1.0 BH back (2.4–2.8 b);
* waist 0.17 BH (0.47 b);
* stance (foot centres) 0.28 BH (0.79 b) idle, 0.35–0.45 BH in a combat crouch;
* helmet 0.13 BH wide x 0.14 BH tall (0.36 x 0.39 b), 0.27 BH (0.76 b) with the cheek blades;
* big crescent "hand" 0.35–0.5 BH tall (use 0.4 BH = 1.1 b), floating 0.35–0.5 BH out from the axis at shoulder height.

Butterfly form, extra landmarks (y above the foot plane, add the 1.2 b hover):
* Forewing hook tops are at crown + 0.95 BH = 1.95 BH (5.46 b).
* The forewing root is on the upper back at 0.82 BH (2.30 b), about 0.1 b behind the spine.
* The hindwing root is at 0.73 BH (2.05 b). The hindwing blade tips are at ≈0.55 BH (1.5 b).
* The ribbon roots (hip spiral eyes) are at 0.5 BH (1.40 b).
* The legs fold in flight, so the crown-to-toe distance is only ≈0.95 BH.

## 2. Silhouette

* **Human, front** (sheet 03, v2 f480):
  - a big white fur ball (the collar) on two long slender legs ending in flared fur boots;
  - a small dark helmet with a lime "V" (the streamers) and two thin rods (the antennae) rising above;
  - navy blade fans sticking out sideways at chest height;
  - a large navy crescent floating at her right shoulder.

  It reads like a white moth-yeti.
* **Human, back** (sheet 04, v4 f720):
  - the fur turns into capelets with **royal-blue tips**, forming a blue "V" down the spine;
  - 2 dark diamond plates float above each shoulder;
  - the blade fans hang down and out.
* **Human, side** (sheets 05 and 10E, v1 f664): digitigrade legs (thigh forward, hock back, standing on the hoof
  tips), the torso leaning 10–15° forward, the head low in the mane.
* **Butterfly, front** (sheet 06, v4 f600 R; sheet 01):
  - a giant X of four wings over a slim white figure;
  - the forewings rise up and out at ≈35–45° and end in curled steel hooks;
  - the hindwings are nearly level blades with blue glowing tips;
  - two lime S-ribbons hang below.

  The wings fill the screen at melee range.
* **Butterfly, side** (sheet 10 A/B/C, v2 f1508, f1980 R):
  - the wings are **flat plates** with only the steel spar rim showing thickness;
  - the roots are behind the shoulders, leaning back 20–30°;
  - the legs dangle, bent;
  - the hindwings and ribbons trail.

  Flat stacked cards are the right primitive for the wings.

## 3. Part list

### 3.1 Head — helmet, eyes, chevron, cheek blades (sheet 02)
* **Helmet-mask:**
  - 0.36 b wide, 0.39 b from the crown spike to the beak point;
  - faceted, steel/slate-blue, with a vertical centre ridge;
  - a tall **crown spike** (+0.1 b) and 4–6 short navy **crown spikes** with lavender rims around the top (v2);
  - the lower half narrows into a down-pointing **beak**.
* **Brow chevron:** a small lime "V" (#E1FAAB) in the forehead, with a second fainter V above it.
* **Cheek blades:** 2 angular dark-steel blades per side sweep out and up from beside the eyes to ±0.38 b.
* **Eyes:** two almond eyes on the beak sides at 2.53 b, about 0.11 b from the axis, facing forward-outward. Each has
  a hot cream-yellow core, a coral-red ring and a violet socket glow. They glow (brightness 15).
* **The back of the head** is covered by the fur hood. Only the crown spikes and the antennae show (v4).

### 3.2 Antennae and streamers (sheets 02, 03, 04)
* **Antennae (2):**
  - thin periwinkle rods (#83A0E3) from the brow;
  - they rise ≈0.45 b and splay outward in a V of ≈15–20°, with a slight outward curve at the tips;
  - they are stiff and vibrate only slightly.
* **Streamers (2):**
  - broad lime flame/leaf blades behind the antennae;
  - root at the back of the helmet, S-curved like a lyre, tips curling outward at 3.5 b;
  - colour goes from lime (#E6E867) to pale (#FAF98D) to a **dark olive tip** (#42523F, ≈last 25%);
  - ≈0.12 b wide.
* Motion: the streamers lag the head by 2–3 t, flutter during kicks and stream backward in jumps and flight
  (sheet 05).

### 3.3 Fur collar, mane and back capelets (sheets 03, 04)
* **Front:**
  - a huge shaggy ruff covering the neck, shoulders and chest;
  - 1.68 b wide, from the top of the head's back (2.6 b) down to 1.89 b;
  - pointed tufts hang to mid-chest;
  - cool off-white (#E2F0F3) with lilac-blue shading. It is not pure white.
* **Back:**
  - layered tufts over both shoulders become **capelets with saturated royal-blue tips** (#5671C5);
  - a blue tuft runs down the spine;
  - the cape ends in a pointed white tabard below the waist with a light-blue V (#97A7E0).
* Butterfly form: the collar is unchanged and the wing roots emerge from under the back capelets.

### 3.4 Shoulder plates and side-blade fans (sheets 03, 04, 14 #7/8)
* **Shoulder plate:** an upright navy leaf-blade on each shoulder, ≈0.55 b tall, pointing up and out, with a lime
  spiral "eye" inlay.
* **Side-blade fan:**
  - 4–6 curved navy blades per side, from under the collar at chest height (≈2.1 b);
  - they fan horizontally and downward; the lowest is ≈0.5 BH (1.4 b) long;
  - tips are pale periwinkle, with thin lime inner strokes.
* The fans stay in butterfly form, as the "middle blade fan" between the fore- and hindwings (v2 §5.3 #4).
* Motion: the fans flare up in wind-ups and kicks, sweep back in dashes, and splay and droop in groggy.

### 3.5 Arms, floating "hands" and flakes (sheets 03, 05; v4 k_f1702)
* **Arms:** slim white upper arms, 0.5 b, hidden in the fur, with navy bracers. They are almost never visible.
  **Leave them out of the rig.**
* **Her right hand:**
  - a chain of 2–3 detached navy plates: a **big crescent hook** (1.1 b, lime "C" inlay, violet tip), a mid shard
    (0.6 b, horizontal) and a small tip;
  - they float in an arc 0.35–0.5 BH out from her right side between hip and shoulder height;
  - they bob ±0.05 BH and lag her motion.
* **Her left hand:** 1–2 smaller crescent and shard pieces near the hip.
* Events (v4 k_f1702, f1716):
  - Before 달빛 점프 the plates re-form as a **vertical chain of 3–4 crescents** at her left side and glow lime.
  - In the kicks the big crescent snaps onto the kicking shin as a blade (v2 f276, f600 R).
  - In groggy the crescents are not visible (v4.md B).
* **Flakes:** 2 small dark diamond plates hover ≈0.15 BH above and ≈0.35 BH out from each shoulder (back view). They
  slowly bob and turn. Smaller flakes drift around, but those are particles.

### 3.6 Torso and hips
* A slim torso, 0.47 b at the waist, widening under the collar. Mostly hidden.
* Colouring: white-lilac with a **lavender centre stripe** (#8E9FD4) from the chest to the crotch and navy tribal
  swirls (#2F485F) on the flanks and hips.
* Small navy **hip plates** point down and out with lime swirls. 2–3 small steel fins per side are visible in the PDF
  render.

### 3.7 Legs, fur boots, hooves (sheets 03, 05, 10E)
* **Digitigrade**, long and slender:
  - hip 1.33 b;
  - knee 0.90 b, slightly forward;
  - hock 0.42 b, back;
  - hoof sole 0.
  - Segments: thigh 0.46 b, shin 0.5 b, metatarsus 0.45 b.
* **Thighs:** lilac-white with steel streaks and a navy armour strip on the outer thigh.
* **Fur boots** from the knee down:
  - shaggy, flaring to 0.4 b wide at the ankle;
  - blue-grey shading with a vivid blue inner stripe (#4B83BC);
  - white spiky tufts at the outer knee, a few lime spikes.
* **Hooves/paws:** cream (#E8DFC4), pointed, 3–4 large ivory claws splayed forward (v2).
* Flight pose: legs together (feet ±0.12 b), knees and hocks bent, toes pointed down (sheet 10 A/B).

### 3.8 Forewings (sheets 01, 07, 15)
Rooted on the upper back at (±0.18, 2.30, +0.28). Per side, at the recommended size: **4.3 b out from the root and
3.2 b up, 0.45 b below the root.**

1. **Steel leading-edge spar:**
   - from the root up and out to a **curled hook** at the outer top, the open spiral of a shepherd's crook;
   - ≈0.08 BH thick;
   - steel-blue, lit #8EA6CD, base #5C6F97, deep #273368;
   - carries an **iridescent sheen strip** (sky → pink-white → violet → indigo) along its lower edge;
   - a small green-teal glint (#33C27A / #49965A) near the hook.
2. **Membrane lobes:**
   - an **outer lobe** (large, ≈1.9 x 1.4 b, tilted 20°) and an **inner lobe** (round, ≈1.2 x 1.0 b) near the root,
     plus a third small lobe in some views;
   - **iridescent** (§4.2), with lime swirl lines across and white-mint highlights;
   - the steel rim around each lobe is 2–3 px at 64 px/b;
   - a pink-violet glowing rim along the trailing edge.
3. **Lime ornamental frame:**
   - a big baroque scroll plate filling the space between the root and the lobes;
   - embossed swirls and a **spiral "eye"** at the root;
   - lime #C7D878 with dark olive shading.

   In game the lime area dominates the wing (it reads as a lime-yellow wing with pale windows).
4. **Trailing-edge claws:** 3 short hooked steel spines between the lobes on the outer-lower edge.
5. **Inner frame claws:** 2 curved steel blades rising from behind the shoulder (PDF). They look like the human form's
   crescents docked into the wing roots.

### 3.9 Hindwings (sheets 01, 07)
* Rooted under the forewing at (±0.18, 2.05, +0.30).
* A **lime scroll lobe** with a dark navy spiral "eye" (#1B275A) runs from the root to ≈1.6 b out. It continues into a
  **long tapering blade** that reaches 3.45 b from the root and droops to ≈0.55 b below the root.
* The blade carries an iridescent strip and ends in a **hot blue glowing tip**: core #E4F0FF, glow #C1DFFA, deep blue
  #1028B6.
* Nearly level at rest. It lags the forewing in the flap.

### 3.10 Ribbon tendrils (sheets 01, 07)
* Each starts at the hip with a lime **spiral "eye" curl**, 0.35 b across, with a dark navy spiral inside.
* It continues as a flat lime **S-ribbon**, 0.12–0.2 b wide, tapering to a sharp tip.
* It curves out to ±1.5 b and down to near toe level. Length ≈2.2 b (0.8 BH).
* Colour: lime #AACF66 with a teal shade (#408970) on the underside.
* It sways with ≈0.2 s lag (4 t), ±10° at rest. It streams back in flight and spreads radially after the explosion.

### 3.11 Folded, cupped, wrapped and cocoon states (sheets 08, 09)
* **Folded (transform, ≈0.1 s):** each forewing folded up and back behind the shoulder as a compact vertical
  ≈0.4 BH panel; the hindwing curls are tucked at the hips (v2 k_f1458). Build: forewing scale 0.4, pitched up 70°,
  yawed back 60°.
* **Raised/closed up:** the forewings nearly vertical with their backs together above the head, a wind-up for slaps
  (v3 f1000).
* **Cupped:** both pairs swing 60–80° forward about vertical axes at the roots, as if hugging a ball. This is used for
  the 코코볼 orb and as the first step of 달빛 해제 (v3 f1339, v4 f340 R).
* **Wrapped pod:**
  - the forewings rotate ≈150° down and forward so their tips meet below the feet; the hindwings fold under;
  - the result is a closed pod ≈1.2 x 1 BH with navy frames outside and lime light leaking from the seams;
  - closing takes 8 t (v4 f400–450 R).
* **Cocoon (entrance, v1 f0–230):**
  - a vertical lozenge 1.35 BH (3.8 b) tall;
  - outer shell of dark slate-green wrapped plates (#374B45 / #4E6D5C) with curled hook ornaments at the upper corners;
  - lime leading edges, a glowing lime core window, and a lime crystal spike pointing down.

  Build it as a **separate prop**, because flat wing cards cannot close into this shape.

### 3.12 Pyro variant (화염 날개, v2 f2276+, v3)
* Every membrane, hindwing blade and ribbon turns gold/orange/magenta (§4.1).
* The steel and lime frames, body, fur and navy plates are unchanged.
* Build: swap the item_model of the wing cards to `*_pyro` variants.

## 4. Colour palette

`12_palette.png` holds the swatch sheet and the gradients. Hexes were sampled with k-means or point medians from the
PDF render (neutral light), the icon, and v1–v4 frames. The game frames are tinted green/teal by the cave light; prefer
the PDF/icon values for the body and the in-game values for the membranes' look.

### 4.1 Per part

| group | hexes |
|---|---|
| fur (collar, mane, boot tufts) | hi `#EEF6F8`, white `#E2F0F3`, shade `#C0CED9`, lilac shade `#A1B1D0`, deep `#8C9BAD`, line `#66738A`; icon/neutral warm white `#F2F3E7` |
| back capelets | royal blue `#5671C5`, deep `#3B54A8`, lit `#7F95D8`, tabard V `#97A7E0` |
| body skin | hi `#DFEFFA`, base `#CFD8EA`, lilac `#B9C4E3`, shade `#A0B4C7`, deep `#7D96A6`; centre stripe `#8E9FD4`; navy swirls `#2F485F` / `#3E4766` |
| fur boots + hooves | boot hi `#E2F3FB`, boot shade `#8099AA`, blue stripe `#4B83BC`, deep `#5A749F`; hoof `#E8DFC4`, hoof shade `#C8C0A6`, deep `#98A896`, claw tips `#F0E0D0` |
| helmet, cheek blades | lit `#8594AE`, base `#5A6A88`, shade `#3C4757`, deep `#252E35`, rim `#ABC4E0`, teal bounce (in game) `#286E80` |
| antennae | hi `#B8CAE4`, base `#83A0E3`, shade `#566796` |
| chevron | `#E1FAAB`, saturated `#C8E840` |
| streamers | hi `#FAF98D`, lime `#E6E867`, base `#C7D878`, shade `#96A564`, olive tip `#42523F`, tip deep `#2F3A22` |
| eyes (glow) | core `#FFF4D8`, hot `#FFDAA8`, yellow `#F8E898`, coral ring `#E3807C`, violet halo `#C5BAFC`, socket `#89A1E9` |
| navy plates (crescents, fans, flakes) | deep `#1C2A4D`, base `#394B75`, mid `#5C6B8C`, rim `#8A95C9`, violet tip `#7462B5`; lime inlay `#C8D040` / `#DBE9A1` |
| wing steel (spar, claws, rims) | hi `#ACC5E9`, lit `#8EA6CD`, base `#5C6F97`, mid `#475A80`, deep `#273368`, game shadow `#1A2A48` |
| lime frame / scrolls / hindwing lobe | hi `#E0E4A8`, game hi `#DFF1A4`, base `#C7D878`, mid `#A4BD6A`, shade `#738C3B`, deep `#455326`; spiral core navy `#1B275A` |
| ribbon tendrils | hi `#DDF392`, base `#AACF66`, mid `#95B753`, teal shade `#408970`, teal deep `#30897C` |
| hindwing blade tip | core `#E4F0FF`, glow `#C1DFFA`, sky `#86B8EA`, blue `#284AA4`, deep `#1028B6` |
| spar sheen strip | sky `#76ADDD`, pink-white `#EBC6F8`, lilac `#D5BCED`, violet `#AB99EC`, purple `#7652B6`, indigo `#3F397B` |
| Pyro membranes | peach core `#F9D0B2`, gold `#FAD77C`, orange `#F2B076`, burnt `#C96839`, pink `#C680A2`, mauve `#A35D83`, rose `#C05C6F`, violet rim `#6D5985`; v2.md adds bright `#FCE2CF` and rims `#B66753` / `#B17EA3` / `#825F89` |
| FX lime (kick arcs, transform flash, orbs) | core `#F1FCC3`, hi `#DAFB92`, base `#BEF565`, mid `#9DE85C`, shade `#83CA5D`, teal edge `#4DA5A9`; transform sphere `#F8FDBB` / `#EFFDA2` / edge `#CFF489` |
| cocoon shell (v1.md) | plates `#374B45` / `#4E6D5C`, core window `#CADE48` / `#D5F086`, spike `#BAF74A` |

### 4.2 Iridescent membrane gradients (stops, core → rim)

* **In game (what to paint on the base card):** `#F0FAE4` → `#E8F9DE` → `#DFF1A4` → `#C2EAB8` → `#A3D19B` → `#B2DDEB` →
  `#86ACE8` → `#B6C1E5` → `#D5BCED` → `#7462B5`. Measured clusters: v2 f1590 `#E6F8F2` `#C2EAB8` `#A3D19B` `#B2DDEB`;
  v4 f600 `#E8F9DE` `#D9F293`; v3 f1440 `#EAF9EE` `#D9F291` `#E1F6C2`.
* **PDF holographic (the overlay card's ramp):** `#E5E6F5` → `#B6C1E5` → `#86ACE8` → `#6BCBD5` → `#73A5A3` →
  `#6CA57E` → `#B0B786` → `#E3E0C9` → `#EBC6F8` → `#AB99EC`. Measured clusters: outer lobe `#E5E6F5` `#86ACE8`
  `#6CA57E` `#73A5A3` `#6BCBD5` `#D3DAC7`; inner lobe `#EBE6D9` `#B6BECD` `#91B253` `#DCDAB5` `#90B9A8`.
* **Hindwing blade (tip → root):** `#E4F0FF` → `#C1DFFA` → `#86B8EA` → `#284AA4` → `#1028B6` → `#A4BD6A`.
* **Pyro membrane:** `#F9D0B2` → `#FAD77C` → `#F2B076` → `#DF9258` → `#C680A2` → `#A35D83` → `#6D5985`.

**What glows** (display brightness 15, or painted bright on a brightness-14 card):
* always: the eyes, the membrane overlays, the hindwing blade tips, the spar sheen, the tendrils (lime looks emissive
  in game), the lime inlays on the plates;
* in tells: the crescent chain glows lime (v4 f1716) and the kicking hoof gets a lime glow.

## 5. Motion

Times below are real-time ticks. Replay timings are already converted.

### 5.1 Wings
* **Hover flap (idle):**
  - period ≈1.0–1.2 s (20–24 t);
  - shallow ±10–15° about the root's forward axis (v2.md, v4.md, sheet 09 row 1);
  - the forewing leads, the hindwing lags 2–3 t at 60% amplitude, the ribbons lag 4 t and swing ±10°;
  - body bob ±0.15 b, rising on the downstroke.
* **Big flap / lift** (v2 25.93–26.87 s, real time, sheet 09 row 2):
  - slow upstroke 16 t raising the forewings to a V (+60–70° from rest);
  - **snap downstroke in ≈3 t** (f1604→f1612) to ≈−10°;
  - recovery 4–6 t.

  Use it for take-offs and as a tell.
* **Active flight:** flaps every 5–8 t (0.25–0.4 s, audio peaks in v2), ±30°.
* **Glide / swoop / dive:**
  - Glide: wings held still, swept 20–40° back (yaw) and 10° above level.
  - Dive (v4 f146 R): body pitched head-down to vertical, wings swept up and back like a dart.
  - Swoop: body horizontal 0.5–1 b above the floor; one wing vertical, its edge dragging (v4 f186 R).
  - Banks: roll 30–45° in arcs, **70–90° for 우아한 날개**, where the wing edge cuts like a blade (v2 35.60–35.93 s).
* **Raised/closed** (slap wind-up), **cupped** (orb, 달빛 해제), **wrapped pod** (8 t), **snap open** (1 t),
  **flung wide** (forewings 10–15° above horizontal, hold ≈10 t, ribbons spread radially): see §3.11.
* **Transform in** (v2, real):
  - green sheath 24.10 s;
  - folded wings 24.30 s;
  - flash sphere 24.40–24.50 s (r ≈0.9 BH);
  - ripple rings 24.55–24.65 s;
  - full spread 24.70 s.

  Rig: wings scale 0 → 0.4 (folded) at t0, then **unfold in 8 t**: about 90° outward and 30° up about the root while
  the scale goes 0.4 → 1.
* **Retract (달빛 해제 end):** all wing parts scale 1 → 0.5 in ≈3 t, switch to a flat emissive lime look, then shatter
  in 2 t (v4 f654–688 R). The human form drops ≈2 b and lands.

### 5.2 Idle and locomotion
* **Human form, grounded:**
  - Idle: upright, legs 0.3–0.35 BH apart, a small sway; the crescents and flakes bob ±0.05 BH; a forward lean of
    10–15° (sheet 05).
  - Threat/hunch: leans 25° forward and the crescents flick up (v1 7.40–7.67 s).
  - **Walk/strafe:** short steps at 2–3 m/s (0.1–0.15 b/t). Digitigrade cycle: the thigh swings ±25°, the shin and
    metatarsus counter-rotate, the hoof plants on its tip. About a 20 t stride.
  - **Burst-run:** 12–16 m/s (0.6–0.8 b/t) for ≈5 t, 3 long strides, body leaning 30° forward, fans swept back,
    crescents trailing (v1 23.13–23.40 s).
  - Dash (달빛 돌진): ≈5 m in 0.1 s.
  - Backflip hop: up to ≈3 b, back 2–3 b, 1.05 s airborne.
  - Spiral jump: apex ≈0.9 BH, 1.33 s airtime.
  - Flip kick apex ≈1.3 BH.
* **Groggy (15 s, 300 t, v4):** the idle pose frozen, slight sway, no turning, crescents hidden, flakes drifting. Then a
  slow 180° turn (24 t) and the crescent chain re-forms (18 t).
* **Butterfly form, never lands:**
  - hovers with toes +1.2 b;
  - drifts in loose loops at 3–6 m/s;
  - climbs to 4–6 b between attacks;
  - always turns back to face the player within ≈0.5 s (10 t).

### 5.3 Kick poses (sheet 05)

| pose | frame | key angles (rig) |
|---|---|---|
| fighting stance | v1 f560 | knees bent 30°, stance 0.4 BH, torso fwd 10° |
| chamber | v1 f592–600 | kicking thigh pitched −100° (knee to the collar), shin folded; support leg straight |
| rising high kick | v1 f608 | kicking leg vertical (thigh −170°), body upright; big crescent locked on the shin |
| overhead flip kick | v1 f616–624 | root pitch 180–270° backflip, legs whip over, apex +1.3 BH; lime crescent wave FX |
| flying side kick | v1 f696 | root roll ≈80° (body horizontal), both legs extended toward the target |
| roundhouse sweep | v1 f704 | root yaw spin, kicking leg ≈horizontal, lime arc follows the hoof |
| low spinning sweep | v1 f1562 (v1.md) | crouch to hips 0.4 BH, one leg extended low, root yaw 360° |
| rush kick contact | v2 f262–276 | leap with one leg forward and level; fans swept back |

## 6. Articulation needed by the patterns

| pattern (PDF / caption) | key poses (source) | must move |
|---|---|---|
| idle (human) | stance, sway (v1 5.4–7.3 s, v2 f30) | root bob/sway; crest lag; crescents/flakes bob |
| locomotion (human) | walk, burst-run, backflip (v1.md §3 L, v2.md §3) | legs (hip/knee/hock), torso lean, fans sweep back |
| 달빛 발차기 / 연속 발차기 | burst-run → plant → rising flip kick → backflip → leap → crescent axe kick (v1 9.87–12.40 s) | root pitch 360° flips, both legs full range, crescent → shin lock, fans flare |
| 달빛 점프 / 발차기 점프 | crescent chain glow tell → low 360° sweep → spiral jump → overhead kick of an orb (v1 25.33–28.60, v4 26.6–31.3) | root yaw spin, crouch, crescent chain re-form (4 plates vertical), spiral jump |
| 달빛 돌진 / 돌진 발차기 | crouch, dash ≈5 m, lunge kick (v2 2.95–6.47) | root dash, leg extension, fans back |
| 광폭한 진공 / 진공참 | hop, foot glow, stomp → vacuum blade (v2 12.8–16.6) | one-leg stomp, hoof glow |
| transformation + 달빛 고치 | backflip apex → sheath → folded wings → flash → unfold (v2 23.70–24.90) | wing scale 0→0.4→1 + unfold rotation, core glow (#30), hover lift |
| 우아한 날개 / 날개 치기 | lift flap → bank 70–90° → dive-swoop → hit → climb, flutter (v2 35.20–37.92) | root roll/pitch, wings flat, big flap |
| 화염 날개의 습격, 날개 휩쓸개 | Pyro recolour; wings raised/closed → slam forward-down → flame sheet/projectiles (v2 f2276, v3) | model swap to `*_pyro`, forewing raise to vertical, slam |
| 달빛 축복 / 2단 코코볼 | cup wings around a lime orb, release, twice (v3 f1255–1405) | cup pose, core glow |
| 달빛 해제 / 강화 해제 | fly → dive → swoop → whirl (tumble 2 turns) → cup → X glint → ring cage → wrap pod 8 t → snap open → blast → flung open → retract → shatter → human drops, groggy 300 t (v4 r0.70–11.43 = v3 32.76–38.23 real) | everything above, plus root tumble (pitch/roll spins), wing pod, scale-out |
| entrance | cocoon prop on the glowing disc → whiteout 18 t → burst → boss falls 4 b → land crouch 15 t (v1.md §8) | cocoon prop, landing crouch |
| death | not in footage; proposed: wings retract and shatter as in 달빛 해제, the human body sinks to its knees, then dissolves into lime motes | wing scale-out, knee bend, per-part shrink |

Joint list (DOF):
* root: position plus full rotation (yaw, pitch, roll), for flips, banks and dives;
* torso: 3; head: 2; crest: 2 (lagged);
* fans: 2 each;
* legs: hip 3, knee 1, hock 1 (the boot carries the hoof);
* crescent chains: free 6-DOF floats, either orbiting with lag or snapped to a shin;
* flakes: free;
* forewings, hindwings: 3 each about the root;
* tendrils: upper 2, lower 2 (chained, lagged);
* core: position and scale.

Use the same poser approach as the Guardian/Raiden rigs: slerped keys, and segment orientation by aimDown for the leg
chain.

## 7. Display entities and construction plan (30)

All parts are `minecraft:item_display` with `item_display:"none"` and an `item_model` from a new `rlk:moth/*` set.
* Element coordinates stay within −16..32. Pivot = model [8,8,8]. The maximum reach from the pivot is 24 units =
  1.5 x scale blocks, which sets the minimum scales below.
* Element rotations are single-axis, in 22.5° steps within ±45°.
* Wings are authored with the root at [8,8,8], the wing plane = XY (z 7.9 / 8.1) and outward = +X. The right-side
  models are separate mirrored models; do not use a negative scale.

| # | display | content | build | scale | pivot (rig b, rest, human) | bright |
|---|---|---|---|---|---|---|
| 1 | `pelvis` | hips, crotch, navy hip plates, small steel fins | boxes + alpha plates | 1.0 | (0, 1.33, 0) | 13 |
| 2 | `torso` | waist → chest under the collar, lavender stripe, navy swirls | tapered boxes | 1.0 | (0, 1.61, 0) | 13 |
| 3 | `collar` | fur ruff (front), hood, back capelets with blue tips, tabard | core box + 10–14 jagged alpha "tuft" cards around it (front/back/sides, turned ±22.5/45°) | 1.0 | (0, 2.25, +0.02) | 14 |
| 4 | `head` | helmet-mask, beak, crown spikes, cheek blades, chevron, eye sockets | small boxes + rotated plates; cheek blades as cards | 1.0 | neck (0, 2.38, −0.04) | 13 |
| 5 | `head_glow` | 2 eyes (+ chevron) | 2 tiny plates proud of the mask | 1.0 | = head | 15 |
| 6 | `crest` | 2 antennae + 2 streamers | antennae thin boxes; streamers 2 crossed alpha cards each (S painted) | 1.0 | (0, 2.75, 0) on the head | 14 |
| 7–8 | `fan_r`, `fan_l` | shoulder plate + 4–6 side blades | blades painted on 2 crossed alpha cards + the plate as its own card | 1.0 | (∓0.42, 2.22, +0.05) on the torso | 13 |
| 9–11 | `thigh_r`, `shin_r`, `foot_r` | thigh; shin; fur boot + hoof | tapered boxes; boot = flared box + 4 tuft cards; hoof plates | 1.0 | hip (−0.14, 1.33, 0), knee (−0.20, 0.90, −0.14), hock (−0.26, 0.42, +0.10) | 13 |
| 12–14 | `thigh_l`, `shin_l`, `foot_l` | mirror | | 1.0 | +X mirror | 13 |
| 15 | `hand_r_a` | big crescent hook (1.1 b), lime C, violet tip | 3 stacked alpha cards + thin box spine | 1.0 | (−0.95, 2.05, −0.15) free | 13 |
| 16 | `hand_r_b` | mid shard + small tip | 2 alpha cards | 1.0 | (−0.75, 1.50, −0.20) free | 13 |
| 17 | `hand_l_a` | crescent (0.8 b) | as #15 | 1.0 | (+0.90, 1.75, −0.10) free | 13 |
| 18 | `hand_l_b` | small shard | card | 1.0 | (+1.05, 1.20, −0.10) free | 13 |
| 19 | `flakes` | 4 dark diamond plates (2 per side) | 4 small plates at (±0.9, 2.75), (±1.1, 2.55) in one model | 1.0 | (0, 2.65, +0.25) on the torso | 13 |
| 20–21 | `fwing_l`, `fwing_r` | forewing: spar + hook, lime scroll frame, membranes (base ramp), claws | 2 back-to-back alpha-cut planes (sheet 15 A) + a 0.5-unit steel rim strip along the spar for edge-on views | **3.0** (1 u = 0.1875 b) | root (±0.18, 2.30, +0.28) | 14 |
| 22–23 | `fwing_glow_l`, `fwing_glow_r` | holographic overlay on the lobes + the leading-edge sheen | 2 translucent planes at z 7.75 / 8.25 (0.03 b off), animated texture (§7.3) | 3.0 | = forewing | 15 |
| 24–25 | `hwing_l`, `hwing_r` | hindwing: lime scroll lobe with navy spiral, blade, blue glow tip painted | 2 back-to-back alpha planes | **2.5** | root (±0.18, 2.05, +0.30) | 14 |
| 26–27 | `tendril_up_l`, `_r` | hip spiral eye + upper ribbon (to ≈1.0 b) | 2 crossed alpha cards (S painted) | 1.0 | (±0.34, 1.40, +0.12) | 14 |
| 28–29 | `tendril_lo_l`, `_r` | lower ribbon + sharp tip (≈1.3 b) | 2 crossed alpha cards | 1.25 | the end of the upper ribbon ≈(±0.95, 0.85, +0.12) | 14 |
| 30 | `core` | chest glow (transform sheath, wrap core, blast, retract flash) | 2 crossed translucent radial cards, scale-animated 0 → 3 | 1.0–3.0 | (0, 2.1, −0.25) | 15 |

**Total: 30 displays** (the Guardian used 31).
* Wings 20–29 sit at scale 0 in human form.
* The crescents (15–18) stay in butterfly form; they dock near the wing roots as the PDF's inner frame claws
  (≈(±0.35, 2.45, +0.30), pointing up).
* If the budget gets tight: drop #5 and paint the eyes on #4 (or use per-element `light_emission`, §7.4), or merge
  #16 into #15.

Props that are not rig-tagged, so the rig `tp` does not drag them (like the Guardian's `spear_prop`):
* `cocoon` (entrance shell, 3.8 b tall, two crossed cards + a box core, with a translucent core window);
* `pod` (optional explicit wrapped-pod shell for 달빛 해제, if the 4 wing cards do not close convincingly);
* `sphere` / `ring_cage` / kick-wave cards: these belong to the pattern FX.

### 7.1 Model extents (units; 1 u = scale/16 b)
* **Forewing, scale 3.0:**
  - root [8,8,8];
  - hook top at x 31.0, y 25.0 (4.3 b out, 3.2 b up);
  - lowest point y 5.6 (−0.45 b);
  - outer lobe centre ≈(23.2, 18.4), inner lobe centre ≈(18.4, 10.7);
  - spar thickness ≈1.2 u.
* **Hindwing, scale 2.5:** root [8,8,8], scroll lobe to x 18, blade tip at (30.1, 4.5); thickness of the blade 1.5–2.5 u.
* **Tendrils:**
  - upper, scale 1.0: spiral eye centred (8,8) r 2.8 u, ribbon to (17.6, −1.6);
  - lower, scale 1.25: from (8,8) to (14, −10) with an S bend.
* **Collar, scale 1.0:** ±13.4 u wide, y −5.8 (front tufts) to +5.6, z ±7.
* **Fans, scale 1.0:** the longest blade reaches 22 u from the pivot.
* **Crest, scale 1.0:** streamer tips at y +12.3 u, x ±6.4 u.
* **Legs, scale 1.0:** thigh 7.4 u, shin 8 u, foot 7.2 u + hoof 1.5 u.

### 7.2 Textures to paint (new `tools/moth_paint.mjs`, reusing the `weapon_paint.mjs` / `guardian_paint_lib.mjs` helpers)

Common settings:
* 4x supersampling, alpha cut at 0.5 for cutout sprites;
* ≥ 56–64 px per block for anything seen at melee range;
* register the textures in `atlases/items.json` (as for the Guardian).

| sprite | size | notes |
|---|---|---|
| `mb_fwing` (+ `_pyro`, `_flat`) | 256x224 | sheet 15 A: steel spar with highlight band, lime scroll plate with embossed swirls + root spiral eye, 2 lobes painted with the in-game ramp + lime swirl lines + white-mint highlights, 2–3 px steel lobe rims, 3 trailing claws, hook spiral; trace the outline from sheet 07 |
| `mb_fwing_glow` (+ `_pyro`) | 256x224 per frame, 16 frames | translucent; PDF holographic ramp sampled along a skewed coordinate + sin warp, masked to the lobes (alpha 0.30–0.55, higher toward the rim) and the leading-edge band (0.55); keep alpha ≥ 0.1 only where wanted (depth write) and fade to 0 before the border |
| `mb_hwing` (+ `_pyro`, `_flat`) | 256x96 | lime scroll lobe + navy spiral, blade with iridescent strip, blue glow tip (radial `#E4F0FF` → `#1028B6`) |
| `mb_tendril_up`, `mb_tendril_lo` (+ variants) | 64x96, 64x128 | lime ribbon, teal underside, spiral eye with navy core |
| `mb_collar_tuft` x3 variants | 128x96 | jagged fur tufts, cool white with lilac-blue tips; back variant with royal-blue tips |
| `mb_fur` | 64x64 tile | fur noise for the boxes |
| `mb_helmet`, `mb_cheek`, `mb_crown` | 64x64, 32x32, 32x32 | faceted slate with rim light; crown spikes navy with lavender rims |
| `mb_eye` | 16x16 | cream core, coral ring, violet halo |
| `mb_streamer`, `mb_antenna` | 64x160, 16x64 | streamer lime → olive tip; antenna periwinkle |
| `mb_fan_blade`, `mb_shoulder_plate` | 128x64, 32x64 | navy with lime inner strokes, pale periwinkle tips |
| `mb_crescent`, `mb_shard`, `mb_diamond` (+ `_glow` tell variants) | 64x128, 64x32, 16x32 | navy, lime "C" inlay, violet tip |
| `mb_skin` | 32x32 | lilac-white, lavender stripe, navy swirl |
| `mb_boot` | 64x64 | fur with blue stripe, white spiky tufts |
| `mb_hoof` | 16x16 | cream + claw lines |
| `mb_core` | 64x64 | translucent radial lime-white glow |

### 7.3 Selling the iridescent wings
1. **Paint, do not tint, the base.** The ramp is multi-hue (lime → mint → cyan → periwinkle → violet), so a constant
   multiply tint cannot produce it. The base card (`fwing_*`) is a cutout with the in-game ramp, lime swirl lines and
   white highlights. Brightness 14 makes it read luminous without being flat.
2. **Holographic overlay card** (`fwing_glow_*`):
   - a translucent copy of the lobe area 0.03 b in front of **and** behind the base;
   - the base writes depth, so only the camera-side overlay is visible;
   - brightness 15;
   - painted with the PDF holographic ramp.
3. **Animate the shimmer at zero command cost:**
   - give the overlay texture an `.mcmeta` animation: 16 frames, `frametime` 3, `"interpolate": true`;
   - each frame shifts the hue phase by 1/16 along a skewed, sine-warped coordinate;
   - the colours then flow across the lobes like oil on a soap film (sheet 15 C/D).

   **Verify in 26.3 that animated sprites work in the items atlas.** If they do not, swap the overlay's `item_model`
   between 4 phase variants every 3–4 t from the rig tick. That costs one `data modify` per wing per swap.
4. **View dependence:** paint the overlay's front and back faces with phases 0.5 apart. Optionally step the phase with
   the flap angle, swapping the variant at the top and bottom of the stroke. The colour then changes as the wing turns,
   which is what iridescence does.
5. **Rim and sheen:** the spar's pink-violet sheen strip and the trailing-edge rim are the brightest overlay pixels
   (alpha 0.55). The hindwing blade tip is painted hot blue on a brightness-14 card. If it needs more, use a tiny extra
   glow plate inside the `hwing` model with per-element `light_emission` 15 (§7.4).
6. **Optional:** `enchantment_glint_override:true` on the overlay item gives a moving violet sheen. Check that the
   glint respects the alpha (it should depth-test against the base); drop it if it paints the transparent areas.
7. **Pyro mode:** swap both cards to `*_pyro`. **Transform-in and retract:** swap to `*_flat` (solid lime, brightness 15)
   and animate the scale. Lime wind particles (dust `#BEF565`, sparse) can trail from the wing tips in fast flight.

### 7.4 Rendering rules carried over from the repo
* Glow parts are separate displays with `brightness:{block:15,sky:15}`. Body parts use 13, fur and lime parts 14.
* Per-element `light_emission` (0–15) in item models: verify in 26.3 before relying on it (the same caveat as the
  Guardian study).
* Translucent sprites sort by quad centroid and write depth where alpha ≥ 0.1. Keep overlays tight to the base card and
  fade their alpha to 0 at the sprite border (`build_raiden_fx_textures.py` rules).
* Display `width`/`height` 16 and `view_range` 2.5 so the 9 b wings are not culled.
* Interpolation (`interpolation_duration` 2–3, `teleport_duration` 1–2) smooths the flap. The snap downstroke needs
  `interpolation_duration` ≤ 2.

## 8. Rest poses (rig b, +X her left, −Z forward)

* **Human idle:**
  - root on the ground;
  - legs: hip (±0.14, 1.33, 0) → knee (±0.20, 0.90, −0.14) → hock (±0.26, 0.42, +0.10) → hoof (±0.33, 0, −0.06);
  - torso pitch −10° (forward);
  - head level, crest upright;
  - fans: blades fanned 8°/20°/32°/44° below horizontal;
  - crescents and flakes at their pivots (§7), bob ±0.14 b over a 40 t loop with phase offsets;
  - wings scale 0.
* **Butterfly hover:**
  - root +1.2 b;
  - legs: hips together (±0.12), thigh pitched −15°, knee bent 30°, hock 40°, hoof pointing down;
  - torso upright;
  - forewing roll +35° (up and out from horizontal in the frontal plane), yaw −10° (cupped slightly forward);
  - hindwing roll −5°, yaw −5°;
  - upper tendril pitch 0, lower tendril hanging (pitch +10° back);
  - fans 15° lower than in human form;
  - crescents docked at the wing roots.
* **Pose deltas:**
  - Flap up: forewing roll +50°, hindwing +40°. Flap down: forewing +20°, hindwing −15°.
  - Big-flap V: forewing roll +75–80°.
  - Raised/closed: forewing roll +85° with the backs together.
  - Glide: root pitch −30–60°, forewing yaw +30° back, legs trailing (+30° pitch back).
  - Wing strike: root roll ±80°.
  - Cupped: forewing and hindwing yaw −70° (forward about a vertical axis).
  - Wrapped pod: forewing pitch about the lateral axis −150° (down and forward), hindwing −120°, tendrils curled in.
  - Flung open: forewing roll +12°, hindwing −10°, tendrils roll ±60° out.
  - Folded (transform t0): forewing scale 0.4, roll +70°, yaw +60° back.
  - Groggy: human idle, torso −5°, fans drooped 15°, crescents hidden.

## 9. Not visible in the footage (proposed)

* **Death:** proposed as above (§6).
* **Butterfly back view:** only v4 f2314 (next clip, 3/4 back). The upper wing surface repeats the front pattern, so
  the cards are double-sided with the same texture. The back shows the blue capelets.
* **Human-form arms:** never clearly visible, so they are left out (§3.5).

## 10. Rejected alternatives

* **Membranes as stained-glass blocks or block_displays:** these give no gradient and no curved silhouette, and they
  cost many entities.
* **One flat card per wing with a constant colour tint:** this cannot produce the multi-hue ramp, and it looks like
  paper.
* **Many-segment forewings (2–3 per wing):** the flap is a root rotation in all the footage and the frame is rigid. The
  budget is better spent on the overlay cards and the 2-segment ribbons.
* **Player-skin cuboids for the body:** the silhouette is fur and blades, not a humanoid skin.

## 11. Open checks for the builder

* Confirm animated item-atlas sprites with interpolation, and per-element `light_emission`, in 26.3 (§7.3, §7.4).
* At BH 2.8 b and span 9 b, check the forewing hook tops (6.7 b up while hovering, more in the V pose) against the arena
  ceiling and the camera at 4–6 b.
* The overlay cards must stay on the camera side of the base card through the whole flap. Test the edge-on angles.
* v3.md (not available to me) holds the real-time map for the Pyro and 코코볼 frames referenced here (v3 f730–1000,
  f1255–1405).

## 12. Annotated sheets in `understand/model/`

| file | content |
|---|---|
| `01_ref_parts_annotated.png` | PDF butterfly render with every part labelled |
| `02_head_icon_and_game.png` | icon head (helmet, eyes, chevron, antennae, streamers) + in-game head and shoulders (v1 f1440) |
| `03_human_front_v2_f0480.png` | human front: landmark heights in BH and b, widths, parts |
| `04_human_back_v4_f0720.png` | human back: capelets with blue tips, flakes, fans, streamers |
| `05_human_kick_poses.png` | 12 stance and kick poses (v1, v2) with s/f/tick |
| `06_butterfly_front_proportions_v4_f0600.png` | butterfly front: spans, wing heights, rig recommendation |
| `07_wing_anatomy.png` | forewing/hindwing/tendril layers (PDF, her left side) |
| `08_wing_states.png` | 12 wing states: spread, up/down stroke, raised, side, glide, ball, cocoon, release wrap, transform, Pyro, human |
| `09_wing_motion_strips.png` | strips: idle flap, big flap with snap, transform in, 달빛 해제, wing slap |
| `10_side_and_34_views.png` | side and 3/4 views of both forms |
| `11_best_reference_frames.jpg` | 16 best frames: front/back/side human, kicks, butterfly front/side, wings raised/wrapped, cocoon, PDF |
| `12_palette.png` | swatches per part + membrane / hindwing / Pyro / sheen gradients + membrane recipe mock |
| `13_scale_vs_player_v2_f0236.png` | ground-plane scale estimate vs the player and the MC numbers |
| `14_rig_breakdown.png` | the 30-display rig in front elevation, both forms, on a 1-block grid with the player |
| `15_wing_texture_target.png` | forewing texture target: base card, overlay, two shimmer phases, Pyro, flat-lime variant |
| `guide-1.png`, `guide-2.png`, `guide-3.png` | 400 dpi page rasters of the PDF |

### 12.1 Best reference frames (detail)

| view | frames (R = 0.5x replay) |
|---|---|
| human front | **v2 f480** (8.00 s), v2 f30 (v2.md k_f0030), v1 f504 (v1.md zoom), v1 f1724 |
| human front 3/4, head | **v1 f1440** (24.0 s), v2 f600 R (very close, kick) |
| human back | **v4 f720** (12.00 s, real), v4 f702, v4 f1420 |
| human side / stance | v1 f664 (11.07 s), v1 f560 |
| kicks | v1 f600 (chamber), f608 (high kick), f616–624 (flip), f696 (flying side), f704 (roundhouse), v1 f1562 (low sweep, v1.md), v2 f262–276 (rush) |
| crescent chain | v4 f1702–1716 (real), v2 f30 |
| butterfly front, wings spread | **v4 f600 R** (far), v2 f1584–1596 (real), v2 f2040–2088 R (near, detail), PDF p.2 |
| butterfly side | **v2 f1508** (real), v2 f1980 R, v2 f1548 (v2.md full-res side + scale) |
| wings raised / folded | v2 f1604 (V, real), v3 f1000 (closed up), v2 f1458 (folded, transform), v3 f1339 (wrapped ball), v4 f400–450 R (pod), v1 f120 (cocoon) |
| Pyro wings | v3 f900, v3 f250, v2 f2282 |
| scale vs player | v2 f236, v2 f180, v1 f1724 (v1.md) |
