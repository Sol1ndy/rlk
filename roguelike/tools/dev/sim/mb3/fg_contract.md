# Experimental Field Generator (실험성 역장 발생 장치, nameplate 브레게 프로토타입) module: core <-> pattern contract

Worktree branch `wip/fg-core` (from `wip/bf` f2ab515). It holds the module core, the framework options of §7, and stage-1
pattern stubs whose hit ticks, areas, coefficients, volley groups and telegraphs are final. Branch `wip/fg` (the module
branch) merges the fx kit of `wip/fg-fx` and wires it (§15: hooks, meter, banner, flags, boss-bar lines; api helpers in
§7.8). The real rig of `wip/fg-rig` is not merged yet (§15). `DP` = `roguelike/`, `F:` = `DP/data/rlk/function/`,
`G:` = `F:mboss/fieldgen/`, `S:` = the scratchpad. The framework contract (hooks, libraries, units) is
`S:mboss/contract.md`, extended by the butterfly's `S:mb2/bf_contract.md` §7 and by §7 below. The binding design is
`S:mb3/plan.md`; the research notes are `S:mb3/understand/v1..v4.md`, `model.md` and `S:mb3/code/adapt.md`; the kit API is
`S:mb3/fg_fx_api.md`. This file is the contract between the field generator **core** and the **pattern modules**
(`cruise`, `field`), so pattern authors can work in parallel. It follows `bf_contract.md` section by section.

---------------------------------------------------------------------------------------------------

## 1. Files, ownership, build

| file | owner | content |
|---|---|---|
| `tools/build_mboss_fieldgen.py` | core | entry script (`python3 tools/build_mboss_fieldgen.py`) |
| `tools/mboss_fieldgen/__init__.py` | core | package doc, `PATTERN_MODULES = ('cruise', 'field')` |
| `tools/mboss_fieldgen/api.py` | core (stable) | `Pattern`, `Gen` writer helpers, `TL` timeline, `DMG`, `KB`, bands, radii, colours, the HUD glyph table, the rig clip table read from the manifest (`ev`, `ev_or`, `clip_len`, `part_sel`), the shared 파쇄 helper `rocks` / `rocks_cancel` |
| `tools/mboss_fieldgen/core.py` | core | 17 hooks, AI + range-band bag, the field sequence (services 20 / 22), the 20-hit meter, break, groggy, recovery, field damage cut, low-gravity request, body clamp, per-form hitbox, entrance, death, HUD, tests, vanilla core fx `G:cfx/**`, generated dispatchers |
| `tools/mboss_fieldgen/cruise.py` | cruise-pattern author | `bomb` (1 C1), `slam` (2 C2), `laser` (3 C3), `missile` (4 C4), `burst` (5 C5), `rock` (6 C6) |
| `tools/mboss_fieldgen/field.py` | field-pattern author | `fzone` (11 F1), `frock` (12 F2), `waves` (21 「인력 충격파」 x3, service) |
| ~~`tools/mboss_fieldgen/stub_rig.py` + `stub_rig_manifest.json`~~ | core, **removed (FGI2, §18)** | the stage-1 stand-in rig `G:rig_stub/**`; the real rig manifest `tools/mboss_fieldgen_rig_manifest.json` is now required |
| `tools/build_mboss_fg_fx.py` (+ `mboss_fg_fx_paint.py`, `mboss_fg_fx_stub_rig.py`) | fx kit (`wip/fg-fx`, merged into `wip/fg`) | `G:fx/{card,cardx,look,clear,uninstall}` + `G:fx/{e,p,tele,snd,hud,prop,test,rig_stub}/**`, RP `fg_kit/*`, font `rlk:mboss_fg` (U+E700-E7FF), manifest `tools/mboss_fg_fx_manifest.json` (API: `fg_fx_api.md`) |

- The generator owns all of `G:**` **except** `G:rig/**` (the rig generator) and the kit's owned paths. `core.foreign()`
  returns `rig/` plus the kit manifest's `owned` dirs / files united with the kit's own constants (`K.OWNED_DIRS`,
  `K.OWNED_FILES`), as the butterfly core does; any other name under `G:fx/` is the core's (fg_fx_api.md §0). Stale files
  are deleted on every run, but only in what the generator owns. That includes `G:rig_stub/**` once the real manifest
  exists. Writing into a foreign path is an assertion error. Never hand-edit generated files.
- A pattern module writes **only** `G:p/<key>/**`, through `gen.pw(key, name, lines)` (or `TL.write`). It never edits
  `api.py`, `core.py`, the registry, the framework or the other module.
- **Generator order** (README "등록 · 모듈"). Every generator writes and cleans only its own paths, so any order and a second
  run give the same bytes. `S:mb3/tests/gen_check.py` checks this.
  1. `python3 tools/build_mboss_core.py` (the framework, whenever the registry or `mboss_lib` changes);
  2. `python3 tools/build_mboss_arena.py`; 3. `python3 tools/build_mboss_proto.py`;
  4. the rig generators with the resource pack (Guardian, butterfly, and later the field generator rig: `G:rig/**` +
     `tools/mboss_fieldgen_rig_manifest.json`);
  5. `python3 tools/build_mboss_guardian.py`; 6. `python3 tools/build_mboss_bf_fx.py --resourcepack <RP>` (`--skip-rp` for
     the datapack only); 7. `python3 tools/build_mboss_butterfly.py`;
  8. `python3 tools/build_mboss_fg_fx.py --resourcepack <RP>` (`--skip-rp` for the datapack only; about 17 s);
  9. `python3 tools/build_mboss_fieldgen.py` (it imports the kit's call builders and reads its manifest's `owned`, so
     the kit goes first by convention; either order gives the same bytes);
  10. `python3 tools/check_mboss_pack.py`.
  `gen_check.py` runs this order, a second time, the reverse order, `G:` wiped (except `rig/`) and rebuilt core → kit and
  kit → core, an ownership probe (a stray file in `fx/p/` survives the core, a stray core name under `fx/` does not), and
  with `RP=` both kits' resource-pack builds twice.
- **Rig merge.** Every rig call goes through `Gen.rig/play/look/form/crack/prop`. These point at `rig_stub/` while
  `api.STUB` is true and at `rig/` once `tools/mboss_fieldgen_rig_manifest.json` exists. At that point delete `stub_rig.py`
  and `stub_rig_manifest.json` and rebuild. The build prints a note for every clip event it had to default (`ev_or`), so a
  renamed event in the real manifest shows up at once. `api.NEED_CLIPS` (the 19 clips of the task) must all exist.
- `core.build()` asserts that ids and keys are unique, ids 1-6 are cruise normal, 11-12 field normal and 21 a field
  service, nothing else besides 20 / 22 (core services), every pattern wrote `start`, `tick` and `cancel`, and the intro /
  death lengths fit the registry `intro` 130 / `death` 110.

## 2. A pattern module

```python
from .api import Pattern, TL, ev_or, clip_len, DMG, KB, CY, NS, L, rocks, rocks_cancel, GOLD
PATTERNS = [Pattern(2, 'slam', '내려찍기', 'c', 'slam', bands=('melee', 'mid'), weight={'melee': 2},
                    max_len=clip_len('slam') + 7, length=clip_len('slam'))]
def emit(g):                      # g = api.Gen
    tl = TL(g, 'slam'); tl.at(0, ...); tl.at(17, ...); tl.at(45, g.end())
    tl.write(['# start header'], ['# tick header'], extra_tick=[...])   # writes start, tick, k/<t>, d/<a>_<b>
    g.pw('slam', 'cancel', [...])
    # optional: 'vis' (hz_vis events), 'pj_end' (projectile events), 'pause' (fight frozen), any helper you call
```

`Pattern(id, key, label, state, clip, kind='normal'|'service', bands=(...), lead=0, recover=20, max_len=120, length=None,
weight=None)`:
- `id`: 1-6 cruise C1-C6, 11-12 field F1-F2, 21 「인력 충격파」 (service; the core starts it). 20 is the field opening and 22
  the pack-up, both core services. These numbers are stable.
- `state`: `'c'` (cruise) or `'f'` (field). It picks the bag of that state; the core never runs a pattern in the other state.
  A test request (§11) switches the device state first.
- `clip`: **the core plays it at clock 0** (`G:p/clip_d`). For a later clip of yours, call `g.play(clip)` at its tick.
- `lead`: the start runs at clock `-lead` (0..20). All stubs use 0.
- `bands` (melee <= 4 b, mid, far >= 8 b), `weight` {band: 1-9}, `recover` (idle ticks after the end), `max_len` (a safety
  end) and `length` (the real end, for the pattern bar; `g.set_len(t)` when it is decided at runtime) work as in the
  Guardian and the butterfly. Every hit is Geo (`Pattern.el` = 5).

## 3. Entry points and the pattern clock

| function | called | executor / position | rule |
|---|---|---|---|
| `G:p/<key>/start` | once, on the tick the pattern begins (clock `-lead`) | `@s` = body, at the body (rotation = body yaw) | the core has already played the clip if `lead` is 0 |
| `G:p/<key>/tick` | every following fight tick | `@s` = body, at the body | `#fgPT mb` = -lead+1, …, 0 (clip played), 1, 2, … = **the clip tick** |
| `G:p/<key>/cancel` | the core aborts it (§4) | the caller: **use selectors, not `@s`** | remove everything you own; idempotent |
| `G:p/<key>/vis` | optional, `hz_vis` of your hazards | `@s` = hazard marker | `#hzEv mb` 0 create / 1 strike / 2 end; `@s mbHzV` = **pattern id × 10 + k** (k 1-9; `vis=111` for F1, `211` for the waves) |
| `G:p/<key>/pj_end` | optional, `pj_end` of your props | `@s` = prop | set `@s mbId <pattern id>` before `pj/launch`; `#pjEv`, `#pjKeep` per the framework |
| `G:p/<key>/pause` | optional, once when the fight freezes while it runs | `@s` = body | drop whatever would hang in the world; the clock continues after the resume |

- Module tick order: clocks and the hit flash, the meter fx (`brk/count`), the break (`brk/begin`), the pip flash, the field
  clocks, the body clamp, the AI state, **the slot** (`p/run`: start / tick, then the core service mechanics `p/svc`, then
  the finish), the low-gravity request, and **the rig tick last**. So a clip you play in `start` / `tick` renders the same
  tick. Hazards you re-aim or resize from `tick` / `extra_tick` take effect in this tick's hit test, because the
  framework's `hz/all` runs after the module tick.
- `TL(g, key)`: `at(t, *lines)`, `span(t0, t1, *lines)`, `write(start_head, tick_head, t0=-lead, extra_tick=())`. Busy ticks
  become `p/<key>/k/<t>` (`k/m<n>` for negative t), reached through a binary dispatch on `#fgPT`. `extra_tick` lines run on
  every tick before the dispatch (per-tick aim and growth). `Gen.at/every` remain for one-liners (moduli `#fgK2 3 4 5 6 8
  10 20`; `#fgK11` and `#fgK40` also exist).
- Moving the body: `mv/*` as the body, `g.bstep(...)`, or `tp @s`. The body (husk) is the rig anchor and the hitbox. It
  stays on the floor; the cruise hover (ring centre about 4.5 b up) and the field height are in the rig forms. While a
  framework glide moves it (`rlk_mb_mv`) the core's leash is off; otherwise a body outside r 16.5 is pulled back 0.3 b/t.

## 4. How a pattern ends, cancel rules

- **End:** `g.end()` (`G:p/end`), normally at clock = clip length. The core finishes the slot after that tick
  (`p/finish`): it clears the slot, `#mbNoLeash` and `rlk_mb_inv`, kills `rlk_mb_fg_lock`, **`rlk_mb_fg_kept`** and
  **`rlk_mb_fg_pat`**, then hands over. A normal pattern goes to idle + `recover`; 20 continues the field opening; 21 goes
  to the field patterns (opening waves, `#fgWvK 1`) or the pack-up (closing waves, `#fgWvK 2`); 22 returns to cruise.
