# Lane VP progress (wip/v-player) — the player's perfect parry / perfect dodge presentation (round V)

Worktree `<S>/cb/wt_vp` (branch `wip/v-player`, base `origin/wip/v` 2793b54cd). Scratch: `<S>/cb/vp` (`sim` = copy of
`tools/dev/sim` with the paths rewritten, `suites.sh`, `out/`, `dbg` = the clip debug datapack, `prev/` = sheets, `bc/` =
javap output). Pack copy `<S>/rp_vp` (from `<S>/rp_fin`, the 11-11b release pack). Contract: `v_brief.md` §3 "VP" + §5.

## Steps
- [x] 1 the box: `rlk:cb` cells <= 256 px (streak = four 256 x 64 strips, glint = two 160 x 64 halves) + the `rplint.py` rule
- [x] 2 tiers: tier 2 / 1 = small pale spark + chain "tick"; only tier 3 gets the big presentation
- [x] 3 the beat engine (clock, gates, mob hold, untouchable, kit clocks, rock-back, interpolation stretch) + `test_cb` section
      `beat` (49 checks) + `beatloop_cb.py` (a real mid-boss fight, beat on = beat off world tick by world tick)
- [x] 4 the avatar: clips `pparry` / `pdodge` for the three rig characters, the stand-in rig for the four mannequin characters,
      the weapon glow variants, the red-pink body tint; sheets
- [x] 5 README 3 / 0-4 / 0-6 / 0-8 / 11, hr_design addendum, ident_hr allow group, gates (below)
- [ ] 6 final report

## What the user asked (v_brief §1.2, §1.5) -> what is built
| item | built |
|---|---|
| the box at the title's place | `tools/build_combat_fx.py`: every cell <= 256 px (asserted in the generator); `rplint.py` flags a cell over 256 px in either direction, `ascent > height`, a missing bitmap, ragged `chars` rows, in any font of the pack. The 11-11b pack: 3 problems (streak 512 x 288, streak_s 512 x 288, glint 320 x 64); the new pack: 0 |
| tier 2 looked perfect | `fx/p2` / `fx/p1`: one small pale-yellow spark glyph (0.45 b / 0.3 b, 3 ticks), a few motes, `block.chain.hit` (+ a quiet amethyst hit for tier 2). No flash particle, no star, no title, no beat. `fx/p3` alone starts the beat |
| slow motion | the beat (below): perfect parry = hit-stop + 4-tick freeze (5 held ticks), perfect dodge = 1-tick hitch, 4 ticks at speed, x1/3 for 9 ticks (7 held ticks) |
| yellow light on the sword | the weapon model itself: the five rig weapon models a beat clip can show (spear, scythe, sword, cryo sword, halberd) have a `<name>_glow` item model (its own elements + an emissive shell of the same elements on yellow-white "hot" copies of its own sprites, light emission 15, so it follows every cut-out) shown from the contact tick to tick 12 at full brightness; a mannequin's vanilla sword gets `wg/<sword>` (the vanilla model + an emissive glow card along the blade); the catalyst characters get a light in the hand of the stand-in rig and their floating catalyst outlined yellow |
| back-flip-like dodge | clip `pdodge`: upright with both arms raised, arching back through the slow motion, then a 360-degree back handspring (inverted with split legs at the apex, hands 0.1 b over the floor), landing in a T pose facing the attacker, sinking into a ready stance |
| P2 crimson field | the dodge overlay is a dark vignette (hue-independent) with a faint pink centre; the ghost's outline is white; the burst and embers are light pink; the avatar is tinted red-pink, full bright, with a pink outline |

