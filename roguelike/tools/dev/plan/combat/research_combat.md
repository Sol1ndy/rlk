# Combat overhaul (parry on F, dodge replaces dash) — player-side research

Repo `/home/user/rlk`, branch `claude/exciting-pascal-ek1vuy` @ `2dcc742`, datapack root `roguelike/`. Read-only research.
Paths: `F:` = `roguelike/data/rlk/function/`, `T:` = `roguelike/tools/`, `R:` = `roguelike/README.md`, `S:` = `roguelike/tools/dev/sim/`.
`F:x/y:12` = file `x/y.mcfunction`, line 12. The balance-gauge side (pips, groggy, `bal/**`) is in
`cb/research_mobs.md`; these notes only give it a hook (`#balSrc tmp` + `function rlk:bal/parry`, as that file proposes, §4.4).

---

## 0. TL;DR

- **There are two real chokes.** (1) `F:player/take_damage` gets every "hit": all custom mobs (`cm/hit_pl` → `cm/hit_pl2`), the whole
  mid / chapter / special boss framework (`mboss/hurt` ← `hz/hurt` and `pj/hit`), 나루카미 (`boss/raiden/hurt` → `cm/hit_pl`), and vanilla
  damage (avatar `view/av_tick`, first person `player/vanilla_hit`). (2) `F:mboss/hz/hurt_pm` (per-mille boss hazards) checks the dash
  itself at `:12` and then deals damage through `mboss/pl_dot`, so it never reaches take_damage. Everything else that lowers HP
  (reaction DoTs `player/hurt_elem`, boss DoTs `mboss/pl_dot`, instant kills, the butterfly curse, void falls) is a DoT, true damage
  or a scripted kill. All of those should stay unparriable and undodgeable.
- **At the choke the attacker is not in context** (`@s` = player). Only the entry points know it: `cm/hit_pl` (`@s` = brain,
  projectile or Raiden hazard marker), `mboss/hurt` (`@s` = hazard marker or prop, which have shape and option scores), `view/av_tick`
  (`on attacker`). So the entry points must set a few one-shot "hit context" scores before calling in. The mboss framework already
  does this with `#mbNoRx` and `#mbSrc` (`F:mboss/hurt:13-16`).
- **F today is NOT "nothing".** `F:player/hotbar/tick:9` → `F:player/f_key:10` is a **second dash key**, and for the bow `:9` toggles
  aim. All eight weapon lores say "우클릭 / F 키 · 대쉬" (`F:char/*/def`). R:716 ("F(양손 바꾸기)는 아무 동작도 하지 않습니다") is
  out of date. Both have been there since the first commit `16508dd`.
- **`dashInvT` is overloaded.** It means dash i-frames and also burst-cast, motion-burst, Ronova-revive and void-fall invulnerability.
  The new dodge needs its own gametime-stamped state. Keep a generic invulnerability score for the rest.
- **Input latency is inconsistent today.** A right-click on the eye shields (`atkBlock` / `atkStrike`) is consumed at the **end** of the
  tick (`F:tick:78`), after that tick's cm and boss hits (`F:tick:48,53,58`). A right-click on a mob shield or the avatar shield is
  consumed mid-tick (`F:tick:45`), before them. F is read in `F:player/tick:43`, before cm and boss hits but after vanilla hits. A
  3-tick perfect window needs all of this made uniform (§3.4).
- **Perfect-dodge detection has a geometry problem.** The dash moves the body 1 block per tick before the hit check, so a perfect
  dodge often leaves the hit area and gets no reward. 홍련's pips already solve this with a 3-block near-miss pad
  (`T:mboss_scarlet/api.py:198-200`, `PIP_R = CUT_R + 3.0`). §7.6 extends that idea.

---

## 1. Damage pipeline to the player

### 1.1 Tick order (who hits when): `F:tick.mcfunction`
| line | step | player-damage relevance |
|---|---|---|
| 16 | `player/knockback/tick` (`rlk_plkb` marker) | applies the previous tick's knockback |
| 18 | `player/swing/tick` | |
| 23 | `view/tick` → `view/av_tick` (`F:view/tick:35`) | **vanilla hits on the avatar** → `view/av_hurt` → take_damage |
| 25 | `player/tick` | `:38` health_tick (**first-person vanilla hits**), `:43` hotbar/tick (**F detection**), `:57-63` dash timers, `:59` `dashInvT −1`, `:60` dash movement, `:73` char/tick (skill cd, energy), `:77` elem_tick (**reaction DoT on the player**), `:79` HUD |
| 45 | `combat/mshield_tick` | right-clicks on mob / avatar shields → `rclick_do` → dash (**mid-tick**) |
| 48, 50 | `cm/world`, `cm/pj/world` | **all custom-mob melee and projectile hits** |
| 53 | `boss/raiden/world` | **나루카미 hits** |
| 58 | `mboss/main` → `mboss/world:23-25` (`hz/all`, `pj/all`, `pull/all`) | **all registry-boss hits** |
| 78 | `combat/atkblock_manage` (`:4-5` polls) | right-clicks on the eye shields → dash (**end of tick**) |
| 80-81 | `dashPX/PZ` | last position, used for the next dash's direction |

### 1.2 The choke: `F:player/take_damage` (hand-written)
- `:3` `#dodged tmp 0`; `:5` `if dashInvT 1..` → `player/dash_iframe` (`#dodged 1`, the hwamu counter, crit particle); `:6` return.
- `:8-15` level scaling (`hurt_lv`, from `@s hurtLv`) and defence `K/(K+def)` (`hurt_k`), clamped to ≥1.
- `:17-22` element: `#elem = @s hurtElem`; physical with superconduct (`scT`) ×1.4; elemental (unless `#mbNRNow`) →
  `element/player_hit`. That applies the reaction to the player and changes `#dmgIn`: amplifying ×, catalyze +, and **transformative
  `rxDmg` added at once** (`F:element/player_hit:9-14`). Freeze → `frz_on_player`.
- `:24` `items/proc/taken` (선장의 팔보호대 / 불사자의 갈기 reduction, cap 60 %); `:26` 광전사 4 (more damage taken); `:29` guard
  shield `gShield`; `:30` element shield `shieldHP`.
- `:31-34` `curHealth −=`, the damage number (`hurt_do` → `hurt_text_macro`, a `dmgText` text_display).
- `:37` 불사자의 갈기 counter queue, `:39` 화무십일홍 검신합일 queue (both "when hit").
- Inputs: `#dmgIn tmp` (raw), `@s hurtLv`, `@s hurtElem`; executed `at <body> anchored eyes`. Output: `#dodged tmp`, `#hurtDmg tmp`.

**Callers of take_damage** (only five):
| caller | source | attacker known there? |
|---|---|---|
| `F:cm/hit_pl2:4` | every cm hit, and through `mboss/hurt` every boss hazard / prop hit, and every 나루카미 hit | no (`@s` = player); the caller one level up knows |
| `F:view/av_hurt:4` ← `F:view/av_tick:21` | vanilla damage on the avatar (shoulder / F5 view) | `av_tick:17-20` reads `on attacker` (element tag, level) |
| `F:player/vanilla_hit:10` ← `F:player/health_tick:10` | vanilla damage to the first-person player | via the advancement `rlk:element_hurt` → `F:element/on_player_hurt:5-10` (`on attacker`, runs at damage time) |
| `F:items/proc/hw_ctr{,_q}` | (comments only) | — |

`F:cm/hit_pl2` (hand): `:1-3` copies `#cmLv/#cmEl/#cmDmg` into `hurtLv/hurtElem/#dmgIn`; `:4` take_damage; `:5` `if #dodged 1 return`;
`:6` knockback start if `#cmKB ≥1`; `:7` `cm/hurt_fx` (red flash `damage @s 0`, `snd/f83` = `entity.player.hurt`).

### 1.3 Custom mobs (`cm/**`)
Entry `F:cm/hit_pl` (hand). `@s` is the attacker: a brain (`rlk_cmb`), a projectile, or a 나루카미 hazard marker. `:3-11` knockback
strength by tag (default 3; `rlk_cmp_ar` / `rlk_cmp_fb` 2; `rlk_cmp_cb` 4; `rlk_cmic` / `rlk_cm_im` 0), then `cm/knockback_direction`
makes `rlk_plkb_source`. `:12` `as @a[tag=player] run cm/hit_pl2`. Wrappers (hand): `F:cm/hit_me` (melee, `@s` = brain, `#cmEl 0`,
`#cmLv = mlv`) and `F:cm/hit_pj` (projectile copies `cmD/cmEl/cmLv`). Generated wrapper: `F:cm/c2/hit_el` (thunder melee,
`T:ch2mob/common.py:268`).

