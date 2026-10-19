// BODY region of the 아펩의 오아시스 파수꾼 rig (plan R4 parts 1-8 and 18-21): the trunk of both forms.
//   abdomen   P1 the rear body (dark plates on top, pale belly scales below) | P3 the robe stem hanging from the waist
//             to the water: dark teal front panel with the olive-gold curl inlay and white diamonds, a green back
//   hem_a/b   P1 the dark belly ribbons (upper / tips) | P3 the lower robe with its pointed flaps, the hem flare
//   chest     P1 the ribcage (pale rib slabs under the belly), the belly shell, the drooping lobes over the sac
//             | P3 the lower chest: lime plates in front, bottle-green back, pale rib-blades curling round the sides
//   shoulders P1 the hump (cowl continuation), the shoulder hooks with the square gold gems in raised frames, the pale
//             bark pauldrons | P3 the upper chest, gold square shoulder plates
//   core      P1 the belly sac Ø 1.4 (one model: glass + the emissive seed) | P3 the gold sternum + navel
//   crys_low / crys_back   P1 the gold spine and shoulder cones | P3 the lower / upper back emeralds, shoulder spikes
//   mantle_<s>_a/b   the shoulder flaps (P1) / carapace plates (P3): ONE model for both forms, tinted per form
// The f1104 "umbrella" (plan R2): identified as the B arms seen from behind / below (the up-turned gold-coned tips and the
// dark back with the lime rim are the B arms of v5 f1908), not the mantle; the mantle keeps its R4 scales (1.7 / 1.5).
//
// Region interface (every region module): REGION, PARTS, models() -> {model name: elements in model units},
// FORM_MODELS {part: {p1: model, p3: model}}, sprites() -> {name: sprite record (apep_materials sprite())}.
// Frames (apep_pose FRAMES): 'w' parts are authored in world axes about their joint as they sit in the reference stance
// (P1: CROUCH, P3: UPRIGHT); hem / mantle in their bone frame 'y' (model -Y along the bone). Blocks; toUnits() at the end.
//
// AP-R2 techniques (r2_body):
//   wrap lofts   the big hulls (hump, thorax, rear body, P3 chest / robe) are lofts whose side facets show ONE sprite
//                painted round the section (u = the azimuth, v = along the axis), so plate rows, scrolls and inlays run
//                continuously over the facets; the paint is light-corrected for the horizontal hulls (the item light
//                of the smooth surface over that of the facet) so the 16 facets do not read as bands.
//   rib bands    a curved band (a rib-blade, the ribcage scrolls, a belt) is a one-section loft that keeps only the
//                facets of its arc, a little outside the hull, with an alpha-cut wrap sprite: the band can slope and
//                taper inside the section while every quad keeps the 22.5-degree facet grid.
//   plates       leaf plates are slabs (painted alpha card + optional core) tilted in 22.5-degree steps over the hulls.
import {loft, slab, rockBox, toUnits, mirrorX, stroke, sdUnion, registerWrap, registerTile} from './mboss_shape_lib.mjs';
import {PART_SCALE} from './apep_pose.mjs';
import {PAL, C, clamp, smooth, mix, N, lift, sink, grey, autoSlot, sprite, onRect, onRectY, spriteSize, r16, sdLeaf, cone, ball, cells, secC, SLOT, TRANSPARENT} from './apep_materials.mjs';
import {cardZ, cardX} from './mboss_model_lib.mjs';

export const REGION = 'body';
export const PARTS = ['abdomen', 'hem_a', 'hem_b', 'chest', 'shoulders', 'core', 'crys_low', 'crys_back', 'mantle_l_a', 'mantle_r_a', 'mantle_l_b', 'mantle_r_b'];
const SP = {};
const D2R = Math.PI / 180;
const sinD = th => Math.sin(th * D2R), cosD = th => Math.cos(th * D2R);
// a card sprite over a shape rect (plane 'y' slabs map the sprite's top row to v0: onRectY)
const card = (name, rect, fn, ppb, forms, use = 'unique', plane = 'z') => {
  if (SP[name]) return name;
  const [w, h] = spriteSize(rect, ppb);
  SP[name] = sprite(w, h, ppb, (plane === 'y' ? onRectY : onRect)(rect, fn), forms, 'body', {use});
  return name;
};
const lineOut = (c, d, w, L) => (d > -w ? mix(c, L, .85) : c);
const oneSided = (els, keep) => { for (const e of els) for (const f of Object.keys(e.faces)) if (!keep.includes(f)) delete e.faces[f]; return els; };
const mirrorEls = els => mirrorX(els);
const sub3 = (a, b) => a.map((x, i) => x - b[i]);
const hsh = (i, j, s = 0) => { let n = (i * 374761393 + j * 668265263 + s * 2246822519) | 0; n = (n ^ (n >>> 13)) * 1274126177 | 0; return ((n ^ (n >>> 16)) >>> 0) / 4294967295; };

// ---- item light (two world lights, ambient 0.4; averaged over the yaw: the boss turns) ------------------------------------
const nrm3 = v => { const l = Math.hypot(...v); return v.map(x => x / l); };
const ML0 = nrm3([.2, 1, -.7]), ML1 = nrm3([-.2, 1, .7]);
const dot3 = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const mcShade = n => Math.min(1, .6 * (Math.max(0, dot3(n, ML0)) + Math.max(0, dot3(n, ML1))) + .4);
const FLT = Array.from({length: 201}, (_, i) => { const ny = -1 + i / 100, h = Math.sqrt(Math.max(0, 1 - ny * ny)); let s = 0;
  for (let j = 0; j < 72; j++) { const a = j * Math.PI / 36; s += mcShade([h * Math.cos(a), ny, h * Math.sin(a)]); } return s / 72; });
const FL = ny => { const x = (clamp(ny, -1, 1) + 1) * 100, i = Math.min(199, Math.floor(x)); return FLT[i] + (FLT[i + 1] - FLT[i]) * (x - i); };
const scl = (c, k) => [clamp(c[0] * k, 0, 255), clamp(c[1] * k, 0, 255), clamp(c[2] * k, 0, 255), c[3] ?? 255];

// ---- wrap lofts ---------------------------------------------------------------------------------------------------------
// The section of a station list at axial a (lerped): {r: [e1+, e2+, e1-, e2-], c: [c1, c2]}.
const arr4 = r => (Array.isArray(r) ? r : [r, r, r, r]);
function secAt(st, a) {
  const s = st.sorted || (st.sorted = [...st].sort((p, q) => p.a - q.a));
  let i = 0;
  while (i < s.length - 2 && a > s[i + 1].a) i++;
  const t = clamp((a - s[i].a) / ((s[i + 1].a - s[i].a) || 1)), L = (x, y) => x + (y - x) * t;
  const r0 = arr4(s[i].r), r1 = arr4(s[i + 1].r), c0 = s[i].c || [0, 0], c1 = s[i + 1].c || [0, 0];
  return {r: [0, 1, 2, 3].map(j => L(r0[j], r1[j])), c: [L(c0[0], c1[0]), L(c0[1], c1[1])]};
}
// the outline point of a section at angle th (quarter ellipses), section coords (e1, e2) incl. the centre
const secPt = (S, th) => { const c = cosD(th), s = sinD(th); return [S.c[0] + (c >= 0 ? S.r[0] : S.r[2]) * c, S.c[1] + (s >= 0 ? S.r[1] : S.r[3]) * s]; };
// e1 / e2 section coordinates + axial -> part (A-frame) point
const toP = (axis, a, x, y) => (axis === 'z' ? [x, y, a] : axis === 'y' ? [x, a, -y] : [a, y, -x]);
// A loft whose facets show one wrap sprite. painter(th (deg), a (axial), p (part point), S (section)) -> rgba | null.
// light: correct the facet light of horizontal hulls (axis z / x) toward the smooth surface's.
function wrapLoft(name, axis, stations, painter, {n = 16, ppb = 32, forms = 'p1', caps = '', ledgeTex = 'g_plate', seed = 0, skip = null, light = true, W = 0, H = 0, translucent = false, ledges = true, ledgeWrap = true} = {}) {
  const as = stations.map(s => s.a), aMin = Math.min(...as), aMax = Math.max(...as), L = aMax - aMin;
  if (!SP[name]) {
    // perimeter of the largest section (blocks) -> sprite width
    const per = Math.max(...stations.map(s => { const r = arr4(s.r); return Math.PI / 2 * (Math.hypot(r[0], r[1]) + Math.hypot(r[1], r[2]) + Math.hypot(r[2], r[3]) + Math.hypot(r[3], r[0])) / Math.SQRT2; }));
    const w = W || Math.min(512, Math.max(16, Math.ceil(per * ppb / 16) * 16)), h = H || r16(L * ppb);
    const fn = (s, t) => {
      const k = Math.min(n - 1, Math.floor(s * n)), th = (k - .5 + (s * n - k)) * 360 / n;
      const a = axis === 'y' ? aMax - t * L : aMin + t * L, S = secAt(stations, a), [x, y] = secPt(S, th);
      let c = painter(th, a, toP(axis, a, x, y), S);
      if (!c) return TRANSPARENT;
      if (light && axis !== 'y') c = scl(c, clamp(FL(sinD(th)) / FL(sinD(k * 360 / n)), .62, 1.6));
      return c;
    };
    registerWrap(name);
    SP[name] = sprite(w, h, ppb, fn, forms, 'body', {translucent});
  }
  const els = loft(axis, stations, {n, tex: ledgeWrap ? name : name, caps, ledgeTex: ledgeWrap ? '__ledge' : ledgeTex, seed, skip, ledges});
  return ledgeWrap ? ledgesToWrap(els, name, axis, n, aMin, aMax) : els;
}
// Ledge / cap quads of a wrap loft re-pointed at a thin strip of the wrap sprite at their azimuth and axial position, so
// the steps between sections take the colour of the facets beside them instead of a tile (no banding on round bodies).
const AXI = {x: 0, y: 1, z: 2};
function elCentre(e) {
  const c = [8 - (e.from[0] + e.to[0]) / 2, (e.from[1] + e.to[1]) / 2 - 8, (e.from[2] + e.to[2]) / 2 - 8];
  if (!e.rotation) return c;
  const {axis, angle, origin} = e.rotation, O = [8 - origin[0], origin[1] - 8, origin[2] - 8], g = (axis === 'x' ? angle : -angle) * D2R, cs = Math.cos(g), sn = Math.sin(g);
  const q = sub3(c, O), r = axis === 'x' ? [q[0], q[1] * cs - q[2] * sn, q[1] * sn + q[2] * cs] : axis === 'y' ? [q[0] * cs + q[2] * sn, q[1], -q[0] * sn + q[2] * cs] : [q[0] * cs - q[1] * sn, q[0] * sn + q[1] * cs, q[2]];
  return [r[0] + O[0], r[1] + O[1], r[2] + O[2]];
}
function ledgesToWrap(els, name, axis, n, aMin, aMax) {
  const ai = AXI[axis], L = aMax - aMin;
  for (const e of els) for (const f of Object.values(e.faces)) {
    if (f.texture !== '#__ledge') continue;
    const P = elCentre(e), a = P[ai];
    // section coordinates (e1, e2) of the centre -> azimuth -> facet slot
    const x = axis === 'z' ? P[0] : axis === 'y' ? P[0] : -P[2], y = axis === 'z' ? P[1] : axis === 'y' ? -P[2] : P[1];
    const th = (Math.atan2(y, x) / D2R + 360 + 180 / n) % 360, k = Math.min(n - 1, Math.floor(th / (360 / n)));
    const t = clamp(axis === 'y' ? (aMax - a) / L : (a - aMin) / L, .01, .99);
    f.texture = '#' + name;
    f.uv = [16 * (k + .3) / n, 16 * t - .05, 16 * (k + .7) / n, 16 * t + .05].map(v => Math.round(clamp(v, 0, 16) * 1e4) / 1e4);
    delete f.rotation;
  }
  return els;
}
// Station rows -> loft stations about a joint J. z-loft rows: [z, half width, top y, bottom y, centre y, box?, centre x?]
const zRows = (J, rows) => rows.map(([z, w, top, bot, cy, box = 0, cx = 0]) => ({a: z - J[2], r: [w, top - cy, w, cy - bot], c: [cx - J[0], cy - J[1]], box}));
// y-loft rows (vertical torso, e2 = forward): [y, half width, front reach, back reach, centre z, box?]
const yRows = (J, rows) => rows.map(([y, w, fr, bk, cz, box = 0]) => ({a: y - J[1], r: [w, fr, w, bk], c: [0, -(cz - J[2])], box}));

