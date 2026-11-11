# Round W — the user's second playtest (of the 11-12 build), lead, 11-12

The 11-12 release (round V, stamp `6b02e54`) was played and recorded: `$S/cb/video3/t3.mp4` (60 fps, 1080p; the
user plays 아를레키노 at **FOV 90**; overview sheets `$S/cb/video3/ov/`). `S` =
`/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`. `v_brief.md` (round V) and
`h_common.md` still apply to everything this file does not change; the reference analysis is `review/v/ref_pd.md`
(recordings `$S/cb/video2/parry.mp4`, `dodge.mp4`), the client facts `review/v/client_facts.md`.

## 1. The user's words (11-12, verbatim; these are the requirements)
1. 「두번째 컷신의 술 마시는 모션이 좀 이상해.」
2. 「그리고 페이즈 전환할 때 꽃잎을 가르는 연출이 있는데 그 꽃잎이 너무 작고 내려오는걸 벤다는 느낌이 아니라 공중에 떠있는걸 베는
   느낌이야.」
3. 「그리고 위에서 내려다보는 시점이 있는데 두 아바타가 다 안 나와.(fov 90 기준)」
4. 「패링 단계 전체적으로 효과음이 좀 부실해.」
5. 「퍼펙트 닷지의 모션이 너무 느려. 그리고 닷지를 공격받지 않는 상황에서 쓰면 대쉬가 나가는게 아니라 그냥 제자리에서 살짝 앞으로
   가는 느낌이어야 해. 이건 닷지 시연 영상을 참고해.」
6. 「나머지 사항은 영상 보고 판단해. 홍련 테스트 3 영상을 올렸어.」

## 2. Lanes and rulings
Findings of the two reviews of t3 arrive as `review/w/findings_cine.json` / `findings_fight.json` (the lead forwards
them); every high / medium finding in your area is yours as well as the user's points.

### WC — cutscenes (owner as lane VC in v_brief §3, plus her cinematic clips and the actor)
1. **The drinking motion** (item 1; the intro's bottle / cup shots — and wherever else she drinks): look at it in the
   recording and in rendered sheets, name what is wrong (the arm path, the cup / bottle's tilt and its place at the
   mouth, the head, timing, the prop in the hand, the pour), and rebuild it so that it reads as a person drinking:
   reach → lift to the lips with the cup level → tilt the cup and the head back together → hold → lower. The prop
   stays in the hand, upright until tilted, its rim at her mouth.
2. **The petal cut at the phase change** (item 2): the petal must be seen **falling** — it enters the frame from above
   and drifts down with a visible sway for at least ~1.5 s before the cut, is still moving down at the cut, and the
   two halves keep falling apart after it. Large enough to read as a petal at once (aim: ≥ 60 px tall at 1080p at the
   moment of the cut, never covering her face during a line). The cut meets it on its way down; her blade passes
   where the petal is on that tick.
3. **The top-down shot** (item 3): both figures fully in frame with margin **at every FOV from 70 to 110** (the user
   plays at 90). Add the check to the shot tests for every shot that is meant to show two figures: both inside the
   frame at FOV 70, 90 and 110 (16:9), not under the dialogue box.
4. FOV in general: re-check the text sizes and every shot's framing at FOV 90 as the primary case (70 and 110 as
   bounds).

### WP — the player (owner as lane VP in v_brief §3)
1. **Parry sounds, every tier** (item 4): the tier-1 / tier-2 block and the perfect parry sound thin. Analyse the
   reference's sound (`parry.mp4` audio: the normal guard's "tink" and the perfect parry's clang + bright ring ~0.75 s
   + the swing whoosh before it) and the recording's (t3), then build layered vanilla-sound stacks with weight: for
   the perfect parry a heavy metallic impact with a low body, a bright ringing tail, and a sub "boom" under the
   freeze; for tier 2 / 1 a solid, clearly metallic clash (not a tick) with a short ring, tier 1 lighter than tier 2,
   all three clearly different in weight. Check loudness against the fight's other sounds (her cue, her swings, the
   player's own attack sounds) so the parry is the loudest event of its moment. Vanilla sounds only.
2. **The perfect dodge is too slow** (item 5): the whole thing reads slow in play. Shorten it: the slow-motion beat
   and the flip together must feel snappy — propose and build a faster timing (starting point: slow motion ≤ 5 world
   ticks at ×1/2, the handspring ≤ 8 ticks, the avatar back in the ready stance within ~14 ticks of the trigger) and
   make the flip itself read fast (larger steps per tick, a clear launch and landing). Keep the beat's contract
   (clocks, untouchable, tests) — only its numbers change.
3. **A dodge with nothing to dodge** (item 5): today it is the full dash. It must be a **short in-place evasive step
   — a small shift forward**, as the reference's plain dodge (measure it in `dodge.mp4`: travel in body heights,
   length in frames, the pose). The full dash distance only when an attack is actually avoided? — no: read the
   reference and decide from it what a plain dodge's travel is in all cases, then say in the README what the dodge
   now does (travel, i-frames, cooldown). Do not weaken the dodge as an answer to attacks: the i-frame windows and
   the cooldowns stay.

### WB — the boss in the fight (owner as lane VB), only if the fight review finds high / medium defects there.

## 3. Common
Base branch `origin/wip/w`; branches `wip/w-cam`, `wip/w-player`, `wip/w-boss`; worktrees `$S/cb/wt_w<c|p|b>`; pack
copies `cp -r $S/rp_rel3 $S/rp_w<c|p|b>` (`rp_rel3` = the 11-12 release pack); progress files `w<c|p|b>_progress.md`.
Gates, rules, saving and the final report as in `h_common.md` / `v_brief.md` §4 (the Fable 5.2 trailer). Nobody can
run the client here: verify in the bytecode what you can, render and look at what you build, and list what only the
user can check.
