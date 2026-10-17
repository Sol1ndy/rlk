// Vector / quaternion helpers and the forward kinematics of the Corrupted Guardian rig.
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
const perp = (v, axis) => sub(v, times(axis, dot(v, axis)));
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
export function ik(S, W, a, b, pole) {
  const d = sub(W, S), L = len(d), u = unit(d);
  let k = 1;
  if (L > (a + b) * .995) k = Math.min(1.12, L / ((a + b) * .995));
  const A = a * k, B = b * k, Lc = Math.min(Math.max(L, Math.abs(A - B) + .02), (A + B) * .995);
  const cosA = Math.max(-1, Math.min(1, (A * A + Lc * Lc - B * B) / (2 * A * Lc))), al = Math.acos(cosA);
  let v = perp(pole, u);
  if (len(v) < 1e-4) v = perp([0, -1, 0], u);
  v = unit(v);
  const E = add(S, add(times(u, A * cosA), times(v, A * Math.sin(al))));
  const Wr = add(S, times(u, Lc));
  return {E, W: Wr, stretch: k, short: L - Lc};
}
// Display conversion of a rig-frame transform (z mirror; see build_raiden_rig.mjs posed()).
export const toDisplayT = t => [t[0], t[1], -t[2]];
export const toDisplayQ = Q => [-Q[0], -Q[1], Q[2], Q[3]];
