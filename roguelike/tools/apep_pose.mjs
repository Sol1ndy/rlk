// Pose -> part transforms of the 아펩의 오아시스 파수꾼 (Guardian of Apep's Oasis) rig: the superset skeleton of both forms
// and both stances, forward kinematics with bind frames, the planted-hand IK, the per-form authoring frames of the part
// models, the hit-proxy columns, the push capsules and the rest anchors. Shared math: mboss_rig_math.mjs. Binding
// numbers: scratchpad ap/plan.md R1-R11 (1 m = 1 b), ap/understand/model_p3.md §6.2 (both rest stances).
//
// Rig frame: +X = the boss's LEFT, +Y up, -Z forward, blocks; the origin is the anchor on the floor (under the thorax
// base in both stances). Euler triples are degrees applied X, then Y, then Z (mboss_rig_math q), always about the rig
// axes as carried by the PARENT bone: pitch + raises a forward-pointing bone (and lowers a back-pointing one), yaw +
// turns a forward-pointing bone toward the boss's right (-X), roll + tips the top toward the boss's right.
//
// ONE RIGID SKELETON (plan R3). The bind pose IS the CROUCH stance: every joint below is the CROUCH position (model_p3
// §6.2) and every attachment offset is that joint minus its parent's joint, in the parent's frame. UPRIGHT is reached by
// joint angles only (apep_clips.mjs STANCES.UPRIGHT; the residuals against model_p3 §6.2 are printed by the builder).
// Where the footage moves an attachment, a pose-only bone carries it: clav_a_<s> (the A roots come in and back),
// hood_hinge (the hood swings back about the back-top of the skull), and the hem_a -> hem_b chain (folded back on the
// floor in the crouch, hanging straight in the upright). The pelvis is the 6-DOF body root (pelT + pelvis euler): the
// waist rises from 2.8 to 3.1 b and moves 0.8 b forward when the thorax stands up; the anchor itself never moves in a
// clip (no root x / z travel, no root yaw: plan R16).
//
// A pose is a full set of channels (DEFAULT_POSE in apep_clips.mjs merged with the clip keys):
//   pos [0, y, 0]                   root offset (y only: the burrow sink to -6 b)
//   rot [p, y, r]                   root rotation about ROOT_PIVOT (the hoop / wheel of 이동 돌진; keyed, plan R16)
//   pelT [x, y, z], pelvis          pelvis translation (blocks) and euler (the whole body about the waist)
//   abdomen hem_a hem_b             rear body / robe stem and the hem chain
//   chest shoulders neck head       the thorax split in two (S-coil, hoop, spiral column), the neck, the skull
//   hood_hinge                      the hood swing (pitch - folds the hood back over the skull)
//   hair_<s>_1 hair_<s>_2           drapes / hair strands (s = l | r)
//   mantle_<s>_a mantle_<s>_b       the shoulder flap / carapace chain
//   clav_a_<s>                      the pose-only clavicle of the A arm
//   <L>_up_<s> <L>_lo_<s> <L>_hand_<s>   FK eulers of the limbs L = a | b | c (upper, lower, hand)
//   ik_<L>_<s>                      0..1: blend of the FK limb toward the IK limb (planted hands, plan R19 foot IK)
//   tg_<L>_<s> [x, y, z]            IK wrist target (root frame); hf_<L>_<s> the IK hand euler (root frame, absolute:
//                                   [0, 0, 0] = flat on the floor as authored); bn_<L>_<s> the elbow-plane twist (deg)
//   beads_<s>                       the bead vine (P3)
//   tail_1 .. tail_7 tail_tip       tail segment eulers; tLift tCurl tSweep tTwist: parametric tail (tLift raises
//                                   tail_1, tCurl adds per segment (up +), tSweep / tTwist the total yaw / roll spread
//                                   over the chain, + = the tail swings to the boss's left)
//   vis                             visibility scale of every part (0 = hidden, the burrow)
import {add, sub, times, mul, q, rot, len, unit, dot, cross, perp, slerp, aimQ, basisQ, ik, toDisplayT, toDisplayQ} from './mboss_rig_math.mjs';

