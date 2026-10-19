// Pose -> part transforms of the 야타용왕 (Azhdaha) rig: the skeleton, forward kinematics, the bake-time foot IK and
// the hit-proxy points. Shared math: mboss_rig_math.mjs. Scale and proportions: scratchpad az/plan.md R1-R2,
// az/understand/model.md §1-§3 (H = 7.0 b) and az/understand/motion.md §2 (joint heights x 0.91, the tree bones dropped:
// the leafy branch is the tail tip).
//
// Rig frame: +X = the boss's LEFT, +Y up, -Z forward, blocks; the origin is the floor point under the centre of the
// four feet (the anchor). Euler triples are degrees applied X, then Y, then Z (mboss_rig_math q): pitch + raises the
// nose (a bone pointing forward) and lowers a bone pointing back; yaw + turns the front toward the boss's right
// (-X); roll + tips the top toward the boss's right.
//
// A pose is a full set of channels (DEFAULT_POSE in azhdaha_clips.mjs merged with the clip keys):
//   pos [0, y, 0]          root offset (y only: jumps, the burrow sink to -7.5; x / z stay 0, the module moves the body)
//   rot [p, y, r]          root rotation about ROOT_PIVOT (whole-body tilt; the burrow pitch)
//   pelvis spine chest     eulers of the spine chain (pelvis about the hip line: the rear-ups)
//   neck1 neck2 head       eulers of the neck chain and the head (about the atlas)
//   jaw                    jaw opening, degrees (0 closed .. 50 wide)
//   beard1 beard2 apron    eulers of the hanging plates (secondary motion)
//   flN flS flM flH        plate-group flare (deg, + = bristle up and out) of the neck ruff, shoulder crest, mid-back
//                          and hip groups; flK their common scale (1 .. 1.15)
//   fwL fwR                fore-paw WRIST targets [x, y, z] in the root frame; fpL fpR paw eulers (root frame;
//                          [0,0,0] = flat on the floor, pitch - curls the claws down)
//   hkL hkR                hind HOCK targets [x, y, z] in the root frame; hfL hfR foot eulers (root frame)
//   t1 .. t8               tail segment eulers relative to the previous segment (pitch - raises a segment: it points
//                          back, so up = negative pitch; use the tail* helpers in azhdaha_clips.mjs)
//   tLift tCurl tSweep tTwist   parametric tail: tLift raises t1 (deg, up +), tCurl adds per segment (up +), tSweep
//                          is the total yaw spread evenly over the chain (+ = the tail swings to the boss's left),
//                          tTwist the total roll; all added to t1..t8
//   vis visBody visTail    visibility scales (0 hides; burrow / tail-only); visBody = everything but the tail
import {add, sub, times, mul, q, rot, len, unit, aimQ, ik, toDisplayT, toDisplayQ} from './mboss_rig_math.mjs';

export const H = 7.0;
export const ROOT_PIVOT = [0, 2.8, .4];
// ---- rest skeleton (rig frame, blocks) ----------------------------------------------------------------------------------
export const J = {
  pelvis: [0, 3.0, 2.4],          // hip line: rear-ups pivot here
  spine1: [0, 3.35, .3],          // mid-back
  chest: [0, 3.35, -1.7],         // shoulder girdle
  neck1: [0, 3.05, -2.55],
  neck2: [0, 2.6, -3.05],
  head: [0, 2.05, -3.7],          // atlas (R2: 0.4 further forward, neck ~1.7 b, the chin slam reaches z -5.5)
  jaw: [0, 1.3, -4.0],            // hinge under the ear
  beard1: [0, 1.05, -3.9],        // throat, under the jaw hinge
  beard2: [0, .72, -3.95],        // the lower layer hangs from the first
  apron: [0, 2.2, -2.8],          // throat plate, hangs between the fore legs
  t1: [0, 2.85, 4.75],            // tail root
  // left limbs (the right mirrors x)
  shoulder: [2.3, 3.25, -2.15], elbow: [2.95, 2.3, -1.8], wrist: [3.15, .5, -2.45],
  hip: [2.0, 3.0, 2.45], knee: [2.35, 1.9, 1.5], hock: [2.5, .72, 3.05],
  // plate-group bases (flare pivots) and crystal mounts
  plN: [0, 2.95, -2.85], plS: [0, 4.0, -1.75], plM: [0, 4.05, .25], plH: [0, 3.55, 2.4],
};
export const TAIL_LEN = [2.3, 2.1, 1.9, 1.8, 1.7, 1.6, 1.6, 1.5];   // 14.5 b (model.md §9)
export const ARM = [len(sub(J.elbow, J.shoulder)), len(sub(J.wrist, J.elbow))];
export const LEG = [len(sub(J.knee, J.hip)), len(sub(J.hock, J.knee))];
const mx = v => [-v[0], v[1], v[2]];

