# Minecraft Java 26.3 — cutscene-camera facts read from bytecode

Source: `client.jar` (version.json: id 26.3, protocol 777, data pack 121.0, resource pack 97.1) and the bundled
`server-26.3.jar`, disassembled with the JDK 25 `javap -c -p -constants`. No decompiler, nothing run.
Tags: **[V]** = read directly in bytecode (class/method named). **[I]** = inferred (combination of verified
pieces, or behaviour that only a running game can confirm).

Naming notes for this version: the HUD class is `net.minecraft.client.gui.Hud` (not `Gui`); entity types are
registered in `net.minecraft.world.entity.EntityTypes`; entity position sync was reworked
(`PositionPath`, `VecDelta`, `InterpolationHandler`, `InterpolationTracker`, `UpdateInterval`); spectator
left-click has its own packet (`ServerboundSpectatorActionPacket`).

---------------------------------------------------------------------------------------------------------

## 1. Camera of a spectated entity

**Where the camera comes from** — `Camera.update(DeltaTracker)` → `alignWithEntity(partialTick)`.

* [V] `Minecraft.getCameraEntity()` = `gameRenderer.mainCamera().entity()`; `setCameraEntity(e)` =
  `camera.setEntity(e)` + `gameRenderer.checkEntityPostEffect(e)`. `Camera.setEntity` only stores the field.
* [V] Partial tick: `getCameraEntityPartialTicks` = `1.0` if `tickRateManager.isEntityFrozen(entity)`, else
  `deltaTracker.getGameTimeDeltaPartialTick(true)`.
* [V] Rotation: `setRotation(entity.getViewYRot(pt), entity.getViewXRot(pt))`.
  * `Entity.getViewYRot(pt)` → `getYRot(pt)` = `Mth.rotLerp(pt, yRotO, yRot)`; `getViewXRot(pt)` → `Mth.lerp(pt, xRotO, xRot)`.
  * `LivingEntity.getViewYRot(pt)` = `Mth.rotLerp(pt, yHeadRotO, yHeadRot)` — **head yaw**, not body yaw.
    Pitch is still `xRot`. (`LocalPlayer.getViewYRot` = `getYRot(pt)`.)
* [V] Position: `lerp(pt, entity.xo, getX())` etc. (y adds `lerp(pt, eyeHeightOld, eyeHeight)`). Only special
  case is a passenger of a new-behaviour minecart.
* [V] Eye height is the camera's own smoothed copy: `Camera.tick()`:
  `eyeHeight += (entity.getEyeHeight() - eyeHeight) * 0.5f` once per client tick. `setEntity` does **not**
  reset it → every switch between camera entities with different eye heights glides vertically
  (halving the gap each tick, ~6 ticks to settle).
* [V] Eye heights: `Entity.getEyeHeight()` returns the dimension eye height; default = `height * 0.85`
  (`EntityDimensions.defaultEyeHeight`).
  * `item_display` / `text_display` / `block_display` / `interaction` / `marker`: `sized(0,0)` → **0.0** (camera exactly at the entity position).
  * `armor_stand`: `sized(0.5, 1.975).eyeHeight(1.7775)`; `Small` → 0.9875; **`Marker:1b` → `MARKER_DIMENSIONS = fixed(0,0)` → 0.0**.
  * player / mannequin: 1.62. So player → marker stand / display = a 1.62-block downward glide at cutscene start, and back up at the end.
* [V] `marker` entities cannot be a camera on the client: `clientTrackingRange(0)` and
  `Marker.getAddEntityPacket` throws `IllegalStateException("Markers should never be sent")`;
  `ClientPacketListener.handleSetCamera` ignores the packet when the entity id is unknown to the client.

**Third person (F5)**

* [V] `detached = !options.getCameraType().isFirstPerson()` — purely the client option, **not** tied to the
  camera entity being the player. Nothing in `setCameraEntity` / `handleSetCamera` changes the camera type, so
  the F5 state the player had is kept while spectating.
* [V] When detached: mirrored type → `setRotation(yRot + 180, -xRot)`; then
  ```
  f2 = 4.0f; f3 = 1.0f
  if (entity instanceof LivingEntity l) { f3 = l.getScale(); f2 = (float) l.getAttributeValue(CAMERA_DISTANCE); }
  f4 = f3; f5 = f2
  if (entity.isPassenger() && vehicle instanceof LivingEntity v) { f4 = v.getScale(); f5 = v.camera_distance }
  move(-getMaxZoom(max(f3*f2, f4*f5)), 0, 0)
  ```
  * Non-living camera entity (any display, interaction): **always 4.0 blocks pull-back**, cannot be changed
    (riding a LivingEntity can only raise it, because of `max`).
  * LivingEntity camera (armor stand, mannequin, mobs): `scale × camera_distance`. `camera_distance` is in
    `LivingEntity.createLivingAttributes()`: `RangedAttribute(default 4.0, min 0.0, max 32.0)`, syncable.
    Setting it to **0** on the camera entity gives `getMaxZoom(0) = 0` → no pull-back.
  * `getMaxZoom`: 8 rays (corner offsets ±0.1) from the camera point backwards, `ClipContext.Block.VISUAL`,
    fluids ignored; the distance is shortened to the nearest block hit.
