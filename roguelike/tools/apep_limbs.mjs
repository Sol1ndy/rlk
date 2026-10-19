// LIMBS region of the 아펩의 오아시스 파수꾼 rig (plan R4 parts 22-39 minus the hands, 48-49; model_p3.md §0 item 2: the six
// phase-3 arms ARE the six phase-1 limbs): the upper and lower segments of the three limb pairs and the bead vines.
//   A (a_up, a_lo)   P1 the long pale shell arms (planted far out, raised in attacks) | P3 the raised "antler" arms:
//                    thin shell, lime leaf blades, a gold elbow cone (model_p3 §2.3 items 13-14)
//   B (b_up, b_lo)   P1 the front "elephant" legs, dark armour fading to pale bark at the foot | P3 the middle arms:
//                    shell + lime cladding on the front, the dark dorsal carapace on the back (v5 f1908)
//   C (c_up, c_lo)   P1 the rear legs | P3 the lower arms reaching down to the water, shell + cladding
//   beads            P3 only: a thin vine with rows of small white leaflets (P1: the empty model)
// Frames (apep_pose FRAMES): every limb segment is authored in its bone frame 'y': model -Y along the bone from the joint
// toward the next joint, model -Z toward the world front at the reference stance (P1 CROUCH, P3 UPRIGHT). The loft
// 'y' section: e1 = model +X, e2 = model front (-Z), so sin(theta) > 0 is the segment's front. Region interface: see
// apep_body.mjs. The right side is the mirror image of the left (mirrorX).
import {loft, slab, crossCards, rockBox, toUnits, mirrorX} from './mboss_shape_lib.mjs';
import {PART_SCALE, J} from './apep_pose.mjs';
import {PAL, C, clamp, mix, N, lift, autoSlot, sprite, onRect, spriteSize, sdLeaf, cone, TRANSPARENT} from './apep_materials.mjs';

