# 아펩의 오아시스 파수꾼 — motion and skeleton study (chapter-3 boss)

Scope: skeleton, secondary motion, every boss motion (key poses, tick timings, root travel, joints,
anticipation / impact / settle), the phase-2 organisms' simple motions, and a proposed clip list in the
`tools/mboss_rig_clips.mjs` format (`{name, len, loop?, next?, blend?, keys:[[t,pose,ease]], events, note}`, sparse keys
over a default pose, ease `io` default / `i` strike-fall / `o` settle-leap / `l` linear spin, `blend` default 3 t,
optional `hidden:[a,b]`, discrete `forms:[[t,'look']]`, overlays as in `fieldgen_clips.mjs`).

Ticks are 20 t/s. "P+n" = ticks after the pattern start P0 given in each section. Sizes: 1 m = 1 block (model study
decision, `model/07_proportions_measured.jpg`). Binding stats are in `src/wiki.md` (RES: boss Dendro 30 % / others 10 %;
organisms Dendro 20 % / others 10 %; 양육 buff = all RES +9900 %, a mechanic: buffed basics cannot be damaged).

## 0. Sources, confidence, sheets

| source | what it gives | used for |
|---|---|---|
| `understand/v1.md` (analyst) | v1 frame-accurate: entrance, 잠복 돌진, crawl, 생명의 손, 발광 slams 1-2, sizes | P1 |
| `understand/v2.md` (analyst) | v2: 발광 slam 3, burrow-relocate, 초목이 시든 풍경, walk, 생명의 꼬리 (P1, 2 sweeps), 근접 콤보 (4 hits), phase-2 opening | P1, P2 entry |
| `understand/v4.md` (analyst) | organisms: guarding, nesting walls, destruction roll/blast, predatory swallow/bud/pod/bites, Heart bar maths | organisms |
| `understand/v5/*` sheets + `v5/events.txt` (no report yet) | P2 end, in-game revival cut-scene, P3 이동 돌진, 종말의 여파 (광역 공격), 증폭의 풀 (3연속 포격) | P3 |
| `understand/v6w/*` sheets + `v6w/events.txt` | v6: 이동 돌진 burst (take 1), P3 tail ×2 (take 2), 생명의 나선 (take 3); w1 종말의 여파; w2 revival cut-scene | P3 |
| `understand/v3/*` sheets | basic organism ranged shot, nurturing tethers, guarding shield cast, spawn | organisms |
| `understand/model/01..08` | part names (numbers ①..㉒ for P1, 50..74 for P3), proportions | skeleton |
| my own dense sheets (deleted after use) | cross-checks of all the above | — |

Not in any footage: the boss going underground at < 1 % (cut out of v2), the death, a 2- or 3-hit combo (only 4 hits
seen), the phase-1 single-sweep tail (both P1 and P3 footage show 2 sweeps), the third shell of 증폭의 풀 (one splash
seen right after shell 2). These are marked **[proposal]** below; everything else is **[seen]** with the frame times.

Key-pose sheets (every cell labelled with pose, video, time, source frame and P+tick), all in
`understand/motion/`, rebuildable with `understand/motion_tools/keypose.py` (`jobs | xargs -P4 … grab`, then `assemble`):

| sheet | content |
|---|---|
| `kp01_p1_idle_turn_walk.jpg` | P1 idle crouch (front/side), pivot turn, spider crawl, half-stand, side-walk |
| `kp02_p1_burrow_strike.jpg` | 잠복 돌진 (v1) + burrow-relocate onto the player (v2) |
| `kp03_p1_hands.jpg` | 생명의 손 |
| `kp04_p1_glow.jpg` | 발광하는 파수꾼 (travel, wind-up, 3 slams) |
| `kp05_p1_rotation.jpg` | 초목이 시든 풍경 |
| `kp06_p1_tail.jpg` | 생명의 꼬리, phase 1 |
| `kp07_p1_combo.jpg` | 근접 콤보, 4 hits |
| `kp08_p2_enter_end.jpg` | phase-2 opening (Heart lowered and dropped) and phase-2 end |
| `kp09_cutscene_w2.jpg` | 2→3 revival cut-scene (wiki clip) |
| `kp10_cutscene_v5.jpg` | in-game revival cut-scene + phase-3 fade-in |
| `kp11_p3_move.jpg` | 이동 돌진 (v5) + the v6 take-1 burst |
| `kp12_p3_tail.jpg` | 생명의 꼬리, phase 3 (2 swings) |
| `kp13_p3_spikes.jpg` | 생명의 나선 |
| `kp14_p3_shells.jpg` | 증폭의 풀 |
| `kp15_p3_aftermath_w1.jpg` | 종말의 여파 (wiki clip) |
| `kp16_p3_aftermath_v5.jpg` | 종말의 여파 in game |
| `kp17_organisms.jpg` | basic spawn / ranged, nurturing tethers, guarding cast + death, nesting flap / loop / walls, destruction fuse / blast, predatory swim / swallow / bud / pod / burst / bites |
| `ov/*.jpg`, `seg/v1_a_intro.jpg` | 1–2 fps overviews from the earlier attempt (kept) |

## 1. Scale and silhouettes

| | phase 1 종막 (dark slate + pale bark) | phase 3 기원 (lime + bottle-green) |
|---|---|---|
| stance | low **six-limbed crouch**: hood forward, 2 elephant forelimbs (pair B) and 2 hind legs (pair C) on petal feet, 2 long leaf-arms (pair A) planted far out to the sides, tail on the ground behind | **tall upright serpent**: trunk out of the ground, S-curved spine, hood on top, leaf-arms (A) held out in a T, the 4 lower leaf hands (B, C) spread on the ground like a skirt, ribbon tail coiled behind |
| height | hood top 4.3 (crouch), crown tip 4.7, half-stand 4.7–5.1, rear-up 7–8, mantle-flower 9.3, spiral column 8–9 | hood top ≈ 7 (5.5–9), arms-up V ≈ 9 |
| width / length | outer hand span 8–11; nose→tail ≈ 13–16 (body ≈ 8–10, tail ≈ 6–7) | leaf-arm span 8–10; lower leaf hands 2.5–3 each; tail ≥ 8 |
| hands | petal foot ≈ 1.5–2.0 across, 4–5 petals 0.7–0.9 × 0.4; gold cone 0.3 on the back | leaf hands 2.5–3, paler cones |
| other | mantle leaf 4.5–5 × 2–2.7; core window 1.2–1.6 under the hood | hair strands to the waist; face rosette on the hood |

Movement character: P1 is a heavy **spider/crab** (crawls fast and low, 0.2–0.35 b/t; slow side-walk 0.1–0.15 b/t),
burrows head-first, attacks by rearing tall and crashing down. P3 is a **rooted serpent**: it rarely walks, it sinks
and travels under water/ground (leaf-pad trail), coils its body into hoops and S-curves, and casts from an upright T.

## 2. Skeleton

### 2.1 Joint tree (one rig for both phases; the phase is a look switch)

```
root (anchor; module position + yaw only)
└─ pelvis            y, pitch, yaw, roll      hip block / P3 trunk base
   ├─ legC_L/R       hip(p,y,r) ─ knee(p) ─ ankle(p) ─ petal foot (open 0..1)      hind legs
   ├─ tail1 ─ tail2 ─ tail3 ─ tail4(blade/tip)   each (p,y)
   └─ spine1 (p,y,r) ─ spine2 (p,y,r) ─ spine3 (p,y,r)      chest + shoulders + core window
      ├─ core         brightness channel (P1 glowing seed in the chest window; P3 navel glow)
      ├─ legB_L/R     shoulder(p,y,r) ─ elbow(p) ─ wrist(p) ─ petal foot        forelimbs ("elephant legs")
      ├─ armA_L/R     shoulder(p,y,r) ─ elbow(p,y) ─ claw/leaf tip(p)             long leaf-arms
      ├─ mantle_L/R   root hinge(p,y,r) [+ bend]                                   cloak leaves (secondary)
      └─ neck (p,y) ─ hood (p,y,r)                                                 head
         └─ drapes    hinge(p,r)                                                  hanging strips / P3 hair (secondary)
```

DOF notes: elbows/knees are single hinges (p) except `armA.elbow` (p,y) so a leaf-arm can sweep sideways; the spine
needs **3 segments** for the P3 S-curve, the hoop/wheel (`HOOP`, 3 × 60° pitch) and the 발광 spiral column; the
tail needs 4 segments for the S-raise and the helical sweeps. All yaw spins live on `pelvis` (the anchor never spins in a
clip).

### 2.2 Rest lengths (blocks) and pivots

| bone | P1 rest | P3 rest | notes |
|---|---|---|---|
| pelvis pivot height | 2.2 (crouch) | 1.8 (trunk base) | P1 sink goes to −3.5; leaps to +7 |
| spine1 / spine2 / spine3 | 1.4 / 1.4 / 1.2 | same | P1 pitched forward-up 15–25°; P3 vertical S |
| neck / hood | 0.6 / hood 2.5 long × 2.0–3.3 wide × 1.6 tall | 0.6 / hood 2.0 long, crest 1.0 | crown cone 0.8–1.0 on the hood |
| armA upper / fore / claw | 2.6 / 2.6 / 0.9 | same | reach 5–6; P1 idle hands planted at ±5 to the sides |
| legB upper / lower / foot | 1.8 / 1.8 / foot Ø 1.8 | same, laid out as skirt | 1.1 thick |
| legC upper / lower / foot | 2.0 / 2.0 / foot Ø 1.5 | same | |
| tail1..4 | 1.8 each (7.2) | ×1.15 (8.3) via the P3 model | blade 1.2 (P1 dark scythe), thin curved point (P3) |
| mantle_L/R | 4.5 × 2.2 panel | lime leaf blades | hinge on spine3 behind the shoulder |
| drapes | 3.0 strips | 3.5 hair strands | hinge under the hood rim |