- `max_len` is only a safety net. `g.release()` hides the pattern bar while a harmless tail plays. The slot stays busy
  until `end()`, and **the AI is never stopped** (the butterfly's S2 froze it).
- **Cancel** happens on tests (`test/cut`), the **break** (`brk/begin`: `lib_clear` first, so every hazard, prop, pull
  and glide is gone), death (`death_start`) and `/reload`. `p/cancel` runs your `cancel`, then kills the three core tags
  above and the warp glitch marker. Your cancel removes the rest. Unthrown slabs and helper displays should carry
  `rlk_mb_fg_pat`, so they go even when your cancel misses them.
- Never deal true damage, never call `combat/apply`, never change `#fgSt`, `#fgField`, `#fgOpen`, `#fgBrk`, `#fgLowG` or any
  other core state. Never touch `#mbLowG` or the low-gravity modifiers, and never count meter hits yourself.

## 5. State, scores, form, range info

All fake players live in objective `mb`. Core names are `#fg*`; **pattern modules use `#fq<id><name>`** (stubs: `#fq6K`,
`#fq12K`, `#fq11N`, `#fq21K`, `#fq21T`). Scratch you may clobber inside one function: `#fgM` (modulo helper), `#fgX`, the
framework scratch `#t #x #y #z` and `#hzSzR/#hzSzR0/#hzSzW` (resize). Storage: your own sub-paths of `rlk:mboss fg`
(stubs: `fg.tl` throw lines, `fg.fz` F1 placement, `fg.wv` wave rim); the module's `cleanup` and `uninstall` remove
`rlk:mboss fg`. On your own entities you may use the framework objectives `mbT` (age), `mbS` (index / group), `mbId` (pj).

| score | meaning | access |
|---|---|---|
| `#fgPT` | pattern clock (clip tick; negative during the lead) | read |
| `#fgPat` / `#fgPick` / `#fgLast` | running slot pattern / the last pick / no-repeat memory | read |
| `#fgSt` | 0 idle, 1 pattern, 3 groggy, 4 recover, 6 break, 7 dying | read |
| `#fgField` | 0 cruise, 1 warp (opening), 2 opening waves, 3 field patterns, 4 closing waves, 5 pack-up | read |
| `#fgOpen` | 1 while the meter is open (unfold → break / pack-up): the damage cut and the meter count | read |
| `#fgBrk` / `#fgCrack` | meter count 0-20 / crack stage 0-3 (4 = burst) | read |
| `#fgLowG` | 1 while the field holds low gravity (the core re-asks `#mbLowG` every tick) | read |
| `#fgWvK` | the waves run: 1 opening, 2 closing | read |
| `#fgTri` | test 42: force the triple third wave (otherwise HP < 50 %, read from the body's `mhpC` / `mhpM`) | read |
| `#fgBand` / `#fgDist` | band at the pick (1 melee, 2 mid, 3 far) / distance in tenths | read (fresh: `function rlk:mboss/mv/dist` → `#mbDist`) |
| `#fgCruN` / `#fgCruLim` | cruise patterns done / before the next field (5 the first time, then 4) | read |
| `#fgFT` / `#fgFN` | field-pattern clock (the closer at 400) / fields opened so far | read |
| `#fgPLen` | the pattern bar's end | write via `g.set_len` |
| `#mbLock` | test lock: 1-6 that cruise pattern only, 11-12 that field pattern only, 17 the field cycle only | read |
| `#mbNoLeash` | 1 during a scripted flight beyond the safe disc; the core resets it | write |

## 6. Damage and hazards

- Coefficients (`api.DMG`, % of the registry base hit `atk 12 × dmgMul 110`; 10-20 user ×1.5, §21): C1 bomb 150 (one
  hit per group of 4) and slam 270, C2 270, C3 75 per touch (one group, re-armed every 10 t), C4 165 per missile
  (2 groups), C5 330, C6 burst 225 and slab 180, F1 75 per event (one group), F2 105 / 120, wave 75 per front (the fix
  round's balance, §19, was 100 / 180, 180, 50, 110, 220, 150 / 120, 50, 70 / 80, 50; before it 80 / 140, 140, 50, 90,
  220, 130 / 110, 120, 130 / 110, 120). Raw values before defence and level (floored): 0.75 = 9, 1.05 = 13, 1.2 = 15,
  1.5 = 19, 1.65 = 21, 1.8 = 23, 2.25 = 29, 2.7 = 35, 3.3 = 43. Knockback `api.KB`: default 3, light 2, heavy 4, none 0.
- Element: every hit is Geo (registry `el` 5, the hazard default). The boss has **no element RES** (`mres` 0, nothing reads
  `#elem`). While the field is up it takes **×0.6** from everything (`incoming` → `field/cut`, reactions included, at least
  1; plan "모든 저항 증가").
- **Telegraph floor:** every damaging hit is made at least 10 t before it can hit (`tell` >= 10), behind a readable tell of
  the device's motion and sound. `test_fieldgen.py` §9 checks it for every hazard made.
- **Telegraph rule (10-20, user; §21):** a ground decal only where the reference footage shows a marker on the floor
  before the hit: C5 지면 충격 (`g.tele_rim` + `g.tele_dark`), F1 감소 영역 (`g.tele_dark`), the C1 finisher / C2 slam (the
  late base flare `p/column_base`). Every other hazard is quiet with no decal and no dmg-0 line; the player reads the
  motion and sound. `pat_cruise.py` / `pat_field.py` §0 check that the set of hazards drawing a ground telegraph is
  exactly {C1-slam, C2-slam, C5-blast} / {F1-zone}.
- **Heights** (`#hzY0` / `#hzY1`, `g.hz_opts(y0=, y1=)`): slams 0-2.0 b; C5 blast and the waves are low (0-0.5 / 0-0.7 b) so
  a jump clears them; C6 / F2 bursts 0-1.2 b, which a low-gravity jump (apex about 3 b) also clears; beams -0.5 to 2.0 b.
- Ground targets on the player use `g.lockp()` (pulled into the walk disc r 20.3, so a wall-hugger is still covered). Points
  the body moves to use `g.lockb()` (r 16.5). The body never goes beyond r 16.5, so the spikes clear the wall ring.
- Direct swings (no hazard) follow the butterfly's rule: `function rlk:mboss/hurt` as the attacker with `#mbHitPct`,
  `#cmEl tmp`, `#mbKB`, `#mbKBDir`; you own the one-hit-per-swing rule. The stubs have none.

## 7. Framework options (new in `tools/build_mboss_core.py` + `mboss_lib.py`) and module helpers

All options are opt-in. Without them every hazard, projectile and the Guardian / butterfly outputs behave exactly as
before (`S:mb3/tests/ident.py`: 0 changed files under `F:mboss/{guardian,proto,butterfly}`). Each option is tested on its
own in `S:mb3/tests/test_fwopts.py`.

### 7.1 `#hzNoDodge 1`: dash i-frames do not help (`g.hz_opts(nododge=1)`)
A one-shot option (reset by `opts_reset`). `hz/init` copies it into the hazard (`mbHzND`). On a hit, `hz/hurt` sets
`#mbNoDodge mb` around `mboss/hurt`, which then calls `mboss/hurt_nd` instead of `cm/hit_pl2`: the player's `dashInvT` is
saved, set to 0 for the call and restored, so the player keeps the i-frames for the next hit. `#mbNoDodge` is 0 again
right after. Used by the waves (a jump clears them, a dash does not).

### 7.2 `hz/aim`: re-aim a live hazard (`g.hz_aim()`)
As the hazard marker, positioned and rotated where it should be: `tp @s ~ ~ ~ ~ 0`, and the frozen forward axis of the hit
test (`mbHzFX` / `mbHzFZ`) is recomputed as `hz/init` does. Call it from the module tick (pattern `tick` / `extra_tick`),
which runs before `hz/all`. C3: `execute as <beam> at <body> rotated as @s rotated ~5 0 positioned ^ ^ ^2.8 run function
rlk:mboss/hz/aim`. Tag the hazard just made with `g.tag_last_hz(tag)`.

### 7.3 `hz/resize {r, r0, w}`: change a live hazard's size (`g.hz_resize(r, r0=0, w=0)`, blocks)
Tenths at the runtime boundary. `r` / `r0` are the outer / inner radius of a disc, ring, sector or full (r0 = the safe
hole), or the length / back of a line; `w` is a line width (0 = keep). The bounds are recomputed with the 0.3 b body pad;
`r` is clamped to 0..40 b. The score form without a macro: set `#hzSzR #hzSzR0 #hzSzW mb` and call `hz/resize_s`, as the
wave front does every tick. A loud hazard (`#hzQuiet 0`) has its framework outline redrawn; a quiet one does not.

### 7.4 `#hzRearm N`: a lingering hazard hits again (`g.hz_opts(rearm=N)`)
A hit (or a dash-dodged hit, which also consumes it) disarms the hazard for N ticks of the re-arm clock `#mbHzClk`, which
ticks in `hz/all` and therefore freezes with the fight. Volley-group members re-arm together (`grp_mark`), so a group of two
beams hits at most once per N t. C3: N 10 on both beams in one group.

### 7.5 `#mbLowG`: low gravity on the player and the shoulder-view avatar
- A per-tick request: `mboss/main` sets `#mbLowG mb 0` first, and a module tick sets it to 1 while it wants low gravity.
  The field generator does this after its slot, while `#fgLowG` is 1, from the banner (field opening clock 56) to the
  break, the pack-up or death.
- `rlk:tick` (shared edit, after `player/swing/tick`, before the view tick): while `#mbLowG` is 1, `mboss/lowg_on` runs as
  every player (the player and every `rlk_av` avatar mannequin). Otherwise, if anything carries `rlk_lowg`, `mboss/lowg_off`
  runs. Modifiers `rlk:mb_lowg`: gravity -0.5 `add_multiplied_base` (×0.5), jump_strength +0.19 `add_multiplied_base`
  (×1.19, apex about 3 b, about 25 t of air time), safe_fall_distance +4 `add_value`; tag `rlk_lowg`. They are re-added
  every tick, so a re-created avatar gets them at once. They are multiplicative so the camera player (gravity base 0) stays
  put. The swing hold (jump ×0) and every other ×0 jump lock still win.
- Cleanup paths: a pause (the module tick stops, so the request lapses and the next tick removes the modifiers), the
  break, the pack-up, death, every framework end (`player_reset` sets `#mbLowG 0`), a vanished body, a relog, and
  `mboss/uninstall` (`lowg_rem` on `@a` and on every `rlk_lowg` entity). `mboss/init` keeps the score in 0..1.

### 7.6 The avatar jump (`view/move`, shared edit)
The shoulder-view avatar's jump velocity is now the avatar's own `jump_strength` (`Motion[1]` = `attribute get`): 0.42 by
default (unchanged) and 0.4998 with low gravity.

### 7.7 Butterfly helpers (unchanged, available)
`pj/steer {max}` homing, the blade hit shape `#pjShape 1` (**reach = hr + 0.65 b**, review FW-1: `api.rocks` throws hr 0.8,
a 1.45 b reach), volley groups `GRP_NEW` + `grp=True` (every member must exist before the group's first strike: FW-4),
and telegraph-only hazards `dmg 0` (`g.tell_line`). See `bf_contract.md` §7.

### 7.8 Module helpers (`api.Gen`)
- `g.lockp()` / `g.lockb()`: marker `rlk_mb_fg_lock` under the player (walk disc r 20.3 / body disc r 16.5). **Keep** it with
  `g.keep(<your tag>)`, which kills the old marker of that tag, re-tags the new one and adds `rlk_mb_fg_kept`. The core kills
  every kept marker at `p/finish` and `p/cancel`, so no later run aims at an older run's marker (butterfly S1).
- `g.clamp_walk()` / `g.clamp_body()` as a marker; `g.bstep('toward'|'away'|'fwd', d)` as the body (only into free spots
  inside r 16.5); `g.tag_last_hz(tag)`; `g.set_len(t)`; `g.release()`; `g.end()`.
- `g.sound(event, vol, pitch)` (vanilla, hostile), `g.dust`, `g.particle`, `g.ring_dust`, `g.say(text, colour)` (mechanics
  captions only; a machine has no voice lines).
- `api.rocks(g, tl, key, pid, burst0, n_burst=8, gap=6, throw0, n_throw=5, throw_gap=8, dmg, dmg_s)` (C6 and F2): a walker
  marker 6 b from the player on the device's side, n bursts (`hz/disc` r 1.8, tell 10, y1 1.2, heavy KB, `vis` pid×10+1)
  each 2.5 b nearer the player, a tuff slab rising 4 b at every burst, and from `throw0` one slab every `throw_gap` t at the
  player's locked feet (a dmg-0 line 10 t ahead, then a blade pj 1.5 b/t, life 24, its own group; `pj_end` shatters it). It
  returns the clock of the last landing; `rocks_cancel(pid)` lists the cleanup lines. Tags `rlk_mb_fg_p<pid>w/s/f/t<j>/tl`.
- `api.part_sel(name)`: the selector of a named rig part (`ring`, `core`, `halo`, `pend`, `medal_e`, `medal_g` in the stub)
  for fx anchors; `None` when the rig has no such part.
- `api.rest_anchor(form, name, default)`: a rig anchor of a rest form from the real manifest's
  `form_states.<form>.rest_anchors` (rig coordinates x left, y up, −z forward), `default` while the stub has none.
  `api.CORE_FIELD_H` = the field core height (4.1; the kit's own docs say 3.84 for its stub rig).
- **The fx kit** (THE effect engine, `fg_fx_api.md`): `api.K` is `tools/build_mboss_fg_fx.py` (tables `K.PRESETS`,
  `K.SOUNDS`, `K.PROPS`, `K.KINDS`, `K.GLYPHS`, colours `K.GOLD`, `K.VIOLET`, …, `K.digits`, `K.pips`, `K.RIG()`); pattern
  modules never import it themselves. On `Gen`, each returns one function line to run in the kit's executor context
  (positioned at the event point, rotated as the aim):
  - `g.fx(name, **args)` (preset `fx/p/<name>`), `g.snd(name)` (recipe `fx/snd/<name>`);
  - `g.tele_disc(r, tell, el=5, hold=3)`, `g.tele_ring`, `g.tele_sector`, `g.tele_line(len, w, tell, el, hold, back)`,
    `g.tele_wave(r0, r1, w, tell, dur, el=9)`, `g.tele_mline(id, len, w, tell, el, hold, back)`, `g.tele_mline_aim(id)`,
    `g.tele_mline_turn(id, d)`, `g.tele_mline_end(id)`, `g.TELE_CLEAR`: decals in blocks (tenths at the boundary). Pair
    each with its `hz/*` made in the same tick with the same `tell` and `g.hz_opts(quiet=1)` (+ `sfx=0` when the kit's
    recipes give the sound);
  - `g.kprop(name)` (as `@s` = your item_display: the kit look `fx/prop/<name>`; `g.prop(name)` stays the RIG's prop),
    `g.klook(kind, col)`, `g.kcard(kind, pos, rot, col, col2, **K.card args)` (tints as an RGB int, `#RRGGBB` or
    (r, g, b) 0..1), `g.khud(name)` (pops, flashes, notices only: the meter, banner and flags are the core's, §15);
  - `g.kit` = `K`.

## 8. FX, sound, tags

- Every entity you create carries `rlk_room`, `rlk_mb_aux`, `rlk_mb_fg_pat` and a tag of yours starting with
  **`rlk_mb_fg_p<id>`**. Reserved core tags: `rlk_mb_fg_lock`, `rlk_mb_fg_kept`, `rlk_mb_fg_pat`, `rlk_mb_fg_fx`,
  `rlk_mb_fg_fxw` (warp glitch), `rlk_mb_fg_pnew` (transient: tag, set scores, untag in the same function), the stub rig's
  `rlk_mb_fgs` / `rlk_mb_fg_prop` and the rig part tags `rlk_mb_fg_<part>`. The kit uses `rlk_fk*`, `#fk*` and `rlk:fgkit`.
- Particles are `force @a[tag=player]` (the helpers do it). Never put world quads at the eyes: the F5 seat camera sees
  them. Field pebbles drift at the player's feet.
- Sounds are **vanilla only** and mechanical / brass (anvil, chain, piston, beacon, respawn anchor, amethyst, trial
  spawner, vault, breeze, crafter, tuff / basalt). Use the kit's recipes `g.snd(name)` (fg_fx_api.md §6); single layers
  `g.sound(...)` for anything a recipe does not cover.
- Looks: the core owns `look/idle|field|groggy|off` and the crack stages. A pattern that wants `look/charge` must restore
  the state's look in `tick` / `cancel` (cruise `idle`, field `field`).
- Telegraphs: the stage-1 stubs still let the framework draw the outlines (`#hzQuiet 0`). When a kit decal replaces one,
  pair it with the `hz/*` in the same tick, with the same `tell` and `g.hz_opts(quiet=1)`. The core clears every kit
  decal (`fx/tele/clear`) on pause, the break, death and test cuts; remove your moving lanes (`g.tele_mline_end`) in your
  `cancel` too.

## 9. Rig clips (from the manifest; ticks at 20/s; events = clip ticks)

(The table below is the stage-1 stub's. Since the rig merge the real manifest rules: §18 lists its numbers.)

The rig API (`rlk:mboss/fieldgen/rig/…`; `@s` = the anchor = the body, as / at it): `init`, `spawn`, `tick` (every game
tick, after the AI), `kill`, `play/<clip>`, `form/{dormant,cruise,field,coreup,tower,laser,deployed}` (instant),
`look/{idle,charge,field,groggy,off}`, `crack/{0..4}`, `face/player`, `face/track`, `flash`, `prop/clear`. The clips switch
forms themselves (stub manifest `forms`); `warp_out` hides the rig from 13 and `warp_in_field` shows it at 0 (`hidden`).

| clip | len | then | events (stub manifest; the real rig manifest rules) |
|---|---|---|---|
| `idle_cruise` / `glide` / `field_idle` / `groggy` | 80 / 20 / 80 / 40 | loop | |
| `entrance` | 112 | idle_cruise | clank 16, pods 24, unfold 28 (cruise form), eye 54, turn 60, rise 80, **risen 110** |
| `bomb_run` | 58 | idle_cruise | turn 0, ports 10, **run 12**, end 57 |
| `slam` | 45 | idle_cruise | column 0, plunge 13, **impact 17**, rise 24 |
| `laser` | 174 | idle_cruise | drop 0, charge 4, aim 22, **fire 24**, off 157, retract 158 |
| `missiles` | 70 | idle_cruise | flare 0, vent 8, **launch 21**, last 34 |
| `coreup` | 110 | idle_cruise | spark 0, **rim 3**, lift 5, beam 29, column 41, **blast 48**, sink 81 |
| `tower_throw` | 157 | idle_cruise | dip 0, vent 12, tower 20, band 38, **burst 55**, **throw 95**, revert 142 |
| `warp_out` | 34 | hold | flip 0, **out 13** (hidden) |
| `warp_in_field` | 24 | field_idle | in 0, **unfold 1**, **banner 22** |
| `wave` | 36 | field_idle | charge 0, beam 23, **impact 24** |
| `field_erupt` | 40 | field_idle | activate 0, **erupt 22** |
| `field_end` | 78 | idle_cruise | lift 0, rise 2, lances 22 (deployed), pack 50 |
| `break` | 34 | groggy | bubble 0, **burst 5**, tilt 5, **wobble 14**, sink 34 |
| `recover` | 15 | idle_cruise | relevel 0, **flip 6** |
| `death` | 106 | hold | flicker 0, **drop 20**, **sink 40**, **out 90** |

The core reads the bold events through `ev_or` with these defaults. The patterns read theirs the same way.

## 10. What the core does (for orientation)

- **Entrance** (intro clock = clip tick + 1): the rig folded (`form/dormant`, `look/off`), floor dust and a low hum; the
  clank at 16, the unfold at 28, the eye at 54 (the nameplate 브레게 프로토타입 on the sub-line, `look/idle`), the rise from
  80, and the fight at **intro 111** (the rise has ended; the registry `intro` 130 is the cap). It is untargetable and
  deals no damage until then.
- **Cruise**: it tracks the player at 4°/t and keeps 6-10 b (glides in at 0.18 b/t, out at 0.15 b/t, only inside r 16.5).
  Picks come from the range-band weighted shuffle bag with no immediate repeat: C1 mid / far×2, C2 melee×2 / mid,
  C3 melee×2 / mid×2, C4 far×3 only, C5 melee×2 / mid, C6 mid×2 / far. An empty bag for the band refills; if that still
  gives nothing, the band alone decides (ignoring the bag), and C1 is the last fallback. Under-bar (gold): cruise patterns
  done toward the next field.
- **The field**, after 5 cruise patterns the first time and 4 later, at a pattern boundary:
  - Service 20 (`warp_out` clip): the halo flips 0-12, the warp-out flash at 13 (untargetable, teleported to the arena
    centre facing the player, a violet glitch over the old spot), the `warp_in_field` clip at 34.
  - At 35 the unfold: targetable, **the meter opens** at 0/20 (crack 0), `look/field`, the field hitbox, the ×0.6 damage
    cut, and the first field's hint "코어를 공격해 역장을 깨뜨리세요" for 120 t.
  - At 56 the banner "중력이 감소하고 점프 능력이 향상됩니다" and **low gravity**.
  - Then the opening waves (service 21) and **400 t of field patterns** (F1 / F2 from the field bag; the device stays at
    the centre and tracks at 3°/t). Unbroken, the closing waves follow, then the pack-up (service 22, `field_end`: the
    meter, low gravity and the cut end at 0, compact at 78). Then cruise, with 4 patterns to the next field.
- **20-hit meter** (`on_hit`; replaces the 3 Pneuma hits): it counts only while open. Reactions and DoTs (`#tfm 1`) and
  item procs (`#sub itv 1`) do not count. At most one count per 6 t (gametime), so a multi-hit burst counts once.
  Untargetable hits and true damage never reach the hook. Each count runs the kit's `hud/meter_hit` in the next module
  tick (`#fkM` = the count, as the body at the field core `api.CORE_FIELD_H` up): the newest pip flashes white for 4 t,
  the crack glint, the brass ping + a note rising with the count. The crack stages are 1 / 2 / 3 at 5 / 10 / 15
  (`rig crack/<n>`: the kit calls it when it drives the module's rig, `core.KIT_CRACKS`; until the real rig is merged the
  kit's crack goes to its own stub rig, so the core keeps its call; the core also cracks a stage the kit skipped, test 31).
- **Break** at 20: the next module tick runs `lib_clear` and cancels the pattern (waves included). The field state ends
  (meter, low gravity, the cut, cruise counters to 4) and the `break` clip plays with the caption "역장 붕괴": crack 4 and the
  gold burst at 5, a groan at 14. Then **groggy 200 t** (slumped hitbox, `look/groggy`, sparks every 20 t; hittable, no
  attacks, no tracking), recover 15 t (`flip` at 6), and back to cruise. Groggy has no damage bonus.
- **Hitbox** (click shield `cur.hit` + husk scale): cruise 2.4 × 4.6 / scale 2.4 (registry), field 2.8 × 5.2 / 2.6, groggy
  2.6 × 3.6 / 2.0.
- **Death**: the pattern is cancelled and the field ends; the `death` clip plays (flicker at 4 / 9, `look/off` at 12, the drop
  at 20, the sink at 40, the scale-out at 90) and the rig is killed at 106 (registry `death` 110). Mechanical sounds only
  (`deathSnd` false).
- **HUD** (spec S5): the name line gets `순항` (cruise) / `역장` (the warp and the pack-up) from the core, then the kit's
  `put_extra`: ` · 역장` + the badge while the meter is open, the low-gravity icon with low gravity, ` · 그로기` from the
  break to the end of the recovery (never doubled). The sub-line shows `순항` / `역장` / `패턴  <label>`; while the meter
  is open the core writes only the running pattern's label and ends with the kit's `put_sub`: `[badge E700] 역장  [20 pips
  E701 / E702 / E703 in groups of 5, gap E7F1]  [digits E720-E72A "n/20"]` + the first field's hint (font
  `rlk:mboss_fg`); during the break `[E704] 역장 붕괴`; then groggy / recovery. The lines are rebuilt on every state change
  and whenever the kit's `#fkHudV` changed (the module tick compares it with `#fgHudV`: the pip flash ends by the kit's
  schedule). The under-bar is the meter (violet, n/20) while open, full during the break, the time left in groggy (green),
  recovery progress (green), pattern progress (Geo), or cruise progress toward the field (gold).
- **Pause** freezes everything. Low gravity lapses (the request stops) and comes back with the first module tick after the
  resume; the running pattern's `pause` runs. **Reload** re-derives the state from the module scores and rebuilds the rig:
  a break in progress becomes a fresh groggy, a groggy continues, a recovery ends, a field opening or warp becomes the
  field at the centre (then the opening waves), a pack-up becomes cruise, and any other field stage resumes at the centre.
- **Performance** (mcsim `S:mb3/dev/perf.py`, 6000 t, an orbiting player, rig excluded): about **269 commands/tick** on
  average (the butterfly with its kit about 242, the Guardian 193). By pattern: idle 148, C1 344, C2 178, C3 256, C4 286,
  C6 323, F1 267, F2 381, waves 280, field opening 157, pack-up 152. The peak is **1769** on an F1 eruption tick (four
  framework discs made at once); C6 / F2 throws reach about 1040.

## 11. Test commands and the test list

- Fight: `/function rlk:mboss/test/start {id:"fieldgen"}` (= `#mbForce mb 3`). `test/kill`, `test/abort`, `test/level` and
  `test/stop` work as for the other bosses. Dying in a test offers "[다시 하기]" for the tested boss.
- `/function rlk:mboss/test/pattern {id:N}`: 1-6 cruise patterns (instant cruise), 11-12 field patterns (instant field),
  20 the field opening, 21 the opening waves, 22 the closing waves → pack-up, 23 the pack-up only, 30 break now (the field
  first if needed), 31 meter +5 (at most 19), 40 groggy, 41 low gravity on / off, 42 the triple third wave on / off,
  99 idle. Anything else prints the help. `test/lock {id:N}`: 1-6, 11-12 (inside the field), 17 the field cycle only,
  0 off. A test cut re-derives the rig form, look and hitbox from the field stage (butterfly S3). A cut field opening
  finishes at once. A cut groggy keeps the cruise counters (S8).
- Offline (mcsim; rig calls logged, `face/*` emulated; `S:mb3/tests/fgsim.py` models attributes, Motion and the dash
  i-frames):
  - `test_fieldgen.py <wt>/roguelike` (section 11: the kit wiring of §15) covers the stub rig, the entrance, rotation and the field cycle over 9000 t (bands,
    no repeats, C4 far only, the body inside r 16.5), the field opening, the meter rules and HUD, the break / groggy /
    recover, the damage cut and element equality, low gravity and every cleanup path, the waves (timing, jump, no dash
    dodge, triple), **per-pattern cases** (hit ticks, coefficients, Geo, telegraph >= 10 t, groups, clamp), pause,
    reload ×5, locks and tests, the S1 / S2 / S3 / S8 regressions, death → boxes, and uninstall.
  - `test_e2e_fieldgen.py` covers the registry and the 10:10:10 roll (unmet first), then the whole framework path gate →
    arena → entrance → cruise → field → 20 hits → break → groggy → recover → kill → 2 item boxes, the test commands and
    uninstall.
  - `test_fwopts.py` covers §7.
- **The shared harness:** `S:mb3/tests/run_all.sh <worktree>/roguelike [tag]` runs the fieldgen suites, the butterfly suites
  (`S:mb3/tests/bf_base/`: the `S:mb2/tests` versions that match the base f2ab515 with the butterfly stub rig, because
  `S:mb2/tests` has since moved on to the real-rig integration of `wip/bf`; the butterfly kit's suite
  `bf_base/test_fx_engine.py` = `S:mb2/fxtests/test_fx_engine.pre_fix.py`, because `S:mb2/fxtests` moved on with the
  BFFIX perf-2 fix of the butterfly kit; `test_e2e_butterfly.py` from `S:mb3/tests`, which expects three rollable
  bosses). After a rebase onto a `wip/bf` with the real butterfly rig and the fixes, point the harness back at
  `S:mb2/tests` / `S:mb2/fxtests`. Once the field generator kit is merged it runs its suite `S:mb3/fxtests/test_fg_fx.py`.
  It also runs the framework / Guardian suites of `S:mb/int_tests/`, `gen_check.py` (§1: documented order, second run,
  reverse order, `G:` wiped and rebuilt both ways, the ownership probe; `RP=<pack>` adds both kits' RP builds twice;
  only the paths a generator writes are copied, the rest is hard-linked and checked unchanged), `ident.py` (§7) and the
  validators (check_refs, check_macro from the root, check_nbtpath, check_mboss_pack, lint_mc; compared with
  `S:mb3/tests/baseline/`, which holds the kit's accepted findings of `S:mb3/fxtests/baseline/*_kit.txt` too). It prints one line per step, writes outputs to `S:mb3/tests/out/<tag>_*`, and exits 1 on any
  failure.
- **When you change a hit tick, an area or a coefficient, update the per-pattern case in `test_fieldgen.py` §9 in the same
  commit.** A pattern author may move their cases into a `pat_<module>.py`, as the butterfly authors did.

## 12. Pattern checklist (stage 2)

Stubs are in place (core author): timelines, hit areas with >= 10 t telegraphs, coefficients, Geo, volley groups,
re-aim / resize / re-arm / no-dodge, body travel. Still to do by the pattern authors: the kit visuals (`fg_fx_api.md` §10
names the preset for every event), telegraph decals (`#hzQuiet 1` + kit decal), the kit's sound recipes and any real
props. Keep the hit ticks, or update the cases.

**C1 일점 상쇄 / 폭격** (`bomb`, mid / far×2): [stub: faces the player at 0; the route is locked at 0 (24.75 b = 45 t ×
0.55 b/t along the yaw, its end pulled back along the line inside r 16.5); a predictor marker glides 4 t ahead; 20 bombs at
12 + 9k/4 from ports ±1.2 b (each `hz/disc` r 1.3 made 4 t before the drop, tell 10, light KB, groups of 4; bomb displays
fall 6 t); the slam clip at 58 (`hz/disc` r 5, tell 17, y1 2.0, heavy KB, → 75), the gold column, end 100]
- [ ] `ports_glow`, `bomb_drop` / `bomb_fall` / `bomb_burst` + `tele_disc(1.3)`, `column_tell`, `plunge`, `slam` (kit §10)

**C2 내려찍기** (`slam`, melee×2 / mid): [stub: lockb + keep `rlk_mb_fg_p2a` at 0, glide 10 t onto it, the column, `hz/disc`
r 5 tell 17 at 17 (y1 2.0, heavy KB), end 45]
- [ ] `column_tell`, `plunge`, `slam`, the decal `tele_disc(5.0, 17)`

**C3 코어 / 레이저 빔** (`laser`, melee×2 / mid×2): [stub: two `hz/line` from r 2.8, length 3, width 0.5, tell 24, active 133,
y -0.5..2.0, light KB, one group, re-arm 10; `hz/aim` every tick ±5°/t (counter-rotating); width 1.0 at 27 and 0.5 at 150;
end 174]
- [ ] `pods_drop`, `laser_charge`, `aim_line`, `laser_fire` + beam props (`laser_core`, `laser_glow`), `tele_mline` lanes
      (re-aimed with the hazards), `laser_spot`, `laser_end`

**C4 바위 폭탄 / 미사일** (`missile`, far×3 only): [stub: 10 drill displays launched at 21 + 3i/2 (sides ±1.2, yaw 36i); each
rises to its apex (`tp ^ ^11 ^3`), locks the player's feet at +7 (`hz/disc` r 1.5, tell 13, its group = the display's
`mbS`), dives with one 12 t interpolated teleport, impact at +20; 2 groups (1-5, 6-10); end 70]
- [ ] `tip_flare`, `vent_shaft`, `missile_launch` + `K.prop('missile')`, `missile_trail`, `tele_disc(1.5)`, `missile_impact`

**C5 지면 충격 / 중력 폭발** (`burst`, melee×2 / mid): [stub: `hz/disc` r 12 at the body made at 3, tell 45 → blast 48, y1 0.5 (a
jump clears it), heavy KB, dash i-frames work; gold flash at 5, up-beam 29-40, column 41-44; end 110]
- [ ] `core_spark`, `core_lift`, `dark_disc` (r 3.5 → 12 by +33), `up_beam`, `rim_flare`, `column_down`, `blast`, `rocks`; clamp R
      inside the arena (open, §14)

**C6 파쇄 / 바위 날리기** (`rock`, mid×2 / far): [stub: dip 0, vent 12, tower 20, flame band 38; `api.rocks` bursts from 55 (8,
6 t apart), throws from 95 (5, 8 t apart); end 157]
- [ ] `dip`, `vent_flare`, `tower_up`, `flame_band`, `floor_burst` + `tele_disc(1.8, 10)`, `slab_rise`, `tele_line`, `slab_throw`
      + `K.prop('slab')`, `slab_trail`, `slab_impact`, `revert`

**F1 감소 영역** (`fzone`, field, every band): [stub: activation 22, events at 22 + (0, 18, 30, 56, 78, 94, 124, 148, 168): each one
group of 1-4 `hz/disc` r 2.8, tell 15 (the first 2-3 b from the player, the others 2-8 b, random yaw, inside the walk disc);
gold eruption at the strike; end 216]
- [ ] `erupt_tell` + `tele_disc(2.8, 15)`, `erupt`, `debris`

**F2 파쇄 (field)** (`frock`, field, every band): [stub: violet activation 0-19, `api.rocks` bursts from 20, throws from 62; end
120]
- [ ] as C6 without the tower build-up

**「인력 충격파」 ×3** (`waves`, service 21): [stub: impacts 24 / 92 / 175 (gaps 68 / 83), charges 24 / 24 / 40; per front
`hz/ring` r 0..2.5 made at the charge start (tell = the charge), active 36, y1 0.7, `nododge 1`, `vis 211`; `grow` every
tick: r = 2.5 + 0.55k (r0 = r - 2.5) through `hz/resize_s`; the rim dust every 2 t; the third wave fires 3 fronts 9 t
apart below 50 % HP (or test 42); end 232]
- [ ] `wave_charge` / `wave_pulse`, `tele_wave`, `wave_band`, `wave_beam`, `wave_burst`, `wave_fire`, `wave_ring` (kit §4.1, §10)

**Core-owned, for the kit integration (not pattern work):** the entrance, the warp / unfold / banner, the meter protocol
(`hud/meter_open`, `meter_hit` per count, `meter_close`), the break / groggy / recover presets, death, pebbles, the
pack-up (kit §10 "Field", "Break", "Death").

## 13. Shared edits (outside `G:`)

All are in this commit and documented in README "고친 공용 파일":
- **Framework** (`tools/build_mboss_core.py` → `F:mboss/*.mcfunction`, `F:mboss/{hz,d}/…`): per-entity scores `mbHzND`,
  `mbHzRA`, `mbHzRT`; `#mbLowG`, `#mbHzClk`, `#mbNoDodge` in `init`; `#hzNoDodge` / `#hzRearm` in `opts_reset`; `hz/init`,
  `hz/tick`, `hz/hurt`, `grp_mark`, `hurt` (`hurt_nd`); new `hz/aim`, `hz/resize`, `hz/resize_s`, `hz/resize_line`,
  `hz/resize_rad`, `hz/rearm_at`, `lowg_on`, `lowg_add`, `lowg_off`, `lowg_rem`; `main` clears `#mbLowG` first; `hz/all`
  advances `#mbHzClk`; `player_reset` and `uninstall` remove low gravity; the `hz/<kind>` headers list the options. The
  generated dispatchers `F:mboss/d/*` and `register` gain the third boss (`#mbId 3`, `#mbN 4`, `#mbRoll 3`).
- **`tools/mboss_lib.py`**: `hz_opts(nododge=, rearm=)`, `hz_aim()`, `hz_resize(r, r0, w)`.
- **`F:tick.mcfunction`**: the two `#mbLowG` lines after `player/swing/tick`.
- **`F:view/move.mcfunction`**: the avatar jump reads the avatar's own `jump_strength`.
- **`tools/mboss_registry.json`**: the `fieldgen` entry (n 3, w 10, enabled).
- **Not changed**: every file under `F:mboss/{guardian,proto,butterfly}/` (byte-identical to f2ab515, `ident.py`), the
  butterfly kit and all Python of the other modules.

## 14. Deviations and open points (core)

- The rig is the stub until `wip/fg-rig` merges (§1). The core reads these manifest events (defaults as in §9): entrance
  clank / unfold / eye / rise / risen, warp_out out, warp_in_field unfold / banner, field_end lances / pack, break burst /
  wobble, recover flip, death drop / sink / out, and the pattern events. The manifest's `objectives` are removed by the
  module's `uninstall`. The kit's own stub rig uses other clip lengths (`fg_fx_api.md` §10 headings: entrance 130,
  bomb_run 97, missiles 73, wave 60, field_end 102). Once the real manifest exists, both sides follow it.
- The kit is wired (§15), but only the meter, the banner and the flags use it so far: the core's other visuals are still
  vanilla (`G:cfx/**`: entrance, warp, unfold, break, groggy, recovery, death, pebbles) and so are the stage-1 pattern
  stubs. The stage-2 specs (`spec/E_entrance.md`, `S1`-`S4`) map them to kit presets. Without the kit RP the glyphs show
  as missing characters.
- The entrance fight starts at intro 111 (the stub's `risen` 110), not at the plan's t94: the plan's figure counts from the
  clank. Change `ENT_RISEN` through the real manifest's `risen` event.
- Low gravity begins at the banner (opening clock 56), not at the unfold (35); the meter and the cut begin at the unfold.
- C5's disc R 12 is centred on the body and is not clamped to the arena (a body near r 16.5 puts part of the disc beyond
  the wall, which is harmless). C6 / F2 bursts can strike a standing player on every burst once the walker reaches them
  (heavy KB 4 normally pushes them out). F1 events always threaten a standing player (the first disc is 2-3 b off with r
  2.8). Both are by design but need a play test.
- Field patterns alternate F1 / F2 (a two-pattern bag with no immediate repeat), and the 400 t timer is checked at
  decisions only, so a field runs about 2-3 patterns.
- Not tested in game; mcsim only (it has no physics: knockback, gravity and jump arcs are modelled for the avatar /
  attribute values only).

## 15. Integration notes (for merging `wip/fg-fx` and `wip/fg-rig`)

**The kit (`wip/fg-fx`, merged into `wip/fg` and wired):**
- `core.clean()` spares the kit's owned paths (manifest `owned` + `K.OWNED_DIRS` / `K.OWNED_FILES`) and `G:rig/**`;
  `gen_check.py` 7b probes both directions.
- Hooks: `uninstall` → `fx/uninstall`; `cleanup` → `hud/banner_cut` (the banner only while it shows: within
  `BANNER_T` 80 t of `field/banner`, from `#fgBanG`), `fx/clear`, `fx/hud/clear`; `pause` → `fx/tele/clear`, and
  `fx/hud/flash_end` only while a title overlay is up (`vBig`); `death_start` → `fx/tele/clear`, `banner_cut`,
  `fx/hud/clear` (every flag); `test/cut` → `fx/tele/clear`, `banner_cut`; `intro/setup` → `fx/hud/clear` (no flag of an
  earlier fight; it also starts `#fkHudV`).
- Meter protocol: `field/open` → `hud/meter_open` (+ `hint_on` on the first field, `hud/hint_end` → `hint_off` 120 t
  later); `brk/count` → `#fkM = #fgBrk`, then as the body `positioned ~ ~<api.CORE_FIELD_H> ~ run fx/hud/meter_hit`;
  `brk/stage` keeps `#fgCrack` and calls the rig crack itself only when the kit drives another rig (its stub, now) or
  skipped the stage; `field/close` and `field/drop` → `hud/kit_off` (`meter_close`, `lowg_off`, `hint_off`, each only
  while its flag is on).
- `field/banner` → `hud/banner_field` (+ `#fgBanG` = gametime) and `hud/lowg_on`; the typed caption stays. `test/lowg`
  toggles the icon with low gravity.
- Groggy: `brk/begin` and `groggy/begin` → `hud/groggy_on` (once); `ai/enter` drops it (the recovery's end, cuts, reloads).
- Lines: `hud/extra` ends with `fx/hud/put_extra`, `hud/sub` with `fx/hud/put_sub` while the meter is open; `hud/refresh`
  stores `#fgHudV = #fkHudV` and the module tick redraws when they differ.
- Removed with the kit: the core's plain-text meter (`hud/meter`, `hud/pips*`, `hud/pipsf*`, `#fgPipT`, `hud/pip_tick`)
  and the vanilla fx it replaced (`cfx/count`, `cfx/crack`, `cfx/banner`). `api.GLYPH` / `api.FONT` now come from the kit.
- Not yet (stage 2, `spec/`): the remaining core visuals in `G:cfx/**` and the patterns' kit visuals and decals.

**The rig (`wip/fg-rig`, still to merge):**
- Merge it, delete `tools/mboss_fieldgen/stub_rig.py` + `stub_rig_manifest.json`, then rerun the generators in the §1
  order: the kit generator after the rig merge, so its `RIG()` points at `rig/` and its stub rig `G:fx/rig_stub/` goes;
  then `core.KIT_CRACKS` turns true and the core drops its own crack call for the stages the kit cracks. Check that the
  real rig's `crack/<n>` runs as the anchor (the body), as the stubs' do.
- `api.CORE_FIELD_H` then reads the manifest's `form_states.field.rest_anchors.core` (4.1 today).
- Re-run the per-pattern cases: the real manifest's clip events differ from the stub's (spec README §3).

## 16. Cruise patterns and sequences, stage 2 (the cruise-pattern author, branch `wip/fg-c`)

Files: `tools/mboss_fieldgen/cruise.py` (C1-C6, rewritten), the new `tools/mboss_fieldgen/seq_c.py` (E entrance and S4
death; writes `G:seq_c/**`), helpers `api.c_*` at the end of `api.py` (marked `[c_: cruise author]`), hook lines in
`core.py` marked `[seq_c: cruise author]`. Tests: `S:mb3/tests_cruise/pat_cruise.py` (77 checks, in that copy's
`run_all.sh` after `test_fieldgen.py`), renders `S:mb3/renders/cruise_{c1..c6,entrance,death}.png`
(`S:mb3/fxrender/render_cruise.py <WT> <RP> <OUT> [jobs]`: replays the patterns in fgsim and rebuilds the kit cards).

**Rules every cruise pattern keeps** (stub numbers below; every rig tick goes through `ev_or` / `clip_len` / `c_clip` /
`c_anchor`, so they move with the real manifest):
- Every damaging hazard is `quiet=1, sfx=0` and is paired, in the same tick and with the same tell, with a kit decal in
  the rock palette `el 5` (`tele_disc` / `tele_mline` / `tele/line`); every tell is >= 10 t; every hit is Geo with the
  §6 coefficients (C1 0.8 / 1.4, C2 1.4, C3 0.5, C4 0.9, C5 2.2, C6 1.3 / 1.1).
- Start lines that place things run `execute at @s` (the body may have been stepped by `ai/loco` / the leash earlier in
  the same module tick, so the function's own position is stale).
- Pause (FX-1): the pattern's `pause` sets `#fq<id>Pz 1`; the first `extra_tick` after the resume runs `p/<key>/resume`:
  `api.c_redraw` redraws the decal of every live quiet hazard of the pattern (`mbHzV` range) with the remaining tell
  `mbHzW - mbHzT - 1` (disc / ring / line from the hazard's own scores); C3 `relane` redraws both lanes at their current
  yaw with tell `max(1, fire - #fgPT)` and the rest of the active window as hold. A hazard that strikes on the resume tick
  itself gets no decal (there is no tick left to show it).
- Kept markers are killed at the pattern's end and in `cancel`, and before every re-keep (C1 `p1p/p1e/p1d`, C1's re-lock
  `p1f`, C2 `p2a`, C3 `p3e/p3g`, C4 `p4t<i>`, the C6 slab / tell tags). No pattern freezes the AI: C5's `g.release`
  (blast + 1) only hides the bar.
- Volley groups: `GRP_NEW` then `grp=True`; FW-4 holds (every member exists before the group's first strike; `c_rocks`
  asserts it for its last pair). C3's two beams are one group with `#hzRearm 10`.

**What the patterns do now:**
- **C1 일점 상쇄** (103 t = `bomb_run` 58 + `slam` 45; spec F2): route locked at 0 through the player's feet
  (24.75 b, end pulled back into r 16.5), `face/track` 0-9, the snap onto the route + `ports_glow` at 10, the glide from
  12 (45 t). A predictor marker glides the same route 4 t ahead; bomb k (12..54, `RUN + 9k/4`) gets `hz/disc` r 1.3,
  tell 10 at the predictor + the port offset (+1.05 / -1.05 / 0 b across the line), the kit bomb drops 6 t from the port
  height 3.8 at its drop tick: strikes 18..60, light KB, volley groups of 4 (at most 5 hits). Finisher (Q4) at 58:
  `lockb` + keep `p1f`, destination D = up to 6 b toward the lock in 0.5 b steps (then `clamp_body`), `hz/disc` r 5 at D
  with tell = the slam clip's impact (17: strike 75), feet up to 2.0 b, heavy KB, the decal, a 10 t glide onto D,
  `column_tell` (+3), `power_select` (+6), plunge 71, rise 82, end 103.
- **C2 slam** (45 t): `face/player`, `lockb` + keep `p2a` at 0, `hz/disc` r 5 tell 17 (y1 2.0, heavy KB) + decal at the
  lock, 10 t glide onto it, `column_tell` (3), `power_select` (8), plunge 13, strike 17, rise 24.
- **C3 lasers** (174 t): two `hz/line` beams from r 3.0, length 2.8, w 0.6 (feet -0.5..2.0 b, light KB, one group,
  `rearm 10`, act = off - fire = 133, tell = fire 24), made at 0 at the orbit's start yaws (eye -90 / gear +90 from the
  device's nose) with their kit lanes `tele_mline` (5.8 long, back -3.0: the band r 3.0-5.8 on the floor). From the
  orbit's start + 1 to its end - 1 (25..156) both are re-aimed every tick (`hz/aim` +5 / -5 deg/t from the frozen body
  yaw) and their lanes follow (`tele_mline_aim`); they meet at 42 / 78 / 114 / 150 (`C3_MEETS`, sparks). `hz/resize`
  w 1.0 at the fire for 3 t (the bloom), then 0.6. Off 157 (`laser_end`, `mline_end`, kill), piston at retract + 7.
  The pitch of the beam fx is `atan2(muzzle h, spot r - muzzle r)` = 41 deg from the `medal_e` anchor.
- **C4 missiles** (70 t, far only): 10 missiles (kit prop) at `C4_T` = launch + round(i (last - launch) / 9) =
  21..34, alternately from the left / right vent; each rises 7 t, arcs to its apex (16 b up, half way to the player,
  3 b off to the side away from its vent; `teleport_duration` 6), locks the player's feet at +14 (`lockp`, kept as
  `p4t<i>`, `hz/disc` r 1.5 tell 14, quiet, decal), turns onto the lock and dives 13 t: impacts at +28 = 49..62. Two
  groups (missiles 1-5, 6-10: at most 2 hits). End = max(clip length, last impact + 1).
- **C5 지면 충격** (110 t): at the rim event (3) `hz/disc` r 12 on the body (unclamped, Q12), tell = blast - rim = 45
  (strike 48), feet up to 0.5 b (a jump clears it), heavy KB, dash i-frames work; decal r 12. `dark_disc` grows
  3.5 -> 12 from lift + 2 to blast - 15, up-beam 29, rim flare at blast - 12, column 41 (floor hit +3), blast fx and
  sound in `vis` 51, `g.release` at blast + 1 (bar only), rocks hover / debris after, sink 81, crafter + chain at
  sink + 19.
- **C6 파쇄** (157 t): dip 0..11 (`bstep toward` 0.2 b/t while the player is >= 5 b away), vent 12, tower 20 (gear
  clicks +6 / +12), flame band 38 / 47 (charge 44), `face/track` until the revert 142. `api.c_rocks(g, tl, 'rock', 6,
  C6_BURSTS, C6_THROWS, 130, 110, el=5)`: 8 bursts (55 + 6k) on the arc walker at the player's distance (clamped
  2.5-18 b) turned by sigma x 90 (7 - k) / 7 deg (sigma random +-1 per run): the sweep crosses the device's front and ends
  on the player's feet; r 1.8, tell 10, y1 1.2, heavy KB; bursts 7-8 one group. A hidden kit slab per burst (scale 0)
  rises at burst + 2 (4-6 b, 12 t, tumbling). 5 throws (95 + 8j) from slabs 1-5: `lockp` + keep, a quiet dmg-0
  `hz/line` (w 2.4, runtime length = distance + 10) + the same `tele/line`, then a blade pj 1.5 b/t, life 24,
  `hr = c_blade_hr(1.45)` = 1.45 - `BLADE_PAD` (parsed from `build_mboss_core.py`, 0.65 today: it follows BFFIX).
  `pj_end`: `#pjEv 4` unless dodged counts `#fq6SH`; at the cap 2 every later tell / throw crumbles its slab instead.
  The unthrown slabs crumble at the revert.

**Sequences** (`seq_c.py`, visual / audio only):
- E (`seq_c/entrance/setup` from `intro/setup`; `seq_c/entrance/tick` from `intro_tick` on `#mbT`): setup = tuff dust +
  `respawn_anchor.ambient`; clank - 3 (13) beacon ambient; clank 16 `awake` + `awake_clank`, sparks +5 / +9; pods 24
  `unfold` (+8 piston); unfold 28 `crown_flare` (+8), gear clicks at unfold + 10 / 16 / 19 while before the eye; eye 54
  `eye_open` at the eye anchor (0, 3.0, -1.38) (the vault shutter is in the recipe; `vault.activate` comes with `awake_clank`); turn 60 grindstone; rise 80
  `rise` + `rise_hum` (again at +14); risen 110 `flash` + `beacon.activate`. The intro's name / done lines are the core's.
- S4 (`seq_c/death/start` from `death_start`; `seq_c/death/tick` from `death_tick`): `death_flicker` + `snd/death` at
  the core (4.5) at 0, flickers at 6 / 12 (beacon deactivate), drop 20 (dust at ^1.5, chain / copper fall), sink 40
  (anvil, chain), land 60 (`death_fall`), `death_fade` at 70 and 82 (+ sound at 82), the core's kill at 106.

**Core hook lines** (`[seq_c: cruise author]`): `import seq_c` + `seq_c.emit(g)` in `build()`; `intro/setup` calls
`seq_c/entrance/setup` (was `cfx/ent_setup`); `intro_tick`'s clank / unfold / rise / rise_dust lines -> one
`seq_c/entrance/tick` (name and done kept); `intro/name` drops `cfx/eye`; `death_start` -> `seq_c/death/start` (was
`cfx/death_start`); `death_tick`'s flicker / drop / sink / out lines -> `seq_c/death/tick` (the rig tick, `look/off`
at 12 and the kill at `DEATH_LEN` kept). The `cfx` dict entries `ent_setup, clank, unfold, eye, rise, rise_dust,
death_*` are **removed** (their files go with the rebuild); the core's `D_DROP / D_SINK / D_OUT` constants are left
(unused now).

**Helpers for the other author** (end of `api.py`, nothing above changed): `c_clip(clip, key, default)` (an extra
clip field of the manifest: `orbit`, `bursts`, `throws`), `c_anchor(clip, event, name, default)`, `c_bf(xyz)` (rig
`(x, y, z)` with -z forward -> `^x ^y ^-z`), `c_blade_pad()` / `c_blade_hr(reach)`, `c_redraw(g, key, lo, hi)`,
`c_rocks(...)` (the whole burst / slab / throw machinery with the cap; returns its tick / vis / crumble / cancel lines
and `done`). F2 could call `c_rocks` with pid 12 instead of its copy (§17); left to the integrator.

**Deviations from the specs / contract:**
- C1 is 103 t long (the slam clip after the run, spec F2), not the stage-1 100; the port height 3.8 b and the three
  ports (+1.05 / -1.05 / 0) come from the stub's body (the real rig's port anchors can replace them).
- C3: with the stub rig the beams are kit props (`laser_core` / `laser_glow`, 3.74 b, pitched) placed and re-aimed by
  the pattern (`api.STUB` only); the real rig's `laser` form draws its own.
- C4: the launch ticks are interpolated between the clip's launch and last events (the stub has no per-missile
  events); the end is max(clip, last impact + 1).
- C5: the rim cue is `block.trial_spawner.about_to_spawn_item 0.6 / 0.7` (FX-4: `respawn_anchor.set_spawn` reads as a
  respawn point being set).
- C6: `C6_END = max(clip length, last throw + 26)`: the real rig's `tower_throw` events (throws up to 132) need 158 t
  against its 155 t clip (the stub: 157 both). The dry run with the rig's HEAD manifest builds.
- S4: the fades are clamped to 70 / 82 (`min(out + 12, registry death - 28)`): a 28 t fade card must end before the
  110 t registry death; the stub's `out` is 90.
- Stub events the stub manifest lacks, with defaults: `coreup.eye` 1, `coreup.up` 16, `death.land` 60.
- Pause: the missiles' `teleport_duration` interpolation of a dive started before the pause runs on (a missile can
  look landed early); its hazard and the impact tick are unchanged. Hazards striking on the resume tick get no redraw.
- `test_fieldgen.py` (copy): the entrance sound list is the kit's (anvil.place, chain.place, piston.extend,
  crafter.craft, beacon.activate, respawn_anchor.ambient, vault.activate, grindstone.use); C4 tell 14
  (`C4_HIT - C4_LOCK`); pattern 6 throws up to the cap (<= 2 slab hits).

