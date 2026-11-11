# 시험 도구 (`tools/dev/sim/`)

게임을 띄울 수 없는 컨테이너에서 쓰던 **mcfunction 모의기와 시험 스위트 · 균형 탐침 · 오프라인 그림 도구**, 그리고 보스 · 몹을 만들
때 쓴 **계획 · 계약 · 브리프 · 검토 문서**(`*.md`, 목록은 `roguelike/README.md` 0-7)를 이전 세션의 스크래치패드에서 옮겨 둔 것이다
(11-03; 그대로 복사했고, 고친 곳은 2절 끝 "11-03 에 고친 곳"(+ 두 스위트 README 의 메모)과 문서의 trailer 줄뿐). 같은 날 문서 검토 뒤
생성기 주석 · 보스 절이 가리키는 문서와 옛 공정성 모의(스크립트 + 결과 로그)를 더 옮겼다: `mboss/` · `tele/` · `mb2/{spec,balance,review,integ}` ·
`mb3/fgfix/sim` · `ap/requests` · `az/requests` · `ap/balance` · `tk/review/bal` · `navia/` · `riglib/`(파일 목록은 `roguelike/README.md` 0-7).
11-05 홍련 I1 에서 그 보스의 스위트 `hr/`(3-4)를 더했다. 11-10 전투 개편 B 에서 균형치 스위트 `bal/tests/`(`test_bal.py` · `test_bal_boss.py`; 데이터팩 밖의 사본에서
`python3 test_bal.py <roguelike>`, `test_bal_boss.py <roguelike> [보스 …]`; 보스 쪽은 `hr/tests/lib` · `ar/s3/lib` 를 읽기만 함)를 더했다. `tools/dev/sim` 에 없는 옛 경로는 옮기지 않은 것이다(6절). 데이터팩 zip 에는 들어가지 않는다(zip 은
`pack.mcmeta` `README.md` `engravings.md` `items.md` `data` 만). 전체 흐름 · 릴리스 게이트는 `roguelike/README.md` 의 0장을 본다.

- **배치는 옛 스크래치패드 구조 그대로**다: 옛 `<S>/ar/tests/test_kit.py` → `sim/ar/tests/test_kit.py`. 스위트들이
  `HERE.parent.parent` 같은 상대 경로와 스크래치패드 상수 `S` / `SCR` 로 서로를 찾기 때문이다(`<S>` = 옛 스크래치패드
  `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`).
- 필요한 것: Python 3.13(표준 라이브러리만; 그림은 numpy · Pillow, 없으면 `pat_p*.py` 는 그림만 건너뜀), Node 22(`ar/s2`
  리그 그림 스크립트), ffmpeg(`ar/tools` 영상 시트). 11-03 컨테이너: Python 3.13.16 · numpy 2.5.3 · Pillow 12.3.0 · Node 22.22.0.
- 스위트는 데이터팩을 **읽기만** 한다: 변형 트리 · 복사본은 자기 폴더의 `tmp/` 에 만들고 지우며, 그 안에서 생성기가 쓰는 폴더
  (`mboss/` · `room/cboss/` · `boss/test/` · `tools/`; `gen_check` 는 + `bossui/`)는 진짜 복사, 나머지 `data/` 는 하드 링크다. 11-03 전
  판은 `boss/test/` 를 하드 링크해서, 복사본에서 돈 `build_mboss_core.py` 가 시험한 트리의 `boss/test/*.mcfunction` 13개를 제자리에서
  다시 썼다(같은 바이트, 새 mtime; `gen_check` 9 실패의 원인 — 3-2). 예외: `test_rig.py --rebuild` 는 리그 생성기를 두 번 실제로
  돌린다. 출력(`out/` `tmp/` 그림)과 1절 표에서 다시 만드는 입력(작업 트리 링크 · 풀어 둔 RP · 영상)은 `.gitignore` 가 막는다.

## 1. 실행 전에: 옛 경로

아래 파일에 옛 스크래치패드 경로가 박혀 있다(고치지 않고 옮겼으므로). **스위트는 시험하는 `roguelike/` 트리 안에 있는 `sim/`
(곧 저장소의 `roguelike/tools/dev/sim` 그 자리)에서 돌리지 않는다** — 데이터팩 밖의 사본에서 돌린다. 둘 중 하나를 한다.

- **A. 옛 경로에 사본(파일을 고치지 않음)** — 새 컨테이너에 그 경로가 없을 때만. 11-03 세션처럼 진짜 스크래치패드가 그 자리에
  있으면 하지 말 것. 심볼릭 링크는 쓰지 않는다(스크립트가 `Path(__file__).resolve()` 로 저장소 안의 진짜 위치로 되돌아가, 변형
  트리를 시험하는 트리 안에 만든다).

  ```bash
  OLD=/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e
  mkdir -p $OLD/scratchpad && cp -a /home/user/rlk/roguelike/tools/dev/sim/. $OLD/scratchpad/
  ```
- **B. 사본을 바꿔 쓰기**(저장소의 파일은 고치지 않는다): 데이터팩 밖의 `<작업>` 에 사본을 두고 그 사본만 고친다 —
  `cp -a /home/user/rlk/roguelike/tools/dev/sim <작업>/sim && cd <작업>/sim && grep -rl --exclude='*.md' --exclude='*.json' 2f5e7b47-ba2f-58bc-b880-1598991e2f8e . | xargs sed -i "s|/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad|$PWD|g"`
  (README · 계획 문서 등 `*.md` 와 기록 `*.json` 은 빼고 아래 28개 파일만 바뀜; 커밋하지 않는다).

경로 상수가 있는 파일(`*.md` 문서에도 이 경로가 글로 적혀 있지만 실행과는 상관없다):
`ar/tests/{kit_dry,pat_p1,pat_p2,test_arlecchino,test_rig}.py`, `ar/s3/lib/knsim.py`, `ar/review/bal/{knfair5,batch5}.py`, `ar/review/rend/final_fx.py`, `ar/s1k/render/render_kn_core.py`,
`ar/s2/{b,r,pv,u1,strip,strips_all}.sh` · `introcmp.py` · `pairs.py`, `az/understand/rigtech_render.py`,
`az/tests_cm/{ident,test_fw_az,test_m0diff}.py`(`REPO = <S>/az/wt_cm`), `az/tests_cm/run_all.sh`, `preview/raiden_preview.py`
(도움말 예시만), 그리고 옛 공정성 모의 기록 `mb2/balance/fsim.py` · `mb3/fgfix/sim/fgfair.py` · `tele/fg/sim/fgfair.py` ·
`tk/review/bal/tkfair.py`(옮기지 않은 스위트의 모의기를 import 하므로 경로를 바꿔도 돌지 않는다 — 4절).

A 를 해도 **옛 작업 트리를 가리키는 기본값**은 살아 있지 않으므로 인자로 준다.

