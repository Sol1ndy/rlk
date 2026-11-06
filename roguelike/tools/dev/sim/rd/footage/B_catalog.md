# B_catalog - Raiden (마가츠 미타케 나루카미노 미코토) patterns from v6-v9

Analyst B. Footage = authority for motion/timing/shape; wiki = names and mechanics.
Per-video logs: `B_v6.md`, `B_v7.md`, `B_v8.md`, `B_v9.md` (same folder).
Reference crops: `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/rd/frames/B/`.
Contact sheets: `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/rd/work/B/{sheets,dense,hi}/`.

Conventions
- t = Minecraft ticks (20/s), counted from the start of the named video. "tell" = first readable cue
  (motion, flash or sound) to the hit; all values come from 10 fps strips + 4-10 kHz SFX peaks (±2 t).
- Sizes in blocks: player = 1.8 b tall; the arena edge is never in shot, so radii are measured against the
  player and their distance to the boss (±25 %).
- "Floor decal" = yes only when something is drawn on the floor before the hit. Stance auras and
  volumetric glows are listed separately.
- v6->v9 look like one continuous guide recording cut into 4 chunks. The burned-in captions name each
  segment. Shogun (humanoid) patterns appear only in v6; everything from v6@39.2 onward is the Tenma form.
- BGM beat 0.455 s (~132 BPM); onsets on the beat grid were discarded as music.

## Pattern table

