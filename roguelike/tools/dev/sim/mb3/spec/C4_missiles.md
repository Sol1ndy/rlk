# C4 중력 시스템·바위 폭탄 (미사일 발사): implementation spec

| field | value |
|---|---|
| pattern | id 4, key `missile`, state cruise, kind normal, owner `cruise.py` |
| clip | `missiles`, 64 t: flare 0, vent 8, **launch 22**, last 35 |
| length | 64 (`max_len=72`); recover 20 |
| element | Geo (5) |
| coefficient | 0.9 per missile (`DMG['c4']` 90, raw 11); **2 volley groups** (missiles 1-5, 6-10) |
| hits | ≤ 2 (1.8) |
| bands | **far ×3 only** (≥ 8 b; PDF: used when the player is far) |

## 1. Footage and plan check

Source: v1 M, 25.66-29.30 s, real time (`understand/v1.md` §3 M); M0 = the tip flare.

| event | footage M+ t | rig `missiles` | verdict |
|---|---|---|---|
| tell 1: both spike tips flare (gold 4-point starbursts, arcs over the ring) | 0-8 | `flare` 0 (the spikes tip up 10°) | ok |
| tell 2: the top opens, a vertical gold shaft vents up (≥ 6 m) | 8-21 | `vent` 8 (eye up, gold vent column 6 b) | ok |
| vent flames | 19-39 | — | fx (`missile_launch` per missile) |
| launches, one every ≈ 1.4 t, crossing arcs, white-blue smoke | 25-39 | `launch` 22 … `last` 35 | −3 t, ok |
| apex / turnover out of view (≥ 15-20 m) | 39-46 | module flight | see F1 |
| steep dive in a tight cluster at ≈ 25 m/s | 47-53 | module flight | |
| impacts walk along the player's path (lag 1-2 m), r 1.2-1.5, ≈ 1 per 1.5 t | 53-68 | 50-63 | ok |
| total | 73 | 64 | ok |

Plan disagreements and fixes:
- **F1 — flight time.** The stub flies a missile 20 t (rise 7, lock at +7, dive 13). The footage gives about 28 t
  from a launch to its impact (first 25 → 53, last 39 → 68). **Fix:** rise 14 t (two segments, 7 + 6 t, then 1 t at
  the apex), lock at L + 14, dive 13 t, impact at **L + 28**. The last impact is 35 + 28 = 63 < 64, so it still fits
  in the clip.
- **"Weak homing"** = the late lock: each missile picks the player's feet at its apex (14 t before its impact) and
  dives straight there. No `pj/steer`, so the framework's ±60° pitch clamp never bites. A running player is trailed
  by 1-2 b, as in the footage.

## 2. AI

- **Bands:** far ×3 only.
- **Facing:** `face/track` 0-21, then hold.
- **Aim locks:** per missile at L_i + 14: `g.lockp()` (the walk disc r 20.3, so a wall-hugger is covered). The lock
  marker is killed in the same function after the hazard and the dive teleport are made.

## 3. Body travel

None. The missiles are module props (kit `prop/missile`: nose along local +z, aim with `tp … facing`).

## 4. Per-missile flight

Launch ticks L_i = 22 + ⌊3i/2⌋ (i = 0..9) = 22, 23, 25, 26, 28, 29, 31, 32, 34, 35.
- Even i: `vent_l` (body frame `^2.81 ^5.0 ^-1.16`).
- Odd i: `vent_r` (`^-2.81 ^5.0 ^1.16`).

| missile clock | what |
|---|---|
| L (0) | summon the prop at its vent, pitch −90 (nose up), `teleport_duration:7`, tags `rlk_room rlk_mb_aux rlk_mb_fg_pat rlk_mb_fg_p4 rlk_mb_fg_p4m`; `mbT 0`; `mbS = #mbGrp` |
| 1 | `tp` 7 b straight up (arrives at 8) |
| 8 | apex point A_i: on the line body → player, 0.5 × the distance from the body, offset sideways 3 b to the side opposite its vent, at y 201 + 16. `teleport_duration:6`, `tp` facing A_i (arrives at 14). This gives the crossing arcs. |
| 14 | **lock**: `g.lockp()`; `#hzGrp = @s mbS`; hazard + decal (§5, tell 14); `tp` the prop facing the lock (instant turn) |
| 15 | `teleport_duration:13`, `tp` to the lock + 0.6 b (the dive, about 1.2-1.4 b/t) |
| 28 | impact: the hazard strikes (vis 41) → fx at the hazard; kill the prop |

Smoke: `K.fx('missile_trail')` at each prop every 3 t of its clock (ambient). Locks:

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| launch | 22 | 23 | 25 | 26 | 28 | 29 | 31 | 32 | 34 | 35 |
| lock (decal) | 36 | 37 | 39 | 40 | 42 | 43 | 45 | 46 | 48 | 49 |
| impact | 50 | 51 | 53 | 54 | 56 | 57 | 59 | 60 | 62 | 63 |

Groups (FW-4 check):
- group 1 = i 0-4: last decal 42 < first strike 50;
- group 2 = i 5-9: last decal 49 < first strike 57.

`g.GRP_NEW` runs at launch i = 0 and i = 5. Each missile stores `#mbGrp` in `mbS` and restores it into `#hzGrp` at
its lock, as the stub does.

## 5. Per-tick timeline

