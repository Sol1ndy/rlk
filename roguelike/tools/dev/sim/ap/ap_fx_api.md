# 아펩의 오아시스 파수꾼 FX / audio / HUD kit — API (`ap_fx_api.md`)

Status: **§0 = the day-0 call list** (stage AP-SPEC, 2026-10-19; plan `S:ap/plan.md` v1 §3.9 item 3, §8; the module
side is `S:ap/ap_contract.md` §0, whose §0.7 summarises this section). It names every telegraph, preset, prop, sound
recipe and HUD call that plan §8 uses, with its macro arguments and executor context. The pattern, organism and revival
authors (AP-P1, AP-P3, AP-REV) and the core's no-op `api.K` (AP-CORE) code against these names from day 0. AP-FX builds
them and then writes §1 onwards (engine, sprites, measured budgets, renders, verification), as `S:mb3/fg_fx_api.md`
§1-§13 do for the field generator. **Names and arguments in §0 are frozen**: AP-FX may add a name by request
(`S:ap/requests/fx.md`) but never renames one or changes its arguments; looks, card counts and sound layers are AP-FX's.

`S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`; `F:` = `data/rlk/function/`;
`AP:` = `F:mboss/apep/`. Model: the field generator kit (`T:build_mboss_fg_fx.py`, `S:mb3/fg_fx_api.md`, on M0 at
99bc097) with the Azhdaha kit's day-0 conventions (`S:az/contract/fx.md`, re-read 2026-10-19 02:07 UTC, unchanged since
2026-10-18 22:30 UTC): the same engine entry points, argument names and order, `el` / `nd`, stacked `tele/wedge` for
swept sweeps, wave ids, safe rims, the mask wash, no rig calls, no kit-owned boss-bar lines. §0.13 lists where Apep
deliberately differs.

## 0. Call list (day 0)

### 0.1 Ownership, prefixes, generator

| what | path | owner |
|---|---|---|
| generator, painters, manifest | `tools/build_mboss_ap_fx.py`, `tools/mboss_ap_fx_paint.py`, `tools/mboss_ap_fx_manifest.json` (`owned`, kinds, presets, props, sounds, glyphs, caps, objectives, tags, palettes) | AP-FX |
| card engine entry points | `AP:fx/{card,cardx,look,clear,uninstall}` | AP-FX |
| internals, telegraphs, dressing pool, presets, sounds, HUD, props, tests, demos | `AP:fx/{e,p,tele,dress,snd,hud,prop,test}/**` | AP-FX |
| any other name under `AP:fx/` | the module core's own files (left alone by the kit's cleaner; the module's `clean()` spares the kit's `owned`) | AP-CORE |
| sprites / models / item definitions | `assets/rlk/{textures,models/item,items}/mboss/ap_kit/<kind>` + atlas entries `rlk:mboss/ap_kit/*` appended to `assets/minecraft/atlases/items.json` by the generator's merge | AP-FX |
| HUD font | `assets/rlk/font/mboss_ap.json` (`rlk:mboss_ap`, **U+E900-E9FF**), `assets/rlk/textures/font/mboss_ap/*` | AP-FX |
| tests, renders | `S:ap/fxtests/**` (`test_ap_fx.py`, `run_kit.sh`), `S:ap/fxrender/**` | AP-FX |
| never written | `AP:rig/**`, every other `AP:**` path, every other kit | — |

Prefixes (all checked free on M0 99bc097; `#pk*`, `rlk_pk*`, `pkS` are the codex's, so the kit letter is `w` for
"Warden"): fake players **`#wk*`** (objective `mb`); objectives **`wkS wkG wkH wkK wkD`** (the fg kit's `fk*` roles);
entity tags `rlk_wk` (every card), `rlk_wk_t` (attack telegraphs), `rlk_wk_wv<k>` (wave rings), `rlk_wk_sr<k>` (safe
rims), `rlk_wk_mr<k>` (moving target rings), `rlk_wk_d<k>` (dressing pool), `rlk_wk_fl` (flood pool), `rlk_wk_demo`;
storage **`rlk:apkit`**; font `rlk:mboss_ap`; item models `rlk:mboss/ap_kit/*`. Every card also carries `rlk_room` +
`rlk_mb_aux` (every cleanup path removes it). No collision with the butterfly kit (`#bk`, U+E6xx), the field generator
kit (`#fk`, U+E7xx), the Azhdaha kit (`#ak`, U+E8xx) or the module core (`#ap*`, `rlk_mb_ap_*`, `rlk:mboss ap.*`).

Generic textures (telegraph rims / fills / rings / lane bars / sector masks and the neutral kinds `glow`, `glint`, `mote`,
`streak`, `ripple`) are **referenced from the fg kit** (`rlk:mboss/fg_kit/…`) in the Apep item models instead of being
painted again (plan §5.4: ≤ 0.35 M **new** px); the kit build fails when a referenced texture is missing.

The kit **never** decides gameplay, makes hazards or projectiles, counts hits, moves the body, calls the rig
(`AP:rig/**`) or reads a manifest (Azhdaha fx.md §0.3). Its demos (`fx/test/*`) use a vanilla stand-in anchor tagged
`rlk_wk_demo`.

### 0.2 Conventions (the fg kit's §1 unless changed here)

- **Executor context**: position = the event point (floor points at the `ap_oasis` floor top, **y 201**), rotation = the
  aim (yaw; pitch 0 unless stated): `execute positioned <point> rotated <yaw> 0 run function rlk:mboss/apep/fx/...`.
  Planes, billboards, the radial trick, stages and `off` exactly as the fg kit.
- **Units**: blocks, ticks, degrees (+ = clockwise seen from above, Minecraft yaw), RGB ints (`16777215` = untinted).
  **Macro args for telegraph, dressing and preset sizes are tenths of a block** like the framework hazards. The Python
  builders (`K.*`, §0.10) take **blocks** and write tenths (Azhdaha fx.md §9).
- **`el`** palettes (rim / fill / flash, starting values AP-FX tunes on both floors and over the water sheet):
  **7 Dendro** `#4E8A1E / #A6D45A / #F1FFD2` (the default: phase 3 and the organisms); **20 gold** `#B07A1E / #EBC55A /
  #FFF4C8` (phase-1 telegraphs on the withered field); **22 target** `#6FA85A / #C1E6A8 / #F5FFF0` (the Q3 following ring);
  **23 olive** `#FCF9ED / #B9B46A / #FFFFF4` (the P4 filling disc, rim `#FCF9ED` per plan); **24 field** `#9DBA2E / #DCEB72 /
  #FFFFD8` (the Q2 mask wash and flood). Any other value draws Dendro.
- **`nd`** (Azhdaha's undodgeable look): 0 normal; 1 the undodgeable rim (`#C36E5A`, the banner red); 2 = 1 + a jump
  chevron. Every §8 decal passes `nd:0`: Apep's undodgeables have no ground decal of their own (homing wheels = props;
  the 종말의 여파 mask = `mask_wash` + safe rims; the failure wither = none). The argument keeps the call shape of the
  Azhdaha kit.
- **Layering** above the floor top: lush water sheet +0.005 (arena prop), dressing pool and mask wash +0.03, attack fills
  +0.035, rims +0.045, wave rings +0.048 / +0.05 (≥ 0.025 b clear of the water sheet); cutout or emissive only.
- **Pairing rule** (plan §7.11 rule 1): every damaging decal is called in the same tick as its framework hazard with the
  same `tell` and size (`#hzQuiet 1`, `#hzSfx 0`); the fill's leading edge reaches the rim on call + tell (the strike
  tick), every card of the shape flashes then and stays `hold` ticks. No ground decal is larger than its hazard; bursts
  beyond it are airborne fx.
- Every macro accepts `with storage` arguments (ints for `el`, `nd`, sizes, ticks).
- **Caps**: ≤ **64** live fx cards (further cards skipped), ≤ **40** live attack-telegraph cards (telegraph calls skipped
  from 34 on), ambient presets (*amb*) skipped from 40 live fx cards on; two own pools never counted against those: the
  **dressing pool** ≤ 16 cards (`fx/dress/*`) and the **flood pool** ≤ 48 cards (`p/flood`). Presets marked *ptcl* draw
  particles only (0 cards).
- **Sounds**: vanilla events only, played `hostile` to `@a[tag=player]` at the executing position with the shared
  `minVolume` rule (`mboss_lib.min_volume`), pitch 0.5-2. The creature events plan §8 names are allowed (warden, ravager,
  slime, breeze, creaking, allay, puffer fish, dolphin, phantom, iron golem, armadillo, evoker fangs, creeper fuse);
  **the death sequence (D) uses no creature vocals**. Layers below are `event volume pitch`; a layer without values plays at
  `0.8 1.0` (AP-FX tunes).
- **Anchors**: positions on the boss come from the rig manifest (`rest_anchors`, `stances.rest_anchors`, per-clip
  `anchors` and `tracks`; `ap_contract.md` §0.4) through `api.py`, never from numbers typed in pattern code.

### 0.3 Card engine (same arguments as the fg / Azhdaha kits)

| function | args | does |
|---|---|---|
| `fx/card` | `{kind,pos,rot,bb,roll,spin,s0,s1,move,life,fade,col}` | one fx card (fg §2.1) |
| `fx/cardx` | `card`'s + `{off,dly,dur,hit,col2}`, vector `s0` / `s1` | the full card (fg §2.2; first-tick fix fg §2.3) |
| `fx/look` | `{kind,col}` | as `@s` (a module item_display): the kind's model + tint, full bright |
| `fx/prop/<name>` | – | as `@s`: a complete prop look (§0.7) |
| `fx/clear` | – | every kit card (fx, telegraphs, waves, rims, rings, the flood pool; **not** the dressing pool), counts zeroed |
| `fx/tele/clear` | – | attack telegraphs, waves, safe rims, moving rings, wall spots, the mask wash |
| `fx/dress/clear` | – | the dressing pool |
| `fx/uninstall` | – | cards, pools, demo anchor, objectives, `#wk*`, storage `rlk:apkit`, schedules |
| `fx/test/{kinds,tele,presets,sounds,hud,props,stage,stop}`, `fx/test/demo/<name>` | – | the fg kit's test set; demos per §8 item on the stand-in anchor |

A dead or reviving player clears every card by itself (fg rule).

### 0.4 Ground telegraphs (`fx/tele/*`, macros; sizes in tenths)

