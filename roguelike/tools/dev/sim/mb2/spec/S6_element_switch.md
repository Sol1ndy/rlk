# S6 Wing element switch (Dendro ⇄ Pyro): implementation spec

| field | value |
|---|---|
| owner | core `ai/prep_begin` → `look/switch` (`#bfWant` = the picked pattern's element) |
| when | butterfly form only, before a pattern whose element differs from the current wing look: the switch happens at once (1 t swap), and the pattern starts **8 t later** (`LOOK_LEAD 8`). The footage gap is 5-12 t. |
| looks | rig `look/dendro` (lime/opal glass), `look/pyro` (orange-gold glass, magenta rims, a mauve-tinted frame), `look/flat` (emissive lime: transform-in and retract) |
| patterns | Pyro: B2 화염 날개의 습격, B3 날개 휩쓸개. Dendro: B1 우아한 날개, B4 달빛 축복, B5 달빛 해제, the transformation. |
| damage | none |

## 1. Footage check

Source: v3 §3.0 (`understand/v3.md`):
- Dendro → Pyro: a 0.49x replay at 3.817-3.867 s, i.e. about 1 real tick. I checked `sheet_pyro_switch_perframe_3.70-4.15.jpg`.
- Pyro → Dendro: real time, 20.333 → 20.350 s, 1 frame.

| aspect | footage | spec |
|---|---|---|
| duration | 1 t; the colours shift through pink-gold to gold-orange (Pyro), or fade back to lime-white (Dendro) | 1 t model swap, plus a 4-6 t glow overlay that carries the "shift" |
| particles | **none**; only a soft rim glow that persists while she is Pyro | **minimal**: a short glow card plus ≤ 8 sparks. The core's 24-dust + 10-flame burst is louder than the footage: reduce it. |
| rim | Pyro: a magenta-pink outer glow `#E26E50` / `#F2C3A8` / `#94526F` on the wing rims; the frame tinted mauve `#6B4061` | the rig's pyro look; optional glowing outline (`Glowing` + `glow_color_override` magenta `#E26E50` on the 2 forewing glow cards) while Pyro |
| body | never changes colour | — |
| audio | Dendro → Pyro: a soft low thump (+9 dB); Pyro → Dendro: masked by the BGM | see §2 |
| gap to the pattern | 5-12 t (swing 1 of B2 starts about 0.6 s after; the B4 wrap 0.25 s after) | 8 t |

## 2. Per-tick timeline (`#bfT` in `ai/prep`)

| t | mechanics | fx | sound |
|---|---|---|---|
| 0 | `look/<el>` (1 t model swap), `#bfLook = #bfWant`; HUD refresh (the element colour of the progress bar) | **→ Pyro:** `tc:glow #FAD77C 1.5→4.5 l6/f3 bb center` at ^ ^3.0 ^ (it behaves as the wing-span centre); 2 × `tc:glow #E26E50 1.0→2.5 l5/f2 bb center` at fwtip_l / fwtip_r; `small_flame` ×8 Δ(2.5,1.0,0.5) at ^ ^3.2 ^. **→ Dendro:** `tc:glow #B6E35A 1.5→4.5 l6/f3 bb center`; 2 × `tc:glow #E5FBC8 1.0→2.5 l5/f2` at the wing tips; `composter` ×8 Δ(2.5,1.0,0.5) | **→ Pyro:** `item.firecharge.use` 0.5/1.4, `block.respawn_anchor.set_spawn` 0.3/1.6. **→ Dendro:** `block.amethyst_block.resonate` 0.5/1.4, `block.azalea_leaves.place` 0.5/1.2 |
| 1-7 | `face/track`; Pyro patterns: `mv/away {d:0.25}` while within 6 b | while Pyro: every 4 t `small_flame` ×1 at each forewing tip (persistent rim embers, kept for the whole Pyro stretch from the module tick) | |
| 8 | `ai/go` → the pattern starts | | |

## 3. Persistent Pyro look

While `#bfLook 1` (in any state of the butterfly form), every 6 t:
- `small_flame` ×1 at fwtip_l and fwtip_r (anchors from the current pose: use the idle-b rest anchors ±4.7, 6.4, -1.8 in the body frame);
- `dust #E26E50 0.6` ×1 at the same points.

This is the footage's persistent rim glow. It stops at the switch back to Dendro and at the revert.

## 4. Notes

- The transformation sets Dendro at its t0 (`look/dendro`). B5 needs Dendro: if the last pattern was Pyro, the core's prep switches before B5 too (B5 has `el` Dendro).
- `look/flat` is for transform-in (if used) and the B5 / revert retract only; it is not an element.

## 5. Checks

- A switch happens only when the look differs.
- The pattern starts exactly 8 t later.
- The Dendro → Pyro → Dendro sequence leaves no leftover Pyro embers.
- Particles per switch ≤ 12; cards ≤ 3.
