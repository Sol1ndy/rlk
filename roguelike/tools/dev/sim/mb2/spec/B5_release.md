# B5 달빛 해제 / 강화 해제 (Moonlight Release): implementation spec

| field | value |
|---|---|
| pattern | id 15, key `release`, form butterfly → human, kind **service** (the core starts it; the pattern file owns only fx and hazards) |
| trigger | after 4-5 butterfly patterns or 900 t of butterfly form, at a decision point (`form/release_go`) |
| clip | `release`, 96 t. Rig events now: fold 0, swoop 6, whirl 18, cup 31, flash 41, glint 42, rings 43, wrap 44, detonation 53, hover 56, shrink 82, flat 84, shatter 88, revert 92, land 96. **Proposed:** flash 35, glint 37, rings 38, shrink 87, flat 87, shatter 91 (§1). |
| core mechanics (`p/svc`) | t0 caption "달빛 해제"; the flat event → `look/flat`; the revert event (92) → `form/revert` (human hitbox, heal orbs vanish); the pattern end → `groggy/begin` |
| element | Dendro (7) |
| coefficient | 2.6 (`DMG['b5']` 260), the biggest hit of the fight |
| hits | 1 |
| recover | none (the groggy follows) |

E below means the detonation tick (53).

## 1. Footage and plan check

Sources:
- real time: v3 D, 32.83-38.28 s (`understand/v3.md` §3 D);
- detail: v4 A, the 0.5x replay (`understand/v4.md` §2 A).

I re-checked `sheet_REPLAY_wrap_explode_5.90-7.70.jpg` (the X glint, ring cage, pod, whiteout).

| event | footage (tick vs E) | clip tick | plan / rig | verdict |
|---|---|---|---|---|
| wings folded up (closed butterfly), tips toward the player; lime butterfly glyphs float | E-53..-48 | 0-5 | fold 0 | ok |
| swoop: dives low at the player, 4-5 b in 0.25 s, wings re-open; **no damage** | E-48..-44 | 5-9 | swoop 6 | ok |
| hovers about 1 b up, lime core at her chest, climbs | E-44..-39 | 9-14 | | |
| whirl: tumbles about 2 turns, wings flicking; lime slash streaks 3-6 m | E-42..-22 | 11-31 | whirl 18 | ok (rig 18-30) |
| lime 4-point star flare, 1 m, at her right side, pulsing; streaks converge on it | E-36..-22 | 17-31 | | fx |
| **cup**: wings swing forward around her front | E-22..-18 | 31-35 | cup 31 | ok |
| **ground flash**: lime mist cone from the floor, 2-3 m | E-18..-16 | **35-37** | flash **41** | **retime → 35** |
| **X glint**: two cyan-white lines (about 8 m) cross through her chest | E-16..-15 | **37-38** | glint **42** | **retime → 37** |
| **ring cage**: 2-3 lime gyroscope rings r about 4 | E-15..-10 | **38-43** | rings **43** | **retime → 38** |
| **wrap**: wings fold into a closed pod (1.2 H × 1 H), core grows, streaks spiral in, she sinks a little | E-9..-1 | 44-52 | wrap 44 | ok |
| wings snap open | E-1 | 52 | | |
| **E: white flash**, a white sphere of r about 5.5 on its first frame | E | 53 | detonation 53 | ok |
| lime dome expands past the player and the camera (≥ 10-11 m) | E..E+2 | 53-55 | | |
| HIT on the player 3-5 b away: -33 % max HP (13018), plus 연소 (the player carried Pyro) | E+3..+5 | 56-58 | 2.6 | ok |
| she re-emerges, wings flung wide, tendrils stream out 5-10 m | E+7..+10 | 60-63 | hover 56 | ok |
| hover about 2 b up (feet 0.8 H), slow beats; amber ember petals | E+10..+34 | 63-87 | | |
| **wings shrink and go flat lime** | E+34..+38 | **87-91** | shrink **82**, flat **84** | **retime → 87, 87** |
| **wings shatter** | E+38..+39 | **91-92** | shatter **88** | **retime → 91** |
| human form in mid-air (feet 1.5-2 b up) | E+39 | 92 | revert 92 | ok |
| lands | E+43 | 96 | land 96 | ok |

