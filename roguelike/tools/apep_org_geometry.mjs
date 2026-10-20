// Models of the Apep phase-2 objects (plan §5, AP-ORG): the six organisms, the Heart of the Oasis, the 소생의 찬가 domes,
// the 둥지 wall blades, the 생명의 손 stalks and the death seed. Used by build_mboss_apep_org.mjs.
//
// Structure (ORG): owners (kinds = organisms riding their aux husk as passengers; objects = fixed or multi displays at
// a marker / spot) -> displays. A display has a joint (its model origin = its pivot) in its parent's frame (root
// displays: the object frame, origin on the floor under the object, +X = its left, +Y up, -Z its facing), a display
// scale (reach = 1.5 x scale blocks round the joint, checkBounds), looks (item ids) and a brightness. Models are authored
// in blocks with the shared shape helpers (mboss_shape_lib.mjs, mboss_model_lib.mjs): root displays with frame 'object'
// are authored in the object frame and shifted by their joint here; frame 'joint' models are authored round the joint.
// Element rotations stay single-axis on the 22.5 degree grid.
import {abox, cardZ, cardX, cardY, faceEl, faceOfDir, lathe, annulus, checkBounds, r4, rotA} from './mboss_model_lib.mjs';
import {loft, slab, crossCards, toUnits, mirrorX, retex, rockBox} from './mboss_shape_lib.mjs';
import {SH, HOOD as NHOOD, NURT, nurtW, PROF, LFR, swatchUV, facetFrac, cardUV, smoothNy, litK, addSprite, bellFacetPx, bellR, skirtR, BAG, bagR, smooth01} from './apep_org_paint.mjs';

export {checkBounds};
export const RIDE_Y = 2.0;           // the husk passenger point above its feet (org manifest passenger.ride_y)
const D2R = Math.PI / 180;

// ---- small geometry helpers (blocks, A-frame) --------------------------------------------------------------------------
const shift = (els, [dx, dy, dz]) => els.map(e => {
  const o = {...e, from: [r4(e.from[0] - dx), r4(e.from[1] + dy), r4(e.from[2] + dz)], to: [r4(e.to[0] - dx), r4(e.to[1] + dy), r4(e.to[2] + dz)]};
  if (e.rotation) o.rotation = {...e.rotation, origin: [r4(e.rotation.origin[0] - dx), r4(e.rotation.origin[1] + dy), r4(e.rotation.origin[2] + dz)]};
  return o;
});
const tint = els => els.map(e => ({...e, faces: Object.fromEntries(Object.entries(e.faces).map(([k, f]) => [k, {...f, tintindex: 0}]))}));
// unshaded faces (no game face shading): the painted tones carry the light, so loft ledges blend into the surface
const flat = els => els.map(e => ({...e, shade: false}));
// stations from profile functions: a0..a1 in n steps; r(a) number or [e1+, e2+, e1-, e2-]; c(a) -> [c1, c2]
const prof = (a0, a1, n, r, c = null, box = 0) => Array.from({length: n + 1}, (_, i) => { const a = a0 + (a1 - a0) * i / n; return {a, r: r(a), c: c ? c(a) : [0, 0], box}; });
const stops = (as, rs, cs = null) => as.map((a, i) => ({a, r: rs[i], c: cs ? cs[i] : [0, 0]}));
// a two-sided card in an axis-aligned plane: corner P0 (blocks), edge vectors du (sprite s) and dv (sprite t, t = 0 at
// P0), both axis-aligned; rot = one element rotation [axis, deg, pivot]. Any in-plane sprite orientation (solveUV).
function quad(sprite, P0, du, dv, {rot, uvr = [0, 0, 1, 1], tint: tn = false} = {}) {
  const P1 = P0.map((x, i) => x + du[i] + dv[i]);
  const n = [du[1] * dv[2] - du[2] * dv[1], du[2] * dv[0] - du[0] * dv[2], du[0] * dv[1] - du[1] * dv[0]];
  const L2 = d => d[0] * d[0] + d[1] * d[1] + d[2] * d[2];
  const fn = X => { const r = X.map((x, i) => x - P0[i]); const s = (r[0] * du[0] + r[1] * du[1] + r[2] * du[2]) / L2(du), t = (r[0] * dv[0] + r[1] * dv[1] + r[2] * dv[2]) / L2(dv);
    return [16 * (uvr[0] + (uvr[2] - uvr[0]) * s), 16 * (uvr[1] + (uvr[3] - uvr[1]) * t)]; };
  const ax = n.map(Math.abs).indexOf(Math.max(...n.map(Math.abs))), dir = [0, 0, 0];
  dir[ax] = 1; const f1 = faceOfDir(dir); dir[ax] = -1; const f2 = faceOfDir(dir);
  const el = faceEl([P0, P1], {[f1]: {tex: sprite, fn}, [f2]: {tex: sprite, fn}}, {shade: false, rot});
  if (tn) for (const f of Object.values(el.faces)) f.tintindex = 0;
  return el;
}
// azimuth th (deg, 0 = forward -Z, 90 = left +X, the 22.5 grid) -> [base quadrant, residual y rotation]
const baseAz = th => { const b = Math.round(th / 90) * 90, g = b - th; if (![-45, -22.5, 0, 22.5, 45].includes(g)) throw new Error('azimuth ' + th); return [((b % 360) + 360) % 360, g]; };
const unitAz = b => [Math.round(Math.sin(b * D2R)), 0, -Math.round(Math.cos(b * D2R))];
const tanAz = b => [-Math.round(Math.cos(b * D2R)), 0, -Math.round(Math.sin(b * D2R))];   // the tangent 90 degrees clockwise from above
// a card in the radial plane at azimuth th: sprite s along the radius (rho0 -> rho1), t down from y1 to y0
function radialCard(sprite, th, rho0, rho1, y0, y1, opt = {}) {
  const [b, g] = baseAz(th), d = unitAz(b);
  return quad(sprite, [d[0] * rho0, y1, d[2] * rho0], [d[0] * (rho1 - rho0), 0, d[2] * (rho1 - rho0)], [0, y0 - y1, 0], {...opt, rot: g ? ['y', g, [0, 0, 0]] : opt.rot});
}
// a card tangent to the circle rho at azimuth th, facing outward: s across (w wide), t from the top yTop down by h;
// tilt (cardinal azimuths only, deg) leans its far end outward about the pivot edge (top, unless pivot 'bottom')
function tangentCard(sprite, th, rho, yTop, w, h, {tilt = 0, pivot = 'top', uvr, tint: tn} = {}) {
  const [b, g] = baseAz(th), d = unitAz(b), tg = tanAz(b);
  const P0 = [d[0] * rho - tg[0] * w / 2, yTop, d[2] * rho - tg[2] * w / 2];
  let rot = g ? ['y', g, [0, 0, 0]] : undefined;
  if (tilt) {
    if (g) throw new Error('tilted tangent cards only at cardinal azimuths');
    const axis = Math.abs(d[2]) > .5 ? 'x' : 'z', py = pivot === 'top' ? yTop : yTop - h;
    // outward lean of the far end: for the top pivot the bottom swings out, for the bottom pivot the top does
    const sgnOut = (axis === 'x' ? (d[2] < 0 ? 1 : -1) : (d[0] > 0 ? 1 : -1)) * (pivot === 'top' ? 1 : -1);
    rot = [axis, sgnOut * tilt, [d[0] * rho, py, d[2] * rho]];
  }
  return quad(sprite, P0, [tg[0] * w, 0, tg[2] * w], [0, -h, 0], {rot, uvr, tint: tn});
}
// a slab from a shared shape (SH): plane 'x' (u = Z, v = Y), 'z' (u = X, v = Y), 'y' (u = X, v = Z) at `at`
const shapeSlab = (name, sprite, plane, at, opt = {}) => slab({plane, at, rect: SH[name].rect, sd: SH[name].sd, sprite, edge: opt.edge || sprite, ...opt});
// mirror images in Z (z -> -z about the joint): faces north / south swap, textures flip, rotations about x and y negate
function mirrorZ(els) {
  return els.map(e => {
    const faces = {};
    for (const [f, face] of Object.entries(e.faces)) {
      const uv = face.uv.slice(), rot = face.rotation || 0;
      if (f === 'north' || f === 'south') { if (rot === 0 || rot === 180) [uv[0], uv[2]] = [uv[2], uv[0]]; else [uv[1], uv[3]] = [uv[3], uv[1]]; }
      else if (f === 'up' || f === 'down') { if (rot === 0 || rot === 180) [uv[1], uv[3]] = [uv[3], uv[1]]; else [uv[0], uv[2]] = [uv[2], uv[0]]; }
      else { if (rot === 0 || rot === 180) [uv[0], uv[2]] = [uv[2], uv[0]]; else [uv[1], uv[3]] = [uv[3], uv[1]]; }
      faces[f === 'north' ? 'south' : f === 'south' ? 'north' : f] = {...face, uv};
    }
    const out = {...e, from: [e.from[0], e.from[1], r4(16 - e.to[2])], to: [e.to[0], e.to[1], r4(16 - e.from[2])], faces};
    if (e.rotation) out.rotation = {...e.rotation, origin: [e.rotation.origin[0], e.rotation.origin[1], r4(16 - e.rotation.origin[2])], angle: e.rotation.axis === 'z' ? e.rotation.angle : -e.rotation.angle};
    return out;
  });
}
// a slab of a shared shape standing in the radial plane at azimuth th (shape u = the distance from the axis, v = height):
// quadrants 90 / 180 are built directly (u = +X / +Z), 270 and 0 as mirror images of 90 and 180
function radialSlab(name, sprite, th, opt = {}) {
  th = ((th % 360) + 360) % 360;
  const [b] = baseAz(th);
  if (b === 270) return mirrorX(radialSlab(name, sprite, 360 - th, opt));
  if (b === 0) return mirrorZ(radialSlab(name, sprite, (540 - th) % 360, opt));
  const [, g] = baseAz(th);
  return shapeSlab(name, sprite, b === 90 ? 'z' : 'x', 0, {...opt, rot: g ? ['y', g, [0, 0, 0]] : null});
}
// a 3-box rounded orb (glow balls): reads round at the sizes used here
const orb = (c, r, tex) => [abox([c[0] - r, c[1] - r * .62, c[2] - r * .62], [c[0] + r, c[1] + r * .62, c[2] + r * .62], tex),
  abox([c[0] - r * .62, c[1] - r, c[2] - r * .62], [c[0] + r * .62, c[1] + r, c[2] + r * .62], tex), abox([c[0] - r * .62, c[1] - r * .62, c[2] - r], [c[0] + r * .62, c[1] + r * .62, c[2] + r], tex)];
