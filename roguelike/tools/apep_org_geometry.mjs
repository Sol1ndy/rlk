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
import {loft, slab, crossCards, toUnits, mirrorX, rockBox, stroke} from './mboss_shape_lib.mjs';
import {SH, addSprite, skinSprite, stalkSkin, PAL, bellFacetPx, bulbFacetPx, domeFacetPx, bellR, skirtR, BAG, bagR, smooth01, guardFacetPx, nestFacetPx, destrFacetPx, predSolidPx, predGlassPx, RIB, nurtRibPx, nurtHoodPx, hoodKeep, hoodNear} from './apep_org_paint.mjs';

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
// a 3-box rounded orb (glow balls): reads round at the sizes used here
const orb = (c, r, tex) => [abox([c[0] - r, c[1] - r * .62, c[2] - r * .62], [c[0] + r, c[1] + r * .62, c[2] + r * .62], tex),
  abox([c[0] - r * .62, c[1] - r, c[2] - r * .62], [c[0] + r * .62, c[1] + r, c[2] + r * .62], tex), abox([c[0] - r * .62, c[1] - r * .62, c[2] - r], [c[0] + r * .62, c[1] + r * .62, c[2] + r], tex)];
// a glowing ball: seven glow discs through the centre (the three axis planes, the two vertical diagonals, two tilted
// 45 degrees): round from every side, bright at the core
function glowBall(c, r, sprite) {
  const [x, y, z] = c, d = 2 * r;
  return [quad(sprite, [x - r, y + r, z], [d, 0, 0], [0, -d, 0]), quad(sprite, [x, y + r, z - r], [0, 0, d], [0, -d, 0]), quad(sprite, [x - r, y, z - r], [d, 0, 0], [0, 0, d]),
    quad(sprite, [x - r, y + r, z], [d, 0, 0], [0, -d, 0], {rot: ['y', 45, c]}), quad(sprite, [x, y + r, z - r], [0, 0, d], [0, -d, 0], {rot: ['y', 45, c]}),
    quad(sprite, [x - r, y, z - r], [d, 0, 0], [0, 0, d], {rot: ['x', 45, c]}), quad(sprite, [x - r, y, z - r], [d, 0, 0], [0, 0, d], {rot: ['x', -45, c]})];
}
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
// a smooth tapered root limb in a vertical plane ('xy': z = c, 2D points [x, y]; 'yz': x = c, points [z, y]): a chain of
// boxes along the Catmull-Rom centreline (each turned about the plane normal to its segment, snapped to the 22.5 grid),
// half width r(t) in the plane and k r(t) across it, the faces painted with the rounded side sprite (u across the face,
// v along the root by arc length: the grain runs on), plus a two-sided skin card in the plane with the smooth tapered
// silhouette (half width 1.1 r): the outline reads smooth from the front and the back, the boxes give the volume.
// sprite: the skin's sprite name (registered here, ppb px per block); end: the last box's far face shown (a cut tip)
const ROOT_TILE = {he_rootS: 4, he_vineS: 64 / 24, st_sideS: 4};    // the side sprite's length in blocks (v repeats)
function rootLimb(sprite, plane, c, P0, r, {side = 'he_rootS', k = .85, sub = 3, ppb = 16, R, owner = 'heart', skin = 1.1, end = false, kin = null, style = null, skinAt = 'mid'} = {}) {
  // skinAt 'faces': two skin cards on the limb's flat sides (at the widest box's half thickness) instead of one in its
  // middle plane: a flat blade (the stalks) shows its painted face from the side; the boxes keep only their edges
  // (with a skin card the boxes stay inside its outline in the plane: kin = their in-plane share of r)
  if (kin === null) kin = sprite ? .82 : 1;
  const P = [];
  for (let i = 0; i < P0.length - 1; i++) for (let j = 0; j < sub; j++) {
    const t = j / sub, a = P0[Math.max(0, i - 1)], b = P0[i], cc = P0[i + 1], d = P0[Math.min(P0.length - 1, i + 2)];
    P.push([0, 1].map(q => .5 * (2 * b[q] + (-a[q] + cc[q]) * t + (2 * a[q] - 5 * b[q] + 4 * cc[q] - d[q]) * t * t + (-a[q] + 3 * b[q] - 3 * cc[q] + d[q]) * t * t * t)));
  }
  P.push(P0[P0.length - 1]);
  const segL = P.slice(1).map((p, i) => Math.hypot(p[0] - P[i][0], p[1] - P[i][1])), Ltot = segL.reduce((x, y) => x + y, 0), TL = ROOT_TILE[side];
  // 3D: plane 'xy' -> [u, v, c] (normal Z, rotations about z); 'yz' -> [c, v, u] (normal X, rotations about x)
  const to3 = ([u, v]) => (plane === 'xy' ? [u, v, c] : [c, v, u]), ax = plane === 'xy' ? 'z' : 'x', nIdx = plane === 'xy' ? 2 : 0, uIdx = plane === 'xy' ? 0 : 2;
  const els = [];
  let arc = 0;
  for (let i = 0; i < P.length - 1; i++) {
    const A = to3(P[i]), B = to3(P[i + 1]), L = segL[i], t3 = A.map((x, q) => (B[q] - x) / L);
    let best = null;
    for (const dAx of [uIdx, 1]) for (const g of [0, 22.5, -22.5, 45, -45]) {
      const d = [0, 0, 0]; d[dAx] = 1; const qv = rotA(ax, g, d);
      const e = Math.min(Math.hypot(qv[0] - t3[0], qv[1] - t3[1], qv[2] - t3[2]), Math.hypot(qv[0] + t3[0], qv[1] + t3[1], qv[2] + t3[2]));
      if (!best || e < best.e - 1e-9) best = {dAx, g, e};
    }
    const tm = (arc + L / 2) / Ltot, rr = r(tm), M = A.map((x, q) => (x + B[q]) / 2), h = L / 2 + rr * .22;
    const oAx = best.dAx === 1 ? uIdx : 1;          // the other in-plane axis
    const half = [0, 0, 0]; half[best.dAx] = h; half[oAx] = rr * kin; half[nIdx] = rr * k;
    const lo = M.map((x, q) => x - half[q]), hi = M.map((x, q) => x + half[q]);
    const span = Math.min(1, 2 * h / TL), v0 = ((arc / TL) % 1) * (1 - span), vk = span / (2 * h);
    const faces = {};
    for (const nAx of skinAt === 'faces' && sprite ? [oAx] : [oAx, nIdx]) for (const sg of [1, -1]) {
      const dir = [0, 0, 0]; dir[nAx] = sg;
      const acr = nAx === oAx ? nIdx : oAx, up = rotA(ax, best.g, dir)[1] > .5;      // a face looking up: the darker grain
      faces[faceOfDir(dir)] = {tex: up ? side + 'U' : side, fn: X => [16 * (X[acr] - lo[acr]) / (hi[acr] - lo[acr]), 16 * (v0 + (X[best.dAx] - lo[best.dAx]) * vk)]};
    }
    if (end && i === P.length - 2) { const dir = [0, 0, 0]; const tq = rotA(ax, -best.g, t3); dir[best.dAx] = tq[best.dAx] > 0 ? 1 : -1; faces[faceOfDir(dir)] = {tex: side, uv: [4, 14, 12, 16]}; }
    els.push(faceEl([lo, hi], faces, {rot: best.g ? [ax, best.g, M] : undefined}));
    arc += L;
  }
  // the skin card
  if (sprite) {
    const st = stroke(P, t => r(t) * skin), pad = Math.max(...Array.from({length: 11}, (_, q) => r(q / 10))) * skin + .04;
    const us = P.map(p => p[0]), vs = P.map(p => p[1]);
    const rect = {u0: Math.min(...us) - pad, u1: Math.max(...us) + pad, v0: Math.min(...vs) - pad, v1: Math.max(...vs) + pad};
    skinSprite(sprite, rect, st, t => r(t) * skin, ppb, owner, R, plane === 'xy' ? 'z' : 'x', style);
    const at = skinAt === 'faces' ? [1, -1].map(sg => c + sg * (k * Math.max(...Array.from({length: 11}, (_, q) => r(q / 10))) + .012)) : [c];
    for (const x of at) els.push(plane === 'xy' ? cardZ(sprite, x, {X0: rect.u0, X1: rect.u1, Y0: rect.v0, Y1: rect.v1}) : cardX(sprite, x, {Z0: rect.u0, Z1: rect.u1, Y0: rect.v0, Y1: rect.v1}));
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
// turns: the display turns the faces are split over (azimuth mod 90 of a tilted face; the end caps and, with vertMain,
// the faces parallel to the axis ride the first display: one rotation about the axis turns them)
// split(face) -> key: the elements grouped by key ({key: [half 0, half 1, ..]}; several looks sharing one sprite)
export function facetBody(name, faces, {owner, ppb = 64, paint, cls = () => 0, tint: tn = false, down = null, flat = null, translucent = false, maxPx = 64, aa = false, turns = [0, 45], vertMain = false, split = null} = {}) {
  const dnOf = f => down || ((f.axis || 'y') === 'z' ? [0, 0, -1] : [0, -1, 0]);
  // (a display turned by +tu about the axis shows, cardinal in its own frame, the faces at azimuth -tu mod 90)
  const turnOf = f => (Math.abs(f.el) > 89.9 || (vertMain && Math.abs(f.el) < 1e-6) ? 0 : Math.round(((90 - (((f.az % 90) + 90) % 90)) % 90) * 10) / 10);
  const cards = faces.map(f => { const tu = turnOf(f), half = turns.indexOf(tu);
    if (half < 0) throw new Error(`${name}: face az ${f.az} el ${f.el} needs a display turned ${tu}`);
    return {f, half, card: faceCard(f, tu ? {axis: f.axis || 'y', deg: tu} : null, dnOf(f))}; });
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
  for (const m of masks) { const k = flat && flat(m.f) ? 8 / Math.max(m.card.w, m.card.h) : ppb; m.pw = Math.max(8, Math.min(maxPx, Math.round(m.card.w * k))); m.ph = Math.max(8, Math.min(maxPx, Math.round(m.card.h * k))); }
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
    // aa (translucent bodies): the edge pixels carry their coverage as alpha, so two faces meeting at an edge sum to
    // one layer (no doubled seam, no stairs); opaque bodies cut binary masks half a pixel past the edge (no gaps)
    if (sd > px * (aa ? .5 : .6)) return [0, 0, 0, 0];
    const c = paint({el: m.card.el, n: m.f.n, cls: m.cls, w: card.w, h: card.h, f: m.f, mask: card.mask}, s, t, Math.max(0, -sd));
    if (aa) { const cov = Math.max(0, Math.min(1, .7 - sd / px)); return [c[0], c[1], c[2], Math.round((c[3] ?? 255) * cov)]; }
    return c;
  }, owner, translucent);
  const els = turns.map(() => []), groups = {};
  for (const c of cards) {
    const m = masks[c.mi], u0 = m.px0 / SW, u1 = (m.px0 + m.pw) / SW, v0 = m.py0 / SH_, v1 = (m.py0 + m.ph) / SH_;
    const e = quad(name, c.card.P0, c.card.du, c.card.dv, {rot: c.card.rot, uvr: [c.flip ? u1 : u0, v0, c.flip ? u0 : u1, v1], tint: tn});
    if (split) (groups[split(c.f)] ||= turns.map(() => []))[c.half].push(e); else els[c.half].push(e);
  }
  return split ? groups : els;
}
// the support function of a point cloud (any convex hull: lumpy, non-symmetric bodies)
export const pointSupport = P => n => { let m = -Infinity; for (const p of P) { const v = p[0] * n[0] + p[1] * n[1] + p[2] * n[2]; if (v > m) m = v; } return m; };
// the support function of a body of revolution about 'y' (radius rf(a), a in [a0, a1]) or 'z' (centre height yc)
export const revSupport = (rf, a0, a1, axis = 'y', yc = 0) => n => {
  const A = axis === 'y' ? n[1] : n[2], hz = axis === 'y' ? Math.hypot(n[0], n[2]) : Math.hypot(n[0], n[1]);
  let m = -Infinity; for (let i = 0; i <= 160; i++) { const a = a0 + (a1 - a0) * i / 160; m = Math.max(m, rf(a) * hz + a * A); }
  return m + (axis === 'z' ? yc * n[1] : 0);
};

