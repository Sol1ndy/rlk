# lane H2c (홍련 rebuild: her cinematic clips) — progress

Branch `wip/combat-hr2c` (from `origin/wip/combat`; merged: `origin/wip/combat` 1124df33c, H1 interface 15fad96a9, H1 final
c1e53b116, `origin/wip/combat` 8fe44f516 and b327762e5 = fix lane FA + the 11-11 stamp), worktree `<S>/cb/wt_hr2c`, pack copy `<S>/rp_hr2c` (`<S>` = the scratchpad of
`h_common.md`). Contract: `hr_design.md` (§8 wins). Owner of `tools/scarlet_cine.mjs` (her 8 cinematic clips, §4.1), her side
of the §4.3 contacts, the `gold` block of `tools/build_mboss_hr_fx.py`, `tools/dev/sim/hr/cine/**` and
`tools/dev/sim/hr/tests/{test_cine,test_contact}.py`.

## Steps
- [x] the 8 clips of §4.1 at the contract lengths with every event: `intro` 1290, `intro_end` 150, `cs1` 720, `lead60` 56,
      `lead5` 116, `lead_re` 60, `repel` 140, `ending` 1372; the hand-over poses of §4.1.
- [x] the contacts of §4.3, her side: 15 rows, a builder gate; `her_tracks.json` (her points per tick in the stage frame).
- [x] the clips against lane H3's actor manifest (0c762626b) and lane H2's sequence moves (8ab741163).
- [x] the `gold` overlay (U+EC17 + its four fade steps U+EC38-EC3B), live since H1's `api.kit_declares`.
- [x] suites, sheets, gates (below).

## How to run
```bash
S=<scratchpad>; WT=$S/cb/wt_hr2c/roguelike; cd $WT
node tools/build_scarlet_rig.mjs --resourcepack $S/rp_hr2c     # her rig + tools/dev/sim/hr/cine/her_tracks.json
python3 tools/build_mboss_hr_fx.py --resourcepack $S/rp_hr2c   # the kit (the gold glyphs)
bash tools/dev/regen_all.sh .
# authoring: only some clips, into a scratch datapack (no manifest; prints the contact errors per row)
node tools/build_scarlet_rig.mjs --resourcepack $S/rp_hr2c --datapack <scratch dp> --only repel,ending [--debug-dp <dbg> --debug-clips repel]
SIM=<copy of tools/dev/sim outside the tree>; cd $SIM/hr/tests
python3 test_cine.py $WT; python3 test_contact.py $WT [--actor <H3's tools/player_motion/cine/manifest.json>]
# sheets from the design's camera points (the debug dp of the rig build; --actor <char> with H3's cine_dbg frames)
node $WT/tools/dev/sim/hr/cine/roots.mjs > roots.json
python3 -I $SIM/hr/cine/shots.py --dbg <dbg> --rp $S/rp_hr2c --roots roots.json --seq repel --ticks 0,26,49,88 -o out.jpg
node $WT/tools/dev/sim/hr/cine/probe.mjs repel 49 88              # her points at single ticks (rig frame)
```