Every cm damage site (the "kind" column is what the choke should be told):
| site | attacker `@s` | kind | gen? |
|---|---|---|---|
| `F:cm/sw/strike:8` (`distance=..3.0` check) | brain 검사 | strike | hand (1ch) |
| `F:cm/sh/bash:15`, `F:cm/sh/rcontact:3-4` (rush contact; `:4` tags `rlk_sh_rhit` unless `#dodged`) | brain 방패병 | strike | hand |
| `F:cm/pj/ar_hit:1` → `hit_pj` | arrow `rlk_cmp_ar` | projectile | hand |
| `F:cm/pj/fb_hit:1` → `hit_pj` | fireball `rlk_cmp_fb` | projectile | hand |
| `F:cm/pj/ic_boom:9` (`#pj 1` direct + burst, `#pj 2` floor burst r2.3) | icicle `rlk_cmic` | projectile (direct) / area (floor) | hand |
| `F:cm/pj/cb_boom:5` (r2.2) | shell `rlk_cmp_cb` | area | hand |
| `F:cm/ns/hit:4`, `F:cm/sp/hit:4` | brain | strike | ch2mob/swarm.py |
| `F:cm/sl/hit:2`, `F:cm/ss/hit:2` → `cm/c2/hit_el` | brain (slime landing) | strike / area | ch2mob |
| `F:cm/kr/a_hit:2` (dash), `F:cm/kr/b_dmg:4` (spin r3, thunder) | brain 카이라기 (elite `rlk_c2e`) | strike | ch2mob/elite.py:155,189 |
| `F:cm/nj/v_dmg:2`; `F:cm/nj/shu_hit:4` | brain 닌자 (elite); shuriken `rlk_nj_shu` | strike; projectile | elite.py:271,326 |
| `F:cm/ci/r_hit:4` | brain 시킨 (dashing body) | strike | elite.py:516 |
| `F:cm/fu/hit:5`, `F:cm/em/hit:5`, `F:cm/sb/hit:3` | brain | strike | ch3mob/swarm |
| `F:cm/cs/p_dmg1:2`, `p_dmg2:2`, `e_dmg:2`, `t_dmg:4` | brain 성수 전갈 (elite `rlk_c3e`) | strike | ch3mob/elite.py:177-227 |
| `F:cm/rv/d_hit:4` (dive); `F:cm/rv/fe_hit:4` | brain 독수리 (elite); feather `rlk_rv_fe` | strike; projectile | elite.py:446,499 |
| `F:cm/pc/sp_dmg:2`, `sl_dmg:2` | brain 재구성자 (elite) | strike (area ring) | elite.py:589-600 |
| (no direct damage) | dr, cc, cw, fp | — | — |

Class tags on the brain: elite = `rlk_c2e` / `rlk_c3e`; swarm = `rlk_c2a` / `rlk_c3a`; id = `rlk_cm_<id>`. Chapter 1 has no elites.
Projectiles carry the owner's `cmId` (e.g. `F:cm/fm/ball:2`, `F:cm/ar/start:6`); owner resolution belongs to the balance side.

### 1.4 Boss framework (`mboss/**`, all generated by `T:build_mboss_core.py`)
- `F:mboss/hurt` (gen at `T:build_mboss_core.py:1225`). `@s` = hazard marker, prop or body.
  - `:12` `#dodged 0`; `:13-16` one-shot inputs `#mbNoRx`, `#mbSrc` (1 hazard, 2 projectile, 0 direct).
  - `:17-21` refused while dead, `rnDie`, `pkMode`, `#mbSt 2` (boss dying), `#mbCine 1`. `:22-24` shield-before flag.
  - `:26-29` `#cmDmg = #mbAtk × #mbHitPct × #mbDmgMul / 10000`. `:31` Bond-of-Life → `hurt_bol`.
  - `:33-36` level, knockback, `kb_src` (`rlk_plkb_source`, `:2` away from `@s` / `:3` along its yaw).
  - `:37` `unless #mbNoDodge 1` → `cm/hit_pl2`; `:39` `if #mbNoDodge 1` → `hurt_nd`. `:40-43` reset, then `hurt_ev`.
- `F:mboss/hurt_nd` (gen `:1289`): zeroes `dashInvT` around `cm/hit_pl2` and restores it. Side effect: an undodgeable hit also
  ignores burst / revive invulnerability.
- `F:mboss/hurt_bol` (gen `:1258`): `:14,:16` same two branches; `:21` `#mbHitBol` only when not dodged.
- `F:mboss/hurt_ev` (gen `:1270`): `:4` dodged → `hurt_dodge`; else `#mbHitEv +1`, `#mbHitEl/Sh/RA/Src`.
- `F:mboss/hurt_dodge` (gen `:1283`): `#mbDodgeEv +1`; `#mbDodgeOk 1` for a projectile, or a hazard with `mbHzRA 0`, `mbHzW ≥ 12`
  and `mbHzND 0` (`:2-4`). Read only by 야타용왕 brand (§2.5).
- **Hazards** (`hz/*`). Created by `hz/{disc,ring,sector,line,full,mask}` → `hz/make` → `hz/init` (gen `:1665`). Per-marker scores:
  - `mbHzK` shape (1 disc, 2 ring, 3 sector, 4 line, 5 full, 6 mask).
  - `mbHzW` tell (create → strike, ticks); `mbHzA` active ticks; `mbHzD` % of the boss hit; `mbHzE` element; `mbHzB/KD` knockback.
  - `mbHzND` no-dodge (`F:mboss/hz/init:16`); `mbHzRA` re-arm; `mbHzG` volley group; `mbHzPm` per-mille (`:22`); `mbBol`; `mbHzI` id.
  - Ticked by `hz/tick` (gen `:1808`; `:8` strike at `T = W`; `:14` `hz/hit` while `W ≤ T < W+A` and not hit).
  - `hz/hit` (gen `:1924`) tests the `rlk_body` feet with a 0.3-block pad.
  - `hz/hurt` (gen `:2008`): `:5` refused in a cine (not consumed); `:6` consumed; `:9` per-mille → `hurt_pm`; `:10-16` copies options
    (ND `:14`), `#mbSrc 1`; `:17` `mboss/hurt`; `:20` volley group marked only if not dodged.
- **Per-mille hazards** `F:mboss/hz/hurt_pm` (gen `:3359`): `:12` **its own dash check**
  (`if mbHzND 0 as @a[...,dashInvT=1..] → player/dash_iframe`); `:13` dodged → `hurt_dodge`; `:19-22` `mboss/pl_dot` (no defence,
  level, reaction or knockback; shields absorb). Users: 타키 nova (`F:boss/tachy/p/mantle/nova/hz:5-7`, `hz/full` 250 ‰), 아펩 ×3,
  아를레키노 ×1.
- **Projectiles** `F:mboss/pj/hit` (gen `:2285`): `:4` cine refusal; `:5` consumed; `:6-12` options (`mbPjND` → `#mbNoDodge`), `#mbSrc 2`;
  `:13` `mboss/hurt`; `:16` group mark unless dodged; `:17-20` module hook `d/pj_end` (`#pjEv 4`, `#pjKeep`).
- **DoTs** `F:mboss/pl_dot` (gen `:3239`) → `pl_dot2` (gen `:3262`). `pl_dot2:2-3,20` zero and restore `dashInvT`; ‰ of max HP,
  guard / element shields, `#mbDotLethal`; damage number. Callers: `F:boss/azhdaha/brand/dot:8` (brand DoT),
  `F:boss/arlecchino/bond/dot:9` (Bond of Life), `F:boss/apep/p/fail/strike:7` (mechanic fail), `F:boss/scarlet/ult/fail60:7`
  (A8 fail 50 %), cproto, and `hz/hurt_pm`.
- Not damage to the player: `mboss/line/*` is the dialogue-line system; `aux_hit` and `px/*` are the player hitting the boss. "pdisc"
  is not a framework function: it is 홍련's HITS shape "disc at the player's spot" (`T:mboss_scarlet/api.py:140,152`), built as a
  `hz/disc`.
