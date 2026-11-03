# B1 우아한 날개 / 날개 치기 (Graceful Wing): implementation spec

| field | value |
|---|---|
| pattern | id 11, key `strike`, form butterfly, kind normal |
| clip | `wing_strike`, 55 t, events bank 0, dive 8, hit 15 |
| element | Dendro (7); the core switches the wings to the Dendro look before the start if needed (prep 8 t) |
| coefficient | 1.3 (`DMG['b1']` 130) |
| hits | 1 (one volley group of 2 hazards) |
| recover | 18 t |

## 1. Footage and plan check

Sources:
- v2 D, 35.20-37.92 s, real time (`understand/v2.md` §2 D). I re-checked `sheet_wingstrike_34.80-36.60.jpg`.
- The tail in v3 R (replay).

Tick 0 = hover facing the player (35.20 s); she starts 4-5 b away, feet about 1-1.5 b up.

| event | footage tick | plan / rig | verdict |
|---|---|---|---|
| lifts slightly, one big wing flap | 1-7 | bank 0-8 | ok |
| **bank**: rolls 70-90°, one wing sweeps down-forward | 8-11 | bank → dive 8 | ok |
| **dive / swoop**: drops low (0.5-1 b), body nearly horizontal, past the player's side, wings flat like blades | 12-14 | dive 8-11 (3 t) | ok |
| **HIT**: the wing edge sweeps through the player (6509 = 16.5 % max HP) | 14.7 | hit 15 | ok |
| ground slash band along the wing path, 6-8 m × 1 m | 16-19 | — | fx |
| trailing vertical crescent flare, 2-3 m | 19-22 | — | fx |
| climbs to 4-5 b | 20-28 | — | |
| flutters: rolls, turns, quick flaps | 28-48 | — | |
| back to hover facing the player at 5-6 b | 48-55 | total 55 | ok |

Areas:
- **Plan:** "front arc r 4, plus a ground slash band and a trailing crescent".
- **Footage:** the damage comes from the banked low wing sweeping horizontally across the player while she swoops past the player's side. The band marks her path.
- **Proposed:** a **lane** along her swoop path (10 × 3.5) **plus** the plan's arc (r 4, ±60°) centred at the lock point, in one group. The lane is the honest read ("her path"); the arc keeps the plan's front sweep.

**Bands:** not in the plan's table. The stub allows melee, mid and far. **Proposed: melee ×2, mid ×1, no far.** The dive is only 7 t, and she must reach the player.

Root travel: the rig bakes pos z -2.2 at the hit and -2.6 to the end (Q1). This spec moves the body.

## 2. AI

- **Bands and weights:** melee ×2, mid ×1.
- **Approach:** none beyond her idle glide (`ai/idle_b` keeps 5-8 b). The core's 8-t look prep runs only after a Pyro pattern.
- **Facing:**
  - t0: `face/player`.
  - t0..3: `face/track`.
  - **t3 lock**, held through the swoop.
  - t22..: `face/track` again (she turns back while climbing).
