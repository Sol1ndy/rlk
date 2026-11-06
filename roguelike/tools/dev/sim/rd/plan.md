# Raiden rework plan (마가츠 미타케 나루카미노 미코토): match the model and patterns to the footage v1-v9

Inputs: `rd/current.md` (audit of the current build at bcb3083), `rd/footage/{A,B}_catalog.md` + per-video logs,
`rd/frames/{A,B}/`, `rd/src/wiki.txt`. Paths: `S:` = scratchpad, `T:` = `roguelike/tools/`, `F:` = `data/rlk/function/`.
Time is in ticks (t), 20 t = 1 s. Sizes are in blocks (b). Arena: walkable radius **23** (outer 24, wall), centre
(0,201,0), blink/clamp radius 20-21 (current.md §1.1).
Ids `A-xx` / `B-xx` are footage catalog ids. Pattern ids (`rdPat`) keep their current meaning where a move maps; 5 and 15
must keep it, because the hand-written `combat/apply` gates on them.

Binding rules applied throughout:
- **R1, telegraph rule 10-20.** A floor decal appears only where the footage shows one, drawn like the footage
  (outline-like, sized to the hazard). Every other hit is quiet. The time from the first readable cue (motion or
  sound) to the hit is ≥ 12 t, or ≥ 20 t for undodgeable or large hits (area ≥ 100 b² or r ≥ 8). Every hit shows a
  visible impact effect covering its area.
- **R2, no tips.** No how-to advice on screen. Allowed: instant-kill warnings, messages the real game shows,
  pattern/form names, phase messages, numbers and the boss's voice lines.
- **R3, real 26.3.** `loadcheck.sh` reports 0 failures. No negative `scoreboard players add/remove`. No glyph font on
  the first element of a text component list. Nothing sunk below the floor. No teleport into blocks.
- **R4, atlas budget.** Raiden ≤ 3.0 M px, with a hard cap of 3.5 M (§C.6).
- **R5, speed.** Fast checks per change and one full gate at the end. At most 2 agents at a time. Work in a
  worktree on `wip/rd`.
- **R6, chapter boss.** Raiden stays the fallback boss for chapters 2-4. Keep the coupling points and the
  difficulty level.

---------------------------------------------------------------------------------------------------------------------
## A. Fight structure

### A.1 Flow
```
spawn (weapon = random sword|polearm, 50/50; no intro, as in the game; subtitle "라이덴의 이나즈마 전하")
 └─ P0 Shogun ──(rage 900, or HP 55 % on the first cycle; both rules unchanged)──> P1 transformation 60 t (immune)
      ▲                                                                              └─> P2 Tenma (shield 750, 80 % DR)
      │                                                                                     │ shield 0
      └── normal_return: FORCED weapon switch (27/28) <── P3 exhausted 300 t (×2 damage) <──┘
death at HP 0 in any non-immune state (clip 48 t, voice line 「그 무엇도 영원한 것은 없다.」)
```
These stay **unchanged**: rage +1/t and +60 per boss hit that lands, the 55 % HP clamp on the first cycle, the shield
(750, drain table, passive decay, 만겁 success −190), the energy drain in P2 (except Skirk), exhausted ×2 for 300 t,
the base stats (267 / 6 / 40), the level scaling and `#bossDmgMul 160`. The footage does not show any of these, so
they keep the chapter-boss balance.

### A.2 Shogun phase (P0)
| topic | decision | source |
|---|---|---|
| Weapon | Random per fight (`rdWpn` 0 sword / 1 polearm). Each weapon has its own bag (§B.2). | wiki "무작위로 창 또는 검"; v1 caption |
| Switching | Only as the **forced first move after each `normal_return`**: sword→polearm uses 28 진세이무죠, polearm→sword uses 27 에이엔노 이카즈마. | wiki: rare before the first Tenma, almost always after the stun; v1/v4 captions |
| Switch after-effects | The weapon switched **to** starts a parallel effect that runs **until the next transformation**, stuns included (wiki ft. 33). Sword: field lightning (A-02). Polearm: blade eyes (A-11). Both are suspended during 5 and 7 so the screen stays readable. | wiki, A-02, A-11 |
| Guard stance 번개 배리어 | Pattern 9, both weapons. It parries basic attacks (`#icd 1`). Hits fill a guard meter → break → 100 t stun → recovery knock-back. In-guard counters by chance. A time-out after ≥ 4 parried hits → 카라타케. | B-03..B-07, wiki 번개 배리어 / 카라타케 / 카운터 어택 |
| Eyes | 10 single eye (break = 100 t stun) is always followed **one pick later** by 4 multi-eye. Multi-eye never comes on its own. Both weapons. | wiki "첫 단일 뇌안 이후 한두 패턴 이내에 광역"; A-18, B-01, B-02 |
| Illusions → Musou | 5 찰나의 포영 is sword only. Whether the real clone is found (100 t stun) or not (3 volleys), **7 몽상의 일심 always follows**. | wiki "찰나의 포영 다음에는 100퍼센트로 폭격"; v3/v4 footage |
| 무념무상 (Musou) | 7: blink to the centre, 8 rim orbs blast in sequence, time-stop darkening, then a field slash of r 19. Safe ring r 19-23 between the orbs. | A-09 |
| Rear checks | Reactive. At choose, when the player stands behind her (> 120° off her facing, ≤ 8 b) **and** has hit her from behind in the last 40 t: 25 판결의 검 (sword) or 26 (polearm). Cooldown 300 t. | wiki 판결의 검; A-03, A-12 |
| Movement | No walking. Remove the approach walk and the 12 t sidestep. She closes distance only by blink (A-19, 16 t, immune) to pattern-specific spots: player's left before 1, player's right before 21, 5.5 b in front before 3, the centre before 7 and 28. Between patterns: idle 16 t. | A-19 "she almost never walks" |
| Range use | At choose, the bag draw takes the first move whose range tag fits the player's distance: near ≤ 7 b, mid 6-14 b, far ≥ 8 b. If none fits, any move is drawn and its own blink closes the gap. | v1-v5 captions (ranged moves at 10-15 b, combos after a blink) |

### A.3 Transformation (P1, 60 t, immune)
Blink to the centre. A lightning ring travels along the floor from her (jumpable). Sky pillars land: one where the player
stood at the cue, five at random spots. A burst at her. The form appears. Title 「악요의 요고우 텐마」 (no hint
subtitle). Optional arena look swap (§D.3). Timeline in §B, row T.

### A.4 Tenma phase (P2)
| topic | decision |
|---|---|
| Body | Floating core figure (+1.0 b, bob ±0.2), a giant left arm with the glaive, 3 thin right arms, 2 tan gauntlet hands and a disc halo with crest (§C.2). The hitbox stays the husk + click shield as now (shared `mob/shield_ensure` is not edited). |
| Bag | {11, 12, 13, 14, 16, 17, 19}. **15 만겁** replaces the 4th pick once per transformation (unchanged). **18 돌진** when the player is ≥ 10 b away at choose and the last pick was not 18. **20 초월의 악요개안** when the player is in her rear cone (±60° of her back) within 9 b (cooldown 300 t). After 16, a 40 % chance chains straight into 17 or 11 (cool 4). |
| Close-in | Blink (pink streak) when 11 needs ≤ 8 b or 16 needs ≤ 9 b. |
| Safe hugging | Wiki: "가까이 붙을수록 피하기 쉬운 페이즈"; guide: the boss's left within ~2 b. The sweeps of 11 and 20 are annuli with an inner radius of 2.0-2.5 b, and the slabs of 17 spawn 2.5 b out, so staying within ~2 b avoids them. 16, 18 and 19 still reach a hugging player. |
| Shield / energy | Unchanged. 만겁 also sets every character's burst energy to 0 at cast, Skirk included (wiki: "모든 원소 폭발 게이지가 초기화"). |