// a two-sided ring band (lathe outward + inward) round the y axis
const band = (c, r, y0, y1, tex, n = 16) => [...lathe('y', c, [{a: [y0, y1], r, tex}], {vFrom: y1, vTo: y0, n}), ...lathe('y', c, [{a: [y0, y1], r: r - .004, tex}], {vFrom: y1, vTo: y0, n, inward: true})];
// a cone spike as two crossed triangle cards along an axis-aligned direction dir from base point P (length L, width w);
// rot = an extra single-axis rotation about P (diagonal spikes)
function spike(sprite, P, dir, L, w, rot) {
  const a = dir.map(Math.abs).indexOf(1), o1 = [0, 0, 0], o2 = [0, 0, 0];
  const others = [0, 1, 2].filter(i => i !== a); o1[others[0]] = 1; o2[others[1]] = 1;
  const tip = dir.map(x => x * L), r = rot ? [rot[0], rot[1], P] : undefined;
  const mk = o => quad(sprite, P.map((x, i) => x + tip[i] - o[i] * w / 2), o.map(x => x * w), tip.map(x => -x), {rot: r});
  return [mk(o1), mk(o2)];
}

// a vertical two-sided panel centred at c, w wide along the azimuth phi (deg: 0 = across X, facing -Z; the 22.5 grid),
// h tall; sprite rows v0..v1 top to bottom (twisted ribbons: one panel per segment, phi stepping round)
function vpanel(sprite, c, w, h, phi, v0 = 0, v1 = 1, tn = false) {
  phi = Math.round(phi / 22.5) * 22.5; phi = ((phi % 180) + 270) % 180 - 90;    // the grid, -90 .. 90
  const base = Math.abs(phi) <= 45 ? 0 : 90, g = base ? (phi > 0 ? phi - 90 : phi + 90) : phi;
  const P0 = base ? [c[0], c[1] + h / 2, c[2] - w / 2] : [c[0] - w / 2, c[1] + h / 2, c[2]], du = base ? [0, 0, w] : [w, 0, 0];
  return quad(sprite, P0, du, [0, -h, 0], {rot: g ? ['y', g, c] : undefined, uvr: [0, v0, 1, v1], tint: tn});
}
// a two-sided strip from A to B (points in the Y-Z plane at x = c0, [y, z]), W wide across X: the strip direction is
// snapped to the 22.5 degree grid (one rotation about X round its middle); sprite rows v0 (at A) .. v1 (at B)
function stripYZ(sprite, A, B, W, v0, v1, {x = 0, ext = .02} = {}) {
  const dy = B[0] - A[0], dz = B[1] - A[1], L = Math.hypot(dy, dz) + 2 * ext, t = [0, dy / Math.hypot(dy, dz), dz / Math.hypot(dy, dz)];
  let best = null;
  for (const d of [[0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]) for (const g of [0, 22.5, -22.5, 45, -45]) {
    const r = rotA('x', g, d), e = Math.hypot(r[1] - t[1], r[2] - t[2]);
    if (!best || e < best.e - 1e-9 || (Math.abs(e - best.e) < 1e-9 && Math.abs(g) < Math.abs(best.g))) best = {d, g, e};
  }
  const m = [x, (A[0] + B[0]) / 2, (A[1] + B[1]) / 2], dv = best.d.map(v => v * L);
  const P0 = [m[0] - W / 2, m[1] - dv[1] / 2, m[2] - dv[2] / 2];
  return quad(sprite, P0, [W, 0, 0], dv, {rot: best.g ? ['x', best.g, m] : undefined, uvr: [0, v0, 1, v1]});
}
// a polyline of strips (pts [y, z]), the sprite running along its whole length
function stripChain(sprite, pts, W, opt = {}) {
  const seg = pts.slice(1).map((p, i) => Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1])), tot = seg.reduce((a, b) => a + b, 0);
  let acc = 0;
  return seg.map((l, i) => { const e = stripYZ(sprite, pts[i], pts[i + 1], W, acc / tot, (acc + l) / tot, opt); acc += l; return e; });
}

// a knobbly root: square boxes along a polyline P (3D points) lying in a plane x = const ('yz', boxes turned about X) or
// z = const ('xy', turned about Z); each box follows its segment's direction snapped to the 22.5 degree grid, overlapping
// its neighbours; r(t) the half thickness (t 0..1 along the root); a knuckle box every `knot` joints; bark tile sprite
function tube(P0, plane, r, tex, {knot = 3, seed = 0, sub = 2} = {}) {
  const P = [];
  for (let i = 0; i < P0.length - 1; i++) for (let j = 0; j < sub; j++) {
    const t = j / sub, a = P0[Math.max(0, i - 1)], b = P0[i], c = P0[i + 1], d = P0[Math.min(P0.length - 1, i + 2)];
    P.push(b.map((_, k) => .5 * (2 * b[k] + (-a[k] + c[k]) * t + (2 * a[k] - 5 * b[k] + 4 * c[k] - d[k]) * t * t + (-a[k] + 3 * b[k] - 3 * c[k] + d[k]) * t * t * t)));
  }
  P.push(P0[P0.length - 1]);
  const ax = plane === 'xy' ? 'z' : 'x', [i1, i2] = plane === 'xy' ? [0, 1] : [1, 2], els = [];
  const dirs = [0, 1].map(k => { const d = [0, 0, 0]; d[k ? i2 : i1] = 1; return d; });
  for (let i = 0; i < P.length - 1; i++) {
    const A = P[i], B = P[i + 1], L = Math.hypot(B[i1] - A[i1], B[i2] - A[i2]), t = [0, 0, 0];
    t[i1] = (B[i1] - A[i1]) / L; t[i2] = (B[i2] - A[i2]) / L;
    let best = null;
    for (const d of dirs) for (const g of [0, 22.5, -22.5, 45, -45]) {
      const q = rotA(ax, g, d), e = Math.min(Math.hypot(q[0] - t[0], q[1] - t[1], q[2] - t[2]), Math.hypot(q[0] + t[0], q[1] + t[1], q[2] + t[2]));
      if (!best || e < best.e - 1e-9) best = {d, g, e};
    }
    const rr = r((i + .5) / (P.length - 1)), M = A.map((v, k) => (v + B[k]) / 2), h = L / 2 + rr * .55;
    const half = [0, 1, 2].map(k => (best.d[k] ? h : rr));
    els.push(rockBox(M.map((v, k) => v - half[k]), M.map((v, k) => v + half[k]), tex, {rot: best.g ? [ax, best.g, M] : undefined, seed: seed + i * 3.7}));
    if (knot && i > 0 && i % knot === 0) { const k = r(i / (P.length - 1)) * 1.18; els.push(rockBox(A.map(v => v - k), A.map(v => v + k), tex, {rot: ['y', 45, A], seed: seed + i * 5.3})); }
  }
  return els;
}
// points of a root in a plane: 2D [u, v] -> 3D (xy: [u, v, c]; yz: [c, u, v]... u along the plane's first axis)
const inPlane = (plane, c, pts) => pts.map(([a, b]) => (plane === 'xy' ? [a, b, c] : [c, a, b]));

// a lit loft (apep_org_paint.mjs PROF): the stations of the profile, the facets on its wrap (u squeezed into the facet
// part of the sprite), every ledge and cap retextured to the swatch of its light factor litK(smooth normal, face
// normal) at its axial band: the steps shade like one smooth surface
const LEDGE_FACES = {y: ['up', 'down'], z: ['north', 'south'], x: ['east', 'west']};
const FACE_NY = {up: 1, down: -1};
function litLoft(name, {caps = '', seed = 0, skip, tint: tn = false, stations} = {}) {
  const p = PROF[name], F = LFR[p.axis], fw = facetFrac(name), g = p.g ?? .8;
  // inscribed: the section polygons' vertices on the profile (the facets inside it), so the silhouette cards cover
  // the stair notches and nothing pokes out past the smooth outline
  const ins = p.inscribe ? Math.cos(Math.PI / p.n) : 1;
  const st = (stations || p.as).map(a => { const s = p.sec(a), r = Array.isArray(s.r) ? s.r.map(x => x * ins) : s.r * ins; return {a, ...s, r}; });
  const els = loft(p.axis, st, {n: p.n, tex: name, ledgeTex: name, caps, seed, skip, tint: tn});
  for (const e of els) {
    const [fname, face] = Object.entries(e.faces)[0];
    if (!LEDGE_FACES[p.axis].includes(fname)) { face.uv = [face.uv[0] * fw, face.uv[1], face.uv[2] * fw, face.uv[3]].map(r4); continue; }
    const m = [0, 1, 2].map(i => (e.from[i] + e.to[i]) / 2), c = [8 - m[0], m[1] - 8, m[2] - 8];
    let P = c;
    if (e.rotation) { const o = e.rotation.origin, O = [8 - o[0], o[1] - 8, o[2] - 8], deg = e.rotation.axis === 'x' ? e.rotation.angle : -e.rotation.angle;
      P = rotA(e.rotation.axis, deg, c.map((x, i) => x - O[i])).map((x, i) => x + O[i]); }
    const dot = v => P[0] * v[0] + P[1] * v[1] + P[2] * v[2], a = dot(F.A), cc = p.sec(a).c || [0, 0];
    const th = Math.atan2(dot(F.e2) - cc[1], dot(F.e1) - cc[0]) / D2R;
    face.uv = swatchUV(name, litK(smoothNy(p, th, a), FACE_NY[fname] || 0, g), a);
  }
  return els;
}

// ================================================================================================================
// facet bodies: convex polyhedra whose face normals sit on the rotation grid (azimuths 90 k in a display's frame,
// elevations 22.5 j), one face per normal, tangent to a smooth convex body (its support function h(n)). Every face is a
// two-sided card cut to its polygon by an alpha mask and lit by the game per its own normal: a low-poly solid with flat
// facets and no stair steps. The diagonal azimuths (45 + 90 k) live on a second display turned 45 degrees about Y
// (its faces are cardinal in its own frame): `half` 0 = the cardinal faces (+ top / bottom), 1 = the diagonal ones.
// ================================================================================================================
const V3 = {add: (a, b) => a.map((x, i) => x + b[i]), sub: (a, b) => a.map((x, i) => x - b[i]), sc: (a, k) => a.map(x => x * k),
  dot: (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2], cross: (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]],
  norm: a => { const l = Math.hypot(...a); return a.map(x => x / l); }};
