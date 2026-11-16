# H1 달빛 발차기 (Moonlit Kick): implementation spec

| field | value |
|---|---|
| pattern | id 1, key `kick`, form human, kind normal |
| clip | `kick_combo`, 51 t, events `hit1` 8, `hit2` 40 |
| lead | 2 (the clock starts at -2, so hit 1 gets a 10 t telegraph) |
| element | Dendro (7, the registry default; no `#hzEl` needed) |
| coefficients | hit 1: 1.0 (`DMG['h1a']` 100); hit 2: 1.2 (`DMG['h1b']` 120) |
| hits | 2 separate hits (each a volley group of 2 hazards), at most 2.2 in total |
| recover | 16 t idle afterwards (the core's `Pattern.recover`) |

Notation is defined in `README.md` §1. In short:
- `S` is her body on the floor.
- `P` is the player's feet.
- `A` and `B` are pattern markers.
- `^x ^y ^z` is the body frame (x = her left, z = forward).
- `tc:kind #hex s0→s1 l/f` is `g.tcard(kind, pos, colour, s0=, s1=, life=, fade=)`.
- `snd event v/p` is `g.sound(event, v, p)`.

## 1. Footage and plan check

Source: v1 9.80-12.40 s, real time (`understand/v1.md` §3 A). I re-checked the frames on `sheet_kick1a/1b` and `kick_fx_keyframes.jpg`. Ticks are counted from the run start, 9.87 s, which is clip tick 0.

| event | footage tick | plan / rig | verdict |
|---|---|---|---|
| burst-run, about 4 b, knee chambered from t2 | 0-5 | run 0-5 | ok |
| plant, white-lime sparkles at the feet | 5 | — | add the fx at t6 |
| foot whip glint | 5.3 | — | fx at t6 |
| **hit 1**, rising vertical crescent | 5.6-6.6 | **8** | Keep 8. The plan's 2 extra ticks of chamber read better; the footage has only about 1 t between the glint and the hit. |
| backflip; lands about 1.2 b behind the kick point | 7-14 | 9-17 (rig spin) | ok |
| settle and face | 14-20 | 17-20 | ok |
| wind-up: low stance, 2 sideways hops of 1-2 b | 20-32 | 20-32 | ok |
| leap, horizontal flying kick, about 3 b | 32-34 | 32-36 | ok |
| lime swirl on the kicking foot (tell) | 35.9 | — | fx at t36 |
| **hit 2**, diagonal crescent axe kick plus ground wave | 37.3-37.9 | **40** | Keep 40, consistent with the hit-1 offset. |
| ground wave lingers | 38-42 | — | fx at t40-43 |
| lands, recovers to idle | 40-51 | land at about 44, end 51 | ok |

Areas, plan vs footage:
- **Hit 1: the footage disagrees with the plan.** The plan says "front arc r about 4, tall". The footage shows a narrow vertical blade arc, a strip about 1.5 m wide from about 0.5 m to 3 m ahead of her, at least 6 m tall, with an r about 1.5 m lime splash at its base.
  - **Proposed fix:** a lane 4.5 long (starting 0.5 behind her) and 2.4 wide, plus a disc of r 1.5 centred 1.2 ahead, in one volley group.
  - If the plan's arc must stay, use `hz_sector(4.0, 35, …)`, not a wide arc.
- Hit 2: the plan's 180° sector of r 5 plus a 6×2 ground wave matches the footage (an arc of r about 6 in front plus a 6×2 m strip). Keep it.
- **Kick-2 direction.** In the footage it is fixed at the start of the wind-up (about t20) and went to her front-right, missing the player. The spec aims it at the player and locks it at t26 (14 t of telegraph). That is a design choice for a fair, readable hit.
- **Root travel.** The rig clip currently bakes the travel in: pos z +0.8 to +1.2 b back during the backflip, then -0.4 b at hit 2. This spec moves the body itself (§3). The two must not both happen; see README Q1.

## 2. AI

- **Bands and weights:** melee (≤ 4 b) ×2, mid (4-8 b) ×1. Never far.
- **Approach:** none before the pattern. The clip's own burst-run (t0-5) closes up to 4.5 b.
  - In the mid band (≤ 8 b) she therefore ends at most 3.5 b from the player.
  - Hit 1 reaches 4.0 b.
- **Facing:**
  - t-2: `face/player` (instant).
  - t-2..5: `face/track` (≤ 12°/t) toward the player while she runs.
  - t6..25: her yaw is held (no tracking): flip, backflip, settle.
  - t26: `face/player`, then held until the end (hops and leap stay on the locked line).
- **Aim locks:**
  - **lock A at t-2**: `g.dest(4.5, 1.5)`. Marker A is on the line to the player, at most 4.5 b from her and 1.5 b short of the player, inside the safe disc. Hit 1 is anchored at A and aimed at the player's position at t-2.
  - **lock B at t26**: `g.dest(3.5, 1.2)` from her position at t26. Marker B is the leap's landing point. Hit 2 is anchored at B, aimed along her yaw at t26.

## 3. Body travel (module side)

| ticks | travel | call |
|---|---|---|
| 0-5 | glide S → A (burst-run, 0.6-0.9 b/t) | `execute positioned as A run function rlk:mboss/mv/glide {t:5}` at t0 |
| 9-16 | backflip: 1.2 b back | `mv/away {d:0.15}` each tick 9..16 |
| 20-31 | 2 sideways hops of 0.75 b each, at 22-24 and 28-30 (side = `#bfSide`, flipped at 28) | each tick: `execute at @s rotated as @s rotated ~90 0 positioned ^ ^ ^0.25 if function rlk:mboss/mv/ok run tp @s ~ ~ ~` (as the core's `ai/strafe_go`; `~-90` for the other side). Her yaw is kept. |
| 32-36 | leap → B | `execute positioned as B run function rlk:mboss/mv/glide {t:4}` at t32 |
| 37-51 | none | |

`mv/step`, `mv/away` and the sideways `tp` check `mv/ok`, which keeps her within r 18.5. `u/dest` already keeps the glide targets inside that disc.

## 4. Per-tick timeline (clip tick; `#bfPT`)

| t | rig | mechanics | fx | sound |
|---|---|---|---|---|
| -2 | (idle) | `face/player`, lock A, **hit-1 hazards (tell 10)** | lane + splash decals (Dendro), tell cue | `block.amethyst_block.resonate` 0.35/1.6 |
| 0 | clip starts: run | glide → A (5 t) | `poof` ×2 at the feet (every 2 t until t5); `tc:leaf #A8DF74 0.3→0.4 l10/f4` ×1 behind her | `entity.breeze.jump` 0.6/1.3, `block.moss_carpet.step` 0.5/1.0, `entity.player.attack.sweep` 0.25/1.5 |
| 2 | knee chambered | | `tc:star #E5FBC8 0.2→0.6 l4/f2 bb center` at foot_r | |
| 3 | | | | `block.moss_carpet.step` 0.4/1.1 |
| 5 | plant | | white-lime sparkles: `wax_off` ×4 Δ(0.5,0.05,0.5) at ^ ^0.1 ^0.6; `dust #E5FBC8 0.8` ×6 | |
| 6 | foot whip | | glint `tc:star #FFFFFF 0.3→1.2 l4/f2 bb center` at ^0 ^0.5 ^1.0 | `block.amethyst_block.chime` 0.5/1.9 |
| 7 | | | ground splash `tc:burst #D7F899 0.5→3.0 l5/f2 rot ~ 90` at ^ ^0.08 ^1.2 | |
| **8** | **hit1** | **hit 1 resolves (strike)** | the crescent (§7 A) | `entity.breeze.wind_burst` 0.6/1.4, `block.azalea_leaves.break` 0.8/1.0, `block.big_dripleaf.tilt_down` 0.6/1.2, `entity.player.attack.sweep` 0.5/1.3 |
| 9-16 | backflip | `mv/away 0.15` per tick | trail: `tc:crescent #BFF191 1.6→2.4 l4/f2 roll 90 spin -150` at ^ ^1.4 ^0 at t9 and t12; `dust #C1F788 1.0` ×2 per tick at the core anchor | `item.trident.riptide_1` 0.3/1.6 at t11 |
| 10-14 | | | trail breaks into leaves: `tc:leaf #A8DF74 0.3→0.4 l12/f6` ×2 at t10 and t13, with `move` (0,-1.2,0.4) | |
| 16 | lands | | `poof` ×6 Δ(0.4,0.05,0.4); `block{block_state:"minecraft:moss_block"}` ×8 | `block.moss.fall` 0.6/1.0 |
| 18 | | | | `block.moss.fall` 0.35/1.2 |
| 20-31 | wind-up, hops | | kicking-foot glow: `dust #E5FBC8 0.7` ×2 every 2 t at foot_r; fans flared (rig) | |
| 22, 28 | hop | sideways hops | `poof` ×3 at the feet | `block.moss_carpet.step` 0.5/1.2 |
| **26** | | `face/player`, lock B, **hit-2 hazards (tell 14)** | sector + wave decals, tell cue | `block.amethyst_block.resonate` 0.35/1.5 |
| 32 | leap | glide → B (4 t) | `tc:slash #D7F899 3.0→3.5 l4/f2` along her path at ^ ^1.0 ^-1 (rot = yaw, bb fixed) | `entity.breeze.jump` 0.6/1.1 |
| 34 | flying kick | | `tc:slash #EDF9DA 2.0→3.0 l3/f1` at ^ ^1.2 ^0 | |
| 36 | tell: foot swirl | | `tc:swirl #D7F899 0.4→1.4 l6/f2 bb center spin 160` at foot_r | `block.amethyst_block.resonate` 0.5/1.6 |
| 39 | | | | `entity.player.attack.sweep` 0.8/0.8 (the whoosh leads by 1 t) |
| **40** | **hit2** | **hit 2 resolves** | the axe-kick crescent plus ground burst (§7 B) | `entity.breeze.wind_burst` 0.8/1.0, `block.big_dripleaf.break` 0.6/1.0, `block.azalea.break` 0.7/0.9, `block.azalea_leaves.break` 0.6/1.2 |
| 40-42 | | | ground wave: 2 blade shards per tick march out (§7 B) | `block.azalea.break` 0.5/1.0 at 41, 0.5/1.1 at 42 |
| 43-47 | | | trail dissolves: `tc:leaf` ×4 at t43 and t46 drifting (`move` (0,-1.5,0.6), l14/f6); `dust #AEE08B 1.2` ×6 along the wave line at t44 | |
| 44 | lands | | `poof` ×6; moss block particles ×8 | `block.moss.fall` 0.6/0.9, `entity.iron_golem.step` 0.3/1.4 |
| 51 | end | `g.end()` | | |

## 5. Damage areas

Call each hazard positioned on the floor, rotated = aim (`execute at A facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ~ 201 ~ run …`). Set `hz_opts(sfx=0)` on every hazard: the composed sounds above replace the framework strike sfx.

### Hit 1 (t-2 → strike t8): volley group G1

1. **Lane:** `hz_line(4.5, 2.4, 10, 100)` with `back=0.5`.
   - It covers -0.5..4.0 b ahead of A and ±1.2 b sideways, height -0.5..3.5 (the default).
   - `kb=3` (default, away along her yaw).
2. **Base splash:** a disc of r 1.5 centred 1.2 b ahead of A (`positioned ^ ^ ^1.2`): `hz_disc(1.5, 10, 100)`, `kb=3`.
3. Both carry `grp=True` after `g.GRP_NEW`, so there is at most one hit.

Selector shape in plain terms: the union of a rectangle (A + (-1.2..1.2, -0.5..4.0) in the aim frame) and a disc (centre A + 1.2·aim, r 1.5).

### Hit 2 (t26 → strike t40): volley group G2

1. **Crescent arc:** `hz_sector(5.0, 90, 14, 120)` at B, aimed along the locked yaw. A half disc of r 5 in front of B. `kb=3`.
2. **Ground wave:** `hz_line(6.0, 2.0, 14, 120)` from B along the yaw: 0..6 b ahead, ±1.0. `kb=3`.
3. One group (`grp=True` after `GRP_NEW`), so at most one hit.

Cap: 2 hits in the pattern (G1 and G2), 1.0 + 1.2.

## 6. Telegraphs

- **Hit 1: 10 t (t-2 → t8).**
  - The framework outline (Dendro colour) plus the kit's lane fill.
  - `tc`/decal `lane` 4.5×2.4, `#B6E35A`, filling from the back edge to the front over 10 t.
  - Plus a disc fill r 1.5 that grows from 0 → r over 10 t.
  - The crescent tell is the chambered knee (t2) and the glint (t6).
- **Hit 2: 14 t (t26 → t40).**
  - A sector fill r 5 (half disc) growing from 0 → r 5.
  - Lane fill 6×2 with two forward chevrons.
  - Readable tells: the hops (t22, t28), the leap (t32), the foot swirl (t36).
- Strike flash: the framework's at the strike tick, plus the fx below.

## 7. FX detail

Palette (v1 §5):
- core `#EDF9DA` / `#E5FBC8`;
- bright `#D7F899` / `#C1F788`;
- mid `#BFF191` / `#AEE08B`;
- edge `#8DCA85`;
- dark teal underlay `#297272` / `#3A765D`;
- flash `#FBFDF4`;
- leaves `#A8DF74`.

### A. Hit-1 crescent (t8)

A tall vertical blade arc rising from the splash and sweeping up and back over her: 6 b tall, about 1 b thick, with jagged leaf blades at the base. The crescent card is flat (XZ); `roll 90` stands it in her sagittal plane.
- Underlay `tc:crescent #297272 5.5→7.0 l6/f3 roll 90 spin -120` at ^ ^0.2 ^0.8.
- Overlay `tc:crescent #C1F788 5.0→6.5 l6/f3 roll 90 spin -120` at the same point, 1 tick later (t9) so the bright layer leads.
- Core streak `tc:slash #EDF9DA 4.0→5.5 l3/f1 roll 80` at ^ ^2.5 ^1.0.
- Base blades: 6 × `tc:shard #A8DF74 0.6→1.4 l6/f3` at ^ ^0.1 ^1.2, rot `~±(0..50) -60` (fanned upward).
- `dust #D7F899 1.2` ×14 Δ(0.6,1.4,0.3) at ^ ^2 ^1.2; `wax_off` ×6.

### B. Hit-2 axe kick (t40) and ground wave (t40-42)

- Huge diagonal crescent from about 5 b above and behind her down to the floor about 6 b ahead.
  - Underlay `tc:crescent #297272 9.0→11.0 l6/f3`, rot = yaw, `roll -35`, `spin 90`, at ^ ^1.8 ^1.0.
  - Overlay `tc:crescent #D7F899 8.5→10.5 l6/f3` at the same point at t41.
- Impact burst `tc:burst #EDF9DA 1.0→4.0 l5/f2 rot ~ 90` at ^ ^0.08 ^2.0; `flash{color:[0.93,0.98,0.85,0.9]}` ×1 at ^ ^0.5 ^2.0.
- Ground wave: `tc:shard` blades erupting along B + (0, k) for k = 1..6 b, 2 per tick on t40/41/42 (k 1-2, 3-4, 5-6).
  - Colours alternate `#D7F899` / `#AEE08B`; `0.5→1.6 l8/f4`; rot `~ -70` (tilted forward).
  - Plus `dust #297272 1.4` ×3 and `dust_color_transition #E5FBC8→#297272 1.2` ×4 at each.
- Lingering trail: `dust #B7D8AF 1.0` ×8 along the wave line at t42 and t44.

Card budget: at most 12 live from this pattern (cap 40).

## 8. Sound

Taken from v1 §6: kick 1 at 10.13-10.20 s, backflip at 10.45-10.94 s, kick 2 at 11.73-11.96 s. The whoosh precedes contact by about 0.1 s.

All layers are listed in the timeline above. Volumes are ≤ 0.8, so per-layer minVolume follows `L.min_volume` and quiet layers (≤ 0.25) fade with distance. Every event in it is already used in the pack except `block.moss_carpet.step`, `block.moss.fall` and `block.big_dripleaf.break` (vanilla 1.20+, also used by the stage-1 core; verify once in 26.3).

## 9. Dodge window and fairness

Player kinematics (README §1.3):
- walk 0.22 b/t;
- sprint 0.28 b/t;
- dash 3 b in 3 t with 6 t of i-frames from the press;
- jump apex 1.25 b.

**Hit 1.** The player is about 1.5 b in front of A.
- Sideways: get out of the 2.4-wide lane by moving 1.2 + 0.3 = 1.5 b. That takes 7 t walking, so 10 t is enough.
- Backward: to more than 4.3 b from A, 2.8 b in 10 t. That needs a sprint (exactly 2.8 b) or a dash.
- Through her: dash forward past A, since behind her is safe.
- Dash i-frames: press during t3..t8.

**Hit 2.** The player is about 1.2-3 b in front of B.
- Leave the r 5 half disc: 2-3.8 b in 14 t (sprint 3.9 b) works.
- Better: dash behind her, since the half plane behind B is safe.
- Or i-frames: press during t35..t40.

Fair, with two distinct reads: a narrow lane, then a wide half disc.

**At the arena r 21.** A and B are clamped inside the safe disc (r 19). A player pinned at the wall with her outward of them cannot back off, but sideways (hit 1) and "behind her" (hit 2) both point into open floor. No unwinnable spot.

## 10. Diagram (top view, player at about 3 b, aim to the right)

```
 hit 1 (t-2 → 8)                         hit 2 (t26 → 40)
                                          .  .  .  .  .
        +---------------+               .                .
   S===>A  lane 4.5x2.4 |  P          .   r 5 half disc     .
        +--(splash r1.5)+             B=======wave 6x2=========>
   run 0-5: S → A (≤ 4.5 b)            .                       .
                                          .  .  .  .  .  .  .
                                     (behind B is safe; B = leap landing)
```

## 11. Implementation sketch (`human.py`)

```python
tl.at(-2, R('face/player'), g.dest(4.5, 1.5), g.keep(a), g.GRP_NEW,
      g.hz_opts(sfx=0, kb=KB['default'], back=0.5, grp=True), on_floor(A_) + g.hz_line(4.5, 2.4, 10, DMG['h1a']),
      g.hz_opts(sfx=0, kb=KB['default'], grp=True),
      f'execute at {A_} facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^1.2 positioned ~ {CY} ~ run '
      + g.hz_disc(1.5, 10, DMG['h1a']), <decals>, g.sound('block.amethyst_block.resonate', 0.35, 1.6))
tl.span(-2, 5, R('face/track'))
tl.at(0, f'execute positioned as {A_} run function rlk:mboss/mv/glide {{t:5}}', ...)
tl.span(9, 16, 'function rlk:mboss/mv/away {d:0.15}')
tl.at(26, R('face/player'), g.dest(3.5, 1.2), g.keep(b), g.GRP_NEW, <sector + line, grp>, ...)
tl.at(32, f'execute positioned as {B_} run function rlk:mboss/mv/glide {{t:4}}')
tl.at(51, g.end())
```

Cancel kills markers A and B (the stub already does). No props.

## 12. Checks

- mcsim: the hit-1 hazards exist from clock -2 with tell 10, and the hit-2 hazards from 26 with tell 14.
- A player inside both shapes of a group takes exactly 1 hit; a player in both groups takes 2.
- Every telegraph lasts ≥ 10 t.
- Body travel: the end position is within 1 b of B (no double travel with the rig; see Q1).
