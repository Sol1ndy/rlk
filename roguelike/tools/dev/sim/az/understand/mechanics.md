# 야타용왕 (Azhdaha): mechanics and pattern-mapping study

Read-only study. Nothing in the repo or in any worktree was changed; this file is the only output.
Inputs: `S:az/src/wiki.md` (binding), the framework on `wip/fg` (newest), the shared datapack on the main line, the earlier
studies and contracts, the chapter study `S:az/understand/chapter.md`, the rig study `S:az/understand/rigtech.md`, and the
video notes that exist so far (`S:az/understand/v1.md`, `v7.md`) plus the motion key sheets in `S:az/understand/motion/`.
The other video notes (v2-v6, v8, v9) were still being written; every timing below that is not cited from v1/v7 or a key
sheet is a proposal and must be checked against them.

## Path shorthand

| short | meaning |
|---|---|
| `S:` | `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad` |
| `FG` | `S:mb3/wt_fg/roguelike` (branch `wip/fg`, fde9db7; newest framework) |
| `DP` | `/home/user/rlk/roguelike` (main line, 7a6dc4f) |
| `F:x/y` | `DP/data/rlk/function/x/y.mcfunction` (the shared files cited here are the same in `FG`) |
| `core:N` | `FG/tools/build_mboss_core.py` line N |
| `lib:N` | `FG/tools/mboss_lib.py` |
| `fgapi:N` `fgcore:N` `fgcruise:N` `fgfield:N` | `FG/tools/mboss_fieldgen/{api,core,cruise,field}.py` |
| `bfcore:N` `bfwing:N` `bfhuman:N` | `DP/tools/mboss_butterfly/{core,wing,human}.py` (`bfwing`/`bfhuman`: same lines in `FG`) |
| `bf2:` | `S:mb2/wt_bf2/roguelike` (branch `wip/bf2`, **uncommitted** work: the cure meter by heal amount) |
| `enc:N` `rh:N` | `DP/tools/build_raiden_encounter.py`, `DP/tools/build_raiden_hazards.py` |
| `t` | ticks (20/s); `b` = blocks |

Body frame used below: `f` = distance along the boss's facing (+ = toward the head), `s` = sideways (+ = the boss's left),
both from the body anchor (the husk), in blocks. Proposed dimensions follow `rigtech.md` §3.3 (rest pose): nose about
f +7.2, chest +3.4, hips −3.2, tail root −6.8, tail tip −13.4, front paws (±2.2, +3.0), hind paws (±2.1, −2.7), body half
width about 2.3. (Rigtech uses rig z with −z forward; signs are flipped here.)

---------------------------------------------------------------------------------------------------

## 0. Short answers

1. **Element pair.** Roll one of 4 pairs (불/번개, 물/얼음, 불/얼음, 물/번개) once, when the chapter-1 boss map is generated,
   and keep it in module scores `#azLeg` (1 Pyro / 2 Hydro) and `#azTail` (3 Electro / 4 Cryo) plus storage. Show it like
   Genshin (two coloured glyphs on a stele at the domain entrance, upper = tail, lower = leg). Repeat it on the gate label,
   in the gate title, on the arena steles, and as element badges on the boss bar's name line. The RES table goes into
   the module **`on_hit` hook**, which runs on the body before the RES step:
   `mres = 10`, then 30 for `#elem` 0 / 5 / `#azLeg` / `#azTail` (§1.4). Reactions are covered too.