### 2.3 Part budget (item_display, fixed UUIDs, `teleport_duration 1`)

| group | parts | count |
|---|---|---|
| body | pelvis, belly shell, spine1, spine2, spine3 (shoulders + gems + back crystals), core | 6 |
| head | neck, hood (dome + crown cone), face (P1 face plate / P3 crest + rosette) | 3 |
| armA ×2 | upper, fore-leaf, claw/tip | 6 |
| legB ×2 | upper, lower, petal foot | 6 |
| legC ×2 | upper, lower, petal foot | 6 |
| tail | tail1, tail2, tail3, tail4 (blade/tip) | 4 |
| secondary | mantle_L, mantle_R, drapes (one double card) | 3 |
| **total** | | **34** (+3 optional: second mantle pair ×2, second drape card) |

Looks (discrete channel, item-model swap on all parts, no part-count change): `p1`, `p1_dark` (burrow, near-black
#2D2A04), `p1_brown` (root-chunk sink, #605D37 / #797745), `ghost` (dissolve-in, translucent), `p3`, `p3_lit` (yellow
charge glow for 증폭의 풀 / 생명의 나선), `withered` (death). `core` brightness is a separate discrete channel (0–15).

Props (separate entities, spawned by the pattern code at clip events): burrow pool decal, ground shadow (P1 travel),
gold ground glow, leaf-pad trail (P3 travel), 4 summoned legs (생명의 손; 3 item_displays each, reuse the legB models),
thorn wheels, rotation disc, shell target rings + beams, spiral spikes, domes and Dendro field (종말의 여파), Heart egg.

## 3. Secondary motion

| item | driver | parameters |
|---|---|---|
| mantle_L/R (P1 cloak leaves / P3 leaf blades) | pendulum sim (as fieldgen) on the spine3 motion + idle `osc` | idle ±4° pitch, period 40 t; lag 2–3 t behind spine3; damping 0.85; authored keys win in hands (cross, flower), glow (spiral), rotation |
| drapes / hair | pendulum sim, gravity down | swing lag 3–4 t; fling outward (+50–70°) during spins (rotation, whirl, hoop); P3 cut-scene "hair whip" = sim on the reveal |
| tail idle | travelling sine `osc` on tail1..4 yaw | ±6°, period 60 t, phase lag 8 t per segment; tail tip lifts +10° every other cycle |
| petal feet | discrete open/close via foot pitch + scale | planted = open flat; lifted ≥ 0.3 b = curl (scale y 0.8, pitch +25°) |
| core glow | `core` channel | idle 9↔12 over 60 t; wind-ups 15; burrowed 0; death flicker 15/3 every 2 t |
| spine breathing | `osc` | P1 spine2 pitch ±2° / pelvis y ±0.08 over 60 t; P3 spine yaw/roll ±3° with 6 t lag per segment (snake sway) |
| crystals, crown, gems | rigid | none |
| robe strips between the legs (P1 ⑮) | part of the drapes card or painted on the belly shell | — |

## 4. Rules for these clips (as in fieldgen / butterfly)

* **No horizontal root travel and no root yaw in clips.** The module moves the anchor: burrow travel (under the hidden
  window), the 잠복 lunge (≈ 0.55 b/t for 13 t), the combo leap (2–3 b), the 이동 돌진 wheel roll (3–4 b), crawl/walk
  loops (stride = speed × len). The module turns the anchor with face/track: **P1 ≤ 9°/t** (footage: 90° in 10 t,
  150–180° in 19 t), **P3 ≤ 6°/t** [proposal].
* **Vertical travel is in the clip** (`pelvis.y`): sinks to −3.5, burst rises, the 발광 leap (+7), the 종말의 여파 hover.
* **Spins end on whole turns**: 생명의 손 swirl 360°, rotation spin 360° (pelvis yaw), combo spin 360°, 종말의 여파
  whirl 360°, 이동 돌진 hoop roll 360° (pelvis pitch). Twists that are not spins (발광 spiral, tail whips) return to 0.
* Burrowed time uses `hidden:[a,b]` (hurtboxes off), and the module shows a prop (shadow / leaf-pad trail) instead.
* Phase/look changes through `forms`; the P1→P3 swap happens inside `revival` while the boss is hidden.
* Authored at footage speed. If the −25 % wind-up tuning of earlier bosses is wanted, use `retime` knots only on
  the long tells listed per clip (hands swirl, glow wind-up, rotation rear, combo rears, tail raise); never shorten the
  rotation disc fill below 23 t or the 종말의 여파 dome window.

## 5. Pose glossary (keys reference these names; angles in degrees, + pitch = forward/down, + yaw = left, + roll = left side up)

Only the joints that differ from `CROUCH` (P1) or `T` (P3) are listed.

| pose | pelvis y / p / yaw / roll | spine1-2-3 p | neck / hood p | armA (sh p, abd, el) | legB / legC | tail | mantle | core |
|---|---|---|---|---|---|---|---|---|
| **CROUCH** (P1 default) | 2.2 / −15 / 0 / 0 | 0, −5, −5 | +25 / +20 | +40, 70 out, 30 (hands planted ±5) | B straight (sh +10, el −20); C bent (hip −20, knee +50, ankle −30) | t1 +20 down, t2-4 −5, curved 10° yaw each | draped (+70) | 10 |
| CROUCH_IN (breath) | 2.12 / −14 | 0, −3, −3 | +27 / +22 | — | — | — | +72 | 12 |
| LOW (crawl) | 1.8 / −5 | +5, 0, 0 | +15 / +10 | +55, 80, 20 | B/C alternate lift 0.6 b | trailing straight | +80 | 9 |
| HALF (half-stand, core lit) | 2.9 / −35 | −10, −10, −5 | +10 / +5 | +20, 60, 40 hanging | C bent more (knee +70) | — | opened ±35 yaw | 15 |
| REAR (tell) | 2.9 / −45 | −15, −10, −10 | −10 / −15 | −60 (raised), 50, 20 | B lifted 0.5 | t1 +30 | lifted (+20) | 12 |
| DIVE (head-first) | 2.0 / +50 | +20, +15, +10 | +30 / +30 | +80 forward-down, 30, 10 | C pushes (knee +20) | t1 −20 up | +80 | 10 |
| SPLAY (sinking) | 0→−3.5 / +10 | +5, 0, 0 | +20 / +20 | abd 90 flat, 0 | B, C abd 60 flat, petals open | flat | flat (+90) | 4 |
| ERUPT (burst up) | 4.2 / −70 | −10, −5, 0 | −20 / −10 | −30 overhead back, 40, 40 | hanging (sh +60) | hanging down | up (−30) | 15 |
| LOOM (over the player) | 3.6 / +30 | +20, +15, +10 | +20 / +25 | −40, 60, 30 | B over the player (sh −30), C planted | t1 +10 | spread | 12 |
| LUNGE (sweep) | 1.5 / +75 | +5, 0, 0 | 0 / 0 | sweeps from −60 to +60 yaw at 0 height | B/C trailing (sh −60) | straight back | streaming (+90) | 12 |
| SPREAD | 2.6 / −25 | −10, −5, 0 | +5 / 0 | 0, 100 wide, 10 | — | — | ±60 yaw | 12 |
| OVERHEAD (hands up) | 3.4 / −55 | −15, −10, −10 | −10 / −15 | −150 (up), 20 together, 10 | C deep (knee +80) | t1 +30 | up | 15 |
| PLUNGE | 1.8 / +40 | +20, +15, +10 | +30 / +20 | +100 down, 20, 0 (claws 1.5 under ground) | B kneel (el +60) | — | flat | 15 |
| CROSS (upright on buried hands) | 3.0 / −50 | −10, −10, 0 | 0 / 0 | +60, 30, 0 (still buried) | C under | — | ±90 sideways (cross) | 12 |
| FLOWER (mantle raised) | 3.6 / −60 | −15, −10, −10 | −10 / −20 | −80, 40, 30 | C deep | t1 +30 | raised −80 (opening flower, 9 m) | 15 |
| COLUMN (spiral) | 4.5 / −80 | −5, −5, −5, twist yaw +60/+60/+60 | 0 / 0 | wound round the body (sh −120, abd −30, el 60) | C under, B lifted | wrapped (yaw +40 each) | wound up | 15 |
| SLAM | 1.6 / +45 | +25, +15, +10 | +30 / +25 | +110 (down), 30, 0 | B kneel | slapped down | flat | 15 |
| AIR (leap apex) | 7.0 / −20 | −10, −10, −10 | −10 / −10 | −60, 50, 40 | tucked (knee +90) | curled up (−30 each) | up | 12 |
| DIVEDOWN | 4.0 / +160 (inverted) | +10, +10, +10 | +20 / +20 | +180 (down past head), 30 | trailing up | trailing up | streaming | 15 |
| ARMSUP | 3.2 / −50 | −10, −10, −5 | −10 / −10 | −140, 60 out, 20 (hands 6.8 up) | — | — | up | 15 |
| LEAN (rear over the player) | 4.0 / −20 then +25 | −10, −5, +10 | +20 / +20 | −60, 70, 40 | C deep, B lifted | t1 +30 | spread | 15 |
| CRASH (sideways) | 1.2 / 0 / 0 / roll −80 | +5, 0, 0 | +10 / 0 | flung out (abd 110) | flung out | out | out | 12 |
| SPIN | = CRASH, pelvis yaw +360 linear | — | — | out | out | out (fling) | sim | 15 |
| SPRAWL | 1.0 / 0 / roll −30 | 0 | +10 | flat out | flat | flat | flat | 9 |
| TAIL_S (tail raised) | 2.4 / −10 | 0, 0, 0 | +20 / +20 | planted | planted | t1 −60 up, t2 +50, t3 −40, t4 +30 (S) | — | 10 |
| TAIL_COCK | 2.3 / −10 / yaw −35 | 0, 0, 0 yaw −10 each | — | planted | planted | t1 −40, yaw −60 / −30 / −20 / −10 | — | 10 |
| TAIL_WHIP | 2.2 / 0 / yaw +60 | yaw +10 each | — | planted | planted | t1 +5, yaw +70 / +40 / +30 / +20 (horizontal, 0.5–2 b high) | swing sim | 12 |
| SWEEP_ARM (combo 1) | 2.4 / −10 / yaw +40 | yaw +10 each | — | R arm: sh +60, abd 90, yaw from −90 to +60 at knee height | — | — | — | 12 |
| **T** (P3 default) | 1.8 / 0 | 0, −5, +5 (soft S) | 0 / +10 | sh 0, abd 90 (T), el 20 up, claw −20 | B/C as skirt: sh abd 80 flat, knee 0, feet flat at r 2.5–3 | coiled on the ground behind (yaw 40/40/40/40) | out sideways −60 | 10 |
| HUNCH (P3) | 1.6 / +20 | +20, +20, +15 | +20 / +20 | +40, 60, 60 (curled in) | skirt | — | down | 12 |
| MOUND | 0.4 / +30 | +40, +40, +30 | +30 / +30 | wrapped in (abd 20, el 100) | skirt folded up | tucked | down | 6 |
| HOOP / WHEEL | 2.0 / +60 | +60, +60, +60 (body a ring) | +60 / +40 | trailing | trailing | +40 each (closes the ring) | trailing | 15 |
| SCOIL (tall S) | 2.5 / −10 / roll +15 | −20, +25, −20 (S) | +15 / +10 | out (T), el 40 | skirt | lifted S behind (t1 −50, t2 +40) | out | 10 |
| CURL (P3 crouch) | 1.0 / +40 | +30, +30, +20 | +30 / +30 | wrapped in | skirt up | coiled tight (yaw 70 each) | down | 8 |
| V (arms up) | 2.0 / −5 | −5, −5, −5 | −15 / −15 | −150, 30 out (V), 10 | skirt | — | up −80 | 15 |
| BALL (shell launch) | 1.4 / +30 | +30, +30, +30 | +30 / +20 | wrapped (abd 10, el 120) | skirt up | tucked | wrapped | 15 |
| TALL | 2.4 / −5 | −5, 0, 0 | 0 / 0 | T, el 10 | skirt | coiled | out | 12 |

