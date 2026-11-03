# C3 중력 시스템·코어 (레이저 빔): implementation spec

| field | value |
|---|---|
| pattern | id 3, key `laser`, state cruise, kind normal, owner `cruise.py` |
| clip | `laser`, 175 t: drop 0, charge 4, aim 23, **fire 25**, off 158, retract 159; manifest `orbit` {from 25, to 158, rate 5, medal_eye az0 90 sense −1, medal_gear az0 −90 sense +1, beam from_down 48, length 3.74, spot_r 5.58} |
| length | 175 (`max_len=181`); recover 20 |
| element | Geo (5) |
| coefficient | 0.5 per touch (`DMG['c3']` 50, raw 6); both beams in **one volley group, re-armed every 10 t** |
| hits | at most one per 10 t from both beams together; a player standing in the band takes about 4 (2.0) |
| bands | melee ×2, mid ×2 |

## 1. Footage and plan check

Source: v1 L, 13.90-22.60 s, real time (`understand/v1.md` §3 L); L0 = the pods dropping.

| event | footage L+ t | rig `laser` | verdict |
|---|---|---|---|
| two pods drop beside the core, about 2 m under the ring, 2-3 m out | 0-4 | `drop` 0-4 (medallions to r 2.8, 2.0 b under the ring) | ok |
| spark charge: gold glints spin on each pod (whine at +16) | 4-22 | `charge` 4-23 (medallions hot) | ok |
| thin white aim lines pod → floor | 22.6 | `aim` 23 (beams extend 23-25) | ok |
| FIRE: thick gold beams down-in, muzzle ring, bloom about 1 m wide for 3 t | 23.6 | `fire` 25 | +1 t, ok |
| sustained beams 0.4-0.5 m (0.7 with glow); the spots close and open like scissors | 27-156 | orbit 25-158 at 5°/t, spots on r 5.58 | ok |
| spots meet | +47, +79, +112, +153 (mean 35 t) | 43 (front), 79 (back), 115 (front), 151 (back) | ok |
| spots widest apart | +65, +94, +134 | 61, 97, 133 | ok |
| beams off | 157 | `off` 158 | ok |
| pods rise back | 158-174 | `retract` 159-175 | ok |

The footage gives spots on r ≈ 5 m (4-7), and the rig puts them at 5.58 b (ring centre 4.5 b, 48° from vertical).

