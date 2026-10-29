// Skeleton and pose solver of the 타키 (Tachy) rig (S:tk/PLAN.md §2.1-2.3). solve(p, form, hist) turns one pose (the
// channels below, sampled from tachy_clips.mjs) into the rig-frame transform {t, q, s} of each of the 40 parts.
//
// Frames. Rig frame: +X her left, +Y up, -Z forward, blocks; the origin is the anchor (the boss body) on the floor.
// Quaternions [x, y, z, w]; eulers [pitch, yaw, roll] in degrees as mboss_rig_math.q (pitch + leans back / raises a toe,
// yaw + turns to her right... see dirBE below for bearings: + = her right).
//
// Pose channels
//   pos [x,y,z]        root offset (the pelvis centre moves by it; 1.10 b above the floor at rest)
//   rot [p,y,r]        pelvis: yaw about up (the facing of the whole figure), then pitch / roll of the hips
//   tor [p,y,r]        spine bend, half in the abdomen, half in the chest
//   head [p,y,r]       neck (35 %) + head (65 %) relative to the chest
//   helm               helmet hinge (0 closed; -100 pushed back as a hood, the face bare: intro E0-E7)
//   fL, fR [x,y,z]     ankle targets in the yaw frame from the floor point under the pelvis (y 0.085 = planted)
//   fpL, fpR / fyL, fyR   foot pitch (+ toes up) / yaw;  kL, kR [x,y,z]  knee pole (yaw frame), default forward
//   hold 0|1           the sword in the right hand (else the right arm is free: aR)
//   gB gE gD           the grip: bearing / elevation (deg) and distance (b) from the swing centre (0.45 b above the
//                      pelvis centre, yaw frame). Interpolated as numbers, so a cut sweeps on an arc, never a poke
//   gF gL              grip follow: 0 = the sphere above; 1 = the grip on the lever gL (b) from the right shoulder (or the
//                      chest centre with lh) along the blade, so a sweep turns about the shoulder
//   cB cR th ed tw     the blade: tip angle th in the cutting plane through bearing cB rolled by cR (0 vertical: th 0
//                      forward, 90 up; 90 horizontal: th + toward her left), the edge leading toward +th (ed 1) or -th
//                      (ed -1), twisted by tw about the blade (yaw frame)
//   lh 0..1            the left hand on the hilt (two-handed) .. free (aL)
//   aL, aR [p,r,k]     free hand targets about the shoulder, chest frame: pitch (+ forward / up the front), roll (+ out
//                      to her side), reach 0..1;  plL, plR [x,y,z] + plwL, plwR: hand plant targets (yaw frame) blended in
//   pL, pR [x,y,z]     elbow poles (chest frame; side-signed x: + = outward)
//   hwL, hwR [p,y,r]   free wrist eulers
//   wS wF wW wFl       wings / cape: spread 0..1, flare 0..1, wrap 0..1, flap amplitude (deg); the mapping per form below
//   td [p,y,r], tdS   tendrils: base euler (side-signed roll) and scale (shown in the abyss form only)
//   hairF 0..1         hair: falls with gravity (head bowed) instead of lying on the back; hairS sweep (hand pushes it back)
//   vis 0..1           everything scaled about the body centre (blink, the high hover)
//   drawn 0|1          the sword shown in the hand (0 = sheathed: hidden; the scabbard model switches separately)
//   ph                 the loop phase 0..1 (cape flutter, tendril writhe; set by the sampler)
import {add, sub, times, len, unit, mul, q, rot, aimQ, ik, basisQ, cross, dot, perp, slerp, armFront, steadyPerp, toDisplayT, toDisplayQ, lerp} from './mboss_rig_math.mjs';
import {PART_NAMES, PART_SCALE, SWORD, modelPoints} from './tachy_geometry.mjs';

