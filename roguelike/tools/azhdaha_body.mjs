// BODY region of the 야타용왕 (Azhdaha) rig: torso (chest, belly, pelvis), the neck, the chest apron (+ its glow
// overlay), the four dorsal plate groups and the three gold crystal groups (model.md §3.2-§3.6).
//
// Region interface (the same in azhdaha_{head,body,legs,tail}.mjs; aggregated by azhdaha_geometry / azhdaha_paint):
//   PARTS      [part, default item model, block brightness] owned by this region (pose: azhdaha_pose.mjs solve())
//   models()   {model: elements (model units)}: the default models, every look variant, the overlays
//   sprites()  {sprite: [w, h, painter (s, t in 0..1) -> rgba, translucent]}: this region's own sprites
//   LOOKS      {legs|tail: {part: {look: item model}}}: the element looks this region answers (model.md §4.2)
//   TINTED     {item: [model, rgb]}: extra item definitions = a model with a constant tint (glow overlays)
// Geometry is authored in blocks in each part's frame (its joint at the origin, the rest skeleton of
// azhdaha_pose.mjs J) and converted with toUnits(els, PART_SCALE[part]).
import {loft, slab, crossCards, rockBox, toUnits, retex, stroke, sdPoly, registerTile, hash, mirrorX, D2R} from './azhdaha_shape.mjs';
import {PART_SCALE, J, PLATE_LEAN} from './azhdaha_pose.mjs';
import {q, rot} from './mboss_rig_math.mjs';
import {cardX, cardZ, abox, faceEl} from './mboss_model_lib.mjs';
import {PAL, LOOK_PAL, C, clamp, smooth, mix, lift, sink, N, creamPx, platePx, goldPx, spriteSize, onRect, TRANSPARENT, bevelLight, cells, ramp} from './azhdaha_materials.mjs';

export const REGION = 'body';
export const PARTS = [
  ['chest', 'chest', 13], ['belly', 'belly', 13], ['pelvis', 'pelvis', 13], ['neck1', 'neck1', 13], ['neck2', 'neck2', 13],
  ['apron', 'apron', 13], ['glow_apron', 'empty', 15],
  ['plates_neck', 'plates_neck', 13], ['plates_sh', 'plates_sh', 13], ['plates_mid', 'plates_mid', 13], ['plates_hip', 'plates_hip', 13],
  ['crys_sh', 'crys_sh', 14], ['crys_mid', 'crys_mid', 14], ['crys_hip', 'crys_hip', 14],
];
const U = (part, els) => toUnits(els, PART_SCALE[part]);
const sfx = look => (look ? '_' + look : '');
const sinD = th => Math.sin(th * D2R);

