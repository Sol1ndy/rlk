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
import {loft, slab, crossCards, rockBox, toUnits, retex, stroke, sdPoly, registerTile, registerWrap, hash, mirrorX, D2R} from './azhdaha_shape.mjs';
import {PART_SCALE, J, PLATE_LEAN, NECK_TILT} from './azhdaha_pose.mjs';
import {q, rot} from './mboss_rig_math.mjs';
import {cardX, cardZ, abox, faceEl} from './mboss_model_lib.mjs';
import {PAL, LOOK_PAL, C, clamp, smooth, mix, lift, sink, scale, N, creamPx, platePx, goldPx, spriteSize, onRect, TRANSPARENT, bevelLight, cells, ramp} from './azhdaha_materials.mjs';

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

// ---- torso helpers ---------------------------------------------------------------------------------------------------------
// zRows: [z, half width, top y, bottom y, box?, centre x?] (axis z); xRows: [x, front z, top y, back z, bottom y, box?]
const zSt = (bone, rows) => rows.map(([z, w, top, bot, box = 0, cx = 0]) => {
  const c = J[bone], h = (top - bot) / 2;
  return {a: z - c[2], r: [w, h, w, h], c: [cx - c[0], (top + bot) / 2 - c[1]], box};
});
const xSt = (bone, rows) => rows.map(([x, zf, top, zb, bot, box = 0]) => {
  const c = J[bone], h = (top - bot) / 2, d = (zb - zf) / 2;
  return {a: x - c[0], r: [d, h, d, h], c: [-((zf + zb) / 2 - c[2]), (top + bot) / 2 - c[1]], box};
});
// Ledge / cap quads of one loft: the shared loft staggers them by k % 4 (0.004 b steps), so quads 4 facets apart share
// a plane and, on wide steps, overlap (the R1 pelvis rear cap, chest front cap and neck2 rings z-fought). Re-stagger
// every quad that lies across the loft axis with its own recess (0.002 + 0.0025 b x its index in the cluster), always
// into the bigger section, so no two of them are closer than 0.0025 b.
const AXI = {x: 0, y: 1, z: 2};
const FACE_SIGN = {x: {west: 1, east: -1}, y: {up: 1, down: -1}, z: {south: 1, north: -1}};
function restagger(els, axis, base = .002) {
  const ai = AXI[axis], groups = new Map(), cand = [];
  for (const e of els) {
    if (Math.abs(e.from[ai] - e.to[ai]) > 1e-6) continue;
    const fs = Object.keys(e.faces);
    if (fs.length !== 1 || !(fs[0] in FACE_SIGN[axis])) continue;
    cand.push([FACE_SIGN[axis][fs[0]], e.from[ai], e]);
  }
  // cluster per facing: consecutive planes closer than 0.04 b form one group (a fixed grid split near neighbours)
  cand.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  let key = null, last = null;
  for (const [sg, v, e] of cand) {
    if (!key || key.sg !== sg || v - last > .04) groups.set(key = {sg}, []);
    groups.get(key).push(e); last = v;
  }
  for (const [{sg}, list] of groups) {
    // model x runs opposite to A-frame x (abox: 8 - X): the outward face sign flips for the x axis
    const out = axis === 'x' ? -sg : sg;
    const plane = out > 0 ? Math.max(...list.map(e => e.from[ai])) : Math.min(...list.map(e => e.from[ai]));
    list.forEach((e, j) => {
      const v = +(plane - out * (base + .0025 * j)).toFixed(4), d = v - e.from[ai];
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
// ---- torso (model.md §2, §3.3, §3.4; r1_critique 1.4-1.6, 1.10, 3.2, 3.5) ---------------------------------------------------
// One smooth body surface (BODY: the profile along z) sampled by three barrels, one z-loft per part (chest, belly,
// pelvis) with a station every 0.3-0.5 b, so the side outline is a fine staircase of 0.02-0.1 b steps: the shoulder
// hump, the long back, the sagging belly (1.42 b mid-body), the rump narrowing into the tail root. The sections are
// egg-shaped (quarter ellipses: the widest line low, at 2.6-2.9 b, a taller top) with fuller top corners over the
// shoulders. Each barrel owns a z range (OWN); outside it, it tucks 0.06 b + 0.1 b per b of depth inside its
// neighbour, so the joints stay closed in the rear-ups (pelvis +55), the charge coil (spine -20 / chest -25 yaw) and
// the rolls, with no coplanar facets at rest. The shoulder and haunch muscles are the legs region's upper arm and
// haunch masses, which stand out of the barrels.
// Paint: the flank and back facets (k 0..8) show ONE wrap sprite per barrel, painted in world coordinates (continuous
// pebble hide, the scute row, the carved glyphs) and light-corrected: albedo x F(smooth normal) / F(facet normal),
// F = the item-display light averaged over the yaw, so the facets and the ledges shade like the smooth body instead
// of flat bands and bright step stripes. The plastron facets (k 9..15) show fold tiles (two broad lengthwise rolls per
// facet, the scute row on the top facet) with the Hydro / Pyro crack looks; the ledges and caps show small
// light-corrected hide / cream tiles by their azimuth.
// BODY rows: [z, top (spine line), bottom, half width, height of the widest line, box (0 round .. 1 square corners)].
const BODY = [
  [-3.08, 3.68, 2.28, 1.85, 2.98, .2], [-2.78, 3.97, 2.0, 2.28, 2.98, .22], [-2.42, 4.13, 1.83, 2.52, 2.96, .22],
  [-2.0, 4.25, 1.7, 2.66, 2.94, .2], [-1.3, 4.3, 1.56, 2.76, 2.92, .2],
  [-.5, 4.24, 1.46, 2.82, 2.9, .18], [.3, 4.18, 1.42, 2.84, 2.88, .18], [1.1, 4.1, 1.45, 2.8, 2.88, .18],
  [1.8, 3.98, 1.6, 2.68, 2.9, .18], [2.5, 3.8, 1.86, 2.48, 2.94, .18], [3.2, 3.58, 2.14, 2.2, 2.96, .16],
  [3.85, 3.38, 2.4, 1.82, 2.96, .12], [4.45, 3.2, 2.58, 1.4, 2.94, .08], [5.0, 3.05, 2.7, .96, 2.92, .04], [5.4, 2.98, 2.76, .66, 2.9, 0],
];
const catmull = (p0, p1, p2, p3, t) => .5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (3 * p1 - p0 - 3 * p2 + p3) * t * t * t);
function bodyAt(z) {
  const n = BODY.length, zc = Math.max(BODY[0][0], Math.min(BODY[n - 1][0], z));
  let i = 0;
  while (i < n - 2 && zc > BODY[i + 1][0]) i++;
  const t = (zc - BODY[i][0]) / (BODY[i + 1][0] - BODY[i][0]), R = j => BODY[Math.max(0, Math.min(n - 1, j))];
  return [1, 2, 3, 4, 5].map(c => catmull(R(i - 1)[c], R(i)[c], R(i + 1)[c], R(i + 2)[c], t));
}
// z ranges owned by each barrel (world, rest) and the tuck of a barrel outside its range
const OWN = {chest: [-9, -1.0], belly: [-1.0, 1.6], pelvis: [1.6, 9]};
const tuck = (P, z) => { const [lo, hi] = OWN[P], d = z <= lo - 1e-6 ? lo - z : z >= hi + 1e-6 ? z - hi : -1; return d < 0 ? 0 : Math.min(.32, .06 + .1 * d); };
// (a station exactly at an owner boundary is tucked on the side that does not own it: the hand-over never shares a plane)
const BARRELS = {
  chest: {bone: 'chest', zs: [-3.08, -2.94, -2.78, -2.6, -2.4, -2.16, -1.88, -1.42, -1.0, -.6, -.1], caps: '-', seed: 11, W: 256, H: 96},
  belly: {bone: 'spine1', zs: [-2.3, -1.65, -1.0, -.45, .25, .95, 1.6, 2.1, 2.7], seed: 23, W: 256, H: 128},
  pelvis: {bone: 'pelvis', zs: [.7, 1.15, 1.6, 2.05, 2.5, 2.9, 3.27, 3.62, 3.96, 4.28, 4.6, 4.9, 5.17, 5.4], caps: '+', seed: 37, W: 256, H: 112},
};
// the section of barrel P at world z: {r: [e1+, e2+, e1-, e2-], cy, box}
// the belly runs 0.008 b inside the common hull and recesses its cross quads by half a stagger step more, so where its
// averaged sections meet the chest's or pelvis's no two quads share a plane (r2_body/tools/zfight2.py)
const GROW = {belly: -.008}, BASE = {belly: .00325};
const secAt = (P, z) => { if (BARRELS[P].sec) return BARRELS[P].sec(z); const [top, bot, hw, cy, box] = bodyAt(z), t = tuck(P, z) - (GROW[P] || 0); return {r: [hw - t, top - cy - t, hw - t, cy - bot - t], cy, box}; };
const barrelSt = P => { const {bone, zs, local} = BARRELS[P], c = local ? [0, 0, 0] : J[bone];
  return zs.map(z => { const s = secAt(P, z); return {a: z - c[2], r: s.r, c: [-c[0], s.cy - c[1]], box: s.box}; }); };
// support distance of a section for the normal angle th (deg), as azhdaha_shape loft
const supp = (s, th) => { const c = Math.cos(th * D2R), n = Math.sin(th * D2R), a = c >= 0 ? s.r[0] : s.r[2], b = n >= 0 ? s.r[1] : s.r[3];
  const ell = Math.hypot(a * c, b * n); return ell + (s.box || 0) * (Math.abs(a * c) + Math.abs(b * n) - ell); };
// the up component of the smooth surface's normal at azimuth th (deg) and world z: the radial direction tilted by the
// slope of the barrel along z (a tapering end faces forward / back)
// (a tilted neck frame: world up = local y cos T + local z sin T)
const smoothNy = (P, th, z) => { const rad = z2 => { const S = secAt(P, z2); return supp(S, th) + S.cy * Math.sin(th * D2R); };
  const sl = (rad(z + .12) - rad(z - .12)) / .24, T = (BARRELS[P].tilt || 0) * D2R;
  return (Math.sin(th * D2R) * Math.cos(T) - sl * Math.sin(T)) / Math.hypot(1, sl); };
const faceNy = (P, k) => Math.sin(k * 22.5 * D2R) * Math.cos((BARRELS[P].tilt || 0) * D2R);
// The item-display light (two world-fixed lights, ambient 0.4; minecraft entity lighting), averaged over the yaw (the
// boss turns): F(ny) for a unit normal with up component ny.
const nrm3 = v => { const l = Math.hypot(...v); return v.map(x => x / l); };
const ML0 = nrm3([.2, 1, -.7]), ML1 = nrm3([-.2, 1, .7]);
const mcShade = n => Math.min(1, .6 * (Math.max(0, dot3(n, ML0)) + Math.max(0, dot3(n, ML1))) + .4);
const FLT = Array.from({length: 201}, (_, i) => { const ny = -1 + i / 100, h = Math.sqrt(Math.max(0, 1 - ny * ny)); let s = 0;
  for (let j = 0; j < 72; j++) { const a = j * Math.PI / 36; s += mcShade([h * Math.cos(a), ny, h * Math.sin(a)]); } return s / 72; });
const FL = ny => { const x = (Math.max(-1, Math.min(1, ny)) + 1) * 100, i = Math.min(199, Math.floor(x)); return FLT[i] + (FLT[i + 1] - FLT[i]) * (x - i); };
const LIGHTK = (nySmooth, nyFace) => Math.max(.55, Math.min(1.6, FL(nySmooth) / FL(nyFace)));
// plastron fold tiles (+ looks) and the light-corrected ledge tiles (hide: classes 2..8, cream: 0..4; class j <-> the
// smooth surface's up component j / 4 - 1)
for (const l of ['', '_hydro', '_pyro']) for (const t of ['tz_pl', 'tz_pl1', 'tz_plb']) registerTile(t + l, 64, 64, 32, {fitU: true});
const LEDGE_H = [2, 3, 4, 5, 6, 7, 8], LEDGE_C = [0, 1, 2, 3, 4];
for (const j of LEDGE_H) registerTile('tz_lh' + j, 32, 32, 32);
for (const j of LEDGE_C) registerTile('tz_lc' + j, 32, 32, 32);
const WRAP_N = 9;                                        // wrap slots: facets k = 0..8
// Post-process of a barrel-like z-loft: wrap u -> compact slots, the right-hand plastron facets turned so their u runs
// upward like the left ones, every ledge / cap retextured to the light-corrected tile of its azimuth class.
function finishBarrel(els, wrap, cyAt, nyAt, cream = th => Math.sin(th * D2R) < -.2) {
  for (const e of els) {
    const [fname, face] = Object.entries(e.faces)[0], tex = face.texture.slice(1);
    if (fname === 'north' || fname === 'south') {
      const pts = elPoints(e), m = [0, 1, 2].map(i => pts.reduce((s, p) => s + p[i], 0) / pts.length), dx = m[0], dy = m[1] - cyAt(m[2]);
      const th = Math.atan2(dy, dx) / D2R, rr = Math.hypot(dx, dy), sn = rr < .45 ? 0 : nyAt(th, m[2]);
      const j = Math.max(0, Math.min(8, Math.round((sn + 1) * 4)));
      face.texture = '#' + (cream(th) && rr >= .45 ? 'tz_lc' + Math.min(4, j) : 'tz_lh' + Math.max(2, j));
      face.uv = [0, 0, 16, 16];
    } else if (tex === wrap) {
      const k = Math.floor(Math.min(face.uv[0], face.uv[2]) + 1e-3);
      if (k > 8) throw new Error(`wrap facet ${k} past the slots`);
      face.uv = [face.uv[0] * 16 / WRAP_N, Math.max(0, Math.min(16, face.uv[1])), face.uv[2] * 16 / WRAP_N, Math.max(0, Math.min(16, face.uv[3]))].map(r => +r.toFixed(4));
    } else if (tex.startsWith('tz_pl')) {
      const pts = elPoints(e), mx = pts.reduce((s, p) => s + p[0], 0) / pts.length;
      if (mx < -.05) face.uv = [face.uv[2], face.uv[1], face.uv[0], face.uv[3]];
    }
  }
  return els;
}
function barrel(P, look = '') {
  const {bone, caps = '', seed} = BARRELS[P], wrap = 'tw_' + P, s = sfx(look), c = J[bone];
  registerWrap(wrap);
  const st = barrelSt(P);
  const tex = k => (k <= 8 ? wrap : k === 12 ? 'tz_plb' + s : (k === 9 || k === 15) ? 'tz_pl1' + s : 'tz_pl' + s);
  const els = restagger(loft('z', st, {tex: k => tex(k), caps, seed}), 'z', BASE[P]);
  const local = BARRELS[P].local;
  return finishBarrel(els, wrap, zp => (local ? secAt(P, zp).cy : bodyAt(zp + c[2])[3] - c[1]), (th, zp) => smoothNy(P, th, local ? zp : zp + c[2]));
}
const chest = look => barrel('chest', look), belly = look => barrel('belly', look), pelvis = look => barrel('pelvis', look);

// ---- neck (model.md §3.3): two tubes along the bone line J.neck1 -> J.neck2 -> J.head, each lofted along its own axis in
// the tilted part frame (azhdaha_pose NECK_TILT: the part's -z runs down the bone), so a sloping neck shows no ring
// steps: local a along the axis (0 = the joint, - toward the head), sections [half width, half height] tapering, the
// centre a little up at the root. neck1 runs from deep inside the hump to past the neck2 joint, neck2 from behind its
// joint into the back of the head (the head region's atlas J.head); painted and light-corrected like the torso.
const vlen = v => Math.hypot(...v);
const NL1 = vlen(J.neck2.map((x, i) => x - J.neck1[i])), NL2 = vlen(J.head.map((x, i) => x - J.neck2[i]));
const NA1 = [1.05, -1.3 * NL1], NA2 = [.42, -1.35 * NL2];
BARRELS.neck1 = {bone: 'neck1', local: true, tilt: NECK_TILT.neck1, neck: true, caps: '+', seed: 41, W: 128, H: 48,
  zs: [0, 1, 2, 3, 4].map(i => NA1[0] + (NA1[1] - NA1[0]) * i / 4),
  sec: a => { const t = Math.max(0, Math.min(1, (NA1[0] - a) / (NA1[0] - NA1[1]))), w = 1.58 - .2 * t, h = 1.0 - .2 * t; return {r: [w, h, w, h], cy: .08 * (1 - t), box: .12}; }};
BARRELS.neck2 = {bone: 'neck2', local: true, tilt: NECK_TILT.neck2, neck: true, caps: '+', seed: 43, W: 128, H: 48,
  zs: [0, 1, 2, 3, 4].map(i => NA2[0] + (NA2[1] - NA2[0]) * i / 4),
  sec: a => { const t = Math.max(0, Math.min(1, (NA2[0] - a) / (NA2[0] - NA2[1]))), w = 1.38 - .33 * t, h = .84 - .18 * t; return {r: [w, h, w, h], cy: 0, box: .12}; }};
const neck1 = () => barrel('neck1'), neck2 = () => barrel('neck2');

// ---- torso paint ------------------------------------------------------------------------------------------------------------
// Hide (v3 f0720 / f1170 close-ups): smooth warm grey-brown skin, not pebbly: big soft light / dark masses, a fine grain,
// faint wrinkle lines, a few low warts on the shoulders and the rump (u, v in px at 32 ppb). Lifted one step over the
// footage (game light is 0.4-1.0 of the albedo).
const SKIN = ramp(['#9A8A6E', '#837358', '#6E5F48', '#5A4D3B', '#463C2E', '#30291F']);
const hideR = SKIN;
function tzHide(u, v, {seed = 3, base = .36, warts = 0} = {}) {
  const m1 = N.e(u * .012 + seed, v * .012), m2 = N.a(u * .035 + seed * 3, v * .035), m3 = N.c(u * .25 + seed, v * .25);
  let t = base + .22 * (m1 - .5) + .1 * (m2 - .5) + .035 * (m3 - .5);
  // wrinkles: thin wavy lines, slightly darker with a lit lip above
  const w = Math.abs(N.f(u * .022 + seed, v * .06) - .5);
  if (w < .012) t += .07 * (1 - w / .012); else if (w < .022) t -= .025 * (1 - (w - .012) / .01);
  let col = SKIN(clamp(t, .03, .97));
  if (warts > 0) {
    const c = cells(u / 11, v / 11, seed + 9, 0, .8), cl = cells((u - 1.5) / 11, (v - 1.5) / 11, seed + 9, 0, .8);
    if (c.id < warts && c.d1 < .3) col = SKIN(clamp(t - .9 * (cl.d1 - c.d1) + .06 * c.d1 / .3, .03, .97));
  }
  return mix(col, SKIN(.15), .12 * smooth(.6, .9, N.b(u * .05 + seed, v * .05)));     // pale dust
}
// Scutes: the band of big domed scales along the hide / plastron boundary (v3 f1170 / f0720: dark grey-brown cobbles,
// two staggered rows, densest behind the shoulder and in front of the hip). z, h in blocks along the body and up from
// the band's foot; returns null between scales.
function scutePx(z, h, dens = 1) {
  const row = Math.floor(h / .22), zz = z / .4 + .5 * row, c = cells(zz, (h - row * .22) / .22 + row, 17, 0, .4);
  if (c.id > dens || h < 0 || h > .44) return null;
  const r = .5 + .12 * c.id, e = c.d1 / r;
  if (e > 1) return null;
  const cl = cells(zz + .06, (h - row * .22 - .03) / .22 + row, 17, 0, .4), lit = cl.d1 - c.d1;
  let col = mix(C('#8A7864'), C('#433729'), clamp(.4 - 3 * lit + .55 * e * e));
  if (e > .8) col = mix(col, C('#241C15'), (e - .8) / .2 * .9);
  return col;
}
// Painted glyphs: broad soft reddish-brown bands (v3 f0720 hip, v3 f1170 behind the shoulder): a two-turn square spiral
// with rounded corners, strokes 0.17 b, faded at the edges. GLYPHS[part]: [z of the left edge, y of the foot, height].
const SPIRAL = stroke([[0, .2], [0, 1], [1, 1], [1, 0], [.3, 0], [.3, .7], [.7, .7], [.7, .35], [.5, .35]], () => 0);
const STRIPE = stroke([[-1.42, 4.12], [-1.62, 3.72], [-1.6, 3.3], [-1.38, 3.02]], () => 0);   // world (z, y), behind the shoulder
const GLYPHS = {belly: [[-.85, 3.02, 1.0]], pelvis: [[3.55, 2.92, .62]], chest: []};
function glyphAt(P, z, y) {
  let a = 0;
  for (const [z0, y0, h] of GLYPHS[P]) {
    const u = (z - z0) / h, v = (y - y0) / h;
    if (u < -.3 || u > 1.3 || v < -.3 || v > 1.3) continue;
    a = Math.max(a, smooth(.1, .068, SPIRAL.near(u, v).d * h));
  }
  if (P === 'belly' || P === 'chest') a = Math.max(a, .8 * smooth(.11, .07, STRIPE.near(z, y).d));
  return a;
}
// The wrap painter of barrel P: (u, v) -> the world point on the smooth surface, its hide / scute / glyph albedo and the
// light correction for the facet that shows it.
function barrelPainter(P) {
  const {zs} = BARRELS[P], z0 = zs[0], z1 = zs[zs.length - 1];
  return (u, v) => {
    const k = Math.min(WRAP_N - 1, Math.floor(u * WRAP_N)), s = u * WRAP_N - k, th = (k + s - .5) * 22.5, z = z0 + v * (z1 - z0);
    const S = secAt(P, z), h = supp(S, th), x = h * Math.cos(th * D2R), y = S.cy + h * Math.sin(th * D2R), side = Math.abs(Math.cos(th * D2R));
    const ny = smoothNy(P, th, z);
    // skin; low warts over the shoulders and the rump; darker along the spine (under the plates); a soft shadow band
    // over the scute row
    const U = 2.7 * th * D2R * 32, V = z * 32, wz = smooth(-1.2, -2.2, z) + smooth(3.0, 4.2, z);
    let col = tzHide(U + 40, V + 300, {warts: .55 * wz});
    col = mix(col, SKIN(.8), .3 * smooth(.6, .95, Math.sin(th * D2R)));
    const hb = y - S.cy + .16 - .14 * Math.exp(-(((z + 1.0) / .7) ** 2)) - .1 * Math.exp(-(((z - 1.5) / .6) ** 2)) + .05 * Math.sin(z * 2.3);
    col = mix(col, SKIN(.7), .3 * smooth(.95, .45, hb) * smooth(.3, .5, hb));
    // form: occlusion round the upper arm (z -2.9..-1.3) and the haunch (z 1.4..3.6) where they leave the barrel, a
    // lit rib-cage bulge between them
    const torso = !BARRELS[P].neck;
    const ao = !torso ? 0 : Math.max(Math.exp(-(((z + 2.1) / .9) ** 2) - ((y - 3.0) / .8) ** 2), Math.exp(-(((z - 2.5) / 1.0) ** 2) - ((y - 2.7) / .8) ** 2));
    col = mix(col, SKIN(.82), .35 * ao * side);
    if (torso) col = mix(col, SKIN(.12), .18 * Math.exp(-(((z - .2) / 1.1) ** 2) - ((y - 3.35) / .45) ** 2) * side);
    const g = torso ? glyphAt(P, z, y) : 0;
    if (g && side > .25) col = mix(col, mix(C('#7A4A33'), C('#6A3E2A'), N.c(z * 3, y * 3)), .72 * g);
    // the scute row along the boundary; under it the crease where the plastron starts (cream below)
    if (side > .5 && torso) {
      const dens = .55 + .45 * smooth(-2.4, -1.4, z) * smooth(2.6, 1.6, z) + .3 * smooth(3.4, 2.8, z);
      const sc = scutePx(z + (x < 0 ? 7 : 0), hb, dens);
      if (sc) col = sc;
      if (hb < -.02) col = hb < -.09 ? PAL.cream(.15 + .1 * smooth(-.2, -.1, hb)) : mix(C('#2C231B'), PAL.cream(.4), smooth(-.02, -.09, hb));
    }
    return scale(col, LIGHTK(ny, faceNy(P, k)));
  };
}
// Plastron fold tiles (u across the facet, 0 = lower edge .. 1 = upper edge; v along the body): n broad lengthwise rolls
// per facet (v3 f1170: pale sage-cream, soft lumps), each lit along its upper third and shaded into a crease at its
// lower edge; beads = the row of small round knobs along the top roll (under the scutes); cross cracks (the Pyro look
// lights them, v9 f0330; Hydro a faint blue). Painted pale: the plastron faces down and the game lights it at the
// ambient 0.4 only.
const BELLY = ramp(['#E6E1CC', '#D2CCB3', '#B9B399', '#9A947C', '#77725E', '#55513F']);
function foldPx(look, n, beads = false) {
  const L = look ? LOOK_PAL[look] : null, R = BELLY;
  return (s, t) => {
    const v = t * 64, i = Math.min(n - 1, Math.floor(s * n)), x = s * n - i;
    const lit = smooth(.4, .85, x) * smooth(1.03, .88, x);
    let tt = .1 - .1 * lit + .14 * smooth(.3, 0, x) + .05 * (N.b(s * 3 + i, v * .05) - .5) + .04 * (N.e(s * 7 + i, v * .2) - .5);
    const p = cells(x * 2.2 + i * 3, v / 18, 5 + i, 0, .7);
    if (p.d1 < .3 && p.id > .62) tt -= .07 * (1 - p.d1 / .3);
    let col = R(clamp(tt, 0, .95));
    if (x < .08) col = mix(col, R(.8), .7 * (1 - x / .08));
    if (beads && x > .66) {
      // a row of round knobs (0.12 b) along the top of the roll
      const bz = v / 4.2, bi = Math.round(bz), dx = (bz - bi) * 4.2 / 32, dy = (x - .83) * .12 * n, d = Math.hypot(dx, dy) / .06;
      if (d < 1) col = R(clamp(.08 + .35 * d * d - .12 * (dy > 0 ? 1 : 0), 0, .9));
    }
    // cross cracks: a zigzag across the roll every ~0.9 b, offset per roll
    const zz = Math.abs(((v / 29 + .37 * i) % 1 + 1) % 1 - .5 + .07 * Math.sin(s * 19 + v * .3));
    if (zz < .022) col = look === 'pyro' ? L.glow(.12 + zz * 14) : look === 'hydro' ? mix(col, L.glow(.35), .5) : mix(col, R(.45), .4);
    else if (zz < .045 && look === 'pyro') col = mix(col, L.glow(.55), .45);
    return col;
  };
}
// light-corrected ledge tiles: the hide / cream seen on a ledge (facing along the body: the game gives it F(0)),
// scaled to the light the smooth surface there would get (never brighter than the albedo: no light stripes)
const ledgePx = (j, cream) => (s, t) => scale(cream ? BELLY(clamp(.12 + .1 * N.b(s * 4 + j, t * 4), 0, 1)) : tzHide(s * 32 + 9 * j, t * 32 + 50), Math.min(1, LIGHTK(j / 4 - 1, 0)));

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
const AP_FOLD = -.78;                                    // the band split (apron frame v)
const lobe = u => { const k = Math.round(u / .41), d = (u - k * .41) / .205; return .075 * Math.sqrt(Math.max(0, 1 - d * d)); };
const apronHem = u => -1.7 + .5 * Math.pow(Math.min(1, u / 2.05), 2.2) - lobe(u);
const apronW = v => 1.22 + .83 * smooth(.6, -.5, v);
const apronSd = (u, v) => Math.max(u - apronW(v), v - (.84 - .1 * Math.min(1, u / 1.22) ** 2), apronHem(u) - v);
function apronEls(sprite, {tint = false, glow = false} = {}) {
  const half = [];
  let px = 0, pz = AZ0;
  for (const [u0, u1, deg] of AP_STRIPS) {
    // strip in its own unrotated frame: X = u - shift on the plane z = pz, turned by deg about the pivot (px, pz); two
    // bands: the lower one (below v -0.78) stands 0.12 b proud, the sagging convex belly of the apron (v3 f2070)
    const shift = u0 - px, rect = {u0: AP.u0 - shift, u1: AP.u1 - shift, v0: AP.v0, v1: AP.v1};
    for (const [vlo, vhi, dz] of [[AP_FOLD, AP.v1, 0], [AP.v0, AP_FOLD, -.12]])
      // only the centre strip has a box core (thickness seen from below); the turned strips are card pairs, whose
      // eroded cores read as stair-stepped edges from the side (r1_critique 1.11)
      half.push(...slab({plane: 'z', at: pz + dz, rect, sd: (X, v) => apronSd(X + shift, v), half: deg ? .015 : .09, sprite, edge: 'cream', cell: .14, inset: 1.2,
        clip: {u0: px, u1: px + (u1 - u0), v0: vlo, v1: vhi}, core: !glow && !deg, cards: glow ? '-' : 'both', tint, eps: glow ? .028 : .012,
        rot: deg ? ['y', deg, [px, 0, pz]] : null}));
    px += (u1 - u0) * Math.cos(deg * D2R); pz += (u1 - u0) * Math.sin(deg * D2R);
  }
  const els = [...half, ...mirrorX(half)];
  // the gold drop spike hanging under the centre lobe (added after the mirror: it sits on the midline)
  if (!glow) els.push(...blade([.005, apronHem(0) + .06, AZ0 - .15], 'z', 0, .42, 3, true));
  return els;
}
// glyph polylines (half apron, u >= 0): zigzag grooves, the centre spine, V folds and meander hooks
const zig = (u, v0, v1, amp, per, ph = 0) => { const pts = []; for (let v = v0; v >= v1 - 1e-6; v -= per / 2) { const k = Math.round((v0 - v) / (per / 2)); pts.push([u + ((k + ph) % 2 ? amp : -amp), v]); } return pts; };
const meander = (cu, cv, r) => [[cu - r, cv + r], [cu + r, cv + r], [cu + r, cv - r], [cu - r * .45, cv - r], [cu - r * .45, cv + r * .3], [cu + r * .35, cv + r * .3], [cu + r * .35, cv - r * .4]];
const sway = (u, v0, v1, amp, per, ph = 0) => { const pts = []; for (let v = v0; v >= v1 - 1e-6; v -= .06) pts.push([u + amp * Math.sin((v0 - v) / per * 2 * Math.PI + ph), v]); return pts; };
const AP_LINES = [
  [[.04, .8], [.04, -1.42]],
  [[.28, .72], [.28, -.55], ...zig(.28, -.55, -1.3, .085, .38).slice(1), [.4, -1.42], [.5, -1.34]],
  zig(.6, .58, -1.52, .11, .66, 1),
  [[.95, .4], [.95, -.18], [1.12, -.18], [1.12, -.42], [.86, -.42], ...zig(.86, -.42, -1.12, .05, .3).slice(1)],
  sway(1.3, .12, -1.38, .07, 1.1),
  zig(1.66, -.28, -1.12, .065, .42, 1),
  meander(1.52, .34, .18), meander(1.86, -.6, .11), meander(.6, -1.62, .1),
].map(pts => stroke(pts, () => 0));
const apronLine = (u, v) => Math.min(...AP_LINES.map(S => S.near(u, v).d));
function apronBumps(u, v) {
  // big round pebble bumps over the lower half (denser toward the hem and the sides); returns the light term or null
  if (v > -.55) return null;
  const c = cells(u / .34, v / .3, 31, 0, .75), dens = smooth(-.55, -1.45, v) * (.75 + .25 * smooth(.6, 1.8, u));
  if (c.id > .2 + .65 * dens) return null;
  const r = .3 + .14 * c.id;
  if (c.d1 > r) return null;
  const cl = cells((u + .035) / .34, (v - .035) / .3, 31, 0, .75);
  return {lit: (cl.d1 - c.d1) * 5, rim: c.d1 / r};
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
// Sheet: 6 cells of 64 x 128 (aspect 1:2): 0-2 side profiles (upright, the tip curling back), 3-5 front faces: 3 a
// straight leaf (the central row), 4-5 feathers whose tip bends outward (side rows; mirrored on the left), with a dark
// mid-rib and amber chevron veins (v4 f0900).
const BLADES = [
  {kind: 's', tip: .2, w: .38}, {kind: 's', tip: .12, w: .34, orange: true}, {kind: 's', tip: .28, w: .4},
  {kind: 'f', w: .42}, {kind: 'f', w: .36, bend: .16, orange: true}, {kind: 'f', w: .34, bend: .24},
];
const SHEET = {cw: 64, ch: 128, n: BLADES.length};
const AS = .5;   // cell aspect (width / height)
const bladeW = (b, t) => (b.kind === 'f' ? (t < .32 ? .55 + .45 * t / .32 : Math.pow((1 - t) / .68, .8)) : 1.2 * (t < .38 ? .5 + .5 * t / .38 : Math.pow((1 - t) / .62, .9)));
const BL = BLADES.map(b => {
  const x0 = b.kind === 'f' ? .5 : .38, top = b.kind === 'f' ? .95 : 1;
  const pts = Array.from({length: 17}, (_, i) => { const t = i / 16; return [(x0 + (b.tip || 0) * smooth(.5, 1, t) * t + (b.bend || 0) * t * t) * AS, t * top]; });
  const S = stroke(pts, t => b.w * AS * bladeW(b, t));
  return {...b, S, sd: (x, y) => S.sd(x * AS, y)};
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
  if (across < (b.kind === 'f' ? .07 : .05)) c = mix(c, R(.95), .65);                       // the dark mid-rib
  if (Math.abs(((n.t * 8 + across * 1.6) % 1) - .5) < .045 && across > .28) c = mix(c, R(.9), .3);
  if (!LP) {
    // amber veins: chevrons rising from the rib on the faces, streaks along the ridge on the profiles (v4 f0900)
    if (b.kind === 'f') { const ph = ((n.t * 6.5 - across * 1.5) % 1 + 1) % 1;
      if (across > .1 && across < .82 && n.t > .05 && n.t < .82 && Math.abs(ph - .5) < .075) c = mix(c, PAL.plateOr(.2 + .5 * n.t), .7 * (1 - .8 * n.t));
    } else if (across > .12 && across < .5 && Math.abs(((across * 5 + n.t * .6) % 1) - .5) < .06 && n.t > .08 && n.t < .7) c = mix(c, PAL.plateOr(.35 + .4 * n.t), .45 * (1 - n.t));
  }
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
// One plate in its group frame: base [x, y, z], length L, side / front cells, splay (deg about Z; - tips toward +X),
// front width factor; flip: the front face mirrored (the left side rows, so their feather tips bend outward too).
function plate(spr, [x, y, z], L, ks, kf, splay = 0, wf = 1, flip = false) {
  const W = L * AS, Wf = L * AS * .9 * wf, rot = splay ? ['z', splay, [x, y, z]] : undefined;
  const side = cardX(spr, x, {Z0: z - .38 * W, Z1: z + .62 * W, Y0: y, Y1: y + L}, {rot});
  const front = cardZ(spr, z, {X0: x - Wf / 2, X1: x + Wf / 2, Y0: y, Y1: y + L * .95}, {rot, uvr: [0, .05, 1, 1], flipU: flip});
  cellUV([side], spr, ks, SHEET.n); cellUV([front], spr, kf, SHEET.n);
  // a thin dark core (the plate's thickness seen edge-on), kept low so its top face stays inside the plate's shadow
  const core = rockBox([x - .04, y, z - .06], [x + .04, y + L * .3, z + .06], spr === 'plates' ? 'plate' : spr.replace('plates', 'plate'), {rot});
  return [side, front, core];
}
// Plate layout per group in WORLD coordinates (rest, before the group lean): [x, base y, z, L, side cell, front cell,
// splay, front width]; entries with |x| > 0.1 are mirrored. Bases sit about 0.25 b inside the hide.
const G = {
  neck: {base: 'plN', g: 'neck', list: [[.02, 3.2, -3.05, 2.3, 0, 3, 0, 1], [.55, 3.12, -2.95, 2.1, 2, 4, -22.5, 1], [1.05, 2.88, -2.8, 1.9, 1, 5, -45, .9],
    [1.4, 2.5, -2.62, 1.5, 0, 5, -45, .8]]},
  sh: {base: 'plS', g: 'sh', list: [[.03, 4.1, -2.3, 3.2, 0, 3, 0, 1.15], [-.04, 4.0, -2.85, 1.8, 1, 3, 0, 1], [.72, 4.05, -1.75, 3.15, 2, 4, -22.5, 1.15],
    [1.45, 3.78, -1.95, 2.5, 1, 5, -45, 1.1]]},
  mid: {base: 'plM', g: 'mid', list: [[.05, 4.1, .1, 3.15, 2, 3, 0, 1.1], [-.05, 4.12, -.6, 1.9, 1, 3, 0, 1], [.75, 4.0, .45, 2.95, 0, 4, -22.5, 1.15],
    [1.5, 3.72, .2, 2.3, 1, 5, -45, 1.05]]},
  hip: {base: 'plH', g: 'hip', list: [[-.09, 3.82, 1.3, 2.75, 0, 3, 0, 1.1], [.03, 3.62, 2.4, 2.4, 2, 3, 0, 1], [-.03, 3.4, 3.65, 2.0, 1, 3, 0, .9],
    [.09, 3.15, 4.4, 1.7, 0, 3, 0, .8], [.7, 3.7, 2.2, 2.3, 2, 4, -22.5, 1], [.68, 3.45, 3.3, 1.8, 1, 5, -22.5, .9], [1.35, 3.45, 2.6, 1.6, 0, 5, -45, .9]]},
};
function plateGroup(key, spr) {
  const {base, g, list} = G[key], B = J[base], Ri = q([-PLATE_LEAN[g], 0, 0]), els = [];
  for (const [x, y, z, L, ks, kf, sp, wf] of list) for (const sx of Math.abs(x) > .1 ? [1, -1] : [1]) {
    const p = rot(Ri, [sx * x - B[0], y - B[1], z - B[2]]);
    els.push(...plate(spr, p, L, ks, kf, sx * sp, wf, sx < 0));
  }
  return els;
}

// ---- gold crystals (model.md §3.6; r1_critique 3.4): trident / bird clusters along the crest's lower edge ---------------------
// One cluster = 1-3 slender gold blades fanned from one root: some turned outward about Z (they read as the spikes
// radiating from the shoulders in the front view, v4 f0900), some tipped back about X (the spikes pointing up and back
// through the crest in the side view, v8 f2256). Each blade is a crossed pair of cards along its own axis (a side card,
// plane x, and a front card, plane z, both carrying the blade's rotation), so it has a solid needle silhouette from
// every side instead of a flat painted fan. Sheet: 4 cells of 48 x 128 (aspect 3:8): 0 a pointed blade, 1 a blade with a
// side barb (the trident's prong), 2 a slender needle, 3 the broad shoulder spike. Gold ramp, a lit and a shaded half
// either side of the bright ridge, darker amber edges.
const SHARD_CELLS = [{w: .42}, {w: .38, barb: true}, {w: .3}, {w: .46, facet: true}];
const SAS = .375;  // shard cell aspect (width / height): broad leaf blades, 0.2-0.5 b wide (v3 f0720, f1170)
const shardW = (t, s) => s.w * (t < .2 ? .6 + .4 * t / .2 : Math.pow((1 - t) / .8, .85)) + .004;
const SHC = SHARD_CELLS.map(s => {
  const S = stroke(Array.from({length: 9}, (_, i) => [.5 * SAS, .02 + .96 * i / 8]), t => SAS * shardW(t, s));
  const B = s.barb ? stroke([[.55 * SAS, .4], [.86 * SAS, .62]], t => SAS * .11 * (1 - t) + .003) : null;
  return {...s, S, B, sd: (x, y) => Math.min(S.sd(x * SAS, y), B ? B.sd(x * SAS, y) : 9)};
});
function shardColour(k, x, y) {
  const s = SHC[k], d = s.sd(x, y);
  if (d > 0) return null;
  const onB = s.B && s.B.sd(x * SAS, y) < s.S.sd(x * SAS, y), n = (onB ? s.B : s.S).near(x * SAS, y), lit = n.s > 0;
  let c = goldPx(lit ? .08 + .22 * n.t : .45 + .2 * n.t, x * 20, y * 80);
  if (s.facet && Math.abs(n.s) > .45 * SAS * shardW(n.t, s)) c = mix(c, PAL.gold(lit ? .2 : .7), .5);   // two bevel facets a side
  if (d > -.007) c = PAL.gold(lit ? .62 : .85);                    // darker amber edges
  else if (Math.abs(n.s) < .005 && n.t < .95) c = PAL.gold(0);     // the bright ridge
  return c;
}
const shardSheet = (s, t) => { const k = Math.min(3, Math.floor(s * 4)); return shardColour(k, s * 4 - k, 1 - t) || TRANSPARENT; };
const shardUV = (els, k) => { for (const e of els) for (const f of Object.values(e.faces)) if (f.texture === '#shards') { const [a, b, c2, d] = f.uv; f.uv = [k * 4 + a / 4, b, k * 4 + c2 / 4, d].map(v => +v.toFixed(4)); } return els; };
// One blade from the root [x, y, z]: axis 'z' (deg < 0 tips toward +X) or 'x' (deg > 0 tips back, +Z), length L, cell k.
// down: the blade hangs from its root (the apron's drop spike).
function blade([x, y, z], axis, deg, L, k, down = false) {
  const w = L * SAS / 2, rot = deg ? [axis, deg, [x, y, z]] : undefined, Y0 = down ? y - L : y, Y1 = down ? y : y + L, uvr = down ? [0, 1, 1, 0] : [0, 0, 1, 1];
  return shardUV([cardX('shards', x, {Z0: z - w, Z1: z + w, Y0, Y1}, {rot, uvr}), cardZ('shards', z, {X0: x - w, X1: x + w, Y0, Y1}, {rot, uvr})], k);
}
// [x, y, z, [[axis, deg, L, cell], ...]]: world rest positions of the right-hand roots (mirrored), about 0.2 b inside
// the hide; the tips reach 4.7-5.3 b (model.md §1: shoulder crystal tips 0.67 H) and stay within the crystal parts' R1 reach
// (PART_SCALE crys_*: x <= 3.3 b / 3.0 b at the hips), inside the shoulder span of the fore legs.
const CRYS = {
  sh: {base: 'plS', list: [
    [1.85, 3.86, -2.0, [['z', -45, 1.7, 3], ['x', 22.5, 1.35, 1], ['z', -22.5, 1.15, 2]]],
    [1.72, 4.0, -1.05, [['z', -22.5, 1.7, 1], ['x', 45, 1.2, 0], ['z', -45, 1.0, 2]]],
    [2.3, 3.4, -2.62, [['z', -45, 1.1, 0], ['z', -22.5, .85, 2]]],
    [1.55, 4.02, -2.6, [['z', -22.5, 1.3, 2], ['x', 22.5, .95, 0]]]]},
  mid: {base: 'plM', list: [
    [2.0, 3.78, .0, [['z', -45, 1.45, 1], ['x', 22.5, 1.25, 0], ['z', -22.5, 1.0, 2]]],
    [1.78, 3.9, 1.0, [['z', -22.5, 1.4, 0], ['x', 45, 1.1, 2]]],
    [2.4, 3.2, .62, [['z', -45, 1.0, 2]]]]},
  hip: {base: 'plH', list: [
    [1.86, 3.48, 2.1, [['z', -45, 1.3, 1], ['x', 22.5, 1.15, 0]]],
    [1.6, 3.4, 3.1, [['z', -22.5, 1.2, 0], ['x', 45, 1.0, 2]]],
    [2.12, 3.0, 2.8, [['z', -45, .95, 2]]]]},
};
function crystalGroup(g) {
  const {base, list} = CRYS[g], B = J[base], els = [];
  for (const [x, y, z, blades] of list) for (const s of [1, -1]) for (const [ax, deg, L, k] of blades)
    els.push(...blade([s * x - B[0], y - B[1], z - B[2]], ax, ax === 'z' ? s * deg : deg, L, k));
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
    glow_apron: {geo: 'empty', hydro: 'glow_apron_hydro', pyro: 'glow_apron_pyro'},
  },
  tail: Object.fromEntries(['plates_neck', 'plates_sh', 'plates_mid', 'plates_hip'].map(p => [p, {geo: p, cryo: p + '_cryo', electro: p + '_electro'}])),
};
export const TINTED = {glow_apron_hydro: ['glow_apron', LOOK_PAL.hydro.tint], glow_apron_pyro: ['glow_apron', LOOK_PAL.pyro.tint]};
// brightness per look (the bright parts of a look; others keep their PARTS level)
// the plates stay dark stone in phase 3 (only the painted rims glow): no full-bright plate parts (r1_critique 3.7)
export const LOOK_BRIGHT = {legs: {hydro: {belly: 13}, pyro: {belly: 14, chest: 14, pelvis: 14}}, tail: {cryo: Object.fromEntries(Object.keys(LOOKS.tail).map(p => [p, 14])), electro: Object.fromEntries(Object.keys(LOOKS.tail).map(p => [p, 14]))}};

export function sprites() {
  const S = {};
  const card = (name, rect, ppb, fn, tr = false) => { const [w, h] = spriteSize(rect, ppb); S[name] = [w, h, onRect(rect, fn), tr]; };
  card('apron', AP, 80, apronPaint(null));
  card('apron_mask', AP, 80, apronMask, true);
  S.plates = [SHEET.cw * SHEET.n, SHEET.ch, plateSheet(null), false];
  S.plates_cryo = [SHEET.cw * SHEET.n, SHEET.ch, plateSheet('cryo'), false];
  S.plates_electro = [SHEET.cw * SHEET.n, SHEET.ch, plateSheet('electro'), false];
  S.shards = [192, 128, shardSheet, false];
  for (const P of Object.keys(BARRELS)) S['tw_' + P] = [BARRELS[P].W, BARRELS[P].H, barrelPainter(P), false];
  for (const l of [null, 'hydro', 'pyro']) { S['tz_pl' + sfx(l)] = [64, 64, foldPx(l, 1), false]; S['tz_pl1' + sfx(l)] = [64, 64, foldPx(l, 1, true), false]; S['tz_plb' + sfx(l)] = [64, 64, foldPx(l, 3), false]; }
  for (const j of LEDGE_H) S['tz_lh' + j] = [32, 32, ledgePx(j, false), false];
  for (const j of LEDGE_C) S['tz_lc' + j] = [32, 32, ledgePx(j, true), false];
  return S;
}
