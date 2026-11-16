# Requests of S2-B (geo_b.py: P5, P5b, P6, P7, P8, P9) — s2.md 13 / 18.6, append-only

## Rpb-1 kit: outline-only tele/disc for the P9 rock rings
- filed in requests/fx.md (Rpb-1, = Rpa-2's `fill` argument / `tele/rim`); not blocking (rim + fill over tell 19 now).
- status: open

## Rpb-2 core (framework hz option, optional): a tangential knockback direction for P7's swept wedges
- what: plan 5 P7 asks "KB tangential 4" (`api.KB['p7_tan']`). Framework hazards push away from the origin
  (`#hzKBDir 0`) or along the aim (`1`); a sector's aim is its mid direction, so neither is tangential. geo_b.py uses
  `#hzKBDir 0` (away from the tail root, 4) for the wedges and the root discs. A `#hzKBDir 2` = "the aim turned 90 deg
  toward #hzKBSide (1 / -1)" in `hz/init` + the KB step would give the swept direction (the player flung along the
  sweep). AZ-CM is released, so this is an S1-CM / I1-WIRE decision; nothing in geo_b blocks on it.
- needed by: P7 (fidelity only; damage and timing unaffected).
- status: open

## Rpb-3 rig (R3b, poses only, optional): stomp_* — make the paw lift visible from the `lift` event
- what: in `stomp_fl/_fr/_hl/_hr` the slamming paw's column top rises 0.04 b over t0-5 and 0.38 b at t6, so the visible
  lift starts at t6 = 11 t before w1 (17); Change note 1 counts the 12-t floor from the motion tell (geo_b plays a step
  sound at `lift` 5, so the tell is 12 t with the sound). Moving 0.15 b of the lift onto t4-5 (no event or length change)
  makes the pose itself carry the 12 t, as stomp3 already does (s1 4, s2 25, s3 48: 13 / 15 / 15 t).
- needed by: P5 readability; pat_geo_b.py accepts the lift up to one tick after the `lift` event.
- status: open

## Notes for the other S2 authors (no request)
- Addon contexts set by the hosts (S2-L / S2-T bodies): stomp/w1, stomp/w3, stomp3/s1, stomp3/s3 at the paw point,
  rotated toward the player (`#azCtxYaw` = that rotation, `#azCtxPaw` = the paw 1-4, `#azCtxGrp` = the wave's group,
  `#azCtxSide` = `#azSide`, `#azCtxT` = E); whip/sweep at the tail root of t23 (start frame), rotated as the start
  facing, `#azCtxA0` / `#azCtxA1` = world yaw (int) of the tail line at t23 / t31, **continuous** (A1 - A0 = +114 for
  the left whip, -114 for the right; not normalised), `#azCtxGrp` = the whip's group; whip/end at the tail root of t31,
  rotated along the end line (`#azCtxYaw` = its world yaw); tailslam/impact at the tail root (f -4.75), rotated straight
  back (`#azCtxYaw` from the context marker).
- P5 / P5b use kit wave ids 5 / 6 / 7 (`tele/wave`) for their three fronts; an addon front running in the same ticks
  (the Cryo ring in w1's / s1's group) should take another id (0-4).
- geo_b.py imports its helpers as `from . import h_pb as HB`; api.py's re-export line for h_pb is not needed (none of
  them is used by another stage).

**I2 status (2940a23 on wip/az).** Rpb-1 served (P9 rock rings tele/disc_o, fill=0). Rpb-3 served (stomp_fl / stomp_hl foot keys: paw up >= 0.15 b at lift t5, events unchanged). Rpb-2 NOT served (tangential knockback needs a framework hz option of the released AZ-CM).
