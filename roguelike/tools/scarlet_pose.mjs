// Skeleton and pose solver of the 홍련 (Scarlet) rig (S:hr/PLAN.md §2.1-2.6; S2d: the player avatar's skeleton). solve(p, hist,
// plan, ctx) turns one pose (the channels below, sampled from scarlet_clips.mjs or S2b's scarlet_cine.mjs and retargeted to this
// skeleton by scarlet_retarget.mjs) into the rig-frame transform {t, q, s} of each of the 29 parts. There is no runtime
// parenting: the look states that re-parent a part (hat worn / back / hand / world / gone, scabbard hand / hip / gone, cup /
// bottle hand / rock / none; api.REPARENT) are pose channels solved here every tick.
//
// Frames. Rig frame: +X her left, +Y up, -Z forward, blocks; the origin is the anchor (the boss body) on the floor.
// Quaternions [x, y, z, w]; eulers [pitch, yaw, roll] in degrees as mboss_rig_math.q (pitch + leans back / lifts the toes,
// yaw + turns her to her right, roll + tips the top toward her right). Bearings (dirBE): 0 = forward, + = her right.
//
// The skeleton (S2d, 11-05) is the player avatar's (tools/build_player_rig.mjs transform(); classic arms): the hip line HIP_Y
// 0.765625 above the floor at pos 0 (straight legs put the shin's outer-layer sole on the floor), the hip joints 0.125 to the
// sides, the torso pivot at the seam (body row 9, 0.1875 above the hip line), the neck 0.5625 above it, the shoulder pivots
// 0.4375 above it and 0.375 to the sides, the elbow 0.25 below the shoulder, the grip (the avatar's weapon point) 0.34375
// below the elbow, the knee 0.375 below the hip joint and the outer-layer sole 0.390625 below the knee. Every IK target is
// clamped to the chain's reach (no stretch).
//
// Pose channels (numbers / vectors interpolate; the discrete ones switch at their key: DISCRETE in scarlet_clips.mjs). The
// clips are authored on S2a's skeleton; scarlet_retarget.mjs maps every sample to this one (angles kept, the pelvis offset,
// the foot / hand targets and the grip distances scaled) and adds the derived weights (w*) below.
//   pos [x,y,z]        the pelvis offset (its pivot = the hip line, HIP_Y above the floor at rest)
//   rot [p,y,r]        the pelvis: yaw = the facing of the whole figure, then pitch / roll of the hips
//   tor [p,y,r]        the torso about the seam;  head [p,y,r]  the head about the neck
//   fL, fR [x,y,z]     sole targets in the yaw frame from the floor point under the pelvis (y 0 = planted);
//   lf 0..1            blends the sole targets into the pelvis frame (flips, tumbles, lying: the legs move with the body)
//   kL, kR [x,y,z]     knee poles (yaw frame; default forward)
//   hold 0|1           the sword in her LEFT hand (sword hand); 0 = the left arm free (aL / plL)
//   gB gE gD           the grip on a sphere about the swing centre (SK.swing above the pelvis pivot, yaw frame): bearing,
//                      elevation (deg), distance (b); interpolated as numbers, so a cut sweeps on an arc
//   gF gL              grip follow: 1 = the grip on the lever gL from her left shoulder (the chest centre with rh 1) along
//                      the blade, so a sweep turns about the shoulder
//   cB cR th ed tw     the blade: its tip at angle th in the cutting plane through bearing cB rolled by cR (0 vertical: th 0
//                      forward, 90 up; 90 horizontal: th + toward her left), the edge leading toward +th (ed 1) or -th
//                      (ed -1), twisted by tw about the blade (yaw frame)
//   rh 0..1            her right hand on the hilt below the left (two hands) .. free
//   aL, aR [p,r,k]     free hand targets about the shoulder (chest frame): pitch (+ forward / up), roll (+ out), reach 0..1
//   plL, plR [x,y,z]   planted hand targets (yaw frame from the floor point under the pelvis), weights plwL, plwR
//   pL, pR [x,y,z]     elbow poles (chest frame; x side-signed: + = outward);  frL, frR  free forearm roll (unused: box hands)
//   bwL, bwR 0..1      the hand to the hat brim (worn): the fist under the brim's side at azimuth clamp(bz + 50, 70, 90) (deg
//                      from her front toward the hand's side); pair with hand 'brim'
//   hiL 0..1           the left hand to the sheathed hilt (the iai grip; the draw); hsR 0..1 the right hand to the scabbard's
//                      throat at the hip;  scHip [p,y]  the hip scabbard turned about its mouth (deg, pelvis frame)
//   hairF 0..1, hairS  (S2a's ponytail; the hair is the skin's own since S2d: unused)
//   vis 0..1           everything scaled about the body centre (the ghost vanish / reappear)
//   sh 0..1, shW 0..1  sheathing: the sword slides into the scabbard (sh 0 = the tip at the mouth, 1 = the guard at the
//                      mouth); shW blends the sword from the free blade frame onto the scabbard's axis
//   skF                the sash's outward swing scale (1 = rest); skG skIF skIB skW (S2a's skirt panels: unused)
//   hwP [x,y,z], hwE [p,y,r]   the hat in the world state (rig frame: relative to the root); scarlet_retarget.mjs maps the
//                      source spots onto HAT_REST and re-anchors the thrown paths (hwF: the flight's position)
//   hhB hhE, hhN [b,e] the hat in the right hand: the direction hand -> brim centre (bearing / elevation, yaw frame) and
//                      the crown's direction
//   scB scE scR        the scabbard in the right hand: its body direction from the mouth (bearing, elevation; yaw frame)
//                      and its roll about the body (edge side); scOff where the hand grips it (blocks from the mouth)
//   cupP, botP [x,y,z] (unused: the rock state is never keyed);  cupT, botT  the cup / bottle tilt in the hand (deg, pouring)
//   discrete: hat (worn|back|hand|world|gone), sword (hand|sheathed|gone), scab (hip|hand|gone), face (calm|smile|closed),
//             hL, hR (open|grip|brim), cup, bottle (none|hand|rock)
//   ph                 the loop phase 0..1 (idle sway, set by the sampler)
//   derived (scarlet_retarget.mjs): wSeat (seated on the kit's stone), wLie (lying on her back), wKnee (the right knee on the
//             floor), wLip (the cup at her lips), hatX (the hat state hand-overs), hwF (a re-anchored world-hat flight)
import {add, sub, times, len, unit, mul, q, rot, aimQ, ik, basisQ, cross, dot, perp, slerp, armFront, steadyPerp, toDisplayT, toDisplayQ, lerp} from './mboss_rig_math.mjs';
import {PART_NAMES, PART_SCALE, SWORD, SCAB, HAT, STRINGS, CUP, BOTTLE, HILT_OFF, modelPoints, HAND_MODELS, FACE_MODELS, PHASE_MODELS, HIDDEN} from './scarlet_geometry.mjs';

export const HIP_Y = .765625;
const unit3 = v => { const m = Math.hypot(...v); return v.map(x => x / m); };
export const SK = {
  hipJ: [.125, 0, 0], waist: [0, .1875, 0], neckB: [0, .5625, 0], shoulder: [.375, .4375, 0],
  armU: .25, fore: .34375, thigh: .375, shin: .390625, ankleY: 0,
  brim: [0, .567, 0], brimTilt: -6, hatBack: [0, .25, .30], hatHand: HAT.R - .04,
  brimHold: {r: .44, azAdd: 50, azMin: 70, azMax: 90, dy: -.07},
  sashKnot: [.26, .09, -.10],
  scabHip: [-.25, .19, -.18], scabHipDir: unit3([-.45, -.42, .79]),
  swing: [0, .55, 0], twoHand: .22, hilt: HILT_OFF, throat: .16,
  anchors: {head: [0, .25, -.02], chest: [0, .30, -.06]}, vis: .30,
  lipMouth: [0, .09, -(.28125 + CUP.r + .02)],
};
export const ARM_REACH = .995 * (SK.armU + SK.fore), LEG_REACH = .995 * (SK.thigh + SK.shin);
const ARM_TURN = 85, ARM_FOLD = .15;
// the fist on the world hat's brim edge: the grip point this far above the brim (the fist's end rests on the brim)
export const HAT_FLOOR_HOLD = .08;
// a contact is measured (and assisted) where its weight is full
const FULL = .999;
// the bounds of the correction guards (their own units: degrees, or cm for the distance guards) and the plan slopes per tick
export const GUARD_BOUND = {scab: 150, scabY: 90, scabH: 90, hat: 60, strings: 120, sash: 120, drop: 12, closeY: 30, incl: 20, tip: 15, rock: 12,
  aHeadR: 10, aTorY: 15, aTorP: 15, aTorR: 8, bPush: 35, bTurn: 60, close: 30, hatBackZ: 15, hatPush: 100};
export const GUARD_SLOPE = {scab: 22, scabY: 22, scabH: 22, hat: 22, strings: 22, sash: 22, drop: 1.5, closeY: 5, incl: 5, tip: 5, rock: 5,
  aHeadR: 5, aTorY: 5, aTorP: 5, aTorR: 5, bPush: 4, bTurn: 15, close: 3, hatBackZ: 3, hatPush: 15};