// ================================================================================================================
// 기본 basic: bell (melee, walks) / bag (ranged, lying), a petal crown at the bag neck, the 수호 shield overlay
// ================================================================================================================
// bell (1.15 b, 1.35 with the stem; v4 f186 / f2310 / v3 f900): a facet body round the smooth bell (bellR: an egg on its
// narrow end, widest at two thirds of its height, a tall round top): 8 azimuths x elevations -22.5 .. 67.5 + the top,
// the dark underside at y .14; the skirt is two more rings of 8 faces: the hanging lobes (elevation 22.5, y .32 -> .1,
// V notches between them) and their flared tips (elevation 45, y .1 -> 0, each a rounded tongue cut by its mask).
// Faces on the diagonals ride the bulb_x display (the bulb turned 45 degrees).
const BELL_FACES = (() => {
  const body = polyFaces([...facetPlanes(revSupport(bellR, .14, 1.16), {el: [-22.5, 0, 22.5, 45, 67.5, 90]}), {n: [0, -1, 0], h: -.14, az: 0, el: -90}]);
  const ring = (rf, y0, y1, el, cls) => polyFaces([...facetPlanes(revSupport(rf, y0, y1), {el: [el]}), {n: [0, 1, 0], h: y1, az: 0, el: 90, hidden: true}, {n: [0, -1, 0], h: -y0, az: 0, el: -90, hidden: true}])
    .filter(f => !f.hidden).map(f => ({...f, skirt: cls}));
  const skirt = [...ring(skirtR, .1, .32, 22.5, 1), ...ring(skirtR, 0, .1, 67.5, 4)];
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
  let lo = Infinity; for (let i = 0; i <= 60; i++) { const z = BAG.z0 + (.58 - BAG.z0) * i / 60; for (let j = 0; j < 16; j++) lo = Math.min(lo, P(BAG.y + bagR(z) * Math.sin(j * Math.PI / 8), z)[1]); }
  const t = r4(-lo + .01), tip = P(BAG.y, BAG.z0 - .02);
  return {r, t, crown: [0, r4(tip[1] + t), r4(tip[2])], crownR: -(90 - r)};
})();
const BAG_FACES = (() => {
  const faces = polyFaces(facetPlanes(revSupport(z => bagR(z) + .01, BAG.z0, .575, 'z', BAG.y), {axis: 'z', el: [-90, -67.5, -45, -22.5, 0, 22.5, 45, 67.5, 90]}));
  return facetBody('bo_bagF', faces, {owner: 'basic', paint: bellFacetPx, cls: () => 3, tint: true, ppb: 84});
})();
function bagModel() {
  const els = [...BAG_FACES[0]];
  els.push(...tint(loft('z', [{a: BAG.z0 + .02, r: .085, c: [0, BAG.y]}, {a: BAG.z0 + .07, r: .085, c: [0, BAG.y]}], {n: 8, tex: 'bo_stemT', caps: ''})));
  return els;
}
const bagModelX = () => [...BAG_FACES[1]];
// the crown (joint at the bag neck, its +Y along the neck): 4 cardinal petals leaning out, 4 diagonal ones
function crownModel(open) {
  // 4 broad crumpled petals leaning out of the neck (more when open) + 2 small ones between; open adds the lime glow
  const els = [];
  for (let k = 0; k < 4; k++) els.push(open ? tangentCard('bo_petal', k * 90, .05, .42, .42, .44, {tilt: 45, pivot: 'bottom'}) : tangentCard('bo_petal', k * 90, .06, .4, .38, .42, {tilt: 22.5, pivot: 'bottom'}));
  for (const th of [45, 135, 225, 315]) els.push(tangentCard('bo_petal', th, .07, .32, .3, .34));
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
// a twisted ribbon as vertical panels, one per step up its length, each turned (on the 22.5 degree grid) to the
// ribbon's width direction there and showing its own cell of an atlas sprite: the ribbon's cross-sections over the step
// projected onto it (u across, y up), so the panel stair never shows and the outline stays smooth however the
// centreline wanders. spec: c(y) -> [x, z] the centreline, W(y) the width, phi(y) the width direction (deg from +X toward
// +Z), y0 .. y1 in n steps, ppb, paint(v, y, e, side) (v -1 .. 1 across, e = blocks to the nearer edge)
const catmull = (ks, vs) => y => { const n = ks.length; if (y <= ks[0]) return vs[0]; if (y >= ks[n - 1]) return vs[n - 1];
  let i = 0; while (y > ks[i + 1]) i++; const t = (y - ks[i]) / (ks[i + 1] - ks[i]), p0 = vs[Math.max(0, i - 1)], p1 = vs[i], p2 = vs[i + 1], p3 = vs[Math.min(n - 1, i + 2)];
  return .5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t * t * t); };
function ribbonAtlas(name, {c, W, phi, y0, y1, n, ppb, paint, owner}) {
  const ov = .006, cells = [], E0 = [[1, 0, 0], [0, 0, 1]];
  const edge = (y, sg) => { const [x, z] = c(y), a = phi(y) * D2R, h = W(y) / 2; return [x + sg * h * Math.cos(a), y, z + sg * h * Math.sin(a)]; };
  for (let k = 0; k < n; k++) {
    const ya = y0 + (y1 - y0) * k / n - ov, yb = y0 + (y1 - y0) * (k + 1) / n + ov, ym = (ya + yb) / 2, [cx, cz] = c(ym);
    const ph = Math.round(phi(ym) / 22.5) * 22.5, want = [Math.cos(ph * D2R), 0, Math.sin(ph * D2R)];
    let best = null;
    for (const e0 of E0) for (const g of [0, 22.5, -22.5, 45, -45]) { const e = rotA('y', g, e0), d = Math.abs(e[0] * want[0] + e[2] * want[2]); if (!best || d > best.d + 1e-9) best = {e0, g, e, d}; }
    const {e0, g, e} = best, uOf = P => (P[0] - cx) * e[0] + (P[2] - cz) * e[2];
    let lo = Infinity, hi = -Infinity;
    for (let i = 0; i <= 12; i++) { const y = ya + (yb - ya) * i / 12; for (const sg of [-1, 1]) { const u = uOf(edge(y, sg)); lo = Math.min(lo, u); hi = Math.max(hi, u); } }
    lo -= .02; hi += .02;
    cells.push({ya, yb, cx, cz, e0, g, e, lo, hi, uOf, pw: Math.max(4, Math.round((hi - lo) * ppb)), ph: Math.max(4, Math.round((yb - ya) * ppb))});
  }
  // shelf-pack the cells (rows of the sprite)
  const SW = Math.min(256, Math.max(16, Math.ceil(Math.max(...cells.map(q => q.pw)) * 2 / 16) * 16));
  let x = 0, yy = 0, shelf = 0;
  for (const q of cells) { if (x + q.pw > SW) { x = 0; yy += shelf; shelf = 0; } q.px0 = x; q.py0 = yy; x += q.pw; shelf = Math.max(shelf, q.ph); }
  const SH_ = Math.max(16, Math.ceil((yy + shelf) / 16) * 16), grid = new Int32Array(SW * SH_).fill(-1);
  cells.forEach((q, i) => { for (let b = q.py0; b < q.py0 + q.ph; b++) for (let a = q.px0; a < q.px0 + q.pw; a++) grid[b * SW + a] = i; });
  addSprite(name, SW, SH_, (S0, T0) => {
    const X = Math.min(SW - 1, Math.floor(S0 * SW)), Y = Math.min(SH_ - 1, Math.floor(T0 * SH_)), i = grid[Y * SW + X];
    if (i < 0) return [0, 0, 0, 0];
    const q = cells[i], u = q.lo + (S0 * SW - q.px0) / q.pw * (q.hi - q.lo), y = q.yb - (T0 * SH_ - q.py0) / q.ph * (q.yb - q.ya);
    const um = q.uOf(edge(y, -1)), up = q.uOf(edge(y, 1));
    if (u < Math.min(um, up) || u > Math.max(um, up)) return [0, 0, 0, 0];
    const v = Math.abs(up - um) < 1e-6 ? 0 : 2 * (u - um) / (up - um) - 1;
    return paint(v, y, (1 - Math.abs(v)) * W(y) / 2);
  }, owner);
  return cells.map(q => {
    const um = (q.lo + q.hi) / 2, w = q.hi - q.lo, h = q.yb - q.ya, M = [q.cx + q.e[0] * um, (q.ya + q.yb) / 2, q.cz + q.e[2] * um];
    const P0 = [M[0] - q.e0[0] * w / 2, q.yb, M[2] - q.e0[2] * w / 2];
    return quad(name, P0, q.e0.map(v => v * w), [0, -h, 0], {rot: q.g ? ['y', q.g, M] : undefined, uvr: [q.px0 / SW, q.py0 / SH_, (q.px0 + q.pw) / SW, (q.py0 + q.ph) / SH_]});
  });
}
// the stalk (v3 f1300 / f1240): one broad slate-teal ribbon with white rims rising from a fan of pale fronds in an S:
// broad and face-on at the foot, sweeping out to the organism's left while it narrows and turns edge-on (half a twist
// by the top), back over the axis and up the back into the hood; the gold shard on the hood's right flank
// (the twist runs through the narrow waist, y .55 .. 1.4: a vertical panel can only follow the twist in 22.5 degree
// kinks, whose edge mismatch scales with the width; the broad foot and top stay flat, their centreline moving in plane)
const NRIB = {c: (() => { const ks = [0, .45, .9, 1.25, 1.6, 1.95, 2.16], fx = catmull(ks, [0, .18, .34, .32, .16, .02, 0]), fz = catmull(ks, [-.04, -.04, -.01, .04, .1, .17, .21]); return y => [fx(y), fz(y)]; })(),
  W: catmull([0, .3, .6, .95, 1.3, 1.75, 2.16], [.7, .58, .44, .3, .4, .5, .48]), phi: y => 180 * smooth01((y - .55) / .85)};
