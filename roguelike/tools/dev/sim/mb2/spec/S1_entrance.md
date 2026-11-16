# S1 Entrance: the cocoon (implementation spec)

| field | value |
|---|---|
| owner | core (`intro/*`, `intro_tick`); the rig plays `entrance`; the prop is `rig/prop/cocoon` |
| clip | `entrance`, 106 t, events nameplate 57, glow 61, whiteout 71, burst 79, land 90, stand 106 |
| intro clock | intro tick = clip tick + 1 (`INTRO_CLIP` 1). The fight starts at intro 107 (`intro/done` → `intro_end`). Registry `intro` 140 is the cap. |
| damage | none; she is untargetable (`rlk_mb_inv`) during the intro |

## 1. Footage and plan check

Source: v1 E, 0.00-5.27 s, real time (`understand/v1.md` §3 E). I re-checked `sheet_cocoon_burst_perframe_3.70-4.53.jpg`. Ticks = v1 ticks; the clip starts with the cocoon already there.

| event | footage tick | rig | verdict |
|---|---|---|---|
| cocoon hovers, tip 0.2 b above a glowing floor disc; thin white-cyan wind streaks curl round it; slight glow pulse | 0-57 | 0-57 (hidden, the prop) | ok |
| fight trigger: nameplate + HP bar fade in | 57 | nameplate 57 | ok (core: sub-line + chime) |
| core brightens; light rays from the seams | 60-70 | glow 61 | ok |
| whiteout: blinding white-yellow glow with god rays | 70-78 | whiteout 71 | ok |
| **burst**: white/cyan/mint crystal shards (about 6-7 b across) + two thin lime vertical crescents (the wing outline) | 78.7 | burst 79 | ok |
| revealed mid-air about 4 b up, curled; shards fly out and fade, cyan wind streaks | 80-82 | | |
| drop of about 4 b with a slight tumble; white 4-point sparkles over the floor; lime leaves drift | 82-89 | | |
| lands on the cocoon's ground point | 89-90 | land 90 | ok |
| landing crouch: legs wide, arm shards spread, leaves falling | 90-105 | | |
| stands → idle | 105 | stand 106 | ok |

One minor audio mismatch:
- In the footage the rising glassy shimmer starts at **t70** (whiteout), not at the glow (t61).
- The core plays its `glow_snd` at 61.
- **Proposed:** a soft layer at 61 and the main rising layers at 69 (§4).

## 2. Placement

