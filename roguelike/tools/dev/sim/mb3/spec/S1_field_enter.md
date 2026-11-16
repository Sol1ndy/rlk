# S1 역장 생성 · 중력 감소: field opening (warp + unfold + low gravity): implementation spec

| field | value |
|---|---|
| owner | core service **20** (`field_in`: mechanics in `p/svc`, fx in `p/field_in/*`) |
| clips | `warp_out` (34, hold: flip 0, **hide 12**, **out 13**), then `warp_in_field` at 34 (24 → `field_idle`: in 0, **unfold 1**, field 17, **banner 22**) |
| clock | the service clock = `warp_out` tick; 34 + t = `warp_in_field` tick t |
| key ticks | warp-out 13, warp-in 34, **unfold 35** (meter open, targetable), **banner 56** (low gravity), end 57 |
| trigger | after 5 cruise patterns (first field) or 4 (later), at a pattern boundary (`ai/next_c` → `field/go`) |
| damage | none |

## 1. Footage and plan check

Source: v1 F, 31.85-38.70 s (`understand/v1.md` §3 F); F0 = the halo flip.

| event | footage F+ t | rig / core | verdict |
|---|---|---|---|
| the halo flips upright and spins; the device noses up 30-40° (whoosh at +1) | 0-12 | `warp_out` flip 0 (nose up 35°, 0-11) | ok |
| warp-out: a 1-2 frame white-cyan pillar where the device was; it is gone | 13 | rig `hide` 12 (vis 1 → 0 over 11-12), core `field/warp` at `out` 13 | **F1** |
| violet glitch streaks drift up and out over the old spot; gold dust | 14-33 | invisible (hold) | fx |
| warp-in flash at the arena centre | 34 | `warp_in_field` in 0 (vis 0 → 1 over 0-2, ring 5.8 b) | ok |
| unfold into the field form: layers spread like a spring, halos violet, violet column, tendrils | 35-51 | `unfold` 1-17 (field form at 17), link beams + column 17-21 | ok |
| banner wipe / text "중력이 감소하고 점프 능력이 향상되고 있습니다…" | 53 / 57 | `banner` 22 → clock 56 | ok |
| slow yaw (90° in 1.5 s), pebbles float all over the arena | 51-91 | field idle, 3°/t | ok |
| core drum flips (≈ 90°) | 102-105 | — | **F2** (pre-wave tell) |
| the end-spike units detach and orbit 5-6 m out | 105-113 | — | F2 |
| gold streaks rise from the floor around the device | 113-131 | — | F2 (kit `gold_streaks`) |
| charge of the first 「인력 충격파」 (sphere round the core) | 129-137 → (cut) | the opening waves start at the next decision | **F2** |

Plan disagreements and fixes:
- **F1 — the warp-out tick.** The rig is invisible from 12 and the core flashes / teleports at 13, which leaves one
  empty tick. **Fix:** play the warp-out fx (`p/warp_out` pillar + `snd/warp_out`) at `ev('warp_out','hide')` (12).
  The untargetable flag and the teleport stay at `out` (13). The device then vanishes inside the flash.
- **F2 — the settle before the first wave.** The core starts the opening waves at the first decision after 57
  (`field/opened` sets `#fgCool 1`), so the first front lands at about 57 + 1 + 25 = 83. The footage gives about
  75 t of settling first: the slow yaw, the core flip, the spike units detaching, gold streaks from the floor, then
  the charge at ≈ 129. That settle is when the player reads the banner, tries the floaty jump and lands the first
  meter hits. **Fix (core, one constant):** `field/opened` sets `#fgCool 40`. The first wave charges at ≈ 98 and
  lands at ≈ 123. Add the fx of the settle: `K.fx('gold_streaks')` at 70 and 85, `K.fx('field_idle')` every 15 t.
- **Low gravity at the banner (56), not the unfold (35):** as the plan and the footage. The meter and the ×0.6 cut
  start at the unfold.

## 2. AI