export const H_CROUCH = 4.4, H_UPRIGHT = 8.5;
export const SIDES = ['l', 'r'];
export const LIMBS = ['a', 'b', 'c'];
const mx = v => [-v[0], v[1], v[2]];
export const mirrorE = e => [e[0], -e[1], -e[2]];
export const mirrorQ = Q => [Q[0], -Q[1], -Q[2], Q[3]];
export const inv = Q => [-Q[0], -Q[1], -Q[2], Q[3]];
const Q0 = [0, 0, 0, 1];
export const ROOT_PIVOT = [0, 2.6, .5];

// ---- the bind skeleton (= CROUCH; rig frame, blocks) -----------------------------------------------------------------
// Tail polyline (model_p3 §6.2 CROUCH): root, the 6 inner joints, the tip joint, the tip end.
export const TAIL_C = [[0, 2.39, 2.89], [0, 1.47, 3.62], [0, .66, 4.49], [0, .27, 5.58], [.31, .19, 6.72], [.69, .19, 7.79], [1.19, .2, 8.8], [1.48, .19, 9.9], [1.6, .2, 10.9]];
// Limb chains (left side): root -> elbow -> wrist -> hand tip (model_p3 §6.2 CROUCH).
export const LIMB_C = {
  a: [[1.55, 3.66, -.93], [3.4, 2.6, -1.6], [4.8, .6, -2.4], [5.3, .15, -2.6]],
  b: [[1.23, 2.85, -1.36], [2.3, 2.0, -2.4], [2.4, .4, -3.0], [2.5, .15, -3.6]],
  c: [[1.14, 2.51, 1.12], [2.6, 2.2, 1.9], [2.9, .4, 2.5], [3.0, .15, 3.0]],
};
// The hem chain (1.4 + 1.1 b): folded back along the floor in the crouch (plan R3), straight down in the upright.
const HEM = [[0, 2.12, 1.14], [0, .72, .92], [0, .15, 1.85]];
// [name, parent, joint, {po: pose-only, tip: the bind point the bone runs to (its child joint / the model end)}]
const BONE_ROWS = [
  ['root', null, [0, 0, 0], {po: true}],
  ['pelvis', 'root', [0, 2.8, 1.0], {po: true}],
  ['abdomen', 'pelvis', [0, 2.8, 1.0], {tip: TAIL_C[0]}],
  ['hem_a', 'abdomen', HEM[0], {tip: HEM[1]}],
  ['hem_b', 'hem_a', HEM[1], {tip: HEM[2]}],
  ...[1, 2, 3, 4, 5, 6, 7].map(i => [`tail_${i}`, i === 1 ? 'pelvis' : `tail_${i - 1}`, TAIL_C[i - 1], {tip: TAIL_C[i]}]),
  ['tail_tip', 'tail_7', TAIL_C[7], {tip: TAIL_C[8]}],
  ['chest', 'pelvis', [0, 3.14, -.01], {tip: [0, 3.34, -1.21]}],
  ['core', 'chest', [0, 2.2, -.85]],
  ['crys_low', 'chest', [0, 3.55, .55]],
  ['shoulders', 'chest', [0, 3.34, -1.21], {tip: [0, 3.4, -1.4]}],
  ['crys_back', 'shoulders', [0, 4.05, -.75]],
  ['neck', 'shoulders', [0, 3.4, -1.4], {tip: [0, 3.4, -1.96]}],
  ['head', 'neck', [0, 3.4, -1.96]],
  ['face', 'head', [0, 3.4, -1.96]],
  ['hood_hinge', 'head', [0, 3.76, -1.93], {po: true}],
  ['hood', 'hood_hinge', [0, 3.76, -1.93]],
  // the crown joint sits between the P1 crown cone on the hood top and the P3 leaf fan on the hood's front edge (which
  // the 107 deg swing carries to the top of the face, model_p3 §2.1 item 2); each form's model is placed in its own frame
  ['crown', 'hood', [0, 3.8, -3.1]],
];
for (const s of SIDES) {
  const m = s === 'l' ? v => v : mx;
  BONE_ROWS.push(
    [`hair_${s}_1`, 'hood', m([1.02, 3.07, -2.7]), {tip: m([1.45, 1.67, -2.69])}],
    [`hair_${s}_2`, `hair_${s}_1`, m([1.45, 1.67, -2.69]), {tip: m([1.7, .2, -2.8])}],
    [`mantle_${s}_a`, 'shoulders', m([1.34, 3.94, -.67]), {tip: m([3.0, 3.4, .4])}],
    [`mantle_${s}_b`, `mantle_${s}_a`, m([1.21, 3.79, .04]), {tip: m([2.6, 3.1, 1.3])}],
    [`clav_a_${s}`, 'shoulders', m([1.21, 3.26, -.63]), {po: true}],
  );
  for (const L of LIMBS) {
    const C = LIMB_C[L].map(m), par = L === 'a' ? `clav_a_${s}` : L === 'b' ? 'shoulders' : 'pelvis';
    BONE_ROWS.push([`${L}_up_${s}`, par, C[0], {tip: C[1]}], [`${L}_lo_${s}`, `${L}_up_${s}`, C[1], {tip: C[2]}], [`${L}_hand_${s}`, `${L}_lo_${s}`, C[2], {tip: C[3]}]);
  }
  // the bead vine exists in phase 3 only: its bind joint is the UPRIGHT measurement carried back by b_up
  BONE_ROWS.push([`beads_${s}`, `b_up_${s}`, m([1.45, 3.19, -1.65]), {tip: m([1.81, 1.35, -.69])}]);
}
export const BONES = BONE_ROWS.map(([name, parent, j, o = {}]) => ({name, parent, j, po: !!o.po, tip: o.tip || null}));
export const BONE = Object.fromEntries(BONES.map(b => [b.name, b]));
// J[name] is the same array as BONE[name].j (the fitting tools move joints in place).
export const J = Object.fromEntries(BONES.map(b => [b.name, b.j]));
export const POSE_ONLY = BONES.filter(b => b.po).map(b => b.name);

