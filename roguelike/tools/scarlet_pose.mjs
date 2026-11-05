// Skeleton and pose solver of the 홍련 (Scarlet) rig (S:hr/PLAN.md §2.1-2.6). solve(p, hist) turns one pose (the channels
// below, sampled from scarlet_clips.mjs or S2b's scarlet_cine.mjs) into the rig-frame transform {t, q, s} of each of the 29
// parts. There is no runtime parenting: the look states that re-parent a part (hat worn / back / hand / world / gone,
// scabbard hand / hip / gone, cup / bottle hand / rock / none; api.REPARENT) are pose channels solved here every tick.
//
// Frames. Rig frame: +X her left, +Y up, -Z forward, blocks; the origin is the anchor (the boss body) on the floor.
// Quaternions [x, y, z, w]; eulers [pitch, yaw, roll] in degrees as mboss_rig_math.q (pitch + leans back / lifts the toes,
// yaw + turns her to her right, roll + tips the top toward her right). Bearings (dirBE): 0 = forward, + = her right.
//
// Pose channels (numbers / vectors interpolate; the discrete ones switch at their key: DISCRETE in scarlet_clips.mjs)
//   pos [x,y,z]        the pelvis offset (its pivot is 1.36 b above the floor at rest)
//   rot [p,y,r]        the pelvis: yaw = the facing of the whole figure, then pitch / roll of the hips
//   tor [p,y,r]        the torso about the waist;  head [p,y,r]  the head about the neck base
//   fL, fR [x,y,z]     ankle targets in the yaw frame from the floor point under the pelvis (y 0.10 = planted);
//   lf 0..1            blends the ankle targets into the pelvis frame (flips, tumbles, lying: the legs move with the body)
//   kL, kR [x,y,z]     knee poles (yaw frame; default forward)
//   hold 0|1           the sword in her LEFT hand (sword hand); 0 = the left arm free (aL / plL)
//   gB gE gD           the grip on a sphere about the swing centre (0.50 b above the pelvis pivot, yaw frame): bearing,
//                      elevation (deg), distance (b); interpolated as numbers, so a cut sweeps on an arc
//   gF gL              grip follow: 1 = the grip on the lever gL from her left shoulder (the chest centre with rh 1) along
//                      the blade, so a sweep turns about the shoulder
//   cB cR th ed tw     the blade: its tip at angle th in the cutting plane through bearing cB rolled by cR (0 vertical: th 0
//                      forward, 90 up; 90 horizontal: th + toward her left), the edge leading toward +th (ed 1) or -th
//                      (ed -1), twisted by tw about the blade (yaw frame)
//   rh 0..1            her right hand on the hilt below the left (two hands) .. free
//   aL, aR [p,r,k]     free hand targets about the shoulder (chest frame): pitch (+ forward / up), roll (+ out), reach 0..1
//   plL, plR [x,y,z]   planted hand targets (yaw frame from the floor point under the pelvis), weights plwL, plwR
//   pL, pR [x,y,z]     elbow poles (chest frame; x side-signed: + = outward);  frL, frR  free forearm roll (deg)
//   bwL, bwR 0..1      the hand to the hat brim (worn): the target is the brim edge at azimuth bzL / bzR (deg from her
//                      front, + toward the hand's side); pair with hand 'brim'
//   hiL 0..1           the left hand to the sheathed hilt (the iai grip; the draw); hsR 0..1 the right hand to the scabbard's
//                      throat at the hip;  scHip [p,y]  the hip scabbard turned about its mouth (deg, pelvis frame)
//   hairF 0..1, hairS  the ponytail falls with gravity / is swept forward (a turn, the wind)
//   vis 0..1           everything scaled about the body centre (the ghost vanish / reappear)
//   sh 0..1, shW 0..1  sheathing: the sword slides into the scabbard (sh 0 = the tip at the mouth, 1 = the guard at the
//                      mouth); shW blends the sword from the free blade frame onto the scabbard's axis
//   skF                the skirt flare scale (1 = rest); skG 0..1 the panels fall with gravity; skIF / skIB the front /
//                      back panel tops pulled in (blocks; lying on the back); skW the wind of a dash (+: the front panels
//                      pressed in, the back ones streaming out; - the other way)
//   hwP [x,y,z], hwE [p,y,r]   the hat in the world state (rig frame: relative to the root)
//   hhB hhE, hhN [b,e] the hat in the right hand: the direction hand -> brim centre (bearing / elevation, yaw frame) and
//                      the crown's direction
//   scB scE scR        the scabbard in the right hand: its body direction from the mouth (bearing, elevation; yaw frame)
//                      and its roll about the body (edge side); scOff where the hand grips it (blocks from the mouth)
//   cupP, botP [x,y,z] the cup / bottle on the rock (rig frame);  cupT, botT  their tilt in the hand (deg, pouring)
//   discrete: hat (worn|back|hand|world|gone), sword (hand|sheathed|gone), scab (hip|hand|gone), face (calm|smile|closed),
//             hL, hR (open|grip|brim), cup, bottle (none|hand|rock)
//   ph                 the loop phase 0..1 (idle sway, set by the sampler)
import {add, sub, times, len, unit, mul, q, rot, aimQ, ik, basisQ, cross, dot, perp, slerp, armFront, steadyPerp, toDisplayT, toDisplayQ, lerp} from './mboss_rig_math.mjs';
import {PART_NAMES, PART_SCALE, SWORD, SCAB, HAT, ARM, LEG, SKIRT, STRINGS, modelPoints, HAND_MODELS, FACE_MODELS, PHASE_MODELS, HIDDEN} from './scarlet_geometry.mjs';

