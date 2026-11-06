# 홍련 — review findings (HR-xx)

Source: R-early (D1, D2, D7) on snap_i1a = 66dafec; every finding re-checked by an independent verifier (all confirmed).
R-late (D3, D4, D5, D6, D2 kit / arena) will append HR-12.. on the I1b + S2c head. F fixes at the source (generators).

| HR | dim id | sev | area | title |
|---|---|---|---|---|
| HR-01 | D1-01 | major | core | A pause or /reload between the A8 judge (fail) and T+214 replays the whole A8 instead of going to P2 |
| HR-02 | D2-01 | major | seq | CS4's one-shot facing teleports the player's avatar to the camera: it pops ~2 b up (default F5 view) or jumps ~3.4 b back (shoulder view) at the start of the ending |
| HR-03 | D7-01 | major | items | 화무십일홍's inventory / codex icon is a sub-pixel hairline (0.38 GUI px wide): a dotted diagonal line in the slot |
| HR-04 | D1-02 | minor | core | The counter (A1/A2) and skill (A6) triggers run before the reserved floor step, so CS1 / the A13 lead-in waits for one more attack |
| HR-05 | D1-03 | minor | core | cleanup leaves the pattern / ghost / sequence fake players in objective hr and storage rlk:hr seq.g after every fight |
| HR-06 | D1-04 | minor | tests | Module test hooks leave the fight in dead states: test 30/35 outside P1/P2 freezes the phase; tests 23/29 make every later gauntlet of the fight unwinnable |
| HR-07 | D1-05 | minor | core | The A13 instant death can be dodged by leaving: a disconnect or save & quit before T+258 restarts A13 with 5/5 |
| HR-08 | D2-02 | minor | items | 홍련일섬's screen-edge vignette is gated on vBig, which never counts down outside the F5 view: it never shows in shoulder view or first person (sr-2, deferred to R) |
| HR-09 | D7-02 | minor | items | 검신합일 fires on any dashInvT, so a downed Ronova (and burst / fall invulnerability) counter-slashes mobs |
| HR-10 | D7-03 | minor | items | The sword's cooldowns survive the run reset: a stray '홍련일섬 ready' click at the next grant, or a swallowed first burst |
| HR-11 | D7-04 | minor | buff | The 'forever' buff scope (question 1) is not one switch: buff_scope is read by no generator, the rift chat keeps '이번 런 · +20/10/10' |

## Details (fix as proposed unless a lead decision below says otherwise)

