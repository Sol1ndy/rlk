# B2 화염 날개의 습격 / 날개탄 (Flaming Wing Raid): implementation spec

| field | value |
|---|---|
| pattern | id 12, key `barrage`, form butterfly, kind normal |
| clip | `wing_barrage`, 117 t |
| events | rig now: swing1 0, swing2 26, swing3 64, swing4 89. **Proposed:** 5, 31, 69, 94 (+5, so the wind-up is inside the clip) |
| element | **Pyro (1)**; the core switches the look to Pyro 8 t before the start (`ai/prep`) and keeps her at ≥ 6 b |
| coefficient | 0.5 per crescent (`DMG['b2']` 50), **at most one hit per swing** (volley group per swing), so at most 4 × 0.5 = 2.0 |
| recover | 20 t |

## 1. Footage and plan check

Source: v3 A, 4.30-10.70 s, real time (`understand/v3.md` §3 A). I re-checked `k_crescents_a/b`, `k_volley0_quad` and `k_wingshot_*`. Ticks are relative to swing 1 = 0 (4.85 s).

| event | footage | plan / rig | verdict |
|---|---|---|---|
| wind-up: body turns 60-90°, one wing swept back | -5..0 before each swing | — | **mismatch**: the clip starts at swing 1 |
| swings | 0, 26, 64, 89 | 0, 26, 64, 89 | ok, but shift +5 (below) |
| flame sheet: swing 1 diagonal, swing 2 horizontal at chest height (≥ 8 m), swing 3 diagonal wave, swing 4 horizontal | +0..+4 | — | **cosmetic only** (no plan damage); see Q15 |
| crescents per swing | 6-8, claw/feather shapes 1-1.5 m with 1-2 m flame tails | 5 | keep 5 (readability, cap) |
| crescents fan out / rise 3-5 b, then curve onto the player's position | spawn +2..+8, turn about +9 | — | |
| landings around the player, 1 m fire splash plus a 2-3 m vertical flame | **+14..+18** | 14-18 | ok |
| speed | 12-15 m/s = 0.6-0.75 b/t | same | ok |
| total from first motion to idle | 117 | 117 | ok with the shift |
| she spins in place, drift ≤ 2 m, keeps 6-8 m | — | — | |

**Fix:** shift the swing events by +5 to **5 / 31 / 69 / 94**. The last landing is then 94 + 18 = 112 < 117. The clip starts with the first wind-up, so pattern tick = clip tick and no lead is needed. The alternative is `lead=5` with the current events, but the rig's wind-up pose would then be missing.

Homing: the footage crescents lock the player's position when they turn (about +9) and do not follow. **Spec:** lock at the swing tick; this gives a 14-18 t marker and is the readable version.

## 2. AI

- **Bands and weights:** mid ×1, far ×2. Never melee.
  - Before the start the core's prep backs her away (≥ 6 b) while the look switches.
- **Facing:**
  - At each wind-up tick (s-5): `face/player` (instant), then `face/track` until s.
  - Between swings: `face/track`. The rig spins the body visually during each swing; the body yaw stays on the player.
- **Locks:** at each swing tick s, `g.lockp()` gives L_s (floor under the player). The 5 targets are offsets from L_s in the aim frame (S → L_s).
- **Distance keeping:** during s+6..s+20, if the player is within 5 b, `mv/away {d:0.2}`; she never closes in. Drift ≤ 2 b in total.

## 3. Swing schedule and targets

Let s ∈ {5, 31, 69, 94} with swing index k = 1..4.

| crescent i | target offset (odd swings 1 and 3: a **cross row**, across the aim) | even swings 2 and 4: a **long row**, along the aim | lands at |
|---|---|---|---|
| 0 (centre) | (0, 0) | (0, 0) | s + 14 |
| 1 | (+1.8, 0) | (0, +1.8) | s + 15 |
| 2 | (-1.8, 0) | (0, -1.8) | s + 16 |
| 3 | (+3.6, 0) | (0, +3.6) | s + 17 |
| 4 | (-3.6, 0) | (0, -3.6) | s + 18 |

