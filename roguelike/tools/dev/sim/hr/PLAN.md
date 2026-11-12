# 홍련 (Scarlet) — special boss: implementation plan

Scratchpad `S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`, `HR` = `S:hr`, repo
`R:` = `/home/user/rlk/roguelike`, `F:` = `R:data/rlk/function`, `T:` = `R:tools`. 20 t = 1 s. Footage times are `vN t`
= clip N at t seconds (60 fps, 1 tick = 3 frames, `fF` = frame F); `T+n` = n ticks after a pattern's T0. Inputs are cited
as `file §`: `patterns.md`, `cutscenes.md`, `questions.md`, `critic.md` (its corrections override the others),
`framework.md`, `model.md`, `arena.md`, `v1.md`…`v5.md` in `HR/understand/`; wiki `HR/wiki/w1.txt` (Stellar Blade boss
page), `w2.txt` (NIKKE page), `digest.md`. Sheets are in `HR/ref/` (≤ 640 px jpg, tiles labelled `vN t fF`). Precedents:
`S:tk/PLAN.md` (타키, the special-boss template), `S:ar/PLAN.md` / `contract.md` / `stage_briefs.md` (아를레키노). The
repository's handover doc is `R:README.md` chapter 0 (pipeline 0-7, gates 0-5, user rules 0-6).

User request (KO, verbatim): "특수보스로 스텔라블레이드의 '홍련'이라는 보스를 만들거야. 이 보스는 원작에서 쓰러지는 모션이
없고 전투 중간중간에 컷신이 나오는데, 컷신은 최대한 비슷하게 만들되 전투가 끝나면 원작과 같은 대사랑 연출을 하고 나서 특수한
이벤트가 일어났으면 좋겠어. (+아이템 1개 지급) / 이벤트는 다음 중 랜덤하게 일어나. / 1. 특수 아이템 지급 — [ MYTHIC ]
화무십일홍 — 능력은 이후 보낼 나무위키 페이지들 보고 구상 / 2. 영구적인 버프 - 내용 구상". Binding rules for this boss on top of
README 0-6: the rig and the arena are an ORIGINAL design (§1.5); her lines come only verbatim from the supplied wiki pages /
footage subtitles (§3.0). §7 (ending → reward → random event → item → buff) was written separately (`HR/plan/reward.md`,
kept as the original) and is merged here. §11 logs what the two critiques (`HR/plan/critique_fidelity.md` = FI-n,
`critique_feasibility.md` = FE-n) changed.

---------------------------------------------------------------------------------------------------------------------

## 0. Decisions at a glance

