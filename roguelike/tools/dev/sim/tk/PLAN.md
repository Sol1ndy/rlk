# 타키 (Tachy) — special boss + rift: implementation plan

Scratchpad `S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`, `TK` = `S:tk`, repo
`R:` = `/home/user/rlk/roguelike`, `F:` = `R:data/rlk/function`. 20 t = 1 s. Footage times are `vN mm.ss`-free seconds
(`v4 13.9` = video v4 at 13.9 s, 60 fps). Every frame sheet cited is in `TK/ref/` (≤ 640 px wide jpg, labelled).

User request (KO, verbatim in the task): a SPECIAL boss, a bit stronger than a mid-boss and about chapter-boss
difficulty; reached through a rift that appears in rooms at a low chance (Sephiria look, `TK/src/rift_ref.png`), never a
node, at most once per run; clearing it = level-up + three item picks; a test function that forces the rift into the
next opened room; boss = Tachy from Stellar Blade (model + patterns from footage only, everything else = our systems,
no parry); some Genshin-element gimmicks; arena + boss-only intro (v1/v2 for the intro, v3–v11 for patterns).

---------------------------------------------------------------------------------------------------------------------

## 0. Decisions at a glance

| item | decision |
|---|---|
| registry | new `kind:"special"` entry `tachy` (n 20, `fn:"boss/tachy"`), arena `tk_lift` (n 3). Runtime = chapter mode (`#mbMode 1`: own arena, floors, music, cine, res) + a new kind tag `#mbKind 2`; entry by rift, reward = level-up + 3 item boxes |
| name / sub | `타키` / `잠식된 제7공수대원` (default; colour `#F2C230`) |
| element | Pyro ⇄ Electro "twin-pole blade" (G1); hits carry the current blade element; no immunity anywhere, `res {"*":10}` |
| phases | P1 망토 (cape, 100→70 %) → M1 mantle → T1 날개 전개 → P2 날개 (70→35 %) → M2 mantle → T2 심연 (arena look `abyss`) → P3 심연 (35→0 %) |
| patterns | 9 families / 11 entries (A1, B1, B2, B3, C1–C3, K, W1, W2, L) + M (mantle) + transitions; no floor decals (footage shows none) |
| gimmicks | G1 twin-pole aura (permanent self-aura, swaps Pyro/Electro), G2 Overload Mantle (shield broken by ANY reaction), G3 Unstable Core (a reaction during a core-glow charge backfires: cancel + stagger) |
| rift | rolled when a combat room is built (3 %, tunable `#riftPm`), at most once per run, never on the boss map / chapter-1 first map; shown when the room is entered (dormant), opens when the room is cleared; walk in (10 t dwell) or click |
| test | `/function rlk:boss/test/rift` (= `rlk:mboss/test/rift`): the next room that gets built holds a rift (any kind but 9 boss / 15 mid-boss). `rift_id {id}` (+ `{id:"help"}`), `special {id}` / `special_ch {id,ch}` (+ help) |
| reward | exactly one level (XP = `xpNeed − xp`, the normal level-up incl. its usual pick) + **3 item boxes** (mid-boss box flow, `picks:3`, chapter rarity) at the rift spot; gold ×`goldMul` 6, sapphire 1 |
| intro | 184 t, boss only, camera-free (no existing boss intro takes the camera: Raiden "카메라는 고정하지 않습니다", mid/chapter intros only `rlk_mb_inv`) |
| budget | ≤ 1.0 M atlas px (plan: rig 0.52 M + kit 0.18 M + rift 0.03 M ≈ 0.73 M → stitched items atlas ≈ 12.45 M / 15.5 M); ≈ 2,900 datapack functions |

Open question for the user (default chosen, build proceeds with it): **reward count** — "레벨업과 함께 아이템 세 개"
is built as *one level-up (which, like every level-up, also grants its normal pick) + 3 item boxes* = 4 selections. The
alternative (level-up whose pick is one of the three, i.e. 2 boxes) is one registry number (`picks`).

---------------------------------------------------------------------------------------------------------------------

## 1. Footage study

### 1.1 What the videos are
- **v1** (`ref/intro_v1_overview_{a,b}.jpg`): cutscene. 0–5 s Tachy hangs limp in a Naytiba nest of cables / tentacles
  under a big lamp-machine (industrial scaffolding, red flesh); 6 s her face entangled; 8–12 s Eve (protagonist, ignore)
  holds her head; 13–14 s the cocoon again; 15–19 s Tachy lies prone on a concrete floor in blood, armour lights glowing
  orange (19 s close-up of orange ring lights); 20–31 s Eve; 32–39 s a giant hydraulic piston machine with thrusters
  descends a shaft (the arena lift).
- **v2** (`ref/intro_v2_0-9s.jpg`, `intro_v2_9-18s.jpg`, `intro_v2_rise.jpg`, `intro_v2_sword.jpg`): 0–1 s Eve; **1.5–
  16.5 s the boss intro** (rise, visor, sword ignite, see §3); 17–21 s Eve; 22–40 s fight start on the round sand
  platform. 32–40 s white pillar / crossing white beams / white streaks = **Eve's** skills (`ref/x_player_fx_v2.jpg`).
- **v3–v7**: a Korean guide video with captions naming each pattern ("장풍 공격 지상/공중", "착지 공격", "블링크",
  "평타 패턴 1/2/3", "연속기+블링크 ×3"). **v7 30 s – v11**: "실전" (a full fight: P1 sand arena, wing reveal v9 0–5,
  transition v10 3.6–6.4, P2 dark arena, the ending cutscene v11 32–39).

### 1.2 Boss effects vs player effects (implementers: do not copy the player's)
| seen | whose | evidence |
|---|---|---|
| orange-red flame arcs along her blade, golden fire crescents, golden lightning from the sky, red core/visor flare, gold blade glint | **boss** | always at her blade / body before or at her hits |
| blue ring around Eve / Tachy, blue-white teleport streaks, white crossing beams, white pillar, pink-white cuts | player (Blink counter, Beta/Burst skills) | v4 32.4–35.8, v2 32–40, v11 29–31 |
| yellow ring that turns blue before a strike | game UI (Blink indicator) | v6 20.2–20.8, v4 39.8–40.0 → we keep only "a gold glint on the blade" |
| big golden-white flash exactly on a hit (v5 7.9, 21.8, 35.0) | player's guard / perfect-parry spark | coincides with Eve's guard pose; the boss's hit itself is the slash |
| "펑" in the captions (B2, B3) | heavy hit (impact), not an AoE | caption "(펑X3) 가드" |

No attack shows a floor marking before the hit → **Tachy gets no floor decal at all** (10-20 telegraph rule). The rift's
floor crack is scenery, not a telegraph.

### 1.3 Model (`ref/model_a.jpg`, `ref/fx_a.jpg` first frame for scale)
- Tall, slim armoured woman, ~1.2× Eve (v8 6.2). Black carbon-weave bodysuit, gunmetal plate armour with hazard
  yellow / gold accents: two yellow bands on the right upper arm and thighs (v2 6.0), hexagon plates on back, collar,
  shoulders and hips (v2 13.0, v9 1.5), a yellow "tie" V on the chest with a 3×3 grid of small yellow lights
  (v2 13.0), orange ring lights on the left shoulder, the right gauntlet, knees and the sword guard (v2 10.5, 14.4).
- Asymmetric arms: massive right pauldron + gauntlet (v2 6.0, 10.5), slimmer left arm.
- Long dark brown / ash hair (looks silver in the warm haze, v2 4.5–6.0), reaching mid-back.
- Helmet: a dark copper-red glossy dome with gold rim, worn up like a hood in the intro, lowered over the face at v2
  11.0 (dark band over the eyes, lips visible), fully closed at 11.5; at 12.5 a **glowing yellow-orange skull** lights up
  inside the visor. In fight the visor is always closed (v9 1.5).
- Wings: in P1 they are folded down her back as a long **cape** (black with bronze-gold feather plates; trails on the
  floor in the intro, v2 1.6–4.0; flutters, v2 8.0–9.5). v9 2.7–4.5 they unfold into large **blade-feather wings**: many
  long black metallic feathers with gold glints (span ≈ 2.4× her height). P2 (v7, v10, v11) adds dark red fleshy
  tendrils among the feathers.
- Weapon: one very long sword (≈ her height): long two-hand grip, a round mechanical guard with an orange ring light,
  a slim slightly curved blade with a serrated mechanical spine and a **yellow glowing edge** (v2 14.0); it ignites into
  flames + sparks (v2 15.2–16.4). In fight the edge glows orange-yellow and trails fire arcs.

