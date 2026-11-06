# B3 날개 휩쓸개 / 날갯짓 (Wing Sweep): implementation spec

| field | value |
|---|---|
| pattern | id 13, key `sweep`, form butterfly, kind normal |
| clip | `flap_dive`, 59 t, events rise 0, dive 20, slam 26, fan 28, glide 33 |
| element | **Pyro (1)**; look switched in prep |
| coefficients | flame fan 1.6 (`DMG['b3']` 160); flame trail 0.3 per touch (`DMG['b3t']` 30), **max 2 touches** |
| hits | the fan 1 + the trail ≤ 2, at most 2.2 |
| recover | 18 t |

## 1. Footage and plan check

Source: v3 B, 10.70-14.60 s, real time (`understand/v3.md` §3 B). I re-checked `sheet_flap_pf_12.85-13.70.jpg` (the flame wall and the red trail line). Tick 0 = the wings raised (11.55 s); start distance 6-7 b.

| event | footage tick | plan / rig | verdict |
|---|---|---|---|
| tell 1: wings V-up, leans back | 0-6 | rise 0 | ok |
| big downstroke (span about 2.9 H) | 6-11 | | |
| upstroke | 11-15 | | |
| rises 0.5-1 b, wings high | 15-20 | rise 0-20 | ok |
| **dive**: head-first toward the player, 2-3 b (6 → 3-4 b away) | 21-25 | dive 20 (4 t) | ok |
| **wing slam**: two vertical flame crescents (1.5-2 b) at the wing tips | 26 | slam 26 | ok |
| flame sweeps along the floor toward the player | 27 | | fx |
| **flame eruption**: a 180° front fan of flame spikes, 2-3 m tall, reaching 4-5 m, past the player | **28-32** | fan 28-32, r 4.5, 2.5 tall | ok |
| embers; a red-orange scorched streak stays | 32-36 | | fx |
| **low glide 4-5 b to her RIGHT**, wings flat; red flame lines trail over the floor | 36-43 | glide 33 | ok in time. **Direction:** sideways, not forward; the rig bakes z -6 forward (Q1) |
| glides back to her idle spot (about 6 b from the player); one settling flap | 43-59 | total 59 | ok |

- Trail damage: "possibly damaging (not confirmed)" in the footage. The plan sets 0.3 per touch, max 2; **keep it** (Q11), with a 10 t ember telegraph.
- **Bands:** not in the plan table; the stub uses melee, mid and far. **Proposed: melee ×1, mid ×2, no far.** The fan reaches only 4.5 b past a slam point at most 3 b closer.

## 2. AI

- **Bands and weights:** melee ×1, mid ×2.
- **Approach:** the core's Pyro prep backs her to ≥ 6 b (`ai/prep`).
  - If the player is closer than 4 b at t16, P is just her current spot (`dest` max 0).
  - The fan still covers the player; dodge by going behind her.
- **Facing:**
  - t0: `face/player`.
  - t0..16: `face/track`.
  - **t16 lock**, held through the dive, the slam and the fan.
  - t43..: `face/track` while returning.
- **Aim lock at t16:**
  - P = `g.dest(3.0, 2.5)`, the slam point: up to 3 b toward the player, 2.5 b short of the player.
  - The aim yaw is toward the player's t16 position.

## 3. Body travel

| ticks | travel |
|---|---|
| 0-20 | none (the rig rises 0.5-1 b + the flaps) |
| 20-25 | glide S → P (`mv/glide {t:6}` at t20) |
| 26-32 | none (the slam, the eruption) |
| 33-42 | glide sideways to her right: 4.5 b over 10 t. Marker G = P + 4.5 b to her right (`positioned ^-4.5 ^ ^0` in the aim frame); `mv/glide {t:10}` at t33 |
| 43-59 | glide back toward a spot 6 b from the player: `mv/away {d:0.25}` while within 6 b, then hover |

## 4. Per-tick timeline

