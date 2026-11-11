# Round V, lane VC (the cutscene camera and the cutscenes) — progress

Branch `wip/v-cam` (from `origin/wip/v` d7e7cf013), worktree `<S>/cb/wt_vc`, pack copy `<S>/rp_vc` (from `<S>/rp_fin`, the
11-11b release pack); `<S>` = the scratchpad of `v_brief.md`. Contract: `v_brief.md` §3 "VC" 1-11, `review/v/client_facts.md`.
Owner of: the FN-cam block of `tools/build_mboss_core.py` / `tools/mboss_lib.py` (`mboss/cam/**`), `tools/mboss_scarlet/{seq,cam}.py`,
`tools/build_player_cine.mjs` (the actor), `tools/build_blank_tex.py`, the suites `hr/tests/{test_cam,test_seq,ev_dry}.py` and the
tools `hr/h2/**`, `hr/cine/built_shots.py`.

## Steps
- [x] the mechanism in the framework (FN-cam v2): display cameras, the grid, keyframes, the hold with its post hook, the lock
      of the interaction ranges, the HUD, the camera texts
- [x] `cam.py` (keyframes / track / chase, prepared cuts) and `seq.py` (every sequence on it; lines on the camera text; the skip
      on Space; the skip's state; the staging fixes)
- [x] the suites (camsim / seqsim client model; test_cam, test_seq) and the shot-sheet tools on the client's picture
- [x] ghosts: the blank textures (generator), the avatar's blank skin, the seat
- [x] shot sheets looked at, docs, gates

## How to run
```bash
S=<scratchpad>; WT=$S/cb/wt_vc/roguelike; cd $WT
python3 tools/build_mboss_core.py && python3 tools/build_mboss_scarlet.py      # FN-cam + the sequences (or: bash tools/dev/regen_all.sh . --mobs)
node tools/build_player_rig.mjs --datapack . --resourcepack $S/rp_vc           # the actor (char/cine/**: blank / hide / show)
python3 tools/build_blank_tex.py --resourcepack $S/rp_vc                       # the three blank textures
SIM=$S/cb/vc/sim; rm -rf $SIM; cp -a $WT/tools/dev/sim $SIM; cd $SIM/hr/tests  # suites never run inside the tested tree
python3 test_cam.py $WT && python3 test_seq.py $WT && python3 ev_dry.py --dp $WT    # test_seq: static run stages skip life actor frames
RLK_DEV=$S bash $WT/tools/dev/loadcheck.sh $WT vc
$S/cb/vc/probe/probe.sh $WT p1                                                  # scratch: FN-cam on the real server (results below)
# shot sheets through the built cameras (the client's viewpoint), her real rig and the actor; --text draws the line's box
cd $SIM/hr/cine && python3 -I built_shots.py $WT --dbg <rig debug dp> --rp <throwaway pack copy> --seq intro --lines --text -o out.jpg
```
(`built_shots.py` needs `<S>/preview/raiden_preview.py`: copy it from `tools/dev/sim/preview/` when the scratchpad is new.)

## What is built, per ruling (v_brief §3 "VC")
**1. Display-entity keyframed camera, on-grid rotations.** `mboss/cam/**` (13 functions): the cameras are EMPTY `item_display`s
(`rlk_mb_cam1` / `rlk_mb_cam2`, tag `rlk_mb_camx` on the whole set). `mboss/cam/grid` rounds a placed rotation to the nearest
360 / 256 step (half a step added, the byte index floored with scale 0.71111112 and written back with scale 1.40625: exact
floats, idempotent) and moves the entity 4 b forward; `mboss/cam/fix` = grid + the OnGround flip on every other placement
(the float sync packet; nothing depends on it). `cam.py`: a shot = its first keyframe + segments (`Key`): one placement per
segment at its first tick, the duration (`mboss_lib.cam_dur`) one tick ahead. `move` (straight, <= 59 t and <= 12 degrees a
segment; `io` as 3-6 segments; a move that keeps its view direction keeps its rotation), `track` (her walk: segments led by
`seq.HER`, her moves on the stage, added to her place when the placement runs), `chase` (per tick at 3-tick interpolation:
only I16 the leap and E7 the arc back).

| sequence | shots | ticks with camera commands (11-11b -> now) | segments | of them |
|---|---|---|---|---|
| intro | 23 | 1308 -> 125 | 49 | 11 moves (20 segments), I15 tracked (4 x 24 t), I16 chased (25 t) |
| cs1 | 13 | 457 -> 39 | 1 | S2's push 10-22 |
| repel | 8 | 53 -> 24 | 1 | R0's push 4-25 |
| ending | 23 | 953 -> 114 | 37 | E2 (3), E6 tilt (5 x 2-3 t), E7 chased (22 t), E14b (6), E16 (1 x 59 t) |
| coda | 3 | 118 -> 9 | 0 | |

The slow pans the review measured as bursts: I3 the moon 110-169 = one 59-tick segment; I5 250-319 = two (34 + 35 t); I9
536-665 = three of 43 t; I19 1350-1400 = one of 50 t; I1 24-74 = one of 50 t. Measured in the suite's client model
(test_seq R12): every rotation ever sent for a camera lies on the grid, no interpolation longer than 59 t.

**2. Third person (4 b behind).** Every shot is written as a viewpoint; the entity stands at viewpoint + 4 x forward of the
SAME grid rotation. Build-time proof (test_seq `stages` G5, `shots.f5_clear`: the 8 corner rays of `Camera.getMaxZoom`):
on every locked tick of CS0 (fixed stage) and of cs1 / repel / ending + coda on five stage placements (centre, and the
avatar at radius 24 on four bearings) the entity is in air and the 4-b line back meets no solid block, barrier or thin
plant. Three shots failed first and were changed: I1 (its viewpoint at f -7.4 put a corner ray into the barrier ring: now
-7.0), R8 on the wall stages (the entity sank to the floor: `seq/lib/camin` now keeps a camera entity of a dynamic stage in
the walk disc and >= 0.3 b over the floor), I7 (looked 25 degrees down at the cup from 0.6 b: now level). First person and
F5-front are not supported during a cutscene (README).

**3. Settled cuts.** The idle camera: duration 0 at t - 3, the placement at t - 2 (a snap), the first segment's duration at
t - 1. Measured (test_seq R9, per cut): the client's pose of the incoming camera equals its server pose with no step left
for >= 2 ticks before every cut (margins 2 t; 6-11 t for a camera made at the start), the first frame is that place, a
move that starts at the cut has made at most its first step; 0 of the 66 cuts slide. Every shot lasts >= 3 ticks (asserted).
Two cameras suffice (the shortest shot, R8, is 4 ticks).

**4. Left click.** `hold_in`: `entity_interaction_range` and `block_interaction_range` get the modifier `rlk:mb_cam`
`-1 add_multiplied_total` (total x 0; the bases are not written), removed at the release (test_cam `lock` L1 / L5).

**5. Skip on Space; Shift.** `seq/<name>/skipin` (+ `skipgo`, `skipoff`): the jump key (`rlk:in_jump`) held `SKIP_HOLD` 20
ticks inside the window; the prompt 「⊙ 건너뛰기 · Space 길게」 on the camera's hint text (the action bar when no camera
holds the player), brightening in 4 steps. The core's Shift input (`core/skip`, lane VB's file) rests: `#skip hr -1`; its
test hook `#skp` is honoured by skipin. **Shift**: the game ends the spectate inside `ServerPlayer.tick`, after every
function; the very next statement there fires the `tick` advancement trigger, so `mboss/cam/post` (the reward of
`rlk:mboss/cam_post`, armed by the hold with `advancement revoke` each held tick) spectates again in the same server tick.
Measured in the model (test_cam `post` P1): Shift held 12 ticks -> after every tick the client and the server are on the
live camera; per tick two camera packets go out in one server tick (to the player, back to the camera). What remains for
the client: the two packets are applied in one drain of its packet queue (fact 19), so no frame is drawn between them
unless a frame boundary falls between two packets sent microseconds apart; in that one frame the client would draw its own
third-person view, which the hold makes the shot's (scale x 2, camera distance + 32: 4 b behind the same point, 0.2 b
higher: test_cam L3). Before: 75-380 px of jump on every frame (T2-SHAKE). Not measurable here: how often such a frame
occurs in the game.