// ---- shingles: overlapping tongues pointing toward +V (U across, V along), cells cw x rl -----------------------------------
// -> {id, fu (0..1 across), fv (0..1 along the visible tongue), e (edge distance, blocks), inside}
function shingle(U, V, cw, rl, seed = 1, jit = .25) {
  const r = Math.floor(V / rl), off = (r & 1) * .5, cu = U / cw + off, ci = Math.floor(cu);
  const fu = cu - ci, fv = V / rl - r, id = hsh(ci, r, seed);
  const sh = (hsh(ci, r, seed + 3) - .5) * jit;                  // per-plate tip shift
  // tongue: full width at the front, tapering to a point at fv = 1 (+ jitter)
  const t = clamp(fv), half = .5 * (t < .45 ? 1 : Math.pow(Math.max(0, 1 - (t - .45) / .55), .75)) - .02;
  const du = Math.abs(fu - .5 - sh * t), e = (half - du) * cw;
  return {id, fu, fv, e, inside: e > 0, row: r, col: ci};
}

// ================================================= phase 1 (CROUCH, world axes about the joint) ================================
const J_ABD = [0, 2.8, 1.0], J_CH = [0, 3.14, -.01], J_SH = [0, 3.34, -1.21], J_CORE = [0, 2.2, -.85], J_CL = [0, 3.55, .55], J_CB = [0, 4.05, -.75];
// The P1 dorsal hull: one profile from behind the cowl to the tail root (world z: top / bottom / half width / centre y).
// The hump peaks at 4.56 b over the A / B roots (v2 f870: higher than the 4.44 cowl), the rear slopes to the tail root.
const P1HULL = [
  // z      w     top   bot   cy
  [-2.55, .92, 3.78, 2.8, 3.3], [-2.2, 1.3, 4.12, 2.5, 3.25], [-1.7, 1.58, 4.38, 2.3, 3.2], [-1.1, 1.72, 4.52, 2.22, 3.2],
  [-.5, 1.74, 4.56, 2.2, 3.2], [.1, 1.68, 4.5, 2.24, 3.2], [.7, 1.56, 4.36, 2.3, 3.2], [1.3, 1.38, 4.12, 2.36, 3.18],
  [1.9, 1.15, 3.8, 2.4, 3.1], [2.45, .86, 3.42, 2.38, 2.95], [2.95, .55, 3.02, 2.2, 2.65],
];
const hullAt = z => {
  const H = P1HULL;
  let i = 0;
  while (i < H.length - 2 && z > H[i + 1][0]) i++;
  const t = clamp((z - H[i][0]) / (H[i + 1][0] - H[i][0])), L = j => H[i][j] + (H[i + 1][j] - H[i][j]) * t;
  return {w: L(1), top: L(2), bot: L(3), cy: L(4)};
};
// the hull rows between z0 and z1 (world), tucked by `tk` (a neighbour's overlap stays inside), stepped every ~0.5 b
function hullRows(z0, z1, tk = 0, step = .5) {
  const n = Math.max(1, Math.round((z1 - z0) / step)), rows = [];
  for (let i = 0; i <= n; i++) { const z = z0 + (z1 - z0) * i / n, h = hullAt(z); rows.push([z, h.w - tk, h.top - tk, h.bot + tk, h.cy, .08]); }
  return rows;
}
// the hull surface height at (x, z) (top), world
const hullTop = (x, z) => { const h = hullAt(z), u = clamp(Math.abs(x) / h.w, 0, .999); return h.cy + (h.top - h.cy) * Math.sqrt(1 - u * u); };

// P1 dorsal paint: dark slate leaf-plates in rows (tongues pointing back), a pale bevel rim on each plate, black gaps; pale
// fish-scale rows on the underside (model.md §3.2, the 35 chest scales); world z and the arc length round the hull.
const SLATE = PAL.p1_slate, BARK = PAL.p1_bark, LINE = PAL.p1_line;
function p1Dorsal(th, z, y, x, {seed = 5} = {}) {
  const s = sinD(th), U = th * D2R * 1.55, V = z + 3;
  if (s < -.5) {
    // underside: pale fish scales (rows of small rounded scales, dark wedges between)
    const sc = shingle(U * 1.0, V, .32, .26, seed + 7, .1);
    let c = BARK(clamp(.25 + .25 * (sc.id - .5) + .35 * smooth(.2, 1, sc.fv)));
    if (!sc.inside || sc.e < .015) c = LINE(.55);
    return mix(c, SLATE(.7), smooth(-.5, -.62, s) * 0 + .15);
  }
  const sh = shingle(U, V, .62, .58, seed, .35);
  let t = .38 + .12 * (sh.id - .5) + .08 * (N.a(U * 3, V * 3) - .5);
  t += .2 * smooth(.25, 0, sh.fv);                                 // shadow under the previous plate's tip
  t -= .1 * smooth(.6, 1, sh.fv) * 0;
  t += .22 * smooth(.3, -.5, s);                                    // the flanks darker, the top lit by the game
  let c = SLATE(clamp(t, .05, .95));
  const vein = Math.abs(sh.fu - .5);
  if (vein < .025 && sh.fv > .2) c = SLATE(clamp(t + .12, 0, 1));
  if (sh.inside && sh.e < .035) c = mix(SLATE(.02), C('#8E967F'), .5 + .5 * smooth(.035, 0, sh.e));   // the pale bevel rim
  if (!sh.inside) c = SLATE(.92);
  // transition to the pale underside
  if (s < -.3) c = mix(c, LINE(.6), smooth(-.3, -.5, s));
  return c;
}
// P1 plate sprite (normalised rect -1..1): a dark slate leaf plate, rounded front (v = 1) to a pointed tip (v = -1),
// pale bevel rim, a raised midrib, side veins; dark under-edge line. Shared by every P1 plate (scaled per plate).
const UR = {u0: -1, u1: 1, v0: -1, v1: 1};
const sdTongue = (u, v) => { const t = clamp((1 - v) / 2), half = t < .4 ? Math.sqrt(Math.max(0, 1 - ((.4 - t) / .4) ** 2)) * .98 : Math.pow(Math.max(0, 1 - (t - .4) / .6), .8) * .98; return Math.max(Math.abs(u) - half, v - 1, -1 - v); };
function p1PlatePaint(u, v) {
  const d = sdTongue(u, v);
  if (d > 0) return null;
  let t = .42 + .1 * (N.b(u * 4, v * 4) - .5) + .12 * (1 - v) / 2;
  const vein = Math.abs(((v * 2.5 + Math.abs(u) * 1.6) % 1 + 1) % 1 - .5);
  if (vein < .05 && Math.abs(u) > .08) t += .07;
  if (Math.abs(u) < .05) t -= .14; else if (Math.abs(u) < .09) t += .06 * (u > 0 ? 1 : -1);
  let c = SLATE(clamp(t, .05, .95));
  if (d > -.09) c = mix(C('#8E967F'), C('#C3C8B0'), smooth(-.09, -.02, d) * .6);
  if (d > -.025) c = SLATE(.95);
  return c;
}
// slab of one leaf plate with a normalised sprite (painted over UR): centre (cu, cv) in the slab plane, half sizes hu x hv;
// so = -1 flips the shape along v (the sprite must be painted flipped too: plane 'y' plates pointing back)
function leafPlate(spriteName, sd, {plane, at, cu, cv, hu, hv, so = 1, half = .045, rot = null, cards = 'both', core = false, edge = 'g_plate', cell = .1}) {
  const R = {u0: cu - hu, u1: cu + hu, v0: cv - hv, v1: cv + hv};
  const sdf = (u, v) => sd((u - cu) / hu, so * (v - cv) / hv) * Math.min(hu, hv);
  return slab({plane, at, rect: R, sd: sdf, half, sprite: spriteName, edge, cell, core, rot, cards});
}