| t | rig | mechanics | fx (kit) | sound |
|---|---|---|---|---|
| 0 | core plays `missiles`: slit hot, spikes tip up 10° | `face/track` 0-21 | `K.fx('tip_flare')` at `spike_tip_l` (`^5.33 ^4.55 ^0`) and `spike_tip_r` (`^-5.33 ^4.55 ^0`) | `K.snd('tip_flare')` |
| 4 | | | `K.fx('spark')` at both tips | |
| 8 | `vent` (eye up, gold column up 6 b) | | `K.fx('vent_shaft')` at the hub top (body + 5.2) | `K.snd('missile_vent')` |
| 15 | | | `K.fx('vent_shaft')` again (the shaft pulses) | `block.fire.ambient` 0.6/0.9 |
| 22-35 | `launch` … `last` | missile i launched at L_i (§4); GRP_NEW at 22 and 29 | `K.fx('missile_launch')` at the vent | `K.snd('missile_launch')` per missile |
| 36-49 | | locks (decal + hazard) | `K.tele_disc(1.5, 14)` at the lock | `K.snd('missile_dive')` at 36 and 43 (once per group), at the lock |
| 38 | the vent column off | | | |
| 50-63 | | impacts | `K.fx('missile_impact')` at the hazard | `K.snd('missile_impact')` per impact |
| 64 | → `idle_cruise` | `g.end()` | | `K.snd('debris_land')` at the last impact point |

## 6. Damage areas

```
# p/missile/lock, as the missile at its apex (L + 14)
g.lockp(),
'scoreboard players operation #hzGrp mb = @s mbS',
*g.hz_opts(kb=KB['default'], vis=41, quiet=1, sfx=0),
'execute at @e[type=minecraft:marker,tag=rlk_mb_fg_lock,limit=1] run ' + g.hz_disc(1.5, 14, DMG['c4']),
'execute at @e[type=minecraft:marker,tag=rlk_mb_fg_lock,limit=1] rotated ~ 0 run ' + K.tele_disc(1.5, 14),
'execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_lock,limit=1] feet run tp @s ~ ~ ~ ~ ~',
# L + 15: data merge entity @s {teleport_duration:13}; tp @s <lock> ~ ~0.6 ~  (store the lock in the prop: use a
# per-missile kept marker rlk_mb_fg_p4t<i> made at 14 and killed at 28 instead of killing the lock at 14)
```

- **Shape:** disc r 1.5 (padded 1.8) at the locked feet, height −0.5..3.5 (not jumpable), act 1, KB 3 (0.6 b), Geo,
  0.9.
- **Cap:** one hit per group, so ≤ 2 hits (1.8).
- The dive target must survive to L + 15. Keep it as `rlk_mb_fg_p4t<i>` (summon a fresh marker at the lock with
  `rlk_mb_fg_pat`, after killing an older `p4t<i>`). Kill it at the impact. That keeps markers from piling up (S1).

## 7. Telegraphs

- Pattern tells: the spike-tip flares (0-8) and the vent shaft (8-21). These say "missiles: keep moving" 22 t before
  the first launch.
- Per missile: a Geo `tele_disc` r 1.5 at the locked feet, 14 t before its impact. At most 10 live (20 telegraph
  cards, as the kit budget measured).

## 8. FX detail

`tip_flare` ×2, `spark` ×2, `vent_shaft` ×2, `missile_launch` ×10, `missile_trail` (ambient), `missile_impact` ×10.
The missile look is the kit prop `prop/missile` (1.3 b drill, nose along +z). The rig's `prop/missile` (nose −Y) is
the alternative. The kit's aims with `tp … facing`, so it is simpler. Peak fx cards about 35.

## 9. Sound

From v1 §6: crackle at the flare, a loud roar for the vent (+23 dB), rapid whooshes for the launches, a falling
whistle, crack + boom per impact.

| tick | sound |
|---|---|
| 0 | `snd/tip_flare` |
| 8 | `snd/missile_vent` |
| 15 | `block.fire.ambient` 0.6/0.9 |
| each launch | `snd/missile_launch` |
| 36, 43 | `snd/missile_dive` |
| each impact | `snd/missile_impact` |
| 64 | `snd/debris_land` |

## 10. Dodge windows

Each decal locks the feet 14 t before its impact:
- walking 3.1 b, sprinting 3.9 b, or half-speed 1.5 b (a far-band player is rarely swinging) all clear the padded
  1.8 b if the player keeps moving;
- standing still: ≤ 2 hits (1.8), one per group.

A running player is trailed by the impacts (the footage look). Jumping does not help (band −0.5..3.5). The dash
i-frames work (press 0-5 t before an impact). Nothing ignores them.

## 11. Diagram (side view)

```
            A (apex, y +16, L+8 .. L+14)          lock at L+14: decal r 1.5 (14 t)
          .'  '.
   vent .'      '.   dive 13 t (~1.3 b/t)
  [S]~~^          '.
   7 b up (L..L+8)  '.
                      v
                      o  impact L+28 (0.9, groups 1-5 / 6-10)
```

## 12. Implementation sketch

Replace the stub's `age`:
- clock 1: up 7, `teleport_duration` 7;
- clock 8: to the apex, `teleport_duration` 6;
- clock 14: `lock` (decal + hazard + keep `p4t<i>` + facing);
- clock 15: `teleport_duration` 13 + `tp` to `p4t<i>` + 0.6;
- clock 28: kill.

The apex marker (`rlk_mb_fg_p4a`, temporary) is computed at clock 8 from the body and the player:
`execute at <body> facing entity <player> feet rotated ~ 0 positioned ^<±3> ^16 ^<0.5 × dist>` (dist from
`mv/dist`, via a macro).

## 13. Checks

- 10 hazards at the locks: tell 14, r 1.5, dmg 90, 2 groups. Every member is made before its group's first strike.
- Impacts at L_i + 28 (50 … 63), all inside the 64 t clip.
- A standing player is hit exactly twice (one per group). A player walking at 0.22 b/t is never hit.
- Every prop and `p4t` marker is gone at the end and after a cancel.