// Display scale per part (blocks per 16 model units; reach 1.5 x scale from the joint).
export const PART_SCALE = {
  chest: 3.0, belly: 3.0, pelvis: 2.8, neck1: 2.0, neck2: 2.0, apron: 1.8, glow_apron: 1.8,
  plates_neck: 2.0, plates_sh: 2.2, plates_mid: 2.2, plates_hip: 2.0, crys_sh: 2.2, crys_mid: 2.2, crys_hip: 2.0,
  head: 2.2, jaw: 2.0, eyes: 1.0, horn_l: 2.0, horn_r: 2.0, beard1: 1.4, beard2: 1.4,
  uarm_l: 1.8, bracer_l: 1.6, paw_l: 1.4, uarm_r: 1.8, bracer_r: 1.6, paw_r: 1.4,
  thigh_l: 2.0, gaiter_l: 1.6, foot_l: 1.4, thigh_r: 2.0, gaiter_r: 1.6, foot_r: 1.4,
  glow_bracer_l: 1.6, glow_bracer_r: 1.6, glow_gaiter_l: 1.6, glow_gaiter_r: 1.6,
  t1: 1.8, t2: 1.6, t3: 1.45, t4: 1.35, t5: 1.3, t6: 1.2, t7: 1.2, t8: 1.2, tip: 1.3,
};
// Rest lean of each plate group (deg, top toward the back): the plates are authored upright in the group frame and the
// group leans them back; the flare channels stand them up (bristle).
export const PLATE_LEAN = {neck: 35, sh: 12, mid: 15, hip: 25};
// BODY region: the bristle widens each plate group across X as it flares (a non-uniform display scale x = flK * (1 +
// PLATE_SPLAY * flare deg)), so the side rows roll further outward instead of the fan only growing (r1_critique 3.6).
export const PLATE_SPLAY = .012;
// BODY region (R2): the neck tubes are lofted along their own axis (no ring steps on a sloping neck), so the neck1 /
// neck2 parts carry the rest slope of their bone (a fixed nose-down pitch, deg) on top of the bone rotation; the neck
// models are authored in that tilted frame. Nothing else uses the neck part frames.
export const NECK_TILT = {neck1: Math.atan2(J.neck1[1] - J.neck2[1], J.neck1[2] - J.neck2[2]) * 180 / Math.PI,
  neck2: Math.atan2(J.neck2[1] - J.head[1], J.neck2[2] - J.head[2]) * 180 / Math.PI};
export const TAIL_PARTS = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 'tip'];
// Fixed placement of the horns in the head frame (the C of each horn is authored in its own YZ plane and turned out:
// yaw opens the back of the C outward, so the front shows "( )"; model.md §0).
export const HORN = {at: [1.8, -.15, -.35], e: [0, 53, 0]};   // R2: the C plane runs from the knob beside the mouth back to the temple
const Q0 = [0, 0, 0, 1];
const perpv = (v, a) => sub(v, times(a, v[0] * a[0] + v[1] * a[1] + v[2] * a[2]));
const inv = Q => [-Q[0], -Q[1], -Q[2], Q[3]];

// Rest bend directions of the limbs (the IK pole that reproduces the rest elbow / knee), in the chest / pelvis frame.
const poleOf = (S, E, W) => { const u = unit(sub(W, S)); return unit(perpv(sub(E, S), u)); };
const ARM_POLE = poleOf(J.shoulder, J.elbow, J.wrist), LEG_POLE = poleOf(J.hip, J.knee, J.hock);

