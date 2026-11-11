// The cutscene actor's pose solver (lane H3, hr_design.md §4.2 / §5.3): channel tracks -> the player avatar's pose fields.
//
// The actor is the player avatar's skeleton (tools/build_player_rig.mjs transform(); slim arms) at scale 1.0 for every
// character. A clip is written as channel tracks (tools/player_motion/cine/clips.mjs); solve() turns one tick's channels
// into the pose fields transform() reads (shift, root, torso, head, right_arm, right_elbow, ..., weapon), so the skeleton
// has one definition and the clip JSON files stay in the player_motion format.
//
// Frames. The stage frame ST(r, u, f) of hr_design.md: the origin at the avatar's feet, r to the actor's right, u up, f
// forward (toward her). The rig's authoring frame A (build_player_rig.mjs, mboss_rig_math.mjs): +X = the figure's left,
// +Y up, -Z forward. A = (-r, u, -f): the same handedness, turned half round. Channels are written in ST; the maths runs
// in A. The display turns A's -Z into the entity's forward (the z mirror of transform()).
//
// Channels (numbers and vectors interpolate between keys; `ease` of the later key shapes the segment):
//   root [r,u,f]    the figure's displacement from the stage origin (the manifest's `shift`; u = height over the floor)
//   hip  [r,u,f]    the pelvis offset from its rest point HIP_Y over the root, in the figure's yaw frame (a crouch: u < 0)
//   rot  [x,y,z]    the pelvis / whole-figure rotation (degrees, X then Y then Z: x + leans back, y + turns to its right,
//                   z + tips the top to its right); y is the clip's root yaw
//   tor, head       the torso about the hip line and the head about the neck (same euler order, relative to the parent)
//   fR, fL [r,u,f]  sole targets in ST (absolute: a planted foot does not move when the root does); kR, kL knee poles
//                   (yaw frame directions)
//   lR, lL [x,y,z,k] the leg by angles in the pelvis frame: the thigh's euler and the knee's bend k >= 0; lfR, lfL 0..1
//                   blend the sole from the ST target (0) to the angles (1): flips, the air, kneeling
//   aR, aL [x,y,z,e] the arm by angles in the chest frame: the upper arm's euler (x + swings it forward, z -/+ lifts the
//                   right / left arm outward) and the elbow's bend e >= 0
//   hR, hL [r,u,f]  hand (grip point) targets in ST; pR, pL elbow poles (yaw frame); wR, wL 0..1 blend angles -> target
//   sw [x,y,z]      the sword's euler in the right forearm's frame ([-90,0,0]: the blade square to the forearm, to its
//                   front); bd, bn [r,u,f] the blade's direction and the normal of its broad face in ST; ws 0..1 blends
//   two 0..1        the left hand on the hilt below the right (two hands)
//   look [r,u,f]    a ST point the head turns to (clamped to the neck's range); wl 0..1
//   br 0..1         the idle breathing layer
import {add, sub, times, lerp, dot, cross, len, unit, mul, q, rot, slerp, basisQ, perp, aimQ, sp, smoothK} from '../../mboss_rig_math.mjs';

