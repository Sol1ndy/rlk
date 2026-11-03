# F1 중력 시스템·감소 영역 (바닥 뜯기): implementation spec

| field | value |
|---|---|
| pattern | id 11, key `fzone`, state field, kind normal, owner `field.py` |
| clip | `field_erupt`, 40 t → `field_idle`: activate 0, lock 12, **erupt 22**; the module runs the 9 events on its own clock |
| length | **260** (`max_len=268`); recover 14 |
| element | Geo (5) |
| coefficient | 1.2 per event (`DMG['f1']` 120, raw 15); all discs of one event are **one volley group** |
| hits | ≤ 1 per event; standing still means one per event (9 × 1.2 = 10.8); a moving player takes 0-2 |
| bands | melee / mid / far (the field bag) |

## 1. Footage and plan check

Sources:
- v3 Z, 0.42-16.20 s (`understand/v3.md` §2 Z), caption **바닥 뜯기 / 범위가 표시된 후 바닥이 뜯겨져 나와 피해를 준다**
  (after the area is shown, the floor is torn out and deals damage);
- v2 A2 (the same zones in the field form, night).

Z0 = the core drum turning. I re-checked `sheet_tear_telegraphs_rows.jpg` (one row per eruption).

| event | footage Z+ t | rig / stub | verdict |
|---|---|---|---|
| activation: the drum faces the player, the medallions slide out to ±4 m on gold link beams | 0-22 | `field_erupt` activate 0, lock 12 (the arch locks facing the front), erupt pulse 22 | ok |
| telegraph 1: 3-4 overlapping dark discs 3-8 m to the player's side | 22-37 | first decal at 22 (tell 15) | ok |
| eruption 1: a mound of floor chunks 3.5-4 m tall | 37 | 22 + 15 = 37 | ok |
| eruptions 2-9 | 87, 117, 135, 156, 185, 195, 235, 246 | stub: 55, 67, 93, 115, 131, 161, 185, 205 | **F1** |
| beams off, the gyroscope spins again | 204-208 | — | fx |
| the device tilts and drifts | 254-280 | end 260 | ok |

- **Telegraph lead:** 0.70-0.75 s = 15 t ✓. **Disc r:** 2.8 (2.5-3.2) ✓.
- **Placement:** 1-4 discs per event, 2-8 m from the player, "at least one often right next to them; never centred on
  them" ✓ (stub).
- **Not jumpable:** the eruption is 3.5-4 b tall; the low-gravity apex is 2.96 b.

Plan disagreements and fixes:
- **F1 — the event clock.** The stub's gaps (18, 12, 26, 22, 16, 30, 24, 20) are tighter than the footage's (50, 30,
  18, 21, 29, 10, 40, 11; the plan says "11-50 t intervals"). **Fix:** use the footage, with the 10 t gap raised to 11
  for the plan's minimum.
  - Decals at 22, 72, 102, 120, 141, 170, 181, 220, 231.
  - Strikes at 37, 87, 117, 135, 156, 185, 196, 235, 246 (gaps 50, 30, 18, 21, 29, 11, 39, 11).
  - The end at 260, as the footage's last eruption + the tilt.

  The two 11 t gaps make overlapping events, which is the footage's "dangerous when chained" pressure.
- **Field palette.** Field decals use the kit's violet palette (el 9), as `fg_fx_api.md` §4 says for the field
  patterns. Every hit is still Geo.

## 2. AI

- The device is at the centre (field). `face/track` (3°/t) throughout. The rig's arch lock (12) faces its front.
- **Placement per event** (as the body, at the decal tick; one volley group per event):
  - N = `random 1..4`;
  - disc 1 at 2.0-3.0 b from the player's feet, a random yaw;
  - discs 2..N at 2.0-8.0 b, random yaws;
  - each pulled into the walk disc (r 20.3, `g.clamp_walk()`).

  The stub's `event` / `more` / `disc` / `place` functions are right.

## 3. Body travel

None.

## 4. Per-tick timeline

`core` = body + 4.1. `medal_e` / `medal_g` = `^3.85 ^4.1 ^0` / `^-3.85 ^4.1 ^0`.

