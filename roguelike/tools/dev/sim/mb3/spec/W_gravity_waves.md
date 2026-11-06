# W 「인력 충격파」 ×3 (중력 웨이브): implementation spec

| field | value |
|---|---|
| pattern | id 21, key `waves`, state field, kind **service** (the core starts it: opening `#fgWvK 1`, closing `#fgWvK 2`), owner `field.py` |
| clips | `wave` (40: charge 0, beam 25, **impact 25**) at 0 and 68; the 3rd wave: **opening `wave_long`** (56: impact 41) at 135, **closing `wave_drop`** (84: drop 36, land 40, impact 40, lift 60, risen 80) at 136. Stub rig fallback: `wave` |
| impacts | **25, 93, 176** (gaps 68 / 83); charges 25 / 25 / 41 (opening) or 40 (closing) |
| < 50 % HP | the 3rd wave fires 3 fronts: plan 9 t apart (185, 194); **recommended 6 t** (182, 188), see F3 |
| length | opening 213 (triple 225 / 231), closing 220 (triple 225 / 231): `g.set_len` at 135 |
| element | Geo (5) |
| coefficient | 1.2 per front (`DMG['wave']` 120, raw 15); one hit per front |
| special | **dash i-frames do not help** (`#hzNoDodge`); low hit band 0-0.7 b (a jump clears it) |

## 1. Footage and plan check

Source: v2 B, 16.28-31.30 s (`understand/v2.md` §3 B), caption **중력 웨이브 / 역장 생성의 시작과 끝에서 사용하는 패턴 /
대시 회피 불가능** (used at the start and end of the field; cannot be dodged with a dash), and clip C (the wave seen from
the upper gallery).

| event | footage | rig | verdict |
|---|---|---|---|
| charge: a bright yellow sphere ≈ 1.9 m round the lower core, orbit swirls, pulses | 23-24 t (waves 1-2), 40-42 t (wave 3) | `wave` charge 0-24 (4 pulses); `wave_long` 0-40; `wave_drop` 0-39 | ok |
| a vertical gold beam core → floor, 1-2 frames, then a floor splash | impact | `beam` = `impact` 25 / 41 / 40 | ok |
| burst flare: white-gold dome ≈ 4 m wide × 2 m tall | impact + 0..+3 | fx | ok |
| the flare dims into a filled fire disc r ≈ 1.8 m (held 5 t) | +1..+6 | fx (`wave_burst`) | ok |
| the ring front expands at 10-12 m/s (0.5-0.6 b/t) from r 2.5 to the wall; a burning band 2-3 m wide | +7 → | the hazard grows r = 2.5 + 0.55 k from the impact | ok (see F4) |
| the player jumps over it with a long low-gravity arc (airtime 22-26 t, apex 2.5-3.5 m) | | low gravity: apex 2.96 b, 25 t | ok |
| impact 1 → 2: 3.40 s | 68 t | 25 → 93 | ok |
| impact 2 → 3: 4.17 s | 83 t | 93 → 176 | ok |
| wave 3: the device sinks 0.5 m during the charge, then after the impact **drops onto the floor** (+5..+8), grounded about 19 t, then the lift-off flash, the rise, the lances, the pack-up | 3rd wave of clip B (the closing sequence: it ends in the compact form) | `wave_drop`: sink 0-36, drop 36-40, **impact on landing 40**, grounded 40-60, lift 60, risen 80 | **F1 / F2** |
| below 50 % HP the 3rd wave fires 3 fronts (PDF; not in the footage) | — | plan: 9 t apart | **F3** |