| id | wiki name (caption) | form | seen (video@s) | tell -> hit (t) | active / hit window | shape / size (b) | floor decal? | fx | avoidance | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| B-01 | 마가츠의 뇌안, single (마가츠의 뇌안) | Shogun | v6@0.0-1.0 | n/a (break target) | eye stays until broken | 1 eye orb ~0.6 b, ~1.5 b up, inside a flat purple lightning disc ~3 b dia | the disc is part of the eye object, not a telegraph | purple orb, eye glyph, lightning disc | attack it; breaking it stuns the boss (caption) | only 1 s shown, then a cut |
| B-02 | 마가츠의 뇌안, multi (마가츠의 뇌안 2) | Shogun | v6@1.05-8.9 | spawn pillars t22-28 -> blast t152-164 (~130 t). Cyan dome glow from t126 (~26 t before) | blast ~12 t | 3 eyes ~6-7 b apart (L/C/R), ~2-3 b up; each blast zone r ~5-6 b; the blast reached ~3-4 b behind the player | YES: thin purple circle on the floor around the eye, r ~5-6 b, from t30 | cyan-white light pillars at spawn; eye orbs with own HP bars; pale-cyan translucent hemisphere warning; violet lightning plus dark shard blast | break one eye, stand in its zone outside the others' rings ("하나를 골라 부수고 범위 밖에서") | the wiki's 광역 뇌안 |
| B-03 | 번개 배리어 / guard stance (방어) | Shogun (sword or spear) | v6@8.9-25.3 | passive | lasts the whole segment (~16 s shown) | parry flash = gold crescent ring r ~1.2 b around the waist on every melee hit | stance aura only: crackling purple ring on the floor under her, r ~1.5-2 b, always on (not an attack cue) | 5-orb halo arch over the head (centre eye emblem plus 4 tomoe orbs); gold parry crescent | ranged/elemental damage; melee is blocked | broken by accumulated damage (B-06). Wiki: weapon (sword/spear) is random per fight |
| B-04 | guard counter, sword (방어 "일정 확률로 카운터") | Shogun sword | v6@12.0-13.8, 15.8-19.4 | t0 = gold ring + black vertical line; +4 t pink 4-point star flash | burst +8..+16 t; floor bolts +20..+44 t; lunge +34..+70 t | 1) spin burst around her r ~2.5-3 b; 2) pink lightning bolts along the floor toward the player, line ~6-8 b; 3) lunge thrust line ~6-8 b through the player's spot | no | gold ring, black line, pink star, violet sphere, pink floor bolts, purple thrust streak | back off at the star; side-step the thrust | 2 instances; the gaps vary (A: 4/8/20/34 t; B: 4/12/44/64 t) |
| B-05 | guard counter, spear (방어 "창의 카운터는 바로 뒤쪽에도") | Shogun spear | v6@21.5-24.4 | parry t430/t442 + black line; star t448 -> sweep t466 (~18 t) | sweep t466-478 | 360 degree spinning spear sweep, r ~4-5 b, includes directly behind her | no (dark aura disc under her while crouched, t425) | dark-violet crescent ring trail | leave melee range in every direction | rear is NOT safe (caption) |
| B-06 | guard break -> stun (방어 파괴) | Shogun | v6@25.4-29.3 | shatter t508-512 after enough hits | stunned >= 70 t shown (cut at 29.3) | golden light pillar comes down on her (t522-532) | no | white-violet shatter burst, gold pillar, white sphere flash | free damage | wiki: break = long stun + resistance down |
| B-07 | stun-recovery knock-back (스턴 회복) | Shogun | v6@29.4-34.8 | floor ring ~20-35 t (t588->t610, t630->t670) | burst ~4-6 t | shockwave dome r ~4-5 b centred on her, knock-back, small damage | YES: glowing purple circle on the floor around her, r ~2.5-3 b | white flash, violet dome, dark crystal shards, floor crackle ~25 t | be outside ~5 b when the stun ends; undodgeable ("회피가 불가능") | seen twice |
| B-08 | phase change to 악요의 요고우 텐마 (변신) | Shogun -> Tenma | v6@35.0-39.1 | floor ring wave t702-712 -> pillars t714-726 | ~25 t of strikes | 1) lightning ring expanding along the floor from her (travelling front); 2) several white-violet lightning pillars (~1.5-2 b wide, sky-high) around the arena; 3) burst at her | the travelling ring itself only | lightning pillars; arena palette teal -> dark blue/violet at ~t740; puppet-arm body fades in t730+ | keep distance and dodge the pillars ("맞으면 더 아프지만 어렵지는 않습니다") | wiki: also comes with the electro shield/gauge mechanics |
| B-09 | 몽상 • 염원이 깃든 백안지륜 (3단 콤보) | Tenma | v6@39.2, v7@0.0-5.3, v7@6.9-17.5 | arm raise 12-16 t before slash 1 (#2 also had a blade glint 37 t before) | slash1 t17 / t179; slash2 +10..+20 t; throw +22..+45 t after slash 2; landing impact; explosion +50 t (#1) / +98 t (#2) after landing | slashes: horizontal glaive sweeps, ~180-200 degrees in front, r ~6-7 b. Throw: beam to a spot ~3 b from the player, impact r ~3 b. Explosion: r ~3-4 b at the planted spear | small floor sparkle/ring at the planted spear 9-18 t before the explosion (seen in #1 and #2) | pink-violet arcs, pink-white spear beam, planted glaive, white flash + dark ink burst | hug the boss's LEFT flank within ~2 b; leave the spear spot before it pops | caption: "검을 두 번 휘두르고 창을 던집니다 창은 잠시 뒤 터집니다" |
| B-10 | 번개 신의 신속한 발도 (발도) | Tenma | v7@18.8-21.0, v7@27.2-30.7 | crouch charge 20-22 t; white-pink orb flash -> hit 10 t (#1) / 22 t (#2) | instant; floor turbulence visual ~14 t | 360 degree horizontal disc slash at hip height, r >= 10 b (went past player and camera) | no (a thin bright circle expands at the boss right after the flash) | big white-pink flash orb at the hilt, violet disc sheet, lightning | dash through at the flash ("번쩍일때 대시"); i-frames | an approach slash arc came first in #1 (t376) |
| B-11 | 몽상 • 궤멸의 검기 (검기) | Tenma | v7@22.1-23.5 (near); v7@38.2 - v8@3.4 (far) | blade glint (v7 t780) -> slabs reach the player at ~11 b in ~22-26 t; wave 2 leaves ~45 t after wave 1 and needs ~40-45 t more to arrive | each projectile hits on contact | wave 1: 5 tall VERTICAL crescent slabs (~4-5 b tall, ~1.5-2 b wide) in a ~60 degree fan, ~9 b/s. Wave 2: one wide LOW crescent on the floor (~16-20 b span, ~1 b tall), slow ~5-6 b/s | no | translucent violet slabs with bright edges; low crescent with dark cracks | near: stay at the boss's left side; far: slip between slabs, dash through the low wave | wiki: first swing = 5 projectiles, second = slow strong projectile |
| B-12 | 몽상 • 단절 (단절) | Tenma | v8@4.4-9.9 | white halo ring at her t90 -> hit t162 (~70 t); band decal from ~t120 (~40 t) | slam t160-168; field t170-200+ | straight line slam along the band: width ~5 b, length >= 25 b (crosses the arena); lingering cracked field r ~4-5 b around her | YES: pale-violet translucent straight band from her feet through the player | blink-in streak, halo ring, sky lightning column, wall of light on impact, cracked glowing floor | step out of the band sideways or dash; avoid the near field | caption: "쇼군 근거리에 작은 데미지를 주는 장판" |
| B-13 | 흉장의 수안, clap variant (박수) | Tenma | v8@10.0-17.6 | summon t216-240 (spikes, dark sphere, flying orb); palm flash -> clap 12 t (#1), ~20 t (#2) | claps t274, t326 | two giant translucent purple hands (~4-5 b tall, ~3 b wide) flank the player 2-3 b away and follow; clap = dark burst sphere r ~3 b on the player | no | faceted violet hands; white 4-point star on each palm; dark-violet burst | dash out right after the palm flash ("손바닥이 빛날 때") | 2 claps seen |
| B-14 | 몽상 • 초월의 악요개안 (뒤 견제) | Tenma | v8@17.65-22.4 | glint flash t353 -> spin t366 (13 t); planted spear: floor ring t428 -> explosion t438 (10 t) | spin t366-372; throw t384-390; explosion t438-444 | 360 degree spin slash r ~6-7 b (behind included); spear thrown to the player; explosion r ~3-4 b; landing -> explosion 46-50 t | YES (small): bright white ring ~2 b dia on the floor around the planted spear | white-hot spin streaks, pink beam, white flash + violet burst | triggered when the player is behind her; get out of the spin radius, then away from the spear | same spear-bomb as B-09 |
| B-15 | 흉장의 수안, shadow variant (추적 손바닥) | Tenma | v8@22.7-27.7 | seed thrown t462; shadow follows ~56 t; it grows (and stops) t524-530 -> palm slam t535-539 (12-15 t) | DoT ticks every ~20 t while following (t491/513/532); slam t535-539 | follow pool ~3 b ellipse under the player; grown disc r ~4-5 b; giant pale-violet palm from above | YES: dark violet-black smoky pool that follows the player, then a large dark-magenta disc | dark seed with eye, ink eruption, lightning ticks "1101", falling palm, dark shards | dash out of the disc as soon as it grows ("그림자가 커질때"); the DoT is minor | wiki: the palm lifts the player and slams |
| B-16 | 번개 신의 강력한 돌진 (돌진) | Tenma | v8@27.75-31.0 | glint t555; white orb flash t568 -> dash t578 (10 t) -> first hit t583 | barrage t583-596 (5-8 hits) | rush ~10 b to the player, then a multi-slash storm ~6-8 b around the arrival point | no | white orb flash, motion blur, pink-white slash streaks and lightning | per guide undodgeable: never let the distance grow (~10 b triggers it) | killed the player in the footage |
| B-17 | 만겁 + 추모의 꽃다발 (즉사기) | Tenma | v8@31.9 - v9@2.9 | vanish t638-652; tint t656; flower t678 -> slash t790-800 (~112 t after the flower) | slash t790-800; dome shatter v9 t32-44 | arena-wide instant-death horizontal slash; barrier dome r ~8-10 b around the flower once the gauge is full | no shaped decal; whole floor/sky tinted pink-violet | magenta lotus bouquet with a small dark orb above; white light column; pale-blue dome; screen-wide white-violet blade; shatter shards | fill the flower's gauge (1 electro hit or 4 other-element hits, caption) before the slash; stand inside the dome | wiki: resets burst energy; multiplayer = marked player only |
| B-18 | 금강괴멸파 (caption 천수의 속박) | Tenma | v9@3.2-22.6 | 3 vajras driven in t82-100; first wave ~6 s later (t212-220). Each pulse: current runs down a vajra + a flash at its top ~0.3-0.5 s before | 6 single rings every 32-40 t (passing the player at t220, 260, 292, 316, 354, 386), then a triple at t404-420 | 3 vajras ~5-6 b apart round the centre, each ~3-4 b tall; each wave = expanding floor ring band ~1-1.5 b wide, ~0.5-1 b tall, ~15-20 b/s, out to the arena edge; final = 3 rings at once | YES: thin purple ring at each vajra base, r ~2.5-3 b (source marker); the wave itself is a floor band | purple crystalline vajras; lightning arcs between them; bright violet ring bands | jump or dash through each ring; final triple needs a dash-jump or 2 dashes; guide says stand near the wall | 6+1 matches the wiki (each vajra once, twice over, then all three) |
| B-19 | 순간이동 / movement | both | v8@4.3, v8@28.1, v7@18.8 | - | - | blink: pink-violet afterimage streak (~5-10 b); blink-out leaves dark crystal spikes; Tenma floats 0.5-1.5 b above the floor | no | afterimage streaks | - | Shogun moves on foot with lunges |

### Patterns named in the wiki but NOT in v6-v9
Shogun: 원류 4-hit spear combo, 뇌명 돌진 (sword/spear dash), 악요 명문, 판결의 검 (rear iai), 뇌전이 이끈 번개
(3 discs + slow slash), 수천수만의 염원 (spear spin + floor shockwave), 영원함의 꿈, 몽상 • 카라타케,
무기 변경 에이엔노 이카즈마 / 진세이무죠 (rain of bolts / eye spawns), 찰나의 포영 (4 clones, X-slash),
몽상의 일심 (orbs at the edge + time-stop slash). Tenma: 흉장의 수안 hand-follow is covered (B-13/B-15);
the electro shield and its periodic energy drain are not visible.

## Model (for a block-display rig)

Reference crops (all <= 960 px): `frames/B/B_v6_27.00_model_shogun_spear_halo.png`,
`B_v6_20.60_model_shogun_sword.png`, `B_v7_06.90_model_tenma_full.png`, `B_v8_09.40_model_tenma_front.png`,
`B_v8_24.00_model_tenma_lance.png`, `B_v9_03.30_model_tenma_hands.png`, `B_v8_12.60_model_clap_hands.png`;
props: `B_v8_35.00_flower_orb.png`, `B_v8_37.95_barrier_dome.png`, `B_v9_11.00_ring_wave.png`, `B_v9_07.60_vajra_floor_ring.png`.

### Form 1 - Raiden Shogun (humanoid, phase 1)
- Silhouette: slim woman, ~1.75-1.8 b (same height as the player). Stands on the ground; no floating parts
  except the halo.
- Hair: very long dark violet, a single thick braid hanging behind to the knees; small purple flower ornament.
- Outfit: lavender-white kimono top with a deep neckline, dark purple patterned obi/side panels, long purple
  sleeve on one arm, dark violet thigh-high stockings, red-orange tassel at the waist. Palette: #2b1d4a (dark),
  #8a5cc8 (violet), #e8ddf0 (pale lavender), #c0392b (accent).
- Weapons (wiki: random per fight): (a) katana ~1.3 b, near-black blade with a violet glow, held low in the
  right hand; (b) naginata ~2.2-2.5 b, dark shaft, single curved violet blade, held upright or across the back.
- Guard halo: an arch of 5 floating orbs ~0.6 b above and behind the head, ~2 b wide: centre = larger flat
  diamond "eye" emblem (~0.4 b, dark violet with a lighter tomoe spiral), plus 2 small tomoe orbs (~0.25 b)
  on each side. Plus a crackling purple ring on the floor (r ~1.5-2 b) in the guard stance.
- Motion: grounded stances; parries flash a gold crescent ring at waist height; counters are fast spins and
  lunges; stunned = slumped, weapon upright; blinks leave a violet afterimage.

### Form 2 - 악요의 요고우 텐마 (Tenma, phase 2)
- Core figure: the same woman (~1.8 b) in a darker armoured variant: black bodysuit with violet glowing lines,
  pale armour plates on hips/legs, dark tasset skirt; two dark curved crest/horn pieces behind the head
  (crescent shapes ~0.6 b, pointing up and out); a large dark DISC HALO behind head and shoulders
  (~1.6-1.8 b dia) with a violet tomoe-eye emblem at its centre and a thin outer ring. Floats 0.5-1.5 b above
  the floor, slow bob.
- Puppet arms (disembodied, no shoulders; pale lilac / pinkish lavender lacquer, about #d8b4e2 with #9a6fb0
  shading; ball joints; glowing violet eye sigils on the forearms):
  - 1 GIANT left arm (upper arm ~2 b, forearm ~2 b, hand ~1 b), rooted ~3 b up behind her left shoulder.
    It wields the main weapon.
  - 3-4 thinner right-side arms (~2.5-3 b each) in a fan rising up and to the right like a halo of arms; one
    holds a short dagger/spearhead pointing up; the hands are open or claw-like.
- Main weapon: a huge glaive/naginata held by the giant arm, usually horizontal across the front at hip
  height: dark violet shaft ~6-7 b long, glowing magenta edge line, single curved blade ~2-2.5 b, a round
  pink guard ornament. It is thrown (B-09/B-14) and re-forms in the hand.
- Two LARGE TAN HANDS (gauntlet-like, #c9a27a with darker bands) hover low in front of her, below her
  feet, palms up/forward, each ~1.2-1.5 b wide, a violet eye sigil on each palm.
- Envelope: ~8 b wide x ~6-7 b tall x ~4 b deep. Hit box = the woman; the arms are visual.
- Motion: the whole rig turns as one; the giant arm swings the glaive in wide flat arcs; spin attacks rotate
  everything 360 degrees; teleports with a pink streak; the crouched iai pose sheathes the glaive low by the hip.

### Summoned props
- Magatsu eye (B-01/02): small violet orb ~0.6 b with a diamond eye glyph and its own HP bar; cyan sky pillar
  at spawn.
- Clap hands (B-13): two translucent violet hands ~4-5 b tall, faceted, darker violet rims, fingers up,
  palms inward; a white 4-point star flashes on each palm.
- Slam palm (B-15): one pale violet-white hand ~4 b coming down from above.
- Planted spear (B-09/B-14): the glaive stuck diagonally in the floor, glowing.
- Vajras (B-18): 3 vertical violet crystalline spike bundles ~3-4 b tall with lightning between them.
- Memorial flower (B-17): magenta lotus/bouquet ~1.5 b on the floor, a small dark orb above it; then a
  translucent pale-blue dome r ~8-10 b.
- Arena look: phase 1 teal shallow-water floor with ripple texture and a pale sky; from the transformation on,
  a dark blue/violet sky and floor with a teal aurora.

## Open questions
1. Spear-bomb delay: landing -> explosion 50 t (v7 #1) and 46-50 t (v8 뒤 견제) but 98 t in v7 #2. Is the
   timer ~2.5 s, with v7 #2 delayed or edited?
2. Iai flash -> hit was 10 t once and 22 t once. Fixed or random delay? The charge start -> hit was ~22 t
   both times.
3. Guard counter (B-04/B-05): the wiki names (몽상 • 카운터 어택 / 판결의 검 / 카라타케) do not map cleanly.
   Which name, and is the floor-bolt + lunge part of the counter or a separate follow-up?
4. Multi-eye blast (B-02): the cyan dome may mark the danger zone or the safe zone. The footage only shows that
   the player near the broken eye's spot was safe. Is the blast per eye (r ~5-6 b each)?
5. Arena radius: never visible. The iai disc (r >= 10 b), the 단절 band (>= 25 b) and the vajra rings
   ("to the wall") need the project's arena radius.
6. 돌진 trigger distance (~10 b observed) and whether the barrage is truly undodgeable in our version.
7. Number of claps (2 seen) and hand follow speed.
8. 단절 lingering field: radius ~4-5 b and duration >= 30 t seen (it was still there when the clip cut).
9. Transformation hit: is the pale sphere seen near the camera (v6 35.15) an expanding hit shell, or a
   party shield?
10. Only Tenma patterns and two Shogun mechanics (eyes, guard) are in v6-v9. The other Shogun-phase attacks
    exist only in the wiki (and possibly in analyst A's v1-v5).