export const HIP_Y = .765625;                 // .75 + 1/64: straight legs put the outer-layer soles on the floor
export const SOLE = 1 / 64;                   // the outer layer under the shin's base box
export const SK = {hipJ: .125, neck: .75, shoulderX: .34375, shoulderY: .625, armU: .25, fore: .34375, thigh: .375, shin: .375};
export const ARM_REACH = SK.armU + SK.fore, LEG_REACH = SK.thigh + SK.shin;
// Two-bone IK without stretch (mboss_rig_math.ik keeps the last 0.5 % of the reach bent; a standing leg must be straight:
// a shin that tilts digs its sole's edge into the floor). The bend side follows the pole and, as there, turns at most 40
// degrees per tick from the previous one where the pole is weak.
const MAX_BEND = 40 * Math.PI / 180;
function ik(S, W, a, b, pole, prevV = null) {
  const d = sub(W, S), L0 = len(d), u = L0 > 1e-9 ? times(d, 1 / L0) : [0, -1, 0];
  const L = Math.min(Math.max(L0, Math.abs(a - b) + 1e-4), a + b);
  const cosA = Math.max(-1, Math.min(1, (a * a + L * L - b * b) / (2 * a * L))), sinA = Math.sqrt(1 - cosA * cosA);
  const pp = perp(pole, u), strength = len(pp) / Math.max(len(pole), 1e-9);
  let v = len(pp) > 1e-4 ? unit(pp) : unit(perp([0, -1, 0], u));
  if (prevV) {
    const pv = perp(prevV, u);
    if (len(pv) > 1e-4) {
      const P = unit(pv), w = smoothK(.26, .5, strength);
      const ang = Math.atan2(dot(cross(P, v), u), dot(P, v));
      const step = Math.max(-MAX_BEND * w, Math.min(MAX_BEND * w, ang));
      v = unit(add(times(P, Math.cos(step)), times(cross(u, P), Math.sin(step))));
    }
  }
  return {E: add(S, add(times(u, a * cosA), times(v, a * sinA))), W: add(S, times(u, L)), v};
}
// the sword model (skirk_weapon_geometry.mjs: grip [8,8,8], the blade along +Y): distances from the grip point in blocks
export const SWORD = {root: 3 / 16, tip: 23.8 / 16, pommel: -6.1 / 16, guard: 2.8 / 16, left: -.235, half: 1.22 / 16};
export const A = v => [-v[0], v[1], -v[2]];   // ST <-> A (its own inverse)
const conj = Q => [-Q[0], -Q[1], -Q[2], Q[3]];
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const D = 180 / Math.PI;

// euler [x,y,z] (degrees, q = Rz Ry Rx) of a quaternion, the solution nearest `prev` (continuous tracks: +-360, and the
// second solution (x + 180, 180 - y, z + 180))
export function euler(Q, prev = null) {
  const [x, y, z, w] = Q;
  const r00 = 1 - 2 * (y * y + z * z), r10 = 2 * (x * y + z * w), r20 = 2 * (x * z - y * w), r21 = 2 * (y * z + x * w), r22 = 1 - 2 * (x * x + y * y);
  const r11 = 1 - 2 * (x * x + z * z), r12 = 2 * (y * z - x * w);
  let e;
  if (Math.abs(r20) > .999999) e = [Math.atan2(-r12, r11) * D, r20 < 0 ? 90 : -90, 0];
  else e = [Math.atan2(r21, r22) * D, Math.asin(-r20) * D, Math.atan2(r10, r00) * D];
  if (!prev) return e;
  const near = (a, p) => a + 360 * Math.round((p - a) / 360);
  const c1 = e.map((a, i) => near(a, prev[i])), c2 = [e[0] + 180, 180 - e[1], e[2] + 180].map((a, i) => near(a, prev[i]));
  const d = c => c.reduce((s, a, i) => s + Math.abs(a - prev[i]), 0);
  return d(c2) + 1e-9 < d(c1) ? c2 : c1;
}

export const REST = {
  root: [0, 0, 0], hip: [0, 0, 0], rot: [0, 0, 0], tor: [0, 0, 0], head: [0, 0, 0],
  fR: [.125, 0, 0], fL: [-.125, 0, 0], kR: [.06, 0, 1], kL: [-.06, 0, 1],
  lR: [0, 0, 0, 0], lL: [0, 0, 0, 0], lfR: 0, lfL: 0,
  aR: [0, 0, 0, 0], aL: [0, 0, 0, 0], hR: [.3, 1, .3], hL: [-.3, 1, .3], pR: [.6, -.5, -.8], pL: [-.6, -.5, -.8], wR: 0, wL: 0,
  sw: [-90, 0, 0], bd: [0, 0, 1], bn: [1, 0, 0], ws: 0, two: 0,
  look: [0, 1.6, 6], wl: 0, br: 0,
};
export const CHANNELS = Object.keys(REST);