Telegraph:
- Footage: cup → explosion is 22 t; the explosion covers r ≥ 10.
- Stub: the r 10 decal starts at E-15.
- **Proposed:** start the decal at the **cup (E-22 = t31)**: 22 t. The plan's "dodge by being farther than 10 b or by dashing at E" needs that time (see §9).

## 2. AI and placement

- **Release point R** (where she hovers and explodes), computed at t0:
  - L0 = the player's floor position; C = the arena centre; u = the unit vector C → L0 (if |C L0| < 1 b, u = S → L0).
  - **R = L0 + 4·u**, then pulled inward to **|C R| ≤ 16 b** (the butterfly hover clamp of README Q9).
  - She ends on the **wall side** of the player, about 4 b from them, as she "swoops past the player". The player's escape is toward the open centre, where at least 21 b of floor lies on the far side.
- **Movement:** swoop S → R (t5-14, `mv/glide {t:9}`); then she stays over R until the revert. From E+10 to E+34 a slight drift of ≤ 1 b.
- **Facing:**
  - t0: `face/player`.
  - t0-31: `face/track`.
  - t31-53: held (cup, pod).
  - t53-92: `face/track` (hover).
  - At the landing (96) the core turns her back to the player for the groggy.
- **Aim lock:** none (radial).

## 3. Per-tick timeline