**Tests and measurements:**
- `pat_cruise.py` replaces fgsim's scheduler with the game's order (the tick counter advances before the due schedules
  run): with fgsim's own order the kit's self-scheduled ager starves and C1 reaches the 64-card cap (the FX-7 class, a
  harness artefact; peak 34 fx cards in the game's order). It records kit calls, hazard creations and `vis` calls and
  checks, per pattern: hit ticks, telegraph leads (decal tell = hazard tell, >= 10), areas, counts / caps, groups, KB /
  y ranges, the pause redraw, cleanup after `test/cut`, death and `test/abort`, plus E and S4.
- `RP=S:mb3/rp_c JOBS=4 tests_cruise/run_all.sh <wt_c/roguelike> c2` on the final tree: ALL GREEN (300 s). An earlier
  run (c1) had one unseeded `int_test_guardian` failure ("every normal pattern ran") that passed on rerun (Guardian
  files byte-identical, `ident` ok). Validators: refs 0 new, nbt 0, pack 0, lint 0,
  macro 0 new after re-saving the copy's `baseline/macro.txt` (+36 `function ... with storage` false positives: the
  redraws, the arc walker, the throw lines, the C3 relane; noted in `vcheck.py`).
- Load (`S:mb3/dev/perf_c.py`, the game's schedule order, 9000 t): average 337 cmd/t (the stage-1 figure 269 was with
  vanilla particles); per pattern average / peak C1 586 / 1917, C2 288 / 1909, C3 540 / 1682, C4 667 / 1499, C5 246 /
  1672, C6 547 / 2567 (the revert crumble at 142), idle 150.

