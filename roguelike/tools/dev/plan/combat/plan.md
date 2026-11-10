# 전투 개편 · 홍련 재완성 — 작업 계획 (리드, 11-10)

읽을 것: `decisions.md`(사용자 요청 원문 · 결정 · 기본값), `research_combat.md`(플레이어 쪽: 피해 경로 · 대쉬 · 입력 · 에너지 · 쿨),
`research_mobs.md`(적 쪽: 균형치 · 그로기 · UI), `research_misc.md`(요이미야 · 활 / 1인칭 · 숄더뷰 제거, 선택 안내, 후반 렉),
`video_notes.md` + `ref/`(원작 영상 분석, 도착하는 대로). 모두 이 폴더(`roguelike/tools/dev/plan/combat/`, 가지 `wip/combat`).

## 가지와 통합
- 통합 가지 `wip/combat`(2dcc742 + 계획 문서). 각 작업은 `wip/combat-<lane>` 에서 하고, 검사를 통과한 단계마다 그 가지를 GitHub 에
  올린다(사용자 허락: wip/*). 끝나면 리드가 `wip/combat` 으로 합친다. 릴리스 때만 `claude/exciting-pascal-ek1vuy` 로.
- 공용 서버 검사: `RLK_DEV=/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad bash <wt>/roguelike/tools/dev/loadcheck.sh <wt>/roguelike <tag>`
  (서버 · JDK 25 준비됨; 한 번에 한 서버, 잠금이 줄 세움).

## 리소스팩
- 리소스팩은 git 밖이다. 11-06 릴리스 RP 는 고아 가지 `wip/rp-snapshot`(`rlk_hud_resourcepack_1106.zip`, 풀면 sha1 b3df6a5f…)에
  있고, 이 컨테이너에는 `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/rp_base` 에 풀어 두었다(읽기 전용으로 쓰고,
  RP 를 고치는 레인은 자기 사본 `cp -r rp_base rp_<lane>` 에서 만든다).

## 단계 (lane)
| lane | 가지 | 내용 | 먼저 끝나야 하는 것 |
|---|---|---|---|
| R | wip/combat-rm | 요이미야 · 활 삭제(+ 저장 월드 이전), 1인칭 · 숄더뷰 삭제(F5 만; 개발자 모드는 지금 경로 유지), 전투 중 「고를 아이템」 안내 숨김 | — |
| P | wip/combat-perf | 후반 렉: Fix A(핫바 아이템 재생성 · 손 감싸기가 인벤토리를 더럽히는 문제) + Fix B(재스캔 비용) | — |
| B | wip/combat-bal | 모든 적의 균형치(일반 4 · 정예 7 · 보스 12) · 노란 마름모 UI · 회복 · 그로기(경직 + 받는 피해 증가, 끝나면 가득) · 균형치 감소원(원소폭발 적중 · 강한 원소반응; 퍼펙트 패링은 C 가 부름) | — |
| C | wip/combat-core | 패링(F, 3단계) · 닷지(대쉬 대체, 퍼펙트 붉은 이펙트, 일반 몹 넓은 창 / 보스 퍼펙트만) · 피해 경로의 공격자 정보 · 패링 불가 공격 표시(보스 큰 공격, 색 섬광) · 대쉬를 읽던 모든 곳 전환 · HUD | R (F 키 · 활 조준 정리) |
| H | wip/combat-hr | 홍련을 새 전투 위에서 다시 완성(원작 영상 기준 패턴 · 패링 가능 여부 · 균형치 12 · 그로기) + 컷신(초반 · 페이즈 전환 · 엔딩: 조작 잠금 · 클로즈업 카메라 · 플레이어 아바타가 검을 들고 함께 연기) | C, B, 영상 분석 |
| I | wip/combat | 통합 · 전체 검사 · 검토(독립 검증) · 균형 측정 · 릴리스 | 모두 |

## 경계(인터페이스) — 레인끼리 이 이름을 쓴다
- **균형치(B 소유, `rlk:bal/**`)**: 적 몸 엔티티에 점수 `bal`(남은 칸) · `balMax` · `balT`(회복 타이머) · `grgT`(그로기 남은 틱).
  `execute as <적> run function rlk:bal/hit {n:<칸>}` = 칸을 깎고(0 이 되면 그로기 시작) UI 갱신. 그로기 여부 = `grgT matches 1..`.
  그로기 동안 받는 피해 배율은 B 가 `combat/apply` 에 넣는다.
- **플레이어 쪽(C 소유)**: 퍼펙트 패링이 성공하면 C 가 그 공격의 주인에게 `bal/hit {n:1}` 를 부른다. 공격자를 알기 위한 "피해 문맥"
  (공격자 · 일반 / 정예 / 보스 · 패링 가능 여부 · 공격 종류)은 C 가 피해 입구(`cm/hit_pl` · `mboss/hurt` · 위험 지대 · 바닐라 경로)에 만든다.
- B 와 C 가 같은 파일을 고쳐야 하면 작은 덩어리로, 서로의 줄은 건드리지 않는다.

## 공통 규칙
README 0-6 의 사용자 규칙 전부(팁 문구 금지 · 바닐라 소리 · 바닥 아래 금지 · 블록 속 순간이동 금지 · 소문자 id · 실제 게임 함정 …),
생성 출력은 손으로 고치지 않고 생성기에서 고쳐 다시 만듦(0-4), 두 번 만들어 같아야 함, 다른 보스의 생성 출력은 그 레인의 의도된 변경만,
스위트 · `run_all.sh`(0-9 의 알려진 실패만) · `check_mboss_pack` 0 · loadcheck 0. 커밋 끝 두 줄은 정확히
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_019wi9c7roqDDkFi2TvFWw6G`.
컨테이너가 다시 시작될 수 있으니 진행 기록(`<lane>_progress.md`, 이 폴더)을 늘 최신으로 두고, 검사를 통과한 단계마다 커밋 · 푸시.

## 정기 보고
- 사용자 11-10: 「중간중간 2~3시간마다 얼마나 남았는지 알려줘」 → 예약 작업 「전투 개편 진행 보고」(trig_01PmTgvoDpBSDggLqhpeSkyU, 3시간마다, 이 세션으로). 릴리스까지 끝나면 삭제.