### A.5 Stun / break states
| state | entered by | length | effects | after |
|---|---|---|---|---|
| clone found (98) | real clone hit in 5 | 100 t | stagger pose, dark stagger disc marker r 2.5 (A-08), damage ×1 | forced 7 |
| eye broken (98) | single eye 10 broken | 100 t | as above, 「간파했군.」 | multi-eye 4 one pick later |
| guard broken (98) | guard meter full in 9 | 100 t | gold light pillar, damage ×1.5 | recovery burst (nododge) at the end |
| exhausted (P3) | Tenma shield 0 | 300 t (wiki ~20 s; 15 s kept for balance) | unchanged (×2, energy refilled) | forced weapon switch |
The current illusion stun of 200 t is cut to 100 t, because the footage stagger is about 64 t + cut and the wiki says
"잠시 무력화".

### A.6 Decisions on the catalogs' open questions
| Q | decision |
|---|---|
| A1, B10 | Tenma is taken from v6-v9 + the wiki. The Shogun is taken from v1-v6. |
| A2 | The pale disc is the sword switch's field-lightning after-effect, separate from A-03. Cadence 80 t: one disc under the player, bolt 20 t later. |
| A3 | The rear checks always aim straight behind her (yaw + 180, locked at the cue). |
| A4 | Musou is 166 t: 8 orbs at r 21 every 45°, blasting 8 t apart. Each orb's 3-ring decal shows 20 t before its blast. |
| A5, B4 | Single eye: if not broken, it blasts at 140 t, r 5 (= its ring). Multi-eye: per-eye disk r 12 at the current three spots, blast 130 t after spawn. The cyan dome glow marks **danger** over each surviving eye from −26 t. A broken eye removes its disk (the pocket). |
| A6 | A-16 "돌진 3콤보" (22) and A-17 "번개돌진 콤보" (23, = 뇌명 돌진(창) + 영원함의 꿈) are two separate polearm moves. |
| A7 | Sizes are the catalog estimates rounded. The grid-measured ones are used exactly: ring 4.5, gaze ring 5, explosion 6.5. |
| A8 | Single eye HP 6 hits, multi eyes 4 hits each (4 t CD). One hit reveals the real clone (as now). |
| A9 | The 5-hit sword chain A-05 is the sword's near melee (8). The polearm's 원류 A-13 is 1. |
| B1 | The planted-glaive bomb is fixed at **50 t** after landing. The 98 t case is treated as an edit outlier. |
| B2 | 발도: charge start → flash 10 → hit 22 t, fixed. |
| B3 | B-04/05 are the in-guard counters (no wiki name, no line). Wiki 카운터 어택 = the stun-recovery knock-back B-07 「터무니 없군.」. 카라타케 = the guard time-out after ≥ 4 parried hits. |
| B5 | Arena r 23: 발도 r 12, 단절 band to the wall, vajra/transform rings to r 24, Musou slash r 19. |
| B6 | 돌진 triggers at ≥ 10 b. The barrage is 3 nododge hits on a disk of r 7. It is avoided by not being far away, or by dashing out of r 7. |
| B7 | 2 claps. The hands follow at 0.3 b/t and lock at the palm flash. |
| B8 | The 단절 near-field is r 4.5 for 40 t, 3 raw damage per 10 t (it can be left). |
| B9 | The transformation hit is the travelling floor ring (jumpable) plus the pillars. There is no separate expanding shell. |

---------------------------------------------------------------------------------------------------------------------
## B. Patterns

### B.0 Hazard API v2 (owned by S1-KIT; fixed here so the stages can work in parallel)
The current shapes s1..s14 become **parametric** hazards. The old ids stay as presets until S3 removes the unused
ones. A hazard is: origin + frozen yaw + shape params + `tell` (hit tick) + `dmg` + flags.
| shape | params | test |
|---|---|---|
| `disk` | r | horizontal distance ≤ r + 0.3 |
| `annulus` | rmin, r, half (deg, 180 = full) | rmin − 0.3 ≤ d ≤ r + 0.3 and \|angle\| ≤ half (covers sectors) |
| `rect` | len, wid, off (start distance), yawoff | box in the yaw frame |
| `to_wall` | wid | rect from the origin along the yaw to the arena circle (len computed at lock, ≤ 47) |
| `sweep` (travelling arc) | r0, v (b/t), band, half | radius band [r0 + v·age − band, r0 + v·age], angle ≤ half (rings = half 180) |
| `slab` (travelling straight) | d0, v, w (half width), depth | front band along the yaw axis, \|lateral\| ≤ w |
| `orb` (travelling disk) | d0, v, r | disk around the moving centre |
| `follow` | r, v | disk that chases the player (B-15 pool) |
| `field` | r, every, dmg | DoT disk while alive (단절 near-field) |
| `safe_dome` | dome r | everywhere **outside** the dome = fatal (만겁) |
Flags: `quiet` | `decal:<kind>` (§B.3) · `nododge` (ignores `#dodged`) · `jump` (vertical band −0.5..+0.75 instead of
−0.5..+3.5) · `kb:<b>` (knock-back through the existing player push path, clamped to r 22.5, never a `tp`) · `lift`
(small upward velocity) · `hits:n` (max hits, default 1) · `detached` (travelling hazards survive `finish`; `pause`,
`transform_start`, `exhausted_start`, `death/start` and `cleanup` kill them).

**Decal / strike split (R1).** `hazard/create` summons a decal display **only** when `decal:` is set. The strike visual
is a **separate** display summoned at the hit tick (strike flicker → afterglow → fade → kill, as now), sized to the
shape, for every hazard, quiet or not. A decal display is killed at the hit tick. Travelling hazards are one display set
(card or segment ring) whose transformation interpolation is written **once** at launch (translation and scale are
linear in time, `interpolation_duration` = travel ticks), with no per-tick commands. The server test uses the same
start tick and speed.

### B.1 Damage
Raw damage → `hurt` (×1.6 `#bossDmgMul`, then level scaling; ×4.18 at Lv12 before defence; current.md §2) is
unchanged. The raw values below stay close to the current hit they replace. The S3 balance pass holds the
**damage-per-minute taken by a standing player and by a scripted dodger, per phase, at Lv 12/18/24, within ±15 % of
the current build** (baseline measured in S0), by scaling a phase's raw values if needed.

### B.2 Pattern table
Legend. **Act** = keep / mod / repl / new / remove. **Tele** = Q (quiet, with the cue source) or D (decal, kind).
Damage is raw, with the current value in brackets. Range tag: N near ≤ 7 b, M mid 6-14 b, F far ≥ 8 b.
Timelines start at choose t0 (yaw locked unless noted). "cue" = the first readable motion or sound. Every listed hit
satisfies cue → hit ≥ 12 t (≥ 20 t where marked ★). A follow-up hit inside one continuous motion (a dash's end
crescent) counts from that motion's cue. Separate swings of a combo each have their own wind-up and are ≥ 10 t after
the previous hit. Tenma rows that start with an optional blink count from the end of the blink.