- Hazard option counts per module (generated tree): `#hzNoDodge 1` 야타용왕 29 files, 아펩 3, 역장 4. `#hzRearm` 야타용왕 9, 아펩 1,
  역장 1, cproto 1. `#hzPm` 아펩 3, 아를레키노 1, 타키 1. Most module hazards are **quiet and made only a few ticks before the strike**
  (`tell < 12` in 72 / 78 아를레키노, 34 / 35 타키, 11 / 12 홍련, 44 / 64 파수꾼, 15 / 17 나비, 37 / 56 역장; 아펩 16 / 77 and 야타용왕
  2 / 151 use long ground tells). The module's pose is the telegraph, so `mbHzW` **cannot** decide parriability (§7.4).
- Boss identity at `mboss/hurt`: one body `@e[type=husk,tag=rlk_mb_body]` (tags `boss`, mid also `miniboss`). `#mbId` = registry n;
  `#mbKind mb` 0 mid / 1 chapter / 2 special (`F:mboss/fight_vars:7,20-22`). Hazards and props store no owner. 아펩's organisms
  shoot framework props (`F:boss/apep/org/pj_end`), so "attacker = boss body" is a default, not always true.

### 1.5 나루카미 (own hazard engine, generated by `T:build_raiden_hazards.py` / `T:raiden_enc/core.py`)
- Hazard marker `rlk_rd_hazard`; kind `rdHK` (1 disk, 2 annulus, 3 / 4 rect, 5 sweep, 6 slab, 7 orb, 8 follow, 9 field, 10 safe dome:
  `F:boss/raiden/hazard/hit:10-25`); tell `rdWind`; tags `rlk_rd_nododge` (`F:boss/raiden/hazard/new:29-30`), `rlk_rd_jump`.
- `F:boss/raiden/hazard/land:1-11` (gen `T:build_raiden_hazards.py:434`): `:7` `#dodged 0`; `:8` nododge → `land_nd`; `:9` → `hurt`;
  `:10` knockback unless dodged.
- `F:boss/raiden/hazard/land_nd:1-7` (gen `:446`): zeroes and restores `dashInvT`, sets `#rdNoDodge`.
- `F:boss/raiden/hurt:1-23` (gen `T:raiden_enc/core.py:433`): `:2-4` refusals; `:8-20` balance multiplier; `:21` **`cm/hit_pl` with
  `@s` = the hazard marker**; `:23` rage +60 only if not dodged.
- `F:boss/raiden/hazard/fatal:1-7` (만겁 outside the dome, from `k/safe_dome:4`): direct `curHealth 0` + `player/die`.

### 1.6 HP loss that bypasses take_damage
| file | what | keep as |
|---|---|---|
| `F:player/hurt_elem:1-11` ← `F:element/dot:10` ← `element/ec_tick:15`, `element/burn_tick:15` (player burning / electro-charged ticks from `player/elem_tick` → `element/tick`) | reaction DoT, no defence; `:2` returns while `dashInvT` | DoT: unparriable, undodgeable, generic i-frames only |
| `F:mboss/pl_dot2` (above) | boss DoT / ‰ hits | unchanged (already ignores i-frames) |
| `F:mboss/butterfly/coc/apply_pl:8-16` | 20 % of current HP curse | bypass |
| `F:boss/scarlet/ult/fatal:1-9`, `F:boss/raiden/hazard/fatal:1-7` | instant kills | bypass |
| `F:mboss/cb/lose:4` | objective loss | bypass |
| `F:room/fall/player:2-7` | void fall % max HP, then `:14 dashInvT 20` | bypass |
| `F:items/proc/{hw_cost:11, salon_pay:7, gring_start:5}` | self costs | bypass |

### 1.7 Vanilla damage
Only `#mobTmp room 1` temporary vanilla mobs and environmental damage reach it (cm brains only target their lures,
R:824-842). In shoulder / F5 view the real player ignores vanilla damage (`F:player/vanilla_hit:2`), and the mannequin avatar takes it
(`F:view/av_tick:1-21`; `:5-10` a hit by the real player is cancelled). In first person `F:player/vanilla_hit:4-10`. Attacker:
`on attacker` (`av_tick:19-20`, `F:element/on_player_hurt:5-9`). A projectile's `on attacker` is the shooter.

---

## 2. The dash, all of it

### 2.1 Input
| path | files | timing |
|---|---|---|
| Right-click on the eye shields `atkBlock` (0.32 cube 0.30 ahead) / `atkStrike` (1.4 cube 1.6 ahead) | `F:combat/atkblock_manage:4-5` → `atkblock_poll:3` / `atkstrike_poll:3` → `F:combat/input/poll_right:1-8` (owner by `on target`) → `F:combat/rclick_do:12` (`player/dash`) / `:13` bow (`char/bow/rdash`) | **end of tick** (`F:tick:78`) |
| Right-click on a mob shield or the avatar shield `rlk_avsh` | `F:combat/mshield_tick:3` → `mshield_rclick:2` → `poll_right` | mid-tick (`F:tick:45`) |
| F5 ride view (`#vmode view 2`) and map | items made consumable (`F:view/ride_tick:23-25`); advancement `rlk:rc_use` (`using_item`) → `F:combat/rc_use:1-2` (`rcU`) → `F:view/ride_tick:26` / `F:view/map_tick:10` → `F:combat/rc_hold:2-5` (first tick, then every 4) → `rclick_do` | in `view/tick` (early) |
| **F (plain)** | `F:player/hotbar/tick:9` → `F:player/f_key:9` bow aim toggle / `:10` `player/dash` | in `player/tick` |

`rclick_do` refusals: `:1` rdCam, `:3-4` map, `:6` pkMode, `:8` burst cast `buT`, `:9` `rnDie`.
`f_key` refusals: `:2` vMap, `:3` pkMode, `:4` dead, `:5` buT, `:6` rnDie.
Holding right-click repeats the interaction every 4 ticks (vanilla), gated by `dashCool` and charges.

### 2.2 Charges, cooldowns, movement
- `F:player/dash:1` refuses during 스커크's own fast move `skDash`; `:2` rdCam; `:3` `pmMoveLock`; `:6` self-cool `dashCool`; `:7` no
  charge → `dash_fail` (`snd/f228` bass); `:8-9` −1 charge, `dashCool = #dashCoolT`; `:10` `dash_go`.
- `F:player/dash_go:1` ends the current motion; **`:4 dashInvT 6`**; `:6-10` cancels the combo (`comboStep 0`, `pmAtkPending`, `naQ`,
  `atkCD 0`); `:11-12` sounds `snd/f226` (`entity.wind_charge.wind_burst` 0.9 1.4) and `f227` (`entity.breeze.slide` 0.7 1.5);
  `:13` cloud; `:15` `dash_dir`; `:17` `char/motion/dash`; `:19` `items/hook/on_dash`.
- Direction `F:player/dash_dir:2-18`: last tick's delta (`dashPX/PZ`, saved at `F:tick:80-81`). Shoulder view uses the input vector
  (`F:view/dash_dir:2-5`). Fallback is the look vector (`dash_lookvec`). `dash_norm`.
- `:21-27`: 1 block per tick for 3 ticks (`dashMoveT 3`).
- Movement `F:player/dash_move_tick:1-23`: four 0.25-block sub-steps per tick (`dash_sub` with axis-split collision `dash_chk_*`,
  one-step climb `dash_up_x/z`), `:22` `items/hook/on_dash_move`. Run at `F:player/tick:60`.
- Regen `F:player/tick:58` → `dash_regen:2-3` → `dash_refill:2-4` (+1 charge, `snd/f229` amethyst chime). Self-cool `:57`. **I-frames
  `:59` `dashInvT −1` per tick.**
- Constants `F:load:810-815` (`#dashMaxBase 2`, `#dashRegenBase 20`, `#dashMax`, `#dashRegenT`, `#dashCoolT 5`). Engraving 질주
  `F:load:930-932` → `F:engravings/scan_more:1-6` (+1 charge, +20 % regen, clamp), `F:engravings/dash/regen:1-5`.
- Objectives `F:load:61-71,529`; init `F:player/init:46-50`; uninstall `F:uninstall:225-236`.

### 2.3 Effective i-frame windows today (follows from 1.1 and 2.2)
- Click on the eye shields arriving before tick N: `dash_go` runs at the end of N, so the hit in tick N is **not** avoided.
  - cm / boss hits avoided in N+1..N+5 (`:59` decrements before them: 5, 4, 3, 2, 1).
  - Vanilla-avatar hits avoided in N+1..N+6.
- Click on a mob shield: hits avoided in N..N+5 (6 ticks).
- So the window depends on what the crosshair is on.

