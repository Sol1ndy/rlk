# S1K requests / notes (아를레키노 fx / sound / HUD kit) — for the lead at I1

Branch `wip/ar-s1k`. The kit implements every name of `api.KIT_PRESETS` / `KIT_PROPS` / `KIT_DECALS` / `KIT_SOUNDS` /
`KIT_HUD` / `KIT_FIXED` with exactly the contract args; nothing here blocks the merge. Items K1–K3 are decisions the lead
may want to confirm, K4–K6 executor conventions S4 should follow (the kit doc lines in `tools/mboss_kn_fx_manifest.json`
`presets.*.doc` say the same), K7 information.

## K1 (lead, PLAN §4.6 wording) — the Banquet banner is a text line under the boss bars, not the title subtitle
PLAN §4.6 says "above the crosshair (title-style subtitle line)". The footage puts the real game's banner directly under
the boss HP bar at the top of the screen (`ref/hud_bars_banner.jpg`, v6 30.0 full frame), and the subtitle line is where
the dialog lines run (F casts its line at pt 0, the window opens at 22: they would overwrite each other), while the action
bar holds the player's 「생명의 계약 N%」 (needed most during the Banquet). Built: `fx/hud/banner {on}` shows `api.BANNER`
as its own bossbar `rlk:kn_banner` (white / progress = no bar in this pack, as `rlk:mboss_sub`), coloured as the real
game (the first phrase 「생명의 계약을 제거하고 일반 공격」 salmon-red #F07858, the rest white); `on:0`, `fx/clear` (pause,
cancel) and `fx/hud/clear` hide it; `fx/uninstall` removes the bossbar. It appears below the three framework bars.
Affected: nobody (S3 already calls `banner {on}` at the window start / end / resume). Please amend PLAN §4.6 / contract §3.3.

## K2 (lead / S3) — slash arcs never reach below the floor (R-S3-4 "the kit keeps its arc above the floor")
`fx/p/slash_arc` measures the executor's height over the floor (storage `rlk:kn fx.fl`, the arena floor 201 by default)
and, from a pitch × roll table of the arc's lowest point (bearings ±80° of the aim), first **lifts** an arc that would
cut the floor by up to 1 b, then shrinks the rest. At S3's call heights: a4/a5 h4 overhead slam (r 36, pitch −50, roll 90
at 1.4 b) → lifted 0.76 b, reach 3.5; e1 spin slash (r 42, −60, 90) → lifted 0.47, reach 4.1; c1/c2 impact slash (r 40,
−40, 90) → lifted 1.0, reach 3.2; d2 rising slash (r 40, −30, 100) → lifted 1.0, reach 2.8; S2's intro flip (r 20, roll
90 at the blade anchor) → lifted to fit. Horizontal arcs (roll 0 / 10 / 180) keep their full reach. If the full reach of
the vertical slashes matters more than the pivot height, S3 can pass a higher pivot (h 2.0) for those four calls.

## K3 (lead, contract §3.3) — `dive_streak {len}` has no colour
Q0's opening fall is a crimson streak (PLAN §6), C / E dives are Pyro; the contract gives `dive_streak` no `c`. Built: an
orange-gold core inside a crimson outer streak (reads for both). If Q0 must be crimson only, add `c` to
`api.KIT_PRESETS['dive_streak']` and S1K splits it (one line).

## K4 (S4) — executor conventions of the P2 presets / props / decals
- `aim_line {len}`: at the chest anchor, `rotated` toward the player **with pitch** (the line follows the executor's
  pitch); each call lives 3 t: call it every tick (or every 2 t) while the aim tracks. `reticle`: at the chest anchor
  rotated toward the player (the reticle sits 0.6 b ahead, grows over 18 t, white-hot from 20 t = the lock, gone at 26).
  `beam {len}`: at the chest anchor rotated toward the locked point, pitch counts.
- `x_mark`: at her feet, rotated toward the player: two 4.6 b strokes crossing 1.6 b ahead, centre 2.3 b up (never below
  0.4 b), the second 12 t after the first, held 72 t (to the final at x + 70), white-hot from 64 t.