export const HIP_Y = 1.10;
export const SK = {
  waist: [0, .10, 0], chestB: [0, .24, 0], neckB: [0, .345, -.005], headB: [0, .085, 0],
  shoulder: [.235, .27, .01], hipJ: [.105, -.07, 0], thigh: .48, shin: .465, ankleY: .085,
  armU: .32, foreL: .29, foreR: .31, handGrip: .06, handGripR: .072,
  pack: [0, .22, .145], wingRoot: [.12, .14, .08], tendrilRoot: [.09, .06, .07],
  helmHinge: [0, .21, .1], hairRoot: [0, .18, .1], hairSeg: .25,
  swing: [0, .45, 0],
  // the scabbard across the lower back over the cape (chest frame): the mouth (hilt) at her right hip, the body rising
  // gently to the left past her left hip (v2 13.2-13.4: the blade comes out horizontally from behind the hips, to the right)
  // (I1: 0.04 b closer to her back and level with it, so the holster stays under the cape that now hangs clear of her)
  scabMouth: [-.22, -.3, .16], scabDir: [.75, 1, 0],
};
const D = Math.PI / 180;
export const dirBE = (b, e = 0) => { const B = b * D, E = e * D; return [-Math.sin(B) * Math.cos(E), Math.sin(E), -Math.cos(B) * Math.cos(E)]; };
export const mirrorE = e => [e[0], -e[1], -e[2]];
const ID = [0, 0, 0, 1];
const conj = Q => [-Q[0], -Q[1], -Q[2], Q[3]];
// shortest rotation taking unit a to unit b
export function fromTo(a, b) {
  const c = cross(a, b), d = dot(a, b);
  if (d < -.9999) { const ax = unit(len(cross(a, [1, 0, 0])) > .1 ? cross(a, [1, 0, 0]) : cross(a, [0, 0, 1])); return [ax[0], ax[1], ax[2], 0]; }
  const w = 1 + d, m = Math.hypot(c[0], c[1], c[2], w);
  return [c[0] / m, c[1] / m, c[2] / m, w / m];
}
export function bladeQ(tip, edge) {
  const Y = unit(tip); let Z = perp(times(edge, -1), Y);
  if (len(Z) < 1e-6) Z = perp([0, 0, 1], Y);
  Z = unit(Z);
  return basisQ(cross(Y, Z), Y, Z);
}
const qa = (axis, deg) => { const s = Math.sin(deg * D / 2); return [axis[0] * s, axis[1] * s, axis[2] * s, Math.cos(deg * D / 2)]; };
const lerpN = (a, b, u) => a + (b - a) * u;
const lerpE = (a, b, u) => a.map((x, i) => x + (b[i] - x) * u);

// ---- hulls (blocks, part space, display scale applied) for the floor checks and guards ------------------------------------
let HULLS = null, MODELS = null;
// the support points of a point set along 98 directions (a cube-sphere grid): the extreme points under any rotation,
// enough for min-y / culling checks of a rotated model (exact for the axis-aligned extremes)
const DIRS = (() => { const D = []; for (let i = -3; i <= 3; i++) for (let j = -3; j <= 3; j++) for (const [a, b, c] of [[1, i / 3, j / 3], [-1, i / 3, j / 3]]) { D.push([a, b, c], [b, a, c], [b, c, a]); } return D; })();
function support(pts) {
  if (pts.length <= 24) return pts;
  const keep = new Set();
  for (const d of DIRS) { let best = -Infinity, bi = 0; for (let i = 0; i < pts.length; i++) { const v = pts[i][0] * d[0] + pts[i][1] * d[1] + pts[i][2] * d[2]; if (v > best) { best = v; bi = i; } } keep.add(bi); }
  return [...keep].sort((x, y) => x - y).map(i => pts[i]);
}
export function setModels(models) {
  MODELS = models; HULLS = {};
  for (const [n, els] of Object.entries(models)) {
    const seen = new Set(), pts = [];
    for (const P of modelPoints(els)) { const k = P.map(v => v.toFixed(3)).join(); if (!seen.has(k)) { seen.add(k); pts.push(P); } }
    HULLS[n] = support(pts);
  }
}
const HCACHE = new Map();
// the hull of an item model shown on part n (model units -> blocks at the part's scale)
export const hullOf = (model, n) => {
  const key = model + '|' + n;
  if (!HCACHE.has(key)) { const k = PART_SCALE[n] / 16; HCACHE.set(key, (HULLS[model] || []).map(P => [P[0] * k, P[1] * k, P[2] * k])); }
  return HCACHE.get(key);
};
// rotation matrix rows of a quaternion
export function qm(Q) {
  const [x, y, z, w] = Q;
  return [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)], [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]];
}
const minY = (pts, t, Q) => { const r = qm(Q)[1]; let m = Infinity; for (const P of pts) { const y = t[1] + r[0] * P[0] + r[1] * P[1] + r[2] * P[2]; if (y < m) m = y; } return m; };
// turn a segment (pivot t, rotation Q, hull pts) about `axis` by the smallest angle (step search, either sense if both
// allowed) so its hull clears y >= clear; returns the new Q
// guard angle bookkeeping of one solve: GUARD.min = {name: minimum angle} (the smoothed plan of a second pass),
// GUARD.used = {name: angle applied}
let GUARD = {min: {}, used: {}};
function clearFloor(t, Q, pts, axis, clear, maxDeg = 100, sense = 1, name = null) {
  const a0 = name ? GUARD.min[name] || 0 : 0;
  const at = a => (a ? mul(qa(axis, sense * a), Q) : Q);
  let a = a0;
  if (minY(pts, t, at(a)) < clear) {
    let lo = a, hi = null;
    for (let x = a + 4; x <= maxDeg; x += 4) if (minY(pts, t, at(x)) >= clear) { hi = x; break; } else lo = x;
    if (hi === null) a = maxDeg;
    else { for (let k = 0; k < 7; k++) { const m = (lo + hi) / 2; if (minY(pts, t, at(m)) >= clear) hi = m; else lo = m; } a = hi; }
  }
  if (name) GUARD.used[name] = a;
  return at(a);
}

