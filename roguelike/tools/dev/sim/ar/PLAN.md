# 아를레키노 (Arlecchino, "The Knave") — chapter-4 boss: implementation plan (both phases)

Scratchpad `S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`, `AR` = `S:ar`, repo
`R:` = `/home/user/rlk/roguelike`, `F:` = `R:data/rlk/function`. 20 t = 1 s. Footage times are seconds into a clip
(`v1 2.45` = AR/src/v1.mp4 at 2.45 s, 60 fps; 1 tick = 3 frames). Every sheet cited is in `AR/ref/` (≤ 640 px jpg,
labelled `vN t`). Wiki = `AR/src/wiki/page.txt` (Namuwiki 「두 세계 불의 잔재」, read as data). `AR/src/v8.mp4` is
**ignored** (user: "마지막 6초짜리 영상은 무시해").

User request (KO, verbatim): "4챕터 보스 아를레키노를 만들거야. 영상이랑 나무위키 페이지 보낼게. 원거리 면역이랑 불 내성은
없애고 생명의 계약 해제 후 강공격은 일반공격으로 바꿔. 전투 진입 모션도 디테일하게 만들어야 해. 보스는 아를레키노 스킨 있는거
그대로 쓰고 2페이즈는 새로 보낼게." Phase-2 material has since arrived (v6, v7, `src/skin_33.png`): this plan covers
**both phases**.

---------------------------------------------------------------------------------------------------------------------

## 0. Decisions at a glance

| item | decision |
|---|---|
| registry | chapter boss `arlecchino` (n 12, `kind:"chapter"`, `fn:"boss/arlecchino"`, `ch [4]`, `route` true at I1), arena `fl_ruins` (n 4). Chapter 4's boss map becomes Arlecchino; chapter 2 and 5+ stay Raiden, 1 Azhdaha, 3 Apep |
| name / sub | P1 `「아를레키노」` / `우인단 집행관 서열 4위` (footage boss bar, `ref/hud_bars_banner.jpg`); P2 `두 세계 불의 잔재` / `페르엘`; colour `#E0303A` |
| user changes | **no ranged immunity** (원거리 면역 deleted, she never evades projectiles); **no Pyro resistance** (wiki 70 % → `res {"*":10}`, same 10 % as every other element); **선혈의 충격 is delivered by the next NORMAL attack** (the original needs a charged attack) |
| element | every hit Pyro (`#elem 1`, 1U, normal player-side reactions). Bond-of-Life hits use a crimson-black look, plain Pyro hits orange-gold (the footage's two colours) |
| phases | intro → **P1 「아를레키노」** (64 % of total HP; floor 70 % of the P1 pool → event E70 "재가 된 만상" + the ≤ 70 % kit; floor 1 → transition **T**) → **P2 「두 세계 불의 잔재」** (36 %, floor 0) → death. `phases [64, 36]` = the wiki's 1 780 814 : 1 001 708 |
| model | existing player avatar `arle` look **as-is** (skin `rlk:skin/arlecchino`, models `rlk:player_motion/arle/*`, scythe `rlk:player_motion/weapons/scythe`) at **× 1.4** (2.8 b, Tachy's accepted size); P2 = `src/skin_33.png` (confirmed P2 skin, §1.4) + twin scythes + six crimson blade-legs; P1 crimson wings only for wing attacks |
| Bond of Life | real player `bol` score (`player/bol/*`): BoL hits add 6 % max HP to the player's bond and heal her 1 % of the phase pool; a BoL hit on a still-bonded player deals 250 %; 1 % max HP every 50 t while bonded; healing clears it (existing `player/heal` → `bol/absorb`); heal orbs (existing 회복구슬) appear whenever she forces a bond |
| counter | clearing her bond arms **선혈의 충격**; the next normal-attack hit on her consumes it: during 붉은 피의 연회 = interrupt + 15 % (P1) / 12.5 % (P2) of the phase pool + 140 t stun; otherwise a crimson burst (2 % of the pool) |
| patterns | P1 8 entries (A 사형장으로의 초대, B 붉은 달의 낫, C 불꽃 도약, D 블러드 돌진; ≤ 70 %: E 와리가리 베기, F 붉은 피의 연회, G 죽음의 칼날, H 연옥 그림자 분신) + E70; P2 7 entries (Q0 낙하 공격, Q1 사형장으로의 초대, Q2 불꽃이 타오르는 낫, Q3 붉은 죽음의 무도회, Q4 떠오르는 재액의 달, Q5 붉은 피의 연회 (A 형벌의 핏값 / B 붉은 피의 사형), Q6 핏빛 연회) |
| floor decals | only F (red flood), G (cross strips ×2, rim tint), E70 (red pool, cosmetic), Q5A (ring / donut / ring outlines). In-air tells allowed where shown: Q4 aim line + reticle, Q5B vertical X, G/Q6 props |
| intro | 150 t, camera-free, boss invulnerable: tea → cup to embers, wisps flee → scythe forms from crimson flame → hold → 360° twirl → flip → stance (§3) |
| arena | `fl_ruins` "영락한 폐허": round Fontaine-ruins plaza r 26 (concentric carved rings), balustrade ring, ruins / trees / cliffs, block sky dome r 44; look `day` (P1) → `crimson` (P2: crimson sky dome + red moon). Dungeon entrance = gravestone with crimson flames (wiki) |
| HUD text | names, phase titles, pattern names, dialog subtitles from the wiki (Raiden precedent), the badge `◆선혈의 충격`, and the real game's banner adapted to our rule (§4.6, open question 1) |
| budget | ≤ 1.0 M atlas px (plan ≈ 0.78 M: rig 0.12 M, kit 0.62 M, gate icon 0.01 M; body / scythe reuse 0 px) → items atlas ≈ 12.94 M / 15.5 M; ≈ 4 000 datapack functions |

### 0.1 Open questions for the user (defaults chosen, the build proceeds with them)
1. **Banner text**: the real game shows 「생명의 계약을 제거하고 강공격으로 「붉은 피의 연회」를 중단시키세요」 during the
   Banquet (`ref/hud_bars_banner.jpg`). Default: show it as the real-game banner (Apep precedent: real-game texts allowed),
   adapted to `…일반 공격으로…`. Alternative (the 10-21 butterfly rule "no how-to text"): no banner.
2. **Heal source**: most of our characters cannot heal, so the counter would be impossible for them. Default: every
   forced bond drops **3 existing 회복구슬** (10 % each, 120° apart, 6–14 b from the centre; two are needed for the 18 %
   bond — the butterfly's "one pickup is too easy" feedback). Alternative: none (pure Genshin).
3. **Scale**: × 1.4 of the player avatar (2.8 b). Alternative × 1.25 (2.5 b, closer to the footage ratio).

---------------------------------------------------------------------------------------------------------------------

## 1. Footage study

### 1.1 What the clips are (chronological order: v5 → v1 → v2 → v3 → v4 → v6 → v7)
A Korean guide video (captions name each pattern, `ref/captions_guide.jpg`; overviews `ref/ov_v1..7.jpg`, 1 fps).

| clip | content |
|---|---|
| v5 | 0–12 title "아를레키노 패턴&생존공략" + cautions (높은 불 속성 저항 / 매우 높은 대미지 / 생명의 계약을 해제할 치유 수단 필수), 13–39 the player walks into the round ruins plaza (`ref/intro_v5_walkin.jpg`); she stands far at the centre with three small white flame-spirits (`ref/intro_v5_approach.jpg`); 39.0 domain shimmer, 39.25 boss bar → fight |
| v1 | 0–1 caption 「아버지표 생명의 계약」 (BoL rules, below); **0.0–5.2 the battle-entry motion** (§3); 1.5–12 원거리 면역 (removed); 14–25 낫 날리기; 26.5–40 도약 베기 |
| v2 | 0–11 돌진 베기; 12.5–27 평타; 28–37.7 패턴 추가 (the 70 % event); 37.5–40 와리가리 베기 |
| v3 | 0–7 와리가리 (cont.); 7.5–29 붉은 피의 연회 (P1, incl. a counter at 27.05); 29.5–40 칼날 소환 |
| v4 | 0–2.5 칼날 소환 (cont.); 3.5–12.5 분신 공격; 13–28 2페이즈 (new sky; the cutscene itself is cut; 19.5 낙하 공격); 28.5–36.5 쌍낫 평타; 37–40 쌍낫 날리기 |
| v6 | 0–4 쌍낫 날리기 (cont.); 5–14 뒤 견제; 15.5–26 아를-빔; 26–40 붉은 피의 연회 (P2) |
| v7 | 0–27 붉은 피의 연회 (P2: 형벌의 핏값 4–12.3, 붉은 피의 사형 16–20, counter 24.15); 28.5–40 핏빛 연회 |

Guide name ↔ wiki name: 낫 날리기 = 붉은 달의 낫, 도약 베기 = 불꽃 도약, 돌진 베기 = 블러드 돌진, 평타 = 사형장으로의
초대, 패턴 추가 = 재가 된 만상 (+ 생명의 계약 강제 부여), 칼날 소환 = 죽음의 칼날, 분신 공격 = 연옥 그림자 분신, 2페이즈 =
낙하 공격, 쌍낫 평타 = 사형장으로의 초대 (P2), 쌍낫 날리기 = 불꽃이 타오르는 낫, 뒤 견제 = 붉은 죽음의 무도회, 아를-빔 =
떠오르는 재액의 달. We use the **wiki names** in game (pattern name on the boss bar).

### 1.2 Bond-of-Life rules as the game states them (caption v1 0.0–0.8, wiki §3.1 / §3.2)
1. Hit by one of her "HP-consuming" attacks (wiki: "생명의 계약 피해") → the character gets 생명의 계약, she **recovers HP**.
2. Hit by such an attack while already bonded → **250 %** damage.
3. While bonded: every 2.5 s, 0.125 % max HP + 200 damage.
4. Clearing the bond (healing; wiki note 10: the charged attack alone is NOT the clear condition) grants **선혈의 충격**:
   the next charged attack is enhanced; the enhanced charged attack **interrupts 붉은 피의 연회** → she takes ≈ 15 %
   (P1) / 12.5 % (P2) of max HP and is groggy for 7 s.
5. 붉은 피의 연회 starts by **forcing** a bond on the player (red sigil closes on the player, flash, red X brand,
   `ref/p1_F_sigil.jpg`).

**The user's change "생명의 계약 해제 후 강공격은 일반공격으로 바꿔"** is about rule 4: it is the *player's* strong
(charged) attack that carries 선혈의 충격 — not a move of hers. Our game has no charged attack, so the shock is delivered
by the player's **next normal attack** (기본 공격: melee swings, bow / catalyst normal shots, Nefer's phantasm hits) that
lands on her (§4.3).

### 1.3 Boss vs player effects (implementers: do not copy the player's)
| seen | whose |
|---|---|
| orange-gold flame arcs, flaming scythe wheel, fire trail on the ground, spin rings | **boss** (plain Pyro) |
| crimson-black thorns, threads from the sky, giant red blades, clones, wings, red X, red moon, orbs, beam | **boss** (BoL attacks) |
| blue water rings, white-blue bubbles, golden shields, Neuvillette's yellow beam, Furina's spirits, damage numbers | player party (Furina, Kokomi, Sigewinne, Neuvillette…) |
| the white shimmer at v5 39.0, the yellow caption boxes, the blue icons | domain / guide UI |

### 1.4 Model (`ref/model_p1.jpg`, `ref/model_p2.jpg`, `ref/model_p2_closeup.jpg`, `ref/skins_p1_p2.jpg`)
- **P1** (v1 0.4–4.6, v2 4.5, v2 16.3): tall slim woman, white hair with black streaks, black / grey / white suit with red
  accents, long legs, heels; one huge crimson scythe 「붉은 달의 형상」 (haft ≈ her height, crescent blade). Wings appear
  only in wing attacks (v1 36.6–39.6, v2 36.25, v4 9.5). Our existing `rlk:skin/arlecchino` (white coat, black, red,
  white hair, red eyes) is the user-mandated look — used unchanged.
- **P2** (v4 21–23, v6 6.6–7.4, v7 1.4): white hair with a black streak, black-red bodysuit / dress, bare pale shoulders,
  red accents, dark legs with red; six crimson blade-legs / wings from the back (wiki: "등 뒤에서 솟아난 6개의 다리",
  "검붉은 날개"); twin crimson scythes.
- **`src/skin_33.png` = the P2 skin** (conclusion): white hair with a black streak, red eyes, bare pale shoulders and
  arms, black bodice with a red X lacing, black skirt / legs with red streaks, a red X ornament at the back of the head —
  exactly the P2 figure; it shares nothing with the P1 coat skin (`ref/skins_p1_p2.jpg`: left pair = existing P1 skin
  front / back (slim arms), right pair = skin_33 (classic 4-px arms)).
- Height ratio in the footage ≈ 1.15 × the player; we use × 1.4 for readability (§0.1 Q3).

### 1.5 Floor markings actually shown (the only allowed floor decals)
F 붉은 피의 연회 P1: the whole floor floods red before hit 1 (`ref/p1_F_field.jpg` 15.15–17.4) and red cracks linger
after hit 2 (20.4–21.4). G 죽음의 칼날: red translucent strips joining the planted blades (`ref/p1_G_cross.jpg` 34.8–36.0,
then the rotated cross), and the floor reddening inside a ring of erupting blades before the final field
(`ref/p1_G_rim.jpg` 38.8–39.8). E70: the red pool spreading from her (`ref/p1_E70_event.jpg` 33–35.75, no damage). Q5A
형벌의 핏값: red ring outlines (disc, then donut, then a wider disc) before each burst (`ref/p2_Q5_banquet_b.jpg` 4.2–12.3).
Nothing else has a floor marking: throws, leaps, dashes, normal strings, the grab, clones, the P2 fall, beams (aim line
in the air), the X execution (vertical X in the air), the feast (orbs are objects). Tells for those are pose, flame
colour, props, sounds.

---------------------------------------------------------------------------------------------------------------------

## 2. Model: display-entity rig (S2)

### 2.1 Reuse of the existing look
- Body parts = the **existing item models of the player avatar** `rlk:player_motion/arle/{head,body,right_arm,
  right_forearm,left_arm,left_forearm,right_leg,right_shin,left_leg,left_shin}` (written by `tools/build_player_rig.mjs`
  from `rlk:skin/arlecchino`; base box + overlay box per part). The boss rig does **not** copy, repaint or re-model them:
  its item displays name those item ids (0 new px; a later change of the avatar skin changes the boss too, as wanted).
- Weapon = the existing `rlk:player_motion/weapons/scythe` (the glowing 붉은 달의 형상, frame: grip [8,8,8], shaft +Y,
  hook −X, cutting edge = lower / inner outline; brightness 15). P2 holds two (right and left), the left mirrored by a
  180° roll so both edges lead in their swings.
- Kinematics: copy the avatar's `transform()` math (hip 0.75, torso 0.75, shoulder offsets ±0.34375 / 0.625, elbow
  −0.25, knee −0.375, hand −0.34375; item_display Y180 fix) into `tools/arlecchino_pose.mjs` and scale every
  translation and part scale by `SIZE = 1.4` (head top 2.8 b). `build_player_rig.mjs` is not imported (it is a script
  with side effects) and not edited. The avatar's authored clips `tools/player_motion/arle.json` (infused_1..6, skill,
  burst) may be **read** as pose sources for the boss's swings (read-only; their timing is re-authored for the boss).
