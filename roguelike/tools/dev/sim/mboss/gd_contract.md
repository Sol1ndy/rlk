# Corrupted Guardian (파수꾼・타락) module: core <-> pattern contract

Worktree branch `wip/mboss`. `DP` = `roguelike/`, `F:` = `DP/data/rlk/function/`, `G:` = `F:mboss/guardian/`.
The framework contract (hooks, libraries, units) is `mboss/contract.md`; the rig API is
`DP/tools/mboss_guardian_rig_api.md`. This file is the contract between the Guardian **core** and the three
**pattern modules**, so pattern authors can work in parallel. Binding design: `mboss/plan.md`, `understand/patterns.md`.

---------------------------------------------------------------------------------------------------

## 1. Files, ownership, build

| file | owner | content |
|---|---|---|
| `tools/build_mboss_guardian.py` | core | entry script (`python3 tools/build_mboss_guardian.py`) |
| `tools/mboss_guardian/__init__.py` | core | package doc, `PATTERN_MODULES = ('p12', 'p34', 'p56')` |
| `tools/mboss_guardian/api.py` | core (stable) | `Pattern`, `Gen` writer helpers, `DMG`, `KB`, bands, colours, the rig clip table read from `tools/mboss_guardian_rig_manifest.json` (`ev(clip, event)`, `clip_len(clip)`) |
| `tools/mboss_guardian/core.py` | core | 17 hooks, AI + rotation, guard, chaos, stars, groggy, entrance, death, HUD, voice, tests, generated dispatchers |
| `tools/mboss_guardian/p12.py` | P1/P2 author | `thrust` (1), `javelin` (2) |
| `tools/mboss_guardian/p34.py` | P3/P4 author | `slam` (3), `pull` (4) |
| `tools/mboss_guardian/p56.py` | P5/P6 author | `flyslam` (5), `sweep_g` (11), `sweep_e` (12), `fail` (13) |

- The generator owns `G:**` **except** `G:rig/**` (`tools/build_mboss_guardian_rig.mjs`). Stale files are deleted on every
  run. Never hand-edit generated files.
- A pattern module writes **only** `G:p/<key>/**`, through `gen.pw(key, name, lines)`. It never edits `api.py`,
  `core.py`, the registry or another module.
- Build order: `python3 tools/build_mboss_core.py` (after registry edits) → `python3 tools/build_mboss_guardian.py`
  → `python3 tools/check_mboss_pack.py`. The rig generator is independent (`node tools/build_mboss_guardian_rig.mjs
  --resourcepack <RP>`) but runs first when the RP side changes: it also writes the chaos star crystal models
  (`rlk:mboss/guardian/star_<1-6|flash|dark>`) and the P4 screen font `rlk:mboss_gd` (`tools/guardian_screen.mjs`),
  and puts the screen frame texts into the manifest (`screen`, read as `api.SCREEN` by p34.py).
- Wind-up tuning (plan.md "공격 선딜 좀 짧게"): the clips are authored on the reference-video timeline and played
  through `RETIME` (`guardian_clips.mjs`, piecewise-linear knots [authored tick, played tick]; strikes and spins on 1:1
  segments). The manifest carries the knots (`retime`, `authoredLen`); `api.rt(clip, t)` maps an authored tick to the
  played one, `api.inv(clip, t)` back (for resampling authored per-tick tables). `ev()` / `clip_len()` are played
  ticks. After a clip change re-measure `p12_spear.json` / `p56_spear.json` (README "창 위치표").
- `core.build()` asserts: unique ids/keys, ids 1-5 and 11-13 present, and every declared pattern wrote
  `start`, `tick`, `cancel`.

## 2. A pattern module

```python
from .api import Pattern, ev, clip_len, DMG, KB, CY
PATTERNS = [Pattern(1, 'thrust', '공간 찌르기', bands=('melee', 'mid'), weight={'melee': 2}, recover=18, max_len=83),
            Pattern(4, 'pull', '어둠 속에서 퍼지는 공간', bands=('melee', 'mid', 'far'), weight={'melee': 1, 'far': 3},
                    away=(5.0, 6.5), max_len=86)]
def emit(g):                       # g = api.Gen
    g.pw('thrust', 'start', [...])
    g.pw('thrust', 'tick', [...])
    g.pw('thrust', 'cancel', [...])
    # optional: 'vis' (hz_vis events), 'pj_end' (projectile events), 'pause' (fight frozen), any helper names you call yourself
```

`Pattern(id, key, label, kind='normal'|'service', bands=(...), close=None|blocks, recover=ticks, max_len=ticks,
length=None|ticks, min_d=None|blocks, weight=None|{band: n}, away=None|(near, to))`:
- `id`: 1-5 normal patterns (P1-P5), 11-19 service patterns (started by the core only). Stable numbers.
- `label`: Korean, shown on the boss-bar sub-line while a normal pattern runs (`패턴  <label>`).
- `bands`: where the shuffle bag may pick it (§5). `close`: the core closes in to this distance before `start`.
- `recover`: idle ticks after it ends. `max_len`: safety end (the core finishes it at this clock even without `p/end`).
- `length`: its real end (`#gdPT` of its `p/end`, default `max_len − 4`) for the boss-bar progress (`#gdPLen`; the bar
  empties on that tick). A pattern that decides a shorter run calls `g.set_len(t)` (P4 refused pull → 32, one fail
  spear → 68).
- `min_d`: the bag picks it only from this distance on inside its bands (no pattern uses it since the tuning; P4 had
  5 b). `weight`: draw weight per band (default 1; melee P1 / P3 2 and P4 1, far P4 and P5 3, so far away they come
  before P2). The weights order the draws inside one bag cycle: every candidate of a band is still drawn once per cycle.
- `away`: (near, to): picked with the player nearer than `near`, the core first hops back to `to` b from the player
  (`ai/back`, state 8, 12 t, rig clip `backstep`) and calls `start` after it (P4: (5, 6.5)). Excludes `close`.

## 3. Entry points and the pattern clock

