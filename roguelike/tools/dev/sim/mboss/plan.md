# Mid-boss (중간보스) + Corrupted Guardian (파수꾼・타락): binding decisions

Roots:
- `DP` = `/home/user/rlk/roguelike`. Generators are in `tools/`; the README is in Korean.
- `M` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/mboss`.
- Research:
  - `M/understand/{m1..m4,model,patterns}.md`;
  - `M/code/{nodes_rooms,boss_infra,elements_damage,integration}.md`;
  - sources in `M/src/` (videos m1-m4, `ref.png`, `guide.pdf`).
- Where these reports conflict, `patterns.md` §13-15 (critic) and this file win.

## User requirements (verbatim intent)
1. A new node "중간보스". It is offered together with other nodes (not alone like the tree root). Choosing it leads to a room where the mid-boss is fought.
2. The battlefield is circular. Square rooms make that hard, so use a separate circular arena and teleport there and back.
3. Several mid-bosses can exist. A random one is picked; there is a registry, and today it has one entry.
4. Killing it grants two item selections of the chapter-appropriate rarity.
5. The first mid-boss is Genshin's 파수꾼・타락:
   - appearance and patterns as in the videos;
   - modelled "as close as possible, with care";
   - mechanics per `guide.pdf`.
6. When the model is done, the user wants several photos (renders), so produce good renders (see R below).

## Framework decisions (from `integration.md`, accepted defaults unless changed here)
- **Node and zone:**
  - Node `k15` "중간보스", zone kind 15, weight 7.
  - Allowed from chapter 1, except the very first offer of chapter 1.
  - Not offered twice in the same chapter (the existing `seen` rule).
- **Gate:** zone 15 has a gate object (oact 14) at its centre. It shows the rolled boss name. A click starts the fight: `combat_start`, then about 1 s later the teleport to the arena.
- **Arena:**
  - Separate circular arena at overworld centre (200, 201, 8): radius 22 floor, walkable radius 21, wall and barrier cap.
  - Floor palette after m2 §2: white marble, rose curved bands, a central rose 4-point star, gold lamp posts.
  - Permanently forceloaded (`load` / `uninstall` / `room/remove`).
  - Built by `tools/build_mboss_arena.py`, with an `ensure` that rebuilds on version mismatch.
  - A light layer that keeps the floor bright enough to stop natural spawns.
- **Registry:**
  - `tools/mboss_registry.json`, generated into `rlk:mboss reg`.
  - Weighted random pick filtered by chapter range and not-yet-met-this-run, with a fallback.
  - `#mbForce` for tests.
  - Per-boss module `F:mboss/<id>/*`, plugged into generated numeric dispatchers `F:mboss/d/<hook>`.
- **Lifecycle:**
  - Return point = `rlk_safe`.
  - Spawn verification and retry; abort path with no reward.
  - Pause while the player is dead or reviving.
  - The out-of-bounds guard returns the player to the arena start.
  - Bossbar via the generic `bossui` with name line and aura glyphs.
  - Minimap hidden during the fight.
  - Death sequence keeps the clear held, then cleanup.
  - Back in the dungeon: gold absorbed, then **`lvup/add {n:2}` + `lvup/toggle`** gives two chapter-rarity picks (a separate counter suppresses character cards if easy; otherwise accept them).
- **Engine additions:**
  - generic per-mob resistance objective `mres`;
  - a hook in `combat/apply` that routes hits on mid-boss bodies and star objects to the module;
  - death hook (`mboss/death_start` instead of kill);
  - mid-boss hitbox HP and XP from the registry.
- **Damage tag:** treat the body like a boss for stun and freeze immunity, but not the 15× gold. Give a modest bonus: gold ×5 and 1 sapphire shard. Make it a registry field.
- **Raiden code is not modified.** Mid-boss code forks reusable ideas into its own namespace.
- **Performance:**
  - mid-boss rig at most about 30 display entities;
  - poses compiled per clip, but far smaller than Raiden's 32 MB;
  - cache part UUIDs or tags so per-tick scans stay cheap.

