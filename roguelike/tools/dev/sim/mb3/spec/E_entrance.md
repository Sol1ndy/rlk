# E Entrance (dormant → unfold → rise): implementation spec

| field | value |
|---|---|
| owner | core `intro/*` (`core.py` `intro()`), fx through the kit |
| clip | `entrance`, 130 t, then `idle_cruise`: clank 16, pods 24, unfold 30, eye 54, turn 60, rise 80, **risen 110**, face 115 |
| intro clock | `#mbT` = clip tick + 1 (`INTRO_CLIP` 1: the clip is played in `intro/setup` on the spawn tick) |
| untargetable | from the spawn to `risen` (intro 111: `intro_end`); the registry `intro` 130 is the cap |
| damage | none |

## 1. Footage and plan check

Source: v1 E, 0.00-6.30 s (`understand/v1.md` §3 E). The v1 ticks count from the video start. The rig's clip ticks use
the same zero, so the columns line up 1:1. E0 = the clank (t16).

| event | footage t (E+) | rig `entrance` | verdict |
|---|---|---|---|
| dormant: a long tan bar with two gold end spikes, low over the emblem; the pendulum spike almost on its shadow | 0-16 | dormant form (ring centre 2.15 b, look off) | ok |
| low / mid machinery sound onset | 13 (−3) | — | sound at 13 |
| **activation clank** (sharp, < 0.1 s) | 16 (0) | `clank` 16 | ok |
| gold sparks / flare at the top hub, small ring lights | 21-29 (+5..+13) | — | fx |
| 4 pods unfold under the ring (thumps at 27, 32) | 24-30 (+8..+14) | `pods` 24 (lift to 2.6 b) | ok |
| crown assembly: gold ring + hub stack rise out of the centre, flares; gear clicks at 40, 46, 49 | 28-46 (+12..+30) | `unfold` 30 (halo, inner ring, core rise out of the hole; lift to 3.0 b) | ok |
| the eye opens (red iris in a gold frame) | 48-58 (+32..+42) | `eye` 54 | ok |
| the core drum tilts and turns 90° | 60-80 (+44..+64) | `turn` 60 (the arch turns 60-78) | ok |
| **rise** to cruise height, eased; whirring air bursts 86-106 | 80-110 (+64..+94) | `rise` 80 → `risen` 110 (3.0 → 4.5 b) | ok |
| settles; yaw toward the player | 110 / 115-126 | `face` 115 | ok (the AI turns the anchor) |
| flows straight into the first pattern | 115 | first pick ≈ 126 (intro 111 + `#fgCool` 16) | ok |

- **Plan "untargetable until about t94".** The footage gives E0 + 94 = t110, the rig's `risen`, so the plan's figure
  counts from the clank. The core already ends the intro at intro 111 (clip 110), which is right. No change.
- **Plan "rises about 2.9 b".** With D 7.0 the rig goes from 2.15 b (dormant) to 4.5 b (cruise): 2.35 b. That follows
  from the scale (model.md), not a timing problem. Keep the rig.

## 2. AI

- Untargetable, no tracking during the clip (the body faces south, toward the arriving player: `spawn` hook).
- From intro 111 the idle tracks at 4°/t; the first decision comes after `#fgCool` 16.

## 3. Body travel

None (the rig rises in the clip).

## 4. Per-tick timeline (clip tick; intro `#mbT` = clip + 1)

`hub` = body + the manifest `ring_centre` of the event + 0.5 (2.55 at 16, 3.1 at 30). `eye` = body-frame
`^ ^3.0 ^1.38` at 54.

