// Shape helpers of the 야타용왕 (Azhdaha) rig, shared by the four region modules azhdaha_{head,body,legs,tail}.mjs.
// Built on mboss_model_lib.mjs (unchanged); everything here is Azhdaha-local, so the other rigs never see it.
//
// Every helper works in BLOCKS in the A-frame of one part (+X = the boss's left, +Y up, -Z forward, the part's joint
// at the origin). A part's elements are converted to model units once, by toUnits(els, scale), where scale is the
// part's display scale (azhdaha_pose.mjs PART_SCALE): 1 block = 16 / scale units, reach = 1.5 * scale blocks.
//
// Primitives
//   loft(axis, stations, opt)   a lofted convex solid: cross-sections are 16-gons (or 8-gons) whose facet normals sit
//                               on the 22.5 degree grid (the only element rotations Minecraft allows), circumscribed
//                               about a rounded rectangle / quarter-ellipse profile per station. Steps between
//                               sections are closed by ledge quads, the ends by caps. Facets show a tile sprite at a
//                               fixed texel density (world-scaled sub-rectangles, hashed offsets): rock hide reads
//                               continuous across facets of different sizes.
//   slab(opt)                   a flat shape extruded about a plane: a painted alpha-cut card on each face (the exact
//                               silhouette from the main view) over a core of greedy-meshed boxes eroded inside the
//                               same signed-distance shape (the thickness from the other views). Optional taper bands.
//                               Plates, horn sleeves, dark horns, shards, talons, teeth, beard plates.
//   crossCards(opt)             two or three cards crossing on a vertical axis (leaf clusters, crystal sprays).
//   rockBox(a, b, tile, opt)    a box whose faces show world-scaled sub-rectangles of a tile sprite.
//   retex(els, map)             the same elements with sprites renamed (element looks = palette-swapped models).
//   mirrorX(els)                mirror image (the right side of a paired part), via mboss_model_lib.mirrorModel.
import {abox, cardX, cardZ, cardY, faceEl, rotA, mirrorModel, r4, faceOfDir} from './mboss_model_lib.mjs';

export const D2R = Math.PI / 180;
const add = (a, b) => a.map((x, i) => x + b[i]), sub = (a, b) => a.map((x, i) => x - b[i]);
const sc = (v, s) => v.map(x => x * s), dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];

