# Moonlit Illusion Butterfly (달빛 환영 나비, title 달빛의 화신) module: core <-> pattern contract

Worktree branch `wip/bf` (the module core of `wip/bf-core` integrated with the fx kit of `wip/bf-fx`, then the human / wing patterns of `wip/bf-h` / `wip/bf-w`, §17; then
the real rig of `wip/bf-rig`, the model polish of `wip/bf-rig-polish` and the fx polish of `wip/bf-fxpolish`, the stub rig removed, §18). `DP` = `roguelike/`, `F:` = `DP/data/rlk/function/`, `B:` = `F:mboss/butterfly/`,
`S:` = the scratchpad. The framework contract (hooks, libraries, units) is `S:mboss/contract.md`, extended by §7 below.
Binding design: `S:mb2/plan.md`; research `S:mb2/understand/v1..v4.md`, `model.md`, `S:mb2/code/reuse.md`. This file
is the contract between the butterfly **core** and the two **pattern modules** (human, wing), so the pattern authors
work in parallel. It mirrors `S:mboss/gd_contract.md` (the Guardian).

---------------------------------------------------------------------------------------------------

## 1. Files, ownership, build

| file | owner | content |
|---|---|---|
| `tools/build_mboss_butterfly.py` | core | entry script (`python3 tools/build_mboss_butterfly.py`) |
| `tools/mboss_butterfly/__init__.py` | core | package doc, `PATTERN_MODULES = ('human', 'wing')` |
| `tools/mboss_butterfly/api.py` | core (stable) | `Pattern`, `Gen` writer helpers, `TL` timeline, `DMG`, `KB`, bands, colours, debuff / cure-meter numbers, the rig clip table read from the manifest (`ev`, `ev_or`, `clip_len`, `part_sel`; `rt` / `tell_rt` for the wind-up retime, §20) |
| `tools/mboss_butterfly/core.py` | core | 17 hooks, forms, AI + rotation, transformation (service pattern 20), groggy, 달빛 고치 / reward, 달빛 이슬, Burning weakness, entrance, death, HUD, tests, generated dispatchers |
| `tools/build_mboss_bf_fx.py` + `tools/mboss_bf_fx_paint.py` | fx kit | THE effect engine: cards, ground telegraph decals, sound recipes, presets, prop looks, HUD glyphs (`B:fx/{card,cardx,look,clear,uninstall}`, `B:fx/{e,p,tele,snd,hud,prop,test}/**`, RP `bf_kit/*`, font `rlk:mboss_bf`); API `S:mb2/bf_fx_api.md`; writes `tools/mboss_bf_fx_manifest.json` (`owned` lists its paths) |
| `tools/mboss_butterfly/human.py` | human-pattern author | `kick` (1 H1 달빛 발차기), `jump` (2 H2 달빛 점프), `dash` (3 H3 달빛 돌진), `vacuum` (4 H4 광폭한 진공) |
| `tools/mboss_butterfly/wing.py` | wing-pattern author | `strike` (11 B1 우아한 날개), `barrage` (12 B2 화염 날개의 습격), `sweep` (13 B3 날개 휩쓸개), `coco` (14 B4 달빛 축복), `release` (15 B5 달빛 해제, service) |
| `tools/mboss_butterfly/seq_h.py` / `seq_b.py` | human / wing author | the S1 / S3 / S4 visuals (`B:seq_h/**`) / the S2 / S5 / S6 visuals and helpers (`B:wx/**`) |
| `tools/build_mboss_butterfly_rig.mjs` + `butterfly_{paint,geometry,pose,clips}.mjs` (on the shared `mboss_rig_*` / `mboss_paint_lib` / `mboss_model_lib` / `mboss_screen_lib`) | rig | the real rig `B:rig/**`, RP `assets/rlk/{textures,models/item,items}/mboss/butterfly/*` + atlas entries, `tools/mboss_butterfly_rig_manifest.json` (the module's clip / event / anchor / prop table); API `tools/mboss_butterfly_rig_api.md` |

- The generator owns `B:**` **except** `B:rig/**` (the rig generator) and the fx kit's paths (`core.foreign()`: the
  kit manifest's `owned` list united with the kit's `OWNED_DIRS` / `OWNED_FILES`; the core's own `B:fx/death_*`,
  `B:fx/groggy` sit beside them). Stale files are deleted on every run, only in what it owns (a stale `B:rig_stub/**` of
  the old stand-in rig too); writing into a foreign path is an assertion error. Never hand-edit generated files.
- A pattern module writes **only** `B:p/<key>/**`, through `gen.pw(key, name, lines)` (or `TL.write`). It never edits
  `api.py`, `core.py`, the registry, the framework or the other module.
- **Generator order** (README "등록 · 모듈"; every generator writes and cleans only its own paths, so any order and a
  second run give the same bytes, checked by `S:mb2/tests/gen_check.py`):
  1. `python3 tools/build_mboss_core.py` (the framework, whenever the registry changes: `F:mboss/*.mcfunction`,
     `F:mboss/{d,hz,pj,pull,mv,aux,line,test,box}/`);
  2. `python3 tools/build_mboss_arena.py` (`F:mboss/arena/`);
  3. `python3 tools/build_mboss_proto.py` (`F:mboss/proto/`);
  4. the rig generators, with the resource pack: `node tools/build_mboss_guardian_rig.mjs --resourcepack <RP>`
     (`F:mboss/guardian/rig/`) and `node tools/build_mboss_butterfly_rig.mjs --resourcepack <RP>` (`B:rig/**` +
     `tools/mboss_butterfly_rig_manifest.json`, which step 7 reads);
  5. `python3 tools/build_mboss_guardian.py` (`F:mboss/guardian/` except `rig/`);
  6. `python3 tools/build_mboss_bf_fx.py --resourcepack <RP>` (the kit; `--skip-rp` for the datapack only);
  7. `python3 tools/build_mboss_butterfly.py` (`B:**` except `rig/` and the kit's paths);
  8. `python3 tools/check_mboss_pack.py`.
- **Rig.** Every rig call goes through `Gen.rig/play/look/prop` (`B:rig/…`); clips, events, fx anchors, parts, props
  and objectives come from `tools/mboss_butterfly_rig_manifest.json` (required: the stub rig and `api.STUB` are gone,
  §18). The build prints a note for every clip event it had to default (`ev_or`), so a renamed event in the manifest
  shows up at once (none with the merged rig).
- `core.build()` asserts: unique ids/keys, ids 1-4 human, 11-14 butterfly, 15 a butterfly service pattern, every
  declared pattern wrote `start`, `tick`, `cancel`; the intro and death lengths fit the registry `intro`/`death`.

## 2. A pattern module

```python
from .api import Pattern, TL, ev_or, clip_len, DMG, KB, CY, EL_PYRO, EL_DENDRO
PATTERNS = [Pattern(1, 'kick', '달빛 발차기', 'h', 'kick_combo', bands=('melee', 'mid'), weight={'melee': 2},
                    lead=2, recover=16, max_len=56, length=51),
            Pattern(12, 'barrage', '화염 날개의 습격', 'b', 'wing_barrage', bands=('mid', 'far'), el=EL_PYRO, ...)]
def emit(g):                      # g = api.Gen
    tl = TL(g, 'kick'); tl.at(-2, ...); tl.at(8, ...); tl.at(51, g.end())
    tl.write(['# start header'], ['# tick header'], t0=-2)     # writes start, tick, k/<t>, d/<a>_<b>
    g.pw('kick', 'cancel', [...])
    # optional: 'vis' (hz_vis events), 'pj_end' (projectile events), 'pause' (fight frozen), any helper you call
```

`Pattern(id, key, label, form, clip, kind='normal'|'service', bands=(...), el=7, lead=0, close=None, recover=20,
max_len=120, length=None, weight=None)`:
- `id`: 1-4 human (H1-H4), 11-14 butterfly (B1-B4), 15 B5 달빛 해제 (service; the core starts it), 20 the
  transformation (core). Stable numbers.
- `form`: `'h'` or `'b'`: the bag of that form; the core never runs a pattern in the other form.
- `clip`: **the core plays it at clock 0** (`B:p/clip_d`); a later clip of yours: `g.play(clip)` at its tick.
- `el`: 7 Dendro / 1 Pyro. For butterfly patterns the core switches the wing look to it 8 t before the start
  (`ai/prep`; 1 t swap with a colour flash), and moves her out to 6 b first for Pyro.
- `lead`: the start runs at clock `-lead` (0..20): tells that must begin before the clip's first motion (H1 hit 1
  at clip tick 8 needs its 10 t tell from -2: its hazards and, since the telegraph rule of 10-20, a body tell).
- `close`: human melee patterns burst-run (0.7 b/t, ≤ 12 t, clip `run_h`) to this distance first.
- `bands`, `weight`, `recover`, `max_len`, `length` as the Guardian (`gd_contract.md` §2). `length` = the real end for
  the pattern bar (`g.set_len(t)` if decided at runtime).

## 3. Entry points and the pattern clock

| function | called | executor / position | rule |
|---|---|---|---|
| `B:p/<key>/start` | once, on the tick the pattern begins (clock `-lead`) | `@s` = body, at the body (rotation = body yaw) | the core has already played the clip if `lead` is 0 |
| `B:p/<key>/tick` | every following fight tick | `@s` = body, at the body | `#bfPT mb` = -lead+1, …, 0 (clip played), 1, 2, … = **the clip tick** |
| `B:p/<key>/cancel` | the core aborts it (§4) | the caller — **use selectors, not `@s`** | remove everything you own; idempotent |
| `B:p/<key>/vis` | optional, `hz_vis` of your hazards | `@s` = hazard marker | `#hzEv mb` 0 create / 1 strike / 2 end; `@s mbHzV` = **pattern id × 10 + k** (k 1-9) |
| `B:p/<key>/pj_end` | optional, `pj_end` of your props | `@s` = prop | set `@s mbId <pattern id>` before `pj/launch`; `#pjEv`, `#pjKeep` per the framework |
| `B:p/<key>/pause` | optional, once when the fight freezes while it runs | `@s` = body | drop what would hang in the world (screen overlays); the clock continues after the resume |

- The rig ticks **after** the AI and the slot in the module tick, so a clip played in `start`/`tick` renders this tick.
- `TL(g, key)` (promoted from the Guardian's p12): `at(t, *lines)`, `span(t0, t1, *lines)`, `write(start_head,
  tick_head, t0=-lead)`; busy ticks become `p/<key>/k/<t>` (`k/m<n>` for negative t) behind a binary dispatch on
  `#bfPT`. `Gen.at/at_body/every` remain for one-liners (moduli `#bfK2 3 4 5 6 8 10 20 40`).