## Corrupted Guardian decisions (from `patterns.md` §15 K1-K26; accepted defaults, with these choices)
- **Look:** follow `model.md`.
  - BH = 3.0 blocks, idle hover 0.35 b, spear 4.35 b in the RIGHT hand.
  - One white wing and the gold winged pauldron/shield on her LEFT.
  - Faceless head: winged crest, red diamond, one eye. Gold halo and crown.
  - Thin dark voxel legs under the skirt; red/black floating cubes; red-black corrupted right arm.
- **Name:**
  - HP bar `파수꾼・타락`, subtitle `개안자 · 세계 망루의 파수꾼`.
  - Registry: `id "guardian"`, `n 1`, element Geo.
- **Rotation (K3):**
  - Entrance, then 3-4 normal patterns (range-filtered shuffle bag, no immediate repeat), then guard I and guard II back to back, then chaos.
  - Chaos ends in groggy or fail, then 4-5 normal patterns, then the next guard pair, and so on.
  - No HP phases.
- **Ranges (K2):**
  - melee ≤4: P3 and P1;
  - mid 4-8: P1, P2;
  - far ≥8: P4 (pull + two 360° swings) and P5 (fly-slam); P2 is also allowed far.
  - Melee patterns close in first.
- **Telegraphs (K4):** every damaging hit gets at least 12 ticks of readable telegraph. Lengthen where the source is shorter (P1, P2 line decals; fail decal ≥20 t).
  Superseded for ground decals by the **Telegraph rule (10-20)** below: the floor is a readable wind-up (10 t, 12 t for P1 thrust 2 and the entrance) from a motion + sound tell; a ground decal only where the footage has one.
- **Guard mode (K5, K6, K22, K24):**
  - 100 t, gold aura, drifts toward the player at about 1 b/s.
  - The record counts hits with element 1-4 on the body, one count per element per 8 t: 3 to record, 9 to re-record.
  - A record completes, then 20 t later the enchanted sweep fires.
  - Timeout, then 19 t later the gold sweep: 180-210° front arc, r 4.5-5.
  - Slot A = guard I result, slot B = guard II result; empty slots make inert stars (A gold, B blue).
  - Slots reset after each chaos.
  - The HUD shows the record progress (bossbar sub-line).
- **Chaos (K7-K12, C10, C11):**
  - Entry: leap and flight to the centre, landing, a 20 t charge, rise to about 3 b hover, then the 350 t timer and the stars.
  - Active stars are immune to their own element. Inert stars take ×0.238 damage (+80 % RES); the boss keeps base RES.
  - Star HP is sized so a typical character breaks both in about 10-12 s.
  - Breaking star 1 deals 6 % boss max HP; star 2 deals 18 % and starts groggy for 220 t (K13).
  - Timeout drops one fail spear per surviving star, at the locked player position: decal ≥20 t, cylinder r 2.5-3, spears 31 t apart, tinted by star colour.
  - Cube streams are ambient (no damage).
  - Stars sit 3-4 b apart and away from the body hitbox.
- **Pull (K14, K15):**
  - Undodgeable after a tell of at least 28 t (red aura and cube cage), needs line of sight, places the player 1 b in front of her facing her.
  - Then wind-up 5 t + hold 14 t, swing 1 (360°, r 5-6), 14 t gap, swing 2.
- **Javelin (K23):** line hazard locked at the beam, 1 b wide, at chest height, to the arena edge. The visual spear flies out and returns harmlessly.
- **Fly-slam (K26):** take-off to +8 b, ring locked at take-off +1 t, impact 20 t later, r 4.5.
- **Slam (K25):** disc r 5 centred 3.5 b in front of her, ring lead 17-18 t.
- **Knockback (K16):** P1 hit 2 and the enchanted sweep get stronger knockback.
- **Damage (K17):** coefficients P1 1.0/1.15, P2 1.3, P3 1.6, P4 1.2 ×2, P5 1.8, P6 gold 1.65 / enchanted 2.5 (+ that element), fail spear 2.2, entrance 1.0. All × the base mid-boss hit; balance against Raiden and the custom mobs.
- **Voice lines (K18):**
  - Typed subtitles with a soft sting, no audio voice: start "통찰하여, 나의 마음을 보아라.", attacks "처결하노라!" / "사라져라 마땅한 존재여!" (≥20 s cooldown), guard "기록하여 판결할 지어다.", groggy "나의 주인님이시여...!", death "시련은... 끝났다...".