// ---- shoulders (joint J_SH): the hump, the dorsal plates, the bark pauldrons, the hooks + gems, the flank plates -------------
const PAUL_R = {u0: -1, u1: 1, v0: -1, v1: 1};
// pauldron plates: lobed rounded shells; pale bark with wood-grain contour swirls round two centres and a dark outline
const sdPauldron = (u, v) => { const r = Math.hypot(u / .97, v / .93), a = Math.atan2(v, u), lobe = v < -.2 ? .06 * Math.cos(a * 7) : 0; return (r - 1 + lobe) * .95; };
function pauldronPaint(u, v, {seed = 0} = {}) {
  const d = sdPauldron(u, v);
  if (d > 0) return null;
  const c1 = [-.25 + .1 * seed, .1], c2 = [.45, -.35];
  const r1 = Math.hypot(u - c1[0], (v - c1[1]) * 1.2), r2 = Math.hypot(u - c2[0], v - c2[1]);
  const sw = Math.min(Math.abs(Math.sin((r1 * 5.2 + .5 * N.d(u * 2 + seed, v * 2)) * Math.PI)), Math.abs(Math.sin((r2 * 6.5 + .4 * N.c(u * 2, v * 2 + seed)) * Math.PI)) + (r2 > .55 ? 1 : 0));
  let t = .14 + .1 * (N.e(u * 3 + seed, v * 3) - .5) + .18 * smooth(.2, -1, v) + .1 * smooth(-.4, -.9, d);
  let c = BARK(clamp(t, 0, .9));
  if (sw < .09) c = mix(c, LINE(.35), .55 * (1 - sw / .09));
  if (d > -.1) c = mix(c, BARK(.55), smooth(-.1, -.04, d));
  if (d > -.045) c = LINE(.75);
  return c;
}
// the hook: the dark shoulder plate curling forward into a hook over the gem (v1 f315, v2 f870); shape coords (z, y)
const HOOK = stroke([[.55, .55], [.0, .72], [-.55, .62], [-.92, .3], [-1.0, -.12], [-.82, -.45], [-.55, -.6]], t => .34 - .22 * t);
const HOOK_R = {u0: -1.4, u1: .95, v0: -.95, v1: 1.1};
const hookPaint = (u, v) => {
  const n = HOOK.near(u, v), hw = .34 - .22 * n.t;
  if (n.d > hw) return null;
  let c = SLATE(clamp(.38 + .2 * (N.a(u * 7, v * 7) - .5) + .25 * n.t * (n.s > 0 ? 1 : .5), 0, 1));
  if (n.d > hw - .06 && n.s < 0) c = mix(c, PAL.p1_seam(.25), .75);      // the pale-lime crescent seam on the inner curve
  else if (n.d > hw - .04) c = C('#8E967F');
  return c;
};
// pale bark shell paint (pauldrons): cream-grey with big irregular wood-grain contour bands and a dark outline at the rim
// (z, y world; a = the dome axis; r01 = 0 at the rim .. 1 at the top of the dome)
function barkShell(z, y, a, r01) {
  const f = Math.hypot((z + 1.6) * 1.1, (y - 3.05) * 1.35) + .45 * N.d(z * .9, y * .9) + .2 * r01;
  const band = Math.abs(((f * 3.1) % 1 + 1) % 1 - .5);
  let t = .16 + .1 * (N.e(z * 2, y * 2) - .5) + .2 * smooth(3.3, 2.3, y) - .08 * r01;
  let c = BARK(clamp(t, 0, .9));
  if (band < .055) c = mix(c, LINE(.3), .5 * (1 - band / .055));
  else if (band < .1) c = mix(c, BARK(.02), .35 * (1 - (band - .055) / .045));
  if (r01 < .07) c = mix(c, LINE(.7), smooth(.07, .02, r01));
  return c;
}
// a pauldron lobe (normalised, the tongue pointing down): bark with a contour band and a dark outline
function pauldronLobe(u, v) {
  const d = sdTongue(u, v);
  if (d > 0) return null;
  let c = BARK(clamp(.26 + .08 * (N.c(u * 3, v * 3) - .5) + .14 * smooth(.6, -.9, v), 0, .9));
  const band = Math.abs(Math.hypot(u, v - .9) * 1.7 % 1 - .5);
  if (band < .06 && v < .7) c = mix(c, LINE(.35), .45);
  if (d > -.1) c = LINE(.72);
  return c;
}
function shouldersP1() {
  const J = J_SH, els = [];
  // the hull (front hump), from under the cowl to the chest
  els.push(...wrapLoft('p1_hump_wrap', 'z', hullSt(J, [-2.55, -2.2, -1.75, -1.3, -.85, -.3, .02], -9, -.3), (th, a) => p1Hull('sh')(th, a + J[2]), {caps: '-', seed: 521, forms: 'p1', ppb: 36}));
  // dorsal shingle plates: rows along the spine, 3 across (the centre flat / pitched, the sides rolled 22.5 / 45 deg)
  const ps = card('p1_plate_y', UR, (u, v) => p1PlatePaint(u, -v), 40, 'p1', 'unique', 'y');
  const pz = card('p1_plate_z', UR, p1PlatePaint, 40, 'p1');
  for (const [z, pitch] of [[-2.1, -22.5], [-1.55, 0], [-1.0, 0], [-.45, 22.5]]) {
    const y0 = hullTop(0, z) + .04;
    els.push(...leafPlate(ps, sdTongue, {plane: 'y', at: y0 - J[1], cu: 0, cv: z - J[2], hu: .52, hv: .5, so: -1, rot: pitch ? ['x', pitch, [0, y0 - J[1], z - J[2]]] : null, cards: '+'}));
    for (const s of [1, -1]) {
      const x = .82 * s, y1 = hullTop(x, z + .1) + .03;
      const half = leafPlate(ps, sdTongue, {plane: 'y', at: y1 - J[1], cu: x, cv: z + .12 - J[2], hu: .46, hv: .48, so: -1, rot: ['z', -22.5 * s, [x, y1 - J[1], z + .12 - J[2]]], cards: '+'});
      els.push(...half);
      // flank plates (plane x, leaning in 45 deg), pointing back-down
      const xf = (hullAt(z + .2).w - .32) * s, yf = hullAt(z + .2).cy + .62;
      els.push(...leafPlate(pz, sdTongue, {plane: 'x', at: xf, cu: z + .2 - J[2], cv: yf - J[1], hu: .42, hv: .4, so: 1, rot: ['z', 45 * s, [xf, yf - J[1], z + .2 - J[2]]], cards: s > 0 ? '+' : '-'}));
    }
  }
  // the pale bark pauldron (v2 f870: a big pale shell capping the B-leg root under the A-arm root, wood-grain contour
  // bands, a dark outline): a lofted dome bulging out of the flank + two lobed plates layering its lower edge
  const half = [];
  // the shell: a z-loft (its outline round in the front view, tapering front and back), inner facets dropped (in the hull)
  const PD = [
    // z      out   up    in    down  cx    cy
    [-2.78, .16, .3, .1, .26, 1.45, 2.86], [-2.5, .44, .62, .2, .55, 1.47, 2.88], [-2.08, .6, .8, .3, .7, 1.5, 2.9],
    [-1.55, .63, .84, .3, .74, 1.52, 2.9], [-1.02, .54, .74, .28, .66, 1.5, 2.92], [-.62, .22, .38, .12, .32, 1.47, 2.95]];
  const pst = PD.map(([z, o, up, i, d, cx, cy]) => ({a: z - J[2], r: [o, up, i, d], c: [cx - J[0], cy - J[1]], box: .06}));
  const zA = PD[0][0], zB = PD[PD.length - 1][0];
  half.push(...wrapLoft('p1_pauld_wrap', 'z', pst, (th, a, p) => {
    const z = a + J[2], e = Math.min((cosD(th) + .42) / .5, (z - zA) / .32, (zB - z) / .32);
    return barkShell(z, p[1] + J[1], 0, clamp(e));
  }, {caps: '-+', ledgeTex: 'g_shell', seed: 524, ppb: 40, skip: (k, th) => cosD(th) < -.45}));
  // the lobed lower edge flaring out like a skirt: three rounded bark lobes (pointing down), dark outline
  const pl = card('p1_pauld_lobe', UR, (u, v) => pauldronLobe(u, v), 40, 'p1');
  for (const [cz, cy, x, hz, hy] of [[-2.32, 2.2, 1.9, .34, .36], [-1.76, 2.1, 1.98, .38, .4], [-1.18, 2.18, 1.92, .34, .36]]) {
    half.push(...leafPlate(pl, sdTongue, {plane: 'x', at: x, cu: cz - J[2], cv: cy - J[1], hu: hz, hv: hy, half: .045, core: true, edge: 'g_shell', cell: .09, rot: ['z', -22.5, [x, cy - J[1], cz - J[2]]]}));
  }
  // the hook + gem: a dark curl in front of the pauldron, the square gem in a raised dark frame facing out-forward
  const hs = card('p1_hook', HOOK_R, hookPaint, 48, 'p1');
  const hz0 = -2.35 - J[2], hy0 = 3.05 - J[1];
  half.push(...slab({plane: 'x', at: 1.62, rect: {u0: hz0 + HOOK_R.u0 * .7, u1: hz0 + HOOK_R.u1 * .7, v0: hy0 + HOOK_R.v0 * .7, v1: hy0 + HOOK_R.v1 * .7},
    sd: (u, v) => HOOK.sd((u - hz0) / .7, (v - hy0) / .7) * .7, half: .09, sprite: hs, edge: 'g_plate', cell: .08, rot: ['y', 22.5, [1.62, hy0, hz0]]}));
  const gz = -2.42 - J[2], gy = 2.98 - J[1];
  half.push(rockBox([1.6, gy - .2, gz - .2], [1.82, gy + .2, gz + .2], 'g_plate', {seed: 522, rot: ['y', 22.5, [1.7, gy, gz]]}));
  half.push(rockBox([1.74, gy - .14, gz - .14], [1.9, gy + .14, gz + .14], 'p1_gem', {seed: 523, rot: ['y', 22.5, [1.7, gy, gz]]}));
  // dark hanging plates over the flank behind the pauldron (over the C-leg root), pointed tips down
  const hp = pz;
  for (const [cz, cy, hz, hy] of [[-.15, 3.25, .42, .85], [.45, 3.1, .4, .8]]) {
    const x = hullAt(cz).w + .02;
    half.push(...leafPlate(hp, sdTongue, {plane: 'x', at: x, cu: cz - J[2], cv: cy - J[1], hu: hz, hv: hy, so: 1, rot: ['z', 22.5, [x, cy - J[1], cz - J[2]]], core: true, half: .05, cell: .12}));
  }
  els.push(...half, ...mirrorEls(half));
  return els;
}