| 기본값(없어진 것) | 대신(아래 `sim/` = 스위트를 돌리는 사본: A 면 `<S>`) |
|---|---|
| `<S>/ar/wt_i1/roguelike`(데이터팩 기본값: `kit_dry` `pat_p1` `pat_p2` `test_arlecchino`(`s3/lib/knsim` 의 `DEFAULT_DP`) `test_rig`) | 첫 인자 / `--dp` 로 `/home/user/rlk/roguelike` |
| `ar/review/rend/final_fx.py` 6줄(`sys.argv` 를 `<S>/ar/wt_i1/roguelike` · `<S>/ar/rp_i1` · `<S>/ar/review/rend` 로 덮어씀; 인자를 받지 않음 — 11-02 `final_fight.jpg` 효과 칸 한 번용) | 그 줄을 작업용으로 고치거나 그 경로에 데이터팩 링크 · 풀어 둔 리소스팩을 둔다 |
| `<S>/ar/rp_s2`, `<S>/tk/rp`(`test_rig.py --rp` / `--ref-rp`) | `--rp <풀어 둔 지금 리소스팩>`, `--ref-rp <직전 릴리스 리소스팩>`(플레이어 아바타 모델이 바이트 단위로 같은지 비교) |
| `<S>/ar/review/bal/snap/roguelike`(`batch5.py` 의 `DP`) | 그 줄을 데이터팩 경로로(또는 그 자리에 트리 복사본) |
| `<S>/az/wt_cm`(git 작업 트리, 기준 커밋을 `git archive` / `show`) | 없으면 스스로 `/home/user/rlk` 를 쓴다(기준 커밋 `22ba247` 이 기록에 있음) |
| 가지 `wip/ar-s3` · `wip/ar-s2`(`test_kit.py` 의 calls 절이 `git archive`; 로컬에만 있던 가지) | `git -C /home/user/rlk branch wip/ar-s3 056d1cd && git -C /home/user/rlk branch wip/ar-s2 53a2d80`(둘 다 릴리스 기록 안의 커밋) |
| `<S>/ar/tmp`(`test_kit.py` 의 임시 폴더, `ar/tools` 의 임시 프레임; 미리 있어야 함) | `mkdir -p sim/ar/tmp`(`.gitignore` 됨) |
| `<S>/ar/wt_s2/roguelike`, `<S>/ar/s2/dbg`, `<S>/ar/rp_s2`(`ar/s2/*`, `pose.mjs` 의 `../wt_s2/roguelike/tools/…` import) | `sim/ar/wt_s2/roguelike` 를 저장소의 `roguelike` 로 링크(그러면 `b.sh` 는 저장소의 `boss/arlecchino/rig/**` · `tools/arlecchino_rig_manifest.json` 을 다시 쓴다), `sim/ar/rp_s2` 에 지금 리소스팩 zip 을 통째로 풀어 둔다(`b.sh` 가 리그를 거기에 쓰고 `r.sh` 가 그것으로 그림; 1페이즈 몸 · 낫은 `player_motion` 모델이라 빈 폴더면 몸이 안 그려짐), `--debug-dp` 폴더는 `b.sh` 가 만듦. 링크와 `rp_s2` 는 커밋하지 않는다(`sim/.gitignore` 의 `ar/wt_*` · `ar/rp_*` 가 막음) |
| `<S>/ar/src/*.mp4`, `<S>/ar/ref/*.jpg`(영상과 대조하는 그림) | 사용자가 보낸 영상(새 세션은 다시 받아야 함) |
| `<S>/ar/src/skin_33.png`(`test_rig.py` 161줄이 모듈 맨 위에서 읽는 P2 스킨 원본, 영상이 아님; 없으면 거기서 멈춤) | `mkdir -p sim/ar/src && cp <풀어 둔 리소스팩>/assets/rlk/textures/mboss/arlecchino/skin_p2.png sim/ar/src/skin_33.png`(바이트가 같음; `*.png` · `ar/src` 라 .gitignore 됨) |

## 2. 모의기 라이브러리 (`lib/`)

의존 순서: `mcsim` ← `fgsim` ← `azsim` ← `cmsim` ← `knsim`(보스별). 스위트마다 쓰는 `lib/` 가 정해져 있다: `ar/tests` 의
`test_cm_ar` · `test_arena_fl` · `test_kit` 은 `ar/tests/lib`, `pat_p1` · `pat_p2` · `test_arlecchino` · `kit_dry` 는 `<S>/ar/s3/lib`(경로
상수), `test_rig` 은 `<S>/mb3/tests/mcsim.py`, `az/tests_cm` 은 자기 `lib/`(나중의 수정이 다른 스위트를 흔들지 않게 일부러 복사해 둔
것). 각 폴더 README 의 md5 는 복사 당시 값이라 지금 파일과 다를 수 있다(지금: `ar` 의 mcsim c87853ff, `az/tests_cm` 의 azsim
e9ccb446; cmsim 셋은 11-03 에 고쳐 아래 "11-03 에 고친 곳" 의 값).

| 파일 | 무엇을 흉내 내나 |
|---|---|
| `mcsim.py` | 작은 mcfunction 해석기: scoreboard · execute(as/at/positioned/rotated/facing/if/unless/store) · return · function(매크로, with storage) · summon · kill · tag · tp · data get/modify, 매크로 줄. 모르는 명령(particle, playsound, title …)은 세고 무시. `ar/` 판(md5 c87853ff…)은 I1 · S5 에서 실제 게임 기능만 더함: 타입 배열 `[I;..]` · `execute summon <type>`(I1), NBT 경로 문법(`[{..}]` 필터, `[-n]`, `[]`, `key{..}`; S5). 알려진 차이: 정수 `summon` / `tp` 좌표의 +0.5 보정 없음 |
| `fgsim.py` | 중간보스 틀 세계(역장 발생 장치 스위트에서 시작): `F:mboss` 바깥 엔진 함수는 대역, `combat/apply` · `element/on_hit` · RES · `incoming` 은 진짜. 속성 수정자, Motion, `rlk:tick` 의 저중력 줄 |
| `azsim.py` | S1-HARN 엔진 래퍼: `combat/apply` · `apply_mods` · 처치 경로(골드 · 회복구슬 · 경험치) · 원소 반응 · `player/take_damage` · 보호막 · 방 진입 / 정리 등을 **데이터팩에서 그대로** 돌림. 엔진 난수는 보스 AI 난수와 분리. 데이터팩은 `AZDP` 환경변수 또는 인자 |
| `cmsim.py` | 챕터 모드 세계: 블록 세계(fill / setblock / `if block`), 청크 불림(forceload + 지연), tellraw · title · stopsound 기록, 따옴표 NBT 키, 방 생성 흉내(`boss_map`), 변형 트리(`variant`: 생성 폴더(`mboss/` · `room/cboss/` · `boss/test/`)와 `tools/`(`tools/dev` 빼고)는 복사, 나머지는 하드 링크, `tmp/` 에; 11-03 에 고친 곳은 아래) |
| `ar/tests/lib/knsim.py` | (S1) `variant_ar(dp, route)`: 아를레키노 항목을 켠 변형 트리, 모듈이 없을 때의 대역 모듈, `ar_fight` |
| `ar/s3/lib/knsim.py` | (S3, **이름만 같고 다른 파일**) 아를레키노 모듈 세계 `KnSim`: 디스패처 줄, `fl_ruins` 경기장 디스패처, 진짜 `mboss/start_go` 로 전투 시작, `hit_body`(공격 종류별 깃발로 진짜 `combat/apply`), 틱당 명령 수, 리그 호출 · 바닥 공격 · 투사체 · 플레이어 피격 기록 |
| `ar/tests/lib/knfxsim.py` | 효과 도구 모의기: 서버 틱 순서, item_display 소환 SNBT, 단계 병합, bossbar · title, `execute summon`, NBT 목록 필터 |
| `mb3/tests/mcsim.py` | 처음 판 mcsim(md5 7ac6cf81…). `ar/tests/test_rig.py` 가 `<S>/mb3/tests` 에서 가져다 씀 |

