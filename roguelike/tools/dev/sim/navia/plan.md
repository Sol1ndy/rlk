# Navia + sheathed weapons: decisions (source of truth for every implementing agent)

Roots:
- `DP` = `/home/user/rlk/roguelike` (git repo root is `/home/user/rlk`, branch `claude/exciting-pascal-ek1vuy`).
- `U` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/navia/understand`. Research reports live here: `rig.md`, `navia.md`, `weapon.md`, `audio_fx.md`, `back.md`, `sheath.md`, `critic.md`, `v1.md`-`v10.md`. Each report's addendum overrides its body.
- `RP` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/rp_final5`, the unpacked resource pack and the deliverable source. Never build into it from a sandbox. Copy it.
- Renderer: `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/preview/raiden_preview.py`; overlay helper `U/fx_markers.py`.
- Reference images: `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/images/`:
  - `4.png`: Navia's weapon;
  - `5.webp`, `6.webp`, `7.webp`: Arlecchino, Skirk and Navia with the weapon on the back.
- Videos: `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/navia/vid/`.

Rules carried from the project:
- Edit generators in `DP/tools/`, never their outputs. The outputs are `DP/data/rlk/function/char/motion/**`, except the hand-maintained `events/` and `*_fx/` files.
- Sounds are compositions of vanilla Minecraft sound events. The videos' audio is reference only.
- Datapack text the player sees and the README are in Korean.
- Macro lines (`$`) must contain at least one `$(var)`, and a line using `$(var)` must start with `$`.
- Run `python3 /tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/check_refs.py` and `check_macro.py` on the datapack you touched.
- Do not put model identifiers in commits. Commit message trailer (exactly):
  `<세션이 정해 준 trailer>`.

## D1. Navia's weapon: the halberd from 4.png
- Build it exactly as `weapon.md` §10-§11 specifies.
  - Model name `navia_halberd`.
  - Grip under the lower gold ring. The head is the "blade" for claymore-style swings. The crescent is on model −X.
- No `halberd_geo` variant. The Geo passive shows only through fx accents.
- Per-character size multiplier: `characters.navia.weaponScale = 1.25` (D5).
- First person keeps the existing `rlk:claymore` item (vanilla-precedent, as for Arlecchino and Skirk). Not restyled in this pass.

## D2. Parasol: rig weapon models swapped per frame
- `navia_parasol` (closed) and `navia_parasol_open`, built to `weapon.md` addendum §A1.
  - Grip `[8,8,8]` at the handle. The muzzle/ferrule is at +Y.
  - Closed length about 17-18 units. Open canopy about 18-19 units across, made from `cap` discs of thin painted boxes.
- The NA4 float uses `navia_parasol_open` with a larger `weapon_scale` (about 1.7). There is no separate model.
- The block-display umbrella gun (`F/char/navia/gun_*`, tag `rlk_nvgun`) is shown only while the rig is not visible (`pmVisible` ≠ 1), i.e. first person. Otherwise two parasols show.

## D3. Weapon attachment modes (generator, per frame, sticky like `hidden`)
`weapon_attach`: `"hand"` (default) | `"back"` | `"world"`.

**hand**
- Today's behaviour: right forearm, plus `weapon_shift` and the `weapon` euler.

**back**
- Torso frame from the neck point `top`, using the character's `sheath` config (`sheath.md` §4.1):
  `t = top + rot(body, sheath.offset)`, `q = body · quat(sheath.euler)`.
- `weapon`/`weapon_shift` are ignored. `weapon_scale` still applies.
- Per-weapon overrides go in `sheath.weapons[<name>]`.

**world**
- A detached weapon (Navia's NA3 thrown claymore, Skirk's floating sword in her put-away).
- Placed in the clip's own frame: feet origin, the rig's yaw.
  `t = weapon_shift` (blocks, authored space), `q = quat(weapon)`.
- **Not** affected by `shift`, `root` or the torso.

**All modes**
- The Z-mirror and the item-display conventions apply exactly as for the other parts.
- `scythe_loco` applies only in `hand`.
- Never interpolate across an attach change. The frame where the attach changes must snap the weapon: emit `interpolation_duration:0` for the weapon line on that tick, or author `weapon_scale` 0 around it.

