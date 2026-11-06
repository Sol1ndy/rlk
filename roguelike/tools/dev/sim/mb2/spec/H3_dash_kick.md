# H3 달빛 돌진 (Moonlit Rush): implementation spec

| field | value |
|---|---|
| pattern | id 3, key `dash`, form human, kind normal |
| clip | `dash_kick`, 50 t, events `charge` 0, `dash` 10, `kick` 15 |
| proposed extra events | `dash_end` 12, `ring` 19 |
| lead | 0 |
| close-in | none (it is the gap closer) |
| element | Dendro (7) |
| coefficient | 1.3 (`DMG['h3']` 130), for the kick and the ring together |
| hits | 1 (one volley group), at most 1.3 |
| recover | 16 t |

## 1. Footage and plan check

Source: v2 2.95-6.47 s, real time (`understand/v2.md` §2 A). Tick 0 = the charge start (4.00 s).

| event | footage tick | plan / rig | verdict |
|---|---|---|---|
| charge: yellow-green motes rise and swirl in; faint floor glow r 1.5-2 | 0-8 | charge 0-10 | ok |
| coil: side-on, leg cocked, crescent plate swept back | 8-10 | — | |
| **dash**, about 5 m in about 0.1 s | 10-12 | dash 10-12 | ok |
| kick: high side kick, navy blade plate on the shin | 12.6-14 | — | |
| **hit flash**: diagonal slash streak, 4 m × 1 m | 14.6 | kick 15 | ok |
| burst: white-yellow, radial spikes | 16-18 | — | fx |
| **all-around slash ring** r 3-3.5 m, ground to about 2 m | **18.6-22** | (plan: the ring at 15) | **mismatch: 4 t later** |
| fade, wisps rise | 22-26 | — | |
| recovery, re-faces | 26-50 | total 50 | ok |

**Fix:** split the hit. A kick sphere at t15 (r 1.5 at the foot, as in the footage) and the ring at **t19** (r 3.5), both in one volley group so the plan's single 1.3 hit is kept. Add the rig event `ring` 19, or use `ev_or('dash_kick','ring',19)`.

## 2. AI

- **Bands and weights:** mid ×1, far ×2. Never melee: at melee range H1 and H2 cover her.
- **Approach:** none. In the far band she dashes at most 7 b, so a player 12 b away sees her close the gap and the ring miss (intended).
- **Facing:**
  - t0: `face/player`.
  - t0..3: `face/track`.
  - **t3 lock**, then held through the recovery (t26 `face/track` resumes so she re-faces by t30).
- **Aim lock at t3:** `g.dest(7.0, 1.5)`, giving marker D: on the line to the player, ≤ 7 b from her, 1.5 b short of the player (safe-disc clamped). The kick and the ring are anchored at D.

## 3. Body travel

| ticks | travel |
|---|---|
| 0-9 | none (a slight crouch, rig) |
| 10-11 | glide S → D in 2 t (`mv/glide {t:2}` at t10), 2.5-3.5 b/t |
| 12-50 | none |

## 4. Per-tick timeline