**11-03 에 고친 곳**(옮긴 그대로의 사본과 일부러 다른 곳; `ar/tests/README.md` · `az/tests_cm/README.md` 의 md5 메모가 지금 파일과
다른 까닭):
- 세 `cmsim.py`(`az/tests_cm/lib` · `ar/tests/lib` · `ar/s3/lib`)의 `variant()` 와 `az/tests_cm/gen_check.py` 의 `light_copy()` 는
  `tools/dev` 를 복사하지 않는다. 이 `sim/` 이 시험하는 `roguelike/` 안(`tools/dev/sim`)에 있으면, 트리를 걷는 복사가 자기 `tmp/` 에서
  만들고 있는 복사본까지 다시 복사해 디스크가 찰 때까지 커졌기 때문이다(그래도 1절대로 데이터팩 밖의 사본에서 돌린다).
- 같은 곳에서 `boss/test/` 를 진짜 복사한다(`variant()` 의 `real`, `gen_check.py` 의 `REAL_DP`): 하드 링크면 복사본의
  `build_mboss_core.py` 가 시험한 트리의 파일을 다시 썼다(맨 위 '읽기만' 항목 · 3-2).
- `ar/tests/run_all.sh`: 경로를 모두 따옴표로 묶었다(공백이 든 경로에서 끝의 `rm -rf` 가 갈라져 엉뚱한 폴더를 지우지 않게).
- 지금 md5: `ar/tests/lib` · `ar/s3/lib` 의 cmsim f81cdc23…, `az/tests_cm/lib/cmsim.py` 7de1dd2c…. 고친 뒤 11-03 에 돌린 스위트는
  `ar/tests/test_cm_ar.py` 하나다(문서 검토 때 저장소의 `tools/dev/sim/ar/tests` 그 자리에서): 65 통과 · 실패 0, 고치기 전
  판(`<S>/ar/tests`)과 출력이 같다. 새 판은 `tools/dev` 밖을 건드리지 않았고(자기 `tmp/` 만 생겼다 지워짐), 고치기 전 판은 시험한
  트리의 `boss/test/*.mcfunction` 13개를 같은 바이트로 다시 써 mtime 만 바꿨다. 고친 `variant()` · `light_copy()` 를 거치는
  나머지 가운데 `az/tests_cm` 의 `test_chapter` · `test_fw_ap` · `test_px` · `gen_check` 는 11-05 홍련 I1 의 `run_all`(I1a · I1b · I1b
  검증 1차, 1절대로 데이터팩 밖 사본에서)에서 돌았다: `test_chapter` · `test_fw_ap` · `gen_check` 통과, `test_px` 는 알려진 4e 하나만
  실패(3-2). 마지막까지 돌리지 않았던 `ar/tests/test_arena_fl.py` 는 11-06 홍련 릴리스 게이트(V-I)에서 돌았다: 46 통과 · 실패 0(같은 때
`ar/tests` 의 나머지도 모두 통과, 3-1).

## 3. 스위트

### 3-1. 아를레키노 (`ar/tests/`; 11-02 릴리스 때 S5 검토 기록상 모두 통과, 11-06 홍련 릴리스 게이트에서 다시 모두 통과)
11-06 결과(1절 B 의 사본에서, `<dp>` = 홍련을 합친 트리): `run_all.sh` 의 `test_cm_ar` 65 · `test_arena_fl` 46 · `test_kit` 8 928 통과
(`run_all.sh` 의 요약 줄은 `^ok ` 줄만 세어 `test_kit` 를 "0 ok" 로 적는다: 결과는 그 출력의 끝줄 `test_kit: 8928/8928 passed`),
`test_arlecchino` · `pat_p1` · `pat_p2` · `kit_dry` 모두 통과, `test_rig --rp <지금 팩> --ref-rp <타키 릴리스 팩>` 67 통과.
실행: 스크래치패드에서 `python3 <스위트> <작업 트리>/roguelike …`. `./run_all.sh <dp> [tag]` 는 **S1 셋만**(test_cm_ar ·
test_arena_fl · test_kit) 돌리고 결과를 `out/<tag>_<스위트>.txt` 에 쓴다. 나머지는 하나씩 돌린다. `test_arlecchino` · `pat_p1` ·
`pat_p2` 의 `<dp>` 는 `/` 가 든 경로로 준다(`./roguelike` 나 절대 경로; `/` 가 없으면 절 · 키 이름으로 읽혀 아무것도 돌지 않는다).

| 파일 | 실행 | 무엇을 검사하나 (마지막 결과) |
|---|---|---|
| `test_cm_ar.py` | `<dp> [절 1..6]` | 틀 FN-1(생명의 계약 바닥 공격 옵션: `× #mbBolRe` 는 bol 공격에만, 맞은 틱에 `#mbHitBol` 한 번, 피하거나 연출 중이면 없음, 일회성 옵션, `cleanup_fight`), 중간보스 전투에 새 이름 없음, 라우팅 1~6챕터, FN-3(`px:false` 챕터 경로 전체: 문 · 시작 · 몸 · 체력 나눔 · 음악 · 바닥 · 단계 전환 · 멈춤 · 리로드 · 처치 · 취소 · 패배 · 시험 별칭), 붉은 숲 음악 묶음 (전부 통과) |
| `test_arena_fl.py` | `<dp> [절 1..9]` | 경기장 테마 `fl_ruins`: 명세 = 레지스트리, 걷는 원은 꽉 찬 블록 · 위가 빔, 방벽이 닫힘, 모습 `day` ↔ `crimson` 왕복 · 조각 한도, 빛(돔 안 12 이상 · 바닥 10), 지점, cmsim 으로 실제 짓기, 입구(비석) (S5: 46 통과) |
| `test_kit.py` | `<dp> [<rp>]` | 효과 도구 `build_mboss_kn_fx.py`: 계약의 모든 이름과 인자, 카드 엔진 · 풀, 프리셋마다 카드 · 수명 · 색 · 바닥 위 높이(`HEIGHT` 표: 11-03 에 `cross_thorns` · `shroud` · `shroud_burst` 추가), 바닥 표시 7종(y + 0.02, 6틱 전 번쩍임), 소품(투사체당 카드 하나), 정리 · 제거, 바닐라 소리만(`<S>/rd/tests/sound_ids.txt`), HUD(배지 · 배너 · 대사 줄), RP 를 주면 스프라이트 · 아틀라스 · 글꼴 (11-03, RP 를 주고: 9079/9079; S5 는 `run_all.sh` 라 RP 없이: 8560/8560) |
| `test_rig.py` | `--dp <dp> --rp <rp> [--ref-rp <rp>] [--rebuild]` | 리그 매니페스트 = 계약(26 파트, 41 클립의 길이 · 반복 · 이벤트 · 형태), 1페이즈는 아바타 모델을 참조만(복사 없음), P2 스킨, 모든 클립의 모든 틱에서 바닥 아래로 내려가는 점 없음 · 틱당 120도 넘는 회전 없음 · 컬링 상자 안, mcsim 으로 spawn / play / look / kill / uninstall, `seq.py`, `--rebuild` 는 두 번 빌드해 바이트 비교 (I1: 67 통과) |
| `test_arlecchino.py` | `[<dp>] [절 이름 …]` — `static` `phases` `bond` `predicate` `shock` `orbs` `ai` `reload` `cleanup` `cost`(번호 1..10 은 안 먹는다: 번호를 주면 아무 절도 돌지 않고 'ALL test_arlecchino CHECKS PASSED' 가 찍힌다) | 모듈 코어: 훅 · 정적 규칙(음수 add/remove 없음, 바닐라 소리, 원거리 면역 · 불 내성 없음), 단계 순서(등장 → P1a → 재가 된 만상 → P1b → 전환 T → P2 → 쓰러짐) · 바닥, 생명의 계약(부여 · 회복 · ×2.5 · 지속 피해 · 강제 부여), 일반 공격 판정(캐릭터별), 선혈의 충격 · 파훼 · 기절, 회복구슬, AI(가중치 · 쿨다운 · 일정), 멈춤 / 리로드, 정리, 틱당 명령 수(P1a 평균 445 · P1b 약 505(11-03, 십자 가시 추가 뒤; 11-02 는 494), 아펩 약 830 보다 적어야) (전부 통과) |
| `pat_p1.py` | `[<dp>] [key …]` | 1페이즈 패턴 a2 a4 a5 b1 b2 c1 c2 d1 d2 e1 f1 g1 h1 e70: 타격 틱 = 클립 이벤트, 모양 · 등급 · 불 원소, bol 옵션, 넉백은 마지막 타격만, 예고 ≥ 12틱(큰 것 ≥ 20), 연속기 간격, 몸의 끝점 · 높이, 투사체, 서 있는 플레이어가 모든 휘두르기에 맞음, 바닥 표시는 PLAN §1.5 만, 매 틱 취소 뒤 남는 것 없음. 그림 `<S>/ar/renders/s3_<key>.png` (전부 통과) |
| `pat_p2.py` | `[<dp>] [hits tells geo q5b beam pj q6 q0 ends cancel pause stand decals static render]` | 2페이즈 Q0~Q6: 위와 같은 항목 + 처형(Q5B 마지막 일격은 죽이지 않음) · 빔 조준 · 깃털 · 낙하 조건 · 500 가지 끝점(블록 속 없음). 그림 `s4_<key>.png`, `<S>/ar/s4/endpoints.json` (전부 통과) |
| `kit_dry.py` | `[<dp>]` | 효과 도구를 켠 채(`api.K` 강제) S3 빌드 전체를 가짜 Writer 로: 예외 없음, 모든 효과 호출이 계약 이름 · 인자, 매크로 줄 (통과) |

