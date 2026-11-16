# C2 내려찍기 (slam alone): implementation spec

| field | value |
|---|---|
| pattern | id 2, key `slam`, state cruise, kind normal, owner `cruise.py` |
| clip | `slam`, 45 t: column 0, plunge 13, **impact 16**, rise 23 |
| length | 45 (`length=45`, `max_len=52`); recover 20 |
| element | Geo (5) |
| coefficient | 1.4 (`DMG['c2']` 140, raw 18), one hit |
| bands | melee ×2, mid ×1 |

## 1. Footage and plan check

Source: the v1 caption "내려찍기는 단독으로도 사용한다" (the slam is also used alone) and the finisher of v1 A
(8.45-10.60 s). There is no separate footage of the solo slam, so I took its timing from the finisher. I re-checked
`sheet_slam_key_crop_8.40-9.80.jpg`.

| event | footage (finisher) | rig `slam` | verdict |
|---|---|---|---|
| core turns face down, gold column (1-1.2 m wide) to the floor; the column marks the slam point | 13 t | `column` 0-13 (the column reaches the floor at 13) | ok |
| column base flares | +13 | — | fx (kit `column_tell` base flare at +9 after its call) |
| plunge 3.5-4 m in 3-4 t, core first | 13-16 | `plunge` 13, 4.5 → 2.3 b in 3 t | ok |
| impact: gold shard burst + dust ring, r ≈ 5 m | 16.5 | `impact` 16 | ok |
| sits low 7 t | 16-23 | 16-23 | ok |
| rises back (about 4 b in 1 s) while drifting away | 23-43 | `rise` 23-44 | ok |

- The stub uses `ev_or('slam', 'impact', 17)` (the stub rig). With the real rig the impact is **16**: read it with
  `ev()`, and the tell follows (16).
- The plan says "column tell 13 t, plunge, slam r 5". The decal is shown from 0, so the readable warning is 16 t.

## 2. AI

- **Bands:** melee ×2, mid ×1 (the glide covers ≤ 8 b).
- **Facing:** `face/player` at 0 (the nose toward the target), then hold.
- **Aim lock at 0:** `g.lockb()` + `g.keep('rlk_mb_fg_p2a')`: the player's feet, pulled inside the body disc r 16.5.
  The slam lands there.

## 3. Body travel

| ticks | travel |
|---|---|
| 0-9 | `execute positioned as <p2a> run function rlk:mboss/mv/glide {t:10}`: onto the lock (melee band ≤ 0.4 b/t, mid ≤ 0.8 b/t) |
| 10-45 | none (the rig plunges, sits and rises in place) |

The device moves over the point while the column falls. The footage shows the same drift during the finisher's column.

## 4. Per-tick timeline

| t | rig | mechanics | fx (kit) | sound |
|---|---|---|---|---|
| 0 | core plays `slam`: core face down, column grows (temporary charge look) | `face/player`; lock + keep p2a; slam hazard (tell 16); glide 10 t | `K.tele_disc(5.0, 16)` at p2a | `K.snd('column_tell')` |
| 3 | | | `K.fx('column_tell', h=4.5)` at p2a (column card 0.3 → 1.15 wide over 4 t, life 15; base flare at 12) | |
| 8 | | | | `block.beacon.power_select` 0.5/1.2 |
| 13 | `plunge` | | `K.fx('plunge')` at the ring centre (body + 4.5) | `K.snd('plunge')` |
| **16** | `impact` | **strike** (vis 21) | `K.fx('slam')` at the hazard, `K.fx('dust_puff')` | `K.snd('slam')` |
| 23 | `rise` | | `K.fx('rise')` at the floor under the body | `block.piston.contract` 0.6/0.8, `entity.breeze.wind_burst` 0.4/0.9 |
| 45 | → `idle_cruise` | `g.end()` | | |

## 5. Damage area

```
# at 0, as the body
g.lockb(), *g.keep('rlk_mb_fg_p2a'), f'tag {P2A} add rlk_mb_fg_pat',
*g.hz_opts(kb=KB['heavy'], y1=2.0, vis=21, quiet=1, sfx=0),
f'execute at {P2A} run ' + g.hz_disc(5.0, C2_HIT, DMG['c2']),          # C2_HIT = ev('slam', 'impact') = 16
f'execute at {P2A} rotated ~ 0 run ' + K.tele_disc(5.0, C2_HIT),
f'execute positioned as {P2A} run function rlk:mboss/mv/glide {{t:10}}'
```

- **Shape:** disc r 5.0 (padded 5.3) at the lock point, height −0.5..2.0, act 1. KB heavy 4 (1.0 b, away from the
  centre), Geo, 1.4. One hit.

## 6. Telegraphs

- The Geo `tele_disc` r 5 fills from 0 and reaches the rim at 16 (the strike), then flashes.
- The rig's gold column from the face-down core lands on the decal's centre once the glide arrives (10). The kit's
  column card marks the target from 3.
- Tell cue: `snd/column_tell` (a rising hum) at 0.

## 7. Projectiles

None.

## 8. FX detail

The same presets as the C1 finisher: `column_tell`, `plunge`, `slam` (18 cards), `dust_puff`, `rise`.

## 9. Sound

| tick | sound |
|---|---|
| 0 | `snd/column_tell` |
| 8 | `block.beacon.power_select` 0.5/1.2 |
| 13 | `snd/plunge` |
| 16 | `snd/slam` |
| 23 | `block.piston.contract` 0.6/0.8, `entity.breeze.wind_burst` 0.4/0.9 |

## 10. Dodge windows

The decal is at the player's 0-tick spot; the strike is at 16. To leave r 5.3 from the centre of the decal:
- walk 3.5 b, sprint 4.5 b: not enough;
- **sprint + dash** (3 b in 3 t + 13 t of sprint, 6.6 b): ok;
- **dash i-frames at the impact:** press 11-16;
- vanilla jump: no (the band goes up to 2.0 b; the apex is 1.25).

Most C2 picks happen in the melee band, where the player is often swinging: half-speed walking gives 1.8 b. The
answer is the dash: it cancels the swing at once and its i-frames cover the impact when pressed at 11-16. This is
the pattern's lesson: "the column = dash it". It ignores nothing: the dash i-frames work.

Worst case: 1.4.

## 11. Diagram

```
        S --glide 10 t--> X (player's feet at t0, inside r 16.5)

                .-'''''''''-.
              .'  gold col.  '.      decal r 5 (16 t)
             (        X        )     plunge 13-16, strike 16
              '.             .'      heavy KB 1.0 b
                '-.........-'
```

## 12. Implementation sketch

The stub is already right except the clip's impact (read `ev('slam','impact')`) and the kit calls. Keep the kill of
`p2a` at the end. The core also kills kept markers.

## 13. Checks

- One hazard at 0: tell = `ev('slam','impact')`, r 5, y1 2.0, dmg 140, KB 4.
- A player standing at the lock is hit at 16. A player 5.4 b away is not.
- The glide stops inside r 16.5 for a wall-hugging player (existing case).
- A second run, with the player moved, slams at the new spot.