### 2.4 HUD
`F:player/hud/tick:4-13` (key = charges × 100 + progress; `build` / `build_slot` / `part`; `:31-32` actionbar layout HP · dash gauge
· energy · gold · dice). Colours and segments in `F:player/hud/setup:1-6`, `#hudSeg 15` (`F:load:826`). Under dodge: unchanged
(charges = dodge charges); comments and README §2 wording only.

### 2.5 Every reader of the dash state, and what it should become
**`dashInvT` writers** (all but the first are not dashes):
- `F:player/dash_go:4` → replace with a dodge stamp (§7.2).
- Generic invulnerability, kept as a separate score (call it `invT`; rename or keep the old name):
  - `F:char/burst_wind:6-7` (cast + `#burstInv 8`, `F:load:736`)
  - `F:char/motion/events/{navia/burst:9, skirk/burst_jin:5, skirk/burst_metsu:5, arle/burst:5}` (`#pmInv`; hand files)
  - `F:char/ronova/revive:18-19` (`#rnDieT 60` + 20)
  - `F:room/fall/player:14` (20)
- Zero-and-restore tricks become a flag instead: `F:mboss/hurt_nd:2-5`, `F:mboss/pl_dot2:2-3,20`, `F:boss/raiden/hazard/land_nd:2-3,7`.

**`dashInvT` readers:**
| reader | today | under dodge |
|---|---|---|
| `F:player/take_damage:5` | any `dashInvT` = dodged | generic `invT` → avoided; then the dodge / parry judge (§7) |
| `F:player/hurt_elem:2` | DoT avoided while dashing | `invT` only (a dodge does not cancel burning / electro-charged) |
| `F:player/knockback/start:7`, `tick:10` | no knockback while i-framed | `invT` or the dodge window open (keep the feel) |
| `F:mboss/hz/hurt_pm:12` | own dash check | call the judge (boss, area, unparriable, ND = `mbHzND`) |
| `F:boss/scarlet/shield/pip:9-10` (gen `T:mboss_scarlet/shield.py:59-70`; rule `T:mboss_scarlet/api.py:198-200` `PIP_RULE`, `PIP_DASH {0:(1,6),1:(1,5)}`, `PIP_R` 6.2) | pip breaks when `dashInvT 1..6` at strike `s` / `1..5` at `s+1`, feet within 6.2 | pip breaks on a **perfect dodge** (stamp within 0..2 ticks of `s`, origin within `PIP_R`) or a **tier-3 parry** of that cut. Re-tune the S5 targets T6 / T7 (R:2159-2160) |
| `F:player/dash_iframe:1-5` | `#dodged 1` + hwamu + crit particle | split into `def/iframe` (generic) and the judge's dodge branch |

**`dashMoveT` readers** (motion-based, keep as they are):
- `F:view/move:23` (input does not move the avatar mid-dash), `F:view/rot:40` (camera hold `#viewDashHold`), `F:view/map_open:38`.
- `F:char/motion/combat/request:7` (no attack start), `char/motion/control/lock:4` (lock cancels the dash),
  `char/motion/loco/observe:32` (loco mode 2), `F:char/navia/aim_start:4`, `F:char/clorinde/auto_tick:3` (stops auto-fire).
- `F:player/nudge:2`, `F:room/fall/tick:3` (no void check mid-dash), `F:room/fall/player:8`.
- `F:mboss/push/capsule:11` (no body push mid-dash), `F:mboss/mv/lv_sample:3` (predictive aim skips dash ticks),
  `F:player/knockback/start:8` and `tick:11`, `F:char/burst_wind:8`, `F:char/ronova/revive:20`,
  `F:items/hook/tick_player:79` (lifeline fires after the dash).

**Charge readers:** `F:player/hud/*`, `F:engravings/scan_more:6`, `F:char/bow/rdash:3` (cancel aim only if a dash will happen). Keep.

**Items and engravings** (`F:items/hook/on_dash:1-17`, `on_dash_move:1-9`). Keep on every dodge, because the dodge is the same motion:
- 키리온 dash slash (`on_dash:3-5`, `on_dash_move:3-5`); 고통 & 절망 stacks (`:7`); 질주 4 dash-through wind damage (`:9`,
  `on_dash_move:7` → `engravings/dash/hit`); 열혈 저울 (`:11`); 선학의 깃 (`:13`); 생명줄 (`on_dash_move:9` + `tick_player:79`).
- Tutorial counter (`:17`); text "1. 이동과 대쉬" and target "대쉬 3번 하기" in `F:lobby/tut/s1:2,5` → rename to 회피 and add a parry step.
- 화무십일홍: `:15` → `F:items/proc/hw_dash:1-5` stamps `#hwDashEnd = now+6` only so that `hw_ctr_q:5-6` can tell a real dash from
  burst / fall / revive i-frames (test `S:hr/tests/test_hwamu.py:583-613`, F3 HR-09). With a separate dodge state this stamp is no
  longer needed (§5.2).

**Characters:**
- 스커크 `skDash` blocks the dash (`F:player/dash:1`). Keep, or allow the dodge to cancel it (decision).
- Bow (요이미야 only, `weaponType:"bow"`): `rclick_do:13` → `F:char/bow/rdash:1-4` (cancel aim, then dash). Keep.
  **F = aim toggle** (`F:player/f_key:8-9` → `char/bow/toggle`) **conflicts with F = parry**. Aim needs a new input (options §3.3).
- Rig clips: `char/motion/dash` (generated, `T:build_player_rig.mjs:448-455`) plays `dash` for 아를레키노 / 스커크 / 나비아. Keep as the
  dodge clip.
- All 8 weapon lores (`F:char/*/def`): "우클릭 / F 키 · 대쉬". 요이미야: "F 키 · 조준 사격", "당기는 중에 F 키나 우클릭(대쉬)을 누르면 쏘지
  않고 취소된다". Rewrite to "우클릭 · 회피", "F 키 · 패리".

**Bosses and the dodge events:**
- 야타용왕 brand: `F:boss/azhdaha/brand/tick:5-7`, `brand/dodge:1-8` (gen `T:mboss_azhdaha/brand.py`) cleanses on `#mbDodgeOk`
  (once per 40 t). Redefine `#mbDodgeOk` = perfect dodge or tier-3 parry.
- 야타용왕 29 · 아펩 3 · 역장 4 `#hzNoDodge` hazards (R:1690-1691 "대시로 못 피하는 공격", the fieldgen shockwave you must jump,
  R:1471,1480): keep as undodgeable, and also make them unparriable by default.
- 나루카미 `rlk_rd_nododge` (돌진, 수천수만의 염원, guard recovery, 만겁 베기; R:1194): undodgeable and unparriable.
  `boss/raiden/hurt:23` rage only on landed hits: a tier-3 parry counts as not landed (`#dodged 1`).
  `hazard/land:10` knockback only when landed: also skip it on any parry.
- 타키: no direct reader. The nova (`hz/full` 250 ‰ `hzPm`, 44-tick module tell) becomes "perfect dodge only".
- 아펩 organism bolt `F:boss/apep/org/pj_end:5`: a dodged bolt flies on to the Heart. A **parried** bolt should end, so the hook needs a
  parry state distinct from `#dodged`.
- 역장 rock `F:mboss/fieldgen/p/rock/pj_end:3`: counts undodged slab hits. Decide whether a tier 1–2 parry counts.
- Framework pull `F:mboss/pull/start:2` (a dash does not stop it) and push capsule: unchanged.
- Raiden module tests `rd/tests` and the boss balance probes assume dash i-frames (§7.8).

**Tests and sims that model `dashInvT`:**
- `S:hr/tests/lib/hrsim.py:307-310,520-575` (`s.dash()` sets `dashInvT` 6..0 before `mboss/main`).
- `S:*/lib/azsim.py` `iframe_end` (e.g. `S:hr/tests/lib/azsim.py:198,369-402`), `S:ar/tests/pat_p2.py:79`.
- `S:az/tests_cm/test_fw_az.py:64,78,92-95,286` ("3c dash i-frames do not block it (and are restored)"); `S:az/tests_cm/test_fw_ap.py`
  (4 refs, ‰ hazards).
- `S:ar/tests/test_cm_ar.py:105-137` (FN-1 dodge); `S:hr/tests/test_scarlet.py:25,212,526-552,614` (pip windows);
  `S:hr/tests/test_hwamu.py:133-139,583-613`; `S:hr/tests/pat_ghost.py:463,499` (dash agent, `dash_economy`).