export const nAzEl = (az, el) => [Math.sin(az * D2R) * Math.cos(el * D2R), Math.sin(el * D2R), -Math.cos(az * D2R) * Math.cos(el * D2R)].map(x => (Math.abs(x) < 1e-12 ? 0 : x));
function solve3(A, b) {
  const det = M => M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0]) + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]);
  const Dt = det(A); if (Math.abs(Dt) < 1e-10) return null;
  return [0, 1, 2].map(c => det(A.map((row, r) => row.map((x, j) => (j === c ? b[r] : x)))) / Dt);
}
// planes [{n, h, ...}] -> faces [{...plane, poly: ordered 3D vertices}]
function polyFaces(planes) {
  const V = [];
  for (let i = 0; i < planes.length; i++) for (let j = i + 1; j < planes.length; j++) for (let k = j + 1; k < planes.length; k++) {
    const x = solve3([planes[i].n, planes[j].n, planes[k].n], [planes[i].h, planes[j].h, planes[k].h]);
    if (x && planes.every(p => V3.dot(p.n, x) <= p.h + 1e-7) && !V.some(y => Math.hypot(...V3.sub(x, y)) < 1e-7)) V.push(x);
  }
  return planes.map(p => {
    const U = V.filter(x => Math.abs(V3.dot(p.n, x) - p.h) < 1e-6);
    if (U.length < 3) return null;
    const c = V3.sc(U.reduce((a, b) => V3.add(a, b)), 1 / U.length);
    const e1 = V3.norm(Math.abs(p.n[1]) > .99 ? [1, 0, 0] : V3.cross([0, 1, 0], p.n)), e2 = V3.cross(p.n, e1);
    U.sort((a, b) => Math.atan2(V3.dot(V3.sub(a, c), e2), V3.dot(V3.sub(a, c), e1)) - Math.atan2(V3.dot(V3.sub(b, c), e2), V3.dot(V3.sub(b, c), e1)));
    return {...p, poly: U, c};
  }).filter(Boolean);
}
// the planes of a facet body round its axis ('y' upright, 'z' lying along z): support h(n), azimuths round the axis
// (deg, the 45 grid; for 'y' 0 = -Z, 90 = +X; for 'z' 0 = +X, 90 = +Y), elevations toward the axis' + end (deg, the 22.5
// grid, +-90 = the end caps), extra planes. Each plane keeps {az, el}.
const AXROT = {y: v => v, z: v => [v[0], -v[2], v[1]]};          // 'z': the 'y' frame turned so +Y -> +Z, -Z -> +Y
export function facetPlanes(h, {axis = 'y', az = [0, 45, 90, 135, 180, 225, 270, 315], el = [0, 22.5, 45, 67.5, 90], extra = []} = {}) {
  const P = [];
  for (const e of el) for (const a of (Math.abs(e) === 90 ? [0] : az)) {
    const n = (axis === 'y' ? nAzEl(a, e) : AXROT.z(nAzEl(a - 90, e))).map(x => (Math.abs(x) < 1e-12 ? 0 : x));
    P.push({n, h: h(n), az: a, el: e, axis});
  }
  return [...P, ...extra];
}
const AXES = {x: [1, 0, 0], y: [0, 1, 0], z: [0, 0, 1]};
const DIRS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]];
// the single grid rotation that turns an axis-aligned direction d into n: {d, axis, g} (g 0 = none)
// (faces up to 45 degrees from the horizontal turn from a horizontal direction, steeper ones from +-Y: masks of
// faces with the same shape then share their card frame)
function gridRot(n) {
  for (const d of DIRS) if (Math.hypot(...V3.sub(d, n)) < 1e-6) return {d, axis: null, g: 0};
  const order = Math.abs(n[1]) < .7072 ? [0, 1, 4, 5, 2, 3] : [2, 3, 0, 1, 4, 5];
  for (const axis of ['x', 'y', 'z']) for (const d of order.map(i => DIRS[i])) { if (Math.abs(V3.dot(d, AXES[axis])) > .5) continue;
    for (const g of [22.5, -22.5, 45, -45]) if (Math.hypot(...V3.sub(rotA(axis, g, d), n)) < 1e-6) return {d, axis, g}; }
  return null;
}
// one face as an element: its card in the axis-aligned plane it is turned from (one grid rotation about the face
// centre), cut to the face rectangle; the mask polygon in the card's (s right, t down as seen from outside). frame =
// the display's turn {axis, deg} (the diagonal half: authored in the frame turned back by it)
function faceCard(f, frame = null, down = [0, -1, 0]) {
  const T = v => (frame ? rotA(frame.axis, -frame.deg, v) : v);
  const n = T(f.n), c = T(f.c), poly = f.poly.map(T);
  const R0 = gridRot(n);
  if (!R0) throw new Error('facet normal off the rotation grid: ' + n.map(x => x.toFixed(3)));
  const {d, axis, g} = R0, un = v => (g ? V3.add(c, rotA(axis, -g, V3.sub(v, c))) : v);
  const P = poly.map(un);
  // card axes in the unturned plane: right as seen from outside, t down (for up / down cards: toward +-Z)
  // (t runs down the body: the body axis' down direction projected into the face, unturned; R = t x n: every face of
  // a ring of a body of revolution then shows the same mask; the end caps keep a fixed frame)
  let R, Td;
  const dn = T(down), tp = V3.sub(dn, V3.sc(n, V3.dot(n, dn)));
  if (Math.hypot(...tp) > 1e-6) { const t0 = (g ? rotA(axis, -g, tp) : tp).map(x => Math.round(x / Math.hypot(...tp))); Td = t0; R = V3.cross(t0, d); }
  else if (d[1] === 0) { R = V3.cross(V3.sc(d, -1), [0, 1, 0]); Td = [0, -1, 0]; }
  else { R = [1, 0, 0]; Td = d[1] > 0 ? [0, 0, 1] : [0, 0, -1]; }
  if (Math.abs(Math.abs(Td[0]) + Math.abs(Td[1]) + Math.abs(Td[2]) - 1) > 1e-9 || Math.abs(V3.dot(Td, d)) > 1e-9) throw new Error('facet card frame off axis: ' + Td);
  const ss = P.map(v => V3.dot(v, R)), ts = P.map(v => V3.dot(v, Td));
  const s0 = Math.min(...ss), s1 = Math.max(...ss), t0 = Math.min(...ts), t1 = Math.max(...ts);
  const P0 = V3.add(V3.add(V3.sc(R, s0), V3.sc(Td, t0)), V3.sc(d, V3.dot(P[0], d)));
  return {P0, du: V3.sc(R, s1 - s0), dv: V3.sc(Td, t1 - t0), rot: g ? [axis, g, c] : undefined, w: s1 - s0, h: t1 - t0,
    mask: ss.map((x, i) => [(x - s0) / (s1 - s0), (ts[i] - t0) / (t1 - t0)]), el: f.el, n: f.n};
}
// a facet body's elements, split over the two display halves (0: the cardinal azimuths + the end caps, 1: the
// diagonal ones, authored in the frame of the display turned 45 degrees about the body axis), and its mask sprite:
// faces sharing a mask (the same polygon and paint class, mirrored masks reuse it flipped) share a cell.
// paint({el, n, cls}, s, t, d = blocks to the polygon edge) -> rgba; flat(face) = an 8 px mask (one-colour faces)
const isCardinal = f => Math.abs(f.el) > 89.9 || Math.abs(((f.az % 90) + 90) % 90) < 1e-6;
export function facetBody(name, faces, {owner, ppb = 64, paint, cls = () => 0, tint: tn = false, down = null, flat = null} = {}) {
  const dnOf = f => down || ((f.axis || 'y') === 'z' ? [0, 0, -1] : [0, -1, 0]);
  const cards = faces.map(f => ({f, half: isCardinal(f) ? 0 : 1, card: faceCard(f, isCardinal(f) ? null : {axis: f.axis || 'y', deg: 45}, dnOf(f))}));
  const keyOf = (Q, f) => cls(f) + '|' + Q.map(([a, b]) => a.toFixed(3) + ',' + b.toFixed(3)).join(';');
  const canon = Q => { const k = Q.map(([a, b]) => [Math.round(a * 1000), Math.round(b * 1000)]); const i0 = k.reduce((m, p, i) => (p[0] < k[m][0] || (p[0] === k[m][0] && p[1] < k[m][1]) ? i : m), 0);
    const r = [...k.slice(i0), ...k.slice(0, i0)]; const r2 = [r[0], ...r.slice(1).reverse()]; return JSON.stringify(r) < JSON.stringify(r2) ? JSON.stringify(r) : JSON.stringify(r2); };
  const masks = [], index = new Map();
  for (const c of cards) {
    const k = cls(c.f) + '|' + canon(c.card.mask), km = cls(c.f) + '|' + canon(c.card.mask.map(([a, b]) => [1 - a, b]));
    if (index.has(k)) { c.mi = index.get(k); c.flip = false; }
    else if (index.has(km)) { c.mi = index.get(km); c.flip = true; }
    else { index.set(k, masks.length); c.mi = masks.length; c.flip = false; masks.push({card: c.card, f: c.f, cls: cls(c.f)}); }
  }

  // pack the masks (shelves; each mask at `ppb` px per block, at least 8 px a side) into one sprite (sides multiples of 16)
  for (const m of masks) { const k = flat && flat(m.f) ? 8 / Math.max(m.card.w, m.card.h) : ppb; m.pw = Math.max(8, Math.min(64, Math.round(m.card.w * k))); m.ph = Math.max(8, Math.min(64, Math.round(m.card.h * k))); }
  const order = masks.map((m, i) => i).sort((i, j) => masks[j].ph - masks[i].ph || i - j);
  // the sprite width (a multiple of 16) giving the smallest sprite
  const pack = SWc => { let x = 0, y = 0, shelf = 0; const at = []; for (const i of order) { const m = masks[i]; if (x + m.pw > SWc) { x = 0; y += shelf; shelf = 0; } at[i] = [x, y]; x += m.pw; shelf = Math.max(shelf, m.ph); } return {at, H: Math.max(16, Math.ceil((y + shelf) / 16) * 16)}; };
  let best = null;
  for (let SWc = Math.ceil(Math.max(...masks.map(m => m.pw)) / 16) * 16; SWc <= 256; SWc += 16) { const r = pack(SWc); if (!best || SWc * r.H < best.SW * best.H) best = {SW: SWc, ...r}; }
  const SW = best.SW, SH_ = best.H;
  masks.forEach((m, i) => { [m.px0, m.py0] = best.at[i]; });
  if (process.env.FB_DEBUG) console.log(name, SW, SH_, masks.map(m => `${m.cls}:${m.f.el}:${m.pw}x${m.ph}`).join(' '));
  const grid = new Int32Array(SW * SH_).fill(-1);
  masks.forEach((m, i) => { for (let yy = m.py0; yy < m.py0 + m.ph; yy++) for (let xx = m.px0; xx < m.px0 + m.pw; xx++) grid[yy * SW + xx] = i; });
  addSprite(name, SW, SH_, (S0, T0) => {
    const X = Math.min(SW - 1, Math.floor(S0 * SW)), Y = Math.min(SH_ - 1, Math.floor(T0 * SH_)), mi = grid[Y * SW + X];
    if (mi < 0) return [0, 0, 0, 0];
    const m = masks[mi], s = (S0 * SW - m.px0) / m.pw, t = (T0 * SH_ - m.py0) / m.ph, {card} = m, Q = card.mask;
    let dmin = Infinity, pos = true, neg = true;
    for (let i = 0; i < Q.length; i++) {
      const a = Q[i], b = Q[(i + 1) % Q.length], ax = a[0] * card.w, ay = a[1] * card.h, bx = b[0] * card.w, by = b[1] * card.h, px = s * card.w, py = t * card.h;
      const ex = bx - ax, ey = by - ay, L = Math.hypot(ex, ey) || 1, cr = ex * (py - ay) - ey * (px - ax);
      const u = Math.max(0, Math.min(1, ((px - ax) * ex + (py - ay) * ey) / (L * L)));
      dmin = Math.min(dmin, Math.hypot(px - ax - u * ex, py - ay - u * ey)); if (cr < 0) pos = false; if (cr > 0) neg = false;
    }
    const sd = (pos || neg) ? -dmin : dmin, px = Math.max(card.w / m.pw, card.h / m.ph);
    if (sd > px * .6) return [0, 0, 0, 0];
    return paint({el: m.card.el, n: m.f.n, cls: m.cls, w: card.w, h: card.h}, s, t, Math.max(0, -sd));
  }, owner);
  const els = [[], []];
  for (const c of cards) {
    const m = masks[c.mi], u0 = m.px0 / SW, u1 = (m.px0 + m.pw) / SW, v0 = m.py0 / SH_, v1 = (m.py0 + m.ph) / SH_;
    els[c.half].push(quad(name, c.card.P0, c.card.du, c.card.dv, {rot: c.card.rot, uvr: [c.flip ? u1 : u0, v0, c.flip ? u0 : u1, v1], tint: tn}));
  }
  return els;
}
// the support function of a body of revolution about 'y' (radius rf(a), a in [a0, a1]) or 'z' (centre height yc)
export const revSupport = (rf, a0, a1, axis = 'y', yc = 0) => n => {
  const A = axis === 'y' ? n[1] : n[2], hz = axis === 'y' ? Math.hypot(n[0], n[2]) : Math.hypot(n[0], n[1]);
  let m = -Infinity; for (let i = 0; i <= 160; i++) { const a = a0 + (a1 - a0) * i / 160; m = Math.max(m, rf(a) * hz + a * A); }
  return m + (axis === 'z' ? yc * n[1] : 0);
};

