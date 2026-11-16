# S2 Transformation (human → butterfly) and the 달빛 고치 debuff: implementation spec

| field | value |
|---|---|
| owner | core service pattern 20 (`transform`), `form/sphere`, `coc/apply`, `dew/spawn` |
| clip | `transform`, 30 t. Rig events now: sheath 0, folded 4, open 4, sphere 6, spread 12, ripple 14. **Proposed:** add `rings` 9 (and keep `ripple` as an alias, or drop it). |
| trigger | at a decision point when the human stretch is over: the first time after 600 t of fight or 5 human patterns (whichever comes first); after each groggy, after 4 human patterns |
| damage | the debuff: **20 % of the current HP**, non-lethal (floor 1), no element, unavoidable (not a hit: no dash, defence or shield) |
| after | butterfly form; the first butterfly decision after `#bfCool 16` |

## 1. Footage and plan check

Source: v2 C, 23.70-26.95 s, real time (`understand/v2.md` §2 C). I re-checked `sheet_transform_crop_23.60-24.90.jpg` frame by frame. Tick 0 = the sheath (24.10 s).

| event | footage tick | plan / rig | verdict |
|---|---|---|---|
| (in the footage she is still airborne from the 광폭한 진공 backflip, about 3 b up) | -7..0 | — | ours starts grounded at a pattern boundary (Q20) |
| **green vertical glow sheath** wraps her lower body; slight descent | 0-2 | sheath 0 | ok |
| hovers upright, antennae flare | 3 | | |
| **folded wings open partially** (compact lime panels about 1 m) | 4 | folded 4, open 4 | ok |
| the debuff icon appears on the party slot | 4.7 | | |
| core flash: a yellow-white flare at her chest; the wing silhouettes snap out | 5 | | |
| **light sphere** r 2-2.5, screen bloom | 6-8 | sphere 6 | ok |
| **player HP -17.4 % of current** | 8 | plan: applied at the sphere (6), 20 % | ok (2 t early is fine) |
| sphere bursts into **concentric ripple rings** (vertical arcs + a floor ring) to r 4-5, radial speed lines | **9-11** | rig `ripple` **14**; the core reads `rings` (missing, fallback 8) | **mismatch: rename to `rings`, set to 9** |
| wings fully unfurled; hovers 1-1.5 b | 12-16 | spread 12 | ok |
| show-off flight (side and back views) | 16-56 | — | optional; ours goes to `idle_b` at 30 |

Total: plan about 30 t. The footage settles by t16-20; the clip is 30. Ok.

## 2. AI

- At the start, `face/player` (instant). No tracking during the clip; the rig is a stationary show.
- The look is set to Dendro at t0 (the core does it).
- No body travel: the rig lifts her to the 1.2 b hover from t4 to t12.

## 3. Per-tick timeline

| t | rig | mechanics | fx | sound |
|---|---|---|---|---|
| 0 | sheath (core glow) | `look/dendro`, `face/player` | green sheath: `tc:glow #B5F089 0.6→1.4 l6/f2 bb vertical` at ^ ^1.0 ^ (a vertical glow column); `dust #B5F089 1.3` ×10 Δ(0.3,0.7,0.3) at ^ ^1.0 ^; `dust #508B90 0.8` ×4 (dark teal edge) | `block.beacon.power_select` 0.8/1.6, `block.respawn_anchor.charge` 0.3/1.6 |
| 1-3 | | | `dust #C2FA72 1.2` ×6 per tick at ^ ^1.0 ^ Δ(0.25,0.6,0.25) | |
| **4** | folded wings open partially | | `end_rod` ×6 speed 0.05 at ^ ^2.3 ^; folded-wing rim glint `tc:star #EFFDA2 0.3→0.9 l3/f1 bb center` at ^±0.6 ^2.6 ^-0.3 | `entity.ender_dragon.flap` 0.6/1.5 |
| 5 | core flash | | `tc:star #FAFCD4 0.4→2.0 l3/f1 bb center` at the core anchor; `dust #FAFCD4 1.6` ×12 at ^ ^2.2 ^ | |
| **6** | **light sphere** | **`form/sphere`: `coc/apply` (debuff) + `dew/spawn` (3 heal orbs)** | sphere: `tc:orb #F8FDBB 0.8→5.0 l7/f3 bb center spin 30` at ^ ^1.6 ^; `tc:glow #FAFCD4 2.0→6.5 l6/f3 bb center`; 3 vertical particle rings r 2.5 (yaw 0/60/120) + a horizontal ring r 2.5 at y 1.6 (`vring` / `ring` in core); bloom `flash{color:[0.97,0.99,0.73,1.0]}` ×1. On the player: the debuff fx (§5). | `item.totem.use` 0.5/1.4, `entity.elder_guardian.curse` 0.4/1.6, `block.beacon.activate` 0.7/1.8 |
| 7-8 | sphere holds | | `tc:orb` fades (its fade) | |
| **9** | **rings** (proposed event) | | ripple 1: floor `tc:ring #BDE592 3.0→7.0 l9/f4 rot ~ 90` (r 3); vertical rings `tc:ring #D0F2B9 2.0→7.0 l8/f4`, one facing her and one at yaw 90; radial speed lines: 8 × `tc:slash #5BEAA0 1.5→3.5 l4/f2`, radial at y 1.4 | `entity.breeze.wind_burst` 0.8/0.8, `block.amethyst_block.resonate` 0.7/1.0 |
| 10 | | | ripple 2: floor ring r 4 (`tc:ring #BDE592 6.0→9.3 l8/f4 rot ~ 90`) + particle ring r 4 | |
| 11 | | | ripple 3: floor ring r 5 (`tc:ring #428B71 8.0→11.6 l8/f4 rot ~ 90`) + particle ring r 5 | `entity.ender_dragon.flap` 0.6/1.5 (the swell) |
| **12** | wings fully spread | | wing-tip sparkle `tc:star #E5FBC8 0.2→0.8 l4/f2` at fwtip_l / fwtip_r | |
| 13 | | | | `entity.ender_dragon.flap` 0.5/1.5 |
| 16-29 | hover flaps | | lime motes from the wing tips every 4 t | `entity.phantom.flap` 0.3/1.6 at 18 and 24 |
| 30 | end | `g.end()` → `form/transform_done` (butterfly state, counters, `#bfCool 16`) | | |

