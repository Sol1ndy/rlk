# S5 The 20-hit break meter and the HUD: implementation spec

| field | value |
|---|---|
| owner | the core (the count, `on_hit`; the state; the boss-bar lines and the under-bar); the kit (the glyphs, the pip flash, the per-count fx and sound, the banner, the pops) |
| meter open | `#fgOpen 1` from the field unfold (opening clock 35) to the break (20 counts), the pack-up start, death or a cut |
| count rule | one count per player hit on the body while open; not reactions / DoTs (`#tfm 1`), not item procs (`#sub itv 1`); **at most one count per 6 t** (gametime) |
| at 20 | the break (`S3_break_groggy_recover.md`) |
| font | `rlk:mboss_fg` (U+E700-E7FF, kit) |

## 1. Footage and plan check

- **Footage:** no counter UI in Genshin (the field ends after 3 Pneuma hits on the core). The release itself is shown
  (v2 A3): the bubble lights, cracks and bursts.
- **User rule** (plan "20-hit break meter"): about 20 hits on the boss / core fill the meter and resolve the field
  (groggy).
- **Plan HUD:**
  - "a violet under-bar with the hits out of 20" ✓ (core `hud/bar_meter`, bossui colour 1 `#C58BFF`);
  - "a sub-line with a badge, 20 pips and '12/20' (font rlk:mboss_fg)" ✓ (core `hud/meter`, kit `put_sub`);
  - "each count gets a crack glint, a sound and a pip flash" ✓ (kit `hud/meter_hit`).
- **Crack stages** on the core bubble: 0 / 1 / 2 / 3 at counts 0-4 / 5-9 / 10-14 / 15-19, 4 = the burst ✓ (rig
  `crack/<n>`).

Plan disagreements and fixes (integration, both sides exist):
- **F1 — two crack callers.** The core's `brk/count` calls `crack/<n>` through `brk/stage`, and the kit's
  `hud/meter_hit` also calls `<RIG>crack/<n>` at 5 / 10 / 15. **Fix:** let the kit do it (it adds `p/bubble_crack`
  and `snd/bubble_crack` with it). The core keeps `#fgCrack` up to date (reloads, tests use it) but drops the rig
  call and `cfx/crack` from `brk/stage` once the kit is merged.
- **F2 — the meter_hit height.** The kit docs say `positioned ~ ~3.84 ~`; the real rig's field core is at **4.1**
  (`form_states.field.rest_anchors.core`). Use the manifest anchor.
- **F3 — duplicate name-line flags.** The core's `hud/extra` writes "   역장" in the field and " · 그로기" during the
  break / groggy / recovery. The kit's `put_extra` writes " · 역장" + the badge (while the meter is open), the
  low-gravity icon and " · 그로기". Both together show the words twice. **Fix:**
  - the core writes "   순항" (cruise, gold) and "   역장" only while `#fgField` ≥ 1 **and** `#fgOpen` 0 (the warp,
    the pack-up);
  - the kit's `put_extra` supplies everything else;
  - drop the core's own " · 그로기".
