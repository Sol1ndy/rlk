# H2 달빛 점프 (Moonlit Leap): implementation spec

| field | value |
|---|---|
| pattern | id 2, key `jump`, form human, kind normal |
| clip | `kick_jump`, 65 t |
| events | rig now: tell 0, sweep 13, jump 33, disc 40, land 55. **Proposed** (§1): tell 0, sweep 13, jump 33, orb 45, kick 52, impact 55, land 59. |
| lead | 0 |
| close-in | `close=3.0`: the core's burst-run (0.7 b/t, ≤ 12 t) to 3 b before the start |
| element | Dendro (7) |
| coefficients | sweep 0.9 (`DMG['h2a']` 90); disc 1.4 (`DMG['h2b']` 140) |
| hits | 2 separate hits, at most 2.3 |
| recover | 16 t |
| special | the first pattern after every groggy (the core forces `#bfReq 2`), as in v4 |

## 1. Footage and plan check

Sources:
- v1 25.33-28.60 s, real time (`understand/v1.md` §3 B). I re-checked `sheet_jumpkick_b_26.87-28.33.jpg` frame by frame (f1612-f1700).
- v4 28.45-31.30 s (`understand/v4.md` §2 D), the post-groggy instance.

Tick 0 = the tell (v1 25.33 s / v4 28.45 s).

| event | v1 tick | v4 tick | plan / rig | verdict |
|---|---|---|---|---|
| tell: arm shard (v1) or crescent chain (v4) glows lime | 0-9 | 0-6 | tell 0-13 | ok |
| pivot | 9-11 | 7-10 | — | |
| **sweep** (low band, knee height) | 12-19 (full at 14) | 12-19 | 13-19 | ok |
| trail fades, small crescent mark on the floor | 20-25 | — | — | fx |
| stand, chamber | 25-30 | — | — | |
| spiral jump start | 33 | 31.6 | 33 | ok |
| orb forms at the raised foot (about 1.3 m, swirl bands) | 45 | — | **disc 40** | **mismatch** |
| star flash above the player | 51.7 | 52 | — | |
| orb axe-kicked down | 53 | — | — | |
| **disc impact** (r about 1.5, dust r 2) | **55.7** | **53.6** | **impact 50** | **mismatch: 5 t early** |
| she lands about 1-2 b from the player | 59.7 | — | land 55 | mismatch |
| idle | 62-65 | — | 65 | ok |

**Fixes:**
- Retime the rig events to orb 45, kick 52, impact 55, land 59. Clip length stays 65.
- Lock the disc on the player's floor position at **t43**, i.e. 12 t before the impact. The footage targets the player's position about 5 t before impact; 12 t is the readable version.
- Disc radius: footage about 1.5 b, plan 2.5 b. **Keep 2.5** (readability and a forgiving read).
- Sweep: plan r 3; footage ±2.5 m at knee height, and a player at 4-5 m was untouched. Keep r 3.
- Recommended addition: make the sweep jumpable (`y1 1.0`, act 4), since it is knee height in both videos. See Q12.

## 2. AI

- **Bands and weights:** melee ×1, mid ×1. Never far.
- **Approach:** the core's close-in burst-run to ≤ 3.0 b (`close=3.0`), then the start.
- **Facing:**
  - t0: `face/player`.
  - t0..10: `face/track`.
  - t11..30: held. The sweep is a 360° spin, so facing is irrelevant.
  - t31: `face/player`.
  - t31..43: `face/track`.
  - t43: locked. She flies on the locked line.
- **Aim locks:**
  - sweep: centred on her body at t3 (the body does not move until t33);
  - jump dest: `g.dest(3.5, 0.8)` at **t33**, giving marker A;
  - disc: `g.lockp()` at **t43**, giving marker L on the floor under the player.

## 3. Body travel

