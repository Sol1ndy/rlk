# lane C 진행 기록 (wip/combat-core)

작업 트리: `<S>/cb/wt_c`(가지 `wip/combat-core`, 기준 `origin/wip/combat` 000bceeb9). 작업 폴더: `<S>/cb/c`.
RP 사본: `<S>/rp_c`(원본 `<S>/rp_base` 는 읽기 전용, 11-06 릴리스 b3df6a5f…).

## 단계
- [ ] C1 입력 · 무적 분리 · 닷지(대쉬 충전 · 게이지 삭제, 짧은 재사용 대기)
- [ ] C2 피해 문맥 · 판정(choke) · 패링 3단계 · 퍼펙트 닷지 · cd_cut · 에너지 · bal/hit
- [ ] C3 효과(패링 단계별 · 퍼펙트 닷지 붉은 화면 · 잔상 · 소리) · 아바타 가드 자세
- [ ] C4 패링 불가 표시(보스 틀 · 모듈) + 노란 섬광
- [ ] C5 대쉬를 읽던 곳 전환(아이템 · 각인 · 캐릭터 · 보스 · 튜토리얼 · 설명문) · README
- [ ] C6 스위트 `tools/dev/sim/cb/tests/test_combat.py` + 기존 스위트 갱신 + 게이트

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