## D4. Sheathed/drawn state machine (all rig characters)
Implement `sheath.md` §3-§4 as designed, with these decisions:
- **States:** `pmSheath` 0 drawn / 1 sheathed / 2 put-away clip running. Unset counts as 1. The rig spawns sheathed.
- **Delay N:**
  - `#pmShDelay tmp` defaults to 100 ticks (5 s).
  - Per-character `sheath.delay` in `<char>.json`: arle 100, skirk 100, navia 110.
  - The countdown runs only while drawn and no clip is active.
- **When N runs out:**
  - Idle on the ground: play `<char>/sheathe` (put-away clip, avatar-yaw basis).
  - Moving, airborne or first person: quick stow. Gold sparkle at the hand, the weapon hides, then grows back on the back.
- **Drawing:** any drawn clip (attacks, skills, bursts unless flagged) draws instantly. The weapon snaps to the hand with no back→hand flight, plus a small gold sparkle at the hand.
- **Dash:** `weapon_state:"sheathed"` for every character. The weapon is on the back during the dash, and a drawn weapon is quick-stowed first. Arlecchino's and Skirk's dash arms are re-authored as free-hand poses from v7 (`U/v7.md`).
- **Ending sheathed:** a drawn clip may end with the weapon on the back. A per-frame `weapon_attach:"back"` at t>0 sets `pmSheath 1` (and `"hand"` sets 0). Navia's NA4, skill and burst end this way: the halberd re-forms on the back (v6, v2 P22).
- **Arlecchino `burst`:** `weapon_state:"sheathed"`. The scythe hangs on the back while she casts empty-handed; drop the 0.001 hide.
- **Skirk:**
  - `burst_metsu` keeps its authored in-clip hide/redraw (drawn).
  - Seven-Phase Flash (`skM`) does **not** hold the weapon drawn.
- **Back mounts:**
  - Arlecchino and Skirk follow `back.md`, which is newer than `sheath.md` §2. If the two disagree, use `back.md`'s final values and check the render against photos 5/6.
  - Navia follows photo 7: the grip end up over her right shoulder, the head down-left about 20° from vertical, the head near the left foot. Re-measure with the real model.
- **Sheathed locomotion:** `idle_s` / `walk_s` / `run_s` / `air_s` loco sets with relaxed empty-hand arms (no gripping fist pose).
- **First person:** state only. The held item is unchanged.

## D5. Generalise the generators (no hard-coded 3/5)
`build_player_rig.mjs` and `build_player_locomotion.mjs` currently hard-code Skirk 3 and Arlecchino 5:
- the `tick` gate;
- `loco/context`;
- `loco/weapon`;
- the `weapons` list;
- `scythe_loco:char==='arle'`;
- the brightness list.

Drive all of these from the `characters` table so adding Navia is data-only. Each character declares:
- `id`, `skin`, `weapon` (default), `weaponScale` (default 1);
- `scytheLoco` (bool);
- `glow` (weapon names given brightness 15);
- `locoWeapons`: an ordered list of `{weapon, if}`, where `if` is an optional execute condition string such as `"score @s arM matches 1.."`.

`characters[c].weaponScale` multiplies every sampled `weapon_scale`: clip poses, spawn lines, loco, the back mount and the world attach.

