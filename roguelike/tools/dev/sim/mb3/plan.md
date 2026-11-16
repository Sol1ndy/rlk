# Mid-boss 3: 실험성 역장 발생 장치 (nameplate 브레게 프로토타입) — binding decisions

Sources: videos `mb3/src/v1..v4.mp4` (in order); description `mb3/src/guide.pdf` (namu wiki, 2 pages).
Research outputs: `mb3/understand/v1..v4.md`, `mb3/understand/model.md`, `mb3/code/adapt.md`.
The butterfly (mb2) is being built at the same time. Its framework helpers (homing pj/steer, blade shapes, volley groups, telegraph-only hazards, the fx kit pattern) are on wip/bf and will be merged before this boss's module is built.

## User requirements
1. "중간보스에 '실험성 역장 발생 장치'도 만들 거야": a third mid-boss in the random registry. Killing it gives the item boxes, like the others. Same care for the model, and send renders when the model is done.
2. "지금 하고 있는 나비 작업이랑 동시에 돌려": runs in parallel with the butterfly.
3. "프뉴마 우시아는 구현되지 않았으니 타수를 채워야 해결되도록 해. 한 20타정도?":
   - The game has no Pneuma/Ousia.
   - The Genshin mechanic is: Ousia charges up; three Pneuma hits on the core cause groggy.
   - It is replaced by a HIT COUNT: about 20 hits on the boss/core fill the meter and resolve it (groggy).

