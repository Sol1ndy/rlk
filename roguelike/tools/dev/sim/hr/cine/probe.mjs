// probe.mjs (H2c authoring tool): solves single poses of 홍련's rig outside the builder (sample -> retarget -> overlay -> solve, one
// pass, no history / plan: the builder's own solve adds its guards' plans) and prints her points in the rig frame (+X her left,
// +Y up, -Z forward).
//   node tools/dev/sim/hr/cine/probe.mjs <clip> <t> [<t> ...]         a clip tick of scarlet_clips.mjs / scarlet_cine.mjs
//   node tools/dev/sim/hr/cine/probe.mjs --pose '<json of source channels>' [--clip <name for the patches> --t <tick>]
// Run from roguelike/. Output: one JSON line per pose {t, hilt, tip, dir, hand_l, hand_r, elbow_l, foot_l, foot_r, pelvis, head, hat_crown}.
import {solve, SK, setModels} from '../../../../scarlet_pose.mjs';
import {retarget, overlay, refCore, setHatFace, hatSwitches} from '../../../../scarlet_retarget.mjs';
import {CLIPS as FIGHT, accumulate, sampleClip, DEFAULT_POSE} from '../../../../scarlet_clips.mjs';
import {add, sub, rot, len, times} from '../../../../mboss_rig_math.mjs';
import {SWORD, allModels} from '../../../../scarlet_geometry.mjs';

setModels(allModels());
setHatFace({t: [0, .45, .5]});
const r3 = v => v && v.map(x => +x.toFixed(3));
export function points(o) {
  const A = o._anchors, sole = n => add(o[n].t, rot(o[n].q, [0, -SK.shin, 0]));
  const ax = rot(o.sword.q, [0, 1, 0]);
  return {hilt: r3(o.sword.t), tip: r3(A.blade_tip), dir: r3(ax), hand_l: r3(A.hand_l), hand_r: r3(A.hand_r), elbow_l: r3(o.forearm_l.t),
    foot_l: r3(sole('shin_l')), foot_r: r3(sole('shin_r')), pelvis: r3(o.pelvis.t), head: r3(A.head), hat_crown: r3(A.hat_crown), hat: r3(o.hat.t),
    sup: {dy: +o._support.dy.toFixed(3), lift: +o._lift.toFixed(3), coreLow: +o._support.coreLow.toFixed(3), lowRef: o._support.lowRef === null ? null : +o._support.lowRef.toFixed(3)},
    guard: Object.fromEntries(Object.entries(o._guard).map(([k, v]) => [k, +(typeof v === 'number' ? v : v.v).toFixed(2)]).filter(([, v]) => v > .3))};
}
export function solvePose(p, clip = '_', t = 0) {
  const qq = overlay(retarget(p, clip, t), clip, t, {});
  return solve(qq, () => null, {}, {pass: 1, clip, t, ref: refCore(p, {})});
}
// the clip's ticks t0..t1 solved in order with their history (the builder's pass 1: the arm's turn / fold limits, the lagging parts);
// over(t, pose) may replace the sampled pose of a tick. Returns the solved outputs (index 0 = t0).
export async function solveSeq(name, t0, t1, over = null) {
  const out = [];
  let refPrev = {};
  for (let t = t0; t <= t1; t++) {
    let p = await clipPose(name, t);
    if (over) p = over(t, p) || p;
    const ref = refCore(p, refPrev); refPrev = ref.prev;
    const qq = overlay(retarget(p, name, t), name, t, {});
    out.push(solve(qq, k => out[out.length - k] || null, {}, {pass: 1, clip: name, t, ref}));
  }
  return out;
}
export async function clipPose(name, t) {
  const cine = (await import('../../../../scarlet_cine.mjs'));
  const c0 = [...FIGHT, ...cine.CLIPS].find(c => c.name === name);
  if (!c0) throw new Error(`no clip ${name}`);
  const L = c0.keys[c0.keys.length - 1][0], c = {...c0, len: L}, base = c.base || DEFAULT_POSE, ks = accumulate(c, base);
  return sampleClip(c, t, ks, base);
}
if (process.argv[1] && process.argv[1].endsWith('probe.mjs')) {
  const a = process.argv.slice(2);
  if (a[0] === '--pose') {
    const p = {...DEFAULT_POSE, ph: 0, ...JSON.parse(a[1])};
    const ci = a.indexOf('--clip'), ti = a.indexOf('--t');
    console.log(JSON.stringify(points(solvePose(p, ci < 0 ? '_' : a[ci + 1], ti < 0 ? 0 : +a[ti + 1]))));
  } else {
    for (const t of a.slice(1)) { const p = await clipPose(a[0], +t); console.log(JSON.stringify({t: +t, ...points(solvePose(p, a[0], +t))})); }
  }
}
void len; void times; void sub; void SWORD; void hatSwitches;
