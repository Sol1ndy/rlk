# Round V — fixes from the user's first playtest of the rebuilt 홍련 (lead, 11-11)

The 11-11b release (stamp `74f89e3`) was played by the user and recorded. This round fixes what the recordings show.
Lanes: **VC** (cutscene camera), **VB** (the boss: wind-ups, blade path, slash effects), **VP** (the player: perfect
parry / dodge presentation). The lead integrates and releases.

`S` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`.

## 1. The user's words (11-11, verbatim; these are the requirements)
1. 「내 눈에 확실히 띄는 건 각종 투명한 엔티티(아머스탠드, 마네킹, 허스크 등)이 보인다는 거랑 컷신에 시점이 서서히 바뀔 때
   시네마틱처럼 변하는게 아니라 뚝뚝 끊겨 보인다는거, 그리고 관전모드라 좌클릭을 누르면 보고 있는 엔티티를 관전했다가 풀려나는
   모션이 살짝씩 보인다는거.」
2. 「그리고 퍼펙트 패링이랑 닷지 특유의 모션(슬로우 연출, 패링은 검에서 노란 빛, 닷지는 배면뛰기 비슷한 모션)이 없고 타이틀에
   네모 박스가 뜨는데 왠지는 모르겠다는 거.」
3. 「그리고 보스 공격의 선동작이 안 보여서 패링 타이밍 맞추기가 너무 어렵다는거. -> 위에서 내려치기로 벤다고 하면 위로 향하는
   동작을 크게 하든지 검 끝의 경로를 눈에 띄게 레이저포인트 쏘듯이 표시하든지 해야될듯」
4. 「검으로 벨 때 나타나는 이펙트(검기, 초승달 모양 이펙트)가 검의 방향이랑 어긋나 있는것도 고쳐야 해」
5. 「닷지랑 패링 모션도 드라이브에서 봐. 파일이름은 닷지 시연.mp4와 패링 시연.mp4야.」 (reference recordings of the
   original game's perfect parry / perfect dodge)
6. 「홍련 테스트 2.mp4 파일을 보면 관전모드라 공중에서 날아다닐 수 있는 버그, shift 누르면 시점이 매우 빨리 흔들리는 버그,
   처음 컷신에서 스킵을 했을 때 홍련이 저 멀리 뒤에 있다가 시작하면 tp하는 버그, 관전 상태에서 좌클릭 누르면 시점이 순간적으로
   바뀌는 버그 등이 있어. 수정해줘」

## 2. Evidence (read your part before designing)
- Recordings (scratch, not in git): `$S/cb/video2/t1.mp4` (first playtest, 294 s), `t2.mp4` (second, the provoked
  bugs), `parry.mp4`, `dodge.mp4` (the reference). 60 fps, 1080p. Overview sheets in `$S/cb/video2/ov*/`.
- `review/v/findings_fight.json` + `review/v/img/*` — the combat review of t1 (16 findings, measured).
- `review/v/findings_cine.json` — the cutscene review of t1 and t2 (28 findings, measured; ids `T1-…`, `T2-…`).
  Evidence images beyond the copies in `review/v/img/` are in `$S/cb/video2/rev_fight/` and `rev_cine/`.
- **`review/v/client_facts.md` — how the 26.3 client and server really behave (camera, spectating, interpolation,
  packets, fonts, HUD order, slow motion), read from the real bytecode. Each statement is marked VERIFIED or INFERRED.
  This replaces the guesses the 11-11 build was made on. Read it before touching anything it covers.**
- The reference analysis (parry / dodge demo): `$S/cb/video2/ref_pd/` and `review/v/ref_pd.md` once the lead adds it
  (lane VP's spec).
- You can check more client / server behaviour yourself, and should before relying on anything unverified:
  the client jar is `$S/mcclient/client.jar` (official names), the server jar `$S/mcjar/server.jar`; disassemble with
  the JDK's own `$S/jdk/jdk-25.0.5+8/bin/javap -c -p -cp <jar> <class>`. **Do not download or run a third-party
  decompiler or any other external code** (blocked here). Nobody can run the game client here: the user is the only
  in-game test, so every client-side assumption you could not verify goes into your report's "only a person can
  check" list, with what to look for.

### What the recordings established (summary)
- **Tofu box**: 16 times in t1, on every tier-3 and tier-2 parry, a hollow box at the title's place; the gold streak
  never drew. Cause (verified): `rlk:cb` glyphs `streak.png` / `streak_s.png` are 512 × 288; the client's glyph atlas
  is 256 × 256 and a larger source cell becomes the missing glyph (`glint.png` 320 × 64 has the same fault).
- **Tier 2 looks like a perfect parry** (same box / flash / star, a few frames shorter): the player cannot tell why a
  gauntlet shield segment did not break. No hit-stop, no slow motion, nothing on the weapon; on a perfect dodge the
  avatar only leans / slides.
- **Wind-ups unreadable**: between cue and hit her silhouette barely changes (a pose change could be named in ~4 of 18
  attacks); the blade is a 2-3 px line; the cue star sits on her white hat over pale grass in P1 and was on screen in
  2 of 8 gauntlet cuts; the only dependable tell was the cue sound 0.37 s before the hit. Leaps (A10, A4) take her
  off screen for 27-30 frames with no tell in frame. The player's own effects (flames, smoke, big damage numbers)
  cover her during cues.
- **Slash effects**: her lilac crescents stand 1.5-4 blocks to one side as tall near-vertical arcs, start on the hit
  frame and keep sweeping 0.4-0.6 s after the blade stopped; 45-90° off the blade where both could be seen.
- **Camera**: slow rotations step (one 1.4° nudge about once a second); 30 of 55 cuts arrive sliding for 2-6 frames
  (three frames inside her body at 17.9 s); translucent ghosts of her hit-box husk (up to 60 % of the frame), of an
  armor stand and of two tall slabs at the arrival; in t2: 37 left-click view jumps, the Shift shake (75-380 px every
  frame while Shift — the skip key — is held), 27 ticks of free flight (6.60-7.97 s), and after the CS0 skip a low
  camera on empty ground with her far away, effects playing where she should stand, and her popping in 0.7 s after
  control returned.
- **HUD in cutscenes**: the crosshair, the sidebar (스택 / 붉은 죽음의 가면), a loot toast, "Press Left Shift to
  Dismount" at each hand-back. **Dialogue lines**: 18-px glyphs, no backdrop, just under screen centre, across her
  face or chest in close shots. **Staging**: the petal is a 690 × 640 px blob over her face for a whole line in CS1;
  an empty shot at 49.9-50.9 s; she is a 40-px speck in the leap shot 63.4-64.9 s.

## 3. Lead rulings

### VC — the cutscene camera and the cutscenes
Keep spectator + `spectate` (the adventure-mode alternative is worse: client_facts §5). Change the rest:
1. **Camera entities = empty `item_display`s** (no item: nothing is drawn, no ghost), not armor stands. Rotation
   reaches the client as bytes (1.40625°, floored) unless a float position-sync packet is forced, so:
   - a shot is a list of **keyframes**; between keyframes the client interpolates (`teleport_duration` = the segment
     length, ≤ 59, set a tick ahead of the `tp` — client_facts §2): one `tp` per segment, not one per tick;
   - **every keyframe's yaw and pitch lie on the 1.40625° grid** (so the floored value is exact and position and
     rotation agree even if nothing else works); a slow pan is then one or a few long linear segments. Also apply
     the OnGround flip (client_facts §2) so the client gets floats where it works — but nothing may depend on it;
   - per-tick re-aiming at a moving subject only where the subject moves fast; no per-tick re-aim on slow shots
     (the I15 jitter).
2. **Third person**: the game is played in F5 (back); a non-living camera entity is then seen from **4 blocks behind
   it along its view direction** (constant, block-clipped: client_facts §1). Place the entity at `V + 4·forward` for
   the intended viewpoint `V`; a build-time check proves for every keyframe that the entity is in air and the 4-block
   segment back to `V` crosses no solid block (the arena's blocks are known to the tools) — re-aim shots that fail.
   First person and F5-front are not supported during cutscenes (say so in the README); the eye-height glide and the
   FOV ease at the first and last cut (client_facts §1, §8) stay under the black / white masks.
3. **Cuts** switch between cameras that have **settled**: the idle camera is snapped (duration 0, set a tick ahead)
   to the next shot's first keyframe early enough that the client has finished with it; use a third camera if two
   cannot always be settled in time. Zero frames of sliding, and never a frame inside a model.
4. **Left-click**: while locked, the player's entity and block interaction ranges are 0 (an attribute modifier that
   forces the total to 0, removed at release — do not overwrite the base the game uses elsewhere).
5. **Shift** ends spectating server-side and cannot be vetoed. So: **the skip moves off Shift** — hold **Space**
   (the jump input; confirm in the bytecode that input packets are still sent while spectating an entity, else pick
   another input that does not end spectating) with the hint text changed to match; and while Shift is held anyway
   the picture must stay as close to the shot as the client allows (the player teleported so that their own
   third-person camera coincides with the shot, rotation included, their `camera_distance` handled) — measure what
   remains and report it. Target: no jumping picture.
6. **Free flight**: find why the hold lost the camera for 27 ticks in t2 (candidates: client_facts §8 — a camera
   entity the client did not have yet makes `spectate` a silent no-op on the server side afterwards; a release by
   click / Shift not re-attached) and make the hold robust: whenever the player is not on the live camera, re-attach
   in a way that really re-sends the camera. The player must never be a free spectator during a locked sequence.
7. **Ghosts**: no living entity may be visible as a ghost during a locked sequence — her hit-box husk, any armor
   stand (stage markers, seats, anchors), the slabs at the arrival (identify them), anything else living. Per kind,
   in this order of preference: make it non-living; or keep it out of every shot's view for the lock (moved away and
   brought back at the hand-back, if the frame logic allows); or, if that entity type is never meant to be seen
   anywhere in this pack (audit it), a fully transparent vanilla texture in the resource pack, written by a generator
   in git. Fix the arrival too (t1 2.4-3.3 s).
8. **The CS0 skip** (and the CS1 skip): the skip lands in exactly the state the unskipped sequence has at that tick —
   her place, pose, hat, props, the actor, the camera, the stage — with nothing playing in an empty place and no pop
   afterwards. No line may be drawn over the black. Add a test that compares the two states.
9. **HUD**: during a locked sequence nothing of the fight HUD shows — the pack's crosshair, the sidebar, toasts; and no
   "Press … to Dismount" at the hand-back (overwrite the action bar in the same tick). The boss bar stays as designed.
10. **Dialogue lines**: readable at a glance — lower third of the screen, glyphs ≥ 28 px at 1080p / GUI scale 2, on a
    dark backdrop, never across her face; the skip hint legible too (≥ 16 px, backdrop). A `text_display` with a
    background, riding or following the camera entity (it is on the view axis 4 blocks ahead of the eye in F5),
    is the suggested way — verify the transform / billboard order and `see_through` in the bytecode; keep the lines
    verbatim.
11. **Staging**: the petal never covers her face during a line and is petal-sized; no empty shot under a line
    (49.9-50.9 s); the leap shot shows her larger than 40 px; anything else in `findings_cine.json` of severity
    high or medium.

Owner of: the camera / lock / hold / skip-input parts of `tools/build_mboss_core.py` and `tools/mboss_lib.py`,
`tools/mboss_scarlet/{seq,cam}.py`, `tools/scarlet_cine.mjs`, the actor (`tools/player_motion/cine/**`,
`tools/build_player_cine.mjs`) where staging needs it, the line / hint drawing, the blank-texture generator.

### VB — the boss in the fight
Hit ticks, damage, shapes and the pick weights do not change (the balance pass stands); what the player sees changes.
1. **Wind-ups you can read**: every hit (parryable or not) is preceded by an anticipation the player can name — the
   blade drawn clearly away from the coming cut (high for a downward cut, back and wide for a sweep), reached ≥ 10
   ticks before the hit for single / first hits (≥ 6 for chain follow-ups) and held; her silhouette must differ from
   idle at the fight camera's distance and angle (4-10 blocks, from behind and above the avatar). Rework the fight
   clips (`tools/scarlet_clips.mjs`) and the gauntlet poses to that end. The blade itself must read at that distance:
   a bright edge / glow so it is ≥ 6 px wide at 1080p from 6 blocks.
2. **The blade path, drawn** (the user's "레이저포인트"): from the wind-up to the hit, the path the blade tip will travel
   is shown in the air as a bright line / arc — derived at build time from the clip's own blade track, so it is always
   where the cut goes — at least 0.12 block thick, visible ≥ 10 ticks before single / first hits (≥ 6 for chain
   follow-ups), and showing **when** as well as where (e.g. a bright head running along the path that arrives exactly
   on the hit tick). Colour: white-gold for parryable hits, the flash colour (yellow / purple / blue) for unparriable
   ones. In the air at blade height — not a floor decal. It supplements the cue star and the chest flashes; those stay
   but must be visible: the star against both fields and not on her white hat, the chest flashes large enough to see
   past the avatar.
3. **Slash effects follow the blade**: every crescent / arc / streak is generated from the same blade track — same
   plane, same direction of travel, at the blade's reach, starting with the swing and gone within ~6 ticks of the hit.
   No effect on the side she is not cutting.
4. **Off-screen attacks**: in A10 / A4 and the gauntlet arrivals the tell must be in the player's view for ≥ 12 ticks
   before the hit (keep her in frame — lower / shorter leaps, arrivals in front of the avatar — and / or a tall
   in-air tell at the target that cannot be missed; no floor decals). Nothing may hit from an empty screen (the G1
   plunge at 162.5-163.4 s). Do not let her land on or dash to within 1.2 blocks of the player's position (the camera
   ends up inside her), and fix the light-column card that fills the screen at 163.4 s.
5. **The 5-segment gauge** shows its segments (dividers).
6. Re-run the balance suites after the change (they must still pass: hit ticks did not move).

Owner of: `tools/mboss_scarlet/{api,ai,p1,p_ghost,core,shield,s3lib}.py`, `tools/scarlet_clips.mjs`,
`tools/build_mboss_hr_fx.py`, the gauge drawing.

### VP — the player's perfect parry and perfect dodge
1. **The box**: every `rlk:cb` bitmap cell ≤ 256 × 256 (streak, streak_s, glint); `tools/dev/rplint.py` learns the
   rule (a font bitmap whose cell exceeds 256 px in either direction, or `ascent > height`, is a problem) so it
   cannot come back, in any font.
2. **Tiers look different**: only the perfect parry gets the big presentation. Tier 2 / tier 1 get a clearly smaller,
   differently coloured block effect and a different sound, so a player reads "blocked, not perfect" at once.
3. **Perfect parry** and **perfect dodge** follow the reference (`review/v/ref_pd.md`): the slow-motion beat, the
   yellow light on the weapon for the parry, the back-flip-like evasive motion for the dodge, the camera / screen
   effects and sounds (vanilla sounds only), for every playable character and weapon (find out how each character's
   avatar is drawn; all must get the motion).
   - **Slow motion**: `tick rate` cannot be used (client_facts §6: a function containing `tick …` does not load in
     single player). Build the beat inside the game: the attacker's clock (mid-boss core patterns and rigs; the
     custom mobs' frame) and the avatar's motion run frozen / at a fraction for the beat with display interpolation
     stretched to match, then resume — timing from the reference, total length short enough that it never eats the
     next input window (the next chain hit must still be answerable: check against chain gaps ≥ 10 t). It applies to
     every enemy, not only 홍련. The parry / dodge windows, cooldowns and the gauntlet timings must behave exactly as
     before in un-slowed terms — say how the beat interacts with them, and prove it with the existing suites.
4. Keep what works (the gold star at the contact, the red wash). In P2 the red wash / red outline vanish against the
   crimson field: make the dodge effect read there too.

Owner of: `tools/build_combat_fx.py`, `data/rlk/function/player/def/**`, `tools/build_player_rig.mjs` and
`tools/player_motion/**` except `cine/`, `tools/dev/rplint.py`, and one clearly delimited "beat" section in
`tools/build_mboss_core.py` / the mob frame.

## 4. Common rules for the three lanes
`h_common.md` applies as written (setup, the user's rules, the resource-pack rules, gates, saving, housekeeping, the
final report), with these differences:
- Base branch `origin/wip/v`; your branch `wip/v-<lane>` (`cam`, `boss`, `player`), worktree `$S/cb/wt_v<c|b|p>`,
  progress file `v<c|b|p>_progress.md`. Pack copy: `cp -r $S/rp_fin $S/rp_v<c|b|p>` (`rp_fin` = the 11-11b release pack).
- The contract is this file; `hr_design.md` still describes everything this file does not change. Where they
  disagree this file wins — and update `hr_design.md` / the README's 홍련 section and section 3 for what you change.
- Commit trailer (exactly, and no model name anywhere else):
  ```
  Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_019wi9c7roqDDkFi2TvFWw6G
  ```
- Look at your own work: render sheets (the drawing tools in README 0-8) of every clip, shot, path and effect you
  change, from the **fight camera's** real distance and angle for combat things, and check them against the user's
  words in §1 before you call it done.
- Another lane's file: do not edit it (the stand-in exception in `h_common.md` holds). The three lanes all regenerate
  shared outputs; the lead regenerates at the merge, so conflicts in generated files are not yours to resolve.
- Do not push to the release branch or to `wip/v`.