const D = Math.PI / 180;
export const dirBE = (b, e = 0) => { const B = b * D, E = e * D; return [-Math.sin(B) * Math.cos(E), Math.sin(E), -Math.cos(B) * Math.cos(E)]; };
const ID = [0, 0, 0, 1];
const safeAxis = v => (len(v) < 1e-4 ? [1, 0, 0] : unit(v));
const sm = u => { const x = Math.max(0, Math.min(1, u)); return x * x * (3 - 2 * x); };
// a gravity pull's weight fades out as the part turns past horizontal (no 180-degree fromTo flips when she is upside down)
const gfade = dn => Math.max(0, Math.min(1, .5 - dn[1]));
export const conj = Q => [-Q[0], -Q[1], -Q[2], Q[3]];
// limit a chain direction's turn per tick to maxDeg, measured from the previous direction carried along by its root's own
// rotation since the previous tick (a flip or a spin turns the chain with the body; only the swing is rate-limited)
function rateLimit(d, pd, dq, maxDeg) {
  if (!pd) return d;
  const c = dq ? rot(dq, pd) : pd, ang = Math.acos(Math.max(-1, Math.min(1, dot(c, d))));
  if (ang <= maxDeg * D) return d;
  const ax = cross(c, d);
  return len(ax) > 1e-6 ? rot(qa(unit(ax), maxDeg), c) : d;
}
export const qa = (axis, deg) => { const s = Math.sin(deg * D / 2); return [axis[0] * s, axis[1] * s, axis[2] * s, Math.cos(deg * D / 2)]; };
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
// IK without stretch: the target clamped to the chain's reach from the root (ik() never stretches then); short = the shortfall
function ikReach(S, W, a, b, pole, prevV) {
  const d = sub(W, S), L = len(d), R = .995 * (a + b);
  const Wc = L > R ? add(S, times(d, R / L)) : W;
  const sol = ik(S, Wc, a, b, pole, prevV);
  sol.short = len(sub(sol.W, W)); sol.target = W;
  return sol;
}

