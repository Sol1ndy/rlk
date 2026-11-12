# Requests from S2-S (transitions + sequences: trans.py, seq.py, h_ps.py; branch wip/az-ps)

Protocol: s2.md 13 / 18.6. Append-only.

## Rps-1 api: g.wave passes the front preset sizes x 100 (blocks converted twice)
- what: `api.Gen.wave` calls `self.fxe('front', el, r0=int(r0 * 10), r1=int(r1 * 10), w=int(band * 10), dur=n)`, but
  `K.fxe` converts blocks to tenths itself (`K.fxe('front', 1, r0=4.0)` -> `{r0:40}`), so every N10 front was drawn at
  ten times its size (T1 wave 1: `fx/p/front/<el> {r0:400,r1:1800,w:350}` = a 40 -> 180 b front for an 18 b hazard).
  Under Change note 1 the travelling front is the only visual of these hazards (P2, P5, P5b, T1, the Cryo rings), so
  the drawn front must equal the hazard. Fix: pass blocks (`r0=r0, r1=r1, w=band`).
- why blocked: T1's fronts (the landslide's only hazard visual) were wrong; the S2-S suite checks the front args
  (`pat_trans.py slide`: r0 40 / r1 180 / 300 tenths).
- local change on wip/az-ps (smallest edit, marked `# REQ ps-1` in `tools/mboss_azhdaha/api.py` Gen.wave). I2a: keep it
  (S2-A / S2-B / S2-T hit the same line; their suites should check the front args too).
- status: open (applied locally in wip/az-ps 44f09b8)

## Rps-2 api: the re-export line of h_ps.py
- what: s2.md 1 says api.py re-exports every stage helper (`from .h_<stage> import *`, "S1-MOD already wrote"), but
  api.py on wip/az only has `from .h_core import *`. trans.py / seq.py import `h_ps` directly, so nothing is blocked; add
  `from .h_ps import *  # noqa: E402,F401,F403` after the h_core line at I2a if the re-export is wanted.
- status: open (not blocking; no local change)

## Rps-3 core: the phase-2 brand banner replaces the absorb banner 13 t early
- what: absorb 1 shows `banner_ab` at its burst t47 (held 60 t, to t107); `svc/phase_2` (called at t94 as plan 5 T2
  says) shows `banner_brand` at once and cuts it. Plan 4.4 says the brand banner shows "when gameplay resumes after
  absorb 1": suggest moving `F('svc/banner_brand')` out of `svc/phase_2` into a `g.banner('brand')` call that S2-S makes
  at the roar (t114, cine end), or delaying it in the core by 20 t.
- status: open (cosmetic; no local change)

## Note (no request): the landslide yaw (R3a report)
- The landslide clip has no yaw schedule and its feet stay planted, so trans.py turns the anchor only in the lead
  (service ticks 0-39: the walk to the centre, or a step-turn in place with the walk clip when already there, <= 4 deg/t)
  and keeps the yaw fixed from the clip start (#azNoTurn every tick). No rig change needed. A 180-degree turn from the
  centre leaves <= 24 degrees uncorrected (the fronts are radial, nothing depends on it).
- A /reload in the middle of the landslide respawns the rig in idle (the rig cannot start a clip mid-way): the remaining
  waves keep their sounds, the jump cue and the bell but lose the lift poses. A `play_at {clip,t}` rig function would fix
  it (R3b / RIGLIB; not requested: /reload is a dev action).

**I2 status (2940a23 on wip/az).** ps-1 served once with pa-1. Rps-2 served (api re-exports h_ps). Rps-3 served (brand banner at absorb 1's roar t114 + its reload + test/p2, removed from svc/phase_2).