### 3-2. 챕터 모드 틀 (`az/tests_cm/`, 모든 챕터 보스가 올라앉는 틀의 회귀 시험)
`build_mboss_core.py` · `mboss_lib.py` · 경기장 · 입구를 고치면 돌린다. 각 스위트는 `<dp>` 를 첫 인자로 받는다
(`python3 test_chapter.py <dp>`; 덧붙는 것: `test_px` `[보스 id]`(기본 cproto), `test_m0diff` `--base` · `--forces` · `--modes`,
`gen_check` `--rp <RP>`, `ident` `[기준 커밋] [--save]`, `run_all.sh` `[tag]` + 환경 변수 `RP=` · `JOBS=`). `vcheck.py` 만 데이터팩 대신
`<refs|macro|nbt|pack|lint> <검사기 출력> [--save]` 를 받는다. 자세한 표는 이 폴더의 `README.md`.

| 파일 | 무엇 |
|---|---|
| `test_chapter.py` | 시험 보스 `cproto` 로 라우팅 · 입구 · 문 · 소환 · 처치 보상(× 15 × 챕터, 사파이어 2, 상자 없음) · 취소 · 패배 · 체력 나눔 · 시험 명령 · 음악 · 경기장 모습 · 정리 경로 · 나루카미 연기 |
| `test_px.py` | 판정 프록시: 공격 하나 = 몸에 한 번, 반응 · 지속 피해 · RES · 바닥 · 리로드 |
| `test_fw_az.py`, `test_fw_ap.py` | 틀 도우미(마스크 · 맞음/피함 이벤트 · `pl_dot` · 밀어내기 · 예측 조준 / ‰ 바닥 공격 · 안전 묶음 · 모습 기록 · 연출 중 거부 · 음악 묶음 · 보조 오브젝트 옵션) |
| `test_m0diff.py` | 중간보스 넷(proto · 파수꾼 · 나비 · 역장)이 기준 커밋과 **행동이 같은지**(같은 시드, 틱마다 기록, 틱당 명령 수 +6.5 이내). 기준 = `git archive 22ba247`(`REPO`) |
| `gen_check.py` | 복사본에서 생성기 순서 · 두 번째 실행 · 거꾸로 · 소유 경로(`--rp` 면 킷 · 보스바의 RP 를 두 번 빌드해 비교) |
| `ident.py` | **낡음**(22ba247 · S1-CM 파일 목록에 고정 — 아래 알려진 실패): 기준 커밋과 바이트 비교(중간보스 출력 · 광장 · 엔진 파일 · `baseline/shared_edits.diff` 에 박은 공용 수정) |
| `vcheck.py`, `baseline/` | 정적 검사기 결과를 기준선과 비교(새 발견만 실패). **`baseline/lint.txt` · `macro.txt`(약 600 KB)는 옮기지 않았다**: `refs` 만 비교 가능, 나머지는 지금 릴리스 트리에서 한 번 돌려 기준선을 다시 만든다 |
| `run_all.sh` | 위 전부 + `<S>/mb3` · `<S>/mb2` · `<S>/mb/int_tests` 스위트(옮기지 않음 → 그 단계는 실패) + 검사기 |

**11-02 기준 이미 알려진 실패**(S1 보고 R6, 새 변경 탓이 아님): `test_m0diff` A(틱당 명령 수: proto +6.57 · 나비 +6.70 · 역장
+6.98 > 예산 6.5, 파수꾼 +5.93 통과; D0 에서도 +6.54 / +6.65 / +6.92) · B, `test_px` 4e, `ident`(22ba247 · S1-CM 파일 목록에 고정돼 낡음: 11-02
트리에서 10개 실패 — `ident` 의 검사 1 넷 · 3a · 3b · 4a~4d; 기준을 다시 만들기 전에는 신호가 없음), 검사기 refs / macro 의 알려진
종류. 기준선을 다시 박는 것은 아직 안 함. (`gen_check` 9 — 시험한 트리의 `boss/test/*.mcfunction` 13개가 하드 링크로 다시 쓰이던 것,
맨 위 '읽기만' 항목 — 는 11-03 의 `REAL_DP` · `variant()` 고침 뒤 11-05 홍련 I1 의 `run_all` 에서 통과해 이 목록과 `roguelike/README.md`
0-9 에서 뺐다.)

### 3-3. 정적 검사기 (스크래치패드 맨 위에 있던 것)
| 파일 | 실행 | 무엇 |
|---|---|---|
| `check_refs.py` | `python3 check_refs.py <dp>` | 부르는 함수 · 함수 태그가 있는지, `$(` 가 매크로 줄 밖에 없는지, (나루카미) 쓰는 점수판이 만들어지는지 |
| `check_macro.py` | 데이터팩 루트에서 `python3 <sim>/check_macro.py <dp>` | `$` 줄의 `$(키)`, 매크로 함수 호출의 인자(빠진 키 · 인자 없이 호출 · 매크로가 아닌데 인자), 없는 함수 |
| `check_nbtpath.py` | `python3 check_nbtpath.py <dp>/data` | NBT 경로 인자가 게임 문법(NbtPathArgument)에 맞는지 |
| `mb/lint_mc.py` | `python3 mb/lint_mc.py <dp> [data/rlk/function 아래 경로 …]`(경로를 안 주면 `mboss/` 만 본다; 전체는 `boss char combat …` 처럼 폴더를 준다) | 명령 모양 린터(괄호 · 따옴표 · execute 문법 · 선택자 · 좌표 · 명령별 모양, 매크로) |
알려진 오탐이 많으므로 **릴리스 트리의 결과와 비교해 새로 생긴 것만** 본다.

