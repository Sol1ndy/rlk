# lane C 진행 기록 (wip/combat-core)

작업 트리: `<S>/cb/wt_c`(가지 `wip/combat-core`, 기준 `origin/wip/combat` 000bceeb9). 작업 폴더: `<S>/cb/c`.
RP 사본: `<S>/rp_c`(원본 `<S>/rp_base` 는 읽기 전용, 11-06 릴리스 b3df6a5f…).

## 단계
- [x] C1 (커밋 2e77d8bd7) 입력 · 닷지 · 판정 · 문맥 · 효과 · 패링 불가 · 읽던 곳 전환 · 설명문
- [x] C2 (c012d3d25) test_cb 200 · hrsim 닷지 모형 · test_scarlet / pat_ghost / test_hwamu · README · 홍련 노란 표시 · 재사용 대기 12틱
- [x] 병합 origin/wip/combat(레인 P, 4163e8f2f) → 0477aacb7; C3 (75e58e9c3) ident_hr 레인 C 묶음 · test_rm · pworld 앞 단계
- [x] C3b-d (4b0c5addf · 38bec12c8 · 0fecbba9a · 4b8181765) 가드 클립 빈 함수 · 우두머리 대리 우클릭 · 동작 잠금 · test_cm_ar
- [x] C4 근접 재판정을 rlk:tick 한 곳(mboss/near_all)으로 · judge 빠른 길(judge2 / end) · np_def 이른 반환 · m0diff / fw_az / fw_ap 갱신
- [x] 병합 origin/wip/combat(레인 B 균형치, 58c6c13f1) → b0f712ddc: bal/hit 대역을 B 의 파일로, README · ident_hr 는 양쪽 다 둠; regen 변화 없음
- [x] C5 test_cb 의 `bal` 묶음(퍼펙트 패링 = 공격자의 균형치 정확히 한 칸; 217/217) · README 대역 설명 고침
- [x] C6 test_m0diff: 병합 트리에서 잰 레인 C 몫(주석 · README 0-9), 레인 C 가 넣고 뺀 가짜 플레이어 이름 목록
- [x] 게이트 전체(병합 트리의 스냅숏 `<S>/cb/c/snap5` = 770c45a61 에서 hr ar az bal, 출력 `<S>/cb/c/out/c5`) → push(origin/wip/combat-core)