| t | rig | mechanics | fx | sound |
|---|---|---|---|---|
| 0 | fold | core: caption "달빛 해제"; compute R (marker `rlk_mb_bf_p15r`) | 3 lime butterfly glyphs (kit `butterfly`, `#B8E04C`, s 0.6, l20/f6, slow drift up) near her; folded-wing rim glow `tc:glow #B6E35A 1.0→1.6 l10/f4 bb center` at the core | `entity.ender_dragon.flap` 0.6/1.2 |
| 5 | swoop | glide → R (9 t) | wing edge dragging: `tc:slash #B6E35A 2.0→3.0 l4/f2 rot <path> 90` at her floor point every 2 t, t5-11; leaves | `entity.phantom.swoop` 0.7/1.0, `entity.ender_dragon.flap` 0.4/1.6 |
| 9 | climb | | lime motes from the wing tips | `entity.phantom.swoop` 0.5/1.3 |
| 14 | over R | | the core glows at her chest: `tc:glow #D8F2BC 0.4→0.9 l14/f4 bb center` | |
| 18-30 | **whirl** | `face/track` | slash streaks (§5 A) every 2 t; star flare (§5 B) every 4 t from t18 | `entity.breeze.whirl` 0.6/1.3 at 18, 0.5/1.4 at 24, 0.5/1.5 at 28; `entity.player.attack.sweep` 0.4/1.6 at 22 and 30 |
| 20 | | | | `block.beacon.power_select` 0.6/1.4 (the charge begins) |
| **31** | **cup** | **dome hazard: disc r 10 at R, tell 22** | the big decal (§4); `tc:glow #D8F2BC 1.0→1.8` at the core | `block.respawn_anchor.charge` 0.7/1.2, `block.beacon.activate` 0.6/1.6 |
| **35** | ground flash | | lime mist cone: `tc:burst #EEFADC 1.0→3.0 l5/f2 rot ~ 90` at R + (0,0.08,0); `dust #D3F0B8 1.4` ×20 in a column Δ(0.6,1.5,0.6) at R + (0,1.5,0); `flash{color:[0.93,0.98,0.86,0.8]}` | `block.amethyst_block.resonate` 0.7/1.0 |
| **37** | X glint | | two `tc:slash #8DEAF0 6.0→8.0 l3/f1`, roll +35 and -35, at the core, rot = yaw + 90 (crossing in front of her); `end_rod` ×6 | `block.amethyst_cluster.hit` 0.8/1.9 |
| **38-43** | ring cage | | 3 rings r 4 around the core (§5 C) at t38, refreshed at t41 | `block.conduit.activate` 0.5/1.4 at 38; `block.respawn_anchor.charge` 0.6/1.5 at 41 |
| 41, 47 | | | outer-edge sparkle at r 10.5 around R: `end_rod` ×24 (one per 15°) at y 0.3 (the "safe line") | |
| **44-52** | wrap (pod) | | the rig's `pod` prop or wing pose; core glow grows: `tc:glow #DFF99C 1.0→3.0 l9/f0 bb center`; inward spiral streaks: 2 per tick `tc:slash #D6EDD2 2.0→0.8 l4/f1` at the core ± 3 b, `move` toward the core; starburst `tc:burst #DFF99C 1.5→2.5 l4/f2 bb center` at t48 and t51 | `block.respawn_anchor.charge` 0.7/1.8, `entity.breeze.whirl` 0.5/0.9 at 44 |
| 49 | | | | `entity.warden.sonic_charge` 0.5/1.8 (4 t ahead) |
| 52 | snap open | | | |
| **53** | **E** | **dome strike** | the explosion (§5 D); screen flash | `entity.generic.explode` 1.0/0.7, `entity.warden.sonic_boom` 0.6/1.4, `block.amethyst_cluster.break` 1.0/0.8, `entity.breeze.wind_burst` 1.0/0.6, `block.beacon.deactivate` 0.6/1.4 |
| 54-55 | | | dome growth (§5 D) | `block.azalea_leaves.break` 0.8/0.9 at 55; `entity.breeze.wind_burst` 0.5/0.8 at 55 |
| 57 | | | | `block.azalea_leaves.break` 0.6/1.1 |
| 58 | | | | `entity.breeze.idle_air` 0.4/0.6 (the low rumble tail) |
| 60-63 | flung open | | tendrils: 8 `tc:slash #77CE3E 2.0→8.0 l8/f4` radial (yaw 45k, pitch -10) at the core; `dust #99E358 1.2` ×20 | |
| 63-87 | hover | `face/track` | amber petals: `tc:leaf #E2BF5F 0.2→0.25 l30/f8 move (0,-3,0)` ×1 every 3 t at a random ±3 b; lime motes `dust #C4F87E 0.8` ×2 every 4 t | `entity.ender_dragon.flap` 0.4/1.7 at 63 and 76 |
| **87** | **shrink + flat** | core: the flat look at this event | wing-tip lime shards: `dust #E7FD7A 1.0` ×6 at the fwtip / hwtip anchors every 2 t, t87-91 | `block.beacon.deactivate` 0.6/1.8 |
| **91** | **shatter** | | `tc:shard` ×10 (`#E7FD7A` / `#DBF796`) at the wing anchors, flung outward (`move` 2 b), l10/f5; `block{block_state:"minecraft:lime_stained_glass"}` ×20 Δ(2,1,1) | `block.amethyst_cluster.break` 0.7/1.5, `block.glass.break` 0.4/1.6, `entity.illusioner.mirror_move` 0.6/1.4 |
| **92** | revert | core: `form/revert` (human hitbox, heal orbs vanish) | | |
| **96** | land | the pattern ends → core `groggy/begin` | `poof` ×8; moss block ×10; `dust #B6E35A 1.0` ring r 1.3 | `block.moss.fall` 0.8/1.0, `entity.iron_golem.step` 0.4/1.4 |

## 4. Damage area and telegraph

