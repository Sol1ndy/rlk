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

### WB — the boss in the fight (owner as lane VB)
The user, 11-12, after seeing the round V blade path in play (verbatim): 「보스의 검로가 보이는건 미리 경로를 보여주라는게 아니라
공격이 좀 더 잘 보이도록 이미 지나온 경로를 표시하라는 거야」 — the lead misread the round V request: the path was never meant
to be shown ahead of the cut. Ruling:
1. **Remove every path shown ahead of the blade**: the pre-drawn swing paths and their running heads, the straight target
   lines of dashes / plunges, the tall mark over a dash's locked spot, kcut's / nb's pre-drawn lines, the gauntlet
   stations' standing paths. Nothing may show where the blade is going to go. (The cue star, the colour flashes and the
   wind-up poses are the telegraph and stay as they are.)
2. **A trail of where the blade has been**: from the first tick of the wind-up to the end of the follow-through the
   blade leaves a bright ribbon behind it — the surface its edge has swept in the last ticks, generated from the
   clip's own blade track (`tools/scarlet_blade_track.json`), brightest at the blade and fading out over ~6-8 ticks —
   so the raise, the hold and the cut can all be followed by eye at the fight camera's distance (the round V size
   rules hold: ≥ 0.12 b wide where it is narrowest, readable on both fields). During a dash or a plunge the trail is
   behind her / her blade along the way she has come. The hit-tick slash generated from the same track (round V) is
   the trail's brightest moment — one coherent effect, not two stacked ones. Colour: keep white-gold for parryable
   hits and the flash colour for unparriable ones unless it reads worse than one colour.
3. The trail follows the pattern clock (frozen / slowed with her during the beat, as the round V cards do).
4. Hit ticks, damage, shapes, weights, the wind-up clips, the blade edge, the cue star, the flashes, leaps, dash stops
   and gauntlet stations of round V stay. Re-run the balance suites.
5. Every high / medium finding of the fight review in your area.

## 3. Common
Base branch `origin/wip/w`; branches `wip/w-cam`, `wip/w-player`, `wip/w-boss`; worktrees `$S/cb/wt_w<c|p|b>`; pack
copies `cp -r $S/rp_rel3 $S/rp_w<c|p|b>` (`rp_rel3` = the 11-12 release pack); progress files `w<c|p|b>_progress.md`.
Gates, rules, saving and the final report as in `h_common.md` / `v_brief.md` §4 (the Fable 5.2 trailer). Nobody can
run the client here: verify in the bytecode what you can, render and look at what you build, and list what only the
user can check.

## 4. Addendum (11-12, the user's fourth recording `$S/cb/video3/t4.mp4`, overview `$S/cb/video3/ov4/`)
The user's words (verbatim):
7. 「네번째 테스트 영상도 올렸어. 이건 세번째 컷신을 수정하기 위함이야. 일단 두 아바타의 몸이 너무 겹쳐. 칼싸움중인데 진짜 몸으로
   대화를하는 느낌이야. 그리고 공중전투가 너무 밋밋해. 뭔 추진기를 달아놨나 아무리 연출이라고 해도 공중에 너무 오래 체류하는걸
   적나라하게 보여줘서 어색해 보여. 차라리 얼굴-복부 사이를 클로즈업해서 칼을 맞대며 스파크가 튀는 연출이 괜찮을 것 같아.」
8. 「그리고 대사가 홍련 오른쪽 위에 작고 멀리 표시될 때가 있는데 확인해서 수정해줘」
9. 「말을 확실하게 안 한 것 같은데, 기존의 '대쉬'는 없어지는거야. 스텔라블레이드의 닷지로 완전히 전환해야 해.」

In t4: gauntlet 2 from ≈ 38 s, the repel cutscene ≈ 50–56 s, the ending from ≈ 57 s (blade locks ≈ 59–60 s and
≈ 66 s with the two bodies pressed together; the aerial duel ≈ 67–75 s seen from far below; lines from ≈ 78 s).