- **F4 — the count digits.** The core writes "n/20" as plain text; the kit draws outlined gold digit glyphs
  (E720-E72A) through `put_sub`. **Use the kit's `put_sub`** (it also carries the flash state). The kit's sub
  components already hold the badge, "역장", the pips and the digits, so while the meter is open:
  - the core's own sub-line is reduced to the running field pattern's label ("패턴  감소 영역", as in
    `fx_hud.png`);
  - it ends with `fx/hud/put_sub` (badge, 역장, pips, digits, and the first-field hint while `hud/hint_on` holds; the
    core calls `hud/hint_off` 120 t after the unfold);
  - it is rebuilt whenever `#fkHudV` changes (the pip flash ends by the kit's schedule).

## 2. The count (core `on_hit`, unchanged)

```
on_hit (@s = body inside combat/apply):
  #fgFlash 1 (the rig hit flash)
  unless #fgOpen 1 → return            (meter closed)
  if #fgBrk >= 20 → return
  if #tfm tmp 1 → return               (reaction / DoT damage)
  if #sub itv 1 → return               (item procs)
  gametime − #fgBrkT ≤ 5 → return      (one count per 6 t)
  #fgBrkT = gametime; #fgBrk += 1; #fgBrkFx 1; at 20: #fgBrkQ 1
```

- Untargetable hits and true damage never reach `on_hit`, so the warp (13-34) and the death add nothing.
- The 6 t cooldown means a multi-hit burst or a shotgun counts once. 20 counts take ≥ 114 t; a steady melee combo
  takes about 160-240 t. The meter is open about 850 t in an unbroken field (opening waves about 213, field patterns
  400, closing waves about 220), so it is reachable without being trivial.
- **Field damage cut:** while `#fgOpen` 1 the boss takes ×0.6 (`incoming` → `field/cut`), reactions included, at least
  1. The plan's "모든 저항 증가" (all resistances up), as a flat cut: no element RES.

## 3. Per-count feedback (core `brk/count`, next module tick after a count)

| step | what |
|---|---|
| 1 | `#fgBrkFx 0`; `#fgCrack` = min(3, `#fgBrk` / 5) |
| 2 | `#fkM mb` = `#fgBrk` |
| 3 | `execute as <body> at @s positioned ~ ~4.1 ~ run function rlk:mboss/fieldgen/fx/hud/meter_hit`. The kit does the rest: the newest pip flashes white for 4 t; `p/meter_glint` (the crack glint on the bubble); `snd/meter_tick` + a chime note rising with the count (pitch 2^((k − 10)/12)); at 5 / 10 / 15 `p/bubble_crack`, `snd/bubble_crack` and `crack/<n>` (as the body) |
| 4 | the core's `#fgPipT 4` (its own flash, only without the kit) and `hud/refresh` |

At 20 the same feedback runs (the 20th pip flashes), then `brk/begin` on the same tick.

## 4. The lines (boss bar, three lines)

| line | cruise | field opening (warp 0-34) | meter open (35 → break / pack-up) | break (34 t) | groggy (200 t) | recover (15 t) |
|---|---|---|---|---|---|---|
| name (`extra`) | "   순항" (gold `#E8C46A`) | "   역장" (violet `#9C86E8`) | kit `put_extra`: " · 역장" + badge E700 (+ low-gravity icon E705 from the banner) | kit: " · 그로기" | kit: " · 그로기" | kit: " · 그로기" |
| sub (`sub`) | "순항" or "패턴  <label>" | "패턴  역장 생성" | "패턴  <field pattern label>" (core), then kit `put_sub`: [E700] 역장 [pips ×20 in groups of 5, E7F1 gaps] [digits "12/20"] + the hint (first field, 120 t) | "[E704] 역장 붕괴" | "그로기  공격할 기회" | "그로기  다시 떠오른다" |
| under-bar | cruise progress to the field (gold, code 8: `#fgCruN` / `#fgCruLim`) or pattern progress (Geo, code 5) | pattern progress | **violet** (code 1 `#C58BFF`): `#fgBrk` / 20 | full (20/20) | green (code 9): time left of 200 | green: recovery progress |

- Pips: E701 empty (dark violet gem), E702 full (gold), E703 the newest, white for 4 t. Groups of 5, separated by E7F1
  (+2 px).
- The digits: E720-E729 + E72A "/" (outlined gold, 9 px), from `K.digits('12/20')`.
- The hint "코어를 공격해 역장을 깨뜨리세요" (attack the core to break the field): the first field only, 120 t from the
  unfold.

## 5. Banners, pops, flashes (kit)

| when | call | what |
|---|---|---|
| field opening 56 | `hud/banner_field` | actionbar "**중력**이 감소하고 **점프** 능력이 향상됩니다" (중력 / 점프 red `#FC5050`, bold) + the low-gravity icon, 4 s (`hudHold 80`); `pop_lowg` (the big icon on the title line); `snd/field_banner` |
| field opening 56 | `hud/lowg_on` | the low-gravity icon on the name line |
| optional, the first field + 80 | `hud/ab_lowg` | a 2 s actionbar: low gravity and what it means (점프 강화 · 낙하 피해 감소 · 충격파는 점프로 피하기) |
| break 5 | `hud/pop_break`, `hud/flash_gold` | the cracked-bubble pop on the title line; a gold flat 0.55 |
| warp-out 12 (players within 8 b) | `hud/flash_white` | a white flat (optional) |
| pause | `hud/flash_end`, `fx/tele/clear` | drop any title overlay |
| the break / pack-up / death | `hud/banner_end`, `hud/meter_close`, `hud/lowg_off`, `hud/hint_off` | |
| fight end, abort, uninstall | `hud/clear` | |

All HUD feedback is on the title / actionbar / boss-bar lines. **No world card at the player's eyes** (the butterfly's
PL-1): the glint is at the core, the pebbles at the feet.