## D6. Navia clips (phase 2; names keep attack-speed scaling)
- **Normal attacks:** `physical_1`..`physical_4`.
  - `playback_rate` 150 (Arlecchino precedent, close to today's 9/9/11/13 cadence).
  - Geo passive (`nvP`) changes fx accents only.
- **NA3:** drag, plant, kick, then the claymore cartwheels at the target and dissolves. Uses `weapon_attach:"world"`.
  - **Three** hits at ≈13/15/17 (1.0× ticks). Needs a third pending-hit slot in `M/combat` (`rig.md` addendum §4).
- **NA4:** parasol shot plus float. The parasol is closed, then open (scale ≈1.7), then closed.
  - Root `shift` rises ≈1.1-1.4 blocks and returns to 0.
  - Total ≈32 ticks at 1.0×. Ends with the halberd re-forming on the back.
- **Skill:**
  - tap `skill` ≈34 ticks, shot at tick 7;
  - hold `skill_aim_in` ≈16, then `skill_aim` loop, then `skill_fire` ≈24 with the blast at +3.
  - Damage moves to a clip event on the shot tick (Arlecchino `skill_go` pattern) with a lock until then. The pitch-dependent muzzle fx stay in `F/char/navia/fire.mcfunction`.
  - All use the parasol and end with the halberd on the back.
- **Burst:** ≈54 ticks compressed, blast at 34 (`buT 34`). No body turn. Parasol on the shoulder, then the halberd re-forms on the back at the end.
- **Dash:** from v7, ≈12 ticks. `weapon_state:"sheathed"`. Gold rose / ribbon / petal fx.
- **Put-away:** `sheathe` from v10, ≈34 ticks, physically placed on the back with no dissolve.
- **Locomotion:**
  - `idle/walk/run/air` (drawn, halberd shouldered or angled up; it must not sink into the floor);
  - plus `_s` sets, from v7 (walk/run/idle with no weapon).
- **NA cadence/recovery:** recoveries are compressed and cancellable as in `critic.md` §7. Skip the C2 follow-up shells and Surging Blade.

## D7. Fx and sound (phase 2)
- **Fx:** particles composed per clip tick in `M/navia_fx/<clip>/t<NN>`, in gold Geo colours (`#F6D57A`, `#E9B949`, `#FFF3C4` cores).
  - Signature shapes that read badly as dust (rose emblem, starburst flash, crescent ribbon) may use short-lived gold `item_display` cards painted by a small generator. The Raiden card engine is the precedent; it must use its own paths, owner tag and cleanup.
- **Legacy:** turn off the legacy Navia particle arcs and the legacy fx sounds for `#charN 6`.
- **Sounds:** `tools/player_motion/audio_navia.py`, wired into `tools/build_player_audio.py`.
  - Vanilla events only, validated against those already used in the pack (`U/../dp_sound_events.txt`) or well-known vanilla ids.
  - Gameplay sounds that the clip now owns are removed or gated, never doubled.

## D8. v10 corrections (Navia put-away; overrides D6 "physically placed")
- `sheathe` follows `U/v10.md`:
  - lift the weapon onto the right shoulder;
  - a forward wrist wheel;
  - flip over the palm;
  - plant it point-down in front of the left hip (mirrored as a right-hand plant; no left-hand slot);
  - gold dissolve at about +42;
  - back speck at about +48;
  - the silhouette grows on the back over about 20 ticks.
- Total about 60-68 ticks; the clip may end once the back re-form completes.
- The halberd head must not sink into the floor at the plant: raise the hand so the spear tip just touches the floor.
- Put-away delay: v10 measures about 95 ticks after the recovery ends, which matches Skirk. Navia `sheath.delay` is 100.
- After N3 (thrown weapon) or the parasol moves: the halberd re-forms on the back at the end of the clip, as D4 says. This replaces Genshin's "stand still 0.6 s" rule, so the weapon is on the back while moving too.

## D9. User feedback on dash arms (binding for Navia's dash)
- The user rejected arms raised above the head and a boxing-guard dash (Arlecchino and Skirk, fixed in commit 6fc64d7). Every dash must use a **running-start arm swing**:
  - elbows bent about 55-75°;
  - the arm opposite the leading leg goes forward with the hand at chest height (world angle about +35° forward of vertical);
  - the other arm goes back and low (about −38°);
  - arms stay close to the body;
  - angles are compensated for the clip's forward lean.
- Reference implementation: the dash clips in `tools/player_motion/arle.json` and `skirk.json` on the main branch, and the helper `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/dashfix/run_arms.py`.
- The gold rose, ribbon and petal fx stay. The pose itself must read as "starting to run", not the Genshin claws-out pose.

## D10. In-game load error found by the user (fixed on main, 00e72e2)
- `items/tune/apply_loop` used `q[0]{m:"d"}`. Minecraft rejects a compound filter right after a list index.
- New checker: `python3 /tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/check_nbtpath.py <datapack data dir>` validates every NBT path argument. Run it with check_refs and check_macro, and keep the result at 0 invalid.
- Main must be merged into wip/navia before release.

## D11. Timing fix after the user's in-game video (binding; spec at navia/mc1/retiming_spec.md)
- User feedback:
  - the moves are too fast;
  - a claymore must swing heavily;
  - the NA4 canopy vanishes too fast;
  - after each of NA1-NA4 the return to idle is far too short;
  - the attack timing should match Genshin.
- Normal attacks use playback_rate 100. Each NA gets its full Genshin recovery tail (idle is reached 46/53/~27/50 ticks after the hit). chain_tick stays at Genshin's earliest next attack: 14 / 14 / 19 / 28 (NA4 chains at landing, so there is no mid-air cancel).
- Heavy feel: anticipation hold, fast strike, half-speed follow-through, a hang, then a slow settle (retime.py time-warp).
- NA4: the canopy stays open for 15 ticks.
- skill, skill_fire and burst get longer recovery tails. Their shot, blast and lock ticks do not change.
- Approved new event lines:
  - cboIdle 0 during the NA tails, so a click continues the string;
  - moving or jumping from the chain tick on ends the tail (finish / sheath/abort);
  - burst: the same cancel from tick 45.
- Coefficients keep today's DPS: NA 256 / 239 / 94×3 / 366 (main-session decision; was 150/140/55×3/215).
- Fixes from the video:
  - the NA4 open canopy is smaller (about 1.2-1.3×, not 1.7) so it does not cover the camera;
  - the backflip rises without moving toward the camera;
  - no grey vanilla sweep particles for Navia's skill shots (combat/apply.mcfunction:51 gate).

## D12. Faster Navia, and no moving or jumping while swinging (binding; all characters)
- User feedback:
  - Navia's attack speed up about 30%, with lower coefficients;
  - no jumping and no moving during an attack;
  - in a gap between hits (like NA1 → NA2) moving is allowed, but a jump makes the next attack hit 1;
  - the last two rules apply to every character.
- **Navia speed:** `playback_rate` 130 on `physical_1`..`physical_4` (the Arlecchino mechanism: pmSpeed = atkSpeed × 130 / 100,
  clamped 25..500). Authored ticks (hit_ticks, chain_tick, events, audio LAYERS, navia_fx tick files) are unchanged and stay
  in step. At atkSpeed 100: hits at game ticks 6 / 5 / 10-12-13 / 9 after each click, next input 11 / 11 / 15 / 22
  (`ceil(100 × chain / 130)`), string 59 game ticks (was 75). NA4 still lands on its chain tick (authored 28 = chain 28).
  - Game-tick timings checked: the NA4 float, landing and canopy are clip poses (authored ticks; canopy open 15 authored ticks
    = 11.5 game ticks); `#pmChainOpen` and the tail-cancel event lines follow atkCD and pmTick; `cboIdle` stays 0 through
    the tails; the 20-tick combo reset is unchanged. Gold card lifetimes and falling petals are game ticks by design.
  - `#naD` in `char/navia/na_coef` has no effect on Navia (the rig path sets atkCD from chain_tick; combo_after1/2 skip
    atkCD while `#pmResolving`).
  - Rig limit: at most 2 authored ticks per game tick keep every Navia NA rotation correct up to atkSpeed ~153 %
    (pmSpeed 200). From pmSpeed 201 (3 ticks on some game ticks) the NA1/NA2 strike and the NA4 backflip can show a
    one-tick reversed blend on their fastest ticks (visual only; at playback 100 this started at atkSpeed 201 %).
- **Navia coefficients:** 197 / 184 / 72 ×3 / 282 % (D11 ÷ 1.3). NA DPS is about 2 % under D11 (the 59-tick string is
  rounded up). `char/navia/na_coef`, the def lore and registry `na1/na2`, and the README.
- **Swing hold (all characters):** a swing runs from the normal attack's start until the tick the next normal-attack
  input is accepted (`atkCD` ≥ 1 at the start of the tick = `#pmChainOpen` 0). For rig characters (3, 5, 6) only while the
  normal clip that opened it is the active clip (`active.normal:1b` written by the clip start; generated
  `char/motion/combat/swing_clip`). One shared state: `player/swing/tick`, called from `rlk:tick` before `view/tick`,
  re-derives `swHold` every tick (also 0 when dead, on the map, in the pick space or under the boss camera).
  - First person (`@s[tag=rlk_body]`): modifiers `rlk:swing_hold` −1 add_multiplied_total on movement_speed and
    jump_strength, re-added or removed every tick (no event can leave them stuck). Not in the shoulder view, where the real
    player is the riding camera (the modifier would only narrow the FOV).
  - Shoulder view and F5: `player/swing/tick` clears the avatar's horizontal velocity on the tick the hold starts;
    `view/move` gives no walking velocity and no jump while held, but still records the pressed direction for the dash
    (`#inAct/#inx/#inz`). Knockback (vanilla velocity and player/knockback teleports), gravity, stepT and dashes move the
    body as before. First-person dashes during a hold take the pressed keys (`player/swing/dash_dir`), since the body
    did not move.
  - Not swings: dash, sheathe, locomotion, skills and bursts (their own locks are unchanged). Dash still cancels a swing
    for every character (atkCD 0) except where it already could not (Skirk's skDash, pmMoveLock).
  - A skill or burst cast during a swing ends it for every character (verification fix): rig characters through the
    skill clip replacing the normal clip; the others through `player/swing/cut` (from `combat/on_skill` and Clorinde's
    Night Vigil lunge), which stores the remaining atkCD in `swCut` so `player/swing/tick` does not hold for the rest of
    that window. The next normal-attack input still waits for the window; a new attack (atkCD above swCut) holds again.
  - Released by: the window end, clip finish / stop / abort / another clip, character switch (`char/player_init` also
    sets atkCD 0 and calls `player/swing/release`), death, map, pick space, boss camera, losing the 'player' tag in
    rlk:tick's two-player branch (`player/swing/release` first, since swing/tick stops running), uninstall (modifiers and
    the `swCut`/`swHold`/`swJump` objectives).
  - Windows at atkSpeed 100 (game ticks): Lumine 6 / 10; Yoimiya 8 per arrow, 6 after an aimed release (fixed);
    Skirk 9 / 6 / 12 / 11 / 23 (infused 10 / 6 / 11 / 13 / 24); Clorinde 4 / 6 / 7 / 6 / 10, pistol 7 per shot (auto-fire
    keeps her standing while it fires); Arlecchino 6 / 7 / 8 / 10 / 8 / 14 (infused 6 / 6 / 7 / 11 / 8 / 14; the 6th hit's
    chain is 16 but the clip ends at 14); Navia 11 / 11 / 15 / 22; Ronova 10 / 10 / 10 / 16; Nefer 5 / 5 / 5 / 10, phantasm 20
    (fixed).
- **Gap rules:** moving keeps the combo for everyone (nothing touches comboStep; Navia's tail still ends on movement
  through `finish`/`sheath/abort`). A jump in the gap sets comboStep 0 (`player/swing/jump`; comboStep is the only string
  state every character reads): shoulder view from `view/move`'s jump, first person from the statistic
  `swJump` (`minecraft.custom:minecraft.jump`), consumed by `player/swing/tick` when not held and by `combat/on_attack`
  before a click (a jump that arrived first makes that click hit 1). A jump statistic during a hold (client latency) is
  discarded.
- Known first-person limits (vanilla): the speed modifier also narrows the FOV (about half at FOV effects 100 %, like the
  burst cast lock); air control does not use movement_speed, so an attack started mid-jump keeps some drift in first
  person; the client applies the modifiers one round trip late.
- Tests: `navia/test_speed_lock.py` (mcsim on the real functions), `ver/adv.py` (independent verification: interaction-poll
  clicks, exact-tick jumps, attack speed 50/200, interrupts incl. skills, NA4 flight, bow, catalyst, held W, view parity, fuzz). `mc1/retime/verify2.py` now reports the Genshin
  1.0× comparison as FAIL by design (the string is 1.3× faster).

## D13. Swing hold becomes a slow; no FOV zoom (binding, user 10-18)
- "못움직이게는 말고 속도가 느려지게 하자" + "화면 확대는 없이" + "이것도 모든 캐릭터 공통이야".
- During a normal-attack swing window, EVERY character walks at 50 % speed instead of stopping. Jumping stays blocked.
- In the gap after the window, walking is at full speed and a jump resets the combo to hit 1 (unchanged).
- No movement_speed attribute change in first person (it zooms the FOV). Use a FOV-neutral method, or fall back as described in the task.
- **Done (path: FALLBACK in first person).**
  - Shoulder view and F5 (the default view): `view/move` walks the avatar at `#swSlow` 50 % of the walking speed while
    `swHold` is 1 (2159 → 1079 per tick at moveSpeed 100), with no sprint bonus; bow draw and skDash factors still
    multiply. Turning (`#lk`, the avatar keeps facing the crosshair during the swing) and the dash direction
    (`#inAct/#inx/#inz`) run exactly as when walking; the jump is skipped while held; the sprint FOV effect is left as it
    is. `player/swing/tick` no longer clears the avatar's velocity at the hold start (the walk sets it every tick).
  - First person: `rlk:swing_hold` −1 on jump_strength only, re-derived every tick; movement_speed is never touched, so
    walking stays at full speed in the window (no FOV change). `player/swing/legacy` removes a movement_speed
    `rlk:swing_hold` left by a D12 save once per player (tag `rlk_sw13`; uninstall removes both modifiers and the tag).
    `player/swing/dash_dir` is gone: the first-person body walks during the swing, so the dash takes the walking
    direction again (pre-D12 rule).
  - Why not a FOV-neutral first-person slow (compared from vanilla client/server behaviour; not seen in game):
    - movement_speed (modifier or slowness): `getFieldOfViewModifier` ×(speed/walk + 1)/2 → 0.75 at half speed.
    - Invisible server-driven vehicle (scaled mob / display seat, the expected candidate): the vehicle is
      server-authoritative, so on every mount the client snaps to the server's copy of its position, which trails the
      client by about one tick (≈0.22 b walking, ≈0.28 b sprinting in single player, plus v×RTT on a server; limit was
      0.05 b), and the riding position sync carries the server's last yaw/pitch (the view jumps back while turning). One
      mount per swing makes this a hitch on every attack. While riding, input lags by a round trip, vanilla knockback is
      lost, every body teleport (player/knockback, dash_sub, mboss/pull, room teleports) dismounts, and
      `mount.onboard` shows on each mount. A display/interaction seat has the same mount snap plus command-side collision.
    - Block speed factor (soul sand/honey + movement_efficiency) and stuck blocks (cobweb, powder snow) need real blocks
      under the player; forcing a crouch with a collidable entity overhead (sneaking_speed 0.5) drops the eye 0.35 b;
      overriding the velocity or teleporting back half the step every tick stutters; item-use slowdown only exists while
      the player holds use (the server cannot start it).
  - Other locks (C): `rlk:motion_hold`, `rlk:burst_cast`, `rlk:navia_aim`, `rlk:frozen` keep movement_speed ×0 (full
    stop needed; a seat would add the same mount snap), so they still zoom in first person. Documented.
  - Release: unchanged per-tick derivation (window end, skill cut, death, map, pick screen, boss camera, character
    switch, the two-player release, uninstall); teleports (P4 pull, knockback) leave nothing to repair. No seat, no RP
    files.
  - Tests: `navia/test_speed_lock.py` and `ver/adv.py` (+ `ver/simbase.py`) now model the first-person client walk from
    the attributes (speed product, jump only with jump_strength > 0 raising swJump) and check: half speed in every
    swing tick and full speed in the gaps for all 8 characters in the shoulder view (single swing, whole strings with W
    held, sprint without bonus, Navia NA4 flight), full speed and no jump in first person, no movement_speed modifier
    ever (runtime invariant and no function adding it), the jump-only modifier exactly while swinging, gap jumps
    resetting to hit 1 in both views, Clorinde auto-fire (half speed / full speed, never jumps), the legacy cleanup,
    release on stop/death/map/pick/boss camera/switch/dash/tag loss/P4 pull teleport, uninstall. D12 copies kept as
    `*.d12.py`.