const EASE = {
  l: u => u, io: u => u * u * (3 - 2 * u), i: u => u * u, o: u => 1 - (1 - u) * (1 - u),
  i3: u => u * u * u, o3: u => 1 - (1 - u) ** 3, io5: u => u * u * u * (u * (6 * u - 15) + 10),
};

// Channel tracks. at(t, {ch: value}, ease): a key. mv(t0, t1, {...}, ease): hold what the channel has until t0, reach the
// value at t1. hold(t, ch...): a key with the current value. arc: {ch: [r,u,f]} adds a bump (x 4u(1-u)) to the segment
// that ends at the key (a foot lifting in a step). Keys of one channel are written in time order.
export class Tracks {
  constructor(len, start = {}) {
    this.len = len; this.k = {};
    for (const ch of CHANNELS) this.k[ch] = [{t: 0, v: structuredClone(start[ch] ?? REST[ch]), e: 'l'}];
  }
  val(ch, t) {
    const ks = this.k[ch];
    if (!ks) throw new Error(`unknown channel ${ch}`);
    let i = ks.length - 1;
    while (i > 0 && ks[i].t > t) i--;
    const a = ks[i], b = ks[i + 1];
    if (!b || t <= a.t) return a.v;
    const u = (t - a.t) / (b.t - a.t), e = EASE[b.e](u);
    let v = typeof a.v === 'number' ? a.v + (b.v - a.v) * e : a.v.map((x, j) => x + (b.v[j] - x) * e);
    if (b.arc) v = v.map((x, j) => x + b.arc[j] * 4 * u * (1 - u));
    return v;
  }
  at(t, set, ease = 'io', arc = null) {
    for (const [ch, v] of Object.entries(set)) {
      const ks = this.k[ch];
      if (!ks) throw new Error(`unknown channel ${ch}`);
      if (!EASE[ease]) throw new Error(`unknown ease ${ease}`);
      const last = ks[ks.length - 1];
      if (t < last.t) throw new Error(`channel ${ch}: key at ${t} before its last key ${last.t}`);
      if (typeof v !== typeof REST[ch] || (Array.isArray(v) && v.length !== REST[ch].length)) throw new Error(`channel ${ch}: bad value ${JSON.stringify(v)}`);
      const key = {t, v: structuredClone(v), e: ease, ...(arc?.[ch] ? {arc: arc[ch]} : {})};
      if (t === last.t) ks[ks.length - 1] = key; else ks.push(key);
    }
    return this;
  }
  hold(t, ...chs) { for (const ch of chs) this.at(t, {[ch]: this.val(ch, t)}, 'l'); return this; }
  mv(t0, t1, set, ease = 'io', arc = null) { this.hold(t0, ...Object.keys(set)); return this.at(t1, set, ease, arc); }
  sample(t) { return Object.fromEntries(CHANNELS.map(ch => [ch, this.val(ch, t)])); }
  // segments that change a channel over more than `max` ticks: almost always a forgotten hold before the move
  slow(max = 48) {
    const out = [];
    for (const ch of CHANNELS) for (let i = 1; i < this.k[ch].length; i++) { const a = this.k[ch][i - 1], b = this.k[ch][i]; if (b.t - a.t > max && JSON.stringify(a.v) !== JSON.stringify(b.v)) out.push(`${ch} ${a.t}-${b.t}`); }
    return out;
  }
}