## 6. Timeline summary (one field)

| field clock | meter |
|---|---|
| opening 35 | `meter_open` 0/20, crack 0 (clean bubble), the hint (first field) |
| opening 56 | the banner, low gravity, the low-gravity flag |
| each count | `meter_hit` (pip flash 4 t, glint, chime k) |
| counts 5 / 10 / 15 | bubble crack stage 1 / 2 / 3 |
| count 20 | the break: `meter_close`, `lowg_off`, `hint_off`, `banner_end`; burst at +5 (`crack/4`, `pop_break`) |
| or the pack-up 0 | `meter_close`, `lowg_off` (no burst) |

## 7. Sound

| when | sound |
|---|---|
| each count | `snd/meter_tick` (`block.amethyst_block.hit` 0.9/1.4, `block.chain.hit` 0.5/1.2) + a chime note `block.note_block.chime` (or the kit's) at 2^((k − 10)/12) |
| counts 5 / 10 / 15 | `snd/bubble_crack` |
| the banner | `snd/field_banner` |

## 8. Dodge windows

Not applicable.

The design point: the meter rewards staying on the device while dodging the field patterns. F1's 15 t discs can be
side-stepped at half speed while attacking (`F1_reduction_zone.md` §10). The waves need a jump, so stop the combo or
dash first. F2's bursts are jumpable with low gravity.

## 9. Diagram (HUD)

```
 Lv.N  실험성 역장 발생 장치  · 역장 (o)(^)                 <- name line (+ kit flags)
 [=============== HP ===============]
 [====violet 12/20========          ]                    <- under-bar
 패턴  감소 영역   (o) 역장  ##### ##### ##*-- -----  12/20   <- sub-line (core label + kit glyphs)
```

## 10. Implementation notes

- `hud/sub`: with the kit merged, while `#fgOpen` 1, build only the pattern label and the hint, then
  `function rlk:mboss/fieldgen/fx/hud/put_sub`. Keep the generated `hud/pips*` functions only for the no-kit build
  (or delete them at the merge).
- `hud/extra`: F3.
- `bars`: unchanged (the violet meter while open).
- Rebuild the lines when `#fkHudV` changes: add `execute unless score #fkHudV mb = #fgHudV mb run …` to the module
  tick.

## 11. Checks

- A count only while `#fgOpen` 1; none from `#tfm 1`, `#sub itv 1`, or within 6 t of the last count.
- `#fkM` equals `#fgBrk` at each `meter_hit`. Crack stages at 5 / 10 / 15. The 20th count breaks on the next module
  tick.
- The under-bar shows `#fgBrk` / 20 in colour 1 while open.
- No duplicate "역장" or "그로기" on the name line.
- The sub-line ends with the kit components. The pip flash ends after 4 t and the lines are rebuilt.