**Rig merge:** nothing to change in `cruise.py` / `seq_c.py`; rerun `pat_cruise.py` (it reads every tick from the module
constants). Expect C3's orbit / anchors, C4's launch ticks, C6's bursts / throws and E / S4 ticks to move; drop the
stub-only C3 beam props by `api.STUB` turning false. Merging with `wip/fg-f`: both branches edit the same core hook
area and `README.md` (the module section); the cruise side removed its `cfx` entries, the field side left its own.

## 17. Field patterns and sequences, stage 2 (the field-pattern author, branch `wip/fg-f`)

Files: `tools/mboss_fieldgen/field.py` (W, F1, F2), the new `tools/mboss_fieldgen/seq_f.py` (S1 / S2 / S3 / the S5
notice; writes `G:seq_f/**`), helpers `api.f_clip_anchor` / `api.f_body_pos` at the end of `api.py`, hook lines in
`core.py` marked `[seq_f: field author]`. Tests: `S:mb3/tests_field/pat_field.py` (82 checks, in that copy's
`run_all.sh`), renders `S:mb3/renders/field_{waves,f1,f2,open,break}.png` (`S:mb3/frender/render_f.py`).

**What the patterns do now** (every rig tick through `ev_or` / `clip_len`, so the stub numbers below move with the
real manifest; every damaging hazard `quiet=1, sfx=0`, paired in the same tick with the same tell with a kit decal in
the field violet `el 9`; every hit stays Geo):
- **W 「인력 충격파」** (service 21): impacts `W_IMPACT` = wave impact + (0, 68, 151) = 24 / 92 / 175 (stub; the spec's
  25 / 93 / 176 belong to rig 0f7c0e8, the rig's HEAD 948f9a3 has impact 24 again). Fronts made at the charge start
  with tell = the clip's impact (`hz/ring` r0 0 r 2.5, act 36, y1 0.7, KB 3, `nododge=1`, tagged `rlk_mb_fg_p21f`),
  paired with `tele_wave(2.5, 21.2, 2.5, tell, 34)` (21.2 = 2.5 + 0.55 x 34: the decal and `p/wave_band` fronts equal
  the hazard front every tick; the kit's example used 21.0). The 3rd wave plays `wave_long` (opening) / `wave_drop`
  (closing) with the hazard at the clip start, tell = its `impact`, the beam from the clip's `impact` core anchor, the
  landing sounds at `land` and the field's only lift-off at `lift`; with the stub rig: `wave` at 151 and a 40 t charge.
  Identical variants (the stub) generate no `#fgWvK` guards. Triple (`#fq21T`, at the 3rd charge start): two more fronts
  **6 t apart** (Q2), made at strike - 10 (tell 10, `mkx`: new ring decal + a pulse). End: last strike + 37 or the clip
  end (212 / 224 stub, `W_ENDS`), `set_len` at the 3rd charge; `fin` kills the fronts (they linger 8 t after their 36 t
  active window by the framework default). The stub's `vis 211` and its dust rim (`draw`, `draw_m`) are gone.
- **F1 감소 영역**: decals at `F1_ACT + (0, 50, 80, 98, 119, 148, 159, 198, 209)` = 22 72 102 120 141 170 181 220 231
  (Q8), strikes + 15, end 260 (+ `play field_idle`). Placement / groups as the stub. Per disc: decal, `p/erupt_tell`,
  `p/erupt` at the strike, `p/debris` at the hazard's end event (strike + 9: the framework's linger 8); the event's
  first disc (tag `rlk_mb_fg_p11f`) carries `snd/erupt_tell` and `snd/erupt`; `snd/debris_land` 25 t after each strike
  that is still inside the pattern.
- **F2 파쇄 (field)**: clip `frock` (fallback `field_erupt`), bursts from `frock.burst` (25) every 6 t, throws from
  `frock.throw` (65) every 8 t, crumble at `frock.end` (100), end `clip_len('frock')` (fallback 110). C6's fixes in a
  module-local walker (`p/frock/burst<k>` + `place`): the arc at the player's distance (2.5-18 b) turned by sigma x
  90 (7 - k) / 7 deg; bursts 7-8 one volley group (`GRP_NEW` at burst 7, FW-4: burst 8 is made before burst 7 strikes);
  kit slabs (`prop/slab`, hidden at scale 0 until their burst + 2, rising 4-6 b over 12 t); throw tells = `lockp` +
  `keep(rlk_mb_fg_p12t<j>)` + a quiet dmg-0 `hz/line` (w 2.4, runtime length) + `tele/line` with the same args; blade pj
  1.5 b/t, life 24, `hr = SLAB_REACH 1.45 - BLADE_PAD 0.65` (Q16: change `BLADE_PAD` if BFFIX changes the blade);
  `pj_end` #pjEv 4 counts `#fq12SH`; at 2 the later tells / throws crumble their slab (Q7 cap).
  **Not shared with C6**: the spec suggests one helper in `cruise.py`; the cruise author works in parallel and owns that
  file, so F2 has its own copy in `field.py` (tags `rlk_mb_fg_p12*`, storage `fg.f2` / `fg.f2l`). Merge the two at
  integration if wanted (same parameters but pid, ticks, palette).
- **Every field pattern** tracks the player (`mv/turn {max:3}` in `extra_tick`) and has a `pause` hook that sets
  `#fq<id>P`; the next pattern tick redraws the kit decal of every live quiet hazard of the pattern with the remaining
  tell (`p/<key>/redraw` -> `rd*`: discs, the throw lines, the wave ring; an expanding front gets `p/wave_band` from its
  next radius with the remaining travel). This is the butterfly review's FX-1 for the field patterns (the core's pause
  hook clears the decals; the cruise patterns need their own).

