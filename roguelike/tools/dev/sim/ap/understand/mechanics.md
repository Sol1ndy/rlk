# 아펩의 오아시스 파수꾼 (Apep Warden): mechanics and pattern-mapping study

Read-only study. Nothing in the repo or in any worktree was changed. Outputs: this file, the calculator
`S:ap/understand/mechanics_work/calc_ap.py` (all numbers in §1-§3 come from it) and committed copies of the framework
files cited below (`S:ap/understand/mechanics_work/fg_*.py`, extracted with `git show fde9db7:...`, because the `wip/fg`
worktree has uncommitted edits by another workflow).

Inputs: `S:ap/src/wiki.md` (binding), the screenshots `S:ap/src/img/11-15`, the video notes that exist
(`S:ap/understand/v1.md`, `v2.md`, `v4.md`, `model.md`), the motion key sheets `S:ap/understand/motion/kp01-kp17`, the raw
caption crops of v3/v5 (`S:ap/understand/v3/captions_all.jpg`, `v3/keys/*`, `v5/caption_texts*.jpg`; their `.md` notes
were not written yet), the framework (`wip/fg`), the shared datapack (main line), the earlier studies, and the sister
studies for Azhdaha (`S:az/understand/mechanics.md`, `chapter.md`). Timings that are cited only from a key sheet are
proposals until the v3/v5/v6 notes land.

## Path shorthand

| short | meaning |
|---|---|
| `S:` | `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad` |
| `DP` | `/home/user/rlk/roguelike` (main line, `7a6dc4f`) |
| `FG` | `S:mb3/wt_fg/roguelike` (branch `wip/fg`, committed `fde9db7`; the working tree has uncommitted edits) |
| `F:x/y` | `DP/data/rlk/function/x/y.mcfunction` |
| `core:N` | `build_mboss_core.py` at `fde9db7` = `S:ap/understand/mechanics_work/fg_build_mboss_core.py`. The working tree adds 2 lines in `world` (≈ 812), so working-tree lines after 812 are N + 2 |
| `lib:N` `bb:N` | `FG/tools/mboss_lib.py`, `FG/tools/build_bossbar.py` (committed copies `fg_mboss_lib.py`, `fg_build_bossbar.py`) |
| `fgapi:N` `fgcore:N` `fgcruise:N` `fgfield:N` | `FG/tools/mboss_fieldgen/{api,core,cruise,field}.py` at `fde9db7` (copies `fg_api.py` …) |
| `bfwing:N` `bfcore:N` `gdcore:N` | `DP/tools/mboss_butterfly/{wing,core}.py`, `DP/tools/mboss_guardian/core.py` |
| `enc:N` `cin:N` | `DP/tools/build_raiden_encounter.py`, `DP/tools/build_raiden_cinematic.py` |
| `AZM` `CH` `MD` | `S:az/understand/mechanics.md`, `S:az/understand/chapter.md`, `S:ap/understand/model.md` |
| `v1 §A` … | `S:ap/understand/v1.md` section A (likewise v2, v4); `kpNN` = `S:ap/understand/motion/kpNN_*.jpg` |
| `t` / `b` / `‱` | ticks (20/s) / blocks / basis points (1/10000) |

Body frame (phase 1, from the rig rest pose `MD` §9.3, rig −z = forward): `f` = along the facing from the thorax
centre (the husk), `s` = sideways. Hood front f ≈ +2.6, front hands (±2.5, +3.7), arm claws (±5.3, +2.6), rear feet
(±3.0, −2.9), tail root f −2.4, tail on the ground f −4.5 … −9.9. Phase 3 is an upright naga, hood 8.5 b up
(`MD` §1.2), leaf hands spread to ±3.8 b.

---------------------------------------------------------------------------------------------------

## 0. Short answers

1. **RES.** The body gets a per-hit `mres` in the module **`on_hit` hook** (`F:combat/apply:23`, before the RES step of
   `apply_mods:13-14`): 30 when `#elem` is 7 (Dendro), else 10. Reactions and DoTs carry their own `#elem`, so they are
   covered. The organisms are framework aux husks. `on_hit` is never called for them (`apply:23` is body-only), so they
   spawn with `#auxRes 10` (`core:237,1075`). Their `aux_hit` hook turns ×0.90 into ×0.80 for Dendro (×8/9), the same
   trick as the Guardian's star resist (`gdcore:252,1162-1168`). "Can't be damaged" is a module branch in `aux_hit`
   (`#dmg 0`, `#mbAuxDone 1`, the "면역" popup `core:1040-1043`). It is not a RES number: `combat/res` never goes below
   1 damage (`F:combat/res:11`).
2. **Phases.**
   - HP: the registry pool (hp 320 at L18 = 7984) is split 53/47 like Genshin (4231 / 3753).
   - Phase 1 runs on the 4231 pool with a **1 % floor (42 HP)** in the module `incoming` hook (Raiden precedent
     `enc:577-597`).
   - Phase 2 is the Heart stage. The boss is underground and untargetable (`rlk_mb_inv`, `F:combat/apply:17`).
   - Phase 3 **re-pools** the body to 3753 with a title swap.
3. **Phase 2 for one player.**
   - The Heart is a module objective: marker + 3 displays + a progress score in ‱. It is not `rlk_mob`.
   - The Genshin numbers are kept: start 2700, basic kill +175, other kills +1100, hit −60 (−120 buffed), 파괴 blast
     −1400.
   - Organisms: framework aux husks with module AI and small display rigs. HP is 2-4 % of the boss pool per kind,
     waves of 4 basics + 1 special, at most 8 alive. The time-out at 75 s spawns 파괴.
   - Stage length ≈ 5-6 waves, 75-95 s.
   - Organisms hit the Heart through **module events**: melee timers, and ranged bolts as framework pj whose life ends
     at the Heart. A player standing in the path takes the bolt instead. No framework "victim" option is needed.
   - **0 % = a two-strike rule** (recommended): the first failure withers the Heart (big non-lethal hit, progress back
     to 27 %, waves restart); the second is a real defeat through the death path.
   - HUD: the 3 framework bars, with the name swapped to 「오아시스의 심장」 and the bossui bar showing the progress.
   - The 2→3 cut-scene: about 170 t behind a white-out, with the arena look swap.
4. **Phase 3, 종말의 여파.**
   - A Dendro field front spreads from the boss over the whole arena (field ticks outside the domes).
   - **3 domes** (r 3.5 b; v5 shows three) appear with light-pillar tells.
   - About 105 t after the field starts, a blast hits everyone **outside every dome**: 80 % max HP, dash i-frames do
     not help, lethal below 80 %.
   - Domes are markers plus a translucent hemisphere display. The check is a horizontal-distance test against each dome
     (Raiden `dome_contains`, `enc:1023-1035`), or Azhdaha's proposed multi-safe "mask" hazard (`AZM` N4) if that lands
     first.
   - It repeats: first about 10 s into phase 3, then on a 45 s cooldown.
5. **Patterns.** Every phase-1 and phase-3 pattern maps onto existing helpers: `hz/disc|ring|sector|line`, `hz/aim`
   re-aimed sweeps, `hz/resize_s` fronts, `#hzAct` windows, volley groups, `pj` with `pj/steer`, `mv/glide`,
   `rlk_mb_inv` burrows and the fieldgen `lockp/lockb/keep`. New pieces:
   - **`#pjNoDodge`** (4 framework lines) for the "undodgeable homing" thorn wheels;
   - the predictive lock `lockv` (`AZM` N3);
   - the dome check;
   - the Heart and organism AI;
   - nesting walls made of barrier blocks;
   - the body-frame classifier (`AZM` N8);
   - hit proxies (`CH` R8);
   - the shared chapter helpers: floor, title swap, bossui colour.
6. **Targeting.**
   - Body-frame zones FRONT / SIDE / UNDER / BACK plus range bands near ≤ 7.5, mid ≤ 14, far.
   - BACK triggers 생명의 꼬리 75 % of the time (wiki: "used when the player is behind it").
   - Slow tracking at 3°/t, with a 90° crab-turn step; front patterns pre-turn.
   - Weighted pick with no immediate repeat (fieldgen template `fgcore:492-589`).
   - Phase 3 has no back rule.
7. **Routing.** As in `CH` §2.2: chapter 3 → `apep`, L18. **Correction to `CH` §4.4:** phase 2 is played on the same
   lake field (`MD` §0; v3/v4 show the Heart on the grass). The golden cave only appears in the w2 cut-scene, so Apep
   needs no second arena and no mid-fight `mboss/ar/switch`.
8. **Main risks.**
   - Which entity the 양육 immunity belongs to: the binding text versus the footage, Q1.
   - The failure rule.
   - The lethality of 종말의 여파.
   - The barrier-block walls and their cleanup.
   - True damage on aux husks pays kill rewards (§2.6 pitfall).
   - Proxies for the 14 b and 8.5 b bodies.
   - Timings still unconfirmed for phase 3.

---------------------------------------------------------------------------------------------------

## 1. Resistances

### 1.1 The binding table and what the footage adds