### HR-01 (D1-01, major, core) A pause or /reload between the A8 judge (fail) and T+214 replays the whole A8 instead of going to P2
- where: data/rlk/function/boss/scarlet/core/g/pause.mcfunction:2-4, resume.mcfunction:2-5, core/re/g.mcfunction:2-6 (generator tools/mboss_scarlet/core.py w('core/g/pause') l.613, resume l.598-612, w('core/re/g') l.691)
- fix: tools/mboss_scarlet/core.py w('core/g/pause'): when not api.ULT60_LETHAL add `execute if score #gres hr matches 2 if score #gk hr matches 1 run scoreboard players set #grs hr 4`; in resume and core/re/g add `execute if score #grs hr matches 4 run function rlk:boss/scarlet/core/p2/from_fail` (with ULT60_LETHAL true the A8 fail is the fatal and today's restart after a revive stays). test_scarlet R9 / R11: a pause and a /reload at T+195..214 after the fail -> P2 at once, no second A8.
- verifier: Kept major. PLAN 3.8 / 5.6's literal row (A8 cancelled -> restart) was written for an unfinished gauntlet. The module itself sends the two other post-judge windows to their judged outcome (core.py pause comment; S3 notes_s4_s2b.md section 6: #grs 3 -> repel, #grs 2 -> the revive stance), so the non-lethal A8 fail is the one window left out. One failed judge can then cost two 500 per-mille hits, or give a second try at the deflect: a wrong flow the player sees. It is not a blocker: no softlock, P2 follows the second A8, the reward is unaffected. The trigger is narrow: /reload, or a multiplayer disconnect inside the 20 t after the fail. Selection screens refuse while #active/#combat (lvup/toggle:4, invd/open:6, codex/open:7). The fail hit cannot kill (pl_dot2:11-14 caps it at curHealth - 1 with #mbDotLethal 0). Correction: the 'singleplayer save & quit + reopen' route is not verified. In 2

### HR-02 (D2-01, major, seq) CS4's one-shot facing teleports the player's avatar to the camera: it pops ~2 b up (default F5 view) or jumps ~3.4 b back (shoulder view) at the start of the ending
- where: F:boss/scarlet/seq/ending/start.mcfunction:4-5 (generator T:mboss_scarlet/seq.py:145-148 face_player_dying(); design text PLAN §3.7 'One-shot facing at 0 (tp … facing + view/sync)')
- fix: T:mboss_scarlet/seq.py face_player_dying(): emit only `execute as @a[tag=player,limit=1] run rotate @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] eyes` (the pull/finish idiom; works while dying), no tp and no view/sync; regenerate; correct PLAN §3.7's sentence; drop the accepted lint line; add a static check (ev_dry or test_scarlet) that seq/ending/start neither tps the player nor calls rlk:view/sync.
- verifier: Kept major: in the default view every clear begins with the player's character popping about 2.3 b up and dropping back over about 9 t, with the camera bobbing, during E1's static beat. That is wrong behaviour a player will notice (a visible effect defect). Corrections to the numbers: the default hop is about 2.26 b (2.0-2.75 b), not about 2.0 b, because the Small armor stand is 0.9875 b tall before ride.s, not 0.49 b; the fall takes about 9 t, not about 7 t. The shoulder view can only be reached by command (/function rlk:view/mode {m:1}; the lobby has no such choice and every load resets #vmode to 2), so F5 is the real case. First person is not affected (view/sync returns 0 without rlk_av). Probably also, not verified (client side): during the one dismounted tick the F5 camera falls back to the player's own camera_distance 0 (view/spawn:27), a 1-tick camera snap. Fix additions: also cor

### HR-03 (D7-01, major, items) 화무십일홍's inventory / codex icon is a sub-pixel hairline (0.38 GUI px wide): a dotted diagonal line in the slot
- where: RP:models/item/mboss/scarlet/item_sword.json (display.gui scale 0.9) + RP:items/mboss/scarlet/item_sword.json, generated by T:scarlet_geometry.mjs:323-342 itemSword() (scabbard box +-0.02 b, MODEL_SCALE 1.5) and T:build_scarlet_rig.mjs:78-88 ITEM_DISPLAY.gui; shown through F:items/mythic/sword_hwamu
- fix: In the rig generator's item_sword writer (T:build_scarlet_rig.mjs, S2a/S2c, the shape S2c keeps): make the item definition RP:items/mboss/scarlet/item_sword.json a minecraft:select on minecraft:display_context with gui (and fixed) -> a dedicated icon model (the same silhouette with the scabbard / grip widened to >= 2.2 model px, about 2 GUI px, and the guard as a face-on plate, or a flat 16x16 icon painted from the rig's sprites: 0 or a few hundred atlas px), fallback = today's 3D model for none / ground / hands. Add a slot-resolution check (lit pixels at GUI x2 >= ~100) to test_rig.py.
- verifier: Major is right: this is a visible model defect on the special mythic reward and breaks the user rule "nothing too small or thin". Corrections to the wording: at native resolution the GUI x2 / x3 icon is a continuous aliased diagonal 1 screen px wide (8-connected, one piece), not a dotted or broken line. It looks beaded only when magnified. At the 1080p auto scale (x4) the line is about 2 px thick (3 lit px per row). It reads as a needle or hairline, not an empty slot. Side observation for D4 (code level, not a new finding, not a blocker): in itemSword() the 'guard' card is built with cardY() without the shift s = -0.72 b that bx() applies, so the decorated guard face sits at model y 7.984 px (mid-scabbard, beside the middle brass band) instead of on the guard plate at y 0.13-0.30 px. The intended position is about 0.304 px, so the card is 7.68 px = 0.72 b too high. It is edge-on and invi

### HR-04 (D1-02, minor, core) The counter (A1/A2) and skill (A6) triggers run before the reserved floor step, so CS1 / the A13 lead-in waits for one more attack
- where: data/rlk/function/boss/scarlet/core/fp.mcfunction:7-8 (generator core.py w('core/fp') l.207-208), ai/decide.mcfunction:5-6
- fix: core.py w('core/fp'): gate both trigger lines on `if score #fl hr matches 0` (or clear #a6q / #ctr in core/floor_hit when it reserves the step); test_scarlet: a 4-hit flurry ending on the floor hit -> CS1 / the lead-in at the next decision with no counter in between.
- verifier: Kept minor: one extra counter or A6 (at most about 55 t, about 2.75 s) before CS1 or the A13 lead-in. Her HP is held at the floor meanwhile, and no softlock follows. The delay is within what PLAN already accepts for 'the running pattern finishes first', so it is not 'clearly off the footage'. PLAN 4.7's 'the next decision at once is A1 / A2' conflicts on paper, but the floor precedence of 4.6 (as 타키 / 아를레키노) is the intended reading. The fix is sound: #fl is set by core/fight before core/fp in the same tick, so gating fp:7-8 on #fl 0 catches the trigger tick. It also stops A6 from cancelling a windup after the floor.

### HR-05 (D1-03, minor, core) cleanup leaves the pattern / ghost / sequence fake players in objective hr and storage rlk:hr seq.g after every fight
- where: data/rlk/function/boss/scarlet/cleanup.mcfunction:34-134 (generator core.py l.648 `resets = [... for k in S.FP]`), seq/lead_stand/start.mcfunction:4
- fix: core.py cleanup: also reset the other owners' families (#sq_* of seq.py, #g_* / #r2_* of p_ghost.py, #a6_* / #a9_* of p1.py; e.g. a list in api.py next to CORE_FP, or collected from the writers) and `data remove storage rlk:hr seq`; or save #hrEv #hrEvDone #hrEvDrop, `scoreboard players reset * hr`, restore them.
- verifier: Kept minor. The brief's blocker list names 'scores / storage left behind after the fight' as examples of breaking the fight, run, reward or world, and this breaks none of them. These are inert fake players in the module's own persistent objective, which by contract already keeps #hrEv* and rig.* between fights. Each is rewritten before any read on every path I checked, so no later fight, run or other boss changes, and all of it goes with the objective at uninstall. It is still a real deviation from the 타키 / 아를레키노 practice and from the cleanup comment ('every state'), so it stays as a minor finding. Both fix options are fine. The save / reset * / restore one also covers future owners.

### HR-06 (D1-04, minor, tests) Module test hooks leave the fight in dead states: test 30/35 outside P1/P2 freezes the phase; tests 23/29 make every later gauntlet of the fight unwinnable
- where: data/rlk/function/boss/scarlet/test/intro.mcfunction, test/skip100.mcfunction, core/replay/end.mcfunction (core.py l.735, l.788); test/a8_fail.mcfunction, test/a13_fail.mcfunction (#pipoff 1, core.py l.781)
- fix: core.py: test 30 / 35 refuse outside #ph 1 / 7 (or replay/end hands back through core/p2/from_fail when #ph is not 1 / 7); reset #pipoff 0 in core/g/end and core/g/pause (a forced fail applies to one judge only).
- verifier: Kept minor and area tests. Only the op test hooks (README 0-8 in-game test commands) reach these states, never normal play. Still, a forced fail that sticks for the rest of the fight, and a replay that freezes the phase, make later test results misleading. Both fixes are sound. A refusal outside #ph 1 / 7 would mirror 타키's force; resetting #pipoff in g/end and g/pause scopes a forced fail to one judge. The D1-01 in-game repro uses test 23, so after the fix the replayed A8 there would become clearable.

### HR-07 (D1-05, minor, core) The A13 instant death can be dodged by leaving: a disconnect or save & quit before T+258 restarts A13 with 5/5
- where: data/rlk/function/boss/scarlet/core/g/pause.mcfunction, resume.mcfunction, core/re/g.mcfunction (the restart rule of PLAN 3.8 / 5.6)
- fix: core.py g/pause / re/g: when the gauntlet's fail is lethal (A13; A8 with ULT60_LETHAL), #pips >= 1 and #pt >= its last counting strike (api.SCRIPTS: 238 for A13, 174 for A8), keep a 'fail pending' #grs value and on resume / reload apply the fail (ult/fatal as the player once tagged and alive -> the existing revive path) instead of restarting; or record the escape as a known limitation in README 0-9 if the restart rule stays.
- verifier: Kept minor. The restart is what PLAN 3.8 / 5.6 specify for a paused gauntlet. The loophole is a consequence the PLAN did not consider, and it needs a deliberate quit, disconnect or op /reload (selection screens refuse in combat), much like save-scumming. It is not 'wrong behaviour a player will notice' in the brief's sense, and nothing breaks. The multiplayer disconnect and /reload routes are confirmed. The singleplayer save & quit + reopen route depends on whether the forceloaded body exists when #load runs (not verified; see D1-01). Either way the instant death does not land after the quit. The two fixes are the lead's design choice: a 'fail pending' #grs that applies ult/fatal on resume or reload once the player is back, or a README 0-9 note.

### HR-08 (D2-02, minor, items) 홍련일섬's screen-edge vignette is gated on vBig, which never counts down outside the F5 view: it never shows in shoulder view or first person (sr-2, deferred to R)
- where: F:items/proc/hw_slash_q.mcfunction:40-42 (decrements only in F:view/ride_tick:13 and F:view/sel_xhair:3)
- fix: Inside SR's file (view/* is read-only for stages): test vBig only where it has a meaning, e.g. replace `unless score @s vBig matches 1..` by `unless function rlk:items/proc/hw_vbig_busy` with a new helper that returns 1 only when `#on view` 1, `#vmode view` 2 and vBig >= 1 (outside F5 nothing else uses the title line, so only ttlT matters); or the lead adds a per-tick vBig decrement outside F5.
- verifier: Kept minor: cosmetic only; the ring, sound, slash and crit window all still fire, and the PLAN calls the vignette optional. Corrections: the lobby does not offer the shoulder view (lobby/set/s20 toggles 1st person <-> F5 only; labels:3 only labels a vmode 1 set by command), so the affected lobby choice is first person. The first map (type 0) sets no vBig (room/gen_title:12-14); every later map sets 70. On the fix: the first option (ignore vBig outside F5) would let the vignette overwrite title-line overlays that set only vBig in every view and cut them short, e.g. mboss/fieldgen|butterfly fx/hud/flash_* (vBig 16, 'on the title line (any view mode)') and her kit's ovl at I1b (PLAN: vBig = in+hold+out). A per-tick vBig decrement in every view (i1_notes' fix, in view/tick before the #eff 0 return) is the safer fix.

### HR-09 (D7-02, minor, items) 검신합일 fires on any dashInvT, so a downed Ronova (and burst / fall invulnerability) counter-slashes mobs
- where: F:player/dash_iframe:4 (SR's hw_ctr_q line) <- F:player/take_damage:5 (any dashInvT >= 1); dashInvT is also set by F:char/ronova/revive:18-19 (downed: #rnDieT 60 + 20 = 80 t), F:char/burst_wind:6-7, F:char/motion/events/{navia,skirk,arle}/burst* (#pmInv), F:room/fall/player:14 (20 t); room hits reac
- fix: Count only a real dodge: gate the dash_iframe line on the dash itself (e.g. `unless score @s rnDie matches 1..` plus a flag player/dash_go sets for its 6 i-frame ticks, or `if score @s dashMoveT matches 1..`), keeping the take_damage line for hits that land. SR's hand file; test_hwamu counter section + a downed / burst-window case.
- verifier: The mechanism is real and minor fits. The downed scenario is overstated, though: P1 calls take_damage every 10 t during rnDie, and the pack's own downed rule stops that. cm/world:10-12 sets #cmDown, so every per-kind brain tick in cm/tick:13-29 is skipped and cm/down cancels and holds the attack. char/ronova/die_tick:4 puts every rlk_mob on team rlk_stun, the body's team (view/fps_tick:5, view/spawn:29), so vanilla mobs drop aggro. mboss/hurt:18, mboss/hz/hurt_pm:9 and boss/raiden/hurt:3 refuse while rnDie >= 1. While downed, only custom-mob projectiles already in flight can hit, because cm/pj/world keeps running from tick:50. The killing blow also queues a counter through take_damage:39 (#hurtDmg >= 1, by design, the same as 불사자의 갈기's lion_queue), and its 40-52 t cooldown covers most of the 60 t downed window. A dodge-counter from the floor is therefore rare. The realistic extra counter

### HR-10 (D7-03, minor, items) The sword's cooldowns survive the run reset: a stray '홍련일섬 ready' click at the next grant, or a swallowed first burst
- where: F:items/proc/hw_clear:2-14 (keeps #hwCtrCd / #hwSlCd and their end times by design); F:player/reset_stacks (the pack's per-run reset of every item timer / cooldown: #lionCd, #maidCd, #skCd, #oathT ...) has no #hw* line; F:player/reset_one (SR's file) resets only hrMoon
- fix: Reset the item state per run as every other item does: in player/reset_one (SR-owned) or by request in player/reset_stacks set #hwCtrCd #hwSlCd #hwCtrQ #hwSlQ #hwCritT #hwStk #hwAtk #hwHits #hwOn 0, #hwWait 0 and `scoreboard players reset 육참골단 stacks`; hw_clear keeps its in-run behaviour.
- verifier: Minor is right. The visible effect is mostly (a): a stray sheathe click and 4 sparks at the first held tick of a later run, usually at the event grant, whenever the previous holder's run ended within the 40-52 s ICD after a burst (common: a death in a boss fight). It is cosmetic, and at a grant it may even read as part of the grant. (b) cannot happen across a real run boundary: run/start clears the inventory, and the event comes minutes into a run. It is reachable only in the lobby trial (discard all, then take the sword from the codex again within 40-52 s) and in tests. There it behaves like the accepted sr-9 drop / pick-up ICD, so on its own it is barely a defect. The core defect is the per-run state leak against reset_stacks' own convention. The proposed reset in reset_one or reset_stacks is the right fix.

### HR-11 (D7-04, minor, buff) The 'forever' buff scope (question 1) is not one switch: buff_scope is read by no generator, the rift chat keeps '이번 런 · +20/10/10'
- where: T:mboss_scarlet/api.py:1167 (EVENT buff_scope, never read), :1199 EV_TEXT chat_buff, :1202 status; T:mboss_scarlet/reward.py:45 (asserts the run values), :109 (ev/record = the literal) -> F:boss/scarlet/ev/record:3; F:player/update_item:100 (fallback '... (이번 런)'); F:load:676-680; PLAN §7.0 table / 
- fix: S3 reward.py: build the buff chat line like ev/title's subtitle (score components of api.BUFF_FP) and take the scope words from buff_scope ('이번 런 동안' / '영구히', EV_TEXT keyed by scope); SR update_item: the scope word from a constant set next to the 조절 지점 (or one more `with` argument), so the switch is api + load only; README 조절 지점 row and PLAN §7.5.3 list every place.
- verifier: Minor is right. The default build is correct, and the wrong notice appears only after someone applies the documented alternative switch (Q1 = forever, still open per contract line 13 and PLAN §0.1) or retunes #hrMoonAtk / #hrMoonCrit / #hrMoonSpd in load (PLAN §7.5.4 suggests 25). In both cases the rift chat record keeps "+20 / +10 / +10" while the title and the stat line follow the constants. The fix belongs to S3 (reward.py builds the chat line from score components plus scope words keyed by buff_scope) and SR (the scope word in update_item). The README / PLAN switch lists should name every place.

## Lead decisions (11-05, binding for F)
- HR-01: as proposed (#grs 4 → core/p2/from_fail in resume and core/re/g when not ULT60_LETHAL) + test_scarlet R9 / R11 cases.
- HR-02: no `tp` of the player in the ending: `rotate @s facing entity <her> eyes` (rotate does not dismount) and, for the avatar,
  `rotate @e[tag=rlk_av,limit=1] facing entity <her> feet`; correct PLAN §3.0 (l.378-380) and §3.7 wording; a sim stub cannot
  show it, so add a static check (no `tp @a[tag=player]` / `tp @s` of the player inside seq/** while the view rig is on).
- HR-03: built on top of S2c (the rig generator S2c changes): `item_sword`'s item definition selects on `display_context`: the
  gui / fixed / ground contexts get a dedicated chunky icon model (our sword's silhouette, blade and scabbard ≥ 2 GUI px wide at
  16 × 16, readable at x2), the hand contexts keep the rig sword; also fix the stray guard card (itemSword() 'guard' cardY()
  without the -0.72 b shift, seen by the D7 verifier). test_rig: a slot-resolution check (lit px / row ≥ 2 at x2).
- HR-04: gate core/fp's A6 and counter triggers on `#fl hr matches 0`.
- HR-05: save #hrEv / #hrEvDone / #hrEvDrop → `scoreboard players reset * hr` → restore; `data remove storage rlk:hr seq`.
- HR-06: both fixes (tests 30 / 35 refuse outside #ph 1 / 7; #pipoff 0 in core/g/end and core/g/pause).
- HR-07: "fail pending": once a lethal gauntlet's last counting strike has passed with #pips ≥ 1 (A13 T+238; A8 T+174 only with
  ULT60_LETHAL), a pause / reload keeps a pending-fail #grs value and resume / re/g applies the fail as soon as the player is
  back and alive (the existing fatal → revive path); before that strike the restart rule (PLAN 3.8 / 5.6) stays. Tests for both.
- HR-08: count vBig down every tick in every view (view/tick, before the first-person return); F must list every vBig reader /
  writer first and confirm nothing else changes for the worse in first person (if something does, gate only the vignette on
  ttlT outside F5 instead) — pack-wide file: run every suite.
- HR-09: a dash-only flag lasting dash_go's 6 i-frame ticks gates the dodge counter (burst / fall / revive i-frames no longer
  count); landed hits (incl. the killing blow) keep queuing as designed.
- HR-10: per-run reset of the sword's state in player/reset_one (as proposed); hw_clear keeps its in-run behaviour.
- HR-11: as proposed (reward.py chat line from score components + scope words keyed by buff_scope; update_item's scope word
  from a constant next to the 조절 지점; README / PLAN list every place).

## Open, unverified (framework-generic, not 홍련's)
- D1 verifier: on a singleplayer save & quit + reopen, 26.3 runs #load before the first ServerLevel.tick adds loaded entities,
  so a forceloaded boss body may be missing when mboss/init runs and mboss/main:7-10 may drop the fight (every boss). Not
  tested; no action unless it shows in V.

## Lead items from I1b (11-05; wip/hr 4c81817) — F does these too (not review findings; reviewers: do not report again)
- LF-01 (minor, arena): the moon halo is summoned at integer x / z (`889 218 -33`, 3 lines) → the game block-centres it, 0.5 b
  east of the moon disc's centre and 1.5 b in front instead of 1 b. Fix with I1b's `api.xyz` helper (decimal x / z) at the source.
- LF-02 (minor, seq): the ending's moon target `facing 889 218 -34` (13 lines) is integer → 0.8° (≤ 2.0°) off the arena centre.
  Same fix.
- LF-03 (docs): PLAN §3.1's seat text predates decision 1 (seat (884.0, 201, 5.0), walk legs while > 7 b); update the PLAN text. **Done by the lead 11-05** (PLAN §3.1 and §6.7).
- LF-04 (tests, other bosses, out of 홍련's scope): the `cmsim` copies the other bosses' suites use let only air and light through
  `#rlk:dash_pass` (the real tag holds more); I1b fixed only `hr/tests/lib`. V decides: port the fix to the shared copies and
  re-run those suites, or list it in README 0-9.
- I1b decisions accepted: (1) the halo's default looks dimmed 17 % (tint 0xD4D4D4) so p1b / p2b can be 1.2× — no second sprite
  pair (render HR/renders/i1b_halo_looks.jpg reads well); (4) cost rule: look-job slice ticks ≤ 5 000, every other fight tick
  ≤ 3 000, average ≤ 600 (contract §5); (3) halo / lotus following the moon / crimson / dark looks → the in-game watch list of the
  release notes (README 0-9 "확인할 것").

## R-late part 1 (11-05; snap_l1 = wip/hr 4c81817; workflow wf_e4c68522-cd7): HR-12 … HR-46
Every finding was confirmed by an independent verifier (no refutation); D3a / D3b / D5 / D2K then had a completeness critic whose
findings (ids `-Cnn`) were verified again. Full text (where / what / evidence / repro / fix): `HR/review/findings_<dim>_late.json`
and `HR/review/critic_<dim>_late.json`; verdicts (with corrections — read them, they refine several fixes):
`HR/review/verdicts_<dim>_late.json` and `verdicts_<dim>_late_c.json`; all in one file: `HR/review/late_p1_all.md`.

| HR | dim id | sev | area | title |
|---|---|---|---|---|
| HR-12 | D3a-01 | major | kit | The tilted / vertical sword-qi effects lie in a plane through her aim line, so the player's own camera sees them edge-on: A1's fan, A3's h1/h3/h4 crescents, A2 / A3 h2 / A8.3 crescents, A3 h5's wedge, A5's line, the A7 throw crescent and A8.8's vertical cut show as nothing, a hairline or a thin column |
| HR-13 | D3a-02 | major | ai | P1 near band starves: with the player within 4.5 b and not hitting her, she strafes ~6 s (119-129 t) without attacking after every second A3, waiting for A9's 300-t cooldown |
| HR-14 | D3a-03 | major | p1 | Every P1 / P2 pattern stacks a static in-clip recovery (22-34 t, no move or turn) on the AI's 16-24 t recovery: 43-56 t from her last hit to her next windup, against the footage's 11-15 t and PLAN §4.1's cap |
| HR-15 | D3a-C01 | major | ghost | The moon disc (R2, A13's three discs) is aimed on its release tick, so its aim is fixed only 0-4 t before it hits whenever the player walks toward her or her retreat is cut short by the rim (rule: aims lock 6-8 t before the hit; PLAN §4.5 "6-8 t before arrival") |
| HR-16 | D3b-C01 | major | kit | Her lines 5 and 24 are wider than the screen at the Auto GUI scale: the subtitle runs off both edges (line 5 loses 「그」 and 「만.」 at 1920x1080, 「그리고」 / 「겠구만.」 at 2560x1440 and 4K; line 24 loses 「조」 / 「니.」 at 1440p and 4K) |
| HR-17 | D2K-01 | major | kit | The A13 instant death's 홍련일섬 slash line (and its petal cards) never render: the kit's card ager clears every card in the same server tick the fatal kills the player |
| HR-18 | D5-01 | major | ai | T1 missed by ~2.5x: P1 costs the melee walker 55.6 %max/min = 0.45 x 타키 (target 1.00-1.15 x): it walks out of 76 % of what a standing player takes from her (타키: 31 %); only her player-centred lock discs (A9, A10) land, and those are the rare picks |
| HR-19 | D5-02 | major | ghost | T5 / T5b missed: the 9 counting cuts of A8 and of A13 cost a standing player 50.4 % max HP (target <= 45 %); after A8's fail hit he is left on 1 HP only by the #mbDotLethal clamp |
| HR-20 | D5-03 | major | buff | G3 missed: B1 「월하대작」 is x0.89 (mid) / x0.94 (late) of 화무십일홍 ★★ net (target within +-5 %); #hrMoonAtk 20 is too low for the measured fight rates |
| HR-21 | D5-C01 | major | items | G2 is only passed at boss-fight counter rates: at the counter cap that PLAN §7.4.2 / §7.4.7 name (crowded rooms, 'at most level with 키리온 even at the counter's cap') 화무십일홍 ★★★ beats 키리온 by 7.7-10.7 points |
| HR-22 | D3a-04 | minor | p1 | A2's lilac glow along the blade (PLAN 6-11, the clip's 'glow' event) is never shown |
| HR-23 | D3a-05 | minor | kit | Tells and trails that should travel with her are left where she started: the A13 / R2 / A10 yellow tell, A6's blink bubble, A4's ribbon |
| HR-24 | D3a-06 | minor | p1 | A9's iai streak is always drawn 12 b long, past the end of her dash and of the hit line |
| HR-25 | D3a-07 | minor | ai | After a flinch the recovery walk / strafe clip is not replayed: she slides in the flinch's held pose |
| HR-26 | D3a-C02 | minor | ai | The counter trigger (A1 / A2) and the rear rule (A1) have no distance gate: ranged hits from 9-14 b make her swing a melee counter at the air, in place of the far rule's gap closer |
| HR-27 | D3a-C03 | minor | ghost | The D2 (+80 deg, 8 b) and D4 (-80 deg, 12 b) reappearances land just outside the default F5 view (and far outside first person); the footage shows them at the screen edge, so the approach is first seen only 7-8 t before its counting cut |
| HR-28 | D3a-C04 | minor | p1 | A4's leap and A10's spring / dive show no trail in P1: the afterimage is gated on P2 although PLAN §4.3 lists it for A4 / A10 and the footage shows the streaks; A10's curved dive trail is missing in both phases |
| HR-29 | D3b-01 | minor | seq | The HUD stays partly on through the cutscenes: the boss bar for all of CS0, the player's actionbar HUD in CS0 (0-19, 541-640), CS1 and CS4 + the coda |
| HR-30 | D3b-02 | minor | kit | A subtitle held over a fading full-screen overlay dims with it, drops out 1-2 t and pops back (line 15 at CS1 110-113, line 11 at the end of the skip's black); a typing step is lost |
| HR-31 | D3b-03 | minor | seq | CS3 -> CS4 seam: the hat jumps about 1.9 b in one tick (beside her -> over her face) with no cut to hide it |
| HR-32 | D3b-04 | minor | seq | CS4 E1b: the lilac ground-slash band stops about 1 b short of the player instead of sweeping across them |
| HR-33 | D3b-05 | minor | event | The coda's item title and the rift chat record show 「[ MYTHIC ] 화무십일홍 ★☆☆」 with dark-red stars, not the item's own display name (gold ★, grey ☆☆) |
| HR-34 | D3b-06 | minor | seq | Holding Shift to skip the intro also fires the F5 Shift-tap: with an unopened level-up pick a deny sound plays at the start of every skip |
| HR-35 | D3b-C02 | minor | event | The coda's item title 「[ MYTHIC ] 화무십일홍 ★☆☆」 (4x) and the buff subtitle 「최종 공격력 +20% · 치명타 확률 +10% · 이동 속도 +10%」 run off the screen edges at 2560x1440 / 4K / 1920x1200 Auto (the item title by 1 px a side already at 1080p) |
| HR-36 | D5-04 | minor | tests | The balance probe's vendored hrsim predates I1b's block-tag fix: on 4c81817 every dry-grass / crimson-root cell of hr_field refuses her mv/ok in the probe |
| HR-37 | D5-05 | minor | tests | The probe's ranged walker crashes in every whole-fight run at A8's dive (T+188), so run_hr.sh silently drops the three whole:ranged:walk:bow runs |
| HR-38 | D5-06 | minor | ai | T8 can be broken in P2: A6's P2 cooldown is 340 t, so a player who lands skill hits often gets two back-blinks 385 t (19.3 s) apart (target: at most one per 20 s) |
| HR-39 | D5-C02 | minor | tests | reward_ev counts 42 % of its counter events while she is invulnerable: the real 검신합일 spends its cooldown on her ghost body and deals nothing, so G1-G3 use a ~23 % too high counter rate |
| HR-40 | D5-C03 | minor | tests | T9 is measured at one level (Lv15 vs L16, a chapter-3 encounter) and passes there by 1.8 s; at chapter-1 / 2 levels, where most rifts open, the item-less kill falls below 230 s |
| HR-41 | D2K-02 | minor | kit | The deflect / A8-fail light column takes the player's body pitch: the 9-b column leans with the view and its base dips below the floor |
| HR-42 | D2K-03 | minor | kit | The P1 ambient petal sinks below the floor when the player looks down: core/amb1 runs ambient_p1 with the player's pitch |
| HR-43 | D2K-04 | minor | arena | 98 floor cells under boulders / wall stones / trunks change by random ticks in game (mycelium -> dirt in moon, crimson nylium -> netherrack in crimson / dark): the looks are not block-exact between jobs |
| HR-44 | D2K-C01 | minor | kit | 홍련일섬's 60-b slash line runs 5.4 b under the floor (CS1 C8, the A13 instant death, the A8 fail with ULT60_LETHAL): test_kit floor-checks scarlet_line only at len 70 |
| HR-45 | D2K-C02 | minor | kit | Player-anchored kit effects are drawn through the first-person camera and never show in first person: the 홍련일섬 line (CS1 C8, the A13 death), the deflect's gold starburst and light column |
| HR-46 | D2K-C03 | minor | seq | CS0's arrival wind (E0, item.elytra.flying) is played at her seat 26.7 b from the player with minVolume 0: it is never heard |

## Lead decisions for HR-12 … HR-46 (11-05, binding for F / S5)
- **HR-12** (qi planes edge-on): as proposed. Kit: `qi_vert` / `qi_fan` / `qi_line` get a stance **across** the aim (yaw 0 = the
  plane perpendicular to the executor's facing, as `qi_band`); `qi_arc` / `qi_wedge` with |roll| ≥ 20 are rolled in the screen
  plane (tilted toward the viewer), not about the aim; floor clamps kept. Callers per the footage (A3 h1 wrapping at the player's
  left, h3 / h4 across the aim, h4 where line(5.0, 1.8) reaches; A5's line across; A8.8 across and ≈ 1.5 b to the player's right;
  A7's throw crescent across her aim); contract §6's A8.8 `yaw:0` corrected. Test: a `view` section rendering every contact effect
  from the default F5 camera behind a player standing on her aim and from first person: ≥ 1 500 card px at 320 × 180 each.
- **HR-13 + HR-14 + HR-18 (+ HR-25, HR-26, HR-38) — the P1 pressure package** (one design; F builds it, S5 sets the numbers with
  the fixed probe):
  1. Pattern ends: every P1-kit pattern ends 8-12 t after its last hit (D5-01's ends: A1 24, A2 22, A3 79, A4 46, A9 40, A10 32);
     R1 / R3 reform tails ≤ 12 t; during any tail kept and in the recovery she walks / strafes **facing and tracking** the player.
     Recovery knob P1 12-20 t, P2 10-16 t. PLAN §4.1 wins over §4.3's tails (update §4.3's table).
  2. No empty band: P1 near gets A10 (weight 20) and small A1 / A2 near weights (their cooldowns), so `ai/none` never runs twice in
     a row while the player is inside a band; if a band is still empty, the 12-t `backstep` clip then the mid pick.
  3. Cooldowns: A9 P1 300 → **160** (not 120: one full-screen flash per ≥ 8 s), A10 P1 **180**; P2 keeps §4.4's "P2 = P1 × 0.85"
     unless S5 measures T2 over its cap (then write the exception into §4.4).
  4. HR-26: the counter (A1 / A2) and rear (A1) rules only inside the near band (≈ 5 b); HR-25: a flinch replays the move clip;
     HR-38: A6's P2 cooldown 400 (and §4.3 / §4.7 / §4.8 agree).
  5. Damage tiers stay inside PLAN's ±20 % knob; the counting cuts get their own tier TC 37 (HR-19). If T1 is still short after
     S5's measurement, add **tracking** (the A3 hits re-aim at their own 6-8-t locks; arcs as the footage shows), never more damage.
  Every change keeps the telegraph rules (quiet tell ≥ 12 t, ≥ 20 t big hits; aims lock 6-8 t; chains ≥ 10 t; no decal) and the
  타키 lessons (no long waits, real gap closers, tracking combos, knockback only on the last hit, no multi-second hovering).
  Targets for S5: T1 1.00-1.10 × 타키 (not the top: the probe walker escapes from inside her box — S5 checks her collision and,
  if the game pushes the player out, keeps the walker outside it), T2 ≤ 1.25, T3 ≤ 1.8, T4 ≤ 40 %, T5 ≤ 45 %, T8, T9 in band.
- **HR-15** (disc aimed at release): as proposed — a floor lock marker at the player's feet 7 t before each release (tagged as
  p1.py's `lock_fn`), she turns to it, `g/disc/throw` aims at it; PLAN §4.4 R2 / §4.5 A7 and the api comments; pat_ghost checks
  incl. a player walking in at 0.22 / 0.28 b/t from 5-9 b and R2 against the rim (hit ≥ 7 t after the lock).
- **HR-16** (lines 5 / 24 too wide): as proposed — every line wider than **192** font px (fits the Auto GUI width of 1920 × 1200
  and smaller; lines 5, 24 and 22) is shown as consecutive subtitles split at its natural pause, the text verbatim
  (`api.LINE_PAGES`; `api.LINES` stays whole), inside the same `LINE_AT` hold. test_kit: every typed step ≤ 192 px, the pages
  joined with one space == `api.LINES[id]`.
- **HR-17** (A13 death line never renders): as proposed — a keep tag (`rlk_hr_fx_keep`) that `fx/clear` and e/world's dead /
  rnDie lines skip (cleanup / uninstall still kill every `rlk_hr_fx`); used by the A13 / ULT60 A8 death line, petals and bolts
  and by CS3's `kick_flash` cards (killed in their own tick today, D3b verifier). Test with `hrsim.kit_on`: alive ≥ 12 t after.
- **HR-19**: as proposed (TC 37 → 12 HP per cut, 40.3 %; PLAN §4.5 / §5.3, `api.cut`, pat_ghost).
- **HR-20 + HR-21 + HR-39 — item / buff (S5)**: (a) reward_ev's counter model fixed (no `dot`; no counter on an invulnerable
  body) and the game fixed the same way: 검신합일 never fires at / spends its cooldown on an `rlk_mb_inv` target (PLAN §7.4.2
  "no target = no cooldown"); (b) the dense-room measurement PLAN §7.4.7 asks for (≥ 8 mobs: counter rate and 홍련일섬's target
  count), G2 judged at the 90th percentile over rooms + boss fights **and** at the cap (FE-5's claim), both slash target counts;
  (c) the item and the buff tuned together until G1-G3 pass: start #hwCtrCdT 80, #hrMoonAtk 28; if the 2-target room reading
  still fails, lower the slash (#hwSlCoef) rather than the counter rate; (d) every number into PLAN §7.4 / §7.5, items.md, the
  tooltip (follows the constant), README 조절 지점. HR-11's fix first.
- **HR-22, HR-23, HR-24**: as proposed (A2 glow incl. the cancel lines; tells / trails follow her or spawn where the move ends;
  A9 streak at the probed length).
- **HR-27**: as proposed (D2 / D4 bearings ±55-60°, inside the default F5 view near its edge; contract change in §7; tests).
- **HR-28**: as proposed (A4 leap / A10 spring trails in both phases along the motion + A10's dive trail; afterimage on A3 / A6
  / A9 stays P2-only); reconcile PLAN §4.3 / §4.4 wording.
- **HR-29** (HUD in cutscenes): as proposed — no boss bar in CS0 (bars off at the intro's start; the bar appears at control, as
  the original's grows at f498), the player HUD held in CS0 / CS1 / CS4 + the coda; CS2 / CS3 / SQ1 / the lead-ins keep it; test.
- **HR-30**: as proposed (a line is never dimmed or dropped by an overlay fade; include CS1 169's red_tint case).
- **HR-31** (CS3 → CS4 hat jump): a hard cut at CS4 tick 0 (a 2-3 t black or white flash, as the original cuts) under which the
  hat moves; done **after I2** (S2d's hat positions); test_rig's hand-over checks include the repel(5 %) → ending seam.
- **HR-32**: `qi_band` gets a sweep-length argument (her distance + 1 b in E1b; A8.2 keeps 2.5 b).
- **HR-33 + HR-35**: the coda title / rift record as components in the item's own colours (dark_red name, the star colours of
  `rlk:items` read at run time); the 4× title ≤ 106 font px (e.g. 「화무십일홍 ★☆☆」, 「[ MYTHIC ]」 moved to the subtitle), the
  buff subtitle ≤ 192 px; numbers from the scores (HR-11). System notices only (no tip text).
- **HR-34**: gate the F5 sneak-tap while a boss intro runs (`#mbLive 1` and `#mbSt 0`); pack-wide file → every suite.
- **HR-36, HR-37, HR-40** (probe): S5 — re-vendor the probe's lib, guard the ranged walker and make batch / analyze fail loudly,
  measure T9 at Lv5 / Lv10 / Lv15 (registry hp 250 → ≈ 270 if needed, with the P1 package).
- **HR-41, HR-42, HR-44, HR-45**: as proposed (absolute pitch for upright / level cards; 홍련일섬's line floor-safe at its real call
  heights and rolls; first-person anchors in front of the camera when there is no avatar); test_kit sweeps executor pitch ±60
  and uses the module's real call arguments.
- **HR-43**: as proposed (a non-ticking floor block, the same in every look, under opaque covers / full water; test).
- **HR-46**: play CS0's E0 wind at the player.


## R-late part 2 (11-06; snap_l2 = wip/hr 3741fc4, the F-I head): HR-47 … HR-55
Files: `HR/review/findings_D4_late.json`, `findings_D6_late.json`, `findings_DF_late.json`; contact sheet
`HR/renders/d4_late_issues.jpg`. DF verified every in-scope fix of HR-01 … HR-46 / LF-01 … LF-04 on the merged head.

| HR | id | sev | area | title |
|---|---|---|---|---|
| HR-47 | D4-01 | major | rig | The sword hand sinks into her head in the overhead poses (retargeted S2a grips on the 0.59-b arm): the blade grows out of the hat crown (A3 6-13 / 48-57 / 71-88, A4, A2 t11, CS4 duel, a7, g_run …); the build only guards the blade |
| HR-48 | D4-02 + DF-01 | minor | kit | A1 reads poorly: the flat hit crescent at body + 1.0 barely shows in first person (one tick ≥ 1 500 px); the tell fan is 189 px in F5 (test floor lowered to 165) |
| HR-49 | D4-03 | minor | rig | Walk / strafe skate (S2d residual, now frequent through HR-14's tails): the strafe never lifts a foot, the walk's planted foot slides ≈ 58 % |
| HR-50 | D6-01 | minor | tests | The cost gate never runs the down window, the A8 / A13 fail branches, the revive path, pause / resume or /reload (real maxima 3 672 slice / 2 299 non-slice, in budget) |
| HR-51 | D6-02 | minor | core | A pause after a deflect judge or a /reload from P2 re-runs a full crimson look job on an already-crimson arena (≈ 7.2 k commands, the fight's heaviest tick) |
| HR-52 | D6-03 | minor | kit | CS0: `fx/e/anim` / `e/stay` cost ≈ 39 commands / tick only to keep the seat stone's still bottle and cup attached |
| HR-53 | DF-02 | minor | docs | PLAN §3.1 says the intro walk ends ≈ 6.3 b from the player; on the S2d body 6.76 b (skip 6.50-6.76) |
| HR-54 | DF-03 | minor | tests | LF-04 still open: the other bosses' cmsim copies let only air / light through `#rlk:dash_pass`; README 0-9 does not list it |
| HR-55 | D6 note | minor | tests | test_arena_hr check 1e starts a Python subprocess without `-B` (wrote a .pyc into a snapshot) |

## Lead decisions for HR-47 … HR-55 (11-06)
- **HR-47**: fix in the rig — a head-clear guard on the grip targets (as `hatClear`): the fist and hilt move out to the side
  / front of the head while the blade keeps its attack direction and its events; a builder gate and a test_rig check that no
  hand, hilt or guard sample is inside the head / torso boxes (≥ 0.01 b) on any tick of any clip (not only the blade).
  Re-render the A3 / A4 / CS4 frames of the contact sheet.
- **HR-48**: as D4 proposes — the A1 crescent rolled ±25-35° like A2's (or raised to ≥ 1.3 b), the fan at h 16 (toward the
  footage's ≈ 1-body-height fan); the view test requires ≥ 1 500 px on ≥ 3 ticks in both views, the fan's own floor raised back.
- **HR-49**: ASIDE-like lifted side steps for the strafe and a longer walk stride so the planted foot holds; speeds unchanged
  (S5's); report the remaining slide.
- **HR-50 … HR-53, HR-55**: as proposed. **HR-54**: list it in README 0-9 (out of 홍련's scope; no port).
- The props' skin-matched colours (the hat brim ΔE 4 from the original's hair colour): kept — they follow the user's own skin
  (S2c decision); the shapes stay ours.
