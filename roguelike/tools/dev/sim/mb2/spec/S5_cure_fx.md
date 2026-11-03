# S5 달빛 고치 cure fx and the reward buff: implementation spec

| field | value |
|---|---|
| owner | core `coc/heal_ev` → `coc/cure` → `coc/cure_fx` / `coc/cure_at` (module tick, `#bfCureT` 1..20) |
| engines | gold cards = Navia's `g.card` (gold-only, which fits); the beam and the emblem = the tinted kit (`g.tcard`) |
| trigger | the first heal event with amount > 0 while `#bfCoc 1` (any heal, the user's decision). It is counted by `mboss/player_heal` from `items/hook/on_heal`; the heal itself is already reduced to 60 %. |
| result | 달빛 고치 off; **달빛 축복 받음**: CRIT +15 % (`#mbCritAdd 15`), DMG +50 % (`#bfDmgPct 150`), healing received 100 %. It lasts until the next 달빛 고치 application or the fight's end. |
| duration of the fx | 20 t at the player |

## 1. Footage check

Source: v4 C, 25.40-27.20 s, real time (`understand/v4.md` §2 C). I checked `sheet_debuff_removal_fx_crop_25.70-26.70.jpg`. Tick 0 = the healing tick that reaches full HP (25.667 s); ours is the first heal.

| event | footage tick | spec tick |
|---|---|---|
| the badge vanishes from the HUD and the party slot; a small white "+" | 0 | 0 (HUD refresh) |
| **gold beam**: thin pale-gold vertical beam, core `#F4EDC9` → white `#FFF8F3`, a 4-point star at its tip, coming down onto the player | 1-7 | 1-6 |
| **gold burst**: a white-gold sphere r 1.5-2 with a gold ring `#E0DD9C` expanding to r 2.5 | 7-12 | 7-11 |
| **gold emblem**: an ornate crown / fleur-de-lis glyph (about 2 b tall, a star on top, `#D5DD81` lines) above the player; gold sparkles rain down | 12-21 | 12-20 |
| audio: high +9 (t1), air +11 (t2.5), air +14 (t7-8), air +10 (t11.5) | | see §3 |

The core implementation matches. This spec adds exact card sizes and the kit's `emblem` sprite.

## 2. Per-tick timeline (`#bfCureT`, at the player's body)

| t | fx | sound |
|---|---|---|
| 0 | HUD: the badge → a gold star `★` on the name line, sub-line "달빛 축복 받음 · 치명타 +15% · 피해 +50%"; typed `g.say('달빛 축복 받음', '#F4E28A', 2, 40, 1)` (optional) | `block.beacon.activate` 0.8/1.6, `entity.player.levelup` 0.4/1.4, `block.amethyst_block.chime` 1.0/1.4 (the core) |
| 1 | star at the beam tip: gold `card('star', '^ ^6.6 ^', bb center, spin 60, s 0.3→1.1, l8/f4)` | `block.amethyst_block.chime` 0.6/2.0 (the high ping) |
| 1-6 | beam descending: per tick `dust #F4EDC9 1.3` ×6 Δ(0.05,0.5,0.05) at y = 6.5 - (t-1); `dust #FFFFFF 0.8` ×2 just below it; plus the beam itself as a tinted card `tc:slash #F4EDC9 5.0→6.0 l6/f2 bb vertical roll 90` at ^ ^3.5 ^. Navia's gold engine has no slash kind (its kinds: rose, star, burst, crescent, petal, shard, ring, glow). | `block.beacon.ambient` 0.4/2.0 at t3 (the shimmer) |
| **7** | **burst**: gold `card('burst', '^ ^1.1 ^', bb center, spin 30, s 0.8→3.2, l6/f3)` (r 1.6); ring `card('ring', '^ ^0.1 ^', rot ~ 90, s 1.5→5.0, l9/f4)` | `entity.firework_rocket.twinkle` 0.6/1.2, `block.amethyst_block.resonate` 0.6/1.4 |
| 7-11 | gold particle rings `#E0DD9C` at y 1.0, r 1.5 → 2.5 (+0.25 per tick) ×14 points | |
| 9 | | `block.amethyst_block.chime` 0.8/1.7 |
| **12** | **emblem**: the kit's **`emblem`** sprite (crown / fleur-de-lis with a star on top) tinted `#D5DD81` (a gold card variant), s 0.6→2.2, `bb vertical`, at ^ ^2.2 ^, l9/f4. Fallback: the core's dust outline (a 7-point stem + two 5-point arcs) + `card('star', '^ ^2.8 ^')` + `card('glow', '^ ^2.2 ^')` | `entity.player.levelup` 0.35/1.8, `block.amethyst_block.chime` 0.7/1.7 |
| 12-20 | sparkle rain: `wax_on` ×2 Δ(0.8,0.4,0.8) at ^ ^3.0 ^ and `end_rod` ×1 per tick | |
| 14 | | `block.amethyst_block.chime` 0.7/2.0 |
| 20 | end | |

## 3. Notes

- **Per player:** the game has one player; the fx runs at `@e[tag=rlk_body]`.
- **A heal that Clorinde converts to Bond of Life** (`#heal` 0 at the end of `on_heal`) does not cure. Document it; the core's hook placement decides (reuse.md §3.7).
- **The reward is replaced** by the next 달빛 고치 (the next transformation): `coc/apply` sets `#bfBuff 0`.
- Navia's gold cards share a 48-card cap with Navia's own fx. If the player is Navia, a skill burst could fill the cap and silently drop the cure fx. Acceptable: the dust beam always draws.

## 4. Diagram (side view at the player)

```
        ✦  (star, t1)
        |
        |  gold beam t1-6
        |
       (P)  burst r1.6 + ring → r2.5, t7-11
        ♛   emblem 2 b, sparkles t12-20
```
