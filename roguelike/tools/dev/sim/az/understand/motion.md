# 야타용왕 (Azhdaha): motion and skeleton study

What this file is for: the rig author and the clip author of the chapter-1 boss. It proposes a skeleton, records every
motion of the 9 reference clips as key poses in **20 tps ticks**, and proposes a clip list with lengths and event ticks
in the format of `tools/mboss_rig_clips.mjs`. The motion must read as **heavy**; §3 turns that into numbers.

Sources:

- the binding user notes `S:az/src/wiki.md`;
- the footage `S:az/src/v1..v9.mp4` (1920×1080, 60 fps, the 패턴분석 part of the HGOO guide);
- the clip conventions of `FG:tools/mboss_rig_clips.mjs`, `FG:tools/fieldgen_clips.mjs`, `tools/guardian_clips.mjs` and
  `FG:tools/mboss_rig_compile.mjs`;
- the arena proposal in `S:az/understand/chapter.md` §4 (Azhdaha arena walk radius **28 b**).

Path prefixes:

| prefix | path |
|---|---|
| `S:` | `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/` |
| `FG:` | `S:mb3/wt_fg/roguelike/` |
| `M/` | `S:az/understand/motion/` (the key-pose sheets) |

Conventions:

- `vN s` is a time in video N, in seconds.
- `t+N` is ticks at 20 tps from the stated zero (1 tick = 3 video frames).
- Every timing comes from a sheet in `M/` (index in §8). Each sheet labels each frame with its seconds and its tick
  offset.
- Rig frame, as in `mboss_rig_math.mjs`:
  - +X is the boss's left, +Y is up, −Z is forward;
  - units are blocks;
  - the origin is the floor point under the centre of the four feet;
  - pitch +X leans back (nose up), yaw +Y turns the boss to its right, roll +Z tips the top toward its right.

No video analyst write-up (`S:az/understand/v*.md`) existed when this was written. The timings below are my own reads of
the sheets. Where an analyst file later disagrees by a tick or two, prefer the one measured on more frames.

---

## 1. Size and proportions

I measured on `M/skel_side_v3.jpg`, a clean left-side profile at v3 10.6 s, and on `M/K_stomp_keys_v3.jpg` c, where the
player stands at the same depth as the front feet. In the second frame the player (1.8 b) is 0.35 of the boss's shoulder
height.

| item | ratio | proposal (b) |
|---|---|---|
| back height (skin, mid-back) | 2.9 × player | **5.2** (shoulder 5.0, hips 4.6) |
| top of the back spikes / crystal plates | 4.2 × player | **7.5-7.8** |
| nose to rump | 2.3 × back height | **12.5** |
| tail, root to tip | about the body length | **11.0** |
| length overall, tail laid out straight | | about 23 |
| fore feet | 6.4 b apart front to back from the hind feet | fore ±2.6 at z −3.2; hind ±2.3 at z +3.1 |
| head | snout 1.9 b above the floor, skull centre 2.6 | head (occiput to snout) 3.0, with the crown 4.3 wide |
| belly clearance | low-slung | belly at 1.6-1.9 b |

The head is carried **low**, below the back line. The neck slopes down and forward from the shoulders, so the snout is at
the player's chest. This is the main silhouette cue, together with the very thick columnar forelegs and the tail arched
high behind (the tip at spike height in phase 1 idle).

The model study (`S:az/understand/model*`) decides the final geometry. These numbers are the motion-relevant
proportions: joint heights, reach and the foot stance. If 23 b overall feels cramped in a 28-b walk-radius arena, scale
the whole rig uniformly (0.85 still reads as huge: back 4.4 b, spikes 6.5 b). Keep the ratios.

Pictures:

- `M/00_skeleton_proposal.jpg`: side, top and front views on a 1-b grid with the 1.8-b player;
- `M/00_skeleton_overlay_v3.jpg`: the near-side joints drawn over the footage profile.

---

## 2. Skeleton

### 2.1 Bones

The rest pose is the idle stance. Pivot coordinates are (x, y, z) in blocks. L bones have x > 0 and R bones mirror them.

| # | bone | parent | pivot (rest) | length | DOF / range | carries |
|---|---|---|---|---|---|---|
| 0 | `root` | anchor | (0, 0, 0) | | clip: `pos` [0, y, 0] and `rot` (pitch, roll); **no x/z, no yaw** (§4) | heights (jump, burrow −7.5), whole-body tilt |
| 1 | `pelvis` | root | (0, 3.7, 3.0), the hip-joint line | to spine1 2.4 | pitch −60…+70, yaw ±25, roll ±20 | **rear-ups pivot here** (chin slam, roar, landslide 6, tail slam lean); the hind half |
| 2 | `spine1` | pelvis | (0, 4.1, 0.7) | 2.2 | pitch ±20, yaw ±30, roll ±15 | the back hump (천동만상 brace); the charge coil (lateral C) |
| 3 | `chest` | spine1 | (0, 3.9, −1.5), the shoulder girdle | 1.5 | pitch ±25, yaw ±35, roll ±20 | fore-leg roots, the weight shift before a stomp |
| 4 | `neck1` | chest | (0, 3.7, −2.9) | 1.35 | pitch −45…+50, yaw ±35 | head lead in turns, chin-slam drive |
| 5 | `neck2` | neck1 | (0, 3.1, −4.1) | 1.2 | pitch −40…+50, yaw ±35 | the same, split for a smooth arc |
| 6 | `head` | neck2 | (0, 2.6, −5.2), the atlas | 3.0 to the snout | pitch −45…+60, yaw ±30, roll ±25 | aim, roar throw-back, chin impact |
| 7 | `jaw` | head | (0, 2.0, −5.5), under the ear | 2.4 | pitch 0 (closed) … −50 (open) | roars, snarls; the lower fangs |
| 8 | `beard1` | jaw | (0, 1.6, −4.9) | 0.8 | simulated (§2.4) | the white-cream mane under the jaw and throat |
| 9 | `beard2` | beard1 | (0, 0.9, −4.3) | 0.7 | simulated | the same, the lower lobe over the chest |
| 10 / 13 | `upperarmL/R` | chest | (±2.1, 3.4, −1.6) | 1.65 | IK (two-bone, elbow pole **back** +Z) | fore leg; mostly hidden in the shoulder mass |
| 11 / 14 | `forearmL/R` | upperarm | (±2.4, 2.0, −1.3), the elbow | 2.1 | IK | the stone gauntlet (the biggest single moving mass) |
| 12 / 15 | `pawL/R` | forearm | (±2.6, 0.55, −2.6), the wrist | 1.3 | keyed: flat when planted, curled in the air (claws down, −40) | 3-4 claws; stomp contact |
| 16 / 19 | `thighL/R` | pelvis | (±1.9, 3.6, 3.0) | 1.8 | IK (knee pole **forward** −Z) | hind leg |
| 17 / 20 | `shinL/R` | thigh | (±2.2, 2.1, 2.0), the knee | 1.6 | IK | |
| 18 / 21 | `footL/R` | shin | (±2.3, 0.9, 3.4), the hock | 1.1 | keyed; semi-plantigrade, the hock 0.9 b up | 3 claws; hind stomps |
| 22-29 | `t1`…`t8` | pelvis, then chained | t1 at (0, 3.3, 4.6) | 1.9, 1.7, 1.5, 1.4, 1.3, 1.15, 1.05, 1.0 (Σ 11.0) | pitch / yaw / roll per segment, ±60 each | whip, slam, scorpion raise, phase-3 pillar |
| 30 | `tailtip` | t8 | the end of t8 | 0.8 | rigid with t8 | the orange leaf tuft at the tip; the muzzle for the shells |
| 31 | `tree1` | spine1 | (0, 5.2, 0.4) | 1.7 | simulated | the orange-leaved branch growing out of the mid-back (seen in every phase) |
| 32 | `tree2` | tree1 | (0, 6.9, 0.1) | 1.6 | simulated | its crown of orange leaves |
| 33 | `spikesA` | chest | the shoulder crest | | flare pitch 0…+20, scale 1…1.1 | shoulder plates and gold crystals |
| 34 | `spikesB` | spine1 | the mid-back crest | | flare 0…+20 | the tallest plates; 천동만상 launch points |
| 35 | `spikesC` | pelvis | the hip crest | | flare 0…+15 | hip plates |