// ================================================================================================================
// 기본 basic: bell (melee, walks) / bag (ranged, lying), a petal crown at the bag neck, the 수호 shield overlay
// ================================================================================================================
// silhouette cards of an inscribed 8-facet lit 'y' loft (PROF card): two-sided cards through the axis along the four
// vertex lines (22.5 + 45k degrees, on the rotation grid), each the smooth profile (two mirrored halves of the card
// region). The vertices lie on the profile, so a card never pokes through a facet; seen face-on the cards fill the
// stair notches of the stepped outline, so the silhouette reads smooth from any side
function silCards(name, {tint: tn = false} = {}) {
  const p = PROF[name], a0 = Math.min(...p.as), a1 = Math.max(...p.as), R = p.card.R, uv = cardUV(name), els = [];
  if (p.n !== 8 || !p.inscribe) throw new Error('silCards: inscribed 8-facet lofts only');
  for (let k = 0; k < 4; k++) {
    const psi = 22.5 + k * 45, base = Math.round(psi / 90) * 90, g = psi - base;
    const d = base % 180 === 0 ? [1, 0, 0] : [0, 0, 1];
    for (const sg of [1, -1]) {
      const e = quad(name, [0, a1, 0], d.map(x => x * sg * R), [0, a0 - a1, 0], {rot: g ? ['y', g, [0, 0, 0]] : undefined, uvr: [uv[0] / 16, 0, 1, 1], tint: tn});
      els.push(e);
    }
  }
  return els;
}
// bell (1.15 b, 1.35 with the stem; v4 f186 / f2310 / v3 f900): a facet body round the smooth bell (bellR: an egg on its
// narrow end, widest at two thirds of its height, a tall round top): 8 azimuths x elevations -22.5 .. 67.5 + the top,
// the dark underside at y .14; the skirt is two more rings of 8 faces: the hanging lobes (elevation 22.5, y .32 -> .1,
// V notches between them) and their flared tips (elevation 45, y .1 -> 0, each a rounded tongue cut by its mask).
// Faces on the diagonals ride the bulb_x display (the bulb turned 45 degrees).
const BELL_FACES = (() => {
  const body = polyFaces([...facetPlanes(revSupport(bellR, .14, 1.16), {el: [-22.5, 0, 22.5, 45, 67.5, 90]}), {n: [0, -1, 0], h: -.14, az: 0, el: -90}]);
  const ring = (rf, y0, y1, el, cls) => polyFaces([...facetPlanes(revSupport(rf, y0, y1), {el: [el]}), {n: [0, 1, 0], h: y1, az: 0, el: 90, hidden: true}, {n: [0, -1, 0], h: -y0, az: 0, el: -90, hidden: true}])
    .filter(f => !f.hidden).map(f => ({...f, skirt: cls}));
  const skirt = [...ring(skirtR, .1, .32, 22.5, 1), ...ring(skirtR, 0, .1, 45, 4)];
  return facetBody('bo_bellF', [...body, ...skirt], {owner: 'basic', paint: bellFacetPx, cls: f => (f.skirt || (f.el < -80 ? 2 : 0)), tint: true, ppb: 72, flat: f => f.el < -80});
})();
function bellModel() {
  const els = [...BELL_FACES[0]];
  // the curled olive stem: a thin tube rising from the top and hooking back over
  els.push(...tint(tube([[0, 1.1, 0], [0, 1.22, -.01], [0, 1.31, .03], [0, 1.34, .1], [0, 1.3, .16], [0, 1.24, .17]], 'yz', t => .024 - .01 * t, 'bo_stemT', {knot: 0, sub: 2, seed: 5})));
  return els;
}
const bellModelX = () => [...BELL_FACES[1]];
// the bag (v3 f900): a facet body round the pear lying along Z (bagR: the round belly behind, the neck forward, its
// axis level at y BAG.y), 8 azimuths round Z x elevations toward the ends; the clips pitch the bulb 20 degrees so the
// neck lifts (BAG_POSE); the drawstring ring at the neck. Its diagonal faces ride bulb_x rolled 45 degrees about Z.
// (v3 f900: the neck raised about 35 degrees; t lifts the lowest point of the pitched bag to the floor; the crown
// joint sits on the neck tip, its +Y along the neck)
export const BAG_POSE = (() => {
  const r = 35, P = (y, z) => rotA('x', r, [0, y, z]);
  let lo = Infinity; for (let i = 0; i <= 60; i++) { const z = -.62 + 1.2 * i / 60; for (let j = 0; j < 16; j++) lo = Math.min(lo, P(BAG.y + bagR(z) * Math.sin(j * Math.PI / 8), z)[1]); }
  const t = r4(-lo + .01), tip = P(BAG.y, -.64);
  return {r, t, crown: [0, r4(tip[1] + t), r4(tip[2])], crownR: -(90 - r)};
})();
const BAG_FACES = (() => {
  const faces = polyFaces(facetPlanes(revSupport(z => bagR(z) + .01, -.62, .575, 'z', BAG.y), {axis: 'z', el: [-90, -67.5, -45, -22.5, 0, 22.5, 45, 67.5, 90]}));
  return facetBody('bo_bagF', faces, {owner: 'basic', paint: bellFacetPx, cls: () => 3, tint: true, ppb: 84});
})();
function bagModel() {
  const els = [...BAG_FACES[0]];
  els.push(...tint(loft('z', [{a: -.6, r: .1, c: [0, BAG.y]}, {a: -.55, r: .1, c: [0, BAG.y]}], {n: 8, tex: 'bo_stemT', caps: ''})));
  return els;
}
const bagModelX = () => [...BAG_FACES[1]];
// the crown (joint at the bag neck, its +Y along the neck): 4 cardinal petals leaning out, 4 diagonal ones
function crownModel(open) {
  // 4 broad crumpled petals leaning out of the neck (more when open) + 2 small ones between; open adds the lime glow
  const els = [];
  for (let k = 0; k < 4; k++) els.push(open ? tangentCard('bo_petal', k * 90, .05, .3, .3, .32, {tilt: 45, pivot: 'bottom'}) : tangentCard('bo_petal', k * 90, .06, .3, .26, .32));
  for (const th of [45, 135, 225, 315]) els.push(tangentCard('bo_petal', th, .07, .24, .22, .26));
  if (open) els.push(...crossCards('bo_glow', [0, .1, 0], .3, .3, {y0: -.15}));
  return els;
}
// the shield overlay: 3 vesica panes, the bubble rim band, the yellow 3-leaf crown
function shieldModel() {
  const els = [];
  for (const th of [67.5, 180, 292.5]) els.push(tangentCard('bo_pane', th, .64, 1.47, .62, 1.42));
  els.push(...band([0, 0, 0], .8, 0, .42, 'bo_bubble', 8));
  els.push(...crossCards('bo_lcrown', [0, 1.42, 0], .48, .26, {y0: 0}));
  return els;
}

// ================================================================================================================
// 양육 nurturing: S ribbon stalk + fronds + gold shard, the hood cap, the orb, the immune ring overlay
// ================================================================================================================
// the stalk (v3 f1240 / f1300): one broad leaf ribbon rising in a half twist (vertical panels, the azimuth stepping
// 22.5 degrees per panel, each showing its slice of the unrolled ribbon sprite, whose alpha draws the smooth edges),
// leaning back a little and forward again under the hood; a second short sweep at the base, pale fronds splayed on
// the ground, the gold shard high on its left
const nurtC = y => [.05 * Math.sin(Math.PI * y / 1.4), y, .1 * Math.sin(Math.PI * y / 2.4) - .04];
function ribbonPanel(sprite, c, wp, h, phi, v0, v1, W) {
  const e = vpanel(sprite, c, wp, h, phi, v0, v1);
  // narrow the card's u window to its width (the sprite spans W)
  const u0 = .5 - wp / (2 * W), u1 = .5 + wp / (2 * W);
  for (const f of Object.values(e.faces)) { const [a, b2, c2, d] = f.uv, lo = Math.min(a, c2), hi = Math.max(a, c2), m = x => r4(lo + (x - lo) / ((hi - lo) || 1) * (hi - lo) * (u1 - u0) + 16 * u0 * 0 + (x - lo) * 0);
    const map = x => r4(16 * u0 + (x - lo) / ((hi - lo) || 1) * 16 * (u1 - u0)); f.uv = [map(a), b2, map(c2), d]; }
  return e;
}
function nurtStalk() {
  const els = [], N = 9, T = NURT.top;
  for (let i = 0; i < N; i++) {
    const y0 = T * i / N, y1 = T * (i + 1) / N, ym = (y0 + y1) / 2, h = y1 - y0 + .04;
    let wp = 0; for (let k = 0; k <= 8; k++) wp = Math.max(wp, nurtW(y0 + (y1 - y0) * k / 8));
    els.push(ribbonPanel('nu_rib', nurtC(ym), wp + .02, h, -22.5 * i, 1 - y1 / T - .02 / T, 1 - y0 / T + .02 / T, NURT.W));
  }
  // the base sweep: a short ribbon turned 90 degrees, leaning out
  els.push(quad('nu_base', [.05, .62, -.02], [0, 0, .42], [0, -.62, 0], {rot: ['z', -22.5, [.05, 0, .19]]}));
  for (let k = 0; k < 6; k++) {
    const th = [0, 67.5, 112.5, 180, 247.5, 292.5][k], [b, g] = baseAz(th), d = unitAz(b), tg = tanAz(b);
    // a frond lying outward on the ground, tip slightly raised (cardinal ones tilted 22.5 up)
    const L = .62, w = .22, P0 = [d[0] * .1 - tg[0] * w / 2, .03, d[2] * .1 - tg[2] * w / 2];
    let rot = g ? ['y', g, [0, 0, 0]] : null;
    if (!g) { const axis = Math.abs(d[2]) > .5 ? 'x' : 'z'; rot = [axis, axis === 'x' ? (d[2] < 0 ? 22.5 : -22.5) : (d[0] > 0 ? 22.5 : -22.5), [d[0] * .1, .03, d[2] * .1]]; }
    els.push(quad('nu_frond', P0.map((x, i) => x + d[i] * L), [tg[0] * w, 0, tg[2] * w], [-d[0] * L, 0, -d[2] * L], {rot}));
  }
  els.push(...crossCards('nu_gem', [.22, 1.78, .14], .2, .34, {y0: -.17}));
  return els;
}
// the hood: a cream leaf bent over the top like a drooping tulip (strips along an arc in the Y-Z plane, the leaf outline
// in the sprite), its edges curled down (two crescent cheeks); tilt = the hood lifted open toward the targets
function nurtCap(t) {
  const els = stripChain('nu_hoodL', NHOOD[t ? 'tilt' : 'idle'], .64);
  for (const x of [.25, -.25]) els.push(...shapeSlab(t ? 'n_cheekT' : 'n_cheek', t ? 'nu_cheekT' : 'nu_cheek', 'x', x, {half: .015, core: false}));
  return els;
}
const nurtOrb = () => [...orb([0, 0, 0], .15, 'nu_orb'), ...crossCards('nu_orb', [0, 0, 0], .44, .44, {y0: -.22})];
const nurtRing = () => band([0, 0, 0], 1.3, 0, .5, 'nu_ring');

