# Requests and notes from AP-P3 (phase-3 patterns Q1-Q5 / Q3s + Q2, `tools/mboss_apep/{p3,aftermath}.py`, branch `wip/ap-p3`)

Protocol: `S:ap/ap_contract.md` §0.11 (append-only, `## R<stage>-<n> <type>: <title>`, what / why / needed by, status).
AP-P3 owns only `p3.py` and `aftermath.py` (+ their generated `AP:p/{mstrike,shells,tail3,spiral,surface,aftermath}/**` and
`AP:dome/**`); everything below is for the owners of the core, the kit, the rig or the org models (I2 integrates).
Suite: `S:ap/tests/pat_p3.py <dp>` (exports `TABLE`); storyboards `S:ap/renders/ap-p3_{q1,q4,q5,q2}.jpg`.

## RP3-1 request (core / api): `Gen.yaw_rebase()` — re-base the running yaw schedule on the body's current facing

- what: `AP:yaw/rebase` (as the body): `#apYaw0 = Rotation[0] x 100 - #apYawSg x schedule[#apYawT]`, and `Gen.yaw_rebase()`
  returning its call line. The yaw driver (`AP:yaw/tick`) then holds the new facing for the rest of the clip.
- why: `move_strike_p3` carries a yaw schedule from t0 (0 until the whip spin 66-72), so the driver overwrites any turn the
  pattern makes. Q1 must surface facing the player (the body is placed at t38 at `L - 2.59 f`, f = from the burst point
  toward the player, so the clip's burst point lands on the locked point and the roll / slam / whip follow f). Meanwhile
  `p3.py` (`p/mstrike/place`) writes the one line `execute store result score #apYaw0 mb run data get entity @s
  Rotation[0] 100` itself (correct because the schedule is 0 at t38), marked `TODO(I2)`.
- needed by: AP-I2 (switch the line to `Gen.yaw_rebase()`). status: open.

## RP3-2 request (core): the Q2 two-segment countdown on the under-bar

- what: while `#apPid 32` runs, the core's `hud/bar` shows the plan's two-segment countdown (plan 8.3 Q2 B0): red until the
  blast, then gold until the dome pop. The pattern provides `#apq32` (the aftermath clip tick; negative during the
  approach, `#apq32S` = the pattern tick the clip starts on): red = `#apq32` from `-#apq32S` to 156, gold = 156 to 189.
- why: `hud/bar` is the core's bars hook (it overwrites `#buSub*` every tick); the pattern cannot draw it. The real
  game's banner (kit `hud/banner_aftermath`) is shown from B0 to t156 by `aftermath.py`.
- needed by: AP-I2. status: open.

## RP3-3 request (fx): a sliced `p/flood`

- what: `p/flood {life}` draws its 44 tiles in one call, about 3.3 k commands in the sim (the whole Q2 blast tick 3.37 k,
  over the plan's 3000-per-tick budget, plan 12.3 perf probe). A sliced variant (e.g. `p/flood {life,part}` drawing a
  third of the cells per call, or the tiles spread over 3 ticks by the kit's ager) lets Q2 call it on t156 / 157 / 158.
- why: the per-tick budget; nothing else in Q2 is above 2 k (the dome pops are already spread over t189-191).
- needed by: AP-FIX (perf). status: open.

## RP3-4 note (core / org): the dome models are stepped by `aftermath.py`

- what: nobody runs `om/objects_tick` yet (requests/org.md RORG-3), so `aftermath.py` calls `function AP:om/dome/tick`
  itself while the domes stand (aftermath t54-195). If the core adds `om/objects_tick` (Heart, domes, stalks, walls) to
  the module tick, drop that line from `p/aftermath/tick` (else the dome clips step twice per tick).
- needed by: AP-REV / AP-I2. status: open (informational).

## RP3-5 note (rig, fidelity): `tail_p3` swing 2 never sweeps the space in front of the boss

- what: `api.wedges('tail_p3', 46, 53, 12)` (the manifest's tail track x the yaw schedule) sweeps the tail line from -57 to
  -176 degrees of the start facing (left side to behind), while swing 1 sweeps -83 to +38 (left through the front). The
  lunge 36-40 moves the body toward the player, so a player in front of the boss is never inside a swing-2 lane
  (`S:ap/renders/ap-p3_q4.jpg`, panels t38 / t50; pat_p3 5e / 5f). Plan 8.3 Q4 reads "swing 2 the same reversed ... standing
  at the body during swing 2 is unsafe (the lunge)".
- why: the wedges must follow the manifest (plan 7.11 rule 3), so the pattern cannot fix it; whether the footage's
  reverse swing (V6W §2.2, 3.10-5.65 s) comes back across the front is for the rig owner / AP-REVIEW (fidelity).
- needed by: AP-REVIEW / the rig owner. status: open (no change made).

## RP3-6 note (fx / I2): the keep decals of Q1 / Q3 / Q3s are called through `Gen.decal('keep', K.tele_disc(...))`

- what: the three keep rows (Q1 rosette ring r 4.2 at t32, Q3 target ring `tele/mring` 10-33 + the held disc r 3.6 at lock
  1, Q3s leaf ring r 3.6 at t26 and the disc r 3.0 under the player at t36) use today's filled `tele/disc`; RI1-1
  (requests/fx.md: the outline-only form) switches them by one keyword at I2. Every other phase-3 hazard is quiet with no
  decal; the resume hooks (`p/{mstrike,shells,surface}/resume`) redraw a pending keep disc with the ticks left after a
  pause (the core's pause hook clears the kit telegraphs).
- needed by: AP-I2 (with RI1-1). status: open (informational).

## RP3-7 note (no-tips rule): what Q2 shows

- what: dropped the plan's sub-line "보호막이 사라질 때까지 기다리세요" (blast -> pop): it tells the player what to do and is
  not in the footage. Kept: the real game's banner (kit `hud/banner_aftermath`, v5 18.2 s / w1) and, after the first
  (non-lethal) cast only, `TXT['q2_lethal']` "다음 종말의 여파는 치명적입니다 — 보호막 안에 머무르세요" (contract §2.5 lists it
  as an instant-kill warning; its second clause is advice, so it is listed as **unsure** for the user). No other text.
- status: informational.

## RP3-8 note (core): the hit sounds read `#mbHitEv` without clearing it

- what: Q4 (`p5_hit` + `hud/flash_hit` on a tail hit) and Q2 (`q2_tick` on a landed field tick) compare `#mbHitEv` with a
  copy taken at their start (`#apq34H`, `#apq32H`) instead of clearing it (cm.md 13.3 lets the module clear it; no other
  Apep reader exists today). If the core starts clearing `#mbHitEv` in its tick, it must do so after `p/run`.
- status: informational.

## AP-I2 status (2026-10-21, `wip/ap` f588262; plan §14 "AP-I2 integrate", contract §3)

- RP3-1: done f588262: `p/mstrike/place` calls `Gen.yaw_rebase()`.
- RP3-2: done f588262: core `hud/bar_q2` / `bar_q2g` (bossui code 2 to t156, code 8 to t189; test_apep 11f).
- RP3-3: done f588262: kit `p/flood_part {life,part}`; Q2 draws it on t156 / 157 / 158 (blast tick 3373 -> 1883 commands).
- RP3-4: done f588262: aftermath's `om/dome/tick` dropped (the core's `obj/tick`).
- RP3-5: open (not served): for AP-REVIEW / the rig owner (fidelity of `tail_p3` swing 2).
- RP3-6: done f588262: `tele/disc_o` for Q1 / Q3 L1 / Q3s and `redraw_fn`.
- RP3-7: informational; `q2_lethal` stays, listed as unsure for the user.
- RP3-8: informational; the core still never clears `#mbHitEv`.
- Also (RP1-3): Q4's wedges are `api.wedges(..., swept=True)` (28 / 116 missed sample points of the bare wedges, 0 now).

## AP-FIX status (2026-10-22)

- RP3-5 served (82943f2 + d57f9ab): `tail_p3`'s swing-2 yaw schedule re-keyed (the body unwinds to face the player during the
  S-coil, swing 2 sweeps from about +75 to −70° across the front) and the Q4 lunge stops 4 b short of the player; pat_p3 5g.
- RP3-7 (no-tips, unsure): unchanged; `q2_lethal`'s second clause is listed for the user.
