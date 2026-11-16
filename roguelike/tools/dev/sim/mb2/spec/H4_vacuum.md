# H4 광폭한 진공 (Raging Vacuum): implementation spec

| field | value |
|---|---|
| pattern | id 4, key `vacuum`, form human, kind normal |
| clip | `vacuum`, 41 t |
| events | crouch 0, glint 9, blade 17, backflip 17, land 38 |
| proposed extra event | `stomp` 16 |
| lead | 0 |
| element | Dendro (7) |
| coefficient | 1.2 (`DMG['h4']` 120) |
| hits | 1 (one blade prop) |
| recover | 18 t |

## 1. Footage and plan check

Sources: v2 B1 12.80-16.60 s and B2 22.62-23.70 s, both real time (`understand/v2.md` §2 B1/B2). Tick 0 = the crouch (13.20 s).

| event | footage tick (B1) | B2 | plan / rig | verdict |
|---|---|---|---|---|
| wind-up: low cat-like crouch, the kicking leg glows | 0-8 | — | crouch 0-9 | ok |
| **tell**: green flame spike behind her + horizontal cyan-white glint with a 4-point flare at the foot | 9.4-11 | (glint) | glint 9 | ok |
| rear-up: hops back a little, leg raised high | 12-14.6 | +2 after the glint | — | |
| stomp into the ground: yellow-green flame flare, about 1 m | 16-17.4 | +5 | — | fx at 16 |
| blade spawns, rising out of the ground | 18.6 | +7 | **blade 17** | Launch at 17 (plan). The visual rises over t17-19 while it already moves: about 2 t early, accepted. |
| blade at full size (4 m tall, 3 m across, 0.5 m thick); she backflips | 20-22.6 | +8 | backflip 17 | ok |
| blade travels straight, 0.7 b/t, no homing, rock debris + dark scar line | 22.6-29+ | — | 0.7 b/t | ok |
| backflip apex 2.5-3 b up, 2-3 b back | 30-32 | — | — | |
| lands | 41 | (none: into the transform) | land 38, clip 41 | ok (crouch 38-41) |

- No conflicts with the plan beyond the 1-2 t blade rise.
- The lock: the stub locks the line at t7 (= 17 - 10). The footage's aim read is the glint at t9.
- **Proposed:** lock at **t9** (the glint). The ground line telegraph appears at t9, The blade spawns 1 b ahead at t17 and flies 0.75 b/t; its 0.65 b hit spheres touch about 0.6 b early. It therefore reaches a player at 4 b at about **t20-21 (11-12 t of warning)** and at 8 b at about **t26 (17 t)**.

## 2. AI

