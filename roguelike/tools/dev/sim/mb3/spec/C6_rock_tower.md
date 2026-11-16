# C6 중력 시스템·파쇄 (바위 날리기, tower form): implementation spec

| field | value |
|---|---|
| pattern | id 6, key `rock`, state cruise, kind normal, owner `cruise.py` |
| clip | `tower_throw`, 157 t: dip 0, vent 12, tower 20, band 38, **burst 55**, **throw 95**, revert 142 |
| length | 157 (`max_len=165`); recover 20 |
| element | Geo (5) |
| coefficients | floor burst 1.3 (`DMG['c6']` 130, raw 17), KB heavy 4; slab 1.1 (`DMG['c6s']` 110, raw 14), KB 3 |
| hits | bursts: ≤ 1 for a standing player (≤ 2 at 4 b); slabs: **≤ 2 per run** (cap, F3); worst case 3.5 (4.8 at 4 b) |
| bands | mid ×2, far ×1 |

## 1. Footage and plan check

Source: v3 R take B, 17.00-24.85 s, and take C (`understand/v3.md` §2 R). R0 = the dip. I re-checked
`sheet_rock_burst_positions.jpg`. The bursts start at the device's front-left, sweep across its front 4-7 m out, and
the last one erupts under the player (hit 8529 = 25 % max HP + knockdown).

| event | footage R+ t | rig `tower_throw` | verdict |
|---|---|---|---|
| dip: roll 25-30°, drops toward the player (ring ≈ 3 m, 2-3 m from her) | 0-12 | `dip` 0 (to 2.8 b, roll 27°) | ok; add a short glide (F4) |
| vent flare: gold shaft up from the top; both medallions flung up / out to ±6 m | 14-22 | `vent` 12 | ok |
| rises to 4.5 m and levels; the tower telescopes up, halo ×1.7 | 22-40 | `tower` 20 | ok |
| medallions dock on the tower top | 40-43 | (in `tower` 20-38) | ok |
| charge: a flat gold flame band under the ring (Ø 4.5-8 m), pulsing | 42-59 | `band` 38 | ok |
| floor bursts ×8, 6 t apart, walking in an arc across the front, the last on the player | 60, 65, 71, 77, 83, 89, 95, 103 | `burst` 55, then every 6 t (55 … 97) | −5 t, ok |
| each burst tears out a slab (3 × 1.2 × 0.8 m, glowing rim), rising to 4-7 m in 10-20 t | 62-100 | module props | ok |
| slab throws, one at a time, straight and slightly down, ≈ 8 t apart, landing within 1-2 m of the player; 6 throws (take C: 4) | ≈ 101-140 | `throw` 95, every 8 t | ok; 5 throws |
| revert: the tower collapses into the ring with a 20° roll wobble | 142-157 | `revert` 142 | ok |

Plan disagreements and fixes:
- **F1 — the walk.** The stub's `api.rocks` puts the first burst 6 b from the player on the device's side, and each
  next one 2.5 b closer. From burst 3 on, every burst is centred on the player's spot. Knockback 4 moves the player
  only 1.0 b (`player/knockback`: 0.1 b × (4+3+2+1)), so a standing player is hit by bursts 3-8: **6 × 1.3 = 7.8**.
  The footage hit her once, with the last burst. **Fix: an arc walker.** Burst k is placed at the player's current
  distance D from the body (clamped 2.5-18 b), at the bearing to the player turned by σ·θ_k. The offsets are
  θ = 90, 77, 64, 51, 39, 26, 13, 0° (90 · (7 − k) / 7), and σ = ±1 is drawn once per run.
  - The sweep crosses the device's front and converges on the player: the last burst is on the feet (10 t before
    the strike), the 7th 13° off.
  - Bursts 7 and 8 share **one volley group**, so a standing player takes one hit.
  - At D 6 the 6th burst is 2.7 b off (miss; reach 2.1), at D 4 it is 1.8 b off (hit).
- **F2 — throw count.** The plan says 4-6, the footage 6 (take C 4). Keep the stub's **5**: 95, 103, 111, 119, 127,
  last landing about 134 < revert 142.
- **F3 — slab cap.** Each throw is its own hazard, and FW-4 rules out grouping throws (a member launched after its
  group struck is armed again). So a standing player could take 5 × 1.1. **Fix: at most 2 slab hits per run.**
  - `pj_end` counts `#pjEv 4` (a hit) in `#fq6SH`.
  - At each throw tell (−10) and at each launch: if `#fq6SH` ≥ 2, skip the throw and drop that slab (crumble fx).
  - Throws are 8 t apart and land in about 6 t, so the count is current at the next launch.