- **P2 body**: `src/skin_33.png` embedded as a base64 constant in `tools/arlecchino_skin_p2.mjs` (2.6 KB; no binary in
  git, the build is self-contained) → RP `textures/mboss/arlecchino/skin_p2.png` (64×64 = 4 096 px) + 10 part models
  `rlk:mboss/arlecchino/p2/<part>` built with the avatar's `skinFaces` UV layout (copied) and overlay inflation —
  **but skin_33 is a classic 4-px-arm skin** (its arm columns 47 / 54–55 are filled; the avatar skin is slim, 3 px):
  P2 arm boxes are 4 px wide with the classic UVs (right arm `[40,16,4,12,4]` / overlay `[40,32,…]`, left arm
  `[32,48,4,12,4]` / overlay `[48,48,…]`) and the shoulder offset becomes ±0.375 (× SIZE) in form p2 (`pose.armW` per
  form); legs / body / head are identical in both layouts. `ref/skins_p1_p2.jpg` renders P1 slim, P2 classic.

### 2.2 Parts (item displays; UUID `524c4b4d-4b4e-4100-8000-0000000000NN`; tags `rlk_room rlk_mb_aux rlk_mb_part rlk_kn_part rlk_kn_<part>`)
| # | part | parent / attach | model (P1 / P2) | notes |
|---|---|---|---|---|
| 00–09 | head, body, right_arm, right_forearm, left_arm, left_forearm, right_leg, right_shin, left_leg, left_shin | avatar kinematics | `rlk:player_motion/arle/<part>` / `rlk:mboss/arlecchino/p2/<part>` | form swap = item swap (snap) |
| 10 | scythe_r | right hand | `rlk:player_motion/weapons/scythe` | brightness 15; `world` attach for throws (hidden while the wheel flies) |
| 11 | scythe_l | left hand | same, roll 180 | scale 0 in P1 |
| 12–23 | leg_1a/1b … leg_6a/6b | spine point (3 per side, 2 segments) | `rlk:mboss/arlecchino/wing_{a,b}` (P1 feathered crimson wing look) / `leg_{a,b}` (P2 blade-leg look) | P1: scale 0 except `wings` look; P2 always shown |
| 24 | cup | right hand | `rlk:mboss/arlecchino/cup` | intro only (white porcelain, gold rim) |
| 25 | saucer | left hand | `rlk:mboss/arlecchino/saucer` | intro only |
| 40 | shadow | root | standard shadow | radius 1.0 |
Culling box 8 × 10, view range 2, billboard fixed. Secondary motion: legs lag 2 t, a slow sine sway (P2 idle).
Sprites: wing / leg segment cards (2 × 64×256), cup + saucer (2 × 16×16), P2 skin 64×64 → **≤ 0.12 M px** (gate 0.15 M).

### 2.3 Looks (rig calls `look/<channel>/<v>`)
`form` p1 | p2 (item swap of 00–09, legs, scythe_l) · `wings` off | open (P1 wing attacks, E70) · `weapon` hand | gone
(thrown, hidden in place) | world · `glow` normal | crimson (brightness ramp on the scythe edge during BoL tells) ·
`props` none | tea (cup + saucer) · `state` normal | hidden · `flash` (hit feedback 3 t).

