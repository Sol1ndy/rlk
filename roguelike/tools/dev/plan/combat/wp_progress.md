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
- [ ] 4 README 2 / 3 / 12-1 / 0-x, gates, commit, push  (in progress)
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

## Item 3 — the dodge set (the old dash removed)
Reference `dodge.mp4` (input log parsed per frame, frames read on the floor grid): a plain dodge is a quick low hop-step,
12-15 frames of motion (4-5 ticks), ≈ 0.5-1 body heights (≈ 0.9 b) in the input direction, standing again by ≈ 30 frames;
a second press 3-26 frames (1-9 ticks) after the first chains the double dodge (log `SHIFT→SHIFT 더블 닷지`, 13 of 13
seen), an aerial cartwheel / side flip, inverted 24-34 frames after the second press; the perfect dodge triggers from
either. Built: `player/dash` (first press: step, cooldown 18 = #dashCoolT) → `player/dodge/again` (a press inside the
cooldown, 1..#dgChW = 10 world ticks after the set's first stamp, not a held F5 repeat: the second move, a new stamp, cooldown
+ 18) → `player/dash_go` → `player/dash_dir` (direction = move input else look, as before) → `player/dash_move_tick` with
`player/dodge/speed` (step 0.5 / 0.3 / 0.2 b = 1.0 b in 3 t; second move 0.25 / 0.4 / 0.4 / 0.35 / 0.25 / 0.15 = 1.8 b in 6 t;
the old dash: 1 b × 3 t). Windows unchanged (perfect 0-2, loose 3-6 for normal / elite), one refund per stamp, energy once
per stamp. Avatar: rig characters clip `dash` (the hop-step, 6 t) / `dash2` (the cartwheel, 9 t); the mannequin characters
crouch for the step (vanilla mannequin pose `crouching` until box_end, verified VALID_POSES in the bytecode) and play dash2
on the stand-in rig (`lite/f`).

## Dash dependents checked (and what became of them)
(see README; filled in step 5)

## Requests to other lanes
- none yet

## Pack files
- none changed (no new textures; clips are display transforms only)

## Log
- 11-12 start (base origin/wip/w 540f5f68c, merged f4187dbd3 for §4-§5). Baseline suites on the untouched tree: test_cb
  383, test_np 125, test_rm, test_bal 117, test_bal_boss 117, test_input_hr 17 (the later ones of that run read a tree
  that was being edited and do not count).
