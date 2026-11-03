# 야타용왕 (Azhdaha, 봉인된 바위 용의 왕): model anatomy study for a display-entity rig

Chapter-1 boss. This file is the modelling reference: the part list, measured proportions, palette and glow states, and
which details are geometry or paint at Minecraft resolution. Motion lives in `motion.md`, rig technology in `rigtech.md`,
and the patterns in `mechanics.md` and `v*.md`. Where those files give model numbers, this file is the owner (`motion.md`
§2.2 says so). §9 lists the conflicts.

Sources:
* `src/wiki.md`: the binding requirements and the text description of the official portrait. The portrait image itself
  is not on disk.
* `src/v1..v9.mp4`: 1920x1080, 60 fps, the 패턴분석 part of the HGOO guide. **The clips cover all four elements**: Hydro
  phase 2 (v4), Pyro phase 2 (v5, v8, v9), Electro phase 3 (v6, v7) and Cryo phase 3 (v7 end, v8, v9). Every colour
  state the model needs is in the footage.
* My own frames are full-res JPEGs in `understand/model_work/full/` (`v<N>_f<frame>.jpg`, 60 fps frame numbers).
  - Gridded and annotated reads are in `model_work/look/` (`t_*`, `g_*` = 10/20/25/50 px grids in full-frame coordinates).
  - The hand traces are in `model_work/trace/*.json`.
  - The palette evidence is in `model_work/palette.json` (k-means per region) and `model_work/palette_rec.json` (the
    recommended ramps with their evidence).
  - The running notes are in `model_work/notes.md`.
  - The scripts are in `understand/model_tools/`: `rng.py` (range decode), `sheet.py`, `grid.py`, `gridov.py`,
    `annot.py`, `palette.py`, `glowpick.py`, `segment.py`, `figlib.py` and `fig*.py`.
* Cross-checked against the analyst reports `v1.md`, `v2.md`, `v5.md`, `v7.md` and `v8.md`, and against `motion.md`,
  `rigtech.md`, `chapter.md` and `mechanics.md` (all in `understand/`).
* Templates: `mb3/understand/model.md` (fieldgen) and `mb2/understand/model.md` (butterfly).

Frame notation: `v8 f2280` is 60 fps frame 2280 of v8 (38.0 s, tick 760). Pixel coordinates are full-frame 1920x1080.