* [V] In F5 the camera entity itself is drawn: `LevelExtractor` skips the camera entity only when
  `!camera.isDetached()` (or keeps it when sleeping). The `LocalPlayer` is drawn only when it is the camera entity.
* [V] Post-effect shader: `GameRenderer.checkEntityPostEffect(entity)` — `Creeper` → `creeper`, `Spider` →
  `spider`, `Enderman` → `invert`, anything else clears it. Called on `setCameraEntity`, and on the F5 key
  with `null` when leaving first person. Armor stands / displays get none.

**Consequence for today's rig [I]**: a player who is in F5-back during the cutscene sees it from 4 blocks behind
the armor stand (default `camera_distance` 4 × scale 1), shortened by blocks, and the invisible camera stand
itself is drawn (as a ghost, see 3). F5-front flips the view. This is not controllable from the server; only
the camera entity's `camera_distance`/`scale` are.

---------------------------------------------------------------------------------------------------------

## 2. Rotation precision and smoothness

### 2.1 Server — `ServerEntity.sendChanges()`

* [V] Called once per server tick per tracked entity in entity-ticking range (`ChunkMap.tick`). The movement
  block only runs when `entity.needsSync || updateInterval.test(tickCount) || entityData.isDirty()`.
  `UpdateInterval.periodic(n).test(t)` = `t % n == 0`; built in `ChunkMap` from `EntityType.updateInterval()`.
* [V] `EntityType.Builder` defaults: `clientTrackingRange = 5`, `updateInterval = 3`. Registrations:

  | type | updateInterval | clientTrackingRange (chunks) | eye height |
  |---|---|---|---|
  | armor_stand | 3 (default) | 10 | 1.7775 (marker 0) |
  | item/text/block_display | **1** | 10 | 0 |
  | interaction | 3 (default) | 10 | 0 |
  | marker | 3 | **0**, never sent | 0 |
  | mannequin, player | 2 | 32 | 1.62 |
  | husk | 3 (default) | 8 | 1.74 |

* [V] `needsSync` is set by `Entity.push`, **`Entity.load` (so every `data merge/modify entity`)** and various
  mob code; `teleportSetPosition` (i.e. `/tp`) does **not** set it. So an armor stand teleported every tick is
  still only sent every 3rd tick.
* [V] Rotation is packed with `Mth.packDegrees(f) = (byte) floor(f * 256 / 360)`; rotation flag =
  `|yaw byte − lastSentYRot| ≥ 1 || |pitch byte − lastSentXRot| ≥ 1`. Unpack = `b * 360 / 256` → 1.40625° grid, **floored**.
* [V] Position flag = `positionCodec.delta(pos).lengthSqr() >= 7.62939453125E-6 || tickCount % 60 == 0`.
* [V] Passenger: only `ClientboundMoveEntityPacket.Rot` (bytes) is ever sent; `wasRiding = true`.
* [V] Non-passenger → `createMovePacket(path, yawByte, pitchByte, pos, rot)`. It returns
  **`ClientboundEntityPositionSyncPacket` (double position, float yRot/xRot)** when any of:
  1. `entity.getRequiresPrecisePosition()` (setter referenced only by `Entity`, `HappyGhast`, `FallingBlockEntity`, `PrimedTnt`);
  2. `teleportDelay > 400` (counter +1 each time this branch runs, reset to 0 by every sync packet → a forced
     sync every 401st evaluation: ~20 s for displays, ~60 s for armor stands);
  3. `wasRiding` (first send after the entity stops being a passenger);
  4. **`wasOnGround != entity.onGround()`**;
  5. `pos` flag set and `VecDeltaCodec.tryEncode` fails: any axis delta `round(v*4096)` outside
     −32768…32767, i.e. **≥ ~8 blocks on one axis since the last sent position**
     (plus an `ItemEntity`-only precision rule).

  Otherwise `PosRot` / `Pos` / `Rot` (`ClientboundMoveEntityPacket`, position as shorts /4096, **rotation as
  bytes**) or nothing.
* [V] Head yaw: separately, `ClientboundRotateHeadPacket(entity, byte)` when the packed head yaw changed —
  **byte only, there is no float path for head yaw**.