// ================================================================================================================
// 수호 guarding: helix spire (spire / bud / wisp looks, mid pivot) + the hovering orb
// ================================================================================================================
const SHEATH = {y: [0, .2, .42, .62, .8, .95], r: [.38, .36, .33, .28, .21, .13]};
function guardBase() {
  const els = [...loft('y', stops(SHEATH.y, SHEATH.r), {n: 16, tex: 'gu_sheath', ledgeTex: 'gu_sheath_l', caps: '-+', seed: 7})];
  for (let k = 0; k < 8; k++) els.push(radialCard('gu_lobe', k * 45 + 22.5, .14, .62, 0, .34));
  els.push(abox([-.12, .3, -.42], [.12, .58, -.32], 'gu_gem', {rot: ['x', -22.5, [0, .44, -.37]]}));
  return els;
}
// the spire: three pale ribbons in a loose triple helix round the axis (a tangent panel per segment), converging and
// narrowing to points at the top
const HELIX = [{th0: 0, y0: .5, y1: 4.42, n: 40, w: .42}, {th0: 180, y0: .5, y1: 4.1, n: 36, w: .38}];
function guardSpire() {
  const els = guardBase();
  for (const R of HELIX) for (let i = 0; i < R.n; i++) {
    const t = (i + .5) / R.n, y = R.y0 + t * (R.y1 - R.y0), h = (R.y1 - R.y0) / R.n, th = R.th0 + 360 * 1.05 * (y - .5) / 3.9;
    const r = .3 * (1 - .8 * smooth01((y - .5) / 3.9)) + .03, w = R.w * (1 - .5 * t) + .03;
    els.push(vpanel('gu_rib', [r * Math.cos(th * D2R), y, r * Math.sin(th * D2R)], w, h + .025, -(th + 90) + 22.5 * 0, 1 - (i + 1) / R.n, 1 - i / R.n));
  }
  return els;
}
function guardBud() {
  // the teal pointed hood over a pale drape flaring to a wavy hem (a wrap loft), the hem lobes and the gold gem in front
  const els = [...loft('y', stops([.95, 1.2, 1.45, 1.65, 1.82, 1.95, 2.04], [.44, .41, .35, .27, .18, .1, .03]), {n: 16, tex: 'gu_bud', ledgeTex: 'gu_bud_l', caps: '-+', seed: 9}),
    ...loft('y', stops([0, .14, .32, .55, .8, 1.05], [.7, .6, .51, .45, .42, .4]), {n: 8, tex: 'gu_drapeW', ledgeTex: 'gu_drape_l', caps: '', seed: 10})];
  for (let k = 0; k < 8; k++) els.push(radialCard('gu_lobe', k * 45 + 22.5, .3, .78, 0, .3));
  els.push(abox([-.13, .24, -.62], [.13, .5, -.5], 'gu_gem', {rot: ['x', -22.5, [0, .37, -.56]]}));
  return els;
}
const guardWisp = () => [...shapeSlab('g_wisp', 'gu_wisp', 'z', 0, {half: .05, cell: .08, inset: .5, edge: 'gu_wisp'}), ...shapeSlab('g_wisp', 'gu_wisp', 'x', 0, {half: .04, core: false})];
const guardOrb = () => [...orb([0, 0, 0], .2, 'gu_orb'), ...crossCards('gu_orb', [0, 0, 0], .6, .6, {y0: -.3})];

// ================================================================================================================
// 둥지 nesting: the pointed cap with the eye, two sepal wings (children of the cap)
// ================================================================================================================
function nestCap() {
  const els = [...loft('y', stops([.1, .26, .42, .58, .72, .86, .98, 1.12], [.3, .29, .25, .19, .13, .08, .045, .02]).map(s => ({...s, c: [0, -.04]})), {n: 16, tex: 'ne_cap', ledgeTex: 'ne_cap_l', caps: '-', seed: 11}),
    ...loft('y', stops([-.3, -.1, .12], [.17, .21, .22]).map(s => ({...s, c: [0, -.08]})), {n: 8, tex: 'ne_cap', ledgeTex: 'ne_cap_l', caps: '-', seed: 13})];
  els.push(...shapeSlab('w_ring', 'ne_ring', 'z', -.17, {half: .035, cell: .04, inset: .4}));
  els.push(...orb([0, 0, -.13], .12, 'ne_orb'));
  els.push(quad('ne_drop', [-.07, -.24, -.19], [.14, 0, 0], [0, -.22, 0]));
  for (let k = 0; k < 8; k++) els.push(radialCard('ne_thorn', k * 45 + 22.5, .24, .34, .02, .14));
  return els;
}
const nestWing = () => shapeSlab('w_wing', 'ne_wing', 'z', 0, {half: .03, cell: .05, inset: .5});

// ================================================================================================================
// 파괴 destruction: the armoured ball (open front), its glowing face + beak; the split husk
// ================================================================================================================
const BALL = {z: [-.44, -.36, -.26, -.14, -.02, .1, .22, .34, .45, .54, .6], R: .6};
function destrShell(husk) {
  const st = BALL.z.map(z => ({a: z, r: Math.sqrt(Math.max(.0025, BALL.R * BALL.R - z * z)) * (z === -.44 ? 1 : 1)}));
  if (husk) {
    // two half shells, split along x and pushed apart, the halves tipped open
    const half = side => loft('z', st, {n: 16, tex: 'de_shell', ledgeTex: 'de_shell_l', caps: '+', tint: true, skip: k => (side > 0 ? (k > 4 && k < 12) : (k < 4 || k > 12))});
    return [...shift(half(1), [.12, 0, 0]), ...shift(half(-1), [-.12, 0, 0])];
  }
  const els = [...loft('z', st, {n: 16, tex: 'de_shell', ledgeTex: 'de_shell_l', caps: '+', seed: 17}), ...annulus('z', [0, 0, 0], -.44, .3, .41, '-', 'de_rim', {n: 16, stagger: .002})];
  // 12 cone spikes on the axis-aligned and 45-degree directions (none on the open front)
  const S = (dir, rot) => spike('de_spike', dir.map(x => x * .5), dir, .46, .26, rot);
  els.push(...S([0, 1, 0]), ...S([0, -1, 0]), ...S([1, 0, 0]), ...S([-1, 0, 0]), ...S([0, 0, 1]));
  for (const [dir, rot] of [[[0, 1, 0], ['x', 45]], [[0, -1, 0], ['x', -45]], [[0, 1, 0], ['z', 45]], [[0, 1, 0], ['z', -45]], [[0, -1, 0], ['z', 45]], [[0, -1, 0], ['z', -45]], [[1, 0, 0], ['y', -45]], [[-1, 0, 0], ['y', 45]]])
    els.push(...S(dir, rot));
  return els;
}
function destrFace() {
  return [cardZ('de_face', -.38, {X0: -.4, X1: .4, Y0: -.4, Y1: .4}),
    ...loft('z', stops([-.38, -.46, -.53], [.09, .07, .02]), {n: 8, tex: 'de_beak', caps: '+', seed: 19})];
}