- **F4 — the dip toward the player.** The footage dips 2-3 m from the player. While the player is farther than 5 b,
  the body steps toward them 0.2 b/t during 0-11 (≤ 2.4 b, `g.bstep('toward', 0.2)`). That keeps the mid-band read
  without leaving the band.

## 2. AI

- **Bands:** mid ×2, far ×1.
- **Facing:** `face/track` 0-142 (4°/t; the dip roll faces the player).
- **Aim locks:**
  - σ (the sweep side) at 0: `random value 0..1` → ±1.
  - Each burst decal tick (strike − 10): the bearing and distance to the player, then the arc point (F1), then
    `g.clamp_walk()`.
  - Each throw tell (throw − 10): `g.lockp()` + `g.keep('rlk_mb_fg_p6t<j>')`.

## 3. Body travel

| ticks | travel |
|---|---|
| 0-11 | `g.bstep('toward', 0.2)` while the player is ≥ 5 b away (≤ 2.4 b) |
| 12-157 | none |

## 4. Per-tick timeline

`ring` = body + the manifest `ring_centre` of the event (2.8 at 12-20, 4.5 from 38). `hub` = ring + 0.7.

| t | rig | mechanics | fx (kit) | sound |
|---|---|---|---|---|
| 0 | core plays `tower_throw`: dip to 2.8 b, roll 27° | `face/track`; σ; dip glide 0-11 | `K.fx('dip')` at the floor under the body, rotated as it | `K.snd('dip')` |
| 12 | `vent` (column up, medallions flung to ±5.5 b) | | `K.fx('vent_flare')` at the hub (`~ ~3.5 ~`) | `K.snd('vent_flare')` |
| 20 | `tower` (rise and level, the tower telescopes, 20-38) | | `K.fx('tower_up')` at the ring (`~ ~3.6 ~`) | `K.snd('tower_up')` |
| 26, 32 | | | | `K.snd('gear_click')` |
| 38 | `band` (tower form; flame band 38-55) | | `K.fx('flame_band')` at the ring underside (`~ ~3.9 ~`) | |
| 44 | | | | `K.snd('flame_charge')` |
| 47 | | | `K.fx('flame_band')` (second pulse) | |
| 45, 51, 57, 63, 69, 75, 81, 87 | | burst decal k (arc point, §5); GRP_NEW before k = 7 | `K.tele_disc(1.8, 10)` at the point | `block.amethyst_block.resonate` 0.3/1.4 (quiet tell cue) |
| **55, 61, 67, 73, 79, 85, 91, 97** | `burst` … | burst k strikes (vis 61); its slab starts rising | `K.fx('floor_burst')` at the hazard | `K.snd('floor_burst')` |
| strike + 2 | | slab k rises 4-6 b over 12 t | `K.fx('slab_rise')` at the burst point | `K.snd('slab_lift')` |
| slabs, every 4 t | | | `falling_dust` (tuff) under each hovering slab (the stub's line) | |
| 85, 93, 101, 109, 117 | | throw tell j (lock + keep + line from slab j) unless capped | `K.tele_line(len, 2.4, 10)` from slab j's floor point toward the lock | `block.chain.hit` 0.5/0.8 |
| **95, 103, 111, 119, 127** | `throw` … | throw j: GRP_NEW, blade pj (§7) unless capped | `K.fx('slab_throw')` at the slab, rotated along the throw; `K.fx('slab_trail')` every 2 t on the flying slab | `K.snd('slab_throw')` |
| each landing (`pj_end` #pjEv 1/2) | | the slab shatters | `K.fx('slab_impact')` | `K.snd('slab_impact')` |
| **142** | `revert` (tower folds, roll wobble) | crumble every unthrown slab | `K.fx('revert')` at the ring (`~ ~4.5 ~`); `K.fx('slab_impact')` under each crumbling slab | `K.snd('revert')`, `K.snd('debris_land')` |
| 157 | → `idle_cruise` | `g.end()` (+ `rocks_cancel`) | | |

## 5. Damage areas

### Floor bursts (8)

```
# p/rock/burst<k>, at its decal tick (strike - 10), as the body
function rlk:mboss/mv/dist                                    # #mbDist = body -> player (tenths)
execute store result storage rlk:mboss fg.rk.d double 0.1 run scoreboard players get #mbDist mb   (clamped 25..180)
data modify storage rlk:mboss fg.rk.a set value <σ·θ_k>       # two generated lines: if #fq6S matches 1 / -1
function rlk:mboss/fieldgen/p/rock/place with storage rlk:mboss fg.rk
   $execute at <body> facing entity <player> feet rotated ~$(a) 0 positioned ^ ^ ^$(d) run summon marker ~ 201 ~ {Tags:[..., "rlk_mb_fg_p6w"]}
execute as <p6w> run <g.clamp_walk()>
g.GRP_NEW                                                     # only for k = 6 (the 7th)
*g.hz_opts(kb=KB['heavy'], y1=1.2, vis=61, quiet=1, sfx=0, grp=(k >= 6))
execute at <p6w> run <g.hz_disc(1.8, 10, DMG['c6'])>
execute at <p6w> rotated ~ 0 run <K.tele_disc(1.8, 10)>
summon the slab k (kit prop/slab, scale 0, hidden) at <p6w> ~0.45; mbS k; mbT -10
kill <p6w>
```

- **Shape:** disc r 1.8 (padded 2.1), height −0.5..**1.2** (a jump can clear it), act 1, KB heavy 4 (1.0 b), Geo, 1.3.
- **Groups:** bursts 1-6 are single hazards; bursts 7-8 are one volley group. FW-4: burst 8's decal is made at 87,
  before the group's first strike at 91.

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| decal | 45 | 51 | 57 | 63 | 69 | 75 | 81 | 87 |
| strike | 55 | 61 | 67 | 73 | 79 | 85 | 91 | 97 |
| offset θ | 90 | 77 | 64 | 51 | 39 | 26 | 13 | 0 |
| miss distance to a standing player at D 6 (b) | 8.5 | 7.5 | 6.4 | 5.2 | 4.0 | 2.7 | 1.4 | 0 |

### Slab throws (5)

Throw j (j = 1..5) uses the slab of burst j. Strike ticks are its landing (about 5-7 t of flight).

```
# throw_tell<j> at throw - 10, as the body
execute if score #fq6SH mb matches 2.. run return run function …/rock/crumble<j>
g.lockp(), *g.keep('rlk_mb_fg_p6t<j>')
execute as <slab j> at @s run function …/rock/tl_line       # dmg-0 hz/line w 2.4 tell 10 + K.tele_line(len, 2.4, 10), quiet
# throw<j> at throw, as the body
execute if score #fq6SH mb matches 2.. run return run function …/rock/crumble<j>
g.GRP_NEW
execute as <slab j> run function …/rock/throw_go
   *g.pj_opts(shape=1, kb=KB['default'], wall=1, grp=True); scoreboard players set @s mbId 6
   execute at @s facing entity <p6t<j>> feet run <g.pj_launch(1.5, 24, DMG['c6s'], 0.8)>
# pj_end: #pjEv 1/2 -> shatter (kit slab_impact + sound), #pjKeep 0; #pjEv 4 -> scoreboard players add #fq6SH mb 1
```

- **Shape:** the framework blade (`#pjShape 1`), hr 0.8 → **reach 1.45 b** from the flight line (FW-1: hr + 0.65).
  The line telegraph w 2.4 (the framework pads it to ±1.5) matches it within 0.05 b. Speed 1.5 b/t (whole
  sub-steps; FW-2 does not apply). Life 24 t. Stops at the floor or a wall (`#pjWall 1`). KB 3, Geo, 1.1, its own
  group (one hit per slab).
- **Cap:** ≤ 2 slab hits per run (F3).

## 6. Telegraphs

- **Pattern tell (55 t):** the dip toward the player, the vent flare, the tower, the pulsing flame band.
- **Bursts:** a Geo `tele_disc` r 1.8 exactly 10 t before each burst. The sweep direction is visible from burst 1,
  so the player knows the last ones will come to them.
- **Slabs:** a Geo `tele_line` (w 2.4) from the slab's floor point to the locked feet, 10 t before the throw. The
  hovering slab with its glowing rim is the long read (the footage throw speed is unreadable).
- Telegraph cards: ≤ 2 burst decals + 2 lines live (14 measured by the kit budget).

## 7. Projectiles

- Slab props: kit `prop/slab` (a box 2.2 × 0.6 × 0.9 with a bright rim), summoned hidden (scale 0) at the burst
  point.
  - At the strike: `data merge` to the full scale with `interpolation_duration` 12, and `tp ~ ~<4..6> ~` with
    `teleport_duration` 12, plus a slow tumble (`left_rotation` small).
  - Thrown: `teleport_duration` 1 (the pj library moves it every tick).
  - Tags: `rlk_room rlk_mb_aux rlk_mb_fg_pat rlk_mb_fg_p6 rlk_mb_fg_p6s`, `mbS` = k. Flying: `rlk_mb_fg_p6f`.
- At most 8 slabs and 2 flying at once.

## 8. FX detail

`dip` (3), `vent_flare` (4), `tower_up` (7), `flame_band` ×2 (8), `floor_burst` ×8 (8 cards each), `slab_rise` ×8
(5), `slab_throw` ×5 (3), `slab_trail` (ambient), `slab_impact` ×5-8 (7), `revert` (3). Peak about 30 fx cards (kit
budget table).

## 9. Sound

From v3 §5: a whoosh on the dip; a roaring hiss with the vent; ratchet clicks while the tower builds; a rising roar
for the flame band; a sharp crystal crack + thump per burst; a grinding rise per slab; a heavy whoosh per throw; a
crash per landing; a clunk on the revert.

| tick | sound |
|---|---|
| 0 | `snd/dip` |
| 12 | `snd/vent_flare` |
| 20 | `snd/tower_up` |
| 26, 32 | `snd/gear_click` |
| 44 | `snd/flame_charge` |
| each burst decal | `block.amethyst_block.resonate` 0.3/1.4 |
| each burst | `snd/floor_burst` |
| each slab rise | `snd/slab_lift` |
| each throw tell | `block.chain.hit` 0.5/0.8 |
| each throw | `snd/slab_throw` |
| each landing | `snd/slab_impact` |
| 142 | `snd/revert` + `snd/debris_land` |

## 10. Dodge windows

- **Bursts:** decal 10 t; to leave 2.1 b from a decal's centre:
  - walk 2.2 b ✓ (just);
  - half-speed 1.1 b ✗ → dash (cancels the swing) or jump;
  - **vanilla jump:** feet above 1.2 b only on press +5..+6, so press at strike −6..−5 (a 2 t window: hard in
    cruise, easy in the field, see F2_field_rocks);
  - dash i-frames: press at strike −5..strike.

  Keeping on the move beats the sweep: each burst is placed where the player was 10 t before.
- **Slabs:** the line shows 10 t before the throw, and the slab lands about 16 t after the lock. A 1.5 b sidestep
  clears the blade:
  - walk 7 t;
  - half-speed 14 t;
  - not by jumping (the blade has two rows);
  - dash i-frames when it arrives.
- No C6 hit ignores the dash i-frames.
- Worst case standing still: 1.3 (pair 7/8) + 2.2 (cap) = 3.5; at D ≤ 4.7 burst 6 adds 1.3.

## 11. Diagram (top view, σ = +1)

```
                         b1 (90 deg)
                    b2 .
               b3  .        the sweep follows the player's bearing,
        b4  .                at the player's distance D from S
   b5 .
  .  b6
 [S] ----- b7 - b8=X (player's feet 10 t before each strike)
   slabs rise at b1..b8; throws from slabs 1-5 at 95/103/111/119/127
   (line 10 t ahead, blade 1.5 b/t, reach 1.45 b)
```

## 12. Implementation sketch

Replace `api.rocks()` for C6 by the pattern's own `p/rock/*` (the contract allows it):
- the arc placement macro;
- the 7/8 pair group;
- the slab rise via the kit prop;
- the 5 throws with the cap;
- crumble at 142.

Keep the tags (`rlk_mb_fg_p6*`) so `rocks_cancel(6)` still clears everything. Share the code with F2 through a
helper in `cruise.py` (F2 calls it with its own pid / ticks / palette): a module-local function, not a core change.

## 13. Checks

- 8 burst hazards: tell 10, r 1.8, y1 1.2, dmg 130, KB 4. Only bursts 7-8 share a group, made before 91.
- A standing player at D 6 is hit once by the bursts (at 91 or 97). Walking straight away from the device at
  0.22 b/t, they are not hit by bursts 7-8 (2.2 b in 10 t > 2.1).
- 5 throw lines: tell 10, dmg 0, w 2.4. Each blade pj is launched 10 t after its line, at 1.5 b/t.
- A standing player is hit by at most 2 slabs. The later slabs crumble.
- Every slab, lock and walker is gone after the end and after a cancel.