- Balance-probe agents: `S:ar/review/bal/` (`azfair_core.py` dodge policy), old fairness sims `S:mb2/balance/fsim.py`,
  `S:mb3/fgfix/sim/fgfair.py`, `S:tele/fg/sim/fgfair.py`.

---

## 3. Input

### 3.1 How F is detected now
- The swap packet swaps main hand and offhand on the server between ticks. Next tick `F:player/tick:43` → `F:player/hotbar/tick`:
  - `:5` offhand has the attack item and `sneakT ≥ 1` → `lvup/toggle` (Shift+F menu)
  - `:7` offhand has a blank item (pick room) and `sneakT ≥ 1` → `lvup/toggle`
  - `:9` offhand has any `rlk_ui` item and `sneakT 0` → `player/f_key`
  - `:10` clear the offhand; `:12` `hotbar/place` re-creates slot 0 (`fix_attack` → `char/weapon_item`); `char/hotbar` rebuilds the
    skill and burst slots.
- `sneakT` = stat `minecraft.custom:minecraft.sneak_time` (`F:load:245`), reset to 0 every tick in `F:lvup/tick:4` (after
  hotbar/tick reads it). It means "was sneaking during the last player tick".
- In F5 ride view the stat does not count (R:2450), so there a sneak **tap** toggles the menu (`F:lvup/tick:8-15` via predicate
  `rlk:in_sneak`).
- `lvup/toggle` refuses in combat (`F:lvup/toggle:5`, "전투 중에는 이동할 수 없습니다").

### 3.2 Reliability of a plain-F detector
- **Works only with a UI item in the main hand.** Hotbar 0–2 (weapon / skill / burst) qualify. Slots 3–8 are kept empty
  (`F:player/inv/manage:11` `sweep_stray`), so F there swaps air with air and nothing can be seen. The pick room fills 0–8 with
  blanks (`F:player/hotbar/blank`).
  - Fix if wanted: give 3–8 an invisible `rlk_ui{role:"pad"}` filler, like the pick room. That changes inventory handling, so it is a
    decision.
- **Shift+F vs F race.** The client handles key binds before it sends the tick's input packet, so Shift and F in the **same client
  tick** reach the server as "F, not sneaking". Holding Shift at least one tick first works. Use `if predicate rlk:in_sneak` **or**
  `sneakT ≥ 1` (the predicate is up to 1 tick fresher). Since Shift+F is refused in combat anyway, in combat treat Shift+F as a parry
  too (no deny message).
- **Key repeat.** Holding F auto-repeats (OS repeat → `KeyMapping.click`, the same reason holding Q keeps dropping), so a parry
  needs a commit / lockout (§7.1).
- An open inventory screen: F over a slot swaps that slot with the offhand. Only `rlk_ui` items in the offhand count today; keep that
  filter.
- **Latency.** Detection sees the press in the first function run after the packet: gametime G_press = the gametime of that tick.
  - Hits that run later in the same tick (cm `F:tick:48,50`, 나루카미 `:53`, bosses `:58`) can be judged with offset 0.
  - Vanilla hits in `view/tick` (`:23`) and `health_tick` (`player/tick:38`) run before `player/tick:43`, so they see the press one tick
    late. Fix: move the F detection into a tiny pre-pass at the top of `rlk:tick` (§7.1).

### 3.3 The bow conflict (decision for the user)
F is 요이미야's aim toggle today. Options:
- (a) Shift + right-click = aim. Conflicts with the F5 ride-view sneak tap menu, `F:lvup/tick:8-15`.
- (b) A second F within N ticks = aim. The first press still parries.
- (c) Hold right-click = aim, tap = dodge. Adds dodge latency; rejected for a 3-tick window.
- (d) Move aim to the skill slot's left-click (`char/cast_skill` vs `cast_skill_r`).
Recommended default: (b) or (d).

### 3.4 Right-click (dodge) timing
- The interaction NBT holds `interaction:{player,timestamp}` (and `attack:{…,timestamp}`). The left-click already has an immediate
  path: advancement `rlk:attack` (`player_hurt_entity`) → `F:combat/input/attack_event` with a `lcSeen` / timestamp de-dup
  (`F:combat/input/attack:4-5`). The right-click has none.
- Fix (either):
  - (A) Run the `atkBlock` / `atkStrike` right-click polls (`F:combat/atkblock_manage:4-5`) at the **top** of `rlk:tick` (before
    `view/tick`). Placement and spawn stay at the end. Cheapest, and it keeps the ordering comment true ("위치 갱신/제거보다 먼저").
  - (B) Add an advancement `player_interacted_with_entity` (entity = interaction with tag `atkBlock` / `atkStrike` / `rlk_mshield`) →
    dodge in packet context, then de-dup the later poll by `interaction.timestamp` (`rcSeen`, like `lcSeen`).
- Either way stamp the dodge with **gametime**: with (A) `time query gametime`; with (B) `interaction.timestamp`, which equals the
  next tick's gametime because packets between ticks read the already-incremented level time.
- The mob-shield poll (`F:tick:45`) and the F5 ride path (in `view/tick`) are already before the hits.
- Note for (A): poll-path left-clicks would also move to the top. That matches the advancement path; recheck `#pmChainOpen`
  (`F:player/tick:47-50`) with the arlecchino / navia chain tests.

---

## 4. Element skill cooldown and energy

- **Skill cooldown** `@s skillCd` (ticks). Decrement `F:char/tick:3`. Set on cast `F:char/cast_skill:12` (`#skillCdT` from
  `F:char/load_cur:13`), then `char/cd_reduce` (모래시계 조각 / 순환 2, multiplicative).
  - Per character: 클로린드 `char/clorinde/cast_skill:6`; 스커크 `char/skirk/mode_end:7`, `dash_end:5` (0 while 일곱빛 섬광 runs);
    로노바 `char/ronova/doom:6`; 아를레키노 burst resets to 0 (`char/arlecchino/burst:24`).
  - **나비아 and 네페르 ignore skillCd.** Their charge timers set it every tick: `F:char/navia/tick:3-9`
    (`skillCd = nvCdE − nvCT` while `nvC 0`) and `F:char/nefer/tick:5-9`; charge `char/{navia,nefer}/charge` resets `nvCT/nfCT 0`.
- **Existing flat cut** `F:engravings/cd_cut:1-4` (`#cut eng` ticks, clamp 0), used by 순환 4 (`F:char/particle_absorb:4-5`) and
  뇌전 4 (`F:engravings/thunder/rx:8-13`). **It is a no-op for 나비아 and 네페르** (an existing gap).
- **Safe "−1 s"**: a new `char/cd_cut` (`#cut` = 20):
  - `#charN 6` and `nvC ≤ 1` → `nvCT += 20` (the charge fires next tick in `navia/tick:6`)
  - `#charN 8` and `nfC ≤ 1` → `nfCT += 20`
  - else if `skillCd ≥ 1` → `scoreboard players remove @s skillCd 20` (positive literal; R:242 forbids negative literals) and clamp to 0
  - Point `engravings/cd_cut` at it to fix the gap.
  - The judge runs inside `cm/world` / `mboss/main`, after `char/tick` (`player/tick:73`), so the display updates next tick. No race.
- **Energy** `@s energy` ×100 (100 = 1 point). Cap `#burstCost100` (`F:char/load_cur:16`); clamp `F:char/tick:5`;
  `energyPt = energy/100` (`:6-7`).
  - Normal gain `F:char/energy_add:3-7`: × `energyRecharge` %, and **returns for 스커크** (`#charN 3`: her energy bar is 뱀의 계략, gained
    only from skill / rifts, drained in 일곱빛 섬광 `char/skirk/mode_tick:3`).
  - "+10 energy" flat: `scoreboard players add @s energy 1000` + clamp as `energy_add:7`. Through ER% instead: `#enAdd 1000` →
    `char/energy_add`. Decide 스커크 (give 뱀의 계략, or nothing).
- **HUD**: actionbar energy gauge `F:player/hud/tick:23-29` (`en_build` / `en_set`, `storage rlk:hud enbar`, `#hudEnSeg 15`); the burst
  slot item name gauge (`buShown`, reset in `en_build:5`); the skill slot item **count** = remaining seconds rounded up
  (`F:char/hotbar:2-29`, `skShown`). All refresh by key compare, so the new code only changes the scores.

---

## 5. Invulnerability, knockback, stagger, counters