2. **Phases.** Three equal pools. HP floors are a clamp in the module `incoming` hook (Raiden precedent): 2/3 during
   phase 1 and the first transition, 1/3 during phase 2 and the second transition, 1 HP while burrowed at the start of
   phase 3, then 0, so the boss dies on the first hit after it surfaces. Hitting a floor queues the transition at the
   next decision point. Sequence:
   - message;
   - **파멸의 산사태** = 6 expanding low ground fronts (the field generator's wave front, `fgfield:413-453`);
   - absorb, untargetable, with the rig recolour `look/<el>` (chest+legs in phase 2, back+tail in phase 3);
   - roar + the element's special.

   Before phase 3 the order is: phase-2 special, then landslide, then absorb, then the tail-only burrow.
3. **Brand (낙인).** In our game shields are rare (4 items, 1 engraving, the Geo crystallize shard) and only about 11
   heal sources exist, so a Genshin copy would punish most runs. Proposal:
   - A landed (not dodged) hit of an absorbed element brands the player for 4 s.
   - At expiry the brand is blocked if the player has any shield. Otherwise a non-lethal DoT runs: 4 ticks × 3 % max HP,
     Cryo stacks ×1/×1.5/×2.
   - Healing ≥ 8 % max HP (cumulative) cleanses it. This is the butterfly's cure meter, generalised.
   - Each new brand on a player without a shield drops a **응결 결정** crystal shard. It reuses the existing
     crystallize-shard pickup, so picking it up gives a shield of the brand's element.
   - It plugs in through a small framework hit event in `mboss/hurt` (`core:929-955`), a player-DoT helper, and
     `#mbHealAmt` (`bf2:`).
4. **Patterns.** All of them map onto existing helpers: `hz/*` shapes with `hz/aim`, `hz/resize`, `#hzRearm`, `#hzNoDodge`;
   `pj` with blade and steer; `mv/leap` and `mv/glide`; the waves; `lockp`. Several new helpers are needed:
   - a predictive lock (player velocity);
   - an orbit mover;
   - a lingering-field preset;
   - a multi-safe-circle "full" hazard for the lightning rounds;
   - runtime element plumbing for hazards and kit decals;
   - Hydro, Pyro, Cryo and Electro kit palettes;
   - a no-player-reaction option.

   Undodgeable (`#hzNoDodge`): side feint, tail whip and the landslide fronts (those are jumpable), the lightning
   rounds, and the brand DoT. Everything else can be dash-dodged (6 t i-frames).
5. **Targeting.** Classify the player each decision in the body frame: head / flank / tail / under / near-a-paw, plus a
   distance band. Use the same projection maths as `hz/hit` (`core:1547-1553,1587-1592`).
   - Turning: slow tracking at idle; a discrete 90° turn step when the angle is large; a short pre-turn before front
     patterns; no turn before side patterns.
   - Choice: weighted per zone. A player on the flank gets the feint or the whip 90 % of the time. No immediate repeats
     except the stomp and the jump (template `fgcore:535-585`).
6. **Main risks:**
   - fairness of the undodgeable side patterns and of the brand;
   - player-side reactions caused by the boss's elements (Melt ×1.5 on the player, Freeze roots the player);
   - the runtime element choice in a generator-baked world;
   - the proxy hit routing (a shared-file change);
   - card and hazard budgets of the 4 element variants;
   - timings not yet confirmed from v2-v6/v8/v9.

---------------------------------------------------------------------------------------------------

## 1. Element choice on entry

### 1.1 What the original does

- Weekly the boss absorbs a **leg/tail** pair. Every one of 2 × 2 = 4 pairs occurs: 불/번개, 물/얼음, 불/얼음, 물/번개
  (`wiki.md:79-81`).
- The domain entrance stele shows **two coloured glyphs: upper = tail (phase 3), lower = leg (phase 2)**. In the guide's
  run, upper is violet (Electro) and lower is pale cyan (Hydro), so the pair is 물/번개 (`v1.md` §1,
  `v1/glyphs_door.jpg`, `v1/k_f1380_door_glyphs_last.jpg`).
- The guide's notes caption also states it: "야타 용왕의 속성은 입장전에도 문 앞의 글자 색으로 알 수 있습니다"
  (`v1.md` §0).
- Other takes use other pairs: v7 take C/D is 불 legs + 얼음 tail (`v7.md` §0).
- The user's binding rule: the pair is decided "on entry", and the boss has 30 % RES to both chosen elements
  (`wiki.md:10-17`).

### 1.2 Roll, storage, lifetime

| item | proposal | why / where |
|---|---|---|
| when | when the chapter-1 boss map is generated, i.e. in the chapter-boss route (`chapter.md` §2.2, `mboss/cb/route` → `mboss/cb/layout {id:"azhdaha"}`), or in the module's `prep` hook that `chapter.md` R1 proposes (runs as the boss zone marker when the entrance is built) | "on entry" = before the gate is pressed, so the entrance can show it |
| what | `random value 0..3` → pairs 0 불/번개, 1 물/얼음, 2 불/얼음, 3 물/번개 (the wiki order) | all four combinations |
| store | fake players `#azLeg mb` (1 Pyro / 2 Hydro), `#azTail mb` (3 Electro / 4 Cryo) in `#elem` numbering (`lib:24`), mirrored in storage `rlk:mboss az.pair {leg:1b..2b,tail:3b..4b}` and on the zone marker's `data.az_pair` (the route carries `boss_id` the same way) | the module `ai/vars` reset at spawn (`fgcore:235-246` pattern) must **not** touch them; the spawn hook re-reads them from storage / the zone |
| lifetime | kept for retries of the same boss map (an aborted fight brings the gate back: `core:748-751` `cancelled`, `chapter.md` R4); cleared by `run/start`, `run/end` and `test/stop` together with `#cbForce` (`chapter.md` §2.2) | the player must not reroll by aborting |
| tests | `test/pattern {id:90..93}` forces the pairs (as `chapter.md` §2.3 proposes); on a live fight it also recolours the rig and the badges | |
| option (open) | roll earlier, at the chapter's last node map (`F:room/end_boss:1-4`, the "보스전" object), and show the pair on that object ("야타용왕 · 물 / 번개") | shields and heals matter in this fight (§3); seeing the pair one map earlier gives the shop and node choices a purpose |

### 1.3 How to announce it

1. **Entrance stele (the original tell).** The chapter-1 boss zone is a "domain entrance" room with a gate object
   (`chapter.md` §3.3 R2, §4.3).
   - The `prep` hook lights two glyphs on a dark stele beside the gate: **upper = tail colour** (Electro violet `#A291D0`
     / Cryo ice `#9FE8F5`), **lower = leg colour** (Pyro `#FF8A3D` / Hydro `#8CCCDE`). Colours: `v1.md` §1, the boss-bar
     aura colours at `core:1150-1153`.
   - Implementation: two `text_display` glyphs from the module kit font (a water curl, a flame, a snowflake, a bolt;
     new codepoints in the az kit's own range, like the field generator's U+E700 font, `fg_fx_api.md` §5), or two
     tinted `item_display` panels. Each has a soft glow particle every 10 t.
2. **Gate object.** Build it like `F:room/obj/make_node2.mcfunction:1-11` (two icons side by side + "A + B" + two
   description lines) instead of the single-icon `make_node` that `k_mboss` uses (`F:room/obj/k_mboss.mcfunction:1-7`).
   Label:
   - line 1: **야타용왕** (gold);
   - line 2: "흡수 원소: 물 (다리 · 2페이즈) · 번개 (꼬리 · 3페이즈)" in the element colours;
   - line 3: "내성: 물리·바위·물·번개 30% · 그 외 10%".
3. **Gate click / fight start title.** As `mboss/gate` (`core:318-337`):
   - title "야타용왕" (cur.title);
   - subtitle "봉인된 바위 용의 왕 · 물 / 번개", built from the pair (a storage text component written at roll time);
   - the bell / heartbeat sounds.
4. **Arena.** The two steles at the arrival point repeat the glyphs (`chapter.md` §4.3, "steles" row).
5. **Boss bar.**
   - Name line: `Lv.6 야타용왕` + `extra[]` (`core:1120`) holding two badges, e.g. `  ◈물` `  ◈번개`. A not-yet-absorbed
     element is drawn dim (#707070 + the glyph). On its absorb it switches to the full element colour. A third badge,
     the brand state, comes in §3.
   - Sub-line (`sub[]`, `core:1130`): the nameplate "봉인된 바위 용의 왕" at the intro (like `fgcore:448-451`), then
     "곧 원소의 힘을 흡수합니다…" during transitions and the pattern names.
   - Under-bar (`#buSub/#buSubMax/#buSubCol`, `core:1124-1127`, colour codes `lib:27`): HP left in the current phase
     pool, coloured by the phase element (Geo 5 → leg element → tail element). §2.7.
6. **On absorb.** A typed line `line/say` (`core:1165-1180`): "물 원소 흡수" / "번개 원소 흡수" in the element colour.
   This is the guide's own caption wording (`v7.md` §0, caption 4 "얼음 원소 흡수"), and the rig recolours (§2.4).

### 1.4 Applying the RES table in the damage code

**The hit path on a framework body** (`F:combat/apply.mcfunction`):

| line | step | relevant to RES |
|---|---|---|
| 15-17 | dying → nothing; `rlk_mb_inv` → only true damage | |
| 21 | `element/on_hit`: auras, reactions; amplifying reactions change `#dmg`; transformative reactions are queued | sets `#rx`, `#tfm` |
| **23** | **`mboss/d/on_hit`** (module hook) for `rlk_mb_body` only, never for true damage. `#elem` is known here | **set `mres` here** |
| 25 | `combat/apply_mods` (`F:combat/apply_mods.mcfunction:1-18`): engravings, items, Yoimiya, Ronova amp, level factor (skipped for `#tfm`), **RES `combat/res` if `mres ≠ 0` (`:13-14`, applies to reactions too)**, then the module `incoming` (`:18`) | |
| 27 | aux objects (`rlk_mb_hit`) leave to `mboss/aux_hit` **after** `apply_mods`, so their RES was already applied with the aux's own fixed `mres` | |
| 64-82 | HP subtraction, kill, rewards, `mboss/death_start` (`:80`) | |

Facts:

- `F:combat/res.mcfunction:1-11` is the Genshin formula: R ≤ 75 → `dmg × (100 − R) / 100`, at least 1. So RES 30 →
  ×0.70 and RES 10 → ×0.90.
- The body starts at `mres 0` (`core:482`, `body_setup`).
- Transformative reaction damage reaches `combat/apply` again with `#elem` = the reaction element:
  - `F:element/aoe_hit.mcfunction:3` (`#elem = #qEl`), for overload, superconduct, shatter, swirl, bloom;
  - `F:element/dot.mcfunction:1-9` for burning and electro-charged.

  So a per-hit `mres` written in `on_hit` covers player hits, amplified hits, reactions and DoTs alike. An Overload on a
  Pyro-legged Azhdaha is resisted as Pyro (30), which matches Genshin.

**The module `on_hit` (phase-independent, the user's "final table"):**

```
# Hook on_hit (@s = body, inside combat/apply before apply_mods; #elem #tfm #rx known). The RES table:
# Physical 30, Geo 30, the chosen Pyro-or-Hydro 30, the chosen Cryo-or-Electro 30, every other element 10.
scoreboard players set @s mres 10
execute if score #elem tmp matches 0 run scoreboard players set @s mres 30
execute if score #elem tmp matches 5 run scoreboard players set @s mres 30
execute if score #elem tmp = #azLeg mb run scoreboard players set @s mres 30
execute if score #elem tmp = #azTail mb run scoreboard players set @s mres 30
```

Notes:

- `#elem` 6 Anemo, 7 Dendro and 8 Void (Ronova) fall to 10. The non-chosen leg and tail elements get 10.
- True damage (`test/kill`, `core:2219-2229`) skips `on_hit` and the RES step, as intended.
- **Proxies.** The rigtech proposal routes a proxy hit to `combat/apply` as the body (`rigtech.md` §3.3, one line at
  the top of `combat/apply`), so `on_hit` and RES run on the body unchanged.
  - If proxies were made as framework aux objects instead (`core:1049-1091`), the table would not apply: `on_hit` is
    called for `rlk_mb_body` only (`combat/apply:23`), and `aux_hit` runs after RES (`:27`). That path would need
    `combat/apply:23` widened to the proxy tag. Keep the redirect.
- **Static or per phase.** The user's table is flat ("Final table", `wiki.md:15`). The original raises the absorbed
  element's RES only after the absorb (Pyro/Hydro +60 from phase 2, Cryo/Electro +50 from phase 3, `wiki.md:53-62`, the
  YouTube description).
  - Recommendation: implement the user's flat table.
  - Keep a generator switch `RES_BY_PHASE` that gates the last two lines on `#azPh` (leg ≥ 2, tail = 3), in case the
    user wants the original ramp. Open question §6 Q1.
- **The butterfly precedent is the opposite case.** The user said "기본적으로 있는 불, 풀 내성은 없애줘":
  - the butterfly has `mres 0` and its `incoming` never reads `#elem` (`bfcore:304-309`; `S:mb2/plan.md:8,25-26`;
    `S:mb2/bf_contract.md:147-148`);
  - the field generator copied the rule (`S:mb3/fg_contract.md:155-156`);
  - `S:mb2/tests/test_butterfly.py:613-627` locks "equal damage for every element, `mres` 0".

  That was a per-boss user decision (`chapter.md` R7). Azhdaha's test must lock the opposite: one hit per element 0-8
  for each of the 4 pairs, and check ×0.70 / ×0.90. The existing butterfly test keeps passing because the edit is
  module-local.
- **HUD.** No RES numbers on the bar. The gate label (§1.3) carries them. The "면역" popup (`core:1040-1043`) is not
  needed: nothing is immune.

---------------------------------------------------------------------------------------------------

## 2. Phases

### 2.1 HP layout and floors

- One pool `mhpM`, three equal thirds (Genshin 292,249 × 3, `wiki.md:50`). With `chapter.md`'s proposal (`hp 360`, L6)
  `mhpM = 3612`, so floors F1 = `mhpM × 2 / 3` = 2408 and F2 = `mhpM / 3` = 1204.
- Module state: `#azPh` 1-3, `#azTr` (0 none, 1 queued, 2 running), `#azBur` (1 = phase-3 tail-only burrow).
- **Floor clamp in the module `incoming` hook** (`F:combat/apply_mods.mcfunction:18`, after RES, before the HP
  subtraction at `F:combat/apply.mcfunction:64-66`). Raiden does the same at 55 % (`enc:577-600`: `#rdAfter = mhpC −
  dmg`, `threshold` clamps `#dmg = mhpC − floor`).

```
# Hook incoming (@s = body). Floors: phase 1 = 2/3, phase 2 = 1/3 (both also during their transition), phase 3 = 1 while
# burrowed (tail-only), else 0. Reaching a floor queues the transition (phases 1-2).
execute if score #dmg tmp matches ..0 run return 0
function rlk:mboss/azhdaha/hp/floor          # sets #azF from #azPh / #azBur and @s mhpM
scoreboard players operation #azAft mb = @s mhpC
scoreboard players operation #azAft mb -= #dmg tmp
execute if score #azAft mb < #azF mb run function rlk:mboss/azhdaha/hp/clamp   # #dmg = mhpC - #azF (>= 0); #azTr 0 -> 1 if #azPh <= 2
```

- `chapter.md` R6 proposes a generic core helper `mboss/floor` (module sets `#mbFloor`). Either works. The generic helper
  is better because Apep needs it too.
- **Display at the floor.** `combat/apply` still prints the clamped number (0). Use a module popup "흡수 중" (like
  `core:1040-1043` "면역"), at most once per 10 t. The red hurt flash is already skipped for 0 (`:57`).
- **When the transition starts.** Genshin shows the message as soon as the threshold is reached; the current attack
  finishes, then 파멸의 산사태 starts.
  - Proposal: `#azTr 1` makes `ai/next` (the decision point, `fgcore:492-508` template) run the transition service
    sequence instead of a pick.
  - A pattern still running is not cut (its hazards stay fair). It is shortened at its `release` point when it has one
    (`fgapi:276-280`).
  - The message shows at once: sub-line + typed line + a gold `title` flash. A player who keeps hitting sees "0" / "흡수
    중", which teaches the floor.

### 2.2 Transition sequence (services, proposed ticks; footage where cited)

| step | 1 → 2 | 2 → 3 | footage / helper |
|---|---|---|---|
| message | "야타용왕이 곧 {물} 원소의 힘을 흡수합니다…" (the leg element named) | same, the tail element | `motion/L_slide_keys_v4.jpg` frame a: the message 20 t before the first wave; `wiki.md:82` |
| phase-2 special first | — | 격류 범람 or 운석 낙하 (§4.3) | `wiki.md:120-123` ("at the second transition it first uses the phase-2 special") |
| **파멸의 산사태** | 6 fronts | 6 fronts | §2.3 |
| absorb | ≈ 110-120 t, untargetable (`rlk_mb_inv`, `core:885`, `F:combat/apply:17`; proxies parked: rigtech `px/state/burrowed`), recolour chest+legs | ≈ 56 t gather + burst + ≈ 90 t ice/spark rain (cosmetic), recolour back+tail | Hydro absorb `motion/M_absorb_hydro_v4.jpg` (13.6-19.4 s ≈ 116 t); Cryo absorb `v7.md` §C (gather 0-36, burst +37, rain to +148, rear +148..156, roar +156..211) |
| roar + special | roar (≈ 55 t, cosmetic dome rings) → 격류 범람 (Hydro) / 운석 낙하 (Pyro) | rear + roar → the tail-only burrow (§2.6) | `motion/N_roar_hydro_v4.jpg` (caption "포효 — 원소를 흡수하고 포효할시 특유의 기술을 사용합니다", then "물방울") |
| floor | stays F1 until the absorb ends, then F2 | stays F2 until the absorb ends, then 1 (burrow) | §2.1 |

- Untargetable only during the absorb itself. The landslide is targetable but floored, so players can still build
  reactions and the guide's "stop attacking, move away" stays the right play (`wiki.md:84-85`).
- Pause/reload: the sequence runs as service patterns on the pattern slot (`fgcore:605-681`: `p/run`, `p/svc`, service
  ids). A reload re-derives the step from `#azTr`/`#azPh`, as the field generator re-derives its field stage
  (`fgcore:376-406`).

### 2.3 파멸의 산사태 (6 hits)

- Original: "6 wide-range shockwaves in a row; every hit is heavy; the shockwave hits only near ground level" (`wiki.md:84-85,120-123`).
  Key sheet `motion/L_slide_keys_v4.jpg`: ground bursts at wave t+1, ≈ +26, +54, ≈ +81, +110, and a late sixth at
  ≈ +164; the bursts radiate around the whole body.
- **Helper: the field generator's expanding front** (`fgfield:413-453`). Per front:
  - a framework `hz/ring {r0:0, r:<start>}` with `#hzQuiet 1`, `#hzSfx 0`, `#hzNoDodge 1` and **`#hzY1` 0.7** (a jump
    clears it);
  - grown every tick by `hz/resize_s` (`core:1660-1672`);
  - paired with the kit's `tele/wave` decal and `p/wave_band` (`fg_fx_api.md` §4.1).

  For Azhdaha:
  - centre = the body anchor;
  - start radius 4 b (outside the paws);
  - end radius **16-18 b** (not the whole arena: the walk radius is 28 b, `chapter.md` §4.3, so "move away" works);
  - speed ≈ 0.5 b/t, band 2.5 b;
  - spacing about 26 t (fronts 1-5), 50 t before the 6th;
  - coefficient ≈ 1.0-1.1 each (`chapter.md` §5.4).
- Dodge rule: dash i-frames do not help (`#hzNoDodge`). Jump each front or stay outside r 18. This matches Genshin
  (i-frames do work there, but the low hit band is the known answer).
- Element: Geo for the first transition. The second transition's fronts carry the leg element, which applies the brand
  (the wiki says nothing about this; flagged in Q8).

### 2.4 Absorb recolours

- What the footage shows:
  - phase 2: chest + legs take the leg element (Hydro: blue glowing meander lines on the bracers and the beard plate;
    Pyro: dark maroon with red-orange crack meanders; `v7.md` §C, `wiki.md:128-131`);
  - phase 3: back crystals + tail take the tail element (icy white-cyan; violet with arcs; `v7.md` §C/D,
    `motion/O_tailburrow_*_v6.jpg`).
- Rig API (rigtech §4.4 proposes it): `look/<pyro|hydro|cryo|electro>` per region group (`legs` = chest + 4 legs,
  `tail` = back plates + crystals + tail segments).
  - Cheapest: one tinted overlay item per region with `custom_model_data` colour tints, the same mechanism the kits use
    (`fg_fx_api.md` §1 "Tint"). That avoids texture swaps (atlas budget: rigtech TL;DR 7).
  - The absorb clip fades the overlay in. Reload and tests re-apply the looks from `#azPh` + `#azLeg/#azTail`.
- Fight ambience: the guide's arena tint changes (the Pyro phase floor turns orange-red with fire strips,
  `motion/T_pyro_v5.jpg`; the Cryo burst turns red → cyan, `v7.md` §C). In MC this is the kit's particles, colour flashes
  (`fx/hud/flash_*`) and, optionally, arena light props. No block swaps.

### 2.5 Phase-2 element extras on phase-1 patterns

The wiki: "every phase-1 pattern gets the absorbed element's extra effect" (`wiki.md:129-131`). The list is in §4.3. Mechanically it is a
`#azPh ≥ 2` branch in each phase-1 pattern's timeline that adds the element hazards. Phase 3 adds the tail element's
extras on top (spikes variant, tail trail) while the leg extras stay.

### 2.6 Phase-3 start: the tail-only burrow and the final hit

- Original:
  - at phase-3 start it burrows at the arena centre and only the tail stays above ground;
  - the tail can be hit;
  - the phase-2 hazards are still active;
  - if HP reaches 0 while burrowed it does not die: a little HP remains, and it must be hit once more after it surfaces
    (`wiki.md:159-162`).
- Guide captions:
  - "꼬리 버로우 — 장판 피하기입니다 번개 속성일 때 중앙 근처에 있으면 피하기 쉽습니다 / 야타용왕의 피가 1 아래로
    내려가지 않습니다" (HP never below 1; `motion/O_tailburrow_in_v6.jpg`);
  - Cryo version: "마찬가지로 장판 피하기입니다 / 번개 장판 피하기보다는 귀찮습니다" (`v7.md` §0 caption 5).

  Dig → tail-only ≈ 76 t (`v7.md` §D). Electro burrow ≈ 10.0 → 36.6 s ≈ 530 t until it rears out
  (`motion/O_tailburrow_in/mid/out_v6.jpg`).
- Our version:
  - **Dig** 16 t + sink 60 t (rigtech §4.2 pose: root sunk, tail chain raised, other parts at scale 0, crater prop).
  - **Tail-only** about **12-16 s** instead of 26 s (our fights are shorter; Q10). `#azBur 1` → floor 1 HP.
    `px/state/tail_only` makes only tail proxies 1-4 vulnerable (rigtech §3.3 table).
  - The body anchor moves to the tail's emergence point (rigtech §4.2) and the leash is off (`#mbNoLeash 1`,
    `core:891`).
  - During the burrow: 서리 습격 (Cryo) or 벼락 습격 (Electro) (§4.4). Phase-2 lingering fields keep ticking.