**6. Free flight.** Cause found (facts 5-7, consistent with the recording: the first 33 ticks of CS0 in t2 show a static
level view from the I1 place, not I1's push-in, until the cut at 60 attaches): at the arrival the camera was summoned into
a chunk still pending for the player, so it was not paired; the client ignored the camera packet for an entity it did not
have; the server counted the camera as set, and every later `spectate` was a no-op. The hold now re-sends the camera for
real (`spectate` to the player, then to the camera, inside `post`, after the server paired the entity in that same player
tick) on the first 3 held ticks, while a module asks (`mboss_lib.cam_resend`: CS0 44 ticks, under its black), and on the
first tick and every fourth tick of a movement key (W A S D Space). test_cam `post` P3 / P4: a camera unknown for 8 ticks is
attached in the tick the client gets it; without the request the control case reproduces the bug and a movement key ends
it in that tick. test_seq R11: the client is on the live camera on every held tick of every sequence.

**7. Ghosts.** (a) cameras: displays (nothing drawn). (b) her hit-box husk: `tools/build_blank_tex.py` writes fully
transparent `textures/entity/zombie/husk.png` + `husk_baby.png` (audit: every husk of the pack is an invisible hit-box
carrier - the framework body, `cm/spawn/*`, the proxies; the one visible husk is the developer fallback `#mobTmp room 1`).
(c) the avatar (an invisible mannequin while the actor stands in): `char/cine/blank` sets `profile.texture` to
`rlk:skin/blank` (kept in `rlk:cine av`, put back by `show`). (d) the F5 seat (an armour stand; armour stands are visible
elsewhere, so no blank texture): removed in `hold_in`, made again by `mboss/cam/seat` at the hand-back. (e) the mob lure
mannequin: blank skin in `cm/lure_new`. (f) the "two tall slabs" of the arrival were not entities: chunk columns of the
dome not yet on the client, with the sky behind (they stand exactly where the dome wall is in t2 6.20 s); CS0's black now
holds 34 t and is gone by 42 (was 2 / 8), which also covers the arrival of the camera entity. test_seq R14: on every held
tick the only living entities are husks and the avatar, both blank.

**8. The skip's state.** Cause of "she pops in": the rig's follow (`rig/tick`) runs in the execution position the hook was
entered with; a body teleported inside the hook left her model at the old place with the follow's cache already updated.
`seq.RIG_NOW` (`rig/follow_now` at the body) after every instant move: both skips, the starts of cs1 / repel / ending. The
skips make both cameras anew on the target shot (nothing still glides). test_seq `skip`: K1 the state 4 ticks after the
jump equals the uninterrupted run's (her place, yaw, MODEL, the live camera, the client's picture, both texts, the props
and the seat rock, the stage, the actor's clock, the lock), K2 the end state and the lines after it, her model at her body
on every tick; a mutation without RIG_NOW fails K1 / K2 with her model at the seat rock. No line over the black: a held run
never calls the kit's title line; the camera text is in the world, under the overlay.

**9. HUD.** The crosshair came from `view/ttl_blank` (the kit's subtitle line re-sent it while the seat existed): no kit line
in a held run, and without the seat `ttl_blank` sends an empty title. The sidebar: `setdisplay sidebar` off in `hold_in`,
`stacks` again at the release. The loot line 「사파이어 +N」: `combat/sap_absorb` adds to `#mbCamSap mb` while a player is held,
the release tells the sum once. "Press ... to Dismount": `mboss/cam/back` sends an empty action bar right after the mount
(facts 18). The boss bar is untouched.

**10. Lines and hint.** Two `text_display`s ride each camera (billboard center, 0.3 b before the eye). Line: scale 0.0858,
the block's middle 62 % below the centre at a field of view of 70, backdrop black 72 %; hint: scale 0.0464, 80 % below.

| fov | line: middle / glyph / widest page | hint: middle / glyph |
|---|---|---|
| 70 | -0.62 / 44 px / 1059 px | -0.80 / 24 px |
| 80 | -0.52 / 37 px / 883 px | -0.67 / 20 px |
| 90 | -0.43 / 31 px / 741 px | -0.56 / 17 px |

(1080p; before: 18 px, no backdrop, just under the centre.) `seq.say`: typed two syllables per 2 t with the kit's typing
sound, pages of `api.LINE_PAGES`, verbatim (test_seq S4 / R4). Never over her face: test_seq F4 (her head +- 0.27 b projected
through the client's viewpoint against the box of the widest page, every line tick; independent of the field of view);
two shots failed first: I5 (re-aimed at her shoulder), S10's last tick (S11's cut moved to 608).

**11. Staging.** Petals: `billboard:"center"`, never nearer than 1.5 b to the lens; S10's passes 2 b BEHIND her (was 0.35 b
before the lens: the 690-px blob), S11's (the one she cuts) at her waist 1.5 b from the lens, E9b's behind her. I14 (the
empty field, 960-979) has no line; line 8 starts on I14b's first frame (the 4 frames of field under it were the cut's
slide). I16 from the side (ST(-4.6, 1.3, 9.2), chased): she is about a fifth of the picture's height (her 1.8 b at 6.1-6.9 b: 200-230 px at 1080p and a field of view of 70; was 40).
T1-START-1: I1 is visible 34-75 (black before), I2 76-109. T1-STAGE-2 (three frames inside her body): the slide of a cut.

