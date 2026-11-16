# Shared rig libraries for the big bosses: `mboss_shape_lib.mjs` and the RIGLIB extras

The RIGLIB stage of the 야타용왕 (Azhdaha) plan (`az/plan.md` Rig decision change 2, §7) adds two things to the shared
display-entity rig libraries. Both are opt-in and back-compatible: the Guardian, butterfly and field generator rigs
build byte-identical outputs (§4).

- `tools/mboss_shape_lib.mjs` (new): the shape helpers of the Azhdaha R1 rig, promoted unchanged from
  `azhdaha_shape.mjs` @7c3e9fe (`wip/az-rig`). The Azhdaha rig (from R3) and the Apep rig import it.
- `tools/mboss_rig_compile.mjs`: a per-part translation tolerance `tol.tp`, plus rig-runtime helpers (part and shadow
  summons with a per-rig culling box and view range, follow lists per body state, `follow_y` sink offsets, the
  static-anchor follow skip, track fitting for the manifest's proxy columns, a culling-box check).

`mboss_rig_clips.mjs`, `mboss_model_lib.mjs`, `mboss_paint_lib.mjs` and `mboss_rig_math.mjs` are unchanged. Rig
branches do not edit these libraries; requests go to a RIGLIB stage, with a new identity proof.

## 1. Switching `azhdaha_shape.mjs` to the shim (R3)

Replace the whole file with:

```js
// Re-export shim: the shape helpers moved to the shared mboss_shape_lib.mjs (RIGLIB); kept so the region modules'
// imports stay valid.
export * from './mboss_shape_lib.mjs';
```

The region modules (`azhdaha_{head,body,legs,tail,materials}.mjs`) keep their imports. The tile and wrap registries
are the same objects through the shim. This was tested on R1 7c3e9fe: with the shim and the new `mboss_rig_compile.mjs`,
the datapack tree, the manifest and the whole resource pack are byte-identical to the R1 build (§4). Apep imports
`./mboss_shape_lib.mjs` directly. Its temporary `apep_shape.mjs` becomes the same shim.

## 2. `mboss_shape_lib.mjs`

**Units and frame.** Every helper works in **blocks** in the A-frame of one part: +X is the boss's left, +Y is up and
−Z is forward. The part's joint is at the origin. `toUnits(els, scale)` converts a part's elements to model units once,
at the end, where `scale` is the part's display scale (`PART_SCALE`): 1 b = 16 / scale units, and the reach is
1.5 × scale b. `checkBounds` (model lib) then guards −16..32.

| export | what |
|---|---|
| `toUnits(els, k)` | block-authored elements → model units for display scale `k`, about the pivot [8, 8, 8]. UVs are untouched. |
| `mirrorX(els)` | the mirror image of a paired part (`mirrorModel`). |
| `retex(els, map)` | the same elements with sprites renamed: `{old: new}` or `old => new`. Used for element looks as palette-swapped models. |
| `hash(...nums)` | a deterministic hash in [0, 1). |
| `TILE`, `registerTile(name, wPx, hPx, pxPerBlock, {fitU})` | the tile registry. A face of w × h b shows a (w·ppb) × (h·ppb) px window of the tile at a hashed offset, so rock reads continuous across facets of any size. `fitU` uses the full width. |
| `tileUV(name, wB, hB, seed)` | that window as a UV rectangle (0..16). An unregistered sprite gets [0, 0, 16, 16]. |
| `WRAP`, `registerWrap(name)` | sprites that a loft wraps round its facets: u is the facet k/n, v runs along the axis. |
| `loft(axis, stations, opt)` | a lofted convex solid, below. |
| `slab(opt)` | a flat painted shape with thickness, below. |
| `crossCards(sprite, c, w, h, {y0 = −h/2, three, flip, uvr})` | 2 (or 3, the third turned 45°) cards crossing on a vertical axis through `c`: leaf clusters, crystal sprays. |
| `rockBox(a, b, tex, {rot, seed, drop})` | a box with world-scaled tile windows per face. `tex` is a tile name or `{all, up, down, front, back, left, right}`. |
| `bez(p0, p1, p2, n = 16)` | the n + 1 points of a quadratic Bézier (2D). |
| `sdCircle(cx, cy, r)`, `sdPoly(P)`, `sdUnion(...f)`, `sdSub(a, b)` | 2D signed distances, negative inside. `sdPoly` is exact everywhere. **The names clash with `mboss_paint_lib.mjs`**, whose `sdPoly(P, near)` is a different function, so alias one set when you import both. |
| `stroke(pts, w)` | a tapered band along a polyline with half width `w(t)` (t = arc fraction): `{L, near(u, v) → {t, s, d}, sd}`. |
| `D2R` | π / 180. |

**`loft(axis, stations, opt)`.**
- `axis` is `'z'` (body, tail, neck; the section is left/up), `'y'` (limbs; left/forward) or `'x'` (across;
  forward/up).
- A station is `{a, r, c, box}`:
  - `a`: the position along the axis;
  - `r`: a radius or the quarter-ellipse semi-axes `[e1+, e2+, e1−, e2−]`;
  - `c`: the `[c1, c2]` centre offset;
  - `box`: 0 for a round profile .. 1 for square corners.
- Each section between two stations takes the profile of its midpoint. Sections are 16-gons (or 8) whose facet normals
  sit on the 22.5° grid.
- Steps between sections are closed by recessed ledge quads (staggered against z-fighting), and the ends by caps.
  Sections overlap by 0.02 b.

Options:

| option | default | meaning |
|---|---|---|
| `n` | 16 | 16 or 8 facets |
| `tex` | — | a tile sprite, or `(k, theta, i) => sprite` (e.g. cream on the belly facets) |
| `caps` | `''` | `'-'`, `'+'` or `'-+'` |
| `ledgeTex` | `tex` | the sprite of the step quads |
| `seed` | 0 | the UV hash seed |
| `skip` | — | `(k, theta, i) => true` leaves a facet out |
| `stagger` | 0.004 | the ledge stagger |
| `grow` | 0 | added to every radius |
| `ledges` | true | close the steps between sections |
| `tint` | false | `tintindex 0` on every face |

**`slab(opt)`.** Builds a flat shape from the signed distance `sd(u, v)`. Each face gets an alpha-cut painted card
showing the exact silhouette, over a core of greedy-meshed boxes eroded inside the same shape. Used for plates, horns,
shards, talons, teeth and beards.

Plane coordinates:

| `plane` | (u, v) | mid-plane |
|---|---|---|
| `'x'` | (Z, Y) | X = `at` |
| `'z'` | (X, Y) | Z = `at` |
| `'y'` | (X, Z) | Y = `at` |

`rect {u0, u1, v0, v1}` is the sprite's area. The sprite painter uses the same coordinates.

Options:

| option | default | meaning |
|---|---|---|
| `half` | 0.1 | the half thickness, or a taper `{along: 'u' \| 'v', bands, h: t => half}` |
| `sprite` | — | the card sprite |
| `edge` | — | the core faces' sprite |
| `cell` | 0.12 | the core voxel size |
| `inset` | 0.6 | the erosion, in cells |
| `core` | true | false gives cards only |
| `rot` | null | one `[axis, deg, pivot]` element rotation for everything |
| `cards` | `'both'` | `'both'`, `'+'` or `'-'` |
| `eps` | 0.012 | how far the cards sit off the core |
| `clip` | — | `{u0?, u1?, v0?, v1?}`: build only that part of the shape, with the sprite still mapped over the whole `rect` |
| `tint` | false | `tintindex 0` on the cards |

**Registries are module state**, one per build process. A rig registers its tiles before it builds its models. Two
rigs built in one process need distinct sprite names.

## 3. Extras in `mboss_rig_compile.mjs`

### 3.1 `tol.tp`: translation tolerance per part

```js
createRigCompiler({..., tol: {t: .012, s: .015, rDefault: 1, r: {...}, tp: {t1: .03, t2: .03, chest: .03}}})
```

- `close()` uses `tol.tp[part] ?? tol.t`. Without `tp` nothing changes.
- An unknown part name in `tp` throws.
- Use about 0.03 b on the long tail and torso parts and keep 0.012 on the head and paws (`az/understand/rigtech.md`
  §2.8: the probe burrow went from 23.5 to 11.1 keys/t). In the self-check, a 6 b segment swinging 60° in 30 t went
  from 19 to 10 keys at 0.035 b.
- The first segment of a clip is still the forced blend-in (≥ `blend` ticks).

### 3.2 Summons: per-rig culling box and view range

```js
summonPart({uuid, tags, item, brightness, pose, viewRange = 3, cull = {width: 16, height: 16}, sky = 15})
summonShadow({uuid, tags, item, radius = 4.5, strength = .8, viewRange = 3, cull = {width: 16, height: 16}})
cullOverhang([x, y, z], cull)   // blocks outside the box (> 0), for the builder's per-clip extents check
```

- `summonPart` writes the existing rigs' part summon string. `uuid` is the int-array SNBT or `[a, b, c, d]`, `tags` a
  list and `pose` a display transform `{t, q, s}`. It reproduces every part summon of the four shipped rigs (Guardian
  29, butterfly 30, field generator 29, Azhdaha R1 46).
- Azhdaha passes `cull: {width: 30, height: 12}, viewRange: 3` (R4). Apep passes `{width: 30, height: 16}`.
- `summonShadow` is the empty-model shadow display (rigtech §2.7). Its radius is at most 64. Azhdaha keeps UUID slot
  0x40.
- `cullOverhang` is **radial**. The culling box is axis-aligned in world space and does not turn with the yaw, so
  hypot(x, z) ≤ width / 2 is the condition that holds at every yaw. R1's per-axis check under-reports at diagonal yaws
  by up to 41 %. Buried points (y < 0) do not count, and width or height 0 means culling is off.

### 3.3 Follow: per-state lists, `follow_y` sink offsets, static-anchor skip

```js
const F = createRigFollow({ns: NS, obj: 'azRig', fn, uuidOf: n => (n === 'shadow' ? SHADOW_UUID : uuidOf(n)),
  lists: {all: PART_NAMES, tail_only: TAIL_PARTS, burrowed: []},   // id 0, 1, 2 (unset score = the first)
  fixed: ['shadow'],                                               // follows every list at the anchor, never sunk
  sink: [-.5, -1, -1.5, ...],                                      // follow_y<k> offsets in blocks, k = 1..n
  staticSkip: true});
F.write();                          // the function files below
F.objectives                        // add to init, remove in uninstall: azRigFl, azRigFy, azRigQ, azRigQx/Qy/Qz/Qw
F.listLines('tail_only')            // commands for state/<name>: select the list (and invalidate the cache)
F.sinkLines(k)                      // select offset k (0 = none)
F.sinkExtra(t => dyOf(clip, t), clip.len)   // extraLines for compileClip (merge with your own)
F.info()                            // lists, fixed, sink table, objectives, functions: for the manifest
```

| function | what |
|---|---|
| `follow` | Runs each tick, as and rotated as the anchor at its feet, pitch 0, as today. With `staticSkip`: 4 `data get` + 1 compare, and it returns while the anchor's x, y, z and yaw (×100, as ints) equal those of the last follow that ran. Otherwise it dispatches on `<obj>Fy` (≥ 1: `follow/sink`) and on `<obj>Fl` (the list). |
| `follow_now` | Invalidates the cache, then runs `follow`. Use it in spawn, after a state change and after anything that moved the parts. |
| `follow/<list>` | One `tp <uuid> ~ ~ ~ ~ ~` per part of the list, plus the `fixed` names. |
| `follow/<list>_y<k>` | The same list sunk by dy_k (`tp <uuid> ~ ~<dy> ~ ~ ~`). The `fixed` names stay at the anchor. |
| `follow/sink`, `follow/<list>_y[/a_b]` | The dispatch trees, with at most 6 leaves per file. |

- **Classic form.** With one list, no `sink` and no `staticSkip`, `write()` writes only the classic `follow` (the
  comment and the tp lines), byte-identical to what the rigs write today. `S:riglib/r3_consumer_patch.py` switches the
  R1 builder to `summonPart` / `summonShadow` / `createRigFollow` in this form with no output change. R3 can start
  from it.
- **Selecting a list or an offset.** `listLines` and `sinkLines` reset `<obj>Qx`, so a change of list or offset always
  moves the parts on the next follow, even while the anchor stands still.
- **Showing parts again.** Select the full list ≥ 1 tick before a clip shows the hidden parts, so they never slide in
  from where they were left.
- **Sink timing (`sinkExtra`).** `rig/tick` runs `follow` before the clip's keys, so the line written at tick t
  selects dy(t + 1) (`lead` = 1, the third argument). The parts are then at dy(t) on every tick t ≥ 1, in step with the
  keys. Tick 0 follows with the offset that is in force when the clip starts (normally 0). A clip that starts sunk keeps
  its parts hidden on tick 0, or the caller selects the offset before `play`.
- **Offsets are outside the pose.** The pose keeps the root unsunk, and the builder adds dy(t) in its own pose checks
  and proxy points. The hidden-state root z offset of Rig decision change 1 stays in the pose: hidden parts cost no
  keys.
- **Static skip granularity.** The cache works on 0.01 b / 0.01° steps, so parts can lag by less than 0.01 b. The ×100
  ints limit the coordinates to |x|, |z| < 21 M blocks. The arenas are near x 200, z 25.

### 3.4 Tracks: proxy columns and tail points as keys + lerp

```js
fitTrack(samples, {tol = .15})   // -> [[t, sample], ...]
fitTracks(samplesByTick, opt)    // samplesByTick[t] = {name: sample} -> {name: keys}
trackAt(keys, t)                 // the value at tick t
```

- **Samples.** `samples[t]` (t = 0..len) is a number, an array, an object such as `proxyPoints()`'s
  `{x, z, base, top, w, hidden?}`, or `null` (parked).
- **Interpolation.** Number fields lerp. Every other field (a flag such as `hidden`, the key set, a null) switches:
  where it changes between t − 1 and t, both ticks are keys.
- **Tolerance.** `tol` is a number for every number field, or `{x: .15, z: .15, top: .3, default: 0}`. Constant fields
  fit exactly.
- **Keys.** The fit is greedy, like the part segments. The first and last ticks are always keys, and linear
  interpolation reproduces every sample within `tol`.
- **Where the keys go.** This is the "px track compile" of FW-17: the rig writes the keys into the manifest (`px`
  `{x, z, top}` keys + `lerp`, plan §3.6), and the framework compiles them into its `px/*` functions (plan §3.3). The
  rig owns no proxy runtime.

## 4. Proofs (RIGLIB, on M0 = 99bc097)

Scripts and logs are in `S:riglib/` (scratchpad `riglib/`).

| check | result |
|---|---|
| The Guardian, butterfly and field generator rigs rebuilt (painted) into an M0 copy (`before/`) and into a copy with the new libraries (`after/`), with `build_rigs.sh` and `hash_rigs.sh` | Identical: RP textures, item models and item definitions per rig; DP `F:mboss/<rig>/rig/**` (1429 / 1150 / 2936 files); the three manifests; the Guardian screen font; `atlases/items.json`. `diff -r` of the whole datapack trees (minus the changed library sources) and of the whole RPs is empty. The M0 rebuild also equals the committed tree and the shipped RP `rp_final9`. |
| The builders' self-checks (`checkBounds`, step and segment rotation limits, alignment and floor checks, atlas budgets) | All pass on both builds. The warnings (3 Guardian half-tick notes) are the same as on M0. |
| The Azhdaha R1 rig (7c3e9fe) with `azhdaha_shape.mjs` as the shim and the new `mboss_rig_compile.mjs` (`r1b/`) | The datapack tree, the manifest and the whole RP are byte-identical to the R1 build (`r1a/`), which equals commit 7c3e9fe. |
| The R1 builder switched to `summonPart` / `summonShadow` / `createRigFollow` (classic) by `r3_consumer_patch.py` (`r1c/`) | Byte-identical outputs. |
| `tests/test_riglib.mjs`: tol.tp, tracks, follow files, summons, culling and the shape-lib exports | 28 checks. |
| `tests/run_follow.py`: the follow functions in the scratch mcfunction interpreter (`mb3/tests/mcsim.py` + UUID targets) | 16 checks: lists, fixed shadow, sink trees, static skip, follow_now, and a sinking clip through `rig/tick` (offset = dy(t) on every clip tick t ≥ 1). |