const NRIB_ELS = ribbonAtlas('nu_ribA', {...NRIB, y0: 0, y1: 2.16, n: 20, ppb: 60, paint: nurtRibPx, owner: 'nurt'});
function nurtStalk() {
  const els = [...NRIB_ELS];
  for (let k = 0; k < 6; k++) {
    const th = [0, 45, 90, 157.5, 270, 315][k], L = [.8, .7, .62, .5, .62, .72][k], [b, g] = baseAz(th), d = unitAz(b), tg = tanAz(b);
    // a frond lying outward on the ground, tip slightly raised (cardinal ones tilted 22.5 up)
    const w = .24, P0 = [d[0] * .08 - tg[0] * w / 2, .03, d[2] * .08 - tg[2] * w / 2];
    let rot = g ? ['y', g, [0, 0, 0]] : null;
    if (!g) { const axis = Math.abs(d[2]) > .5 ? 'x' : 'z'; rot = [axis, axis === 'x' ? (d[2] < 0 ? 22.5 : -22.5) : (d[0] > 0 ? 22.5 : -22.5), [d[0] * .08, .03, d[2] * .08]]; }
    els.push(quad('nu_frond', P0.map((x, i) => x + d[i] * L), [tg[0] * w, 0, tg[2] * w], [-d[0] * L, 0, -d[2] * L], {rot}));
  }
  return els;
}
// the hood (cap frame, round its joint): a cream bonnet over the orb - a facet body round an egg tilted 25 degrees
// forward-down with a pointed tulip tip at the front, cut open underneath and at the lower front (the cut drawn by the
// masks in 3D: nurtHoodPx); tilt = the opening lifted toward the targets. Diagonal faces on cap_x
const HOOD_C = [0, 0, -.14];
const HOOD_FACES = (() => {
  const P = [], tl = 30 * D2R;
  for (let i = 1; i < 12; i++) for (let j = 0; j < 24; j++) { const a = Math.PI * i / 12, b = 2 * Math.PI * j / 24;
    const x = .34 * Math.sin(a) * Math.cos(b), y = .3 * Math.cos(a), z = .52 * Math.sin(a) * Math.sin(b);
    P.push([HOOD_C[0] + x, HOOD_C[1] + y * Math.cos(tl) + z * Math.sin(tl), HOOD_C[2] + z * Math.cos(tl) - y * Math.sin(tl)]); }
  P.push([0, .3, -.12], [0, -.42, -.62]);
  const body = polyFaces(facetPlanes(pointSupport(P), {el: [-90, -67.5, -45, -22.5, 0, 22.5, 45, 67.5, 90]}));
  // both looks in one sprite: faces clear of either cut share their cell
  const faces = ['idle', 'tilt'].flatMap(look => body.filter(f => hoodKeep(f, look)).map(f => ({...f, look, i: body.indexOf(f), cut: hoodNear(f)})));
  return facetBody('nu_hoodF', faces, {owner: 'nurt', paint: nurtHoodPx, cls: f => (f.cut ? f.look + f.i : 'f' + f.i), ppb: 36, maxPx: 24, split: f => f.look});
})();
const nurtCap = look => [...HOOD_FACES[look][0], ...crossCards('nu_gem', [-.36, -.06, -.06], .18, .36, {y0: -.18})];
const nurtCapX = look => HOOD_FACES[look][1];
const nurtOrb = () => glowBall([0, 0, 0], .19, 'nu_orb');
const nurtRing = () => band([0, 0, 0], 1.3, 0, .5, 'nu_ring');

// ================================================================================================================
// 수호 guarding: helix spire (spire / bud / wisp looks, mid pivot) + the hovering orb
// ================================================================================================================
// (v3 f2088 / sheet 07 base): a dark-teal calyx sheath 1.45 b tall, two staggered rows of pale grey-blue scale lobes
// round its foot and a gold crystal in front, out of which two broad pale ribbons wind round each other in a double
// helix (about two turns) to two sharp points at 4.4 / 4.1 b. The sheath is a facet body round a vase (8 azimuths; the
// diagonal faces on spire_x, the spire turned 45 degrees)
const ringPts = (rings, apex) => { const P = []; for (const [y, r] of rings) for (let j = 0; j < 32; j++) { const a = j * Math.PI / 16; P.push([r * Math.cos(a), y, r * Math.sin(a)]); } if (apex) P.push(apex); return P; };
const GUARD_EL = [-90, 0, 22.5, 45, 67.5, 90];
const SHEATH_FACES = (() => {
  const faces = polyFaces(facetPlanes(pointSupport(ringPts([[0, .44], [.1, .45], [.3, .435], [.55, .39], [.8, .32], [1.04, .23], [1.27, .13]], [0, 1.54, 0])), {el: GUARD_EL}));
  return facetBody('gu_sheathF', faces, {owner: 'guard', paint: guardFacetPx, cls: f => (f.el < -80 ? 9 : 0), ppb: 46, maxPx: 40, flat: f => f.el < -80});
})();
// the ribbons: a helical band wrapped round a 16-gon cylinder of radius r(y) (one vertical tangent panel per 22.5
// degree step; the band crosses each panel diagonally). Each step rises RIB.q r and the band is RIB.k r tall, so every
// panel shows the same tile of gu_ribT (the band, pale with a grey under edge and bright upper rim) scaled to it; the
// last RIB.nT panels show the taper tiles (the band narrowing to its point). r shrinks up the spire and widens a little
// at the very top, so the two tips part
const ribR = y => .27 - .13 * smooth01((y - .9) / 2.3) - .04 * smooth01((y - 2.9) / .8) + .06 * smooth01((y - 3.6) / .7);
function ribbon(ph, y0, y1) {
  const steps = []; let y = y0;
  for (let k = 0; ; k++) { const r = ribR(y), dy = RIB.q * r; if (y + dy > y1 + 1e-9) break; steps.push({k, y, r, dy}); y += dy; }
  const n = steps.length, tw = Math.tan(11.25 * D2R);
  return steps.map(({k, y: yb, r, dy}, i) => {
    const j = Math.max(0, i - (n - RIB.nT - 1)), Hp = dy + RIB.k * r, yc = yb + dy / 2;
    return tangentCard('gu_ribT', ph + 22.5 * k, r, yc + Hp / 2, 2 * r * tw * 1.05, Hp, {uvr: [j / RIB.tiles, 0, (j + 1) / RIB.tiles, 1]});
  });
}
const RIB_ELS = [...ribbon(0, .62, 4.42), ...ribbon(180, .62, 4.1)];
function guardSpire() {
  return [...SHEATH_FACES[0], ...RIB_ELS, abox([-.13, .52, -.43], [.13, .72, -.37], 'gu_gem', {rot: ['x', -22.5, [0, .62, -.4]]})];
}
const guardSpireX = () => SHEATH_FACES[1];
// the bud (v4 f560, ~2 b): a teal ogive hood with pale seams and a thin spike over a pale drape (three stacked frustum
// rings flaring to the hem: upright, 22.5 and 45 degrees out; the hem ring cut into rounded tongues), the gold gem in
// front of the drape. Both facet bodies share one sprite; their diagonal faces ride spire_x
const BUD_FACES = (() => {
  const hood = polyFaces(facetPlanes(pointSupport(ringPts([[.84, .47], [1.0, .465], [1.2, .41], [1.4, .33], [1.58, .24], [1.74, .15], [1.88, .07]], [0, 1.99, 0])), {el: GUARD_EL})).map(f => ({...f, part: 'hood'}));
  const ring = (rf, y0, y1, el, part) => polyFaces([...facetPlanes(revSupport(rf, y0, y1), {el: [el]}), {n: [0, 1, 0], h: y1, az: 0, el: 90, hidden: true}, {n: [0, -1, 0], h: -y0, az: 0, el: -90, hidden: true}])
    .filter(f => !f.hidden).map(f => ({...f, part}));
  const t1 = Math.tan(22.5 * D2R), rA = .44, rB = rA + .3 * t1;
  const drape = [...ring(() => rA, .45, .94, 0, 'drape'), ...ring(y => rA + (.45 - y) * t1, .15, .45, 22.5, 'drape'), ...ring(y => rB + (.15 - y), 0, .15, 45, 'hem')];
  const cls = f => (f.el < -80 ? 9 : f.part === 'hood' ? 1 : f.part === 'hem' ? 3 : 2);
  return facetBody('gu_budF', [...hood, ...drape], {owner: 'guard', paint: guardFacetPx, cls, ppb: 40, maxPx: 40, flat: f => f.el < -80});
})();
function guardBud() {
  return [...BUD_FACES[0], ...spike('gu_spike', [0, 1.9, 0], [0, 1, 0], .3, .08), abox([-.12, .24, -.54], [.12, .42, -.48], 'gu_gem', {rot: ['x', -22.5, [0, .33, -.51]]})];
}
const guardBudX = () => BUD_FACES[1];
const guardWisp = () => [...shapeSlab('g_wisp', 'gu_wisp', 'z', 0, {half: .05, cell: .08, inset: .5, edge: 'gu_wisp'}), ...shapeSlab('g_wisp', 'gu_wisp', 'x', 0, {half: .04, core: false})];
const guardOrb = () => glowBall([0, 0, 0], .26, 'gu_orb');