- `rapid_slash`: one call per slash at her body + 1.2 (two random horizontal-ish crimson arcs, 5.5 b, 3 t).
- `final_burst {r}`: at her feet. `feather_hit`, `orb_burst {r}`: at the landing / orb point **on the floor**.
  `orb_gather`: at her feet (the orbs fly in to 1.6 b around her at 1.5 b up). `moon_flare`: at the halo marker or her.
  `legs_burst`: at the spine anchor rotated as the body. `pillar {r}`: at her feet (6 b column).
- `dive_streak {len}` (Q0): at the body + 1, rotated as the body: the streak runs down-forward at 50° and is clamped to end
  above the floor.
- `ring_o {r,t}` / `donut_o {r0,r,t}`: positioned at the decal centre **on the floor** (y = the floor top; the kit adds
  0.02), `t` = ticks from the call to the hit (the flash is at t − 6).
- Props: `crescent` and `feather` are one face card facing the display's rotation (= its flight, pitch counts); the feather's
  tip points to the display's local −y (down when the display is level). `orb` always faces the viewer. Call the prop
  once per display (resume may call it again: idempotent).

## K5 (S2 / S3) — props on markers
A prop called on a non-display entity (S2's wisp markers `rlk_kn_wisp_<i>`, the T moon marker) gets **one follower
display** the kit keeps on it every tick (and removes when the marker is gone; re-calling replaces it); a prop called on
an `item_display` (S3's projectiles, S3's `core/wisps` displays) is dressed in place. `wisp_turn {c}` recolours either
(the display itself, or the follower of the marker it runs as). So both wisp conventions (S2 markers, S3 displays) work;
after I1 one convention is enough (R-S2-3). Followers carry `rlk_kn_fxf rlk_room rlk_mb_aux` (not `rlk_kn_fx`): `fx/clear`
(pause) keeps them; `fx/uninstall` kills them.

## K6 (S3) — `spin_ring` is drawn 0.3 b above its executor
S2 calls `spin_ring {r:25,c:1}` at her feet for the intro floor ring; a flat ring card at the floor would be a floor
marking, so the ring sits 0.3 b up. S3's calls at the body + 1.0 therefore show the ring at 1.3 b (S3's e1 aerial spin at
+1.6 → 1.9). If 1.0 b is wanted for S3's rings, pass + 0.7.

## K7 (information) — names, budgets, cost
- 362 functions under `boss/arlecchino/fx/`; objectives `knFx` (fake players), `knFxS knFxG knFxH knFxK knFxD` (card
  clock), `knFxL` (follower links); storage `rlk:kn fx.*`; bossbar `rlk:kn_banner`; tags `rlk_kn_fx` (+ `_c` fx, `_d`
  decals, `_fl` the flood), `rlk_kn_fxa` (animated props), `rlk_kn_fxf` / `rlk_kn_fxl` (followers / leaders),
  `rlk_kn_fx_demo`. Font `rlk:mboss_kn` U+EB00 (badge ◆), ending with a reference to minecraft:default.
- Pools: fx cards capped at 96 (ambient `gate_flames` / `ambient_petals` skipped from 64); decals never capped; the flood
  is one card a second call re-times.
- Atlas: 44 own sprites, 0.413 M px (budget 0.70 M); fg kit `glow` / `mote` / `spark` referenced (0 px).
- `fx/hud/badge {on}` appends `◆선혈의 충격` to `rlk:mboss sub[]` (root `{text:"",extra:[…]}`), removes an old one first
  (idempotent), and while on a 10 t chain re-appends it if a rewrite of `sub` dropped it.
- `fx/hud/line {id}`: Raiden's typed steps (2 syllables per step, 2 t apart, the full line 44 t + 12 t fade, a quiet
  note-block tick each) on the subtitle line with `ttlT` / `view/ttl_blank` (the framework's caption conventions); a new
  line replaces the running one; `fx/hud/clear` stops and blanks it.
- The gate icon item model `rlk:mboss/kn_kit/gate_icon` exists (the registry `icon.model` switch is the lead's at I1).