## Framework decisions (from code/adapt.md; binding unless changed here)
- **Base:** branch from wip/bf (f2ab515). It already has the butterfly framework helpers (pj/steer, blade shape, volley groups, dmg-0 hazards), the shared rig libs (wip/bf-rig) and the kit pattern.
  - Copy and rename the butterfly api/core skeleton, stub rig and tests to `#fg*` / `rlk_fg*` / `rlk:mboss/fieldgen/**`.
  - Copy the fx kit as `rlk:mboss/fieldgen/fx/**`: font rlk:mboss_fg at U+E700-E7FF, a Geo (el 5) telegraph palette, new sprites.
  - The rig uses the shared mboss_rig_* libraries (merge wip/bf-rig's libs into the rig worktree).
- **Registry:**
  - id `fieldgen`, n 3, el 5 (Geo), w 10, minCh 1;
  - name `실험성 역장 발생 장치`, sub `브레게 프로토타입`, colour `#E8C46A`;
  - hp 230, xp 30, atk 12, dmgMul 110, goldMul 5, sap 1, picks 2;
  - scale 2.4, hit 2.4×4.6, intro 130, death 110, deathSnd false;
  - icon minecraft:clock.
  - The three mid-bosses roll 10:10:10, with an unmet boss first.
- **Element:** mres 0, no element RES; Geo hits.
- **Scale and body:**
  - Ring outer diameter D = 7.0 b. The ring centre is about 4.5 b up in cruise and about 5.8 b in the field. The pendulum tip hangs 0.3-0.6 b above the floor, so melee can hit it.
  - Hit volume: the husk under the axis at scale 2.4 plus a shield.
  - Body clamped to r ≤ 16.5.
  - Untargetable during the entrance until the rise ends.
- **Forms (one superset rig, at most 32 parts; model.md):** dormant, cruise (compact), field, core-up, tower, laser, deployed.

## Rotation (binding)
- **Entrance** (about 130 t, untargetable until about t94):
  - the dormant folded device clanks awake;
  - the pods unfold and the crown and halo assemble;
  - the eye opens;
  - it rises about 2.9 b and turns to the player.
- **Cruise patterns** (range-band bag, no immediate repeat):
  - **C1 일점 상쇄 / 폭격:**
    - turn and pitch 10 t, ports glow 2 t;
    - about 20 bombs over about 45 t, dropped along a straight flight line over the player (glide about 0.55 b/t, clamped);
    - each bomb falls 5-6 t onto its own predicted-point decal (≥10 t lead) and bursts at r 1.3;
    - finisher: a gold column tell 13 t from the face-down core, a 3-4 t plunge, a slam of r 5;
    - coefficients: bomb 0.8 (one hit per volley group of 4 bombs), slam 1.4.
  - **C2 내려찍기 (slam alone):** column tell 13 t, plunge, slam r 5; coefficient 1.4.
  - **C3 코어 / 레이저 빔:**
    - the medallions dock beside the core and drop (4 t), with a spark charge (18 t);
    - two gold beams counter-rotate about 5°/t around the device for 133 t; floor spots on an r ≈ 5 circle; the width blooms then narrows (0.5 → 1.0 → 0.5 b);
    - line hazards re-aimed every tick, re-armed every 10 t, in one volley group;
    - coefficient 0.5 per touch.
  - **C4 바위 폭탄 / 미사일 (far band):**
    - spike-tip flare and vent shaft tell 21-25 t;
    - 10 gold drill-missiles launched over 14 t; they rise out of view, then dive with weak homing;
    - late-lock decals r 1.5 with a lead of at least 10 t;
    - 2 volley groups; coefficient 0.9.
  - **C5 지면 충격 / 중력 폭발:**
    - core flip-up tell (eye out +1-4, gold flash and lift +5/6);
    - outer rim decal at the final radius R = 1.7 D (about 12 b; clamp inside the arena) from +3;
    - the dark disc grows to R by +33; an up-beam +29-40; the column down +41-44;
    - a single full-area blast at +48;
    - dodge by leaving the disc, or by jumping or dashing (i-frames) at the blast;
    - coefficient 2.2.
  - **C6 파쇄 / 바위 날리기:**
    - dip and roll toward the player 12 t; vent flare and medallions flung up 8 t; tower form 18 t; flame-band charge 17 t;
    - 8 floor bursts 6 t apart walking in an arc onto the player (decals r 1.8, ≥10 t lead; coefficient 1.3, heavy knockback);
    - lifted slabs, then about 4-6 slab throws 8 t apart as blade projectiles at about 1.5 b/t toward the player (coefficient 1.1);
    - revert 15 t.
- **Field (역장 생성 — 중력 감소):**
  - Triggered after 5 cruise patterns (first) or 4 (later), at a pattern boundary.
  - Halo flip and warp-out flash; about 21 t invisible with violet glitch streaks; warp-in at the arena centre; unfold into field form (violet halos, violet column, orbiting medallions).
  - Banner/caption "중력이 감소하고 점프 능력이 향상됩니다". Floating pebbles.
  - **Low gravity** for the whole field, on the player and the shoulder-view avatar:
    - gravity ×0.5, jump_strength ×1.19, safe_fall_distance +4, as multiplicative modifiers rlk:mb_lowg;
    - the avatar jump reads its own jump_strength;
    - framework flag #mbLowG re-derived every tick with every cleanup path;
    - the shared swing rules still apply: no jump during a swing.
  - **Field damage cut:** the boss takes 40 % less damage while the field is up ("all RES up" in the caption).
  - **Field sequence:**
    - 「인력 충격파」 ×3 at the start: charge sphere, 1-tick beam, flare dome, then an arena-wide expanding ring front at 0.55 b/t;
      - its hit band is low (0-0.7 b), so a jump clears it, and dash i-frames do NOT help (#hzNoDodge);
      - wave gaps 68 and 83 t; the 3rd has a longer charge (40 t);
      - below 50 % HP the 3rd wave fires 3 fronts 9 t apart;
      - coefficient 1.2 each.
    - Then about 400 t of field patterns:
      - **F1 감소 영역:** 9 eruption events at 11-50 t intervals; each is 1-4 dark discs of r 2.8 placed 2-8 b from the player with a 15 t lead, then a gold eruption; coefficient 1.2.
      - **F2 파쇄 in field form:** bursts walking onto the player and slab throws, as C6 without the tower build-up.
    - If not broken: the closing 「인력 충격파」 ×3, then pack-up (lift-off flash, 20 t rise, lances, roll/pack into compact form); no groggy.
- **20-hit break meter** (replaces the 3 Pneuma hits — user decision):
  - Open only while the field is up (from the unfold to the break or end).
  - Counts player hits on the boss (the module on_hit hook):
    - reactions, DoTs (#tfm 1) and item procs (#sub itv 1) do NOT count;
    - at most one count per 6 t.
  - At 20: cancel the running pattern and clear hazards; end low gravity and the damage cut; play the break (the core bubble cracks through stages 0-3 at 0-4/5-9/10-14/15-19, then bursts; tilt 25-30° in 9 t, damped wobble 20 t, sink); groggy 200 t; re-level 6 t; core flip 9 t; back to cruise.
  - HUD:
    - a violet under-bar with the hits out of 20;
    - a sub-line with a badge, 20 pips and "12/20" (font rlk:mboss_fg);
    - each count gets a crack glint, a sound and a pip flash.
- **Groggy:** 200 t, slumped (ring centre about 3.0 b, roll 25°, seam off, halo slid, pendulum swinging). Hittable; no attacks.
- **Death:** the seam flickers out, the halo and drill pods fall, the ring sinks tilted 40°, then it scales out (about 110 t). Mechanical sounds only.
- **Telegraphs:** every damaging hit has at least 10 t of readable warning on marble and pink.
- **Telegraph rule (10-20, user; supersedes the line above where they differ):** a ground telegraph only where the
  reference footage shows a marker on the floor (kept: C1 finisher / C2 slam base flare, C5 rim + dark disc, F1 dark
  disc); every other hit is read from the device's motion, its own projectile / slab and the sound, still with >= 10 t
  of tell. Audit `S:tele/fg/audit.md`, contract §21.
- **Sounds:** vanilla only, mechanical/brass (anvil, chain, piston, beacon, respawn anchor, amethyst, trial spawner, breeze charge...).

## Framework additions (opt-in, in build_mboss_core.py)
- #hzNoDodge: a hit ignores dash i-frames.
- hz/aim: re-aim a line hazard each tick.
- hz/resize.
- #hzRearm: re-arm a lingering hazard every N t.
- #mbLowG: the low-gravity flag and its rlk:tick lines.
- The view/move avatar jump reads the avatar's own jump_strength.
- The Guardian and butterfly outputs must stay byte-identical except for the intended shared edits.

## Stage-2 decisions (binding)
- Every recommended answer in mb3/spec/README.md's open questions is accepted. In particular:
  - **Q2:** the triple third wave's gap is 6 t (impacts 176/182/188), so it can be cleared.
  - **Q4-Q7:** the cruise.py changes as the specs say:
    - C1: finisher re-lock, end 103;
    - C3: azimuths -90/+90, band r 3.0-5.8, width 1.0 then 0.6, body yaw frozen;
    - C4: flight 28 t;
    - C6: arc walker, bursts in a 7-8 volley pair, at most 2 slab hits.
  - **Q8/Q9:** F1 event ticks from the footage (end 260). F2 uses the rig's frock clip.
  - **Q10/Q11/Q14:** #fgCool 40 after the field opening; warp-out fx at the hide tick; look/idle at the dock tick.
  - **Q13:** the meter uses the kit HUD (put_sub, #fkHudV redraw) and the field core height 4.1.
  - **Q16:** the slab blade reach follows the framework's final blade rule. The butterfly fix round may change the blade reach; keep a total reach of about 1.45 b.
- **Ownership:**
  - the fx kit (wip/fg-fx, `rlk:mboss/fieldgen/fx/*`, fg_fx_api.md) is THE effect engine. The core wires it per fg_contract.md §15;
  - the rig (wip/fg-rig) is merged later, after its clips; until then the stub rig and the event names apply.

## Rig integration notes (from the clips author, binding at rig merge)
- **Rig commits:** wip/fg-rig 0f7c0e8 (model) and 948f9a3 (28 clips).
- **C3 lasers:** read the medallion orbit from the manifest. The eye medallion starts at azimuth +90 and the gear at -90, at 5°/t in opposite directions from tick 25 to 158, with floor spots at r 5.58. The stub's 0/180 start must go.
- **F1/F2:** play field_idle when they end, and apply look/idle at field_end's dock event (58).
- **Waves:** the third wave plays wave_long (beam 39, burst 40). The wave that lands the device plays wave_drop (drop 40, land 44, risen 83).
- **Disk:** keep scratch builds small. The disk was nearly full at one point.

## Fix round (binding; applied on wip/fg after the state and fidelity reviews, mb3/review/{state,fidelity})
- **State.**
  - FG-S1: a reload between the 20th count and its module tick re-derives the break from the meter (`#fgBrkQ` again when
    the meter is open and full); a pending count keeps its feedback.
  - FG-S2: `field/open` is idempotent (`field/reopen`: look, hitbox, lines only), and the field banner plays once per
    field (`#fgBanF` = the field number it played for). A reload or a test cut in the opening after the unfold, or a
    test request inside an open field, keeps the meter, the field number and the hint's end.
  - FG-S3 (framework, shared by every module): no tagged player is a pause (`mboss/world` → `pause_tick`), so the
    module's pause hook runs and its decals come back on the resume. The Guardian and the butterfly get the same fix;
    nothing else of theirs changes (their outputs stay byte-identical).
- **Fidelity.**
  - FID-1: the 20th hit while the closing `wave_drop` has the device on the floor or low in its rise plays the rig's new
    `break_low` (same events and length as `break`, from the grounded pose: bubble and burst at the grounded core, then
    the heave and tilt into the slump). The rig now has 29 clips.
  - FID-2: the C1 bombs leave the rig's front ports `port_0` / `port_7` (1.05 b to the side, 2.25 b ahead, 3.48 b up;
    the centre bomb between them), decals under them.
  - FID-3: the kit's `ports_glow` keeps only its dust; the module puts a glow on each of the 8 manifest port anchors.
    The glows stand still, so they last 4 t ("ports glow 2 t" and a 2 t fade, gone 2 t into the run glide; the
    verification round: with 14 t they trailed the gliding ports by up to 2.9 b).
  - FID-4: the meter feedback (`meter_hit`, crack flashes) is drawn at the rig core while `wave_drop` moves it.
  - FID-5: the C1 / C2 slam point gets the kit's `column_base` (floor glow, base flare, no column card); the rig draws
    the column under the gliding device.
  - FID-6: F1 plays `field_idle` at the beams-off (206), not at its end (260).
  - FID-7: the closing triple wave follows the rig core (beams, pulses, the charge sphere); every wave beam is on the
    rig's own beam tick.
  - FID-8: one death fade at the clip's `out` (80).
  - FID-9: the pack-up sparks at `horiz` (32) on the medallions' anchors.
- **Balance (supersedes the coefficients of "Rotation").** Measured with the reviewer's fairness sim
  (mb3/fgfix/sim: a copy of mb3/review/fairness_verify/fgfair.py; Lv4 item-less player, 3 seeds × 3 min, the Guardian on the same
  harness), target: within about 20 % of the Guardian's HP per minute for stand / melee walk / ranged walk.
  - A walker breaks the field during the opening waves (a jump clears them), so the field patterns hit only a player
    who never breaks it; a melee player stood under C3's medallions and jumped C5's blast. So:
  - coefficients: C1 bomb 1.0 and finisher 1.8, C2 1.8, C3 0.5, C4 1.1, C5 2.2, C6 1.5 / 1.2, F1 0.5, F2 0.7 / 0.8,
    「인력 충격파」 0.5 (were 0.8 / 1.4, 1.4, 0.5, 0.9, 2.2, 1.3 / 1.1, 1.2, 1.3 / 1.1, 1.2);
  - range bands: C1 melee / mid / far ×2, C2 melee ×2 / mid, C3 mid, C4 far ×3, C5 mid, C6 melee / mid ×2 / far (C3 and
    C5 left the melee band; C1 and C6 joined it);
  - every cruise pattern recovers 12 t (was 20).

  | HP per minute | Guardian | before (fde9db7) | after the fixes, old balance | after |
  |---|---|---|---|---|
  | stand | 217.1 | 335.2 (1.54×) | 342.9 (1.58×) | 250.9 (1.16×) |
  | melee walk | 162.9 | 43.9 (0.27×) | 43.9 (0.27×) | 150.3 (0.92×) |
  | ranged walk | 137.0 | 81.2 (0.59×) | 89.7 (0.65×) | 116.1 (0.85×) |
- **10-20 user round (supersedes the coefficients above; contract §21, branch `wip/tele-fg`).**
  - "역장 발생 장치의 계수를 많이 올려야될 것 같아": every coefficient ×1.5 (C1 bomb 1.5 and finisher 2.7, C2 2.7,
    C3 0.75, C4 1.65, C5 3.3, C6 2.25 / 1.8, F1 0.75, F2 1.05 / 1.2, 「인력 충격파」 0.75); range bands, recovery,
    sizes and timings unchanged.
  - Telegraph rule (10-20), see "Telegraphs": decals out of C1 bomb, C3, C4, C6 / F2 bursts and throws, the waves; the
    slab throw gets `p/slab_glint` on the slab (not a ground marker) so its 10 t tell is visible.
  - Same sim, seeds and player model (`S:tele/fg/sim`); HP lost / deaths per minute:

  | per minute | Guardian | rel (039b911) | after (agent reads the slab glint) | after (agent without lanes) |
  |---|---|---|---|---|
  | stand | 217.1 / 1.33 | 250.9 / 1.67 (1.16×) | 376.0 / 2.33 (1.73×) | 376.0 / 2.33 |
  | melee walk | 162.9 / 1.00 | 139.3 / 0.78 (0.86×) | 211.8 / 1.33 (1.30×) | 312.9 / 1.89 |
  | ranged walk | 137.0 / 0.78 | 113.1 / 0.56 (0.83×) | 177.7 / 1.00 (1.30×) | 247.8 / 1.44 |