// ---- the 49 parts (plan R4 order = UUID idx 0x00-0x30; contract §0.4.3) --------------------------------------------------
// [part, region, brightness, display scale ((reach + 10 %) / 1.5), P3 brightness when it differs]
export const PART_ROWS = [
  ['abdomen', 'body', 13, 1.6], ['hem_a', 'body', 13, 1.4], ['hem_b', 'body', 13, 1.7], ['chest', 'body', 13, 1.5],
  ['shoulders', 'body', 13, 2.0], ['core', 'body', 15, 1.3], ['crys_low', 'body', 14, 1.1, 15], ['crys_back', 'body', 14, 1.5, 15],
  ['neck', 'head', 13, .8], ['head', 'head', 13, 1.3], ['face', 'head', 15, 1.5], ['hood', 'head', 13, 2.1], ['crown', 'head', 15, 1.4],
  ['hair_l_1', 'head', 13, 1.2], ['hair_r_1', 'head', 13, 1.2], ['hair_l_2', 'head', 13, 1.2], ['hair_r_2', 'head', 13, 1.2],
  ['mantle_l_a', 'body', 13, 1.7], ['mantle_r_a', 'body', 13, 1.7], ['mantle_l_b', 'body', 13, 1.5], ['mantle_r_b', 'body', 13, 1.5],
  ['a_up_l', 'limbs', 13, 2.0], ['a_up_r', 'limbs', 13, 2.0], ['a_lo_l', 'limbs', 13, 2.1], ['a_lo_r', 'limbs', 13, 2.1],
  ['a_hand_l', 'hands', 13, 1.0], ['a_hand_r', 'hands', 13, 1.0],
  ['b_up_l', 'limbs', 13, 1.5], ['b_up_r', 'limbs', 13, 1.5], ['b_lo_l', 'limbs', 13, 1.5], ['b_lo_r', 'limbs', 13, 1.5],
  ['b_hand_l', 'hands', 13, 1.8], ['b_hand_r', 'hands', 13, 1.8],
  ['c_up_l', 'limbs', 13, 1.4], ['c_up_r', 'limbs', 13, 1.4], ['c_lo_l', 'limbs', 13, 1.6], ['c_lo_r', 'limbs', 13, 1.6],
  ['c_hand_l', 'hands', 13, 1.2], ['c_hand_r', 'hands', 13, 1.2],
  ...[1, 2, 3, 4, 5, 6, 7].map(i => [`tail_${i}`, 'tail', 13, 1.1]), ['tail_tip', 'tail', 13, 1.0],
  ['beads_l', 'limbs', 14, 1.6], ['beads_r', 'limbs', 14, 1.6],
];
export const PART_NAMES = PART_ROWS.map(r => r[0]);
export const PART_SCALE = Object.fromEntries(PART_ROWS.map(r => [r[0], r[3]]));
export const PART_REGION = Object.fromEntries(PART_ROWS.map(r => [r[0], r[1]]));
export const PART_BRIGHT = Object.fromEntries(PART_ROWS.map(r => [r[0], r[2]]));
export const PART_BRIGHT_P3 = Object.fromEntries(PART_ROWS.map(r => [r[0], r[4] ?? r[2]]));
export const TAIL_PARTS = PART_NAMES.filter(n => n.startsWith('tail_'));
export const HAND_PARTS = PART_NAMES.filter(n => PART_REGION[n] === 'hands');

