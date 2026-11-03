# Chapter-2 regular mobs — shared contract (lead, 10-28)

User request (Korean, verbatim): "2스테이지 잡몹을 만들거야. 원신이나 스컬, 세피리아의 몹들을 갖고와도 되긴 하는데, 너무 쉽거나
그냥 단순히 숫자만 많으면 지루할 수 있어. 정예 몹으로 움직임이 빠른 몹을 몇 개 넣거나, 패턴이 단순한 몹을 많이 넣어서 한 번에
여러 명을 때릴 수 있도록 해 타격감을 주거나 하면 좋겠어." Then: "특정 원소에 면역인 몹은 빼" (NO elemental immunity, NO
element-gated shields — every element damages every ch2 mob the same). Theme: Inazuma (Genshin) only. All 7 mobs. Chapter-1 mobs
are NOT mixed into chapter 2.

Two worktrees build in parallel and the lead merges:
- A = S/ch2/wt_a, branch wip/ch2-swarm, RP sandbox S/ch2/rp_a: the framework (routing, generator entry, shared hit feel,
  haste, test command) + 1 졸개 + 2 슬라임 + 3 창병 대열 + 7 북잡이.
- B = S/ch2/wt_b, branch wip/ch2-elite, RP sandbox S/ch2/rp_b: 4 카이라기·뇌전 + 5 그림자 닌자 + 6 시킨 술사 (+ 시킨).
(S = /tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad)