* [V] Order inside the tick: movement packet first, then `sendDirtyEntityData()`. A `teleport_duration`
  changed in the same tick as the `tp` therefore reaches the client *after* the move it was meant for.
* [V] `Entity.sendTeleportTransitionToPlayers` (called by every same-dimension teleport): sends a float
  `ClientboundTeleportEntityPacket` to **players riding the teleported entity**, and to all trackers only if
  `!type.hasUpdateInterval() || getMoveSimulationType() == SERVER_AND_CLIENT` — not the case for displays or
  armor stands (default `AUTHORITATIVE_SIDE`, they have an interval).
* [V] **`TeleportCommand.performTeleport` ends with `entity.setOnGround(true)`** (for every entity that is not a
  fall-flying LivingEntity), and passes `resetCamera = true` to `teleportTo`.
* [V] `Entity.load` does `onGround = input.getBooleanOr("OnGround", false)`; `/data … entity` goes through
  `EntityDataAccessor.setData` → `entity.load(...)`. `Display.tick()` never calls `move()`, and a `Marker`
  or `NoGravity` armor stand has `hasPhysics() == false` → `travel` skipped, so nothing else rewrites `onGround`.

**Vanilla way to get float rotation to the client [V pieces, I as a whole — not run in game]:** make condition 4
true on the ticks you need it. After the first `tp` a display's `onGround` is stuck at `true`; so
* tick A: `tp @s …` then `data merge entity @s {OnGround:0b}` → flag false ≠ wasOnGround true → float sync;
* tick B: `tp @s …` only → flag true ≠ wasOnGround false → float sync;
* repeat A/B (the merge must come *after* the tp, and only on alternate uses, otherwise the flag does not flip).

This costs one entity NBT save+load on every other use. It only helps a **non-living** camera: a LivingEntity's
view yaw is the head yaw, which is byte-only.

### 2.2 Client

* [V] `handleMoveEntity` → `entity.moveOrInterpolateTo(path[, yRot, xRot])` (rotation only when the packet has it).
  `handleEntityPositionSync` → `moveOrInterpolateTo(path, yRot, xRot)` if the entity is ticking and the jump is
  `≤ 64` blocks (`distanceToSqr > 4096` → `snapTo`), then `setOnGround`.
* [V] `Entity.moveOrInterpolateTo` → `interpolationHandler.interpolateTo(...)`; if the handler returns false
  (`InterpolationHandler.NO_OP`, the default for entities without their own handler, e.g. `interaction`) →
  plain `setPos` / `setRot`.
* [V] Per client tick (`ClientLevel.tickNonPassenger` → `Entity.commonTick`): `setOldPosAndRot()`, then
  `getInterpolation().interpolate()`, `tickCount++`, then `tick()`. Rendering lerps old→current with the
  partial tick, so each tick's step is drawn as a straight, frame-rate-smooth segment.
* [V] `AbstractInterpolationHandler.interpolateTo`: `interpolationSteps == 0` → `entity.snapTo(...)` (old =
  new, no blend) and cancel; a packet whose target equals the active target is ignored (no restart);
  otherwise `startInterpolating` — **from the entity's current state**. Before every step,
  `adjustInterpolationTargetFromDeltas` shifts the stored target by whatever the entity moved/turned outside
  the handler (so a `snapTo` during an active interpolation carries the unfinished remainder along).

**Display entities** — `Display.createInterpolationHandler()` = `LinearInterpolationHandler.create(this, 0)`;
`onSyncedDataUpdated(DATA_POS_ROT_INTERPOLATION_DURATION_ID)` → `setInterpolationLength(teleport_duration)`.

* [V] `teleport_duration` NBT is clamped `0…59`.
* [V] `LinearInterpolationHandler.startInterpolating`: store target, `remainingSteps = interpolationSteps`.
  `doInterpolate`: `f = 1/remainingSteps`; `pos = lerp(pos, target, f)`, `yRot = rotLerp(f, yRot, targetYRot)`,
  `xRot = lerp(f, xRot, targetXRot)`; `remainingSteps--`. → **position and rotation are both interpolated,
  linearly, constant speed, N ticks.**
* [V] A new packet mid-interpolation (different target) resets `remainingSteps = N` and continues from the
  current interpolated state (no jump; speed changes). Changing `teleport_duration` only affects later starts.

**LivingEntity (armor stand)** — `LivingEntity.createInterpolationHandler()` =
`SteppedInterpolationHandler.create(this)`, `interpolationSteps = type.updateInterval()` (3 for armor stands).
On the server the same factory returns a `SteppedInterpolationTracker` that records the per-tick positions
between sends; the client replays that path (`InterpolationData.addSteps/getNewPositionAndRotation`),
rot-lerping body yaw/pitch across the path, with an adaptive catch-up speed.