### 5.1 Today
- **Invulnerability**:
  - `dashInvT` (§2.5).
  - Framework refusals: `mboss/hurt:17-21` (dead, `rnDie`, `pkMode`, boss dying, cine), `pl_dot:6-10`, `hz/hurt:5` and `pj/hit:4`
    (cine: refused, not consumed), `boss/raiden/hurt:2-4`.
  - The real player in shoulder view ignores vanilla damage (`vanilla_hit:2`); Raiden camera `rdCam`.
  - Shields absorb before HP (`take_damage:29-30`). Damage reduction items, cap 60 % (`items/proc/taken:1-11`).
- **Knockback**: `player/knockback/{start,tick,step,check}`. A marker `rlk_plkb` faces the recoil; `pkbT` 0.1-block steps decaying 1
  per tick; source `rlk_plkb_source` from `cm/knockback_direction` or `mboss/kb_src:1-3`.
  - `start:2-8` refused while dead, at 0 HP, `rnDie`, `pkMode`, `vMap`, `dashInvT`, `dashMoveT`; `:15-16` cancels `stepT`, stops the
    avatar (`view/stop_h`). Started only by `cm/hit_pl2:6`; 나루카미 has its own `hazard/kb`.
  - Displacement: framework pull `mboss/pull/*` and push `mboss/push/*`. Vanilla knockback applies only in first person.
- **Stagger / control on the player**: none as a hit-stun.
  - Freeze reaction (`element/frz_on_player:1-2`, movement and jump ×0, `frz_end`); burst cast lock (`char/burst_wind`, movement −100 %);
    motion lock `pmMoveLock`; swing slow (`player/swing`); low gravity (`mboss/lowg_*`).
  - Hit feedback = `cm/hurt_fx` (red flash + `entity.player.hurt`) and the damage number (`player/hurt_do`).

### 5.2 Counter mechanics that should become parry / dodge triggers
| mechanic | today | proposal |
|---|---|---|
| 화무십일홍 「검신합일」 (`items.md:1599`; `F:player/take_damage:39`, `F:player/dash_iframe:4` → `F:items/proc/hw_ctr_q:1-9` → next item tick `hw_due` → `hw_ctr:1-27`, 138 % thunder to the nearest enemy in 12 blocks, cd `#hwCtrCdT 80`, `F:items/tune/b10:39-40`; `hw_dash` stamp) | "공격을 받거나 대쉬로 흘려내면" | "패리(any tier, or tier ≥ 2) 또는 완벽 회피". Drop or keep "being hit" (user decision; lore + items.md text). `hw_dash` becomes unnecessary. Re-run `test_hwamu` |
| 불사자의 갈기 (`take_damage:37` → `items/proc/lion_queue:1-2`, cd `#lionCdT 40`) | counter when hit | keep "when hit". Optionally not on tier 3 (no hit landed) |
| 야타용왕 brand cleanse (`#mbDodgeOk`) | "perfect dodge" = dodged one-shot ≥ 12 t / projectile | perfect dodge **or** tier-3 parry (`hurt_dodge` gen `T:build_mboss_core.py:1283`) |
| 홍련 shield pips / 자영 연참 (A8 · A13) | dash i-frames at the cut's strike | perfect dodge (near-miss `PIP_R`) or tier-3 parry. The "대시 경제" note (R:2142) and T6 / T7 (R:2159-2160) need a re-run |
| 나루카미 malice | +60 per landed hit | unchanged via `#dodged` |
| 방패병 rush contact (`cm/sh/rcontact:4`) | a dodge keeps the rush going | a parry should **consume** the contact (blocked) |
| framework volley group (`hz/hurt:20`, `pj/hit:16`) | the first landed hit disarms the volley; a dodge does not | decision: a tier-3 parry marks the group (one parry blocks the volley) or not (each prop must be parried) |
| item hooks `on_dash` / `on_dash_move` | dash | fire on every dodge. A new `items/hook/on_pdodge` / `on_parry` lets later items key off perfect actions |

---

## 6. Visual and sound resources for the three parry tiers and the perfect dodge

### 6.1 Where the avatar is
- Shoulder / F5 view (the default): `@e[tag=rlk_av,limit=1]`, a **mannequin** (`F:view/spawn:8`; tags `rlk_view rlk_av rlk_body
  rlk_pet`) that carries `rlk_body`. The real player is invisible with gravity 0 (`F:view/spawn:24-28`).
  - Rig characters (아를레키노, 스커크, 나비아) hide the mannequin (`F:char/motion/hide_avatar:1-3`) and show display parts `rlk_pm`,
    posed in `char/motion/tick` (`F:player/tick:104`).
- First person: `rlk_body` is the player (`F:view/fps_tick:3`, `F:view/tick:25`); there is no avatar.
- Anchor rule already used by 홍련's deflect (`F:boss/scarlet/shield/judge:8-11`):
  - avatar: `at @e[tag=rlk_body] … positioned ~ ~1.3 ~`
  - first person: `positioned ~ ~1.62 ~ positioned ^ ^ ^1.8` (in front of the eyes)
- The Navia card system drops clip cards in first person (`#pmFxFP`, `F:fx/nv/spawn:11-13`).

### 6.2 Particles (vanilla, already used in this pack, so known to load in 26.3)
- `flash{color:[r,g,b,a]}` (tinted flash: `F:room/rift/grow`, `F:mboss/fieldgen/fx/p/warp_out`)
- `dust{color,scale}`, `dust_color_transition{from_color,to_color,scale}`
- `end_rod`, `crit`, `enchanted_hit`, `electric_spark`, `sweep_attack`, `firework`, `glow`, `wax_on/off`, `poof`, `cloud`, `gust`,
  `damage_indicator`, `block{block_state}`, `snowflake`, `cherry_leaves`

Suggested sets (all `force @a[tag=player]` at the anchor; 6–15 commands per event):
- **Tier 3, perfect parry** (gold-white): `flash{color:[1f,0.93f,0.62f,1f]}` ×1; `crit` 0.25 spread 0.6 ×14; `end_rod` 0.12 ×8;
  `firework` 0.15 ×6; `dust{color:[1f,0.85f,0.35f],scale:1.2}` ×8. Same palette as 홍련's deflect `clash_gold`.
- **Tier 2** (cool white-blue, smaller): `flash{color:[0.75f,0.88f,1f,1f]}`; `crit` ×8; `electric_spark` ×6.
- **Tier 1** (dull): `crit` ×4; `poof` ×3; `dust{color:[0.7f,0.7f,0.7f],scale:0.9}` ×4. No flash.
- **Perfect dodge** (red; new):
  - `flash{color:[1f,0.12f,0.12f,1f]}` at the **dodge origin**
  - a ring of `dust_color_transition{from_color:[1f,0.2f,0.2f],to_color:[0.25f,0f,0f],scale:1.4}`
  - a red `dust{color:[1f,0.1f,0.15f],scale:1.6}` trail on each move tick (from `items/hook/on_dash_move`, gated by a flag)
  - `end_rod` streaks back toward the body when the +10 energy lands

### 6.3 Display geometry
- **Without the resource pack**: tinted `text_display` panels. `F:view/shield_build` builds a hexagonal bubble from text_displays with
  ARGB `background` (`F:view/shield_on:3-7`). A one-tick-to-six-tick red / gold panel ring or a flat flash quad works the same way.
  Damage-number style text exists (`player/hurt_text_macro`, aged by `combat/text_tick`). No "PERFECT" text: the 10-21 text rule
  (R:237-240) only allows real game wording, and Stellar Blade shows none.
- **Gold cards (Navia kit)**: `F:fx/nv/card {kind, pos, rot, bb, roll, spin, s0, s1, move, life, fade}`. Kinds: rose, star, burst,
  crescent, petal, shard, ring, glow. Presets `fx/nv/p/*` (e.g. `hit_star`, `hit_ring`, `flash_glow`). Aged pack-wide by
  `fx/nv/world` (`F:tick:72`); cap 48. Gold only (`item_model rlk:navia_fx/<kind>`); generator `T:build_navia_fx_cards.py`.
  Usable now for tier 3 (gold star or burst, ring).
- **Tinted cards**: the boss kits use `custom_model_data.colors` tint (`F:boss/scarlet/fx/e/spawn` `colors:[$(col)]`), e.g. 홍련
  `fx/p/clash_gold`, `clash_spark`, `star4`, `pip_break`, `light_column`. Do not reuse a boss kit pack-wide (its pool, ager and cleanup
  belong to the fight). Better: a small player kit `fx/pd/*` cloned from `T:build_navia_fx_cards.py` with a tint channel → one red
  set for the perfect dodge, white / gold / blue for parry. Atlas headroom is ~0.28 M px (R:198, R:290); 4–6 small 64 px textures are
  enough. Needs the resource pack (R:51-53) and `rplint`.

