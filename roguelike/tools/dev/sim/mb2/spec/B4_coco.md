# B4 달빛 축복 / 2단 코코볼 (Moonlight Blessing): implementation spec

| field | value |
|---|---|
| pattern | id 14, key `coco`, form butterfly, kind normal |
| clip | `coco`, 76 t, events wrap 5, orb1 19, ball 30, ball_open 42, orb2 46 |
| pattern end | t98 = orb 2 launch 46 + its life 50 + 2. Set with `g.set_len`, or the stub's `B4_END`. The clip ends at 76 and the rig returns to idle_b while the orbs fly. |
| element | Dendro (7) |
| coefficient | 1.5 per orb (`DMG['b4']` 150), **one hit per orb** (contact or burst), at most 3.0 |
| recover | 20 t |

## 1. Footage and plan check

Source: v3 C, 20.22-24.20 s, real time (`understand/v3.md` §3 C). I re-checked `sheet_orb1_replay_26.30-28.10.jpg` and `k_orb1_fate`. Tick 0 = the Pyro → Dendro switch (20.35 s).

| event | footage tick | plan / rig | verdict |
|---|---|---|---|
| glides forward 1-2 b, wings to flat | 0-4 | — | |
| **wrap**: both wings curl forward into a ring; a lime core lights at her chest | 5-9 | wrap 5 | ok |
| charge: lime streak lines converge, the core grows to about 0.4 H | 10-15 | | |
| wings snap open | 16-18 | | |
| **orb 1** released at chest height, 1 m ahead: a 1.7 m translucent lime sphere with 2-3 gyroscope rings | 19 | orb1 19 | ok |
| orb 1 drifts toward the player and sinks to about 0.5 m above the floor | 20-24 | | |
| lime ground burst r 2-2.5 where orb 1 was | 27-29 | — | see below |
| **cocoon ball**: wings wrapped into a ball about 3.4 b across, drifting 1-2 m toward the player | 30-42 | ball 30-42 | ok |
| ball opens | 42-45 | ball_open 42 | ok |
| **orb 2** launched from her side with a lime ring | 46-48 | orb2 46 | ok |
| flash at the player; orb 2 detonation, radial V-blades 5-6 m across (16.5 % max HP) | 49-50 | — | |
| recovery, hovering about 2 b in front of the player | 51-76 | total 76 | ok |

- **Orb behaviour.** In the footage orb 1 lived only about 8-10 t (sank and burst near the floor) and orb 2 hit point-blank 4 t after its launch: the player stood close.
- The caption and the PDF say the orbs are **slow, strongly homing and long-range**. The plan: "steer toward the player for about 40 t, then burst with radial ground blades r 2.5-3. A dash dodges them."
- **Keep the plan.** The footage's short lives are what slow homers do at point blank. With the orbs at 0.3 b/t, a player 2-3 b away gets the same 8-10 t contact as in the video.

## 2. AI

- **Bands and weights:** mid ×1, far ×1. Never melee.
  - The core's prep switches the look to Dendro (from Pyro) 8 t ahead.
- **Approach:** t0-4 she glides 1.5 b toward the player (as in the footage), only while she is farther than 6.5 b. During the ball (t30-42) she drifts up to 1.5 b toward the player but never closer than 5 b; before each launch (t17, t44) she backs off to 5 b if needed (`mv/away {d:0.2}`).
- **Facing:**
  - t0: `face/player`, then `face/track` all pattern long (no lock: the orbs home).
- **Orb aim:** at launch, the orb is turned toward the player's chest (`facing entity @e[tag=rlk_body] feet` + 0.9); then `pj/steer`.

## 3. Projectiles: the two orbs