### 3-4. 홍련 (`hr/tests/`; 11-05 I1 에서 옮김, 그때 모두 통과)
스크래치패드 `hr/tests/` 에서 쓰던 것을 같은 상대 경로로 옮겼다(`hr/tests/lib` = `hrsim.py` + 챕터 틀 모의기 사본, `hr/s1k/lib` = 효과 도구 ·
경기장 모의기, `hr/s1k/vanilla/` = 경기장 시험이 읽는 26.3 바닐라 블록 태그 몇 개, `hr/sr/srsim.py` = 아이템 · 버프 도우미). 실행은 다른
스위트처럼 데이터팩 밖의 사본에서(`cp -a <저장소>/roguelike/tools/dev/sim <작업>/sim`, 그 안의 `hr/tests` 에서). `<dp>` = 시험할
`roguelike/`, `<rp>` = 풀어 둔 리소스팩. 경로 상수: `ev_dry.py` · `test_rig.py` 의 기본값만 옛 스크래치패드(`--dp` / `--rp` 로 준다),
`test_special_hr.py` · `ident_hr.py` 는 기준 커밋을 `/home/user/rlk` 에서 읽는다(`git show` · `ls-tree`).
11-06 릴리스 게이트(V-I)에서 모두 다시 통과(개수는 `roguelike/README.md` 「홍련」 절의 「릴리스 게이트」 줄; `ident_hr` 는 이때부터 릴리스
도장이 바꾸는 `pack.mcmeta` 를 허용 목록에 둔다). 이 보스의 계획 · 계약 · 단계 브리프 · 요청 · 검토 문서(`hr/PLAN.md` · `hr/contract.md` ·
`hr/stage_briefs.md` · `hr/requests/` · `hr/review/findings.md` · `hr/review/bal/` 의 README 와 S5 결과 로그 · `hr/i1/i1_notes.md`)도 11-06 에
같은 상대 경로로 옮겼다(그 안의 `HR/…` = 옛 스크래치패드 `hr/…`; 균형 탐침의 스크립트 · 모의기는 옮기지 않음).

| 파일 | 실행 | 무엇 (I1 결과) |
|---|---|---|
| `test_special_hr.py` | `<dp>` | 특수 보스 틀 FN-a `winWord` · FN-b 보상 훅 · FN-c `poof` · FN-f 보스바 끄기, 레지스트리 검사, 음악 묶음, 켜기 전 / 뒤 트리(그녀가 켜져 있으면 S1 때의 `ident` 절과 R2b 는 건너뜀 — `ident_hr.py` 가 대신) |
| `test_rig.py` | `--dp <dp> --rp <rp> [--rebuild]` | 리그 계약(29부위 · 47클립 · 호출 · 앵커) · 소환 · 모델(유령 쌍둥이 · 갓 테) · `item_sword` · 모든 클립의 키(바닥 · 120도 · 컬링 · 소품 방향) · mcsim 실행 · 색 거리 · 영상 클립의 이벤트 상태 52곳 · 넘겨 주는 자세; S2c · S2d(I2, 매니페스트에 S2d 항목이 있을 때): 스킨 · 몸(아바타 모델과 같은 상자 · UV, 슬림 팔) · 뼈대 · 계약 값 = 빌드가 잰 값 · 접촉 · 공중 · 칼날 매 틱 · 든 소품 · 갓 · 섞여 들어오기 · 등장의 바위 · 각도 보존(`scarlet_retarget.mjs --dump`) · 리타깃 표 · 결합; `--rebuild` 는 리그 생성기를 두 번 실제로 돌려 바이트 비교(I2: 152); F-I: 아이템 정의의 `display_context` 고르기와 슬롯 아이콘 `item_sword_icon`(GUI × 2 에서 양 끝 모서리 줄 말고 줄마다 2 px 이상 · 100 px 이상 · 한 덩어리, 슬롯 안, 긴 부분 2 GUI px 이상, 바닥 변환), 코등이 카드 자리(HR-03), CS3(5 %) → CS4 이음매(몸은 맞물리고 머리 ≤ 0.25칸, 갓은 0틱 하드 컷 밑에서만, HR-31) |
| `ev_dry.py` | `--dp <dp> [-v]` | 시퀀스 8개의 가짜 Writer 빌드(효과 도구 켜고 / 끄고, 두 번 같음) · 참조 · 정적 규칙 · 틱 · 대사 · 음악 · 모습 · 경고 띠 · 신호 · mcsim 시운전(이벤트 두 갈래, 매 틱 `cancel`, 건너뛰기, CS4 거리) · 장식 달무리의 밝은 모습(`p1b` / `p2b`: 등장 112~146 · CS4 690~780, 건너뛰기 · 취소 때 되돌림) · 던지는 칼의 크기 · 반지름(`seq.S0` · `SWORD_R`)과 손에서 나오는 자리(매니페스트 `item_sword.toss_offset`, S2d; I2: 68); F-I: CS4 0틱의 하드 컷(`seq.SEAM_CUT`, HR-31) |
| `test_scarlet.py` | `<dp> [절 …]` | 코어: 훅(앉는 돌 자리는 명령마다 소수점까지 그대로: `hooks` K3b — 게임은 소수점 없는 x · z 를 블록 가운데로 옮기고 모의기는 쓴 그대로 읽음) · 단계 순서 · 바닥 · 무적 · 실드 · 판정 · 쓰러짐 · lead-in · 건너뛰기(`skip`: 끝 상태가 전체 등장과 같음, 거리 포함) · AI · 멈춤 / `/reload`(시계 `#sq -1`) · 정리 · 배경 효과의 박자(`phases` P14 · P15: P1 10틱 · P2 쪽 6틱, 장면 중 없음) · 모습 작업마다 장식 소품(`look` L5) · CS4 거리(`cs4`) · 틱 비용(`cost`: 효과 도구도 진짜로 돌려(`kit_on`) 단계별 평균 · 최대 · 효과 도구 몫, 조각 틱 따로); F-I: `cleanup` C3(이긴 · 멈춘 · 정리 뒤 목표 hr 에는 이벤트 점수만, 저장소 `seq` 없음 — F3 요청 r5); V2(HR-50): `cost` 가 쓰러짐(타이머 · 5 % 바닥 → lead_down), A8 · A13 실패 갈래(되살아남 → lead_stand → A13), 멈춤 · `/reload`(A8 판정 직후 · P2 · 쓰러짐)까지 재고(Z5: 모두 닿음), Z4(HR-51: 이미 그 모습인 경기장에 모습 작업 없음) · Z6(HR-52: CS0 동안 킷의 틱마다 소품 사슬이 안 돎); `look` L6(HR-51: 도장이 요청한 모습이면 작업 없이 장식만) |
| `pat_p1.py` · `pat_ghost.py` | `<dp> [key …]` | 1 · 2페이즈 패턴과 연참: 타격 틱 = 클립 이벤트, 모양 · 등급 · 넉백, 예고 ≥ 12 / 20틱, 겨눔 고정, 끝점(`mv/ok`), 유령 창, 원반(틱당 1.75칸), 베기 9번 · 대시 에이전트 · 실드 · 판정 · 스위치, 매 틱 취소 |
| `test_reward.py` | `<dp>` | 이벤트 뽑기 · 중복 규칙 · 지급(E56) · 보상 훅 · `/reload` 한 번만; `real` 절은 SR 의 진짜 아이템 · 버프 파일로(칸이 가득하면 발밑 드롭); F-I: 버프 갈래 · `scope` 의 액션바 글자에서 코다 첫 틱의 빈 액션바(F2 의 `seq.HUD_BLANK`)는 셈하지 않음 |
| `test_kit.py` | `<dp> [<rp>]` | 효과 도구: 계약의 이름 · 인자, 모듈이 부르는 모든 킷 호출(합친 트리면 그 트리의 모듈, 킷만 있는 트리면 `wip/hr-s4` · `wip/hr-s2b` 를 임시로 빌드), 카드 엔진 · 풀, 프리셋 높이(I2: 플레이어 크기 몸의 부르는 높이, S2d 요청 s2d-3) · 수명 · 색, 소품(앉는 돌 위의 병 · 잔 0.19칸 위 이상, 달무리 `p1b` / `p2b` 의 밝기 비 포함), `leaves_dark` 의 음수 `n`(뒤쪽 잎: `{n:20}` + `{n:-20}` = 40장), 정리 · 제거, 바닐라 소리, HUD, RP 를 주면 그림 · 아틀라스 · 글꼴; F-I: 보기(`view`) 카메라는 S2d 몸의 가슴(모듈 기본 효과 높이 1.0칸)을 봄, A1 부채의 F5 바닥값 165 px(S2d 의 작은 부채), 롤 90 쐐기 변형의 길이 × 0.78; V2(HR-48): A1 의 효과(부채 · 초승달)는 7틱 중 3틱 이상에서 두 시점 모두 1 500 px(부채의 F5 는 250 px), 다른 효과는 최댓값; (HR-52) 앉는 돌의 병 · 잔은 틱마다 도는 `e/anim` 밖(10틱마다 `e/stay_t`), `bare` 로 바로 사라짐 |
| `test_arena_hr.py` | `<dp>` | 경기장 `hr_field`: 명세 = 레지스트리 · 걷는 원 · 방벽 · 빛 · 식물의 받침(`hr/s1k/vanilla` 태그) · 모습 셋의 절대 채우기 · `dark` 3틱 간격 · 조각 한도 · cmsim 으로 실제 짓기 · `ensure`; V2(HR-55): 1e 의 두 번째 인터프리터는 `-B`(1f: 시험한 트리에 바이트코드를 쓰지 않음) |
| `test_hwamu.py` · `test_moon.py` | `<dp> [절 …]` | 아이템 화무십일홍(정의 · 등록 · 풀 밖 · ★ 표 · 세 효과 · 정리 · 틱당 명령 수) · 버프 월하대작(stat_buffs · × 1.20 · reset · uninstall · 스탯 줄). `test_hwamu` 는 계획 `PLAN.md` 와 저장한 위키 `wiki/w2.txt` 를 `$HR_DOCS` 나 스위트 옆(`hr/`)에서 찾고, 없으면 그 글과 맞추는 검사만 건너뛴다(끝에 `SKIPPED` 목록) |
| `ident_hr.py` | `<dp> [--base 35b82e5]` | 11-03 트리 `35b82e5` 와 바이트 비교: 계약 §5 허용 목록 · SR 손 파일 · `boss/scarlet/**` · 이 보스의 매니페스트 밖은 같아야 함(11-10: 전투 개편 lane R 이 바꾸고 · 더하고 · 지운 파일 묶음 `LANE_R` 을 더함 — 지운 파일이 허용되는 묶음은 이것뿐; 다른 레인도 자기 묶음을 더한다) |
| `gen_check_hr.py` | `<dp> --rp <rp>` | 복사본(`tmp/`)에서 이 보스에 닿는 생성기(코어 · 경기장 · 리그 · 킷 · 모듈 · 검사)를 두 번 · 정해진 순서 / 거꾸로 · 소유 경로만 쓰는지 · 리그와 킷의 RP 쪽 두 번 |

