// TAIL region of the 아펩의 오아시스 파수꾼 rig (plan R4 parts 40-47; model.md §3.6, model_p3.md §2.4 item 24, §3 item 7):
// the twisted two-band ribbon tail, 9.1 b in both forms, 7 segments + the tip.
//
// THE RIBBON (v2 f1125 / f1135 / f1260, v5 f1875, v6 f140 / f165): two flat straps wound round each other like a two-ply
// strap, a broad PALE strap (slot band_a: P1 #C9C6B4 pale bark, P3 pale grey-white) and a narrower DARK strap (slot
// band_b: P1 slate #4B5348, P3 dark green), with see-through windows between them. They wind round a flattened
// elliptic tube (0.72 x 0.45 b at the root, 0.3 x 0.19 b at the tip joint: a ribbon, not a round tube), so the
// envelope keeps its width from every side while the bands cross diagonally.
//   * Geometry: the tube is a 16-facet prism circumscribing the ellipse, facet normals on the 22.5-degree grid (the only
//     element rotations Minecraft allows). Each strap covers the facets within its angular half-width of its centre
//     angle; the centre angle turns with the arc length s from the root (pitch 1.45 b at the root tightening to 1.0 b at
//     the tip joint). So every facet is covered by a strap over one z-interval per turn, and each such interval is ONE
//     slat element (a thin plate on the facet, as long as the strap crossing): the strap edges step diagonally one
//     facet at a time, and the strap paint (its dark cel outline, lit centre) maps across the slat's length.
//   * Joints: the twist phase runs on s, so it is continuous across the segment joints; the roll of each segment's
//     authoring frame against the previous one (the previous frame parallel-transported across the bend) is folded into
//     the phase. Each segment's slats run 0.14 b past its end joint (filling the wedge on the outside of a bend);
//     neighbouring segments sit 0.012 b apart in radius (odd segments inside) so the overlaps never share a plane.
//     tail_1 starts 0.2 b inside the abdomen (under its sheath).
//   * THE ROOT SHEATH (v2 f1260 / f1275 / f1290, v5 f1890, MP3 §3 item 8): tail_1 and tail_2 up to z 0.92 wear 7 rings of
//     shingled scale plates (16 facet plates per ring, round 0.94 x 0.84 b at the root flattening to 0.76 x 0.53 b),
//     each ring smaller than the one before by more than the plate thickness so it slides under the previous ring's
//     cut-out scale tips; the straps start under the last ring. A frill of 7 pale jagged leaf fins (radial planes)
//     stands round the root where the tail leaves the body (the pale flaps of v2 f1260).
//   * Paint: two grey tiles tinted per form (g_tail_a pale, g_tail_b dark; 128 x 304 px). Rows 0-191: four alpha-cut band
//     variants (u along the strap, 8 px per facet, 16 facets per period; the slat ends slant with the strap edge); 192-239:
//     a solid strip (v across the strap) for the scroll and the whip: the dark outline at both strap edges, a lit band
//     and a sheen line on the pale strap with faint wood-grain swirls, a lit centre ridge on the dark one. g_tail_a
//     240-271: the sheath ring (two staggered rows of six pointed grey shield scales with outlines, lit front bevels,
//     white studs and cracks on the pale ground, the back row's tips cut out); 272-303: four frill leaves. g_tail_b
//     240-271: the scythe crescent (272-303 clear).
//   tail_7    P1 = the plain segment; P3 = tail_7_p3: the pale strap ends in a leaf point and the dark one closes, the
//             dark whip (a flattened taper) emerging from inside them.
//   tail_tip  P1 (v2 f1260 / f1275 / f1245): the pale strap ramps off the tail top and rolls forward and under into a
//             spiral scroll (outer turn r 0.21 b + an inner 3/4 turn), resting just over the ground; the dark strap ends
//             under it and the scythe blade (an alpha-cut crescent card standing on its edge, 2 b long) runs back from
//             under the scroll along the ground beside the tail, angled 22.5 deg away from it. P3 (v6 f140, v5 f1875):
//             the dark whip runs on to a point 1.45 b past the tip joint (2.2 b of whip in all).
// Frames (apep_pose FRAMES): every tail part is authored in its bone frame 'z' at the CROUCH stance (+Z along the
// segment toward the next joint, +Y = world up made perpendicular; the joint at the origin) and serves both forms.
// Region interface: see apep_body.mjs.
import {toUnits, registerTile} from './mboss_shape_lib.mjs';
import {faceEl} from './mboss_model_lib.mjs';
import {PART_SCALE, TAIL_C, solve, modelFrames} from './apep_pose.mjs';
import {STANCES} from './apep_clips.mjs';
import {mul, rot} from './mboss_rig_math.mjs';
import {clamp, smooth, N, autoSlot, sprite, grey, TRANSPARENT} from './apep_materials.mjs';