// Pose channel names (for the clip checks): every non-root bone has an euler channel.
export const EULER_CHANNELS = BONES.filter(b => b.name !== 'root').map(b => b.name);

// ---- forward kinematics ----------------------------------------------------------------------------------------------------
// Rodrigues rotation of v about the unit axis a by deg.
const turn = (v, a, deg) => { const t = deg * Math.PI / 180, c = Math.cos(t), s = Math.sin(t); return add(add(times(v, c), times(cross(a, v), s)), times(a, dot(a, v) * (1 - c))); };
// Rotation mapping the bind direction d0 (with the bend normal n0) onto d (with n): basis(d, n) * basis(d0, n0)^-1.
function frameQ(d, n) { const x = unit(d), z0 = unit(perp(n, x)), y = cross(z0, x); return basisQ(x, y, z0); }
const relQ = (d0, n0, d, n) => mul(frameQ(d, n), inv(frameQ(d0, n0)));
// Limb bind geometry (left / right): segment lengths, the bind bend normal and pole (from the current joints).
function limbGeom(s, L) {
  const S = J[`${L}_up_${s}`], E = J[`${L}_lo_${s}`], W = J[`${L}_hand_${s}`];
  const n0 = unit(cross(sub(E, S), sub(W, E)));
  return {S, E, W, a: len(sub(E, S)), b: len(sub(W, E)), n0, pole: unit(perp(sub(E, S), unit(sub(W, S))))};
}
export const limbLen = (L, s) => { const G = limbGeom(s, L); return [G.a, G.b]; };
// Tail parametric channels per segment.
const TAIL_SEG = ['tail_1', 'tail_2', 'tail_3', 'tail_4', 'tail_5', 'tail_6', 'tail_7', 'tail_tip'];