// ---- torso (model.md §2, §3.3, §3.4) --------------------------------------------------------------------------------------------
// The torso is built from overlapping rounded masses instead of one stepped barrel per part: a short barrel per part
// (chest, belly, pelvis) plus a cream plastron under the belly, a big rounded boulder over each fore leg (the shoulder
// hump, 4.3-4.4 b) and over each haunch, so no long facet runs the whole body (no terraces, no stripes) and the top view
// reads as a fat oval. Every mass is a 16-gon loft (azhdaha_shape loft) authored in WORLD rest coordinates and moved
// into its bone frame; the masses of neighbouring parts overlap by 1-2 b so the joints stay closed in the rear-ups
// (pelvis +55), the charge coil (spine yaw -20, chest -25) and the rolls.
//   zRows: [z, half width, top y, bottom y, box?, centre x?]   (axis z)
//   xRows: [x, front z, top y, back z, bottom y, box?]          (axis x: the profile in the y-z plane, round from the side)
const zSt = (bone, rows) => rows.map(([z, w, top, bot, box = 0, cx = 0]) => {
  const c = J[bone], h = (top - bot) / 2;
  return {a: z - c[2], r: [w, h, w, h], c: [cx - c[0], (top + bot) / 2 - c[1]], box};
});
const xSt = (bone, rows) => rows.map(([x, zf, top, zb, bot, box = 0]) => {
  const c = J[bone], h = (top - bot) / 2, d = (zb - zf) / 2;
  return {a: x - c[0], r: [d, h, d, h], c: [-((zf + zb) / 2 - c[2]), (top + bot) / 2 - c[1]], box};
});
// Tile per facet angle: the top and flanks in rock hide, a band of big scutes on the lower flank, the cream plastron
// underneath (one broad fold per facet).
const TZ = {hide: 'tz_hide', big: 'tz_hide_lg', scute: 'tz_scute', belly: 'tz_belly'};
const hideTex = (under, {scute = TZ.scute, lo = -.55, mid = -.2} = {}) => (k, th) => { const s = sinD(th); return s < lo ? under : s < mid ? scute : TZ.hide; };
// the plastron loft: cream folds from the widest facet down, the scute row above it, hide above that (inside the barrel)
const plastronTex = under => (k, th) => { const s = sinD(th); return s < .08 ? under : s < .8 ? TZ.scute : TZ.hide; };
for (const l of ['', '_hydro', '_pyro']) registerTile('tz_belly' + l, 64, 128, 32, {fitU: true});
registerTile(TZ.hide, 128, 128, 32); registerTile(TZ.big, 128, 128, 22); registerTile(TZ.scute, 64, 64, 30);
const pair = els => [...els, ...mirrorX(els)];
// Ledge / cap quads of one loft: the shared loft staggers them by k % 4 (0.004 b steps), so quads 4 facets apart share
// a plane and, on wide steps, overlap (the R1 pelvis rear cap, chest front cap and neck2 rings z-fought). Re-stagger
// every quad that lies across the loft axis with its own recess (0.002 + 0.0014 b x its index in the ring), always into
// the bigger section, so no two of them are closer than 0.0014 b.
const AXI = {x: 0, y: 1, z: 2};
const FACE_SIGN = {x: {west: 1, east: -1}, y: {up: 1, down: -1}, z: {south: 1, north: -1}};
function restagger(els, axis) {
  const ai = AXI[axis], groups = new Map();
  for (const e of els) {
    if (Math.abs(e.from[ai] - e.to[ai]) > 1e-6) continue;
    const fs = Object.keys(e.faces);
    if (fs.length !== 1 || !(fs[0] in FACE_SIGN[axis])) continue;
    const sg = FACE_SIGN[axis][fs[0]], key = sg + ':' + Math.round(e.from[ai] / .05);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(e);
  }
  for (const [key, list] of groups) {
    const sg = +key.split(':')[0];
    // model x runs opposite to A-frame x (abox: 8 - X): the outward face sign flips for the x axis
    const out = axis === 'x' ? -sg : sg;
    const plane = out > 0 ? Math.max(...list.map(e => e.from[ai])) : Math.min(...list.map(e => e.from[ai]));
    list.forEach((e, j) => {
      const v = +(plane - out * (.002 + .0014 * j)).toFixed(4), d = v - e.from[ai];
      e.from = e.from.slice(); e.to = e.to.slice(); e.from[ai] = v; e.to[ai] = v;
      if (e.rotation) { const o = e.rotation.origin.slice(); o[ai] = +(o[ai] + d).toFixed(4); e.rotation = {...e.rotation, origin: o}; }
    });
  }
  return els;
}
const lz = (stations, opt) => restagger(loft('z', stations, opt), 'z');
// Hidden-quad culling inside one part: every loft is also kept as a solid (its sections' 16-gons, as azhdaha_shape
// loft builds them); a quad whose corners, centre and edge midpoints all lie 0.03 b inside another solid of the same
// rigid part can never be seen and is dropped (the buried halves of the capsules, ledges inside the barrel, ...).
const FRM = {z: {A: [0, 0, 1], e1: [1, 0, 0], e2: [0, 1, 0]}, y: {A: [0, 1, 0], e1: [1, 0, 0], e2: [0, 0, -1]}, x: {A: [1, 0, 0], e1: [0, 0, -1], e2: [0, 1, 0]}};
const dot3 = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
function solidOf(axis, stations, mirror = false) {
  const F = FRM[axis], L = (x, y) => (x + y) / 2, ar = r => (Array.isArray(r) ? r : [r, r, r, r]), secs = [];
  for (let i = 0; i < stations.length - 1; i++) {
    const s0 = stations[i], s1 = stations[i + 1], c0 = s0.c || [0, 0], c1 = s1.c || [0, 0];
    const r = [0, 1, 2, 3].map(j => L(ar(s0.r)[j], ar(s1.r)[j])), box = L(s0.box || 0, s1.box || 0);
    const h = Array.from({length: 16}, (_, k) => { const th = k * 22.5 * D2R, cs = Math.cos(th), sn = Math.sin(th);
      const a = cs >= 0 ? r[0] : r[2], b = sn >= 0 ? r[1] : r[3], ell = Math.hypot(a * cs, b * sn); return ell + box * (Math.abs(a * cs) + Math.abs(b * sn) - ell); });
    secs.push({a0: Math.min(s0.a, s1.a), a1: Math.max(s0.a, s1.a), c: [L(c0[0], c1[0]), L(c0[1], c1[1])], h});
  }
  return (p, m = .03) => {
    const P = mirror ? [-p[0], p[1], p[2]] : p, a = dot3(P, F.A), u = dot3(P, F.e1), v = dot3(P, F.e2);
    return secs.some(sc => a > sc.a0 + m && a < sc.a1 - m && sc.h.every((h, k) => (u - sc.c[0]) * Math.cos(k * 22.5 * D2R) + (v - sc.c[1]) * Math.sin(k * 22.5 * D2R) < h - m));
  };
}
// A-frame sample points of an element (block space): corners, centre and edge midpoints of its faces, after rotation
function elPoints(e) {
  const lo = [8 - e.to[0], e.from[1] - 8, e.from[2] - 8], hi = [8 - e.from[0], e.to[1] - 8, e.to[2] - 8], pts = [];
  for (const x of [lo[0], (lo[0] + hi[0]) / 2, hi[0]]) for (const y of [lo[1], (lo[1] + hi[1]) / 2, hi[1]]) for (const z of [lo[2], (lo[2] + hi[2]) / 2, hi[2]]) pts.push([x, y, z]);
  if (!e.rotation) return pts;
  const {axis, angle, origin} = e.rotation, O = [8 - origin[0], origin[1] - 8, origin[2] - 8], g = (axis === 'x' ? angle : -angle) * D2R, c = Math.cos(g), s = Math.sin(g);
  return pts.map(([x, y, z]) => { const q = [x - O[0], y - O[1], z - O[2]];
    const r = axis === 'x' ? [q[0], q[1] * c - q[2] * s, q[1] * s + q[2] * c] : axis === 'y' ? [q[0] * c + q[2] * s, q[1], -q[0] * s + q[2] * c] : [q[0] * c - q[1] * s, q[0] * s + q[1] * c, q[2]];
    return [r[0] + O[0], r[1] + O[1], r[2] + O[2]]; });
}
// groups: [{els, solid}] of one part -> all elements except those buried in another group's solid
function cullHidden(groups) {
  const out = [];
  groups.forEach((g, i) => { for (const e of g.els) { const pts = elPoints(e); if (!groups.some((h, j) => j !== i && h.solid && pts.every(p => h.solid(p)))) out.push(e); } });
  return out;
}
// Disc-closed loft (near-round sections only): the facets of azhdaha_shape loft without its 16-quad ledge rings and
// caps; each step and end is closed by ONE quad showing a 16-gon alpha disc (tz_disc: hide, the 16-gon of facet
// normals k x 22.5 degrees inscribed in the quad), facing the smaller side and 0.004 b inside the bigger section. Where
// neither section contains the other, one disc a side. Saves ~15 elements per step on the capsules.
registerTile('tz_disc', 64, 64, 32);
function discLoft(axis, stations, opt) {
  const F = FRM[axis], els = loft(axis, stations, {...opt, ledges: false, caps: ''}), L = (x, y) => (x + y) / 2;
  const sec = i => { const s0 = stations[i], s1 = stations[i + 1], r = [0, 1, 2, 3].map(j => L(s0.r[j], s1.r[j])); return {r, c: [L(s0.c[0], s1.c[0]), L(s0.c[1], s1.c[1])]}; };
  const sup = (S, k) => { const th = k * 22.5 * D2R, cs = Math.cos(th), sn = Math.sin(th); return Math.hypot((cs >= 0 ? S.r[0] : S.r[2]) * cs, (sn >= 0 ? S.r[1] : S.r[3]) * sn) + S.c[0] * cs + S.c[1] * sn; };
  const contains = (A, B) => Array.from({length: 16}, (_, k) => k).every(k => sup(A, k) >= sup(B, k) - 1e-3);
  const disc = (S, a, dir) => {
    // the quad over the section's bounding box at axial a, facing dir (+1 / -1 along the axis)
    const P = (u, v) => [0, 1, 2].map(i => F.A[i] * a + F.e1[i] * u + F.e2[i] * v);
    const ad = a - dir * .004;
    const p0 = [0, 1, 2].map(i => F.A[i] * ad + F.e1[i] * (S.c[0] - S.r[2]) + F.e2[i] * (S.c[1] - S.r[3]));
    const p1 = [0, 1, 2].map(i => F.A[i] * ad + F.e1[i] * (S.c[0] + S.r[0]) + F.e2[i] * (S.c[1] + S.r[1]));
    const d = F.A.map(x => x * dir), face = d[0] > .5 ? 'left' : d[0] < -.5 ? 'right' : d[1] > .5 ? 'up' : d[1] < -.5 ? 'down' : d[2] > .5 ? 'back' : 'front';
    return faceEl([p0, p1], {[face]: {tex: 'tz_disc', uv: [0, 0, 16, 16]}});
  };
  const n = stations.length - 1, up = stations[n].a > stations[0].a ? 1 : -1;
  for (let i = 1; i < n; i++) {
    const A = sec(i - 1), B = sec(i), a = stations[i].a;
    if (contains(A, B) && contains(B, A)) continue;
    if (contains(A, B)) els.push(disc(A, a, up));
    else if (contains(B, A)) els.push(disc(B, a, -up));
    else { els.push(disc(A, a, up)); els.push(disc(B, a, -up)); }
  }
  if ((opt.ends || '').includes('-')) els.push(disc(sec(0), stations[0].a, -up));
  if ((opt.ends || '').includes('+')) els.push(disc(sec(n - 1), stations[n].a, up));
  return els;
}
const capsuleZ = (stations, opt) => { const els = discLoft('z', stations, opt);
  return [{els, solid: solidOf('z', stations)}, {els: mirrorX(els), solid: solidOf('z', stations, true)}]; };
