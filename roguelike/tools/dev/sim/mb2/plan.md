# Mid-boss 2: 달빛 환영 나비 (title 달빛의 화신) — binding decisions

Sources: videos `mb2/src/v1..v4.mp4` (continuous, in order); description `mb2/src/guide.pdf` (namu wiki, 3 pages).
Research outputs: `mb2/understand/v1..v4.md`, `mb2/understand/model.md`, `mb2/code/reuse.md`.

## User requirements
1. Use the videos and the PDF as reference. "모델링에 공을 들여서 만들어줘": put real care into the model, the same standard as the Corrupted Guardian. Send renders when the model is done.
2. "기본적으로 있는 불, 풀 내성은 없애줘": the boss has NO extra Pyro or Dendro resistance (in Genshin it does). It uses base RES only.
3. "디버프 해제할 때 '풀피 회복' 말고 그냥 회복만 돼도 해제되게 하자": the 달빛 고치 debuff is removed by ANY healing the player receives, not only by healing to full HP. Removing it grants the PDF's reward buff (CRIT +15 %, DMG +50 %).
4. It is registered in the mid-boss registry: a random mid-boss is picked, and killing it gives the item boxes, like the Guardian.

## Framework decisions (from code/reuse.md)

### Registry
- Entry fields:
  - id `butterfly`, n 2, el 7 (Dendro), w 10, minCh 1, maxCh 99;
  - name `달빛 환영 나비`, sub `달빛의 화신`, colour `#B6E35A`;
  - hp 240, xp 30, atk 12, dmgMul 110, goldMul 5, sap 1, picks 2;
  - scale 1.4, hit about 1.6×3.0 (resized in butterfly form);
  - intro about 140, death about 100, deathSnd false;
  - icon: a lime/white item.
- Keep `enabled: false` until every hook exists, then turn it on.
- Random pick between the Guardian and the Butterfly is weighted 10:10.

### RES and elements
- mres 0 and no per-element RES; incoming never checks #elem for reductions. An mcsim test locks in that #elem 0/1/7 hits deal equal damage.
- Boss hits apply their element through the existing #cmEl path:
  - human kicks: Dendro;
  - butterfly patterns: Dendro or Pyro, per pattern.
- **Burning weakness (PDF):** in butterfly form, any Pyro or Dendro hit from the player puts her into the Burning state, even without the other aura (start or refresh the existing burn DoT, reaction 10 machinery). Human form uses the normal reaction rules.

### Shared rig code
- Move the generic Guardian rig libraries into shared `tools/mboss_rig_*.mjs` modules, leaving re-export shims in the old files:
  - guardian_rig_math and guardian_paint_lib;
  - the generic parts of guardian_geometry, guardian_clips (retime/sampling), the rig compiler and the screen-font engine.
- Prove the Guardian rebuild is byte-identical (datapack + RP).
- Python AI/api helpers are copied and renamed (`#bf*`), not refactored.

### One rig for both forms
- A single superset rig of at most 34 item_displays.
- Wings and tendrils sit at scale 0 in human form.
- Props (cocoon, wrapped pod, orb sphere, ring cage, crescents, blades) are separate entities.
- Hitbox resized per form.

## Butterfly-specific decisions

### Forms and rotation
- **Entrance (cocoon):**
  - A wrapped-wing cocoon hovers over a glowing lime floor disc. At t57 the nameplate appears.
  - Glow 18 t, then an 8 t whiteout, then it bursts into white/cyan crystal shards at about t79.
  - She drops from about 4 b up, lands about t90 and stands at about t106. No damage. The fight starts after that.