| topic | decision | source |
|---|---|---|
| registry | new `kind:"special"` entry `scarlet` (n 21, `fn:"boss/scarlet"`), arena `hr_field` (n 5, `#mbAr 5`). Rift-only like 타키, chapter mode (`#mbMode 1`, `#mbKind 2`), `enabled:false` at D0, I1 flips it | framework.md §1, §5 |
| names / numbers | prefix `hr`: objective `hr`, rig `hrRig*`, kit `hrFx*`, tags `rlk_hr_*`, storage `rlk:hr`, RP `rlk:mboss/scarlet/*` (rig) + `rlk:mboss/hr_kit/*` (kit), font `rlk:mboss_hr` U+EC00-ECFF, rig UUID `524c4b4d-4852-4400-8000-0000000000NN` | framework.md §5 |
| name / sub / colour | 「홍련」 / 「월하곡」 (the line under her name on the original result panel, v5 23.17) / `#E8466A` | cutscenes.md §9 |
| element | Electro (`el 3`): every hit Electro 1U (her NIKKE code is 전격, her sword-qi is light purple); `res {"*":10}`, no immunity, no element-gated shield | framework.md §5, README 0-6 |
| look | ORIGINAL design: a Joseon wandering swordswoman with a red-lotus motif — flat-brimmed horsehair hat with a crimson lotus knot at the back of the band, ivory long robe + ink-violet vest, black hair with a crimson ribbon, long single-edged sword drawn left-handed from a black-lacquer scabbard; lilac sword-qi; the original's distinctive pieces are not reproduced (§1.5, §2.2) | user rule, model.md §1-§3 |
| size | 2.55 b to the head top (×1.42 the 1.8 b player), 2.82 b to the hat crown, brim Ø 1.60 b; husk `scale 1.35`, click shield `hit {w:1.2,h:2.9}`, no hit proxies | model.md §1, 타키 lesson (README 0-6) |
| phases | intro CS0 → **P1** (100 → 60 % floor) → **CS1** 홍련일섬 + arena turns crimson → **SQ1** → **A8 gauntlet** (5-pip shield) → success: **CS2** repelled → **down** 200 t; fail: heavy non-lethal hit → **P2** (→ 5 % floor) → lead-in → **A13 ultimate** → success: **CS3** → scripted lethal hit → **CS4 ending** → §7; fail: instant death | patterns.md §10, cutscenes.md §1 |
| P1 patterns | A1 회전 반월참 and A2 역습 일섬 (counters), A3 오연 반월, A4 월하 낙참 + A5 공중 원륜, A6 후방 섬보 (+ bark), A9 황광 원참, A10 황광 낙참 | patterns.md §2-§6, questions.md Q-A2 |
| P2 patterns | the P1 kit with the same moves and timings, shorter recoveries and lilac afterimages, + R1 자영 돌격, R2 월륜 일섬, R3 자영 활강, assembled only from footage moves | questions.md Q-A1 (question 5) |
| gauntlets | A8 (60 %) and A13 (5 %): darkness from T0−17, lilac ghost, 9 ghost cuts + the final dive (A13 adds 3 moon discs), she is invulnerable; footage timings stretched to the telegraph rule | patterns.md §5, critic.md C30-C58 |
| shield / pips | 5 pips; one removed per **well-timed dash** at a counting ghost cut (the dash's i-frames on at the strike tick, the player near the cut's lock point — independent of the dash direction, §5.1); judged at the final dive (0 pips → deflect → counter cinematic) | framework.md §4.2, Q-B1 (question 6) |
| fail at 60 % | non-lethal: the dive lands for 500 ‰ max HP (cannot kill) + a push, no counter, no down window, straight to P2 | Q-A6 (question 6) |
| fail at 5 % | instant death through dash i-frames and shields (Ronova's revive applies); a warning banner (instant-death exception) | Q-B2 (question 6), README 0-6 |
| telegraphs | no floor decal anywhere (the footage shows none); quiet tells ≥ 12 t, ≥ 20 t for big / undodgeable / yellow; chains ≥ 10 t apart; aims lock 7 t before the hit; the yellow tell kept for A9, A10, A7 | critic.md C70, Q-B7, Q-B8, Q-B14 |
| lines | 25 verbatim lines: 23 in the fight (11 encounter, the bark 「거기가 아닐세.」, 4 enrage = wiki 1-2 + the footage split of 3, 7 clear) + 2 NIKKE lines in §7's coda (w2 l.405 / l.298); none invented; 「어림없다」 not used | cutscenes.md §11, critic.md §3, w2 |
| on-screen text | name, sub, typed lines, the instant-death warning banner, the intro's skip prompt 「⊙ 건너뛰기」 (the original's, verbatim), §7's item / buff names, numbers and notices; no pattern names, no tips | README 0-6 (10-21) |
| camera | none (the convention of every boss, not a question): one-shot facing + framing by position; black / negative-like / pink-white / tint flashes as full-screen title glyphs | framework.md §2.6, Q-B4 |
| cutscenes | CS0 640 t (all 11 encounter lines; holding Shift 20 t skips to line 11, as the original's skip does), CS1 213 t, SQ1 60 t, CS2/CS3 104 t (boss-only "repelled" clip), lead-ins 70/82 t, CS4 1042 t (std) + §7's coda 120 t | cutscenes.md §1-§8, Q-A14 / Q-A17 (question 7) |
| arena | `hr_field` 「달빛 억새밭」: a moonlit silver-grass field (walk r 25) — ORIGINAL, asymmetric composition: a wide lotus pond on the moon side with a rock-islet lotus stone lantern, one old pine leaning over the water, the moon in open sky beside it, bamboo and cherry groves, low stone walls; no stair, no pair of masses framing the moon; looks `moon` (P1) → `crimson` (P2, red moon) → `dark` (gauntlets) | arena.md §1-§7, user rule |
| music | P1 `music.overworld.cherry_grove` (a pool: `len 0` from D0, S1 measures its tracks, FN-e), P2 `music.nether.crimson_forest` (6076), ending `music.overworld.cherry_grove` once | Q-B17, framework.md FN-e |
| difficulty | ≈ 타키: `hp 260` (S5: 타키 250 + 4 %), `atk 12`, `dmgMul 135`, `lvAdd 1`, tiers T1-T4 = 29 / 42 / 62 / 71 % (타키's final, T3 + 10.7 % by S5); S5 targets and results in §4.8 | README 타키, framework.md §6.13 |
| reward / event / item / buff | §7; defaults given to the build: level up 1 + 1 item pick + the random event, 50 % 「[ MYTHIC ] 화무십일홍」 / 50 % the buff 「월하대작」 for the rest of the run | task, questions 1-3 |
| rift share | `w` 10 = 타키's (equal weight; one rift per run) | question 4 |
| framework changes | FN-a reward word per special, FN-b optional per-special reward hook in `sp/reward`, FN-c no `poof` at `death_finish` per entry (§7.1), FN-d the arena entry n 5 (D0) + its theme (S1K), FN-e cherry-grove pool lengths, FN-f a bars-off flag so a module can hide the boss bars mid-fight (S1) | framework.md §1.11, FE-6 |
| budget | items atlas ≤ 0.43 M px of the 0.57 M left (rig ≤ 0.15, kit ≤ 0.26, gate icon ≤ 0.005; §7 plans 0 px, its 0.015 M stays a reserve) → stitched ≈ 13.06 M ≤ 13.2 M; ≈ 7 400 functions / ≈ 21 MB incl. §7 (§9.6) | framework.md §2.5, README 0-5 |

### 0.1 Open questions for the user (1-4 = the four questions already sent, same numbers; 5-7 = design questions; each of 1-7 has a default the build proceeds with and is one switch; 8 = a consent README 0-2 requires before any server test)
1. **영구적인 버프는 얼마나 가나요?** 기본: 이번 판(런)이 끝날 때까지(생명력 노드와 같은 방식). 다른 안: 판이 끝나도 남음 — 이 팩의
   첫 영구 성장(지금 판을 넘어 남는 것은 사파이어뿐)이라 수치를 낮추고(최종 공격력 +8 % · 치명타 확률 +4 % · 이동 속도 +4 %) 한 번만
   받습니다. (`EVENT['buff_scope']`, §7.5.3)
2. **보상 구성.** 기본: 레벨 업 1 + 아이템 선택 1 + 무작위 이벤트. 다른 안: 특수 보스 기본값(레벨 업 1 + 아이템 상자 3)에 이벤트를
   더함. (`picks`)
3. **이벤트 확률.** 기본: 「[ MYTHIC ] 화무십일홍」 50 % / 영구 버프 「월하대작」 50 %. (`EVENT['item_pm']`)
4. **균열에서 타키와의 비율.** 기본: 같은 비율(10 : 10). 균열은 한 판에 많아야 하나라 둘 중 하나가 나옵니다. 다른 안: 홍련을 더
   드물게, 2챕터부터, 또는 타키를 만난 판 다음부터. (`w`, `minCh`)
5. **2페이즈 일반 패턴.** 영상에는 없습니다(60 % 반격 뒤 쓰러진 사이에 5 %까지 깎였음). 기본: 1페이즈 패턴을 같은 동작으로 쓰되
   패턴 사이 쉬는 틈만 줄이고, 영상의 환영 연참에서 그대로 떼어 낸 패턴 셋(자영 돌격 · 자영 활강 · 월륜 일섬 한 발)을 더함 —
   영상에 없는 동작은 만들지 않습니다. 다른 안: 2페이즈는 쓰러짐 + 필살기만(영상 그대로), 또는 위키 글만 보고 새 패턴을 구상.
   (`P2_KIT`)
6. **실드 5칸과 실패.** 원작은 퍼펙트 패링마다 한 칸이 깎이지만 이 팩에는 패링이 없습니다. 기본: 환영의 베기를 맞기 직전에 대시로
   피할 때마다 한 칸(베기 9번 중 5번; 어느 쪽으로 대시해도 됨). 60 %에서 실드가 남으면 마지막 낙하 일격이 최대 체력 50 % 피해(죽지
   않음)로 들어오고 반격 · 쓰러짐 없이 2페이즈로 갑니다. 5 %에서 실드가 남으면 즉사(로노바 부활은 적용, 부활하면 필살기를 다시
   함)이고, 즉사기라서 허용되는 경고 띠 「대시로 베기를 아슬아슬하게 피해 실드를 모두 깎으세요 — 실드가 남으면 즉사합니다」를
   5 % 필살기 동안 띄웁니다. 다른 안: 60 %도 즉사(경고 띠도 함께), 5 %도 큰 피해만(경고 띠 없음), 다른 문구. (`PIP_RULE`,
   `ULT60_LETHAL`, `ULT5_LETHAL`, `WARN_TEXT`)
7. **컷신 길이와 건너뛰기.** 기본: 등장 컷신은 다 보면 약 32초(입장 대사 11줄)이고, Shift 를 1초 누르고 있으면 원작처럼
   「낭자 생각은 어떤가?」부터 이어집니다(원작의 「⊙ 건너뛰기」 문구 그대로). 끝 연출은 약 52초(클리어 대사 7줄과 원작의 몸짓 ·
   모자 인사; 칼싸움은 줄임)이고 건너뛸 수 없습니다. 다른 안: 등장도 건너뛰기 없음, 끝 연출 짧게 약 30초 / 원작 길이 약 75초.
   (`INTRO_SKIP`, `END_PROFILE`)
8. **시험 서버 동의(EULA).** 각 단계와 릴리스의 "실제 서버 로드" 검사는 Minecraft 서버를 돌리므로 Minecraft EULA
   (https://aka.ms/MinecraftEULA) 동의가 필요합니다(README 0-2 2번 ②; 11-03 까지 동의 기록 없음). 기본: 동의를 받기 전에는 서버를
   돌리지 않고(단계 작업은 하되 서버 검사와 릴리스는 동의 뒤로), 동의를 받으면 날짜를 README 0-8 에 적습니다.

---------------------------------------------------------------------------------------------------------------------

## 1. Footage study

### 1.1 What the clips are
One continuous YouTube recording, "스텔라블레이드 DLC(니케) 홍련(어려움난이도, 노히트, 퍼펙트패리)" — a Hard, **no-hit,
perfect-parry** showcase — cut into five clips (patterns.md notation; cutscenes.md §0). No boss hit ever connects, so the
footage gives **no damage numbers and no hit boxes**: every size below is the visible sword-qi read through a moving
camera (±30 %).

| clip | content |
|---|---|
| v1 (≈ 40.2 s) | 0-1.88 the intro's opening shot (Eve climbs the entrance stairs, 홍련 a tiny figure at the far stairs; skip prompt from f50, critic C15), black f114, the post-skip end of the intro (line 11, the face reveal, the draw, the stance) to 8.05; control at 8.05; **P1** 8.05-26.30 (A1, A4 + A5, A9, A6 + bark, A2, A10, A3); 26.3-37.28 she is knocked down / far while Eve hits her; **CS1** starts at 37.28 (HUD off) |
| v2 (≈ 40.1 s) | CS1's end (skipped at 1.07; the two subtitles, the petal, the flashes, 홍련일섬, the recolour) to 6.93; **SQ1** 6.93-9.70; **A8 gauntlet** 9.70-19.08; **CS2** counter cinematic 19.72-24.95; downed 24.95 → |
| v3 (≈ 40.3 s) | still downed to 4.10, kip-up, the 5 % lead-in; **A13 ultimate** 8.20-20.48; **CS3** 21.10-26.25 (= CS2, critic C38); **CS4** part A 26.27 → (ground slash, △ strike, duel) |
| v4 (≈ 40.2 s) | CS4 part B: aerial duel, landing, sheathe, clear lines 1-5 |
| v5 (≈ 25.1 s) | CS4 part C: moon gaze, the greeting, lines 5 (tail)-7, fade (21.67); result panel 21.9-25.1 「도전 성공 / 胜利 / 어려움 모드 / 홍련 / 월하곡 / 최고 기록 달성! / 01:20.52」 |

The player skipped the intro and the start of CS1 (hold-to-skip, cutscenes.md §0.1): the encounter lines 1-10 and the
enrage lines 1-2 are wiki text only (w1 §3), staged here by us. w2 (NIKKE) is the source of the sword 화무십일홍 and her
skills for §7; it adds no fight footage.

### 1.2 Order of the fight and the HP track (patterns.md §10, cutscenes.md §1)
Times since control (≈, contiguous clips): P1 0-29 s → CS1 29-39 → SQ1 + A8 39-51 → CS2 52-57 → downed 57-76 → lead-in
76-80 → A13 80-93 → CS3 93-98 → CS4 98-174 → result. HP: 100 % → 63.1 % at the CS1 cut (bar may lag) → 60.2 % when the HUD
returns (shield full) → unchanged during A8 → 55.7 % after CS2 (−4.5 %) → ≈ 8 % at v2 39.45 → **5.2 %, unchanged while
hit** (the floor) → unchanged during A13 → 3.5 % / 2.3 % in CS3 → she never reaches 0; the clear cinematic follows. The wiki:
"체력이 10% 남았을 때 이 패턴을 넘기면 자동으로 클리어된다" (the footage puts it at 5 %).

### 1.3 Boss effects vs player effects (implementers: never copy Eve's)
| seen | whose | evidence |
|---|---|---|
| lilac / magenta sword-qi crescents, rings, bands, the X, the dome (white-pink rim, fade 0.3-0.8 s); the lilac ghost form, its mist and ribbons; the pink blade glow; the yellow tell (sphere + flare line); the A7 discs; A9's whole-screen magenta; A10's claw streaks and radial burst; the dive's pink-white flash + lilac light column; the pale blue-white back-blink bubble (A6); the red slash line + petal burst of 홍련일섬; thin yellow lightning in the gauntlets (decoration) | **boss** | patterns.md §2-§7 |
| the orange / gold screen-wide parry streaks, the gold starburst on the parried dive, the orange contact spark, the white-cyan crescents and white pillars (Eve's skills), the blue spark at Eve's hand (her hairpin blade), Eve's red-orange tint and flip kick, her pale afterimage on perfect dodges, her cyan-glowing boots (the kick) | **player (Eve)** | patterns.md A1, A5, A8, A9; cutscenes.md §5 |
| "⊙ 건너뛰기" with its ring, the △ prompt + cyan ring, the boss HP bar, the 5-segment shield, the diamond row, the result panel | game UI | cutscenes.md §12 |

Gold / orange clash bursts appear only where her blade meets the player's — the deflect (§5.4) and the cinematic blade
locks and duel (CS1 C1, CS2 / CS3 R2, CS4) — and the cyan-gold kick flash only in R8; never on a boss attack during the
fight.

### 1.4 Floor markings: none
No floor marker or ground decal appears before any hit in the whole fight (five clip analysts; critic.md C70 re-checked A1,
A3, A4, A9, A10, every gauntlet ring and the discs). Every ring, fan, dome and crescent appears at its contact frame or
travels from her blade. → **홍련 has no floor decal of any kind** (rule 10-20). Tells are her pose, the blade glint, the
ghost's reappearance and approach, the yellow tell, the darkness and sounds. Effects that lie on the ground at the
contact tick (A8.4's flat ring, A8.5's X) are hit effects, never shown before the hit.

### 1.5 The originality rule and how §2 / §6 apply it
The rig and the arena are an **original design in the same mood**, not a copy of the original game's character or level.
We keep only the generic archetype the fight and the staging need, take proportions, heights, hat states, hand / prop
usage, lighting moods and distances from model.md / arena.md, and design every distinctive piece anew.

| element | kept (archetype) | not reproduced (model.md §2 / arena.md §2) | ours (§2.2 / §6) |
|---|---|---|---|
| figure | a swordswoman of about human height, long hair | silver-white hair with lilac shadows, pointed ear fins, black hair bow | ink-black hair with a violet sheen in a low ponytail tied with a crimson 댕기 ribbon |
| hat | a wide brim she tips, holds, loses, wears on her back and puts back on | the parchment 전모 cone, U-shaped twin spikes, quilted coil, fur pompoms, gold hook, folded cloth, pendant plaque, quilted rope + violet tassel, the front-left cloud motif that turns crimson in P2, black-red rim with gold frets | a flat round brim of black horsehair weave (흑립-like, slightly translucent) with a tall lacquered crown, a crimson silk hatband with a red-lotus knot at the back (nothing painted on the brim's top), 갓끈 bead strings |
| body | — | white high-cut bodysuit, gold sternum strip, straps, slate capelet, samurai 袖 pauldron, violet tassets with crests, crimson pleats, calligraphy sash, back orbs + spine chain | an ivory 철릭-style long robe with a pleated skirt, an ink-violet sleeveless 전복 vest with a red-lotus roundel, a crimson sash |
| legs / arms | — | crested silver thigh-highs, knee cops, heeled boots; bare arms, bracer with violet rings | dark trousers, ivory 행전 leg wraps, black 목화 boots; long sleeves with leather 토시 bound by crimson cords |
| sword | a long single-edged slightly curved sword drawn **left-handed** from a scabbard (cross-draw from the right hip); light-purple sword-qi | the mechanical sword: flat pale grip with a dark slot, no guard, quilted grip + tassel; the scabbard's slotted mechanical throat and squared tip | a 환도-style long blade with a faint violet temper line, a lotus-shaped iron guard with a brass rim, a violet-cord grip, a black-lacquer scabbard with brass lotus-leaf fittings |
| palette | lilac sword-qi / ghost (an effect colour) | white / violet / silver / parchment / champagne-gold costume values of model.md §2 | ivory / ink-violet / crimson / black / brass (§2.2) |
| arena | a moonlit silver-grass field; silver under a white moon → red field under a red moon; darkness for the gauntlets; field 35-50 m; the moon low over the far end | the moon gate as a composition: two glyph monoliths (紅蓮之哀 / 榮枯盛衰) framing the moon (the "lit tower"), its 22-step axial stairway on a stacked-stone terrace, the lantern pairs at the stair top, the entrance stair from below, the temple halls and pagoda | a wide lotus pond with a rock-islet lotus stone lantern (연화 석등), one old pine leaning over the water, the moon in open sky beside it, bamboo and cherry groves, low stone walls with small lanterns; no terrace stair, no pair of tall masses framing the moon, no glyphs, no monoliths |

How it is enforced: S2a's originality sheet (§2.7) puts each row's original reference crop next to our part; `test_rig.py`
fails when a part's base paint is within ΔE 10 of the model.md §2 paint value of the same role (hat top `#E6DCCF`,
bodysuit `#E4E2E8`, thigh-highs `#CFCBD3`, tasset `#8E6CB4`, gold strip `#CDB78C`, hair `#DDD7E2`); `test_arena_hr.py`
fails on any text display or column of glyph blocks in the arena, on a stairway within ± 20° of the moon's bearing and on
two block masses ≥ 8 b tall mirrored about it (no gate framing, §9.3). The lead sends the U1 + originality sheets to the
user as soon as S2a has them (README 0-7 step 4).

### 1.6 What the footage does not give (→ §0.1 defaults)
No damage or hit-box evidence (no-hit run; tiers and shapes are ours, tuned by S5). No regular P2 pattern (Q-A1). No
failure branch of either gauntlet (the instant death is wiki text, Q-B2 / Q-B3). The intro and enrage lines 1-10 / 1-2
were skipped (Q-A13). Open measurement points that the plan decides (critic.md §6): A9's windup ring is staged as the
sweep plane, not a hit (C5); P1 contact frames are taken as the hit (≤ 1.7 t possible offset, C75 — irrelevant after the
windups are stretched); the hand that rises to the brim is her right (C30, C46); CS1 shot 7 → 8 is played as one push-in.
Dropped on purpose (no counterpart in the pack; each a questions.md default): the diamond row (balance gauge 20 → 24
pips, Q-A11); her weakness to knock-downs (w1 「다운시키는 공격에 약하다」; the grenade / beta-skill downs of v1 26.3-37.28 —
only the framework's staggers, framework.md §4.6, Q-A21); W5 (the execution counter), W6 (the stylish cinematic attack
with a Repulse finish) and W7 「어림없다」 (no execution / Repulse in the pack, Q-A1, Q-A16); A12's △ input (staged without
input, Q-A18); the result panel except 「도전 성공」 / 「월하곡」 (胜利, 어려움 모드, 최고 기록 달성!, the clear time; Q-A19);
Volt (Q-A20); the aerial duel's flat purple-haze backdrop (v3 38.73-40.30, `#5E2F48`).

---------------------------------------------------------------------------------------------------------------------

## 2. Model: display-entity rig (S2a; the cinematic clips S2b)

### 2.1 Scale and silhouette (proportions from model.md §1, scaled; the 타키 lesson: not too small or thin)
- Player 1.8 b. 홍련 stands **2.55 b** to the head top (≈ 1.42 ×; the footage puts her at Eve's height, the 10-30 playtest
  asks for a bigger boss — 타키 2.81 b, 아를레키노 2.8 b), **2.82 b** to the hat crown. 6.7 heads (head 0.38 b): a little
  larger than the real 7.5-8 for readability (model.md §6 did the same).
- Heights (sole 0): ankle 0.10, knee 0.68, hip joint 1.28, belt 1.36-1.48, waist 1.50, bust 1.75, shoulder 1.95, neck
  2.05, chin 2.17, eyes 2.36, head top 2.55; hat brim worn at 2.40 (front edge at the brows, tilted 6° forward).
- Widths: shoulders 0.62, waist 0.34, hips 0.56; robe skirt flaring to 0.80 at the hem (hem at y 0.40, mid-shin); limbs
  1.15 × a realistic girth.
- Hat: flat round brim **Ø 1.60 b** (≈ 2.6 × the shoulders; the archetype's huge disc), crown Ø 0.44 × 0.30 high.
- Sword total **2.10 b** (≈ 0.82 H, model.md §1 0.85 H): blade 1.75 × 0.07 × 0.025, 3° curve, single edge; guard Ø 0.13;
  grip 0.33. Scabbard 1.82 × 0.09 × 0.045 (≈ 0.71 H). The hand hangs at y ≈ 0.90, so a straight-down blade would sink
  0.85 b into the floor: idle / walk / guard poses keep the blade angled low across her front (tip ≥ 0.10 b above the
  floor); point-down only with the arm raised (model.md §6 note). The floor-dip gate checks the blade tip, scabbard tip,
  hat brim, hair and skirt every clip tick.
- Body: husk `scale 1.35` (≈ 0.81 × 2.63 b), click shield `hit {w:1.2,h:2.9}`; no hit proxies (`px` is forbidden for
  specials). Culling box 8 × 8 (brim + leaps), view range 2, billboard fixed. Shadow radius 0.9.

### 2.2 The original design (paint guide; every part described well enough to paint it)
Concept: a Joseon wandering swordswoman (협객) under the moon; the name 홍련 (red lotus) is the motif. Lighting is not baked:
paint neutral values, the arena's moonlight / crimson light colours them (model.md §0).
- **Hat (흑립-like)**: a flat round brim of fine black horsehair weave — concentric rings and radial ribs at 8 px spacing,
  slightly translucent (alpha 215), a faint lilac sheen on the outer 2 px of the rim; a tall straight lacquered crown
  (octagonal drum) in glossy black with one highlight stripe; a crimson silk hatband (0.06 b) with a **red-lotus knot**
  (매듭) at the **back** of the band, centred behind the crown: five crimson petals, pink tips, a gold-thread centre;
  nothing painted on the brim's top (the original's front-left motif that changes colour in P2 is not echoed, model.md
  §2.1). Underside: the same weave, darker, with the crown's shadow. P2: the knot glows (emissive look `p2`).
- **Hat strings (갓끈)**: two strings of beads from the brim's inner sides, meeting in a loop under the chin and hanging
  to the chest: dark-red jasper beads (0.035) alternating with pale amber beads (0.03) and black spacers.
- **Face**: young, calm; almond eyes with **amber** irises and a dark ring, thin dark brows, small nose, soft rose lips;
  three face cards: `calm`, `smile` (closed-lip smile, lines 2 / 4 / 6), `closed` (eyes closed, line 7).
- **Hair**: ink black with a violet sheen, blunt bangs to the brows with two longer strands framing the face, side locks
  to the collarbones, a long low ponytail tied at the nape with a crimson **댕기** ribbon (two tails along the hair, a small
  gold stamped pattern).
- **Robe (철릭-style)**: ivory long robe, crossed collar with a white 동정 collar band, narrow sleeves; from the waist a
  knife-pleated skirt to mid-shin split in four panels, each with a 0.10-b **crimson band of stylised lotus petals** at
  the hem.
- **Vest (전복)**: ink-violet sleeveless long vest over the robe, open at the front, edged with a thin brass thread; a
  **red-lotus roundel** (Ø 0.20) embroidered on the back between the shoulder blades and a small one (Ø 0.07) on the left
  breast.
- **Sash**: crimson cloth sash wrapped twice at the waist, knotted at the left hip; two tails with brass end caps.
- **Arms**: robe sleeves; on the forearms dark-brown leather **토시** guards bound by three crimson cords each; bare hands.
- **Legs**: dark plum trousers (seen at the knees in motion), ivory **행전** wraps from knee to ankle with two crimson ties,
  black **목화** boots with a thick white sole.
- **Sword**: steel blade with a faint **violet temper line** along the edge side and a bright 1-px edge; a **lotus-shaped
  guard** (eight petals) in dark iron with a brass rim; grip wrapped in violet cord in a diamond pattern over ivory ray
  skin; brass pommel cap. No tassel, no mechanical parts.
- **Scabbard**: black lacquer with a thin red-lacquer line along the spine, **brass lotus-leaf fittings** at the mouth,
  the middle and the tip, two crimson cord hangers. Worn at the right hip (mouth forward, edge up, angled back-down 30°);
  carried in the right hand by the throat in cinematics (model.md §3).
- **Intro props** (from the poem of lines 1-4, 월하독작): a small white porcelain cup with a blue rim and a white-and-blue
  porcelain bottle (백자) painted with a cobalt lotus scroll.
- **Ghost form**: one flat glowing lilac for every part including the hat (model.md §5): a 16 × 16 gradient (core `#9A4FB8`,
  body `#C97EDD`, rim `#F0C8FA`, alpha 200), brightness 15. The ribbons, mist and sparkles are kit effects.

| role | base | shade | highlight |
|---|---|---|---|
| robe, leg wraps | `#EDE6D6` ivory | `#C9BFA8` | `#FBF7EE` |
| collar band | `#F8F6F0` | `#D8D2C4` | — |
| vest | `#2A2033` ink-violet | `#1A1420` | `#4A3A5A`, brass thread `#B89A5A` |
| sash, hatband, ties, cords, 댕기 | `#9E1F35` crimson | `#6E1222` | `#C8354F` |
| lotus motif | `#C8304A` petals | `#8E1C30` | tips `#F08AA0`, gold thread `#C9A45C` |
| trousers | `#3A3340` | `#26212B` | `#55495C` |
| boots | `#1C1A1E` | `#0F0E10` | sole `#E8E4DC` |
| arm guards | `#4A3428` leather | `#2E2018` | `#6E5040` |
| skin | `#F1D5C4` | `#D4AE9C` | `#FBE8DE` |
| hair | `#15121A` | `#0A080D` | sheen `#4B3A66` |
| eyes / lips | amber `#C98A3A`, ring `#5A3A1A` | — | lips `#C46A70` |
| hat weave / crown | `#1E1A24` (alpha 215) / `#141118` | `#0E0C12` | rim sheen `#5A4A70` |
| hat knot (P1 / P2 emissive) | `#D23A55` / `#FF5A78` | `#8E1C30` | `#FF9AB0` |
| beads | jasper `#7A1E2A`, amber `#E3C27A` | — | — |
| blade / temper / edge | `#CCC8D2` / `#9C7BC8` / `#F4F2F8` | spine `#6E6874` | — |
| guard / brass | iron `#2E2A30` / `#B8924A` | `#7E6230` | `#E0C27A` |
| grip | cord `#3E2A55`, ray skin `#E8E2D4` | — | — |
| scabbard | `#141216`, line `#7A1622` | — | lacquer gloss `#4A4652` |
| ghost | `#C97EDD` | `#9A4FB8` | `#F0C8FA` |

### 2.3 Parts (item displays; UUID `524c4b4d-4852-4400-8000-0000000000NN`, NN = #, shadow `…40`)
Tags `rlk_room rlk_mb_aux rlk_mb_part rlk_hr_part rlk_hr_<part>`; billboard fixed; view range 2. Sizes w × h × d in blocks.

| # | part | parent | size | content (§2.2) | looks | bright |
|---|---|---|---|---|---|---|
| 00 | pelvis | root | 0.38×0.20×0.26 | robe waist, sash wrapped twice, knot at the left hip | — | 13 |
| 01 | torso | pelvis | 0.42×0.50×0.26 | robe body, crossed collar, vest with brass edge, lotus roundels | — | 13 |
| 02 | head | torso | 0.32×0.38×0.34 | skull, hair cap, bangs, ears | — | 13 |
| 03 | face | head | card 0.24×0.26, 0.002 in front | eyes, brows, nose, lips | `calm` `smile` `closed` | 13 |
| 04 | hair_tail_1 | head | 0.15×0.42×0.08 | ponytail upper half, the 댕기 knot | — | 13 |
| 05 | hair_tail_2 | hair_tail_1 | 0.12×0.44×0.06 | ponytail lower half, ribbon tails | — | 13 |
| 06 / 07 | lock_r / lock_l | head | 0.07×0.32×0.05 | side locks | — | 13 |
| 08 / 09 | arm_r / forearm_r | torso / arm_r | 0.13×0.40×0.13 / 0.12×0.42 (+ hand 0.10×0.14) | sleeve; arm guard + hand | hand `open` `grip` `brim` | 13 |
| 10 / 11 | arm_l / forearm_l | torso / arm_l | mirrored | mirrored | hand `open` `grip` `brim` | 13 |
| 12 / 13 | thigh_r / shin_r | pelvis / thigh_r | 0.17×0.62×0.17 / 0.15×0.66 (+ foot 0.12×0.10×0.30) | trousers; leg wrap + boot | — | 13 |
| 14 / 15 | thigh_l / shin_l | pelvis / thigh_l | mirrored | mirrored | — | 13 |
| 16 / 17 | skirt_fl / skirt_fr | pelvis | 0.30×0.98×0.03 | front skirt panels, lotus hem band | — | 13 |
| 18 / 19 | skirt_bl / skirt_br | pelvis | 0.32×1.02×0.03 | back skirt panels | — | 13 |
| 20 | sash_tails | pelvis | 0.12×0.52×0.02 | two crimson tails, brass caps | `p1` `p2` (emissive edge) | 13 / 14 |
| 21 | hat | head (re-parentable) | brim Ø 1.60 × 0.025 (four squares at 0 / 22.5 / 45 / −22.5° → 16-gon, stacked 0.003 apart), crown Ø 0.44 × 0.30, band 0.06 | weave brim, lacquer crown, hatband, lotus knot at the back | `worn` `back` `hand` `world` `gone`; `p1` `p2` | 13 |
| 22 | hat_strings | hat | 0.34×0.60×0.02 | bead strings | — | 13 |
| 23 | sword | forearm_l (grip at the hand point) | 2.10 total (§2.1) | blade, lotus guard, grip, pommel | `hand` `gone` | 13 |
| 24 | sword_glow | sword | 1.75×0.08 overlay (0.004 off both faces) | emissive edge | `off` `lilac` `pink` `violet` `gold` | 15 |
| 25 | scabbard | forearm_r (throat at the hand) / pelvis | 1.82×0.09×0.045 | lacquer, brass fittings, cords | `hand` `hip` (pelvis at (−0.22, 1.40, 0.02)) `gone` | 13 |
| 26 | hilt_sheathed | scabbard | guard + grip at the mouth | shown only while sheathed | scale 0 unless `sword sheathed` | 13 |
| 27 | cup | forearm_r / world | Ø 0.07 × 0.05 | porcelain cup | `none` `hand` `rock` | 13 |
| 28 | bottle | forearm_l / world | 0.12 × 0.26 | porcelain bottle | `none` `hand` `rock` | 13 |
| 40 | shadow | root | r 0.9 | standard shadow | — | — |

Element rule (RP README §4): elements inside −16..32, one rotation axis of −45 / −22.5 / 0 / 22.5 / 45: the flat brim is
four flat squares rotated about Y (a 16-gon) and the crown four boxes the same way, so no element needs two axes; the
brim tilt comes from the display transform. The four brim squares are stacked 0.003 b apart in y and each paints only its
own corner wedges (the shared centre is transparent on three of them), so no faces are coplanar and the translucent weave
never stacks; S2a renders the brim close from the side (§2.7). Every part has a ghost model (same geometry,
`rlk:mboss/scarlet/ghost`).
Secondary motion (clip-driven): hair chain lag 3 t, skirt panels follow their thigh at 0.6 × the swing with a 2-t lag, sash
tails and ribbon lag 3 t, hat strings lag 2 t, idle sway sine 40 t.

### 2.4 Looks and states (`rig/look/<channel>/<v>`)
`form` normal | ghost (every part → its ghost model, brightness 15; `sword_glow` lilac) · `phase` p1 | p2 (hat knot and
sash-tail edges emissive crimson) · `hat` worn | back (hanging between the shoulder blades by the strings) | hand (in the
right hand, brim vertical, at shoulder height) | world (the clip keys its transform relative to the root: knocked off,
flying, lying beside her, over her face) | gone · `sword` hand | sheathed (blade hidden, `hilt_sheathed` shown) | gone ·
`blade` off | lilac | pink | violet | gold · `scabbard` hand | hip | gone · `face` calm | smile | closed · `state` normal |
hidden · `flash` (hit feedback 3 t). `scabbard gone` hides the scabbard with the sheathed hilt (§7's sword toss). The
intro props `cup` / `bottle` are keyed by the `intro` clip; `props/none` hides both. Clips set the hat / sword / scabbard /
face states they need at their own events; the module only calls `form`, `phase`, `blade` and `state`.

### 2.5 Clips (contract; names / lengths / loops / events frozen at D0; ticks = played clip ticks)
| clip | len | events |
|---|---|---|
| `idle` / `idle2` (P2: lower, blade further out) | 40 loop | — |
| `walk`, `glide` (P2 walk-in: leaning slide) | 24 / 16 loop | step 0, 12 / — |
| `strafe_l`, `strafe_r` | 20 loop | step 0, 10 |
| `backstep` | 12 | land 10 |
| `flinch` | 6 | — |
| `a1` | 34 | pivot 0, glint 6, lock 7, fan 10, hit 14, end 34 |
| `a2` | 30 | glint 0, draw 4, lock 5, glow 6, hit 12, end 30 |
| `a3` | 96 | glint 0, lock1 7, h1 14, lock2 23, h2 30, lock3 38, h3 45, lock4 50, h4 57, lock5 62, h5 69, end 96 |
| `a4` | 60 | crouch 0, leap 2, apex 6, glint 7, lock 12, flip 13, dive 16, hit 20, crouch2 22, slash 25, lock2 27, ring 28, hit2 34, land 38, end 60 |
| `a6` | 20 | bubble 0, gone 2, appear 4, settle 10, end 20 |
| `a9` | 64 | turn 0, spin 3, ring 4, yellow 8, star 17, lock 22, flash 24, go 26, cut 28, end 64 |
| `a10` | 56 | crouch 0, spring 2, apex 8, yellow 10, lock 14, dive 20, hit 22, end 56 |
| `a7_tell` | 16 | back 0, yellow 2, retreat 4, settle 14, end 16 |
| `a7_throw` | 16 | crouch 0, up 4, crescent 6, spin 7, release 12, end 16 |
| `g_brim` | 14 | raise 0, hold 6, end 14 (loop 6-14) |
| `g_tell` | 12 | lilac 0, burst 3, gone 4, end 12 |
| `g_reform` | 10 | appear 0, solid 4, end 10 |
| `g_dash` (D1) | 12 | appear 0, go 6, arrive 10, end 12 |
| `g_glide` (D2) | 12 | appear 0, go 2, stop 9, end 12 |
| `g_drop` (D3) | 14 | flash 0, gone 2, appear 7, land 12, end 14 |
| `g_run` (D4) | 14 | appear 0, run 2, lunge 10, end 14 |
| `g_ring` (A8.1) | 14 | arc 0, hit 3, spin 4, end 14 |
| `g_rise` (A8.2) | 14 | spin 0, arms 6, hit 9, end 14 |
| `g_leap` (A8.3) | 18 | coil 0, raise 5, hit 9, tumble 10, gone 16, end 18 |
| `g_sweep` (A8.4) | 14 | arm 0, hit 3, spring 4, end 14 |
| `g_x` (A8.5) | 16 | drop 0, raise 2, hit 6, gone 14, end 16 |
| `g_wrap` (A8.6) | 12 | land 0, hit 3, end 12 |
| `g_dome` (A8.7) | 12 | swirl 0, hit 3, end 12 |
| `g_vert` (A8.8) | 20 | crouch 0, glow 1, hit 5, rise 6, gone 18, end 20 |
| `g_dive` (A8.9) | 10 | appear 0, dive 3, hit 6, end 10 |
| `g_deflect` | 12 | stop 0, fall 2, lock 10, end 12 |
| `repel` (CS2 / CS3) | 104 | lock 0, grab 8, hat_back 8, flash 24, throw 28, b2b 44, toss 58, hat_off 60, land 75, lie 78, petals 80, kick 102, end 104 |
| `down` | 40 loop | — |
| `kipup` | 20 | legs 0, up 8, crouch 10, raise 14, end 20 |
| `lead_down` | 82 | legs 0, up 7, sword_up 10, hat_hand 12, walk 12, refill 29, hat_over 42, hat_on 48, glow 56, dark 64, brim 65, end 82 |
| `lead_stand` | 70 | stagger 0, hat_hand 8, walk 10, refill 18, hat_over 30, hat_on 36, glow 44, dark 52, brim 53, end 70 |
| `sq1` | 60 | crouch 0, rise 6, rehat 10, hat_hand 12, hat_on 28, standoff 30, dark 42, brim 46, end 60 |
| `intro` | 554 | CS0 0-553 (§3.1 beat ticks): l1 20, pour 30, l2 62, sip 80, l3 104, raise 110, l4 146, l5 198, cup_down 206, stand 214, turn 248, l6 300, scab_hand 300, l7 352, l8 398, gesture 402, l9 444, l10 502, scab_up 510, end 554 |
| `intro_end` | 86 | CS0 554-640 (= the skip's target, §3.1), ticks − 554: l11 0, smile 2, head_down 36, turn_away 44, spin 50, draw 56, stance 60, brim 62, tuck 76, music 76, push 82, end 86 |
| `cs1` | 213 | §3.2: lunge 0, lock 10, l13 12, push 32, leap 36, hat_back 40, land 52, l14 58, glint 96, black 100, sheathe 104, hat_on 104, l15 104, petal 114, petal2 128, l16 144, cut 154, neg 161, pink 165, slash 169, recolour 173, hat_back2 176, music 179, swirl 183, end 213 |
| `ending` | 1042 | §3.7: glint 16, band 20, rise 28, hat_on 44, raise 48, clash1 58, lock 62, back 80, lunge 92, clash2 96, x1 108, x2 116, x3 124, pass 140, strike 143, return 170, clash3 174, flash2 188, leap 190, a1 204, a2 216, a3 228, white 232, fly 238, land 258, rise 268, walk 272, scab_up 284, swing 296, l17 300, music 300, seated 320, l18 368, l19 448, head_down 494, turn 506, l20 536, profile 600, hand 612, l21 664, gaze 690, dip 786, pivot 794, l22 800, gesture 860, smile 920, l23 936, brim 936, pull 980, eyes 1030, end 1042 (H, §3.7) |
| `ev_give` / `ev_toast` (§7.3.2) | 34 / 34 | lift 0, present 12, toss 30, end 34 / look 0, palm 14, offer 30, end 34 (tick 0 = `ending`'s last pose) |
| `ev_leave` (§7.3.2) | 10 | turn 0, gone 6, end 10 |
Big swings (A3 crescents, the spins, the leaping cuts, the draw, the sheathe's scabbard swing) are keyed every tick (≤ 120°
per tick, RIGLIB check); quiet cinematic beats may key every 2-4 t with interpolation. The gauntlet script `play`s the
next clip over the previous one (play replaces), so the cut clips' tails are maximum lengths. Root motion is never in a
clip: the module / sequence moves the body (`mboss/mv/*`), the rig follows the anchor.

### 2.6 Anchors and props
`rig/anchor/{hand_l,hand_r,blade_tip,blade_mid,scabbard_mouth,hat_crown,head,chest}` moves the one `rlk_hr_anchor`
marker there (effects run `at` it). The rig owns no other world entity: the seat rock, moon halo, lotus flowers, petals
and the projectile cards are kit props (§9.2).

### 2.7 Reference renders S2a / S2b must deliver (≤ 640 px; renderer `S:az/understand/rigtech_render.py`, wrapper as `S:ap/rigwork/r1/r.sh`)
- `HR/renders/s2_U1.jpg`: front / side / back / ¾ of the normal form, the P2 accents, the ghost form, the five hat states and
  the iaido stance, next to a 1.8 b player stand-in.
- `HR/renders/s2_orig.jpg`: the originality sheet — per §1.5 row, the original's reference crop (`HR/ref/model_hat_top.jpg`,
  `model_front.jpg`, `model_back.jpg`, `model_legs.jpg`, `model_sword_hilt.jpg`, `model_sword_scab.jpg`, `model_colors.jpg`)
  beside our part, captioned with what differs.
- Clip strips every 2 t (every 4 t for `intro`, `intro_end`, `cs1`, `ending`); the cinematic strips next to `v1s_intro_*`, `v2f_cs_*`,
  `v2f_c*` / `v3r_c*`, `v3r_a_kipup`, `v3r_e_*`, `v4k_*`, `v5e_*`; one side render per held-prop pose (blade low in idle,
  iaido stance, the draw, the sheathe, the scabbard at the hip and in the hand, the hat in the hand and on the back); a
  close side view of the brim at rest and tilted (no flicker, no stacked translucency, §2.3); the item / thrown-sword
  model `rlk:mboss/scarlet/item_sword` in the gui, hand and ground transforms (§7.3.2).

### 2.8 Atlas share (rig ≤ 0.15 M px; plan ≈ 0.09 M)
32 px/b on the body, 64 px/b on the head and the hat, 128 px/b on the face cards: head 64², face 3 × 32², hair 4 × 32×64,
torso 64², pelvis 64×32, arms 4 × 32×64, legs 4 × 32×64, skirt 4 × 32×64, sash 2 × 32², hat 128² + crown 64², knot 2 × 16²,
strings 16×64, sword 32×128, glow 5 × 16×128, scabbard 32×128, hilt 32², cup 16², bottle 32², ghost 16² ≈ 91 k px.
Together with the kit (≤ 0.26 M, itemized in §9.2), the gate icon (≤ 0.005 M) and §7 (0 px: the item / thrown-sword model
reuses this sheet; 0.015 M kept as a reserve): ≤ 0.43 M of the ≈ 0.57 M left under the 13.2 M gate (stitched ≈ 13.06 M),
leaving ≈ 0.14 M for the next boss.

---------------------------------------------------------------------------------------------------------------------

## 3. Cutscenes and scripted sequences (S2b `seq.py`; services written by S3's generator into `F:boss/scarlet/seq/**`)

### 3.0 Common rules
- **Division** (framework.md §2.3): the core owns invulnerability (`rlk_mb_inv`), `cine`, the phase switch, floors, the
  death finish and when a sequence starts; a sequence owns its rig clip, sounds, kit effects and props, typed lines, titles,
  overlays, push rings, the arena look calls (`api.arena_look`) and the body moves inside it (`mboss/mv/glide|leap`, end
  points through `mv/ok`), and emits the music line of its `music` event through `api.music(ph)`. Every effect sits on a
  clip event (`api.ev`); `#sqdone` at the clip end; `cancel` idempotent.
- **Tools** (framework.md §2.6; nothing new): rig clips; kit effects / props; kit typed lines `fx/hud/line {id}` (subtitle
  slot, Raiden letter reveal); full-screen title-glyph overlays `fx/hud/ovl {g,in,hold,out}` (Guardian P4 / Apep
  precedent, `vBig` rests the F5 crosshair; while a line is up the overlay's fade-in / fade-out is drawn as opacity-step
  glyphs (20 / 40 / 60 / 80 %) re-sent every tick at full title alpha — the title and the subtitle share one alpha, so a
  vanilla title fade would dim the line and its end drop it; F2, HR-30); arena look jobs; push rings (no damage); one-shot facing = `mboss/pull/start
  {t:0}` positioned at the player's feet (`#pullFace 1`) while fighting; while dying (pull refuses then) `rotate`, no
  teleport: `execute as @a[tag=player] anchored eyes run rotate @s facing entity <body> eyes` and `rotate
  @e[tag=rlk_av,limit=1] facing entity <body> feet` (the F5 seat rides the avatar: a tp would dismount it and move the
  avatar; first person has no avatar; F2, HR-02); the boss bars off / on through `mboss_lib.bars(on)`
  (FN-f, §9.2: the framework re-shows bars every tick otherwise); the actionbar with `hudHold` (the 야타용왕 banner
  precedent) for the intro's skip prompt and to hold the player's HUD (`hudHold 2` every tick) through CS0, CS1,
  CS4 and the coda (CS2 / CS3 / SQ1 / the lead-ins keep it; the footage hides it there, cutscenes.md §12; F2, HR-29); each
  of these sequences also blanks the actionbar once at its start (`title @a[tag=player] actionbar ""`: the hold only stops
  new sends, the game keeps the last actionbar ~60 t; CS0's skip prompt at 20 then takes the line). No camera, no letterbox, no slow motion, no input lock (the convention of every
  boss).
- **Overlays are approximations**: title glyphs can only paint over the screen, so `negative` is a pale cyan-white field
  with a dark rim and a dark diagonal band (it cannot invert the scene's colours; said in the release note).
- **Line over an overlay** (kit rule, S1K): while an overlay is up, a line step re-sends the overlay glyph as the title
  (with its remaining hold) instead of `view/ttl_blank`, so a typed subtitle shows on the black (as v1 f133 and v2 f71 do).
- **Staging frame**: the footage's "screen-left / right" means relative to Eve's view of her. Every sequence stores the
  player's position and yaw at its tick 0 in the marker `rlk_hr_stage`; "the player's right / front" below is relative to
  it; "north" = −z (the moon side; the moon disc itself is at bearing 12°, `api.MOON_POS`, §6.2).
- **Player safety**: `#mbCine 1` (`cine/start` … `end`) through CS1 and CS2 / CS3 (every boss hit refused, live hazards
  unspent); CS4 runs in the death state `#mbSt 2` (nothing can hit the player, the player's attacks are swallowed); the
  intro has no hazards and the boss is invulnerable; SQ1 and the lead-ins create no hazard. The player is never locked.
- **Lines** (`api.LINES`, speaker 홍련, colour `#F2D0E8`, two syllables per 2-t step with `block.note_block.hat` 0.3, hold
  then clear; a new line replaces a running one). Verbatim only (cutscenes.md §11, critic.md §3):

| id | text | where | ticks on screen | source |
|---|---|---|---|---|
| 1-4 | 꽃 속에 술 한 병 놓고, / 벗 없이 혼자 술잔 드네. / 잔 들어 밝은 달 맞이하니, / 달과 나와 그림자 셋이 되었네... | CS0 20 / 62 / 104 / 146 | 40 / 40 / 40 / 50 | w1 조우 시 대사 1-4 (Li Bai, 月下獨酌) |
| 5 | 그리고 이제 친구가 와 주었으니 월하독작이 아니라, 대작이 되겠구만. | CS0 198 | 100 | w1 조우 5 |
| 6-10 | 낭자, 내 말하지 않았던가? / 곧 또 보게 될 것 같다고. / 아름다운 곳이지 않나? / 신세진 것도 있겠다, 이 달 아래서... / 한 수 가르침을 청하고 싶네만. | CS0 300 / 352 / 398 / 444 / 502 | 50 / 44 / 44 / 56 / 50 | w1 조우 6-10 |
| 11 | 낭자 생각은 어떤가? | CS0 554 | 68 | w1 조우 11 = v1 f133-f335 (203 f) |
| 12 | 거기가 아닐세. | A6 + 12 | 63 | v1 f1010-f1198 (footage only) |
| 13-14 | 낭자, 대단하구만. / 진심으로 가겠네. | CS1 12 / 58 | 44 / 42 | w1 광폭화 1-2 |
| 15-16 | 천지만물을 벤다는 건... / 이런 것일세. | CS1 104 / 144 | 36 / 40 | v2 f71-f182 / f211-f328 (the footage split, period not "!"; line 16 is up before the petal is cut and runs through the slash, as in the footage) |
| 17-23 | 낭자, 여기까지 하세. / 대단하네, 좋은 수련이 되었어. / 이제 정말 가야겠네. / 다음 번에 만나면, 그땐 같이 한잔 하면 좋을 텐데... / 달빛과 바람을 안주 삼아... 말일세. / 어디 보자, 낭자네에선 이렇게 인사한다고 들었는데... / 당신의 기억이 이어지기를. | CS4 300 / 368 / 448 / 536 / 664 / 800 / 936 | 60 / 68 / 45 / 119 / 130 / 130 / 90 (the footage lengths) | w1 클리어 1-7 = v4 f674 → v5 f1124 |
| 24 | 조심하게. 칼자루를 쥐었다고 그 검의 주인이 되는 것은 아니니. | §7 coda E4, item branch | ≤ 48 | w2 l.405 (NIKKE 획득) |
| 25 | 한잔할 텐가? 안주는 달빛과 바람일세. | §7 coda E4, buff branch | ≤ 48 | w2 l.298 (the page's quote; the 대화 2 entry l.409 spells it 「한 잔 할텐가?」 — l.298 is used) |
Not used in the fight: 「어림없다」 (a paraphrase, w1) and the other NIKKE voice lines of w2. §7's event coda adds the two
NIKKE lines 24-25 verbatim (above), and the item quotes w2 l.411 (its tooltip) and, optionally, w2 l.522 (the ★★★ chat
line) — all verbatim from the user's pages; `api.EVENT['lines']` off gives a wordless coda.

A line wider than 192 font px (the subtitle is drawn at 2x and never wraps; 192 px fits the Auto GUI width of 1920 × 1200
and every smaller window) is shown as consecutive subtitles split at its natural pause (`api.LINE_PAGES`), typed one after
the other inside the same `LINE_AT` hold (the hold split by the pages' widths), the pages joined with one space = the line
verbatim (`api.LINES` stays whole): 5 「그리고 이제 친구가 와 주었으니」 / 「월하독작이 아니라, 대작이 되겠구만.」 (260 px →
120 + 136), 22 「어디 보자,」 / 「낭자네에선 이렇게 인사한다고 들었는데...」 (196 → 38 + 154), 24 「조심하게. 칼자루를 쥐었다고」 /
「그 검의 주인이 되는 것은 아니니.」 (236 → 106 + 126) (F2, HR-16).

### 3.1 CS0 — intro (boss only; `seq/intro`, clips `intro` 554 + `intro_end` 86, registry `intro` 650)
Policy as every boss: no camera, no lock, `rlk_mb_inv` until 640 (the framework's intro state), title at the draw, push
ring at the end. No boss bar in CS0: `mboss_lib.bars(0)` in the spawn hook and again at `core/intro/begin` (the framework's
`start_go` shows the bars only while `#mbBarOff` is 0 — F2's request f2-8, applied at F-I), `bars(1)` at control
(`core/intro/done`), the HP bar filling over its first 30 t (the module's bars hook runs `mboss/bars_ramp` while `#mbSt 1`,
`#mbT ..29`) as the original's grows at f498; the player's HUD is held every tick (F2, HR-29). The player arrives at `start` (south rim, facing north) under the framework's 1-s arrival blindness
(`F:mboss/tp_in:2`), so the first line starts at 20. She spawns on the line from `start` to the moon (the moon is at
bearing 12°, §6.2) — since the lead's I1b decision 1 (11-05) the seat is (884.0, 201, 5.0), about 5 b nearer the player than
the first ≈ C + (4.5, 0, −8): 26.73 b from `start`; the intro's walk legs run while she is more than 7 b away and end 6.76 b
(the skip: 6.50-6.76 b) from a player standing at `start` (S2d's 0.4-b rise and 1.1-b step aside; I1b's seat gave 6.3 b;
V2, HR-53; test_scarlet `skip` prints both, ≤ 7.05 checked) (`api.xyz` writes the seat with decimal x / z) — seated on the kit prop `seat_rock` (a low flat stone,
no collision), back to the player, facing the moon: the composition of the footage's opening wide (v1 0-1.88: the field,
the far figure under the moon). Lines 1-10 are wiki-only (skipped in the footage), staged by us from their meaning (the
poem: a bottle among flowers, drinking alone, the cup raised to the moon, the moon, me and my shadow); line 11 onward
follows the post-skip footage (cutscenes.md §2 shots 1-4).

| beat | source | ticks | her pose / motion | effects / props | sounds (vanilla) | line |
|---|---|---|---|---|---|---|
| E0 arrival | v1 0-1.88 | 0-20 | seated, back to the player; cup in her right hand (rig `cup hand`), bottle on the rock (`seat_rock` look `bottle`), hat worn, sword sheathed at the right hip | kit `arrive_rift` behind the player (closes over 30 t), `moon_halo` (P1), lotus buds, `ambient_p1` | `item.elytra.flying` 0.12 pitch 0.6 (wind, `stopsound` at 40), the wind (`cs0_wind`) at the player (at her seat, 26.7 b away, its minVolume 0 reached no one; F2, HR-46) | — |
| E1 | enc. 1 | 20-60 | picks up the bottle in her left hand (24; rock `bare`), pours (30-44), puts it back (46-52; rock `bottle`) | — | `item.bottle.empty` 0.3 pitch 1.4 at 32 | 1 |
| E2 | enc. 2 | 62-102 | cup to her lips (70), sips (78-86), lowers it (94) | — | `entity.generic.drink` 0.35 pitch 1.3 at 80 | 2 |
| E3 | enc. 3 | 104-144 | raises the cup to the moon, arm extended, head up (110-140) | `moon_halo` +20 % (112-140) | `block.amethyst_block.chime` 0.3 pitch 1.2 at 118 | 3 |
| E4 | enc. 4 | 146-196 | lowers the cup, looks down at her shadow on her right (160-180), slow sway | — | — | 4 |
| E5 | enc. 5 | 198-298 | sets the cup down (206: rig `cup none`, rock `set`), rises (214-244), turns to the player (248-268, body yaw turned by the sequence), a small laughing head tilt (270-290) | — | `block.decorated_pot.insert` 0.3 pitch 1.8 at 206; `item.armor.equip_leather` 0.3 at 230 | 5 |
| E6-E7 | enc. 6-7 | 300-396 | takes the scabbard from her hip into her right hand (300, `scabbard hand`) and walks toward the player (`walk`, 0.15 b/t in 12-t `mv/glide` legs, stops at ≤ 7 b) | — | `block.grass.step` 0.25 every 12 t | 6, 7 |
| E8 | enc. 8 | 398-442 | stops; sweeps her open left hand from the moon across the field (402-432) | kit `petals_drift` | `block.cherry_leaves.fall` 0.3 at 410 | 8 |
| E9 | enc. 9 | 444-500 | walks on (444-490, stops at ≤ 7 b), looking at the player from under the brim | — | steps | 9 |
| E10 | enc. 10; v1 4.8-5.8 | 502-552 | stops; raises the scabbard upright before her right shoulder (510) | — | `item.armor.equip_chain` 0.3 pitch 1.4 at 510 | 10 |
| E11 | enc. 11; v1 2.2-7.45 (`v1s_intro_*`, `mg_v1_hands_zoom`) | 554-624 (clip `intro_end` from 554) | smile (face `smile` 556-588); lowers her head (590), turns away (598-604), spins (604-610) → **the draw** at 610 (left hand cross-draws from the scabbard in her right; `sword hand`) → **stance** 614 facing the player: arms spread, scabbard low in the right hand tip down-and-out, sword arm out to her left; the right hand drops, the left (sword) hand rises to the brim (616-624) | **title 「홍련」 / 「월하곡」 at 610** (`mboss_lib.title`, `#E8466A`); kit `glint {c:5}` (white) at `blade_tip` + `qi_arc {r:18,yaw:0,pitch:0,roll:0,c:1}` at 610 | `item.trident.return` 0.6 pitch 0.9 at 606; `entity.player.attack.sweep` 0.6 pitch 1.4 at 610; `block.amethyst_block.resonate` 0.5 pitch 1.6 at 612 | 11 (554-622) |
| E12 stance | v1 7.45-8.05 | 624-640 | settles into the guard (idle); the scabbard tucked to the right hip (630); `seat_rock` and props removed (630) | music phase 1 at 630; push ring r 4 (no damage) at 636 | `item.armor.equip_leather` 0.3 at 630 | — |

**Skip** (`api.INTRO_SKIP` true, question 7; the original's hold-to-skip, cutscenes.md §0, questions.md Q-A14): from 20 to
540 the actionbar shows the original's prompt 「⊙ 건너뛰기」 verbatim (grey `#A8A8B0`) with the pack's control hint
「 · Shift 길게」 (`hudHold` refreshed each tick, so the player's actionbar HUD is off meanwhile — the original hides its
HUD in the intro too, cutscenes.md §12). Holding sneak (predicate `rlk:in_sneak`) brightens the prompt in four 5-t steps
(the original's filling ring); released early, the count resets. The pack's F5 sneak-tap (`lvup/tick`: a Shift press opens /
closes the item-selection space) is off while a boss intro runs (`#mbLive 1`, `#mbSt 0`; not inside the selection space),
so the skip hold makes no deny sound (F3, HR-34). 20 t held → actionbar cleared, ovl `black` in 0 hold 20
out 6; under the black the sequence clears the intro's effects, sounds and line, removes `seat_rock` and the props (rig
`props/none`), stands her ≤ 7 b from the player facing them with the scabbard upright in her right hand (E10's end pose;
an `mv/ok` point on her line to the player), then jumps to 554: `rig/play/intro_end`, line 11 typed on the black (as the
footage's post-skip v1 f133). The intro then runs E11-E12 as usual (86 t; ≈ 6 s in all when skipped at once, instead of
32 s).
Test 30 replays the intro (boss invulnerable), test 35 skips it at tick 100. Reload during it → the end of E12.

### 3.2 CS1 — the 60 % cutscene: enrage lines + 홍련일섬 + the arena turns crimson (`seq/cs1`, clip `cs1` 213)
Trigger: the next decision after the hit that reached the 60 % floor (the running pattern finishes first). The core:
`rlk_mb_inv` from 0 until the end of CS2 (or the A8 fail), `cine/start` 0-213, the remaining P1 hazards cancelled at 0,
the boss bars off (`mboss_lib.bars(0)`, FN-f; the module's `bars` hook draws nothing while `#hud hr 0`) — the footage hides
the HUD (cutscenes.md §12) — and `#mbFloor` moved to 5 % of `mhpM`. Footage: cutscenes.md §3 (shots 1-5 before the skip,
6-11 after it), arena.md §6. From C5 on, the beats keep the footage's spacing relative to line 16 (v2 f211 = tick 144;
only the gap between lines 15 and 16 is shortened, 10 → 4 t): line 16 is on screen before the petal is cut and runs
through the slash, as in the footage (f211 vs the cut f236-f243, the negative f262, the slash f284).

| beat | source | ticks | her pose / motion | effects / arena | sounds | line |
|---|---|---|---|---|---|---|
| C0 lunge | shot 1 (v1 37.28-37.48) | 0-10 | dashes to 1.8 b in front of the player (≤ 20 b, 8 t, `mv/glide` + `mv/ok`), lilac streak; one-shot facing of the player at 0 | kit `afterimage {len}` | `entity.phantom.swoop` 0.5 pitch 1.6 at 2 | — |
| C1 blade lock | shots 2-3 (v1 37.50-38.75) | 10-32 | blades crossed vertically against the player's position, both hands on the grip, leaning in; pushing (24-30) | kit `clash_gold` at `blade_mid` at 10, `clash_arc` (orange lightning arcs between her blade and the player) 14-22 | `block.anvil.land` 0.35 pitch 1.7 + `item.trident.hit` 0.5 at 10; `entity.lightning_bolt.impact` 0.15 pitch 2.0 at 14, 18 | 13 (12-56) |
| C2 apart | shot 3 end, shot 4 (38.70-39.15) | 32-54 | pushes off: push ring r 2.5 (no damage) on the player at 32; she leaps back 6 b (`mv/leap {t:16,h:15}`), lands in a low ready stance at 52; the hat swings onto her back (40, `hat back`) | — | `item.armor.equip_leather` 0.5 at 40; `block.grass.step` 0.6 at 52 | — |
| C3 wide hold | shots 4-5 (v1 39.2 → v2 1.05) | 54-100 | low ready stance, hat on her back, blade low pointing to her left; a white glint on the blade at 96 | kit `leaves_dark {n:8}` across the sky 60-90; `glint {c:5}` at 96 | `block.amethyst_block.resonate` 0.5 pitch 1.8 at 96 | 14 (58-100) |
| C4 black | shot 6 (v2 f64-f94, 10 t; the NIKKE burst blacks out first, w2) | 100-110 | (hidden by the black) puts the hat on (104, `hat worn`: shot 7 shows her face under the brim) and sheathes for the iai draw (104, `sword sheathed`), right hand on the scabbard at the hip, left hand on the hilt | **ovl `black`** in 0 hold 10 out 3 | `block.beacon.deactivate` 0.5 pitch 0.6 at 100 | 15 (104-140), typed on the black |
| C5 the petal | shots 7-8 (v2 f95-f261) | 110-161 | iai stance, head lowered under the brim; a big red petal drifts across in front of her face **from her right to her left** (the player's left → right, as on screen in the footage) (114-126) and sinks past her mouth (126-134); then the footage's focus pull: a second petal card drifts into the player's view **1.6 b in front of the eyes** (stage-marker yaw, eye height, 0.7 b wide, turning slowly) at 128-150 and holds; a thin glowing line appears across it (faint 152, clear 154; v2 f236-f243) | kit prop `petal_big` (look `whole`) 1 b before her face at head height 114-134; a second `petal_big` (`whole` → `cut` at 154) before the player's eyes 128-169 | `block.cherry_leaves.fall` 0.4 at 114; `block.amethyst_block.chime` 0.6 pitch 2.0 at 154 | 15; 16 from 144 |
| C6 negative | shot 9 (f262-f272) | 161-165 | — | **ovl `negative`** (the approximation, §3.0) in 0 hold 4 out 0 | `entity.player.attack.sweep` 1.0 pitch 0.5 + `item.trident.riptide_3` 0.6 pitch 1.6 at 161 | 16 |
| C7 pink-white | shot 10 (f273-f283) | 165-169 | — | **ovl `pinkwhite`** (dark-red → gold diagonal line) in 0 hold 4 out 10 | — | 16 |
| C8 **홍련일섬** (A11) | shot 11 (f284-f415) | 169-213 | the draw has happened: post-slash pose, blade swept out low to her left, body twisted; with the twist the hat swings onto her back (176, `hat back`; SQ1 lifts it from there, `v2f_a_boss_far_01.jpg` f414-f444); the petal card before the player splits in two halves that fall (prop `split`) | kit `scarlet_line {len:600,yaw:<perpendicular to her → player>,roll:<rising 13° toward the player's right>}` through the player's chest point (y + 1.3), fading by 199 (cutscenes.md §3 shot 11: lower-left → upper-right, `cr_v2_a11.jpg`; F2: the line through the player's chest point — F5: the avatar's chest, 1.3 b; in first person (no avatar) at the eye, 1.2 b toward her; it slides along its own length so its low end stays 0.25 b over the floor, HR-44 / HR-45); `petal_burst {r:20}` + orange sparks at her; ovl `red_tint` in 0 hold 4 out 20 at 169; **arena look `crimson`** (4 slices 173-176); rig `phase p2` at 173; kit `leaves_dark {n:40}` 171-213 (dark-red / black leaves, arena.md §6); `leaves_swirl` round her 183-213 | `item.trident.thunder` 0.5 pitch 1.4 + `entity.generic.explode` 0.3 pitch 1.8 + `block.glass.break` 0.5 pitch 0.6 at 169; music phase 2 at 179 | 16 (to 184) |
No damage to the player (the footage: Eve's HP unchanged; `#mbCine`). The player is not knelt (the avatar is not the boss's
to animate). The footage's 25-t crossfade (f330-f405) is imitated by the slice job under the fading red tint. CS1 ends at
213 → SQ1. Footage length after the skip 117 t + ≈ 198 t seen before it; ours 213 t.

### 3.3 SQ1 — the P2 opener (`seq/sq1`, clip `sq1` 60; cutscenes.md §4, critic C29-C31)
| ticks | motion | HUD / arena | sounds |
|---|---|---|---|
| 0 | `cine/end`; she is ≈ 8 b from the player in the twisted post-slash crouch, the hat on her back; dark-red leaves swirl round her | boss bars on (`mboss_lib.bars(1)`); under bar = shield **5/5** (electro, §5.2) — the footage's HUD returns with a full shield | — |
| 6-10 | straightens | — | — |
| 10-30 | re-hat: the right hand lifts the hat from her back (10-20, `hat hand` 12) and sets it on her head (22-30, `hat worn` 28) | — | `item.armor.equip_leather` 0.4 at 28 |
| 30-42 | stand-off: still, facing the player, hands together at the hip, blade low | — | — |
| 42-52 | **darkness onset (T0 − 17)**: the `dark` look job is called at 42 and its four real slices land at 43 / 46 / 49 / 52 (far dome and moon first, the walk light last: the footage's ≈ 9-t ramp, §6.6) | arena look `dark`; no warning banner (A8's fail is non-lethal; with `ULT60_LETHAL` true the banner comes on at 43, §5.5) | `block.beacon.deactivate` 0.7 pitch 0.6 at 43; `entity.warden.sonic_charge` 0.2 pitch 1.8 at 44 |
| 46-60 | the right hand rises to the hat brim and stays (`g_brim` pose; the pre-tell critic C30 found: T−14 … T0) | — | `block.amethyst_block.resonate` 0.4 pitch 1.2 at 48 |
| 60 | **T0 of A8** (§4.5) | — | — |
Invulnerable throughout; no hazard. Length 60 t (footage v2 6.93 → 9.70 = 55 t: crouch, re-hat, stand-off); the darkness
at T0 − 17 already puts 44 t between the first visible tell and the gauntlet's first cut (T0 + 27).

### 3.4 CS2 / CS3 — the counter cinematic as a boss-only clip (`seq/repel`, clip `repel` 104)
Trigger: the shield is empty when the final dive lands (§5.4): S4's `g_deflect` (12 t: she halts 1 b above the player, a
gold starburst at the player = the player-side success feedback, she drops into the blade lock), then `seq/repel {at:60|5}`
at T0 + 206 (A8) / T0 + 270 (A13), as the footage cuts 12.3-12.7 t after the parried dive. The player cannot be animated:
we keep her half of the footage (the grab, the throw, the kick) and play it against the player's position (stage marker),
not locked. `cine/start` 0-104; she stays `rlk_mb_inv` (only the scripted true damage passes, `F:combat/apply:23`). k =
frames after the hard cut (cutscenes.md §5; the same cinematic at 60 % and 5 %, critic C38).

| beat | footage k (t) | ticks | her motion (body moves by the sequence, `mv/ok` end points) | effects | HP | sounds |
|---|---|---|---|---|---|---|
| R0 blade lock | 0-25 (0-8) | 0-8 | 1.2 b in front of the player, leaning in, blade pressed against the player's position; one-shot facing of the player at 0 | `clash_spark` at `blade_mid` every 3 t, pink-violet embers | — | `block.anvil.land` 0.3 pitch 1.8 at 0; `item.trident.hit` 0.4 at 4 |
| R1 grabbed | 25-70 (8-23) | 8-24 | the hat swings onto her back (8, `hat back`; shot 3 "hat on her back"); her sword arm is jerked up and held (as if caught); she rises on her toes, turned sideways | — | — | `item.armor.equip_chain` 0.4 pitch 0.8 at 16 |
| R2 clash on the hat | 71-83 (24-28) | 24-28 | reels from a gold-white burst on the hat on her back (shot 4) | `clash_gold` at `hat_crown` (behind her shoulders) | −1.5 % at 24 | `entity.player.attack.crit` 0.7 + `block.anvil.place` 0.3 pitch 1.6 at 24 |
| R3 tipped over | 84-130 (28-43) | 28-44 | swung round the player on a half circle r 1.5 (`mv/leap {t:16,h:10}`), body rolled with the boots high, the hat's underside to the player | — | — | `entity.player.attack.sweep` 0.6 pitch 0.7 at 30 |
| R4 back to back | 131-174 (44-58) | 44-58 | pressed 0.8 b behind the player, facing away; both turn | — | — | `block.grass.step` 0.4 at 44 |
| R5 thrown | 175-218 (58-73) | 58-73 | thrown over the player's shoulder: an arc over the player (+2.5 b) to 3.5 b in front of the player (`mv/leap {t:15,h:25}`); the hat comes off at 60 and flies 2 b aside (`hat world`) | — | — | `entity.player.attack.knockback` 0.6 at 58 |
| R6 lands on her back | 219-233 (73-78) | 73-78 | lands flat on her back | `dust_ring {r:15}` | −1.5 % at 75 | `entity.generic.big_fall` 0.6 + `block.grass.break` 0.5 at 75 |
| R7 lies | 234-307 (78-102) | 78-102 | lies on her back, the hat beside her | `repel {at:5}` only: `petal_burst {r:10}` at 80 (v3 k≈240; not in v2) | — | `block.cherry_leaves.break` 0.4 at 80 (`at:5` only) |
| R8 the kick | 308-313 (102-104) | 102-104 | a cyan-gold impact flash on her head | `kick_flash` at `head` (kept cards: the kill at 5 % happens in that tick, F2 HR-17) | 60 %: −1.5 % at 102 → the down window; 5 %: **the lethal true hit** at 102 (`mboss/true_pct {pct:100}` → `death_start` → CS4) | `entity.player.attack.strong` 0.8 + `block.anvil.land` 0.4 pitch 1.2 at 102 |
HP steps are true damage of 15 ‰ of `mhpM` through `mboss/true_hit` (`#mbTrue`; `true_pct` takes whole %): 60 % → −4.5 %
in all (footage 53 → 49 columns, −4.5 %); 5 % → −3 % then the kill (footage 5.2 → 2.3 %, then the clear cinematic).

### 3.5 SQ2 — the down window and the 5 % lead-ins (`seq/down` is core-driven; `seq/lead_down`, `seq/lead_stand`)
- **Down** (after CS2): clip `down` (loop), she lies on her back, hat beside her; `rlk_mb_inv` off, normal damage (no
  multiplier; footage v2 24.95 → v3 4.10, questions.md Q-A8), the under bar = remaining down ticks (gold, max 200). It ends
  (a) at 200 t → `kipup` (20 t, invulnerable) → the P2 decision loop after a 12-t recovery; (b) 40 t after the hit that
  reached the 5 % floor → `lead_down` → A13 (the footage: ≥ 4 s at the floor, then the kip-up).
- **`lead_down`** (82 t; v3 4.10-8.18, cutscenes.md §6, critic C43-C47): legs swing up 0, upright 7, sword vertical above
  her 10; hat at head height in the right hand 12 (`hat hand`), walks 2 b sideways holding it at shoulder height 12-48;
  **shield refill 29** (under bar 0 → 5/5 in one step, kit `shield_refill` at her, `block.respawn_anchor.charge` 0.4 pitch
  1.6); hat lifted over her head 42, **hat on 48** (`item.armor.equip_leather` 0.4); low-blade guard 48-65, a faint lilac
  glow line along the blade 56-63 (`blade lilac`); **darkness + the hand to the brim 65** (= T0 − 17: the `dark` job is
  called at 64 so its first slice lands at 65, §6.6; sounds as SQ1 43; the instant-death warning banner on only if A13's
  fail is lethal — `ULT5_LETHAL`, the default — §5.5); T0 at 82. Invulnerable throughout.
- **`lead_stand {g:a8|a13}`** (70 t; `g:a13` when the 5 % floor is reached while she is standing in P2; also the restart of
  a gauntlet `g` after a pause or a revive, §3.8 / §5.5 / §5.6): a staggering step back 0-8, takes the hat off into her
  right hand 8, walks 2 b sideways 10-30, **refill 18**, hat over 30, on 36, blade glow 44-51, **darkness + brim 53** (T0 −
  17; `dark` called at 52); the warning banner only if that gauntlet's fail is lethal (A13: `ULT5_LETHAL`; A8:
  `ULT60_LETHAL`); T0 at 70.

### 3.6 SQ3 — the ultimate (staging; the hits are §4.5, the rules §5)
Darkness from T0 − 17; the one-tick lilac switch at T0 (`form ghost`, critic C47); the warning banner on
(`ULT5_LETHAL`); ghost cuts; at T0 + 126 the yellow tell and the retreat; three moon discs; the run-in and the closing
cuts; she rises out of view and reappears high above the player **in her normal colours** (`form normal` at the
reappear, footage v3 f1213-f1216); the dive; the darkness lifts at the dive (arena look `crimson`, 4 slices) with a gold
flash (success) or the instant-death staging (§5.5); CS3 follows at T0 + 270.

### 3.7 CS4 — the clear ending (`seq/ending`, clip `ending` 1042 = H; then §7's coda; registry `death` = H + 122 = 1164)
Trigger: CS3's lethal hit → `mboss/death_start` (`#mbKilled 1`, `#mbSt 2`, bars hidden, music stopped, then the module's
`death_start` rolls §7's event (`ev/roll`, 7.3.1) and starts `seq/ending`; `deathSnd:false`; FN-c: no `poof` at the end,
she leaves, she does not die). The
footage: cutscenes.md §8 (v3 E1-E10, v4 S1-S10, v5 S1-S3). Eve's own shots (the △ input, her blade docking, her close-ups)
and the camera moves have no counterpart; the duel is played as her strikes stopping at the player in gold sparks.
One-shot facing at 0 (`rotate`: the player toward her eyes from their own eyes, the F5 avatar toward her feet; no
teleport; F2, HR-02). Profile `std` (question 7): the lines at their footage lengths, the
gaps and the duel compressed (≈ 52 s; the original ≈ 76 s with its fade). With no camera, distance does the framing: the
footage's lines are close-ups (S5-S8, v5 S1-S3), so she walks in to 4.5 b before line 17 and stays there.

| beat | footage | ticks | motion (stage = the player's spot at 0; "toward the moon" = toward `api.MOON_POS`) | effects | sounds | line |
|---|---|---|---|---|---|---|
| E1 under the hat | v3 E1 26.27-27.25 | 0-16 | lies on her back where CS3 left her (3.5 b in front of the player), the hat over her face (`hat world`) | the original's hard cut at 0 (v3 26.267: CS3's kick → the low close shot of her lying): a 3-t white flash, ovl `white` in 0 hold 2 out 1 (`seq.SEAM_CUT`; F-I, HR-31) — the hat's move from beside her (the repel's DOWN at 5 %, 1.87 b away) over her face runs under it | — | — |
| E1b ground slash (A12) | v3 f1626-f1635 | 16-28 | a lilac glint at the hat's edge (16); a broad lilac band sweeps horizontally at the player's chest height from her across the player (20-28) | `glint {c:1}` at `hat_crown`; `qi_band` with storage `seq.band` = `{len:120,yaw:0,pitch:0,roll:0,sw:<her distance to the player + 1 b, tenths>}` (it sweeps across the player wherever they stand; F2, HR-32) | `block.amethyst_block.resonate` 0.6 pitch 1.8 at 16; `entity.breeze.wind_burst` 0.6 pitch 1.2 + `entity.player.attack.sweep` 0.7 pitch 0.8 at 20 | — |
| E2 rise, glow, clash | v3 E2 27.27-28.58 | 28-62 | kips up (28-38), catches the hat and puts it on (40-46, `hat worn` 44), stands 3 b from the player facing them, arms spread, sword hand raised (48); violet glow on the raised blade 48-58 (`blade violet`; the △ moment, no input, Q-A18); gold flash between them at 58 | `clash_gold` at the midpoint at 58 | `block.respawn_anchor.charge` 0.4 pitch 1.8 at 48; `block.anvil.land` 0.4 pitch 1.5 + `entity.player.attack.crit` 0.6 at 58 | — |
| E3-E5 blade lock | v3 28.60-29.13 | 62-80 | crossed blades 1.2 b from the player, sparks | `clash_spark` every 4 t at `blade_mid` | `item.trident.hit` 0.4 at 64, 72 | — |
| E6 stance | v3 29.15-29.78 | 80-92 | slides back 3 b into a side-on stance | — | `block.grass.step` 0.4 at 80 | — |
| E7 lunge + exchange | v3 29.80-31.38 | 92-130 | lunges (92-96): the big clash at 96; yellow lightning arcs round her (98-106); three more strikes at the player at 108, 116, 124, each stopping at the player in gold sparks | `clash_gold` 96; `deco_bolt` ×3 at her 98-106; `clash_spark` 108 / 116 / 124 | `block.anvil.place` 0.3 pitch 1.7 + `entity.player.attack.strong` 0.5 at 96; `entity.lightning_bolt.impact` 0.2 pitch 1.9 at 100; `item.trident.hit` 0.4 at 108 / 116 / 124 | — |
| E8 the pass | v3 31.40-37.58 | 130-170 | crouches low, sword back (130-140), dashes past the player 8 b (140-146) with a passing strike at 143, turns (150-160), holds (160-170) | `afterimage` 140-146; `clash_spark` 143 | `entity.phantom.swoop` 0.5 pitch 1.6 at 140 | — |
| E9 strike + lock | v3 37.62-38.72 | 170-190 | dashes back in (170-174), strikes (174), blades crossed (176-186), a second flash (188) | `clash_gold` 174, 188 | as E7 | — |
| E10-S3 aerial | v3 38.73 → v4 4.55 | 190-238 | leaps up and back (190-198, +5 b, `mv/leap`), hangs 4 b from the player with the sword out to her left (198-238); three strikes toward the player at 204, 216 (overhead, the biggest), 228, white-hot clash cores between them; a blade lock in the air 232-238 | `clash_gold` 204 / 216 / 228; **ovl `white`** in 0 hold 3 out 8 at 232 | `entity.player.attack.sweep` 0.6 at 204 / 216 / 228; `block.anvil.land` 0.5 pitch 1.3 at 216; `item.trident.thunder` 0.3 pitch 1.8 at 232 | — |
| S4 landing | v4 4.57-9.12 | 238-268 | flies back in a long arc and lands crouched 10 b from the player toward the moon (on the player → moon bearing when inside walk − 1.5, else the farthest free bearing) at 258 (`mv/leap {t:20,h:40}`); thin petal streaks in the wind | `petals_wind` 240-268 | `entity.generic.big_fall` 0.4 at 258 | — |
| S5 sheathe | v4 9.13-14.05 | 268-330 | rises and turns to the player (268-272) and walks in to **4.5 b** (272-296, `walk`, `mv/glide` legs + `mv/ok`: the footage's slow push-in on her); blade low in her left hand, the scabbard upright in her right (`scabbard hand` 284); swings the scabbard down across her body (296-304); sheathes at waist height (304-320, `sword sheathed` 320); a big pink petal crosses at 306 (footage: swing f666-f684, sheathe f705-f735, line 1 from f674) | `petal_big` 306-314 | `item.armor.equip_chain` 0.3 pitch 1.6 at 296; `block.iron_trapdoor.close` 0.25 pitch 1.8 at 320 (the click); music phase 3 (once) at 300 | 17 (300-360) |
| S6 the smile | v4 14.07-18.27 | 330-440 | stands 4.5 b from the player facing them, `face smile`, head slightly tilted | — | — | 18 (368-436) |
| S8 turning away | v4 21.93-34.12 | 440-660 | lowers her head, the brim hides her eyes (494-506); turns in place, her back to the player, toward the moon (506-526); turns her face over her left shoulder (600-612), raises one open hand chest-high (612-628), smiles (628-650) | — | steps 506-526 | 19 (448-493), 20 (536-655) |
| S10-C1 moon gaze | v4 35.90 → v5 6.20 | 660-794 | back to the player, facing the moon (the player sees her from behind her shoulder, as v5 S1); looks up at it (head +15°, 690-770); the hat dips to her right (786-794, the start of the turn) | `moon_halo` brightens 680-780; `petals_heart` 740-770; `motes_warm` low 664-720 | `block.amethyst_block.chime` 0.2 pitch 0.8 at 700 | 21 (664-794) |
| C2 the greeting | v5 6.22-13.85 | 794-934 | pivots ~180° to her left in place (794-815), the sheathed sword low in her right hand sweeping flat behind her legs (801-810) → faces the player; an open-palm left-hand "let me see" gesture chest-high (860-900); a closed-lip smile (920-934) | — | `item.armor.equip_leather` 0.2 at 805 | 22 (800-930) |
| C3 the hat-tip | v5 13.87-20.33 | 934-1042 | eyes close (`face closed` 936) and her left hand rises, open palm to the player, to the brim (936-944, `hand brim`); speaks with the hand at the brim; grips the brim and pulls the hat down over her eyes with a 10° bow (980-992); eyes hidden 992-1020; her face rises under the held brim, eyes open (`face calm` 1030), looking at the player; holds, the left hand still at the brim, the sheathed sword in her right hand (1030-1042; footage f1186-f1220, the last beat before the original's fade) | `petals_heart` 1000-1030 | `item.armor.equip_leather` 0.3 at 984 | 23 (936-1026) |
**H = 1042** (`ending`'s last tick): `#sqdone`; the core starts §7's `seq/event` (7.3.2) in the same `death_tick`. The rig
stays visible (§7 hides it at E40, when she leaves in petals). The original's fade (v5 f1220-f1300) and result panel (black
→ flash → 「도전 성공 / 胜利 …」, cutscenes.md §9) are not part of CS4: §7 plays the fade at E110-E120, after the event
(the original's order ending → black → result), and the reward title at the rift carries 「도전 성공」. Tested: her distance
to the player over 300-1042 is 3.5-6 b when the player has not moved.
Profiles (question 7, `api.END_PROFILE`): `std` as above; `short` (≈ 600 t): E1b + E2's clash, the landing, the walk-in and
the sheathe, lines at 0.8 × length with 8-t gaps, the turn, the gaze, the greeting and the hat-tip; `full` (≈ 1500 t): the
footage's pacing with the duel and the aerial exchange at full length (six aerial clashes). Each profile ends in the same
H pose; `death` = its length + 122.

### 3.8 Pause, reload and the registry limits
| running | pause → resume | `/reload` |
|---|---|---|
| CS0 | freezes → continues | the end of E12 (standing, sword drawn, props and rock gone, title shown) |
| CS1 | freezes → continues | SQ1 tick 0: arena `crimson`, `phase p2`, hat on her back, music 2, bars shown |
| SQ1 / lead-ins | freeze → continue | restart the sequence from 0 (arena look forced to `crimson` first) |
| A8 / A13 | cancelled (hazards, discs, ghost, banner off; darkness lifted) → on resume `lead_stand` with `g` = that gauntlet, and the gauntlet from T0, shield 5/5. Except after a judge: deflect → CS2 / CS3, the A8 fail (non-lethal) → P2 at once, a lethal fail → the revive stance; and a lethal gauntlet (A13; A8 with `ULT60_LETHAL`) paused after its last counting cut (strike + 1: A13 T+239, A8 T+175) with pips left keeps the fail pending: the instant death lands as soon as the player is back and alive (then the revive path) | as pause (a pending fail lands at once when the player is there, else at the resume) |
| CS2 / CS3 | freezes → continues | its end: CS2 → the down window; CS3 → the lethal hit → CS4 |
| down | the timer pauses | the down continues with ≤ 100 t left |
| CS4 / §7 coda | freezes → continues (no fight tick needed: lines and effects are schedule-driven) | the framework finishes the death at once (`F:mboss/reload:3`, the reward is still paid); the reward hook applies the event the coda did not reach (7.3.4) |
Registry limits: CS0 640 ≤ `intro` 650; `death` = H + 122 = 1164 (CS4 1042 + §7's coda 120 t + a 2-t margin, 7.1.2).
Every line ends inside the death state (`cleanup_fight` clears the kit HUD at `sp/won`, framework.md §1.10).

---------------------------------------------------------------------------------------------------------------------

## 4. Patterns, AI and difficulty (S3 `p1.py` + `ai.py`; S4 `p_ghost.py`)

### 4.1 Common rules
- **Hazards**: only the framework's `mboss/hz/{disc,ring,sector,line,full}`, `pj/launch`, `pl_dot`, `mv/*`, `push_ring`,
  through `mboss_lib.hz_opts` / `pj_opts`; every one quiet (`#hzQuiet 1`), no `tele`, **no floor decal** (§1.4). Every hit
  Electro (`el 3`) 1U with the normal player-side reactions.
- **Telegraph rule** (README 0-6 10-20; questions.md Q-B7): first visible motion → hit ≥ 12 t; ≥ 20 t for big (area ≥ 100
  b², r ≥ 8), undodgeable or yellow-tell attacks; chain hits ≥ 10 t apart; aims lock **7 t** before the hit (`api.LOCK_LEAD`).
  Only the windups are stretched (the footage's 3.3-14.7-t windups, patterns.md §8); strike motions keep the footage speed;
  the footage gaps inside chains (12-16 t) are kept; the two 9-t gaps of the gauntlets (A8.6 → A8.7) become 12.
- **Knockback**: only the last hit of a chain (kb 3 = 0.6 b); single-hit patterns kb 2; gauntlet cuts kb 0 (README 0-6, 타키).
- **Tracking chains** (타키 R2): before each chain hit she re-aims (≤ 10° per tick) and steps 0.3 b toward the player
  (stops when blocked or at 2.4 b).
- **Movement safety**: every end point (landing, dash end, blink, reappear) through `mv/ok` + leash inside `api.MOVE_R`
  = safe − 0.5 = 22.5 b (what `F:mboss/ar/<aid>/ok` accepts, e.g. `F:mboss/ar/tk_lift/ok:1-2`); every reappear / landing
  list ends with a guaranteed fallback (the point on the player → C line ≤ 21 b from C); the walk disc is flat full
  blocks with nothing overhead below y 226, so leaps never enter blocks; parts never below the floor (rig gate).
- **Recovery** between patterns: P1 8-16 t (S5, the knob's −4 t), P2 10-16 t (`api.RECOVER`), walking / strafing facing the player (0.12 b/t; P2
  `glide` 0.18 b/t) — the punish window. Every P1-kit pattern ends 8-12 t after its last hit (`api.PAT_END`: A1 24, A2 22,
  A3 79, A4 46, A9 40, A10 32; A6 at 16 as before), R1 / R3 12 t after theirs (67 / 49). During a tail kept she turns to
  track the player every tick and walks / strafes facing and tracking them as in the recovery (walk / P2 glide in beyond
  6 b, else a strafe; `ai/tail` = the recovery's move and clip, `ai/tail_step` = one step each later tick): from
  `api.TAIL_MOVE` = 4 t after the last hit (the clip's follow-through plays until then; A4 from its landing 38), R1 / R3
  from the solid row (62 / 46: the reform is over, she is hittable), R2 from 4 t after its last release (32 / 46). The
  recovery that follows keeps that move and its clip while it still fits the band (walk / glide in beyond 6 b, a strafe
  nearer; `ai/tail_keep`: no new pick, no strafe flip, no clip restart), else it picks anew. She never stands still longer
  than that outside scripted beats (no long waits). **This rule wins over §4.3's / §4.4's clip tails.** (F1, HR-14; F-I
  checked the hand-over on S2d's rig: the move clip's blend from the attack clip turns a part ≤ 50°/t (a strafe / walk),
  ≤ 56°/t into the P2 glide — the glide's own entry from idle is 57°/t, the attack clips' own swings 75-109°/t — so no pose
  pops; `HR/renders/fi_tails.jpg`.)
- **Ghost state** (gauntlet moves, R1, R3): while vanished or in ghost form the body is `rlk_mb_inv` and tagged
  `rlk_hr_ghost` (parked at her last spot while hidden, as 타키's K); she is solid and hittable again after `g_reform`.
- **Colours** (kit arg `c`): 1 lilac sword-qi `#C97EDD` / rim `#FFE6FA`; 2 pink-magenta (A1's glint and fan, A4's glint,
  A9's cut, A8.8's glow; v1.md B1 / B2);
  3 yellow tell `#FFE14A`; 4 crimson (P2 accents, 홍련일섬); 5 white glint.

### 4.2 Damage and shapes
`mboss/hurt` coefficient % (`api.DMG`) × `atk` 12 × `dmgMul` 135 (1.00 = 16.2 raw). Tiers from 타키's final values:
**T1 29, T2 42, T3 62, T4 71** (README 타키; S5 moved T3 56 → 62, +10.7 %: `mboss/hurt`'s raw hit 9 → 10, §4.8); S5 may move them ±20 %. Shapes: `sector(r, half°)`, `disc(r)` (around her),
`line(len, w)`, `pdisc(r)` = a disc at the player's spot (the gauntlet cut builder, §5.3), `pj_disc` (the A7 projectile,
§4.5). Sizes follow questions.md Q-B10: areas centred on the player keep the footage metres (1 m = 1 b); reaches tied to
her body scale × 1.5 (2.55 b / 1.7 m).

### 4.3 Phase-1 entries (S3 `p1.py`; `ref` = `HR/ref` sheets)
**A1 회전 반월참 — Turning Crescent Cut** (v1 9.667-10.400, f580-f624; `cr_v1_a1.jpg`, `v1s_a2_*`, `mg_p1_areas.jpg`)
- When: the counter trigger (§4.7) with the player beside or behind her (|bearing| > 45°), the rear rule, or the P1 near
  pick (weight 10; both only inside the near band, §4.7).
- Clip `a1` 34: pivot 0 (the brim swings round), a magenta blade glint 6 (the only cue in the footage), lock 7, a rising
  vertical magenta fan of sword-qi 10 (cosmetic, `qi_fan {h:16,c:2}`), **hit 14**: the flat crescent `sector(4.0, 80)`
  **T2 kb 2**. The pattern ends at 24 (she turns to the player 15-23 and walks / strafes from 18, §4.1), then the AI
  recovery. Footage glint → hit 6 t, first motion → hit 8 t → stretched to 14.
- FX / sounds: `glint {c:2}` 6; `qi_fan {h:16,c:2}` 10 (standing across her aim, bulging to her left, F2 HR-12; at her
  body + 1.1, 1.2 b ahead — S2d's x 0.78 had made it h 13 at + 0.85, 189 px from the F5 camera; V2, HR-48: h 16 again, ≥ 250
  px on ≥ 3 ticks in F5); `qi_arc {r:40,yaw:0,pitch:0,roll:-25,c:1}` 14 (the crescent is purple, v1.md B1; V2, HR-48: rolled
  −25° so it stands across her aim as A2's does — the flat one at the body + 1.0 read in first person on one tick only; now
  ≥ 1 500 px on ≥ 3 of 7 ticks in F5 and in first person); `entity.player.attack.sweep` 0.6 pitch 1.3 at
  10, `entity.breeze.wind_burst` 0.4 pitch 1.5 + `block.amethyst_block.resonate` 0.5 pitch 1.7 at 14.
- Answer: step out of 4 b or dash.

**A2 역습 일섬 — Combo-Breaker Slash** (v1 19.050-19.500, f1143-f1170; `cr_v1_a2a6a5.jpg`, `v1s_a8_*`)
- When: the counter trigger with the player in front (|bearing| ≤ 45°), or the P1 near pick (weight 10).
- Clip `a2` 30: pale lilac glints on her lower body / blade 0, the blade drawn (white streak) 4, lock 5, lilac glow along
  the blade 6-11 with a hook crescent at the tip at 10, **hit 12**: upper-right → lower-left `sector(3.6, 70)` **T2 kb 2**;
  the pattern ends at 22 (she turns to the player 13-21; from 16 she walks / strafes, §4.1: the move clip takes over from
  the raised sword's follow-through). The lilac glow 6-11 is the rig look `blade lilac` from the `glow` event (6), off at
  the hit and in A2's cancel (A6 may cancel the windup; F1, HR-22). Footage glint → hit 4.3 t (the fastest) → 12.
- FX / sounds: `glint {c:1}` 0; `qi_arc {r:36,roll:35,c:1}` 12 (the hook is purple, v1.md B5); `item.trident.throw` 0.4
  pitch 1.6 at 4, `entity.player.attack.sweep` 0.7 pitch 1.5 at 12.

**A3 오연 반월 — Five-Crescent Combo** (v1 23.150-26.300, f1389-f1578; `cr_v1_a3_leads.jpg`, `v1s_a12*`, `v1s_combo5`)
- When: near (≤ 4.5 b); at 4.5-8 b she glides in 0.3 b/t during 0-14.
- Clip `a3` 96: glint 0; **h1 14** giant vertical wrap-around crescent `sector(4.2, 90)` T1; **h2 30** short lunge (1.5 b)
  + downward diagonal `sector(4.0, 60)` T1; **h3 45** vertical `sector(4.0, 50)` T1; **h4 57** overhead vertical
  `line(5.0, 1.8)` T1; **h5 69** rising diagonal wedge `sector(4.6, 70)` **T2 kb 3**. Locks at h − 7; re-aim + 0.3 b step
  before h2-h5. Gaps 16 / 15 / 12 / 12 (footage 16 / 14.7 / 12.3 / 12.3). The pattern ends at 79 (she turns to the player 70-78 and walks / strafes from 73,
  §4.1), then the AI recovery (the footage leaves her open after hit 5). First glint → h1 3.3 t in the footage → 14.
- FX / sounds: `qi_vert {h:34,yaw}` across her aim (F2, HR-12; S2d's body: h 27 at her body + 0.15) — h1 yaw 0 1.4 b
  ahead (bulging to her right = the player's left, the footage's 'at Eve's left'), h3 yaw 180 1.4 b ahead (to her left), h4
  yaw 0 2.0 b ahead (toward where line(5.0, 1.8) reaches, still before a player at the 2.4-b chain stop; F-I kept 2.0 b: at
  3.0 / 3.5 b it stands behind that player and first person sees nothing, 0 px, F5 3 319 / 4 123 px vs 2 259); `qi_arc
  {r:40,roll:-35,c:1}` h2 and `qi_wedge {r:46,roll:40}` h5 stand across the aim and are rolled in that (screen) plane;
  `entity.player.attack.sweep` 0.6 at each hit (pitch 1.2 → 1.6 rising), + `entity.breeze.wind_burst` 0.5 at h5.

**A4 월하 낙참 + A5 공중 원륜 — Moon-Leap Dive + Aerial Ring Spin** (v1 10.800-12.550, f648-f753; `cr_v1_a4.jpg`, `v1s_a3_*`, `v1s_a4_*`)
- When: mid / far (4.5-14 b) — a gap closer.
- Clip `a4` 60: crouch 0, **leap 2** (rises 6 b in 4 t and travels ≤ 10 b toward the player, `mv/leap`), apex 6-13 (hangs
  7 t; a magenta-lilac glint along the blade 7-12 = the tell, the footage's only one), lock 12 (the player's spot), flip 13-16
  (a sword-qi ribbon wraps round her), dive 16-20 onto the locked spot (an S-shaped ribbon from the sky), **hit 20**:
  `disc(2.6)` at the landing **T3 kb 0**; A5: crouch 22, a straight slash line 25 (cosmetic; F2, HR-12: `qi_line {len:100}` from 5 b on her left across her facing,
  her + 0.95 b (S2d's body), 1.5 b ahead: the footage's long horizontal slash from the frame's left edge), lock2 27, she spins ~1 b off
  the ground 28-33 (a flat lilac ring at head height), **hit2 34**: `disc(3.0)` round her **T1 kb 2**; land 38; the pattern
  ends at 46 (she turns to the player 35-45 and walks / strafes from the landing 38, §4.1). First motion → hit 20 (footage 19.7); chain gap 14 (footage 14.5). Apex 7 t (no hovering).
- FX / sounds: the afterimage trail along the leap in both phases (the kit `afterimage {len:15}` at her body at 2 / 4 / 6:
  start, middle, apex; F1, HR-28); `glint {c:2}` 7; `qi_ribbon` 13-20 (its cards follow her, `fx/follow_on` .. `follow_off`:
  F2, HR-23); `dive_impact {r:26}` 20; `qi_ring {r:30,c:1}`
  28-34; `entity.breeze.jump` 0.5 at 2; `block.amethyst_block.resonate` 0.6 pitch 1.9 at 7; `entity.phantom.swoop` 0.5 pitch
  1.4 at 14; `entity.generic.explode` 0.3 pitch 1.7 + `block.amethyst_block.break` 0.7 at 20; `item.trident.riptide_1` 0.5
  pitch 1.5 at 30.

**A6 후방 섬보 — Back-Blink + 「거기가 아닐세.」** (v1 16.233-16.367 + line v1 16.833-19.967; `cr_v1_a6.jpg`, `v1s_a7_*`)
- When (the wiki's "근접 베타스킬 사용 중엔 … 회피", W4): a skill or burst hit on her (`#skillDmg tmp 1` read in `on_hit`)
  while the player is ≤ 4.5 b and she is between patterns or in the first 6 t of a windup; 60 %; cooldown 400 t in both phases
  (§4.8's cap: at most one per 20 s; F1, HR-38);
  never in the first 200 t of a phase.
- Clip `a6` 20: a pale blue-white translucent bubble 0 (`blink_bubble`, following her: F2, HR-23), she glides 12 b straight back in 3 t (`mv/glide
  {t:3}`; blocked → 8-10 b to a side), appears in stance 4, settles 10; `rlk_mb_inv` 0-4 (the rest of the skill misses).
  No hit. **Line 12 at 12** (63 t). The next decision comes 16 t later; from far she then closes (§4.7).
- Sounds: `entity.illusioner.mirror_move` 0.7 pitch 1.3 at 0; `entity.enderman.teleport` 0.2 pitch 1.8 at 3.

**A9 황광 원참 — Yellow-Ring Grand Slash** (v1 13.067-14.733, f784-f884; `cr_v1_a9_ring*.jpg`, `cr_yellow_cmp.jpg`, `v1s_a5_*`, `v1s_a6_*`)
- When: near / mid (≤ 7 b).
- Clip `a9` 64: turn 0 (a lilac streak at her right), counter-clockwise spin 3, a flat lilac ring round her waist at 4
  (the blade's sweep plane, r 3.5, cosmetic — critic C5 left open whether it hit; we do not make it one), **yellow tell 8-16**
  (sphere Ø 1.6 + horizontal flare line; footage 5.7 t), a lilac 4-point star + thin circle at her chest (anchor `chest`,
  upright, facing the player, Ø 1.7 b; v1.md B3 "star glint at her") 17-22,
  lock 22, **full-screen magenta** at 24 (ovl `magenta` in 0 hold 3 out 6; footage f830-f878), go 26 (an iai dash through
  the locked point to 3 b beyond, ≤ 12 b, `mv/glide {t:2}` + `mv/ok`), **cut 28**: `line(dash, 2.4)` + `disc(4.0)` at the
  locked point, one group, **T3 kb 3**. The pattern ends at 40 (she stands beyond the player, back turned, turns back to
  them from the cut on and walks / strafes from 32, §4.1). First
  motion → hit 28 (footage 18).
- FX / sounds: `qi_ring {r:35,c:1}` 4; `yellow_tell {t:8}` 8; `star4` 17; `qi_cut` with storage `core.a9` (len = the probed dash length, the
  hazard line's own compound; F2, HR-24) + `qi_ring {r:40,c:2}` 28;
  `block.bell.use` 0.6 pitch 1.5 + `block.beacon.power_select` 0.5 pitch 1.9 at 8 (the yellow chime, shared by A10 and A7);
  `block.amethyst_block.chime` 0.8 pitch 2.0 at 17; `entity.illusioner.cast_spell` 0.6 pitch 1.4 at 24;
  `item.trident.riptide_3` 0.6 pitch 1.6 + `entity.player.attack.sweep` 1.0 pitch 0.6 at 28.

**A10 황광 낙참 — Yellow Plunge** (v1 20.000-21.700, f1200-f1302; `v1s_a10_*`, `cr_yellow_cmp.jpg`)
- When: near / mid / far (P1 near weight 40, S5; F1 gave it 20: the plunge on the locked spot is the move that reaches a player hugging her;
  F1, HR-13) — the second gap closer.
- Clip `a10` 56: crouch 0, **spring 2** (rises 5 b, drifting toward the player ≤ 0.4 b/t), apex 8-20 (crouched; **yellow
  tell 10-18** in the air; footage 4.7 t), lock 14, dive 20-22 (a curved lilac trail; 3-4 claw-like lilac streaks fall from
  the sky onto the locked spot at 20), **hit 22**: the landing burst `disc(3.5)` **T3 kb 3**; the pattern ends at 32 (she turns to the player 23-31 and walks /
  strafes from 26, §4.1). First motion
  → hit 22 (footage 14). Apex 12 t (no hovering for seconds).
- FX / sounds: the afterimage trail along the spring (2 / 5 / 8) and the dive (20 / 21) in both phases, the dive's lilac
  line from her toward the locked spot at 20 (`qi_line {len:60}` from her body + 0.8, `facing entity <lock> feet rotated
  ~-90 ~`: the kit's line runs across its facing, F2-7; the kit clamps it above the floor; F1, HR-28); `yellow_tell {t:8}`
  10 (its cards follow her through the apex drift, F2, HR-23); `claw_streaks {r:15}` 20; `burst_radial {r:35}` 22;
  `entity.breeze.jump` 0.5 at 2; the yellow chime at 10; `entity.phantom.swoop` 0.6 pitch 1.2 at 20;
  `item.mace.smash_ground` 0.6 + `block.amethyst_cluster.break` 0.7 at 22.

### 4.4 Phase-2 entries (S4 `p_ghost.py`) and the enraged P1 kit
The P1 entries stay with their timings and ends (questions.md Q-A1 default; §4.1); P2 adds `idle2`, `glide`, the lilac
`afterimage` on A3's glide, A6's blink and A9's dash (A4's leap and A10's spring / dive have their trails in both phases,
§4.3), recoveries 10-16 t, cooldowns × 0.85 rounded to 10 t (A9 160 → 140, A10 120 → 100 (S5); A6 400 in both phases). Three P2-only entries are cut from the gauntlets' footage moves
(the wiki's 순식간에 거리를 좁히는 돌진기 / 연속 돌진기 / 즉발성 원거리 견제, W1-W3):

**R1 자영 돌격 — Ghost Rush** (= the gauntlets' opening block: A8.T, D1, A8.1-A8.3, without shield or darkness)
- When: mid / far. T0 = start. Lilac switch 0 (`form ghost`, `rlk_mb_inv`), burst 3, hidden 4; reappear 14 b at the
  player's front-left 14 (`g_dash`), dash 20-24 to 1.5 b at the player's right; **hit1 27** `pdisc(3.2)` T2 (made 14,
  lock 20); **hit2 40** `pdisc(3.2)` T2 (made 27, lock 33); **hit3 55** (she leaps over the player) `pdisc(3.2)` **T3
  kb 3** (made 40, lock 48); she lands 3 b beyond the player and reforms 55-62 (`g_reform`, hittable at 62; from 62
  she walks / strafes facing the player, §4.1, no `idle2`); the pattern ends at 67 (12 t after the last hit), then the P2
  recovery (keeping that move).

**R2 월륜 일섬 — Moon Disc** (= one A7 disc after the yellow tell)
- When: mid / far. Clips `a7_tell` + `a7_throw`: a step back 0, **yellow tell 2-10**, retreats 6 b (glide 4-14, `mv/ok`),
  settles 14; crouch 16, blade up 20, crescent 22, spin 23-27, **release 28**: one `pj_disc` (§4.5) aimed at its lock —
  the player's floor spot 7 t before the release (21; she faces it from then on) — arriving ≈ 34-36 (first visible motion
  → arrival ≥ 32 t; lock → hit ≥ 7 t + the flight). At ≤ 30 % HP a second disc: spin 36-40, lock 35, release 42. From 4 t
  after the last release (32 / 46) she moves as in the recovery (glide in beyond 6 b, else a strafe; facing the player)
  until 60 (F1, HR-15 / HR-14). T2; the last disc kb 2.

**R3 자영 활강 — Ghost Glide** (= the gauntlets' second block: A8.T, D2, A8.4, A8.5)
- When: near / mid. Lilac switch 0, burst 3, hidden 4; reappear low 8 b at the player's front-right (+55°) 10 (`g_glide`),
  glides to 1.6 b at the player's front-right 11-19; **hit1 24** `pdisc(3.2)` T2 (made 10, lock 17; she springs up and hangs turning
  24-32); **hit2 37** `pdisc(3.2)` **T3 kb 3** (made 24, lock 30; the X); reforms 37-46 (from 46 she walks / strafes facing
  the player, §4.1, no `idle2`); the pattern ends at 49 (12 t after the last hit).

### 4.5 The gauntlets A8 (60 %) and A13 (5 %) — S4 (`p/a8`, `p/a13`), rules in §5
**Move set** (patterns.md §5, critic C30-C58; one ghost at a time; every cut = a counting `pdisc(3.2)` on its own tier TC 37
(`api.DMG['TC']`; raw 5 = 12 HP on the item-less Lv15 player, 9 cuts 40.3 % ≤ 45 %; F1, HR-19) kb 0, Electro,
made ≥ 12 t before its strike, following the player until the lock at strike − 7, §5.3). The sword-qi shapes are effects
at the contact tick:

| id | move | clip | her motion (relative to the player's facing) | effect at contact (kit) | sounds |
|---|---|---|---|---|---|
| A8.T | tell + vanish | `g_tell` 12 | the whole body incl. the hat turns lilac in one tick (0), holds 3 t; bursts into lilac-white mist at 3; white-lilac ribbons trace the silhouette and the brim 3-8; sparkles gone by 12 | `ghost_burst` | `entity.illusioner.prepare_mirror` 0.7 pitch 1.0 + `block.amethyst_block.resonate` 0.7 pitch 1.2 at 0 |
| D1 | far reappear + dash | `g_dash` 12 | appears 14 b away at bearing −40° (front-left; fallback +40°, 0°, ±90° at 10 b), hovers / grows 6 t, dashes straight to 1.5 b at the player's right in 4 t, leaning forward, sword trailing | `ghost_trail {len}` (lilac flame trail + white speed lines) | `entity.illusioner.mirror_move` 0.5 pitch 1.6 at 0; `entity.phantom.swoop` 0.4 pitch 1.8 at 6 |
| D2 | side reappear + glide | `g_glide` 12 | appears low 8 b at the player's front-right (+55°: inside the default F5 view near its edge, FOV 70: 39° off the camera axis of 51.2° at 16:9 / 48.2° at 16:10; F1, HR-27), glides legs forward, a sliding stop at 1.6 b front-right (+45°) | `ghost_trail` | as D1 |
| D3 | flash-blink drop | `g_drop` 14 | flashes white-violet (electric texture) 0, dissolves into rising white ribbons 2, rematerialises 2.5 b out and 3 b up at the player's up-right (+60°) at 7, drops diagonally onto them 7-12 | `ghost_flash`, `ghost_burst` | `entity.illusioner.cast_spell` 0.5 pitch 1.8 at 0 |
| D4 | far reappear + run-in | `g_run` 14 | vanishes with a purple glow and a white ring outline; appears 12 b at the player's front-left (−55°: 43° off the default F5 camera axis; F1, HR-27), runs in on foot, sword back (2-10), lunges with the sword overhead (10) | `ghost_burst`, `ghost_trail` | footsteps `block.grass.step` 0.3 ×3 |
| A8.1 | 원륜참 ring cut | `g_ring` 14 (hit 3) | crouched at the player's right; the arc wraps down from the player's upper-left and closes into a horizontal ring round them at waist / knee height; then spins in place | `qi_ring {r:22,c:1}` at the player | `entity.player.attack.sweep` 0.7 pitch 1.3 + `block.amethyst_block.resonate` 0.4 |
| A8.2 | 역사선 올려베기 rising diagonal | `g_rise` 14 (hit 9) | spins in place at the player's right 0-6, arms up 6, cuts a band from the player's lower-left ground to the upper right, riding its upper end | `qi_band {len:70,yaw:0,pitch:35,roll:0,sw:25}` (the 2.5-b sweep it always had, F2) | sweep pitch 1.1 |
| A8.3 | 도약 사선 내려베기 leaping overhead | `g_leap` 18 (hit 9) | coils at the player's right 0-5, sword overhead, leaps over the player (`mv/leap {t:6,h:30}`) cutting upper-left → lower-right; tumbles above them 10-16, vanishes there 16 | `qi_arc {r:45,roll:-40,c:1}` (white edge), 2 b ahead of the cut spot in the player's facing (standing across it: on the player's own plane first person would see nothing; F2) | `entity.breeze.jump` 0.4 at 3; sweep pitch 1.0 |
| A8.4 | 지면 횡베기 low sweep | `g_sweep` 14 (hit 3) | sword arm back 0; a very wide flat crescent / ring at ground level round the player; springs straight up and hangs upright, turning 4-14 | `qi_ring {r:30,c:1}` at y + 0.1 | sweep pitch 0.8 + `item.trident.riptide_1` 0.4 |
| A8.5 | 사선 내려베기 · X | `g_x` 16 (hit 6) | drops at the player's right 0, sword swung up behind 2, a big crescent upper-right → lower-left crossing A8.4's trail into an X at the player's feet; stays close 6-14, vanishes 14 | `qi_x {r:25}` (in first person — no avatar — the X sits 1.2 b ahead of the cut spot, its arms still cross it: at the player's feet it is out of view; F2) | sweep pitch 1.2 |
| A8.6 | 감아베기 low wrap-around | `g_wrap` 12 (hit 3) | lands at the player's side, a flat crescent from the player's lower-left round their legs rising to the right | `qi_arc {r:40,roll:15,c:1}` at 0.8 b (thigh height; at 0.4 b the floor clamp shrank it to a sliver from the F5 camera; F2) | sweep pitch 1.0 |
| A8.7 | 회전 돔 spin dome | `g_dome` 12 (hit 3) | a swirl over the top 0, a 360° spin: a ring with a pink-white rim at waist height + a translucent dome that expands to a thin white outline and fades | `qi_dome {r:35}` | `item.trident.riptide_2` 0.5 pitch 1.4 |
| A8.8 | 수직 올려베기 rising vertical | `g_vert` 20 (hit 5) | crouched low at the player's right, blade low; **pink blade glow** 1-4 (`blade pink`); springs up cutting vertically (a tall crescent at the player's right, ground to above the head); rises tumbling 8 b up and out of view (hidden 18) | `glint {c:2}`, `qi_vert {h:34,yaw:0,c:2}` 1.5 b to the player's right and 1.5 b ahead, standing across the player's facing (F2) | `block.amethyst_block.chime` 0.6 pitch 1.9 at 1; sweep pitch 1.5 at 5 |
| A8.9 | 낙하 일격 the dive (the judge) | `g_dive` 10 (hit 6) | reappears 6 b above the player **in her normal colours** (`form normal`), sword overhead, dives head-first, blade pointing down (a thin vertical blade line 1-2 t before the hit) | success: `g_deflect` + gold starburst + `light_column`; fail: §5.5 | `entity.phantom.swoop` 0.7 pitch 1.0 at 3 |
Decoration (questions.md Q-A12): thin yellow lightning `deco_bolt` 3-6 b from the player, no hit box, no sound but
`entity.lightning_bolt.impact` 0.15 pitch 1.9 — A8 at T + 34 / 102 / 161 / 193 (v2 11.42 / 14.80 / 17.77 / 19.37), A13 at
T + 70 / 225 / 245 / 258 (the footage's bolts at the second D1 dash, U9, the rise and the dive, v3 f696 / f1124 / f1186 /
f1246, put on the plan's timeline).

**A8 script** (v2 9.700-19.700; T0 = SQ1 60; footage T+ in brackets; "made / lock / strike" = the cut's hazard ticks):
| T+ | step | clip (start) | cut hazard made / lock / strike |
|---|---|---|---|
| −17 / −14 | darkness / hand to the brim (SQ1) | `g_brim` | — |
| 0-12 | A8.T [0-12.7] | `g_tell` 0 | — |
| 14-24 | D1 [14.7, 20-24] | `g_dash` 14 | cut 1: 14 / 20 / 27 |
| 27 | A8.1 [27.0] | `g_ring` 24 | cut 2: 27 / 33 / 40 |
| 40 | A8.2 [39.8] | `g_rise` 31 | cut 3: 40 / 48 / 55 |
| 55 | A8.3 [55.0] (vanishes in the air 62) | `g_leap` 46 | — |
| 70-79 | D2 [73-78] | `g_glide` 70 | cut 4: 70 / 75 / 82 |
| 82 | A8.4 [80.2] | `g_sweep` 79 | cut 5: 82 / 87 / 94 |
| 94 | A8.5 [92.3] (vanishes 103) | `g_x` 88 | — |
| 108-118 | D1 [106, 112-116] | `g_dash` 108 | cut 6: 108 / 114 / 121 |
| 121 | A8.1 [~118] | `g_ring` 118 | — |
| 130-142 | D3 [127-141] | `g_drop` 130 | cut 7: 130 / 140 / 147 |
| 147 | A8.6 [~144] | `g_wrap` 144 | cut 8: 147 / 152 / 159 |
| 159 | A8.7 [~153; 9-t gap → 12] | `g_dome` 156 | cut 9: 159 / 167 / 174 |
| 174 | A8.8 [~168] (pink glow 170-173, rises out of view, hidden 186) | `g_vert` 169 | — |
| 188-194 | A8.9 [187.7]: reappears 188, dives, **judge at 194** (20 t after cut 9) | `g_dive` 188 | — |
| 194 | darkness lifts (arena look `crimson`, slices 194-197) | — | — |
| 194-206 | success: `g_deflect` → CS2 at 206 [200.3]; fail: §5.5, `g_reform` 194-204, P2 decision at 214 | — | — |

**A13 script** (v3 8.200-21.083; T0 = the lead-in's end):
| T+ | step | clip (start) | cut hazard made / lock / strike |
|---|---|---|---|
| −17 | darkness, hand to the brim, warning banner on | (lead-in) | — |
| 0-12 | A8.T [0-10.3] | `g_tell` 0 | — |
| 14-24 | D1 [14.7, 21.3-25.7] | `g_dash` 14 | U1: 14 / 20 / 27 |
| 27 | U1 A8.1 [27.7] | `g_ring` 24 | U2: 27 / 33 / 40 |
| 40 | U2 A8.2 [40.0] | `g_rise` 31 | U3: 40 / 48 / 55 |
| 55 | U3 A8.3 [54.5] (vanishes in the air 62) | `g_leap` 46 | — |
| 67-77 | D1 [67, 74-78] | `g_dash` 67 | U4: 67 / 73 / 80 |
| 80 | U4 A8.1 [80.3] (vanishes 89) | `g_ring` 77 | — |
| 96-105 | D2 [98, 99-105] | `g_glide` 96 | U5: 96 / 101 / 108 |
| 108 | U5 A8.4 [107.7] | `g_sweep` 105 | U6: 108 / 113 / 120 |
| 120 | U6 A8.5 [119.7] (vanishes 128) | `g_x` 114 | — |
| 129-141 | reappears 3 b from the player inside the **yellow tell** (129-137; its cards follow her: F2, HR-23) [130.7-138], retreats to 12 b (131-141) onto a lilac sparkle cloud | `a7_tell` 127 | — |
| 143-155 | disc 1: crouch, blade up, crescent, spin + **gold blade line** 150-154 (`blade gold`), **release 155** → at the player ≈ 162 [145.3] | `a7_throw` 143 | `pj_disc` |
| 155-167 | disc 2 (inside a tilted saturn-like ring), **release 167** → ≈ 174 [~157] | `a7_throw` 155 | `pj_disc` |
| 168-180 | disc 3 (running crouch, lilac wedge on the blade), **release 180** → ≈ 187 [~170] | `a7_throw` 168 | `pj_disc` |
| 187-194 | stands far; vanish 5 at 194 (purple glow + white ring) | — | — |
| 198-208 | D4 [189.3, 192-201] | `g_run` 198 | U8: 198 / 204 / 211 |
| 211 | U8 A8.6 [~202] | `g_wrap` 208 | U9: 211 / 216 / 223 |
| 223 | U9 A8.7 [211.3; 9.3 → 12] | `g_dome` 220 | U10: 223 / 231 / 238 |
| 238 | U10 A8.8 [~226] (pink glow 234-237; rises, hidden 250) | `g_vert` 233 | — |
| 252-258 | U11 A8.9 [245.7]: reappears 252 in normal colours, dives, **judge at 258** | `g_dive` 252 | — |
| 258 | darkness lifts (success) / the instant death (§5.5) | — | — |
| 258-270 | success: `g_deflect` → CS3 at 270 [258] | — | — |

**A7 disc** (`pj_disc`; patterns.md A7, questions.md Q-B9): `pj/launch` blade shape (`#pjShape 1`), half width hr 1.4
(2.8 b wide; the footage 2.5-3.4 m at Eve), height 0.2-2.4 b (a jump does not clear it), 1.8 b/t (the footage is near-
instant; ≈ 7 t of visible flight from 12 b), life 16 t, wall stop, aimed at its lock: a floor marker at the player's feet 7 t
before the release (`g/disc/lock`, `api.DISC_LOCK`: R2 21 / 35, A13 148 / 160 / 173; she faces it from then on), so lock →
hit = 7 t + the flight at any distance (F1, HR-15); no homing; one card per disc (kit prop `disc`, horizontal, spinning 30° per tick, facing its flight; summoned
then rotated, README 0-6); **T2**, kb 0 (the last disc of R2 kb 2), Electro; dodgeable; never counts for the shield
(yellow = unblockable in the original, questions.md Q-B8). Release: `item.trident.riptide_2` 0.6 pitch 1.7 +
`entity.breeze.shoot` 0.5; flight `item.trident.throw` 0.3. The yellow tell (`yellow_tell {t:8}` + the yellow chime) comes
≥ 20 t before the first disc arrives (A13: 129 → 162).

### 4.6 Phase machine (S3 `core.py`; floors as 타키 / 아를레키노: the hit reaching a floor stops there, the step starts at the next decision)
1. `spawn` → **intro** CS0 (640; skipped → from 554) → **P1**, `#mbFloor` = 60 % of `mhpM`, `phases [100]`.
2. 60 % floor hit → the running pattern finishes → **CS1** (213; `rlk_mb_inv`, `cine`, bars off, floor → 5 %) → **SQ1** (60)
   → **A8**.
3. A8 judge at T + 194: shield 0 → `g_deflect` → **CS2** `repel` (104, −4.5 % true) → **down** (≤ 200 t; damage normal) →
   `kipup` (20) → **P2**. Shield > 0 → **fail-60** (§5.5) → `g_reform` → **P2** (no counter, no down; a pause / reload
   between the judge and T + 214 goes to P2 at once: F1, HR-01).
4. P2 (the P1 kit with shorter recoveries + R1-R3). 5 % floor hit → the running pattern finishes (or, from the down window,
   40 t later) → `lead_stand {g:a13}` (70) / `lead_down` (82) → **A13**.
5. A13 judge at T + 258: shield 0 → `g_deflect` → **CS3** `repel` (−1.5 %, −1.5 %, the lethal true hit at 102) →
   `death_start` (+ `ev/roll`, 7.3.1) → **CS4** `ending` (1042 = H) → §7's coda `seq/event` (120) → `death_finish` at
   H + 122 = 1164 (no `poof`, FN-c) → `sp/won` → `sp/reward` (+ the FN-b hook, 7.1.4).
   Shield > 0 → **the instant death** (§5.5); a revived player → `lead_stand {g:a13}` → A13 again (shield 5/5).
Invulnerable windows: the intro; CS1 → the end of CS2 (incl. SQ1 and A8; only the scripted true damage passes); `kipup`;
the lead-ins → CS4; the ghost states of R1 / R3; A6 ticks 0-4. Test hooks: `boss/test/pattern {id}` (§9.2). A reserved
step (`#fl`: CS1 / the A13 lead-in) is not delayed by a trigger: the counter (A1 / A2) and the skill trigger (A6) do not
start while it is reserved (F1, HR-04).

### 4.7 AI (S3 `ai.py`; `api.BANDS`, `api.WEIGHTS`, `api.COOLDOWN`)
Decision at each pattern end + recovery. Bands: **near ≤ 4.5 b, mid ≤ 11 b, far > 11 b**; rear = ±60° behind her.

| entry | P1 near / mid / far | P2 near / mid / far | cooldown P1 / P2 (t) |
|---|---|---|---|
| A3 | 50 / 15 (≤ 8 b) / 0 | 35 / 10 (≤ 8 b) / 0 | 120 / 100 |
| A4 (+A5) | 0 / 35 / 40 | 0 / 20 / 20 | 160 / 140 |
| A9 | 40 / 10 (≤ 7 b) / 0 | 20 / 10 (≤ 7 b) / 0 | 160 / 140 |
| A10 | 40 / 25 / 35 | 0 / 15 / 20 | 120 / 100 |
| R1 | — | 0 / 20 / 35 | — / 220 |
| R2 | — | 0 / 15 / 25 | — / 260 |
| R3 | — | 20 / 25 / 0 | — / 200 |
| A1 / A2 | 10 / 0 / 0 each + the counter trigger | counter trigger only | 100 / 85 each |
| A6 | skill trigger only (§4.3) | skill trigger only | 400 / 400 |
- **Counter trigger** (A1 / A2 = the footage's "counter out of a hit reaction", questions.md Q-A2): ≥ 4 player hits on her
  in the last 40 t while she is in recovery or idle → 70 %: the next decision at once is A1 (player beside / behind) or A2
  (in front); she plays `flinch` (6 t) on every 4th hit taken in recovery. Only inside the near band (≤ 4.5 b,
  `api.BANDS[0]`): ranged hits from farther leave the decision to the far rule / the band pick (HR-26). While a floor step
  is reserved neither the counter nor A6 starts (HR-04). A flinch's last tick plays the move clip again (HR-25; the walk /
  glide / strafe, and the far fallback's approach glide).
- **No long waits / gap closing** (README 0-6 10-30; Q-A3): the player > 8 b away for 30 t → P1: A4 60 % / A10 40 %; P2:
  R1 40 % / A4 30 % / R2 30 % (cooldowns respected; fallback: `glide` in + A3). After A6 the next decision (16 t) uses this
  rule. **Rear rule**: the player in her rear zone 20 of 30 t and inside the near band (≤ 4.5 b) → A1 (its
  cooldown ignored once per 200 t); farther, the far rule / band pick (HR-26).
- **No empty band** (HR-13): the weights / cooldowns leave every band a move; a band still empty twice in a row (no pattern
  between) → the 12-t `backstep` clip (she steps straight away from the player at 0.3 b/t while nearer than 5 b, its
  first 10 t, `mv/ok`-checked), then the mid pick of the phase (`ai/backstep`, `ai/bs_pick`).
- No immediate repeat of an entry; weights renormalised over the entries that are off cooldown and allowed by distance.

### 4.8 Difficulty (target: 타키, "a bit stronger than a mid-boss, close to a chapter boss")
| | 타키 (README) | 홍련 (plan) |
|---|---|---|
| registry | hp 250, atk 12 × dmgMul 135, lvAdd 1, tiers 29 / 42 / 56 / 71 % | hp 260, the rest the same but T3 62 (S5) |
| structure | 3 phases, 2 mantles (break or nova), 11 entries | 2 phases + 2 gauntlets, 7 P1 entries + 3 P2 entries, a 200-t down window |
| scripted HP | — | −4.5 % (CS2), −3 % + the kill (CS3); the last ≈ 2 % is never fought |
| invulnerable time | intro 9 s + transitions | intro 32 s (≈ 6 s when skipped at once), CS1 10.7 s, SQ1 3 s, A8 10 s, CS2 5 s, lead-in 4 s, A13 13 s, CS3 5 s ≈ 83 s (≈ 57 s with the skip) |
| measured / target | whole fight 134 %/min (1.23 × the guardian), standing 216 %/min, worst 40-t window 35 %, kill 202-216 s | §4.8 targets below |
S5 fairness probe (`tools/dev/sim/ar/review/bal/knfair5.py` agents and seeds, ported as `HR/review/bal/hrfair.py`; item-less
Lv15 vs her level, 3 seeds × 3600 t). 타키's README figures come from another tool (`S:tk/review/bal/tkfair.py`), so the
same `hrfair.py` agents and seeds first run on 타키 for the baseline and every target is a ratio measured by that one tool:
P1 melee walker 1.0-1.15 × 타키; P2 ≤ 1.25 × 타키; standing ≤ 1.8 × the guardian standing; worst 40-t window ≤ 40 %; all 9
gauntlet cuts on a standing agent ≤ 45 % max HP (so the 60 % fail hit of 50 % leaves ≥ 1 HP by design); four dash agents
at the counting cuts — stand-then-dash, and move-then-dash outward / sideways / inward at 0.22 and 0.28 b/t — each score
with ≥ 90 % of correctly timed dashes (strike − 2 ± 2 t, §5.1) and clear the shield in ≥ 90 % of the gauntlets, a random
dasher (± 8 t) in ≤ 50 %; A6 at most once per 20 s; item-less sword kill 230-270 s incl. the cutscenes
(≈ 150-185 s of fighting). Knobs: tiers ±20 % (the counting cuts have their own TC 37, §4.5), `hp` ±15 %, `DOWN_T`
160-260, `CUT_R` 2.8-3.6, recoveries ±4 t from P1 12-20 / P2 10-16 (F1 moved the base: P1 16-24 → 12-20, P2 12-18 →
10-16). S5 sets the tier numbers; F1 did not change T1-T4.

**S5 (11-06) — the measured pass** (`HR/review/bal`, hrfair 1.2 with the commit's own `lib/hrsim.py`, the `hr` preset =
108 runs: seeds 11 / 22 / 33, 3 600 t per phase run, item-less Lv15 vs L16; T9 also Lv5 vs L6 and Lv10 vs L11 (HR-40);
타키 = `base_tachy.json`, the Guardian standing 164.0). On F-I's 3741fc4: T1 0.81 × (FAIL), T9 Lv5 229.6 s (FAIL), the rest
in band. The levers in the lead's order (HR-13 / 14 / 18 point 5), each measured on the P1 walker (3 seeds; a what-if tree
= the commit regenerated with one api patch): A9 / A10 P1 near weights 25 / 20 → 35 / 35 and A10's cooldown 180 → 140:
0.93 ×; → 40 / 40 and 120 / 100: 0.97 ×; + the recovery knob P1 12-20 → **8-16**: 1.00 ×; A1 / A2 near 15 (0.96 ×) and
A9 / A10 near 50 (0.98 ×): no gain, not kept; `TAIL_MOVE` not moved (F-I checked the pose hand-over at 4 t); **tracking**
(re-aim ≤ 30°/t up to each 7-t lock): 0.86 ×, rejected — the walker reads every locked body-centred sector 12 t early and
steps round it whatever her turn rate, only the player-centred discs (A9, A10) land; then the tier knob **T3 56 → 62**
(+10.7 %, `mboss/hurt`'s raw 9 → 10 = 23 → 25 HP; A4's dive, A9, A10, R1's third / R3's second cut): 1.05 ×; and the `hp`
knob **250 → 260** (+4 %) for T9's margin at the low levels (Lv5 235.4 → 240.7 s; Lv2 259.4 s, the lowest reachable rift
level, stays under 270). P2 keeps P1 × 0.85 (T2 1.11 ×: no exception). Result (the final measurement on the S5 head wip/hr 005f00a, `HR/review/bal/hr_s5_summary.log`; ed2e175's `hr_s5b`
gave the same numbers; README 「홍련」 난이도 · 균형):

| target | 3741fc4 (F-I) | S5 | band | |
|---|---|---|---|---|
| T1 P1 melee walker %max/min ÷ 타키 whole 124.0 | 99.9 = 0.81 × | 130.6 = **1.05 ×** (seeds 134.1 / 136.8 / 120.8; 0.95 × 타키 P1) | 1.00-1.10 (not the top) | PASS |
| T2 P2 melee walker | 131.1 = 1.06 × | 138.0 = **1.11 ×** | ≤ 1.25 | PASS |
| T3 standing max(P1, P2) ÷ the Guardian | 236.4 = 1.44 × | 244.0 = **1.49 ×** (P1 234.6) | ≤ 1.8 | PASS |
| T4 worst 40-t window, melee walker | 19.8 % | **20.5 %** | ≤ 40 % | PASS |
| T5 / T5b the 9 cuts on a standing agent | 40.3 / 40.3 % | **40.3 / 40.3 %** (A8's fail hit then 50.0 %, A13 discs 16.8 %) | ≤ 45 % | PASS |
| T6 the six dash agents: pips per timed dash / clears | 100 % / 100 % | **100 % / 100 %** (216 / 216, 24 / 24 each) | ≥ 90 % | PASS |
| T7 random dasher (± 8 t) clears | 29 % | **29 %** (7 / 24) | ≤ 50 % | PASS |
| T8 A6 starts in any 400 t (skill hits every 150 t; P2 also every 60 t) | 1 | **1** (shortest gaps 457 / 582 / 458 t) | ≤ 1 | PASS |
| T9 item-less kill incl. the cutscenes, Lv5 / Lv10 / Lv15 | 229.6 / 234.9 / 240.8 s | **240.7 / 242.8 / 245.4 s** (fighting 157 / 160 / 162 s) | 230-270 s | PASS |
Also: the ranged walker's whole fight now completes (HR-37: 92.6 %max/min), the perfect dasher P1 / P2 / whole 0.0 / 14.7 /
6.3; her collision does not push the player's avatar in the default F5 view (the avatar carries the camera seat, a
vehicle is never pushed), so the walker keeps its overlap (S5 report).

---------------------------------------------------------------------------------------------------------------------

## 5. The shield, the pips and the instant death (S3 `shield.py`; the gauntlet scripts call it)

### 5.1 Mapping "perfect parry × 5" onto this pack (question 6)
The original: the 5-segment shield is full at the gauntlet's start, each perfect parry removes about one segment, an empty
shield turns the final strike into Eve's counter; otherwise the instant death (w1 §3; patterns.md §10.5). The pack has no
parry or guard (framework.md §4.3); its timing skill is the dash: 6 t of i-frames (`F:player/dash_go:4`, `dashInvT 6`,
counted down by `F:player/tick:59`), 3 b in 3 t along the movement input, or the look direction when standing
(`F:player/dash_dir:14-27`). The framework's perfect-dodge flag `#mbDodgeOk` (`F:mboss/hurt_dodge:4`) is set only when the
i-frames eat a hazard that finds the player's feet inside it; a player who moves and then dashes on along that movement
ends outside the cut and gets no event, so a pip rule on `#mbDodgeOk` would reward only standing still. The pip is
therefore independent of the hazard geometry (`api.PIP_RULE = 'timed_dash'`): `shield/cut {s}` stores the cut's lock
point on its `rlk_hr_cut` marker, and **at the strike tick s a pip is removed when the player's dash i-frames are on
(`dashInvT` 1..6; at s + 1, for the tick order, `dashInvT` 1..5 = a dash started by s) and the player's feet are within
`CUT_R` + 3.0 = 6.2 b of the lock point** — one pip per cut at most, whatever the dash direction. Counting cuts: the nine
ghost cuts of each gauntlet (A8 cuts 1-9; A13 U1-U6, U8-U10). Not counting: the A7 discs (yellow = dodge-only in the
original), A8.9 (the judge), R1 / R3 (no shield there). Five of nine are needed (four spare). Dash economy (2 charges,
20 t each, 5-t self-cooldown): the tightest stretch (cuts 1-3, 13 / 15 t apart) needs two charges and one regenerated —
feasible, and only five timed dashes are needed.

### 5.2 The display (questions.md Q-B12)
The boss-bar under bar (`#buSub` / `#buSubMax` / `#buSubCol` from the module's `bars` hook; framework.md §4.7):
`#buSubMax 5`, `#buSubCol 1` (electro), `#buSub` = pips left — shown from SQ1 tick 0 (full, as the footage's HUD returns
with a full shield) and from the lead-in's refill beat (0 → 5 in one step, critic C44) to the judge; during the down window
the under bar is the down timer (gold, max 200); otherwise none. A pip removed: the bar drops one segment and kit
`pip_break` (lilac shards at the player) + `block.amethyst_cluster.break` 0.8 pitch 1.4 + `entity.player.attack.crit` 0.5
pitch 1.6. No other text (rule 10-21) except §5.5's banner at 5 %.

### 5.3 Building a counting cut (`api.cut(made, lock, strike)`: a D0 call builder that emits `function rlk:boss/scarlet/g/cut/…` lines; S4 owns `g/cut/**`)
At its `made` tick: `hz_opts(quiet=1, el=3, kb=0, act=2)` + `mboss/hz/disc {r:32,tell:<strike − made>,dmg:37}` (tier TC, `api.DMG['TC']`) positioned
at the player's feet, tagged `rlk_hr_cut`, stored with its strike tick; every tick until `lock` (= strike − 7) the pattern
re-aims it onto the player (`mboss/hz/aim` as the marker, positioned at the player; `mboss_lib.hz_aim()`); from the lock it
stays, and `shield/cut {s}` stores the lock point (§5.1). The damage radius **3.2** (`api.CUT_R`, wider than the visible
ring of ≈ 2.2): a player still inside it at the strike without i-frames takes TC damage and no pip; a dash in [strike − 5,
strike] is never hit (its i-frames cover the strike) and scores the pip in any direction; walking out or dashing out early
→ no damage, no pip.

### 5.4 The judge (A8 T + 194, A13 T + 258)
`shield/judge`: `#pips hr 0` → **deflect**: no hazard; she halts 1 b above the player; kit `clash_gold` (the gold starburst
= the player-side success feedback, §1.3) + `light_column` at the player (F2: the gold starburst at the avatar's chest, in
first person 1.8 b out on the view ray; the `light_column` upright, pitch 0, at the avatar, in first person 1.8 b ahead); `block.anvil.land` 0.6 pitch 1.4 +
`entity.player.attack.crit` 0.8; darkness lifts; `g_deflect` (12) → CS2 / CS3 (§3.4). The pattern always runs to the dive
(questions.md Q-A7: in both videos the shield is empty after the 5th cut but the counter comes after the dive).

### 5.5 The fail branches
- **60 % (default non-lethal, `ULT60_LETHAL false`)**: pips > 0 at T + 194 → the dive lands: kit `dive_impact {r:30}` +
  `light_column`; the player takes `mboss/pl_dot` **500 ‰** of max HP (`#mbDotLethal 0`: it cannot kill), applied
  directly (no dodge, no position check: the failed check itself is the hit) and, in the same tick, a push ring at the
  impact point (`mboss_lib.push_ring(2.5, 3)`: `pl_dot` carries no knockback, `F:mboss/pl_dot:1-12`);
  `entity.generic.explode` 0.5 pitch 1.4 + `block.amethyst_block.break` 0.8. Darkness lifts; she lands 2 b from the
  player, `g_reform` (10) → P2 at T + 214 with her HP unchanged (no counter, no down window). With `ULT60_LETHAL true`
  the 60 % fail is the instant death below (+ the banner).
- **5 % (default lethal, `ULT5_LETHAL true`)**: pips > 0 at T + 258 → **the instant death** (w1: "시스템 제약을 무시하는
  절명기"), staged as her burst 홍련일섬 (w2: the screen blacks out before the slash sound):
  | T+ | what |
  |---|---|
  | 252 | she reappears high in her normal colours (as the success branch) |
  | 255-258 | **ovl `black`** in 0 hold 3 out 0 |
  | 258 | **ovl `pinkwhite`** in 0 hold 3 out 8; kit `scarlet_line {len:600,roll:<rising 13° toward the player's right>}` through the player's chest point (as CS1 C8; in first person at the eye + 1.2 b); the line, the petal burst and that tick's bolts are kept cards (`fx/keep_on` .. `keep_off`, tag `rlk_hr_fx_keep`: `death_start` / pause `fx/clear` and the ager's dead / revive clears leave them to finish their life, alive ≥ 12 t after the kill, the line 30 t; F2, HR-17); `petal_burst {r:20}`; `item.trident.thunder` 0.7 pitch 1.2 + `entity.player.attack.sweep` 1.0 pitch 0.5 + `block.glass.break` 0.6 pitch 0.5; **`ult/fatal`** on the player |
  `ult/fatal` (S3, as `F:boss/raiden/hazard/fatal`): skipped if the player is already reviving (`rnDie ≥ 1`); else
  `player/hurt_do` with all current HP, `curHealth 0`, `player/die` — it bypasses `mboss/hurt`, so dash i-frames and every
  shield are ignored; **Ronova's one revive still applies**. Dead → the normal run failure (a test → `test/defeat`). Revived →
  the fight pauses while the player revives (framework); on resume the darkness is lifted, she stands 8 b away in her stance,
  and 60 t later `lead_stand {g:a13}` → A13 again with the shield at 5/5 and the banner. No line.
- **The warning** (allowed only for instant-death moves, README 0-6 10-21; question 6): bossbar `rlk:hr_warn` (kit
  `fx/hud/warn {on}`; its own line under the framework's bars as 아를레키노's `rlk:kn_banner`) from the darkness onset (T0 − 17)
  to the judge, only in a gauntlet whose fail is lethal (A13 with `ULT5_LETHAL`, A8 with `ULT60_LETHAL`; SQ1, the lead-ins
  and every `lead_stand {g}` restart check the same switch), white text with 「즉사」 in crimson `#FF3A55`; default wording
  `api.WARN_TEXT` = 「대시로 베기를 아슬아슬하게 피해 실드를 모두 깎으세요 — 실드가 남으면 즉사합니다」. Not shown at 60 %
  (non-lethal there: no how-to text for non-lethal moves); the shield's meaning at 60 % is learnt from the under bar and
  the fail hit.

### 5.6 Edge cases
Pause during a gauntlet (the player dead / reviving / in a menu): the gauntlet is cancelled (cut hazards, discs, ghost,
banner off, darkness lifted); on resume `lead_stand {g:a8|a13}` and that gauntlet restarts from T0 with 5/5 (the banner
only where §5.5 allows it) — unless its outcome is already decided: the judged deflect → CS2 / CS3, the judged A8 fail
(non-lethal) → P2 at once, the judged lethal fail → the revive stance, and a lethal gauntlet past its last counting cut's
pip window (strike + 1) with pips left → the instant death as soon as the player is back and alive (then the revive path).
A `/reload` while the pause lasts keeps that decision (F1, HR-01 / HR-07). The player dies from cut damage in A8 → the normal death path (Ronova applies; after a revive
A8 restarts the same way). The player leaves the walk disc → the framework's out-of-bounds return; cut hazards keep
following until their lock. `/reload` → as pause. Cleanup → `rlk_hr_cut` markers, discs, the banner and every under-bar
value removed (idempotent); every fake player of objective hr but the event scores (save → reset * hr → restore), storage
`core.*` and `seq.*` (F3, HR-05).

---------------------------------------------------------------------------------------------------------------------

## 6. Arena `hr_field` 「달빛 억새밭」 (owner: **S1K**, `tools/mboss_arena_hr_field.py`; registry entry by D0)

### 6.1 Registry entry (`arenas{}`, frozen at D0 as `api.ARENA_SPEC`; D0 adds it — until S1K's theme module exists the
arena generator writes stub functions for it, `T:build_mboss_arena.py:35`)
```json
"hr_field": {"n": 5, "theme": "hr_field", "ver": 1, "cx": 880, "cy": 201, "cz": 8, "r": 28, "walk": 25, "safe": 23,
  "start": {"x": 880.5, "y": 201.0, "z": 31.5, "yaw": 180.0, "pitch": 0.0},
  "box": {"x0": 832, "y0": 190, "z0": -40, "x1": 928, "y1": 250, "z1": 56}, "looks": ["moon", "crimson", "dark"],
  "oob": {"y0": 198, "y1": 236}}
```
Chunks x 52-58 × z −3..3 = 49 (≤ 256), clear of every fixed forceload and of `fl_ruins` (chunks 44-50) (framework.md §5).
The core adds `#mbAr 5` with its radii to `fight_vars`. C = the axis (880.0, 201, 8.0); floor blocks at y 200; "north" =
−z = bearing 0°, the moon side (the moon at bearing 12°, §6.2); the player arrives at the south rim facing north.

### 6.2 Layout — an original composition in the footage's mood (arena.md §1, §7; the moon gate is not reproduced, §1.5)
The footage's mood, sizes and light (a moonlit silver-grass field, the moon low over the far end, lanterns, bamboo,
blossom), in an asymmetric composition of our own: nothing on the moon's axis, no stair, no pair of tall masses framing
the moon (the gate / "lit tower" of arena.md §2), no glyphs.
- **Field** (walk disc r 25, footage field ≈ 35-50 m): flat full blocks at y 200, a silver-grass meadow; no obstacle, no
  slab, nothing overhead below y 226 except the light layer (y 206). A barrier ring at r 26-27 (y 201-215).
- **North** (bearings ≈ 300°-60°, irregular): a wide **lotus pond** r 27-36 (water 1 deep, rim of `packed_mud` /
  `mud_bricks`, `big_dripleaf` for lotus leaves, `lily_pad`; the flowers are 8 kit props `lotus`); its far shore a low
  natural bank of mossy tuff boulders and dry grass (r 36-41, 1-3 b; no wall, no stair); **one old crooked pine** (노송)
  rooted on a boulder at bearing 322°, r 38, 14 b tall, its trunk (`spruce_log`, leaning in steps) reaching out over the
  water toward the moon and its flat cloud-layer crowns (persistent `spruce_leaves` / `dark_oak_leaves`, 9 b wide) ending
  at ≈ bearing 355°; the **Korean lotus stone lantern** (연화 석등, 6 b) on a flat rock islet at bearing 28°, r 31: an
  octagonal base ringed with downward lotus petals (`stone_brick_stairs` upside down), a slim post (`andesite_wall`), an
  upturned lotus-cup capital, a firebox with four windows (`ochre_froglight` behind `iron_bars`), a curved roof
  (`deepslate_tile_stairs` / slabs) and a bud finial; bamboo behind the bank.
- **The moon**: a block disc r 5 on the north dome wall at bearing 12°, elevation 22° from C (centre ≈ (889, 218, −34), a
  vertical disc facing south), in open sky to the right of the pine crown, seen whole from C and from `start` (CS0's
  opening composition, CS4's moon gaze; CS0 E0 and CS4 S10-C1 turn her to face it, yaw toward `api.MOON_POS`). A kit
  `moon_halo` card in front of it.
- **Sides** (60°-150°, 210°-300°): low dry-stone walls at r 27-28 (1-2 b, moss carpet on top) with small stone lanterns
  every 30° (2.5 b, warm `ochre_froglight` fireboxes); bamboo groves (r 30-38, `bamboo`), six cherry trees (`cherry_log` +
  persistent `cherry_leaves`, their falling-petal particles come free) at bearings 70°, 110°, 140°, 220°, 250°, 290°, r 32-36.
- **South** (150°-210°): the low wall continues, with a 3-b gap at the arrival (the player arrives by the rift, §6.7; no
  entrance stair).
- **Beyond** (r 38-44): tuff / deepslate outcrops and dark tree masses; a painted band of mountain ridges and mist on the
  dome base (`gray_terracotta`, `black_terracotta`, `light_blue_terracotta`); no buildings, no glyphs, no monoliths.
- **Sky**: a block dome r 46 lit from inside (fl_ruins technique; no world-time dependence).
- **Light**: a grid of `light[level=15]` at y 206 over the walk disc (floor ≥ 12, no spawns); lanterns warm.

### 6.3 Look `moon` (P1, default; arena.md §4 P1 palette, `arena_palette_p1.jpg`)
| element | blocks | target colour |
|---|---|---|
| walk floor | `mycelium` 70 %, `pale_moss_block` 12 %, `coarse_dirt` 10 %, `tuff` 8 % (flush stones) | field #625A61, shadows #453D3C |
| grass (no collision, `#rlk:dash_pass`) | `short_dry_grass` on 25 % and `tall_dry_grass` on 12 % of the **mycelium** cells only | plume tips #998F9D |
| dome | horizon 0-6° `light_blue_terracotta`; 6-60° `blue_terracotta`; zenith 60-90° `blue_terracotta` with `black_terracotta` noise | #6B74AF / #3A3752 |
| moon disc | `white_concrete` face, `light_gray_concrete` maria, `snow_block` highlights, a rim of `pearlescent_froglight` | #CEE1FD, core #DEF9FE |
| cherry crowns | `cherry_leaves` | #6F6079 lit |
| kit props | `moon_halo` look `p1` (white-blue), `lotus` look `bud` (closed, pale pink) | — |
| ambient (module, every 10 t near the player) | `cherry_leaves` (free from the trees), 1 `ash` speck at 8-14 b | sparse (arena.md §5) |

### 6.4 Look `crimson` (P2; CS1 173-176; arena.md §4 P2 palette, §6 the recolour)
| element | blocks (swap order: plants first, then the floor, so every plant always stands on a valid support) | target |
|---|---|---|
| grass | `short_dry_grass` / `tall_dry_grass` → `crimson_roots` (on mycelium = `#dirt`, valid) | tips #CA5438-#DE5C2D |
| walk floor | `mycelium` → `crimson_nylium`, `pale_moss_block` → `nether_wart_block` (no plants on those cells), `coarse_dirt` / `tuff` kept | grass body #802B2B |
| dome | horizon → `crimson_planks`, body → `purple_terracotta`, zenith → `blue_terracotta` (kept) with `black_terracotta` | fog #573137, sky #64405C / #4E3B57 |
| moon disc | face → `pink_concrete`, maria → `red_terracotta` (rim kept) | #F9868B, maria #B23B4B |
| cherry crowns | `cherry_leaves` → `nether_wart_block` | #691C3C-#922B3D |
| kit props | `moon_halo` → `p2` (red), `lotus` → `bloom` (open crimson) | — |
| ambient | every 6 t near the player: `crimson_spore` ×2, `dust` {#D55D87, 1.2} ×1; `firefly` ×1 per 20 t low over the grass (id checked in 26.3) | arena.md §5 |

### 6.5 Look `dark` (the gauntlets, from `crimson`; T0 − 17 → the judge; arena.md §4 "ultimate darkness", patterns.md §0.1)
The footage: the sky and far field sink to near-black over ≈ 9 t, only the grass around Eve stays lit, and the dark lifts
with the final dive's flash. Never `blindness` (it hides the far ghost, questions.md Q-B6).
| element | blocks |
|---|---|
| dome (all bands) | → `black_concrete` / `black_terracotta` |
| moon disc | → `black_concrete` (face, maria and rim); `moon_halo` → `off` |
| lantern fireboxes | `ochre_froglight` → `black_concrete` |
| walk light layer | `light[level=15]` → `light[level=6]` (the field dims; the lilac ghost is brightness 15 and stays readable) |
| decor light blocks outside the walk | → `light[level=0]` |
Every transition (moon ↔ crimson ↔ dark) is one job of absolute spans and block-exact (§6.6). Risk: the light-level swap
makes the light engine re-light ≈ 49 chunks in one tick; S1K measures the hitch in game; fallback B (`api.DARK_LIGHT
false`): the dome / moon / lanterns only.

### 6.6 Look jobs and limits
A look job is keyed only by its target look, and without the theme's `look_lines` a non-default look writes only the cells
that differ from `looks[0]` (`T:build_mboss_arena.py:371-389`): a `crimson` job would never undo what only `dark` changed
(fireboxes, the light layer, the moon rim). So S1K's theme implements `look_lines(look)` = absolute spans, for every cell
any look changes (the union, ≈ 16 k cells: grass ≈ 730, floor ≈ 1.6 k, outer field ≈ 330, dome ≈ 11 k, moon ≈ 80, crowns
≈ 600, fireboxes, the walk light layer ≈ 1.9 k, decor lights), of that cell's state in `look`: one job, block-exact from any
source look. Each job has 4 real slices (`fill … strict` row spans, ≤ 32 768 cells per fill, ≤ 8 000 commands per slice,
≤ 40 slices; one slice per tick, `T:build_mboss_arena.py:307`): `moon` and `crimson` on consecutive ticks (≈ 3.5-5 k
commands each; fl_ruins' crimson ≈ 4.9 k); `dark` with two empty padding slices after each real one, so its slices land
3 t apart (far dome and moon first, the walk light last) and the field dims over ≈ 9 t as in the footage (patterns.md §0
item 1) — the job is called at T0 − 18 and its real slices land at T0 − 17 / − 14 / − 11 / − 8. A look call is refused
while any arena job runs (`F:mboss/arena/fl_ruins/look/crimson:3`), so `api.arena_look()` is a request: the core keeps the
wanted look in `#hrLook hr` and starts the job at the first tick with `#mbArBuild 0` (a pause or a reload inside a running
job can no longer leave the arena dark). The framework's `ensure` restores `moon` at the next fight.
A floor cell under an opaque cover or full / waterlogged water (any look) is `coarse_dirt` in every look: mycelium / crimson
nylium would turn to dirt / netherrack there by random ticks and the looks would drift (F2, HR-43). The look jobs change
23 280 cells (was 23 378); commands per look: moon 7 052, crimson 7 221, dark 6 650 (slices ≤ 2 518); build slices ≤ 4 962.

### 6.7 Entry, exit, decor props
- Arrival at `start` (south rim, 23.5 b from C, facing north) out of a closing rift tear 1.5 b behind (kit `arrive_rift`,
  30 t, using the shared `rlk:rift/*` models of `build_rift.py`). No dungeon entrance build (a special boss has none).
- Exit and reward: the framework's `sp/won` returns the player to the rift spot; §7.
- Kit decor props spawned by the module at `spawn` (S1K `fx/prop/*`, removed by cleanup): `moon_halo` (12-b card in front
  of the moon), 8 × `lotus` on the pond, `seat_rock` (intro only, at the seat (884.0, 201, 5.0) on the `start` → moon line, §3.1).

### 6.8 Renders (S1K)
`HR/renders/s1k_arena_moon.jpg`, `s1k_arena_crimson.jpg`, `s1k_arena_dark.jpg`: top-down + a perspective from `start`
and one from C looking at the moon (in open sky beside the pine; no gate framing), next to `HR/ref/arena_keyframes.jpg`
and `arena_palette_p1/p2.jpg`.

---------------------------------------------------------------------------------------------------------------------

## 7. Ending → reward → random event → item → buff

Merged from `HR/plan/reward.md` (the reward planner's section; that file stays the original text). What the two critiques
changed here is listed in §11. This section starts at CS4's hand-off **H** = `ending` tick 1042 (7.1.2). Notation as the
header and `framework.md`: `F:` / `T:` with `:<line>`, `README:<n>` = a line of `R:README.md`, `items.md:<n>` =
`R:items.md`; 20 t = 1 s; `E<n>` = event tick n after H. Module id `scarlet` (§0). Stages as §9.1 (S1 framework, S1K kit
+ arena, S2a rig / S2b sequences, S3 core, SR the item and buff hand files, S5 balance).

User defaults this section builds on (= the questions already sent, §0.1 1-4; all switchable, one knob each):

| Q | default | knob |
|---|---|---|
| 1 "영구적인 버프" scope | rest of the run | `api.EVENT['buff_scope']` `'run'` / `'forever'` + one line in `F:player/reset_one` (7.5.3) |
| 2 reward | level up 1 + 1 item pick + the random event | registry `lvup 1`, `picks 1` (3 = the special default) |
| 3 event odds | 50 % item / 50 % buff | `api.EVENT['item_pm']` = 500 (‰ for the item branch) |
| 4 rift share with 타키 | equal weight | registry `w` (§8) |

### 7.0 Decisions at a glance

| item | decision |
|---|---|
| how it ends | she never dies: the module ends the fight with the scripted lethal true hit `mboss/true_pct {pct:100}` at the A13 counter's kick (CS3), so the kill-only reward path pays; the death state (`#mbSt 2`) plays CS4 + the event coda instead of a collapse; no poof (FN-c) |
| reward | gold × `goldMul` + 1 sapphire + 5 % heal-orb roll at the lethal hit (framework); **event coda in her field** (6 s); return; title `홍련 도전 성공` (FN-a) / `레벨 업 · 아이템 상자 1개`; one level (its usual pick); the reward hook (FN-b: record, pending drop, reload safety); rift collapse → **1 item box** |
| event | rolled at `death_start`; item 500 ‰ / buff 500 ‰; never a duplicate (holding the sword → buff, buff on → item); granted once at E56 of the coda (or by the hook if the coda was cut) |
| item | `[ MYTHIC ] 화무십일홍` (`sword_hwamu`): 공격력 +25 %; 「육참골단」 4 basic hits → ATK +6 % ×5 stacks (6 s), −4 % current HP above 50 %; 「검신합일」 on a hit taken or dodged → 138 % ATK electro counter (4 s cd; S5, was 2 s), crit dmg +30 % at HP ≤ 60 %; 「홍련일섬」 on burst → 500 % ATK electro to every enemy ≤ 20 b (40 s cd; S5, was 849 %), crit rate +20 % for 10 s if HP ≤ 50 %. Granted at ★☆☆. `box_exclude`; user-requested exception to the mythic rule |
| buff | 「월하대작」 for the rest of the run (load's 조절 지점 `#hrMoonRun 1`): **최종 공격력 +27 %** (`ampAtk`; S5, was 20 %), 치명타 확률 +10 %, 이동 속도 +10 % |
| framework | FN-a `winWord` (record field) · FN-b `rwHook` → `<fn root>/reward` (literal line in `sp/reward`) · FN-c `poof:false` — all in `T:build_mboss_core.py` + `mboss_lib.py` + `check_mboss_pack.py` (S1); 타키 / spproto module outputs and records byte-identical |
| budget | 0 new atlas px (the rig's sword texture is reused by the thrown prop / item icon model `rlk:mboss/scarlet/item_sword`; everything else is particles, the fight's `black` overlay and one new font glyph `vig`, not in the items atlas); ≈ 70 new functions + ≈ 100 rig key files for 3 short clips |

### 7.1 The end without a death, the reward path, framework changes FN-a / FN-b / FN-c

#### 7.1.1 The chain (framework facts: framework.md §1.5, §1.10, §1.11)

The reward exists only after a kill: `#mbKilled 1` is set only in `F:mboss/death_start:7`, gold / sapphire / orb come
only with the lethal hit (`F:combat/apply:83-85`), `F:mboss/sp/won:10` pays only when killed. So:

| # | when | function (owner) | what happens |
|---|---|---|---|
| 1 | CS3 (A13 counter, `#mbSt 1`, HUD on, she is `rlk_mb_inv` + `#mbCine 1`) ends on the kick impact | module (S3, §3.4) → `mboss/true_pct {pct:100}` (`F:mboss/true_pct:1-7` → `true_hit`) | true damage passes the invulnerability and the 5 % floor (`F:combat/apply:23`, `F:mboss/floor`); the module stops its tick once `#mbSt` became 2 |
| 2 | same tick | `F:combat/apply:83-85,91` | heal-orb roll 5 % (an orb at her feet, collectable during the ending), kill XP 0 (`xp 0`, required by `lvup 1`, `T:mboss_lib.py:136-137`), gold random(2..4) × chapter × `goldMul` + `sap` 1 sapphire shard (the body's `miniboss` tag), then `mboss/death_start` |
| 3 | same tick | `F:mboss/death_start:3-17` | `rlk_mb_dying`, `#mbKilled 1`, `#mbSt 2` (nothing can hurt the player: `F:mboss/hurt:20`), `lib_clear`, bars hidden, no wither roar (`deathSnd:false`), music stop, then the module's `death_start` hook: **`boss/scarlet/ev/roll` (7.3.1)**, the ending music, `seq/ending` (CS4) |
| 4 | death ticks | `F:mboss/death_shell:1-2` → module `death_tick` | CS4 (§3.7) until H = 1042, then **`seq/event`** (7.3.2) H … H + 120 |
| 5 | `#mbT` = `cur.death` (= H + 122 = 1164) | `F:mboss/death_finish` (FN-c) | no puff for her (she already left in petals at E40), `kill` the invisible body → the zone clears (`room/combat_tick`) |
| 6 | next tick | `room/combat_clear` → `F:mboss/sp/clear:3-4` → `F:mboss/sp/won:3-12` | leftover arena gold absorbed (`ar/<aid>/box_absorb`), `cleanup_fight` (module `cleanup`: rig, kit, lines, event entities, every fake player of objective `hr` and storage `core.*` / `seq.*` — **not** the `#hrEv*` scores, saved around `scoreboard players reset * hr`; F3, HR-05), `tp_out` to the rift under the coda's black, arena sweep / `fl_off` |
| 7 | same tick | `F:mboss/sp/won_kill:3-8` → `F:mboss/sp/reward` (FN-a, FN-b) | title `홍련 도전 성공` / `레벨 업 · 아이템 상자 1개` (72 t), `sp/lvup` (one level, chat, `pkPending +1`), **`boss/scarlet/reward`** (7.3.4), rift collapse 30 t → `close_end` → 1 box (`mboss/box/drop_all`, row of 1); then test replay links, `forget` |

`/reload` while dying finishes the death at once (`F:mboss/reload:3`): the reward is still paid and the reward hook
applies an event the coda did not reach (7.3.4). `boss/test/kill` (`F:mboss/test/kill:1-4`) jumps straight to step 2,
so the ending + event can be tested without the fight.

#### 7.1.2 Hand-off contract with CS4 (§3.7)

- **H** = CS4's last tick (`ending` 1042): line 7 「당신의 기억이 이어지기를.」 is finished and its kit line cleared, the hat-tip
  resolved (the original's "eyes back", `HR/understand/cutscenes.md` §8 S3 ≈ v5 f1186), she stands ≈ 4.5 b from the
  player (§3.7 S5) with the hat on, her left hand still at the brim and the sheathed sword in her right hand (carried by
  the throat, model.md §3 — as the footage keeps it to the end), the ending track still playing. **CS4 does not play the
  original's final fade** (≈ v5 f1220-f1300): that beat moves to E110–E120 here, so the black falls after the event,
  right before the return (the original's order ending → black → result).
- `seq/ending` sets `#sqdone`; the core then starts `seq/event` (both run in `death_tick`; S2b writes both services).
- Registry `"death": H + 122 = 1164` (2 t margin after the coda's black), `"deathSnd": false`, plus this section's fields
  (7.1.3–7.1.5, 7.2): `"lvup": 1, "picks": 1, "xp": 0, "winWord": "도전 성공", "rwHook": true, "poof": false`.
- Module test ids 90–92 reserved for the event (7.3.1); kit line ids 24-25 (§3.0) and the new glyph `vig` (U+EC16; the
  black is the fight's `black` overlay, 7.3.2) in the D0 kit contract; clips `ev_give`, `ev_toast`, `ev_leave` and the
  look `scabbard gone` in the D0 rig contract (§2.4-§2.5).

#### 7.1.3 FN-a — the word: 「도전 성공」 instead of 「처치」 (S1)

Why: she is not killed; 「도전 성공」 is the original's own result-screen word (cutscenes.md §9 R3, Q-A19), so it may be shown
verbatim (rule 10-21). Today the word is a literal in `F:mboss/sp/reward:8` and `F:mboss/test/swon_msg:1`.

| file | change |
|---|---|
| `T:mboss_registry.json` | 홍련 entry: `"winWord": "도전 성공"` |
| `T:mboss_lib.py` `load_registry` (special branch `:131-141`) | `winWord` optional, special entries only, non-empty string ≤ 12 chars |
| `T:build_mboss_core.py:143-145` `snbt_entry` | after the special `lvup` append: `if 'winWord' in b: parts.append(f'winWord:{s(b["winWord"])}')` → only her record gets the field; 타키 / spproto record text unchanged |
| `T:build_mboss_core.py:4478-4499` `w('sp/reward')` | line 8 becomes two lines (the first is today's line, only guarded): `execute unless data storage rlk:mboss cur.winWord run title @a[tag=player] title [{nbt:"cur.title",storage:"rlk:mboss",interpret:true},{text:" 처치",color:"#FFE08A",bold:true}]` and `execute if data storage rlk:mboss cur.winWord run title @a[tag=player] title [{nbt:"cur.title",storage:"rlk:mboss",interpret:true},{text:" "},{nbt:"cur.winWord",storage:"rlk:mboss",color:"#FFE08A",bold:true}]` (a non-interpreted `nbt` string component is already used in game: `F:mboss/gate:13` `cur.sub`); header comment updated |
| `T:build_mboss_core.py:4643-4649` `w('test/swon')` + new `w('test/swon_msg_w')` | `test/swon` gets a first line `execute if score #mbKilled mb matches 1 if data storage rlk:mboss cur.winWord run return run function rlk:mboss/test/swon_msg_w with storage rlk:mboss tlast`; `swon_msg_w` = `swon_msg` with `{nbt:"cur.winWord",storage:"rlk:mboss",color:"gray",bold:false}` + `"! 균열 자리에 아이템 상자가 떨어졌습니다(누르면 아이템 선택). "` in place of `"처치! …"` (`cur` still exists there: `test/won` runs before `forget`) |

Result: `홍련 도전 성공` / `레벨 업 · 아이템 상자 1개`; `[특수 보스 테스트] 도전 성공! 균열 자리에 …`. 타키 still reads `타키 처치`.

#### 7.1.4 FN-b — a per-special reward hook (S1)

Why: the event needs code at the rift after the return (pending drop when the inventory was full, the outcome if the
coda was cut, a chat record). Adding `reward` to `SPECIAL_HOOKS` (`T:mboss_lib.py:35`) would force it on 타키 / spproto
(new files, changed outputs); an opt-in flag with a literal line keeps them byte-identical (framework.md §1.10 B2).

| file | change |
|---|---|
| `T:mboss_registry.json` | 홍련 entry: `"rwHook": true` (no record field: the line is literal) |
| `T:mboss_lib.py` | `SPECIAL_OPT_HOOKS = {'rwHook': 'reward'}` beside `SPECIAL_HOOKS` (`:31-35`, comment: optional special hooks, required only when the entry sets the flag; no macro); validation: `rwHook` bool, special entries only |
| `T:build_mboss_core.py` `w('sp/reward')` | after the `sp/lvup` line, one literal line per entry with the flag (the `sp/gate` / `sp/prep` technique, `:4324-4354`): `execute if data storage rlk:mboss cur{id:"scarlet"} as @a[tag=player,limit=1] run function rlk:boss/scarlet/reward` (+ a comment line `# hr FN-b: per-special reward hooks (registry rwHook)`) |
| `T:check_mboss_pack.py` hook loop `:49-58` + specials `:142-170` | hooks += `[h for f, h in L.SPECIAL_OPT_HOOKS.items() if b.get(f)]`; for each such entry the exact literal line must be in `mboss/sp/reward`; `mboss/test/swon_msg_w` joins the frozen runtime names |

Hook contract (written by the module generator, S3): `boss/scarlet/reward`, not a macro, @s = the player (not
positioned: the hook positions itself `at @e[tag=rlk_body,limit=1]`, README:1986), called once per kill after the reward
title and the level-up and before the rift collapse; `cur` and `#mbId` still set, `#mbOn 0` (no fight tick: anything
later must be schedule-driven); must not use the title slot (the reward title holds `vBig` / `ttlT` 72).

#### 7.1.5 FN-c — no poof (S1)

| file | change |
|---|---|
| `T:mboss_registry.json` | 홍련 entry: `"poof": false` |
| `T:build_mboss_core.py:143-145` | `if b.get('poof') is False: parts.append('poof:0b')` (any kind; only entries that set it) |
| `T:build_mboss_core.py:1181-1184` `w('death_finish')` | `execute unless data storage rlk:mboss cur{poof:0b} at @s run particle minecraft:poof ~ ~1 ~ 0.6 1 0.6 0.02 30 force @a[tag=player]` (+ comment); `kill @s` unchanged |

#### 7.1.6 Identity and checks
Shared outputs that change (listed in I1's `ident.py` allow-list, §9.5): `mboss/sp/reward`, `mboss/test/swon`,
`mboss/test/swon_msg_w` (new), `mboss/death_finish`, `mboss/register` (her record). Behaviour for every other boss is
unchanged (their records have no `winWord` / `poof`, no hook line); `boss/tachy/**`, `mboss/spproto/**` and their record
text stay byte-identical. Cost: +1 `data` check in `death_finish` and in `sp/reward` per kill.

### 7.2 Reward composition and delivery order

| piece | source | when / where | how the player sees it |
|---|---|---|---|
| gold random(2..4) × chapter × `goldMul` | framework (`miniboss` tag, `F:combat/gold_drop:13,16,24-25`) | lethal hit, at her body; pieces fly to the player 0.6 s later; anything left is absorbed at `sp/won` | the gold counter (HUD) |
| 1 sapphire shard (`sap 1`) | framework | lethal hit | stat item |
| heal orb (5 %) | framework `F:combat/apply:83` | lethal hit, at her feet | the orb |
| **random event** (item or buff) | module (S3 logic, S2b staging) | **coda E0–E120 in her field, grant at E56** | coda staging + title (7.3); chat record at the rift |
| title | FN-a | at the return | `홍련 도전 성공` / `레벨 업 · 아이템 상자 1개` |
| level up 1 | `lvup 1` → `F:mboss/sp/lvup:3-6` | at the return | the normal fanfare + chat `[레벨 업] …`; +12 HP / +2 ATK / +2 DEF; its usual pick (`pkPending +1`, Shift+F) |
| 1 item pick | `picks 1` | rift collapse 30 t after the return | one box at the rift; first click = one items-only chapter-rarity pick (`F:room/obj/do_mbox:1-13`) |

So the player makes two ordinary picks (the level-up's and the box's, as with 타키) and gets one event.

**Decision: the event comes between the ending and the item pick — as the coda of the ending, in her arena, before the
black and the result title.** Reasons:
1. The user's order: "원작과 같은 대사랑 연출을 하고 나서 특수한 이벤트가 일어났으면" — the event directly follows her lines
   and staging, in the same scene.
2. Staging: only the arena has her rig, the sword prop, the moon field and the kit; after `sp/won` there is no fight
   tick, no rig, and the room is not hers (all text after the return would be schedule-driven, framework.md §1.10 C).
3. Title slot and clutter: in the coda the title slot is free; at the rift the reward title owns it for 72 t while the
   level-up chat, the rift implosion and the box land at the same time.
4. The original's sequence survives: ending → black → result screen (「도전 성공」). The event sits inside her scene
   before the black, the result title follows it.
5. After the box would mean waiting on the player (boxes and the level-up pick are opened whenever the player likes).
6. Robust: one outcome per kill whatever happens — the reward hook (FN-b) applies it if the coda was cut (/reload) and
   drops the item at the rift if the inventory was full.

Rejected: (B) the whole event at the rift inside `sp/reward` — weaker staging, needs a schedule-driven ticker and a
deferred rift collapse; (C) roll in the arena, announce at the rift ≥ 72 t later — splits one beat in two places for no
gain (her lines cannot react to the roll: no invented lines).

Value next to 타키 (level up + 3 boxes): two extra chapter-rarity boxes are worth ≈ +12 % DPS at chapter 2
(rarity table `F:items/register:123-127`, ≈ +6 % per average pick); the event is worth ≈ +26–35 % (7.5.4). 홍련 pays
≈ 15–20 % more than 타키, in line with her harder fight (the run-ending ultimate, Q-B2).

### 7.3 The event: roll, staging, texts, grant

#### 7.3.1 The roll (S3 `tools/mboss_scarlet/reward.py` → `boss/scarlet/ev/roll`)
- Called from the module's `death_start` (step 3 above), so the coda knows its branch from E0 and the reward hook knows
  it even when the coda never ran.
- State (objective `hr`, never touched by `cleanup`; cleared by the reward hook, the module's `spawn` and `uninstall`):
  `#hrEv` 0 none · 1 item · 2 buff; `#hrEvDone` 1 = applied; `#hrEvDrop` 1 = the item waits for the rift (full inventory).
- Order: test override `rlk:hr ev.force` "item" / "buff" (ids below; in the `ev.*` storage namespace, §9.0) → **no
  duplicate**: the player holds `sword_hwamu` (`it_sword_hwamu ≥ 1`) → buff; `hrMoon ≥ 1` → item → else `random value
  1..1000`, `≤ api.EVENT['item_pm']` (500, written as a literal: regenerate to change) → item, else buff. One rift per
  run ⇒ at most one event per run; the duplicate rule only matters in tests (or in the cross-run variant, 7.5.3).
- Tests (module `test` hook, listed in `test/help`): `boss/test/pattern {id:91}` = next event 화무십일홍, `{id:92}` =
  월하대작, `{id:90}` = random again; then `boss/test/kill` plays ending + event. The override is cleared after use.

#### 7.3.2 Staging (S2b `seq/event`, kit by S1K, logic calls into S3) — 120 t, both branches

Common rules:
- Positions: her = the body / rig anchors (`hand_r`, `hand_l`, `chest`; S2a provides `rig/anchor/*`); the player =
  `@e[tag=rlk_body,limit=1]` (the avatar in F5 / shoulder view, the player in 1st person; chest = `~ ~1.1 ~`, README:1986).
  No camera control, no player teleport; the player may walk (the death state refuses every hit).
- Event entities (the thrown sword `item_display`, the moonlight orb `marker`) carry `rlk_room rlk_mb_aux rlk_hr_ev`:
  removed by the module `cleanup`, `mboss/cleanup_aux` and the `/reload` init. Summoned, then rotated with `tp` /
  `rotate` (summon ignores the execute rotation); never below the walk floor; one display per prop.
- Text slots: the kit typed line (subtitle) E4–E52 only; the event title E56–E110 (the 4x title ≤ 106 font px, the subtitle
  ≤ 192 font px: whole at every Auto GUI width down to 1920 × 1200 / 384 GUI px; the buff's third number on the actionbar
  for the same 54 t, `hudHold 54`; F3, HR-35); the black E110–E122 (subtitle cleared first). `vBig` / `ttlT` set for each title (the F5 crosshair title pauses, README:1979).
- The exit is shared: E34 clip `ev_leave` (a quarter turn away), E40 a burst of petals and wind hides her and the rig goes
  `state/hidden` — she leaves "바람 따라 구름 따라" instead of dying; the body stays invisible until `death_finish`.
- The coda lines are her NIKKE lines 24-25 of §3.0, verbatim from the user's page w2 (no invented line; switch
  `api.EVENT['lines']`). They are event casts (never skipped by the kit's "another line < 80 t ago" rule).
- Vanilla sounds only; no new texture: petals / moonlight / wind are particles (`cherry_leaves`, `dust`, `end_rod`,
  `gust`, all already used in the pack); the black is the fight's `black` overlay (`fx/hud/ovl`); the vignette `vig` (7.4.5)
  is one new kit font glyph (U+EC16; font glyphs are not in the items atlas).

**Item branch 「검을 건네다」 (`#hrEv 1`)**

| E | her (rig) | props | effects (kit `fx/p/*`) | sound (kit `fx/snd/*`) | text |
|---|---|---|---|---|---|
| 0 | `face/player`; clip `ev_give` starts from CS4's last pose: the left hand leaves the brim, the right hand raises the sheathed sword it holds | — | — | `ev_lift` | — |
| 4 | | | | | typed line 24 「조심하게. 칼자루를 쥐었다고 그 검의 주인이 되는 것은 아니니.」 (w2 l.405, 획득), cleared ≤ E52 |
| 12 | `present`: both hands hold it out horizontally at chest height, hilt to the player's right | | `ev_glint` runs along the scabbard | `ev_chime` | |
| 30 | `toss`: an underhand toss; the rig's scabbard and sheathed hilt hide (`scabbard gone`) | `ev_sword` display spawns at `hand_r` and arcs 14 t to 0.9 b in front of the player's chest (apex +1.2 b), one end-over-end turn (≤ 30°/t) | `ev_trail` each flight tick | `ev_toss` | |
| 34–40 | clip `ev_leave`; E40 `state/hidden` | | `ev_leave` at her chest | `ev_leave` | |
| 44 | — | the sword stops upright (scabbard down), bobbing | `ev_beam {h:80,t:6}` (a silver moonbeam onto it) | `ev_beam` | |
| 50 | | it sinks into the player's hand (scale 1 → 0.15 over 5 t) | | | |
| 56 | | removed | `ev_take {c:1}` (lilac) | `ev_take_i` | **grant** (`ev/apply`); title = the item's name + its own stars `화무십일홍 ★☆☆` (68 font px: the name dark_red as every mythic, the stars `rlk:items stars[<its star>]` read at run time by `ev/stars` — gold ★ / grey ☆ as in the inventory —, a light `shadow_color` on the root for legibility over the red field) / subtitle `[ MYTHIC ] 신화 아이템을 얻었습니다` (150 font px; `[ MYTHIC ]` dark_red with the same light shadow, the notice #E8E2D0) (F3, HR-33 / HR-35) |
| 56–108 | | | `ev_petals {n:2}` every 4 t round the player | | title holds |
| 110 | | | ovl `black` in 10 hold 12 out 0 (the original's fade, held to the return) | | |

**Buff branch 「월하대작」 (`#hrEv 2`)**

| E | her (rig) | props | effects | sound | text |
|---|---|---|---|---|---|
| 0 | `face/player`; clip `ev_toast` starts from CS4's last pose: the left hand leaves the brim; she looks up at the moon (the moon-gaze beat of her ending), the left hand rises palm up | — | — | `ev_chime` | — |
| 4 | | | | | typed line 25 「한잔할 텐가? 안주는 달빛과 바람일세.」 (w2 l.298), cleared ≤ E52 |
| 14 | `palm`: palm up at chest height | | `ev_palm` (a small moonlight "cup" in her palm, every tick) | | |
| 30 | `offer`: the palm extends to the player (the toast) | the moonlight orb (`marker`) leaves her palm and floats 12 t to the player's chest | `ev_palm` at the orb each tick | `ev_toss` | |
| 34–40 | clip `ev_leave`; E40 hidden | | `ev_leave` | `ev_leave` | |
| 42 | — | orb arrives (removed) | `ev_beam {h:80,t:10}` onto the player + `ev_wind {r:15}` (gust + petal swirl r 1.5) | `ev_beam` | |
| 56 | | | `ev_take {c:2}` (silver) | `ev_take_b` | **grant** (`ev/apply`); title `월하대작` (#DDE6FF, bold) / subtitle `최종 공격력 +27% · 치명타 확률 +10%` (154 font px) + actionbar `이동 속도 +10%` for the same 54 t (`hudHold 54`) (#FFE08A, numbers as `score` components of `#hrMoonAtk / #hrMoonCrit` / `#hrMoonSpd tmp`; F3, HR-35 / HR-11: the whole line is 228 font px, no one-line wording with every stat name fits 192 px; precedent 나비's `ab_buff`) |
| 56–108 | | | petals drift | | title holds |
| 110 | | | ovl `black` in 10 hold 12 out 0 | | |

Kit names (S1K; args in tenths, the precedents' convention):

| name | content |
|---|---|
| `fx/p/ev_glint` | the fight kit's blade glint along the scabbard (`hand_r` → sword tip) |
| `fx/p/ev_trail` | at the point: 2 `cherry_leaves` + 1 lilac `dust` [0.79,0.63,1.0] |
| `fx/p/ev_petals {n}` | `cherry_leaves` n + petal `dust` [0.84,0.36,0.53] (#D55D87, arena.md §4) n round the point |
| `fx/p/ev_leave` | 60 `cherry_leaves` + 30 petal `dust` + 1 `gust` at her chest, spread 0.6 / 1.2 / 0.6 |
| `fx/p/ev_beam {h,t}` | a silver column from +h/10 b down to the point over t ticks: `end_rod` (speed 0) + `dust` [0.87,0.90,1.0] scale 1.4 |
| `fx/p/ev_wind {r}` | a 16-point ring of small white `dust` + 1 `gust` + 6 `cherry_leaves`, radius r/10 |
| `fx/p/ev_palm` | 2 `end_rod` + 3 silver `dust` at the point |
| `fx/p/ev_take {c}` | 20 `end_rod` (speed 0.15) + a 16-point ring r 1.2 of lilac (c 1) or silver (c 2) `dust` |
| `fx/snd/ev_lift` | `item.armor.equip_chain` 0.6 / 1.2 |
| `fx/snd/ev_chime` | `block.amethyst_block.chime` 0.5 / 1.4 |
| `fx/snd/ev_toss` | `entity.breeze.wind_burst` 0.4 / 1.6 |
| `fx/snd/ev_leave` | `entity.breeze.whirl` 0.6 / 1.3 + `block.cherry_leaves.break` 0.5 / 1.0 |
| `fx/snd/ev_beam` | `block.amethyst_block.resonate` 0.7 / 0.9 |
| `fx/snd/ev_take_i` | `item.armor.equip_netherite` 0.7 / 1.1 + `block.note_block.chime` 0.6 / 1.5 |
| `fx/snd/ev_take_b` | `entity.generic.drink` 0.5 / 1.2 + `block.amethyst_block.resonate` 0.7 / 1.4 |
| ovl `black` | the fight's black overlay (U+EC10, §9.2), reused for the coda's fade; title only, root text empty + unstyled, `font:"rlk:mboss_hr"` on the glyph (no glyph-font inheritance) |
| glyph `vig` | new: an edge-only dark vignette (centre clear) for the item's 홍련일섬 cue (7.4.5); U+EC16, frozen at D0 so the hand-written item code can name it |

All sound ids are in `R:tools/dev/sim/rd/tests/sound_ids.txt`. Clips for S2a (rig contract, §2.5): `ev_give` 34 t
`{lift:0, present:12, toss:30}`, `ev_toast` 34 t `{look:0, palm:14, offer:30}`, `ev_leave` 10 t `{turn:0, gone:6}`. One
new model serves both the thrown prop (`item_display`, rig scale) and the item in hand: `rlk:mboss/scarlet/item_sword`
(F-I, HR-03: the slot / frame / ground contexts show its icon `item_sword_icon`, §7.4.1)
(written by S2a's rig generator inside its own RP tree `mboss/scarlet/**`), the rig's ORIGINAL sword and scabbard joined
as one sheathed piece, same texture (0 px), with gui / hand / ground / fixed transforms (held props point the right way;
nothing below the floor).

#### 7.3.3 Texts (Korean, verbatim)

| when | where | text | kind |
|---|---|---|---|
| item E4–E52 | subtitle (kit typed line) | 조심하게. 칼자루를 쥐었다고 그 검의 주인이 되는 것은 아니니. | her line 24, w2 l.405 |
| buff E4–E52 | subtitle (typed) | 한잔할 텐가? 안주는 달빛과 바람일세. | her line 25, w2 l.298 |
| item E56 | title / subtitle | 화무십일홍 ★☆☆ / [ MYTHIC ] 신화 아이템을 얻었습니다 | item name + its stars / tier + notice |
| buff E56 | title / subtitle / actionbar | 월하대작 / 최종 공격력 +27% · 치명타 확률 +10% / 이동 속도 +10% | buff name / numbers |
| return | title / subtitle (FN-a) | 홍련 도전 성공 / 레벨 업 · 아이템 상자 1개 | result-screen word |
| reward hook | chat | `[월하의 선물] 신화 아이템 ` + the item's display name in its own colours (`[ MYTHIC ] 화무십일홍` dark_red + the stars of `ev/stars`) — or — `[월하의 선물] 월하대작 — ` + the scope words of `api.EVENT['buff_scope']` (`api.BUFF_SCOPE_WORDS`: run `이번 런 동안`, forever `영구히`) + ` 최종 공격력 +27% · 치명타 확률 +10% · 이동 속도 +10%` with the three numbers as score components of `api.BUFF_FP` (F3, HR-33 / HR-11) | notice |
| reward hook, full inventory | chat | [월하의 선물] 보유 칸이 가득 차서 화무십일홍을 발밑에 놓았습니다. | notice |
| test | chat (FN-a) | [특수 보스 테스트] 도전 성공! 균열 자리에 아이템 상자가 떨어졌습니다(누르면 아이템 선택). [다시 하기] [로비로] | test notice |

Widths (26.3 glyph advances, Hud.extractTitle: title x4, subtitle x2, never wrapped; the Auto GUI width is 384 GUI px at
1920 × 1200): 4x title ≤ 106 font px, subtitle ≤ 192 font px (test_reward words: HR-35).

No how-to text anywhere (names, her wiki lines, numbers, notices only). "월하대작" (月下對酌) answers her encounter line
「…월하독작이 아니라, 대작이 되겠구만.」 (w1 l.64) and clear lines 4–5 (w1 l.84-85).

#### 7.3.4 Grant: give vs drop, once only (S3)

`ev/apply` (from `seq/event` at E56, or from the reward hook): returns if `#hrEvDone 1`; sets it; then as the player:
- **item** (`ev/item`): raise `rlk:pinv enh.sword_hwamu` to `api.EVENT['item_enh']` (1 = ★☆☆) with
  `items/enh_get` / `items/enh_add {id:"sword_hwamu"}` before the item is built (`F:items/enh_add:1-9` works by id, held
  or not); capacity check exactly as `F:root/give:4-5` (`data get storage rlk:pinv order` ≥ `invCap`): room →
  `items/give {id:"sword_hwamu"}` (`F:items/give:1-8`); full → `#hrEvDrop 1` (never `give` into a full inventory: it is
  silently lost, framework.md §3.8; ground items left in the arena are lost too).
- **buff** (`ev/buff`): `scoreboard players set @s hrMoon 1` (7.5.2); `items/stat_light` picks it up within 2 t.

`boss/scarlet/reward` (FN-b hook): `#hrEv 0` → `ev/roll` (the ending never reached it); `#hrEvDone 0` → `ev/apply`
(cut coda: grant without staging); `#hrEvDrop 1` → `execute at @e[tag=rlk_body,limit=1] run function rlk:items/drop
{id:"sword_hwamu"}` (the return point is a checked floor, `F:mboss/sp/ret_at`; a glowing mythic ground item with the
aura, [회수] / [판매], never despawns, removed at run end: `F:items/drop_spawn:2-14`, `F:run/end:18`) + the notice;
`ev/record` (chat line); then `#hrEv*` = 0 and `ev.force` removed. A run that ends between the kill and the reward
(impossible in practice: steps 5–7 are back to back) pays nothing, like every boss.

### 7.4 [ MYTHIC ] 화무십일홍

#### 7.4.1 Identity

| field | value |
|---|---|
| id | `sword_hwamu` (lowercase; parallels `sword_kirion`; `it_sword_hwamu` is created by `F:items/register:116-120`) |
| name / display | `화무십일홍`; shown as every mythic: `[ MYTHIC ] 화무십일홍 ☆☆☆` … `★★★` in `dark_red` (`F:items/register:6,9`, `F:items/set_name:1`, README:873) — the user's "[ MYTHIC ] 화무십일홍" |
| rarity / price | `mythic`; sells for 1 500 (`F:items/register:11`) |
| kind / slot | `type:"accessory"` like all 94 items; one of the 9–18 held-item slots (not the character's weapon slot 0) |
| look | `item:"minecraft:iron_sword"`, `model:"rlk:mboss/scarlet/item_sword"` (in the RP from I1) = S2a's model (the rig's ORIGINAL sheathed-sword model with gui / hand / ground / fixed transforms, same texture → 0 px; `F:items/build_display:26` uses a def's `model`); without it the vanilla sword shows. F-I (HR-03, lead decision 11-05): the item definition selects on `display_context`: gui / fixed / ground → the slot icon `rlk:mboss/scarlet/item_sword_icon` (the same sheathed sword drawn in GUI px along the slot's diagonal: scabbard 2.4 / grip 2.0 GUI px wide, the guard a 5.2-px bar, brass fittings, a crimson cord, the scabbard's decorated face toward the camera; rig sprites only, 0 px; lit front; `HR/renders/fi_icon.jpg`), the hands and the coda's thrown prop (`item_display` none) → the rig model (0.38 GUI px wide in a slot: the hairline HR-03 found); the rig model's guard card sits on its guard plate |
| engravings | 광전사 · 예리 (`["berserk","keen"]`: self-harm berserker + crits) |
| pools | **never**: added to `box_exclude` (`F:items/build_rarbuckets:3` → `["sword_kirion","demonomicon","sword_hwamu"]`): no level-up pick, box, shop slot or shop node (`F:items/pick_cand:2`), no 나무뿌리 bucket (`F:engravings/byeng_item:2`); only the 홍련 event (and the lobby trial codex, `F:codex/give2:5`) |
| codex | still listed in the 신화 tab (`F:codex/lists:1-4` appends `box_exclude` back); label `lab.sword_hwamu = {t:"화무십일홍",dy:"-0.632"}` in `F:codex/labels` (one line, like `불씨의 맹약`) |
| duplicates | the event never gives a second copy in a run (7.3.1); a lobby copy can stack: the stat line counts per copy (pack default), the effects once (`matches 1..`, one shared state) |
| rule exception | the mythic tier is for the seven archons + Columbina and no main-DPS items (README:858, `items.md:5`); 화무십일홍 is a NIKKE / Stellar Blade main-DPS sword → **user-requested exception (11-04)**, written into `items.md:5` and README:858: 「예외(사용자 요청 11-04): 화무십일홍(`sword_hwamu`, 신화) — 니케 · 스텔라 블레이드 홍련의 검. 특수 보스 홍련의 이벤트로만 얻는다(상자 · 상점 · 레벨 업 · 나무뿌리에 나오지 않음).」 |

#### 7.4.2 From her NIKKE skills (w2 l.339-361) to this pack

| NIKKE (lv 10) | here | hook (real, cited) | why the numbers move |
|---|---|---|---|
| 육참골단: after 10 normal-attack hits, ATK +23.15 % (5 stacks, 5 s), current HP −4.01 % | **every 4th basic-attack hit**: +1 stack (max 5, ATK +6 % each, all stacks last 6 s and refresh on each gain) and **−4 % of current HP while HP > 50 % of max** | `F:items/hook/on_hit` (from `F:combat/on_hit`, once per landed basic swing / arrow / shot); ATK via `F:items/hook/stat_buffs` `atkPct` | 10 AR shots ≈ 1 s in NIKKE; our 4 hits ≈ 1.8 s (1.4–3.2 hits/s per character, README:674-683). +115 % ATK would break the pack → +30 % at 5 stacks. Current-HP cost cannot kill; the 50 % floor parks the player in the low-HP band below without dropping to one-hit range (precedent 살롱의 초대장 pays only above half, `F:items/proc/salon_pay:1-3`) |
| 검신합일: when hit, 30 % chance to deal 138.24 % final ATK to the attacker; HP ≤ 60 %: crit dmg +6.61 % | **when a hit reaches you or a dash's i-frames eat it** ("물 흐르듯이 공격을 흘려내서", w2 l.601) — only the dash's own i-frames count (the dash tick + 6: `items/hook/on_dash` → `hw_dash`, `#hwDashEnd`); burst wind-up, void-fall and Ronova's revive i-frames reuse `dashInvT` and do not; a landed hit (the killing blow too) does (F3, HR-09): a lilac counter-slash on the nearest enemy ≤ 12 b that is not invulnerable (`tag=!rlk_mb_inv`: a boss in a cutscene / ghost / gauntlet is no target; F3, HR-39), **138 % ATK electro**, cooldown 4 s (S5; 2 s before, 7.4.7); no target = no cooldown spent. **HP ≤ 60 %: crit dmg +30 %** | `F:player/take_damage:37` (beside 불사자의 갈기's counter) and `F:player/dash_iframe:2`; queued, dealt next tick at `rlk_body` (no new damage inside a hit, README:860); the dash window from `F:items/hook/on_dash` (`hw_dash`), checked in `hw_ctr_q` (`#dodged tmp 1` = the dash_iframe path) | a NIKKE unit is hit several times a second (30 % ≈ 1 counter/s); our player is hit or dodges ≈ 0.2–0.6 times/s, near 1/s in crowded rooms or with dash spam → always, capped one per 2 s (the legendary counter 불사자의 갈기 has cd 2 s, `items.md:1367`; at 1 per s the item would beat 키리온 by 20+ points, 7.4.7). S5 measured the dense rooms (≈ 1.1 hits / s reach the player): at the 2-s cap ★★★ beat 키리온 by 6-16 points, so the cap is one per 4 s (7.4.7). Our crit dmg base is 150 % (`F:player/init:19`): +6.6 % is invisible, +30 % = the 예리 engraving's 4-piece bonus |
| 홍련일섬 (burst, 40 s): HP ≤ 50 % → crit rate +19.57 % for 10 s; 849.15 % final ATK to all enemies; the screen goes dark, then the slash | **when you use your elemental burst** (40 s internal cooldown): a 4-t hush (optional edge vignette), then **500 % ATK electro to every enemy ≤ 20 b** (S5; 849 % before, 7.4.7); if HP ≤ 50 % at the cast, **crit rate +20 % for 10 s** | `F:items/hook/on_cast_burst` (`F:char/burst_go:22` and Skirk's casts); damage dealt 4 t later from the item tick (not inside the burst's own damage) | no spare key exists (framework.md §4.1) → her burst = your burst; 40 s ≈ every 2–3 of our bursts |
| (stat) | 공격력 +25 % | `stats:{atkPct:25}` | the mythic ATK line (불씨의 맹약 +25 %, `items.md:1535`) |

#### 7.4.3 Numbers per star (exact engine rounding: `(base × fac + 500) / 1000`, `F:items/tune/apply_loop:6-10`, factors `F:items/tune/register:3`; stats the same way, `F:items/tune/stat_one`)

| constant (`tmp`) | m | ☆☆☆ | ★☆☆ (event) | ★★☆ | ★★★ (base) |
|---|---|---|---|---|---|
| stat `atkPct` (`F:items/tune/stats_scale`) | a | +13 % | +17 % | +21 % | +25 % |
| `#hwStkAtk` ATK per stack | a | 3 % | 4 % | 5 % | 6 % |
| `#hwStkDur` stack time | d | 84 t (4.2 s) | 96 t | 108 t | 120 t (6 s) |
| `#hwCtrCoef` counter | a | 69 % | 92 % | 115 % | 138 % |
| `#hwCtrCdT` counter cooldown | c | 104 t | 96 t | 88 t | 80 t (4 s; S5, was 40 t) |
| `#hwLowCd` crit dmg at HP ≤ 60 % | a | +15 % | +20 % | +25 % | +30 % |
| `#hwSlCoef` 홍련일섬 | a | 250 % | 334 % | 417 % | 500 % (S5, was 849 %) |
| `#hwSlCdT` 홍련일섬 cooldown | c | 1 040 t (52 s) | 960 t | 880 t | 800 t (40 s) |
| `#hwSlCrit` crit rate after the burst | a | +10 % | +13 % | +17 % | +20 % |
| `#hwSlCritDur` | d | 140 t | 160 t | 180 t | 200 t (10 s) |
| fixed (not tuned): 4 hits per stack (`#hwEvery`), 5 stacks (`#hwStkMax`), HP cost 4 % (`#hwCost`, the price — salon precedent `F:items/tune/b10:51`), floor 50 % (`#hwFloor`), low-HP 60 % (`#hwLowHp`), burst HP 50 %, ranges 12 / 20 b, slash delay 4 t | | | | | |

#### 7.4.4 In-game text (def, Korean; numbers at the current star through `tk` placeholders, README:879)

```
data modify storage rlk:items registry.sword_hwamu set value {item:"minecraft:iron_sword",model:"rlk:mboss/scarlet/item_sword",name:"화무십일홍",type:"accessory",rarity:"mythic",stats:{atkPct:25},abilities:[
 {text:"",extra:[{text:"「육참골단」",color:"#F28CB1"},{text:" 기본 공격이 4번 적중할 때마다 현재 체력을 조금 잃고"}]},
 {text:"",extra:[{text:"공격력이 증가한다. (중첩)"}]},
 {text:"",extra:[{text:"「검신합일」",color:"#F28CB1"},{text:" 공격을 받거나 대쉬로 흘려내면 가까운 적에게 반격해"}]},
 {text:"",extra:[{text:"번개 원소 피해",color:"#C58BFF"},{text:"를 준다. 체력이 60% 이하이면 치명타 피해가 증가한다."}]},
 {text:"",extra:[{text:"「홍련일섬」",color:"#F28CB1"},{text:" 원소폭발을 쓰면 주변의 모든 적을 베어 "},{text:"번개 원소 피해",color:"#C58BFF"},{text:"를 준다."}]},
 {text:"",extra:[{text:"이때 체력이 50% 이하이면 한동안 치명타 확률이 증가한다."}]},
 {text:""},
 {text:"",extra:[{text:"육참골단: "},{text:"공격력 +",color:"#FFE08A"},{tk:{c:"#hwStkAtk",x:1,d:1,p:0,u:"%"},color:"#FFE08A"},{text:" (최대 5중첩 · ",color:"#FFE08A"},{tk:{c:"#hwStkDur",x:1,d:20,p:1,u:"초"},color:"#FFE08A"},{text:")",color:"#FFE08A"}]},
 {text:"",extra:[{text:"체력 소모: "},{text:"현재 체력의 4% (체력이 절반 이하면 없음)",color:"#FFE08A"}]},
 {text:"",extra:[{text:"반격 피해: "},{text:"공격력의 ",color:"#FFE08A"},{tk:{c:"#hwCtrCoef",x:1,d:1,p:0,u:"%"},color:"#FFE08A"},{text:" (12칸 · 쿨타임 ",color:"#FFE08A"},{tk:{c:"#hwCtrCdT",x:1,d:20,p:1,u:"초"},color:"#FFE08A"},{text:")",color:"#FFE08A"}]},
 {text:"",extra:[{text:"치명타 피해 증가: "},{tk:{c:"#hwLowCd",x:1,d:1,p:0,u:"%"},color:"#FFE08A"}]},
 {text:"",extra:[{text:"홍련일섬 피해: "},{text:"공격력의 ",color:"#FFE08A"},{tk:{c:"#hwSlCoef",x:1,d:1,p:0,u:"%"},color:"#FFE08A"},{text:" (20칸 · 쿨타임 ",color:"#FFE08A"},{tk:{c:"#hwSlCdT",x:1,d:20,p:0,u:"초"},color:"#FFE08A"},{text:")",color:"#FFE08A"}]},
 {text:"",extra:[{text:"치명타 확률 증가: "},{tk:{c:"#hwSlCrit",x:1,d:1,p:0,u:"%"},color:"#FFE08A"},{text:" (",color:"#FFE08A"},{tk:{c:"#hwSlCritDur",x:1,d:20,p:1,u:"초"},color:"#FFE08A"},{text:")",color:"#FFE08A"}]}
],desc:["홍련이 사용하는 태도 화무십일홍은 그녀의 언니가 남긴 유품이다.","“이 검으로 베지 못하는건 없네. 강대한 적은 물론, 괴로운 과거마저 베어버리지.”"],engravings:["berserk","keen"]}
data modify storage rlk:items ids append value "sword_hwamu"
```
Both lore lines are verbatim from w2: the first is the page's own sentence (l.633, narration — no invented text set next
to her quote), the second her line (l.411, 대화 3). Skill names
in petal pink `#F28CB1`, element words in Electro `#C58BFF`, numbers `#FFE08A` (README:882).

`items.md` (new 8th entry of `## mythic — 8개`, the 3-star text as the file's convention, `items.md:1-9`):
```
8. 화무십일홍 `sword_hwamu`

   참고: 승리의 여신: 니케 홍련(전격 · 버스트 III) — 화무십일홍 · 육참골단 · 검신합일 · 홍련일섬.
   특수 보스 홍련(스텔라 블레이드)의 이벤트 보상 전용 — 사용자 요청(11-04)으로 신화 등급 규칙의 예외

    [ MYTHIC ] 화무십일홍
    공격력 +25%

    「육참골단」 기본 공격이 4번 적중할 때마다 현재 체력을 조금 잃고
    공격력이 증가한다. (중첩)
    「검신합일」 공격을 받거나 대쉬로 흘려내면 가까운 적에게 반격해
    번개 원소 피해를 준다. 체력이 60% 이하이면 치명타 피해가 증가한다.
    「홍련일섬」 원소폭발을 쓰면 주변의 모든 적을 베어 번개 원소 피해를 준다.
    이때 체력이 50% 이하이면 한동안 치명타 확률이 증가한다.

    육참골단: 공격력 +6% (최대 5중첩 · 6.0초)
    체력 소모: 현재 체력의 4% (체력이 절반 이하면 없음)
    반격 피해: 공격력의 138% (12칸 · 쿨타임 4초)
    치명타 피해 증가: 30%
    홍련일섬 피해: 공격력의 500% (20칸 · 쿨타임 40초)
    치명타 확률 증가: 20% (10.0초)

    각인  광전사 · 예리

    홍련이 사용하는 태도 화무십일홍은 그녀의 언니가 남긴 유품이다.
    “이 검으로 베지 못하는건 없네. 강대한 적은 물론, 괴로운 과거마저 베어버리지.”
```

#### 7.4.5 Cues (HUD, sound, particles; body effects at `rlk_body` `positioned ~ ~1.62 ~`, README:1986)

| moment | HUD | sound (new hand wrappers `F:snd/f422`… with keys `#k352`…, the `F:snd/f134` pattern) | particles |
|---|---|---|---|
| stack gained | sidebar `육참골단` = stacks (the `전의` / `열기` pattern in `F:items/hook/tick_player`), cleared at 0 | `block.amethyst_block.chime` 0.45 / 1.3; at 5 stacks + `block.cherry_leaves.break` 0.4 / 1.2 | 3 lilac `dust` [0.79,0.63,1.0] + 2 `cherry_leaves` |
| HP paid | the HP bar drops (no hurt number) | — | 2 crimson `dust` [0.75,0.12,0.25] |
| HP ≤ 60 % (crit dmg on) | — | — | 3 lilac `dust` every 20 t |
| counter | — | `entity.player.attack.sweep` 0.7 / 1.4 + `block.amethyst_block.resonate` 0.4 / 1.8 | at the target: 1 `sweep_attack`, a 2.5 b lilac crescent (6 `dust`), 6 `electric_spark` |
| 홍련일섬 cast | optional 6-t edge vignette (kit glyph `vig`, title; skipped while `vBig` ≥ 1, centre stays clear; vBig is counted down once per tick in every view by `F:view/tick` — F5, shoulder, first person, map, selection space, dead —, so the vignette shows in first person too once a title has run out; before F3 only the F5 path counted it down, sr-2; F3, HR-08) | `entity.breeze.inhale` 0.6 / 0.8 | lilac ring r 2 at the body |
| 홍련일섬 hit (+4 t) | — | `entity.player.attack.sweep` 1.0 / 0.6 + `entity.lightning_bolt.impact` 0.35 / 1.7 (once) | per target: 2 `sweep_attack`, a 1.5 b vertical lilac line, 8 `electric_spark`, 4 `cherry_leaves` |
| crit rate on (10 s) | — | — | 2 `electric_spark` every 10 t |
| 홍련일섬 ready | — | `block.chain.place` 0.4 / 1.6 (a sheathe click) | 4 `electric_spark` |
| ★★★ reached (optional) | chat `[홍련] 화무십일홍이 한층 더 날카롭게 벼려졌네. 자, 이걸 이제 누구한테 휘두를지 지켜보게나.` (w2 l.522, verbatim) | — | — |

Per tick while held: ≈ 8–12 commands (timers, queues, sidebar); triggers add one-off bursts.

#### 7.4.6 Implementation (SR; all hand-maintained sources per README:84 — no generator involved)

| file | change |
|---|---|
| `F:items/mythic/sword_hwamu/def` (new) | 7.4.4 |
| `F:items/register` | `function rlk:items/mythic/sword_hwamu/def` after `:113`; `"sword_hwamu"` appended to the `impl` list `:122` |
| `F:items/build_rarbuckets:3` | `box_exclude` += `"sword_hwamu"` |
| `F:items/tune/b10` | unconditional constants (7.4.3 bases + fixed ones) and `t.sword_hwamu = [{n:"#hwStkAtk",m:"a"},{n:"#hwStkDur",m:"d"},{n:"#hwCtrCoef",m:"a"},{n:"#hwCtrCdT",m:"c"},{n:"#hwLowCd",m:"a"},{n:"#hwSlCoef",m:"a"},{n:"#hwSlCdT",m:"c"},{n:"#hwSlCrit",m:"a"},{n:"#hwSlCritDur",m:"d"}]` + `ids append` (README:876) |
| `F:codex/labels` | `lab.sword_hwamu` |
| `F:items/hook/on_hit` | `execute if score @s it_sword_hwamu matches 1.. run function rlk:items/proc/hw_hit` |
| `F:items/hook/stat_buffs` | `execute if score @s it_sword_hwamu matches 1.. run function rlk:items/proc/hw_stat` (stacks → `atkPct`; HP ≤ 60 % → `critDamage`; `#hwCritT` → `critChance`) |
| `F:items/hook/tick_player` | `…matches 1.. run function rlk:items/proc/hw_tick` (timers, the two queues, ready cue, sidebar) and `execute unless … matches 1.. if score #hwOn itv matches 1 run function rlk:items/proc/hw_clear` (sold / dropped: state and sidebar gone) |
| `F:items/hook/on_cast_burst` | `execute if score @s it_sword_hwamu matches 1.. unless score #hwSlCd itv matches 1.. run function rlk:items/proc/hw_slash_q` |
| `F:player/take_damage` after `:37` | `execute if score @s it_sword_hwamu matches 1.. if score #hurtDmg tmp matches 1.. unless score #hwCtrCd itv matches 1.. run function rlk:items/proc/hw_ctr_q` |
| `F:player/dash_iframe` after `:2` | same call without the `#hurtDmg` test (a dodged hit) |
| `F:items/proc/hw_hit`, `hw_stack`, `hw_cost`, `hw_stat`, `hw_tick`, `hw_ctr_q`, `hw_ctr`, `hw_slash_q`, `hw_slash`, `hw_slash_fx`, `hw_ready`, `hw_clear` (new) | item damage by the README:859 recipe: `char/dmg_calc` with `rlk:tune m_sword_hwamu.coef` ← `#hwCtrCoef` / `#hwSlCoef`, `#skillDmg 0`, `#stunHit 0`, `#elem 3`, `#elU 1000`, `#icd 1`, **`#sub itv 1`**, targets tagged `rlk_hit`, `combat/apply_reset`, `#sub itv 0`, `char/after_hit` (eye_strike / lion_boom precedent). Counter target `@e[tag=rlk_mob,distance=..12,sort=nearest,limit=1]`; slash targets `@e[tag=rlk_mob,distance=..20]` (boss bodies are `rlk_mob`, `F:mob/setup:19`). HP cost with `operation -=` only (no negative literals), floor at 1. Item timers as fake players in `itv` (`#hwHits #hwStk #hwT #hwCtrCd #hwCtrQ #hwSlCd #hwSlQ #hwCritT #hwOn #hwPulse`) |
| `F:snd/f422`–`f429` (new) | the item's sound wrappers (`#k352`–`#k359`) |
| `F:items/proc/hw_dash` (F3, HR-09) | from `F:items/hook/on_dash`: `#hwDashEnd` = gametime + 6 (the dash's own i-frames) |
| `F:items/proc/hw_reset` (F3, HR-10) | from `F:player/reset_one`: `hw_clear` + `#hwCtrCd` / `#hwSlCd` / `#hwDashEnd` 0 — a new run clears them (like every item timer in `player/reset_stacks`); the in-run drop / pick-up rule (`hw_clear`, sr-9) stays |
| `F:items/enh_add` (optional) | `$data modify storage rlk:tmp eid set value "$(id)"` + `execute if score #enh tmp matches 3 if data storage rlk:tmp {eid:"sword_hwamu"} run tellraw …` (the ★★★ line) |
| `items.md`, README:856-905 (§6 item list, 등급 규칙 exception) | 7.4.1 / 7.4.4 |

#### 7.4.7 Balance against the existing mythics and legendaries

Model `HR/plan/calc/ev.py` (stand-alone, stdlib; S5 replaces its guesses — 2.2 basic hits/s, 0.3 counters/s, 3.5 average
stacks, HP ≤ 60 % 60 % of the time, ≤ 50 % at half the bursts — with rates measured by the balance probe), re-run with the
2-s counter cooldown by `HR/plan/calc/ev_cd40.py` (the range = 0.3 counters/s … the cooldown's cap; the 1-s cooldown gave
★★★ +86.5 % / +79.0 % at its cap):

| item (3 stars unless noted) | mid player Lv 15 (+50 % ATK from items, crit 20 / 150) | late Lv 30 (+100 %, 35 / 180) | source |
|---|---|---|---|
| 화무십일홍 ☆☆☆ / ★☆☆ (event) | +26-27 % / +35-38 % DPS | +23-24 % / +31-34 % | 7.4.3 |
| 화무십일홍 ★★☆ / ★★★ | +45-51 % / +57-65 % (+63 % in rooms at 0.3/s: the slash hits many) | +40-45 % / +50-58 % (+57 %) | |
| 불씨의 맹약 (mythic) | ≈ +58 % | ≈ +53 % | `items.md:1535`, `F:items/tune/b10` |
| 마검: 키리온 (legendary, 300-kill transform) | ≈ +65 % | ≈ +56 % | `items.md:1212` |
| 초월 · 악요개안 (mythic) | ≈ +18 % (+45 % ER) | ≈ +18 % | `items.md:1425` |
| 불사자의 갈기 (legendary, defensive counter 150 %, r 4, cd 2 s) | defensive | | `items.md:1367` |

At ★★★ it sits with 불씨의 맹약 and at most level with 키리온 even at the counter's cap — strong like a mythic. What keeps it
from breaking a run: the HP cost parks a long fight at ~50 % HP (more exposure, no healing from the item; anti-synergy
with 장생의 호리병's full-HP bonus, synergy with 살롱의 초대장's heat); the burst nuke is 250–500 % (S5; 425–849 % before) once per 40–52 s, ≈ 12 % of a
chapter-2 mob's HP after the level correction; the counter is capped at one per 4 s (S5; 2 s before). Tuning knobs for S5: `#hwStkAtk`,
`#hwSlCoef`, `#hwCtrCdT`, the floor (`#hwFloor`); S5 measures the counter rate and 홍련일섬's target count in dense rooms (≥
8 mobs) and in the 타키 / 홍련 fights; gate: ★★★ ≤ 키리온 at the 90th-percentile counter rate.

**S5 measurement (11-06; lead decision HR-20 / HR-21 / HR-39).** `HR/review/bal/reward_ev.py` = this model fed with the
probe's 홍련 boss runs (melee walker + dasher, P1 / P2 / whole, 33 runs of ed2e175: 1.64 basic hits / s → K 3.28, 「육참골단」
4.7 stacks at ★★★, HP ≤ 60 % for 0.73 of the time with the item's cost, counter events only at her hittable body — the
game's `hw_ctr` skips an `rlk_mb_inv` target and spends no cooldown, F3) and with the **dense rooms** of
`room/roomfair.py` (the REAL custom-mob brains / attacks / projectiles of chapters 1-3, #mobN 8 at map 5: 8-14 mobs, a
melee player who does not dodge; 9 rooms cleared in 26-86 s): 1.09 hits / s reach the player, the player's own hits 2.04
/ s (K 4.08), 홍련일섬's targets ≤ 20 b 10.7 in the first 5 s and 5.3 over a room. G2 is read four ways — at the p90 counter
rate over rooms + boss fights (each half the weight) and at the cooldown's cap, each with the slash on 1 and on 2
targets — at the boss fights' K **and** at the rooms' K (키리온 at the same K); all eight must be ≤ 키리온. With 2-s
counters (D0) ★★★ beat 키리온 at the cap by 15 / 16 points (2 targets, mid / late); the lead's start (counter 4 s) still
failed the late 2-target readings (69.7 vs 68.3 at the boss K) and 홍련일섬 had to come down to 500 % (700: 60.9 vs 58.8
at the rooms' K; 560 passed by 0.3, 500 passes by 1.3). Result (★★★ unless noted, mid / late):

| | mid (Lv15) | late (Lv30) |
|---|---|---|
| 화무십일홍 ☆☆☆ / ★☆☆ / ★★☆ / ★★★ (boss fights, median counters) | +24.0 / +34.1 / +44.6 / +56.2 % | +20.8 / +29.6 / +39.0 / +49.4 % |
| 불씨의 맹약 / 키리온 (boss K) | +60.7 / +77.6 % | +55.0 / +68.3 % |
| G1 ★★★ / 불씨의 맹약 | ×0.972 | ×0.964 |
| G2 boss K: p90 aoe 1 / aoe 2, cap aoe 1 / aoe 2 vs 키리온 | 63.3 / 68.8, 64.3 / 69.8 ≤ 77.6 | 56.2 / 61.4, 57.1 / 62.4 ≤ 68.3 |
| G2 rooms' K 4.08 (키리온 67.7 / 58.8) | p90 59.5 / 63.9, cap 60.3 / 64.7 | p90 52.5 / 56.7, cap 53.3 / 57.5 |
| G3 B1 (27 / 10 / 10) / item ★★ net (slot 4 %, exposure 2 %) | 32.8 / 36.1 % → ×0.976 | 34.9 / 30.8 % → ×1.032 |
So: `#hwCtrCdT` 40 → **80** (4 s at ★★★, 4.4 / 4.8 / 5.2 s below), `#hwSlCoef` 849 → **500**, `#hrMoonAtk` 20 → **27**
(7.5.4); `#hwStkAtk` 6 and `#hwFloor` 50 kept. Not in the gate: the slash really hits 5-11 mobs in a dense room (the
2-target model understates its room value), and at ev.py's guessed K 4.4 (not measured; the rooms' K is 4.08) the late
cap reading with 2 targets is level with 키리온 (56.0 vs 56.0; mid 63.2 vs 64.7) and G3 late ×1.048 (S5 report).

### 7.5 The permanent buff

#### 7.5.1 Options (all themed on her; numbers for the default run scope)

| option | effect | system | EV (mid / late, DPS) | verdict |
|---|---|---|---|---|
| **B1 「월하대작」 (月下對酌) — moonlight and wind** | 최종 공격력 +27 % (S5; 20 % before), 치명타 확률 +10 %, 이동 속도 +10 % | `ampAtk` (the existing final-ATK multiplier: `F:items/hook/stat_buffs:5`, `F:items/stat_light:39,47-48`; no user yet), `critChance`, `moveSpeed` | +32.8 % / +34.9 % and +10 % speed (S5 at 27; +25.5 / +27.5 % at 20), from the first second, no slot, no risk | **recommended** |
| B2 「유수(流水)」 — perfect dodges | a dash that eats a hit (`F:player/dash_iframe`) gives ATK +25 % for 5 s and makes the next basic attack release a lilac sword-qi wave (120 % ATK electro, 8 b); 3 s cooldown | `atkPct` timer + an item-style proc | +15–20 % in boss fights, +5–8 % in rooms; zero for players who walk out of attacks | swingy; overlaps 검신합일 |
| B3 「검기(劍氣)」 — the sword-qi | every 5th basic-attack hit releases a light-purple crescent (90 % ATK electro, 10 b, pierces) | an item proc without an item | ≈ +12–16 % | an item in disguise; one more particle proc on every character |

Why B1: the simplest true "buff" (one score, one `stat_buffs` line), good for every character and build, always on;
its value is set to match the item branch (7.5.4); and its theme closes her ending — "다음 번에 만나면, 그땐 같이 한잔 하면
좋을 텐데… 달빛과 바람을 안주 삼아… 말일세." becomes the drink she shares at once: moonlight = power, wind = speed.

#### 7.5.2 B1 specification (SR)

| item | value |
|---|---|
| state | objective `hrMoon` (per player: 0 none, 1 on) — `F:load:151` beside `nodeHp`; `F:uninstall:449` removes it |
| scope (default "run") | `F:player/reset_one` gets `execute unless score #hrMoonRun tmp matches 0 run scoreboard players set @s hrMoon 0` (load's 조절 지점 `#hrMoonRun tmp 1` = run; unset counts as run; F3, HR-11) (run start `F:run/start:9`, run failure `F:run/fail:3`, `rlk:reset`) — the `nodeHp` precedent (생명력 노드, `F:room/obj/do_hp:2`) |
| numbers | `load` "조절 지점": `#hrMoonAtk tmp 27` (S5, 7.5.4; 20 before), `#hrMoonCrit tmp 10`, `#hrMoonSpd tmp 10`, `#hrMoonRun tmp 1` (the scope) (not enhancement-scaled: it is not an item) |
| apply | `F:items/hook/stat_buffs`: `execute if score @s hrMoon matches 1.. run function rlk:player/hr_moon/apply` → `ampAtk += #hrMoonAtk`, `critChance += #hrMoonCrit`, `moveSpeed += #hrMoonSpd` (every 2 t through `F:items/stat_light:40`) |
| gain | `boss/scarlet/ev/buff` sets the score (7.3.4); the coda title and the rift chat line (the 생명력 node's chat precedent, `F:room/obj/do_hp:3`); every number the player reads (the coda subtitle / actionbar, the rift chat, the stat line) is a score component of the 조절 지점 constants (F3) |
| status | one lore line on ◆ 스탯 정보 (inventory slot 8) while on: `☾ 월하대작 · 최종 공격력 +27% · 치명타 확률 +10% · 이동 속도 +10% (이번 런)` (#DDE6FF; the bracket is the 4th `with` argument: `이번 런`, or `영구` when `#hrMoonRun 0`, F3) — `F:player/update_item`: `hrMoon` joins the change hash `#uh` and passes the line (or an empty text when off) as a new `$(moon)` argument that `F:player/update_item_macro` appends to the item's lore list (no item modifier: the pack has none, `R:data/rlk/item_modifier/` does not exist, and no gate would check a broken one). The ATK / 치명타 확률 / 이동 속도 rows of the same item show the raised values. No sidebar entry (the sidebar is for timed stacks) |
| codex | none (the codex lists items; the buff is explained by its title, the chat line and the stat line) |
| stacking | `ampAtk` multiplies the final ATK after all `atkPct` (not diluted by item ATK %); a future `ampAtk` source would add inside the same multiplier (100 + Σ); crit / move add to the item and engraving totals (no new cap: crit chance above 100 % is simply always-crit in `F:char/dmg_calc`); at most once per run (one rift per run, and the roll gives the item while the buff is on) |

#### 7.5.3 If the user picks "across runs" (Q1 = forever)
The pack's first meta-progression (only sapphire survives a run today: `F:player/reset_one:1`, README:639). Same B1 with
**smaller numbers, once ever**: 최종 공격력 +8 %, 치명타 확률 +4 %, 이동 속도 +4 % (the three `load` constants); `hrMoon` is
not reset by `reset_one` (the sapphire pattern) but is lost by `uninstall` like sapphire; once owned, the roll always
gives the item (7.3.1: `hrMoon ≥ 1` → item), so later rifts still pay; the stat item says `(영구)` and is visible in the
lobby. Switch: load's 조절 지점 (`#hrMoonAtk / #hrMoonCrit / #hrMoonSpd` 8 / 4 / 4 and `#hrMoonRun 0`: `reset_one` keeps
`hrMoon`, the stat line says `(영구)`) + `api.EVENT['buff_scope'] = 'forever'` (the rift chat's 「영구히」; regenerate);
test_moon checks that the two agree (`api.BUFF_VALUES[scope]`, `#hrMoonRun` = 1 for run). No line to delete (F3, HR-11).

#### 7.5.4 Expected value next to the item branch

| branch | right after the event | later in the run | costs |
|---|---|---|---|
| item ★☆☆ (granted) | +34.1 % / +29.6 % DPS (S5, measured) | ★★☆ +44.6 % / +39.0 %, ★★★ +56.2 % / +49.4 % (S5) — the mythic is the natural first target of the enchant node's 2–4 upgrades (README:962, README:1044) | a held-item slot (0 to ≈ −8 % when it replaces a common / rare item), long fights at ~50 % HP |
| buff B1 | +32.8 % / +34.9 % DPS + 10 % move speed (S5, `#hrMoonAtk` 27; D0's 20: +25.5 / +27.5 %) | the same (no upgrades) | none |

With the item realising about ★★ (≈ +40 % gross, ≈ +32–38 % after the slot and the exposure) and the buff ≈ +26–28 %
plus speed and safety, the two rolls are close: the item keeps the higher ceiling and the show, the buff is safe and
immediate. If the probe finds players reach ★★★ most of the time, raise `#hrMoonAtk` to 25 (+31 % / +33 %).
**S5 (11-06)**: on the probe's fight rates the item ★★ net is +36.1 % (mid) / +30.8 % (late); `#hrMoonAtk` **27** puts B1
at ×0.976 / ×1.032 of it (G3 ±5 %; the passing window is 24-29; D0's 20 gave ×0.90 / ×0.95).

### 7.6 Tests and gates (suites in `HR/tests/`, moved to `tools/dev/sim/hr/tests/` at I1; the `ar/tests` style: vendored `lib/` mcsim ← fgsim ← azsim ← cmsim, `check(id, cond, detail)`)

| suite (owner) | checks |
|---|---|
| `test_special_hr.py` (S1, §9.3) — the **fw** part of this section | registry validation (`winWord` / `rwHook` / `poof` only where allowed; `picks 1`, `lvup 1`, `xp 0` pass), her record has `winWord:"도전 성공"` + `poof:0b`, 타키 / spproto records and `boss/tachy/**`, `mboss/spproto/**` byte-identical, `sp/reward` lines (guarded 처치 line == today's line, the `winWord` line, exactly one hook line after `sp/lvup` and before `#spPk`), `death_finish` gating, `test/swon_msg_w`, `check_mboss_pack` 0; F3 **tap**: no F5 sneak-tap while a boss intro runs (HR-34) |
| `test_reward.py` (S3) | **flow** (mcsim chain): true_pct 100 → orb roll / gold × goldMul / 1 sapphire / `#mbKilled 1` → roll → ending → `seq/event` at H → grant at E56 → `death_finish` at H + 122 without poof → won → title words → exactly one level and `pkPending +1` → hook once → 1 box. **roll**: 10 000 seeded rolls 50 ± 1.5 %, `item_pm` 0 / 1000, forced branches (held sword → buff, `hrMoon` → item, `ev.force`), cleared after use. **inv**: room → `items/give`, order +1, `enh 1` (★☆☆); full at `invCap` 9 and 18 → no give, `#hrEvDrop 1`, one ground item at `rlk_body` with `rlk_daura`, one notice; never lost, never doubled. **reload**: `/reload` at every tick E0–E120 and during CS4 → the outcome applied exactly once (coda or hook), no `rlk_hr_ev` left. **words**: every on-screen string of 7.3.3 verbatim; the two coda lines equal `api.LINES` 24-25 = w2 l.405 / l.298 byte for byte; no other text; F3: at the reward hook objective hr holds only the event scores and storage rlk:hr no core / seq (HR-05); the item title / chat record star colours from rlk:items (HR-33); widths 4x title ≤ 106, subtitles ≤ 192 font px, the buff's third number on the actionbar, held for the title's 54 t (a coda run with the real player/hud/tick) (HR-35); **scope**: retuned constants and the forever dry build in the subtitle / actionbar / rift chat (HR-11) |
| `test_hwamu.py` (SR) | def / register / `impl` / `box_exclude` / codex label / engravings / `items.md` mirror; never offered (`pick_cand` / shop / 나무뿌리 buckets); tune table vs 7.4.3 for stars 0–3 (exact rounding); stacks: 4 hits → 1, max 5, refresh, all drop at 0; HP cost 4 % of current above 50 %, none at ≤ 50 %, never below 1, no negative literals; counter on a landed hit and on `dash_iframe`, 2 s cooldown, nearest ≤ 12 b, no target = no cooldown, queued (no damage inside `take_damage`); crit dmg only at ≤ 60 %; slash only from `on_cast_burst`, ICD, 4-t delay, every `rlk_mob` ≤ 20 b once, crit rate only if HP ≤ 50 % at the cast; `#sub itv 1` on all item damage; state and sidebar cleared when sold / dropped; sounds in `sound_ids.txt`; `vig` overlay skipped while `vBig` ≥ 1 (vBig counted down in every view, `F:view/tick`, F3 HR-08); both lore lines equal w2 l.633 / l.411; F3: dodge counters only inside a real dash's i-frames, never burst / fall / revive ones (HR-09); no counter / cooldown on an rlk_mb_inv body (HR-39); **run**: player/reset_one clears state + cooldowns (HR-10); **view**: vBig counted down once per tick in every view (HR-08) |
| `test_moon.py` (SR) | `stat_buffs` adds exactly +27 `ampAtk` / +10 crit / +10 move when `hrMoon 1` (`api.BUFF_VALUES`); final ATK = old × 1.27 (±1); `reset_one` clears (run) / keeps (`#hrMoonRun 0`); load's 조절 지점 agrees with api.EVENT buff_scope; the stat line's scope word (F3); `uninstall` removes; the stat-item lore line (`update_item_macro`'s `$(moon)`) present iff on and its numbers equal the constants |
| `ev_dry.py` (S2b, with S1K's kit) | both branches 120 t; every kit call exists; lines cleared before E56; title at E56, black at E110, subtitle cleared before it; sword prop rotation set after summon, never below the floor, arrives in front of the player wherever the player stands (8 positions incl. 20 b away); rig hidden at E40; `cleanup` leaves nothing |
| `review/bal/reward_ev.py` (S5) | `HR/plan/calc/ev.py` (+ `ev_cd40.py`) fed with probe-measured hit / dodge / burst rates; targets: item ★★★ within ±10 % of 불씨의 맹약 and ≤ 키리온 at the 90th-percentile counter rate, B1 within ±5 % of the item at ★★ net; S5 (11-06): G2 in eight readings — the p90 counter rate over rooms + boss fights (each half the weight) and the cooldown's cap, × the slash on 1 / 2 targets, × the boss fights' K and the dense rooms' K (`room/roomfair.py`: ≥ 8 custom mobs, the REAL brains and attacks) — all ≤ 키리온; counter events only at a hittable body (HR-39); results in 7.4.7 |

Gates (as 0-5, README:178-217, and §9.5): loadcheck 0 function load failures (all new hand files); `rplint` 0 (the item /
prop model); `check_mboss_pack` 0; two identical builds + RP hash; `ident.py` (only the allow-listed shared outputs
change, §9.5); `az/tests_cm/run_all.sh` and the four checkers with no new finding (SR's hand files are checked only by
`check_refs`); static rules (no negative `add/remove` literals, lowercase ids, vanilla sounds, glyph roots empty + `font`
named, no tip text); atlas: **+0 px** for this section; per-tick: the coda ≤ ≈ 300 commands at its peak tick (death state,
outside the fight average), the item ≤ ≈ 12 per tick held. In-game checks for the release note (no bot client on 26.3):
both branches by `pattern {id:91|92}` + `kill`, a full inventory, `/reload` in the coda, the dark_red title over the red
field, the stat-item lore line.

### 7.7 Owner stages, files, estimate

| stage | owns (this section) | size | time |
|---|---|---|---|
| D0 (lead) | registry fields of 7.1.2 (numbers, §8); `api.EVENT`, `api.ITEM_ID`, names (`#hrEv #hrEvDone #hrEvDrop`, `rlk:hr ev.force`, tag `rlk_hr_ev`), function names `boss/scarlet/{reward,ev/*}`, the guarded builders `api.ev_apply()` / `api.ev_title()` (`''` until `reward.py` exists), `SEQS += event`, clips `ev_give / ev_toast / ev_leave`, the look `scabbard gone`, kit names (8 presets, 7 sounds, line ids 24-25, glyph `vig` U+EC16), test ids 90–92, SR's public names (`sword_hwamu`, `hrMoon`, `#hrMoon*`, the model id `rlk:mboss/scarlet/item_sword`) | contract text | ≈ 1 h |
| S1 | FN-a / FN-b / FN-c: `T:build_mboss_core.py` (`snbt_entry`, `sp/reward`, `test/swon`, `test/swon_msg_w`, `death_finish`), `T:mboss_lib.py`, `T:check_mboss_pack.py`; a README fragment for the 특수 보스 rows (§9.7); the **fw** checks in `test_special_hr.py` | ≈ 60 generator lines; 4 changed + 1 new output | ≈ 2 h |
| S1K | the 8 `fx/p/ev_*` presets, 7 `fx/snd/ev_*` recipes, line ids 24-25, the glyph `vig` | ≈ 20 functions, 0 px | ≈ 2 h |
| S2a | clips `ev_give` (34 t), `ev_toast` (34 t), `ev_leave` (10 t) and the look `scabbard gone`; the model `rlk:mboss/scarlet/item_sword` (thrown prop + item icon: the rig's sheathed sword, rig texture, gui / hand / ground / fixed transforms) written by the rig generator inside its RP tree | ≈ 100 rig key files (≈ 0.4 MB) | ≈ 3 h |
| S2b | `seq/event` in `T:mboss_scarlet/seq.py` (both branches, the thrown sword / orb motion, titles via S3's `ev/title` through `api.ev_title()`); `ev_dry.py` | ≈ 8 seq functions | ≈ 2 h |
| S3 | `T:mboss_scarlet/reward.py` → `boss/scarlet/ev/{roll,apply,item,buff,title,record,reset}`, `boss/scarlet/reward`; `death_start` / `spawn` / `cleanup` / `uninstall` wiring; test ids 90–92 + `test/help` rows; `test_reward.py` | ≈ 14 functions | ≈ ½ day |
| **SR** (own slot beside S1K, §9.7) | every hand-file change of 7.4.6 and 7.5.2 (`items/**`, `player/{take_damage,dash_iframe,reset_one,update_item,update_item_macro,hr_moon/apply}`, `codex/labels`, `snd/f422-f429`, `load`, `uninstall`), `items.md`; README fragments (§6 item list, the 등급 규칙 exception, the boss section's item / buff rows; the lead merges them, §9.7); `test_hwamu.py`, `test_moon.py` | ≈ 25 new functions + ≈ 14 edited files, ≈ 0.05 MB | ≈ ½–1 day |
| S5 | `reward_ev.py` with probe rates; one tuning pass on `#hwStkAtk`, `#hwSlCoef`, `#hwCtrCdT`, `#hwFloor`, `#hrMoonAtk` | — | in the review pass |

Merge order as §9.1 (S1 → S1K → S2a → S2b → S3 → S4 → SR). SR only touches hand files; S3's calls to
`items/give {id:"sword_hwamu"}` are harmless before SR lands (`F:items/give:8` guards on the registry). Totals for this
section: ≈ 70 functions + ≈ 100 rig key files, ≈ 0.5 MB, **0 atlas px**.

Open points (defaults in place, each one knob): (1) Q1–Q4 as the table at the top (= §0.1 1-4). (2) The item is granted
at ★☆☆ (`api.EVENT['item_enh']` 0 = the pack's usual ☆☆☆). (3) The coda uses two NIKKE lines from w2 (switch `lines` off
for a wordless coda). (4) 검신합일's "30 % when hit" became "always, 2 s cooldown, dodges count" — the literal 30 % is one
constant away but rarely fires here. (5) The 50 % floor on 육참골단's HP cost is ours (NIKKE has none). (6) The 홍련일섬
edge vignette (on by default, 6 t, centre clear). (7) The dark_red item title over the red field (light `shadow_color`;
check in game). (8) The item icon is the rig's original sword (drop `model` for the vanilla sword) — F-I: in the slot / frame / on the
ground a chunky icon model of it (HR-03, §7.4.1). (9) `ampAtk` gets its
first user. (10) The CS4 hand-off (7.1.2): CS4 ends before the original's fade; registry `death` = H + 122 = 1164.

---------------------------------------------------------------------------------------------------------------------

## 8. Registry entry (D0 adds it with `enabled:false` and every number filled; S1 adds the §7 fields and the measured music length; I1 flips `enabled` and sets the icon model)
```json
{"id": "scarlet", "n": 21, "fn": "boss/scarlet", "kind": "special", "enabled": false, "w": 10, "minCh": 1, "maxCh": 99,
 "name": "홍련", "sub": "월하곡", "color": "#E8466A", "el": 3,
 "hp": 260, "xp": 0, "atk": 12, "lvAdd": 1, "dmgMul": 135, "goldMul": 6, "sap": 1, "picks": 1, "lvup": 1,
 "scale": 1.35, "hit": {"w": 1.2, "h": 2.9}, "intro": 650, "death": 1164, "deathSnd": false,
 "winWord": "도전 성공", "rwHook": true, "poof": false,
 "arena": "hr_field", "theme": "hr_field", "res": {"*": 10}, "phases": [100],
 "music": {"1": {"ev": "minecraft:music.overworld.cherry_grove", "len": 0},
           "2": {"ev": "minecraft:music.nether.crimson_forest", "len": 6076},
           "3": {"ev": "minecraft:music.overworld.cherry_grove", "len": 0}},
 "icon": {"item": "minecraft:iron_sword", "model": "rlk:mboss/hr_kit/gate_icon"}}
```
| field | value / why |
|---|---|
| `id` `n` `fn` `kind` | `scarlet`, 21 (the next special; 97-99 are tests), `boss/scarlet` (allowed for specials), `special` (framework.md §5) |
| `enabled` `w` | false at D0 (the module does not exist yet); I1 → true; `w` 10 = 타키's: equal rift share (question 4) |
| `minCh` `maxCh` | 1-99 like 타키 (question 4 may raise `minCh`) |
| `name` `sub` `color` `el` | 홍련 / 월하곡 / `#E8466A` / 3 Electro (her default hit element) |
| `hp` `xp` `atk` `lvAdd` `dmgMul` | 260 (S5: 타키's 250 + 4 %, T9 at Lv5 / 10 / 15, §4.8) / 0 (required with `lvup 1`, `T:mboss_lib.py:136-137`) / 12 / 1 / 135 — 타키's (§4.8) |
| `goldMul` `sap` | 6 / 1 through the scripted lethal hit (the body carries `miniboss`, framework.md §1.5; §7.2) |
| `picks` `lvup` | 1 / 1 (question 2; `load_registry` casts them, so D0 writes numbers, never placeholders) |
| `scale` `hit` | 1.35 / 1.2 × 2.9 (§2.1) |
| `intro` | 650 ≥ CS0 640 |
| `death` | 1164 = CS4 1042 (H) + §7's coda 120 t + 2 t (7.1.2); `END_PROFILE` `short` / `full` set it to their length + 122 |
| `deathSnd` | false (no wither death sound; she leaves) |
| `winWord` `rwHook` `poof` | FN-a / FN-b / FN-c (§7.1.3-7.1.5): written by S1 together with their validation (an unknown field changes nothing before S1's generator reads it) |
| `arena` `theme` | `hr_field` (n 5, §6; D0 adds `arenas.hr_field` = `api.ARENA_SPEC`) |
| `res` `phases` | `{"*":10}` (no immunity) / `[100]` (one pool; the steps are floors, §4.6) |
| `music` | 1 cherry-grove pool: `len 0` (play once) until S1 measures the 26.3 asset index into `MUSIC_TRACKS` and sets `music_len` (FN-e; the 아를레키노 D0 precedent); 2 crimson-forest pool (6076, already measured); 3 cherry grove once for CS4 |
| `icon` | vanilla `iron_sword` + kit model `rlk:mboss/hr_kit/gate_icon` (a red lotus over a long blade); until I1 the model is `minecraft:iron_sword` |

---------------------------------------------------------------------------------------------------------------------

## 9. Implementation split (parallel stages, strict file ownership; 타키 §9 / 아를레키노 §11 structure)

### 9.0 D0 — the frozen contract (lead, before any stage)
Branch `wip/hr-d0` from the current working branch head (README 0-2). Writes and freezes:
- `T:mboss_scarlet/__init__.py` (package doc + ownership) and **`T:mboss_scarlet/api.py`** (import it, never copy
  values): §1 identity / registry / `ARENA_SPEC` / `MOON_POS` / `arena_look(look)` (a request kept in `#hrLook hr`, §6.6;
  `''` until S1K's theme module exists); §2 `DMG`, `HITS` `{key: [(clip, event, shape, dims, tier, kb)]}`, `CUT_R` 3.2,
  `LOCK_LEAD` 7, `TELL_MIN` 12, `TELL_BIG` 20, `COMBO_GAP` 10, `MOVE_R` 22.5, `DISC` (hr 1.4, y 0.2-2.4, 1.8 b/t, life 16);
  §3 floors `FLOOR_P1` 600 ‰ / `FLOOR_ULT` 50 ‰, `PIPS` 5, `PIP_RULE` 'timed_dash' (§5.1), `A8_SCRIPT` / `A13_SCRIPT` /
  `R1` / `R3` (the §4.4-4.5 tables as tuples), `JUDGE_T` {a8: 194, a13: 258}, `DOWN_T` 200, `DOWN_FLOOR_WAIT` 40,
  `COUNTER_PM` (15, 15, 15) / (10, 10, 'kill'), `FAIL60_PM` 500, the switches `ULT60_LETHAL` false, `ULT5_LETHAL` true,
  `DARK_LIGHT` true, `WARN_TEXT`, `END_PROFILE` 'std', `INTRO_SKIP` true (`SKIP_HOLD` 20, `SKIP_T` 554), `P2_KIT`
  'footage', the A6 / counter triggers; §4 `BANDS`, `WEIGHTS`, `COOLDOWN`, the far / rear rules; §5 keys `P1` (a1 a2 a3 a4
  a6 a9 a10), `P2` (r1 r2 r3 a8 a13), `SEQS` (intro cs1 sq1 repel lead_down lead_stand ending event), `OWN`, `TEST_IDS`,
  `LINES` (§3.0, ids 1-25) + `LINE_AT`; §6 names (objective `hr`, `CORE_FP`, tags, storage `rlk:hr`, rig UUID); §7 rig
  contract `PARTS`, `LOOKS`, `RIG_CALLS`, `CLIPS {name: (len, loop, {event: tick})}` (the 47 clips of §2.5), `ANCHORS`,
  `check_manifest`, `rig()`, `play()`, `ev()`; §8 kit contract `KIT_PRESETS`, `KIT_PROPS`, `KIT_SOUNDS`, `KIT_HUD`,
  `OVERLAYS` (+ `vig`), `KIT_SPRITES` (the §9.2 table; the kit generator asserts it) and the card caps, `api.K`; §9
  `Writer`, `Pattern`, `Service`, `cut(made, lock, strike)` (a call builder that emits `function rlk:boss/scarlet/g/cut/…`
  lines; S4 owns `g/cut/**`), `bars(on)` (FN-f's `mboss_lib.bars`; `''` until S1 lands), and §7's frozen names
  (`EVENT`, `ITEM_ID`, `#hrEv*`, `rlk:hr ev.force`, tag `rlk_hr_ev`, the guarded `ev_apply()` / `ev_title()` that return
  `''` until `reward.py` exists, test ids 90-92, `sword_hwamu`, `hrMoon`, `#hrMoon*`, the model id
  `rlk:mboss/scarlet/item_sword`).
- `T:mboss_scarlet/stub_rig_manifest.json` (generated from `api.py --write-stub`, lead only): 29 parts + shadow, 47 clips,
  looks, anchors, calls.
- Empty stubs owned by the stages from then on: `seq.py` (`SERVICES = []`, S2b), `p_ghost.py` (`PATTERNS = []`, S4),
  `reward.py` (`SERVICES = []`, S3).
- The registry entry of §8 (`enabled:false`, every number filled) and `arenas.hr_field` = `api.ARENA_SPEC` (§6.1). With the
  theme module missing, `build_mboss_arena.py` writes stub functions for it (`T:build_mboss_arena.py:35`); those stubs, the
  new `F:mboss/ar/hr_field/**` and the dispatcher lines the new arena adds are declared D0 outputs. `mboss_lib.py` is not
  touched (a disabled special may already name an arena, `T:mboss_lib.py:140-141`).
- `HR/contract.md` (ownership, names, interfaces, rules, gates, the I1 `ident.py` allow-list of §9.5, change log) and
  `HR/stage_briefs.md` (one brief per stage in the README 0-7 ①-⑨ form).
Checked at D0: every registry-reading generator regenerates byte-identical outputs apart from the declared D0 outputs
(`git status`); `check_mboss_pack.py` 0 problems; `RLK_DEV=$DEV bash tools/dev/loadcheck.sh . hr_d0` → 0 failures (once
the EULA consent of §0.1 question 8 is recorded).
Namespaces: functions `boss/scarlet/**` (module), `boss/scarlet/rig/**` (S2a), `boss/scarlet/fx/**` (S1K),
`boss/scarlet/seq/**` (S2b via S3's generator), `boss/scarlet/{ev/**,reward}` (S3), `boss/scarlet/{p,g}/**` (S4 via S3's
generator), `mboss/arena/hr_field/**` (S1K via `build_mboss_arena.py`), `mboss/ar/hr_field/**` (core). Scores `hr`
(module, incl. `#hrEv*` and `#hrLook`), `hrRig*` (rig), `hrFx*` (kit), `hrMoon` (SR, per player); tags `rlk_hr_part`
`rlk_hr_anchor` `rlk_hr_fx` `rlk_hr_deco` `rlk_hr_p` `rlk_hr_p_<key>` `rlk_hr_cut` `rlk_hr_ghost` `rlk_hr_down`
`rlk_hr_stage` `rlk_hr_ev`; storage `rlk:hr` keys `core.*` (S3), `rig.*` / `seq.*` (S2a / S2b), `fx.*` (S1K), `g.*` (S4),
`ev.*` (S3); RP `rlk:mboss/scarlet/*` (incl. `item_sword`), `rlk:mboss/hr_kit/*`, font `rlk:mboss_hr`, bossbar
`rlk:hr_warn` — all lowercase.

### 9.1 Stages and ownership (write / delete only your own; scratch and tests under `HR/<stage>/`, `HR/tests/`)
| stage | owns | delivers |
|---|---|---|
| **S1 framework** | `T:build_mboss_core.py` (FN-a reward / test word per special, default 처치; FN-b the optional per-special reward hook, one literal line in `sp/reward` only for entries with `rwHook`, so 타키 / spproto outputs stay byte-identical; FN-c no `particle poof` in `death_finish` for entries with `"poof": false`; FN-f the bars-off flag `#mbBarOff mb`, zeroed in `fight_vars` and `cleanup_fight`, with `mboss/world:26` skipping `mboss/bars` while it is 1), `T:mboss_lib.py` (validation of `winWord` / `rwHook` / `poof`, `SPECIAL_OPT_HOOKS`, `MUSIC_TRACKS` cherry grove = FN-e, `bars(on)` = the flag + `bars_hide` / `bars_show`), `T:mboss_registry.json` (the §7 fields, the measured music length), `T:check_mboss_pack.py`; `test_special_hr.py`; README fragments (§9.7) | core outputs (`F:mboss/**` except module trees, `F:boss/test/**`) |
| **S1K kit + arena** | new `T:build_mboss_hr_fx.py` (with `--skip-rp`, as `build_mboss_kn_fx.py`), `T:mboss_hr_fx_paint.py`, `T:mboss_hr_fx_manifest.json` (generated); new `T:mboss_arena_hr_field.py` (with `look_lines`, §6.6) | `F:boss/scarlet/fx/**` (incl. §7's `ev_*`), RP `mboss/hr_kit/**` + atlas entries (filter-then-push), font `rlk:mboss_hr`; `F:mboss/arena/hr_field/**` (three looks) |
| **S2a rig** | new `T:build_scarlet_rig.mjs`, `T:scarlet_{pose,geometry,paint,clips}.mjs`, `T:scarlet_rig_manifest.json` (generated), `T:scarlet_rig_api.md` | `F:boss/scarlet/rig/**`, RP `mboss/scarlet/**` (incl. the item / thrown-sword model `item_sword`); the U1 and originality sheets; the 36 fight / gauntlet clips and the 3 §7 clips |
| **S2b sequences** (from `wip/hr-s2a`) | new `T:scarlet_cine.mjs` (the eight cinematic clips `intro`, `intro_end`, `cs1`, `sq1`, `repel`, `lead_down`, `lead_stand`, `ending`; S2a's generator imports it from a stub), `T:mboss_scarlet/seq.py` | the eight sequences of §3 and `seq/event` (§7.3.2) (`seq/**`, written by S3's generator); the cinematic strips |
| **S3 core + AI + P1 + shield + event logic** (from `wip/hr-s1`) | new `T:build_mboss_scarlet.py`, `T:mboss_scarlet/{core,ai,shield,p1,s3lib,reward}.py` | `F:boss/scarlet/**` except `rig/`, `fx/`, `seq/` and S4's dirs: the 17 hooks + `test/help`, `init`, the phase machine, floors, invulnerability / cine, counters (§3.4 HP steps), the down window, the shield (§5), `ult/fatal`, AI, A1-A10, HUD wiring (bars, under bar, the skip prompt), the look request, decor-prop spawning, pause / reload / cleanup, `ev/**` + `reward` (§7.3), tests |
| **S4 ghost patterns** (from `wip/hr-s3`) | `T:mboss_scarlet/p_ghost.py` | `F:boss/scarlet/p/{a8,a13,r1,r2,r3}/**` and the shared ghost helpers `F:boss/scarlet/g/**` (cut builder `g/cut/**`, reappear points, discs; written by S3's generator) |
| **SR reward items** | the hand-maintained files of §7.4.6 / §7.5.2 (`F:items/**` lines, the new `items/mythic/sword_hwamu/**` and `items/proc/hw_*`, `player/{take_damage,dash_iframe,reset_one,update_item,update_item_macro,hr_moon/apply}`, `codex/labels`, `snd/f422-f429`, `load`, `uninstall`), `items.md`; `test_hwamu.py`, `test_moon.py`; README fragments | 「[ MYTHIC ] 화무십일홍」 and 「월하대작」 |
Then **I1** (lead, `wip/hr`): merge S1 → S1K → S2a → S2b → S3 → S4 → SR, apply requests, `enabled:true`, the icon model,
regenerate all (`regen_all.sh` gets, after the Arlecchino lines, `[ -f tools/build_mboss_hr_fx.py ] && run
tools/build_mboss_hr_fx.py --skip-rp` and `[ -f tools/build_mboss_scarlet.py ] && run tools/build_mboss_scarlet.py`;
README 0-4's RP block gets `node tools/build_scarlet_rig.mjs --resourcepack $RP` and `python3 tools/build_mboss_hr_fx.py
--resourcepack $RP`; the arena theme is picked up by `build_mboss_arena.py`), gates, the README section 「홍련
(`boss/scarlet/`)」 and every README / RP README edit merged by the lead from the stages' fragments (§9.7). **R**: one
bundled review (state + real-game traps; fidelity vs the footage and the originality rule; fairness probe) → **F** fixes →
**S5** one balance pass → **V** verify → release (stamp 「홍련 · 특수 보스」; README 0-1 / 0-9 / 0-10 and the RP README
version rows).

### 9.2 Contracts between stages
- **Rig (S2a → S2b / S3 / S4)**: `api.RIG_CALLS` = `rig/{init,spawn,spawn_hidden,tick,kill,uninstall,flash,state/normal,
  state/hidden,face/player,face/track}`, macro `rig/face/set {yaw}`, `rig/look/form/{normal,ghost}`, `look/phase/{p1,p2}`,
  `look/hat/{worn,back,hand,world,gone}`, `look/sword/{hand,sheathed,gone}`, `look/blade/{off,lilac,pink,violet,gold}`,
  `look/scabbard/{hand,hip,gone}`, `look/face/{calm,smile,closed}`, `look/props/none`, `rig/anchor/<api.ANCHORS>`,
  `rig/play/<clip>` / `rig/start/<clip>` for every `api.CLIPS` key (47). Raiden / Apep / 타키 semantics: `play` = tick 0 at
  the next `rig/tick`, event e on the e-th `rig/tick`, `play` replaces the running clip; the rig never moves the anchor
  except `face/*`, never reads module scores, never goes below the floor; `state/hidden` scales parts to 0 in place. Until
  S2a's manifest exists, `api.rig()` points at S3's `rig_stub/**` (every call; `play/<clip>` sets `#rigc hr`).
- **Kit (S1K → S2b / S3 / S4 / §7)** through `api.K` only (it returns `''` while the kit manifest is missing; values in
  tenths of a block / degrees / ticks; `c` per §4.1). Presets `fx/p/<name>`: `qi_arc {r,yaw,pitch,roll,c}`, `qi_ring {r,c}`,
  `qi_band {len,yaw,pitch,roll,sw}`, `qi_x {r}`, `qi_dome {r}`, `qi_vert {h,yaw,c}`, `qi_fan {h,c}`, `qi_wedge {r,roll}`,
  `qi_ribbon`, `qi_line {len}`, `qi_cut {len}`, `glint {c}`, `star4`, `yellow_tell {t}`, `ghost_burst`, `ghost_trail {len}`,
  `ghost_flash`, `afterimage {len}` (one translucent lilac silhouette card per frame, ≤ 4 alive, fading over 6 t — no rig
  copy), `blink_bubble`, `shield_refill`, `pip_break`, `dive_impact {r}`, `light_column`, `claw_streaks {r}`, `burst_radial
  {r}`, `dust_ring {r}`, `kick_flash`, `clash_gold`, `clash_spark`, `clash_arc`, `deco_bolt`, `scarlet_line {len,yaw,roll}`
  (the roll sign stated in `api.K`), `petal_burst {r}`, `petals_drift`, `petals_wind`, `petals_heart`, `motes_warm`,
  `leaves_dark {n}`, `leaves_swirl`, `ambient_p1`, `ambient_p2`, `arrive_rift`, and §7's 8 `ev_*` (7.3.2). Props
  `fx/prop/<name>` (`@s` = the card / marker): `disc` (one card per projectile, summoned then rotated), `petal_big {look}`
  (whole / cut / split; CS1 uses two), `moon_halo {look}` (p1 / p2 / off), `lotus {look}` (bud / bloom), `seat_rock {look}`
  (bottle / bare / set). Switches around preset calls: `fx/keep_on` / `keep_off`, `fx/follow_on` / `follow_off` (F2). Sounds `fx/snd/<name>`: one recipe per sound named in §3-§5 and §7 (vanilla ids only;
  `mboss_lib.sound` min-volume rule; every id used here is in `R:tools/dev/sim/rd/tests/sound_ids.txt`). HUD (font
  `rlk:mboss_hr`, glyph roots empty and unstyled, the font ends with a `minecraft:default` reference): `fx/hud/line {id}`
  (ids 1-25, letter reveal, overlay-aware, §3.0), `fx/hud/ovl {g,in,hold,out}` (`g` = black, negative, pinkwhite, red_tint,
  magenta, white; glyphs U+EC10-EC15 ≈ 144 × 81, sized as Apep's; `vBig` set to in + hold + out), the glyph `vig` U+EC16
  (§7.4.5), `fx/hud/warn {on}` (bossbar `rlk:hr_warn`), `fx/hud/skip {s}` (the intro's actionbar prompt 「⊙ 건너뛰기」 + the
  control hint at brightness step s 0-4, `hudHold` 2; `s:5` clears it), `fx/hud/clear`. Gate icon
  `rlk:mboss/hr_kit/gate_icon`. Caps: fx cards 96, ambient 48 (the 아를레키노 values; the ager kills the oldest). Kit wiring
  by S3: `cleanup` → `fx/clear` + `fx/hud/clear`; `pause` / `death_start` → `fx/clear` (CS4 then starts its own effects);
  `uninstall` → `fx/uninstall` (cards, objectives, the warn bossbar). Kit sprites (`api.KIT_SPRITES`; the kit generator
  asserts the sum ≤ **0.26 M px**; the overlays and `vig` are font glyphs, not in the items atlas):

| sprite | frames × px | px |
|---|---|---|
| `qi_arc` crescent (also `qi_vert`, `qi_fan`, and `qi_x` = two crossed arcs) | 4 × 128×64 | 32 768 |
| `qi_ring` flat ring (also `qi_dome`'s rim) | 2 × 128² | 32 768 |
| `qi_band`, `qi_ribbon`, `ghost_trail` | 2 × 128×32 each | 24 576 |
| `qi_dome` shell, `qi_wedge` | 128×64, 64×128 | 16 384 |
| `glint` + `star4`, shards (`shield_refill` / `pip_break`), lotus (bud / bloom) | 2 × 32² each | 6 144 |
| `yellow_tell` sphere + flare line | 64² + 128×16 | 6 144 |
| `ghost_burst` mist / ribbons, `ghost_flash`, `blink_bubble` | 3 × 64², 64², 64² | 20 480 |
| `afterimage` silhouette | 64×128 | 8 192 |
| `dive_impact` / `burst_radial` | 128² | 16 384 |
| `light_column`, `claw_streaks`, `deco_bolt` | 32×128 each | 12 288 |
| `clash_gold` / `kick_flash`, `clash_spark` / `clash_arc` | 2 × 64², 2 × 32×128 | 16 384 |
| `scarlet_line` | 256×16 | 4 096 |
| `petal_big` (whole / cut / split), small petals and leaves | 3 × 64², 8 × 16² | 14 336 |
| `moon_halo` (p1 / p2) | 2 × 96² | 18 432 |
| `disc` | 2 × 64² | 8 192 |
| `seat_rock` (vanilla block textures) | — | 0 |
| **total** | | **237 568 ≈ 0.24 M** |

- **Shield (S3 → S4)**, `api.SHIELD_CALLS`: `shield/arm` (5/5 + under bar), `shield/cut {s}` (register a counting cut's strike
  tick and store its lock point; the pip check runs at s and s + 1 only: the player's `dashInvT` 1..6 at s or 1..5 at
  s + 1, feet within `CUT_R` + 3.0 of the lock point, §5.1), `shield/judge` (→ `#gres hr` 1 deflect / 2 fail), `ult/fail60`,
  `ult/fatal`, `shield/off`. Cut hazards only through `api.cut(made, lock, strike)` (S4's `g/cut/**`); discs only through
  `api.disc()`.
- **Sequences (S2b → S3 core)**: `api.Service` per `api.SEQS` (8: the seven of §3 + `event`); `seq/<name>/{start,tick,cancel}`;
  `repel {at:60|5}`, `lead_stand {g:a8|a13}`; the core starts them and owns invulnerability / cine / floors / the kill at
  `repel` 102 (the sequence emits the HP-step event, the core applies `true_hit`) and the intro skip (it reads the sneak
  hold and calls `seq/intro/skip`); body moves inside sequences via `mboss/mv/*` + `mv/ok` only.
- **Event hand-off (S2b → S3 / §7)**: `seq/ending` sets `#sqdone` at H = 1042; the core starts `seq/event` in the same
  `death_tick` (§7.1.2); `seq/event` calls S3's `ev/apply` and `ev/title` only through `api.ev_apply()` / `api.ev_title()`;
  registry `death` = H + 122 = 1164 covers the coda.
- **Arena (S1K → all)**: `api.arena_look('moon'|'crimson'|'dark')` = a request (`#hrLook hr`) the core turns into the look
  job when no arena job runs (§6.6; `''` until S1K's theme exists); decor props through `api.K.prop`.
- **Framework (S1 → S3 / §7)**: FN-a/b/c behind registry fields; FN-f through `api.bars(on)` (never the framework-private
  `#mbBar`); the module reads `#mbKind 2` only for wording; `sp/*` never calls module code except through the existing
  dispatchers and the FN-b line.
- **Test ids** (`boss/test/pattern {id:N}`, `api.TEST_IDS`, `test/help` lists them): 1 A1 · 2 A2 · 3 A3 · 4 A4 + A5 · 5 A6 ·
  6 A9 · 7 A10 · 11 R1 · 12 R2 · 13 R3 · 20 CS1 → SQ1 → A8 · 21 A8 now (5/5) · 22 A8 with 0 pips (→ deflect → CS2 → down) ·
  23 A8 fail · 24 CS2 only · 25 down window · 26 `lead_stand {g:a13}` + A13 · 27 A13 now · 28 A13 with 0 pips (→ CS3 →
  kill → CS4 → the coda) · 29 A13 fail (instant death; in a test → `test/defeat`) · 30 intro replay (P1 / P2 only) · 31 look `dark` on /
  off · 32 look `crimson` · 33 P2 now (skip CS1 / A8) · 34 HP = 5 % floor + 1 · 35 intro skip at tick 100 (P1 / P2 only) · 80 HP = next
  floor + 1 · 90 the next event random · 91 the next event = 화무십일홍 · 92 the next event = 월하대작 (§7.3.1) · 99 hold.
  `test/lock {id}` for 1-13. A forced fail (23 / 29: `#pipoff`) applies to that gauntlet's judge only (`core/g/end`,
  `core/g/pause` clear it; F1, HR-06).
- **No cross-stage reference before it exists** (a missing function fails the whole load): `api.rig`, `api.K`,
  `api.arena_look`, `api.bars`, `api.ev_apply()`, `api.ev_title()` return the right line or `''`.

### 9.3 Tests (harness of `S:tk/tests` / `tools/dev/sim/ar/tests`: the `S:az/tests_cm/lib` sims vendored unchanged with md5s + `HR/tests/lib/hrsim.py`)
- `test_special_hr.py` (S1): registry validation (special `scarlet`, arena `hr_field`, the new fields), FN-a wording, FN-b
  line only for `scarlet` (타키 / spproto `sp/reward` byte-identical), FN-c, FN-f (bars stay off while `#mbBarOff 1`, the
  flag cleared by `fight_vars` / `cleanup_fight`, every other boss's bars unchanged), the rift roll share 10 : 10 (seeded,
  ≈ 50 %), music pool length; the **fw** checks of §7.6.
- `test_kit.py` (S1K): every contract name with the right macro args; caps (96 / 48) and ager; the sprite table vs
  `api.KIT_SPRITES` (sum ≤ 0.26 M); a line during an overlay keeps the overlay on the title, `ttl_blank` after it; the warn
  bossbar lifecycle; the skip prompt (`hudHold` set, cleared by `s:5`, text = 「⊙ 건너뛰기」 verbatim + the hint); pause
  clear; uninstall leaves nothing; vanilla sound ids only; glyph root rule; lines equal `api.LINES` 1-25 verbatim.
- `test_arena_hr.py` (S1K): walk disc flat full blocks; plants only `#rlk:dash_pass`; nothing overhead below y 226 except
  the light layer; barrier closed; all six transitions `moon` ↔ `crimson` ↔ `dark` block-exact (absolute spans, §6.6) and
  a look call issued while a job runs (the request waits, then runs); the `dark` job's real slices 3 t apart; slices / fill
  / command limits; light ≥ 12 (moon, crimson) and ≥ 6 (dark) on the walk disc; every plant on a valid support in every
  look; the moon disc unobstructed from C and from `start`; no stairway within ± 20° of the moon's bearing; no two block
  masses ≥ 8 b tall mirrored about it within ± 25° (no gate framing); no text display or glyph column anywhere (§1.5).
- `test_rig.py` (S2a, S2b for the cinematic clips): manifest vs contract (`api.check_manifest`, 47 clips); floor-dip and
  ≤ 120°/t over every clip tick (blade tip, scabbard tip, brim, hair, skirt); hat states; the brim squares not coplanar;
  ghost models use only the ghost texture; UUIDs / tags; kill / uninstall leave nothing; `seq.py` writes only `seq/**`; the
  palette-distance check of §1.5; the model `item_sword` (gui / hand / ground / fixed transforms, rig texture only).
- `test_scarlet.py` (S3): hooks; the phase order of §4.6 incl. both fail branches; floors 60 % / 5 %; invulnerable windows;
  the CS2 / CS3 HP steps; the down window (both exits); pips (a timed dash at a counting cut −1 whatever its direction,
  disc dodges ignored, one per cut, never below 0); the judge; fail-60 (500 ‰ + the push, never kills at 1 HP);
  `ult/fatal` (through i-frames and shields, skipped while `rnDie`, a revive → A13 again); the banner never on during A8
  with `ULT60_LETHAL false` nor during A13 with `ULT5_LETHAL false`, incl. restarts after pause / revive; the intro skip
  (sneak held 20 t at any tick 20-540 → black, line 11 at the jump, the same end state as the full intro; released early →
  no skip); counter / skill / far / rear triggers, weights and cooldowns (seeded); bars off in CS1 and back in SQ1; the look
  request through pause / reload inside a running job; her distance to the player over CS4 300-1042 is 3.5-6 b when the
  player has not moved; pause / reload in every phase and sequence (§3.8); cleanup leaves no `rlk_hr_*`; tick cost.
- `pat_p1.py` (S3), `pat_ghost.py` (S4): every hit tick = its clip event and the §4.5 tables; tells ≥ 12 / 20, gaps ≥ 10,
  lock lead 7; shapes / tiers / kb; quiet, no decal; every counting cut made ≥ 12 t before its strike, following the player
  until the lock, act 2, dodgeable; the pip window in the sim with four dash agents — stand-then-dash, and move-then-dash
  outward / sideways / inward at 0.22 and 0.28 b/t — each scoring with ≥ 90 % of correctly timed dashes; discs (speed, aim
  at release, wall stop, one card); reappear points (bearings, distances, `mv/ok` within `MOVE_R` 22.5 with the player at r
  22 facing outward, the guaranteed fallback, never in blocks); the darkness ticks; a 2-charge dasher reaches every
  counting window; cancel at every tick leaves nothing.
- §7's suites (7.6): `test_reward.py` (S3), `test_hwamu.py` and `test_moon.py` (SR), `ev_dry.py` (S2b).
- I1: `gen_check.py` (every generator twice → identical; documented order and reverse; owned paths only), `ident.py`
  (every other boss / mob output byte-identical except the allow-list of §9.5), the moved suites `tools/dev/sim/ar/tests`
  and `az/tests_cm` (`run_all.sh`, run from a copy, `R:tools/dev/sim/README.md` §1) and `S:tk/tests` with no new failure;
  S5: `HR/review/bal/hrfair.py` (§4.8 targets, 타키 baseline by the same tool) and `reward_ev.py` (7.6).

### 9.4 Renders (≤ 640 px; delete intermediates)
S2a: `s2_U1.jpg`, `s2_orig.jpg`, clip strips, prop side views, the brim close-up, the `item_sword` model (§2.7). S2b: the
cinematic strips vs the footage sheets (incl. CS1's two petal cards and the CS4 walk-in). S1K: the kit sprite sheet, one
strip per preset / prop, the overlay glyph sheet, the three arena looks (§6.8). S3 / S4: top-down hit-shape diagrams over
time per pattern (`HR/renders/s3_<key>.png`, `s4_<key>.png`) and one gauntlet timeline chart per gauntlet (cut ticks, lock
ticks, dash windows, pips). SR: the item tooltip and the stat item, rendered as text. The lead sends `s2_U1.jpg` +
`s2_orig.jpg` to the user as soon as they exist.

### 9.5 Gates (every stage before hand-off; all at I1 / V — README 0-5)
1. `RLK_DEV=$DEV bash tools/dev/loadcheck.sh <worktree>/roguelike hr_<stage>` → `0 function load failure(s)` (after the
   EULA consent of §0.1 question 8 is recorded in README 0-8).
2. `python3 -I tools/dev/rplint.py <RP>` → 0 problems (stages touching the RP).
3. Regenerate twice → byte-identical, RP hash equal; `python3 tools/check_mboss_pack.py` → 0 problems.
4. Static rules (README 0-6): no negative `scoreboard players add/remove` literals; macro lines parse with `"help"`; NBT
   paths valid; no `tp` into blocks (destinations via `mv/ok`); nothing below the floor; vanilla sounds only; no glyph-font
   inheritance; lowercase ids; held props right from the side; one card per projectile; rotation after `summon`; no floor
   decal; on-screen text only names, the sub, the 25 lines of §3.0, the warning banner, the intro's skip prompt, §7's item
   / buff names, numbers and notices (7.3.3), 「도전 성공」 and system notices.
5. Budgets: this boss ≤ 0.43 M items-atlas px (rig ≤ 0.15 M, kit ≤ 0.26 M, gate icon ≤ 0.005 M; §7 0 px, 0.015 M reserve)
   and the stitched atlas ≤ 13.2 M (`python3 -I tools/dev/atlas_px.py <RP>`); model elements at rest ≤ 6 500; average
   commands per fight tick ≤ Apep's (≈ 830; target ≤ 600, look-job spikes ≤ 5 k).
6. The stage's suites green; `ident.py` green against the allow-list; every other generator's output unchanged except the
   stage's own files. S1, SR, I1 and V also run `az/tests_cm/run_all.sh` and the four checkers (`check_refs`, `check_macro`,
   `check_nbtpath`, `mb/lint_mc` in `R:tools/dev/sim/`) and diff them against the `35b82e5` tree: no new failure or finding.
The I1 allow-list (frozen in `HR/contract.md`): the FN outputs (`mboss/sp/reward`, `mboss/test/swon`, `mboss/test/swon_msg_w`
(new), `mboss/death_finish`, `mboss/register`, `mboss/world`, `mboss/fight_vars`, `mboss/cleanup_fight`); every
`F:mboss/**` file that gains an n 21 / `hr_field` line when I1 enables her (`d/*`, `register`, `sp/gate`, `sp/prep`,
`sp/pp/scarlet`, `sp/g/scarlet`, `cb/inc/scarlet`, the `ar/*` and `arena/*` dispatchers + `ar/hr_field/**` +
`arena/hr_field/**`, `fight_vars`, `test/help_special`, the uninstall dispatch); the SR hand files.

### 9.6 Estimates
| part | functions | size |
|---|---|---|
| rig (29 parts + shadow × 47 clips; ≈ 2 290 scripted ticks — intro 640, CS1 213, CS4 1042, repel 104, lead-ins 152, SQ1 60, §7 78 — keyed every 2-4 t on quiet beats) | ≈ 5 500 (the earlier 3 800 + the precedents' 60-70 % overrun: 타키 1 300 → 2 205, 아를레키노 2 000 → 3 244) | ≈ 9-12 MB |
| module core + AI + shield + P1 + HUD + skip + look request + event logic (§7) + tests | ≈ 550 | 2.3 MB |
| ghost patterns (A8, A13, R1-R3, discs, cut builder) | ≈ 420 | 1.8 MB |
| sequences (8, incl. `event`) | ≈ 270 | 1.3 MB |
| kit (≈ 53 presets / props incl. §7's 8, ≈ 97 sound recipes, HUD, 25 lines) | ≈ 490 | 2.1 MB |
| arena `hr_field` (+ `mboss/ar/hr_field`; absolute-span look jobs) | ≈ 140 + 17 | 1.8 MB |
| framework FN-a/b/c/f | ≈ 12 | — |
| SR hand files (item + buff) | ≈ 25 new (+ ≈ 14 edited) | 0.05 MB |
| **total** | **≈ 7 400** | **≈ 21 MB** |

| stage | agent-hours | wall slot (2 agents at a time; slot A / B) |
|---|---|---|
| D0 (lead, incl. §7's frozen names) | 4 | h 0-4 |
| S1 framework (FN-a/b/c/e/f, registry fields, `test_special_hr.py`) | 5 | A h 4-9 |
| S2a rig (paint, U1 / originality sheets ≈ h 10 → to the user, 36 fight clips + 3 §7 clips, `item_sword`) | 10 | B h 4-14 |
| S3 core + AI + P1 + shield + event logic (from `wip/hr-s1`) | 13 | A h 9-22 |
| S2b cinematic clips + sequences incl. `seq/event` (from `wip/hr-s2a`) | 12 | B h 14-26 |
| S4 ghost patterns (from `wip/hr-s3`) | 8 | A h 22-30 |
| S1K kit + arena (+ §7's kit) | 11 | B h 26-37 |
| SR item + buff hand files | 6 | A h 30-36 |
| I1 | 6 | h 37-43 |
| R (state + traps ∥ fidelity + fairness, incl. §7) | 2 × 4 | h 43-47 |
| F (rig / kit ∥ core / patterns / reward) | 2 × 3 | h 47-50 |
| S5 balance (fight + item / buff) | 4 | h 50-54 |
| V + release | 3 | h 54-57 |
≈ 96 agent-hours, ≈ 57 h wall. Slot A (S1 → S3 → S4 → SR, 32 h) and slot B (S2a → S2b → S1K, 33 h) are balanced; the
critical path is slot B → I1. S3 / S4 / S2b develop on the D0 stubs (stub rig manifest, empty kit lines, stub arena).

### 9.7 Order of work, worktrees, disk, documents
D0 → (S1 ∥ S2a) → (S3 ∥ S2a → S2b) → (S4 ∥ S2b) → (SR ∥ S1K) → I1 → R → F → S5 → V → release. Each stage works in
`HR/wt_<stage>` on `wip/hr-<stage>` (`cd /home/user/rlk && git worktree add -b wip/hr-<stage> <S:hr/wt_<stage>> wip/hr-d0`;
S3 from `wip/hr-s1`, S4 from `wip/hr-s3`, S2b from `wip/hr-s2a`), commits there with the session trailer, never pushes
(the lead pushes the working branch). At most **two** stage worktrees at once (≈ 260 MB each) plus RP copies only for
S2a / S2b and S1K (`cp -r S:ar/rp_i1 HR/rp_<stage>`, ≈ 48 MB, never hard links), one review / probe datapack snapshot at a
time (≈ 250 MB; R, F, S5) and scratch ≤ 100 MB → peak ≈ 970 MB of the ≈ 2.0 GB free (`df -h /` 11-04). Each loadcheck
re-copies `data/` (≈ 231 MB) into `S:mcsrv` and each suite variant tree copies `mboss/` (≈ 69 MB), so `df -h /` ≥ 800 MB
is required before creating a worktree, an RP copy or a snapshot; remove a worktree and its RP copy right after its
merge, a snapshot right after its use; delete render intermediates and big scratch arrays. S1 tests FN-a/b/c/f with
`spproto` and a local forced `enabled:true` copy. Before the first loadcheck the lead records the user's EULA consent
(§0.1 question 8; README 0-2 2 ②, 0-8).
Shared documents: stages write fragments (`HR/<stage>/readme_*.md`, `HR/<stage>/rp_readme_*.md`); only the lead edits
`R:README.md` and the RP README (§2 font table, §3 generator table, §4 budget lines, §6 version row), at I1 / V. V copies
`HR/{PLAN.md,plan/reward.md,plan/critique_*.md,contract.md,stage_briefs.md,requests,review}` (no `ref/`, no renders) to
`R:tools/dev/sim/hr/`, as README 0-7 lists the precedents' documents.

---------------------------------------------------------------------------------------------------------------------

## 10. Reference sheets (`HR/ref/`, 513 sheets; tiles labelled `vN t fF`; ignore the time labels of `ov_v*.jpg`, ≈ +1.98 s)
- **Overviews**: `ov_v1` … `ov_v5`; the 1-s coverage walk `cr_walk_v1a` … `cr_walk_v5a`; v1 `v1s_half_*`, `v1s_d10_*`;
  v2 `v2f_seg_*`; v3 `v3r_seg_*`; v4 `v4k_seg_*`; v5 `v5e_ov05a/b`.
- **Intro CS0**: `v1s_intro_stairs`, `v1s_intro_02`, `v1s_intro_a/b/c`, `v1s_intro_keys`, `v1s_intro_keys2`, `v1s_intro_rig`,
  `v1s_start_f444`, `v1s_start_zoom`, `mg_v1_hands`, `mg_v1_hands_zoom`, `cr_v1_stance_hand`, `mg_v1_skip_on`, `cr_skip_v1on`.
- **P1**: A1 `cr_v1_a1`, `v1s_a2_*`; A2 / A6 / A5 `cr_v1_a2a6a5`, `v1s_a8_*`, `v1s_a7_*`, `cr_v1_a6`; A3 `cr_v1_a3_leads`,
  `v1s_a12*`, `v1s_combo5`; A4 + A5 `cr_v1_a4`, `v1s_a3_*`, `v1s_a4_*`; A9 `cr_v1_a9_ring`, `cr_v1_a9_ringzoom`, `v1s_a5_*`,
  `v1s_a6_*`; A10 `v1s_a10_*`; the yellow tell `cr_yellow_cmp`, `mg_yellow_cmp`; areas `mg_p1_areas`; the flick `cr_v1_flick`;
  knock-downs `cr_v1_2832`, `v1s_a15_down`; the bark `cr_sub_v1bark_on`; HUD `v1s_hud_*`, `cr_v1_pipfill`.
- **CS1**: `v1s_cs_f2232`, `v1s_cs_keys`, `v2f_cs_*` (0to8, burst, hat, keys1/2, petal, red, skip, slash_1f, wide),
  `cr_v2_petalcut`, `cr_v2_shot78`, `cr_v2_a11`, `mg_v1_skip_cs1`, `mg_skip_ring`, `arena_p2_transform`, `arena_cs1_restage`.
- **SQ1 + A8**: `v2f_a_*`, `v2f_b0_vanish`, `v2f_b1_dash`, `v2f_b*_tick`, `v2f_b_10to13/13to17/17to20`, `v2f_s1_1f` …
  `v2f_s9_dive`, `v2f_s9_ring`, `v2f_t0_*`, `cr_pretell_v2`, `cr_pretell_zoom`, `cr_pretell_hand`, `cr_tell_T0`,
  `cr_a82_windup`, `cr_rings_cmp`, `cr_v2_close_a/b`, `mg_v2_blink`, `mg_pink_glint`, `mg_dark_g_vs_u`, `mg_dark_end`,
  `mg_g_vs_u_light`, HUD `v2f_hud_*`.
- **CS2 / CS3**: `v2f_c1`, `v2f_c2`, `v2f_c_hat`, `v2f_c_hit`, `v2f_c_keys1/2`, `v2f_c_stomp_tick`, `v2f_c_throw`, `v3r_c1`,
  `v3r_c2`, `v3r_c_shots1/2`, `v3r_c_flip`, `v3r_c_mid`, `v3r_c_end_2f`, `cr_counter_cmp`, `mg_counter_cmp`.
- **Down + lead-in**: `v2f_d_*`, `v2f_e_*`, `cr_v2_down`, `v3r_a_*` (down, getup, kipup, kipup_2f, pose, standoff, dim),
  `cr_v3_kipup`, `cr_pretell_v3`, `v3r_hud_shfill_1f`, `v3r_hud_shield`.
- **A13**: `v3r_b0_tell_1f`, `v3r_b1_dash_tick`, `v3r_b_ov1-4`, `v3r_s1_1f` … `v3r_s10_dive_1f`, `v3r_s4_tick`, `v3r_s5_tick`;
  discs `v3r_d1/d2/d3_*`, `v3r_disc1/2/3_*`, `v3r_disc1_eve`, `v3r_v4_halo_2f`, `cr_v3_disc1_gold`, `cr_v3_discs_a/b`,
  `cr_v3_tell_zoom`, `cr_v3_u9`, `cr_v3_end`; darkness `arena_ult_dark`, `arena_ult_end`.
- **CS4**: part A `v3r_e_*` (shots1-4, slash_2f, qte_full, qte_2f, icon, mid, return_tick), `v3r_f1-5`, `cr_v3_qte`;
  part B `v4k_a_t1-5`, `v4k_c*` (clashes, lock, land, orbit), `v4k_s4_*` (rise, sheathe, sword), `v4k_s5_face`, `v4k_s6_*`,
  `v4k_s7*`, `v4k_s8_eve2`, `v4k_s9_*`, `v4k_mouth`, `v4k_streaks`, `cr_v4_land`; part C `v5e_s0_*`, `v5e_s1_*`, `v5e_s2_*`
  (turn, blade, hands, sword, walk, stand), `v5e_s3_*` (hand_2f, tip_3f, peek_6f, keys1-3); the result `v5e_vic_*`,
  `v5e_victory_*`, `v5e_timer_*`, `cr_v5_timer`.
- **Subtitles / UI**: `cr_sub_all`, `mg_subs_all`, `v2f_sub_*`, `v4k_sub_*`, `v5e_sub_read1/2`, `v1s_subs_zoom`, `cr_skip`,
  `mg_skip_ring_v4v5`, `v4k_skip_*`, `v5e_skip_*`.
- **Model** (proportions and states only; §1.5): `model_front`, `model_34side`, `model_back`, `model_scale`, `model_hat_states`,
  `model_ghost`, `model_sword_hilt`, `model_sword_scab`, `model_colors` (the palette NOT to reproduce), `model_hat_top`,
  `model_hat_under`, `model_face`, `model_arms`, `model_waist`, `model_legs`, `model_pendant`, `model_survey_*`.
- **Arena** (mood, sizes and light only; §1.5): `arena_keyframes`, `arena_layout_sketch`, `arena_survey_v1-5`,
  `arena_palette_p1/p2`, `arena_moon_p1`, `arena_moon_first_red`, `arena_p2_transform`, `arena_grass_wind_p2`, `arena_ground*`,
  `arena_particles_p1/p2`, `arena_motes_v5`, `arena_sky_*`, `arena_v1_*`, `arena_v2_bgstrip`, `arena_v3_e8_pan`,
  `arena_v4_air`, `arena_v4_gate_air`, `arena_bg_*`, `arena_entrance_sides`; the glyph sheets `arena_glyph_*` are what NOT
  to build.
- Tools that made them: `HR/tmp/mg_tools/`, `cr_tools/` (re-run `scan.py` / `hudscan.py` / `subscan.py` before
  `events.py` / `verify.py`), `arena_tools/`, `model_tools/`, `v2f_tools/`, `v4k_tools/`, `v5e_tools/`.

---------------------------------------------------------------------------------------------------------------------

## 11. Critique log (11-04)

Two adversarial critiques of the plan (all but §7) and of `HR/plan/reward.md` (§7): `HR/plan/critique_fidelity.md`
(FI-1 … FI-23: 2 blockers, 5 majors, 16 minors) and `HR/plan/critique_feasibility.md` (FE-1 … FE-22: 1 blocker, 7
majors, 14 minors). Every blocker and major was applied; every minor was applied except where a row says otherwise.
Each change was re-checked against the source named in the row (cutscenes.md, critic.md, v1.md, v2.md, patterns.md,
model.md, arena.md, questions.md, w1 / w2, the repository at `35b82e5`).

| id | verdict | what changed / why |
|---|---|---|
| FI-1 | applied (with FI-23's variant) | CS4 ends at **H = 1042** without the fade / hand-off / rig hide; the core starts §7's `seq/event`; `death` 1164; `EV_START`, `END_HANDOFF_T`, `event.py` dropped (§3.7, §7.1.2, §8, §9). Instead of the proposed scabbard tuck (motion the footage does not have), the sheathed sword stays in her right hand as in the footage (model.md §3) and §7.3.2 E0 raises it |
| FI-2 | applied | the north end no longer re-skins the moon gate: a wide pond, one pine (322°), the lotus lantern on an islet (28°), the moon in open sky at 12°, no stair, no south entrance stair (§0, §1.5, §6.2, `test_arena_hr.py`); verified against arena.md §1-§2 (gate, monoliths, the "lit tower"); `seat_rock` moved onto the `start` → moon line |
| FI-3 | applied | the coda's w2 lines are lines 24-25 of `api.LINES` (w2 l.405 / l.298, checked verbatim); §3.0 note, `test_kit` ids 1-25, gate 4; the tooltip (w2 l.411) and ★★★ chat (l.522) named |
| FI-4 | applied | §0.1 keeps the user's 1-4 (buff scope, reward, odds, rift share), adds 5 P2 kit, 6 shield / fails / banner, 7 cutscenes, 8 EULA (FE-18); the camera question dropped (the convention of every boss); references in §0 / §5.1 / §8 renumbered; Q5 now matches §4.4 (same moves, shorter rests) |
| FI-5 | applied | CS1 213 t: line 16 at 144 (footage f211) before the petal cut 154 (f236-f243), negative 161, pink-white 165, slash 169, recolour 173, music 179 (cutscenes.md §3, critic C22-C25) |
| FI-6 | applied | CS4 S5: she walks in to 4.5 b (272-296), swing 296-304, sheathe 304-320 (footage f666-f735 against line 1 at f674); the lines play at 4.5 b; distance test 3.5-6 b |
| FI-7 | applied | `lead_stand {g}` (g = a8 / a13); the how-to banner only in a gauntlet whose fail is lethal (SQ1, lead-ins, restarts); test |
| FI-8 | applied | the petal crosses from her right to her left (cutscenes.md §3 shot 7: image left → right with the camera facing her) |
| FI-9 | applied | a second petal card 1.6 b before the player's eyes carries the cut line (the footage's focus pull, `cr_v2_petalcut.jpg`) |
| FI-10 | applied | `scarlet_line` rises 13° to the player's right in CS1 C8 and in the 5 % instant death (cutscenes.md §3 shot 11) |
| FI-11 | applied in part | `hat worn` at C4 (104, under the black: shot 7 shows her under the brim). Rejected: the hat flying off at the slash and being picked up from the grass — `v2f_a_boss_far_01.jpg` f414-f444 shows the hat behind her shoulders before she lifts it, and the tumbling disc is marked a guess (cutscenes.md §13.8); so the hat swings onto her back at 176 and SQ1 lifts it from there |
| FI-12 | applied | `repel`: `hat back` at 8 (clip event), the clash on the hat on her back, the petal burst only in `repel {at:5}` (cutscenes.md §5 shots 3, 4, 9) |
| FI-13 | applied | §1.3's sentence now says where gold / orange clash bursts and the kick flash appear |
| FI-14 | applied (mechanism changed) | `dark`'s four real slices land 3 t apart (T0 − 17 / − 14 / − 11 / − 8) through empty padding slices in the theme's `look_lines` — the framework's job runner does one slice per tick (`T:build_mboss_arena.py`), so no framework change |
| FI-15 | applied | the lotus knot moved to the back of the hatband; nothing on the brim's top (model.md §2.1 / §5) |
| FI-16 | applied | the tooltip's first lore line is w2 l.633 verbatim instead of our own sentence |
| FI-17 | applied | A9's star at her chest (v1.md B3 "star glint at her") |
| FI-18 | applied | A1 glint and fan `c:2` (magenta), A2 hook `c:1` (purple) (v1.md B1 / B5, patterns.md A1 / A2) |
| FI-19 | applied | SQ1 60 t (footage 55 t); the darkness at T0 − 17 already gives a 44-t tell |
| FI-20 | applied | `INTRO_SKIP` true (questions.md Q-A14's alternative): hold Shift 20 t → black → line 11, the original's 「⊙ 건너뛰기」 verbatim with a control hint; `intro` split into `intro` 554 + `intro_end` 86; test 35; question 7 lets the user turn it off |
| FI-21 | applied | §1.6 lists what is dropped on purpose (w1 l.74 quote and W5-W7 checked) |
| FI-22 | applied | bolts A8 T + 34 / 102 / 161 / 193 (v2 11.42-19.37), A13 T + 70 / 225 / 245 / 258 (v3 f696 / f1124 / f1186 / f1246 on the plan's timeline) |
| FI-23 | applied | as FI-1's variant: one rig state at H (`scabbard hand`) |
| FE-1 | applied (CS4 length per FI-1) | one end-of-fight contract (§7's); CS4 1042 rather than the critique's 1066 (with the fade gone, 1042 is the footage's last beat), so `death` 1164, not 1188; `SEQS += event`, 47 clips, `api.EVENT` / `ITEM_ID` / guarded `ev_apply()` / `ev_title()`, test ids 90-92; ownership S1 framework, S3 `reward.py`, S2a clips + model, S2b `seq/event`, SR hand files; one lines rule; one suite list |
| FE-2 | applied | pips from the dash i-frames at the strike + the feet within `CUT_R` + 3 of the lock point, whatever the dash direction (`F:player/dash_go:4`, `dash_dir:14-27`, `hurt_dodge:4` checked); `#mbDodgeOk` no longer read; four moving dash agents in `pat_ghost.py` and the probe |
| FE-3 | applied | absolute-span `look_lines` (any look from any look, block-exact); `arena_look` is a request retried while `#mbArBuild ≥ 1` (`T:build_mboss_arena.py:371-389`, the refusal in `look/<look>` checked); six transitions + a call during a job tested |
| FE-4 | applied | D0 adds `arenas.hr_field` (stub functions declared); S1 runs first: D0 → (S1 ∥ S2a) → (S3 ∥ S2a → S2b) → (S4 ∥ S2b) → (SR ∥ S1K) → I1 |
| FE-5 | applied | 검신합일 cooldown 2 s (`#hwCtrCdT` 52 / 48 / 44 / 40 t); `HR/plan/calc/ev_cd40.py` re-run: ★★★ +57-65 % / +50-58 % (at the cap = 키리온 +65 / +56 %); S5 gate at the 90th-percentile counter rate |
| FE-6 | applied | FN-f: `#mbBarOff mb` + `mboss_lib.bars(on)` (`F:mboss/world:26`, `bars:3` checked); the bars-hidden CS1 now works |
| FE-7 | applied | §7 rows added; S2 split into S2a (rig) / S2b (cinematics + sequences); SR gets slot A; ≈ 96 agent-h, ≈ 57 h wall; rig ≈ 5 500 functions, 9-12 MB |
| FE-8 | applied | `az/tests_cm/run_all.sh` and `check_refs` / `check_macro` / `check_nbtpath` / `mb/lint_mc` vs `35b82e5` for S1, SR, I1, V; the `ident.py` allow-list written out (§9.5) |
| FE-9 | applied | the item / prop model is `rlk:mboss/scarlet/item_sword` in S2a's RP tree; the def names it (`F:items/build_display:26`) |
| FE-10 | applied | guarded `regen_all.sh` lines, the RP commands in README 0-4, `--skip-rp` for the kit generator |
| FE-11 | applied | the registry carries numbers from D0 (`picks 1`, `lvup 1`, `xp 0`, `death 1164`, music 1 `len 0`); `mboss_lib.py` untouched (`T:mboss_lib.py:131-141` checked) |
| FE-12 | applied | `MOVE_R` 22.5 = safe − 0.5 (`F:mboss/ar/tk_lift/ok:1-2`), a guaranteed fallback point, a test at r 22 |
| FE-13 | applied | the fail-60 push is `mboss_lib.push_ring(2.5, 3)` (`pl_dot` has no knockback) |
| FE-14 | applied | the buff's stat line goes through `update_item_macro` (no item modifier; the pack has none) |
| FE-15 | applied | `api.KIT_SPRITES` itemized (≈ 0.238 M ≤ 0.26 M, asserted by the generator), caps 96 / 48, `afterimage` = one silhouette card, ≤ 4 alive |
| FE-16 | applied | brim squares 0.003 b apart, each painting its own wedges; a close side render |
| FE-17 | applied | `negative` is an approximation (a pale field with a dark rim and band), said in §3.0 and the release note |
| FE-18 | applied | the EULA consent is §0.1 question 8 and gate 1's precondition (README 0-2 2 ②, 0-8 checked) |
| FE-19 | applied | disk peak ≈ 970 MB of 2.0 GB with one probe snapshot at a time; the 800-MB rule covers snapshots |
| FE-20 | applied | `hrfair.py` (from `knfair5.py`) runs on 타키 first; every target is a ratio from that one tool |
| FE-21 | applied | stages write README / RP README fragments; the lead merges them; V copies the plan documents to `tools/dev/sim/hr/` |
| FE-22 | applied | `api.cut()` is a D0 call builder for S4's `g/cut/**`; `evForce` → `ev.force` |

Consistency fixes made in the same pass (no critique id): the look `scabbard gone` for §7's toss; §7's `fl_black` is the
fight's `black` overlay and `vig` the one new glyph (U+EC16; reward.md had called the vignette "the gauntlet's", which the
fight never had); `P2_KIT` added to `api.py` (§0.1 named it), `LETTERBOX` dropped; the sound list cited at its repository
path (all 54 ids re-checked); "north" vs the moon's bearing 12°; §7's "main PLAN" references and `R:` / `H/` notation
mapped to this file's (`README:<n>`, `HR/`); stage names S2a / S2b throughout; CS4's `std` length ≈ 52 s in §0.1.