// ---- units -----------------------------------------------------------------------------------------------------------
// Block-authored elements -> model units for display scale k (about the pivot [8, 8, 8]; uv untouched).
export function toUnits(els, k) {
  const f = 16 / k, m = v => v.map(x => r4(8 + (x - 8) * f));
  return els.map(e => {
    const o = {...e, from: m(e.from), to: m(e.to)};
    if (e.rotation) o.rotation = {...e.rotation, origin: m(e.rotation.origin)};
    return o;
  });
}
export const mirrorX = els => mirrorModel(els);
// Rename sprites (element looks): map {old: new} or a function old -> new.
export function retex(els, map) {
  const f = typeof map === 'function' ? map : n => map[n] ?? n;
  return els.map(e => ({...e, faces: Object.fromEntries(Object.entries(e.faces).map(([k, fc]) => [k, {...fc, texture: '#' + f(fc.texture.slice(1))}]))}));
}
// Small deterministic hash in 0..1.
export const hash = (...a) => { let h = 2166136261; for (const x of a) { h ^= Math.round(x * 1000) | 0; h = Math.imul(h, 16777619); } h ^= h >>> 13; h = Math.imul(h, 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; };

// ---- tile sprites ------------------------------------------------------------------------------------------------------
// TILE registry: sprite name -> [width px, height px, px per block]. Region modules register their tiles here so the
// loft / rockBox UV maps know the texel density. A face of w x h blocks shows a (w ppb) x (h ppb) px window of the
// tile at a hashed offset (clamped inside the tile; faces larger than the tile stretch).
export const TILE = {};
export const registerTile = (name, w, h, ppb, opt = {}) => { TILE[name] = [w, h, ppb, opt]; };
export function tileUV(name, wB, hB, seed) {
  const t = TILE[name];
  if (!t) return [0, 0, 16, 16];
  const [W, H, ppb, opt = {}] = t, du = opt.fitU ? 1 : Math.min(1, wB * ppb / W), dv = Math.min(1, hB * ppb / H);
  const u0 = (1 - du) * hash(seed, 1.7), v0 = (1 - dv) * hash(seed, 9.3);
  return [u0 * 16, v0 * 16, (u0 + du) * 16, (v0 + dv) * 16].map(r4);
}

// ---- loft ---------------------------------------------------------------------------------------------------------------
// Axis frames: A along the loft, e1 / e2 span the cross-section (theta measured from e1 toward e2).
const FR = {
  z: {A: [0, 0, 1], e1: [1, 0, 0], e2: [0, 1, 0]},     // body, tail, neck: e1 = left, e2 = up
  y: {A: [0, 1, 0], e1: [1, 0, 0], e2: [0, 0, -1]},    // limbs: e1 = left, e2 = forward
  x: {A: [1, 0, 0], e1: [0, 0, -1], e2: [0, 1, 0]},    // across: e1 = forward, e2 = up
};
const AX = {x: [1, 0, 0], y: [0, 1, 0], z: [0, 0, 1]};
// Support distance of a station's profile for the normal angle th (deg): quarter ellipses with semi-axes r = [e1+,
// e2+, e1-, e2-], blended toward the bounding rectangle by `box` (0 round .. 1 square corners).
function support(st, th) {
  const c = Math.cos(th * D2R), s = Math.sin(th * D2R);
  const a = c >= 0 ? st.r[0] : st.r[2], b = s >= 0 ? st.r[1] : st.r[3];
  const ell = Math.hypot(a * c, b * s), rect = Math.abs(a * c) + Math.abs(b * s);
  return ell + (st.box || 0) * (rect - ell);
}
// Station: {a (axial position), r: number | [e1+, e2+, e1-, e2-], c: [c1, c2] centre offset, box}. Sections run
// between consecutive stations with the profile of their midpoint (lerped). Options:
//   n          facets per section (16 or 8)
//   tex        tile sprite (string) or fn(k, theta, i) -> sprite (e.g. cream on the underside facets)
//   caps       '-' / '+' / '-+': close the first / last station
//   ledgeTex   sprite of the step quads (default tex)
//   seed       uv hash seed
//   skip       fn(k, theta, i) -> true to leave a facet out (hidden inside another solid)
export const WRAP = new Set();
export const registerWrap = name => WRAP.add(name);
export function loft(axis, stations, {n = 16, tex, caps = '', ledgeTex = null, seed = 0, skip = null, stagger = .004, grow = 0, ledges = true, tint = false} = {}) {
  const aMin = Math.min(...stations.map(s => s.a)), aMax = Math.max(...stations.map(s => s.a));
  const {A, e1, e2} = FR[axis], els = [];
  const N = k => { const th = k * 360 / n; return [th, add(sc(e1, Math.cos(th * D2R)), sc(e2, Math.sin(th * D2R)))]; };
  // per section: the profile at its midpoint
  const secs = [];
  for (let i = 0; i < stations.length - 1; i++) {
    const s0 = stations[i], s1 = stations[i + 1], L = (x, y) => x + (y - x) * .5;
    const rr = j => L(arr(s0.r)[j], arr(s1.r)[j]) + grow;
    secs.push({a0: s0.a, a1: s1.a, r: [rr(0), rr(1), rr(2), rr(3)], c: [L((s0.c || [0, 0])[0], (s1.c || [0, 0])[0]), L((s0.c || [0, 0])[1], (s1.c || [0, 0])[1])], box: L(s0.box || 0, s1.box || 0)});
  }
  const poly = sec => {
    // facet lines x.n_k = h_k (2D coords in e1/e2 about the section centre); vertices between facets k and k+1
    const h = [], nn = [];
    for (let k = 0; k < n; k++) { const [th] = N(k); h.push(support(sec, th)); nn.push([Math.cos(th * D2R), Math.sin(th * D2R)]); }
    const V = [];
    for (let k = 0; k < n; k++) {
      const j = (k + 1) % n, [a1, b1] = nn[k], [a2, b2] = nn[j], det = a1 * b2 - a2 * b1;
      V.push([(h[k] * b2 - h[j] * b1) / det, (a1 * h[j] - a2 * h[k]) / det]);
    }
    return {h, V};
  };
  const P = secs.map(poly);
  const texOf = (k, i) => (typeof tex === 'function' ? tex(k, k * 360 / n, i) : tex);
  const lt = (k, i) => ledgeTex || texOf(k, i);
  const OV = .02;   // every section reaches OV past its ends (the steps never open a slit)
  const cen = sec => add(sc(e1, sec.c[0]), sc(e2, sec.c[1]));
  for (let i = 0; i < secs.length; i++) {
    const sec = secs[i], {V} = P[i], C = cen(sec);
    for (let k = 0; k < n; k++) {
      const [th, nk] = N(k);
      if (skip && skip(k, th, i)) continue;
      const v0 = V[(k - 1 + n) % n], v1 = V[k];
      const w = Math.hypot(v1[0] - v0[0], v1[1] - v0[1]);
      if (w < 1e-4) continue;
      const m = add(C, add(sc(e1, (v0[0] + v1[0]) / 2), sc(e2, (v0[1] + v1[1]) / 2)));
      const lo = Math.min(sec.a0, sec.a1), hi = Math.max(sec.a0, sec.a1), dn = sec.a1 < sec.a0;
      const exLo = dn ? i < secs.length - 1 : i > 0, exHi = dn ? i > 0 : i < secs.length - 1;
      const tx = texOf(k, i), A0 = lo - (exLo ? OV : 0), A1 = hi + (exHi ? OV : 0);
      const wuv = WRAP.has(tx) ? (() => { const f = a => (axis === 'y' ? (aMax - a) : (a - aMin)) / (aMax - aMin); const va = f(A0), vb = f(A1);
        return [16 * k / n, 16 * Math.min(va, vb), 16 * (k + 1) / n, 16 * Math.max(va, vb)]; })() : null;
      els.push(facet(axis, nk, m, w, A0, A1, tx, seed * 131 + i * 17 + k, C, wuv));
    }
  }
  // ledges between sections: recessed into the bigger section, staggered against z-fighting where neighbours overlap
  for (let i = 0; i < (ledges ? secs.length - 1 : 0); i++) {
    const sa = secs[i], sb = secs[i + 1], Ca = cen(sa), Cb = cen(sb);
    for (let k = 0; k < n; k++) {
      const [th, nk] = N(k);
      const ha = P[i].h[k] + dot(Ca, nk), hb = P[i + 1].h[k] + dot(Cb, nk);
      if (Math.abs(ha - hb) < 2e-3) continue;
      const big = ha > hb ? i : i + 1, small = big === i ? i + 1 : i, bmid = (secs[big].a0 + secs[big].a1) / 2, face = bmid > sa.a1 ? -1 : 1;
      if (skip && skip(k, th, small)) continue;
      const pB = P[big], CB = cen(secs[big]);
      const v0 = pB.V[(k - 1 + n) % n], v1 = pB.V[k], w = Math.hypot(v1[0] - v0[0], v1[1] - v0[1]);
      const mt = add(CB, add(sc(e1, (v0[0] + v1[0]) / 2), sc(e2, (v0[1] + v1[1]) / 2)));
      const a = sa.a1 - face * stagger * (1 + (k % 4));
      els.push(ledge(axis, nk, mt, w, Math.min(ha, hb) - .03, Math.max(ha, hb), a, face, lt(k, small), seed * 71 + i * 13 + k));
    }
  }
  // caps: a central rectangle plus a ring of quads from 0.3 h outward (stepped further in, so they win the overlap)
  for (let [end, i, face] of [['-', 0, -1], ['+', secs.length - 1, 1]]) {
    if (!caps.includes(end)) continue;
    const pp = P[i], sx = secs[i], Cx = cen(sx), a0 = end === '-' ? sx.a0 : sx.a1;
    face = Math.sign(a0 - (sx.a0 + sx.a1) / 2);
    const hx = j => support(sx, j * 90) * .65;
    const lo = add(add(Cx, sc(e1, -hx(2))), sc(e2, -hx(3))), hi = add(add(Cx, sc(e1, hx(0))), sc(e2, hx(1)));
    const ac = a0 - face * stagger * 6;
    const uvc = tileUV(lt(0, i), hx(0) + hx(2), hx(1) + hx(3), seed * 29 + i);
    const P0 = add(lo, sc(A, ac - dot(lo, A))), P1 = add(hi, sc(A, ac - dot(hi, A)));
    const fnc = X => [uvc[0] + (uvc[2] - uvc[0]) * (dot(sub(X, P0), e1) / Math.max(1e-6, dot(sub(P1, P0), e1))), uvc[1] + (uvc[3] - uvc[1]) * (dot(sub(X, P0), e2) / Math.max(1e-6, dot(sub(P1, P0), e2)))];
    els.push(faceEl([P0, P1], {[faceOfDir(sc(A, face))]: {tex: lt(0, i), fn: fnc}}, {shade: true}));
    for (let k = 0; k < n; k++) {
      const [, nk] = N(k);
      const v0 = pp.V[(k - 1 + n) % n], v1 = pp.V[k], w = Math.hypot(v1[0] - v0[0], v1[1] - v0[1]);
      const mt = add(Cx, add(sc(e1, (v0[0] + v1[0]) / 2), sc(e2, (v0[1] + v1[1]) / 2)));
      const c0 = dot(Cx, nk);
      els.push(ledge(axis, nk, mt, w, c0 + pp.h[k] * .3, c0 + pp.h[k], a0 - face * stagger * (1 + (k % 4)), face, lt(k, i), seed * 53 + k + i));
    }
  }
  if (tint) for (const e of els) for (const f of Object.values(e.faces)) f.tintindex = 0;
  return els;
}
const arr = r => (Array.isArray(r) ? r : [r, r, r, r]);
// The rotation g (deg, multiple of 22.5 within +-45) about AX[axis] and the axis-aligned direction d with rotA(axis, g, d) = nk.
function quant(axis, nk) {
  const cands = [];
  for (const d of [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]) {
    if (Math.abs(dot(d, AX[axis])) > .5) continue;
    for (const g of [0, 22.5, -22.5, 45, -45]) { const r = rotA(axis, g, d); if (Math.hypot(...sub(r, nk)) < 1e-6) cands.push([d, g]); }
  }
  if (!cands.length) throw new Error('facet normal off the 22.5 degree grid: ' + nk);
  cands.sort((x, y) => Math.abs(x[1]) - Math.abs(y[1]));
  return cands[0];
}
// Facet quad: centre m (3D, on the facet), normal nk, tangent width w, axial a0..a1. O = rotation origin (on the axis).
function facet(axis, nk, m, w, a0, a1, tex, seed, O0, wuv = null) {
  const dims = {u: w, v: a1 - a0};
  const A = AX[axis], [d, g] = quant(axis, nk);
  const O = add(O0, sc(A, (a0 + a1) / 2));
  const m0 = add(O, rotA(axis, -g, sub(add(m, sc(A, (a0 + a1) / 2 - dot(m, A))), O)));   // unrotated centre
  const t = rotA(axis, 0, crossv(A, d));                                                  // tangent of the unrotated quad
  const P = (a, s) => add(add(m0, sc(A, a - dot(m0, A))), sc(t, s));
  const uv = wuv || tileUV(tex, dims.u, dims.v, seed);
  const fn = X => { const s = dot(sub(X, m0), t) / w + .5, v = (dot(X, A) - a0) / (a1 - a0);
    return [uv[0] + (uv[2] - uv[0]) * s, uv[1] + (uv[3] - uv[1]) * (axis === 'y' ? 1 - v : v)]; };
  return faceEl([P(a0, -w / 2), P(a1, w / 2)], {[faceOfDir(d)]: {tex, fn}}, {shade: true, rot: g ? [axis, g, O] : undefined});
}
const crossv = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
// Step / cap quad in the plane a (axial), radial band [h0, h1] along nk (from the axis), tangent width w round the
// facet centre mt, facing +/-A.
function ledge(axis, nk, mt, w, h0, h1, a, face, tex, seed) {
  const A = AX[axis], [d, g] = quant(axis, nk);
  const O = sc(A, a);
  const t = crossv(A, d);
  // facet-centre tangential offset (in the rotated frame) is dot(mt, t_rot); unrotate the band into the d frame
  const tr = rotA(axis, g, t), s0 = dot(mt, tr);
  const P = (r, s) => add(O, add(sc(d, r), sc(t, s)));
  const uv = tileUV(tex, w, Math.max(.05, h1 - h0), seed);
  const fn = X => { const s = (dot(X, t) - s0) / w + .5, r = (dot(X, d) - h0) / Math.max(1e-6, h1 - h0); return [uv[0] + (uv[2] - uv[0]) * s, uv[1] + (uv[3] - uv[1]) * (1 - r)]; };
  return faceEl([P(h0, s0 - w / 2), P(h1, s0 + w / 2)], {[faceOfDir(sc(A, face))]: {tex, fn}}, {shade: true, rot: g ? [axis, g, O] : undefined});
}

// ---- slab ---------------------------------------------------------------------------------------------------------------
// Shape coordinates (u, v) per plane: 'x' -> (Z, Y) mid-plane X = at; 'z' -> (X, Y) mid-plane Z = at; 'y' -> (X, Z)
// mid-plane Y = at. rect {u0, u1, v0, v1} = the sprite's area (the painter of the sprite uses the same coordinates:
// spriteOn(rect, ...) in the region modules). sd(u, v) < 0 inside.
//   half       half thickness (blocks), or taper {along: 'u' | 'v', bands: n, h: t (0..1 along the axis) -> half}
//   cell       core voxel size; inset: erosion in cells (core stays inside the painted outline)
//   core       false: cards only (thin plates)
//   edge       sprite of the core faces (the visible rim from oblique views)
//   rot        [axis, deg, pivot] one element rotation for everything (22.5 degree steps)
//   cards      'both' | '+' | '-' : which faces get a card (+ = the +X / +Z / +Y side)
export function slab({plane, at = 0, rect, sd, half = .1, sprite, edge, cell = .12, inset = .6, core = true, rot = null, cards = 'both', eps = .012, clip = null, tint = false}) {
  if (clip) {
    // only the part of the shape inside clip (blocks, the same u/v), the sprite still mapped over the whole rect
    const c = {u0: Math.max(rect.u0, clip.u0 ?? rect.u0), u1: Math.min(rect.u1, clip.u1 ?? rect.u1), v0: Math.max(rect.v0, clip.v0 ?? rect.v0), v1: Math.min(rect.v1, clip.v1 ?? rect.v1)};
    const fu = x => (x - rect.u0) / (rect.u1 - rect.u0), fv = y => (rect.v1 - y) / (rect.v1 - rect.v0), fz = z => (z - rect.v0) / (rect.v1 - rect.v0);
    const uvBase = plane === 'y' ? [fu(c.u0), fz(c.v0), fu(c.u1), fz(c.v1)] : [fu(c.u0), fv(c.v1), fu(c.u1), fv(c.v0)];
    return slabIn({plane, at, rect: c, uvBase, sd, half, sprite, edge, cell, inset, core, rot, cards, eps, tint});
  }
  return slabIn({plane, at, rect, uvBase: [0, 0, 1, 1], sd, half, sprite, edge, cell, inset, core, rot, cards, eps, tint});
}
function slabIn({plane, at, rect, uvBase, sd, half, sprite, edge, cell, inset, core, rot, cards, eps, tint}) {
  const els = [], {u0, u1, v0, v1} = rect;
  const sub_ = (a, b, x) => a + (b - a) * x;
  const bands = typeof half === 'number' ? [{lo: 0, hi: 1, h: half}] : Array.from({length: half.bands}, (_, j) => ({lo: j / half.bands, hi: (j + 1) / half.bands, h: half.h((j + .5) / half.bands)}));
  const along = typeof half === 'number' ? 'u' : half.along;
  for (const b of bands) {
    // the band's slice of the rect
    const R = along === 'u' ? {u0: u0 + (u1 - u0) * b.lo, u1: u0 + (u1 - u0) * b.hi, v0, v1} : {u0, u1, v0: v1 - (v1 - v0) * b.hi, v1: v1 - (v1 - v0) * b.lo};
    const uvr0 = along === 'u' ? [b.lo, 0, b.hi, 1] : [0, b.lo, 1, b.hi];
    const uvr = [sub_(uvBase[0], uvBase[2], uvr0[0]), sub_(uvBase[1], uvBase[3], uvr0[1]), sub_(uvBase[0], uvBase[2], uvr0[2]), sub_(uvBase[1], uvBase[3], uvr0[3])];
    for (const sgn of [1, -1]) {
      if (cards !== 'both' && cards !== (sgn > 0 ? '+' : '-')) continue;
      const o = at + sgn * (b.h + eps);
      if (plane === 'x') els.push(cardX(sprite, o, {Z0: R.u0, Z1: R.u1, Y0: R.v0, Y1: R.v1}, {uvr, rot, tint}));
      else if (plane === 'z') els.push(cardZ(sprite, o, {X0: R.u0, X1: R.u1, Y0: R.v0, Y1: R.v1}, {uvr, rot, tint}));
      else els.push(cardYuv(sprite, o, R, uvr, rot, tint));
    }
    if (!core) continue;
    // greedy mesh of the eroded shape inside this band
    const nu = Math.max(1, Math.round((R.u1 - R.u0) / cell)), nv = Math.max(1, Math.round((R.v1 - R.v0) / cell));
    const cu = (R.u1 - R.u0) / nu, cv = (R.v1 - R.v0) / nv, er = inset * Math.min(cu, cv);
    const inside = Array.from({length: nv}, (_, j) => Array.from({length: nu}, (_, i) => sd(R.u0 + (i + .5) * cu, R.v0 + (j + .5) * cv) < -er));
    const used = inside.map(r => r.map(() => false));
    for (let j = 0; j < nv; j++) for (let i = 0; i < nu; i++) {
      if (!inside[j][i] || used[j][i]) continue;
      let i1 = i; while (i1 + 1 < nu && inside[j][i1 + 1] && !used[j][i1 + 1]) i1++;
      let j1 = j; const rowOk = jj => { for (let x = i; x <= i1; x++) if (!inside[jj][x] || used[jj][x]) return false; return true; };
      while (j1 + 1 < nv && rowOk(j1 + 1)) j1++;
      for (let jj = j; jj <= j1; jj++) for (let x = i; x <= i1; x++) used[jj][x] = true;
      const a = [R.u0 + i * cu, R.v0 + j * cv], z = [R.u0 + (i1 + 1) * cu, R.v0 + (j1 + 1) * cv], h = b.h;
      let lo, hi;
      if (plane === 'x') { lo = [at - h, a[1], a[0]]; hi = [at + h, z[1], z[0]]; }
      else if (plane === 'z') { lo = [a[0], a[1], at - h]; hi = [z[0], z[1], at + h]; }
      else { lo = [a[0], at - h, a[1]]; hi = [z[0], at + h, z[1]]; }
      const drop = plane === 'x' ? ['left', 'right'] : plane === 'z' ? ['front', 'back'] : ['up', 'down'];
      els.push(abox(lo, hi, edge, {rot, drop: cards === 'both' ? drop : drop.filter(f => (cards === '+' ? f === (plane === 'x' ? 'left' : plane === 'z' ? 'back' : 'up') : f !== (plane === 'x' ? 'left' : plane === 'z' ? 'back' : 'up')))}));
    }
  }
  return els;
}
// Horizontal card over an (X, Z) rect with a sub-rect uvr of the sprite: u along +X, v along +Z.
function cardYuv(sprite, y, R, uvr, rot, tint = false) {
  const fn = ([X, , Z]) => [16 * (uvr[0] + (uvr[2] - uvr[0]) * (X - R.u0) / (R.u1 - R.u0)), 16 * (uvr[1] + (uvr[3] - uvr[1]) * (Z - R.v0) / (R.v1 - R.v0))];
  const el = faceEl([[R.u0, y, R.v0], [R.u1, y, R.v1]], {up: {tex: sprite, fn}, down: {tex: sprite, fn}}, {shade: false, rot});
  if (tint) for (const f of Object.values(el.faces)) f.tintindex = 0;
  return el;
}

// ---- crossed cards --------------------------------------------------------------------------------------------------------
// Cards through the point c: a cardZ and a cardX (and with three: one more cardZ turned 45 degrees), each showing the
// whole sprite over a w x h rect centred on c horizontally, from c[1] + y0 to c[1] + y0 + h.
export function crossCards(sprite, c, w, h, {y0 = -h / 2, three = false, flip = false, uvr = [0, 0, 1, 1]} = {}) {
  const [x, y, z] = c, Y0 = y + y0, Y1 = y + y0 + h;
  const out = [cardZ(sprite, z, {X0: x - w / 2, X1: x + w / 2, Y0, Y1}, {uvr, flipU: flip}),
    cardX(sprite, x, {Z0: z - w / 2, Z1: z + w / 2, Y0, Y1}, {uvr, flipU: !flip})];
  if (three) out.push(cardZ(sprite, z, {X0: x - w / 2, X1: x + w / 2, Y0, Y1}, {uvr, flipU: !flip, rot: ['y', 45, c]}));
  return out;
}

// ---- boxes ------------------------------------------------------------------------------------------------------------------
// Box with world-scaled tile windows per face (tex: tile name or {all, up, down, ...}).
export function rockBox(a, b, tex, {rot, seed = 0, drop = []} = {}) {
  const lo = a.map((v, i) => Math.min(v, b[i])), hi = a.map((v, i) => Math.max(v, b[i])), d = sub(hi, lo);
  const spec = typeof tex === 'string' ? {all: tex} : tex, uv = {};
  const dims = {front: [d[0], d[1]], back: [d[0], d[1]], left: [d[2], d[1]], right: [d[2], d[1]], up: [d[0], d[2]], down: [d[0], d[2]]};
  let s = seed;
  for (const f of Object.keys(dims)) uv[f] = tileUV(spec[f] || spec.all, ...dims[f], (s += 7.31));
  return abox(lo, hi, {...spec, uv}, {rot, drop});
}

// Points of a quadratic Bezier (for curved horns, tails of plates): n + 1 points.
export const bez = (p0, p1, p2, n = 16) => Array.from({length: n + 1}, (_, i) => { const t = i / n; return [0, 1].map(k => (1 - t) ** 2 * p0[k] + 2 * (1 - t) * t * p1[k] + t * t * p2[k]); });
// Signed distance helpers in 2D (u, v), blocks.
export const sdCircle = (cx, cy, r) => (u, v) => Math.hypot(u - cx, v - cy) - r;
export function sdPoly(P) {
  return (x, y) => {
    let d = Infinity, inside = false;
    for (let i = 0, j = P.length - 1; i < P.length; j = i++) {
      const [ax, ay] = P[j], [bx, by] = P[i], dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy || 1e-12;
      const t = Math.max(0, Math.min(1, ((x - ax) * dx + (y - ay) * dy) / l2));
      d = Math.min(d, Math.hypot(x - ax - t * dx, y - ay - t * dy));
      if ((ay > y) !== (by > y) && x < (bx - ax) * (y - ay) / (by - ay) + ax) inside = !inside;
    }
    return inside ? -d : d;
  };
}
// Tapered stroke along a polyline: half width w(t), t = 0..1 arc fraction; returns {sd, near(u, v) -> {t, s, d}}.
export function stroke(pts, w) {
  const seg = [];
  let L = 0;
  for (let i = 0; i < pts.length - 1; i++) { const [ax, ay] = pts[i], [bx, by] = pts[i + 1], l = Math.hypot(bx - ax, by - ay) || 1e-9; seg.push({ax, ay, dx: (bx - ax) / l, dy: (by - ay) / l, l, l0: L}); L += l; }
  const near = (x, y) => {
    let best = null;
    for (const g of seg) {
      const qx = x - g.ax, qy = y - g.ay, a = Math.max(0, Math.min(g.l, qx * g.dx + qy * g.dy)), ex = qx - a * g.dx, ey = qy - a * g.dy, d2 = ex * ex + ey * ey;
      if (!best || d2 < best.d2) best = {d2, t: (g.l0 + a) / L, s: g.dx * qy - g.dy * qx};
    }
    return {t: best.t, s: best.s, d: Math.sqrt(best.d2)};
  };
  return {L, near, sd: (x, y) => { const n = near(x, y); return n.d - w(n.t); }};
}
export const sdUnion = (...f) => (x, y) => Math.min(...f.map(g => g(x, y)));
export const sdSub = (a, b) => (x, y) => Math.max(a(x, y), -b(x, y));