#### Phase 0 — both weapons
| id | footage | act (current) | timeline (t) | shape / size (b) | tele | dmg | notes |
|---|---|---|---|---|---|---|---|
| 27 무기 변경 – 검 | A-01 | new (forced after recovery, polearm→sword) | raise + hoop 0 (cue) · vortex disc at feet 6-18 (FX) · ★burst 20 · model swap 22 · end 34 | disk r 6, centre 1 b forward | Q (raise, hoop, `respawn_anchor.charge`) | 16 | 「번개여, 나의 호령을 따르라.」 Starts the field lightning. |
| 28 무기 변경 – 창 | A-10 | new (forced, sword→polearm) | blink to centre 0-14 · hoop + vortex 14 (cue) · ★burst 34 · swap 36 · end 46 | disk r 5 | Q (hoop, flash 30) | 16 | 「무상의 진!」 Starts the blade eyes. |
| 6 field lightning | A-02 | **repl** (낙뢰 is no longer a bag move; id kept for `test/pattern`) | every 80 t while the sword effect runs: decal at the player's feet (locked) 0 → bolt 20 | disk r 2.5 | **D** `disc_pale` r 2.5 (pale fill, brighter rim) | 8 (12) | impact ring r 3, crack marks linger 40 t (scorch, not a warning) |
| 6b blade eye | A-11 | new (polearm effect) | every 60 t: eye sigil 1.5 b beside the player, 0.3 b up (cue) · glint 8 · burst 12 | disk r 2 | Q (the sigil object; no floor decal) | 8 | |
| 9 번개 배리어 (guard) | B-03..07 | new (N, ≤ 1 per 3 picks) | guard 0-160: basic hits (`#icd 1`) parried (gold waist crescent, dmg ×0.1). Skills, bursts and reactions pass at ×0.5. Meter: basic +1, other +2, break at 14. **Counter** (35 % on a parried hit, CD 60): sword: black line c0 (cue) → spin c12 → floor bolts c24 → lunge c40; spear: cue c0 → star c8 → sweep c18. **Break** → stun 100 t; recovery decal at 76 → ★burst 100. **Time-out** at 160 with ≥ 4 parried hits → **카라타케**: blink back 6 b 160-166, raise 170 (cue) → ★slash 190 | counters: disk r 3; rect 8 × 1.5 (locked c12); rect 8 × 2 (relocked c28); spear disk r 4.5. Recovery: disk r 4.5, nododge, kb 2.5. 카라타케: rect 14 × 3 | counters Q (black line + `shield.block`). Recovery **D** `ring` r 4.5 (footage glowing circle, 24 t). Stance aura `aura` r 1.8 (footage; not a warning) | 8 / 8 / 12; spear 12; recovery 6; 카라타케 24 | lines 「가소롭군.」 「터무니 없군.」 (recovery) 「슬슬 끝내지.」 (카라타케). Parry and guard live in `incoming` (Raiden-owned). |
| 10 마가츠의 뇌안 (단일) | A-18, B-01 | new (any range) | cast 0 · sky beam 4 · eye 8 (orb 1.8 b up, 6 hits) · ring decal 8-14, fades by 28 · dome glow 122 · ★blast 148 unless broken · she holds a cast/idle pose while it lives | disk r 5 at the eye | **D** `ring` r 5, spawn only (dark disc expands into a bright ring, then fades, as footage) | 30 | 「이 눈으로 속세를 꿰뚫어 보리.」 HUD (real game): 「마가츠의 뇌안」을 계속 공격해서 제거하세요. Break → 「간파했군.」 → stun 100 t → queue 4 one pick later. |
| 4 마가츠의 뇌안 (광역) | B-02 | mod (P4) | cast 0 · 3 sky pillars 6 · eyes 10 at the current spots (centre+(−10,−6), (10,−6), (0,11)), 2.5 b up, 4 hits each · dome glow over survivors 114 · ★blast 140 · end 150 | disk r 12 per surviving eye; broken eye = no disk (pocket); 1 hit max | **D** `ring` r 12 per eye, thin, from 10 until the blast (footage) + cyan dome glow (volumetric) | 34 (34) | 「뇌광이 영원의 땅을 비추는구나.」 The timer grows 58 → 140 t, enough to break one eye. |

#### Phase 0 — sword
| id | footage | act (current) | timeline (t) | shape / size (b) | tele | dmg | notes |
|---|---|---|---|---|---|---|---|
| 3 뇌명 돌진 (검) | A-04 | mod (P3 뇌명) F | **far**: blink 0-6 to 5.5 b in front · iai stance 12 (cue) · star flash 18 (aim lock) · hit1 30 (she dashes 9 b, 28-36) · hit2 36 · idle to 66 (A-04: ~2 s free hits). **near** (≤ 6 b): raise 0 · flash 10 · hit1 22 · hit2 28 · end 40 | far: rect 10 × 3 along the dash, then annulus 0-4 ±70° at the end. Near: rect 9 × 2, then rect 4 × 2 at the end (vertical crescent) | Q (stance + `amethyst_block.resonate` star) | 14 / 13 (16 / 15) | 「뇌명.」 |
| 8 5단 콤보 | A-05 | **new** N | stance spark 0 (cue) · lunge 1.5 b at 4 · S1 12 · S2 22 · S3 34 · S4 50 · S5 64 · end 74 | S1: 2 rects 6 × 1.2 at ±25° (V). S2: rect 9 × 1.5, yaw +20°. S3: disk r 2.5 at 2 b ahead. S4: rect 10 × 2, yaw −20°. S5: disk r 3 at 2.5 b ahead | Q (spark, sweep sounds) | 8 / 8 / 9 / 12 / 13 | Gaps ≥ 10 t, each with its own wind motion. |
| 2 뇌전이 이끈 번개 | A-06 | **repl** (P2 회전 참격) F | star flash 0 (cue) · discs launched 6 / 10 / 18 (each re-aimed at launch) · wind-up 26-32 · wave launched 34 · end 64 (detached wave expiry) | discs: `orb` r 1.7, 0.8 b up, v 2.0, ≤ 24 b. Wave: `sweep` r0 1, v 0.8, band 1, half ±22° (≈ 9 b wide at 12 b), **jump** | Q (projectiles are visible in flight) | 9 × 3 / 16 (10 × 3 / 18) | 「뇌전은 인간의 의지 따위로 변하지 않아」 |
| 5 찰나의 포영 | A-07 | mod | blink out 0 (hidden, immune; the gate stays `rdPat 5`) · 4 clone pillars 8 at 13 b from the player (90° apart, clamped r ≤ 20) · clones 12 · volleys V = 40 / 96 / 152: clone raises sword V−14 (cue, aim lock) → launch V → reaches the player ≈ V+16 · after volley 3 + 30, the real body appears | fake: `slab` w 6 (12 wide), depth 1, chest height, v 0.8. Real: 2 slabs crossing at ±15° (X) | Q (raise + glint card on the blade) | 10 each (10) | 「찰나의... 포영!」. Clones are dark-violet smoky silhouettes at **boss scale** (now 2.4×); the revealed one glows. Remove the hint subtitle. Found → 「간파했군.」 → stun 100 t → 7. Not found → 7. Removes the 3 t X tell. |
| 7 몽상의 일심 | A-09 | mod | blink to centre 0-6 「무념 무상, 천하가 고요하리.」 · raise + moon arc + sky bolts 10 · orb k (k 0..7): decal 30+8k → blast 50+8k · whole-field darkening + frozen shards 110 「무념 무상, 일도 단절.」 (cue) · ★slash 130 · lingering strokes 130-158 (visual) · end flash 160 · end 166 | orbs: disk r 4 at r 21, every 45°, random rotation. Slash: disk r 19 | orbs **D** `rings3` r 4 (3 concentric thin rings, footage). Slash Q (darkening = 20 t cue; uniform tint over the whole field, not a hazard outline) | 10 / 30 (same) | Safe: r 19-23 in the 8 b gaps between orbs. |
| 25 판결의 검 | A-03 | **new** reactive | hand glow + charge sound 0 (cue, yaw+180 locked) 「판결은 내려졌다.」 · thin beam 10 (FX) · hit 14 · crystal wall lingers to 26 · end 30 | rect 12 × 1.6 behind her | Q | 15 | |