| t | rig | mechanics | fx | sound |
|---|---|---|---|---|
| 0 | wings V-up | `face/player` | wing-tip embers `flame` ×2 at fwtip_l / fwtip_r every 3 t until t20; Pyro rim glow `tc:glow #FAD77C 1.0→1.6 l20/f6 bb center` at the core anchor | `entity.ender_dragon.flap` 0.7/1.4 |
| 6 | downstroke 1 | | `small_flame` ×6 Δ(3,0.3,0.6) at ^ ^2.5 ^0 (wing sweep) | `entity.ender_dragon.flap` 0.8/1.2 |
| 13 | upstroke | | | `entity.ender_dragon.flap` 0.6/1.5 |
| **16** | rise | **lock P + aim; fan hazard (tell 12, act 5)** | fan decal: Pyro half disc r 4.5 at P (§6); tell cue | `item.firecharge.use` 0.35/1.6 |
| **20** | **dive** | glide → P (6 t) | flame trail from the wing tips: `dust #F88F39 1.2` ×2 per tick at hwtip_l / hwtip_r, t20-25 | `entity.phantom.swoop` 0.7/1.2 |
| **26** | **slam** | | two vertical flame crescents at the wing tips: `tc:flame #F8D486 0.8→2.0 l6/f3` at ^±1.7 ^0 ^0.8 (rot = aim), plus `tc:crescent #F09A5F 2.0→4.0 l5/f2 roll 90` at each | `entity.ender_dragon.flap` 0.8/0.9, `entity.generic.explode` 0.4/1.6 |
| 27 | | | flame sweeps along the floor: `tc:slash #F7CC9C 2.5→4.0 l4/f2 rot <aim> 90` at ^ ^0.06 ^1.5 / ^0.06 ^3.0 | |
| **28** | fan | **fan strike (act 28-32)** | eruption ring 1 (§7 A) | `entity.blaze.shoot` 0.9/0.8, `entity.ghast.shoot` 0.5/1.2, `block.fire.ambient` 0.9/1.0 |
| 29 | | | eruption ring 2 | |
| 30 | | | eruption ring 3 (outer) | `block.fire.ambient` 0.7/1.3, `entity.generic.explode` 0.3/0.7 |
| 32-36 | embers | | `dust #EDC30B 0.8` ×10 over the fan Δ(2.2,0.4,1.2) every 2 t; scorch `dust #585542 1.8` ×16 on the fan floor at t32; `campfire_cosy_smoke` ×3 at t33 | `entity.blaze.burn` 0.4/0.9 at 33 |
| **33** | glide | glide → G (10 t); **trail segment 1 at t34** | | `block.fire.ambient` 0.5/0.8 |
| 34, 36, 38, 40 | | **trail segments 1-4 (tell 10, act 8)** at her floor position | ember line (§7 B) | `block.fire.ambient` 0.4/1.1 at t36 |
| 44, 46, 48, 50 | | segment k flares (its strike, act 8) | flare (§7 B) | per flare: `block.fire.ambient` 0.5/1.6, `entity.generic.burn` 0.3/1.4 |
| 45, 50, 54 | return glide, settle flaps | away 0.25/t while within 6 b | | `entity.ender_dragon.flap` 0.4/1.6 at 45 / `entity.phantom.flap` 0.4/1.5 at 50 and 54 |
| 59 | end | `g.end()` (the trail segments are framework hazards and run out by themselves, last at t58) | | |

## 5. Damage areas

### Flame fan (made at t16; strike t28, active 28-32)

- At P, rotated along the aim, on the floor: `hz_opts(el=1, act=5, y1=2.5, kb=3, sfx=0)`, then `hz_sector(4.5, 90, 12, 160)`.
- **Shape:** a half disc of r 4.5 in front of P (180°), height -0.5..2.5 b, active 5 ticks.
- Pyro, 1.6, KB 3 (away from P). One hit.

### Flame trail (4 segments; 2 groups)

- Segment k at her floor position at t = 34, 36, 38, 40:
  - `hz_opts(el=1, kb=0, act=8, sfx=0, grp=True)`, then `hz_disc(1.0, 10, 30)`.
  - **Shape:** a disc of r 1.0, height -0.5..3.5, strike at t+10, active 8 ticks.
- Groups:
  - `GRP_NEW` before segment 1 → group T1 = segments 1-2;
  - `GRP_NEW` before segment 3 → group T2 = segments 3-4.
- **At most 2 trail touches** in total (one per group). Pyro, 0.3 each, KB 0.
- Burning: a Pyro trail touch on a Dendro-marked player (from B1, B4 or a human kick) starts the native Burning on the player. That is intended: the footage's "연소를 활용한 강력한 공격".

## 6. Telegraphs

- **Fan: 12 t (t16 → t28).**
  - Pyro half-disc decal at P: fill `#FF8A3D` growing from P outward to r 4.5, rim `#FAD77C`, the straight edge (behind P) drawn brighter so "behind her = safe" reads.
  - Earlier reads: the two big flaps and the rise (t0-20).
- **Trail: 10 t per segment.**
  - The segment appears as a line of dark embers on the floor (`dust #8C5436` + `#EDC30B` sparks), then flares with flame.
  - The kit decal: a thin ember ring r 1.0, `#E04040` → `#F06A30`.