- **Surfacing**:
  - burst disc r 5 at the emergence point (tell 20 t; the last lightning round may land on it, `wiki.md:181-182`), then
    `#azBur 0`;
  - floor 0, all proxies back (`px/state/normal`).
  - If `mhpC` is 1 at that moment, show the sub-line "마지막 일격!" and a gold glow on the proxies until the next hit.
    The kill then runs the normal path (`F:combat/apply.mcfunction:69-80` → `core:893-908` death shell), with chapter-mode
    rewards (`chapter.md` R4/R5).
- While burrowed, `true_hit` (`core:968-990`) still bypasses the floor. `test/kill` must keep working (`chapter.md` R6).

### 2.7 HUD for phases

- Main HP bar: the whole pool (`core:1121-1122`). The bossui cannot draw notches (`DP/tools/build_bossbar.py`).
- Under-bar (module `bars` hook, `core:1124-1127`):

  | state | under-bar | colour |
  |---|---|---|
  | fight | `#buSub = mhpC − floor`, `#buSubMax = mhpM / 3` (the phase pool) | phase element via `elem_to_bu` (`core:1158-1161`) |
  | transition | sequence progress | gold (8) |
  | burrow | burrow time left | tail element |

- Name line `extra[]`: the two element badges (§1.3) and the brand badge (§3.3 item 6).

