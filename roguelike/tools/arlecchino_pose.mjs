// Skeleton and pose solver of the 아를레키노 (Arlecchino) rig (S:ar/PLAN.md §2.1; API tools/arlecchino_rig_api.md).
//
// The skeleton is the player avatar's (tools/build_player_rig.mjs transform(), copied below as avatarTransform for the
// parity test): hip 0.75, torso 0.75 to the neck, shoulders at +-0.34375 (slim, form p1) / +-0.375 (classic, form p2)
// and 0.625 up the torso, elbow 0.25 below the shoulder, hand point 0.34375 below the elbow, thigh pivots at +-0.125,
// knee 0.375 below, sole 0.375 below the knee. The boss is the avatar x SIZE (api.SIZE = 1.4): solve() works in avatar
// units and scales every translation and part scale by SIZE about the anchor point on the floor at the end.
//
// Frames. Rig frame: +X her left, +Y up, -Z forward, avatar units; origin = the anchor (the boss body) on the floor.
// Quaternions [x, y, z, w]; eulers [pitch, yaw, roll] degrees as the avatar's quat() (= mboss_rig_math.q, q = Rz Ry Rx):
// pitch + leans back, yaw + turns her to her right (clockwise from above), roll + tips the top toward her right.
// Side-signed channels (bearings, rolls, plane eulers, pole x) are written for the left side and mirrored for the right
// (+ = outward on both sides).
//
// Pose channels (the defaults are DEFAULT_POSE in arlecchino_clips.mjs)
//   sh [x,y,z]          hip shift (the avatar's shift)        rt [p,y,r]  root about the hip (the whole figure)
//   to [p,y,r]          torso                                  hd [p,y,r]  head
//   fR fL [x,y,z]       sole targets (IK legs), rig frame turned by fy (deg); y 0 = planted (the sole box on the floor)
//   kR kL [x,y,z]       knee poles (foot frame, side-signed x)
//   Arms, per side X in {R, L} (R = her right, holds scythe_r; L = her left, holds scythe_l in form p2):
//   wX 0|1              the arm holds its scythe (grip channels) / is free
//   aX [p,r,k]          free hand: pitch (+ forward / up the front), roll (+ out to her side), reach 0..1 about the shoulder
//   hX [x,y,z], hXw     free hand point in the torso frame from the neck point (rig x: + her left), blended by hXw
//   pX [x,y,z]          elbow pole, torso frame, side-signed x
//   onL / onR 0..1      the free hand on the OTHER scythe's shaft (two-handed), at onD (+ toward the head) from that grip
//   Scythe X (pivot = the model grip [8,8,8] at the hand):
//   gX [b,e,d]          the grip on a sphere about the shoulder (torso frame): bearing (+ out), elevation, distance
//   gfX, glX            0 = the sphere; 1 = on the lever glX along the shaft from the shoulder (a straight arm along the haft)
//   spX [p,y,r]         the cutting plane: the frontal plane (up, out) turned by this euler (torso frame, side-signed)
//   thX                 the shaft angle in the plane: 0 up, 90 out, 180 down, -90 across her body; a swing = thX keyed
//   edX                 +1: the hook (the crescent's point) leads when thX increases, -1 when it decreases (the avatar's
//                       calibrated strikes, tools/player_motion/arle.json infused_*: the point goes first); between keys
//                       the crescent rolls about the shaft (never a one-tick flip)          twX: extra roll about the shaft
//   slX                 the hand this far up the shaft from the model grip (+ toward the head)
//   ssX [x,y,z]         scale multipliers in the model frame (x = the hook width, y = the shaft); 0 = hidden
//   wdX 0|1, wpX        the scythe set in the world (rig frame point wpX, plane in the rig frame); the arm is free
//   Wings / blade legs (12 parts, 3 pairs a side, 2 segments):
//   lS lF lW lFl lV     spread 0..1, flare (lift, deg), wrap 0..1 (round her front), flap amplitude (deg), visibility
//                       (form p1 wings: 0 hidden .. 1; form p2 the legs are always shown)
//   lP [a,b,c]          per-pair scale (upper, middle, lower pair; the transition unfolds them one pair at a time)
//   tea 0|1, cupT       the cup (right hand) and saucer (left hand) shown; cup tilt toward her lips (deg)
//   vis                 everything scaled about the body centre (the death vanish)
//   ph                  loop phase 0..1 (set by the sampler: idle sway, wing flutter)
import {add, sub, times, len, unit, mul, q, rot, aimQ, ik, basisQ, cross, dot, perp, slerp, armFront, steadyPerp, toDisplayT, toDisplayQ, lerp, qAngle} from './mboss_rig_math.mjs';
import {hulls, AVATAR, SCYTHE, itemId, SHOULDER_X, BODY, PART_NAMES, CRESCENT_MID} from './arlecchino_geometry.mjs';