### 1.4 Moves found (detail in §4)
A1 gap-close dash (v8 4.0–4.4), B1 wing-wrap two-hit (v5 5.8–8.5, 13.4–15.8), B2 side-step four-hit (v5 18–30),
B3 charged six-hit (v5 30.4–40, v3 0–2), C1–C3 combo + blink-strike (v6 14–39, v7 0–29), K blink ambush + sky plunge
(v4 29.6–40, v6 0–6), W1 ground crescents (v3 9.6–28), W2 air crescents + dive (v3 29–40, v4 0–3.2), L sky landing
(v4 5.8–28), wing reveal (v9 0–5), phase transition (v10 3.6–13), death (v11 32–39).

---------------------------------------------------------------------------------------------------------------------

## 2. Model: display-entity rig (S2)

### 2.1 Scale and silhouette
- Player = 1.8 b. Tachy stands **2.25 b** to the helmet top (×1.25). Hip (pelvis centre) 1.10 b, shoulder top 1.80 b.
- Folded wings / cape: from the shoulder blades to 0.12 b above the floor (1.55 b long, 0.95 b wide). Spread wings:
  each 2.7 b (3 segments 0.95 / 0.95 / 0.80), span ≈ 5.8 b, chord 1.3 b. Never below the floor.
- Sword total 2.30 b: grip 0.40, guard ring Ø 0.24, blade 1.90 × 0.12 × 0.035, curvature 4°, mechanical spine teeth.
  Scabbard 2.0 b diagonally on the back (left shoulder → right hip), stays after the draw.
- Body: husk `scale 1.25` (0.75 × 2.44 b), click shield `hit {w:1.1,h:2.6}`; **no hit proxies** (`px:false`, a humanoid
  fits one body; saves ~2,000 functions).

### 2.2 Parts (40 item displays + shadow; UUID `524c4b4d-544b-4900-8000-0000000000NN`, NN 00–27, shadow 40)
Tags `rlk_room rlk_mb_aux rlk_mb_part rlk_tk_part rlk_tk_<part>`; culling 8 × 6; view range 2; billboard fixed.

| # | part | parent | size (b, w×h×d) | colours / material | looks | bright |
|---|---|---|---|---|---|---|
| 00 | pelvis | root | 0.42×0.22×0.26 | gunmetal plates, yellow trim | — | 13 |
| 01 | abdomen | pelvis | 0.30×0.24×0.20 | black carbon weave, hex side plates | — | 13 |
| 02 | chest | abdomen | 0.46×0.36×0.26 | black suit, yellow V "tie" `#F2C230`, 3×3 light grid | `grid_off` `grid_on` | 13 |
| 03 | chest_glow | chest | 0.20×0.20 overlay | emissive grid / core | `off` `amber` `red` `gold` | 15 |
| 04 | neck | chest | 0.10×0.10×0.10 | black | — | 13 |
| 05 | head | neck | 0.22×0.26×0.24 | pale face `#E9D3C8`, red lips `#9C2A2E`, dark brows (64 px/b) | — | 13 |
| 06 | hair_top | head | 0.28×0.20×0.30 | dark ash brown `#3B2E2A`, highlight `#6E5A50` | — | 13 |
| 07–09 | hair_1 / 2 / 3 | hair_top (chain) | 0.26×0.34×0.06 each | same, tapering | — | 13 |
| 10 | helmet | head | dome 0.34×0.30×0.36 | copper-red gloss `#5A2418`→`#8A3A22`, gold rim `#C99A3A` | `up` (hood) `down` (closed) — animated translation | 13 |
| 11 | visor_glow | helmet | 0.24×0.20 overlay | emissive skull | `off` `pyro` (`#FFB21E`) `electro` (`#FFF0A0`) `abyss` (`#FF3A2A`) | 15 |
| 12 | collar | chest | 0.40×0.18×0.34 | hex plates gunmetal + gold edging | — | 13 |
| 13 | shoulder_l | chest | 0.24×0.20×0.26 | gunmetal, **orange ring light** `#FF8A1E` | — | 14 |
| 14–16 | upper_arm_l / forearm_l / hand_l | chain | 0.11×0.32 / 0.10×0.30 / 0.10×0.14 | black suit, gold seams | hand `open` `grip` | 13 |
| 17 | shoulder_r | chest | 0.34×0.26×0.34 | massive hex pauldron, two yellow bands | — | 13 |
| 18–20 | upper_arm_r / forearm_r / hand_r | chain | 0.14×0.32 / 0.16×0.36 (gauntlet) / 0.12×0.16 | yellow bands, ring light on gauntlet | hand `open` `grip` `fist` | 13 |
| 21 | spine_pack | chest | 0.36×0.50×0.16 | mechanical spine, hex plates, wing mounts | — | 13 |
| 22 | tassets | pelvis | 0.50×0.30×0.40 | armoured skirt plates, yellow edge | — | 13 |
| 23–25 | thigh_l / shin_l / foot_l | chain | 0.15×0.52 / 0.13×0.50 / 0.12×0.30 | black + gunmetal greaves, knee ring light | — | 13 |
| 26–28 | thigh_r / shin_r / foot_r | chain | same | same, yellow thigh band | — | 13 |
| 29–31 | wing_l1 / l2 / l3 | spine_pack | cape 0.48×0.52 / feather 0.95×1.3 each | cape: black + bronze-gold plates; feather: black metal `#0E0E10` sheen `#4A4A55`, gold edge glints | `cape` `feather` `abyss` (+ dark red flesh `#5E1018`) | 13 |
| 32–34 | wing_r1 / r2 / r3 | spine_pack | same | same | same | 13 |
| 35 | sword | hand_r | 2.30 total | dark steel `#2C2C30`, serrated spine, guard ring | `sheathed` (hidden in hand, shown in scabbard) `drawn` | 13 |
| 36 | sword_edge | sword | 1.90×0.05 overlay | emissive edge | `off` `yellow` `pyro` (flame `#FF6A1A`→`#FFC04A`) `electro` (white-gold `#FFE35A` crackle) `glint` | 15 |
| 37 | scabbard | spine_pack | 2.0×0.10 | black, gold fittings | — | 13 |
| 38–39 | tendril_l / tendril_r | spine_pack | 0.12×1.4 | dark red flesh, black tips | scale 0 until T2 | 12 |

Clip-driven secondary motion: hair chain (lag 3 t), wing segments (lag 2 t), cape flutter (sine, 40 t).

### 2.3 Looks / states
- Form: `cape` (P1 + intro), `winged` (from T1), `abyss` (T2 on: wings `abyss` + tendrils shown).
- Visor: `up` + `off` (intro start) → `down` + `pyro`/`electro` (fight; follows G1) → `abyss` red in P3 tells.
- Blade edge follows G1 (`pyro` / `electro`), `glint` during the K / C glint, `off` before the intro ignite.
- `flash` (hit feedback, 3 t), `hidden` (blink gone, high hover out of sight), `mantle` (wings wrapped, cocoon overlay
  card from the kit).

### 2.4 Clips (contract; names / lengths / event ticks frozen at D0; ticks = played clip ticks)
| clip | len | events |
|---|---|---|
| `idle` (per form) | 40 loop | — |
| `walk`, `strafe_l`, `strafe_r` | 24 / 20 / 20 loop | step 0, 12 |
| `backstep` | 12 | land 10 |
| `flinch` | 6 | — |
| `stagger` | 50 (loop 10–50) | — |
| `stun` | 120 (loop 20–100) | rise 100 |
| `swap_pyro`, `swap_electro` | 24 | drag 6, ignite 14 |
| `blink_out` / `blink_in` | 8 / 10 | gone 6 / appear 0, settle 8 |
| `leap_up` / `hover` / `dive` / `land` | 16 / 40 loop / 12 / 16 | lift 6, top 16 / — / impact 10 / settle 14 |
| `leap_high` / `hover_high` | 16 / 40 loop | gone_high 16 |
| `a1_dash` | 34 | flare 0, go 14, hit 20, end 34 |
| `b1_wrap2` | 50 | wrap 0, open 22, hit1 24, hit2 40, end 50 |
| `b2_side4` | 78 | hop 0, land 14, hit1 22, raise 30, hit2 44, hit3 54, hit4 64, end 78 |
| `b3_six` | 112 | glow 0, dash 30, hit1 40, hit2 50, hit3 60, raise 64, bang1 76, bang2 88, bang3 100, end 112 |
| `c1_combo` | 92 | h1 14, h2 32 (spin), h3 46, h4 58, glint 68, thrust 86, end 92 |
| `c2_combo` | 74 | h1 12, h2 24, h3 38, glint 50, thrust 68, end 74 |
| `c3_combo` | 104 | flare 0, h1 22, h2 32, h3 44, h4 60, h5 70, glint 80, thrust 98, end 104 |
| `k_hold` / `k_glint` / `k_leap` / `k_plunge` | 20 loop / 18 / 14 / 20 | — / glint 0, thrust 16 / up 8 / arcs 0, hit 16 |
| `w1_wave` | 88 | plant 0, glow 6, wave1 46, wave2 58, wave3 70, end 88 |
| `w2_air` / `w2_dive` | 66 / 16 | c1 14, c2 28, c3 42, pull 46, go 66 / slash 10, end 16 |
| `l_shock` | 20 | shock 10, end 20 |
| `mantle_in` / `mantle_hold` / `mantle_break` / `mantle_nova` | 24 / 40 loop / 40 / 44 | wrap 12, lift 20 / — / crack 0, fall 20 / swell 0, flash 40, hit 44 |
| `intro` | 184 | see §3 |
| `t1_wings` | 80 | kneel 0, split 10 (model swap), spread 30, flare 50, stand 70 |
| `t2_abyss` | 110 | stagger 0, flare 20, tendrils 36, dark 50, swap 60, rise 90 |
| `death` | 130 | knee 20, sword_plant 36, visor_off 50, wings_fall 70, collapse 100, ash 116 |