// ================================================================================================================
// 포식성 predatory: body looks fish / fish_flare / bud / pod / face; the jaw bowl, the tail fin, the core (children)
// ================================================================================================================
// the fish hood: a leaf-shaped shell, pointed at the snout (-Z) and toward the tail, widest a little before the middle,
// a high rounded back and a flat underside where the translucent bowl hangs (profile leaf(s), s = 0 snout .. 1 tail)
const FISH = {z0: -1.25, z1: 1.2, w: .54, top: .6, bot: .12};
const leaf = z => { const s = Math.min(1, Math.max(0, (z - FISH.z0) / (FISH.z1 - FISH.z0))); return s < .42 ? Math.sin(Math.PI / 2 * s / .42) ** 1.4 : Math.sin(Math.PI / 2 * (1 - s) / .58) ** .9; };
const FISH_U = [0, .04, .1, .19, .3, .43, .57, .71, .83, .93, 1];
const fishZ = FISH_U.map(u => FISH.z0 + u * (FISH.z1 - FISH.z0));
const topAt = z => FISH.top * leaf(z) + .02;
function predFish(flare) {
  const st = fishZ.map(a => { const L = leaf(a); return {a, r: [FISH.w * L + .02, FISH.top * L + .02, FISH.w * L + .02, FISH.bot * L + .02], c: [0, 0], box: -.3}; });
  const els = [...loft('z', st, {n: 16, tex: 'pr_hood', ledgeTex: 'pr_hood_l', caps: '-+', seed: 23})];
  for (const [z, big] of [[-.3, 1], [.18, 1], [.62, 0]]) {
    const y = topAt(z) - .08, sp = big ? 'pr_horn' : 'pr_hornS', H = big ? .67 : .36, W = big ? .4 : .24;
    els.push(quad(sp, [-W / 2, y + H - .05, z], [W, 0, 0], [0, -H, 0], {rot: ['x', 22.5, [0, y, z]]}), quad(sp, [0, y + H - .05, z - W / 2], [0, 0, W], [0, -H, 0], {rot: ['x', 22.5, [0, y, z]]}));
  }
  const ew = FISH.w * leaf(-.62) + .03;
  for (const s of [1, -1]) els.push(quad('pr_eye', [s * ew, .26, -.73], [0, 0, .22], [0, -.22, 0]));
  if (flare) {
    for (const [dir, rot] of [[[0, 1, 0]], [[1, 0, 0]], [[-1, 0, 0]], [[0, 1, 0], ['z', 45]], [[0, 1, 0], ['z', -45]], [[0, -1, 0], ['z', 45]], [[0, -1, 0], ['z', -45]]])
      for (const z of [-.55, -.1]) els.push(...spike('pr_flare', [dir[0] * .3, dir[1] * .25, z], dir, .55, .14, rot ? rot : undefined));
  }
  return els;
}
function predJaw() {
  // the translucent bowl under the hood (hinge frame: hinge at body z +0.4), two bottom sepals, the long front fin + gem
  const z0 = -.4, zs = [0, .1, .3, .55, .78, .95].map(u => FISH.z0 + .04 + u * (FISH.z1 - FISH.z0 - .1));
  const st = zs.map(a => { const L = leaf(a); return {a: a + z0, r: [FISH.w * L * .9 + .02, .04, FISH.w * L * .9 + .02, .5 * L + .03], c: [0, -.02]}; });
  const els = [...loft('z', st, {n: 8, tex: 'pr_bowl', ledgeTex: 'pr_bowl_l', caps: '-+', seed: 29})];
  for (const s of [1, -1]) els.push(quad('pr_sepal', [s * .25 - .07, -.94, -.2 + z0], [.14, 0, 0], [0, .62, 0], {rot: ['z', s * 22.5, [s * .25, -.32, -.2 + z0]]}));
  els.push(quad('pr_fin', [.34, -.12, -.62 + z0], [.24, 0, 0], [0, 0, -1.15], {rot: ['y', -22.5, [.46, -.12, -.62 + z0]]}));
  els.push(abox([.38, -.2, -.72 + z0], [.56, -.04, -.56 + z0], 'pr_gem'));
  return els;
}
const predTail = () => [quad('pr_tail', [0, .5, -.04], [0, 0, .94], [0, -1.0, 0])];
const predCore = () => [...orb([0, 0, 0], .22, 'pr_core'), ...crossCards('pr_core', [0, 0, 0], .6, .6, {y0: -.3})];
// the bud (empowered): a diamond 2.1 x 1.6 - a cream ogive of eight petal facets closing to a point (a short horn on
// top, four petals leaning in), over a translucent green star bowl tapering to the lower point, eight sepals at the rim
function predBud() {
  const els = [...loft('y', stops([0, .2, .4, .58, .74, .87, .97, 1.02], [0, .2, .4, .58, .74, .87, .97, 1.02].map(y => .76 * Math.cos(Math.PI / 2 * Math.min(1, y / 1.02)) ** .85 + .02)), {n: 16, tex: 'pr_hood', ledgeTex: 'pr_hood_l', caps: '-', seed: 61}),
    ...loft('y', prof(-.95, 0, 5, y => .7 * (1 - Math.pow(-y / .95, 1.15)) + .02), {n: 8, tex: 'pr_bowl', ledgeTex: 'pr_bowl_l', caps: '', seed: 62})];
  for (let k = 0; k < 4; k++) els.push(tangentCard('pr_petal', k * 90, .7, .82, .82, .84, {tilt: -22.5, pivot: 'bottom'}));
  els.push(...shift(crossCards('pr_horn', [0, 0, 0], .26, .44, {y0: 0}), [0, .9, 0]));
  for (let k = 0; k < 8; k++) els.push(radialCard('pr_sepal', k * 45 + 22.5, .45, 1.02, -.42, .06));
  return els;
}
// the pod (inflated, 3.5 b): a tall double-lobed clam - the round translucent lower lobe holding the core, the cream lid
// lobe closed on top of it at a waist (centre frame: the floor at y -1.3)
function predPod() {
  // sphere-like lobes in equal latitude steps (smooth outlines): the lower lobe 16-sided, the lid 8-sided
  const lat = (c, R, n, k = 1) => Array.from({length: n + 1}, (_, i) => { const th = -Math.PI / 2 + Math.PI * i / n; return {a: c + R * k * Math.sin(th), r: R * Math.cos(th) + .04}; });
  const els = [...loft('y', lat(-.43, .87, 8), {n: 16, tex: 'pr_bowl', ledgeTex: 'pr_bowl_l', caps: '-+', seed: 63}),
    ...loft('y', lat(1.02, .72, 7, 1.12), {n: 8, tex: 'pr_hood', ledgeTex: 'pr_hood_l', caps: '-+', seed: 64})];
  els.push(...shift(crossCards('pr_horn', [0, 0, 0], .3, .5, {y0: 0}), [0, 1.8, 0]));
  return els;
}
function predFace() {
  const els = [...loft('z', prof(-.62, .5, 6, z => { const t = (z + .62) / 1.12; return .75 * Math.sin(Math.PI * Math.min(1, .15 + t * .85)) ** .5 + .02; }), {n: 16, tex: 'pr_face', ledgeTex: 'pr_face_l', caps: '-+', seed: 37})];
  els.push(...crossCards('pr_horn', [0, .66, -.1], .34, .6, {y0: 0}));
  els.push(abox([-.16, -.52, -.6], [.16, -.2, -.5], 'pr_gem', {rot: ['z', 45, [0, -.36, -.55]]}));
  els.push(quad('pr_eye', [-.08, .3, -.66], [.16, 0, 0], [0, -.16, 0]));
  return els;
}

// ================================================================================================================
// the Heart of the Oasis: lemon bulb (looks by tint), root cradle (pedestal / full), two root arms, glow tips, vine
// hand (idle / wrap) and four vine stem segments
// ================================================================================================================
const LEMON = {L: 1.6, W: 1.3, H: 1.15};
function heartBulb() {
  const z = [-1.6, -1.5, -1.36, -1.16, -.9, -.56, -.18, .2, .58, .92, 1.18, 1.38, 1.52, 1.6];
  const f = a => { const t = Math.abs(a) / LEMON.L; return Math.pow(Math.max(0, 1 - t * t), .62) * (1 - .55 * Math.pow(t, 6)) + .035; };
  const els = [...loft('z', z.map(a => ({a, r: [LEMON.W * f(a), LEMON.H * f(a), LEMON.W * f(a), LEMON.H * f(a)]})), {n: 16, tex: 'he_bulb', ledgeTex: 'he_bulb_l', caps: '-+', tint: true, seed: 41})];
  els.push(...tint([cardZ('he_swirl', 0, {X0: -.9, X1: .9, Y0: -.85, Y1: .85}), cardX('he_swirl', 0, {Z0: -1.1, Z1: 1.1, Y0: -.8, Y1: .8}), cardY('he_swirl', 0, {X0: -.9, X1: .9, Z0: -1.1, Z1: 1.1})]));
  return els;
}
// the cradle: a low dark mound and six knobbly root fingers splaying into the turf and gripping the bulb's flanks and
// ends (planes through the bulb axis, offset so none is a mirror of another); pedestal adds pale petal clumps + sprouts
const FINGERS = [
  ['xy', .35, [[2.35, -.05], [1.95, .25], [1.6, .66], [1.46, 1.12], [1.42, 1.6], [1.3, 2.1]]],
  ['xy', -.6, [[2.2, -.05], [1.85, .3], [1.55, .72], [1.44, 1.2], [1.36, 1.7], [1.18, 2.02]]],
  ['xy', .55, [[-2.25, -.05], [-1.9, .28], [-1.58, .7], [-1.45, 1.15], [-1.38, 1.62], [-1.2, 1.98]]],
  ['xy', -.3, [[-2.4, -.05], [-2.0, .22], [-1.62, .62], [-1.47, 1.1], [-1.43, 1.55], [-1.32, 2.06]]],
  ['yz', -.5, [[-.05, 2.6], [.3, 2.15], [.72, 1.8], [1.2, 1.66], [1.6, 1.5], [1.9, 1.3]]].map(x => x),
  ['yz', .45, [[-.05, -2.55], [.28, -2.1], [.7, -1.78], [1.15, -1.66], [1.56, -1.52], [1.86, -1.32]]],
];
function heartCradle(pedestal) {
  const els = [...loft('y', prof(0, .55, 4, y => 1.45 * Math.sqrt(Math.max(0, 1 - (y / .58) ** 2)) + .03), {n: 16, tex: 'he_root', ledgeTex: 'he_root_l', caps: '+', seed: 43})];
  FINGERS.forEach(([pl, c, pts], i) => els.push(...tube(inPlane(pl, c, pts), pl, t => .19 - .12 * t, 'he_root', {seed: 50 + i * 11})));
  if (pedestal) {
    for (let k = 0; k < 6; k++) { const a = (k * 60 + 15) * D2R; els.push(...crossCards('he_petal', [Math.sin(a) * .9, .42, -Math.cos(a) * .9], .56, .34, {y0: 0})); }
    for (const a of [20, 140, 260]) els.push(...crossCards('he_sprout', [Math.sin(a * D2R) * .45, .5, -Math.cos(a * D2R) * .45], .24, .7, {y0: 0}));
  }
  return els;
}
// the two tall root arms rising at the bulb's sides and curling over its top (one taller), two shorter side roots;
// the glow tips sit on their ends (heart_tips)
const ARMS = [
  ['xy', .25, [[1.55, .1], [1.88, .95], [1.98, 1.85], [1.84, 2.75], [1.5, 3.5], [1.0, 4.02], [.45, 4.24], [.02, 4.12], [-.18, 3.84]], .22],
  ['xy', -.4, [[-1.5, .1], [-1.82, .9], [-1.88, 1.75], [-1.7, 2.55], [-1.32, 3.2], [-.82, 3.62], [-.34, 3.74], [.02, 3.55]], .2],
  ['yz', .3, [[.1, 1.75], [.8, 2.02], [1.55, 2.05], [2.15, 1.85], [2.5, 1.55]], .14],
  ['yz', -.55, [[.1, -1.7], [.75, -2.0], [1.4, -2.02], [1.9, -1.84]], .13],
];
const heartArms = () => ARMS.flatMap(([pl, c, pts, r0], i) => tube(inPlane(pl, c, pts), pl, t => r0 * (1 - .7 * t) + .03, 'he_root', {seed: 90 + i * 13}));
function heartTips() {
  const els = [];
  ARMS.forEach(([pl, c, pts], i) => { const P = inPlane(pl, c, pts), e = P[P.length - 1], k = i < 2 ? 1.1 : .75;
    els.push(...crossCards('he_tip', [e[0], e[1] + .05, e[2]], .34 * k, .66 * k, {y0: 0})); });
  // a second flame half way up each tall arm, smaller ones on the finger tips
  for (const i of [0, 1]) { const P = inPlane(ARMS[i][0], ARMS[i][1], ARMS[i][2]), m = P[5]; els.push(...crossCards('he_tip', [m[0], m[1] + .1, m[2]], .28, .52, {y0: 0})); }
  for (const i of [0, 3, 4]) { const [pl, c, pts] = FINGERS[i], e = inPlane(pl, c, pts)[5]; els.push(...crossCards('he_tip', [e[0], e[1] + .02, e[2]], .2, .4, {y0: 0})); }
  return els;
}
// the vine hand (joint = the wrist just above the upright egg's top): six vine fingers hugging the egg (half axes .91 x
// 1.12 at pose scale 0.7, its centre 1.24 below the wrist) from the crown over the shoulder to below the equator, the
// tips curling in; wrap = the grip closed tighter and further down
function vineHand(wrap) {
  const els = [rockBox([-.13, -.12, -.13], [.13, .16, .13], 'he_vine', {seed: 3})];
  const A = .95, B = 1.16, C = -1.24, phiEnd = wrap ? 2.25 : 1.95;
  const finger = (k, off, sgn, plane) => {
    const pts = [];
    for (let i = 0; i <= 4; i++) { const ph = .12 + (phiEnd - .12) * i / 4 + (i === 4 ? .1 : 0), rr = i === 4 ? .9 : 1;
      pts.push([sgn * A * Math.sin(ph) * rr * (1 + .03 * k), C + B * Math.cos(ph) * rr]); }
    return tube(inPlane(plane, off, pts.map(([u, v]) => (plane === 'xy' ? [u, v] : [v, u]))), plane, t => .075 - .04 * t, 'he_vine', {knot: 0, sub: 1, seed: 7 + k});
  };
  els.push(...finger(0, .12, 1, 'xy'), ...finger(1, -.28, 1, 'xy'), ...finger(2, .3, -1, 'xy'), ...finger(3, -.1, -1, 'xy'), ...finger(4, .2, 1, 'yz'), ...finger(5, -.15, -1, 'yz'));
  return els;
}
const vineStem = () => [quad('he_stem', [-.3, .1, 0], [.6, 0, 0], [0, -6.3, 0]), quad('he_stem', [0, .1, -.3], [0, 0, .6], [0, -6.3, 0]), abox([-.07, -6.2, -.07], [.07, .05, .07], 'he_root')];