// ---- wing / cape mapping per form ---------------------------------------------------------------------------------------------
// returns [e1, e2, e3] eulers (relative: seg1 to the chest frame, seg2 to seg1, seg3 to seg2) for side s (+1 left)
export const WING_BASE = .95;
// wrap target frames (chest frame) of segment i, side s: the segment's direction d (model -Y) and the model's -X (the
// feathers / the panel's inner edge) pointing down for the wings, forward for the cape panels
const WRAP_D = {winged: [[.7, -.3, -.65], [-.75, -.18, -.62], [-.95, -.12, .28]], cape: [[.3, -.9, -.3], [-.05, -1, -.22], [-.12, -1, -.1]]};
function wrapFrame(form, i, s) {
  const f = form === 'cape' ? 'cape' : 'winged', d0 = WRAP_D[f][i], d = unit([d0[0] * s, d0[1], d0[2]]);
  const Y = times(d, -1);
  // model +X: up for the wings (feathers hang down), back for the cape (its outer edge wraps forward); the right side's
  // models are mirror images, so their +X is the other way
  let X = f === 'cape' ? [0, 0, -s] : [0, s, 0];
  X = unit(sub(X, times(Y, dot(X, Y))));
  return basisQ(X, Y, cross(X, Y));
}
export function wingEulers(p, form, s, t) {
  const {wS = 0, wF = 0, wW = 0, wFl = 0} = p, ph = (p.ph || 0) * 2 * Math.PI;
  if (form === 'cape') {
    const A = 2.5 + 7 * wF, fl = i => A * Math.sin(ph - i * .9 + (s > 0 ? 0 : .6));
    // wF: the cape streams back and out in a gust or a dash (v2 7.5-9.5: flung out behind her like a flag)
    // I1: a positive pitch turns a segment's lower end FORWARD (toward her legs); the cape used to hang 7-19 deg forward
    // through her hips and thighs. Now the top panel trails 8 deg BACK from the shoulder blades (12 deg with the stance's
    // torso lean; clear of the hips) and the lower panels fall back to the vertical; a gust (wF) streams all three back.
    const e1 = [-(8 + 56 * wF) + fl(0), s * 8 * wS, s * (5 + 22 * wS + 16 * wF)];
    const e2 = [8 - 32 * wF + fl(1), 0, -s * 4 * wS];
    const e3 = [4 - 18 * wF + fl(2), 0, -s * 3 * wS];
    return [e1, e2, e3];
  }
  // winged: the wings rest 95 % spread behind her (P2 / P3 footage: v7 0.4, v4 38.0); wS is added (-0.95 = folded)
  const S = Math.max(0, Math.min(1, WING_BASE + wS)), flap = wFl * Math.sin(ph);
  // low poses (crouch, kneel, prone) carry the wings higher so their feathers stay off the floor
  const low = Math.max(0, Math.min(1, (-(p.pos ? p.pos[1] : 0) - .12) / .4));
  let e1 = [lerpN(38, 18, S) + 10 * wF + 12 * low, s * lerpN(4, -14, S), s * (lerpN(20, 108, S) + 14 * wF + flap + 34 * low)];
  let e2 = [lerpN(4, 6, S), 0, s * (lerpN(-160, -14, S) + 8 * wF + .5 * flap + 16 * low)];
  let e3 = [lerpN(2, 4, S), 0, s * (lerpN(150, -12, S) + 6 * wF + 10 * low)];
  return [e1, e2, e3];
}