## 6. Motions

Each section: footage timeline (video time → P+ticks), then the clip design: key ticks with poses, root travel,
joints that do the work, anticipation / impact / settle, events.

### 6.1 Phase-1 idle, turn, crawl, walk  [seen; `kp01`]

* **Idle** (v1 11.0–15.1, 26.6–28.0; v2 2.25–4.6, 33.5–34.6): `CROUCH` breathing, hood slightly low, slow sway; core
  steady soft glow; mantle hangs. Clip `idle_p1` 60 t loop: `CROUCH`(0) → `CROUCH_IN`(30) → `CROUCH`(60).
* **Turn in place** (v1 15.10–15.60): ≈ 90° in 10 t, pivoting on the hands, body low. Module turns the anchor at
  9°/t; clip `turn_p1` 20 t loop gives the stepping: legB_L lift 0–5, legC_R 5–10, legB_R 10–15, legC_L 15–20 (lift
  0.5 b, petals curl), pelvis counter-roll ±4°, mantle lags.
* **Crawl reposition** (v1 15.60–17.00): low, fast spider gait with dust, 8–10 b in 28 t (0.3 b/t, peak 0.35), then
  slows 8 t and rises into `HALF` facing the player with the core lit (17.40–18.60). Clip `crawl_p1` 16 t loop
  (diagonal pairs B_L+C_R at 0–8, B_R+C_L at 8–16; stride 4.8 b at 0.3 b/t; arms A paddle forward alternately; tail
  trails straight), `crawl_stop_p1` 32 t (`LOW`→`CROUCH` 0–8, `HALF` 16–24, hold; core 15 at 16).
* **Walk** (v2 13.50–15.70): crab side-walk, hump 4.6 b, 0.1–0.15 b/t, thumps ≈ every 9 t. Clip `walk_p1` 36 t loop
  (C_L 0, B_L 9, C_R 18, B_R 27; stride 4.3 b at 0.12 b/t; side-walk = module moves the anchor sideways, the clip
  is direction-agnostic).

### 6.2 Phase-1 entrance  [seen, v1 0.00–5.37; not in the brief but needed]

Dark pool + crown spike 0–16 t; hood rises 16–31; stands and reaches up to the glowing bulb 31–60; flash 60;
embers 63–80; drops to `CROUCH` with a roar pose 91–107. Clip `entrance_p1` 110 t: `SPLAY` at y −3 (0) → hood out
(16, y −1.5) → `HALF` (31) → arm A_R raised to −150 (45–60) → flash event 60 → `REAR` (80) → `CROUCH` (100, `o`).
Untargetable throughout. `forms [[0,'p1_dark'],[30,'p1']]`.

### 6.3 잠복 돌진 (caption 잠복 공격) + the burrow-relocate  [seen; `kp02`]

Footage v1, P0 = 6.30 s (v1.md §3.A):

| P+ | s | pose / event |
|---|---|---|
| 0–5 | 6.30–6.55 | **tell**: `REAR` (hood lifts, arms open up) |
| 5–10 | 6.55–6.80 | `DIVE` head-first, body darkens |
| 10–20 | 6.80–7.30 | `SPLAY` sinking into a dark leaf-shaped pool (6–8 b), petals splayed |
| 20–29 | 7.30–7.75 | last fronds sink, pool flattens |
| 29–50 | 7.75–8.78 | **underground**: dark boss-shaped shadow glides 10–14 b at ≈ 0.6 b/t, stops 2–4 b beside the player |
| 50 | 8.80 | **BURST** = hit 1 (gold flash, radial gold blades r 3–5, cylinder r 3.5 h 4) |
| 51–61 | 8.85–9.35 | `ERUPT` upward, black leaf debris |
| 61–75 | 9.35–10.05 | `LOOM` over the player, turns (legs overhead) |
| 76–83 | 10.10–10.43 | **LUNGE-SWEEP** = hit 2 (gold slash band 9 × 3 × 2.5 along the facing), body flies flat |
| 83–94 | 10.43–11.00 | lands crouched 6–8 b to the side; pale "spine" afterimage fades |
| 94–176 | 11.0–15.1 | idle punish window |

Clip `burrow_strike` (94 t, next `idle_p1`, `hidden:[28,50]`, `forms:[[8,'p1_dark'],[50,'p1']]`):
`CROUCH`0 → `REAR`5 (`o`) → `DIVE`10 (`i`) → `SPLAY` y −0.5 @20 (`l`) → `SPLAY` y −3.5 @28 → hold → y −3.5 @49 →
`ERUPT`56 (`o`, from y −1 at 50) → `LOOM`68 → `LOOM`+arms back (A sh −60, yaw −70) @74 → `LUNGE` arms through @80
(`i`) → `LUNGE` end @83 → `SPLAY`-ish landing y 1.6 @89 (`i`) → `CROUCH`94 (`o`).

* Root travel: module moves the hidden anchor to the shadow stop point during 29–50 (shadow prop rides on it,
  ≈ 0.6 b/t, lock the target at P+44); module turns 61–75 toward the player; module slides the anchor 7 b along the
  facing during 76–89 (≈ 0.55 b/t).
* Joints: pelvis y (sink/erupt), spine pitch (dive), armA shoulders/elbows (sweep), legs fold during the lunge.
* Anticipation 10 t (rear + dive) and the shadow stop (6 t before the burst); impact at 50 and 80; settle 83–94.
* Events: `tell 0, dive 5, sink 10, pool 12, hide 28, travel 29, lock 44, burst 50, rise 56, loom 61, wind 72,
  sweep 76, sweep_end 83, land 89, end 94`.

**Burrow-relocate** (v2 4.62–6.75, P0 = 4.62): tell 0–5 (crouch lower), sink 5–15 tinting brown and breaking into
root chunks with gold glints, gone 15–19, dissolves in on the player in 2–3 t as an upright hooded figure (hood top
6.3), settles 21–43; no hit (it is the opener of 초목이 시든 풍경 here). Clips `sink_p1` (18 t, `hidden:[15,-1]`,
`forms:[[5,'p1_brown']]`; `CROUCH`0 → y 1.6 @5 → `SPLAY` y −3.5 @15) and `emerge_on_p1` (24 t, `hidden:[0,1]`,
`forms:[[1,'ghost'],[4,'p1']]`; `HALF` raised to y 3.2, spine −60 (upright hooded) @1 → settle sway @12 → @24);
module teleports the anchor to the player while hidden (≈ 4 t). Events `sink_p1 {tell 0, sink 5, chunks 9, hide 15}`,
`emerge_on_p1 {show 1, solid 4, settle 12, end 24}`.

### 6.4 생명의 손 (caption 땅에 손꼽기)  [seen; `kp03`]

Footage v1, P0 = 18.60 s (v1.md §3.H):