// ---- hulls (blocks, part space at display scale) ---------------------------------------------------------------------------
let HULLS = null;
// the base box (element 0) of every body model (part frame, blocks): the blade-body guard and the lying / seat contacts
export const BOX = {};
const DIRS = (() => { const L = []; for (let i = -3; i <= 3; i++) for (let j = -3; j <= 3; j++) for (const [a, b, c] of [[1, i / 3, j / 3], [-1, i / 3, j / 3]]) L.push([a, b, c], [b, a, c], [b, c, a]); return L; })();
function support(pts) {
  if (pts.length <= 24) return pts;
  const keep = new Set();
  for (const d of DIRS) { let best = -Infinity, bi = 0; for (let i = 0; i < pts.length; i++) { const v = pts[i][0] * d[0] + pts[i][1] * d[1] + pts[i][2] * d[2]; if (v > best) { best = v; bi = i; } } keep.add(bi); }
  return [...keep].sort((x, y) => x - y).map(i => pts[i]);
}
export function setModels(models) {
  HULLS = {};
  HCACHE.clear();
  HAT_VIS = null;
  for (const [n, els] of Object.entries(models)) {
    const seen = new Set(), pts = [];
    for (const P of modelPoints(els)) { const k = P.map(v => v.toFixed(3)).join(); if (!seen.has(k)) { seen.add(k); pts.push(P); } }
    HULLS[n] = support(pts);
    if (n === 'hat_p1') {
      // the hat's visible points (blocks): the crown's corners and the brim's painted ring (radius HAT.R) at the heights of
      // the brim squares (their corners outside the ring are transparent)
      const k = PART_SCALE.hat / 16, R = HAT.R / k, ys = [...new Set(pts.filter(P => Math.hypot(P[0], P[2]) > R + .1).map(P => P[1]))];
      HAT_VIS = [...pts.filter(P => Math.hypot(P[0], P[2]) <= R + .1),
        ...ys.flatMap(y => Array.from({length: 32}, (_, i) => [R * Math.cos(i * Math.PI / 16), y, R * Math.sin(i * Math.PI / 16)]))].map(P => P.map(x => x * k));
    }
  }
  for (const [n, m] of [['head', 'head'], ['torso', 'torso'], ['pelvis', 'pelvis'], ['arm_l', 'arm_l'], ['arm_r', 'arm_r'], ['forearm_l', 'forearm_l_grip'],
    ['forearm_r', 'forearm_r_grip'], ['thigh_l', 'thigh_l'], ['thigh_r', 'thigh_r'], ['shin_l', 'shin_l'], ['shin_r', 'shin_r']]) {
    const e = models[m][0], X = [(8 - e.from[0]) / 16, (8 - e.to[0]) / 16], Z = [(e.from[2] - 8) / 16, (e.to[2] - 8) / 16];
    BOX[n] = [[Math.min(...X), (e.from[1] - 8) / 16, Math.min(...Z)], [Math.max(...X), (e.to[1] - 8) / 16, Math.max(...Z)]];
    const o = models[m][1], OX = [(8 - o.from[0]) / 16, (8 - o.to[0]) / 16], OZ = [(o.from[2] - 8) / 16, (o.to[2] - 8) / 16];
    BOX[n + '_layer'] = [[Math.min(...OX), (o.from[1] - 8) / 16, Math.min(...OZ)], [Math.max(...OX), (o.to[1] - 8) / 16, Math.max(...OZ)]];
  }
}
const HCACHE = new Map();
let HAT_VIS = null;
export const hatVisPts = () => HAT_VIS;
export const hullOf = (model, n) => {
  const key = model + '|' + n;
  if (!HCACHE.has(key)) { const k = PART_SCALE[n] / 16; HCACHE.set(key, (HULLS[model] || []).map(P => [P[0] * k, P[1] * k, P[2] * k])); }
  return HCACHE.get(key);
};
export function qm(Q) {
  const [x, y, z, w] = Q;
  return [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)], [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]];
}
export const minY = (pts, t, Q, s = 1) => { const r = qm(Q)[1]; let m = Infinity; for (const P of pts) { const y = t[1] + s * (r[0] * P[0] + r[1] * P[1] + r[2] * P[2]); if (y < m) m = y; } return m; };
// the depth of a world point inside a part's box (part frame), > 0 inside
export function boxDepth(P, v, box) {
  const L = rot(conj(v.q), sub(P, v.t)), [lo, hi] = box;
  return Math.min(L[0] - lo[0], hi[0] - L[0], L[1] - lo[1], hi[1] - L[1], L[2] - lo[2], hi[2] - L[2]);
}
// guard bookkeeping of one solve: GUARD.min = the plan of this tick (the smoothed minimum / applied value of each guard),
// GUARD.used = {name: value} (degrees, or cm for the distance guards; {v, dir} for the vector guards bPush / bTurn / close)
let GUARD = {min: {}, used: {}, prefer: {}, sense: {}};
// turn a segment (pivot t, rotation Q, hull pts) about `axis` by the smallest angle (sense +1 / -1, or 0 = either) so its
// hull clears y >= clear; returns the new Q
function clearFloor(t, Q, pts, axis, clear, maxDeg = 100, sense = 1, name = null, s = 1) {
  const a0 = name ? Math.min(GUARD.min[name] || 0, maxDeg) : 0;
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
  best.failed = best[0] > maxDeg;
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
// the core parts (the generic floor rule, the lying / seat roots) and the parts whose hull lifts the whole figure off the floor
export const CORE = ['pelvis', 'torso', 'head', 'thigh_l', 'thigh_r', 'shin_l', 'shin_r'];
const LIFT_PARTS = ['pelvis', 'torso', 'head', 'face', 'arm_l', 'forearm_l', 'arm_r', 'forearm_r', 'thigh_l', 'shin_l', 'thigh_r', 'shin_r'];
// the blade-body guard's boxes (the hands hold the hilt and the scabbard by design)
const BLADE_BODY = ['head', 'torso', 'pelvis', 'thigh_l', 'thigh_r', 'shin_l', 'shin_r', 'arm_r', 'arm_l'];
// the body boxes a flying world hat keeps out of
const HAT_CLEAR = ['head', 'torso', 'pelvis', 'arm_l', 'arm_r', 'forearm_l', 'forearm_r', 'thigh_l', 'thigh_r', 'shin_l', 'shin_r'];

// the free blade frame of a pose (no arm, no guard): the grip G and the blade rotation SQ (also the builder's SH0' probe)
export function freeBlade(p, R, Ryaw, SL, Cw) {
  const u0 = rot(Ryaw, dirBE(p.cB, 0)), v0 = rot(qa(u0, p.cR), rot(Ryaw, [0, 1, 0]));
  const T0 = add(times(u0, Math.cos(p.th * D)), times(v0, Math.sin(p.th * D)));
  let Ed = add(times(u0, -Math.sin(p.th * D)), times(v0, Math.cos(p.th * D)));
  const twist = 90 * (1 - Math.max(-1, Math.min(1, p.ed))) + (p.tw || 0);
  if (Math.abs(twist) > 1e-6) Ed = rot(qa(T0, twist), Ed);
  const SQ = bladeQ(T0, Ed);
  const Gs = add(Cw, times(rot(Ryaw, dirBE(p.gB, p.gE)), p.gD));
  const Gf = add(lerp(SL, Cw, Math.min(1, p.rh || 0)), times(T0, p.gL || .55));
  return {G: lerp(Gs, Gf, p.gF || 0), SQ, T0};
}

// ---- solve -----------------------------------------------------------------------------------------------------------------
// p: full (retargeted) pose; hist(k): the solved output k ticks before (or null); plan: the planned guard values of this tick
// (builder pass 2+); ctx: {pass, clip, t, ref (refCore of the source)}. Returns {part: {t, q, s}} (rig frame)
// plus non-enumerable extras (_anchors, _prev, _guard, _lift, _corr, _contacts, _stretch, _support, _hatQ, _sashKnot).
export function solve(p, hist = () => null, plan = {}, ctx = {}) {
  const o = {};
  const part = (n, t, Q, s = 1) => { o[n] = {t, q: Q, s: Array.isArray(s) ? s : [s, s, s]}; };
  const prev = hist(1)?._prev || {}, keep = {};
  const pass2 = (ctx.pass || 1) > 1;
  GUARD = {min: plan, used: {}, prefer: prev.gs || {}, sense: {}};
  const pl = n => plan[n] ? (typeof plan[n] === 'number' ? plan[n] : plan[n].v) : 0;
  const pls = n => pl(n + '+') - pl(n + '-');
  const setS = (n, v) => { GUARD.used[n + '+'] = Math.max(0, v); GUARD.used[n + '-'] = Math.max(0, -v); };
  const contacts = {}, stretch = {arm: 1, leg: 1};
  const wSeat = p.wSeat || 0, wLie = p.wLie || 0, wKnee = p.wKnee || 0, wLip = p.wLip || 0;
  const lf = Math.max(0, Math.min(1, p.lf || 0));

  // ---- 1-2. the root: pelvis offset, the planted-feet drop (planned), the seat; the lying rest (below, with the torso) ----
  const Ryaw = q([0, p.rot[1], 0]);
  const floorP = [p.pos[0], 0, p.pos[2]];
  const drop = pl('drop') / 100;
  let R = [p.pos[0], HIP_Y + p.pos[1] - drop, p.pos[2]];
  if (wSeat > 0) R[1] += (SUP.T + .1406 + .004 - R[1]) * wSeat;
  // ---- 3. the torso about the seam, the head about the neck (lying incline / chin tip / rock; the reach assists; the IAI turn)
  let lie = {incl: 0, tip: 0, rock: 0};
  // the reach assists (planned): torso yaw / bow / roll with the head counter-turned (br: a torso roll for the brim, the head
  // rolling with it), the head roll for the brim
  const assist = {y: pls('aTorY'), p: pls('aTorP'), r: pls('aTorR'), hr: pls('aHeadR')};
  const frame = (R0, lieX, as) => {
    const Pq = mul(Ryaw, q([p.rot[0] + lieX.rock, 0, p.rot[2]]));
    const Wst = add(R0, rot(Pq, SK.waist));
    const Cq = mul(Pq, q([p.tor[0] - lieX.incl - as.p, p.tor[1] + as.y, p.tor[2] + as.r]));
    const Nb = add(Wst, rot(Cq, SK.neckB));
    const Hq = mul(Cq, q([p.head[0] - lieX.tip, p.head[1] - as.y, p.head[2] - as.r + as.hr]));
    return {Pq, Wst, Cq, Nb, Hq};
  };
  if (pass2) lie = {incl: pl('incl'), tip: pl('tip'), rock: pls('rock')};
  let {Pq, Wst, Cq, Nb, Hq} = frame(R, lie, assist);
  const chestFwd = () => rot(Cq, [0, 0, -1]);

  // ---- 4. legs (IK clamped to the reach; seated feet; the boot loop; the kneel root; the planted-feet drop measured) ----
  const segQ = (key, dir, front) => { const F = steadyPerp(front, unit(dir), prev['f_' + key], [0, 0, -1]); keep['f_' + key] = F; return aimQ(dir, F); };
  let legs = {};
  const solveLegs = (lfX = lf, only = null) => {
    if (!only) legs = {};
    let need = 0;
    for (const [s, k, F, kp] of [[1, 'l', p.fL, p.kL], [-1, 'r', p.fR, p.kR]]) {
      if (only && !only.includes(k)) continue;
      const H = add(R, rot(Pq, [SK.hipJ[0] * s, SK.hipJ[1], SK.hipJ[2]]));
      const Aw = add(floorP, rot(Ryaw, F)), Ab = add(R, rot(Pq, [F[0], F[1] - HIP_Y, F[2]]));
      let A = lerp(Aw, Ab, lfX);
      if (wSeat > 0) {
        const Hy = rot(conj(Ryaw), sub(H, floorP));
        A = lerp(A, add(floorP, rot(Ryaw, [Hy[0], 0, Hy[2] - .36])), wSeat);
      }
      let pole = rot(lf > .5 ? Pq : Ryaw, kp || [s * .12, 0, -1]);
      // kneeling: the right knee bends toward its spot on the floor, down-forward of the hip joint
      if (k === 'r' && wKnee > 0) pole = unit(lerp(unit(pole), unit(rot(Ryaw, [0, -.55, -.83])), wKnee));
      const fwd = rot(lf > .5 ? Pq : Ryaw, [0, 0, -1]);
      // the planted-feet drop: how far the hip joint must come down for the leg to reach a planted target (cm)
      if (lf < .5 && F[1] <= .0066 && wSeat < .5 && wKnee < .5) {
        const hz = Math.hypot(A[0] - H[0], A[2] - H[2]), dy = H[1] - A[1];
        if (hz < LEG_REACH) need = Math.max(need, dy - Math.sqrt(LEG_REACH * LEG_REACH - hz * hz));
      }
      let sol, thQ, shQ;
      // the boot loop (the sole end on the floor); the kneeling right shin rests on its knee (the kneel root sets her height),
      // only its foot end is kept off the floor
      const kneel = k === 'r' && wKnee > .5, hp = hullOf('shin_' + k, 'shin_' + k), hpts = kneel ? hp.filter(P => P[1] < -.2) : hp;
      const solveAt = Aq => {
        sol = ikReach(H, Aq, SK.thigh, SK.shin, pole, prev['leg' + k]);
        const kv = times(sol.v, -1);
        thQ = segQ('th' + k, sub(sol.E, H), armFront(sub(sol.E, H), kv, fwd));
        shQ = segQ('sh' + k, sub(sol.W, sol.E), armFront(sub(sol.W, sol.E), kv, fwd));
        return minY(hpts, sol.E, shQ);
      };
      const low0 = solveAt(A);
      if (low0 < .002) {
        // raise the target by the depth (up to 4 steps), then bisect an overshoot back to 0.002-0.004: a raise also turns the
        // shin, so one step can leave an inclined planted shin hovering
        let lo = 0, hi = .003 - low0, lhi = solveAt(add(A, [0, hi, 0]));
        for (let it = 0; it < 3 && lhi < .002; it++) { lo = hi; hi += .003 - lhi; lhi = solveAt(add(A, [0, hi, 0])); }
        for (let it = 0; it < 8 && lhi > .004; it++) {
          const m = (lo + hi) / 2, lm = solveAt(add(A, [0, m, 0]));
          if (lm >= .002) { hi = m; lhi = lm; } else lo = m;
        }
        A = add(A, [0, hi, 0]);
        solveAt(A);
      }
      part('thigh_' + k, H, thQ); part('shin_' + k, sol.E, shQ);
      keep['leg' + k] = sol.v;
      legs[k] = {H, E: sol.E, W: sol.W, short: sol.short};
    }
    return need;
  };
  let needDrop = solveLegs();
  if (wLie > 0) {
    // lying: the legs ride the pelvis (their points in the pelvis frame, solved at the un-rocked frame); the incline / chin tip /
    // rock chosen on the grid (pass 1; pass 2 applies the plan); the root lift rests the lowest of pelvis / torso / head / legs
    // on the floor; the legs re-solved
    // the provisional legs solved high above the floor (no boot loop bends them), then carried as pelvis-frame points
    const R0 = R, Rhi = add(R, [0, 5, 0]);
    R = Rhi; ({Pq, Wst, Cq, Nb, Hq} = frame(R, lie, assist)); solveLegs(1);
    const iP = conj(Pq), legPts = [];
    for (const n of ['thigh_l', 'thigh_r', 'shin_l', 'shin_r']) for (const P of worldPoints(n, n, o[n])) legPts.push(rot(iP, sub(P, Rhi)));
    R = R0;
    if (!pass2) {
      const best = lieSearch(p, R, frame, prev.lie, legPts);
      lie = {incl: best.incl * wLie, tip: best.tip * wLie, rock: best.rock * wLie};
      keep.lie = best;
    }
    const F0 = frame(R, lie, assist);
    let low = Math.min(...[['pelvis', R, F0.Pq], ['torso', F0.Wst, F0.Cq], ['head', F0.Nb, F0.Hq]].map(([n, t, Q]) => minY(hullOf(n, n), t, Q)));
    for (const P of legPts) low = Math.min(low, R[1] + rot(F0.Pq, P)[1]);
    R = add(R, [0, (.002 - low) * wLie, 0]);
    ({Pq, Wst, Cq, Nb, Hq} = frame(R, lie, assist));
    needDrop = solveLegs();
  }
  GUARD.used.incl = lie.incl; GUARD.used.tip = lie.tip; setS('rock', lie.rock);
  if (wKnee > 0) {
    // the right knee on the floor: the root height where the lowest shin_r hull point near the knee is 0.002 (secant
    // iterations; the legs re-solved each time), blended in by wKnee
    const kneeLow = () => { const v = o.shin_r, M = qm(v.q); let low = Infinity;
      for (const P of hullOf('shin_r', 'shin_r')) if (P[1] >= -.08) low = Math.min(low, v.t[1] + M[1][0] * P[0] + M[1][1] * P[1] + M[1][2] * P[2]);
      return low; };
    const at = y => { R = [R[0], y, R[2]]; ({Pq, Wst, Cq, Nb, Hq} = frame(R, lie, assist)); needDrop = solveLegs(); return kneeLow() - .002; };
    const y0 = R[1];
    let a = y0, fa = kneeLow() - .002, b = Math.max(y0 - .12, Math.min(y0 + .25, y0 - fa)), fb = at(b);
    for (let it = 0; it < 8 && Math.abs(fb) > 5e-4; it++) {
      const c = Math.abs(fb - fa) > 1e-6 ? b - fb * (b - a) / (fb - fa) : b - fb;
      a = b; fa = fb; b = Math.max(y0 - .12, Math.min(y0 + .25, c)); fb = at(b);
    }
    if (wKnee < 1) at(y0 + (b - y0) * wKnee);
  }
  GUARD.used.drop = Math.min(GUARD_BOUND.drop, (drop + (needDrop > .003 ? needDrop : 0)) * 100);
  part('pelvis', R, Pq); part('torso', Wst, Cq); part('head', Nb, Hq); part('face', Nb, Hq);

  // ---- 5. the hip scabbard (closeY toward the left hand at the iai grip; the two-axis floor guard) ----
  const scHipT = add(R, rot(Pq, SK.scabHip));
  const sh0 = p.scHip || [0, 0];
  const hipQ = cy => mul(Pq, mul(q([sh0[0], sh0[1] + cy, 0]), bladeQ(SK.scabHipDir, [0, 1, 0])));
  let closeY = pls('closeY');
  let scHipQ = hipQ(closeY);
  const SL0 = () => add(Wst, rot(Cq, [SK.shoulder[0], SK.shoulder[1], SK.shoulder[2]]));
  if ((p.hiL || 0) >= .5 && (p.scab || 'hip') === 'hip') {
    // the hilt within the left arm's reach: the scabbard yaws about its mouth (the right hand at the throat turns it)
    const shortAt = cy => Math.max(0, len(sub(add(scHipT, rot(hipQ(cy), [0, SK.hilt, 0])), SL0())) - ARM_REACH);
    if (shortAt(closeY) > .005) {
      let best = closeY, bs = shortAt(closeY);
      for (const sg of [1, -1]) for (let a = 2; a < GUARD_BOUND.closeY; a += 2) { const c = closeY + sg * a; if (Math.abs(c) >= GUARD_BOUND.closeY) break; const s = shortAt(c); if (s < bs - 1e-4) { bs = s; best = c; } }
      closeY = best; scHipQ = hipQ(closeY);
    }
  }
  setS('closeY', closeY);
  const scHull = hullOf('scabbard', 'scabbard');
  scHipQ = clearFloor(scHipT, scHipQ, scHull, rot(Pq, [1, 0, 0]), .03, GUARD_BOUND.scab, 0, 'scab');
  if (minY(scHull, scHipT, scHipQ) < .03 - 1e-3 || pl('scabY')) scHipQ = clearFloor(scHipT, scHipQ, scHull, rot(Pq, [0, 1, 0]), .03, GUARD_BOUND.scabY, 0, 'scabY');
  let scT = null, scQ = null;
  const hiltOf = () => add(scT || scHipT, rot(scQ || scHipQ, [0, SK.hilt, 0]));
  const throatOf = () => add(scHipT, rot(scHipQ, [0, SK.throat, 0]));

  // ---- 6. the worn hat's frame (the brim targets of the hands) ----
  const hatWorn = () => ({t: add(Nb, rot(Hq, SK.brim)), q: mul(Hq, q([SK.brimTilt, 0, 0]))});
  const brimHold = (bz, side, hat = hatWorn()) => {
    const az = Math.max(SK.brimHold.azMin, Math.min(SK.brimHold.azMax, bz + SK.brimHold.azAdd));
    return add(add(hat.t, rot(hat.q, times(dirBE(-side * az, 0), SK.brimHold.r))), [0, SK.brimHold.dy, 0]);
  };

  // ---- 7. hand targets ----
  const shoulderOf = s => add(Wst, rot(Cq, [SK.shoulder[0] * s, SK.shoulder[1], SK.shoulder[2]]));
  let SL = shoulderOf(1), SR = shoulderOf(-1);
  const armDir = (a, side) => { const P = a[0] * D, B = a[1] * D * side, y = -Math.cos(P), z = -Math.sin(P); return [-y * Math.sin(B), y * Math.cos(B), z]; };
  const poleOf = (pp, s) => rot(Cq, pp ? [pp[0] * s, pp[1], pp[2]] : [s * .55, -.35, .75]);
  // the arm's shoulder -> hand direction turns at most ARM_TURN degrees per tick (world frame; a fast sweep of a short arm would
  // flip it in one tick: the hand lags a little, the sword grip follows the hand)
  const armSolve = (k, S, target, pole) => {
    const pd = prev['ad' + k], pl = prev['al' + k], d0 = sub(target, S);
    let L0 = len(d0);
    // ... and folds / unfolds at most ARM_FOLD b per tick (a kip-up swings the shoulder past a grip held in the yaw frame)
    if (pl !== undefined && L0 > 1e-6) { const L1 = Math.max(pl - ARM_FOLD, Math.min(pl + ARM_FOLD, Math.min(L0, ARM_REACH))); target = add(S, times(d0, L1 / L0)); L0 = L1; }
    if (pd && L0 > 1e-6) { const d = rateLimit(unit(sub(target, S)), pd, null, ARM_TURN); target = add(S, times(d, L0)); }
    let sol = ikReach(S, target, SK.armU, SK.fore, pole, prev['arm' + k]);
    // the upper arm too: a folding arm whose elbow would swing more than ARM_TURN degrees keeps its elbow on the previous side
    const pu = prev['ud' + k], ud = unit(sub(sol.E, S));
    if (pu && Math.acos(Math.max(-1, Math.min(1, dot(pu, ud)))) / D > ARM_TURN) {
      const alt = ikReach(S, target, SK.armU, SK.fore, pu, null), ua = unit(sub(alt.E, S));
      if (dot(pu, ua) > dot(pu, ud)) sol = alt;
    }
    keep['arm' + k] = sol.v; keep['ud' + k] = unit(sub(sol.E, S));
    keep['ad' + k] = unit(sub(sol.W, S)); keep['al' + k] = len(sub(sol.W, S));
    return sol;
  };
  const prevAx = n => (prev.ax && prev.ax[n]) || [0, -1, 0];
  const prevFl = () => hist(1)?.forearm_l?.q || ID;
  // the contact a hand reaches for this tick: {kind, T (target), w} (the strongest weight wins; recorded as a shortfall)
  const handTargets = side => {
    const k = side > 0 ? 'l' : 'r', S = side > 0 ? SL : SR, a = side > 0 ? p.aL : p.aR;
    let T = add(S, times(rot(Cq, armDir(a, side)), a[2] * (SK.armU + SK.fore)));
    const cts = [];
    const w = side > 0 ? (p.plwL || 0) : (p.plwR || 0), P = side > 0 ? p.plL : p.plR;
    if (w > 0 && P) {
      let PT = add(floorP, rot(Ryaw, P)), kind = 'floor';
      if (p.stone && p.stone[k]) { PT = stoneTarget(k, p.stone[k]); kind = 'stone'; }
      else if (p.kneelHat && side < 0) kind = 'hatfloor';
      T = lerp(T, PT, w);
      if (w >= FULL) cts.push({kind, T: PT, w});
    }
    const bw = side > 0 ? (p.bwL || 0) : (p.bwR || 0);
    if (bw > 0) { const bz = side > 0 ? (p.bzL ?? 35) : (p.bzR ?? 35), B = brimHold(bz, side); T = lerp(T, B, bw); if (bw >= FULL) cts.push({kind: 'brim', T: B, w: bw, az: Math.max(SK.brimHold.azMin, Math.min(SK.brimHold.azMax, bz + SK.brimHold.azAdd))}); }
    if (side > 0 && (p.hiL || 0) > 0) { const H = hiltOf(); T = lerp(T, H, p.hiL); if (p.hiL >= FULL) cts.push({kind: 'hilt', T: H, w: p.hiL}); }
    if (side < 0 && (p.hsR || 0) > 0) { const H = throatOf(); T = lerp(T, H, p.hsR); if (p.hsR >= FULL) cts.push({kind: 'throat', T: H, w: p.hsR}); }
    if (side < 0 && wLip > 0) { const M = add(Nb, rot(Hq, SK.lipMouth)), H = sub(M, times(prevAx('forearm_r'), CUP.hand)); T = lerp(T, H, wLip); if (wLip >= FULL) cts.push({kind: 'lips', T: H, w: wLip}); }
    if (side < 0 && p.hatX && p.hatX.hold) {
      // the hat hand-overs: the right hand to the hat's hold point (the pre-roll before a pickup, the put-on before a release)
      const hp = hatHoldPoint(p.hatX.hold);
      if (hp) { T = lerp(T, hp, p.hatX.hw); if (p.hatX.hw >= FULL) cts.push({kind: p.hatX.hold === 'world' ? 'hatfloor' : 'hat', T: hp, w: p.hatX.hw}); }
    }
    return {T, cts};
  };
  // the stone rule (seated; the kit's item spots, SUP): the bottle's neck in the left fist with its base on the spot, the cup's
  // base on its spot under the right fist (the frames of the previous tick); an empty hand stays at the item's hold point
  function stoneTarget(k, item) {
    if (k === 'l') {
      const bq = hist(1)?.bottle?.q || mul(prevFl(), q([p.botT || 0, 0, 0]));
      return add(rot(Ryaw, SUP.bottle), rot(bq, [0, BOTTLE.neck, 0]));
    }
    const cq = mul(Ryaw, q([p.cupT || 0, 0, 0]));
    return sub(add(rot(Ryaw, SUP.cup), rot(cq, [0, CUP.centre, 0])), times(prevAx('forearm_r'), CUP.hand));
  }
  // the hold point of a hat state (where the right hand takes / leaves the hat)
  const hatHoldPoint = st => {
    if (st === 'worn') return brimHold(p.bzR ?? 35, -1);
    if (st === 'back') {
      // the rim point of the back hat nearest her right shoulder (the top edge is out of a player-size arm's reach)
      const t = add(Wst, rot(Cq, add(SK.hatBack, [0, 0, pl('hatBackZ') / 100]))), d = rot(conj(Cq), sub(SR, t));
      const r = unit([d[0], d[1], 0]);
      return add(t, rot(Cq, times(r, HAT.R - .04)));
    }
    if (st === 'world' && p.hwS) { const c = p.hwS; return [c[0] - Math.sign(c[0]) * (HAT.R - .02), c[1] + HAT_FLOOR_HOLD, c[2]]; }
    return null;
  };

  // ---- 8. blade, arms ----
  const Cw = add(R, rot(Ryaw, SK.swing));
  let {G, SQ} = freeBlade(p, R, Ryaw, SL, Cw);
  const scab = p.scab || 'hip';
  const hold = (p.hold ?? 1) > .5;
  const shW = Math.max(0, Math.min(1, p.shW || 0));
  const sw = p.sword || 'hand';
  let solR, gripR, solL, gripL, tgtL = null, tgtR = null;
  const ctsL = [], ctsR = [];
  // planned blade corrections (pass 2+): the push of the grip (torso frame) and the turn of the blade about the grip
  const bp = plan.bPush, bt = plan.bTurn;
  const swordFree = sw === 'hand' && shW < .5 && hold;
  if (swordFree && bp && bp.v > 0) G = add(G, times(rot(Cq, bp.dir), bp.v / 100));
  if (swordFree && bt && bt.v > 0) SQ = mul(qa(unit(rot(Cq, bt.dir)), bt.v), SQ);
  const solveRight = (extra = [0, 0, 0]) => {
    const {T, cts} = handTargets(-1);
    ctsR.length = 0; ctsR.push(...cts);
    if (scab === 'hand') {
      const d = rot(Ryaw, dirBE(p.scB ?? 0, p.scE ?? 80));
      tgtR = add(T, extra);
      solR = armSolve('r', SR, tgtR, poleOf(p.pR, -1));
      gripR = solR.W;
      scQ = mul(qa(unit(d), p.scR || 0), bladeQ(d, rot(Ryaw, [0, 0, -1])));
      scT = sub(gripR, times(unit(d), p.scOff || 0));
      // the hand-held scabbard's floor guard: turned up about the fist (the smallest turn, either sense) to clear 0.03
      ({scT, scQ} = scabHandFloor(gripR, scT, scQ));
    } else {
      const rh = hold ? Math.max(0, Math.min(1, p.rh || 0)) : 0;
      const sy = rot(SQ, [0, 1, 0]);
      tgtR = add(lerp(T, add(G, times(sy, -SK.twoHand)), rh), extra);
      if (rh >= FULL) ctsR.push({kind: 'twohand', T: tgtR, w: rh});
      solR = armSolve('r', SR, tgtR, poleOf(p.pR, -1));
      gripR = solR.W;
    }
  };
  function scabHandFloor(g, t, Q) {
    const hull = hullOf('scabbard', 'scabbard'), rel = rot(conj(Q), sub(t, g));
    const lowAt = (ax, a) => { const Qa = mul(qa(ax, a), Q); return g[1] + Math.min(...hull.map(P => rot(Qa, add(rel, P))[1])); };
    const d = rot(Q, [0, 1, 0]), ax = safeAxis(cross(d, [0, 1, 0]));
    const a0 = Math.min(GUARD.min.scabH || 0, GUARD_BOUND.scabH - 1);
    let best = null;
    for (const sg of [1, -1]) {
      const axS = times(ax, sg);
      for (let a = a0; a < GUARD_BOUND.scabH; a += (a < a0 + 1e-9 && a0 > 0 ? 1 : 2)) if (lowAt(axS, a) >= .03) { if (!best || a < best.a) best = {a, ax: axS}; break; }
    }
    if (!best) { if (lowAt(ax, 0) < .03) GUARD.used.scabH = GUARD_BOUND.scabH; return {scT: t, scQ: Q}; }
    if (best.a > 0) GUARD.used.scabH = Math.max(GUARD.used.scabH || 0, best.a);
    const Qa = mul(qa(best.ax, best.a), Q);
    return {scT: add(g, rot(Qa, rel)), scQ: Qa};
  }
  let sheathe = null;
  const solveLeft = () => {
    if (shW > 0) {
      const sT = scT || scHipT, sQ = scQ || scHipQ;
      const ax = rot(sQ, [0, 1, 0]), back = times(ax, -1);
      const depth = (p.sh || 0) * (SWORD.tip - SWORD.guard);
      const Gsh = add(sT, times(back, SWORD.tip - depth));
      // on the scabbard's axis the blade takes the scabbard's edge frame (S2d: independent of the free blade, so SH0' = the
      // on-axis pose exactly and the draw / sheathe blends turn the blade at most shW of the way)
      const edgeQ = bladeQ(ax, rot(sQ, [0, 0, -1]));
      if (!sheathe) sheathe = {G0: G, SQ0: SQ};
      G = lerp(sheathe.G0, Gsh, shW); SQ = slerp(sheathe.SQ0, edgeQ, shW);
    }
    ctsL.length = 0;
    if (hold) {
      tgtL = G;
      solL = armSolve('l', SL, G, poleOf(p.pL, 1));
      gripL = solL.W;
      if (shW >= FULL) ctsL.push({kind: 'sheathe', T: G, w: shW});
      // the grip follows the hand where the arm falls short (through a draw / sheathe blend too: only the blade fully on the
      // scabbard's axis stays there)
      if (len(sub(gripL, G)) > .002 && shW < .999) G = gripL;
    } else {
      const {T, cts} = handTargets(1);
      ctsL.push(...cts);
      tgtL = T;
      solL = armSolve('l', SL, T, poleOf(p.pL, 1));
      gripL = solL.W;
    }
  };
  solveRight();
  if (!scT) { scT = scHipT; scQ = scHipQ; }
  solveLeft();
  // the prop closure: the left hand short of a point on the hand-held scabbard (the hilt, the sheathe) -> the right hand (the
  // scabbard) comes toward it by the shortfall (planned: guard close, a vector in the yaw frame)
  // (a mostly drawn blade, shW < 0.5, is the free blade's: no closure)
  const leftOnScab = scab === 'hand' && (((p.hiL || 0) >= .5 && !hold) || (hold && shW >= .5));
  {
    const cp = plan.close;
    let extra = cp && cp.v > 0 ? rot(Ryaw, times(cp.dir, cp.v / 100)) : [0, 0, 0];
    if (len(extra) > 0) { solveRight(extra); sheathe = null; solveLeft(); }
    let total = extra;
    if (leftOnScab) {
      for (let it = 0; it < 3; it++) {
        // the scabbard (with the left hand's target on it) comes toward the left hand by the shortfall
        const sh = sub(tgtL, gripL);
        if (len(sh) < .005) break;
        total = sub(total, sh);
        if (len(total) > GUARD_BOUND.close / 100) total = times(total, GUARD_BOUND.close / 100 / len(total));
        solveRight(total); sheathe = null; solveLeft();
      }
    }
    if (len(total) > 1e-6) GUARD.used.close = {v: len(total) * 100, dir: rot(conj(Ryaw), unit(total))};
  }

  // ---- 9. reach assists: a contact still short by > 0.01 turns the torso (and the head for the brim) toward it ----
  // (a sheathe into the hip scabbard counts: its point rides the pelvis, a torso turn brings the left shoulder to it; the
  // hand-held scabbard comes to the left hand by the closure instead)
  const allCts = () => [...ctsL.map(c => ({...c, side: 1})), ...ctsR.map(c => ({...c, side: -1}))]
    .filter(c => c.kind !== 'twohand' && (c.kind !== 'sheathe' || scab === 'hip'));
  {
    const cts = allCts();
    const shortOf = (F, c) => {
      const S = add(F.Wst, rot(F.Cq, [SK.shoulder[0] * c.side, SK.shoulder[1], SK.shoulder[2]]));
      let T = c.T;
      if (c.kind === 'brim') { const ht = {t: add(F.Nb, rot(F.Hq, SK.brim)), q: mul(F.Hq, q([SK.brimTilt, 0, 0]))}; T = brimHold(c.side > 0 ? (p.bzL ?? 35) : (p.bzR ?? 35), c.side, ht); }
      else if (c.kind === 'lips') T = sub(add(F.Nb, rot(F.Hq, SK.lipMouth)), times(prevAx('forearm_r'), CUP.hand));
      return Math.max(0, len(sub(T, S)) - ARM_REACH);
    };
    const worst = as => Math.max(0, ...cts.map(c => shortOf(frame(R, lie, as), c)));
    const s0 = worst(assist);
    if (cts.length && s0 > .01) {
      const brim = cts.some(c => c.kind === 'brim');
      let best = {...assist}, bv = s0, bc = 0;
      const cost = as => Math.abs(as.y - assist.y) + Math.abs(as.p - assist.p) + Math.abs(as.r - assist.r) + Math.abs(as.hr - assist.hr);
      const tryA = as => { const v = worst(as), c = cost(as); if (v < bv - 1e-4 || (Math.abs(v - bv) < 1e-4 && c < bc)) { bv = v; best = as; bc = c; } };
      if (brim) {
        const side = cts.find(c => c.kind === 'brim').side;
        for (let h = 0; h < GUARD_BOUND.aHeadR; h += 1) for (let r = -GUARD_BOUND.aTorR + 2; r <= GUARD_BOUND.aTorR - 2; r += 2) {
          const as = {...assist, hr: assist.hr - side * h, r: assist.r + r};
          if (Math.abs(as.hr) >= GUARD_BOUND.aHeadR || Math.abs(as.r) >= GUARD_BOUND.aTorR) continue;
          const v = worst(as), c = cost(as);
          if ((v <= .01 && (bv > .01 || c < bc)) || (bv > .01 && v < bv - 1e-4)) { bv = v; best = as; bc = c; }
        }
      } else {
        for (let y = -GUARD_BOUND.aTorY + 1; y <= GUARD_BOUND.aTorY - 1; y += 2) for (let pp = -GUARD_BOUND.aTorP + 1; pp <= GUARD_BOUND.aTorP - 1; pp += 2)
          for (let r = -GUARD_BOUND.aTorR + 2; r <= GUARD_BOUND.aTorR - 2; r += 2) {
            const as = {y: assist.y + y, p: assist.p + pp, r: assist.r + r, hr: assist.hr};
            if (Math.abs(as.y) >= GUARD_BOUND.aTorY || Math.abs(as.p) >= GUARD_BOUND.aTorP || Math.abs(as.r) >= GUARD_BOUND.aTorR) continue;
            // the smallest turn that brings the contact within 0.01 (else the one that helps most)
            const v = worst(as), c = cost(as);
            if ((v <= .01 && (bv > .01 || c < bc)) || (bv > .01 && v < bv - 1e-4)) { bv = v; best = as; bc = c; }
          }
      }
      if (cost(best) > 0) {
        Object.assign(assist, best);
        ({Pq, Wst, Cq, Nb, Hq} = frame(R, lie, assist));
        part('torso', Wst, Cq); part('head', Nb, Hq); part('face', Nb, Hq);
        SL = shoulderOf(1); SR = shoulderOf(-1);
        sheathe = null;
        ({G, SQ} = freeBlade(p, R, Ryaw, SL, Cw));
        if (swordFree && bp && bp.v > 0) G = add(G, times(rot(Cq, bp.dir), bp.v / 100));
        if (swordFree && bt && bt.v > 0) SQ = mul(qa(unit(rot(Cq, bt.dir)), bt.v), SQ);
        scT = null; scQ = null;
        const cl = GUARD.used.close ? rot(Ryaw, times(GUARD.used.close.dir, GUARD.used.close.v / 100)) : [0, 0, 0];
        solveRight(cl);
        if (!scT) { scT = scHipT; scQ = scHipQ; }
        solveLeft();
      }
    }
    setS('aTorY', assist.y); setS('aTorP', assist.p); setS('aTorR', assist.r); setS('aHeadR', assist.hr);
  }
  // ---- 10. the blade-body guard (sword in hand): push the grip out of her body, then turn the blade; then groundSword ----
  const armSegs = () => {
    for (const [k, S, sol] of [['l', SL, solL], ['r', SR, solR]]) {
      const up = sub(sol.E, S), fo = sub(sol.W, sol.E);
      part('arm_' + k, S, segQ('ua' + k, up, armFront(up, sol.v, chestFwd())));
      part('forearm_' + k, sol.E, segQ('fa' + k, fo, armFront(fo, sol.v, chestFwd())));
    }
  };
  armSegs();
  // the stone rule with this tick's forearms: the targets above used the previous tick's frames; the refinements put the
  // bottle's base / the cup's base on its spot (the item swaps in or out of the hand there; a relaxed fixed point, <= 8
  // rounds: the forearm turns with the target, the plain iteration oscillates)
  if (p.stone) for (let it = 0; it < 8; it++) {
    const cL = ctsL.find(c => c.kind === 'stone'), cR = ctsR.find(c => c.kind === 'stone');
    if (!cL && !cR) break;
    let err = 0;
    if (cL) {
      const bq = mul(o.forearm_l.q, q([p.botT || 0, 0, 0])), spot = rot(Ryaw, SUP.bottle);
      err = Math.max(err, len(sub(sub(gripL, rot(bq, [0, BOTTLE.neck, 0])), spot)));
      cL.T = lerp(cL.T, add(spot, rot(bq, [0, BOTTLE.neck, 0])), .55); tgtL = cL.T;
      solL = armSolve('l', SL, cL.T, poleOf(p.pL, 1)); gripL = solL.W;
    }
    if (cR) {
      const cq = mul(Ryaw, q([p.cupT || 0, 0, 0])), axR = rot(o.forearm_r.q, [0, -1, 0]), spot = add(rot(Ryaw, SUP.cup), rot(cq, [0, CUP.centre, 0]));
      err = Math.max(err, len(sub(add(gripR, times(axR, CUP.hand)), spot)));
      cR.T = lerp(cR.T, sub(spot, times(axR, CUP.hand)), .55); tgtR = cR.T;
      solR = armSolve('r', SR, cR.T, poleOf(p.pR, -1)); gripR = solR.W;
    }
    armSegs();
    if (err < .004) break;
  }
  const bladeDeep = (Gx, SQx, margin = .02, parts = BLADE_BODY) => {
    const ax = rot(SQx, [0, 1, 0]); let best = null;
    for (const n of parts) {
      const v = o[n]; if (!v) continue;
      const [lo, hi] = BOX[n], iq = conj(v.q);
      for (let k = 0; k <= 24; k++) {
        const y = SWORD.bladeLo + (SWORD.tip - SWORD.bladeLo) * k / 24, P = add(Gx, times(ax, y));
        const L = rot(iq, sub(P, v.t));
        let dm = Infinity, ai = 0, sg = 1;
        for (let i = 0; i < 3; i++) { const a = L[i] - lo[i], b = hi[i] - L[i]; if (a < dm) { dm = a; ai = i; sg = -1; } if (b < dm) { dm = b; ai = i; sg = 1; } }
        if (dm > -margin && (!best || dm > best.d)) { const e = [0, 0, 0]; e[ai] = sg; best = {d: dm, n: rot(v.q, e), part: n, y}; }
      }
    }
    return best;
  };
  const swordClear = .10 + (.03 - .10) * wLie;
  let pushV = bp && swordFree && bp.v > 0 ? times(rot(Cq, bp.dir), bp.v / 100) : [0, 0, 0];
  let turnA = bt && swordFree && bt.v > 0 ? bt.v : 0, turnAx = bt && bt.v > 0 ? rot(Cq, bt.dir) : null;
  // the guard also runs through a draw / sheathe blend (the blade between the free pose and the scabbard's axis can sweep
  // through her head: intro_end's overhead draw); only the blade fully on the axis (shW 1) is left alone
  if (sw === 'hand' && hold && shW < .999) {
    for (let it = 0; it < 6; it++) {
      const b = bladeDeep(G, SQ); if (!b) break;
      const ax = rot(SQ, [0, 1, 0]);
      let push = perp(b.n, ax); push = len(push) < .2 ? b.n : unit(push);
      let step = times(push, b.d + .02 + .005);
      const room = (GUARD_BOUND.bPush - 1) / 100 - len(pushV);
      if (room < .005) break;
      if (len(step) > room) step = times(push, room);
      // the grip moves only as far as the sword arm takes it along the push (else stage 2 turns the blade)
      const G0 = G, sol = armSolve('l', SL, add(G, step), poleOf(p.pL, 1));
      const moved = dot(sub(sol.W, G0), push);
      if (moved < .5 * len(step)) { armSolve('l', SL, G0, poleOf(p.pL, 1)); break; }
      solL = sol; gripL = sol.W; G = gripL;
      pushV = add(pushV, sub(G, G0));
      if ((p.rh || 0) >= .5 && scab !== 'hand') solveRight();
      armSegs();
    }
    // stage 2: still inside -> turn the blade about the grip away from the body by the smallest angle (6-degree steps; about
    // the axis across the blade and the push normal, then about the normal), preferring a turn that also keeps the blade off
    // the floor (groundSword's clearance)
    let b = bladeDeep(G, SQ);
    if (b) {
      const ax = rot(SQ, [0, 1, 0]), pts = hullOf('sword', 'sword');
      const offFloor = Qx => G[1] + Math.min(...pts.map(P => rot(Qx, P)[1])) >= swordClear - 1e-3;
      let best = null;
      for (const pass of [0, 1]) {
        for (const axis of [safeAxis(cross(ax, b.n)), safeAxis(perp(b.n, ax))]) for (const sg of [1, -1]) {
          for (let a = 6; a < GUARD_BOUND.bTurn - turnA; a += 6) {
            if (best && a >= best.a) break;
            const Q2 = mul(qa(times(axis, sg), a), SQ);
            if (!bladeDeep(G, Q2) && (pass || offFloor(Q2))) { best = {a, Q2, axis: times(axis, sg)}; break; }
          }
        }
        if (best) break;
      }
      if (best) { SQ = best.Q2; turnA += best.a; turnAx = best.axis; }
    }
  }
  if (len(pushV) > 1e-5) GUARD.used.bPush = {v: len(pushV) * 100, dir: rot(conj(Cq), unit(pushV))};
  if (turnA > 0 && turnAx) GUARD.used.bTurn = {v: turnA, dir: rot(conj(Cq), unit(turnAx))};
  if (sw === 'hand' && shW < .999) SQ = groundSword(G, SQ, rot(Ryaw, [0, 0, -1]), swordClear);
  const bladeResidue = sw === 'hand' && shW < .999 && hold ? (bladeDeep(G, SQ, 0)?.d || 0) : 0;

  // ---- limb floor guard: an arm whose hull dips below 0.002 raises its target by the deficit ----
  const armLow = k => Math.min(minY(hullOf('arm_' + k, 'arm_' + k), o['arm_' + k].t, o['arm_' + k].q), minY(hullOf(k === 'l' ? HAND_MODELS.forearm_l[p.hL || 'grip'] : HAND_MODELS.forearm_r[p.hR || 'open'], 'forearm_' + k), o['forearm_' + k].t, o['forearm_' + k].q));
  for (const k of ['l', 'r']) {
    for (let it = 0; it < 3; it++) {
      const low = armLow(k);
      if (low >= .002 - 1e-4) break;
      const dy = [0, .002 - low + .001, 0];
      if (k === 'l') {
        if (hold) { G = add(G, dy); }
        tgtL = add(tgtL, dy);
        solL = armSolve('l', SL, tgtL, poleOf(p.pL, 1)); gripL = solL.W;
        if (hold && shW < .999) G = gripL;
      } else {
        tgtR = add(tgtR, dy);
        solR = armSolve('r', SR, tgtR, poleOf(p.pR, -1)); gripR = solR.W;
        if (scab === 'hand') { const d = rot(Ryaw, dirBE(p.scB ?? 0, p.scE ?? 80)); scT = sub(gripR, times(unit(d), p.scOff || 0)); }
      }
      armSegs();
    }
  }
  stretch.arm = Math.max(solL.stretch || 1, solR.stretch || 1);

  // ---- 11. sword, glow, scabbard, sheathed hilt ----
  const swS = sw === 'hand' ? 1 : 0;
  part('sword', G, SQ, swS); part('sword_glow', G, SQ, swS);
  const scS = scab === 'gone' ? 0 : 1;
  part('scabbard', scT, scQ, scS);
  part('hilt_sheathed', scT, scQ, sw === 'sheathed' && scab !== 'gone' ? 1 : 0);

  // ---- 12. hat (worn / back / hand / world / gone; the hand-overs) and its strings ----
  const hat = p.hat || 'worn';
  const hatState = st => {
    if (st === 'worn' || st === 'gone') return hatWorn();
    if (st === 'back') {
      let z = pl('hatBackZ') / 100;
      // the head clearance: the brim disc (torso frame) behind every head point within its circle by 0.02
      const hp = hullOf('head', 'head'), M = qm(mul(conj(Cq), Hq)), nb = rot(conj(Cq), sub(Nb, Wst)), c = SK.hatBack;
      let need = 0;
      const pts = [...hp];
      const [lo, hi] = BOX.head_layer;
      for (let i = 0; i <= 4; i++) for (let j = 0; j <= 4; j++) pts.push([lo[0] + (hi[0] - lo[0]) * i / 4, lo[1] + (hi[1] - lo[1]) * j / 4, hi[2]]);
      for (const P of pts) {
        const x = nb[0] + M[0][0] * P[0] + M[0][1] * P[1] + M[0][2] * P[2], y = nb[1] + M[1][0] * P[0] + M[1][1] * P[1] + M[1][2] * P[2], zz = nb[2] + M[2][0] * P[0] + M[2][1] * P[1] + M[2][2] * P[2];
        if (x * x + (y - c[1]) ** 2 <= (HAT.R + .02) ** 2) need = Math.max(need, zz + .02 - (c[2] + z));
      }
      if (need > 0) z = Math.min(GUARD_BOUND.hatBackZ / 100, z + need);
      GUARD.used.hatBackZ = z * 100;
      return {t: add(Wst, rot(Cq, add(SK.hatBack, [0, 0, z]))), q: mul(Cq, q([90, 0, 0]))};
    }
    if (st === 'hand') {
      const D1 = unit(rot(Ryaw, dirBE(p.hhB ?? -90, p.hhE ?? 0))), N1 = unit(rot(Ryaw, dirBE(...(p.hhN || [-90, 0]))));
      let Nn = perp(N1, D1); if (len(Nn) < 1e-3) Nn = perp([0, 1, 0], D1);
      return {t: add(gripR, times(D1, SK.hatHand)), q: basisQ(cross(unit(Nn), unit(times(D1, -1))), unit(Nn), unit(times(D1, -1)))};
    }
    // world: a rest spot (hwS) or a re-anchored flight (hwF: {t, q})
    if (p.hwF) return {t: [...p.hwF.t], q: p.hwF.q};
    return {t: [...(p.hwS || [1, .02, -.35])], q: p.hwSq || mul(Ryaw, q(p.hwE || [0, 0, 0]))};
  };
  let H = hatState(hat), hS = hat === 'gone' ? 0 : 1;
  const hatHull = hullOf('hat_p1', 'hat');
  // the state itself clears the floor (a turn about the horizontal axis under its up axis); a hand-over blend then only lifts
  if (hS && hat !== 'world') H = {t: H.t, q: clearFloor(H.t, H.q, hatHull, safeAxis(cross(rot(H.q, [0, 1, 0]), [0, 1, 0])), .02, GUARD_BOUND.hat, 0, 'hat')};
  if (p.hatX && hat !== 'gone') {
    // the hand-overs: put-on / swing (hatX.to: before the switch the hat blends toward the destination state, on a line or
    // over the back of her head) and pickup (hatX.from: after the switch it blends from the solved hat of the tick before
    // the switch, k ticks back, into the new state)
    const X = p.hatX;
    if (X.to && X.to.bw > 0) {
      const other = hatState(X.to.dest);
      H = X.to.path === 'arc' ? arcBlend(H, other, X.to.bw, Nb, Cq) : {t: lerp(H.t, other.t, X.to.bw), q: slerp(H.q, other.q, X.to.bw)};
    }
    const prevH = X.from && X.from.bw < 1 ? hist(X.from.k)?.hat : null;
    let floor = .002;
    if (prevH && prevH.s[0] > 0) {
      H = {t: lerp(prevH.t, H.t, X.from.bw), q: slerp(prevH.q, H.q, X.from.bw)};
      floor = Math.min(floor, minY(hatHull, prevH.t, prevH.q, 1));   // a pickup off the floor starts where the hat lay
    }
    const lo = minY(hatHull, H.t, H.q, 1);
    if (lo < floor) H = {t: add(H.t, [0, floor - lo, 0]), q: H.q};
  }
  const hT = H.t, hQ = H.q;
  part('hat', hT, hQ, hS);
  {
    const pq = hist(2)?._hatQ || hQ;
    let sq = slerp(hQ, pq, .5), st = hT;
    if (hat === 'world') { sq = mul(hQ, q([90, 0, 0])); st = add(hT, rot(hQ, [0, .015, 0])); }   // lying over the brim
    else {
      const down = rot(sq, [0, -1, 0]);
      sq = mul(slerp(ID, fromTo(down, [0, -1, 0]), .45 * gfade(down)), sq);
      if (hS) sq = clearFloor(hT, sq, hullOf('hat_strings', 'hat_strings'), safeAxis(rot(sq, [1, 0, 0])), .02, GUARD_BOUND.strings, 0, 'strings');
    }
    part('hat_strings', st, sq, hS);
    Object.defineProperty(o, '_hatQ', {value: hQ, enumerable: false});
  }

  // ---- 13. sash tails (from the knot at her left hip; hang with gravity, lag 3 t); the cup and the bottle ----
  {
    const kt = add(R, rot(Pq, SK.sashKnot));
    const lagK = hist(3)?._sashKnot;
    const outw = rot(Pq, unit([SK.sashKnot[0], 0, SK.sashKnot[2]]));
    let dir = unit(add(add([0, -1, 0], times(rot(Pq, [0, -1, 0]), .35)), times(outw, .34 * (p.skF ?? 1))));
    if (lagK) dir = unit(add(dir, times(sub(lagK, kt), 2.2)));
    dir = rateLimit(dir, prev.sashD, prev.Pq ? mul(Pq, conj(prev.Pq)) : null, 45);
    keep.sashD = dir; keep.Pq = Pq;
    const F = steadyPerp(rot(Pq, [0, 0, -1]), dir, prev.sash, rot(Pq, [0, 0, -1]));
    keep.sash = F;
    let sq = aimQ(dir, F);
    sq = clearFloor(kt, sq, hullOf('sash_p1', 'sash_tails'), safeAxis(cross(dir, [0, 1, 0])), .03, GUARD_BOUND.sash, 0, 'sash');
    part('sash_tails', kt, sq);
    Object.defineProperty(o, '_sashKnot', {value: kt, enumerable: false});
  }
  {
    const cup = p.cup || 'none', bot = p.bottle || 'none';
    const cupQ = mul(Ryaw, q([p.cupT || 0, 0, 0]));
    const axR = rot(o.forearm_r.q, [0, -1, 0]);
    const cupBase = add(add(gripR, times(axR, CUP.hand)), rot(cupQ, [0, -CUP.centre, 0]));
    if (cup === 'hand') part('cup', cupBase, cupQ);
    else part('cup', cupBase, cupQ, 0);
    // the bottle held by the neck: its neck point (BOTTLE.neck above the base) in the left fist, tilted about it (botT)
    const fl = o.forearm_l.q;
    const botQ = mul(fl, q([p.botT || 0, 0, 0]));
    const botBase = sub(gripL, rot(botQ, [0, BOTTLE.neck, 0]));
    if (bot === 'hand') part('bottle', botBase, botQ);
    else part('bottle', botBase, botQ, 0);
    keep.ax = {forearm_r: axR, forearm_l: rot(fl, [0, -1, 0])};
  }

  // ---- 14. support: the generic floor rule (S2a's contact truth, refCore), then S2c's lift-only rule ----
  const lowOf = names => { let m = Infinity; for (const n of names) { const v = o[n]; if (!v || v.s[0] < 1e-4) continue; m = Math.min(m, minY(hullOf(modelOn(n, p), n), v.t, v.q)); } return m; };
  // weight (1 - wSeat): the seat holds her on the stone; a lying / kneeling root does not stop the rule. Touched (S2a's
  // lowest < 0.012): the lowest core point to 0.002 (it finishes a partial lying / kneeling root; may be negative: no float);
  // airborne (>= 0.05): at least min(S_LEG x S2a's height, 0.12) up, never pulled down (a kip off its lying root stays up)
  const wRoot = Math.max(wSeat, wLie, wKnee);
  let dy = 0;
  const lowRef = ctx.ref ? ctx.ref.low : null;
  const coreLow = lowOf(CORE);
  if (lowRef !== null && (p.vis ?? 1) >= .999 && wSeat < 1) {
    const touch = .002 - coreLow, air = Math.max(0, Math.min(SLEG * lowRef, .12) - coreLow);
    const wa = Math.max(0, Math.min(1, (lowRef - .012) / (.05 - .012)));
    dy = ((1 - wa) * touch + wa * air) * (1 - wSeat);
  }
  const moveAll = d => { if (d) for (const [n, v] of Object.entries(o)) if (!(n === 'hat' && hat === 'world')) v.t = add(v.t, [0, d, 0]); };
  moveAll(dy);
  // planted feet stay planted: when the touch rule lifted her (a crouch's knee-end corner was the lowest point), a planted
  // foot left hovering is re-planted (that leg re-solved to its floor target from the raised hip joint)
  if (dy > .004) {
    const hov = [['l', p.fL], ['r', p.fR]].filter(([k, F]) => lf < .5 && F[1] <= .0066 && wSeat < .5 && wKnee < .5
      && minY(hullOf('shin_' + k, 'shin_' + k), o['shin_' + k].t, o['shin_' + k].q) > .006).map(([k]) => k);
    if (hov.length) { const R0 = R; R = add(R, [0, dy, 0]); solveLegs(lf, hov); R = R0; }
  }
  let low = lowOf(hat === 'worn' || hat === 'back' ? [...LIFT_PARTS, 'hat'] : LIFT_PARTS);
  const lift = low < .002 ? .002 - low : 0;
  moveAll(lift);
  // a flying world hat (hwF) clears her body (guard hatPush, a vector in the rig frame, planned): out of every body box,
  // away from her body's axis (pelvis -> head centre); the 1.32-b brim leaves from her back as she falls (repel)
  if (hat === 'world' && p.hwF) {
    const hp = hatVisPts(), hpv = plan.hatPush;
    let push = hpv && hpv.v > 0 ? times(hpv.dir, hpv.v / 100) : [0, 0, 0];
    const deepest = T => {
      let w = -1;
      for (const n of HAT_CLEAR) {
        const v = o[n]; if (!v || v.s[0] < 1e-4) continue;
        const [lo, hi] = BOX[n], iq = conj(v.q);
        for (const P0 of hp) {
          const L = rot(iq, sub(add(T, rot(o.hat.q, P0)), v.t));
          w = Math.max(w, Math.min(L[0] - lo[0], hi[0] - L[0], L[1] - lo[1], hi[1] - L[1], L[2] - lo[2], hi[2] - L[2]));
        }
      }
      return w;
    };
    const axisPt = T => {
      const a = o.pelvis.t, ab = sub(add(o.head.t, rot(o.head.q, [0, .25, 0])), a);
      return add(a, times(ab, Math.max(0, Math.min(1, dot(sub(T, a), ab) / Math.max(1e-9, dot(ab, ab))))));
    };
    let T = add(o.hat.t, push);
    // (2 cm clear: the display's interpolation between keys must not bring the brim back in)
    for (let it = 0; it < 8; it++) {
      const d = deepest(T); if (d <= -.02) break;
      const step = times(safeAxis(sub(T, axisPt(T))), d + .035);
      T = add(T, step); push = add(push, step);
    }
    const mv = sub(T, o.hat.t);
    o.hat.t = T; o.hat_strings.t = add(o.hat_strings.t, mv);
    if (len(push) > 1e-5) GUARD.used.hatPush = {v: Math.min(GUARD_BOUND.hatPush, len(push) * 100), dir: unit(push)};
  }
  // visibility about the body centre
  if ((p.vis ?? 1) !== 1) {
    const c = add(R, [0, SK.vis + dy + lift, 0]);
    for (const v of Object.values(o)) { v.t = add(c, times(sub(v.t, c), p.vis)); v.s = times(v.s, p.vis); }
  }
  // the parts the skin already shows (HIDDEN: the hair, the side locks, the skirt panels) rest at scale 0 in one fixed
  // transform, so a clip keys them once at its tick 0
  for (const n of HIDDEN) o[n] = {t: [0, HIP_Y, 0], q: [0, 0, 0, 1], s: [0, 0, 0]};
  // the contacts: the grip's distance to its target after the moves (world targets stay; body targets moved with her)
  const ctsList = [];
  {
    const mv = dy + lift, WORLD = new Set(['stone', 'floor', 'hatfloor']);
    for (const [cts, g, side] of [[ctsL, gripL, 1], [ctsR, gripR, -1]]) for (const c of cts) {
      const T = WORLD.has(c.kind) ? c.T : add(c.T, [0, mv, 0]), d = len(sub(add(g, [0, mv, 0]), T));
      contacts[c.kind] = Math.max(contacts[c.kind] || 0, d);
      ctsList.push({kind: c.kind, side, d, T, ...(c.az !== undefined ? {az: c.az} : {})});
    }
  }
  // anchors (rig frame, after the support moves): the grips, the blade tip / middle (the left hand while the sword is hidden),
  // the scabbard's mouth, the crown top, the head centre, the chest
  const up = [0, dy + lift, 0];
  const swOn = o.sword.s[0] > 1e-4;
  const gW = o.sword.t, ax = rot(o.sword.q, [0, 1, 0]);
  const anchors = {
    hand_l: add(gripL, up), hand_r: add(gripR, up),
    blade_tip: swOn ? add(gW, times(ax, SWORD.tip)) : add(gripL, up),
    blade_mid: swOn ? add(gW, times(ax, (SWORD.bladeLo + SWORD.tip) / 2)) : add(gripL, up),
    scabbard_mouth: o.scabbard.t, hat_crown: add(o.hat.t, rot(o.hat.q, [0, HAT.crownH + .02, 0])),
    head: add(o.head.t, rot(o.head.q, SK.anchors.head)), chest: add(o.torso.t, rot(o.torso.q, SK.anchors.chest)),
  };
  Object.defineProperty(o, '_anchors', {value: anchors, enumerable: false});
  keep.gs = {...GUARD.prefer, ...GUARD.sense};
  Object.defineProperty(o, '_prev', {value: keep, enumerable: false});
  Object.defineProperty(o, '_lift', {value: lift, enumerable: false});
  Object.defineProperty(o, '_guard', {value: GUARD.used, enumerable: false});
  Object.defineProperty(o, '_contacts', {value: contacts, enumerable: false});
  Object.defineProperty(o, '_stretch', {value: stretch, enumerable: false});
  Object.defineProperty(o, '_support', {value: {dy, lift, coreLow: coreLow + dy + lift, lowRef, wRoot, bladeResidue, grips: {l: add(gripL, up), r: add(gripR, up)},
    targets: {l: tgtL && add(tgtL, up), r: tgtR && add(tgtR, up)}, lie, assist: {...assist}, closeY, cts: ctsList}, enumerable: false});
  return o;
}
// the lying rest: the torso incline toward her front, the chin tip and a rock of the whole figure about the pelvis that
// minimise the largest of the pelvis / torso / head gaps once the lowest of them (and the legs) rests on the floor; 1-degree
// grid, a small preference for small turns and for the previous tick's solution (no flip-flop)
// the kit's seat stone (rig frame, her yaw; request s2d-2) and its item spots: the bottle at her left, the cup at her right
export const SUP = {T: .24, front: -.135, back: .505, half: .6, bottle: [.42, .24, .15], cup: [-.42, .24, .15]};
const SLEG = .765625 / 1.18;
function lieSearch(p, R, frame, prevBest, legPts) {
  let best = null;
  const zero = {y: 0, p: 0, r: 0, hr: 0};
  // the grid stops one degree inside every bound (a planned value at its bound is a build error)
  for (let rock = -GUARD_BOUND.rock + 1; rock <= GUARD_BOUND.rock - 1; rock++) {
    let legLow = Infinity;
    const F0 = frame(R, {incl: 0, tip: 0, rock}, zero);
    for (const P of legPts) legLow = Math.min(legLow, R[1] + rot(F0.Pq, P)[1]);
    const pel = minY(hullOf('pelvis', 'pelvis'), R, F0.Pq);
    for (let incl = 0; incl < GUARD_BOUND.incl; incl++) for (let tip = 0; tip < GUARD_BOUND.tip; tip++) {
      const F = frame(R, {incl, tip, rock}, zero);
      const lows = [pel, minY(hullOf('torso', 'torso'), F.Wst, F.Cq), minY(hullOf('head', 'head'), F.Nb, F.Hq)];
      const low = Math.min(...lows, legLow);
      // gaps up to 0.035 are free (the design's prototypes: 0.01-0.035); beyond, the largest gap dominates; then the
      // smallest turns, ties to the previous tick's solution (weighted below the turns: a turn no longer needed relaxes,
      // at the planner's 5 deg/t)
      const gap = Math.max(...lows) - low;
      let cost = 10 * Math.max(0, gap - .035) + gap * .05 + .001 * (incl + tip + Math.abs(rock));
      if (prevBest) cost += .0005 * (Math.abs(incl - prevBest.incl) + Math.abs(tip - prevBest.tip) + Math.abs(rock - prevBest.rock));
      if (!best || cost < best.cost - 1e-12) best = {incl, tip, rock, cost, gap, lows: lows.map(x => x - low)};
    }
  }
  return best;
}
// the swing of the hat between worn and back (or back and worn): its position about the neck in the torso frame turns from
// over the head to behind the back on an arc (polar: angle and radius interpolated), the rotation slerped
function arcBlend(A, B, w, Nb, Cq) {
  const ic = conj(Cq), a = rot(ic, sub(A.t, Nb)), b = rot(ic, sub(B.t, Nb));
  const ang = v => Math.atan2(v[2], v[1]), rad = v => Math.hypot(v[1], v[2]);
  const t = ang(a) + (ang(b) - ang(a)) * w, r = rad(a) + (rad(b) - rad(a)) * w, x = a[0] + (b[0] - a[0]) * w;
  return {t: add(Nb, rot(Cq, [x, r * Math.cos(t), r * Math.sin(t)])), q: slerp(A.q, B.q, w)};
}
// turn the sword about its grip (smallest turn, iterated) until its whole hull is `clear` b above the floor
function groundSword(G, Q, fwd = [0, 0, -1], clear = .10) {
  const pts = hullOf('sword', 'sword');
  let out = Q;
  for (let it = 0; it < 8; it++) {
    let lo = null, ly = Infinity;
    for (const P of pts) { const y = G[1] + rot(out, P)[1]; if (y < ly) { ly = y; lo = P; } }
    if (ly >= clear - 1e-4) break;
    const L = len(lo), d = times(rot(out, lo), 1 / L), minYv = (clear + 2e-3 - G[1]) / L;
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
void STRINGS; void SCAB;