// ================================================================================================================
// 둥지 nesting: the pointed cap with the eye, two sepal wings (children of the cap)
// ================================================================================================================
// (v4 f900 / f840): a blue-teal onion body drawn up into a long sharp spire (a facet body, 8 azimuths: the diagonal
// faces on cap_x), the pale keyhole outline painted round the eye and up the front (nestFacetPx), the glowing eye orb
// set into the front low down inside a pale ring, a gold drop hanging under it
const NEST_FACES = (() => {
  const faces = polyFaces(facetPlanes(pointSupport(ringPts([[-.34, .1], [-.27, .21], [-.14, .29], [.02, .315], [.16, .3], [.32, .25], [.5, .175], [.7, .1], [.88, .05]], [0, 1.12, .02])), {el: [-90, -45, -22.5, 0, 22.5, 45, 67.5, 90]}));
  return facetBody('ne_capF', faces, {owner: 'nest', paint: nestFacetPx, cls: f => (f.el < -80 ? 9 : [315, 0, 45].includes(f.az) && f.el < 80 ? 100 + f.az + f.el : 0), ppb: 40, maxPx: 40, flat: f => f.el < -80});
})();
function nestCap() {
  const els = [...NEST_FACES[0]];
  els.push(...shapeSlab('w_ring', 'ne_ring', 'z', -.33, {half: .03, cell: .04, inset: .4}));
  els.push(...glowBall([0, -.02, -.32], .17, 'ne_orb'));
  els.push(quad('ne_drop', [-.07, -.27, -.37], [.14, 0, 0], [0, -.22, 0]));
  return els;
}
const nestCapX = () => NEST_FACES[1];
const nestWing = () => shapeSlab('w_wing', 'ne_wing', 'z', 0, {half: .03, cell: .05, inset: .5});

// ================================================================================================================
// 파괴 destruction: the armoured ball (open front), its glowing face + beak; the split husk
// ================================================================================================================
// (v4 f1140 / f1200): a dark olive armour ball r .6 (a facet body round Z, 8 azimuths x 22.5 degree elevations; the
// diagonal faces on shell_x, the shell rolled 45 degrees about Z), open in front where the glowing face sits in a pale
// rim, 13 dark cone spikes. Both looks share the tinted sprite (normal = white tint): the husk is the shell split
// along X, the halves pushed apart, no spikes
const BALL_R = .6;
const BALL_FACES = (() => {
  const faces = polyFaces(facetPlanes(revSupport(z => Math.sqrt(Math.max(0, BALL_R * BALL_R - z * z)), -BALL_R, BALL_R, 'z'), {axis: 'z', el: [-45, -22.5, 0, 22.5, 45, 67.5, 90],
    extra: [{n: [0, 0, -1], h: .42, az: 0, el: -90, front: true}]})).filter(f => !f.front);
  return facetBody('de_shellF', faces, {owner: 'destr', paint: destrFacetPx, cls: f => (f.el > 80 ? 2 : f.el < -40 ? 1 : 0), tint: true, ppb: 48, maxPx: 32,
    split: f => (f.c[0] > .01 ? 'p' : f.c[0] < -.01 ? 'n' : 'z')});
})();
const HUSK_DX = .12;
function destrShell(husk, half = 0) {
  const G = BALL_FACES, T = v => (half ? rotA('z', -45, v) : v);
  if (husk) return [...shift(G.p[half], T([HUSK_DX, 0, 0])), ...shift(G.n[half], T([-HUSK_DX, 0, 0]))];
  const els = [...G.p[half], ...G.n[half], ...(G.z ? G.z[half] : [])];
  if (half) return els;
  els.push(...tint(annulus('z', [0, 0, 0], -.425, .35, .45, '-', 'de_rim', {n: 16, stagger: .002})));
  // 13 cone spikes on the axis-aligned and 45-degree directions (none on the open front)
  const S = (dir, rot) => tint(spike('de_spike', dir.map(x => x * .5), dir, .5, .24, rot));
  els.push(...S([0, 1, 0]), ...S([0, -1, 0]), ...S([1, 0, 0]), ...S([-1, 0, 0]), ...S([0, 0, 1]));
  for (const [dir, rot] of [[[0, 1, 0], ['x', 45]], [[0, -1, 0], ['x', -45]], [[0, 1, 0], ['z', 45]], [[0, 1, 0], ['z', -45]], [[0, -1, 0], ['z', 45]], [[0, -1, 0], ['z', -45]], [[1, 0, 0], ['y', -45]], [[-1, 0, 0], ['y', 45]]])
    els.push(...S(dir, rot));
  return els;
}
function destrFace() {
  return [cardZ('de_face', -.39, {X0: -.39, X1: .39, Y0: -.39, Y1: .39}), ...glowBall([0, 0, -.4], .1, 'de_beak')];
}

// ================================================================================================================
// 포식성 predatory: body looks fish / fish_flare / bud / pod / face; the jaw bowl, the tail fin, the core (children)
// ================================================================================================================
// the fish hood: a leaf-shaped shell, pointed at the snout (-Z) and toward the tail, widest a little before the middle,
// a high rounded back and a flat underside where the translucent bowl hangs (profile leaf(s), s = 0 snout .. 1 tail)
const FISH = {z0: -1.25, z1: 1.2, w: .54, top: .6, bot: .12};
const leaf = z => { const s = Math.min(1, Math.max(0, (z - FISH.z0) / (FISH.z1 - FISH.z0))); return s < .42 ? Math.sin(Math.PI / 2 * s / .42) ** 1.4 : Math.sin(Math.PI / 2 * (1 - s) / .58) ** .9; };
const topAt = z => FISH.top * leaf(z) + .02;
// a body of z stations with an elliptic section (x half width, y above / below): sec(z) -> {w, top, bot, y}
const zBodyPts = (z0, z1, sec, th0 = 0, th1 = 2 * Math.PI) => { const P = [];
  for (let i = 0; i <= 40; i++) { const z = z0 + (z1 - z0) * i / 40, q = sec(z); for (let j = 0; j <= 32; j++) { const th = th0 + (th1 - th0) * j / 32, sn = Math.sin(th);
    P.push([q.w * Math.cos(th), (q.y || 0) + (sn >= 0 ? q.top : q.bot) * sn, z]); } }
  return P; };