- `hr/tests/lib/hrsim.py`(I1b 검증 1차): `kit_on(s)` 이면 효과 도구(`boss/scarlet/fx/**`)가 대역 없이 진짜로 돈다(`azsim` 의 KITS 처럼;
  카드 관리 `fx/e/world` 는 바닐라처럼 예약한 틱 안에서, 같이 부르는 `view/ttl_blank` 도 진짜) — 모듈이 부르는 킷 호출 243가지(`uninstall` 빼고)가 킷 자체 시험틀
  (`hr/s1k/lib/hrfxsim.py`)과 명령 수까지 같다. `s.kit_hist`(틱마다 효과 도구 몫), `kit_ex(s, 이름)`(킷 호출의 실행자 태그 · 부른 함수 · `#ph`).
- `hr/tests/lib/hrsim.py`(I1): `#rlk:dash_pass` · `#rlk:cm_pass` 를 데이터팩의 태그 파일대로 푼다(26.3 의 `#minecraft:replaceable` 포함) —
  사본 `cmsim.py` 는 공기와 빛만 통과시켜, 경기장의 마른 풀 · 진홍 뿌리 칸에서 `mv/ok` 가 막혔다(게임에서는 통과).

### 3-5. 전투 개편 lane R (`cb/tests/`; 11-10, 가지 `wip/combat-rm`)
`python3 test_rm.py <dp> [static yoi view picksub]`(데이터팩 밖 사본에서). 모의기 `cb/tests/lib/psim.py` + `lib/mcsim.py` = 전투 개편 조사의
하네스(`tools/dev/plan/combat/perf_harness/psim.py`, 그 mcsim = `ar/tests/lib/mcsim.py` 에 값 없는 점수를 0 으로 읽는 판)를 복사해 둔 것이고,
고친 곳은 두 가지(같은 폴더의 mcsim 을 읽음, 값이 그대로인 `data modify storage … set` 은 게임처럼 0 을 돌려줌). 진짜 `rlk:load` · `rlk:player/tick` ·
`lvup/pick_sub` · `view/tick` 을 돌린다.

| 절 | 무엇 |
|---|---|
| `static` | 요이미야 · 활 파일 · 호출 · 점수판 · 생성된 `px/db` 의 `aurEnd` 줄이 없음, 로노바 · 클로린드의 투사체 틀(`char/bow/arrow_*` · `assist` · `calc`)은 남고 종류 7 · 8 만, F(`player/f_key`)는 조준 켜기가 아님 |
| `yoi` | 저장 월드 이전: 요이미야로 저장 → 다시 켬(플레이어 없이 load) → 루미네 · `start_char` · 선택지 / 떨굴 목록에서 카드 뺌 → 접속한 플레이어의 틱에 한 번 다시 고르기(무기 · 조준 감속 · 사이드바 · 바닥 카드), 다른 캐릭터로 저장된 월드는 목록만 |
| `view` | F5 하나: 모드 · 숄더뷰 파일 없음, 로비 「시점」 버튼 없음 · `built` 12, `#on view 1` · `#vmode view 2` 는 load 의 고정값(생성된 파수꾼 줄만 읽음), 1인칭 · 숄더뷰로 저장된 월드 → F5(옛 카메라 저장값 지움, 다음 틱 아바타 길), 개발자 모드는 `view/fps_tick` |
| `picksub` | 「고를 아이템 N개」가 방 전투(`#active room 1` + `#combat room 1..`) · 보스 엔진(`#mbLive mb 1`) 동안 안 뜸, 싸움이 시작되면 바로 지움(아랫줄만), 끝나면 20틱 안에 다시 뜸, 싸움 중 레벨 업, 예전 규칙(선택 공간 · 사망 · `ttlT`) — 바꾸기 전 트리에서는 5개 실패 |