- Moving the body: `mv/*` as the body or `tp @s`. The body is the rig anchor and the hitbox; it stays on the floor
  (the butterfly's hover, climbs and dives are in the clips: toes +1.2 b hovering).

## 4. How a pattern ends, cancel rules

- **End:** `g.end()` (`B:p/end`) normally at clock = clip length; the core finishes the slot after that tick
  (`p/finish`: clears the slot, `rlk_mb_inv`, `#mbNoLeash`, the core markers `rlk_mb_bf_dest`/`rlk_mb_bf_lock` and
  every marker tagged `rlk_mb_bf_kept`, §7.5) and hands over: idle + `recover` (normal), `form/transform_done` (20),
  the groggy (15).
- `max_len` is a safety net only. `g.release()` only hides the pattern bar for a harmless tail: the slot stays busy
  until `p/end`, then the owner continues as usual (fix S2: it used to return early in `ai/pat_done` and freeze the AI).
- Optional `p/<key>/pause` (the fight froze) and `p/<key>/resume` (it runs again): the core's `pause` / `resume` hooks
  dispatch them. (Before the telegraph rule of 10-20 the resume hook redrew the kit decal of every quiet hazard still in
  its tell, `B:u/redraw` (fix FX-1), and B2's resume its landing decals; with no decals both are gone.) B3 keeps a
  pause / resume pair (tele int fix round F1, 10-20): its pause kills the red ember card of every live trail segment
  (`mbHzV 131`, still in its tell; an fx card ages by game time through the freeze) and its resume lays it again at
  full size with life = the ticks left + 1 (`p/sweep/ember`, macro args in storage `rlk:mboss bfr`).
- **Cancel** on tests (`test/pattern`), death, `/reload`. The caller runs `rlk:mboss/lib_clear` first where hazards
  must go (kills `rlk_mb_hz`, `rlk_mb_hzfx`, `rlk_mb_pj` props, pull points, stops `mv`). Your cancel removes the rest.
- Never deal true damage, never call `combat/apply`, never change `#bfSt`, `#bfForm` or other core state, never
  touch the player modifiers (`#mbHealPct`, `#mbCritAdd`), never apply or cure 달빛 고치 yourself.

## 5. State, scores, form, range info

All fake players live in objective `mb`. Core names `#bf*`; **pattern modules use `#bp<id><name>`** (e.g. `#bp12N`).
Scratch you may clobber inside one function: `#bfM` (modulo helper), framework scratch `#t #x #y #z`.

| score | meaning | access |
|---|---|---|
| `#bfPT` | pattern clock (clip tick; negative during the lead) | read |
| `#bfPat` / `#bfPick` | running slot pattern / the last pick | read |
| `#bfSt` | 0 idle 1 pattern 2 burst-run close-in 3 groggy 4 turn + chain re-form 5 wing look prep 7 dying | read |
| `#bfForm` | 1 human, 2 butterfly | read |
| `#bfLook` | current wing element look (7 dendro, 1 pyro) | read |
| `#bfBand` / `#bfDist` | band at the pick (1 melee ≤ 4 b, 2 mid, 3 far ≥ 8 b) / distance in tenths | read (fresh: `function rlk:mboss/mv/dist` → `#mbDist`) |
| `#bfHumN/#bfHumLim/#bfHumT/#bfHumTL`, `#bfBfN/#bfBfLim/#bfBfT` | form stretch counters and limits | read |
| `#bfCoc`, `#bfBuff` | the player has 달빛 고치 / 달빛 축복 받음 | read |
| `#mbLock` | test lock: 1-4 / 11-14 that pattern only, 16 form cycle only | read |
| `#mbNoLeash` | 1 during a scripted flight beyond the safe disc; the core resets it | write |

## 6. Damage and hazards

- Coefficients (`api.DMG`, % of the registry base hit `atk 12 × dmgMul 110`; the balance values of §20, the spec /
  stage-2 numbers were H1 100 / 120, H2 90 / 140, B1 130, B2 50, B3 160 + 30, B4 150, B5 260): H1 55 / 70, H2 45 / 70,
  H3 130, H4 120, B1 70, B2 35 per crescent (one hit per swing), B3 80 + trail 20 per touch (max 2), B4 100 per orb
  (one hit per orb), B5 130. Raw (before defence and level): 0.3 = 3, 0.5 = 6, 0.9 = 11, 1.0 = 13, 1.2 = 15, 1.3 = 17,
  1.4 = 18, 1.5 = 19, 1.6 = 21, 2.6 = 34. Knockback `api.KB`: default 3, light 2, heavy 4, none 0.
- Elements: hazards default to the registry `el` 7 (Dendro); Pyro hits set `#hzEl 1` / `#pjEl 1` (`g.hz_opts(el=1)`,
  `g.pj_opts(el=1)`). Every boss hit applies 1 U on the player (framework), so alternating Dendro and Pyro burns the
  player natively (plan: butterfly patterns are Dendro or Pyro per pattern).
- **Telegraph floor:** every damaging hit ≥ 10 t of readable telegraph (`tell` ≥ 10, or a telegraph-only decal ≥ 10 t
  ahead, §7.4). Create a hazard `tell` ticks before the clip's hit event.
- **Telegraph rule (10-20, binding; `S:tele/bf/audit.md`):** a ground telegraph only where the reference footage shows
  one, and her footage shows none. So: every hazard `#hzQuiet 1` + `#hzSfx 0` with NO kit decal (`g.tele_*`), no
  telegraph-only lane (§7.4), no floor marker before the hit; the 10 t floor is read from her motion and sound (clip
  pose / body fx + sound → strike), and the strike tick draws the attack's own impact visual. The one ground visual kept
  ahead of a hit: B3's flame-trail red ember line (TRIM). TF (달빛 고치): no hazard, nothing on the ground (KEEP). H1
  hit 1 adds a body tell at -2 (`snd/kick_whoosh`, foot glow / glint). Locked by `S:mb2/tests/tele_rule.py`.
- Areas anchored on the player stay inside the walkable arena: `g.lockp()` pulls the lock point inside the safe disc.
- Direct swings (no hazard): `function rlk:mboss/hurt` as the attacker with `#mbHitPct`, `#cmEl tmp`, `#mbKB`,
  `#mbKBDir`; one hit per swing is yours (or use a volley group, §7.3).
- The boss has **no element RES** (user decision): never read `#elem` to reduce damage; `mres` stays 0 (locked by
  `test_butterfly.py`).

## 7. Projectile and hazard helpers (framework additions in `tools/build_mboss_core.py` + `api.Gen`)

Python builders in `mboss_lib` (re-exported on `Gen`): `hz_opts(..., grp=False)`, `tell_line`, `pj_opts`, `pj_launch`,
`pj_steer`, `GRP_NEW`. Distances in blocks, speeds in blocks per tick.

### 7.1 Homing: `rlk:mboss/pj/steer {max}`
As a live prop, at it, **from the module tick** (it runs before `pj/all` moves the props): turn the flight direction
toward the player's chest (feet + 0.9 b, so the hit point 0.9 b under the prop meets the feet) by at most `max`
degrees in yaw (the short way round) and in pitch this call; pitch clamped to ±60°. Python `g.pj_steer(9)`.
B4 stub: `execute as @e[...orb...] at @s run function <p/coco/orb>` from `p/coco/tick`, steering 9°/t for 40 t.
Tested: 9°/call exactly, the short way round, the pitch clamp, a 0.5 b/t homing prop catches a player 37° off its
launch line that a straight one misses (`test_pjx.py`).

### 7.2 Blade hit shape: `#pjShape 1`
`g.pj_opts(shape=1)` before `pj/launch`: the hit test is a line across the flight direction, `hr` on **each side**
(`hr` = half width, ≤ 4 b). It **reaches hr + 0.3 off the line**, the same body pad as every other shape and as the
lane decal (fix FW-1; it reached hr + 0.65): 0.45 b spheres whose outer centres sit at ±(hr + 0.3 − 0.45), ≤ 0.6 b
apart, in three rows 0.9 / 0.3 b below and 0.3 b above the prop (feet from the floor to floor + 1.65 b, no height
gap, a jump does not dodge it); swept by the 0.25 b sub-steps. H4's vacuum blade (3 wide): `hr 1.5` (back from the hr
1.2 workaround). Shape 0 (default) = the old sphere. Speeds fly exactly ceil(spd / 0.25) sub-steps of 0.25 b
(0.7 and 0.75 → 0.75 b/t, 0.35 → 0.5 b/t; fix FW-2: an exact 0.75 / 1.75 / 2.75 used to fly one sub-step faster).

### 7.3 Volley groups (one hit per volley): `rlk:mboss/grp_new` + `#hzGrp` / `#pjGrp`
`g.GRP_NEW` makes a new id in `#mbGrp mb` (never 0); `g.hz_opts(grp=True)` / `g.pj_opts(grp=True)` put the next
hazard / prop into it (one-shot options, reset after each create). The **first landed hit** of a group (not dodged:
`#dodged tmp` 0) makes every other live hazard and prop of the group harmless (`mboss/grp_mark`: `mbHzHit`/`mbPjHit`
1; their visuals and flights go on). The group is remembered (`#mbGrpL`): a member made **after** the group landed its
hit starts harmless (`hz/init`, `pj/launch`; fix FW-4), so a burst created at a prop's life end cannot hit a second
time. A dash-dodged hit does not consume the group. Use it for B2 (one group per swing:
5 crescents), H1 hit 2 (crescent + ground wave), B1 (arc + slash band), B4 (an orb and its burst decal: copy the
orb's group with `scoreboard players operation #hzGrp mb = @s mbPjG`), B3's trail (two groups → at most 2 touches).

### 7.4 Telegraph-only hazards: `dmg 0`
`hz/*` with `dmg:0` (`g.tell_line(len, w, tell)`, or any shape with dmg 0) draws the outline and the progress, fires
the strike flash and the module visual events (`hz_vis` 0/1/2), and **never tests for a hit** (before: `dmg 0` still
dealt 1 and knocked back). H4 stub: the 30 × 3 b line locked at clock 7, its blade at 17.

### 7.5 Module helpers (`api.Gen`)
- `g.dest(max_b, keep_b)`: as the body, marker `rlk_mb_bf_dest` on the line to the player, at most `max_b` from her,
  `keep_b` short of the player, inside the safe disc (`B:u/dest`). `g.lockp()`: marker `rlk_mb_bf_lock` under the
  player, inside the safe disc. In butterfly form dest points also stay inside r 16.5 (`wx/u/okb`; fix S6). **Keep**
  either with `g.keep(<your tag>[, src])`: it kills an older marker of your tag first, re-tags the new one and adds
  `rlk_mb_bf_kept`, which `p/finish` and `p/cancel` kill (fix S1: kept markers piled up, one per run, and
  `@e[tag=<kept>,limit=1]` picked the OLDEST, so every later run aimed at the first run's spot). Markers a pattern
  summons itself should carry `rlk_mb_bf_kept` too (`wing.summon_m`, `h_lock_walk` do). Typical: `tl.at(t, g.dest(4, 1.5),
  g.keep('rlk_mb_bf_p1a'))` → `execute positioned as @e[...p1a...] run function rlk:mboss/mv/glide {t:5}`.
- **The fx kit** (`S:mb2/bf_fx_api.md`, THE effect engine; the stage-1 tinted engine `cards.py` / `B:tc/**` is gone).
  `api.K` is the kit module; `Gen` re-exports its call builders (each returns one function line, run in the executor
  context the kit documents: position = the event point, rotation = the aim; see its §1 and §9 "usage per pattern"):
  `g.fx(name, **args)` a preset `B:fx/p/<name>` (60, one per plan event: `kick_rise`, `ground_wave`, `vac_trail`,
  `fire_swing`, `flame_fan`, `orb_burst`, `rel_dome` {r}, …), `g.snd(name)` a vanilla sound recipe `B:fx/snd/<name>`,
  `g.kcard(kind, pos, rot, bb=, roll=, spin=, s0=, s1=, move=, life=, fade=, col=, dly=, dur=, hit=, col2=)` one card
  (painted kinds keep the video colours under white; neutral ones take `col` as an int, `'#RRGGBB'` or `(r, g, b)`),
  `g.tele_disc / tele_ring / tele_sector / tele_line(...)` the ground decals (visual only; unused by the butterfly's
  patterns since the telegraph rule of 10-20, §6), `g.kprop(name)` a prop look as `@s`
  (`vblade`, `fire`, `orb`, `orb_ring`, `dew`), `g.khud(name)` the HUD / screen functions. Caps 64 fx + 40 telegraph
  cards (counted apart); cards age by themselves (a self-scheduled function), carry `rlk_room` + `rlk_mb_aux` + `rlk_bk*`,
  and go with the fight (`cleanup` → `fx/clear`), on `pause` (decals) and `death_start` (decals). Prefer a preset to
  hand-made cards. Navia's gold `g.card(...)` still exists but the butterfly does not use it.
- **H4 prop height.** The kit's `vblade` look stands across the flight (the plane of the `#pjShape 1` hit line),
  4 b tall from its lower tip 0.9 b under the prop to 3.1 b over it, x −1.33..+1.33 of the hr 1.5 hit: launch the prop
  0.9 b above the floor (the stub's `^ ^0.9 ^1.0`), so its tip touches the floor where the lower hit row is
  (measured: `S:mb2/integ/vblade_check.py`, views `S:mb2/renders/integ_vblade.png`).
- Palettes: `api.LIME LIME_PALE LIME_CORE TEAL_DARK OPAL CYAN CYAN_DEEP` (Dendro/moonlight), `PYRO_GOLD PYRO_MAG
  PYRO_ORANGE` (Pyro #FAD77C → #C680A2), `GOLD GOLD_RING GOLD_EMBLEM` (the cure), `COC COC_SWIRL` (the debuff badge).
- `api.part_sel(name)`: selector of a named rig part (`rlk_mb_bf_<name>`, e.g. `foot_r`, `hand_r`, `core`,
  `fwing_l`) for fx anchors; `None` when the rig has no such part.

## 8. FX, sound, tags

- Every entity you create: `rlk_room`, `rlk_mb_aux` and a tag of yours starting **`rlk_mb_bf_p<id>`** (cancel kills
  by it). Decals shown through `vis` also carry `rlk_mb_hzfx`. Reserved core tags: `rlk_mb_bf_dest`, `rlk_mb_bf_lock`,
  `rlk_mb_bf_dew`, `rlk_mb_bf_dewn`, `rlk_mb_bf_fx`, `rlk_mb_bf_prop` (+ `rlk_mb_bf_prop_<kind>`, `_new`: the rig props), `rlk_mb_butterfly_part`
  and `rlk_mb_bf_<part>` (rig parts); the kit's `rlk_bk*` (cards, telegraphs) and fake players `#bk*`, storage
  `rlk:bfkit`.
- Screen effects: never world quads at the eyes (F5 seat camera). Particles `force @a[tag=player]` (helpers do it).
- Sounds: **vanilla only**: the kit's recipes `g.snd(name)` (composed from the audio tables of v1.md §6 … v4.md §6),
  or single layers `g.sound(event, vol, pitch)` (hostile, minVolume per layer).
- Looks: the core owns the wing element look (`look/dendro|pyro|flat`) and the form (`form/human|butterfly`); a
  pattern that needs a different look mid-pattern must restore it in `tick`/`cancel`.
- No voice lines (a creature). Captions only for mechanics, owned by the core: the debuff hint and "달빛 해제".

## 9. Rig clips (from the manifest; ticks at 20/s; events = clip ticks)

Since the wind-up tuning (§20) the ten damaging clips play through the rig's `RETIME`: the table gives the played
lengths and events (the authored length in brackets; the manifest carries `retime` and `authoredLen`).

The RIG API (`rlk:mboss/butterfly/rig/…`, `@s` = the anchor = the body, as/at it; the full contract is
`tools/mboss_butterfly_rig_api.md`): `init`, `spawn`, `spawn_hidden` (parts at scale 0, for the entrance), `tick` (every
game tick, after the AI), `kill`, `play/<clip>`, `look/{dendro,pyro,flat}`, `form/{human,butterfly}` (instant),
`face/player`, `face/track` (≤ 12°/call), `flash`, `tell/{on,off}`, `prop/clear`, `prop/{cocoon,pod,orb}` (at the
execution point and yaw; the cocoon's origin is its centre, 2.15 b up). `transform`, `release`, `revert` and `death`
switch the form at the right tick themselves (manifest `forms`). Clip anchors (`clips[].anchors[event]`: hoof, wing tip,
core, head, crescent points in rig coordinates) are read by `api.h_anchor` / `api.anchor`.

| clip | len | then | events (the rig manifest; aliases: kick_jump disc = orb, vacuum tell = glint, release xglint / cage = glint / rings) |
|---|---|---|---|
| `idle_h` | 40 | loop |  |
| `step_h` | 16 | loop |  |
| `run_h` | 8 | loop |  |
| `back_h` | 12 | idle_h |  |
| `turn_h` | 24 | idle_h |  |
| `kick_combo` | 43 (51) | idle_h | run 0, plant 5, **hit1 8**, backflip 9, land1 16, hop 19, hop2 22, leap 25, swirl 28, **hit2 32**, land 36 |
| `kick_jump` | 52 (65) | idle_h | tell 0, **sweep 10**, sweep_end 16, jump 22, orb 34, disc 34, kick 39, **impact 42**, land 46 |
| `dash_kick` | 46 (50) | idle_h | charge 0, dash 6, dash_end 8, **kick 11**, **ring 15** |
| `vacuum` | 37 (41) | idle_h | crouch 0, tell 5, glint 5, stomp 12, **blade 13**, backflip 13, land 34 |
| `groggy_h` | 40 | loop |  |
| `entrance` | 106 | idle_h | nameplate 57, glow 61, whiteout 71, burst 79, land 90, stand 106 |
| `transform` | 29 (30) | idle_b | glow 0, open 3, **sphere 5**, rings 8, spread 11 (form → butterfly at 3) |
| `idle_b` | 22 | loop |  |
| `glide_b` | 16 | loop |  |
| `wing_strike` | 51 (55) | idle_b | bank 0, dive 4, **hit 11** |
| `wing_barrage` | 95 (117) | idle_b | **swing1 4**, **swing2 24**, **swing3 52**, **swing4 72** |
| `flap_dive` | 52 (59) | idle_b | rise 0, dive 13, slam 19, **fan 21**, glide 26 |
| `coco` | 64 (76) | idle_b | wrap 3, **orb1 14**, ball 22, ball_open 30, **orb2 34** (the pod prop ball → ball_open) |
| `release` | 83 (96) | idle_h | fold 0, swoop 3, climb 7, whirl 14, cup 23, flash 26, glint 28, xglint 28, rings 28, cage 28, wrap 33, snap 39, **detonation 40**, hover 50, shrink 74, flat 74, shatter 78, revert 79, land 83 (form → human at 79) |
| `revert` | 43 | idle_h | shrink 30, flat 32, shatter 36, revert 37, land 43 (form → human at 37; not used by the core) |
| `death` | 100 | hold | stagger 0, **shatter 10**, **kneel 30**, **dissolve 50**, gone 100 (human from 0) |
| `chain_reform` | 18 | idle_h | stack 6 |

Arena: the barrier cap is only over the wall ring (y 208-215) and the light layer (y 206) is invisible, so wing tops
up to 10 b over the walkable disc never touch a visible block; displays render through barriers anyway.

## 10. What the core does (for orientation)

- **Entrance** (intro clock, clip tick + 1): cocoon prop over a glowing lime floor disc with wind streaks, the title
  on the sub-line at 58 (the video's nameplate 57), glow ramp at 62, whiteout 72, **burst 80** (prop cleared, white /
  cyan / mint crystal shards, two lime crescents, the kit's `cocoon_burst`), the drop with sparkles and leaves, landing
  at 91 (kit `land`: mint ripple, leaves, moss dust), she stands at 107, the fight at **108** (registry `intro` 140 is
  the cap). Kit fx on the way: `cocoon_disc` (spawn → burst), `motes` (1, 21, 41), `cocoon_glow` (62), `whiteout` +
  `hud/flash_white` (72). No damage, untargetable.
- **Human form**: grounded; idle locomotion = walk in beyond 7 b, back off at walking pace inside 2.2 b (`back_h`),
  short strafing steps 16 t of every 40 t; bag picks per band; melee patterns burst-run in (`close`).
- **Stretches**: first human stretch = 5 patterns or 600 t of fight, whichever first (checked at decisions only);
  then **transformation** (service 20, 29 t: cocoon glow, wings open 3-11, light sphere at 5 = **달빛 고치** + 3 **달빛
  이슬**, ripple rings r 3-5); butterfly form = 4-5 patterns or 900 t, then **달빛 해제** (service 15: caption at 0,
  the dome at 40, wings flat lime at 74, human again at 79: hitbox, heal orbs vanish); **groggy 300 t** (back turned,
  no tracking, no attacks; at +20, if still debuffed, the 달빛 이슬 the cure meter still needs: 1 or 2, §20); turn 24 t
  + chain re-form 18 t; then H2 first
  and 4 human patterns in all; transformation; …
- **Butterfly form**: hovering (rig), glides in beyond 8 b at 0.25 b/t, out inside 5 b at 0.2 b/t; the wing look
  switches 8 t before each pattern (Pyro patterns back off to 6 b during the switch).
- **Hitbox**: human 1.6 × 3.0 (registry, husk scale 1.4), butterfly 2.2 × 4.4 (husk scale 1.8): click shield,
  `cur.hit` (a re-created shield keeps it), husk scale; switched at the transformation end and at the revert.
- **달빛 고치** (player): 20 % of the CURRENT HP, non-lethal (≥ 1 damage, HP ≥ 1), no element, a number, the swirl,
  curse sound, typed hint "달빛 고치 — 체력 15% 회복하면 해제"; DMG on her ×50 % (`incoming`, reactions included), CRIT −100
  (`#mbCritAdd` → `items/hook/stat_buffs`; forced crits from engravings are undone in `incoming`: ×100/critDamage, shown
  as normal), healing received ×60 % (`#mbHealPct` → `mboss/player_heal` → `items/hook/on_heal`). The **cure meter**
  (§20; user "일정 체력 이상 회복해야 하게", it used to be any heal ≥ 1): every heal through `player/heal` adds its
  received amount (after the ×60 %, overheal included, even one Clorinde converts to Bond of Life) to `#bfCure`; at 15 %
  of max HP (`#bfCureT`) it is cured: gold beam → gold burst with a ring → gold emblem with sparkles (the kit's `p/cure`
  + `snd/cure_chime`, about 20 t) and **달빛 축복 받음**: CRIT +15 and CRIT DMG +50 (`#mbCritAdd` / `#mbCritDmgAdd` →
  `items/hook/stat_buffs`; user "피해 +50%가 아니라 치명타 피해 +50%야", it was DMG ×150 %) until the next 달빛 고치 or
  the fight's end. The meter restarts at each application. Cleared (meter included) on fight end, player death /
  revival, abort, run end, map change, wipe, uninstall; reload re-asserts it from the module state and keeps the meter.
- **달빛 이슬**: 3 glowing lime orbs (item_display, glow outline) 6-14 b from the arena centre, 120° apart; touching
  one (1.6 b) heals 13 % max HP rounded up (red herb applies) through `player/heal`: 7.8 % under the debuff, so two
  of them fill the 15 % meter.
- **Burning weakness**: in butterfly form any Pyro or Dendro hit of the player (not reaction damage) attaches both auras
  and starts / refreshes reaction 10 (burnDmg = 50 % of the player's reaction base, DoT every 10 t, "연소" text). Human
  form: normal reactions.
- **Death**: patterns cancelled, debuff/buff off, heal orbs gone, `death` clip; wings shatter (butterfly form) at 6,
  kneel at 24, rising moonlight motes and crystal shards from 40, the rig killed at 100 = registry `death`. No vocals.
- **HUD**: name line `Lv.N 달빛 환영 나비` + auras + `인간형`/`나비형` + `· 그로기`, then the kit's badges
  (`fx/hud/put_extra`: the 달빛 고치 glyph U+E600, maroon #8C525C disc with a salmon swirl, or the reward glyph U+E601);
  sub-line = form + wing look / `패턴  <label>` / groggy, then `fx/hud/put_sub` ("[badge] 달빛 고치 — 회복하면 해제
  [dew icon]" or "[badge] 달빛 축복 받음 (치명타 +15% · 피해 +50%)"). The badge flags follow `#bfCoc` / `#bfBuff`:
  `coc/apply_pl` → `hud/buff_off` + `hud/coc_on` (+ `hud/ab_coc`: the numbers on the actionbar), `coc/cure` →
  `hud/coc_off` + `hud/buff_on` (+ `ab_buff`, `pop_buff`), `coc/clear` → `hud/clear`, `coc/assert` (reload) rebuilds
  them from the scores. Hooks: `uninstall` → `fx/uninstall`, `cleanup` → `fx/clear` + `fx/hud/clear`, `pause` →
  `fx/tele/clear` + `fx/hud/flash_end` (the latter only while a title overlay is up, `vBig ≥ 1`, so a selection
  screen's own title is not wiped), `death_start` → `fx/tele/clear`. Under-bar = pattern progress (element colour), groggy / recovery (green), butterfly time left (Dendro),
  first human stretch time left (gold).
- **Performance** (mcsim `tests/dev/perf.py`, 4000 t orbiting player, rig excluded): ≈ 242 commands/tick average
  with the kit (its card ager `fx/e/age` ≈ 36 of them; 199 before the integration) vs the Guardian's 193; the busiest
  ticks (≈ 2.0-2.4 k commands) are B2 swings (5 framework hazards) and `u/dest` walks, plus the cure's 11 cards.

## 11. Test commands and the test list

- Fight: `/function rlk:mboss/test/start {id:"butterfly"}` (= `#mbForce mb 2`; node path: `/scoreboard players set
  #mbForce mb 2`, `/data modify storage rlk:room next set value [15]`, `/scoreboard players set #mapType room 1`,
  `/function rlk:run/next_map`). `test/kill`, `test/abort`, `test/level`, `test/stop`; dying in a test offers
  "[다시 하기]" for the tested boss (was hard-coded to proto).
- `/function rlk:mboss/test/pattern {id:N}`: 1-4 human patterns, 11-14 butterfly patterns (the form follows at once,
  no 달빛 고치), 15 / 30 달빛 해제, 20 transformation (with 달빛 고치 + 이슬), 21 달빛 고치 only, 22 a heal of 25 % of
  max HP through the real path (15 % received under the debuff: it cures), 23 3 달빛 이슬, 24 debuff/buff off, 40 groggy, 42 change form at the next decision, 91 a
  simulated Pyro hit (Burning weakness), 99 idle; anything else prints the help. `test/lock {id:N}`: 1-4, 11-14 (after
  a transformation), 16 form cycle only, 0 off.
- Offline (mcsim; rig calls logged, `face/*` emulated): `python3 S:mb2/tests/test_butterfly.py <wt>/roguelike`
  (the real rig's manifest and API files, entrance timing, rotation and forms over 7000 t, the timers, the wing look leads, 달빛 고치 / cure /
  reward / cleanup paths, 달빛 이슬, Burning weakness, equal damage for every element + mres 0, pause, reload ×3, locks,
  the hit tick + coefficient + element of every pattern, death → boxes), `test_e2e_butterfly.py` (registry and 50/50
  roll, test commands, the whole framework path gate → arena → entrance → fight → kill → item boxes, the dome avoided
  at 12 b and dodged by a dash, uninstall), `test_pjx.py` (§7 helpers), `S:mb2/fxtests/test_fx_engine.py` (the kit).
  test_butterfly also checks the kit wiring (hooks, badges, the entrance / transformation / switch / cure / death fx
  calls, the cards ageing out and staying under the caps).
- **The shared harness:** `S:mb2/tests/run_all.sh <worktree>/roguelike [tag]` runs every suite (butterfly, kit,
  framework / Guardian of `S:mb/int_tests/`, unchanged), the generator order check (`gen_check.py`: documented order,
  second rebuild, reverse order, `B:` wiped and rebuilt in both kit / module orders; `RP=<pack>` adds the kit's RP
  build twice) and the validators (check_refs, check_macro, check_nbtpath, check_mboss_pack, lint_mc; their findings
  are compared with the known baseline lists in `S:mb2/tests/baseline/`). One summary line per step, outputs in
  `S:mb2/tests/out/<tag>_*.txt`, exit 1 on any failure.
- **Per-pattern timing cases:** section 9 of test_butterfly.py runs `S:mb2/tests/pat_<module>.py` for every module of
  `PATTERN_MODULES` (`pat_human.py`, `pat_wing.py`; format and the recorded run in `pat_case.py`). Each pattern id
  a module declares needs a case (the suite fails otherwise). A case locks the hit ticks / coefficients / elements
  (`want`) and may check anything else on the pattern clock (`check(run)`: `run.hits`, `run.kit` (kit calls),
  `run.sounds`, `run.rig`). **When you change a hit tick or a coefficient, update your pat_<module>.py in the same
  commit**; the human author edits only `pat_human.py`, the wing author only `pat_wing.py`.

## 12. Pattern checklist (stage 2)

Stubs in place (core author): timelines, hit areas with ≥ 10 t telegraphs, coefficients, elements, body travel,
volley groups, homing. To do by the pattern authors (fx, telegraph decals, sounds; keep the hit ticks or update the
timing test):

**H1 달빛 발차기** (`kick`, melee/mid, lead 2) — [stub: sector r 4 / 75° at 8 (made at -2), glide 4 b in 5 t,
backflip away 10-19, sector r 5 / 90° + line 6 × 2 (one group) at 40 (made at 30), glide 5 t to the leap spot]
- [ ] rising flip-kick crescent (two layers: dark teal under bright lime, #EDF9DA → #297272), backflip trail, sideways hops
- [ ] axe-kick crescent + the ground wave strip that lingers 4-5 t; leaf shards; audio v1 §6 (kick 1, backflip, kick 2)

**H2 달빛 점프** (`jump`, melee/mid, close 3 b) — [stub: disc r 3 active 13-18, jump glide 33-55, disc r 2.5 locked at 40 → 50]
- [ ] arm-shard / chain glow tell 0-13, 360° low sweep streak, spiral ribbons on the jump, orb at her foot, star flash
- [ ] the Dendro disc / vortex kicked onto the locked spot, dust cloud; audio v1 §6

**H3 달빛 돌진** (`dash`, mid/far) — [stub: motes 1-9, dest 6 b, dash glide 10-12, disc r 3.5 at 15]
- [ ] mote charge, lunge streak, kick sphere + Dendro ring r 3.5, leafy burst; audio v2 §6

**H4 광폭한 진공** (`vacuum`, far/mid) — [stub: telegraph-only line 30 × 3 locked at 7, blade prop (pane) launched at 17,
blade shape hr 1.5, 0.75 b/t, life 60; backflip drift 18-38]
- [ ] spike + glint tell (kit `vac_crouch`, `vac_glint`, `vac_stomp`), the vertical crescent blade (`g.kprop('vblade')` on the prop, §7.5 "H4 prop height"), `vac_trail` every 2 t, rushing hiss (`snd/vacuum_pass`) as it passes

**B1 우아한 날개** (`strike`, Dendro) — [stub: sector r 4 / 80° + band 4 × 2 (back 2, one group) at 15, glide in 9-15, away 20-35]
- [ ] bank, dive, wing arc + ground slash band + trailing crescent; climb / flutter; audio v2 §6

**B2 화염 날개의 습격** (`barrage`, Pyro) — [stub: per swing 0/26/64/89 a lock under the player and 5 discs r 1, 1.1 b apart,
tells 14-18, one group per swing]
- [ ] 5 fire crescents fanning out then diving onto the lock (real props; `pj/steer` optional), splash + ground marker each

**B3 날개 휩쓸개** (`sweep`, Pyro) — [stub: fan sector r 4.5 / 90°, height 2.5, active 28-32 (made at 16), dive glide
22-26, trail discs r 1 at 37-49 (two groups: ≤ 2 touches)]
- [ ] two flaps + rise, head-first dive, slam, the flame fan (kit `flame_slam`, `flame_fan`), the flame trail visuals (`flame_trail`)

**B4 달빛 축복** (`coco`, Dendro) — [stub: orbs at 19 / 46: item_display 1.7 b, pj 0.5 b/t, homing 9°/t for 40 t, burst
decal r 2.8 at +50 (made at +40, same group as the orb)]
- [ ] wing-wrap charge, the lime sphere with gyroscope rings (a rig orb prop, or the kit's `g.kprop('orb')` + `g.kprop('orb_ring')`; `orb_charge`, `orb_launch`, `orb_burst`, `cocoon_ball`), cocoon ball 30,
      radial ground blades on the burst

**B5 달빛 해제** (`release`, service 15) — [stub: swoop glide 0-14 past the player, dome disc r 10 telegraphed 38 → 53,
heavy knockback]
- [ ] whirl with the lime 4-point star flare, cup, ground flash, cyan X glint, ring cage r 4 (E-15..-10), the pod,
      white flash and the lime dome r 10, tendrils, embers, the wing shatter; audio v4 §6. The core owns the caption,
      the flat look at 87, the revert at 92 and the groggy.

## 13. Deviations and open points (core)

- The core reads these manifest events (the defaults are the rig's ticks): entrance nameplate/glow/whiteout/burst/
  land, transform open/sphere/rings, release detonation/flat/revert, death shatter/kneel/dissolve (10/30/50), and the
  pattern events of §9. Manifest `objectives` are removed by the module's `uninstall` (it also runs `rig/kill` and
  `rig/prop/clear`); `props` lists the free props (`cocoon`, `pod`, `orb`).
- 달빛 고치 is 20 % of the **current** HP (plan; video 17 %, PDF 40 %); the cure is 15 % of max HP of received healing
  (the user's second decision, §20; first: any heal ≥ 1); the
  reward lasts until the next application or the fight's end (no timer). A death or a Ronova revival during the fight
  clears both (plan "cleared on death"); the next transformation applies it again.
- The heal hook runs first in `items/hook/on_heal` (before Clorinde's conversion), so a converted heal still fills
  the meter and is reduced first.
- The Burning weakness attaches 0.8 U of both auras and starts reaction 10 only if she is not burning; while burning,
  the hits refresh the auras (so the DoT goes on).
- The dome of B5 is a disc r 10 (plan: dodge farther than 10 b or by dashing at E), not `hz/full`.
- B2 crescents are hazards in the stub (no props); the plan's 0.6-0.75 b/t diving props are for the wing author.
  Done: real projectiles (§16 B2, kept at the merge; their long-range dive speed is open, §17).
- The `revert` clip is not used by the core (the release clip includes the revert at 92).

## 14. Integration notes (wip/bf: core + fx kit)

- The fx kit is the only effect engine. The core's stage-1 tinted engine is gone: `tools/mboss_butterfly/cards.py`,
  `tools/build_mboss_butterfly_fx.py`, `B:tc/**`, `Gen.tcard`, the scores `#bfTcN` / `#bfTcNow` / `#bfCureT`, the
  20-tick gold-card cure clock (`coc/cure_fx`, `coc/cure_at`), and the RP files `assets/rlk/{textures,models/item,items}/
  mboss/bf_fx/*` + their atlas entries (removed from the sandbox RP `S:mb2/rp_bf`; a release RP built from an older
  core still carries them: delete those three folders and the `rlk:mboss/bf_fx/*` atlas sources). Every core visual
  now calls the kit: entrance (`cocoon_disc`, `motes`, `cocoon_glow`, `whiteout` + `hud/flash_white`, `cocoon_burst`,
  `land` + recipes), transformation (`tf_sheath`, `tf_sphere`, `tf_ripples`, `transform_glow` / `transform_swell`,
  `flap_big` / `flap_small`), the wing switch (`pyro_switch` / `dendro_switch` + recipes), 달빛 고치 (`coc_apply`,
  `snd/debuff`, badges, `ab_coc`), the cure (`cure`, `cure_chime`, badges, `ab_buff`, `pop_buff`), 달빛 이슬 (`prop/dew`
  look on the orb, `dew_spawn`, `dew_pulse` every 20 t), groggy (`snd/groggy`, `motes` every 40 t), the chain
  re-form (`chain_reform` + recipe), death (`snd/death`, `wing_shatter` at the shatter event in butterfly form,
  `death_motes` every 15 t of the dissolve, `snd/death_motes`). Vanilla particles stay where they are cheap.
- Not used on purpose: `hud/pop_coc` at the application (the typed caption "달빛 고치 — 회복하면 해제" runs
  `rlk:mboss/line/say`, whose every step blanks the title line through `view/ttl_blank` and would cut the pop; the
  actionbar notice `ab_coc` carries the numbers), `hud/flash_maroon` / `flash_gold` (optional in the kit's table).
- The kit's `vblade` look was edge-on to the flight (rolled 90° about z: a crescent in the vertical plane through
  the flight line, 0 b wide seen from the player, its lower tip 0.22 b above the floor). It now stands across the
  flight with the lower tip on the floor (§7.5 "H4 prop height"); the core's projectile hit (rows 0.9 b under and 0.3 b
  over the prop, hr 1.5) is unchanged.

## 15. Human patterns H1-H4 and the sequences S1 / S3 / S4: stage-2 notes (human author, branch `wip/bf-h`)

Files: `tools/mboss_butterfly/human.py` (H1-H4), the new `tools/mboss_butterfly/seq_h.py` (writes `B:seq_h/**`: the S1 / S3 /
S4 visuals and sounds), the per-pattern cases `S:mb2/tests_h/pat_human.py`, the extra suite `S:mb2/tests_h/test_human.py`
(added to `tests_h/run_all.sh`) with its recorder `tests_h/hrec.py`, the renders `S:mb2/renders/human_{h1,h2,h3,h4,s1,s3_s4}.png`
(script `S:mb2/hrender/render_h.py`: each pattern / sequence run in mcsim, every kit card / decal call drawn with
`fxrender/render_fx.py` on the plaza floor, the stub rig's stand-in figure, the framework hit areas outlined in red on
the top views). §12's H1-H4 items are done.

**Shared additions.**
- `api.py`, END block "Human-pattern author" (every name prefixed so it cannot collide with the wing block's `WALK_R` /
  `anchor` / `lockw`): `H_WALK_R` 20.3, `h_anchor(clip, event, part, default)` (manifest `clips[].anchors`, rig x left /
  y up / −z forward → `'^x ^y ^z'`; `default` is a body-frame string, the spec's point, while the stub has no anchors),
  `Gen.h_lock_walk(tag)` (marker `tag` under the player pulled inside the walk disc r 20.3 in ≤ 3 steps of 0.25 b, plan
  Q8), `Gen.h_ring_dust(...)`, `Gen.h_anchor`.
- `core.py` lines marked "[seq_h: human author]" / "[human author]": `build()` → `seq_h.emit(g)` after `core.emit()`;
  `ai/state` first line → `p/vacuum/blades` while `#bp4B` ≥ 1 (H4's blades outlive the pattern, spec Q14); `intro/setup`
  → `seq_h/entrance/setup`, `intro_tick` keeps the rig tick, `intro/name` (sub-line only), `intro/burst` (`prop/clear`
  only), `intro/done` and calls `seq_h/entrance/tick` (`intro/hover|glow_snd|glow|white|fall|land` removed); `form/revert`
  → `seq_h/revert`; `groggy/begin` → `seq_h/groggy/begin`, `groggy/tick` → `seq_h/groggy/tick` (`fx/groggy` removed),
  `recover/begin|tick` → `seq_h/recover/begin|tick`; `death_start` → `seq_h/death/start`, `death_tick` keeps the rig tick
  / kill and calls `seq_h/death/tick` (`fx/death_shatter|motes|end` removed). The core keeps every mechanic.
- Scores `#bp1S` (H1 hop side), `#bp3D #bp3X #bp3Z` (H3 lane bucket), `#bp4L` (H4 lane length), `#bp4B` (live blades).
  Tags `rlk_mb_bf_p1a/p1b`, `p2a/p2b`, `p3a` (markers, killed at the pattern's start and end and in cancel; the stub
  leaked them: a second H3 aimed at the first one's D), `rlk_mb_bf_p4` + `p4b` / `p4n` / `p4g` / `p4s` (the blade).
- Every damaging hit is `hz/*` (`#hzQuiet 1`, `#hzSfx 0`) made in the same tick, context and tell as its kit decal (the
  long-fight check: 33 hazards, 33 decals, every tell ≥ 10). Cancel also runs `fx/tele/clear` (test/cut has no decal
  clear; only the running pattern has decals).

**Deviations from the specs (spec/H1..H4, S1, S3, S4) and why.**
- **H1.** Hit 1 is the Stage-2 strip: `hz_line` len 4.0 with `#hzBack` 0.5 (framework lines cover −back..len, so the
  spec's "4.5 long from 0.5 behind A" is len 4.0 + back 0.5) + splash r 1.5 at A + 1.2, aimed by A's own yaw (= toward
  the player at −2). The spec's dark teal underlay crescent cards (#297272 under #C1F788 / #D7F899) are not added: the
  kit's painted `cres_lime` carries the teal inner band and the leaf spikes, and a second tinted crescent turned the
  read dark in the renders; the same for the H2 sweep (#3A765D) and H3 ring (#2C898F) underlays. The foot swirl (no kit
  swirl kind) is a tinted `ripple` card. The lead-in whoosh and the hit layers use `snd/kick_impact` (+ the spec's
  singles at the other ticks).
- **H2.** Missing stub events fall back relative to `impact` (orb = impact − 10, kick = impact − 3, land = impact + 4,
  lock = impact − 12): the stub (impact 50) and the real rig (orb 45 / kick 52 / impact 55 / land 59, lock 43) both
  keep the 12 t disc telegraph. The jump destination stays on `u/dest` (r 18.5); only the disc lock uses the walk
  disc (`h_lock_walk`, a player at r 20.6 gets the disc at r 20.3). Recipes: `shard_tell`, `sweep`, `spiral_jump`,
  `disc_kick`, `disc_impact`, `land`; `disc_fall` is called at the kick (lands on the impact ± 1 t).
- **H3.** The kick and the ring hit as one group (Stage-2). The dash lane length is |SD| in 0.5 b buckets (1-7 b) from
  a squared-distance dispatch (the spec allows a fixed 7 b overshoot); it is a quiet dmg-0 `tell_line` paired with
  `tele/line` w 0.8, tell 7. The kick-1 burst at 15 is cards; the kit's `kick_burst` (its crescent ring) is drawn at the
  ring event 19.
- **H4.** **Blade half width 1.2, not 1.5**: the framework's blade samples are 0.65 b spheres, so hr 1.5 hits up to
  2.15 b off the line (0.8 b past the drawn blade) and breaks the spec's own check ("1.9 b off the line is untouched",
  "leave the 3.0 b lane: 1.8 b"); hr 1.2 reaches 1.85 b. The lane decal is `tele/line` w 3.0 from her feet to the wall:
  its length is found by a binary search over whole blocks (2-40) for the farthest point inside r 20.7, and its tell
  makes the fill's bright edge reach the far end when the blade does (the kit has no scrolling chevrons); it is paired
  with a quiet dmg-0 `tell_line` of the same size (the spec's `tell_line(30, 3, 8)` replaced). The aim is locked at
  the rig's `tell` event (9, the glint; the stub locked at 7). Rear-up and backflip step straight back along her locked
  yaw (not `mv/away`, which follows the player). The blade is summoned at scale 0.3 about its lower tip and grows to
  the kit's `vblade` look over 3 t from 18. The blade fx run from the core's `ai/state` (before the pattern tick), so
  the trail starts at 18 (spec "18+") every 2 t, debris every 4 t, the swoop at 19, the low rush at 23, `snd/
  vacuum_pass` once within 4 b of the player, the shatter at the wall / life end (event 1 / 2), a spark on a hit (event
  4, the blade flies on).
- **S1.** One kit `cocoon_disc` with life up to the burst instead of tinted cards refreshed every 20 t (the pale rim
  ripple is refreshed every 20 t). The rising shimmer (`snd/cocoon_glow`) moved to the whiteout − 2 (69, Q21), a soft
  `respawn_anchor.charge` at the glow (61): **test_butterfly.py section 1 now expects `snd/cocoon_glow` at whiteout − 2**
  (my copy `tests_h/test_butterfly.py`). The burst's `snd/cocoon_tail` at burst + 3, chimes at + 6 / + 9.
- **S3.** The chain re-form stays sequential after the 24 t turn (Q16's overlap is optional; the core's 42 t and the
  rig blend are unchanged). The release tail's fx at 87 / 91 / 96 are B5's (wing.py); `seq_h/revert` is only the shard
  drift at 92. The standalone `revert` clip (S3 D) has no caller in the rotation and is not wired.
- **S4.** Ticks follow the manifest events (shatter / kneel / dissolve): the knees-buckle cue at kneel − 10 (≥ shatter
  + 2), chimes at dissolve + 18 / 34 / 48, `snd/death_motes` at 90 (kit table), the last motes and a 0.8 / 2.0 chime at
  96. Human form: the crescent plates crack (navy shards at the hands) instead of the wing shatter.
- **Not applicable.** The butterfly body clamp r 16.5 (Q9): H1-H4, S1 and S3 run in human form, S4 does not move her.
- **Checks** (`pat_human.py` in test_butterfly section 9, `test_human.py`; `run_all.sh` green, also on a scratch build
  with `wt_rig`'s real manifest): exact hit lists; every hazard's shape / tell / group / KB / element / anchor and its
  decal twin; H1 sidestep 2.0 / 1.4 b, behind B; H2 jump 1.1 / 0.9 b, dash, walking out, the wall lock; H3 the dodged
  kick not consuming the group, the lane harmless, 10.5 / 12 b; H4 1.9 / 1.8 / 1.0 b off the line, a jump, 4 b (11 t of
  warning), the 0.75 b/t straight path, its 60 t life and shatter; pause (decals gone, clock frozen, both hits after the
  resume), boss death / cancel / abort mid-pattern (nothing left); a 3000 t fight (rule, caps ≤ 45 cards, no marker
  leak); the S1 / S3 / S4 kit calls and audio on their ticks in both forms.

## 16. Wing patterns B1-B5 and the sequences S2 / S5 / S6: stage-2 notes (wing author, branch `wip/bf-w`)

Files: `tools/mboss_butterfly/wing.py` (B1-B5), the new `tools/mboss_butterfly/seq_b.py` (writes `B:wx/**`: S2 / S5 / S6 fx
and the shared runtime helpers below), the per-pattern cases `S:mb2/tests/pat_wing.py` (incl. S2 / S5 / S6), the renders
`S:mb2/renders/wing_{b1,b2,b3,b4,b5,seq}.png` (script `S:mb2/wdev/wing_render.py`: the patterns run in mcsim, every kit
call / particle / prop is drawn with `fxrender/render_fx.py`, the stub rig's stand-in figure). §12's B1-B5 items are done.

**Shared additions.**
- `api.py`, END block "Wing-pattern author": `WX`, `WALK_R` 20.3, `BODY_R_B` 16.5, `REL_R` 16, `anchor(clip, event, part,
  default)` / `rest_anchor(form, part, default)` (the rig manifest's fx anchors, rig coordinates → body frame `^x ^y ^z`;
  the stub has none, so the defaults = the real rig's butterfly rest anchors `B_CORE`, `B_FWTIP_*`, `B_HWTIP_*`), the call
  builders `lockw()`, `clamp_walk()`, `clamp_body()`, `clamp_release()`, `bstep(kind, d)`.
- `B:wx/u/*` (seq_b): `lockw` (lock marker `rlk_mb_bf_lock` under the player pulled inside the walk disc r 20.3, plan Q8),
  `clamp_w|b|r` (a marker pulled inside r 20.3 / 16.5 / 16 in 0.5 b steps), `okb` + `toward|away|fwd {d}` (body steps
  only inside r 16.5), `btick` (every core tick in butterfly form: the body leash at r 16.5, 0.3 b/t back toward the
  axis, plan Q9 — it also covers the core's idle glide — and the S6 Pyro rim embers every 6 t).
- `core.py` hook lines (each marked "wing author"): the tick hook (`wx/cure/tick` while `#bpS5T` ≥ 1, before the heal
  event; `wx/u/btick` in butterfly form, before `ai/state`), `look/switch` → `wx/sw/fx` (the stage-1 24-dust + 8-flame
  burst removed, S6 "≤ 12 particles, ≤ 3 cards"), `transform()` → `seq_b.emit(g)` and `wx/tf/<t>` on the busy clock
  ticks (the core keeps look/dendro, face/player, `form/sphere` via `p/svc` and the end), `coc/apply_pl` → `wx/coc/fx`,
  `coc/cure` → `wx/cure/start`, `coc/clear` → `#bpS5T 0`. New scores: `#bpS5T` (S5 clock), `#bpCl` (clamp loops),
  `#bp15C` (B5 centre case).
- Every damaging hazard of B1 / B3 / B4 / B5 is `hz/*` with `#hzQuiet 1`, sfx 0 and its kit decal made in the same tick
  in the same context with the same tell (wing.py `hz_tele`). Patterns read every rig event by its Stage-2 name with the
  Stage-2 tick as default (`ev_or`), so the stub (`release` has no `glint`/`rings`/`shrink`, `coco` no `wrap`/`ball_open`,
  `flap_dive` no `fan`, old `wing_barrage` swings 0/26/64/89, `transform` rings 8) and the real rig (checked: the whole
  `pat_wing.py` passes on a scratch build with `wt_rig`'s manifest) both work.

**Deviations from the specs (spec/B1..B5, S2, S5, S6) and why.**
- **B1.** Shapes, group, tell 12, KB 3, lock L / H at 3 as specified. The spec table's "dive 8" is the rig's `dive` 12;
  the body glide to H still starts at hit − 7 = 8 (the spec's travel table) and the rig shows the 12-15 dive. H is clamped
  to r 16.5, so near the wall the swoop ends short of the player's side. Where a kit recipe covers a spec layer set it is
  used (`snd/wing_dive` at 8, `snd/wing_strike` at 15); the other spec layers stay single sounds. "slash" cards are the
  kit's `streak` (floor slashes lie flat along the lane), the wing arc is `cres_lime` (dark teal tint under white).
- **B2 (the main change, a task requirement).** The crescents are **real framework projectiles**, not the spec's ground
  hazards with timed visuals: crescent i of swing s is a `pj` prop (kit `prop/fire`) in the swing's volley group,
  launched at s+2+i with dmg 0; its path is a fixed timetable driven by the `mv` library (fan-out `mv/glide` 5 t from the
  wing-root point ^(2.4 sin θ) ^3.6 ^(2.4 cos θ) rising 35° at 0.6 b/t, then the curved dive `mv/leap {t:7, h:8}` onto
  its marker), so it lands exactly on s+14+i when its decal fills; on that tick the pattern sets `@s mbPjD 50` (a
  framework pj score written by the module) and the pj step (`#pjShape 0`, hr 1.2, pitch −90 so the 0.25 b sub-step only
  lifts it from 0.65 to 0.9 b over the marker) tests the sphere r 1.2 + 0.3 at the floor point = the splash; life 13 ends
  it the tick after (ev 4 → removed). Consequences: harmless in the air; the dive speed adapts to the distance (≈ 0.7 b/t
  at mid range, up to ≈ 1.5 b/t at 14 b; plan 0.6-0.75); a jump (feet ≥ 1 b) can clear the edge of a splash (a sphere,
  where a `hz/disc` would reach 3.5 b up). The markers are decal-only (`tele/disc` r 1.2 Pyro, no paired `hz`): the hit
  is the projectile's. `#pjWall 0` (the light layer y 206 is inside the fan-out apex height). With the old stub events
  (swing1 0) the pattern takes `lead` 5 so the wind-up keeps its 5 t; with the Stage-2 events (5/31/69/94) lead 0. The
  ember glow card at each landing is dropped (the spec's first cut under the card cap); scorch dust stays.
- **B3.** The dive glide runs from the rig's `dive` (22) to `slam` (26), 4 t (spec 20 → 26; plan "dive 4 t"); the side
  glide starts at `glide` − 1 (33) as the spec. The trail visuals sit on the hazards (her floor point), not under the
  wing tips as bf_fx_api §9 suggests, so what burns is what hurts; the segment decal is `tele/disc` r 1 Pyro (the kit has
  no ember-line decal) plus a dark red floor streak and ember dust; the flare is the hazard's `hz_vis` strike event
  (`#hzVis 131` → `p/sweep/vis`: kit `flame_trail` + tongues + crackle). Since the telegraph rule (10-20) the disc decal
  is gone and the red floor streak is the trail's only ground visual; it lives 11 t (tell + 1: up to the flare; tele
  int fix round F3, it was 18 t, 8 t past the flare; the footage's lines show ~6-8 t, v3 13.35-13.60). The +10 flare
  is a design addition: the footage shows nothing erupting along the lines (audit flag 5).
- **B4.** The orbs are the kit's `prop/orb` + two `prop/orb_ring` displays (the stub has no orb prop) that follow 0.25 b
  ahead along the flight (no one-tick lag) and spin. With the real rig manifest (`props` orb, pod) the build switches to
  the rig's `prop/orb` displays riding an invisible pj carrier and shows the rig's `prop/pod` during the ball (30-42) and
  the B5 wrap (44-52): generated and simulated, not yet seen in game. Orbs launch level toward the player (the 9°/t steer
  turns them to the chest). The burst hazard + decal are made in the module tick at age 40 (tell 10, the orb's `mbPjG`),
  the same tick pj_end (ev 2, keep 1) releases the orb; a popped orb (contact, dash, wall) leaves no burst. Early end
  once both orbs are gone after the clip (76). No radial blade marks on the burst decal (the kit has no `vmark`): the
  `orb_burst` preset draws the blades at the burst.
- **B5.** R and the 22 t dome telegraph from the cup as Stage-2; the decal is the kit's `tele/disc` r 10 (no separate big
  ring card), the safe line is 24 `end_rod` points at r 10.5 (41, 47). The screen flashes are the kit's `hud/flash_white`
  (E) and `flash_lime` (E+2) for the player wherever they stand (the spec's 14 b split is not possible with one title
  overlay). The core keeps the caption, the flat look, the revert and the groggy.
- **S2.** The fx follow S2 §3 per tick in `wx/tf/<t>`; the debuff fx (`wx/coc/fx`) adds the maroon / salmon dust spiral,
  the badge pop glow and the curse / resonate layers to the kit's `coc_apply` + `snd/debuff` (the core keeps the HUD /
  actionbar / caption lines). `pop_coc` stays unused (§14).
- **S5.** The kit's `cure` + `snd/cure_chime` at the cure tick, then 20 t of the spec's per-tick layers (the gold dust beam
  from 6.5 b, the gold particle rings 1.5 → 2.5 b, the sparkle rain, the chimes at 1 / 3 / 7 / 9 / 12 / 14) on `#bpS5T`;
  the star at the beam tip is the preset's descending glint (no extra card).
- **S6.** The kit's `pyro_switch` / `dendro_switch` (+ 1 gold glow card for Pyro, 2 pale tip glows for Dendro) within
  ≤ 3 cards and ≤ 12 particles; the persistent Pyro embers use the idle-b rest anchors, not the live pose.

**Checks** (`pat_wing.py`, run by test_butterfly section 9; `run_all.sh` green): the hit lists on the clip events, every
decal / hazard argument (tell ≥ 10, shapes, quiet, sfx 0, element, KB, groups), dodge geometry (B1 2.1 / 1.9 b off the
lane; B2 1.6 b off each row; B3 behind P; B5 10.5 / 9.9 b from R), caps (B2 one per swing incl. a dash-dodged landing,
B3 trail 2 of 4, B4 one per orb), projectile paths (B2 spawn / fan-out speed / landing on the marker 0.9 b up / armed
only on landing / ≤ 5 live; B4 0.25 b/t, ≤ 9°/t, pitch ≤ 60, stop at 40, decal + burst at 40 / 50, dash pops it), the
clamps (walk disc 20.3, body 16.5, release 16, the centre case), pause (frozen props, decals cleared, landings +20 t),
abort and boss death (nothing of B2 / B4 left), the S2 / S5 / S6 fx ticks.

## 17. Integration notes (wip/bf: the human and wing patterns)

`wip/bf-h` (47ceb5a, §15) and `wip/bf-w` (8cb5fd3, §16), both on b0d1697, merged into `wip/bf` in one merge commit.
- **Conflicts.** `api.py`: both END blocks kept (the human block, then the wing block; the human names carry `h_` / `H_`,
  so nothing collides). `core.py`: both authors' marked hook lines merged as they were (wing: the tick hook `wx/cure/tick`
  + `wx/u/btick`, `look/switch`, `transform()`, `coc/apply_pl|cure|clear`; human: `build()` → `seq_h.emit`, `ai/state` →
  `p/vacuum/blades`, intro, `form/revert`, groggy, recover, death); every generated core function equals one author's
  output (no function is changed by both). README butterfly section: the H lines from `wip/bf-h`, the B lines from
  `wip/bf-w`; the generator structure (`seq_h.py`, `seq_b.py`, the two api END blocks), the test list (`test_human.py`)
  and the status line updated, the human's `api.anchor` mention is now `api.h_anchor` (in the merged api `anchor` is the
  wing helper). Generated files were never hand-merged: `B:p/pj_end` (now 4 vacuum, 12 barrage, 14 coco) was rebuilt.
- **Build.** The §1 order (core, arena, proto, the Guardian rig and the kit with `--resourcepack S:mb2/rp_bf`, Guardian,
  butterfly, check_mboss_pack) run twice: no byte changed in the datapack or the RP; `gen_check.py` 1-6b pass.
- **Tests** (`S:mb2/tests`; the replaced files are in `tests/pre_merge/`): `pat_human.py`, `hrec.py`, `test_human.py` from
  `tests_h`, `pat_wing.py` from `tests_w`; `run_all.sh` = the wing author's self-locating `H=$(dirname "$(realpath "$0")")`
  + the human author's `test_human` step; `test_butterfly.py` section 1 expects `snd/cocoon_glow` at whiteout − 2 (Q21,
  `seq_h.SHIMMER_LEAD`). `tests_h/` and `tests_w/` are superseded (the human's dev helpers `tests_h/dev/hdump.py`,
  `hseq.py` stay there; they point at `tests_h`). `RP=S:mb2/rp_bf run_all.sh` on the merged tree: all 22 steps green.
  A scratch copy of the merged tree with `wip/bf-rig`'s committed manifest + `B:rig/**` (rebuilt: `rig_stub/` gone)
  passes test_butterfly (incl. both pattern-case files), test_human and test_e2e_butterfly.
- **Decisions.** H4's blade half width is **1.2** (§15; replaces the `hr 1.5` of §7.2, §7.5, §12 and §14: the drawn
  `vblade` still spans x ±1.33 b, the hit now reaches 1.85 b off the line, so a player 1.9 b off it is safe). B2 keeps
  the wing author's **real projectiles** (§16; replaces §13's stub hazards).
- **Open for review: B2's dive speed at long range.** Each crescent fans out for 5 t at 0.6 b/t, then dives onto its
  marker on a fixed 7 t `mv/leap`, so the dive speed follows the distance. Measured on the merged tree (mcsim, body and
  player still, `S:mb2/merge_hw/b2_speed.py`): mean dive speed 0.85 b/t at 6 b, 1.17 at 10 b, 1.64 at 14 b (one row:
  1.3-1.95), 2.17 at 18 b, 2.71 at 22 b (peaks 3.5 b/t), against the plan's 0.6-0.75 b/t; B2 is picked in the mid and
  far bands (far weight 2), so the far cases are common. Still harmless in the air and the decals (made at the swing, 14-18 t) are unchanged,
  but far away the crescents snap down. Options: start the dive earlier / make it longer for far markers (the landing
  tick stays), cap the speed and let a far landing come later (its decal tell must follow), or cap the marker distance.
- Still open from §15 / §16: nothing is seen in game yet; B4's rig-orb / pod path with the real manifest is generated
  and simulated only; the standalone `revert` clip has no caller.

## 18. Integration notes (wip/bf: the real rig, the model polish, the fx polish)

`wip/bf-rig` (100f096: the shared mid-boss rig libraries with the Guardian shims, the butterfly rig, 22 clips and the
clip-review fixes), `wip/bf-rig-polish` (ce3fcea: model geometry / paint only) and `wip/bf-fxpolish` (5b41287: kit sprites,
presets, sound recipes) merged into `wip/bf` (merge commits eab8c47, 0b0786e, a8c30f4), then the integration commit
b98f833 (stub removal, rebuild, module fixes, README).
- **Merges.** No textual conflict. The polish's manifest differs from `wip/bf-rig`'s only in `textures` / `atlas_px`: the
  merge was resolved by rebuilding the rig with the merged sources (`node tools/build_mboss_butterfly_rig.mjs
  --resourcepack S:mb2/rp_bf`): the rebuilt manifest equals the textual merge (72 sprites, 1.33 M px), the generated
  `B:rig/**` is unchanged, the RP butterfly sprites / models / items equal the polish sandbox's. The kit rebuild on the
  merged tree writes the fxpolish branch's datapack bytes and its sprites, models, items and font.
- **Stub removed** (§1): `tools/mboss_butterfly/stub_rig.py`, `stub_rig_manifest.json` and `B:rig_stub/**` (the first
  module build removed the stale folder); `api.STUB`, `STUB_MANIFEST` are gone, `RIG_DIR` is `rig`, the manifest is
  required. Docstrings of `api.py`, `core.py`, `human.py`, `wing.py`, `__init__.py`, `build_mboss_butterfly.py` updated.
- **Build.** The §1 order with both rig generators (`S:mb2/integ2/rebuild.sh <dp> <rp> <log>`): no `ev_or` fallback note
  (every event the core and the patterns read is in the manifest); run twice: no byte changed in the datapack, the
  manifests or the RP. **Guardian**: `F:mboss/guardian/**` (2358 files incl. `rig/`), `tools/mboss_guardian_rig_manifest.json`,
  its RP textures / models / items and the `mboss_gd` font are byte-identical to the pre-merge build (f2ab515); only
  `tools/mboss_guardian_rig_api.md` (a doc line about the shared libraries) and the `guardian_*.mjs` sources (now
  re-export shims / users of `mboss_rig_*`) changed. The RP atlas gained only the 72 `mboss/butterfly/*` entries (the
  rest equals the fxpolish sandbox's atlas).
- **Module changes for the real rig.**
  - `intro/setup`: `rig/spawn_hidden` instead of `spawn` (every part starts at scale 0; `spawn` showed her standing in
    the rest pose for the ≥ 3 t blend into `entrance`), `prop/cocoon` run `positioned ~ ~2.15 ~` (the real prop's
    origin is its centre; the stub added 2.1 itself).
  - Death events from the manifest are 10 / 30 / 50 (defaults updated to match), the nameplate tick is the manifest's
    `nameplate` (57). `seq_h`'s S4 cues follow them (kneel − 10 = 20 ≥ shatter + 2; chimes at dissolve + 18 / 34 / 48).
  - `kick_jump`: the human author's defaults already were the rig's (orb 45, kick 52, impact 55, land 59; disc lock 43):
    no change.
  - **B3 glide timing** (plan "Review-fix decisions", fidelity F6): the low side glide starts on the rig's `glide` event
    (33, 10 t to 43), the trail segments at glide + 1 + 2i (34 / 36 / 38 / 40, flares 44-50), the return at glide + 10
    (43). The head-first dive glide runs from the rig's `dive` (20) to `slam` (26): 6 t (the stub's 22 gave 4 t; the
    clip's dart dive is 20-25). `pat_wing.py`'s B3 `trail` follows the same formula.
  - **Pod prop** (rig API §6.1): the rig's closed shell `prop/pod` is summoned at the body-frame core anchor of the event
    (`coco` ball 30, `release` wrap 44; an older pod is killed first), is moved with her to that anchor every tick and
    is cleared at `coco` ball_open 42 / `release` snap 52 (B5 used to keep it until the detonation, B4 placed it at a
    fixed `^ ^3.0 ^`); B4's `cocoon_ball` glow and the ball-open ripple sit at the same anchor. Cancels kill it as before.
    The orbs ride the rig's `prop/orb` on an invisible pj carrier (§16, now the live path).
- **Tests** (`S:mb2/tests`; the replaced files are in `S:mb2/integ2/*.pre.py` / `lint_baseline.pre.txt`):
  `test_butterfly.py` section 0 = real-rig checks (the manifest is the module's, no stub file or `rig_stub/` left, the 22
  clips with plan.md's lengths, 30 parts, every rig function the module calls exists in `B:rig/`, props cocoon / pod /
  orb, the form switches, no `ev_or` fallback), section 1 expects `spawn_hidden`; `pat_wing.py`: the B3 trail formula and
  B4 / B5 pod checks (the logged `rig/prop/pod` call is emulated by a display, so the module's moves and kills act on it:
  summoned at ball / wrap, within 0.35 b of the anchor every tick, gone at ball_open / snap); `vcheck.py` / the lint
  baseline: +850 findings, every one `bad target '<uuid>'` in `mboss/butterfly/rig/` (the rig's fixed-UUID `tp` keys,
  the same false positive as the Guardian rig's 957). `RP=S:mb2/rp_bf run_all.sh`: all 22 steps green.
- **Docs.** `bf_fx_api.md` §3 (sprite wording), §6 (the recipe table printed from the generator: the polished layer
  stacks), §7 (the preset table printed from the generator, with a layers column), §9 (a note on the real events);
  README (rig, generation order, B3 / B4 / B5 / death ticks, shared rig libraries, status); this file §1, §8, §9 (the
  clip table is the manifest's), §11, §13.
- **Renders.** `S:mb2/renders/integ2_{h1,h2,b2,b4,b5}.png` (script `S:mb2/integ2/tools/render_integ2.py <dp> <rig debug dp>
  <rp> <out>`): each pattern run in mcsim as the suites do; per frame the real rig (spawn + the exact debug pose
  `bf_dbg/<clip>/<clip tick>` of the clip the core played, the wing look, the rig's pod / orb props where the pattern
  holds them) rendered with `S:mb/gw/tools/preview.py` from `rp_bf`, and the kit cards, decals, particles, B2 crescent
  props and the player ray-cast with `fxrender/render_fx.py`, depth-tested against the rig layer. The debug datapack
  `S:mb2/integ2/dbg` comes from the rig generator run on a copy of `tools/` (`--datapack <scratch> --no-paint --debug-dp`).
- **Open.** Nothing is seen in game yet. The rig's orb is a translucent glass sphere (shells of alpha 0.05-0.6): offline
  it reads faint against the marble beyond about 6 b (B4 frames); check in game, a kit glow inside it would be cheap.
  plan.md's other review-fix decisions (balance F1, B5 escape F3, keep-away F5, B2 dive speed F1, transform inside the
  body clamp F2, swoop cap F3, the B2 crescent orientation F4, the Pyro back-off F5, and the core review findings in
  `S:mb2/review/core_findings.json`) are not part of this integration (they are done in §19).

## 19. Review-fix round (wip/bf, after §18; plan.md "Review-fix decisions" and "Fix round")

Every confirmed finding of `S:mb2/review/core_findings.json` and `pattern_findings.json` is fixed in the generators,
each with a regression check named by its id (`S:mb2/tests/test_fixes.py`; FW-1/2/4 in `test_pjx.py`, perf-2 in
`S:mb2/fxtests/test_fx_engine.py`). What a pattern author has to know:

- **Markers (S1).** `g.keep` kills an older marker of the tag and tags `rlk_mb_bf_kept`; `p/finish` / `p/cancel` kill
  every `rlk_mb_bf_kept`. A marker that must outlive its pattern needs another tag (none does today).
- **Release (S2).** `g.release()` no longer freezes the AI: it hides the pattern bar only.
- **Framework (FW-1/2/4).** Blade reach hr + 0.3 (§7.2); `pj_launch` speeds fly ceil(spd / 0.25) sub-steps; a volley
  member made after its group's hit starts harmless (§7.3). The Guardian uses no blade and no group; its pj speed (5.0)
  gives the same macro bytes: its generated functions are byte-identical and its behaviour unchanged.
- **Test replays (FW-3, framework).** `test/start_ch` saves `rlk:mboss tlast {id, ch}`; `[다시 하기]` in `test/defeat_msg` and
  the new `test/won_msg` runs `test/start_ch` with both (it went through `test/start`, chapter 1). This was a framework
  bug for the Guardian too (a chapter-5 Guardian test replayed chapter 1); fixed for every mid-boss.
- **Uninstall (perf-4).** The framework removes `rlk:mboss tlast`, the butterfly `bfd` and `bfr`.
- **Kit ager phase (perf-2, kit).** `fx/e/make` counts the stages from game time + 1 (the 1 t schedule runs at the end of
  the same server tick): the main interpolation starts one tick after the summon (it used to merge in the summon tick,
  so cards never animated), the telegraph flash lands on the strike tick, every card lives exactly `life` ticks. The
  harnesses (`bfsim.run_sched`, `test_fx_engine.FxSim.tick`) now run the timer queue in the vanilla order (FX-7), and the
  suites count cap-refused card / telegraph calls (`s.skipped`, must be empty) instead of a peak that could not fail.
  The kit is butterfly-only: no Guardian output changes.
- **Pause / resume (FX-1).** The resume hook redraws the decal of every quiet hazard still in its tell (tell left =
  `mbHzW − mbHzT − 1`: the hook runs before this tick's `hz/all`) and dispatches `p/<key>/resume`; B2's redraws its
  landing markers (each holds its landing clock in `mbT`).
- **Card budget (FX-2).** Decorative cards give way from `#bkN 48` (the dew pulses, B2's flame tails); the 3 dew orbs pulse
  7 t apart; `fire_land` has 5 cards (was 7). 7000 t / 6000 t orbit fights: 0 refused calls.
- **Core.** S3 `#bfWing` (wings shown: butterfly form, or a transformation past `open`) decides the death shatter, and a
  test cut after `open` restores the human rig; S4 `#bfDew1` (the groggy orb is offered) brings the orb back on a
  /reload (verify round: the reload hook keeps what it resumes in its own `#bfRl`, since `dew/spawn1` draws its random
  angle into the scratch `#bfX` the hook used: a reload in the turn skipped `groggy/end`, and an angle of 2 started a
  second groggy); PL-2 the sphere clears the old orbs, so exactly 3; S6 butterfly idle glides, the Pyro back-off and dest
  points inside r 16.5; S7 test 42 sets `#bfBfN = #bfBfLim`; S8 the human stretch counters restart at `groggy/begin`;
  perf-3 `u/dest` measures the distance once; perf-5 every death card ends before the fight cleanup's `fx/clear`
  (motes 50 / 65, shards 53..89, the last glow at 92); PL-1 first person (no `rlk_av`): no camera-facing card at the
  player for 달빛 고치 / the cure, only the floor ring; FX-3 a cure clears the still-typing debuff hint (`line/clear`);
  FX-6 a hover flap (`snd/flap_small`) every 18 t in butterfly form while no pattern runs; FX-4 the doubled sound
  layers (a kit recipe and a single layer on the neighbouring tick) are gone.
- **Patterns.** F1 B2's dive time from the distance (§ plan "Fix round"), `B2_VMAX 0.7`, `B2_DMIN 7`, `B2_DMAX 60`, arc
  0.4 b, per-swing tags `p12t<k><i>` / `p12c<k><i>`, the end once every crescent has landed (verify round: swing 4
  also sets the pattern bar's end `#bfPLen` to the last landing + 1, so the bar no longer runs empty at 117 while far
  dives still fall); F4 the flame tail
  (`p/barrage/tail`); F2 the transformation glides inside r 16.5 in 4 t; F3 B5 swoop 9..13 t by |SR| and the approach
  (prep: beyond 8 b, 0.4 b/t, <= 10 t), R along the wall when the r 16 clamp would move it (fairness F3); F5 the
  Pyro back-off also with the look already Pyro (fairness F5: glide out only inside 3.5 b); F6 B3's glide on the
  rig's event (33: trail 34/36/38/40, return 43; with the clip review's note, already at §18); fairness F1 the
  coefficients (`api.DMG`, plan "Fix round").
- **Not fixed (judged not real by the verify pass):** fairness F2 (the player-side Burning is intended; counted in the
  balance), F4 (H2's locked disc, the spec's design; plan only asks for 10 t), FX-5 (the transformation's sound
  layers are what the binding specs ask for).
- **Balance tool.** `S:mb2/balance/bal.py <dp> <label>` (the reviewer's `fsim.py`, adapted: B2 landing clock from the
  marker, per-swing tags, the blade reach) prints the stand / melee walk / ranged walk table against the Guardian.
- **Guardian identity check.** `S:mb2/integ3/gseed/gseed.py <seed> <suite> <dp>` runs a framework / Guardian suite with
  Python's `random` seeded (mcsim's `random value`; `PYTHONHASHSEED=0`): `int_tests/test_guardian.py` on b98f833 and on
  this round gives byte-identical output for seeds 1-6. Its "rotation: every normal pattern ran" check is unseeded and
  fails for some draws on both trees (seed 3: P3 never drawn in 5200 t; 1 of 18 unseeded runs): a pre-existing flake of
  that suite, not a behaviour change.

## 20. User feedback after the 10-18 release (wip/bf2 on 7a6dc4f; plan.md "User feedback after the 10-18 release")

Three binding changes; what a pattern author has to know:

- **Reward (UF-1, "피해 +50%가 아니라 치명타 피해 +50%야").** 달빛 축복 받음 = CRIT RATE +15 and CRIT DMG +50 (`api.BUFF_CRIT`,
  `BUFF_CRIT_DMG`). Framework: a new fight-scoped modifier `#mbCritDmgAdd mb` (init / `player_reset` 0), added to the
  player's `critDamage` by the second mid-boss line of `items/hook/stat_buffs` (`#mbLive` 1, like `#mbCritAdd`). The
  module sets it in `coc/cure` (50) and zeroes it in `coc/apply_pl`, `coc/clear`, `coc/assert`; `#bfDmgPct` is 100 with
  the reward (the old ×150 is gone; `incoming` only applies the debuff's ×50 and the forced-crit undo). Kit texts:
  sub-line "(치명타 +15% · 치명타 피해 +50%)", `hud/ab_buff` "치명타 +15% · 치명타 피해 +50%".
- **Wind-ups (UF-2, "선딜 좀 줄이고").** `butterfly_clips.mjs` `RETIME` plays the ten damaging clips (H1-H4, the
  transformation, B1-B5) with about 25 % shorter wind-ups through the shared `mboss_rig_clips.retime` (the Guardian's
  mechanism; knots on key ticks so no keys collide, strikes and follow-throughs on 1:1 segments, recoveries shifted).
  The §9 table has the played events; the manifest carries `retime` / `authoredLen`. `api.CLIPS[c]['retime']`,
  `api.rt(clip, authored tick)` (half up, as the rig) and `api.tell_rt(t)` (= max(10, round(0.75 t))) are new. Rules the
  patterns follow: every event comes from the manifest (`ev_or` defaults are the played ticks now); a spec tick that is
  not an event goes through `rt`; a telegraph longer than the 10 t floor is `tell_rt(old)`. Per pattern:
  - H1: hit 1 unchanged (8, lead 2: the 10 t floor); hit 2 32, locked / telegraphed at 21 (11 t); the hops on the clip's
    `hop` / `hop2` events (19, 22; they were leap − 10 / − 4), the leap on `leap` (25). H2: sweep 10 (decal from 0), jump
    22, disc lock = impact − 10 (32 → 42). The H2 spiral-jump spin (authored 33-45) stays 1:1: the rig compiler refuses
    more than 120° per tick per part, which a compressed spin hit. H3: lock 1 (kick tell 10, ring 14), dash 6-8, kick 11,
    ring 15. H4: glint 5, stomp 12, blade 13 (the glint still 8 t ahead of the launch; a player 4 b away gets 11 t).
  - Transformation: open 3, sphere 5 (the 1 t key spacing 2..6 allows no more), rings 8, len 29; `seq_b` fx ticks via `rt`.
  - B1: dive 4, hit 11, lock 1 (tell 10), glide 4-11. B2: swings 4 / 24 / 52 / 72 (`B2_WIND` 4, lead 0); the move-away
    span after a swing ends before the next wind-up (`min(s + 20, gap_end)`); the crescent dives are unchanged (distance
    rule), so the last crescents of a swing can land after the next swing begins (each swing keeps its own volley group).
    B3: dive 13, slam 19, fan 21, lock 11 (tell 10), glide 26, trail 27-33. B4: wrap 3, orb 1 14, ball 22-29, orb 2 34,
    end 86. B5: swoop 3, whirl 14, cup 23 (dome tell 17, was 22), glint / rings 28, wrap 33, snap 39, detonation 40, flat
    74, revert 79, land 83; the swoop window is 11 t, so `B5_VMAX` 1.2 b/t (was 1.0) and `B5_GLIDE` 8..11 t.
  - Checks: `pat_human.py` / `pat_wing.py` read the module's constants (`WG.B1_TELL`, `WG.B3_TELL`, `whirl` event), so the
    decal fills are verified on the new hit ticks; `test_fixes.py` UF-2 locks the wind-up ratios (x0.70-0.84, the
    transformation x0.83), the 1:1 strikes and the telegraph lengths; `test_butterfly.py` section 0 the authored / played
    clip lengths. Two harness fixes the shorter clips exposed: `test_human.py` cut / death cases ran `go(n=40)`, which now
    outlived H4 (n = the cut tick); `pat_wing.py` B2's "step sideways" case moved the player back on the next swing tick,
    which coincided with a swing-3 landing at swing4 71 (swing 4 is 72).
- **Cure meter (UF-3, "일정 체력 이상 회복해야 하게").** Framework: `mboss/player_heal` adds every heal's amount after the
  `#mbHealPct` factor (now rounded half up) to `#mbHealAmt mb`, overheal included (the cap comes later in `player/heal`);
  init / `player_reset` zero it. Core: `coc/heal_ev` adds `#mbHealAmt` to `#bfCure` while `#bfCoc` 1 (then clears both
  counters); `coc/meter` (as the player) sets the target `#bfCureT` = 15 % of max HP (floor, ≥ 1) and the kit readout
  `#bkCureP` (meter %, floor, capped at 15) / `#bkCureT` (15); at the target `coc/cure`, below it `coc/progress` (chime,
  salmon / gold dust at the feet, `hud/ab_cure`). `coc/apply_pl` restarts the meter, `coc/clear` and the cure zero it,
  `coc/assert` (reload) keeps it. 달빛 이슬 heal 13 % rounded up (`api.DEW_HEAL_PCT`; ×0.6 = 7.8 %: two always fill the 15 %
  for any max HP with the half-up rounding; one never does from max HP 20 up: below that the 1 HP floor of the
  target lets one orb cure, and a player has at least 100 max HP). Groggy: `dew/spawn1` → `dew/need` (one orb's effective heal
  vs what the meter lacks) → `#bfDew1` = 1 or 2 → `dew/offer` (opposite each other); `dew/take` counts `#bfDew1` down, a
  reload re-offers what is left. Test 22 is a 25 % max-HP heal (15 % received: cures). Kit: the sub-line entry reads
  "[badge] 달빛 고치 — 회복 <#bkCureP>/<#bkCureT>% [dew]" (score components), `hud/ab_cure` (new), `ab_coc` "체력 15% 회복하면
  해제 · …"; the typed hint is "달빛 고치 — 체력 15% 회복하면 해제". Checks: `test_butterfly.py` sections 4 / 5 (one orb does
  not cure, two do, an item heal (jelly) and a character heal (Clorinde's lunge) fill it, overheal at full HP counts, the
  meter restarts on a new application, the groggy re-offer of 2 / 1, cleanup paths), `test_e2e_butterfly.py` (two orbs in
  the end-to-end fight), `test_fixes.py` UF-3 + the S4 / PL-1 / PL-2 / FX-3 cases updated to the meter; the harness's
  `bfsim.flat` resolves score components.
- **Balance** (`S:mb2/balance/bal.py`, Lv4 item-less player, seeds 11 / 22 / 33 × 3 min; `S:mb2/bf2work/bal_bf.py` runs
  the butterfly half and reuses the unchanged Guardian runs): the shorter wind-ups alone gave stand / melee walk /
  ranged walk 251.9 / 219.7 / 141.9 HP/min (1.16 / 1.39 / 1.09x of the Guardian's 217.1 / 158.3 / 130.6); with H1 55 / 70,
  H2 45 / 70, B1 70, B3 80, B4 100, B5 130 (H3, H4, B2, the B3 trail unchanged) 217.3 / 181.8 / 127.3 (1.00 / 1.15 /
  0.98x). The released build measured 243.6 / 184.4 / 112.9 (1.12 / 1.16 / 0.86x).
- **Verify round (wip/bf2, after e016416).** Re-derived from the generated functions and both manifests: every retimed
  segment has slope <= 1 and every played event is the warped authored event; every hazard has a same-tick, same-tell kit
  decal (fills on the hit tick) and every tell is >= 10 t; the hit ticks equal the played manifest events. Reward: the full
  `items/stat_light` path gives crit rate +15 / crit dmg 150 -> 200 and no damage factor in `incoming` (a 100 crit lands
  for 200, it was 225). Cure-meter edge repros (`S:mb2/bf2v/cure.py`): a heal in the same tick before an application, the
  exact target, a /reload with a partial meter, a max-HP change mid-debuff, prayer beads (the meter counts the amount before
  the beads' boost: the mid-boss hook runs first), max HP 100, red herb (at most +50 %: one orb 117 of 150), a groggy reload
  after one of two orbs. `bal.py` re-run (Guardian runs included) gives the same table. Fixed: the stale coefficients in
  the generated headers of `p/kick|jump|strike|barrage/start` (now from `api.DMG`), the human / wing docstrings and the
  README pattern lines (H1 0.55 / 0.7, H2 0.45 / 0.7, B4 1.0); comment and doc text only.
- **Build.** The §1 order twice: no byte changed (datapack, manifests, RP). The Guardian (`F:mboss/guardian/**`, its
  manifest and RP files) is byte-identical to 7a6dc4f; the RP sandbox `S:mb2/rp_bf2` equals the released RP (the retime
  changes no model or texture). Lint baseline: +29 −105 `bad target '<uuid>'` rig key files (moved to the played ticks).