// solve(p) -> {bone: {t (joint, rig frame), R (pose rotation: world relative to bind), s (scale)}} for every bone
// (pose-only bones included). prev: the previous frame's limb bend directions (o._bend) for IK continuity.
export function solve(p, {prev = null} = {}) {
  const o = {};
  const e = n => p[n] || [0, 0, 0];
  const bend = {};
  const limbDone = new Set();
  for (const b of BONES) {
    if (o[b.name] || limbDone.has(b.name)) continue;
    if (b.name === 'root') { o.root = {t: [0, 0, 0], R: Q0}; continue; }
    const P = o[b.parent];
    if (b.name === 'pelvis') { o.pelvis = {t: add(b.j, p.pelT || [0, 0, 0]), R: q(e('pelvis'))}; continue; }
    const m = /^([abc])_up_([lr])$/.exec(b.name);
    if (m) { solveLimb(o, p, m[1], m[2], P, prev, bend); for (const x of ['up', 'lo', 'hand']) limbDone.add(`${m[1]}_${x}_${m[2]}`); continue; }
    let E = e(b.name);
    const ti = TAIL_SEG.indexOf(b.name);
    if (ti >= 0) {
      const n = TAIL_SEG.length, up = (ti === 0 ? p.tLift || 0 : 0) + (p.tCurl || 0);
      E = [E[0] - up, E[1] + (p.tSweep || 0) / n, E[2] + (p.tTwist || 0) / n];
    }
    o[b.name] = {t: add(P.t, rot(P.R, sub(b.j, BONE[b.parent].j))), R: mul(P.R, q(E))};
  }
  // root: offset and rotation about ROOT_PIVOT (applied to everything; the IK targets are root-frame)
  const R0 = q(p.rot || [0, 0, 0]), pos = p.pos || [0, 0, 0];
  for (const v of Object.values(o)) { v.t = add(add(ROOT_PIVOT, rot(R0, sub(v.t, ROOT_PIVOT))), pos); v.R = mul(R0, v.R); v.s = p.vis ?? 1; }
  Object.defineProperty(o, '_bend', {value: bend, enumerable: false});
  return o;
}
function solveLimb(o, p, L, s, P, prev, bend) {
  const k = `${L}_${s}`, G = limbGeom(s, L), up = `${L}_up_${s}`, lo = `${L}_lo_${s}`, hd = `${L}_hand_${s}`;
  const par = BONE[up].parent, S = add(P.t, rot(P.R, sub(G.S, BONE[par].j)));
  const ev = n => p[n] || [0, 0, 0];
  // FK
  const Rup = mul(P.R, q(ev(up)));
  const w = Math.max(0, Math.min(1, p['ik_' + k] ?? 0));
  let RupF = Rup, RloF, RhF;
  if (w < 1e-6) {
    const Rlo = mul(Rup, q(ev(lo)));
    o[up] = {t: S, R: Rup};
    o[lo] = {t: add(S, rot(Rup, sub(G.E, G.S))), R: Rlo};
    o[hd] = {t: add(o[lo].t, rot(Rlo, sub(G.W, G.E))), R: mul(Rlo, q(ev(hd)))};
    return;
  }
  // IK: wrist target (root frame), elbow pole = the bind elbow side carried by the parent, twisted by bn about S -> W
  const Wt = p['tg_' + k] || G.W;
  const axis = unit(sub(Wt, S));
  const pole = turn(rot(P.R, G.pole), axis, p['bn_' + k] || 0);
  const R = ik(S, Wt, G.a, G.b, pole, prev && prev[k]);
  bend[k] = R.v;
  const n = unit(cross(sub(R.E, S), sub(R.W, R.E)));
  const nn = len(n) > 1e-6 ? n : rot(P.R, G.n0);
  const RupI = relQ(sub(G.E, G.S), G.n0, sub(R.E, S), nn);
  const RloI = relQ(sub(G.W, G.E), G.n0, sub(R.W, R.E), nn);
  const RhI = q(p['hf_' + k] || [0, 0, 0]);
  RupF = slerp(Rup, RupI, w);
  const Eb = add(S, rot(RupF, sub(G.E, G.S)));
  RloF = slerp(mul(RupF, q(ev(lo))), RloI, w);
  const Wb = add(Eb, rot(RloF, sub(G.W, G.E)));
  RhF = slerp(mul(RloF, q(ev(hd))), RhI, w);
  o[up] = {t: S, R: RupF}; o[lo] = {t: Eb, R: RloF}; o[hd] = {t: Wb, R: RhF};
}
// Euler triple [x, y, z] (degrees, the q() order: X, then Y, then Z) of a rotation quaternion.
export function eulerOf(Q) {
  const [x, y, z, w] = Q;
  const m20 = 2 * (x * z - w * y), m21 = 2 * (y * z + w * x), m22 = 1 - 2 * (x * x + y * y), m10 = 2 * (x * y + w * z), m00 = 1 - 2 * (y * y + z * z);
  const D = 180 / Math.PI;
  return [Math.atan2(m21, m22) * D, Math.asin(Math.max(-1, Math.min(1, -m20))) * D, Math.atan2(m10, m00) * D].map(v => Math.round(v * 100) / 100 || 0);
}
// A bind-frame point (rig frame, CROUCH) carried by bone n in the solved pose.
export const carry = (o, n, P) => add(o[n].t, rot(o[n].R, sub(P, J[n])));