Conventions (as in the earlier studies and `motion.md`):
* **Rig space**: +X = the boss's left, +Y = up, −Z = forward, units in blocks (b). "Her/his left" is the boss's own side.
* **H** = height of the tallest dorsal-plate tip in the standing idle. This is the master dimension; every size is given
  in H first.
  - In game H ≈ **9 m**: v1.md 9.5, v7.md 8.3 and v8.md 9.0 (v2.md's 5.4 m is rejected, §1.1).
  - **Recommended H = 7.0 b** (§1.3).
* **L** = body length, rump to snout (horn front), without the tail.

---------------------------------------------------------------------------------------------------

## 0. Key findings and corrections to the brief

* **The eyes are glowing RED, not amber.** Narrow slit eyes sit deep under the brow, angled down toward the snout. The
  hot core is `#FFE0E0`/`#FF8A8E`, the body `#F04352`/`#C81A2C`. The portrait text says amber `#FFB000`; every combat
  frame shows red (v2 f0750, v4 f2160, v3 f2280; v5.md §4.1 agrees).
* **The "gold-amber crystalline horn crown" is two big composite horns, one per side.** It is not a crown of many horns.
  Each horn has three parts:
  - a thick **gold sleeve** (the lower two thirds), rooted at the jaw corner. It ends in a rounded **gold knob** that
    points forward-down beside the mouth.
  - an **orange-brown meander inlay** engraved on the sleeve.
  - a **dark brown, almost black horn** (the upper third) that grows out of the top of the sleeve.
  - Seen from the side, the whole horn is a **C-crescent that opens forward**: the knob at the bottom front, the arc
    swinging back past the eye, the dark tip curling forward and slightly inward above the brow.
  - Seen from the front, the two horns frame the face like brackets "( )".
  - Behind each sleeve sits a small gold **square-meander "ear" plate (回)** on a dark mount.
  - Best frames: v4 f2160, v3 f2280, v1 f2370, v2 f0420 (`02_head.jpg`, `01_part_map.jpg` D).
  - The gold reads **opaque and saturated** in game (lit `#E6A93A`/`#C98625`). It is not glassy, so paint it as polished
    stone-gold with a bright rim, not as a translucent crystal.
* **The face is a dark rocky mask, not a lion muzzle.** It is dark brown and faceted, with short radiating spikes around
  the brow and a grey-brown **keel blade** running up the forehead between the eyes.
  - Below it is a cream **beak / chin shield** with a serrated upper edge. That edge is the closed mouth line with the
    teeth.
  - Open, the mouth shows rows of blocky white teeth, pink-red gums and a cream lower jaw (v2 f0840, v4 f1620).
* **The "white-cream beard / mane" is a layered stone beard that becomes a huge chest APRON.**
  - Two or three triangular cream plates hang under the jaw.
  - They continue into one big draped cream stone panel between the fore legs. Its foot is only 0.06 H (0.4 b) above
    the floor.
  - It is engraved with a large line glyph (vertical zigzag and meander lines) and has round pebble bumps along its lower
    edge (v2 f0600, v3 f2100, v3 f2070).
  - This apron is the "chest" that glows in phase 2.
* **The leafy "tree on the back" is the TAIL TIP; there is no separate tree.**
  - The distal ~40 % of the tail is a dark **branch** carrying leaf clusters: orange-gold in phases 1–2, white-cyan
    crystal blossoms under Cryo, violet blossoms under Electro.
  - The tail is usually carried in a high arc over the back, so in front views the branch looks like a tree growing out
    of the back (v1.md f2060 "tree on the back", `motion.md` bones `tree1/tree2`).
  - The tail laid along the ground proves it: v3 f1680, v3 f1230, v8 f1320 (`model_work/look/tree_check.jpg`).
  - **Drop the `tree1/tree2` bones; the tail-tip parts carry the leaves.**
* **The tail is very long.** Measured along its curl it is 1.5–1.7 L in three frames (v7 f0600, v8 f2280; v7.md
  1.6–1.7 L; v8.md 1.3 L). The underside is a broad **cream ventral fin with gold veins**: a central line plus nested
  upward chevrons, like a leaf. It is 0.44 H wide at the root (v3 f1500, v3 f1560, v7 f1200). The top carries a row of
  dark blade spikes that shrink toward the tip.
* **The back is two systems interleaved.**
  - **Dark umber blade plates**, like obsidian feathers, fan up and back in about 3 rows a side plus a central row. The
    tallest are over the shoulders (1.0 H) and over mid-back (0.98 H), falling to 0.6 H at the hips. Some plates have
    orange-amber bases. A **ruff of smaller plates** radiates back from the neck behind the head.
  - **Gold crystal shards** sit between and below the plates, about 5 a side. Each is a 3-pronged "trident / bird" cluster.
    A bigger spike crowns each shoulder.
  - The plates **bristle** (+15 %, fan out to about 1.0 H wide) in the absorbs and the spike launch (v4 f0900, v1.md f2202).
* **Legs.**
  - Fore: a columnar **red-brown stone bracer** (gauntlet) from the wrist to above the elbow, carved with zigzag and
    meander lines and set with small gold studs. **3–4 amber-orange hexagonal crystal prisms** jut back from the elbow.
    The paw has **4 big black talons + 1 dew claw** over pale toe pads.
  - Hind: a grey-cream lower leg with **horizontal ribbed rings** (stacked stone bands), an **orange crystal spur** on
    the heel, and 3–4 talons. Dark plates and gold crystal clusters sit on the hips.
* **Element recolours (binding: two elements on entry).**
  - **Phase 2 recolours the 4 legs + the chest apron (+ the belly crack lines).** The carved lines glow in the leg
    element and the bracer/gaiter stone darkens to the element's base.
    - Hydro: navy-black stone with white-cyan lines.
    - Pyro: deep red stone with orange lines.
  - **Phase 3 recolours the back plates + the tail.**
    - Plate edges glow: Cryo white-cyan, Electro violet.
    - The tail-tip leaves are replaced by the element's blossoms: Cryo white-cyan crystals, Electro violet blossoms.
  - The tail leaves **stay orange-gold through phase 2** (v4 f0900).
  - The eyes are red in every phase. The gold horns and crystals keep their gold.
* **Scale.** The analysts agree within ±10 % once v2.md's heights are discounted.
  - In game: H ≈ 9 m, L ≈ 13 m, tail ≈ 17–22 m along the curl, front claw span ≈ 10.4 m, horn span ≈ 5.7 m.
  - **Recommended H = 7.0 b.** This gives L 10.2 b, tail 14.5 b, claw span 8.1 b, horn span 4.4 b and eyes 1.5 b
    (head low).
  - It suits the 28-b walk radius proposed in `chapter.md`, and it matches `rigtech.md` (crest 7–7.5 b) and v5.md (≥ 7 b
    to read as huge). §1.3 gives the alternatives.

## 1. Overall size and proposed scale

### 1.1 Absolute size: what each study measured

| study | method | H (plate tips) | other anchors |
|---|---|---|---|
| v1.md | Barbara 1.55 m + two floor rings (pinhole, 45° FOV), f2310/f2202/f2060 | **9.5 m** (9–10.5) | front claw span 11.0, head width 5.5, eye height 2.0 (head low), 4.1 (raised) |
| v7.md | Barbara/Kaeya + ground-row scaling on three frames | **8.3 m** (6.7–10.9) | claw span 9.5–10, eyes 1.9, head length 2.9, body 10.5, tail ≈ 17 along the curl |
| v8.md | Kaeya/Barbara rulers on four frames | **9.0 m** (7.5–11) | body 13, tail 17 (±30 %), head width 5.5, foot 2.0–2.5 |
| v2.md | ground-circle calibration | 5.4 m (**rejected**) | its widths agree with the others (claw span 9.7–10.3, horn span 6.1–6.25, eye spacing 1.05), but its heights would make the claw span 1.85 H, against 1.08–1.17 H everywhere else. It probably measured a crouched frame (v3 f0705 is in the charge coil). |
| **this study** | ratios only (5 broadside frames, 3 traced views, 2 front frames), scaled with the consensus H | **≈ 9 m** | — |

### 1.2 Measured proportions (H units; metres at H = 9 m; blocks at the recommended H = 7.0 b)

Heights (standing idle, head low unless noted). Sources: my frames plus the analysts. The side scan of v8 f2280 is in
`model_work/notes.md`.

| landmark | H | m | b | evidence |
|---|---|---|---|---|
| tallest dorsal-plate tip (over the shoulders) | **1.00** | 9.0 | **7.0** | v8 f2280 scan (tip at 1150,258; floor 560); v1/v7/v8 |
| plates bristled (absorb, spike launch) | 1.15 | 10.4 | 8.05 | v1.md f2202 (11 vs 9.5 m) |
| mid-back plates / hip plates | 0.92–0.98 / 0.60–0.75 | | 6.6 / 4.2–5.25 | v8 f2280 scan |
| neck ruff plates (behind the head) | 0.60–0.73 | | 4.2–5.1 | v8 f2280 scan |
| shoulder crystal tips | 0.67 | 6.0 | 4.7 | v1.md 6.4/9.5 |
| shoulder hump (hide top over the fore legs) | **0.61** | 5.5 | **4.3** | v8 f2280 0.60–0.64; v7.md 0.66; v8.md 0.51–0.74 |
| hip top / rump top | 0.52 / 0.45 | | 3.6 / 3.15 | v8 f2280, v7 f0600 |
| tail root (centre) | 0.40 | 3.6 | 2.8 | v8 f2280, v7 f0600 |
| belly underside, mid-body | **0.20** (0.17–0.29) | 1.8 | **1.4** | v8 f2280 0.18; v7.md 0.23; v8.md 0.29 standing tall; 0.07 crouched (v3 f1170) |
| apron (chest) foot | 0.06 | 0.5 | 0.4 | v1 f2130 |
| eye, head low | **0.21** (0.16–0.23) | 1.9 | **1.5** | v1.md 2.0/9.5; v7.md 1.9/8.3; v8.md 1.4/9 (roar crouch) |
| eye, head raised (walk, roar) | 0.43 | 3.9 | 3.0 | v1.md 4.1 (f2202); my v1 f2130 3.85 m |
| brow/crest top, head low | 0.38 (0.35–0.45) | 3.4 | 2.65 | v1.md 3.3; v2.md 4.0; v8.md 3.7 |
| horn tips, head low | 0.55 | 5.0 | 3.85 | v8 f2280; v2.md ≥ 5.0 |
| snout tip / chin, head low | 0.12 / 0.02 | 1.1 / 0.2 | 0.85 / 0.15 | v1.md chin 0.2 m (f2310) |
| fore bracer (gauntlet) | 0.06 → 0.32 | 0.5 → 2.9 | 0.4 → 2.25 | v1 f2130 (top at the elbow crystals); v2.md bracer top 2.3 m |
| elbow crystals | 0.33 → 0.45 | | 2.3 → 3.15 | v1 f2130, v3 f0720 |
| hind gaiter (ribbed) / heel spur | 0.05 → 0.22 / 0.20 | | 0.35 → 1.55 / 1.4 | v3 f1560 |

Lengths (side view):

| item | ratio | m | b | evidence |
|---|---|---|---|---|
| **L, rump → snout (horn front)** | **1.46 H** (1.40–1.78; median of 5 frames 1.47) | 13.1 | **10.2** | v8 f2280 1.46 (scan H), v7 f0600 1.47, v3 f1320 1.51, v3 f1170 1.45 (crouch), v7 f0540 1.78 (walking, head forward); v7.md 1.32, v8.md 1.44 |
| wheelbase (front ↔ hind foot centres) | 0.72 H (0.60–0.75) | 6.5 | 5.0 | v8 f2280 0.75, v7 f0540 0.63; v8.md 0.73, v7.md 0.60, v1.md ≈ 0.74 |
| snout ahead of the front feet | 0.36 H | 3.2 | 2.5 | v8 f2280 |
| rump behind the hind feet | 0.38 H | 3.4 | 2.7 | v8 f2280 |
| head length, snout → back of the crest | 0.32 H | 2.9 | 2.25 | v7.md 2.9 m; v7 f0540 0.35 incl. horns |
| neck, occiput → shoulder front | ≈ 0.25 H | 2.3 | 1.75 | estimate (the neck is short, thick and sloping down) |
| **tail, along the centreline** | **1.5–1.7 L** (2.2–2.5 H) | 20–22 | **14.5 recommended** (= 1.42 L) | v8 f2280 1.68 L, v7 f0600 1.54 L, v8 f1320 ≥ 1.23 L (cut by the frame); v7.md 1.6–1.7 L; v8.md 1.3 L |
| tail thickness at the root: core / with top spikes + fin | 0.20 / 0.29 H | 1.8 / 2.6 | 1.4 / 2.0 | v8 f2280 (91 px of H 302 with spikes) |
| tail thickness, mid / distal (with spikes) | 0.22 / 0.09 H | | 1.55 / 0.65 | v8 f2280 |
| leafy branch | the last ≈ 40 % of the tail | | ≈ 5.8 | v3 f1680, v8 f2280, v7 f0600 |

Widths (front, rear, top):

| item | ratio | m | b | evidence |
|---|---|---|---|---|
| **front claw span (outer edges)** | **1.16 H** (1.08–1.17) | 10.4 | **8.1** | v1 f2130 (665 px); v1.md 11.0/9.5; v7.md 9.5–10/8.3; v8.md 9.75/9 |
| one fore paw incl. claws | 0.25 H | 2.3 | 1.75 | v1.md 2.4; v2.md 2.1–2.3; v7.md 2.3 |
| fore bracer width | 0.21 H | 1.9 | 1.5 | v1 f2130 110 px; v1.md 2.15 |
| shoulder span incl. the shoulder crystals | 1.05 H | 9.4–9.8 | 7.35 | v1.md 9.4; v8.md 9.8 |
| torso, widest (mid-belly) | ≈ 0.85 H | 7.7 | 6.0 | estimate from the front and rear widths |
| hind span (outer edges) | ≈ 0.95 H | 8.6 | 6.65 | v3 f1560, scaled by assumption; hind feet 0.23 of it |
| hind foot | 0.22 H | 2.0 | 1.55 | v3 f1560 |
| **tail root (ventral fin seen from behind)** | **0.44 H** | 4.0 | **3.1** | v3 f1560 (280 of 608 px) |
| **gold horn sleeves, outer span** | **0.63 H** (0.58–0.69) | 5.7 | **4.4** | v1 f2130 363/665 px; v1.md 5.5; v2.md 6.1–6.25; v8.md 5.5 |
| cheek guards / helmet width | 0.42 H | 3.5–4.1 | 2.95 | v7.md 3.5; v2.md 4.1 |
| face (dark mask) width at the eyes | 0.22 H | 2.0 | 1.55 | v4 f2160 (1.9 eye spacings); v2.md 2.1 |
| eye spacing (centres) | 0.115 H | 1.05 | 0.8 | v2.md 1.05; v1.md 1.0; v1 f2130 68 px |
| chest apron width | 0.28 H | 2.5 | 2.0 | v1 f2130 |
| plate fan width: idle / bristled | 0.75 / 1.0 H | | 5.25 / 7.0 | v4 f0900 (fan 1.7 × the sleeve span), v1.md f2202 |

The figures:
* `model/04_silhouettes_traced.jpg`: the three traced outlines and the same outlines normalised to H.
* `model/05_proportions_blocks.png`: side, front and top elevations of the recommended block-out at H = 7.0 b on a 1-b
  grid, with the 1.8-b player.

### 1.3 Scale decision

| option | H | L | tail (curl) | claw span | eye (head low) | crest (head low) | player : H | arena |
|---|---|---|---|---|---|---|---|---|
| compact | 6.0 b | 8.8 | 12.4 | 7.0 | 1.3 (player's chest) | 2.3 | 0.30 | fits r 22–24 |
| **recommended** | **7.0 b** | **10.2** | **14.5** | **8.1** | **1.5** (just under the player's eyes) | **2.65** | **0.26** | **r 28 (`chapter.md` az_cavern)** |
| "true feel" | 8.0 b | 11.7 | 16.6 | 9.3 | 1.7 (eye to eye) | 3.0 | 0.23 | needs r ≥ 32 |
| Genshin | 9 m | 13 m | 20–22 m | 10.4 m | 1.9 m (over Barbara's head) | 3.4 m | 0.17–0.18 | — |

**Use H = 7.0 b.**
* The player still stands under the chin between the fore paws (gap 4.6 b), as in every frontal shot (v2.md).
* The head is in melee reach (snout 0.85 b, crest 2.65 b), as the wiki asks ("attack the head and the tail").
* The tail sweeps reach about 20 b from the body centre: the whole of an r 28 floor, which is what makes 교활한 통수 the
  worst pattern.
* `motion.md` used plate tips 7.5–7.8 b. At 7.0 b its joint heights scale by 0.91 (§9).

Hit volume (not visual): follow `rigtech.md` §3.3, with about 11 ground-level interaction proxies on the spine, legs and
tail. The head proxy sits at the eye height of the current pose.

## 2. Silhouette

* **Side** (`04` bottom left, v8 f2280, v7 f0600, v3 f1170): a low, massive, barrel-bodied quadruped.
  - The head is carried **below the back line** with the chin near the floor. The neck slopes down and forward from a
    high shoulder hump.
  - A long saw-tooth crest of dark plates runs from the neck (0.6–0.73 H) to the shoulders (1.0 H), stays high over
    mid-back (0.92–0.98 H) and falls to the hips (0.6–0.75 H). Gold trident shards poke out along its lower edge.
  - The fore legs are thick vertical columns (the bracers). The hind legs are bent, with the hock low (semi-plantigrade).
  - The tail leaves the rump at 0.4 H. It is carried either in a high arc over the back (idle, roars, phase 3) or low
    behind and curling up at the tip (walking).
  - The horn crescents stand above the head like a gold-and-black "C" opening forward.
* **Front** (v1 f2130, v2 f0750, v4 f2160): a wide, almost square mass.
  - The two bracer columns sit at the corners, 1.16 H apart.
  - The red-eyed dark mask is framed by the "( )" gold sleeves. The cream apron fills the space between the legs nearly
    to the floor.
  - Above it all, the dark plate fan. In the absorb crouch it reads as a spiky crown up to 1.15 H (v4 f0900).
* **Rear** (v3 f1560): two ribbed grey-cream hind gaiters with orange heel spurs. Between them the tail rises out of a
  broad cream **ventral fin with gold leaf-veins**, 0.44 H wide at the base. Dark plates and gold hip crystals sit on
  each side.
* **Top** (constructed, `05` bottom): a fat oval torso, 6.0 b wide and 8 b long, with the head 1.55 b wide (4.4 b with
  the sleeves). The plate rows splay out from the spine like ribs. The tail is 3.1 b wide at the root and tapers to the
  leafy branch. No true top view exists in the footage; the closest are v4 f0900 (front-high) and v3 f0480.

## 3. Part list

Part numbers match the callouts in `model/01_part_map.jpg`. Sizes are at H = 7.0 b.

### 3.1 Head (callouts 1, 2, 3, 12, 21, 22, 23; `02_head.jpg`)
* **Skull / face mask (3)**: a dark brown, faceted rock mask, wedge-shaped toward the snout.
  - Length 2.25 b (snout to the back of the crest). Width 1.55 b at the eyes, 2.95 b across the cheek guards.
  - About 6–8 short **radiating spikes** (0.3–0.5 b) frame the brow and run back over the crown into the neck ruff.
  - A grey-brown **keel blade** (0.25 b wide, 1 b tall) runs up the forehead between the eyes and continues as the
    crest ridge.
  - Colours: mask `#523629`/`#3E281F`, keel `#8A6650`/`#6A4A3A`.
* **Eyes (2)**: red slits, 0.3 b long and 0.1–0.12 b tall, 0.8 b apart. Recessed under the brow, angled down toward the
  midline. Emissive red (`eye` ramp, §4). They are the main "where is it looking" cue: keep them bright in every phase.
* **Beak / chin shield (22)**: a cream stone plate shaped like an inverted shield, 1.1 b wide, covering the front of the
  muzzle and the chin. Its upper edge is serrated (the teeth of the closed mouth). Colour `#DCD2BA`/`#C3B89D` with dark
  engraved lines.
* **Jaw + mouth**: the lower jaw hinges under the ear and opens up to 45–50° (`motion.md` bone 7).
  - Inside: an upper and a lower row of **blocky white teeth**, about 8 per row visible across the front, 0.15–0.2 b
    each, and **2 larger lower fangs** at the corners (portrait).
  - Gums `#C9505E`/`#A73A48`, tongue `#B45A62`, teeth `#F2EAD6`/`#D8CDB4`.
  - Outside, the jaw is covered by the cream beard (3.2).
* **Horns ×2, composite (1 = sleeve, 12 = dark horn, 21 = knob)**:
  - Path, at the head-low pose: from the knob (rig ±0.95, 0.55, −4.75 from the body centre; beside the mouth corner),
    up and out past the eye to the widest point (±2.2 b from the midline at eye height), up-back to the brow top (2.9 b),
    then the dark horn up to the tip at 3.85 b, curling forward and slightly inward.
  - **Sleeve**: thick gold, 0.75 b at the knob tapering to 0.55 b. A raised rim along its outer edge, an orange-brown
    meander/zigzag inlay along the face. The knob is a rounded bulb 0.5 b across.
  - **Dark horn**: 0.5 b at the sleeve mouth to a 0.08 b tip. Matte near-black brown with a faint warm highlight.
  - Length along the curve ≈ 3.8 b (sleeve 2.6 + dark horn 1.2).
* **Meander ear plates ×2 (23)**: square plates behind the sleeves at the temples, 0.6 × 0.55 b. Gold `#E6A93A` with the
  回 square spiral engraved dark (`#6B3719`), on a dark brown mount that juts out like an ear.
* **Small gold brow edging**: thin gold rims on the crest plates over the brow (v5.md "smaller gold brow plate"). This is
  minor: paint it on the crest plates.

### 3.2 Beard and chest apron (callout 4; `03_body_details.jpg` B)
* **Beard**: 2–3 layered triangular cream plates hanging from under the jaw and throat. 1.6 b wide, lengths 0.8 and
  0.7 b. These are `motion.md`'s `beard1/beard2`.
* **Apron**: one large draped cream stone panel, 2.0 b wide, from the throat (≈ 1.9 b) down between the fore legs to
  0.4 b above the floor.
  - Slightly convex. The lower edge is lobed, with rows of round pebble bumps (0.2–0.3 b).
  - A small gold drop-spike hangs at the bottom centre.
  - The engraving is a big line glyph: vertical zigzag bands and square-meander hooks in thin dark grooves (`#4E463A`).
    The phase-2 element glow runs in these lines (§4.2).

### 3.3 Neck
Short and thick (≈ 1.75 b). It slopes down and forward from the shoulder hump to the occiput. The front is under the
beard. The back carries the **neck ruff**: 5–6 smaller dark plates (1.2–2 b) radiating backward, the "spiky lion mane"
silhouette behind the head (v5.md).

### 3.4 Torso: hide and belly (13, 14)
* **Rock hide**: olive-umber stone (`hide` ramp).
  - Covered in round **pebble scales**, 0.15–0.35 b, larger on the shoulders and haunches.
  - Big rounded muscle masses: the shoulder hump (to 4.3 b), the haunches (to 3.6 b) and the upper arms.
* **Belly**: cream-grey plastron of **4–6 broad horizontal ribs**, like a turtle underside, from behind the apron to the
  groin. The underside is at 1.4 b mid-body. Faint vertical crack lines; in Pyro phase 2 the cracks glow red-orange
  (v9 f0330).

### 3.5 Dorsal plates (6)
* Dark umber blades, like obsidian feathers. Pointed, slightly curved back, 0.15–0.25 b thick, 0.6–1.0 b wide at the
  base, 1.2–3.0 b long.
* Groups (side scan of v8 f2280, tips in H):

  | group | plates | tips |
  |---|---|---|
  | neck ruff | 5–6 small | 0.60–0.73 |
  | shoulder crest | 5–6, the tallest | to 1.00 |
  | mid-back | 4–5 | 0.92–0.98 |
  | hips | 4 | 0.60–0.75 |
  | central spine row | 4 short | — |

  Between them, about 20 plates per side when counting the small ones.
* From the front-high view (v4 f0900), the rows **splay outward** like a fan. Idle width 5.25 b, bristled 7.0 b.
* Colour `plate` ramp. Several plates have **orange-amber lower thirds** (`#C47A2E` → `#7E4219`). Rim highlights are
  greyish.
* Phase 3: the plate edges glow in the tail element (§4.2).

### 3.6 Gold crystals (5, 9, 19, 20)
* **Back / shoulder shards (5)**: about 5 a side along the lower edge of the plate crest, plus one large spike on top of
  each shoulder (to 4.7 b).
  - Each is a cluster of 2–3 flat pointed blades fanned out like a trident or a bird with spread wings. 0.25–0.4 b
    blades, 0.8–1.4 b long.
  - Saturated gold (`gold` ramp) with darker amber edges.
* **Elbow crystals (9)**: 3–4 hexagonal prisms per fore leg, jutting backward and up from the elbow. 0.2–0.3 b thick,
  0.8–1.0 b long. Amber at the tip grading to orange-red at the base (`crystal` ramp).
* **Heel spurs (19)**: one orange-red prism per hind leg on the back of the gaiter top, 0.25 b thick, 0.7 b long.
* **Hip clusters (20)**: 3–4 small gold blades on each hip (rear view).
* None of these change colour with the element.

### 3.7 Fore legs ×2 (7, 8)
* The upper arm is mostly hidden in the shoulder mass (pebble hide).
* **Bracer**: a columnar red-brown stone gauntlet, 1.5 b wide, from the wrist (0.4 b) to the elbow (2.25 b).
  - Front face: carved **zigzag / meander lines** (light grooves `#B08A68` in dark stone) and 2–3 small gold studs
    near the top.
  - The phase-2 glow runs in these lines. In Hydro the front face shows a large diamond glyph with inner lines (v4 f1680).
* **Paw**: 1.75 b wide, 0.5 b tall. Pale beige knuckle pads (`#9C8E78`), **4 big curved black talons**: 0.3 b wide,
  0.55 b long, pale-tipped. A small dew claw on the inside.

### 3.8 Hind legs ×2 (15, 18)
* Thigh: a big haunch mass with 2–3 dark plates on its top edge and the gold hip cluster.
* Knee forward. **Shin/gaiter**: grey-cream stone with **4–5 horizontal ribbed rings**, 1.3 b wide, from 0.35 to 1.55 b.
  Engraved lines on the rings carry the phase-2 glow (v8 f2280, v8 f1320).
* Hock low (≈ 0.9 b) with the orange heel spur.
* Foot 1.55 b wide with 3 big talons + 1 small (rear view v3 f1560).

### 3.9 Tail (16, 17, 11)
* **Body**: a thick tapering chain.
  - Core diameter 1.4 b at the root, 0.8 b mid, 0.25 b at the branch.
  - The **top** carries a row of about 10–12 dark blade spikes: 0.9 b tall at the root, shrinking to 0.2 b, angled back.
  - The **underside** is the broad cream **ventral fin**: 3.1 b wide at the root (a skirt between the hind legs), 1.2 b
    mid, merging into the branch. It carries a **gold vein pattern**: a central line plus nested upward chevrons, like a
    leaf midrib (`#C98625`).
  - The flanks are dark umber like the plates.
* **Branch + leaves (11)**: the last ≈ 40 % (≈ 5.8 b) is a dark, gnarled branch (`#45342A`) with 2–3 short side twigs
  and **6–8 leaf clusters** (0.8–1.0 b each).
  - Geo (phases 1–2): orange-gold autumn leaves (`leaf` ramp).
  - Cryo: white-cyan crystal blossoms.
  - Electro: violet blossoms with pink-violet sparks.
  - The tip leaves rustle in idle (`motion.md`).
* Recommended length 14.5 b along the centreline (measured 13.3–17.3 b at H = 7). The rig chain in `motion.md` is 8
  segments + tip, Σ 11 b; lengthen it to ≈ 14.5 b (§9).

### 3.10 Glowing lines and cracks (phase looks)
In-game "glowing veins" are the **carved lines** of the bracers, gaiters, apron and belly cracks (phase 2), and the
**plate edges** and tail leaves (phase 3).
* There are no glowing veins in phase 1: only the eyes glow. The gold parts are bright but not emissive.
* The lines **pulse brighter** in the wind-ups and the absorbs (v5.md §4.2).

### 3.11 Not rig parts (fx or props)
The element sigils (火 / Hydro hooks), the brands, the floor glyphs, the rocks and meteors, the water orbs, the ice spikes
and lightning, the absorb vortex, the burrow crater and the dust. The stone steles of the intro seal are arena props.

## 4. Colour palette

Full swatches with the footage evidence: `model/06_palette.png`. Data: `model_work/palette_rec.json`. Evidence (k-means
per region): `model_work/palette.json` and `palette.txt`.

The footage is fog-tinted: olive haze in phase 1, blue for Hydro and Cryo, red for Pyro, violet for Electro. The ramps
below are lifted to a neutral light and checked against the portrait palette in `wiki.md`.

### 4.1 Base (all phases)

| material | ramp, hi → deep |
|---|---|
| rock hide | `#8C7B5E #77674D #655640 #554733 #433827 #2E261A` |
| dorsal plates | `#8E6B55 #6E4C3B #573A2C #452C22 #34211A #221510`; orange bases `#E39A48 #C47A2E #A35E22 #7E4219 #5A2C12` |
| dark horn | `#5E4A3E #46362E #352823 #2A201C #1F1815 #141010` |
| gold sleeves / shards / ear plates | `#FFE7A0 #F7C957 #E6A93A #C98625 #9E5E1A #6A3A12`; inlay `#A65A24 #8A4A1E #6B3719 #4A2412` |
| elbow / heel crystals | `#FFD98A #F4A845 #E07A2A #B9521C #7E3014` (tip → base) |
| cream stone (beard, apron, beak, belly, ventral fin) | `#EFE8D4 #DCD2BA #C3B89D #A69B80 #857B63 #625946`; engraved line `#6E6352 #4E463A #3A3329` |
| fore bracer | `#B08A68 #946E50 #77543C #5E402D #4A3022 #24150F` |
| hind gaiter | `#C7BBA0 #ADA086 #918469 #756A54 #5A5142 #3E382E` |
| talons | `#6E655A #554C43 #3E3631 #2D2723 #1F1A18`; toe pads `#9C8E78 #7A6E5C` |
| face mask / keel | `#8A6650 #6A4A3A #523629 #3E281F #2E1D17 #21140F` |
| mouth | gums `#C9505E #A73A48 #7A2733`, tongue `#B45A62`, teeth `#F2EAD6 #D8CDB4` |
| eyes (emissive) | `#FFE0E0 #FF8A8E #F04352 #C81A2C #8E0E1B #4E070E` |
| tail branch | `#5A4434 #45342A #34271F #261C16` |
| Geo leaves (phases 1–2) | `#FFD98A #F7B54A #E58F2E #C06A1E #8A4515` |

### 4.2 Element looks

The **legs** look covers the 2 fore bracers, the 2 fore paws, the 2 hind gaiters and feet, the apron and the belly
cracks. The **tail** look covers the dorsal plates, the neck ruff, the tail spikes, the tail branch and the leaves.

| look | region | glow lines (core → edge) | base recolour | evidence |
|---|---|---|---|---|
| **Geo** (phase 1) | — | none (eyes only) | base ramps | v2, v3 |
| **Hydro** (phase 2) | legs + chest | `#F0F8FF #CDE6FF #9CC4F2 #6E96D8 #4A66B4` (white-cyan with a blue edge) | bracers and gaiters → navy-black stone `#566982 #3F5472 #302F4B #202036`; apron stays cream with blue-white lines | v4 f1680, f1380; v5.md (navy legs, white-cyan lines) |
| **Pyro** (phase 2) | legs + chest + belly cracks | `#FFF0D0 #FFC98A #F9A761 #E5703A #B8401E` | bracers and gaiters → deep red stone `#C03124 #96271D #6E1C15 #46120D`; apron cream with red-orange lines | v5 f0420/f0240, v9 f0330, v8 f2280; v5.md |
| **Cryo** (phase 3) | back + tail | plate edges `#F2FFFF #CFF6FF #9EE3F5 #6CC4E2 #3F95BE` | plates and branch cool down `#4E5A70 #3E4A60 #2B3A50 #1E2A3E`; leaves → crystal blossoms `#F4FFFF #C9F9FC #95DCEC #6CBFD9 #4E9BBB` | v8 f1680, f2160, f2280; v9 f0330 |
| **Electro** (phase 3) | back + tail | plate edges `#F6E2FF #DDB0F6 #B97CEB #8F55D6 #6438B0` | plates and branch → `#5A4060 #463050 #34243E #24182C`; leaves → blossoms `#C7B4F2 #9C7FD6 #7657B8 #5A40A0 #3D2A6C`, sparks `#E4A6F0` | v6 f2340, v7 f0600, f0060; v5.md (pink-violet tree) |

* Phase 3 **keeps** the phase-2 legs look (v9 f0330: Pyro legs with a Cryo tail; v8 f1680 the same). The two looks are
  independent channels.
* There are four combinations, 불/번개, 물/얼음, 불/얼음 and 물/번개, and all four must render: the legs channel takes
  Geo, Hydro or Pyro and the tail channel takes Geo, Cryo or Electro.
* The absorb: about 110–120 t, untargetable (`mechanics.md` §2.4). The look switches at the burst, and the glow lines
  pulse.

### 4.3 What glows (brightness 15) and when

| part | phase 1 | phase 2 | phase 3 |
|---|---|---|---|
| eyes | yes | yes | yes |
| gold sleeves / shards / crystals | bright (14), not emissive | bright (14) | bright (14) |
| bracer / gaiter / apron lines | no | **yes** (legs element) | yes |
| plate edges, tail spikes | no | no | **yes** (tail element) |
| tail leaves / blossoms | warm-bright (14) | warm-bright (14) | **yes** (blossoms 15) |

## 5. Geometry or paint at Minecraft resolution

The cut-off at H = 7.0 b:
* **Geometry** for anything that changes the **silhouette**, moves on its own, or is bigger than about 0.25 b in its
  smallest dimension.
* **Paint** for surface relief under 0.2 b and for every engraved or line pattern.

Assume about 48 px per block on the head, horns and bracers, and 32 px/b elsewhere (`rigtech.md` §5.2).

| detail | size (b) | verdict | how |
|---|---|---|---|
| horn sleeves + knobs | 0.55–0.75 thick, 2.6 long | **geometry** | 4–6 tapered boxes per horn along the C curve (22.5° steps), the knob as 2 stacked boxes; 2 horn parts |
| dark horn tips | 0.5 → 0.08, 1.2 long | **geometry** | 3–4 tapering boxes continuing the curve |
| meander inlay on the sleeves | 0.05 lines | paint | dark-orange lines on the gold face texture |
| ear plates | 0.6 × 0.55 × 0.15 | **geometry** (thin box on a mount box) | the 回 spiral is painted |
| face mask facets + brow spikes | spikes 0.3–0.5 | **geometry** for 6–8 spikes and the keel blade | small boxes rotated ±22.5°; facet shading painted |
| eyes | 0.3 × 0.12 | geometry (emissive card) | a recessed card on a separate bright part, or a texture look on the head |
| beak / chin shield | 1.1 wide | **geometry** | 2–3 boxes; the serrated edge as a cut-out card along the lip line |
| teeth | 0.15–0.2 | **mixed** | the 2 lower fangs and 4 front teeth per jaw as boxes; the rest painted on the inner jaw faces |
| gums, tongue | — | paint | inner faces of the jaw and head boxes |
| beard plates | 0.8 × 1.6 | **geometry** | 2–3 tilted thin boxes or cards (secondary sway) |
| apron | 2.0 × 1.5, convex | **geometry** | 3 stacked boxes stepping out (convex) + a lobed bottom card |
| apron glyph lines, pebble edge | lines 0.05, pebbles 0.2–0.3 | paint (+ glow overlay) | the line pattern is also the phase-2 glow mask |
| dorsal plates | 0.15–0.25 thick, 1.2–3 long | **geometry** | one thin tilted box per plate (about 30–36 plates in 3–4 groups), or crossed cut-out cards for the small ones |
| plate edge glow | 0.05 | paint (look overlay) | a pale rim on the plate texture; brightness 15 for the plate parts in phase 3, or an overlay |
| gold shards | blades 0.25–0.4 × 1 | **geometry** | 2–3 thin boxes per cluster at ±22.5/45°; about 12 clusters |
| elbow crystals / heel spurs | 0.2–0.3 thick | **geometry** | hex prism = 2 crossed boxes rotated 45°, 3–4 per elbow, 1 per heel |
| rock hide pebbles | 0.15–0.35 | paint, plus 3–5 large rounded bumps as boxes on shoulders and haunches | bevel-shaded discs on the hide tile |
| belly ribs | bands 0.4, relief 0.1 | paint + 2 shallow step boxes | |
| fore bracer | 1.5 × 1.85 column | **geometry** (an octagonal-ish box stack, 0.05 b proud of the arm) | carved lines painted; gold studs as tiny boxes (optional) |
| talons | 0.3 × 0.55 | **geometry** | 2 tapered boxes each, 4 per fore paw, 3–4 per hind foot (about 30 boxes) |
| toe pads | 0.25 | paint (+1 box per pad optional) | |
| hind gaiter rings | rings 0.25 tall, relief 0.08 | **geometry for the ribbed silhouette** | 4–5 stacked boxes alternating ±0.04 b; lines painted |
| tail spikes | 0.2–0.9 tall | **geometry** | 1–2 blade boxes per tail segment |
| tail ventral fin | 3.1 → 1.2 wide, 0.2 thick | **geometry** (a flat wide box under each of the first 5 segments) | gold veins painted |
| tail branch + twigs | 0.25 thick | **geometry** | thin boxes |
| leaves / blossoms | clusters 0.8–1.0 | **cut-out cards** (2 crossed cards per cluster) | the leaf shapes painted with alpha; the element swaps the texture |
| carved glow lines (all) | 0.05 | paint | as a separate look texture (§7.3) |

## 6. Articulation the model must allow

These are the hinges and silhouettes the patterns need (`motion.md` §2.1 has the full bone list). They set where the
parts are cut:
* **Jaw** opens to −50° (roars, chin slam). The teeth must exist on both jaws, and the gums show.
* **Head and neck**: pitch −45…+60°; the head rears to 9–10 b in the rear-ups.
* **Horns** are rigid with the head (no secondary motion). They are separate parts only for reach (§7) and brightness.
* **Beard** sways (secondary). The apron hangs from the chest and swings 5–10° in the rear-ups.
* **Plate groups bristle** (pitch out +12…+20°, scale ×1.1) in the absorb and 천동만상. Group them by bone: neck ruff,
  shoulder crest, mid-back, hips.
* **Fore legs**: upper arm, bracer and paw. The paws curl claws-down in the air.
* **Hind legs**: thigh, shin, foot.
* **Tail**: 8 segments + tip, each ±60°. It whips, slams, raises like a scorpion, and stands up as a pillar in the
  phase-3 burrow. The tip leaves rustle.
* **Burrow**: everything except the tail sinks below an opaque floor (`rigtech.md` §4).

## 7. Construction plan (for the rig author)

### 7.1 Parts
This builds on `rigtech.md` §5.1: 37 core parts, cap 48, hard cap 56. Model-side changes:

| group | parts | display scale | notes |
|---|---|---|---|
| torso | pelvis, belly, chest | 2.5–3 | hide tiles; belly ribs on `belly`; chest carries the shoulder humps |
| apron | apron (child of chest) | 1.6 | separate for the legs look and the swing |
| beard | beard1, beard2 | 1.2–1.5 | cream plates |
| neck | neck1, neck2 | 2 | neck ruff plates on neck2 |
| head | head (mask, keel, brow spikes, beak top, ear plates), jaw (teeth, beard root), eyes (emissive) | 2.2 / 2.2 / 1 | eyes as their own bright part |
| horns | in `head`, or horn_l / horn_r (sleeve + dark horn + knob) | 2.2 (in head) / 1.6–2 | reach is not the problem: the tips are ≈ 2.6 b from the atlas pivot, inside the 3.3 b reach of a scale-2.2 head. Split them only to keep the head model under its element count or to give the gold its own brightness (14 vs 13). |
| plates | plates_neck, plates_shoulder, plates_mid, plates_hip | 2 | 4 groups for bristling; phase-3 look |
| crystals | crys_l, crys_r (shoulder + back shards) | 1.6 | rigid with chest/spine; never recoloured |
| fore legs ×2 | upperarm, bracer, paw | 1.6–2 | legs look on bracer + paw; elbow crystals on `bracer` |
| hind legs ×2 | thigh, gaiter, foot | 1.6–2 | legs look on gaiter + foot; heel spur on `gaiter` |
| tail | t1…t8 + tip | 1.6 (t1–t4), 1.2 (t5–t8) | spikes and ventral fin per segment; tail look on all |
| tail branch | branch1, branch2 (leaf clusters) | 1.2 | tail look; replaces `motion.md` tree1/tree2 |
| glow overlays (optional) | glow_bracer ×2, glow_gaiter ×2, glow_apron | same as the host | brightness 15, alpha-cut line masks; only needed if baked lines look dull (§7.3) |

That is about 44 parts without the overlays and 49 with them. Add about 12 hit proxies (`rigtech.md` §3.3).

### 7.2 Textures
`rigtech.md` §5.2 densities apply, with a budget of ≤ 1.2 M atlas px. Sprites to paint:

| area | sprites |
|---|---|
| hide | `hide_a`, `hide_b` (pebbles, tiled, 128²) |
| plates | `plate_dark` + `plate_dark_orange` (64×128), `plate_cryo`, `plate_electro` |
| gold | `gold_sleeve` (meander inlay, 128×256), `gold_shard` (64×128), `ear_meander` (32×32), `crystal_amber` (32×64) |
| head | `horn_dark`, `mask` (faceted), `keel`, `beak` (serrated edge, alpha), `teeth`, `gums`, `eye` (64×16, emissive) |
| cream | `beard`, `apron` (192×192 glyph), `belly_ribs` (160×128), `fin_veins` (128×192) |
| legs | `bracer` (160×96, carved lines) + `bracer_hydro` + `bracer_pyro`; `gaiter` (ribbed, 128×64) + Hydro/Pyro; `paw`, `talon` |
| tail | `tail_top`, `tail_side`, `branch` |
| leaves | `leaf_geo`, `blossom_cryo`, `blossom_electro` (cut-out, 64×64 each) |

### 7.3 How to show the element looks
Two options, with no API change either way:
1. **Texture-swap looks** per part (the butterfly's `wlook` pattern). The line pixels are painted in the glow colour,
   and during the phase the part brightness goes to 15. This is cheap and reads well on the bracers and gaiters (small,
   dark parts), but it flattens their shading.
2. **Bright overlay parts** (`glow_*`), as the fieldgen `ring_glow`: line-only alpha textures 0.02 b proud, brightness
   15, tinted per element.
   * `mechanics.md` §2.4 suggests the same idea as a tinted overlay item per region using the kits' tint mechanism.
   * Tinting one white line texture per element also saves atlas space.

**Recommendation**: option 2 for the legs channel (5 overlays, white masks, tint per element); option 1 for the tail
channel (plates and leaves need different shapes per element anyway).

## 8. Best reference frames per part

All of these are in `model_work/full/`. Composite sheets: `08_best_frames.jpg`, `02_head.jpg`, `03_body_details.jpg`.

| part / view | best frames |
|---|---|
| whole side + tail arc (the side ruler) | **v8 f2280**; v7 f0600 (Electro, tail loop); v7 f0540 (walking); v3 f1170 (close, crouched, tail raised); v3 f1320 |
| front, whole | **v1 f2130** (walking, head raised); v2 f0750 (head low, crouch); v3 f1800 (3/4) |
| rear + tail root | **v3 f1560**; v3 f1530, f1590; v7 f1200 (rear 3/4, Electro) |
| high front, plate fan | **v4 f0900** (absorb crouch); v4 f0840–f0960 |
| head front | **v4 f2160**; v2 f0420; v4 f1560; v3 f2280 (3/4 low) |
| horn construction | **v1 f2370** (oblique); v3 f2280 (knob); v4 f1830 (from above) |
| mouth open | **v2 f0840**; v4 f1620; v2 f0540; v6 f0480 (roar, Electro) |
| beard + apron | **v2 f0600**; v3 f2100; v3 f2070; v4 f1380 (Hydro glow lines) |
| belly ribs + hide pebbles | **v3 f1170**; v3 f0720 |
| back plates + gold shards | **v3 f0720**; v3 f1290, f1320 (far); v8 f2280 (scan) |
| fore bracer + talons | **v3 f2100**; v2 f0600; v4 f1680 (Hydro lines); v9 f0330 (Pyro) |
| hind gaiter + heel spur | **v3 f1560**; v8 f2280 (Pyro glyph lines) |
| tail underside / fin veins | **v3 f1500**; v3 f1560; v7 f1140–f1200 |
| tail branch: Geo / Cryo / Electro | **v3 f1680** / **v8 f2160** / **v7 f0600** |
| phase looks: Hydro / Pyro / Cryo / Electro | v4 f1680 / v5 f0420 + v9 f0330 / v8 f1680 / v6 f2340 |
| absorbs | v4 f0900 (Hydro), v5 f0240 (Pyro), v7 f1500 (Cryo), v6 f0060–f0300 (Electro) |

## 9. Conflicts with the other studies (proposed resolutions)

| item | other study | this study | resolution |
|---|---|---|---|
| tree on the back | `motion.md` bones `tree1/tree2`; v1.md "tree on the back" | it is the tail tip (§0) | drop `tree1/tree2`; the leaves are on `t8`/tip/branch parts |
| plate-tip height | `motion.md` 7.5–7.8 b | H = 7.0 b recommended | scale `motion.md` joint heights by 0.91, or keep 7.6 if the arena gets r ≥ 30 |
| nose → rump | `motion.md` 12.5 b (1.63 H) | 1.46 H (10.2 b) | use 1.46 H (5 frames + v7/v8 analysts) |
| wheelbase | `motion.md` 6.4 b (0.84 H) | 0.72 H (5.0 b) | use 0.72 H; check the foot IK in the stomp clips |
| tail length | `motion.md` 11 b (Σ 8 segments); `chapter.md` total 14–16 b | 1.5–1.7 L measured; 14.5 b recommended | lengthen the chain to ≈ 14.5 b (segments 2.3, 2.1, 1.9, 1.8, 1.7, 1.6, 1.6, 1.5) |
| eye colour | wiki portrait amber | red in game | red |
| absolute size | v2.md 5.4 m to the spikes | ≈ 9 m | v2.md's heights are inconsistent with its own widths |

## 10. Files in `understand/model/`

| file | content |
|---|---|
| `01_part_map.jpg` | front (v1 f2130), side (v8 f2280), rear (v3 f1560) and head (v4 f2160) with the 23 numbered parts and a legend |
| `02_head.jpg` | 6 head close-ups: front mask/keel/beak/eyes (labelled), 3/4 knob, horn construction, open mouth ×2, roar |
| `03_body_details.jpg` | back plates + shards, apron glyph, fore bracer + talons, belly ribs, hind gaiters, tail fin veins, Geo / Cryo / Electro tail tips |
| `04_silhouettes_traced.jpg` | hand traces on the side, front and rear frames, and the same outlines normalised to H with the landmark lines and both players |
| `05_proportions_blocks.png` | recommended block-out at H = 7.0 b: side, front and top on a 1-b grid, the MC player and a dimension list |
| `06_palette.png` | base ramps and the four element looks, with the k-means evidence chips |
| `07_element_states.jpg` | 12 frames: Geo base, Hydro absorb/legs/chest, Pyro absorb/legs/chest, Cryo back/tail, Electro back/absorb/tail |
| `08_best_frames.jpg` | the 12 best reference frames (side, front, rear, plate fan, head, horn, mouth, apron, back, tail) |

## 11. Open checks for the builder

* The C-curve of the horns has to be built from 22.5° box steps. Check it in a side render against v8 f2280 and v1 f2370
  (knob forward, tip forward), and in a front render against v4 f2160 ("( )").
* The plate crest is about 30 thin boxes. Check the silhouette from the side and from the front-high camera (v4 f0900)
  for gaps and z-fighting (`rigtech.md` §2.4).
* The tail at 14.5 b with scale-1.6 segments: check `checkBounds` per segment (reach 2.4 b at scale 1.6, segment ≤ 2.3 b
  plus spikes).
* The leaf cards need alpha-cut sprites with transparent borders (the butterfly overlay rule).
* The glow overlays, if used, must sit 0.02 b proud and stay hidden (scale 0) in the Geo look.
* At H = 7.0 b the apron foot is 0.4 b above the floor. The player's camera at the boss's chin sees under the apron only
  at an extreme angle; keep the inner faces painted dark.