| function | called | executor / position | rule |
|---|---|---|---|
| `G:p/<key>/start` | once, on the tick the pattern begins | `@s` = body, at the body (rotation = body yaw) | play the first clip here (`g.play(clip)`): the rig ticks **after** the AI, so the clip's tick 0 renders this game tick |
| `G:p/<key>/tick` | every following fight tick | `@s` = body, at the body | `#gdPT mb` = 1, 2, … = **the clip tick** of the clip played in `start` (verified by the mcsim timing test) |
| `G:p/<key>/cancel` | when the core aborts it (§4) | the caller (normally the body) — **use selectors, not `@s`** | remove everything you own, reset your fake players; idempotent |
| `G:p/<key>/vis` | optional, `hz_vis` of your hazards | `@s` = hazard marker | `#hzEv mb` 0 create / 1 strike / 2 end; your visual id `@s mbHzV` = **pattern id × 10 + k** (k 1-9) |
| `G:p/<key>/pj_end` | optional, `pj_end` of your props | `@s` = prop | set `scoreboard players set @s mbId <pattern id>` on the prop before `pj/launch`; `#pjEv`, `#pjKeep` per the framework |
| `G:p/<key>/pause` | optional, once when the fight freezes (player dead / reviving; `G:pause` → `G:p/pause_d`) while your pattern runs (not on its pick tick) | `@s` = body | drop what would hang in the world until the resume (P4: the screen layers); the clock simply continues after the resume |

- Timeline helpers (`api.Gen`): `g.at(t, cmd)`, `g.at((t0, t1), cmd)` (on `#gdPT`), `g.at_body(t, sub)`,
  `g.every(n, cmd)` (moduli `#gdK2 #gdK3 #gdK4 #gdK5 #gdK6 #gdK8 #gdK20`), `g.fn(rel)`, `g.rig(call)`, `g.play(clip)`,
  `g.end()`, `g.voice_attack()`, `g.sound(...)`, `g.dust(...)`, `g.dust_fade(...)`, `g.particle(...)`, `g.card(...)`,
  `g.say(...)`, `g.hz_opts/hz_disc/hz_ring/hz_sector/hz_line/hz_full` (blocks; `mboss_lib`). Retiming: `rt(clip, t)`
  (authored → played tick), `inv(clip, t)` (played → authored time) from `api`.
- A clip played later (e.g. `swing` after `pull`) starts on that tick: its tick c = `#gdPT − <play tick>`.
- Moving the body: `mv/*` as the body, or `tp @s`. Never move it while the clip plants the spear (rig API §4).

## 4. How a pattern ends, cancel rules

- **End:** call `function rlk:mboss/guardian/p/end` (`g.end()`), normally at `#gdPT = clip length`. The core finishes the
  slot after that tick's pattern tick (`p/finish`): clears `#gdPat/#gdPT`, removes `rlk_mb_inv` from the body, resets
  `#mbNoLeash` (except during chaos) and hands over to the owning state: idle + `recover` (normal), `guard/after`
  (sweeps), the chaos fail sequence (fail spears).
- `max_len` is a safety net only; a pattern that relies on it is a bug.
- **Release** (`g.release()` = `G:p/release`, `#gdPRel 1`): the dangerous part is over; the owning state may move on
  now while the pattern finishes a harmless tail in the slot (the slot stays busy: no new decision, no pattern bar,
  `p/finish` then skips the owner hand-over). Used by the fail spears: she leaves 10 t after the last impact while the
  planted spear still dissolves (m4 +90).
- **Cancel** (`G:p/cancel` → your `cancel`) happens on: tests (`test/pattern`), boss death (`death_start`), `/reload`,
  and the chaos fail safety end. Before it the caller runs `rlk:mboss/lib_clear` where hazards must go (tests; death
  already did), which kills `rlk_mb_hz`, `rlk_mb_hzfx`, `rlk_mb_pj` props, pull points and stops `mv`. Your cancel must
  remove the rest (markers, displays, props released from `pj`) by tag. The core then resets the slot, `rlk_mb_inv`
  (fight state only) and the leash, and restores the rig spear look.
- Do not deal true damage, never call `combat/apply`, never change `#gdSt` or other core state.
- If you tag the body `rlk_mb_inv` (e.g. P5 while she is in the sky) remove it yourself; the core also removes it at
  finish/cancel.

## 5. State, scores, range info

All fake players live in objective `mb`. Core names start with `#gd`; **pattern modules use `#gp<id><name>`**
(e.g. `#gp4Ok`, `#gp13K`). Scratch you may clobber inside one function: `#gdM` (modulo helper), `#t`… framework scratch.

| score | meaning | pattern access |
|---|---|---|
| `#gdPT` | pattern clock (clip tick) | read |
| `#gdPat` | running slot pattern id | read |
| `#gdSt` | AI state: 0 idle 1 normal pattern 2 close-in 3 guard 4 chaos 5 groggy 6 approach 7 dying 8 hop back | read |
| `#gdBand` / `#gdDist` | band at the pick (1 melee ≤ 4 b, 2 mid, 3 far ≥ 8 b) / distance in tenths | read (fresh: `function rlk:mboss/mv/dist` as the body → `#mbDist`) |
| `#gdSwEl` | element of the enchanted sweep (1 pyro 2 hydro 3 electro 4 cryo) | read (12) |
| `#gdFailN`, `#gdFailK1`, `#gdFailK2` | surviving stars at T0 and their kinds (1-4 element, 5 inert gold, 6 inert blue), slot order | read (13) |
| `#gdSlotA`, `#gdSlotB` | record slots of this cycle (0 empty, 1-4) | read |
| `#gdGN`, `#gdGP` | guard number (1/2), guard phase (1 entry, 2 window, 3 sweep, 4 gap) | read |
| `#gdCP`, `#gdTim`, `#gdF` | chaos phase (1 travel 2 charge 3 hold 4 fail), timer, fail clock | read |
| `#mbLock` | framework test lock (1-5 = that pattern only, 6 = guard pair + chaos only) | read |
| `#mbNoLeash` | 1 during scripted flights; set it yourself during your flight (P5), the core resets it | write |