// ---- per-form authoring frames of the part models ---------------------------------------------------------------------------
// Each part model is authored (region modules) in an AUTHORING FRAME at a REFERENCE STANCE, about the part's joint:
//   'w'  world axes (the rig frame) as the part sits in the reference stance: what the footage shows, front / side
//   'y'  model -Y along the bone toward its tip (limbs, hair, hem, flaps); front (-Z) = the `front` hint
//   'z'  model +Z along the bone toward its tip (tail); up (+Y) = the `front` hint's up
// The display rotation of a part is then R_pose * R_ref^-1 * A (A = the authoring frame in world at the reference
// stance). A model authored for UPRIGHT therefore shows exactly as authored in the UPRIGHT stance and turns with its
// bone into every other pose (the P3 crawl included). FRAMES[part][form] = {ref: 'CROUCH' | 'UPRIGHT', kind, front}.
export const FRAMES = {};
const F = (ref, kind = 'w', front = null) => ({ref, kind, front});
for (const n of PART_NAMES) FRAMES[n] = {p1: F('CROUCH'), p3: F('UPRIGHT')};
for (const s of SIDES) {
  const sx = s === 'l' ? 1 : -1;
  for (const L of LIMBS) for (const x of ['up', 'lo']) FRAMES[`${L}_${x}_${s}`] = {p1: F('CROUCH', 'y', [0, 0, -1]), p3: F('UPRIGHT', 'y', [0, 0, -1])};
  for (const x of ['1', '2']) FRAMES[`hair_${s}_${x}`] = {p1: F('CROUCH', 'y', [0, 0, -1]), p3: F('UPRIGHT', 'y', [0, 0, -1])};
  for (const x of ['a', 'b']) FRAMES[`mantle_${s}_${x}`] = {p1: F('CROUCH', 'y', [0, 1, 0]), p3: F('UPRIGHT', 'y', [0, 0, 1])};
  FRAMES[`beads_${s}`] = {p1: F('UPRIGHT', 'y', [0, 0, -1]), p3: F('UPRIGHT', 'y', [0, 0, -1])};
  void sx;
}
for (const n of ['hem_a', 'hem_b']) FRAMES[n] = {p1: F('CROUCH', 'y', [0, 0, -1]), p3: F('UPRIGHT', 'y', [0, 0, -1])};
for (const n of TAIL_PARTS) FRAMES[n] = {p1: F('CROUCH', 'z', [0, 1, 0]), p3: F('CROUCH', 'z', [0, 1, 0])};
// the hood is authored as the cowl in both forms (the crawl hood closes over the face; plan R2 hood_hinge swings it back)
FRAMES.hood = {p1: F('CROUCH'), p3: F('CROUCH')};
FRAMES.crown = {p1: F('CROUCH'), p3: F('UPRIGHT')};
// the P3 hands are authored per variant use: B / C leaf hands as held in the UPRIGHT stance, the A fork raised
// the abdomen: the P1 rear body along the crouch, the P3 robe stem hanging in the upright
// Bone direction at a solved pose (joint -> carried tip).
function boneDir(o, n) {
  const b = BONE[n];
  if (!b.tip) return null;
  return unit(sub(carry(o, n, b.tip), o[n].t));
}
// Authoring frame A (world, at the reference pose o) of part n for a frame spec.
export function authorFrame(o, n, spec, side = 'l') {
  if (spec.kind === 'w') return Q0;
  const d = boneDir(o, n);
  const f = side === 'r' && spec.front ? mx(spec.front) : spec.front || [0, 0, -1];
  if (spec.kind === 'y') return aimQ(d, f);
  // 'z': model +Z along d, model +Y toward f
  const Z = d, Y = unit(perp(f, Z).some(Math.abs) ? perp(f, Z) : perp([0, 1, 0], Z)), X = cross(Y, Z);
  return basisQ(X, Y, Z);
}