// a z-loft with its solid (and the mirrored pair: two groups)
const lumpZ = (stations, opt, {mirror = false} = {}) => { const els = lz(stations, opt);
  return mirror ? [{els, solid: solidOf('z', stations)}, {els: mirrorX(els), solid: solidOf('z', stations, true)}] : [{els, solid: solidOf('z', stations)}]; };

function chest(look = '') {
  const B = 'tz_belly' + sfx(look);
  return cullHidden([
    // the shoulder girdle barrel (front cap under the neck, the rear end buried in the belly)
    ...lumpZ(zSt('chest', [[-2.95, 1.5, 3.6, 2.0, .1], [-2.6, 2.15, 3.95, 1.64, .12], [-2.05, 2.5, 4.16, 1.5, .14], [-.95, 2.66, 4.16, 1.44, .14],
      [.5, 2.72, 4.02, 1.43, .14]]), {tex: hideTex(B), caps: '-', seed: 11}),
    // the shoulder boulders: a rounded muscle capsule along the body over each fore leg (the hump, 4.4 b), burying the
    // upper-arm root; round from the front
    ...capsuleZ(zSt('chest', [[-3.34, .3, 3.78, 3.14, 0, 2.4], [-3.17, .6, 4.07, 2.84, 0, 2.43], [-2.92, .82, 4.28, 2.6, 0, 2.46], [-2.55, .94, 4.38, 2.5, 0, 2.47],
      [-1.6, .96, 4.38, 2.47, 0, 2.47], [-1.02, .86, 4.25, 2.58, 0, 2.42], [-.62, .58, 4.0, 2.86, 0, 2.3]]), {tex: TZ.big, ends: '-+', seed: 13}),
  ]);
}
function belly(look = '') {
  const B = 'tz_belly' + sfx(look);
  return cullHidden([
    // the back barrel (both ends buried in the chest / pelvis) over the bulging cream plastron
    ...lumpZ(zSt('spine1', [[-1.7, 2.7, 4.18, 2.15, .14], [-.4, 2.84, 4.18, 2.1, .14], [1.25, 2.8, 4.08, 2.1, .14], [2.45, 2.58, 3.92, 2.2, .14]]),
      {tex: hideTex(B, {lo: -.9, mid: -.9}), seed: 23}),
    ...lumpZ(zSt('spine1', [[-2.35, 2.45, 2.78, 1.52], [-1.75, 2.8, 2.75, 1.43], [-1.0, 3.0, 2.73, 1.38], [-.2, 3.08, 2.72, 1.35], [.7, 3.08, 2.72, 1.36],
      [1.5, 2.95, 2.72, 1.42], [2.1, 2.72, 2.74, 1.58], [2.5, 2.35, 2.76, 1.9]]), {tex: plastronTex(B), seed: 29, caps: '+'}),
  ]);
}
function pelvis(look = '') {
  const B = 'tz_belly' + sfx(look);
  return cullHidden([
    ...lumpZ(zSt('pelvis', [[.85, 2.72, 4.08, 1.85, .14], [1.95, 2.64, 3.9, 1.96, .14], [3.05, 2.38, 3.68, 2.08, .12], [4.05, 1.86, 3.46, 2.2, .1],
      [4.78, 1.26, 3.26, 2.38, .05], [5.22, .72, 3.06, 2.55]]), {tex: hideTex(B), caps: '+', seed: 37}),
    // the haunch boulders over the hip joints (round from behind)
    ...capsuleZ(zSt('pelvis', [[1.3, .5, 3.6, 2.6, 0, 2.05], [1.58, .8, 3.82, 2.25, 0, 2.08], [2.0, .96, 3.93, 2.05, 0, 2.1], [3.1, .98, 3.9, 2.05, 0, 2.1],
      [3.58, .84, 3.75, 2.2, 0, 2.05], [3.92, .55, 3.5, 2.5, 0, 1.95]]), {tex: TZ.big, ends: '-+', seed: 41}),
  ]);
}
// ---- neck: two lofts along the bone line J.neck1 -> J.neck2 -> J.head (rest), so a moved head joint keeps them joined --------
// tube(): stations every ~0.3 b in z from A to B (world, rest), the centre on the line, [half width, half height] lerped.
function tube(bone, A, B, [wA, hA], [wB, hB], {n, caps = '', seed, tex}) {
  const d = B.map((b, i) => b - A[i]), rows = [], steep = Math.abs(d[1]) > Math.abs(d[2]);
  const sa = Math.abs(d[1]) / Math.hypot(d[1], d[2]), ca = Math.abs(d[2]) / Math.hypot(d[1], d[2]);
  for (let i = 0; i <= n; i++) {
    const t = i / n, p = A.map((a, k) => a + (B[k] - a) * t), w = wA + (wB - wA) * t, h = hA + (hB - hA) * t;
    if (steep) rows.push({a: p[1] - J[bone][1], r: [w, h / sa, w, h / sa], c: [-J[bone][0], -(p[2] - J[bone][2])], box: .1});
    else rows.push({a: p[2] - J[bone][2], r: [w, h / ca, w, h / ca], c: [-J[bone][0], p[1] - J[bone][1]], box: .1});
  }
  return restagger(loft(steep ? 'y' : 'z', rows, {tex: steep ? (k, th) => tex(k, th + 180) : tex, caps, seed}), steep ? 'y' : 'z');
}
const neckTex = (k, th) => (sinD(th) < -.55 ? 'tz_belly' : sinD(th) < -.2 ? TZ.scute : TZ.hide);
const lerp3 = (a, b, t) => a.map((x, i) => x + (b[i] - x) * t);
function neck1() {
  // from inside the hump (z -1.85) to just past the neck2 joint
  const A = [0, 3.12, -1.85], B = lerp3(J.neck1, J.neck2, 1.25);
  return tube('neck1', A, B, [1.58, 1.0], [1.36, .82], {n: 4, seed: 41, tex: neckTex});
}
function neck2() {
  // from behind the neck2 joint into the back of the head (the head author's atlas J.head)
  const A = lerp3(J.neck2, J.neck1, .45), B = lerp3(J.neck2, J.head, 1.35);
  return tube('neck2', A, B, [1.38, .84], [1.05, .66], {n: 4, seed: 43, tex: neckTex, caps: '+'});
}