#### Phase 0 — polearm
| id | footage | act (current) | timeline (t) | shape / size (b) | tele | dmg | notes |
|---|---|---|---|---|---|---|---|
| 1 원류 4단 | A-13 (+A-14) | mod (P1 4연격) N | blink 0-6 to 2.5 b at the player's left · raise 10 (cue) · tip star 16 · H1 28 · H2 38 · H3 48 · H4 62 · bolt field 82 · follow-up (60 %, only if the player is ≥ 5 b away at 90): raise 90, glow 96 (lock), hit 104 · end 96 / 112 | H1, H2: annulus 0-5.5 ±90°. H3: rect 6 × 1.5. H4: rect 15 wide × 3 deep at 2-5 b ahead. Field: 7 disks r 1.2 in a 10 × 6 zone centred 8 b ahead (1 hit max). Lance: disk r 2 at the locked spot | Q (star at the tip, slam + crackle 20 t before the field) | 9 / 9 / 10 / 15, field 8, lance 14 (9 × 3, 15, 12, 12) | Field impacts show a reddish ring (footage); this is strike FX. |
| 21 수천수만의 염원 | A-15 | **new** N | blink 0-6 to 4.5 b at the player's right · twirl 10-46 (cue, loop sound) 「번개와 함께 흙으로 돌아가라.」 · flash 48 · ★hit 50 · end 62 | disk r 6.5 around her, **nododge** | Q (twirl) | 22 | wiki: "회피 불가". 40 t tell. |
| 22 돌진 3콤보 | A-16 | **new** F | twirl 0 (cue) 「속세는 그림자와 같지.」 · lock 12 → D1 20 · lock 22 → D2 32 · lock 34 → D3 44 · end 58 | 3 × rect 11 × 2 from her through the locked point. She moves along each in 4 t (clamped r ≤ 20) | Q (twirl; each re-aim pause ≥ 10 t) | 12 × 3 | |
| 23 번개돌진 콤보 | A-17 | **new** M | polearm behind the hip 0 (cue) 「뇌명.」 · lock 6 · star 8 · zig-zag dash hit 14 · ring flash 22 · ring 34 · crouch + column 40 · lunge 52 · end 64 | dash: rect 9 × 2 to the locked point (she arrives beside the player). Ring: disk r 4.5 (grid-measured). Lunge: rect 5 × 2 ahead | Q | 12 / 6 / 14 | The ring is weak (footage). |
| 24 원거리 창 | A-14 | **new** standalone F (≥ 10 b) | blink 0-6 to 7 b from the player · raise 10 (cue) · tip glow 16 (lock) · hit 24 · end 34 | disk r 2 at the locked spot + diagonal lance FX + rift streaks | Q | 14 | Also the 50 % follow-up of 1. |
| 26 창 뒤 견제 | A-12 | **new** reactive | twirl 0 (cue) · hit1 16 · hit2 26 · end 36 | both: annulus 4.2-5.8, ±100° about her rear | hit1 Q; its lightning band stays on the floor 16-26 = hit2's warning (footage) | 10 / 12 | |