export const REGION = 'limbs';
export const PARTS = ['a_up_l', 'a_up_r', 'a_lo_l', 'a_lo_r', 'b_up_l', 'b_up_r', 'b_lo_l', 'b_lo_r', 'c_up_l', 'c_up_r', 'c_lo_l', 'c_lo_r', 'beads_l', 'beads_r'];
const dist = (a, b) => Math.hypot(...a.map((v, i) => v - b[i]));
const LEN = {};
for (const L of ['a', 'b', 'c']) { LEN[`${L}_up`] = dist(J[`${L}_up_l`], J[`${L}_lo_l`]); LEN[`${L}_lo`] = dist(J[`${L}_lo_l`], J[`${L}_hand_l`]); }
const sinD = th => Math.sin(th * Math.PI / 180);
// a limb segment: a tapered round loft along -Y from +ov (overlap into the parent) to -(len + 0.06)
function segLoft(len, r0, r1, tex, {bulge = 1.06, seed = 0, ov = .14} = {}) {
  return loft('y', [{a: ov, r: r0 * .92}, {a: -len * .35, r: r0 * bulge}, {a: -len * .7, r: (r0 + r1) / 2}, {a: -len - .06, r: r1}], {n: 16, tex, caps: '+-', seed});
}
// ---- phase 1 ---------------------------------------------------------------------------------------------------------------
const A1 = {up: [.38, .32], lo: [.33, .25]}, B1 = {up: [.62, .55], lo: [.55, .38]}, C1 = {up: [.56, .5], lo: [.5, .34]};
function p1(seg) {
  const [L] = seg.split('_'), len = LEN[seg];
  if (L === 'a') return segLoft(len, ...A1[seg.slice(2)], (k, th) => (sinD(th) < -.55 ? 'g_plate' : 'g_shell'), {seed: 300 + len * 10});
  const R = L === 'b' ? B1 : C1, x = seg.slice(2);
  // the legs: dark armour plates on the upper segment, the dark -> pale bark gradient on the lower (model.md §3.4)
  return segLoft(len, ...R[x], x === 'up' ? 'g_plate' : 'p1_leg', {seed: 310 + len * 10, bulge: 1.1});
}
// ---- phase 3 ---------------------------------------------------------------------------------------------------------------
const A3 = {up: [.2, .17], lo: [.17, .13]}, B3 = {up: [.3, .25], lo: [.26, .21]}, C3 = {up: [.28, .23], lo: [.24, .19]};
// lime leaf blade card in the plane x = at (u = Z, v = Y), along the segment
const BLADE_R = {u0: -.2, u1: .2, v0: -1.0, v1: 0};
const bladeSd = sdLeaf(0, -1.0, 0, .17, {p: .9});
const bladePaint = (u, v) => { const d = bladeSd(u, v); if (d > 0) return null; let c = PAL.p3_lime(clamp(.18 + .35 * (-v) + .12 * (N.a(u * 9, v * 9) - .5))); if (Math.abs(u) < .015) c = PAL.p3_line(.35); if (d > -.02) c = PAL.p3_line(.6); return c; };
function blade(at, y0, h, flip = 1) {
  // a blade of length h starting at y0 (its base) pointing down the segment, standing out on the side x = at
  const k = h / 1.0, rect = {u0: BLADE_R.u0 * k, u1: BLADE_R.u1 * k, v0: y0 - h, v1: y0};
  const sd = (u, v) => bladeSd(u / k, (v - y0) / k) * k;
  return slab({plane: 'x', at, rect, sd, half: .025, sprite: 'p3_blade', edge: 'p3_lime', cell: .06, core: false, rot: ['z', flip * 22.5, [at, y0, 0]]});
}
function p3(seg) {
  const [L] = seg.split('_'), len = LEN[seg], x = seg.slice(2);
  const R = L === 'a' ? A3 : L === 'b' ? B3 : C3;
  // shell sides, lime cladding on the front, the dorsal carapace (tinted plate) on the back; the sideways B arms carry it
  // over the top as well (v5 f1908: from behind they read dark with a lime rim). In the bone frame 'y' of a B arm at
  // UPRIGHT, model +X is world up (left arm; the mirrored right arm likewise), model -Z the front.
  const cosD = th => Math.cos(th * Math.PI / 180);
  const tex = (k, th) => (sinD(th) > .38 ? 'p3_lime' : (sinD(th) < -.38 && L !== 'c') || (L === 'b' && cosD(th) > .55) ? 'g_plate' : 'g_shell');
  const els = segLoft(len, ...R[x], tex, {seed: 330 + len * 10});
  if (L === 'a') { els.push(...blade(R[x][0] + .04, -len * .12, len * .5, 1), ...blade(R[x][0] + .02, -len * .52, len * .42, 1)); }
  if (L === 'b') els.push(...blade(R[x][0] + .03, -len * .2, len * .55, 1));
  // the gold elbow cone (A and B lower segments, at the elbow, standing out on the outer side)
  if ((L === 'a' || L === 'b') && x === 'lo') els.push(...cone([R[x][0] * .7, .05, 0], .13, .42, 'p3_gold', {axis: 'x', seed: 340}));
  return els;
}
// bead vine (phase 3): a thin vine hanging along -Y with three rows of small white leaflets
const BEAD_R = {u0: -.25, u1: .25, v0: -.35, v1: .35};
const beadPaint = (u, v) => {
  // a vertical string of 4 small leaflets on a thin vine
  if (Math.abs(u) < .022) return PAL.p3_beads(.75);
  for (let i = 0; i < 4; i++) { const cy = .27 - i * .18, s = i % 2 ? 1 : -1; const dx = u - s * .1, dy = v - cy; const e = (dx * dx) / (.11 * .11) + (dy * dy) / (.06 * .06); if (e < 1) return e > .7 ? PAL.p3_beads(.45) : PAL.p3_beads(.05 + .2 * e); }
  return null;
};
function beads() {
  const L = dist(J.beads_l, [1.81, 1.35, -.69]), els = [rockBox([-.035, -L, -.035], [.035, .05, .035], 'p3_lime', {seed: 351})];
  for (let i = 0; i < 3; i++) els.push(...crossCards('p3_bead', [0, -.25 - i * (L - .3) / 3, 0], .5, .7, {y0: -.7}));
  return els;
}
// ---- region interface ------------------------------------------------------------------------------------------------------
const SEGS = ['a_up', 'a_lo', 'b_up', 'b_lo', 'c_up', 'c_lo'];
export function models() {
  const out = {};
  for (const seg of SEGS) for (const [f, fn] of [['p1', p1], ['p3', p3]]) {
    const L = toUnits(autoSlot(fn(seg)), PART_SCALE[`${seg}_l`]);
    out[`${seg}_l_${f}`] = L; out[`${seg}_r_${f}`] = mirrorX(L);
  }
  const b = toUnits(autoSlot(beads()), PART_SCALE.beads_l);
  out.beads_l_p3 = b; out.beads_r_p3 = mirrorX(b);
  return out;
}
export const FORM_MODELS = {
  ...Object.fromEntries(SEGS.flatMap(seg => ['l', 'r'].map(s => [`${seg}_${s}`, {p1: `${seg}_${s}_p1`, p3: `${seg}_${s}_p3`}]))),
  beads_l: {p1: 'empty', p3: 'beads_l_p3'}, beads_r: {p1: 'empty', p3: 'beads_r_p3'},
};
export function sprites() {
  const [bw, bh] = spriteSize(BLADE_R, 48), [ew, eh] = spriteSize(BEAD_R, 64);
  return {
    p3_blade: sprite(bw, bh, 48, onRect(BLADE_R, bladePaint), 'p3', 'limbs'),
    p3_bead: sprite(ew, eh, 64, onRect(BEAD_R, beadPaint), 'p3', 'limbs'),
  };
}
void [C, mix, lift, TRANSPARENT];
