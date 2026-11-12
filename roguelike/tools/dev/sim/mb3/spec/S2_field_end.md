# S2 Field end, unbroken (closing 「인력 충격파」 ×3 + pack-up): implementation spec

| field | value |
|---|---|
| owner | the core: `field/closer` (after 400 t of field patterns, at a decision point) → service 21 with `#fgWvK 2` (the closing waves, `W_gravity_waves.md`) → `field/packing` → service **22** (`field_out`, clip `field_end`) → `field/down` (cruise) |
| clips | the waves (the 3rd = **`wave_drop`**), then **`field_end`**, 102 t → `idle_cruise`: lift 0, rise 2, lances 20, horiz 40, pack 50, dock 72, packed 96 |
| key ticks (pack-up clock) | **0**: meter closed, low gravity off, the ×0.6 cut off (`field/close`); 72: the idle look; 102: cruise, 4 cruise patterns to the next field |
| damage | the closing waves only (W spec); the pack-up deals none |

## 1. Footage and plan check

Source: v2 B3-B4, 22.90-31.30 s (`understand/v2.md` §3 B). Ticks relative to the 3rd wave's impact (25.00 s).

| event | footage W3 + t | ours (W3 = the closing waves' 176) | verdict |
|---|---|---|---|
| wave 3: longer charge, the device sinks 0.5 m | −42..0 | `wave_drop` 0-36 (charge 40) | ok |
| impact burst | 0 | impact 40 (on landing) | ok (drop order: W spec F2) |
| the device drops 1.5-2 m onto the floor | +5..+8 | `drop` 36-40 (−4..0) | ok |
| grounded, the ring expanding | +8..+27 | 40-60 (0..+20) | ok |
| lift-off flash (white-gold burst under the device) | +27 | `wave_drop` `lift` 60 (+20) | ok |
| rise to the hover (2-2.5 m) | +28..+48 | 60-80 (+20..+40) | ok |
| the lances deploy (vertical, spike down, 4-5 m out) | +44..+60 | `field_end` lances 20-40 (≈ +65..+85) | **+21 t** |
| the lances turn horizontal | +63..+72 | `horiz` 40 (≈ +85) | +22 t |
| the roll / pack-up (ring tilts 20-30°, rocks; the core ring swings up) | +72..+92 | `pack` 50-72 (≈ +95..+117) | +23 t |
| the lances dock, the pods tuck | +92..+100 | `dock` 72 (≈ +117) | +25 t |
| compact; violet fades by +106 | +102..+106 | `packed` 96, clip end 102 (≈ +141..+147) | +40 t |

- **The whole tail is about 40 t longer than the footage.** The waves service ends at max(the last front's expiry,
  `wave_drop`'s end) = 220, then a decision tick, then `field_end`'s 102 t. Accepted: the extra time is a harmless
  hover and a punish window. If wanted, the rig could shorten `field_end`'s first 20 t (the small 5.8 → 6.2 rise),
  since `wave_drop` already rose. A note for the rig author, not a module change.
- **Double lift-off.** `wave_drop` has the lift-off (60) and `field_end` starts with "lift-off flash (0)". Fire the kit
  `lift_off` and `snd/lift_off` only once, at `wave_drop` `lift` (W spec); `field_end` 0 gets only the rise hum.
- **The look.** The rig note says "call `look/idle` at 72 or earlier" (violet fades 72-96). The core calls
  `look/idle` at 0 (`field/close`). Recommended: keep the meter / low-gravity / cut ending at 0 (gameplay), but move
  `look/idle` to `dock` (72), so the violet halos fade with the pack-up as in the footage.
- **Plan:** "the closing 「인력 충격파」 ×3, then pack-up (lift-off flash, 20 t rise, lances, roll/pack into compact
  form); no groggy" ✓.

## 2. AI

- At the centre. The closing waves as W. During the pack-up: no tracking (the roll is the clip's), no attacks.
- After `field/down`: cruise; `#fgCruLim` 4; `#fgCool` 20.

## 3. Body travel

None. Cruise locomotion resumes after `field/down`.

## 4. Per-tick timeline (pack-up clock; the waves are in `W_gravity_waves.md`)

`ring` = body + the manifest `ring_centre` (5.8 → 6.2 by 20, 6.2 at 50, 5.0 at 72, 4.5 at 96).

| t | rig | mechanics (core) | fx (kit) | sound |
|---|---|---|---|---|
| (waves 196) | `wave_drop` `lift` | (meter still open, low gravity on) | `K.fx('lift_off')` at the floor (W spec) | `K.snd('lift_off')` |
| **0** | core plays `field_end`: lift (5.8 → 6.2) | `field/close`: `#fgOpen 0` (meter closed, cut off), `#fgLowG 0` (low gravity ends next tick), HUD | `K.hud('meter_close')`, `K.hud('lowg_off')`, `K.hud('hint_off')` | `K.snd('rise_hum')` |
| 20 | `lances` (spikes and medallions out to ±5.6 b, spike down) | | `K.fx('spark')` at each lance (`^5.6 ^5.6 ^0` / `^-5.6 ^5.6 ^0`) | `K.snd('pack_up')` |
| 40 | `horiz` (the lances turn horizontal) | | | `block.chain.place` 0.6/0.9 |
| 50 | `pack` (the roll and rock, 50-72) | | `K.fx('pack_up')` at the ring (`~ ~6.2 ~`), rotated as the body | `K.snd('core_flip')` |
| 60 | | | | `block.chain.step` 0.6/0.7 (the rock) |
| **72** | `dock` (lances dock, the core swings up, pods tuck) | `look/idle` (moved from 0, cosmetic) | `K.fx('pack_up')` at the ring (`~ ~5.0 ~`) | `K.snd('revert')` |
| 96 | `packed` (cruise form) | | | `block.crafter.craft` 0.5/1.1 |
| **102** | → `idle_cruise` | `g.end()` → `field/down`: `#fgField 0`, cruise hitbox, `#fgCruLim 4`, `#fgCool 20` | | |

## 5. Damage areas

None in the pack-up. (adapt.md suggested a lift-off pulse `hz/disc r 3`. The plan does not have it, and the footage
shows no hit. Not added.)

## 6. Telegraphs

None needed. The closing waves have their own.

## 7. Projectiles

None.

## 8. FX detail

`lift_off` (in `wave_drop`), `spark` ×2, `pack_up` ×2.

## 9. Sound

From v2 §8: an air burst at the lift-off; a mechanical whirr as the lances deploy (`trial_spawner` / piston /
spyglass); clockwork on the pack-up.

| tick | sound |
|---|---|
| (waves 196) | `snd/lift_off` |
| 0 | `snd/rise_hum` |
| 20 | `snd/pack_up` |
| 40 | `block.chain.place` 0.6/0.9 |
| 50 | `snd/core_flip` |
| 60 | `block.chain.step` 0.6/0.7 |
| 72 | `snd/revert` |
| 96 | `block.crafter.craft` 0.5/1.1 |

## 10. Dodge windows

Nothing to dodge in the pack-up.
- While the closing waves run the meter is still open, so the player can still break the field. Above all during
  `wave_drop`'s grounded 20 t (core resting on the floor, 176-196): a punish window.
- From pack-up 0 hits no longer count and deal full damage (the cut is off).
- Low gravity ends at 0: a player mid-air falls with normal gravity. Harmless (no fall damage; the multiplier is 0).

## 11. Diagram (side view)

```
 waves 136-176  sink, DROP onto the floor (impact 176), grounded 176-196, lift-off 196, rise -> 216
 pack-up 0      meter / low gravity / cut OFF; rise to 6.2 b
 20-40   <=====lance=====[ring]=====lance=====>   +-5.6 b
 50-72         roll / rock, the core swings up
 72-96         dock, violet fades (look/idle at 72)
 102           compact cruise; 4 cruise patterns to the next field
```

## 12. Implementation notes (core)

- The service 22 `field_out` timeline: replace the vanilla lines with the kit calls above. Read
  `ev('field_end', 'lances' / 'horiz' / 'pack' / 'dock' / 'packed')`. The stub defaults (lances 22) are only used
  while the stub rig is in use.
- `field/close`: keep the meter / low gravity / cut ending at 0. Move `g.look('idle')` to a new `field_out` timeline
  line at `dock`.
- Integration (`fg_contract.md` §15): `field/close` → `hud/meter_close` + `hud/lowg_off` (+ `hint_off`).

## 13. Checks

- `#fgOpen` 0 and `#fgLowG` 0 from pack-up 0. `#mbLowG` 0 on the next module tick.
- `look/idle` at 72.
- Cruise (`#fgField 0`) at 102, with `#fgCruLim` 4.
- No hazard is made during the pack-up.
- The closing waves use `wave_drop`.