That is 36 bones. The horns and the gold brow crown are **rigid with `head`**: translucent crystal, no secondary motion.
The shoulder "feather" tufts are rigid with `chest`; the optional `spikesA` flare covers the roars.

### 2.2 Display parts

Raiden uses 52 parts and the mid-bosses use 28-34. The big masses need several displays per bone. Estimates:

- pelvis 3, spine1 3, chest 3;
- head 3 (skull, crown, horns), jaw 1, beard 2;
- 4 legs × 3;
- tail 9;
- tree 2, spike groups 3-5.

That comes to about **56-64 item_displays**. The model study owns this number. Motion only needs the 36 pivots above to
be separate display groups.

### 2.3 Legs: bake-time IK

Feet must not slide; that is the whole heavy look. Do not key the leg rotations directly. Key **foot targets** in the
anchor frame, plus the paw / foot orientation. At bake time, solve each leg with `ik()` from `mboss_rig_math.mjs`
(two-bone, pole, `prevV` continuity):

- fore: upperarm + forearm reach the wrist, elbow pole (0, −0.3, +1);
- hind: thigh + shin reach the hock, knee pole (0, −0.2, −1).

Then:

- **Planted feet keep their target** while the body moves above them: weight shifts, rear-ups, breathing. In a rear-up
  the hind feet stay planted and the fore targets lift with the chest.
- **Turn clips**: the anchor yaws (module). A planted foot must stay fixed in the world, so the bake counter-rotates
  planted targets by the clip's own yaw schedule (§4). The module must then turn the anchor by exactly that schedule.
- **Travel clips** (walk, gallop): stance feet slide backward in the anchor frame at the declared travel speed. This is
  the same idea as fieldgen's `drive` declaration. The module must glide at that speed while the clip plays.
- Allow the 12 % IK stretch only in the gallop and the jump take-off.

### 2.4 Tail and the simulated secondary chains

**Tail keys are parametric.** The bake expands them to 8 segments:

| channel | meaning |
|---|---|
| `tLift` | pitch of t1 at the root, up + |
| `tCurl` | pitch added per segment; it makes the high arc of the idle and the scorpion curl |
| `tSweep` | total yaw, spread over the chain with a lag of **2 t per segment** from root to tip |
| `tTwist` | roll |
| `tFlat` | 0…1: blends the chain to lie on the floor (whip, slam) |
| `tPillar` | 0…1: blends to the phase-3 vertical pillar |

On top of this goes an overlay: a travelling wave (amplitude, period) for idle drift.

Simulated secondary chains are damped springs driven by the parent's acceleration. They are baked per tick like
fieldgen's pendulum (three passes for loops, soft limit by `tanh`):

| chain | period | damping / t | limit | note |
|---|---|---|---|---|
| beard1-2 | 16 t | 0.15 | 25° | swings forward on a chin slam, lifts on the roar throw-back |
| tree1-2 | 24 t | 0.10 | 15° | ×1.5 the body motion; rustles 2-3 times after every impact |
| tail (added to the keys) | 20 t | 0.12 | 20° per segment | follow-through after the whip, the slam and the gallop stop |
| spikes flare | none | | | keyed only |

### 2.5 Phase looks