### WC, added (the "third cutscene" = the repel and the ending's duel)
5. **Bodies apart**: in every blade lock, clash and exchange of the repel, CS1 and the ending the two figures keep a
   swordfighter's distance — the blades meet between them, torsos never overlap or touch on screen, no limb of one
   inside the other's silhouette (except the scripted grab / throw / kick contacts, which must read as such). Add a
   build-time check on the two rigs' body boxes (a minimum gap between torsos during every lock / clash span) next to
   the existing contact checks, and frame the shots so the gap is visible.
6. **The aerial duel goes.** No long hovering in mid-air, no wide shot of two figures floating. Replace the aerial part
   of the ending with what the user asks for: **close shots between face and abdomen** of the blades meeting — a fast
   exchange of clashes with **sparks flying at each contact** (bright spark bursts at the blades' crossing point, a
   flash, vanilla sounds), cut quickly between a few close angles (her side, the actor's side, the crossed blades),
   feet on the ground or out of frame; any leap is short and seen only as launch or landing. Keep the ending's story
   beats, lines (verbatim, same order) and its end state; the sequence's length may change — update every dependent
   number (registry `death`, tests).
7. **The stray dialogue text** (item 8): sometimes a line shows small and far away at her upper right instead of in
   the lower-third box. Find it in t3 / t4, find the cause (candidates: the line's text display not riding the live
   camera after a cut or a camera remake — e.g. after a skip, a re-attach, or on the idle camera; a display left at a
   stage position; the pre-round-V line path still firing in some sequence or in the lead-ins / fight lines), and fix
   the class of bug, with a test that every line shown during a lock is on the live camera's text displays and that
   no other line-text entity exists in the world at that tick. Lines spoken outside a lock (in the fight) must have
   a deliberate, readable place as well.

### WP, changed (item 9 replaces ruling WP-3)
3. **The dash is gone; the dodge is the reference game's dodge, completely.** Measure the reference (`dodge.mp4`: the
   plain dodge, the double dodge = a second press chaining a second evasive move, the perfect dodge) and build exactly
   that set: a plain dodge is a short, quick evasive step with its i-frames (travel, duration, pose and direction rule
   from the reference — the user describes it as "just shifting slightly on the spot", not a dash), a second press
   within the reference's window chains the second move, and the perfect dodge is the (now faster) beat. Nothing of
   the old long dash remains — not as a fallback, not on a modifier. Re-derive cooldowns and i-frame windows so the
   dodge is as good an answer to attacks as before (the perfect window and the tiers of the looser windows against
   normal mobs stay as the user decided on 11-10), and adapt everything that was built on the dash as movement
   (engravings / items that changed dash distance, cooldown or charges such as 질주; room traversal; boss patterns
   whose fairness assumed dash travel — check the balance sims' dodging agents) — list each and what became of it.

## 5. Commit trailer from 11-12 03:40 KST (the session's model changed; this replaces v_brief §4's trailer for round W)
```
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019wi9c7roqDDkFi2TvFWw6G
```
Commits made before this point keep the trailer they have.

## 6. Addendum (11-12 04:05 KST): the parry whiff ladder goes
The user asked whether the original game lengthens the parry cooldown when F is mashed; it does not (the escalating
lock was the round-A review's addition, `rulings_A.md` A-01 (2)). The user: 「없애」 ("remove it").
**WP**: remove the whiff streak entirely — every F press locks for the base `#parGap` (12 t) and nothing else; no
streak counter, no `#parWsT` / `#parWsClr` behaviour, no growing lock. Keep the base lock and the rule that an ignored
press during the lock does not re-arm early (A-01 (1)), so mashing faster than the gap still never gets a press in.
Update test_cb, README 3 and `c_progress` / `fa_progress` notes. Then re-check what the ladder was guarding: the
gauntlet metronome search (`test_metro`: G1 / G2 must stay uncleared by any fixed-period masher) and the balance
agents (hrfair T7: sloppy ≤ 35 %, masher / dodger 0 % clears; T6 / T13) — report the numbers; if a masher can now
clear a gauntlet, say so with the period that does it and do not fix it by bringing the ladder back (the lead decides).