Range bands (K2) and close-in: P1 melee/mid, P2 mid/far, P3 melee (close to 3 b first), P4 every band, P5 far. The
bands (melee ≤ 4 b, far ≥ 8 b) and P3's close-in stay through the area tuning: P3 starts within 3 b, inside its r 6
disc 3.5 b ahead, and she drifts to within 8-9 b between patterns, where P5 must still be a far pick.
The bag is weighted per band (melee: P1 2, P3 2, P4 1; mid 1 each; far: P4 3, P5 3, P2 1). Pull guarantee (`ai/pick`):
on the last pick of a stretch of normals (`#gdLeft 0`) with no P4 yet in it (`#gdP4N 0`, reset at `guard/begin1`) the
pick is P4 (`ai/pity`) at any distance (plan.md "P4 for melee players": before, the guarantee needed > 4 b and a player
who stayed in melee saw P4 in 0 of 127 stretches). P4 picked with the player nearer than 5 b hops back first
(`ai/back`, 12 t: the spot 6.5 b from the player on the line through her, turned round the player by ±40, ±80, ±120,
180 deg until it passes `mv/ok`, i.e. sideways along the wall and then toward the centre; push-off dust, glide 11 t,
landing puff, then `ai/go`). The core picks, closes in (glide 0.3 b/t, ≤ 30 t) or hops back and only then calls
`start`, so `start` can assume the band (P4: the player ≥ about 5 b away unless the player follows her).

## 6. Damage and hazards

- Coefficients (`api.DMG`, % of the registry base hit; K17): entrance 100, P1 100 / 115, P2 130, P3 160, P4 120 ×2,
  P5 180, gold sweep 165, enchanted sweep 250 (+ the element), fail spear 220. Knockback (`api.KB`, K16): P1 hit 2 and
  the enchanted sweep 4, default 3, light 2.