// ---- torso paint (body tiles; the shared hide tiles of azhdaha_materials stay for the legs) --------------------------------
// Rock hide: olive-umber stone one ramp step darker than R1 (model.md §4.1 hide #655640 base; r1_critique 1.10), big
// soft light/dark masses, pebble patches with lit tops and dark crevices, hairline cracks.
const HIDE_GREY = ramp(['#8E8A72', '#706C58', '#58553F', '#3E3C2E', '#2A281F']);
function tzHide(u, v, {cell = 9, seed = 3, warm = 0, peb = .62, base = .46} = {}) {
  // grey-olive stone (the footage reads greyer than the model.md hide ramp): mostly smooth with soft light / dark
  // masses, pebble patches only where a low-frequency mask is high
  const R = t => mix(PAL.hide(t), HIDE_GREY(t), .4);
  const m1 = N.e(u * .018 + seed, v * .018), m2 = N.a(u * .05 + seed * 3, v * .05), m3 = N.c(u * .22 + seed, v * .22);
  let t = base + .24 * (m1 - .5) + .12 * (m2 - .5) + .05 * (m3 - .5);
  const c = cells(u / cell, v / cell, seed), cl = cells((u - 1.2) / cell, (v - 1.2) / cell, seed);
  const pm = smooth(peb - .1, peb + .1, N.d(u * .028 + 7 * seed, v * .028));
  const edge = c.d2 - c.d1, lit = cl.d1 - c.d1;   // > 0 on the side of a pebble facing the upper left
  t += pm * (.08 * (c.id - .5) - .5 * lit + .06);
  let col = R(clamp(t, .05, .95));
  if (pm > .05 && edge < .11) col = sink(col, .6 * pm * (1 - edge / .11));
  const cr = Math.abs(N.f(u * .03 + seed, v * .045) - .5);
  if (cr < .011) col = sink(col, .4 * (1 - cr / .011));
  else if (cr < .02) col = mix(col, R(.25), .15);
  col = mix(col, R(.15), .2 * smooth(.62, .9, N.b(u * .07 + seed, v * .07)));    // pale dust
  if (warm) col = mix(col, C('#6C5638'), warm * N.b(u * .04, v * .04));
  return col;
}
// Scutes: the band of big rounded scales along the lower flank (v3 f1170 / f0720), domed and lit from the upper left.
function tzScute(u, v) {
  const sx = 12, sy = 10.5, c = cells(u / sx, v / sy, 17, 0, .5), cl = cells((u - 1.4) / sx, (v - 1.6) / sy, 17, 0, .5);
  const edge = c.d2 - c.d1, lit = cl.d1 - c.d1;
  let col = mix(PAL.hide(clamp(.44 + .1 * (c.id - .5) - .9 * lit + .18 * c.d1 + .06 * (N.a(u * .1, v * .1) - .5), .05, .95)), HIDE_GREY(.5), .3);
  if (edge < .13) col = sink(col, .65 * (1 - edge / .13));
  return col;
}
// Plastron fold (one per facet, u across): a rounded band, lit along its upper third, shaded into a dark groove at both
// edges; faint cross cracks (the Pyro look lights them), the odd round pebble lump.
function tzBelly(look) {
  const L = look ? LOOK_PAL[look] : null;
  return (s, t) => {
    const v = t * 128, R = PAL.cream;
    const prof = Math.sin(Math.PI * clamp(s));
    // painted bright: the plastron faces down / away from the item lights (game shade 0.4-0.55)
    let tt = .42 - .3 * prof + .1 * smooth(.2, .8, s) + .07 * (N.b(s * 3 + 1, v * .05) - .5) + .04 * (N.e(s * 9, v * .3) - .5);
    let col = R(clamp(tt, .1, .95));
    if (s < .06 || s > .95) col = mix(col, PAL.groove(.7), .75);
    else if (s < .12 || s > .89) col = mix(col, PAL.groove(.4), .35);
    const cr = Math.abs(N.f(s * 2 + 4, v * .04) - .5);
    if (cr < .018 && s > .1 && s < .9) {
      if (look === 'pyro') col = L.glow(.2 + cr * 25);
      else if (look === 'hydro') col = mix(col, L.glow(.35), .6);
      else col = mix(col, PAL.groove(.6), .55);
    }
    const p = cells(s * 2.2, v / 14, 5, 0, .7);
    if (p.d1 < .28 && p.id > .7) col = mix(col, R(.12 + .6 * (p.d1 - .1)), .5);
    return col;
  };
}

