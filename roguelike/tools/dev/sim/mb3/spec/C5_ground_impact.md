# C5 중력 시스템·지면 충격 (중력 폭발): implementation spec

| field | value |
|---|---|
| pattern | id 5, key `burst`, state cruise, kind normal, owner `cruise.py` |
| clip | `coreup`, 130 t: spark 0, eye 1, **rim 3**, lift 5, up 16, beam 29, column 41, **blast 48**, sink 81 |
| length | 130 (`max_len=138`); `g.release()` at 49 (the bar hides while it settles); recover 20 |
| element | Geo (5) |
| coefficient | 2.2 (`DMG['c5']` 220, raw 29), one hit; KB heavy 4 |
| bands | melee ×2, mid ×1 |

## 1. Footage and plan check

Source: v4 G, 1.55-10.22 s (`understand/v4.md` §3 G), caption **중력 폭발 / 광범위 중력 공격을 날린다 / 범위 내에서도 점프 및
대시 무적으로 회피가 가능하다** ("even inside the area it can be dodged by a jump or the dash i-frames"). P0 = the
first spark.

| event | footage P+ t | rig `coreup` | verdict |
|---|---|---|---|
| pre-onset whoosh (rising 300 → 900 Hz) | −5..−3 | — | sound optional (§9) |
| gold spark at the top of the core arch | 0 | `spark` 0 | ok |
| the core turns its eye outward | 1-4 | `eye` 1 | ok |
| outer rim faintly drawn at the final radius | ≈ 3 | `rim` 3 | ok |
| "번쩍": a gold flame burst round the core as it lifts | 5-6 | `lift` 5 (core to +2.8 b by 15) | ok |
| dark disc under the device, r ≈ 0.5 D | 6-7 | — | fx `dark_disc` from 7 |
| core-up posture: three eyes in a row, each topped by a vertical spike | 15-29 | `up` 16 | ok |
| dark fill grows 0.06 D/t (linear 7-25), reaches R by 33 | 7-33 | — | fx (grow 26 t) |
| upward gold beam, arcs | 29-40 | `beam` 29 | ok |
| rim flares bright (last warning) | 36-41 | — | fx `rim_flare` at 36 |
| core drops back; gold column down to the floor centre | 40-44 | `column` 41 | ok |
| column hits the floor: shard burst | 43.7 | — | fx `floor_hit` at 44 |
| full-area blast, white-gold, jagged crack ring | **48** | `blast` 48 | ok |
| rocks fly up, hover 0.1-0.8 D, crack ring at the rim glows | 49-77 | — | fx `rocks` |
| return to compact (roll 10-20°) | 81-130 | `sink` 81, cruise at 128 | ok |

- **Radius.** R = 1.7 D = 12 b (D 7.0, model.md). The plan says "R = 1.7 D (about 12 b; clamp inside the arena)". The
  stub (and contract §14) centre a disc of r 12 on the body without a clamp. See F1.
