# 실험성 역장 발생 장치 (nameplate 브레게 프로토타입, Breguet Prototype): modelling spec for a display-entity rig

Sources:
* `src/guide.pdf` (namu wiki, 2 pages). Page 1 has the portrait icon (626x625, `understand/model_work/pdf/img-000.png`) and the
  full render (1807x1288, `img-001.png`). Page 2 has the lore and the pattern list. The 300 dpi page rasters are
  `understand/model/guide-1.png` and `guide-2.png`.
* `src/v1..v4.mp4` (1920x1080, 60 fps; all four are real time, with no slow-motion replays). My own frames are in
  `understand/model_work/full/` (`v<N>_f<frame>.png`) and my crops are in `model_work/crops/`. The low-resolution overview
  sheets are `model_work/sheet_v*_*.jpg` and the strips are `model_work/strip_*.jpg`. My scripts are in
  `understand/model_tools/`: `sheetlib.py`, `sheet01..09.py`, `palette.py`, `rig_plan.py`, `grid.py`, `gridcrop.py`,
  `measure_check.py` and `prevgrid.py`.
* I used the per-video reports `understand/v1.md`, `v2.md`, `v3.md` and `v4.md` for the pattern timings and the pattern
  names. I re-measured the model myself.
* The shared rig libraries are on `wip/bf-rig` in `mb2/wt_rig/roguelike/tools/`: `mboss_rig_math.mjs`,
  `mboss_rig_clips.mjs`, `mboss_rig_compile.mjs`, `mboss_model_lib.mjs` and `mboss_paint_lib.mjs`. §7 is written against
  them, and the butterfly's `build_mboss_butterfly_rig.mjs` and `mboss_butterfly_rig_api.md` are the pattern to copy.

Frame notation: `v3 f0945` is 60 fps frame 945 of v3 (15.75 s, tick 315; tick = f / 3).

Conventions (the same as the Guardian and butterfly studies):
* **Rig space**: +X = the device's left, +Y = up, −Z = forward. "Forward" is the side with the keystone iris (§3.3), which
  is the side the device yaws toward the player. The origin is on the floor under the ring axis. The ring centre is at
  (0, H, 0), and the hover height H is a clip channel.
* **D** = the outer diameter of the main ring, without the spikes. This is the master dimension, and every size below is
  given in D first. **b** = Minecraft blocks. The recommended scale is **D = 7.0 b** (§1).
* Pattern names: caption name in the guide videos = PDF name.
  * 폭격 = 중력 시스템·일점 상쇄
  * 레이저 빔 = 중력 시스템·코어
  * 미사일 발사 = 중력 시스템·바위 폭탄
  * 바닥 뜯기 = 중력 시스템·감소 영역
  * 바위 날리기 = 중력 시스템·파쇄
  * 중력 웨이브 = 「인력 충격파」
  * 중력 폭발 = 중력 시스템·지면 충격
  * 역장 생성 - 중력 감소 = the Ousia field state

---------------------------------------------------------------------------------------------------

## 0. Key findings and corrections to the brief

* **Everything floats; nothing is connected.** The main ring is an **open annulus with no spokes and no hub**: the top views
  (v3 f0930, f0945; sheet 02 K) show the floor through the hole. The core hangs or sits in that hole. The halo, the plates
  and the pendulum float on the axis with gaps between them. Two medallions and four drill pods fly around freely.
  * The spacing of the stack changes from form to form. From the halo top to the pendulum tip it is 0.82 D in cruise,
    about 1.07 D in the field form and about 1.1 D in the tower form.
  * So the rig is a **set of free bodies around one root**, not a skeleton. That makes it cheap, but it needs about seven
    named body configurations ("forms", §8).
* **The two "devices beside the core" (PDF 코어 pattern) are two different medallions**:
  * an **eye medallion**: a gold ring with a dark spiral/eye centre and a glowing orange C-ring face;
  * a **gear medallion**: a toothed gear with a glowing hub.

  Evidence: v3.md §6.1 #6, v3 f1620, my v2 f0000 crops (sheet 05), and the PDF ring ends, where one end shows the glowing C
  and the other a dark gear.
  * In cruise they **dock at the two spike mounts at the ring ends**.
  * In 감소 영역 they slide out to ±0.55 D on gold link beams.
  * They are the **laser emitters** in 코어. In the deployed form they ride in the spike X frames as "lances". In 파쇄 they
    dock on top of the tower.
  * The video analysts called them "eye-pods", "laser pods", "gear hubs" or "medallions"; these are all the same two parts.
* **The eye medallion on the front of the band is not the core.** In v2 f1020 it stays on the ring front while the core
  hangs, charging, below the ring (sheet 04).
  * It is a **keystone iris** on the front keystone of the ring: a cream ring with a red-orange pupil in a gear/ray frame,
    with a big gold spike (0.16 D) under it.
  * Shut, it reads as the **gold sunburst fan** seen in the compact views (v2 f1812, v4 f0120, v3 f0930).
  * Its spike **flips up** in the core-up and tower forms. That gives the "three eyes in a row, each topped by a vertical
    spike" of 지면 충격 (v4 f0210): the iris in the middle and the two medallions at the ring ends.