const yBodyPts = (rings, extra = []) => [...ringPts(rings), ...extra];
const PRED_ELZ = [-67.5, -45, -22.5, 0, 22.5, 45, 67.5];
// (v4 f2070 / f2400 / f1920 / f1956 / f2175) the body's solid parts as facet bodies sharing one opaque sprite: the
// fish hood (round Z), the bud's cream ogive and the pod's lid (round Y), the closed face ball (round Z); the glassy
// parts share one translucent sprite: the jaw bowl (round Z, jaw frame), the bud's star bowl and the pod's lower lobe.
// Diagonal faces ride body_x (turned 45 degrees about Z for the fish / face, about Y for the bud / pod) and jaw_x
const PRED_SOLID = (() => {
  const tag = (fs, part) => fs.map(f => ({...f, part}));
  const fish = tag(polyFaces(facetPlanes(pointSupport(zBodyPts(FISH.z0, FISH.z1, z => { const L = leaf(z); return {w: FISH.w * L + .015, top: FISH.top * L + .015, bot: FISH.bot * L + .015}; })), {axis: 'z', el: PRED_ELZ})), 'fish');
  const budR = y => .76 * Math.cos(Math.PI / 2 * Math.min(1, y / 1.02)) ** .85 + .02;
  const bud = tag(polyFaces(facetPlanes(pointSupport(yBodyPts([0, .2, .4, .58, .74, .87, .97].map(y => [y, budR(y)]), [[0, 1.04, 0]])), {el: [-90, 0, 22.5, 45, 67.5, 90]})).filter(f => f.el > -80), 'bud');
  const sph = (c, R, k, n = 9) => Array.from({length: n + 1}, (_, i) => { const a = -Math.PI / 2 + Math.PI * i / n; return [c + R * k * Math.sin(a), R * Math.cos(a) + .01]; }).filter(([, r]) => r > .02);
  const pod = tag(polyFaces(facetPlanes(pointSupport(yBodyPts(sph(1.02, .72, 1.12), [[0, 1.02 + .81, 0], [0, 1.02 - .81, 0]])), {el: [-90, -67.5, -45, -22.5, 0, 22.5, 45, 67.5, 90]})), 'pod');
  const face = tag(polyFaces(facetPlanes(pointSupport(zBodyPts(-.6, .62, z => { const r = Math.sqrt(Math.max(0, .66 * .66 - (z - .02) ** 2)) + .01; return {w: r, top: r * 1.04, bot: r}; })),
    {axis: 'z', el: [-90, ...PRED_ELZ, 90]})), 'face');
  return facetBody('pr_solidF', [...fish, ...bud, ...pod, ...face], {owner: 'pred', paint: predSolidPx, cls: f => f.part + (f.n[1] < -.2 ? 'u' : '') + f.el, ppb: 23, maxPx: 28, split: f => f.part});
})();
const PRED_GLASS = (() => {
  const tag = (fs, part) => fs.map(f => ({...f, part}));
  // the jaw bowl (jaw frame: the hinge at body z +0.4): the lower half of an ellipsoid under the hood, its flat top hidden
  const jaw = tag(polyFaces(facetPlanes(pointSupport(zBodyPts(FISH.z0 + .04, FISH.z1 - .06, z => { const L = leaf(z); return {w: FISH.w * L * .9 + .02, top: 0, bot: .5 * L + .03}; }, Math.PI, 2 * Math.PI)
    .map(([x, y, z]) => [x, y - .02, z - .4])), {axis: 'z', el: PRED_ELZ})).filter(f => f.n[1] < .3), 'jaw');
  const bowlR = y => .7 * (1 - Math.pow(-y / .95, 1.15)) + .02;
  const bud = tag(polyFaces(facetPlanes(pointSupport(yBodyPts([0, -.2, -.4, -.6, -.78].map(y => [y, bowlR(y)]), [[0, -.97, 0]])), {el: [-90, -67.5, -45, -22.5, 0, 90]})).filter(f => f.el < 80), 'bud');
  const pts = []; for (let i = 0; i <= 10; i++) { const a = -Math.PI / 2 + Math.PI * i / 10, y = -.43 + .87 * Math.sin(a), r = .87 * Math.cos(a) + .01; if (r > .02) pts.push([y, r]); }
  const pod = tag(polyFaces(facetPlanes(pointSupport(yBodyPts(pts, [[0, .44, 0], [0, -1.3, 0]])), {el: [-90, -67.5, -45, -22.5, 0, 22.5, 45, 67.5, 90]})), 'pod');
  return facetBody('pr_glassF', [...jaw, ...bud, ...pod], {owner: 'pred', paint: predGlassPx, cls: f => f.part + f.el, ppb: 20, maxPx: 28, translucent: true, aa: true, split: f => f.part});
})();
function predFish(flare) {
  const els = [...PRED_SOLID.fish[0]];
  for (const [z, big] of [[-.3, 1], [.18, 1], [.62, 0]]) {
    const y = topAt(z) - .08, sp = big ? 'pr_horn' : 'pr_hornS', H = big ? .67 : .36, W = big ? .4 : .24;
    els.push(quad(sp, [-W / 2, y + H - .05, z], [W, 0, 0], [0, -H, 0], {rot: ['x', 22.5, [0, y, z]]}), quad(sp, [0, y + H - .05, z - W / 2], [0, 0, W], [0, -H, 0], {rot: ['x', 22.5, [0, y, z]]}));
  }
  const ew = FISH.w * leaf(-.62) + .04;
  for (const s of [1, -1]) els.push(quad('pr_eye', [s * ew, .27, -.74], [0, 0, .22], [0, -.22, 0]));
  if (flare) {
    for (const [dir, rot] of [[[0, 1, 0]], [[1, 0, 0]], [[-1, 0, 0]], [[0, 1, 0], ['z', 45]], [[0, 1, 0], ['z', -45]], [[0, -1, 0], ['z', 45]], [[0, -1, 0], ['z', -45]]])
      for (const z of [-.55, -.1]) els.push(...spike('pr_flare', [dir[0] * .3, dir[1] * .25, z], dir, .55, .14, rot ? rot : undefined));
  }
  return els;
}
function predJaw() {
  // the translucent bowl under the hood (hinge frame: hinge at body z +0.4), two bottom sepals, the long front fin + gem
  const z0 = -.4, els = [...PRED_GLASS.jaw[0]];
  for (const s of [1, -1]) els.push(quad('pr_sepal', [s * .25 - .07, -.94, -.2 + z0], [.14, 0, 0], [0, .62, 0], {rot: ['z', s * 22.5, [s * .25, -.32, -.2 + z0]]}));
  els.push(quad('pr_fin', [.34, -.12, -.62 + z0], [.24, 0, 0], [0, 0, -1.15], {rot: ['y', -22.5, [.46, -.12, -.62 + z0]]}));
  els.push(abox([.38, -.2, -.72 + z0], [.56, -.04, -.56 + z0], 'pr_gem'));
  return els;
}
const predTail = () => [quad('pr_tail', [0, .5, -.04], [0, 0, .94], [0, -1.0, 0])];
const predCore = () => glowBall([0, 0, 0], .28, 'pr_core');
// the bud (empowered): a diamond 2.1 x 1.6 - a cream ogive of petal facets closing to a point (a short horn on top, four
// petals leaning in), over a translucent green star bowl tapering to the lower point, eight sepals at the rim
function predBud() {
  const els = [...PRED_SOLID.bud[0], ...PRED_GLASS.bud[0]];
  for (let k = 0; k < 4; k++) els.push(tangentCard('pr_petal', k * 90, .7, .82, .82, .84, {tilt: -22.5, pivot: 'bottom'}));
  els.push(...shift(crossCards('pr_horn', [0, 0, 0], .26, .44, {y0: 0}), [0, .9, 0]));
  for (let k = 0; k < 8; k++) els.push(radialCard('pr_sepal', k * 45 + 22.5, .45, 1.02, -.42, .06));
  return els;
}
// the pod (inflated, 3.5 b): a tall double-lobed clam - the round translucent lower lobe holding the core, the cream lid
// lobe closed on top of it at a waist (centre frame: the floor at y -1.3)
function predPod() {
  return [...PRED_GLASS.pod[0], ...PRED_SOLID.pod[0], ...shift(crossCards('pr_horn', [0, 0, 0], .3, .5, {y0: 0}), [0, 1.8, 0])];
}
function predFace() {
  const els = [...PRED_SOLID.face[0]];
  els.push(...crossCards('pr_horn', [0, .66, -.1], .34, .6, {y0: 0}));
  els.push(abox([-.13, -.5, -.63], [.13, -.24, -.55], 'pr_gem', {rot: ['z', 45, [0, -.37, -.59]]}));
  els.push(quad('pr_eye', [-.1, .1, -.62], [.2, 0, 0], [0, -.2, 0]));
  return els;
}
const predBodyX = look => (look === 'bud' ? [...PRED_SOLID.bud[1], ...PRED_GLASS.bud[1]] : look === 'pod' ? [...PRED_GLASS.pod[1], ...PRED_SOLID.pod[1]] : look === 'face' ? PRED_SOLID.face[1] : PRED_SOLID.fish[1]);

// ================================================================================================================
// the Heart of the Oasis: lemon bulb (looks by tint), root cradle (pedestal / full), two root arms, glow tips, vine
// hand (idle / wrap) and four vine stem segments
// ================================================================================================================
// the bulb (v3 f270 / v4 f1650 / sheet 08): a translucent glowing lemon lying along Z, 3.2 x 2.6 x 2.3, a facet body
// round a lumpy lemon point cloud (pointed ends, soft lobes): 8 azimuths x the 22.5 elevations; the faces facing the
// upper left carry the white specular band (cls 1-3), every facet edge a soft darker rib line; grey values tinted per
// look. The diagonal faces ride heart_bulb_x (the bulb turned 45 degrees about its Y). Three crossed swirl cards inside.
const LEMON = {L: 1.6, W: 1.3, H: 1.15};
const lemonF = a => { const t = Math.min(1, Math.abs(a) / LEMON.L); return Math.pow(Math.max(0, 1 - t * t), .6) * (1 - .45 * Math.pow(t, 6)); };
const LEMON_PTS = (() => { const P = [];
  for (let i = 0; i <= 64; i++) { const z = -LEMON.L + 2 * LEMON.L * i / 64, f = lemonF(z);
    for (let j = 0; j < 48; j++) { const th = j * 2 * Math.PI / 48, lump = 1 + .045 * Math.sin(3 * th + 1.1 * z) + .03 * Math.cos(2 * th - .9 * z + .4);
      P.push([LEMON.W * f * lump * Math.cos(th), LEMON.H * f * lump * Math.sin(th) * (Math.sin(th) < 0 ? .93 : 1), z]); } }
  return P; })();
const SPEC = (() => { const v = [-.5, .8, -.35], l = Math.hypot(...v); return v.map(x => x / l); })();
const BULB_FACES = facetBody('he_bulbF', polyFaces(facetPlanes(pointSupport(LEMON_PTS), {el: [-90, -67.5, -45, -22.5, 0, 22.5, 45, 67.5, 90]})),
  {owner: 'heart', paint: bulbFacetPx, tint: true, translucent: true, aa: true, ppb: 23, maxPx: 40,
    cls: f => { const k = f.n[0] * SPEC[0] + f.n[1] * SPEC[1] + f.n[2] * SPEC[2]; return k > .86 ? 3 : k > .66 ? 2 : k > .42 ? 1 : 0; }});