| property | value |
|---|---|
| count | 2 (orb 1 at t19, orb 2 at t46); at most 2 live |
| carrier | `item_display` tagged `rlk_mb_bf_p14o`, carrying the rig's **orb prop** (manifest prop `orb`: a 1.7 b lime glass sphere + 2 gyroscope rings). Call `rig/prop/orb` at the launch point and use its sphere display as the `pj` prop; the two ring displays ride it as passengers and spin with looping transformations. Fallback: the kit's `tc:orb` look in a prop. |
| spawn | orb 1: chest, 1.2 b ahead, i.e. body frame ^0 ^3.0 ^1.2 (the core anchor at orb1 is (0, 3.16, -0.23), which is ^0 ^3.16 ^0.23; push it 1 b forward). Orb 2: her right side ^-1.2 ^3.0 ^0.8 ("from her side"). |
| speed | **0.25 b/t**: `pj_launch(0.25, …)`, giving `spd` 2 and 1 sub-step of 0.25 per tick. **Warning:** the framework rounds the speed up to 0.25-b sub-steps (`pjN = ceil(spd·0.4)`), so the stub's `pj_launch(0.35, …)` (spd 4) and the plan's 0.3 (spd 3) both fly at **0.5 b/t**, which is not slow. 0.25 is about a walk (0.22) and slower than a sprint (0.28), which matches "slow". |
| homing | `pj_steer(9)` each tick, ages 1..40: ≤ 9° yaw and pitch per tick. Turn radius = 0.25 / 0.157, about 1.6 b. Pitch is clamped ±60°. It aims at the player's feet + 0.9, so the orb glides at about 0.9 b above the floor near the player, rolling over the floor like the footage's sinking orb. |
| life | **40 t as a `pj`**, then 10 t as a still prop: `pj_launch(0.25, 40, 150, 0.8)`. The `pj` speed cannot go below one 0.25 b sub-step per tick (`pjN` minimum 1), so the stop is done by ending the `pj` life, not with `mbPjV`. |
| hit radius | `hr` 0.8, i.e. a 1.1 b sphere around the point 0.9 b below the prop (against the player's feet) |
| burst | `pj_end` **event 2** (life over at age 40): `#pjKeep 1`, so the orb is released as a plain, harmless entity that stays where it is. Place a burst hazard `hz_disc(2.8, 10, 150)` on the floor under it, **in the orb's group** (`#hzGrp = @s mbPjG`). The pattern's orb tick keeps counting `mbT`, pulses it for 10 t, and at age 50 plays the burst fx and kills it, on the same tick as the hazard strike. |
| contact | event 4 (hit) → `#pjKeep 0`: it pops with the burst fx. Contact is only possible before age 40 (afterwards it is no longer a `pj`), so no burst decal exists yet when it pops. |
| wall | event 1 → the burst fx, removed (its group is unused, so no damage) |
| cap | one hit per orb (contact or burst); two orbs = 3.0 max |
| element / KB | Dendro (`#pjEl 7`), `#pjKB 2` (light); the burst hazard KB 3 |
| group | `g.GRP_NEW` before each launch; `pj_opts(grp=True)`; the burst hazard copies the orb's `mbPjG` |

## 4. Per-tick timeline

| t | rig | mechanics | fx | sound |
|---|---|---|---|---|
| 0 | wings to flat | `face/player`; glide toward the player (`mv/toward {d:0.3}` t0-4, only beyond 6.5 b) | | |
| **5** | **wrap** | | core glow `tc:glow #D2FA8E 0.4→1.0 l14/f3 bb center` at the core anchor | `block.beacon.power_select` 0.5/1.8 |
| 10-15 | charge | | converging streaks: 2 per tick `tc:slash #D0F0C0 1.6→0.6 l4/f1` at the core ± 2.5 b (random yaw/pitch), `move` toward the core; the core `tc:orb #D2FA8E 0.5→1.0 l6/f2 bb center` at t10 and t13 | `block.conduit.activate` 0.4/1.6 at t10, `block.amethyst_block.resonate` 0.5/1.4 at t14 |
| 16-18 | wings snap open | | | `entity.ender_dragon.flap` 0.5/1.6 at t16 |
| **19** | **orb 1** | `GRP_NEW`; orb 1 launch (§3) | launch ring `tc:ring #D0F0C0 1.5→3.5 l4/f2` (vertical, facing the player) at the spawn | `entity.breeze.shoot` 0.5/1.2, `block.amethyst_block.chime` 0.6/1.5, `entity.allay.item_thrown` 0.5/0.8 |
| 20.. | | orb flight (§5 below) | orb trail every 2 t | at the orb, every 20 t: `block.beacon.ambient` 0.35/2.0 |
| **30** | **ball** | the ball drifts toward the player (`mv/toward {d:0.12}` t30-42, unless within 5 b) | the rig's `pod` prop (or the wing pose); `tc:swirl #CCF39C 2.0→3.2 l12/f3 bb center spin 160` at the core; glow `tc:glow #DEF6D9 1.0→1.8 l12/f4 bb center` | `entity.breeze.whirl` 0.6/1.2, `block.moss.place` 0.5/0.9 |
| 36 | | | | `entity.breeze.whirl` 0.4/1.0 |
| **42** | **ball open** | | `tc:ring #CCF39C 2.0→4.0 l4/f2 bb center` | `entity.ender_dragon.flap` 0.5/1.5 |
| **46** | **orb 2** | `GRP_NEW`; orb 2 launch from her right side | lime ring `tc:ring #D0F0C0 1.5→3.5 l5/f2` (vertical) | `entity.breeze.shoot` 0.6/1.0, `block.amethyst_block.chime` 0.6/1.3 |
| 59 | (orb 1 age 40) | orb 1 `pj` life ends (event 2) → still prop; burst decal r 2.8 (tell 10) | §6 | at the orb: `block.beacon.power_select` 0.4/1.9 |
| **69** | (orb 1 age 50) | **orb 1 burst** (unless it already popped) | burst (§7) | burst sound (§8) |
| 76 | clip ends → `idle_b` | `face/track`; keep ≥ 5 b | | |
| 86 | (orb 2 age 40) | orb 2 stops, burst decal | | |
| **96** | (orb 2 age 50) | **orb 2 burst** | | |
| 98 | end | `g.end()` (or earlier, when both orbs are gone and t ≥ 76) | | |

**Orb flight, per orb, per tick (age a):**
- a 1..40: `pj_steer(9)`.
- Every 2 t: `dust #E5FBC8 1.0` ×3 Δ(0.4,0.4,0.4) + `end_rod` ×1.
- Every 10 t: a floor shadow ring under it, `dust #B6E35A 0.8` ×10 on r 0.8 at the floor (it reads the depth).
- a 40: the `pj` life ends (event 2, keep 1), it stops, and the decal appears.
- a 41..49: the orb pulses: scale 1.0 ↔ 1.15 every 3 t via an interpolated transformation.
- a 50: burst.

## 5. Damage areas

- **Contact:** a sphere r 1.1 around the point 0.9 b below the orb, vs the player's feet. 150 %, Dendro, KB 2.
- **Burst:** a disc r 2.8 on the floor under the orb's age-40 position, height -0.5..3.5, strike at age 50. 150 %, Dendro, KB 3.
- Same group per orb, so 1 hit max per orb.

## 6. Telegraphs

- **The orb itself** is the telegraph for contact: 1.7 b, glowing, slow. Before orb 1 there are also the wrap and charge (t5-19, 14 t), and before orb 2 the ball (t30-46).
  - Earliest possible contact: at the band minimum of 4 b, the orb spawns 1.2 b ahead and hits at 1.1 b, so it travels 1.7 b at 0.25 b/t: **about 7 t after the launch**.
  - The readable warning is therefore counted from the charge, not the launch:
    - orb 1: the wrap / core glow at t5, 21 t before the earliest contact at about t26;
    - orb 2: the ball opening at t42, 11 t before the earliest contact at about t53.
  - **Recommendation:** keep `ai/idle_b`'s 5 b minimum during B4. If she is closer than 5 b at t17 or t44, she drifts back 0.2 b/t before the launch, so each orb gets ≥ 10 t of flight before contact.
- **Burst: 10 t.** A disc fill r 2.8 under the stopped orb: lime `#B6E35A` growing over 10 t, with 10 radial blade marks (the kit's `vmark` or short `tc:slash` floor lines) showing the spike pattern.

## 7. FX detail

Palette (v3 §5):
- sphere `#D2FA8E` / `#9CDB7D` / `#63BB65`, rings `#D0F0C0` / `#95C0A3`, dark `#38896B`;
- burst `#EAFDD9` / `#B4F7B6` / `#DEFCAD` / `#83D394`;
- ground blades `#B4EB68` / `#80BD77`, dark `#2C686D` / `#356F64`;
- ball glow `#CCF39C` / `#DEF6D9` on `#307181` / `#5B9E92`.

**Burst** (age 50, or contact): radial V-shaped ground blades, 5-6 b across.
- 10 × `tc:shard` (or the kit's `blade`) at the orb's floor point:
  - rot `~36k -55` (tilted outward), `s 0.6→1.8 l8/f4`;
  - colours alternate `#B4EB68` / `#80BD77`;
  - `move` outward 0.6.
- `tc:burst #EAFDD9 1.5→5.6 l5/f2 rot ~ 90`.
- `tc:glow #DEFCAD 3.0→5.0 l6/f3 bb center` at +1 b.
- `flash{color:[0.92,0.99,0.85,0.9]}` ×1.
- `dust #83D394 1.5` ×20 Δ(1.6,0.4,1.6).
- `tc:leaf #B4EB68` ×4.

## 8. Sound

Taken from v3 §6:
- orb charge 20.65-21.30 s (thin rising sparkle);
- orb flight 21.32-21.65 (faint whir);
- bursts 21.82-21.86 and 22.85-23.14 (airy boom + leafy crackle);
- ball 21.86-22.26 (swirling rustle).

**Burst layers:** `entity.breeze.wind_burst` 0.8/1.0, `block.azalea_leaves.break` 0.8/1.0, `entity.generic.explode` 0.4/1.5, `block.big_dripleaf.break` 0.6/1.0; then `block.azalea_leaves.break` 0.5/1.2 one tick later.

Not yet used in the pack: `entity.allay.item_thrown`, `block.big_dripleaf.break`, `entity.breeze.whirl`.

## 9. Dodge window and fairness

- **Outrun:** the orb (0.25 b/t) is slower than a sprint (0.28) and about as fast as a walk. A sprinting player gains slowly.
  - After 40 t it stops and bursts 10 t later: keep moving 3 b away from the decal.
- **Dash sideways** when it is about 2 b away: with a 1.6 b turn radius and 3 b of dash it overshoots and circles. A second dash or a sprint clears it before age 40.
- **Fight it:** it cannot be destroyed (no aux).
- **At r 21:** the orb's homing cuts corners if a player runs in a circle along the wall, so the wall is where a dash is needed. Fair: two charges, 20 t regen.
- Worst case: two orbs converging from different angles (orb 1 at age 27-40 while orb 2 launches). Each is 1.5 and can hit once. The ≥ 27 t gap keeps them readable.

## 10. Diagram

```
   S (wrap 5-18) --orb1(t19)--> ~ ~ ~ homing 9°/t, 0.25 b/t ~ ~ ~>  P
                                                 \ age 40: stops, decal r2.8, burst age 50
   S (ball 30-42, drifts) --orb2(t46, her right side)--> ~ ~ ~ >   P
   dash sideways at ~2 b: it overshoots (turn radius ~1.6 b) and circles
```

## 11. Implementation sketch (`wing.py`, extends the stub)

```python
# launch: rig orb prop at the spawn point, aimed at the player's chest; pj speed 2 (0.25 b/t)
g.pw(k, 'orb_new', [..., f'function {NS}{RIG_DIR}/prop/orb', ...,   # tag its sphere rlk_mb_bf_p14o + p14n
     g.GRP_NEW, *g.pj_opts(el=EL_DENDRO, kb=KB['light'], grp=True),
     f'execute as @e[type=minecraft:item_display,tag={new},limit=1] at @s run ' + g.pj_launch(0.25, 40, DMG['b4'], 0.8)])
g.pw(k, 'orb', ['scoreboard players add @s mbT 1',
     f'execute if score @s mbT matches 1..40 run ' + g.pj_steer(9),
     f'execute if score @s mbT matches 50 run {g.fn(f"p/{k}/burst_fx")}', ...])     # burst fx + kill at age 50
# pj_end: ev 4 -> pop (keep 0); ev 2 (age 40) -> keep 1 + burst_tell (hz_disc r 2.8, tell 10, #hzGrp = @s mbPjG)
```

`pj_launch(0.25, …)` → `_tenths(0.25)` = 2 (Python rounds half to even) → spd 2 → exactly one 0.25 b sub-step per tick. Write `pj_launch(0.2, …)` if you prefer not to rely on the rounding.

## 12. Checks

- Orb effective speed 0.25 b/t.
- The steer is ≤ 9° per tick.
- One hit per orb even if the player touches it and then stands in the burst.
- A popped orb never leaves a decal.
- At age 40 the orb stops dead and is no longer a `pj` (touching it is harmless); the burst hazard strikes at age 50.
- The pattern end does not cut live orbs (the end is 98, or both gone).
- Live orb count ≤ 2.
