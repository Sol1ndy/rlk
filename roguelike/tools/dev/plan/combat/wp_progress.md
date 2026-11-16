# Lane WP progress (wip/w-player) — parry sounds, the faster perfect dodge, the dash replaced by the reference game's dodge set (round W)

Worktree `<S>/cb/wt_wp` (branch `wip/w-player`, base `origin/wip/w`). Scratch `<S>/cb/wp`: `sim` = copy of `tools/dev/sim`
with the paths rewritten (`mksim.sh`), `suites.sh <dp> <tag>` (output `out/<tag>_*.txt`, summary `out_<tag>.txt`), `snd/`
(`mix.py` = an offline renderer of playsound stacks from the real vanilla files with the client's gain / pitch rules read
from the 26.3 bytecode; `try2.py <stack file>` prints the envelope), `mc/` (the official asset index + sounds.json of 26.3,
the downloaded .ogg / .wav of ~150 candidate events: untrusted data, read with `-I`), `aud/` (the recordings' audio),
`ref/` (reference frame sheets), `dbg/` (the beat clips' debug datapack for `beat_sheet.py`). Pack copy `<S>/rp_wp`
(from `rp_rel3`). Contract: `w_brief.md` §1, §2 "WP", §4 "WP, changed" (the dash is removed entirely), §5 (trailer).

## Steps
- [x] 1 parry sounds: analysis (reference + t3) and new layered stacks for tiers 1 / 2 / 3 (+ the boom, the release); the
      perfect dodge's and the plain dodge's sounds in the same pass
- [x] 2 the faster perfect dodge: beat ×1/2 on 4 world ticks (holds 1 · 3 · 5 · 7), the flip at once (0-7), ready on 10,
      over on 14; the stretch passes ×2; clips; suites' expectations (test_cb beat / fx, beatloop_cb, test_vi)
- [x] 3 the dodge set (the dash is gone): plain step 1.0 b / 3 t, double dodge (second press 1..10 t later: aerial
      cartwheel 1.8 b / 6 t, new stamp, cooldown + 18), perfect dodge = the beat; clips `dash` (rewritten) / `dash2` (new)
      for all seven characters; held-F5 repeats never chain the double; hrsim / test_input_hr model; test_cb `double`
- [x] 3b (review T3-02/03) the dodge moves by context: twist / lunge-step / back-step on an avoided hit / cartwheel
- [x] 3c (review T3-05 / T3-07 / T3-10) tier sparks bigger, coloured, beside the head; star above the head line; tint warmer
      and half as strong; bolts 1.5x with white-yellow dust; weapon glow hotter and re-applied on beat ticks 1-2; guard whoosh
- [x] 4 README 2 / 3 / 10 / 12-1 and the rig notes; checkpoint a68b795d2 pushed
- [x] 5 (w_brief §6) the whiff ladder removed: press = #parGap 12 always, any parry #parChain 1; test_cb lock / test_input_hr /
      hrsim notes; README 3; c_progress / fa_progress notes
- [x] 6 (the user: chains parryable in full) the rule checked in the core (nothing to fix: every tier -> par_use = #parChain 1;
      the beat stamps presses on the combat clock; the dodge never blocks F); test_cb lock gains the chain lemma; new
      tools/dev/sim/cb/tests/chainparry.py (every pattern of 7 bosses + 홍련's chains / gauntlets)
- [x] 7 gates on the final tree, the suites, test_metro / hrfair numbers without the ladder, commit, push, report
- [ ] 5 dash dependents: the list below checked in the code; balance sims; final gates; report

## Item 1 — sounds (what was measured, what is built)
Reference (`parry.mp4` audio, 50 ms bands, dBFS of the recording): perfect parry — swing whoosh −10..0 frames, the clang at
0..+2 frames (−33 dBFS, broadband), then a brighter ring +7..+25 frames at −30..−31 dBFS with partials 1.97 / 2.2-2.3 / 2.6 /
3.26 kHz, linear decay to ≈ −44 dBFS at 0.8 s (≈ 0.75 s in all); the normal guard: −34..−36 dBFS for ≈ 0.3 s, energy at
3-6 kHz (a "tink", not a tick). Ours in t3 (perfect parries at 78.1 / 83.3 / 154.0 / 183.4 s): the contact burst reaches
−34..−36 dBFS for 0.1 s and is down 10-15 dB by 0.15 s; the ring is lost (−45..−50 dBFS; the amethyst chime file is at
volume 0.2, the resonate at −35 dB peak), i.e. thinner and shorter than the reference and quieter than her swings
(the fight's loudest moments −28..−31 dBFS). Rendered offline (`snd/mix.py`, same files, gain clamp(vol × file vol, 0, 1) ×
(1 − d / (16 × max(vol, 1))) at the 4.5-b camera distance, pitch clamp 0.5..2 = playback speed):

| rendered, dB (relative) 0-50 / 100-150 / 300 / 550 / 800 ms | before | after |
|---|---|---|
| perfect parry | −33 / −45..−49 / −38 / −37 / −45 | −22 / −21..−24 / −26 / −42 / −54 |
| tier 2 | −43 / −63 / gone | −28 / −36..−40 / −55 |
| tier 1 | −43 / −73 / gone | −31 / −44..−50 / −70 |

(After: the perfect parry is 11 dB louder at the contact and its body lasts 0.3 s at full level, tier 2 ≈ 6 dB under it,
tier 1 ≈ 3 dB under tier 2; both blocks ring ≈ 0.25 / 0.15 s instead of a 50-ms tick.) Stacks: README 3 「효과」.

## Item 2 — the perfect dodge (real ticks, 0 = the trigger)
Before: hold 1, full speed 2-5, ×1/3 on 6-14 (holds 6 7 9 10 12 13), flip clip started on 5 (two arms up through the slow
motion), the handspring 14-21, ready 26, over 27, N = 7. After: hold 1 · 3 · 5 · 7 (×1/2 from tick 1 to 8: world ticks on 2
4 6 8), untouchable 1-11 (the same 7 world ticks as before), the clip `pdodge` starts on tick 0: launch (knees loaded, arms
thrown back) → 60° a tick backward → apex inverted on 3 → first foot down on 6 → landed facing the attacker on 7 (tint off,
landing sound) → the landing taken low on 8 → ready stance on 10 → over on 14, N = 4. The world displays' interpolation is
stretched ×2 (passes on 0 2 4 6, teleport_duration on 0 / back on 6, all back on 8). Contract kept: the clock list, the
gates, untouchable, the input buffer, proofs (a)-(e) in `test_cb beat` / `beatloop_cb` / `beatloop_hr` / `test_vi`.

## Item 3 — the dodge set (the old dash removed; w_brief §4 "WP, changed", review T3-02 / T3-03)
Reference `dodge.mp4` (this lane: the input log parsed per frame, frames on the floor grid; the reviewer: floor-compensated
tracks, `review/w/findings_fight.json` T3-03): no attack, no direction -> in place (< 0.3 bh), a twist with an arm flung out,
~12 frames; an attack incoming -> a straight upright back-step away from the enemy, 1.9-2.2 bh, 5-12 frames, arms spread on
landing; a direction held -> a low lunge-step that way, ~1.4 bh, 20-25 frames; a second press 3-26 frames (1-9 ticks) after
the first -> the double dodge's sideways cartwheel (20 frames, ~1.3 bh more); no slow motion / tint / sound on a plain
dodge. Built (`player/dash` -> `player/dodge/again` -> `player/dash_go` -> `dash_dir` / `dodge/len` / `dash_move_tick` +
`dodge/speed*`, `player/dodge/away` from `player/def/dg_refund`):

| move (#dgMv) | when | travel | clip (rig) | mannequin |
|---|---|---|---|---|
| 1 twist | first press, no direction held | 0.4 b / 3 t forward (0.2 0.12 0.08) | `dash` 6 t | crouch |
| 3 lunge-step | first press, moving / F5 input held | 1.6 b / 5 t that way (0.5 0.4 0.35 0.2 0.15) | `dash_l` 10 t | crouch |
| 4 back-step | the stamp avoided an attack (perfect / loose / 홍련 pip query), once per stamp | 2.7 b / 4 t straight away from the attacker (0.9 0.8 0.6 0.4) | `dash_b` 8 t facing the attacker (not over pdodge / dash2) | crouch |
| 2 cartwheel | a second press 1..#dgChW (10) world ticks after the first, not a held F5 repeat, once per set | 2.2 b / 6 t (0.3 0.45 0.45 0.45 0.35 0.2), after a back-step in its direction | `dash2` 9 t | stand-in rig `lite/f` |

Windows unchanged: perfect 0-2 t (every class), loose 3-6 t (normal / elite); every move is a stamp (its own windows, refund,
energy). Cooldown 18 / 12 after an avoided attack (질주 2: 14 / 10); the cartwheel adds 18 (a set = 2 windows per 36 t, the
old rate). The old dash: 3 b / 3 t every time (1 b a tick), a flat "superman" pose.

## The whiff ladder (w_brief §6) and the chain guarantee
- Removed: `#parWs` / `#parWsMax` / `#parWsT` / `#parWsClr` (load, press, par_use, reset). Every accepted press locks `#parGap` 12;
  a parry of any tier sets the lock to `#parChain` 1 (par1 / par2 / par3 -> par_use); a refused press still blocks every F for
  `#parRe` 3 (A-01 (1) as fix A built it, `#parMl cb`).
- What the ladder guarded, measured without it (test_cb `lock`): blind F at a fixed period gets a press in once per 12 t, so at most
  3 / 12 = 25 % of the ticks are in a perfect window (period 3 t is the worst: 25.0 %, a strike would still do 38 % of its damage);
  against 229 real strikes (20-60 t gaps): F every 4 / 12 / 13 t = 20.1 / 20.5 / 21.4 % perfect, 42 / 38 / 44 % of the damage taken
  (with the ladder: <= 7.6 % / >= 79.8 %). test_metro / hrfair: see the gate results below.
- The chain lemma (test_cb `lock`): 135 chains (fixed gaps 1-40 and 120 random), the ideal press (h - 1, or h after a 1-t gap):
  every hit perfect, no press refused; after a tier-1 / tier-2 parry of the first hit every later hit still perfect; F while
  the dodge cooldown runs and a step / double dodge moves: every press taken. The beat: test_cb `beat` (b) chains 10 / 3 / 2 t
  apart with the beat on (presses during a hold count on the resume tick).
- `tools/dev/sim/cb/tests/chainparry.py` (the ideal parrier through the REAL f_key in hzlog's boss worlds and 홍련's H1 world, two
  passes until the hit set is stable): 117 patterns (106 with 2+ parryable hits), **624 / 624 parryable hits perfect, 0 presses
  refused**; per boss (patterns / parryable hits / smallest gap): 파수꾼 8 / 19 / 13 t, 나비 9 / 51 / 18, 역장 9 / 90 / 6, 야타용왕 20 /
  99 / 4, 아펩 14 / 41 / 13, 타키 12 / 91 / 10, 아를레키노 21 / 154 / 10, 홍련 chains 22 (11 keys x 2 phases) / 59 + G1 9 / 9 (16 t) +
  G2 11 / 11 (14 t). Unparriable hits of the same runs (dodge-only) counted apart. Not simulated: 나루카미 and the custom mobs (no
  simulator of their AI in tools/dev/sim) - covered by the lemma.
- test_metro without the ladder (the lead decides; the ladder is not brought back): G1 (a8) is cleared (5+ perfect) by mashers of
  period 4 and 6 t (6 perfect); 12 / 15 / 18 / 19 t reach 4. G2 (a13) is cleared by periods 13 / 15 / 16 t (5) and mashers 3 / 7 t
  (5) and 4 t (6). test_metro's 4 checks fail for that reason (reported, not changed).

## Dash dependents checked (and what became of them)
| what read the dash | where | now |
|---|---|---|
| item hooks on_dash / on_dash_move (키리온 marks, 고통 & 절망, 열혈 저울, 선학의 깃, 생명줄, tutorial counter) | `items/hook/on_dash*` | once per move (a double dodge = twice, at the old rate: each move costs 18 t of cooldown); on_dash_move every moving tick of a move. Shorter paths: fewer enemies passed |
| 질주 (2) cooldown −20 %, (4) wind damage to enemies passed (2.2 b round the body each move tick) | `engravings/dash/regen`, `engravings/dash/hit` | (2) unchanged (14 / 10); (4) unchanged radius, shorter path (README 12-1 updated) |
| 질주 (1) move speed +5 % | `stat` | unaffected |
| room traversal (gaps, steps) | `dash_sub` / `dash_up_*`, `room/fall/*` | doors are reachable on flat floor from every zone (README 10): nothing needs the dash; the one-block step-up per move stays; the safe-spot marker still skips moving ticks |
| knockback / DoT immunity while moving, `mboss/mv/lv_sample`, `mboss/push/capsule`, `view/move`, `combat/request`, `loco/observe`, 클로린드 auto fire, 나비아 aim, burst / fall / map resetting dashMoveT | many | read `dashMoveT` only: unchanged (moves last 3-6 t, as the dash's 3) |
| the rig dash clips (arle / skirk / navia `dash`, 나비아's fx + audio) | `tools/player_motion/{arle,skirk}.json`, `navia/dash_sheathe.json`, `navia_audio/dash.py` | removed; `dash` / `dash_l` / `dash_b` / `dash2` generated for all seven from `beat/clips.json` |
| the dash sound (wind_charge burst + breeze slide, −20..−30 dBFS in t3, louder than the parries: T3-10) | `player/dash_go` | `player/dodge/snd_step` (leather + a quiet slide) / `snd_flip` |
| the balance sims | `hr/tests/lib/hrsim.py` (hrfair2, test_bal_hr, pat_*, test_metro) | model the cooldown, not the travel (the player stands): the double dodge added to the cooldown model; targets unmoved (test_bal_hr / pat_* results below) |
| old fair sims of the chapter bosses (`mb3/fgfix`, `tk/review`, `ap/balance`, `tele/fg`, `mb2/balance`) | not gated | model the pre-11-10 dash (charges, i-frames, 3-b escape) — already out of date since 11-10; not changed (listed for the lead) |
| boss fairness that assumed dash travel | hazards | every hit goes through the judge (windows + the start-spot box `rlk_dgo`); escaping an area without timing now needs walking or the back-step after an avoided hit |

## Requests to other lanes
- none yet

## Pack files (all written by generators in git; no new texture, same sizes: items atlas 13.108 M px unchanged)
- `assets/rlk/textures/font/cb/tint.png` - `tools/build_combat_fx.py --resourcepack` (warmer, half the cover)
- `assets/rlk/textures/player_motion/weapons/<31 sprites>_hot.png` - `node tools/build_player_rig.mjs` (90 % yellow-white, alpha 235)
- the rig's item models / clips are datapack functions (display transforms): no pack change for the dodge clips

## Log
- 11-12 start (base origin/wip/w 540f5f68c, merged f4187dbd3 for §4-§5). Baseline suites on the untouched tree: test_cb
  383, test_np 125, test_rm, test_bal 117, test_bal_boss 117, test_input_hr 17 (the later ones of that run read a tree
  that was being edited and do not count).
- 11-12 checkpoints a68b795d2 (sounds, faster perfect dodge, dodge set v1), 9a0218329 (dodge by context, parry visuals, ladder
  removed), merge 07f7de0bd (w_brief §6), then the final commit (chainparry, suites, docs).

## Gates on the final tree (11-12)
- Generators twice in the release order (scarlet rig, hr fx, bossbar, combat fx, player rig, player audio, blank tex, regen_all
  --mobs, bf / fg fx): tree 1c7fb1e2a after both rounds, pack hash df5f66cc both rounds. check_mboss_pack 0, rplint 0, items
  atlas 13.108 M px, loadcheck wpg2: 0 function load failures, Done, 1871 advancements.
- Suites (copy of tools/dev/sim): test_cb 400/400 (double 17, lock with the chain lemma, beat, beatloop), test_np 125/125,
  test_rm, test_bal 117, test_bal_boss 117, test_input_hr 19/19, pat_p1 559, pat_p2 70, pat_ghost 65, test_flow 40, test_bal_hr
  79, test_vi 208/208, ident_hr (group LANE_WP), test_scarlet 48, chainparry 624/624 (0 exceptions). test_metro 15/19: the four
  metronome checks fail because the ladder is gone (reported above, the lead decides).
- hrfair2 `--only g,chain` (3 seeds): T5 40.3 / T5b 49.3 PASS; T6 s0 100 % perfect, 100 % cleared; T6 s1 87.9 % (101 % of the
  86.6 ceiling) / 100 % in the window, 100 % cleared; **T7 sloppy 0 %, masher (F every 4 t) 50 % (G2 cleared in all 3 seeds,
  G1 in none), dodger 0 % (0 damage) - miss on the masher** (the ladder's job); T13 53 / 53 perfect, 0 refused PASS.

