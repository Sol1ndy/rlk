# C1 중력 시스템·일점 상쇄 (폭격) + slam finisher: implementation spec

| field | value |
|---|---|
| pattern | id 1, key `bomb`, state cruise, kind normal, owner `cruise.py` |
| clips | `bomb_run` (58: turn 0, ports 10, run 12, end 56), then `slam` played by the pattern at 58 (45: column 0, plunge 13, impact 16, rise 23) |
| length | 58 + 45 = **103** (`length=103`, `max_len=110`); recover 20 |
| element | Geo (5), every hit |
| coefficients | bomb 0.8 (`DMG['c1']` 80, raw 10), one hit per volley group of 4; slam 1.4 (`DMG['c1s']` 140, raw 18) |
| hits | at most 5 bomb groups + 1 slam; in practice ≤ 2 bombs + 1 slam = **3.0** |
| bands | mid ×1, far ×2 (core bag) |

Ticks are the pattern clock `#fgPT` = the clip tick of `bomb_run`; 58+ continue on the same clock while `slam` plays
(slam tick = t − 58). Every event tick is read with `ev()` / `ev_or()`; the numbers here are the rig manifest of
`wip/fg-rig` 0f7c0e8 (`tools/mboss_fieldgen_rig_manifest.json`).

## 1. Footage and plan check

Source: v1 A, 5.75-10.60 s, real time (`understand/v1.md` §3 A). A0 = the turn (t115 of v1). I re-checked
`sheet_slam_key_crop_8.40-9.80.jpg`: while the column is up the device is still drifting across the screen after the
running player, and it plunges 2-3 b behind her.

| event | footage A+ t | plan / rig | verdict |
|---|---|---|---|
| turn to the player, nose down 15-20° | 0-10 | `turn` 0 (nose down 18°, temporary charge look) | ok |
| underside ports light up | 10-12 | `ports` 10 | ok |
| first bomb leaves a port | 12.3 | `run` 12 | ok |
| first impact (fall 5-6 t from about 4.5 m) | 17.5 | drop 12 + fall 6 = 18 | ok |
| bomb stream, 8-12 per second, 20-25 bombs, 6-8 in the air | 12-57 | 20 bombs, one every 2.25 t, 12-54 | ok |
| straight flight over the player at 0.5-0.6 b/t | 13-57 | glide 12-57, ≤ 0.55 b/t, locked line | ok |
| drifting after the running player, still bombing | 33-57 | — | **finisher re-lock** (below) |
| slam column from the face-down core | 54-67 (13 t) | `slam` played at 58: column 58-71 | +4 t: keep (the rig levels out 56-58 into the slam pose) |
| plunge | 67-70 | `plunge` 71-74 | +4 t, ok |
| impact r ≈ 5, gold shard burst, dust ring | 70.5 | `impact` 74 | ok |
| sits low, then rises (about 4 b in 1 s) | 71-97 | sit 74-81, `rise` 81-102 | ok |
| total | 97 | 103 | ok |

Plan disagreements and fixes:
- **F1 — finisher placement.** The stub slams wherever the 24.75 b route ends: usually 10-15 b past the player, so
  the 1.4 hit never threatens. The footage drifts after the player during the column and lands 2-5 m from her.
  **Fix:** at 58, lock the player's feet (`lockb`), and glide the body up to **6 b** toward that point over 10 t
  (58-67). The slam disc sits at that destination from 58 (tell 16).
- **F2 — end tick.** The stub ends at `C1_SLAM_HIT + 25`: 100 with the stub rig (75 + 25), 99 with the real rig
  (74 + 25). The `slam` clip runs to 58 + 45 = 103, so ending early lets the next pattern's clip cut the rise.
  **Fix:** end at `C1_SLAM + clip_len('slam')`.
- **F3 — port offsets.** The rig has 8 ports on a ring of r 2.74 (`port_0..7`). The footage drops bombs "left /
  right / centre" in a 3-4 m strip. Use the lateral offsets of the inner ports (x ±1.05: `port_0/3/4/7`) and the
  axis: **+1.05 (left), −1.05 (right), 0 (centre)**, cycling L, R, C. The stub's ±1.2 is close; use ±1.05 so the
  bombs visibly leave the front ports.