| function | args | drawn at | used by (§8) |
|---|---|---|---|
| `tele/disc` | `{r,tell,el,nd,hold}` | the floor point | P1 burst, P2 plunge, P3 slams, P4 (`el:23`, `hold:31` = the active window), P6 hits 2-4, Q1 burst / slam / sweep, Q3 shells, Q3s splash / shell, Q5 landings, O6a, O7 |
| `tele/sector` | `{r,a,tell,el,nd,hold}` — `a` = half-angle, **any integer 1..180, drawn within 1°**; `a ≥ 175` draws a disc | the apex, rotated = aim | P6 hit 1 (78°), O1 basic cone (27°), O6b bites (24°) |
| `tele/wedge` | `{r0,r1,a0,a1,tell,el,nd,hold}` — an annular sector between `a0 < a1` (degrees relative to the executor's yaw, + = clockwise from above, `a1 − a0` ≤ 180), radii `r0..r1` (Azhdaha fx.md §3.1) | the swept tick's tail root, rotated = the reference yaw | P5 / Q4 lanes: **one call per swept tick**, stacked by the host at the lane start (§0.11) |
| `tele/line` | `{len,w,back,tell,el,nd,hold}` — covers −back..len along the aim, `w` wide (`hz/line` + `#hzBack`) | the start point, rotated = aim | P1 sweep lane, Q5 leaf blades, O2 bolt aim lane (`w` = 2 × the bolt's hit radius) |
| `tele/crack` | `{len,w,back,tell,nd,hold}` — `tele/line` geometry in the white-gold glowing crack-line look (the plan's `crack_lines`, gold fixed) | the stalk root, rotated along the strip | P2 strips |
| `tele/wave` | `{id,r0,r1,w,tell,dur,el,nd,hold}` (id 0-7) — a disc fills to `r0` over `tell`, then the front ring travels `r0 → r1` in `dur` ticks with the band edge `w` behind | the floor centre | P3 thorn-wheel carpet (ids 0-2, one per slam) |
| `tele/wave_end` | `{id}` | – | P3 cancel |
| `tele/mask_wash` | `{r,tell,hold}` — one floor-wide card over radius `r` (the `el:24` field look); the domes' safe rims sit on it | the arena centre | Q2 field |
| `tele/safe_rim` | `{id,r,tell,hold}` (id 0-5) — a dome footprint: pale rim ring with a bright edge + the dome glyph | the dome centre | Q2 footprints, from the banner B0 to the pop |
| `tele/safe_end` | `{id}` | – | Q2 pop, cancel |
| `tele/mring` | `{id,r,el}` (id 0-3) — a moving target ring without fill timing (**not a hazard decal**) | the floor point | Q3 target ring (`id:0`, `r:36`, `el:22`) |
| `tele/mring_move` | `{id,t}` — move ring `id` to the executing point over `t` ticks (`teleport_duration`) | the new point | Q3 (every 2 t, `t:2`) |
| `tele/mring_end` | `{id}` | – | Q3 lock 1, cancel |
| `tele/wall_spot` | `{tell,hold}` — one 둥지 blade footprint (1.4 × 0.5 b bar, pale yellow-green; no damage) | the blade spot, rotated = blade facing | O4 walls (`tell:12`, `hold:40`) |
| `tele/clear` | – | – | core (pause, death, cancel) |

`api.wedges()` (AP-CORE) builds the per-tick `hz/sector` wedges of a swing and the matching `tele/wedge` stack from the
same rig-manifest data (`tracks.tail_root` × the dense `yaw` × r), so the drawn union equals the hit union by
construction (plan §7.11 rule 3).

### 0.5 Long-lived dressing (`fx/dress/*`, the dressing pool)

| function | args | does | used by |
|---|---|---|---|
| `dress/swirl` | `{r}` | the Heart's gold swirl ring decal (r 35) at the arena centre | T1 t45 → CS t24 |
| `dress/ley` | `{n}` | `n` (6-8) pulsing orange-gold ley-line crack strips from the centre to r 14 ("지맥 이상"), bearings from a fixed table | T1 t106 → CS t24 |
| `dress/redraw` | – | re-make the pool from `rlk:apkit dress` (after `/reload`, which kills the `rlk_mb_aux` cards) | `reload` in phase 2 |
| `dress/clear` | – | remove the pool | CS white-out, cleanup, uninstall |

### 0.6 Presets (`fx/p/<name>`; args in tenths; executor = the "at" column)

| preset | args | at | what | used by |
|---|---|---|---|---|
| `p/spark` | – | any | small lime-gold spark burst | tells, clicks |
| `p/flash` | – | any | white-green glow flash | bright moments |
| `p/leaf_splash` | – | floor | leaf + mote splash (withered field; airborne spray) | P1 land, P4 crash, Q3 shell 1 |
| `p/water_splash` | – | floor | water + leaf splash on the lush sheet | Q1, Q3s, CS t92, D t82 |
| `p/burrow_pool` | `r` | floor | dark olive leaf pool spreading to `r` (35 = 7 b Ø), 40 t | E t0, P1 t4, P3 t5 |
| `p/leaf_flakes` | – | floor | black leaf flakes rising | E, P1 sink |
| `p/bulb_flash` | – | the Heart bulb | the bulb flash | E t60 |
| `p/gold_embers` | – | the bulb | golden leaf embers drifting (every 4 t) *amb* | E t63-80 |
| `p/shadow_glide` | – | hidden anchor (floor) | underground travel: dark leaf ripple + dust (every 2 t) *amb* *ptcl* | P1 t23-44, P3 t23-39 |
| `p/gold_burst` | – | floor | white-gold flash + radial crystal blades, airborne | P1 burst, P3 slams |
| `p/leaf_debris` | – | floor | black leaf debris + pale ghost-leaf spray | P1 burst |
| `p/slash_band` | `len` | lane start, rotated = aim | white-gold streak 1-2.5 b high along the lane | P1 sweep |
| `p/spine_afterimage` | `len` | lane start, rotated = aim | pale rib afterimages along the sweep path, 10 t | P1 sweep |
| `p/root_chunks` | – | floor | brown root chunks with gold glints sinking | R t4, T1 t20 / t30 |
| `p/emerge_motes` | – | body | white-green motes of the 4 t scale-in | R t18 |
| `p/swirl_wisps` | – | body | pale-green spirals, whirling leaves (every 4 t) | P2 t5-27 |
| `p/plunge_flash` | – | floor | white-gold plunge flash | P2 t30 |
| `p/splinter_splash` | – | floor | green splinter splash | P2 t30 |
| `p/slam_arc` | – | stalk root, rotated along the strip | slam arc trail + flash + green splinters | P2 slams |
| `p/gold_glow` | `r` | floor | soft gold ground glow, **no rim** (must not read as a telegraph) | P3 t39-44 |
| `p/crown_debris` | – | body | crown / hood emergence debris | P3 t44 |
| `p/spiral_wisps` | – | body | wind-up spirals around the column (every 4 t) | P3 t94-130 |
| `p/blade_burst` | `r` | floor | gold blade rays to `r`, airborne | P3 slams (`r` 72) |
| `p/wheel_carpet` | `r0,r1,dur` | floor centre | 18-20 pale-green thorn-wheel cards riding the carpet front r0 → r1 in `dur` (call on the tick before the slam, fg `wave_band` rule) | P3 slams |
| `p/homing_trail` | – | a homing wheel prop | gold-orange spark trail (every 2 t) *ptcl* | P3 |
| `p/wheel_pop` | – | the prop | wheel pop sparks (r 1.5) | P3 end of life / hit |
| `p/spin_trails` | – | body | spark trails white-gold → pale green (every 3 t) | P4 t47-71 |
| `p/spin_flash` | – | body | mid-spin flash | P4 t57 |
| `p/tail_tip_flash` | – | tail tip anchor | the white tail-tip flash ("dash now" cue) | P5 t23, Q4 t11 |
| `p/arc_trail` | `r,a,dir` | tail root, rotated = arc mid-bearing | white-gold arc trail over a swing (`a` half-angle, `dir` ±1) | P5 swings |
| `p/arm_sweep` | `r,a` | body, rotated = aim | arm-sweep arc + ground furrow | P6 hit 1 |
| `p/slam_burst` | – | floor | double-slam radial burst + dark debris + white-gold cracks | P6 hit 2 |
| `p/spin_ring` | `r` | body | ring of gold sparks | P6 hit 3 |
| `p/leap_slam` | – | floor | biggest flash + black / gold debris | P6 hit 4 |
| `p/spawn_marker` | – | spawn point | pale wireframe dome, 20 t | T1 t116, every organism spawn |
| `p/org_burst` | – | organism | pale-green burst | basic kill, failure, CS wilt |
| `p/heart_gain` | – | the bulb | gain sparkle | `heart/add` |
| `p/heart_hit` | – | the bulb | red-gold motes | `heart/sub` |
| `p/crown_flare` | – | basic's crown | crown flare | O2 t3-12 |
| `p/comet_trail` | – | the bolt prop | green comet trail, bow ≤ 0.5 b (every 2 t) *ptcl* | O2 |
| `p/shield_pop` | – | basic | yellow 3-leaf crown flash | O3 shields up, a pool breaking |
| `p/guard_death` | – | 수호 | red embers + black twisted wisp | O3 death |
| `p/wall_motes` | – | blade | dissolve motes | O4 |
| `p/blink_flash` | – | 둥지 | blink flash | O4 blink out 0 / in 3 |
| `p/tether` | `len` | the 양육 orb, rotated facing the basic (pitch counts) | one wavy tether beam, dust `#D4E784` (refresh every 2 t) *ptcl* | O5 |
| `p/nurt_burst` | – | 양육 | green-yellow self-destruct sparks | O5 |
| `p/bite_flash` | – | bite point | white-yellow bite flash | O6b |
| `p/pred_burst` | – | 포식성 | burst r 3.6 | O6a t42 |
| `p/fuse_pulse` | – | 파괴 face | fuse glow pulse (every 9 t, every 4 t in the last 20 t) | O7 |
| `p/blast_dome` | – | 파괴 | green translucent dome r 3, 12 t | O7 blast |
| `p/cradle_dust` | – | the cradle | root-chunk dust of the cradle rise | T1 t45-65 |
| `p/heart_beam` | – | the cradle | green-gold light beam, 10 t | T1 t100 |
| `p/gold_motes` | – | floor centre | drifting gold motes (every 20 t) *amb* | phase 2 |
| `p/shock_ring` | – | floor centre | Dendro shock ring r 0 → 26 | 「소생 실패」 |
| `p/wilt_ring` | – | floor centre | green pulse ring r 0 → 26 over 20 t | CS t0 |
| `p/gold_drip` | – | the egg | gold dripping (every 3 t) *amb* | CS t0-24 |
| `p/ember_arc` | `len,h` | a bank twig (theme `POINTS['ember_twig']`), rotated facing the egg | the 「불씨」 spark arcing into the egg | CS t64-76 |
| `p/green_lightning` | – | the egg | green lightning ribbons | CS t76-84 |
| `p/revival_burst` | – | floor centre | leaf splash of the Warden bursting out | CS t92 |
| `p/leaf_mound` | – | floor | leaf mound + spray at the sink | Q1 t8, Q3s t8 |
| `p/leaf_pad` | – | hidden anchor (floor) | one translucent 2-3 b leaf pad, life 30 t (every 4 t) *amb* | Q1 t16-42, Q3s t20-36 |
| `p/rosette` | – | burst point | 8-12 glowing leaves rising, airborne (the ground ring is `tele/disc r 42`) | Q1 t32 |
| `p/surface_burst` | – | burst point | white-lime flash + leaf spray | Q1 t44 |
| `p/hoop_trail` | – | body | the hoop arc trail | Q1 t44-49 |
| `p/belly_splash` | – | floor | belly-flop splash | Q1 t61 |
| `p/sweep_ring` | `r` | body | leaf-blade ring of the 360° whip (core `#E0F996`, rim `#A2CA6C`) | Q1 t69 |
| `p/light_sprouts` | – | body | light sprouts at the rise | Q1 t71 |
| `p/crouch_splash` | – | body | splash as it crouches to charge | Q2 t0 |
| `p/whirl_leaves` | – | body | whirling leaves (every 3 t) | Q2 t18-36 |
| `p/field_ring` | `r0,r1,dur` | floor centre | flat translucent yellow-green wave r0 → r1 in `dur` (the visible front of the field release) | Q2 t40 |
| `p/floor_glitter` | – | floor centre | glitter on the tinted floor (every 10 t) *amb* | Q2 t80-155 |
| `p/light_pillar` | – | dome centre | 10 t light-pillar tell | Q2 t44 / 48 / 52 |
| `p/dome_rise` | – | dome centre | base-rim sparkle as a dome forms | Q2 t54 / 58 / 62 |
| `p/beam_rain` | – | floor centre | falling light columns over the disc (every 4 t) | Q2 t134-156 |
| `p/flood` | `life` | floor centre | yellow flood tiles over the walk disc that **skip every cell within the dome radius of a live `rlk_mb_ap_dome`** (flood pool) | Q2 t156 |
| `p/dome_pop` | – | dome centre | pop flash + shards | Q2 t189 |
| `p/green_burst` | – | body | green burst | Q2 t190 |
| `p/launch_flash` | – | the crown / muzzle anchor | launch flash | Q3 t35, Q3s t46 |
| `p/beam_column` | `w` | floor | vertical light beam column `w` wide (`#FDFBBD`) | Q3 t45, Q3s t48, Q5 t14 |
| `p/spores` | – | floor | spore puffs *amb* | Q3 t45 |
| `p/shell_streak` | `h` | floor point | a yellow streak falling from `h` above onto the point (call 6 t before) | Q3 t87 / 90 |
| `p/shell_burst` | – | floor | burst r 3 | Q3 t93 / 96, Q3s t48 |
| `p/leaf_ring` | – | floor | leaf cards circling the surfacing decal | Q3s t26-36 |
| `p/surface_splash` | – | floor | surfacing splash | Q3s t36 |
| `p/light_band` | `len` | muzzle anchor, rotated = the shot | horizontal light band of the flat shot | Q3s t46 |
| `p/crescent_trail` | `r,a,dir` | tail root, rotated = arc mid-bearing | green crescent trails (`#A4D6AC / #BFE682 / #EBF898`) | Q4 swings |
| `p/glitter_shower` | – | body | glitter shower | Q4 t53 |
| `p/charge_streaks` | – | body | charge streaks converging | Q5 t10-19 |
| `p/star_flare` | – | the glint point | 4-point star flare | Q5 t37 / t43 |
| `p/helix_trail` | – | an orb prop | double-helix ribbon (two sine strands, dust `#E7F99F` → `#8BCAAA`; every tick) *ptcl* | Q5 t42-55 |
| `p/orb_impact` | – | floor | star burst + upthrust crystal / leaf spikes | Q5 t49 / t55 |
| `p/leaf_skim` | `len` | lane start, rotated = aim | skimming pale-yellow leaf blades | Q5 t64 |
| `p/leaf_dissolve` | – | body | white leaflet burst (every 6 t) | D t100-118 |
| `p/haze_withered` | – | floor centre | olive `dust` drift (every 10 t) *amb* *ptcl* | phase 1, T1, phase 2 |
| `p/haze_lush` | – | floor centre | `spore_blossom_air` + `happy_villager` glints (every 10 t) *amb* *ptcl* | from CS t64 |

Energy particles on kills are the framework's (`function rlk:char/particles {n:1,el:7}`, 파괴 `n:4`), not the kit's.

Plan §8 proposal names that are a different kit call: `ring_gold` = `tele/disc` with `el:20` (the P1 burst disc is the
gold ring); `rot_disc` = `tele/disc {r:90,tell:24,el:23,nd:0,hold:31}`; `crack_lines` = `tele/crack`; `target_ring` =
`tele/mring` (`el:22`); `leaf_pads` = `p/leaf_pad` every 4 t; the `rosette` ground ring = `tele/disc {r:42}` and its
airborne petals = `p/rosette`; `thorn_wheel` / `thorn_wheel_homing` = the props of §0.7 (carpet wheels as cards in
`p/wheel_carpet`); `seed_orb` = `prop/seed_orb`; the Q2 "floor tinted" = `tele/mask_wash`; `light_pillar`, `flood`,
`field_ring`, `beam_rain`, `beam_column`, `sweep_ring` keep their names as presets.

### 0.7 Props (`fx/prop/<name>`, as `@s` = a display the module owns)

| prop | look | used by |
|---|---|---|
| `prop/thorn_wheel_homing` | gold-orange thorn wheel Ø 2 (rim and core) with a red 4-point flare, camera-facing spin | P3 homing `pj` (`#pjNoDodge 1`) |
| `prop/thorn_wheel` | pale-green carpet wheel Ø 1.6 (the card look of `p/wheel_carpet` as a prop) | P3 (prop fallback) |
| `prop/seed_bolt` | O2 ranged bolt: lime seed ball Ø 0.6 with a glow, camera-facing | O2 `pj` |
| `prop/seed_orb` | Q5 orb Ø 0.6-0.8, glowing yellow-green with a spiral glyph, camera-facing, bob | Q5 visual projectiles moved by the module |
| `prop/charge_ball` | Q3 light ball (`#FDFBBD` core, white-green halo), camera-facing | Q3 t14-35 at the crown anchor + 1.5 b |
| `prop/water_sheet` | one 14 b translucent water tile (≈ 40 % alpha), flat | theme `props('lush')` kind `water_sheet` (16 tiles at y 201.005) |
| `prop/lily_pad`, `prop/bell_flower`, `prop/bulb_flower` | lush pond dressing beyond r 22 | theme `props('lush')` |
| `prop/bank_crystal` | gold crystal spikes on the bank r 26-29, brightness 15 | theme `props()` (both looks) |
| `prop/gate_crystal` | gold-green crystal display (≈ 1.5 b, brightness 15, static) | the entrance room: `AP:prep` summons them at the theme's `entrance_layout()['glyphs']` spots (`ap_contract.md` §0.6.7) |

Leaf pads, rosette petals, light pillars and flood tiles (plan §5.3 "kit props") are **card kinds inside the presets**,
not module-owned displays. Item models usable outside the kit: `rlk:mboss/ap_kit/<prop>` for the theme's prop records
(`ap_contract.md` §0.6.6) and `rlk:mboss/ap_kit/gate_crystal` (the gate's second icon, `cprep.apep.gate.model2`,
`ap_contract.md` §0.6.7). Keep `teleport_duration:1` on moving props.

### 0.8 Sound recipes (`fx/snd/<name>`, no args)

| recipe | layers (`event volume pitch`; none = 0.8 1.0) | used by |
|---|---|---|
| `e_emerge` | entity.warden.emerge – 0.8; block.rooted_dirt.break (×3); block.azalea_leaves.break | E t0-31 |
| `e_flash` | block.amethyst_block.chime; block.beacon.power_select – 1.5 | E t60 |
| `e_heart_up` | block.vine.step; block.amethyst_block.resonate – 1.2 | E t70 |
| `e_roar` | entity.ravager.roar 0.6 1.3 | E t100 |
| `p1_dive` | entity.warden.dig – 0.9; block.rooted_dirt.break; block.mud.break | P1 t4, P3 t5, T1 t20 ("sink as P1") |
| `p1_travel` | entity.warden.dig 0.4 1.2; block.gravel.step – 0.5 | P1 every 7 t underground |
| `p1_ring` | block.beacon.activate 0.4 1.5 | P1 t32 |
| `p1_burst` | entity.warden.emerge – 1.4; block.amethyst_cluster.break; entity.generic.explode 0.4 1.3 | P1 t44 |
| `p1_sweep` | entity.player.attack.sweep – 0.5; entity.breeze.wind_burst – 0.6 | P1 t64 |
| `p1_land` | entity.ravager.step; block.moss.fall | P1 t77 |
| `r_sink` | block.rooted_dirt.break – 0.6 (×3); entity.warden.dig – 1.1 | R t4 |
| `r_emerge` | entity.warden.emerge 0.6 1.3; block.azalea.place | R t18 |
| `p2_swirl` | entity.breeze.whirl – 0.7; block.beacon.ambient – 1.6 | P2 t5 |
| `p2_swirl_tick` | block.azalea_leaves.break – 0.8 | P2 every 3 t, t5-27 |
| `p2_plunge` | entity.warden.dig – 0.7; entity.evoker_fangs.attack; block.rooted_dirt.break | P2 t30 |
| `p2_stalks` | block.hanging_roots.break; entity.warden.emerge 0.5 1.5 | P2 t36 |
| `p2_lines` | block.sculk_sensor.clicking – 1.6 | P2 t40 |
| `p2_slam` | entity.iron_golem.attack – 0.6; entity.generic.explode 0.3 1.5; block.big_dripleaf.break | P2 slams |
| `p2_flower` | entity.ravager.roar 0.6 1.2; block.azalea_leaves.break | P2 t118 |
| `p2_fold` | entity.ravager.step | P2 t128 |
| `p3_emerge` | entity.warden.emerge – 1.1 | P3 t44 |
| `p3_glow` | block.beacon.activate 0.4 1.5; block.sculk_catalyst.bloom | P3 t39 |
| `p3_windup` | block.bamboo.break – 0.6; entity.breeze.idle_air | P3 t94 |
| `p3_slam` | entity.warden.attack_impact; entity.generic.explode 0.5 0.7; block.big_dripleaf.break | P3 slams |
| `p3_wheels` | block.amethyst_cluster.place (×3) | P3 each slam |
| `p3_wheel_roll` | block.azalea_leaves.step – 0.6 | P3 every 4 t while a carpet runs |
| `p3_wheel_hit` | entity.player.hurt_sweet_berry_bush; block.amethyst_cluster.break | P3 thorn hit (`#mbHitEv`) |
| `p3_homing_loop` | block.amethyst_block.resonate – 1.6; entity.blaze.burn 0.3 1.8 | P3 every 10 t per homing wheel |
| `p4_rear` | entity.breeze.wind_burst 0.5 0.6; block.azalea_leaves.break | P4 t0 |
| `p4_hum` | block.beacon.ambient 0.4 1.4; block.sculk_sensor.clicking | P4 t16 |
| `p4_spin` | entity.ravager.attack – 0.6; entity.player.attack.sweep – 0.5 (×3); entity.generic.splash | P4 t40 |
| `p5_raise` | entity.breeze.idle_air – 0.7 | P5 t8 |
| `p5_cock` | entity.creaking.activate – 1.4; item.trident.riptide_1 – 0.6 | P5 t23 (the cue) |
| `p5_swing` | entity.player.attack.sweep – 0.6; item.trident.throw – 0.5 | P5 t28 / t52 |
| `p5_hit` | entity.player.attack.knockback | P5 / Q4 hit (`#mbHitEv`) |
| `p6_sweep` | entity.player.attack.sweep – 0.7; block.grass.break | P6 hit 1 |
| `p6_slam` | entity.warden.sonic_boom 0.5 1.6; entity.generic.explode – 0.7; block.mud.break (×4) | P6 hits 2 / 4 |
| `p6_spin` | entity.player.attack.sweep – 0.6; entity.player.attack.sweep – 0.8 | P6 hit 3 |
| `m_crawl` | entity.camel.step – 0.6; block.moss_carpet.step; block.azalea_leaves.step | `crawl_p1`, `walk_p3` steps |
| `m_walk` | entity.warden.step – 0.8 | `walk_p1` steps |
| `o1_attack` | entity.slime.attack – 1.2; block.big_dripleaf.tilt_down | O1 strike |
| `heart_hit` | block.amethyst_block.hit 0.4 0.6 | every Heart loss |
| `heart_gain` | block.amethyst_block.chime, pitch 2^((k − 10) / 12) with k = ⌊#apHt / 1000⌋ (11 generated steps) | every Heart gain |
| `o2_pivot` | block.big_dripleaf.tilt_up – 1.4 | O2 t0 |
| `o2_charge` | entity.breeze.charge 0.4 1.6 | O2 t3 |
| `o2_shoot` | entity.breeze.shoot – 1.3 | O2 t12 |
| `o2_hit` | block.moss.break – 1.3 | O2 bolt end |
| `o3_collapse` | block.bamboo.break 0.5 0.8; block.mangrove_roots.place – 0.7 | O3 t0 / t16 |
| `o3_cast` | block.beacon.activate 0.5 1.6 | O3 t30 |
| `o3_pop` | block.amethyst_block.resonate – 1.4; item.shield.block 0.4 1.6 | O3 shields / a pool breaks |
| `o3_death` | block.chorus_flower.death; entity.slime.death – 0.7 | O3 death |
| `shield_hit` | item.shield.block 0.4 1.6 | a hit absorbed by `apShd` |
| `o4_rise` | block.big_dripleaf.place – 0.7 (×3); block.azalea.place; block.amethyst_cluster.place – 1.2 | O4 t12 |
| `o4_fade` | block.azalea_leaves.break; block.beacon.deactivate 0.3 2.0 | O4 dissolve |
| `o4_flap` | entity.phantom.flap 0.3 1.5 | O4 flying (every 14 t) |
| `o5_hum` | block.beacon.ambient 0.2 1.8 | O5 every 40 t while linked |
| `o5_destruct` | block.azalea_leaves.break; entity.allay.death – 1.3; block.amethyst_cluster.break | O5 self-destruct |
| `o6_gulp` | entity.generic.eat – 0.6; entity.slime.squish | O6a t12 |
| `o6_bud` | block.beacon.power_select 0.4 1.5 | O6a t12 |
| `o6_inflate` | entity.puffer_fish.blow_up – 0.8 | O6a t32 |
| `o6_burst` | entity.puffer_fish.blow_out; block.amethyst_cluster.break – 1.4; entity.firework_rocket.blast 0.5 0.8 | O6a t42 |
| `o6_bite` | entity.evoker_fangs.attack – 1.3; entity.ravager.attack 0.4 1.6 | O6b each bite |
| `o6_bite_first` | `o6_bite` + entity.player.attack.crit | O6b first bite of a chain |
| `o6_swim` | entity.dolphin.swim – 1.2 | O6 swimming (every 16 t) |
| `o7_roll` | entity.armadillo.roll – 0.8 | O7 every 8 t |
| `o7_primed` | entity.creeper.primed – 1.4 | O7 contact |
| `o7_suck` | entity.breeze.inhale – 0.8 | O7 suck-in |
| `o7_blast` | entity.generic.explode – 0.8; entity.warden.sonic_boom 0.3 1.6 | O7 blast |
| `org_kill` | block.azalea_leaves.break; entity.slime.squish_small | basic kill |
| `timeout_warn` | event.raid.horn 0.3 1.0 | time-out warning |
| `fail_strike` | block.respawn_anchor.deplete – 0.6; block.big_dripleaf.break – 0.5; block.sculk_shrieker.shriek 0.4 0.8 (**proposal**: plan §3.4 names no sound) | 「소생 실패」 |
| `t1_cradle` | block.rooted_dirt.break; block.mangrove_roots.place – 0.7 | T1 t45 |
| `t1_lower` | block.amethyst_block.resonate – 1.2; block.spore_blossom.break | T1 t50 |
| `t1_land` | block.honey_block.fall – 0.6; block.beacon.power_select – 1.4; block.amethyst_block.chime | T1 t100 |
| `t1_hud` | ui.toast.in – 1.2 | T1 t106 |
| `spawn_marker` | block.chorus_flower.grow; block.sculk_shrieker.place – 1.5 | every spawn marker |
| `cs_complete` | block.respawn_anchor.set_spawn – 1.3; block.amethyst_block.chime | CS t0 |
| `cs_ember` | block.fire.ambient 0.3 1.6 | CS t64 |
| `cs_flash` | block.beacon.activate; entity.lightning_bolt.thunder 0.3 2.0 | CS t80 |
| `cs_heal` | block.amethyst_block.resonate – 1.4 | CS t80 |
| `cs_emerge` | entity.warden.emerge – 0.8; block.azalea_leaves.break (×4) | CS t92 |
| `cs_reveal` | block.beacon.activate – 0.7 | CS t132 |
| `q1_sink` | entity.warden.dig – 1.2; block.mud.break; entity.player.splash.high_speed – 0.6 | Q1 t8, Q3s t8 |
| `q1_trail` | block.big_dripleaf.tilt_down – 0.8; block.lily_pad.place | Q1 / Q3s every 4 t underground |
| `q1_rosette` | block.flowering_azalea.place; block.spore_blossom.place – 0.6 | Q1 t32 |
| `q1_burst` | entity.warden.emerge 0.6 1.3; entity.generic.splash; block.big_dripleaf.break | Q1 t44 |
| `q1_slam` | entity.generic.explode 0.4 1.4; entity.player.attack.sweep – 0.6; entity.generic.splash | Q1 t61 / t69 |
| `q1_rise` | block.big_dripleaf.tilt_up; block.vine.step | Q1 t71 |
| `q2_banner` | block.respawn_anchor.set_spawn – 0.7; entity.elder_guardian.curse 0.4 1.4 | Q2 B0 |
| `q2_charge` | block.conduit.activate – 0.8; block.beacon.power_select – 0.6 | Q2 t0 |
| `q2_whirl` | entity.breeze.whirl | Q2 t18 |
| `q2_release` | entity.warden.sonic_charge – 1.4; entity.breeze.wind_burst – 0.6 | Q2 t40 |
| `q2_field_loop` | block.bubble_column.upwards_ambient; block.sculk.spread – 1.4 | Q2 every 20 t, t40-156 |
| `q2_tick` | entity.player.hurt_sweet_berry_bush | Q2 each landed field tick |
| `q2_dome` | block.beacon.activate – 1.8; block.amethyst_block.chime (×3); block.respawn_anchor.charge – 1.6 | Q2 t54 / 58 / 62 |
| `q2_rain` | block.beacon.power_select 0.5 1.8 | Q2 t134 |
| `q2_blast` | entity.warden.sonic_boom – 0.8; entity.dragon_fireball.explode – 0.7; entity.lightning_bolt.thunder 0.4 1.5 | Q2 t156 |
| `q2_pop` | block.glass.break 0.5 1.5; block.amethyst_cluster.break; block.bubble_column.bubble_pop | Q2 t189 |
| `q3_charge` | block.respawn_anchor.charge – 1.5; block.beacon.ambient | Q3 t14 |
| `q3_launch` | entity.breeze.shoot – 0.8; item.crossbow.shoot – 0.5 | Q3 t35 |
| `q3_impact1` | entity.generic.explode – 1.2; block.beacon.deactivate – 1.5; block.big_dripleaf.break | Q3 t45 |
| `q3_lock` | block.beacon.power_select – 1.6; entity.breeze.charge – 1.2 | Q3 t79 / 82 at the lock point (AP-FIX RV-02) |
| `q3_impact2` | entity.dragon_fireball.explode 0.5 1.4 | Q3 t93 / 96 |
| `q3s_surface` | block.mud.break; entity.player.splash – 0.6; block.azalea_leaves.break | Q3s t36 |
| `q3s_charge` | block.respawn_anchor.charge 0.6 1.5; block.amethyst_block.resonate – 1.6 | Q3s t36 |
| `q3s_launch` | entity.breeze.shoot – 0.8; item.trident.riptide_1 0.5 1.4 | Q3s t46 |
| `q3s_impact` | entity.generic.explode 0.5 1.3; block.beacon.activate – 1.8; block.cherry_leaves.break | Q3s t48 |
| `q4_swing` | `p5_swing` + block.azalea_leaves.fall (×3) | Q4 t14 |
| `q4_rear` | entity.creaking.activate – 0.6; entity.ravager.step – 0.6 | Q4 t3, t36 |
| `q4_swing2` | `q4_swing` + block.amethyst_cluster.step (×4) + item.bone_meal.use | Q4 t46 |
| `q5_unfold` | entity.breeze.charge – 1.2; block.big_dripleaf.tilt_up – 0.6; block.amethyst_block.chime (×3) | Q5 t10 |
| `q5_orb` | block.amethyst_cluster.place; block.beacon.ambient 0.3 1.8 | Q5 each orb (t19-32) |
| `q5_flare` | block.beacon.power_select 0.5 1.8 | Q5 t37 / 43 |
| `q5_launch` | entity.arrow.shoot – 0.6 (×6); item.trident.throw 0.4 1.4 | Q5 t42 / 48 |
| `q5_impact` | entity.generic.explode 0.3 1.6; block.amethyst_cluster.break – 0.8; block.pointed_dripstone.land | Q5 t49 / 55 |
| `q5_blades` | entity.breeze.wind_burst – 1.2; block.cherry_leaves.fall | Q5 t64 |
| `d_droop` | block.big_dripleaf.break – 0.5 | D t30 |
| `d_face_fade` | block.beacon.deactivate – 0.6 | D t30 (face → `p3_dim`) |
| `d_leaves` | block.azalea_leaves.break (×3) | D t85, 100, 110 |
| `d_splash` | entity.generic.splash | D t82 |
| `d_sink` | block.respawn_anchor.deplete – 0.8 | D t100 |
| `d_seed` | block.amethyst_block.chime | D t120 (the seed prop) |

Single extra layers stay `g.sound(event, vol, pitch)` in the module (Azhdaha fx.md §8).

### 0.9 HUD (font `rlk:mboss_ap`, U+E900-E9FF)

The kit owns **no boss-bar line** (Azhdaha fx.md D9): the core composes `extra[]` / `sub[]` from `K.glyph(name)` /
`K.badge(kind, on)` strings; the under-bar countdowns (time to the time-out warning; the Q2 two-segment countdown red →
gold) and the Heart progress bar (`#buHpCol bu 10` = `#EDCF63`, `#buNoNum bu 1`, cm.md §11) are the core's bossui lines.
Sub-lines and first-time hints are typed by the core with `rlk:mboss/line/say` from the texts in `api.py`.

| function | args | does | used by |
|---|---|---|---|
| `hud/title` | `{g,t,c,s,hold}` | the title line: glyph `g` (`heart`, `warn`, `fail`, `success`, `none`) + the module's text `t` in colour `c`, subtitle `s`, for `hold` ticks | T1 t106 「오아시스의 심장」, the time-out "!", 「소생 실패」, "오아시스의 심장이 소생했습니다" |
| `hud/banner_aftermath` | – | actionbar banner "**소생의 찬가 보호막** 안으로 들어가서 종말의 여파를 막아내세요" (the first phrase red `#C36E5A`, the rest white) with the dome glyph, held until `banner_end` | Q2 B0 → t156 |
| `hud/banner_end` | – | drop the banner | Q2 t156, cancel |
| `hud/whiteout` | `{hold}` | full-screen white on the title line: fade-in 4 t, `hold`, fade-out 8 t (no Blindness, no FOV change) | CS t24 (`hold:28` → white to t64) |
| `hud/flash_white` | – | full-screen white flash, 6 t | Q2 t156 |
| `hud/flash_green` | – | full-screen green flash (`#B6E35A`), 8 t | CS t80 |
| `hud/flash_hit` | – | thin white-gold edge flash, 3 t | P5 / Q4 tail hit ("screen flash on a hit") |
| `hud/flash_end` | – | drop a title overlay at once | pause, cancel |
| `hud/clear` | – | every banner / overlay off | cleanup, death, abort, uninstall |

Glyphs: U+E900 Apep badge; U+E901-E905 special badges ◆ (수호, 둥지, 양육, 포식성, 파괴); U+E906 "⚠"; U+E910-E913 title
glyphs (heart, warn "!", fail = the withered Heart, success); U+E914 the dome glyph; U+E920-E923 full-screen flats (white
1.0, white 0.9, green 0.5, edge vignette 0.35); U+E9F0-E9F2 spaces −1 / +2 / +1. `K.badge(kind, on)`: kinds `guard`,
`nest`, `nurt`, `pred`, `destr`, `fail`, dim `#707070` when off, the kind's colour when on (the phase-2 name line "◆수호").
The generator refuses to write the font when a codepoint collides with any `assets/*/font/*.json` (`hud`, `minimap`,
`bossbar`, `mboss_gd`, `mboss_bf`, `mboss_fg`, `mboss_az`; FN-28).

### 0.10 Python API (`import build_mboss_ap_fx as K`; no files written on import; mirrored by the no-op `api.K` until AP-I1)

```python
K.card(kind, pos='~ ~ ~', rot='~ ~', bb='fixed', roll=0, spin=0, s0=0.0, s1=1.0, move=(0, 0, 0), life=8, fade=0,
       col=K.WHITE, dly=0, dur=0, hit=-1, col2=-1, off=None)
K.tele_disc(r, tell, el=7, nd=0, hold=3);            K.tele_sector(r, a, tell, el=7, nd=0, hold=3)
K.tele_wedge(r0, r1, a0, a1, tell, el=7, nd=0, hold=3)
K.tele_line(length, w, tell, el=7, nd=0, hold=3, back=0.0); K.tele_crack(length, w, tell, nd=0, hold=3, back=0.0)
K.tele_wave(wid, r0, r1, w, tell, dur, el=7, nd=0, hold=2); K.tele_wave_end(wid)
K.tele_mask_wash(r, tell, hold);  K.tele_safe_rim(sid, r, tell, hold);  K.tele_safe_end(sid)
K.tele_mring(mid, r, el=22);  K.tele_mring_move(mid, t=2);  K.tele_mring_end(mid);  K.tele_wall_spot(tell, hold)
K.dress(name, **args)            # 'swirl' (r=3.5), 'ley' (n=7), 'redraw', 'clear'
K.fx(name, **args); K.snd(name); K.prop(name); K.look(kind, col); K.hud(name, **args); K.glyph(name); K.badge(kind, on)
K.KINDS, K.PRESETS, K.SOUNDS, K.PROPS, K.GLYPHS, K.AMBIENT, K.TELE_COL         # tables
K.CAP, K.TCAP, K.SOFT, K.DCAP, K.FLCAP                                          # 64 / 40 / 40 / 16 / 48
K.FN, K.FONT, K.OWNED_DIRS, K.OWNED_FILES                                       # 'rlk:mboss/apep/fx/', 'rlk:mboss_ap'
```

Every builder takes blocks (degrees for angles, ticks for times) and writes tenths, and asserts that its name exists;
macro placeholders are allowed inside macro presets (fg §8).

### 0.11 Per-pattern call index (§8 → kit; `t` = the pattern clock, played ticks; values in blocks as `K.*` takes them)

Hazards (`hz/*`, `pj/*`, `#hzQuiet 1`) are the module's and are not repeated; every telegraph row is paired with its
hazard. "body" = `execute as <body> at @s rotated as @s rotated ~ 0`; "floor" = a floor point rotated as the aim;
"L" = a locked point.

| item | t | where | calls |
|---|---|---|---|
| **E** | 0 | floor under the body | `fx('burrow_pool', r=3.5)`, `fx('leaf_flakes')`, `snd('e_emerge')` |
| | 60 / 63-80 / 70 / 100 | bulb / bulb / – / body | `fx('bulb_flash')` + `snd('e_flash')`; `fx('gold_embers')` every 4 t; `snd('e_heart_up')`; `snd('e_roar')` |
| **P1** | 4 / 8 | floor | `fx('burrow_pool', r=3.5)` + `snd('p1_dive')`; `fx('leaf_flakes')` |
| | 23-44 | hidden anchor | `fx('shadow_glide')` every 2 t; `snd('p1_travel')` every 7 t |
| | 32 / 44 | L | `tele_disc(4.2, 12, el=20)` + `snd('p1_ring')`; `fx('gold_burst')`, `fx('leaf_debris')`, `snd('p1_burst')` |
| | 52 / 64 / 77 | body (yaw locked at 52) | `tele_line(10.8, 3.6, 12, el=20)`; `fx('slash_band', len=10.8)` + `fx('spine_afterimage', len=10.8)` + `snd('p1_sweep')`; `snd('p1_land')` |
| **R** | 4 / 18 | floor / body | `fx('root_chunks')` + `snd('r_sink')`; `fx('emerge_motes')` + `snd('r_emerge')` |
| **P2** | 0 | body floor | `tele_disc(4.2, 30, el=20)` (the plunge at t30) |
| | 5-27 | body | `fx('swirl_wisps')` every 4 t; `snd('p2_swirl')` at 5, `snd('p2_swirl_tick')` every 3 t |
| | 30 / 36 | floor | `fx('plunge_flash')`, `fx('splinter_splash')`, `snd('p2_plunge')`; `snd('p2_stalks')` (stalk props: org `leg_rise`) |
| | 40 | each stalk root, rotated through L | `tele_crack(8.4, 3.0, 22 / 29 / 35 / 42)`, `snd('p2_lines')` |
| | 62 / 69 / 75 / 82; 118 / 128 | the slamming stalk's root; body | `fx('slam_arc')` + `snd('p2_slam')`; `snd('p2_flower')`; `snd('p2_fold')` |
| **P3** | 5 / 23-39 | floor / hidden anchor | `fx('burrow_pool', r=3.5)` + `snd('p1_dive')`; `fx('shadow_glide')` every 2 t |
| | 39 / 44 / 94-130 | centre / centre / body | `fx('gold_glow', r=3.0)` + `snd('p3_glow')`; `fx('crown_debris')` + `snd('p3_emerge')`; `fx('spiral_wisps')` every 4 t, `snd('p3_windup')` at 94 |
| | 111 / 141 / 164 | centre | slam decals `tele_disc(5.4, 30 / 23 / 31, el=20)` (slams t141 / 164 / 195) + `tele_wave(k, 3.0, 14.4, 1.0, <same tell>, 14)` with k = 0 / 1 / 2 |
| | slam − 1 / slam | centre | `fx('wheel_carpet', r0=3.0, r1=14.4, dur=14)`; `fx('gold_burst')`, `fx('blade_burst', r=7.2)`, `snd('p3_slam')`, `snd('p3_wheels')`, 2 × `prop('thorn_wheel_homing')`, `snd('p3_wheel_roll')` every 4 t for 14 t |
| | homing life | each wheel | `fx('homing_trail')` every 2 t, `snd('p3_homing_loop')` every 10 t, `fx('wheel_pop')` at the end; `snd('p3_wheel_hit')` on a hit |
| **P4** | 0 / 16 | body / body floor | `snd('p4_rear')`; `tele_disc(9.0, 24, el=23, hold=31)` + `snd('p4_hum')` |
| | 40 / 47-71 / 57 | body | `snd('p4_spin')` + `fx('leaf_splash')`; `fx('spin_trails')` every 3 t; `fx('spin_flash')` |
| **P5** | 8 / 14 | body / each swept tick's tail root | `snd('p5_raise')`; swing 1: 8 × `tele_wedge(0, 11.4, a0, a1, 28 + k − 14, el=20)` (k = 0..7; `a0 / a1` = the tail-line angles of ticks 27 + k / 28 + k from `api.wedges()`) |
| | 23 / 28 | tail tip / tail root | `fx('tail_tip_flash')` + `snd('p5_cock')`; `fx('arc_trail', r=11.4, a=100, dir=1)` + `snd('p5_swing')` |
| | 39 / 52 | swept tails / tail root | swing 2: 8 × `tele_wedge(0, 11.4, a0, a1, 52 + k − 39, el=20)`; `fx('arc_trail', r=11.4, a=100, dir=-1)` + `snd('p5_swing')` |
| | on a hit | player | `snd('p5_hit')`, `hud('flash_hit')` |
| **P6** | 4 / 14 | body, rotated = aim | `tele_sector(7.2, 78, 10, el=20)`; `fx('arm_sweep', r=7.2, a=78)` + `snd('p6_sweep')` |
| | 32 / 46 | 4.8 b ahead | `tele_disc(6.6, 14, el=20)`; `fx('slam_burst')` + `snd('p6_slam')` |
| | 73 / 83 | body | `tele_disc(7.2, 10, el=20)`; `fx('spin_ring', r=7.2)` + `snd('p6_spin')` |
| | 98 / 120 | 7.2 b ahead | `tele_disc(6.6, 22, el=20)`; `fx('leap_slam')` + `snd('p6_slam')` |
| **M** | step events | body | `snd('m_crawl')` (`crawl_p1`, `walk_p3`), `snd('m_walk')` (`walk_p1`) |
| **T1** | 20 / 30 / 45 | floor / floor / centre | `fx('root_chunks')` + `snd('p1_dive')`; `fx('root_chunks')`; `dress('swirl', r=3.5)` + `fx('cradle_dust')` + `snd('t1_cradle')` |
| | 50 / 100 / 106 / 116 | – / cradle / – / spawn points | `snd('t1_lower')`; `fx('heart_beam')` + `snd('t1_land')`; `hud('title', g='heart', …)` + `snd('t1_hud')` + `dress('ley', n=7)`; `fx('spawn_marker')` + `snd('spawn_marker')` |
| **phase 2** | events | – | `fx('heart_gain')` + `snd('heart_gain')`; `fx('heart_hit')` + `snd('heart_hit')`; `fx('gold_motes')` every 20 t; `fx('haze_withered')` every 10 t; time-out `snd('timeout_warn')` + `hud('title', g='warn', …)` |
| **O1** | 0 / 10 | basic, rotated at the Heart | `tele_sector(3.1, 27, 10)`; `snd('o1_attack')` |
| **O2** | 0 / 3 / 12 | basic / crown / crown | `snd('o2_pivot')` + `tele_line(<d>, 1.4, 12)`; `fx('crown_flare')` + `snd('o2_charge')`; `prop('seed_bolt')` + `snd('o2_shoot')`, `fx('comet_trail')` every 2 t, `snd('o2_hit')` at the end |
| **O3** | 0 / 16 / 30 / death | 수호 / 수호 / basics / 수호 | `snd('o3_collapse')` (0, 16); `snd('o3_cast')` + `fx('shield_pop')` + `snd('o3_pop')` per shielded basic; `fx('guard_death')` + `snd('o3_death')`; absorbed hits `snd('shield_hit')` |
| **O4** | 0 / 12 / +40 | blade spots | `tele_wall_spot(12, 40)` per blade; `snd('o4_rise')`; `fx('wall_motes')` + `snd('o4_fade')`; `fx('blink_flash')` at blink 0 / 3; `snd('o4_flap')` every 14 t |
| **O5** | every 2 t | orb → basic | `fx('tether', len=<d>)` per link; `snd('o5_hum')` every 40 t; self-destruct `fx('nurt_burst')` + `snd('o5_destruct')` |
| **O6a** | 12 / 32 / 42 | 포식성 | `snd('o6_gulp')` + `snd('o6_bud')`; `tele_disc(3.6, 10)` + `snd('o6_inflate')`; `fx('pred_burst')` + `snd('o6_burst')` |
| **O6b** | bite − 10 / bite | the locked sector | `tele_sector(2.6, 24, 10)`; `fx('bite_flash')` + `snd('o6_bite')` (`o6_bite_first` on the first); `snd('o6_swim')` every 16 t |
| **O7** | roll / contact / +56 / +61 | 파괴 | `snd('o7_roll')` every 8 t; `tele_disc(3.6, 61)` + `snd('o7_primed')` + `fx('fuse_pulse')`; `snd('o7_suck')`; `fx('blast_dome')` + `snd('o7_blast')` |
| **kills** | – | organism | basic `fx('org_burst')` + `snd('org_kill')`; specials their death clips |
| **failure** | 0 | centre / each organism | `fx('shock_ring')` + `snd('fail_strike')` + `hud('title', g='fail', …)`; `fx('org_burst')` each |
| **CS** | 0 / 0-24 | centre / egg | `fx('wilt_ring')` + `snd('cs_complete')` + `fx('org_burst')` each; `fx('gold_drip')` every 3 t |
| | 24 / 64-76 | – / twig | `hud('whiteout', hold=28)` + `dress('clear')`; `fx('ember_arc', len=<d>, h=3.0)` + `snd('cs_ember')`; `fx('haze_lush')` every 10 t from 64 |
| | 76-84 / 80 / 92 / 132 | egg / – / centre / – | `fx('green_lightning')`; `hud('flash_green')` + `snd('cs_flash')` + `snd('cs_heal')`; `fx('revival_burst')` + `fx('water_splash')` + `snd('cs_emerge')`; `snd('cs_reveal')` |
| **Q1** | 8 / 16-42 | floor / hidden anchor | `fx('leaf_mound')` + `snd('q1_sink')`; `fx('leaf_pad')` + `snd('q1_trail')` every 4 t |
| | 32 / 44 | L | `tele_disc(4.2, 12)` + `fx('rosette')` + `snd('q1_rosette')`; `fx('surface_burst')` + `fx('water_splash')` + `snd('q1_burst')`; `fx('hoop_trail')` 44-49 |
| | 46 / 48 | roll end / body | `tele_disc(4.2, 15)` (slam t61); `tele_disc(12.0, 21)` (sweep t69) |
| | 61 / 69 / 71 | floor / body / body | `fx('belly_splash')` + `snd('q1_slam')`; `fx('sweep_ring', r=12.0)` + `snd('q1_slam')`; `fx('light_sprouts')` + `snd('q1_rise')` |
| **Q2** | B0 | each dome centre | `hud('banner_aftermath')` + `snd('q2_banner')`; `tele_safe_rim(k, 4.5, <B0 → dome k forms>, <forms → pop>)` for k = 0..2 |
| | 0 / 18-36 | body | `fx('crouch_splash')` + `snd('q2_charge')`; `fx('whirl_leaves')` every 3 t + `snd('q2_whirl')` at 18 |
| | 40 | centre | `tele_mask_wash(26.0, 40, 96)` (filled at the first tick t80, held to t176) + `fx('field_ring', r0=3.0, r1=26.0, dur=18)` + `snd('q2_release')`; `snd('q2_field_loop')` every 20 t to 156 |
| | 44 / 48 / 52; 54 / 58 / 62 | dome k | `fx('light_pillar')`; `fx('dome_rise')` + `snd('q2_dome')` (dome props: org `dome_rise`) |
| | 80-155 / 134-156 | centre | `fx('floor_glitter')` every 10 t, `snd('q2_tick')` per landed tick; `fx('beam_rain')` every 4 t + `snd('q2_rain')` at 134 |
| | 156 / 189 / 190 | centre / dome k / body | `hud('flash_white')` + `fx('flood', life=24)` + `snd('q2_blast')` + `hud('banner_end')`; `fx('dome_pop')` + `snd('q2_pop')` + `tele_safe_end(k)`; `fx('green_burst')` |
| **Q3** | 10 → 33 | the feet 6 t ago | `tele_mring(0, 3.6, el=22)`, then `tele_mring_move(0, 2)` every 2 t |
| | 14-35 | crown + 1.5 | `prop('charge_ball')` on a module display; `snd('q3_charge')` at 14 |
| | 33 / 35 / 45 | L1 / crown / L1 | `tele_mring_end(0)` + `tele_disc(3.6, 12)`; `fx('launch_flash')` + `snd('q3_launch')`; `fx('beam_column', w=3.0)` + `fx('leaf_splash')` + `fx('spores')` + `snd('q3_impact1')` |
| | 79 / 82; 87 / 90; 93 / 96 | L2 / L3 | `snd('q3_lock')` at the lock point and the shell sliding to 5 b over it, then falling to it (AP-FIX RV-02; no floor decal: none row); `fx('shell_streak', h=2.9)`; `fx('shell_burst')` + `snd('q3_impact2')` |
| **Q3s** | 8 / 20-36 | floor / hidden anchor | `fx('leaf_mound')` + `snd('q1_sink')`; `fx('leaf_pad')` + `snd('q1_trail')` every 4 t |
| | 26 / 36 | surfacing point / player | `tele_disc(3.6, 10)` + `fx('leaf_ring')`; `fx('surface_splash')` + `fx('water_splash')` + `snd('q3s_surface')` + `snd('q3s_charge')` + `tele_disc(3.0, 12)` at the player |
| | 46 / 48 | muzzle / L | `fx('light_band', len=<d>)` + `fx('launch_flash')` + `snd('q3s_launch')`; `fx('beam_column', w=2.0)` + `fx('shell_burst')` + `snd('q3s_impact')` |
| **Q4** | 2 / 3 / 11 / 14 | swept tails / body / tip / tail root | swing 1: 8 × `tele_wedge(0, 12.0, a0, a1, 14 + k − 2)` (k = 0..7); `snd('q4_rear')`; `fx('tail_tip_flash')`; `fx('crescent_trail', r=12.0, a=100, dir=1)` + `snd('q4_swing')` |
| | 32 / 36 / 46 / 53 | swept tails / body / tail root / body | swing 2: 8 × `tele_wedge(0, 12.0, a0, a1, 46 + k − 32)`; `snd('q4_rear')`; `fx('crescent_trail', r=12.0, a=100, dir=-1)` + `snd('q4_swing2')`; `fx('glitter_shower')` |
| **Q5** | 10 / 14 / 19-32 | body / body / orb spots | `fx('charge_streaks')` + `snd('q5_unfold')`; `fx('beam_column', w=1.5)`; 12-14 × `prop('seed_orb')` + `snd('q5_orb')` |
| | 37 / 43 | glint / 6 + 6 landing points | `fx('star_flare')` + `snd('q5_flare')`; `tele_disc(2.0, 12)` × 6 per volley |
| | 42 / 48; 49 / 55 | orbs / landings | `snd('q5_launch')`, `fx('helix_trail')` every tick per orb; `fx('orb_impact')` per landing + `snd('q5_impact')` |
| | 52 / 64 | lane starts | `tele_line(14.0, 2.2, 12)` × 2; `fx('leaf_skim', len=14.0)` × 2 + `snd('q5_blades')` |
| **D** | 0 | – | `fx/tele/clear`, `hud('clear')` (death_start) |
| | 30 / 82 / 85-110 / 100-118 / 120 | body | `snd('d_droop')` + `snd('d_face_fade')`; `fx('water_splash')` + `snd('d_splash')`; `snd('d_leaves')` at 85 / 100 / 110; `fx('leaf_dissolve')` every 6 t + `snd('d_sink')` at 100; `snd('d_seed')` |
| **arena** | every 10 t | centre | `fx('haze_withered')` (phase 1, T1, phase 2), `fx('haze_lush')` (phase 3) |

The wedge counts and angles come from the rig manifest: with the stub's schedules a swing sweeps 200° in 8 ticks
(25° per tick); the real `yaw` and `tracks` set them at AP-RC1.

Per-moment budget targets (AP-FX measures them in §11): P3 slam + carpet ≤ 48 fx / ≤ 12 telegraph cards; P5 / Q4 swing
≤ 16 telegraph cards (8 wedges × 2); Q5 volleys A + B ≤ 30 fx / ≤ 26 telegraph cards; Q2 blast ≤ 40 fx + the flood pool
+ the wash and 3 rims (≤ 8 telegraph cards); phase 2 at the organism cap ≤ 40 fx / ≤ 30 telegraph cards with the dressing
pool full.

### 0.12 Hook lines for the core (wired at AP-I1, plan §10)

| module hook / event | kit calls |
|---|---|
| `uninstall` | `fx/uninstall` |
| `cleanup`, fight end, abort | `fx/clear` + `fx/hud/clear` + `fx/dress/clear` |
| `pause` | `fx/tele/clear` + `fx/hud/flash_end` + `fx/hud/banner_end` (a running Q2 is cancelled on pause, plan §7.2) |
| `resume` | nothing (the dressing pool stays; patterns that restart redraw their own decals) |
| `reload` in phase 2 | `fx/dress/redraw` (cards die with every `rlk_mb_aux` in `init`) |
| `death_start` | `fx/tele/clear` + `fx/hud/clear` |
| a cancelled pattern | `fx/tele/clear` is the core's; a pattern ends its own waves / rings / rims (`wave_end`, `mring_end`, `safe_end`) |
| boss-bar lines | the core composes `extra[]` / `sub[]` from `K.glyph()` / `K.badge()` |

No `rlk:tick` / `rlk:load` hook: cards are aged by `fx/e/world` (a `1t` schedule chain started by the first card, with
the fg first-tick fix).

### 0.13 Differences from the fg kit and the Azhdaha kit (deliberate)

| item | fg kit | Azhdaha kit (fx.md) | Apep kit | why |
|---|---|---|---|---|
| sector half-angle | snaps to 30 / 45 / 60 / 90 | 7.5° steps | **any integer degree** | plan hazards use 78°, 27°, 24° and decal = hazard within the 0.3 b pad (a 7.5° step misses by up to 0.38 b at r 7.2). Fallback if AP-FX cannot draw it: the pattern authors snap the **hazard** to the kit step (78 → 75, 27 → 30, 24 → 22.5) by request |
| palettes | `el` 5 / 9 / 0 | `el` = `#elem` 0-5 (6-8 draw Geo) + `nd` 0/1/2 | `el` 7 + Apep styles 20 / 22 / 23 / 24; `nd` 0/1/2 kept | the phase-1 gold, the target ring, the olive disc and the field are not element colours |
| element families `…/<el>` | – | presets, props, banners, sounds 1..5 | none | one element (Dendro) for the whole fight |
| long-lived decals | – | field pool `tele/field`, `tele/strip` (16 cards) | dressing pool `fx/dress/*` (16) + flood pool (48) | the phase-2 dressing lasts ≈ 100 s and is not a hazard; the flood needs many tiles once |
| moving target ring | – | – | `tele/mring*` | Q3's lagging ring (not a hazard decal) |
| wall footprints | – | – | `tele/wall_spot` | 둥지 walls (no damage) |
| crack-line strips | – | – | `tele/crack` | P2's white-gold strip look |
| creature sounds | banned (mechanical boss) | – | allowed as plan §8 names them; none in D | Apep is a creature |
| title line | `hud/pop_*` glyph alone | `hud/cue_*`, flashes | `hud/title {g,t,c,s,hold}` carries the module's text with the glyph; `hud/whiteout {hold}` | the module's Korean titles and the kit glyphs share the title line; the CS white-out is 40 t |
| generic textures | painted by the kit | painted | referenced from the fg kit | plan §5.4 (≤ 0.35 M new px) |
| adopted from Azhdaha | stub rig + rig calls, `hud/put_extra` | no rig calls, no boss-bar lines, `tele/wedge` stacks, wave ids, safe rims, mask wash, blocks in Python | **as Azhdaha** | one convention for both chapter kits (a later shared engine, fg §13) |

## 1. What is built (AP-FX, 2026-10-19)

Stage AP-FX, worktree `S:ap/wt_fx` (branch `wip/ap-fx`, base RIGLIB `039b911` = M0 `99bc097` + the shared rig
libraries), resource-pack sandbox `S:ap/rp_fx` (a copy of the shipped `S:rp_final9`, which is never written). Every name
and argument of §0 is built as listed there; §0 is unchanged. Additions (no §0 name changed): `hud/heart_bar` (the FN-24
fallback, §9.3) and the Python helpers of §10.

| | count | where |
|---|---|---|
| generator, painters, manifest | 3 files | `tools/build_mboss_ap_fx.py` (≈ 3300 lines), `tools/mboss_ap_fx_paint.py` (stdlib painters), `tools/mboss_ap_fx_manifest.json` (written on every run) |
| functions | 383 | `AP:fx/**` (`e` 12, `tele` 44, `dress` 15, `p` 116 = 95 presets + their macro workers, `snd` 121, `hud` 11, `prop` 12, `test` 47, entry points 5) |
| presets / sounds / props | 95 / 121 / 11 | §6 / §8 / §7 |
| sprite kinds | 91 = 37 own + 40 telegraph pieces (all own) + 13 fg-kit references + 1 alias | §5 |
| new atlas pixels | **0.262 M** (own 37 kinds 0.176 M + pieces 0.086 M) | budget 0.35 M (plan §5.4); the fg references add none |
| HUD glyphs | 21 + 3 spaces in `rlk:mboss_ap` (U+E900-E9F2) | §9 |

Build (datapack, then the pack; both idempotent, §12):

```
cd <worktree>/roguelike
python3 tools/build_mboss_ap_fx.py --resourcepack <unpacked pack>     # datapack + pack (needs the fg kit's sprites built)
python3 tools/build_mboss_ap_fx.py --skip-rp                          # datapack only
```

The generator owns exactly `AP:fx/{e,p,tele,dress,snd,hud,prop,test}/**` and `AP:fx/{card,cardx,look,clear,uninstall}`
(manifest `owned`): a stale file in an owned folder is removed, every other path under `AP:` is left alone (checked by
`run_kit.sh` step `own`). It writes no file on import (`import build_mboss_ap_fx as K`).

## 2. Engine

The fg kit's card engine with its own prefixes (§0.1): `fx/card` / `fx/cardx` → storage `rlk:apkit a` → `fx/e/make`
→ `fx/e/spawn` (one `summon` with the three stage snapshots in the item's `custom_data`: `wkS` start scale, `wkG` the
end transformation with `interpolation_duration` = dur, `wkF` scale 0 over `fade`; `wkC` the hit colour) → `fx/e/born`
(stage clock = gametime + 1, the fg first-tick fix: the ager runs at the end of the server tick that made the card, so
the main interpolation starts in the next server tick and the client animates it). Stages per card: shows at clock +
dly, interpolates from clock + dly + 1 over dur, recolours (`colors[0]` ← `wkC`) at clock + hit, shrinks over the last
`fade` ticks, removed at clock + dly + life. `fx/e/world` is a `1t` self-scheduled ager (no `rlk:tick` hook): it clears
the fx / telegraph / flood cards when the player is dead or reviving (`dead=1`, `rnDie≥1`), ages every card but the
dressing pool, pulses the dressing pool, recounts the pools and stops when no card is left (`e/zero`).

| pool | tag | counter | cap | rule |
|---|---|---|---|---|
| fx cards | `rlk_wk` (not `_t`, `_d`, `_fl`) | `#wkN` | **64** | `card` / `cardx` return when 64 are live (per card: a preset is cut, never refused) |
| ambient presets | – | `#wkN` | **40** | the 9 *amb* presets (§6) return whole from 40 live fx cards |
| attack telegraphs | `rlk_wk_t` | `#wkTN` | **40** | every `tele/*` shape returns from 34 live (`TCAP − 6`) **and** when its own card count would pass 40 (`#wkTq`): a shape is drawn whole or not at all |
| dressing | `rlk_wk_d` | `#wkDN` | **16** | never aged; swirl 2 cards, ley `n` strips (≤ 8) |
| flood | `rlk_wk_fl` | `#wkFN` | **48** | `p/flood` only (44 cells) |

Objectives `wkS wkG wkH wkK wkD` (the card's stage ticks), fake players `#wk*` on `mb` (`#wkInit`, `#wkNow`, the
counters, `#wkMinus1` and the scratch values; `fx/e/init` sets the constants and is called by every entry that needs
them, including `dress/swirl`, `dress/ley` and `tele/e/prep`). Storage `rlk:apkit`: `a` (the card being made), `t`
(telegraph arguments and palette), `pa` / `pf` (preset worker arguments), `dress` (the dressing pool's arguments for
`dress/redraw`), `hud` (`g`, `gc`, `ban`, `hbar`).

**Tenths.** Telegraph, dressing and preset size arguments are tenths of a block (§0.2). A preset with arguments is a
public macro `p/<name>` that turns the tenths into block floats in `rlk:apkit pa` (`execute store result storage ...
float 0.1`, scaled per argument) and calls its worker `p/e/<name> with storage rlk:apkit pa`; the Python builders take
blocks (`K.fx('wheel_carpet', r0=3.0, r1=14.4, dur=14)` writes `{r0:30,r1:144,dur:14}`).

## 3. Telegraphs

### 3.1 Palettes and layers

| `el` | rim (col1) | fill (col2) | flash (col3) | use |
|---|---|---|---|---|
| 7 Dendro (default) | `#4E8A1E` | `#A6D45A` | `#F1FFD2` | phase 3, organisms |
| 20 gold | `#B07A1E` | `#EBC55A` | `#FFF4C8` | phase-1 telegraphs on the withered field |
| 22 target | `#6FA85A` | `#C1E6A8` | `#F5FFF0` | Q3 ring |
| 23 olive | `#FCF9ED` | `#B9B46A` | `#FFFFF4` | P4 disc |
| 24 field | `#9DBA2E` | `#DCEB72` | `#FFFFD8` | Q2 wash, flood |

`nd ≥ 1` turns the rim (and the edge bars) `#C36E5A`; `nd 2` adds the `t_jump` chevron (one card). The safe rim draws
dim `#B9C9A8` until its dome forms (call + tell), then white; wall spots `#C6CDB0`. Heights above the floor top:
wash / dressing +0.03, fills +0.035, rims and pieces +0.045, inner rims and bars +0.046, wave rings +0.048 / +0.05.

Every damaging shape follows the pairing rule (§0.2): `tele/e/prep` sets life = tell + hold + 1, the fill grows over
tell − 1 ticks from the tick after the call, so its edge reaches the rim on call + tell, where every card of the shape
flashes (col3) and stays `hold` ticks (default 3). Checked for each shape in `test_ap_fx.py` §2-§7.

### 3.2 Sectors and wedges: any integer degree

A shape of full angle F (sector: 2a, wedge: a1 − a0) and radius r is a fan of **n equal pieces**, n = ⌈F / M⌉ with M =
32° (r > 3.5 b) or 64° (r ≤ 3.5 b). Each piece is one card of the family width W ∈ {2, 4, 8, 16, 22, 27, 32, 40, 48, 56,
64}° — the smallest W ≥ P with P = F / n — squeezed across by k = tan(P/2) / tan(W/2) (the card's x scale k·r, z scale
r), so its painted edges land exactly P apart. k is linear in P inside each family band, `k ≈ (A + B·P) / 10⁶` (P in
tenths), with k(W) = 1 exactly (manifest `pieces.k`; worst error 0.02 %), computed in `tele/e/kw<W>` from scoreboard
integers. Piece i sits at bearing a0 + F (2i + 1) / (2n) (tenths, integer division: every edge within 0.1° of the
requested angle; the tests allow 0.2°). Because k ≤ 1 the squeezed arc dips **inward** between the piece edges and
never passes r: at most 1.2 % of r for r > 3.5 (≤ 0.13 b at r 11.4) and 3.9 % for r ≤ 3.5 (≤ 0.14 b).

| card | kind | when |
|---|---|---|
| fill piece | `t_pf<W>` (grows from 0.01 b, or from r0 for an annular wedge) | every piece |
| rim piece | `t_pa<W>` (W ≤ 32; r > 3.5), `t_pas<W>` (thick, r ≤ 3.5), `t_pe<W>` (thick with its two radial edges painted just inside, a one-piece sector at r ≤ 3.5) | every piece |
| inner rim piece | `t_pa<W>` / `t_pas<W>` at r0 | annular wedges (r0 ≥ 1 b) |
| edge bars | `t_bar` 0.24 b wide at ±a, offset 0.12 b inward | sectors of n ≥ 2 or r > 3.5 |

Card counts (`K.sector_cards(r, a)`): sector 2n + 2, or **2** for a one-piece sector at r ≤ 3.5, or 2 for a ≥ 175 (the
disc); wedge 2n (3n annular). The §8 calls: P6 hit 1 (a 78, r 7.2) **12**; O1 cone (27°, r 3.1) **2**; O6b bite (24°,
r 2.6) **2**; a P5 / Q4 swept wedge (25°) **2**, a whole swing 16. `K.piece_geometry(F, r, a0)` returns the pieces
[(bearing, W, k)] exactly as the functions draw them (the renderer and the tests use it). Render:
`S:ap/fxrender/ap_tele_sectors.png` (every panel with the exact hazard outline), `ap_tele_wedges.png`.

Swept wedges (`tele/wedge`): the host stacks one per swept tick at the lane start (`api.wedges()`, §0.4), each with tell =
its swept tick − the stack tick, so the stack fills together and flashes tick by tick along the sweep (a travelling flash;
`ap_tele_wedges.png` t14 / t17 / t21).

### 3.3 The other shapes

| shape | cards | look |
|---|---|---|
| `tele/disc` | 2 (`t_fill` + `t_rim`; +1 `t_jump` with nd 2) | the fg disc in the `el` palette |
| `tele/line` | 5 (`t_lane` + 4 `t_bar`: two rails, two caps; +1 nd 2) | the fill grows toward the far end, its bright edge reaches it on the hit |
| `tele/crack` | 6 (the line's 5 + one `t_crack` strip) | white-gold crack line, gold palette fixed |
| `tele/wave` | 4 (disc 2 + front and band rings `t_ring` tagged `rlk_wk_wv<id>`) | the disc fills to r0 over tell, then the ring pair travels r0 → r1 in dur ticks (`teleport_duration`-free: scale interpolation); the disc goes after its hold, the rings after the travel; `wave_end {id}` kills them |
| `tele/mask_wash` | 1 (`t_wash`, r) | the field look (el 24) for tell + hold + 1 |
| `tele/safe_rim` | 2 (`t_safe` + the `t_dome` glyph, tag `rlk_wk_sr<id>`) | dim → bright at call + tell, lives tell + hold + 1; `safe_end {id}` |
| `tele/mring` | 2 (`t_target` + `t_rim`, tag `rlk_wk_mr<id>`, `teleport_duration:2`) | no fill timing; `mring_move {id,t}` sets `teleport_duration` t and moves both; `mring_end {id}` |
| `tele/wall_spot` | 1 (`t_wall`) | 1.4 × 0.5 b, pale yellow-green, rotated with the executor |

`tele/clear` removes every `rlk_wk_t` card (attack shapes, waves, rims, rings, wall spots, the wash); `fx/clear` also the
fx and flood cards; neither touches the dressing pool.

## 4. Dressing pool and flood pool

- `dress/swirl {r}`: the `d_swirl` ring (r blocks) + a soft gold `glow` under it (1.3 r);
  `dress/ley {n}`: n `d_ley` strips (n clamped 6-8) from r 1.8 to r 14 on the absolute bearings 12, 58, 104, 152, 197,
  243, 290, 333 (the first n), their width
  breathing over 20 t (`dress/e/pulse`, run by the ager). Both store their arguments in `rlk:apkit dress`, so
  `dress/redraw` (after `/reload`) rebuilds the pool; `dress/clear` empties it. Pool cap 16 (swirl 2 + ley ≤ 8 = 10).
  Render `ap_dress_flood.png`.
- `p/flood {life}`: 44 yellow `fl_tile` cards on a 7.5 b grid over the walk disc (cell centres within 26.6 b), each
  skipped when a live `rlk_mb_ap_dome` marker is within 7.5 b of the cell centre (the dome interiors stay clear), plus a
  flash; tiles live `life` ticks (min 6). Pool cap 48.

## 5. Sprites

### 5.1 Own kinds (37)

Each is `assets/rlk/textures/mboss/ap_kit/<kind>.png` + a model + an item definition with a `custom_model_data` tint
(default white).

| kind | plane | px | tint | look |
|---|---|---|---|---|
| `leaf` | face | 32×32 | neutral | leaf (tint pale green, black `#2A2A10`, gold) |
| `leaf_blade` | face | 32×64 | neutral | glowing leaf blade (rosette petals, sweep / skim blades, spikes) |
| `blade` | face | 32×64 | neutral | faceted crystal blade (white-gold burst blades) |
| `pool` | flat | 64×64 | painted | dark olive leaf pool (burrow) |
| `pad` | flat | 64×64 | painted | translucent green leaf pad (underground trail) |
| `mound` | face | 64×32 | painted | lime leaf mound with white spray, foot at b 0 |
| `root_chunk` | face | 32×32 | painted | brown root chunk with gold glints |
| `thorn_wheel` | face | 96×96 | painted | pale-green carpet thorn wheel |
| `thorn_wheel_homing` | face | 96×96 | painted | **gold-orange (`#F7C25E` / `#E8902A`) homing wheel with the red (`#E23A2A`) 4-point flare** |
| `seed_bolt` | face | 32×32 | painted | lime seed bolt (O2) |
| `seed_orb` | face | 64×64 | painted | yellow-green orb with a spiral glyph (Q5) |
| `charge_ball` | face | 64×64 | painted | Q3 light ball (`#FDFBBD` core, white-green halo) |
| `beam` | cross | 32×128 | neutral | light column, foot at b 0, 1 b tall at scale 1 |
| `dome_flare` | face | 64×32 | neutral | half-dome flare, pivot at the base |
| `crescent` | face | 128×32 | neutral | crescent trail segment |
| `rib` | face | 64×64 | painted | pale rib afterimage (P1 sweep) |
| `spiral` | face | 64×64 | neutral | spiral wisp |
| `splash` | face | 64×64 | neutral | water splash crown, foot at b 0 |
| `shard` | face | 32×64 | neutral | glass shard (dome pop) |
| `wisp` | face | 32×64 | painted | black twisted wisp (수호 death) |
| `lightning` | face | 32×128 | neutral | lightning ribbon, root at b 0 |
| `water_sheet` | flat | 128×128 | painted | lake water tile (1 b at scale 1; the records use 14) |
| `lily_pad` | flat | 64×64 | painted | lily pad |
| `bell_flower`, `bulb_flower` | cross | 32×64 | painted | pond flowers, foot at b 0 |
| `bank_crystal`, `gate_crystal` | cross | 64×128 | painted | gold crystal spikes / gold-green gate crystal (1.5 b) |
| `t_jump` | flat | 32×32 | neutral | jump chevron (nd 2) |
| `t_crack` | flat | 32×128 | painted | P2 white-gold crack line (`#FFFBE0` / `#F2D27A`) |
| `t_wash` | flat | 96×96 | neutral | 종말의 여파 field wash |
| `t_safe` | flat | 128×128 | painted | dome footprint rim with leaf sprigs (`#E4F69D` / `#F8FFE2`) |
| `t_dome` | flat | 48×48 | painted | dome glyph decal |
| `t_target` | flat | 64×64 | neutral | Q3 target disc |
| `t_wall` | flat | 64×32 | painted | 둥지 blade footprint |
| `d_swirl` | flat | 128×128 | painted | the Heart's gold swirl ring |
| `d_ley` | flat | 32×128 | painted | 지맥 이상 ley-line strip |
| `fl_tile` | flat | 32×32 | painted | flood tile (`#DFEA59` / `#E8E63E` / `#FBFAA4`, seamless) |

The Dendro palettes are painted in two registers: the **withered** phase-1 look (olive / gold / white-gold: `pool`,
`root_chunk`, `rib`, `t_crack`, `d_swirl`, `d_ley`, the gold `el 20` telegraphs) and the **lush** phase-3 look (lime /
yellow-green / pale mint: `mound`, `pad`, `seed_orb`, `splash`, `t_safe`, `fl_tile`, `water_sheet`, `lily_pad`, the
Dendro `el 7` telegraphs). Neutral kinds take their colour from the tint (presets pass the palette values above).

### 5.2 Telegraph pieces (40 own kinds)

`t_pf<W>` for every W (11), `t_pa<W>` for W ≤ 32 (7), `t_pas<W>` and `t_pe<W>` for every W (11 + 11); each a W-degree
slice painted with the fg kit's telegraph bands (fill gradient, rim band, inner line) so a squeezed piece reads like
the fg sector; heights 64 px (fills, edged pieces) / 32-48 px (rims). 0.086 M px in all.

### 5.3 fg kit references (no new pixels)

`glow glint mote streak ripple spark smoke t_rim t_rim_s t_ring t_fill t_bar t_lane` point at `rlk:mboss/fg_kit/*`; the
alias `thorn_wheel_x` = `thorn_wheel` on a cross plane. The generator refuses to write the pack unless every referenced
fg sprite exists with the size the fg kit declares and is in the item atlas (`check_refs`), so the kit needs the fg
kit's pack first (as in `rp_final9`); `run_kit.sh` step `rp_scope` checks that against the shipped pack only the kit's
folders, its font and its 77 atlas entries differ.

## 6. Presets (95)

Card counts per call are in the manifest (`presets.<name>.cards`, the flood's in `pool_cards`); the heaviest:
`flood` 44 (pool), `wheel_carpet` 18, `leap_slam` 17, `sweep_ring` 13, `slam_burst` / `pred_burst` / `ember_arc` /
`blade_burst` 12, `revival_burst` 11, `rosette` / `gold_burst` 10. Every preset's cards expire (tested).

- **Ambient** (*amb*, return whole from 40 live fx cards): `gold_embers shadow_glide gold_motes gold_drip leaf_pad
  floor_glitter spores haze_withered haze_lush`.
- **Particles only** (*ptcl*, 0 cards): `shadow_glide homing_trail comet_trail tether helix_trail haze_withered haze_lush`.
- **Arguments** (tenths): `burrow_pool gold_glow blade_burst spin_ring sweep_ring {r}`, `slash_band spine_afterimage
  tether light_band leaf_skim {len}`, `ember_arc {len,h}`, `wheel_carpet field_ring {r0,r1,dur}`, `arc_trail
  crescent_trail {r,a,dir}`, `arm_sweep {r,a}`, `flood {life}`, `beam_column {w}`, `shell_streak {h}`.
- `wheel_carpet`: 18 crossed pale-green wheels (`thorn_wheel_x`) around the slam point that ride r0 → r1 in `dur`
  ticks; called at strike − 1 they start travelling on the same tick as the `tele/wave` front of the same slam
  (tested).
- `arc_trail` / `crescent_trail` / `arm_sweep`: 7 (5 for the arm) segments on the arc of radius r over ±a about the
  executor's yaw, revealed in order in `dir` (+1 clockwise), each fading behind the head; the tail root is the executor.
- `homing_trail` spins the executing display a quarter turn per call (`prop/e/spin`, as `@s` when it is an
  item_display; nothing when it is not) and leaves gold-orange dust: run it every 2 t as the module's homing wheel.
- `ember_arc {len,h}`: the 「불씨」 ember (CS t64-76): 12 sparks shown one after another on a parabola `len` long and
  `h` high, from the bank twig (the executor, rotated toward the egg; pitch counts) into the egg.
- The generic `spark` and `flash` (tells, clicks, bright moments) are 1-card billboards.

Render: `ap_presets_1.png`, `ap_presets_2.png` (every preset at a characteristic tick, alternating floors).

## 7. Props (11)

As §0.7. Each `prop/<name>` is one `data merge entity @s` (item model, tint, billboard, brightness 15, view range 2,
the transformation; `teleport_duration` is the module's). `thorn_wheel_homing` is Ø 2.05 camera-facing; the module runs
`p/homing_trail` on it every 2 t, which also spins it (four quarter-turn quaternions, `SPIN_Q`). Render: the homing
wheels in `ap_vs_footage_p1.png` (row 4), every prop sprite in `ap_sprites_*.png`.

## 8. Sounds (121 recipes, 263 layers)

Every §0.8 name, each a fixed list of vanilla `playsound … hostile @a[tag=player] ~ ~ ~ <vol> <pitch> <minVolume>`
lines (`mboss_lib.min_volume`; manifest `sounds.<name>.layers`); a ×N layer is N copies at pitch +0, +0.07, −0.06,
+0.12, −0.11 (clamped 0.5-2); at most 10 layers per recipe.
The death recipes (`d_*`) use no creature voice (tested against the voice-event list); `heart_gain` picks its chime
pitch from `#apHt mb` in 11 steps (`floor(#apHt / 1000)`, a semitone apart, ending an octave up at 10000), so the
chime rises with the Heart; the core keeps `#apHt` current. The call list's sound names equal `K.SOUNDS` (tested).

## 9. HUD

### 9.1 Font `rlk:mboss_ap`

| glyph | cp | px (h, ascent) | use |
|---|---|---|---|
| `apep` | E900 | 36² (9, 8) | Apep badge |
| `guard nest nurt pred destr` | E901-E905 | 24² (7, 7) | ◆ badges (tinted by the text colour) |
| `warn`, `fail_s` | E906, E907 | 36² (9, 8) | ⚠, the small withered-Heart failure mark |
| `t_heart t_warn t_fail t_success` | E910-E913 | 48² (12, 10) | title glyphs |
| `dome` | E914 | 36² (9, 8) | the banner's dome glyph |
| `fl_white fl_white9 fl_green fl_edge` | E920-E923 | (144, 69) | full-screen flats: white 1.0, white 0.9, green `#B6E35A` 0.5, edge vignette |
| `bar0 bar1 bar_l bar_r` | E930-E933 | 4×8 (8, 7) | Heart bar cells: dim, gold, caps |
| spaces | E9F0-E9F2 | – | −1 / +2 / +1 |

The generator checks every codepoint against all `assets/*/font/*.json` of the pack (`hud minimap bossbar mboss_gd
mboss_bf mboss_fg mboss_az`) and refuses to write on a collision.

### 9.2 Functions

As §0.9. `hud/title` composes `[<glyph component from storage hud.gc>, {text:t, color:c, bold}]` with `times 6 hold 12`
and sets `vBig` (hold + 18) so the F5 crosshair title rests meanwhile. `hud/banner_aftermath` sends the actionbar line

> `[dome glyph] ` **소생의 찬가 보호막** (`#C36E5A`, bold) ` 안으로 들어가서 종말의 여파를 막아내세요` (white)

every 20 t (`hud/e/banner_tick`, a schedule chain) holding the regular actionbar HUD (`hudHold 30`) until
`hud/banner_end` / `hud/clear`. `hud/whiteout {hold}` = `fl_white` on the title line, `times 4 hold 8` (no Blindness,
no FOV change); `flash_white` (`fl_white9`, 0 2 4), `flash_green` (1 3 4), `flash_hit` (`fl_edge`, 0 1 2);
`flash_end` drops any overlay at once. Render: `ap_hud.png`.

### 9.3 Heart bar fallback (FN-24) and badges

The Heart progress bar is the core's bossui line (`#buHpCol` / `#buNoNum`, §0.9). If FN-24 lands without those options,
the kit's fallback is ready: **`hud/heart_bar`** (no args) writes `rlk:apkit hud.hbar` = a text component of 20 cells
(gold `bar1` up to `#apHt / 500`, dim `bar0` after, caps) from `#apHt mb` (0..10000); the core appends
`{nbt:"hud.hbar",storage:"rlk:apkit",interpret:true}` to its line. `K.heart_bar(v)` returns the same string in Python.
`K.badge(kind, on)` gives the ◆ + name component (dim `#707070` off, the kind colour on: 수호 `#F2D45C`, 둥지 `#C9E07A`,
양육 `#D4E784`, 포식성 `#E07A5A`, 파괴 `#F0A040`; `fail` = the `fail_s` mark in `#C36E5A`).

## 10. Python API additions (beyond §0.10)

```python
K.piece_geometry(f_deg, r=7.2, a0=0.0)   # [(bearing deg, W, k)]: the fan exactly as tele/sector|wedge draw it (§3.2)
K.sector_cards(r, a)                     # attack-telegraph cards of one tele/sector call
K.heart_bar(v, vmax=10000)               # the FN-24 fallback bar string (§9.3)
K.flood_cells()                          # the 44 flood cell centres (blocks from the arena centre)
K.kind_info(kind)                        # (plane, px, extent, neutral, texture id, description) of any kind
K.PIECES, K.PIECE_MAX, K.PIECE_MAX_SMALL, K.SMALL_R, K.TSKIP, K.DOME_TAG, K.DOME_SKIP, K.BADGES, K.TITLE_G
K.DEMOS, K.DEMO_LEN, K.TEST_ARGS, K.test_call(name)   # the demo timelines and the preset test calls
```

## 11. Measured budgets

`test_ap_fx.py` §15 plays every demo (§0.11 call index at its ticks around the stand-in) and records the per-tick peak
of live cards; the phase-2 load is a synthetic 200 t timeline at the organism cap.

| moment | fx cards | telegraph cards | target (§0.11) |
|---|---|---|---|
| P3 slam + carpet (`glow`) | 45 | 12 | ≤ 48 / ≤ 12 |
| P5 swing (`tail`) | 9 | **16 per swing**; 18 for one tick (t39: swing 1's last wedge in its 3 t hold as swing 2 stacks) | ≤ 16 |
| Q4 swing (`tail_p3`) | 11 | 16 | ≤ 16 |
| Q5 volleys A + B (`spiral`) | 20 | **24** (the 12 landing discs); 34 for two ticks (t53-54) with the two leaf-blade lanes of t52 | ≤ 30 / ≤ 26 |
| Q2 blast (`aftermath`) | 33 | 7 (wash + 3 rims) | ≤ 40 / ≤ 8, + the flood pool (34 cells drawn with 3 domes) |
| phase 2 at the organism cap (6 organisms, 3 attack slots + a bite chain + a fuse, motes, haze, full dressing pool) | 25 | 17 | ≤ 40 / ≤ 30 |
| other demos (max) | 31 (`move_strike`) | 24 (`hands`: 4 crack strips) | caps 64 / 40 |

Notes: the P5 one-tick overlap and the Q5 lanes stay below the caps (40; telegraph calls are skipped from 34 live, so a
further telegraph during t53-54 of Q5 would be skipped: `S:ap/requests/fx.md`).

## 12. Verification

`S:ap/fxtests/run_kit.sh <worktree>/roguelike [tag]` (`RP=<pack>` adds the pack checks), all green at the final commit:

| step | result |
|---|---|
| `test_ap_fx` (mcsim, 17 sections) | **3860 checks OK** (3575 without RP) |
| `test_fg_fx` (the fg kit's suite, unchanged) | 1185 checks OK |
| `idem` | datapack and pack unchanged by a rebuild; no file outside the kit's paths changed; fg kit sources / outputs byte-identical to `039b911` |
| `own` | a stray file in `fx/p/` is removed, stray core files under `AP:` survive, the scratch rebuild equals the tree |
| `rp_scope` | against `rp_final9`: only `ap_kit` folders, `mboss_ap` font and 77 atlas entries differ |
| validators | refs 27 / macro 2607 / lint 3758 findings, **0 new** vs the M0 baselines + the kit's accepted list; nbt 0 invalid; `check_mboss_pack` 0 problems |

`test_ap_fx.py` sections: 1 engine (stage clock, first-tick fix, offsets, cardx stages), 2 disc / palettes / nd, 3 sectors
(14 half-angles × 4 radii: pieces tile the angle within 0.2°, arcs within r, dips ≤ 0.15 b, rim kinds, bars, counts =
`K.sector_cards`), 4 wedges (stacked swing, flash per swept tick, annular, 180°), 5 line / crack, 6 waves (front synced
to the hazard), 7 wash / safe rims / mring / wall spot, 8 caps and clears, 9 dressing pool, 10 flood (dome cells
skipped), 11 every preset (cards = manifest, expiry, ambient soft cap, carpet geometry, arc order, particles), 12 every
sound (call-list equality, layers, pitch, minVolume, no voices in D, the Heart chime), 13 HUD (title, banner red phrase
and refresh, white-out, flashes, heart bar, badges, font), 14 props + homing spin, 15 every demo + budgets, 16 uninstall,
ownership, Python API (tenths, name asserts, call-list equality), 17 the pack (sprites, models, items, atlas, fg
references, the 0.35 M budget, font and codepoint check).

Accepted validator findings (`kit_baseline.py` classifies them; any other new finding fails): macro 40 — `<target>
needs [...] but called without args` on `function <target> with storage rlk:apkit <path>` lines (the checker does not
follow `with storage`; every such call runs in `test_ap_fx.py`); lint 15 — `unknown command 'time'` (`time query
gametime`: the stage clock, the spin and trail phases), `execute without run` on `execute store result score … if
entity …` lines, and the two `e/spawn` macro shapes read with placeholders. The same classes the fg and Azhdaha kits
accept.

M0 suites: `S:ap/fxtests/m0/run_all.sh` = the M0 harness (`S:mb3/tests`) with the kit's accepted findings added to its
validator baselines, the kit suite as a step and `ident.py` reading its base from the tree's repository (the S1-FX
copy's patch: `mb3/wt_core` is gone). Run on the final tree with `RP=S:ap/rp_fx`: **ALL GREEN** (1059 s) — the fieldgen,
cruise, field, framework-option, butterfly (+ e2e, pjx, human, bf fx engine), fg kit, Apep kit, Guardian / framework
suites (guardian, e2e, p12, p34, p56, life, hz, mv, pj, roll, box), `gen_check` (generator order and idempotency incl.
both kits' pack builds), `ident` (Guardian, proto, butterfly, fieldgen byte-identical to M0 99bc097; vs 039b911 only
the kit's 386 own paths differ) and the five validators (0 new findings).

## 13. Renders (`S:ap/fxrender/`, `render_ap.py <worktree> <pack> <out> [sprites|tele|presets|demos|footage|hud]`)

The renderer runs the kit's own functions in the test's mcsim harness and ray-casts the item_display cards it leaves
(summon SNBT, tp rotation, stage merges with their interpolation, the hit recolour, prop merges), plus the recorded
particles as dots, on two procedural floors (withered moss, lush shallow water).

| file | shows |
|---|---|
| `ap_sprites_withered.png`, `ap_sprites_lush.png` | every fx sprite / prop kind on both floors |
| `ap_tele_palettes.png` | the disc in every palette and nd at fill and hit, both floors |
| `ap_tele_sectors.png` | 12 sectors (1° … 175°, r 2.6 … 11.4) at the hit with the exact hazard outline |
| `ap_tele_wedges.png` | P5 and Q4 swing stacks at t6 / t14 / t17 / t21, an annular wedge |
| `ap_tele_shapes.png` | lanes, crack strips, the P3 disc + travelling wave, Q2 wash and safe rim, Q3 ring, wall spot, O7 fuse, nd 2 |
| `ap_dress_flood.png` | the swirl + ley dressing (t2 / t10 / t30) and the Q2 flood with the dome cells skipped |
| `ap_presets_1.png`, `ap_presets_2.png` | all 95 presets |
| `ap_demos.png` | 16 demos at a key tick from behind the player |
| `ap_vs_footage_p1.png`, `ap_vs_footage_p3.png` | footage frames (`ref/v1_fx.jpg`, `ref/p3_fx.jpg`) next to the matching demo moments: P1 burst, P2 cracks, P3 carpet, P3 homing wheels; Q2 field, Q2 beam rain, Q4 crescents, Q5 helix / impacts |
| `ap_hud.png` | titles, the 종말의 여파 banner (with a 1:1 inset), white-out and flashes, the Heart bar fallback and badges |

## 14. Differences from §0 and open points

- Nothing in §0 changed. Additions: `hud/heart_bar` + `K.heart_bar` (§9.3), the helpers of §10.
- Wedge and sector pieces up to 64° only at r ≤ 3.5 b; above, 32° (the dip bound). A one-piece small sector paints its
  edges into the rim (`t_pe<W>`) instead of two bars.
- Footage comparison: the kit carries the floor and air effects; the big translucent Q2 domes, the boss body and the
  organism shells are the org / rig stages' models. The lush phase reads much brighter and greener in the footage than a
  vanilla floor: the `el 7` and field palettes were chosen to stay readable over the water sheet, not to match the
  footage's bloom.
- Requests and notes for other stages: `S:ap/requests/fx.md`.

## 15. 10-20 Telegraph rule (user, 2026-10-20) — pointer

`plan.md` §14 "10-20 Telegraph rule (user)": ground telegraphs only where the footage shows one. The kit stays as built;
§0.11's per-pattern calls drop `tele_disc` for P1 (the `shadow_glide` is the marker), P2's plunge, P3's slams, P6, Q1's slam
/ sweep, Q3 shells 2-3, Q5's landings, O6a, O7; `tele_line` for P1's sweep, Q5's blades, O2; `tele_wave` for P3's carpet;
the `tele_wedge` stacks of P5 / Q4; `tele_sector` for P6 hit 1, O1, O6b; `tele_wall_spot` for O4. Still called:
`tele_disc` (P4 with fill; Q1 / Q3 L1 / Q3s without the progress fill), `tele_crack` (without the `t_lane` fill),
`tele_mring*`, `mask_wash`, `safe_rim` / `safe_end`, the dressing pool, every preset and prop. Unused after the rule:
`tele/sector`, `tele/wedge` and the 40 slice pieces, `tele/line`, `tele/wave` / `wave_end`, `tele/wall_spot` + `t_wall`,
the `el 20` gold palette, `t_jump`. The one kit change the rule needs: a no-fill option on `tele/disc` and `tele/crack`
(to be filed in `S:ap/requests/fx.md`); O1 needs a small hit preset.

## 16. AP-I2 additions (2026-10-21; `wip/ap`)

Served at AP-I2 (requests/fx.md RI1-1, ap-p1.md RP1-5, ap-p3.md RP3-3 / RP3-6, ap-rev.md RREV-6); nothing of §0 renamed.

| function / preset | args | at | what | user |
|---|---|---|---|---|
| `tele/disc_o` | `tele/disc`'s `{r,tell,el,nd,hold}` | the floor point | the outline-only disc: the static rim alone (`t_rim` / `t_rim_s`), flashing on call + tell; 1 card (+1 with nd 2) | Q1's leaf ring, Q3 shell 1's held disc, Q3s's leaf ring and target disc (+ their resume redraws) |
| `tele/crack_o` | `tele/crack`'s `{len,w,back,tell,nd,hold}` | the stalk root, rotated along the strip | the outline-only crack strip: the two rails, the two caps and the white-gold crack line (`t_crack`) at full length, static, flashing on the hit; no `t_lane` fill; 5 cards | P2's strips (+ the resume macro `p/hands/crack`) |
| `p/o1_hit` | – | 1.6 b ahead of the basic, 0.6 b up | a small pale-green glint (life 4) + composter leaf bits + crit sparks | O1's strike (t10 of the lean) |
| `p/flood_part` | `{life, part}` | the floor centre | `p/flood` sliced: part 0 / 1 / 2 draws the cells i ≡ part (mod 3) of the flood grid (part 0 also the flash); the same dome skip | Q2 t156 / 157 / 158 with life 24 / 23 / 22 (the blast tick was 3.4 k commands) |

Python: `K.tele_disc(r, tell, el=7, nd=0, hold=3, fill=1)` and `K.tele_crack(length, w, tell, nd=0, hold=3, back=0.0,
fill=1)`: `fill=0` names the `_o` function with the same arguments. `K.fx('flood_part', life=24, part=0)`. The manifest's
`telegraphs` list carries `disc_o` / `crack_o`; `presets` 97. No new sprite: the atlas is unchanged by these (the kit's
77 sprites, 0.262 M new px). `TEST_ARGS` has `part: 0` (the kit's preset test calls).