### 3-6. 전투 개편 검토 B 의 고침 (`cb/tests/`; 11-11, 가지 `wip/combat-fix-b`; `tools/dev/plan/combat/fb_progress.md`)
데이터팩 밖 사본에서. 보스 쪽은 `hr/tests/lib`(아를레키노는 `ar/s3/lib`), 몹 쪽은 `bal/tests/lib` 의 모의기를 읽기만 한다.

| 파일 | 실행 | 무엇 |
|---|---|---|
| `hzlog.py` | `<dp> <보스> pat [--ids=..] [--dodge] [--stand] [--out=f.json]` · `<dp> <보스> fight [--ticks=3000] [--out=f.json]` | 하네스(검토 B 의 `hzlog.py` 를 `repro` 대로 다시 만든 것): 보스 하나(guardian butterfly fieldgen azhdaha apep tachy arlecchino)를 실제 틀 · 모듈로 싸우게 하고 위험 지대(`hz/init` 뒤의 종류 · 닿는 거리 · 예고 · 피해 · 닷지 불가 · ‰ · 다시 맞기 · 패링 불가 · 묶음 · 만든 함수 · 타격 틱), 투사체, 모듈의 직접 타격, 경고 섬광(틱 · 자리 · 바닥 위 높이), 판정에 닿은 타격(피함 · 잃은 체력), 틱당 명령 수를 JSON 으로. `pat` = 시험 번호마다 새 싸움, `--dodge` = 매 틱 퍼펙트 닷지, `--stand` = 패링 불가 · 닷지 가능 위험 지대가 예고되는 동안 플레이어를 그 안에 세움(먼저 터지는 것부터), `fight` = 매 틱 회복되는 가만히 선 플레이어 |
| `np_table.py` | `<기록 폴더> <tag> [보스 …] [--cmp=<다른 tag>] [--json=f]` | 그 기록(`<tag>_<보스>_{pat,dodge,stand,fight}.json`)으로 보스별 표(패턴마다 모양 · 상태 P / U / U-ND / U-field · 섬광에서 타격까지 틱 · 매 틱 닷지로 피한 수), `--cmp` 는 두 tag 의 `fight` 기록 비교(패링 불가 표시 말고는 같아야 함) |
| `test_np.py` | `<dp> [fw b08 b09 mobs table] [--logs=<폴더> --tag=<tag>] [--jobs=N]` | 고침의 검사(6522feef5 에서는 실패): `fw` 기본 규칙 · 옵션 · `np_auto` · 문 · 섬광 자리 · 묶음의 답, `b08` 타키 그로기 바닥, `b09` 아펩 치워 둔 몸, `mobs` 궁수 화살 · 시킨(자식 프로세스), `table` 일곱 보스의 `hzlog` 기록(직접 돌리거나 `--logs` 로 재사용: 패링 불가 패턴 = 판정 목록, 섬광 ≥ 20틱 전 · 바닥 위 1칸 이상 · 닷지 불가 / 장판에는 없음, 한 묶음 · 한 타격에 답 하나, 매 틱 닷지로 모두 피함, 연달아 닷지해야 하는 불가 타격의 간격, 그 지대 안에 세운 플레이어도 모두 판정 · 회피) |

### 3-7. 전투 개편 검토 A 의 고침 (`cb/tests/`; 11-11, 가지 `wip/combat-fix-a`; `tools/dev/plan/combat/fa_progress.md`)
`python3 test_cb.py <dp> [static input lock judge tiers dodge cool context energy cd bal boss near raiden readers fx bossloop cost]`
(데이터팩 밖 사본에서; lane C 의 스위트에 더한 것). 틀이 달라진 점: 입력은 `rlk:tick` 의 앞 단계 줄(`#now` · `player/def/input` · `#dgOpen` · 상자 줄)을
파일에서 읽어 그대로 실행하고(`prepass`), 모의기에 `rotate` · `kill` 의 결과 수 · `data merge` 의 Glowing · `x_rotation` · interaction 의 진짜 클릭
자료(psim 은 엔티티 자료 검사를 모두 참으로 답해 눈앞 실드가 매 틱 "클릭"되었다)를 더했다. 실패가 삼켜지지 않게 `no_errors` 가 패링 · 닷지 함수의
모의기 오류 목록을 본다.

| 절 | 무엇 (검토 A 의 어느 것) |
|---|---|
| `input` | 진짜 F · 우클릭 경로, 누르고 있는 아이템 사용 우클릭(A-02), F + 우클릭 한 틱(A-08), 도장 없는 플레이어의 첫 닷지와 시작 자리 상자의 정리(A-07) |
| `lock` | 헛누름 연속 12 / 24 / 36 / 48, 무시된 F 뒤 3틱, 1~2틱 연타는 한 번, 3~40틱 모든 주기와 불규칙 간격의 퍼펙트 창 비율 · 실제 타격 229번(리뷰어의 루프), 정당한 플레이(10~40틱 연쇄의 h − 1, 3틱 · 2틱 연속기의 모든 박자), 실수 하나의 값, 연타로 연속기 통과(A-01) |
| `cool` | 닷지 재사용 대기 18 / 피하면 12(한 번만 돌려줌), 질주 2 = 14 / 10, 재사용 대기마다 누르는 닷지의 루프(A-12) |
| `fx` | 만든 틱에 나이를 먹어도 효과가 제 길이(A-05), 잔상은 먼 청크로 옮겨진 뒤에만 kill(A-03) · 몸의 yaw(A-06), 덮개가 끝나는 틱의 조준점(A-09) |
| `bal` | 퍼펙트 패링의 균형치는 적의 자리에서(B-05) |
| `bossloop` | `bossloop_cb.py <dp> [보스 n]`(자식 프로세스; `hr/tests/lib` 의 azsim 을 읽기만 함): 실제 중간보스 전투의 월드 루프에 `rlk:tick` 의 앞 단계 줄과 `mboss/near_all` 줄을 넣어, 앞 단계가 매 틱 · 근접 재판정이 창이 열린 틱에만 돌고, 몸이 떠난 닷지가 근접 재판정으로 퍼펙트 닷지가 되며, 몸 표시가 매 틱 제자리로 돌아오는지(A-11) |

실제 26.3 서버 탐침은 스위트 밖: `tools/dev/plan/combat/fa_probe/`(`probe.sh` · 탐침 팩 `rvp` · `parse.py`, 고치기 전 / 뒤 결과).