---------------------------------------------------------------------------------------------------

## 3. The brand (낙인)

### 3.1 Original

- From phase 2, the absorbed elements' hits brand the character. Without a shield, a strong, long DoT follows when the
  brand expires. The brand counts as an element attachment, so healers and cleansers remove it; shields are the main
  answer (`wiki.md:68-72`).
- In-game tip, seen in `motion/N_roar_hydro_v4.jpg` top banner: "야타용왕이 물 원소 공격에 명중한 후 캐릭터가 보호막의
  보호를 받지 못하면, 계속 물 원소 피해를 받습니다".
- Measured in `v7.md` §A2: after a hit, a glowing pink-violet square rune on the chest and a violet aura. HP drops
  **≈ 5.1 % max HP every 20 t, ≥ 5 ticks** (≈ 25 % max HP).
- Cryo brands stack (`wiki.md:167-168`).

### 3.2 What our players have

| kind | source | numbers | file:line |
|---|---|---|---|
| element shield `shieldHP` (15 s, `shieldT`) | crystallize shard pickup | amount = reaction base × 130 %; **its element `shieldEl` absorbs that element at 250 %** | `F:element/rx/crystal.mcfunction:1-15`, `F:element/run/crystal.mcfunction:1-12`, `F:element/crystal_tick.mcfunction:1-15`, `F:element/shield_absorb_el.mcfunction:1-17`, `#shElEff 250` `F:load:661` |
| | 옥장 방패 (jade_shard, mythic): skill → 30 % max HP for 20 s | `F:items/proc/jade.mcfunction:1-8`, `F:load:967-968` |
| | 흑요석 거울 (obsidian_mirror, epic): skill → 12 % for 8 s | `F:items/proc/mirror.mcfunction:1-6`, `F:load:996-998` |
| | 잠결의 별 (night_stars, rare): skill → 8 % | `F:items/proc/night_start.mcfunction:1-6`, `F:load:1085-1086` |
| | 무결점 보호막 (seamless_shield, epic): burst → periodic 6 % + 2 % heal | `F:items/proc/seam_pulse.mcfunction:1-11`, `F:load:1067-1071` |
| | `element/shield_gain` keeps the larger shield, 300 t | `F:element/shield_gain.mcfunction:1-7` |
| engraving shield `gShield` | 수호 (guard) ×4: 100 HP, regrows 15 s after breaking | `F:engravings/guard/absorb.mcfunction:1-12`, `F:engravings/guard/tick.mcfunction:1-9`, `F:load:901-903`, `F:engravings/register.mcfunction:6` |
| shield order on a hit | guard first, then the element shield | `F:player/take_damage.mcfunction:29-30`, `F:player/hurt_elem.mcfunction:4-6` |
| heals | heal orb 10 % (5 % kill roll; none in a boss arena) `F:combat/healorb_heal.mcfunction:1-9`, `F:load:839`; items: 메이드의 건틀릿, 정화의 풀고리, 해파리 등불, 사냥개 호루라기, 장생의 호리병, 민들레 씨앗, 치유의 부적, 간호사의 주사기, 비운 깃발, 지니 램프, 무결점 보호막 (`F:items/proc/{maid,gring_pulse,jelly_heal,hound_heal,gourd_heal,dandelion,talisman_heal,nurse_pay,flag_heal,genie_pulse,seam_pulse}`); shop heal node; Clorinde (converted to Bond of Life, `F:char/heal_hook.mcfunction:3`); Arlecchino burst | every heal goes through `F:player/heal.mcfunction:1-6` → `F:items/hook/on_heal.mcfunction:1-7` → `mboss/player_heal` (`core:419-430`: `#mbHealEv`, `#mbHealPct`) |
| heal amount | `bf2:tools/build_mboss_core.py:410-425` adds `#mbHealAmt` (the amount after `#mbHealPct`, overheal included); the butterfly's 달빛 고치 is cured at 15 % max HP cumulative (`bf2:tools/mboss_butterfly/core.py:916-937`, `bf2:tools/mboss_butterfly/api.py:127-128`) | **uncommitted on `wip/bf2`**; must land before Azhdaha uses it |
| cleanses | **none**. `element/clear` (`F:element/clear.mcfunction:1-15`) is only called by `player/init` and `player/on_respawn` | — |
| player DoT paths | reaction DoT: `F:element/dot.mcfunction:8` → `F:player/hurt_elem.mcfunction:1-11` (no defence; **dash i-frames block it** `:2`; shields absorb `:4-6`); the butterfly's non-lethal debuff hit (`F:mboss/butterfly/coc/apply_pl.mcfunction:1-14`: % of current HP, floor 1 HP, no i-frames, no shields) | — |
| player auras | a boss element hit attaches 1 U to the player and reacts (`F:player/take_damage.mcfunction:17-22` → `F:element/player_hit.mcfunction:1-16`; reaction base 50 % of the hit, `F:load:1153`) | §3.5 |

So:

- shields come from 4 items (one mythic), one engraving, or a Geo crystallize, which needs a Geo character and an
  aura on a mob;
- heals come from about 11 items;
- nothing cleanses.

A chapter-1 player usually has neither. A Genshin-strength brand (≈ 25 % max HP per brand, `v7.md`) would make phase 2/3
a damage race.

### 3.3 Proposed rules (fair adaptation)

1. **Brand on hit.** A hit that lands (`#dodged 0`) with the element of an absorbed slot brands the player:
   - the leg element in phases 2-3, the tail element in phase 3;
   - lingering fields count too (one brand refresh per 10 t of standing in them);
   - Geo and physical hits never brand.

   Brand state:
   - element `#azBrE`;
   - timer `#azBrT` = **80 t** (4 s), refreshed by new hits;
   - stacks `#azBrN` (Cryo only: 1-3; others 1);
   - a new element replaces the old brand.
2. **Expiry.**
   - If the player then has a shield (`shieldHP ≥ 1` or `gShield ≥ 1`): the brand dissolves with a small chime and a
     cyan sparkle, "보호막이 낙인을 막았습니다". No cost (open: a chip of the shield).
   - Otherwise: **DoT 4 ticks, every 20 t, each 3 % max HP × stack factor** (Cryo ×1 / ×1.5 / ×2), element-coloured
     numbers. Shields that appear mid-DoT absorb the ticks: guard first, then the element shield, which absorbs at 250 %
     when its element matches.
   - Dash i-frames do not stop the ticks. Defence does not apply. **Non-lethal**: a tick never takes the player below
     1 HP, like the butterfly's debuff (`F:mboss/butterfly/coc/apply_pl.mcfunction:10-11`); Q4.
   - A Lv5 player (148 HP): 4 × 4 = 16 HP per brand (11 %); Cryo ×3 stacks 32 HP.
3. **Cleanse by healing.** While branded or burning, healing ≥ **8 % max HP** cumulative (`#mbHealAmt`) clears the
   brand / the DoT. Use the butterfly's cure fx style. A heal orb (10 %) or any item heal of that size counts. The same
   meter idea the user asked for on the butterfly ("일정 체력 이상 회복해야 하게"; `bf2:` core:916-918).
4. **In-arena counterplay: 응결 결정 (crystal shards).** When a brand is applied and the player has no shield, Azhdaha's
   back sheds one shard:
   - cooldown 200 t, at most 2 alive;
   - placed 4-6 b from the player, pulled toward the arena centre (`lockp` + clamp, `fgapi:288-318`), never inside a
     live hazard's telegraph if avoidable;
   - life 200 t;
   - glowing gold-amber with the brand's colour inside.

   Pickup = the existing crystallize pickup: `F:element/crystal_tick.mcfunction:5-10` → `element/shield_gain` with
   `#shEl` = the brand element, so the shield absorbs that element at 250 %. Shield = **12 % max HP** (≈ 18 HP at Lv5,
   ≈ 44 HP vs the brand element), 15 s.
   - This is the butterfly's 달빛 이슬 idea (heal orbs because "few characters heal", `S:mb2/plan.md:98`) translated
     into Genshin's shield answer. It fits the boss's gold-crystal look.
   - Engravings and characters that react to shards (반석/petra, Navia's shard gain, Ronova's void crystal;
     `F:element/crystal_tick.mcfunction:7-14`) trigger as with any crystallize shard. That is a small bonus, acceptable.
5. **Cryo stacks.** 서리 습격 and the ice spikes stack. A third stack flashes the badge red.
6. **Telegraph of the danger.**
   - The player sees the brand on themselves: a rune ring particle (element dust) at chest height every 4 t, and the
     sidebar line "낙인(물) 3" (seconds) like the guard engraving's "수호 보호막" line (`F:engravings/guard/tick.mcfunction:2-3`,
     sidebar `stacks`, `F:load:587-588`).
   - On the boss bar's name line, a third badge "  ◈낙인 물 3s".
   - The first brand of the fight types a hint: "낙인 — 보호막이 있으면 사라집니다 · 체력 8% 회복 · 결정을 주우세요".

### 3.4 Where it plugs in