// ---- the hull split by ownership: each part owns [o0, o1] of the dorsal hull and runs past it into its neighbours,
// tucked inside them (0.07 b + 0.12 b per b), so the S-coil / hoop bends stay closed and no two lofts share a facet plane
function hullSt(J, zs, o0, o1, grow = 0) {
  return zs.map(z => {
    const h = hullAt(z), tk = (z < o0 - 1e-6 ? .07 + .12 * (o0 - z) : z > o1 + 1e-6 ? .07 + .12 * (z - o1) : 0) - grow;
    return {a: z - J[2], r: [h.w - tk, h.top - h.cy - tk, h.w - tk, h.cy - h.bot - tk], c: [-J[0], h.cy - J[1]], box: .08};
  });
}
// the hull's bottom arc: signed arc length from the bottom midline (+ = the boss's left), blocks
const arcX = (th, z) => { const h = hullAt(z); return ((((th - 270) % 360) + 540) % 360 - 180) * D2R * (h.w + h.cy - h.bot) / 2; };
// The underside scrollwork of the thorax (v2 f480): pairs of pale scroll plates sweeping in from the flanks and curling
// into a spiral beside the midline, a dark central spine with pale lenses between the pairs, dark green-grey gaps.
const RIBZ = [-1.5, -.92, -.34, .24];
// one scroll: in from the flank sweeping back, curling into a spiral beside the midline (X, dz from the rib's z)
const SCROLL = stroke([[1.75, -.62], [1.4, -.44], [1.05, -.22], [.75, .0], [.5, .16], [.3, .16], [.2, .04], [.22, -.1], [.34, -.16], [.45, -.1], [.44, .0], [.36, .02]],
  t => .24 * Math.pow(1 - t, .65) + .03);
function ribUnder(X, z) {
  const ax = Math.abs(X);
  let best = null;
  for (const zi of RIBZ) { const n = SCROLL.near(ax, z - zi), hw = .24 * Math.pow(1 - n.t, .65) + .03, e = n.d - hw; if (!best || e < best.e) best = {e, t: n.t, s: n.s, hw}; }
  // the central spine: dark wedges with a pale lens between each pair
  const zr = (z + 1.5 + .29) / .58, fr = zr - Math.floor(zr);
  const lens = ax < .13 * Math.sin(Math.PI * clamp((fr - .2) / .6)) && z > -1.7 && z < .9;
  if (best.e < 0) {
    const inner = -best.e / best.hw;
    let c = BARK(clamp(.18 - .16 * smooth(.15, .7, inner) + .06 * (N.c(X * 4, z * 4) - .5) + .1 * best.t, 0, .9));
    if (Math.abs(best.s) < .012 && best.t < .8) c = mix(c, LINE(.35), .4);   // the grain line along the scroll
    if (best.e > -.05) c = mix(C('#4A5545'), C('#646E5C'), smooth(-.05, -.025, best.e));   // the thick dark outline
    return c;
  }
  if (lens) return mix(BARK(.1), BARK(.4), smooth(.13, 0, ax));
  const sh = smooth(.02, .16, -best.e);
  return mix(C('#5B6553'), C('#353D33'), .35 + .5 * sh + .15 * (N.b(X * 3, z * 3) - .5));
}
// cracked "dried mud" belly shell (the plate behind the sac, v2 f2040 item 8)
function crackedShell(X, z) {
  const c1 = cells(X * 3.2, z * 3.2, 77, 0, .9), e = c1.d2 - c1.d1;
  let c = BARK(clamp(.14 + .16 * c1.id + .1 * (N.e(X * 2, z * 2) - .5), 0, .9));
  if (e < .07) c = mix(LINE(.55), c, e / .07 * .6);
  return c;
}
// pale fish scales (the neck / chest underside, model.md item 35) and broad belly scales (the rear body)
function fishScales(X, z, big = false) {
  const sc = shingle(X, z + 3, big ? .5 : .3, big ? .36 : .24, big ? 13 : 7, .1);
  let c = BARK(clamp(.2 + .2 * (sc.id - .5) + .3 * smooth(.25, 1, sc.fv), 0, .95));
  if (!sc.inside || sc.e < .016) c = LINE(.5);
  return c;
}
// P1 hull paint: dorsal plates above, the region's underside below, a dark rim line between
function p1Hull(kind) {
  return (th, z) => {
    const s = sinD(th);
    if (s > -.42) return p1Dorsal(th, z);
    const X = arcX(th, z);
    let c;
    if (kind === 'ab') c = fishScales(X, z, true);
    else if (z < -1.62) c = fishScales(X, z);
    else c = Math.abs(X) < .34 && z > -.62 && z < .75 ? crackedShell(X, z) : ribUnder(X, z);
    if (s > -.5) c = mix(c, LINE(.8), smooth(-.5, -.42, s) * .8);
    return c;
  };
}