## Ids (fixed; both sides use them)
| id | mob | owner |
|---|---|---|
| ns | 떠돌이 무사 졸개 (one spawn call = ONE mob; A's pack spawner calls it 4-6 times) | A |
| sl | 번개 슬라임 (large) | A |
| ss | 작은 번개 슬라임 | A |
| sp | 반란군 창병 (one mob; the line spawner places 3) | A |
| dr | 오니 북잡이 | A |
| kr | 카이라기·뇌전 | B |
| nj | 그림자 닌자 | B |
| cc | 우인단 번개 시킨 술사 | B |
| ci | 번개 시킨 (summoned by cc only) | B |

- Spawn entry per mob: `rlk:cm/spawn/<id>` (same convention as chapter 1: at the caller's position/rotation, the new
  brain tagged `rlk_newmob` like ch1, level applied by the caller exactly as ch1 rooms / `cm/test_init` do).
- Group spawners (A): `rlk:cm/spawn/g_ns` (pack 4-6), `rlk:cm/spawn/g_sp` (line of 3), `g_sl` (2-3 large slimes).
- Test command: the existing `/function rlk:cm/test {t:"<id>"}` must work for every id above (and the g_* groups).
- Mob function roots: `cm/<id>/...` (B never writes outside `cm/kr|nj|cc|ci`, `cm/spawn/{kr,nj,cc,ci}`, its own generator
  module, its own rig/texture files and its own RP assets; anything else B needs from the shared framework goes into
  B's report as a request, or is written into B's own files).

## Generators (standing rule: never hand-edit generated outputs)
- All ch2 mob datapack files are written by `roguelike/tools/build_ch2_mobs.py` (A owns the entry). It imports
  `ch2mob/common.py` (A), `ch2mob/swarm.py` (A), and — if the file exists — `ch2mob/elite.py` (B). Each module exposes
  `build(w)` where `w(path, text)` writes a function under data/rlk/function/ and records it; the entry deletes stale ch2
  files it owns (only under the ch2 ids' folders) and prints a one-line summary.
  B: until A's entry exists in your tree, write a tiny local runner `roguelike/tools/build_ch2_elite_only.py` that calls
  `ch2mob/elite.py` the same way; the lead deletes it at merge. Keep `elite.py` free of imports from A's modules except
  through a small local shim you own (`ch2mob/elite_lib.py`), so the merge is file-disjoint.
- Rigs / skins / item models: their own node/python generators (B: `tools/build_ch2_elite_rigs.mjs`, A:
  `tools/build_ch2_swarm_rigs.mjs`), each adding its atlas sources idempotently (filter-then-push by id, like
  build_mobs.mjs). Resource ids lowercase `[a-z0-9_./-]` only. Texture budget: A ≤ 0.5 M px, B ≤ 0.5 M px stitched (the
  items atlas is at 11.6 M; client limit ~15.5 M).

## Shared behaviour both sides honour
- Framework: reuse the chapter-1 custom-mob structure (brain husk `rlk_cmb` + visual + lure `rlk_lure`, `cmId`, `cm/clean`,
  `cm/hit_pl*`, stun/freeze cancel rules, health bar, level scaling). Read README §5 / §5-1 and the cm/ sources first.
- NO elemental immunity, NO resistance tables, NO element-gated shield. Attacks may apply Electro to the player.
- Haste (drummer): while a 북잡이 drums, every cm mob within 10 b carries tag `rlk_cm_haste` (A sets/clears it each tick).
  Every ch2 mob (A and B) must: move 30 % faster (movement_speed attribute modifier with a fixed id, removed when the tag
  goes) and advance its attack cooldown / wind-up timers ×1.3 while tagged (e.g. +1 extra tick on 3 of 10 ticks — integer
  only, deterministic). Visual: a yellow aura particle on hasted mobs (A draws it for all).
- Telegraph rule: no floor decals unless stated below; every attack has a visible tell (glint/pose/glow + vanilla sound)
  ≥ the listed time; nothing undodgeable.
- No tutorial / "how to play" text anywhere (user rule).
- Real-game rules: no negative literals in `scoreboard players add/remove`; no teleports into blocks (ground/space checks
  like ch1), nothing below the floor, rooms' walls/doors never broken; text components never inherit a glyph font.
- Damage via `player/take_damage` path like ch1 (`cm/hit_pl`), raw values below, scaled by the existing level rule.

## Roster (raw numbers are first drafts; base = ch1 검사 HP 18 / hit 15)
A — swarm (hit feel: knockback resistance 0 instead of 0.5, hit stun 0.25 s instead of 0.1 s; death = fling back + pop
burst + kill sound; a multi-kill cue when ≥3 cm mobs die within 10 t: a heavy vanilla sound at the player + burst):
1. ns 떠돌이 무사 졸개: HP 8, packs of 4-6 that keep within 2-3 b of a pack leader. In range (2.5 b) the whole pack raises
   blades together (0.6 s, blade glint + sound) then a short slash, 15.
2. sl 번개 슬라임: HP 14, hops toward the player; crouch 0.5 s then body slam (12). Dies → splits into 3 `ss`.
   ss: HP 3 (one hit), fast hops, latches near the player then after 1 s a small shock (r 1.5, 6; a small electro ring
   tell on the floor around it is allowed). Any slime death discharges r 2 to OTHER slimes (6 % of their max HP... or a
   flat value tuned so a cluster of ss chain-pops) — never to the player.
3. sp 반란군 창병: HP 10, a line of 3 walking abreast; 1 s spear-tip glow, then all thrust-dash 2 b forward (16). Slow to
   turn (90°/s) so flanking works.
7. dr 오니 북잡이: HP 20, stationary; drums → haste (above) in r 10; any hit interrupts drumming for 2 s.
B — elites (normal ch1 hit feel; 1 per room at most):
4. kr 카이라기·뇌전: HP 70, fast. A: 3 zig-zag dash slashes (each 0.35 s glint tell, ~5 b, 14 each), then 1.2 s recovery
   (the punish window). B: electro-charged spin slash r 3 (0.8 s blade-glow tell, 18). Not staggerable while dashing.
5. nj 그림자 닌자: HP 45, very fast. Vanish in smoke → reappear 3 b behind the player (safe ground only) → 0.5 s glint +
   sound → slash (16). After 2 ambushes: 1.5 s exhausted (standing, punish window). At range > 10 b: 3-way shuriken fan
   (0.5 s tell, 8 each).
6. cc 우인단 번개 시킨 술사: HP 50. Summons 4 `ci` (HP 2, one hit) that orbit the player at ~4 b, then one at a time glow
   0.5 s and ram (8). If the player gets within 3 b: blink 6 b away (safe ground, 5 s cooldown). Max 4 live cicins; resummon
   when all are dead after a cooldown. cc dies → all its cicins vanish.

## Routing (A)
- Chapter 2 rooms use ONLY the ch2 roster (no ch1 mobs). Chapters 3+ keep today's behaviour (ch1 roster) until their own
  roster exists. `#mobTmp` keeps its meaning.
- Room composition by map order (1-6): 1-2 → two swarm groups (졸개 pack + slimes); 3-4 → 1-2 swarm groups + 1 elite (kr
  or cc), drummer sometimes (~35 %); 5-6 → 창병 line + 졸개 pack + 1 elite (nj, or any) + drummer (~60 %). Scale the
  counts with whatever the room's current mob-count rule is (keep total threat comparable to ch1 at the same level).
  A routes B's ids through a macro call (`$function rlk:cm/spawn/$(id)`), which is resolved at run time, so A's tree loads
  cleanly without B's files (a direct `function rlk:cm/spawn/kr` line would fail to load in A's tree). A must not create
  any file under B's ids.