export const REGION = 'tail';
export const PARTS = ['tail_1', 'tail_2', 'tail_3', 'tail_4', 'tail_5', 'tail_6', 'tail_7', 'tail_tip'];
const SEG = PARTS.slice(0, 7);
const D2R = Math.PI / 180;
const sub = (a, b) => a.map((x, i) => x - b[i]), dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const unit = v => { const l = Math.hypot(...v); return v.map(x => x / l); };
const LEN = TAIL_C.slice(0, 8).map((p, i) => Math.hypot(...sub(TAIL_C[i + 1], p)));
// arc length of each joint from the root (S0[i] = the start of part i; S0[7] = the tip joint)
const S0 = LEN.reduce((a, l) => [...a, a[a.length - 1] + l], [0]);
const LT = S0[7];
// ---- the authoring frames at CROUCH (apep_pose authorFrame, kind 'z', up hint [0, 1, 0]) and the roll offsets ------------
const FR = TAIL_C.slice(0, 8).map((p, i) => {
  const Z = unit(sub(TAIL_C[i + 1], p)), Y = unit(sub([0, 1, 0], Z.map(z => z * Z[1]))), X = cross(Y, Z);
  return {X, Y, Z};
});
const turnAbout = (v, a, rad) => { const c = Math.cos(rad), s = Math.sin(rad), k = cross(a, v), d = dot(a, v); return v.map((x, i) => x * c + k[i] * s + a[i] * d * (1 - c)); };
const ROLL = [0];
for (let i = 0; i < 7; i++) {
  const A = FR[i], B = FR[i + 1], ax = cross(A.Z, B.Z), sn = Math.hypot(...ax);
  const Xt = sn < 1e-9 ? A.X : turnAbout(A.X, ax.map(x => x / sn), Math.atan2(sn, dot(A.Z, B.Z)));
  ROLL.push(ROLL[i] + Math.atan2(dot(Xt, B.Y), dot(Xt, B.X)) / D2R);
}
// ---- the joints per form: mitre planes and roll offsets --------------------------------------------------------------------
// A rigid segment chain kinks at its joints; each part's straps end on a MITRE plane per facet (the bisector of the joint
// angle, so the ends meet without a gap on the outside of a bend or a lip on the inside). The bend differs per stance:
// P1 is cut for CROUCH (its only stance); the P3 models serve the crawl (CROUCH) and the UPRIGHT coil (bends 24-44 deg,
// tail_2 / tail_3 twisted 18 deg), so their mitres and roll offsets split the difference between the two stances
// (residual 6-11 deg per joint in either stance, under the 0.035 b overlap).
const TP = PARTS;
const POSE_REF = {CROUCH: solve(STANCES.CROUCH), UPRIGHT: solve(STANCES.UPRIGHT)};
const MF = modelFrames(POSE_REF);
const inv = Q => [-Q[0], -Q[1], -Q[2], Q[3]];
const nrm3 = v => { const l = Math.hypot(...v); return v.map(x => x / l); };
function jointsIn(st) {
  const o = POSE_REF[st], Q = TP.map(n => mul(o[n].R, MF.p1[n]));
  return Array.from({length: 7}, (_, j) => {
    const zj1 = rot(inv(Q[j]), rot(Q[j + 1], [0, 0, 1])), m = nrm3([zj1[0], zj1[1], 1 + zj1[2]]);
    const m1 = rot(inv(Q[j + 1]), rot(Q[j], m));
    // twist: part j's X carried across the bend, measured in part j+1's frame
    const A = {X: rot(Q[j], [1, 0, 0]), Z: rot(Q[j], [0, 0, 1])}, B = {X: rot(Q[j + 1], [1, 0, 0]), Y: rot(Q[j + 1], [0, 1, 0]), Z: rot(Q[j + 1], [0, 0, 1])};
    const ax = cross(A.Z, B.Z), sn = Math.hypot(...ax);
    const Xt = sn < 1e-9 ? A.X : turnAbout(A.X, ax.map(x => x / sn), Math.atan2(sn, dot(A.Z, B.Z)));
    return {end: m, start: m1, roll: Math.atan2(dot(Xt, B.Y), dot(Xt, B.X)) / D2R};
  });
}
const JC = jointsIn('CROUCH'), JU = jointsIn('UPRIGHT');
const avg = (a, b) => nrm3(a.map((x, i) => x + b[i]));
const JOINTS = {p1: JC, p3: JC.map((c, j) => ({end: avg(c.end, JU[j].end), start: avg(c.start, JU[j].start), roll: c.roll + (JU[j].roll - c.roll) / 2}))};
const ROLLF = Object.fromEntries(Object.entries(JOINTS).map(([f, J]) => [f, J.reduce((a, j) => [...a, a[a.length - 1] + j.roll], [0])]));
// the cut z of a mitre plane (normal m through the point at z0) at the cross-section point (x, y)
const cutZ = (m, z0, x, y) => z0 - (m[0] * x + m[1] * y) / m[2];
const OVL = .035;
// ---- the ribbon profile along s ---------------------------------------------------------------------------------------------
// a / b: the tube's semi-axes (left-right / up-down in the segment frame), dA / dB: the pale / dark strap's angular
// half-widths (deg), t: the slat thickness
const A_OF = s => .19 + .23 * Math.pow(clamp(1 - s / LT), 1.1);
const prof = s => { const a = A_OF(Math.min(s, LT)), k = (a - .19) / .23; return {a, b: .62 * a, dA: 74, dB: 50, t: .026 + .014 * k}; };
// twist phase (deg) = the pale strap's centre angle (from +X toward +Y): pitch P(s) = P0 + PK s; PH0 puts the pale strap
// on top (90 deg) at the tail end where the P1 scroll rolls up from it
const P0 = 1.7, PK = (1.15 - 1.7) / LT, turns = s => 360 * Math.log((P0 + PK * s) / P0) / PK;
const CURL_Z = .36;
const PH0 = 90 - turns(LT + CURL_Z) - ROLL[7];
const phase = s => PH0 + turns(s);
const sOfPhase = ph => (P0 * Math.exp(PK * (ph - PH0) / 360) - P0) / PK;
// ---- the 16-facet prism of an ellipse ---------------------------------------------------------------------------------------
// facet k (normal angle 22.5 k deg): h = distance of its plane from the axis, c = tangential offset of its midpoint, len
function facet(a, b, k, step = 22.5) {
  const nrm = j => [Math.cos(j * step * D2R), Math.sin(j * step * D2R)], h = j => Math.hypot(a * nrm(j)[0], b * nrm(j)[1]);
  const vert = j => { const n1 = nrm(j), n2 = nrm(j + 1), h1 = h(j), h2 = h(j + 1), det = n1[0] * n2[1] - n1[1] * n2[0]; return [(h1 * n2[1] - h2 * n1[1]) / det, (n1[0] * h2 - n2[0] * h1) / det]; };
  const v0 = vert(k - 1), v1 = vert(k), e = [-nrm(k)[1], nrm(k)[0]], m = [(v0[0] + v1[0]) / 2, (v0[1] + v1[1]) / 2];
  return {h: h(k), c: m[0] * e[0] + m[1] * e[1], len: Math.hypot(v1[0] - v0[0], v1[1] - v0[1])};
}
// The strap tiles (128 px wide, u along the strap: one 8 px column per facet, 16 per period): rows 0-191 hold four
// alpha-cut BAND variants of RH px, each a parallelogram whose start and end edges slant by DV[r] of the row per facet
// column, so a slat's ends follow the strap's diagonal edge instead of stepping; rows 192-239 are a solid strip (v across
// the strap) for the scroll and the whip. A strap of half-width d (deg) slants by 22.5 / (2 d + 22.5) of its slat.
// tile layout (both strap tiles, TW x TH px, v in 0..16 units = PXV per px): rows 0-191 the four band variants (RH px each),
// 192-239 the solid strip, then g_tail_a: 240-271 the root-sheath scale ring, 272-303 four frill leaves (32 x 32);
// g_tail_b: 240-303 the scythe blade (128 px/b across its height). VS keeps the small v offsets of the 240 px layout on the same pixel rows.
const TW = 128, RH = 48, TH = 304, PXV = 16 / TH, VS = 240 / TH;
const DV = [.15, .2, .3, .45], ROWU = RH * PXV, SOLID = 4 * ROWU, SH0 = 240 * PXV, SHH = 32 * PXV, FR0 = 272 * PXV, FRH = 32 * PXV, BL0 = 240 * PXV, BLH = 64 * PXV;
const rowOf = d => { const x = 22.5 / (2 * d + 22.5); return DV.reduce((b, v, i) => (Math.abs(v - x) < Math.abs(DV[b] - x) ? i : b), 0); };
// One slat: a thin plate on facet k over local z0..z1 (clipped from the full slat Z0..Z1 = the strap crossing plus half
// a facet's slant at each end), band row `row`; inset (b) from the tube surface. Unrotated configuration psi (a multiple
// of 90) + element rotation th (-45 .. 45) about the segment axis. The end faces map to a transparent corner (the cut
// is in the band's slant).
const NAME = {'1,0': 'left', '-1,0': 'right', '0,1': 'up', '0,-1': 'down'};
function slat({k, z0, z1, Z0, Z1, row, F, t, tex, inset = 0, step = 22.5}) {
  const deg = ((k * step) % 360 + 360) % 360;
  let th = ((deg + 45) % 90) - 45;
  const psi = Math.round(deg - th);
  if (Math.abs(th) < 1e-6) th = 0;
  const n = [Math.round(Math.cos(psi * D2R)), Math.round(Math.sin(psi * D2R))], e = [-n[1], n[0]];
  const r = F.h - inset - t / 2, ov = .006, hl = F.len / 2 + ov;
  const c = [n[0] * r + e[0] * F.c, n[1] * r + e[1] * F.c];
  const hx = Math.abs(n[0]) * t / 2 + Math.abs(e[0]) * hl, hy = Math.abs(n[1]) * t / 2 + Math.abs(e[1]) * hl;
  const lo = [c[0] - hx, c[1] - hy, z0], hi = [c[0] + hx, c[1] + hy, z1];
  const ke = ((Math.round(k * step / 22.5) % 16) + 16) % 16, pe = P => ((P[0] - c[0]) * e[0] + (P[1] - c[1]) * e[1]) / (2 * hl) + .5;
  const pn_ = P => ((P[0] - c[0]) * n[0] + (P[1] - c[1]) * n[1]) / t + .5;
  const vOf = P => (row < 0 ? SOLID + ROWU * clamp(pe(P)) : row * ROWU + ROWU * (P[2] - Z0) / (Z1 - Z0));
  const uOf = P => (row < 0 ? ke + clamp((P[2] - Z0) / (Z1 - Z0)) : ke + clamp(pe(P)));
  const face = {tex, fn: P => [uOf(P), vOf(P)]};
  const side = {tex, fn: P => [row < 0 ? uOf(P) : ke + (pe(P) > .5 ? .94 : .04) + .02 * clamp(pn_(P)), row < 0 ? SOLID + (.1 + .2 * clamp(pn_(P))) * VS : vOf(P)]};
  const end = {tex, fn: P => (row < 0 ? [ke + .1 + .2 * clamp(pn_(P)), vOf(P)] : [ke + .85 + .1 * clamp(pe(P)), row * ROWU + (.02 + .03 * clamp(pn_(P))) * VS])};
  const faces = {[NAME[n.join()]]: face, [NAME[n.map(x => -x).join()]]: face, [NAME[e.join()]]: side, [NAME[e.map(x => -x).join()]]: side, front: end, back: end};
  return faceEl([lo, hi], faces, {rot: th ? ['z', th, [0, 0, (z0 + z1) / 2]] : undefined});
}
// The two straps of part i in form f between its start and end cuts (start: z = za, or the mitre of joint i-1; end: the
// mitre of joint i, or z = zb), each facet cut at its own centre point, OVL past each plane.
// shape(s) -> {a, b, dA, dB, t}: a strap whose half-width is under 4 deg is absent there.
function straps(i, f, {za = null, zb = null, shape = prof} = {}) {
  const els = [], s0 = S0[i], roll = ROLLF[f][i], inset = i % 2 ? .012 : 0, J = JOINTS[f];
  const pj = (z, k) => { const p = shape(s0 + z), F = facet(p.a, p.b, k), n = [Math.cos(k * 22.5 * D2R), Math.sin(k * 22.5 * D2R)]; return [n[0] * F.h - n[1] * F.c, n[1] * F.h + n[0] * F.c]; };
  const zaOf = k => (za !== null ? za : (() => { const [x, y] = pj(0, k); return cutZ(J[i - 1].start, 0, x, y) - OVL; })());
  const zbOf = k => (zb !== null ? zb : (() => { const [x, y] = pj(LEN[i], k); return cutZ(J[i].end, LEN[i], x, y) + OVL; })());
  const phiA = phase(s0 - .5) + roll, phiB = phase(s0 + LEN[i] + .5) + roll;
  for (const [tex, off, key] of [['g_tail_a', 0, 'dA'], ['g_tail_b', 180, 'dB']]) {
    for (let k = 0; k < 16; k++) {
      const ctr = k * 22.5 - off, za_ = zaOf(k), zb_ = zbOf(k);
      // the strap (centre = phase + off) covers facet k while phase + roll lies within ctr +- d (+ 360 n)
      for (let nn = Math.floor((phiA - ctr - 180) / 360) - 1; nn <= Math.ceil((phiB - ctr + 180) / 360) + 1; nn++) {
        const mid = ctr + 360 * nn;
        let d = shape(sOfPhase(mid - roll))[key];
        if (d < 4) continue;
        let zs0 = sOfPhase(mid - d - roll) - s0, zs1 = sOfPhase(mid + d - roll) - s0;
        // re-evaluate the half-width at the slat's own centre (straps that taper)
        d = shape(s0 + (zs0 + zs1) / 2)[key];
        if (d < 4) continue;
        // the full slat: the crossing plus half the strap edge's advance over one facet at each end
        const Z0 = sOfPhase(mid - d - 11.25 - roll) - s0, Z1 = sOfPhase(mid + d + 11.25 - roll) - s0;
        const z0 = Math.max(za_, Z0), z1 = Math.min(zb_, Z1);
        if (z1 - z0 < .008) continue;
        const p = shape(s0 + (z0 + z1) / 2), F = facet(p.a, p.b, k);
        els.push(slat({k, z0, z1, Z0, Z1, row: rowOf(d), F, t: p.t, tex, inset}));
      }
    }
  }
  return els;
}
// ---- the root sheath (v2 f1260 / f1290, v5 f1890) -----------------------------------------------------------------------------
// tail_1 and most of tail_2 wear rings of shingled scale plates: 16 facet plates per ring on that ring's ellipse (round at
// the root, flattening toward the ribbon), each ring smaller than the one before by more than the plate thickness, so its
// front slides under the previous ring's cut-out scale tips (no shared planes). The straps start under tail_2's last ring.
// The root ring carries a frill of pale pointed leaf fins (radial planes through the axis) where the tail leaves the body.
const SH_T = .014, STRAP_Z1 = .56;
const SH_RINGS = [[0, -.22, .26], [0, .16, .62], [0, .52, .98], [0, .88, 1.31], [1, -.1, .36], [1, .24, .66], [1, .52, .92]];
const SH_A = j => .47 - .015 * j, SH_B = j => .42 - .026 * j;
// the plate on facet k of a ring over z0..z1, painted with the scale strip (column kk of 16)
function shPlate({k, z0, z1, F, kk, t = SH_T, tex = 'g_tail_a'}) {
  const deg = ((k * 22.5) % 360 + 360) % 360;
  let th = ((deg + 45) % 90) - 45;
  const psi = Math.round(deg - th);
  if (Math.abs(th) < 1e-6) th = 0;
  const n = [Math.round(Math.cos(psi * D2R)), Math.round(Math.sin(psi * D2R))], e = [-n[1], n[0]];
  const r = F.h - t / 2, hl = F.len / 2 + .006, c = [n[0] * r + e[0] * F.c, n[1] * r + e[1] * F.c];
  const hx = Math.abs(n[0]) * t / 2 + Math.abs(e[0]) * hl, hy = Math.abs(n[1]) * t / 2 + Math.abs(e[1]) * hl;
  const pe = P => clamp(((P[0] - c[0]) * e[0] + (P[1] - c[1]) * e[1]) / (2 * hl) + .5), pz = P => clamp((P[2] - z0) / (z1 - z0));
  const face = {tex, fn: P => [kk + pe(P), SH0 + SHH * pz(P)]};
  const side = {tex, fn: P => [kk + (pe(P) > .5 ? .97 : .03), SH0 + SHH * pz(P) * .6]};
  // one-sided (R18: the camera inside the tail root sees through): the outer face and the two facet edges only
  const faces = {[NAME[n.join()]]: face, [NAME[e.join()]]: side, [NAME[e.map(x => -x).join()]]: side};
  return faceEl([[c[0] - hx, c[1] - hy, z0], [c[0] + hx, c[1] + hy, z1]], faces, {rot: th ? ['z', th, [0, 0, (z0 + z1) / 2]] : undefined});
}
function sheath(i) {
  const els = [];
  SH_RINGS.forEach(([p, z0, z1], j) => {
    if (p === i) for (let k = 0; k < 16; k++) els.push(shPlate({k, z0, z1, F: facet(SH_A(j), SH_B(j), k), kk: (k + 3 * j) % 16}));
  });
  return els;
}
// a leaf fin in the radial plane at angle phi (deg from +X toward +Y): z0..z1 along the axis, r0..r1 out from it; both large
// faces show frill leaf `cell` (u along z, v outward); the thin faces are left out
function fin({phi, z0, z1, r0, r1, cell, t = .022, tex = 'g_tail_a'}) {
  const deg = ((phi % 360) + 360) % 360;
  let th = ((deg + 45) % 90) - 45;
  const psi = Math.round(deg - th);
  if (Math.abs(th) < 1e-6) th = 0;
  const n = [Math.round(Math.cos(psi * D2R)), Math.round(Math.sin(psi * D2R))], e = [-n[1], n[0]];
  const rm = (r0 + r1) / 2, hr = (r1 - r0) / 2, c = [n[0] * rm, n[1] * rm];
  const hx = Math.abs(n[0]) * hr + Math.abs(e[0]) * t / 2, hy = Math.abs(n[1]) * hr + Math.abs(e[1]) * t / 2;
  const face = {tex, fn: P => [4 * cell + 4 * clamp((P[2] - z0) / (z1 - z0)), FR0 + FRH * (1 - clamp(((P[0] * n[0] + P[1] * n[1]) - r0) / (r1 - r0)))]};
  const faces = {[NAME[e.join()]]: face, [NAME[e.map(x => -x).join()]]: face};
  return faceEl([[c[0] - hx, c[1] - hy, z0], [c[0] + hx, c[1] + hy, z1]], faces, {rot: th ? ['z', th, [0, 0, (z0 + z1) / 2]] : undefined});
}
// the frill: down, the two lower diagonals, the sides and two small upper-side fins
const FRILL = [[270, -.02, .8, .2, .96, 0], [225, .02, .8, .22, .95, 1], [315, .02, .8, .22, .95, 2], [180, .08, .74, .24, .88, 3], [0, .08, .74, .24, .88, 1],
  [157.5, .14, .62, .26, .72, 2], [22.5, .14, .62, .26, .72, 3]];