- **Bands and weights:** far ×2, mid ×1. Plan: never melee.
  - Not melee: at d < 3.5 b the blade arrives < 10 t after the glint. A melee variant would need the lock at t7 (the stub's) and a 2-t later launch (Q13).
- **Approach:** none. She keeps her spot; idle locomotion keeps 2.2-8.5 b.
- **Facing:**
  - t0: `face/player`.
  - t0..8: `face/track`.
  - **t9 lock**: `face/player`, then held to the end (the backflip goes straight back along the locked line).
- **Aim lock at t9:** her yaw toward the player's feet at t9. The blade flies along that yaw with pitch 0.

## 3. Body travel

| ticks | travel |
|---|---|
| 0-12 | none |
| 12-14 | rear-up: 0.3 b back (`mv/away {d:0.1}` ×3) |
| 17-34 | backflip: 2.5 b back (`mv/away {d:0.15}` each tick) |
| 35-41 | none (landing crouch) |

## 4. Per-tick timeline

| t | rig | mechanics | fx | sound |
|---|---|---|---|---|
| 0 | crouch | `face/player` | | `block.moss_carpet.step` 0.4/0.9 |
| 0-8 | leg glows | `face/track` | `dust #E2FC88 0.8` ×2 at foot_r every 2 t; `dust #C9F2AD 0.6` ×1 rising | |
| **9** | **glint** | **lock yaw; line telegraph** (`tell_line(30, 3.0, 8)`, outline only) | flame spike behind her `tc:flame #C9F2AD 1.0→2.6 l6/f3` at ^ ^0 ^-0.6 (pivot at the base); glint line `tc:slash #F6FDE0 2.0→3.0 l4/f2` at ^ ^0.4 ^0.8, rot = yaw + 90 (horizontal, across); flare `tc:star #FFFFFF 0.3→1.2 l4/f2 bb center` at foot_r; lane decal (kit) 3 wide from S along the yaw to the arena edge, lime, scrolling chevrons toward the far end | `block.amethyst_cluster.hit` 0.7/1.8, `block.note_block.chime` 0.35/2.0 |
| 12-14 | rear-up | away 0.1/t | `poof` ×2 at the feet at t12 | `entity.breeze.jump` 0.4/1.0 at t13 |
| **16** | stomp | | ground flare `tc:burst #E2FC88 0.6→2.0 l4/f2 rot ~ 90` at ^ ^0.08 ^1.0; `tc:flame #FBFDE1 0.4→1.2 l4/f2` at ^ ^0 ^1.0; rock debris `block{block_state:"minecraft:mossy_cobblestone"}` ×8 Δ(0.4,0.2,0.4) speed 0.2 | `entity.breeze.wind_burst` 0.8/1.0, `block.big_dripleaf.tilt_down` 0.6/1.0 |
| **17** | blade, backflip | **blade prop summoned at ^0 ^0.9 ^1.0, yaw locked, pitch 0; `pj_launch(0.7, 60, 120, 1.5)` with shape 1 (blade)** | blade visual scale 0.3→1.0 over 3 t (interpolation); §7 | `item.trident.riptide_2` 0.7/1.2, `block.azalea_leaves.break` 0.6/0.9 |
| 17-34 | backflip | away 0.15/t | motes `dust #C9F2AD 0.7` ×1 at the core anchor every 2 t | `item.trident.riptide_1` 0.3/1.6 at 20 |
| 18+ (per blade tick) | | the blade flies (framework `pj`) | trail (§7 B) every tick; floor scar every 2 t | at the blade: `entity.phantom.swoop` 0.5/1.4 at t19; `entity.breeze.idle_air` 0.4/1.0 at t23; `block.grass.break` 0.5/1.0 every 4 t |
| wall / life | | `pj_end` event 1 or 2 → the blade shatters | `tc:burst #D6F7B9 1.0→3.0 l4/f2 bb center` + `tc:shard #A9E97D` ×5 at the blade | `block.amethyst_cluster.break` 0.6/1.2, `entity.breeze.wind_burst` 0.4/1.4 |
| 38 | land | | `poof` ×6, moss block ×8 | `entity.breeze.land` 0.6/0.9, `block.moss.fall` 0.5/1.0 |
| 41 | end | `g.end()`: the pattern ends; a still-flying blade lives on (it is a `pj` prop with `rlk_mb_aux`) | | |

## 5. Damage area: a projectile (the blade)

| property | value |
|---|---|
| count | 1 |
| spawn | at t17 at ^0 ^0.9 ^1.0 of her body: on her centre line, 1 b ahead. The `pj` hit rows sit 0.9 b below the prop (floor) and 0.3 b above it. |
| direction | the yaw locked at t9, pitch 0 |
| speed | 0.7 b/t (`spd` 7 tenths: 3 sub-steps of 0.25 per tick, i.e. 0.75 b/t effective) |
| life | 60 t (reaches about 45 b, more than the arena diameter of 42); `#pjWall 1` stops it at the wall ring (event 1) |
| homing | none |
| hit shape | `#pjShape 1` blade: a line across the flight, half width `hr` 1.5 → **3.0 b wide**. Points at most 0.8 b apart in 2 rows (floor and +1.2 b), each a 0.65 b sphere against the player's feet. Swept every 0.25 b. A jump does not dodge it (the second row). |
| damage | 120 % of the base hit, Dendro (`#pjEl 7` or the default), `#pjKB 3` along the flight yaw |
| cap | one hit (`mbPjHit`). After a hit `#pjKeep 1`: it flies on harmlessly (it is a blade wave). Do not pop it. |
| ground marker | the lane decal from t9 (§6); the blade itself |

`pj_end` (id 4): events 1 and 2 shatter the blade (fx) with `#pjKeep 0`; event 4 sets `#pjKeep 1` and adds a hit spark at the player.

## 6. Telegraphs

- **Lane: t9 → the blade's arrival.** Arrival ≈ 17 + (d - 1 - 0.6)/0.75: about t20 at d 4 (11 t after the decal) and about t26 at d 8 (17 t).
  - The framework `tell_line(30, 3.0, 8)` (outline; its harmless strike flash at t17 coincides with the launch).
  - Plus the kit's lane decal: 3.0 wide, from S to the wall along the locked yaw, lime `#B6E35A`, with forward chevrons that scroll every 2 t until the blade has passed (kill it at the blade's end).
- The glint and flame spike (t9), the rear-up (t12) and the stomp (t16) are the readable sequence.

## 7. FX detail

Palette (v2 §4):
- blade `#A9E97D` / `#64BC56`, dark core `#1E545F` / `#3B7F77`, edge `#D6F7B9` → `#F6FDE0`;
- stomp flare `#FBFDE1` / `#E2FC88` / `#C9F2AD`;
- scar `#2F5A3A`.

### A. Blade prop

An `item_display` carrying the fx kit's **`vblade`** model: a vertical crescent wall 3 b across × 4 b tall, its face perpendicular to the flight, with leaf-blade spikes along the edge.
- Layers: dark teal core `#1E545F`, body `#A9E97D` → `#64BC56`, bright rim `#D6F7B9`.
- `brightness 15`, `billboard fixed`, `teleport_duration 1`.
- Transformation: translation (0, 1.1, 0), so its base sits on the floor while the prop is 0.9 b up. Scale 0.3 → 1.0 over 3 t at spawn (`interpolation_duration 3`).
- **Until the kit has `vblade`:** use `tc:moon` geometry in a prop (face card 3×4 via non-uniform scale [3,4,1]), tinted `#A9E97D`, plus a second card `#1E545F` 0.05 b behind it. The stage-1 glass pane is a placeholder only.