// ---- chest (joint J_CH): the mid-back hull with the underside ribcage + belly shell, the calyx cupping the sac ------------
// the calyx: pale grey lobes cupping the sac from below / behind (v2 f2040 item 7): a z-loft round the sac's lower half,
// its front edge cut into rounded lobes, contour lines, a dark outline
const SAC = {c: [0, 1.7, -1.0], r: .7};
function calyxPaint(th, z) {
  const tt = th < 90 ? th + 360 : th, lob = 5, ph = ((tt - 146.25) / 247.5) * lob, i = Math.floor(ph), f = ph - i;
  const lobeFront = -1.16 + .3 * Math.pow(Math.abs(f - .5) * 2, 1.6) + .05 * (i % 2);
  if (z < lobeFront) return null;
  const e = Math.min(z - lobeFront, Math.abs(f - .5) < .48 ? 9 : (.5 - Math.abs(f - .5)) * 1.2 + .015);
  let c = mix(C('#C7C8BA'), C('#8F9488'), clamp(.3 + .4 * (sinD(th) < 0 ? -sinD(th) : 0) + .2 * (N.d(th * .05, z * 3) - .5)));
  const band = Math.abs(((z - lobeFront) * 4.2 % 1) - .5);
  if (band < .07) c = mix(c, LINE(.4), .4);
  if (Math.abs(f - .5) > .47) c = mix(c, LINE(.6), .7);
  if (e < .045) c = LINE(.72);
  return c;
}
function chestP1() {
  const J = J_CH, els = [];
  els.push(...wrapLoft('p1_chest_wrap', 'z', hullSt(J, [-.72, -.3, .15, .6, .95, 1.25], -.3, .95), (th, a) => p1Hull('ch')(th, a + J[2]), {seed: 511, forms: 'p1', ppb: 40}));
  // the calyx round the sac
  const zs = [-1.18, -.92, -.66, -.45, -.3];
  const st = zs.map(z => { const d = z - SAC.c[2], r = Math.sqrt(Math.max(.02, SAC.r * SAC.r - d * d)) + .1; return {a: z - J[2], r: [r, r, r, r], c: [SAC.c[0] - J[0], SAC.c[1] - J[1]]}; });
  els.push(...wrapLoft('p1_calyx', 'z', st, (th, a) => calyxPaint(th, a + J[2]), {caps: '+', ledgeTex: 'g_shell', seed: 512, forms: 'p1', ppb: 40,
    skip: k => !(k >= 7 || k <= 1)}));
  return els;
}
// ---- core (joint J_CORE): the belly sac, Ø 1.4 (v2 f2040, f417): a yellow-green glass bulb, painted with its depth: a lit
// rim, a deeper glowing interior and the golden seed flower seen through the glass toward the front-below (the views
// that see it: the player in front, the rear-up), veins and a specular highlight. Opaque (no sorting artefacts); the
// glow is the core brightness channel (12 / 15).
const SEEDV = nrm3([0, -.55, -.83]);
const SEED_A = nrm3([1, 0, 0]), SEED_B = [SEEDV[1] * SEED_A[2] - SEEDV[2] * SEED_A[1], SEEDV[2] * SEED_A[0] - SEEDV[0] * SEED_A[2], SEEDV[0] * SEED_A[1] - SEEDV[1] * SEED_A[0]];
const SEEDP = stroke([[0, -.55], [0, .5]], t => .2 * Math.sin(Math.PI * Math.min(1, t * 1.15)) + .01);
function sacPaint(d) {
  // d: unit direction from the sac centre (part frame)
  const depth = dot3(d, SEEDV), u = dot3(d, SEED_A), v = dot3(d, SEED_B);
  let c = mix(C('#CFE39A'), C('#9BB060'), clamp(.5 - .45 * d[1]));                 // the glass body, darker below
  c = mix(c, C('#EEF8C8'), .5 * smooth(.7, 1, 1 - Math.abs(depth)));                  // a lit rim round the view axis
  if (depth > .1) {
    // the seed seen through the glass: a golden almond with a midrib, two leaf wings, soft edges (blurred by the glass)
    const k = 1 / (.35 + .65 * depth), su = u * k * .9, sv = v * k * .9;
    const n = SEEDP.near(su, sv), seed = n.d - (.2 * Math.sin(Math.PI * Math.min(1, n.t * 1.15)) + .01);
    const wing = Math.min(Math.hypot((Math.abs(su) - .3) / .22, (sv - .12) / .12) - 1, 9);
    const g = Math.max(smooth(.08, -.04, seed), .8 * smooth(.25, -.1, wing));
    const tone = PAL.p1_gold(clamp(.25 + .3 * (sv + .5) - .2 * smooth(.03, -.06, seed)));
    c = mix(c, tone, g * smooth(.1, .35, depth) * .85);
    if (Math.abs(su) < .025 && seed < 0) c = mix(c, PAL.p1_gold(.7), .6);
    c = mix(c, C('#F7FFD6'), .25 * smooth(.6, 1, depth) * (1 - g));                 // the glow behind the seed
  }
  const vein = Math.abs(((Math.atan2(d[0], -d[2]) / Math.PI * 4 + .4 * d[1] * d[1]) % 1 + 1) % 1 - .5);
  if (vein < .03) c = mix(c, C('#7E9446'), .45);
  const hl = Math.hypot((d[0] - .38) / .2, (d[1] - .62) / .16);                    // the specular highlight, upper left
  if (hl < 1) c = mix(c, C('#FCFFF2'), .85 * smooth(1, .45, hl));
  return c;
}
function coreP1() {
  const J = J_CORE, c = sub3(SAC.c, J);
  // lofted across (axis x): the two views that matter (the front, and from below in the rear-up) see facets, not ledges
  const ts = [-.98, -.86, -.62, -.3, 0, .3, .62, .86, .98];
  const st = ts.map(t => ({a: c[0] + t * SAC.r, r: SAC.r * Math.sqrt(1 - t * t), c: [-c[2], c[1]]}));
  return wrapLoft('p1_sac', 'x', st, (th, a, p) => sacPaint(nrm3(sub3(p, c))), {caps: '-+', ledgeTex: 'p1_core', seed: 531, forms: 'p1', light: false, ppb: 40});
}
// ---- abdomen (joint J_ABD): the rear body hull, back plates rising into spiky leaf points (v1 f720), belly scales ----------
function abdomenP1() {
  const J = J_ABD, els = [];
  els.push(...wrapLoft('p1_abd_wrap', 'z', hullSt(J, [.62, .95, 1.4, 1.9, 2.45, 2.95], .95, 3.2), (th, a) => p1Hull('ab')(th, a + J[2]), {caps: '+', seed: 501, forms: 'p1'}));
  // two rows of back plates, the rear ones lifting into points (plane y, pitched up at the back) + flank points
  const ps = card('p1_plate_y', UR, (u, v) => p1PlatePaint(u, -v), 40, 'p1', 'unique', 'y');
  const pz = card('p1_plate_z', UR, p1PlatePaint, 40, 'p1');
  for (const [z, pitch, hu, hv] of [[1.2, 22.5, .5, .5], [1.85, 22.5, .44, .5], [2.45, 45, .36, .46]]) {
    const y0 = hullTop(0, z) + .03;
    els.push(...leafPlate(ps, sdTongue, {plane: 'y', at: y0 - J[1], cu: 0, cv: z - J[2], hu, hv, so: -1, rot: ['x', -pitch, [0, y0 - J[1], z - .2 - J[2]]], cards: 'both', core: true, half: .04, cell: .12}));
  }
  const half = [];
  for (const [z, dy, hz, hy] of [[1.15, .1, .44, .55], [1.75, .05, .4, .5], [2.3, 0, .34, .42]]) {
    const h = hullAt(z), x = h.w * .78, y = h.cy + .55 + dy;
    half.push(...leafPlate(pz, sdTongue, {plane: 'x', at: x, cu: z - J[2], cv: y - J[1], hu: hz, hv: hy, rot: ['z', 45, [x, y - J[1], z - J[2]]], cards: '+'}));
  }
  els.push(...half, ...mirrorEls(half));
  return els;
}
// ---- gold crystals: lemon-gold faceted cones leaning back from a dark collar (the spine) / out (the shoulders) -------------
// A cone = a short dark 8-facet collar + two crossed crystal cards: the front card tilted back 22.5 deg about x, the side
// card showing the leaning profile (sheared triangle). The painted facets carry the light: a lit left facet, a shaded
// right facet, a bright ridge, a dark base line (model.md §8: 2-tone facets).
function crystalPaint(ramp, lean) {
  return (u, v) => {
    // u -1..1 across, v -1 (base) .. 1 (tip); the axis bends by lean * t^2
    const t = (v + 1) / 2, cx = lean * t * t, hw = .98 * (1 - t) + .02;
    const x = (u - cx) / hw;
    if (Math.abs(x) > 1 || v < -1 || v > 1) return null;
    let k = x < -.05 ? .08 + .25 * (1 + x) * .5 : .45 + .3 * x;
    k += .12 * (1 - t);
    let c = ramp(clamp(k, 0, 1));
    if (Math.abs(x + .05) < .08) c = mix(c, ramp(0), .7);                 // the ridge highlight
    if (Math.abs(x) > .88) c = ramp(.92);                               // the dark facet edges
    if (t < .06) c = ramp(.85);
    return c;
  };
}
function crystal(c, r, h, lean, ramp, tag, {side = 0} = {}) {
  // c: base centre; lean = the tip's offset toward +z (back) in units of h; side: the tip's offset toward +x (out)
  const els = [];
  els.push(...loft('y', [{a: c[1] - .05, r: r * 1.25, c: [c[0], -c[2]]}, {a: c[1] + .06, r: r * 1.12, c: [c[0], -c[2]]}], {n: 8, tex: 'g_plate', caps: '+', seed: 7}));
  const sf = card(`${tag}_cr_f`, UR, crystalPaint(ramp, side / r), 48, 'p1'), ss = card(`${tag}_cr_s`, UR, crystalPaint(ramp, -lean * h / r), 48, 'p1');
  els.push(cardZ(sf, c[2], {X0: c[0] - r, X1: c[0] + r, Y0: c[1], Y1: c[1] + h}, {rot: lean ? ['x', 22.5, [c[0], c[1], c[2]]] : undefined}));
  els.push(cardX(ss, c[0], {Z0: c[2] - r, Z1: c[2] + r, Y0: c[1], Y1: c[1] + h}));
  return els;
}
function crysLowP1() {
  const J = J_CL, els = [];
  for (const [z, r, h] of [[.82, .15, .56], [1.42, .12, .42]]) els.push(...crystal([0, hullTop(0, z) - .02 - J[1], z - J[2]], r, h, .4, PAL.p1_gold, 'p1g'));
  return els;
}
function crysBackP1() {
  const J = J_CB, els = [];
  for (const [z, r, h] of [[-1.82, .15, .52], [-1.18, .2, .78], [-.52, .18, .66], [.12, .15, .52]]) els.push(...crystal([0, hullTop(0, z) - .02 - J[1], z - J[2]], r, h, .4, PAL.p1_gold, 'p1g'));
  // the shoulder cones, out of the pauldron top (v2 f870 item 18), leaning out
  const half = crystal([1.72, 3.66 - J[1], -1.62 - J[2]], .15, .55, 0, PAL.p1_gold, 'p1gs', {side: .35});
  els.push(...half, ...mirrorEls(half));
  return els;
}

// the dark belly ribbons: three alpha strips hanging along -Y (the bone frame 'y'), one-sided (the front face; plan R18)
const RIB_R = {u0: -.2, u1: .2, v0: -1.5, v1: .05};
const ribbonPaint = tip => (u, v) => { const t = clamp(-v / 1.5), hw = tip ? .19 * (1 - t) + .01 : .19 - .03 * t; if (Math.abs(u) > hw) return null; let c = PAL.p1_slate(clamp(.55 + .25 * t + .1 * (N.a(u * 9, v * 6) - .5))); if (Math.abs(u) > hw - .03) c = lift(c, .18); if (Math.abs(u) < .015) c = sink(c, .25); return c; };
function ribbons(tip, len) {
  const sp = card(tip ? 'p1_ribbon_tip' : 'p1_ribbon', RIB_R, ribbonPaint(tip), 32, 'p1'), els = [];
  for (const [x, r, z] of [[-.45, 22.5, .02], [0, 0, -.02], [.45, -22.5, .02]]) {
    const e = cardZ(sp, z, {X0: x - .2, X1: x + .2, Y0: -len, Y1: .05}, {rot: r ? ['z', r, [x, 0, z]] : undefined});
    els.push(...oneSided([e], ['north']));
  }
  return els;
}
// ================================================= phase 3 (UPRIGHT, world axes about the joint) ===============================
const J3_ABD = [0, 3.11, .07], J3_CH = [0, 4.17, -.04], J3_SH = [0, 5.39, -.07], J3_CORE = [0, 4.82, -1.12], J3_CL = [0, 3.70, .47], J3_CB = [0, 5.73, .70];
// The P3 torso profile (v6 f480, v5 f1908; model_p3 §2.2): world y -> half width, front / back reach from the axis, axis z.
// Broad shoulders (2.6 b) narrowing to the 1.5 b waist, the ventral side forward.
const P3T = [
  // y      w     fr    bk    cz
  [2.75, .7, .6, .66, .02], [3.05, .74, .62, .7, -.02], [3.45, .82, .66, .74, -.05], [3.9, .96, .7, .8, -.06], [4.4, 1.1, .74, .85, -.05],
  [4.85, 1.22, .76, .88, -.05], [5.25, 1.3, .75, .9, -.06], [5.6, 1.22, .68, .84, -.08], [5.9, .98, .56, .7, -.1], [6.15, .64, .42, .52, -.12]];