## The beat (how it works)
State (objective `cb`): `#btK` 0 none / 1 parry / 2 dodge, `#btA` age in real ticks (0 = the hit's tick), `#btHold` 1 = this real
tick the world is held, `#btInv` 1 = the player is untouchable this tick, `#btLag` = held ticks so far (never reset: part of
the clock), `#btAdj` = `#btLag` - `#btHold`; tunable `#btOn tmp` (1 = hold the world; 0 = effects only, the 11-11b clock).
`rlk:tick`: `#now cb` = gametime; `execute if score #btK cb matches 1.. run function rlk:player/def/beat/clock`;
`#now cb -= #btAdj cb`; ... the worlds ...; `execute if score #btK cb matches 1.. run function rlk:player/def/beat/post`.

- **The combat clock** `#now cb` = gametime - held ticks = the number of the next world tick to run. Every stamp of the
  parry / dodge logic (`parAt` `parLk` `parHit` `dgAt` `dgRw` `#dgEnd` `#dgKill` `#parMl` `#dgRf`, the queries
  `q_pf0` / `q_pf1`) is on it, so windows, the F lock, the whiff ladder and the 홍련 pips count world ticks: nothing changes in
  un-slowed terms. An F or a dodge pressed during a hold is stamped with the tick the world resumes on (an input buffer: the
  beat never eats an answer).
- **Schedules** (real ticks after the hit): parry: hold 1-5 (hit-stop, deflect, freeze), release 6; untouchable 1-5; the
  presentation runs to 16. Dodge: hold 1, go 2-5, then hold 6-7 / go 8, hold 9-10 / go 11, hold 12-13 / go 14 (x1/3), full speed
  from 15; untouchable 1-14; the handspring 14-21, ready 26. N (the stretch) = 5 / 7.
- **Untouchable**: `judge2` step 3-1 (after the perfect dodge and the perfect parry, so a perfect answer inside a beat is still
  that answer), `player/hurt_elem`, `mboss/pl_dot2`. Scripted lethal hits that never went through the judge (홍련's `ult/fatal`,
  나루카미's `hazard/fatal`, the butterfly's `coc/apply_pl`) are not voided: they are mechanics, and they sit on the held clock.
- **Ending**: `beat/end` (idempotent) on its last tick, when the next beat starts, and from the clock on: no tagged player,
  `dead`, `rnDie`, `pkMode`, `vMap`, `rdCam`, `#mbCam`, `#mbCine`, the camera-hold tag; `rlk:load` calls `beat/reset`.

## The clock list (every clock that follows the beat, found by search, and how it is gated)
Search: the dispatch lines of `rlk:tick`, every `time query gametime` (115 files), every `schedule` (303 lines), every
per-tick decrement in `player/tick` and `mob/tick`.

| clock | where | how it follows the beat |
|---|---|---|
| registry bosses: module AI and pattern clocks, the rig (clip clock, follow), `mv` glides / leaps, `hz` hazards, `pj` projectiles, `pull`, bars, typed lines, chapter mode (`world_cm_pre/post`), boss DoT, the gauntlet / shield / ULT clocks of 홍련, balance `bal_tick` | `mboss/main` -> `mboss/world` (everything a boss fight ticks hangs under it) | hook 1 in `build_mboss_core.py`: `mboss/main`'s first line returns on a held tick, before `#mbLowG` / `#mbCam` are cleared (the requests survive). One command per boss tick. (A condition on `rlk:tick`'s own `mboss/main` line costs none, and was tried: the camera suites' `hr/h2/camsim.py` finds that line by its exact text and lane VC edits the lines next to it, so the hook stays in the core as the brief says.) |
| the near re-test of the dodge window | `rlk:tick` -> `mboss/near_all` | gated in `rlk:tick` |
| custom mobs: brains (`cmS` wind-ups, `cmCd` cooldowns), all cm rigs (ch1 / ch2 / ch3), aim markers | `cm/world` | the condition on its `rlk:tick` line |
| custom-mob projectiles and ground effects | `cm/pj/world` | the condition on its `rlk:tick` line |
| 나루카미: AI, objects, hazards, movement fx, domes, orbs, vfx worlds, her own balance clock | `rlk:tick` -> `boss/raiden/world` | gated in `rlk:tick` (her clock runs outside the registry: one dispatcher line) |
| every mob: stun `stunT`, balance regen / groggy `balT` (`bal/tick`), element state and DoTs `elAct` (`element/tick`: `frzT` too) | `mob/tick` | the three lines gated; the health bar, the click shield and vanilla-hit detection keep running (the player can hit a frozen enemy) |
| vanilla AI and physics of mobs (walking, vanilla melee, the cm brains' pathfinding) | the server | `beat/hold_on` / `hold_off` on every hold edge: `NoAI:1b` on every `rlk_mob` that did not have it (tag `rlk_bt_noai`), restored unless a freeze / groggy took over meanwhile (their "was NoAI before" notes `rlk_noai` / `rlk_bal_noai` are corrected) |
| the F lock, the whiff ladder, the 3-tick re-press block, parry / dodge windows, the dodge-start box | stamps on `#now cb` | the combat clock (above) |
| the dodge cooldown `dashCool` | `player/tick` | the decrement is gated |
| the effect kits of 6 bosses (cards' ages: az, ap, tk, kn, bf, fg; self-scheduled, so they run on held ticks) | `<boss>/fx/e/{world,make}`, `fx/tele/wave_to`, apep `fx/p/**` | in the generators: `e/world` skips a held tick on its second line (it only re-schedules itself: the per-run counters stand still too) and every `time query gametime` is followed by `-= #btLag cb` (ages and timed cards stay in step with the hits afterwards). `beatloop_cb.py` compares the kits' scores too |
| the warning glint's spacing `#npGap` | `mboss/np_gate` | core hook: `#npNow mb -= #btAdj cb` |
| 야타용왕's "time since the proxy was hit", 역장's break / banner stamps | `boss/azhdaha/{ai/sample4,on_hit}`, `mboss/fieldgen/{on_hit,field/banner,hud/banner_cut}` | `-= #btAdj cb` in the module generators |
| display interpolation of world displays in the x1/3 phase | client | `beat/st/*` (below) |

**Not on the beat's clock, on purpose** (player side or cosmetic; said here so nobody has to search again): the player's own
timers in `player/tick` (attack / combo / skill cooldowns, buffs, i-frames `dashInvT`, the dash travel `dashMoveT`), the
avatar and its rig, the player's projectiles and summons (`char/**`, `items/hook/tick_world`, `element/tick_world`), item procs
on gametime stamps (`items/proc/*`), the balance sources' per-target throttles (`bal/src/hit`, the player's hits), 나비아's
cards, damage numbers, drops, the room logic (`room/tick`: waves, doors), the lobby, 나루카미's background and the arena
builders (`schedule`), same-tick caches (`#plG` `#pxG`), vanilla projectiles in flight (none of the pack's enemies fires one:
cm arrows are `rlk_cmp` displays), particles and sounds (client side, already emitted).
**Lane VB's files** (not edited): `tools/build_mboss_hr_fx.py` has 8 gametime reads (`fx/e/world`, `fx/e/make`, the HUD line /
overlay clocks, the cue's 20-tick phase): see "Requests".

## Display interpolation in the slow motion (`beat/st/*`)
Fact read in the client (`net.minecraft.world.entity.Display`): `readAdditionalSaveData` calls
`setTransformationInterpolationDelay(getIntOr("start_interpolation", 0))` with force = true on EVERY load, i.e. on every
`data merge / modify entity` of a display; on the client that restarts the interpolation clock. Without a changed render
property (`RENDER_STATE_IDS` = translation, scale, both rotations, billboard, brightness, shadow radius, shadow strength) the
old from -> to pair is replayed from its start (a visible pop); with one, the new pair is "what is shown now -> the target".
So every write the beat makes to a display also changes `shadow_strength` (0.99 / 0.98 / 0.97 / 0.96, back to 1; displays with
a real shadow are skipped): the write then only re-times the motion in flight.
- 5, 8, 11 (after the world tick): for every world rig / projectile display (`rlk_mb_part`, `rlk_mb_pj`, `rlk_raiden_part`, `rlk_cmlink`, `rlk_cmp`, within 48 b)
  whose `interpolation_duration` is not the value the beat wrote last (`btD`): x3 (the next world tick is 3 ticks away).
- 5: `teleport_duration` 1..19 x3 (the client gets the move before the duration, so one world tick ahead); 11: back.
- 14 (or the beat's end): durations still stretched go back to their own value.
Not stretched: the kits' cards and other props (their scheduled worlds pose them after the pass; they step at 6.7 Hz for the
9 ticks), living
entities (the client's own 3-tick stepping smooths their position).

## The rocked-back attacker (generic) and the module hook
`beat/rock_on` (tick 2) / `rock_off` (tick 6, before the world's tick): rig parts that all stand on the anchor (registry bosses
`rlk_mb_part`, 나루카미 `rlk_raiden_part`, custom mobs `rlk_cmlink` of the attacker's `cmId`) get `tp ^ ^0.06 ^-0.2 ~ -16`: a
display's pitch tilts the whole model about its entity position (the feet), so the body rocks back 16 degrees and steps back
0.2 b; tag `rlk_bt_rk`, undone exactly. Registry bosses only when `mboss/d/beat_rock` says so (upright, man-sized: 파수꾼,
아를레키노, 타키, 홍련, the test bosses; registry `"rock": 0/1` overrides): 나비, 역장, 야타용왕 and 아펩 are not tilted (a long or
lying body would swing its far end; they still freeze and get the lightning). Core dispatchers `mboss/d/beat_parried` / `beat_release`
(registry flag `"beat"`, like `"bal"`): a module's own pose replaces the generic tilt when `beat_parried` returns 1.

## Proof (a)-(e) (`tools/dev/sim/cb/tests`: `test_cb.py` sections `beat` and `beatloop` = `test_beat.py`)
- (a) nothing changes without a perfect answer: the older sections of `test_cb` (251 checks: input, lock, judge, tiers, dodge,
  cool, context ...) run with `#btOn 0` and pass unchanged; every 홍련 / 아를레키노 / balance suite passes unchanged; with
  `#btOn 1` and no perfect answer `rlk:tick` pays 3 commands for the beat and `mboss/main` 1.
- (b) every later event exactly N ticks later: `beat` drives six scripted fights with the beat on and off (chains 10 / 3 / 2 t
  apart, mistimed presses over all tiers, dodge cooldowns 18 / 12, dodges of normal mobs): identical events on the beat's clock,
  real length = + 5 per perfect parry + 7 per perfect dodge. `beatloop_cb.py`: the three mid-bosses in the real framework,
  about 1600 world ticks each: every `# mb` score (framework, module, effect kit), the body, every hazard clock, both health
  pools and the dodge cooldown identical world tick by world tick; held 45 / 90 / 60 = 5 x 9 / 18 / 12; with dodges mixed in
  the two runs still agree. `beatloop_hr.py`: 홍련 in the suites' H1 world: gauntlet G1 (9 cuts, the closest 16 t apart),
  G2 (11 cuts, closest 14 t) and 900 ticks of the free P1 fight (25 perfect parries): the judged strikes, every `# hr` /
  `# mb` score, her body and both health pools identical world tick by world tick; held = 5 x the perfect parries.
- (c) no damage during a beat: melee, an undodgeable unparriable boss hit and a DoT tick on each freeze tick; boss strikes 4
  and 6 world ticks into a dodge beat; `beatloop` mixed policy: 0 health lost on untouchable ticks.
- (d) back-to-back: chains 10 / 3 / 2 t apart all perfect (the 3-t and 2-t strings need the input buffer: F during the hold
  counts on the release tick), seven beats in a row leave nothing, a perfect parry inside a dodge beat starts its own beat,
  the gauntlets' closest cuts (above).
- (e) exits: death, Ronova's revival wait, the selection space, the map, `#mbCine`, `#mbCam`, `rlk:load`, the lost player tag,
  each during a parry freeze and during a dodge slow motion (16 cases): on the next tick nothing is held (`#btK` / `#btHold` /
  `#btInv` 0, the mob has its AI back, a mob frozen before keeps its own NoAI, no tag, no marker, the clock keeps its lag); a
  freeze the player starts during the hold survives the release and loses the wrong "was NoAI" note.

## Cost against the budgets
- Idle (no beat running): `rlk:tick` + 3 commands (the clock test, `#now cb -= #btAdj cb`, the post test), `mboss/main` + 1
  (its first line), the cm and Raiden gates + 0 (conditions on existing lines), each effect-kit world + 2 while it has cards
  (the hold test, the lag), each kit `make` + 1. `test_scarlet`: P1 471 / P2 481 commands per tick as on the base tree's
  count (budget 830); `test_flow`: the whole fight 361, G1 385, G2 399; the player side (`perf_harness/pmeas.py`, late18):
  idle 688 -> 688, combat 692 -> 692, the F press 6 ticks 3 875 -> 3 877 (`beat/act`).
  `az/tests_cm test_m0diff` A (mid-boss tick cost against the 10-20 release; a relative budget of + 6.5 + lane C 1.2 that the
  tree already exceeded for three of the four: README 0-9) gets this lane's share `LANE_VP_CMD` 1.0 (the hold test):
  proto + 8.03 -> + 9.04, 파수꾼 + 7.16 -> + 8.17, 나비 + 8.27 -> + 11.67, 역장 + 8.76 -> + 11.88 (나비 / 역장: + their kits' lines).
- One perfect parry (17 ticks; measured in `test_cb`'s world, everything real): 1 500 commands with a rig character, 2 050
  with a mannequin character (the stand-in rig's 11 poses per tick), + about 175 for the generic tilt of a 29-part rig = about
  100 - 130 per tick while it runs. One perfect dodge (27 ticks): 1 900 / 2 700, + the stretch passes of a 29-part rig about
  1 150 (three passes, the teleport_duration pass and its undo) = about 110 - 145 per tick while it runs; its heaviest single
  tick is tick 5 (the clip start + the first passes: about +700).
- The worst sustained case is a gauntlet answered perfectly: G2 = 11 beats in 282 world + 55 held ticks: (399 x 282 + 11 x
  2 200) / 337 = about 405 commands per tick with parries, about 440 with dodges (11 x 3 850 over 359 ticks) - half the 830
  budget. A held tick itself is cheap: the world costs 1 command (`mboss/main` returns), only the player side runs.
- Atlas: 12.940 M -> 13.089 M px (the 31 half-resolution hot sprites + two glow cards; limit 13.2 M). Fonts are not in the atlas.

## Client facts verified in the bytecode (javap, `<S>/cb/vp/bc`)
- `Display.readAdditionalSaveData` / `setTransformationInterpolationDelay(.., true)` / `tick()` / `RENDER_STATE_IDS` (above).
- `BakedQuad$MaterialInfo.of(Material$Baked, Transparency, ..)`, `lightEmission`, `TextureAtlasSprite.transparency()`: item quads
  pick their render type from the sprite's own transparency and carry a light emission (the glow shell / cards blend and glow).
- Fonts: `client_facts.md` 7 (the lead's): cell > 256 px -> missing glyph.
- `DisplayRenderer.calculateOrientation`: a FIXED display is drawn with `rotationYXZ(-yaw, +pitch, 0)` of its ENTITY rotation:
  the entity's pitch tilts the whole model about the entity position (the generic rocked-back tilt: pitch -16 = the top goes
  away from the facing).

## Pack files (all written by generators in git)
- `assets/rlk/font/cb.json`, `assets/rlk/textures/font/cb/{streak_0..3,tint,vig,star,spark,bolt_1..3,burst,glint_l,glint_r}.png`
  (replacing streak / streak_s / wash / star / glint) — `tools/build_combat_fx.py --resourcepack`
- `assets/rlk/textures/player_motion/weapons/<31 sprites>_hot.png` (the sprites of the five glow models at half resolution,
  pushed to yellow-white) + `wglow_blade.png`, `wglow_orb.png`, 33 atlas entries (items atlas 12.940 M -> 13.089 M px);
  `assets/rlk/{models/item,items}/player_motion/weapons/{spear,scythe,sword,cryo_sword,navia_halberd}_glow.json`;
  `assets/rlk/models/item/player_motion/wg/{blade,orb}.json`, `assets/rlk/items/player_motion/wg/{iron_sword,diamond_sword,netherite_sword,orb}.json`;
  every `assets/rlk/{models/item,items}/player_motion/<7 characters>/<10 parts>.json` (tintindex 0 + the custom_model_data tint)
  — `node tools/build_player_rig.mjs --datapack . --resourcepack <RP>`

## Requests to other lanes
- **VB** (`tools/build_mboss_hr_fx.py`): put her kit on the beat's clock like the other six: after each
  `execute store result score <X> <OBJ> run time query gametime` add `scoreboard players operation <X> <OBJ> -= #btLag cb`
  (8 places: `fx/e/world`, `fx/e/make`, the HUD line / overlay clocks, the cue phase), and as the second command of `fx/e/world`:
  `execute if score #btHold cb matches 1 run return run schedule function rlk:boss/scarlet/fx/e/world 1t replace`. Without it her cards keep running
  while she is frozen and a timed card (the new blade path's head) arrives 5 / 7 ticks before its hit after a beat.
- **VB** (optional): her own rocked-back pose instead of the generic tilt: registry entry `scarlet` gets `"beat": 1` and the
  module two functions, `boss/scarlet/beat_parried` (as the body, at it, 2 ticks after the contact; return 1) and
  `boss/scarlet/beat_release` (4 ticks later, before her tick).
- **Lead**: `tools/dev/sim/hr/tests/ident_hr.py` has this lane's allow group (`LANE_VP`, also in `ALLOW_GONE`); the other
  lanes will add theirs next to it. The resource pack's own README (font table: `rlk:cb` is now U+EE00-EE0D + two spaces
  U+EE1E / EE1F) is the lead's at the release.

## Log
- 11-11 start; baseline suites on the untouched tree all pass (test_cb 296, test_np 125, test_rm, test_bal 117, test_bal_boss
  117, test_input_hr 17, test_metro 30, pat_p1 559, pat_p2 70, pat_ghost 65 ...).
