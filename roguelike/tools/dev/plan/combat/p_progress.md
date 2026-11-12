# lane P (wip/combat-perf) — 진행 기록

작업 트리: `<S>/cb/wt_p` (가지 `wip/combat-perf`, 기준 `origin/wip/combat` 6ff826f). `<S>` = 스크래치패드
`/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`. 측정 틀 사본 `<S>/cb/p_perf`(원본 `<S>/cb/misc/perf`),
스위트 사본 `<S>/cb/p_sim`(README 1절 B), 기준 트리 `<S>/cb/p_base/roguelike`(`git archive origin/wip/combat`).

## 할 일 / 상태
- [x] 0. 준비: 틀 사본(`<S>/cb/p_perf`: psim 에 `append from …[]` 전부 붙이기 추가, `pworld.py` = 받침 + ride_tick 의 아이템 줄, `pmeas.py` 측정, `pequiv.py` 상태 비교), 기준 측정
- [x] A1 핫바 아이템을 다시 만든 그 틱(자기 변화 창 안)에 consumable · hand_wrap
- [x] A2 F 로 넘어온 UI 아이템의 인벤 이벤트는 dirty 아님
- [x] B1 inv/sync: 실물 수 = order 길이면 collect_loop 건너뜀
- [x] B2 equip_scan: manage 직후에는 order 의 id 만(이전 보유 id 0 으로)
- [x] B3 scan_add 매크로 없이
- [x] B4 각인 정렬 한 번에(묶음)
- [ ] B5 (선택) 같은 서명이면 다시 만들지 않음 — 하지 않음: info_build 는 정렬 결과 말고도 첫 줄 3~7번 칸의 실물을 다시 놓는다(플레이어가 각인 칸끼리 바꿔 놓은 것도 고침); 건너뛰면 그 경우 동작이 달라짐
- [x] 게이트: check_mboss_pack 0 · run_all · ar/tests · az/tests_cm · hr/** · loadcheck cb_p (아래 「게이트 결과」)

## 기록
- 커밋(로컬): A a0f59f2 · B1 2d67ae4 · B2/B3 e816b8b · B4 c9a64ce (아직 push 전 — 게이트 뒤).
- 측정(`pmeas.py`, 늦은 런 18개 ★★★): 전투 4 427 → 775 명령/틱(A), F-대쉬 6틱 41 027 → 4 577. 한 번의 정리(pass) 12 402 → (B 뒤 측정 예정).
- 찾은 것: (1) A 가 없앤 「우연한 정리」가 가리던 dirty 누락 = items/enh_add(홍련 보상, 인벤 가득) → enh_add 가 dirty 표시.
  (2) player/inv/order_count2 가 load 의 상수 `#c2 tmp`(=2, char/nefer/cat_tick 의 법구 회전)를 덮어씀(기존 버그, 정리 때마다 0) — B1 은
  collect_none 으로 같은 값을 남겨 동작 그대로. 따로 고칠 일로 보고.
- 상태 비교: `pequiv.py` 10 시나리오(18개 ★★★ · 3개 · 중복+석판+강화 섞음 · invCap 9 가득 · 나비아/네페르/클로린드/로노바/스커크 충전 · 빈 인벤;
  전투 · F-대쉬 · 버리기 · 자리 바꾸기 · 얻기 · 강화 · 각인 dev · 10초 폴백 · 개발자 모드). base→A 는 settled, 단계 사이는 raw.
- 11-10 16:0x: loadcheck cb_p = 0 실패(exit 0, 26.3, Done, 1870 advancements), check_mboss_pack 0. 문서 커밋 be6b7ce
  (README 6 한 줄 + scan_add 언급, ident_hr 허용 목록 「combat P」, perf_harness 에 lib/mcsim.py · pworld · pmeas · pequiv · chkreg).
- 스위트: `<S>/cb/p_runsuites.sh <sim 사본> <dp> <tag>` → `<sim>/out_<tag>/summary.txt`. 기준 = `p_sim_base`(tag base), 결과 = `p_sim`(tag final).
- 상태 비교 결과는 `<S>/cb/p_perf/out/eq_*.txt`.
- 상태 비교 끝: base→A(settled) 10/10, A→B1 · B1→B23 · B23→B4(raw) 각 10/10 같음(남는 차이는 스크래치뿐: rlk:scan.* · rlk:pinv.pcnt/cscan…
  · rlk:eng.b/bt · #syO… · 스캔이 끝에 남기는 #cnt #cntF #enh #fA #fD #fC — 모두 읽기 전에 다시 씀). 빠른 스캔 44/61(late18), collect 건너뜀 38/58.
- 측정(pmeas, 같은 틀): late18 한 번의 정리 12 210 → 5 448(매크로 1 066 → 399, 매크로 줄 2 196 → 741; B1 manage 2 889 → 1 007,
  B2/B3 equip_scan 9 321 → 7 087, B4 → 4 440); 밖 764 → 703(최대 12 822 → 6 066); 전투 4 427 → 707(scan 6.2/s → 0.2/s);
  F-대쉬 6틱 41 027 → 4 577(최악 틱 13 061 → 884). small3: 정리 8 117 → 1 638, 밖 714 → 655, 전투 3 147 → 659, F-대쉬 28 604 → 4 426.
- ar test_kit 은 /home/user/rlk 에 가지 wip/ar-s3 · ar-s2 가 없어 사본(p_sim · p_sim_base)의 CALL_SRC 를 커밋 056d1cd · 53a2d80 로 바꿔 돌림:
  base · final 모두 8928/8928.
- 리드 요청(11-10): order_count2 의 #c1/#c2 → #oc1/#oc2 (load 상수 #c2 tmp = 2 를 덮던 것; 네페르 법구 회전), collect_none 없앰.
  load 가 tmp 에 두는 41개 상수(#c<n> · #<n> · #neg<n>)를 load 밖에서 쓰는 곳은 이것뿐(grep). 커밋 e3bed04.
  `perf_harness/test_consts.py`: 출시 트리 · 고치기 전(B4) FAIL(#c2 = 0), 고친 뒤 PASS. B4→C2 상태 비교 10/10(#c2 만 의도된 차이).
  제안 작업 task_b4f074da 는 이것으로 대신(이미 닫혀 있었음).
- `perf_harness/test_lag.py`: 전투 400틱 스캔 ≤ 4, 다시 만든 틱에 consumable, F 뒤 6틱 스캔 0 · 무기 복귀, 진짜 인벤 편집 · 왼손 rlk 아이템 ·
  지도 중 이벤트는 여전히 정리. final PASS, 출시 트리 FAIL 1 · 2 · 3.
- 최종 트리(e3bed04): loadcheck cb_p 0(exit 0, Done, 1870 advancements), check_mboss_pack 0.
- 스위트(최종): ar 은 고치기 전 트리에서 모두 통과(test_cm_ar 65 · arena_fl 46 · test_kit 8928 · arlecchino · pat_p1 · pat_p2 · kit_dry),
  hr · az 는 최종 트리에서 진행 중(`p_sim/out_final/summary_{hr,az}.txt`). 30분 배경 한도에 한 번 끊겨 2시간 한도로 다시.

## 게이트 결과 (최종 트리 = #c2 고침 뒤)
- loadcheck cb_p: 0 function load failure(s), exit 0 (26.3, Done, Loaded 1870 advancements). check_mboss_pack: 0 problem(s).
- 생성기는 고치지 않음(두 번 만들기 해당 없음; az gen_check 는 base · final 모두 통과).
- ar/tests: run_all(test_cm_ar 65 · test_arena_fl 46 · test_kit 8928/8928) · test_arlecchino · pat_p1 · pat_p2 · kit_dry 모두 통과.
- az/tests_cm/run_all.sh: base 와 같은 결과(0-9 의 알려진 것만): test_m0diff 40 FAILED(+6.59/+5.94/+6.71/+6.99, base 와 같은 수),
  test_px 4e, ident 10, mb3/mb2/mb 스위트 없음(옮기지 않음), vcheck macro/lint 기준선 없음. 검사기 원출력 base 대비: refs 함수 수만,
  nbt 0 invalid, lint 같음, macro 는 「with storage 를 모르는 called without args」 같은 종류가 자리만 옮김(+1).
- hr/tests: test_special_hr · test_scarlet · pat_p1 · pat_ghost · test_reward · test_kit 13362 · test_arena_hr 94 · test_hwamu 280 ·
  test_moon 55 · ev_dry 78 · ident_hr 통과(허용 목록에 「combat P」 + 지운 세 파일은 ALLOW_GONE). test_rig · gen_check_hr 는 풀어 둔
  리소스팩이 컨테이너에 없어 못 돎(--rp 필요; base 도 같음).