| P+ | s | pose / event |
|---|---|---|
| 0–7 | 18.60–18.95 | `SPREAD`, rears |
| 7–36 | 18.95–20.40 | **tell**: twists round ≈ 1 full turn with pale-green wisps spiralling, leaves whirl |
| 36–39 | 20.40–20.55 | `OVERHEAD` hands together |
| 40 | 20.617 | **PLUNGE** both hands into the ground (white-gold flash), green splinter splash r 3–4 (hits at the boss) |
| 47–53 | 20.95–21.25 | crouched, hands buried |
| 53–68 | 21.25–22.00 | 4 summoned legs rise around the player (2 near at ±6 b, 2 far), 5–7 b hooked stalks |
| 68–79 | 22.00–22.55 | glowing crack-line telegraphs from each leg toward the middle (11 t) |
| 82 / 89 / 95 / 102 | 22.68 / 23.05 / 23.35 / 23.72 | **4 strip slams** R, L, L-front, R (7 × 2.5 strips, 6–7 t apart) |
| 103–120 | 23.75–24.60 | legs sink, debris settles |
| 120–128 | 24.60–25.00 | `CROSS` upright on buried hands |
| 128–148 | 25.00–26.00 | pulls hands out, `FLOWER` rear (9 m) |
| 148–160 | 26.00–26.60 | folds to `CROUCH` (thud) |

Clip `hands` (160 t, next `idle_p1`): `CROUCH`0 → `SPREAD`7 → swirl: pelvis yaw 0→360 over 7–36 (`l`) with spine
twist lag (+20 yaw on spine3 at 20, back to 0 at 36), arms A swirling out (abd 100), mantle flung by the sim →
`OVERHEAD`39 (`o`) → `PLUNGE`40 (`i`, 1 t) → hold `PLUNGE` 40–47 → settle `PLUNGE` deeper (y 1.6) @53 → tiny spine dips
(+5 pitch, 2 t) at 82/89/95/102 as the remote legs slam → `CROSS`124 → `FLOWER`140 (`o`) → `CROUCH`160 (`i` then
`o` thud at 154).

* Root travel: none (the slams are remote props). Turn: none (the swirl is a whole pelvis turn).
* Anticipation 40 t (very long, readable); impact at the plunge and the 4 slams; settle 103–160.
* Events: `spread 0, swirl 7, raise 36, plunge 40, legs 53, lines 68, slam1 82, slam2 89, slam3 95, slam4 102,
  sink 103, stand 120, pull 128, flower 138, fold 148, end 160`.
* Retime candidate: swirl 7–36 → 7–29 (−25 %).

### 6.5 발광하는 파수꾼 (caption 발광)  [seen; `kp04`]

Footage: v1 P0 = 28.00 s (travel + slams 1–2), v2 0.0–2.25 (slam 3). v2 0.0 ≈ v1 40.0 ± 0.6 s (YouTube clock), so the
slam-3 tick is ± 12 t.

| P+ | s | pose / event |
|---|---|---|
| 0–6 | v1 28.00–28.30 | `REAR` tell |
| 6–30 | 28.30–29.50 | `DIVE`, sinks into a dark pool |
| 30–51 | 29.50–30.53 | shadow drifts **to the arena centre** (10–15 b) |
| 51–56 | 30.55–30.80 | gold glow on the ground at the emergence point (tell) |
| 56–72 | 30.80–31.60 | crown spike, then the hood rises out with debris |
| 72–132 | 31.60–34.60 | emerges into `CROUCH`, turns to the player (≈ 60 t of turning/idle) |
| 132–180 | 34.60–37.00 | **wind-up**: lifts the leaf-arms, twists them round itself, rises |
| 180–189 | 37.00–37.45 | `COLUMN`: all leaf-arms wound into a vertical spiral 8–9 b |
| 191 | 37.567 | **SLAM 1**: collapses forward (`SLAM`), cylinder r 4.5 + gold blade burst r 6 + ≈ 16–20 thorn wheels on a ring r 3–6 |
| 214–220 | 38.70–39.00 | short re-rear (6 t tell) |
| 221 | 39.033 | **SLAM 2** + wheels |
| 230–247 | 39.4–40.3 | leaps high (`AIR` over the centre) |
| 247–262 | v2 0.33–1.05 | `DIVEDOWN` head-first from 6–8 b |
| ≈ 262 | v2 1.10 | **SLAM 3** touch-down + wheel ring |
| 262–296 | v2 1.1–2.8 | wheels sweep and home; boss crouched at the centre, idle |

Wheels: spawn on the slam (+0…+4 t), roll outward 0.75–1 b/t for ≈ 10 t, then 2 per slam home on the player
(turn ≤ 8°/t, 0.35–0.45 b/t), live ≈ 22 t, small damage, "undodgeable" in Genshin.

Clips: `burrow_in_p1` (30 t: `REAR`6 → `DIVE`12 → `SPLAY` y −3.5 @28; `hidden:[28,-1]`; `forms [[8,'p1_dark']]`;
events `tell 0, dive 6, sink 8, hide 28`), module moves the hidden anchor to the centre (≈ 20 t, shadow prop), then
`emerge_crown_p1` (40 t, `hidden:[0,5]`: gold ground glow prop at 0, crown at y −1.5 @5, hood at y −0.5 @12, `HALF`
@24 (`o`), `CROUCH` @40; events `glow 0, crown 5, hood 10, out 21, end 40`), the module turns to the player, then
`glow_slams` (t0 = v1 34.60):

`CROUCH`0 → arms lifting (A sh −60) @12 → winding: spine yaw +20/+20/+20 and arms wrapping @30 → `COLUMN` @48 (`o`)
→ hold @57 → `SLAM` @59 (`i`, 2 t) → hold low @63 → `CROUCH` @80 → `REAR` @86 (`o`) → `SLAM` @89 (`i`) → `CROUCH`
@95 → `AIR` @106 (`o`, pelvis y 7) → hold @113 → `DIVEDOWN` y 4 @122 (`i`) → `SLAM` y 1.6 @130 (`i`) → `CROUCH` @150
(`o`) → @160. Len 160, next `idle_p1`.

* Root travel: horizontal none (all at the centre); vertical leap +7 b in the clip.
* Joints: spine twist + armA wrap (wind-up), pelvis pitch (collapse), whole-body flip (dive).
* Anticipation: 48 t wind-up (footage 59 t incl. a slower start; retime 0–48 → 0–36), 6 t before slam 2, the leap
  before slam 3. Impacts 59 / 89 / 130. Settle 130–160.
* Events: `wind 0, coil 30, column 48, slam1 59, wheels1 59, rear2 82, slam2 89, wheels2 89, leap 98, apex 106,
  dive 115, slam3 130, wheels3 130, settle 150, end 160`.

### 6.6 초목이 시든 풍경 (caption 회전 공격)  [seen; `kp05`]

Footage v2, preceded by the burrow-relocate onto the player (6.3); P0 = 6.75 s (v2.md §3.R):

| P+ | s | pose / event |
|---|---|---|
| 0–5 | 6.75–7.00 | arms swing up out of the drapes |
| 5–13 | 7.00–7.40 | `ARMSUP` (hands 6.8 up, belly core visible) |
| 13–25 | 7.40–8.00 | `LEAN` rears to full height (≥ 7) over the player |
| 21 | 7.80 | **disc telegraph** r ≈ 7.5 appears and fills from the centre (23 t) |
| 25–44 | 8.00–8.95 | sways tall, arms hanging |
| 44 | 8.95 | disc full = dodge cue |
| 45–52 | 9.00–9.35 | `CRASH` sideways (falls to its right), limbs flung out |
| 52–76 | 9.35–10.55 | **SPIN** lying low, ≈ 1–1.5 turns, hurt window inside r 7.5 (flash at 62) |
| 76–105 | 10.55–12.00 | `SPRAWL`, pushes itself up |
| 105–135 | 12.00–13.50 | stands, turns to the player |

Clip `rotation` (135 t, next `idle_p1`): (after `emerge_on_p1`) upright 0 → `ARMSUP`10 (`o`) → `LEAN` up @20 → `LEAN`
over @30 → sway (spine roll ±6°) @37 → @44 → `CRASH` @52 (`i`, roll −80, y 1.2) → `SPIN`: pelvis yaw 0→360 over 52–76
(`l`, 15°/t) → `SPRAWL` @82 (`o`) → push up (C plants, spine −20) @100 → `CROUCH` @118 → @135.

* Root travel: none (spins where it emerged). Turn: module 118–135.
* Anticipation 45 t incl. the 23 t disc; impact window 52–76 (hit once, knock outward); long settle 76–135.
* Events: `arms 0, rear 13, disc 21, full 44, crash 45, spin 52, flash 62, spin_end 76, rise 90, stand 105, end 135`.
* Retime candidate: 0–21 → 0–16 only (keep the 23 t fill).

### 6.7 생명의 꼬리, phase 1 (caption 꼬리치기)  [seen as 2 sweeps; `kp06`]

Trigger: player behind the boss. Footage v2, P0 = 15.73 s:

| P+ | s | pose / event |
|---|---|---|
| 0–19 | 15.73–16.70 | turns its back (150–180°, module ≈ 9°/t) |
| 11–31 | 16.30–17.30 | **tell**: tail rises and curls into an S (`TAIL_S`), body coils |
| 31–37 | 17.30–17.62 | `TAIL_COCK` |
| 37–46 | 17.62–18.05 | **SWING 1**: body whips round, tail sweeps horizontally 0.5–2 b high, white-gold arc (dodged) |
| 46–61 | 18.05–18.80 | recoil, tail drawn back the other way |
| 61–66 | 18.80–19.05 | coil |
| 66–73 | 19.05–19.40 | **SWING 2** reverse direction (hit −5324 = 25 % max HP at 67) |
| 73–141 | 19.40–22.80 | sprawled with the tail on the ground, rises, turns |