// ================================================================================================================
// domes, wall blade, stalks, seed
// ================================================================================================================
// the dome: a hemisphere-like shell r 4.45, h 4.22 in 8 bands of equal latitude steps (tall near the ground, thin near
// the top), each a two-sided 16-gon ring, the steps closed by two-sided annuli, a small cap on top
const DOME = Array.from({length: 8}, (_, i) => { const a0 = i * 11.25 * D2R, a1 = (i + 1) * 11.25 * D2R, am = (a0 + a1) / 2;
  return [r4(4.22 * Math.sin(a0)), r4(4.22 * Math.sin(a1)), r4(4.45 * Math.cos(am) + .02)]; });
function domeShell() {
  const els = [];
  for (const [y0, y1, r] of DOME) els.push(...band([0, 0, 0], r, y0, y1, 'do_shell'));
  for (let i = 0; i < DOME.length - 1; i++) els.push(...annulus('y', [0, 0, 0], DOME[i][1], DOME[i + 1][2] - .01, DOME[i][2], '+-', 'do_shell', {n: 16, stagger: .003}));
  els.push(...annulus('y', [0, 0, 0], DOME[DOME.length - 1][1], 0, DOME[DOME.length - 1][2], '+-', 'do_shell', {n: 8, stagger: .003}));
  return els;
}
function domeDecor() {
  const els = [];
  for (const [y0, y1, r] of DOME.slice(0, 2)) els.push(...band([0, 0, 0], r - .05, y0, y1, 'do_vine'));
  els.push(...band([0, 0, 0], 4.47, 0, .32, 'do_rim'));
  els.push(...crossCards('do_sprout', [0, 4.18, 0], .6, .7, {y0: 0}));
  return els;
}
function wallBlade() {
  // a slightly cupped blade: three strips (the side ones turned 22.5 degrees), the midrib as a thin box
  const R = SH.wa_blade.rect, W = R.u1 - R.u0, H = R.v1 - R.v0, w3 = W / 3;
  return [quad('wa_blade', [-w3 / 2, H, 0], [w3, 0, 0], [0, -H, 0], {uvr: [1 / 3, 0, 2 / 3, 1]}),
    quad('wa_blade', [w3 / 2, H, 0], [w3, 0, 0], [0, -H, 0], {uvr: [2 / 3, 0, 1, 1], rot: ['y', -22.5, [w3 / 2, 0, 0]]}),
    quad('wa_blade', [-w3 * 1.5, H, 0], [w3, 0, 0], [0, -H, 0], {uvr: [0, 0, 1 / 3, 1], rot: ['y', 22.5, [-w3 / 2, 0, 0]]})];
}
const stalkLow = () => loft('y', stops([-.4, .3, 1.0, 1.7, 2.3, 2.7], [.56, .5, .46, .43, .41, .4]), {n: 16, tex: 'st_bark', ledgeTex: 'st_bark_l', caps: '-+', seed: 47});
const stalkHigh = () => loft('y', stops([-.05, .6, 1.2, 1.7, 2.1], [.4, .38, .35, .31, .28]), {n: 16, tex: 'st_bark', ledgeTex: 'st_bark_l', caps: '-+', seed: 53});
const stalkTip = () => [...shapeSlab('s_hook', 'st_hook', 'x', 0, {half: .17, cell: .1, inset: .5, edge: 'st_bark'}), ...spike('st_cone', [0, 1.3, -.3], [0, 1, 0], .3, .16, ['x', 45])];
const seedModel = () => [...crossCards('se_seed', [0, .17, 0], .26, .34, {y0: -.17, three: true}), quad('se_seed', [-.13, .02, .17], [.26, 0, 0], [0, 0, -.34])];