* [V] Head yaw: `handleRotateMob` → `entity.lerpHeadTo(unpackDegrees(byte), 3)`; `LivingEntity.aiStep`:
  `while lerpHeadSteps > 0: yHeadRot = rotLerp(1/steps, yHeadRot, target); steps--`.
* [V] `ArmorStand` does not override `getViewYRot` or `lerpHeadRotationStep` → **the armor-stand camera's yaw is
  the head yaw: a byte (1.40625° grid), eased over 3 client ticks.** Pitch is `xRot`, also bytes in practice
  (float only inside a position-sync packet).

### 2.3 What a 0.07°/tick pan looks like

1.40625 / 0.07 = 20.1 ticks per byte step.

* **(c) armor stand, as today [V mechanics, I visual]:** the view yaw stands still for ~1 s, then moves 1.406°
  over 3 ticks (≈0.47°/tick for 150 ms), repeat. Sends happen only every 3rd tick, so the steps land every
  18 or 21 ticks. Position is smooth but ~3 ticks late. This is defect B.
* **(b) display, `tp` every tick, `teleport_duration` 1–3, no float trick:** position smooth (N=1: exact,
  one tick late; N=2/3: each tick closes 1/N of the gap → exponential smoothing, lag ≈ N−1 ticks). Yaw: the
  target still only changes once per ~20 ticks; N=1 → one 1.406° jump inside a single tick per second;
  N=2 → 0.70, 0.35, 0.18…°; N=3 → 0.47, 0.31, 0.21, 0.14…° per tick, then still. Smoother than (c) but a
  clear 1 Hz pulse. Averaging it away needs N ≈ 20 (≈1 s of lag, speed still rippling ~0.04–0.11°/tick).
* **(b′) same, with the `OnGround` flip every tick:** every tick carries exact float yaw/pitch → 0.07° per
  tick, drawn as straight segments at frame rate. [I] Residual risk is client/server tick phase jitter
  (a client tick that receives 0 or 2 updates): N=1 can hitch for one tick, N=2 hides it at one tick of lag.
* **(a) display, one `tp` per keyframe with `teleport_duration` N (≤59):** one constant-speed linear move of
  position and rotation per segment, rendered at frame rate — the smoothest result available.
  Without the float trick the end rotation is floored to the 1.40625° grid, so a 40-tick segment that should
  turn 2.8° turns 1.41°, 2.81° or 4.22°: continuous, but the speed changes from segment to segment (and a
  short segment can turn 0°). With the flip on the keyframe tick the endpoint is exact and the pan is a true
  0.07°/tick. Constraints: linear only (ease in/out = several segments); set N at least one tick before the
  first `tp` that should use it; the 60-tick keep-alive `Pos` packet is harmless (same target → ignored);
  the forced sync after 400 evaluations restarts an active segment only if no sync happened in the last
  400 ticks (each keyframe flip resets that counter).
* **Hard cuts with a display:** a jump > 64 blocks arrives as a sync packet and snaps; a shorter jump is
  interpolated with the current duration unless `teleport_duration` was 0 *before* that tick. A snap during
  an unfinished interpolation keeps drifting by the unfinished remainder (see 2.2). Switching between two
  already-positioned camera entities (as today) is the clean cut.

---------------------------------------------------------------------------------------------------------

## 3. Spectator rendering of invisible entities

* [V] `Entity.isInvisibleTo(Player p)`: `if (p.isSpectator()) return false;` then same-team
  `canSeeFriendlyInvisibles()` → false; else `isInvisible()`. **The spectator test is first and unconditional.**
* [V] `LivingEntityRenderer.extractRenderState`: `isInvisibleToPlayer = isInvisible && entity.isInvisibleTo(Minecraft.player)`
  — the local player, not the camera entity.
* [V] `LivingEntityRenderer.submit`: `visible = !isInvisible`; `translucent = !visible && !isInvisibleToPlayer`;
  `getRenderType(state, visible, translucent, glowing)` → translucent ⇒ `RenderTypes.entityTranslucentCull(texture)`;
  colour `translucent ? 654311423 (0x26FFFFFF, alpha 38/255 ≈ 15%) : -1`. Null (nothing drawn) only when
  not visible, not translucent, not glowing.
* [V] Affected: every `LivingEntityRenderer` subclass — husk/zombie, mannequin/player (`AvatarRenderer`), mobs,
  armor stands. `ArmorStandRenderer.getRenderType` special-cases `isMarker` but still returns
  `entityTranslucent(texture, false)` when translucent → **marker armor stands are ghosted too.**
  Only `LivingEntityRenderer` and `LivingEntityRenderState` reference `isInvisibleTo`.