## 7. FX detail

Palette (v3 §5):
- flame wall `#F09A5F` / `#F7CC9C`, dark `#8C5436`, edge `#A46076`, saturated `#F88F39`;
- scorch `#585542`, ember `#EDC30B`;
- trail red `#E04040` / `#F06A30`.

### A. Flame eruption (t28-30)

A 180° fan of flame spikes rising from the floor; she stands in its centre.
- The kit's **`spike`** (a tall flame shard, pivot at the base), or `tc:flame`.
- 13 cards on 3 arcs in front of P, angles across -80..+80° (rot = aim + angle):
  - t28: inner arc r 1.5, 4 cards, `s 0.8→2.2 l7/f3`, `#F7CC9C`;
  - t29: middle arc r 3.0, 5 cards, `s 0.8→2.8 l7/f3`, `#F09A5F`;
  - t30: outer arc r 4.3, 4 cards, `s 0.8→2.5 l6/f3`, `#F88F39`.
- `flame` ×30 Δ(2.5,0.8,1.5) speed 0.04 at ^ ^0.8 ^2.0 (aim frame).
- `lava` ×6.
- `tc:burst #F7CC9C 1.0→4.5 l4/f2 rot ~ 90` at P.

### B. Trail (per segment)

- On creation: `tc:slash #E04040 1.6→2.0 l18/f6 rot <glide yaw> 90` at the segment (a floor line along the glide), plus `dust #8C5436 1.2` ×4.
- On the flare (strike): `tc:flame #F06A30 0.4→1.0 l8/f3` ×2 at the segment ±0.4 b, `flame` ×8 Δ(0.5,0.3,0.5).

## 8. Sound

Taken from v3 §6:
- flaps 12.20 s;
- slam 12.84-12.97 (low +7…+9);
- eruption crackle 13.26-13.45;
- low rumble 13.38-14.03.

Not yet used in the pack: `entity.ghast.shoot`, `entity.generic.burn`.

## 9. Dodge window and fairness

**Fan.** The player is about 2.5 b in front of P (the dest keep).
- Out of r 4.5 + 0.3: 2.3 b back in 12 t (walk 2.6 b), OK.
- Or get behind the straight edge: past P's side, about 3 b.
- Or dash: the i-frames must cover act t28-32, so press at **t27** or **t28** (6 t covers t27-32 / t28-33).
- Fair: the fan is the pattern's big hit, telegraphed 12 t, with the two big flaps as the earlier read.

**Trail.**
- Embers show 10 t before each flare, and the segments are only 1.0 b wide. Do not walk through her glide line during t44-58.
- Cap 0.6.

**At r 21.** P is clamped (safe disc). A player at the wall in front of P can run sideways along the wall (the fan's straight edge is 9 b wide). 2.3 b of outward room is not needed.

## 10. Diagram

```
                .  . fan r4.5 180° .  .
              .     (P = slam point)    .
   S ------dive------> P ===aim===> P_player
              (behind P = safe)
                 |
                 v  glide to her right 4.5 b (t33-42), trail ooo (r 1.0, flare +10)
                 G
```

## 11. Implementation sketch (`wing.py`)

```python
tl.at(16, R('face/player'), g.dest(3.0, 2.5), g.keep(a),
      g.hz_opts(el=EL_PYRO, act=5, y1=2.5, kb=KB['default'], sfx=0),
      f'execute at {A_} facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ~ {CY} ~ run ' + g.hz_sector(4.5, 90, 12, DMG['b3']))
tl.at(20, f'execute positioned as {A_} run function rlk:mboss/mv/glide {{t:6}}')
tl.at(33, f'execute at {A_} facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^-4.5 ^ ^ run summon minecraft:marker ~ ~ ~ {{Tags:[...,"{gk}"]}}',
      f'execute as {G_} run function rlk:mboss/mv/clamp', f'execute positioned as {G_} run function rlk:mboss/mv/glide {{t:10}}')
for i, t in enumerate((34, 36, 38, 40)):
    tl.at(t, *( [g.GRP_NEW] if i in (0, 2) else [] ),
          *g.hz_opts(el=EL_PYRO, kb=KB['none'], act=8, sfx=0, grp=True), f'execute positioned ~ {CY} ~ run ' + g.hz_disc(1.0, 10, DMG['b3t']), <trail fx>)
```

## 12. Checks

- Fan: tell 12, act 5, y1 2.5.
- A player standing on all 4 segments takes exactly 2 × 0.3.
- Behind P (outside the half disc) no hit.
- The trail runs along her right side (perpendicular to the aim).