The phase looks do not change the motion. Element colour sits on the legs and chest in phase 2, and on the back and tail
in phase 3. These are material swaps (like the Guardian's element looks), not bones.

---

## 3. What makes it heavy (authoring rules, in numbers)

1. **Anticipation is long.** The visible wind-up before each hit is long and is the dodge cue. Keep it, or compress it
   only with RETIME (rule 9).

   | attack | wind-up before the hit |
   |---|---|
   | chin slam | 47 t (rear-up hold 20 t) |
   | jump slam | 20 t to the take-off, 44 t to the landing |
   | charge | 31 t coil |
   | 천동만상 | 18 t brace |
   | stomp | 22 t |
   | tail slam | 52 t (hold 36 t) |
   | landslide | 76 t to the first wave |
   | tail whip | only 9 t, but always preceded by the side feint |

2. **Weight shift before any foot lifts.** The body slides 0.3-0.5 b away from the lifting foot over at least 6 t, by
   chest or pelvis roll 6-10° and root offset. This applies to stomps, steps and the landslide tell.
3. **Dip before every rise.** Before a rear-up, take-off or breach, the root drops 0.3-0.6 b over at least 8 t.
4. **Impacts.**
   - Arrive with ease `i` over 3-6 t.
   - On the impact tick, the head and chest overshoot 4-8° past the contact pose.
   - Then 2-4 t of compression: root −0.2…−0.5 b, spine flex 3-6°.
   - Then a slow `o` settle of 15-30 t.
   - Beard, tree and tail ring 2-3 times.
   - Every impact has an event (screen shake, dust, sound).
5. **Overlapping action.** The head leads turns by 6-10 t; the chest follows the head by 2-3 t; the pelvis follows by 3-5
   t; the tail follows the pelvis by 2 t per segment.
6. **Speed caps for big masses.**
   - Body pitch at most 8° per tick, except in the slam frames (at most 15°/t).
   - Root height at most 0.4 b/t, except the jump.
   - The tail tip may reach 40°/t in the whip.
   - The compiler's 120° per tick check is never close.
7. **Ballistics.** Use the Minecraft gravity scale, g ≈ 0.08-0.09 b/t², so apex h = g·T²/8. The jump slam's 24 t of
   air gives about 6.5 b. Hang time at the apex is 2-4 t at most; no floaty holds.
8. **Idle is not still.**
   - Breathing: period 80 t, chest pitch ±1.2°, root ±0.05 b.
   - Head drift: yaw ±3°, pitch ±2.5°.
   - Snarl: jaw 3-8°, every 80 t.
   - Tail: a travelling wave ±4°, phase lag 3 t per segment.
9. **Retiming only compresses.** `retime()` throws on a slowed segment. Author at the slowest wanted timing (the footage
   timing) and speed wind-ups up later in the `RETIME` table, as the Guardian TUNE pass did.

---

## 4. What the clip carries and what the module carries

This follows `fieldgen_clips.mjs`: the clip has no horizontal root travel and no root yaw. The module (`mv/glide`,
`mv/leap`, `mv/turn`) moves and turns the anchor, and the body hitbox follows the anchor.

| motion | module travel | module yaw | clip carries |
|---|---|---|---|
| walk | glide **0.13 b/t** (fixed while `walk` plays; the feet are baked to it) | ≤ 2°/t toward the target | gait, bob, roll |
| turn45 / turn90 | none | **scripted schedule**: smoothstep from tick 6 to tick (len−6), 45° or 90° (peak 5.6°/t for turn90) | steps (feet counter-rotated), head lead, tail drag |
| jump slam | `mv/leap` t20→t44 (24 t) toward the target, distance clamp(dist − 3, 4, 14) b | tracks until t18, then locked | height arc 0 → 6.5 → 0 b, body pitch |
| charge | glide along the locked line, **0.8 b/t**, about 28-30 t (up to 24 b, clamped to the arena) | locked at the launch; the skid adds ≤ 30° | coil, gallop, skid |
| tail whip | none | **scripted 180°** from t9 to t20 (peak about 25°/t), overshoot +10° at t24, back by t30 | tail sweep on the floor, lag |
| tail slam | none | after t70, a normal turn back toward the target | tail raise and slam |
| burrow dive | glide 3 b forward t18→t40 | locked | pitch nose-down, sink to y −7 |
| burrow travel | underground glide 0.3 b/t toward the target (hidden) | free | hidden (y −7.5) |
| breach / emerge | emerge glides 2-3 b forward t8→t38; it appears 5-8 b in front of the target | faces the target | rise from y −5…−7 |
| phase-3 sink | glide to the arena centre first (wiki), then none | none | sink and tail pillar |
| all other attacks | none | tracks during the first 30-40 % of the wind-up, then locked | everything |

Notes:

- **Below-floor heights** (burrow, phase 3) are new to the mid-boss rigs. The fieldgen builder checks that "every low
  point stays over the floor while visible". Azhdaha's builder must allow `root.y` down to −7.5 b.
  - Parts below the floor are hidden by the opaque arena floor.
  - Still, scale the fully buried bones to 0 during the long holds (`burrow_travel`, `tail_pillar`). This saves
    per-tick work and stops edge glitches through the water-look floor if that floor is not opaque.
- **Phase-3 hitbox.** While the body is buried, the damageable target is the tail pillar. The module must move or attach
  a hitbox at the tail (about 0-8 b up at the arena centre) for `p3_sink` → `tail_pillar_sink`.
- **Two-layer tail (open question).** In the original, Azhdaha keeps attacking while the tail fires shells. The rig
  compiler plays one clip per anchor, so `tail_shells` below is a standalone clip in which the body only idles and
  tracks.
  - A later framework option could be a separate tail-only clip layer: the tail parts on their own clip id and tick.
    That is a compiler change, not a motion question.

---

## 5. Motions

Each motion lists:

- the footage it comes from;
- the key poses with ticks (zero = the clip's tick 0);
- the joints that carry it;
- the anticipation / impact / settle beats;
- the root travel.

### 5.1 Idle (breathing)

**Footage:** v1 33.9-35.3, v3 10.3-12.8 (side view, `M/G_charge_b_v3.jpg`), v4 0-2.4 (`M/L_slide_tell_v4.jpg`), and the
portrait.

**Pose.**

- Four legs planted wide, elbows tucked, the head low (snout 1.9 b), jaw nearly closed.
- The back arched up at mid-back.
- The tail arched up and back in a high curve, the tip at about the spike height (6-8 b) and curling forward.

**Motion.**

- Breath: chest/spine1 pitch ±1.2°, root +0.05 b on the inhale; period 80 t.
- Head: a slow pitch nod ±2.5° (40 t), yaw drift ±3° (80 t).
- A low snarl: jaw 3 → 8 → 3° over t30-50.
- Tail wave ±4° in yaw, 3 t lag per segment.
- Tree and beard simulated.
- Feet locked.

**Clip:** `idle`, 80 t, loop.

### 5.2 Turn in place

**Footage.**

- v4 2.4-3.4: about 90° in about 20 t at the end of the landslide tell, 4.5°/t peak.
- After the charge (v3 9.9-12.8) it re-faces slowly.
- It never turns while a strike is active.

**Proposal:** two sizes, mirrored L/R. Small corrections (< 20°) are not turned at all: the head and neck aim inside the
attack clips instead.

**`turn90_l` / `turn90_r`, 36 t.**

| ticks | what happens |
|---|---|
| 0-8 | head and neck lead 25° into the turn; weight goes onto the inner fore |
| 4 → 12 | outer fore steps: lift 0.5 b, plant at 12 (root dip −0.08) |
| 10 → 18 | inner hind steps |
| 16 → 24 | inner fore steps |
| 22 → 30 | outer hind steps |
| 6 → 30 | anchor yaw (smoothstep) |
| 8-30 | the pelvis lags the chest by 4 t; the tail drags 15° outward, then swings through |
| 30-36 | settle; the head overshoots 5° and returns |

Speed: 2.5°/t on average, 5.6°/t peak.

**`turn45_l` / `turn45_r`, 24 t:** two steps (outer fore 3 → 10, inner hind 10 → 17); anchor yaw from 4 to 18.

**`turn180`, 60 t:** used after the tail slam. It is two `turn90` step patterns run back to back with the head leading
40°.

**Events:** `step_fl`, `step_fr`, `step_hl`, `step_hr` (plant ticks), `yaw0`, `yaw1`.

### 5.3 Reposition walk

**Footage:** v3 6.0-7.35 (`M/F_walk_v3.jpg`): it advances about 3.5 b in 27 t, so **0.13 b/t**. Azhdaha rarely walks; it
closes distance with the jump, charge or burrow. The walk is for short repositioning and the phase-3 move to the centre.

**`walk`, 40 t, loop.** Lateral-sequence walk.

- Plants: LH at 0, LF at 10, RH at 20, RF at 30.
- Each foot swings for 12 t and stands for 28 t.
- Stride 5.2 b; fore foot lift 0.6 b, hind 0.45 b.
- Root −0.06 b at each fore plant.
- Chest roll ±1.5° toward the stance side; spine1 yaw ±2.5° with the chest countering.
- The head counter-bobs ±0.08 b, lagging 3 t.
- Tail yaw ±5° in opposite phase.
- Events: the four plants (light shake, step sound).

**`walk_stop`, 16 t:** the last fore plants at 4; the body pitches forward 2° and settles; the head bobs once; the tail
swings through.

### 5.4 Roar

The roar has two forms.

#### (a) Rear-up roar 포효

**Footage.**

- v4 19.6-24.4, `M/N_roar_keys_v4.jpg`: the phase-2 start, and the start of 격류 범람 (water orbs).
- v5 5.6-9.6, `M/N_roar_pyro_v5.jpg`: the pyro 운석 roar.
- v7 31.1-34.4, `M/M_absorb_cryo_v7.jpg`: the end of the phase-3 absorb.

**`roar_rear`, 100 t.**

| ticks | beat | footage |
|---|---|---|
| 0-8 | load: root −0.3, head down, haunches set, tail pressed to the floor | 19.6-20.0 |
| 8-20 | rise (ease `o`): pelvis pitch +55° about the hip line, so the chest goes up about 3.5 b and the head to about 9-10 b. The fore paws leave the floor at t12; the fore legs fold up and out with the claws spread at chest height. Head thrown back +30°, jaw −45° at t18. | up by 20.6 (t+20) |
| 20 | **roar**: sound, radial blast ring | |
| 20-76 | hold, belly to the front. Tremor: chest and head ±1.5° at a 4 t period, jaw quiver. Tail t1-t3 braced on the floor as a third leg. Tree and beard shake. | 20.6-23.4 |
| 76-90 | drop (ease `i`): the fore paws slam at **t88** | 23.6-24.4 |
| 88-92 | compression −0.35 | |
| 90-100 | settle, one head shake | |

Joints: pelvis (the main hinge), chest, neck, head, jaw, fore IK targets, tail base. Root travel: none.

#### (b) Low roar

**Footage:**

- the intro end (v1 31.5-33.6, the radial wind blast);
- the portrait pose;
- the phase-3 absorb start (v6 7.25-9.5).

**`roar_low`, 50 t.**

| ticks | what happens |
|---|---|
| 0-10 | the body pushes back onto the haunches (pelvis −0.4, chest +0.3); the fore legs brace wide; the head thrusts forward and up 20° |
| 10 | jaw −50°, **roar** |
| 12 | blast (radial ring) |
| 12-36 | hold with tremor |
| 36-50 | close and settle |

### 5.5 Chin slam (갈라지는 봉인의 땅, caption 머리 내려찍기)

**Footage:** v2 8.3-12.4, `M/E_chin_keys_v2.jpg`. Zero is v2 8.3. With water fields in phase 2: v4 28.4-32.0 (the same
body motion).

**`chin_slam`, 84 t.**

| ticks | beat |
|---|---|
| 0-14 | anticipation: the head swings up and to its right (yaw −20°, pitch +25°), jaw snarls open; weight back |
| 14-22 | rear-up: pelvis +40°; the fore paws leave the floor at t18; the **left fore rises highest** (the wiki tell "left foot at the top", at t30); belly to the target |
| 22-42 | hold up, looking down at the target, slight sway (v2 9.4-10.4) |
| 42-47 | slam (ease `i`): chest and head come down; the neck stretches; head pitch −35° drives the chin into the floor in front, about 6-7 b ahead of the centre |
| **47** | **impact** (v2 10.65): a crack line forward |
| 47-52 | compression: root −0.25, head 6° past contact |
| 52-82 | slow settle; the head lifts last (v2 11.3-12.4) |

Events: `lift 2`, `rear 18`, `top 30`, `drop 42`, `impact 47`, `end 84`. Root travel: none.

### 5.6 Jump slam (바위 분쇄 충돌)

**Footage:** v2 2.4-5.7, `M/D_jump_keys_v2.jpg`. Zero is v2 2.4. Phase 2 hydro: v4 32.2-36.6.

**`jump_slam`, 72 t.**

| ticks | beat | footage |
|---|---|---|
| 0-15 | deep crouch: root −0.6, chest down, haunches loaded, head low | 2.4-3.15 |
| 15-18 | head lifts | 3.25 |
| 18-20 | the front lifts (pelvis +15°) | 3.32-3.4 |
| **20** | **take-off**: hind legs extend explosively (IK stretch) | |
| 20-44 | air: root height up to **6.5 b at t32** (out of frame at v2 4.3), body pitch +20° rising, then −15° falling (t40). The fores reach forward and down; the hinds trail. | |
| **44** | **landing**, fores and chest: **wave 1** | v2 4.6 |
| 44-50 | compression −0.5 | |
| 50-55 | the hinds land with a heave; the **left hind** comes down at **t55**: **wave 2** (wiki: "watch the left hind leg") | v2 5.15-5.25 |
| 55-72 | settle; head up last | |

Travel: `mv/leap` from t20 to t44 (§4). Events: `crouch 0`, `takeoff 20`, `apex 32`, `land 44`, `wave2 55`, `end 72`.

### 5.7 Charge (바위 용왕의 돌진: curls the body back, then charges)

**Footage:** v3 6.6-10.3 (`M/G_charge_keys_v3.jpg`, `M/G_charge_roll_v3.jpg`, `M/G_charge_b_v3.jpg`). Zero is v3 6.6.

The coil is a **lateral C-curl**. The head and chest swing round to its right flank (spine1 yaw −20°, chest −25°, neck
−15°, head −10°), the right shoulder drops (roll 8°), the root sinks 0.4, and the tail swings to the same side, so the
body is nearly a ring.

The release is a low, shoulder-first bound across the arena, about 30 t long, ending in a skid. The camera passes it, so
the gait is not clear in the footage. A bound gallop with the head low and the body still twisted about 20° is the best
match.

**`charge_coil`, 34 t, next `charge_run`.**

| ticks | what happens |
|---|---|
| 0-8 | head lowers |
| 8-14 | curl |
| 14-31 | coiled hold with a tremble (the tell, v3 7.3-8.15) |
| 31-34 | release; dust burst at 32 (`launch`) |

**`charge_run`, 12 t, loop.** Bound gallop:

- hinds push at 0, fores reach at 4 and plant at 6, hinds swing 6-12;
- body pitch ±6°, root ±0.25;
- head pitched −15° (horns forward), still turned 15° toward the old curl side;
- tail streaming low.

The module glides at 0.8 b/t.

**`charge_stop`, 24 t.**

| ticks | what happens |
|---|---|
| 0-8 | skid: fores braced forward, pelvis yaw 25° (the rear swings out), root −0.3, dust; the module may add ≤ 30° of yaw |
| 8 | `stop` |
| 8-24 | recover; head up; tail follow-through |

The footage settles at v3 9.9-10.3.

### 5.8 Back-spike launch (천동만상)

**Footage:** v1 35.9-37.9, `M/C_spikes_keys_v1.jpg` f-o. Zero is v1 35.9. The phase-3 variants (ice / electro fields)
have the same body motion (`M/Q_espikes_v7.jpg`).

**`spikes`, 48 t.**

| ticks | what happens |
|---|---|
| 0-14 | brace: crouch (root −0.35), head down −20°, back humped (spine1 pitch −8°); spike groups bristle +12° at t10-16 |
| 16-18 | heave: root +0.15 snap, flare +20°, jaw opens |
| **18** | **launch** (v1 36.8): 4 gold spikes leave spikesB and spikesA |
| 18-24 | secondary bursts (`launch_last 24`) |
| 24-34 | spikes relax |
| 34-48 | settle into idle |

The spikes land about 1 s later and explode about 3 s after landing. That is module timing, not clip timing. Root travel:
none.

### 5.9 Foot stomp, three shockwaves (산명곡응)

**Footage.**

- Front: v3 29.7-32.5 (`M/K_stomp_keys_v3.jpg`); zero is v3 29.8.
- Hydro front: v4 36.6-38.4 (`M/K_stomp_hydro_keys_v4.jpg`).
- Front and back feet both occur (wiki).

**`stomp_fl`, 72 t.** The others are mirrors: `stomp_fr`, and `stomp_hl` / `stomp_hr` with the hind changes below.

| ticks | beat | footage |
|---|---|---|
| 0-6 | weight shift away: chest roll 6° away, root 0.35 b to the other side, the other fore braced | |
| 6-15 | lift: paw to 3.0 b, elbow high, chest roll 10° away, head turned 15° toward the foot | 29.9-30.25, highest at 30.25 |
| 15-17 | hang (the tell) | |
| 17-22 | slam (ease `i`) | |
| **22** | **wave 1** | v3 30.55 |
| 22-26 | compression; the paw stays planted, pressing | |
| **37** | **wave 2**: chest dip −3° at 36-38, a shoulder push | 31.3 |
| **52** | **wave 3**: the same dip | 32.05 |
| 52-72 | recover | |

**Hind variant:**

- the hind foot lifts to 1.8 b (knee high);
- pelvis roll 8° away;
- the tail swings 20° to the opposite side as a counterweight;
- the same ticks.

Waves are 15 t apart. The wiki says the three cannot all be dodged with back-to-back dodges, so do not shorten the gaps.

### 5.10 Side feint (성동격서, caption 좌우로 흔드러)

**Footage:** v3 13.0-15.6, `M/H_feint_keys_v3.jpg`. Zero is v3 13.0. It is used when the target is at its side, and it
is usually followed by the tail whip.

**`feint`, 56 t.**

| ticks | beat | footage |
|---|---|---|
| 0-12 | sway to its right (roll 8°, root 0.4 b right, head 15° right): the feint | 13.0-13.6 |
| 12-18 | sway back past the centre to the left (roll −10°) | 13.6-13.9 |
| 18-22 | heave: root +0.2, then down to −0.4 | |
| **22** | **impact**: rock spikes erupt along **both flanks**, with small hits front and back | 14.1 |
| 22-30 | shudder | |
| 30-52 | recover; head turns toward the target | |

Events: `sway 0`, `swayback 12`, `drop 18`, `burst 22`, `end 56`.

### 5.11 Tail whip (교활한 통수, caption 꼬리 후려치기)

**Footage:** v3 19.6-21.8, `M/I_whip_fine_v3.jpg`. Zero is v3 19.6. Phase 3 leaves an element strip on the swept arc:
`M/R_tailatk_electro_v7.jpg`, `M/R_tailatk_cryo_v8.jpg`.

It is a **fast 180° pivot**. The tail lies flat and sweeps a wide floor arc (about 240° of sweep, tip radius about 11 b).
Rocks erupt along the swept arc right after.

**`tail_whip`, 52 t.**

| ticks | beat | footage |
|---|---|---|
| 0-8 | wind: the body coils away from the whip direction (chest yaw +15°); the tail cocks to the opposite side (+25°) and drops toward the floor (`tFlat` → 1); root −0.2 | 19.6-19.95 |
| 9-20 | **pivot**: the anchor yaws 180° on the module's schedule. The front pivots on the fores; the hind end swings round. The tail lags 2 t per segment, so the tip arrives last. | 20.05-20.62 |
| 12-20 | hit window: sweep | |
| 20-24 | overshoot +10°, then the tail counter-swings | |
| **22** | `erupt`: rocks and spikes along the arc | 20.7-21.0 |
| 24-50 | settle; the tail returns to the high arc by 50 | 21.0-21.8 |

Events: `wind 0`, `pivot 9`, `sweep 12`, `sweep_end 20`, `erupt 22`, `end 52`.

### 5.12 Tail slam (꼬리찍기)

This one is in the footage but not in the wiki list. The caption says the wind-up is long and it can be dodged sideways.

**Footage:** v3 24.1-29.7 (`M/J_tailslam_keys_v3.jpg`, `M/J_tailslam_b_v3.jpg`). Zero is v3 24.4. The target is behind
the boss.

**`tail_slam`, 90 t.**

| ticks | beat |
|---|---|
| 0-12 | the tail rises high over the back (`tLift` +60°, the curl straightens, tip about 12 b up); the body leans onto the fores |
| 12-48 | hold, tip quivering (the long tell) |
| 48-52 | slam (ease `i`): the tail crashes in a straight line **behind** the boss, flat along the body axis |
| **52** | **impact** (v3 26.8) |
| 54-58 | gold spikes erupt along the tail line (v3 27.1) |
| 58-70 | drag: the tail drags 30° sideways and lifts |
| 70-90 | settle; then the module plays `turn180` toward the target (v3 28.4-29.6) |

### 5.13 Burrow, travel, emerge (잠복 돌진; phase 1 only; invulnerable underground)

**Footage.**

- Dive: v2 13.6-15.8 (`M/F_dive_keys_v2.jpg`).
- Travel and breaches: v2 16-40 (`M/F_burrow_*`; the analyst's `S:az/understand/v2/sheet_surface*`).
- Final emerge: v3 3.4-6.8 (`M/F_emerge_keys_v3.jpg`, `M/F_walk_v3.jpg`).

**`burrow_dive`, 44 t.** Zero is v2 13.6.

| ticks | what happens |
|---|---|
| 0-12 | snarl: head up, jaw −40° (v2 13.9) |
| 12-18 | head down to the floor |
| 18-30 | dive: pitch −50° (nose-down, about the chest), root → −3.5, roll 20° (twisting), the hinds push |
| 30-40 | the rear and tail slide under (root → −7, pitch eases to −20) |
| 42 | the tail tip is gone (v2 15.8) |

Module: 3 b forward glide, t18 → t40.

**`burrow_travel`, 20 t, loop.** Root at −7.5, all parts below the floor (hidden, scaled 0). The visuals are module fx: a
moving dust and rock plume, plus rock-fall along the player's movement.

An optional `burrow_fin` variant (root −5.6) shows only the spikesB tips sliding along the floor like a fin.

**`burrow_breach`, 36 t.** "2~3회 잠시 올라오며 피해": two or three brief surfacings, about 60-90 t apart (v2 22.6,
25.6, 30.3).

| ticks | what happens |
|---|---|
| 0-8 | rumble (gold crack ring at the target) |
| 8-14 | burst: head and chest breach at +50° pitch, root −7 → −2.5 (head 3-4 b above the floor), jaw open |
| 14-18 | hang |
| 18-30 | fall back under |
| 30-36 | hidden |

Events: `ring 0`, `burst 8`, `hit 10`, `under 30`.

**`burrow_emerge`, 56 t.** Zero is v3 4.0.

| ticks | what happens |
|---|---|
| 0-8 | rumble; spike tips first |
| **8** | **burst**: gold rocks (v3 4.4) |
| 8-30 | the body rises nose-first while crawling forward (root −5 → 0, pitch +25 → 0) |
| 24 / 28 | the fores claw out and plant |
| 30-38 | the hinds climb out |
| 40-50 | shake: roll ±5°, 4 t period (v3 6.2) |
| 50-56 | settle |

Module: 2-3 b forward glide, t8 → t38. The footage stands fully at v3 6.8 and walks on.

### 5.14 The six-hit transition (파멸의 산사태)

**Footage.**

- v4 0-12.6: `M/L_slide_tell_v4.jpg`, `M/L_slide_keys_v4.jpg`, `M/L_slide_a_v4.jpg`, `M/L_slide_b_v4.jpg`.
- v5 24.6-32.6, phase 2 → 3: `M/L_slide_tell_v5.jpg`, `M/L_slide_c_v5.jpg`, `M/L_slide_d_v5.jpg`.

Zero is the message 야타용왕이 곧 … 원소의 힘을 흡수합니다 (v4 0.0). The caption gives the tell: "오른쪽 앞뒤 발을 천천히
들거나 안내 문구가 뜨면 빠르게 뒤로" (it slowly lifts the right fore and hind feet). Every wave is a low, wide ring.

**`landslide`, 270 t.**

| ticks | beat | footage |
|---|---|---|
| 0-60 | tell: the module turns it to face the target (about 90°, v4 2.4-3.4); the head lowers and growls; **slow lift of the right fore (20-40) and the right hind (36-56)**, 0.8 b each, 20 t up and down | |
| 60-76 | crouch | |
| **76** | **wave 1**: both fores slam and the chest drops | v4 3.8 |
| 90-100 | lift right fore | |
| **104** | **wave 2** | v4 5.2 |
| 118-128 | lift left fore | |
| **132** | **wave 3** | v4 6.6 |
| 144-152 | lift right fore | |
| **156** | **wave 4** | v4 7.8 |
| 172-182 | lift left fore | |
| **186** | **wave 5** | v4 9.3 |
| 186-212 | recover, gather | |
| 212-232 | **big rear-up**: pelvis +65°, fores high and spread, head up roaring | v4 10.6-11.6 |
| 232-237 | hang | |
| 237-240 | body slam | |
| **240** | **wave 6**, the biggest | v4 12.0 |
| 240-270 | heavy settle, head down | |

Wave gaps are +28, +28, +24, +30, +54. Events: `tell 0`, `w1 76`, `w2 104`, `w3 132`, `w4 156`, `w5 186`, `rear 212`,
`w6 240`, `end 270`. The HP floor is a module matter.

Phase 2 → 3 order (wiki): first the phase-2 special (meteors or water orbs), then `landslide`, then the absorb.

### 5.15 Absorb (원소 흡수)

#### Phase 1 → 2

**Footage:** v4 13.6-19.6 (`M/M_absorb_keys_v4.jpg`, `M/M_absorb_hydro_v4.jpg`); pyro v5 1.6-6.4. Zero is v4 14.0.

**`absorb`, 108 t, next `roar_rear`.**

| ticks | what happens |
|---|---|
| 0-12 | the head presses to the floor (head −40°, chest −0.8 b); the back and spike crown point at the sky; fores wide |
| 12-60 | hold: a slow heave (20 t), the element swirl at the legs (fx) |
| 60-70 | push up |
| 70-76 | left fore lifts; **stamp at 76** (v4 17.8) |
| 88-100 | right fore lifts; **stamp at 100** (v4 19.0) |
| 100-108 | settle |

Then the roar (v4 19.6).

#### Phase 2 → 3

**Footage:** v6 0-9.5 (`M/M_absorb_electro_v6.jpg`) and v7 23.6-34.4 (`M/M_absorb_cryo_v7.jpg`).

**`absorb_p3`, 70 t, next `roar_rear`.**

| ticks | what happens |
|---|---|
| 0-20 | it stands tall: chest +0.3, head lifted +20°, spike groups flare +15° (the element orb forms above the back) |
| 20-60 | hold, chest heaving, head looking up |
| 60-70 | gather |

In the footage the orb phase lasts 50-60 t and then the rear-up roar follows (v7 31.1-34.4). After the roar comes
`p3_sink`.

### 5.16 Phase-3 burrow: only the tail above ground

**Footage:**

- electro: v6 10.0-38.0 (`M/O_tail_keys_v6.jpg`, `M/O_tailburrow_in_v6.jpg`, `M/O_tailburrow_mid_v6.jpg`,
  `M/O_tailburrow_out_v6.jpg`);
- cryo: v8 0-23 (`M/O_tailburrow_cryo_v8.jpg`).

The boss first moves to the arena centre (wiki).

**`p3_sink`, 80 t.** Zero is v6 10.4.

| ticks | what happens |
|---|---|
| 0-8 | crouch |
| 8-32 | sink: root 0 → −4, pitch −25° nose-down, rocking ±4° (v6 10.8-12.0) |
| 32-50 | sink fully: root → −7.5, the pelvis pitched so the tail root stays at the floor |
| 50-72 | the tail rises from flat to vertical (`tPillar` 0 → 1; v6 13.8-14.3) |
| 72-80 | settle |

**`tail_pillar`, 80 t, loop.**

- The tail stands about 8 b above the floor (t1 at the floor), a slight S.
- Sway ±6° in pitch and roll, lagging 3 t per segment up the chain.
- The tip leaves rustle; a glow pulse every 40 t.
- The body is hidden.

The pillar is the hittable target (§4).

**`tail_pillar_strike`, 24 t (optional).** The tip nods 30° toward a target and back at t10. It is a cue for each
lightning round (벼락 습격, 4 rounds) or ice circle (서리 습격).

**`tail_pillar_sink`, 20 t.** The tail drops straight down; gone at 18 (v6 33.0-33.4, with a dust cloud).

The module then waits hidden (about 60 t in v6) and plays `burrow_emerge` near the target. The footage shows the rock
spikes at v6 36.4, the burst at 37.0 and the body out at 38.0. If the HP reached 0 underground, it emerges first and dies
on the next hit (wiki).

### 5.17 Tail fires shells (쏟아지는 천화 / 번개의 가루, caption 원소발사)

**Footage:**

- electro: v7 0-10 (`M/P_shells_keys_v7.jpg`, `M/P_shells_electro_v7.jpg`);
- cryo: v8 28-40 and v9 0-6.6 (`M/P_shells_cryo_v8.jpg`, `M/P_shells_cryo_v9.jpg`).

**`tail_shells`, 180 t.** Zero is v7 0.0.

| ticks | what happens |
|---|---|
| 0-20 | the tail lifts over the back into a **scorpion pose**: `tLift` +75°, t2-t4 vertical, t5-t8 curling forward over the head, tip about 10 b above the shoulders; the body braces |
| 20-32 | charge: the tip coils tighter and quivers (v7 1.0-1.6) |
| 34, 54, 74, 94, 114 | **five volleys**: each one, the tip recoils back 12° at v and snaps forward at v + 4 |
| 114-150 | hold |
| 150-176 | the tail lowers to the idle arc (v7 8.4-10.0) |

The muzzle is the `tailtip` end. The body idles; the module tracks at ≤ 2°/t. Cryo: 5 volleys of homing ice spikes.
Electro: the shells are fired at once and fall in sequence. Both use the same clip, and the module paces the projectiles.

### 5.18 Entrance

**Footage:** v1 24.0-33.6, `M/A_intro_v1.jpg`. The glyph-light seal and the steles breaking are arena props.

**`intro`, 150 t, next `idle`.**

| ticks | what happens |
|---|---|
| 0-30 | sealed crouch: head down, still, glyph light |
| 30-60 | rises and rears up (pelvis +50°) |
| 50, 70 | stele cracks (`crack1`, `crack2`) |
| 60-100 | rear-up roar hold |
| 100-116 | drops to all fours; impact 116 |
| 120-150 | low roar: jaw −50°, radial blast at 130 |

The fight starts with the open-mouth crouch of the portrait (v1 33.5).

### 5.19 Death (no footage; proposed)

The lines are "난… 사라지지 않아! / 모…락스…!".

**`death`, 120 t.**

| ticks | what happens |
|---|---|
| 0-14 | stagger: root 0.5 b back, head jerks up, jaw opens |
| 14-34 | the fores buckle (elbows fold); the chest drops; **chin hits the floor at 34** |
| 34-52 | the hinds fold; the pelvis drops 2 b; belly on the floor |
| 52-70 | slumps onto its right flank (roll +18°); **the tail falls flat at 66** |
| 70-92 | the head lifts weakly (the last line) and falls at 92 |
| 92-120 | still; the eye glow fades |

The module then plays the seal / petrify fx (gold glyphs, as in the domain text). Events: `stagger 0`, `chin 34`,
`tail 66`, `last 80`, `head 92`, `still 96`, `end 120`.

### 5.20 Reference pose

**`pose_ref`, 20 t, loop.** The portrait: a low roaring crouch, fores braced wide, the head thrust forward, the jaw at
−45°, the tail curled behind. It is for renders and the end pose of `intro`.

---

## 6. Proposed clip list

All clips are authored at footage speed. Events are in authored ticks. "Mirror" means generated by a mirror pass in the
clip generator: swap L/R channels and negate yaw and roll.

| clip | len | loop / next | events (tick) | module | §  |
|---|---|---|---|---|---|
| `idle` | 80 | loop | (snarl 30) | ≤ 2°/t tracking | 5.1 |
| `walk` | 40 | loop | `lh 0`, `lf 10`, `rh 20`, `rf 30` | glide 0.13 b/t | 5.3 |
| `walk_stop` | 16 | → idle | `plant 4` | | 5.3 |
| `turn45_l`, `turn45_r` (mirror) | 24 | → idle | `step_*` plants 10, 17; `yaw0 4`, `yaw1 18` | yaw 45 by schedule | 5.2 |
| `turn90_l`, `turn90_r` (mirror) | 36 | → idle | plants 12, 18, 24, 30; `yaw0 6`, `yaw1 30` | yaw 90 by schedule | 5.2 |
| `turn180` | 60 | → idle | plants 12…54; `yaw0 6`, `yaw1 54` | yaw 180 by schedule | 5.2 |
| `intro` | 150 | → idle | `rise 30`, `crack1 50`, `crack2 70`, `land 116`, `roar 120`, `blast 130` | | 5.18 |
| `pose_ref` | 20 | loop | | | 5.20 |
| `roar_low` | 50 | → idle | `roar 10`, `blast 12` | | 5.4 |
| `roar_rear` | 100 | → idle | `rise 8`, `roar 20`, `drop 76`, `land 88` | | 5.4 |
| `chin_slam` | 84 | → idle | `lift 2`, `rear 18`, `top 30`, `drop 42`, `impact 47` | tracks until about 20 | 5.5 |
| `jump_slam` | 72 | → idle | `takeoff 20`, `apex 32`, `land 44`, `wave2 55` | leap 20 → 44 | 5.6 |
| `charge_coil` | 34 | → charge_run | `coil 8`, `launch 32` | locks the line at 31 | 5.7 |
| `charge_run` | 12 | loop | `plant 6` | glide 0.8 b/t | 5.7 |
| `charge_stop` | 24 | → idle | `skid 0`, `stop 8` | skid yaw ≤ 30° | 5.7 |
| `spikes` | 48 | → idle | `brace 0`, `launch 18`, `launch_last 24` | | 5.8 |
| `stomp_fl`, `stomp_fr` (mirror) | 72 | → idle | `lift 6`, `slam 17`, `w1 22`, `w2 37`, `w3 52` | | 5.9 |
| `stomp_hl`, `stomp_hr` (mirror) | 72 | → idle | the same | | 5.9 |
| `feint` | 56 | → idle (or `tail_whip`) | `sway 0`, `swayback 12`, `drop 18`, `burst 22` | | 5.10 |
| `tail_whip` | 52 | → idle | `wind 0`, `pivot 9`, `sweep 12`, `sweep_end 20`, `erupt 22` | yaw 180 scripted 9 → 20 | 5.11 |
| `tail_slam` | 90 | → turn180 | `raise 0`, `hold 12`, `slam 48`, `impact 52`, `spikes 54` | | 5.12 |
| `burrow_dive` | 44 | → burrow_travel | `snarl 4`, `dive 18`, `under 42` | glide 3 b, 18 → 40 | 5.13 |
| `burrow_travel` | 20 | loop | | underground glide 0.3 b/t; hidden | 5.13 |
| `burrow_breach` | 36 | → burrow_travel | `ring 0`, `burst 8`, `hit 10`, `under 30` | | 5.13 |
| `burrow_emerge` | 56 | → idle | `rumble 0`, `burst 8`, `fore 24`, `out 38`, `shake 40` | glide 2-3 b, 8 → 38 | 5.13 |
| `landslide` | 270 | → absorb / absorb_p3 | `tell 0`, `w1 76`, `w2 104`, `w3 132`, `w4 156`, `w5 186`, `rear 212`, `w6 240` | turn to face in 0-60 | 5.14 |
| `absorb` | 108 | → roar_rear | `press 0`, `rise 60`, `stamp1 76`, `stamp2 100` | | 5.15 |
| `absorb_p3` | 70 | → roar_rear | `orb 0`, `gather 60` | | 5.15 |
| `p3_sink` | 80 | → tail_pillar | `sink 8`, `under 50`, `tail 50`, `pillar 72` | move to the centre first | 5.16 |
| `tail_pillar` | 80 | loop | `pulse 0`, `pulse 40` | hitbox at the tail | 5.16 |
| `tail_pillar_strike` | 24 | → tail_pillar | `strike 10` | | 5.16 |
| `tail_pillar_sink` | 20 | (hidden) | `gone 18` | then `burrow_emerge` | 5.16 |
| `tail_shells` | 180 | → idle | `raise 0`, `charge 20`, `v1 34`, `v2 54`, `v3 74`, `v4 94`, `v5 114`, `lower 150` | tracking ≤ 2°/t | 5.17 |
| `death` | 120 | (end) | `stagger 0`, `chin 34`, `tail 66`, `last 80`, `head 92` | | 5.19 |

That is 34 clips, 30 authored and 4 mirrors. Total authored length is about 2400 t. The long holds (`tail_pillar`,
`burrow_travel`, the roar holds) compile to few keys, so most of the output size is in the fast clips.

**RETIME starting points** (chapter 1, if playtests say so):

- Keep the tells that the wiki calls the dodge cue at full length: chin-slam hold, tail-slam hold, landslide tell,
  stomp hang.
- Shorten the dead time instead: settles −20 %, the absorb hold −30 %, the `roar_rear` hold −25 %.

---

## 7. Open points for the plan

1. **Tail layer.** Should Azhdaha attack while the tail fires (original behaviour)? That needs a tail-only clip layer in
   the rig compiler (§4). Without it, `tail_shells` is standalone.
2. **Below-floor states.** The builder check, scale-0 hiding and the phase-3 tail hitbox (§4) are framework and module
   work.
3. **Turn schedules.** Feet stay planted only if the module follows each clip's yaw schedule exactly. Export the
   schedule with the clip, in the manifest or as an events table, so the module does not use `mv/turn` with a free rate
   during these clips.
4. **The charge gait** is half-hidden by the camera in the footage. The bound gallop is my best fit. The coil (lateral
   C) and the skid are clear.
5. **Death** is not in the footage; §5.19 is a proposal.
6. **Scale.** 23 b overall in a 28-b-radius arena (§1). The model study may prefer ×0.85.

---

## 8. Key-pose sheet index (`M/`)

Sheet types:

- **`*_keys_*` and `00_*`** are hand-picked, cropped key frames: label, seconds and ticks from the stated zero. **Use
  these first.**
- **`*_a/_b/_c/_d`** and others are even-step sheets over the whole window, at 0.1-0.5 s steps.

| motion | key sheets | wider sheets |
|---|---|---|
| skeleton | `00_skeleton_proposal.jpg`, `00_skeleton_overlay_v3.jpg`, `skel_side_v3.jpg` | |
| intro / roar_low | | `A_intro_v1.jpg`, `A_roar_intro_v1.jpg` |
| idle | `B_idle_keys_v1.jpg` | `B_idle_v1.jpg`, `G_charge_b_v3.jpg` (side idle) |
| 천동만상 | `C_spikes_keys_v1.jpg` | `C_spikes_a_v1.jpg`, `C_spikes_b_v1.jpg`, `C_spikes_c_v2.jpg`, `Q_espikes_v7.jpg` |
| jump slam | `D_jump_keys_v2.jpg` | `D_jump_a_v2.jpg`, `D_jump_b_v2.jpg`, `S_hydro_chin_jump_v4.jpg` |
| chin slam | `E_chin_keys_v2.jpg` | `E_chin_a_v2.jpg`, `E_chin_b_v2.jpg`, `S_hydro_chin_jump_v4.jpg` |
| burrow / emerge / walk | `F_dive_keys_v2.jpg`, `F_emerge_keys_v3.jpg`, `F_walk_v3.jpg` | `F_burrow_a_v2.jpg`, `F_burrow_b_v2.jpg`, `F_burrow_c_v2.jpg`, `F_burrow_d_v3.jpg` |
| charge | `G_charge_keys_v3.jpg`, `G_charge_roll_v3.jpg` | `G_charge_a_v3.jpg`, `G_charge_b_v3.jpg` |
| side feint | `H_feint_keys_v3.jpg` | `H_feint_a_v3.jpg`, `H_feint_b_v3.jpg` |
| tail whip | `I_whip_fine_v3.jpg`, `I_whip_keys_v3.jpg` | `I_whip_a_v3.jpg`, `I_whip_b_v3.jpg`, `R_tailatk_electro_v7.jpg`, `R_tailatk_cryo_v8.jpg` |
| tail slam | `J_tailslam_keys_v3.jpg` | `J_tailslam_a_v3.jpg`, `J_tailslam_b_v3.jpg` |
| stomp | `K_stomp_keys_v3.jpg`, `K_stomp_hydro_keys_v4.jpg` | `K_stomp_a_v3.jpg`, `K_stomp_b_v3.jpg`, `K_stomp_hydro_v4.jpg` |
| landslide | `L_slide_keys_v4.jpg`, `L_slide_tell_v4.jpg`, `L_slide_tell_v5.jpg` | `L_slide_a_v4.jpg`, `L_slide_b_v4.jpg`, `L_slide_c_v5.jpg`, `L_slide_d_v5.jpg` |
| absorb | `M_absorb_keys_v4.jpg` | `M_absorb_hydro_v4.jpg`, `M_absorb_pyro_v5.jpg`, `M_absorb_electro_v6.jpg`, `M_absorb_cryo_v7.jpg` |
| roar_rear | `N_roar_keys_v4.jpg` | `N_roar_hydro_v4.jpg`, `N_roar_pyro_v5.jpg` |
| phase-3 tail burrow | `O_tail_keys_v6.jpg` | `O_tailburrow_in_v6.jpg`, `O_tailburrow_mid_v6.jpg`, `O_tailburrow_out_v6.jpg`, `O_tailburrow_cryo_v8.jpg` |
| tail shells | `P_shells_keys_v7.jpg` | `P_shells_electro_v7.jpg`, `P_shells_cryo_v8.jpg`, `P_shells_cryo_v9.jpg` |
| phase-2 pyro overview | | `T_pyro_v5.jpg`, `U_misc_v9.jpg` |

Tools, re-runnable, in `S:az/understand/motion_tools/`:

- `sheet.py`: even-step sheets;
- `keys.py`: picked key frames with crops and tick labels;
- `skeleton.py`: the skeleton views and the overlay;
- `jobs.txt`: the batch of windows used.