Offsets are (x = her left in the aim frame, z = along the aim, away from her), in blocks from L_s. Each target marker is clamped onto the floor disc. Today that is `mv/clamp`, which pulls it inside the boss safe disc (r 18.5). **Recommended:** a walk-disc clamp (r 20.3, `@WALKP@`) for ground-hazard targets. See README Q8, where wall-hugging players otherwise sit up to 2.5 b outside every lock.

Spawn points: on the leading wing, spread from root to tip, one per tick.
- Crescent i spawns at **s + 2 + i** at the body-frame point P_i = ^(2.4·sin θ_i) ^3.6 ^(2.4·cos θ_i), with fan angles θ = (0, +30°, -30°, +60°, -60°) for i = 0..4. It sits 2.4 b out at shoulder/wing-root height (toes 1.2 + 2.4).
- If the rig provides per-swing wing anchors, use lerp(root, fwtip, 0.3 + 0.15 i) at the swing event instead. The current manifest anchors at the swing events have the wing tips at y 6.8-8.5, which is too high for a readable launch.

## 4. Projectile (visual) and hazard per crescent

Damage comes from the **ground hazard** at the target. The flying crescent is a timed visual that lands exactly when the hazard strikes, so they cannot desync.

| property | value |
|---|---|
| hazard | at the target T_i, made at s: `hz_opts(el=1, kb=2, sfx=0, grp=True)`, then `hz_disc(1.2, land_i - s, 50)` (tell 14..18). One group per swing (`GRP_NEW` at s). |
| visual prop | `item_display` tagged `rlk_mb_bf_p12c`, kit model **`feather`** (a fire-crescent claw 1.2 b long with a flame tail): core `#F8F2B8`, mid `#F8D486`, edges `#DE9884` / `#CC6976`; `brightness 15`, `teleport_duration 1`. Placeholder: `tc:flame` geometry in a prop. |
| scores | `mbT` age (0 at spawn); `mbS` the landing tick; `mbId` 12; a link to its target marker `rlk_mb_bf_p12t` by index (`@s mbHzV` = i, or one marker tag per index) |
| phase 1, fan-out (age 0..5) | `tp ^ ^ ^0.6` along its launch rotation: yaw = aim + θ_i, pitch -35° (rising). About 3 b out and 1.7 b up. |
| phase 2, dive (age 6..landing-1) | `execute facing entity <its target marker> feet run tp @s ^ ^ ^0.75 ~ ~`. No other homing: it flies at the locked target, never at the live player. |
| landing tick | `tp` exactly onto T_i + (0,0.3,0), splash fx, kill the prop and its marker |
| live count | 5 per swing; swings ≥ 25 t apart and lives ≤ 16 t, so at most 5 props + 5 markers |

## 5. Per-tick timeline (per swing s; k = 1..4)

| t | rig | mechanics | fx | sound |
|---|---|---|---|---|
| s-5 | wind-up (turn, wing back) | `face/player` | wing-tip embers `flame` ×3 at fwtip (both) | `entity.ender_dragon.flap` 0.6/1.4, `entity.player.attack.sweep` 0.4/0.7 |
| s-1 | | | | `entity.player.attack.sweep` 0.8/0.7 (the whoosh leads the sheet) |
| **s** | **swing** | `g.lockp()` → L_s, `GRP_NEW`, 5 target markers + **5 hazards** (tell 14..18) | flame sheet (§7 A); 5 Pyro target decals r 1.2 (§6) | `entity.blaze.shoot` 0.8/0.9, `item.firecharge.use` 0.8/0.8, `entity.ghast.shoot` 0.4/1.2 |
| s+2..s+6 | spin follow-through | crescent i spawns at s+2+i | spawn puff `flame` ×4 + `dust #F8D486 1.2` ×3 at P_i | `block.fire.ambient` 0.8/1.5 at s+3, `entity.blaze.burn` 0.3/1.2 at s+3, `item.trident.riptide_1` 0.3/1.6 at s+6 |
| s+2..s+18 | | crescents fly (§4) | per-crescent trail (§7 B) | |
| s+12 | idle flap | | | `entity.ender_dragon.flap` 0.4/1.6 |
| **s+14..s+18** | | **one crescent lands per tick; its hazard strikes** | splash (§7 C) at T_i | per landing at T_i: `entity.generic.burn` 0.6/1.2, `entity.firework_rocket.blast` 0.4/0.8; the centre one also `block.fire.extinguish` 0.25/1.6 |
| 117 | end | `g.end()` | | |

