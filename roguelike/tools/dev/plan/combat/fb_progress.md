# Fix lane FB (the enemy side after review B) — progress

Branch `wip/combat-fix-b` (from `origin/wip/combat` 6522feef5), worktree `<scratchpad>/cb/wt_fb`. Work folder `<scratchpad>/cb/fb`
(`sim/` = the copy of `tools/dev/sim` the suites run from, `base/` = `git archive` of 6522feef5, `snap/` = a plain copy of the
worktree for the harness, `out/` = harness logs, `ed/` = the edit scripts of this lane, `runsuites.sh` / `hzall.sh` / `sync.sh` /
`snap.sh`). Spec: `decisions.md`; findings `review/findings_B.json` (+ A-04 of `findings_A.json`); rulings `review/rulings_B.md`.

## What was done (per finding)
- **B-01** `mboss/hz/np_def`: unparriable by default only no-dodge, per-mille, re-arming, full-arena (kind 5) and mask (kind 6)
  hazards; no size thresholds. The modules name their big hits with `L.hz_opts(noparry=1)` (table below).
- **B-02 / B-03 / B-04** the warning glint: `mboss/hz/np_auto` (framework: only for an unparriable hazard that hits, can be
  dodged, is not re-arming and is made >= 12 t before its strike), `mboss/np_glint` (gate `np_gate` + the boss's glint point
  `d/np_at`, generated from the registry field `glint` [up, forward]) and `mboss/np_glint_here` (the module's own rig point);
  `mboss_lib.np_warn()`, `hz_opts(noparry=1, glint=False)` (= `#hzNoParry 2`), `glint_of`, `NP_LEAD` / `NP_LEAD_BIG`. Modules
  call it at the tell tick. No glint for no-dodge mechanics and lingering fields (Raiden: none of her hazards flashes any
  more, B-11).
- **B-10 + A-04** `mboss/grp_hit` (hz/hurt, pj/hit, hz/hurt_pm_dodge): a landed hit, a tier-1/2 parry, a perfect parry and a
  perfect dodge consume the volley group; burst / revive i-frames do not.
- **B-06** `cm/ar/shoot` (hand file): the arrow gets the line's `cmId`. **B-07** `tools/ch2mob/elite.py`: `cm/cc/flock` sends
  no cicin while the caster's `grgT` runs; `cm/ci/r_hit` -> `r_hit_own` for an owned cicin (the hit is made with the
  caster's id, so `player/def/ctx_cm` finds her; the own id is put back).
- **B-08** `boss/tachy/core/ground` + `bal_on`. **B-09** `bal/boss/may` (tools/build_balance.py): no pips for a registry
  body with `rlk_mb_inv`.
- **Q5b** the nine cuts are parryable by the new default (disc 5.5, two cuts to a volley group: five answers 6 t apart); the
  finisher is per mille = unparriable by the rule, glint with the aura 20 t before. No hazard changed: a passive player
  takes what she took before.
- **B-12** README: section 3 (rule, table, glint, groups, balance), 0-8, 0-9, the framework section, the seven boss sections,
  the archer / conjurer rows. The 홍련 section is untouched (lane H).

## Files (sources; generated output follows from them)
`tools/build_mboss_core.py`, `tools/mboss_lib.py`, `tools/mboss_registry.json` (`glint` on seven entries + a `_doc` line),
`tools/mboss_guardian/p56.py`, `tools/mboss_butterfly/wing.py`, `tools/mboss_fieldgen/cruise.py`,
`tools/mboss_azhdaha/{leg,tail,trans}.py`, `tools/mboss_apep/p1.py`, `tools/mboss_tachy/{s3lib,p_air,p_mantle,core}.py`,
`tools/mboss_arlecchino/{s3lib,core,p1,p2}.py`, `tools/build_raiden_hazards.py`, `tools/build_balance.py`,
`tools/ch2mob/elite.py`, hand file `data/rlk/function/cm/ar/shoot.mcfunction`; suites `tools/dev/sim/cb/tests/{hzlog,np_table,
test_np}.py` (new), `test_cb.py` (the pinned rule lines), `tools/dev/sim/hr/tests/ident_hr.py` (allow-list group).
No resource-pack file changes (the glint glyph is the one lane C made; `build_raiden_hazards.py --resourcepack <copy>` leaves
the pack's hash at b3df6a5f...).

## How to reproduce / check
```bash
W=<work>; cp -a roguelike/tools/dev/sim $W/sim     # + the path rewrite of sim README 1 B
cd $W/sim/cb/tests
python3 hzlog.py <roguelike> <boss> pat --out=$W/out/<tag>_<boss>_pat.json            # every pattern (test ids)
python3 hzlog.py <roguelike> <boss> pat --dodge --out=$W/out/<tag>_<boss>_dodge.json  # a perfect dodge on every tick
python3 hzlog.py <roguelike> <boss> fight --ticks=3000 --out=$W/out/<tag>_<boss>_fight.json   # passive player, healed
python3 np_table.py $W/out <tag> [boss ...] [--cmp=<other tag>]                       # the table below; the fight log compared
python3 test_np.py <roguelike> [fw b08 b09 mobs table] [--logs=$W/out --tag=<tag>]    # the checks (fail on 6522feef5)
```
Never regenerate a tree while a harness reads it (use a copy: `snap.sh`).

## Steps
- [x] baseline: harness logs + suites on 6522feef5 (`out/base_*`, `sim/out_base`)
- [x] core + lib + registry, the seven modules, Raiden, mobs, balance, Tachy grounding
- [x] `test_np.py` (84 `table` checks + fw 19 / b08 4 / b09 5 / mobs 6 pass on the tree; on the base: `table` 29 fail, the others 14 fail)
- [x] README (section 3, 0-8, 0-9, framework + boss sections, mob rows), `tools/dev/sim/README.md` 3-6
- [x] harness on the tree: the table and the fight comparison below
- [x] gates on the committed tree (suites from a copy of `tools/dev/sim`, the tree = a plain copy of the worktree):
  - `regen_all.sh --mobs` + `build_raiden_hazards.py --resourcepack <copy>` + `build_combat_fx.py`, twice: no diff; the RP copy's
    hash stays b3df6a5f... (= `rp_base`: no pack file changes; `rplint` 0, atlas 12.919 M); `check_mboss_pack` 0 problems
  - loadcheck `fb2` (26.3 server): `0 function load failure(s)`, `Starting minecraft server version 26.3`, `Done (`
  - `test_bal` 117/117, `test_bal_boss` 129/129 (scarlet 6a follows B-09: an untargetable body takes no pips), `test_cb` 217/217,
    `test_rm` all, `test_np` 34 + 84 (`table` on the harness logs)
  - `az/tests_cm/run_all`: the base's statuses — `test_chapter` / `test_fw_az` / `test_fw_ap` / `gen_check` pass; known failures
    unchanged: `test_m0diff` 38 (A: proto +7.03, Guardian +6.16, butterfly +7.26, fieldgen +7.76 per tick; before +7.14 / +6.24 /
    +7.29 / +7.88), `test_px` 4e, `ident` 10, refs 8 known kinds; `check_refs` / `check_macro` / `check_nbtpath` / `lint_mc`
    outputs equal the base's but for the counters and `np_glint` -> `np_gate` in one known lint line
  - `ar/tests`: `test_cm_ar` 65, `test_arena_fl` 46, `test_kit` 8928/8928 (run against a private clone holding `wip/ar-s3`: the
    main checkout has no such branch, so `run_all.sh` stops there on the base too), `test_arlecchino`, `pat_p1`, `pat_p2`, `kit_dry` all pass
  - `hr/tests` (her module's output is byte-identical; these check the framework under her): `test_special_hr` all (E9: the
    generated glint table lives in `mboss/d/` beside the dispatchers), `ident_hr` (allow-list group "fix B"), `ev_dry` 78,
    `test_moon` 55, `test_hwamu` 283, `test_arena_hr` 94, `test_kit` 13362, `test_scarlet`, `pat_p1`, `pat_ghost`, `test_reward` all pass (`test_rig` needs her skin source and
    `gen_check_hr` the resource pack: not part of this lane's change)
- [x] push `wip/combat-fix-b`

## Counts (pattern groups with an unparriable part / all; in brackets: those with the glint = unparriable and dodgeable)
| boss | before (6522feef5) | after | hazards unparriable in the pattern runs | glints in the pattern runs |
|---|---|---|---|---|
| 파수꾼 | 4 / 8 (4) | 2 / 8 (2) | 21 / 41 -> 7 / 41 | 21 -> 7 |
| 나비 | 2 / 9 (2) | 1 / 9 (1) | 5 / 77 -> 1 / 77 | 5 -> 1 |
| 역장 | 5 / 9 (3) | 3 / 9 (1) | 22 / 291 -> 10 / 291 | 19 -> 1 |
| 야타용왕 | 14 / 23 (8) | 9 / 23 (3) | 114 / 410 -> 56 / 410 | 71 -> 12 |
| 아펩 | 10 / 12 (9) | 4 / 12 (3) | 89 / 131 -> 38 / 131 | 45 -> 10 |
| 타키 | 4 / 12 (4) | 2 / 12 (2) | 13 / 94 -> 2 / 94 | 13 -> 2 |
| 아를레키노 | 12 / 21 (12) | 6 / 21 (6) | 46 / 196 -> 19 / 196 | 31 -> 11 |

(The reviewer's 11 of 21 for 아를레키노 counts A 4-hit / 5-hit as one. 홍련: her module's list, lane H. 나루카미: her no-dodge
hazards + kinds 9 / 10, no glint.) Before, glints also flashed for no-dodge and lingering hazards (역장 laser / waves, 야타용왕
feint / whip / slide / bolt / orb / fire fields, 아펩 aftermath) and 1 t before the hit for 타키 / 아를레키노.

## The table (harness `hzlog.py pat` + `pat --dodge` + `fight`, tool `np_table.py`; tree = this branch)
Legend: per pattern folder the distinct hazards made in the pattern runs with their state — **P** parryable, **U** unparriable and
dodgeable (the glint), **U-ND** unparriable and no dodge (position / jump; own tell, no glint), **U-field** unparriable
lingering hazard (no glint). `glint → strike` = ticks from the warning glint to the strike of the U hazards (min-max).
`avoided / hits` = with a perfect dodge on every tick, hits avoided / hits that reached the judge. The line under each table
compares the passive 3000-tick fight with 6522feef5 (same seed): hazard, projectile, hit and direct-hit logs but for the
unparriable flag, HP lost, commands per tick.

### 파수꾼・타락 (guardian) — 2 of 8 attack groups have an unparriable part (2 dodgeable = with the glint); passive fight: 6 / 40 hazards unparriable, 6 glints, 24 hits, 206.0 commands / tick
| pattern | hazards [state] | glint → strike | avoided by | perfect dodge on every tick: avoided / hits |
|---|---|---|---|---|
| p/thrust P1 공간 찌르기 | line 9.3 D100 [P] ×7; line 8.4 D115 [P] ×6 | – | parry (F) or perfect dodge | 13/13 |
| p/pull P4 어둠 속에서 퍼지는 공간 | sector 6.8 D120 [P] ×6 | – | parry (F) or perfect dodge | 3/3 |
| p/javelin P2 공간 투창 | line 20 D130 [P]; 1 projectile(s) | – | parry (F) or perfect dodge | 1/1 |
| p/flyslam P5 하늘을 심판하는 자 | disc 5.5 D180 [U] ×5 | 26 t | perfect dodge (no parry) - glint | 5/5 |
| p/slam P3 공간을 집행하는 시련 | disc 6 D160 [P] ×2 | – | parry (F) or perfect dodge | 2/2 |
| p/sweep_g 파수 모드 휘두르기 | sector 6 D165 [P] ×5 | – | parry (F) or perfect dodge | – |
| p/sweep_e 파수 모드 원소 휘두르기 | sector 6 D250 [P] ×7 | – | parry (F) or perfect dodge | – |
| p/fail 파괴 실패 창 | disc 3.4 D220 [U] ×2 | 20 t | perfect dodge (no parry) - glint | 2/2 |
fight log vs base: hz same, pj same, hits same, direct same, ticks same; hazards 40 -> 40, hits 24 -> 24, HP lost 559 -> 559, commands / tick 206.1 -> 206.0

### 달빛 환영 나비 (butterfly) — 1 of 9 attack groups have an unparriable part (1 dodgeable = with the glint); passive fight: 2 / 62 hazards unparriable, 2 glints, 50 hits, 449.1 commands / tick
| pattern | hazards [state] | glint → strike | avoided by | perfect dodge on every tick: avoided / hits |
|---|---|---|---|---|
| p/kick H1 달빛 발차기 | line 4 D55 [P] ×6; disc 1.5 D55 [P] ×6; sector 5 D70 [P] ×6; line 6 D70 [P] ×6 | – | parry (F) or perfect dodge | 10/10 |
| p/dash H3 달빛 돌진 | disc 1.5 D130 [P] ×6; disc 3.5 D130 [P] ×6 | – | parry (F) or perfect dodge | 4/4 |
| p/jump H2 달빛 점프 | disc 3 D45 [P] ×5; disc 2.5 D70 [P] ×5 | – | parry (F) or perfect dodge | 9/9 |
| p/vacuum H4 광폭한 진공 | 3 projectile(s) | – | parry (F) or perfect dodge | – |
| p/strike B1 우아한 날개 | line 10 D70 [P] ×4; sector 4 D70 [P] ×4 | – | parry (F) or perfect dodge | 3/3 |
| p/sweep B3 날개 휩쓸개 | sector 4.5 D80 [P] ×4; disc 1 D20 [P] ×16 | – | parry (F) or perfect dodge | 3/3 |
| p/barrage B2 화염 날개의 습격 | 80 projectile(s) | – | parry (F) or perfect dodge | – |
| p/coco B4 달빛 축복 | disc 2.8 D100 [P] ×2; 6 projectile(s) | – | parry (F) or perfect dodge | – |
| p/release 달빛 해제 | disc 10 D130 [U] | 26 t | perfect dodge (no parry) - glint | 1/1 |
fight log vs base: hz same, pj same, hits same, direct same, ticks same; hazards 62 -> 62, hits 50 -> 50, HP lost 457 -> 457, commands / tick 449.1 -> 449.1

### 실험성 역장 발생 장치 (fieldgen) — 3 of 9 attack groups have an unparriable part (1 dodgeable = with the glint); passive fight: 15 / 148 hazards unparriable, 1 glints, 56 hits, 429.6 commands / tick
| pattern | hazards [state] | glint → strike | avoided by | perfect dodge on every tick: avoided / hits |
|---|---|---|---|---|
| p/bomb C1 일점 상쇄 | disc 1.3 D150 [P] ×120; disc 5 D270 [P] ×6 | – | parry (F) or perfect dodge | 16/16 |
| p/slam C2 내려찍기 | disc 5 D270 [P] ×6 | – | parry (F) or perfect dodge | 6/6 |
| p/rock C6 파쇄 | disc 1.8 D225 [P] ×53; 11 projectile(s) | – | parry (F) or perfect dodge | 10/10 |
| p/laser C3 코어 광선 | line 2.8 D75 [U-field] ×6 | – | leave it (lingering; no parry), no glint | 1/1 |
| p/missile C4 바위 폭탄 | disc 1.5 D165 [P] ×20 | – | parry (F) or perfect dodge | 4/4 |
| p/burst C5 지면 충격 | disc 12 D330 [U] | 45 t | perfect dodge (no parry) - glint | – |
| p/fzone F1 감소 영역 | disc 2.8 D75 [P] ×50 | – | parry (F) or perfect dodge | 19/19 |
| p/frock F2 파쇄(역장) | disc 1.8 D105 [P] ×26; 9 projectile(s) | – | parry (F) or perfect dodge | 3/3 |
| p/waves 인력 충격파 | ring 0-2.5 D75 [U-ND] ×3 | – | position / jump only (no parry, no dodge), own tell, no glint | 0/3 |
fight log vs base: hz same, pj same, hits same, direct same, ticks same; hazards 148 -> 148, hits 56 -> 56, HP lost 1015 -> 1015, commands / tick 429.7 -> 429.6

### 야타용왕 (azhdaha) — 9 of 23 attack groups have an unparriable part (3 dodgeable = with the glint); passive fight: 0 / 122 hazards unparriable, 0 glints, 70 hits, 767.1 commands / tick
| pattern | hazards [state] | glint → strike | avoided by | perfect dodge on every tick: avoided / hits |
|---|---|---|---|---|
| p/chin 턱 내려찍기 | disc 5 D48 [P]; sector 5.6 D48 [P] | – | parry (F) or perfect dodge | – |
| p/spikes 가시 | disc 1.6 D34 [P] ×94; disc 2.5 D34 [P] ×92 | – | parry (F) or perfect dodge | 44/44 |
| p/jump 도약 | disc 4.5 D44 [P] ×17; ring 0-3 D44 [P] ×33 | – | parry (F) or perfect dodge | – |
| p/charge 돌진 | disc 4 D158 [P] | – | parry (F) or perfect dodge | – |
| p/burrow 잠복 | disc 3.4 D50 [P] ×23; disc 1.4 D29 [P] ×21; disc 3 D58 [P] ×11; disc 3.7 D79 [P] ×4; disc 4 D45 [P] ×3 | – | parry (F) or perfect dodge | 36/36 |
| p/stomp 발 구르기 | ring 0-1.5 D36 [P] ×3; disc 2.8 D36 [P] | – | parry (F) or perfect dodge | – |
| p/feint 성동격서 | line 6.6 D101 [U-ND] ×2; disc 2.5 D50 [P] ×2 | – | parry (F) or perfect dodge; position / jump only (no parry, no dodge), own tell, no glint | – |
| p/whip 교활한 통수(꼬리 채찍) | sector 12 D129 [U-ND] ×9; disc 2 D129 [U-ND] ×6; disc 1.7 D129 [U-ND]; disc 1.2 D129 [U-ND]; disc 1.1 D129 [U-ND]; disc 1.6 D71 [P] ×4 | – | parry (F) or perfect dodge; position / jump only (no parry, no dodge), own tell, no glint | – |
| p/tailslam 꼬리 내려찍기 | line 1.7 D122 [P] ×2 | – | parry (F) or perfect dodge | – |
| p/stomp3 발 구르기(3) | ring 0-1.5 D36 [P] ×3; disc 2.8 D36 [P] ×3 | – | parry (F) or perfect dodge | – |
| p/slide 파멸의 산사태 | ring 0-4 D71 [U-ND] ×5; ring 0-4 D86 [U-ND] | – | position / jump only (no parry, no dodge), own tell, no glint | 0/1 |
| orb 물 구체 | disc 1.3 D29 [U-field] ×4 | – | leave it (lingering; no parry), no glint | – |
| p/meteor 운석 | disc 5.2 D110 [U]; disc 2.8 D66 [P] ×6 | 28 t | parry (F) or perfect dodge; perfect dodge (no parry) - glint | 2/2 |
| fld 불 장판 | disc 4.5 D8 [U-field] ×2; disc 2.8 D8 [U-field] ×6; disc 4 D13 [U-field] ×2 | – | leave it (lingering; no parry), no glint | 48/48 |
| p/frost 서리 습격(B3) | disc 7.5 D79 [U] ×9 | 22 t | perfect dodge (no parry) - glint | 5/5 |
| p/burrow3 B3 솟구침 | disc 5.2 D122 [U] ×2 | 35 t | perfect dodge (no parry) - glint | – |
| xt 꼬리 원소 부가 | ring 0-1.5 D50 [P] | – | parry (F) or perfect dodge | – |
| xl 다리 원소 부가 | 8 projectile(s) | – | parry (F) or perfect dodge | – |
| p/bolt 벼락 습격(B3) | mask safe 3.2 D101 [U-ND] ×3; disc 1.6 D44 [P] ×6; mask safe 2.8 D101 [U-ND] | – | parry (F) or perfect dodge; position / jump only (no parry, no dodge), own tell, no glint | 6/10 |
| p/icicle 고드름 | disc 1.6 D40 [P] ×5 | – | parry (F) or perfect dodge | 5/5 |
| p/shell 물 포탄 | disc 2.4 D58 [P] ×8 | – | parry (F) or perfect dodge | 2/2 |
| p/icespike 얼음 가시 | disc 4 D40 [P] ×3 | – | parry (F) or perfect dodge | 1/1 |
| p/elspike 번개 가시 | disc 3 D50 [P] ×6 | – | parry (F) or perfect dodge | 4/4 |
fight log vs base: hz same, pj same, hits same, direct same, ticks same; hazards 122 -> 122, hits 70 -> 70, HP lost 529 -> 529, commands / tick 767.4 -> 767.1

### 아펩의 오아시스 파수꾼 (apep) — 4 of 12 attack groups have an unparriable part (3 dodgeable = with the glint); passive fight: 12 / 53 hazards unparriable, 12 glints, 45 hits, 826.2 commands / tick
| pattern | hazards [state] | glint → strike | avoided by | perfect dodge on every tick: avoided / hits |
|---|---|---|---|---|
| p/burrow P1 잠복 돌진 | disc 4.2 D108 [P] ×2; line 10.8 D125 [P] ×2 | – | parry (F) or perfect dodge | 4/4 |
| p/hands P2 생명의 손 | disc 4.2 D67 [P] ×4; line 8.4 D85 [P] ×16 | – | parry (F) or perfect dodge | 8/8 |
| p/wither P4 초목이 시든 풍경 | disc 9 D85 [U] ×5 | 24 t | perfect dodge (no parry) - glint | 4/4 |
| p/combo P6 근접 콤보 | sector 7.2 D55 [P] ×6; disc 6.6 D67 [P] ×5; disc 7.2 D50 [P] ×2; disc 6.6 D77 [P] | – | parry (F) or perfect dodge | 8/8 |
| p/glow P3 발광하는 파수꾼 | disc 5.4 D110 [U] ×2; ring 2-3 D30 [P] ×3; disc 5.4 D130 [U]; 6 projectile(s) (6 U) | 23-31 t | parry (F) or perfect dodge; perfect dodge (no parry) - glint; position / jump only (no parry, no dodge), own tell, no glint | 3/3 |
| p/tail P5 생명의 꼬리 | sector 11.4 D130 [U] ×8; sector 11.4 D140 [U] ×8 | 16-27 t | perfect dodge (no parry) - glint | – |
| p/mstrike Q1 이동 돌진 | disc 4.2 D56 [P] ×5; disc 4.2 D60 [P] ×4; disc 12 D60 [P] ×4 | – | parry (F) or perfect dodge | 8/8 |
| p/aftermath Q2 종말의 여파 | mask safe 4.5 10‰ [U-ND] ×7; mask safe 4.5 800‰ [U-ND] ×7 | – | position / jump only (no parry, no dodge), own tell, no glint | 0/64 |
| p/shells Q3 포탄 | disc 3.6 D52 [P] ×3; disc 3 D45 [P] ×2 | – | parry (F) or perfect dodge | 4/4 |
| p/surface Q3s 솟구침 | disc 3.6 D32 [P] ×2; disc 3 D52 [P] ×2 | – | parry (F) or perfect dodge | 2/2 |
| p/tail3 Q 꼬리(3단계) | sector 12 D52 [P] ×8; sector 12 D56 [P] ×8 | – | parry (F) or perfect dodge | 2/2 |
| p/spiral Q5 나선 | disc 2 D48 [P] ×12; line 14 D24 [P] ×2 | – | parry (F) or perfect dodge | 2/2 |
fight log vs base: hz same, pj same, hits same, direct same, ticks same; hazards 53 -> 53, hits 45 -> 45, HP lost 554 -> 554, commands / tick 826.3 -> 826.2

### 타키 (tachy) — 2 of 12 attack groups have an unparriable part (2 dodgeable = with the glint); passive fight: 0 / 88 hazards unparriable, 0 glints, 85 hits, 496.3 commands / tick
| pattern | hazards [state] | glint → strike | avoided by | perfect dodge on every tick: avoided / hits |
|---|---|---|---|---|
| p/a1 1 돌진 베기 | line 12 D42 [P] ×3; sector 4.1 D42 [P] ×3 | – | parry (F) or perfect dodge | – |
| p/c1 5 연속기 · 블링크 | sector 4.3 D29 [P] ×12; disc 5 D42 [P] ×8; sector 4.1 D29 [P] ×8; sector 4.8 D42 [P] ×7; line 0.5 D56 [P] ×4; line 0 D56 [P] ×2; line 1 D56 [P] | – | parry (F) or perfect dodge | 35/35 |
| p/b2 3 옆걸음 4연격 | sector 4.3 D42 [P] ×5; line 6 D56 [P] ×3; sector 3.8 D29 [P] ×6 | – | parry (F) or perfect dodge | 14/14 |
| p/b1 2 날개 가리기 2연격 | sector 4.6 D42 [P]; sector 4.1 D56 [P]; disc 1.9 D56 [P] | – | parry (F) or perfect dodge | 2/2 |
| p/w1 9 지상 장풍 | 23 projectile(s) | – | parry (F) or perfect dodge | – |
| p/b3 4 충전 6연격 | sector 6 D42 [P]; sector 4.3 D29 [P] ×2; sector 3.8 D42 [P] ×3; disc 1.7 D42 [P] ×3 | – | parry (F) or perfect dodge | 3/3 |
| p/c2 6 연속기 · 블링크 Ⅱ | sector 4.1 D29 [P] ×4; sector 4.3 D42 [P] ×2; line 0.5 D56 [P] ×2 | – | parry (F) or perfect dodge | 6/6 |
| p/c3 7 붉은 핵 연속기 | sector 4.1 D29 [P] ×3; sector 4.6 D42 [P] ×2; line 0.5 D56 [P] | – | parry (F) or perfect dodge | 5/5 |
| p/k 8 블링크 | line 3 D56 [P]; disc 4.2 D71 [P] | – | parry (F) or perfect dodge | 1/1 |
| p/w2 10 공중 장풍 | sector 5.4 D71 [P]; 3 projectile(s) | – | parry (F) or perfect dodge | – |
| p/l 11 착지 공격 | disc 1.7 D42 [P]; disc 5.5 D71 [U] | 20 t | parry (F) or perfect dodge; perfect dodge (no parry) - glint | 2/2 |
| p/mantle 과부하 외피(깃털 · 노바) | full 250‰ [U] | 44 t | perfect dodge (no parry) - glint | 1/1 |
fight log vs base: hz same, pj same, hits same, direct same, ticks same; hazards 88 -> 88, hits 85 -> 85, HP lost 688 -> 688, commands / tick 496.4 -> 496.3

### 아를레키노 (arlecchino) — 6 of 21 attack groups have an unparriable part (6 dodgeable = with the glint); passive fight: 0 / 54 hazards unparriable, 0 glints, 64 hits, 443.3 commands / tick
| pattern | hazards [state] | glint → strike | avoided by | perfect dodge on every tick: avoided / hits |
|---|---|---|---|---|
| p/a2 A 사형장으로의 초대 2타 | sector 4.2 D36 [P] ×40 | – | parry (F) or perfect dodge | 38/38 |
| p/c1 C 불꽃 도약 | disc 3.6 D50 [P] ×16; line 6 D50 [P] ×16 | – | parry (F) or perfect dodge | 16/16 |
| p/b1 B 붉은 달의 낫 | 25 projectile(s) | – | parry (F) or perfect dodge | – |
| p/a5 A 5타 | sector 4.2 D26 [P] ×2; disc 4.6 D36 [P]; sector 3.6 D36 [P]; disc 2.2 D36 [P]; disc 4.8 D36 [P] | – | parry (F) or perfect dodge | 1/1 |
| p/a4 A 4타 | sector 4.2 D26 [P] ×2; disc 4.6 D36 [P]; sector 3.6 D36 [P]; disc 2.2 D36 [P] | – | parry (F) or perfect dodge | – |
| p/d1 D 블러드 돌진 | line 6.5 D36 [P]; sector 4.2 D36 [P] ×3; line 14 D36 [P] ×2 | – | parry (F) or perfect dodge | 1/1 |
| p/b2 B 손아귀 | disc 2.2 D36 [P]; 4 projectile(s) | – | parry (F) or perfect dodge | 1/1 |
| p/c2 C 날개 | disc 3.6 D50 [P]; line 6 D50 [P]; sector 5.6 D36 [P] | – | parry (F) or perfect dodge | 2/2 |
| p/d2 D 추가타 | line 14 D36 [P]; sector 4.2 D36 [P] | – | parry (F) or perfect dodge | – |
| p/e1 E 와리가리 베기 | sector 5.2 D36 [P]; disc 4.2 D36 [P] | – | parry (F) or perfect dodge | 2/2 |
| p/f1 F 붉은 피의 연회 | full D36 [U] ×2 | 30-50 t | perfect dodge (no parry) - glint | 2/2 |
| p/g1 G 죽음의 칼날 | line 14 D36 [P] ×4; full D26 [U] | 34 t | parry (F) or perfect dodge; perfect dodge (no parry) - glint | 3/3 |
| p/h1 H 연옥 그림자 분신 | line 5 D36 [P] ×2; sector 6 D36 [P]; sector 5 D36 [P] | – | parry (F) or perfect dodge | 4/4 |
| p/q0 Q0 낙하 공격 | disc 3 D36 [P] ×8; ring 3-7 D36 [P] ×8 | – | parry (F) or perfect dodge | 8/8 |
| p/q2 Q2 불꽃이 타오르는 낫 | disc 2.2 D36 [P] ×9; sector 4.5 D36 [P] ×9; 9 projectile(s) | – | parry (F) or perfect dodge | 9/9 |
| p/q1 Q1 사형장으로의 초대(쌍낫) | disc 4.2 D26 [P] ×6; sector 4.5 D26 [P] ×6; sector 4.4 D26 [P] ×10; 32 projectile(s) | – | parry (F) or perfect dodge | 22/22 |
| p/q3 Q3 붉은 죽음의 무도회 | disc 4.6 D36 [P]; 4 projectile(s) | – | parry (F) or perfect dodge | – |
| p/q4 Q4 떠오르는 재액의 달 | line 30 D50 [U] ×3 | 26 t | perfect dodge (no parry) - glint | 3/3 |
| p/q5a Q5A 형벌의 핏값 | disc 6 D50 [U]; ring 6-15 D50 [U]; disc 11 D64 [U] | 21-35 t | perfect dodge (no parry) - glint | – |
| p/q5b Q5B 붉은 피의 사형 | disc 5.5 D26 [P] ×9; disc 7.5 300‰ [U] | 20 t | parry (F) or perfect dodge; perfect dodge (no parry) - glint | – |
| p/q6 Q6 핏빛 연회 | disc 1.6 D26 [P] ×6; disc 4 D50 [U]; disc 5 D50 [U] ×8 | 28 t | parry (F) or perfect dodge; perfect dodge (no parry) - glint | 7/7 |
fight log vs base: hz same, pj same, hits same, direct same, ticks same; hazards 54 -> 54, hits 64 -> 64, HP lost 1232 -> 1232, commands / tick 443.3 -> 443.3

Glint points (above the floor; from the pattern runs): 파수꾼 P5 2.8 b (her chest, registry) · the failure spears 6.0 / 3.0 b (she
hovers); 나비 4.9 b (the rig's core anchor in the whirl); 역장 4.5 b (the core); 야타용왕 운석 2.6 b up and 3.2 b ahead of the anchor
(registry: between chest and head) · 서리 4.0 b on the tail pillar · B3 2.5 b above the mound at the centre; 아펩 3.3 b up, 1.0 b
ahead (registry: thorax / head); 타키 노바 1.75 b · 착지 공격 at her chest while still high (14.75 b above the floor); 아를레키노 the
rig's chest anchor of the clip tick (1.5-2.8 b above her feet; Q4 5.9 b and Q6 13.8 b above the floor: she is in the air).

Not unanswerable (test_np `table` 9-11): with a perfect dodge on every tick every U hit is avoided and no U-ND hit is; two U
strikes that a dodge must answer are never closer than 10 t (the least a 12-t cooldown allows): the nearest are 아펩's two
tail swings (>= 17 t for one standing spot), 타키's landing (the parryable impact 10 t before the shock: F, then the dodge),
아를레키노 Q5A 26 / 37 t, F 36 t, 파수꾼's two failure spears 23 t, 야타용왕's frost circles 34 t (the last one 24 t before the
emergence).

## Decided here (say so if it should be otherwise)
- **Raiden** (B-04 + B-11): every unparriable hazard of hers is no-dodge or a field / safe dome, so `hazard/new` flashes no
  glint at all now (before: her four no-dodge attacks did). `player/def/fx/rd_glint` (lane FA's folder) is left unused.
- **Leads**: the glint is at the start of the strike's own tell: 20-35 t for most, 44 / 45 / 50 t for the three long
  charges (타키 노바, 역장 지면 충격, 연회의 첫 타: one glint at the start of the charge), 16 t for 아펩's second tail swing (it
  starts right after the first; swing 1: 20 t). No timing, damage or shape of any boss attack changed.
- **아펩 발광**: only the three slam discs are unparriable (the ruling says discs); the rolling carpet ring is a separate,
  parryable / jumpable hit, and it shares its volley group with one homing wheel (no-dodge): answering the ring perfectly
  also spends that wheel.
- **야타용왕 성동격서 / 꼬리 채찍**: the no-dodge lanes / sectors keep the small parryable discs of the same pattern (front / back
  bumps, the cracks after the whip): a place to leave + ordinary hits, as before; no glint.
- **B-09** by the framework flag `rlk_mb_inv` (untargetable body) in `bal/boss/may`, not by a module hook: 아펩's parked body,
  any boss under the floor / away in the air. Lane H's planned `#mbBalOff` line goes into the same function (keep both).
- **Tachy 착지 공격 / Arlecchino Q4, Q6**: the glint is on the body in the air (the rule: the visible body). Whether it is inside
  the F5 top view has to be seen in the game.

## Log
- 11-11 baseline (6522feef5): harness logs of the seven bosses reproduce the reviewer's table (4 / 8, 2 / 9, 5 / 9, 14 / 23, 10 / 12,
  4 / 12, 아를레키노 12 / 21 by pattern folder) and its leads (타키 / 아를레키노 1 t); `test_np` on the base: `table` 29 fail, `fw` /
  `mobs` / `b08` / `b09` 14 fail (B-01 thresholds, B-06 no owner, B-07 rams during the groggy / no attacker, B-08 y 201.33 for the whole
  groggy, B-09 gauge 0 + pending while parked).
- 11-11 the tree: table above; passive 3000-tick fights identical to the base in all seven (hazards, projectiles, hits, HP lost);
  commands per tick 206.1 -> 206.0, 449.1 -> 449.1, 429.7 -> 429.6, 767.4 -> 767.1, 826.3 -> 826.2, 496.4 -> 496.3, 443.3 -> 443.3.
- The machine was shared with the 홍련 lanes while the suites ran (load 10-20): suite times are 2-4 x the usual.
- Open for the merge: lane FA may touch the same places — `build_mboss_core.py` hz/hurt / pj/hit (A-04 is done here through
  `mboss/grp_hit`), README section 3 and the boss lines 2052 / 2192 / 2201 (A-10), `test_cb.py` (here: the pinned np_def / hz/init
  lines, the np_def cases, the Raiden glint check); lane H: `build_balance.py` `bal/boss/may` (its `#mbBalOff` line next to this
  lane's `rlk_mb_inv` line), `ident_hr.py` (allow-list groups).
