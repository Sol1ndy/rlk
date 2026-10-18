// Vector / quaternion helpers and forward kinematics shared by the mid-boss display-entity rigs
// (Corrupted Guardian, Moonlit Butterfly); guardian_rig_math.mjs re-exports this module.
// Frame: +X = her left, +Y up, -Z forward, blocks; the floor point under her is the origin.
// Quaternions are [x, y, z, w]; euler triples are degrees applied X, then Y, then Z
// (q = Rz * Ry * Rx, as build_raiden_rig.mjs). Pitch +X leans back, -X bows forward; yaw +Y
// turns her to her right; roll +Z tips the top toward her right.
export const rad = d => d * Math.PI / 180;
export const add = (a, b) => a.map((x, i) => x + b[i]);
export const sub = (a, b) => a.map((x, i) => x - b[i]);
export const times = (v, s) => v.map(x => x * s);
export const lerp = (a, b, t) => a.map((x, i) => x + (b[i] - x) * t);
export const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
export const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
export const len = v => Math.hypot(...v);
export const unit = v => times(v, 1 / Math.max(len(v), 1e-9));
export function mul(a, b) { const [x, y, z, w] = a, [X, Y, Z, W] = b; return [w * X + x * W + y * Z - z * Y, w * Y - x * Z + y * W + z * X, w * Z + x * Y - y * X + z * W, w * W - x * X - y * Y - z * Z]; }
export function q(e = [0, 0, 0]) { const [x, y, z] = e.map(v => rad(v) / 2); return mul(mul([0, 0, Math.sin(z), Math.cos(z)], [0, Math.sin(y), 0, Math.cos(y)]), [Math.sin(x), 0, 0, Math.cos(x)]); }
export const rot = (Q, v) => mul(mul(Q, [...v, 0]), [-Q[0], -Q[1], -Q[2], Q[3]]).slice(0, 3);
export const unit4 = v => { const m = Math.hypot(...v); return v.map(x => x / m); };
export function slerp(a, b, t) {
  let d = dot(a, b) + a[3] * b[3];
  if (d < 0) { b = b.map(x => -x); d = -d; }
  if (d > .9995) return unit4(a.map((x, i) => x + (b[i] - x) * t));
  const th = Math.acos(d), s = Math.sin(th);
  return a.map((x, i) => (x * Math.sin((1 - t) * th) + b[i] * Math.sin(t * th)) / s);
}
export const qAngle = (a, b) => 2 * Math.acos(Math.min(1, Math.abs(dot(a, b) + a[3] * b[3]))) * 180 / Math.PI;
// Rotation whose columns are the images of the authoring x/y/z axes.
export function basisQ(X, Y, Z) {
  const m = [[X[0], Y[0], Z[0]], [X[1], Y[1], Z[1]], [X[2], Y[2], Z[2]]], tr = m[0][0] + m[1][1] + m[2][2];
  let s;
  if (tr > 0) { s = Math.sqrt(tr + 1) * 2; return unit4([(m[2][1] - m[1][2]) / s, (m[0][2] - m[2][0]) / s, (m[1][0] - m[0][1]) / s, s / 4]); }
  if (m[0][0] > m[1][1] && m[0][0] > m[2][2]) { s = Math.sqrt(1 + m[0][0] - m[1][1] - m[2][2]) * 2; return unit4([s / 4, (m[0][1] + m[1][0]) / s, (m[0][2] + m[2][0]) / s, (m[2][1] - m[1][2]) / s]); }
  if (m[1][1] > m[2][2]) { s = Math.sqrt(1 + m[1][1] - m[0][0] - m[2][2]) * 2; return unit4([(m[0][1] + m[1][0]) / s, s / 4, (m[1][2] + m[2][1]) / s, (m[0][2] - m[2][0]) / s]); }
  s = Math.sqrt(1 + m[2][2] - m[0][0] - m[1][1]) * 2;
  return unit4([(m[0][2] + m[2][0]) / s, (m[1][2] + m[2][1]) / s, s / 4, (m[1][0] - m[0][1]) / s]);
}
export const perp = (v, axis) => sub(v, times(axis, dot(v, axis)));
// Frame with model -Y along dir (a hanging segment) and its front face (-Z) toward `front`.
export function aimQ(dir, front = [0, 0, -1]) {
  const Y = times(unit(dir), -1);
  let F = perp(front, Y);
  if (len(F) < 1e-4) F = perp([0, 1, 0], Y);
  const Z = times(unit(F), -1), X = cross(Y, Z);
  return basisQ(X, Y, Z);
}
// Spear frame: tip (model +Y) along `tip`, blade plane normal (model -Z face) toward `face`.
export function sp(tip, face = [0, 0, -1]) {
  const T = unit(tip);
  let N = perp(face, T);
  if (len(N) < 1e-4) N = perp([0, 0, -1], T);
  if (len(N) < 1e-4) N = perp([1, 0, 0], T);
  const Z = times(unit(N), -1), X = cross(T, Z);
  return basisQ(X, T, Z);
}
// Two-bone IK: shoulder S, wrist target W, segment lengths a, b, elbow pole direction.
// Up to 12 % stretch when the target is out of reach; the wrist falls short beyond that.
// prevV (optional): the previous frame's bend direction (`v` of the last result). Where the
// pole lies within about 30 degrees of the shoulder-wrist line its bend plane is unstable, so
// the elbow keeps the previous side there, and the bend plane never turns more than MAX_BEND
// degrees per frame; this removes the one-tick elbow flips of a fixed pole.
const MAX_BEND = 40 * Math.PI / 180;
export const smoothK = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
export function ik(S, W, a, b, pole, prevV = null) {
  const d = sub(W, S), L = len(d), u = unit(d);
  let k = 1;
  if (L > (a + b) * .995) k = Math.min(1.12, L / ((a + b) * .995));
  const A = a * k, B = b * k, Lc = Math.min(Math.max(L, Math.abs(A - B) + .02), (A + B) * .995);
  const cosA = Math.max(-1, Math.min(1, (A * A + Lc * Lc - B * B) / (2 * A * Lc))), al = Math.acos(cosA);
  const pp = perp(pole, u), strength = len(pp) / Math.max(len(pole), 1e-9);   // sin(pole, line)
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
  const E = add(S, add(times(u, A * cosA), times(v, A * Math.sin(al))));
  const Wr = add(S, times(u, Lc));
  return {E, W: Wr, v, stretch: k, short: L - Lc};
}
// Roll reference for an arm segment: the inside of the bend (-v) faces the segment's front
// (model -Z); where the segment runs along the bend direction (a tightly folded arm) it falls
// back to the torso front. Stable for any arm direction, unlike the torso front alone.
export function armFront(dir, v, front) {
  const D = unit(dir), f1 = perp(times(v, -1), D), f2 = perp(front, D), w = smoothK(.12, .35, len(f1));
  const a = len(f1) > 1e-6 ? unit(f1) : [0, 0, 0], b = len(f2) > 1e-6 ? unit(f2) : unit(perp([0, 1, 0], D));
  const F = add(times(a, w), times(b, 1 - w));
  return len(F) > 1e-6 ? F : b;
}
// Direction perpendicular to `axis` from `raw`, kept continuous across frames: it turns about
// the axis from the previous frame's direction toward raw by at most MAX_ROLL per frame, and
// where raw lies near the axis (strength = sin of the angle below about 0.4) by a weighted
// share only. A fist therefore rolls round the shaft over a few ticks instead of flipping in
// one when the shaft sweeps through the shoulder direction (body space: root spins do not count).
const MAX_ROLL = 55 * Math.PI / 180;
export function steadyPerp(raw, axis, prev = null, fallback = [0, 0, -1]) {
  const pr = perp(raw, axis), s = len(pr) / Math.max(len(raw), 1e-9);
  let F = len(pr) > 1e-6 ? unit(pr) : unit(perp(fallback, axis));
  if (!prev) return F;
  const pv = perp(prev, axis);
  if (len(pv) < 1e-6) return F;
  const P = unit(pv), w = smoothK(.12, .42, s);
  const ang = Math.max(-MAX_ROLL, Math.min(MAX_ROLL, Math.atan2(dot(cross(P, F), axis), dot(P, F)) * w));
  return unit(add(times(P, Math.cos(ang)), times(cross(axis, P), Math.sin(ang))));
}
// Display conversion of a rig-frame transform (z mirror; see build_raiden_rig.mjs posed()).
export const toDisplayT = t => [t[0], t[1], -t[2]];
export const toDisplayQ = Q => [-Q[0], -Q[1], Q[2], Q[3]];