## What is built (by design section)
- **§4.1 the clips** (`tools/scarlet_cine.mjs`; sparse keys on S2a's skeleton, retargeted and solved by the rig builder):
  - `intro`: seated on the stone with cup and bottle (take 326, pour 352, down 414; raise 470, drink 600, cup down 700),
    the grip and the blade a hand out 756-786, up on the rock 792, turned to the actor 840-880 in steps, off the rock 1040,
    the walk 1052-1148, the hat tip 1160, the crouch 1230, the leap 1234-1258, landed (= `intro_end` 0 at 1290).
  - `intro_end`: rises, the brim lifted 40-56, the cross-draw 66-72 (one tick per key), upright, the stance 90-100, idle 150.
  - `cs1`: the lunge 6-9 and the X lock at K1 10-30, the shove, the leap back 34-50, low; sheathed 200 (a cut); the bottle
    216-500, the hat swing 240-258, the drink, the wipe 506; the iai 610, the draw 642-649, the slash 650, the post-slash
    pose at 720 (= `lead60` 0). **Tick 566 keys every shown part (1-tick keys to 567): the skip seeks the clip to 565.**
  - `lead60` (rise / stand / brim), `lead5` (stagger, backing off 8-60, the blade lifted 84-98, brim 100-106), `lead_re`:
    all end in `g_brim`'s hold.
  - `repel`: from `g_dive`'s line (blend 0-3) down onto KR, the press 10-26, the wide swing 27-30, her wrist seized 31-48,
    the hilt on her crown 49, reeling 50-52, the two cuts 56 / 62 with the sword arm tucked, back to back 68-78 (forearm
    at KS), the shoulder throw 79-100 (flat, the hat flying off 84-100), on her back 101-129, the kick jolt 130-132 (the hat
    taken 131), the kip-up 133-138, the hat back on 139, `idle2` at 140.
  - `ending`: on her back (= repel 129), the kip-up 6-15 (hat taken 9, worn 20), the sword raised 42, the lunge 50-54 as a
    three-tick flèche (the brim grazed at KG on 52, half way through the sequence's glide), the X lock at KE2 56-80, shoved,
    the spring back, the run 150-188, the clash and lock at KE5 190-204, the aerial duel (KA1-KA4, cut keys every tick),
    the flight to the mark 314-334, the scabbard 388, the sheathe 398-460 (click 452), the smile, the turn to the moon
    650-700, the look back, the gaze, the pivot 1072-1094, the walk 1094-1154, the gesture, the hat tip, `H_POSE` at 1372.
- **§4.3 contacts**: `CONTACTS` in `scarlet_cine.mjs` (K1, KR, KW, KH, KS, KT.over, KT.land, KK, KG, KE2, KE5, KA1-KA4); the
  builder measures her side every build and fails above tolerance (0.08 blades, 0.12 hands / feet / body);
  `tools/dev/sim/hr/cine/her_tracks.json` = her hilt, tip, hands, left elbow, feet, pelvis, head, hat crown and brim per
  tick in the stage frame for the 5 staged clips (+ the root track).
- **Root tracks** (`ROOTS` in `scarlet_cine.mjs`) = lane H2's `seq.py` moves (`m/*`), tick for tick: the clips animate in
  place; the root rows are only used for her stage-frame points (tracks, contacts).
- **§5.1 / §3.0 the `gold` overlay**: the marked "H2c block" of `build_mboss_hr_fx.py`: a white-hot centre on a gold field,
  a level flare, amber corners (the video's deflect frame); alpha 0.93; the fade steps come from the base loop.

## Gates (final tree, after the H1 / `origin/wip/combat` merges)
| gate | result |
|---|---|
| rig build twice | byte-identical (rig dir, manifest, `her_tracks.json`, the pack copy) |
| kit + `regen_all.sh` twice | identical; `check_mboss_pack` 0 problems |
| `test_cine.py` | 159 / 159 |
| `test_contact.py` | 47 / 47 her side; 86 / 86 with H3's manifest (both sides + where they meet) |
| loadcheck | `hr2c_b` 0, `hr2c_c` 0, `hr2c_d` 0, `hr2c_e` 0 (the final tree, after the FA merge) |
| rplint / atlas | 0 / 12.919 M px |
| `test_kit.py` | 11 243 / 11 246: the 3 rows that fail are not the overlay's: 104 sounds pinned (H1 added 5), the module's preset calls (H2's sequences are not on this branch) |
| `test_rig.py` | still pins the 11-06 set (47 clips, the old cine events: crashes at `scab_hand`; lanes H1c / H2 own the update). A scratch copy past those rows: see Decisions |

Contact worst values (her side, b): K1 0, KR 0.007, KW 0.014, KH 0.012, KS 0.098, KT.over 0.008, KT.land 0.079, KK 0.031,
KG 0.038, KE2 0, KE5 0, KA1 0, KA2 0.016, KA3 0.010, KA4 0.033. Where the blades meet the actor's (H3 manifest): every pair
within 0.015 b; no blade deeper than 0.04 b into the other's head box (KA2 / KA4 graze its corner).

## Decisions / deviations (and why)
- **Locks** (K1, KE2, KE5, KA4): her hilt below K and 0.1 b to the actor's left (r +0.1), not the design's "above KR /
  X-left": with H3's actor (its hilt at K + (0.3, −0.3, −0.25)) that is where both blades cross without either going
  through the other's head or hands.
- **The throw** stays flat on her back (pelvis pitch ≤ 108°), not inverted: the rig's floor is the root level and nothing
  may hang below it while the root arcs. KT.over at 2.95 puts her 1.3-1.7 b over the actor's head.
- **The repel's hat** lands at `HAT_REST.hold` = rig (−1.25, 0.02, 0.55), beside her head on her right, and is rig-relative
  (it slides with her root during the kick's slide 129-135; under the kick that reads as the hat swept along).
- **The scabbard** is in her hand from 388 to 1372 (not 388-452): `H_POSE` (= `ev_give` 0) holds it.
- **repel 0** re-grips the sword in the left hand on the dive's line (the 3-tick blend covers it; head / chest within 0.25 b
  of `g_dive`'s end); **repel 140**: the right hand is still on its way down from the brim (the next clip's blend).
- **R9** is a kip-up (the design's "roll to her feet": the kip-up reads at this distance and lands in `idle2`).
- **The intro** stands on the rock inside the clip (792-1040) and steps off; the rock height is `ROCK_T` 0.24 b.
- **The ending's lunge**: the sequence glides 50-54 (the design's numbers), so at the graze (52) her root is half way (3.75);
  her body is thrown 0.55 b ahead of it in a three-tick flèche (51-53, feet off the ground) to put the brim on KG.
- **The aerial duel** follows H2's moves (in to f 3.2 at 222-228, up to u 6.4 at 250-262, to (6.0, 3.3) at 276-286); her
  grips were drawn in to keep the same blade lines through KA1-KA4.
- **cs1 566 / 567** are declared `cuts` of the clip: every shown part keys at 566 with a 1-tick move to 567 (a normal run
  is unchanged; after the skip's seek the parts reach the clip's pose by 567, under the skip's black).
- `test_rig.py` (S2a's 11-06 suite) in a scratch copy past its old-contract rows (the states / hand-overs / big-swing spans
  of the 11-06 events, `seq.SEAT_RISE`, the 47-clip counts): the generic rows that touch these clips and stay open —
  the hat's switch jumps 0.19-0.20 b at repel 84 (off in the throw) and 139 (put on); the brim 1.7 mm into the base head's
  top corner at cs1 236; the sheathed hilt 1-2 cm off the scabbard pivot at intro 787-788 (the compiler's 1-tick
  reappearance key); `float` at repel 0-2 is the replay's artifact of the 3-tick blend (the clip starts in the air, the
  suite replays it without the previous clip); the lying right fist 0.046 b off its floor target while the hat pick-up's
  pre-roll pulls it to the hat (repel 127-130, ending 5-8: two contacts on one hand). Fixed in this lane after that run:
  the blade-forearm rule at repel 82 (the pull keeps the hook's line), the lying arm (elbow out to her side: no lift, the
  core on the floor, the fist on the brim at 0.17 b, the floor hat reached within 0.035 b, the pole reset as she rises),
  the intro's landing (a deeper crouch 1258-1276: the left palm on the ground instead of 0.29 b above it).
- **I18 (lane H2's camera)** at intro 1290-1296: with the hat low after the landing her brim passes 0.13 b in front of the
  lens (HR(0.15, 1.35, 1.0)); from about 1297 the lens is under the brim as the shot intends. A box stand-in did not show it.

## Requests to other lanes
- **H2 / HI** (`seq.py`): nothing blocking; her root tracks equal your moves. I18's first frames: see Decisions (lower
  the eye or start the shot a few ticks later if the brim fills the lens in game). The lethal kick's seam: the ending places her
  at f 4.2 at tick 0 (she lay at 3.0 at repel 129): the 1.2 b jump is under the seam's white, as you built it.
- **HI** (`test_rig.py`, owner H2 per §6.2): the cinematic rows (states, hand-overs, big-swing spans, the intro stone
  check with `seq.SEAT_RISE`) still name the 11-06 events; `test_cine.py` holds the §4.1 versions of those checks.
- **H3**: nothing open (all 86 contact rows meet).
- **H1**: nothing open.

## Pack files
Added by the kit generator (from the H2c block): `assets/rlk/textures/font/mboss_hr/gold.png`, `gold_1.png` … `gold_4.png`;
changed: `assets/rlk/font/mboss_hr.json` (5 bitmap providers). The rig builder adds nothing new (the pack copy's rig
files equal `rp_base`'s).

## Only a person in the game can check
1. The `gold` wash at the repel's deflect (0, in 0 / hold 4 / out 3) and the clashes of the ending: warm, not white.
2. The three locks (cs1 K1, ending KE2 / KE5) and the aerial cuts KA1-KA4 with the real actor: the blades cross, nobody's
   blade through a head.
3. The repel: the hilt on her hat at 49, the throw over the shoulder (flat), the hat landing beside her head, the kick.
4. The ending's flèche at 50-54 (feet off the ground 51-53) and the graze of her brim at 52.
5. The CS1 skip: after the black (566-586) she stands sheathed with nothing left over from the pre-skip pose.
6. The intro on the stone: the cup / bottle on the stone's item spots, the step onto and off the rock.