| piece | where | change |
|---|---|---|
| hit event | `mboss/hurt` (`core:929-955`), after the hit (`:950-952`) | new, opt-in: `execute if score #dodged tmp matches 0 run function rlk:mboss/hit_ev`. It sets `#mbHitEv += 1`, `#mbHitEl = #cmEl` and `#mbHitSh` = 1 when the player had a shield before the hit (stored before `cm/hit_pl2`). The running module reads and clears it in its tick, exactly like `#mbHealEv` (`core:419-430`, `bfcore:286`). Also catches pj hits (`core:1863-1878` → `mboss/hurt`) and direct swings |
| brand logic | module `tick` (after the AI state, before `p/run`, like `fgcore:295-312`) | `brand/ev` (apply / refresh / stack), `brand/tick` (timer, expiry test, DoT clock, cleanse by `#mbHealAmt`, shard drops), `brand/clear` (death, pause, cleanup, fight end) |
| DoT helper | new framework function `mboss/pl_dot` (score form: `#mbDotPct` ‰ of max HP, `#mbDotEl`, `#mbDotLethal`) | from `F:player/hurt_elem.mcfunction:3-11`, but: `dashInvT` saved/zeroed/restored like `hurt_nd` (`core:956-962`); element colour via `#elem` for `player/hurt_do` (`F:player/hurt_do.mcfunction:1-5`); HP floor 1 unless lethal; refused when dead / reviving / selection screen like `mboss/hurt` (`core:937-940`). Apep's DoTs can reuse it |
| heal cleanse | `#mbHealAmt` (`bf2:` core:410-425) | merge `wip/bf2` first |
| shards | module copy of `F:element/run/crystal.mcfunction:2-6` | extra tags `rlk_room`, `rlk_mb_aux` so `cleanup_aux` (`core:758-762`) and room clears remove them; `rxDmg` = 12 % max HP, `rxEl` = brand element; pickup stays in `F:element/tick_world.mcfunction:3` |
| HUD | module `bars` / `extra[]`; sidebar `stacks` entry | `scoreboard players reset 낙인 stacks` on clear (the guard line does the same, `F:engravings/guard/tick.mcfunction:4`) |
| pause | module `pause` hook | brand and DoT clocks freeze with the fight (they live in the module tick) |
| death / cleanup | module `death_start`, `cleanup` | clear brand, DoT, shards, sidebar line |

### 3.5 Player-side reactions from the boss's elements (risk, needs a decision)

Every elemental boss hit attaches to the player and reacts (`F:player/take_damage.mcfunction:22` → `F:element/player_hit.mcfunction:1-16`).

| pair | reaction | effect on the player |
|---|---|---|
| 불 + 얼음 | Melt ×1.5 (`F:element/on/ice.mcfunction:3`), ×2 the other way | a 50-damage hit becomes 75-100 |
| 물 + 얼음 | Freeze | `F:element/frz_on_player.mcfunction:1-2` sets movement and jump to 0: rooted inside a telegraph |
| 불 + 번개 | Overload | burst damage + knock |
| 물 + 번개 | Electro-charged | ticks |
| any + 번개/얼음 vs Hydro aura | Superconduct | **`scT 240`, physical damage taken ×1.4 for 12 s** (`F:element/player_hit.mcfunction:15`, `F:player/take_damage.mcfunction:19-21`) |

Genshin does all of this too. In our chapter 1, with the brand on top, it is double punishment, and the Freeze can be a
death sentence.

Recommendation: a framework one-shot option `#hzNoRx` / `#pjNoRx`, and the score `#mbNoRx` around `mboss/hurt`. A one-line
gate at `F:player/take_damage.mcfunction:22` (`unless score #mbNoRx tmp matches 1`) skips `element/player_hit` for that
hit but keeps `hurtElem` for the number colour. Azhdaha sets it on every elemental hazard: **the brand replaces player-side
reactions** (Q3).

### 3.6 Tests

mcsim (`chapter.md` R15):

- brand on a landed hit only (a dodged hit does not brand; `#hzNoDodge` hits do);
- expiry with a guard shield / an element shield / none;
- the DoT ticks, non-lethality, the 250 % same-element shield;
- the heal cleanse at 8 % (two small heals that add up);
- shard drop, cap and pickup → `shieldEl`;
- Cryo stacks;
- pause freezes;
- reload keeps or clears consistently;
- cleanup removes the shards and the sidebar line;
- `#mbNoRx` skips `player_hit` but keeps the colour.

---------------------------------------------------------------------------------------------------

## 4. Pattern mapping

### 4.1 Helper inventory

**Existing (framework, `core`, call builders in `lib`):**

| helper | lines | use here |
|---|---|---|
| `hz/disc ring sector line full` + options (`#hzAct #hzEl #hzKB #hzKBDir #hzY0/1 #hzR0 #hzBack #hzSfx #hzVis #hzCol #hzLinger #hzQuiet #hzGrp #hzNoDodge #hzRearm`) | `core:1242-1269`, `opts_reset core:210-238`, `hz/init core:1285-1354`, `lib:143-196` | every ground hit |
| one hit per hazard; feet-only test inside a height band | `core:1530-1566` (band `:1534-1538`) | jumpable fronts: `#hzY1` 0.7 |
| `hz/aim` (move / re-aim a live hazard) | `core:1634-1648`, `lib:184-186` | moving orbs, sweeping tail, homing meteors |
| `hz/resize` / `resize_s` | `core:1649-1699`, `lib:189-191` | expanding fronts, growing fields |
| `#hzRearm N` (lingering, hits again) | `core:1302,1427,1629-1633` | fields, orbs |
| `#hzNoDodge` (dash i-frames ignored for that hit) | `core:1301,1623`, `hurt_nd core:956-962` | side feint, tail whip, landslide fronts, lightning rounds |
| `hz/full` + safe circle `#hzR0` (one circle) | `core:1251,1596-1612`, drawing `core:1487-1499` | — (one safe circle only; see N4) |
| volley groups `grp_new` / `grp_mark` (one hit per group) | `core:1813-1828`, `lib:222` | multi-point volleys (spikes, shells, waves) |
| telegraph-only hazard (dmg 0) | `core:1428-1429`, `lib:194-196` | lead lines |
| `hz_vis` module hook (#hzEv 0 create / 1 strike / 2 end) | `core:1352-1353,1509-1510,1432-1433`; module dispatch `fgcore:663-667` | fire fields on strike, kit visuals |
| `pj/launch` (sphere or **blade** `#pjShape 1`, walls, return, groups), `pj_end` hook | `core:1732-1812`, `lib:199-214` | water waves (blade), shells, icicles, meteors in flight |
| `pj/steer {max}` (homing, ±60° pitch) | `core:1829-1862`, `lib:217-219`; used by `bfwing:433-550` (B4, steer at `:513`) | icicles (쏟아지는 천화) |
| `mv/glide`, `mv/leap` (parabola), `mv/turn`, `mv/face`, `mv/step/toward/away`, `mv/clamp`, `mv/leash`, `mv/dist` | `core:2005-2162` | jump slam, charge, turning, distance bands |
| `pull/start` (undodgeable relocation) | `core:1937-2001` | not needed |
| `aux/*` (breakable helper objects) | `core:1003-1091` | not needed (proxies use the rigtech redirect) |
| `true_hit`, `true_pct` | `core:968-999` | tests |
| bars, `extra[]`, `sub[]`, under-bar; `line/say` | `core:1111-1131`, `1165-1218` | HUD |

**Existing (module templates).**

| helper | where |
|---|---|
| `Pattern` record: bands, weights, lead, recover, max_len | `fgapi:170-205` |
| `TL` per-tick timeline | `fgapi:423-474` |
| `lockp`/`lockb` + `keep` (no stale markers), `clamp_*`, `bstep`, `tag_last_hz`, `every` | `fgapi:288-345` |
| the kit re-exports (`g.fx`, `g.snd`, `g.tele_*`, `g.kcard`) | `fgapi:347-375` |
| expanding front (hz/ring + resize_s + `tele/wave` + band) | `fgfield:413-453` |
| bombs along a line, volley groups of 4 | `fgcruise:224-313` (C1) |
| rotating line hazards re-aimed per tick with `#hzRearm` + moving lanes `tele/mline` | `fgcruise:344-440` (C3) |
| late-lock missiles (lock the feet at +14, disc, tell 14) | `fgcruise:441-533` (C4) |
| walker bursts toward the player + thrown slabs (blade pj) | `fgapi:479-…` (`rocks`), `fgcruise:578-…` (C6) |
| projectiles on a fixed timetable (mv/glide + mv/leap), harmless until landing | `bfwing:245-347` (B2) |
| blade pj sweep | `bfhuman:528-529` (H4) |
| random-area eruptions | `fgfield:189-210` (F1) |
| Raiden: jumpable expanding annulus (shape 11) and the calamity disk with a safe dome | `rh:60-77`, `enc:66-70`, `enc:992-1030` (Raiden-only code, idea reference) |

**New helpers proposed (N-numbers used in the tables).**

| id | helper | level | sketch |
|---|---|---|---|
| N1 | runtime element on hazards / pj / decals | module | `scoreboard players operation #hzEl mb = #azE mb` (the option is a plain score; `hz_opts` only emits `set`, `lib:152-157`); kit decals called `with storage` holding `el`; presets dispatched per element by generated `execute if score #azLeg …` lines |
| N2 | kit palettes Pyro / Hydro / Cryo / Electro | az kit | today `tele/*` draws only 5 Geo, 9 violet, 0 physical; any other value draws Geo (`fg_fx_api.md` §4) |
| N3 | predictive lock `lockv {lead}` | module | keep the player body's position for the last 6 t in the module tick; marker at pos + velocity × lead, clamped to the walk disc (`lockp` + clamp, `fgapi:288-318`). "Chosen from the movement direction": back spikes, ice circles, burrow rockfall, electro lumps (`wiki.md:103-104,116-117,165-167,185-187`) |
| N4 | `hz/full` with several safe circles (kind 6 "mask") | framework | hit unless the player's feet are within `R0` of any marker `rlk_mb_hzsafe` whose `mbHzI` = the hazard id (horizontal test like Raiden's `dome_contains`, `enc:1024-1030`); drawing left to the kit (quiet). One hazard per lightning round instead of 10-16 discs |
| N5 | orbit mover | module | prop (`item_display`) + `hz/disc` (`#hzRearm 10`, `#hzAct` = life) re-aimed onto the prop every tick (`hz/aim`); angle advanced by ω per tick around a centre (the body or a fixed point) via `execute rotated <yaw> positioned ^ ^ ^r` |
| N6 | lingering field | module | `hz/disc` with `#hzAct` 120-200, `#hzRearm 10`, low coefficient, `#hzQuiet` + kit decal with `hold` = life; brand refresh through N2-hit events; global cap 6 (the oldest is cancelled with `hz/cancel`, `core:1700-1703`) |
| N7 | hit event + DoT helper + no-reaction option | framework | §3.4, §3.5 |
| N8 | local-frame classifier `u/zone` | module (or framework `mv/local`) | §5.1 |
| N9 | proxies + per-part state | framework + rig | `rigtech.md` §3.3; the module reads `#mbPart` (hit part) and toggles `px/state/*` |
| N10 | generalised front builder `wave(centre, r0, r1, spd, band, tell, dmg, nododge, el)` | module | from `fgfield:425-453`, so the landslide, jump slam, stomp and Hydro waves share one code path |

