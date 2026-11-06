# 달빛 환영 나비 (title 달빛의 화신): pattern implementation specs

These are the stage-2 specs for the second mid-boss. Each file is one pattern or sequence. It gives:
- the per-tick timeline aligned to the rig clip and its events;
- the AI (bands, approach, facing, aim lock);
- telegraphs ≥ 10 t;
- the exact damage shapes, groups, caps, knockback, element and coefficient;
- projectiles;
- fx and sound per tick;
- the dodge window at the plaza arena;
- an ASCII diagram and an implementation sketch against the stage-1 API.

Every place where `plan.md` disagrees with the footage is flagged in the file's §1, with a proposed fix.

The binding design is `mb2/plan.md`. The research is in `mb2/understand/v1..v4.md`, `model.md` and `mb2/code/reuse.md`.

Against what these specs were written:
- stage-1 API and stubs: `wt_core` `tools/mboss_butterfly/{api,core,human,wing,cards}.py` and `mboss_lib.py`;
- the in-progress rig manifest: `wt_rig` `tools/mboss_butterfly_rig_manifest.json`.

I re-checked these key frames myself:
- v1 `sheet_jumpkick_b` (H2 disc timing);
- v2 `sheet_transform_crop` (ring timing) and `sheet_wingstrike` (B1 swoop);
- v3 `k_crescents_a`, `sheet_orb1_replay`, `sheet_flap_pf_12.85-13.70`;
- v4 `sheet_REPLAY_wrap_explode`.

## 0. Index

| file | id | name | clip (len) | owner |
|---|---|---|---|---|
| [H1_kick_combo.md](H1_kick_combo.md) | 1 | 달빛 발차기 | `kick_combo` (51) | `human.py` |
| [H2_kick_jump.md](H2_kick_jump.md) | 2 | 달빛 점프 | `kick_jump` (65) | `human.py` |
| [H3_dash_kick.md](H3_dash_kick.md) | 3 | 달빛 돌진 | `dash_kick` (50) | `human.py` |
| [H4_vacuum.md](H4_vacuum.md) | 4 | 광폭한 진공 | `vacuum` (41) | `human.py` |
| [B1_wing_strike.md](B1_wing_strike.md) | 11 | 우아한 날개 / 날개 치기 | `wing_strike` (55) | `wing.py` |
| [B2_wing_barrage.md](B2_wing_barrage.md) | 12 | 화염 날개의 습격 / 날개탄 | `wing_barrage` (117) | `wing.py` |
| [B3_flap_dive.md](B3_flap_dive.md) | 13 | 날개 휩쓸개 / 날갯짓 | `flap_dive` (59) | `wing.py` |
| [B4_coco.md](B4_coco.md) | 14 | 달빛 축복 / 2단 코코볼 | `coco` (76, + orbs to 98) | `wing.py` |
| [B5_release.md](B5_release.md) | 15 | 달빛 해제 / 강화 해제 | `release` (96) | `wing.py` (fx, hazard) + core (`svc`) |
| [S1_entrance.md](S1_entrance.md) | — | entrance (cocoon) | `entrance` (106) | core `intro/*` |
| [S2_transform_debuff.md](S2_transform_debuff.md) | 20 | transformation + 달빛 고치 | `transform` (30) | core |
| [S3_revert_groggy_reform.md](S3_revert_groggy_reform.md) | — | revert, groggy 300 t, turn, chain re-form | `release` tail, `groggy_h`, `turn_h`, `chain_reform`, `revert` | core |
| [S4_death.md](S4_death.md) | — | death | `death` (100) | core |
| [S5_cure_fx.md](S5_cure_fx.md) | — | 달빛 고치 cure fx + reward | — (20 t at the player) | core |
| [S6_element_switch.md](S6_element_switch.md) | — | wing element switch | looks `dendro` / `pyro` / `flat` | core `look/switch` |

## 1. Conventions

### 1.1 Notation used in every file

- **Points.**
  - `S` = her body on the floor (the hitbox husk; the rig follows it; it stays on the floor in butterfly form too).
  - `P` = the player's feet (`@e[tag=rlk_body]`).
  - `C` = the arena centre (200, 201, 8).
- **Markers.** `A`, `B`, `D`, `H`, `L`, `R`, `G` = pattern markers.
  - `g.dest(max, keep)`: on the line to the player, ≤ max from her, keep short of the player, inside the safe disc.
  - `g.lockp()`: on the floor under the player.
  - `g.keep(tag)`: renames the marker so the next call does not replace it.