export const HIP_Y = 1.36;
export const SK = {
  hipJ: [.105, -.08, 0], waist: [0, .14, 0], neckB: [0, .55, 0], shoulder: [.25, .43, .01],
  armU: ARM.upper, fore: ARM.fore + ARM.grip, thigh: LEG.thigh, shin: LEG.shin, ankleY: .10,
  hairRoot: [0, .2, .145], hairSeg: [.42, .44], lockRoot: [.13, .36, -.115],
  brim: [0, .45, 0], brimTilt: -6, hatBack: [0, .25, .225], hatHand: .76,
  sashKnot: [.215, .07, -.085], skirtTop: .045,
  scabHip: [-.2, .05, -.12], scabHipDir: [-.2, -.62, .76],
  swing: [0, .5, 0],
};
const D = Math.PI / 180;
export const dirBE = (b, e = 0) => { const B = b * D, E = e * D; return [-Math.sin(B) * Math.cos(E), Math.sin(E), -Math.cos(B) * Math.cos(E)]; };
const ID = [0, 0, 0, 1];
const safeAxis = v => (len(v) < 1e-4 ? [1, 0, 0] : unit(v));
// a gravity pull's weight fades out as the part turns past horizontal (no 180-degree fromTo flips when she is upside down)
const gfade = dn => Math.max(0, Math.min(1, .5 - dn[1]));
const conj = Q => [-Q[0], -Q[1], -Q[2], Q[3]];
// limit a chain direction's turn per tick to maxDeg, measured from the previous direction carried along by its root's own
// rotation since the previous tick (a flip or a spin turns the chain with the body; only the swing is rate-limited)
function rateLimit(d, pd, dq, maxDeg) {
  if (!pd) return d;
  const c = dq ? rot(dq, pd) : pd, ang = Math.acos(Math.max(-1, Math.min(1, dot(c, d))));
  if (ang <= maxDeg * D) return d;
  const ax = cross(c, d);
  return len(ax) > 1e-6 ? rot(qa(unit(ax), maxDeg), c) : d;
}
const qa = (axis, deg) => { const s = Math.sin(deg * D / 2); return [axis[0] * s, axis[1] * s, axis[2] * s, Math.cos(deg * D / 2)]; };
export function fromTo(a, b) {
  const c = cross(a, b), d = dot(a, b);
  if (d < -.9999) { const ax = unit(len(cross(a, [1, 0, 0])) > .1 ? cross(a, [1, 0, 0]) : cross(a, [0, 0, 1])); return [ax[0], ax[1], ax[2], 0]; }
  const w = 1 + d, m = Math.hypot(c[0], c[1], c[2], w);
  return [c[0] / m, c[1] / m, c[2] / m, w / m];
}
// blade frame: +Y along tip, the edge (model -Z) toward `edge`
export function bladeQ(tip, edge) {
  const Y = unit(tip); let Z = perp(times(edge, -1), Y);
  if (len(Z) < 1e-6) Z = perp([0, 0, 1], Y);
  Z = unit(Z);
  return basisQ(cross(Y, Z), Y, Z);
}