export const SIZE = 1.4;
export const SK = {hip: .75, torso: .75, shoulderY: .625, upper: .25, fore: .34375, pelvisX: .125, thigh: .375, shin: .375,
  sole: .015625, neck: [0, .75, 0], spine: [0, .56, .14], chest: [0, .48, -.14]};
const D = Math.PI / 180;
const ID = [0, 0, 0, 1];
const qa = (axis, deg) => { const s = Math.sin(deg * D / 2); return [axis[0] * s, axis[1] * s, axis[2] * s, Math.cos(deg * D / 2)]; };
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const mirrorE = e => [e[0], -e[1], -e[2]];
const MX = (v, s) => (s > 0 ? v : [-v[0], v[1], v[2]]);
const ME = (e, s) => (s > 0 ? e : mirrorE(e));

// ---- the avatar's transform() (tools/build_player_rig.mjs), copied for the parity test (hand attach only) --------------------
const zeros = [0, 0, 0];
function aquat(e = zeros) { const [x, y, z] = e.map(a => a * D / 2); return mul(mul([0, 0, Math.sin(z), Math.cos(z)], [0, Math.sin(y), 0, Math.cos(y)]), [Math.sin(x), 0, 0, Math.cos(x)]); }
export function avatarTransform(pose) {
  const fields = ['shift', 'root', 'torso', 'head', 'right_arm', 'right_elbow', 'left_arm', 'left_elbow', 'right_leg', 'right_knee', 'left_leg', 'left_knee', 'weapon', 'weapon_shift'];
  const p = {...Object.fromEntries([...fields.map(k => [k, [0, 0, 0]]), ['weapon_scale', [1, 1, 1]]]), ...pose};
  const root = aquat(p.root), body = aquat(p.torso), hip = add([0, .75, 0], p.shift), out = {};
  const top = add(hip, rot(body, [0, .75, 0]));
  out.body = {t: top, q: body}; out.head = {t: top, q: mul(body, aquat(p.head))};
  for (const [side, sign] of [['right', -1], ['left', 1]]) {
    const shoulder = add(hip, rot(body, [sign * .34375, .625, 0]));
    const arm = mul(body, aquat(p[side + '_arm']));
    const elbow = add(shoulder, rot(arm, [0, -.25, 0]));
    const fore = mul(arm, aquat(p[side + '_elbow']));
    out[side + '_arm'] = {t: shoulder, q: arm}; out[side + '_forearm'] = {t: elbow, q: fore};
    const leg = aquat(p[side + '_leg']), pelvis = add(hip, [sign * .125, 0, 0]);
    out[side + '_leg'] = {t: pelvis, q: leg};
    out[side + '_shin'] = {t: add(pelvis, rot(leg, [0, -.375, 0])), q: mul(leg, aquat(p[side + '_knee']))};
    if (side === 'right') out.weapon = {t: add(add(elbow, rot(fore, [0, -.34375, 0])), rot(fore, p.weapon_shift)), q: mul(fore, aquat(p.weapon)), s: p.weapon_scale};
  }
  for (const v of Object.values(out)) {
    v.t = add(hip, rot(root, v.t.map((x, i) => x - hip[i]))); v.q = mul(root, v.q);
    v.t = [v.t[0], v.t[1], -v.t[2]]; v.q = [-v.q[0], -v.q[1], v.q[2], v.q[3]];
  }
  return out;
}