* [V] Layers (armor, held/head items) run regardless (`shouldRenderLayers` = true) — same as outside spectator.
* [V] Shadows: `EntityRenderer.extractShadow` is skipped when `state.isInvisible` — no shadow for invisible
  entities, spectator or not. Name tags: `LivingEntityRenderer.shouldShowName` uses `isInvisibleTo(player)`,
  so a spectator can also see names that invisibility would hide; never for the camera entity itself
  (`entity != getCameraEntity()`); armor stands only when `CustomNameVisible`.
* [V] Displays, interactions, markers: unchanged for spectators. `DisplayRenderer` has no invisibility or
  spectator reference; `interaction` and `marker` are registered with `NoopRenderer`; markers are never sent.
* [V] `scale` attribute: `RangedAttribute(default 1.0, min 0.0625, max 16.0)`.

**Is there a vanilla state that hides an invisible living entity from a spectator?** [V] No flag does: team
options only add visibility, `Marker`, passenger state and glowing do not enter the decision. What does work:

1. [V] **Transparent texture from the resource pack.** The ghost is the entity's normal texture; `entity.fsh`
   does `if (color.a < ALPHA_CUTOUT) discard;` on the *texture* alpha before the 15% tint, and alpha 0 blends
   to nothing anyway. A fully transparent `textures/entity/zombie/husk.png` (if husks are only used as hit
   boxes) / `textures/entity/armorstand/wood.png` makes the ghost disappear. Mannequins: `PlayerSkin.Patch`
   has a `texture` field (resource-pack asset id) → a transparent skin [V field exists, I that it fully
   replaces the skin texture path].
2. [V] **Don't use a LivingEntity**: an `interaction` entity draws nothing, a display draws only its content.
3. [V] **Shrink**: `Entity.shouldRenderAtSqrDistance`: drawn only within `bbox.getSize() * 64 * viewScale`
   blocks; `viewScale = clamp(renderDistance/8, 1, 2.5) × entityDistanceScaling`. A husk at scale 0.0625 has
   an average edge of ~0.066 → ~4 blocks × viewScale, and is 12 cm tall inside that. (A marker armor stand
   has its own rule: size 0 → 4.0 → 256 × viewScale blocks, so shrinking does not hide it.)
4. [I] Move them out of sight / out of tracking range for the duration.

---------------------------------------------------------------------------------------------------------

## 4. Left-click and other inputs while spectating

**The click path**

* [V] `Minecraft.pick(pt)`: `hitResult = player.raycastHitResult(pt, getCameraEntity())`.
  `LocalPlayer.raycastHitResult` → `pick(cameraEntity, blockInteractionRange(), entityInteractionRange(), pt)`:
  origin = **camera entity** eye position and view vector (not the pulled-back F5 camera); ranges = the
  **local player's** attributes. Entity candidates: `EntitySelector.CAN_BE_PICKED` (not spectator, `isPickable()`).
  The entity hit is finally passed through `filterHitResult(hit, eye, entityRange)`:
  `if (!location.closerThan(eye, range)) → BlockHitResult.miss`; `closerThan` is strict `distSqr < range²`.
* [V] The item `attack_range` branch is dead in spectator: `LivingEntity.getActiveItem()` returns `EMPTY` for spectators.
* [V] `Minecraft.startAttack()`: `if (gameMode.isSpectator()) { hit instanceof EntityHitResult ?
  gameMode.spectate(entity) : gameMode.spectatorNoAction(); return true; }` → `ServerboundSpectatorActionPacket(OptionalInt id)`.
* [V] Server `handleSpectatorAction`: needs `player.isSpectator()`, entity inside the world border,
  `player.isWithinEntityInteractionRange(entity.getBoundingBox(), 3.0)` (range = attribute + 3.0, measured from
  the server player, which sits at the camera), and `entity.isPickable()` → **`player.setCamera(entity)`**.
  This is defect C. `handleAttack` returns immediately for spectators.
* [V] Pickable: living entities (husk, mannequin, non-marker armor stand), `interaction`. Not pickable:
  marker armor stands (`ArmorStand.isPickable` = `super && !isMarker()`), displays (no override).
* [V] `entity_interaction_range`: `RangedAttribute(default 3.0, min 0.0, max 64.0)`, syncable, part of
  `createLivingAttributes`. `Player.entityInteractionRange()` is just the attribute value.
  **Setting the player's value to 0 makes `closerThan(eye, 0)` always false → every entity pick becomes a
  miss on the client → left-click sends `spectatorNoAction`, which the server ignores.** (A modified client
  could still send the packet; the server would then allow entities within 3.0 blocks.) It also removes the
  entity-hover crosshair. Block picks (`block_interaction_range`) continue and are harmless.