- The body spawns at the arena marker (the framework).
- The cocoon prop sits at the body point:
  - the cocoon model is 3.8 b tall with its tip 0.2 b above the floor (the rig prop's own offsets);
  - its billboard halo glows around it.
- The player arrives from the gate side (the arena `start`, about 17 b away). The 57 t of hover is the walk-up. There is no proximity trigger; the timeline runs from intro tick 1.

## 3. Per-tick timeline (clip tick; intro tick = +1)

| t | rig / prop | mechanics | fx | sound |
|---|---|---|---|---|
| 0 | `entrance` clip; cocoon prop on | `intro/setup` (rig init/spawn, human hitbox, HUD) | floor disc: `tc:glow #81C4AB 6.0→7.0 l24/f0 rot ~ 90` at ^ ^0.05 ^0 (r 3.5), refreshed every 20 t until t79; rim `tc:ring #BCDDD2 8.0→8.2 l24/f0 rot ~ 90`, same refresh | `block.beacon.ambient` 0.3/1.6 at t0 and t40 (faint hum) |
| 0-78, every 4 t | | | `intro/hover`: lime floor ring r 1.6 (dust); `dust #E5FBC8` ×4 at the floor; wind streaks: `dust_color_transition #FFFFFF→#8DEAF0 0.8` ×2 at ^ ^2.2 ^ Δ(1.0,1.4,1.0); `end_rod` ×1. Every 8 t one curling streak `tc:slash #E6F6F8 1.5→2.5 l6/f2` at ^ ^2.0 ^ with a random yaw and roll ±40, `spin 90` | |
| **57** | nameplate | core `intro/name`: the sub-line "달빛의 화신" | `tc:star #E5FBC8 0.3→1.4 l6/f3 bb center` at the cocoon tip (^ ^3.9 ^) | `block.amethyst_block.resonate` 0.7/1.2, `block.beacon.ambient` 0.4/1.6 |
| **61** | glow | | `intro/glow` every 2 t, t61-78: `dust #D5F086 1.4` ×6 at ^ ^2.1 ^ Δ(0.35,0.9,0.35) + `end_rod` ×2 speed 0.06 (the rays); core window `tc:glow #CADE48 0.8→1.6 l10/f2 bb center` at ^ ^2.6 ^ (t61, t69) | `block.respawn_anchor.charge` 0.35/1.6 (soft) |
| 69 | | | | **rising shimmer**: `block.beacon.power_select` 0.8/1.4, `block.amethyst_block.resonate` 0.8/1.0 |
| **71** | whiteout | | `intro/white`: `dust #F8FFC0 2.6` ×30 at ^ ^2.1 ^ Δ(0.7,1.2,0.7); `end_rod` ×16 speed 0.12; `tc:glow #F8FFC0 2.0→5.0 l8/f0 bb center` at ^ ^2.1 ^ (blinding); `flash{color:[0.97,1.0,0.75,1.0]}` ×1 | `block.beacon.activate` 0.6/1.8 |
| 75 | | | god rays: 6 × `tc:slash #F8FFC0 3.0→5.0 l4/f1`, radial (roll 60k) at ^ ^2.1 ^ | `block.respawn_anchor.charge` 0.5/1.8 |
| **79** | **burst**; the rig becomes visible 4 b up; `prop/clear` | core `intro/burst` | crystal shards: `tc:burst #F9FDFC 1.0→6.5 l7/f3 bb center spin 25`; `tc:glow #BAF3E3 2.0→5.0 l6/f3`; 8 × `tc:shard` (`#BAF3E3` / `#78D8D1` / `#F9FDFC` / `#39B4C1`) radial, s 0.6→1.6, l10/f5, `move` 2.5 b outward; two lime crescents `tc:moon #C8F060 2.0→3.2 l8/f4` at ^±1.5 ^2.6 ^ (rolled facing out); `block{white_stained_glass}` ×36, `block{light_blue_stained_glass}` ×22 | `block.amethyst_cluster.break` 1.0/1.0, `block.glass.break` 0.8/1.3, `entity.breeze.wind_burst` 0.8/1.2, `block.amethyst_block.chime` 0.9/1.6 |
| 80-82 | revealed, curled | | cyan wind streaks: `dust_color_transition #FFFFFF→#39B4C1 1.0` ×6 Δ(1.5,1,1.5) at ^ ^4.5 ^ | |
| 82, 85, 88 | drop (tumble) | | `intro/fall` every 4 t: `wax_off` ×2 over the floor; `tc:leaf #A8DF74 0.3→0.35 l14/f6 move (0,-2,0)` ×2; `tc:star #FFFFFF 0.2→0.6 l4/f2 bb center` at a random floor spot within r 2 (the 4-point sparkles) | `block.amethyst_block.chime` 0.7/1.8 at 82, 0.6/1.5 at 85, 0.5/1.7 at 88 (the glittering tail) |
| **90** | land | core `intro/land` | `poof` ×10, moss block ×14, lime floor ring r 1.3; `tc:ring #B6E35A 1.0→3.0 l5/f2 rot ~ 90` at the floor | `block.moss.fall` 0.9/1.0, `entity.iron_golem.step` 0.4/1.4 |
| 90-105 | landing crouch | | leaves still falling: `tc:leaf` ×1 every 4 t | |
| 106 | stand | | | |
| intro 107 | — | `intro/done`: `intro_end`, `#bfCool 20`, AI on | | |

## 4. Sound summary

Taken from v1 §6:
- cocoon charge 3.48 → 3.90 s (rising glassy shimmer, low rumble);
- burst 3.93 (bright shatter), glittering tail to 4.80;
- landing 4.47.

Not yet used in the pack: `block.moss.fall`.

## 5. Fairness

There are no hits. The fight starts 1 t after she stands. The first decision waits `#bfCool 20` t, so the first attack telegraph cannot start before intro 127.

## 6. Diagram (side view)

```
   t0-78                         t79                      t82-90           t90-106
     /\   cocoon 3.8 b             * shards *               (her)            stands
    /  \  hovering                *  ( ) *   lime ( )         |  drop 4 b     _|_
    \  /                           *     *   crescents        v
  ===\/=== glowing disc r3.5    ==================         ======          ======
```

## 7. Checks

- No hazard is ever made in the intro.
- The prop is cleared at 79.
- The rig is visible from 79.
- Card count ≤ 20 at the burst.
- `intro_end` at intro tick 107 ≤ 140.