### B. Trail (every tick while flying)

- `dust #64BC56 1.4` ×3 Δ(1.3,0.2,0.1) at the blade base.
- `dust_color_transition #F6FDE0→#64BC56 1.0` ×2 at the blade top.
- Every 2 t, a scar on the floor behind the blade: `dust #2F5A3A 1.6` ×4 on its centre line, lasting about 1 s.
- Every 4 t: `block{block_state:"minecraft:mossy_cobblestone"}` ×2 and `tc:leaf #A9E97D` ×2 thrown up and forward (`move` (0,1.2,1.5), l10/f5).

## 8. Sound

Taken from v2 §6:
- glint 13.75 s (high +10);
- hop 13.94;
- stomp and blade 14.00-14.47 (whoosh + leafy roar);
- travel 14.33-14.76 (hiss, low thump when it passes);
- landing 15.16.

Notes:
- The blade sounds play at the blade's position (`execute at <blade> run …`), so their direction tells the player where it is.
- Not yet used in the pack: `block.grass.break`, `entity.breeze.idle_air`, `block.moss.fall`, `block.moss_carpet.step`.

## 9. Dodge window and fairness

- **Sidestep:** leave the 3.0-wide lane, i.e. 1.5 + 0.3 = 1.8 b, possible from t9.
  - At d 4 the time available is about 11 t (walk 2.4 b, sprint 3.1 b).
  - At d 8 it is about 17 t.
  - Easy for a player who reads the glint.
- **Dash through the blade:** press when it is 1-2 b away (i-frames 6 t; the blade crosses the player in about 2 t).
- **Jump:** no (two-row blade).
- **At r 21:** the blade runs to the wall. A player pinned at the wall on the line still has the whole sideways room. The lane is never wider than 3 b, so there is no trap.

## 10. Diagram

```
 t9 lock (glint)                         t17 launch, 0.75 b/t, 3 b wide, to the wall
  wall |                                                                   | wall
       |   S(backflips 2.5 b back) <-  [blade]==> . . . . . P . . . . . . |
       |   ==================== lane decal 3.0 b ======================== |
                                        sidestep 1.8 b ↑↓
```

## 11. Implementation sketch (`human.py`)

```python
H4_GLINT, H4_STOMP = ev_or('vacuum', 'glint', 9), ev_or('vacuum', 'stomp', 16)
tl.at(H4_GLINT, R('face/player'), g.hz_opts(sfx=0),
      f'execute rotated as @s rotated ~ 0 positioned ~ {CY} ~ run ' + g.tell_line(30.0, 3.0, H4_BLADE - H4_GLINT), <lane decal>, <fx>, <snd>)
tl.at(H4_BLADE,
      f'execute rotated as @s rotated ~ 0 positioned ^ ^0.9 ^1.0 run summon minecraft:item_display ~ ~ ~ {{Tags:[...,"rlk_mb_bf_p4b"],'
      'teleport_duration:1,interpolation_duration:3,brightness:{block:15,sky:15},item:{id:"minecraft:paper",count:1,'
      'components:{"minecraft:item_model":"rlk:mboss/bf_fx/vblade"}},transformation:{...scale:[0.3f,0.3f,0.3f]}}',
      f'execute rotated as @s rotated ~ 0 positioned ^ ^0.9 ^1.0 run tp @e[tag=rlk_mb_bf_p4b,limit=1] ~ ~ ~ ~ 0',
      'scoreboard players set @e[tag=rlk_mb_bf_p4b] mbId 4',
      *g.pj_opts(shape=1, kb=KB['default'], wall=1),
      'execute as @e[tag=rlk_mb_bf_p4b,limit=1] at @s run ' + g.pj_launch(0.7, 60, DMG['h4'], 1.5))
tl.at(H4_BLADE + 1, 'data merge entity @e[tag=rlk_mb_bf_p4b,limit=1] {start_interpolation:0,transformation:{scale:[1f,1f,1f],translation:[0f,1.1f,0f]}}')
```

Add a `p/vacuum/pj_end` for the shatter fx. The blade's own per-tick fx come from a `p/vacuum/blade` tick, run from the pattern tick and, after `g.end()`, from a module-level "live blade" check: `execute if entity @e[tag=rlk_mb_bf_p4b]` in the core tick (see Q14). Cancel kills `rlk_mb_bf_p4`.

## 12. Checks

- The blade speed effective 0.75 b/t.
- A player 1.9 b off the line is untouched.
- A player on the line is hit once.
- A jump does not avoid it.
- The wall stops it and plays the shatter.
- The lane decal exists from t9.
- Tell ≥ 10 t before the earliest hit in the bands: about t20 at 4 b (mid band minimum).