**`ServerPlayer.setCamera(e)`** [V]: no-op if unchanged (so a per-tick `spectate` hold costs nothing); otherwise
`teleportTo(camera.level, camera.x, y, z, {}, ownYRot, ownXRot, false)`, `chunkSource.move(this)`,
`ClientboundSetCameraPacket`, `connection.resetPosition()`.
`SpectateCommand` refuses non-spectators (`commands.spectate.not_spectator`).

**What ends spectating** [V]

* Sneak — server side: the client always sends `ServerboundPlayerInputPacket` when key state changes
  (`LocalPlayer.sendChanges`, independent of the camera); `handlePlayerInput` → `setShiftKeyDown`;
  `ServerPlayer.tick()`: camera ≠ self and alive → `absSnapTo(camera pos + rot)`, `chunkSource.move`,
  `if (wantsToStopRiding()) setCamera(this)` (`Player.wantsToStopRiding` = `isShiftKeyDown()`). The player is
  left at the camera's position. Nothing can veto it; the per-tick `spectate` puts it back on the next tick.
* Camera entity not alive → `setCamera(this)`.
* **Any `/tp` of the player** — `TeleportCommand` passes `resetCamera = true`; `ServerPlayer.teleportTo` then
  calls `setCamera(this)`. Same for the spectator menu's teleport (`handleTeleportToEntityPacket`).
* `setGameMode(non-spectator)` → `setCamera(this)`. (Switching *to* spectator calls `stopRiding()`.)
* Distance: no check — the player is snapped onto the camera every tick, which also drives chunk loading and
  entity tracking (`ChunkMap.TrackedEntity.updatePlayer` uses `player.position()`).
* Client side: nothing resets the camera when the entity is merely removed from the client world [I].

**Other spectator inputs** [V] (`Minecraft.handleKeybinds`, `MouseHandler.onScroll`, `SpectatorGui`)

* Hotbar keys 1–9: `hud.getSpectatorGui().onHotbarSelected(i)` → opens / selects in the client-side spectator
  menu (teleport to player / team). Choosing a target sends `ServerboundTeleportToEntityPacket` → ends the spectate.
* Middle click: two bindings share mouse button 2 — `key.pickItem` → `pickBlockOrEntity()`, and
  `key.spectatorHotbar` → `SpectatorGui.onHotbarActionKeyPressed()` (opens the menu / confirms the selected slot).
* Mouse wheel: menu open → `SpectatorGui.onMouseScrolled`; otherwise changes `abilities.flyingSpeed`
  (clamped 0.005…0.2).
* F5 toggles perspective as usual; inventory key opens the inventory screen; drop and swap-offhand are
  skipped for spectators. `key.toggleSpectatorShaderEffects` toggles the mob shader.
* All of this is client-only; **no server-side way to suppress it**. The menu only appears when a key is pressed.

---------------------------------------------------------------------------------------------------------

## 5. Non-spectator alternative (adventure + `rotate` / `tp` every tick)

* [V] `handleMovePlayer` (`ClientboundPlayerPositionPacket`): ignored for position if the player is a passenger;
  otherwise `setValuesFromPositionPacket(change, relatives, player, false)` → `setPos`, `setYRot`, `setXRot`
  and the old pos/rot are moved with them → **snap, no interpolation**; then the accept packet.
* [V] `handleRotatePlayer` (`ClientboundPlayerRotationPacket`): `setYRot`, `setXRot`, `setOldRot()` → **snap**;
  answers with a `ServerboundMovePlayerPacket.Rot`.
* [V] Mouse: `MouseHandler.turnPlayer` calls `player.turn(dx, dy)` every frame whenever the mouse is grabbed —
  no dependence on game mode or camera entity. Between two server corrections the view follows the mouse.
* [V] Riding: a passenger's position is `vehicle.positionRider(...)` each client tick, so it follows the
  vehicle's interpolated motion (a display with `teleport_duration` → smooth). Riders additionally get the
  float `ClientboundTeleportEntityPacket` for every vehicle teleport, applied through the same handler.
  The rider's **view rotation stays its own** (mouse); `LocalPlayer.getViewYRot` = `getYRot(pt)`.
  Mounting shows the `mount.onboard` action-bar message (`handleSetEntityPassengersPacket`).
* [V] Sneak always dismounts, server side: `Player.rideTick`: `if (!clientSide && wantsToStopRiding() && isPassenger()) stopRiding()`.
* [V] F5 with the *player's* `camera_distance` = 0: pull-back 0, so the view is at the eye, but the camera is
  "detached": no first-person hand (`GameRenderer.renderItemInHand` needs first person, HUD not hidden, mode
  ≠ spectator), no crosshair (`Hud.extractCrosshair` needs first person), and the player's own model/equipment
  is drawn at the camera.
