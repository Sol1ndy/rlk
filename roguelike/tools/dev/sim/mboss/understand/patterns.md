# 파수꾼・타락 (개안자 · 세계 망루의 파수꾼): consolidated pattern spec

Sources (all under `scratchpad/mboss/`):
- PDF: `src/guide.pdf` (namu.wiki 5.11 파수꾼・타락, pp. 73-75). It is an image-only PDF, so it was read visually; no text layer exists.
- Video reports: `understand/m1.md` (patterns 1-5), `m2.md` (guard mode ×3 and the chaos start), `m3.md` (chaos end, star breaks, groggy, inert-star chaos start), `m4.md` (chaos fail). The frames are in `understand/m1/` to `understand/m4/`.
- Model: `understand/model.md` (rig, scale and poses).
- Code context, used only to phrase the open decisions: `code/elements_damage.md`, `code/integration.md`, `code/boss_infra.md`.

Notation:
- `m2 18.30 s / f1098 / t366` is a time inside a video: seconds, 60 fps frame, and 20 tps tick (t = s×20 = f/3).
- **rel** is ticks from the first boss motion of the pattern. Every timeline below gives rel ticks first and the source ticks in brackets.
- **BH** = boss height. The model fixes **BH = 3.0 b** (`model.md` §1).
- Distances and AoE radii were measured against the player (≈1.65 m), so they carry over **1 m → 1 b**.
- Confidence tags: **[obs]** observed in the footage; **[pdf]** stated by the PDF or a guide caption; **[inf]** inferred; **[prop]** proposal (not in any source).

Every clip is from an **edited guide video**: cuts, replays, cross-fades and four different attempts are mixed together. No uncut sequence of normal patterns exists. Read §0.3 before using any "order" information.

---------------------------------------------------------------------------------------------------

## 0. Overview

### 0.1 Pattern list

| # | PDF name | guide caption | range condition | element | evidence |
|---|---|---|---|---|---|
| 1 | 공간 찌르기 | 찌르기 · 2회 연속 찌르기 공격 | mid (start 3-5 m) [obs] | Geo | m1 0.00-4.73 |
| 2 | 공간 투창 – 심판하는 파수꾼 | 투창 · 창을 던져 공격한다 | mid (6-8 m at the throw) [obs] | Geo | m1 5.30-9.47 |
| 3 | 공간을 집행하는 시련 | 창 꽂기 · 근접 거리에서 창을 내다 꽂아 공격한다 | **melee** [pdf] (2-3 m) [obs] | Geo | m1 9.85-14.50 |
| 4 | 어둠 속에서 퍼지는 공간 | 공간의 권능 · 대상을 강제 소환한다 / 휘두르기 · 창을 두 번 휘둘러 공격한다 | **far** [pdf] (8-10 m) [obs] | Geo (pull: none) | m1 14.73-17.50 (+ slowed replay 17.93-21.8), 22.50-25.05 |
| 5 | 하늘을 심판하는 자 | 직접 꽂기 · 직접 날아와서 창을 내다 꽂는다 | **far** [pdf] (10-12 m) [obs] | Geo | m1 26.45-31.52 |
| 6 | 파수 모드 – 기록하고 판결하는 자 | 파수 모드 I / II | any [obs] | Geo, or the recorded element | m2 0.70-10.6, 11.85-17.1, 18.30-26.0 |
| 7 | 혼돈 – 신성한 붉은 에너지 | 혼돈 / 파괴 성공 / 그로기 / 타성 원소별 / 파괴 실패 | after **2 guard modes** [pdf] | — | m2 26.33-40.03; m3 all; m4 all |
| — | entrance (등장) | — | fight start | Geo | **PDF only** |
| — | groggy (그로기) | 그로기 | 2nd star broken | — | m3 1.45-5.85, 16.75-27.1 |
| — | death (사망) | — | HP 0 | — | **PDF only** |

### 0.2 Boss constants
- **Name** (HP bar): `개안자` / `세계 망루의 파수꾼`, Lv.103 [obs]. The PDF card reads `파수꾼・타락 / 개안자 - 세계 망루의 파수꾼`, so the subtitle is the generic boss title (see C3).
- **Max HP**: derived from the fixed star-break numbers 43 873 = 6 % and 131 619 = 18 %, giving ≈731 217 [obs].
- **No HP-threshold phases** [obs/pdf]. Neither the PDF nor the footage shows any. m1 runs from 100 % to 97.5 % with no change.
- **Locomotion**: never walks.
  - Idle hover: feet 0.3-0.5 b up (0.35 b in the model), slow bob.
  - Movement: glides at ≈1 m/s in guard mode and 2-4 m/s on the approach after a fail.
  - Fast moves: dashes (thrust 2 ≥35 m/s), leap + arcing flight (8-10 m/s), straight vertical take-off (fly-slam).
- **Default stance**: spear held low and diagonal (tip to her right-front-down, butt across the chest), wing hanging. Most patterns end with a spear twirl back to this pose (≈0.6-0.8 s, 12-16 t).

