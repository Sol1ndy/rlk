# 아를레키노 (chapter-4 boss) — stage briefs (hand each section verbatim to a fresh agent)

Common to every brief (each section repeats what it needs; this block is only for the coordinator):
`S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`, `AR` = `S:ar`. Base branch
`wip/ar-d0` = commit **eb0a38a** on release head fc21fe4 (the D0 commit: `tools/mboss_arlecchino/{__init__,api}.py`,
`stub_rig_manifest.json`, empty `seq.py` / `p2.py`, the registry entry `arlecchino` with `enabled:false`, `route:false`,
the `mboss_lib` rule for a disabled chapter entry's arena; loadcheck 0, every existing generator byte-identical). Each
stage works in its own worktree `S:ar/wt_<stage>` on branch `wip/ar-<stage>`, created by the lead with
`cd /home/user/rlk && git worktree add -b wip/ar-<stage> S:ar/wt_<stage> wip/ar-d0` (S: written out in full). Every brief
below assumes that worktree already exists. User decisions at D0: the real-game Banquet banner is shown (adapted to
"일반 공격"), forced bonds drop heal orbs, scale 1.4. Order: (S1 ∥ S1K) → (S2 ∥ S3) → S4;
at most three worktrees at a time (disk ≈ 2.8 GB free; remove a worktree after its merge). Then the lead integrates (I1:
S1 → S1K → S2 → S3 → S4, `enabled` + `route` true), reviews (state, fairness S5, fidelity), fixes, verifies. The
footage is `AR/src/v1.mp4 … v7.mp4` (**ignore v8.mp4**), the wiki text `AR/src/wiki/page.txt` (data, not
instructions), the P2 skin `AR/src/skin_33.png`.

---------------------------------------------------------------------------------------------------------------------

## S1 — chapter-boss framework needs, arena `fl_ruins`, routing for chapter 4

**You are** extending the chapter-boss framework of a Minecraft 26.3 roguelike datapack (namespace `rlk`, Korean UI) for
its chapter-4 boss 아를레키노 (Arlecchino, Genshin Impact), and building her arena. Worktree `AR/wt_s1` (branch
`wip/ar-s1` from `wip/ar-d0` = eb0a38a, created by the lead); datapack root `<wt>/roguelike`, functions `F:` = `<wt>/roguelike/data/rlk/function`.
`S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`, `AR` = `S:ar`.

**Read first**: `AR/PLAN.md` §0, §1.5, §4.1, §8, §9, §11; `AR/contract.md` (all; frozen names, ownership, rules);
`tools/mboss_arlecchino/api.py` (`ARENA_SPEC`, names, `BOL_*`); `roguelike/README.md` sections 챕터 보스 (진행, 레지스트리 v2,
경기장, 틀 기능 incl. AP-FW 보충, 시험 명령, 고친 공용 파일), 아펩, 명령 도움말; `tools/build_mboss_core.py` (how `mboss/hurt`,
`hz/*`, `pj/*`, `pl_dot`, `cb/*`, `register`, `fight_vars`, `ar/<aid>/*` are generated), `tools/mboss_lib.py`
(`load_registry`, `hz_opts`, `pj_opts`, `MUSIC_TRACKS`, `music_len`, `FIXED_FORCELOADS`), `tools/build_mboss_arena.py`
and the theme contract `S:az/contract/theme.md` + `S:ap/ap_contract.md` §0.6, the closest themes
`tools/mboss_arena_ap_oasis.py` and `tools/mboss_arena_tk_lift.py`, the Raiden block-dome sky (`tools/build_raiden_arena.py`,
`build_raiden_backdrop.py`), `tools/build_cboss_rooms.py` (`entrance_layout()`), `S:ap/framework_needs.md` (how AP-FW
added framework options), the footage arena sheet `AR/ref/arena.jpg` and `AR/ref/ov_v5.jpg`.

**Goal**
1. **FN-1 Bond-of-Life hazards** (contract §3.1): option `bol=N` (1..100) in `mboss_lib.hz_opts` / `pj_opts` (and the ‰
   hazard path `#hzPm`), carried per hazard / projectile exactly like `#hzNoRx`; in `mboss/hurt` (and the ‰ path) the raw
   damage of such a hit × `#mbBolRe mb` / 100 (a module-owned score; `init` / `cleanup_fight` set 100); after a hit that
   reached the player (not dodged, not refused by `#mbCine`) set `#mbHitBol mb N` (the module reads and clears it). Options
   removed with `scoreboard players reset` (mid-boss fights carry no new names). Mid-boss behaviour identical
   (`S:az/tests_cm` `test_m0diff.py`), ≤ +1 command per hit, `ident.py` diffs only where you intend.
2. **FN-3**: a chapter entry with `px:false` + `shield:true` runs the whole chapter path (route, gate, start, `cb/inc`,
   floors, repool, bars, won / cancel / lose, test aliases). Prove it with the D0 `arlecchino` entry forced on in a local
   uncommitted registry copy (or a throw-away test entry) in your harness; fix the core where it assumes proxies.
3. Registry: add `arenas.fl_ruins` exactly = `api.ARENA_SPEC` (n 4); measure the `minecraft:music.nether.crimson_forest`
   pool from the 26.3 asset index (jar / assets under `S:mcjar`, as AP-FW did) into `MUSIC_TRACKS` and set music 1 `len`
   = `music_len`. Keep `arlecchino` `enabled:false`, `route:false` (the lead flips both at I1).
4. Arena theme `tools/mboss_arena_fl_ruins.py` (PLAN §8): look `day` (default) and `crimson`; the plaza floor (flat full
   blocks inside walk 26, carved concentric rings and spokes), balustrade ring + invisible barrier, Fontaine ruins / trees /
   cliffs to r 40, the block sky dome r 44 lit from inside (no world-time dependence), light layer y 206 (floor ≈ 12, no
   spawns), nothing above the walk disc below y 226 except the light layer; `look_lines('crimson')` (dome / backdrop /
   moon disc ≈ 16 k blocks, `fill … replace` boxes ≤ 32 768, ≤ 4 slices) and back; `SENTINEL`, `CHECK`, `POINTS` (rim
   posts of the three wisps at bearings 0 / 150 / 210, r 28); `entrance_layout()` = the gravestone of PLAN §8.4 for the
   kind-9 zone (`tools/build_cboss_rooms.py` picks it up). Slices within the framework limits (≤ 40 slices, fill ≤ 32 768,
   ≤ 8 000 commands per slice).
5. `check_mboss_pack.py`: the new arena, FN-1 names. README: rows in "챕터 보스" (FN-1, px:false chapters, routing note
   "4챕터 → 아를레키노 (I1부터)", arena `fl_ruins`), the help table if a list changes.

**Do not touch**: `tools/mboss_arlecchino/**`, `F:boss/arlecchino/**`, kit / rig files, Raiden, other bosses' modules,
the player avatar files (`tools/build_player_rig.mjs`, `tools/player_motion/**`, `F:char/**`, `F:player/**`).

**Tests** (`AR/tests/`, harness style of `S:ap/tests` / `S:tk/tests`: vendor `S:az/tests_cm/lib` sims unchanged with
md5s in a README, add `lib/knsim.py`): `test_cm_ar.py` — routing table ch1–ch6 with a local `route:true` (ch4 →
arlecchino, ch2 and 5+ Raiden, 1 Azhdaha, 3 Apep), gate / start / won / cancel / lose / pause / reload with `px:false`,
FN-1 (× only on `bol` hazards, event once per landed hit, dodged / cine = no event, reset after the fight), music pool
length; `test_arena_fl.py` — walk disc flat full blocks, barrier closed, nothing overhead below y 226, both looks
reachable and reversible, slices within limits, light ≥ 12 everywhere spawnable, box inside the spec, entrance build.
Run the existing suites `S:az/tests_cm/run_all.sh`, `S:ap/tests/run_all.sh`, `S:tk/tests/run_all.sh` against your tree:
only your intended diffs (update pinned shared-edit baselines only with the lead's OK, documented).

**Renders**: `AR/renders/s1_arena_day.jpg`, `s1_arena_crimson.jpg` (top-down + perspective from the start point),
`s1_entrance.jpg`, next to `AR/ref/arena.jpg` (≤ 640 px wide).

**Gates** (helper: `bash AR/tools/regen_d0.sh <wt>/roguelike` reruns every registry-reading Python generator in the
documented order; then `git status` shows exactly your files): `bash S:mcsrv/loadcheck.sh <wt>/roguelike ar_s1` → 0; every generator you own twice → identical; all other
generators (core, arena, cboss rooms, proto, cproto, spproto, guardian, butterfly, fieldgen, azhdaha, apep, tachy, kits
`--skip-rp`, ch2, ch3) produce identical output except your intended files; `python3 tools/check_mboss_pack.py` green;
your suites green; standing rules (contract §4). Commit on `wip/ar-s1` ending with
`<세션이 정해 준 trailer>`;
no push.

**Report**: commits, files owned, FN-1 lines as generated (hurt, hz, pj, pm paths), per-hit command delta, test counts,
loadcheck result, arena block counts per slice and look-job size, render paths, function count, requests
(`AR/requests/s1.md`).

---------------------------------------------------------------------------------------------------------------------

## S1K — Arlecchino FX / sound / HUD kit

**You are** building the effects kit of the chapter-4 boss 아를레키노 (Arlecchino, Genshin Impact) in a Minecraft 26.3
datapack + resource pack. Worktree `AR/wt_s1k` (branch `wip/ar-s1k` from `wip/ar-d0` = eb0a38a, created by the lead).
`S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`, `AR` = `S:ar`.

**Read first**: `AR/PLAN.md` §1.3, §1.5, §3, §4.6, §5, §6, §11.2, §11.6; `AR/contract.md` §2–4; `tools/mboss_arlecchino/
api.py` §8 (`KIT_PRESETS`, `KIT_PROPS`, `KIT_DECALS`, `KIT_SOUNDS`, `KIT_HUD`, `KIT_FIXED`, `LINES`); the footage sheets
`AR/ref/*.jpg` (every pattern sheet: colours, shapes; `captions_guide.jpg` and `hud_bars_banner.jpg` for the HUD); the
closest kits `tools/build_mboss_tk_fx.py` + `mboss_tk_fx_paint.py` (Tachy) and `tools/build_mboss_ap_fx.py` (+ `S:ap/ap_fx_api.md`;
decal drawing `tele/disc_o`, `crack_o`), the butterfly kit's screen flash / badge glyphs (`tools/build_mboss_bf_fx.py`),
Raiden's dialog subtitles (`tools/build_raiden_encounter.py` `LINES`, letter reveal).

**Goal**
1. `tools/build_mboss_kn_fx.py` (+ `tools/mboss_kn_fx_paint.py`, writes `tools/mboss_kn_fx_manifest.json`): copy-adapt the
   Tachy / Apep kit engine (card engine, counted pools, self-rescheduling ager, no shared-file hooks). Implement **every**
   name in `api.KIT_PRESETS` / `KIT_PROPS` / `KIT_DECALS` / `KIT_SOUNDS` / `KIT_HUD` / `KIT_FIXED` with the exact macro
   args (tenths / degrees / ticks; `c` 1 Pyro orange-gold `#FF8A2A`→`#FFD27A`, `c` 2 crimson BoL `#7A0A1A`→`#FF3A4A` with
   black smoke — the footage's two colours). Decals only the seven of contract §3.3, at floor y + 0.02, each flashing
   6 t before its `t`. Props: the flaming scythe wheel (4-frame spin), crescents, crimson feather, orb, giant crimson
   blade, crimson clone silhouette, wisps (white / red, bobbing), red-moon halo. HUD: font `rlk:mboss_kn` (badge
   `◆선혈의 충격`, banner line, dialog subtitles `hud/line {id}` with Raiden-style letter reveal for every `api.LINES` id;
   glyph root always an empty unstyled text), `hud/clear`. Sounds: one recipe per name (vanilla events only, the
   `mboss_lib.sound` min-volume rule; recipes from PLAN §3, §5, §6). Gate icon model `rlk:mboss/kn_kit/gate_icon` (crimson
   scythe over a red moon). In-game demos `fx/test/<name>` on a vanilla stand-in for each preset / prop / decal.
2. Sprites ≤ **0.70 M px** total (plan ≈ 0.62 M, PLAN §11.6), lowercase ids, no glyph-font inheritance.

**Do not touch**: registry, core, `mboss_lib`, `tools/mboss_arlecchino/**`, other stages' files, other kits.

**Tests** (`AR/tests/test_kit.py`): every contract name exists with the right macro-ness and args, ager / pool caps,
decal flash timing and floor height, pause clear, uninstall removes objectives and cards, sounds only vanilla ids
(`S:rd/tests/sound_ids.txt`), glyph root rule, the banner / line texts equal `api.LINES` / PLAN §4.6.

**Renders**: `AR/renders/s1k_sprites.jpg` (sprite sheet), `s1k_presets.jpg` (one strip per preset / prop / decal) next
to the matching `AR/ref/` frames.

**Gates** (helper: `bash AR/tools/regen_d0.sh <wt>/roguelike` reruns every registry-reading Python generator in the
documented order; then `git status` shows exactly your files): RP plain copy `cp -r S:tk/rp AR/rp_s1k` (current release RP; never hard links); `python3 -I S:mcsrv/rplint.py
AR/rp_s1k` clean; `bash S:mcsrv/loadcheck.sh <wt>/roguelike ar_s1k` → 0; your generator twice → identical (DP and RP);
other generators' outputs unchanged; atlas ≤ 0.70 M px for `kn_kit`; standing rules (contract §4). Commit on
`wip/ar-s1k` with the trailer `<세션이 정해 준 trailer>`; no push.

**Report**: commits, preset / prop / decal / sound / HUD counts, sprite px, function count, render paths, requests
(`AR/requests/s1k.md`).

---------------------------------------------------------------------------------------------------------------------

## S2 — Arlecchino rig, battle-entry motion, transition and death sequences

**You are** building the display-entity rig (model + clips) of the chapter-4 boss 아를레키노 (Arlecchino, Genshin
Impact) and her sequences (battle-entry intro, phase-2 transition, death) in a Minecraft 26.3 datapack + resource pack.
The user wants the **existing Arlecchino player skin used as-is** for phase 1 and a detailed battle-entry motion.
Worktree `AR/wt_s2` (branch `wip/ar-s2` from `wip/ar-d0` = eb0a38a, created by the lead).
`S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`, `AR` = `S:ar`.

**Read first**: `AR/PLAN.md` §1.4, §2 (all), §3 (all), §5–6 (motions per pattern), §11.2; `AR/contract.md` §1–3.2;
`tools/mboss_arlecchino/api.py` §7 (`PARTS`, `LOOKS`, `RIG_CALLS`, `CLIPS`, `ANCHORS`, `SIZE`, `check_manifest`), §9
(`Service`, `Writer`, `OWN['S2seq']`) and `tools/mboss_arlecchino/stub_rig_manifest.json`; the player avatar rig
`tools/build_player_rig.mjs` (read-only: `transform()`, `skinFaces`, `bodyModels`, the `arle` entry, the weapon frame) and
its clips `tools/player_motion/arle.json` (read-only pose sources), `tools/scythe_geometry.mjs` (the scythe's frame:
grip [8,8,8], shaft +Y, hook −X, edge = lower / inner outline); the Tachy rig as the structural template
(`tools/build_tachy_rig.mjs`, `tachy_*.mjs`, `tools/tachy_rig_api.md`) on the shared RIGLIB (`mboss_rig_compile.mjs`,
`mboss_rig_clips.mjs`, `mboss_model_lib.mjs`, `mboss_shape_lib.mjs`, `mboss_paint_lib.mjs`, `mboss_rig_math.mjs`, all
unchanged); the footage sheets `AR/ref/intro_*.jpg`, `model_*.jpg`, `skins_p1_p2.jpg`, `p1_*.jpg`, `p2_*.jpg` and the
videos `AR/src/v1.mp4 … v7.mp4` frame by frame where needed (tools `AR/tools/sheet2.py`, `picks.py`; keep extracted
frames ≤ 640 px jpg in `AR/s2/`, delete what you do not keep; **ignore v8.mp4**); the offline renderer
`S:az/understand/rigtech_render.py` (wrapper style `S:ap/rigwork/r1/r.sh`).

**Goal**
1. `tools/build_arlecchino_rig.mjs` (+ `arlecchino_{pose,geometry,paint,clips}.mjs`, `arlecchino_skin_p2.mjs`) writing
   `F:boss/arlecchino/rig/**` (owned, rebuilt from scratch), RP `assets/rlk/{textures,models/item,items}/mboss/arlecchino/**`
   + atlas entries, `tools/arlecchino_rig_manifest.json` (stub schema + transforms / budgets / sprites; `api.check_manifest`
   passes), `tools/arlecchino_rig_api.md`. Model per PLAN §2: the 10 body parts are item displays of the **avatar's
   existing item models** `rlk:player_motion/arle/<part>` (never copied or repainted) in form p1; form p2 uses
   `AR/src/skin_33.png` embedded as base64 in `arlecchino_skin_p2.mjs` → `textures/mboss/arlecchino/skin_p2.png` + 10 part
   models built with the avatar's `skinFaces` layout and overlay inflation (**skin_33 is a classic 4-px-arm skin, the
   avatar's is slim**: P2 arms 4 px wide with classic UVs, shoulder offset ±0.375 × SIZE in form p2, PLAN §2.1); scythes = `rlk:player_motion/weapons/
   scythe` (right; left mirrored in p2, edges leading); six crimson wing / blade-leg pairs (P1 `wings` look only for wing
   attacks, P2 always), cup + saucer props for the intro; kinematics = the avatar's `transform()` copied and scaled by
   `api.SIZE` 1.4. UUIDs `524c4b4d-4b4e-4100-8000-0000000000NN`, tags `rlk_room rlk_mb_aux rlk_mb_part rlk_kn_part
   rlk_kn_<part>`, objectives `knRig*` only; every call of `api.RIG_CALLS` + `play/` / `start/` per clip +
   `face/set {yaw}` + `anchor/<name>`. Build gates: no part / prop / blade tip below the feet at any compiled tick, event
   keys present, ≤ 120° per tick, atlas **≤ 0.15 M px**, rest elements ≤ 6 500, models within −16..32.
2. Clips from the footage with the contract's exact lengths / events (PLAN §2.4). Big swings keyed **every tick** (twirl,
   spin rings, slams, wing sweeps); held weapons checked from the side (edge leading, hook the right way). The **intro**
   (150 t) beat by beat as PLAN §3.1 (tea sip, cup to embers + wisps fleeing, arm out, crimson vortex, the scythe growing
   from the palm, horizontal hold, the 10 t 360° frontal twirl, hold, flip, the stance with the crescent low by the right
   foot) matched against `AR/ref/intro_v1_summon.jpg`, `intro_v1_fine.jpg`, `intro_v1_twirl.jpg`, `intro_v1_stance.jpg`;
   `t_p2` (180 t, PLAN §3.2, form swap at 90 hidden by the pillar), `death` (110 t, PLAN §3.3), `e70`, `brk`, `stun`.
3. `tools/mboss_arlecchino/seq.py`: `SERVICES` = one `api.Service` per `api.SEQS` (`intro`, `t_p2`, `death`); each
   `build(W)` writes only `seq/<name>/{start,tick,cancel}` with `W = api.Writer('S2seq', api.OWN['S2seq'])`, clock
   `#sq kn`, end `#sqdone kn 1`, ticks from `api.ev`, effects / sounds / dialog only via `api.K` (`api.lines`), rig only
   via `api.rig` / `api.play`, the P2 look via `api.arena_look('crimson')` at `t_p2`'s blackout event, titles through
   `mboss_lib.title(...)` (intro at 80, P2 at 140), the intro push ring via `mboss_lib.push_ring` (no damage), the wisps
   via the kit props. Phase switches, invulnerability, `repool` and music are the core's (S3); sequences never set phases.

**Do not touch**: `api.py`, the stub manifest, other `tools/mboss_arlecchino/*.py`, registry, core, kit, arena, the
avatar files (`tools/build_player_rig.mjs`, `tools/player_motion/**`, `F:char/**`) — read-only.

**Tests** (`AR/tests/test_rig.py`): manifest vs contract, floor-dip and step checks over every clip tick (incl. scythe
tips, legs, cup / saucer), the avatar item ids referenced and not re-written, P2 arm UVs classic (4 px) and P1 slim, the
embedded P2 skin equals
`AR/src/skin_33.png` byte-for-byte after decoding, culling, UUID / tag set, `rig/kill` + `uninstall` leave nothing,
`look/*` idempotent, `seq.py` builds with a dummy Writer and only writes `seq/**`, every seq tick referenced exists.

**Renders**: `AR/renders/s2_U1.jpg` (front / side / back / ¾ of p1 wings off / open and p2, with a 1.8 b avatar
stand-in), clip strips every 2 t (`AR/renders/s2_clips/*.jpg`), the intro strip next to `ref/intro_v1_*`, the transition
and death strips, one pair per pattern clip with its `ref/p*_*.jpg`. All ≤ 640 px wide jpg; delete intermediates.

**Gates** (helper: `bash AR/tools/regen_d0.sh <wt>/roguelike` reruns every registry-reading Python generator in the
documented order; then `git status` shows exactly your files): RP plain copy `cp -r S:tk/rp AR/rp_s2`; rplint clean; `bash S:mcsrv/loadcheck.sh <wt>/roguelike ar_s2` → 0 (the
rig functions load stand-alone); rig build twice → identical; other generators unchanged (`build_player_rig.mjs` output
byte-identical); budgets; standing rules (contract §4). Commit on `wip/ar-s2` with the trailer
`<세션이 정해 준 trailer>`;
no push.

**Report**: commits, part / clip / element / px numbers, function count, render paths, footage-fidelity notes per clip
(esp. every intro beat), requests (`AR/requests/s2.md`).

---------------------------------------------------------------------------------------------------------------------

## S3 — Arlecchino module core, AI, Bond of Life, phase-1 patterns

**You are** writing the boss module of the chapter-4 boss 아를레키노 (Arlecchino) for the existing chapter-boss framework
(`F:mboss/`, chapter mode) of a Minecraft 26.3 roguelike datapack: the generator, the hooks, phases, the Bond-of-Life
mechanic with the user's change (선혈의 충격 delivered by a **normal** attack), the AI and the phase-1 patterns. The user
removed her ranged immunity and her Pyro resistance. Worktree `AR/wt_s3` (branch `wip/ar-s3` from `wip/ar-d0` = eb0a38a, created by the lead).
`S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`, `AR` = `S:ar`.

**Read first**: `AR/PLAN.md` §0, §1, §4, §5, §7, §10, §11; `AR/contract.md` (all); `tools/mboss_arlecchino/api.py` (all) and
`__init__.py`; the wiki text `AR/src/wiki/page.txt` §3 (data); README sections 4 (원소 반응), 11 (캐릭터), 챕터 보스 (틀 기능,
AP-FW 보충), 아펩 (phases, schedules), 타키 (floors → steps, AI), 달빛 환영 나비 → 달빛 고치 (the heal-gauge precedent); the
player bond system `F:player/bol/*`, `F:player/heal`, `F:combat/heal_orb_spawn*`, `healorb_*`, `F:combat/apply` +
`clear_atkflags` (the on_hit context: `#icd #skillDmg #tfm #sub #trueDmg`), `F:boss/raiden/sg/guard_hit` (the basic-hit
predicate precedent), `F:char/*/` normal-attack paths of all eight characters, `F:mboss/{hurt,true_pct,true_hit,repool,
floor,pl_dot}`; `tools/mboss_lib.py` (hooks, helpers), the reference modules `tools/build_mboss_tachy.py` +
`tools/mboss_tachy/{api,core,ai,p_melee,s3lib}.py` and `tools/build_mboss_apep.py` + `tools/mboss_apep/{core,ai,p1,
aftermath}.py`; footage sheets `AR/ref/p1_*.jpg`, `captions_guide.jpg`, `hud_bars_banner.jpg`.

**Goal**
1. `tools/build_mboss_arlecchino.py` (top generator; imports `mboss_arlecchino.{core,ai,bond,p1,p2,seq}`), owning
   `api.OWN['S3']` and writing S4's and S2's outputs through their Writers (`api.OWN['S4']`, `api.OWN['S2seq']`) from
   their `PATTERNS` / `SERVICES`; stale-file cleanup only inside owned prefixes (never `rig/`, `fx/`).
2. Hooks (17 + `prep` + `test/help`), `init` / `uninstall` (objective `kn`, `api.CORE_FP`), the phase machine intro →
   P1a → (70 % floor) E70 → P1b → (floor 1) T → `repool 36` → P2 (Q0 first) → death (PLAN §7.1), `#mbFloor`, music
   phases, titles (P1 「아를레키노」 / 우인단 집행관 서열 4위 at the intro's title event; P2 at T 140), bars (pattern name +
   badge), pause / resume / reload / cleanup per phase (reload in intro → end of intro; in a pattern → cancel + recover; in
   T → finish T; in a stun → keep the remaining stun), `prep` (gate lines, the gravestone flame chain), kit wiring
   (contract §3.3), the dialog lines (`api.LINES`) at each cast.
3. `bond.py` (PLAN §4, contract §3.5): BoL hits via `#mbHitBol` (bond + heal her), `#mbBolRe` every tick, the DoT, forced
   bond + heal orbs (`bond/force`, `bond/orbs`, ≤ 3 `rlk_kn_orb`), clear detection by polling `bol` → 선혈의 충격, the
   normal-attack predicate in `on_hit` (only sets `#shk_hit`), the resolve in `tick` (break windows from
   `api.BREAK_WINDOWS` → cancel + clamped true damage + `brk` → `stun` 140 t; else the 2 % burst), cleanup removing only
   `min(bol, #given)`. **No ranged immunity and no Pyro resistance anywhere**.
4. `ai.py`: bands, rear / far dwell rules, `api.WEIGHTS` / `COOLDOWN` / `SCHEDULE` (F and Q5 schedules, P2 Q3 rear rule),
   no repeat, recovery walk / strafe, the phase step at the next decision after a floor; only patterns present in the
   PATTERNS lists (S4's may still be empty: skip them).
5. `p1.py`: A (a2 / a4 / a5), B (b1 / b2), C (c1 / c2), D (d1 / d2), E (e1), F (f1 incl. its decals and window), G (g1), H (h1)
   and the E70 event as `api.Pattern`s per PLAN §5 and `api.HITS` (ticks from `api.ev`, shapes, tiers, BoL flags through
   FN-1 `bol=`, decals only `api.KIT_DECALS`, `#hzQuiet 1` otherwise, end points via `mv/ok` inside `api.MOVE_R`).
6. While `tools/arlecchino_rig_manifest.json` is absent: `rig_stub/**` (every `api.rig` call; `play/<clip>` sets `#rigc kn`)
   — never when the real manifest exists. While S2's `seq.SERVICES` is empty: stand-in sequences (wait the clip length,
   titles at their events). While S1's FN-1 is absent on your branch: write the `bol=` option through `mboss_lib` only if
   it exists, else fall back to setting `#mbHitBol` yourself from `#mbHitEv` + a pattern flag (documented, removed at I1).
   Never reference a function another stage has not produced (`api.K`, `api.rig`, `api.arena_look` handle it).
7. README section "아를레키노 (`boss/arlecchino/`)" (player summary, phases, patterns, the bond / shock rules and the
   user's three changes, test ids, files / build order) as `AR/s3/readme_arlecchino.md` (the lead merges it at I1).

**Do not touch**: `api.py`, stub manifest, `seq.py`, `p2.py`, registry, core, kit, rig, arena, the avatar / player files.
The registry entry stays `enabled:false`, `route:false`: test through the harness (call hooks directly) and, for an
in-game check, a local uncommitted `enabled:true` + core regeneration.

**Tests** (`AR/tests/`: `test_arlecchino.py`, `pat_p1.py`, harness `lib/knsim.py` shared with S1/S4 — if S1's is not on
your branch yet, write yours in `AR/s3/lib/` and the lead merges): PLAN §11.3 (hooks, phase order, floors, E70 once, BoL
rules incl. ×2.5 only while bonded and only on BoL hits, DoT only after her bond and non-lethal, forced-bond skip states,
clear → shock, the normal-attack predicate per character (table: which attack kinds count; exceptions listed), break
inside / outside windows (clamped, never skips T), stun, orbs, AI weights / cooldowns / schedules over seeded runs, pause /
reload per phase, cleanup leaves no `rlk_kn_*` and only her bond removed; every P1 hit tick == clip event, tells ≥ 12 / 20 t,
combo gaps ≥ 10 t, shapes / reach / tiers / BoL flags, decals only the allowed keys, end points inside walk − 1.5 and never
in blocks, cancel at every tick leaves nothing).

**Renders**: per P1 pattern a top-down hit-shape diagram over time (`AR/renders/s3_<key>.png`, ≤ 640 px).

**Gates** (helper: `bash AR/tools/regen_d0.sh <wt>/roguelike` reruns every registry-reading Python generator in the
documented order; then `git status` shows exactly your files): `bash S:mcsrv/loadcheck.sh <wt>/roguelike ar_s3` → 0; `build_mboss_arlecchino.py` twice → identical;
`check_mboss_pack.py` green; other generators unchanged; standing rules (contract §4: no negative add/remove literals, no
tutorial text, no glyph-font inheritance, vanilla sounds). Commit on `wip/ar-s3` with the trailer
`<세션이 정해 준 trailer>`;
no push.

**Report**: commits, function counts per subtree, per-tick command cost of a fight tick (vs Apep ≈ 830), test counts,
the per-character normal-attack table, requests (`AR/requests/s3.md`), anything S4 / S2 must know.

---------------------------------------------------------------------------------------------------------------------

## S4 — Arlecchino phase 2 (두 세계 불의 잔재 페르엘) patterns

**You are** writing the phase-2 patterns of the chapter-4 boss 아를레키노 (Arlecchino → 「두 세계 불의 잔재」 페르엘) for an
existing boss framework in a Minecraft 26.3 datapack. Worktree `AR/wt_s4` (branch `wip/ar-s4` from `wip/ar-d0` = eb0a38a, created by the lead; rebased
on S3's branch if the lead says so). `S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`, `AR` = `S:ar`.

**Read first**: `AR/PLAN.md` §1.2, §1.5, §4, §5.1, §6 (all), §7, §11.2; `AR/contract.md` §2–4; `tools/mboss_arlecchino/
api.py` (`HITS` `q0…q6`, `P2_MUL`, `dmg`, `DASH_LEN`, `BREAK_WINDOWS`, `BOND_CALLS`, `MOVE_R`, `Pattern`, `Writer`,
`OWN['S4']`, `K`, `rig`, `ev`) and the docstring of `p2.py`; README 중간보스 → 공용 라이브러리 (`pj/launch` blades / balls,
`pj/steer`, `grp_new`, `hz/*` incl. `ring`, `hz/full`, `pl_dot` / `#hzPm`, `mv/*` incl. `mv/ok`, `mv/leash`, `mv/lockv`,
`mboss_lib.pj_opts` / `hz_opts` incl. S1's `bol=`); reference pattern files `tools/mboss_tachy/p_air.py` (leaps, hovers,
projectiles) and `tools/mboss_apep/p3.py` (mortars, rings); footage sheets `AR/ref/p2_*.jpg` and the videos
`AR/src/v4.mp4` (13–40), `v6.mp4`, `v7.mp4` (**ignore v8.mp4**).

**Goal**
1. `tools/mboss_arlecchino/p2.py`: `PATTERNS` = `api.Pattern`s for `q0` (hover far → fall on the player when they move or
   after 80 t; once), `q1` (twin string, 3–6 hits incl. the returning crescents), `q2` (wheel throw exploding at the locked
   point, dash after it, slash), `q3` (rear whip-spin, then q1 h1–h3 near or two crescents far), `q4` (rise, 1–3 beams with
   the in-air aim line + reticle, 50 t apart), `q5a` / `q5b` (both: forced bond at `brand` via `api.BOND_CALLS['force']` + `['orbs']`; q5a 형벌의 핏값 rings with
   the `ring_o` / `donut_o` decals, q5b 붉은 피의 사형 with the vertical X, rapid slashes and the non-lethal 450 ‰
   `pm_disc` final; the AI picks 50 / 50 with no repeat; break windows `api.BREAK_WINDOWS`), `q6` (rise, six feather volleys, eight
   orbs to the rim, dive, impact + orb explosions) — PLAN §6 exactly: ticks only from `api.ev`, hits from `api.HITS` with
   `api.dmg(tier, phase=2)`, BoL through `bol=`, decals only `ring_o` / `donut_o`, `#hzQuiet 1` otherwise, effects /
   sounds / dialog via `api.K`, rig via `api.rig` / `api.play`, markers tagged `rlk_kn_p rlk_kn_p_<key>`, state in
   `#<key>_<x> kn`, idempotent `cancel` (the core's break uses it on q5), optional `pause` / `resume`.
2. Safety: every end point (hover, dive, dash, landing) through `mv/ok` + leash inside `api.MOVE_R`; never in blocks;
   heights ≤ 12 b over the floor (dome is higher); parts never below the floor; she stays hittable in the air (no ranged
   immunity); `rlk_mb_inv` never set by P2 patterns.

**Do not touch**: `api.py`, the stub manifest, `core/ai/bond/p1/seq.py`, `build_mboss_arlecchino.py` (S3's), registry,
core, kit, rig. **Commit only `p2.py`** (and tests outside the repo): the generated `F:boss/arlecchino/p/q*/**` are written
by S3's generator at integration. To load-check before that, use a throw-away runner `AR/s4/run_s4.py` (not committed)
that builds your PATTERNS with `api.Writer('S4', api.OWN['S4'])` into your worktree plus a minimal throw-away
`boss/arlecchino/rig_stub/**` and `bond/{force,orbs}` stubs, then `git clean` those outputs before committing.

**Tests** (`AR/tests/pat_p2.py`, harness `lib/knsim.py` or your own under `AR/s4/lib/`): every hit tick == clip event,
tells ≥ 12 t / big ≥ 20 t, ring / donut geometry (safe bands exist), the Q5B final non-lethal and dash-dodgeable, beam
lock vs aim, projectile speeds / returns / wall stop, Q6 orb rim positions inside walk and the safe band between, Q0 trigger
(move / timeout, once), end points over 500 seeded player positions incl. the rim (inside walk − 1.5, never in blocks),
cancel at every tick leaves nothing, pause / resume.

**Renders**: per pattern a top-down / side diagram of the hit shapes over time (`AR/renders/s4_<key>.png`, ≤ 640 px).

**Gates** (helper: `bash AR/tools/regen_d0.sh <wt>/roguelike` reruns every registry-reading Python generator in the
documented order; then `git status` shows exactly your files): `bash S:mcsrv/loadcheck.sh <wt>/roguelike ar_s4` → 0 with your outputs + the throw-away stubs built; your
outputs twice → identical; `check_mboss_pack.py` green; no other output changed; standing rules (contract §4). Commit on
`wip/ar-s4` with the trailer `<세션이 정해 준 trailer>`; no push.

**Report**: commits, function counts, test counts, end-point statistics, requests (`AR/requests/s4.md`), anything S3 must
wire (calls, scores it reads).