- 0: `face/player` (the stub's `tp … facing`): the nose-up shows the underside to the player.
- 13: the body is teleported to the arena centre (`u/centre`), facing the player, untargetable (`rlk_mb_inv`).
- 35 → the field: no travel; the idle tracks at 3°/t (`ai/idle_f`).

## 3. Body travel

13: `tp` to the arena marker (the centre). Hidden from 12 to 34, so the jump is invisible. A glitch marker
(`rlk_mb_fg_fxw`) stays at the old spot, 13-34.

## 4. Per-tick timeline (service clock)

`halo` = body + 4.5 + 1.6 = 6.1 (cruise). After 34 the body is at the centre: `core` = + 5.8 at 34 (folded), + 4.1
from 51 (the field core). `old` = the glitch marker (floor).

| t | rig | mechanics (core) | fx (kit) | sound |
|---|---|---|---|---|
| 0 | `warp_out`: halo flip, nose up 35° | `field/warp_begin`: `#fgField 1`; `face/player`; HUD (name line "역장") | `K.fx('halo_flip')` at the halo | `K.snd('halo_flip')` |
| 6 | | | | `block.beacon.power_select` 0.8/1.2 |
| **12** | `hide` (vis → 0) | | `K.fx('warp_out')` at the floor under the body (pillar 1-2 frames, glitch start, gold dust); `K.hud('flash_white')` for players within 8 b | `K.snd('warp_out')` |
| **13** | `out` (hidden, holding) | `field/warp`: glitch marker at the old spot, `rlk_mb_inv`, `tp` to the centre facing the player | | |
| 14, 19, 24, 29 | | | `K.fx('glitch')` at `old` (ambient) | `K.snd('glitch')` at 16 |
| **34** | `play/warp_in_field`: in (vis → 1 over 0-2, ring 5.8 b) | kill the glitch marker | `K.fx('warp_in')` at the core (`~ ~5.8 ~`); `K.fx('warp_pillar')` at the floor under it | `K.snd('warp_in')` |
| **35** | `unfold` (1-17: core drops 1.7 b, plates spread, pods out, medallions out, halos violet) | `field/open`: targetable; **meter 0/20**; `crack/0`; `look/field`; field hitbox 2.8 × 5.2 / scale 2.6; the ×0.6 cut; `#fgFN` + 1; the hint (first field) | `K.fx('field_unfold')` at the core (`~ ~4.8 ~`); `K.hud('meter_open')`; `K.hud('hint_on')` (first field only) | `K.snd('field_unfold')` |
| 39, 43, 47 | | | `K.fx('field_idle')` at `~ ~4.4 ~` | |
| 51 | `field` (17: field form; link beams + violet column 51-55) | | `K.fx('spark')` at each medallion (`^3.85 ^4.1 ^0`, `^-3.85 ^4.1 ^0`) | `block.beacon.activate` 0.5/0.7 |
| **56** | `banner` (22) | `field/banner`: `#fgLowG 1` (→ `#mbLowG` every module tick → `rlk:mb_lowg` on the player and the avatar); the caption | `K.hud('banner_field')` (actionbar 4 s, pop, its own sound); `K.hud('lowg_on')`; `K.fx('pebbles')` at the player's feet | (`snd/field_banner` inside `banner_field`) |
| 57 | → `field_idle` | `g.end()` → `field/opened` (`#fgField 2`, `#fgCool` **40**, F2) | | |
| after: 70, 85 | | | `K.fx('gold_streaks')` at the floor under the device | |
| every 15 t | | | `K.fx('field_idle')` at the core | `K.snd('field_hum')` every 40 t |
| every 20 t while low gravity | | core `field/tick` | `K.fx('pebbles')` at the player's feet (never the eyes: the PL-1 lesson) | |

## 5. Low gravity (framework `#mbLowG`, core `#fgLowG`)

- **Modifiers `rlk:mb_lowg`:**
  - gravity −0.5 `add_multiplied_base` (×0.5);
  - jump_strength +0.19 `add_multiplied_base` (×1.19);
  - safe_fall_distance +4 `add_value`.

  They go on the player and every `rlk_av` avatar, re-added every tick. The avatar jump reads its own jump_strength
  (`view/move`: 0.4998).
- **Jump:** apex 2.96 b, 25 t in the air; feet above 0.7 b from press +2 to +22 (vanilla: apex 1.25, 12 t).
- **The swing hold still wins:** no jump while swinging (jump ×0). A dash ends the swing at once.
- **Cleanup paths** (contract §7.5, all core / framework):
  - pause (the request lapses);
  - the break (`field/drop`);
  - the pack-up (`field/close` at field_end 0);
  - death (`death_start`);
  - every framework end (`player_reset`);
  - relog;
  - `uninstall` (`lowg_rem`).
- The HUD flag `hud/lowg_on` / `lowg_off` mirrors it on the name line.

## 6. Telegraphs

No hit. The reads are:
- the halo flip (a field is coming);
- the warp flash;
- the banner (the rule change);
- the floating pebbles and the low-gravity icon (state);
- the meter on the sub-line.

## 7. Projectiles

None.

## 8. FX detail

`halo_flip` (4), `warp_out` (6), `glitch` ×4 (3), `warp_in` (3), `warp_pillar` (2), `field_unfold` (6), `field_idle`,
`spark` ×2, `pebbles` (6, ambient), `gold_streaks` (5, ambient), and the HUD pops / flashes `flash_white` (optional,
near players only). Peak about 14 fx cards (kit budget: field warp 14).

## 9. Sound

From v1 §6: a whoosh at the flip, a bright zap and low whoomp for each warp, a violet glitch crackle, a low drone
(centroid 0.7 kHz) from the banner, a clank + whoosh at the core flip.

| tick | sound |
|---|---|
| 0 | `snd/halo_flip` |
| 6 | `block.beacon.power_select` 0.8/1.2 |
| 12 | `snd/warp_out` |
| 16 | `snd/glitch` |
| 34 | `snd/warp_in` |
| 35 | `snd/field_unfold` |
| 51 | `block.beacon.activate` 0.5/0.7 |
| 56 | `snd/field_banner` (via `hud/banner_field`) |
| every 40 t of the field | `snd/field_hum` |

## 10. Dodge windows

Nothing to dodge.
- 0-12: the device can still be hit at its old spot, but the meter is not open, so nothing counts.
- 13-34: untargetable.
- From 35: hits count toward the meter (cap one per 6 t) and deal ×0.6.

## 11. Diagram

```
 old spot (cruise)                         arena centre C
 t0-11  halo flips, nose up
 t12    pillar flash, gone  ~~~ violet glitch 14-33 ~~~
                                           t34 warp-in flash (ring 5.8 b)
                                           t35-51 unfold: core hangs 4.1 b, medallions +-3.85 b
                                           t35 meter 0/20, targetable, damage x0.6
                                           t56 banner, LOW GRAVITY
                                           t57 -> settle 40 t -> opening waves
```

## 12. Implementation notes (core)

- `p/svc`: warp-out fx at `ev('warp_out','hide')`. The kit lines go into the `field_in` timeline (they are fx only).
- `field/opened`: `#fgCool 40` (F2). This changes the core's field-cycle test expectation in `test_fieldgen.py` §3
  (the first wave impact moves from opening + 1 + 25 to opening + 40 + 25).
- Integration hooks (`fg_contract.md` §15): `field/open` → `hud/meter_open` (+ `hint_on`); `field/banner` →
  `hud/banner_field` + `hud/lowg_on`.

## 13. Checks

- `rlk_mb_inv` from 13 to 35. The body is at the centre from 13.
- Meter open at 35, low gravity from 56 (`#mbLowG` 1 on every module tick after it).
- The glitch marker is gone at 34 and after a cancel.
- The first wave impact is about 40 + 25 t after the end of the opening.
- A test cut during the opening finishes the field at once (`field/up`).