// ---- apron (model.md §3.2; r1_critique 3.1): the chest's big cream stone shield ------------------------------------------------
// A convex bell 3.6 b wide hanging from the throat (its top tucked 0.8 b up inside the neck, so a raised head uncovers it)
// to a lobed hem 0.4 b above the floor, between the fore legs. Three bent strips a side (0, 22.5, 45 degrees about Y),
// each a painted alpha card on both faces over a core of eroded boxes; the left half is authored and mirrored, so the
// sprite holds the half-glyph unrolled along the strips (u = arc length from the midline, v = height in the apron frame,
// whose origin is J.apron, world [0, 2.2, -2.8]).
// The glyph: dense thin vertical zigzag grooves, a central spine with a diamond, square-meander hooks; the lower half
// carries round pebble bumps and the lobed hem; a small gold drop spike hangs at the bottom centre.
const AP = {u0: 0, u1: 2.05, v0: -1.8, v1: .86};
const AZ0 = -.3;                                         // the centre strip's mid-plane (apron frame z; world z -3.1)
const AP_STRIPS = [[0, .66, 0], [.66, 1.4, 22.5], [1.4, 2.05, 45]];
const lobe = u => { const k = Math.round(u / .41), d = (u - k * .41) / .205; return .075 * Math.sqrt(Math.max(0, 1 - d * d)); };
const apronHem = u => -1.7 + .5 * Math.pow(Math.min(1, u / 2.05), 2.2) - lobe(u);
const apronW = v => 1.22 + .83 * smooth(.6, -.5, v);
const apronSd = (u, v) => Math.max(u - apronW(v), v - (.84 - .1 * Math.min(1, u / 1.22) ** 2), apronHem(u) - v);
function apronEls(sprite, {tint = false, glow = false} = {}) {
  const half = [];
  let px = 0, pz = AZ0;
  for (const [u0, u1, deg] of AP_STRIPS) {
    // strip in its own unrotated frame: X = u - shift on the plane z = pz, turned by deg about the pivot (px, pz)
    const shift = u0 - px, rect = {u0: AP.u0 - shift, u1: AP.u1 - shift, v0: AP.v0, v1: AP.v1};
    half.push(...slab({plane: 'z', at: pz, rect, sd: (X, v) => apronSd(X + shift, v), half: .09, sprite, edge: 'cream', cell: .11,
      clip: {u0: px, u1: px + (u1 - u0)}, core: !glow, cards: glow ? '-' : 'both', tint, eps: glow ? .028 : .012, rot: deg ? ['y', deg, [px, 0, pz]] : null}));
    px += (u1 - u0) * Math.cos(deg * D2R); pz += (u1 - u0) * Math.sin(deg * D2R);
  }
  if (!glow) {
    // round pebble knobs on the hem lobes
    for (const u of [.41, .82]) { const v = apronHem(u); half.push(rockBox([u - .11, v - .02, AZ0 - .17], [u + .11, v + .17, AZ0 + .1], 'cream', {seed: u * 7})); }
  }
  const els = [...half, ...mirrorX(half)];
  // the gold drop spike hanging under the centre lobe (added after the mirror: it sits on the midline)
  if (!glow) els.push(...shard([.005, apronHem(0) + .06, AZ0 - .03], .34, 2, 0, {thick: .03, flip: true}));
  return els;
}
// glyph polylines (half apron, u >= 0): zigzag grooves, the centre spine, V folds and meander hooks
const zig = (u, v0, v1, amp, per, ph = 0) => { const pts = []; for (let v = v0; v >= v1 - 1e-6; v -= per / 2) { const k = Math.round((v0 - v) / (per / 2)); pts.push([u + ((k + ph) % 2 ? amp : -amp), v]); } return pts; };
const meander = (cu, cv, r) => [[cu - r, cv + r], [cu + r, cv + r], [cu + r, cv - r], [cu - r * .45, cv - r], [cu - r * .45, cv + r * .3], [cu + r * .35, cv + r * .3], [cu + r * .35, cv - r * .4]];
const AP_LINES = [
  [[0, .8], [0, -1.55]],
  [[0, -.02], [.17, -.2], [0, -.38]],
  zig(.3, .74, -1.38, .07, .42),
  zig(.62, .62, -1.6, .065, .5, 1),
  [...zig(.95, .4, -1.18, .06, .46), [1.05, -1.3], [1.18, -1.22]],
  zig(1.28, .2, -1.5, .07, .44, 1),
  zig(1.6, -.12, -1.34, .06, .4),
  [[.3, -1.38], [.46, -1.62], [.62, -1.6]],
  meander(1.55, .3, .17), meander(.95, -1.48, .12), meander(1.88, -.62, .1),
].map(pts => stroke(pts, () => 0));
const apronLine = (u, v) => Math.min(...AP_LINES.map(S => S.near(u, v).d));
function apronBumps(u, v) {
  // round pebble bumps over the lower half (denser toward the hem); returns the light term or null
  if (v > -.45) return null;
  const c = cells(u / .26, v / .24, 31, 0, .7), dens = smooth(-.45, -1.4, v);
  if (c.id > .25 + .6 * dens) return null;
  const r = .3 + .12 * c.id;
  if (c.d1 > r) return null;
  const cl = cells((u + .03) / .26, (v - .03) / .24, 31, 0, .7);
  return {lit: (cl.d1 - c.d1) * 6, rim: c.d1 / r};
}
function apronPaint(look) {
  const L = look ? LOOK_PAL[look] : null;
  return (u, v) => {
    const s = apronSd(u, v);
    if (s > 0) return null;
    let c = creamPx(u * 60 + 40, v * 60 + 40);
    c = mix(c, PAL.cream(.45), .25 * smooth(.6, 2.05, u) + .15 * smooth(-1.0, -1.8, v));
    const b = apronBumps(u, v);
    if (b) { c = mix(c, PAL.cream(clamp(.3 - .25 * b.lit + .25 * b.rim * b.rim)), .7); if (b.rim > .85) c = mix(c, PAL.cream(.6), .4); }
    if (s > -.035) c = mix(c, PAL.cream(.7), .6);                       // the shadowed rim / hem lip
    const d = apronLine(u, v);
    if (d < .016) c = L ? L.glow(.1 + d / .016 * .4) : mix(PAL.groove(.55), PAL.groove(.9), d / .016);
    else if (d < .03) c = L ? mix(c, L.glow(.55), .45 * (1 - (d - .016) / .014)) : mix(c, PAL.cream(.08), .35);   // the lit lip of the groove
    return c;
  };
}
const apronMask = (u, v) => { if (apronSd(u, v) > 0) return null; const d = apronLine(u, v); return d < .022 ? [255, 255, 255, 255] : d < .04 ? [255, 255, 255, Math.round(255 * (1 - (d - .022) / .018))] : null; };