// model-space boxes of the body parts (px about the pivot [8,8,8], the outer layer included): bodyModels() of
// build_player_rig.mjs. [from, to] in blocks.
const px = (from, to, inflate) => [from.map(v => (v - inflate - 8) / 16), to.map(v => (v + inflate - 8) / 16)];
export const BOX = {
  head: px([4, 8, 4], [12, 16, 12], .5), body: px([4, -4, 6], [12, 8, 10], .25),
  right_arm: px([6.5, 4, 6], [9.5, 10, 10], .25), right_forearm: px([6.5, 2, 6], [9.5, 8, 10], .25),
  left_arm: px([6.5, 4, 6], [9.5, 10, 10], .25), left_forearm: px([6.5, 2, 6], [9.5, 8, 10], .25),
  right_leg: px([6, 2, 6], [10, 8, 10], .25), right_shin: px([6, 2, 6], [10, 8, 10], .25),
  left_leg: px([6, 2, 6], [10, 8, 10], .25), left_shin: px([6, 2, 6], [10, 8, 10], .25),
};
export const BASE = Object.fromEntries(Object.entries({
  head: [[4, 8, 4], [12, 16, 12]], body: [[4, -4, 6], [12, 8, 10]],
}).map(([n, [a, b]]) => [n, px(a, b, 0)]));
export const corners = ([a, b]) => [0, 1, 2, 3, 4, 5, 6, 7].map(i => [i & 1 ? b[0] : a[0], i & 2 ? b[1] : a[1], i & 4 ? b[2] : a[2]]);
const SHIN_SOLE = corners(BOX.right_shin).filter(c => c[1] < -.3);

// A limb segment along `dir` in the bend plane of normal n = u x v: its hinge axis (model X) is the plane's normal, so the
// roll is defined for any bend (a front direction is not: a folded arm runs along it). arm: the inside of the bend is the
// segment's front; leg: the outside (the knee cap).
const segQ = (dir, u, v, armLike) => {
  const Y = times(unit(dir), -1), n = unit(cross(u, v)), X = armLike ? times(n, -1) : n, Z = unit(cross(X, Y));
  return basisQ(cross(Y, Z), Y, Z);
};
const qdot = (a, b) => Math.abs(a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3]);
const breath = (t, w) => (w ? w * Math.sin(2 * Math.PI * t / 80) : 0);