// ---- solve ---------------------------------------------------------------------------------------------------------------
// p: full pose; form: 'cape' | 'winged' | 'abyss'; hist(k): the solved output k ticks before (or null). Returns
// {part: {t, q, s}} (rig frame) plus non-enumerable extras (_grip, _tip, _prev).
export function solve(p, form = 'cape', hist = () => null, guardMin = {}) {
  const o = {};
  GUARD = {min: guardMin, used: {}};
  const part = (n, t, Q, s = 1) => { o[n] = {t, q: Q, s: Array.isArray(s) ? s : [s, s, s]}; };
  const prev = hist(1)?._prev || {};
  const Ryaw = q([0, p.rot[1], 0]);
  const Pq = mul(Ryaw, q([p.rot[0], 0, p.rot[2]]));
  const R = [p.pos[0], HIP_Y + p.pos[1], p.pos[2]];
  const floorP = [p.pos[0], 0, p.pos[2]];
  const half = mul(q(times(p.tor, .5)), ID);
  const Aq = mul(Pq, half), Cq = mul(Aq, half);
  const W = add(R, rot(Pq, SK.waist)), Cb = add(W, rot(Aq, SK.chestB));
  part('pelvis', R, Pq); part('tassets', R, Pq);
  part('abdomen', W, Aq);
  part('chest', Cb, Cq); part('chest_glow', Cb, Cq);
  const Nb = add(Cb, rot(Cq, SK.neckB));
  const Nq = mul(Cq, q(times(p.head, .35))), Hq = mul(Nq, q(times(p.head, .65)));
  part('neck', Nb, Nq); part('collar', Nb, Cq);
  const Hb = add(Nb, rot(Nq, SK.headB));
  part('head', Hb, Hq); part('hair_top', Hb, Hq);
  // helmet: turned about the hinge behind the crown
  const hq = mul(Hq, q([p.helm || 0, 0, 0])), hinge = add(Hb, rot(Hq, SK.helmHinge));
  const ht = add(hinge, rot(hq, times(SK.helmHinge, -1)));
  part('helmet', ht, hq); part('visor_glow', ht, hq);
  // spine pack, wings / cape, tendrils, scabbard
  const pack = add(Cb, rot(Cq, SK.pack));
  part('spine_pack', pack, Cq);
  for (const [s, k] of [[1, 'l'], [-1, 'r']]) {
    const root = add(pack, rot(Cq, [SK.wingRoot[0] * s, SK.wingRoot[1], SK.wingRoot[2]]));
    const E = wingEulers(p, form, s, 0);
    let Q = Cq, t = root;
    const L = form === 'cape' ? [.53, .53, .5] : [.95, .95, .8];
    // the wrap (wW): each segment slerps toward a target frame round her front (a cloak of feathers / the cape's panels
    // turned round her sides), chest frame; blended by smoothstep(wW)
    const ww = Math.max(0, Math.min(1, p.wW || 0)), wk = ww * ww * (3 - 2 * ww);
    // I1: the cape follows her back while she stands (the eulers above); as her torso tips toward the horizontal (prone,
    // on hands and knees: the intro) it falls toward the floor instead (the floor guard below then lays it out behind
    // her as a train, v2 1.5-4.0) rather than sticking up off her back
    const upr = Math.max(0, dot(rot(Cq, [0, -1, 0]), [0, -1, 0])), grav = form === 'cape' ? .9 * Math.pow(1 - upr, 1.5) : 0;
    for (let i = 0; i < 3; i++) {
      Q = mul(Q, q(E[i]));
      if (grav > 1e-3) Q = slerp(Q, mul(fromTo(rot(Q, [0, -1, 0]), [0, -1, 0]), Q), grav);
      if (wk > 0) Q = slerp(Q, mul(Cq, wrapFrame(form, i, s)), wk);
      const n = `wing_${k}${i + 1}`, model = form === 'cape' ? `cape_${k}${i + 1}` : form === 'abyss' ? `wing_${k}${i + 1}_a` : `wing_${k}${i + 1}`;
      // floor guard: the cape trails back (pitch about its own X), a wing segment turns up about the body's forward axis
      // floor guard: the cape trails back (pitch about its own X); a wing segment lifts toward up about the axis across it
      if (form === 'cape') Q = clearFloor(t, Q, hullOf(model, n), rot(Q, [1, 0, 0]), .03, 110, -1, n);
      else { const d = rot(Q, [0, -1, 0]); let ax = cross(d, [0, 1, 0]); if (len(ax) < .2) ax = add(ax, times(rot(Cq, [0, 0, -1]), .2 * s)); Q = clearFloor(t, Q, hullOf(model, n), unit(ax), .03, 170, 1, n); }
      part(n, t, Q);
      t = add(t, rot(Q, [0, -L[i], 0]));
    }
    const ph = (p.ph || 0) * 2 * Math.PI;
    const td = p.td || [30, 0, 35], tdq = mul(Cq, q([td[0] + 8 * Math.sin(ph * 2 + s), s * td[1], s * (td[2] + 10 * Math.sin(ph * 3 + s * 1.3))]));
    const troot = add(pack, rot(Cq, [SK.tendrilRoot[0] * s, SK.tendrilRoot[1], SK.tendrilRoot[2]]));
    const tS = form === 'abyss' ? (p.tdS ?? 1) : 0;
    part(`tendril_${k}`, troot, tS > 1e-3 ? clearFloor(troot, tdq, hullOf('tendril', 'tendril_' + k), rot(Cq, [1, 0, 0]), .03, 120, -1, 'tendril_' + k) : tdq, tS);
  }
  const scab = add(Cb, rot(Cq, SK.scabMouth)), scabQ = mul(Cq, bladeQ(SK.scabDir, [0, 0, 1]));
  part('scabbard', scab, scabQ);
  // ---- legs (IK; the hips do not twist with the torso) ----
  const footM = {};
  // a limb segment hanging along dir with its front toward `front`, the front kept continuous across ticks
  const segQ = (key, dir, front) => { const F = steadyPerp(front, unit(dir), prev['f_' + key], [0, 0, -1]); footM['f_' + key] = F; return aimQ(dir, F); };
  for (const [s, k, F, fp, fy, kp] of [[1, 'l', p.fL, p.fpL, p.fyL, p.kL], [-1, 'r', p.fR, p.fpR, p.fyR, p.kR]]) {
    const H = add(R, rot(Pq, [SK.hipJ[0] * s, SK.hipJ[1], SK.hipJ[2]]));
    const A = add(floorP, rot(Ryaw, F));
    const pole = rot(Ryaw, kp || [s * .15, 0, -1]);
    const sol = ik(H, A, SK.thigh, SK.shin, pole, prev['leg' + k]);
    const fwd = rot(Ryaw, [0, 0, -1]);
    const kv = times(sol.v, -1);
    part('thigh_' + k, H, segQ('th' + k, sub(sol.E, H), armFront(sub(sol.E, H), kv, fwd)));
    part('shin_' + k, sol.E, segQ('sh' + k, sub(sol.W, sol.E), armFront(sub(sol.W, sol.E), kv, fwd)));
    part('foot_' + k, sol.W, mul(Ryaw, q([fp || 0, -s * (fy || 0), 0])));   // fy + = toes out
    footM['leg' + k] = sol.v;
  }
  // ---- arms ----
  const Cw = add(R, rot(Ryaw, SK.swing));
  const shoulderOf = s => add(Cb, rot(Cq, [SK.shoulder[0] * s, SK.shoulder[1], SK.shoulder[2]]));
  const SL = shoulderOf(1), SR = shoulderOf(-1);
  const chestFwd = rot(Cq, [0, 0, -1]);
  // a free arm: a = [pitch (+ forward / up the front), roll (+ out to her side), reach 0..1] about the shoulder, chest frame
  const armDir = (a, side) => { const P = a[0] * D, B = a[1] * D * side, y = -Math.cos(P), z = -Math.sin(P); return [-y * Math.sin(B), y * Math.cos(B), z]; };
  const freeTarget0 = (S, a, side, reach) => add(S, times(rot(Cq, armDir(a, side)), a[2] * reach));
  // a free hand may be planted (hands on the floor, a hand on the head): plL / plR in the yaw frame from the floor point
  // under the pelvis, blended in by plwL / plwR
  const freeTarget = (S, a, side, reach) => { const w = side > 0 ? (p.plwL || 0) : (p.plwR || 0), P = side > 0 ? p.plL : p.plR;
    const F = freeTarget0(S, a, side, reach); return w > 0 && P ? lerp(F, add(floorP, rot(Ryaw, P)), w) : F; };
  // the sword: grip point, frame; the right wrist sits beside the grip toward the shoulder
  // the blade: its tip direction is the angle th inside a cutting plane (the plane through the bearing cB and up,
  // rolled by cR about that bearing: 0 vertical, 90 horizontal with th + toward her left, ±45 diagonals); the edge leads
  // along the arc (ed +1: toward increasing th, -1: decreasing), turned by tw about the blade
  const u = rot(Ryaw, dirBE(p.cB, 0)), v = rot(qa(u, p.cR), rot(Ryaw, [0, 1, 0]));
  const c = Math.cos(p.th * D), sn = Math.sin(p.th * D);
  const T = add(times(u, c), times(v, sn));
  // ed between keys turns the edge smoothly about the blade (ed 1 -> -1 = a half turn), never a one-tick flip
  let Ed = add(times(u, -sn), times(v, c));
  const twist = 90 * (1 - Math.max(-1, Math.min(1, p.ed))) + (p.tw || 0);
  if (Math.abs(twist) > 1e-6) Ed = rot(qa(T, twist), Ed);
  let SQ = bladeQ(T, Ed);
  // the grip: on a sphere about the swing centre (gB, gE, gD), blended (gF) toward the lever point gL along the blade
  // from the right shoulder (one hand) / the chest centre (two hands): a sweep then turns about the shoulder
  const Gs = add(Cw, times(rot(Ryaw, dirBE(p.gB, p.gE)), p.gD));
  const Gf = add(lerp(SR, Cw, Math.min(1, p.lh || 0)), times(T, p.gL || .55));
  let G = lerp(Gs, Gf, p.gF || 0);
  const arm = (k, S, target, pole, Lf) => {
    const sol = ik(S, target, SK.armU, Lf, pole, prev['arm' + k]);
    footM['arm' + k] = sol.v;
    return sol;
  };
  const poleOf = (pp, s) => rot(Cq, pp ? [pp[0] * s, pp[1], pp[2]] : [s * .55, -.35, .75]);
  let wristR, handRQ;
  // the wrist sits beside the grip, away from the edge and toward the shoulder; kept continuous across ticks (steadyPerp)
  const wristDir = (S, Gp, sy, prevW) => steadyPerp(add(perp(sub(S, Gp), sy), times(Ed, -.35 * len(sub(S, Gp)))), sy, prevW, rot(Cq, [0, -1, .3]));
  if ((p.hold ?? 1) > .5) {
    const w0 = wristDir(SR, G, rot(SQ, [0, 1, 0]), prev.wR);
    const tgt = add(G, times(w0, SK.handGripR));
    const sol = arm('r', SR, tgt, poleOf(p.pR, -1), SK.foreR);
    wristR = sol.W;
    // the grip follows the hand where the arm falls short
    const sy = rot(SQ, [0, 1, 0]);
    const w = wristDir(SR, sub(wristR, times(w0, SK.handGripR)), sy, w0);
    footM.wR = w;
    G = sub(wristR, times(w, SK.handGripR));
    handRQ = basisQ(cross(w, times(sy, -1)), w, times(sy, -1));
    part('upper_arm_r', SR, segQ('uar', sub(sol.E, SR), armFront(sub(sol.E, SR), sol.v, chestFwd)));
    part('forearm_r', sol.E, segQ('far', sub(wristR, sol.E), armFront(sub(wristR, sol.E), sol.v, chestFwd)));
  } else {
    const sol = arm('r', SR, freeTarget(SR, p.aR, -1, SK.armU + SK.foreR), poleOf(p.pR, -1), SK.foreR);
    wristR = sol.W;
    const fq = segQ('far', sub(wristR, sol.E), armFront(sub(wristR, sol.E), sol.v, chestFwd));
    handRQ = mul(fq, q(mirrorE(p.hwR || [0, 0, 0])));
    part('upper_arm_r', SR, segQ('uar', sub(sol.E, SR), armFront(sub(sol.E, SR), sol.v, chestFwd)));
    part('forearm_r', sol.E, fq);
  }
  part('hand_r', wristR, handRQ);
  // the left hand: on the hilt below the right hand (lh) or free
  {
    const sy = rot(SQ, [0, 1, 0]);
    const G2 = add(G, times(sy, SWORD.twoHand));
    const w2 = wristDir(SL, G2, sy, prev.wL);
    footM.wL = w2;
    const tH = add(G2, times(w2, SK.handGrip));
    const tF = freeTarget(SL, p.aL, 1, SK.armU + SK.foreL);
    const lh = (p.hold ?? 1) > .5 ? (p.lh || 0) : 0;
    const sol = arm('l', SL, lerp(tF, tH, lh), poleOf(p.pL, 1), SK.foreL);
    const fq = segQ('fal', sub(sol.W, sol.E), armFront(sub(sol.W, sol.E), sol.v, chestFwd));
    part('upper_arm_l', SL, segQ('ual', sub(sol.E, SL), armFront(sub(sol.E, SL), sol.v, chestFwd)));
    part('forearm_l', sol.E, fq);
    const wl = w2;
    const gripQ = basisQ(cross(wl, times(sy, -1)), wl, times(sy, -1));
    // free -> on the hilt: the hand turns over the blend (smoothstep of lh), never in one tick
    const k = lh <= 0 ? 0 : lh >= 1 ? 1 : lh * lh * (3 - 2 * lh);
    part('hand_l', sol.W, slerp(mul(fq, q(p.hwL || [0, 0, 0])), gripQ, k));
  }
  // shoulders follow 30 % of their arm's swing
  for (const [k, S, s] of [['l', SL, 1], ['r', SR, -1]]) {
    const dir = unit(sub(o['forearm_' + k].t, S)), down = rot(Cq, [0, -1, 0]);
    part('shoulder_' + k, S, mul(slerp(ID, fromTo(down, dir), .3), Cq));
    void s;
  }
  // the sword (pivot at the grip): turned up about the grip where its hull would reach the floor
  const drawn = p.drawn ?? 1;
  if (drawn > 0) SQ = groundSword(add(G, [0, 0, 0]), SQ, rot(Ryaw, [0, 0, -1]));
  part('sword', G, SQ, drawn); part('sword_edge', G, SQ, drawn);
  // ---- hair (lies on the back, lags the head by 3 t, falls with gravity when hairF) ----
  {
    const root = add(Hb, rot(Hq, SK.hairRoot));
    const back = [unit(rot(Cq, [0, -1, .34])), unit(rot(Cq, [0, -1, .1])), unit(rot(Cq, [0, -1, .02]))];
    const g = p.hairF || 0, lagP = hist(3)?._hairRoot;
    let drag = lagP ? sub(lagP, root) : [0, 0, 0];
    if (len(drag) > .25) drag = times(drag, .25 / len(drag));
    let t = root;
    for (let i = 0; i < 3; i++) {
      let d = unit(lerp(back[i], [0, -1, 0], Math.min(1, g * (.7 + .15 * i))));
      d = unit(add(d, times(drag, 1.2 + .8 * i)));
      if (p.hairS) d = unit(add(d, times(rot(Hq, [0, .3, 1]), p.hairS * (1 - .3 * i))));
      // stay off the floor
      const L = SK.hairSeg + (i === 2 ? .12 : 0), end = add(t, times(d, L));
      // near the floor the lock turns (continuously) toward the face's heading and lies flat instead of dipping
      const w = Math.max(0, Math.min(1, (.2 - end[1]) / .2));
      if (w > 0) { const up = rot(Cq, [0, 1, .3]), hb = unit([up[0], 0, up[2]]); d = unit(add(d, times(hb, .5 * w))); }
      if (t[1] + d[1] * L < .04) { const hz = Math.hypot(d[0], d[2]) || 1e-6, sy = -Math.max(0, Math.min(1, (t[1] - .04) / L)), cy = Math.sqrt(Math.max(0, 1 - sy * sy)); d = [d[0] / hz * cy, sy, d[2] / hz * cy]; }
      // never more than 28 degrees per tick (a lock does not jump)
      const pd = prev['hd' + i];
      if (pd) { const ang = Math.acos(Math.max(-1, Math.min(1, dot(pd, d)))); const mx = 28 * D; if (ang > mx) { const ax = cross(pd, d); d = len(ax) > 1e-6 ? rot(qa(unit(ax), mx / D), pd) : d; } }
      if (t[1] + d[1] * L < .07) { const hz = Math.hypot(d[0], d[2]) || 1e-6, sy = -Math.max(0, Math.min(1, (t[1] - .07) / L)), cy = Math.sqrt(Math.max(0, 1 - sy * sy)); d = [d[0] / hz * cy, sy, d[2] / hz * cy]; }
      footM['hd' + i] = d;
      const front = add(rot(Cq, [0, 0, 1]), rot(Cq, [0, .45, 0]));
      const F = steadyPerp(front, d, prev['hair' + i], rot(Cq, [0, 0, 1]));
      footM['hair' + i] = F;
      part('hair_' + (i + 1), t, aimQ(d, F));
      t = add(t, times(d, SK.hairSeg));
    }
    Object.defineProperty(o, '_hairRoot', {value: root, enumerable: false});
  }
  // ---- root lift: no body point below the floor ----
  let low = Infinity;
  for (const n of LIFT_PARTS) {
    const v = o[n], m = minY(hullOf(modelOn(n, p, form), n), v.t, v.q);
    if (m < low) low = m;
  }
  const lift = low < .002 ? .002 - low : 0;
  if (lift) for (const v of Object.values(o)) v.t = add(v.t, [0, lift, 0]);
  // visibility about the body centre
  if ((p.vis ?? 1) !== 1) {
    const c = add(R, [0, .2 + lift, 0]);
    for (const v of Object.values(o)) { v.t = add(c, times(sub(v.t, c), p.vis)); v.s = times(v.s, p.vis); }
  }
  Object.defineProperty(o, '_grip', {value: add(G, [0, lift, 0]), enumerable: false});
  Object.defineProperty(o, '_tip', {value: add(add(G, [0, lift, 0]), times(rot(SQ, [0, 1, 0]), SWORD.tip * 1)), enumerable: false});
  Object.defineProperty(o, '_prev', {value: footM, enumerable: false});
  Object.defineProperty(o, '_lift', {value: lift, enumerable: false});
  Object.defineProperty(o, '_guard', {value: GUARD.used, enumerable: false});
  return o;
}
// parts whose hull lifts the whole figure off the floor (the chains and the sword have their own guards)
const LIFT_PARTS = ['pelvis', 'abdomen', 'chest', 'neck', 'head', 'hair_top', 'helmet', 'collar', 'shoulder_l', 'upper_arm_l', 'forearm_l', 'hand_l',
  'shoulder_r', 'upper_arm_r', 'forearm_r', 'hand_r', 'spine_pack', 'tassets', 'thigh_l', 'shin_l', 'foot_l', 'thigh_r', 'shin_r', 'foot_r', 'scabbard'];