## 4. 균형 탐침 (`ar/review/bal/`, `ap/balance/azfair_core.py`)
- `knfair5.py <dp> <mode> <policy> <dodge> <char> <seed> [n] [lv] [plv] [out.json]`: 아이템 없는 Lv15 플레이어 대 L18 보스,
  `mode` = `p1a` / `p1b` / `p2`(10만 체력 보스로 그 단계만 n틱) / `whole`(진짜 체력으로 끝까지), `policy` · `dodge` 는
  `azfair_core.py` 의 것(쓴 조합: `melee:walk` · `melee:none` · `ranged:walk`; 칼 `sword` / 활 `bow`), 시드 11 · 22 · 33.
  조용한 판정은 자세를 보고 12틱 먼저 알아챈다고 친다(`KN_LEAD`). 사람 대역 에이전트는 아펩 때의 `azfair_core.py`(위협
  읽기 · 피할 곳 찾기 · 점프 · 대시 시점; 파수꾼 수치를 재현). `KN_ORB=1` = 생명의 계약 중 회복구슬을 주우러 가는 에이전트,
  `KN_API='<json>'`(+ `KN_PMX=1`) = api 표를 메모리에서만 바꿔 보는 what-if(파일은 안 씀).
- `batch5.py <label> <dmgMul|-> <mode:policy:dodge:char,…> [jobs]` → `out/<label>/*.json`, `analyze5.py <label…>`: %최대
  체력/분을 아펩 기준(P1 근접 걷기 127.7 · 근접 안 피함 132.2 · 원거리 걷기 78.7, P3 94.4 · 186.5 · 92.8)과 비교, 최악 40틱
  창(Q5B 마지막 일격 포함 / 제외), 구슬 · 파훼 · 사망. `run_pass.sh` · `run_final.sh` = S5 에서 돌린 그대로.
- 11-02 결과: P1 근접 걷기 1.15 × 아펩 P1, P2 걷기 + 구슬 1.00 × 아펩 P3, 최악 40틱 42.9 %, 회복 안 하는 걷는 플레이어도
  연회 두 번을 버팀.
- 옛 보스의 공정성 모의(11-03 에 기록으로 옮김: 보스 절 · 생성기 주석이 수치의 근거로 듦; 옮기지 않은 스위트의 모의기를 import 하므로
  그대로는 돌지 않는다): 나비 `mb2/balance/`(`bal.py` → `fsim.py`; `mb2/tests` 의 `bfsim`), 역장 `mb3/fgfix/sim/`(수정 라운드) ·
  `tele/fg/sim/`(10-20 × 1.5 다시 돌림)의 `fgfair.py` · `batch.py` · `analyze.py`(`mb3/tests` 의 `fgsim`; 결과 `*.log`), 타키
  `tk/review/bal/tkfair.py`(`tk/s3/lib`; 결과 `*.log`), 아펩 `ap/balance/`(`apfair.py` · `batch.py` · `analyze.py` · `breakdown.py`,
  `ap/tests/lib` 의 `apsim`; 표 `analysis.txt`, 자기 `README.md`).

## 5. 그림 도구
- `preview/raiden_preview.py`(numpy z-버퍼 래스터라이저: summon / data merge / tp / function 을 해석하고 RP 의 아이템 정의 ·
  모델을 읽어 PNG) + `az/understand/rigtech_render.py`(UUID 선택자 패치; mboss 형 리그는 이것으로):
  `python3 -I az/understand/rigtech_render.py --dp <디버그 dp> --rp <rp> --spawn rlk:boss/<id>/rig/spawn --apply <함수…> --views front,right,iso --light mc -q -o out.jpg`
  (`--strip a..b:step` 필름 띠, `--extent` `--center` `--cols` `--width` `--title`). 디버그 dp = 리그 생성기의 `--debug-dp <폴더>`.
- `ar/s2/`: 리그 그림 묶음 — `b.sh`(디버그 빌드) · `pose.mjs` + `pv.sh`(자세 하나) · `strip.sh` / `strips_all.sh`(클립 띠) ·
  `u1.sh`(U1 시트: 정면 · 옆 · 뒤 · 3/4) · `introcmp.py` / `pairs.py`(영상 프레임과 나란히).
- `ar/s1k/render/render_kn.py <dp> <rp> <out>`(+ `render_kn_core.py` 카드 광선 추적) = 효과 도구 시트, `ar/s1k/quicksheet.py
  <rp> <out.jpg>` = 스프라이트 시트, `ar/review/rend/final_fx.py` = 11-02 `final_fight.jpg` 의 효과 칸(경로가 6줄에 박혀 인자를 안
  받음 — 1절 표).
- `ar/tools/`(ffmpeg + Pillow; `sheet2` · `picks` · `capat` · `captions` 는 임시 프레임을 `../tmp` 에 만들고 지움(미리 있어야 함), 결과는
  인자로 준 `OUT.jpg`; 영상은 `picks.py` 만 `../src/<vid>.mp4` 에서 읽고 `sheet2` · `capat` · `captions` 는 첫 인자 `VIDEO` 경로): `sheet2.py VIDEO START END STEP OUT.jpg` 시간 간격 시트 ·
  `picks.py OUT.jpg cols thumbw vid:t[:x,y,w,h] …` 골라 뽑은 프레임 · `capat.py` / `captions.py` 자막 영역 · `skinview.py`
  스킨 앞뒤 · `html2txt.py` 저장한 위키 HTML → 글.

## 6. 옮기지 않은 것 (옛 스크래치패드에만 있음; 11-03 컨테이너에는 아직 있지만 새 컨테이너에는 없음)
`tools/dev/sim` 에 없는 옛 경로는 옮기지 않은 것이다(`roguelike/README.md` 0-7 끝 · 0-8).
- 다른 보스의 스위트: 타키 `tk/tests`(약 370 KB, `tk/s3/lib` · 서버 jar 안쪽 jar 필요), 아펩 `ap/tests`(약 460 KB),
  야타용왕 `az/tests`(`test_wire_az.py` 의 H2 / H3 는 1챕터만 라우팅된다고 가정해 낡음) · `az/harness`, 나루카미
  `rd/tests`(약 300 KB; `--strict` 예산표 `plan_table.json` 이 11.0 M 으로 낡음; `test_kit` 이 읽는 `sound_ids.txt` 만 옮김), 중간보스 `mb/int_tests` · `mb2/tests` ·
  `mb3/tests`(+ `bf_base`, `fxtests`), 2 · 3챕터 몹 `ch2/tests_a|b` · `ch3/…`, 문 높이 `doors`, 손 소품 `heldfix`, 단계 · 효과 킷
  스위트(아펩 `ap/{rigtests,orgtests,fxtests,tests_arena}`, 야타용왕 `az/{fxtests,tests_pa,tests_pb,tests_pl,tests_ps,tests_pt,tests_rig,
  tests_arena,tests_mod}`, 나비 · 역장 `mb2/fxtests` · `mb3/fxtests`).
- 이전 단계의 균형 탐침(`ar/s3/bal/knfair.py`, `ar/s4/bal/knfair2.py`: `knfair5.py` 가 대신함).
- 작업 폴더: 렌더(`*/renders` · `ap/arenarender` · `az/arenarender` · `ap|az|mb3/fxrender`), 리그 작업(`ap/rigwork` · `az/rigwork` ·
  `ap/orgwork`, `riglib/` 의 나머지), 검토 작업(`mb3/review`, `mb2/review` · `mb2/integ` · `mb3/fgfix` 의 나머지), D0 작업 도구 `ap/spec/`.
- 계획 · 계약 문서는 `roguelike/README.md` 0-7 목록에 적은 것만 옮겼다: `ap/` · `az/` 의 계획 초안 · 비평 · 원장(`plan_draft.md` ·
  `plan_crit_*.md` · `plan_ledger.md`)과 단계 메모(`ap/i1_notes.md` · `final_summary.md` 등)는 옮기지 않았다.
- 출력 · 로그 · 그림 · 영상 · 기준선 큰 파일.