**Sequences** (`seq_f.py`, visual / audio only; specs S1, S2, S3, S5):
- S1: `field_in(g, tl)` adds to the core's service-20 TL: halo flip 0, the warp-out pillar + `snd/warp_out` at
  `warp_out.hide` (stub default 12; spec F1) + `hud/flash_white` only with a player within 8 b, glitch at 14 / 19 / 24 /
  29 over the `rlk_mb_fg_fxw` marker (+ the sound at 16), warp-in / pillar at `WARP_LEN`, the unfold crackle at 39 / 43 /
  47, the medallion sparks at `WARP_LEN + warp_in_field.field` (51). `seq_f/unfold` (field/open) and `seq_f/banner`
  (field/banner: the first pebbles). `field/opened` sets `#fgCool seq_f.SETTLE` = **40** (Q10); the gold streaks at
  opening + 13 / + 28 (70 / 85) are keyed to `#fgCool` 28 / 13 in `seq_f/field/tick`.
- Field ambience (`seq_f/field/tick`, from `field/tick`): pebbles at the player's feet every 20 t of `#fgClk` while
  `#fgLowG` (**not while the waves run**: a pebble card lives up to 66 t and three fire bands need 48 cards; measured peak
  with the triple 55 of 64, no skipped call in the game's schedule order), `p/field_idle` at the core every 20 t
  (spec: 15; there is no `#fgK15`) outside the waves, `snd/field_hum` every 40 t, the first field's `hud/ab_lowg` when
  `#fgHintT` = `BANNER_T + FIN_BANNER - FIN_UNFOLD` (101: opening 136, when the banner's hold ends).
- S2: `field_out(g, tl)` on the service-22 TL: `rise_hum` at 0 (+ `lift_off` there while the rig has no `wave_drop`:
  one lift-off per field), lances (sparks at ±5.6 b, `snd/pack_up`), `horiz` chain, `pack` (`p/pack_up` + `core_flip`),
  `dock`: **`look/idle`** + `p/pack_up` + `snd/revert` (Q14), `packed` crafter. Stub defaults for the events the stub
  manifest lacks: horiz 40, dock 72, packed 76 (`field_end` 78 long). `field/close` calls `look/idle` only outside the
  pack-up (`#fgPat` != 22: tests, reloads).
- S3: `seq_f/brk/start` (bubble glow at the field core + `break_glow`), `brk/burst` (burst, floor ring, `pop_break`,
  `flash_gold`, `break_burst`), `brk/tick` (wobble groan at `wobble`, spark + chain at wobble + 10), `groggy/begin`
  (sink dust, beacon), `groggy/tick` (sparks at the slumped core every 40 t from 20, Q17; creaks at 40 / 120),
  `recover/begin` (recover glow + `snd/recover`), `recover/flip` (spark + `core_flip`). Heights from the manifest's
  `break` / `recover` clip anchors (defaults 4.1 / 3.5 / 2.5 / 3.3 / 4.2). **`hud/groggy_off` stays in `ai/enter`**
  (the flag runs to the end of the recovery, §15; spec S3 put it at recover 0).
- S5: nothing else changed: the meter protocol of §15 stands (pat_field checks counts during F1 / F2 / the waves and
  the 20th count cancelling a running wave).

**Core hook lines** (`[seq_f: field author]`): `import seq_f`; `field/warp` drops `cfx/warp_out`; `field/open` ->
`seq_f/unfold`; `field/banner` + `seq_f/banner`; `field/close` look guard; `field/opened` `#fgCool` SETTLE;
`field/tick` -> `seq_f/field/tick` (the old pebble modulo lines removed); `brk/begin` -> `seq_f/brk/start`;
`brk/tick` -> `seq_f/brk/tick` (was `cfx/groan`); `brk/burst` -> `seq_f/brk/burst`; `groggy/begin` ->
`seq_f/groggy/begin`; `groggy/tick` -> `seq_f/groggy/tick` (was the 20 t `cfx/groggy_spark`); `recover/begin` /
`recover/tick` -> `seq_f/recover/*`; `services()`: the field_in / field_out TLs keep only their mechanics (`tp`
facing, the glitch marker kill, `end`) plus `seq_f.field_in` / `field_out`, and `seq_f.emit(g)`. The core's vanilla
`cfx/{warp_out, warp_in, unfold_f, pebbles, break_start, break_burst, groan, groggy, groggy_spark, recover, flip}` are
still generated but no longer called (left for the integrator to drop with the cruise author's entrance / death ones).

**Deviations from the specs / contract:**
- The F2 / C6 helper duplication above; the waves' `vis` dropped; the triple gap 6 (Q2, accepted).
- Pebbles paused during the waves, `field_idle` every 20 t (not 15) and not during the waves (card room).
- F1 debris at strike + 9 (the hazard end event with the framework's default linger), not + 3.
- Spec W section 5 lists 32-36 for a player 20 b out; the front is active for k 0..35, so it is 32-35.
- `hud/groggy_off` at the recovery's end (the §15 rule) instead of recover 0.
- The C1 / C6 core numbers of §10-§12 are not touched here; §3 / §9 / §12's waves / F1 / F2 figures are superseded by
  this section (impacts, ends 212 / 224, F1 end 260, F2 110 with the frock ticks, the settle 40).

**Tests changed in `S:mb3/tests_field`** (the copy of `S:mb3/tests`): `test_fieldgen.py` §3 (the opening waves start
`SETTLE` t after the opening), §8 (triple 6 t apart), §9 (pattern 12: at most 2 slab hits, 2-5 throws; pattern 6
unchanged); `run_all.sh` runs `pat_field.py`; `baseline/{refs,macro}.txt` + `vcheck.py` notes: -1 / -2 findings of the
stub's wave rim, +14 macro false positives (`function ... with storage`: the F2 arc walker, the throw line, the pause
redraws) and +1 pre-existing ref (`room/deco/p`) that moved into check_refs' 40-line window.

**Rig merge:** nothing to change in `field.py` / `seq_f.py`; re-run `pat_field.py` (it reads every tick from the module
constants). Expect the waves' variants to diverge (`wave_long` 56 / `wave_drop` 84 in the rig's HEAD: the closing end
becomes 219), F2 to use `frock`, F1's `field_erupt` now chaining to `field_active` (the patterns play `field_idle` at
their end, as the rig note asks). Dry run: a scratch copy of this tree with the rig's HEAD manifest (948f9a3; the kit
regenerated for the real rig, only the stub `cruise.py`'s C6 length assertion disabled in the copy: it fails with the
real `tower_throw`) builds, and `pat_field.py` passes all 82 checks on it (wave_long / wave_drop variants, frock).