// the item model a part shows (for its hull) in a pose / form
export function modelOn(n, p, form) {
  if (n === 'hand_l') return (p.hold ?? 1) > .5 && (p.lh || 0) > .5 ? 'hand_l_grip' : (p.hL === 'grip' || p.hL === 'fist' ? 'hand_l_grip' : 'hand_l_open');
  if (n === 'hand_r') return (p.hold ?? 1) > .5 ? 'hand_r_grip' : p.hR === 'fist' ? 'hand_r_fist' : p.hR === 'grip' ? 'hand_r_grip' : 'hand_r_open';
  if (n === 'scabbard') return (p.scab || 'empty') === 'full' ? 'scabbard_full' : 'scabbard';
  if (n.startsWith('wing_')) return form === 'cape' ? n.replace('wing_', 'cape_') : form === 'abyss' ? n + '_a' : n;
  if (n.startsWith('tendril')) return 'tendril';
  if (n === 'sword_edge') return 'edge_p';
  if (n === 'chest_glow') return 'grid';
  if (n === 'visor_glow') return 'skull';
  return n;
}
// turn the sword about its grip (smallest turn, iterated) until its whole hull is 0.04 b above the floor
function groundSword(G, Q, fwd = [0, 0, -1]) {
  const pts = [...hullOf('sword', 'sword'), ...hullOf('edge_p', 'sword_edge')];
  let out = Q;
  for (let it = 0; it < 8; it++) {
    let lo = null, ly = Infinity;
    for (const P of pts) { const y = G[1] + rot(out, P)[1]; if (y < ly) { ly = y; lo = P; } }
    if (ly >= .04 - 1e-4) break;
    const L = len(lo), d = times(rot(out, lo), 1 / L), minYv = (.04 + 2e-3 - G[1]) / L;
    // turn toward the blade's horizontal heading (a blade pointing straight down turns toward `fwd`)
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
export {PART_NAMES, conj};