- **Height.** The footage hits "the whole disc at once", and the caption allows a jump. The plan's low band: y1 0.5 b
  (a vanilla jump's feet are above 0.5 b on t2..t9).

Plan disagreements and fixes:
- **F1 — "clamp inside the arena".** The body is clamped to r ≤ 16.5, so a disc r 12 can reach 7.5 b past the wall
  (r 21). Those cards are inside the solid wall blocks, so nothing shows and nothing is hit there. The floor beyond the
  far edge always stays open: at least the crescent from r 16.5 − 12 = 4.5 on the far side to the wall. **Recommended:
  keep R 12, unclamped** (no gameplay effect). Do not glide to the centre first: v4 casts it over the centre, but the
  cruise device can be anywhere, and a glide would delay the 3 t rim read.

## 2. AI

- **Bands:** melee ×2, mid ×1. It punishes a player who stays close; a far player is already safe (≥ 12.3 b).
- **Facing:** none needed (radial). Hold the yaw.
- **Aim:** none. The disc is centred on the body.

## 3. Body travel

None.

## 4. Per-tick timeline

`core` = body + the manifest `core` anchor of the event (4.5 at 0-5, 7.76 at 16-41, 5.59 at 48).

| t | rig | mechanics | fx (kit) | sound |
|---|---|---|---|---|
| 0 | core plays `coreup`: spark | | `K.fx('core_spark')` at the core (`~ ~4.5 ~`) | `K.snd('core_spark')` |
| 1 | `eye` (eye out, 1-4) | | | `K.snd('core_flip')` |
| **3** | `rim` | **hazard: disc r 12, tell 45** (§5) | `K.tele_disc(12.0, 45)` at the floor under the body | `block.respawn_anchor.set_spawn` 0.6/0.6 (the marker read) |
| 5 | `lift` ("번쩍", core rising to +2.8 b by 15) | | `K.fx('core_lift')` at the core | `K.snd('core_lift')` |
| 7 | | | `K.fx('dark_disc', r0=3.5, r=12.0, grow=26, life=42)` at the floor (3.5 → 12 by 33, held to 49) | `block.beacon.power_select` 0.6/0.6 |
| 16 | `up` (three spikes up) | | | `block.crafter.craft` 0.6/1.0 |
| 29 | `beam` (the up-beam, 29-40) | | `K.fx('up_beam')` at the core (`~ ~7.76 ~`) | `K.snd('up_beam')` |
| 36 | | | `K.fx('rim_flare', r=12.0)` at the floor centre | `block.amethyst_block.resonate` 0.7/0.6 |
| 41 | `column` (core drops back, the column down to the floor) | | `K.fx('column_down', h=7.8)` at the floor centre | `K.snd('column_down')` |
| 44 | | | `K.fx('floor_hit')` at the floor centre | `block.amethyst_cluster.break` 0.7/0.7, `entity.generic.explode` 0.4/1.3 |
| **48** | `blast` | **the blast strikes** (vis 51, `#hzEv 1`) | `K.fx('blast', r=12.0)`, `K.fx('rocks')` at the floor centre | `K.snd('blast')` |
| 49 | | `g.release()` (harmless tail: the bar hides) | | |
| 54, 64 | | | | `K.snd('rocks_hover')` |
| 77 | | | | `K.snd('debris_land')` |
| 81 | `sink` (settle back, roll 10-20°) | | | `block.piston.contract` 0.6/0.9 |
| 100 | | | | `block.crafter.craft` 0.5/1.0, `block.chain.place` 0.5/1.0 |
| 130 | → `idle_cruise` (cruise form at 128) | `g.end()` | | |

## 5. Damage area

```
# at 3, as the body
*g.hz_opts(kb=KB['heavy'], y1=0.5, vis=51, quiet=1, sfx=0),
g.hz_disc(12.0, C5_BLAST - C5_RIM, DMG['c5']),             # tell 45 = ev('coreup','blast') - ev('coreup','rim')
'positioned ~ 201 ~ rotated ~ 0 run ' + K.tele_disc(12.0, 45)
```

- **Shape:** disc r 12 (padded 12.3) on the body, height **−0.5..0.5 b** (a jump clears it), act 1, KB heavy 4
  (1.0 b, away from the axis), Geo, 2.2. One hit.
- **Dash i-frames work** (default; the caption says so). No `nododge`.

## 6. Telegraphs

45 t from the rim to the blast:
- the Geo rim + progress fill (the kit `tele_disc` reaches the rim exactly at 48);
- the darker floor disc growing 3.5 → 12 (7-33, the footage's marker);
- the core lift "번쩍" at 5, the PDF's "코어가 위로 올라가면 재빨리 피하자" (move away fast when the core goes up);
- the rim flare at 36;
- the column at 41 (the 7 t final cue).

The kit draws `tele_disc` r 12 with 2 telegraph cards.

## 7. Projectiles

None. The rocks after the blast are fx (`p/rocks`: 12 cards spread over r 2-11, hover, drift down).

## 8. FX detail

`core_spark` (3), `core_lift` (6), `dark_disc` (1), `up_beam` (4), `rim_flare` (2), `column_down` (2), `floor_hit`
(10), `blast` (4), `rocks` (12). Peak about 27 fx cards (kit budget).

## 9. Sound

From v4 §6: dense crackle on the spark, a bright flare on the lift, a rising crackle with the up-beam, a zap for the
column, a big broadband boom, debris crackle and a low rumble, clockwork on the return.

| tick | sound |
|---|---|
| 0 | `snd/core_spark` |
| 1 | `snd/core_flip` |
| 3 | `block.respawn_anchor.set_spawn` 0.6/0.6 |
| 5 | `snd/core_lift` |
| 7 | `block.beacon.power_select` 0.6/0.6 |
| 16 | `block.crafter.craft` 0.6/1.0 |
| 29 | `snd/up_beam` |
| 36 | `block.amethyst_block.resonate` 0.7/0.6 |
| 41 | `snd/column_down` |
| 44 | `block.amethyst_cluster.break` 0.7/0.7 + `entity.generic.explode` 0.4/1.3 |
| 48 | `snd/blast` |
| 54, 64 | `snd/rocks_hover` |
| 77 | `snd/debris_land` |
| 81 | `block.piston.contract` 0.6/0.9 |
| 100 | `block.crafter.craft` 0.5/1.0 + `block.chain.place` 0.5/1.0 |

The pre-onset whoosh of the footage (P −5) cannot play before the pattern starts. The spark sound covers it.

## 10. Dodge windows

- **Leave the disc** (12.3 b from the body by 48; the rim shows at 3, 45 t):
  - from 4 b (the melee band edge): 8.3 b. Walk 38 t ✓, sprint 30 t ✓, half-speed swinging 75 t ✗ (stop attacking, or
    dash once: it cancels the swing);
  - from 1 b (under the device): 11.3 b. Walk 51 t ✗, sprint 40 t ✓, walk + one dash 41 t ✓.
- **Jump at the blast** (vanilla, feet > 0.5 b on press +2..+9): press at **39-46** (8 t window). A swinging player
  cannot jump: stop the combo at least the swing length before.
- **Dash i-frames at the blast:** press at **43-48**.
- Nothing here ignores the dash i-frames.

Worst case: 2.2 (one hit). With D 7 the real menace is the melee band: the device rewards a player who reads the lift
and either leaves, jumps or dashes.

## 11. Diagram

```
                 . - ' ' ' ' - .           rim R 12 from t3 (tell 45)
             . '    dark fill    ' .        fill 3.5 -> 12 over 7..33
           .     (grows 0.32 b/t)    .      rim flare 36, column 41-44
          :            [S]            :     BLAST 48: feet <= 0.5 b, 2.2, KB 4
           '         core +2.8       '      jump 39-46 / dash 43-48 / leave r 12.3
             ' .                 . '
                 ' - . . . . - '
```

## 12. Implementation sketch

The stub is right in mechanics (hazard at `rim` with tell `blast − rim`, y1 0.5, KB heavy). Add the kit timeline and
`g.release()` at `blast + 1`. Read `ev('coreup', …)` for every row (rim, lift, beam, column, blast, sink).

## 13. Checks

- One hazard at `rim` (3): tell 45, r 12, y1 0.5, dmg 220, KB 4, no `nododge`.
- One hit at 48 for a grounded player at 8 b.
- No hit for a player whose feet are 0.8 b up at 48.
- No hit with `dashInvT` ≥ 1 at 48.
- No hit at 12.4 b.