Props owned by the rig (`rig/prop/<kind>`): `cables` (6 strands × 3 thin black block-display segments from the
overhead lamp to her body, release/retract animation), `scabbard_glow`. Everything else visual is the kit (§7 S1K).

### 2.5 Reference renders S2 must deliver
`TK/renders/U1_sheet.jpg`: front / side / back / ¾ in each form (cape, winged, abyss) with visor up / down / skull,
next to a 1.8 b player stand-in; clip strips every 4 t for all clips; footage pairs (`ref/model_a.jpg` frames).

---------------------------------------------------------------------------------------------------------------------

## 3. Intro (boss only, from v1 + v2) — `seq/intro`, clip `intro`, registry `intro:190`

Policy (as every existing boss): no camera, no player lock, boss `rlk_mb_inv` until the end, title at the ignite, push
ring (no damage) at the end. The player arrives at the arena start (south edge, 22 b from the centre, facing north) out
of a closing rift tear (§6.4). Sounds are vanilla only (`mboss_lib.sound` min-volume rule).

| beat | source | ticks | boss pose / motion | effects | sounds |
|---|---|---|---|---|---|
| E0 hang | v1 0.0–5.0, 13–14 | 0–30 | hangs limp 7 b above the centre in 6 cables from the lamp machine, head down, hair and cape hanging, slow 1° sway | warm lamp light (arena light blocks), dust motes falling (`falling_dust` sand) | `ambient.basalt_deltas.mood` once 0.5; `block.chain.step` 0.4 at 10, 22 |
| E1 drop | (v1 → v1 15) | 30–44 | cables snap one by one (30, 33, 36), she falls 12 t and lands prone at 42 | cable whip-up (prop), dust ring + sparks at 42 | `block.chain.break` ×3 (pitch 0.7/0.8/0.6), `entity.iron_golem.damage` 0.6 + `block.anvil.land` 0.5 pitch 0.6 at 42 |
| E2 lie | v1 15.0–19.0, v2 1.6 | 44–60 | prone, cape spread over legs as a train; ring lights pulse orange twice | ring-light pulse (looks) | `entity.warden.heartbeat` 0.7 at 48, 56 |
| E3 push up | v2 1.6–4.0 (`intro_v2_rise.jpg`) | 60–84 | arms push the torso up, onto hands and knees, head hanging | sand trickles | `block.piston.extend` 0.5 pitch 0.6 at 62, `item.armor.equip_netherite` 0.6 at 74 |
| E4 rise | v2 4.0–7.0 | 84–108 | crouch, then straighten to standing, head still bowed, hair falling forward | — | `block.copper_bulb.turn_on` 0.4 pitch 0.6 at 96 |
| E5 cape flare | v2 7.5–9.5 | 108–116 | cape (folded wings) flares behind in a gust, she turns her head toward the player | dust gust | `item.elytra.flying` short (stopsound at 116) 0.5 |
| E6 hair | v2 10.0–10.5 | 116–126 | head lifts, right hand sweeps the hair back (face visible) | — | `item.armor.equip_leather` 0.5 |
| E7 visor | v2 11.0–12.0 | 126–136 | helmet slides from `up` over the face to `down` | — | `block.iron_trapdoor.close` 0.7 pitch 0.7, `block.respawn_anchor.charge` 0.5 at 134 |
| E8 skull | v2 12.5–13.0 | 136–142 | visor skull ignites `pyro`, chest grid lights on | glow flicker | `block.beacon.activate` 0.6 pitch 1.4, `entity.blaze.ambient` 0.4 |
| E9 draw | v2 13.4–14.6 (`intro_v2_sword.jpg`) | 142–156 | right hand draws the sword from the back scabbard, sweeps it out low to the right; guard ring lights | — | `item.trident.return` 0.6 pitch 0.8, `entity.player.attack.sweep` 0.5 |
| E10 ignite | v2 15.0–16.5 | 156–170 | raises the blade vertical; the edge ignites `pyro` (flames + sparks) | flame/spark card stream along the edge; **title + sub at 156** | `item.firecharge.use` 0.8, `block.fire.ambient` 0.6, `entity.blaze.shoot` 0.5 |
| E11 stance | (v8 0–3) | 170–184 | lowers into the combat stance; music phase 1 at 176; push ring r 4 (no damage) at 178 | ember burst | `entity.wither.ambient` 0.3 pitch 1.6 |

`mboss` intro ends at 184 (`#mbIntro` 190 cap). Reload during the intro → jump to E11 end (standing, sword lit).
Test: `boss/test/pattern {id:26}` replays the intro (boss invulnerable).

Death `seq/death` (130 t, from v11 32–39 / v10 4–6): knees buckle (20), sword planted (36), visor glow fades (50), wings
sag and shed black feathers / ash (70–100), collapse forward (100), dissolve to ash (116–130, parts shrink at the floor,
never below it). Then the special win path (§7.7).