function heartBulb() {
  const els = [...BULB_FACES[0]];
  els.push(...tint([cardZ('he_swirl', 0, {X0: -.8, X1: .8, Y0: -.75, Y1: .75}), cardX('he_swirl', 0, {Z0: -1.0, Z1: 1.0, Y0: -.7, Y1: .7}), cardY('he_swirl', 0, {X0: -.8, X1: .8, Z0: -1.0, Z1: 1.0})]));
  return els;
}
const heartBulbX = () => [...BULB_FACES[1]];
// the cradle (v3 f0 / f270, v4 f1650): a low dark mound and six root fingers - each rises from a foot splayed into the
// turf (r 2.2-2.6), thickest at its knee beside the bulb's lower flank, and climbs the flank to grip it; three shapes,
// each also mirrored to the other side (planes through the bulb axis, offset so no two coincide); two short roots at the
// lemon's ends. pedestal adds pale petal clumps + gold sprouts (v2 f2340). Root limbs: rootLimb (boxes + skin card).
const fingerR = r0 => t => .05 + (r0 - .05) * Math.sin(Math.PI * Math.min(1, .18 + t * .95)) ** .7 * (1 - .55 * t);
const FINGER_SHAPES = [
  // [2D points (x outward, y up), half width (t), plane offset, mirrored-copy offset]
  [[[2.55, -.04], [2.15, .12], [1.72, .42], [1.5, .92], [1.47, 1.45], [1.36, 1.98], [1.1, 2.38]], fingerR(.2), .38, -.62],
  [[[2.3, -.04], [1.95, .2], [1.66, .55], [1.52, 1.05], [1.42, 1.6], [1.2, 2.05]], fingerR(.18), -.66, .5],
  [[[2.05, -.04], [1.8, .1], [1.55, .36], [1.44, .78], [1.38, 1.2]], fingerR(.16), .02, -.1],
];
const END_ROOT = [[[2.62, -.04], [2.2, .14], [1.84, .44], [1.68, .82], [1.7, 1.22]], fingerR(.17)];
// (the root limbs register their skin sprites: built once at load, before the sprites are painted)
const CRADLE_ROOTS = (() => { const els = [];
  FINGER_SHAPES.forEach(([pts, r, c1, c2], i) => {
    const one = rootLimb('he_skF' + i, 'xy', 0, pts, r, {R: PAL.root, ppb: 14});
    els.push(...shift(one, [0, 0, c1]), ...shift(mirrorX(one), [0, 0, c2]));
  });
  const end = rootLimb('he_skE', 'yz', 0, END_ROOT[0], END_ROOT[1], {R: PAL.root, ppb: 14});
  els.push(...shift(end, [-.42, 0, 0]), ...shift(mirrorZ(end), [.36, 0, 0]));
  return els; })();
function heartCradle(pedestal) {
  const els = [...loft('y', [{a: 0, r: 1.15}, {a: .22, r: 1.02}, {a: .4, r: .8}, {a: .54, r: .42}], {n: 16, tex: 'he_rootS', ledgeTex: 'he_root_l', caps: '+', seed: 43}), ...CRADLE_ROOTS];
  if (pedestal) {
    for (let k = 0; k < 6; k++) { const a = (k * 60 + 15) * D2R; els.push(...crossCards('he_petal', [Math.sin(a) * .9, .42, -Math.cos(a) * .9], .56, .34, {y0: 0})); }
    for (const a of [20, 140, 260]) els.push(...crossCards('he_sprout', [Math.sin(a * D2R) * .45, .5, -Math.cos(a * D2R) * .45], .24, .7, {y0: 0}));
  }
  return els;
}
// the two tall root arms (v4 f1650 / v3 f270): rising beside the bulb's flanks, bowing out, then curling over its top
// toward the middle (one shape, mirrored, offset in z), two shorter roots beside the lemon's ends; the glow tips
// (heart_tips) sit on their ends (ARM_TIPS)
const ARM = [[[1.62, -.05], [1.9, .8], [2.04, 1.7], [1.95, 2.6], [1.62, 3.38], [1.1, 3.92], [.5, 4.18], [.04, 4.1], [-.2, 3.86]], t => .07 + .25 * Math.pow(1 - t, 1.3)];
// the second arm: lower (3.6 b), its tip curling back outward over the bulb's shoulder
const ARM2 = [[[1.55, -.05], [1.86, .75], [1.98, 1.6], [1.86, 2.45], [1.52, 3.12], [1.08, 3.52], [.72, 3.6], [.56, 3.4], [.66, 3.2]], t => .065 + .22 * Math.pow(1 - t, 1.3)];
const SIDE = [[[.12, 1.62], [.5, 1.98], [1.0, 2.2], [1.55, 2.2], [2.05, 2.0], [2.45, 1.68]].map(([y, z]) => [z, y]), t => .06 + .13 * Math.pow(1 - t, 1.2)];
const ARM_SET = [['xy', .28, false], ['xy', -.42, true], ['yz', .32, false], ['yz', -.5, true]];
const ARM_ELS = (() => { const arm = rootLimb('he_skA', 'xy', 0, ARM[0], ARM[1], {R: PAL.root, ppb: 13}), arm2 = rootLimb('he_skA2', 'xy', 0, ARM2[0], ARM2[1], {R: PAL.root, ppb: 13});
  const side = rootLimb('he_skS', 'yz', 0, SIDE[0], SIDE[1], {R: PAL.root, ppb: 13});
  return [...shift(arm, [0, 0, .28]), ...shift(mirrorX(arm2), [0, 0, -.42]), ...shift(side, [.32, 0, 0]), ...shift(mirrorZ(side), [-.5, 0, 0])]; })();
const heartArms = () => ARM_ELS;
// the arm tip points (object frame): the tall arms' ends, half way up, and the side roots' ends
const ARM_TIPS = (() => { const e = ARM[0][ARM[0].length - 1], m = ARM[0][5], e2 = ARM2[0][ARM2[0].length - 1], m2 = ARM2[0][4], se = SIDE[0][SIDE[0].length - 1];
  return {main: [[e[0], e[1], .28], [-e2[0], e2[1], -.42]], mid: [[m[0], m[1], .28], [-m2[0], m2[1], -.42]], side: [[.32, se[1], se[0]], [-.5, se[1], -se[0]]]}; })();
function heartTips() {
  const els = [];
  for (const p of ARM_TIPS.main) els.push(...crossCards('he_tip', [p[0], p[1] + .02, p[2]], .38, .74, {y0: 0}));
  for (const p of ARM_TIPS.mid) els.push(...crossCards('he_tip', [p[0], p[1] + .08, p[2]], .28, .52, {y0: 0}));
  for (const p of ARM_TIPS.side) els.push(...crossCards('he_tip', [p[0], p[1] + .02, p[2]], .26, .5, {y0: 0}));
  // small flames on the gripping fingers' tips
  for (const [pts, , c1, c2] of FINGER_SHAPES.slice(0, 2)) { const e = pts[pts.length - 1]; els.push(...crossCards('he_tip', [e[0], e[1], c1], .18, .36, {y0: 0}), ...crossCards('he_tip', [-e[0], e[1], c2], .18, .36, {y0: 0})); }
  return els;
}
// the vine hand (joint = the wrist just above the upright egg's top): six vine fingers hugging the egg (half axes .91 x
// 1.12 at pose scale 0.7, its centre 1.24 below the wrist) from the crown over the shoulder to below the equator, the
// tips curling in; wrap = the grip closed tighter and further down
function vineHand(wrap) {
  const els = [rockBox([-.12, -.1, -.12], [.12, .18, .12], 'he_vineS', {seed: 3})];
  const A = .97, B = 1.18, C = -1.24, phiEnd = wrap ? 2.3 : 1.9;
  // a sage-green tendril from the wrist over the egg's crown and shoulder to the flank, its tip flicking out (v2 f2200)
  const finger = (k, off, sgn, plane) => {
    const pts = [[0, 0]];
    for (let i = 1; i <= 5; i++) { const ph = .1 + (phiEnd - .1) * i / 5; pts.push([sgn * A * Math.sin(ph) * (1 + .03 * k), C + B * Math.cos(ph)]); }
    const e = pts[pts.length - 1], ph = phiEnd + (wrap ? .25 : .4);
    pts.push([sgn * (A * Math.sin(ph) + (wrap ? .02 : .16)), C + B * Math.cos(ph) - .06]);
    return rootLimb(null, plane, off, pts, t => .085 - .05 * t, {side: 'he_vineS', k: .9, sub: 2, end: true});
  };
  els.push(...finger(0, .12, 1, 'xy'), ...finger(1, -.3, 1, 'xy'), ...finger(2, .3, -1, 'xy'), ...finger(3, -.12, -1, 'xy'), ...finger(4, .22, 1, 'yz'), ...finger(5, -.16, -1, 'yz'));
  return els;
}
const vineStem = () => [quad('he_stem', [-.3, .1, 0], [.6, 0, 0], [0, -6.3, 0]), quad('he_stem', [0, .1, -.3], [0, 0, .6], [0, -6.3, 0]), abox([-.07, -6.2, -.07], [.07, .05, .07], 'he_vineS')];

