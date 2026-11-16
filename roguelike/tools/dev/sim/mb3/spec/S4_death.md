# S4 Death: implementation spec

| field | value |
|---|---|
| owner | the core: `death_start` / `death_tick` (`#mbT` 1 … 110 = registry `death` 110), then the framework's `death_finish` (item boxes) |
| clip | **`death`**, 110 t, hold: flicker 0, **drop 20**, **sink 40**, **land 60**, **out 70**, gone 110 |
| rig | `tick` for `#mbT` 1-109; `kill` at 110 (the rig note: "call kill after 110") |
| sounds | **mechanical only** (`deathSnd` false: no framework death voice) |
| damage | none |

## 1. Footage and plan check

Death is not in the footage. These are the plan's and model.md §9's proposal, and the rig follows them.

| event | plan / model.md | rig `death` | verdict |
|---|---|---|---|
| the seam flickers hot / off three times, the eye fades | "the seam flickers out" | flicker 0-18 | ok |
| the halo drops and rolls off; the pods stop and fall; the spikes droop | "the halo and drill pods fall" | drop 20 | ok |
| the ring tilts and sinks to the floor | plan **40°**; model.md: 40° to ring centre 0.6 b | the ring tilts **30°** and sinks until its low rim rests on the floor (ring centre 2.45 b), 20-60 | **F1** |
| the medallions clatter down beside it | model.md | land 60 | ok |
| everything scales out with gold sparks | "then it scales out (about 110 t)" | out 70 → gone 110 | ok |

- **F1 — tilt 30° vs 40°.** At D 7, a 40° tilt with the low rim on the floor puts the ring centre about 2.25 b up and
  the far rim 4.5 b. The rig's 30° rests the low rim at the same floor contact. **Keep the rig** (a visual detail; the
  footage cannot settle it).
- **F2 — stub `out` 90.** The core reads `ev_or('death','out',90)`; the real rig has `out` **70**. With the manifest
  the core follows (70). The last kit `death_fade` must end by 110: the framework's cleanup (`fx/clear`) at
  `death_finish` would cut it (the butterfly's perf-5 lesson). Call `death_fade` at 70 and 82 only (its cards live
  ≤ 27 t).

## 2. AI

None. `p/cancel` at `death_start`; the field ends (meter, low gravity, cut); `#fgSt 7`.

## 3. Body travel

None.

## 4. Per-tick timeline (`#mbT` = clip tick; the clip is played in `death_start`, tick 0)

`core` = body + 4.5 (it ends at about 1.9 when landed).

| t | rig | mechanics (core) | fx (kit) | sound |
|---|---|---|---|---|
| **0** | `play/death`: flicker (temporary look off / hot) | `death_start`: `p/cancel`, `#fgOpen 0`, `#fgLowG 0`, `#fgField 0`, `prop/clear` | `fx/tele/clear`; `K.hud('meter_close')`, `K.hud('lowg_off')`, `K.hud('groggy_off')`; `K.fx('death_flicker')` at the core | `K.snd('death')` |
| 6 | | | `K.fx('death_flicker')` | `block.beacon.deactivate` 0.5/1.6 |
| 12 | | `look/off` (the stored look; the clip's temporary off ends here anyway) | `K.fx('death_flicker')` | `block.beacon.deactivate` 0.4/1.8 |
| **20** | `drop` (halo drops and rolls off, pods fall, spikes droop) | | `K.fx('dust_puff')` at the floor under the halo side (`^1.5 ^ ^`) | `block.chain.fall` 0.6/0.8, `block.copper.fall` 0.5/0.8 |
| **40** | `sink` (ring tilts 30° and sinks, 40-60) | | | `block.anvil.place` 0.6/0.5, `block.chain.step` 0.5/0.6 (a groan) |
| **60** | `land` (low rim on the floor, the medallions clatter) | | `K.fx('death_fall')` at the floor under the body | `K.snd('death_fall')` |
| **70** | `out` (scale-out 70-110) | | `K.fx('death_fade')` around the core (`~ ~1.9 ~`) | |
| 82 | | | `K.fx('death_fade')` | `K.snd('death_fade')` |
| 109 | (the last rig tick) | | | |
| **110** | `gone` | `R('kill')`; the framework `death_finish` → the item boxes, cleanup (`fx/clear`, `hud/clear`) | | |

## 5. Damage areas

None. The framework cleared the hazards, props, pull and movement before `death_start`.

## 6. Telegraphs

None.

## 7. Projectiles

None. `prop/clear` removes the rig props (a falling bomb or a missile) at 0. Pattern props carry `rlk_mb_fg_pat` and
die in `p/cancel`.

## 8. FX detail

`death_flicker` ×3 (2), `dust_puff` (2), `death_fall` (9), `death_fade` ×2 (8, ambient). Every card has expired by
109 (the last `death_fade` at 82: life ≤ 22 + delay ≤ 5).

## 9. Sound

Mechanical only (no creature sound). The kit recipes are checked against a voice list.

| tick | sound |
|---|---|
| 0 | `snd/death` (beacon deactivate, respawn anchor deplete, vault deactivate, chain break) |
| 6 | `block.beacon.deactivate` 0.5/1.6 |
| 12 | `block.beacon.deactivate` 0.4/1.8 |
| 20 | `block.chain.fall` 0.6/0.8 + `block.copper.fall` 0.5/0.8 |
| 40 | `block.anvil.place` 0.6/0.5 + `block.chain.step` 0.5/0.6 |
| 60 | `snd/death_fall` |
| 82 | `snd/death_fade` |

## 10. Dodge windows

None.

## 11. Diagram (side view)

```
 t0-18   [=ring=]  seam flickers x3, eye fades
 t20     halo drops and rolls off, pods fall, spikes droop
 t40-60       \ ring tilts 30 deg, sinks: low rim on the floor (centre 2.45 b)
 t60          medallions clatter, dust ring
 t70-110      scale-out with gold motes (fades at 70 and 82 only)
 t110         rig kill -> death_finish -> 2 item boxes
```

## 12. Implementation notes (core)

- `death_tick`:
  - replace `cfx/death_flicker` at 4 / 9 by the kit at 0 / 6 / 12;
  - `cfx/death_drop` at `drop`, `cfx/death_sink` at `sink`, `cfx/death_out` at `out` (read with `ev()`);
  - add `land` (60) for `death_fall`.
- `death_start`: add `fx/tele/clear`, `hud/meter_close`, `hud/lowg_off`, `hud/groggy_off` (`fg_contract.md` §15).
- The assertion `DEATH_LEN <= BOSS['death']` holds (110 ≤ 110). `death_tick` runs at `#mbT` 110 before
  `death_finish`, so the kill at 110 happens.

## 13. Checks

- The rig ticks 1-109 and is killed at 110 (no rig part left after `death_finish`).
- No kit card is alive at 110.
- No sound outside the kit's mechanical set.
- `#mbLowG` 0 from the death tick.
- The item boxes appear (existing e2e case).