## Real-server probe (26.3, `<S>/cb/vc/probe/probe.sh`, a copy of the server dir under the shared lock)
- `execute positioned 3.5 120 3.5 rotated 137.25 -12.5 run function rlk:mboss/cam/spawn_at {id:1}` -> an item_display at
  `[0.879, 120.876, 0.608]` (= the viewpoint + 4 forward) with `Rotation [137.8125f, -12.65625f]`, `teleport_duration 0`,
  both texts riding it (`execute as <text> on vehicle`), the helper marker gone.
- `tp` to `3.5 121 3.5 33.3 44.4` + `mboss/cam/fix` -> `Rotation [33.75f, 45.0f]`, `Pos [1.929, 118.172, 5.852]`, OnGround 0b;
  again -> the same rotation, OnGround 1b; `-179.9 90` -> `[-180.0f, 90.0f]`, 4 b straight down; the text's `Pos` = the camera's.
- the line merge: `text {color:"#F2D0E8", text:"낭자 생각은 어떤가?"}`, `background -1207959552`, `translation [0, -0.13989, 3.7]`.
- `mboss/cam/spawn` twice: 6 entities; `teleport_duration:77` is stored as 59; `mboss/cam/kill`: none left.
- loadcheck: `Loaded 1871 advancements` (+ 1).
The first loadcheck of the tree found what no simulator did (`... run as @a ...` in the typing-sound line, 168 files): fixed,
and test_seq S3 now refuses an execute subcommand after `run`.

