// Pose -> part transforms for the Corrupted Guardian rig (forward kinematics + arm IK).
// A pose is a full set of channels (DEFAULT_POSE merged with clip keys, see guardian_clips.mjs):
//   pos [x,y,z]   root offset from the anchor (the floor point under her); y holds the hover
//   rot [p,y,r]   root rotation about the body centre ROOT_PIVOT
//   pelvis, skirtF, skirtO, tail, legR, legL, torso, head, bracket, shield, wing   eulers (deg)
//   wc, ws, wp    wing tier opening deltas (deg, + = outward and up)
//   grip [x,y,z]  right-hand grip point on the shaft (body space, before the root transform)
//   spear q       spear frame (sp(tip, face)); sAt slides the spear through the hand (blocks
//                 toward the tip); spearS 0 hides it (detached / thrown)
//   rFree 0..1    right wrist follows rw/rq instead of the spear; rPole elbow hint
//   lOn 0..1      left hand on the shaft at lAt blocks from the right hand toward the tip;
//                 otherwise the free wrist lw / hand frame lq; lPole elbow hint
//   halo, glow    halo and halo glow scale; fx spear glow (0 = off); trail 0/1; vis overall,
//                 bodyVis everything but the spear (entrance, death)
//   cubes         spread of the floating body cubes; rHand / lHand discrete hand models
import {add, sub, times, lerp, dot, cross, len, unit, mul, q, rot, slerp, basisQ, aimQ, ik, armFront, steadyPerp, toDisplayT, toDisplayQ} from './guardian_rig_math.mjs';
import {PART_SCALE, VOX_REST} from './guardian_geometry.mjs';

export const ROOT_PIVOT = [0, 1.9, 0];
const HIP = [0, 1.78, 0], WAIST = [0, 1.85, 0];
const R_ARM = [.5, .48], L_ARM = [.48, .46], HAND_GRIP = .14;
const BRACKET_REST = q([0, 8, 24]), SHIELD_REST = q([0, 0, -62]), WING_REST = q([0, -12, -16]), TAIL_REST = q([0, 0, 10]);
const perp = (v, a) => sub(v, times(a, dot(v, a)));
const toQ = v => (v.length === 4 ? v : q(v));
// fixed compound turn of the lower-body voxel displays (guardian_geometry.mjs VOX_REST)
const VOX_Q = Object.fromEntries(Object.entries(VOX_REST).map(([k, e]) => [k, q(e)]));

// Fist frame around the shaft: model X along the shaft (toward the tip), model -Y from the
// wrist to the shaft.
function fistQ(T, F) { const Y = times(F, -1); return basisQ(T, Y, cross(T, Y)); }

