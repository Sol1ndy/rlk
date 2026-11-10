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
- [ ] 게이트 전체(병합 트리의 새 스냅숏에서 hr ar az bal) → push

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