* [V] HUD (`Hud.extractRenderState`), in order, each bracket a later GUI stratum:
  `[camera overlays (vignette, pumpkin, spyglass…), crosshair]` → `[hotbar + decorations, effect icons, boss bar]`
  → sleep overlay → demo → scoreboard sidebar → **action bar** → **title / subtitle** (title scaled ×4) → chat →
  tab list → subtitles. So a title glyph covers hotbar, hearts, crosshair, boss bar, sidebar and action bar;
  it does not cover chat or the tab list.
  * Adventure: item hotbar, hearts/armor/food (`gameMode.canHurtPlayer()`), XP/contextual bar, selected-item
    name, crosshair and hand in first person.
  * Spectator: `SpectatorGui.extractHotbar` only (visible only while the menu is open), no hearts, crosshair
    only on an entity that is a `MenuProvider` or an interactable block, no hand. Boss bar, effects, title,
    action bar the same in both. Hotbar/hearts also need the camera entity to be a `Player` (`getCameraPlayer`).

**Verdict [I]:** it cannot look as locked or as clean as `spectate`. Rotation arrives as 20 Hz snaps with no
interpolation, the mouse turns the view freely between them (visible jitter whenever the player touches the
mouse), sneak dismounts, and the survival HUD is on screen unless a title glyph is used to cover it. Position
alone can be made smooth by riding a display. Usable for "player keeps looking around from a fixed seat",
not for an authored camera.

---------------------------------------------------------------------------------------------------------

## 6. Slow motion (`tick`)

* [V] `TickCommand.register`: `literal("tick").requires(hasPermission(Commands.LEVEL_ADMINS))` =
  `Permissions.COMMANDS_ADMIN` = `PermissionLevel.ADMINS` (level 3). `rate` argument is a float `1.0 … 10000.0`.
* [V] Functions are parsed with `Commands.createCompilationContext(functionCompilationPermissions)`
  (`ServerFunctionLibrary`); brigadier checks `node.canUse(source)` only while parsing (`CommandDispatcher.parseNodes`)
  — there is no permission re-check in the function execution classes.
  * Integrated server: `IntegratedServer.getFunctionCompilationPermissions()` returns the constant
    `LevelBasedPermissionSet.GAMEMASTER` (level 2); world loading uses the same constant
    (`WorldOpenFlows`, `CreateWorldScreen`). → **a function containing `tick …` does not parse in single
    player; that function fails to load.** No setting changes this.
  * Dedicated server: `function-permission-level` in server.properties, default `GAMEMASTER` (2). With 3 or 4
    the command compiles and then runs from the tick tag (the runtime source `ServerFunctionManager.getGameLoopSender`
    is GAMEMASTER, but nothing checks it at run time).
* [V] Client: `handleTickingState` sets the client `TickRateManager`; `Minecraft.getTickTargetMillis(f)` =
  `runsNormally() ? max(f, millisecondsPerTick()) : f`. Below 20 TPS the client's own ticks and partial ticks
  stretch with the server → real, smooth slow motion for everything tick-based (entity interpolation, display
  `interpolation_duration` — `Display.calculateInterpolationProgress` counts client ticks —, the player's own
  movement). Mouse look stays real-time. Above 20 TPS the client stays at 50 ms. `tick freeze`: players (and
  entities carrying players) keep ticking (`TickRateManager.isEntityFrozen`).
* So `tick rate 10` for half a second would be genuine slow motion — but it is not reachable from a datapack
  in single player.

---------------------------------------------------------------------------------------------------------

## 7. Fonts (bitmap provider)

* [V] `FontTexture.SIZE = 256`; `add()` asks `DynamicAtlasTree.insert(pixelWidth, pixelHeight, spacing 1)`,
  which fails when `w > 256 || h > 256` → returns null. `GlyphStitcher.stitch` then creates a fresh 256×256
  texture and tries once more; still null for an oversized glyph.
* [V] `FontSet`'s wrapped stitcher: `Objects.requireNonNullElse(stitcher.stitch(info, bitmap), missingGlyph)` →
  **an oversized glyph silently becomes the missing-glyph box.** No exception, the font and its other
  glyphs stay; the result is cached per glyph (`DelayedBake`), one empty atlas page is wasted.
* [V] The size that counts is the **source cell in pixels**: `BitmapProvider.Definition.load`:
  `cellW = imageWidth / columns`, `cellH = imageHeight / rows`; the uploaded bitmap is `cellW × cellH`
  whatever `height` says. So exactly 256×256 fits, 257 does not.