The brief says one swing in phase 1; the footage shows two. Proposal: author both.

* `tail_p1` (single, 90 t): `CROUCH`0 → `TAIL_S`24 (`o`) → `TAIL_COCK`35 → `TAIL_WHIP`44 (`i`; pelvis yaw −35→+60
  inside the clip, returns to 0 by 70; tail chain lags 1–2 t per segment) → recoil @56 → `SPRAWL`-light @70 → `CROUCH`
  @90. Events `turn 0, raise 11, cock 31, swing 37, hit 41, swing_end 46, settle 70, end 90`.
* `tail_p1x2` (footage, 141 t): as above to 46, recoil `TAIL_COCK` mirrored @61, `TAIL_WHIP` mirrored @70 (`i`),
  `SPRAWL` @85, `CROUCH` @125, @141. Events `turn 0, raise 11, cock 31, swing1 37, hit1 41, cock2 61, swing2 66,
  hit2 67, end2 73, rise 100, end 141`.
* Hit volume: sector r 9.5, h 0–2.5, sweeping 180–270° at 25–30°/t. Body travel ≈ 1–2 b (ignore; pivots).
* Retime candidate: raise 11–31 → 11–26.

### 6.8 근접 콤보 (caption 콤보 공격, "2~4단")  [4 hits seen; `kp07`]

Footage v2 take 2, P0 = 24.45 s: hits at P+14 (low arm sweep), +50 (rear-up double slam), +87 (spin sweep), +131
(leaping double slam); recovery to +181. Slow on purpose ("매우 느릿하여").

| segment | P+ (footage) | key poses |
|---|---|---|
| a: arm sweep | 0–10 tell (R arm back, body twists) / 10–17 sweep (hit 14, 130° sector r 6 h 1.5) / 17–29 recover | `SWEEP_ARM` start → through |
| b: double slam | 29–47 rear on the hind legs, arms ≈ 7 b high / 50 slam (r 5–5.5, 4 b in front) / 51–63 cracks | `REAR`→`OVERHEAD`→`SLAM` |
| c: spin sweep | 77–82 twist / 82–92 one full turn low (hit 87, ring r 6 h 1.5) | pelvis yaw 360 |
| d: leap slam | 97–126 tallest rear / 126–131 lunge 2–3 b forward / 131 impact (r 5.5, 6 b in front) / 131–181 recovery, steps back | `LEAN`→`SLAM` |

Clips (the module plays 2–4 segments and appends `combo_end` unless the last one is `combo_d`):
`combo_a` 29 t (events `tell 0, swing 10, hit 14, end 29`), `combo_b` 48 t (`rear 0, high 16, slam 21, hold 21, end 48`),
`combo_c` 20 t (`twist 0, spin 5, hit 10, end 20`; pelvis yaw 0→360 over 5–15, `l`), `combo_d` 84 t (`rear 0, tall 26,
lunge 29, slam 34, recover 50, end 84`; module slides the anchor 2.5 b during 29–34), `combo_end` 20 t (back to
`CROUCH`). Anticipations 10 / 18 / 5 / 29 t. Retime candidates: b 0–18 → 0–14, d 0–29 → 0–22.

### 6.9 소생 단계 진입 (going under at < 1 %) and the phase-2 opening  [boss part: proposal; Heart part: seen `kp08`]

The boss sink is cut out of v2 (34.63 s cross-fade). Proposal `sink_revive` (60 t, `hidden:[45,-1]`,
`forms:[[20,'p1_brown']]`): stagger 0–10 (hood droops, `core` flickers 15/3), `SPLAY` flat 10–20, sinks as root chunks
20–45 (y 0 → −3.5, `l`), hidden 45; events `stagger 0, flicker 4, sink 20, chunks 30, hide 45, heart 50, end 60`.

Seen (v2 34.80–40.33): camera in the canopy; the **Heart (golden egg)** is held by a dark vine "hand" and lowered
slowly (35.4–38.3, ≈ 58 t, swaying 1–2 b); cut to the empty nest; the egg falls in 5 t (38.95–39.20), lands with a small
squash and a vertical green-gold light beam (10 t); HUD 「오아시스의 심장」 at 39.47, message at 39.62; organism spawn
markers at 40.0. Progress ≈ 25–27 %. Prop clip `heart_drop` 30 t: fall 0–5 (`i`), squash 5–8 (scale y 0.9, xz 1.05),
settle 8–14 (`o`), beam 5–15; events `fall 0, land 5, beam 5, hud 10, spawn 18, end 30`.

Phase-2 end (v5 0–4.2): bar jumps to 100 % at 1.4 s, the Heart just idles, fade to black 3.4–3.8. No boss motion.

### 6.10 2→3 revival cut-scene  [seen; `kp09`, `kp10`]

w2 (wiki clip, 25 fps): egg pulsing in the nest 0–36 t, a gold ring; egg lifts out, light dripping 36–82; dark scene, an
ember (「불씨」) carried along a stalk 82–145; egg in the canopy, vines wrap it and glow 145–213; **flash** 213–215 and a
shock of leaves 216–228; wide shot of the lake arena, calm green swirl 229–326; **the Warden bursts out of the water** in
a leaf splash 328; close-ups (hood + emerald crystals, mantle, back) 330–354; flash 355; **reveal** 356–390: tall
serpent, arms spread, hair whipping. In game (v5 4.4–12.45): lake 0–36, leaf burst 38, hood 42–48, mantle/crown
52–60, chest gold plate 62–66, flash 68–70, full-body reveal sway 72–110, fade 112–116, black, phase 3 fades in at
11.4–12.0 s already in `T` facing the player.

Clip `revival` (160 t, next `idle_p3`, `hidden:[0,60]`, `forms:[[0,'p1_dark'],[60,'p3']]`, `blend 6`): boss hidden
while the Heart prop pulses (0–20), lifts (20–40) and flashes (40); at 60 bursts up out of the centre (`MOUND` y −1 →
`CURL` y 1 @66, `o`), rises back to camera (`HUNCH` @80), reaches with arm A_R (sh −120) @90, flash event 96, unfurls
into `T` with arms going wide (`V`-ish @104 → `T` @118, `o`), sways (drapes sim whips) to 160. Events `pulse 0, lift 20,
flash1 40, burst 60, splash 60, reach 88, flash2 96, reveal 100, end 160`. Screen fade / title handled by the module.

### 6.11 Phase-3 idle, turn, walk  [seen; `kp10`, `kp14`, `kp16`]

* **Idle** (v5 12.0–12.45, 31.6–32.3; v6 6.5–8.4): `T`, upright, arms out with curled leaf tips waving slowly, body
  snake-sways, hair hangs, lower leaf hands flat as a skirt, tail coiled on the ground. Clip `idle_p3` 60 t loop: `T`0 →
  `T` with spine roll +3/−3/+3 and arms el +10 @30 → `T`60; osc on mantle and tail.
* **Turn**: `turn_p3` 20 t loop: skirt hands shuffle (B_L, C_R, B_R, C_L at 0/5/10/15, lift 0.3), spine yaw counter-lag
  6 t; module ≤ 6°/t.
* **Walk** (v5 19.8–21.8: walks low on its long pale legs toward the centre, tail trailing and flicking once at 20.7–21.4):
  `walk_p3` 32 t loop, legs B/C as a spider gait under a lowered torso (pelvis 2.6, spine −20), stride 3.8 b at
  0.12 b/t; events steps 0/8/16/24. The tail flick is a `tail_flick_p3` 20 t one-shot [optional].

### 6.12 이동 돌진 (caption 이동 공격: "바닥에서 빠르게 튀어 올라 꼬리를 휘두른다")  [seen; `kp11`]

Footage v5, P0 = 12.45 s (v6 0.75–1.6 shows the same burst + slash, faster after the burst):

| P+ | s | pose / event |
|---|---|---|
| 0–11 | 12.45–13.00 | starts to sink, `HUNCH` |
| 11–16 | 13.00–13.25 | collapses to a `MOUND` |
| 16–22 | 13.25–13.55 | sinks into a green glow ring on the water |
| 22–48 | 13.55–14.85 | **underground**: a trail of leaf pads travels to the player (≈ 12–15 b, ≈ 0.5 b/t) |
| 41–48 | 14.50–14.85 | pads gather into a ring = burst point (7 t tell) |
| 52 | 15.05 | **BURST** up (hit 1) |
| 52–57 | 15.05–15.30 | curls into a `HOOP` in the air |
| 57–69 | 15.30–15.90 | rolls forward as a wheel (≈ 1 turn, 3–4 b) |
| 69 | 15.90 | **wheel slams down** (hit 2) |
| 73–79 | 16.10–16.40 | tail lands, **TAIL SWEEP** along the ground (hit 3, sector r 9) |
| 79–99 | 16.40–17.40 | rises to `T` |

v6 take 1: burst 0.75 s → slash 0.85–1.15 (+2…+8 t) → low crouch 1.3 → hunched over the player 1.55; i.e. the hoop/roll can
be skipped when the burst is right on the player. Treat as variant `move_strike_p3_short` (burst 0, slash 4, crouch 11, end 30).

Clip `move_strike_p3` (100 t, next `idle_p3`, `hidden:[22,50]`): `T`0 → `HUNCH`11 → `MOUND`16 (`i`) → y −3.5 @22 →
hold → `MOUND` y −1 @50 → `HOOP` y 3 @57 (`o`) → roll: pelvis pitch 0→360 over 57–69 (`l`) → `HOOP` y 1.2 @69 (`i`) →
tail chain whip (`TAIL_WHIP` analogue, tail yaw +80/+50/+40/+30) @77 (`i`) → `CURL` @83 → `SCOIL` @92 → `T` @100 (`o`).

