# S2d requests (wip/hr-s2c = 4e46cd7, S2d fix round 3 over 10e4467 (fix round 2; fix round 1: 6feefb6 + c048830 over c070a59); for the lead's merge into wip/hr)

S2d puts 홍련 on the player avatar's body (head top 2.00, hat crown 2.30 (m), brim Ø 1.32, sword 1.94, scabbard 1.52;
registry scale 1.0, hit 1.2 × 2.4). WT has no kit (api.K off), so these WH-only items still draw / place the 2.55-b S2a
figure. Line numbers are WH bd8c52d (I1b round 1) unless marked 4c81817 (I1b round 2, WH's head now); each item quotes the
old text — find it by the text if lines moved.
(m) = S2d's measured value from its build (tools/scarlet_rig_manifest.json `dims`); the lead keeps it in sync if S2d is rebuilt.
Fix round 1 (11-05): the worn hat sits on the head (its brim 0.502 above the neck, level; the crown's bottom 0.013 over the
head's top): HAT_TOP 2.36 -> 2.30, the hit box 2.5 -> 2.4; her intro rise moves her off the seat stone (seq.py, s2d-7).
Fix round 2 (11-05): the user's skin is a SLIM skin (3-px arms), so her arms are now the player avatar's own slim arms (3 x 12 x 4
px, shoulder pivots +-0.34375 instead of +-0.375; tools/arlecchino_geometry.mjs P1_SPECS = build_player_rig.mjs): s2d-1's arm
shapes follow. No contract value changes (HEIGHT 2.00, HAT_TOP 2.30, hit 1.2 x 2.4, BRIM_D 1.32, the sword / scabbard / item
lengths are as before). New since round 1: s2d-3's test_kit VARIANTS bullet, s2d-6's walk-distance lines, s2d-7's conflict
recipe for the generated files.
Fix round 3 (11-05): rig-only (the elbow is a hinge; the compile keeps what ships near the solved frame after every first key;
g_dive takes blend 1 because it starts from the hidden rig; the crown lid square 0.005 wider) plus two stand-in anchor values in
core.py (s2d-7). No contract value, clip timing / event / name or WH-side request changes; s2d-1..6 stand as they are.

s2d-1 Kit afterimage = the player-size figure (MUST: the S2a silhouette brings the old long limbs back in every P2 leap / dash /
      blink and the CS1 / CS4 dashes).
  - T:mboss_hr_fx_paint.py:513-553 paint_afterimage and :556-570 paint_inside: replace the S2a shapes (keep the rim / colour code,
    the 64 x 128 sprite and the box a -0.25..0.25, b 0..1; api.KIT_SPRITES frozen):
        AI_S = 2.65        # >= HAT_TOP + 0.05 and >= 2 x BRIM_D (the brim fits the card's half width 0.25 x AI_S)
        x = a * AI_S; y = b * AI_S          (both functions; blocks, feet at 0, +x = her sword (left) side as before)
        brim   abs(y - 2.00) < 0.035 and abs(x) < 0.66
        crown  2.00 <= y <= 2.31 and abs(x) < 0.25
        head   1.49 <= y <= 2.02 and abs(x) < 0.28              (square)
        torso  0.74 <= y <= 1.50 and abs(x) < 0.265
        legs   0.00 <= y <= 0.75 and 0.01 < abs(x) < 0.265      (two legs)
        arms   seg_dist(x, y, -0.344, 1.40, -0.39, 0.78) < 0.11 ; seg_dist(x, y, 0.344, 1.40, 0.42, 0.86) < 0.11
               (fix round 2: her slim arms, 3 px + the sleeve layer = 0.11 b half-width, shoulders +-0.344)
        sword  seg_dist(x, y, 0.42, 0.86, 0.63, 0.10) < 0.022     (paint_afterimage only, inside = max(inside, 0.9))
    docstring (:514-515): "... the player-size figure (S2d): 2.0 b to the head top, the hat crown 2.31, feet at b 0, 2.65 b
    tall at scale 2.65". (AI_S stays 2.65: >= HAT_TOP 2.30 + 0.05 and >= 2 x BRIM_D 2.64.)
  - T:build_mboss_hr_fx.py:964 card('afterimage', '~ ~$(oy) ~', bb='vertical', s0=2.8, s1=2.8, …) -> s0=2.65, s1=2.65.
  - Keep AI_CLAMP (:954, -120: the card's feet at her feet) and S3's call at the body + 1.2 (p1.py:47).
s2d-2 Kit seat stone and its items (MUST: from the 0.75-b stone her 0.77-b legs would leave the floor; the items must stand
      where her hands set them down / pick them up).
  - T:build_mboss_hr_fx.py:1339-1341 SEAT (offsets in the stone's ^left ^up ^forward frame; the stone faces her facing):
        'rock':   ('minecraft:tuff', (0.0, 0.375, 0.0), (1.5, 0.75, 1.1))  -> ('minecraft:tuff', (0.0, 0.12, -0.185), (1.2, 0.24, 0.64))
        'bottle': ('minecraft:potion', (0.45, 0.75, 0.05), 0.5)            -> ('minecraft:potion', (0.42, 0.24, -0.15), 0.42)
        'cup':    ('minecraft:bowl', (-0.4, 0.75, 0.2), 0.42)              -> ('minecraft:bowl', (-0.42, 0.24, -0.15), 0.26)
    The stone: top 0.24 = her thighs' underside (hip 0.385 (m)); front face 0.135 b in front of her anchor (clear of her
    shins), back face 0.505 behind. Item scales match the rig's bottle (0.30 tall) and cup (Ø 0.15); check in the merged
    intro render (if the stone sits in front of her heels, the local z sign is the other way: negate the three z).
    Fix round 1: she leaves the stone without stepping into it — seq.py (WT) glides her 0.4 b forward over the rise (214-226)
    and 1.1 b to her right (226-246, before the turn), so the stone must stay where this item puts it (behind her heels);
    test_rig.py's "seat stone" check models those glides and the turn.
  - :1332-1334 PROPS['seat_rock'] doc: "1.5 x 0.75 x 1.1 b, its top 0.75 b over the display" -> "1.2 x 0.24 x 0.64 b, its top
    0.24 b over the display (under her thighs, behind her heels)".
  - T:dev/sim/hr/tests/test_kit.py:506  check(it.pos[1] >= d.pos[1] + 0.7, …)  ->  check(it.pos[1] >= d.pos[1] + 0.19, …).
  - T:mboss_arena_hr_field.py:834 SEAT_CLEAR = 1.8: keep.
s2d-3 Kit preset docs and test heights (SHOULD; S2d's new call heights, rule K x 0.78):
  - T:build_mboss_hr_fx.py docs: :750 qi_arc "the body + 1.3" -> "1.0"; :763 qi_ring "1.0 / 2.0" -> "0.8 / 1.55"; :825 qi_vert
    "the body + 0.2" -> "0.15"; :839 qi_fan "the body + 1.1" -> "0.85"; :848 qi_wedge "1.3 / 1.1" -> "1.0 / 0.85"; :859 qi_ribbon
    "1.3" -> "1.0"; :872 qi_line "1.2 / 1.0" -> "0.95 / 0.8"; :883 qi_cut "1.0" -> "0.8"; :913 yellow_tell "1.3" -> "1.0"; :923
    ghost_burst "1.0-1.4" -> "0.8-1.1"; :935 ghost_trail "0.6-1.2" -> "0.45-0.95"; :948 ghost_flash "the body + 1.0" -> "0.95" (its only call is
    p_ghost.py at_body(0.95), G1); :764 qi_ring's vanish "the body + 1.0" -> "0.8" (p_ghost.py at_body(0.8), G12); :971
    blink_bubble "1.3" -> "1.0"; :978 shield_refill "the body + 1.4" -> "1.1" (the refill runs through seq.py's me() default);
    :1145 petals_wind "her + 1" -> "0.8"; :1196 leaves_swirl "her + 1.4" -> "1.1". Unchanged: :775 qi_band (at the player).
  - T:dev/sim/hr/tests/test_kit.py:383-392 HEIGHT: qi_arc (1.0, 0.3), qi_ring (0.8, 0.1), qi_vert (0.0, 0.15), qi_fan (0.85,),
    qi_wedge (0.85, 1.0), qi_ribbon (1.0,), qi_line (0.95, 0.8), qi_cut (0.8,), yellow_tell (1.0,), ghost_burst (0.8,),
    ghost_trail (0.45,), ghost_flash (0.95,), blink_bubble (1.0,), shield_refill (1.1,), petals_drift (1.1,), petals_wind (0.8,),
    petals_heart (1.1,), leaves_swirl (1.1,), ev_leave (1.1,); every other entry unchanged (afterimage (0.0, 1.2) stays).
  - T:dev/sim/hr/tests/test_kit.py:396 VARIANTS 'qi_fan': [{'h': 16}] -> [{'h': 13}] (A1's new call, p1.py:95-96 `^ ^0.85 ^1.2`,
    h=13); for consistency :399 'qi_vert': [{}, {'yaw': 90}, {'h': 24}] -> [{}, {'yaw': 90}, {'h': 19}] (A7's new call,
    p_ghost.py:693-694). MUST with the HEIGHT edit above: without the qi_fan variant edit the new HEIGHT 0.85 fails 20 checks
    ('qi_arc_0..3 reaches -0.135 b below the floor': a 1.6-b fan centred 0.85 b up); with it test_kit passes 10594 / 10594 (the
    couplings verifier's scratch merge of c048830 into 4c81817).
s2d-4 Kit effect sizes that enclose her body (optional, x 0.78; keep yellow_tell, a gameplay tell): T:build_mboss_hr_fx.py
      :973 blink_bubble s0 1.8 / s1 3.0 -> 1.4 / 2.4; :929-930 ghost_burst s1 2.2 / 2.0 -> 1.7 / 1.6; :950 ghost_flash s1 2.4 ->
      1.9; :908 star4 s1 1.7 -> 1.3 (and its doc :905 "1.7 b" -> "1.3 b"); :865 qi_ribbon s0 1.5 / s1 1.9 -> 1.2 / 1.5; :940 / :942 ghost_trail 3.6 / 4.0 -> 2.8 / 3.1;
      :1262 ev_leave spread (0.6, 1.2, 0.6) -> (0.5, 0.95, 0.5) (and its doc :1259 "0.6 / 1.2 / 0.6" -> "0.5 / 0.95 / 0.5"); :1203 leaves_swirl dust spread (1.2, 1.0, 1.2) -> (1.0, 0.8, 1.0).
s2d-5 Suites (HR/tests is the shared working copy; WH's copies are newer for ev_dry / test_kit / test_scarlet):
  - test_rig.py: WH T:dev/sim/hr/tests/test_rig.py == HR/tests/test_rig.py before S2d (checked at bd8c52d): take S2d's
    HR/tests/test_rig.py (diff first; if WH's copy changed since, merge both sides).
  - ev_dry.py: do NOT copy the file. Apply S2d's edits to WH's copy by content: `(tr.get('scale') or [1.5])[0]` ->
    `(tr.get('scale') or [seq.S0])[0]`; `0.737 * sc` -> `seq.SWORD_R * sc`; and append S2d's "S23 toss offset" check block
    (HR/tests/ev_dry.py, marked "# S2d").
  - test_kit.py: the two edits of s2d-2 / s2d-3 in WH's copy; then copy WH's ev_dry.py, test_kit.py, test_scarlet.py AND
    lib/hrsim.py back to HR/tests (diff lib/ first: WH's test_scarlet.py calls hrsim's kit_on / kit_ex, I1b round 1) so the
    working copy equals the repo copy (I2's rule).
  - test_scarlet.py skip (I2, lead decision 1): re-run it after the merge — S2d's rise / aside glides (s2d-2, s2d-7) start her
    walk 0.4 b further from `start` and 1.1 b aside; estimate 6.75 b at the walk's end from a player at `start` (26.73 + 0.4,
    then sqrt(27.13^2 + 1.1^2) = 27.15, minus 17 legs x 1.2 b), inside I2's 7.05 b.
s2d-6 README (WH), the 「홍련」 section:
    (lines at 4c81817; round 2 moved them +1 from bd8c52d)
    :1997 "허스크(크기 1.35, 클릭 판정 1.2 × 2.9" -> "허스크(크기 1.0, 클릭 판정 1.2 × 2.4"
    :2099 "무릎 높이 돌" -> "낮은 돌(윗면 0.24칸)"
    :2100 "바닐라 응회암 1.5 × 0.75 × 1.1칸" -> "바닐라 응회암 1.2 × 0.24 × 0.64칸"
    :2136 "그림자(0x40, 반지름 0.9)" -> "그림자(0x40, 반지름 0.6)"
    :2135-2147 the rig item ("- **리그**" … "함수 2 629개(6.57 MB; 키 파일 2 109).": S2a's, or S2c's after I2) -> S2d's
      fragment HR/s2d/readme_rig.md (sizes: 머리 끝 2.00칸 · 갓 꼭대기 2.30칸 (m), 테 지름 1.32칸, 칼 1.94칸 · 칼집 1.52칸,
      and S2d's budgets)
    :2164 "돌 윗면 0.75칸 = 앉은 그녀의 골반 0.96칸 아래" -> "돌 윗면 0.24칸 = 앉은 그녀의 허벅지 아랫면(골반 0.385칸)"
    :2102-2103 (the intro walk; fix round 1's rise / aside glides): "일어나 돌아서서" -> "일어나 달 쪽으로 0.4칸 나선 뒤 오른쪽으로
      1.1칸 비켜서서(발을 옮겨 딛으며) 돌아서"; "약 6.3칸에서 멈춤" -> "약 6.8칸에서 멈춤" (the I2 test_scarlet `skip` measure
      in the couplings verifier's scratch merge: the full intro 6.76 b from a player who stays at `start`, the skip 6.50-6.76 b;
      I2 limit 7.05)
    keep :2148-2149 (item_sword, no size), :2154 and :2170. RP README: S2c's fragment -> HR/s2d/rp_readme_rig.md. README
    0-4's RP block: nothing new (no file or atlas entry added; only the hair models and their ghost twins are dropped).
s2d-7 Merge notes. S2d touches: registry :156; api.py :39, :453-454 + one new line after :454 (WH :455-456 +1; I1b's api hunks
      are elsewhere); core.py :113-114, :965-967, :982 (WH :1002-1004, :1019); seq.py WT :88, :255, :330-339, :401, :403, :509,
      :565, :567, :635, :650 (WH bd8c52d :88, :269, :344-353, :418, :420, :526, :583, :585, :653, :668); s3lib.py :151, :154;
      p1.py (identical in both trees); p_ghost.py (WH = WT + 1 after :640); scarlet_cine.mjs :13 (import) and :49 (HIP_DIR)
      only; scarlet_clips.mjs :353-355 only (fix round 3: g_dive's options get `blend: 1` + a 2-line comment; WH's file is
      byte-identical to S2c's, so it merges clean); new tools/scarlet_retarget.mjs. Fix round 3 also changes core.py's
      stand-in ANCHOR_OFF (:965-967 = WH :1002-1004, already in the core.py list): take S2d's lines ('hand_r' (-0.45, 0.8, 0.0),
      'hat_crown' (0.0, api.HAT_TOP, 0.15); the built idle-t0 anchors rounded to 0.05). No generated output depends on it while
      the rig manifest exists.
      WH moved to 4c81817 (I1b round 2). A trial merge (`git merge-tree --write-tree --name-only 4c81817 <S2d>`, the couplings
      verifier) conflicts in core.py :113-114 (the spawn comment: keep S2d's "husk scale 1.0, click" / "shield 1.2 x 2.4" with
      round 2's {api.xyz(seat)}) and in ~75 GENERATED files: data/rlk/function/boss/scarlet/p/** (the particle fallback heights
      against I1b's kit lines), boss/scarlet/seq/event/**, boss/scarlet/seq/intro/** (including rename/rename and rename/delete of
      the intro tick buckets seq/intro/b/*), boss/scarlet/spawn and mboss/register. Recipe: resolve core.py as above; for every
      generated file take either side (e.g. `git checkout --theirs -- <path>`, or `git rm` for the rename/delete leftovers), then
      rebuild the rig into HR/rp_hr (`node tools/build_scarlet_rig.mjs --resourcepack <HR/rp_hr>`) and run HR/tools/regen_d0.sh
      (build_mboss_core.py and build_mboss_scarlet.py rewrite them all), then `git add -A`; never hand-resolve a generated file.
      Every source but core.py auto-merges (seq.py too: SEAT_RISE / SEAT_ASIDE beside I1b's `..70`). The verifier's trial: no
      conflict marker left; the rebuilt rig and manifest equal the S2d commit's byte for byte; check_mboss_pack 0.
      Fix round 1 adds to seq.py: the CS0 header's SEAT_RISE / SEAT_ASIDE constants (WT :221-224, before `def build_intro`) and
      the rise / aside glides after the cup_down line (WT :242-247 = WH 4c81817 after :251), 5 lines above the walk-leg rule
      that I1b changed (`#mbDist ..81` -> `..70`, WH :257): git may join them into one conflict hunk — keep both (S2d's lines,
      I1b's `..70`).
      Fix round 2 adds to seq.py only two comment lines in the CS0 header (the rig's feet step with the aside glide; no code
      change); its sources are the rig's (scarlet_geometry / pose / retarget / skin .mjs, build_scarlet_rig.mjs, scarlet_rig_api.md),
      every other change is the regenerated rig tree and manifest. The suites: take HR/tests/test_rig.py again (s2d-5).
      Hold I2 (the S2c merge) until S2d's commit: I2's last step removes HR/wt_s2c and HR/rp_s2c.