// ================================================================================================================
// domes, wall blade, stalks, seed
// ================================================================================================================
// the dome (v5 f1590, w1 f184 / f330): a translucent lime hemisphere r 4.45 as a facet body of 16 azimuths x elevations
// 0 / 22.5 / 45 / 67.5 + the top, every face a two-sided card (seen from inside too) painted with the light leaf
// sprigs rising from the base; the tilted faces ride three more displays turned 22.5 / 45 / 67.5 degrees (dome_decor is
// the 45 one and also carries the bright base rim and the sprout on top)
const DOME_R = 4.45, DOME_TURNS = [0, 22.5, 45, 67.5];
const DOME_FACES = (() => {
  const az = Array.from({length: 16}, (_, k) => k * 22.5);
  const faces = polyFaces([...facetPlanes(revSupport(y => Math.sqrt(Math.max(0, DOME_R * DOME_R - y * y)), 0, DOME_R), {az, el: [0, 22.5, 45, 67.5, 90]}), {n: [0, -1, 0], h: 0, az: 0, el: -90, hidden: true}]).filter(f => !f.hidden);
  return facetBody('do_shellF', faces, {owner: 'dome', paint: domeFacetPx, translucent: true, aa: true, ppb: 17, maxPx: 64, turns: DOME_TURNS, vertMain: true,
    cls: f => (Math.abs(f.el) > 89 ? 0 : Math.round(f.az / 22.5) % 3)});
})();
const domeShell = () => DOME_FACES[0];
function domeDecor() {
  const els = [...DOME_FACES[2]];
  els.push(...band([0, 0, 0], DOME_R + .03, 0, .26, 'do_rim'));
  els.push(...crossCards('do_sprout', [0, DOME_R - .12, 0], .5, .58, {y0: 0}));
  return els;
}
function wallBlade() {
  // a cupped leaf: three strips up to 2.0 b (the side ones turned 22.5 degrees back), the tip above it one strip leaning
  // out 22.5 degrees (the leaf's top curling over)
  const R = SH.wa_blade.rect, W = R.u1 - R.u0, H = R.v1 - R.v0, w3 = W / 3, h1 = 2.0, vb = (H - h1) / H;
  return [quad('wa_blade', [-w3 / 2, h1, 0], [w3, 0, 0], [0, -h1, 0], {uvr: [1 / 3, vb, 2 / 3, 1]}),
    quad('wa_blade', [w3 / 2, h1, 0], [w3, 0, 0], [0, -h1, 0], {uvr: [2 / 3, vb, 1, 1], rot: ['y', -22.5, [w3 / 2, 0, 0]]}),
    quad('wa_blade', [-w3 * 1.5, h1, 0], [w3, 0, 0], [0, -h1, 0], {uvr: [0, vb, 1 / 3, 1], rot: ['y', 22.5, [-w3 / 2, 0, 0]]}),
    quad('wa_blade', [-W / 2, H + .02, 0], [W, 0, 0], [0, -(H - h1) - .04, 0], {uvr: [0, 0, 1, vb + .014], rot: ['x', 22.5, [0, h1, 0]]})];
}
// the 생명의 손 stalk (v1 f1320 / f1344): a pale flattened shell blade ~1 b wide rising from the ground and bending
// forward (-Z) into a scythe-like hook, in three segments (the slam bends them at the joints): root limbs in the Y-Z
// plane (boxes + skin card, the blade 1.6x wider than thick) with a dark slate back edge and veins (stalkSkin)
const STALK = {
  low: [[[.02, -.4], [.08, .4], [.12, 1.2], [.07, 2.0], [-.02, 2.72]], t => .58 - .13 * t],
  high: [[[0, -.06], [-.04, .65], [-.16, 1.3], [-.36, 1.85], [-.52, 2.12]], t => .44 - .1 * t],
  tip: [[[0, -.04], [.02, .45], [-.06, .9], [-.28, 1.24], [-.55, 1.26], [-.7, 1.08], [-.72, .9]], t => .34 * (1 - .82 * t) + .02],
};
const stalkLimb = (key, ppb) => rootLimb('st_sk_' + key, 'yz', 0, STALK[key][0], STALK[key][1], {side: 'st_sideS', k: .78, sub: 3, ppb, owner: 'stalk', R: PAL.stalk, style: stalkSkin, end: key === 'tip', skinAt: 'faces', skin: 1.04, kin: .96});
const STALK_ELS = {low: stalkLimb('low', 15), high: stalkLimb('high', 15), tip: stalkLimb('tip', 20)};
const stalkLow = () => STALK_ELS.low;
const stalkHigh = () => STALK_ELS.high;
const stalkTip = () => [...STALK_ELS.tip, ...spike('st_cone', [0, 1.2, -.42], [0, 1, 0], .3, .16, ['x', 45])];
const seedModel = () => [...crossCards('se_seed', [0, .17, 0], .26, .34, {y0: -.17, three: true}), quad('se_seed', [-.13, .02, .17], [.26, 0, 0], [0, 0, -.34])];

