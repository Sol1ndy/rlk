# S3 Revert, groggy, turn and chain re-form: implementation spec

| field | value |
|---|---|
| owner | core: `form/revert` (in the B5 timeline), `groggy/*`, `recover/*`; the standalone `revert` clip for a no-blast revert |
| clips | inside `release`: shrink/flat 87, shatter 91, revert 92, land 96 (proposed retime; see B5). Then `groggy_h` (loop 40), `turn_h` 24, `chain_reform` 18. Standalone `revert`: 43 t, events shrink 30, flat 32, shatter 36, land 43. |
| groggy | **300 t** (15 s) from the landing: motionless, her back to the player, no tracking, no attacks, normal damage taken (no bonus) |
| after | the turn (24 t), the chain re-form (18 t); then the human rotation with **H2 forced first** (`#bfReq 2`, as in v4), then 4 human patterns before the next transformation |
| damage | none |

## 1. Footage and plan check

Source: v4 B/D, 11.45-31.30 s, real time (`understand/v4.md` §2 B-D). The revert itself is in v3 / v4 A (see B5).

| event | footage | plan / core | verdict |
|---|---|---|---|
| human form drops 1.5-2 b, lands upright, back to the player | E+39..E+43 | release 92-96 | ok |
| groggy: still, no turn or attack; 2 navy diamond plates hover above each shoulder; the big crescents not visible; no stun icon or fx | landing → +300 t (14.97 s) | 300 | ok |
| turns slowly, 180° at about 150°/s | 24 t | `turn_h` 24, `mv/turn` max 9°/t | ok |
| plates re-form: 4 crescents fly in and stack into a vertical chain at her left side; low thud | **turn +17 .. turn +35** (overlapping the turn's end); thud at turn +24 | `chain_reform` **after** the turn: +24 .. +42; the core's thud at +30 | **minor**: the footage overlaps by 7 t |
| tell of 달빛 점프 (the chain glows) | turn +37 | the forced H2 starts at about +46 (cool 4) | ok |

**Proposed (optional):** start `chain_reform` at turn +17 so the two overlap, as in the footage. The total turn + re-form becomes 35 t instead of 42. The H2 tell then begins at about +39. If the rig cannot blend the two clips, keep them sequential (the current core).

## 2. Per-tick timeline

### A. Revert (inside B5's clip; release ticks)

| t | rig | mechanics | fx | sound |
|---|---|---|---|---|
| 87 | shrink + flat lime | `look/flat` (core) | lime shard motes at the wing anchors every 2 t (B5) | `block.beacon.deactivate` 0.6/1.8 |
| 91 | shatter | | 10 shard cards + lime glass particles (B5) | `block.amethyst_cluster.break` 0.7/1.5, `block.glass.break` 0.4/1.6, `entity.illusioner.mirror_move` 0.6/1.4 |
| 92 | human form, 1.5-2 b up | `form/revert`: human state and hitbox, `dew/clear` (orbs fade with a `poof`), HUD | wing-shard drift: `dust #E7FD7A 0.8` ×8 Δ(1.5,1,1.5) | |
| 96 | land | the B5 pattern ends → `groggy/begin` | landing: `poof` ×8, moss block ×10, lime ring r 1.3 | `block.moss.fall` 0.8/1.0, `entity.iron_golem.step` 0.4/1.4 |

### B. Groggy (`#bfT` 0..300 from `groggy/begin`)

| t | rig | mechanics | fx | sound |
|---|---|---|---|---|
| 0 | `groggy_h` (loop 40); body yaw = away from the player (+180) | `#bfSt groggy`; the HUD groggy bar (300 t, colour 9 / lime); `#mbNoLeash 0` | | `block.respawn_anchor.deplete` 0.6/1.2 |
| every 10 t | | | dazed motes: `dust #B6E35A 0.7` ×2 at ^ ^2.4 ^ Δ(0.5,0.3,0.5) + `end_rod` ×1 (the core's `fx/groggy`). Shoulder plates drift (rig). | |
| 20 | | if `#bfCoc 1` (still debuffed): `dew/spawn1` (one heal orb) | the orb spawn fx | `block.amethyst_block.chime` 0.6/1.4 |
| every 100 t (t100, t200) | | | a faint lime ring at her feet `tc:ring #B6E35A 1.5→2.5 l8/f4 rot ~ 90` (it reads "still dazed") | `block.beacon.ambient` 0.25/0.8 (optional) |
| 280 | | | stirring: `tc:star #E5FBC8 0.2→0.7 l4/f2` at the shoulder plates | `entity.breeze.idle_air` 0.3/1.0 |
| 300 | | `recover/begin` | | |

### C. Turn and chain re-form (`#bfT` from `recover/begin`)

| t | rig | mechanics | fx | sound |
|---|---|---|---|---|
| 0 | `turn_h` | `mv/turn {max:9}` each tick 1..24 (≥ 180° in 24 t) | | `entity.breeze.idle_air` 0.4/1.2 |
| 17 (overlap option) or 24 | `chain_reform` | | the crescents fly in: 4 × `tc:crescent #394B75 0.4→1.1 l6/f2 roll 90`, moving from 2 b out to her left-side chain position (`move` inward) | |
| re-form +6 (turn +24 or +30) | plates stack | | `dust #B6E35A 1.1` ×10 at her left (^0.7 ^1.8 ^0); `tc:glow #C2E18C 0.4→1.0 l6/f2 bb center` at hand_l_a | `block.chain.place` 0.8/0.8, `block.amethyst_block.place` 0.7/1.2 |
| re-form +18 | done | `groggy/end`: human counters (4 patterns, no time limit), `#bfReq 2` (H2 first unless locked), `#bfCool 4` → idle → H2 | | |

### D. Standalone `revert` clip (43 t)

For a butterfly → human change **without** the blast: tests, or a future soft end. Not used in the normal rotation (B5 contains its own revert).

| t | rig | fx | sound |
|---|---|---|---|
| 0-29 | hover rises to 2 b, slow flaps | | `entity.ender_dragon.flap` 0.4/1.7 at 6 and 18 |
| 30 | shrink | lime shard motes at the wing anchors | `block.beacon.deactivate` 0.6/1.8 |
| 32 | flat | (the core: `look/flat`) | |
| 36 | shatter (form → human) | shard cards ×8, lime glass ×16 | `block.amethyst_cluster.break` 0.7/1.5, `entity.illusioner.mirror_move` 0.6/1.4 |
| 43 | land | `poof` ×8, lime ring | `block.moss.fall` 0.8/1.0 |

## 3. AI

- **Groggy:** no AI, no locomotion, no tracking. The body yaw stays where `groggy/begin` set it (away from the player).
- **Turn:** `mv/turn {max:9}` toward the player.
- **After the re-form:** normal human idle, then H2 (forced).
- The groggy is a big damage window for the player. With the cure reward (CRIT +15 %, DMG +50 %) it is the intended payoff. The footage shows 2 % boss HP for a Lv.103 boss; ours is relative to `hp 240`.

## 4. Fairness

- No hazards. The heal orb at t20 (if still debuffed) gives a no-heal character the cure before the burst window.
- The turn and re-form (42 t, or 35) are a clear "she is back" read before H2's tell.

## 5. Diagram

```
  t96 land (back to P)       groggy 300 t              turn 24 t        chain 18 t      H2 tell
        S  ← P                S  ◦(heal orb if debuffed)   S ↻ → P        S ][ (chain)    ...
```

## 6. Checks

- `#bfSt` groggy for exactly 300 t.
- No `face/track` calls in groggy.
- One heal orb at groggy t20 only if `#bfCoc 1`.
- H2 is the first pattern after the groggy (unless `#mbLock`).
- The human counters reset to 4 patterns.