// ---- display transforms ---------------------------------------------------------------------------------------------------
// refs = {CROUCH: solved o, UPRIGHT: solved o} (the stance rest poses); M[form][part] = R_ref^-1 * A.
export function modelFrames(refs) {
  const M = {p1: {}, p3: {}};
  for (const n of PART_NAMES) for (const f of ['p1', 'p3']) {
    const spec = FRAMES[n][f], o = refs[spec.ref], side = /_r(_|$)/.test(n) ? 'r' : 'l';
    M[f][n] = mul(inv(o[n].R), authorFrame(o, n, spec, side));
  }
  return M;
}
// Display transform of part n in pose o for form f ({t, q, s} in display space, the part's display scale applied).
export function toDisplay(n, o, M, f, k = 1) {
  const v = o[n], Q = mul(v.R, M[f][n]), s = v.s * PART_SCALE[n] * k;
  return {t: toDisplayT(v.t), q: toDisplayQ(Q), s: [s, s, s]};
}
// A model-frame point (blocks, as authored in the region module) of part n -> rig frame, for this pose and form.
export const modelPoint = (o, M, f, n, P) => add(o[n].t, rot(mul(o[n].R, M[f][n]), times(P, o[n].s)));

// ---- hit proxies (plan R7; ground columns, rigtech §3.3) ----------------------------------------------------------------------
// [name, part (the framework's flash / dedupe part), flash group, width (max of the two stance widths, contract D2),
//  ground point: [bone, bind point], top: [[bone, bind point], ...] (the column top = the highest + margin), margin]
// The ground point of each column is a point carried by a bone; the top follows the highest of its top points.
export const PROXIES = [
  ['head', 'head', 'head', 2.8, ['head', [0, 2.7, -3.35]], [['hood', [0, 4.4, -2.6]], ['crown', [0, 4.9, -2.55]]], -.4],
  ['chest', 'chest', 'body', 3.0, ['chest', [0, 2.1, -.05]], [['shoulders', [0, 4.45, -.9]]], .5],
  ['abd', 'abdomen', 'rear', 2.6, ['abdomen', [0, 2.4, 2.0]], [['abdomen', [0, 3.5, 1.8]]], .5],
  ['tail_a', 'tail_3', 'tail', 1.8, ['tail_4', [.2, .25, 6.1]], [['tail_4', [.2, 1.3, 6.1]]], .7],
  ['tail_b', 'tail_6', 'tail', 1.8, ['tail_7', [1.35, .2, 9.4]], [['tail_7', [1.35, 1.3, 9.4]]], .7],
  ...SIDES.flatMap(s => {
    const m = s === 'l' ? v => v : mx;
    return [
      [`a_${s}`, `a_hand_${s}`, 'arms', 1.8, [`a_hand_${s}`, m([5.1, .3, -2.5])], [[`a_lo_${s}`, m([3.6, 2.4, -1.7])]], -.1],
      [`b_${s}`, `b_hand_${s}`, 'front', 2.2, [`b_hand_${s}`, m([2.45, .3, -3.4])], [[`b_lo_${s}`, m([2.3, 2.0, -2.4])]], 1.0],
      [`c_${s}`, `c_hand_${s}`, 'rear', 1.8, [`c_hand_${s}`, m([2.95, .3, 2.75])], [[`c_lo_${s}`, m([2.6, 2.2, 1.9])]], .8],
    ];
  }),
];
// Proxy columns of a solved pose: {name: {x, z, top, w}} in the rig frame (+x = the boss's left, -z = its front);
// top = 0 while every carrying part is hidden (vis 0).
export function proxyPoints(o) {
  const out = {};
  for (const [nm, , , w, [gb, gp], tops, margin] of PROXIES) {
    const G = carry(o, gb, gp);
    const top = Math.max(...tops.map(([b, P]) => carry(o, b, P)[1])) + margin;
    const hidden = o[gb].s < 1e-3;
    out[nm] = {x: +G[0].toFixed(2), z: +G[2].toFixed(2), top: hidden ? 0 : +Math.max(1.0, top).toFixed(2), w};
  }
  return out;
}
// Local px column [x, z, top] (contract §0.4.2: local = (rig.x, rig.y, -rig.z)).
export const pxLocal = c => [c.x, +(-c.z).toFixed(2) || 0, c.top];