// ---- dorsal plates (model.md §3.5; r1_critique 3.3) -------------------------------------------------------------------------------
// Fewer, larger feather blades (1.5-3.3 b): a tall central row (tallest over the shoulders, 7.3 b, and mid-back, 7.0 b,
// falling to 4.7 b over the rump: the v8 f2280 crest) and one or two side rows splayed 22.5 / 45 degrees. Each plate is
// a crossed pair of painted cards, a side card (its profile, plane x) and a front card (its face, plane z), turned out
// by the splay, over a thin dark core; the group part leans every plate back (azhdaha_pose.mjs PLATE_LEAN). Central
// plates of one group sit at x +-0.03..0.06 so no two side cards share a plane (r1_critique 1.6).
// Sheet: 6 cells of 64 x 128 (aspect 1:2): 0-2 side profiles (upright, the tip curling back), 3-5 front faces.
const BLADES = [
  {kind: 's', tip: .2, w: .38}, {kind: 's', tip: .12, w: .34, orange: true}, {kind: 's', tip: .28, w: .4, notch: true},
  {kind: 'f', w: .44}, {kind: 'f', w: .38, orange: true}, {kind: 'f', w: .5, notch: true},
];
const SHEET = {cw: 64, ch: 128, n: BLADES.length};
const AS = .5;   // cell aspect (width / height)
const bladeW = (b, t) => (b.kind === 'f' ? (t < .3 ? .5 + .5 * t / .3 : Math.pow((1 - t) / .7, .85)) : 1.2 * (t < .38 ? .5 + .5 * t / .38 : Math.pow((1 - t) / .62, .9)));
const BL = BLADES.map(b => {
  const x0 = b.kind === 'f' ? .5 : .38, top = b.kind === 'f' ? .93 : 1;
  const pts = Array.from({length: 17}, (_, i) => { const t = i / 16; return [(x0 + (b.tip || 0) * smooth(.5, 1, t) * t) * AS, t * top]; });
  const S = stroke(pts, t => b.w * AS * bladeW(b, t));
  return {...b, S, sd: (x, y) => { let d = S.sd(x * AS, y); if (b.notch) { const n = Math.hypot((x - (b.kind === 'f' ? .74 : .62)) * AS, y - .58); d = Math.max(d, -(n - .035)); } return d; }};
});
function bladeColour(b, x, y, look) {
  const d = b.sd(x, y);
  if (d > 0) return null;
  const n = b.S.near(x * AS, y), across = Math.abs(n.s) / Math.max(1e-3, b.w * AS * bladeW(b, n.t));
  const LP = look ? LOOK_PAL[look] : null;
  // Cryo / Electro: the stone stays dark (the deep end of the look ramp); only the rim and a ridge glint glow
  const R = LP ? (t => LP.stone(.45 + .55 * t)) : PAL.plate;
  let c = platePx(x * 60, y * 120, R);
  // a central ridge (one half lit, one shaded) and feather grain toward the tip
  c = n.s > 0 ? mix(c, R(.12), .45 * (1 - across)) : mix(c, R(.8), .4 * (1 - across));
  if (across < .05) c = mix(c, R(.05), .6);
  if (Math.abs(((n.t * 8 + across * 1.6) % 1) - .5) < .045 && across > .28) c = mix(c, R(.9), .3);
  // amber veins along the ridge (v4 f0900) and the orange lower third of some plates
  if (!LP && across > .12 && across < .5 && Math.abs(((across * 5 + n.t * .6) % 1) - .5) < .06 && n.t > .08 && n.t < .7) c = mix(c, PAL.plateOr(.35 + .4 * n.t), .45 * (1 - n.t));
  if (b.orange && y < .45) c = mix(c, PAL.plateOr(.1 + 1.4 * y), smooth(.45, .1, y));
  if (d > -.012) c = LP ? LP.glow(.12) : mix(c, PAL.plate(0), .6);          // rim: greyish highlight / element glow
  else if (LP && d > -.03) c = mix(c, LP.glow(.5), .45);
  if (LP && across < .045 && n.t > .3) c = mix(c, LP.glow(.35), .5);
  return c;
}
const plateSheet = look => (s, t) => { const k = Math.min(SHEET.n - 1, Math.floor(s * SHEET.n)); return bladeColour(BL[k], s * SHEET.n - k, 1 - t, look) || TRANSPARENT; };
const cellUV = (els, spr, k, n) => {
  for (const e of els) for (const f of Object.values(e.faces)) if (f.texture === '#' + spr) { const [a, b, c2, d] = f.uv; f.uv = [(k + a / 16) * 16 / n, b, (k + c2 / 16) * 16 / n, d].map(v => +v.toFixed(4)); }
  return els;
};
// One plate in its group frame: base [x, y, z], length L, side / front cells, splay (deg about Z; - tips toward +X), front width factor.
function plate(spr, [x, y, z], L, ks, kf, splay = 0, wf = 1) {
  const W = L * AS, Wf = L * AS * .9 * wf, rot = splay ? ['z', splay, [x, y, z]] : undefined;
  const side = cardX(spr, x, {Z0: z - .38 * W, Z1: z + .62 * W, Y0: y, Y1: y + L}, {rot});
  const front = cardZ(spr, z, {X0: x - Wf / 2, X1: x + Wf / 2, Y0: y, Y1: y + L * .93}, {rot, uvr: [0, .07, 1, 1]});
  cellUV([side], spr, ks, SHEET.n); cellUV([front], spr, kf, SHEET.n);
  const core = rockBox([x - .04, y, z - .06], [x + .04, y + L * .5, z + .06], spr === 'plates' ? 'plate' : spr.replace('plates', 'plate'), {rot});
  return [side, front, core];
}
// Plate layout per group in WORLD coordinates (rest, before the group lean): [x, base y, z, L, side cell, front cell,
// splay, front width]; entries with |x| > 0.1 are mirrored. Bases sit about 0.25 b inside the hide.
const G = {
  neck: {base: 'plN', g: 'neck', list: [[.02, 3.2, -3.05, 2.3, 0, 3, 0, 1], [.55, 3.12, -2.95, 2.1, 2, 4, -22.5, 1], [1.05, 2.88, -2.8, 1.9, 1, 5, -45, .9],
    [1.4, 2.5, -2.62, 1.5, 0, 3, -45, .8]]},
  sh: {base: 'plS', g: 'sh', list: [[.03, 4.1, -2.3, 3.2, 0, 3, 0, 1.15], [-.04, 4.0, -2.85, 1.8, 1, 4, 0, 1], [.72, 4.05, -1.55, 2.95, 2, 5, -22.5, 1.1],
    [.76, 4.0, -2.42, 2.2, 0, 3, -22.5, 1], [1.45, 3.78, -1.85, 1.95, 1, 4, -45, 1]]},
  mid: {base: 'plM', g: 'mid', list: [[.05, 4.1, .1, 3.15, 2, 5, 0, 1.1], [-.05, 4.12, -.6, 1.9, 1, 3, 0, 1], [.75, 4.0, .62, 2.7, 0, 4, -22.5, 1.1],
    [.72, 4.06, -.35, 2.0, 2, 3, -22.5, 1], [1.5, 3.72, .2, 2.0, 1, 5, -45, 1]]},
  hip: {base: 'plH', g: 'hip', list: [[-.09, 3.82, 1.3, 2.75, 0, 3, 0, 1.1], [.03, 3.62, 2.4, 2.4, 2, 4, 0, 1], [-.03, 3.4, 3.65, 2.0, 1, 5, 0, .9],
    [.09, 3.15, 4.4, 1.7, 0, 3, 0, .8], [.7, 3.7, 2.2, 2.3, 2, 4, -22.5, 1], [.68, 3.45, 3.3, 1.8, 1, 5, -22.5, .9], [1.35, 3.45, 2.6, 1.6, 0, 3, -45, .9]]},
};
function plateGroup(key, spr) {
  const {base, g, list} = G[key], B = J[base], Ri = q([-PLATE_LEAN[g], 0, 0]), els = [];
  for (const [x, y, z, L, ks, kf, sp, wf] of list) for (const sx of Math.abs(x) > .1 ? [1, -1] : [1]) {
    const p = rot(Ri, [sx * x - B[0], y - B[1], z - B[2]]);
    els.push(...plate(spr, p, L, ks, kf, sx * sp, wf));
  }
  return els;
}