| t | rig | mechanics (core) | fx (kit) | sound |
|---|---|---|---|---|
| 0 (spawn tick) | `init`, `spawn`, `form/dormant`, `look/off`, `play/entrance` | cruise hitbox (untargetable anyway); HUD lines | floor dust (stub `cfx/ent_setup`: tuff block particles) | `block.respawn_anchor.ambient` 0.6/0.6 |
| 13 | | | | `block.beacon.ambient` 0.4/0.6 (machinery onset) |
| **16** | `clank` | | `K.fx('awake')` at the hub | `K.snd('awake_clank')` |
| 21, 25 | | | `K.fx('spark')` at the hub | |
| **24** | `pods` (pods drop, lift to 2.6 b) | | `K.fx('unfold')` at the ring centre (`~ ~2.15 ~`), rotated as the body | `K.snd('unfold')` |
| 30 | `unfold` (halo, inner ring, core rise; lift to 3.0 b) | | `K.fx('crown_flare')` at the hub top (`~ ~3.2 ~`) | |
| 32 | | | | `block.piston.extend` 0.6/0.8 (second thump) |
| 38 | | | `K.fx('crown_flare')` | |
| 40, 46, 49 | | | | `K.snd('gear_click')` |
| **54** | `eye` (iris and seam idle) | `intro/name`: the nameplate 브레게 프로토타입 on the sub-line, `look/idle` | `K.fx('eye_open')` at the eye | `K.snd('eye_open')` |
| 60 | `turn` (the arch turns 90°, 60-78) | | | `block.grindstone.use` 0.3/0.6 |
| **80** | `rise` (3.0 → 4.5 b, 80-110) | | `K.fx('rise')` at the floor under the body | `K.snd('rise_hum')` |
| 94 | | | `K.fx('rise')` | `K.snd('rise_hum')` |
| **110** | `risen` (cruise form) | `intro/done`: `intro_end` (targetable), `#fgCool` 16, `ai/enter` | `K.fx('flash')` at the core (`~ ~4.5 ~`) | `block.beacon.activate` 0.5/1.3 ("online") |
| 115 | `face` | the idle has been tracking since 111 (4°/t) | | |
| 126 | (the entrance clip is cut by the first pattern's clip at 126-130, which is fine: the pose is cruise by 110) | the first decision | | |

The stub's vanilla `cfx/clank`, `cfx/unfold`, `cfx/eye`, `cfx/rise`, `cfx/rise_dust` lines are replaced by these kit
calls once the kit is merged.

## 5. Damage areas

None. Untargetable until 110 (the framework intro shell's `rlk_mb_inv`).

## 6. Telegraphs

None needed. The HUD shows the boss bar from the spawn (framework intro), and the nameplate sub-line at 54.

## 7. Projectiles

None.

## 8. FX detail

`awake` (4), `spark` ×2 (1), `unfold` (8), `crown_flare` ×2 (3, ambient), `eye_open` (2), `rise` ×2 (4), `flash` (1).
Peak about 12 fx cards (kit budget: entrance 12).

## 9. Sound

From v1 §6: sharp metallic clank, low thumps and gear clicks, a low mechanical groan and click as the eye opens, a
whirring rise. No voice (`deathSnd` false applies to the death; the entrance has no voice either).

| tick | sound |
|---|---|
| 0 | `block.respawn_anchor.ambient` 0.6/0.6 |
| 13 | `block.beacon.ambient` 0.4/0.6 |
| 16 | `snd/awake_clank` |
| 24 | `snd/unfold` |
| 32 | `block.piston.extend` 0.6/0.8 |
| 40, 46, 49 | `snd/gear_click` |
| 54 | `snd/eye_open` |
| 60 | `block.grindstone.use` 0.3/0.6 |
| 80, 94 | `snd/rise_hum` |
| 110 | `block.beacon.activate` 0.5/1.3 |

## 10. Dodge windows

Nothing to dodge. Player hits on the body during 0-110 do nothing (untargetable).

## 11. Diagram (side view)

```
 t0-16   ____[==dormant bar==]____   ring 2.15 b, pendulum tip 0.2 b
 t24-48     pods drop, crown + halo rise out of the hole, lift to 3.0 b
 t54        eye opens (nameplate)        t60-78 arch turns
 t80-110          ( halo )
              [=====ring=====]   ring 4.5 b (cruise)
                    |  pendulum tip 0.55 b
 t110 targetable, fight starts; t115 settled
```

## 12. Implementation notes (core)

- Read `ENT_CLANK` … `ENT_RISEN` with `ev()` (they already are); add `ENT_PODS = ev('entrance','pods')` for the
  unfold fx (the stub uses `unfold` for its unfold sound).
- The core never plays a pattern clip before 110, so no clip cuts the rise.

## 13. Checks

- `intro_end` at clip 110 (intro 111).
- `look/idle` and the nameplate at 54.
- No hazard and no damage before 111.
- Exactly one `play/entrance`.