### 0.3 What the footage says about pattern order (weak evidence)
- **m1** is a showcase. Its clips appear **in PDF order** (1 → 5) and come from different attempts, so it says nothing about AI order or cooldowns.
- **m2 clip B** (attempt #1, apparently one take) runs:
  - **guard I** from 100 % boss HP → swing → 43 t of recovery and reposition;
  - **guard II** → swing → 20 t later, a **leap to the centre** for chaos.
  So the two guard modes ran **back to back, with no normal pattern between them**, and chaos followed immediately. This matches the caption "파수 모드 패턴 2회 반복 후 중앙으로 이동".
- **Boss HP at chaos**:

  | attempt | boss HP at chaos | source |
  |---|---|---|
  | #1 | ≈97.9 % | m2, m3 C |
  | #2 | ≈84 % | m3 E |
  | #3 | ≈98.4 % | m3 G |
  | #4 | 100 % | m3 H |

  So the guard → guard → chaos cycle is **not HP-gated**, and it comes early in the fight (attempt #4 reached chaos without damaging the boss at all).
- **After a fail** (m4): she leaves the centre, glides to ≈2 m from the player and raises her wing as if to start an attack.
- **After groggy** (m3 F): get-up, then a recovered stance with no attack for ≥1.5 s before the cut.
- **No video shows a second chaos cycle inside one fight.** m3 G is attempt #3, not a second cycle of attempt #2.

---------------------------------------------------------------------------------------------------

## 1. Idle and movement

**Selection**: between patterns, and while closing in.

**Poses** [obs]:
- **Idle**: feet 0.3-0.5 b up, legs dangling, a slight bob. The spear is low and diagonal; the wing is fanned down.
  - m1 f0, m1 9.85-11.0, m4 6.8-7.83 (`key_f0469`).
  - Model rest pose: `model.md` §8 (bob +0.05 b over a 40 t loop).
- **Guard drift**: ≈0.8-1 m/s toward the player while guard mode is active (m2 A5).
- **Short reposition** between attacks: a ≈2 m glide while the spear rotates up, then down-diagonal (m2 B9, 17.10-18.30, 24 t).
- **Approach after a fail** (m4 28-30, 5.0-7.83 s):
  - hover ≈0.3 m, spear held level and pointing at the player, wing spread;
  - then a 45° diagonal raise and a lower;
  - 2-4 m/s, reaching ≈2 m from the player after ≈36 t.
- **Leap + flight** (chaos entry, m2 B18-B20): see §8.1.
- **Twirl to idle** after attacks: whoosh pulses, e.g. m1 13.60 and 13.74, with the tail at 14.72.

**Geometry**: the gameplay hurtbox is ≈1.2 b wide × 3.0 b tall on the torso and skirt, excluding the wing and the spear (`model.md` §1).

**Sounds**: glide `entity.phantom.flap` (p 0.7, v 0.4); twirl `item.trident.riptide_1` (p 1.4, quiet) + `entity.player.attack.sweep` (p 0.7) per half-turn (`model.md` §7).

**Voice**: none.

---------------------------------------------------------------------------------------------------

## 2. Entrance (등장): PDF only

**Selection**: fight start.

**PDF text**: "보스가 있는 위치로 다가가면 등장하는데, 숨어있다가 나타나는 형식의 이전의 보스들과는 달리 어떤 표시도 남기지 않은 상태에서 나온다. 등장 시 창을 바닥에 꽂으며 나타나는데, 이때 바닥에 내리꽂히는 창에 맞아도 피해를 입는다."
- She appears when the player comes near, **with no prior marker**.
- She appears **while planting her spear into the ground**, and **the falling spear deals damage**.

**Timeline**: not observed.
- `model.md` §9 proposal [prop]: drop `spear_prop` from ≈8 b up onto the arena centre (point down, 3 t fall, Geo impact); fade the rig in beside it over 10 t; she grabs the spear (hand at f 0.74), pulls it out (8 t) and twirls to idle.
- `integration.md` §6.1 / D12-D13 proposal [prop]: an 80 t intro with an untargetable boss and a filling bar; a gold glint plus a **24 t ground telegraph** (disc r 3); the plant (Geo hit, gold ring, spikes).

**Geometry**: unknown. Reuse the P3 impact look: pillar, flash, radial crystal blades [prop].

**Damage**: yes, per the PDF; the value is unknown.

**FX** [prop]: reuse the P3 impact (§5) and the P5 vertical gold pillar (§7).

**Sounds** [prop]: the P3 impact composition (`entity.generic.explode` p 0.9 + `block.amethyst_cluster.break` + `item.trident.thunder` v 0.3), then the pull-out thud (`block.chain.break` p 0.6 + `block.stone.break`).

**Voice** [pdf]: 전투 시작 "**통찰하여, 나의 마음을 보아라.**"

**Evidence**: none in m1-m4.

---------------------------------------------------------------------------------------------------

## 3. P1 공간 찌르기: two thrusts

**PDF** [pdf]: "전방위 바위 창으로 2회를 찔러 공격한다." (stabs twice with a Geo spear, "from any direction").

**Selection** [obs]: the boss starts ≈3-5 m in front of the player, hovering ≈0.5 m up. There is no other condition.

**Timeline** (m1 A; rel 0 = wind-up start, m1 0.20 s / t4):

| rel t | [m1 t] | event |
|---|---|---|
| 0-4 | 4-8 | Wind-up: spear raised level and cocked back, torso yawed ≈−30°, wing flares up |
| 4-16 | 8-20 | **Charge glow**: a gold lightning-like streak grows along the shaft and blade, full by rel 16 |
| 19 | 23.3 | **Glint**: white-gold oval flare at the tip (the last telegraph) |
| 20-21 | 24-25 | Lens streak through the spear (1-2 frames) |
| 21-26 | 25-30 | Coil: drifts up and back, spear aimed down-forward at the player |
| 27-28 | 31-32 | Lunge 1: dives 2-3 m forward and down |
| **28** | **32** | **HIT 1** |
| 28-38 | 32-42 | Burst fades; she rises next to the player among gold and dark cubes |
| 38-54 | 42-58 | Reposition: flies up and back to 4-6 m away and 2-3 m up, turning in the air, spear pointing down at the player |
| 54-57 | 58-61 | Dive start: body pitched nose-down |
| 57-58 | 61-62 | Lunge 2: a diagonal dash of 5-6 m in 2-3 t |
| **58** | **62** | **HIT 2**: the player is knocked down (lying from 3.6 to 4.07 s) |
| 58-64 | 62-68 | Impact flare; a diagonal light trail lingers |
| 65 | 69 | Lands ≈1 m beside the downed player |
| 72-84 | 76-88 | Flourish: spear swept up with a gold glint and twirled overhead |
| 91 | 95 | Back to idle. **Total ≈91 t** |

Key gaps: glow → hit 1 = 24 t; glint → hit 1 = 9 t; hit 1 → hit 2 = 30 t; recovery after hit 2 ≈33 t.

**Geometry** [obs]:
- **Hit 1**: a sphere of r ≈1.5 b at the spear tip after the 2-3 b lunge.
- **Hit 2**: the dash path (≈1 b wide, 5-6 b long) plus a sphere of r ≈1.5 b at its end.
- The second thrust comes from a **new direction**, a dive from above. This is presumably what the PDF's "전방위" (omnidirectional) means [inf].
- No ground telegraph is shown.

**Damage** [obs]: hit 1 = 2414 (12.5 % of 19 268 max HP); hit 2 = 2767 (14.4 %) plus a knockdown.

**FX** [obs]:
- **Charge streak**: core `#FCF5AE`, mid `#CDB37E`, edge `#9D8650`.
- **Hit 1**: a gold burst sphere ≈3 b wide and a circular shock-ring arc ≈3.5 b; gold geo cubes (0.3-0.5 b, `#FCF09B` / `#C09F5E` / `#A17832`); dark-brown cubes and rock debris.
- **Hit 2**: a gold streak ≈1 b wide along the dash; an impact flare.
- Palette: `#FDF6B0` / `#D8C385` / `#A07F37`.

**Sounds** [obs]:

| event | m1 time | character | vanilla composition |
|---|---|---|---|
| charge | 0.55 → 1.42 s (rel 7-24) | rising airy shimmer, 8-16 kHz | `block.beacon.power_select` (p 1.6-2.0, quiet) + `block.amethyst_block.chime` ticks |
| hit 1 | peak 1.71-1.76 s | sharp crystalline crack and burst, ≈0.4 s | `item.trident.hit` (p 0.8) + `block.amethyst_cluster.break` + `entity.generic.explode` (p 1.6, v 0.4) |
| dive | swoosh 2.98-3.06 s | — | `entity.player.attack.sweep` (p 0.7) |
| hit 2 | peak 3.21-3.33 s | as hit 1 | as hit 1 |
| landing / flourish | low thumps 3.54-4.03 s | — | twirl composition |

**Voice**: none audible. The PDF's "attack" lines could go here [prop], see §11.

**Evidence**: m1 0.00-4.73 s only. Pink-lit arena; `sheet_thrust_*.jpg`, `k_f0040/0072/0096/0150/0170/0186/0270`.

---------------------------------------------------------------------------------------------------

## 4. P2 공간 투창 – 심판하는 파수꾼: javelin

**PDF** [pdf]: "직선으로 창을 던져 바위 원소 피해를 준다." (throws the spear in a straight line, Geo damage).

**Selection** [obs]:
- The clip opens at point-blank range (5.30 s, partly cut); the distance opens to ≈6-8 m by the time the glyph appears.
- The PDF gives no range condition. It fits mid to far range [inf].

**Timeline** (m1 B; rel 0 = m1 5.75 s / t115, after the cuts at 5.33 and 5.73 s):

| rel t | [m1 t] | event |
|---|---|---|
| 0-6 | 115-121 | Horizontal spear spin around her body, big wing swing; spear swept down-left with a gold trail |
| 8 | 123 | Gold slash flash low-left; **the spear vanishes from her hands** |
| 9-22 | 124-137 | **Glyph telegraph**: a gold concave 4-point star ≈1 b wide at chest height, ≈1.5 b to her side; it rotates and shrinks |
| 21-24 | 136-139 | The glyph compresses into a spinning gold ring (≈0.6 b) |
| **25.7** | **140.7** | **Vertical white-gold beam** through the glyph (≈1 BH tall, 1-2 frames): the last telegraph |
| 26-29 | 141-144 | Glyph re-flashes larger (≈1.5 b) → ring |
| 29-33 | 144-148 | Draw-back: arm back, spear re-materialises in her hand with a gold glow and cubes |
| **33-34** | **148-149** | **Release**: white-gold explosion ≈2 b wide at her hand |
| 35-37 | 150-152 | Launch disc: a gold circle/portal ≈1.5-2 b across at the launch point, plus gold cubes |
| **37.7-39** | **152.7-154** | **Projectile**: a straight horizontal line at chest height (1.2-1.5 b), crossing the screen (≥15 b) in 1-2 frames |
| 39-43 | 154-158 | Trail lingers: yellow streak ≈0.5 b thick, tumbling gold and dark cubes, rock debris |
| 43-56 | 158-171 | Empty-handed |
| 56-59 | 171-174 | **The spear returns** along the line to her |
| 61-74 | 176-189 | Overhead catch (spear vertical), lowers and twirls to idle. **Total ≈74 t** |

Key gaps: glyph → release = 25 t; beam → release = 8 t; release → line = 4 t; the spear is away ≈24 t.

**Geometry** [obs]:
- A straight line from her hand toward the player, ≥15 b long, at chest height.
- The visible core is ≈0.5 b thick; use a ≈1 b-wide hit line.
- It is effectively hitscan: ≥60 m/s, i.e. 3-5 b/t, or an instant line with a 1-2 t sweep.
- Not observed: the aim-lock time, piercing, and whether the returning spear deals damage.

**Damage**: not observed. The player was not hit.

**FX** [obs]:
- **Glyph**: core `#F7EAA9`, mid `#AA9B58`.
- **Trail**: core `#FDF495`, mid `#C7AC57`, edge `#9F7A32`; cubes `#FCF09B`.
- **Release**: white `#FFFFFD` burst.
- **Launch disc**: gold ring outline.

**Sounds** [obs]:

| event | m1 time | character | vanilla composition |
|---|---|---|---|
| spin whooshes | 5.68-5.82, 5.98 s | — | `entity.player.attack.sweep` (p 0.6-0.8) + `item.trident.riptide_1` (p 1.4, quiet) |
| glyph | 6.75-7.15 s | glittery ticks | `block.amethyst_block.resonate` |
| glyph burst | 7.18-7.30 s | bright burst | `block.beacon.activate` (p 1.8) |
| release + flight | 7.40-7.95 s | crack, then a crackling whoosh | `item.trident.throw` (p 0.7) + `entity.firework_rocket.blast` (p 1.2) + `item.trident.riptide_2` |
| return / catch | 8.55-9.16 s | soft whoosh, low whoomp | `item.trident.return` (p 0.8) |

**Voice**: none audible.

**Evidence**: m1 5.30-9.47 s only. Night forest lighting; `sheet_javelin_*.jpg`, `javelin_keyframes.jpg`, `k_f0380/0412/0422/0446/0456/0460/0520`.

---------------------------------------------------------------------------------------------------

## 5. P3 공간을 집행하는 시련: melee spear slam

**PDF** [pdf]: "근접 거리에서 바위 창을 냅다 꽂는다." (slams the Geo spear down at melee range).

**Selection** [pdf+obs]: melee range. She idled 2-3 m in front of the player before the raise.

**Timeline** (m1 C; rel 0 = raise, m1 11.02 s / t220):

| rel t | [m1 t] | event |
|---|---|---|
| 0-7 | 220-227 | **Raise**: spear swung up and back over her head (two hands, torso pitched +30°) |
| **8.7** | **228.7** | **Ground ring telegraph** appears: a thin gold ellipse line with a faint amber fill, centred on the landing point |
| 12-21 | 232-241 | Hold overhead, spear vertical, lens-flare glint on the blade |
| 22-25 | 242-245 | **Downswing**: the spear tilts forward and drives down |
| **26** | **246** | **IMPACT**: a vertical gold pillar at the landing point (≈0.6 b wide, ≥2 BH tall); the ring vanishes |
| 27 | 247 | White-gold flash fills the ring area |
| 28-32 | 248-252 | Gold burst; **gold crystal blades jut radially out of the ground**; gold cubes and dark rock chunks |
| 32-48 | 252-268 | **The spear stays stuck in the ground**; sparkles at the tip |
| 48-54 | 268-274 | Pulls the spear out |
| 54-70 | 274-290 | Twirls and returns to idle. **Total ≈70 t** |

Key gaps: ring → impact = **17-18 t**; raise → impact = 26 t; recovery ≈44 t.

**Geometry** [obs]:
- A disc of **r ≈5 b** (4.8-5.6), centred **≈3.5 b in front of her**, about one spear length; that puts it on or near the player.
- It extends to ≈1.5 b behind her.
- The ring line is ≈0.1 b thick.

**Damage**: not observed. The player left the ring.

**FX** [obs]:
- **Ring**: rim `#EDD559` / `#F1D135`, faint amber fill.
- **Impact**: core `#FCF8AE`, mid `#DCC773`, edge `#A68E42`.
- **Sparkles**: 4-point stars at the planted tip.

**Sounds** [obs]:

| event | m1 time | character | vanilla composition |
|---|---|---|---|
| raise | whoosh 11.17-11.30 s | — | — |
| charge | 11.57-12.13 s | rising shimmer | `block.beacon.power_select` + `block.respawn_anchor.charge` (p 1.5) |
| impact | onset 12.21 s, peak 12.22-12.39 s, 0.6 s decay | deep boom + crystal crack | `entity.generic.explode` (p 0.9) + `block.amethyst_cluster.break` + `item.trident.thunder` (v 0.3) |
| twinkles | 13.1-13.2 s | — | — |
| pull-out | 13.35-13.40 s | low thud | `block.chain.break` (p 0.6) + `block.stone.break` |
| twirl | whooshes 13.77-14.08 s | — | twirl composition |

**Voice**: none audible.

**Evidence**: m1 9.85-14.50 s only. `sheet_plant_*.jpg`, `measure_plant_ring_*.jpg`, `k_f0676/0690/0712/0738/0740/0746/0790/0830`.

---------------------------------------------------------------------------------------------------

## 6. P4 어둠 속에서 퍼지는 공간: forced pull + two 360° swings

**PDF** [pdf]: "캐릭터가 멀리 있을 경우 대상을 파수꾼에게 근접 거리 강제로 이동시킨다. 이어서 창을 2회 휘두른다." (if the character is far, she forces it to melee range, then swings the spear twice).

**Selection** [pdf+obs]: far. The player started ≈8-10 m away (≈3-4 BH).

### 6.1 Pull

Timeline (m1 D, real time; rel 0 = m1 15.50 s / t310). Do **not** time from the 0.70× slowed replay at 17.93-21.8 s.

| rel t | [m1 t] | event |
|---|---|---|
| −0.6 | 309.4 | Crackling hiss starts (+28 dB above 8 kHz at rel 4.4) |
| 0.7 | 310.7 | Red haze appears behind her |
| 2-14 | 312-324 | Red mist swirls and intensifies, with crimson/pink energy arcs; **she lifts her free (corrupted) hand as an open claw**; a low rumble builds (rel 6-28) |
| **10.7** | **320.7** | **Cage starts**: the first black cube with glowing red edges appears at the player's feet |
| 12-17 | 322-327 | 5-8 cubes (0.4-0.6 b) stack up the legs to the torso; red cubes also float around the boss |
| 17-27 | 327-337 | **Cage complete**: a column of black cubes encasing the player (≈1.2× player height, 0.7× wide) with a red glow halo |
| 26-28 | 336-338 | Red concave-diamond screen vignette closes in |
| **28-30** | **338-340** | **White full-screen flash** (≈5 frames) |
| 30-31 | 340-341 | Orange-red field with a white 4-point star outline and peach cubes; sound burst at rel 30.6 |
| 31-32 | 341-342 | Filled red diamond over the scene |
| **32** | **342** | **The player has been relocated ≈1 b in front of her, facing her** |
| 32-40 | 342-350 | Vignette fades; the hiss decays |
| 32-≈60 | 342-≈370 | Glowing red/orange cubes drift and dissolve |

Key gaps: aura → cage = 10 t; **cage start → teleport = 18 t (cage → flash)**, ≈21 t to the relocation; aura → relocated = 32 t.

**Geometry**:
- The pull targets the player and is not an AoE.
- Destination ≈1 b in front of the boss, the player facing her.
- **The pull itself deals no damage** [obs].
- Not observed: whether a dash can break it, its maximum range, and what happens with line-of-sight blockers.

### 6.2 Two swings

Timeline (m1 E; rel 0' = wind-up, m1 22.50 s / t450):

| rel t | [m1 t] | event |
|---|---|---|
| 0-5 | 450-455 | Wind-up: spear lifted and laid horizontally behind her shoulders (tip back-left), wing raised high |
| 5-19 | 455-469 | **Hold** (telegraph, 0.72 s) |
| **20-24** | **470-474** | **Swing 1**, forehand (her left → right): a waist-height **full-circle** gold crescent |
| 24-29 | 474-479 | Trail fades: gold sparkles and dark cubes |
| 29-33 | 479-483 | Spear carried to her right side |
| **33-39** | **483-489** | **Swing 2**, backhand: crescent rising low-right to high-left, thicker, **full circle again** |
| 39-51 | 489-501 | Recovery: spear up vertical, twirl, idle. **Swing part ≈51 t** |

Key gaps: wind-up → swing 1 = 20 t; **swing 1 → swing 2 = 14-15 t**.

**Pull → swing delay: uncertain.**
- If the clip is real time after the replay's flash (21.12 s), relocation → wind-up = 28 t, and → swing 1 = 48 t.
- In that time the player ran from 1 m to 6-7 m and escaped both swings. That points to a shorter real delay, or to the replay still being slowed (C18).

**Geometry** [obs]:
- **Swings**: a horizontal disc centred on the boss, **r ≈5-6 b**, **360°**, height band from the ground to ≈1.5 b.
- These are **not** the 180-210° guard sweep of P6.

**Damage**: not observed. The player was at 6-7 m and was not hit.

**FX** [obs]:
- **Red "space" energy**: mist `#641E19` / `#68292E` / `#81474A`; aura `#751D22` → `#9F465A` → `#E37C95`.
- **Cage**: edges `#B82F3A`, faces `#0F0001`, glow `#600005`.
- **Screen effects**:
  - vignette `#820C19` / `#892E40` / `#A9555B`;
  - flash `#FFF4E2`;
  - field `#EE8262` / `#E64A2E`, cubes `#FABF9F`;
  - diamond `#87150D` / `#B92C39` / `#ED755D`.
- **Floating cubes**: `#D34B23` / `#C04B29` / `#61190E`.
- **Swing trail**: core `#FDF6A6`, mid `#DDBC78`, edge `#A37C4E`.

**Sounds** [obs]:

| event | m1 time | character | vanilla composition |
|---|---|---|---|
| pull aura | 15.47-17.05 s | continuous crackling hiss + rising rumble | `block.respawn_anchor.charge`, `block.fire.ambient` loop, `entity.warden.sonic_charge` (p 1.4, quiet), `block.portal.trigger` (short) |
| teleport | 16.92-17.05 s | burst, then a sudden drop | `entity.enderman.teleport` (p 0.6) + `block.respawn_anchor.deplete` + `entity.illusioner.mirror_move` |
| swing 1 | low thump 23.39-23.63 s; peak 23.61-23.67 s | — | `entity.player.attack.sweep` (p 0.6-0.8) + `item.trident.riptide_1` (p 1.4, quiet) |
| swing 2 | 24.18-24.33 s | — | as swing 1 |

**Voice**: none audible.

**Evidence**:
- m1 14.73-17.50 s: pull, real time.
- m1 17.93-21.8 s: the same pull replayed at 0.70×. **Not for timing.**
- m1 22.50-25.05 s: the two swings.
- Sheets: `sheet_pull_cage_*.jpg`, `sheet_pull_flash_*.jpg`, `sheet_swing1/2_*.jpg`, `measure_swing_arcs_f1419_f1461.jpg`.

---------------------------------------------------------------------------------------------------

## 7. P5 하늘을 심판하는 자: fly to the player and slam

**PDF** [pdf]: "멀리 있을 경우 직접 날아와서 캐릭터에게 바위 창을 냅다 꽂는다." (if far, she flies over and slams the Geo spear into the character).

**Selection** [pdf+obs]: far. The player walked back to ≈10-12 m (≈4 BH) before the pattern.

**Timeline** (m1 F; rel 0 = m1 26.45 s / t529):

| rel t | [m1 t] | event |
|---|---|---|
| 0-2 | 529-531 | Spear raised vertical (tip up); black-brown cubes climb the shaft |
| 2-4 | 531-533 | **Glint**: 4-point star flare on the spear head |
| 4-12 | 533-541 | Holds the vertical spear; dark cubes keep rising |
| 12-16 | 541-545 | Gold spiral ribbons wind around her body; ground glow at her feet |
| 16-19 | 545-548 | **Vertical gold beam** erupts up through her (3-4 BH tall, ≈0.5 b wide) with crescent arcs |
| 19-23 | 548-552 | **Take-off**: rockets straight up out of view, with a dark-cube trail |
| **20.7** | **549.7** | **Target ring** appears under the **player** (r ≈1 b). **Its position is locked here** |
| 22-24 | 551-553 | Ring at r 2-3 b |
| 26-40 | 555-569 | Ring full at **r ≈4.5 b**: bright rim, translucent fill; gold 4-point sparkles fall from the sky onto the centre. **The ring does not follow the player.** |
| 39-41 | 568-570 | Descent: a gold light pillar slams onto the ring centre; she drops spear-first |
| **41** | **570** | **IMPACT** at the ring centre |
| 42-46 | 571-575 | Explosion: gold flame-like spikes and rock debris |
| 47-51 | 576-580 | **Ground spike ring**: gold/orange crystal shards 0.5-1.5 b tall, out to r 4-5 b |
| 51-71 | 580-600 | Spikes linger; she stands at the centre with the spear planted |
| 71-79 | 600-608 | Spikes fade; she pulls the spear out |
| 79-101 | 608-630 | Twirls and lowers to idle. **Total ≈101 t** |

Key gaps: glint → beam = 14 t; beam → gone = 7 t; **ring spawn → impact = 20 t** (5 t growth + 15 t at full size); impact → spikes = 6 t; spikes live 24-30 t.

**Geometry** [obs]:
- A disc of **r ≈4.5 b** at the player's position at ring spawn, damaging on impact.
- Whether the lingering spikes deal damage is not observed.
- Flight height: out of the frame, ≥6 b. The model suggests y +6 b.

**Damage**: not observed. The player escaped sideways.

**FX** [obs]:
- **Beam**: core `#F9E8A5`, mid `#CBA582`.
- **Ring**: rim `#DBCE63`, fill `#C5A47B` (≈30-40 % alpha), edge `#9F7868`.
- **Descent pillar**: `#FDF5B4` / `#DABA83` / `#A36E29`.
- **Spikes**: `#F9E293` / `#C8975E` / `#A16B41`, saturated `#F3C242`.

**Sounds** [obs]:

| event | m1 time | character | vanilla composition |
|---|---|---|---|
| ascent | 27.28-27.56 s | rising whoosh burst | `entity.ender_dragon.flap` (p 1.3) + `item.trident.riptide_3` |
| fall | 27.99-28.27 s | falling whistle | `block.beacon.deactivate` (p 1.8) |
| impact | peak 28.66-28.80 s | boom | `entity.generic.explode` + `entity.zombie.attack_iron_door` (p 0.6) |
| spikes | crackle tail to 29.24 s | crackling crystals | `block.pointed_dripstone.land` ×n + `block.amethyst_cluster.place` |
| pull-out | thud 30.36 s | — | pull-out composition |
| twirl | whoosh 30.81 s | — | twirl composition |

**Voice**: none audible.

**Evidence**:
- m1 26.45-31.52 s only.
- m1 says the clip "continues into m2". m2 clip A opens at ≈97 % HP after m1 ends at 97.5 %, so they may be one take.
- Sheets: `sheet_fly_*.jpg`, `measure_fly_ring_f1680.jpg`, `k_f1599/1626/1636/1645/1650/1680/1710/1740/1790`.

---------------------------------------------------------------------------------------------------

## 8. P6 파수 모드 – 기록하고 판결하는 자: guard mode and element record

**PDF** [pdf]: "주변에 창을 돌리고 파수 모드로 진입한다. 파수 모드는 5초간 지속되며 시간이 지나면 창을 휘두른다. 원소 기록하여 불, 물, 얼음, 번개의 3회에 걸쳐서 공격하면 해당 창이 인첸트되고 창을 휘두른다. 이미 기록된 원소는 9회의 원소 피해를 입혀야지 다시 기록할 수 있다."

**Guide captions** [pdf]:
- 파수 모드 I: "주변에 창을 돌리고 파수 모드에 진입한다. 파수 모드 지속시간 5초 / 원소 기록 시작: 3회의 원소 피해(불, 물, 번개, 얼음)를 입히면 기록 완료. 기록 종료 후 휘두르기 공격".
- 파수 모드 II: "이미 기록된 원소는 9회의 원소 피해…를 입혀야 다시 기록할 수 있다 / 새로운 원소는 마찬가지로 3회의 피해로 기록 가능".

**Selection**:
- Any distance: 4-6 m in clip A, 2-3 m in clip B [obs].
- It runs twice per cycle, then chaos [pdf].
- In m2 clip B the two guards ran back to back (guard I swing end → guard II entry = **43 t**), and guard I started at **100 % boss HP** [obs].

### 8.1 Timeline, timeout case (m2 clip A; rel 0 = twirl start, m2 0.70 s / t14)

| rel t | [m2 t] | event |
|---|---|---|
| 0-16 | 14-30 | **Entry twirl**: spear to horizontal, vertical overhead, then twirled like a baton in front of her (the hand slides to mid-shaft) |
| 16-35 | 30-48.7 | **Gold spin discs**: the spear trail draws vertical gold discs ⌀ ≈3-3.5 b, centred 1-1.5 b from her, in sequence to her right, front and around; gold crystal spikes, debris and small dark-red cubes kick up where they touch the floor (rel 28-35) |
| 35-44 | 48.7-58 | **Flat gold ground ring** around her, **r ≈4.5 b**, ≈0.15 b thick, expanding and fading over ≈0.4 s. **No damage** (it passed under the player) |
| 44-50 | 58-64.3 | Settles into the guard pose |
| **50-154** | **64.3-168.3** | **GUARD ACTIVE, 104 t measured** (PDF 5 s = 100 t). Record counting runs; she drifts toward the player at ≈0.8-1 m/s |
| 139-154 | 153-168 | Guard-end charge: the gold glow intensifies; a big pale-gold 4-point sigil (`#FFFDBF`) flares at her shield/chest at ≈rel 146 |
| 154 | 168.3 | Timeout; the HUD icon disappears |
| 154-173 | 168-187 | **Wind-up (19 t)**: spear lifted high, over her head and back, cocked behind her right shoulder |
| **173-178** | **187-192** | **GOLD SWEEP ACTIVE (5 t)**. The player was hit at rel 177 (m2 f574) |
| 178-198 | 192-212 | Recovery: FX gone by rel 182; spear held level pointing to her right; she returns to the low stance |

### 8.2 Timeline, record case (m2 clip B; R = record complete, m2 14.80 s / t296)

| rel t | [m2 t] | event |
|---|---|---|
| guard −51 … 0 | 244.7-296 | Guard active. Electro hits are counted at 13.50 and 14.17 s (each +120° on the HUD ring); the 3rd completes the record **2.57 s into the guard**, and **she swings at once** |
| **R** | **296** | **Record complete**: a white-violet starburst on her (`#FCE4FC` core, `#E484FC` rays, ≈0.5 BH); the HUD icon flashes white |
| R+4…R+6 | 300-302.4 | **Enchant**: a horizontal violet-white light line through her and along the spear |
| R+7…R+19 | 302.7-315 | Wind-up: spear raised high to her left with a violet glow; pauldron gems turn magenta |
| **R+19…R+27** | **315.3-323.3** | **ELECTRO SWEEP ACTIVE (8 t)**: a violet crescent with forked lightning striking the ground inside the arc. The player was hit at ≈R+24 |
| R+27…R+46 | 323-342 | Recovery: violet arcs crackle on the ground until ≈R+42 |
| R+46…R+70 | 342-366 | Reposition: ≈2 m glide toward the player |

### 8.3 Guard II, re-record of an already-recorded element (m2 B10-B17)
| m2 time / tick | event |
|---|---|
| t366-388 | Entry spin: **always gold**, even with Electro remembered |
| t≈380-388 | Gold ground ring |
| t388-400.7 | Settle. Entry total ≈35 t, against 50 t in clip A |
| t400.7 | Guard active. The **wing and pauldron gems glow magenta** because the element is remembered |
| — | 9 Electro hits are counted at ≈0.42-0.67 s intervals, +40° each |
| t479.3 | Re-record complete, **3.93 s into the guard** |
| t481.7-486 | Enchant: a violet-white ring burst around her waist (r ≈0.5 BH) plus the line |
| t486.7-498.3 | Wind-up |
| **t498.7-506.7** | **Sweep active** (again R+19…R+27) |
| t506.7-520 | Recovery |
| t526.7 | Leap to the centre (§9) |

### 8.4 Record rules
- **Counting** [pdf+obs]:
  - Elements: Pyro, Hydro, Electro and Cryo only.
  - A **new** element needs **3** elemental hits.
  - An element **already recorded** needs **9**.
  - Counted hits were never closer than ≈0.42 s apart (≈8-9 t): the game rate-limits counting per element.
- **Effect** [obs]: on completion the swing comes **19-20 t later**, without waiting for the timer. The swing uses the recorded element (colour, lightning, and the player gets that element's damage).
- **Memory**: the recorded element is remembered across guards (the gems stay magenta in guard II) and feeds the chaos stars (§9).
- **Not observed**:
  - two **different** elements recorded;
  - what guard II does to slot B when the re-record fails;
  - Pyro and Hydro looks.

### 8.5 Geometry
- **Entry**: the discs and the r 4.5 b ground ring are **non-damaging** telegraphs [obs].
- **Sweep (gold and element)**: a **180-210° front arc**, **r ≈4.5-5 b**, waist to ground height, swept from her left to her right (screen right → left) in 5 t (gold) or 8 t (element) [obs].
- The gold version adds a row of vertical crystal spikes (0.5-1.5 b) along the arc edge.

### 8.6 Damage [obs]
- Gold sweep: −4003 (20.8 % of 19 268, Linnea).
- Electro sweep: −7417, twice (30.6 % of 24 218, Clorinde).
- In absolute terms the enchanted sweep hit ≈1.85× as hard (same level-90 DEF class).

### 8.7 FX [obs]
- **Guard pose**:
  - spear diagonal, pointing up and to her right at 35-45°;
  - wing raised and opened (tiers 70° / 85° / 105°, `model.md` §8);
  - a gold aura on the whole body and the spear (`#E4B43C` → `#FCFC84`), small floating gold square motes (≈0.15 b, `#E4CC54`);
  - shield glowing gold.
- **Remembered element**: the shield/wing gems are tinted with it (Electro `#E484FC`, core `#FAE6FA`).
- **Spin discs**: rim `#FCE484` / `#E4B43C` with a white-hot edge; fill `#B49C54` / `#9C843C`.
- **Gold sweep**: `#CC9C3C`, `#E4B43C`, `#E4B454`, highlight `#FCFC84`, white core; spikes `#FCE484`.
- **Electro sweep**: `#E484FC`, `#CC6CFC`, `#B454FC`, `#CC84FC`, shadows `#6C54CC` / `#5454B4`, core `#FCE4FC`; forked bolts, violet shards.
- **HUD**:
  - black disc with a pale-yellow star while recording nothing;
  - element icon with a lavender (`#B9A0E6`) ring filling clockwise, +120° (new) or +40° (re-record) per hit;
  - white flash on completion;
  - the icon stays, with an empty ring, after the guard.

### 8.8 Sounds [obs]

| event | m2 time | character | vanilla composition |
|---|---|---|---|
| entry twirl | 1.05-1.25 s (whooshes at 0.99, 1.415, 1.625) | — | `item.trident.riptide_1` (p 0.8) + low `entity.player.attack.sweep` per half-turn |
| spin discs | 1.87, 2.04, 2.49, 2.61 s | metallic "shing" | `item.trident.throw` + `block.amethyst_block.chime` (p 1.4-1.8), `entity.illusioner.cast_spell` |
| ground ring | 2.69-2.86 s | sub thumps | low-pitch `block.amethyst_block.place`, `entity.iron_golem.step` |
| gold wind-up | 9.09 s | swell | `item.trident.riptide_2` (p 0.7) |
| **gold hit** | 9.49-9.60 s | heavy crunching sweep | `entity.player.attack.sweep` (0.6) + `block.pointed_dripstone.land` / `block.basalt.break` + quiet `entity.generic.explode` (p 1.3) |
| record complete | 14.89-14.94 s | zap | `entity.lightning_bolt.impact` (quiet, p 1.5) + `block.respawn_anchor.charge` |
| enchant | 15.04-15.12 s | deep sub thump | `block.beacon.activate` (p 1.2) + short `entity.warden.sonic_charge` |
| **Electro hit** | onset 15.82, peak 16.01-16.07, tail 16.15-16.27 s | whoosh into an electric slash | sweep + `entity.lightning_bolt.impact` (p 1.6-2.0, v 0.5) + crackle (`block.copper_bulb.turn_on` / `entity.breeze.wind_burst`) |
| swing #2 | 25.16-25.22 s | same as the Electro hit | same |

Tones near the guard starts are BGM, not a guard chime.

**Voice** [pdf]: 파수 모드 진입 "**기록하여 판결할 지어다.**" Not audible in m2.

**Evidence**:
- m2 0.70-10.6 s: clip A, no record, gold sweep.
- m2 11.85-17.10 s: guard I, Electro record. Only the tail of the entry is shown.
- m2 18.30-26.0 s: guard II, Electro re-record.
- Sheets: `n_guardentry1_*`, `t_guardentry_quad`, `b_180-500`, `o_goldswing_*`, `f_880-1000`, `i_1420-1560`, `q_record_icon_strip.png`.

---------------------------------------------------------------------------------------------------

## 9. P7 혼돈 – 신성한 붉은 에너지: chaos, element stars, break / fail

**PDF** [pdf]: "파수 패턴 2회 이후, 중앙으로 이동하여 활성 원소별 2개 소환. 기록이 완료된 원소는 상시 부착된다. 활성화되지 못한 원소는 타성 원소별을 소환한다. 소환시 모든 내성이 80% 증가한다. 기록 파괴 제한 시간은 17.5초이며 만약 시간안에 파괴 못하면 파괴 실패한 원소 개수만큼 강력한 창을 내려꽂는다. 첫 번째 별과 두 번째 별 원소 파괴하면 보스는 최대 체력 6%/18%만큼 피해를 주고 11초간 그로기 상태가 된다."

**Guide captions** [pdf]:
- 혼돈: "파수 모드 패턴 2회 반복 후 중앙으로 이동 / 활성 원소별 2개 소환 (기록 원소 상시 부착 & 면역), 파괴 시간 제한 17.5초".
- 파괴 성공: "첫 번째 원소별 파괴 시 최대 체력 6% 대미지 / 두 번째 원소별 파괴 시 최대 체력 18% 대미지 | 합계 최대 체력 24% / 기록 원소 대미지".
- 타성 원소별: "원소 기록 실패 시 타성 원소별 소환 (**모든 저항 80%**) / 상시 부착과 면역 요소 없음".
- 파괴 실패: "원소별 파괴 실패 시 파괴에 실패한 원소별 개수만큼 범위 공격 / 공격 범위 안 넓음, 벗어나기 쉬움, 회피도 가능".

**Selection**: immediately after the 2nd guard sweep (20 t later in m2) [obs+pdf].

### 9.1 Entry: two observed variants

**Variant A** (m2 B18-B24, attempt #1, Electro; from range). rel 0 = leap, m2 26.33 s / t526.7.

| rel t | [m2 t] | event |
|---|---|---|
| 0-9 | 526.7-536 | **Leap** straight up: spear vertical, wings flaring, red cubes burst around her |
| 9-31 | 536-558 | Low **arcing flight** to the centre star (≈10-15 b in ≈1.3 s, 8-10 b/s), trailing red/black voxel cubes (partly off-frame) |
| **32** | **559** | **Lands on the centre star**: the heaviest boom in m2 |
| 33-63 | 560-589 | **Centre charge (≈30 t)**: spear held level; red-orange flare on the spear head at rel 40; from rel 49 a red orb with blocky red cubes gathers at her hand/chest (the "+" sigil forming) |
| 63-68 | 590-595 | **Rise** to a hover with the feet ≈1 BH (3 b) up; red translucent light shafts hang below her |
| **69** | **595.7** | **Chaos timer starts** (350 t) |
| 70-73 | 597-600 | **2 stars spawn** on the centre beneath her; the world tints crimson |
| ≈85 → | 612 → | Cube streams start |

**Variant B** (m3 G, attempt #3, nothing recorded → inert stars; low glide). rel 0 = arrival over the centre, m3 27.73 s / t554.7. The approach was already ≥8 b/s from ≥4.5 b out, and the clip starts after a dissolve.

| rel t | [m3 t] | event |
|---|---|---|
| −11-0 | 543.7-554.7 | Low glide (feet 0-0.2 BH up), spear raised behind her right shoulder, red voxel cluster pulsing on the chest |
| 0-1 | 554.7-555.5 | Stops over the centre star; the timer icon appears (empty); red cubes burst around the legs |
| 1-9 | 555.7-564 | **Red crescent shards** (0.3-0.5 BH, `#C01830`), 6-10 flung radially |
| 2-12 | 556.7-566.7 | **Rise** to a hover with the feet ≈1.0-1.1 BH up (10 t) |
| 3-6 | 558-561 | Gold-orange flare at her head/halo (≈0.5 BH) throwing gold and red cubes; the crimson sky starts |
| **6-9** | **561-564** | **Red cross sigil assembles** above her head (≈3 t); **timer fill starts at rel 6** |
| 8-16 | 562.7-570.7 | **Stars spawn**: ≈0.3 b voxel clusters stretch upward into 4-point crystals over 8 t; HP bars at rel 8-9 |
| 16-33 | 570.7-588 | Static hover, spear horizontal behind her shoulders |
| 33 → | 588 → | Cube streams start |

In both variants the timer starts within 1-2 t of the stars appearing.

### 9.2 Hold (timer running, 350 t)
**Boss** [obs]:
- Static hover over the centre (feet ≈3 b up), slow bob.
- Wings spread; arms up with the **spear held horizontally behind her shoulders** (crescent to screen right).
- **Red cross sigil** above her head:
  - shape: 5 cubes; ≈0.52 × 0.41 BH;
  - colours: faces `#C21F2A` / `#AE1120`, rims `#6E0001` / `#8B0107`, glow `#E45852`, white 4-point glint `#FDF2EB`;
  - it hides the halo.
- She does not attack.

**Stars** [obs]:
- **2 stars** on the floor directly beneath her, 0.7-1.5 b apart, each with its own small HP bar and aura icon. Look:

  | star | look | size |
  |---|---|---|
  | active Electro | violet crystals with sparks (`#9D3ED6` / `#D282FA` / `#E6BEFA`, orb `#F3CEF9`) | small |
  | active Cryo | icy 4-point crystals (`#DEFFFD` / `#98E6F3` / `#7CC7E2` / `#618CB9`) | large, ≈0.6-0.7 BH |
  | inert, gold (left) | slim 4-point crystal (`#FCE582` / `#F2BB76` / `#E59D78`) | ≈0.38 BH at spawn, ≈0.7 BH at timeout |
  | inert, blue (right) | slim 4-point crystal (`#A6CEFD` / `#96ACF2` / `#8D83D9`) | ≈0.38 BH at spawn, ≈0.7 BH at timeout |

  The inert stars **grow** over the chaos.
- **Active stars**: the recorded element is permanently attached [pdf]; they are **immune** to it [pdf/inf]. Hydro hits on the Electro stars showed 감전 plus "면역" pop-ups, and the Hydro numbers 8355 and 16691 broke them.
- **Inert stars**: **all RES +80 %**, no aura, no immunity [pdf caption].
- **Element mapping, observed**:
  - Electro recorded (twice) → 2 Electro stars;
  - Cryo recorded → 2 Cryo stars;
  - nothing recorded → 1 gold + 1 blue inert star.
  - Mixed cases were never seen.

**Ambience** [obs]:
- Crimson sky dome: `#963246`, `#7E2539`, `#8E1C31`, `#922037`, `#9D1D35`; at dusk the floor also turns crimson with glowing orange crack lines.
- **Cube streams**:
  - shape: snake chains of 8-12 cubes, led by a gold cube (`#E4CC54`, 0.5-0.8 b), followed by hollow red-edged cubes (`#FC5454` on `#4C2521`) and embers;
  - motion: they arc out from around her, sweep the arena and dive to the floor near the player at 6-10 b/s, with 2-5 visible at once.
  - **No player damage was observed** (C8).

**HUD** [obs]: a timer icon whose white ring fills clockwise over 17.5 s (≈20.6°/s).

### 9.3 Star break → boss damage (identical every time) [obs]
Let S be the tick a star dies.

| tick | event |
|---|---|
| S+1 | A 4-point starburst on the boss's chest in the star's colour: ≈0.5-0.6 BH; the inert break gives ≈2 BH of white rays |
| **S+5** | **Boss HP −6 % (1st star) or −18 % (2nd star)**, fixed amounts, shown as a damage number in the star's colour, with a thin ring around her (r 0.35-0.5 BH) |
| S+5…S+15 | Elemental sparks and arcs on her |
| **1st star** | Chaos continues: timer, sigil and streams stay; the sigil dims briefly |
| **2nd star** | The timer icon goes at once. She hangs ≈6 t, then **falls ≈1 BH** (drifting ≤1 BH sideways) and lands **16-20 t** after the break; no impact AoE. The sky dome fades at S+14…S+18 (attempt #1), or a crimson tint lingers to ≈S+136 (attempt #2). Sigil and streams vanish → **groggy** (§10) |

- Two stars can break 3 t apart; each resolves on its own (m3 E).
- Order does not matter: whichever breaks first deals 6 %.

**Break colours** [obs]:
- Electro: `#C85DCC` / `#852E83` / `#DBC9ED`.
- Cryo: `#A2FEFD` / `#9DD4E2` / `#EBFAFA`.
- Inert: `#FBFFFF` / `#8D808A`.

### 9.4 Timeout → fail spears (m4; T0 = timer full, m4 0.500 s / t10)
| T0 + t | event |
|---|---|
| 0-5 | Timer icon glows pale pink |
| 6 | Icon removed |
| 7 | **Stars flash white** (2 t); their HP bars go |
| 7-10 | Stars collapse into gold voxel clusters (≈1 b) |
| 10-14 | Voxels darken to black with red edges; she twists and sweeps her wing across her front; the streams stop (≈+10…+15) |
| 15 | Sigil breaks into 3 cubes and fades |
| 15-17 | **Absorption**: two V-shaped cube chains (gold-led) fly from the stars' spot into her chest (≈20 b/s) |
| 18-19 | Red gyroscope ring around her upper body (1.3 BH, `#B30B2E`) |
| 19-21 | White-gold 4-point starburst on her chest (rays ≈0.8 BH) |
| 21-25 | Crimson smoke plumes ≈2 BH wide like wings; a red horizontal light line; **the sky haze is removed**; she rises 0.5-0.7 BH above her chaos hover |
| **Per surviving star k** (k = 0, 1, …; the k-th spear is ≈31 t after the previous one): | |
| 23 + 31k | A gold cube column forms (under or through her for k = 0, high above her for k = 1) |
| 25 + 31k | A red blade grows out of it: a **giant copy of her spear, point down**, ≥8-10 b long (head 3.0-3.4 b, crescent span 2 b), hanging with its tip **3.6-3.9 b above the target**. **Ground decal** appears: a red concave 4-point star **centred on the player** with one arm pointing at the arena centre. Its side arms open from ±2.7 b to >±9 b in 6 t (≈20 b wide). **The target is locked here** |
| 37-40 + 31k | The spear turns from red to **the star's colour** (gold → gold; blue → pink → violet → blue) |
| **49 + 31k** | **Drop in ≤1 t + IMPACT** at the locked point: flash column and starburst rays |
| 50-51 + 31k | Gold (or blue) dome of light, ≈2.9 b wide and tall |
| 51-54 + 31k | Blast: **X of crossed light beams** 8-10 b tall; a spike field (gold ±8 b; blue ice splash ±4 b); rock debris |
| 54-62 + 31k | Residue: crimson floor with gold cracks (or blue cracks); the giant spear stays planted ≈30 t, then dissolves upward into cubes over ≈10 t |

- During the fail she descends to stand on the floor at the centre (≈+55 t).
- For spear 2 she holds her spear across her shoulders, then raises it vertically overhead in the last ≈0.3 s before the drop.
- She **never attacks with her own spear** in this sequence.
- After the last impact (+80 t): she leaves the centre at ≈+90 t, glides to ≈2 b from the player by ≈+126 t, and resumes normal patterns.
- Boss HP is unchanged (no heal, no shield).
- Measured decal-rim leads: 22 t (spear 1) and 16 t (spear 2).

**Fail geometry** [obs+pdf]:
- The decal is huge, but the caption says the attack range is small, easy to leave and dodgeable. The player escaped each spear with one 2-2.5 b side dash while still inside the decal.
- So the **hit = a cylinder of r ≈2.5-3 b around the impact point** (the dome ≈2.9 b); the decal is visual.

**Fail damage**: not observed (the player was never hit).

### 9.5 Sounds

**Chaos entry and hold** [obs]:

| event | time | character | vanilla composition |
|---|---|---|---|
| leap | m2 26.27-26.57 s | soft mid/high whoosh | `entity.phantom.flap`, short `item.elytra.flying` |
| **landing** | **m2 27.95-28.17 s** | strongest sub event in m2 | `entity.generic.explode` (p 0.6, v 0.6) + `block.anvil.land` (p 0.5) |
| red charge | m2 28.68-28.81 s | high whine over a hiss | `block.beacon.ambient` / `block.respawn_anchor.charge` (p 1.5) |
| star spawn | m2 29.88-29.92 s | glassy crystalline pop + ticks | `block.amethyst_cluster.break` + `block.amethyst_block.resonate` (p 1.2-1.6) |
| glide arrival (G) | m3 27.9-28.0 s | low/mid swell | `item.trident.riptide_1` (p 0.6) |
| flare + sigil + stars (G) | m3 28.30-28.45 s | broadband rise | `block.respawn_anchor.charge` + `block.beacon.activate` (p 1.4) + `block.amethyst_cluster.place` ×2 |
| streams | throughout | not isolable | `entity.blaze.shoot` (low pitch, quiet) per stream, `block.chain.place` ticks |

**Star breaks** [obs]:

| event | time | character | vanilla composition |
|---|---|---|---|
| star 2 break | m3 1.00-1.05 s | bright crystalline burst, ≈0.3 s | `block.amethyst_block.break` + `block.glass.break` (p 1.4) + `entity.lightning_bolt.impact` (v 0.3, p 2.0) |
| star 1 break | m3 6.78 s | full-band hit with sub, then ≈0.5 s sizzle | `entity.generic.explode` (v 0.4, p 1.6) + `block.amethyst_cluster.break` + `block.respawn_anchor.deplete` |
| fall landing | m3 17.55 s | soft air burst | `block.amethyst_block.fall` + quiet `entity.player.attack.knockback` (p 0.8) |

**Fail** [obs] (m4 §7; good AV sync):

| event | m4 time | character | vanilla composition |
|---|---|---|---|
| expiry | — | nothing audible | `block.respawn_anchor.deplete` (p 0.7) + quiet `block.bell.resonate` |
| absorb burst | 1.55-1.62 s | short bright burst | `block.beacon.activate` (p 1.6) + `entity.evoker.cast_spell`; smoke `entity.wither.shoot` (p 0.5, v 0.3) |
| spear forms | 1.80-2.22 s | fiery-crystalline roar | `block.respawn_anchor.charge` (0.8) + `block.beacon.power_select` (0.6) + `block.amethyst_block.resonate` (0.8) + quiet `entity.warden.sonic_charge` |
| hang | 2.25-2.55 s | sub drone | `block.beacon.ambient` (p 0.5) loop; colour change `block.amethyst_block.chime` (p 1.5) |
| pre-drop | 2.65-2.90 s | rising whistle | `item.trident.riptide_3` (p 1.4, v 0.5) |
| drop | 2.95-2.97 s | sharp click | `item.trident.hit_ground` (p 0.5) + `entity.lightning_bolt.impact` (p 0.8, v 0.6) |
| gold blast | 3.05-3.70 s | big crash, then crackle and rumble | `entity.generic.explode` (p 0.7) + `block.amethyst_cluster.break` + `block.pointed_dripstone.land` ×3 + quiet `entity.lightning_bolt.thunder` (p 1.6) + `block.basalt.break` |
| blue blast | 4.60-4.75 s | crash | `entity.generic.explode` (0.8) + `block.glass.break` (0.7) + `entity.player.splash.high_speed` + `block.powder_snow.break` |
| icy shimmer | 4.85-5.9 s | glitter | `block.amethyst_block.chime` (p 1.6-2.0) ×4-6 |

**Voice**: none audible. The PDF lists none specific to chaos. The "attack" lines fit the fail spears [prop].

### 9.6 Evidence
- **Entry**: m2 26.33-30.0 s (variant A); m3 27.18-28.53 s (variant B).
- **Hold**: m2 29.78-40.03 s; m3 0-0.93 s, 5.93-9.92 s, 28.5-32.9 s, 35.6-39.53 s; m4 0-0.48 s.
- **Breaks**:
  - m2 39.517 s: Electro star 1; m3 6.667 s is the replay of the same break;
  - m3 0.95-1.10 s: Electro star 2;
  - m3 16.367 s and 16.50 s: both Cryo stars;
  - m3 34.967 s: blue inert star 1.
- **Fail**: m4 0.5-7.83 s (attempt #3, both inert stars).

---------------------------------------------------------------------------------------------------

## 10. Groggy (그로기)

**PDF / caption** [pdf]: "11초간 그로기 상태" / "기믹 수행 성공 시 11초간 그로기 / 추가 내성 감소 없음" (no extra resistance shred).

**Selection**: the 2nd star breaks inside the 17.5 s window.

**Timeline** (G0 = 2nd break; attempt #2 real time, m3 16.55 s / t331 → 27.03 s):

| G0 + t | [m3 t] | event |
|---|---|---|
| 6-20 | 337-351 | Fall (§9.3); on the floor at the centre by ≈+16…+20 |
| 20-136 | 351-467 | **Pose A**: standing almost upright with a slight slump. The spear is **planted head-down, vertical, at her right**, with the corrupted hand on the upper shaft. Wing low and spread; **halo blazing**. A **crimson pool decal** on the floor: ripples to ≈1 BH and a thin dark-red ring at ≈1.8 BH (5.4 b). She does not move |
| 136-143 | 467-474 | The lighting/tint lifts to normal (7 t); the pool fades |
| 136-169 | 467-500 | **Pose B**: head bowed, torso folded forward, **the gold shield swung in front of her body**, spear vertical behind her |
| **169-181** | **500-512** | **Get-up**: the wing sweeps out and up (widest spread, 1.2-1.4 BH); she lifts into a hover; the spear comes forward into her right hand, pointing down-forward |
| 181-≥210 | 512-541 | Recovered stance: the spear levelled forward by ≈+200. No attack before the cut at +210 |

Attempt #1 (m3 B 1.45-5.85 s): fall, then an **upright variant** with the spear held vertically (not visibly planted) for ≥3.85 s of footage.

**Duration**:
- Caption: **220 t**.
- Measured: get-up starts at 169 t and ends at 181 t; she stays passive to ≥210 t (C12).

**Geometry / damage**:
- No AoE.
- The boss takes normal damage; there is no extra multiplier [pdf].

**FX** [obs]:
- Halo blaze: `#F7E2A6`, core `#FEEAC3`, short rays.
- Pool: `#BD1925` / `#8F3136` / `#B6333A`, highlights `#ECC7C2`, ripple lines `#C25D62`.

**Sounds** [obs]:
- No identifiable boss SFX while groggy. Proposal: a quiet loop of `block.beacon.ambient` (p 0.6).
- Get-up wing whoosh at m3 25.95 s: `entity.phantom.flap` ×2 (p 0.7) + `item.armor.equip_elytra`.
- Landing: soft air burst (§9.5).

**Voice** [pdf]: 그로기 "**나의 주인님이시여...!**" Not audible in m3.

**Evidence**:
- m3 1.45-5.85 s (attempt #1; m3 D 9.93-12.7 s is a duplicate).
- m3 16.75-27.1 s (attempt #2).
- Sheets: `d_groggy_*`, `key_f1148/1300/1440/1530/1622`.

---------------------------------------------------------------------------------------------------

## 11. Death (사망) and voice lines

**Death: PDF only.**
- 사망: "**시련은... 끝났다...**".
- The PDF's story section says the field version (니힐리타) talks during combat and, when the fight ends, "**시련은 끝났다는 말과 함께 날아간다**" (says the trial is over and **flies away**).
- `model.md` §5 proposed a slump plus a dissolve into red cubes and gold motes [prop]. That contradicts the fly-away (C22).
- Recommended [prop]:
  - groggy-A slump for ≈20 t with the line;
  - then the chaos-leap take-off (vertical rise, red/gold cube trail, `entity.ender_dragon.flap` p 1.3 + `item.trident.riptide_3`) out of the arena top;
  - the rig fades to cubes as it leaves.

**All voice lines** [pdf]:
- The PDF calls her the **only automaton-class enemy that speaks**.
- **None is audible in m1-m4**: the BGM masks them, and the guide captions cover the subtitle area.
- Display them as typed subtitles; there is no audio source.

| trigger | line | where to use |
|---|---|---|
| 전투 시작 | 통찰하여, 나의 마음을 보아라. | entrance (§2) |
| 공격 | 처결하노라! | attack starts [prop]: e.g. P5 take-off, P4 cast, P2 release, fail spear 1 |
| 공격 | 사라져라 마땅한 존재여! | as above; alternate randomly with a cooldown [prop] |
| 파수 모드 진입 | 기록하여 판결할 지어다. | P6 entry twirl |
| 그로기 | 나의 주인님이시여...! | groggy start (2nd break) |
| 사망 | 시련은... 끝났다... | death |

---------------------------------------------------------------------------------------------------

## 12. Damage reference (all observed hits)

| hit | Genshin damage | % of target max HP | target |
|---|---|---|---|
| P1 thrust 1 | 2414 | 12.5 % | Linnea, 19 268 HP |
| P1 thrust 2 (+knockdown) | 2767 | 14.4 % | Linnea |
| P6 gold sweep | 4003 | 20.8 % | Linnea |
| P6 Electro sweep | 7417 (×2) | 30.6 % | Clorinde, 24 218 HP |
| star break 1 / 2 (to the boss) | 43 873 / 131 619 | 6 % / 18 % of ≈731 217 | boss |

- All other hits (P2, P3, P4 swings, P5, fail spears, entrance) were dodged or never shown.
- Relative scale [obs]: thrust ≈ 0.6× the gold sweep; enchanted sweep ≈ 1.85× the gold sweep.

---------------------------------------------------------------------------------------------------

## 13. Critic: contradictions between sources

| id | topic | sources disagree | resolution / recommendation |
|---|---|---|---|
| C1 | Boss height | m1: 2.7 m (1.6× player). m2: 3.0 m (1.8×). model: 1.6 body / 1.85 with halo | Use **BH = 3.0 b** (model). Keep AoE radii in metres → blocks 1:1 (they were measured against the player, not BH) |
| C2 | Spear length | m1: 3.5-4 m. m2: 4.3-4.5 m | 4.35 b (model, measured on level-spear frames) |
| C3 | Identity | m2 calls her "Nihilita"; m3/m4 read the HP subtitle as **Melanta** | The PDF's boss card gives `개안자 - 세계 망루의 파수꾼` to the **generic** 파수꾼・타락; its named list also titles Melanta "세계 망루의 파수꾼", so the subtitle alone cannot tell them apart. The wing can: the PDF says Melanta has a **red-brown wing on her right** and Nihilita a white wing on her left. The video boss has a white wing on her **left**, so she is the generic 파수꾼・타락 with the Nihilita look. Mechanics are unaffected; use the generic name and title |
| C4 | Shield side | The task brief says shield on the right | Footage and model: **wing and shield both on her left**; spear in the right (corrupted) hand |
| C5 | Head | m1: "white hair/veil" | Model: crest feathers, no hair, no face (one-eyed diamond) |
| C6 | Chaos entry | m2: leap → flight → **landing** → **≈30 t charge** → rise → timer → stars (stars +41 t after landing). m3 G: low glide → **no landing**, rise at once (10 t) → timer and stars +6…+16 t | G may start after the dissolve, or the entry may depend on distance. m4 places G's player 12-19 b from the centre, so m3's "4.5 m" is an underestimate. Pick one (§15 K10) |
| C7 | Sigil onset | m2: red cross "≈36 s, likely fail build-up" | m3 G: it assembles 7-9 t after arrival. m2 f1836 (30.6 s) already shows it cropped at the top of the frame. **The sigil is present for the whole chaos** |
| C8 | Cube-stream damage | m2: "player keeps losing HP" | m3: no HP change in A/G/H. m2's drop 35 773 → 17 600 (49 %) matches **Neuvillette's charged-attack self-drain, which stops at 50 %**. So the streams did **no observed damage** |
| C9 | Star look and size | m2: Electro = 2 stacked violet cubes + pink orb, 1.1-1.3 m, 1.2-1.5 m apart. m3: inert = slim 4-point crystals 1.1-1.2 m, 0.7 m apart; Cryo ≈2 m, ≈1 m apart. m4: inert ≈2 m at timeout | m3 G shows every star spawning as a voxel cluster that becomes a crystal; m2 f1836 shows small violet 4-point crystals. Recommend **one 4-point crystal model, tinted per element**, spawning from a voxel cluster at ≈1.2 b and growing to ≈2 b over the 350 t |
| C10 | **Who gets +80 % RES** | PDF: "활성화되지 못한 원소는 타성 원소별을 소환한다. 소환시 모든 내성이 80% 증가한다". Caption: "타성 원소별 소환 (**모든 저항 80%**)". `code/elements_damage.md` §0/§6 and `integration.md` §9.3 / D17 give **the boss** `mres 80` during chaos | The caption ties the +80 % to the **inert stars**. Recommend: inert stars take ×0.238 (or a larger HP pool); the boss keeps normal RES. If boss RES is kept for design reasons, mark it as a deliberate deviation |
| C11 | Active-star immunity | Caption "기록 원소 상시 부착 & **면역**"; the integration outline has no immunity | m2 f1878: "면역" pops coincide with 감전 (Electro-Charged ticks are Electro damage), while Hydro numbers broke the Electro stars. So: **immune to the recorded element only**. Add it to the star route |
| C12 | Groggy length | Caption: 11 s (220 t). Measured: get-up starts +169 t, upright +181 t, passive to ≥+210 t | Read 220 t as the no-attack window: pose A/B to ≈+170, get-up 12 t, stance until +220. Or hold the pose for 208 t and get up at the end (pick one, §15 K13) |
| C13 | Guard duration | PDF 5 s; m2 measured 5.2 s (±2 f capture jitter) | 100 t |
| C14 | Guard entry length | Clip A 50 t (twirl → pose); guard II ≈35 t | 40-50 t; use the same for both guards |
| C15 | Fail-spear area | Decal ≈20 b-wide star; caption "공격 범위 안 넓음, 벗어나기 쉬움" | Damage cylinder r 2.5-3 b at the locked point; the decal is visual only |
| C16 | Fail decal lead | 22 t (spear 1) vs 16 t (spear 2) | Use one value ≥20 t for every spear (see K4) |
| C17 | Two different swings | P4 swings: **360°, r 5-6 b**, two hits 14 t apart. P6 sweep: **180-210° front arc, r 4.5-5 b**, one hit | Not a contradiction, but `integration.md` §9.3 only describes the P6 sector. P4 needs its own full-circle hazard |
| C18 | Pull → swing delay | m1 replays the pull at 0.70×; relocation → wind-up measures 28 t only if the clip is real time after the replay. The player got 6-7 m away first | Uncertain. Recommend 10-14 t from relocation to the wind-up (the swings must threaten a pulled player, but stay escapable: wind-up + hold = 20 t) |
| C19 | Chaos timer HUD glyph | m2: red disc with a white glyph. m3: black disc with a rose glyph | Cosmetic; MC uses the bossbar countdown (integration D21/D22) |
| C20 | Entrance telegraph | PDF: appears "어떤 표시도 남기지 않은 상태" (no prior marker) | `integration.md` D13 adds a glint + 24 t ground telegraph. That is fine for fairness (house rule ≥12 t), but it deviates from the source; at least no marker before she appears |
| C21 | Star placement vs reactions | Footage: stars directly under the boss (3 b below), 0.7-1.5 b apart | `elements_damage.md` §10: transformative reactions on a star splash every `rlk_mob` within 4 b, including the other star and (with the body on the floor) the boss. Either accept it or move the stars 3-4 b apart and the body hitbox off the star spot |
| C22 | Death | `model.md` §5: dissolve into cubes | PDF: line, then **flies away**. Prefer the fly-away |
| C23 | P1 "전방위" | PDF "전방위" (omnidirectional) | Video: two aimed thrusts, the 2nd a dive from a new angle above. Implement as an aimed lunge + reposition + diving lunge, not a 360° burst |
| C24 | "Second chaos" (m3 summary) | The task summary says m3 shows "a second chaos start" | m3 §0: segment G is attempt #3, a different fight. **No second cycle has been observed** |

---------------------------------------------------------------------------------------------------

## 14. Critic: gaps (never seen, or unclear)

| id | gap | effect on implementation |
|---|---|---|
| G1 | **Entrance** and **death**: never filmed. **Voice lines**: none audible | Entrance = model §9 / integration §6.1 proposal; death = fly-away (§11); lines as typed subtitles only |
| G2 | **AI order, cooldowns, repetition**: m1 is edited in PDF order. There is no uncut normal-pattern stretch, no second guard→chaos cycle, and nothing on how many normal patterns come before the first guard | The rotation must be designed (K3) |
| G3 | **Damage of P2, P3, P4 swings, P5, fail spears, entrance**; knockback rules (only P1 hit 2 showed a knockdown) | Coefficients must be designed (K17, K16) |
| G4 | **Pyro/Hydro records**; **two different elements**; **one recorded + one failed**; a guard II whose re-record **fails** | Star composition rules must be designed (K6). Pyro/Hydro tints come from model.md §4 (proposed) |
| G5 | **Fail with active (element) stars** (spear colours), **fail with 1 star left** (does the 6 % break still apply? → yes; groggy → no, inferred) | Spear tint = star element (inferred, m4 §5.2); 1 spear for 1 star |
| G6 | **Javelin**: aim-lock time, width, piercing, damage from the returning spear | K23 |
| G7 | **Pull**: escapable by dash or range? Max range? Obstacles? | integration D19 = undodgeable after the tell (K14) |
| G8 | **Thrust**: no ground telegraph; tracking during the coil is unknown | Needs an MC telegraph (K4) |
| G9 | **Guard mode**: is the boss damaged normally (yes, HP moved)? Can she be interrupted? Do discs/ring damage (not observed)? What exactly counts as an "elemental hit" (application vs damage, ICD)? | K5 |
| G10 | **Chaos**: does the boss take damage while hovering? Does anything attack the player (no damage observed)? What if the player stays far away? | K9, K11 |
| G11 | **Star HP values**: Genshin numbers are meaningless in MC | K8 |
| G12 | **Inert star colours**: always gold + blue? (both observations say yes) | Fix gold (left) + blue (right) |
| G13 | **Low-HP behaviour / enrage**: none in the PDF or footage | No HP phases (state it explicitly in the spec) |
| G14 | **Screen effects** (pull vignette and flash, crimson sky): MC has no direct equivalent | K21 |
| G15 | **What follows groggy**: the footage ends 1.5 s into the recovered stance | Resume the normal rotation after ≈20 t |

---------------------------------------------------------------------------------------------------

## 15. Critic: what must be decided for the Minecraft implementation

Defaults are recommendations. "D…" refers to `code/integration.md` §15.

| id | decision | recommended default | notes |
|---|---|---|---|
| K1 | Scale | BH 3.0 b; footage metres → blocks 1:1; idle hover 0.35 b; chaos hover feet 3 b | model.md §1 |
| K2 | Range bands for selection | melee ≤4 b: P3 (and P1); mid 4-8 b: P1, P2; far ≥8 b: P4, P5 (PDF "멀리"); P2 also usable far | Reuse Raiden's `REACH` + `close_in`. Melee patterns close in first (house rule from the Raiden pass) |
| K3 | Rotation / cycle | Entrance → 3-4 normal patterns (shuffle bag filtered by range, no immediate repeat) → guard I → guard II (back to back, as in m2) → chaos → groggy or fail → 4-5 normal patterns → next guard pair … | The cycle is not HP-gated (§0.3). A shorter opening (guard after 1-2 normals) matches the 100 %-HP observations |
| K4 | **Telegraph floor** | Every damaging hit gets ≥12 t (0.6 s) of clear telegraph, the house minimum adopted for Raiden. Needs lengthening: P1 hit 1 (glint 9 t → add a 12 t line decal), P1 hit 2 (3-4 t dive → line decal from the start of the reposition, ≥12 t), P2 (beam 8 t → glyph 25 t already serves, plus a 12 t line decal), fail decal 16 t → 20 t | Source-faithful leads: P3 ring 17-18 t, P5 ring 20 t, P6 19-20 t, P4 swings 20 t |
| K5 | Record rules | Count hits with `#elem` 1-4 (Pyro/Hydro/Electro/Cryo) on the body, **one count per element per 8 t**, independent of ICD; 3 for a new element, 9 to re-record; physical, Geo, Anemo and Dendro never count | elements_damage §5. No Hydro characters exist, so Hydro can be recorded only via items or reactions |
| K6 | **Star composition** | Slot A = guard I result, slot B = guard II result (integration §9.3); recorded → active star of that element; empty → inert star (slot A gold, slot B blue). A re-record (9 hits) fills slot B with the same element. A guard that completes no record leaves its slot empty (inert), even when guard I's element is still remembered | Matches every observation (Electro + re-record → 2 Electro; nothing → gold + blue). Alternative: any recorded element → both stars of that element |
| K7 | **+80 % RES target** | Inert stars only (C10). The boss keeps base RES during chaos | Changes integration D17 and elements_damage §6's chaos use; the generic `mres` hook is still needed for the stars |
| K8 | Star HP pools | Sized so a skill-light character breaks both stars in ≈10-12 s of the 17.5 s. Inert pools include the ×0.238 RES. Active stars: own element immune (C11); reaction hits count extra | Navia, Nefer and Ronova only ever make inert stars (elements_damage §14.5) |
| K9 | Hover hitbox | Keep the body hitbox on the floor below the hovering rig (integration risk note); the stars sit 3-4 b in front of and behind it | C21 |
| K10 | Chaos entry | Variant A (leap 10 t → flight ≈20-30 t → landing → **charge 20 t** → rise 5-10 t → timer + stars together) when the boss is ≥6 b from the centre; glide plus the same charge when nearer | The charge is a readable "chaos is coming" beat; m3 G's 6 t is too short to read |
| K11 | Cube streams | Ambient only (no damage), 2-4 visible | C8. If chaos feels empty, give the streams light, telegraphed damage as a deliberate deviation |
| K12 | Fail spears | Per surviving star: lock the player's position when the decal appears; decal ≥20 t; drop ≤1 t; damage cylinder r 2.5-3 b; dodge i-frames apply; one hit per spear; spears 31 t apart; tint = star colour; no groggy afterwards | m4 §5 |
| K13 | Groggy | 220 t total: pose A ≈116 t → pose B ≈34 t → get-up 12 t → stance, with no attacks until +220; `mres` irrelevant; no damage bonus | C12 |
| K14 | Pull | Undodgeable after a ≥12 t visible tell (aura 10 t + cage 18 t = 28 t already); requires line of sight and ≤ arena radius; teleport to 1 b in front of her facing her | integration D19 |
| K15 | Pull → swings | Relocation → wind-up 10-14 t; wind-up 5 t + hold 14 t → swing 1 (360°, r 5-6 b) → 14 t → swing 2 | C18 |
| K16 | Knockdown | P1 hit 2 and the P6 enchanted sweep use stronger knockback (`#cmKB` 4); others 2-3 | MC has no knockdown state |
| K17 | Damage coefficients (× base boss hit) | P1 1.0 / 1.15; P2 1.3; P3 1.6; P4 swings 1.2 each; P5 1.8; P6 gold 1.65, enchanted 2.5 (with the element attached); fail spear 2.2 each; entrance 1.0 | Only P1 and P6 are anchored to observations; the rest are proposals |
| K18 | Voice lines | Typed subtitle (caption or actionbar) with a soft sting; the 2 attack lines on P2/P4/P5 and fail spear 1 with a ≥20 s cooldown; no audio voice | §11 |
| K19 | Entrance | Plant from above with a short telegraph (≥12 t) despite the PDF's "no sign" (integration D12/D13); damaging; line at the plant | C20 |
| K20 | Death | Line → slump ≈20 t → fly-away take-off with a cube trail and a fade | C22 |
| K21 | Screen FX | Pull: `title` font-glyph flash (white → red) + vignette, or `darkness` for 10 t. Chaos sky: crimson `dust` columns and particle haze at the arena rim (MC cannot tint the sky per player) | — |
| K22 | Records across cycles | Reset both slots after each chaos (integration D24); the gems return to gold | No evidence either way |
| K23 | Javelin | Instant line hazard locked at the vertical beam (rel 25.7), 1 b wide at chest height (y +0.6…+1.8), ≥20 b or to the arena edge, resolved over 2 t; visual spear prop flies 5 b/t; return flight harmless | m1 B |
| K24 | Guard entry/ring | Non-damaging telegraph; voice line at the twirl; HUD record progress per integration D21 | §8 |
| K25 | P3 slam origin | Disc r 5 b centred 3.5 b in front of her; she closes to ≤3 b first | §5 |
| K26 | P5 flight | Take-off to +8 b (above the light layer at y 205 if needed; the light blocks have no collision); ring locked at take-off + 1 t; 20 t to impact; spikes visual only | §7 |

---------------------------------------------------------------------------------------------------

## 16. File index

- Frames and sheets: `understand/m1/` … `understand/m4/` (see each report's file index), `understand/model/` (poses and palettes).
- PDF pages 73-75 (patterns, chaos, voice table): `src/guide.pdf`, pages 2-4.
- This file: `understand/patterns.md`.