| ticks | travel |
|---|---|
| 0-32 | none |
| 33-58 | glide S → A over 26 t (`mv/glide {t:26}` at t33; the rig shows the arc and apex of about 2.5 b) |
| 59-65 | none |

## 4. Per-tick timeline

| t | rig | mechanics | fx | sound |
|---|---|---|---|---|
| 0 | tell: the crescent chain lines up at her left and glows (rig `bfRigTell 1`) | `face/player` | `tc:glow #E5FBC8 0.4→1.2 l12/f4 bb center` at hand_l_a; `dust #B8F060 0.9` ×3 at hand_l_a every 2 t until t12; `end_rod` ×1 every 4 t | `block.amethyst_block.chime` 0.7/1.6, `block.beacon.ambient` 0.35/1.8 |
| **3** | | **sweep hazard: disc r 3 at S, tell 10, act 4, y1 1.0** | disc fill decal r 3, tell cue | `block.amethyst_block.resonate` 0.35/1.6 |
| 5 | | | | `block.amethyst_block.chime` 0.5/1.8 |
| 10 | pivot | | `tc:slash #B8F060 1.2→1.6 l3/f1 rot ~ 90` at ^ ^0.1 ^0.3 (lime streak on the trailing foot) | `block.amethyst_block.resonate` 0.4/1.6 |
| **13** | sweep starts | **strike; active 13-16** | the sweep band (§7 A) | `entity.player.attack.sweep` 0.8/1.1, `entity.breeze.whirl` 0.6/1.4, `block.moss.break` 0.6/1.0 |
| 14-16 | spin | | the band continues: second card at t15 | |
| 17 | follow-through | | leaf debris `tc:leaf #A8DF74` ×6 radial, `move` 2 b outward, l12/f6 | `block.moss.fall` 0.7/0.8 (the low thump at v1 26.20 s) |
| 18 | | | | `entity.player.attack.sweep` 0.4/1.4 (swish tail) |
| 20 | trail fades | | floor mark `tc:moon #B9E4A7 1.0→1.3 l20/f8 rot ~ 90` at ^ ^0.05 ^0.6 | |
| 25-32 | stand, chamber | | | |
| **33** | jump | `face/player`, dest A, glide 26 t | spiral ribbons: `tc:swirl #AADB84 1.5→3.0 l8/f3 bb center spin 170` at ^ ^1.2 ^0 and again at t37 (^ ^2.4 ^0); helix dust `#AADB84 1.0` ×2 per tick, t33-41, on a rising r 1.4 helix (precomputed offsets) | `entity.breeze.charge` 0.6/1.1, `entity.breeze.whirl` 0.5/1.0 |
| 36 | airborne | | | `item.elytra.flying` 0.2/1.4 |
| 38 | | | | `entity.breeze.idle_air` 0.4/0.8 (the low rumble from 27.31 s) |
| **43** | | **lock L; disc hazard r 2.5 at L, tell 12, kb 4** | disc fill decal r 2.5 at L; target mark `tc:star #E5FBC8 0.3→0.8 l12/f3 bb center` at L + (0,3,0) | `block.amethyst_cluster.hit` 0.45/1.8 |
| 45 | orb at her raised foot | | orb `tc:orb #C1F788 0.6→1.3 l8/f2 bb center` at foot_r (rig at `orb`); `tc:ring #D4F8C6 1.2→1.8 l8/f2 bb center spin 120` | `block.conduit.activate` 0.4/1.8 |
| 47-50 | somersault, orb overhead | | orb trail: `dust #D4F8C6 1.0` ×3 per tick at foot_r | `item.trident.riptide_1` 0.25/1.6 at 48 |
| 51 | | | star flash `tc:star #FBFDF4 0.4→1.8 l4/f2 bb center` at the orb | `entity.firework_rocket.twinkle` 0.6/1.4 |
| **52** | **kick** | | orb burst: `tc:burst #E4F8CC 2.0→4.0 l4/f2 bb center`; two wind crescents `tc:ring #FFFFFF 6.0→8.1 l5/f2`, one horizontal (`rot ~ 90`) and one vertical, at the orb | `entity.breeze.shoot` 0.6/1.2, `entity.player.attack.sweep` 0.7/0.9 |
| 53-54 | | | falling disc: `tc:glow #A6E282 4.6→5.0 l3/f0 rot ~ 90 move (0,-2.6,0)` from L + (0,2.7,0); rim `tc:ring #C2ECB0 5.4→5.8 l3/f0 rot ~ 90` with the same move | |
| **55** | **impact** | **disc strike** | impact (§7 B) | `entity.generic.explode` 0.4/1.4, `entity.breeze.wind_burst` 0.7/0.8, `block.azalea_leaves.break` 0.8/1.0, `block.moss.break` 0.6/0.9 |
| 56-62 | | | dust cloud: `dust #A8DF74 3.0` ×4 and `dust #8DC07E 3.5` ×3 at L + (0,1,0) Δ(1.2,0.8,1.2) every 2 t | `block.azalea_leaves.break` 0.4/1.2 at 57 |
| 59 | lands | | `poof` ×6, moss block ×8 | `block.moss.fall` 0.6/1.0 |
| 65 | end | `g.end()` | | |