| t | rig | mechanics | fx | sound |
|---|---|---|---|---|
| 0 | charge | `face/player` | floor glow `tc:glow #C7DB75 1.0→3.5 l12/f3 rot ~ 90` at ^ ^0.06 ^0 | `entity.breeze.charge` 0.6/1.4, `block.azalea_leaves.break` 0.35/1.6 |
| 0-9 | | | motes: `dust #C7DB75 0.6` ×3 Δ(0.9,0.9,0.9) at ^ ^1.0 ^0, and `end_rod` ×1 Δ(0.8,0.6,0.8) speed 0.02, every tick. From t5 the motes converge: `dust #E6F6F8 0.5` on a ring of r = 1.6 - 0.15·(t-5), y 1.2, ×6 | `block.amethyst_block.chime` 0.3 at t2/4/6/8 with pitch 1.6/1.7/1.8/1.9 |
| **3** | | **lock D; kick hazard (tell 12) + ring hazard (tell 16), group G** | decals: kick disc r 1.5 at D + 1.2·aim; ring disc r 3.5 at D; dash lane 0.8 wide from S to D; tell cue | `block.amethyst_block.resonate` 0.35/1.6 |
| 5 | | | | `block.azalea_leaves.break` 0.3/1.7 |
| 8 | coil | | shin plate glint `tc:star #F0FEF6 0.3→1.0 l4/f2 bb center` at foot_r | |
| **10** | dash | glide → D (2 t) | afterimage `tc:glow #B2FBDD 1.2→0.4 l4/f2 bb center` at ^ ^1.2 ^0 (start point); path streak `tc:slash #B2FBDD L→L l4/f2` with L = path length, centred halfway at ^ ^1.0 ^L/2 (fixed, rot = yaw). Use 3 cards at 1/4, 2/4 and 3/4 of the path, s 2.5 each, if L is not known at build time. | `entity.breeze.jump` 0.7/1.3, `item.trident.riptide_1` 0.4/1.5 |
| 12 | kick chambers | | | |
| 14 | | | hit flash: diagonal `tc:slash #F0FEF6 3.0→4.0 l3/f1 roll 35` at ^ ^1.6 ^1.0 | `entity.player.attack.sweep` 0.5/1.2 |
| **15** | **kick** | **kick strike (group G)** | `tc:burst #F9FDE0 1.0→4.0 l4/f2 bb center` at ^ ^1.4 ^1.2; `flash{color:[0.98,0.99,0.88,0.9]}` ×1 | `entity.breeze.wind_burst` 0.8/1.0, `item.mace.smash_ground` 0.6/1.3, `entity.player.attack.strong` 0.5/1.2 |
| 16-17 | | | burst spikes: `tc:shard #EAFDB2 0.6→1.5 l5/f2` ×6 radial at ^ ^1.4 ^1.2, rot `~60k -20` | `block.cherry_leaves.break` 0.7/1.0 at 17 |
| 18 | | | | `entity.player.attack.sweep` 0.8/0.7 (the ring whoosh leads) |
| **19** | ring slash | **ring strike (group G)** | ring (§7) | `block.cherry_leaves.break` 0.7/1.1, `block.azalea.break` 0.6/1.0 |
| 20-22 | | | ring continues (second spin card at t20); shards fly out | `block.cherry_leaves.break` 0.5/1.2 at 21 |
| 22-26 | fade | | wisps: `dust #B6F392 0.9` ×3 Δ(1.5,0.3,1.5) rising (`end_rod` ×1) every 2 t; `tc:leaf #A9ED97` ×3 at t23 | |
| 26-50 | recovery | `face/track` from 26 | | |
| 50 | end | `g.end()` | | |

## 5. Damage areas (volley group G, made at t3 after `g.GRP_NEW`)

1. **Kick.** `hz_opts(grp=True, kb=3, sfx=0)`, then at D facing the player, `positioned ^ ^ ^1.2`: `hz_disc(1.5, 12, 130)`. A disc of r 1.5 centred 1.2 b past D toward the player, height -0.5..3.5. Strike t15.
2. **Ring.** `hz_opts(grp=True, kb=3, sfx=0, act=3)`, then at D: `hz_disc(3.5, 16, 130)`. A filled disc of r 3.5 around D, active t19-21.
3. **Dash lane (telegraph only).** `hz_opts(sfx=0)` + `g.tell_line(len=|SD|, 0.8, 7)` at S aimed at D. If `|SD|` is only known at runtime, use the kit's lane decal stretched to D, or a fixed `tell_line(7.0, 0.8, 7)`, which overshoots harmlessly. **dmg 0.**

At most one hit (G): whichever lands first. Dendro, 1.3, KB 3 (away from D).

## 6. Telegraphs

- Kick: 12 t (t3 → 15). Ring: 16 t (t3 → 19). Both decals appear at t3.
  - The ring fill grows from 0 → r 3.5 over 16 t.
  - The kick disc fill grows over 12 t, brighter rim.
  - The dash lane shows her path.
- Earlier read: the mote charge from t0, plus the floor glow under her.

## 7. FX detail

