# Requests and notes from AP-REV (T1, the Heart, the revival stage, the failure strike, the CS, the organisms and walls — `tools/mboss_apep/revival.py`, `org.py`, branch `wip/ap-rev`)

Protocol: `S:ap/ap_contract.md` §0.11 (append-only, `## R<stage>-<n> <type>: <title>`, what / why / needed by, status).
AP-REV wrote only `revival.py` / `org.py` (+ their generated `AP:{rev,heart,org,wall}/**`, `AP:p/{t1,fail,cs}/**`); everything
below is for the owners of the core, the api, the harness, the kit or the plan (I2 integrates). Suite: `S:ap/tests/pat_rev.py
<dp>` (exports `TABLE`); harness helper `S:ap/tests/revsim.py`; storyboards `S:ap/renders/ap-rev_{t1,stage,walls,cs}.jpg`.

## RREV-1 request (core): tick the Heart's clips outside the stage; one owner for the org object ticks

- what: run `AP:heart/tick` (AP-REV's wrapper of `om/heart/tick`, a no-op without the Heart) once per tick in the intro
  tick (E) and the phase-1 module tick, or the shared `om/objects_tick` for every object (RORG-3). Then switch
  `heart/p1_up` from its fallback (one 30 t client interpolation per display to the canopy pose of
  `om/heart/spawn/canopy`, marked in the file) to `om/heart/play/heart_up`, so the canopy `heart_hang` sway plays too.
- why: nothing ticks the org objects in E / phase 1 on `wip/ap` d15e500; AP-REV ticks the Heart itself only while it owns
  the stage (T1 `p/t1/tick`, phase 2 `rev/tick`, the failure `p/fail/tick`, the CS `p/cs/tick`) and the walls in
  `rev/tick` (`wall/tick` -> `om/wall/tick`). If the core adds `om/objects_tick` everywhere (RP1-2, RP3-4), remove those
  calls with it (else the Heart / wall clips step twice per tick).
- needed by: AP-I2. status: open.

## RREV-2 request (harness): fold `revsim.py` into `lib/apsim.py`

- what: the org runtime needs from the sim: `ride` / `execute on passengers|vehicle` (passengers follow a tp of their
  vehicle, survive a killed vehicle dismounted), `rotate`, `data merge entity` into `Ent.data`, `data modify entity ...
  item.components."minecraft:item_model"`, `execute if|unless data entity <t> <compound>`, summons keeping their NBT,
  `execute align`, `execute facing <x> <y> <z>`, the sorts `random` / `furthest`, and `rlk:char/particles` as a no-op.
  `S:ap/tests/revsim.py` patches them into `apsim.ApSim` (ported from `S:ap/orgtests/test_ap_org.py`).
- why: without them `test_apep.py` / `test_e2e_apep.py` stop with `NotImplementedError: on` at the first organism.
  Until I2: `python3 pat_rev.py <dp> --core [sections]` and `--e2e` run those suites with the patch.
- needed by: AP-I2 (run_all.sh). status: open.

## RREV-3 request (tests): stub-era expectations in `test_apep.py` to update

- what (each now covered with the real timing in `pat_rev.py`):
  - intro 3c / 3d and reload 15a / 15b look for the stub's `rlk_mb_ap_heartd` prop at y + 9 / y + 20: the real Heart is the
    AP-ORG object (bulb display UUID `…4800-8000-000000000000`, tag `rlk_mb_ap_heart_bulb`, at the floor point; its
    translation y 10.12 in the entrance state, 21.12 in the canopy; the marker `rlk_mb_ap_heart` at the centre);
  - stage 7c-7g expect organisms 1-3 ticks after a wave is due / test 29: every spawn now shows its 20 t spawn marker and
    a 10 t emergence (untargetable, plan 7.6.3), and the wave check runs every 8 t (the first wave at once). `kill_orgs`
    must wait until they are solid (`rlk_mb_inv` gone); the time-out 파괴 is a pending marker (`rlk_mb_ap_ospawn`, apK 5)
    first (pat_rev 2a-2e, 4f-4m);
  - reload 15c / 15d count the organisms 5 t after the reload: the wave is marked again and emerges 20 t later (pat_rev
    14a / 14b);
  - `mod_ents` misses the real model / object tags (`rlk_ap_om`, `rlk_mb_ap_heart_bulb`, `rlk_mb_ap_wallb`, …).
- measured on `wip/ap-rev` with `pat_rev.py <dp> --core`: 13 of the core checks fail, all of these (3c 3d 7c 7d 7e x3 7f 7g
  15a 15b 15c 15d); every other section passes (build intro res t1 stage orgs fail cs tests pause reload death abort
  uninstall px budget: P2 with 6 organisms 741 commands / t). `pat_rev.py <dp> --e2e`: all `test_e2e_apep` checks pass.
- needed by: AP-I2. status: open.

## RREV-4 request (core): uninstall removes the org models and objects

- what: in `uninstall` kill `@e[tag=rlk_ap_om]` (every AP-ORG display: organism models, the Heart, domes, stalks, the seed,
  wall blades) or call `org/clear` + `rev/clear` + `om/kill_all`.
- why: `MODULE_TAGS` holds the markers only; killing the organism husks leaves their model passengers dismounted, and the
  Heart displays carry `rlk_ap_om` + `rlk_mb_ap_heart_<display>`, not `rlk_mb_ap_heart`. `cleanup` is fine (it calls
  `org/clear` and `rev/clear`). AP-REV's own markers carry `rlk_mb_ap_om` (in `MODULE_TAGS`).
- needed by: AP-I2. status: open.

## RREV-5 request (core, perf): skip the body push request and the proxy polling while parked (phase 2)

- what: `push/req` (21 commands per tick) runs every tick in phase 2 although the parked body never pushes; the framework
  proxy poll / follow of the parked body costs ~44 more.
- why: the plan 7.6.4 budget is <= 800 commands per tick on average at the cap; measured in the sim (pat_rev 16a, 5
  organisms incl. a chaining 포식성 and a 양육 with 3 tethers, the player Dendro-afflicted): 784 average (max 1436); with 수호
  + 둥지 + walls 703. AP-REV already dispatches the organisms by kind, draws the tethers every 8 t (the dust lives 7-36 t)
  and checks the waves every 8 t. The margin is thin.
- needed by: AP-FIX (perf). status: open.

## RREV-6 request (kit, = RI1-1): the O1 impact preset

- what: a small impact preset for the basic's melee cone (O1) at the strike tick.
- why: the 10-20 rule removed O1's decal; `org/basic/m_hit` shows vanilla `composter` + `crit` particles 1.6 b ahead
  meanwhile (marked `TODO(I2) RI1-1`).
- needed by: AP-I2. status: open.

## RREV-7 plan: decisions inside the plan's latitude (for the I2 change note)

- what (plan 7.5-7.7, 7.6.3-7.6.7, 8.2; no tick, size or coefficient changed):
  1. Spawns: every organism (waves, the time-out, the reload respawn) = the kit spawn marker on its point for 20 t, then
     the husk, untargetable 10 t (emergence). Tests 23-28 (`org/spawn_<kind>`) spawn at once. The wave clock and the
     alive count include pending spawns; the due check runs every 8 t (at once for the stage's first wave). Basics take
     4 distinct r 12 points (random among those >= 4 b from the player); 수호 / 파괴 the point nearest 10 b from the
     player (8-12, else 6-14, else any), 둥지 the nearest, 포식성 the farthest (free points first), 양육 the r 7 point
     nearest one of the wave's basics. The shuffle bag refills when all four are drawn.
  2. Basics: melee walks to the wait ring r 4.5, then asks every 10 t for a slot + the lowest free socket (pushed out to
     r 3.4 round the cradle); the first lean 20 t after reaching the socket, then every 40 t. Ranged stop on reaching
     r 12.6 (their r 12 spawn ring), lie down (10 t), ask for a slot every 10 t, the first bolt 20 t after it. The bolt
     ends at the Heart inside a box = the bulb box's larger side 3.2 b + 2 x 1.5 b square, y ± (1.15 + 1.5) round the
     bulb centre; a hit on the player ends it (`#pjKeep 0`), a dodged bolt flies on to the Heart.
  3. 수호: the first cast when it becomes solid; a pool break passes the rest of the hit to the HP; a basic becoming solid
     within r 10 of a living 수호 is shielded; with two 수호 alive one's death keeps the shields.
  4. 양육: the first cast when solid, re-links every 80 t; the immunity / cylinder follow the link count.
  5. 포식성: no basic to swallow (or its prey killed before the eat tick) = un-empowered (no burst, bites x0.7). Before each
     chain and single bite it dashes to 2 b of the player (1.5 b/t, 2 t) so the 2.6 b sectors can reach; the chain clip
     starts 4 t before bite 1 (its first snap is at clip t4; contract 0.5.5 said 8 t before the first strike); a single
     bite's readable start (the flare + o6_swim + the dash) is 12 t before it, the sector 10 t.
  6. 파괴: to the nearest of the three stops; the blast disc is made at contact with its 61 t tell; after the blast it
     tumbles 2.5 b away from the Heart over 5 t during `org_die`; a 파괴 killed before the blast cancels its hazard.
  7. 둥지 walls: the three groups at the player's facing + 0 / 120 / 240 deg, r 4.2 round the locked feet; blades at
     -20 / 0 / +20 deg of each 60 deg arc, barrier cells every 5 deg along the arc; the 30 % variant one arc at r 3.6
     ahead. A cell is skipped when the player's box + 1 b meets it (volume test for `@e[tag=rlk_body]` and
     `@a[tag=player]`), an organism stands within 1.5 b of its centre, its centre is within 5.31 b of the Heart (4.6 +
     the half diagonal) or beyond r 25. The blocks go at the dissolve start (life 40), the blades 8 t later.
  8. The failure strike after a lose: the service keeps running and restarts the stage at t60 (the Ronova edge); no
     wither strike after the lose. The ⚠ is the kit's failure badge (U+E907).
  9. The Heart: `heart_gain` / `heart_hit` clips only while the stage runs; the CS kills the cradle / arms / sprouts at
     t30 under the white-out and the whole Heart at t92 (the egg fades into the Warden); the stage markers (sockets, 파괴
     stops) are made at T1 t106 / phase-2 ready and removed at the white-out.
- needed by: AP-I2 (plan.md §14 note). status: open.

## RREV-8 note (no-tips rule): what the revival stage shows

- what: neutral info and the real game's texts only: 「오아시스의 심장」 (title), 「마물을 처치해서 소생 진행도를 올리세요」 (T1
  t108; v2 39.6 s, v3), "소생 진행도 NN%", the wave count, the specials' badges, the failure badge; the instant-kill warning
  「소생 실패」 + "다시 한 번 실패하면 쓰러집니다"; the time-out "!" + "오아시스의 심장이 위험합니다" / "파괴의 증식 생명체가
  나타납니다" (neutral information; not in the footage, v4 shows no warning — **unsure**, kept as the I1 notes allow it);
  "오아시스의 심장이 소생했습니다". No first-time hints (the plan's four organism hints are not built); pat_rev 15a / 15b
  scan every text of the owned functions.
- status: informational.

## AP-I2 status (2026-10-21, `wip/ap` f588262; plan §14 "AP-I2 integrate", contract §3)

- RREV-1: done f588262: the core's `AP:obj/tick` (E, phases 1-3, D) steps the Heart / domes / stalks / wall blades; revival's
  `heart/tick` and its calls and org's `om/wall/tick` line dropped; `heart/p1_up` plays `om/heart/play/heart_up`.
- RREV-2: done f588262 (harness, scratch): `revsim.py` folded into `lib/apsim.py`; `revsim.py` is a shim.
- RREV-3: done f588262 (tests, scratch): test_apep 1a 1f 2a 3c 3d 7c-7g 15a-15d 18a, `mod_ents`, `solid()`; test_e2e_apep on the
  shipped route + the lose variant.
- RREV-4: done f588262: `uninstall` kills `@e[tag=rlk_ap_om]`.
- RREV-5: part done f588262: `push/req` skipped in phase 2; the framework proxy poll of the parked body left for AP-FIX.
- RREV-6: done f588262: kit preset `o1_hit` at O1's strike.
- RREV-7: done f588262: plan §14 AP-I2 note, item 5.
- RREV-8: informational; the time-out lines stay, listed as unsure for the user.

## AP-FIX status (2026-10-22)

- RREV-5: the framework's proxy poll of the parked body stays (a framework file; the soak's phase 2 at the cap averages
  709 commands per tick ≤ 800). The module's `hz_vis` hook no longer computes anything (no route).
- RREV-8: the time-out lines stay, listed as unsure for the user.
- api.REV after the balance pass: basic kill +300, special +1300, basic hit −54, buffed −108.
