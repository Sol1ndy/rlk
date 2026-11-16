# 홍련 rebuild, lane H3 — the player's cutscene actor (branch `wip/combat-hr3`)

Contract: `hr_design.md` §3.0 (actor, displacement limits, hand-back), §4.2 (the 5 clips), §4.3 (contacts), §5.3 (calls), §6.3
(suite), §8. `S` = the session scratchpad. Pack copy: `S/rp_hr3` (from `S/rp_base`).

## Done
- **Rig and calls** (§5.3): `rlk:char/cine/{spawn,play {clip},tick,face {yaw},stop}`, objective `cine`, fake players `#cavT`
  (the module's clock) / `#cavC` (clip 1-5) / `#cavP` / `#cavR` / `#cavF` / `#cavFy` / `#cavCh`, storage `rlk:cine`, tags
  `rlk_cine_root` (a marker) / `rlk_cine_part` / `rlk_cine_<part>` (+ `rlk_room`, `rlk_mb_aux`: every sweep takes them) /
  `rlk_cine_hid`. 11 item displays = the player rig's part list on the avatar's skeleton (`transform()` of
  `build_player_rig.mjs`) at scale 1.0, fixed UUIDs `524c4b4d-4349-4e45-8000-0000000000NN`, brightness 13 / 15 and view range 2
  as her rig, no culling box. Part models: `rlk:player_motion/{lumine,skirk,clorinde,arle,navia,ronova,nefer}/<part>` by
  `#charN` (1, 3-8); one sword `rlk:player_motion/weapons/cine_sword` (= the rig's `sword` model).
- **Clips** (§4.2): `cs0` 1440, `cs1` 720, `repel` 140, `ending` 1372, `coda` 120, written as channel tracks in
  `tools/player_motion/cine/clips.mjs`, solved by `lib.mjs` (FK / IK blend, two-hand grips, look-at, floor search for the
  soles). The build writes `tools/player_motion/cine/<clip>.json` (player_motion format) and compiles them.
- **Contacts** (§4.3) all inside tolerance (build check + manifest): K1 0.000, KR 0.000, KW 0.017, KH 0.051, KS on the shoulder,
  KK 0.011, KG 0.000, KE2 0.011, KE5 0.000, KA1 0.000, KA2 0.014, KA3 0.000, KA4 0.000 (blocks; blades 0.08, hands / feet 0.12).
- **Manifest** `tools/player_motion/cine/manifest.json`: per clip `len`, `grip`, `beats`, `steps` (footfall ticks), `slides`,
  `two_hands`, `handback`, `her` (the sheets' stand-in marks), `sync`, `contact` results and per tick `shift`, `hilt`, `tip`,
  `hand_r`, `hand_l` (+ `pommel`, `foot_r`, `foot_l`, `head`, `shoulder_r`) in the stage frame; also calls, tags, the sword's
  lengths (`hilt_to_tip` 1.4875, `blade_root` 0.1875), the contact table, the limits.
- **Generator**: `tools/build_player_cine.mjs`, called by `build_player_rig.mjs` (two hooks: `cineAtlas` before the block
  aliases, `buildCine` at the end). The player rig's own outputs are byte-identical (test `--rebuild`, `ident_hr`).
  Build gates (throw unless `--cine-allow`): nothing under the floor, ≤ 120° per tick, `shift` inside the limits and zero at
  the hand-backs, the last pose = the avatar's idle, planted soles (outside declared slides), IK reach, two-hand grips, the
  contacts, the clip hand-overs (repel 129 = ending 0, ending 1372 = coda 0), no channel drifting over a forgotten hold.
- **Suite** `tools/dev/sim/hr/tests/test_actor.py` (217 checks) and the sheet tool `tools/dev/sim/hr/actor_sheet.py`.
  `ident_hr.py` gained the lane's bundle (`LANE_H3`).

## How it plays (for H2 / HI)
- `spawn`: as the player, at the stage marker, rotated as the stage. `play {clip:"cs0"}`; every tick the module writes
  `#cavT cine` and calls `tick` as the player (`api.actor_clock()` / `api.actor('tick')`). `stop` anywhere.
- The whole displacement is inside the display transforms: the entities stay at the stage origin, the root only keeps the
  place and yaw (`face {yaw}` turns it in 12 ticks, the short way; the parts follow).
- A part gets a key only when its transform changes (interpolation segments; holds send nothing). **26.3 fact** (server jar,
  `Display.readAdditionalSaveData`): every NBT write to a display resets its interpolation clock, and with an unchanged
  transform the client replays the last interpolation — so no per-tick re-sends, and never `data modify` a part's item.
- Jumps of `#cavT`: sync ticks = every 20 ticks, each clip's end, `cs0` 1290, `cs1` 566: exact at once. Any other tick: the
  snap of the sync tick before it, then the keys replayed (lands within 40 ticks). After a snap the running segments start
  one tick late and are back on time at their ends (the cut masks cover it). A forward gap of ≤ 20 ticks replays the keys.
- `tick` without a root (the actor swept by `/reload`, a room wipe, mboss cleanup) calls `stop`: the avatar shows again.
- Hidden while the actor stands: the avatar (invisibility 1 s at a time + empty hands, re-applied every tick: it shows by
  itself if the ticks stop), a rig character's `rlk_pm` displays and Ronova's / Nefer's floating catalyst (`view_range` 0,
  tag `rlk_cine_hid`; `stop` restores 1.5 / 1). `stop` removes the objective and the storage; `spawn` / `play` / `face` add
  the objective again, so `play` may come before `spawn`.

## Deviations from the design (and why)
1. **cs0 walk cycle 16 t, not 24 t.** At 0.075 b/t a 24-t cycle needs 0.9-b steps; the 0.75-b leg cannot keep a sole planted
   that long (and 80 t is not a multiple of 24). 10 steps, footfalls at 24, 32, … 96 and the closing step 102 (`steps`).
2. **repel, the pass (62-68)**: the root goes through r −0.5 (she stands on the axis; the design lists only f). Legs carried
   (a leaping stride), declared slide 61-68.
3. **repel, the hilt strike (49)**: KH is 2.20 up, out of a standing arm's reach from above: a short hop in the pose (the
   pelvis +0.14, `shift` stays 0) and the pommel driven forward onto KH (hilt 0.051 from it).
4. **repel, the back-flip**: airborne 132-138, lands 138, the idle at 140 (design: 132-139, lands ready 140: the hand-back
   pose must be the idle). The flip's height is in the pose (`shift` u = 0).
5. **ending, the aerial duel**: no full turn (root yaw stays 0 in every clip); at KA2 (260-266, two hands) the root is at
   r −0.5 so both hands reach a level guard whose blade points right with K on the axis.
6. **ending, the run (150-188)**: gathers 150-164, three driving steps 164-188 (only 1.5 b lie inside the forward limit).
7. **Blade locks with two hands**: the X convention puts the hilt 0.3 b to the actor's right of K, so the pelvis leans up to
   0.25 b right and the torso turns (inside the pose; `shift` r = 0 except 2 and 5).
8. **cs1**: 716-720 goes to the idle (not "ready"); the planted sword leans (the grip 1.42 up: the sword is 1.49 b long).
9. **Sword roll**: the blade may be shown rolled half round its axis (the same picture) to avoid 180° spins; the hand-back
   check compares the sword modulo that roll.
10. No shadow under the actor (the displacement is in the transforms; her rig has a shadow helper).

## Requests to other lanes
- **H2**: step sounds at the manifest's `steps` of `cs0` (24 … 96, 102; then 1255, 1259, 1395, 1400, 1434, 1438) instead of
  every 12 t; frame the repel's pass (62-68, r down to −0.5) and KA2 (r −0.5) from the manifest's `shift`; the ending after a
  repel: `play {clip:"ending"}` without a new `spawn` (tick 0 = the kick's pose, checked); `face {yaw}` takes the absolute yaw.
- **H2c**: the actor's side is in the manifest columns. 26-30 my blade sweeps up and to +r (hers is thrown that way); 36-48
  my left hand is at KW; 49 the pommel comes onto KH from the front; 70-78 my right fist is at about ST(0.26, 1.60, 1.74) over
  her forearm (KS above the shoulder); 84-96 my hands travel to ST(0.3, 0.6, 2.5) / (−0.1, 0.5, 2.5); 129 the right sole is on
  KK. Blade locks: my hilt at K + (0.3, −0.3, −0.25).
- **HI**: `test_contact.py` can read `clips.<id>.tick.hilt` / `.tip` (the blade's root is 0.1875 b from `hilt`); README 0-4 /
  the pack README need a line (the player rig build also builds the actor; the pack files below). `uninstall` needs nothing
  (`stop` leaves no objective).

## Pack files (all from `node tools/build_player_rig.mjs --datapack . --resourcepack <RP>`)
- added: `assets/rlk/textures/skin/lumine.png` (copied from `tools/player_motion/cine/skin/lumine.png` = her profile
  texture `textures.minecraft.net/texture/f979940d…a9566f`, 64 × 64, fetched 11-10),
  `assets/rlk/{items,models/item}/player_motion/{lumine,clorinde,ronova,nefer}/<10 parts>.json` (80 files),
  `assets/rlk/items/player_motion/weapons/cine_sword.json`.
- changed: `assets/minecraft/atlases/items.json` gains `rlk:skin/{lumine,clorinde,ronova,nefer}` (+16 384 px: the three
  existing skins were profile textures only, not atlas sprites). Atlas 12.919 M → 12.935 M px (gate 13.2 M).

## Gates (last run)
`test_actor.py <dp> --rp S/rp_hr3 --ref-rp S/rp_base --rebuild`: 217 / 217 · `ident_hr.py`: passed (with `LANE_H3`) ·
`regen_all.sh`: 0 failures, no file outside the lane changed · `check_mboss_pack.py`: 0 problems · `rplint`: 0 ·
`atlas_px`: 12 935 424 px · loadcheck: 0 function load failures (26.3). Other `hr/tests` suites do not read the actor.

## Sheets
`python3 -I hr/actor_sheet.py --dbg <dbg> --rp <rp> --man <dp>/tools/player_motion/cine/manifest.json --clip repel --ticks
0..140:3 --view az:55,10 -o out.jpg` (from a copy of `tools/dev/sim`; `<dbg>` = the builder's `--cine-debug-dp`). Looked at
for 스커크 and 루미네 (every clip) and 클로린드 (coda); fixed from them: knees that did not reach the floor, limbs through the
torso in the locks / the hilt strike / the throw, a blade through the head in the level guard, sword points under the floor.

## Next (if resumed)
- Polish only: the left elbow still grazes the torso for 2-4 ticks entering two locks (ending 54-55, 190), the right elbow
  0.04 inside in the dash's follow-through; a shadow helper; more life in the aerial duel's legs.
- After H2 / H2c land: HI's `test_contact.py` against her clips; in-game look (below).

## Only a person in the game can check
- The 1-tick lag after a snap and the 0-tick snap itself under each cut mask; the actor's brightness next to her.
- The avatar ↔ actor swap at spawn / stop for each character (스커크 · 아를레키노 · 나비아: their rig displays; 로노바 · 네페르:
  the catalyst), and that nothing of the avatar shows during a sequence (the hand item for one frame every 2 s).
- Lumine's skin on the 3-px arms; the sword's size in the two-shots; the feet in the arena's plants.
- The reading of the choreography in the real cameras: the lock convention, the grab, the hilt strike, the throw, the kick.