Swing ticks: 5, 31, 69, 94 → landings 19-23, 45-49, 83-87, 108-112.

## 6. Telegraphs

- **Per target: 14-18 t.**
  - A Pyro decal r 1.2 at T_i from s: orange fill `#FF8A3D` growing to r 1.2 at its landing tick, rim `#FAD77C`, a magenta inner edge `#C680A2`.
  - Plus the framework outline (pyro colour).
- The row orientation alternates (cross / long), and the decals show it at once.
- Earlier reads: the wind-up (s-5) and the flame sheet (s).

## 7. FX detail

Palette (v3 §5):
- sheet core `#F8F2B8` / `#F9E38E` / `#FDF6DC`, mid `#F8D486` / `#ECC989` / `#DEA262`;
- edges `#DE9884` / `#CC6976` / `#A26A7A`, saturated `#F4BA33` / `#EB9F26` / `#ED7C59`;
- wind streaks `#FBF9F9`;
- scorch `#585542`, ember `#EDC30B`.

### A. Flame sheet (s)

A giant flame wave in the swing plane.
- Odd swings, diagonal: `tc:crescent #CC6976 8.0→9.0 l4/f2 roll 35 spin 170` (underlay) and `tc:crescent #F8D486 7.6→8.6 l4/f2 roll 35 spin 170` at ^ ^3.0 ^0.5, rot = yaw + 90.
- Even swings, horizontal: roll 0.
- `flame` ×20 Δ(2.5,0.6,1.0) speed 0.05 at ^ ^3.0 ^1.5.
- 4 white wind streaks `tc:slash #FBF9F9 3.0→4.5 l3/f1` around her (even swings only, as in the footage).

### B. Crescent trail (per crescent, per tick)

- `flame` ×1 and `small_flame` ×1 at the prop.
- `dust_color_transition #F8D486→#A26A7A 1.0` ×2.

### C. Landing splash (at T_i)

- `tc:burst #F9E38E 0.6→2.4 l5/f2 rot ~ 90` at T + (0,0.08,0).
- Vertical flame streak `tc:flame #F8D486 0.8→2.5 l6/f3` at T (pivot at the base).
- `lava` ×3, `flame` ×8 Δ(0.5,0.2,0.5).
- Scorch mark `dust #585542 1.6` ×6 on the floor, plus an ember glow `tc:glow #EDC30B 1.0→1.4 l20/f10 rot ~ 90`.

Card budget per swing: about 4 (sheet) + 5 (flames) + 5 (bursts) + 5 (embers), roughly 19 live at the worst moment. Under the cap of 40, but **it shares the cap with the decals**: if the kit decals are tinted cards too, drop the ember glow cards first.

## 8. Sound

Taken from v3 §6:
- wind-ups and swings 4.58-4.65, 4.89, 6.04-6.16, 8.05, 9.26-9.41 s (air +14…+20, about 0.3 s);
- launch crackle 5.16-5.23 and 8.09-8.34;
- landings 8.756, 8.896, 10.156 (sharp crack + puff).

Not yet used in the pack: `entity.ghast.shoot`, `entity.generic.burn`.