Plan disagreements and fixes:
- **F1 — the start azimuths.** The stub makes beam A at the body's yaw (front) and beam B at yaw + 180 (back). The rig
  starts the eye medallion at the device's **left** (az +90) and the gear at its **right** (az −90), and they meet
  in **front** 18 t after `fire`. With the stub the floor hazards would sit 90° away from the drawn beams for the
  whole 133 t. **Fix:**
  - beam E (eye) is made at yaw Y − 90 (the body's left) and turns **+5°/t** (clockwise from above);
  - beam G (gear) is made at Y + 90 and turns **−5°/t**.

  In MC yaw terms the rig's azimuth az (from the front toward the left) is yaw = Y − az. So E's yaw is
  Y − 90 + 5(t − 25) and G's is Y + 90 − 5(t − 25). At 43 both are at Y (front): the rig's meet.
- **F2 — the width.** The plan says "the width blooms then narrows (0.5 → 1.0 → 0.5 b)". The stub turns that into
  1.0 for the whole firing time (27-150). The footage shows a 3 t bloom about 1 m wide at fire and a 0.4-0.5 b beam
  (0.7 b with its glow) after it. **Fix:**
  - the lane decal at 0.6 (the charge read);
  - the hazard at **1.0 for 25-27** (the bloom, with the kit's `laser_fire` bloom);
  - **0.6 from 28** to the end (core 0.45 + glow).
- **F3 — the band.** The stub's line runs r 2.8-5.8. A beam leaves the medallion (r 2.93, 2.38 b up) and reaches the
  floor at r 5.58. Across a standing player's body (0-1.8 b) it lies at r 3.58-5.58. With w 0.6 and the 0.3 body pad
  it touches player centres at r 2.98-6.18. **Fix:** a line from **r 3.0, length 2.8** (3.0-5.8; padded 2.7-6.1).
  That makes the inside of the medallion circle (r < 2.7) a clean safe zone, the read the footage gives (the party
  hits the core from under the device during the lasers).
- **F4 — no turning.** The rig orbits the beams relative to its root. If the body yawed during the pattern, the
  drawn beams would turn with it, while the hazards are re-aimed by fixed increments. **The body must keep its yaw
  from 0 to 175**: no `face/*` in C3. The core runs no AI turning during a pattern, so this is just "do not add it".

## 2. AI

- **Bands:** melee ×2, mid ×2 (the beams cover r 2.7-6.1; a far player sees it as a gap).
- **Approach:** none. **Facing:** none (frozen yaw Y, the yaw at the pick: the idle has been tracking the player at
  4°/t, so the front faces roughly toward them).
- **Aim:** none at the player. The geometry is fixed to the body's yaw at 0 and the orbit.

## 3. Body travel

None.

## 4. Per-tick timeline

Positions in the beam frame: `rotated ~-90 0` (E) / `rotated ~90 0` (G) from the body, then `^ ^2.38 ^2.93` is the
muzzle (the medallion's face at `charge`..`off`) and `^ ^0.05 ^5.58` the floor spot. While firing use the hazard
marker's own yaw: `execute as <E> at <body> rotated as @s …`.

| t | rig | mechanics | fx (kit) | sound |
|---|---|---|---|---|
| 0 | core plays `laser`: medallions drop (0-4) | GRP_NEW; beam hazards E and G made (tell 25, act 133); tagged p3e / p3g | lanes: `K.tele_mline(0, 5.8, 0.6, 25, hold=133, back=-3.0)` rotated Y − 90, `K.tele_mline(1, …)` rotated Y + 90, at the floor under the body | `K.snd('pods_drop')` at the ring |
| 3 | | | `K.fx('pods_drop')` at each muzzle | |
| 4 | `charge` (medallions hot) | | `K.fx('laser_charge')` at each muzzle | `K.snd('laser_charge')` |
| 9, 14, 19 | | | `K.fx('laser_charge')` at each muzzle | `block.amethyst_block.chime` 0.4/1.8 at 14 |
| 23 | `aim` (beams extend) | | `K.fx('aim_line', len=3.74)` at each muzzle, rotated beam yaw / pitch 42 | `block.respawn_anchor.charge` 0.5/1.9 |
| **25** | **`fire`** | hazards strike (active 25-157); `hz_resize` to w 1.0 | `K.fx('laser_fire', len=3.74)` at each muzzle (muzzle ring + bloom 3 t) | `K.snd('laser_fire')` |
| 26-157, every tick | orbit 5°/t | E: `hz/aim` +5°, G: `hz/aim` −5°; then `K.tele_mline_aim(0/1)` rotated as each | | |
| 28 | | `hz_resize` both to w 0.6 | | |
| 25, 28, 31, … (every 3 t) | | | `K.fx('laser_spot')` at each floor spot (ambient) | |
| 25, 35, … 155 (every 10 t) | | | | `K.snd('laser_loop')` at E's spot (even tens) / G's spot (odd tens) |
| 43, 115 (front meet), 79, 151 (back meet) | | | `K.fx('spark')` at the meeting spot | `block.amethyst_block.resonate` 0.4/1.6 |
| **158** | `off` (beams off 158-160) | hazards already expired (last active 157); kill p3e / p3g | `K.fx('laser_end')` at each muzzle (beam yaw); `K.tele_mline_end(0)`, `K.tele_mline_end(1)` | `K.snd('laser_stop')` |
| 159-175 | `retract`, re-dock | | | `block.piston.contract` 0.6/0.9 at 166 |
| 175 | → `idle_cruise` | `g.end()` | | |

## 5. Damage areas

```
# at 0, as the body (rotated as the body = Y; no turning afterwards)
g.GRP_NEW,
*g.hz_opts(act=133, y0=-0.5, y1=2.0, kb=KB['light'], grp=True, rearm=10, sfx=0, quiet=1, vis=31),
'execute rotated as @s rotated ~-90 0 positioned ^ ^ ^3.0 run ' + g.hz_line(2.8, 0.6, 25, DMG['c3']),
g.tag_last_hz('rlk_mb_fg_p3e'),
*g.hz_opts(act=133, y0=-0.5, y1=2.0, kb=KB['light'], grp=True, rearm=10, sfx=0, quiet=1, vis=31),
'execute rotated as @s rotated ~90 0 positioned ^ ^ ^3.0 run ' + g.hz_line(2.8, 0.6, 25, DMG['c3']),
g.tag_last_hz('rlk_mb_fg_p3g'),
# 25: bloom; 28: sustained
f'execute as {E} run ' + g.hz_resize(2.8, 0, 1.0), f'execute as {G} run ' + g.hz_resize(2.8, 0, 1.0)     # at 25
f'execute as {E} run ' + g.hz_resize(2.8, 0, 0.6), f'execute as {G} run ' + g.hz_resize(2.8, 0, 0.6)     # at 28
# every tick 26..157 (extra_tick, before hz/all)
f'execute as {E} at {BODY} rotated as @s rotated ~5 0 positioned ^ ^ ^3.0 run function rlk:mboss/hz/aim'
f'execute as {G} at {BODY} rotated as @s rotated ~-5 0 positioned ^ ^ ^3.0 run function rlk:mboss/hz/aim'
f'execute as {E} at {BODY} rotated as @s run ' + K.tele_mline_aim(0)
f'execute as {G} at {BODY} rotated as @s run ' + K.tele_mline_aim(1)
```

- **Shape:** two lines from r 3.0 to 5.8 along their yaws (padded: r 2.7-6.1, half-width 0.6 incl. pad; 0.8 during the
  bloom). Height −0.5..2.0 (the beam's body-height part; a vanilla jump does not clear it). Active 25-157 (133 t).
  KB light 2 (0.3 b). Geo, 0.5.
- **Group + re-arm:** one group for both beams, `#hzRearm 10`. After a hit (or a dash-dodged hit) both beams are
  harmless for 10 t of the hazard clock. So a player can never take more than one hit per 10 t, even where the
  spots cross.
- **Sync rule:** at clip tick t, E's yaw = Y − 90 + 5(t − 25), G's = Y + 90 − 5(t − 25). Generate the increment sign
  from the manifest's `orbit.medal_eye.sense` (−1 → +5 yaw) and `orbit.medal_gear.sense` (+1 → −5 yaw), and the start
  azimuths from `az0`, so a rig change follows. If the manifest has no `orbit` (the stub), use these defaults.

## 6. Telegraphs

- **25 t before the first hit:** the medallions drop (0-4), the spark charge on both (4-23), the aim lines (23), and
  the two Geo lanes. Each lane covers r 3.0-5.8 at its beam's start yaw; it fills by 25 and then stays in the flash
  colour while it turns with its beam (`hold` 133).
- **During firing** the rig's gold beams and the floor spots are the read. The lanes keep marking the hit band on the
  floor, so the safe inside (r < 2.7) and outside (r > 6.1) stay obvious.
- The meets in front (43, 115) and behind (79, 151) are the moments to cross.

## 7. Projectiles

None. The beams are the rig's `beam_l` / `beam_r` parts (gold `beamLook`). The kit's `prop/laser_core` /
`laser_glow` are not needed with the real rig, so keep them only for the stub rig if wanted.

## 8. FX detail

- `pods_drop` ×2 (3), `laser_charge` ×2 at 4 / 9 / 14 / 19 (5 cards each), `aim_line` ×2 (23), `laser_fire` ×2 (25,
  3 cards each), `laser_spot` ×2 every 3 t (ambient: skipped when 40+ fx cards live), `spark` at the four meets,
  `laser_end` ×2 (158).
- Peak fx cards about 24 (kit budget table). Telegraph cards: 2 lanes × 5 = 10.

## 9. Sound

From v1 §6: clank at the drop; a bright rising whine (centroid 5.5 kHz) during the charge; a hissing roar at fire; a
hum + crackle loop; a power-down.

| tick | sound |
|---|---|
| 0 | `snd/pods_drop` |
| 4 | `snd/laser_charge` |
| 14 | `block.amethyst_block.chime` 0.4/1.8 |
| 23 | `block.respawn_anchor.charge` 0.5/1.9 |
| 25 | `snd/laser_fire` |
| 25 + 10k | `snd/laser_loop` at a spot |
| meets | `block.amethyst_block.resonate` 0.4/1.6 |
| 158 | `snd/laser_stop` |
| 166 | `block.piston.contract` 0.6/0.9 |

## 10. Dodge windows

- **Safe zones:** r < 2.7 (under the medallions: the husk keeps the player out of about r 0.75, so 0.75-2.7) and
  r > 6.1.
  - A melee player within 2.7 b keeps hitting the device the whole time; that is the intended answer.
  - A mid-band player steps out past 6.1 b.
- **Crossing the band (3.4 b wide):**
  - walk 15 t, sprint 12 t, half-speed 31 t;
  - a spot moves at 0.49 b/t along r 5.58 (0.39 b/t at r 4.5);
  - cross right after a beam passes your angle: the next one comes from the other side, at least 18 t later on the
    meeting line, longer elsewhere.
- **Standing in the band:** each beam passes a fixed angle once per 72 t, about 3 t of contact per pass (band
  1.2 b / 0.39 b/t). That is about 4 passes in 133 t: **about 4 hits (2.0)**, never two within 10 t.
- **Jump:** no (vanilla apex 1.25 < 2.0).
- **Dash:** 6 t of i-frames cover one pass; a dash-dodged hit also starts the 10 t re-arm. No C3 hit ignores the
  i-frames.

## 11. Diagram (top view, the device faces up)

```
                     front (yaw Y)
                 t43 / t115: spots meet
                         .
          E (eye) .-'    ^    '-. G (gear)
     t25 az+90  /   r 3.0 .. 5.8  \  t25 az-90
       ---> E  |   [ medallions ]  |  G <---      E turns +5 deg/t (clockwise)
               |   safe r < 2.7    |              G turns -5 deg/t
                \                 /
                 '-.    .    .-'
                     t79 / t151: meet behind
         safe outside r 6.1; one hit per 10 t at most (0.5)
```

## 12. Implementation sketch

Rework the stub `laser()`:
- start yaws `~-90` / `~90` (F1), r0 3.0, length 2.8, width 0.6 (F3);
- the re-aim window 26..157 in `extra_tick`, with the lane re-aim right after `hz/aim`;
- resize at 25 → 1.0 and at 28 → 0.6 (F2);
- the kit timeline above;
- cancel: kill p3e / p3g, `K.tele_mline_end(0)`, `K.tele_mline_end(1)`.

Read `orbit` from the manifest in `api.py`, or derive it in `cruise.py` (`api.CLIPS` keeps only id / len / loop /
next / events, so add `orbit` to the clip table or read `_MAN` once).

## 13. Checks

- Two hazards made at 0: tell 25 (= `ev('laser','fire')`), act 133, one group, re-arm 10, y −0.5..2.0, r0 3.0,
  length 2.8.
- At t = 43 both hazard yaws equal the body yaw (front meet). At t = 79 they equal Y + 180. In general E = Y − 90 + 5(t − 25).
- Width 1.0 on 25-27, 0.6 from 28.
- A player at r 4.5 standing still: every hit ≥ 10 t apart, ≤ 5 hits, all 50 Geo, the first ≥ 25.
- A player at r 2.0 or r 6.5: no hit.
- The body yaw is unchanged from 0 to 175.