* **The core is a gyroscope assembly**, not just a drum. It has:
  * a dark plum sphere (Ø 0.36–0.40 D) with bronze ribs and dark-red side pads;
  * the eye (gold glow ring, black pupil);
  * a **vertical gear ring ("arch")** around the sphere: bronze, with cream clamps and a dark-red lining;
  * a **tilted grooved brim**;
  * a **thin orbit wire with a gold bead**.

  The arch turns continuously about a horizontal axis (v3.md §6.1 #5). It locks facing the target during 감소 영역 and
  swings 180° over the top when the core flips between "hanging" and "tucked". The core has four positions:
  * **tucked** in the ring hole: compact/cruise;
  * **hanging** 0.28 D below the ring: field, waves, 감소 영역;
  * **lifted** 0.40 D above the ring: 지면 충격;
  * **face-down**, projecting a column: the slam.
* **The halo has a partner.** A thinner **inner gold glow ring** (Ø 0.34 D) floats just under the halo in cruise (v3 f1770,
  v1 f2160).
  * In the field both turn **violet**.
  * In 파쇄 the halo rises to +0.45 D and scales ×1.7 on top of the **tower**: a telescoping column with two tier discs
    (v3 f1510). Neither the brief nor the PDF mentions the tower.
* **The pendulum** is a silver 6-tooth cog with a keyhole, a bronze spindle, a cream-gold **protractor arc** (a vertical
  semicircle, concave up, that reads as a crossbar edge-on) and a gold 4-facet dagger.
  * In the field (and in some compact shots) the cog becomes a **violet crystal flame**, the Ousia glow.
  * Under the core there are **two plates**. The lower plate (Ø 0.38–0.42 D) becomes a wide annulus around the violet glow
    in the field, and a smaller disc sits above it. They separate "like a spring" in the field.
* **Scale.** The reports disagree: v1 gives D ≈ 7.5–8 m, v2 ≈ 5 m and v4 ≈ 6.5–8 m. The proportions inside the device agree
  within 5 % (§1). **Recommended: D = 7.0 b.**
  * The player (1.8 b) is then 0.26 D (Genshin 0.20–0.32 D).
  * The spikes are 10.1 b tip to tip, which fits the r 21 arena.
  * The cruise pendulum (0.6–2.6 b) stays hittable from the ground.
* **20 hits instead of Pneuma (user rule).** The model shows the meter on the core itself. During the field a translucent
  white-gold **bubble** sits around the core (the release bubble of v2 11.90 s). It shows **crack stage 0–3 for hits 0–4,
  5–9, 10–14 and 15–19**. At 20 it bursts and the release runs (§5.4).
  * This is one look swap on `core_glow`, so the counter is readable without UI. The module still owns the count and the
    HUD.
  * There is no Pneuma/Ousia element anywhere in the model or the looks; violet is only the colour of the field.
* **No voice; a machine.** The idle is a hover with spinning parts, so "breathing" comes from the spinners (§5.1).

## 1. Overall size and proposed scale

Measured by me on two broadside frames (`03_proportions_measured.png`). Pixel rows are full-resolution 1080p.

| landmark (from the ring centre) | cruise, v1 f0330 (D = 370 px) | field, v1 f2160 (D = 500 px) | blocks at D = 7 (cruise / field) |
|---|---|---|---|
| halo top | +0.26 D | +0.27 D | +1.8 / +1.9 |
| halo centre (Ø 0.43–0.46 D) | +0.22 D | +0.22 D | +1.6 / +1.55 |
| inner glow ring (Ø 0.34 D) | about +0.19 D | +0.19 D | +1.35 / +1.3 |
| arch top / core top | +0.14 D (arch, tilted) | — | +0.95 |
| ring band (incl. teeth and lower tier) | +0.09 … −0.09 D | same | +0.6 … −0.65 |
| core centre | ≈ 0 (tucked) | −0.28 D | +0.1 / −1.96 |
| drill pod tips / pods | −0.23 D (r ≈ 0.42 D) | pods at core level, r ≈ 0.5 D | −1.6 / −1.9 |
| lower plate (Ø 0.38 / 0.42 D) | −0.21 D | −0.46 D | −1.5 / −3.2 |
| pendulum cog | −0.30 D | −0.52 D | −2.1 / −3.6 |
| protractor bar | −0.38 D | −0.61 D | −2.7 / −4.2 |
| dagger tip | −0.56 D | about −0.8 D | −3.9 / −5.5 |
| rim spike tip to tip | 1.39–1.46 D | 1.46 D | 10.1 b |
| ring centre over the floor | 0.62–0.67 D (v1, v4) | 0.8–0.85 D (v1, v2) | **4.5 b / 5.8 b** |

Other measures, in D units (PDF, sheet 01; cross-checked against v3/v4):

| part | size |
|---|---|
| ring | radial width 0.125 D, so the inner edge is at r 0.375 D; band height 0.11 D (+0.03 D teeth, +0.05 D lower tier) |
| rim spike | 0.22 D long, base 0.09 D; mount/X frame 0.17 D |
| core sphere | Ø 0.36–0.40 D (use 0.36 D = 2.5 b) |
| arch | Ø 0.42 D |
| brim | Ø 0.48 D |
| orbit wire | Ø 0.52 D |
| eye | glow ring Ø 0.14 D; frame Ø 0.17 D |
| medallions | Ø 0.13–0.15 D (1.0 b), 0.05 D thick |
| drill pods | gear disc Ø 0.13 D, height 0.18 D |
| keystone iris | Ø 0.13 D; its spike 0.16 D |
| pendulum | cog Ø 0.09 D, arc span 0.21–0.23 D, dagger 0.17 D; 0.30 D in all |
| tower (v3) | column Ø 0.2 D, 0.39 D tall; tiers Ø 0.53 D and 0.56 D; halo ×1.7 at +0.45 D |

**Scale decision.** The three reports' absolute sizes disagree:

| report | method | D |
|---|---|---|
| v1 | horizon fit | 7.5–8 m |
| v2 | player beside the grounded device | 5.0 m (likely low; the player stood 1–3 m in front) |
| v4 | the blast rim bounds R ≥ 8.3 m, with R = 1.7 D | 6.5–8 m |
| v3 | ±20 % | ring 7.5–8 m |

My own check on v3 f0150 (the player inside the lower stack) is not usable: she is crouched mid-jump.

**Use D = 7.0 b.** The player is then 0.26 D: v1/v3/v4 give 0.20–0.25 D and v2 gives 0.32 D. It also works in the arena:

| item | value | why it works |
|---|---|---|
| spike span | 10.1 b | about half the arena radius (r 22, walk 21), like Genshin's 7–11 m spikes in a ≥ 20 m plaza |
| cruise ring centre | 4.5 b | — |
| cruise pendulum cog | 2.4 b | head height: melee can hit the lower stack from the ground |
| field core centre | 3.8 b (bottom 2.6 b) | ground melee reaches it; the low-gravity jump makes it easy |
| core-up blast R (fx, v4) | 1.7 D = 12 b | matches v4.md's gameplay value |

## 2. Silhouette

* **Cruise / compact** (sheet 02 C–E, v1 f0330, v4 f0600, v2 f0870): a wide flat ring with two long gold spearheads. A thin
  copper halo floats above with a gold glow ring under it. The gyroscope core sits in the middle with its bronze arch
  showing above the ring.
  * Below the ring: four spinning-top pods, a bronze plate, and the pendulum (cog, protractor, dagger) hanging almost to the
    floor.
  * From the front: the keystone iris on the band with a big gold spike under it, and the medallions at the ring ends.
  * It reads as a **flying brass gyroscope / clock escapement**.
* **Dormant** (v1 f0000): the ring is seen edge-on as a flat tan bar with the spikes. Two drill pods are tucked under the
  ring ends and only the dagger shows under the centre. The ring centre is 0.3 D (2.15 b) up.
* **Field** (v1 f2160, v3 f0600, v2 f0000): the stack opens downward.
  * The core hangs with its eye out, gold link beams join it to the two medallions at ±0.55 D, and the drill pods float at
    core level.
  * The plates spread as a wide annulus filled with violet light, and the pendulum glows violet.
  * There are two violet halos.
* **Core-up** (v4 f0210): a gold sphere rises above the ring. Three eyes sit in a row (the iris and the two medallions),
  each with a gold spike pointing up. The ring rolls about 10°.
* **Tower** (v3 f1510): a cream column with two gold-edged tier discs telescopes up out of the ring hole, with the enlarged
  halo on top and the medallions docked at the top. The end spikes tilt up 45° and a flame band burns under the ring.
* **Deployed** (v2 f1704): the spikes with their medallions float 0.8 D out on both sides as lances (cone, bronze shaft, X
  frame round a glowing eye). The ring is hot.
* **Top view** (v3 f0945): a cream annulus with bronze brackets, two dark-red eye-ports, and the spike mounts at 3 and 9
  o'clock. The halo seen from above sits inside the hole and the core floats below.

## 3. Part list

### 3.1 Main ring (sheet 01 #2–6, sheet 05)
* **Annulus**: outer D, inner 0.75 D. It is segmented: joints every 22.5–45°, with cream blocks between bronze brackets.
* **Upper band** (outer wall, 0.11 D high): cream ceramic blocks in the upper half and bronze/brass in the lower half. They
  **interlock by a square wave**, about 2 teeth per 1/16 of the circumference. A **glowing orange-gold seam** runs in the
  joint (`#FFD081 → #C99468`).
  * The square-wave line is the most recognisable texture of the boss. It is **white-gold** when it is not glowing (v1,
    #ECEAE8).
* **Raised teeth**: blocky cream/gold steps on the top edge (crenellation), 0.03 D high. They read in silhouette, especially
  in the dormant edge-on view.
* **Top face**: flat cream panels (`#E0D2CD`) with bronze brackets and an **inner gold crenellated rim**. It carries two
  round **eye-ports**: dark-red/black centres with orange rims, at about −60° and +120° from the front.
* **Lower tier**: a narrower toothed ring under the band (r 0.31–0.46 D). It has cream ribs with dark slots and reads as a
  gear.
* **Underside**: 8 round **bomb ports** (gold rims `#E1BC7E`, dark core `#743B01`). They glow hot during 일점 상쇄.
* **Keystones**:
  * **Back**: a cream T-shaped block cluster rising 0.06 D above the band, with a stepped bronze "bell" under it.
  * **Front**: carries the **iris** (§3.3).
* **Spike mounts** at ±X: curved bronze brackets that cradle a docked medallion.
* Materials: matte cream ceramic, worn brass, dark bronze joints, emissive seam. The glow strips are a separate display
  (`ring_glow`) so they can be brightness 15 and swap looks.

### 3.2 Rim spikes ×2 (sheet 01 #7–10)
* A gold spearhead, 0.22 D long with a 0.09 D base, faceted with **alternating bright gold (`#EBC263`) and pale cream-gold
  (`#EBD9B1`) facets**: an 8-facet pyramid. It has a ribbed cream/gold collar at the base.
* A bronze shaft runs behind the collar into a **4-prong X frame** (bronze, dark-red inner ring). The frame is the cradle of
  a medallion and makes the lance.
* States (rotation about the device Z axis at the socket):

  | state | spike direction |
  |---|---|
  | cruise | horizontal out |
  | compact front (v4 f0600) | down-out 45° |
  | tower | up 45° |
  | core-up | vertical up |
  | lance, first | vertical down, 0.8 D out |
  | lance, then | horizontal out |
  | field charge (v1 f2256) | detached, orbiting 0.7–0.8 D out, tips swivelling in |

### 3.3 Keystone iris (front of the band; sheet 04, v4 f0600, v2 f1020)
* Open: a cream ring (`#FCE0B8`) round a red-orange pupil (`#975942`, deep `#6E251C`) in a gear/ray frame. A small gold spike
  sits above it and a **big gold spike** (0.16 D, base 0.08 D) sits below.
* Shut: a **gold sunburst fan** (radial gold ribs) covers it, as in the compact top-front and day views.
* The spike flips **up** in the core-up and tower forms: a 180° roll about the forward axis keeps the iris facing forward.
* States: shut (dormant, cruise travel), open (attacks), hot (charging, 지면 충격).

### 3.4 Core assembly (sheet 01 #12–17, sheet 04)
* **Sphere**: Ø 0.36 D (2.5 b). Dark plum shell (`#4D3130`) with lighter bronze rib lines (`#8F734F` / `#CFB895`), two
  dark-red curved **side pads** (`#531B11`), a cream Y-bracket at the bottom and a short gold stud.
* **Eye**: on the sphere surface, Ø 0.14 D glow ring.
  * Idle: gold ring `#F6E998 → #AE6A11`, black pupil `#100904` with an **orange streak** across it, cream gear-tooth frame
    around it.
  * Field: red-orange (`#FBE7A3 → #833810`).
  * Charge: white-gold.
  * Exposed (v1 f2412): a gold sphere with a white-gold "ε" glyph.
  * Groggy: dim amber.
* **Arch (vertical gear ring)**: Ø 0.42 D, section about 0.03 x 0.05 D. Dark bronze (`#624127`) with cream clamps every
  ~30° and a **dark-red lining** (`#48180A`) inside.
  * It is a gimbal: it turns continuously about a horizontal axis when free, locks facing the target in 감소 영역, and
    swings 180° over the top in the flips.
* **Brim**: a grooved tan disc (`#D6B693` → `#8B6B48`) from the sphere out to Ø 0.48 D, tilted about 20°, with dark tick
  marks on the rim. A **thin orbit wire** (Ø 0.52 D, `#6D4318`) carries a **gold bead** (`#CEA132`) at the front.
  * They precess slowly.
* **Glow sphere**: the translucent shell for the charge (yellow, Ø ≈ 0.4 D), the field bubble (white-gold, with cracks for
  the 20-hit meter) and the exposed gold state.

### 3.5 Halo pair
* **Halo**: Ø 0.44 D. Thin and segmented with about 10 joints; band 0.035 D wide x 0.02 D thick.
  * Normal look: copper-brown `#624127` with rose highlights (rose-copper `#A6626E` in daylight) and a gold inner glow.
  * Field look: violet `#896CC7` with a pale lilac rim.
  * It flips upright and spins about a horizontal axis before the warp (v1 31.85 s).
* **Inner glow ring**: Ø 0.34 D, just under the halo. Thin and translucent: gold in cruise, violet in the field, the third
  tier of the tower.

### 3.6 Medallions ×2 (sheet 05)
* **Eye medallion**: Ø 1.0 b, 0.35 b thick. A gold ring (`#E2BD89`) with bronze teeth on the rim, a dark spiral/eye centre
  (`#443B4C`) and a glowing orange **C-ring** face (`#F4C165`).
* **Gear medallion**: a 12-tooth bronze-gold gear of the same size with a hub that glows gold.
* Both spin about their face axis when free (4.5 and −6°/t). In 코어 they fire the lasers from their faces.

### 3.7 Drill pods ×4 ("spinning tops")
* A small cog cap, a **gear disc** Ø 0.13 D with cream teeth and dark slots, a **glowing gold collar ring**, and a downward
  **striped cone** (dark bronze with gold/orange glowing bands). 0.18 D tall.
* Positions:

  | form | where |
  |---|---|
  | cruise | under the ring at r 0.42 D, azimuths ±45° and ±135° |
  | dormant | tucked under the ring ends |
  | field | at core level, r 0.5 D, orbiting slowly |
  | deployed | spread to r 0.55 D |

* They spin fast about their vertical axis (spinning tops).

### 3.8 Plates
* **Lower plate**: a bronze annulus with a glowing groove on the rim (`#B88D58`, groove `#EEC170`).
  * Cruise: Ø 0.38 D with a small hole.
  * Field: a wide annulus Ø 0.42 D round the violet column; scale 1.4.
  * Core-up: dropped to just above the pendulum.
* **Upper small disc** (`plate2`): Ø 0.3 D. It separates from the plate in the field.

### 3.9 Pendulum (sheet 01 #21–23, sheet 05)
* From the top down:
  * a silver 6-tooth cog with a keyhole (`#C5C4C5`, `#989899`), Ø 0.09 D;
  * a bronze spindle;
  * the protractor arc: a cream-gold semicircle (`#D4C39D`) with ticks, span 0.22 D, concave up, in a vertical plane;
  * a gold 4-facet dagger, 0.17 D.

  Length 0.30 D (2.07 b).
* It hangs plumb with a slight sway (±3°) and lags root motion by 2–4 t.
* **Ousia look**: the cog wrapped in a violet crystal flame (`#A18CEA`, `#7562D0`, pale `#D9CFE2`), and a violet column
  between the core and the plate.

### 3.10 Tower (파쇄 only; v3 f1140–f1510)
* A cream/gold block **column**, Ø 0.2 D, rising 0.39 D above the ring centre, with the medallions docked on its top.
* **Tier 1**: a dark bronze disc, Ø 0.53 D, at +0.19 D.
* **Tier 2**: a flat disc, Ø 0.56 D, with a glowing gold edge ring, at +0.29 D.
* The **inner glow ring** forms tier 3 at +0.36 D, and the halo sits at +0.45 D scaled ×1.7.
* It telescopes up in 18 t and collapses in 15 t.

### 3.11 Not rig parts (fx or props)
These are not rig parts: the bombs, the missiles (gold drill spikes with blue-white smoke trails), the lifted floor slabs
and rocks, the floating pebbles, the shockwave ring, the floor markers, the flame band under the ring (파쇄), the warp
pillar and the violet glitch.

## 4. Colour palette

Full swatches are in `07_palette.png`. The evidence (k-means clusters per sampled region) is in `model_work/palette.json` and
`palette_proof.jpg`. Body hexes come from the neutral-light PDF render. The in-game day read is warmer and pinker (last
material row).

| material | ramp, hi → deep |
|---|---|
| cream ceramic (band top half, top face, keystones, clamps) | `#EFE3CC #E0D2B8 #C4B6A2 #ADA086 #75674D #423217` |
| bronze/brass (band lower half, brackets, plates, drill bodies) | `#E7CAA5 #C0A17F #A78663 #94704A #785936 #583412` |
| gold (spikes, teeth caps, dagger, bead, iris fan) | `#F6E5B8 #EBD9B1 #EBC263 #C3AC8A #A3875F #7C5C2E` (alternate the 2nd and 3rd on facets) |
| dark bronze/copper (halo, arch, wire, gears) | `#CCC3BE #A17A4A #816651 #624127 #4E2D15 #2E1A0C` |
| plum core shell | `#CFB895 #8F734F #6A4A44 #4D3130 #3A2426 #24161A` |
| dark red (pads, arch lining) | `#A1634E #8F442D #7C3521 #531B11 #48180A #3E1416` |
| silver (cog) | `#E6E4E6 #C5C4C5 #AFAEAF #989899 #72695D #4E4840` |
| protractor cream-gold | `#E4D6B2 #D4C39D #B7A47B #907C50 #624C23 #3F2F14` |
| in-game day read of the device | `#F6D9A6 #C4A080 #AF8D72 #9E7C5F #87604B #5E4232` |

| glow (brightness 15) | ramp |
|---|---|
| `slit_idle` (seam, ports) | `#FFE6A8 #FFD081 #F4C165 #E3BF73 #DBA978 #C99468` |
| `slit_hot` (charge, bombs, missiles, field) | `#FFFFF0 #FFF4C8 #FFE9A0 #FBD27A #F2B65C #E09A45` |
| `slit_off` (dormant, groggy, death) | `#8A6A46 … #382817` |
| core eye idle | `#FBF5D8 #F6E998 #F2DA8E #CFA659 #AE6A11`, pupil `#100904` |
| core eye field | `#FBE7A3 #D4B181 #B7905D #9D5E2F #833810 #3A0E06` |
| keystone iris | `#FCE0B8 #DAAD8B #B1846A #975942 #6E251C #3A140E` |
| charge sphere / gold column | `#FDFBD1 #FDEEAA #FBE483 #F5CF88 #E2AE66 #BC8354` |
| release bubble | `#FFFFFF #FFFAF9 #F4EDE0 #E8DFCC #D9C9A8`, cracks white |
| lasers / link beams | core `#FFF6DA #FADEA8`, body `#FCD88F #E4BB76`, edge `#D4A558 #A97A3A` |
| Ousia violet (halos, cog flame, column) | `#E6DDF6 #D9CFE2 #A18CEA #896CC7 #7562D0 #57337D` |

What glows:
* always: the seam and port rims, the core eye, the iris pupil, the medallion faces, the drill collar rings and cone bands,
  the plate groove, and the inner glow ring;
* in states: the charge sphere and bubble, the beams and columns, the violet field parts, and the hot ring.

## 5. Motion

### 5.1 Parts that rotate on their own (continuous spinners)
Rates are in degrees per tick. Each loop length is chosen so that a whole number of symmetry steps fits (§7.6).

| part | axis | rate | where seen |
|---|---|---|---|
| halo | its own vertical axis | 2.25 (one turn in 8 s) | v1 cruise; joints visible |
| inner glow ring | vertical | −4.5 (counter) | v1 f2040, v3 f1770 |
| core arch (gyroscope) | horizontal (its diameter), with a slow yaw of the gimbal | free: one face turn every 10–20 t; cruise: rock ±20° over 80 t; locked in 감소 영역 | v3.md §6.1 #5, v1 f0330 (tilted), v2 f0870 (upright) |
| brim + orbit wire | precesses about the core's vertical axis | 4.5 | PDF, v4 f0210 |
| medallions | their face axis | eye 4.5, gear −6; laser: also orbit the axis at 5 | v2 f0000, v4 T, v1 f1032 |
| drill pods | their vertical axis | 11.25 (fast top spin) | v1, v4 f0600 |
| tower tiers | vertical | ±3 (counter-rotating) | v3 f1510 |
| plate | vertical | 1 (barely) | — |
| main ring | none in flight (it yaws with the body); rolls/tilts with the root | — | v1.md §7.2 |

### 5.2 Hover, tilt, flight (root channels)
* **Hover**:
  * The ring centre is at H (cruise 4.5 b) with a **bob of ±0.12 b over 80 t**.
  * A slow pitch/roll wobble of ±1.5° runs on a second harmonic.
  * The pendulum lags the bob by 3 t (swing ±2°).
* **Yaw**: it turns toward the player at 45–90°/s, so `face/track` should use **maxDeg 3–4 per tick**, not the butterfly's
  12. Between attacks it drifts slowly (15–30°/s).
* **Attack tilts**:

  | when | tilt |
  |---|---|
  | bomb run | nose-down 15–20° |
  | before the warp | nose-up 30–40° (shows the underside) |
  | form changes | roll 10–25° |
  | 파쇄 dip | roll 25–30° while dropping to ring height 2.8 b (12 t) |
  | release | **tilt 25–30° in 9 t, then a damped wobble ±8° → 0 over ~20 t, re-level 6 t** |
  | pack-up | tilts 20–30° and rocks twice (20 t) |

* **Flight**: the module moves the anchor; the clips have **no x/z root travel**, as in the butterfly rig.
  * Straight bomb run at 0.5–0.6 b/t.
  * Low glide beside the player in 파쇄 take C: ring at 2.5–2.8 b, rolled 15–25°, about 0.15 b/t.
  * During travel the medallions and drill pods trail by 2–4 t (key their offsets 2–4 t late), and the pendulum swings
    back up to 12°.
* **Vertical moves (in the clips)**:

  | move | profile |
  |---|---|
  | entrance rise | 2.15 → 4.5 b over 30 t, eased |
  | slam plunge | −3.5 b in 3–4 t (ease-in), sit 7 t, rise 20 t (ease-out) |
  | wave-3 drop | sink 0.5 b during the charge, then −2.5 b in 4 t onto the floor with the stack compressed (core resting on the floor, ring centre about 2.3 b); grounded 19 t; lift-off pulse; rise 20 t |
  | field | sits higher (5.8 b) |

### 5.3 The core flip-up: 지면 충격 / 중력 폭발 (v4, P0 = 2.55 s, first spark; strip row 2 of `06_motion_strips.png`)

| P+ t | core | eye / iris | spikes, medallions | ring / root | glow parts |
|---|---|---|---|---|---|
| 0 | tucked in the ring hole | — | docked, spikes horizontal | level | spark on the arch top (fx at the core anchor) |
| 1–4 | turns so that the eye faces forward-out | eye open | — | — | sparks |
| 5–6 | **"flash" lift starts** (ease-out) | iris opens | — | small yaw | `core_glow` gold flash, scale 0 → 1.2 → 0.6 in 3 t |
| 7–15 | rises to **+0.40 D (+2.8 b)**; arch upright behind the sphere, brim tilts 25° | eye forward | spikes roll ±90° to vertical about their sockets; medallions slide to the ring ends (±3.6, +0.3) and face forward; **iris spike flips up** (roll 180° about Z, split into 2 keys) | **roll to 10°** | — |
| 16–28 | holds, bob ±0.05 b, arch still | — | — | — | floor marker grows (fx) |
| 29–40 | holds | eye hot | — | — | **up-beam**: `column` gold, pointing up, length 0 → 6 b in 4 t, crackle |
| 40–44 | **drops back toward the ring in 3 t (ease-in)** to +0.6 b | — | — | — | the column switches to **down**, core → floor centre (length ≈ H) |
| 48 | holds | — | — | — | **blast** (fx, one damage tick) |
| 49–77 | holds | — | — | — | rocks hover (fx) |
| 81–130 | sinks into the ring hole; the arch swings back over | iris shuts, its spike flips down | spikes return horizontal; medallions re-dock | roll back to level | — |

The other core moves:

| move | timing | motion |
|---|---|---|
| hanging → tucked ("core flips to the top") | 9 t, after the release (v2 14.20–14.65 s) and in the pack-up roll | the core group rises 2.1 b (from −1.96 to +0.1) while the arch rotates **180° about the device X axis**, from hanging under the ring to standing over it |
| slam | column tell 13 t | the eye pitches 90° down (core_eye aim −90°), the arch rolls flat, then the gold column goes down to the slam point |
| missiles (바위 폭탄) | — | eye pitches up 90°, the arch lies flat, and a gold column goes up from the core as the vent shaft (1.5 m wide, ≥ 6 m) |
| field core flip (v1 36.95 s) | 3 t | the arch swings 90° about X |

### 5.4 Other transitions (strips in `06_motion_strips.png`; timings from v1–v4.md)

| transition | timing | rig motion |
|---|---|---|
| **Entrance** (untargetable E0…E+94; E0 = the clank) | E+0…110 | dormant → drill pods drop (+8…14) → halo and arch rise out of the hole and the plate and pendulum drop (+12…30) → iris/eye opens (+38) → the arch turns about 90° (+44…64) → rise 2.15 → 4.5 b (+64…94, eased) → yaw to the player (+99…110) |
| **Warp to the field** | F+0…51 | halo flips upright and spins about a horizontal axis while the root pitches nose-up 30–40° (12 t) → `vis` 1 → 0 in 1 t at F+13 (warp-out flash fx) → invisible 21 t (the module teleports the anchor to the arena centre) → `vis` 0 → 1 in 2 t → **unfold to FIELD in 16 t**: the core drops 2.1 b, the plates spread, the drill pods move out to core level, the medallions slide out beside the core, halos and pendulum go violet (look swap at the unfold start), then the link beams appear |
| **Field charge** (v1 37.1 s) | — | the spikes detach and orbit 0.7–0.8 D out with their tips swivelling inward |
| **Release (20 hits)** | — | bubble stage 3 → bright 5 t → **burst** (scale 1 → 1.6 and hide in 2 t) → root roll 25–30° in 9 t → wobble 20 t → (groggy, §9) → re-level 6 t → core flips to the top 9 t → violet off |
| **Pack-up roll** (end of the field, v2 28.6–30.4 s) | 28 t | lances turn horizontal; the ring tilts 20–30° and rocks; the arch swings up from under the ring; the lances dock as rim spikes (8 t); the drill pods tuck; violet fades |
| **Laser** (코어; L0 = pods drop) | L+0…174 | medallions drop to r 2.8 b, y −2.0 (4 t) → charge 18 t (hot look) → beams extend 0 → 3.6 b in 2 t at L+24, each **48° out from vertical** so the floor spots run on r ≈ 5.5 b → the medallions **orbit the axis in opposite directions at 5°/t** for 133 t (the spots meet every 35 t, front and back) → beams off → retract 16 t |
| **Tower** (파쇄) | R+0…157 | dip: roll 25–30° and drop (12 t) → vent: column up + medallions flung to ±5.5 b (8 t) → rise and level while the tower telescopes up (18 t): column out, tiers to +1.35 / +2.0, inner ring to +2.5, halo to +3.2 at ×1.7, end spikes up 45°, iris spike up, medallions dock on the column top → flame band (fx) 17 t → bursts and slabs (fx) → revert 15 t with a 20° roll wobble |
| **감소 영역** | 22 t | activation: the arch faces the target and stops spinning, the medallions slide out to ±3.85 b on link beams, the stack spreads to field spacing; at the end the beams go off and the gyroscope spins again |
| **Waves** (인력 충격파) | 24 t charge (40 t for the 3rd) | `core_glow` charge sphere grows 0 → 1.0 with 4 pulses, the eye goes hot, then the down column flashes 1 t; the 3rd adds the drop (§5.2) |

## 6. Articulation needed by the patterns

| pattern | key poses (sources) | must move |
|---|---|---|
| entrance | dormant → unfold → rise (v1 0–6.3 s) | everything; the stack spacing; `vis` stays 1 |
| idle / cruise | v1 f0330, v4 f0600 | bob, halo spin, gyroscope, drill spin, pendulum sway, slow yaw |
| 일점 상쇄 (폭격) + slam | nose-down flight, ports hot, face-down core + column, plunge (v1 5.75–10.6 s) | root pitch, y plunge, slit look, eye aim, column |
| 코어 (레이저 빔) | medallions drop and counter-orbit with beams (v1 13.9–22.6 s) | medallion orbit, beams (length, aim, look) |
| 바위 폭탄 (미사일) | spike tips flare, eye up + vent column (v1 25.7–29.3 s) | eye aim up, column up, slit hot; missiles are fx |
| 감소 영역 (바닥 뜯기) | gyroscope lock, link beams (v3 2.2–15 s) | arch lock, medallions to ±3.85, beams |
| 파쇄 (바위 날리기) | dip, vent, tower, flame band, throws, revert (v3 17–25 s) | tower parts, halo scale, spike tilt, iris flip, root dip/roll |
| field start / 역장 생성 | halo flip, warp, unfold, violet (v1 31.9–38.7 s) | `vis`, halo flip, field spacing, looks |
| 인력 충격파 ×3 (and ×3 below 50 %) | charge sphere, beam, burst, 3rd drop (v2 16.5–26.3 s) | core_glow, column, y drop with stack compression |
| 지면 충격 (중력 폭발) | core lift, three spikes up, up-beam, column (v4 2.55–6.5 s) | §5.3 |
| release → groggy → recover | bubble burst, tilt, wobble, flip to the top (v2 11.9–14.97 s) | root roll, core_glow, flip |
| deploy / pack | lances out, then the roll (v2 26.3–30.3 s) | spikes + medallions far out, root rocks |
| death (proposed, §9) | — | every part drops and spreads, `vis` |

## 7. Display entities and construction plan (28 parts, budget 32)

### 7.1 Rules (from the shared libraries)
* All parts are `minecraft:item_display` with `item_display:"none"` and an `item_model` from a new
  `rlk:mboss/breguet/*` set. Textures go in `assets/rlk/textures/mboss/breguet/` and are registered in the items atlas.
* `mboss_model_lib.mjs` limits:
  * coordinates −16..32, so the reach from the pivot is ≤ 24 units = 1.5 x scale blocks (`checkBounds`);
  * element rotations single-axis, ±22.5/±45° (`rotM`);
  * right-side models are `mirrorModel` copies, never negative scales.
* The parts follow the anchor with `tp`, `teleport_duration` 1. The clips are compiled by `createRigCompiler`
  (`mboss_rig_compile.mjs`): one key per interpolation segment, ≤ 120° per tick and per segment.
* Fixed UUIDs follow the butterfly pattern: `524c4b4d-4252-4c00-8000-0000000000NN`
  (`[I;1380731725,1112689664,-2147483648,NN]`; 0x4252 = "BR").
* Tags: `rlk_room`, `rlk_mb_aux`, `rlk_mb_part`, `rlk_mb_breguet_part`, `rlk_mb_br_<part>`.
* Objectives: `brRigC/T/F/Y`, plus `brRigForm` and `brRigLook`.
* Functions: `rlk:mboss/breguet/rig/...`. Generator: `tools/build_mboss_breguet_rig.mjs` with `breguet_paint.mjs`,
  `breguet_geometry.mjs`, `breguet_pose.mjs` and `breguet_clips.mjs`.
* Culling: the ring and the tower tiers are 7 b wide, so give every part `width:8, height:8` (the ring 10) and
  `view_range` 3.

### 7.2 Part table
Pivots are offsets from the ring centre in the cruise form (§8 has the other forms). "units" is the farthest model point
from the pivot. Schematic: `08_rig_breakdown.png`. Data: `model_work/rig_plan.json` (`model_tools/rig_plan.py`).

| NN | part | models (looks) | build | scale | units | pivot (cruise) | bright | motion |
|---|---|---|---|---|---|---|---|---|
| 01 | `ring` | ring | 16-segment annulus (§7.3): band facets, top/bottom faces, inner wall, 32 teeth, lower tier, keystone T block + bell, port discs | **2.4** | 23.3 | (0,0,0) | 14 | root only |
| 02 | `ring_glow` | slit_idle / slit_hot / slit_off | emissive strips 0.02 b proud of the band seam (16 facet cards), port and bomb-port rim cards | 2.4 | 23.5 | (0,0,0) | 15 | look swap |
| 03 | `hub_eye` | iris_shut / iris_open / iris_hot | iris card stack (frame, fan or eye) facing −Z + 8-facet gold spike along −Y | 1.0 | 20.8 | (0, 0, −3.45) | 14 | flip 180° about Z; look |
| 04 | `halo` | halo / halo_violet | lathe outer + inner walls (16 facets) + annulus cards top/bottom, 10 joint marks | 1.25 | 20.0 | (0, 1.6, 0) | 14 | **spin 2.25** |
| 05 | `halo2` | halo2_gold / halo2_violet | translucent annulus card + thin lathe wall | 1.0 | 19.2 | (0, 1.35, 0) | 15 | **spin −4.5** |
| 06 | `core` | core | `knob()` sphere (12 bands x 16 facets, polar shell), pads, Y bracket, stud | 1.0 | 20.8 | (0, 0.1, 0) | 13 | keyed |
| 07 | `core_eye` | eye_idle / eye_charge / eye_field / eye_dim | 3 stacked cards at the sphere surface (z −1.3 b); pivot = core centre | 1.0 | 22.4 | = core | 15 | keyed aim |
| 08 | `core_arch` | arch | lathe about Z: bronze outer + red inner walls, 12 clamp boxes | 1.1 | 21.8 | = core | 13 | gyroscope (keyed) |
| 09 | `core_brim` | brim | 2 annulus cards (brim, tilted 22.5° in-model) + wire ring card with bead | 1.3 | 22.8 | = core | 14 | **precession 4.5** |
| 10 | `core_glow` | glow_charge / bubble_0..3 / bubble_burst / glow_gold | 3 crossed + 2 tilted translucent radial cards | 1.0 | 22.4 | = core | 15 | scale + look |
| 11 | `spike_l` | spike | 8-facet gold cone (lathe n 8) + collar (n 16) + shaft + X frame cards | **1.3** | 23.4 | (3.5, 0, 0), tip +X | 14 | keyed (dock/roll/detach) |
| 12 | `spike_r` | spike_r (mirrorModel) | mirror | 1.3 | 23.4 | (−3.5, 0, 0) | 14 | keyed |
| 13 | `medal_eye` | medal_eye / medal_eye_hot | lathe drum n 16 (teeth boxes) + face cards (C-ring, spiral) | 1.0 | 8.8 | (3.3, −0.35, 0) | 14 | **spin 4.5**; orbit |
| 14 | `medal_gear` | medal_gear / medal_gear_hot | 2 crossed cog cards + lathe rim + hub card | 1.0 | 8.8 | (−3.3, −0.35, 0) | 14 | **spin −6**; orbit |
| 15–18 | `drill_fl`, `drill_fr`, `drill_bl`, `drill_br` | drill | `turned()` profile (cap, gear disc with tooth boxes, collar, striped cone), n 16 | 1.0 | 10.4 | r 2.95 at ±45° / ±135°, y −0.95 | 14 | **spin 11.25**; orbit |
| 19 | `plate` | plate | annulus cards (top/bottom) + lathe rim with the groove | 1.25 | 18.6 | (0, −1.5, 0) | 14 | keyed, scale 1 → 1.4 |
| 20 | `plate2` | plate2 | as plate, smaller | 1.25 | 14.7 | (0, −1.62, 0) | 14 | keyed |
| 21 | `pendulum` | pendulum | cog (crossed cards + thin box), spindle box, arc (3 stacked semicircle cards), dagger (lathe n 4); pivot at the hang point | **1.6** | 21.0 | (0, −1.85, 0) | 14 | keyed sway, 2–4 t lag |
| 22 | `pend_glow` | ousia | translucent violet flame cards around the cog + short column | 1.6 | 9.0 | = pendulum | 15 | scale |
| 23–24 | `beam_l`, `beam_r` | beam_gold / beam_link | 2 crossed translucent cards, 1 b long along −Y from the pivot | 1.0 | 16.0 | at the medallions | 15 | scale (length in Y) + aim |
| 25 | `column` | col_gold / col_violet | 2 crossed translucent cards, 1 b along −Y (flip for up) | 1.0 | 16.0 | = core | 15 | scale (length) |
| 26 | `tower_col` | tower_col | turned column n 16 + block boxes; pivot at the base | **2.0** | 21.6 | hidden at (0, −0.3, 0) | 14 | keyed telescope |
| 27 | `tower_t1` | tower_t1 | annulus cards + lathe rim | 1.3 | 22.8 | hidden | 14 | keyed + spin 3 |
| 28 | `tower_t2` | tower_t2 | annulus cards + glowing rim lathe | 1.4 | 22.3 | hidden | 15 | keyed + spin −3 |

* **Spare budget: 4.** The best uses, in order:
  1. a `flame` band card for 파쇄, if the fx kit cannot follow the device;
  2. a separate `hub_spike`, if the iris and its spike must move apart;
  3. a second core glow shell for a double-layer bubble;
  4. a warp-pillar card.
* **Hidden parts**: scale 0, kept in place (like the butterfly's wings in human form).
* **Brightness**: the solid parts are 13–14, so the cream stays cream in the plaza's light; the glow parts are 15.

### 7.3 Rings as segmented models (how to build each one)
* **Main ring** (scale 2.4, so 1 u = 0.15 b and R = 23.3 u):
  * 16 segments, one every 22.5°.
  * Each segment is a box spanning r 17.5–23.3 u and y −2.3…+2.3 u, with its outer face as the band facet. It is built at
    azimuth 0 and turned with a single-axis Y rotation (0, ±22.5, ±45, plus the box re-oriented for 67.5/90), exactly as
    `lathe()` places its facets. The un-rotated `from`/`to` stay within −16..32.
  * Adjacent boxes overlap in a wedge at the inner edge. **Offset the top and bottom faces of odd segments by 0.04 u** to
    avoid z-fighting, or make the top faces separate `faceEl` quads per segment.
  * The **band texture must repeat per facet**. `lathe()` maps one sprite around the whole circumference, which would need
    16 x 96 px > 512. Add a `latheTile` variant (u = 16·(0.5 + rel·t / w)) so that every facet shows a whole tile. Design
    the tile so that its square wave is continuous across the edges, with 2 waves per tile.
  * Add an inner wall: `lathe` with inward faces, a 3-line variant using `faceOfDir(−d)`.
  * Add 32 raised tooth boxes on the top edge (2 per segment), the lower tier as 16 narrower boxes (r 15.5–21.3 u,
    y −2.3…−4.3 u), and the keystone T block (6 boxes) at azimuth 180° (back).
  * The front keystone is a socket only; the iris is part 03.
  * Ports are small discs (`disc()`) on the top and bottom faces.
  * Expect about 120 elements.
* **ring_glow**: the same 16 facets as single cards 0.1 u outside the band (seam strip texture with alpha), plus 2 port-rim
  and 8 bomb-port-rim cards. It is a separate display because brightness is per entity.
* **Halo, halo2, plates, tower tiers, brim**: these are thin flat rings. Build each one as **annulus cards** (`cardY`
  top + bottom, alpha ring texture, perfectly round from above and below) **plus a 16-facet lathe wall** (outer, and inner
  where thick enough), so that they also read edge-on. This is the butterfly's `ring` model recipe
  (`butterfly_geometry.mjs`: a `cardY` annulus plus a thin lathe band).
* **Arch**: lathe about Z (a vertical ring): 16 outer facets with the bronze tile, 16 inner facets with the red lining, and
  12 cream clamp boxes straddling it.
* **Spheres and cones**: use `knob()` for the core sphere, `turned()` for the drill pods and the tower column, `lathe(n 8)`
  for the spike cones (alternate the facet colours in the tile) and `lathe(n 4)` for the dagger.

### 7.4 Textures (`breguet_paint.mjs`, built on `mboss_paint_lib.mjs`)
* There are about 66 sprites, **≈ 0.34 M atlas px** in all; the butterfly uses 1.06 M of the 2 M budget, if the budget is
  shared.
* Paint at 64 px/b or more for anything seen at melee range. The sprites are alpha-cut at 0.5; the glow sprites use
  `paintT`. Use the `Grid` SDF painter, `bevel`, `litAt` (light from the upper left) and `tone()` ramps from §4.

| sprite | size | notes |
|---|---|---|
| `br_band` | 96x48 | upper cream / lower bronze with the square-wave joint (2 waves), dark seam groove, block joints, wear |
| `br_top`, `br_inner`, `br_tier`, `br_tooth` | 64x64, 64x32, 64x32, 32x32 | top panels with brackets; pale inner wall; ribs + dark slots; tooth caps |
| `br_keystone`, `br_bell` | 64x64, 32x32 | cream blocks; stepped bronze |
| `br_slit_idle` / `_hot` / `_off` | 64x16 each | the seam strip, emissive |
| `br_port`, `br_bombport` | 32x32 | dark-red centre with an orange rim; gold rim, dark core |
| `br_iris_shut` / `_open` / `_hot` | 64x64 | sunburst fan; cream ring + red pupil; white-gold |
| `br_gold_facet`, `br_collar`, `br_xframe` | 64x64, 64x32, 64x64 | alternating facets; ribbed rings; 4-prong frame with a dark-red ring |
| `br_shell`, `br_pad` | 128x64, 32x32 | plum shell with bronze meridian ribs (polar wrap); red cushion |
| `br_eye_idle` / `_charge` / `_field` / `_dim` | 64x64 | gear frame + glow ring + pupil + orange streak (the icon is the target) |
| `br_arch_out`, `br_arch_in`, `br_clamp` | 128x16, 128x16, 16x16 | bronze with tick marks; dark-red lining; cream clamp |
| `br_brim`, `br_wire` | 128x128 each | grooved annulus with rim ticks; thin ring with the bead |
| `br_glow_charge`, `br_bubble0..3`, `br_bubble_burst`, `br_glow_gold` | 64x64 each | translucent radial glows; bubbles with 0–3 crack networks |
| `br_halo_*`, `br_halo2_*` | 128x16 walls, 128x128 annulus | copper with joints / violet; gold / violet glow rings |
| `br_medal_eye(_hot)`, `br_medal_gear(_hot)`, `br_medal_rim` | 64x64, 64x16 | C-ring face + spiral; 12-tooth gear + glowing hub |
| `br_drill`, `br_drill_top` | 128x64, 32x32 | profile wrap: cap, gear teeth, glowing collar, striped cone |
| `br_plate_top`, `br_plate_rim`, `br_plate2_top` | 128x128, 128x16, 96x96 | bronze annulus; glowing groove |
| `br_cog`, `br_cog_side`, `br_arc`, `br_dagger`, `br_ousia` | 64x64, 32x32, 128x64, 64x32, 64x96 | silver cog with keyhole; protractor with ticks; gold facets; violet flame |
| `br_beam_gold`, `br_beam_link`, `br_col_gold`, `br_col_violet` | 32x64, 32x64, 32x128, 32x128 | translucent, fading to alpha 0 at the long edges |
| `br_tower_col`, `br_tower_t1`, `br_tower_t2`, `br_tower_rim` | 128x64, 128x128, 128x128, 128x16 | cream blocks; dark disc; gold-edged disc |

### 7.5 Looks (item-model swaps; discrete clip channels, as the butterfly's `wlook`)

| look | values | parts | use |
|---|---|---|---|
| `slit` | idle / hot / off | `ring_glow` | hot = charges, bombs, missiles, the field; off = dormant, groggy, death |
| `iris` | shut / open / hot | `hub_eye` | — |
| `eye` | idle / charge / field / dim | `core_eye` | — |
| `glow` | charge / bubble_0..3 / burst / gold | `core_glow` | the module sets `brRigCrack` = hits / 5 (0–3) and `look_apply` re-applies it, like the butterfly's `bfRigLook` |
| `field` | normal / violet | halo, halo2 | `pend_glow` is shown by scale |
| `medals` | idle / hot | `medal_eye`, `medal_gear` | — |
| `beam` | gold / link | `beam_*` | — |
| `col` | gold / violet | `column` | — |

### 7.6 Spinning versus keyed parts, and the cost
* Every motion is baked into the clips. The compiler places a key only where the client's lerp/slerp drifts. A constant
  spin about a fixed axis needs one key per ≤ 118° of rotation.
* With the rates of §5.1 an 80 t idle loop costs:

  | part | turn per loop | segments |
  |---|---|---|
  | halo | 180° | 2 |
  | halo2 | 360° | 4 |
  | brim | 360° | 4 |
  | each drill pod | 900° | 8 |
  | medal_eye | 360° | 4 |
  | medal_gear | 480° | 5 |

  That is under 60 part keys per 80 t on top of the bob.
* **Loop and clip-boundary rule.** A spinner must end every clip on a multiple of its symmetry step, so that the next clip's
  3 t blend never unwinds a spin:

  | part | symmetry step |
  |---|---|
  | halo | 36° (10 joints) |
  | drill pods | 45° (8 teeth) |
  | gear medallion | 30° |
  | eye medallion, brim, inner ring | 360° (asymmetric) |

  Author the spin as `angle = t · k·step / L`, with `k = round(ω·L / step)` per clip. For example, the drill pods at
  11.25°/t over L = 80 give exactly 20 steps.
* Keyed (non-cyclic) motion: the root, the stack spacing, the core group, the spike rolls, the medallion and drill orbits
  (per clip), the beams, the tower and the pendulum lag.
* **Tolerances** (`TOL.r`, degrees): the ring is 7 b wide, so 1° moves its rim 6 cm.

  | part | tolerance |
  |---|---|
  | ring, ring_glow | 0.25 |
  | halo | 0.4 |
  | spikes | 0.4 |
  | pendulum | 0.5 |
  | beams | 0.3 |
  | core group | 0.5–0.6 |
  | the rest | 1.0 |

  `TOL.t` 0.012 b and `TOL.s` 0.015, as for the butterfly.
* **Pose channels** (proposed `DEFAULT_POSE`):

  | channel | values | meaning |
  |---|---|---|
  | `pos` | [0, y, 0] | ring centre |
  | `rot` | [p, y, r] | about the ring centre |
  | `vis` | number | scale of everything about the ring centre |
  | `halo` | {o, e, s} | halo offset, rotation, scale |
  | `halo2` | {o, s} | inner ring offset, scale |
  | `hub` | 0…180 | iris spike roll |
  | `core` | {o, e} | core group offset, rotation |
  | `eye` | [yaw, pitch] | aim on the sphere |
  | `arch` | [p, y, r] | plus the gyro phase |
  | `brim` | tilt [p, r] | — |
  | `glowS` | number | glow sphere scale |
  | `spikeL`, `spikeR` | {o, e} | paired, mirrored as in `butterfly_pose.mjs` |
  | `medE`, `medG` | {o, e} | — |
  | `drill` | {r, y, az, s} | shared, with per-pod overrides |
  | `plate`, `plate2` | {y, s} | — |
  | `pend` | {y, swing [p, r]} | — |
  | `pglow` | number | Ousia glow scale |
  | `beamL`, `beamR` | {len, w} | — |
  | `col` | {len, up 0/1} | — |
  | `tower` | {ext 0..1, t1, t2} | — |

  Discrete: `slit`, `iris`, `eyelook`, `glowlook`, `field`. Sampler phase: `ph` (the spins).

### 7.7 Hit volume and anchors (for the module)
* The device has no body to hit except the **core** and, in cruise, the hanging **lower stack**.
* Proposal: a click shield or interaction on the core centre (w 2.6, h 2.6), moved per form from the manifest anchors, and a
  second one on the plate and pendulum (w 1.4, h 3.0) for ground melee in cruise. The 20-hit meter counts hits on either
  while the field is up (cap 1 per 4–5 t; see v2.md §5).
* Manifest anchors per event (rig coordinates, as the butterfly's `anchors`):

  | anchor | used for |
  |---|---|
  | `core`, `eye` | column origin |
  | `spike_tip_l/r` | missile tip flares |
  | `medal_e`, `medal_g` | laser muzzles |
  | `beam_spot_l/r` | floor spots |
  | `port_0..7` | bomb drops |
  | `vent_l/r` | missile launches |
  | `pend_tip`, `ring_centre`, `tower_top` | — |

## 8. Rest poses per form (offsets from the ring centre, b; H = ring-centre height)

| part | DORMANT H 2.15 | CRUISE H 4.5 | FIELD H 5.8 | CORE-UP H 5.0, roll 10° | TOWER H 4.5 | LASER H 4.5 | DEPLOYED H 5.6 |
|---|---|---|---|---|---|---|---|
| halo | scale 0 at 0 | +1.6, spin | +1.55 violet | +1.6 | +3.2, scale 1.7 | +1.6 | +1.55 violet |
| halo2 | scale 0 | +1.35 gold | +1.3 violet | +1.35 | +2.5 | +1.35 | +1.3 violet |
| hub_eye | shut, spike down | shut/open, spike down | open | open, **spike up** | **spike up** | open | open |
| core group | 0, arch flat | +0.1, arch rocking | −1.96, eye out | **+2.8**, arch upright | −0.4 | +0.1 | −1.96 |
| spikes | horizontal | horizontal | horizontal (orbit out in the charge) | at (±3.6, +0.9), **vertical up** | tilted **up 45°** | horizontal | **(±5.6, −0.6)**, down then horizontal |
| medal_eye / medal_gear | docked (±3.3, −0.35) | docked | **(±3.85, −1.96)** + link beams | (±3.6, +0.3), facing forward | on the column top (±0.5, +3.6) | **r 2.8, y −2.0, counter-orbit 5°/t** | in the spike X frames |
| drill pods | r 3.2, y −0.45, scale 0.7 | r 2.95, y −0.95 | r 3.5, y −1.9, orbit 1°/t | r 2.4, y −1.0 | r 2.95, y −0.95 | as cruise | r 3.8, y −1.2 |
| plate / plate2 | −0.55 / hidden | −1.5 / −1.62 | −3.22 (×1.4) / −2.8 | −2.95 / −2.75 | −1.9 / −1.75 | as cruise | −3.0 / −2.6 |
| pendulum hang | +0.12 (only the dagger shows) | −1.85 | −3.4 (violet) | −2.6 (violet) | −2.2 (violet) | −1.85 | −3.2 |
| tower | hidden | hidden | hidden | hidden | col out, t1 +1.35, t2 +2.0 | hidden | hidden |
| looks | slit off, iris shut | slit idle | slit hot, violet, bubble | slit hot, iris hot | slit hot | medals hot, beams gold | slit hot |

* Pendulum tip over the floor: 0.2 (dormant), 0.58 (cruise), 0.33 (field), 0.33 (core-up), 0.23 (tower).
* The core-up hang point puts the tip at 0.33 b. It is drawn with the plate just above the pendulum, as in v4 f0210.

## 9. Not visible in the footage (proposed)

* **Groggy** (after the 20-hit release). v2 shows only a 2 s stagger.
  * Proposal: hold a **slumped pose** for the design length (e.g. 100–160 t):
    * ring centre 3.0 b, root roll 25° + pitch 8°;
    * `slit` off, eye dim, iris shut;
    * halo slid 0.6 b sideways and tilted 30°;
    * drill pods hanging 0.3 b lower and spinning at a quarter speed;
    * pendulum swinging freely ±12° over 40 t;
    * medallions sunk beside the core;
    * a slow ±3° wobble.
  * Then **recover**: re-level 6 t + flip to the top 9 t.
* **Death**:
  * the seam flickers off (slit hot/off alternating 3×), the eye fades;
  * the halo drops and rolls off;
  * the drill pods stop and fall;
  * the spikes droop 45°;
  * the ring tilts 40° and sinks to the floor (ring centre 0.6 b) over 40 t;
  * the medallions clatter down beside it;
  * then `vis` scales out with gold sparks (fx).
* **Back view**: the back keystone (T block + bell) faces backward. Otherwise the device is radially symmetric; the iris is
  the only front marker.

## 10. Rejected alternatives

* **The ring as `block_display` cubes** (v2.md hint: 32 copper/sandstone blocks). That is 32+ entities and the square-wave
  seam cannot be painted; one 16-segment item model with a tiled painted band is 1 entity.
* **Splitting the ring into 2–4 displays.** It never deforms. Its "spring" spread in the field is the plates and the core
  moving apart, not the ring.
* **One display for the core** with the eye and arch inside it. The arch must spin about a horizontal axis while the eye
  aims independently, and the glow needs brightness 15. Four displays (sphere, eye, arch, brim) + the glow shell is the
  minimum.
* **Particles for the lasers and link beams.** They must follow the counter-orbiting medallions exactly. As rig parts the
  compiler keeps them aligned for free.
* **Treating the keystone eye as the core.** It contradicts v2 f1020, where both are visible at once (§0).

## 11. Open checks for the builder

* Confirm D = 7.0 b in the arena: the ring centre at 5.8 b in the field and the tower top at 8 b. Check them against the
  arena walls and the third-person camera.
* The 8-facet spike lathe with alternating facet colours needs the tile split per facet (`latheTile`). Check that the
  facets read as faceted, not banded.
* The z-fighting of the overlapping ring segments (§7.3) must be checked in game, from above at a grazing angle.
* Translucent glow shells and the bubble cards must stay inside the sphere's depth order. Keep the alpha at 0 at the sprite
  borders (the butterfly overlay rule).
* Which medallion docks on which side is arbitrary (they orbit and swap). Keep the eye medallion on +X in cruise, as in the
  PDF.
* The arch's free rotation direction and rate are rough (one face turn every 0.5–1 s in v3). Tune them by eye.

## 12. Annotated sheets in `understand/model/`

| file | content |
|---|---|
| `01_ref_parts_annotated.png` | PDF render with all 23 parts numbered, a legend and sizes in D |
| `02_forms_and_states.png` | 12 forms/states from my own frames: dormant, unfold, cruise, compact front, arch upright, field, release tilt, deployed lances, core-up, laser, top view, grounded |
| `03_proportions_measured.png` | cruise (v1 f0330) and field (v1 f2160) broadsides with measurement lines in D and blocks, plus the scale decision table |
| `04_core_and_eyes.png` | icon, PDF core, field eye, exposed core, charge sphere, release bubble, core-up, keystone iris |
| `05_ring_spikes_pods_pendulum.png` | top views, PDF band halves, spike + mount, drill pods and medallions, lance, pendulum, Ousia glow |
| `06_motion_strips.png` | 6 time strips with tick offsets: entrance, core flip-up, release + flip to the top, laser, pack-up roll, bomb run + slam |
| `07_palette.png` | recommended ramps per material and per glow look, with the sampled evidence |
| `08_rig_breakdown.png` | the 28-part rig on a 1-block grid with the 1.8 b player: cruise, field, core-up and tower elevations, top view, part legend |
| `09_best_reference_frames.jpg` | the 20 best frames (below) |
| `guide-1.png`, `guide-2.png` | 300 dpi page rasters of the PDF |

### 12.1 Best reference frames

| view | frames |
|---|---|
| every part, clean | **PDF render** (`model_work/pdf/img-001.png`); icon `img-000.png` (core eye) |
| cruise broadside / proportions | **v1 f0330** (5.50 s); dormant v1 f0000; unfold v1 f0150 |
| compact front, keystone iris | **v4 f0600** (10.00 s); v2 f1020 (iris + hanging core together) |
| compact, arch upright | v2 f0870 (night), v2 f1812 / f1860 (day, sunburst fan) |
| field | **v1 f2160** (broadside), v1 f2040 (unfolding, spring spread), **v3 f0600** (close: core, link beams, plate annulus), v2 f0000 (medallion faces) |
| top view | **v3 f0945**, v3 f0930 |
| lances | v2 f1704 (horizontal), v2 f1668 (vertical) |
| core-up | **v4 f0210**, strip v4 2.50–4.95 s |
| tower | **v3 f1510**, v3 f1180, v3 f1140 (medallions docked on top) |
| laser | v1 f1032, strip v1 13.95–17.8 s |
| underside, pendulum, bombs | v1 f0480 |
| release / bubble | v2 f0718–f0735 |
| missiles / vent shaft | v1 f1584 |
| grounded | v2 f1586 |
| cruise close at dusk (halo + inner glow ring) | v3 f1770 |