- **Dome:**
  - At t31: `hz_opts(kb=4, sfx=0)`, then `execute at R positioned ~ 201 ~ run hz_disc(10.0, 22, 260)`.
  - **Shape:** a filled disc of r 10 around R on the floor, height -0.5..3.5 (always the player's whole reach).
  - Strike at E (53). Dendro, 2.6, KB 4 (heavy, radial from R). One hit.
- **Telegraph: 22 t.**
  - The framework outline at r 10 (Dendro colour, every 4 t).
  - The kit's **big ring decal**: `ring` s 23.3 (r 10) `#B6E35A`, lying flat at R + (0,0.06,0), held t31-53.
  - A fill `glow` growing s 2 → 20 over 22 t, alpha low (`#B6E35A`).
  - At t41 and t47 the safe-line sparkles at r 10.5.
- Earlier reads:
  - the caption at t0;
  - her settling over R at t14;
  - the star flare (t17-31).
- **Burning:** a Dendro hit on a Pyro-marked player re-triggers Burning (native): the "연소를 활용한 강력한 공격" of the info card. B2 and B3 leave Pyro on the player shortly before.

## 5. FX detail

Palette (v3 §5, v4 §5):
- flare `#F8FCE7` / `#D8F2BC` / `#AEE76F`, haze `#53AD50`;
- rings `#CCF59C` / `#91CF7E` / `#64B360`, cage `#ADE87F`, core `#DCFA9A`;
- X glint `#8DEAF0` with a white core;
- pod `#DFF99C` / `#E5F6DC`, shell `#D6EDD2` / `#A4D260` / `#58A353`;
- whiteout `#FEFEF9` / `#E7FDB9`;
- dome `#87F155` / `#5CD63D` / `#C2F999` / `#F8FDDA`, rim `#B6FC9D` / `#7AFA88` / `#3CDC71`;
- tendrils `#77CE3E` / `#99E358` / `#C4F87E`;
- embers `#E2BF5F` / `#FFEBB5`;
- retract `#E7FD7A` / `#DBF796`.

### A. Whirl slash streaks (t18-30, every 2 t)

- 2 × `tc:slash #9FD57F 3.0→5.5 l4/f2` at the core with a random yaw and roll (±60°), `bb fixed`.
- One of each pair is `#F8FCE7` (white core).

### B. Star flare (t18-30, every 4 t)

- `tc:star #EEFDCF 0.8→2.0 l4/f1 bb center` at ^-1.2 ^0 ^0 from the core anchor (her right).
- `tc:glow #53AD50 1.0→1.6 l4/f2 bb center` behind it.
- Converging streaks `tc:slash #AEE76F 1.6→0.6 l3/f1` ×2 moving into it.

### C. Ring cage (t38-43)

- 3 × `tc:ring #ADE87F 8.6→9.3 l6/f1` (r 4) at the core:
  - one vertical facing the player (`rot ~ 0`);
  - two tilted (`rot ~60 30`, `rot ~-60 -30`);
  - each `spin 170`.
- Refresh at t41.
- Inner `tc:crescent #DCFA9A 2.0→3.0 l3/f1` flicks ×2 per refresh.

### D. Explosion (t53-62)

- t53:
  - Screen: the kit's screen overlay **white** (alpha about 0.9) for 2 t, then **lime tint** `#87F155` (alpha about 0.35) for 10 t, for players within 14 b of R; lime tint only beyond that.
  - `tc:burst #FDFDFB 6.0→11.0 l3/f1 bb center` at R + (0,3,0).
  - `tc:orb #F8FDDA 10.0→16.0 l2/f0 bb center` at R + (0,3,0).
  - `explosion_emitter` ×1.
  - `flash{color:[0.99,0.99,0.98,1.0]}` ×1.
- t54: dome shell `tc:orb #87F155 16.0→21.0 l2/f0 bb center`; ground band `tc:ring #B6FC9D 10.0→24.5 l3/f0 rot ~ 90` at R + (0,0.1,0).
- t55: shell holds `tc:orb #5CD63D 21.0→21.5 l6/f0 bb center`; second band `tc:ring #7AFA88 20.0→24.5 l5/f2 rot ~ 90`.
- t53-56: `dust #5CD63D 2.0` ×60 on a sphere shell (r grows 5 → 10, precomputed points); `end_rod` ×30 speed 0.6 from R + (0,3,0); `tc:leaf #E0E06D` ×10.
- **Request to the fx kit:** a real translucent sphere model `dome` (inward and outward faces, alpha 0.3-0.5, rim brighter) scaled 11 → 21 b over 2 t and swapped to fainter variants every 2 t. Billboard orb cards are the fallback.

## 6. Dodge window and fairness

The player is at about 4 b from R (R is 4 b beyond them, toward the wall) when she settles at t14.

- **Distance:** get to more than 10.3 b from R, i.e. 6.3 b toward the centre.
  - From the caption (t0): 53 t (sprint 14.8 b).
  - From the decal (t31): 22 t (sprint 6.2 b, borderline; with one dash, 9.2 b).
  - Fair for anyone reacting to the caption, the swoop or the star flare.
- **Dash i-frames:** the strike is at E = 53; press at **t48-53** (6 t). The pod snapping open (t52) and `sonic_charge` (t49) are the cues. This always works, wall or not.
- **At r 21:** R is clamped to |C R| ≤ 16. If the player hugs the wall (|C L0| = 20), R is 16 and the player is 4 b *outward* of her.
  - Escape along the wall needs about 10.6 b of arc: sprint (t14 → 53, 39 t = 10.9 b) or dash + sprint.
  - Or the dash at E. Tight but fair; the dash answer is universal.
- **Burning:** a Pyro-marked player takes the Burning DoT after the hit (about +100 % of a Pyro hit's base over 2 s). Expected and readable (the 연소 text).

## 7. Diagram

```
                 wall (r 21)
            .  -  ' R (≤ 16 from C) '  -  .        dome r 10 around R (strike E = t53)
         .        swoop S → R t5-14         .
       .               P (≈4 b from R)        .    escape toward C (open floor), or dash t48-53
        .                  ↓  6.3 b            .
          .                C (centre)        .
             '  -  .  _  _  _  _  .  -  '
 caption t0 · whirl 18-31 · cup 31 (decal) · flash 35 · X 37 · cage 38-43 · pod 44-52 · E 53
```

## 8. Implementation sketch (`wing.py`)

```python
B5_CUP, B5_DET = ev_or('release', 'cup', 31), ev_or('release', 'detonation', 53)
tl.at(0, R('face/player'), g.lockp(), g.keep(a, 'rlk_mb_bf_lock'),             # a = L0
      f'execute at @e[tag=rlk_mb_arena,limit=1] facing entity {A_} feet rotated ~ 0 positioned as {A_} positioned ^ ^ ^4 '
      f'run summon minecraft:marker ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","{r}"]}}',
      f'execute as {R_} run {g.fn("u/clamp16")}')                              # new core util: pull inside r 16 (Q9)
tl.at(5, f'execute positioned as {R_} run function rlk:mboss/mv/glide {{t:9}}')  # the swoop, t5-14
tl.at(B5_CUP, g.hz_opts(kb=KB['heavy'], sfx=0), f'execute at {R_} positioned ~ {CY} ~ run ' + g.hz_disc(10.0, B5_DET - B5_CUP, DMG['b5']), <decals>)
```

The C → L0 direction for an L0 near the centre falls back to S → L0: test `execute at C if entity A distance=..1` and use `facing entity A` from the body instead.

## 9. Checks

- The dome tell is 22 t; strike at clip 53.
- A player at 10.5 b from R is untouched; a player at 9.9 b takes 2.6.
- A dash pressed at t49 avoids it.
- |C R| ≤ 16.
- No hazard before t31.
- After the end, the groggy begins with her back to the player.
- The heal orbs are gone at t92.