// ---- gold crystals (model.md §3.6; r1_critique 3.4): trident / bird clusters along the crest's lower edge ---------------------
// One cluster = a crossed pair of cards (side + front) showing a whole fan of 2-3 flat pointed blades painted in one cell
// (so it reads as a trident or a bird with spread wings from the front and from the side), turned out by its splay,
// over a short gold core. Sheet: 4 cells of 64 x 64: 0 trident, 1 bird (one long wing), 2 single broad blade (the big
// shoulder spike), 3 twin V.
const SHARD_FANS = [
  [[0, .98, .34, 1], [-36, .7, .3, 1], [34, .62, .28]],
  [[-8, .95, .34, 1], [-44, .78, .3], [30, .52, .24]],
  [[0, 1, .42, 1]],
  [[-18, .95, .34, 1], [22, .84, .3, 1]],
];
// each blade: a broad pointed leaf curving slightly outward, the 'bird' ones with a barb notch cut into the outer edge
const SH = SHARD_FANS.map(fan => fan.map(([deg, L, w, barb]) => {
  const a = deg * D2R, dx = Math.sin(a), dy = Math.cos(a), x0 = .5, y0 = .03, bend = Math.sign(deg || 1) * .06;
  const pts = Array.from({length: 9}, (_, i) => { const t = i / 8; return [x0 + (dx * L * .92 + bend * t) * t, y0 + dy * L * .92 * t]; });
  const S = stroke(pts, t => w * (t < .22 ? .5 + 2.3 * t : 1) * Math.pow(1 - t, .75) * .5 + .006);
  // the barb: a notch on the outer edge at 55 % of the blade
  const nx = x0 + dx * L * .5 + Math.sign(deg || 1) * dy * w * .3, ny = y0 + dy * L * .5 - Math.sign(deg || 1) * dx * w * .3;
  return {S, dx, dy, sd: barb ? (x, y) => Math.max(S.sd(x, y), -(Math.hypot(x - nx, y - ny) - w * .16)) : (x, y) => S.sd(x, y)};
}));
function shardColour(k, x, y) {
  let best = null;
  for (const b of SH[k]) { const d = b.sd(x, y); if (d <= 0 && (!best || d < best.d)) best = {d, b}; }
  if (!best) return null;
  const n = best.b.S.near(x, y), side = n.s > 0;
  let c = goldPx(side ? .1 + .25 * n.t : .42 + .2 * n.t, x * 60, y * 60);
  if (best.d > -.014) c = PAL.gold(side ? .55 : .8);           // darker amber edges
  if (Math.abs(n.s) < .007 && n.t < .92) c = PAL.gold(0);      // the bright facet ridge
  return c;
}
const shardSheet = (s, t) => { const k = Math.min(3, Math.floor(s * 4)); return shardColour(k, s * 4 - k, 1 - t) || TRANSPARENT; };
const shardUV = (els, k) => { for (const e of els) for (const f of Object.values(e.faces)) if (f.texture === '#shards') { const [a, b, c2, d] = f.uv; f.uv = [k * 4 + a / 4, b, k * 4 + c2 / 4, d].map(v => +v.toFixed(4)); } return els; };
// A cluster at [x, y, z] (its base), height L, cell k, splay (deg about Z); flip: the cell hangs down (the apron drop spike)
function shard([x, y, z], L, k, splay = 0, {thick = .07, flip = false} = {}) {
  const rot = splay ? ['z', splay, [x, y, z]] : undefined, Y0 = flip ? y - L : y, Y1 = flip ? y : y + L, uvr = flip ? [0, 1, 1, 0] : [0, 0, 1, 1];
  const els = shardUV([cardX('shards', x, {Z0: z - L / 2, Z1: z + L / 2, Y0, Y1}, {rot, uvr}), cardZ('shards', z, {X0: x - L / 2, X1: x + L / 2, Y0, Y1}, {rot, uvr})], k);
  if (thick) els.push(rockBox([x - thick, flip ? y - L * .4 : y, z - thick], [x + thick, flip ? y : y + L * .4, z + thick], 'gold', {rot, seed: x * 3 + z}));
  return els;
}
// [x, y, z, L, cell, splay]: world rest positions (x > 0, mirrored), base about 0.2 b inside the hide
const CRYS = {
  sh: {base: 'plS', list: [[2.15, 3.95, -1.95, 2.5, 2, -22.5], [1.75, 4.0, -1.0, 2.2, 0, -22.5], [2.45, 3.4, -2.6, 1.8, 3, -45], [1.6, 4.02, -2.62, 1.75, 1, -22.5]]},
  mid: {base: 'plM', list: [[2.05, 3.75, .0, 2.3, 0, -45], [1.82, 3.9, 1.0, 2.0, 1, -22.5], [2.4, 3.2, .62, 1.7, 3, -45]]},
  hip: {base: 'plH', list: [[1.88, 3.5, 2.1, 2.0, 0, -45], [1.6, 3.42, 3.1, 1.7, 1, -22.5], [2.15, 3.0, 2.8, 1.6, 3, -45]]},
};
function crystalGroup(g) {
  const {base, list} = CRYS[g], B = J[base], els = [];
  for (const [x, y, z, L, k, sp] of list) for (const s of [1, -1]) els.push(...shard([s * x - B[0], y - B[1], z - B[2]], L, k, s * sp));
  return els;
}

