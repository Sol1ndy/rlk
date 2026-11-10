# lane C 진행 기록 (wip/combat-core)

작업 트리: `<S>/cb/wt_c`(가지 `wip/combat-core`, 기준 `origin/wip/combat` 000bceeb9). 작업 폴더: `<S>/cb/c`.
RP 사본: `<S>/rp_c`(원본 `<S>/rp_base` 는 읽기 전용, 11-06 릴리스 b3df6a5f…).

## 단계
- [x] C1 (커밋 2e77d8bd7) 입력 · 닷지 · 판정 · 문맥 · 효과 · 패링 불가 · 읽던 곳 전환 · 설명문
- [x] C2 (c012d3d25) test_cb 200 · hrsim 닷지 모형 · test_scarlet / pat_ghost / test_hwamu · README · 홍련 노란 표시 · 재사용 대기 12틱
- [x] 병합 origin/wip/combat(레인 P, 4163e8f2f) → 0477aacb7; C3 (75e58e9c3) ident_hr 레인 C 묶음 · test_rm · pworld 앞 단계
- [ ] 게이트 전체(스위트 c3 묶음 진행 중: `<S>/cb/c/out/c3`, 실행기 `<S>/cb/c/suites.sh`, 스냅숏 `<S>/cb/c/snap2`) → push

## 설계 (구현됨)
- 입력: rlk:tick 맨 앞 `player/def/input`(F → player/f_key = 패링 입력, 눈앞 · 몹 실드의 우클릭, F5 rc_hold) + `#now cb`, `#dgOpen cb`.
- 상태(시각 도장): parAt · parLk · parHit · dgAt · dgRw. 닷지 = player/dash(충전 없음, #dashCoolT 15) → dash_go → def/dodge_stamp(+ rlk_dgo 상자).
- 판정: player/take_damage → player/def/judge(무적 > 퍼펙트 닷지 > 3단계 > 넓은 닷지 > 2 · 1단계). 문맥 #hcK/#hcC/#hcNP/#hcND + 태그 rlk_hc_atk.
- 근접 재판정: 창이 열린 동안 rlk_dgo 를 몸으로(ghost_on/off): cm/world · cm/pj/world 전체, mboss hz/hit_near · pj/near, 나루카미 try_near.
- 효과: tools/build_combat_fx.py(RP 글꼴 rlk:cb U+EE00-04 + g/**), 손 player/def/fx/**. 가드 클립 tools/player_motion/<c>/guard.json.
- 패링 불가: mboss hz/np_def(기본 규칙) · #hzNoParry/#pjNoParry, np_glint; 나루카미 nododge(+ k 9/10).

## 기록
- 11-10 시작: 작업 트리 만듦.
- 11-10 코드 1차: 위 설계 전부 + 대쉬 HUD 삭제 + 화무십일홍 · 홍련 조각 · 아펩 탄 · 방패병 돌진 · 설명문. regen 한 번 깨끗, loadcheck cb_c 0.
  RP: rp_c 에 font/cb.json + textures/font/cb/*.png 만 더함(플레이어 리그는 items.json 순서만 바뀌어 rp_base 것으로 되돌림).
- 11-10 병합 뒤: regen_all --mobs 두 번 깨끗 · build_combat_fx / build_raiden_hazards / build_player_rig 두 번 같음(RP 해시 같음) ·
  loadcheck cb_c 0 · test_cb 200/200 · test_rm 72/72 · test_hwamu 283/283 · ident_hr 통과 · test_lag(perf_harness) 통과 · rplint 0 ·
  atlas 12.919 M(변화 없음) · 검사기(refs/macro/nbt/lint) 새 종류 없음. 가드 클립의 빈 fx / events 함수 손으로 더함(대쉬처럼).
- 커밋 trailer 는 C2 부터 `Claude Fable 5.2`(조정자 지시).