* Root travel: module moves the hidden anchor along the leaf-pad trail 22–48, then slides it 3.5 b forward during the
  roll 57–69.
* Joints: whole spine as a ring (3 × 60°), pelvis pitch spin, tail chain.
* Anticipation: the pad ring 41–48 (and the sink 0–22); impacts 52 / 69 / 77; settle 79–100.
* Events: `sink 0, mound 11, hide 22, trail 22, mark 41, show 50, burst 52, hoop 52, roll 57, slam 69, tail 73,
  sweep 77, rise 79, end 100`.

### 6.13 종말의 여파 (caption 광역 공격)  [seen in w1 + v5; `kp15`, `kp16`]

w1 (25 fps, P0 = 0): idle with the banner 0–36; crouches into a mound with a green charge glow 40–64; rises and whirls,
long limbs swinging in wide arcs 66–92; lands, a flat Dendro ring spreads on the water 96–100; seated, arms out 100–112;
flash 115; ring wave spreads 120–130; light pillar at the dome spot 136–140; **dome forms around the player** 144–156;
leaf splash on the dome 160–165; player inside, boss aloft/behind 170–210; **light columns rain** 216–238; white-out
240 (blast); dome holds 245–270; **dome pops** 275; green burst at the boss 280–290; upright, arms spread 296–324.

v5 (relative to the field start F0 = 22.00 s): crawls to the centre first with one tail flick (18.3–21.8); field
spreads 0–26; dome flash +28, dome formed +32, more domes (≥ 3 on the field) +60; boss flash +44 and rises/rolls into
the air +50; player waits in a dome +60…+104; **blast streak +105**, flood wave +110…+134; domes pop +161; boss stands
+172, `T` +188.

Phase timings agree: field → dome 28–40 t, dome → blast 70–92 t, blast → dome pop 36–56 t.

Clip `aftermath` (240 t, next `idle_p3`) [timings: average of w1 and v5]:
`T`0 → `CURL` (charge, `p3_lit`) @20 → `MOUND` @24 (`i`) → whirl: rise to `TALL` y 3 with pelvis yaw 0→360 over
26–50 (`l`, arms flung by abd 110, sim on drapes) → `CROUCH`-like seated (pelvis 1.2, arms out abd 100) @52 (`i`, field
starts) → hold to 84 (domes spawn) → `HOOP` rising y 1→6 @100 (`o`, roll pitch 0→360 over 92–108, `l`) → aloft hold,
arms `V` @110…150 (hover bob ±0.2) → `V` brightest @150 (rain starts) → blast @172 → descend y 6→1.8 @190 (`i`) → `CURL`
@205 (domes pop, green burst) → `T` @228 (`o`) → @240.

* Root travel: none horizontally during the cast (module walks it to the centre first with `walk_p3`); hover is the
  clip's pelvis y.
* Anticipation: 52 t charge + whirl; field 52–84; domes at 84 (the safe zones), 88 t of dome time before the blast;
  impact 172 (lethal outside domes); settle 205–240.
* Events: `charge 0, whirl 24, land 52, field 52, domes 84, rise 92, aloft 100, rain 150, blast 172, descend 178,
  pop 205, burst 206, end 240`.
* Wiki quirk: if the boss is knocked down during the cast the domes vanish first and the blast comes after a short
  delay; implement as "interrupt → `pop` immediately, `blast` 20 t later".

### 6.14 증폭의 풀 (caption 3연속 포격: "세 번의 포격… 첫 번째 포격 속도가 유난히 빠르다")  [seen except shell 3; `kp14`]

Footage v5, P0 = 32.40 s:

| P+ | s | pose / event |
|---|---|---|
| 0–14 | 32.40–33.10 | `HUNCH` forward, arms curl in |
| 19 | 33.35 | **target ring** on the ground at the player |
| 25–40 | 33.65–34.40 | body lights yellow (`p3_lit`), rises, glow gathers at the crown |
| 46 | 34.70 | **LAUNCH 1** (flash up from the crown) |
| 46–56 | 34.70–35.20 | `BALL` (curled ball of leaves) |
| 56 | 35.20 | **IMPACT 1** (beam column at the ring, 10 t flight = the fast one) |
| 56–72 | 35.20–36.00 | splash; cools to the dark hood (`p3`) |
| 72–100 | 36.0–37.4 | turns (module) |
| 100–118 | 37.4–38.3 | `T` charge, arms spread, yellow body |
| 119 | 38.35 | **SHELL 2** lands right of the player |
| ≈ 123 | 38.55 | second splash (= shell 3?, low confidence) |
| 130 | 38.90 | `V` arms up → sinks at 39.2 (this instance chains into 이동 돌진) |

Clip `shells` (128 t, next `idle_p3`; the module may chain `move_strike_p3` as the footage does):
`T`0 → `HUNCH`14 → (ring 19) → `TALL` lit @32 (`o`, `forms [[25,'p3_lit'],[60,'p3'],[100,'p3_lit'],[126,'p3']]`) →
`V`-crown @40 → flick: hood −25, arms up @46 (`i`) → `BALL` @50 → hold @56 → `T` @72 (`o`) → `T` @100 → arms flick
(sh −40, `i`) @104 and @109 → `V` @128.
Events: `hunch 0, mark1 19, lit 25, launch1 46, hit1 56, cool 60, mark2 96, mark3 100, launch2 104, launch3 109,
hit2 119, hit3 124, end 128` (shells 2/3: 15 t flight, slower than shell 1). Root travel none.

### 6.15 생명의 꼬리, phase 3 (caption 꼬리 공격: "꼬리를 2회 후려친다")  [seen; `kp12`]

Footage v6 take 2, P0 = 2.50 s (after the module turned it, v6 1.8):

| P+ | s | pose / event |
|---|---|---|
| 0–14 | 2.50–3.20 | `CURL` low crouch, tail curls up behind, cocks |
| 16–18 | 3.30–3.40 | **SWING 1**: horizontal whip, green trail to 3.9 |
| 30–50 | 4.0–5.0 | rises coiling into `SCOIL` (tall S) |
| 52–56 | 5.1–5.3 | coils down |
| 58–62 | 5.4–5.6 | **SWING 2**: big ground sweep (yellow-green trail), reverse direction |
| 70–78 | 6.0–6.4 | rises out of the VFX |
| 80–118 | 6.5–8.4 | `TALL` idle, arms spread |

Clip `tail_p3` (100 t, next `idle_p3`): `T`0 → `CURL` + tail cocked (tail yaw −60/−30/−20/−10, t1 −40) @14 (`o`) →
whip (pelvis yaw +60, tail yaw +70/+40/+30/+20) @18 (`i`) → hold @22 → `SCOIL` @46 (`o`) → `CURL` cocked mirrored @56
→ whip mirrored, low (t1 +10) @60 (`i`) → @63 → `HUNCH` @70 → `TALL` @80 (`o`) → `T` @100.
Events: `crouch 0, cock 4, swing1 16, hit1 17, rise 30, coil 46, swing2 58, hit2 59, rise 70, end 100`.
Strike-to-strike 42 t (P1: 29 t). Hit: sector r 9.5, h 0–2.5. Root travel none.

### 6.16 생명의 나선 (caption 가시 발사: "가시를 여러 개 소환하고 한꺼번에 날린다")  [seen; `kp13`]

Footage v6 take 3, P0 = 8.75 s:

| P+ | s | pose / event |
|---|---|---|
| 0 | 8.75 | `TALL`, arms spread |
| 5–10 | 9.00–9.25 | dark `CURL`, tail coiled |
| 13 | 9.40 | rises with glow |
| 19 | 9.70 | `V` arms up, yellow light column |
| 25 | 10.00 | stands tall, arms wide |
| 25–43 | 10.0–10.9 | many small yellow spiral spikes summoned around/above it, hovering |
| 49 | 11.20 | glint (aim) |
| 54 | 11.45 | **FIRE** all at once; DNA-helix trails rain on the player 54–75 |
| 77 | 12.60 | recover |
| 85–95 | 13.0–13.5 | sinks (this instance chains into 이동 돌진) |

Clip `spikes` (84 t, next `idle_p3`, `forms [[13,'p3_lit'],[60,'p3']]`): `T`0 → `CURL`8 (`i`) → `TALL` @13 (`o`) →
`V` @19 (`o`) → `T` wide (abd 100) @25 → hold, slight sway → arms pull back (sh +20, el 60) @49 → arms thrust forward
(sh −30 toward the player) @54 (`i`) → hold @66 → `T` @84 (`o`). Events `curl 5, rise 13, column 19, summon 25,
aim 43, glint 49, fire 54, rain 54, impacts 58-75, recover 77, end 84`. Root travel none.

### 6.17 Death  [proposal; no footage]

Clip `death` (120 t, `blend 6`, `forms [[85,'withered']]`, `hidden:[118,-1]`): hit-stagger, hood snaps back (neck −30)
@0–8 → face/core flicker (`core` 15/3 every 2 t) 8–30 → body droops, arms fall (`HUNCH` → arms abd 20) @30–55 →
kneels: pelvis 1.8 → 0.6, skirt hands spread flat @55–70 → topples forward onto the water (spine +30/+30/+20, hood
+40) @70–82 (`i`, splash event 82) → withers @85–100 → sinks / dissolves into leaves (y −2) @100–118 → gone; leave a small
golden seed prop glowing at the spot. Events `hit 0, flicker 8, droop 30, kneel 55, fall 70, land 82, wither 85,
sink 100, gone 118, end 120`.