## 설계 (구현됨)
- 입력: rlk:tick 맨 앞 `player/def/input`(F → player/f_key = 패링 입력, 눈앞 · 몹 실드의 우클릭, F5 rc_hold) + `#now cb`, `#dgOpen cb`.
- 상태(시각 도장): parAt · parLk · parHit · dgAt · dgRw. 닷지 = player/dash(충전 없음, #dashCoolT 12) → dash_go → def/dodge_stamp(+ rlk_dgo 상자).
- 판정: player/take_damage → player/def/judge(빠른 길: 창 밖이면 end 만) → judge2(무적 > 퍼펙트 닷지 > 3단계 > 넓은 닷지 > 2 · 1단계) → end(문맥 지움). 문맥 #hcK/#hcC/#hcNP/#hcND + 태그 rlk_hc_atk.
- 근접 재판정: 창이 열린 동안 rlk_dgo 를 몸으로(ghost_on/off): cm/world · cm/pj/world 전체, mboss near_all(hz/near · pj/near, rlk:tick 에서 mboss/main 뒤 창이 열린 틱만), 나루카미 try_near.
- 효과: tools/build_combat_fx.py(RP 글꼴 rlk:cb U+EE00-04 + g/**), 손 player/def/fx/**. 가드 클립 tools/player_motion/<c>/guard.json.
- 패링 불가: mboss hz/np_def(기본 규칙) · #hzNoParry/#pjNoParry, np_glint; 나루카미 nododge(+ k 9/10).

## 기록
- 11-10 시작: 작업 트리 만듦.
- 11-10 코드 1차: 위 설계 전부 + 대쉬 HUD 삭제 + 화무십일홍 · 홍련 조각 · 아펩 탄 · 방패병 돌진 · 설명문. regen 한 번 깨끗, loadcheck cb_c 0.
  RP: rp_c 에 font/cb.json + textures/font/cb/*.png 만 더함(플레이어 리그는 items.json 순서만 바뀌어 rp_base 것으로 되돌림).
- 11-10 병합 뒤: regen_all --mobs 두 번 깨끗 · build_combat_fx / build_raiden_hazards / build_player_rig 두 번 같음(RP 해시 같음) ·
  loadcheck cb_c 0 · test_cb 200/200 · test_rm 72/72 · test_hwamu 283/283 · ident_hr 통과 · test_lag(perf_harness) 통과 · rplint 0 ·
  atlas 12.919 M(변화 없음) · 검사기(refs/macro/nbt/lint) 새 종류 없음. 가드 클립의 빈 fx / events 함수 손으로 더함(대쉬처럼).
- 커밋 trailer 는 C2 부터 조정자 지시대로, C4 부터 실행 환경이 주는 표기대로.
- 11-10 C4: m0diff 의 레인 C 몫 — 틱당 비용(근접 재판정 · 입력 앞 단계)을 LANE_C_CMD 1.2 로 예산에 더함, 효과 개체 · 새 objective 는 비교에서 뺌.
  fw_az / fw_ap: #mbDodgeOk 는 이제 퍼펙트 닷지 · 3단계 패링만(무적 · 넓은 닷지 · 1-2단계는 아님).
- 11-10 병합 전 트리(7d06a6649)의 스위트 c4(중간에 멈춤: 병합 트리에서 다시 돎): hr 12개 중 통과 10 + ident_hr(스냅숏이 git 이 아니라 실패; 작업 트리에서 따로 통과) +
  test_rig 1(사용자 스킨 원본이 없는 환경 탓), ar run_all · test_arlecchino · pat_p1 통과. regen 두 번 같음, check_mboss_pack 0, loadcheck cb_c 0, test_lag 통과.
- 11-10 병합 트리(770c45a61) 게이트: regen_all --mobs 두 번 + raiden / combat_fx / player_rig 다시 = 변화 없음, check_mboss_pack 0, loadcheck cb_c 0,
  test_lag 통과, test_cb 217/217, test_rm 72/72, test_bal 117/117, test_bal_boss 통과, ident_hr 통과(작업 트리에서), ar 전부 통과.
  az run_all: m0diff(A 역장 예산 · A 나비 says · B = 기준과 같은 종류, 기준 58c6c13f1 은 37개 / 병합 38개: 더해진 하나가 역장 예산), px 4e, ident 10,
  refs 새 8(레인 C 것 하나: `player/def/fx/g/title -> g/t_` 매크로 이름, 알려진 종류), 옮기지 않은 mb / mb2 / mb3 스위트와 baseline/macro.txt 없음(환경).
  m0diff A(틱당 명령, 기준 58c6c13f1 → 병합): proto 6.40 → 7.14, 파수꾼 5.75 → 6.24, 나비 6.51 → 7.29, 역장 6.80 → 7.88.
- RP 확인: rp_c 에 레인 B 의 build_balance.py --resourcepack 을 함께 넣은 사본에서 rplint 0 · 아틀라스 12.919 M; 글꼴 코드 겹침 없음(bal U+ED00-ED22, cb U+EE00-EE04 · EE0F).
- 11-10 스위트 c5 끝(병합 트리): hr 전부 통과(test_special_hr · test_scarlet · pat_p1 · pat_ghost · test_reward · test_kit 13362 · test_arena_hr 94 ·
  test_hwamu 283 · test_moon 55 · ev_dry 78 · gen_check_hr 28; test_rig 160/161 = 사용자 스킨 원본이 없는 환경 탓 하나; ident_hr 은 작업 트리에서 통과),
  ar 다섯 · bal 둘 · test_cb 217 · test_rm 72 통과. az run_all 을 기준(origin/wip/combat 58c6c13f1)에도 돌려 단계별로 비교: 같은 상태, 다른 것은
  m0diff 37 → 38(역장 예산 하나)과 refs 새 7 → 8(매크로로 만든 이름 `player/def/fx/g/t_$(g)`)뿐. fw_az · fw_ap 는 레인 C 의미로 고친 시험이라 기준에서는 실패, 병합에서 통과.

## 11-12 round W (lane WP)
닷지는 옛 대쉬(3칸 / 3틱)가 아니라 원작의 닷지 한 벌(제자리 비틀기 · 걸음 · 피하면 백스텝 · 더블 닷지 옆돌기; `wp_progress.md`), 패링의 헛누름 사다리는
없앰(w_brief §6). 창 · 재사용 대기 · 판정 순서는 그대로.