// ---- hulls (blocks, part space at display scale) ---------------------------------------------------------------------------
let HULLS = null;
const DIRS = (() => { const L = []; for (let i = -3; i <= 3; i++) for (let j = -3; j <= 3; j++) for (const [a, b, c] of [[1, i / 3, j / 3], [-1, i / 3, j / 3]]) L.push([a, b, c], [b, a, c], [b, c, a]); return L; })();
function support(pts) {
  if (pts.length <= 24) return pts;
  const keep = new Set();
  for (const d of DIRS) { let best = -Infinity, bi = 0; for (let i = 0; i < pts.length; i++) { const v = pts[i][0] * d[0] + pts[i][1] * d[1] + pts[i][2] * d[2]; if (v > best) { best = v; bi = i; } } keep.add(bi); }
  return [...keep].sort((x, y) => x - y).map(i => pts[i]);
}
export function setModels(models) {
  HULLS = {};
  for (const [n, els] of Object.entries(models)) {
    const seen = new Set(), pts = [];
    for (const P of modelPoints(els)) { const k = P.map(v => v.toFixed(3)).join(); if (!seen.has(k)) { seen.add(k); pts.push(P); } }
    HULLS[n] = support(pts);
  }
}
const HCACHE = new Map();
export const hullOf = (model, n) => {
  const key = model + '|' + n;
  if (!HCACHE.has(key)) { const k = PART_SCALE[n] / 16; HCACHE.set(key, (HULLS[model] || []).map(P => [P[0] * k, P[1] * k, P[2] * k])); }
  return HCACHE.get(key);
};
export function qm(Q) {
  const [x, y, z, w] = Q;
  return [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)], [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]];
}
const minY = (pts, t, Q, s = 1) => { const r = qm(Q)[1]; let m = Infinity; for (const P of pts) { const y = t[1] + s * (r[0] * P[0] + r[1] * P[1] + r[2] * P[2]); if (y < m) m = y; } return m; };
// guard bookkeeping of one solve: GUARD.min = {name: the smoothed minimum angle (second pass)}, GUARD.used = {name: angle}
let GUARD = {min: {}, used: {}, prefer: {}, sense: {}};
// turn a segment (pivot t, rotation Q, hull pts) about `axis` by the smallest angle (sense +1 / -1, or 0 = either) so its
// hull clears y >= clear; returns the new Q
function clearFloor(t, Q, pts, axis, clear, maxDeg = 100, sense = 1, name = null, s = 1) {
  const a0 = name ? GUARD.min[name] || 0 : 0;
  const try1 = sg => {
    const at = a => (a ? mul(qa(axis, sg * a), Q) : Q);
    let a = a0;
    if (minY(pts, t, at(a), s) < clear) {
      let lo = a, hi = null;
      for (let x = a + 4; x <= maxDeg; x += 4) if (minY(pts, t, at(x), s) >= clear) { hi = x; break; } else lo = x;
      if (hi === null) return [maxDeg + 1, at(maxDeg)];
      for (let k = 0; k < 7; k++) { const m = (lo + hi) / 2; if (minY(pts, t, at(m), s) >= clear) hi = m; else lo = m; }
      a = hi;
    }
    return [a, at(a)];
  };
  let best = sense ? try1(sense) : null;
  if (!sense) {
    // either sense: the smaller turn, but keep the sense the guard took last tick while it does the job (no flip-flop)
    const p1 = try1(1), p2 = try1(-1), pref = name ? GUARD.prefer[name] : 0;
    best = p1[0] <= p2[0] ? p1 : p2;
    if (pref) { const [P, O] = pref > 0 ? [p1, p2] : [p2, p1]; if (P[0] <= maxDeg && P[0] <= O[0] + 30) best = P; }
    if (name && best[0] > .5) GUARD.sense[name] = best === p1 ? 1 : -1;
  }
  if (name) GUARD.used[name] = Math.min(best[0], maxDeg);
  return best[1];
}

// ---- the item model a part shows in a pose (for its hull; the form / phase swaps keep the geometry) ---------------------------
export function modelOn(n, p) {
  if (HIDDEN.includes(n)) return 'empty';
  if (n === 'forearm_r') return HAND_MODELS.forearm_r[p.hR || 'open'];
  if (n === 'forearm_l') return HAND_MODELS.forearm_l[p.hL || 'grip'];
  if (n === 'face') return FACE_MODELS[p.face || 'calm'];
  if (n === 'hat') return PHASE_MODELS.hat.p1;
  if (n === 'sash_tails') return PHASE_MODELS.sash_tails.p1;
  if (n === 'sword_glow') return 'glow_lilac';
  if (n === 'hilt_sheathed') return 'hilt';
  return n;
}
// the rest radius of the panels and their mid azimuths (deg from her front toward her left)
const PANELS = [['skirt_fl', 45, 'l', SKIRT.dr[0]], ['skirt_fr', -45, 'r', SKIRT.dr[1]], ['skirt_bl', 135, 'l', SKIRT.dr[2]], ['skirt_br', -135, 'r', SKIRT.dr[3]]];
export const FLARE = 11;