- **Body frame.** `^x ^y ^z` executed `at @s rotated as @s rotated ~ 0` (the body's yaw).
  - x = her **left**, y = up, z = forward.
  - "Her right" = `^-x`.
- **Rig anchors** (manifest `clips[].anchors[event]`) are rig coordinates (x her left, y up, **-z forward**), so the body-frame position is `^x ^y ^-z`.
  - The anchors are foot_l/r, fwtip_l/r, hwtip_l/r, core, head, hand_r_a and hand_l_a.
  - Names like `foot_r@hit1` mean that anchor at that event.
  - Read them from the manifest at build time (Q3); the numbers quoted in the specs are today's.
- **Tinted card:** `tc:kind #RRGGBB s0→s1 l<life>/f<fade> [bb …] [rot …] [roll …] [spin …] [move …] at <pos>` was the
  stage-1 `g.tcard` (`cards.py`, cap 40). **Integration (wip/bf): that engine is removed; the fx kit is the engine**
  (`bf_fx_api.md`). Read a `tc:` line as a kit card `g.kcard(<kit kind>, pos, rot, bb=, roll=, spin=, s0=, s1=, move=,
  life=, fade=, col='#RRGGBB')` with the kind mapped: star → `glint` (tinted) or `star4` (painted lime flare), burst →
  `burst` (painted lime-white) or `glow`, ring → `ripple`, glow → `glow`, orb → `sphere`, slash → `streak`, crescent →
  `cres_lime` / `cres_cyan` / `cres_fire` (painted, keep `col` white), moon → `cres_lime` (or the `vblade` prop look),
  shard → `shard`, leaf → `leaf`, flame → `flame_tongue` / `flame_puff`, swirl → the `coc_apply` preset. Painted kinds
  keep the video colours under white; only the neutral ones (`glint glow mote streak leaf bfly ripple`) take the hex.
  First look for the matching kit preset (`bf_fx_api.md` §7 / §9 maps every event of these specs to one).
  - `rot ~ 90` lays a face card flat on the floor.
  - `roll 90` stands the flat `crescent` card in her sagittal plane.
- **Gold card:** `g.card(kind, …)` (Navia's engine, gold only, cap 48 shared with Navia). Used only for the cure fx.
- **Sound:** `event v/p` = `g.sound(event, v, p)` = one `playsound … hostile @a[tag=player] ~ ~ ~ v p minVol`, with minVol from `L.min_volume`. Vanilla only.
- **dust:** `dust #hex scale ×n Δ(dx,dy,dz)` = `g.dust(rgb, scale, pos, delta, n)`.

### 1.2 Hazards, projectiles and groups (framework)

- `hz_disc(r, tell, dmg)`, `hz_ring`, `hz_sector(r, half_angle, …)`, `hz_line(len, width, …)` (option `back`) and `hz_full` are called positioned on the floor, rotated = aim.
  - `tell` = ticks until the strike.
  - `dmg` = % of the base hit (`atk 12 × dmgMul 110`).
  - Defaults: height -0.5..3.5 (`y0` / `y1`), act 1, KB 3.
- **Set `hz_opts(sfx=0)` on every butterfly hazard.** The composed sounds replace the framework strike sfx (Q7).
- `tell_line` = a telegraph-only line (dmg 0, never a hit).
- **Volley group:** `g.GRP_NEW` then `grp=True` on every hazard or projectile of the group. The first hit makes the rest harmless.
- `pj_launch(spd, life, dmg, hr)`:
  - the speed is **rounded up to whole 0.25 b sub-steps**: spd 0.25 → 0.25 b/t; 0.3-0.5 → 0.5 b/t; 0.7 → 0.75 b/t;
  - the hit test is 0.9 b below the prop;
  - shape 1 = blade (2 rows; a jump does not dodge it);
  - `pj_steer(max°)` = homing.
- Coefficient scale: **1.0 is about 11 % of an item-less player's max HP** (reuse.md §7.2). The boss uses no element RES at all (user decision): nothing in these specs touches `mres` or `#elem` reductions.

### 1.3 Player kinematics (for the dodge windows)

| move | value |
|---|---|
| walk | 0.22 b/t (movement_speed 0.1) |
| sprint | 0.28 b/t |
| jump | apex 1.25 b; feet ≥ 1.0 b on ticks +3..+8 after the press |
| dash | 3 b in 3 t; **6 t of i-frames from the press** (`dashInvT 6`); 2 charges, 1 regen per 20 t, 5 t self cooldown |
| body hit radius | about 0.3 b (the framework adds 0.3 to every test) |

### 1.4 Arena (plaza, registry `arena`)

- Centre (200, 201, 8).
- Walkable r 21, safe r 19. The boss `mv/ok` keeps the body within r 18.5; `mv/clamp` also pulls markers to 18.5.
- Wall ring r 21-22, y 201-207 (solid).
- Barrier cap only over the wall ring, y 208-215.
- Light layer at y 206 over the disc (light blocks: no collision, no effect on displays).
- The player enters from (200.5, 201, 25.5), 17.5 b south of the centre.

### 1.5 Card size cheat sheet (stage-1 `cards.py` sprites; s = card size)

| kind | plane | what s means | for radius / length R |
|---|---|---|---|
| `glow`, `orb`, `burst`, `star` | face | diameter 1 b at s 1 | s = 2R |
| `ring` | face | ring radius 0.43 b at s 1 | **s = 2.33 R** (r 3 → 7.0, r 4 → 9.3, r 5 → 11.6, r 10 → 23.3) |
| `crescent` | flat (XZ) | outer radius 0.5 at s 1, a 160° arc, inner radius 0.45·outer | s = 2R |
| `slash` | face | length 1 b, thickness 0.125 b at s 1 | s = L |
| `shard` | face, pivot at the root | 0.25 × 1 b | s = height |
| `flame` | face, pivot at the base | 0.5 × 1 b | s = height |
| `leaf` | face | 0.5 × 1 b | s = length |
| `moon`, `swirl` | face | 1 b | s = diameter |

### 1.6 Telegraph conventions (all patterns)

- **≥ 10 t** from the decal to the strike for every damaging hit. The shortest in these specs is 10 t (H1 hit 1, H2 sweep, B3 trail, B4 burst; H4 at 4 b is 11 t); most are 12-22 t.
- **Outline:** the framework (element colour `HZ_COLOURS`, every 4 t).
- **Fill:** the kit decal grows from 0 to the full shape at the strike tick (a "progress" read).
  - Dendro: fill `#B6E35A`, rim `#E5FBC8`.
  - Pyro: fill `#FF8A3D`, rim `#FAD77C`, inner edge `#C680A2`.
- **Tell cue:** a soft sound at the decal's first tick.
  - Dendro: `block.amethyst_block.resonate` 0.35/1.6.
  - Pyro: `item.firecharge.use` 0.35/1.6.
  - B5 adds its big charge layers.
- **Aim lock = decal start.** No pattern re-aims after its decal appears (B4's orbs home by design; they carry their own telegraph).

## 2. Global timing and coefficient table

Ticks are pattern clock = clip tick. Telegraph windows are decal → strike.

| id | pattern | clip, len | form / el | bands (weight) | approach | aim lock | telegraph → strike | shape(s) | coef | KB | cap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H1 달빛 발차기 | kick_combo 51, lead 2 | H / Dendro | melee 2, mid 1 | the clip's own run ≤ 4.5 b | A t-2; B t26 | -2→**8** (10); 26→**40** (14) | lane 4.5×2.4 (back 0.5) + disc r 1.5 @1.2 ahead · sector r 5 ±90° + line 6×2 | 1.0 · 1.2 | 3 | 2 hits (2.2) |
| 2 | H2 달빛 점프 | kick_jump 65 | H / Dendro | melee 1, mid 1 | burst-run to 3 b | sweep: self, t3; L t43 | 3→**13** (10, act 4, y ≤ 1.0); 43→**55** (12) | disc r 3 at S · disc r 2.5 at L | 0.9 · 1.4 | 3 · 4 | 2 hits (2.3) |
| 3 | H3 달빛 돌진 | dash_kick 50 | H / Dendro | mid 1, far 2 | — (it is the dash) | D t3 | 3→**15** (12); 3→**19** (16, act 3) | disc r 1.5 @D+1.2 + disc r 3.5 @D (one group) | 1.3 | 3 | 1 |
| 4 | H4 광폭한 진공 | vacuum 41 | H / Dendro | mid 1, far 2 | — | yaw t9 | 9→launch **17**; arrival ≈ t20 at 4 b (11 t), t26 at 8 b (17 t) | pj blade 3 b wide × 4 tall, 0.75 b/t, 60 t, no homing | 1.2 | 3 | 1 |
| 11 | B1 우아한 날개 | wing_strike 55 | B / Dendro | melee 2, mid 1 | idle glide | L, H t3 | 3→**15** (12) | lane 10×3.5 from S + sector r 4 ±60° at L (one group) | 1.3 | 3 | 1 |
| 12 | B2 화염 날개의 습격 | wing_barrage 117 (swings **5/31/69/94**) | B / **Pyro** | mid 1, far 2 | prep backs to ≥ 6 b | L_s at each swing | s→**s+14..18** (14-18) | 5 × disc r 1.2 (cross row / long row, 1.8 spacing) | 0.5 each | 2 | 1 per swing (≤ 2.0) |
| 13 | B3 날개 휩쓸개 | flap_dive 59 | B / **Pyro** | melee 1, mid 2 | prep ≥ 6 b | P t16 | 16→**28** (12, act 5); trail +10 | sector r 4.5 ±90°, y ≤ 2.5 · 4 × disc r 1.0 (act 8) | 1.6 · 0.3 | 3 · 0 | 1 + 2 (2.2) |
| 14 | B4 달빛 축복 | coco 76 (end 98) | B / Dendro | mid 1, far 1 | glide 1.5 b; the ball drifts | — (homing) | charge t5→contact ≥ t26 (21); ball open t42→contact ≥ t53 (11); burst 10 | pj sphere r 1.1 (0.25 b/t, steer 9°/t, 40 t) / disc r 2.8 | 1.5 each | 2 · 3 | 1 per orb (≤ 3.0) |
| 15 | B5 달빛 해제 | release 96 | B → H / Dendro | service | swoop S → R | R t0 | 31→**53** (22) | disc r 10 at R | 2.6 | 4 radial | 1 |
| 20 | transformation | transform 30 | H → B | service | — | — | sheath t0 → t6 | 달빛 고치: 20 % current HP, non-lethal, unavoidable | — | — | — |

Rotation (core, plan):
- **Human:** shuffle bag by band (melee ≤ 4 b, mid 4-8, far ≥ 8), no immediate repeat, recover 16-18 t. Transformation after 600 t or 5 patterns the first time, then after 4 patterns.
- **Butterfly:** bag; the look switch happens 8 t before a pattern of the other element; 달빛 해제 after 4-5 patterns or 900 t.
- **Groggy** 300 t, then the turn 24 t and the chain 18 t, then H2 forced.

## 3. Rig clip events: plan / rig vs footage

Proposed changes for the rig author (Q2). Event names are the contract the modules read with `ev()` / `ev_or()`.

| clip | event | rig now | footage | proposed | why |
|---|---|---|---|---|---|
| `kick_combo` | hit1 / hit2 | 8 / 40 | 6 / 37.5 | keep | consistent +2 for a readable chamber |
| `kick_jump` | disc | 40 | orb 45, kick-down 53 | **orb 45, kick 52** | the disc impact is 5 t later in the footage |
| `kick_jump` | impact | (missing; stub fallback 50) | **55-56** (v1), 54 (v4) | **impact 55** | |
| `kick_jump` | land | 55 | 59.7 | **59** | |
| `kick_jump` | sweep_end | (missing; fallback 19) | 19 | add 19 (or act 4 from 13) | |
| `dash_kick` | dash_end, ring | (missing) | 12, **18.6-22** | **dash_end 12, ring 19** | the ring follows the kick by 4 t |
| `vacuum` | stomp | (missing) | 16-17 | **stomp 16** | fx hook |
| `wing_barrage` | swing1..4 | 0/26/64/89 | wind-up 5 t before swing 1 | **5/31/69/94** | the wind-up inside the clip; last landing 112 < 117 |
| `transform` | ripple → **rings** | ripple 14 | **9-11** | **rings 9** | the core reads `rings` (fallback 8); the footage rings at 9-11 |
| `release` | flash / glint / rings | 41 / 42 / 43 | **35 / 37 / 38** (E-18 / -16 / -15) | **35 / 37 / 38** | |
| `release` | shrink / flat / shatter | 82 / 84 / 88 | **87 / 87 / 91** (E+34 / +34 / +38) | **87 / 87 / 91** | the core's `look/flat` follows `flat` |
| `chain_reform` | start | after `turn_h` | turn +17 | optional overlap | S3 |
| others | — | — | — | ok | entrance, flap_dive, coco, wing_strike, revert, death match |

**Root travel (Q1).** These clips bake horizontal root offsets that the module also performs:
- `kick_combo` (z +1.2 → -0.4);
- `vacuum` (+2.6);
- `wing_strike` (-2.6);
- `flap_dive` (-6);
- `release` (-4).

## 4. FX list (for the fx-kit agent and the authors)

### 4.1 Tinted card kinds already in stage-1 `cards.py`, and what the specs use them for

| kind | uses | main colours |
|---|---|---|
| `star` | glints, the cure star, the release flare, sparkles | `#FFFFFF` `#E5FBC8` `#EEFDCF` `#FBFDF4` `#FAFCD4` |
| `burst` | impacts, the cocoon burst, the dome flash | Dendro `#EDF9DA` `#E7FDAA` `#EAFDD9` `#A6E282`; Pyro `#F9E38E` `#F7CC9C`; white `#FDFDFB` `#F9FDFC` |
| `ring` | ripple rings, wind crescents, the ring cage, floor rings, big decal outline | `#BDE592` `#D0F2B9` `#428B71` `#ADE87F` `#B6FC9D` `#7AFA88` `#D0F0C0` `#E1F0A0` `#FFFFFF` |
| `glow` | floor glows, cores, the sheath, element-switch flash, ember glow | `#81C4AB` `#B5F089` `#D2FA8E` `#DFF99C` `#FAD77C` `#E26E50` `#8C525C` `#EDC30B` |
| `orb` | the light sphere, the dome (fallback), the H2 orb | `#F8FDBB` `#87F155` `#5CD63D` `#F8FDDA` `#C1F788` |
| `slash` | streaks, the X glint, god rays, floor slash bands, tendrils, the trail line, the cure beam | `#E7FDAA` `#8DEAF0` `#9FD57F` `#77CE3E` `#F0FEF6` `#E04040` `#F4EDC9` |
| `crescent` | kick crescents, the sweep band, wing arcs, flame sheets, the ring slash | Dendro `#C1F788` `#D7F899` `#D6FAC5` `#B6F392` `#D4FA88`, with underlays `#297272` `#3A765D` `#2C898F` `#23717A`; Pyro `#F8D486` / `#CC6976` `#F09A5F` |
| `moon` | the cocoon-burst wing outline, the H2 floor mark | `#C8F060` `#B9E4A7` |
| `shard` | blade shards, crystal shards, ground blades (fallback) | `#A8DF74` `#74E542` `#BAF3E3` `#E7FD7A` `#394B75` |
| `leaf` | drifting leaves, amber petals | `#A8DF74` `#ADDE6D` `#B4EB68` `#E2BF5F` |
| `flame` | flame spike (H4 tell), fire streaks, fan spikes (fallback), crescent prop (fallback) | `#C9F2AD` `#F8D486` `#F06A30` |
| `swirl` | the foot swirl, spiral ribbons, the ball, the debuff swirl | `#D7F899` `#AADB84` `#CCF39C` `#E8858A` |

### 4.2 New kit items requested

| item | for | description |
|---|---|---|
| `vblade` (model) | H4 | a vertical crescent wall 3 b across × 4 b tall, face ⟂ flight; leaf-blade spikes on the edge; core `#1E545F`, body `#A9E97D`→`#64BC56`, rim `#D6F7B9`; used on an `item_display` `pj` prop with non-uniform scale |
| `feather` (tinted) | B2 | a fire-crescent claw 1.2 b with a 1-2 b flame tail, oriented along its flight; core `#F8F2B8`, mid `#F8D486`, edges `#DE9884` / `#CC6976` |
| `spike` (tinted) | B3 | a tall flame shard, pivot at the base (the eruption fan) |
| `blade` / `vmark` (tinted) | B4 burst (and the H1 wave) | a V-shaped ground blade (radial burst) and its flat floor mark for the burst decal |
| `butterfly` (tinted) | B5 | a small butterfly outline glyph (0.6 b), `#B8E04C` |
| `emblem` (tinted) | S5 | a crown / fleur-de-lis glyph with a star on top, `#D5DD81` |
| `dome` (3D model) | B5 | a translucent sphere shell, faces inward and outward, alpha 0.3-0.5, brighter rim; 2-3 fading variants swapped every 2 t; scaled 11 → 21 b over 2 t |
| decals | all hazards | Dendro and Pyro tinted floor decals with progress fill: **disc** (r 1-10), **ring** outline (r up to 10.5), **sector** (half-angles 60 / 90), **lane** (len up to 30, width 0.8-3.5, chevrons), **ember line** (B3 trail). Cheap enough for 5 concurrent (B2). |
| screen overlays | B5 (and S1 whiteout optionally) | a full-screen **white** flash (2 t) and a **lime tint** (10 t, fading) as title-font glyphs (Guardian `guardian_screen.mjs` technique, font `rlk:mboss_bf` U+E600..) |
| HUD glyphs | S2, S5 | the 달빛 고치 badge (maroon `#8C525C` disc, salmon `#D06A60` rim, `#E8858A` swirl) and the reward star (gold `#F4E28A`) for the boss-bar name line |

### 4.3 Palette

| group | colours |
|---|---|
| Dendro core / bright / mid / edge / dark | `#EDF9DA` `#E5FBC8` / `#D7F899` `#C1F788` / `#BFF191` `#AEE08B` / `#8DCA85` / `#297272` `#3A765D` |
| lime accent (registry colour) | `#B6E35A` |
| opal / cyan / white-cyan | `#D4F8C6` / `#8DEAF0` `#39B4C1` / `#BAF3E3` `#F9FDFC` |
| Pyro | `#FAD77C` `#F8D486` `#F8F2B8` → `#DE9884` `#CC6976` → magenta `#C680A2`; orange `#FF8A3D` `#F88F39`; scorch `#585542`, ember `#EDC30B` |
| release dome | `#87F155` `#5CD63D` `#C2F999` `#F8FDDA`; rim `#B6FC9D` `#7AFA88` |
| gold (cure) | `#F4EDC9` `#FFF8F3` `#E0DD9C` `#D5DD81` |
| debuff | `#8C525C` `#E8858A` `#D06A60` |

### 4.4 Vanilla particles used

All are already used in the pack:
- `dust`, `dust_color_transition`;
- `end_rod`, `wax_on`, `wax_off`;
- `flame`, `small_flame`, `lava`;
- `poof`, `composter`, `sweep_attack`;
- `flash{color:[r,g,b,a]}`, `explosion_emitter`, `campfire_cosy_smoke`;
- `block{block_state:…}` (moss_block, mossy_cobblestone, white / light_blue / lime stained glass).

### 4.5 Budget

- Tinted cards ≤ 40 live (stage-1 cap). The worst cases are B2 (about 19) and B5 at E (about 15).
- `pj` / module props ≤ 16: B2 5 + markers, B4 2, H4 1.
- Particles ≤ about 60 per tick (B5 at E is the peak).

## 5. Sound list (vanilla)

Events and where they are used. Volumes are 0.25-1.0, pitches 0.6-2.0, ≤ 4 layers on one tick. **NEW** = not yet used anywhere in the pack: these are vanilla 1.20 / 1.21 events, but verify them once in 26.3.

| event | used in | typical v/p |
|---|---|---|
| `block.amethyst_block.chime` | H1 H2 H3 B4 S1 S3 S4 S5 | 0.3-1.0 / 1.3-2.0 |
| `block.amethyst_block.resonate` (the Dendro tell cue) | all Dendro telegraphs, S1 S2 S4 S5 S6 | 0.35-0.8 / 0.7-1.6 |
| `block.amethyst_block.break` / `.place` | S4 / S3 | 0.6 / 0.9; 0.7 / 1.2 |
| `block.amethyst_cluster.break` / `.hit` | H4 B5 S1 S3 S4 / H2 H4 B5 | 0.6-1.0 / 0.8-1.5; 0.45-0.8 / 1.8-1.9 |
| `block.azalea.break`, `block.azalea_leaves.break` / `.place` | H1 H3 / H1-4 B1 B4 B5 / S6 | 0.4-0.8 / 0.9-1.7 |
| `block.beacon.activate` / `.ambient` / `.deactivate` / `.power_select` | B5 S1 S2 S5 / H2 B4 S1 S3 S5 / B5 S3 S4 / B4 B5 S1 S2 | 0.25-0.8 / 0.8-2.0 |
| `block.big_dripleaf.tilt_down` | H1 H4 | 0.6 / 1.0-1.2 |
| **NEW** `block.big_dripleaf.break` | H1 B4 | 0.6 / 1.0 |
| `block.chain.place` | S3 | 0.8 / 0.8 |
| **NEW** `block.cherry_leaves.break` | H3 B1 | 0.5-0.8 / 1.0-1.2 |
| `block.conduit.activate` | H2 B4 B5 | 0.4-0.5 / 1.4-1.8 |
| `block.fire.ambient` / `.extinguish` | B2 B3 / B2 | 0.4-0.9 / 0.8-1.6 |
| `block.glass.break` | B5 S1 S3 S4 | 0.4-0.8 / 1.2-1.6 |
| **NEW** `block.grass.break` | H4 (blade travel) | 0.5 / 1.0 |
| `block.moss.break` / `.place` | H2 / B4 | 0.6 / 0.9-1.0 |
| **NEW** `block.moss.fall` | H1 H2 H4 B5 S1 S3 S4 (landings) | 0.35-0.9 / 0.8-1.2 |
| **NEW** `block.moss_carpet.step` | H1 H4 (steps) | 0.4-0.5 / 0.9-1.2 |
| `block.note_block.chime` | H4 | 0.35 / 2.0 |
| `block.respawn_anchor.charge` / `.deplete` / `.set_spawn` | B5 S1 S2 / S3 / S6 | 0.3-0.7 / 1.2-1.8 |
| **NEW** `entity.allay.item_thrown` | B4 | 0.5 / 0.8 |
| `entity.blaze.burn` / `.shoot` | B2 B3 | 0.3-0.9 / 0.8-1.2 |
| `entity.breeze.charge` / `.jump` / `.land` / `.shoot` / `.wind_burst` | H2 H3 / H1 H3 H4 / H4 / H2 B4 / H1-4 B1 B4 B5 S1 S2 | 0.4-1.0 / 0.6-1.4 |
| **NEW** `entity.breeze.idle_air` / `entity.breeze.whirl` | H2 H4 B5 S3 / H2 B4 B5 | 0.3-0.6 / 0.6-1.5 |
| `entity.elder_guardian.curse` | S2 | 0.35-0.4 / 1.6-1.7 |
| `entity.ender_dragon.flap` | B1-B5 S2 S3 | 0.4-0.8 / 0.9-1.8 |
| `entity.firework_rocket.blast` / `.twinkle` | B2 / H2 S5 | 0.4-0.6 / 0.8-1.4 |
| `entity.generic.explode` | H2 B3 B4 B5 | 0.3-1.0 / 0.7-1.6 |
| **NEW** `entity.generic.burn` | B2 B3 | 0.3-0.6 / 1.2-1.4 |
| **NEW** `entity.ghast.shoot` | B2 B3 | 0.4-0.5 / 1.2 |
| `entity.illusioner.mirror_move` | B5 S3 S4 | 0.5-0.6 / 1.4 |
| `entity.iron_golem.step` | H1 B5 S1 S3 S4 | 0.3-0.4 / 1.4 |
| `entity.phantom.flap` / `.swoop` | B1 B3 S2 / H4 B1 B3 B5 | 0.3-0.7 / 1.0-1.6 |
| `entity.player.attack.sweep` / `.strong` / `entity.player.levelup` | H1-3 B1 B2 B5 / H3 / S5 | 0.25-0.8 / 0.7-1.6 |
| `entity.warden.sonic_charge` / `.sonic_boom` | B5 | 0.5-0.6 / 1.4-1.8 |
| `item.elytra.flying`, `item.firecharge.use` (the Pyro tell cue), `item.mace.smash_ground`, `item.totem.use`, `item.trident.riptide_1` / `_2` | H2; B2 B3 S6; H3; S2; H1-4 B1 B2 | 0.2-0.8 / 0.8-1.6 |

## 6. Open questions, with a recommended answer

**Q1. Root travel: the rig bakes horizontal motion that the module also performs (double travel).**
- The rig WIP bakes forward/back root offsets in `kick_combo`, `vacuum`, `wing_strike`, `flap_dive` and `release` (§3).
- The stage-1 stubs also move the body (`mv/glide`, `mv/away`). She would travel twice, and at clip end the root snaps back from its offset to the anchor.
- **Recommended:** follow the Guardian contract (`mboss_guardian_rig_api.md` §4).
  - Clips carry height, leans and limbs only.
  - Horizontal root XZ stays ≤ 0.5 b inside a clip and is 0 at its last key.
  - The module moves the body along the travel tables in each spec (§3 of the H and B files).
  - The hitbox then follows the visual.

**Q2. Event retimes and names (§3).**
- **Recommended:** the rig author applies the table in §3 (`kick_jump` orb / kick / impact / land, `dash_kick` ring, `vacuum` stomp, `wing_barrage` +5, `transform` `rings` 9, `release` 35/37/38 and 87/87/91).
- The pattern code reads them with `ev_or(…, default = the proposed value)`, so either side can land first.

**Q3. Anchor helper.** Spawn points use manifest anchors (foot_r@disc, fwtip@swing, core@orb1, …).
- **Recommended:** add `A.anchor(clip, event, part) → '^x ^y ^-z'` to `api.py`, reading `clips[].anchors`. Specs then never hard-code rig numbers.
- If an anchor is missing, fall back to the body-frame points given in the specs.

**Q4. H1 hit 1 shape.**
- The plan says "front arc r about 4". The footage shows a narrow vertical crescent: a strip about 1.5 m wide, 0.5-3 m ahead, plus an r 1.5 splash.
- **Recommended:** a lane 4.5 × 2.4 (back 0.5) + a disc r 1.5 in one group. It is faithful, and it gives the combo two different reads (narrow, then wide).

**Q5. B5 telegraph and placement.**
- The stub's r 10 decal starts at E-15, which is too short to walk out of r 10 from 4 b.
- **Recommended:**
  - the decal from the cup, E-22 (t31);
  - the release point R = player + 4 b outward from the centre, clamped to ≤ 16 b from the centre, so the escape is toward open floor;
  - the universal answer is the dash at t48-53.

**Q6. Butterfly bands.** The plan's table has none.
- **Recommended:** B1 melee 2 / mid 1; B2 mid 1 / far 2; B3 melee 1 / mid 2; B4 mid 1 / far 1.
- B1 and B3 are not picked in the far band: their dive covers ≤ 7-8 b.
- The stub has B1 and B3 in all three bands.

**Q7. Framework strike sfx.**
- **Recommended:** `sfx=0` on every butterfly hazard, with all sounds composed per spec. The framework's explode/anvil/golem layers do not fit the moonlight palette and would double the impacts.

**Q8. Lock clamp radius.**
- `u/lockp` and `mv/clamp` pull ground targets inside the boss safe disc (r 18.5).
- A player hugging the wall (r 18.5-21) then stands up to 2.5 b outside every locked hazard: H2 disc, B1, B2 rows, B3, B5 R.
- **Recommended:** a `u/lockw` (or a clamp radius argument) that clamps **ground-hazard targets** to the walk disc (`@WALKP@` = 20.3). Keep r 18.5 for points the body moves to (`u/dest`).

**Q9. Butterfly hover clamp and arena height.**
- The wings span about 9.3 b. With the body allowed out to r 18.5, the wing tips reach r 23 and clip into the 7-high wall ring.
- **Recommended:** in butterfly form, clamp her body (idle glide, `dest`, B5 R) to **r ≤ 16.5**: a core `u/dest` radius argument plus a leash at 16.5.
- Heights are fine:
  - hovering wing tops 6.4 b (rig anchors);
  - `flap_dive` dive pose to about 10 b;
  - displays ignore the barrier cap (which only sits over the wall ring) and the light layer.

**Q10. B4 orbs.**
- The footage orbs burst after about 8-10 t (the player stood close). The plan says "home about 40 t then burst".
- **Recommended:**
  - keep the plan: 0.25 b/t (pj spd 2: the stub's 0.35 actually flies at 0.5 b/t), steer 9°/t;
  - `pj` life 40, then a still prop with an r 2.8 burst 10 t later in the same group;
  - contact pops it.

**Q11. B3 flame-trail damage** (unconfirmed in the footage).
- **Recommended:** keep the plan (0.3 per touch, max 2, KB 0), with a 10 t ember telegraph and act 8. It punishes walking through her glide line and seeds Burning combos.

**Q12. H2 sweep jumpable?**
- **Recommended: yes.** `y1 1.0`, act 4. It is knee height in both videos; the jump window is t8-t10 and the dash t11-t13. The 10 t decal stays for players who just walk out.

**Q13. H4 in the melee band?** The plan says far and mid only.
- **Recommended:** keep the plan. Below 3.5 b the blade would arrive < 10 t after the glint. A melee variant needs the lock at t7 and the launch at t19.

**Q14. Projectiles that outlive their pattern** (the H4 blade after t41, B4 orbs to t98).
- **Recommended:**
  - B4 ends at t98 (`B4_END`), so its orbs live inside the pattern.
  - For the H4 blade, run its per-tick fx from a core "live props" check (`execute if entity @e[tag=rlk_mb_bf_p4b]` → `p/vacuum/blade_tick`) in the module tick, so it keeps its trail after `g.end()`.
  - The framework `pj` moves it either way.

**Q15. B2 flame sheets.**
- **Recommended:** cosmetic only (no hazard). The plan gives damage only to the crescents (0.5, one per swing). A 4.5 b sheet hit would make B2 unfair at mid range.

**Q16. Turn and chain re-form overlap.**
- **Recommended:** optional. Start `chain_reform` at turn +17 (as in the footage, 35 t total). Keep the core's sequential 42 t if the rig cannot blend the clips.

**Q17. Sounds not yet in the pack** (§5 NEW).
- **Recommended:** keep them (all vanilla 1.20 / 1.21). The first in-game check confirms they still exist in 26.3; the fallbacks are `block.azalea_leaves.break` (for the leaves / grass ones), `block.moss.break` (for `moss.fall` / `moss_carpet.step`), `entity.breeze.wind_burst` (for `breeze.whirl` / `idle_air`), `entity.blaze.shoot` (for `ghast.shoot`) and `block.fire.ambient` (for `generic.burn`).

**Q18. The card cap is shared with decals.** If the kit's decals are tinted cards too, B2 (5 decals + its fx) and B5 approach 40.
- **Recommended:**
  - decals on their own cap / tag (or particle-drawn);
  - drop the ember-glow cards first when the cap is reached;
  - the `tc/card` skip-on-cap is already silent.

**Q19. Debuff timing.** The footage HP drop comes at t8 (2 t after the sphere).
- **Recommended:** keep the plan's t6 (the core). It is unavoidable and non-lethal by design.

**Q20. The transformation in the footage starts airborne**, straight out of a 광폭한 진공 backflip.
- **Recommended:** keep it grounded at a pattern boundary (the core). Simpler, and the clip already lifts her into the hover.

**Q21. Entrance shimmer audio.**
- **Recommended:** a soft `respawn_anchor.charge` at the glow (61), and the main rising layers at 69, as in the footage onset (3.48 s).

**Q22. H1 kick-2 direction.** The footage fixes it at the wind-up start (about t20), and it missed the player.
- **Recommended:** aim it at the player at t26 and hold it (14 t decal). It is a deliberate, readable attack rather than a random direction.
