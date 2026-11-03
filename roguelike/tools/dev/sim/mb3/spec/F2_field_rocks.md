# F2 중력 시스템·파쇄 in the field form: implementation spec

| field | value |
|---|---|
| pattern | id 12, key `frock`, state field, kind normal, owner `field.py` |
| clip | **`frock`**, 110 t → `field_idle`: vent 0, flame 8, **burst 25**, **throw 65**, end 100 (stub rig fallback: `field_erupt`) |
| length | 110 (`max_len=118`); recover 14 |
| element | Geo (5) |
| coefficients | floor burst 1.3 (`DMG['f2']` 130), KB heavy 4; slab 1.1 (`DMG['f2s']` 110), KB 3 |
| hits | as C6: bursts ≤ 1 for a standing player (≤ 2 within 4.7 b), slabs ≤ 2 (cap); worst case 3.5 |
| bands | melee / mid / far (the field bag) |

C6 without the tower build-up (plan). The mechanics are C6's (`C6_rock_tower.md` §5); this file lists only what
differs.

## 1. Footage and plan check

- The plan: "**F2 파쇄 in field form:** bursts walking onto the player and slab throws, as C6 without the tower
  build-up".
- The footage of 바위 날리기 (v3 R) is mostly in the compact form. Take C runs into the field form of v4 T (rocks still
  hanging next to the field device), so the pattern does occur in the field.
- The take-C variant where the device glides low beside the player is **not** used: in the field the device stays at
  the centre (plan, v1 F, core).

| event | rig `frock` | stub | verdict |
|---|---|---|---|
| vent column up (the tell; no tower) | vent 0-8 | violet activation 0-19 | use the rig |
| flame band under the ring (pulsing) | flame 8-25 | — | fx |
| bursts, 8, 6 t apart | burst 25 (25 … 67) | 20 … 62 | **F1: use `ev('frock','burst')`** |
| throws, 5, 8 t apart | throw 65 (65 … 97) | 62 … 94 | F1 |
| back to the field hover | end 100-110 | end 120 | F1: end at `clip_len('frock')` |

Plan disagreements and fixes:
- **F1 — the clip.** The stub uses `field_erupt` (the F1 activation pose) and its own ticks. The rig added `frock` for
  this pattern. **Fix:** `clip = 'frock' if 'frock' in CLIPS else 'field_erupt'`; the burst / throw / end ticks from
  `ev()` and `clip_len()`.
  - Bursts strike at 25, 31, 37, 43, 49, 55, 61, 67 (decals 15 … 57).
  - Throws at 65, 73, 81, 89, 97 (tells 55 … 87); the last landing at about 104.
  - End 110.
- **F2 — the walk, groups and cap:** C6's F1 / F3 fixes (the arc walker at the player's distance from the centre, the
  bursts 7-8 volley pair, ≤ 2 slab hits).
- **Field palette:** decals and throw lines in the violet field palette (`el=9`). Every hit is still Geo.

## 2. AI

- The device is at the centre. `face/track` (3°/t). No dip, no travel.
- Aim locks as C6: σ at 0; each burst decal re-reads the bearing / distance (clamped 2.5-18 b) from the body (the
  centre) to the player; each throw tell locks the feet (`lockp` + `keep('rlk_mb_fg_p12t<j>')`).

## 3. Body travel

None.

## 4. Per-tick timeline

`ring` = body + 5.8 (the field ring centre). `hub` = ring + 0.7.

| t | rig | mechanics | fx (kit) | sound |
|---|---|---|---|---|
| 0 | core plays `frock`: the vent column up (0-8) | σ (sweep side) | `K.fx('vent_flare')` at the hub (`~ ~6.5 ~`) | `K.snd('vent_flare')` |
| 8 | `flame` (flame band under the ring, 8-25) | | `K.fx('flame_band')` at the ring underside (`~ ~5.2 ~`) | |
| 10 | | | | `K.snd('flame_charge')` |
| 16 | | | `K.fx('flame_band')` | |
| 15, 21, 27, 33, 39, 45, 51, 57 | | burst decal k (arc point); GRP_NEW before k = 7 | `K.tele_disc(1.8, 10, el=9)` | `block.amethyst_block.resonate` 0.3/1.4 |
| **25, 31, 37, 43, 49, 55, 61, 67** | `burst` … | burst k strikes (vis 121); slab k rises at +2 | `K.fx('floor_burst')`; at +2 `K.fx('slab_rise')` | `K.snd('floor_burst')`; at +2 `K.snd('slab_lift')` |
| 55, 63, 71, 79, 87 | | throw tell j unless capped | `K.tele_line(len, 2.4, 10, el=9)` from slab j's floor point to the lock | `block.chain.hit` 0.5/0.8 |
| **65, 73, 81, 89, 97** | `throw` … | throw j: blade pj 1.5 b/t unless capped | `K.fx('slab_throw')`; `K.fx('slab_trail')` every 2 t | `K.snd('slab_throw')` |
| each landing | | shatter (`pj_end` 1/2), count a hit (4) | `K.fx('slab_impact')` | `K.snd('slab_impact')` |
| **100** | `end` (back to the hover, 100-110) | crumble every unthrown slab | `K.fx('slab_impact')` under each | `K.snd('debris_land')`, `block.piston.contract` 0.5/0.9 |
| 110 | → `field_idle` | `g.end()` + `rocks_cancel(12)` | | |