- **Entrance (K19):**
  - She plants the spear from above.
  - A short ground telegraph (≥12 t) before the damaging plant, though the PDF says she appears without warning (a deliberate deviation for fairness). Superseded by the Telegraph rule (10-20): no ground marker (PDF p.73); the sky glint and the falling spear are the 18 t tell.
  - The start line plays at the plant.
- **Death (K20):** line, slump about 20 t, then a fly-away take-off with a cube trail and fade.
- **Screen FX (K21):** pull flash via a title font glyph or `darkness`; chaos crimson haze with particles at the rim.
- **Fx style:** gold Geo cards and particles (reuse the Navia `fx/nv` card engine idea through a boss-owned copy or a generalised engine), red/black cube motifs, element tints per `model.md` §4.
- **Sounds:** vanilla only, composed per the reports' audio notes.

- **Telegraph rule (10-20)** (binding, user 2026-10-20: "보스의 모든 공격에 바닥의 예고를 보여줄 필요는 없어. 영상에 없다면 그냥 보스의 동작을 보고 회피해야 하는 거니까 그대로 구현해줘"; audit `tele/gd/audit.md`, wip/tele-gd):
  - A hazard shows a pre-hit ground telegraph only when the reference footage shows one, shaped and timed like the footage. Every Guardian hazard is quiet (`#hzQuiet 1`: no framework outline, progress outline or strike flash).
  - Keep / trim (ground telegraph): **P3** slam (thin gold ring card, appearing at 40 % and reaching the rim in 5 t, + faint amber fill; m1 11.42-12.25 s), **P5** fly-slam (28 gold rim bars, translucent amber glow fill, gold 4-point star at the centre; no progress circle; m1 27.42-28.62 s), **fail spears** (red concave 4-point star decal with pink streaks; no damage ring; m4 1.55-4.55 s; the hit radius r 3.4 is shown at the impact by a flat ring of the star colour at 37 / 39).
  - Read from motion and sound (no ground telegraph): the entrance plant (sky glint 16 → spear falls 20-34), P1 thrust 1 (clip 0, streak 3, lock 11, glint 14 → 21) and thrust 2 (rise 31, glide 34-42, dive charge 39 → 46), P2 javelin (air glyph 10-19, lock 17, beam 20 → 27), P4 swings (clip 36, hold glint 41 → 51; 64), the gold sweep (chest sigil end − 4, wind-up, riptide 9 → 15) and the enchanted sweep (record starburst 0, enchant line 3 → 16). Mechanic markers stay: the P4 cage and screen effects.
  - No damage, size or timing change.

## R. Renders for the user
When the model is finished, produce a render set in `M/renders/`:
- front, back, left, right and three-quarter views;
- a spear close-up;
- the halo and wing details;
- a side-by-side with `ref.png`;
- the boss next to the 2-block player rig for scale.

PNG, about 1600 px wide, on a neutral background.

## User feedback on model draft 1 (binding)
- **"왼팔이 너무 각진데":** her LEFT arm (the gold arm under the shield and wing) reads as plain rectangular boxes. Rebuild it as a slender, tapered, armoured arm:
  - rounded shoulder and elbow caps;
  - a tapered upper arm and forearm, with painted sprite-card silhouettes and gold metallic gradients instead of flat boxes;
  - the orange inner-forearm glow seen in ref.png;
  - an elegant gold clawed hand with separate fingers.