| entity | Dendro | Physical, Pyro, Hydro, Anemo, Electro, Cryo, Geo | source |
|---|---|---|---|
| Warden, phases 1 and 3 | **30** | 10 | `wiki.md:16-19` (user follow-up "풀내성은 본체 30%"; the table's 70 is overridden), `img/11.png` |
| phase-2 organisms (all 6 kinds) | **20** | 10 | `wiki.md:17-18` ("따까리 20%"; the table's 50 is overridden), `img/14.png` |
| 양육 "buffed" state | — | — | `wiki.md:18-19`: a mechanic, "buffed organisms can't be damaged" (§2.5.6, Q1) |

- `#elem` 8 (Ronova's Void) is "other", so 10.
- The user's rule replaces the earlier bosses' "no RES at all" rule (`S:mb2/bf_contract.md` "never read `#elem`",
  `S:mb3/fg_contract.md:155-156`). That rule was a per-boss user decision (`CH` R7) and does not bind here.

### 1.2 How per-entity RES is expressed today

- **One `mres` score per entity**, a framework objective (`core:85` `OBJECTIVES`). `combat/apply_mods` applies it
  through `combat/res` when it is non-zero (`F:combat/apply_mods:13-14`).
- `F:combat/res:1-11` is the Genshin formula:

  | R | result |
  |---|---|
  | < 0 | ×(100 − R/2)/100 |
  | 0-75 | ×(100 − R)/100 |
  | > 75 | ×100/(100 + 4R) |

  The result is **at least 1**. So RES 10 = ×0.90, 20 = ×0.80, 30 = ×0.70.
- The body starts at `mres 0` (`core:482`). Aux objects get `mres = #auxRes` at spawn (`core:1052,1075`; option reset at
  `core:237`).
- The hit path on the body (`F:combat/apply`):

  | line | step |
  |---|---|
  | 16-17 | dying / `rlk_mb_inv` refusal |
  | 21 | element and reactions (`#elem` = the reaction's element for transformative damage) |
  | **23** | **module `on_hit` (body only, `tag=rlk_mb_body`)** |
  | 25 | `apply_mods` (level factor, then RES, then module `incoming` at `apply_mods:18`) |
  | 27 | **aux objects leave to `mboss/aux_hit` after `apply_mods`** |
  | 64-82 | the HP subtraction and the kill path |

### 1.3 Body: the module `on_hit` hook

```
# Hook on_hit (@s = body inside combat/apply, before apply_mods; #elem #tfm #rx known). User table: Dendro 30, others 10.
scoreboard players set @s mres 10
execute if score #elem tmp matches 7 run scoreboard players set @s mres 30
```

- Reactions and DoTs re-enter `combat/apply` with `#elem` = the reaction element (`F:element/aoe_hit:3`,
  `F:element/dot:1-9`; see `AZM` §1.4), so they are covered.
- True damage (`test/kill`, `core:2219-2229`) skips both `on_hit` and RES.
- Who it touches in our game: Nefer's default element is Dendro (`F:combat/find_immediate:43`,
  `F:char/melee/extra:17`), and so are some item procs (`F:items/proc/case_hit1:6`, `skandha_hit:9`). A Nefer player
  deals ×0.70 instead of ×0.90: the phase-1 kill takes 145 s instead of 113 s at sword pace (`calc_ap.py`). That is the
  intended counter-pick pressure; mention it on the gate label.
- **HUD:** the gate label (`CH` R2) prints "내성: 풀 30% · 그 외 10%"; nothing on the bar.

### 1.4 Organisms (aux husks): spawn RES 10, Dendro correction in `aux_hit`

`on_hit` is never called for aux husks (`apply:23` is body-only). Widening that line to `rlk_mb_hit` would also call the
Guardian's `on_hit` for its stars, a behaviour change in a finished boss. So:

```
# spawn: scoreboard players set #auxRes mb 10   (before function rlk:mboss/aux/spawn)
# Hook aux_hit (@s = organism; #dmg already x0.90 from mres 10): Dendro 20 = x8/9 more, at least 1.
execute if score #elem tmp matches 7 if score #dmg tmp matches 1.. run function rlk:mboss/apep/org/res_dendro
#   res_dendro: #dmg *= 8; #dmg /= 9; ..0 -> 1
```

- This is the Guardian's precedent: `star/resist` scales `#dmg` inside `aux_hit` (`gdcore:252,1162-1168`).
- Rounding error: at most 1 point (100 → 90 → 80; 7 → 6 → 5).
- The same hook also handles:
  - the 수호 shield pool (§2.5.2);
  - the 양육 immunity (§2.5.6);
  - kill bookkeeping, through `rlk_mb_broken` (`core:1044-1048`), which the module reads in its tick.

---------------------------------------------------------------------------------------------------

## 2. Phase 1 → phase 2 (소생 단계) for one player

### 2.1 HP layout and the 1 % floor

| quantity | value (hp 320, L18; `calc_ap.py`) | how |
|---|---|---|
| registry pool | 7984 | `F:mob/level_apply` via `body_setup` (`core:469-483`); level L18 = `(3 − 1) × 6 + 5 + 1` (`F:room/mob_init:35-40`, `#mapIdx 5`) |
| phase 1 / phase 3 | **4231 / 3753** (53 / 47 %) | Genshin 667,805 / 593,605 = 52.9 / 47.1 % (`img/11.png`) |
| phase-1 floor | 1 % of 4231 = **42 HP** | wiki "Hp가 1퍼센트 미만이 되면" (`img/13.webp`) |

- At spawn the module stores `#apTot = mhpM` and `#apP3 = #apTot × 47 / 100`, then sets
  `mhpM = mhpC = #apTot − #apP3`.
- The bar therefore shows the phase-1 pool full. Phase 3 shows a fresh full bar (§3.1), like the separate Genshin bars.
- `#apTot` also sizes the organisms (§2.5), so they never depend on which pool the body holds.
- **Floor clamp** in the module `incoming` hook (`F:combat/apply_mods:18`, after RES, before the subtraction at
  `F:combat/apply:64-66`). The Raiden template is `enc:577-597` (floor 55 %, `threshold` sets `#dmg = mhpC − floor`).
  Use the generic `mboss/floor` that `CH` R6 proposes for Azhdaha if it lands first.
- Reaching the floor sets `#apTr 1`. At the next decision point (`ai/next`, template `fgcore:492-508`) the transition
  service runs instead of a pick. A running pattern is not cut: it ends at its `release` (`fgapi:276-280`).
- At the floor `combat/apply` prints 0. Add a module popup at most once per 10 t (like the "면역" popup
  `core:1040-1043`).
- `test/level` re-runs `level_apply` (`core:2248-2255`) and resets `mhpM`. The module `test` hook must re-split the pool
  (Q17).

### 2.2 Transition sequence (service `T1`, ≈ 140 t; footage: v1 §A dive/sink, v2 §H, `kp08`)

| t | event | footage | implementation |
|---|---|---|---|
| 0 | typed line + sub-line "종막 오아시스 파수꾼이 땅속으로 숨어듭니다…" | the sink itself is cut out of v2 (v2 §0, 34.63 s cross-fade) | `line/say` (`core:1165-1180`) |
| 0-6 | rear (the same tell as 잠복 돌진) | v1 §A A+0…+5 | rig clip `dive` |
| 6 | untargetable; proxies off; leash off | — | `tag rlk_mb_inv` (`F:combat/apply:17`, no click shield `F:mob/shield_ensure:6`), `#mbNoLeash 1` (`core:891`), `px/state/burrowed` (rigtech, `CH` R8) |
| 6-30 | dive and sink into the dark pool; body to the arena centre (hidden) | v1 §A A+5…+29 | pool decal (kit), rig sink + parts at scale 0 (`MD` §9.2 "Burrow"), `tp` to the arena marker |
| 30-90 | the Heart is lowered from the canopy by a vine "hand" | v2 §H 35.4-38.3 s (≈ 58 t) | Heart prop at y + 14 → y + 3, `teleport_duration` steps; vine-hand prop |
| 90-96 | the egg drops into the root nest | v2 39.0-39.2 s | 6-t fall, squash (scale 1 → 1.15 × 0.85 → 1, `MD` §11) |
| 96-106 | vertical green-gold light beam | v2 39.2-39.7 s | kit `end_rod` column + flash |
| 100 | HUD swap: name 「오아시스의 심장」; the bossui bar ramps 0 → 27 % over 10 t | v2 39.47 s | §2.8 |
| 102 | message "마물을 처치해서 소생 진행도를 올리세요" | v2 39.62 s | sub-line + actionbar |
| 110-130 | wave-1 spawn markers (pale wireframe domes) | v2 40.0 s (`k_f2418`) | kit decal, 20 t |
| 130 | wave 1 emerges; the stage clock starts | — | §2.4 |

- Phase-1 hazards and props still alive at t0 finish normally. At t6 any phase-1 leftover is cleared with the
  framework's `lib_clear` set (`core:918-925`: `rlk_mb_hz`, `rlk_mb_hzfx`, `rlk_mb_pj`, pull, mv), so nothing hangs
  into phase 2.
- **The body stays alive and keeps `rlk_zmob`.** The zone cannot clear (`core:464`, `F:room/combat_clear`).
- The body stays the bar carrier, because `bars` runs as the body (`core:830`).

### 2.3 The Heart of the Oasis (objective entity)

**Model.** One prop with 3 displays (`MD` §5):
- `heart_bulb`: a translucent lemon seed, 2.0 × 2.6 b, leaning 65°;
- `heart_cradle`: 5 roots, top 3.0 b;
- `heart_tips`: 5 glowing sprout cards at brightness 15, up to 3.8 b;
- a gold swirl ring decal r 3 on the ground (always on in phase 2);
- a marker `rlk_mb_ap_heart`, tags `rlk_room rlk_mb_aux`, at the arena centre.

It is **not** `rlk_mob`, so the player cannot hit it.

| item | value |
|---|---|
| progress | `#apHt mb` in ‱ (basis points, so 17.5 ‰ is an integer) |
| start | 2700 (wiki ~27 %, v2 measured ≈ 25 %) |
| win | ≥ 10000 → the cut-scene (§2.9) |
| fail | ≤ 0 (§2.7) |
| basic kill | +175 (wiki 1.75 %; v4 measured +1.9 %) |
| any other kill | +1100 (wiki 11 %; v4 measured +11.9 %) |
| basic hit on the Heart | −60 (wiki 0.6 %; v4 −0.5 / −0.7) |
| buffed basic hit | −120 |
| 파괴 blast | −1400 (wiki 14 %; v4 −13.6 %) |

- A hit is a **module event**, not a hazard. `hz/hit` only ever tests the player's body (`core:1530-1566`), and
  `CH` R10's `#hzVictim` proposal is not needed. A melee basic subtracts at its strike tick. A ranged basic's bolt
  subtracts when its pj life ends at the Heart (`pj_end` event 2, `core:1879-1903`).
- **Feedback:**
  - a loss flinches the bulb (red-gold motes, `block.amethyst_block.hit` at a low pitch);
  - a gain sparkles it (a chime whose pitch rises with progress; `v4` §5 suggests `block.amethyst_block.chime`);
  - the bossui trail shows recent losses by itself (`bb:1-25` "white recent-damage trail").
- **Reload.** `#apHt` and the stage scores survive (scores). Every display dies (`core:175`); the module `reload` hook
  rebuilds the Heart from scores.

### 2.4 Waves, spawns, cap, time-out

| wave | content | starts when |
|---|---|---|
| 1 | 4 basics (2 melee, 2 ranged) | the stage start (§2.2 t130) |
| 2 | 4 basics + 수호 | the previous wave has ≤ 1 alive, or 20 s after the previous wave |
| 3 | 4 basics + 둥지 | same |
| 4 | 4 basics + 양육 | same |
| 5 | 3 basics + 포식성 (it swallows one) | same |
| 6+ | 4 basics + 1 special from a shuffle bag {수호, 둥지, 양육, 포식성}; from wave 7 two specials | same |
| time-out | 75 s into the stage: warning, then 1 파괴; another every 20 s (at most 2 alive) | the stage clock |

- **Cap:** 8 organisms alive. A due wave waits; time-out spawns ignore the cap.
- The order follows the guide's demonstrations (v3/v4 captions: 수호 → 둥지 → 파괴 → 포식성 → 양육). 파괴 is the
  time-out punisher in the wiki ("시간을 오래 끌 경우 경고메시지와 함께 파괴의 증식생명체가 나온다", `img/14.png`).
- **Warning:** title "!" + "오아시스의 심장이 위험합니다" (gold/red), a sub-line timer and a horn (e.g.
  `event.raid.horn` at low volume, vanilla).
- **Spawn points:** 8 fixed points on a ring r 10-13 around the Heart. Never closer than 4 b to the player. A wave
  spreads over 3-4 points. Each spawn is a 20 t wireframe marker (v2 §H `k_f2418`), then a 10 t emergence (Genshin's
  cell-split look; kit motes).
- **Expected length** (`calc_ap.py`, Genshin values, ~15 ‱×10 lost per wave): **5-6 waves**. A wave takes about
  15-20 s at sword pace (basics 4 × 4.3 s single-target, AoE less; a special 6-9 s; walking), so **75-95 s**, slightly
  above `CH` §5.4's 60-90 s target.
  - If the fairness sim shows more than 100 s, raise the basic kill to +250 and the special kill to +1200
    (5 waves).
  - If an ignored Heart drains too slowly, shorten the basics' attack interval.
- **Drain if ignored:** 4 basics hitting every 40 t = 12 ‰/s, so 27 % lasts **22 s** (`calc_ap.py`). In v3 take A the
  guide let 6-7 basics drain 25 % in about 4 s (`v3/heartbar.txt` 4.5 → 8.0 s, then `k_f0540` "도전 실패"). Ours is
  gentler on purpose.

### 2.5 The six organisms

**Common build (recommended): framework aux husks + module AI + small display rigs.**

| part | how | reference |
|---|---|---|
| gameplay entity | `mboss/aux/spawn`: an invisible NoAI husk with `rlk_mob`, the overhead HP bar (`F:mob/setup:14` → `F:mob/hb_spawn`), the click shield (`F:mob/shield_ensure:16`, 1.2 × 2.2), the boss level, never `rlk_zmob`, `#auxRes 10` | `core:1049-1091` |
| HP | `#auxHp` = `#apTot` × ‰ / 1000 (overflow-safe pool, as the Guardian's stars do; `#auxHpPct` would read the body's *current* `mhpM`, which changes between phases) | `gdcore:1078-1090` |
| damage taken | the same mods as the body (engravings, items, level factor, RES 10) → module `aux_hit` (Dendro ×8/9, shields, immunity) → `aux/take` (number, `rlk_mb_broken`) | `F:combat/apply:25-27`, `core:1003-1048` |
| kill | the module tick reads `rlk_mb_broken`: progress, death fx, energy particles, `kill` (passengers first). Aux kills pay **no** XP, gold or heal orbs (they return before `apply:64-82`) | `core:1044-1048`, `F:combat/apply:27` |
| model | 1-3 `item_display`s per organism with RP item models (`MD` §6 table), riding the husk as passengers (as the HP bar does, `F:mob/hb_spawn:8`), translated down to the feet; looks are item-model swaps; motion is `transformation` interpolation (bob, flap, spin, pulse) | `MD` §6 |
| movement | module stepping `tp ^ ^ ^v` facing the target, y snapped to the floor (the arena is flat), ≈ 5 commands per organism per tick; no `mv/*` (≈ 25 commands per mover, `S:mb3/code/adapt.md:90`) | — |
| attacks | framework `hz/*` and `pj` with the organism as `@s` (knockback source, `core:948-949,963-967`), so the fairness sim sees them | `core:1242-1878` |
| tags / scores | `rlk_mb_ap_org` + `rlk_mb_ap_<kind>`; `mbS` = kind 1-6, `mbT` = state clock, `mbId` = link / variant (free module scratch, `core:82-83`); module objective `apShd` for shields | — |

**Why not the existing mob system (`F:cm/*`, `F:room/mob_*`):**
- cm mobs are vanilla-AI husk brains that chase a "lure" at the player (`F:cm/world:3-9`, `F:cm/aggro:1-6`) and cannot
  target an objective;
- they hold `rlk_zmob` and pay XP, gold and heal orbs through the normal kill path (`F:combat/apply:69-81`);
- they have one flat `mres`, no hit hook and no link logic;
- their attacks (`F:cm/hit_pl`) are invisible to the framework fairness tooling.

**Budget.**
- Entities per organism: a husk, an interaction, 5 HP-bar displays and 1-3 model displays, about 9; 8 organisms make
  about 72.
- Commands: about 15-25 per organism per tick, about 200 per tick at the cap, inside the framework budget (average
  ≤ 250, peak ≤ 2.5 k; `S:mb3/code/adapt.md:866`).
- The Warden's rig is hidden in phase 2, so the frame budget is free.

#### Stats

All attacks are Dendro (el 7). Damage is in % of the registry atk (`core:941-945`). Numbers are for an item-less Lv15
player: HP 268, def 38 (`calc_ap.py`).

| kind | HP ‰ of 7984 | HP | kill time, RES 10 / Dendro 20 | Genshin ratio (of total HP) | player damage |
|---|---|---|---|---|---|
| 기본 basic | 20 | 159 | 4.3 / 4.8 s | 47 ‰ | melee/bolt 25 % → 11 HP (4 %); buffed 35 % → 17 HP |
| 수호 guarding | 40 | 319 | 8.5 / 9.6 s | 94 ‰ | none |
| 파괴 destruction | 30 | 239 | 6.4 / 7.2 s | 59 ‰ | blast 67 % → 34 HP (12 %) |
| 포식성 predatory | 35 | 279 | 7.5 / 8.4 s | 71 ‰ | burst 35 %; chain 67/34/20/13 % (1.0/0.5/0.3/0.2) ≈ 68 HP (25 %) per chain |
| 둥지 nesting | 30 | 239 | 6.4 / 7.2 s | 71 ‰ | none (walls) |
| 양육 nurturing | 40 | 319 | 8.5 / 9.6 s | 94 ‰ | none |

Genshin's organisms carry about 2× these shares, but a party kills them with AoE in 1-2 s. A single player needs the
halved pools to keep waves at 15-20 s. Damage ratios are scaled from the Genshin ATK table (basic 381, 파괴/포식성
7613, boss 11,419; `img/14.png`): "100 %" of a 7613-ATK organism ≈ 67 % of the boss coefficient. The basic is raised
from a Genshin 2 % to 25 % so that standing in their lines is noticeable but trivial.

#### 2.5.1 기본 증식 생명체 (basic)

Sources: `img/15.png`, v4 §4.2, v3 keys `k_f0990-k_f1050`.

- **Approach.** It hops to the Heart at 0.08 b/t.
  - Melee basics stop at r 2.6 from the Heart centre; the bulb surface is ≈ 1.3 b.
  - Ranged basics stop at r 6-7.5.
- **Melee, every 40 t.** A 10 t lunge squash tell, then the strike:
  - Heart −60 (buffed −120);
  - a `hz/sector {r:22,a:45,tell:10,dmg:25}` aimed at the Heart from the tell start, so a player in that small cone
    is hit too.
- **Ranged, every 50 t.**
  - The crown opens for 12 t (v3 `k_f0999` "bag crown open charge").
  - A bolt is launched as a `pj/launch` sphere prop: hr 0.6, life 16 t, speed = distance / 16, `#pjWall 0`, dmg 25,
    aimed at the bulb.
  - `pj_end` event 2 (life over at the Heart): Heart −60.
  - Event 4 (it hit the player): `#pjKeep 0`, the Heart is spared. **Body-blocking works**, and the player learns it.
  - Launch at y + 1.6: the pj sphere test sits 0.9 b under the prop (`core:1796-1797`).
- The organisms attack the Heart first ("심장을 1순위로 공격", `img/14.png`). Basics never chase the player.
- **Kill:** +175, a pale-green burst, `block.azalea_leaves.break` + `entity.slime.squish_small` (v4 §5).

#### 2.5.2 수호 증식 생명체 (guarding)

Sources: v4 §2.2-2.3, v3 keys `k_f1908-k_f2088`.

- **Spawn animation, 30 t:** collapse, bud, regrow, orb on top (v3 `k_f1908…k_f1992`).
- **Then the shields pop** onto every basic within r 10, including later spawns while it lives.
- **Shield:** a pool `apShd` = **3 × the basic's max HP (480)**, shown as 2-4 leaf panes per basic (v4 §2.2,
  1.3 × 0.55 b).
  - In `aux_hit`: Pyro hits count ×2.5 against it (the Genshin Dendro-shield rule). It absorbs before HP, like the
    custom shield soldier (`F:cm/sh/absorb:10-17`).
  - When fully absorbed: a sky-blue number (the module takes over the number with `#mbAuxDone 1`) and
    `item.shield.block` (v4 §5).
- **Guard death:** every shield vanishes at once (v4 §2.3: "shields vanish with the kill").
- **First time:** the hint "수호의 증식 생명체를 먼저 처치하세요". The v4 caption: "보호막 파괴가 거의 불가하므로
  수호의 증식 생명체를 먼저 파괴해야만 한다".
- Immobile, no attack. Kill: +1100, red embers and a black wisp (v4 §2.3).
- Note: `wiki.md:115-116` ("the shield must be removed first before the guarding organism can be removed") is a
  mis-transcription. The caption says the opposite and the footage agrees.

#### 2.5.3 둥지 증식 생명체 (nesting)

Sources: v4 §2.4, `img` text `wiki.md:92-96`.

- **Movement.** It hovers 1 b up and keeps 4-8 b from the player. If it is more than 12 b away it **teleports** to 5 b
  from the player (blink fx). The footage never shows a blink; the wiki states it.
- **Cast every 160 t.**
  - Tell: it curls into a vertical loop for 12 t.
  - **Walls:** 3 groups 120° apart at r 3.5 around the player's feet, locked at the tell start. Each group is 3 leaf
    blades over a 60° arc, 2.5 b tall.
  - Variant (30 %): one arc of 3 blades 3 b ahead of the player's facing ("3 at once in front", wiki).
  - They live 40 t and dissolve in 8 t (v4: 2.0 s + 0.4 s). **No damage** (caption "공격능력은 없다").
- **Block build (recommended):**
  - `minecraft:barrier` at floor + 1 and + 2 under each blade display.
  - Barrier is **not** in `#rlk:dash_pass`, so it stops the dash and the knockback checks
    (`F:player/dash_chk_*`, `F:player/knockback/check`) and the avatar's physics.
  - It **is** in `#rlk:cm_pass`, so framework projectiles fly through (`DP/data/rlk/tags/block/cm_pass.json`).
  - Rules:
    - never on the player's own block or the block above;
    - at least two 60° gaps;
    - only inside the walk disc;
    - only in phase 2 (the boss is underground, so no boss hazard can trap the player).
  - Cleanup: `fill … air replace minecraft:barrier` limited to y + 0..+2 inside r 26. Run it on the wall timeout and
    in the module `pause`, `cleanup`, `reload`, `death_start` and `uninstall` hooks, because the init/reload aux kill
    (`core:175`) removes only the displays. The arena's own barrier cap is at y 208-215 (`CH` §4.1) and stays clear of
    that band.
  - Fallback without blocks: "soft walls". If the body's feet are inside a blade rectangle, push it back out with
    `player/knockback/check` + `tp`. That costs more commands and feels worse.
- Kill: +1100.

#### 2.5.4 포식성 증식 생명체 (predatory)

Sources: v4 §2.6, `wiki.md:103-107`.

- **Fish form.** It swims at 0.15 b/t to the nearest basic.
- **Swallow** at ≤ 1.5 b: rears 6 t, scoops 6 t. The basic is removed with no progress. If that basic was buffed, the
  양육 takes −40 % (§2.5.6).
- **Empower.** Bud for 20 t (hovering, the core lit), then it inflates for 8 t (the tell).
- **Burst:** `hz/disc {r:30,tell:8,dmg:35}` (the wiki's "single bite 50 %"; v4 1676 = half of the first chain bite).
- **Then** it circles the player at 3-5 b for 40-60 t.
- **Bite chain × 2.**
  - 4 bites 6 t apart, each a 1.5 b lunge + `hz/sector {r:22,a:40,tell:8,dmg:67|34|20|13}`; the first tell is 12 t.
  - v4 measured 3352 / 1676 / 1005 / 670 = 1.0 / 0.5 / 0.3 / 0.2.
  - 14 t pause, then the second chain (v4: 9 bites in 3.07 s).
- **After that,** a single bite (34) every 60 t until it is killed.
- **No basic to swallow:** it goes for the player un-empowered (no burst; the chains at ×0.7).
- **Dodging:** dash (2 charges, 5 t between dashes, 6 t i-frames: `F:load:800-804`, `F:player/dash_go:4`), or keep
  more than 3.7 b away (lunge 1.5 + reach 2.2).
- The guide's verdict: "the real damage threat of phase 2" (v4 §2.6: −84 % HP in 6 s). Ours: about 25 % per chain.
- Kill: +1100.

#### 2.5.5 파괴 증식 생명체 (destruction)

Sources: v4 §2.5, `wiki.md:108-112`.

- **Roll** to the Heart at 0.12 b/t: about 75 t from r 11 (the shell spins).
- **Fuse:** 56 t on contact (v4: contact → blast 2.8 s). The face pulses every 9 t and faster in the last 20 t, with
  `entity.creeper.primed` at contact.
- **Suck-in** 5 t (v4: the air band drops 15 dB), then the **blast**:
  - `hz/disc {r:30,tell:61,dmg:67}`, made at contact so the decal is the fuse;
  - **Heart −1400**;
  - a green dome fx r 3 and the husk shell (v4 §4.5).
- **Killed before the blast:** +1100 and **energy particles** `function rlk:char/particles {n:4,el:7}`
  (`F:char/particles:1-8`; the wiki's "+20 energy"). Other kinds drop n 1.
- Kill window: about 130 t from spawn, with 6.4 s of single-target DPS needed. Fair.

#### 2.5.6 양육 증식 생명체 (nurturing): two readings, Q1

Sources: `img/14.png`, v3 keys `k_f1240`, `k_f1440-k_f1542`, v3 caption.

- **Common.**
  - It walks to 5-7 b from the basics' cluster and stands on its glowing ring.
  - It links up to **3** nearest basics: green tether beams, a 20 t link-up tell (v3 `k_f1240`).
  - Linked basics get the `buffed` look: a green aura and a lime ring. Their Heart hits cost 120 and their player
    damage is 35 %.
  - A buffed basic that dies or is swallowed costs the nurturing **40 % of its max HP** ("버프 받은 기본 증식 생명체가
    제거될 경우 최대 체력의 40%만큼 체력을 잃는다").
- **Reading A (footage; recommended).**
  - `img/14.png` puts "모든 내성이 9910%로 증가" on the row "양육의 증식 생명체 **버프 중**", the nurturing itself.
  - The v3 caption reads "기본 증식 생명체를 강화하고 **막강한 저항을 얻는다** / 강화된 기본 증식 생명체를 처치하면
    **자멸한다**".
  - The footage shows buffed basics dying (`k_f1537`), then the nurturing self-destructing (`k_f1542`).
  - So: **the nurturing cannot be damaged while ≥ 1 link holds** ("면역" popup). Buffed basics are killable; each one
    killed costs it 40 %; the 3rd kill (120 %) destroys it.
  - The user's "buffed organisms can't be damaged" then describes the organism in the "버프 중" row.
- **Reading B (the `wiki.md:98-101` transcription).**
  - Buffed basics cannot be damaged. The nurturing is killable normally; its death ends every buff.
- Both are one switch in the module (`NURTURE_MODE`). The progress values are the same.
- **Pitfall for A:** the 40 % loss must be applied to the aux's `mhpC` in the module, with the module's own break. A
  `mboss/true_hit` on an aux husk skips `aux_hit` (`F:combat/apply:27`, `unless score #trueDmg`) and runs the normal kill
  path. That would `kill` it and pay XP, gold and a heal-orb roll (`F:combat/apply:64-81`).
- Kill: +1100.

### 2.6 Framework pitfalls for the organisms

| pitfall | where | rule |
|---|---|---|
| true damage on aux | `F:combat/apply:27,64-81` | never `true_hit`/`true_pct` an organism; change `mhpC` and tag `rlk_mb_broken` in the module |
| `#auxHpPct` follows the body's current `mhpM` | `core:1077-1086` | use `#auxHp` from `#apTot` |
| every aux dies on `/reload` | `core:175` | module `reload`: keep `#apHt`, the wave index and the stage clock; clear the walls; respawn the current wave (markers 20 t) |
| pause | `core:822,851-856` | the module tick does not run while paused, so organisms freeze (NoAI husks); the walls stay, so clear them in the `pause` hook and re-cast later |
| hazards refused while dying | `core:1275-1277` | not an issue: the body is in state 1 throughout phase 2 |
| organisms and `lib_clear` | `core:918-925` | `lib_clear` does not kill organisms (husks); the module kills them at the cut-scene, at the failure wither and in `cleanup` (`cleanup_aux` kills `rlk_mb_aux`, `core:758-762`) |
| riding displays and `tp` | — | teleporting a vehicle keeps its passengers in current Java; verify once in-game / mcsim (Q9) |

### 2.7 Heart at 0 %: what failure means here

- **Genshin.** The domain fails: the "도전 실패" panel with "27초 후 자동 포기" (v3 `k_f0540`, `k_f0640`; the v3 caption
  "게이지가 모두 소모되면 강제로 실패된다").
- **Our roguelike.** Death means losing the run:
  - `F:player/die:1-7` → `F:player/hook_respawn:3-5` → `F:run/fail:1-11` (`run/end`, `player/reset_one`, lobby);
  - test mode goes to `test/defeat` (`core:2270-2282`).

| option | rule | verdict |
|---|---|---|
| A, faithful | 0 % → `mboss/cb/lose` (`CH` R14: `curHealth 0` → `player/die`) | harsh: one mechanic slip ends a 3rd-chapter run; Ronova's once-per-map revive (`F:player/die:4`) would bring the player back into a dead stage, so the stage must restart anyway |
| **B, two strikes (recommended)** | **1st 0 %:** "소생 실패" (below); **2nd 0 % in the same fight:** option A | keeps the tension, forgives one mistake |
| C, soft | progress floors at 0, the stage continues | loses the mechanic |

**"소생 실패" (option B, first failure), about 60 t:**
- The Heart withers (dark look) and a Dendro shock ring spreads from it, r 0 → 26.
- Every organism bursts with no progress.
- The player takes **50 % max HP, non-lethal**: the `AZM` N7 helper `mboss/pl_dot` with `#mbDotLethal 0`, or
  `mboss/hurt` + a 1 HP floor like the butterfly's debuff (`F:mboss/butterfly/coc/apply_pl:10-11`).
- Progress back to 2700, the wave index back to 2, the time-out clock reset.
- The warning "다시 한 번 실패하면 쓰러집니다" (red), and the sub-line keeps a ⚠ badge.
- Ronova edge case: with option A after a Ronova revive, restart the stage at 2700 once more.

### 2.8 HUD in phase 2

The framework's 3 bars are enough (`core:1111-1131`). The `bars` hook runs as the body, which is alive underground.

| line | phase 2 content | how |
|---|---|---|
| 1, name (`rlk:mboss`) | "「오아시스의 심장」" (gold) + `extra[]` badges of the special kinds alive (e.g. "  ◆수호" in its colour) + "  4웨이브" | title swap `mboss/title` (`CH` R6: writes `cur.title`, which `core:1120` reads) |
| 2, bossui (`rlk:mboss_state`) | the progress bar: `#buHp` = `#apHt` / 10 (‰), `#buMax` = 1000; the module sets them after the core (`core:1121-1127` then `d/bars`) | works today in red; for the Genshin gold (#EDCF63, v2 §5) add the `#buHpCol` option to `bb:47,188` (`CH` R10) |
| under-bar | the time-out gauge: time left to the warning (gold 8), red (2) after it | `#buSub/#buSubMax/#buSubCol` (`core:1124-1127`, colours `bb:50-58`) |
| 3, sub (`rlk:mboss_sub`) | "마물을 처치해서 소생 진행도를 올리세요" → "소생 진행도 47%" + hints (수호 first, …) | `sub[]` + `line/say` |
| actionbar / title | stage start, time-out warning, failure, 100 % | `title` as in `mboss/gate` (`core:330-336`) |

Optional: organism name tags over the specials, the "phantom view" labels (v4 §0; the guide was holding Elemental
Sight). Presentation only.

### 2.9 Phase 2 → 3 cut-scene (≈ 170 t)

Sources: w2 (19.5 s) and the in-game version in v5 3.7 → 11.9 s (`kp09`, `kp10`): fade to black, the lake, a leaf
burst, the hood out of the leaves, a flash, the reveal, the phase-3 fade-in.

| t | event | implementation |
|---|---|---|
| 0 | progress reaches 10000: every organism wilts (the Heart's green pulse ring r 0 → 26 over 20 t); walls cleared; no hazards remain | the module kills organisms; `lib_clear` set |
| 0-20 | the Heart blazes, light beam; sub-line "오아시스의 심장이 소생했습니다" | props, kit flash |
| 20 | white-out: a full-screen flash glyph on the title line (the kit's `hud/flash_white` pattern, `S:mb3/fg_fx_api.md` §5) + `blindness` 2 s | — |
| 20-60 (screen covered) | **arena look swap** withered → lush (`CH` §4.4 block swap in slices; displays and decor only if the builder prefers); body re-pooled to 3753 (§3.1); rig look `p3`; player `tp` to the arrival spot facing the centre (`tp_start`, `core:528`) | — |
| 60-150 | the reveal: egg rises, the vine hand grips it, a green burst, leaf burst, the Warden of Oasis Prime emerges (rig clip `emerge_p3`, ≈ 80 t; v5 `kp10` P+38 leaf burst → P+69 flash → P+150 fade-in). Optional camera: generalise Raiden's cinematic camera (`F:boss/raiden/camera/{start,hold,end}`, `cin:17-100`) into a framework `mboss/cam/*` | — |
| 150-170 | title "기원 오아시스 파수꾼" / subtitle "「불씨」를 받아 소생한 생명" (`img/11.png`); bars refill over 30 t (like `bars_ramp`, `core:1132-1136`, from the module `bars` hook); music switch (`CH` R11); targetable, proxies on | — |

- The boss deals nothing during the cut-scene: no patterns, no hazards.
- A pause (death screen, selection) freezes the timeline, because the module tick does not run.
- `/reload` mid-scene re-derives "phase 3 ready" from the scores.

### 2.10 Tests (mcsim + in-game)

`test/chapter {id:"apep"}` (`CH` §2.3), then module ids through `test/pattern {id}` (`core:2237-2242`):

| id | action |
|---|---|
| 20 | enter phase 2 |
| 21 / 22 | Heart +25 % / −25 % |
| 23-28 | spawn one organism of each kind at a spawn point |
| 29 | force the time-out |
| 30 | skip to phase 3 |
| 40 | force a stage failure |

mcsim suite `test_apep.py` (copy of `S:mb3/tests/fgsim.py`, `CH` R15) checks:
- progress arithmetic per event;
- the cap and the time-out;
- the shield pool with the Pyro ×2.5;
- the nurturing mode A/B;
- swallow → −40 %;
- 파괴 killed vs blast;
- wall placement never on the player, ≥ 2 gaps, cleared on pause/reload/cleanup;
- bolt body-block;
- organism RES (Dendro ×0.80, other ×0.90);
- aux kills pay nothing;
- the failure strikes;
- reload in each stage state.

---------------------------------------------------------------------------------------------------

## 3. Phase 3 and 종말의 여파

### 3.1 Entering phase 3

- `mhpM = mhpC = #apP3` (3753).
- The title swap to "기원 오아시스 파수꾼" with `cur.sub` "「불씨」를 받아 소생한 생명".
- RES unchanged (Dendro 30).
- `#apPh 3`. Floor 0: the kill runs the normal death path → the chapter clear (`CH` R4/R5).
- Proxies on the upright naga (`MD` §9.1: face, chest, trunk base, 4 leaf hands, the tail). Without proxies the hood
  (8.5 b up) and the hands (±3.8 b) are outside melee reach: `F:combat/find_immediate:60-62` measures 3.5 / 4.5 / 5 b
  to the husk's feet.

### 3.2 What the footage shows

Sources: `kp15` (w1, 25 fps, wiki clip), `kp16` (v5 22.0 s, in game), wiki §2.2.3; v5 captions in
`S:ap/understand/v5/caption_texts*.jpg`.

**Caption** (v5, the guide): "광역 공격 — 몸 바로 주변부터 시작하여 맵 전체에 장판이 깔리고 틱데미지를 준다 / 곧 이어서
강력한 광역 공격을 날린다 / 즉사기는 아니며 기믹 보호막으로 간단히 회피가 가능하다" ("a field starts right around the
body, covers the whole map and ticks damage; a strong AoE follows; not an instant kill, the mechanic shield avoids it
easily").

**HUD banner** (w1, v5): "…안으로 들어가서 종말의 여파를 막아내세요".

| v5 (F0 = field start) | w1 | event |
|---|---|---|
| P−74 … P−38 | — | over the player, crouch; walks to the centre (tail whips on the way) |
| P−4 | P+98 "lands, field ring" | low at the centre |
| P+4 … P+18 | P+124 "ring wave spreads" | the field spreads from the body (tick damage; a green number "1048" on the player at w1 P+138) |
| P+28 … P+32 | P+138 "pillar = dome spawn", P+148 "dome forms" | the first dome forms where a light pillar fell |
| P+64 | — | **three domes** stand |
| P+44 / P+50 | P+116 / P+190 | boss flash; the boss rolls aloft |
| P+105 | P+218-230 light columns rain, **P+240 white-out (blast)** | the blast |
| P+114 … P+126 | P+252 "dome holds" | a flood wave over the floor |
| P+161 | P+276 | the domes pop |
| P+172 / P+188 | P+300 | the boss stands, upright T-pose |

So the field front opens the attack, the domes appear 25-60 t later, and the blast comes about 75 t after the first
dome. The whole move is about 200 t. The wiki adds:
- "Entering the dome is not hard, but leaving it too early can kill you";
- "it repeats as the fight goes on" (`wiki.md:125-131`).

### 3.3 Proposed timeline (service pattern Q2, 210 t)

| t | event | implementation |
|---|---|---|
| −40 … 0 | the boss walks to the centre (≤ 0.25 b/t) | `bstep toward` the arena marker (`fgapi:321-326` template) |
| 0 | banner (actionbar + sub-line) "보호막 안으로 들어가서 종말의 여파를 막아내세요"; the under-bar becomes a countdown to the blast | kit-style banner (`S:mb3/fg_fx_api.md` §5) |
| 4-30 | **field front**: an expanding ring r 3 → 26 at 0.9 b/t, with the kit `tele/wave` decal + a band | the fieldgen wave front without damage: `hz/ring` dmg 0 + `hz/resize_s` per tick (`fgfield:413-453`, `core:1660-1672`), or decal only |
| 20 / 40 / 56 | **domes 1, 2, 3**: a light pillar (10 t tell) then a dome r 3.5 b | dome 1: 6-9 b from the player, toward the middle ring; domes 2 and 3 at ±120° around the arena centre on r 12-16; never within 7 b of the boss anchor; inside the safe disc (`mv/clamp`, `core:2132-2143`) |
| 30 … 100 | **field ticks** every 20 t on a player outside every dome: 2 % max HP, Dendro, non-lethal | the dome check (§3.4) + `pl_dot` (`AZM` N7) |
| 80-104 | light columns rain (fx); the under-bar turns red; "곧 폭발합니다!" | kit |
| **105** | **blast**: everyone outside every dome takes **80 % max HP** (lethal below it), Dendro; dash i-frames do not help; shields absorb as usual (`F:player/take_damage:29-30`) | the dome check + `pl_dot` 800 ‰, lethal; fallback `mboss/hurt` with `#mbHitPct 420` (= 80 % at pLv15, `calc_ap.py`) and `#mbNoDodge 1` (`core:950-962`) |
| 114-126 | flood wave: a second hit for anyone outside, 20 % max HP ("leaving too early can kill you") | as above |
| 105-160 | the domes hold (the player can stay) | — |
| 161 | the domes pop; banner off; the boss rises | — |
| 161-210 | recovery (punish window) | — |

Fairness:
- **At least 85 t** from the first dome to the blast. A dome is 3.5 b wide and ≤ 9 b from the player, so even a walk
  (0.22 b/t) gets there in about 40 t.
- The blast is lethal only for a player who ignores 85 t of banner, countdown and pillars, and who is already below
  80 % HP.
- Caption "즉사기는 아니며" means a full-HP player survives. Q3 asks whether to cap it non-lethal.

### 3.4 Dome model and the check

**Model, per dome:**
- a marker `rlk_mb_ap_dome` (tags `rlk_room rlk_mb_aux`; score `mbS` = radius in tenths, 35);
- an `item_display` translucent green hemisphere (RP model, scale 7 b, brightness 14; cf. the Heart's translucency
  rules, `MD` §11);
- a rim ring decal (kit) + 4 rising leaf cards;
- a light-pillar card for the tell.

The domes are props: no collision, and organisms do not exist in phase 3.

**Check (module, at each field tick and at the blast).** As `rlk_body` (the avatar or the first-person player, never
the camera; cf. `core:1530-1531`):

```
scoreboard players set #apSafe mb 0
execute as @e[type=marker,tag=rlk_mb_ap_dome] at @s run function rlk:mboss/apep/dome/contains   # dx²+dz² <= r²  ->  #apSafe 1
execute if score #apSafe mb matches 0 run function rlk:mboss/apep/dome/hit
```

- `contains` is Raiden's `dome_contains` (`enc:1023-1035`): a horizontal test in hundredths, so a jump inside is safe.
- The pre-test `distance=..7` keeps the cost at about 15 commands per dome.
- It costs about 50 commands on 7 ticks of the move.

**Alternative.** Azhdaha's proposed framework "mask" hazard (`AZM` N4: `hz/full` that hits unless the feet are within
`R0` of any marker `rlk_mb_hzsafe` with the hazard's id). It is better for the fairness sim, which reads `rlk_mb_hz`
markers (`CH` §3.1 reason 2). Use it if it lands first. The framework's `hz/full` today has **one** safe circle only
(`core:1251,1596-1612`).

**Why not `hz/full` ×3:** each hazard would hit unless the player were inside *its own* circle, so three hazards would
always hit at least twice.

### 3.5 Repeats

- First use after the first phase-3 pattern. v5: phase 3 fades in at 11.9 s, 종말의 여파 starts at 22.0 s.
- Then a **cooldown of 900 t** (45 s) of fight time. It is forced at the next decision point once the cooldown is over
  and the phase-3 pool has dropped another 30 %, and it never runs twice without ≥ 3 other patterns in between.
- With a 100 s pure-DPS phase 3 (`calc_ap.py`), that means 2-3 uses per fight.
- The wiki's quirk (a knockdown during the skill pops the dome first) is skipped: we have no poise system.

---------------------------------------------------------------------------------------------------

## 4. Pattern mapping

### 4.1 Helper inventory (existing)

| helper | lines | used for |
|---|---|---|
| `hz/disc ring sector line full` + options (`#hzAct #hzEl #hzKB #hzKBDir #hzY0/1 #hzR0 #hzBack #hzSfx #hzVis #hzCol #hzLinger #hzQuiet #hzGrp #hzNoDodge #hzRearm`) | `core:1242-1269`, defaults `core:210-238`, `hz/init` `core:1285-1354` | every ground hit |
| one hit per hazard; a dodge consumes it; volley groups | `core:1613-1628`, `grp_new/grp_mark` `core:1813-1828` | volleys, the rotation dodge cue |
| `#hzAct` active window (the hazard keeps testing) | `core:1290,1424-1429` | 초목이 시든 풍경's spin window |
| `hz/aim` (re-aim a live hazard) | `core:1634-1648` | tail sweeps (rotating line) |
| `hz/resize_s` (grow per tick) | `core:1649-1699` | wheel carpet, field front |
| `#hzNoDodge` → `mboss/hurt_nd` | `core:1301,1623`, `core:950-962` | none of the hazards; the dome hit goes through `hurt` with `#mbNoDodge 1` |
| `pj/launch` (sphere or blade), `pj_end` events, groups | `core:1732-1812,1863-1903` | basics' bolts, shells, spikes, wheels |
| `pj/steer {max}` (homing ±60° pitch; works on any `@s`) | `core:1829-1862` | homing thorn wheels (butterfly B4 template: 0.25 b/t, 9°/t, `bfwing:540-660`, steer at `:622`) |
| `mv/glide`, `mv/leap`, `mv/face`, `mv/turn`, `mv/toward/away`, `mv/clamp`, `mv/dist` | `core:2005-2162` | lunges, the combo leap, turning, bands |
| `rlk_mb_inv` (untargetable, no click shield) + `#mbNoLeash` | `F:combat/apply:17`, `F:mob/shield_ensure:6`, `core:891` | burrows (fieldgen warp precedent `fgcore:688-695`) |
| `aux/*` | `core:1003-1091` | organisms (§2.5) |
| `true_hit` / `true_pct` | `core:968-999` | tests only (never on aux, §2.6) |
| bars, `extra[]`, `sub[]`, under-bar, `line/say` | `core:1111-1131,1165-1218` | HUD |
| `Pattern` (bands, weights, lead ≤ 20, recover, max_len), `TL` timelines | `fgapi:170-205,423-474` | pattern records |
| `lockp/lockb` + `keep`, `clamp_walk/body`, `bstep`, `tag_last_hz`, `at/every` | `fgapi:289-345` | locks, body steps |
| expanding front (ring + `resize_s` + kit `tele/wave` + band) | `fgfield:413-453` | wheel carpet, field front |
| rotating re-aimed line hazards + moving lanes | `fgcruise:344-440` (C3) | tail sweeps |
| late-lock missiles (lock at +14, disc, tell 14) | `fgcruise:441-533` (C4) | shells |
| bombs along a line / volley groups of 4 | `fgcruise:224-313` (C1) | spike rain |
| Raiden dome check, cinematic camera | `enc:991-1035`, `cin:17-100` | 종말의 여파, cut-scene (idea reference, Raiden-only code) |

### 4.2 New helpers

| id | helper | level | sketch |
|---|---|---|---|
| A1 | **`#pjNoDodge`** | framework (≈ 4 lines) | a per-prop score `mbPjND` copied in `pj/launch` (as `mbHzND`, `core:1301`); `pj/hit` sets `#mbNoDodge` from it around `mboss/hurt` and resets it (as `hz/hurt` does, `core:1623-1625`); default 0, so existing bosses stay byte-identical. Fallback without it: a visual-only pj (dmg 0) plus a follower `hz/disc` with `#hzNoDodge 1` re-aimed onto the prop every module tick (the module tick runs before `hz/all`, `core:826-828`; one tick of lag) |
| A2 | `lockv {lead}` predictive lock | module | `AZM` N3: the player's last 6 t of positions → a marker at pos + velocity × lead, clamped to the walk disc (`fgapi:289-319`) |
| A3 | dome check + `pl_dot` | module (+ the `AZM` N7 framework helper) | §3.4 |
| A4 | Heart + organism AI + waves | module | §2.3-2.5 |
| A5 | nesting walls (barrier fill + cleanup) | module | §2.5.3 |
| A6 | body-frame classifier `u/zone` | module | `AZM` N8; §5.1 |
| A7 | hit proxies, `px/state/*` | framework + rig | `CH` R8, `S:az/understand/rigtech.md` §3.3 (shared with Azhdaha) |
| A8 | `mboss/floor`, `mboss/title`, bossui `#buHpCol` | framework | `CH` R6, R10 (shared) |
| A9 | cinematic camera `mboss/cam/*` (optional) | framework | from `F:boss/raiden/camera/*` (`cin:17-100`) |

### 4.3 Phase 1: 종막 오아시스 파수꾼

- Ticks are proposals: about 75-85 % of the footage wind-ups, the earlier bosses' rule (`S:mb3/plan.md` "−25 %").
- Every damaging hit keeps **≥ 10 t of telegraph** (`S:mb3/fg_contract.md:158-159`).
- Coefficients are in % of atk (100 = 51 HP = 19 % of an item-less Lv15 player; 150 = 28 %; `calc_ap.py`).

| # | pattern (wiki) | footage | mapping | dodge |
|---|---|---|---|---|
| P1 | **잠복 돌진** (burrow, burst at the player, forward attack) | v1 §A: tell 0-5, dive 5-10, sink 10-29, shadow glides 29-50 (≈ 0.6 b/t, stops 2-4 m beside the player), burst +50 (r 3.5), rise to +75, lunge-sweep +76…+83 (box ≈ 9 × 3), land +94, punish ≈ 80 t | t0 rear; t5 `rlk_mb_inv` + proxies off + `#mbNoLeash 1`; t8-24 sink (pool decal); t24-44 shadow decal glides to `lockv` (A2, lead 10) ≤ 0.7 b/t; **t34 lock fixed + ring decal**; t44 burst `hz/disc {r:35,tell:10,dmg:130}`, body `tp` there, targetable at t48; t48 `mv/face`, yaw locked; t50 `hz/line {len:90,w:30,tell:14,dmg:150}` along the facing; t64 body `mv/glide` 6 b forward in 7 t; t71 land; recover 50 t | dash / step out (both) |
| P2 | **생명의 손** (hands in the ground, 4 legs burst out and slam) | v1 §H: spread 0-7, swirl tell 7-36, plunge +40 (splash r 3.5 at the boss), legs rise +53…+68 around the player (2 near, 5-8 m to each side; 2 farther), line tells +68…+79, slams +82/+89/+95/+102 (R-L-L-R), sink to +120, rear and fold to +160 | t0-30 swirl (rig `hands_wind`); t30 plunge `hz/disc {r:35,tell:30,dmg:80}` at the body; t36 `lockp` + `keep`; legs at 4 spots on r 5.5 around the lock (±60° and ±140° from the boss → lock axis); t44 each leg's `hz/line {len:90,w:25}` aimed from its spot through the lock, tells 20/26/31/37 (slams t64/70/75/81), dmg 110, its own group; leg props rise t40-50, arc on their tick, sink after; recover 40 t | step out of the lines |
| P3 | **발광하는 파수꾼** (to the centre, 3 slams, undodgeable homing thorn wheels) | v1 §G + v2 §G: dig +0…+30, shadow to the centre +30…+51, gold glow +51…+56, emerge to +72, turn to +132, spiral wind-up to +191, **slam 1 +191** (r 4-5 + blade burst r 5-7), a carpet of 15-25 wheels rolling out at 0.75-1 b/t, 2 wheels per slam home onto the player (hit ≈ 21 t after the slam), slam 2 +29 t (6 t tell), slam 3 +29 t (a dive from 6-8 m) | t0-30 dig; t30-45 shadow to the centre; t45 gold-glow decal; t50-66 emerge (targetable t60); t66-96 spiral wind-up = slam-1 telegraph `hz/disc {r:55,tell:30,dmg:130}` at the centre (disc + blade burst); per slam: **wheel carpet** = `hz/ring` front r 3 → 12 at 0.8 b/t (`#hzQuiet`, `#hzY1 12`: jumpable, dmg 35, dodgeable; `fgfield:413-453`) + 12 wheel props riding it; **2 homing wheels** = pj sphere hr 0.8, 0.3 b/t, `pj/steer {max:5}` from +8 to +40, life 44, dmg 35, **`#pjNoDodge 1` (A1)**, both in one volley group (≤ 1 wheel hit per slam); slam 2 at t120 (leap clip; the disc decal from t100), slam 3 at t144 (dive from 7 b, the disc from t124); recover 40 t | slams and carpet: dash or leave; homing wheels: **i-frames do not help**, but a late sideways dash (3 b) or a tight circle beats a 5°/t turn (radius ≈ 3.4 b); ≤ 3 wheel hits × 17 HP |
| P4 | **초목이 시든 풍경** (range shown, then a rotating attack; dash when it is full) | v2 §R (often after the burrow-relocate v2 §B: tell 5, sink 10, emerge on the player 2-3 t, no damage): arms up +5, rear +13…+25, disc r 7.5 shown at +21, fills to the rim at +44 (dodge cue), crash +45…+52, spin +52…+76, recovery ≈ 60 t | optional relocate when the player is > 9 b away: t0-15 sink (`rlk_mb_inv`), t15 `tp` to `lockb` (`fgapi:295-299`), emerge, no hit; then t20 arms up; **t40 disc decal r 7.5 starts filling**; `hz/disc {r:75,tell:30,dmg:140}` with **`#hzAct 24`** (the spin window), KB 4 outward → strike t70, active to t94; recover 50 t (the slow push-up is the punish window) | leave r 7.5 before t70, or **dash on the fill**: the strike tick's dodge consumes the hazard (`core:1613-1617`), as the caption says ("범위가 완전히 꽉 찼을 때 대시하면 피할 수 있다") |
| P5 | **생명의 꼬리** (player behind; hard to dodge) | v2 §T: turns its back (150-180° in 19 t), tail raise +11…+31, swing 1 +37…+46, swing 2 +66…+73 (reverse), 25 % max HP hit (5324 / 21200), recovery 68 t | t0-12 small turn (≤ 40°) so the tail root faces the player; t12-30 tail raise + the kit lane `tele/mline` over the arc; **t30 swing 1**: `hz/line {len:95,w:25,dmg:160}` from the tail root, re-aimed every tick through 200° in 8 t (25°/t; C3 template `fgcruise:344-440`), tell = 18 t of lane; **t56 swing 2** reversed; KB 4; separate hazards; recover 50 t | a timed dash through the line, or stand at the head (wiki) |
| P6 | **근접 콤보** (2-4 hits, slow) | v2 §C: hits at +14 (low arm sweep, 130° r 6), +50 (double slam r 5-5.5, 4 m ahead), +87 (spin ring r 6), +131 (leaping double slam r 5.5, 6 m ahead, lunge 2-3 m) | hit 1 `hz/sector {r:60,a:65,tell:12,dmg:100}` t12; hit 2 `hz/disc {r:55}` 4 b ahead, tell 18 → t40, dmg 130; hit 3 `hz/disc {r:60}` around the body, tell 12 → t68, dmg 100; hit 4 `hz/disc {r:55}` 6 b ahead, tell 24 → t100, body `mv/glide` 2.5 b forward, dmg 150; length 2/3/4 by roll (3/4/3) | keep distance (caption "거리를 벌리는 것이 낫다") or dash each |
| M | crawl reposition | v1 §M: 8-10 m in ≈ 2 s, low crab crawl, then a half-stand | locomotion only: `bstep` 0.25 b/t for ≤ 40 t when the player is far or after P1 (`fgapi:321-326`) | — |
| T1 | **소생 단계 진입** | §2.2 | service | — |

### 4.4 Phase 3: 기원 오아시스 파수꾼

| # | pattern (wiki) | footage | mapping | dodge |
|---|---|---|---|---|
| Q1 | **이동 돌진** (underground, bursts out at the player; caption "바닥에서 빠르게 튀어 올라 꼬리를 휘두른다") | `kp11` (v5 M0 12.45 s): sinks +1…+22, leaf-pad trail +31…+41, pad ring = burst point +48, burst +52, curls into a hoop +57, rolling wheel +63, slams down +69, tail lands +73, **tail sweep +77**, rises +83…+99 | t0-20 sink (`rlk_mb_inv`); t20-40 leaf-pad trail decal to `lockv` (A2) at 0.8 b/t; **t36 lock + pad ring r 3.5** → t48 `hz/disc {r:35,tell:12,dmg:130}`, body `tp`; t53-65 the body rolls 4 b toward the player (`mv/glide`) and the tail-sweep sector `hz/sector {r:80,a:75}` aimed along the roll, tell 20 → t73, dmg 150; recover 26 t | dash / step out twice |
| Q2 | **종말의 여파** | §3.2 | §3.3 | enter a dome (i-frames do not help) |
| Q3 | **증폭의 풀** (several shells in a row; caption "세 번의 포격 / 첫 번째 포격 속도가 유난히 빠르다") | `kp14` (v5 32.4 s): target ring on the player +19, crown charge +40, launch 1 +46, **impact 1 +56 (a fast beam)**, splash +60, turning +92, T-pose charge +108, **shell 2 +119, shell 3 ≈ +123** | t19-44 a ring decal r 2.5 follows the player's feet (moved every 2 t); **t44 the ring stops = lock** → `hz/disc {r:25,tell:12,dmg:120}` (impact t56; kit sky beam); t95-105 charge; t105 lock A (`lockv`, lead 8), t109 lock B (`lockp`) → `hz/disc {r:30,tell:14,dmg:100}` each (impacts t119, t123), separate groups (late-lock template `fgcruise:441-533`); recover 30 t | move when the ring stops (r 2.5 in 12 t: walk + dash); dash or step for 2 and 3 |
| Q4 | **생명의 꼬리** (P3: swings the tail twice at the player) | `kp12` (v6 take 2): low crouch +0, tail curls up +8, cocked +14, **swing 1 +17**, rises / S coil +36…+46, coils down +54, **swing 2 (ground) +59** | as P5 but no BACK condition and no turn-away; swing 1 tell 14 (t17), swing 2 tell 14 (t59); rotating `hz/line {len:100,w:25,dmg:150}` from the coil anchor; recover 30 t | timed dash or range > 10 b |
| Q5 | **생명의 나선** (many spikes fired at the player; fairly hard to dodge) | `kp13` (v6 take 3): arms spread +0, crouch +5, rises +13, V arms + light column +19, **spikes summoned +33**, hover +43, **glint +49**, **fire +54**, helix trails rain +61…+69, recover +77, sinks +85…+109 (often into a burrow) | t33 12 spike props on a ring r 3 at y + 5-6 around the body; **t49 lock A** (`lockp`): 6 landing decals r 1.3 scattered within r 2.5 of A (tell 11); t54 launch 6 pj (sphere hr 0.6, 1.2 b/t, pitched to the points), dmg 90, **one volley group**; **t57 lock B** (`lockv`, lead 10): 6 more at t62 (group 2), landing ≈ t66-70; recover 30 t, then with a 40 % chance chain into Q1 (the footage sinks after it) | leave the scatter (≈ r 3.8 including the hit radius) or dash; ≤ 2 hits |

### 4.5 Dodge rules, undodgeable set, hit volume

- **I-frames.**
  - A dash gives `dashInvT 6` (`F:player/dash_go:4`). `take_damage` returns with `#dodged 1` while it runs
    (`F:player/take_damage:3-6`).
  - 2 charges, 20 t regeneration, 5 t between dashes (`F:load:800-804`). The burst gives `#burstInv 8`
    (`F:load:725`).
  - A dodged hazard is spent (`core:1613-1617`). A dodged member of a volley group does not disarm the group
    (`core:1627`).
- **Undodgeable by i-frames:**
  - the P3 homing wheels (wiki "회피가 불가능한 유도형 스킬"; A1);
  - the 종말의 여파 field ticks, blast and flood (the dome is the answer);
  - the phase-2 failure wither (§2.7).

  Everything else is dodgeable, including 생명의 꼬리 ("hard", not "impossible") and the 파괴 blast.
- **Hit volume:** hazards test the player's feet in a height band (`core:1534-1538`, default −0.5 … +3.5 b). The
  wheel carpet uses `#hzY1 12` so a jump clears it, like the fieldgen fronts.
- **Projectiles:** sphere tests sit 0.9 b under the prop (`core:1796-1797`), so set launch heights accordingly. Blades
  (`#pjShape 1`) are not needed here.
- **Player-side reactions:** every hit is Dendro, so a player with a Hydro aura gets Bloom extra damage and a Pyro aura
  gives Burning (`F:element/player_hit:1-16`). The butterfly (Dendro) already does this. Keep it unless the fairness
  sim shows Burning on top of 생명의 나선 is too much (`AZM` §3.5 proposes `#mbNoRx`).

---------------------------------------------------------------------------------------------------

## 5. Targeting, facing, zones, weights

### 5.1 Body-frame zones (A6)

Projection as `hz/hit` does it:
- a frozen forward unit ×1000 from a temporary marker at `^ ^ ^1` (`core:1342-1350`);
- `fwd = (dx·fx + dz·fz)/1000` (`core:1547-1553`), `side = (dx·fz − dz·fx)/1000` (`core:1587-1592`).

It costs about 25 commands, once per decision and every 10 t for the turn logic.

| zone (phase 1) | condition (b) | meaning |
|---|---|---|
| FRONT | f ≥ 2.5 and \|s\| ≤ 4 + 0.6 (f − 2.5) | in front of the hood / hands (the wiki's recommended spot) |
| SIDE | \|s\| > 3 and −3 ≤ f < 2.5 | beside the long arms (claws at ±5.3) |
| UNDER | \|s\| ≤ 3 and −3 ≤ f < 2.5 | under the thorax (the belly core at f +1.2 is melee-reachable) |
| BACK | f < −3 | behind the hips / along the tail (f −2.4 … −9.9) |
| band | `mv/dist` from the anchor (`core:2144-2162`): near ≤ 7.5 (the P4 disc), mid 7.5-14, far > 14 | |

Phase 3 (upright naga): only the band matters (near ≤ 6, mid 6-14, far > 14). The tail coils round the trunk
(`MD` §1.2), so there is no BACK.

### 5.2 Turning and movement

- **Idle tracking** `mv/turn {max:3}` (`core:2083-2102`; fieldgen idle at `fgcore:470-476`).
- **Turn step** when |Δyaw| > 60° at idle: a 90° crab-turn clip in 10 t (v1 §M: "turns ≈ 90°, the body pivots on its
  hands").
- **Front patterns** (P1 lunge, P2 aim, P6) pre-turn up to 10 t (`Pattern.lead`, `fgapi:194`). P5 deliberately turns
  its back (≤ 40°). Area patterns (P3, P4, Q2, Q3, Q5) need no turn.
- **Locomotion.** A crab crawl toward a far player (≤ 0.25 b/t, `bstep`); the post-P1 crawl-away reposition (v1 §M).
- **Body disc** r 16 (`clamp_body`, `fgapi:316-319`; the leash `core:2121-2127` against the arena safe radius), so the
  10 b of tail behind the anchor stays inside walk r 26 (`CH` §4.4).
- **Anti-stall.** If the player stays in BACK for ≥ 3 decisions while P5 is on cooldown, a 180° turn step follows.

### 5.3 Pattern choice

Decision at each pattern boundary (`ai/next`, template `fgcore:492-508`):

```
test request > lock > transition queued (#apTr 1) > 종말의 여파 due (phase 3) >
BACK rule (phase 1: 75 % -> P5 when off cooldown 200 t) > weighted pick by zone and band, no immediate repeat
```

Weights, phase 1 (0 = never):

| pattern | FRONT near | FRONT mid/far | SIDE / UNDER | BACK (the other 25 %) | notes |
|---|---|---|---|---|---|
| P1 잠복 돌진 | 1 | 3 (far 4) | 2 | 2 | cooldown 400 t |
| P2 생명의 손 | 1 | 3 | 2 | 2 | — |
| P3 발광하는 파수꾼 | 2 | 2 | 2 | 2 | cooldown 700 t; first allowed after 3 patterns |
| P4 초목이 시든 풍경 | 4 | 2 (with the relocate) | 4 | 2 | — |
| P5 생명의 꼬리 | 0 | 0 | 1 (SIDE, f < 0) | rule | — |
| P6 근접 콤보 | 4 | 1 (mid only) | 1 | 0 | front only |

Phase 3: Q1 far 3 / mid 2 / near 1; Q3 mid 3 / far 3 / near 1; Q4 near 3 / mid 2; Q5 2 everywhere; Q2 scheduled
(§3.5).

- **No immediate repeat:** `unless score #apLast matches <id>` on every candidate line (`fgcore:535-553`). Keep the
  `cand_any` / first-pattern fallbacks (`fgcore:564-589`).
- **Recover** 20-50 t per pattern (heavy ones longer). P4 and P1 have the long punish windows of the footage (v1 §A
  ≈ 4 s idle; v2 §R ≈ 3 s).

---------------------------------------------------------------------------------------------------

## 6. Chapter-3 routing (aligned with `CH`)

| item | value | reference |
|---|---|---|
| route | `room/pick/boss` → generated `mboss/cb/route`: `#chapter 3` → `mboss/cb/layout {id:"apep"}`; others as `CH` (1 → azhdaha, else Raiden); `#cbForce` for tests | today `F:room/pick/boss:3` always loads Raiden; `CH` §2.2 |
| carry / spawn | zone `data.boss_id:"apep"`; `room/boss_spawn` → `mboss/cb/start {id}`; gate object oact 16 | `F:room/boss_spawn:2-3`, `F:room/mob_wave:2`; `CH` R2 |
| level | L18 (boss map `#mapIdx 5`, chapter 3) | `F:room/mob_init:35-40` |
| theme | the chapter-3 dungeon is Sumeru (`#th 5`), entrance room "sandstone + mud-brick oasis gate" | `F:room/theme:10,16`; `CH` §4.4 |
| registry | `id apep`, `kind chapter`, `ch [3]`, `n 11`, `w 0`, `el 7`, `hp 320`, `atk 12`, `dmgMul 150`, `xp 40`, `goldMul 1`, `sap 0`, `picks 0`, `intro ≈ 110` (v1 §E 107 t), `death ≈ 140`, `deathSnd false`, `arena ap_oasis` | `CH` §5.4, R1 |
| rewards | the body is summoned **without** `miniboss` → ×15 gold × chapter + 2 sapphires (as Raiden); organisms pay nothing | `F:combat/gold_drop`; `CH` R5 |
| arena | `ap_oasis` (440, 201, 8), walk 26, safe 24; withered look for phases 1-2, lush for phase 3 (swap during the §2.9 white-out) | `CH` §4.4 |
| **correction** | **no `ap_cave`, no `mboss/ar/switch`**: phase 2 is played on the same field; the golden cave is only the w2 cut-scene (`MD` §0; v3 `k_f0420`, v4 §4.7) | — |
| lose path | `mboss/cb/lose` (`CH` R14) for the second Heart failure (§2.7) | — |
| music | phase 1 `music_disc.5`/`13`, phase 2 `music.nether.*`, phase 3 `music_disc.creator`/`relic` (vanilla; lengths to measure) | `CH` R11 |
| tests | `test/chapter {id:"apep"}`; module ids 1-6 (P1-P6), 20-40 (§2.10), 31-35 (Q1-Q5), 36 (종말의 여파) | `CH` §2.3 |

---------------------------------------------------------------------------------------------------

## 7. Risks and open questions

**Q1 — 양육: who is immune?**
- The binding text says "buffed organisms can't be damaged".
- `img/14.png` and the v3 caption and footage put the immunity on the **nurturing itself** while it buffs; killing the
  buffed basics makes it self-destruct (§2.5.6).
- `wiki.md:98-101` puts it on the basics.
- Recommendation: reading A (footage). Both are one switch. **Needs the user's word.**

**Q2 — What does a Heart failure cost?**
- Recommended: two strikes (§2.7). The first failure costs a non-lethal 50 % HP hit and a restart from 27 %; the second
  is a death (run over).
- Alternatives: instant run loss (faithful), or no failure.

**Q3 — 종말의 여파 lethality.**
- Proposed: 80 % max HP, lethal below that, with ≥ 85 t of dome time. The caption says "즉사기는 아니며".
- Alternative: cap it non-lethal (floor 1 HP).
- Also decide between a %-max-HP hit (needs `AZM` N7) and a coefficient hit (420 % ≈ 80 % at Lv15; less vs high-HP
  builds).

**Q4 — Progress values and stage length.**
- With the Genshin values the stage is 5-6 waves, 75-95 s.
- If the fairness sim (`S:mb3/review/fairness/sim/fgfair.py` → `apfair.py`; the agent must learn kill-the-guard-first
  and body-blocking) shows > 100 s, use +250 / +1200.
- The whole fight is then about 6 min item-less (phase 1 113 s + phase 2 ~85 s + cut-scene 9 s + phase 3 100 s pure DPS,
  plus downtime). That is long for a run boss; `hp 300` cuts about 6 %.

**Q5 — Undodgeable homing wheels.**
- These need the framework option `#pjNoDodge` (A1, 4 lines, default off). Prove Guardian/butterfly/fieldgen output
  identity (`S:mb3/tests/ident.py`).
- Fallback: a visual pj + a follower `#hzNoDodge` disc.
- Damage stays chip (≤ 3 × 6 %).

**Q6 — Barrier-block walls.**
- Leaks if a cleanup path misses them. Every exit path needs `wall/clear_all`: timeout, pause, reload, cleanup,
  death_start, uninstall, `room/remove` / `arena ensure`.
- Risk of trapping the camera / avatar.
- A wall cast onto a dash path cuts the dash short (intended).
- Test the shoulder-view avatar against barrier collision in game.

**Q7 — True damage on aux husks** runs the normal kill path and pays rewards (§2.6). Every "lose 40 % HP" / "self-destruct"
must be module-side.

**Q8 — Command and entity budget** at 8 organisms + Heart + walls (§2.5). It should fit (≈ 200 commands/tick); measure it
with the mcsim perf tool (`S:mb2/tests/dev/perf.py`).

**Q9 — Riding displays.** `tp` of a husk with passengers (HP bar + model displays) must keep them mounted. Verify once
(cm mobs only move by vanilla AI today).

**Q10 — Phase-2 location.** In place (recommended; footage) or the separate golden cave of `CH` §4.4. The latter needs
`mboss/ar/switch` and a second build, for no gameplay gain.

**Q11 — Proxies (`CH` R8).** They are blocking for both forms. Melee reach is 3.5-5 b to the husk's feet
(`F:combat/find_immediate:60-62`). The phase-1 hood is 2.6-3.7 b ahead of the anchor, the claws 5.3 b aside, the
phase-3 face 7.8 b up. Share the rigtech implementation with Azhdaha; proxies are off while burrowed (`MD` §9.1).

**Q12 — Timings not yet confirmed.**
- Phase 3 (Q1-Q5, 종말의 여파) comes only from the `kp11-kp16` key sheets and the v5 captions.
- v3/v5/v6 notes were still being written.
- The 생명의 손 leg placement (2 near + 2 far) is from v1 only.
- The 발광 slam-3 dive is from v2 §G only.
- The 양육 link radius and the 둥지 blink are not seen in the footage.

**Q13 — Player-side Dendro reactions** (Bloom/Burning on the player, `F:element/player_hit`). Keep, as the butterfly does,
unless the sim says otherwise.

**Q14 — Organism rewards.** None (aux), plus energy particles (파괴 n 4, others n 1). Should basics give anything? Genshin:
no.

**Q15 — Arena look swap mid-fight** (block slices during the white-out) and restoring the withered look for the next
fight (`ensure` with a look stamp, `CH` §4.4). Both need the arena generator change (`CH` §4.5).

**Q16 — Reload / pause in every state.**
- Transition: resume at the stage start.
- Phase 2: keep the progress, respawn the current wave, clear the walls.
- Cut-scene: jump to phase 3 ready.
- 종말의 여파: cancel, rebuild no domes, reset the cooldown.
- Fieldgen precedent: `fgcore:376-407` re-derives the state from scores.

**Q17 — `test/level`** resets `mhpM` through `level_apply` (`core:2252-2253`). The module test hook must re-split the pools
and keep the phase.

**Q18 — Shared framework edits.** These belong with the chapter-mode change, not inside the module: `mboss/floor`,
`mboss/title`, bossui `#buHpCol`, `#pjNoDodge`, proxies, `mboss/cam/*`, `pl_dot`. Azhdaha needs most of them too
(`AZM` §4.1 N-list, `CH` §3.4).