### 6.4 Rig motions (`char/motion`, generated by `T:build_player_rig.mjs` + `T:build_player_locomotion.mjs`, sources `T:player_motion/{arle,skirk,navia}.json`, audio `T:build_player_audio.py`)
- Only 아를레키노, 스커크 and 나비아 have rig clips (`F:char/motion/clips/{arle,navia,skirk}/*`, each with a `dash` clip). A
  parry / guard clip means a new clip per rig character + RP + regen. Leave it for a later step.
- Mannequin characters (루미네, 요이미야, 클로린드, 로노바, 네페르): `swing @e[tag=rlk_av,limit=1] offhand|mainhand` (the `cm/swing`
  pattern). Nothing to show in first person.
- Perfect-dodge afterimage: an option is a brief red glow on the avatar via a red-coloured team. Risky: the avatar sits in team
  `rlk_stun` (`F:view/spawn:29`; teams `F:load:1225-1229`), so prefer particles or cards.

### 6.5 Sounds (vanilla only, R:233)
Ids checked against `S:rd/tests/sound_ids.txt`. The once-per-tick wrapper `snd/fN` + `#kN snd` is hand-maintained now (its generator
`build/psnd.py` is gone).
- Tier 3: `block.anvil.land` 0.5 1.8 + `item.trident.hit` 0.8 1.4 + `block.amethyst_block.resonate` 0.7 1.6. Alternative
  `entity.breeze.deflect` 1 1.2. 홍련's deflect is `anvil.land 0.6 1.4` + `entity.player.attack.crit 0.8 1`
  (`F:boss/scarlet/fx/snd/deflect`).
- Tier 2: `item.shield.block` 0.8 1.3 + `entity.player.attack.crit` 0.6 1.5.
- Tier 1: `item.shield.block` 0.7 0.85.
- Perfect dodge: `entity.illusioner.mirror_move` 0.8 1.3 + `entity.breeze.slide` 0.6 0.8. The +10 energy can use
  `block.amethyst_block.chime` 0.7 0.8 (charge refill already uses chime 1.6, `snd/f229`).
- The dodge itself keeps `snd/f226` / `f227`.

---

## 7. Proposed architecture

### 7.1 Parry state (per player; gametime stamps, no per-tick decrement)
- `parAt` = gametime of the last accepted press; `parLk` = gametime until which presses are ignored; `parHit` = gametime of the last
  successful parry (one press parries any number of hits **in the same tick**, then it is consumed).
- New **input pre-pass** at the top of `rlk:tick`, after the 2-player guard and before `F:tick:16`:
  `execute as @a[tag=player] if items entity @s weapon.offhand *[minecraft:custom_data~{rlk_ui:{}}] run function rlk:player/def/f_in`
  - Shift (predicate `rlk:in_sneak` or `sneakT ≥ 1`) and not in combat → `lvup/toggle` (as `hotbar/tick:5,7`).
  - Else, if no `vMap`, `pkMode`, `dead`, `buT` or `rnDie`, and `now ≥ parLk`: `parAt = now`; `parLk = now + #parGap`; guard fx;
    interrupt the swing (decision).
  - Clear the offhand. `hotbar/tick:5-10` become dead lines and go.
- Tier by `p = now − parAt` at the hit: tier 3 `0..#parW3−1`, tier 2 `..#parW2−1`, tier 1 `..#parW1−1`.
  - Defaults: `#parW3 3` (9 frames), `#parW2 6`, `#parW1 9`, `#parGap 10`. A success sets `parLk = now + 2` so combos can be chained.
  - Constants go in `F:load`'s 조절 지점 (R:655).

### 7.2 Dodge state
- `dash_go` stops writing `dashInvT`. It writes `dgAt = now` (with §3.4 (A) or (B) so a click before tick N gives `dgAt = N`, uniform
  across all input paths), stores the origin `dgX/dgZ` (body milliblocks, for the near miss), and `dgRw 0` (reward not yet paid).