// ---- region exports ---------------------------------------------------------------------------------------------------------
export function models() {
  const M = {
    chest: U('chest', chest()), belly: U('belly', belly()), pelvis: U('pelvis', pelvis()), neck1: U('neck1', neck1()), neck2: U('neck2', neck2()),
    apron: U('apron', apronEls('apron')),
    crys_sh: U('crys_sh', crystalGroup('sh')), crys_mid: U('crys_mid', crystalGroup('mid')), crys_hip: U('crys_hip', crystalGroup('hip')),
  };
  for (const look of ['hydro', 'pyro']) {
    M['chest_' + look] = U('chest', chest(look));
    M['belly_' + look] = U('belly', belly(look));
    M['pelvis_' + look] = U('pelvis', pelvis(look));
    M['apron_' + look] = U('apron', apronEls('apron_' + look));
  }
  M.glow_apron = U('glow_apron', apronEls('apron_mask', {tint: true, glow: true}));
  for (const [g, part] of [['neck', 'plates_neck'], ['sh', 'plates_sh'], ['mid', 'plates_mid'], ['hip', 'plates_hip']]) {
    M[part] = U(part, plateGroup(g, 'plates'));
    for (const look of ['cryo', 'electro']) M[part + '_' + look] = U(part, plateGroup(g, 'plates_' + look));
  }
  return M;
}
export const LOOKS = {
  legs: {
    chest: {geo: 'chest', hydro: 'chest_hydro', pyro: 'chest_pyro'},
    belly: {geo: 'belly', hydro: 'belly_hydro', pyro: 'belly_pyro'},
    pelvis: {geo: 'pelvis', hydro: 'pelvis_hydro', pyro: 'pelvis_pyro'},
    apron: {geo: 'apron', hydro: 'apron_hydro', pyro: 'apron_pyro'},
    glow_apron: {geo: 'empty', hydro: 'glow_apron_hydro', pyro: 'glow_apron_pyro'},
  },
  tail: Object.fromEntries(['plates_neck', 'plates_sh', 'plates_mid', 'plates_hip'].map(p => [p, {geo: p, cryo: p + '_cryo', electro: p + '_electro'}])),
};
export const TINTED = {glow_apron_hydro: ['glow_apron', LOOK_PAL.hydro.tint], glow_apron_pyro: ['glow_apron', LOOK_PAL.pyro.tint]};
// brightness per look (the bright parts of a look; others keep their PARTS level)
// the plates stay dark stone in phase 3 (only the painted rims glow): no full-bright plate parts (r1_critique 3.7)
export const LOOK_BRIGHT = {legs: {hydro: {apron: 14, belly: 13}, pyro: {apron: 14, belly: 14, chest: 14, pelvis: 14}}, tail: {cryo: Object.fromEntries(Object.keys(LOOKS.tail).map(p => [p, 14])), electro: Object.fromEntries(Object.keys(LOOKS.tail).map(p => [p, 14]))}};

export function sprites() {
  const S = {};
  const card = (name, rect, ppb, fn, tr = false) => { const [w, h] = spriteSize(rect, ppb); S[name] = [w, h, onRect(rect, fn), tr]; };
  card('apron', AP, 80, apronPaint(null));
  card('apron_hydro', AP, 80, apronPaint('hydro'));
  card('apron_pyro', AP, 80, apronPaint('pyro'));
  card('apron_mask', AP, 80, apronMask, true);
  S.plates = [SHEET.cw * SHEET.n, SHEET.ch, plateSheet(null), false];
  S.plates_cryo = [SHEET.cw * SHEET.n, SHEET.ch, plateSheet('cryo'), false];
  S.plates_electro = [SHEET.cw * SHEET.n, SHEET.ch, plateSheet('electro'), false];
  S.shards = [256, 64, shardSheet, false];
  S.tz_hide = [128, 128, (s, t) => tzHide(s * 128, t * 128), false];
  S.tz_hide_lg = [128, 128, (s, t) => tzHide(s * 128, t * 128, {cell: 12, seed: 5, warm: .25, peb: .52, base: .44}), false];
  S.tz_scute = [64, 64, (s, t) => tzScute(s * 64, t * 64), false];
  // the 16-gon disc closing the capsule steps (facet normals k x 22.5 degrees, inradius = the half side)
  S.tz_disc = [64, 64, (s, t) => (Array.from({length: 16}, (_, k) => k * 22.5 * D2R).every(a => (s - .5) * Math.cos(a) + (t - .5) * Math.sin(a) <= .5)
    ? tzHide(s * 128, t * 128, {cell: 12, seed: 5, warm: .25, peb: .52, base: .44}) : TRANSPARENT), false];
  for (const l of [null, 'hydro', 'pyro']) S['tz_belly' + sfx(l)] = [64, 128, tzBelly(l), false];
  return S;
}
