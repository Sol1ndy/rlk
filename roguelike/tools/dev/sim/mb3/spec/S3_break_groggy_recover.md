# S3 역장 붕괴 (20-hit break) → groggy 200 t → recover: implementation spec

| field | value |
|---|---|
| owner | the core: `on_hit` (the count) → `brk/count` (each count's fx) → `brk/begin` (the 20th) → `brk/tick` → `groggy/*` → `recover/*` |
| clips | **`break`** (34 → `groggy`: bubble 0, **burst 5**, tilt 5, wobble 14, sink 34), **`groggy`** (160, loop), **`recover`** (15 → `idle_cruise`: relevel 0, **flip 6**, done 15) |
| states | `#fgSt` 6 break (34 t) → 3 groggy (200 t) → 4 recover (15 t) → 0 idle (cruise, `#fgCool` 16) |
| damage | none from the boss. The boss takes normal damage (the ×0.6 cut ends at the break); no groggy bonus |

## 1. Footage and plan check

Source: v2 A3, 11.20-15.20 s (`understand/v2.md` §3 A3); the 3-Pneuma release, replaced by the 20-hit meter (user
decision). Ticks from the bubble lighting (11.90 s).

| event | footage t | rig / core | verdict |
|---|---|---|---|
| a gold-white translucent bubble (2-2.5 m) round the core lights up, cracked | 0 | `break` bubble 0 (the bubble flares 0-5) | ok |
| brightest | 2.4 | — | |
| **the bubble bursts**: gold flash + a thin arc ring; a tiny hit number ("resistances up") | 4.7 | `burst` 5 (scale 1 → 1.6 → 0 over 5-7) | ok |
| the whole device tilts 25-30°; a horizontal gold spark ring expands at floor level | 5-14 | `tilt` 5-14 (28°) | ok |
| tilted, rocking / wobbling | 14-34 | `wobble` 14-34 (±8° → 0) + `sink` toward the slump | ok |
| levels out | 37-43 | `recover` relevel 0-6 | ok, after the groggy |
| the core flips to the top | 46-55 | `recover` flip 6-15 | ok |
| compact form | 61 | done 15 | ok |
| a long groggy | **not in the footage** (2.8 s stagger only) | groggy 200 t (plan, design) | plan |

- **Plan:** "At 20: cancel the running pattern and clear hazards; end low gravity and the damage cut; play the break
  … groggy 200 t; re-level 6 t; core flip 9 t; back to cruise" ✓ (core).
- **Plan "the core bubble cracks through stages 0-3 at 0-4/5-9/10-14/15-19, then bursts"** ✓ (`crack/0..3`, `crack/4`
  at the burst). See `S5_meter_hud.md` for the count side.
- **The groggy pose** (plan: ring centre about 3.0 b, roll 25°, seam off, halo slid, pendulum swinging): the rig's
  `groggy` has ring 3.3 b, roll 25°, pitch 8°, the pendulum ±12° ✓ (0.3 b higher: fine).

## 2. AI

- **Break** (34 t) and **groggy** (200 t): no tracking, no attacks, no travel.
- **Recover** (15 t): no tracking. Then `ai/enter` with `#fgCool` 16 (the idle turns toward the player first).
- The cruise counters restart at the groggy start: 4 cruise patterns to the next field. A test cut keeps them (the
  S8 lesson).

## 3. Body travel

None (the body stays at the centre where the field was; cruise locomotion resumes after the recovery).

## 4. Per-tick timeline

`core` = body + the manifest `core` anchor: 4.1 at 0-5 (field), 3.5 at 14, 2.5 at 34 and in the groggy, 3.3 at the
`recover` flip.

### Break (clock = `#fgT`, the `break` clip tick)

| t | rig | mechanics (core) | fx (kit) | sound |
|---|---|---|---|---|
| (count 20) | | `on_hit` sets `#fgBrkQ`; the next module tick runs `brk/count` (the 20th pip) then `brk/begin` | `K.hud('meter_hit')` with `#fkM` 20 (as every count) | (`snd/meter_tick` + the top note) |
| **0** | `play/break`: bubble flares | `brk/begin`: `lib_clear` (every hazard, prop, pull, glide), `p/cancel` (waves included), `field/drop` (meter, low gravity, cut off; cruise counters), `#fgSt 6`, caption "역장 붕괴" | `fx/tele/clear`; `K.hud('banner_end')`, `K.hud('meter_close')`, `K.hud('lowg_off')`, `K.hud('hint_off')`; `K.fx('bubble_glow')` at the core | `K.snd('break_glow')` |
| **5** | `burst` + `tilt` (28° in 9 t) | `brk/burst`: `#fgCrack 4`, `crack/4` | `K.fx('break_burst')` at the core; `K.fx('break_ring')` at the floor under it; `K.hud('pop_break')`; `K.hud('flash_gold')` | `K.snd('break_burst')` |
| **14** | `wobble` (±8° → 0, sinking) | | | `K.snd('groggy_wobble')` |
| 24 | | | `K.fx('spark')` at the core | `block.chain.step` 0.5/0.6 |
| **34** | `sink` → `groggy` (loop) | `groggy/begin`: `#fgSt 3`, groggy hitbox 2.6 × 3.6 / scale 2.0, `look/groggy` | `K.fx('sink_dust')` at the floor; `K.hud('groggy_on')` | `block.beacon.deactivate` 0.8/0.7 |

### Groggy (clock = `#fgT` 0..200)

| t | rig | mechanics | fx (kit) | sound |
|---|---|---|---|---|
| 20, 60, 100, 140, 180 | `groggy` loop (slump, pendulum ±12°, slow wobble) | hittable, no attacks; the green under-bar counts down | `K.fx('groggy_sparks')` at the core (`~ ~2.5 ~`) (ambient) | `K.snd('groggy_spark')` |
| 40, 120 | | | | `block.anvil.place` 0.3/0.5 (a creak) |
| **200** | | `recover/begin` | | |

The core's every-20 t `cfx/groggy_spark` becomes every 40 t (the kit recipe says 30-40 t; 20 t is noisy).

### Recover (clock = `#fgT` 0..15)

| t | rig | mechanics | fx (kit) | sound |
|---|---|---|---|---|
| **0** | `play/recover`: re-level (0-6) | `#fgSt 4`, `look/idle`, `#fgCrack 0`, `crack/0` (the empty shell is ready for the next field) | `K.hud('groggy_off')`; `K.fx('recover')` at the core (`~ ~3.3 ~`) | `K.snd('recover')` |
| **6** | `flip` (the core flips to the top, 6-15) | `cfx/flip` | `K.fx('spark')` at the ring (`~ ~4.2 ~`) | `K.snd('core_flip')` |
| **15** | `done` (cruise form) | `recover/end`: cruise hitbox, `look/idle`, `#fgCool 16`, `ai/enter` | | |

## 5. Damage areas

None. Everything is cleared at break 0 (`lib_clear`, `p/cancel`, `fx/tele/clear`). A hit the player took on the
same tick from an already-struck hazard stands.

## 6. Telegraphs

No hazards. The reads:
- the 20th pip and the bubble glow (0);
- the burst pop (5);
- "역장 붕괴" on the sub-line / caption;
- " · 그로기" + the green timer under-bar for 200 t: "free hits".

## 7. Projectiles

None. Live slabs and missiles are killed by `p/cancel` / `lib_clear` (they carry `rlk_mb_fg_pat`).

## 8. FX detail

`bubble_glow` (2), `break_burst` (15), `break_ring` (2), `spark`, `sink_dust` (5), `groggy_sparks` ×5 (2, ambient),
`recover` (4), `spark`. HUD: `pop_break`, `flash_gold`, `groggy_on` / `groggy_off`. Peak about 19 fx cards (kit
budget: break 19).

## 9. Sound

From v2 §8: a bright crack (+27 dB air) as the bubble lights and bursts; a metallic groan (masked) during the tilt and
wobble; clockwork for the flip-up.

| tick | sound |
|---|---|
| break 0 | `snd/break_glow` |
| break 5 | `snd/break_burst` |
| break 14 | `snd/groggy_wobble` |
| break 24 | `block.chain.step` 0.5/0.6 |
| break 34 | `block.beacon.deactivate` 0.8/0.7 |
| groggy every 40 t | `snd/groggy_spark` |
| groggy 40, 120 | `block.anvil.place` 0.3/0.5 |
| recover 0 | `snd/recover` |
| recover 6 | `snd/core_flip` |

## 10. Dodge windows

None needed: 249 t without a threat (34 + 200 + 15). The groggy hitbox is lower (2.6 × 3.6, scale 2.0), so melee and
arrows hit the slumped core easily.

## 11. Diagram (side view)

```
 t0   (bubble lights)          t5 BURST, tilt 28 deg        t14-34 wobble, sink
        .-.                         \  ring  /                   ___ring___  3.3 b, roll 25
       ( * ) core 4.1 b               \    /                      \_core_/
 groggy 200 t: slumped, pendulum swinging, sparks every 40 t, hittable, no attacks
 recover: re-level 0-6, core flips to the top 6-15 -> cruise (4 patterns to the next field)
```

## 12. Implementation notes (core)

- `brk/begin`: add `fx/tele/clear`, `hud/banner_end`, `hud/meter_close`, `hud/lowg_off`, `hud/hint_off`
  (`fg_contract.md` §15).
- `brk/burst`: the kit calls. `groggy/begin`: `hud/groggy_on`. `recover/begin`: `hud/groggy_off`.
- `groggy/tick`: sparks every 40 t (`#fgK40` exists).
- The 20th count: `brk/count` runs before `brk/begin` in the module tick order, so the 20th pip flash and sound
  happen on the break tick. Keep that order.

## 13. Checks

- The 20th counted hit: on the next module tick no hazard, prop or pattern is left; `#fgOpen`, `#fgLowG` and
  `#mbLowG` are 0.
- `crack/4` at 5; groggy from 34 for 200 t; recover 15 t; idle at 249.
- No hazard is made from break 0 to recover 15.
- The cruise counters: `#fgCruN` 0, `#fgCruLim` 4.
- A reload during the break becomes a fresh groggy (existing case).