## 5. Damage areas

Exactly C6 §5 with:
- pid 12, tags `rlk_mb_fg_p12*`;
- vis 121;
- the burst ticks / throw ticks above;
- the decals and lines at `el=9`;
- `DMG['f2']` / `DMG['f2s']`;
- the slab cap counter `#fq12SH`.

## 6. Telegraphs

The vent + flame band (25 t before the first burst), then per burst a violet `tele_disc` r 1.8 10 t ahead, per throw
a violet `tele_line` w 2.4 10 t ahead.

## 7. Projectiles

The slabs: kit `prop/slab`, as C6 (rise 4-6 b over 12 t at the burst; blade pj hr 0.8, reach 1.45 b, 1.5 b/t, life
24, wall stop).

## 8. FX detail

`vent_flare`, `flame_band` ×2, `floor_burst` ×8, `slab_rise` ×8, `slab_throw` ×5, `slab_trail` (ambient),
`slab_impact` ×5-8. Field pebbles continue (ambient).

## 9. Sound

As C6 without the dip / tower / revert sounds:

| tick | sound |
|---|---|
| 0 | `snd/vent_flare` |
| 10 | `snd/flame_charge` |
| each burst decal | `block.amethyst_block.resonate` 0.3/1.4 |
| each burst | `snd/floor_burst` |
| each slab rise | `snd/slab_lift` |
| each throw tell | `block.chain.hit` 0.5/0.8 |
| each throw | `snd/slab_throw` |
| each landing | `snd/slab_impact` |
| 100 | `snd/debris_land` + `block.piston.contract` 0.5/0.9 |

## 10. Dodge windows (low gravity on)

- **Bursts:** the 10 t decal (the same walk-out numbers as C6). Now the **jump is easy**: low gravity keeps the feet
  above 1.2 b from press +3 to +21, so any press in **strike −21..strike −3** clears a burst (19 t window). That is
  the caption's "점프질 해야 피하기 쉽다" (easier if you keep jumping). A swinging player cannot jump: stop the combo
  or dash first. Dash i-frames: press at strike −5..strike.
- **Slabs:** sidestep 1.5 b within about 16 t of the line appearing (walk 7 t, half speed 14 t). A jump does not dodge
  the blade (two rows; the slab descends toward the feet). Dash i-frames work.
- No F2 hit ignores the dash i-frames.

## 11. Diagram

```
          b1 . b2 .  b3 .
                         b4 .  b5 .  b6
     [S] centre                          b7  b8 = x (player, 10 t before)
     violet decals r 1.8 (10 t, jumpable y <= 1.2), slabs rise, 5 throws 65..97
```

## 12. Implementation sketch

Call the shared C6 helper (module-local in `field.py` / `cruise.py`):

```python
F2_CLIP = 'frock' if 'frock' in CLIPS else 'field_erupt'
F2_BURST = ev_or('frock', 'burst', 25)
F2_THROW = ev_or('frock', 'throw', 65)
F2_END = clip_len(F2_CLIP) if F2_CLIP == 'frock' else 120
Pattern(12, 'frock', '중력 시스템·파쇄', 'f', F2_CLIP, bands=('melee', 'mid', 'far'), recover=14,
        max_len=F2_END + 8, length=F2_END)
rock_arc(g, tl, 'frock', pid=12, burst0=F2_BURST, throw0=F2_THROW, el_tele=9, dmg=DMG['f2'], dmg_s=DMG['f2s'],
         crumble_at=ev_or('frock', 'end', 100))
```

## 13. Checks

- With the real rig, bursts strike at 25 + 6k, throws launch at 65 + 8j, the end is at 110.
- Decals: tell 10, r 1.8, y1 1.2, el 9 visuals, dmg 130. The 7/8 pair forms one group.
- A low-gravity jump pressed at strike −10 clears a burst. Standing still: ≤ 1 burst hit + ≤ 2 slab hits.