| t | rig | mechanics | fx (kit) | sound |
|---|---|---|---|---|
| 0 | core plays `field_erupt`: activate (the arch slows, the eye looks out, slit hot) | `face/track` | `K.fx('spark')` at both medallions | `block.beacon.activate` 0.7/1.3, `block.conduit.activate` 0.6/1.2, `block.crafter.craft` 0.6/0.7 |
| 6 | | | link-beam glints: `K.fx('spark')` at the midpoints `^1.9 ^4.1 ^0` / `^-1.9 ^4.1 ^0` | |
| 12 | `lock` (the arch locks facing the front) | | | `block.chain.place` 0.5/1.2 |
| **22** | `erupt` (gold pulse from the core, a 0.15 b bob) | **event 1** (§5) | `K.fx('flash')` at the core; per disc: `K.fx('erupt_tell')` + `K.tele_disc(2.8, 15, el=9)` | `K.snd('erupt_tell')` once |
| **37** | | event 1 erupts (vis 111, `#hzEv 1` per disc) | per disc `K.fx('erupt')` | `K.snd('erupt')` once per event (the first disc's vis) |
| 40 | (back to `field_idle`) | | per disc `K.fx('debris')` (ambient) | |
| 62 | | | | `K.snd('debris_land')` |
| 72, 102, 120, 141, 170, 181, 220, 231 | | events 2-9 (decals) | as at 22, without the core flash | `K.snd('erupt_tell')` |
| 87, 117, 135, 156, 185, 196, 235, 246 | | the eruptions | as at 37 | `K.snd('erupt')`; `K.snd('debris_land')` at +25 |
| 206 | | | | `block.chain.place` 0.6/0.9, `block.copper_trapdoor.close` 0.6/0.9 (beams off) |
| 260 | | `g.end()` | | |

## 5. Damage areas

```
# p/fzone/event (as the body): one volley group, N discs
g.GRP_NEW
execute store result score #fq11N mb run random value 1..4
execute store result storage rlk:mboss fg.fz.d double 0.1 run random value 20..30      # disc 1
function …/disc ; function …/more                                                      # discs 2..N: 20..80
# p/fzone/disc
execute store result storage rlk:mboss fg.fz.a double 1 run random value 0..359
function …/place with storage rlk:mboss fg.fz            # marker rlk_mb_fg_p11d at the player + (a, d), floor
execute as <p11d> run <g.clamp_walk()>
*g.hz_opts(kb=KB['default'], grp=True, vis=111, quiet=1, sfx=0)
execute at <p11d> run <g.hz_disc(2.8, 15, DMG['f1'])>
execute at <p11d> rotated ~ 0 run <K.tele_disc(2.8, 15, el=9)>
execute at <p11d> run <K.fx('erupt_tell')>
kill <p11d>
```

- **Shape:** disc r 2.8 (padded 3.1), height −0.5..3.5 (not jumpable, even with low gravity), act 1, KB 3 (0.6 b),
  Geo, 1.2.
- **Group:** all discs of an event are made in the same tick (FW-4 safe): one hit per event.
- **The sound once per event:** the `vis` handler plays `snd/erupt` only when `#fq11S` < the event index (set it at
  the first disc's strike), or simply only on the disc made first (tag it `rlk_mb_fg_p11f` at creation).

## 6. Telegraphs

- 15 t per event: the violet kit decal (rim + fill reaching the rim on the strike tick) plus the dark `erupt_disc` card
  fading in over 6 t (the footage's darkened floor).
- The pattern's long read is the activation (0-22): medallions out on the link beams, the arch locking.
- At most 4 discs per event and 2 events overlapping: 16 telegraph cards (kit budget 14, measured on the stub ticks).
  OK under the cap of 40.

## 7. Projectiles

None. The flying debris is fx (`p/erupt` chunks, `p/debris` hovering chunks).

## 8. FX detail

`spark` ×4, `flash`, per disc `erupt_tell` (1) + `erupt` (9) + `debris` (5, ambient). Peak about 47 fx cards on a
4-disc eruption (kit budget: F1 47, with 8 ambient skips). The pebbles of the field keep drifting (ambient).

## 9. Sound

From v3 §5 and v2 §8: a whir + bright hum at the activation; the telegraph is masked by the BGM (a quiet charge
click); a crack + gravel burst per eruption (+8..+23 dB); a soft patter about 1 s later.

| tick | sound |
|---|---|
| 0 | `block.beacon.activate` 0.7/1.3, `block.conduit.activate` 0.6/1.2, `block.crafter.craft` 0.6/0.7 |
| 12 | `block.chain.place` 0.5/1.2 |
| each decal tick | `snd/erupt_tell` (once) |
| each eruption | `snd/erupt` (once) |
| eruption + 25 | `snd/debris_land` |
| 206 | `block.chain.place` 0.6/0.9 + `block.copper_trapdoor.close` 0.6/0.9 |

## 10. Dodge windows

- Disc 1 is 2-3 b from the player's feet with r 3.1 (padded): the player is inside it, 0.1-1.1 b from its edge.
  - Walk: 5 t. Half-speed (swinging): 10 t. Sprint: 4 t. All inside the 15 t lead.

  So a melee player keeps attacking, sidesteps once per event, and keeps the meter going. Other discs (2-8 b off)
  may block a direction: read the decals.
- Jump: no (y1 3.5 > apex 2.96).
- Dash i-frames: yes (press 0-5 t before the eruption).
- Worst case standing still: one hit per event (10.8 over 9 events). Realistic: 0-2 (1.2-2.4).

## 11. Diagram

```
              o         (disc 2..N, 2-8 b off)
        .--.
       ( D1 )  x player     disc 1 always 2-3 b off: the player stands in it
        '--'        .--.
                   ( D3 )   decal 15 t (violet), eruption r 2.8, one hit per event
   [S] at the centre, link beams to the medallions
   events at 22 72 102 120 141 170 181 220 231 (+15)
```

## 12. Implementation sketch

The stub is right in mechanics. Change:
- `F1_EVENTS` to the footage ticks (F1) and `F1_END` to 260;
- add the kit calls (decal el 9, `erupt_tell`, `erupt`, `debris`) and the once-per-event sounds.

## 13. Checks

- 9 events at 22, 72, 102, 120, 141, 170, 181, 220, 231. Each has 1-4 discs: r 2.8, tell 15, dmg 120, one group
  made in one tick.
- A standing player is hit once per event (inside disc 1). With N forced to 1 (a test seed), a player who steps
  1.2 b away from disc 1's centre side is not.
- Every disc is inside the walk disc r 20.3.
- The pattern ends at 260.