Transitions: **T1 날개 전개** (`t1_wings`, 80 t, v9 2.7–4.8): kneels, cape panels split (model swap hidden by an ember
burst at 10), wings spread (30) and flare gold (50), push ring r 4 (no damage) at 50, invulnerable throughout.
**T2 심연** (`t2_abyss`, 110 t, v10 3.6–6.4): stagger back, visor flares red (20), tendrils burst from the wing roots
(36), 20 t blindness at 50 (vanilla fade like v10's black frame) during which the arena look job `abyss` runs, music
phase 2 at 60, rise (90). Invulnerable throughout.

---------------------------------------------------------------------------------------------------------------------

## 4. Patterns, AI and difficulty (S3 melee / S4 aerial)

### 4.1 Common rules
- Every attack is a quiet hazard (`#hzQuiet 1`), no floor decal; tells are the pose, the blade colour/glint, the
  chest/visor flare and sounds. First visible motion → hit ≥ 12 t; big (area ≥ 100 b², r ≥ 8, or undodgeable) ≥ 20 t.
  Combo follow-ups ≥ 10 t apart. Aim locks at the tell.
- Damage = `mboss/hurt` coefficient % × `atk` 12 × `dmgMul` 135 (1.00 = 16.2 raw). Tiers: **T1 light 70**,
  **T2 medium 100**, **T3 heavy 135**, **T4 big 170**; nova = `pl_dot` 400 ‰ (non-lethal, leaves 1). S5 balance may move
  them ±20 %.
- Element: blade hits = current G1 element (`#hzEl` / `#pjEl` 1 or 3, 1U, normal player-side reactions); lightning
  attacks (K plunge, L shock, mantle feathers) are always Electro; B3 bangs always Pyro.
- Movement safety: blink / landing / dash end points via `mv/ok` + `mv/leash` inside `walk − 1.5`; the arena floor
  inside walk is flat solid blocks, nothing overhead below y 226, so leaps never enter blocks; parts never below the floor.
- Recovery after each pattern: idle 18–26 t (P3 12–18 t) with slow prowl / strafe facing the player — the punish window.

### 4.2 Pattern entries
Shapes: `sector(r, half°)`, `disc(r)`, `ring(r0,r)`, `line(len,w)` (framework `mboss/hz/*`), `pj` = `mboss/pj/launch`
(blade `#pjShape 1` = crescent). "t" = clip ticks.

**A1 돌진 베기 — gap-close dash** (`ref/t_A1_v8.jpg`, v8 4.0–4.4; `fx_a.jpg` #2)
- When: distance > 7 b (all phases). Tell: chest + visor flare red-orange, blade drawn back low (t 0–14), sound
  `entity.ravager.roar` 0.4 pitch 1.8 + `item.firecharge.use` 0.5.
- Motion: dash 12 b (or to 2 b before the player, max) in 6 t (t 14–20) along the locked line; fire trail.
- Hit: `line(len to stop, w 1.6)` during the dash (T2) + end `sector(3.4, 60)` at t 20 (T2, same group = one hit).
- G3 window: t 0–14.

**B1 날개 가리기 2연격 — wing-wrap double** (`ref/t_B1_v5.jpg`, v5 5.8–8.5; P2+)
- Tell: wings wrap around her front like a closed cloak (t 0–22, 24 t visible, v5 5.8–7.0), blade hidden low behind.
- Motion: wings snap open (22), h1 horizontal slash (24), step 1 b in, h2 rising diagonal slash (40).
- Hits: h1 `sector(3.8, 75)` T2; h2 `sector(3.4, 60)` + `disc(1.6)` T3.
- Near only (≤ 5 b; from mid she walks in during the wrap at 0.12 b/t).

**B2 옆걸음 4연격 — side-step four-chain** (`ref/t_B2_v5.jpg`, `t_B2b_v5.jpg`, v5 18–30)
- Tell: a lateral hop 3 b to her left or right (random) with the sword vertical behind (t 0–14), land (14).
- Hits: h1 lunge slash (22) `sector(3.6, 60)` + 1.5 b step T2; raise overhead (30–44, glow) → h2 overhead heavy (44)
  `line(5, 1.8)` T3; h3 quick sweep (54) `sector(3.2, 90)` T1; h4 quick sweep back (64) `sector(3.2, 90)` T1.
- Near / mid (≤ 8 b); used to turn when the player is behind her.

**B3 충전 6연격 — charged six-chain** (`ref/t_B3_v5.jpg`, `t_B3b_v5.jpg`, v5 30.4–40; P3)
- Tell: stands, chest core + visor glow red (t 0–30, `entity.warden.sonic_charge` 0.5 pitch 1.3), blade low.
- Motion: dash-in (30–40, to 2.5 b), h1 wide fire arc (40) `sector(5.0, 85)` T2, h2 backhand (50) `sector(3.6, 70)` T1,
  h3 (60) `sector(3.6, 70)` T1, raise (64), three heavy chops ("펑" ×3) at 76 / 88 / 100: `sector(3.2, 45)` +
  `disc(1.4)` each T3 Pyro, re-aimed at each raise (≤ 30° turn).
- G3 window: t 0–30.

**C 연속기 + 블링크 — combo then blink-strike** (3 variants; `ref/t_C1_v6_{a,b}.jpg`, `t_C2_v7.jpg`, `t_C3_v7_{a,b}.jpg`)
- C1 (P1+; v6 14–22): h1 diagonal fire arc (14) `sector(3.6,70)` T1; h2 **spin** (32) `disc(4.2)` T2 (full fire ring);
  h3 (46) `sector(3.4,70)` T1; h4 big diagonal (58) `sector(4.0,80)` T2; **glint** (68: gold star on the blade +
  `block.amethyst_block.resonate` 0.8 pitch 1.6 + `item.trident.return`) → **thrust** (86) dash 7 b through the locked
  point `line(7, 1.8)` T3 (18 t after the glint).
- C2 (P2+; v7 0–6): h1 (12) T1, h2 (24) T1, h3 rising (38) `sector(3.6,70)` T2, glint 50 → thrust 68 T3.
- C3 (P3; v7 9.6–15): **red core flare** tell (0–22, G3 window), h1 22, h2 32, h3 44 (T1 each), pose (44–60), h4 60,
  h5 70 (T2), glint 80 → thrust 98 T3.
- After a C, 50 % → G1 swap.

**K 블링크 — blink ambush + sky plunge** (`ref/t_K_v4_{a,b}.jpg`, `t_K_v6_c.jpg`, v4 29.6–40, v6 0–6)
- Vanish: `blink_out` (6 t, gold spark burst + `entity.enderman.teleport` 0.6 pitch 0.6), gone 24 t (body
  `rlk_mb_inv`, parked at her spot, rig hidden).
- Reappear (`blink_in`) 4.5 b from the player (front arc first, then sides; `mv/ok`), wings spread, blade low and
  glowing (v4 36.4–39.6); **hold 20–60 t** (random; P3 10–40).
- Glint (`k_glint` 0) → thrust through the locked point at 16: `line(6, 1.8)` T3.
- Leap (`k_leap`, 14 t, rises 6 b) → **sky arcs**: thin golden lightning arcs crawl down from the sky above the
  player's locked spot for 16 t (v4 33.3–33.9; arcs hang from 8 b up, not a floor marking) → plunge (16): she drops onto
  the spot, `disc(3.5)` T4 Electro, golden lightning burst.
- P3 "K2": after the plunge, one more vanish → reappear → glint → thrust (no second plunge).
- Afterwards G1 swap (always).

**W1 지상 장풍 — ground crescents** (`ref/t_W1_v3_{a,b}.jpg`, v3 9.6–28)
- Precondition: distance ≥ 12 b; otherwise she backsteps + blinks to the far side first (blink_out/in, 34 t).
- Tell: plants her feet, blade held level to the side, gold glow grows along the edge (t 0–40; `block.beacon.ambient`
  0.6 pitch 1.8 + rising `block.respawn_anchor.charge`). G3 window: t 6–40.
- Waves at 46 / 58 / 70: horizontal crescent `pj` blade `hr 3.5` (7 b wide), height covers 0–1.65 b (jumping doesn't
  clear it), 1.25 b/t, life 32 t, wall stop, each aimed at the player when released; T2, current element. Visible
  crescent card + fire trail; impact sparks.

**W2 공중 장풍 + 강하 — air crescents + dive** (`ref/t_W2_v3_{a,b}.jpg`, `t_W2_v4_c.jpg`, v3 29–35, v4 0–3.2; P2+)
- Leap up 6 b (`leap_up`, 16 t), hover. Crescents at 14 / 28 / 42 of `w2_air`: vertical crescent `pj` ball `hr 1.3`,
  1.1 b/t, diagonal down at the player's chest, life 30 t; T2.
- Pull back (46–66: blade back, wings flare; `entity.phantom.swoop` 0.7) → dive (`w2_dive`): she rockets to the locked
  point (≤ 14 b, 6 t), slash at 10: `sector(4.5, 80)` T4 (big arc, ≥ 20 t from the pull) → `land`.

**L 착지 공격 — sky landing** (`ref/t_L_v4_a.jpg`, `t_L_v4_impact.jpg`, v4 5.8–28; P2+)
- Leap high (`leap_high`, 16 t, +13 b, y ≤ 214), `rlk_mb_inv` while high, small glinting silhouette that follows the
  player at 0.15 b/t; glints every 30 t (`entity.phantom.flap` 0.4); hover 80–120 t.
- Dive (`dive`, 12 t, visible streak with dark wings and the blade pointing down), lands on the point locked at the dive
  start (10), planted (`land`), **shock at t 20 after the dive start**: `disc(5.5)` T4 Electro, golden lightning
  burst + `entity.lightning_bolt.impact` 1.0 + `entity.generic.explode` 0.6. Landing impact itself `disc(1.4)` T2.
- Cooldown 700 t (P3 560 t).

**M 과부하 외피 — the mantle** (G2, §5.2; clips `mantle_*`). During it: a glowing feather falls on the player's spot
every 36 t (visible feather `pj` falling from 8 b, 16 t, `disc(1.8)` T1 Electro); nova on failure (`mantle_nova`: swell
0–40 (wings glow white-gold, `block.beacon.power_select` + rising `entity.warden.sonic_charge`), hit 44 =
`hz/full` dodge-able by dash, `pl_dot 400 ‰` Electro, non-lethal).

### 4.3 Phases and AI (`ai.py`)
- Floors (as Azhdaha): 70 % and 35 % (`#mbFloor`); the hit reaching a floor reserves the next phase step, which starts at
  the next decision point: M1 → T1 → P2; M2 → T2 → P3. `phases [100]`.
- Decision every pattern end + recovery; distance bands near ≤ 5 b, mid 5–12 b, far > 12 b; zone behind = rear ±60°.
- Weights (0 = not in that phase):

| pattern | P1 near/mid/far | P2 near/mid/far | P3 near/mid/far | cooldown (t) |
|---|---|---|---|---|
| A1 | 0 / 30 / 45 | 0 / 20 / 30 | 0 / 15 / 25 | 120 |
| B1 | – | 25 / 10 / 0 | 15 / 5 / 0 | 160 |
| B2 | 35 / 15 / 0 | 15 / 10 / 0 | 10 / 5 / 0 | 140 |
| B3 | – | – | 20 / 20 / 0 | 300 |
| C1 / C2 / C3 | 35 / 20 / 0 (C1) | 20 / 15 / 0 (C2), C1 10 / 5 / 0 | 25 / 15 / 0 (C3), C2 15 / 10 / 0 | 200 each |
| K | 15 / 20 / 20 | 10 / 20 / 15 | 15 / 20 / 15 | 260; never twice within 2 patterns, never right after a C |
| W1 | 15 / 15 / 35 | 0 / 15 / 25 | 0 / 0 / 20 | 360 |
| W2 | – | 10 / 20 / 25 | 0 / 15 / 20 | 420 |
| L | – | 5 / 10 / 20 | 0 / 15 / 20 | 700 (P3 560); first use ≥ 200 t into P2 |

- No immediate repeat. If the player stays in the rear zone 20 of 30 t → B2 (hop turns her) 70 % or K 30 %. Far > 14 b
  for 40 t → A1 or W1. P3: recovery shortened, cooldowns × 0.8.
- G1 swap: after every K, 50 % after a C, forced when 600 t (P3 400 t) passed without a swap.

### 4.4 Difficulty target ("중간보스보다 좀 세고 챕터 보스와 비슷")
- Registry: `hp 280`, `atk 12`, `dmgMul 135`, `lvAdd 1` (level = zone level + 1), `res {"*":10}`.
- S5 fairness sim (copy of `S:ap/balance`, same agents and seeds as the Guardian / fieldgen runs): walking melee agent
  HP lost / min = 1.15–1.35 × Guardian, standing agent ≤ 1.8 × Guardian; item-less level-appropriate sword kill time
  150–190 s (Azhdaha ≈ 199 s) incl. mantles; a reaction-using agent kills ~25 % faster (G1–G3 pay off). Adjust tiers
  ±20 %, `hp` ±15 %.

---------------------------------------------------------------------------------------------------------------------

## 5. Elemental gimmicks (S3 owns, `elem.py`)

### 5.1 G1 쌍극 칼날 — twin-pole blade (permanent aura, swap)
- She always carries her blade element as a **self-aura** on the body: `aFire` (Pyro) or `aThunder` (Electro) refreshed
  to 1000 when < 400, every 20 t (score write + `elAct 1`, no damage event; the other aura set to 0 at a swap, so her own
  swap never reacts). Player reactions on her therefore work all fight long: Hydro → vaporize / electro-charged, Cryo →
  melt / superconduct, Dendro → burning / quicken, Anemo → swirl, Geo → crystallize, Pyro ⇄ Electro → overload, Void →
  its void reactions. No element is resisted beyond the flat 10 %.
- Her hits carry the same element → player-side reactions punish taking both colours in a row (built-in system).
- Swap: `swap_pyro` / `swap_electro` (24 t, stationary, punishable): she drags the blade through her left palm, the edge
  changes flame-orange ⇄ white-gold crackle, the visor skull colour follows, a boss-bar badge `◈불` / `◈번개` (element
  colour) changes; sounds `item.firecharge.use` + `block.fire.extinguish` (to Electro: `entity.lightning_bolt.impact`
  0.4 pitch 1.8 + `block.respawn_anchor.charge`). Start element Pyro.
- Learning without text: colour of the blade / visor / badge + the reaction names popping on every hit.

### 5.2 G2 과부하 외피 — Overload Mantle (at 70 % and 35 %)
- `mantle_in`: she wraps herself in the wings, rises 1.2 b, the cocoon glows with alternating Pyro / Electro veins (the
  self-aura alternates every 60 t in sync: orange ⇄ gold), boss-bar under-line = **mantle gauge 100** (gold), badge `◈외피`.
- Body takes 20 % damage (not immune). Gauge damage: **any reaction triggered on her (#rx ≥ 1 on `on_hit`) −12**,
  electro-charged / burning ticks −4, any other hit −1 (once per 5 t). Every element reacts with at least one of the
  two alternating auras, so every character can break it (≈ 9 reactions); physical-only cannot in time (≈ 500 t needed).
- Time limit 360 t (M1) / 300 t (M2). Break → `mantle_break`: drops, **stun 120 t** (takes +50 % damage, `incoming`),
  +15 energy to the player (`char/energy_add`), sound `block.glass.break` + `entity.zombie_villager.cure` low.
  Fail → `mantle_nova` (40 t tell, dash-dodgeable nova, §4.2 M), no stun. Either way the transition follows.
- Feathers fall during the mantle (§4.2 M). Reload / pause keep gauge and time.

### 5.3 G3 불안정한 핵 — Unstable Core (reaction during a charge)
- Core-glow windows (tag `rlk_tk_core` on the body): A1 t 0–14, B3 t 0–30, W1 t 6–40, C3 t 0–22 — exactly the
  red/amber chest + visor flare tells.
- The first reaction on her inside a window → **backfire**: the pattern is cancelled (`cancel` path, hazards removed),
  orange-gold explosion at her chest (kit `core_burst`), `mboss/true_pct {pct:3}`, `stagger` 50 t (+30 % damage taken).
  Once per pattern; not during a mantle.
- Learning: big pop + stagger the first time a player happens to react on a glowing core; no text.

---------------------------------------------------------------------------------------------------------------------

## 6. Arena `tk_lift` (S1K: `tools/mboss_arena_tk_lift.py`)

### 6.1 Registry entry
```json
"tk_lift": {"n": 3, "theme": "tk_lift", "ver": 1, "cx": 640, "cy": 201, "cz": 8, "r": 27, "walk": 24, "safe": 22,
  "start": {"x": 640.5, "y": 201.0, "z": 30.5, "yaw": 180.0, "pitch": 0.0},
  "box": {"x0": 600, "y0": 190, "z0": -32, "x1": 680, "y1": 250, "z1": 48}, "looks": ["dust", "abyss"],
  "oob": {"y0": 198, "y1": 235}}
```
Chunks x 37–42 × z −2–3 = 36 (≤ 256), clear of every fixed forceload (plaza 176–223, cp_test ends at 556).
Core adds `#mbAr 3` radii (W10 240, S10 220) to `fight_vars`.

### 6.2 Look `dust` (P1/P2, from v2 22–40, v8, v6: `ref/intro_v2_overview_b.jpg`, `t_C1_v6_a.jpg`)
A round industrial lift platform at the bottom of a shaft, half buried in sand, warm orange haze.
- Floor (y 200, full blocks only, flat inside walk 24): base `smooth_sandstone` with `sandstone` / `cut_red_sandstone`
  noise and `sand` drifts (flat, single layer); concentric grooves at r 6, 11, 16, 21 (1 b, `polished_deepslate`); centre
  disc r 4 `waxed_weathered_cut_copper` ring + `waxed_cut_copper` core (the rusty raised disc of v2 2.0); four 5×5 hatch
  panels at r 14 on the diagonals (`polished_tuff` with a `yellow_concrete` / `black_concrete` hazard border).
- Wall ring r 25–27, h 10: `polished_blackstone_bricks` + `iron_bars` windows + `chain` columns every 30°, Naytiba
  flesh patches (`nether_wart_block`, `crimson_hyphae`, `shroomlight` nodes) on 1/3 of the ring; barrier cap y 211–225.
- Beyond the wall (decor, r 28–38): truss towers (`iron_bars` + `chain` + `waxed_copper_block` girders) with
  `ochre_froglight` lamps (the red-orange scaffolds of v2), flesh tendrils on the shaft wall.
- Overhead: the **lamp machine** of v1 at y 226–240 over the centre: a cylinder Ø 9 (`polished_deepslate`, two
  `yellow_concrete` bands, `iron_block` rim), lamp underside ring `ochre_froglight` + `light` blocks, drooping cables
  (`chain`, `black_wool` strands) — the intro's cables hang from it. Dark shaft ceiling y 242 (no sky).
- Light: `light` blocks y 206 over the walk disc (floor ≈ 12, no spawns), warm. Ambient (module): `falling_dust`
  (sand) motes, `white_ash`.
### 6.3 Look `abyss` (P3, from v4 / v7 / v10 7–13: `ref/t_L_v4_a.jpg`, `t_C3_v7_a.jpg`)
Look job (floor top layer of the walk disc + wall accents, ≈ 2.6 k blocks, 1–2 slices; runs under T2's blindness):
sand → `deepslate_tiles` / `cracked_deepslate_tiles` / `tuff_bricks`, red veins `red_nether_bricks` with `shroomlight`
nodes every ~6 b (glow, full blocks; no magma — it burns), copper disc → `cracked_polished_blackstone_bricks`,
more flesh on the wall. Light layer unchanged. Reset to `dust` by the framework's ensure at the next fight.
### 6.4 Entry / exit
- Arrival: player at `start` (south edge, facing the centre where Tachy hangs). A **rift tear** (same models as the
  dungeon rift, §7.3) stands 1.5 b behind the start and closes over 30 t (kit `fx/p/arrive_rift`).
- Win: the player returns to the rift spot in the dungeon (§7.7). Cancel: same, the rift stays open.

---------------------------------------------------------------------------------------------------------------------

## 7. Rift system (S1: `tools/build_rift.py` → `F:room/rift/**` + shared hook lines; framework `F:mboss/sp/**`)

### 7.1 Where / when
- Natural roll in `room/zone_build` (the moment a room is opened — its door revealed — or the map's first zone built),
  `@s` = zone marker. Eligible: run active (`#active room 1`), no boss test (`#mbTest`, `#rdTest` ≠ 1), `#riftUsed room
  0`, `#mapType ≠ 8` (not the boss map), not (`#chapter 1` and `#mapIdx 0`), `zkind 1` (combat room), any chapter.
- Chance `#riftPm room` per mille, default **30 (3 %)** ("조절 지점" row). ≈ 17 combat rooms per chapter → ≈ 35 %
  per chapter-1, ≈ 78 % per 3-chapter run.
- Success: zone tag `rlk_riftz`, `data.rift:{id:"<special id>"}` (special roll: `mboss/sp/roll` over enabled `kind
  special` by `w`, chapter range, unmet-this-run first), `#riftUsed 1` (**at most once per run**; it counts even if never
  entered), `mboss/sp/prep {id}` = forceload the special's arena + start its ensure job now (built long before the room
  is cleared; one arena job at a time is fine — chapter arenas only build on boss maps, which never roll a rift).
- Never a node: no node entry, no zone-kind change, no map-title change; the room keeps its kind and contents.

### 7.2 Showing, opening, persistence
- `room/zone_enter` / `room/zone_first` on a `rlk_riftz` zone → `room/rift/show`: pick the spot (7.4), summon the rift.
  Combat room → **dormant** (half size, dim, sparse arcs, not enterable) — the player sees it during the fight.
  Non-combat room (only via the test) → open at once.
- `room/combat_clear` on that zone (the room's own fight) → `room/rift/open` (grow 20 t, burst, sounds). Why only after
  the clear: one zone hosts one fight at a time (`#combat` = zid, `rlk_zmob`, door locks); entering mid-fight would leave
  live mobs and a locked room behind; Sephiria's rift is likewise taken in a quiet room.
- Persistence: rift entities are `rlk_room` → they stay while the map exists (leave and come back: still there), go with
  the map (`room/clear`, `room/wipe`, run end, `uninstall`). `room/rift/forget` (from `room/clear`) resets `#riftOn`;
  `mboss/cleanup` already releases every arena forceload (generated line for `tk_lift`). `/reload`: `room/rift/init`
  re-derives `#riftOn` from an existing `rlk_rift` marker.

### 7.3 Look (from `src/rift_ref.png`: a black hole-tear with crackling white-blue lightning and a lit floor)
- `void`: item_display, billboard vertical, 1.7 × 2.6 b black ragged tear (model `rlk:rift/void`, 64×96 px, black with
  a 1–2 px ragged edge), brightness 0 look; `rim`: same shape 1.1× behind, emissive white-cyan (`#E8FBFF` → `#7FD8FF`),
  brightness 15, slow 0.97–1.03 pulse.
- `crack`: flat floor card 3.2 b (`rlk:rift/crack`, 64×64: black jagged cracks + faint cyan glow), y + 0.02.
- `arc` ×3: lightning cards (`rlk:rift/arc_0..3`, 32×64 frames) around the rim, frame every 2 t, re-rolled roll angle
  every 4 t, billboard center.
- Particles (open, every 2 t): `electric_spark` ×2 on the rim, `end_rod` ×1 drifting, `squid_ink` ×1 at the edge,
  `reverse_portal` ×2 pulled in; dormant every 6 t at a third of that. Text: label `균열` (white, bold) above, hint line
  "▶ 좌클릭" when aimed (existing hover machinery; no other text).
- Sounds (vanilla): open `entity.lightning_bolt.thunder` 0.4 pitch 1.6 + `block.end_portal.spawn` 0.5 pitch 1.3;
  ambient every 40 t `block.respawn_anchor.ambient` 0.6 + crackle `entity.lightning_bolt.impact` 0.15 pitch 1.9 (random);
  enter `block.portal.trigger` 0.5 + `entity.enderman.teleport` 0.8 pitch 0.6; close `block.respawn_anchor.deplete` 0.8 +
  `block.beacon.deactivate` 0.6.
- Sprites ≈ 0.03 M px, owned by `build_rift.py` (RP `assets/rlk/{textures,models/item,items}/rift/*`, lowercase ids).

### 7.4 Spot (`room/rift/spot/*`)
Random cell point of the zone (as `room/mob_try`), ≤ 24 tries, the ground found like `room/mob_up`; accept when: 3×3
footprint of solid non-`#rlk:no_spawn` floor at the same y, 3 b of `#rlk:dash_pass` above all nine, not over a pit
(fall boxes), ≥ 3 b inside the cell walls, ≥ 4.5 b from every `rlk_door`, ≥ 3.5 b from every `rlk_obj` / `rlk_odisp`
(node objects, shop stands, gates), ≥ 5 b from the player. Fallback: the zone centre ground (`mob_up`), then the
player's `rlk_safe` spot + 2 b forward. The marker faces the zone centre (`data.yaw`).

### 7.5 Entering
- Walk in: player body ≤ 1.0 b horizontal / |dy| < 1.5 from the anchor for **10 consecutive ticks** while open, `#combat
  0`, not in the selection space / map screen / dead (particles converge during the dwell). Or click (`oact 17`,
  `room/obj/k_rift` makes the hover marker + label; `room/obj/click` already refuses during combat).
- `mboss/sp/gate` (mirrors `mboss/gate` + `cb/gate`): peaceful → refuse (message like the mid-boss); arena job running
  (`#mbArBuild ≥ 1`) → "균열이 아직 안정되지 않았습니다. 잠시 뒤 다시 들어가세요." and a 40 t re-entry cooldown (the
  player is not moved); else kill the hover group, `room/combat_start` on the rift's zone (doors lock), `#spOn mb 1`,
  `#spawnT room 30`, title/sub, sounds, the rift state `entering` (bright pulse); the player is pulled to the anchor feet
  (safe spot) with blindness at 20 t; `room/mob_wave` (hook) → `mboss/sp/start_zone` (reads `data.rift.id`) → `sp/start {id}` → arena wait (`sp/wait`, as
  `cb/wait`) → `start_go` → `ret` overwritten with the rift spot (`sp/ret_rift`, yaw toward the room centre) → `tp_in`.

### 7.6 Test commands (S1; help per `tools/help_lib.py`)
- `/function rlk:boss/test/rift` (= `rlk:mboss/test/rift`, no argument): arms `#riftForce room 1` and says
  "[균열] 다음에 여는 방에 균열이 나타납니다. (보스 · 중간보스 방 제외)". The **next zone built** (door reveal, or a new
  map's first zone) of any kind except 9 / 15 gets the rift regardless of chance, `#riftUsed`, map type, chapter or test
  state; the force is then cleared (and `#riftUsed` set). Works before `run/start` too (the first zone of the run).
- `rift_id {id:"tachy"}` = the same with a fixed special boss; `{id:"help"}` lists `kind special` entries (help_lib
  `head` + `row`, `check_lines`; the numeric line moves to `rift_id_do`).
- `special {id}` / `special_ch {id,ch}`: a run-less real fight (like `test/chapter`): builds a real node map (chapter
  `ch`, map 2), forces the rift into the first opened combat room with no mobs (`#spAuto`), stands the player before
  it and enters when the arena is ready. `{id:"help"}` / `{id:"help",ch:1}` lists specials.
- Existing `boss/test/{pattern,lock,kill,abort,level,stop}` work for the special (dispatch by `#mbId`); `pattern
  {id:"help"}` prints Tachy's `test/help`. README "명령 도움말" table gets the new rows.

### 7.7 Reward and exit (`mboss/sp/clear` → `sp/won` → `sp/reward`)
- `room/combat_clear` on the rift zone during a special fight → `sp/won` (as `cb/won`: gold absorbed from the arena,
  `cleanup_fight`, `tp_out` to the rift spot, arena forceload off) returning `#mbKilled`.
- Killed: `room/rift/close` (collapse 30 t: rim shrinks, arcs snap inward, implosion `reverse_portal` + `flash`, then
  removed; the zone tag becomes `rlk_riftdone`), title `타키 처치` / sub `레벨 업 · 아이템 상자 3개`, then
  1) **level-up**: `#xpAdd tmp = xpNeed − xp` → `player/level/add_xp` (one level, the normal fanfare and its usual pick);
  2) **3 item boxes**: `execute as <zone> at <rift anchor> run function rlk:mboss/box/drop_all` with `#mbPk 3`
  (chapter rarity, `pkMb` items-only picks, the existing open/spend flow); 3) gold × `goldMul` 6 and 1 sapphire shard
  through the kill (`miniboss` tag on the body → `combat/gold_drop`'s mid-boss multiplier).
- Not killed (`/kill`, spawn failure, lost body, `test/abort`): no reward, the rift reopens (`room/rift/reopen`).
- Defeat in the arena = the normal run failure (as mid-bosses).

### 7.8 Shared-file hook lines (inserted idempotently by `build_rift.py`, marker comment `# rift (build_rift.py)`)
| file | line |
|---|---|
| `room/zone_build` | after `zst 1`: `function rlk:room/rift/roll` |
| `room/zone_enter` | after `zst 2`, before the combat return: `execute if entity @s[tag=rlk_riftz] at @s run function rlk:room/rift/show` |
| `room/zone_first` | last: same `show` line |
| `room/combat_clear` | before the kind-9 lines: `execute if entity @s[tag=rlk_riftz] if score #spOn mb matches 1 run return run function rlk:mboss/sp/clear` and `execute if entity @s[tag=rlk_riftz] run function rlk:room/rift/open` |
| `room/mob_wave` | first: `execute if entity @s[tag=rlk_riftz] if score #spOn mb matches 1 run return run function rlk:mboss/sp/start_zone` |
| `room/obj/click` | `execute if score @s oact matches 17 run return run function rlk:room/rift/click` |
| `room/tick` | `execute if score #riftOn room matches 1 run function rlk:room/rift/tick` |
| `room/clear` | `function rlk:room/rift/forget` |
| `run/start` | `scoreboard players set #riftUsed room 0` |
| `load` | `#riftPm room 30` in "조절 지점" + `function rlk:room/rift/init` |
| `uninstall` | `function rlk:room/rift/uninstall` |

Core-generated changes (S1 in `build_mboss_core.py`): `mboss/box/drop_all` clamp 3 + a 3-box `row` (−1.5 / 0 / +1.5 b);
`register` (`sreg[]`, `sbyid`), `fight_vars` (`#mbMode 1`, `#mbKind 2` for special, `#mbAr 3` radii), `start_cancel` /
`test/won` / `test/defeat` wording for special, `mboss/sp/**`, `mboss/test/{rift,rift_id,rift_id_do,special,
special_ch,help_special}`, `boss/test/{rift,rift_id,special,special_ch}` aliases. `mboss_lib`: kind `special`
(validation: own arena required, `picks` 1–3, `lvup` 0/1, `w` ≥ 0, no `ch`/`route`; `fn` may be `boss/<id>`),
`special_bosses()`, `SPECIAL_HOOKS = []` (the 17 hooks + `test/help` suffice). `check_mboss_pack.py`: special entries.

---------------------------------------------------------------------------------------------------------------------

## 8. Registry entry (S1 adds; S3 tunes numbers)
```json
{"id": "tachy", "n": 20, "fn": "boss/tachy", "kind": "special", "enabled": true, "w": 10, "minCh": 1, "maxCh": 99,
 "name": "타키", "sub": "잠식된 제7공수대원", "color": "#F2C230", "el": 1,
 "hp": 280, "xp": 45, "atk": 12, "lvAdd": 1, "dmgMul": 135, "goldMul": 6, "sap": 1, "picks": 3, "lvup": 1,
 "scale": 1.25, "hit": {"w": 1.1, "h": 2.6}, "intro": 190, "death": 130, "deathSnd": false,
 "arena": "tk_lift", "theme": "tk_lift", "res": {"*": 10}, "phases": [100],
 "music": {"1": {"ev": "minecraft:music.nether.basalt_deltas", "len": "<max track, measured>"},
           "2": {"ev": "minecraft:music.dragon", "len": 6883}},
 "icon": {"item": "minecraft:blaze_rod", "model": "rlk:mboss/tk_kit/gate_icon"}}
```
`music.nether.basalt_deltas` is a pool: S1 measures its tracks from the 26.3 asset index into `MUSIC_TRACKS`
(as AP-FW did) and uses `music_len`.

---------------------------------------------------------------------------------------------------------------------

## 9. Implementation split (parallel, strict file ownership)

### 9.0 D0 — contracts (lead, ½ day, before the stages)
Writes and freezes: `TK/contract.md` (this plan's §2.4 clip table, §4 hit table, kit call list, scores / tags / storage,
test ids), `R:tools/mboss_tachy/api.py` (constants: `DMG` tiers, `CLIPS` {name: (len, {event: tick})}, `EL`, kit-call
stubs `K.*` that emit `function rlk:boss/tachy/fx/...` lines, score names), `R:tools/mboss_tachy/stub_rig_manifest.json`
(schema of the Apep stub: parts, clips, events, looks; the core reads it until S2's manifest lands), the registry entry
with `enabled:false`. Branch base = current release HEAD.

Namespaces: function roots `boss/tachy/**` (module), `boss/tachy/rig/**` (S2), `boss/tachy/fx/{card,cardx,look,clear,
uninstall}` + `fx/{e,p,tele,snd,hud,prop,test}/**` (S1K), `mboss/sp/**` + `room/rift/**` (S1), `mboss/arena/tk_lift/**`
(S1K via `build_mboss_arena.py`), `mboss/ar/tk_lift/**` (core). Scores `tk*` (rig `tkRig*`), tags `rlk_tk_*`, storage
`rlk:tk`; rift: scores `rift*` (+ `#rift*` holders in `room`), tags `rlk_rift*`, `oact 17`; RP ids `rlk:mboss/tachy/*`,
`rlk:mboss/tk_kit/*`, `rlk:rift/*`, font `rlk:mboss_tk` (glyph root text always empty + unstyled: no glyph-font
inheritance).

### 9.1 Stages and ownership
| stage | owns (writes / deletes only these) | delivers |
|---|---|---|
| **S1 framework + rift** | `tools/build_mboss_core.py` (special kind, `mboss/sp/**`, box row of 3, tests + aliases + help), `tools/mboss_lib.py`, `tools/mboss_registry.json`, `tools/check_mboss_pack.py`, `tools/build_rift.py` → `F:room/rift/**`, `room/obj/k_rift`, RP `rift/*`, the hook lines of §7.8, README sections "특수 보스 · 균열" + help rows | rift E2E with a stand-in boss (`proto`-like `spproto` entry, `w 0`) and the `cp_test` arena until `tk_lift` lands |
| **S1K kit + arena** | `tools/build_mboss_tk_fx.py` + `tools/mboss_tk_fx_paint.py` → `F:boss/tachy/fx/{card,cardx,look,clear,uninstall}`, `fx/{e,p,tele,snd,hud,prop,test}/**`, RP `mboss/tk_kit/*`, font `rlk:mboss_tk`, `tools/mboss_tk_fx_manifest.json`; `tools/mboss_arena_tk_lift.py` (theme: `layout`, `look_lines("abyss")`, `entrance` none) | presets (§9.2), sound recipes, HUD badges / mantle gauge cells, arena both looks |
| **S2 rig + sequences** | `tools/build_tachy_rig.mjs`, `tachy_{pose,geometry,paint,materials,clips}.mjs`, `tools/tachy_rig_manifest.json`, `tools/tachy_rig_api.md` → `F:boss/tachy/rig/**`, RP `mboss/tachy/*`; `tools/mboss_tachy/seq.py` (intro, death, T1, T2 bodies) | U1 sheet, clip strips, manifest (clips/events exactly D0's) |
| **S3 core + AI + gimmicks + melee** | `tools/build_mboss_tachy.py`, `tools/mboss_tachy/{core,ai,elem,mantle_core,p_melee}.py` → `F:boss/tachy/**` except `rig/`, `fx/` kit files and `p/{k,w1,w2,l,mantle}/**` | hooks (17 + `test/help`), phases / floors, G1–G3, AI, A1 B1 B2 B3 C1–C3, tests ids, HUD wiring, reload / pause |
| **S4 aerial + ranged + mantle hazards** | `tools/mboss_tachy/{p_air,p_mantle}.py` → `F:boss/tachy/p/{k,w1,w2,l,mantle}/**` | K (+K2), W1, W2, L, mantle feathers + nova; blink / leap safety |
Then **I1 integration** (lead): merge order S1 → S1K → S2 → S3 → S4, `enabled:true`, regenerate all, gates. **R reviews**
(state / fairness+balance S5 / fidelity vs footage), **F fixes**, **V verify**, release.

### 9.2 Contracts between stages
- **Clips**: names, lengths, events of §2.4 (S2 must match D0 exactly; S3/S4 take hit ticks from `api.CLIPS`; a rig
  manifest mismatch fails `build_mboss_tachy.py`). Rig API (Apep/Raiden style): `rig/{init,spawn,tick,play/<clip>,
  start/<clip>,face/{player,track,set},look/{form,visor,edge,chest,hands}/<v>,state/{normal,hidden},flash,prop/<kind>,
  prop/clear,kill,uninstall}`; anchor = body; the rig never moves the anchor except `face/*`.
- **Kit presets** (`fx/p/<name>`, args in tenths, executor/position as noted): `slash_arc {r,yaw,pitch,roll,el}`,
  `spin_ring {r,el}`, `thrust_trail {len,el}`, `dash_trail {len,el}`, `glint` (at the blade tip), `core_flare {c}`,
  `core_burst`, `crescent_h {el}` / `crescent_v {el}` (looks for `pj` cards), `sky_arcs {r,t}`, `bolt`, `shock_ring {r}`,
  `ember_burst`, `blink_out`, `blink_in`, `wing_flare`, `feather` (pj look), `cocoon {pct}`, `cocoon_crack`, `nova_swell
  {t}`, `nova_flash`, `ignite_blade`, `dust_ring {r}`, `swap_fx {el}`, `arrive_rift`, `ambient_dust`, `gate_icon` model.
  Sound recipes `fx/snd/<name>` for every sound named in §3–§5. HUD: `fx/hud/badge {el}` (`◈불` `◈번개` `◈외피`),
  `fx/hud/gauge {pct}`, `fx/hud/clear`. Kit wiring: `cleanup` → `fx/clear` + `fx/hud/clear`; `pause` → `fx/clear`;
  `death_start` → `fx/clear`; `uninstall` → `fx/uninstall`.
- **Hazards**: only framework `mboss/hz/{disc,sector,line,full}`, `pj/launch` (+ `#pjShape 1`), `grp_new`, `pl_dot`,
  `true_pct`, `mv/*`, `push/ring`, `cine/*`; options via `mboss_lib` helpers; all `#hzQuiet 1`, no tele.
- **Damage tiers** via `api.DMG` only; **elements** via `api.EL` (G1 current element score `tkEl` 1/3).
- **Pattern files**: `boss/tachy/p/<pat>/{start,tick,cancel,pause?,k/<t>}`; the core calls `start`, then `tick` each
  tick, `cancel` on G3 backfire / phase step / death / cleanup; patterns set `#tkDone 1` at their end.
- **G3**: patterns tag the body `rlk_tk_core` exactly in their window (helpers `api.core_on(t0,t1)`).
- **Special framework** (S1 → S3): `mboss/sp/*` never calls module code except through the existing dispatchers; the
  module reads `#mbKind 2` only for wording.

### 9.3 Tests (harness in the `S:ap/tests` style: vendored `az/tests_cm/lib` sims + `TK/tests/lib/tksim.py`)
- `test_rift.py` (S1): eligibility table (kinds, map types, ch1 map 0, tests, peaceful), 3 % roll statistics (seeded),
  once per run (incl. never-entered), force arm (every kind but 9/15, before `run/start`, cleared after use), spot rules
  over all 30 normal + 12 first + 12 level-up layouts × 5 themes × 40 seeds (doors ≥ 4.5, objects ≥ 3.5, footprint, no
  pit), dormant → open on clear, walk-in dwell, click, refusals (combat, arena building), persistence (leave / return),
  map change cleanup (entities, forceload, `#riftOn`), cancel → reopen, kill → closed + level + 1 + 3 boxes + pkPending,
  reload in each rift state.
- `test_special.py` (S1): registry validation, `sreg`, dispatch, `fight_vars`, start / wait / won / cancel / lose /
  pause / reload, `drop_all` rows of 1–3, wording, tests + help output (`help_lib` format).
- `test_tachy.py` (S3): hooks, phases / floors / M → T order, G1 aura refresh and swap (no self-reaction), G2 gauge math
  per reaction type, G3 windows == tells, AI weights / cooldowns / no-repeat (seeded), stun / incoming multipliers,
  pause / reload per phase, cleanup leaves nothing (`rlk_tk_*`).
- `pat_melee.py` (S3), `pat_air.py` (S4): every hit tick == clip event, tell ≥ 12 / 20 t, shapes / reach, tiers,
  elements, no tele, blink / landing spots inside walk − 1.5 and never in blocks, leap heights ≤ 214, parts never below
  the floor.
- `gen_check.py` (I1): every generator twice → identical; documented order and reverse; owned paths only.
- `ident.py` (I1): guardian / butterfly / fieldgen / proto / cproto / azhdaha / apep / raiden outputs byte-identical
  except the listed shared files (diff pinned, as `az/tests_cm/baseline/shared_edits.diff`).
- `balance/` (S5): fairness agents (stand, melee walker, ranged walker, reaction user), targets §4.4.

### 9.4 Renders
U1 rig sheet + clip strips vs footage (S2); kit sprite sheet + preset strips (S1K); arena top-down + perspective, both
looks (S1K); rift dormant / open / closing next to `src/rift_ref.png` (S1); intro beat strip next to
`ref/intro_v2_0-9s.jpg` / `intro_v2_9-18s.jpg` (S2); per-pattern strips next to the `ref/t_*` sheets (S3/S4). Offline
renderer `S:az/understand/rigtech_render.py` (wrapper as `S:ap/rigwork/r1/r.sh`).

### 9.5 Gates (every stage before hand-off, all at I1 / V)
1. `bash S:mcsrv/loadcheck.sh <worktree>/roguelike tk_<stage>` → 0 function load failures.
2. `python3 -I S:mcsrv/rplint.py <RP>` → clean (lowercase ids, atlas sources, JSON).
3. Regenerate twice, byte-identical (`gen_check.py`); `python3 tools/check_mboss_pack.py` green.
4. Static rules (scripts from `S:check_*.py`): no negative `scoreboard ... add/remove` literals, macro lines parse with
   `"help"`, NBT paths valid, no `tp` into blocks (all destination via `mv/ok` / safe-floor checks), nothing below the
   floor (rig floor-dip gate), vanilla sounds only (`S:rd/tests/sound_ids.txt`), no glyph-font inheritance, no tutorial
   text (only names, phase titles, badges, gauge, the rift label/hint, refusal messages).
5. Budgets: Tachy atlas ≤ 1.0 M px (rig ≤ 0.52 M `ATLAS_BUDGET`, kit ≤ 0.18 M, rift ≤ 0.03 M), stitched items atlas
   ≤ 12.7 M; shown display elements at rest ≤ 6,500; per-tick command budget of a fight tick ≤ Apep's.
6. Test suites green; `ident.py` green.

### 9.6 Estimates
| part | functions | size |
|---|---|---|
| rig (40 parts × 44 clips, Raiden 751 / Guardian 1,429 / Apep 3,175 as anchors) | ≈ 1,300 | ≈ 7 MB |
| module core + AI + gimmicks + seq + HUD + tests | ≈ 450 | 2 MB |
| patterns (11 entries + mantle; `k/<t>` busy-tick files) | ≈ 650 | 3 MB |
| kit (fx engine + ~30 presets + ~60 sound recipes + HUD) | ≈ 330 | 1.5 MB |
| arena `tk_lift` (+ `mboss/ar/tk_lift`) | ≈ 90 + 17 | 1 MB |
| framework `mboss/sp` + tests + aliases, rift `room/rift` | ≈ 60 + 80 | 0.3 MB |
| **total** | **≈ 2,980** (no px proxies: −2,000 vs Apep) | **≈ 15 MB** |
Texture: rig 0.52 M (40 parts at 32 px/b, face / visor 64 px/b), kit 0.18 M (crescents 2×128×32, slash arcs 5×128×64,
spin ring 128², lightning 7×32×64/128, shock ring 128², glints, feathers, cocoon 64², embers; generic glows reused from
the fg kit), rift 0.03 M, gate icon 0.004 M → **≈ 0.73 M px** (items atlas 11.7 → ≈ 12.45 M of ~15.5 M).

### 9.7 Order of work and hand-offs
D0 → (S1 ∥ S1K) and (S2 ∥ S3) and S4 (2 agents per workflow) → I1 → reviews (state, fairness S5, fidelity) → F → V →
release (stamp "타키 · 균열", README, zips). S3/S4 develop on the D0 stub manifest and kit stubs; S1 tests with
`spproto` on `cp_test`; S2 delivers the manifest before I1 (core regenerates nothing for px since `px:false`).

---------------------------------------------------------------------------------------------------------------------

## 10. Reference sheets (all in `TK/ref/`)
- Intro: `intro_v1_overview_a.jpg`, `intro_v1_overview_b.jpg`, `intro_v2_overview_a.jpg`, `intro_v2_overview_b.jpg`,
  `intro_v2_0-9s.jpg`, `intro_v2_9-18s.jpg`, `intro_v2_rise.jpg`, `intro_v2_sword.jpg`.
- Model: `model_a.jpg` (rise, cape, side, face + ring light, visor closing, skull glow, hex suit + yellow V, sword draw,
  ignite, helmet + hood, wings unfold, P2 wings); `fx_a.jpg` (scale vs player + one key frame per move).
- Patterns: `t_A1_v8.jpg`, `t_B1_v5.jpg`, `t_B2_v5.jpg`, `t_B2b_v5.jpg`, `t_B3_v5.jpg`, `t_B3b_v5.jpg`, `t_C1_v6_a.jpg`,
  `t_C1_v6_b.jpg`, `t_C2_v7.jpg`, `t_C3_v7_a.jpg`, `t_C3_v7_b.jpg`, `t_K_v4_a.jpg`, `t_K_v4_b.jpg`, `t_K_v6_c.jpg`,
  `t_W1_v3_a.jpg`, `t_W1_v3_b.jpg`, `t_W2_v3_a.jpg`, `t_W2_v3_b.jpg`, `t_W2_v4_c.jpg`, `t_L_v4_a.jpg`,
  `t_L_v4_impact.jpg`, `t_wings_v9.jpg` (T1), `t_phase_v10.jpg` (T2).
- Player-only effects (do not copy): `x_player_fx_v2.jpg`.
- Tools that made them: `TK/tools/sheet.py` (interval contact sheet with timestamps, optional crop),
  `TK/tools/picks.py` (individually cropped frames).