## Gates
GATES_PLACEHOLDER

## Deviations (and why)
- **The skip input lives in the sequence, not in the core**: `core.py` (the Shift input) is lane VB's file. `seq/<name>/skipin`
  reads the jump key and parks the core's input with `#skip hr -1`; `core/skip*` stay generated but never run past their
  first line.
- **Shift is not "the player teleported onto the shot"** (ruling 5's suggestion): the re-spectate inside the player's own
  tick keeps the client ON the camera, which is better than any own-view placement; the own view is made to coincide
  anyway (scale / camera distance) for the one frame the client could draw between the two packets.
- **The hint is under the line, not at the bottom edge**: with the text 0.3 b before the eye a wider field of view pulls
  both toward the centre; the bottom edge would cut the hint off below a field of view of about 65.
- **The avatar is not moved away** for the lock (preference 2 of ruling 7): the sequences, the coda's gift and the framework
  read its place; its skin is blank instead. The husk is the framework body of every boss: blank texture (preference 3)
  after the audit; README names the one developer-only visible husk.
- **`test_scarlet.py` / `hr/tests/lib/hrsim.py`** (H1's suite and the shared sim): the two CS0-skip checks press the jump
  key now and the sim knows `rlk:in_jump` (4 + 3 lines); nothing else of them is touched.
- **R6 of test_seq** (commands of a sequence's own files in a tick): 400 -> 440. `RIG_NOW` runs the rig's follow (36
  commands) inside the sequence's call at a start; before, the same follow ran later in that tick from `rig/tick`.
- The actor (`build_player_cine.mjs`) is rebuilt through `build_player_rig.mjs` (lane VP's file, not edited): only
  `char/cine/{hide,show,blank}` change.

## Pack files (added by `tools/build_blank_tex.py`; nothing else of the pack changes: `diff -r rp_fin rp_vc`)
`assets/minecraft/textures/entity/zombie/husk.png`, `assets/minecraft/textures/entity/zombie/husk_baby.png`,
`assets/rlk/textures/skin/blank.png` (64 x 64, alpha 0). **The husk ghost only goes with the new pack.**

## Shared files changed outside F:boss/scarlet, F:mboss/cam, F:char/cine (test_cam `ident`)
`combat/sap_absorb` (2 lines), `cm/lure_new` (the blank profile), `lvup/tick` (a comment), new
`data/rlk/advancement/mboss/cam_post.json`. Other bosses' generated outputs: byte-identical (they use no camera).

## Only a person in the game can check
Nobody can run the client here: what follows is read from bytecode or measured in the suites' client model, never seen.
1. **The 4-block third person** (ruling 2): in F5-back the framing equals the sheets (close shots: her face in the upper
   middle). If every shot is 4 b too near or too far, the assumption fails. First person / F5-front: unsupported.
2. **Smooth pans** (1): I3 the moon 110-169, I5 250-319, I9 536-665, I19 1350-1400, I1 24-74, E14b 960-1037, the tilt E6
   204-216: constant flow, no burst-and-rest. The chased shots I16 (1234-1259) and E7 (314-336): she stays in the frame.
3. **Cuts** (3): no slide of 2-6 frames after any cut; the bottle shot (tick 320, 17.9 s in t1) does not start inside her.
4. **Ghosts** (7): none near her (needs the NEW resource pack: blank husk), none at the avatar's place or over its head,
   none at the arrival (black until tick 42; then the arena complete). After a hand-back the avatar's skin is back at once
   (Lumine's is a profile skin: look for a default-skin blink).
5. **Left click** (4): clicking through a cutscene changes nothing.
6. **Shift / keys** (5, 6): Shift held: the picture stays (a rare single-frame blink is possible: how often?); W A S D and a
   short Space do nothing; no free flight at the start of CS0.
7. **The skip** (5, 8): Space held 1 s brightens the prompt and skips; after CS0's skip the black lifts on her standing 6.5 b
   ahead with line 11 on screen, nothing plays in an empty place, nothing pops at the hand-back; CS1's skip likewise.
8. **Lines** (10): lower third, dark backdrop, large glyphs, never over her face; the box is not cut by her body or a prop
   (it is 0.3 b before the lens); particles / translucent effects drawn over the backdrop (the translucent draw order was
   not verified); the typing sound; size and place at the player's field of view (70-90 intended).
9. **HUD** (9): no crosshair, no sidebar, no sapphire chat line during a lock (told once at the hand-back), no "Press Shift
   to Dismount", no second "press F5" chat hint; the boss bar as before.
10. **Staging** (11): S10's petal passes behind her head, S11's is cut at her waist, E9b's passes behind her; the leap I16.
11. The OnGround flip and the per-tick `advancement revoke` have no visible or audible side effect (no toast, no sound).

## Verified in the 26.3 bytecode (javap -c -p; client `<S>/mcclient/client.jar`, server `server-26.3.jar` of `<S>/mcjar/server.jar`)
Beyond `review/v/client_facts.md` (whose [V] items this lane re-used as they are), read for this lane:

| # | fact | where |
|---|---|---|
| 1 | `ServerPlayer.tick()`: the camera block (snap to the camera entity, `chunkSource.move`, `wantsToStopRiding()` -> `setCamera(this)`, a dead camera -> `setCamera(this)`) is followed at once by `CriteriaTriggers.TICK.trigger(this)` | `ServerPlayer.tick` offsets 69-144 |
| 2 | an advancement's reward function runs synchronously inside the trigger: `PlayerAdvancements.award` -> `AdvancementRewards.grant` -> `ServerFunctionManager.execute(fn, player source)` | `PlayerAdvancements.award` 67, `AdvancementRewards.lambda$grant` |
| 3 | functions of the tick tag run before the levels tick (`MinecraftServer.tickChildren`: `getFunctions().tick()` first); in a level `ServerChunkCache.tick` (the entity tracker's `sendChanges`) runs before the entities tick | `tickChildren` 34 / 172, `ServerLevel.tick` 342 / 471 |
| 4 | a revoked advancement without `display` sends nothing: `flushDirty` builds its packet only from visible advancements and skips it when all three collections are empty | `PlayerAdvancements.flushDirty` 151-223 |
| 5 | `ServerPlayer.setCamera`: nothing when unchanged; else `teleportTo(camera pos, own rotation)`, `ClientboundSetCameraPacket`, `resetPosition` | `ServerPlayer.setCamera` |
| 6 | the client changes its camera entity only in `handleSetCamera` (ignored when the entity id is unknown: `getEntity(level) == null`), `handleLogin`, `handleRespawn`, a level change; `GameRenderer.tick` only replaces a NULL camera entity | callers of `Minecraft.setCameraEntity` / `Camera.setEntity` |
| 7 | the server pairs an entity with a player only when the entity's chunk is in the player's view AND not pending in the player's chunk sender (`ChunkMap.isChunkTracked`); `ChunkMap.move(player)` (called from the camera block of `ServerPlayer.tick`) re-evaluates every tracked entity | `ChunkMap$TrackedEntity.updatePlayer` 80-122, `ChunkMap.isChunkTracked`, `ChunkMap.move` |
| 8 | `handleSpectatorAction` with an empty entity id does nothing (a click that picks nothing is ignored by the server) | `ServerGamePacketListenerImpl.handleSpectatorAction` 38-44 |
| 9 | the client's pick: ray length `max(block range, entity range)`; an entity hit counts only when `distSq < entityRange²` and is passed through `filterHitResult(hit, eye, entityRange)`: with both ranges 0 no entity is ever picked, also when the camera entity stands inside a hit box | `LocalPlayer.raycastHitResult` / `pick` |
| 10 | attribute value = `(base + Σ add_value) × (1 + Σ add_multiplied_base) × Π (1 + add_multiplied_total)`: one `add_multiplied_total -1` modifier forces 0 whatever the base and the other modifiers | `AttributeInstance.calculateValue` |
| 11 | `LocalPlayer.sendChanges` sends `ServerboundPlayerInputPacket` whenever the key state changed, before and independent of `sendPosition` (the only part guarded by `isControlledCamera`); `ClientInput.tick` in `aiStep` is unguarded; `Minecraft.tick` calls `sendChanges` every client tick; `KeyboardInput.tick` reads up / down / left / right / jump / shift / sprint | `LocalPlayer.sendChanges` 12-57 / 133, `aiStep` 165, `KeyboardInput.tick` |
| 12 | `TeleportCommand.performTeleport`: a relative rotation is `given − entity rotation` (so the result is the SOURCE's rotation + the offset: `execute rotated as X run tp @s ~ ~ ~ ~ ~` gives X's rotation; `tp @s ^ ^ ^4` keeps the rotation), then `setOnGround(true)` | `performTeleport` 106-245 |
| 13 | `AbstractInterpolationHandler.interpolateTo`: `interpolationSteps == 0` -> `entity.snapTo` + `cancel()`; a target equal to the running one is ignored; else `startInterpolating` from the current state | offsets 0-72 |
| 14 | `DisplayRenderer.submit`: nothing is drawn without a sub state; `ItemDisplayEntityRenderState.hasSubState` = the item is not empty (an EMPTY item_display draws nothing) | `DisplayRenderer.submit` 8-19 |
| 15 | billboard `center`: orientation `rotationYXZ(−(cameraYRot − 180)°, −cameraXRot°, 0)`, then `poseStack.mulPose(transformation)`: the translation is in the camera-aligned frame (x = screen right, y = up, z = toward the viewer) | `DisplayRenderer.calculateOrientation` case 4, `transformYRot` / `transformXRot`, `submit` 50-76 |
| 16 | text display layout: rotate π about Y, scale −0.025; line height 10, block height `10 n − 1`; `translate(1 − width / 2, −height, 0)`: the block's bottom edge is the display's origin, the text is centred; the backdrop quad (−1, −1)..(width, height) is drawn only when the background colour is not 0; flag 2 = see-through (not used: the normal mode is depth-tested) | `DisplayRenderer$TextDisplayRenderer.submitInner` 8-273 |
| 17 | passenger attachment points default to `(0, f(height), 0)`: a display (height 0) carries a passenger exactly at its own position; the client ticks a vehicle before its passengers | `EntityAttachment$Fallback`, `ClientLevel.tickNonPassenger` |
| 18 | `ServerPlayer.startRiding` sends `ClientboundSetPassengersPacket` to the player at once; the client shows `mount.onboard` through `Hud.setOverlayMessage` only when the player was not yet riding; an action bar packet uses the same slot | `ServerPlayer.startRiding` 79-82, `ClientPacketListener.handleSetEntityPassengersPacket`, `setActionBarText` |
| 19 | the client processes the queued packets of a frame in one drain (`PacketProcessor.processQueuedPackets` empties the queue; called once per frame in `Minecraft.runTick`) | `PacketProcessor.processQueuedPackets`, `Minecraft.runTick` 124 |
| 20 | the husk's textures are `textures/entity/zombie/husk.png` and `husk_baby.png` (64 × 64) and only the husk renderer names them | `HuskRenderer` constants, the jar's assets |

## Requests to other lanes
- **VB** (`core.py`): remove the Shift skip input (`core/skip`, `core/skip_cs1`, `core/skip_go`, `core/skip_cs1_go`,
  `core/skip_clear` and their calls in `intro_tick` / `tick` / the replay) or leave it: it is parked by `#skip hr -1`
  (`seq/<name>/skipin` sets it every tick; the sequences' starts too). `api.SKIP_HINT` (' · Shift 길게') and the kit's
  `fx/hud/skip` are no longer shown in a locked run; the hint text now lives in `seq.SKIP_KEY_HINT` (' · Space 길게').
  If the core keeps a skip of its own for another sequence: read `rlk:in_jump`, never `rlk:in_sneak`.
- **VB / the rig builder**: `rig/follow_now` is called by the sequences (`seq.RIG_NOW`); keep the name. Any core code that
  teleports her body inside a hook (`tp @s ...`, not `mboss/mv/*`) and expects the model to be there in the same tick
  needs the same line (`execute at @s rotated as @s rotated ~ 0 run function rlk:boss/scarlet/rig/follow_now`).
- **VB** (`build_mboss_hr_fx.py`, optional): `fx/hud/line` still draws the subtitle for the fight's line 12 and for runs
  without a held player; nothing needed for round V.
- **VP** (`rplint.py`, optional): the three blank textures are 64 x 64 RGBA with every alpha 0; rplint passes them today.
- **Lead**: `room/mob_summon` (hand file): the developer fallback `#mobTmp room 1` summons a VISIBLE husk, which the blank
  husk texture hides; switch that line to a zombie if the fallback is still wanted. The release pack must be built with
  `python3 tools/build_blank_tex.py --resourcepack <RP>` (README 0-4).