// prev: the previous frame's arm bend directions {rV, lV} (IK continuity, see ik()), fist
// directions {rF, lF} and segment roll references {rU, rFo, lU, lFo} (steadyPerp); the result
// carries this frame's in o._bend.
export function solve(p, {warn, prev = null} = {}) {
  const o = {};
  const R0 = q(p.rot), shift = p.pos;
  const P = q(p.pelvis);
  const part = (n, t, Q, s = 1) => { o[n] = {t, q: Q, s: Array.isArray(s) ? s : [s, s, s]}; };
  // lower body
  part('pelvis', HIP, P);
  part('skirt_f', add(HIP, rot(P, [0, -.04, -.1])), mul(P, q(p.skirtF)));
  part('skirt_o', add(HIP, rot(P, [0, -.04, 0])), mul(P, q(p.skirtO)));
  part('tail', add(HIP, rot(P, [.24, -.08, .08])), mul(mul(P, q(p.tail)), TAIL_REST));
  part('leg_r', add(HIP, rot(P, [-.1, -.18, .02])), mul(mul(P, q(p.legR)), VOX_Q.leg_r));
  part('leg_l', add(HIP, rot(P, [.1, -.18, .02])), mul(mul(P, q(p.legL)), VOX_Q.leg_l));
  // the trail hangs under the feet and follows the mean leg swing; one slow tumble, out of phase
  // with the root bob, on top of the per-cube drift frames (the clips swap cubes_b_<n>)
  const Lq = mul(P, slerp(q(p.legR), q(p.legL), .5)), w = p.ph * 2 * Math.PI;
  part('cubes_b', add(add(add(HIP, rot(P, [0, -.18, .02])), rot(Lq, [.04, -1.44, 0])), [0, Math.sin(w + 2.2) * .035, 0]),
    mul(mul(Lq, q([4 * Math.sin(w + .9), 10 * Math.sin(w), 5 * Math.sin(w + 2.6)])), VOX_Q.cubes_b), p.cubes);
  // upper body
  const Tq = q(p.torso);
  part('torso', WAIST, Tq);
  const neck = add(WAIST, rot(Tq, [0, .76, 0])), Hq = mul(Tq, q(p.head));
  part('head', neck, Hq);
  part('halo', add(neck, rot(Hq, [0, .25, .15])), Hq, p.halo);
  part('halo_glow', add(neck, rot(Hq, [0, .25, .19])), Hq, p.glow);
  part('cubes_c', add(add(neck, rot(Tq, [-.2, -.12, .08])), [0, Math.cos(p.ph * 2 * Math.PI) * .03, 0]), mul(Tq, q([10, -30 * Math.sin(p.ph * 2 * Math.PI), 0])), p.cubes);
  const front = rot(Tq, [0, 0, -1]);
  const Rs = add(WAIST, rot(Tq, [-.3, .56, 0])), Ls = add(WAIST, rot(Tq, [.3, .56, 0]));
  // spear and right arm
  const S = toQ(p.spear), T = rot(S, [0, 1, 0]), G = p.grip;
  part('spear', sub(G, times(T, p.sAt)), S, p.spearS);
  // glow width grows gently with fx (idle 0.55 -> about 0.4 b of aura around the blade)
  const gw = .7 + .4 * p.fx;
  part('spear_glow', sub(G, times(T, p.sAt)), S, p.fx > .01 && p.spearS > .01 ? [gw * p.spearS, p.spearS, gw * p.spearS] : 0);
  // fist reference: from the shoulder to the shaft, or toward rPalm where a clip sets it (spins)
  const kP = Math.min(1, len(p.rPalm)), Fref = kP > 1e-3 ? add(times(unit(sub(G, Rs)), 1 - kP), times(unit(p.rPalm), kP)) : sub(G, Rs);
  const Fr = steadyPerp(Fref, T, prev && prev.rF, front);
  const gripW = sub(G, times(Fr, HAND_GRIP)), gripQ = fistQ(T, Fr);
  const rW = lerp(gripW, p.rw, p.rFree);
  const rQ = p.rFree > 0 ? slerp(gripQ, toQ(p.rq), p.rFree) : gripQ;
  const RA = ik(Rs, rW, ...R_ARM, p.rPole, prev && prev.rV);
  if (warn && RA.short > .02) warn(`right wrist out of reach by ${RA.short.toFixed(2)} b`);
  // segment roll: the inside of the bend faces the segment front (armFront), turning at most
  // 55 degrees per frame about the segment (steadyPerp), so a moving bend plane cannot spin it
  const roll = (dir, v, key) => steadyPerp(armFront(dir, v, front), unit(dir), prev && prev[key]);
  const rU = roll(sub(RA.E, Rs), RA.v, 'rU'), rFo = roll(sub(RA.W, RA.E), RA.v, 'rFo');
  part('r_upper', Rs, aimQ(sub(RA.E, Rs), rU), [1, len(sub(RA.E, Rs)) / R_ARM[0], 1]);
  part('r_fore', RA.E, aimQ(sub(RA.W, RA.E), rFo), [1, len(sub(RA.W, RA.E)) / R_ARM[1], 1]);
  part('r_hand', RA.W, rQ, 1);
  // cubes peel off the top-back of the corrupted shoulder (model.md §3.9), clear of the arm
  part('cubes_a', add(Rs, add(rot(Tq, [-.17, .1, .12]), [0, Math.sin(p.ph * 2 * Math.PI + 1.3) * .05, 0])), mul(Tq, q([0, 40 * Math.sin(p.ph * 2 * Math.PI + .7), 15])), p.cubes);
  // left arm: free claw or a hand on the shaft
  const LG = add(G, times(T, p.lAt));
  const Fl = steadyPerp(sub(LG, Ls), T, prev && prev.lF, front);
  const lGripW = sub(LG, times(Fl, HAND_GRIP)), lGripQ = fistQ(T, Fl);
  const lW = lerp(p.lw, lGripW, p.lOn);
  const lQ = slerp(toQ(p.lq), lGripQ, p.lOn);
  const LA = ik(Ls, lW, ...L_ARM, p.lPole, prev && prev.lV);
  if (warn && p.lOn > .5 && LA.short > .02) warn(`left wrist out of reach by ${LA.short.toFixed(2)} b`);
  const lU = roll(sub(LA.E, Ls), LA.v, 'lU'), lFo = roll(sub(LA.W, LA.E), LA.v, 'lFo');
  part('l_upper', Ls, aimQ(sub(LA.E, Ls), lU), [1, len(sub(LA.E, Ls)) / L_ARM[0], 1]);
  part('l_fore', LA.E, aimQ(sub(LA.W, LA.E), lFo), [1, len(sub(LA.W, LA.E)) / L_ARM[1], 1]);
  part('l_hand', LA.W, lQ, 1);
  // bracket, shield, wing
  const B = add(WAIST, rot(Tq, [.28, .64, .06])), Bq = mul(mul(Tq, q(p.bracket)), BRACKET_REST);
  part('bracket', B, Bq);
  const Sc = add(B, rot(Bq, [.92, 0, 0])), Sq = mul(mul(Bq, q(p.shield)), SHIELD_REST);
  part('shield', Sc, Sq);
  part('shield_eye', Sc, Sq);
  const Wr = add(WAIST, rot(Tq, [.62, .42, .16])), Wq = mul(mul(Tq, q(p.wing)), WING_REST);
  part('wing_cov', Wr, mul(Wq, q([0, 0, p.wc])));
  part('wing_sec', Wr, mul(Wq, q([0, 0, p.ws])));
  part('wing_pri', Wr, mul(Wq, q([0, 0, p.wp])));
  // root transform, visibility, display scale
  for (const v of Object.values(o)) {
    v.t = add(add(ROOT_PIVOT, rot(R0, sub(v.t, ROOT_PIVOT))), shift);
    v.q = mul(R0, v.q);
  }
  // visibility: vis scales everything about the body centre, bodyVis everything but the spear
  const c = add(ROOT_PIVOT, shift);
  for (const [n, v] of Object.entries(o)) {
    const k = p.vis * (n.startsWith('spear') ? 1 : p.bodyVis);
    if (k !== 1) { v.t = add(c, times(sub(v.t, c), n.startsWith('spear') ? p.vis : k)); v.s = times(v.s, k); }
  }
  Object.defineProperty(o, '_bend', {value: {rV: RA.v, lV: LA.v, rF: Fr, lF: Fl, rU, rFo, lU, lFo}, enumerable: false});
  return o;
}
// Rig frame -> display transform {t, q, s} with the part's display scale applied.
export function toDisplay(name, v, scaleName = name) {
  const k = PART_SCALE[scaleName];
  return {t: toDisplayT(v.t), q: toDisplayQ(v.q), s: v.s.map(x => x * k)};
}