## 9. Dodge window and fairness

- **Cross rows** (swings 1 and 3, across the aim):
  - Step **toward or away from her** by 1.2 + 0.3 = 1.5 b, in 14 t (walk 3 b), OK.
  - Sideways needs 5.1 b (the row spans ±4.8): do not.
- **Long rows** (swings 2 and 4, along the aim): step **sideways** 1.5 b.
- Landing order centre → ±1.8 → ±3.6 punishes standing still first and running along the row last.
- **Dash:** through any single splash at its landing tick.
- **Cap:** one hit per swing whatever the player does, so the worst case is 2.0 over 117 t.
- **At r 21:** targets clamp to the floor disc. A player at the wall facing a cross row steps inward (toward her) 1.5 b, which is always possible. With today's r 18.5 clamp, a wall-hugger is never reached; that is Q8.

## 10. Diagram (cross row = swings 1 and 3; long row = 2 and 4)

```
 swing 1/3 (cross)                        swing 2/4 (long)
                                                    o (+3.6)
    S ~~~~flame sheet~~~~                           o (+1.8)
     \  \  |  /  /   crescents fan out    S ~~~~>   O L (centre, first)
   o   o   O   o   o   ← row across the aim         o (-1.8)
 -3.6 -1.8 L +1.8 +3.6  (lands 18 16 14 15 17)      o (-3.6)
   dodge: forward / back 1.5 b              dodge: sideways 1.5 b
```

## 11. Implementation sketch (`wing.py`)

```python
B2_SWINGS = [ev_or('wing_barrage', f'swing{i}', d) for i, d in enumerate((5, 31, 69, 94), 1)]
ROW = [(0, 0), (1.8, 0), (-1.8, 0), (3.6, 0), (-3.6, 0)]          # cross; swap to (0, x) for even swings
for k, s in enumerate(B2_SWINGS, 1):
    tl.at(s - 5, R('face/player'), <wind-up fx/snd>)
    lines = [R('face/player'), g.lockp(), f'kill @e[type=minecraft:marker,tag={lk}]', g.keep(lk, 'rlk_mb_bf_lock'), g.GRP_NEW]
    for i, (x, z) in enumerate(ROW if k % 2 else [(0, a) for a, _ in ROW]):
        land = 14 + i
        lines += [f'execute at {L_} facing entity @s feet rotated ~180 0 positioned ^{x} ^ ^{z} run summon minecraft:marker ~ ~ ~ '
                  f'{{Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12t","rlk_mb_bf_p12t{i}"]}}',
                  f'execute as @e[tag=rlk_mb_bf_p12t{i},limit=1] run function rlk:mboss/mv/clamp',
                  *g.hz_opts(el=EL_PYRO, kb=KB['light'], sfx=0, grp=True),
                  f'execute at @e[tag=rlk_mb_bf_p12t{i},limit=1] positioned ~ {CY} ~ run ' + g.hz_disc(1.2, land, DMG['b2'])]
    tl.at(s, *lines, <sheet fx>, <snd>)
    for i in range(5):
        tl.at(s + 2 + i, g.fn(f'p/{k_}/spawn{i}'))     # summons the feather prop i aimed at yaw + theta_i, pitch -35
# the pattern tick runs p/barrage/fly for every rlk_mb_bf_p12c (phase 1 / phase 2 / landing)
```

Cancel kills `rlk_mb_bf_p12c` and `rlk_mb_bf_p12t*`. Pause needs nothing: the props are moved by the module tick, which freezes.

## 12. Checks

- Each swing: 5 hazards in one group, tells 14..18.
- A player standing on L takes exactly 1 hit per swing.
- A player 1.6 b off the row (perpendicular to it) takes none.
- Each prop reaches its target on its landing tick (distance 0 at landing).
- Live props ≤ 5.
- Targets inside the clamp radius (r 18.5 today, r 20.3 after Q8).
