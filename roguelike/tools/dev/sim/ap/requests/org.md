# Requests and notes from AP-ORG1 (the Apep phase-2 objects, `tools/build_mboss_apep_org.mjs`, branch `wip/ap-org`)

Protocol: `S:ap/ap_contract.md` §0.11 (append-only, `## R<stage>-<n> <type>: <title>`, what / why / needed by, status).
The org runtime is built to `ap_contract.md` §0.5 (the frozen clip table) without a change; `tools/mboss_apep_org_api.md`
describes it. Nothing here blocks another stage.

## RORG-1 note: organism models ride the husk at `ride_y` 2.0 — for AP-CORE (and AP-FW / S1-CM if the aux husk changes)

- what: every organism's model displays are passengers of the framework aux husk; the generator subtracts the husk's
  passenger point, 2.0 b above its feet (manifest `passenger.ride_y`), from every display translation. If the aux husk's
  entity type or scale changes (a different passenger height), set `RIDE_Y` in `tools/apep_org_geometry.mjs` and rebuild.
- why: a mismatch lifts or sinks every organism by the difference (the HP-bar fallback `om/<kind>/bars` uses the same
  constant).
- needed by: AP-CORE (spawn path: `aux/spawn`, then `om/<kind>/spawn` as the husk). status: open (informational).

## RORG-2 note: caller-owned markers; dome and wall placement — for AP-CORE / AP-REV / AP-P3 (answers RFX-3)

- what: `om/dome/spawn {i}` and `om/wall/spawn` summon **only the displays** at the execution point. The dome marker
  (`rlk_mb_ap_dome` + `rlk_mb_hzsafe`, `mbHzSG` = the cast's group, FN-14) and the wall group marker (`rlk_mb_ap_wall`,
  its barrier blocks) are the casting module's (`ap_contract.md` §0.3). Run both at the floor point (y 201): the dome
  displays' pivot is their feet, and the kit's `p/flood` measures the marker's 3D distance (RFX-3). A new wall blade
  keeps `rlk_ap_om_new` until the next `om/wall/spawn`: tag it into its group right after the call.
- needed by: AP-REV (Q2 domes), AP-CORE / the 둥지 module (walls). status: open (informational).

## RORG-3 note: object and organism ticks — for AP-CORE

- what: run `om/tick` as every organism husk once per tick (dispatch on `apK`), and `om/objects_tick` once per tick while
  any Heart / dome / stalk / wall display exists. `om/init` creates the objectives (`apK apS apT apOC apOI`). After turning
  a husk call `om/face` as it (a `tp` would dismount the models).
- needed by: AP-CORE. status: open (informational).

## AP-I2 status (2026-10-21, `wip/ap` f588262)

- RORG-3: done f588262: the core's `AP:obj/tick` runs `om/<object>/tick` for each object while its displays exist (the
  Heart bulb, a dome shell, a stalk, a wall blade), once per module tick, before the stage and the main slot; `om/tick` for
  the organisms stays AP-REV's `org/tick` dispatch.