// One tick: channels c (Tracks.sample), tick t (the breathing phase), hist (the previous tick's solve, for continuity).
// Returns {pose (the player rig's fields, eulers in degrees), hist, info: {short: IK shortfalls, lift}}.
export function solve(c, t, hist = null) {
  const b = breath(t, c.br), info = {short: {}, lift: 0};
  const Qroot = q(c.rot), Qyaw = q([0, c.rot[1], 0]);
  const hipW = add(add(A(c.root), [0, HIP_Y, 0]), rot(Qyaw, A([c.hip[0], c.hip[1] + .004 * b, c.hip[2]])));
  const tor = [c.tor[0] - .7 * b, c.tor[1], c.tor[2]];
  const Qbody = mul(Qroot, q(tor));
  const neck = add(hipW, rot(Qbody, [0, SK.neck, 0]));
  // head: its angles, or turned to the look point within the neck's range
  let headE = [c.head[0] + .5 * b, c.head[1], c.head[2]];
  let Qhead = mul(Qbody, q(headE));
  if (c.wl > 0) {
    const eye = add(neck, rot(Qbody, [0, .25, 0])), d = unit(sub(A(c.look), eye));
    const up = rot(Qbody, [0, 1, 0]), Z = times(d, -1);
    let X = cross(up, Z); X = len(X) < 1e-4 ? rot(Qbody, [1, 0, 0]) : unit(X);
    const rel = euler(mul(conj(Qbody), basisQ(X, cross(Z, X), Z)));
    const lim = [clamp(rel[0], -50, 50), clamp(rel[1], -80, 80), 0];
    Qhead = slerp(Qhead, mul(Qbody, q(lim)), c.wl);
  }
  // legs. The shin is a box without an ankle: a tilted shin digs an edge of its sole into the floor, so the sole target rises
  // until the lowest corner of the outer layer is on the floor (the least rise that does it).
  const leg = side => {
    const sx = side === 'R' ? -1 : 1, J = add(hipW, rot(Qroot, [sx * SK.hipJ, 0, 0]));
    const fk = c['l' + side], w = 1 - c['lf' + side];
    const Qfk = mul(Qroot, q(fk.slice(0, 3))), Qsfk = mul(Qfk, q([-fk[3], 0, 0])), kneeFk = add(J, rot(Qfk, [0, -SK.thigh, 0]));
    const soleFk = add(kneeFk, rot(Qsfk, [0, -SK.shin, 0]));
    if (w < 1e-6) return {J, E: kneeFk, W: soleFk, v: rot(Qfk, [0, 0, -1]), Ql: Qfk, Qs: Qsfk};
    const T = A(c['f' + side]); T[1] += SOLE;
    const P0 = lerp(soleFk, T, w);
    const pole = lerp(rot(Qfk, [0, 0, -1]), unit(rot(Qyaw, A(c['k' + side]))), w);
    let short = 0;
    const at = h => {
      const P = [P0[0], P0[1] + h, P0[2]], d = sub(P, J), L = len(d);
      short = Math.max(0, L - LEG_REACH);
      const s = ik(J, L > LEG_REACH ? add(J, times(d, LEG_REACH / L)) : P, SK.thigh, SK.shin, pole, hist?.v?.['leg' + side] || null);
      const ul = unit(sub(s.W, J)), Ql = segQ(sub(s.E, J), ul, s.v, false), Qs = segQ(sub(s.W, s.E), ul, s.v, false);
      return {J, E: s.E, W: s.W, v: s.v, Ql, Qs, low: Math.min(...SHIN_SOLE.map(p => add(s.E, rot(Qs, p))[1]))};
    };
    let out = at(0);
    if (out.low < -1e-4) {
      let lo = 0, hi = null, best = out;
      for (let k = 1; k <= 60 && hi === null; k++) { const o = at(.005 * k); if (o.low > best.low) best = o; if (o.low >= -1e-4) hi = .005 * k; else lo = .005 * k; }
      if (hi === null) out = best;
      else { for (let i = 0; i < 12; i++) { const m = (lo + hi) / 2; if (at(m).low >= -1e-4) hi = m; else lo = m; } out = at(hi); }
    }
    if (w > .999 && short > 1e-4) info.short['foot' + side] = short;
    return out;
  };
  const LR = leg('R'), LL = leg('L');
  // arms and the sword
  const arm = (side, target, w) => {
    const sx = side === 'R' ? -1 : 1, S = add(hipW, rot(Qbody, [sx * SK.shoulderX, SK.shoulderY, 0]));
    const fk = c['a' + side], fe = [fk[0] + (side === 'R' ? 1 : -1) * .8 * b, fk[1], fk[2]];
    const Qfk = mul(Qbody, q(fe)), Qffk = mul(Qfk, q([fk[3], 0, 0])), elbFk = add(S, rot(Qfk, [0, -SK.armU, 0]));
    const handFk = add(elbFk, rot(Qffk, [0, -SK.fore, 0]));
    if (w < 1e-6) return {S, E: elbFk, W: handFk, v: rot(Qfk, [0, 0, 1]), Qa: Qfk, Qf: Qffk};
    const P = lerp(handFk, target, w), pole = lerp(rot(Qfk, [0, 0, 1]), unit(rot(Qyaw, A(c['p' + side]))), w);
    const d = sub(P, S), L = len(d), Pc = L > ARM_REACH ? add(S, times(d, ARM_REACH / L)) : P;
    const s = ik(S, Pc, SK.armU, SK.fore, pole, hist?.v?.['arm' + side] || null);
    const ua = unit(sub(s.W, S));
    if (w > .999 && L - ARM_REACH > 1e-4) info.short['hand' + side] = L - ARM_REACH;
    return {S, E: s.E, W: s.W, v: s.v, Qa: segQ(sub(s.E, S), ua, s.v, true), Qf: segQ(sub(s.W, s.E), ua, s.v, true)};
  };
  const AR = arm('R', A(c.hR), c.wR);
  // The sword looks the same rolled half round its blade. The held-in-space frame takes the roll nearer the in-hand frame (a
  // blend goes the short way), and what is shown takes the roll nearer the tick before, so neither a blend nor a turning
  // edge ever spins the blade through 180 degrees.
  const QwFk = mul(AR.Qf, q(c.sw));
  let QwAbs = sp(A(c.bd), A(c.bn));
  { const alt = mul(QwAbs, [0, 1, 0, 0]); if (qdot(alt, QwFk) > qdot(QwAbs, QwFk)) QwAbs = alt; }
  let Qw = c.ws <= 0 ? QwFk : slerp(QwFk, QwAbs, c.ws);
  if (hist?.Qw) { const alt = mul(Qw, [0, 1, 0, 0]); if (qdot(alt, hist.Qw) > qdot(Qw, hist.Qw)) Qw = alt; }
  const blade = rot(Qw, [0, 1, 0]);
  const pommel = add(AR.W, times(blade, SWORD.left));
  const wL = c.wL + (1 - c.wL) * c.two;
  const tL = c.two > 0 ? (c.wL > 0 ? lerp(pommel, lerp(A(c.hL), pommel, c.two), c.wL / wL) : pommel) : A(c.hL);
  const AL = arm('L', tL, wL);
  // the fields transform() reads
  const E = (name, Q) => euler(Q, hist?.pose?.[name] || null);
  const pose = {
    shift: sub(hipW, [0, .75, 0]),
    root: E('root', Qroot), torso: E('torso', mul(conj(Qroot), Qbody)), head: E('head', mul(conj(Qbody), Qhead)),
    right_arm: E('right_arm', mul(conj(Qbody), AR.Qa)), right_elbow: E('right_elbow', mul(conj(AR.Qa), AR.Qf)),
    left_arm: E('left_arm', mul(conj(Qbody), AL.Qa)), left_elbow: E('left_elbow', mul(conj(AL.Qa), AL.Qf)),
    right_leg: E('right_leg', mul(conj(Qroot), LR.Ql)), right_knee: E('right_knee', mul(conj(LR.Ql), LR.Qs)),
    left_leg: E('left_leg', mul(conj(Qroot), LL.Ql)), left_knee: E('left_knee', mul(conj(LL.Ql), LL.Qs)),
    weapon: E('weapon', mul(conj(AR.Qf), Qw)), weapon_shift: [0, 0, 0], weapon_scale: [1, 1, 1],
  };
  return {pose, info, hist: {pose, Qw, v: {legR: LR.v, legL: LL.v, armR: AR.v, armL: AL.v}}};
}