- At a hit, `d = now − dgAt`:
  - **perfect** if `d < #dgPW` (3) and not ND;
  - **loose** if `d < #dgLW` (6 = today's window) and not ND and attacker class ≤ `#dgLooseC` (default: normal and elite);
  - **bosses**: only perfect avoids.
- Perfect → `#dodged 1`, red fx, `energy +1000` once per dodge (`dgRw`), `#mbDodgeOk 1`, hook `items/hook/on_pdodge`, hwamu.
  Loose → `#dodged 1`, the old crit particle.
- Generic `invT` (§2.5) is checked first and gives `#dodged 1` with no rewards.

### 7.3 Choke
New `F:player/def/judge`, called from
- `F:player/take_damage` (replaces `:3-6`);
- `F:mboss/hz/hurt_pm:12` (generator `T:build_mboss_core.py:3359`; context boss / area / unparriable).

Not called from `player/hurt_elem` (DoT: generic `invT` only) or from `pl_dot2` / fatal / curse.

Order inside take_damage:
1. `#dodged 0`, `#parT 0`.
2. `invT` → return.
3. judge: dodge, then parry. Tier 3 → `#dodged 1` (no damage), `#parT 3`, `char/cd_cut`, `function rlk:bal/parry` (`#balSrc`),
   gold fx → return.
4. Level and defence (`:8-15`).
5. Element (`:17-22`).
6. **Tier 2 / 1: `#dmgIn ×20/100` or `×50/100`, clamp ≥ 1**. Placed after the element step so transformative reaction damage added by
   `element/player_hit` is reduced too.
7. Items taken, berserk, shields, HP (`:24-34`).
8. Counters: lion (`:37`, landed hits only), hwamu.

Outputs:
- `#dodged tmp` (1 = no damage, unchanged meaning for every current reader)
- `#parT tmp` 0–3 (new)
- `#pdg tmp` 1 = perfect dodge

`cm/hit_pl2:5-7` skips knockback and `hurt_fx` when `#parT ≥ 1` and plays the tier fx instead. Knockback on tier 1–2 is a decision;
default none.

### 7.4 Per-hit context the entry points must set (one-shot `tmp` scores, read and reset by the judge, like `#mbNoRx`)
| score | meaning | set by |
|---|---|---|
| `#hcK` | 1 strike, 2 projectile, 3 area, 4 DoT / true (never judged), 0 vanilla | `cm/hit_me` → 1; `cm/hit_pj` → 2 (`cb_boom` → 3); `cm/pj/ic_boom` 2 / 3 by `#pj`; generated cm sites via `ch2mob/ch3mob` (`shu_hit`, `fe_hit` → 2); `mboss/hurt` from `#mbSrcIn` (2 → 2; 1 → 1 for sector / line / disc, 3 for full / mask / ring); `hz/hurt_pm` → 3; 나루카미 by `rdHK` (5 / 6 / 7 travelling → 2, 3 / 4 rect → 1, else 3) |
| `#hcC` | 0 normal, 1 elite, 2 boss | `cm/hit_pl`: brain or owner tags `rlk_c2e` / `rlk_c3e` → 1; `rlk_rd_hazard` → 2; `mboss/hurt` → 2 (mid-boss: decide; `#mbKind 0`); vanilla `on attacker` tags `boss` / `miniboss` |
| `#hcNP` | unparriable | new hazard / prop options `#hzNoParry` / `#pjNoParry` → `mbHzNP` / `mbPjNP` (`T:mboss_lib.py:394-430,472-487` `hz_opts(noparry=)`, `pj_opts(noparry=)`; init in `hz/init`, `pj/launch`). **Default 1** for `mbHzND 1`, `mbHzPm ≥ 1`, `mbHzRA ≥ 1`, `mbHzK 5/6` (full, mask), and kind 2 rings (jumpable waves); default 0 for one-shot disc / sector / line and props. 나루카미: `rlk_rd_nododge` and kinds 9 / 10 → 1. cm: `cb_boom` and the `ic_boom` floor burst → 1 |
| `#hcND` | undodgeable | `#mbNoDodge` (already one-shot from `mbHzND` / `mbPjND`), `rlk_rd_nododge`. Replaces the zero-and-restore of `dashInvT` in `hurt_nd`, `land_nd` and `pl_dot2` |
| `#balSrc` | attacker for balance | cm brain `cmId` (projectile → owner `cmId`), `-1` boss body, `-2` 나루카미 (per `cb/research_mobs.md` §4.4) |

### 7.5 What each `#dodged` / new-state reader should test
`cm/hit_pl2:5` and `boss/raiden/hazard/land:10` → skip on `#dodged 1` **or** `#parT ≥ 1`. `boss/raiden/hurt:23` → `#dodged`.
`cm/sh/rcontact:4` → tag (consume) also when `#parT ≥ 1`. `mboss/hz/hurt:20`, `pj/hit:16` → decision (§5.2).
`mboss/hurt_ev:4`, `hurt_dodge` → dodge events, and `#mbDodgeOk` = perfect dodge or tier 3. `mboss/hurt_bol:21` → no bond on tier 3.
`boss/apep/org/pj_end:5` → end the bolt on `#parT ≥ 1`. `mboss/fieldgen/p/rock/pj_end:3` → decide.
`items/proc/hw_ctr_q:5-6` → the new triggers.

### 7.6 Near-miss for the perfect dodge (needed for the "+10 energy" and pips to fire reliably)
- The body moves 1 block per tick before the hit tests. 홍련 already pads its pip test by +3 blocks (`T:mboss_scarlet/api.py:200`).
- **Hazards**: while any perfect window is open (`#dgOpen`), make `hz/hit` test with an extra pad (+3000 milliblocks in the radial,
  sector and line checks; one global gate in `hz/all`, generator `T:build_mboss_core.py:1106,1924`). Any contact inside that window is
  resolved as a perfect dodge, so the pad can only **reward, never damage**. Skip ND hazards (they would damage).
- **cm melee**: the range tests are literal selectors (e.g. `F:cm/sw/strike:8` `distance=..3.0`). Either add a second line per site
  (`if #dgOpen unless …..R if …..R+3 → player/def/near`) in the hand file and in the ch2 / ch3 generators, or accept that out-of-range
  dodges give no reward.
- **Projectiles** pass by anyway (no pad needed).

### 7.7 Cost per tick
- Today: `hotbar/tick:5,7,9` = 3 `execute if items` per tick, plus the dash lines in `player/tick:57-63`.
- New: the pre-pass is 1 line per tick (−2 net); dodge and parry state cost 0 per tick (gametime stamps); `invT` decrement 1 (same as
  today). Optional `#gt` store (1) if several places need gametime; the near-miss gate in `hz/all` is 1 per tick only during a boss
  fight.
- Per hit: about 15–25 commands (gametime, two subtractions, flag tests). Per press: about 8. Fx per event: 6–15 (+ cards aged by their
  world tick).
- Budgets: `test_m0diff` +6.5 per tick over `22ba247` (already exceeded by proto / 나비 / 역장, R:511-512), so **add nothing to the
  per-hazard tick path** outside the gated near-miss. Fight average ≤ 아펩 ~830 (R:200).

### 7.8 Build order and tests
1. **D0 contract**: names (`parAt`, `parLk`, `dgAt`, `dgRw`, `invT` or the kept name, `#hcK/C/NP/ND`, `#parT`, `#pdg`, constants), the
   `bal/parry` interface with the mobs side, user decisions (bow aim, elite / mid-boss class for dodge, knockback on tier 1–2, volley
   group, 스커크 energy, hwamu "being hit", rule text).
2. **S1 input + i-frame split, behaviour kept**:
   - the pre-pass (F), the early right-click poll (§3.4 A), `invT` split (writers §2.5), `dgAt` stamp with a 6-tick loose window for
     every class;
   - prove "same as today" (except the right-click now protecting one tick earlier);
   - update the harness models (`hrsim.dash`, `azsim.iframe_end`, `test_fw_az`, `test_cm_ar`, `test_hwamu`, `pat_p2`) to set the new
     stamps.
3. **S2 choke + context**: `player/def/judge`; context lines in `cm/hit_pl` / `hit_me` / `hit_pj` / `pj/ic_boom` (hand) and the
   ch2 / ch3 generators; `mboss/hurt`, `hurt_bol`, `hurt_nd`, `hz/hurt_pm`, `hz/init`, `pj/launch`, `T:mboss_lib.py` options
   (`build_mboss_core.py`); 나루카미 `hurt` / `land` / `land_nd` (`raiden_enc/core.py`, `build_raiden_hazards.py`); vanilla paths.
   Tiers, `char/cd_cut`, energy, `bal/parry` stub, `#mbDodgeOk`.
4. **S3 fx**: particles and sounds first (no RP). Optional `fx/pd` card generator + RP + `rplint` + atlas.
5. **S4 consumers**: hwamu, 야타용왕 brand (`mboss_azhdaha/brand.py`), 홍련 pips (`mboss_scarlet/shield.py`, `api.py` `PIP_*`), apep
   bolt, cm shield rush, item hooks `on_pdodge` / `on_parry`, tutorial s1 + a parry step, the 8 weapon lores, `items.md`,
   `engravings.md`, R:§2 / §3 (and R:716).
6. **S5 near-miss + balance**: `hz/hit` pad, cm near lines; re-run 홍련 T6 / T7 (`S:hr/review/bal` README), 아를레키노 dodge probe
   `S:ar/review/bal/knfair5.py` with a parry / dodge policy in `azfair_core.py`.

**Tests** (README 0-8, `S:README.md`). Run from a copy outside the datapack (`S:README.md` §1 B). Note: `<S>` there
(`S:README.md:13`) **is this session's scratchpad path**, so do not use option A here.
- New suite `S:pd/tests/` on a copy of `S:hr/tests/lib` (most complete harness: real `take_damage`, `time query gametime`, `in_sneak`
  predicate, command counts):
  - (1) tier by offset 0..10 for cm strike, cm projectile, boss hazard, boss prop, ‰ hazard, 나루카미, vanilla;
  - (2) ND / NP defaults per shape and option;
  - (3) loose window vs normal / elite, perfect only vs boss;
  - (4) `invT` still blocks, DoT never judged;
  - (5) `cd_cut` for all 8 characters including 나비아 / 네페르 charges and 스커크 mode;
  - (6) energy +1000 once per dodge with clamp;
  - (7) same-tick press latency (F pressed before `cm/world` hits; right-click before boss hits);
  - (8) lockout and key repeat;
  - (9) per-tick command delta;
  - (10) `#dodged` / `#parT` readers (§7.5).
- Regressions: `S:az/tests_cm/run_all.sh` (`test_fw_az`, `test_fw_ap`, `test_m0diff` budget, `gen_check`), `S:ar/tests/run_all.sh` +
  `test_arlecchino` / `pat_p1` / `pat_p2`, `S:hr/tests/*` (`test_scarlet` pips, `pat_ghost`, `test_hwamu`, `ident_hr` allow-list),
  checkers `check_refs` / `check_macro` / `check_nbtpath` / `mb/lint_mc` (compare with the release tree).
- Gates: `tools/dev/regen_all.sh` twice (+ `--mobs`, because cm generators change), `check_mboss_pack`, `loadcheck`
  (`0 function load failure(s)`), `rplint` and atlas if the RP changes.

---

## 8. Facts to carry into D0
- R:716 is out of date: F (no Shift) = dash; with the bow, aim toggle.
- `dashInvT` = dash, burst, motion-burst, revive and fall i-frames; undodgeable hits zero it, which also strips burst invulnerability
  (`mboss/hurt_nd`, `raiden/land_nd`).
- The right-click is late by one tick on the eye shields only (§2.3).
- 나비아 / 네페르 ignore `engravings/cd_cut` today.
- `mbHzW` (tell) is short on most quiet boss hazards, so parriability must be an explicit option, not derived from the tell.
- Generated vs hand: `mboss/**` = `T:build_mboss_core.py`; 나루카미 = `T:build_raiden_hazards.py` / `T:raiden_enc/core.py`;
  `boss/scarlet/shield/*` = `T:mboss_scarlet/shield.py`; `boss/azhdaha/brand/*` = `T:mboss_azhdaha/brand.py`; ch2 / ch3 `cm/*` =
  `T:ch2mob` / `T:ch3mob`; `char/motion/**` (most) = `T:build_player_rig.mjs`; `fx/nv/**` = `T:build_navia_fx_cards.py`.
  Hand: `player/**`, `combat/**`, `view/**`, `element/**`, `items/**`, `engravings/**`, ch1 `cm/*` and the shared `cm/hit_*`,
  `char/*` (not motion), `char/motion/events/**`, `lobby/**`, `snd/**`.