* [V] `scale = height / cellH` (oversample = 1/scale); advance = `(int)(0.5 + actualWidth * scale) + 1`, where
  `actualWidth` is found by scanning for the right-most non-transparent column; bearing top = `ascent`.
* [V] Codec: `height` optional, default 8, no range check; `ascent` required; validation error if
  `ascent > height`; `chars` rows must be non-empty and equal length. A codec error is logged as
  `Unable to load font '{}' in {} in resourcepack: '{}'` (that font file from that pack is skipped) [V string, I scope];
  a provider that throws while loading: `Failed to load builder {}, rejecting`.
* [I] Anything larger than 256 px in either direction has to be cut into several glyphs.

---------------------------------------------------------------------------------------------------------

## 8. Other things in these code paths that bite a spectate camera

1. **Eye-height glide** [V]: section 1 — 1.62 blocks over ~6 ticks at the first and last cut between the
   player and a zero-eye-height camera entity. Cover it (fade) or accept it.
2. **F5** [V]: section 1 — 4-block pull-back for any non-living camera, `scale × camera_distance` for a living
   one, block-clipped; F5-front mirrors; the camera entity is drawn in F5.
3. **`SetCamera` to an entity the client does not have** [V]: `handleSetCamera` silently ignores it, while the
   server already considers the camera set, so re-issuing `spectate` is a no-op and the client stays on the old
   view. The target must already be tracked by that client (within `clientTrackingRange × 16` blocks of the
   player = current camera, capped by view distance, chunk sent) when the cut happens.
4. **The player is physically at the camera** on the server every tick [V]: everything keyed on the player's
   position (selectors, an avatar that follows the player, distance checks) sees the camera position; when
   the spectate ends the player stands where the camera was.
5. **`tp` of the player ends the spectate** [V] (section 4). Useful as the exit, harmful mid-cutscene.
6. **FOV** [V]: `Camera.tickFov` uses `getFieldOfViewModifier` only while the camera entity is an
   `AbstractClientPlayer`, otherwise target 1.0, eased by 0.5 per tick → a short FOV change at the cut if the
   player was sprinting or had a speed modifier.
7. **Sound listener** [V]: `soundManager.updateSource(gameRenderer.mainCamera())` — the listener is the camera
   (including the F5 pull-back), not the player.
8. **Hand / crosshair** [V]: none in spectator (section 5).
9. **Display cuts and durations** [V]: `teleport_duration` set in the same tick as the `tp` applies one move late;
   jumps ≤ 64 blocks are interpolated, > 64 snap (section 2).
10. **`/posteffect add <targets> <id>`** exists in 26.3 [V] (`PostEffectCommand`, permission level 2,
    `ServerPlayer.addPostEffect` → `ClientboundPostEffectsPacket` → `LocalPlayer.setActivePostEffects`):
    resource-pack post chains can be switched per player from functions (fade, letterbox, grading) without
    spending the title slot. Not examined further.

---------------------------------------------------------------------------------------------------------

## Recommendation

Keep spectator + `spectate` (nothing else gives a locked view), but replace the armor stands with two empty
`item_display` camera entities and drive them by keyframes: `teleport_duration` N fixed at summon (or set a
tick earlier), one `tp` per segment plus the `OnGround` flip on that tick so the endpoint arrives as float,
per-tick `tp` with duration 2 and the flip only for curved moves, hard cuts by switching between the two
entities. That removes the byte-quantised, 3-tick-eased head yaw that causes B. For C, set the player's
`entity_interaction_range` base to 0 for the duration and restore it afterwards; keep the per-tick `spectate`
for sneak. For A, the camera entities themselves no longer draw anything; the remaining invisible living
entities (husk hit box, mannequins) need one of: a fully transparent texture in the shipped resource pack,
replacement by `interaction` entities, or being shrunk / moved away while the cutscene runs.
**Not verified from bytecode, check in game first:** (1) the `OnGround` flip end to end — each link is read,
the whole was not run, including that `data merge` with a real change always reaches `Entity.load`;
(2) that players are in F5-back: a display camera is then viewed from 4 blocks behind the entity along the
view axis (less if a block is in the way), exactly like today's armor stand at default `camera_distance`, so
shots must be authored with the entity 4 blocks ahead of the intended viewpoint — if first person and F5 must
match, only a living camera with `camera_distance` 0 does that, and it brings the byte yaw back;
(3) per-tick update delivery jitter between client and server ticks at `teleport_duration` 1;
(4) that a transparent texture is acceptable for every use of that entity type in the map, and that the
mannequin `profile.texture` override replaces the skin fully; (5) the eye-height glide and FOV ease at the
first/last cut look acceptable or are covered by a fade.