- Check it from the shoulder-camera distance and close up, and keep the pose articulation intact.
- **"다리에 빨간색 큐브들이 원본은 불규칙적이고 너가 만든건 좌우대칭으로 너무 정갈해":** the leg and trail voxel cubes must be irregular. Mix sizes and tilts, place them asymmetrically with uneven gaps, thin them out toward the bottom, vary the colour, and avoid mirroring and lockstep motion. This is being fixed on wip/mb-model (legcubes workflow). Integration must take wip/mb-model's latest commit.
- **"별이 해당 원소에 면역은 아니고 내성이 있도록 하자. 40%정도"** (binding, replaces C11 immunity): an active element star is NOT immune to its own element. It takes that element's hits with **40 % resistance** (×0.6 damage through the mres curve, or the equivalent IMMUNE_PCT setting in tools/mboss_guardian/core.py). All other elements hit normally. Inert stars keep +80 % RES. Update the star sizing, the README and the in-game hint text (no "면역" wording), and make sure the "면역" popup no longer appears.
- **"중간보스 클리어하면 바로 아이템 선택으로 넘어가는게 아니라 바닥에 아이템 상자가 두 개 떨궈지도록 해. 그리고 발전과제 클리어 소리 없애"** (binding):
  - After the kill, back in the dungeon, do NOT open the selection screen.
  - Two item boxes (`cur.picks`) fall from the sky onto the floor at the 중간보스 zone centre, where the gate stood: a drop animation, particles and a landing thud. They sit side by side.
  - Each box is a clickable room object with a new oact. One click gives one chapter-rarity, items-only pick (`pkMb` +1, `lvup/add {n:1}`, then toggle) and removes only that box. (Superseded by the box fix below: the box stays, opened, until its pick is used.)
  - Labels: "아이템 상자" / "챕터 등급 아이템 선택".
  - Remove `ui.toast.challenge_complete` from `mboss/reward`. Keep the kill title, with the subtitle naming the boxes.
- [x] **"상자 열고 아이템 선택 창에서 SHIFT 눌러서 돌아오면 상자가 없어져있어"** (binding, bug fix on the released mid-boss build): the box was killed on the click, so backing out of the screen with Shift left no box.
  - A box disappears only when ITS pick is actually used (an item chosen).
  - Clicking a closed box adds its pick (`pkMb` +1, `lvup/add {n:1}`), marks the box opened (a tag and a visible change, label "(열림)") and opens the screen. Backing out leaves it.
  - Clicking an opened box only reopens the screen: no new pick, the same offer (no free reroll). Shift+F works too.
  - Whenever a mid-boss pick is consumed (`lvup/act/resolve` on an mbSet), exactly one opened box is removed, with the open/poof fx and sound moved there.
  - Two boxes: open A, back, open B, back → both opened, 2 picks; choosing twice removes both, one per choice; A again only reopens.
  - Map change with an opened box: the pick stays pending (Shift+F), the box goes with the room; unopened boxes are lost as before. No orphan counters, no `pkMb` drift. Drop animation, zone state, combat refusal and cleanup paths unchanged.
  - Done (wip/mbox-fix): `mboss/box/open` (generated; `rlk_mb_boxopen` on the whole group, `oarg` = open age, gold outline `Glowing` + `glow_color_override`, three-line label "아이템 상자 / (열림) / 다시 눌러 선택" so two labels 1.5 b apart never overlap), `mboss/box/spend` + `box/gone` (the oldest opened box, chest open + chime + gold burst + poof, `room/obj/kill_group`), hand-written `room/obj/do_mbox` (open / reopen; guard: an opened box with no `pkMb` left is removed without a pick) and one line in `lvup/act/resolve`. The offer is `rlk:lvpick choices`, kept by `lvup/exit` and rolled by `lvup/toggle` only when empty. State only on the box entities; invariant opened boxes ≤ `pkMb` ≤ `pkPending`. Tests: `mb/boxfix_tests/test_box.py` (real lvup screen code: back out, reopen, Shift+F, interleavings, map change, carried and level-up picks, guards) and `test_e2e_guardian.py` (boxes stay opened, one removed per used pick).
  - Verified (wip/mbox-fix): validators and all mid-boss suites green; the copy of `test_box.py` gained adversarial cases (twelve back-out/reopen cycles, reroll then back out and re-enter (offer and paid-reroll count kept), level-up and box picks mixed with the real draw and character cards forced on, skip and swap (including backing out of the swap step), the map view open on a click, a map change and a death while selecting, uninstall). Fix: the open sounds of `box/gone` played at the box, but a pick is only ever used in the selection screen, 40+ b from the room, so they were never heard; they now play at the player (the particles stay at the box).