- **Aim lock at t3:**
  - L = `g.lockp()` (the player's floor point).
  - Aim yaw = S → L.
  - H = the swoop end point: L + 2.0 b along the aim + 1.2 b to her **right** (`positioned ^-1.2 ^ ^2.0` in the aim frame at L). She passes the player's left side, as in the footage, where she passes screen-left of the player.

## 3. Body travel

| ticks | travel |
|---|---|
| 0-7 | bank drift: 0.15 b/t toward L (`mv/toward {d:0.15}`); the rig carries the rise |
| 8-15 | dive: glide → H over 7 t (`execute positioned as H run function rlk:mboss/mv/glide {t:7}` at t8) |
| 16-27 | climb and glide on: 0.12 b/t along the aim (`mv/step {d:0.12}`) |
| 28-48 | flutter: small drift, `mv/away {d:0.06}` (stays ≥ 5 b) |
| 48-55 | settle |

The body stays on the floor; the rig carries the 0.5-1 b swoop height and the 4-5 b climb.

## 4. Per-tick timeline

| t | rig | mechanics | fx | sound |
|---|---|---|---|---|
| 0 | bank start (lift + flap) | `face/player` | | `entity.ender_dragon.flap` 0.5/1.8 at t1 |
| **3** | | **lock L, H; group G: lane + arc (tell 12)** | lane decal 10 × 3.5 from S along the aim; arc decal r 4, ±60° at L; tell cue | `block.amethyst_block.resonate` 0.35/1.6 |
| 6 | | | wing-tip motes `dust #E7FDAA 0.8` ×2 at fwtip_l / fwtip_r (every 2 t, t6-14) | |
| **8** | **dive** | glide → H (7 t) | | `entity.ender_dragon.flap` 0.6/1.5, `entity.phantom.swoop` 0.6/1.3 |
| 10-14 | swoop low | | streak behind her: `tc:slash #E7FDAA 2.5→3.0 l3/f1` at ^ ^0.8 ^-1.0 every tick, rot = aim | `entity.phantom.swoop` 0.5/1.6 at t12 |
| **15** | **hit** | **strike (G)** | wing arc (§7 A) | `entity.player.attack.sweep` 0.8/0.8, `entity.breeze.wind_burst` 0.7/1.1, `block.cherry_leaves.break` 0.8/1.0 |
| 16-19 | | | ground slash band (§7 B) | `item.trident.riptide_1` 0.5/1.6 at t16 |
| 19 | | | trailing vertical crescent (§7 C) | `entity.player.attack.sweep` 0.5/1.3, `block.azalea_leaves.break` 0.5/1.2 |
| 20-28 | climb | step 0.12/t | leaves `tc:leaf #D4FA88` ×2 at t21 and t25 (fall, `move` (0,-2,0), l16/f6); motes from the wing tips | `entity.ender_dragon.flap` 0.5/1.6 at t22 |
| 28-48 | flutter | | | `entity.phantom.flap` 0.4/1.4 at t32, t37, t44 |
| 50 | settle | | | `entity.phantom.flap` 0.3/1.6 |
| 55 | end | `g.end()` | | |

## 5. Damage area (group G, made at t3 after `g.GRP_NEW`; strike t15)

1. **Swoop lane.** At S, rotated toward L, on the floor: `hz_opts(grp=True, kb=3, sfx=0)` then `hz_line(10.0, 3.5, 12, 130)`.
   - A rectangle 0..10 b along the aim, ±1.75 b, height -0.5..3.5.
   - With d ≤ 8 b (the bands) it reaches at least 2 b past L.
2. **Wing arc.** At L, rotated along the aim: `hz_opts(grp=True, kb=3, sfx=0)` then `hz_sector(4.0, 60, 12, 130)`. A 120° sector of r 4 ahead of L, along the aim.
3. One hit total. Dendro, 1.3, KB 3 (along the aim yaw / away from the centre).

## 6. Telegraphs

- 12 t (t3 → t15). The lane fill sweeps from S toward the far end over 12 t (it shows the direction). The arc fills from L outward.
- Earlier reads: the bank (t0-8) and the wing raise.

## 7. FX detail

Palette (v2 §4, v3 §3 R):
- band `#E7FDAA` / `#D4FA88` / `#ADDE6D`;
- crescent `#E3FCB7` / `#80DE76`, dark `#23717A`;
- trail core `#D2FA8E` / `#9CDB7D`, teal underlay `#38896B`.

### A. Wing arc (t15)

The flat wing blade sweeping across.
- Underlay `tc:crescent #23717A 7.5→8.2 l4/f2` (flat, horizontal) at ^ ^0.8 ^0, rot = aim yaw, `spin -120`.
- Overlay `tc:crescent #D4FA88 7.2→8.0 l4/f2` at ^ ^0.85 ^0, same.
- At L: `tc:burst #E7FDAA 0.8→2.6 l4/f2 bb center` at L + (0,1,0); leaves `tc:leaf #ADDE6D` ×6 (l12/f6, `move` outward 1.5).

### B. Ground slash band (t16-19)

A long lime crescent trail along her path.
- 4 floor slashes `tc:slash #E7FDAA 2.5→3.0 l8/f4 rot <aim> 90` at S + (2, 4, 6, 8) b along the aim: two at t16, two at t17.
- Under each, `tc:slash #38896B 2.8→3.2 l8/f4` 0.02 b lower (teal underlay).
- `dust #ADDE6D 1.0` ×10 along the band at t18.

### C. Trailing vertical crescent (t19-22)

- `tc:crescent #80DE76 3.0→5.0 l6/f3 roll 90 spin 120` at H + (0,1.0,0), rot = aim.
- Underlay `#23717A` 0.1 b behind it.

## 8. Sound

Taken from v2 §6: flap 35.35 s, bank 35.69, hit 35.93-36.00 (mid +12), long swish 36.02-36.35, flaps 37.20 / 37.45 / 37.82.

`block.cherry_leaves.break` is not yet used in the pack.

## 9. Dodge window and fairness

- **Sidestep:** out of the 3.5 lane and away from the arc. From L, that is 1.75 + 0.3 = 2.05 b in 12 t. Walking gives 2.6 b, so OK.
  - Sideways to **her left** (the side away from H) is best: the arc is ahead of L.
- **Backward** (toward her): no. The lane covers the whole path.
- **Dash** at t10-15 (i-frames cover the strike at t15).
- **At r 21:** L and H are inside the safe disc. The lane may run into the wall beyond the player (harmless). Sidestepping is always available.

## 10. Diagram

```
                      . arc r4 ±60° .
  S ====================L===========H ==>     lane 10 x 3.5 from S (her swoop path)
  (bank 0-8, dive 8-15)  P(t3)        she passes P's left side 1.2 b, climbs away
```

## 11. Implementation sketch (`wing.py`)

```python
tl.at(3, R('face/player'), g.lockp(), g.keep(a, 'rlk_mb_bf_lock'),
      f'execute at {A_} facing entity @s feet rotated ~180 0 positioned ^-1.2 ^ ^2.0 run summon minecraft:marker ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","{h}"]}}',
      f'execute as {H_} run function rlk:mboss/mv/clamp', g.GRP_NEW,
      g.hz_opts(grp=True, kb=KB['default'], sfx=0), f'execute facing entity {A_} feet rotated ~ 0 positioned ~ {CY} ~ run ' + g.hz_line(10.0, 3.5, 12, DMG['b1']),
      g.hz_opts(grp=True, kb=KB['default'], sfx=0), f'execute at {A_} facing entity @s feet rotated ~180 0 positioned ~ {CY} ~ run ' + g.hz_sector(4.0, 60, 12, DMG['b1']))
tl.at(8, f'execute positioned as {H_} run function rlk:mboss/mv/glide {{t:7}}')
```

`facing entity @s feet rotated ~180 0` from L gives the aim direction S → L, because @s is the body.

## 12. Checks

- One hit max.
- Tell 12.
- A player 2.1 b off the lane centre line and outside the arc is not hit.
- The body ends near H, then drifts.