- Registry balance (`tools/mboss_registry.json`, enabled): `hp 250`, `atk 12`, `dmgMul 110`, `intro 90`, `death 90`,
  `deathSnd false`. `mboss/hurt` passes `#cmDmg = atk × pct × dmgMul / 10000` straight to `cm/hit_pl2`; there is **no**
  boss multiplier (Raiden's ×1.6 lives only in `boss/raiden/hurt`). Raw hits: 1.0 = 13, P1b 1.15 = 15, P2 1.3 = 17,
  P3 1.6 = 21, P4 1.2 = 15, P5 1.8 = 23, gold sweep 1.65 = 21, fail spear 2.2 = 29, enchanted sweep 2.5 = 33. After the
  level factor and defence, for an item-less player at the zone level: 1.0 ≈ 11 % of max HP (ch1 Lv4 15 of 136, ch2 24,
  ch3 32, ch4 42) and the enchanted sweep ≈ 29-30 % (40 / 62 / 84 / 107); two levels behind ≈ 38 %. No one-shot, no
  same-tick double hit (hazards ≥ 13 t apart). A 1.0 hit is a chapter-1 fire-mage bolt (8-22 raw) and about 1/2.6 of
  Raiden's heaviest hit after his ×1.6. HP: at chapter 1, map 3 (level 4) 250 → ≈ 1 900 (the ×4 mob HP multiplier),
  ≈ 63 % of Raiden's 3 010 at level 7; the two star breaks (24 %) and the groggy window bring the effective fight to
  about half of Raiden's.
- Sounds: `g.sound` → `mboss_lib.sound`, minVolume per layer (vol / 3, ≤ 0.4; 0 for layers ≤ 0.25).
- Hazards: set one-shot options, then call the shape positioned on the floor point (`positioned ~ {CY} ~`) rotated =
  aim: `scoreboard players set #hzSfx mb 3` … `execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0
  positioned ~ 201 ~ run function rlk:mboss/hz/line {len:55,w:22,tell:12,dmg:100}` (Python: `g.hz_line(5.5, 2.2, 12,
  DMG['p1a'])`). Element: `#hzEl` (−1 = boss Geo), colour `#hzCol`. The aim is locked at creation.
- **Telegraph floor (K4, tuned):** every damaging hit ≥ 10 t (`tell`; was 12 t), the undodgeable pull ≥ 20 t of tell; the
  wind-ups are ~25 % shorter than the source and the hit areas ~20 % larger (plan.md). The hit resolves at `tell`, so
  create the hazard `tell` ticks before the clip's hit event (P1 hit 1: create at 11, tell 10, hit at clip 21).
- **Telegraph rule (10-20)** (plan.md; audit `tele/gd/audit.md`): a ground telegraph only where the footage shows one.
  Every Guardian hazard is created quiet (`#hzQuiet 1` / `hz_opts(quiet=1)`: no framework outline, progress outline or
  strike flash). Ground telegraphs kept, trimmed to the footage: **P3** (`#hzVis 31`: the thin gold ring card, 40 % →
  rim in 5 t, + the faint amber fill), **P5** (28 rim bars, glow fill, star emblem; no progress circle), **fail spears**
  (the red star decal; no damage ring; a flat r 3.4 ring of the star colour at the hit, `p/fail/ring<kind>`, is the
  impact visual). Read from motion and sound, no ground telegraph: entrance, P1 ×2, P2, P4 ×2, gold / enchanted sweep;
  for these the K4 floor counts from a distinguishable clip pose + sound to the hit (10 t, 12 t for P1 thrust 2 and the
  entrance), and each has an impact visual of its own. `test_guardian.py` §10 checks the set of hazards that draw a
  ground telegraph = {P3, P5, fail}.
- Areas anchored on the player stay inside the walkable arena (r 21): the P5 ring centre is pulled to within 15.5 b of
  the axis, a fail disc to within 17.6 b (both still cover a player standing at the wall).
- Direct swings (no hazard): `function rlk:mboss/hurt` as the attacker with `#mbHitPct`, `#cmEl tmp`, `#mbKB`,
  `#mbKBDir`; one hit per swing is yours to enforce. Pull: `rlk:mboss/pull/start {t:N}` positioned at the destination.
- Projectiles: summon your prop (e.g. `g.rig('prop/spear')`, tagged `rlk_mb_gd_prop_new` for that call), give it
  `mbId <pattern id>`, then `pj/launch`; visual-only props use `dmg:0` (K23: the javelin damage is the line).

## 7. FX, sound, tags

- Every entity you create: `rlk_room`, `rlk_mb_aux` and **`rlk_mb_gd_p<id>`** (cancel kills by it). Hazard decals
  shown through `vis` also carry `rlk_mb_hzfx`. Reserved core tags: `rlk_mb_gd_fx`, `rlk_mb_gd_star`, `rlk_mb_gd_starv`
  (the star crystal item_displays), `rlk_mb_gd_sigil`, `rlk_mb_gd_cs`, `rlk_mb_gd_cs<s>`, `rlk_mb_gd_cs<s>_<k>`,
  `rlk_mb_gd_csh`, `rlk_mb_gd_csend` (cube stream chains) (the core kills `rlk_mb_gd_fx` at every chaos reset — do not
  use it).
- Screen effects: never world-space quads at the eyes (the F5 seat view's camera is 3.5-6 b behind the seat). Use a
  title with the screen font (`api.SCREEN['frames'][name]`, set `vBig` on the player so the F5 crosshair title rests,
  `p/pull/scr_end` to end it) or a status effect.
- Gold Geo cards: `g.card(kind, pos, ...)` = Navia's `rlk:fx/nv/card` (rose, star, burst, crescent, petal, shard, ring,
  glow; size = card width in blocks; cap 48 live cards shared with Navia). Element colours: `api.EL_HEX/EL_RGB`,
  star kinds `api.STAR_HEX/STAR_RGB`, gold `api.GOLD*`, crimson `api.CRIMSON*`.
- Particles: `force @a[tag=player]` (helpers do it). Sounds: **vanilla only**, `g.sound(event, vol, pitch)` → `hostile`
  source; compositions per patterns.md audio tables.
- Rig looks: the core sets/restores the spear for the enchanted sweep and guard mode (`spear/gold`), the eye for
  guard/chaos and the body glow (`glow/gold` in the guard window, `glow/off`). Patterns may call `rig/spear/<el>` or
  `rig/eye/<el>` only if they restore them in `tick`/`cancel`.
- Voice: `g.voice_attack()` ("처결하노라!" / "사라져라 마땅한 존재여!", shared 20 s cooldown). Used by P2 (release), P4
  (cast), P5 (take-off), fail spear 1. Other lines belong to the core.

## 8. Rig clips (id, length, then, events = clip ticks)

Played ticks (after `RETIME`, §1); the authored length is in brackets for the retimed clips.

| clip | id | len | then | events |
|---|---|---|---|---|
| `idle` | 0 | 40 | loop |  |
| `glide` | 1 | 24 | loop |  |
| `thrust` | 2 | 79 (91) | idle | glow 3, glint 14, **hit1 21**, rise 31, dive 42, **hit2 46**, land 53, flourish 60 |
| `javelin` | 3 | 67 (76) | idle | spin 0, vanish 9, glyph 10, beam 20, rematerialise 22, **release 26**, **launch 27**, return 49, catch 54 |
| `slam` | 4 | 64 (70) | idle | raise 0, ring 7, glint 9, down 16, **impact 20**, pull 42, twirl 48 |
| `pull` | 5 | 32 (40) | idle | aura 0, cage 7, **relocate 24** |
| `swing` | 6 | 46 (51) | idle | windup 0, **swing1 15**-19, **swing2 28**-34 |
| `flyslam` | 7 | 91 (101) | idle | raise 0, glint 5, beam 12, takeoff 14, ring 16, gone 18, dive 29, **impact 31**, spikes 37, pull 61, twirl 69 |
| `guard_entry` | 8 | 50 | guard | twirl 0, discs 16, ring 35, settle 44, guard 50 |
| `guard` | 9 | 40 | loop |  |
| `sweep` | 10 | 39 (44) | idle | windup 0, **active 14**-19 (blade slices 15-19) |
| `sweep_e` | 11 | 45 (50) | idle | enchant 0, windup 5, **active 14**-22 (blade slices 16-22) |
| `chaos_leap` | 12 | 32 | chaos_charge | leap 0, land 32 |
| `chaos_charge` | 13 | 36 | chaos_hover | charge 0, flare 7, rise 30, hover 36 |
| `chaos_hover` | 14 | 40 | loop |  |
| `chaos_fail` | 15 | 30 (40) | hold | twist 8, rise 16, high 19 |
| `chaos_land` | 16 | 26 | hold | land 22 |
| `chaos_fall` | 17 | 20 | groggy_a | hang 0, fall 6, land 18 |
| `groggy_a` | 18 | 40 | loop |  |
| `groggy_b` | 19 | 34 | getup | fold 0, getup 34 |
| `getup` | 20 | 40 | idle | spread 0, lift 6, stance 12 |
| `entrance` | 21 | 60 | idle | fall 0, **impact 14**, appear 14, grab 26, pull 34 |
| `death` | 22 | 80 | hold | slump 0, takeoff 22, gone 76 |
| `pose_ref` | 23 | 20 | loop |  |
| `chaos_raise` | 24 | 24 | idle | raise 0, overhead 6 |
| `backstep` | 25 | 12 | idle | push 2, peak 6, land 10 (the hop back before a P4 from melee range; the core glides the body) |

Body travel (rig API §4): horizontal travel is the pattern's job (move the body); heights/limbs/spear are in the clip.
Keep the body still while the spear is planted: `slam` 20-42, `flyslam` 31-61, `entrance` 14-26. P1: lunge 3 b at
19-21, fly back during 31-33 (rise), to the dive spot 34-42, dash 6 b at 44-46. P5: glide under the locked ring during
18-29. Javelin: the rig spear is hidden 9-22 and 27-54; the flying spear is `rig/prop/spear` (scale 2.2, grip at the
origin, tip +Y → rotate `left_rotation:[0.7071f,0f,0f,0.7071f]` to point it forward; tint copies
`rlk:mboss/guardian/prop_spear_<red|gold|pyro|hydro|electro|cryo>`; at scale 5.5 the tip is 8.1 b from the grip).

## 9. What the core does (for orientation)

- **Entrance** (intro clock): 16 sky glint + the plant hazard r 3.6 (quiet: no ground marker, rule 10-20), 20 `entrance`
  clip (rig hidden until then; the spear falls from 7 b with a gold trail), 34 plant hit (100 %, tell 18; was 26 / 40 /
  24 t) + "통찰하여, 나의 마음을 보아라.", 60 fight.
- **Rotation (K3):** 3-4 normals (range-filtered shuffle bag, no immediate repeat, close-in for P3, hop back for a P4 in
  melee range, one P4 per stretch guaranteed at any distance) → guard I → guard II → chaos → groggy or fail → 4-5
  normals → … No HP phases.
- **Guard (K5, K6, K22, K24):** `guard_entry` 50 t (twirl, discs 16-35, ground ring 35, no damage), "기록하여 판결할 지어다."
  (once per pair), gold eye (slot A's element in guard II when remembered); window 100 t: gold aura (rig `spear/gold` +
  `glow/gold` outline on the whole body, 3 gold dust a tick, motes and a spear spark every 2 t), drift ~1 b/s, record
  counting (on_hit: `#elem` 1-4, `#tfm` excluded, one count per element per 8 t, 3 new / 9 for slot A's element in guard
  II). Record → slot, `rig/spear/<el>`, pattern 12 at once (blade slices 16-22, front at 18; r 6). Timeout → pattern 11
  (blade slices 15-19, front at 17; r 6).
  Then 20 t → guard II (`GUARD_GAP[1]`, 43 t after the strike as in m2); guard II → chaos at once when the sweep clip
  ends (`GUARD_GAP[2] = 0`: the clip's own 20-23 t tail after the last slice = m2's 20 t). The glow ends at the record
  (element spear) or when the gold sweep ends.
- **Chaos (K7-K12):** leap (≥ 6 b from the centre) or glide to the centre, landing, `chaos_charge` (30 t charge + rise),
  hover → 350 t timer, stars from slots A/B (her right / left, 4.2 b out at ±24°: 3.4 b apart, under and in front of
  her), cross sigil, crimson rim haze, ambient cube streams (no damage; up to 3 snake chains of 8-12 cubes: a 0.62 b
  gold lead + black-glass followers with a red #FC5454 glow outline, 0.52 → 0.3 b, each taking its predecessor's
  place of the previous tick; at the floor the lead vanishes and the followers pop into it one per tick). Stars: aux
  husks, pool 4.2 % (active) / 1.7 % with RES 80 (inert) of the body's max HP; visual = upright 4-point crystal
  item_display (`star_<kind>`, 1.15 b at 8 t → 2.1 b at the timeout, turning 3°/t). Active stars carry their element
  permanently and take it with **40 % RES** (`star/resist`: ×0.6, at least 1; other elements and physical in full;
  user decision, replaces C11's immunity); a hit that is 0 after that is swallowed (`star/ignore`), so the framework
  zero-damage popup never shows; hits outside the running timer do nothing. Sizing (`STAR_PM`, `KILL_S` 75 s, asserted
  at build): own-element active 75 × 4.2 % / 0.6 ≈ 5.3 s + inert 75 × 1.7 % / 0.238 ≈ 5.4 s ≈ 10.6 s for both (also
  10.5 / 10.7 s for two active / two inert), other-element active ≈ 3.2 s.
  Break → S+5 true damage 6 % (1st) / 18 % (2nd); the 2nd → `chaos_fall` + groggy 220 t (pose B at 136, get-up 170,
  "나의 주인님이시여...!"). Timeout → `chaos_fail`, star flash (+5) / collapse / absorb (+11), pattern 13 (spears; the m4
  fail schedule x0.75: impacts +37 / +60), `chaos_land` at +25 (`FAIL_LAND`, lands at +47 between the spears),
  `chaos_raise` at +54 (2 spears; derived from p56 `FAIL_HIT + FAIL_GAP - 6`); 10 t after the last impact (`FAIL_REL`,
  +47 / +70) the fail pattern releases the slot (`g.release()`), she leaves the centre (approach glide) while the
  planted spear still dissolves, the pattern tail ends at the last impact + 31; then the next normals. Slots reset after
  each chaos.
- **Death (K20):** "시련은... 끝났다...", `death` clip (slump, fly-away), cube trail, rig killed at 80, body at 90. No
  creature vocals: amethyst-cluster + beacon-deactivate stings, flap + riptide at the take-off; the registry's
  `deathSnd false` silences the framework's wither roar. Entrance: the plant's hazard has `#hzSfx 0` (the module's own
  impact sounds only).
- **HUD:** name line `Lv.N 파수꾼・타락` + slots `기록 ◇◆` + state; under-bar = pattern progress (gold), guard = leading
  element's record progress (its colour; gold = window time before the first count), chaos timer (Pyro code 2),
  groggy time (green); sub-line = pattern name / per-element counts `불 1/3 …` / stars + seconds left (+ "기록 원소 별:
  같은 원소 40% 내성" while an active star stands). The pattern bar counts down against `#gdPLen` (the real end).
- **Reload:** every mover stops (`mv/stop` on `rlk_mb_mv`: P5's glide under the ring, chaos travel), glow off.

## 10. Test commands

- Fight: `/function rlk:mboss/test/start {id:"guardian"}` (chapter 1) or `test/start_ch {id:"guardian",ch:3}`; then
  `test/kill`, `test/abort`, `test/level {lv:N}`, `test/stop`.
- `/function rlk:mboss/test/pattern {id:N}` (Guardian ids): 1-5 next normal pattern (cuts the running one; P3 closes in);
  11 gold sweep, 12 enchanted sweep (electro), 13 fail spears (2 inert stars) — run at once; 20 guard I, 21 guard II with
  slot A = electro (9 to re-record); 30 chaos with the current slots, 31 electro ×2, 32 inert ×2, 33 pyro + cryo;
  40 groggy; 41 break one star; 42 chaos timer to 1 s; 91-94 a counted pyro/hydro/electro/cryo hit for the record
  (8 t limit applies); 99 back to idle. Any other id prints the help.
- `/function rlk:mboss/test/lock {id:N}`: 1-5 = only that pattern (no guard cycle), 6 = guard pair + chaos only, 0 = off.
- Offline: `python3 scratchpad/mb/test_guardian.py <worktree>/roguelike` (mcsim; rig stubbed): entrance timing,
  rotation over 5200 t, record rules, stars, breaks, groggy, fail, lethal break → reward, pause, reload, lock, and the
  player-hit tick + coefficient of every damaging pattern against its clip events. Extend it when a pattern changes
  its hit ticks (section 8 of the test).
  Pattern suites: `test_p12.py`, `test_p34.py`, `test_p56.py`. Whole fight: `test_e2e_guardian.py` (gate → arena →
  entrance → normals → guard I records Pyro → guard II times out → chaos with an active pyro + an inert blue star →
  both broken → groggy → resume → kill → won → 2 picks; the fail variant leaves the pyro star to its fail spear; plus
  a pause in P4's screen overlay and the uninstall hook). Review-fix checks: stars 3.4 b apart, 40 % own-element RES
  (no popup), P4 in every stretch of normals at 3 b (melee), 6 b and 10 b (and it pulls), the hop back (12 t, 6.5 b,
  sideways along the wall), a melee-range P4 always hops first, guard aura / glow, guard II → chaos
  ≈ 20 t, fail departure at +71 with the tail to +91, reload mid-glide, the progress bar against the real end, death
  without vocals, minVolume per layer; in `test_p34.py` the title frames per tick, the fallback swings, and the pull
  in the real arena block geometry (`build_mboss_arena.layout()` + light layer + barrier cap through mcsim's
  `block_test`) at 10 / 33 b, against the wall, jumping and from a raised body, the hop back from 3 b followed by the
  pull and both swings, and a player sprinting out of the r 6.8 swings right after the pull. Tuning copies of the
  suites (new numbers) and the P4 frequency tool live in `scratchpad/mb/tune_tests/`.

## 11. Pattern checklist (from patterns.md §2-§9 and §15; all done, merged on wip/mboss; the bracket notes were the stub status)

Ticks and sizes in the items are the source (authored) ones; the last item of each block is the played version after
the user tuning (wind-ups ~25 % shorter, areas ~20 % larger, plan.md).

**P1 공간 찌르기** (`p12.py`, clip `thrust`, mid 3-5 m) — [stub: clips, 2 line hazards 12/16 t, lunge/fly-back/dash]
- [x] wind-up 0-4, gold charge streak along the shaft 4-16 (`#FCF5AE/#CDB37E/#9D8650`), glint flare 19, lens streak 20-21
- [x] hit 1 at 28: sphere r ≈1.5 at the tip after a 2-3 b lunge; gold burst ≈3 b + shock-ring arc ≈3.5 b, gold/dark cubes
- [x] rise and reposition 38-54 (4-6 b back, 2-3 b up in the rig), dive 54-57, dash 5-6 b in 2-3 t, hit 2 at 58 (path ≈1 b
      wide + sphere r 1.5), knockdown → KB 4; trail; land 65; flourish 72-84
- [x] K4: line decal ≥ 12 t before each hit; damage 1.0 / 1.15
- [x] sounds: charge `block.beacon.power_select` (p 1.6-2.0) + `amethyst_block.chime`; hits `item.trident.hit` (0.8) +
      `amethyst_cluster.break` + `generic.explode` (1.6, 0.4); dive `player.attack.sweep` (0.7)
- [x] tuning (played): lock 11 → hit 1 at 21 (lane 9.3 × 2.9 b, tell 10, lunge 3 b, tip sphere r 1.8), rise 31, lock 34
      → hit 2 at 46 (lane 8.4 × 2.7 b, tell 12, dive spot 6.6 b from the target, dash 6 b), hit fx x1.2, 79 t
- [x] rule 10-20: no lane decals (hz_vis 11 / 12 and their amber bars removed; quiet lanes); the tell is the streak and
      glint on the spear (tracking stops at 11) and the rise + glide to the dive spot

**P2 공간 투창** (`p12.py`, clip `javelin`, mid/far) — [stub: line 1 b to the edge locked at 24, tell 12, prop out/back]
- [x] spin 0-6 + gold trail, vanish 8-10, glyph (gold concave 4-point star ≈1 b, rotating/shrinking) 11-27 → spinning ring
- [x] vertical white-gold beam at 28 (last telegraph), re-flash, draw-back + rematerialise 29-33
- [x] release explosion ≈2 b at 35, launch disc 35-37, line at chest height ≥ 15 b in 1-2 frames, trail 39-43
- [x] K23: line locked at the beam, 1 b wide, to the edge, 2 t; visual spear 5 b/t; return harmless 56-61, catch 63
- [x] sounds: spin `player.attack.sweep` + `trident.riptide_1`; glyph `amethyst_block.resonate`; burst `beacon.activate`
      (1.8); release `trident.throw` (0.7) + `firework_rocket.blast` (1.2) + `trident.riptide_2`; return `trident.return`
- [x] tuning (played): spin 4-8, vanish 9, lock 17, beam 20, release 26, launch 27 (tell 10), lane 1.2 b wide, return 49,
      catch 54, 67 t
- [x] rule 10-20: no lane decal (hz_vis 21 removed; quiet lane); the air glyph 10-19 and the beam at 20 are the tell

**P3 공간을 집행하는 시련** (`p34.py`, clip `slam`, melee, close to ≤ 3 b) — [stub: disc r 5 at 3.5 b, ring lead 17 t]
- [x] raise 0-7, gold ellipse ring + amber fill at 9 centred 3.5 b in front (K25), glint 12-21, downswing 22-25
- [x] impact 26: vertical gold pillar (≈0.6 b × ≥ 2 BH), white flash, radial crystal blades, gold cubes, rock chunks
- [x] spear planted 26-48 (body still), sparkles at the tip; pull-out 48-54; twirl 54-70
- [x] sounds: charge `beacon.power_select` + `respawn_anchor.charge` (1.5); impact `generic.explode` (0.9) +
      `amethyst_cluster.break` + `trident.thunder` (0.3); pull-out `chain.break` (0.6) + `stone.break`
- [x] tuning (played): ring 7 → impact 20 (tell 13), disc r 6 at 3.5 b (decal, fill, flash and shock ring to match),
      planted 20-42, 64 t
- [x] rule 10-20 (trim): the ring card (vis 31) + amber fill stay, the ring now appears at 40 % and reaches the rim in
      5 t (m1 11.42-11.70 s); the hazard is quiet (no framework outline / progress outline / strike flash)

**P4 어둠 속에서 퍼지는 공간** (`p34.py`, clips `pull` + `swing`, mid from 5 b + far) — [stub: 32 t tell, pull to 1.3 b, 2 sectors 360°]
- [x] red haze + mist + arcs behind her 1-14, open-claw cast, rumble; cage of black red-edged cubes at the player 11-27
- [x] K14: undodgeable after ≥ 28 t, needs line of sight (no range limit; light / barrier pass), destination 1 b in
      front facing her (checked: a blocked destination falls back like a blocked line of sight)
- [x] K21: vignette 22-27 → white flash 28-29 → orange field + star 30 → red diamond 31 → reopening 32-38, as title
      font glyph frames (`rlk:mboss_gd`, 2 × 2 tiles of 256 × 144 px at 128 × 72 title units each, U+E500.., spaces
      U+E5F0/1), right in first person and the F5 seat view; `vBig` rests the F5 crosshair title meanwhile
- [x] K15: swing clip 10-14 t after the relocation; swing 1 (360°, r 5-6, waist band) at +20, swing 2 at +33 (14 t apart);
      gold crescents (`#FDF6A6/#DDBC78/#A37C4E`), dark cubes; 1.2 each
- [x] sounds: aura `respawn_anchor.charge`, `fire.ambient`, `warden.sonic_charge` (1.4); teleport `enderman.teleport`
      (0.6) + `respawn_anchor.deplete` + `illusioner.mirror_move`; swings `player.attack.sweep` + `trident.riptide_1`
- [x] tuning (played): cage 7-13, screen 14-30 (frames 1:1), line of sight 19, relocation 24 (tell 24 ≥ 20), swing clip
      at 36, swings r 6.8 at 51 / 64 (tell 15), 82 t; every band (melee weight 1: from closer than 5 b the core hops back
      to 6.5 b first), the stretch guarantee at any distance
- [x] rule 10-20: no ring decals (hz_vis 41 / 42 and `p/pull/vis` removed; quiet swings); the swing clip at 36, the hold
      glint at 41 and the riptide + knockback sounds 2 t before each swing are the tell

**P5 하늘을 심판하는 자** (`p56.py`, clip `flyslam`, far) — [stub: ring locked at 21, r 4.5, 20 t, body glides under it]
- [x] dark cubes climbing the shaft 0-12, glint 6, gold spiral ribbons 12-16, beam 16-19 with crescent arcs
- [x] take-off 19-23 to +8 b with a dark-cube trail; K26 ring locked at take-off + 1-2 t, grows to r 4.5, does not follow
- [x] falling gold 4-point sparkles 26-40; descent pillar 39-41; impact 41 (explosion, spikes 47-51 out to r 4-5,
      visual only), spear planted 41-71, pull-out 71-79, twirl 79-101; 1.8
- [x] sounds: ascent `ender_dragon.flap` (1.3) + `trident.riptide_3`; fall `beacon.deactivate` (1.8); impact
      `generic.explode` + `zombie.attack_iron_door` (0.6); spikes `pointed_dripstone.land` ×n + `amethyst_cluster.place`
- [x] tuning (played): glint 5, beam 12, take-off 14, lock 15, ring r 5.5 from 16 (28 rim bars, tell 15; centre within
      15.5 b of the axis), glide 18-29, impact 31, spikes to r 5.6, planted 31-61, 91 t
- [x] rule 10-20 (trim): the rim bars, glow fill, star emblem, sparkles and pillar stay; the dust progress circle is gone

**P6 sweeps** (`p56.py`, clips `sweep` / `sweep_e`; started by the core) — [stub: sector a 100 r 5, tell 19, act 5 / 8]
- [x] gold sweep (timeout): 180-210° front arc r 4.5-5 from her left to her right, 5 t, row of vertical crystal spikes
      along the arc edge, `#CC9C3C/#E4B43C/#FCFC84`; 1.65
- [x] enchanted sweep (record): enchant line through her R+4..6, wind-up with the element glow, 8 t active arc in the
      element colour + per-element strike fx (electro forked bolts and violet shards; pyro / hydro / cryo per model.md
      §4), lingering arcs to R+42; 2.5 + element, KB 4
- [x] sounds: wind-up `trident.riptide_2` (0.7); gold hit `player.attack.sweep` (0.6) + `pointed_dripstone.land` /
      `basalt.break` + quiet `generic.explode` (1.3); element hit sweep + `lightning_bolt.impact` (1.6-2.0, 0.5) + crackle
- [x] tuning (played): arc r 6 (rim, slabs, ribbons, spikes x1.2), gold slices 15-19 (front 17, clip 39 t), enchanted
      slices 16-22 (front 18, clip 45 t)
- [x] rule 10-20: no rim decal (`rim0`-`rim4`, the per-slice rim flash) and no progress arc; the guard-end swell and
      chest sigil / the record starburst and enchant line, the wind-up and its sounds are the tell

**Fail spears** (`p56.py`, pattern 13; clock 0 = T0) — [stub: decal + locked disc r 2.8 at +25/+56, tell 24, red→colour prop]
- [x] per spear j: gold cube column (23 + 31j), giant red copy of her spear point-down with the tip 3.6-3.9 b above
      the target (25 + 31j), concave 4-point star decal centred on the player, one arm at the centre, side arms opening
      from ±2.7 to > ±9 b in 6 t (visual only)
- [x] colour change red → star colour 37-40 + 31j; drop ≤ 1 t + impact 49 + 31j (flash column, starburst, dome ≈2.9 b,
      X of light beams 8-10 b, spike field gold ±8 b / ice splash ±4 b), spear planted ≈30 t, dissolves upward
- [x] K12: cylinder r 2.5-3, one hit per spear, dash i-frames apply, 2.2; voice on spear 1
- [x] sounds: forms `respawn_anchor.charge` (0.8) + `beacon.power_select` (0.6) + `amethyst_block.resonate` (0.8);
      hang `beacon.ambient` (0.5); colour `amethyst_block.chime` (1.5); pre-drop `trident.riptide_3` (1.4, 0.5); drop
      `trident.hit_ground` (0.5) + `lightning_bolt.impact` (0.8, 0.6); gold blast `generic.explode` (0.7) +
      `amethyst_cluster.break` + `pointed_dripstone.land` ×3 + `lightning_bolt.thunder` (1.6, quiet) + `basalt.break`;
      blue blast `generic.explode` (0.8) + `glass.break` (0.7) + `player.splash.high_speed` + `powder_snow.break`
- [x] tuning (played, the m4 schedule x0.75): column 17 + 23j, decal + lock 19 + 23j, impact 37 + 23j (tell 18); disc
      r 3.4 (24 ring bars; centre within 17.6 b of the axis), arms ±3.2 → ±11.4 b, dome r 1.75
- [x] rule 10-20 (trim): the star decal, streaks, column and giant spear stay; the hazard is quiet and the r 3.4 damage
      ring (24 bars) is gone; a flat ring of the star colour at r 3.4 at the impact (37 / 39 + 23j, `p/fail/ring<kind>`)

## 12. Deviations and open points (core)

Pattern deviations accepted at the merge (authors' notes, verified against the generated functions and the mcsim tests;
numbers after the user tuning, plan.md "공격 선딜 좀 짧게 하고 공격 범위를 좀 늘려봐": every damaging wind-up ~25 %
shorter through the rig's `RETIME`, every hit area ~20 % larger with its decal and fx, the coefficients unchanged):
- P1: lanes 9.3 × 2.9 b from the coil spot (lock 11) and 8.4 × 2.7 b from the dive spot (lock 34; was 8.5 × 2.4 / 7.0 ×
  2.2 at 16 / 42); hit 2 volume = the 6 b dash path plus its end; the rig's spear tip reaches about 3.5 b past the
  player at 46 (visual only).
- P2 (K23): aim and lane lock at clip 17 (= launch − 10, the tuned floor); the beam at 20 is the last flash; the lane is
  1.2 b wide (whole tenths only; plan: about 1.25).
- P3: the visual impact is centred on the measured planted tip (3.1 b), the hazard stays at 3.5 b (K25) with r 6 (was 5);
  the close-in stays 3 b. With tell 13 a player at 3 b needs a dash to leave the disc (or dashes through the strike).
- P4: line of sight checked at 19 (before the flash), no range limit; blocked (or a blocked destination at 24) → the
  cage shatters, the screen clears and she swings in place (#gp4Ok 2, the pattern resolves); a refused pull (dead,
  reviving, selection screen, map view) ends P4 at 32 with no swings; head-height cage cubes only around the
  shoulder-view avatar; `p/pull/pause` ends the screen overlay. Picked in every band: melee at weight 1 (P1 / P3 2),
  mid 1, far ×3, plus the once-per-stretch guarantee at any distance (plan.md "P4 for melee players"; plan K2 had far
  only, the first fix the mid band from 5 b, which a melee player never left). From closer than 5 b the core first
  hops back to 6.5 b (`ai/back`, 12 t, clip `backstep`), then the normal P4 runs. The swings are r 6.8 (plan about
  6.5-7) with tell 15; the 12 t relocation → swing-clip gap (K15 10-14 t) stays, so a player sprinting out right after
  the pull escapes them.
- P5: the landing point locks at 15 (take-off + 1) and is pulled to within 15.5 b of the axis (the r 5.5 ring stays in
  the walkable arena), the hazard is created at 16, impact 31. With tell 15 leaving the ring takes a dash.
- P6: the sweeps strike in blade slices (gold 15-19, front 17; enchanted 16-22, front 18), arc r 6 (was 5), one hit per
  sweep.
- Fail spears (the m4 schedule x0.75): target locks at 17 (gold column; pulled to within 17.6 b of the axis), hazard +
  decal at 19 (tell 18), impact 37, spears 23 t apart; disc r 3.4 (was 2.8); the blue spear goes red → electro
  (violet) at 28 → hydro (blue) at 30 (no pink prop model).
- Block displays use `block_state:{id:"minecraft:…"}` everywhere (the project's 26.3 form; core, proto and every
  pattern aligned at the merge).


- `chaos_charge` holds the spear level for 30 t (the clip), not the 20 t of plan.md's chaos line; timer and stars start
  at the hover (clip tick 36 after the landing).
- Active stars take their own element with 40 % RES (user decision, replaces the plan's immunity; `OWN_EL_RES` in
  core.py). A one-element character that records its own element in both guards still breaks both stars in ≈ 10.5 s.
- Star pools assume a skill-light full-damage kill time of ≈ 75 s at the zone level (`KILL_S`; 4.2 % / 1.7 % per
  star ≈ 5.3 s each); measure in game with `test/start` and adjust `STAR_PM` / `KILL_S` in core.py (the build asserts
  10-12 s for both stars).
- Stars 3.4 b apart (±24°, plan 3-4 b; the source has them touching under her, 0.7-1.5 b).
- Fail: she departs 10 t after the last impact (m4 +90) instead of after the planted spear's dissolve.
- The record counts every hit with `#elem 1-4` (no `#apply`/ICD gate), reactions (`#tfm 1`) excluded.
- The pull LOS check and the cage displays are P4's job (the open arena has no obstacles today).
- The shuffle bag draws every candidate of a band once per cycle, so the band weights only order the draws: in melee P4
  is about a third of the picks (P1 / P3 / P4 alike), as in the far band (P2 / P4 / P5). The guarantee then rarely has
  to fire.
- Body-centred areas (P3 disc, P4 swings, P6 arcs) can reach past the wall ring when she stands near it (she stays
  within the 18.5 b safe disc); the 7 b high wall hides those decal parts. Areas anchored on the player (P5 ring, fail
  disc) are pulled inside the walkable r 21 instead.