// prev: the previous frame's limb bend directions (o._bend) for IK continuity (ik prevV).
export function solve(p, {prev = null} = {}) {
  const o = {};
  const part = (n, t, Q, s = 1) => { o[n] = {t, q: Q, s: Array.isArray(s) ? s : [s, s, s]}; };
  // spine chain: pelvis -> spine1 -> chest -> neck1 -> neck2 -> head -> jaw
  const bone = (parent, at, e) => {
    const T = parent ? add(parent.t, rot(parent.q, sub(at, parent.rest))) : at;
    return {t: T, q: parent ? mul(parent.q, q(e)) : q(e), rest: at};
  };
  const Bp = bone(null, J.pelvis, p.pelvis);
  const Bs = bone(Bp, J.spine1, p.spine), Bc = bone(Bs, J.chest, p.chest);
  const Bn1 = bone(Bc, J.neck1, p.neck1), Bn2 = bone(Bn1, J.neck2, p.neck2), Bh = bone(Bn2, J.head, p.head);
  const Bj = bone(Bh, J.jaw, [-p.jaw, 0, 0]);    // jaw opens chin-down (pitch - lowers a forward bone)
  const Bb1 = bone(Bj, J.beard1, p.beard1), Bb2 = bone(Bb1, J.beard2, p.beard2);
  const Ba = bone(Bc, J.apron, p.apron);
  const at = (B, v) => add(B.t, rot(B.q, sub(v, B.rest)));           // a rest-frame point carried by bone B
  part('pelvis', Bp.t, Bp.q); part('belly', Bs.t, Bs.q); part('chest', Bc.t, Bc.q);
  part('neck1', Bn1.t, mul(Bn1.q, q([-NECK_TILT.neck1, 0, 0]))); part('neck2', Bn2.t, mul(Bn2.q, q([-NECK_TILT.neck2, 0, 0])));
  part('head', Bh.t, Bh.q); part('jaw', Bj.t, Bj.q); part('eyes', Bh.t, Bh.q);
  part('beard1', Bb1.t, Bb1.q); part('beard2', Bb2.t, Bb2.q);
  part('apron', Ba.t, Ba.q); part('glow_apron', Ba.t, Ba.q);
  const Qh = q(HORN.e), Qhr = q([HORN.e[0], -HORN.e[1], -HORN.e[2]]);
  part('horn_l', add(Bh.t, rot(Bh.q, HORN.at)), mul(Bh.q, Qh));
  part('horn_r', add(Bh.t, rot(Bh.q, mx(HORN.at))), mul(Bh.q, Qhr));
  // plate groups (flare: pitch back + roll outward is not one axis, so the flare is a pitch about the group base;
  // the fan width comes from the scale flK) and the crystal clusters (rigid)
  const flare = (n, B, base, deg, g) => part(n, at(B, base), mul(B.q, q([PLATE_LEAN[g] - deg, 0, 0])), [p.flK * (1 + PLATE_SPLAY * deg), p.flK, p.flK]);
  flare('plates_neck', Bn2, J.plN, p.flN, 'neck'); flare('plates_sh', Bc, J.plS, p.flS, 'sh');
  flare('plates_mid', Bs, J.plM, p.flM, 'mid'); flare('plates_hip', Bp, J.plH, p.flH, 'hip');
  part('crys_sh', at(Bc, J.plS), Bc.q); part('crys_mid', at(Bs, J.plM), Bs.q); part('crys_hip', at(Bp, J.plH), Bp.q);
  // legs: two-bone IK to the wrist / hock targets (root frame), rest pole carried by the chest / pelvis
  const bend = {};
  const limb = (side, S, Wt, ab, pole, prevV, names, endQ) => {
    const R = ik(S, Wt, ab[0], ab[1], pole, prevV);
    const front = [0, 0, -1];
    part(names[0], S, aimQ(sub(R.E, S), front), [1, 1, 1]);
    part(names[1], R.E, aimQ(sub(R.W, R.E), front), [1, 1, 1]);
    part(names[2], R.W, endQ);
    return R;
  };
  for (const [s, k] of [[1, 'L'], [-1, 'R']]) {
    const sx = s > 0 ? 'l' : 'r', m = v => (s > 0 ? v : mx(v));
    const poleA = rot(Bc.q, m(ARM_POLE)), poleL = rot(Bp.q, m(LEG_POLE));
    const RA = limb(s, at(Bc, m(J.shoulder)), p['fw' + k], ARM, poleA, prev && prev['a' + k], [`uarm_${sx}`, `bracer_${sx}`, `paw_${sx}`], q(p['fp' + k]));
    const RL = limb(s, at(Bp, m(J.hip)), p['hk' + k], LEG, poleL, prev && prev['l' + k], [`thigh_${sx}`, `gaiter_${sx}`, `foot_${sx}`], q(p['hf' + k]));
    bend['a' + k] = RA.v; bend['l' + k] = RL.v;
    part(`glow_bracer_${sx}`, o[`bracer_${sx}`].t, o[`bracer_${sx}`].q);
    part(`glow_gaiter_${sx}`, o[`gaiter_${sx}`].t, o[`gaiter_${sx}`].q);
  }
  // tail chain from the pelvis: segment i points along +Z from its joint; the parametric channels add to t1..t8
  let T = at(Bp, J.t1), Qt = Bp.q;
  const n = TAIL_LEN.length;
  for (let i = 0; i < n; i++) {
    const e = p['t' + (i + 1)], up = (i === 0 ? p.tLift : 0) + p.tCurl;
    Qt = mul(Qt, q([e[0] - up, e[1] + p.tSweep / n, e[2] + p.tTwist / n]));
    part('t' + (i + 1), T, Qt);
    T = add(T, rot(Qt, [0, 0, TAIL_LEN[i]]));
  }
  part('tip', T, Qt);
  // root: offset and rotation about ROOT_PIVOT (applied to everything, the limb targets included: they are root-frame)
  const R0 = q(p.rot);
  for (const v of Object.values(o)) { v.t = add(add(ROOT_PIVOT, rot(R0, sub(v.t, ROOT_PIVOT))), p.pos); v.q = mul(R0, v.q); }
  // visibility (scale about each part's own joint: hidden parts collapse in place)
  for (const [nm, v] of Object.entries(o)) {
    const k = p.vis * (TAIL_PARTS.includes(nm) ? p.visTail : p.visBody);
    if (k !== 1) v.s = times(v.s, k);
  }
  Object.defineProperty(o, '_bend', {value: bend, enumerable: false});
  return o;
}
// Rig frame -> display transform {t, q, s} with the part's display scale applied.
export function toDisplay(name, v) {
  const k = PART_SCALE[name];
  return {t: toDisplayT(v.t), q: toDisplayQ(v.q), s: v.s.map(x => x * k)};
}
// A point given in a part's own frame (blocks, as authored in its region module) -> rig frame, for this pose.
export const pointOf = (o, n, pt) => { const v = o[n]; return add(v.t, rot(v.q, [pt[0] * v.s[0], pt[1] * v.s[1], pt[2] * v.s[2]])); };