### 4.2 Phase 1 (Geo; `hz` element 5 = registry `el`)

Ticks are proposals scaled from the key sheets. Earlier bosses used about 75 % of footage wind-ups
(`S:mb3/plan.md` "-25 %"). Coefficients follow `chapter.md` §5.4.

| # | pattern (wiki) | footage | mapping | dodge |
|---|---|---|---|---|
| P1 | **갈라지는 봉인의 땅** (chin slam) | `motion/E_chin_keys_v2.jpg`: rear t+14..44, slam t+48; caption "타이밍에 맞춰 대시하면 회피됩니다" | `hz/line` from the head anchor forward (len 9, w 5) **or** `hz/sector r 8, a 40` at the nose; tell ≈ 36 t; coef 1.4; heavy KB; crack decals | dash (the wiki's "dodge once when the head comes down") |
| P2 | **바위 분쇄 충돌** (jump slam, two splits) | `motion/D_jump_keys_v2.jpg`: crouch 0-17, airborne 18-41, land 42-44, split 1 ≈ 44-46, split 2 ≈ 55-57 | `mv/leap` of the body to `lockb` (pulled into the body disc) + rig jump clip; proxies follow (rigtech `px/state/jump`); landing disc r 6 (tell = flight); **2 fronts** (N10) from the landing point, r 3 → 12, 11 t apart, `#hzY1` 0.7, dodgeable; coef 1.2 each; one volley group per front | dash twice, or jump |
| P3 | **바위 용왕의 돌진** (charge) | `motion/G_charge_keys_v3.jpg`: curl 0-31, launch 34 | pre-turn to the player (§5.2), then `hz/line` len 20, w 6 from the body (tell ≈ 26 t), the body `mv/glide` along it 12 t, clamped to the body disc; coef 1.8; only when the player is far in front | sidestep (the line is long, dash across) |
| P4 | **천동만상** (back spikes, 4 rocks) | `v1.md` §S: tell 15 t; markers 18 t before each landing; landings S+47/+53/+57/+64; planted rocks explode ≈ 40 t later; points on the boss→target line, 3.5-4.5 m apart | 4 marker discs r 1.8 (tell 18) at P1 = head + 3 b toward the target, P2 = `lockv` (N3, lead 10), P3/P4 = +4/+8 b beyond along the movement (or the boss→target line); spike props fall in 4 t (timetable like `bfwing:245-347`); landing hit coef 1.0; then the planted spike explodes: second `hz/disc` r 2.5 tell 40, coef 1.0; landings in one volley group, explosions in another | step off the line; dash the explosion |
| P5 | **산명곡응** (foot stomp, 3 waves) | `motion/K_stomp_keys_v3.jpg`: lift t−30, slam t+1, rings t+3..+40 | at the stomping paw (front or hind, the one the player crowds, §5.1): 3 fronts (N10) r 1.5 → 9, 10 t apart, `#hzY1` 0.7, coef 1.0, 3 volley groups; **repeatable** | dash the first or into the third (wiki); jumping works too (2 dash charges, 20 t regen, `F:load:801-804`) |
| P6 | **성동격서** (side feint) | `motion/H_feint_keys_v3.jpg`: sway t0-20, flank eruptions t+22-34 | two flank rectangles (`hz/line` along the body, offset ±(half width + 2.5), len 12, w 5, back 6) **`#hzNoDodge 1`**, coef 1.2; plus small dodgeable discs r 3 at the nose and tail root (the "little hit" front and back, coef 0.6); tell ≥ 20 t | **undodgeable**: leave the flank |
| P7 | **교활한 통수** (tail whip) | `motion/I_whip_keys_v3.jpg`: raise 0-25, sweep 29-36, eruptions 33-50 | a rotating `hz/line` (len = tail length 12, w 3) from the tail root, re-aimed every tick (`hz/aim`, as C3 `fgcruise:344-440`), sweeping ≈ 200° over 8 t on the side the player is on, **`#hzNoDodge 1`**, coef 1.6; eruption decals along the end line; tell ≥ 24 t (tail raise + `tele/mline` lane) | **undodgeable**: run with the tail or stay at the head (wiki) |
| P8 | **잠복 돌진** (burrow charge; phase 1 only) | `v2/k_f1002…k_f2412`: burrow ring markers ×6, two surfacings, rock shafts | dig 20 t, untargetable (`rlk_mb_inv`, proxies parked); rocks along the player's movement (N3; bombs-along-a-line template `fgcruise:224-313`, discs r 1.5 tell 14); 2 emerges: ring marker r 4 under `lockv` (tell 24), burst disc r 4 coef 1.6, body teleported there; the 2nd emerge comes from the arena centre straight at the target when the target is at the edge (`wiki.md:116-119`): a line from the centre (len to target + 4, w 5) | dash; sidestep the 2nd |
| T1 | **파멸의 산사태** | §2.3 | 6 fronts (N10), `#hzNoDodge 1`, `#hzY1` 0.7 | jump or leave r 18 |

### 4.3 Phase 2 (leg element; brands)

**Hydro (물):**

| pattern | wiki / footage | mapping |
|---|---|---|
| **격류 범람** (special; at phase-2 start, then a normal pattern with a cooldown ≥ 600 t) | orbs circle the boss, wide ring, multi-hit + brand; "정중앙을 제외하곤 어디든 피격될 수 있습니다" (`motion/N_roar_hydro_v4.jpg` caption "물방울") | N5: 6 orbs (prop: blue water sphere) on 2-3 circles (r 6, 10, 14), clockwise, ω 2-3°/t, each a `hz/disc r 1.6`, `#hzRearm 10`, coef 0.35 per touch, life 240 t; each orb its own volley group (so two orbs cannot double-hit in one tick); orbs fade at life end; brand |
| chin slam + water field on the dodge side | `motion/S_hydro_chin_jump_v4.jpg` caption "물줄기가 추가되어 피격 가능성이 높아집니다 / 범위는 랜덤한 위치에 표시됩니다" | after P1: 2 Hydro discs r 3 at random sides of the head (tell 16), coef 0.8 |
| jump slam + 8-direction water waves | wiki `:139-140`; caption "점프 — 물줄기가 추가되어…" | after P2's landing: 8 **blade pj** (`#pjShape 1`, `core:1799-1812`) from the landing point, yaw 0/45/…/315, hr 1.6 (reach hr + 0.65), speed 0.9 b/t, life 22 t, prop 0.9 b above the floor (so the lower sample row is at floor level), one volley group; coef 0.8 |
| stomp + 8-direction waves | wiki `:141`; caption "지진파" | same 8 blades from the paw after the 3rd ring |

**Pyro (불):**

| pattern | wiki / footage | mapping |
|---|---|---|
| **운석 낙하** (special at phase-2 start, then cooldown ≥ 600 t) | homing meteors near the boss; the first one cannot be shaken off; fire fields after (`wiki.md:144-146`; `motion/T_pyro_v5.jpg` "포효 - 운석: 운석이 떨어져 장판이 형성됩니다") | 5-6 meteors: each a decal disc r 2.5 whose hazard follows the player at ≤ 0.25 b/t (`hz/aim` per tick toward the player, tell 30-40 t; the first follows at full speed = cannot be shaken); falling prop over the last 6 t; strike coef 1.2; then a fire field (N6) r 2.5, 160 t; brand |
| **화염 잠식** (every pattern adds fire fields) | "where the brand lands a wide persistent Pyro field" (`wiki.md:147-150`); caption "불덩이 — 물과는 다르게 돌덩이가 튀어나와 장판을 형성합니다" | in the `hz_vis` strike event (`#hzEv 1`) of hazards flagged "leaves fire" (vis id class), spawn a field (N6) r 2.2-3 at the strike point (or at the player when the hit landed), 140-200 t, coef 0.25 per 10 t, brand refresh; cap 6 fields |

### 4.4 Phase 3 (tail element; brands; Cryo stacks)

**The burrow (service, §2.6):**

| element | pattern | mapping |
|---|---|---|
| Cryo | **서리 습격** (ice circles keep spawning, spikes from the centre after a few s; random or at the player with a bias to the movement direction; `wiki.md:165-168`, `v7.md` §D: circle r ≥ 4 m) | every 25-30 t a circle at `lockv` (N3, lead 15 t) or random (30 %): decal r 3.5 + `hz/disc r 3.5`, tell 40 t, coef 0.9, Cryo brand stack; at most 2 alive; the circle's fill makes the timing readable |
| Electro | **벼락 습격** (4 rounds; the safe spots shrink 5 → 4 → 3 → 2 groups; purple light marks the strike zones; the range expands at the end; `wiki.md:179-182`; `motion/O_tailburrow_mid_v6.jpg` shows rune circles and bolts) | 4 rounds every ≈ 60 t. **N4** mask hazard (`#hzNoDodge 1`, tell 30 t, coef 1.0): safe circles r 3.0 (round 4: r 2.5) at S = 5/4/3/2 points on rings r 6-14 around the burrow; at least one safe circle ≤ 8 b from the player at telegraph time (reachable: walk 0.22 b/t × 30 t + a dash); the kit draws the purple field plus clean green-rimmed safe circles (the framework's safe colour is index 10, `core:121-122`). Fallback without N4: one Raiden-style dome per safe circle (`enc:1024-1030`), or 10-16 strike discs on a grid minus the safe cells |

**Normal phase-3 additions** (on top of P1-P7 and the leg extras):

| pattern | wiki / footage | mapping |
|---|---|---|
| **쏟아지는 천화** (Cryo: ice sphere near the tail fires homing icicles, 5 volleys; boss keeps attacking; `wiki.md:169-173`; `motion/P_shells_cryo_v8.jpg` caption "다섯 번이나 유도 고드름이 발사되는 얼음 구체와 범위 내 얼음 조각이 내리는 장판") | sphere prop above the tail tip (8 b up); 5 volleys of 3 icicle pj (sphere hr 0.6, speed 0.9 b/t, life 40, **`pj/steer {max:4}`** for the first 14 t, `bfwing:433-550` template), one group per volley, coef 0.6; plus one hail field (N6) under the player at volley 3 |
| **번개의 가루** (Electro shells) | `v7.md` §A1: tail-up tell 30 t; 8 shells every 7 t to a hover cloud; 20 t later dives one by one every 7 t, each 8 t, r 2.5; homing in direction only; "keep sprinting" | 8 shell props → cloud (mv/glide) → dive: lock the player's feet at launch (`lockp`, C4 late-lock template `fgcruise:441-533`), `hz/disc r 2.5` tell 8 + the falling prop; coef 0.7; groups of 4 (at most 2 hits) |
| **천동만상 – 얼음 가시** (replaces P4) | ice field, Cryo damage after a delay, then hail keeps falling there (`wiki.md:174-176`) | P4's 4 points become Cryo discs r 3 (tell 30, coef 1.0, stack), each leaving a hail field (N6) r 3 for 120 t |
| **천동만상 – 번개 가시** (replaces P4) | `v7.md` §A2: flare 10 t, launch 12 t; 6-7 lumps; a hexagram r ≈ 5 under / ahead of the player ≥ 20 t before; a bolt 2-3 t before each lump; "dash when it sticks" | 6 lumps: per lump a decal hexagram r 5 at `lockv` (N3) + the strike `hz/disc r 3.5` tell 20 (bolt fx at tell − 3), spacing 10 t ×4 then 30 t; coef 1.0 each, its own group; caption-faithful counter = a dash on the bolt |
| 교활한 통수 + trail (P7, phase 3) | `v7.md` §B: tail raised ≥ 40 t (arcs at −28 t), whip 2 t, bolts +1, crystal waves +2..+10 and +16..+26, a field strip ≥ 60 t that brands; caption "꼬리공격이 강화됩니다" | P7 + 2 waves of dodgeable discs along the end line (r 1.5, tells 10 / 24) + a strip field: `hz/line` len 12, w 4, `#hzAct` 80, `#hzRearm 10`, coef 0.25 + brand |

### 4.5 Dodge, undodgeable and fairness rules

- **How i-frames work.**
  - `player/dash_go` sets `dashInvT 6` (0.3 s) (`F:player/dash_go.mcfunction:4`). `player/take_damage` returns at once
    with `#dodged 1` while `dashInvT ≥ 1` (`F:player/take_damage.mcfunction:3-6`, `F:player/dash_iframe.mcfunction:1-3`).
  - Charges regenerate every 20 t, with 5 t between dashes (`F:load:801-804`).
  - The burst also gives i-frames (`#burstInv 8`, `F:char/burst_wind.mcfunction:6-7`, `F:load:725`); so does a fall
    rescue (20 t, `F:room/fall/player.mcfunction:14`).
  - A dodged framework hazard is spent too (one hit per hazard, `core:1614-1617`). A dodged member of a volley group does
    not disarm the group (`core:1627`, `:1873`).
- **`#hzNoDodge`.** `hz/hurt` sets `#mbNoDodge` (`core:1623`). `mboss/hurt` then calls `hurt_nd`, which zeroes
  `dashInvT` for that one hit and restores it (`core:950-962`). There is no pj equivalent: projectiles are always
  dodgeable (`core:1863-1878`).
- **Azhdaha's undodgeable set:**
  - P6 feint (flanks only), P7 whip, T1 landslide fronts (jumpable);
  - 벼락 습격 rounds (stand in a safe circle);
  - the brand DoT (not a hit);
  - fire / hail / strip fields (lingering; dodging them makes no sense).
- **Telegraph floors.** Every damaging hit has ≥ 10 t of readable telegraph (`S:mb3/fg_contract.md:157-158`, checked by
  `test_fieldgen.py` §9). For Azhdaha: ≥ 12 t for dodgeable hits, **≥ 20 t for undodgeable side hits**, with a dedicated
  side decal (red-amber flank lanes), and the first side punishment of the fight types "옆구리는 위험합니다 — 머리나
  꼬리 쪽으로".
- **Hit volume.** The hazard test uses the player's feet only, inside a height band (`core:1530-1538`). Overhead parts of
  the dragon never hit by themselves. Every hit is a ground hazard or a projectile. That is consistent and readable.
- **Knockback.** Hazard knockback goes away from the hazard origin or along the aim (`core:1294-1297`, `kb_src`
  `core:963-967`). Flank hits should push outward (origin = the body), never under the body.

---------------------------------------------------------------------------------------------------

## 5. Targeting a huge boss

### 5.1 Local frame and zones (N8)

- Projection, as `hz/hit` does it (`core:1541-1553` forward, `:1587-1592` side):
  - the body forward unit ×1000 from a temporary marker at `^ ^ ^1` (`core:1342-1350`), or from the yaw with the stored
    cosine table (`core:120,135`);
  - player offset `(dx, dz)` in milliblocks;
  - `f = (dx·fx + dz·fz)/1000`, `s = (dx·fz − dz·fx)/1000`.

  It costs about 25 commands, once per decision and once per 10 t for the HUD/turn logic.
- Zones (blocks; scale them with the rig's rest anchors, read as `fgapi:158-162` does):

| zone | condition | meaning |
|---|---|---|
| HEAD | f ≥ 4.5 and \|s\| ≤ 4 + 0.6 (f − 4.5) | in front of the chest / head (the recommended spot) |
| FLANK | \|s\| ≥ 2.6, −5 ≤ f < 4.5 | 옆구리 (punished) |
| TAIL | f < −5 | behind the hips / along the tail (the other recommended spot) |
| UNDER | \|s\| < 2.6, −5 ≤ f < 4.5 | under the belly between the legs |
| near paw k | horizontal distance to paw k ≤ 2.8 | stomp trigger (front-left, front-right, hind-left, hind-right) |
| band | `mv/dist` (`core:2144-2162`) from the anchor: near ≤ 9, mid 9-15, far > 15 | jump / charge / specials |

- With proxies on the bones (rigtech §3.3), the part that was hit (`#mbPart`) is a second signal for "where the player
  fights from". Weight it lightly (last 3 s) so a ranged player at the flank is still read correctly from position.

### 5.2 Turning and movement

- The boss turns slowly. The field generator tracks at 4°/t at idle (`fgcore:45,473`, `mv/turn` `core:2083-2102`).
  Azhdaha:
  - **small correction**: ≤ 3°/t while |Δyaw| ≤ 50°;
  - **turn step**: |Δyaw| > 50° at idle → a 90° turn clip in 12 t (7.5°/t) with foot thuds (v1: "lifts its near forepaw
    and turns ≈ 60-90° toward the player" in ≈ 0.6 s, `v1.md` §S);
  - moving the whole-body yaw on the anchor with `teleport_duration` keeps the rig cheap (rigtech TL;DR 5).
- **Front patterns** (P1, P3, P2 aim): a pre-turn lead of up to 10 t (`Pattern.lead`, `fgapi:181-182`), then the aim is
  locked at the wind-up start.
- **Side and tail patterns** (P6, P7): no turn. Being at the side is the trigger.
- **Area patterns** (P4, shells, icicles, specials): no turn needed. The rig plays a head-track clip
  (`face/track` exists in earlier rigs).
- **Anti-stall.** The player stays in TAIL for ≥ 3 decisions without a whip → a 180° turn-around step, then front
  patterns.
- **Locomotion.** Mostly stationary.
  - Walk 0.1 b/t toward the player when the player is > 15 b away and no far pattern was picked (`bstep toward`,
    `fgapi:320-325`).
  - Never back off. The body stays in a body disc r ≈ 8-10 around the arena centre (`fgcore:279-282` leash template), so
    the 13-b tail still clears the arena's walk radius 28 (`chapter.md` §4.3).
  - Jump and charge destinations are clamped to that disc (`lockb`, `clamp_body`).

### 5.3 Pattern choice

Decision at each pattern boundary (`ai/next`, template `fgcore:492-508`):

```
test request > lock > transition queued (#azTr 1) > burrow sequence > specials due (forced at phase start) >
FLANK side rule (90 %: feint / whip) > weighted pick by zone and band, no immediate repeat except P2 / P5
```

Weights per zone (phase 1; 0 = never):

| pattern | HEAD near | HEAD mid/far | FLANK (the other 10 %) | TAIL | UNDER / near paw | notes |
|---|---|---|---|---|---|---|
| P1 chin slam | 4 | 1 (mid only) | 0 | 0 | 1 (front paws) | front only |
| P2 jump slam | 1 | 3 | 1 | 2 | 1 | may repeat; a repeat is drawn at half weight ("rarely repeats") |
| P3 charge | 0 | 4 (far only) | 0 | 0 | 0 | front + far |
| P4 back spikes | 2 | 3 | 2 | 2 | 1 | any |
| P5 stomp | 1 (front paws) | 0 | 2 (paw ≤ 2.8 b) | 2 (hind paws) | 5 | may repeat |
| P6 side feint | 0 | 0 | rule | 0 | 0 | FLANK rule only |
| P7 tail whip | 0 | 0 | rule | 4 | 0 | FLANK rule + TAIL |
| P8 burrow charge | 1 | 2 | 0 | 1 | 0 | phase 1; cooldown ≥ 600 t |

- **FLANK rule.** `random 0..99 < 90` → P6 or P7 (weights 5 : 4, never the same one twice in a row); else the table.
  The wiki gives "~90 %" for the feint; the whip "comes when someone is at the side" (`wiki.md:109-115`).
- **Phase 2.** The leg special (격류 범람 / 운석 낙하) joins every zone with weight 2, cooldown 600 t (forced once at
  phase start). P8 leaves (`wiki.md:117-118`).
- **Phase 3.** Shells / icicles join HEAD mid/far, TAIL and FLANK-10 % with weight 3, cooldown 400 t. P4 becomes its tail
  variant.
- **No immediate repeat.** `unless score #azLast matches <id>` on every candidate line except P2 and P5 (the field
  generator writes it for all, `fgcore:546-549`). A bag is not needed; the original is weighted random by position. Keep
  the `cand_any` and first-pattern fallbacks (`fgcore:575-583`).
- **Recover.** After each pattern 16-28 t (heavy ones longer). The specials add 30 t.

### 5.4 Size-specific notes

- Melee reach is measured to entity positions, not hitboxes (`F:combat/find_immediate.mcfunction:60-62`). The single
  click shield is sized by the registry `hit` (`F:mob/shield_ensure.mcfunction:20`, `core:492-495`). Hits on the head and
  tail therefore need the proxies (rigtech §3.3, `chapter.md` R8). The burrow needs tail-only proxies (§2.6).
- Hazards are anchored at rig anchors (nose, paws, tail root, tail tip), computed `^s ^ ^f` from the body yaw. Moving
  parts (the jump, the whip) take their anchors from the clip's per-tick track (rigtech §3.3 "proxy track").
- Players can walk through the body (no collision, rigtech §3.6). UNDER is therefore a real zone; the stomp covers it.

---------------------------------------------------------------------------------------------------

## 6. Risks and open questions

**Q1 RES timing.** Flat table from entry (the user's "final table") or raised on absorb (original)? Recommendation: flat;
the switch `RES_BY_PHASE` is in §1.4.

**Q2 Brand strength and counterplay.**
- Proposed: 4 s brand, 4 × 3 % non-lethal DoT, shield blocks, 8 % heal cleanse.
- The **응결 결정** shards are a new mechanic (not in Genshin) and need the user's approval.
- Alternatives: lethal DoT; the DoT only while no shield at each tick; a dash-cleanse.
- Tune with the fairness simulator once N7 exists (`S:mb3/review/fairness/sim/fgfair.py`; its agent must learn zones and
  shard pickup).

**Q3 Player-side reactions.** Recommendation: skip them for Azhdaha's hits (`#mbNoRx`, §3.5). Otherwise 물/얼음 can Freeze
the player in place and 불/얼음 Melts the hits ×1.5-2.

**Q4 Lethality.** Should the landslide's six heavy fronts be able to kill a full-HP Lv5 player? `chapter.md` §5.4
estimates ≈ 140 damage for 6 hits vs 148 HP. They are jumpable and avoidable by distance, so recommended yes. The brand
DoT: no.

**Q5 Undodgeable side patterns.** In shoulder view with a 20-b body the player may not see that they are at the flank.

Mitigations:
- ≥ 20 t tell;
- flank-lane decals;
- the first-time hint;
- the 10 % non-side fallback;
- the anti-stall turn.

Watch out for an unwanted case: a player who just landed from the jump slam on the flank must get one dodgeable pattern
first. Proposal: the FLANK rule is skipped on the first decision after P2 / P3 / P8 moved the body.

**Q6 Runtime elements vs baked generators.** Element per hazard, kit decal colour, presets and rig looks are runtime
choices.
- Options: `operation` for `#hzEl` / `#pjEl` (N1), macro decals `with storage`, and 2 × 2 preset families.
- More files; the kit card budgets (64 fx / 40 telegraph cards, `fg_fx_api.md` §1, measured §11) must be checked per
  element. Water orbs + fire fields + spikes at once is the worst case.
- A separate az kit means a third near-identical kit generator; "one shared engine" (`fg_fx_api.md` §13) is overdue.

**Q7 Proxies and dedupe.** These are shared-file changes:
- a redirect line in `combat/apply`;
- `#atkSeq` in `melee_begin`, `clear_atkflags`, `element/core_*`, `element/dot` (rigtech §3.3).

All earlier bosses must stay byte-identical in their module outputs (`S:mb3/tests/ident.py`). The per-swing dedupe can
eat a legitimate hit in the same tick (lost hit, never a double hit).

**Q8 Element of the second landslide.** Geo or the leg element (with a brand)? The wiki is silent. Propose: the leg
element, coefficient 0.9.

**Q9 Transition order details.**
- Confirm from v4-v6 notes (pending) that before phase 3 the phase-2 special comes before the landslide (`wiki.md:122`).
- Confirm how long the original waits between the message and the first front (≈ 20 t in `motion/L_slide_keys_v4.jpg`).

**Q10 Burrow length.** Genshin ≈ 26 s (`motion/O_tailburrow_*_v6.jpg`). Proposed 12-16 s. The tail damage window and the
1-HP clamp must not stall a strong player for long (a "마지막 일격!" cue after surfacing).

**Q11 Hydro orbs.**
- "Usually clockwise; some spots are hit and some are not; watch the angle" plus "anywhere except the exact centre"
  needs the v4 notes for radii, count and speed.
- Multi-hit per orb is capped by `#hzRearm 10` per orb.
- Several orbs crossing the player in one tick: one hit (each orb is its own volley group, `core:1813-1828`, but then
  different orbs can each hit). Decide whether all orbs share one group with `#hzRearm` (at most one hit per 10 t
  overall, the C3 approach `S:mb3/fg_contract.md:191-194`). Recommended: share.

**Q12 Meteors.** "First a meteor that cannot be shaken off falls near the boss" is ambiguous. Proposed: the first decal
follows the player at full speed until 6 t before impact (only a dash or a shield helps); the rest follow at 0.25 b/t.

**Q13 Lightning-round geometry.** The safe-group layout (5 → 4 → 3 → 2) and "the range expands at the end" need the v6
notes. N4 (the mask hazard) is a new framework kind and needs tests (hit unless inside any safe circle; volley groups;
the drawing is the kit's).

**Q14 Arena.** Walk r 28, body disc r 8-10 and front ranges up to 20 b (charge) must keep a safe ring at the edge.
Landslide fronts end at r 16-18 so "move away" works. The jump-slam landing clamp must keep the 13-b tail inside the wall.

**Q15 Timings not yet confirmed.** Chin slam, jump, charge, stomp, feint and whip wind-ups come from the motion key sheets
only. Hydro waves, meteors, icicles, the ice spikes variant and the lightning rounds await v2-v6, v8, v9. Every number
in §4 is a proposal until those notes land.

**Q16 Pair display timing.** Roll at the boss map (entry) or one map earlier so the player can shop for shields and heals?
Recommendation: show it earlier if the user agrees; the binding text says "on entry".

**Q17 Reload safety.** Brand, shards, fields, orbs and the tail-only state must be re-derived or cleared on `/reload`.
Every aux entity dies on reload (`core:174-176`). The module `reload` hook re-derives phase, looks and proxies from
scores, as the field generator does (`fgcore:376-406`). Brand clocks (scores) survive; the shards (`item` entities tagged
`rlk_mb_aux`) are killed. Accept that.

**Q18 Dependencies.** `#mbHealAmt` lives only in the uncommitted `wip/bf2` tree (`bf2:` core:410-425). The chapter mode
(`chapter.md` R1-R16), the proxies (rigtech) and the multi-arena constants (`chapter.md` R3) are prerequisites. N4 and N7
are new framework code. Plan them with the chapter-mode change, not inside the module.