## 4. The debuff 달빛 고치: mechanics (binding plan + core)

**Application, at t6 (`coc/apply`, as the player, unless dead, reviving or on a selection screen):**
- Damage = `curHealth × 20 / 100`, at least 1. Then `curHealth -= dmg`, floored at 1.
- The number is shown via `player/hurt_do` with `#elem 0`.
- It bypasses dash i-frames, defence and shields: it is a debuff tick.

**State while active:**
- player outgoing DMG on the boss × 0.5 (`#bfDmgPct 50`, module `incoming`);
- CRIT -100 (`#mbCritAdd -100`, through `items/hook/stat_buffs`), with forced crits undone in `incoming` (`coc/uncrit`);
- healing received × 0.6 (`#mbHealPct 60`, through `items/hook/on_heal` → `mboss/player_heal`).

**A previous reward buff ends here:** `#bfBuff 0`.

**HUD:**
- the badge on the boss-bar name line: maroon pill `#8C525C` with a salmon swirl `#E8858A` (the kit's HUD glyph, or the core's text badge `◖꩜◗`);
- the sub-line: "달빛 고치 — 회복하면 해제";
- the typed hint `g.say('달빛 고치 — 회복하면 해제', '#E8858A', 2, 50, 1)`.

**Cure:** see `S5_cure_fx.md`. The first heal with amount > 0 cures it (`coc/heal_ev`).

**Heal orbs:** 3 × 달빛 이슬 at random spots 6-14 b from the arena centre, 120° apart (`dew/spawn`). Each heals 8 % max HP through `player/heal`. They vanish at the revert (B5 t92). If the player is still debuffed, one orb comes back at groggy t20.

## 5. FX on the player at t6 (the debuff lands)

- A spiral of maroon / salmon dust (`#8C525C` / `#E8858A`, 16 points rising 0.3 → 2.2 b around the player's body, r 0.35-1.1). The core already does this.
- `tc:swirl #E8858A 0.3→1.8 l14/f6 bb center spin -150` at the player + (0,1.2,0).
- Badge pop: `tc:glow #8C525C 0.4→1.2 l8/f4 bb center` at the player + (0,2.4,0) (the badge "pops big then settles", as in the footage's UI).
- Sounds at the player: `entity.elder_guardian.curse` 0.35/1.7, `block.amethyst_block.resonate` 0.6/0.7.

## 6. Fairness

- The debuff is unavoidable by design (the plan, the video).
  - It never kills (floor 1).
  - It is announced by the sheath (t0) and the sphere (t6).
  - The heal orbs give a cure that every character can reach (6-14 b from the centre).
- The transformation has no hazard, so the player gets a free 30 t to reposition. The first butterfly attack's telegraph starts ≥ 16 t after the end.

## 7. Diagram (top view)

```
              ( ripple r5 )
          ( ( ripple r4 ) )
        ( ( ( sphere r2.5 ) ) )     t6 sphere → 달빛 고치 on P, 3 heal orbs ◦ at 6-14 b from C
              S (sheath)                         ◦          ◦
                         P                              ◦
```

## 8. Checks

- The damage = floor(cur × 0.2), with HP ≥ 1 after.
- `#mbHealPct 60`, `#mbCritAdd -100`, `#bfDmgPct 50` after t6.
- 3 orbs exist at t6.
- The rings fx at t9-11 (event `rings`).
- The form is butterfly at t30.