// ---- push capsules (plan R11, contract §0.4.6: boxes f0 <= f <= f1, |s| < hw, local; + the plan column) ------------------------
const cap = (f, r) => ({f0: +(f - r).toFixed(2), f1: +(f + r).toFixed(2), hw: r, col: {f, r}});
export const CAPSULES = {sac: cap(1.0, 1.0), hips: cap(-1.0, 1.2), stem: cap(0.0, 1.4)};

// ---- rest anchors (contract §0.4.3; local frame) ---------------------------------------------------------------------------
// [bone, bind point (rig frame, CROUCH)] carried by the bone; the face, core, crown and hood-top anchors depend on the
// form (each form's model sits elsewhere on its part): FORM_POINTS give them as model points of the shown form.
export const ANCHOR_POINTS = {
  pelvis: ['pelvis', [0, 2.8, 1.0]], thorax: ['chest', J.chest], shoulder: ['shoulders', J.shoulders], head: ['head', J.head],
  hood_front: ['hood', [0, 3.0, -4.0]], tail_root: ['tail_1', TAIL_C[0]], tail_tip: ['tail_tip', TAIL_C[8]],
  ...Object.fromEntries(SIDES.flatMap(s => LIMBS.map(L => [`hand_${L}_${s}`, [`${L}_hand_${s}`, (s === 'l' ? v => v : mx)(LIMB_C[L][3])]]))),
};
// Per-form model points (part, point in the form's authoring frame about the joint; region modules author them there):
//   face  P1 the bud skull under the cowl (crouch) | P3 the mask centre, (0, 6.9, -0.9) in the UPRIGHT stance
//   core  P1 the belly sac centre (0, 1.7, -1.0) in the crouch | P3 the sternum centre (0, 4.4, -0.7) upright
//   crown P1 the crown cone tip (0, 5.0, -2.55) | P3 the glowing bud at the fan centre
//   hood_top P1 the cowl top (0, 4.4, -2.6) | P3 the peak (the cowl's front tip swung up, 8.5 b upright)
export const FORM_POINTS = {
  face: {p1: ['face', [0, -.5, -1.35]], p3: ['face', [0, .82, -.56]]},
  core: {p1: ['core', [0, -.5, -.15]], p3: ['core', [0, -.42, .41]]},
  crown: {p1: ['crown', [0, 1.2, .55]], p3: ['crown', [0, .45, -.82]]},
  hood_top: {p1: ['hood', [0, .64, -.67]], p3: ['hood', [0, -.76, -2.07]]},
};
export const toLocal = P => [+P[0].toFixed(2) || 0, +P[1].toFixed(2) || 0, +(-P[2]).toFixed(2) || 0];
