// fit.mjs (H2c authoring tool): searches a clean sword grip for a contact pose. For a pose function G -> source pose (scarlet_cine.mjs
// _t builders) it tries grip points on a grid in the rig frame and keeps those the single-pose solve leaves alone: the hand reaches
// the grip, no clear / blade guard moves it (gripClear, bPush, bTurn, handClearL/R below `guardMax` cm), the blade's centre line
// passes the contact point within `tol`. The best by the distance to `near` (the grip wanted) is printed; its numbers go into the
// clip as constants (the build stays deterministic and does not run this).
//   import {searchGrip} from './fit.mjs'      (see the repel block of tools/scarlet_cine.mjs for the tables it produced)
import {points, solvePose, solveSeq, clipPose} from './probe.mjs';
import {DEFAULT_POSE} from '../../../../scarlet_clips.mjs';

const sub = (a, b) => a.map((x, i) => x - b[i]), len = a => Math.hypot(...a), dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
export const segDist = (P, A, B) => { const ab = sub(B, A), u = Math.max(0, Math.min(1, dot(sub(P, A), ab) / dot(ab, ab))); return len(sub(P, A.map((x, i) => x + ab[i] * u))); };
const BAD = ['gripClear', 'bPush', 'bTurn', 'handClearL', 'handClearR'];
export function evalPose(p) {
  const o = points(solvePose({...DEFAULT_POSE, gN: 0, ph: 0, ...p}));
  const g = BAD.reduce((s, n) => s + (o.guard[n] || 0), 0);
  return {o, g};
}
export function searchGrip(poseOf, {K = null, near, box, step = .06, guardMax = .6, tol = .03, dmin = .22, dmax = 1.5, show = 3, accept = null} = {}) {
  const out = [];
  for (let x = box[0][0]; x <= box[1][0] + 1e-9; x += step) for (let y = box[0][1]; y <= box[1][1] + 1e-9; y += step) for (let z = box[0][2]; z <= box[1][2] + 1e-9; z += step) {
    const G = [+x.toFixed(3), +y.toFixed(3), +z.toFixed(3)];
    if (K) { const d = len(sub(K, G)); if (d < dmin || d > dmax) continue; }
    let r; try { r = evalPose(poseOf(G)); } catch { continue; }
    const he = len(sub(r.o.hand_l, G)), kd = K ? segDist(K, r.o.hilt, r.o.tip) : 0;
    if (r.g > guardMax || he > .02 || kd > tol) continue;
    const ex = accept ? accept(r.o) : 0;
    if (ex === false) continue;
    out.push({G, g: +r.g.toFixed(2), he: +he.toFixed(3), kd: +kd.toFixed(3), d: +len(sub(G, near)).toFixed(3), ex, tip: r.o.tip, head: r.o.head, elbow: r.o.elbow_l});
  }
  out.sort((a, b) => a.d - b.d);
  return out.slice(0, show);
}

// the same search for tick t of a clip with the solver's history (ticks t0..t-1 as authored): what the builder's pass 1 gives there
export async function searchGripSeq(clip, t, poseOf, {K = null, near, box, step = .06, guardMax = .6, tol = .03, dmin = .22, dmax = 1.5, show = 3, accept = null, t0 = 0, handTol = .02} = {}) {
  const {solve} = await import('../../../../scarlet_pose.mjs');
  const {retarget, overlay, refCore} = await import('../../../../scarlet_retarget.mjs');
  const hist = await solveSeq(clip, t0, t - 1), base = await clipPose(clip, t), out = [];
  let refPrev = {};
  for (let k = t0; k < t; k++) refPrev = refCore(await clipPose(clip, k), refPrev).prev;
  for (let x = box[0][0]; x <= box[1][0] + 1e-9; x += step) for (let y = box[0][1]; y <= box[1][1] + 1e-9; y += step) for (let z = box[0][2]; z <= box[1][2] + 1e-9; z += step) {
    const G = [+x.toFixed(3), +y.toFixed(3), +z.toFixed(3)];
    if (K) { const d = len(sub(K, G)); if (d < dmin || d > dmax) continue; }
    let o;
    try { const p = {...base, ...poseOf(G)}, qq = overlay(retarget(p, clip, t), clip, t, {});
      o = points(solve(qq, k => hist[hist.length - k] || null, {}, {pass: 1, clip, t, ref: refCore(p, refPrev)})); } catch { continue; }
    const g = BAD.reduce((s, n) => s + (o.guard[n] || 0), 0), he = len(sub(o.hand_l, G)), kd = K ? segDist(K, o.hilt, o.tip) : 0;
    if (g > guardMax || he > handTol || kd > tol) continue;
    const ex = accept ? accept(o) : 0;
    if (ex === false) continue;
    out.push({G, g: +g.toFixed(2), he: +he.toFixed(3), kd: +kd.toFixed(3), d: +len(sub(G, near)).toFixed(3), ex, tip: o.tip, hilt: o.hilt});
  }
  out.sort((a, b) => a.d - b.d);
  return out.slice(0, show);
}
// the clip's ticks as the builder's pass 1 solves them: per tick the points and the distance of the blade's line to K (if given)
export async function reportSeq(clip, t0, t1, K = null) {
  const outs = await solveSeq(clip, 0, t1);
  return outs.slice(t0).map((o, i) => { const P = points(o); return {t: t0 + i, hilt: P.hilt, tip: P.tip, hand_l: P.hand_l, kd: K ? +segDist(K(t0 + i), P.hilt, P.tip).toFixed(3) : null, guard: P.guard}; });
}