## 7. Organisms (phase 2) — simple rigs and clips  [seen unless marked; `kp17`]

Common: organisms spawn as **pale wireframe/ghost domes** (≈ 0.8–1 b, v2 40.0, v3 1.2–2.0) that materialise; on death
they pop with leaf debris (basic) or a burst (others). 4 basics spawn at once. Organisms bob/turn on their own; the
module moves them.

| organism (size) | parts | clips (len t) | motion notes |
|---|---|---|---|
| **Heart of the Oasis** (bulb 2 × 3 lying, root cradle 3, sprouts to 3.5–4) | bulb, cradle, sprouts | `heart_idle` 40 loop; `heart_drop` 30; `heart_hit` 6; `heart_lift` 46 (cut-scene) | idle: bulb scale 1.00↔1.03, sprouts sway ±5°, gold ground swirl r 2.5–3.5 always on; hit: white flash 2 t (no flash seen in game, optional) |
| **기본 basic** (1.0 b bell bud) | bulb, crown petals | `org_spawn` 20; `basic_bob` 24 loop; `basic_melee` 14; `basic_ranged` 20; `org_die` 10 | **bob**: hop-slide toward the Heart, squash 0.9 / stretch 1.1 over 12 t, y +0.15. **ranged** (v3 16.42–17.4): squash 0–3, stretch + crown opens 3–6, **fire** bolt at 6–7 (green, to the Heart or the player), crown closes 10–20. **melee** [proposal]: lean back 0–4, bump forward 0.4 b 4–7 (hit 6), settle 14. Looks: `shielded` (2–4 translucent leaf panes 1.3 × 0.55 around it), `buffed` (green aura; immune) |
| **양육 nurturing** (≈ 2.2 b spiral stalk + hooded cap + orb, on a green ground ring r 1.2) | stalk, cap, orb | `nurt_idle` 40 loop; `nurt_buff` 20 (+ hold); `org_die` 17 | **buff** (v3 20.6–22.0): cap tilts toward the targets 0–8, **3 wavy green tether beams** from the orb to up to 3 basics from 8 on, held while they live; orb pulses every 10 t |
| **수호 guarding** (2.4 b twisted ribbon spire + orb 0.35 floating 0.6 above) | spire, orb | `guard_idle` 60 loop; `guard_cast` 12; `guard_die` 17 | idle: orb bob ±0.1, slow spin. **cast** (v3 33.05–33.6): orb rises from the tip 0–7, shields pop on nearby basics at 9–10. **die** (v4 6.33–7.20): red ember burst, collapses into a black twisted wisp with two ribbon horns, fades over 17 t; shields vanish at once |
| **둥지 nesting** (2.2 × 1.3, hovers 0.5–1.5 up; cap + orb + 2 arched sepal limbs) | cap, orb, limb_L, limb_R | `nest_fly` 14 loop; `nest_cast` 12; `nest_blink` 6 [wiki]; `org_die` 12 | **fly**: limbs flap V ↔ wide arch (period 12–16 t), y bob 0.2. **cast** (v4 11.70–12.37): limbs curl up into a vertical loop around the orb (12 t), then **3 leaf-wall groups erupt** around the player in 1 t (r 3–4, 120° apart, 3–5 blades 2.5–3 b tall), unfold 5 t, stand 40 t, dissolve into motes 8 t. No attack |
| **파괴 destruction** (Ø 1.2 spiked ball + yellow beak) | shell, beak | `destr_roll` 32 loop; `destr_fuse` 56; `destr_suck` 5; `destr_blast` 1; `org_die` 10 | **roll**: one turn per 32 t (≈ 0.12 b/t), beak spins with it; stops against the Heart. **fuse** (v4 19.0–21.55): beak/core pulses every 9 t, every 4 t in the last 20 t, glowing ring. **suck** (21.55–21.78): white-hot, shrinks 0.85, sound drop. **blast** 21.80: star rays 3, green dome r 3 for 12 t, blackened husk flung 2–3 b over 7 t; Heart −14 % |
| **포식성 predatory** (fish 2.5 long; bud 2.1 × 1.6; pod 3.5 tall) | body, head/jaw, tail fin, fins (+ form swap fish/bud/pod) | `pred_swim` 16 loop; `pred_swallow` 24; `pred_bud` 20 loop; `pred_inflate` 8; `pred_burst` 10; `pred_bite` 6; `pred_bite_chain` 38; `org_die` 12 | **swim**: tail fin yaw ±25°, body ±8° with 3 t lag, 0.15–0.2 b/t, 1–1.5 b up. **swallow** (v4 29.9–31.2): rears up 0–8, scoops down 8–12 (basic removed at 12), closes into the bud 12–24 (`form bud` at 14). **bud**: hover 0.2 above a gold swirl, spin 2°/t, bob. **inflate** (32.22–32.62): `form pod`, scale y 1 → 1.7 in 8 t. **burst** 32.65: rays r 3 (0.5 B), shreds, `form fish` at 2. **bite**: jaw open 0–3, lunge 1.5–2 b (module), snap 4 (hit). **chain**: 4 bites every 6 t (1.0 / 0.5 / 0.3 / 0.2 B), 14 t pause, repeat (9 bites seen) |

Spawn clip `org_spawn` (20 t): ghost dome look 0–12 (`forms [[0,'ghost']]`), materialise with a scale pop 0.8 → 1.05 → 1.0
at 12–20 (`forms [[12,'solid']]`). The v3/v4 white "phantom view" with name tags is the uploader's Elemental Sight,
not a mechanic.

## 8. Proposed clip list

Boss rig clips (`tools/apep_clips.mjs`, same shape as `butterfly_clips.mjs` / `fieldgen_clips.mjs`):

| clip | len | loop / next | hidden | forms | events (tick) |
|---|---|---|---|---|---|
| entrance_p1 | 110 | → idle_p1 | [0,4] | 0 p1_dark, 30 p1 | pool 0, hood 16, reach 31, flash 60, embers 63, crouch 91, roar 100, end 110 |
| idle_p1 | 60 | loop | | | — |
| turn_p1 | 20 | loop | | | step 0/5/10/15 |
| crawl_p1 | 16 | loop | | | stepA 0, stepB 8 (dust) |
| crawl_stop_p1 | 32 | → idle_p1 | | | plant 8, open 16, end 32 |
| walk_p1 | 36 | loop | | | step 0/9/18/27 |
| burrow_strike | 94 | → idle_p1 | [28,50] | 8 p1_dark, 50 p1 | tell 0, dive 5, sink 10, pool 12, hide 28, travel 29, lock 44, burst 50, rise 56, loom 61, wind 72, sweep 76, sweep_end 83, land 89, end 94 |
| sink_p1 | 18 | (hold hidden) | [15,-1] | 5 p1_brown | tell 0, sink 5, chunks 9, hide 15 |
| emerge_on_p1 | 24 | → rotation | [0,1] | 1 ghost, 4 p1 | show 1, solid 4, settle 12, end 24 |
| burrow_in_p1 | 30 | (hold hidden) | [28,-1] | 8 p1_dark | tell 0, dive 6, sink 8, hide 28 |
| emerge_crown_p1 | 40 | → idle_p1 | [0,5] | 5 p1_dark, 20 p1 | glow 0, crown 5, hood 10, out 21, end 40 |
| hands | 160 | → idle_p1 | | | spread 0, swirl 7, raise 36, plunge 40, legs 53, lines 68, slam1 82, slam2 89, slam3 95, slam4 102, sink 103, stand 120, pull 128, flower 138, fold 148, end 160 |
| glow_slams | 160 | → idle_p1 | | | wind 0, coil 30, column 48, slam1 59, rear2 82, slam2 89, leap 98, apex 106, dive 115, slam3 130, settle 150, end 160 (wheels = slam ticks) |
| rotation | 135 | → idle_p1 | | | arms 0, rear 13, disc 21, full 44, crash 45, spin 52, flash 62, spin_end 76, rise 90, stand 105, end 135 |
| tail_p1 | 90 | → idle_p1 | | | turn 0, raise 11, cock 31, swing 37, hit 41, swing_end 46, settle 70, end 90 |
| tail_p1x2 | 141 | → idle_p1 | | | raise 11, cock 31, swing1 37, hit1 41, cock2 61, swing2 66, hit2 67, end2 73, rise 100, end 141 |
| combo_a | 29 | → combo_b / combo_end | | | tell 0, swing 10, hit 14, end 29 |
| combo_b | 48 | → combo_c / combo_end | | | rear 0, high 16, slam 21, end 48 |
| combo_c | 20 | → combo_d / combo_end | | | twist 0, spin 5, hit 10, end 20 |
| combo_d | 84 | → idle_p1 | | | rear 0, tall 26, lunge 29, slam 34, recover 50, end 84 |
| combo_end | 20 | → idle_p1 | | | end 20 |
| sink_revive | 60 | (hold hidden) | [45,-1] | 20 p1_brown | stagger 0, flicker 4, sink 20, chunks 30, hide 45, heart 50, end 60 |
| revival | 160 | → idle_p3 (blend 6) | [0,60] | 0 p1_dark, 60 p3 | pulse 0, lift 20, flash1 40, burst 60, reach 88, flash2 96, reveal 100, end 160 |
| idle_p3 | 60 | loop | | | — |
| turn_p3 | 20 | loop | | | step 0/5/10/15 |
| walk_p3 | 32 | loop | | | step 0/8/16/24 |
| tail_flick_p3 | 20 | → idle_p3 | | | flick 8 (optional) |
| move_strike_p3 | 100 | → idle_p3 | [22,50] | | sink 0, mound 11, hide 22, trail 22, mark 41, show 50, burst 52, roll 57, slam 69, tail 73, sweep 77, rise 79, end 100 |
| move_strike_p3_short | 30 | → idle_p3 | | | burst 0, slash 4, crouch 11, end 30 (v6 variant; replaces move_strike_p3 from its burst tick 52 on, after the same sink and trail) |
| aftermath | 240 | → idle_p3 | | 20 p3_lit, 205 p3 | charge 0, whirl 24, land 52, field 52, domes 84, rise 92, aloft 100, rain 150, blast 172, descend 178, pop 205, burst 206, end 240 |
| shells | 128 | → idle_p3 | | 25 p3_lit, 60 p3, 100 p3_lit, 126 p3 | hunch 0, mark1 19, lit 25, launch1 46, hit1 56, cool 60, mark2 96, mark3 100, launch2 104, launch3 109, hit2 119, hit3 124, end 128 |
| tail_p3 | 100 | → idle_p3 | | | crouch 0, cock 4, swing1 16, hit1 17, rise 30, coil 46, swing2 58, hit2 59, rise2 70, end 100 |
| spikes | 84 | → idle_p3 | | 13 p3_lit, 60 p3 | curl 5, rise 13, column 19, summon 25, aim 43, glint 49, fire 54, impacts 58–75, recover 77, end 84 |
| death | 120 | — (blend 6) | [118,-1] | 85 withered | hit 0, flicker 8, droop 30, kneel 55, fall 70, land 82, wither 85, sink 100, gone 118, end 120 |