#### Phase 1 — transformation
| id | footage | act | timeline | shape | tele | dmg | notes |
|---|---|---|---|---|---|---|---|
| T 변신 | B-08 | mod (burst s8 r6) | 「이 몸이 곧 영원이다」 + blink to centre 0-6, rise · floor ring launched 20 · sky crackle 24 (cue; one pillar locked on the player's spot) · ★pillars 44 · burst at her 46 (FX) · form + title 50 · `armor_start` 60 | ring: `sweep` r0 2, v 1.0, band 1.4, full, **jump**. Pillars: 6 disks r 1.5 (5 random, ≥ 6 b apart) | ring: the travelling band itself is the visual (footage). Pillars Q | ring 14, pillars 16 (18) | immune (phase 1) |

#### Phase 2 — Tenma
| id | footage | act (current) | timeline (t) | shape / size (b) | tele | dmg | notes |
|---|---|---|---|---|---|---|---|
| 11 몽상 • 염원이 깃든 백안지륜 (3단) | B-09 | mod (P11) | blink if > 8 b · raise 0 (cue) 「방해는 모두 베겠노라」 · SW1 14 · SW2 26 · cock-back 42 (cue, lock) · throw impact 54 · glaive re-forms 62-70 · bomb decal 92 · bomb 104 · end 108 | SW: annulus 2.5-7.5 ±100°. Throw: disk r 3 at the locked spot. Bomb: disk r 3.5 at the planted glaive | SW and throw Q. Bomb **D** `ring` r 3.5, 12 t (footage sparkle/ring) | 19 / 19 / 18 / 20 (19 / 19 / 22) | The planted glaive prop is cut at the floor (R3). |
| 20 몽상 • 초월의 악요개안 | B-14 | **new** reactive | glint 0 (cue) 「어리석군」 · spin 13 · throw 31 (lock 19) · bomb decal 69 · bomb 81 · end 85 | spin: annulus 2.0-7 full. Throw: disk r 3. Bomb: disk r 3.5 | as 11 | 18 / 18 / 20 | |
| 16 번개 신의 신속한 발도 | B-10 | mod (P16 iai variant) | blink if > 9 b · crouch charge 0 (cue) · orb flash + thin expanding ring at her 10 (FX) · ★hit 22 · floor turbulence 22-36 · end 40 | disk r 12 (360°, hip height). Dash i-frames dodge it | Q | 30 (30 + 26) | 40 % chains into 17 or 11. |
| 19 몽상 • 단절 | B-12 | **new id** (split from P16) | blink to 10 b in front if outside 6-14 · halo ring 6 (cue) 「단절!」 · sky column 16 · band decal 24 (lock) · ★slam 64 · near-field 66-106 · end 70 (field detached) | slam: `to_wall` w 5 through the locked player spot. Field: disk r 4.5, 3 per 10 t | slam **D** `band` (two bright edge lines + faint pale fill, footage), 40 t. Field: the cracked glowing floor is its own visual (footage) | 34 / 3 per tick (34 / 5) | |
| 12 흉장의 수안 · 박수 | B-13 | mod (P12, 1 clap) | spikes + dark sphere 0-14 (cue) 「감옥으로 만들어 주지」 · orb flies 16 · hands appear 24 (±2.8 b beside the player), follow 0.3 b/t · palm flash 50 (lock) · clap1 64 · re-form 80 · flash 104 · clap2 118 · end 130 | disk r 3 between the hands, ×2 | Q (the hands; palm star 14 t) | 16 × 2 (25) | |
| 13 흉장의 수안 · 추적 손바닥 | B-15 | mod (P13) | twirl 0 · seed 8 → ink at the player's feet 12 · pool follows 12-68 at 0.32 b/t, ticks at 28 / 48 / 68 · stops and grows 68-72 · palm slam 84 · end 96 | pool: `follow` r 1.5 (DoT r 1.8). Slam: disk r 4.5 + `lift` | **D** `pool` (dark smoky, follows), then grown dark-magenta disc r 4.5 (footage) | ticks 4 (6 per 8 t), slam 24 (24) | Growth → slam 16 t. |
| 14 금강괴멸파 | B-18 | mod (P14) | 「천수의 속박!」 hurl 0 · vajras 6 / 12 / 18 at side 6 around the centre (r 3.5) · pulse k (order 1,2,3,1,2,3) at P = 60 + 36k: current runs down the vajra P−10 (cue), top flash P−2, ring starts P · triple at 276 · end 310 | rings: `sweep` r0 2, v 0.8, band 1.4, full, **jump**, to r 26 | base **D** `ring` r 2.5 per vajra (source marker, footage). The ring bands themselves are visible | 14 each (14) | The ~6 s wait before the first wave is shortened to 3 s. Speed 0.52 → 0.8 (footage 15-20 b/s). Ring visuals = segment cards (§C.6). |
| 15 만겁 | B-17 | mod (P15 + judgment rig) | 「그 끝은 만겁일지니...」 0 · flash + vanish 14 (immune, hidden, energy → 0) · arena tint 18 · flower 40 + light column 42 · gauge (1 electro / 4 other hits, unchanged) → dome grows to r 8 in 8 t · beam from the flower 140 (cue) · slash 152 · dome cracks 160 → shatters 176 · reappear 184 · end 196 | `safe_dome` r 8 (fatal outside; 1 damage inside) | no shaped decal (footage: whole-floor tint) | fatal | HUD (real game, instant kill): 「추모의 꽃다발」에 번개 원소 공격을 가해 보호막을 펼치세요. **Judgment rig and camera lock removed** (§F): the slash is one giant crescent card swept 360° around the centre over 6 t at 2.5 b height, plus a white flash card. `camera/hold` stays as a no-op. |
| 17 몽상 • 궤멸의 검기 | B-11 | **repl** (P17 static rays) | glint 0 (cue) 「궤멸하라!」 · lock 4 · swing1 8 → 5 slabs · swing2 53 → low wave · end 70 (waves detached) | slabs: 5 × `slab` w 0.9, height 4.5, d0 2.5, v 0.45, at −30/−15/0/15/30°, 1 hit max for the set. Wave: `sweep` r0 2.5, v 0.28, band 1, ±40°, **jump** | Q (the projectiles are visible) | 15 / 20 (17 / 21) | |
| 18 번개 신의 강력한 돌진 | B-16 | **repl** (P18 static line) | trigger ≥ 10 b · glint 0 (cue) 「뚫려라!」 · flash 13 (lock) · rush 23 (to 1.5 b short of the lock, 4 t) · ★barrage 28 / 34 / 40 · end 52 | 3 × disk r 7 around the arrival point, **nododge** | Q (glint + flash) | 14 × 3 (22 + 19 × 2) | |
| P3 exhausted | — | keep | collapse → kneel → recover (300 t) | — | — | — | Subtitle "갑주 파괴" only. |

**Removed:** P6 낙뢰 as a bag move, the P16 50/50 variant, the P18 static line, the approach walk and sidestep,
the judgment rig (`T:build_raiden_judgment_rig.mjs`, 180 functions, 22 models), the camera lock, the 2.4×
illusion scale, and every hint subtitle (§D.2).

### B.3 Decal kinds (the only floor decals left; all outline-like, scaled to the hazard)
| kind | sprite | used by | life |
|---|---|---|---|
| `ring` | thin bright circle (256²) | 4 eyes r 12 · 10 eye r 5 (spawn flash) · glaive bomb r 3.5 · guard recovery r 4.5 · vajra base r 2.5 · stagger marker r 2.5 (state) | per row |
| `rings3` | 3 concentric thin rings (256²) | 7 Musou orbs r 4 | 20 t |
| `disc_pale` | pale fill, brighter rim (128²) | 6 field lightning r 2.5 | 20 t |
| `band` | two edge lines + faint fill (64 × 256, stretched) | 19 단절 w 5 | 40 t |
| `pool` | dark smoky blot (256²) | 13 shadow r 1.5 → 4.5 | 60 t |
| `aura` | crackling ring (reuses `ring` + crackle card) | 9 guard stance r 1.8 | guard |
| `tint` | uniform 64² gradient, 35 % alpha | 7 time-stop, 15 arena tint (whole field, not an outline) | event |

---------------------------------------------------------------------------------------------------------------------
## C. Model

### C.1 Shogun (P0); target height 2.0 b
| item | now | new |
|---|---|---|
| body | 10 skin boxes from the user-supplied 64² skin + `_dull` copies | Keep the supplied skin and the 10 parts. Add to the models: wide drooping sleeves below the hips (right sleeve longer, dark violet), obi knot + tassel, flower ornament on the left of the head. |
| hair | in the skin | + `braid` part: one long braid to the hips, with secondary swing |
| back drape | none | + `drape` part: translucent dark violet train #4a3a70 at about 65 % alpha, waist to ankles, flaring |
| halo | `chakra` ring with tomoe | **Halo arch** (1 part): an eye emblem (diamond lens, 0.6 b) 0.9 b above the head, and 4 tomoe orbs (0.35 b, #8f5cff) at head and chest height ±0.9 b behind the upper back, joined by thin lightning threads. Slight bob and roll, no orbit. Brighter in guard. |
| weapon | katana / polearm swap | Same single part, model swap by look `sword` / `polearm`. Katana 1.45 b: slim, pale violet-white glowing blade, dark hilt, held low with the tip down and forward. Polearm 2.3 b: dark violet ringed shaft, curved glowing blade at the low end in idle, short top spike. + `weapon_fx` card |
| extras | crown, ribbon_r/l, armor | removed; + `aura` (guard floor ring, shown only in guard) |
| silhouette checks | — | Pale torso and dark legs. The sleeves and drape widen the outline below the waist (A catalog model notes). |

### C.2 Tenma (P2); envelope about 8 × 7 × 4 b
| item | new |
|---|---|
| core | The same 10 body parts with look `tenma`: skin boxes tinted dark (black bodysuit with violet glow lines), pale hip and leg plates and dark tassets in the leg models. Floats +1.0 b, bob ±0.2. Braid kept, drape hidden. |
| disc halo + crest (1) | Dark disc 1.7 b in diameter, violet tomoe-eye emblem at the centre, thin outer ring. Two dark crescent horns (0.6 b) behind the head, pointing up and out. |
| giant left arm (3: upper 2 b, forearm 2 b, hand 1 b) | Disembodied, rooted 3 b up behind her left shoulder. Pale lilac lacquer #d8b4e2 with #9a6fb0 shading, ball joints, glowing eye sigils on the forearm. Holds the glaive. |
| glaive (1) + `glaive_fx` (1) | Shaft 6.5 b, magenta edge line, curved blade 2.2 b, round pink guard ornament. Usually horizontal across the front at hip height. Hidden while thrown (a separate planted prop); re-forms over 8 t. |
| 3 thin right arms (6: upper + forearm-with-hand each) | 2.5-3 b each, fanned up and right like a halo of arms. One holds a short dagger/spearhead pointing up; open and claw hands. |
| 2 gauntlet hands (2) | Tan #c9a27a with darker bands, 1.3 b wide, a violet eye sigil on each palm. They hover low in front, below her feet, palms up. Kept ≥ 0.3 b above the floor (floor check). |
| removed | the current cradle hands, 4 rear arms, `giant_weapon` katana arm, lilac box plates |
| props (separate entities) | multi/single eye orb (reuse `electro_orb`, restyled), blade-eye sigil card, clone silhouettes (dark tint + glow variant; 2 poses), Musou crystal orbs, **vajras** (crystalline spike bundles 3.5 b, replacing `lightning_stake`), flower (magenta lotus + dark orb, restyling `remembrance_flower`), dome r 8, clap hands (translucent faceted violet, 4.5 b), slam palm (pale, 4 b, from above), planted glaive (glaive model tilted, cut at the floor), seed (dark orb with eye), switch hoop + vortex cards |

### C.3 Rig approach: move to the shared RIGLIB
| option | for | against |
|---|---|---|
| keep pre-bake (`rig/poses/<phase>/<clip>/<t>`) | no new framework | 1,948 files × 52 `data merge` (32 MB), ~330 commands per tick idle, no floor or step checks, no debug poses. With ~36 new clips × 2 forms it would grow past 2,500 files. The model is rewritten anyway (the Tenma form is entirely new). |
| **RIGLIB** (`mboss_rig_compile`, `mboss_rig_clips`, `mboss_shape_lib`, `mboss_paint_lib`, `mboss_model_lib`, `createRigFollow`) | Compiled interpolation segments (keys only where the client lerp diverges), binary-tree dispatch, follow lists per form, step-violation and culling checks, debug poses for `S:az/understand/rigtech_render.py`. Proven on 5 bosses. | The controller contract changes from `rdAnim` scores to `rig/play/<clip>` calls (a mechanical change in S2). New code, about +1-2 h. |
**Decision: RIGLIB.**
- Generator files: `T:build_raiden_rig.mjs` (rewritten), plus new `T:raiden_geometry.mjs`, `T:raiden_clips.mjs` and
  `T:raiden_paint.mjs`. No edits to the shared libraries; any need goes in as a request.
- Output stays under `F:boss/raiden/rig/`: `init`, `spawn`, `tick`, `play/<clip>`, `start/<clip>`, `c/**`, `d/**`,
  `follow*`, `state/{shogun,tenma,hidden}`, `look/{sword,polearm,tenma}`, `flash` (one part group, 3 t), `kill`.
- Fixed UUIDs come from an append-only table. The tag `rlk_raiden_part` is kept.
- Manifest v2 (`T:raiden_rig_manifest.json`): clips, lengths, **events**, parts, px ledger, element counts, culling.
- **Build checks:** step violations; **floor** (no shown element of any part or prop below y 0 at any compiled
  tick); visible elements ≤ 3.5 k Shogun / ≤ 6 k Tenma; px ledger ≤ budget.
- **Temporary `rig/legacy_anim`** maps the old 25 `rdAnim` ids to the nearest new clips, so the old encounter still
  runs after merge M1. S3 deletes it.

### C.4 Budgets
| | now | target |
|---|---|---|
| rig parts | 52 | **30** (cap 34): 10 body · Shogun 6 (braid, drape, weapon, weapon_fx, halo arch, aura) · Tenma 14 (disc halo, arm 3, glaive 2, right arms 6, gauntlets 2) |
| commands per tick (rdsim) | ~330 idle, ≤ 520 peak | ≤ 150 idle, ≤ 320 peak |
| `F:boss/raiden` | 2,670 files / 35 MB | ≤ 1,100 files / ≤ 10 MB |
| Raiden RP models | 337 / 10.3 MB | ≤ 220 / ≤ 5 MB |

### C.5 Clips (manifest v2; the encounter takes hit ticks from these events)
| clip | len | events (played tick) |
|---|---|---|
| `idle_sword`, `idle_polearm` | 40 L | — (halo bob) |
| `blink_out` / `blink_in` | 6 / 10 | gone 4 / appear 0, settle 8 |
| `iai_dash` (3 far) | 36 | stance 0, flash 6, hit1 18, hit2 24 |
| `iai_near` (3 near) | 28 | raise 0, flash 10, hit1 22, hit2 28 |
| `combo5` (8) | 74 | cue 0, s1 12, s2 22, s3 34, s4 50, s5 64 |
| `disc_cast` (2) | 40 | cue 0, d1 6, d2 10, d3 18, wave 34 |
| `rear_iai` (25) | 30 | cue 0, hit 14 |
| `musou` (7) | 166 | starts at pattern t0 and embeds the blink-in: appear 6, raise 10, arc 20, dark 110, slash 130, end 160 |
| `guard` | 20 L | — |
| `parry` | 6 | flash 1 |
| `counter_sword` / `counter_spear` | 46 / 26 | cue 0, burst 12, bolts 24, lunge 40 / cue 0, star 8, sweep 18 |
| `karatake` | 32 | retreat 0, raise 10, hit 30 |
| `switch_sword` / `switch_polearm` | 34 / 32 | hoop 2, vortex 8, burst 20, swap 22 / hoop 0, burst 20, swap 22 |
| `p_4hit` (1) | 76 | raise 4, star 10, h1 22, h2 32, h3 42, h4 56 |
| `p_lance` (24, 1 follow-up) | 24 | raise 0, glow 6, hit 14 |
| `p_twirl_slam` (21) | 52 | twirl 0, flash 38, hit 40 |
| `p_twirl_dash` (22) | 58 | twirl 0, d1 20, d2 32, d3 44 |
| `p_zigzag` (23) | 64 | hip 0, star 8, dash 14, ring 34, lunge 52 |
| `p_rear` (26) | 36 | twirl 0, h1 16, h2 26 |
| `cast` (eyes, 6/6b cue) | 20 | cast 8 |
| `stagger` / `stun_recover` | 20 + 40 L / 24 | — / burst 24 |
| `transform` | 60 | rise 4, ring 20, pillars 44, form 50 |
| `death` | 48 | — |
| `t_idle` | 60 L | hover bob, arm drift |
| `t_blink_out` / `t_blink_in` | 6 / 10 | as the Shogun's |
| `t_combo3` (11) | 70 | raise 0, sw1 14, sw2 26, cock 42, throw 54, reform 62 |
| `t_spin_throw` (20) | 46 | glint 0, spin 13, throw 31 |
| `t_iai` (16) | 40 | crouch 0, flash 10, hit 22 |
| `t_waves` (17) | 70 | glint 0, swing1 8, swing2 53 |
| `t_danjeol` (19) | 80 | halo 6, raise 10, band 24, slam 64 |
| `t_summon` (12) | 24 | sphere 4, throw 16 |
| `t_seed` (13) | 20 | twirl 0, throw 8 |
| `t_vajra` (14) | 30 | hurl 6, 12, 18 |
| `t_vanish` / `t_reform` (15) | 14 / 20 | gone 14 / appear 0 |
| `t_rush` (18) | 52 | glint 0, flash 13, rush 23, b1 28, b2 34, b3 40 |
| `t_collapse` (→ P3) | 46 | form T→S at 20, kneel 46 |
| `exhausted` / `recover` | 60 L / 28 | — |
That is 45 clips. The pattern-to-clip offsets in §B are binding. S1-RIG may retime inside a
clip, but not the event ticks.

### C.6 Texture budget and reclaim (R4)
| family | now (M px) | after |
|---|---|---|
| fxg `tele_*` (16) | 1.31 | 0 (deleted) |
| fxg `charged_*` (16) | 1.31 | 0 (deleted; the strike visuals no longer need a charged decal) |
| fxg `ringq_*` (13) | 1.64 | ≈ 0.01: one 32 × 256 band sprite. Rings are drawn by 24 segment cards per ring with one interpolation (vajra, transform) |
| `shockwave` 512² | 0.26 | 0.07 (256²) |
| `crescent_a/b` | 0.26 | 0.13 |
| other fxg (~49 sprites) | 2.14 | ≤ 1.7 (drop judgment, rift and sky-bolt sprites, plus any left unused after S2) |
| new decal sprites (§B.3) | — | ≤ 0.25 |
| rig painted sprites (lacquer tile, gauntlet tile, glaive, halo disc/emblem, tomoe orb, braid, drape, sleeves) | ≈ 0 (concrete + swatches) | ≤ 0.45, tint-shared |
| props / new FX cards | — | ≤ 0.25 |
| **Raiden total** | **6.92** | **target ≤ 3.0 M, cap 3.5 M** (reclaim ≥ 3.9 M) |
| stitched items atlas | 14.41 | **gate ≤ 11.0 M** at S3. Forecast with Apep's 1.45 M budget: ≈ 12.4 M, under both the 15.5 M I1 gate and the 15.8 M two-boss gate, so Apep's Q27 (halving Raiden rings) is no longer needed. |

---------------------------------------------------------------------------------------------------------------------
## D. FX, sound, HUD

### D.1 Cues and sounds (vanilla only; every id is checked against the 26.3 `sound_event` registry, §E.1)
| cue | visual | sound (`minecraft:`) |
|---|---|---|
| star flash (iai, polearm tip, glaive glint) | 4-point white-violet star card + 1 b ring flash | `block.amethyst_block.resonate` p1.6 + `entity.firework_rocket.twinkle` p1.4 |
| blink out / in | violet flicker → wisp / speed streaks + smoke | `entity.enderman.teleport` p1.4 / `entity.illusioner.mirror_move` p1.2 |
| polearm twirl | vertical bright ring card (1.5 b) spinning | `entity.player.attack.sweep` every 6 t + `item.trident.riptide_1` p1.6 |
| weapon switch | dark hoop → vortex disc (FX) → dome burst | `block.respawn_anchor.charge` p1.2 → `entity.lightning_bolt.impact` + `block.beacon.activate` p1.5 |
| bolt / lance impact | vertical bolt, flat shock ring, crystal shards, scorch | `entity.lightning_bolt.impact` (+ `thunder` p1.4 vol .5 for big ones) |
| crystal walls / spikes | jagged violet crystal cards | `block.amethyst_cluster.break` + `block.glass.break` p1.3 |
| parry / counter cue | gold waist crescent / black vertical line | `item.shield.block` p1.4 / `block.anvil.land` p2 vol .4 |
| guard shatter + stun pillar | white-violet burst, gold light pillar | `block.glass.break` p0.8 + `block.beacon.power_select` p1.2 |
| eye spawn / glow / break / blast | sky beam, orb, dome glow, starburst | `block.beacon.activate` / `block.beacon.ambient` / `block.amethyst_cluster.break` / `entity.generic.explode` p1.4 + lightning impact |
| Musou darkening / slash | field tint + frozen shards / giant crescent + strokes | `entity.warden.sonic_charge` / `entity.warden.sonic_boom` + `entity.lightning_bolt.thunder` |
| Tenma sweeps / throw / bomb tell / bomb | glaive arcs / pink beam / small ring / flash + ink burst | `entity.player.attack.sweep` p0.6 + `item.trident.throw` p0.7 / `item.trident.thunder` / `block.respawn_anchor.charge` p1.5 / `entity.generic.explode` + lightning impact |
| 발도 charge / flash / hit | lightning gather / orb flash / disc sheet | `block.beacon.power_select` p1.6 / star sound / `entity.warden.sonic_boom` p1.3 |
| waves (slabs, low wave) | violet slabs / low crescent | `entity.breeze.wind_burst` p1.4 / `item.trident.riptide_3` p0.7 |
| 단절 | halo ring, sky column, band, wall of light | `block.beacon.activate` p0.8, `entity.lightning_bolt.thunder` p1.2 vol .5, `block.respawn_anchor.set_spawn` p1.2, `entity.lightning_bolt.impact` + `entity.generic.explode` p0.7 |
| clap | hands, palm star, dark burst | `entity.evoker.prepare_summon` p1.2, `block.amethyst_block.chime` p2, `entity.iron_golem.attack` p0.6 + `block.anvil.land` p0.5 |
| shadow | seed, pool, ticks, growth, palm | `entity.ender_eye.launch`, `block.sculk.spread` loop, lightning impact p2 vol .3, `block.sculk_shrieker.shriek` p1.5, `entity.iron_golem.damage` p0.5 + explode p0.8 |
| vajra | drive, current, pulse, ring | `block.anvil.land` p0.6 + lightning impact, `block.beacon.ambient` p1.8, `block.conduit.attack.target`, `entity.breeze.wind_burst` p0.6 |
| 만겁 | vanish, tint, flower, gauge, dome, slash, shatter | `entity.illusioner.mirror_move` p0.6, `block.beacon.deactivate` p0.5, `block.amethyst_block.resonate`, `block.note_block.chime`, `block.beacon.power_select` p1.6 + `block.glass.place`, `entity.lightning_bolt.thunder` + `entity.warden.sonic_boom` p0.6, `block.glass.break` × 3 |
| 돌진 | glint, rush, barrage | star sound, `item.trident.riptide_3`, `entity.player.attack.sweep` × 6 |
| transformation | ring, pillars, burst | `entity.lightning_bolt.thunder`, `entity.wither.spawn` p1.6 vol .4, `block.beacon.activate` |

### D.2 HUD and text (R2)
| current text | action |
|---|---|
| spawn subtitle "바닥의 보랏빛 예고를 보고 회피하세요" | **remove** → "라이덴의 이나즈마 전하" (the real boss-bar epithet) |
| pattern captions "name · advice" (e.g. "몽상의 일심 · 가장자리의 번개 구슬 사이로 피하세요") | **name only** (the wiki names above) |
| transform subtitle "번개 갑주를 파괴하면 잠시 무력화됩니다" | **remove** (title 「악요의 요고우 텐마」 only) |
| exhausted "갑주 파괴 · 지금 공격하세요!" | → "갑주 파괴" |
| illusion "X자로 베는 분신이 진짜 · 찾아서 공격하세요" | **remove** |
| judgment hint "꽃을 공격 → 보호막 안으로! 번개 1타 / 다른 공격 4타" | → the real game message 「추모의 꽃다발」에 번개 원소 공격을 가해 보호막을 펼치세요 (instant kill + real game) |
| — | **add** (real game) 「마가츠의 뇌안」을 계속 공격해서 제거하세요 while the single eye lives |
| boss bars | unchanged (name + "번개 갑주"/"갑주 파괴", sub-bar). First text element plain; the font `rlk:bossbar` only after it (R3) |
New voice lines (wiki): 너무 느리군. (blink, 1 in 3) · 판결은 내려졌다. · 번개와 함께 흙으로 돌아가라. ·
속세는 그림자와 같지. · 가소롭군. · 슬슬 끝내지. · 터무니 없군. · 무상의 진! · 이 눈으로 속세를 꿰뚫어 보리. · 어리석군.
「번개여, 나의 호령을 따르라.」 moves from 낙뢰 to the sword switch. A no-tips lint in `test_raiden` greps every
`title`/`tellraw`/`actionbar` under `boss/raiden` for advice words (피하·회피·하세요·점프·대시·이동·서 있·공격하) with an
allow-list of the two real-game messages.

### D.3 Arena look (optional, S2-TENMA, drop if short of time)
The footage switches the floor from teal water to dark blue-violet at the transformation. Proposal: phase-0 floor
`prismarine` (teal, animated), with `fill` rows (≈ 47 commands) swapping to `blue_terracotta` at the transformation
and back at `normal_return`. `room/raiden/arena` builds phase 0, and cleanup restores it. No other arena change.

---------------------------------------------------------------------------------------------------------------------
## E. Implementation

### E.0 Ownership (one owner per file; others send requests)
| stage | owns |
|---|---|
| S0 | split of `T:build_raiden_encounter.py` into `T:raiden_enc/{core,lines,shogun,tenma}.py` (byte-identical output); `S:rd/tests/**`; `--only` flag in `T:build_raiden_fx_textures.py` |
| S1-RIG | `T:build_raiden_rig.mjs`, `T:raiden_{geometry,clips,paint}.mjs`, `T:raiden_rig_manifest.json`; delete `T:build_raiden_judgment_rig.mjs`; RP `models/item/raiden/*` and `items/raiden/*` except `fx_*`; prop models |
| S1-KIT | `T:build_raiden_{hazards,hazard_vfx,fx_textures,materials,signature_vfx,object_vfx,orb}.py`, `T:raiden_obj_cards.py`, `T:raiden_fx_textures.json`, RP `textures/raiden/{fx,fxg}`, `fx_*` models |
| S2-SHOGUN | `raiden_enc/{core,shogun,lines}.py` (core holds bag/choose/finish/incoming; Tenma choose rules come as data from `tenma.py`), `T:build_raiden_{illusions,movement}.py` |
| S2-TENMA | `raiden_enc/tenma.py`, `T:build_raiden_{cinematic,arena}.py` |
| S3 | merges, balance constants, README "나루카미 보스전" section, `legacy_anim` and preset removal |
**No shared engine file is edited.** `combat/*`, `mob/*`, `view/tick`, `room/*` and `mboss/*` keep calling the
interface of current.md §5:
- ids `init`, `spawn`, `world`, `cleanup`, `bars_hide`, `incoming`, `death/start`, `object/on_hit`, `camera/hold`
  (now a no-op) and `test/{won,defeat}`;
- tags `rlk_raiden`, `rlk_rd_object`, `rlk_raiden_arena`;
- scores `rdPhase`, `rdPat` (5 = illusion hidden, 15 = 만겁 hidden, both immune), `rdBlink`, `rdDeath`, `rdCam`
  (kept, unused), `#rdTest`, `#rdBar`.

### E.1 Fast checks (per change, seconds) and when loadcheck runs
| change | check |
|---|---|
| encounter / hazards / FX | the touched generator (< 1 s) → `python3 -I S:rd/tests/test_raiden.py <dp> -k <ids>` (rdsim on the touched patterns: hazard set, hit ticks vs §B, cue → hit ≥ 12/20, decal policy per hazard vs §B.3, damage, max hits, cmds/tick; ≤ 3 s) → `check_raiden_pack.py` (0.5 s) |
| rig | `node build_raiden_rig.mjs` (target ≤ 8 s; its floor, step, element and px checks) → `rigtech_render.py` on the touched clips only (~1 s per panel) |
| sprites | `build_raiden_fx_textures.py --only <names>` → one FX render of the touched kinds |
| always (in `test_raiden`, < 1 s) | static 26.3 traps: no `scoreboard players (add\|remove) … -N`; no glyph font on the first text element; every `playsound` id is in the 26.3 registry (from `server.jar --reports`, cached in `S:rd/tests/sound_ids.txt`); no-tips lint; no `tp` of `@a`/`rlk_body` except arena-safe helpers |
| **loadcheck** | at each commit batch (≤ 1 per hour per agent), at stage end and before any delivery: `flock S:mcsrv/.lock bash S:mcsrv/loadcheck.sh <wt>/roguelike <tag>` → 0 failures. **Always use `flock`**: the script runs `pkill java` and shares one world, so two agents cannot run it at once. |
No full gate before S3.

### E.2 Stages (≤ 2 agents at a time)
| # | stage | slot | depends | deliverables | fast checks | est. |
|---|---|---|---|---|---|---|
| S0 | **Setup** | B | — | Worktree `S:rd/wt` on `wip/rd` from `claude/exciting-pascal-ek1vuy` (6f051b4); RP sandbox `S:rd/rp` (copy of the last delivered RP). Encounter split (byte-identical). `test_raiden.py` (rdsim promoted + static traps + a policy table `S:rd/tests/plan_table.json` transcribed from §B). `identjudge_rd.py` (Raiden-owned paths may differ, everything else equal to the release). `--only` flag. **Baseline**: current DPM per phase at Lv 12/18/24 (standing + dodger). Baseline loadcheck 0. | byte-identical rebuild, loadcheck | 1 h |
| S1-RIG | **Model + clips** | A | — (starts at once; branch `wip/rd-rig`, worktree `S:rd/wt_rig`) | C.1-C.5: both forms, props, 45 clips + manifest v2 events, `legacy_anim`, debug poses. **U1 sheet → user**: Shogun sword and polearm (front, side, back, 3/4); Tenma (front, 3/4, side, back); key poses (iai stance, twirl, guard, Musou raise, glaive sweep, Tenma iai crouch, 단절 raise); props (clap hands, vajras, flower + dome, eyes, clones); next to the footage crops `frames/B/B_v7_06.90…`, `B_v9_03.30…`, `frames/A/v1_12.50…` | rig build checks, renders, loadcheck at end | 6 h |
| S1-KIT | **Hazards + FX + reclaim** | B (after S0) | S0 | B.0 engine v2 (parametric shapes, travelling hazards, flags, decal/strike split, segment rings); the §B.3 decal sprites; reclaim (C.6) with the atlas print; strike visuals per shape; kit tests in `test_raiden` (each shape × quiet/decal, timing, `jump`, `nododge`, `detached`); old presets s1..s14 still work | kit tests, pack check, atlas print, loadcheck at end | 4 h |
| M1 | **Merge** (lead) | — | S1-RIG, S1-KIT | `wip/rd` = S0 + RIG + KIT; build_all; `test_raiden` (old patterns through `legacy_anim` + presets); loadcheck | as listed | 0.3 h |
| S2-SHOGUN | **Phase 0** | A | M1 | A.2, B.2 phase 0 (1-10, 21-28, guard/counters/카라타케/stuns, eyes, illusions + Musou, rear checks, range bag, blink, after-effects), §D.2 lines; per-pattern renders at hit ticks (internal) | `test_raiden -k` per id, pack check, loadcheck at end | 5 h |
| S2-TENMA | **Transformation + phase 2** | B | M1 | A.3-A.4, B.2 T and 11-20 (만겁 rework, vajra segment rings, travelling waves, rush), exhausted/`normal_return` hook (calls Shogun's forced switch through `core`), optional arena look (D.3), death | same | 5 h |
| S3-I | **Integrate + balance** | A | S2 × 2 | Merge; remove `legacy_anim` and unused presets/sprites; balance pass (B.1 ±15 %); README section rewritten (Korean: rule notes, new patterns, generators); `test_raiden` full | full `test_raiden`, loadcheck | 1.5 h |
| S3-R | **One review** (read-only) | B, in parallel with the S3-I gate run | S3-I | One reviewer covering fidelity vs footage (renders + §B), state/cleanup (pause, reload, transform, exhausted, death, test/stop with every phase × pattern), fairness (R1 tells, nododge list), R2 text, R3 traps. Output `S:rd/review/findings.json` | — | 1 h |
| S3-F | **Fix + final gate + release** | A | S3-R | Fixes, final gate (E.3) **once**, ff release, stamp "빌드 10-2x 라이덴", push, zips; **final sheet + summary → user** | final gate | 1.5 h + 0.3 h gate |
**Budget:** 8 agent runs, about 25 agent-hours, about **15 h wall** (S1 6 h → M1 → S2 5 h → S3 4 h). There is one
model checkpoint with the user (U1, not blocking: feedback is folded into S2/S3-F), and one review pass.

### E.3 Final gate (run once, about 17 min)
1. `build_raiden_all.py` × 2: the second run changes 0 bytes.
2. `check_raiden_pack.py`, `check_mboss_pack.py`.
3. `check_refs`, `check_macro`, `check_nbtpath`, `lint_mc`: no new Raiden findings. The `camera/end` false positive
   goes away with the camera lock.
4. `test_raiden.py` full: every pattern with both weapons, every transition, the stuns, cleanup (`rlk_raiden_aux`
   empty), budgets (C.4), the policy table, the static traps.
5. `test_chapter.py` (17 s) + `ident.py` with `identjudge_rd.py`.
6. `az/tests_cm/run_all.sh` (~10 min; covers the chapter 2-4 routing to Raiden).
7. `loadcheck.sh` (with `flock`): **0 failures**.
8. Atlas: stitched ≤ 11.0 M px and Raiden ≤ 3.5 M (target 3.0).
9. Final contact sheet.
`az/tests/run_all.sh` (29 min) runs only if a file outside the Raiden-owned set changed (none planned).

---------------------------------------------------------------------------------------------------------------------
## F. Risks and decisions

### F.1 Risks (handled inside the plan)
| risk | mitigation |
|---|---|
| Client lerp of travelling cards vs the server hit test drifting apart | Both launch on the same tick with the same kinematics; a kit test compares the card's position (from the written interpolation) with the hazard front at 3 ages. |
| The guard parry depends on `#icd` / `#skillDmg` being set by every player attack path (bows, catalysts, characters) | S2-SHOGUN checks this with one attack per character in rdsim. Fallback: parry all hits at ×0.25. |
| Longer timelines (eyes 140, Musou 166, vajra 310) make fights longer | The B.1 balance pass also reports time-to-kill; trim waits (vajra start, eye timers) first. |
| Too much going on at once with the after-effects (field lightning / blade eyes) | Suspended in 5 and 7; cadence 80 / 60 t is tunable in S3. |
| RIGLIB fast spins (twirls) and the 120° step limit | The compiler keys spins every tick; the step check fails the build instead of shipping a pop. |
| Two agents running loadcheck at once | `flock` (E.1). |
| ident pins Raiden to 22ba247 | `identjudge_rd.py` re-judges (S0). |
| Atlas reclaim falls short | Halve the 256² bolt sprites (−0.5 M) before S3's gate. |

### F.2 Decisions for the user (defaults are used unless the user objects; nothing waits on the answer)
1. **만겁 presentation.** The current camera-locked cinematic (rift + giant puppet arm + katana) is not in the footage,
   which shows a free camera and an arena-wide blade sweep. **Default: replace it with the footage version.** This
   removes 180 functions and 22 models.
2. **Undodgeable moves.** As the game and the guide video describe them, 돌진 (B-16), 수천수만의 염원 (A-15) and the
   guard-recovery burst ignore dash i-frames. They can be avoided only by distance, and their tells are ≥ 20 t.
   **Default: keep them undodgeable.**