// ================================================================================================================
// the structure
// ================================================================================================================
// display: {name, scale, pivot, joint [x,y,z] (rest, in the parent frame), parent, frame ('object' | 'joint'), bright,
//   looks {look: item}, def, overlay, models {model: () => elements}, cull [w, h] (fixed objects), note}
const D = (name, o) => ({name, parent: null, frame: 'joint', overlay: false, bright: 14, scale: 1, pivot: 'feet', joint: [0, 0, 0], ...o});
// the twin of a facet-body display: the body's diagonal faces on a display that copies `par` (its clip transform, scale
// and look) turned by rot in par's frame; model / item names: the parent's item with `key` inserted (heart_bulb_idle ->
// heart_bulbx_idle), the same tints. Its parent's clip scales must commute with the turn (the builder checks).
function twin(par, name, rot, model, build, o = {}) {
  const looks = {}, items = {}, models = {[model]: build};
  for (const [look, item] of Object.entries(par.looks)) {
    const it = name + '_' + look;
    looks[look] = it;
    const pi = par.items && par.items[item];
    items[it] = [model, pi ? pi[1] : null];
  }
  return D(name, {pivot: par.pivot, frame: par.frame, parent: par.name, joint: [0, 0, 0], scale: par.scale, bright: par.bright, follow: () => rot, lookOf: par.name,
    looks, def: par.def, models, items, twinOf: par.name, note: `the diagonal facets of ${par.name} (${par.name} turned ${rot.find(x => x)} degrees)`, ...o});
}
const DOME_SHELL = D('dome_shell', {idxs: [0x10, 0x12, 0x14], pivot: 'feet', frame: 'object', scale: 3.3, looks: {idle: 'dome_shell_idle'}, def: 'idle', models: {dome_shell_idle: domeShell}, note: 'translucent facet hemisphere r 4.45 (alpha <= 0.35, two-sided); its tilted faces at 22.5 / 45 / 67.5 degrees on dome_shell_b / dome_decor / dome_shell_c'});
const HEART_BULB = D('heart_bulb', {idx: 0x00, pivot: 'centre', joint: [0, 1.6, 0], scale: 1.2, bright: 15, looks: {idle: 'heart_bulb_idle', egg_gold: 'heart_bulb_egg_gold', egg_green: 'heart_bulb_egg_green', withered: 'heart_bulb_withered', blaze: 'heart_bulb_blaze'}, def: 'idle',
  models: {heart_bulb_m: heartBulb}, items: {heart_bulb_idle: ['heart_bulb_m', 0xDCEB5C], heart_bulb_egg_gold: ['heart_bulb_m', 0xF5CF4A], heart_bulb_egg_green: ['heart_bulb_m', 0xA8D850],
    heart_bulb_withered: ['heart_bulb_m', 0x8A8258], heart_bulb_blaze: ['heart_bulb_m', 0xFFFCD8]},
  note: 'translucent lemon seed 3.2 x 2.6 x 2.3 (a facet body; its diagonal faces on heart_bulb_x), alpha ~0.86; the arrival egg = this model at scale 0.7, pitch 90 (upright)'});
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
        return D(nm, {pivot: 'feet', frame: 'object', parent: 'bulb', follow: () => rot, lookOf: 'bulb', twinOf: 'bulb',
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
      D('stalk', {pivot: 'feet', frame: 'object', scale: 1.6, looks: {idle: 'nurt_stalk_idle'}, def: 'idle', models: {nurt_stalk_idle: nurtStalk}, note: 'S-curved twisting slate-teal ribbon with white rims (atlas panels), pale fronds on the ground'}),
      D('cap', {pivot: 'centre', joint: [0, 2.18, .06], looks: {idle: 'nurt_cap_idle', tilt: 'nurt_cap_tilt'}, def: 'idle', models: {nurt_cap_idle: () => nurtCap('idle'), nurt_cap_tilt: () => nurtCap('tilt')},
        note: 'cream bonnet hood (a facet body cut open underneath, the tulip tip in front) + the gold shard; tilt = the opening lifted toward the targets'}),
      // the hood's diagonal facets (the cap turned 45 degrees about its Y)
      D('cap_x', {pivot: 'centre', parent: 'cap', follow: () => [0, 45, 0], lookOf: 'cap', twinOf: 'cap', looks: {idle: 'nurt_capx_idle', tilt: 'nurt_capx_tilt'}, def: 'idle',
        models: {nurt_capx_idle: () => nurtCapX('idle'), nurt_capx_tilt: () => nurtCapX('tilt')}, note: 'the diagonal facets of cap (cap turned 45 degrees)'}),
      D('orb', {pivot: 'centre', joint: [0, 2.06, -.4], bright: 15, looks: {on: 'nurt_orb_on'}, def: 'on', models: {nurt_orb_on: nurtOrb}, note: 'pulse'}),
      D('ring', {pivot: 'feet', frame: 'object', overlay: true, looks: {on: 'nurt_ring_on'}, def: 'on', models: {nurt_ring_on: nurtRing}, note: 'translucent cylinder r 1.3, h 0.5, only while immune (om/nurt/ring/on|off)'}),
    ]},
  guard: {type: 'kind', id: 3, name: '수호', hover: 0, hp_bar_y: 3.0, shield: {w: 1.4, h: 3.0}, size: {h: 4.4, bud: 2.0, orb_d: 0.4},
    displays: [
      D('spire', {pivot: 'mid', frame: 'object', scale: 1.75, joint: [0, 2.2, 0], looks: {spire: 'guard_spire_spire', bud: 'guard_spire_bud', wisp: 'guard_spire_wisp'}, def: 'spire',
        models: {guard_spire_spire: guardSpire, guard_spire_bud: guardBud, guard_spire_wisp: guardWisp},
        note: 'facet-body teal sheath with grey-blue scale lobes and a gold crystal, two pale helix ribbons to 4.4 / 4.1 b; bud = teal ogive hood over a pale flared drape; wisp = the black death wisp'}),
      // the diagonal facets of the sheath / hood / drape (the spire turned 45 degrees about its Y; empty in the wisp look)
      D('spire_x', {pivot: 'mid', frame: 'object', parent: 'spire', scale: 1.75, follow: () => [0, 45, 0], lookOf: 'spire', twinOf: 'spire',
        looks: {spire: 'guard_spirex_spire', bud: 'guard_spirex_bud', wisp: 'guard_spirex_wisp'}, def: 'spire',
        models: {guard_spirex_spire: guardSpireX, guard_spirex_bud: guardBudX, guard_spirex_wisp: () => []}, note: 'the diagonal facets of spire (spire turned 45 degrees; empty in the wisp look)'}),
      D('orb', {pivot: 'mid', joint: [0, 5.05, 0], bright: 15, looks: {on: 'guard_orb_on'}, def: 'on', models: {guard_orb_on: guardOrb}, note: 'bobs 0.6-0.8 above the tip'}),
    ]},
  nest: {type: 'kind', id: 4, name: '둥지', hover: 1.0, hp_bar_y: 2.75, shield: {w: 1.6, h: 2.2}, size: {w: 2.2, h: 1.3},
    displays: [
      D('cap', {pivot: 'centre', joint: [0, 1.3, 0], looks: {idle: 'nest_cap_idle'}, def: 'idle', models: {nest_cap_idle: nestCap}, note: 'facet-body onion cap with a long spire, the keyhole outline, the orb eye (painted emissive) in its pale ring, the gold drop'}),
      D('cap_x', {pivot: 'centre', parent: 'cap', follow: () => [0, 45, 0], lookOf: 'cap', twinOf: 'cap', looks: {idle: 'nest_capx_idle'}, def: 'idle', models: {nest_capx_idle: nestCapX}, note: 'the diagonal facets of cap (cap turned 45 degrees)'}),
      D('wing_l', {pivot: 'centre', parent: 'cap', joint: [.17, .02, .02], looks: {idle: 'nest_wing_l_idle'}, def: 'idle', models: {nest_wing_l_idle: nestWing}}),
      D('wing_r', {pivot: 'centre', parent: 'cap', joint: [-.17, .02, .02], looks: {idle: 'nest_wing_r_idle'}, def: 'idle', models: {nest_wing_r_idle: () => mirrorX(nestWing())}}),
    ]},
  destr: {type: 'kind', id: 5, name: '파괴', hover: 0, hp_bar_y: 1.75, shield: {w: 1.3, h: 1.3}, size: {d: 1.2, spikes: 0.2, beak: 0.4},
    displays: [
      D('shell', {pivot: 'centre', joint: [0, .62, 0], spinAxis: 'x', looks: {normal: 'destr_shell_normal', husk: 'destr_shell_husk'}, def: 'normal',
        models: {destr_shell_m_normal: () => destrShell(false), destr_shell_m_husk: () => destrShell(true)}, items: {destr_shell_normal: ['destr_shell_m_normal', 0xFFFFFF], destr_shell_husk: ['destr_shell_m_husk', 0x3A3833]},
        note: 'facet-body armour ball r 0.6 open in front, pale rim, 13 cone spikes; husk = the shell split along X (tinted black)'}),
      D('shell_x', {pivot: 'centre', parent: 'shell', follow: () => [0, 0, 45], lookOf: 'shell', twinOf: 'shell', looks: {normal: 'destr_shellx_normal', husk: 'destr_shellx_husk'}, def: 'normal',
        models: {destr_shellx_m_normal: () => destrShell(false, 1), destr_shellx_m_husk: () => destrShell(true, 1)}, items: {destr_shellx_normal: ['destr_shellx_m_normal', 0xFFFFFF], destr_shellx_husk: ['destr_shellx_m_husk', 0x3A3833]},
        note: 'the diagonal facets of shell (shell rolled 45 degrees about its Z)'}),
      D('face', {pivot: 'centre', joint: [0, .62, 0], spinAxis: 'x', bright: 15, looks: {on: 'destr_face_on'}, def: 'on', models: {destr_face_on: destrFace}, note: 'pulse scale'}),
    ]},
  pred: {type: 'kind', id: 6, name: '포식성', hover: 1.2, hp_bar_y: 2.75, shield: {w: 1.6, h: 1.6}, size: {fish: [2.5, 1.3], bud: [2.1, 1.6], pod: [3.5, 1.8]},
    displays: [
      D('body', {pivot: 'centre', joint: [0, 1.3, 0], scale: 1.6, looks: {fish: 'pred_body_fish', fish_flare: 'pred_body_fish_flare', bud: 'pred_body_bud', pod: 'pred_body_pod', face: 'pred_body_face'}, def: 'fish',
        models: {pred_body_fish: () => predFish(false), pred_body_fish_flare: () => predFish(true), pred_body_bud: predBud, pred_body_pod: predPod, pred_body_face: predFace},
        note: 'fish = the leaf-shark hood; bud / pod / face are their own models (jaw and fin hidden)'}),
      // the diagonal facets of body (turned 45 degrees about its Z for the fish / face, about its Y for the bud / pod)
      D('body_x', {pivot: 'centre', parent: 'body', scale: 1.6, follow: look => (look === 'bud' || look === 'pod' ? [0, 45, 0] : [0, 0, 45]), lookOf: 'body', twinOf: 'body',
        looks: Object.fromEntries(['fish', 'fish_flare', 'bud', 'pod', 'face'].map(l => [l, 'pred_bodyx_' + l])), def: 'fish',
        models: Object.fromEntries(['fish', 'fish_flare', 'bud', 'pod', 'face'].map(l => ['pred_bodyx_' + l, () => predBodyX(l)])), note: 'the diagonal facets of body'}),
      D('jaw', {pivot: 'centre', parent: 'body', joint: [0, -.02, .4], scale: 1.6, looks: {idle: 'pred_jaw_idle'}, def: 'idle', models: {pred_jaw_idle: predJaw}, note: 'the translucent bowl, sepals and the long front fin; hinge behind the middle'}),
      D('jaw_x', {pivot: 'centre', parent: 'jaw', scale: 1.6, follow: () => [0, 0, 45], lookOf: 'jaw', twinOf: 'jaw', looks: {idle: 'pred_jawx_idle'}, def: 'idle', models: {pred_jawx_idle: () => PRED_GLASS.jaw[1]}, note: 'the diagonal facets of the jaw bowl'}),
      D('fin', {pivot: 'centre', parent: 'body', joint: [0, .02, 1.12], looks: {idle: 'pred_fin_idle'}, def: 'idle', models: {pred_fin_idle: predTail}, note: 'the tail fin; yaw +-25 in pred_swim'}),
      D('core', {pivot: 'centre', parent: 'body', joint: [0, -.08, -.2], bright: 15, looks: {on: 'pred_core_on'}, def: 'on', models: {pred_core_on: predCore}}),
    ]},
  heart: {type: 'object', kind: 'single', tag: 'rlk_mb_ap_heart', cull: [9, 30],
    displays: [
      HEART_BULB,
      twin(HEART_BULB, 'heart_bulb_x', [0, 45, 0], 'heart_bulbx_m', heartBulbX, {idx: 0x09}),
      D('heart_cradle', {idx: 0x01, pivot: 'mid', frame: 'object', joint: [0, .9, 0], scale: 2.2, looks: {pedestal: 'heart_cradle_pedestal', full: 'heart_cradle_full'}, def: 'pedestal',
        models: {heart_cradle_pedestal: () => heartCradle(true), heart_cradle_full: () => heartCradle(false)}, note: '5 knobbly root fingers + the mound; pedestal adds pale petal clumps + 3 gold sprouts'}),
      D('heart_arms', {idx: 0x02, pivot: 'mid', frame: 'object', joint: [0, 2.1, 0], scale: 2.2, looks: {idle: 'heart_arms_idle'}, def: 'idle', models: {heart_arms_idle: heartArms}, note: 'two root arms curling over the bulb to 4.0-4.3 b'}),
      D('heart_tips', {idx: 0x03, pivot: 'mid', frame: 'object', joint: [0, 2.1, 0], scale: 2.2, bright: 15, looks: {idle: 'heart_tips_idle'}, def: 'idle', models: {heart_tips_idle: heartTips}, note: 'leaf-flame sprouts, swaying'}),
      D('vine_hand', {idx: 0x04, pivot: 'centre', joint: [0, 11.2, 0], scale: 1.8, looks: {idle: 'vine_hand_idle', wrap: 'vine_hand_wrap'}, def: 'idle', models: {vine_hand_idle: () => vineHand(false), vine_hand_wrap: () => vineHand(true)}}),
      ...[0, 1, 2, 3].map(k => D('vine_stem_' + k, {idx: 0x05 + k, pivot: 'centre', joint: [0, 26, 0], scale: 4.4, looks: {idle: 'heart_vine_stem'}, def: 'idle', models: k ? {} : {heart_vine_stem: vineStem}, note: 'stretched along its length between the canopy rim and the hand'})),
    ]},
  dome: {type: 'object', kind: 'fixed_set', count: 3, radius: 4.5, tag: 'rlk_mb_ap_dome', cull: [10, 5],
    displays: [
      DOME_SHELL,
      twin(DOME_SHELL, 'dome_decor', [0, 45, 0], 'dome_decor_idle', domeDecor, {idxs: [0x11, 0x13, 0x15], looks: {idle: 'dome_decor_idle'}, items: {}, note: 'the shell faces turned 45 degrees + the bright base rim and the sprout on top (the shell turned 45 degrees)'}),
      twin(DOME_SHELL, 'dome_shell_b', [0, 22.5, 0], 'dome_shellb_idle', () => DOME_FACES[1], {idxs: [0x16, 0x17, 0x18], looks: {idle: 'dome_shellb_idle'}, items: {}}),
      twin(DOME_SHELL, 'dome_shell_c', [0, 67.5, 0], 'dome_shellc_idle', () => DOME_FACES[3], {idxs: [0x19, 0x1A, 0x1B], looks: {idle: 'dome_shellc_idle'}, items: {}}),
    ]},
  wall: {type: 'object', kind: 'multi', max: 15, tag: 'rlk_mb_ap_wall', cull: [2, 3.2], blocks: {block: 'minecraft:barrier', y: [201, 202], place: 'replace air'},
    displays: [D('wall_blade', {pivot: 'feet', frame: 'object', scale: 2.0, looks: {idle: 'wall_blade_idle'}, def: 'idle', models: {wall_blade_idle: wallBlade}, note: 'translucent yellow-green blade 0.9 x 2.86, midrib, two windows'})]},
  stalk: {type: 'object', kind: 'fixed_set', count: 4, height: [5.5, 6.0], tag: 'rlk_mb_ap_stalk', cull: [14, 7],
    displays: [
      D('stalk_low', {idxs: [0x20, 0x23, 0x26, 0x29], pivot: 'feet', joint: [0, 0, 0], scale: 2.3, bright: 13, looks: {idle: 'stalk_low_idle'}, def: 'idle', models: {stalk_low_idle: stalkLow}}),
      D('stalk_high', {idxs: [0x21, 0x24, 0x27, 0x2A], pivot: 'feet', parent: 'stalk_low', joint: [0, 2.62, 0], scale: 1.8, bright: 13, looks: {idle: 'stalk_high_idle'}, def: 'idle', models: {stalk_high_idle: stalkHigh}}),
      D('stalk_tip', {idxs: [0x22, 0x25, 0x28, 0x2B], pivot: 'feet', parent: 'stalk_high', joint: [0, 2.02, 0], scale: 1.25, looks: {idle: 'stalk_tip_idle'}, def: 'idle', models: {stalk_tip_idle: stalkTip}, note: 'hooked tip + small gold cone'}),
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