// the shoulder joints (ST) of a channel set: where the arms hang from (the clip helpers fit the body to a grip with it)
export function shoulders(c) {
  const Qroot = q(c.rot), Qyaw = q([0, c.rot[1], 0]), Qbody = mul(Qroot, q(c.tor));
  const hipW = add(add(A(c.root), [0, HIP_Y, 0]), rot(Qyaw, A(c.hip)));
  return {R: A(add(hipW, rot(Qbody, [-SK.shoulderX, SK.shoulderY, 0]))), L: A(add(hipW, rot(Qbody, [SK.shoulderX, SK.shoulderY, 0])))};
}
// the hip offset u (channel hip[1]) that rests the lowest point of the legs and the torso on the floor (a kneel, a crouch)
export function groundHip(c, t = 0) {
  let lo = c.hip[1] - .6, hi = c.hip[1] + .6;
  const low = u => { const p = solve({...c, hip: [c.hip[0], u, c.hip[2]], br: 0}, t).pose, f = frames(p); let m = Infinity;
    for (const [n, box] of Object.entries(BOX)) if (/leg|shin|body/.test(n)) for (const cn of corners(box)) m = Math.min(m, add(f[n].t, rot(f[n].q, cn))[1]); return m; };
  for (let i = 0; i < 24; i++) { const m = (lo + hi) / 2; if (low(m) >= -3e-4) hi = m; else lo = m; }
  return hi + 3e-4;
}
// The part frames in A of a pose in the player rig's fields: transform() of build_player_rig.mjs before its display
// mirror (the same joints and lengths; tested against transform() by the builder). {part: {t, q}} + named points.
export function frames(p) {
  const root = q(p.root), body = q(p.torso), hip = add([0, .75, 0], p.shift), out = {};
  const top = add(hip, rot(body, [0, .75, 0]));
  out.body = {t: top, q: body}; out.head = {t: top, q: mul(body, q(p.head))};
  for (const [side, sign] of [['right', -1], ['left', 1]]) {
    const shoulder = add(hip, rot(body, [sign * .34375, .625, 0]));
    const arm = mul(body, q(p[side + '_arm'])), elbow = add(shoulder, rot(arm, [0, -.25, 0])), fore = mul(arm, q(p[side + '_elbow']));
    out[side + '_arm'] = {t: shoulder, q: arm}; out[side + '_forearm'] = {t: elbow, q: fore};
    const leg = q(p[side + '_leg']), pelvis = add(hip, [sign * .125, 0, 0]);
    out[side + '_leg'] = {t: pelvis, q: leg};
    out[side + '_shin'] = {t: add(pelvis, rot(leg, [0, -.375, 0])), q: mul(leg, q(p[side + '_knee']))};
    if (side === 'right') out.weapon = {t: add(add(elbow, rot(fore, [0, -.34375, 0])), rot(fore, p.weapon_shift)), q: mul(fore, q(p.weapon))};
  }
  for (const v of Object.values(out)) { v.t = add(hip, rot(root, sub(v.t, hip))); v.q = mul(root, v.q); }
  return out;
}
// named points of a pose in ST (the manifest's columns and the contact checks)
export function points(p) {
  const f = frames(p), at = (n, v) => A(add(f[n].t, rot(f[n].q, v)));
  return {
    hilt: at('weapon', [0, 0, 0]), tip: at('weapon', [0, SWORD.tip, 0]), pommel: at('weapon', [0, SWORD.pommel, 0]), guard: at('weapon', [0, SWORD.guard, 0]),
    hand_r: at('right_forearm', [0, -SK.fore, 0]), hand_l: at('left_forearm', [0, -SK.fore, 0]),
    foot_r: at('right_shin', [0, -SK.shin - SOLE, 0]), foot_l: at('left_shin', [0, -SK.shin - SOLE, 0]),
    knee_r: at('right_shin', [0, 0, 0]), knee_l: at('left_shin', [0, 0, 0]),
    head: at('head', [0, .25, 0]), chest: at('body', [0, -.3, 0]), waist: at('body', [0, -.7, 0]), hip: A(add([0, .75, 0], p.shift)),
    shoulder_r: at('right_arm', [0, 0, 0]), shoulder_l: at('left_arm', [0, 0, 0]),
  };
}
// the lowest point (A y = ST u) of the body boxes and of the sword's axis
export function lowest(p) {
  const f = frames(p);
  let body = Infinity, part = '';
  for (const [n, box] of Object.entries(BOX)) for (const cn of corners(box)) { const y = add(f[n].t, rot(f[n].q, cn))[1]; if (y < body) { body = y; part = n; } }
  const sword = Math.min(...[SWORD.pommel, SWORD.tip].map(d => add(f.weapon.t, rot(f.weapon.q, [0, d, 0]))[1]));
  return {body, part, sword};
}
// blade samples (root..tip, the axis) inside the head / torso base boxes: the deepest penetration in blocks (0 = none)
export function bladeInBody(p) {
  const f = frames(p);
  let worst = 0;
  for (let i = 0; i <= 12; i++) {
    const P = add(f.weapon.t, rot(f.weapon.q, [0, SWORD.root + (SWORD.tip - SWORD.root) * i / 12, 0]));
    for (const n of ['head', 'body']) {
      const L = rot(conj(f[n].q), sub(P, f[n].t)), [a, bb] = BASE[n];
      const depth = Math.min(...L.map((x, j) => Math.min(x - a[j], bb[j] - x)));
      if (depth > worst) worst = depth;
    }
  }
  return worst;
}
export {add, sub, times, lerp, dot, cross, len, unit, mul, q, rot, slerp, sp, aimQ};