Palette (v2 §4):
- slash core `#F0FEF6`, light `#B2FBDD`, mid `#5DE1B7`, edge `#2C898F`;
- burst `#F9FDE0` / `#EAFDB2` / `#A2ECA3`;
- ring `#D3FAB9` / `#B6F392`, saturated `#74E542`, rim `#E1F0A0`;
- motes `#C7DB75` / `#E6F6F8`.

**Ring (t19-22):** a horizontal spiral or crescent slash around her, r 3.5, thin bright rim arcs, leaf-blade shards flung out.
- Underlay `tc:crescent #2C898F 6.6→7.2 l4/f2 spin 170` (flat) at ^ ^1.0 ^0.
- Overlay `tc:crescent #B6F392 6.4→7.0 l4/f2 spin 170` at ^ ^1.05 ^0.
- At t20 the same pair with yaw +180 (full circle).
- Rim `tc:ring #E1F0A0 6.0→8.1 l5/f2 rot ~ 90` at ^ ^1.0 ^0 (ring radius 3.5 at s 8.1).
- Shards `tc:shard #74E542 0.8→1.6 l6/f3` ×8 at ^ ^1.0 ^0, rot `~45k -10`, `move` (0,0,2.0) (fly outward).
- `dust #D3FAB9 1.2` ×24 on a ring of r 3.3 at y 1.0.

## 8. Sound

Taken from v2 §6:
- charge rustle 4.09-4.52 s;
- lunge whoosh 4.50;
- kick boom 4.82-4.92 (low +14, high +15);
- crackle tail to 5.3.

`block.cherry_leaves.break` is not yet used in the pack (1.20+).

## 9. Dodge window and fairness

The player is about 1.5 b in front of D, and about 0.3 b from the kick disc centre.
- **Kick:** leave r 1.5 + 0.3, i.e. 1.8 b in 12 t (walk 2.6 b), easy. Sideways is best.
- **Ring:** leave r 3.5 + 0.3 = 3.8 from D. From 1.5 b that is 2.3 b in 16 t (walk 3.5 b), OK. Backward is best.
- Moving straight back escapes both, which teaches the read "back off when she charges".
- **Dash:**
  - A press at t10-t15 makes the kick (t15) miss.
  - Dashing *backward* at t13-t15 moves the player 3 b away from D, which also clears the ring (r 3.8) by distance.
  - A dash with no distance (i-frames only) cannot cover both the kick and the ring's act t19-21, which needs i-frames from 15 to 21, i.e. 7 t.
  - So the expert answer is a backward dash on the kick; the easy answer is to walk back during the 12-16 t telegraph.
- Player at the wall (D clamped at r ≤ 19): moving sideways along the wall leaves r 3.8 in about 14 t of sprint. Fair.

## 10. Diagram

```
                       .  -  -  .
 S . . . dash lane . .D  kick(r1.5)o  P        (t3 lock: D = 1.5 b short of P, ≤ 7 b from S)
                     .   ring r3.5     .
                       '  -  -  '
 charge 0-10, dash 10-12, kick 15, ring 19 (one hit)
```

## 11. Implementation sketch (`human.py`)

```python
H3_RING = ev_or('dash_kick', 'ring', 19)
tl.at(3, R('face/player'), g.dest(7.0, 1.5), g.keep(a), g.GRP_NEW,
      g.hz_opts(grp=True, kb=KB['default'], sfx=0),
      f'execute at {A_} facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^1.2 positioned ~ {CY} ~ run '
      + g.hz_disc(1.5, H3_KICK - 3, DMG['h3']),
      g.hz_opts(grp=True, kb=KB['default'], sfx=0, act=3), f'execute at {A_} positioned ~ {CY} ~ run ' + g.hz_disc(3.5, H3_RING - 3, DMG['h3']),
      g.hz_opts(sfx=0), f'execute at @s facing entity {A_} feet rotated ~ 0 positioned ~ {CY} ~ run ' + g.tell_line(7.0, 0.8, 7))
tl.at(10, f'execute positioned as {A_} run function rlk:mboss/mv/glide {{t:2}}')
```

## 12. Checks

- One hit from G even when the player stands inside both discs.
- Kick tell 12, ring tell 16.
- No hit at all from the lane.
- The end position is within 0.5 b of D.
