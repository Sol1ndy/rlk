# lane R 진행 기록 (wip/combat-rm)

작업 트리: `<S>/cb/wt_r`(가지 `wip/combat-rm`, 기준 `origin/wip/combat` 6ff826f6a). 작업 폴더: `<S>/cb/r`
(스위트 사본 `r/sim` — 1절 B 방식, 경로를 `r/sim` 으로 바꿈; 기준 트리 `r/base/roguelike` = 6ff826f6a 의 git archive).

## 단계
- [x] R1 요이미야 · 활 삭제 + 저장 월드 이전 (커밋 R1; 시험 `tools/dev/sim/cb/tests/test_rm.py` static · yoi)
- [x] R2 1인칭 · 숄더뷰 삭제(F5 만) (커밋 R2; test_rm view)
- [x] R3 전투 중 「고를 아이템」 안내 숨김 + 시험 (커밋 R3; test_rm picksub: 기준선 5 실패 → 0)
- [x] 게이트(재생성 두 번 · check_mboss_pack · 스위트 · run_all · ar/tests · az/tests_cm · hr 전부 · loadcheck cb_r) — 아래 「최종 게이트」

## 기록
- 11-10 시작: 작업 트리 만듦.
- R1: 지움 = char/yoimiya 17 · char/bow 활 전용 19(arrow_trail 포함) · weapon_item_bow. 남김 = char/bow/arrow_{tick,step,hit,end,home} · assist · calc
  (로노바 7 · 8 종류만). 이전 = char/migrate_yoi_load(load: cur · start_char · choices · dropq) + char/migrate_yoi(player/tick 한 줄,
  rlk:mig yoi 1b 일 때 한 번: select lumine, rlk:bow_aim, 사이드바, 바닥 카드). 생성기 = build_mboss_core PX_DB aurEnd 줄 → px/db 재생성.
  게이트: regen 두 번 같음 · check_mboss_pack 0 · loadcheck cb_r 0 · test_rm 43/43 · test_hwamu view 8/8 · test_arlecchino predicate/static ·
  test_px(알려진 4e 만). 기준선 스위트(6ff826f6a, `r/basewt`)는 `r/out/base` 에 돌고 있음.
- R2: 지움 = view/{mode,mode_do,mode_help,on,off,ride,rot,rot_lead,cam_go,cam_step,cam_put,cam_y,cam_calc,dur_set,dur_set2,set,tune,tune_apply}
  · lobby/set/{s20,s22,s24,s25}. view/tick = 개발자 모드만 fps_tick, 나머지 ride_tick. load: #on view 1 · #vmode view 2 고정(파수꾼 생성 줄용),
  rlk:view cam/opt/optv/st/pr 지움. 로비 built 12, 「시점」 버튼 없음. README 13절 새로 씀(13-1 없앰), 0-9 에 보스 1인칭 갈래 목록.
  test_hwamu view(개발자 모드 · F5 · 사망 · 선택 공간 7/7). 게이트: regen 두 번 변화 없음 · check_mboss_pack 0 · loadcheck cb_r 0 ·
  test_rm 62/62 · test_special_hr 통과 · 검사기 새 것 없음(줄 이동만).
- R3: lvup/pick_sub 에 두 줄(#active room 1 + #combat room 1.. / #mbLive mb 1 → #ps 0), 떠 있던 줄은 title clear 대신 subtitle ""
  (F5 조준점 유지). README 12절. 게이트: loadcheck cb_r 0 · test_rm 72/72.

## 최종 게이트 (daee040d3 위, 11-10)
- regen_all --mobs 두 번: 두 번째 뒤 변화 없음(생성기 변경은 R1 의 PX_DB 한 줄뿐) · check_mboss_pack 0 problem(s) · loadcheck cb_r 0.
- 기준선(6ff826f6a, `r/basewt`) 대비, 1절 B 사본(`r/sim`; ar test_kit 의 calls 절은 가지 대신 커밋 056d1cd · 53a2d80 을 씀, `ar/tmp` 만듦):
  hr: test_special_hr · test_scarlet · pat_p1 · pat_ghost · test_reward · test_kit 13362 · test_arena_hr 94 · test_hwamu 279(기준 280: 숄더뷰
  경우 하나를 뺌) · test_moon 55 · ev_dry 78 · ident_hr(LANE_R 묶음을 더한 뒤) 모두 통과. test_rig · gen_check_hr 는 리소스팩이 필요해 두 트리
  모두 돌리지 못함. ar: run_all(test_cm_ar 65 · test_arena_fl 46 · test_kit 8928) · test_arlecchino · pat_p1 · pat_p2 · kit_dry 통과.
  az/tests_cm run_all: 기준선과 같은 알려진 실패만(test_m0diff A 는 줄어듦: 기준 force 99 · 2 · 3 초과 → force 3 +6.61 하나, B 는 같은 검사에
  지운 #bow* · #yoi* 상수 이름이 더해짐; test_px 4e; ident 10; 옮기지 않은 mb2 · mb3 · int_tests; vcheck 기준선 없음). test_rm 72/72.
- 검사기(check_refs · check_macro · check_nbtpath · lint_mc 손 폴더): 새 것 없음(줄 이동 · 같은 오탐 종류만).