Plan disagreements and fixes:
- **F1 — which 3rd clip.** The stub plays `wave` for every wave and gives the 3rd a 40 t charge without a 40 t clip.
  The rig has two 3rd-wave clips.
  - **Opening: `wave_long`** (no drop; the device must stay up for the field patterns).
  - **Closing: `wave_drop`**: the footage's drop belongs to clip B, which ends in the pack-up, and the rig's
    `field_end` starts from the hover with a small lift.

  The clip starts at 176 − `ev(clip,'impact')` (135 / 136). The hazard is made at the clip start with
  `tell = ev(clip,'impact')` (41 / 40), so the charge read and the hit line up. Fallback without these clips (stub):
  `wave` at 176 − `ev('wave','impact')`, the hazard at 136, tell 40 (the stub's behaviour).
- **F2 — drop order.** The footage bursts, then drops about 5 t later. The rig drops first and bursts on landing
  (40). Keep the rig: it reads well ("it slams into the floor and the ring leaves it"), and the hit tick is the clip's
  `impact`.
- **F3 — the triple below 50 % HP.** The plan (adapt.md) claims one low-gravity jump clears three fronts 9 t apart.
  With the 0.3 b body pad, a front sits on a standing player for **6 ticks** (r from d − 0.3 − 2.5 to d + 0.3, at
  0.55 b/t). Three fronts 9 t apart cover T..T+5, T+9..T+14 and T+18..T+23. A low-gravity jump keeps the feet above
  0.7 b only from press +2 to +22 (21 t). So:
  - no single jump clears all three;
  - two jumps cannot either: the 4 grounded ticks around a landing never fit the 3 t gaps.

  A standing jumper always takes one front.
  - **Fix (recommended): 6 t apart** (impacts 176, 182, 188): the three fronts then cover T..T+17, and one jump
    pressed at T−5..T−2 clears them all (a 4 t window), which keeps the plan's intent.
  - Alternative: keep 9 t and accept one guaranteed hit unless the player walks *toward* the device while jumping
    (the fronts then pass faster: 0.77 b/t relative, total ≈ 17 t).
- **F4 — the first-tick disc.** The front is `hz/ring {r0:0, r:2.5}` at the impact: a player within 2.8 b of the axis
  is hit on the impact tick (the footage's burning disc under the device). Keep it; the charge sphere is the warning.

## 2. AI

- The device stays at the arena centre (the core put it there). No travel.
- Facing: `face/track` (3°/t) for the look only; the waves are radial.
- `#fgTri` / HP < 50 % is read at the 3rd charge start (135): `mhpC × 2 < mhpM` or test 42.

## 3. Body travel

None (`wave_drop` drops and rises in the clip).

## 4. Per-tick timeline

`core` = body + 4.1 (field). For `wave_drop` use the clip anchor: 3.6 at 36, 1.25 at 40-60. `floor` = the body's
floor point (the centre). W_i = the impact tick of wave i.

| t | rig | mechanics | fx (kit) | sound |
|---|---|---|---|---|
| **0** | core plays `wave` (charge 0-24) | front 1 made: `hz/ring` r0 0 → r 2.5, tell 25, tagged p21f | `K.tele_wave(2.5, 21.0, 2.5, 25, 34)` at `floor`; `K.fx('wave_charge', t=25)` at `core` | `K.snd('wave_charge')` |
| 8, 16 | | | `K.fx('wave_pulse')` at `core` | |
| 15 | | | | `K.snd('wave_charge2')` |
| 24 | | | `K.fx('wave_band', r0=25, r1=210, w=25, dur=34)` at `floor` (moves from 25 in step with the hazard) | |
| **25** | `beam` / `impact` | front 1 strikes; `grow` every tick after (r = 2.5 + 0.55 k, r0 = r − 2.5) | `K.fx('wave_beam', h=4.1)` at `floor` | `K.snd('wave_beam')` |
| 26 | | | `K.fx('wave_burst')` at `floor` | `K.snd('wave_burst')` |
| 25 + 3k (k = 0..11) | | | `K.fx('wave_fire', r=2.5 + 0.55·3k)` at `floor` | `K.snd('wave_ring')` at the front point nearest the player |
| 40 | → `field_idle` | | | |
| **68** | `play/wave` | front 2 made (tell 25) | as at 0 (`tele_wave`, `wave_charge`) | `K.snd('wave_charge')` |
| 92 / **93** | | front 2 strikes at 93 | `wave_band` at 92; `wave_beam` at 93; `wave_burst` at 94; fire / ring sounds every 3 t | as wave 1 |
| **135** (opening) | `play/wave_long` (charge 0-40) | `tri` check → `#fq21T`; front 3 made (tell 41); `g.set_len(…)` | `tele_wave(…, 41, 34)`; `wave_charge {t:41}` | `K.snd('wave_charge')` |
| **136** (closing) | `play/wave_drop` (sinks 0.5 b, 136-172) | `tri` check; front 3 made (tell 40); `g.set_len(…)` | `tele_wave(…, 40, 34)`; `wave_charge {t:40}` | `K.snd('wave_charge')` |
| every 8 t of the 3rd charge | | | `K.fx('wave_pulse')` | |
| 166 | | | | `K.snd('wave_charge2')` |
| 172-176 (closing) | `drop` 36 → `land` 40 (ring 2.4 b, the core on the floor) | | | `block.heavy_core.place` 0.8/0.6, `block.anvil.land` 0.5/0.6 at 176 |
| 175 / **176** | `impact` (41 / 40) | front 3 strikes | `wave_band` at 175; `wave_beam` (h 4.1 opening, 1.25 closing) at 176; `wave_burst` at 177 | `K.snd('wave_beam')`, `K.snd('wave_burst')` |
| triple, recommended (G 6) | | fronts 4 / 5 made at 172 / 178 (tell 10), strike 182 / 188 | per extra front: `tele_wave(…, 10, 34)` at its make tick, `wave_band` at strike − 1, `wave_beam` + `wave_burst` at the strike | `K.snd('wave_beam')` per extra front |
| (plan G 9) | | fronts 4 / 5 made at 175 / 184 (tell 10), strike 185 / 194 | the same | |
| 196 (closing) | `lift` 60 (lift-off pulse) | | `K.fx('lift_off')` at `floor` | `K.snd('lift_off')`, `K.snd('rise_hum')` |
| 216 (closing) | `risen` 80 | | | |
| end | → `field_idle` | the end: last strike + 37 or the clip end, whichever is later | | |

End ticks:

| | single 3rd | triple G 6 | triple G 9 |
|---|---|---|---|
| opening | 213 | 225 | 231 |
| closing | 220 | 225 | 231 |

## 5. Damage areas

```
def front(tell):
    return [*g.hz_opts(act=36, y1=0.7, kb=KB['default'], nododge=1, sfx=0, vis=211, quiet=1),
            g.hz_ring(0.0, 2.5, tell, DMG['wave']), g.tag_last_hz('rlk_mb_fg_p21f')]
# made at the body (the centre) on the floor; the stub's 'grow' runs from extra_tick for every p21f:
#   k = mbHzT - mbHzW + 1 (k-th active tick), r = 25 + 11k/2 tenths, r0 = r - 25, w 0 -> hz/resize_s
```

- **Shape:** an expanding ring.
  - At the strike tick: r0 0, r 2.5 (the burst disc).
  - Then at each active tick k ≥ 1 the band is [r − 2.5, r] with r = 2.5 + 0.55 k, padded 0.3 on both sides.
  - Active 36 t: the band passes r 21 (the wall) at k ≈ 34.
  - Height −0.5..0.7 b.
- Geo, 1.2 per front, KB 3 (0.6 b, outward), **#hzNoDodge 1** (the dash i-frames are saved, zeroed and restored
  around the hit: the player keeps them for other hazards).
- Each front is its own hazard: ≤ 1 hit per front. A sequence is 3 fronts (3.6), or 5 fronts below 50 % HP (6.0).

Exposure of a standing player at distance d (whole ticks after the impact):

| d (b) | 3 | 5 | 8 | 12 | 16 | 20 |
|---|---|---|---|---|---|---|
| hit ticks k | 1-6 | 4-9 | 10-15 | 17-22 | 24-29 | 32-36 |

## 6. Telegraphs

Per front:
- the charge sphere (25 / 41 / 40 t, 4 pulses);
- the violet `tele_wave` disc filling to r 2.5 at the axis over the charge;
- then the drawn front ring and its second ring 2.5 b behind (in sync with the hazard every tick);
- the standing flame wall of `wave_band` (16 segments).

Extra fronts (triple): a fresh `tele_wave` with tell 10 and a second charge pulse at the core. Telegraph cards ≤ 10
(kit budget).

## 7. Projectiles

None.

## 8. FX detail

Per front: `wave_charge` (4), `wave_pulse` ×2-5 (4), `wave_band` (16), `wave_beam` (2), `wave_burst` (4), `wave_fire`
×12 (particles only). The closing sequence adds `lift_off` (5). Peak 59 fx cards with the triple + pebbles (kit
budget, under the cap of 64; the ambient pebbles are skipped first).

## 9. Sound

From v2 §8: a rising airy hiss (+11..+21 dB) during the charge with a 350-400 Hz tone; a thump + bright crack at the
beam / burst; a low rumble while the ring travels (+6..+10 dB); a heavy thud for the drop; an air burst at the
lift-off.

| tick | sound |
|---|---|
| each charge start | `snd/wave_charge` |
| impact − 10 | `snd/wave_charge2` |
| impact | `snd/wave_beam` |
| impact + 1 | `snd/wave_burst` |
| every 3 t of a front | `snd/wave_ring` (at the front point nearest the player) |
| closing 176 | `block.heavy_core.place` 0.8/0.6 + `block.anvil.land` 0.5/0.6 |
| closing 196 | `snd/lift_off` + `snd/rise_hum` |

## 10. Dodge windows (low gravity is always on during the waves)

- **Jump** (feet above 0.7 b from press +2 to +22).
  - One front: press anywhere in **[T−17, T−2]**, where T is the first tick the front touches the player (16 t
    window).
  - Triple, G 6: **[T−5, T−2]** (4 t).
  - Triple, G 9: no single jump works (F3).
- **Swinging players cannot jump.** Stop the combo before the charge ends, or dash (the dash ends the swing at once;
  the dash itself does not dodge), then jump (≥ 1 t later).
- **Dash: does NOT help** (`#hzNoDodge`). This is the only hit of the boss that ignores the i-frames.
- **Leave:** impossible (arena-wide, and no gallery: the plaza wall is 7 high).
- **Under the device:** within 2.8 b of the axis the impact disc hits on the impact tick. Jump before the beam.

## 11. Diagram (top view)

```
                 . - ~ ~ ~ - .         front r = 2.5 + 0.55 k  (k = ticks after the impact)
             . '   . - ~ - .   ' .     band [r - 2.5, r], height 0..0.7 b, 1.2, NO dash dodge
           .     .'  burst  '.    .
          :     :    [S]      :    :   impacts 25 / 93 / 176 (charges 25 / 25 / 41|40)
           '     '.  r 2.5  .'    '    < 50 % HP: + fronts at 182 / 188 (rec.) or 185 / 194 (plan)
             ' .   ' - ~ - '   . '
                 ' - ~ ~ ~ - '  -> to the wall (r 21) in about 34 t; JUMP over it
```

## 12. Implementation sketch (`field.py`)

```python
W_IMPACT0 = ev_or('wave', 'impact', 25)
W_IMPACT = (W_IMPACT0, W_IMPACT0 + 68, W_IMPACT0 + 68 + 83)            # 25, 93, 176
W3_OPEN = 'wave_long' if 'wave_long' in CLIPS else None
W3_CLOSE = 'wave_drop' if 'wave_drop' in CLIPS else None
W_TRI_GAP = 6                                                         # plan 9 (F3)
# 0: front(W_IMPACT0); 68: g.play('wave') + front(25)
# 3rd: if #fgWvK 1 and W3_OPEN: at 176 - ev(W3_OPEN,'impact') play + tri + front(ev(W3_OPEN,'impact'))
#      if #fgWvK 2 and W3_CLOSE: at 176 - ev(W3_CLOSE,'impact') play + tri + front(ev(W3_CLOSE,'impact'))
#      else (stub): play('wave') at 176 - ev('wave','impact'); tri + front(40) at 136
# triple: at 176 + G - 10 and 176 + 2G - 10: if #fq21T 1: front(10) + K.tele_wave(2.5, 21, 2.5, 10, 34)
# set_len at the tri check: max(last strike + 37, clip end)
```

The two branches of the 3rd wave (the opening and the closing) are generated as two timeline variants selected by
`#fgWvK` at 135. `grow` stays as in the stub.

## 13. Checks

- The impacts are at 25, 93, 176, and fronts are made at their charge starts (0, 68, 135 / 136) with tells 25, 25,
  41 / 40.
- A player standing 8 b out is hit at impact + 10 by each front (1.2, Geo, no dash dodge).
- A jump pressed at T−2 clears a front (existing case).
- A triple:
  - fronts strike at 176 + 6 and 176 + 12 (recommended);
  - a jump pressed at T−3 clears all three;
  - 5 hits for a standing player.
- The closing variant plays `wave_drop`, the opening `wave_long`.
- The pattern ends after the last front has expired (no front stops growing mid-arena).