## 5. Damage areas

### Sweep (t3 → strike t13, active 13-16)

- `hz_opts(act=4, y1=1.0, kb=3, sfx=0)` then `execute positioned ~ 201 ~ run g.hz_disc(3.0, 10, 90)` at S.
- **Shape:** a filled disc of r 3.0 around her floor point, height -0.5..1.0 b (feet test), active for 4 ticks.
- Dendro, 0.9, KB 3 (away from her). One hit.
- If the jumpable variant is rejected, use the default height (-0.5..3.5) and act 6.

### Disc (t43 → strike t55)

- `hz_opts(kb=4, sfx=0)` then `execute at L run g.hz_disc(2.5, 12, 140)`.
- **Shape:** a filled disc of r 2.5 at L, height -0.5..3.5.
- Dendro, 1.4, KB 4 (heavy, radial from L). One hit.

The two hazards are separate (not one group): a player caught by both takes 2.3.

## 6. Telegraphs

- **Sweep: 10 t.**
  - The lime disc fill grows over r 3 (t3 → 13).
  - The chain glow (t0) and the chime are the earlier read.
  - In the jumpable variant, add a low ring outline at y 0.5 (`dust #D6FAC5 0.8` ×18 around r 3 at t9 and t11) to signal "low".
- **Disc: 12 t.**
  - A disc fill r 2.5 at L, plus a star mark hovering 3 b above L.
  - Then the orb, the flash and the falling disc (t45-54) draw the eye to L.

## 7. FX detail

Palette (v1 §5, v4 §5):
- sweep `#D6FAC5` / `#B9E4A7` core, `#94BC90` mid, `#3A765D` dark;
- chain glow `#C2E18C`, core `#DCF9DC`;
- spiral `#AADB84`;
- orb `#C1F788` / `#D4F8C6` / `#8DD57A`;
- star `#FBFDF4` / `#DAF7B2`;
- disc rim `#C2ECB0`, fill `#A6E282` / `#84C75D`;
- dust `#A8DF74` / `#8DC07E`.

### A. Sweep (t13-16)

A horizontal lime band at knee height, about ±2.5-3 b around her, with flame-like leaf flares, spinning once.
- t13: underlay `tc:crescent #3A765D 5.6→6.0 l4/f2` (flat, horizontal) at ^ ^0.45 ^0, `spin 170`.
- t13: overlay `tc:crescent #D6FAC5 5.4→6.0 l4/f2 spin 170` at ^ ^0.5 ^0.
- t15: a second pair rotated 180° (yaw +180), so the two halves give a full 360° band.
- `dust #B9E4A7 1.0` ×16 on a ring of r 2.8 at y 0.4 (t14).
- `sweep_attack` ×2 at ^ ^0.5 ^1.5.