- **Human form (인간형):** patterns come from a range-band shuffle bag (as the Guardian's): melee ≤4 b / mid / far ≥8 b.

  | id | name | bands | timeline (ticks) | damage |
  |---|---|---|---|---|
  | H1 | 달빛 발차기 | melee, mid | burst-run about 4 b in 5 t; hit 1 rising flip-kick crescent at t8 (front arc r about 4, tall); backflip; 12 t sideways-hop wind-up; flying leap; hit 2 axe-kick crescent at t40 (r about 5) plus a ground wave line 6×2 b; total about 51 t | 1.0, then 1.2 |
  | H2 | 달빛 점프 | melee, mid | arm shard glows lime as the tell (13 t); 360° low sweep r 3 at t13-19; spiral jump at t33 toward the player (3-4 b); orb at her foot; star flash; Dendro disc kicked onto the player position locked at t40, impact t50, r 2.5; total about 65 t | 0.9, then 1.4 |
  | H3 | 달빛 돌진 | mid, far | mote charge 10 t; dash about 5-6 b in 2 t; kick plus Dendro ring r 3.5 at t15; total about 50 t | 1.3 |
  | H4 | 광폭한 진공 | far, mid | crouch 9 t; spike and glint tell; vertical crescent blade (3 wide × 4 tall) launched at t17 along the locked line at 0.7 b/t to the arena edge, no homing; backflip, airborne 21 t; total about 41 t | 1.2 |

  - Human locomotion is grounded:
    - short strafing steps;
    - burst-runs (12-16 m/s, about 5 t) to close in before melee patterns;
    - backing off at walking pace.
- **Transformation (human → butterfly)** happens when the human-form timer expires at a pattern boundary:
  - first time: after 600 t of fight or 5 human patterns, whichever comes first;
  - after each groggy: after 4 human patterns.

  Sequence (about 30 t, a service pattern):
  - the cocoon glows;
  - the folded wings open over 8 t;
  - a light sphere of r 2.5 appears, then ripple rings of r 4-5;
  - the wings are fully spread.

  **달빛 고치** is applied at the light-sphere moment (see Debuff below).
- **Butterfly form (나비형):** she always hovers (toes at +1.2 b), glides at 4-8 m/s, dives at 12-15 m/s, and keeps 6-8 b for the Pyro patterns. Before each pattern the wing element switches in 1 t, 5-12 t ahead: Dendro = lime/opal textures, Pyro = orange-gold with magenta rims.

  | id | name | element | timeline (ticks) | damage |
  |---|---|---|---|---|
  | B1 | 우아한 날개 / 날개 치기 | Dendro | bank 8 t; dive 3 t; wing-arc hit at t15 (front arc r 4, plus a ground slash band and a trailing crescent); climb/flutter recovery; total about 55 t | 1.3 |
  | B2 | 화염 날개의 습격 / 날개탄 | Pyro | 4 spinning wing swings at t0/26/64/89; each throws 5 fire crescents that fan out, then dive onto the player position, 14-18 t later at 0.6-0.75 b/t; each crescent has a 1 b splash and a ground marker; one hit per swing at most; total about 117 t | 0.5 per crescent |
  | B3 | 날개 휩쓸개 / 날갯짓 | Pyro | 2 big flaps and a rise (20 t); head-first dive (4 t); wing slam at t26; 180° front flame fan (r 4.5, 2.5 tall) active t28-32; then a low glide leaving a flame trail (0.3 per touch, max 2); total about 59 t | 1.6 |
  | B4 | 달빛 축복 / 2단 코코볼 | Dendro | wing-wrap charge; orb 1 (a 1.7 b lime sphere with gyroscope rings) launched at t19; cocoon ball 12 t; orb 2 at t46. Orbs fly slowly and home strongly (PDF): they steer toward the player for about 40 t, then burst with radial ground blades r 2.5-3. A dash dodges them. Total about 76 t plus orb flight | 1.5 per orb |
  | B5 | 달빛 해제 / 강화 해제 | Dendro | the finale after 4-5 butterfly patterns or 900 t of butterfly form. Wings fold up; swoop past the player; climb; mid-air whirl with a lime 4-point star flare (20 t); wings cup forward (E-22); ground flash; cyan X glint; lime gyroscope ring cage r 4 (E-15..-10); wings wrap into a pod (E-9..-1); detonation E at about t53: a white flash and a lime dome of r 10 b. Dodge by being farther than 10 b or by dashing (i-frames) at E. She hovers about 2 b up for about 37 t, the wings shrink, go flat lime and shatter, she reappears in human form at E+39 and lands at E+43 | 2.6 |

  - **Groggy:** after B5 she reverts to human form and is groggy for 300 t (15 s): motionless idle, back turned, no tracking, no attacks. Then she turns (24 t), the crescent chain re-forms (18 t), and the human rotation resumes (the video goes straight into H2).
- No HP phases; the rotation is purely time and pattern based.
- **Telegraphs:** every damaging hit has at least 10 t of readable telegraph (ground decals or crescent tells). Video timings are used otherwise. **Superseded by the telegraph rule of 10-20 (end of this file): no ground decals; the 10 t tell is read from her motion and sound.**
- Arena: the shared plaza arena r 21. Check that the butterfly wing tops (about 6.7 b while hovering, up to about 10 b when climbing) clear the barrier cap, or keep her climbs lower.

### Debuff 달빛 고치 (adapted, binding)
- **Applied** at the transformation light sphere to the player:
  - 20 % of current HP as non-lethal damage (floor 1, no element). The video shows 17 % of current HP; the PDF says 40 %. 20 % is the middle ground;
  - while active: player outgoing DMG -50 %, CRIT rate -100 % (forced crits from engravings are undone too), healing received -40 %;
  - a HUD icon (a maroon badge with a salmon swirl, #8C525C) next to the bossbar sub-line, and the hint "달빛 고치 — 회복하면 해제".
- **Removed by ANY heal** (user decision): the first heal event with amount > 0 through player/heal → items/hook/on_heal removes it. The heal itself is still reduced by 40 %.
- **On removal:** a gold beam down, a gold burst and a gold emblem with sparkles (about 20 t), plus a chime. The reward buff 달빛 축복 받음 gives CRIT +15 % and DMG +50 % until the next 달빛 고치 application or the end of the fight.
- **Cure in the arena:** few characters heal, so when the debuff is applied, 3 glowing "달빛 이슬" (moon dew) heal orbs appear at random spots 6-14 b from the arena centre. They reuse combat/heal_orb_spawn2 or a module copy with a moon look. Touching one heals 8 % max HP and so cures the debuff. Uncollected orbs vanish when the butterfly form ends (B5). If the player is still debuffed after B5, one new orb appears during the groggy.
- **Cleanup:** the debuff and the buff are cleared at fight end, on death, on abort and on uninstall. Shared code edits are limited to items/hook/on_heal and items/hook/stat_buffs (crit), plus the module's own incoming/outgoing hook.

### Death and voice lines
- Death (not in the footage):
  - she staggers and the wings (if any) shatter into lime/opal shards;
  - she kneels;
  - she dissolves into rising moonlight motes and white-cyan crystal shards, about 100 t;
  - no creature voices.
- No voice lines: she is a creature. Short typed captions are used only for mechanics: the debuff hint on application and "달빛 해제" before B5.

### FX and sounds
- **FX:** lime #B6E35A / opal / cyan crescents and dust, using the tinted card engine.
- **Pyro:** orange-gold #FAD77C → magenta #C680A2.
- **Sounds:** vanilla only, composed per the video audio notes in v1-v4.md.

### Rig clips (the contract between the rig and module agents)
Names and lengths in ticks. Event ticks are relative to the clip start. They can be retuned, but the modules read them from the manifest.

| clip | length | key events |
|---|---|---|
| `idle_h` | loop 40 | |
| `step_h` | loop 16 | |
| `run_h` | loop 8 | burst-run |
| `back_h` | 12 | |
| `turn_h` | 24 | |
| `kick_combo` | 51 | hit1 8, hit2 40 |
| `kick_jump` | 65 | tell 0-13, sweep 13-19, jump 33, disc 40, land 55 |
| `dash_kick` | 50 | dash 10-12, kick 15 |
| `vacuum` | 41 | blade 17, backflip 17-38 |
| `groggy_h` | loop 40 | |
| `entrance` | 106 | cocoon burst 79, land 90 |
| `transform` | 30 | wings open 4-12, sphere 6 |
| `idle_b` | loop 22 | |
| `glide_b` | loop 16 | |
| `wing_strike` | 55 | hit 15 |
| `wing_barrage` | 117 | swings 0/26/64/89 |
| `flap_dive` | 59 | slam 26 |
| `coco` | 76 | orb1 19, orb2 46 |
| `release` | 96 | detonation 53, revert 92 |
| `revert` | 43 | |
| `death` | 100 | |
| `chain_reform` | 18 | |

Looks: element look `dendro` / `pyro` / `flat`, set by command, swapping wing models. Flash.

## Stage-2 decisions (answers to spec/README.md open questions; binding)
- **Q1 root travel:** rig clips carry height, lean and local offsets only. The horizontal root offset returns to 0 by the clip's end and is never baked as travel. The MODULE moves the body (the Guardian contract). Clip authors must remove baked horizontal travel: kick_combo, vacuum, wing_strike, flap_dive, release, etc.
- **Q2 event retimes and names (spec):**
  - kick_jump: orb 45, kick 52, impact 55, land 59;
  - dash_kick: kick 15, ring 19;
  - vacuum: stomp 16, blade 17;
  - wing_barrage: swings 5/31/69/94;
  - transform: event name `rings` at t9;
  - release: flash 35, glint 37, rings 38, detonation 53, shrink 87, flat 87, shatter 91.

  The rig manifest uses these names and ticks. The module reads them from the manifest.
- **H1 hit 1:** a vertical strip (lane 4.5×2.4 plus a disc of r 1.5), not a front arc.
- **H3:** the kick and the ring are two hazards in ONE volley group, so they count as a single 1.3 hit.
- **Q5/Q6 butterfly bands:**

  | pattern | melee | mid | far |
  |---|---|---|---|
  | B1 | 2 | 1 | – |
  | B2 | – | 1 | 2 |
  | B3 | 1 | 2 | – |
  | B4 | – | 1 | 1 |

- **Q7:** sfx=0 on every butterfly hazard; the patterns compose their own sounds.
- **Q8:** the butterfly module clamps locked ground-hazard targets to the walk disc (r 20.3), not r 18.5, so a player hugging the wall is still covered. The Guardian is unchanged.
- **Q9:** in butterfly form her body is clamped to r 16.5; the B5 release point to r 16.
- **B4:** orbs fly at 0.25 b/t (spd 2), home for 40 t, then stop by ending their projectile life.
- **B5:** the dome decal (r 10) starts at the cup (t31, 22 t of warning). The release point is about 4 b beyond the player toward the wall (clamped to r 16), so the player escapes toward the centre or dashes at E.
- **FX engine:** the fx kit (wip/bf-fx, `rlk:mboss/butterfly/fx/*`, bf_fx_api.md) is THE effect engine.
  - The core's small tinted engine (`mboss/butterfly/tc/**`, RP mboss/bf_fx/*) is migrated to kit calls and removed.
  - The core's clean() spares the kit's owned paths.
  - Core hooks call the kit:
    - uninstall → fx/uninstall;
    - cleanup → fx/clear and fx/hud/clear;
    - pause → fx/tele/clear and fx/hud/flash_end;
    - death_start → fx/tele/clear;
    - the HUD lines → fx/hud/put_extra and put_sub;
    - the coc and buff badges → the kit glyphs.
- Every other recommended answer in spec/README.md is accepted unless it contradicts this plan.

## Review-fix decisions (binding, after the core and pattern reviews)
- Fix every confirmed (real=true) finding in mb2/review/core_findings.json and the pattern review files.
- **Balance (fairness F1):** the butterfly must be within about 20 % of the Guardian's damage per minute for the same player behaviours, measured with the reviewer's sim (mb2/review/fairness*/), stand / melee walk / ranged walk.
  - Start from the butterfly-form coefficients ×0.7: B1 1.0, B2 0.35, B3 1.2, B4 1.0 per orb (or one volley group for both orbs), B5 1.8.
  - Player-side Burning from her own Pyro/Dendro alternation is intended; count it in the numbers.
  - Re-run until it holds. Human-form coefficients change only if needed.
- **B5 escape (fairness F3, adopted as an improvement):** when the r 16 clamp moves R (player beyond about r 12), move R 4 b along the wall tangent instead of outward, so the escape from the decal stays at 7.3 b or less.
- **Melee uptime (fairness F5):** reduce the butterfly keep-away. Glide out only inside 3.5 b (was 5 b); the Pyro back-off to 6 b stays.
- **Fidelity:**
  - B2 dive speed scales with distance (dive time = dist / 0.7 b/t, clamped), with the decals kept in sync;
  - transform inside the body clamp;
  - B5 swoop speed capped;
  - the B2 crescent oriented along its flight with a flame tail;
  - the Pyro back-off even when the wings are already Pyro;
  - the B3 glide timing read from the real rig events.

## Fix round (applied on wip/bf; supersedes the damage columns above where they differ)
- **Coefficients after the balance runs** (mb2/balance/bal.py = the reviewer's fight sim, Lv4 item-less player, 3 seeds x
  3 min, stand / melee walk / ranged walk): H1 0.7 / 0.9, H2 0.6 / 0.9, H3 1.3, H4 1.2, B1 0.8, B2 0.35 per crescent,
  B3 0.9 + trail 0.2 (max 2), B4 1.2 per orb, B5 1.8 -> **1.5**. The butterfly form went x0.7 first (the plan's start);
  that left the melee walker at 1.6x the Guardian, so H1 / H2 (the patterns that hit a swinging melee player most) were
  cut too, and B4 (what reaches a ranged player) rose back to 1.2.

  | HP per minute | before (b98f833) | after | Guardian |
  |---|---|---|---|
  | stand | 368.1 (1.70x) | 243.6 (1.12x) | 217.1 |
  | melee walk | 326.1 (2.06x) | 184.4 (1.16x) | 158.3 |
  | ranged walk | 261.0 (2.00x) | 112.9 (0.86x) | 130.6 |

  The player-side Burning of her Pyro / Dendro alternation stays (intended) and is in these numbers.
- **B2 dives** take D = (L + 4 x 0.4) / 0.7 b/t ticks, 7..60 (L = the straight distance from the fan-out end to the
  landing point, measured in game at the swing); the decal, the dive, the landing and the pj life all use the same D.
  Between the swings she glides in at 0.3 b/t while beyond 9 b. Each crescent draws a 1-2 b flame streak along its
  flight; the claw itself stays camera-facing (readable from any side).
- **B5**: the swoop takes ceil(|SR| / 1.0 b/t) = 9..13 t (ends before the whirl at 18); beyond 8 b she glides in at
  0.4 b/t for at most 10 t first (the prep state). When the r 16 clamp would move R (player beyond about r 12), R goes
  4 b along the wall, on the side away from her: the walk out of the dome is <= 6.5 b for every player radius.
- **Transformation** glides her inside r 16.5 in its first 4 t (before the wings open).
- **Butterfly idle**: glide out only inside 3.5 b; glides, the Pyro back-off and the butterfly-form dest points stay
  inside r 16.5. The Pyro back-off to 6 b also runs when the wings are already Pyro (the pattern waits at most 8 t).
- **Groggy 달빛 이슬**: it stays until it is taken, the next transformation's sphere (which always leaves exactly 3) or the
  next butterfly form's end; a /reload brings it back while it is offered.
- **First person** (no shoulder-view avatar): no camera-facing kit cards at the player's own eyes for 달빛 고치 and its
  cure (only the floor ring, the spiral, the sounds, the HUD and the title-line pop).
- **H4** blade back to the spec's hr 1.5 at 0.75 b/t (the framework blade now reaches hr + 0.3, the lane decal's edge).

## User feedback after the 10-18 release (binding)
- **"피해 +50%가 아니라 치명타 피해 +50%야":** the reward buff (after the 달빛 고치 cure) is CRIT RATE +15 % and CRIT DMG +50 %, not DMG +50 %. Fix the code, the HUD text, the README and the hints.
- **"선딜 좀 줄이고":** shorten every damaging attack's wind-up by about 25 %, like the Guardian tune. A readable telegraph of at least 10 t stays. Retime the rig clips with the shared clip retime (RETIME tables). Event ticks, fx, sounds and decals move with the hits.
- **"일정 체력 이상 회복해야 하게. 하나만 먹어도 기믹 처리되는건 너무 쉬운 것 같아":** the cure now needs cumulative healing.
  - While debuffed, every heal event adds its EFFECTIVE amount (after the -40 % healing penalty, counting overheal so a player near full HP is not stuck) to a cure meter.
  - The debuff is removed when the meter reaches 15 % of max HP.
  - 달빛 이슬 orbs heal 13 % max HP each (7.8 % effective), so 2 of the 3 orbs cure; other healing sources contribute.
  - The HUD shows the progress (e.g. the badge plus "회복 9/15%"), with a small chime per heal.
  - The meter resets on each new application.
  - The groggy's single extra orb still appears if the player is still debuffed. If 2 orbs are needed and only 1 is offered, spawn 2.
- **Applied (wip/bf2 on 7a6dc4f):**
  - Reward: `coc/cure` sets #mbCritAdd 15 and the new framework modifier #mbCritDmgAdd 50 (added to `critDamage` in `items/hook/stat_buffs` while #mbLive); #bfDmgPct stays 100. Cleared by `coc/clear` / `mboss/player_reset`. HUD/hint/README text: "치명타 +15% · 치명타 피해 +50%".
  - Wind-ups: RETIME tables in `tools/butterfly_clips.mjs` (exported in the rig manifest); the module maps every literal tick through `api.rt(clip, t)` and every lock-on telegraph through `api.tell_rt(t) = max(10, round(0.75 t))`. Strikes / follow-throughs keep full speed. Played wind-ups: H1 hit2 32->24, H2 sweep 13->10 / disc 42->32, H3 kick 15->11, H4 blade 17->13, transform hit 6->5, B1 15->11, B2 swing1 5->4 and gaps 26/38/25 -> 20/28/20, B3 fan 28->21, B4 orb1 19->14 (gap 27->20), B5 dome 53->40 (telegraph 22->17, swoop cap 1.0 -> 1.2 b/t). H1 hit1 stays 10 (floor).
  - Coefficients lowered to keep the 3-policy HP/min near the Guardian: H1 55/70, H2 45/70, H3 130, H4 120, B1 70, B2 35, B3 80/20, B4 100, B5 130. Sim (3 seeds, 3600 t): stand 217.3 (1.00x), melee walk 181.8 (1.15x), ranged walk 127.3 (0.98x) vs Guardian 217.1 / 158.3 / 130.6.
  - Cure meter: framework `mboss/player_heal` adds the effective heal to #mbHealAmt; `coc/heal_ev` moves it into #bfCure while debuffed and cures at #bfCureT = floor(15 % max HP, >= 1). Dew heals ceil(13 %) -> 2 orbs always cure (checked for every max HP 1..2000). Chime + dust + `hud/ab_cure` per heal; HUD sub "— 회복 P/T% ". Meter resets in `apply_pl`; cleared in `coc/clear` (fight end, death, uninstall).
  - Groggy: `dew/need` offers 1 orb if the remaining need fits one dew heal, else 2 (`#bfDew1` counts the outstanding offer; reload re-offers).

## Telegraph rule (10-20, user, binding)
"보스의 모든 공격에 바닥의 예고를 보여줄 필요는 없어. 영상에 없다면 그냥 보스의 동작을 보고 회피해야 하는 거니까":
a ground telegraph (framework outline, kit decal, telegraph-only lane, a marker or glow laid on the floor where the hit
lands) only where the reference footage shows one; otherwise the player reads her motion and sound. The audit
(`S:tele/bf/audit.md`, per attack with frame times and evidence sheets) found **no ground telegraph anywhere in her
footage** (the ground light is the attack itself at impact, or a glow at her own feet).
- **Keeps a ground telegraph:** B3's flame trail only (TRIM: the red ember line she lays down = the footage's flame line,
  visible 10 t before its flare; its r 1 disc decal is gone). TF (달빛 고치) KEEP: unavoidable, nothing on the ground.
- **Read from motion and sound (REMOVE):** H1 hits 1 / 2, H2 sweep (and its knee-high dust rings) / disc (and the glint
  over its target), H3 (and the dmg-0 dash lane), H4 (and the dmg-0 blade lane to the wall), B1, B2 (the landing
  decals), B3 fan, B4 orbs (the floor shadow ring) and bursts, B5 dome (and the r 10.5 safe-line ring). Every hazard
  stays `hz/*` with `#hzQuiet 1` (no outline, no strike flash) and `#hzSfx 0`; tells, sizes and damage are unchanged;
  each strike draws its own impact visual. The resume redraw (core `u/redraw`, B2 `p/barrage/resume` + `redraw`) is gone.
- **Readability fix:** H1 hit 1's burst-run starts only 8 t before the hit, so a body tell at -2 (kit `snd/kick_whoosh`,
  a lime glow + glint on her kicking foot) restores the 10 t floor. No timing change.
- **Locked by** `S:mb2/tests/tele_rule.py` (test_butterfly section 11): the hazards drawing a ground telegraph = the
  audit's keep / trim set {B3 trail}.