## 18. Integration of the cruise, field and rig branches (FGI2, branch `wip/fg`)

Merges, in this order, each with its own merge commit: `wip/fg-c` (e90b71d, §16), `wip/fg-f` (b10587e, §17),
`wip/fg-rig` (0f7c0e8 model + 948f9a3 clips; it carries the shared `mboss_rig_*` / `mboss_model_lib` / `mboss_paint_lib`
/ `mboss_screen_lib` libraries, the Guardian shims and the butterfly rig of `wip/bf-rig` d08202a, taken as they are), then
the integration commit.
- **Conflicts.** `api.py`: both END blocks kept (the cruise author's `c_*` first, then the field author's `f_*`).
  `core.py`: the `[seq_c]` and `[seq_f]` hook lines touch different hooks and merged textually. `README.md`: the module
  section rewritten for the merged state. Generated files: rebuilt, never hand-merged (after the field merge only the
  pause dispatcher `p/pause_d` differed: it now dispatches the cruise patterns' `pause` too).
- **Stub rig removed.** `tools/mboss_fieldgen/stub_rig.py`, `stub_rig_manifest.json` and `G:rig_stub/**` are gone, and so
  are the kit's `tools/mboss_fg_fx_stub_rig.py` and `G:fx/rig_stub/**` (fg_fx_api.md §9). `api.STUB` / `STUB_MANIFEST`
  are gone: `api.MANIFEST` is the real manifest (asserted), `RIG_DIR` = `rig`. The kit generator was rerun: `K.RIG()` =
  `rlk:mboss/fieldgen/rig/`; it asserts the manifest too.
- **Cracks.** `core.KIT_CRACKS = True` (asserted against `K.RIG()`): the kit's `hud/meter_hit` cracks the rig at 5 / 10 /
  15 as the body; `brk/stage` calls `u/crack_d` only for a stage the kit skipped (test 31's +5, reloads). The old
  unconditional core crack branch is gone.
- **Dead code dropped.** The core's vanilla `cfx/**` (no caller since `seq_c` / `seq_f`: `Core.cfx()` removed, its 11
  files deleted by the rebuild); C3's stub-only kit beam props (`rlk_mb_fg_p3b*`: the rig's `laser` clip draws the
  beams with `beam_l` / `beam_r`).