// ---- solve -----------------------------------------------------------------------------------------------------------------
// p: full pose; hist(k): the solved output k ticks before (or null). Returns {part: {t, q, s}} (rig frame) plus
// non-enumerable extras (_anchors, _prev, _guard, _lift).
export function solve(p, hist = () => null, guardMin = {}) {
  const o = {};
  const part = (n, t, Q, s = 1) => { o[n] = {t, q: Q, s: Array.isArray(s) ? s : [s, s, s]}; };
  const prev = hist(1)?._prev || {}, keep = {};
  GUARD = {min: guardMin, used: {}, prefer: prev.gs || {}, sense: {}};
  const Ryaw = q([0, p.rot[1], 0]);
  const Pq = mul(Ryaw, q([p.rot[0], 0, p.rot[2]]));
  const R = [p.pos[0], HIP_Y + p.pos[1], p.pos[2]];
  const floorP = [p.pos[0], 0, p.pos[2]];
  part('pelvis', R, Pq);
  const Wst = add(R, rot(Pq, SK.waist)), Cq = mul(Pq, q(p.tor));
  part('torso', Wst, Cq);
  const Nb = add(Wst, rot(Cq, SK.neckB)), Hq = mul(Cq, q(p.head));
  part('head', Nb, Hq); part('face', Nb, Hq);
  const chestFwd = rot(Cq, [0, 0, -1]);

  // ---- legs (IK; each foot raised just enough that its boot stays on the floor) ----
  const segQ = (key, dir, front) => { const F = steadyPerp(front, unit(dir), prev['f_' + key], [0, 0, -1]); keep['f_' + key] = F; return aimQ(dir, F); };
  const lf = Math.max(0, Math.min(1, p.lf || 0));
  const legs = {};
  for (const [s, k, F, kp] of [[1, 'l', p.fL, p.kL], [-1, 'r', p.fR, p.kR]]) {
    const H = add(R, rot(Pq, [SK.hipJ[0] * s, SK.hipJ[1], SK.hipJ[2]]));
    const Aw = add(floorP, rot(Ryaw, F)), Ab = add(R, rot(Pq, [F[0], F[1] - HIP_Y, F[2]]));
    let A = lerp(Aw, Ab, lf);
    const pole = rot(lf > .5 ? Pq : Ryaw, kp || [s * .12, 0, -1]);
    const fwd = rot(lf > .5 ? Pq : Ryaw, [0, 0, -1]);
    let sol, thQ, shQ;
    for (let it = 0; it < 3; it++) {
      sol = ik(H, A, SK.thigh, SK.shin, pole, prev['leg' + k]);
      const kv = times(sol.v, -1);
      thQ = segQ('th' + k, sub(sol.E, H), armFront(sub(sol.E, H), kv, fwd));
      shQ = segQ('sh' + k, sub(sol.W, sol.E), armFront(sub(sol.W, sol.E), kv, fwd));
      const low = minY(hullOf('shin_' + k, 'shin_' + k), sol.E, shQ);
      if (low >= .004) break;
      A = add(A, [0, .006 - low, 0]);
    }
    part('thigh_' + k, H, thQ); part('shin_' + k, sol.E, shQ);
    keep['leg' + k] = sol.v;
    legs[k] = {H, E: sol.E, W: sol.W};
  }

  // ---- arms ----
  const shoulderOf = s => add(Wst, rot(Cq, [SK.shoulder[0] * s, SK.shoulder[1], SK.shoulder[2]]));
  const SL = shoulderOf(1), SR = shoulderOf(-1);
  const armDir = (a, side) => { const P = a[0] * D, B = a[1] * D * side, y = -Math.cos(P), z = -Math.sin(P); return [-y * Math.sin(B), y * Math.cos(B), z]; };
  const poleOf = (pp, s) => rot(Cq, pp ? [pp[0] * s, pp[1], pp[2]] : [s * .55, -.35, .75]);
  const armSolve = (k, S, target, pole) => { const sol = ik(S, target, SK.armU, SK.fore, pole, prev['arm' + k]); keep['arm' + k] = sol.v; return sol; };
  // the scabbard at the hip (needed by the hands' targets): the mouth at the right hip's front, the body back and down,
  // the edge up, turned (scHip) and lifted off the floor if needed
  const scHipT = add(R, rot(Pq, SK.scabHip));
  const sh0 = p.scHip || [0, 0];
  let scHipQ = mul(Pq, mul(q([sh0[0], sh0[1], 0]), bladeQ(SK.scabHipDir, [0, 1, 0])));
  scHipQ = clearFloor(scHipT, scHipQ, hullOf('scabbard', 'scabbard'), rot(Pq, [1, 0, 0]), .03, 80, 0, 'scab');
  let scT = null, scQ = null;
  const hiltOf = () => add(scT || scHipT, rot(scQ || scHipQ, [0, -.185, 0]));
  // the hat's worn frame (needed for the brim targets of the hands)
  const hatWornQ = mul(Hq, q([SK.brimTilt, 0, 0])), hatWornT = add(Nb, rot(Hq, SK.brim));
  const brimPoint = (az, side) => add(hatWornT, rot(hatWornQ, times(dirBE(-side * az, 0), HAT.R - .04)));
  const freeTarget = (S, a, side, k) => {
    let T = add(S, times(rot(Cq, armDir(a, side)), a[2] * (SK.armU + SK.fore)));
    const w = side > 0 ? (p.plwL || 0) : (p.plwR || 0), P = side > 0 ? p.plL : p.plR;
    if (w > 0 && P) T = lerp(T, add(floorP, rot(Ryaw, P)), w);
    const bw = side > 0 ? (p.bwL || 0) : (p.bwR || 0);
    if (bw > 0) T = lerp(T, sub(brimPoint(side > 0 ? (p.bzL ?? 35) : (p.bzR ?? 35), side), [0, .03, 0]), bw);
    if (side > 0 && (p.hiL || 0) > 0) T = lerp(T, hiltOf(), p.hiL);
    if (side < 0 && (p.hsR || 0) > 0) T = lerp(T, add(scHipT, rot(scHipQ, [0, .14, 0])), p.hsR);
    void k;
    return T;
  };
  // the blade (as tachy_pose: plane bearing cB, roll cR, angle th; edge leading by ed; twist tw)
  const u0 = rot(Ryaw, dirBE(p.cB, 0)), v0 = rot(qa(u0, p.cR), rot(Ryaw, [0, 1, 0]));
  const T0 = add(times(u0, Math.cos(p.th * D)), times(v0, Math.sin(p.th * D)));
  let Ed = add(times(u0, -Math.sin(p.th * D)), times(v0, Math.cos(p.th * D)));
  const twist = 90 * (1 - Math.max(-1, Math.min(1, p.ed))) + (p.tw || 0);
  if (Math.abs(twist) > 1e-6) Ed = rot(qa(T0, twist), Ed);
  let SQ = bladeQ(T0, Ed);
  const Cw = add(R, rot(Ryaw, SK.swing));
  const Gs = add(Cw, times(rot(Ryaw, dirBE(p.gB, p.gE)), p.gD));
  const Gf = add(lerp(SL, Cw, Math.min(1, p.rh || 0)), times(T0, p.gL || .55));
  let G = lerp(Gs, Gf, p.gF || 0);

  // ---- scabbard (needed before the sheathe) ----
  const scab = p.scab || 'hip';

  // the right arm: free / on the hilt (rh) / holding the scabbard by its throat (scab hand) / at the brim
  let solR, gripR;
  const hrold = scab === 'hand';
  if (hrold) {
    const d = rot(Ryaw, dirBE(p.scB ?? 0, p.scE ?? 80));
    const tgt = freeTarget(SR, p.aR, -1, 'r');
    solR = armSolve('r', SR, tgt, poleOf(p.pR, -1));
    gripR = sol2grip(solR);
    scQ = mul(qa(unit(d), p.scR || 0), bladeQ(d, rot(Ryaw, [0, 0, -1])));
    scT = sub(gripR, times(unit(d), p.scOff || 0));
  } else {
    const rh = (p.hold ?? 1) > .5 ? Math.max(0, Math.min(1, p.rh || 0)) : 0;
    const sy = rot(SQ, [0, 1, 0]);
    const G2 = add(G, times(sy, -.13));
    const tF = freeTarget(SR, p.aR, -1, 'r');
    solR = armSolve('r', SR, lerp(tF, G2, rh), poleOf(p.pR, -1));
    gripR = sol2grip(solR);
  }
  if (!scT) { scT = scHipT; scQ = scHipQ; }

  // sheathing: the sword onto the scabbard's axis, sliding in (sh 0 = the tip at the mouth, 1 = the guard at the mouth)
  const shW = Math.max(0, Math.min(1, p.shW || 0));
  if (shW > 0) {
    const ax = rot(scQ, [0, 1, 0]), back = times(ax, -1);
    const depth = (p.sh || 0) * (SWORD.tip - SWORD.guard);
    const Gsh = add(scT, times(back, SWORD.tip - depth));
    const SQsh = mul(fromTo(rot(SQ, [0, 1, 0]), ax), SQ);
    const edgeQ = bladeQ(ax, rot(scQ, [0, 0, -1]));
    G = lerp(G, Gsh, shW); SQ = slerp(SQ, slerp(SQsh, edgeQ, .7), shW);
  }
  // the left arm: the sword hand (the grip point = the hand) or free / at the brim
  let solL, gripL;
  if ((p.hold ?? 1) > .5) {
    solL = armSolve('l', SL, G, poleOf(p.pL, 1));
    gripL = sol2grip(solL);
    // the grip follows the hand where the arm falls short
    if (len(sub(gripL, G)) > .002 && shW < .5) G = gripL;
  } else {
    solL = armSolve('l', SL, freeTarget(SL, p.aL, 1, 'l'), poleOf(p.pL, 1));
    gripL = sol2grip(solL);
  }
  // segments of both arms. S2c: the arms are skin boxes one pixel outward of the bone, so the forearm keeps the upper arm's
  // roll (both framed by the bend: armFront), the elbow stays aligned; S2a's knuckle turn toward the held blade / scabbard
  // and the free roll frL / frR (the hand shapes) have no effect on a box hand and are not applied
  for (const [k, S, sol] of [['l', SL, solL], ['r', SR, solR]]) {
    const up = sub(sol.E, S), fo = sub(sol.W, sol.E);
    part('arm_' + k, S, segQ('ua' + k, up, armFront(up, sol.v, chestFwd)));
    part('forearm_' + k, sol.E, segQ('fa' + k, fo, armFront(fo, sol.v, chestFwd)));
  }

  // ---- sword, glow, scabbard, sheathed hilt ----
  const sw = p.sword || 'hand';
  if (sw === 'hand' && shW < .5) SQ = groundSword(G, SQ, rot(Ryaw, [0, 0, -1]));
  const swS = sw === 'hand' ? 1 : 0;
  part('sword', G, SQ, swS); part('sword_glow', G, SQ, swS);
  const scS = scab === 'gone' ? 0 : 1;
  part('scabbard', scT, scQ, scS);
  part('hilt_sheathed', scT, scQ, sw === 'sheathed' && scab !== 'gone' ? 1 : 0);

  // ---- hat (worn / back / hand / world / gone) and its strings ----
  const hat = p.hat || 'worn';
  let hT, hQ, hS = 1;
  if (hat === 'worn') { hT = hatWornT; hQ = hatWornQ; }
  else if (hat === 'back') { hT = add(Wst, rot(Cq, SK.hatBack)); hQ = mul(Cq, q([90, 0, 0])); }
  else if (hat === 'hand') {
    const D1 = unit(rot(Ryaw, dirBE(p.hhB ?? -90, p.hhE ?? 0))), N1 = unit(rot(Ryaw, dirBE(...(p.hhN || [-90, 0]))));
    hT = add(gripR, times(D1, SK.hatHand));
    let Nn = perp(N1, D1); if (len(Nn) < 1e-3) Nn = perp([0, 1, 0], D1);
    hQ = basisQ(cross(unit(Nn), unit(times(D1, -1))), unit(Nn), unit(times(D1, -1)));
  } else if (hat === 'world') { hT = [...(p.hwP || [.9, .02, -.4])]; hQ = mul(Ryaw, q(p.hwE || [0, 0, 0])); }
  else { hT = hatWornT; hQ = hatWornQ; hS = 0; }
  if (hS && hat !== 'world') hQ = clearFloor(hT, hQ, hullOf('hat_p1', 'hat'), safeAxis(cross(rot(hQ, [0, 1, 0]), [0, 1, 0])), .02, 60, 0, 'hat');
  part('hat', hT, hQ, hS);
  // the root lift the body will take (below): the chains' floor guards clear the floor as it stands after it
  let fo = Infinity;
  for (const n of (hat === 'worn' || hat === 'back' ? [...LIFT_PARTS, 'hat'] : LIFT_PARTS)) {
    const v = o[n];
    if (!v || v.s[0] < 1e-4) continue;
    fo = Math.min(fo, minY(hullOf(modelOn(n, p), n), v.t, v.q));
  }
  const fOff = fo < .002 ? .002 - fo : 0;
  {
    const pq = hist(2)?._hatQ || hQ;
    let sq = slerp(hQ, pq, .5), st = hT;
    if (hat === 'world') { sq = mul(hQ, q([90, 0, 0])); st = add(hT, rot(hQ, [0, .015, 0])); }   // lying over the brim
    else {
      const down = rot(sq, [0, -1, 0]);
      sq = mul(slerp(ID, fromTo(down, [0, -1, 0]), .45 * gfade(down)), sq);
      if (hS) sq = clearFloor(hT, sq, hullOf('hat_strings', 'hat_strings'), safeAxis(rot(sq, [1, 0, 0])), .02 - fOff, 120, 0, 'strings');
    }
    part('hat_strings', st, sq, hS);
    Object.defineProperty(o, '_hatQ', {value: hQ, enumerable: false});
  }

  // ---- hair: the ponytail (two segments, lags 3 t, falls with gravity, off the floor) and the side locks ----
  {
    const root = add(Nb, rot(Hq, SK.hairRoot));
    const back = [unit(rot(Cq, [0, -1, .06])), unit(rot(Cq, [0, -1, .02]))];
    const g = p.hairF || 0, lagP = hist(3)?._hairRoot, hf = .05 - fOff;
    let drag = lagP ? sub(lagP, root) : [0, 0, 0];
    if (len(drag) > .3) drag = times(drag, .3 / len(drag));
    let t = root;
    for (let i = 0; i < 2; i++) {
      const L = SK.hairSeg[i];
      let d = unit(lerp(back[i], [0, -1, 0], Math.min(1, g * (.75 + .2 * i))));
      d = unit(add(d, times(drag, 1.3 + 1.0 * i)));
      if (p.hairS) d = unit(add(d, times(rot(Hq, [0, .25, -1]), p.hairS * (1 - .3 * i))));
      if (t[1] + d[1] * L < hf) { const hz = Math.hypot(d[0], d[2]) || 1e-6, sy = -Math.max(0, Math.min(1, (t[1] - hf) / L)), cy = Math.sqrt(Math.max(0, 1 - sy * sy)); d = [d[0] / hz * cy, sy, d[2] / hz * cy]; }
      d = rateLimit(d, prev['hd' + i], prev.Hq ? mul(Hq, conj(prev.Hq)) : null, 30);
      if (t[1] + d[1] * L < hf) { const hz = Math.hypot(d[0], d[2]) || 1e-6, sy = -Math.max(0, Math.min(1, (t[1] - hf) / L)), cy = Math.sqrt(Math.max(0, 1 - sy * sy)); d = [d[0] / hz * cy, sy, d[2] / hz * cy]; }
      keep['hd' + i] = d;
      const F = steadyPerp(rot(Cq, [0, 0, -1]), d, prev['hair' + i], rot(Cq, [0, 0, -1]));
      keep['hair' + i] = F;
      // S2c: the hair is a slab of the skin's back hair, 0.42 wide: lift it about its root, then roll it flat about its own
      // line, until its hull clears the floor (as the post-lift floor stands); the next segment hangs from this one's end
      const hn = 'hair_tail_' + (i + 1), hp = hullOf(hn, hn);
      let hq = clearFloor(t, aimQ(d, F), hp, safeAxis(cross(d, [0, 1, 0])), .012 - fOff, 90, 0, 'hairP' + i);
      const hd = rot(hq, [0, -1, 0]);
      hq = clearFloor(t, hq, hp, hd, .012 - fOff, 60, 0, 'hairR' + i);
      part(hn, t, hq);
      t = add(t, times(rot(hq, [0, -1, 0]), L));
    }
    Object.defineProperty(o, '_hairRoot', {value: root, enumerable: false});
    keep.Hq = Hq;
    for (const [s, k] of [[-1, 'r'], [1, 'l']]) {
      const lr = add(Nb, rot(Hq, [SK.lockRoot[0] * s, SK.lockRoot[1], SK.lockRoot[2]]));
      let lq = mul(Hq, q([0, 0, 0]));
      const dn = rot(lq, [0, -1, 0]);
      lq = mul(slerp(ID, fromTo(dn, [0, -1, 0]), .5 * gfade(dn)), lq);
      part('lock_' + k, lr, lq);
    }
  }

  // ---- sash tails (from the knot at her left hip; hang with gravity, lag 3 t) ----
  {
    const kt = add(R, rot(Pq, SK.sashKnot));
    const lagK = hist(3)?._sashKnot;
    // down, along the pelvis, and out over the skirt's flare (the knot sits just outside the skirt's top ring)
    const outw = rot(Pq, unit([SK.sashKnot[0], 0, SK.sashKnot[2]]));
    let dir = unit(add(add([0, -1, 0], times(rot(Pq, [0, -1, 0]), .35)), times(outw, .34 * (p.skF ?? 1))));
    if (lagK) dir = unit(add(dir, times(sub(lagK, kt), 2.2)));
    dir = rateLimit(dir, prev.sashD, prev.Pq ? mul(Pq, conj(prev.Pq)) : null, 45);
    keep.sashD = dir; keep.Pq = Pq;
    const F = steadyPerp(rot(Pq, [0, 0, -1]), dir, prev.sash, rot(Pq, [0, 0, -1]));
    keep.sash = F;
    let sq = aimQ(dir, F);
    sq = clearFloor(kt, sq, hullOf('sash_p1', 'sash_tails'), safeAxis(cross(dir, [0, 1, 0])), .03 - fOff, 120, 0, 'sash');
    part('sash_tails', kt, sq);
    Object.defineProperty(o, '_sashKnot', {value: kt, enumerable: false});
  }

  // ---- skirt panels (follow their thigh at 0.6 x the swing, 2 t lag; flare; clear the legs and the floor) ----
  {
    // the thighs' directions in the pelvis frame (so the 2-tick lag follows the swing, not the body's own turn)
    const Pinv = [-Pq[0], -Pq[1], -Pq[2], Pq[3]];
    const lag = hist(2)?._legDirs, legDir = k => rot(Pinv, unit(sub(legs[k].E, legs[k].H)));
    const dirsNow = {l: legDir('l'), r: legDir('r')};
    const dirs = lag || dirsNow;
    PANELS.forEach(([n, az, side, dr], i) => {
      const a = az * D, rIn = SKIRT.R0 + dr - (i < 2 ? (p.skIF || 0) : (p.skIB || 0));
      const piv = add(R, rot(Pq, [rIn * Math.sin(a), SK.skirtTop, -rIn * Math.cos(a)]));
      // the thigh's swing in the pelvis frame: forward (pitch) and sideways (roll) components
      const dl = dirs[side], fwdSw = Math.atan2(-dl[2], -dl[1]) / D, sideSw = Math.atan2(dl[0], -dl[1]) / D;
      const outward = .6 * (fwdSw * Math.cos(a) + sideSw * Math.sin(a));
      let pitch = FLARE * (p.skF ?? 1) + Math.max(-14, outward) - 24 * (p.skW || 0) * Math.cos(a);
      let pq = mul(Pq, mul(q([0, -az, 0]), q([pitch, 0, 0])));
      // gravity: the panel falls toward hanging straight down
      const g = p.skG || 0;
      if (g > 0) { const dn = rot(pq, [0, -1, 0]); pq = mul(slerp(ID, fromTo(dn, unit(add([0, -1, 0], times(rot(pq, [0, 0, -1]), .3)))), g * gfade(dn)), pq); }
      // clear the legs: knee / shin points inside the panel's sector must stay behind it (0.07 b inside)
      const nrm = () => rot(pq, [0, 0, -1]);
      const ptsIn = [];
      for (const k of ['l', 'r']) {
        const L = legs[k];
        for (const P of [L.E, lerp(L.H, L.E, .6), lerp(L.E, L.W, .4)]) {
          const rel = rot(Pinv, sub(P, R)), paz = Math.atan2(rel[0], -rel[2]) / D;
          let dA = Math.abs(((paz - az) % 360 + 540) % 360 - 180);
          if (dA < 50 && rel[1] < SK.skirtTop) ptsIn.push(P);
        }
      }
      const axis = () => rot(pq, [1, 0, 0]);
      for (let it = 0; it < 12; it++) {
        const worst = Math.max(-1, ...ptsIn.map(P => dot(sub(P, piv), nrm()) + .085));
        if (worst <= 0) break;
        pq = mul(qa(axis(), 6), pq);
      }
      pq = clearFloor(piv, pq, hullOf(n, n), axis(), .02 - fOff, 110, 0, n);
      part(n, piv, pq);
    });
    Object.defineProperty(o, '_legDirs', {value: dirsNow, enumerable: false});
  }

  // ---- intro props: cup (right hand) / bottle (left hand) / on the rock ----
  {
    const cup = p.cup || 'none', bot = p.bottle || 'none';
    const cupQ = mul(Ryaw, q([p.cupT || 0, 0, 0]));
    if (cup === 'hand') part('cup', add(gripR, [0, -.02, 0]), cupQ);
    else if (cup === 'rock') part('cup', [...(p.cupP || [.3, .45, -.2])], Ryaw);
    else part('cup', gripR, cupQ, 0);
    const fl = o.forearm_l.q;
    const botQ = mul(fl, q([p.botT || 0, 0, 0]));
    if (bot === 'hand') part('bottle', add(gripL, rot(fl, [0, -.2, 0])), botQ);
    else if (bot === 'rock') part('bottle', [...(p.botP || [-.3, .45, -.2])], Ryaw);
    else part('bottle', gripL, botQ, 0);
  }

  // ---- root lift: no body point below the floor ----
  let low = Infinity;
  for (const n of (hat === 'worn' || hat === 'back' ? [...LIFT_PARTS, 'hat'] : LIFT_PARTS)) {
    const v = o[n];
    if (!v || v.s[0] < 1e-4) continue;
    const m = minY(hullOf(modelOn(n, p), n), v.t, v.q);
    if (m < low) low = m;
  }
  const lift = low < .002 ? .002 - low : 0;
  if (lift) for (const [n, v] of Object.entries(o)) if (!(n === 'hat' && hat === 'world') && !((n === 'cup' && (p.cup === 'rock')) || (n === 'bottle' && p.bottle === 'rock'))) v.t = add(v.t, [0, lift, 0]);
  // visibility about the body centre
  if ((p.vis ?? 1) !== 1) {
    const c = add(R, [0, .3 + lift, 0]);
    for (const v of Object.values(o)) { v.t = add(c, times(sub(v.t, c), p.vis)); v.s = times(v.s, p.vis); }
  }
  // the parts the skin already shows (HIDDEN: the side locks, the skirt panels) rest at scale 0 in one fixed transform, so a
  // clip keys them once at its tick 0
  for (const n of HIDDEN) o[n] = {t: [0, HIP_Y, 0], q: [0, 0, 0, 1], s: [0, 0, 0]};
  // anchors (rig frame, after the lift): the grips, the blade tip / middle (the left hand while the sword is hidden), the
  // scabbard's mouth, the crown top, the head centre, the chest
  const swOn = o.sword.s[0] > 1e-4;
  const gW = o.sword.t, ax = rot(o.sword.q, [0, 1, 0]);
  const anchors = {
    hand_l: add(gripL, [0, lift, 0]), hand_r: add(gripR, [0, lift, 0]),
    blade_tip: swOn ? add(gW, times(ax, SWORD.tip)) : add(gripL, [0, lift, 0]),
    blade_mid: swOn ? add(gW, times(ax, (SWORD.bladeLo + SWORD.tip) / 2)) : add(gripL, [0, lift, 0]),
    scabbard_mouth: o.scabbard.t, hat_crown: add(o.hat.t, rot(o.hat.q, [0, HAT.crownH + .02, 0])),
    head: add(o.head.t, rot(o.head.q, [0, .3, -.02])), chest: add(o.torso.t, rot(o.torso.q, [0, .3, -.06])),
  };
  Object.defineProperty(o, '_anchors', {value: anchors, enumerable: false});
  keep.gs = {...GUARD.prefer, ...GUARD.sense};
  Object.defineProperty(o, '_prev', {value: keep, enumerable: false});
  Object.defineProperty(o, '_lift', {value: lift, enumerable: false});
  Object.defineProperty(o, '_guard', {value: GUARD.used, enumerable: false});
  return o;
}
// the hand's grip point of an arm solution (the IK target end = 0.08 below the wrist along the forearm)
function sol2grip(sol) { return sol.W; }
// parts whose hull lifts the whole figure off the floor (the chains, the panels and the sword have their own guards)
const LIFT_PARTS = ['pelvis', 'torso', 'head', 'face', 'arm_l', 'forearm_l', 'arm_r', 'forearm_r', 'thigh_l', 'shin_l', 'thigh_r', 'shin_r', 'lock_l', 'lock_r'];
// turn the sword about its grip (smallest turn, iterated) until its whole hull is 0.10 b above the floor
function groundSword(G, Q, fwd = [0, 0, -1]) {
  const pts = hullOf('sword', 'sword');
  let out = Q;
  for (let it = 0; it < 8; it++) {
    let lo = null, ly = Infinity;
    for (const P of pts) { const y = G[1] + rot(out, P)[1]; if (y < ly) { ly = y; lo = P; } }
    if (ly >= .10 - 1e-4) break;
    const L = len(lo), d = times(rot(out, lo), 1 / L), minYv = (.10 + 2e-3 - G[1]) / L;
    let h = [d[0], 0, d[2]];
    if (len(h) < .25) h = add(h, times(fwd, .25 - len(h)));
    const hl = len(h) || 1e-6, sy = Math.min(1, minYv), cy = Math.sqrt(Math.max(0, 1 - sy * sy));
    const d2 = [h[0] / hl * cy, sy, h[2] / hl * cy], ax = cross(d, d2), sa = len(ax);
    if (sa < 1e-9) break;
    const ang = Math.atan2(sa, dot(d, d2)), u = times(ax, 1 / sa), sn = Math.sin(ang / 2);
    out = mul([u[0] * sn, u[1] * sn, u[2] * sn, Math.cos(ang / 2)], out);
  }
  return out;
}
export function toDisplay(n, v) {
  const k = PART_SCALE[n];
  return {t: toDisplayT(v.t), q: toDisplayQ(v.q), s: v.s.map(x => x * k)};
}
export const fromDisplay = (n, v) => ({t: [v.t[0], v.t[1], -v.t[2]], q: [-v.q[0], -v.q[1], v.q[2], v.q[3]], s: v.s.map(x => x / PART_SCALE[n])});
// world points of a part's model at a solved transform (rig frame)
export function worldPoints(model, n, v) {
  if (Math.max(...v.s.map(Math.abs)) < 1e-4) return [];
  const M = qm(v.q);
  return hullOf(model, n).map(P => { const x = P[0] * v.s[0], y = P[1] * v.s[1], z = P[2] * v.s[2];
    return [v.t[0] + M[0][0] * x + M[0][1] * y + M[0][2] * z, v.t[1] + M[1][0] * x + M[1][1] * y + M[1][2] * z, v.t[2] + M[2][0] * x + M[2][1] * y + M[2][2] * z]; });
}
export {PART_NAMES};
void STRINGS; void basisQ;