### 2.4 Clips (contract; names / lengths / events frozen at D0; ticks = played clip ticks)
| clip | len | events |
|---|---|---|
| `idle` / `idle2` (P2) | 40 loop | — |
| `walk` / `walk2`, `strafe_l` / `strafe_r` (+2) | 24 / 20 loop | step 0, 12 |
| `backstep` | 12 | land 10 |
| `flinch` | 6 | — |
| `stun` / `stun2` | 140 (loop 20–120) | kneel 10, rise 120 |
| `intro` | 150 | §3.1 |
| `a2` | 46 | raise 0, h1 14, h2 24, end 46 |
| `a4` / `a5` | 100 / 124 | h1 14, h2 24, h3 44, h4 64, end 100 / as a4 + h5 84, end 124 |
| `b1` | 60 | raise 0, spin 10, release 28, catch 52, end 60 |
| `b2` | 130 | spin 10, rel1 28, spin2 40, rel2 58, reach 76, lock 80, grab 96, end 130 |
| `c1` | 80 | crouch 0, jump 8, apex 18, lock 44, dive 48, impact 54, end 80 |
| `c2` | 140 | as c1 + wing_open 84, wing 90, end 140 |
| `d1` | 56 | flare 0, go 26, hit 30, end 56 |
| `d2` | 76 | as d1 + fhit 46, end 76 |
| `e1` | 112 | rise 0, zig1 16, zig2 26, zig3 36, zig4 46, zig5 56, lock 64, go 70, sweep 76, spin 92, end 112 |
| `f1` | 232 | raise 0, brand 22, centre 40, arms 100, flood 110, hit1 160, wings 166, hit2 196, end 232 |
| `g1` | 140 | plant 0, blades 6, cross1 34, relock 40, cross2 62, rim 70, field 104, end 140 |
| `h1` | 156 | leap 0, perch 10, clones 20, strike 34, drop 96, wing 104, sweep 112, end 156 |
| `e70` | 110 | glow 0, rise 20, pool 40, brand 70, wings 74, land 96, end 110 |
| `brk` | 20 | hit 0 (the counter's stagger; then `stun`) |
| `t_p2` | 180 | §3.2 |
| `q0_hover` / `q0_dive` | 40 loop / 40 | — / go 0, impact 20, blades 28, end 40 |
| `q1` | 124 | h1 14, h2 30, h3 46, h4 66, h5 82, h6 100, end 124 |
| `q2` | 70 | windup 0, release 20, go 34, slash 42, end 70 |
| `q3` | 36 | whip 0, spin 14, end 36 |
| `q4_up` / `q4_shot` / `q4_land` | 20 / 50 / 16 | top 20 / aim 0, lock 20, fire 26, end 50 / land 12 |
| `q5a` | 180 | raise 0, brand 22, ring1 60, hit1 95, donut 100, hit2 121, ring3 130, hit3 158, end 180 |
| `q5b` | 136 | raise 0, brand 22, x 26, mark 50, s1 56 (then every 3 t to s9 80), final 96, end 136 |
| `q6` | 200 | fly 0, gone 20, moon 30, v1 50, v2 60, v3 70, v4 80, v5 90, v6 100, orbs 110, toss 125, lock 140, dive 160, impact 168, end 200 |
| `death` | 110 | §3.3 |
Big swings (spin rings, twirl, slams, wing sweeps) are keyed **every tick** over the swing (≤ 120°/t, the RIGLIB check);
held weapons are checked from the side in the renders (edge leading, hook pointing the right way in stances).

### 2.5 Reference renders S2 must deliver
`AR/renders/s2_U1.jpg`: front / side / back / ¾ of P1 (wings off and open) and P2, next to a 1.8 b avatar stand-in;
clip strips every 2 t for every clip; the intro strip next to `ref/intro_v1_summon.jpg`, `intro_v1_twirl.jpg`,
`intro_v1_stance.jpg`; one pair per pattern clip with its `ref/p*_*.jpg` sheet. Renderer: `S:az/understand/
rigtech_render.py` (wrapper style `S:ap/rigwork/r1/r.sh`).

---------------------------------------------------------------------------------------------------------------------

## 3. Battle-entry motion, transition, death (S2: clips + `seq.py`)

### 3.1 Intro (boss only; `seq/intro`, clip `intro`, registry `intro:160`)
Policy as every boss: no camera, no player lock, `rlk_mb_inv` until 150, title at 80, push ring (no damage) at 140,
music phase 1 at 136. The player arrives at `start` (south edge, 22.5 b from the centre, facing north); she stands at the
centre facing south. Frame references: `ref/intro_v1_tea.jpg` (v1 0.0–1.2), `intro_v1_summon.jpg` (0.6–1.8 every
0.05 s), `intro_v1_fine.jpg` (1.1–3.1), `intro_v1_twirl.jpg` (2.35–3.85 every 0.05 s), `intro_v1_stance.jpg` (3.6–5.0),
`intro_v1_overview.jpg`, `intro_v5_approach.jpg` (the spirits). Footage durations are kept for the fast beats (twirl,
flip) and stretched ×1.5–2 for the quiet ones (Minecraft reads slower). Sounds are vanilla only, `mboss_lib.sound`
min-volume rule; "kit" = S1K preset.

| beat | source | ticks | pose / motion | effects (kit) | sounds |
|---|---|---|---|---|---|
| E0 tea | v5 33–39.5, v1 0.0–0.6; wiki "홍차를 마시며 기다리고 있다" | 0–30 | standing tall, weight on the left leg; left hand holds the saucer at the sternum, right hand lifts the cup to the lips (8–14), sips (14–22), lowers it to the saucer (22–30); head slightly tilted down | `props tea`; 3 white flame-wisps (kit prop `wisp`, white) circle her at r 1.3 b, 0.3–0.9 b high, bobbing | `entity.generic.drink` 0.35 pitch 1.3 at 16; `block.amethyst_block.chime` 0.3 at 4, 20 (wisps) |
| E1 cup to embers | v1 0.6–1.15 | 30–44 | both hands drop to the hips; head lifts to the player | cup + saucer burst into red-orange embers (`embers_puff`), `props none` at 34; wisps flee to three rim posts (bearings 150°, 210°, 0°; r 28) over 20 t and idle there for the whole fight (wiki) | `block.fire.extinguish` 0.4 pitch 1.6 at 34; `entity.allay.item_thrown` 0.4 at 35 |
| E2 reach | v1 1.2–1.3 | 44–52 | right arm swings out sideways to shoulder height, palm down, fingers spread | crimson embers stream into the right palm | `block.respawn_anchor.charge` 0.5 pitch 1.4 at 44 |
| E3 summon | v1 1.35–1.5 | 52–60 | slight crouch, torso turns 20° right | crimson flame vortex at the hand and her left side (`scythe_form`) | `item.firecharge.use` 0.6 pitch 0.7 at 52; `block.fire.ambient` 0.6 |
| E4 form | v1 1.5–1.75 | 60–72 | the haft grows out of the palm both ways (scythe_r scale 0.2 → 1 along +Y, `weapon hand`), the crescent ignites last at 70 | flame tongue along the haft, crescent flash | `entity.blaze.shoot` 0.6 pitch 0.8 at 62; `item.trident.return` 0.6 at 70 |
| E5 hold | v1 1.77–2.4 | 72–92 | holds the scythe horizontal at chest height, haft across the body, crescent at her left hanging down, edge forward; looks at the player | ember drift; **title + sub at 80** (boss bar `「아를레키노」` / `우인단 집행관 서열 4위`), dialog 「두려운가? 아니면 두려워할 용기조차 없는 건가?」 at 80 | `entity.wither.ambient` 0.25 pitch 1.8 at 80 |
| E6 twirl | v1 2.45–2.95 | 92–104 | one-handed **360° twirl in the frontal plane**: blade right-low (92) → overhead (95) → left-high (97) → sweeping low in front (99–101) → right, haft horizontal (104); keyed every tick | crimson crescent trail closing into a full ring (`twirl_ring`), a flame ring on the floor r 2.5 at 98 | `entity.player.attack.sweep` 0.6 pitch 0.6 at 94 and 100; `item.trident.riptide_1` 0.5 pitch 1.3 at 96 |
| E7 hold 2 | v1 3.0–3.3 | 104–110 | haft horizontal pointing to her right, crescent upright at her left | — | — |
| E8 flip | v1 3.35–3.55 | 110–116 | rolls the scythe through the hand: crescent swings from her left over to her right (≤ 90°/t) | short flame arc | `item.armor.equip_netherite` 0.6 at 112 |
| E9 stance | v1 3.6–5.0 | 116–150 | lowers into the stance: crescent low by her right foot (tip 0.1 b above the floor, never below), haft rising diagonally across the body to the left shoulder, right hand at the hip, left hand open; idle breathing from 130 | embers fall off the blade; push ring r 4 (no damage) at 140 | `block.respawn_anchor.set_spawn` 0.5 pitch 0.7 at 120; `entity.warden.heartbeat` 0.6 at 126; music phase 1 at 136 |
Reload during the intro → jump to the end of E9 (standing, scythe drawn, wisps at their posts). Test 25 replays it.

### 3.2 Transition T (P1 floor → P2; `seq/t_p2`, clip `t_p2`, 180 t; designed — the footage cuts the cutscene)
Sources: wiki (animated cutscene 「두 세계 불의 잔재」, red moon / 붉은 달, six legs, burnt crimson wings, twin scythes,
spirits turning red, BGM 2 「종말의 자비송」, line 「보아라, 모든 선의를 불태울 칼날을!」), the P2 opener (v4 13.5–21.4,
`ref/p2_T_transition.jpg`, `p2_Q0_fall.jpg`). Body `rlk_mb_inv`, `cine/start` (player damage refused) 0–180; hazards of
P1 cancelled at 0.

| ticks | motion | effects / arena | sounds |
|---|---|---|---|
| 0–24 | staggers back (`brk` pose), drops to one knee, scythe planted | ember burst, `glow crimson` | `entity.wither.hurt` 0.4 pitch 1.6 |
| 24–50 | head bowed; the planted scythe bleeds crimson flame up her body | flame column builds (`pillar` r 1.2, rising) | `block.fire.ambient` loop, `block.beacon.deactivate` 0.6 |
| 50–70 | **blackout**: 20 t blindness on the player (as Tachy's T2) while the arena look job `crimson` runs (dome, moon, backdrop) | wisps 2 of 3 turn red (wiki) | `entity.warden.sonic_charge` 0.4 |
| 70–110 | she rises 3 b inside the crimson pillar; at 90 the form swaps p1 → p2 (hidden by the pillar's peak) | red moon halo card on (`moon_halo`) | `entity.blaze.ambient` 0.6 pitch 0.5 at 90 |
| 110–130 | the six blade-legs unfold one pair at a time (110, 116, 122) | crimson feather / ash burst per pair | `item.elytra.flying` short 0.5; `entity.phantom.flap` 0.5 ×3 |
| 130–150 | twin scythes form in both hands (as E4, mirrored) | flame tongues | `item.trident.return` 0.6 ×2 |
| 140 | **title** `두 세계 불의 잔재` / `페르엘`, music phase 2, dialog 「보아라, 모든 선의를 불태울 칼날을!」 | `mboss/title`, `repool 36` | `entity.ender_dragon.growl` 0.4 pitch 1.2 |
| 150–180 | she launches up and away to the hover spot (north, 14 b from the player, 10 b up, `mv/ok`) → `q0_hover`; Q0 follows (§6) | streak | `entity.phantom.swoop` 0.6 |

### 3.3 Death (`seq/death`, 110 t; wiki: "별도의 사망대사 없이 자신의 낫을 집어넣는 모션과 함께 불꽃으로 사라진다")
0 stop (flinch), 10 lowers both scythes, 30 the scythes dissolve into embers (put away), 50 straightens and turns to the
player, 70 crimson flames climb her body, 96 she vanishes in a flame burst (parts scale to 0 in place, never below the
floor), the legs shed ash; wisps fade back to white at 100. No dialog. Then `cb/won`.

---------------------------------------------------------------------------------------------------------------------

## 4. Bond of Life, 선혈의 충격 and the user's changes (S3 owns `bond.py`; framework FN-1 by S1)

### 4.1 Player bond (existing system, no shared-file edits)
- The player's `bol` score (HP units; HUD 「생명의 계약 N%」 already in the action bar) is the bond. Add with
  `#bolPct tmp` + `function rlk:player/bol/add_pct` as the player; healing clears it through the existing
  `player/heal → player/bol/absorb` (every heal: items, characters, 회복구슬).
- **BoL hit** (a hazard / projectile created with the FN-1 option `bol`): after a landed hit the framework raises
  `#mbHitBol mb` = the option value; the module (same tick) adds that % of max HP to the bond (`BOL_HIT 6`), sets
  `#bonded kn 1`, and heals her `BOL_HEAL_PM 10` ‰ of the phase pool (`mhpC += …`, capped at `mhpM`).
- **Re-hit 250 %** (S5: **150 %**, and per-mille hits are not multiplied): the module keeps `#mbBolRe mb` = 250 while `#bonded kn 1` and the player's `bol ≥ 1`, else 100;
  FN-1 multiplies a BoL hazard's raw damage by it (before defence). Dash-dodged hits never bond.
- **Bond DoT**: while `#bonded kn 1` and `bol ≥ 1`: every 50 t `mboss/pl_dot` `BOL_DOT_PM 10` ‰, Pyro, non-lethal
  (Genshin 0.125 % + 200 ≈ 1 % at L90). The DoT only follows a bond **she** gave (a Clorinde / Arlecchino player's own
  bond does not tick until she bonds them).
- **Forced bond** (`bond/force`): `bol += 18 %` max HP (S5: her earlier bond is taken back first, so her part becomes exactly
  18 % and two orbs always clear it; the player's own bond stays), `#bonded 1`, `#given += …`, no damage, no dodge; brand ring + X + red screen
  flash (kit); 3 heal orbs (§4.4). Skipped while the player is dead, in the selection space, in the map screen or
  respawning (as the butterfly's cocoon).
- Cleared: `bol` reaches 0 (any way) while `#bonded 1` → `#bonded 0`, `#given 0`, **선혈의 충격 armed** (`#shock kn 1`),
  kit `shock_gain` at the player, badge on. `#given kn` sums the bond she added since the last clear; at cleanup / won /
  cancel / defeat the module removes `min(bol, #given)` from the player (no shock, no hooks beyond `player/bol/on_change`),
  so a Clorinde / Arlecchino player keeps the bond of her own kit.

### 4.2 Removed mechanics
- **원거리 면역**: not implemented in any form (no evasion, no projectile filter, no invulnerability window tied to
  projectiles). Her only invulnerable windows: intro, E70 (until its brand tick), T, death.
- **불 내성 70 %**: `res {"*":10}` (Pyro 10 % like the rest). `res_pre` handles it; nothing special in the module.

### 4.3 선혈의 충격 via a normal attack (the user's change)
- Predicate "normal-attack hit" (read in the module's `on_hit`, which `combat/apply` calls before `apply_mods`):
  `#icd tmp 1` and `#skillDmg tmp 0` and `#tfm tmp 0` and `#sub itv 0` and `#trueDmg tmp 0` (= Raiden's
  `boss/raiden/sg/guard_hit` rule + no item proc). S3 verifies it per character (lumine, yoimiya bow normal and aimed
  shots, skirk, clorinde sword + pistol normal shots, arlecchino, navia, ronova, nefer) and lists exceptions.
- On such a hit with `#shock 1`: `on_hit` only records `#shk_hit kn 1` (no recursion into `combat/apply`); the module's
  next `tick` resolves it:
  - inside a **break window** (F 22–159, Q5A 22–121, Q5B 22–96): cancel the pattern (hazards, decals, props, banner),
    **true damage** P1 15 % / P2 12.5 % of the phase pool (`#mbTrue` = `mhpM × 150 / 1000` or `× 125 / 1000`, clamped so
    `mhpC` stays ≥ the current floor + 1: true damage ignores floors), clip `brk` → `stun` **140 t** (no damage-taken
    multiplier, AI paused), kit `break_burst`, dialog none, Banquet cooldown restarts from the stun's end.
  - outside: kit `shock_hit` crimson burst + true damage 2 % of the pool (same clamp).
  - either way `#shock 0`, badge off. The shock persists until used (or the fight ends); one shock at a time.

### 4.4 Heal orbs (existing 회복구슬)
At every forced bond (E70, F, Q5): 3 orbs via `function rlk:combat/heal_orb_spawn` (as any executor, positioned) at
6–14 b from the arena centre, 120° apart, random start bearing (independent of decals: every floor-wide hit is
dash-dodgeable). 10 % max HP each (`#orbHealPct`): the 18 % bond needs **two**. Existing
`healorb_tick` / pickup / sound; the arena `sweep` removes leftovers; at most 3 alive (older ones removed first).

### 4.5 Numbers (api, S5 tunes)
`BOL_HIT 6` % · `BOL_FORCE 18` % · `BOL_REHIT_PCT 250` (S5: 150) · `BOL_DOT_PM 10` / `BOL_DOT_T 50` · `BOL_HEAL_PM 10` ·
`BREAK_PM {p1:150, p2:125}` · `STUN_T 140` · `SHOCK_BONUS_PCT 2` · `ORBS 3`, `ORB_R (6, 14)`.

### 4.6 HUD
Player action bar: the existing 「생명의 계약 N%」. Boss bar: name / sub per phase; third line = pattern name and, while
armed, `◆선혈의 충격` (crimson, kit glyph). During a break window: the adapted real-game banner (§0.1 Q1) as its own
boss-bar line under the bars (kit `hud/banner` = bossbar `rlk:kn_banner`, as the footage puts it right under the HP bar;
the subtitle line is the dialog's; removed at the window's end; I1, S1K K1). Dialog subtitles per pattern
(Raiden's letter-reveal style, kit `hud/line {id}`), lines from the wiki (§5–6). No other text.

---------------------------------------------------------------------------------------------------------------------

## 5. Phase 1 patterns (S3 `p1.py`)

### 5.1 Common rules
- Damage = `mboss/hurt` coefficient % × atk 12 × dmgMul 150 (1.00 = 18 raw). Tiers **T1 32, T2 45, T3 62, T4 80**; P2 × 1.2
  (`P2_MUL 120`). BoL hits as §4. Every hit Pyro 1U.
- Tells: first visible motion → hit ≥ 12 t, big (area ≥ 100 b², r ≥ 8, full arena, or not dash-dodgeable) ≥ 20 t, combo
  follow-ups ≥ 10 t apart; aim locks at the tell's last 6–8 t. Quiet hazards (`#hzQuiet 1`) except the decals of §1.5.
- Movement safety: every end point (landing, dash end, perch, zig-zag points) through `mv/ok` inside `walk − 1.5`; the
  floor inside walk is flat full blocks and nothing hangs below y 226 (the dome is higher), so leaps never enter blocks;
  parts never below the floor.
- Recovery after each pattern: 16–24 t idle with the scythe low (P2 12–18 t) — the punish window.
- Dialog: one line at each cast (random among the pattern's lines).

### 5.2 Entries (`sector(r, half°)`, `disc(r)`, `ring(r0,r)`, `line(len,w)`, `full()` = framework `mboss/hz/*`; `pj` = `mboss/pj/launch`)
**A 사형장으로의 초대 — normal string** (`ref/p1_A_normal_2hit.jpg` v2 13–16.6, `p1_A_normal_5hit.jpg` v2 19–24.5;
dialog 「뭘 망설이는 거지?」)
- Near (≤ 4.5 b; from 4.5–7 b she walks in 0.2 b/t during the raise). > 70 %: `a2` — h1 14 horizontal sweep right→left
  `sector(4.2,75)` T2, h2 24 backhand `sector(4.2,75)` T2. ≤ 70 %: `a4` / `a5` (4–5 hits, 50 / 50) — h1 14 T1, h2
  24 T1 (as above), h3 44 **spin ring** `disc(4.6)` T2, h4 64 **overhead slam** `sector(3.6,40)` + `disc(2.2)` 2.6 b ahead
  T3 (burst), h5 84 spin ring `disc(4.8)` T2. Plain Pyro (orange arcs).

**B 붉은 달의 낫 — scythe throw** (`p1_B_throw.jpg` v1 15.4–18.1, `p1_B_throw_overview.jpg`, `p1_B_throw2_grab.jpg`
v1 19.5–24.6)
- `b1`: raise 0, the scythe spins into a vertical flaming wheel in front of her (10–28), release 28: **wheel `pj`**
  (hr 1.1, covers 0–2.4 b high, 1.4 b/t, out 16 b along the locked line, then returns to her hand at 1.4 b/t; out and back
  are separate groups) T2, fire trail on the ground behind it (cosmetic, after it passes); catch 52.
- ≤ 70 %: `b2` — two wheels (rel1 28 at the locked point, rel2 58 at `mv/lockv` lead 6), then **the grab**: reach 76
  (arm out, crimson glow on the palm), lock 80 (the player's spot), hit 96: crimson claw closes there `disc(2.2)` T2
  **BoL** (claw card appears at 92, no floor decal; tell 20 t from the reach).

**C 불꽃 도약 — leap slash** (`p1_C_leap.jpg` v1 26.5–29.0 and 32.0–35.0, `p1_C_wing.jpg` v1 35.4–39.9; dialog
「피어오르는 불꽃으로.」)
- `c1`: crouch 0, jump 8 (+9 b in 10 t, flaming crescent at the take-off), apex 18–44 (spins with flame, drifts toward
  the player ≤ 0.35 b/t), lock 44, dive 48–54 to the locked spot (`mv/ok`), impact 54: `disc(3.6)` + `line(6,2.0)` along
  her facing T3 (one group). Tell 46 t from the jump.
- ≤ 70 %: `c2` adds the wing strike: wing_open 84 (crimson wings burst open, `wings open`), wing 90 `sector(5.6,70)` T2
  **BoL**; wings held to 130.

**D 블러드 돌진 — dash slash** (`p1_D_dash.jpg` v2 0–11.5, `p1_D_follow.jpg` v2 7.4–11.4; dialog 「도망칠 수 없다.」)
- `d1`: flare 0 (red flare on her body, scythe drawn back low, v2 7.8), go 26 (6 t dash along the locked line to the
  player's spot + 1.5 b, ≤ 14 b, `mv/ok`), hit 30: `line(dash,2.0)` + end `sector(4.2,70)` T2 (one group). Tell 30 t.
- ≤ 70 %: `d2` follow-up fhit 46 (if the dash landed or the player is ≤ 5 b): burst `disc(3.2)` + rising slash
  `sector(4.0,60)` T2 (one group; v2 9.9–10.2).

**E 와리가리 베기 — aerial zig-zag** (≤ 70 %; `p1_E_zigzag_a.jpg` v2 37.5–40, `p1_E_zigzag_far.jpg`,
`p1_E_zigzag_b.jpg` v3 0–7.25)
- `e1`: rise 0 (hops back to 10–12 b from the player, hovers 2.5 b up), five lateral dashes of 4 b (alternating, red
  streaks) at 16, 26, 36, 46, 56, lock 64, go 70 (6 t dive to the player), sweep 76 `sector(5.2,90)` T2, spin 92 vertical
  wheel slash `disc(4.2)` T2. Plain Pyro. Hittable throughout (no ranged immunity).

**F 붉은 피의 연회 — Banquet of Crimson Blood (P1)** (≤ 70 %, scheduled; `p1_F_banquet.jpg` v3 7.5–29.5,
`p1_F_sigil.jpg`, `p1_F_field.jpg`, `p1_F_counter.jpg`; dialog 「어둠이 내려앉는 순간 멸망이 도래한다.」 /
「카운트 다운이 시작됐군.」 / 「네가 몸을 기댈 거미줄이 있을까.」)
- `f1`: raise 0 (scythe up, the crimson sigil ring contracts onto the player 6–22), **brand 22 = forced bond** (§4.1) +
  3 heal orbs + banner; **break window 22–159**; centre 40 (she glides to the arena centre, arms out); flood 110: the
  red flood decal spreads from her over the whole floor (48 t); **hit1 160** = crimson threads + thorns everywhere
  `full()` T3 **BoL**, dash-dodgeable; wings 166 (she rises 1 b, wings open); **hit2 196** = blast `full()` T3 **BoL**,
  dash-dodgeable (the flood flashes 6 t before each hit); cracks decal 196–232 (cosmetic).
- Counter (§4.3) inside the window: break + stun. Footage: the bond at v3 10.25 → hit1 17.9 (7.6 s) and a counter
  49 t after the bond (v3 24.6 → 27.05).

**G 죽음의 칼날 — Blades of Death** (≤ 70 %; `p1_G_blades.jpg` v3 29.5–40, `p1_G_cross.jpg` 34.2–38.2,
`p1_G_rim.jpg` 38–40, `p1_G_field.jpg` v4 0–3.4; dialog 「도망치기 바쁜 꼴이 가엾게 떠는 짐승 같구나.」)
- `g1`: plant 0 (scythe planted), blades 6: four giant crimson blades rise at the ends of a **plus cross centred on the
  player's locked spot** (arms 14 b, kit prop `blade`), strip decals 6–34; cross1 34: two `line(28,3.0)` T2 **BoL** (one
  group); relock 40 on the player, **X cross** (rotated 45°), strips 40–62, cross2 62 T2 **BoL**; rim 70: blades erupt
  around the rim (12 props at r 24) and the floor tint decal grows (34 t); field 104: `full()` T2 **BoL**, dash-dodgeable.

**H 연옥 그림자 분신 — Purgatory shadow clones** (≤ 70 %; `p1_H_clones.jpg` v4 0–13, `p1_H_launch.jpg` 4.3–6.7,
`p1_H_leapback.jpg` 8.8–10.9; dialog 「연옥의 그림자를 보아라.」)
- `h1`: leap 0 up a crimson thread to a web strung 7 b above a point 6 b behind her (kit props `threads`, `web`), perch
  10; clones 20: two crimson shadow clones (kit prop `clone`, scythe silhouettes) dive from the web left and right in
  arcs (14 t, visible) converging on the player's locked spot; strike 34: two crossing `line(10,2.0)` slashes T2 **BoL**
  (separate groups); perched 40–96 (hittable); drop 96: she drops "backward" to 3 b in front of the player (`mv/ok`),
  wing 104 `sector(6.0,80)` T2 **BoL** (wings open), sweep 112 `sector(5.0,90)` T2; wings held to 140.

**E70 재가 된 만상 — the 70 % event** (`p1_E70_event.jpg` v2 28–37.7; dialog 「힘 뺄 거 없어. 도망칠 수 없을 테니.」)
- At the 70 % floor's next decision: `e70` — glow 0, she rises 1 b (20), the red pool decal spreads from her (40–70,
  cosmetic), **brand 70 = forced bond** + 3 orbs (+ banner only during break windows, i.e. not here), wings 74 (open,
  held to 96), land 96. `rlk_mb_inv` until 70; the floor moves to 1 at 70. From then the ≤ 70 % kit is active (A5, B2,
  C2, D2, E, F, G, H).

---------------------------------------------------------------------------------------------------------------------

## 6. Phase 2 patterns (S4 `p2.py`; form p2: twin scythes, six legs, all hits × `P2_MUL`)

**Q0 낙하 공격 — opening fall** (`p2_Q0_fall.jpg` v4 17.6–21.6; wiki "2페이즈 시작 후 이동 시 바로 낙하 공격")
- After T she hovers far and high (`q0_hover`, 10 b up, 14 b from the player, silhouette with legs spread, visible).
  Trigger: the player moves ≥ 1.5 b from where they stood at T's end, or 80 t. Lock at the trigger → `q0_dive` 0–20
  (visible crimson streak descending), impact 20 `disc(3.0)` T2 **BoL**, blades 28: crimson blade eruption `ring(3,7)`
  T2 **BoL** (separate group). Tell 20 t (big). Once per fight (repeats after a reload in P2 only if it never ran).

**Q1 사형장으로의 초대 (P2) — twin string, up to 6** (`p2_Q1_twin.jpg` v4 28.5–37)
- `q1`: h1 14 spin `disc(4.2)` T1, h2 30 cross slash `sector(4.5,70)` T2, h3 46 **thrown crescent** `pj` (hr 1.0, 1.2 b/t,
  12 b out and back) T1, h4 66 sweep `sector(4.4,80)` T1, h5 82 sweep `sector(4.4,80)` T2, h6 100 double throw (two
  crescents ±15°) T1. Stops after h3 or h5 when the player is > 7 b at that tick (3–6 hits). Plain Pyro.

**Q2 불꽃이 타오르는 낫 — throw then dash** (`p2_Q2_throw_a.jpg` v4 37–40, `p2_Q2_throw_b.jpg` v6 0–5)
- `q2`: windup 0, release 20 a flaming wheel `pj` at the locked point (1.5 b/t), it explodes on arrival `disc(2.2)` T2;
  go 34 she dashes after it to that point (`mv/ok`), slash 42 `sector(4.5,80)` T2.

**Q3 붉은 죽음의 무도회 — rear check** (`p2_Q3_rear.jpg` v6 5–15.5)
- Trigger: the player in her rear ±60° for 20 of 30 t (80 %). `q3`: whip 0 (she whips around, legs flare), spin 14
  `disc(4.6)` T2; then immediately: player ≤ 6 b → `q1` cut to h1–h3; else → two thrown crescents (as Q1 h6) aimed at the
  player (v6 11–13).

**Q4 떠오르는 재액의 달 — beams ×1–3** (`p2_Q4_beam.jpg` v6 15.5–26.5)
- `q4_up` (rises 4 b, backs off to 10–14 b), then per shot `q4_shot`: aim 0 (a thin red **aim line** from her chest to the
  player, tracking, + a growing reticle sigil at her chest — in the air), lock 20, fire 26: beam `line(30,2.2)` from her
  through the locked point T3 **BoL** (scorch decal after, cosmetic); 1–3 shots (2 if the first missed, 3 at ≤ 50 % of
  the P2 pool), shots 50 t apart (v6 17.75 / 20.25 / 22.75), `q4_land`.

**Q5 붉은 피의 연회 (P2)** (scheduled; `p2_Q5_banquet_a.jpg` v6 26–40, `p2_Q5_banquet_b.jpg` v7 0–28; dialog
「이제 네 본심을 볼 수 있겠군.」 / 「형벌을 시작하지.」 / 「일몰은 그저, 모든 것의 시작일 뿐.」)
- Both variants open the same way (raise 0, brand 22 = forced bond + 3 orbs + banner); the AI picks one (50 / 50, never
  the same twice in a row):
- **Q5A 형벌의 핏값** (`q5a`, v7 4.2–12.3; break window 22–121): ring1 60 outline `disc(6)` around her → hit1 95 `disc(6)`
  T3 **BoL**; donut 100 outline `ring(6,15)` → hit2 121 T3 **BoL**; ring3 130 outline `disc(11)` → hit3 158 T4 **BoL**.
  Safe: outside 6 for hit1, inside 6 for hit2, outside 11 for hit3 (the wiki's two outs: counter after hit1, or leave
  after hit2).
- **Q5B 붉은 피의 사형** (`q5b`, v6 31.5–35.3, v7 16–19.3; break window 22–96): x 26–50 she carves a huge **vertical red
  X** in front of her (kit `x_mark`, 4 b, facing the player); s1–s9 56–80 rapid slashing all around her `disc(5.5)` T1 each
  (one group per 2 slashes: ≤ 5 landings); final 96 `pm_disc(7.5, 450)` = `pl_dot` **450 ‰** (S5: **300 ‰**, not x `#mbBolRe`) Pyro **BoL**, non-lethal
  (leaves 1), dash-dodgeable. Wiki: a near-instant kill in Genshin; ours keeps the threat but never one-shots (S5 checks).
- Counter → 12.5 % + stun 140 t.

**Q6 핏빛 연회 — Blood-red feast** (`p2_Q6_feast.jpg` v7 28–40; dialog 「해와 달은 결국 지고 파멸은 계속해서
찾아오지!」 / 「부질없는 저항이군!」 / 「희망은 사라진지 오래다!」)
- `q6`: fly 0 → she rises to 12 b over the arena's north half (stays hittable), moon 30 (the red moon halo flares); six
  volleys 50–100 (every 10 t): crimson feather bolts `pj` from her legs arcing down onto the player's spot (visible ≥ 14 t,
  `disc(1.6)` T1); orbs 110: eight crimson orbs gather around her; toss 125: they fly to the rim (r 22, 45° apart,
  visible, pulsing on the floor); lock 140; dive 160 to the locked spot (8 t streak); impact 168 `disc(4.0)` T3 **BoL** +
  every orb explodes `disc(5.0)` T3 **BoL** (one group with the impact). Safe: between the rim orbs and the dive.

---------------------------------------------------------------------------------------------------------------------

## 7. Phases, AI and difficulty (S3 `ai.py`, weights frozen in `api.py`)

### 7.1 Phase machine
intro (150) → P1a (> 70 %) → [70 % floor] E70 → P1b → [floor 1] T (180, invulnerable) → P2 (Q0 first) → death (110).
Floors as Azhdaha / Tachy: a hit reaching a floor stops there; the step starts at the next decision (the running pattern
finishes). `phases [64, 36]`: P1 pool = 64 % of total; `repool 36` at T 140.

### 7.2 Decisions
Every pattern end + recovery; bands **near ≤ 4.5 · mid ≤ 11 · far > 11**; rear = ±60° behind her.

| pattern | P1a n/m/f | P1b n/m/f | P2 n/m/f | cooldown (t) |
|---|---|---|---|---|
| A (a2 / a4 · a5) | 60 / 10 / 0 | 45 / 10 / 0 | – | 60 |
| B (b1 / b2) | 10 / 35 / 35 | 10 / 30 / 30 | – | 160 |
| C (c1 / c2) | 10 / 30 / 30 | 10 / 25 / 25 | – | 200 |
| D (d1 / d2) | 0 / 25 / 40 | 0 / 20 / 30 | – | 140 |
| E | – | 0 / 20 / 25 | – | 260 |
| G | – | 15 / 20 / 15 | – | 420 |
| H | – | 10 / 15 / 20 | – | 380 |
| F | – | schedule | – | first ≥ 240 t after E70, then every 900 t and ≥ 3 other patterns |
| Q1 | – | – | 60 / 15 / 0 | 60 |
| Q2 | – | – | 10 / 35 / 40 | 160 |
| Q3 | – | – | rear rule | 120 |
| Q4 | – | – | 0 / 25 / 40 | 300 |
| Q6 | – | – | 10 / 20 / 25 | 600; first ≥ 400 t into P2 |
| Q5 | – | – | schedule | first ≥ 300 t after Q0, then every 900 t and ≥ 3 other patterns |
No immediate repeat; far > 14 b for 40 t → D (P1) / Q2 (P2) 60 % else C / Q4; the schedule waits for the current pattern;
pause / reload keep the schedule clock (as Apep's aftermath). Between patterns she walks / strafes facing the player
(0.12 b/t), never teleports (the removed evasion steps are not reused).

### 7.3 Difficulty (chapter 4; compare Apep ch3 and Raiden)
- Registry: `hp 320` (Apep 290), `atk 12`, `dmgMul 150` (Apep 150), `lvAdd 0`, `res {"*":10}`; P2 × 1.2 (the wiki's
  P2 attack is × 1.4 of P1; tempered). Level scaling of chapter 4 already raises HP / damage over Apep.
- S5 fairness sim (copy `S:ap/balance`, same agents and seeds): P1 melee walker %max HP/min 0.95–1.15 × Apep P1
  (127.7), P2 ≤ 1.25 × Apep P3 melee walk, worst 40 t window ≤ 45 %, all hits of one cast on a standing agent ≤ 60 %
  (Q5B final excluded, non-lethal), undodgeable share ≤ 25 %, perfect dasher ≤ 0.3 × Guardian walker; item-less sword
  kill 6.0–7.0 min (Apep 5.95); a counter-using agent ≥ 10 % faster; a no-heal agent (orbs ignored) still survives
  ≥ 2 Banquets from full HP. Adjust tiers ±20 %, `hp` ±15 %, `BOL_*` within ±50 %.
- Raiden (chapters 2 / 5+) is unchanged.

---------------------------------------------------------------------------------------------------------------------

## 8. Arena `fl_ruins` "영락한 폐허" (S1: `tools/mboss_arena_fl_ruins.py`)

### 8.1 Registry entry
```json
"fl_ruins": {"n": 4, "theme": "fl_ruins", "ver": 1, "cx": 760, "cy": 201, "cz": 8, "r": 30, "walk": 26, "safe": 24,
  "start": {"x": 760.5, "y": 201.0, "z": 30.5, "yaw": 180.0, "pitch": 0.0},
  "box": {"x0": 712, "y0": 190, "z0": -40, "x1": 808, "y1": 250, "z1": 56}, "looks": ["day", "crimson"],
  "oob": {"y0": 198, "y1": 230}}
```
Chunks x 44–50 × z −3–3 = 49 (≤ 256), clear of every fixed forceload and of `tk_lift` (37–42). Core adds `#mbAr 4`
radii to `fight_vars`.

### 8.2 Look `day` (P1; `ref/arena.jpg` v5 13 / 16 / 2, v1 33.2, v3 38.6, v1 27.8)
- Plaza (floor y 200, full blocks, flat inside walk 26): pale stone (`smooth_stone`, `polished_diorite`, `calcite`
  tiles) with carved concentric bands (the footage's rings): centre disc r 3 (`chiseled_stone_bricks` star), rings at r 6,
  r 10–11 (double), r 16, r 22–23 with radial spokes every 30° (`polished_andesite` / `stone_bricks`), cracked tiles
  (`cracked_stone_bricks`), moss in seams (`moss_block`, full blocks only).
- r 26–28: a low curb + broken balustrade (`polished_diorite_wall`, `stone_brick_wall`, quartz pillars) with gaps closed
  by the barrier ring (invisible, y 201–215); grass and flowers outside.
- r 28–40: Fontaine ruins — round-window walls and arches (`stone_bricks`, `quartz_bricks`, `polished_deepslate` trim,
  `oxidized_copper` caps), broken columns, ivy, dark trees (dark oak / spruce), rock outcrops and a cliff edge to the south
  and east with a painted sea / mountain band on the dome base.
- Sky: a **block dome** r 44 (Raiden technique): `light_blue_concrete` → `white_concrete` horizon band with
  `white_wool` cloud patches, lit from inside (light blocks in the shell); light layer y 206 over the walk disc (floor
  ≈ 12, no spawns). Ambient (module): drifting white petals (`cherry_leaves` particle tinted white) and the three wisps at
  their rim posts.

### 8.3 Look `crimson` (P2; `ref/arena.jpg` v4 14, 16.5, 24, v7 36)
Look job (runs under T's 20 t blackout; dome shell + backdrop only, the walk floor never changes): dome blues →
`pink_concrete` / `magenta_terracotta` / `red_concrete` bands with a dark crimson zenith (concrete / terracotta only),
the **red moon** = a blocks disc r 6 on the north dome wall (`redstone_block` rim, `red_concrete`
face, `shroomlight` glow ring) + the kit's halo card; outside r 28 a few grass patches → `red_terracotta`, a few `red_stained_glass` panes in the
arches. `fill … replace` boxes ≤ 32 768 blocks, ≤ 4 slices (≈ 16 k blocks).
`ensure` restores `day` at the next fight.

### 8.4 Entrance, gate, spirits
- `entrance_layout()` (dungeon kind-9 zone): a **gravestone** (wiki: "쿠자비나의 이름이 적힌 비석 … 진홍빛 불꽃") of
  `polished_deepslate` / `chiseled_polished_blackstone` with a carved top; the module's `prep` starts a self-rescheduling
  crimson-flame particle chain on it (as cproto's `glow`, stops when the prop is gone, `uninstall` clears the schedule).
  Gate lines (`cprep.arlecchino.gate`): `추억: 빛과 그림자의 결별` / `「아를레키노」` / `영락한 폐허`.
- Spirits: three kit props `wisp` (white flame child-spirits) — around her in E0, at three rim posts from E1, two turn red
  at T, back to white at death. Purely visual (no collision, no hit).

---------------------------------------------------------------------------------------------------------------------

## 9. Registry entry (D0 adds with `enabled:false`, `route:false`; I1 flips both)
```json
{"id": "arlecchino", "n": 12, "fn": "boss/arlecchino", "kind": "chapter", "ch": [4], "route": false, "enabled": false,
 "w": 0, "minCh": 4, "maxCh": 4, "name": "아를레키노", "sub": "우인단 집행관 서열 4위", "color": "#E0303A", "el": 1,
 "hp": 320, "xp": 40, "atk": 12, "lvAdd": 0, "dmgMul": 150, "goldMul": 1, "sap": 0, "picks": 0,
 "scale": 1.4, "hit": {"w": 1.2, "h": 2.9}, "shield": true, "px": false,
 "intro": 160, "death": 110, "deathSnd": false, "arena": "fl_ruins", "theme": "fl_ruins",
 "res": {"*": 10}, "phases": [64, 36],
 "music": {"1": {"ev": "minecraft:music.nether.crimson_forest", "len": "<pool: measured by S1, music_len>"},
           "2": {"ev": "minecraft:music.dragon", "len": 6883}},
 "icon": {"item": "minecraft:netherite_hoe", "model": "rlk:mboss/kn_kit/gate_icon"}}
```
(The boss bar shows 「아를레키노」 through `mboss/title`; the registry name stays plain for lists / help.)

---------------------------------------------------------------------------------------------------------------------

## 10. The phase seam (how P2 plugs in, and what to do if the user sends more P2 material)
- P2 is cleanly separable: its patterns live only in `p2.py` (S4), its clips only in the `*2` / `q*` / `t_p2` / `death`
  rows, its model only in form `p2` + `arlecchino_skin_p2.mjs`, its arena only in look `crimson`. The seam is the P1
  floor (1 %) → T (S2 `seq/t_p2`) → `repool 36` → Q0.
- If P2 had to be dropped temporarily: `phases [100]`, floor 0 in P1, `death` plays in form p1 (the clip keys only the
  shared body parts), S4's PATTERNS empty (the core skips missing patterns, as Tachy's).
- If the user sends a new P2 video / skin: only S2 (P2 clips, skin constant), S4 (Q entries) and the P2 rows of the AI /
  HITS tables change; the contract's P2 clip rows are amended through a request.

---------------------------------------------------------------------------------------------------------------------

## 11. Implementation split (parallel, strict file ownership; Tachy §9 structure)

### 11.0 D0 — contracts (done: branch `wip/ar-d0`, commit eb0a38a on release head fc21fe4)
Writes and freezes on branch `wip/ar-d0` (from the release head): `AR/contract.md` (final), `R:tools/mboss_arlecchino/
api.py` (sections: 1 identity / registry / arena spec `ARENA_SPEC`; 2 damage tiers `DMG`, `P2_MUL`, `HITS` per pattern
`[(clip, event, shape, dims, tier, bol)]`, `DASH_LEN`, tell constants; 3 phases / floors / BoL `BOL_*` / break / stun;
4 AI `BANDS`, `WEIGHTS`, `COOLDOWN`, `SCHEDULE`; 5 keys, ownership `OWN`, test ids; 6 names (scores / tags / storage);
7 rig contract `PARTS`, `LOOKS`, `RIG_CALLS`, `CLIPS {name: (len, loop, {event: tick}, form)}`, `check_manifest`;
8 kit contract `KIT_PRESETS`, `KIT_PROPS`, `KIT_DECALS`, `KIT_SOUNDS`, `KIT_HUD`, `LINES` (dialog ids → text);
9 `Writer`, `Pattern`, `Service`), `R:tools/mboss_arlecchino/stub_rig_manifest.json` (generated from api.py), empty
`seq.py` / `p2.py` stubs, the registry entry (§9, `enabled:false`, `route:false`). Nothing else changes (every existing
generator output byte-identical).

Namespaces: functions `boss/arlecchino/**` (module), `boss/arlecchino/rig/**` (S2), `boss/arlecchino/fx/**` (S1K),
`mboss/arena/fl_ruins/**` (S1 via `build_mboss_arena.py`), `mboss/ar/fl_ruins/**` (core). Scores: objective `kn`
(module), `knRig*` (rig), `knFx*` (kit); tags `rlk_kn_*`; storage `rlk:kn`; RP `rlk:mboss/arlecchino/*` (rig),
`rlk:mboss/kn_kit/*` (kit), font `rlk:mboss_kn` (glyph root text always empty + unstyled). The prefix `kn` is free
(`ak`, `ar` are taken: Azhdaha kit / arena core / the player Arlecchino's `ar*` scores).

### 11.1 Stages and ownership
| stage | owns (writes / deletes only these) | delivers |
|---|---|---|
| **S1 framework + arena + routing** | `tools/build_mboss_core.py` (FN-1 BoL hazard option, FN-3 px:false chapter path), `tools/mboss_lib.py` (FN-1 helper opts, `MUSIC_TRACKS` crimson forest), `tools/mboss_registry.json` (arena entry, music len), `tools/check_mboss_pack.py`, `tools/build_cboss_rooms.py` (only if the theme needs it), new `tools/mboss_arena_fl_ruins.py`; README "챕터 보스" rows (routing ch4, FN-1, arena) | core outputs (`F:mboss/**` except module trees, `F:boss/test/**`), `F:mboss/arena/fl_ruins/**`, `F:room/cboss/arlecchino/**`; arena renders both looks |
| **S1K kit** | new `tools/build_mboss_kn_fx.py`, `tools/mboss_kn_fx_paint.py`, `tools/mboss_kn_fx_manifest.json` (generated) | `F:boss/arlecchino/fx/**`, RP `mboss/kn_kit/**`, font `rlk:mboss_kn`; presets, props, decals, sounds, HUD (badge, banner, dialog lines), gate icon |
| **S2 rig + entry motion + sequences** | new `tools/build_arlecchino_rig.mjs`, `tools/arlecchino_{pose,geometry,paint,clips}.mjs`, `tools/arlecchino_skin_p2.mjs`, `tools/arlecchino_rig_manifest.json` (generated), `tools/arlecchino_rig_api.md`, `tools/mboss_arlecchino/seq.py` | `F:boss/arlecchino/rig/**`, RP `mboss/arlecchino/**`; `F:boss/arlecchino/seq/{intro,t_p2,death}/**` (written by S3's generator from `seq.py`) |
| **S3 core + AI + BoL + P1** | new `tools/build_mboss_arlecchino.py`, `tools/mboss_arlecchino/{core,ai,bond,p1,s3lib}.py` | `F:boss/arlecchino/**` except `rig/`, `fx/`, `seq/`, the `api.P2` pattern dirs: 17 hooks + `prep` + `test/help`, phases / floors / E70, BoL / shock / break / orbs, AI, A–H |
| **S4 phase 2** | `tools/mboss_arlecchino/p2.py` | `F:boss/arlecchino/p/{q0,q1,q2,q3,q4,q5a,q5b,q6}/**` (written by S3's generator): Q0–Q6 |
Then **I1** (lead): merge S1 → S1K → S2 → S3 → S4, registry `enabled` + `route` true, regenerate all, gates; README
section "아를레키노 (`boss/arlecchino/`)" from S3's `readme_arlecchino.md`. **R reviews**: state, fairness + balance
(S5), fidelity vs footage, then **F** fixes, **V** verify, release (stamp "아를레키노 · 4챕터").

### 11.2 Contracts between stages
- **Framework FN-1 (S1 → S3/S4)**: hazard / projectile option `bol` (1–100, % of max HP) set through
  `mboss_lib.hz_opts(bol=…)` / `pj_opts(bol=…)` (and for `#hzPm` hits), stored per hazard / prop like `#hzNoRx`;
  in `mboss/hurt` (and `pl_dot` for `#hzPm`): if the option is set, raw damage × `#mbBolRe mb` / 100 (module-owned score,
  default 100; reset by `cleanup_fight`); after a hit that reached the player (not dodged) `#mbHitBol mb` = the option
  value (read and cleared by the module, like `#mbHitEv`). Options reset with `scoreboard players reset` so mid-boss
  fights carry no new names; mid-boss behaviour identical (`test_m0diff.py`), per-tick cost ≤ +1 command per hit.
- **FN-3**: a chapter entry with `px:false` + `shield:true` runs the whole chapter path (route, gate, start, `cb/inc`,
  floors, repool, bars, won / cancel / lose) — S1 proves it with a test entry or the D0 entry forced on locally.
- **Rig (S2 → S3/S4)**: `api.RIG_CALLS` (`rig/{init,spawn,spawn_hidden,tick,kill,uninstall,play/<clip>,start/<clip>,
  face/{player,track,set},look/<channel>/<v>,state/{normal,hidden},flash,anchor/<name>}`), Raiden / Apep semantics
  (`play` = tick 0 at the next `rig/tick`; event e on the e-th `rig/tick`); the rig never moves the anchor except
  `face/*`; anchors (`hand_r`, `hand_l`, `blade_r`, `blade_l`, `chest`, `palm_r`) for effect positions; manifest =
  stub schema + transforms; `api.check_manifest` must pass.
- **Kit (S1K → S2/S3/S4)**: only through `api.K` (`p`, `prop`, `decal`, `snd`, `hud`) with the names and macro args of
  `api.KIT_*` (tenths of a block / degrees / ticks; `c` 1 Pyro orange, 2 crimson BoL); `K` returns `''` while the kit
  manifest is missing (wrap with `api.lines`). Decals only for the §1.5 list (`api.KIT_DECALS`), each `{r|len,w,yaw,t}`
  with a flash 6 t before the hit. Kit wiring by S3: `cleanup` → `fx/clear` + `fx/hud/clear`, `pause` / `death_start` →
  `fx/clear`, `uninstall` → `fx/uninstall`.
- **Patterns / sequences**: `api.Pattern` / `api.Service`; files `boss/arlecchino/p/<key>/{start,tick,cancel,resume?}`;
  the core calls `start`, `tick` each tick, `cancel` on break / phase step / death / cleanup; `#done kn 1` at the end;
  break windows declared in `api.BREAK_WINDOWS[key] = (t0, t1)` (the core opens / closes them on `#pt`); hits only from
  `api.HITS` and `api.ev`; BoL via the FN-1 option only; heal orbs only via `bond.orbs()`.
- **No cross-stage reference before it exists** (a missing function fails the load): `api.rig`, `api.K`,
  `api.arena_look` return the right line or `''`.

### 11.3 Tests (harness style of `S:ap/tests` / `S:tk/tests`: vendored `S:az/tests_cm/lib` sims + `AR/tests/lib/knsim.py`)
- `test_cm_ar.py` (S1): routing table ch1–ch6 (ch4 → arlecchino after the flip, 2 / 5+ Raiden), gate / start / won /
  cancel / lose with `px:false`, FN-1 (×`#mbBolRe` only on `bol` hazards, event once per landed hit, dodged = no event,
  reset after the fight, mid-boss outputs identical), music pool length.
- `test_arena_fl.py` (S1): walk disc flat full blocks, nothing below y 226 above the walk disc except the light layer,
  barrier closed, both looks reachable and reversible, look job slices within limits, light ≥ 12, box inside the spec.
- `test_kit.py` (S1K): every contract name exists with the right args, pool caps, decal flash timing, pause clear,
  uninstall leaves nothing, vanilla sound ids only (`S:rd/tests/sound_ids.txt`), glyph root rule.
- `test_rig.py` (S2): manifest vs contract, floor-dip and step checks over every clip tick (cup / saucer / scythe tip /
  legs included), avatar models referenced (no copies), P2 skin embedded, UUID / tag set, `kill` / `uninstall` leave
  nothing, seq.py writes only `seq/**`.
- `test_arlecchino.py` (S3): hooks, phase order (intro → P1a → E70 → P1b → T → P2 → death), floors, BoL rules (bond add,
  heal, ×2.5 only while bonded, DoT only after her bond, non-lethal), forced bond skip states, clear → shock, the
  normal-attack predicate per character, break inside / outside windows (clamped true damage, never skips T), stun,
  orbs (count, ring, cap, sweep), AI weights / cooldowns / schedules (seeded), pause / reload per phase, cleanup leaves
  no `rlk_kn_*`, the shock reset and only HER part of the player's bond removed (`#given`, §4.1; a Clorinde / Arlecchino
  player's own bond survives).
- `pat_p1.py` (S3), `pat_p2.py` (S4): every hit tick == clip event, tells ≥ 12 / 20 t, combo gaps ≥ 10 t, shapes /
  reach / tiers / BoL flags, decals only for the §1.5 keys, end points inside walk − 1.5 and never in blocks, heights,
  projectiles (speed, return, wall stop), cancel at every tick leaves nothing.
- I1: `gen_check.py` (every generator twice → identical; documented order and reverse; owned paths only), `ident.py`
  (guardian / butterfly / fieldgen / proto / cproto / azhdaha / apep / tachy / raiden outputs identical except the listed
  shared outputs), `balance/` (S5).

### 11.4 Renders
S1: arena top-down + perspective, both looks, entrance gravestone. S1K: sprite sheet, one strip per preset / decal. S2:
U1 sheet, clip strips, intro strip vs `ref/intro_v1_*`, transition and death strips, pattern pairs. S3 / S4: top-down
hit-shape diagrams over time per pattern (`AR/renders/s3_<key>.png`, `s4_<key>.png`). All ≤ 640 px jpg / png; delete
intermediates.

### 11.5 Gates (every stage before hand-off; all at I1 / V)
1. `bash S:mcsrv/loadcheck.sh <worktree>/roguelike ar_<stage>` → 0 function load failures.
2. `python3 -I S:mcsrv/rplint.py <RP>` → clean (lowercase ids, atlas sources, JSON).
3. Regenerate twice, byte-identical; `python3 tools/check_mboss_pack.py` green.
4. Static rules: no negative `scoreboard … add/remove` literals; macro lines parse with `"help"`; NBT paths valid; no
   `tp` into blocks (destinations via `mv/ok` / safe-floor checks); nothing below the floor (rig floor-dip gate, decals
   at y + 0.02); vanilla sounds only; no glyph-font inheritance; no tutorial text (allowed: names, phase titles, pattern
   names, the badge, dialog lines, the one real-game banner, refusal messages); decals only §1.5.
5. Budgets: atlas ≤ 1.0 M for this boss (rig ≤ 0.15 M, kit ≤ 0.70 M, icon ≤ 0.01 M), stitched items atlas ≤ 13.2 M;
   shown display elements at rest ≤ 6 500; per-tick command cost of a fight tick ≤ Apep's (≈ 830 avg).
6. Suites green; `ident.py` green.

### 11.6 Estimates
| part | functions | size |
|---|---|---|
| rig (26 parts × 42 clips, long intro / banquet / transition / feast clips) | ≈ 2 000 | ≈ 8 MB |
| module core + AI + BoL / shock / break + E70 + HUD + tests | ≈ 480 | 2 MB |
| P1 patterns (A–H, 13 clip variants) | ≈ 560 | 2.5 MB |
| P2 patterns (Q0–Q6) | ≈ 480 | 2 MB |
| kit (engine + ≈ 45 presets / props / decals + ≈ 70 sounds + HUD + lines) | ≈ 400 | 1.8 MB |
| arena `fl_ruins` (+ `mboss/ar/fl_ruins`, entrance) | ≈ 120 + 17 | 1.5 MB |
| framework FN-1 / FN-3 + tests | ≈ 20 | 0.1 MB |
| **total** | **≈ 4 100** | **≈ 18 MB** |
Texture: rig ≈ 0.12 M (P2 skin 4 096, wing / leg cards 2 × 64×256 ×2 looks, cup / saucer), kit ≈ 0.62 M (flame arcs
5×128×64, crimson arcs 5×128×64, spin ring / twirl ring 2×128², wheel 4 frames 64², claw 64², threads / thorns 4×32×128,
blade 32×128, clone 64×128, web 128², flood / cracks / strip / ring decals 5×128², X mark 128², beam + aim line 2×32×128,
reticle / sigil 2×128², moon halo 128², orb 32², feather 32×64, wisp 3 frames 32², brand X 64², embers / ash 4×16²,
badge / banner glyphs), gate icon 0.01 M → **≈ 0.75 M** (items atlas 12.16 → ≈ 12.9 M of ~15.5 M).

### 11.7 Order of work, worktrees, disk
D0 → (S1 ∥ S1K) → (S2 ∥ S3) → S4 → I1 → R (state, fairness S5, fidelity) → F → V → release. At most **three
worktrees** at a time (each ≈ 230 MB + generated; disk ≈ 2.8 GB free): remove each stage worktree after its merge.
RP for stage work: plain copy of the current release RP (`cp -r S:tk/rp AR/rp_<stage>`, ≈ 44 MB; never hard links) for
S1K and S2 only; delete render intermediates. S3 / S4 develop on the D0 stub manifest and kit stubs; S1 tests FN-1 with
cproto / a local forced entry.

---------------------------------------------------------------------------------------------------------------------

## 12. Reference sheets (`AR/ref/`, made with `AR/tools/sheet2.py`, `picks.py`, `capat.py`, `skinview.py`)
- Overviews: `ov_v1.jpg` … `ov_v7.jpg` (1 fps); captions `captions_guide.jpg`; HUD `hud_bars_banner.jpg`.
- Intro: `intro_v5_walkin.jpg`, `intro_v5_approach.jpg`, `intro_v1_tea.jpg`, `intro_v1_summon.jpg`, `intro_v1_fine.jpg`,
  `intro_v1_twirl.jpg`, `intro_v1_stance.jpg`, `intro_v1_overview.jpg`.
- Model: `model_p1.jpg`, `model_p2.jpg`, `model_p2_closeup.jpg`, `skins_p1_p2.jpg`.
- P1: `p1_A_normal_2hit.jpg`, `p1_A_normal_5hit.jpg`, `p1_B_throw.jpg`, `p1_B_throw_overview.jpg`,
  `p1_B_throw2_grab.jpg`, `p1_C_leap.jpg`, `p1_C_wing.jpg`, `p1_D_dash.jpg`, `p1_D_follow.jpg`, `p1_E70_event.jpg`,
  `p1_E_zigzag_a.jpg`, `p1_E_zigzag_b.jpg`, `p1_E_zigzag_far.jpg`, `p1_F_banquet.jpg`, `p1_F_sigil.jpg`,
  `p1_F_field.jpg`, `p1_F_counter.jpg`, `p1_G_blades.jpg`, `p1_G_cross.jpg`, `p1_G_rim.jpg`, `p1_G_field.jpg`,
  `p1_H_clones.jpg`, `p1_H_launch.jpg`, `p1_H_leapback.jpg`, `p1_x_ranged_immunity_REMOVED.jpg` (what is NOT built).
- P2: `p2_T_transition.jpg`, `p2_Q0_fall.jpg`, `p2_Q1_twin.jpg`, `p2_Q2_throw_a.jpg`, `p2_Q2_throw_b.jpg`,
  `p2_Q3_rear.jpg`, `p2_Q4_beam.jpg`, `p2_Q5_banquet_a.jpg`, `p2_Q5_banquet_b.jpg`, `p2_Q6_feast.jpg`.
- Arena: `arena.jpg`.