const torsoAt = y => {
  const H = P3T;
  let i = 0;
  while (i < H.length - 2 && y > H[i + 1][0]) i++;
  const t = clamp((y - H[i][0]) / (H[i + 1][0] - H[i][0])), L = j => H[i][j] + (H[i + 1][j] - H[i][j]) * t;
  return {w: L(1), fr: L(2), bk: L(3), cz: L(4)};
};
function torsoSt(J, ys, o0, o1, grow = 0) {
  return ys.map(y => {
    const h = torsoAt(y), tk = (y < o0 - 1e-6 ? .06 + .12 * (o0 - y) : y > o1 + 1e-6 ? .06 + .12 * (y - o1) : 0) - grow;
    return {a: y - J[1], r: [h.w - tk, h.fr - tk, h.w - tk, h.bk - tk], c: [-J[0], -(h.cz - J[2])], box: .1};
  });
}
// ---- P3 paint ---------------------------------------------------------------------------------------------------------------
const BOT = PAL.p3_bottle, LIME = PAL.p3_lime, PALE = PAL.p3_pale, L3 = PAL.p3_line;
// glossy bottle-green dorsal plates (rounded leaves in rows pointing down), near-black rims, a lime line highlight
function p3Back(U, V, seed = 41) {
  const sh = shingle(U, V, .5, .44, seed, .3);
  let t = .58 + .1 * (sh.id - .5) + .1 * (N.a(U * 3, V * 3) - .5) - .25 * smooth(.5, 0, sh.fv) * 0;
  t += .22 * smooth(.3, 0, sh.fv);                                   // the shadow under the plate above
  t -= .22 * smooth(.5, .2, Math.abs(sh.fu - .38 - .1 * sh.fv)) * (1 - sh.fv);   // the glossy highlight streak
  let c = BOT(clamp(t, .1, .98));
  if (sh.inside && sh.e < .045) c = sh.e < .022 ? BOT(.98) : mix(PAL.p3_rim(.45), BOT(.5), .3);
  if (!sh.inside) c = BOT(1);
  return c;
}
// lime leaf plates (front / upper chest): broad leaves fanning out from the sternum, darker green veins and outlines
function p3Front(U, V, seed = 43) {
  const sh = shingle(U * .9, V, .62, .55, seed, .25);
  let c = LIME(clamp(.28 + .14 * (sh.id - .5) + .1 * (N.c(U * 3, V * 3) - .5) + .18 * smooth(.25, 0, sh.fv), 0, .95));
  const vein = Math.abs(sh.fu - .5);
  if (vein < .02) c = mix(c, L3(.4), .5);
  else { const sv = Math.abs(((sh.fv * 3 + vein * 2.5) % 1) - .5); if (sv < .05) c = mix(c, L3(.3), .3); }
  if (!sh.inside || sh.e < .022) c = L3(.6);
  return c;
}
// the torso wrap: back plates behind, lime plates in front, dark green on the flanks under the rib-blades
function p3Torso(th, y, kind) {
  const s = sinD(th), U = th * D2R * 1.1;
  if (s < -.25) return p3Back(U, 9 - y);
  let c = p3Front(U, 9 - y);
  const flank = smooth(.55, .2, s);
  c = mix(c, BOT(.62 + .1 * N.b(th * .05, y * 2)), flank * (kind === 'ch' ? .85 : .5));
  if (s < -.1) c = mix(c, BOT(.95), smooth(-.1, -.25, s));
  return c;
}
// ---- compact band lofts: a one-section loft keeping facets ks, its wrap sprite packed to those slots ---------------------
function bandLoft(name, axis, st, ks, painter, {n = 16, ppb = 40, forms = 'p3'} = {}) {
  const m = ks.length, as = st.map(s => s.a), aMin = Math.min(...as), aMax = Math.max(...as), L = aMax - aMin;
  if (!SP[name]) {
    const per = Math.max(...st.map(s => { const r = arr4(s.r); return Math.PI / 2 * (Math.hypot(r[0], r[1]) + Math.hypot(r[1], r[2]) + Math.hypot(r[2], r[3]) + Math.hypot(r[3], r[0])) / Math.SQRT2; }));
    const w = Math.min(512, Math.max(16, Math.ceil(per * m / n * ppb / 16) * 16)), h = r16(L * ppb);
    SP[name] = sprite(w, h, ppb, (s, t) => {
      const j = Math.min(m - 1, Math.floor(s * m)), k = ks[j], th = (k - .5 + (s * m - j)) * 360 / n;
      const a = axis === 'y' ? aMax - t * L : aMin + t * L, S = secAt(st, a), [x, y] = secPt(S, th);
      return painter(th, a, toP(axis, a, x, y)) || TRANSPARENT;
    }, forms, 'body');
  }
  const kk = ks.map(k => ((k % n) + n) % n);
  const els = loft(axis, st, {n, tex: name, seed: 3, skip: k => !kk.includes(k), ledges: false});
  for (const e of els) for (const f of Object.values(e.faces)) {
    if (f.texture !== '#' + name) continue;
    const k = Math.floor(Math.min(f.uv[0], f.uv[2]) * n / 16 + 1e-3), j = kk.indexOf(k);
    for (const i of [0, 2]) f.uv[i] = Math.round(((f.uv[i] - 16 * k / n) * n / m + 16 * j / m) * 1e4) / 1e4;
  }
  return els;
}
// ---- rib-blades: pale grey curved blades hugging the ribcage from the sternum edge round the side to the back, sloping
// down (v6 f480, model_p3 §2.2 item 8): band lofts a little outside the chest; wood-grain swirls, a dark outline, a lime
// stripe on the upper edge, the front end curling up beside the sternum.
const RIBS3 = [[4.98, 4.42, .17], [4.56, 3.98, .16], [4.14, 3.58, .14]];
function ribBlade(th, y, [yf, yb, w0]) {
  const t = clamp((92 - th) / 140), yc = yf + (yb - yf) * t * (.6 + .4 * t) + .07 * smooth(.12, 0, t), hw = w0 * (1 - .65 * t) + .02 * smooth(.9, 1, t);
  const d = Math.abs(y - yc) - hw;
  if (d > 0 || t >= 1 || th > 96) return null;
  const e = -d;
  let c = PALE(clamp(.12 + .12 * t + .1 * (N.d(th * .06, y * 4) - .5) + .12 * smooth(0, hw, y - yc + hw * .3) * 0, 0, .9));
  const grain = Math.abs((((y - yc) / hw * 2.2 + th * .02 + N.a(th * .03, y * 3)) % 1 + 1) % 1 - .5);
  if (grain < .07) c = mix(c, PALE(.6), .35);
  if (y > yc + hw - .045 && t < .85) c = mix(c, PAL.p3_rim(.4), .8);              // the lime upper edge
  if (e < .025) c = L3(.75);
  return c;
}
function chestP3() {
  const J = J3_CH, els = [];
  els.push(...wrapLoft('p3_chest_wrap', 'y', torsoSt(J, [3.0, 3.3, 3.7, 4.1, 4.5, 4.85, 5.15], 3.3, 4.85), (th, a) => p3Torso(th, a + J[1], 'ch'), {forms: 'p3', seed: 591, ppb: 36}));
  const half = [];
  RIBS3.forEach(([yf, yb, w0], i) => {
    const y0 = yb - w0 - .08, y1 = yf + w0 + .1, ym = (y0 + y1) / 2, h = torsoAt(ym), g = .06 + .02 * i;
    const st = [y0, y1].map(y => ({a: y - J[1], r: [h.w + g, h.fr + g, h.w + g, h.bk + g], c: [0, -(h.cz - J[2])]}));
    half.push(...bandLoft(`p3_rib${i}`, 'y', st, [13, 14, 15, 0, 1, 2, 3, 4], (th, a) => ribBlade(th, a + J[1], [yf, yb, w0])));
  });
  els.push(...half, ...mirrorEls(half));
  return els;
}
// shoulders (joint J3_SH): the upper chest (lime leaf plates fanning from the collar, the green back), square lime-gold
// gems in raised dark frames on both shoulders (v6 f90 / v5 f450)
function shouldersP3() {
  const J = J3_SH, els = [];
  els.push(...wrapLoft('p3_sh_wrap', 'y', torsoSt(J, [4.6, 4.85, 5.25, 5.6, 5.9, 6.15], 4.85, 9), (th, a) => p3Torso(th, a + J[1], 'sh'), {forms: 'p3', seed: 601, caps: '+', ppb: 36}));
  const half = [];
  const gy = 5.62 - J[1], gz = -.48 - J[2], gx = .98;
  half.push(rockBox([gx - .2, gy - .2, gz - .12], [gx + .2, gy + .2, gz + .08], 'g_plate', {seed: 602, rot: ['y', -22.5, [gx, gy, gz]]}));
  half.push(rockBox([gx - .14, gy - .14, gz - .17], [gx + .14, gy + .14, gz], 'p3_gem', {seed: 603, rot: ['y', -22.5, [gx, gy, gz]]}));
  els.push(...half, ...mirrorEls(half));
  return els;
}
// core (joint J3_CORE): the gold sternum (model_p3 §2.2 item 7): a dark-gold frame plate under a bright segmented plate, 7
// chevron segments with bevels, the diamond at the top, the navel glow at the bottom
const STERN_R = {u0: -.46, u1: .46, v0: -1.62, v1: .78};
const sternSd = (u, v) => { const w = .4 - .12 * clamp((-.42 - v) / 1.1) - .25 * clamp((v - .3) / .42); return Math.max(Math.abs(u) - w, v - .7, -1.52 - v); };
function sternPaint(u, v) {
  const d = sternSd(u, v);
  if (d > 0) return null;
  const seg = (v - Math.abs(u) * .65 + 1.52) * 3.1, i = Math.floor(seg), f = seg - i;
  let c = PAL.p3_sternum(clamp(.08 + .18 * f + .1 * (N.c(u * 6, v * 6) - .5) + .1 * (Math.abs(u) / .4), 0, 1));
  if (f < .14) c = PAL.p3_sternum(.82);                                   // the dark seam between chevrons
  else if (f < .24) c = PAL.p3_sternum(0);                                // the lit lip below it
  if (Math.abs(u) < .03 && v < .25) c = mix(c, C('#FFFFE8'), .6);         // the glowing centre vein
  if (v > .22 && Math.abs(u) + Math.abs(v - .48) * 1.1 < .19) c = Math.abs(u) + Math.abs(v - .48) * 1.1 < .1 ? C('#FFFFE8') : C('#F1F59A');
  return lineOut(c, d, .035, PAL.p3_sternum(.92));
}
const sternFrameSd = (u, v) => sternSd(u * .88, (v + .4) * .95 - .4) - .03;
function coreP3() {
  const els = [];
  els.push(...slab({plane: 'z', at: .36, rect: STERN_R, sd: sternFrameSd, half: .04, sprite: card('p3_sternframe', STERN_R, (u, v) => (sternFrameSd(u, v) > 0 ? null : PAL.p3_cone_gold(clamp(.72 + .15 * (N.b(u * 5, v * 5) - .5)))), 32, 'p3'), edge: 'p3_gold', cell: .12, cards: '-', core: true}));
  els.push(...slab({plane: 'z', at: .28, rect: STERN_R, sd: sternSd, half: .05, sprite: card('p3_sternum', STERN_R, sternPaint, 56, 'p3'), edge: 'p3_gold', cell: .1, cards: '-'}));
  // the navel: a glowing gold-lime knob under the sternum
  els.push(...ball([0, -1.74, .3], .17, 'p3_gold', {seed: 611}));
  return els;
}
// ---- emeralds (P3 crys parts, brightness 15): elongated octagonal cut gems pointing back, in a gold / dark frame ---------
const EMR = PAL.p3_emerald;
function gemPaint(th, a, a0, a1) {
  const t = clamp((a - a0) / (a1 - a0)), lit = Math.cos((th - 115) * D2R);
  let c = EMR(clamp(.62 - .3 * lit - .25 * t + .06 * N.a(th * .1, t * 4), 0, 1));
  if (t > .55 && Math.abs(lit - .9) < .12) c = mix(c, C('#F4FFD8'), .6);
  return c;
}
function emerald(name, c, rx, ry, depth, {frame = 'gold', spike = 0} = {}) {
  // c: the gem's base centre on the back surface; it grows toward +z (back)
  const st = [{a: c[2], r: [rx, ry, rx, ry], c: [c[0], c[1]]}, {a: c[2] + depth * .45, r: [rx * .92, ry * .92, rx * .92, ry * .92], c: [c[0], c[1]]}, {a: c[2] + depth, r: [rx * .25, ry * .25, rx * .25, ry * .25], c: [c[0], c[1]]}];
  const els = wrapLoft(name, 'z', st, (th, a) => gemPaint(th, a, c[2], c[2] + depth), {n: 8, caps: '+', forms: 'p3', light: false, ppb: 48});
  // the frame: a diamond ring behind the gem (+ a spike pointing down)
  const FR = {u0: -rx * 1.6, u1: rx * 1.6, v0: -ry * 1.5 - spike, v1: ry * 1.5};
  const outer = (u, v) => Math.max(Math.abs(u) / (rx * 1.45) + Math.abs(v) / (ry * 1.42) - 1, 0) * Math.min(rx, ry) - (spike && v < 0 && Math.abs(u) < .09 * (1 + (v + ry) / spike) ? 1 : 0);
  const sdF = (u, v) => { const o = Math.abs(u) / (rx * 1.45) + Math.abs(v) / (ry * 1.42) - 1, sp = spike && v < -ry * .5 ? Math.abs(u) - .1 * clamp(1 + (v + ry * 1.2) / spike) : 9; return Math.min(o * Math.min(rx, ry), sp); };
  const fs = card(`${name}_frame`, FR, (u, v) => { const d = sdF(u - c[0], v - c[1]); if (d > 0) return null; const inner = Math.abs(u - c[0]) / rx + Math.abs(v - c[1]) / ry; let col = frame === 'gold' ? PAL.p3_cone_gold(clamp(.35 + .3 * (v - c[1]) / -ry * .5 + .2 * N.c(u * 6, v * 6))) : BOT(.85); if (inner < 1.05) col = BOT(.95); if (d > -.03) col = frame === 'gold' ? PAL.p3_cone_gold(.85) : BOT(1); return col; }, 40, 'p3');
  void outer;
  els.push(...slab({plane: 'z', at: c[2] - .01, rect: {u0: c[0] + FR.u0, u1: c[0] + FR.u1, v0: c[1] + FR.v0, v1: c[1] + FR.v1}, sd: (u, v) => sdF(u - c[0], v - c[1]), half: .04, sprite: fs, edge: frame === 'gold' ? 'p3_gold' : 'g_plate', cell: .1, cards: '+'}));
  return els;
}
function crysLowP3() {
  // the lower-back emerald at the waist, 0.8 b, in a dark frame (v5 f1908)
  const J = J3_CL, y = 3.62, h = torsoAt(y);
  return emerald('p3_emr_low', [0, y - J[1], h.cz + h.bk - .04 - J[2]], .27, .4, .32, {frame: 'dark'});
}
function crysBackP3() {
  // the upper-back emerald between the shoulder blades, 1.0 b, in a gold frame with a spike (v5 f1908) + shoulder spikes
  const J = J3_CB, y = 5.32, h = torsoAt(y), els = [];
  els.push(...emerald('p3_emr_up', [0, y - J[1], h.cz + h.bk - .04 - J[2]], .33, .5, .38, {frame: 'gold', spike: .45}));
  const half = crystal([.92, 5.86 - J[1], .32 - J[2]], .11, .42, .5, PAL.p3_emerald, 'p3e');
  els.push(...half, ...mirrorEls(half));
  return els;
}
// ---- the robe (abdomen = the stem, hem_a = the lower robe, hem_b = the hem flare; model_p3 §2.2 items 10-12) ------------
// dark teal front panel with the olive-gold curl inlay framing it and white diamond emblems, a bottle-green back
const ROBE = PAL.p3_robe;
function robePanel(th, y, {diamonds = []} = {}) {
  const s = sinD(th), c0 = cosD(th);
  if (s < -.2) return p3Back(th * D2R * .8, 9 - y, 47);
  const X = c0 * .8;                                                      // across the front panel
  let c = ROBE(clamp(.45 + .12 * (N.a(X * 4, y * 2) - .5) + .2 * smooth(.6, .95, Math.abs(X)), 0, 1));
  // the olive-gold curl inlay: two wavy borders framing the panel, curling inward every 0.7 b
  const bx = .42 + .06 * Math.sin(y * 4.5), dB = Math.abs(Math.abs(X) - bx);
  const ph = ((y * 1.45) % 1 + 1) % 1, curl = Math.hypot(Math.abs(X) - (bx - .14), (ph - .5) * .7) - .09;
  if (dB < .025 || (Math.abs(curl) < .022 && Math.abs(X) < bx)) c = mix(c, C('#C9C27A'), .85);
  else if (dB < .045) c = mix(c, C('#7F8345'), .6);
  for (const yd of diamonds) { const dd = Math.abs(X) / .14 + Math.abs(y - yd) / .2; if (dd < 1) c = dd < .7 ? C('#F2F4EE') : C('#A9B7A6'); }
  if (s < 0) c = mix(c, BOT(.92), smooth(0, -.2, s));
  return c;
}
function abdomenP3() {
  const J = J3_ABD;
  const rows = [[3.5, .7, .62, .7], [3.1, .68, .6, .68], [2.5, .7, .62, .7], [1.9, .76, .68, .76], [1.35, .84, .75, .82], [.95, .9, .8, .88]];
  const st = rows.map(([y, w, fr, bk]) => ({a: y - J[1], r: [w, fr, w, bk], c: [0, -(.07 - J[2])], box: .1}));
  return wrapLoft('p3_stem_wrap', 'y', st, (th, a) => robePanel(th, a + J[1], {diamonds: [2.9, 2.25, 1.62]}), {forms: 'p3', seed: 561, caps: '+', ppb: 32});
}
// hem flaps: pointed dark teal leaves with an olive-gold edge and midrib (both sides painted)
const FLAP_R = UR;
const flapSd = (u, v) => sdLeaf(0, -1, .95, .9, {p: .7})(u, v);
function flapPaint(u, v) {
  const d = flapSd(u, v);
  if (d > 0) return null;
  let c = ROBE(clamp(.42 + .14 * (N.a(u * 5, v * 5) - .5) - .12 * v, 0, 1));
  const vein = Math.abs(((v * 2 + Math.abs(u) * 1.6) % 1 + 1) % 1 - .5);
  if (vein < .04 && Math.abs(u) > .08) c = mix(c, C('#7F8345'), .4);
  if (Math.abs(u) < .05) c = mix(c, C('#C9C27A'), .55);
  if (d > -.09) c = mix(c, C('#C9C27A'), .75);
  return c;
}
// hem_a (bone frame 'y': -Y down the bone; the joint 0.55 in front of the stem axis): the lower robe, a cone widening down,
// and three pointed flaps over its front
function hemAP3() {
  const els = [], cz = -.55;
  const st = [[.25, .74], [-.45, .86], [-1.0, .98], [-1.42, 1.06]].map(([y, r]) => ({a: y, r: [r, r * .88, r, r * .92], c: [0, cz]}));
  els.push(...wrapLoft('p3_hema_wrap', 'y', st, (th, a) => robePanel(th, a + 2.69, {diamonds: []}), {forms: 'p3', seed: 571, ppb: 32}));
  const fs = card('p3_hemflap', FLAP_R, flapPaint, 40, 'p3');
  for (const [x, ry, h] of [[0, 0, .6], [.46, 22.5, .52], [-.46, -22.5, .52]]) {
    const z = -.86 - .55 + .55, y = -1.0;
    els.push(...leafPlate(fs, flapSd, {plane: 'z', at: -.87 + (x ? .1 : 0), cu: x, cv: y, hu: .26, hv: h, half: .03, core: false, rot: ry ? ['y', -ry, [x, y, -.87]] : null}));
    void z;
  }
  return els;
}
// hem_b (bone frame 'y', 1.3 b down to the water): the hem flare and the pointed flaps splayed onto the water in six
// directions (model_p3 item 12; v6 f480), each flap tilted out 45 deg so the hem reads as a star from above
function hemBP3() {
  const els = [], cz = -.85;
  const st = [[.12, 1.0], [-.5, 1.18], [-.95, 1.36], [-1.13, 1.42]].map(([y, r]) => ({a: y, r, c: [0, cz]}));
  els.push(...wrapLoft('p3_hemb_wrap', 'y', st, (th, a) => robePanel(th, a + 1.3, {}), {forms: 'p3', seed: 581, ppb: 28}));
  const fs = card('p3_hemflap', FLAP_R, flapPaint, 40, 'p3');
  // front / back flaps (plane z, tilted 45 about x), side flaps (plane x, tilted 45 about z), four diagonal flaps upright
  const R = 1.42, yb = -1.05;
  els.push(...leafPlate(fs, flapSd, {plane: 'z', at: cz - R, cu: 0, cv: yb - .5, hu: .34, hv: .62, so: 1, half: .03, rot: ['x', -45, [0, yb, cz - R]]}));
  els.push(...leafPlate(fs, flapSd, {plane: 'z', at: cz + R, cu: 0, cv: yb - .5, hu: .34, hv: .62, so: 1, half: .03, rot: ['x', 45, [0, yb, cz + R]]}));
  for (const s of [1, -1]) els.push(...leafPlate(fs, flapSd, {plane: 'x', at: s * R, cu: cz, cv: yb - .5, hu: .34, hv: .62, so: 1, half: .03, rot: ['z', -45 * s, [s * R, yb, cz]]}));
  for (const [sx, sz] of [[1, 1], [1, -1], [-1, 1], [-1, -1]]) {
    const x = sx * R * .74, z = cz + sz * R * .74;
    els.push(...leafPlate(fs, flapSd, {plane: 'z', at: z, cu: x, cv: yb - .32, hu: .3, hv: .52, so: 1, half: .03, rot: ['y', sx * sz * 45, [x, 0, z]]}));
  }
  return els;
}
// ================================================= the mantle (both forms, bone frame 'y') ==================================
// A pointed leaf flap along -Y that curls toward model -Z (up in the crouch: the P1 collar of dark flaps whose tips curl up,
// "dark horns" at the cowl sides in v2 f2076; back in the upright: the P3 carapace wings over the shoulders): three
// segments at 0 / 22.5 / 45 deg, each a slab clipped from the one leaf outline so the sprite runs on unbroken. Outer face
// dark (slot plate), inner face pale with cream leaf-scale rows (slot shell, model.md item 34), a light rim on the outer
// face (slot band_a: pale in P1, mint-lime in P3).
const mantleSd = (L, W) => sdLeaf(0, -L, .05, W, {p: .62});
function mantleOut(L, W) {
  const sd = mantleSd(L, W);
  return (u, v) => {
    const d = sd(u, v);
    if (d > 0) return null;
    const t = -v / L;
    let g = .5 + .08 * (N.a(u * 5, v * 3) - .5) - .12 * t + .1 * smooth(.3, 0, Math.abs(u) / W);
    const vein = Math.abs(((v * 2.6 + Math.abs(u) * 2.2) % 1 + 1) % 1 - .5);
    if (vein < .045 && Math.abs(u) > .06) g -= .1;
    if (Math.abs(u) < .03) g -= .14; else if (Math.abs(u) < .06) g += .08;
    if (d > -.035) g = .3;
    return grey(g);
  };
}
function mantleIn(L, W) {
  const sd = mantleSd(L, W);
  return (u, v) => {
    const d = sd(u, v);
    if (d > 0) return null;
    // rows of cream leaf scales with dark wedges toward the rib
    const sc = shingle(Math.abs(u) + .02, -v, .2, .17, 31, .1);
    let g = .9 - .25 * smooth(.25, 1, sc.fv) + .04 * (sc.id - .5);
    if (!sc.inside || sc.e < .012) g = .5;
    if (Math.abs(u) < .03) g = .42;
    if (d > -.035) g = .38;
    return grey(g);
  };
}
function mantleRim(L, W) {
  const sd = mantleSd(L, W);
  return (u, v) => { const d = sd(u, v); if (d > 0 || d < -.06) return null; return grey(.95 - 3 * Math.abs(d + .03)); };
}
function mantle(L, W, tag) {
  const segs = [[0, .42], [.42, .72], [.72, 1]].map(([a, b]) => [a * L, b * L]), ang = [0, 22.5, 45];
  const rect = {u0: -W - .05, u1: W + .05, v0: -L - .05, v1: .1};
  const so = card(`g_flap_${tag}`, rect, mantleOut(L, W), 32, 'both', 'tinted'), si = card(`g_flapin_${tag}`, rect, mantleIn(L, W), 32, 'both', 'tinted');
  const sr = card(`g_flaprim_${tag}`, rect, mantleRim(L, W), 32, 'both', 'tinted');
  const sd = mantleSd(L, W), els = [];
  let y = 0, z = 0;                                       // the start of the current segment after the earlier bends
  segs.forEach(([s0, s1], i) => {
    const dy = y + s0, th = ang[i], R = {...rect, v0: rect.v0 + dy, v1: rect.v1 + dy};
    const clip = {v0: -s1 + dy - (i < 2 ? .03 : .06), v1: -s0 + dy + (i ? .03 : .1)};
    const sdf = (u, v) => sd(u, v - dy), rot = th ? ['x', th, [0, y, z]] : null;
    els.push(...slab({plane: 'z', at: z, rect: R, sd: sdf, half: .05, sprite: so, edge: 'g_plate', cell: .1, cards: '-', clip, rot}));
    els.push(...slab({plane: 'z', at: z, rect: R, sd: sdf, half: .05, sprite: si, edge: 'g_plate', cell: .1, cards: '+', core: false, clip, rot}));
    els.push(...slab({plane: 'z', at: z, rect: R, sd: sdf, half: .062, sprite: sr, edge: 'g_plate', cell: .1, cards: '-', core: false, clip, rot}));
    const len = s1 - s0;
    y -= len * Math.cos(th * D2R); z -= len * Math.sin(th * D2R);
  });
  for (const e of els) for (const f of Object.values(e.faces)) if (f.texture === `#g_flaprim_${tag}`) f.rim = true;
  return els;
}
// ---- region interface ------------------------------------------------------------------------------------------------------
let built = null;
export function models() {
  if (built) return built;
  const u = (els, n) => toUnits(autoSlot(els), PART_SCALE[n]);
  const out = {
    abdomen_p1: u(abdomenP1(), 'abdomen'), abdomen_p3: u(abdomenP3(), 'abdomen'),
    hem_a_p1: u(ribbons(false, 1.48), 'hem_a'), hem_a_p3: u(hemAP3(), 'hem_a'),
    hem_b_p1: u(ribbons(true, 1.2), 'hem_b'), hem_b_p3: u(hemBP3(), 'hem_b'),
    chest_p1: u(chestP1(), 'chest'), chest_p3: u(chestP3(), 'chest'),
    shoulders_p1: u(shouldersP1(), 'shoulders'), shoulders_p3: u(shouldersP3(), 'shoulders'),
    core_p1_bulb: u(coreP1(), 'core'), core_p3_sternum: u(coreP3(), 'core'),
    crys_low_p1: u(crysLowP1(), 'crys_low'), crys_low_p3: u(crysLowP3(), 'crys_low'),
    crys_back_p1: u(crysBackP1(), 'crys_back'), crys_back_p3: u(crysBackP3(), 'crys_back'),
  };
  // the mantle: one model per flap for both forms (tinted per form by its slots)
  const rimSlot = els => { for (const e of els) for (const f of Object.values(e.faces)) if (f.rim) { delete f.rim; f.tintindex = SLOT.band_a; } return els; };
  const um = (els, n) => toUnits(rimSlot(autoSlot(els)), PART_SCALE[n]);
  const ma = um(mantle(1.95, .56, 'a'), 'mantle_l_a'), mb = um(mantle(1.8, .5, 'b'), 'mantle_l_b');
  Object.assign(out, {mantle_l_a: ma, mantle_r_a: mirrorX(ma), mantle_l_b: mb, mantle_r_b: mirrorX(mb)});
  return (built = out);
}
export const FORM_MODELS = {
  abdomen: {p1: 'abdomen_p1', p3: 'abdomen_p3'}, hem_a: {p1: 'hem_a_p1', p3: 'hem_a_p3'}, hem_b: {p1: 'hem_b_p1', p3: 'hem_b_p3'},
  chest: {p1: 'chest_p1', p3: 'chest_p3'}, shoulders: {p1: 'shoulders_p1', p3: 'shoulders_p3'},
  crys_low: {p1: 'crys_low_p1', p3: 'crys_low_p3'}, crys_back: {p1: 'crys_back_p1', p3: 'crys_back_p3'},
  mantle_l_a: {p1: 'mantle_l_a', p3: 'mantle_l_a'}, mantle_r_a: {p1: 'mantle_r_a', p3: 'mantle_r_a'},
  mantle_l_b: {p1: 'mantle_l_b', p3: 'mantle_l_b'}, mantle_r_b: {p1: 'mantle_r_b', p3: 'mantle_r_b'},
};
// the core's own look channel (contract §0.4.7): p1_bulb / p3_sternum
export const CORE_MODELS = {p1_bulb: 'core_p1_bulb', p3_sternum: 'core_p3_sternum'};
export function sprites() { models(); return {...SP}; }
void [cosD, sdUnion, sink, cells, sub3, J_ABD, J_CH, J_CORE, J_CL, J_CB, yRows];