## 2. AI

- **Bands:** mid ×1, far ×2 (the run is its own approach). Not picked in the melee band.
- **Facing:**
  - 0-9: `face/track` (≤ 4°/t: the idle already faces the player within about 20°).
  - 10: snap the anchor to the route yaw: `execute as @s at @s facing entity <route end E> feet run tp @s ~ ~ ~ ~ 0`
    (the rig follows the anchor with `teleport_duration` 1, so a 10-30° snap reads as a quick turn).
  - 10-57: hold (no tracking during the run).
  - 58-67: hold; the finisher glide may run sideways to the nose. That is fine: the slam pose is symmetric.
- **Aim lock 1 (t0): the route.** The line from the body through the player's feet, yaw ψ0.
  - E = body + 24.75 b along ψ0 (45 t × 0.55 b/t), pulled back along the line in 0.5 b steps until inside r 16.5
    (stub `route` / `pull`).
  - The predictor marker P starts at the body with yaw ψ0 and glides the same route 4 t ahead of the body.
- **Aim lock 2 (t58): the finisher.** `g.lockb()` + `g.keep('rlk_mb_fg_p1f')`. The destination Dst is on the segment
  from the body to that lock, at `min(6, |lock − body|)` from the body, then `g.clamp_body()`.

## 3. Body travel

| ticks | travel |
|---|---|
| 0-11 | none |
| 8-53 | predictor P: `execute as P positioned as E run function rlk:mboss/mv/glide {t:45}` at 8 (arrives at 53) |
| 12-57 | body: `execute positioned as E run function rlk:mboss/mv/glide {t:45}` at 12; speed = \|E − S\| / 45 ≤ 0.55 b/t |
| 58-67 | body: `execute positioned as <Dst marker> run function rlk:mboss/mv/glide {t:10}` (≤ 0.6 b/t) |
| 68-103 | none: the clip plunges and rises in place |

P and the body move on the same line at the same speed, so P at tick t equals the body at t + 4. A bomb's decal made
at P 4 t before its drop is exactly under the port it falls from.

## 4. Per-tick timeline

`ring` = body + 4.5 (cruise ring centre), `floor` = `positioned ~ 201 ~`. Kit calls (`K.*`) need the kit merged
(`fg_fx_api.md`); until then keep the stub's vanilla lines.

| t | rig | mechanics | fx (kit) | sound |
|---|---|---|---|---|
| 0 | core plays `bomb_run` (turn, nose down, temporary charge look) | route lock (`p/bomb/route`), P summoned at the body; `face/track` 0-9 | — | `entity.breeze.whirl` 0.5/0.9 (turn) |
| 8, 10, 12, 14 | | bomb decals 1-4 (group 1), see §5 | `K.tele_disc(1.3, 10)` at each | — |
| 8 | | P starts its glide (45 t) | | |
| 10 | `ports` | face the route (tp facing E) | `K.fx('ports_glow')` at `ring`, rotated as the body | `K.snd('bomb_port')` |
| 12 | `run` | body glide 45 t to E | | `entity.breeze.charge` 0.6/0.6 |
| drops 12, 14, 16, 18, 21, 23, 25, 27, 30, 32, 34, 36, 39, 41, 43, 45, 48, 50, 52, 54 | | — | `K.fx('bomb_drop', h=3.8)` at the bomb's floor point (body + lateral offset, rotated as P) | `K.snd('bomb_drop')`; `K.snd('bomb_fall')` on the first drop of each group (12, 21, 30, 39, 48) |
| decals = drop − 4 | | `hz/disc` r 1.3, tell 10 (strike = drop + 6) | kit decal (§6) | — |
| strikes 18 … 60 (drop + 6) | | the bomb's hazard strikes (vis 11, `#hzEv 1`) | `K.fx('bomb_burst')` at the hazard | `K.snd('bomb_burst')` on even bombs only |
| 56 | `end` (levels out) | | | |
| **58** | **pattern plays `slam`** (column 0: core face down, gold column grows to the floor by 71) | finisher lock + Dst; slam hazard r 5, tell 16 at Dst; body glide 10 t | `K.tele_disc(5.0, 16)` at Dst | `K.snd('column_tell')` |
| 61 | | | `K.fx('column_tell', h=4.5)` at Dst (its base flare fires at +9 = 70) | |
| 64 | | | | `block.beacon.power_select` 0.5/1.2 (rising) |
| 71 | slam `plunge` (4.5 → 2.3 b, stack compressed) | | `K.fx('plunge')` at the ring centre (body + 4.5) | `K.snd('plunge')` |
| **74** | slam `impact` | **slam strikes** (vis 12) | `K.fx('slam')` at the hazard; `K.fx('dust_puff')` | `K.snd('slam')` |
| 81 | slam `rise` | | `K.fx('rise')` at the floor under the body | `block.piston.contract` 0.6/0.8, `entity.breeze.wind_burst` 0.4/0.9 |
| 103 | (clip ends → `idle_cruise`) | `g.end()` | | |

