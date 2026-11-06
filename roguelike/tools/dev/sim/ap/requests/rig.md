# Requests and notes from AP-R1 (the Apep rig, `tools/build_mboss_apep_rig.mjs`, branch `wip/ap-rig`)

Protocol: `S:ap/ap_contract.md` §0.11 (append-only, `## R<stage>-<n> <type>: <title>`, what / why / needed by, status).
None of these blocks another stage: the real manifest `tools/mboss_apep_rig_manifest.json` validates against
`S:ap/spec/stub_rig_manifest.json` (`validate.py rig … --against …: ok`), and every name of contract §0.4 is kept.

## RRIG-1 note: the face look `hidden` swaps the face to the empty model (contract §0.4.7 says "scale 0")

- what: `look/face/hidden` sets the `face` part's item to `empty` (`looks.face.parts.face.hidden = null` in the
  manifest, note "the empty model"); the clip keys keep the face's normal scale.
- why: a scale-0 face would have to be carried by every clip key of every clip that hides it (crawl, stand / crouch,
  sinks); the item swap has the same visible effect at one command and survives respawns through `look_apply`.
- needed by: AP-CORE (nothing to change; `look/face/<look>` is the only call). status: informational.

## RRIG-2 note: the hair parts hang from the hood (plan R2 draws them under the head)

- what: `hair_<s>_1` parents to `hood` (pose bone `hood_hinge` → `hood`); `hair_<s>_2` to `hair_<s>_1`.
- why: the 107° hood swing carries the hair roots from the cowl sides (crouch) to beside the face (upright); hung from
  the head, the upright hair rows of the R3 table could not reach the 0.25 b limit. With the hood parent every row is ≤ 0.25 b
  (max 0.234 b over 60 joints).
- needed by: AP-RC1 (animate the hair as hood children). status: informational.

## RRIG-3 note: CROUCH bind joints moved from the measured crouch table to make one rigid skeleton

- what: the rigid-skeleton fit (`S:ap/rigwork/tools/fit_upright.mjs`) moved a few CROUCH joints from the `MP3` crouch
  values: hair roots and `hem_a` by ≤ 0.38 b, `clav_a` (pose-only, unmeasured) by 0.68 b; tail joints re-spaced
  (`TAIL_C`). The manifest `skeleton.joints` lists the values used.
- why: R3 (UPRIGHT by joint angles only, every residual ≤ 0.25 b) cannot hold with the measured crouch values.
- needed by: AP-CORE / AP-P1 (anchors and px read from the manifest, so nothing to do). status: informational.

## RRIG-4 note: stub-clip choices inside the frozen table

- what: `death` kneels / falls into the crawl at 55-82 before its sink (its stance score stays UPRIGHT, as frozen);
  `aftermath` blends CROUCH → UPRIGHT over 72-84 (so the `p3_open` hands at 76 open on lifted wrists); every
  CROUCH ↔ UPRIGHT blend passes a halfway key with every limb on IK and the B / C wrists 1.2 b off the water; P1 hand
  events with lifted variants (`entrance_p1` raised claw 31-91, `crawl_p1` curls) lift that wrist in the stub.
- why: R9 (every part top ≤ −0.1 b at a hidden-span start) and the builder's hands-over-the-water check.
- needed by: AP-RC1 (replaces the stub keys; keep the same events, stance events and hidden spans). status: open.

## RRIG-5 request: a lower crawl stance (optional, for AP-RC1 / AP-CORE to decide)

- what: the reference crawl (v6 f165, f90, f528) carries the belly near the water and the hood front at the water;
  the R1 crawl is the CROUCH pose with the P3 looks (plan R1), belly ≈ 1.5 b, hood front ≈ 3 b.
- why: silhouette fidelity of phase 3 (`S:ap/rigwork/r1/r1_crawl_side.jpg`).
- needed by: AP-RC1 (could be a pose inside the crawl clips without a new stance), or AP-CORE if it wants a third stance
  (capsules / px sets per stance would change). status: open, no change made.

## AP-I2 status (2026-10-21, `wip/ap` f588262)

- The stub rig is dropped (`stub_rig.py`, `stub_rig_rt.py`, `tools/mboss_apep/stub_rig_manifest.json`): the module and the
  framework px compiler read the real manifest alone (36 D0 clips asserted). RRIG-5 (a lower crawl stance) stays open.

## AP-FIX status (2026-10-22)

- RP3-5 (from AP-P3): served by the AP-FIX rig commit 82943f2 (`tail_p3` yaw knots; contract §4.1).
- RRIG-5 (a lower crawl stance): still open; to be decided with the user at model sign-off.