// ---- hulls and floor helpers --------------------------------------------------------------------------------------------------
export function qm(Q) {
  const [x, y, z, w] = Q;
  return [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)], [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]];
}
// world points (rig frame) of a model at a transform {t, q, s} (s in the model frame)
export function worldPoints(model, v) {
  const H = hulls()[model];
  if (!H || !H.length || Math.max(...v.s.map(Math.abs)) < 1e-4) return [];
  const M = qm(v.q);
  return H.map(P => { const x = P[0] * v.s[0], y = P[1] * v.s[1], z = P[2] * v.s[2];
    return [v.t[0] + M[0][0] * x + M[0][1] * y + M[0][2] * z, v.t[1] + M[1][0] * x + M[1][1] * y + M[1][2] * z, v.t[2] + M[2][0] * x + M[2][1] * y + M[2][2] * z]; });
}
const lowest = (model, v) => { const P = worldPoints(model, v); return P.length ? Math.min(...P.map(x => x[1])) : Infinity; };
// the turn about `axis` lifting the model to y >= clear: the sense in which its lowest point starts to rise (so a slam into the
// floor turns back the way it came, the same way every tick), the other sense only when that one cannot clear it
// (toward = the part's main axis on the previous tick: when given, the turn goes back toward it, against the swing)
function liftTurn(model, v, axis, clear, maxDeg, pref = 1, toward = null, mainAxis = [0, 1, 0]) {
  const P0 = worldPoints(model, v);
  if (!P0.length) return {q: v.q, a: 0};
  let low = P0[0];
  for (const P of P0) if (P[1] < low[1]) low = P;
  if (low[1] >= clear) return {q: v.q, a: 0};
  const r = sub(low, v.t), dy = cross(axis, r)[1];
  let s0 = Math.abs(dy) > 1e-3 * len(r) ? Math.sign(dy) : pref;
  if (toward) { const A = rot(v.q, mainAxis), k = dot(cross(axis, A), toward); if (Math.abs(k) > .02) s0 = Math.sign(k); }
  const at = a => ({...v, q: mul(qa(axis, a), v.q)});
  const need = sg => {
    let lo = 0, hi = null;
    for (let x = 3; x <= maxDeg; x += 3) { if (lowest(model, at(sg * x)) >= clear) { hi = x; break; } lo = x; }
    if (hi === null) return null;
    for (let k = 0; k < 8; k++) { const m = (lo + hi) / 2; if (lowest(model, at(sg * m)) >= clear) hi = m; else lo = m; }
    return hi;
  };
  const a0 = need(s0), a1 = need(-s0);
  // the preferred sense unless the other one is much shorter (then the turn would swing round the long way)
  const sg = a0 !== null && (a1 === null || a0 <= 1.6 * a1 + 12) ? s0 : a1 !== null ? -s0 : s0;
  const a = (sg === s0 ? a0 : a1) ?? maxDeg;
  return {q: at(sg * a).q, a: sg * a};
}