- [x] **"중간보스 공격 선딜 좀 짧게 하고 공격 범위를 좀 늘려봐"** (binding, applied after the review-fix run):
  - Done (wip/mboss-tune): the rig clips play through `RETIME` (guardian_clips.mjs; strikes 1:1, wind-ups compressed,
    fx / sounds / tables mapped with `api.rt`, spear tables re-measured); wind-ups -22 to -25 % (P1 28 → 21 / 20 → 15,
    P2 36 → 27, P3 26 → 20, pull 32 → 24, swings tell 20 → 15, P5 41 → 31, sweeps 20/21 → 15/16, fail 49 → 37 with the
    schedule x0.75, entrance tell 24 → 18); areas x1.2 (P1 lanes 9.3 × 2.9 / 8.4 × 2.7, P2 1.2 b, P3 r 6, P4 r 6.8, P5 r
    5.5, sweeps r 6, fail r 3.4, entrance r 3.6) with decals and fx to match; P5 ring / fail disc kept inside r 21. Bands
    and P3 close-in unchanged (gd_contract §5, §12).
  - Shorten every damaging attack's wind-up (from the start of its tell to the damage tick) by about 25 %. Floor: 10 t of readable telegraph. The undodgeable pull keeps a tell of at least 20 t.
  - The guard-mode sweeps, chaos fail spears and entrance shorten in proportion.
  - Increase every hit area by about 20-25 %, with the telegraph decals and fx scaled to the new size exactly. Everything stays inside the walkable r21 arena.
    - P1 sweep arcs and reach;
    - P2 javelin width (about 1.25 b);
    - P3 slam disc r5 → r6;
    - P4 swings r5-6 → about r6.5-7;
    - P5 ring r4.5 → r5.5;
    - gold/enchanted sweeps r4.5-5 → about r5.5-6;
    - fail spear r2.8 → about r3.4.
  - Keep the per-hit damage coefficients unchanged.
  - Update the tests, README and gd_contract to the new numbers.
- [x] **P4 for melee players** (binding, follow-up to "끌어당기는 패턴이 안나오는데"): verification showed P4 never appears for a player who stays in melee range (0 of 127 stretches), and most characters are melee. Fix:
  - The once-per-stretch P4 guarantee (ai/pity) fires at ANY distance.
  - P4 may also be picked from the melee band at a low weight (about 1 vs 2 each for P1/P3).
  - When P4 starts with the player closer than about 5 b, she first backsteps/glides away to about 6-7 b (about 10-12 t, with a readable hop and a dust puff), so the cage tell and pull read clearly. Then the normal P4 runs.
  - Expected result in mcsim: P4 in nearly every stretch for held-at-3 b, hugging and in-and-out melee behaviour, as well as for ranged players.
  - Update test_guardian's "P4 never in melee" check, the README rotation section and gd_contract §5/§12.
  - Done (wip/mboss-tune): `ai/pity` at any distance, P4 in every band (melee weight 1 vs P1 / P3 2), the hop back
    (`ai/back`, 12 t to 6.5 b, rig clip `backstep`, sideways along the wall); p4freq: P4 in every stretch for held 3 b,
    melee 2.5 b, dodger / dodgerW, and still every stretch for held 6 / 10 / 15, strafe, kite, wander, still 10.