## 5. Damage areas

### Bombs (20; 5 volley groups of 4)

For bomb k (k = 0..19): drop d_k = 12 + ⌊9k/4⌋, lateral offset x_k = (+1.05, −1.05, 0)[k mod 3].

```
# at d_k - 4, as the body (one line block per bomb; GRP_NEW before k = 0, 4, 8, 12, 16)
g.GRP_NEW                                                     # only when k % 4 == 0
*g.hz_opts(kb=KB['light'], grp=True, vis=11, quiet=1, sfx=0)
execute at P rotated as P positioned ^{x_k} ^ ^ positioned ~ 201 ~ run <g.hz_disc(1.3, 10, DMG['c1'])>
execute at P rotated as P positioned ^{x_k} ^ ^ positioned ~ 201 ~ rotated ~ 0 run <K.tele_disc(1.3, 10)>
```

- **Shape:** disc r 1.3 (padded 1.6), height −0.5..3.5 (not jumpable), act 1, KB light 2 (0.3 b), Geo.
- **Groups** (FW-4 check: every member exists before the group's first strike):

| group | bombs | decals | first strike |
|---|---|---|---|
| 1 | 0-3 | 8, 10, 12, 14 | 18 |
| 2 | 4-7 | 17, 19, 21, 23 | 27 |
| 3 | 8-11 | 26, 28, 30, 32 | 36 |
| 4 | 12-15 | 35, 37, 39, 41 | 45 |
| 5 | 16-19 | 44, 46, 48, 50 | 54 |

- A player standing on the line is within 1.6 b of about 2 bombs (spacing 1.24 b along the line, offsets ±1.05),
  which usually fall in one or two neighbouring groups: **≤ 2 hits (1.6)** in practice.

### Finisher slam

```
# at 58, as the body
g.lockb(), *g.keep('rlk_mb_fg_p1f'),
function rlk:mboss/fieldgen/p/bomb/dst          # summons rlk_mb_fg_p1d at min(6, d) toward p1f, clamp_body
*g.hz_opts(kb=KB['heavy'], y1=2.0, vis=12, quiet=1, sfx=0)
execute at <p1d> positioned ~ 201 ~ run <g.hz_disc(5.0, ev('slam','impact'), DMG['c1s'])>     # tell 16
execute at <p1d> positioned ~ 201 ~ rotated ~ 0 run <K.tele_disc(5.0, 16)>
execute positioned as <p1d> run function rlk:mboss/mv/glide {t:10}
```

- **Shape:** disc r 5.0 (padded 5.3) centred on Dst, height −0.5..2.0 (a vanilla jump does not clear it), act 1,
  KB heavy 4 (1.0 b), Geo, 1.4. One hit.
- `p/bomb/dst` (as the body, at it, facing p1f): summon `rlk_mb_fg_p1d` (+ `rlk_mb_fg_pat`) at `^ ^ ^<min(6, dist)>`
  (`function rlk:mboss/mv/dist` → `#mbDist` tenths; cap at 60 → `execute store … run …` a macro step), then
  `g.clamp_body()` on it. Kill an older `rlk_mb_fg_p1d` first (S1 lesson).

## 6. Telegraphs

- **Long read:** the turn and nose-down (0-10), the bomb ports lighting (10).
- **Bombs:** every bomb has a Geo `tele_disc` r 1.3 exactly 10 t before its burst (fill reaches the rim on the strike
  tick). At most 8 bomb decals live at once (4 groups overlap by ≤ 2): 16 telegraph cards (kit budget table: C1 16).
- **Slam:** a Geo `tele_disc` r 5 at Dst from 58 (16 t) plus the rig's gold column from the face-down core and the
  kit column card at Dst (61-76). The column reaches the floor at 71 (the rig), the plunge starts there.
- No lane decal over the whole strip (adapt.md suggested one): the per-bomb decals already show the strip, and a
  24 b lane would cost 5 telegraph cards for 45 t.

## 7. Projectiles

None. The bombs are kit cards (`p/bomb_drop`: the painted bomb + a gold streak falling `h` b in 5 t, life 6). The
hazard, not the card, deals the damage. The rig's `prop/bomb` (a 3-D bomb) is the alternative look: summon it at the
port point, `tp` it to the floor with `teleport_duration` 5, kill it at drop + 6. It costs one entity per bomb (up to
3 live); the card costs nothing per tick. **Recommended: the kit card.**

## 8. FX detail

- Ports: `p/ports_glow` (8 port glows) at the ring centre, rotated as the body, at 10.
- Bomb fall: `p/bomb_drop {h:3.8}` at the floor point; port height in the nose-down pose is 3.1-4.7 b (`port_0`
  3.1 front, `port_4` 4.67 back at `ports`), 3.8 is the axis underside.
- Burst: `p/bomb_burst` (gold spiky burst, scorch, dust) from the hazard's `vis` on `#hzEv 1`.
- Slam: `p/column_tell {h:4.5}`, `p/plunge`, `p/slam` (18 cards: the shard burst, shock ring, dust), `p/dust_puff`,
  `p/rise`. Peak fx cards about 32 at 74 (kit budget table).

## 9. Sound

From v1 §6: continuous thumps during the run, short crack + crystal per impact, a rising hum on the column, a heavy
boom at the slam. All are kit recipes except the two vanilla accents in §4.

| tick | sound |
|---|---|
| 0 | `entity.breeze.whirl` 0.5/0.9 |
| 10 | `snd/bomb_port` |
| 12 | `entity.breeze.charge` 0.6/0.6 |
| each drop | `snd/bomb_drop` |
| first drop of each group | `snd/bomb_fall` |
| every second impact | `snd/bomb_burst` |
| 58 | `snd/column_tell` |
| 64 | `block.beacon.power_select` 0.5/1.2 |
| 71 | `snd/plunge` |
| 74 | `snd/slam` |
| 81 | `block.piston.contract` 0.6/0.8, `entity.breeze.wind_burst` 0.4/0.9 |

## 10. Dodge windows

Player kinematics: README §1.3.
- **Bombs.** The route is visible from 0 (the device turns onto it). The bombs reach a player standing D b along the
  line at about 18 + D/0.55 (D 8: about 33). Leaving the strip means 2.7 b sideways (1.05 + 1.3 + 0.3):
  - walk: 12 t;
  - walk while swinging (half speed): 25 t;
  - sprint: 10 t;
  - dash: 3 t.

  All of these fit, because a mid / far player has at least 20 t. Jumping does not help (the height band is
  0-3.5 b). The dash i-frames cover one bomb (press 0-5 t before its strike).
- **Slam.** The decal r 5 is at Dst from 58, and the strike is at 74 (16 t). From Dst's centre to outside 5.3 b:
  - walk: 3.5 b, not enough;
  - sprint: 4.5 b, not enough;
  - sprint + dash: 3 + 13 × 0.28 = 6.6 b, ok;
  - **dash i-frames at the impact:** press 69-74;
  - vanilla jump: no (the band goes up to 2.0 b; the apex is 1.25).

  A swinging player must dash (the dash cancels the swing at once). From the decal's rim (5 b off), one step out is
  enough.
- No hit of C1 ignores the dash i-frames.
- Worst case standing still: 2 × 0.8 + 1.4 = 3.0.

## 11. Diagram

```
 t0 lock ψ0 (route through the player's feet, end E pulled inside r 16.5)

   S ====P (4 t ahead)=================>=====================> E
        L o     o     o     o     o     ...      bombs every 2.25 t, ±1.05 b
        C    o     o     o     o                 decal r 1.3, 10 t, groups of 4
        R o     o     o     o     o
                       x  player at t0

 t58: lock the player again (lockb) -> Dst = up to 6 b from the body toward it
       E ------glide 10 t-----> Dst      (column 58-71, plunge 71-74)
                          .-'''''''-.
                         (  r 5 slam  )  strike 74, heavy KB, 1.4
                          '-.......-'
```

## 12. Implementation sketch (`cruise.py`)

```python
C1_RUN = ev_or('bomb_run', 'run', 12); C1_PORTS = ev_or('bomb_run', 'ports', 10)
C1_GLIDE, C1_FALL, C1_LEAD = 45, 6, 4
C1_BOMBS = [C1_RUN + (9 * k) // 4 for k in range(20)]
C1_SIDE = (1.05, -1.05, 0.0)                       # L, R, C (body frame ^x = left)
C1_SLAM = clip_len('bomb_run')                      # 58
C1_SLAM_HIT = C1_SLAM + ev_or('slam', 'impact', 16) # 74
C1_END = C1_SLAM + clip_len('slam')                 # 103
Pattern(1, 'bomb', '중력 시스템·일점 상쇄', 'c', 'bomb_run', bands=('mid', 'far'), weight={'far': 2},
        max_len=C1_END + 7, length=C1_END)
# tl.at(0, 'route' (stub), face/track 0..9)
# tl.at(C1_RUN - C1_LEAD, P glide); tl.at(C1_PORTS, tp facing E, K.fx('ports_glow'), K.snd('bomb_port'))
# for k, d in enumerate(C1_BOMBS): decal + hz at d - 4; kit drop at d (rotated as P)
# tl.at(C1_SLAM, g.play('slam'), lockb, keep('rlk_mb_fg_p1f'), dst, hz r 5 tell C1_SLAM_HIT - C1_SLAM, glide {t:10})
# tl.at(C1_END, kill p1p / p1e / p1d, g.end())
# vis: 11 -> K.fx('bomb_burst') (+ snd on even), 12 -> K.fx('slam'), K.snd('slam')
# cancel: kill @e[tag=rlk_mb_fg_p1]  (route markers, Dst; kept p1f is killed by the core)
```

Every marker gets `rlk_mb_fg_pat` + `rlk_mb_fg_p1`. Each marker tag is killed before its summon (the S1 lesson).
`p/finish` also kills them.

## 13. Checks (test_fieldgen.py §9 or a new pat_cruise.py)

- 20 bomb hazards: tell 10, r 1.3, dmg 80; 5 groups of 4. Every group's members are made before its first strike.
  A standing player on the line takes ≤ 1 hit per group.
- The slam hazard is made at 58: tell = `ev('slam','impact')` (16), r 5, y1 2.0, dmg 140, KB 4, at Dst. Dst is at most
  6 b from the body at 58 and inside r 16.5.
- A player standing still at their 58 spot, within 6 b of the route end, is hit at 74. One 6 b away sideways is not.
- The route end and the body stay inside r 16.5 for a player 12 b away (existing case).
- The pattern ends at 103. A second run aims at the new spot (kept markers).