// ---- the solve ------------------------------------------------------------------------------------------------------------------
// p: full pose; form 'p1' | 'p2'; prev: the previous tick's bookkeeping (continuity of rolls / bend planes) or null.
// Returns {parts: {name: {t, q, s, model}} (rig frame, boss units), anchors: {name: [x,y,z]} (boss units), keep (for the next tick)}.
export function solve(p, form = 'p1', prev = null) {
  const P = prev || {}, keep = {};
  const o = {};
  const part = (n, t, Q, s, model) => { o[n] = {t, q: Q, s: Array.isArray(s) ? s : [s, s, s], model}; };
  const rootQ = q(p.rt), hip = add([0, SK.hip, 0], p.sh);
  const Tq = mul(rootQ, q(p.to));
  const top = add(hip, rot(Tq, SK.neck));
  const Hq = mul(Tq, q(p.hd));
  const bodyModel = n => (form === 'p2' ? itemId('p2/' + n) : AVATAR(n));
  part('body', top, Tq, 1, bodyModel('body'));
  part('head', top, Hq, 1, bodyModel('head'));
  const fwd = rot(q([0, p.rt[1], 0]), [0, 0, -1]);
  const segQ = (key, dir, front) => { const F = steadyPerp(front, unit(dir), P['f_' + key], [0, 0, -1]); keep['f_' + key] = F; return aimQ(dir, F); };

  // ---- legs: IK to the sole targets; a tilted shin lifts its own target until its sole box clears the floor ----
  const footQ = q([0, p.fy || 0, 0]);
  for (const [s, k, F, kp] of [[1, 'L', p.fL, p.kL], [-1, 'R', p.fR, p.kR]]) {
    const side = s > 0 ? 'left' : 'right';
    const Hj = add(hip, rot(rootQ, [s * SK.pelvisX, 0, 0]));
    const pole = rot(footQ, MX(kp || [.12, 0, -1], s));
    const A = rot(footQ, F), ffwd = rot(footQ, [0, 0, -1]);
    // the sole point is the bottom of the shin's overlay box (0.375 + 0.0156 below the knee): a straight leg reaches it
    // from the hip at 0.75 + 0.0156 (DEFAULT_POSE sh y). A tilted shin stands on the corner of its sole box: the target
    // rises until that corner touches the floor (the leg's own lift; the root lift below only catches the rest)
    let sol, up = 0;
    for (let it = 0; it < 4; it++) {
      sol = ik(Hj, add(A, [0, up, 0]), SK.thigh, SK.shin + SK.sole, pole, P['leg' + k]);
      if (A[1] > .3) break;
      const d = sub(sol.W, sol.E), low = lowest(bodyModel(side + '_shin'), {t: sol.E, q: aimQ(d, armFront(d, times(sol.v, -1), ffwd)), s: [1, 1, 1]});
      if (Math.abs(low) < 2e-3) break;
      up = Math.max(0, up - low);
    }
    keep['leg' + k] = sol.v;
    const kv = times(sol.v, -1);
    part(side + '_leg', Hj, segQ('th' + k, sub(sol.E, Hj), armFront(sub(sol.E, Hj), kv, ffwd)), 1, bodyModel(side + '_leg'));
    part(side + '_shin', sol.E, segQ('sh' + k, sub(sol.W, sol.E), armFront(sub(sol.W, sol.E), kv, ffwd)), 1, bodyModel(side + '_shin'));
  }

  // ---- scythes: the frame in the cutting plane, the grip on the sphere / lever ----
  const shX = SHOULDER_X[form];
  const shoulder = s => add(hip, rot(Tq, [s * shX, SK.shoulderY, 0]));
  const scy = {};
  for (const [s, X] of [[-1, 'R'], [1, 'L']]) {
    const hold = (p['w' + X] || 0) > .5, world = (p['wd' + X] || 0) > .5;
    if (!hold && !world) continue;
    const frame = world ? q([0, 0, 0]) : Tq;
    const PQ = mul(frame, q(ME(p['sp' + X], s)));
    const up = rot(PQ, [0, 1, 0]), out = rot(PQ, [s, 0, 0]), nrm = unit(cross(up, out));
    const th = p['th' + X] * D, c = Math.cos(th), sn = Math.sin(th);
    const A = unit(add(times(up, c), times(out, sn)));
    const dA = unit(add(times(up, -sn), times(out, c)));
    const ed = clamp(p['ed' + X] ?? 1, -1, 1);
    let Hk = rot(qa(A, 90 * (1 - ed) + (p['tw' + X] || 0)), dA);
    const S = shoulder(s);
    let G;
    if (world) G = [...p['wp' + X]];
    else {
      const [b, e, d] = p['g' + X], dir = rot(Tq, MX([Math.sin(b * D) * Math.cos(e * D), Math.sin(e * D), -Math.cos(b * D) * Math.cos(e * D)], s));
      const Gs = add(S, times(dir, d)), Gl = add(S, times(A, p['gl' + X] ?? (SK.upper + SK.fore)));
      G = lerp(Gs, Gl, clamp(p['gf' + X] || 0));
    }
    scy[X] = {A, Hk, nrm, G, hold: hold && !world, S, s};
  }

  // ---- arms (IK) ----
  const chestFwd = rot(Tq, [0, 0, -1]);
  const armDir = (a, s) => { const Pp = a[0] * D, B = a[1] * D * s, y = -Math.cos(Pp), z = -Math.sin(Pp); return [-y * Math.sin(B), y * Math.cos(B), z]; };
  const hands = {};
  const reach = SK.upper + SK.fore;
  for (const [s, X, Y] of [[-1, 'R', 'L'], [1, 'L', 'R']]) {
    const side = s > 0 ? 'left' : 'right';
    const S = shoulder(s);
    let target, holdIt = scy[X]?.hold;
    if (holdIt) target = scy[X].G;
    else {
      const a = p['a' + X] || [0, 8, 1];
      target = add(S, times(rot(Tq, armDir(a, s)), (a[2] ?? 1) * reach * .985));
      const hw = clamp(p['h' + X + 'w'] || 0);
      if (hw > 0) target = lerp(target, add(top, rot(Tq, p['h' + X])), hw);
      const on = clamp(p['on' + X] || 0);
      if (on > 0 && scy[Y]) target = lerp(target, add(scy[Y].G, times(scy[Y].A, p.onD ?? -.3)), on);
    }
    const pole = rot(Tq, MX(p['p' + X] || [.55, -.35, .75], s));
    const sol = ik(S, target, SK.upper, SK.fore, pole, P['arm' + X]);
    keep['arm' + X] = sol.v;
    part(side + '_arm', S, segQ('ua' + X, sub(sol.E, S), armFront(sub(sol.E, S), sol.v, chestFwd)), 1, bodyModel(side + '_arm'));
    part(side + '_forearm', sol.E, segQ('fa' + X, sub(sol.W, sol.E), armFront(sub(sol.W, sol.E), sol.v, chestFwd)), 1, bodyModel(side + '_forearm'));
    hands[X] = sol.W;
    if (holdIt) scy[X].G = sol.W;          // the grip follows the hand where the arm falls short
  }

  // ---- place the scythes (the grip is the part pivot); turned up about the grip in their plane where they would reach the floor ----
  const guards = {};
  for (const [s, X, n] of [[-1, 'R', 'scythe_r'], [1, 'L', 'scythe_l']]) {
    const sc = scy[X];
    const ss = p['ss' + X] || [1, 1, 1];
    const shown = !!sc && (form === 'p2' || X === 'R') && Math.max(...ss.map(Math.abs)) > 1e-4;
    if (!shown) { part(n, hands[X], o[(s > 0 ? 'left' : 'right') + '_forearm'].q, 0, SCYTHE); continue; }
    let Q = basisQ(sc.Hk, sc.A, cross(sc.Hk, sc.A));
    const t = sub(sc.G, times(sc.A, p['sl' + X] || 0));
    const g = liftTurn(SCYTHE, {t, q: Q, s: ss}, sc.nrm, .03, 150, P['gs' + X] || 1, P['gA' + X] || null);
    if (g.a) keep['gs' + X] = Math.sign(g.a);
    keep['gA' + X] = rot(g.q, [0, 1, 0]);
    guards[n] = g.a;
    part(n, t, g.q, ss, SCYTHE);
  }

  // ---- wings (p1) / blade legs (p2): 3 pairs a side from the spine point, 2 segments; legs lag 2 ticks ----
  {
    const lagQ = P.lagT ? slerp(Tq, P.lagT[1] || Tq, .45) : Tq;
    keep.lagT = [Tq, P.lagT ? P.lagT[0] : Tq];
    const wing = form === 'p1', vis = wing ? clamp(p.lV || 0) : 1;
    const S_ = clamp(p.lS || 0), Fl = p.lF || 0, W_ = clamp(p.lW || 0), ph = (p.ph || 0) * 2 * Math.PI, flap = (p.lFl || 0);
    const root0 = add(hip, rot(Tq, SK.spine));
    const LEN = wing ? [.8, 1.0] : [.82, 1.06];
    // (elevation, azimuth from straight back toward her side) per pair: folded / spread; segment b absolute in the same terms
    const TAB = wing
      ? {a0: [[64, 18], [44, 22], [24, 26]], a1: [[52, 80], [26, 88], [2, 96]], b0: [[30, 14], [8, 18], [-14, 22]], b1: [[34, 104], [6, 112], [-24, 120]]}
      : {a0: [[64, 26], [40, 32], [16, 38]], a1: [[40, 70], [14, 80], [-12, 90]], b0: [[-34, 34], [-50, 42], [-64, 50]], b1: [[-48, 82], [-58, 90], [-70, 100]]};
    const dirOf = (el, az, s) => [s * Math.sin(az * D) * Math.cos(el * D), Math.sin(el * D), Math.cos(az * D) * Math.cos(el * D)];
    for (const [s, sideK] of [[1, 'L'], [-1, 'R']]) {
      for (let i = 0; i < 3; i++) {
        const idx = sideK === 'L' ? 2 * i + 1 : 2 * i + 2;    // legs 1 3 5 her left? -> 1/2 upper, 3/4 mid, 5/6 low
        const na = `leg_${idx}a`, nb = `leg_${idx}b`;
        const sway = (wing ? 1.5 : 3) * Math.sin(ph + i * 1.1 + (s > 0 ? 0 : .7)), fl = flap * Math.sin(ph * 2 + i * .5);
        const mix = (x0, x1) => [x0[0] + (x1[0] - x0[0]) * S_ + Fl + sway + fl, x0[1] + (x1[1] - x0[1]) * S_];
        let [ea, aa] = mix(TAB.a0[i], TAB.a1[i]), [eb, ab] = mix(TAB.b0[i], TAB.b1[i]);
        if (W_ > 0) { aa += (150 - aa) * W_ * .8; ab += (165 - ab) * W_ * .8; ea += (-10 - ea) * W_ * .5; eb += (-40 - eb) * W_ * .5; }
        const R0 = add(root0, rot(Tq, [s * .07, -.07 * i, 0]));
        const da = unit(rot(lagQ, dirOf(ea, aa, s)));
        const flat = d => { let f = perp([0, -1, 0], d); if (len(f) < 1e-3) f = perp(rot(Tq, [0, 0, 1]), d); return unit(f); };
        const cardQ = (d, f) => basisQ(times(f, -1), times(d, -1), cross(times(f, -1), times(d, -1)));
        const mA = wing ? itemId('wing_a') : itemId('leg_a'), mB = wing ? itemId('wing_b') : itemId('leg_b');
        let qa_ = cardQ(da, flat(da));
        // the wings / legs are drawn larger than the avatar scale (the footage's spans reach two to three times her height)
        const sc = vis * clamp((p.lP || [1, 1, 1])[i]) * (wing ? 1.25 : 1.35);
        if (sc > 1e-3) {
          const ax = unit(len(cross(da, [0, 1, 0])) > .2 ? cross(da, [0, 1, 0]) : rot(Tq, [1, 0, 0]));
          const g = liftTurn(mA, {t: R0, q: qa_, s: [sc, sc, sc]}, ax, .03, 120, P['lg' + na] || -1); qa_ = g.q; if (g.a) keep['lg' + na] = Math.sign(g.a);
        }
        const daF = rot(qa_, [0, -1, 0]);
        const R1 = add(R0, times(daF, LEN[0] * sc));
        const db = unit(rot(lagQ, dirOf(eb, ab, s)));
        let qb_ = cardQ(db, flat(db));
        if (sc > 1e-3) {
          const ax = unit(len(cross(db, [0, 1, 0])) > .2 ? cross(db, [0, 1, 0]) : rot(Tq, [1, 0, 0]));
          const g = liftTurn(mB, {t: R1, q: qb_, s: [sc, sc, sc]}, ax, .03, 140, P['lg' + nb] || -1); qb_ = g.q; if (g.a) keep['lg' + nb] = Math.sign(g.a);
        }
        part(na, R0, qa_, sc, mA);
        part(nb, R1, qb_, sc, mB);
      }
    }
  }

  // ---- props: the cup (right hand) and saucer (left hand), upright in the yaw frame ----
  {
    const tea = clamp(p.tea || 0), yq = q([0, p.rt[1] + (p.to[1] || 0) * .6, 0]);
    // shown at 1.5 x the boss scale (a teacup at the true 1.4 scale reads as a speck next to the blocky hands)
    part('cup', add(hands.R, [0, .02, 0]), mul(yq, q([-(p.cupT || 0), 0, 0])), tea * 1.5, itemId('cup'));
    part('saucer', add(hands.L, [0, -.045, 0]), yq, tea * 1.5, itemId('saucer'));
  }

  // ---- root lift: no body point below the floor ----
  let low = Infinity;
  for (const n of BODY) { const v = o[n]; const m = lowest(v.model, v); if (m < low) low = m; }
  const lift = low < 0 ? -low + 1e-4 : 0;
  if (lift) for (const v of Object.values(o)) v.t = add(v.t, [0, lift, 0]);
  for (const X of ['R', 'L']) if (hands[X]) hands[X] = add(hands[X], [0, lift, 0]);

  // ---- anchors (avatar units, before vis / SIZE) ----
  const an = {};
  an.hand_r = hands.R; an.hand_l = hands.L;
  an.palm_r = add(hands.R, rot(o.right_forearm.q, [0, -.02, -.07]));
  an.chest = add(add(hip, [0, lift, 0]), rot(Tq, SK.chest));
  an.spine = add(add(hip, [0, lift, 0]), rot(Tq, SK.spine));
  for (const [X, n] of [['R', 'scythe_r'], ['L', 'scythe_l']]) {
    const v = o[n];
    an['blade_' + X.toLowerCase()] = Math.max(...v.s) > 1e-4 ? add(v.t, rot(v.q, CRESCENT_MID.map((c, i) => c * v.s[i]))) : hands[X];
  }

  // ---- visibility about the body centre, then x SIZE about the anchor ----
  const vis = p.vis ?? 1;
  if (vis !== 1) {
    const C = add(hip, [0, .3 + lift, 0]);
    for (const v of Object.values(o)) { v.t = add(C, times(sub(v.t, C), vis)); v.s = times(v.s, vis); }
    for (const k of Object.keys(an)) an[k] = add(C, times(sub(an[k], C), Math.max(vis, .001)));
  }
  for (const v of Object.values(o)) { v.t = times(v.t, SIZE); v.s = times(v.s, SIZE); }
  for (const k of Object.keys(an)) an[k] = times(an[k], SIZE);
  return {parts: o, anchors: an, keep, lift: lift * SIZE, guards,
    edge: Object.fromEntries(['R', 'L'].filter(X => scy[X]).map(X => [X, {A: scy[X].A, Hk: scy[X].Hk, nrm: scy[X].nrm}]))};
}

// display conversion (z mirror) and back
export const toDisplay = v => ({t: toDisplayT(v.t), q: toDisplayQ(v.q), s: v.s});
export const fromDisplay = v => ({t: [v.t[0], v.t[1], -v.t[2]], q: [-v.q[0], -v.q[1], v.q[2], v.q[3]], s: v.s});
export {PART_NAMES, qAngle};