// ---- hit proxies (rigtech.md §3.3: ground-anchored interaction columns on the bones) -----------------------------------
// [name, part, point in the part frame (blocks), w, top above the point (blocks), state flags]. tail_only = vulnerable
// in the phase-3 tail-only state.
export const PROXIES = [
  ['head', 'head', [0, -.6, -1.0], 2.8, 1.6, ''], ['chest', 'chest', [0, 0, -.4], 4.6, 1.5, ''], ['belly', 'belly', [0, 0, .2], 4.6, 1.5, ''],
  ['hips', 'pelvis', [0, 0, 1.0], 4.4, 1.2, ''],
  ['tail1', 't1', [0, 0, 1.6], 2.6, 1.2, 'tail_only'], ['tail2', 't3', [0, 0, 1.0], 2.2, 1.0, 'tail_only'],
  ['tail3', 't5', [0, 0, .9], 1.8, .9, 'tail_only'], ['tail4', 't7', [0, 0, 1.0], 1.4, .8, 'tail_only'],
  ['paw_l', 'paw_l', [0, -.3, -.5], 1.8, 2.6, ''], ['paw_r', 'paw_r', [0, -.3, -.5], 1.8, 2.6, ''],
  ['foot_l', 'foot_l', [0, -.4, -.5], 1.8, 2.6, ''], ['foot_r', 'foot_r', [0, -.4, -.5], 1.8, 2.6, ''],
];
// Proxy columns for a solved pose: {name: {x, z, base, top, w}} (rig frame; base = max(0, the point's floor
// projection), top = the bone point's height + its top margin). A part hidden by vis (scale 0) reports hidden: true.
export function proxyPoints(o) {
  const out = {};
  for (const [nm, pt, at, w, top] of PROXIES) {
    const v = o[pt], P = add(v.t, rot(v.q, at)), hidden = v.s[0] < 1e-3;
    out[nm] = {x: +P[0].toFixed(2), z: +P[2].toFixed(2), base: +Math.max(0, P[1] - 2).toFixed(2), top: +(P[1] + top).toFixed(2), w, ...(hidden ? {hidden: true} : {})};
  }
  return out;
}
export {Q0, inv};