// ================================================================================================================
// the structure
// ================================================================================================================
// display: {name, scale, pivot, joint [x,y,z] (rest, in the parent frame), parent, frame ('object' | 'joint'), bright,
//   looks {look: item}, def, overlay, models {model: () => elements}, cull [w, h] (fixed objects), note}
const D = (name, o) => ({name, parent: null, frame: 'joint', overlay: false, bright: 14, scale: 1, pivot: 'feet', joint: [0, 0, 0], ...o});
export const ORG = {
  basic: {type: 'kind', id: 1, name: '기본', hover: 0, hp_bar_y: 1.6, shield: {w: 1.2, h: 1.6}, size: {h: 1.15, h_stem: 1.35, d: 0.9, bag: [1.43, 1.31]},
    displays: [
      D('bulb', {pivot: 'feet', frame: 'object', looks: {bell: 'basic_bulb_bell', bag: 'basic_bulb_bag', buffed: 'basic_bulb_buffed', bag_buffed: 'basic_bulb_bag_buffed', dying: 'basic_bulb_dying', bag_dying: 'basic_bulb_bag_dying'}, def: 'bell',
        // a clip's look switch keeps the bulb's variant: {to: {from: alt}} (bell -> bag keeps the buff; dying keeps the form)
        variants: {bag: {buffed: 'bag_buffed'}, dying: {bag: 'bag_dying', bag_buffed: 'bag_dying'}},
        models: {basic_bulb_m_bell: bellModel, basic_bulb_m_bag: bagModel},
        items: {basic_bulb_bell: ['basic_bulb_m_bell', 0xEFEEE8], basic_bulb_buffed: ['basic_bulb_m_bell', 0xF4FFE0], basic_bulb_dying: ['basic_bulb_m_bell', 0x8E8A76],
          basic_bulb_bag: ['basic_bulb_m_bag', 0xEFEEE8], basic_bulb_bag_buffed: ['basic_bulb_m_bag', 0xF4FFE0], basic_bulb_bag_dying: ['basic_bulb_m_bag', 0x8E8A76]}}),
      // the diagonal facets (one element rotation cannot both turn and tilt a face): bulb_x = the bell's, the bulb turned
      // 45 degrees about its Y; bulb_y = the bag's, the bulb rolled 45 degrees about the bag axis Z; each shows its leader's
      // look (an empty model in the other form)
      ...[['bulb_x', [0, 45, 0], 'bell'], ['bulb_y', [0, 0, 45], 'bag']].map(([nm, rot, form]) => { const L = l => (l.startsWith('bag') ? 'bag' : 'bell'), m = f => (f === form ? `basic_${nm.replace('_', '')}_m_${form}` : 'basic_bulbxy_m_none');
        return D(nm, {pivot: 'feet', frame: 'object', parent: 'bulb', follow: () => rot, lookOf: 'bulb',
          looks: Object.fromEntries(['bell', 'bag', 'buffed', 'bag_buffed', 'dying', 'bag_dying'].map(l => [l, `basic_${nm.replace('_', '')}_${l}`])), def: 'bell',
          variants: {bag: {buffed: 'bag_buffed'}, dying: {bag: 'bag_dying', bag_buffed: 'bag_dying'}},
          models: form === 'bell' ? {basic_bulbx_m_bell: bellModelX, basic_bulbxy_m_none: () => []} : {basic_bulby_m_bag: bagModelX},
          items: Object.fromEntries([['bell', 0xEFEEE8], ['buffed', 0xF4FFE0], ['dying', 0x8E8A76], ['bag', 0xEFEEE8], ['bag_buffed', 0xF4FFE0], ['bag_dying', 0x8E8A76]].map(([l, c]) => [`basic_${nm.replace('_', '')}_${l}`, [m(L(l)), c]])),
          note: `the ${form}'s facets on the diagonal azimuths: the bulb turned 45 degrees about ${form === 'bell' ? 'its Y' : 'the bag axis Z'} (empty in the other form)`}); }),
      D('crown', {pivot: 'centre', joint: BAG_POSE.crown, looks: {closed: 'basic_crown_closed', open: 'basic_crown_open'}, def: 'closed',
        models: {basic_crown_closed: () => crownModel(false), basic_crown_open: () => crownModel(true)}, note: 'the petal crown at the bag neck (scale 0 while a bell); the glow is painted emissive'}),
      D('shield', {pivot: 'feet', frame: 'object', overlay: true, scale: 1.15, looks: {on: 'basic_shield_on'}, def: 'on', models: {basic_shield_on: shieldModel},
        note: '3 cutout vesica panes 0.62 x 1.42 + a low-alpha bubble rim band + a yellow 3-leaf crown; only while shielded (om/basic/shield/on|off)'}),
    ]},
  nurt: {type: 'kind', id: 2, name: '양육', hover: 0, hp_bar_y: 2.8, shield: {w: 1.4, h: 2.6}, size: {h: 2.4},
    displays: [
      D('stalk', {pivot: 'feet', frame: 'object', scale: 1.6, looks: {idle: 'nurt_stalk_idle'}, def: 'idle', models: {nurt_stalk_idle: nurtStalk}, note: 'S-curved dark-teal ribbon with pale rims, fronds, the gold shard'}),
      D('cap', {pivot: 'centre', joint: [0, 2.18, .06], looks: {idle: 'nurt_cap_idle', tilt: 'nurt_cap_tilt'}, def: 'idle', models: {nurt_cap_idle: () => nurtCap(false), nurt_cap_tilt: () => nurtCap(true)}, note: 'cream hood-leaf; tilt = the hood lifted open'}),
      D('orb', {pivot: 'centre', joint: [0, 2.06, -.4], bright: 15, looks: {on: 'nurt_orb_on'}, def: 'on', models: {nurt_orb_on: nurtOrb}, note: 'pulse'}),
      D('ring', {pivot: 'feet', frame: 'object', overlay: true, looks: {on: 'nurt_ring_on'}, def: 'on', models: {nurt_ring_on: nurtRing}, note: 'translucent cylinder r 1.3, h 0.5, only while immune (om/nurt/ring/on|off)'}),
    ]},
  guard: {type: 'kind', id: 3, name: '수호', hover: 0, hp_bar_y: 3.0, shield: {w: 1.4, h: 3.0}, size: {h: 4.4, bud: 2.0, orb_d: 0.4},
    displays: [
      D('spire', {pivot: 'mid', frame: 'object', scale: 1.6, joint: [0, 2.2, 0], looks: {spire: 'guard_spire_spire', bud: 'guard_spire_bud', wisp: 'guard_spire_wisp'}, def: 'spire',
        models: {guard_spire_spire: guardSpire, guard_spire_bud: guardBud, guard_spire_wisp: guardWisp}}),
      D('orb', {pivot: 'mid', joint: [0, 5.05, 0], bright: 15, looks: {on: 'guard_orb_on'}, def: 'on', models: {guard_orb_on: guardOrb}, note: 'bobs 0.6-0.8 above the tip'}),
    ]},
  nest: {type: 'kind', id: 4, name: '둥지', hover: 1.0, hp_bar_y: 2.75, shield: {w: 1.6, h: 2.2}, size: {w: 2.2, h: 1.3},
    displays: [
      D('cap', {pivot: 'centre', joint: [0, 1.3, 0], looks: {idle: 'nest_cap_idle'}, def: 'idle', models: {nest_cap_idle: nestCap}, note: 'cap + the orb eye (painted emissive)'}),
      D('wing_l', {pivot: 'centre', parent: 'cap', joint: [.17, .02, .02], looks: {idle: 'nest_wing_l_idle'}, def: 'idle', models: {nest_wing_l_idle: nestWing}}),
      D('wing_r', {pivot: 'centre', parent: 'cap', joint: [-.17, .02, .02], looks: {idle: 'nest_wing_r_idle'}, def: 'idle', models: {nest_wing_r_idle: () => mirrorX(nestWing())}}),
    ]},
  destr: {type: 'kind', id: 5, name: '파괴', hover: 0, hp_bar_y: 1.75, shield: {w: 1.3, h: 1.3}, size: {d: 1.2, spikes: 0.2, beak: 0.4},
    displays: [
      D('shell', {pivot: 'centre', joint: [0, .62, 0], spinAxis: 'x', looks: {normal: 'destr_shell_normal', husk: 'destr_shell_husk'}, def: 'normal',
        models: {destr_shell_normal: () => destrShell(false), destr_shell_m_husk: () => destrShell(true)}, items: {destr_shell_husk: ['destr_shell_m_husk', 0x3A3833]}}),
      D('face', {pivot: 'centre', joint: [0, .62, 0], spinAxis: 'x', bright: 15, looks: {on: 'destr_face_on'}, def: 'on', models: {destr_face_on: destrFace}, note: 'pulse scale'}),
    ]},
  pred: {type: 'kind', id: 6, name: '포식성', hover: 1.2, hp_bar_y: 2.75, shield: {w: 1.6, h: 1.6}, size: {fish: [2.5, 1.3], bud: [2.1, 1.6], pod: [3.5, 1.8]},
    displays: [
      D('body', {pivot: 'centre', joint: [0, 1.3, 0], scale: 1.6, looks: {fish: 'pred_body_fish', fish_flare: 'pred_body_fish_flare', bud: 'pred_body_bud', pod: 'pred_body_pod', face: 'pred_body_face'}, def: 'fish',
        models: {pred_body_fish: () => predFish(false), pred_body_fish_flare: () => predFish(true), pred_body_bud: predBud, pred_body_pod: predPod, pred_body_face: predFace},
        note: 'fish = the leaf-shark hood; bud / pod / face are their own models (jaw and fin hidden)'}),
      D('jaw', {pivot: 'centre', parent: 'body', joint: [0, -.02, .4], scale: 1.6, looks: {idle: 'pred_jaw_idle'}, def: 'idle', models: {pred_jaw_idle: predJaw}, note: 'the translucent bowl, sepals and the long front fin; hinge behind the middle'}),
      D('fin', {pivot: 'centre', parent: 'body', joint: [0, .02, 1.12], looks: {idle: 'pred_fin_idle'}, def: 'idle', models: {pred_fin_idle: predTail}, note: 'the tail fin; yaw +-25 in pred_swim'}),
      D('core', {pivot: 'centre', parent: 'body', joint: [0, -.08, -.2], bright: 15, looks: {on: 'pred_core_on'}, def: 'on', models: {pred_core_on: predCore}}),
    ]},
  heart: {type: 'object', kind: 'single', tag: 'rlk_mb_ap_heart', cull: [9, 30],
    displays: [
      D('heart_bulb', {idx: 0x00, pivot: 'centre', joint: [0, 1.6, 0], scale: 1.2, bright: 15, looks: {idle: 'heart_bulb_idle', egg_gold: 'heart_bulb_egg_gold', egg_green: 'heart_bulb_egg_green', withered: 'heart_bulb_withered', blaze: 'heart_bulb_blaze'}, def: 'idle',
        models: {heart_bulb_m: heartBulb}, items: {heart_bulb_idle: ['heart_bulb_m', 0xDCEB5C], heart_bulb_egg_gold: ['heart_bulb_m', 0xF5CF4A], heart_bulb_egg_green: ['heart_bulb_m', 0xA8D850],
          heart_bulb_withered: ['heart_bulb_m', 0x8A8258], heart_bulb_blaze: ['heart_bulb_m', 0xFFFCD8]},
        note: 'translucent lemon seed 3.2 x 2.6 x 2.3, alpha ~0.86; the arrival egg = this model at scale 0.7, pitch 90 (upright)'}),
      D('heart_cradle', {idx: 0x01, pivot: 'mid', frame: 'object', joint: [0, .9, 0], scale: 2.2, looks: {pedestal: 'heart_cradle_pedestal', full: 'heart_cradle_full'}, def: 'pedestal',
        models: {heart_cradle_pedestal: () => heartCradle(true), heart_cradle_full: () => heartCradle(false)}, note: '5 knobbly root fingers + the mound; pedestal adds pale petal clumps + 3 gold sprouts'}),
      D('heart_arms', {idx: 0x02, pivot: 'mid', frame: 'object', joint: [0, 2.1, 0], scale: 2.2, looks: {idle: 'heart_arms_idle'}, def: 'idle', models: {heart_arms_idle: heartArms}, note: 'two root arms curling over the bulb to 4.0-4.3 b'}),
      D('heart_tips', {idx: 0x03, pivot: 'mid', frame: 'object', joint: [0, 2.1, 0], scale: 2.2, bright: 15, looks: {idle: 'heart_tips_idle'}, def: 'idle', models: {heart_tips_idle: heartTips}, note: 'leaf-flame sprouts, swaying'}),
      D('vine_hand', {idx: 0x04, pivot: 'centre', joint: [0, 11.2, 0], scale: 1.8, looks: {idle: 'vine_hand_idle', wrap: 'vine_hand_wrap'}, def: 'idle', models: {vine_hand_idle: () => vineHand(false), vine_hand_wrap: () => vineHand(true)}}),
      ...[0, 1, 2, 3].map(k => D('vine_stem_' + k, {idx: 0x05 + k, pivot: 'centre', joint: [0, 26, 0], scale: 4.4, looks: {idle: 'heart_vine_stem'}, def: 'idle', models: k ? {} : {heart_vine_stem: vineStem}, note: 'stretched along its length between the canopy rim and the hand'})),
    ]},
  dome: {type: 'object', kind: 'fixed_set', count: 3, radius: 4.5, tag: 'rlk_mb_ap_dome', cull: [10, 5],
    displays: [
      D('dome_shell', {idxs: [0x10, 0x12, 0x14], pivot: 'feet', frame: 'object', scale: 3.3, looks: {idle: 'dome_shell_idle'}, def: 'idle', models: {dome_shell_idle: domeShell}, note: 'two-sided shell, alpha <= 0.35'}),
      D('dome_decor', {idxs: [0x11, 0x13, 0x15], pivot: 'feet', frame: 'object', scale: 3.3, looks: {idle: 'dome_decor_idle'}, def: 'idle', models: {dome_decor_idle: domeDecor}, note: 'cutout vine band, bright base rim, sprout on top'}),
    ]},
  wall: {type: 'object', kind: 'multi', max: 15, tag: 'rlk_mb_ap_wall', cull: [2, 3.2], blocks: {block: 'minecraft:barrier', y: [201, 202], place: 'replace air'},
    displays: [D('wall_blade', {pivot: 'feet', frame: 'object', scale: 2.0, looks: {idle: 'wall_blade_idle'}, def: 'idle', models: {wall_blade_idle: wallBlade}, note: 'translucent yellow-green blade 0.9 x 2.86, midrib, two windows'})]},
  stalk: {type: 'object', kind: 'fixed_set', count: 4, height: [5.5, 6.0], tag: 'rlk_mb_ap_stalk', cull: [14, 7],
    displays: [
      D('stalk_low', {idxs: [0x20, 0x23, 0x26, 0x29], pivot: 'feet', joint: [0, 0, 0], scale: 1.9, bright: 13, looks: {idle: 'stalk_low_idle'}, def: 'idle', models: {stalk_low_idle: stalkLow}}),
      D('stalk_high', {idxs: [0x21, 0x24, 0x27, 0x2A], pivot: 'feet', parent: 'stalk_low', joint: [0, 2.62, 0], scale: 1.5, bright: 13, looks: {idle: 'stalk_high_idle'}, def: 'idle', models: {stalk_high_idle: stalkHigh}}),
      D('stalk_tip', {idxs: [0x22, 0x25, 0x28, 0x2B], pivot: 'feet', parent: 'stalk_high', joint: [0, 2.02, 0], scale: 1.1, looks: {idle: 'stalk_tip_idle'}, def: 'idle', models: {stalk_tip_idle: stalkTip}, note: 'hooked tip + small gold cone'}),
    ]},
  seed: {type: 'object', kind: 'single', tag: 'rlk_mb_ap_seed', cull: [1, 1],
    displays: [D('seed', {idx: 0x30, pivot: 'feet', bright: 15, looks: {idle: 'seed_idle'}, def: 'idle', models: {seed_idle: seedModel}, note: 'glowing golden seed at the death spot'})]},
};
export const KINDS = Object.keys(ORG).filter(k => ORG[k].type === 'kind');
export const OBJECTS = Object.keys(ORG).filter(k => ORG[k].type === 'object');
// rest world position of a display's joint (object frame), parents first
export function restJoint(owner, name) {
  const d = ORG[owner].displays.find(x => x.name === name);
  const p = d.parent ? restJoint(owner, d.parent) : [0, 0, 0];
  return p.map((v, i) => v + d.joint[i]);
}
// every model (block geometry converted to model units for its display's scale): {model: {els, owner, display}}
export function allModels() {
  const out = {};
  for (const [owner, o] of Object.entries(ORG)) for (const d of o.displays) for (const [m, build] of Object.entries(d.models || {})) {
    let els = build();
    if (d.frame === 'object') els = shift(els, restJoint(owner, d.name).map(v => -v));
    out[m] = {els: toUnits(els, d.scale), owner, display: d.name};
  }
  return out;
}
// item definitions: {item: {model, tint (int | null), owner, display, look}}; untinted looks point at their own model
export function allItems() {
  const out = {};
  for (const [owner, o] of Object.entries(ORG)) for (const d of o.displays) for (const [look, item] of Object.entries(d.looks)) {
    if (out[item]) continue;
    const t = d.items && d.items[item];
    out[item] = {model: t ? t[0] : item, tint: t ? t[1] : null, owner, display: d.name, look};
  }
  return out;
}
