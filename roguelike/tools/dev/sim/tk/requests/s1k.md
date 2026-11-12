# S1K requests and hand-off notes (branch wip/tk-s1k)

Committed: `tools/build_mboss_tk_fx.py`, `tools/mboss_tk_fx_paint.py`, `tools/mboss_tk_fx_manifest.json` (generated; its
presence switches `api.K` on), `tools/mboss_arena_tk_lift.py`, and the kit output `F:boss/tachy/fx/{card,cardx,look,clear,
uninstall}` + `fx/{e,p,snd,hud,prop,test}/**` (178 functions). No registry, core or `F:mboss/**` output. RP (built into
`S:tk/rp_s1k`): `assets/rlk/{textures,models/item,items}/mboss/tk_kit/*`, font `rlk:mboss_tk` (U+EA00-EAFF), 26 atlas
entries `rlk:mboss/tk_kit/*`. Tests `S:tk/tests/test_kit.py <wt>/roguelike [<rp>]`, `S:tk/tests/test_arena_tk.py
<wt>/roguelike` (harness `S:tk/tests/lib/tkfxsim.py`). Renders `S:tk/renders/s1k_*.jpg` (scripts `S:tk/s1k/render_*.py`).

## Requests
| # | what | why | affects |
|---|---|---|---|
| K1 | `api.KIT_SOUNDS` += `'wave_charge'` (`block.beacon.ambient` 0.6 / 1.8 + `block.respawn_anchor.charge` 0.6 / 1.0) | S4's R3 (W1 charge); the recipe `fx/snd/wave_charge` is already built (manifest `sounds_beyond_api`) | api.py, S4 (`p_air.py`: replace its two direct playsound lines by `K.snd('wave_charge')`) |
| K2 | registry `tachy.icon` = `{item:"minecraft:netherite_sword", model:"rlk:mboss/tk_kit/gate_icon"}` | the kit's gate icon (sword behind the visor skull) exists now | registry (lead, I1) |
| K3 | S3 `p_melee.py` B3 bangs: `fx_slash(3.2, PYRO, pitch=80)` draws the arc mostly below the floor (pitch tilts the aim down 80 deg; roll 0 keeps the blade plane flat about that aim). For an overhead chop use `roll=90, pitch=15` (the sweep runs from overhead down to the floor ahead; roll +90 = top -> bottom) | footage v5 32-40 "펑" chops | S3 |
| K4 | S3 `resume`: after a pause inside the mantle call `fx/p/cocoon {pct}` again (fx/clear, run by pause, removes the cocoon pool; badge / gauge are storage and survive). S4's R2 (the nova resume) uses `nova_swell {t:<rest>}`: any t works (life t + 6) | the cocoon is a long-lived card | S3 core.py |
| K5 | contract §2 names of the kit: objective `tkFx` (fake players `#n #cn #now #wd #c2 #roll #spin #life #fade #dly #dur #hit #pool #a #el #p #c #demo #dt`) + `tkFxS tkFxG tkFxH tkFxK tkFxD`; tags `rlk_tk_fx_c` (fx pool), `rlk_tk_fx_coc` (cocoon pool), `rlk_tk_fx_new/_go/_sh/_fd/_hit` (engine stages), `rlk_tk_fx_demo` (+ `_p<i>`, test props); storage `rlk:tk fx.{init,a,pa,ax,tgc,hud.badge,hud.gauge}` | contract text only | contract.md |

## Notes for the other stages
- **Executor points** (as S3's notes; documented per preset in the manifest): `slash_arc` pivots at the executor (S3: body +1.2,
  rotated as the body) with `{yaw,pitch}` offsets and `roll` about the aim (0 flat left -> right, 90 overhead -> down, 175 the
  reverse sweep), reach `r`; `spin_ring` at the executor (S3 +1.0); `thrust_trail` / `dash_trail` from the executor along the
  aim over `len` (dash at the feet = executor - 0.85); `glint` 0.4 b right / 1.4 b ahead; `core_flare` / `core_burst` at the
  chest; `cocoon` centre 1.1 b above the executor (the hovering body); `sky_arcs` / `bolt` / `shock_ring` / `dust_ring` /
  `arrive_rift` at the floor point; `ignite_blade` at the sword guard (blade up +y 2.2 b); `impact` at the hit point;
  `high_glint` at the hovering body; `ambient_dust` around the arena centre (particles only, ambient soft cap).
- **No floor decals**: no flat card lies on the floor; the rings (`shock_ring` +0.35, `nova_flash` -0.8 / -0.4 from the chest,
  `spin_ring` at the executor) are airborne shockwaves at the hit tick. `sky_arcs` end >= 0.8 b above the floor.
- **Element looks**: el 1 = orange flame tint `#FFA45A` + flame particles; el 3 = white-gold `#FFF0B0` + the crackle overlay
  `arc_e` / golden bolts + electric sparks. A card's growth always completes before its fade (the builder extends life).
- **HUD**: `hud/badge {el}` writes `rlk:mboss extra` = [badge] (root `{text:"",extra:[...]}` unstyled; the ◈ glyph sibling in
  `rlk:mboss_tk`, the name a plain sibling); `hud/gauge {pct}` appends 20 gold cells (pct / 5 lit) after the badge on the same
  name line; `hud/clear` empties both. S3 also shows the gauge as the bossui under-bar (`hud/bar_gauge`, `#buSub`): the lead may
  keep both or drop one.
- **arrive_rift**: the rift parts are kit item ids `rlk:mboss/tk_kit/rift_{void,rim,arc0..3}` whose item definitions point at
  S1's models `rlk:item/rift/{void,rim,arc_0..3}` when the pack holds them at kit build time, else at the kit's fallback (tear
  + glow + sky arcs). At I1 build the kit's RP after S1's `build_rift.py` (checked both ways; the datapack is the same).
- **Props** (S4): `crescent_h_{1,3}` = a face quad 7 x 1.65 b + a flat quad 7 x 3 b, centred on the display (fly it at floor
  + 0.825..0.9); `crescent_v_{1,3}` crossed quads 2.6 b; `feather` a vertical billboard 1.6 b (pitch ignored).
- **Arena tk_lift** (S1 adds `arenas.tk_lift` = `api.ARENA_SPEC`; checked with a local registry copy and
  `build_mboss_arena.emit`): 16 build slices (y 190..250 in 4-layer slabs, max 2 388 commands), look jobs `abyss` / `dust`
  2 slices each (2 269 cells; 688 + 631 / 530 + 514 commands), sentinel `(640,196,8) polished_deepslate`, 87 hidden lights
  (shaft floor, tower tops, cable tops, the roof). Floor block light 10 (the light layer `light[level=15]` at y 206 as the plan
  says; 12 needs the layer at y 204 or lower: the lead may change `LIGHT_Y`), no dark spawn cell in either look.
  `POINTS`: `centre start rift hang machine cable0..5` (the six intro cable anchors on the machine underside, y 228) for S2.
  No `entrance_layout` (the rift is the entrance). Loadcheck with the arena generated: 0 failures.
