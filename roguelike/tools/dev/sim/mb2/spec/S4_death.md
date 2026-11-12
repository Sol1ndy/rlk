# S4 Death: implementation spec

| field | value |
|---|---|
| owner | core hooks `death_start` / `death_tick`; fx functions `fx/death_*` |
| clip | `death`, 100 t, events stagger 0, shatter 10, kneel 30, dissolve 50, gone 100. It starts from either form. |
| registry | `death` 100 (the cap of the death shell); `deathSnd false` (no framework roar) |
| damage | none; the fight is over for the player too: 달빛 고치 and the reward are cleared, the heal orbs removed |

## 1. Source

Not in the footage. Plan.md: "she staggers and the wings (if any) shatter into lime/opal shards; she kneels; she dissolves into rising moonlight motes and white-cyan crystal shards, about 100 t; no creature voices."

The core reads `ev_or('death', 'shatter', 6)`, `kneel` 24 and `dissolve` 40. The manifest has 10 / 30 / 50, so the manifest wins. The timeline below uses the manifest values.

## 2. Per-tick timeline (`#mbT` = death clock, 1..100; clip tick = `#mbT`)

| t | rig | mechanics | fx | sound |
|---|---|---|---|---|
| 0 (`death_start`) | `death` clip, stagger | `p/cancel`, `coc/clear`, `dew/clear`, `#bfSt dead`, `prop/clear` (the framework has already cleared hazards, props and bars) | hit flash (rig `flash`); `tc:burst #FFFFFF 0.8→2.6 l4/f2 bb center` at the core anchor; `flash{color:[0.95,1.0,0.9,0.9]}` | `block.amethyst_cluster.break` 0.8/0.8, `block.beacon.deactivate` 0.6/0.9 |
| 4 | stagger back | | crack lines: 3 × `tc:slash #E5FBC8 1.0→1.8 l4/f2` at the core with random rolls | `block.amethyst_block.break` 0.6/0.9 |
| **10** | shatter (butterfly form only: the wings scale out) | | if `#bfForm 2`: `fx/death_shatter`: lime / opal shards (6 × `tc:shard`), `block{lime_stained_glass}` ×30, `block{white_stained_glass}` ×16, `dust #D4F8C6 1.4` ×20. In human form: the crescent plates crack: `tc:shard #394B75` ×4 at hand_r_a / hand_l_a | `block.glass.break` 0.6/1.2, `entity.illusioner.mirror_move` 0.5/1.4 |
| 20 | knees buckle | | | `block.amethyst_block.resonate` 0.5/0.7 |
| **30** | kneel | | `poof` ×8; moss block ×10; `dust #B6E35A 0.9` ring r 1.0 | `block.moss.fall` 0.8/0.9, `entity.iron_golem.step` 0.4/1.4 |
| 30-49 | kneeling, head bowed | | `dust #E5FBC8 0.6` ×1 rising every 4 t | |
| **50** | dissolve begins (the parts scale out from the extremities) | | every 2 t, 50-96: `fx/death_motes` (`dust #E5FBC8 1.0` ×4 rising, `dust_color_transition #FFFFFF→#8DEAF0 0.9` ×3, `end_rod` ×2, `block{light_blue_stained_glass}` ×2); every 6 t, a crystal shard `tc:shard #BAF3E3 0.4→1.0 l10/f5` with `move` (0,2.5,0) from a random body point | `block.beacon.deactivate` 0.7/1.2, `block.amethyst_block.resonate` 0.6/0.8 |
| 68, 84, 98 | | | | `block.amethyst_block.chime` 0.6 at pitch 1.8 / 1.5 / 1.2 (a descending, fading chime) |
| 96 | | `fx/death_end` | the last motes fly up: `end_rod` ×20 speed 0.18, `dust #EDF9DA 1.6` ×16; `tc:glow #E5FBC8 1.0→2.5 l6/f3 bb center` at ^ ^1.2 ^ | `block.amethyst_block.chime` 0.8/2.0 |
| 99 | | the rig ticks until 99 | | |
| 100 | gone | rig `kill` (it must not tick after this, or it would respawn) | | |

## 3. Notes

- No creature voices. Only the crystal, beacon and amethyst palette.
- The reward boxes and the mid-boss loot are the framework's (`won`), after `death_finish`.
- Card budget: ≤ 12 live.

## 4. Diagram (side view)

```
 t0 stagger    t10 wings shatter (bf)   t30 kneel     t50-96 dissolve (motes, shards rise)    t100 gone
    \o/  *         * ✶ *                   _o_            .  ° .  ✧ .  °
     |            (shards)                  /\           ° .  o  .  °
```