const frill = () => FRILL.map(([phi, z0, z1, r0, r1, cell]) => fin({phi, z0, z1, r0, r1, cell}));
const BACK = .2;
const segment = (i, f, shape = prof) => (i === 0 ? [...sheath(0), ...frill()]
  : i === 1 ? [...sheath(1), ...straps(1, f, {za: STRAP_Z1, shape})] : straps(i, f, {za: i === 0 ? -BACK : null, shape}));
// ---- tail_7 in P3 and the tips -------------------------------------------------------------------------------------------------
const ST = S0[7], S7 = S0[6];
// P3: in tail_7 the pale strap narrows to a leaf point (z 0.25 .. 0.8) and the dark one closes after it (.. 0.98) round
// the dark whip, a flattened 8-facet taper on the axis from z 0.15 through the tip part to a point 1.45 b past the joint
const p3Shape = s => {
  const p = prof(s), z = s - S7;
  return {...p, dA: p.dA * Math.pow(clamp(1 - (z - .25) / .55), .7), dB: p.dB * Math.pow(clamp(1 - (z - .45) / .53), .6)};
};
// the whip (v5 f1890, v6 f140): flat dark pieces (0.24 b) on the axis, a half twist over its length (one grid step per
// piece or two) so its broad face turns toward every camera, width w(z) x thickness
// 0.38 w, faces on the solid strip of g_tail_b (u along the whip, v across it)
function flatPiece({z0, z1, deg, w, t, tex, u0, u1}) {
  deg = ((deg % 360) + 360) % 360;
  let th = ((deg + 45) % 90) - 45;
  const psi = Math.round(deg - th);
  if (Math.abs(th) < 1e-6) th = 0;
  const n = [Math.round(Math.cos(psi * D2R)), Math.round(Math.sin(psi * D2R))], e = [-n[1], n[0]];
  const hx = Math.abs(n[0]) * t / 2 + Math.abs(e[0]) * w / 2, hy = Math.abs(n[1]) * t / 2 + Math.abs(e[1]) * w / 2;
  const uOf = P => u0 + (u1 - u0) * (P[2] - z0) / (z1 - z0), across = P => clamp((P[0] * e[0] + P[1] * e[1]) / w + .5);
  const face = {tex, fn: P => [uOf(P), SOLID + ROWU * across(P)]}, rim = {tex, fn: P => [uOf(P), SOLID + (.1 + .15 * clamp((P[0] * n[0] + P[1] * n[1]) / t + .5)) * VS]};
  const end = {tex, fn: P => [u0 + .2 * across(P), SOLID + (.1 + .15 * clamp((P[0] * n[0] + P[1] * n[1]) / t + .5)) * VS]};
  const faces = {[NAME[n.join()]]: face, [NAME[n.map(x => -x).join()]]: face, [NAME[e.join()]]: rim, [NAME[e.map(x => -x).join()]]: rim, front: end, back: end};
  return faceEl([[-hx, -hy, z0], [hx, hy, z1]], faces, {rot: th ? ['z', th, [0, 0, (z0 + z1) / 2]] : undefined});
}
// whip width along the arc length from the start of tail_7 (sw): 0.27 b where it emerges, a point 1.45 b past the tip joint
const WHIP_END = LEN[6] + 1.45;
const whipW = sw => .26 * Math.pow(clamp(1 - (sw - .5) / (WHIP_END - .5)), .8) + .006;
function whip(i, za, zb) {
  const els = [], off = i === 6 ? 0 : LEN[6], roll = ROLLF.p3[i];
  for (let z = za; z < zb - 1e-6; z += .24) {
    const z1 = Math.min(zb, z + .24), sw = off + (z + z1) / 2, w = whipW(sw);
    const deg = Math.round((sw * 72 + 90 + roll) / 22.5) * 22.5;
    els.push(flatPiece({z0: z - .01, z1: z1 + .01, deg, w, t: Math.max(.012, w * .38), tex: 'g_tail_b', u0: (sw * 6) % 12, u1: (sw * 6) % 12 + 1.4}));
  }
  return els;
}
function tipP3() {
  return whip(7, -.04, 1.45);
}
// P1: the straps run on to the scroll (pale to CURL_Z, the dark one a little further under it)
const p1TipShape = s => { const z = s - ST, p = prof(s); return {...p, dA: z < CURL_Z ? p.dA : 0, dB: z < CURL_Z + .1 ? p.dB : 0}; };
// the scroll (v2 f1260 / f1275): the pale strap leaves the top of the tail end, ramps up 22.5 deg and rolls forward and
// under into a spiral about the X axis: an outer turn of radius SC_R (over the top, down the front, back along the ground,
// up behind) and an inner 3/4 turn closing to 0.07 b; its lowest point 0.02 b over the ground at CROUCH. One plate per
// 22.5 deg chord, the chords centred on the 22.5 grid so every plate turns about X by a grid angle; the rims (the spiral
// seen from the side) carry the strap's dark outline.
const SC_R = .21, SC_C = [-.17 + SC_R, .66];
const scR = a => (a <= 270 ? SC_R : SC_R - (SC_R - .07) * (a - 270) / 270);
const scP = a => [SC_C[0] + scR(a) * Math.cos(a * D2R), SC_C[1] + scR(a) * Math.sin(a * D2R)];
function scrollPlate(P0, P1, w, h, u, tex) {
  const ctr = [0, (P0[0] + P1[0]) / 2, (P0[1] + P1[1]) / 2], len = Math.hypot(P1[0] - P0[0], P1[1] - P0[1]) * 1.1 + .006;
  const al = Math.round(Math.atan2(P1[0] - P0[0], P1[1] - P0[1]) / D2R / 22.5) * 22.5, q = Math.round(al / 90), th = al - q * 90, alongZ = ((q % 2) + 2) % 2 === 0;
  const lo = alongZ ? [-w / 2, ctr[1] - h / 2, ctr[2] - len / 2] : [-w / 2, ctr[1] - len / 2, ctr[2] - h / 2];
  const hi = alongZ ? [w / 2, ctr[1] + h / 2, ctr[2] + len / 2] : [w / 2, ctr[1] + len / 2, ctr[2] + h / 2];
  const along = P => clamp((alongZ ? (P[2] - ctr[2]) : (P[1] - ctr[1])) / len + .5);
  const face = {tex, fn: P => [u + .55 * along(P), SOLID + ROWU * clamp((P[0] + w / 2) / w)]};
  const rim = {tex, fn: P => [u + .55 * along(P), SOLID + .15 * VS]};
  const ends = {tex, fn: P => [u, SOLID + ROWU * clamp((P[0] + w / 2) / w)]};
  const faces = alongZ ? {up: face, down: face, left: rim, right: rim, front: ends, back: ends} : {front: face, back: face, left: rim, right: rim, up: ends, down: ends};
  return faceEl([lo, hi], faces, {rot: th ? ['x', -th, ctr] : undefined});
}
function scroll() {
  const els = [], p = prof(LT + CURL_Z), w0 = 2 * p.a * .8, tex = 'g_tail_a';
  // the ramp from the strap end on the tail top to the outer turn
  const a0 = -56.25, S = scP(a0);
  els.push(scrollPlate([p.b - .012, CURL_Z - .04], S, w0, .03, 1, tex));
  for (let k = 0, a = a0; a < 540 - 1e-6; k++, a += 22.5) {
    const w = w0 * (1 - .12 * Math.max(0, a - 270) / 270), h = a < 270 ? .032 : .026;
    els.push(scrollPlate(scP(a), scP(a + 22.5), w, h, 2 + (k * .55) % 12, tex));
  }
  return els;
}
// the scythe blade (v2 f1260 / f1275 / f1230): a dark crescent standing on its edge beside the tail end (x 0.2), from under
// the scroll back along the ground to a point 2 b behind it, angled 22.5 deg away from the tail (the hook seen from above,
// v2 f1245). One thin card: both large faces show the alpha-cut crescent of g_tail_b rows 240-303 (u along the blade, v
// down its 0.5 b height; bottom edge 0.03 b over the ground at CROUCH, the tip lifting 0.09 b); the thin faces left out.
const BL_LEN = 2.0, BL_Z0 = .56, BL_X = -.2, BL_Y0 = -.205, BL_H = .5;
function blade() {
  const tex = 'g_tail_b', t = .02;
  const face = {tex, fn: P => [16 * clamp((BL_Z0 - P[2]) / BL_LEN), BL0 + BLH * clamp((BL_Y0 + BL_H - P[1]) / BL_H)]};
  return [faceEl([[BL_X - t / 2, BL_Y0, BL_Z0 - BL_LEN], [BL_X + t / 2, BL_Y0 + BL_H, BL_Z0]], {left: face, right: face},
    {rot: ['y', -22.5, [BL_X, 0, BL_Z0]]})];
}
// the blade crescent (X 0 at the scroll .. 1 at the point; Y 0 top .. 1 bottom of the 0.5 b cell): a straight-ish lower
// edge rising toward the point, a convex back, dark slate with a sheen band, a pale cutting edge along the top, outline
function bladePaint(X, Y) {
  const zb = X * BL_LEN, yb = (1 - Y) * BL_H, q = zb / BL_LEN;
  const bot = .03 + .09 * Math.pow(q, 2.5), h = .34 * Math.pow(Math.max(0, 1 - q), .8) * Math.min(1, .55 + 2 * zb), top = bot + h;
  if (yb < bot || yb > top) return TRANSPARENT;
  const dpx = Math.min(yb - bot, top - yb) * 128, fy = (yb - bot) / Math.max(h, 1e-3);
  let g = .38 + .04 * (pn(N.e, X, Y, 9, 2) - .5) + .1 * smooth(.45, .8, fy) - .05 * smooth(.3, 0, fy);
  if ((top - yb) * 128 < 6 && q < .97) g = .66 - .1 * q;                                  // the pale cutting edge
  if (dpx < 2 || (BL_LEN - zb) * 64 < 1) g = .16;
  return grey(clamp(g));
}
function tipP1() {
  return [...straps(7, 'p1', {zb: CURL_Z + .1, shape: p1TipShape}), ...scroll(),
    ...blade()];
}
// ---- paint (128 x 304 grey tiles: the band rows, the solid strip, the sheath, frill and blade rows; see DV / TH) ------------
const TAU = Math.PI * 2;
const pn = (f, u, v, ku, kv) => f(Math.cos(TAU * u) * ku / 6 + 7, Math.sin(TAU * u) * ku / 6 + v * kv);   // periodic in u
// tile pixel -> (u along the strap 0..1, x across it 0..1, epx = distance to the strap edge in px) or null (cut away)
function bandAt(u, v) {
  const py = v * TH;
  if (py >= 5 * RH) return null;
  if (py >= 4 * RH) { const x = (py - 4 * RH) / RH; return {u, x, epx: Math.min(x, 1 - x) * RH}; }
  const r = Math.floor(py / RH), vv = (py - RH * r) / RH, uu = (u * 16) % 1, dv = DV[r];
  const es = vv - dv * uu, ee = 1 - dv + dv * uu - vv;
  if (es < 0 || ee < 0) return null;
  return {u, x: es / (1 - dv), epx: Math.min(es, ee) * RH};
}
// the pale strap (x across 0..1): a lit band near one edge, a cel shadow band along the other (the strap rolls a little
// at its edges, v2 f1135), a thin sheen line, wood-grain contour swirls in the middle (P1 bark), the dark cel outline
// the root-sheath ring (x round the ring 0..1, 16 facets, 8 scales per painted row; y along the ring 0 front .. 1 back):
// two staggered rows of pointed shield scales (grey fill, dark outline, a lit front bevel, a white stud on some, a crack
// on others) on the pale ground; behind the back row's tips the plate is cut away so the next ring shows through
const hsh = (i, j) => { let n = (Math.imul(i, 73856093) ^ Math.imul(j, 19349663)) >>> 0; n = Math.imul(n ^ (n >>> 13), 1274126177) >>> 0; return ((n ^ (n >>> 16)) >>> 0) / 4294967296; };
const SC_N = 6, SC_ROWS = [{y0: -.08, y1: .62, off: 0}, {y0: .38, y1: .995, off: .5}];
function scaleHit(x, y) {
  for (let r = 0; r < SC_ROWS.length; r++) {
    const {y0, y1, off} = SC_ROWS[r], X = x * SC_N - off, i = Math.round(X), sy = (y - y0) / (y1 - y0);
    for (const ii of [i - 1, i, i + 1]) {
      const id = ((ii % SC_N) + SC_N) % SC_N, jit = hsh(id, r), cx = ii + .1 * (hsh(id, r + 7) - .5), sx = X - cx - .12 * (hsh(id, r + 3) - .5) * Math.max(0, sy - .3);
      if (sy <= 0 || sy >= 1) continue;
      const f1 = sy < .2 ? Math.sqrt(1 - ((.2 - sy) / .2) ** 2) : 1, f2 = Math.pow(1 - sy, .75) / .846;
      const w = (.45 + .05 * jit) * f1 * f2;
      if (Math.abs(sx) < w) {
        const epx = Math.min((w - Math.abs(sx)) * 128 / SC_N, sy * (y1 - y0) * 32 * 1.6, (1 - sy) * (y1 - y0) * 32 * 2);
        return {r, id, sx: sx / (w + 1e-6), sy, epx, jit, fpx: sy * (y1 - y0) * 32};
      }
    }
  }
  return null;
}
function sheathPaint(x, y) {
  const s = scaleHit(x, y);
  if (!s) {
    if (y > .62) return TRANSPARENT;
    return grey(clamp(.9 + .05 * (pn(N.b, x, y, 10, 3) - .5)));
  }
  let g = .58 + .07 * (pn(N.c, x, y, 12, 4) - .5) + .1 * (s.jit - .5) - .08 * smooth(.45, 1, s.sy) + .05 * smooth(.2, -.8, s.sx);
  if (s.fpx > 1.2 && s.fpx < 3.2 && Math.abs(s.sx) < .8) g += .14;                       // the lit front bevel
  if (s.jit < .3 && Math.hypot(s.sx * 4.2, (s.sy - .28) * 9) < 1) g = .97;              // a white stud
  if (s.jit > .7 && Math.abs(s.sx - .25 * (s.sy - .5) - .15) < .07 && s.sy > .35 && s.sy < .8) g = .38;   // a crack
  if (s.epx < 1.3) g = .26;
  return grey(clamp(g));
}
// a frill leaf (cell 0..3; zz along the tail 0..1, rr outward 0..1): a swept, jagged spike from the base inside the sheath to
// the tip out and back, pale with a grey shade along its lower edge, a midrib and the dark outline
function frillPaint(cell, zz, rr) {
  const P0 = [.2, .05], P1 = [.42 + .04 * cell, .5 - .03 * cell], P2 = [.97, .93 - .06 * (cell % 2)];
  let best = 9, bt = 0;
  for (let k = 0; k <= 40; k++) {
    const t = k / 40, bx = (1 - t) ** 2 * P0[0] + 2 * (1 - t) * t * P1[0] + t * t * P2[0], by = (1 - t) ** 2 * P0[1] + 2 * (1 - t) * t * P1[1] + t * t * P2[1];
    const d = Math.hypot(zz - bx, rr - by);
    if (d < best) { best = d; bt = t; }
  }
  const w = (.24 + .02 * cell) * Math.pow(1 - bt, .85) * (1 + .22 * Math.sin(bt * 19 + cell * 2.1)) + .008;
  const base = rr < .24 && zz > .04 && zz < .5;
  const d = best - w;
  if (d > 0 && !base) return TRANSPARENT;
  const epx = base ? 9 : -d * 32;
  let g = .87 + .04 * (pn(N.a, zz, rr, 6, 3) - .5);
  if (rr < .05 + .9 * zz * zz - .02) g -= .12;                                              // the shaded lower side
  if (best < .018 && bt > .08 && bt < .9) g = .64;                                          // the midrib
  if (epx < 1.3) g = .3;
  return grey(clamp(g));
}
// the pale tile's extra rows: the sheath ring (240-271) and the frill leaves (272-303)
function paleExtra(u, v) {
  const py = v * TH;
  if (py < 272) return sheathPaint(u, (py - 240) / 32);
  const c = Math.floor(u * 4);
  return frillPaint(c, u * 4 - c, 1 - (py - 272) / 32);
}
const paleTile = (u, v) => {
  if (v * TH >= 5 * RH) return paleExtra(u, v);
  const b = bandAt(u, v);
  if (!b) return TRANSPARENT;
  const {x, epx} = b;
  let g = .9 + .04 * (pn(N.a, u, x, 9, 3) - .5);
  g += .06 * smooth(.08, .16, x) * smooth(.34, .24, x);                 // the lit band
  g -= .13 * smooth(.6, .7, x) * smooth(.97, .9, x);                   // the cel shadow band
  if (Math.abs(x - .5) < .018) g -= .07;                               // the sheen line
  const su = u * 5, ci = Math.floor(su), fu = su - ci, cv = .38 + .14 * ((ci * 7919) % 7) / 7;
  const rr = Math.hypot((fu - .5) * 1.25, (x - cv) * 2.2), ring = Math.abs(Math.sin(rr * 30 + 1.5 * pn(N.c, u, x, 6, 2)));
  if (rr < .36 && ring < .2 && x > .16 && x < .66) g -= .12 * (1 - ring / .2) * smooth(.36, .26, rr);
  if (epx < 2.4) g = .32 + .05 * (pn(N.d, u, x, 8, 4) - .5);
  else if (epx < 4.2) g -= .07;
  return grey(clamp(g));
};
// the dark strap: a lit centre ridge, darker margins and the outline
const darkTile = (u, v) => {
  if (v * TH >= 5 * RH) return bladePaint(u, (v * TH - 240) / 64);
  const b = bandAt(u, v);
  if (!b) return TRANSPARENT;
  const {x, epx} = b, ex = Math.min(x, 1 - x);
  let g = .47 + .05 * (pn(N.e, u, x, 14, 2) - .5) + .1 * smooth(.25, .45, ex) - .08 * smooth(.2, .06, ex);
  if (epx < 2.2) g = .19;
  else if (epx < 3.8) g -= .08;
  return grey(clamp(g));
};
registerTile('g_tail_a', TW, TH, 32);
registerTile('g_tail_b', TW, TH, 32);
// ---- region interface ------------------------------------------------------------------------------------------------------
// models(): {model name: elements in model units}; FORM_MODELS {part: {p1, p3}}; sprites(): the region's card sprites.
export function models() {
  const out = {};
  SEG.forEach((n, i) => {
    out[n] = toUnits(autoSlot(segment(i, 'p1')), PART_SCALE[n]);
    out[n + '_p3'] = toUnits(autoSlot(i < 6 ? segment(i, 'p3') : [...segment(6, 'p3', p3Shape), ...whip(6, .2, LEN[6] + .1)]), PART_SCALE[n]);
  });
  out.tail_tip_p1 = toUnits(autoSlot(tipP1()), PART_SCALE.tail_tip);
  out.tail_tip_p3 = toUnits(autoSlot(tipP3()), PART_SCALE.tail_tip);
  return out;
}
export const FORM_MODELS = {...Object.fromEntries(SEG.map(n => [n, {p1: n, p3: n + '_p3'}])), tail_tip: {p1: 'tail_tip_p1', p3: 'tail_tip_p3'}};
export function sprites() {
  return {
    g_tail_a: sprite(TW, TH, 32, paleTile, 'both', 'tail', {use: 'tinted'}),
    g_tail_b: sprite(TW, TH, 32, darkTile, 'both', 'tail', {use: 'tinted'}),
  };
}
export const NOTES = {tail_1: 'root sheath: 4 rings of shingled scale plates + a frill of 7 pale leaf fins; tail_2: 3 more rings over the strap start; tail_3..7: two straps wound round a flattened 16-facet tube (pale band_a, dark band_b), one model per segment for both forms (slot tints); the twist runs on the arc length, continuous over the joints',
  tail_7: 'P3 model tail_7_p3: the straps end round the emerging dark whip', tail_tip: 'P1 pale spiral scroll + dark alpha-cut scythe crescent; P3 dark whip'};