- **Rig integration notes (plan.md).** All already driven by the manifest in the authors' code; verified with the real
  manifest by the folded suites:
  - C3: start yaws and turn rates from `orbit` (eye az0 +90, sense -1; gear az0 -90, sense +1; rate 5; 22..155): the
    hazards turn E = Y - 90 + 5 (t - 22), G = Y + 90 - 5 (t - 22); meets 40 / 76 / 112 / 148; the spots r 5.58 (fx), the
    hit band r 3.0-5.8 (Q5). The stage-1 0 / 180 start is gone (since §16).
  - F1 plays `field_idle` at its end (260; `field_erupt` chains to the `field_active` loop until then); F2 plays it at the
    end of `frock` (110, the clip's own `next` too). The pack-up's `look/idle` is at `field_end.dock` 58 (seq_f), not at
    0 (`field/close` skips it while pattern 22 runs).
  - Waves: the 3rd wave plays `wave_long` in the opening (beam 39, impact 40: made at 135, impact 175, the clip ends 191)
    and `wave_drop` in the closing (drop 40, land 44, lift 63, risen 83: ends 219). Ends: opening 212, closing 219,
    triple 224.
- **F2 / `api.c_rocks` dedupe: not done.** The two copies differ in more than pid / ticks / palette: F2's pause redraw
  finds its hazards by the tags `rlk_mb_fg_p12z` / `p12y` (`c_rocks` redraws by `hz_vis` id through `c_redraw`), F2's
  throw line ends on the locked feet (`c_rocks`: 1 b past them), F2 counts every `#pjEv 4` toward the cap (`c_rocks`
  skips dodged hits), and `pat_field.py` checks F2's tags and storage (`fg.f2`, `fg.f2l`). Moving F2 onto `c_rocks`
  changes behaviour and its tests; left for a later pass with its own spec decision.
- **The butterfly in this branch.** `tools/mboss_butterfly_rig_manifest.json` (d08202a) now exists, so the butterfly
  generator of f2ab515 (unchanged here) builds against its real rig (`rig/`, its `rig_stub/` deleted). The butterfly's
  own fixes and its real-rig integration live on `wip/bf`; the f2ab515-era butterfly suites (`tests/bf_base`) pass on it.
  `tests/ident.py` now checks: the Guardian and proto outputs (and the Guardian rig manifest) byte-identical to
  f2ab515; the butterfly's sources identical to f2ab515 and its rig identical to d08202a; and, rebuilt in a scratch copy
  without its rig manifest, the butterfly reproduces f2ab515's `F:mboss/butterfly/**` byte for byte.
- **Real-rig clip numbers** (948f9a3; the module reads them, no event falls back to a default):

| clip | len | events the module reads | module ticks now |
|---|---|---|---|
| `entrance` | 110 | clank 16, pods 20, unfold 30, eye 60, turn 60, rise 64, risen 94 | fight at intro 95 (was 111) |
| `bomb_run` → `slam` | 57 + 37 | ports 10, run 12; slam: plunge 13, impact 17, rise 22 | C1: bombs 18-60, finisher 57, slam 74, end 94 (was 103) |
| `slam` | 37 | plunge 13, impact 17, rise 22 | C2: strike 17, end 37 (was 45) |
| `laser` | 165 | charge 4, aim 20, fire 22, off 155, `orbit` 22-155 | C3: tell 22, act 133, meets 40/76/112/148, end 165 (was 174) |
| `missiles` | 60 | flare 0, vent 8, launch 23, last 37 | C4: launches 23-37, impacts 51-65, end 66 (was 70) |
| `coreup` | 130 | rim 3, lift 5, up 15, beam 29, column 41, blast 48, sink 81 | C5: strike 48, end 130 (was 110) |
| `tower_throw` | 155 | dip 0, vent 12, tower 20, band 38, `bursts` 55-97, `throws` 100-132, revert 140 | C6: end 158 (was 157) |
| `warp_out` / `warp_in_field` | 34 / 40 | hide 12, out 13 / unfold 1, field 17, banner 22 | warp 13, unfold 35, banner 56 (unchanged) |
| `wave` / `wave_long` / `wave_drop` | 40 / 56 / 84 | impact 24 / 40 / 40, land 44, lift 63 | impacts 24 / 92 / 175, ends 212 / 219 / 224 |
| `field_erupt` → `field_active` | 22 | lock 12, erupt 22 | F1: decals 22..231, end 260 + `field_idle` |
| `frock` | 110 | flame 8, burst 25 (`bursts` 25-67), throw 65 (`throws` 65-97), end 100 | F2: end 110 + `field_idle` |
| `field_end` | 70 | lances 20, horiz 32, pack 40, dock 58, packed 70 | pack-up 70 (was 78), `look/idle` at 58 |
| `break` | 40 | burst 5, wobble 14 | groggy from 40 (was 34) |
| `recover` | 15 | flip 6 | unchanged |
| `death` | 110 | drop 20, sink 40, land 62, out 80 | fades 70 / 82, rig kill 110 (was 106) |

- **Tests folded** into `S:mb3/tests` (backups of the pre-merge files in `S:mb3/tests_bak_fgi2/`): `pat_cruise.py` and
  `pat_field.py` (in `run_all.sh` after `test_fieldgen`); `test_fieldgen.py` with the cruise author's §3 / §9 changes
  and the field author's §3 / §8 / §9 changes (the 파쇄 case now caps both C6 and F2 at 2 slab hits, 2-5 throws) and a
  real-rig §0 (the manifest, 28 clips with the rig API lengths, every rig call the module and the kit make exists in
  `rig/`, `K.RIG()` / `KIT_CRACKS`, no event defaulted); `baseline/{refs,macro}.txt` the union of both authors'
  (each one's removals kept), `baseline/lint.txt` + 2804 fixed-UUID `bad target` lines of the two rigs; `vcheck.py`
  and `run_all.sh` notes merged; `ident.py` rewritten (above); the kit's `S:mb3/fxtests/test_fg_fx.py` logs the real
  rig (backup `test_fg_fx.pre_rig.py`).
- **Results.** The documented generator order (core, arena, proto, the three rigs with `RP=S:mb3/rp_fg`, guardian, bf
  kit, butterfly, fg kit, fieldgen, check) twice: no file changes in the datapack, the tools and the resource pack; the
  Guardian outputs, rig manifest and RP assets byte-identical. `run_all.sh` (RP, JOBS 4): ALL GREEN, 29 steps
  (`pat_cruise` 77, `pat_field` 82, `test_fieldgen` 129, kit 1188 checks).
- **Renders.** `S:mb3/renders/integ_{c1,c3,c5,c6,w,f1,break}.png` (`S:mb3/fxrender/render_integ.py`): each scene runs in
  fgsim; the real rig is drawn from its debug poses (`--debug-dp`) with the module's look / crack calls, the kit's
  cards, decals and particles over it.
- **Open points.** ~~F1's "beams off" sounds play at 206 (spec F1) while the rig keeps the bright `field_active` links
  until `field_idle` at 260~~ (fixed in §19, FID-6). The rig's `prop/bomb` / `prop/missile` are
  unused (the kit's props fly). Load figures in §10 / §16 were measured with the stub rig (rig excluded).

## 19. Fix round (FGFIX, branch `wip/fg`; reviews `S:mb3/review/{state,fidelity}`)

Every real finding of the state and fidelity reviews is fixed in the generators, each with a regression check
(`S:mb3/tests`; the new checks fail on fde9db7).

| id | fix | where | check |
|---|---|---|---|
| FG-S1 | the reload hook sets `#fgBrkQ` again when the meter is open and full (`#fgBrk` 20) and keeps a pending count's `#fgBrkFx` while the meter is open | `core.py` `reload` | `test_fieldgen.py` §12a |
| FG-S2 | `field/open` returns into `field/reopen` (look, hitbox, lines) when the meter is open already; `field/banner` plays once per field (`#fgBanF` = the `#fgFN` it played for) | `core.py` | §12b (reloads at opening clock 50 / 54, test 21 inside an open field) |
| FG-S3 | framework: `mboss/world` with no tagged player runs `pause_tick` (the module's pause hook once, `#mbPause`), the resume line brings it back. Shared bug: the Guardian and the butterfly get it too; their own outputs stay byte-identical (`ident.py`) | `build_mboss_core.py` `world` | `test_fieldgen.py` §12c (F1 decals redrawn), `test_fwopts.py` (Guardian, butterfly, field generator) |
| FID-1 | the rig's new clip `break_low` (`fieldgen_clips.mjs`; same length and events as `break`, from `wave_drop`'s grounded pose); `brk/low` (read before `p/cancel`) sets `#fgBrkLo` while the closing `wave_drop` has the device low (`field.W3_LOW` = pattern clock 176..207: drop + 1 .. the middle of the rise); `brk/begin` plays `break_low` then; `seq_f` draws the bubble glow / burst / sink spark at `break_low`'s core anchors | rig, `core.py`, `field.py`, `seq_f.py` | §12d; the rig render `S:mb3/fgfix/out/c_break_low.png` |
| FID-2 | C1 bombs from the manifest's `bomb_run` `drop` anchors `port_0` / `port_7` (lateral ±1.048, forward 2.253, h 3.483; the centre bomb between): decal, drop point and `bomb_drop h` | `cruise.py` | `pat_cruise.py` C1 (the decal and the bomb's start vs the manifest ports) |
| FID-3 | kit `p/ports_glow`: only its dust (spread 1.6 b); the module adds a `glow` card on each of the 8 `bomb_run` `ports` anchors, 4 t (`cruise.C1_GLOW_LIFE`: 2 t and a 2 t fade, gone 2 t into the run glide, so the still cards never trail the moving ports; verification round) | `build_mboss_fg_fx.py`, `cruise.py` | `pat_cruise.py` C1 FID-3 (anchors; life and body travel) |
| FID-4 | `brk/count` → `brk/hit`: while `#fgPat` 21 / `#fgWvK` 2, `brk/hit_wd` positions `meter_hit` at the `wave_drop` core of the pattern clock (`field.WD_CORE`, 0.1 b bins), else at 4.1 | `core.py`, `api.f_anchor_at` / `f_core_h` | §12d |
| FID-5 | kit preset `p/column_base` (floor glow, base flare, a few end rods; no column card) at the C1 / C2 slam point; `column_tell` stays in the kit | `build_mboss_fg_fx.py`, `cruise.py` | `pat_cruise.py` C1 / C2 |
| FID-6 | F1 plays `field_idle` with its beams-off sounds at `F1_OFF` 206; the end (260) only ends | `field.py` | `pat_field.py` F1 |
| FID-7 | `field.w3_core(v, t)`: the closing triple's extra beams from the grounded core (1.3), the pulses (also the extra fronts' pulse, moved out of `mkx`) at the core of their tick, the closing charge sphere at the charge's mean core height (`mk40h385`, 3.85); every main beam on the rig's `beam` tick (impact − 1) at the core there | `field.py` | `pat_field.py` W FID-7 and the beam checks |
| FID-8 | `seq_c`: one `death_fade` with its sound at `out` (80): cards gone by 108 | `seq_c.py` | `pat_cruise.py` S4 |
| FID-9 | the pack-up sparks at `horiz` (32) on the `field_end` `horiz` anchors `medal_e` / `medal_g` (±5.6, 5.45 up); `lances` keeps its sound | `seq_f.py` | `pat_field.py` S2 |

- **New helpers** (`api.py` end): `f_anchor_at(clip, t, name, default)` (an anchor at any clip tick, linear between the
  manifest's event anchors) and `f_core_h(clip, t)`.
- **Balance** (plan.md "Fix round"): coefficients §6; bands C1 melee / mid / far ×2, C2 melee ×2 / mid, C3 mid ×2, C4
  far ×3, C5 mid, C6 melee / mid ×2 / far; `cruise.CRU_RECOVER` 12 for every cruise pattern. Sim `S:mb3/fgfix/sim`
  (`batch.py <label> fgbase|base`, `analyze.py <label>`; `S:mb3/fgfix/variant.py` builds a lean variant copy):
  stand 250.9 / melee walk 150.3 / ranged walk 116.1 HP per minute against the Guardian's 217.1 / 162.9 / 137.0
  (1.16× / 0.92× / 0.85×; before 335.2 / 43.9 / 81.2).
- **Rig**: 29 clips (`break_low` id 28, appended so no other clip id moved). The new clip reuses the parts' models: no model,
  texture or item definition was added (`node tools/build_mboss_fieldgen_rig.mjs --resourcepack S:mb3/rp_fg --no-paint`). `baseline/lint.txt`
  +39 fixed-UUID `bad target` lines of `rig/c/break_low/k/*`.
- **Tests**: `test_fieldgen.py` §0 (29 clips) and §12 (new), `test_fwopts.py` (the no-player pause, all three modules),
  `pat_cruise.py` / `pat_field.py` (the fixes above; coefficients from `api.DMG`); backups of the pre-fix files in
  `S:mb3/fgfix/tests_bak/`.
- **Results.** The documented generator order (core, arena, proto, the three rigs with `RP=S:mb3/rp_fg`, guardian, bf
  kit, butterfly, fg kit, fieldgen, check; `S:mb3/fgfix/rebuild.sh`) twice: no file changes in the worktree or the
  resource pack. `run_all.sh` (RP, JOBS 4): ALL GREEN, 29 steps (`test_fieldgen` 139, `pat_cruise` 78, `pat_field` 83,
  `test_fwopts` 26, kit 1185 checks; the Guardian, butterfly and framework suites, `ident.py` and `gen_check.py`
  unchanged and green).

## 20. Merge into the release line (wip/merge-fg, on claude/exciting-pascal-ek1vuy 5556c79)

`wip/fg` aa8cd73 merged into the release line (the butterfly final 78f8753, the 10-18 release 7a6dc4f, the 10-19 feedback
e016416 / a6611de, the stamp 5556c79), worktree `S:mb3/wt_merge`, one merge commit. The two sides share two merge bases
(f2ab515 and d08202a, through wip/bf-rig); the effective base is a282871 (= f2ab515 + d08202a).
- **Resolution.** Butterfly (code, clips, rig, kit, docs, `F:mboss/butterfly/**`): the release line's, whole (this branch's
  pre-final copy, built against the d08202a rig, is dropped). Field generator (`G:**`, its tools, rig, kit, manifests): this
  branch's. Shared framework: both sides' changes, every one kept. `tools/build_mboss_core.py` = this branch's options
  (`#hzNoDodge`, `hz/aim`, `hz/resize`, `#hzRearm`, `#mbLowG` + `lowg_*`, `hurt_nd`, the FG-S3 `world` pause) and the
  release's FW-1..4 (blade reach hr + 0.3, `#mbGrpL`, the test replay {id, ch} / `test/won_msg`), `#mbCritDmgAdd`,
  `#mbHealAmt` and the half-up heal factor; the only hand-merged lines are `init` and `player_reset` (both sides' scores).
  `tools/mboss_lib.py` merged cleanly (`hz_opts(nododge, rearm)`, `hz_aim`, `hz_resize` + `pj_speed_tenths`, `_tenths_up`).
  `items/hook/{on_heal,stat_buffs}`, `tick`, `view/move`, the registry (fieldgen n 3, w 10, enabled; 10:10:10) merged
  without conflict. Generated files: never hand-merged; regenerated.
- **One field generator change the merge required** (plan Q16): `field.BLADE_PAD` is now `api.c_blade_pad()` (read from
  the framework source, 0.3 with FW-1; it was the constant 0.65), so F2's slab half width is 1.2 (pj `hr:12`; `api.c_blade_hr` rounds to the
  framework's tenths, halves up, since MERGEV) and its reach is 1.5 b (the w 2.4 throw lane + the 0.3 pad; it was
  0.8 + 0.65 = 1.45 b), as C6's `c_rocks` already did through `c_blade_hr`. Generated: `p/frock/throw_go` and `p/rock/rk_go`
  (`hr:8` -> `hr:12`); every other `G:` file is byte-identical to aa8cd73. Doc lines: `core.py` / `api.c_blade_pad`
  docstrings, README (F2 line, merge note, `ident.py` line, `stat_buffs` "마지막 두 줄").
- **Build.** The documented order (core, arena, proto, the three rigs, guardian, bf kit, butterfly, fg kit, fieldgen, player
  rig, player audio, navia fx cards, check; `S:mb3/mergework/rebuild.sh`) twice into `S:rp_final9` (a copy of the shipped
  `S:rp_final8`): the second run changed nothing (datapack, tools, RP). `F:mboss/{guardian,proto,butterfly}/**`, the
  Guardian / butterfly manifests and sources are byte-identical to 5556c79; the RP is rp_final8 plus the field generator's
  rig, kit, font and 161 atlas entries (its fieldgen assets equal `S:mb3/rp_fg`'s).
- **Tests.** `S:mb2/tests/run_all.sh` and `S:mb3/tests/run_all.sh` (RP rp_final9, JOBS 4) ALL GREEN on the merged tree
  (tag `merge1`); the checks that pinned the pre-merge bases were updated, backups in `S:mb3/merge_bak/`: mb3 `ident.py`
  (base 5556c79: Guardian, proto and butterfly outputs and sources), `bf_base/` (the release suites), `bfsim.py`,
  `test_e2e_butterfly.py` (release test + three rollable bosses; the same file in mb2/tests), `test_e2e_fieldgen.py`
  (tlast {id, ch}: FW-3), `pat_field.py` (F2 slab `hr` from `FLD.SLAB_HR`), `run_all.sh` comments; the macro / lint
  baselines of both suites (each plus the merged tree's findings already accepted by the other; vcheck.py docstrings).
  `S:navia/test_speed_lock.py`: all passed (151). Seeded Guardian suite (`S:mb2/integ3/gseed`, seeds 1-3): the same output
  as the release tree except the ignored-command count (+6: the three new hazard objectives in `init`, run twice).
- **Balance after the merge** (`S:mb3/fgfix/sim`, `batch.py merge_fg fgbase`): stand 250.9 / melee walk 139.3 / ranged walk
  113.1 HP per minute (fix round vF: 250.9 / 150.3 / 116.1; Guardian 217.1 / 162.9 / 137.0: 1.16x / 0.86x / 0.83x, still
  inside the 20 % target). The walkers' small drop comes with the merged framework (FW-1..4: the three-row blade, the
  sub-step speeds, late volley members); not re-tuned.
- **Verification (MERGEV, scratchpad `mb3/mergev/`).** Per-file origin audit against 5556c79, aa8cd73 and both merge
  bases: no one-sided change lost (every release-only change kept; the fg-only changes not taken are this branch's
  pre-final butterfly outputs and the Q16 files); the 8 files changed on both sides are a clean 3-way merge plus
  union resolutions (`build_mboss_core.py`: 3 regions, `init` 1, `player_reset` 2, README 3). Rebuild in the documented
  order from a `git archive` of the merge and a copy of the shipped `rp_final8`: the datapack equals the commit and the
  RP equals `rp_final9` byte for byte; a second run changes nothing. Validators on both parents and the merge: no
  finding of the merged tree is absent from both parents. Probes (`probe_fw.py`, `probe_bf.py`, `probe_roll.py`):
  FG-S3 with the player entity gone (all three bosses), `#mbLowG` (on, dropped by a no-player pause, back on resume,
  never in the other fights), `#hzNoDodge` and `#mbGrpL` in Guardian / butterfly fights, the blade reach table
  (hr + 0.3), the butterfly cure meter with half-up heals and `#mbHealAmt`, the crit buff through `stat_buffs`, no
  heal / crit leak into a fieldgen fight, the registry roll (10:10:10, met / chapter / force passes). The one fix: the
  F2 / C6 slab comments and docs said hr 1.15 / reach 1.45 b while the pj launches hr 12 (1.2 b, reach 1.5 b);
  `c_blade_hr` now returns the launched tenths and the generated comments, README and this section say 1.2 / 1.5 b (no
  gameplay change: both `hr:12` launches are unchanged). Renders: `S:mb3/merge_renders/merge_{c6,f2,w}.png`.

## 21. Telegraph rule and the ×1.5 damage (10-20 user feedback; worktree `S:tele/wt_fg`, branch `wip/tele-fg` on 039b911)

User (verbatim): "역장 발생 장치의 계수를 많이 올려야될 것 같아. 그리고 이건 공통된 얘긴데 보스의 모든 공격에 바닥의 예고를
보여줄 필요는 없어. 영상에 없다면 그냥 보스의 동작을 보고 회피해야 하는 거니까 그대로 구현해줘."

- **Telegraph rule (10-20).** A ground telegraph (kit decal, outline, ground marker preset) only where the reference
  footage shows a marker on the floor before the hit; otherwise none, and the hit is read from the device's motion and
  sound. Audit per hazard with the frame times checked: `S:tele/fg/audit.md` (evidence `S:tele/fg/evidence/`).

  | hazard | decision | in game now |
  |---|---|---|
  | C1 bomb | remove | no decal; turn + pitch + whirl 0, port glows 10, the falling bomb (6 t), `bomb_burst` |
  | C1 finisher slam, C2 slam | trim | no r 5 decal, no 15 t floor glow; the rig column + `column_base` (now only the base flare) 12 t in |
  | C3 beams | remove | no lanes (`tele_mline*`, relane); aim lines 20, beams + `laser_spot` |
  | C4 missiles | remove | no decal; the diving missile with its trail, the dive whistle, `missile_impact` |
  | C5 blast | keep, trim | `tele/rim` r 12 palette 6 (pale gold) from 3 + `tele/dark` r 3.5 → 12 (7 → 33, to 48); `rim_flare` at r 12; no fill / progress edge |
  | C6 bursts, F2 bursts | remove | no decal; the walking chain + the positional resonate 10 t ahead |
  | C6 / F2 slab throws | remove | no dmg-0 line, no lane; the slab flares (`p/slab_glint`) + chain clink 10 t before the throw |
  | F1 zones | keep, trim | `tele/dark` at full size r 2.8 from its first tick (r0 = r, grow 1; tele int fix round F2: it grew r 0.8 → 2.8 over 6 t, the footage's discs are full size within 1-2 frames, v3 3.25 → 3.30, 10.70), to the strike; the dark dust `p/erupt_tell`; no violet `tele_disc` |
  | waves (and the triple) | remove | no charge disc / rings (`tele/wave`, `rd_tell`); charge sphere, pulses, hisses, beam, burst, the fire band |

- **Kit** (`build_mboss_fg_fx.py`): `tele/rim` (rim-only disc, 1 card) and `tele/dark` (the dark floor disc as a decal
  card: cleared on a pause, redrawn by the pattern), palette 6; presets `slab_glint` (new), `column_base` (base flare
  only), `erupt_tell` (dust only), `rim_flare` (scale 2 r through `p/e/rim_flare`), `dark_disc` removed (→ `tele/dark`).
  Size fix (needed by the rule: the kept markers are now the only ones): the `erupt_disc` / `ripple` sprites are 1 b
  across at scale 1, so the old `erupt_tell` (scale 2.8) drew r 1.4 for an r 2.8 zone, `dark_disc` (scale 12) and
  `rim_flare` (scale 12) r 6 for the r 12 blast; `tele/dark` and `rim_flare` now use scale 2 r. Demos updated (blast, erupt,
  waves); `fx/test/tele` shows the two new shapes. Not changed: `blast`'s white flash and ripple are still drawn at r / 2
  (an impact visual, not a telegraph; its crack ring is at r).
- **Module.** `cruise.py`: decals out of C1-C4 / C6, C5 rim + dark disc and its own `redraw` (rim with the ticks left; the
  dark disc at its size then, growing on to R by blast - 15), pause / resume only in C5. `field.py`: F1 `tele/dark` + its
  `rd` redraw; F2 without decal, dmg-0 line, `rd` / `rd_line` and pause; waves without `tele/wave` and `rd_tell` (the
  band redraw stays). `api.py`: `DMG` ×1.5; `c_rocks` without the burst decal and the throw line (`rk_tl` = the glint);
  `Gen.tele_rim` / `tele_dark`; the dead `rocks()` and the now unused `c_redraw` removed. Hazard sizes, timings,
  heights, groups and caps are unchanged; every hazard keeps `tell >= 10` from a clip pose / sound tell (C1 bomb 18,
  slams 17, C3 22, C4 51 / 14 per missile, C5 48, bursts 17, F1 15, waves >= 24, triple 10) and an impact visual at its
  strike (`pat_*` §0).
- **Damage ×1.5** (`api.DMG`, §6). Fairness sim `S:tele/fg/sim` (copy of `S:mb3/fgfix/sim`, same seeds, player model and
  harness; `rel` = the release 039b911, `after` = this branch): see the table below.

  | per minute: HP lost / deaths | Guardian | rel (039b911) | after, sim agent without lanes | after, agent reads the glint |
  |---|---|---|---|---|
  | stand | 217.1 / 1.33 | 250.9 / 1.67 (1.16×) | 376.0 / 2.33 (1.73×) | 376.0 / 2.33 (1.73×) |
  | melee walk | 162.9 / 1.00 | 139.3 / 0.78 (0.86×) | 312.9 / 1.89 (1.92×) | 211.8 / 1.33 (1.30×) |
  | ranged walk | 137.0 / 0.78 | 113.1 / 0.56 (0.83×) | 247.8 / 1.44 (1.81×) | 177.7 / 1.00 (1.30×) |

  The sim agent dodges from the hazard markers (the same entities with or without a decal), so removing the decals
  changes its play only where it read a decal-only hazard: the dmg-0 slab lanes of C6 / F2. Without them (strict run
  `after`) it cannot sidestep a throw and C6 goes from 9 to 40 hits (melee) / 11 to 40 (ranged). The `after_glint`
  run (`GLINT=1`) gives it what a player now sees instead: the slab that flares 10 t before its throw and the lock on
  the player; its hit rate is then the release's (6.11 / 5.56 hits per minute vs 6.11 / 5.44) and the rise is the
  ×1.5 alone (×1.52 / ×1.57). Logs and outputs: `S:tele/fg/sim/{rel,after,after_glint}.log`, `out/`.
  Past the old ±20 % target on purpose (the user asked for a large raise): about 1.3× the Guardian for walkers, 1.73×
  for a player who never dodges.
- **Tests** (copies in `S:tele/fg/harness/mb3/{tests,fxtests}`): `pat_cruise.py` / `pat_field.py` (§0 the keep-set and
  impact-visual checks, no-decal checks per hazard, C5 / F1 pause redraws, the others draw nothing after a pause, the F2
  sidestep reads the lock and the slab instead of the lane), `test_fieldgen.py` (coefficients ×1.5, no throw lines, the new
  helpers), `test_fg_fx.py` (`tele/rim`, `tele/dark`, `rim_flare` sizes; the budget plans without the removed decals; its
  mcsim path works from a harness copy), `run_all.sh` (the kit suite next to it), `ident.py` (reads the commits through
  the checked worktree: the old `mb3/wt_core` is gone), `baseline/macro.txt` + `vcheck.py` docstring (+6 findings of the
  accepted `function ... with storage ...` class: the new kit functions and the C5 / F1 redraws).