Organism clips (one small rig each, `tools/apep_org_clips.mjs`): `org_spawn 20`, `org_die 10–17`, `heart_idle 40L`,
`heart_drop 30`, `heart_hit 6`, `heart_lift 46`, `basic_bob 24L`, `basic_melee 14 {hit 6}`, `basic_ranged 20 {fire 6}`,
`nurt_idle 40L`, `nurt_buff 20 {tether 8}`, `guard_idle 60L`, `guard_cast 12 {orb 0, shields 10}`, `guard_die 17`,
`nest_fly 14L`, `nest_cast 12 {walls 12}`, `nest_blink 6 {out 0, in 3}`, `destr_roll 32L`, `destr_fuse 56 {pulse every 9,
then 4 from 36}`, `destr_suck 5`, `destr_blast 1 {blast 0}`, `pred_swim 16L`, `pred_swallow 24 {eat 12, bud 14}`,
`pred_bud 20L`, `pred_inflate 8`, `pred_burst 10 {hit 0, fish 2}`, `pred_bite 6 {hit 4}`, `pred_bite_chain 38 {hit 4/10/16/22}`.

Code shape (first entries; the rest follow the table):

```js
// tools/apep_clips.mjs — proposal. Poses: motion.md §5. 20 t/s. Module moves/turns the anchor.
const k = (t, pose, ease) => ease ? [t, pose, ease] : [t, pose];
export const CLIPS = [
  {name: 'idle_p1', len: 60, loop: true, keys: [k(0, CROUCH), k(30, CROUCH_IN), k(60, CROUCH)],
   osc: {mantle: [4, 40], tail: [6, 60, 8]}, events: {}, note: 'breathing, core 9-12'},
  {name: 'burrow_strike', len: 94, next: 'idle_p1', hidden: [28, 50], forms: [[8, 'p1_dark'], [50, 'p1']],
   keys: [k(0, CROUCH), k(5, REAR, 'o'), k(10, DIVE, 'i'), k(20, SPLAY_HALF, 'l'), k(28, SPLAY_UNDER), k(49, SPLAY_UNDER),
          k(50, BURST_START), k(56, ERUPT, 'o'), k(68, LOOM), k(74, LOOM_WIND), k(80, LUNGE, 'i'), k(83, LUNGE_END),
          k(89, LAND, 'i'), k(94, CROUCH, 'o')],
   events: {tell: 0, dive: 5, sink: 10, pool: 12, hide: 28, travel: 29, lock: 44, burst: 50, rise: 56, loom: 61,
            wind: 72, sweep: 76, sweep_end: 83, land: 89, end: 94},
   note: 'module: hidden anchor follows the shadow 29-50 (0.6 b/t), turn 61-75, slide 7 b 76-89'},
  {name: 'rotation', len: 135, next: 'idle_p1',
   keys: [k(0, UPRIGHT_HOOD), k(10, ARMSUP, 'o'), k(20, LEAN_UP), k(30, LEAN_OVER), k(44, LEAN_OVER), k(52, CRASH, 'i'),
          k(76, SPIN_360, 'l'), k(82, SPRAWL, 'o'), k(100, PUSH_UP), k(118, CROUCH), k(135, CROUCH)],
   events: {arms: 0, rear: 13, disc: 21, full: 44, crash: 45, spin: 52, flash: 62, spin_end: 76, rise: 90, stand: 105, end: 135},
   note: 'disc r7.5 fills 21-44 (never retime below 23 t); spin = pelvis yaw 0->360'},
  // … hands, glow_slams, tail_p1(x2), combo_a-d, sink_revive, revival, P3 clips, death as in the table
];
export const RETIME = {           // optional -25 % wind-ups, speed-up only
  hands: [[0, 0], [36, 29], [160, 153]], glow_slams: [[0, 0], [48, 36], [160, 148]],
  rotation: [[0, 0], [21, 16], [135, 130]], tail_p1: [[0, 0], [31, 26], [90, 85]],
  combo_b: [[0, 0], [18, 14], [48, 44]], combo_d: [[0, 0], [29, 22], [84, 77]],
};
```

## 9. Event → vanilla sound (from the analysts' audio tables; vanilla only)

| event | sound layers |
|---|---|
| dive / sink / burrow | `entity.warden.dig` p 0.9 + `block.rooted_dirt.break` + `block.mud.break` |
| underground travel | `entity.warden.dig` p 1.2 quiet every 6–8 t + `block.gravel.step` p 0.5 |
| burst / emerge | `entity.warden.emerge` p 1.3–1.4 + `block.amethyst_cluster.break` + `entity.generic.explode` p 1.3 v 0.4 |
| sweeps (lunge, tail, combo) | `entity.player.attack.sweep` p 0.5–0.7 + `entity.breeze.wind_burst` p 0.6 / `item.trident.throw` p 0.5 |
| slams (발광, combo, hands legs) | `entity.warden.attack_impact` + `entity.generic.explode` p 0.7 v 0.5 + `block.big_dripleaf.break` |
| swirl / whirl tells | `entity.breeze.whirl` p 0.7 + `block.azalea_leaves.break` p 0.8 every 3 t |
| thorn wheels | spawn `block.amethyst_cluster.place`; roll loop `block.azalea_leaves.step` p 0.6; pop `block.amethyst_cluster.break` |
| disc / ring telegraphs | `block.beacon.ambient` p 1.4 v 0.4 + `block.sculk_sensor.clicking` |
| crawl / walk steps | `entity.camel.step` p 0.6 + `block.moss_carpet.step`; heavy `entity.warden.step` p 0.8 |
| Heart drop / beam | `block.honey_block.fall` p 0.6 + `block.beacon.power_select` p 1.4 + `block.amethyst_block.chime` |
| organisms | spawn `block.chorus_flower.grow`; basic death `block.azalea_leaves.break` + `entity.slime.squish_small`; walls `block.big_dripleaf.place` ×3 p 0.7; roll `entity.armadillo.roll` p 0.8; fuse `entity.creeper.primed` p 1.4; blast `entity.generic.explode` p 0.8; swallow `entity.generic.eat` p 0.6; inflate/burst `entity.puffer_fish.blow_up` / `blow_out`; bite `entity.evoker_fangs.attack` p 1.3 |
| P3 shells / spikes / aftermath [proposal] | launch `entity.breeze.shoot` p 0.8; impact `entity.generic.explode` p 1.2 + `block.amethyst_block.break`; spikes summon `block.pointed_dripstone.place` ×n p 1.6, fire `entity.arrow.shoot` ×n p 0.6; dome `block.beacon.activate` p 1.5; blast `entity.warden.sonic_boom` p 0.8 + `entity.lightning_bolt.thunder` v 0.4 |

## 10. Gaps and decisions for the module author

1. **Phase-1 tail count**: brief = 1 swing, footage (v2) = 2 sweeps 29 t apart. Both clips are listed (`tail_p1`,
   `tail_p1x2`).
2. **Combo length**: only the 4-hit chain is seen; 2–3-hit chains are cut versions (segments a–c + `combo_end`).
3. **Shell 3** of 증폭의 풀: only a second splash 4 t after shell 2 is visible; timing 124 is a proposal.
4. **소생 단계 진입 sink, death**: no footage; clips are proposals built from the burrow anatomy and fieldgen/butterfly
   death conventions.
5. **종말의 여파 hover**: in v5 the boss rolls up into the air (+50) and stays high behind the domes; w1 is ambiguous
   (boss above the dome). Medium confidence; a grounded `TALL` cast is the fallback.
6. **v5 18.3–21.8** (looms over the player, crouch, walk to the centre with a tail flick) precedes 종말의 여파 in game;
   treated as `walk_p3` + optional `tail_flick_p3`, not as a separate pattern (it is not in the wiki's P3 list).
7. **v6 take-1 burst** (burst → slash in ≈ 5 t) is a shorter 이동 돌진 than v5's hoop/roll/tail version;
   `move_strike_p3_short` covers it.
8. Turn rates: P1 9°/t is measured; P3 6°/t is a proposal (P3 never turned fast on camera).