### B. Disc impact (t55)

- `tc:burst #A6E282 1.0→5.5 l5/f2 rot ~ 90` at L + (0,0.08,0).
- `tc:glow #C2ECB0 4.0→5.0 l6/f3 rot ~ 90`.
- `flash{color:[0.76,0.93,0.69,0.8]}` ×1 at L + (0,0.6,0).
- `dust #84C75D 1.6` ×20 Δ(1.2,0.2,1.2).
- `tc:leaf` ×6 outward, l14/f6.
- `cherry_leaves` ×10 Δ(1.2,0.5,1.2): tint does not apply, so they are optional; prefer the lime leaf cards.

## 8. Sound

Taken from v1 §6 and v4 §6: tell shimmer 25.49-25.85 s, low thump 26.20, swish 26.27-26.44, spiral jump 27.0-27.75 with rumble, orb sparkle 27.6-27.93, disc impact 28.16-28.30.

Not yet used in the pack:
- `entity.breeze.whirl`;
- `entity.breeze.idle_air`;
- `block.moss.fall`.

## 9. Dodge window and fairness

**Sweep.** She stands about 3 b from the player (close-in).
- Out: from 0.5-3 b to more than 3.3 b, at most 2.8 b in 10 t (sprint).
- Jump (variant): a vanilla jump keeps the feet at or above 1.0 b on ticks +3..+8 after the press. The jump press window is **t8-t10**. A press at t10 clears t13-t18, which covers act 13-16. It is a 3-tick skill read.
- Dash: the i-frames must cover t13-16, so press at **t11-t13** (6 t of i-frames from the press).

**Disc.**
- Move out of r 2.5 from L: 2.8 b in 12 t, sprint 3.4 b, OK.
- Or dash at t50-55.

Fair: one stationary 360° read, then a targeted drop with a 12 t marker.

**At r 21.** L is clamped inside the safe disc, and moving in any direction escapes the disc. There is no wall trap.

## 10. Diagram

```
 sweep (t3 → 13..16)                disc (t43 → 55)
      . - - - .                        S - - jump (33..58) - - > A
    .     r3    .                                      .--.
   .      S      .   <- P (≤ 3 b)                     ( L  )  r 2.5   (P at t43)
    .           .                                      '--'
      ' - - - '                         she lands at A, 0.8 b short of P's t33 spot
 knee height (y ≤ 1.0): jumpable
```

## 11. Implementation sketch (`human.py`)

```python
H2_ORB, H2_KICK = ev_or('kick_jump', 'orb', 45), ev_or('kick_jump', 'kick', 52)
H2_IMPACT, H2_LAND = ev_or('kick_jump', 'impact', 55), ev_or('kick_jump', 'land', 59)
H2_LOCK = H2_IMPACT - 12                    # 43
tl.at(3, g.hz_opts(act=4, y1=1.0, kb=KB['default'], sfx=0), f'execute positioned ~ {CY} ~ run ' + g.hz_disc(3.0, 10, DMG['h2a']))
tl.at(33, R('face/player'), g.dest(3.5, 0.8), g.keep(a), f'execute positioned as {A_} run function rlk:mboss/mv/glide {{t:26}}')
tl.at(H2_LOCK, g.lockp(), g.keep(b, 'rlk_mb_bf_lock'), g.hz_opts(kb=KB['heavy'], sfx=0),
      f'execute at {B_} run ' + g.hz_disc(2.5, H2_IMPACT - H2_LOCK, DMG['h2b']))
```

## 12. Checks

- Hazards: sweep tell 10 / act 4 / y1 1.0; disc tell 12 with its strike at clip 55.
- The post-groggy forced H2 starts after `chain_reform`: the tell glow continues the re-formed chain.
- Body end within 1 b of A.
