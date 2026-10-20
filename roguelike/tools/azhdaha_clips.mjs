// Clips of the 야타용왕 (Azhdaha) rig, stage R3a: the 41 clips of plan.md §3.2 / contract manifest.md §5 (35 authored + 6
// mirrors) on the frozen R3 skeleton, plus the R1 debug poses as dbg_<name> (renders and checks only).
//
// Authoring model. Every clip is authored at footage speed (az/understand/motion.md §5 key poses, the binding lengths and
// events of the table below) and baked by bake() into DENSE keys, one per PLAYED tick (linear between ticks):
//   1. body keys: sparse [authored tick, pose, ease] keys (the shared format of mboss_rig_clips.mjs), sampled at the
//      authored time of each played tick (the inverse of the RETIME knots, so the compression stays smooth; retime only
//      compresses, plan §0), with per-channel delays (`lag`: overlapping action, the head leads, the pelvis follows) and
//      a per-segment delay of the tail chain (`tailLag`: follow-through, the tip arrives last);
//   2. overlays (breathing, tremor, the idle tail wave);
//   3. feet: every foot is a key list in the anchor frame (`feet`): planted in the world ('W': it stays put while the
//      body dips, tilts or the anchor turns by the clip's yaw schedule; the bake converts it to the root-frame IK target
//      of azhdaha_pose.mjs and counter-rotates it), keyed in the root frame ('K': the body keys' fw*/hk* channels, e.g.
//      the fore paws carried up by a rear-up), riding with the root at rest ('R': burrows, the jump), or a function
//      ('F': walk / gallop cycles under a gliding anchor). Between keys the target blends with an arc lift;
//   4. secondary motion: damped springs on the played sequence (the beard bibs and the throat apron swing after the head
//      and chest move).
// A clip carries no horizontal root travel and no root yaw (the module moves and turns the anchor by the exported yaw
// schedule); a root z offset only while the body is hidden (Rig decision change 1: the tail-only pillar on the anchor).
// Mirrors (`_r` / `_fr` / `_hr` of the table) are generated: left / right channels swapped, x negated, yaw and roll
// negated.
//
// Frames: rig frame (+x the boss's left, +y up, +z BACK, the floor under the centre of the four feet) for the pose
// channels; the manifest's local frame is (x, y, -z). Yaw: Minecraft units, + = clockwise from above = toward the boss's
// right; turning toward its left is negative.
import {EASE, accumulate as acc, sampleClip as sampleShared} from './mboss_rig_clips.mjs';
import {J, ROOT_PIVOT, TAIL_SWEEP, PART_SCALE, solve, pointOf} from './azhdaha_pose.mjs';
import {partModels, PARTS} from './azhdaha_geometry.mjs';
import {q, mul, rot, add, sub, lerp, times} from './mboss_rig_math.mjs';

const mx = v => [-v[0], v[1], v[2]];
const D = Math.PI / 180;
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const smooth = u => { u = clamp(u, 0, 1); return u * u * (3 - 2 * u); };
const conj = Q => [-Q[0], -Q[1], -Q[2], Q[3]];
// euler [x, y, z] (degrees, q = Rz Ry Rx as mboss_rig_math q) of a quaternion
export function eulerOf(Q) {
  const [x, y, z, w] = Q;
  const r00 = 1 - 2 * (y * y + z * z), r10 = 2 * (x * y + z * w), r20 = 2 * (x * z - y * w), r21 = 2 * (y * z + x * w), r22 = 1 - 2 * (x * x + y * y);
  return [Math.atan2(r21, r22) / D, Math.asin(clamp(-r20, -1, 1)) / D, Math.atan2(r10, r00) / D];
}

// ---- the binding clip table (plan.md §3.2 = contract manifest.md §5): name, played len, authored len, loop, next,
// RETIME knots (authored -> played), played events. The builder asserts every clip against it.
export const CLIP_TABLE = [
  ['idle', 80, 80, true, null, null, {snarl: 30}],
  ['walk', 40, 40, true, null, null, {lh: 0, lf: 10, rh: 20, rf: 30}],
  ['walk_stop', 16, 16, false, 'idle', null, {plant: 4}],
  ['turn45_l', 24, 24, false, 'idle', null, {plant_1: 10, plant_2: 17, yaw0: 4, yaw1: 18}],
  ['turn45_r', 24, 24, false, 'idle', null, {plant_1: 10, plant_2: 17, yaw0: 4, yaw1: 18}],
  ['turn90_l', 36, 36, false, 'idle', null, {plant_1: 12, plant_2: 18, plant_3: 24, plant_4: 30, yaw0: 6, yaw1: 30}],
  ['turn90_r', 36, 36, false, 'idle', null, {plant_1: 12, plant_2: 18, plant_3: 24, plant_4: 30, yaw0: 6, yaw1: 30}],
  ['turn180', 60, 60, false, 'idle', null, {plant_1: 12, plant_2: 18, plant_3: 24, plant_4: 30, plant_5: 36, plant_6: 42, plant_7: 48, plant_8: 54, yaw0: 6, yaw1: 54}],
  ['intro', 150, 150, false, 'idle', null, {eyes: 25, rise: 30, crack1: 50, crack2: 70, seal: 112, land: 116, roar: 120, blast: 130}],
  ['pose_ref', 20, 20, true, null, null, {}],
  ['roar_low', 40, 50, false, 'idle', [[0, 0], [10, 8], [50, 40]], {roar: 8, blast: 10}],
  ['roar_rear', 82, 100, false, 'idle', [[0, 0], [20, 20], [76, 62], [100, 82]], {rise: 8, roar: 20, drop: 62, land: 74}],
  ['chin_slam', 65, 84, false, 'idle', [[0, 0], [47, 35], [84, 65]], {lift: 2, rear: 14, top: 23, drop: 32, impact: 35}],
  ['jump_slam', 53, 60, false, 'idle', [[0, 0], [28, 21], [60, 53]], {crouch: 0, takeoff: 6, apex: 13, land: 21, wave2: 32}],
  ['charge_coil', 26, 34, false, 'charge_run', [[0, 0], [32, 24], [34, 26]], {coil: 6, launch: 24}],
  ['charge_run', 12, 12, true, null, null, {plant: 6}],
  ['charge_stop', 21, 24, false, 'idle', [[0, 0], [8, 8], [24, 21]], {skid: 0, stop: 8}],
  ['spikes', 40, 48, false, 'idle', [[0, 0], [18, 14], [24, 20], [48, 40]], {brace: 0, launch: 14, launch_last: 20, gold_on: 0, gold_off: 22}],
  ['stomp_fl', 63, 72, false, 'idle', [[0, 0], [22, 17], [52, 47], [72, 63]], {lift: 5, slam: 13, w1: 17, w2: 32, w3: 47}],
  ['stomp_fr', 63, 72, false, 'idle', [[0, 0], [22, 17], [52, 47], [72, 63]], {lift: 5, slam: 13, w1: 17, w2: 32, w3: 47}],
  ['stomp_hl', 63, 72, false, 'idle', [[0, 0], [22, 17], [52, 47], [72, 63]], {lift: 5, slam: 13, w1: 17, w2: 32, w3: 47}],
  ['stomp_hr', 63, 72, false, 'idle', [[0, 0], [22, 17], [52, 47], [72, 63]], {lift: 5, slam: 13, w1: 17, w2: 32, w3: 47}],
  ['stomp3_fl', 85, 90, false, 'idle', [[0, 0], [22, 17], [90, 85]], {lift: 3, s1: 17, s2: 40, s3: 63}],
  ['stomp3_fr', 85, 90, false, 'idle', [[0, 0], [22, 17], [90, 85]], {lift: 3, s1: 17, s2: 40, s3: 63}],
  ['feint', 50, 56, false, 'idle', [[0, 0], [22, 22], [56, 50]], {sway: 0, swayback: 12, drop: 18, burst: 22}],
  ['tail_whip_l', 64, 64, false, 'idle', null, {raise: 0, cock: 12, pivot: 20, sweep: 23, sweep_end: 31, erupt: 33, settle: 42}],
  ['tail_whip_r', 64, 64, false, 'idle', null, {raise: 0, cock: 12, pivot: 20, sweep: 23, sweep_end: 31, erupt: 33, settle: 42}],
  ['tail_slam', 70, 90, false, 'idle', [[0, 0], [52, 39], [58, 45], [90, 70]], {raise: 0, hold: 9, slam: 36, impact: 39, spikes: 41}],
  ['burrow_dive', 40, 44, false, 'burrow_travel', [[0, 0], [18, 14], [44, 40]], {snarl: 3, dive: 14, under: 40}],
  ['burrow_travel', 20, 20, true, null, null, {}],
  ['burrow_breach', 36, 36, false, 'burrow_travel', null, {ring: 0, burst: 8, hit: 10, under: 30}],
  ['burrow_emerge', 53, 56, false, 'idle', [[0, 0], [40, 40], [56, 53]], {rumble: 0, burst: 8, fore: 24, out: 38, shake: 40}],
  ['landslide', 203, 270, false, 'idle', [[0, 0], [76, 57], [104, 77], [132, 98], [156, 118], [186, 139], [212, 159], [240, 179], [270, 203]],
    {tell: 0, w1: 57, w2: 77, w3: 98, w4: 118, w5: 139, rear: 159, w6: 179, end: 203}],
  ['absorb', 94, 108, false, 'idle', [[0, 0], [12, 12], [60, 46], [108, 94]], {press: 0, rise: 46, burst: 47, stamp1: 62, stamp2: 86, gold_on: 0, gold_off: 60}],
  ['absorb_p3', 52, 70, false, 'idle', [[0, 0], [60, 42], [70, 52]], {orb: 0, burst: 42, gather: 42, gold_on: 0, gold_off: 50}],
  ['p3_sink', 66, 80, false, 'tail_pillar', [[0, 0], [8, 8], [50, 40], [80, 66]], {sink: 8, under: 40, tail: 40, pillar: 58}],
  ['tail_pillar', 80, 80, true, null, null, {pulse: 0, pulse2: 40}],
  ['tail_pillar_strike', 24, 24, false, 'tail_pillar', null, {strike: 10}],
  ['tail_pillar_sink', 20, 20, false, null, null, {gone: 18}],
  ['tail_cast', 34, 40, false, 'idle', [[0, 0], [24, 18], [40, 34]], {raise: 0, charge: 12, fire: 18, lower: 26}],
  ['death', 120, 120, false, null, null, {stagger: 0, chin: 34, tail: 66, last: 80, head: 92, still: 96}],
];
export const TABLE = Object.fromEntries(CLIP_TABLE.map(([name, len, authored, loop, next, retime, events]) => [name, {name, len, authored, loop, next, retime, events}]));
export const MIRRORS = {turn45_r: 'turn45_l', turn90_r: 'turn90_l', stomp_fr: 'stomp_fl', stomp_hr: 'stomp_hl', stomp3_fr: 'stomp3_fl', tail_whip_r: 'tail_whip_l'};
// Hidden spans / recorded states (contract manifest.md §4.6, binding; the clips hide exactly these ticks) and the clips a
// respawn queues per stored body state.
export const RESPAWN_CLIP = {normal: 'idle', burrowed: 'burrow_travel', tail_only: 'tail_pillar'};
export const TRACK_CLIPS = ['tail_whip_l', 'tail_whip_r', 'tail_slam', 'tail_cast', 'tail_pillar', 'tail_pillar_strike', 'tail_pillar_sink', 'p3_sink'];

// ---- tail curves (per-segment UP angles, deg: + raises a segment; the tail region's constants) --------------------------
export const tailUp = (ups, yaw = [], roll = []) => Object.fromEntries(ups.map((u, i) => ['t' + (i + 1), [-u, yaw[i] || 0, roll[i] || 0]]));
export const fore = (w, e = [0, 0, 0], wr = null, er = null) => ({fwL: w, fpL: e, fwR: wr || mx(w), fpR: er || [e[0], -e[1], -e[2]]});
export const hind = (h, e = [0, 0, 0], hr = null, er = null) => ({hkL: h, hfL: e, hkR: hr || mx(h), hfR: er || [e[0], -e[1], -e[2]]});
// TAIL_REST: the idle carry, a big arc rising from the rump, back and over, the leafy tip forward over the mid-back at
// ~10 b (v3 23.6 s, v3 f1365, v1 idle front: the "tree" above the plates).
export const TAIL_REST = [22, 25, 27, 28, 27, 25, 23, 21];
// TAIL_LOOP: the phase-3 loop / shells carry (v8 f2280 trace: top 11.3-11.8 b, rear z ~9, the tip over the shoulders).
export const TAIL_LOOP = [29, 28, 29, 29, 26, 22, 19, 18];
// TAIL_LOW: laid out behind, the branch just off the floor (v3 f1680); TAIL_WHIP: flat on the floor for the sweep.
export const TAIL_LOW = [-8, -6, -2, 4, 7, 5, 3, 1];
export const TAIL_WHIP = [-9, -10, 1, 6, 9, 4, 0, -3];
// R3a curves: TAIL_HIGH the tail-slam raise (a near straight pole over the rump, the tip ~12 b up, v3 J f24.9);
// TAIL_FLAT the slam impact (straight back along the floor, the branch lifted at the end); TAIL_BRACE the rear-up
// third leg (relative to a pelvis pitched up 45-55: the root segment lifts back to the floor line); TAIL_CAST the
// scorpion cast (the root raised, the column vertical, the branch curled forward over the shoulders, v7 A1);
// TAIL_TUCK the dive (following the body into the hole). (R3b: TAIL_HIGH's branch t5-t8 curls a little further over
// the back, so the raised tip of tail_whip / tail_slam stays inside its 18 b culling box: it overshot by 0.2-0.4 b)
export const TAIL_HIGH = [46, 22, 12, 10, 10, 11, 13, 15];
export const TAIL_FLAT = [-12, -9, -2, 3, 5, 3, 6, 12];
export const TAIL_BRACE = [46, 4, -2, 0, 4, 8, 10, 14];
export const TAIL_CAST = [44, 30, 18, 12, 30, 34, 30, 26];
export const TAIL_TUCK = [-20, -14, -8, -4, -2, 0, 0, 0];
// TAIL_PILLAR: the tail-only pillar (body hidden, the root sunk with the root z offset of Rig decision change 1 so the
// tail root lies under the anchor): t1 turned straight up (+90 about the pelvis), the column straight to t7 so the four
// tail columns stack on the anchor (contract §4.4: within 0.3 b), the crown (t8, tip) nodding forward.
export const TAIL_PILLAR = [90, 0, 0, 0, 0, 0, 6, 18];
export const PILLAR_ROOT = {pos: [0, -8.55, -J.t1[2]], rot: [0, 0, 0]};
export const DEFAULT_POSE = {
  pos: [0, 0, 0], rot: [0, 0, 0],
  pelvis: [0, 0, 0], spine: [0, 0, 0], chest: [0, 0, 0], neck1: [0, 0, 0], neck2: [0, 0, 0], head: [0, 0, 0], jaw: 0,
  beard1: [0, 0, 0], beard2: [0, 0, 0], apron: [0, 0, 0],
  flN: 0, flS: 0, flM: 0, flH: 0, flK: 1,
  ...fore(J.wrist), ...hind(J.hock),
  ...tailUp(TAIL_REST), tLift: 0, tCurl: 0, tSweep: 0, tTwist: 0,
  vis: 1, visBody: 1, visTail: 1,
};
export const restPose = () => structuredClone(DEFAULT_POSE);
export const accumulate = clip => acc(clip, DEFAULT_POSE);
export const sampleClip = (clip, t, ks) => sampleShared(clip, t, ks, {defaults: DEFAULT_POSE});

// ---- feet ------------------------------------------------------------------------------------------------------------------
export const REST_FEET = {fl: J.wrist, fr: mx(J.wrist), hl: J.hock, hr: mx(J.hock)};
const FOOT_CH = {fl: ['fwL', 'fpL'], fr: ['fwR', 'fpR'], hl: ['hkL', 'hfL'], hr: ['hkR', 'hfR']};
export const FEET = ['fl', 'fr', 'hl', 'hr'];
// the anchor frame of an anchor turned by yaw d (MC deg, + clockwise from above) seen from the clip-start frame:
// a world point W (clip-start rig frame) in the turned frame
export const toAnchor = (W, d) => { const c = Math.cos(d * D), s = Math.sin(d * D); return [W[0] * c - W[2] * s, W[1], W[0] * s + W[2] * c]; };
// the world point (clip-start frame) of the rest foot of an anchor turned to heading h
export const restAt = (f, h = 0) => toAnchor(REST_FEET[f], -h);
const PIV = ROOT_PIVOT;
const toRoot = (A, P) => add(rot(conj(q(P.rot)), sub(sub(A, P.pos), PIV)), PIV);
const rootEuler = (E, P) => (P.rot[0] || P.rot[1] || P.rot[2] ? eulerOf(mul(conj(q(P.rot)), q(E))) : E);
const upRoot = P => rot(conj(q(P.rot)), [0, 1, 0]);

// the shoulder / hip of a pose in the root frame and the chest / pelvis bone rotation (mode 'S' feet: a target fixed in the
// chest or pelvis frame, e.g. the fore paws folded in front of a reared chest whatever its angle)
function limbBase(P, f) {
  const qp = q(P.pelvis), qs = mul(qp, q(P.spine)), qc = mul(qs, q(P.chest));
  const s = f[1] === 'r' ? -1 : 1, m = v => [s * v[0], v[1], v[2]];
  if (f[0] === 'h') return {t: add(J.pelvis, rot(qp, sub(m(J.hip), J.pelvis))), q: qp};
  const ts = add(J.pelvis, rot(qp, sub(J.spine1, J.pelvis))), tc = add(ts, rot(qs, sub(J.chest, J.spine1)));
  return {t: add(tc, rot(qc, sub(m(J.shoulder), J.chest))), q: qc};
}
// ---- floor guard: the low parts of the head chain, the beard bibs, the throat apron and the tail keep clear of the floor
// (element-hull points of the real models); the head is lifted at neck1 (the face kept level), the bibs swept back, the
// apron swung forward, a tail segment raised. Off while the rig is buried or hidden; `contact` spans allow the chin
// lower (an intended impact). The corrections are smoothed over +-2 ticks (never below what a tick needs).
const D2R = Math.PI / 180;
function elCorners(e, k) {
  const out = [];
  for (const x of [e.from[0], e.to[0]]) for (const y of [e.from[1], e.to[1]]) for (const z of [e.from[2], e.to[2]]) {
    let p = [x, y, z];
    if (e.rotation && e.rotation.angle) {
      const {angle, axis, origin} = e.rotation, a = angle * D2R, c = Math.cos(a), s = Math.sin(a), d = [p[0] - origin[0], p[1] - origin[1], p[2] - origin[2]];
      const r = axis === 'x' ? [d[0], d[1] * c - d[2] * s, d[1] * s + d[2] * c] : axis === 'y' ? [d[0] * c + d[2] * s, d[1], -d[0] * s + d[2] * c] : [d[0] * c - d[1] * s, d[0] * s + d[1] * c, d[2]];
      p = [r[0] + origin[0], r[1] + origin[1], r[2] + origin[2]];
    }
    out.push([(8 - p[0]) * k / 16, (p[1] - 8) * k / 16, (p[2] - 8) * k / 16]);
  }
  return out;
}
const GUARD_PARTS = ['head', 'jaw', 'eyes', 'horn_l', 'horn_r', 'beard1', 'beard2', 'apron', 'glow_apron', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 'tip',
  'chest', 'belly', 'pelvis', 'tail_skirt', 'neck1', 'neck2', 'bracer_l', 'bracer_r', 'glow_bracer_l', 'glow_bracer_r'];
let HULL = null;
function hull() {
  if (HULL) return HULL;
  const models = partModels(), MOD = Object.fromEntries(PARTS.map(([n, m]) => [n, m]));
  const dirs = []; for (let i = 0; i < 60; i++) { const z = 1 - 2 * (i + .5) / 60, r = Math.sqrt(1 - z * z), ph = i * 2.39996; dirs.push([r * Math.cos(ph), r * Math.sin(ph), z]); }
  HULL = {};
  for (const n of GUARD_PARTS) {
    const pts = (models[MOD[n]] || []).flatMap(e => elCorners(e, PART_SCALE[n])), keep = new Set();
    for (const d of dirs) { let b = -1, bv = -Infinity; pts.forEach((p, i) => { const v = p[0] * d[0] + p[1] * d[1] + p[2] * d[2]; if (v > bv) { bv = v; b = i; } }); if (b >= 0) keep.add(b); }
    HULL[n] = [...keep].map(i => pts[i]);
  }
  return HULL;
}
const lowOf = (o, names) => { let m = Infinity; for (const n of names) { if (o[n].s[0] < 1e-4) continue; for (const pt of hull()[n]) m = Math.min(m, pointOf(o, n, pt)[1]); } return m; };
// (R3b: the rump skirt is not in the body group: it is a flap hinged at the tail root that swings clear of the floor itself,
// azhdaha_pose.mjs SKIRT_FLOOR)
const GROUPS = {head: ['head', 'jaw', 'eyes', 'horn_l', 'horn_r'], beard: ['beard1', 'beard2'], apron: ['apron', 'glow_apron'], body: ['chest', 'belly', 'pelvis', 'neck1', 'neck2'],
  bl: ['bracer_l', 'glow_bracer_l'], br: ['bracer_r', 'glow_bracer_r']};
// the body underside on the floor: the root is raised by what the torso sinks below it (before the feet are solved, so the
// planted feet stay put); returns the raise
function bodyLift(P) {
  let lift = 0;
  for (let it = 0; it < 4; it++) {
    const lo = lowOf(solve(P), GROUPS.body);
    if (lo >= -.005) break;
    const d = -lo + .01;
    P.pos = add(P.pos, [0, d, 0]); lift += d;
  }
  return lift;
}
const TAILN = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8'];
function guardNeeds(P, allow, cap = .16) {
  // returns the corrections {neck, beard, apron, tail: [8]} this pose needs (0 when clear)
  const need = {neck: 0, beard: 0, apron: 0, fwL: 0, fwR: 0, tail: new Array(8).fill(0)};
  const Q = structuredClone(P);
  for (let it = 0; it < 8; it++) {
    const o = solve(Q);
    let done = true;
    const h = lowOf(o, GROUPS.head), cl = .04 - allow;
    if (h < cl) { const d = Math.min(25, (cl - h) / .035 + .3); need.neck += d; Q.neck1 = add(Q.neck1, [d, 0, 0]); Q.head = add(Q.head, [-.55 * d, 0, 0]); done = false; }
    const b = lowOf(o, GROUPS.beard);
    if (b < .03) { const d = Math.min(25, (.03 - b) / .02 + .5); need.beard += d; Q.beard1 = add(Q.beard1, [-d, 0, 0]); Q.beard2 = add(Q.beard2, [-.6 * d, 0, 0]); done = false; }
    const a = lowOf(o, GROUPS.apron);
    if (a < .03) { const d = Math.min(25, (.03 - a) / .025 + .5); need.apron += d; Q.apron = add(Q.apron, [d, 0, 0]); done = false; }
    for (const [g, ch] of [['bl', 'fwL'], ['br', 'fwR']]) {
      const lo = lowOf(o, GROUPS[g]);
      if (lo < -.02 && need[ch] < cap) { const d = Math.min(cap - need[ch], -.02 - lo + .01); need[ch] += d; Q[ch] = add(Q[ch], times(upRoot(Q), d)); done = false; }
    }
    for (let i = 0; i < 9; i++) {
      const names = i < 8 ? [TAILN[i]] : ['tip'];
      const lo = lowOf(o, names);
      if (lo < .05) {
        const k = Math.min(i, 7), d = Math.min(20, (.05 - lo) / (.035 * (1 + Math.max(0, i - k))) + .4);
        need.tail[k] += d; Q[TAILN[k]] = add(Q[TAILN[k]], [-d, 0, 0]); done = false;
        break;
      }
    }
    if (done) break;
  }
  return need;
}
const smoothNeed = (arr, loop) => {
  const n = arr.length, at = i => arr[loop ? ((i % n) + n) % n : clamp(i, 0, n - 1)];
  const m = arr.map((_, i) => Math.max(at(i - 2), at(i - 1), at(i), at(i + 1), at(i + 2)));
  const mt = i => m[loop ? ((i % n) + n) % n : clamp(i, 0, n - 1)];
  return m.map((_, i) => (mt(i - 2) + mt(i - 1) + mt(i) + mt(i + 1) + mt(i + 2)) / 5);
};
function guard(poses, S, T, knots) {
  const L = poses.length, loop = !!T.loop, n = loop ? L - 1 : L;
  const hid = p => (S.hidden || []).some(([a, b]) => p >= a && p <= b);
  const allowAt = p => { const a = unwarp(knots, p); return Math.max(0, ...(S.contact || []).filter(([a0, a1]) => a >= a0 && a <= a1).map(c => c[2])); };
  const needs = poses.slice(0, n).map((P, p) => (P.pos[1] < -.6 || hid(p) || S.guard === false ? null : guardNeeds(P, allowAt(p), S.wristCap ?? .16)));
  const ch = (get) => smoothNeed(needs.map(x => (x ? get(x) : 0)), loop);
  const neck = ch(x => x.neck), beard = ch(x => x.beard), apron = ch(x => x.apron), tail = TAILN.map((_, i) => ch(x => x.tail[i])), wl = ch(x => x.fwL), wr = ch(x => x.fwR);
  poses.forEach((P, p) => {
    const j = Math.min(p, n - 1);
    if (!needs[j] && !(neck[j] || beard[j] || apron[j])) { /* blended edges still apply below */ }
    P.neck1 = add(P.neck1, [neck[j], 0, 0]); P.head = add(P.head, [-.55 * neck[j], 0, 0]);
    P.beard1 = add(P.beard1, [-beard[j], 0, 0]); P.beard2 = add(P.beard2, [-.6 * beard[j], 0, 0]);
    P.apron = add(P.apron, [apron[j], 0, 0]);
    P.fwL = add(P.fwL, times(upRoot(P), wl[j])); P.fwR = add(P.fwR, times(upRoot(P), wr[j]));
    TAILN.forEach((t, i) => { P[t] = add(P[t], [-tail[i][j], 0, 0]); });
  });
}

// ---- baking ----------------------------------------------------------------------------------------------------------------
const TAIL_CH = ['tLift', 'tCurl', 'tSweep', 'tTwist'];
const segEuler = (P, i) => {
  const e = P['t' + (i + 1)], up = (i === 0 ? P.tLift : 0) + P.tCurl;
  return [e[0] - up, e[1] + P.tSweep * TAIL_SWEEP[i], e[2] + P.tTwist / 8];
};
// authored time of a played tick (inverse of the piecewise-linear knots)
const unwarp = (knots, p) => {
  if (!knots) return p;
  for (let i = 1; i < knots.length; i++) {
    const [a0, b0] = knots[i - 1], [a1, b1] = knots[i];
    if (p <= b1) return a0 + (a1 - a0) * (p - b0) / (b1 - b0);
  }
  const [a, b] = knots[knots.length - 1];
  return a + (p - b);
};
export const warpT = (knots, a) => {
  if (!knots) return a;
  for (let i = 1; i < knots.length; i++) {
    const [a0, b0] = knots[i - 1], [a1, b1] = knots[i];
    if (a <= a1) return b0 + (b1 - b0) * (a - a0) / (a1 - a0);
  }
  return knots[knots.length - 1][1];
};
// a damped spring driven by the angular acceleration of its parent (deg per tick sequence): the offset of a hanging plate
function spring(drive, {period = 16, zeta = .3, gain = 1, limit = 20, loop = false}) {
  const n = drive.length, w = 2 * Math.PI / period, out = new Array(n).fill(0);
  const acc2 = i => { const a = drive[(i - 1 + n) % n], b = drive[i], c = drive[(i + 1) % n]; return loop || (i > 0 && i < n - 1) ? a - 2 * b + c : 0; };
  let x = 0, v = 0;
  for (let pass = 0; pass < (loop ? 3 : 1); pass++) for (let i = 0; i < n; i++) {
    v += -w * w * x - 2 * zeta * w * v - gain * acc2(i);
    x += v;
    out[i] = limit * Math.tanh(x / limit);
  }
  return out;
}
const sumPitch = (P, chs) => chs.reduce((s, c) => s + (Array.isArray(P[c]) ? P[c][0] : P[c]), 0);

// S: {name, keys, lag, tailLag, feet, yaw (played tick -> deg), drive, over, springs, hidden, state, anchors, tracks, note}
export function bake(S) {
  const T = TABLE[S.name];
  if (!T) throw new Error(`clip ${S.name} is not in the table`);
  const A = T.authored, L = T.len, knots = T.retime;
  if (S.keys[0][0] !== 0 || S.keys[S.keys.length - 1][0] !== A) throw new Error(`clip ${S.name}: keys must run 0..${A} (authored)`);
  const src = {name: S.name, len: A, keys: S.keys};
  const ks = accumulate(src);
  const wrapA = x => (T.loop ? ((x % A) + A) % A : clamp(x, 0, A));
  const at = x => sampleClip(src, wrapA(x), ks);
  const lag = S.lag || {}, tailLag = S.tailLag ?? 1.5;
  const yawAt = p => (S.yaw ? S.yaw[clamp(Math.round(p), 0, S.yaw.length - 1)] : 0);
  const poses = [];
  for (let p = 0; p <= L; p++) {
    const a = unwarp(knots, p);
    const P = at(a);
    for (const [ch, l] of Object.entries(lag)) if (l) P[ch] = structuredClone(at(a - l)[ch]);
    // the tail chain: segment i carries the tail channels of authored time a - tailLag * i
    for (let i = 0; i < 8; i++) P['t' + (i + 1)] = segEuler(i && tailLag ? at(a - tailLag * i) : P, i);
    for (const c of TAIL_CH) P[c] = 0;
    for (const f of S.over || []) f(a, P, p);
    if (S.guard !== false && P.pos[1] > -.6 && !(S.hidden || []).some(([h0, h1]) => p >= h0 && p <= h1)) bodyLift(P);
    // feet
    const d = yawAt(p);
    for (const f of FEET) {
      const F = (S.feet && S.feet[f]) || [[0, 'W', 'rest']];
      const [ch, ech] = FOOT_CH[f];
      const modeAt = (k, a) => {
        const [, mode, arg] = F[k];
        if (mode === 'K') return {T: P[ch], E: P[ech]};
        if (mode === 'R') return {T: arg === 'rest' || !arg ? REST_FEET[f] : arg, E: P[ech]};
        if (mode === 'S') { const B = limbBase(P, f), off = f[1] === 'r' ? mx(arg.off) : arg.off, e = arg.e || [0, 0, 0];
          return {T: add(B.t, rot(B.q, off)), E: eulerOf(mul(B.q, q(f[1] === 'r' ? [e[0], -e[1], -e[2]] : e)))}; }
        if (mode === 'F') { const r = arg(a, p, P); return {T: toRoot(r.A, P), E: rootEuler(r.E || [0, 0, 0], P)}; }
        // 'W': planted in the world (clip-start frame); counter-rotated by the anchor yaw, compensated for the root
        const o = F[k][3] || {};
        const W = add(arg === 'rest' ? restAt(f, o.h || 0) : arg, [0, o.y || 0, 0]);
        const Wd = S.drive ? add(W, [0, 0, S.drive * p]) : W;
        return {T: toRoot(toAnchor(Wd, d), P), E: rootEuler([o.pitch || 0, (o.h || 0) - d, o.roll || 0], P)};
      };
      let k = 0;
      while (k + 1 < F.length && F[k + 1][0] <= a) k++;
      let R;
      if (k + 1 < F.length && a > F[k][0]) {
        const a0 = F[k][0], a1 = F[k + 1][0], u = (a - a0) / (a1 - a0), o = F[k + 1][3] || {};
        const e = EASE[o.ease || 'io'](u), m0 = modeAt(k, a), m1 = modeAt(k + 1, a);
        const arc = Math.sin(Math.PI * clamp(o.peak ? (u < o.peak ? u / o.peak * .5 : .5 + (u - o.peak) / (1 - o.peak) * .5) : u, 0, 1));
        R = {T: add(lerp(m0.T, m1.T, e), times(upRoot(P), (o.lift || 0) * arc)), E: add(lerp(m0.E, m1.E, e), [(o.curl || 0) * arc, 0, 0])};
      } else R = modeAt(k, a);
      P[ch] = R.T;
      P[ech] = R.E;
    }
    poses.push(P);
  }
  // secondary motion: the beard bibs after the head chain, the throat apron after the chest
  if (S.springs !== false) {
    const head = poses.map(P => sumPitch(P, ['rot', 'pelvis', 'spine', 'chest', 'neck1', 'neck2', 'head']) - P.jaw);
    const chest = poses.map(P => sumPitch(P, ['rot', 'pelvis', 'spine', 'chest']));
    const loop = !!T.loop, n = poses.length - (loop ? 1 : 0);
    const b1 = spring(head.slice(0, n), {period: 16, zeta: .28, limit: 18, loop}), b2 = spring(head.slice(0, n), {period: 13, zeta: .24, gain: 1.3, limit: 22, loop});
    const ap = spring(chest.slice(0, n), {period: 18, zeta: .3, gain: .8, limit: 10, loop});
    poses.forEach((P, i) => {
      const j = Math.min(i, n - 1);
      P.beard1 = add(P.beard1, [b1[j], 0, 0]); P.beard2 = add(P.beard2, [b2[j] - b1[j] * .3, 0, 0]); P.apron = add(P.apron, [ap[j], 0, 0]);
    });
  }
  guard(poses, S, T, knots);
  const keys = poses.map((P, p) => [p, P, 'l']);
  return {name: S.name, len: L, loop: !!T.loop, next: T.next, blend: S.blend ?? 3, keys, events: {...T.events}, authoredLen: A, retime: knots || [],
    hidden: S.hidden || [], state: S.state || [], anchors: S.anchors || {}, tracks: TRACK_CLIPS.includes(S.name), yaw: S.yaw || null, note: S.note || '',
    drive: S.drive || 0, plants: S.plants || {}, mirror_of: null, gold: S.gold || [], stateCalls: S.stateCalls || [], floorFree: S.floorFree || []};
}

// ---- mirrors ---------------------------------------------------------------------------------------------------------------
const mE = e => [e[0], -e[1], -e[2]];
const SWAP = {fwL: 'fwR', fwR: 'fwL', fpL: 'fpR', fpR: 'fpL', hkL: 'hkR', hkR: 'hkL', hfL: 'hfR', hfR: 'hfL'};
export function mirrorPose(P) {
  const o = {};
  for (const [k, v] of Object.entries(P)) {
    const dst = SWAP[k] || k;
    if (k === 'pos' || k.startsWith('fw') || k.startsWith('hk')) o[dst] = mx(v);
    else if (Array.isArray(v) && v.length === 3) o[dst] = mE(v);
    else if (k === 'tSweep' || k === 'tTwist') o[dst] = -v;
    else o[dst] = v;
  }
  return o;
}
const PAW_SWAP = {fl: 'fr', fr: 'fl', hl: 'hr', hr: 'hl'};
export function mirrorClip(c, name) {
  return {...c, name, keys: c.keys.map(([t, P, e]) => [t, mirrorPose(P), e]), yaw: c.yaw ? c.yaw.map(v => -v) : null, mirror_of: c.name,
    plants: Object.fromEntries(Object.entries(c.plants || {}).map(([e, f]) => [e, PAW_SWAP[f] || f])),
    anchors: structuredClone(c.anchors), note: `mirror of ${c.name}: ` + c.note};
}

// ---- small helpers for authoring ---------------------------------------------------------------------------------------------
// smoothstep yaw schedule (dense, played ticks; 2 decimals as the stub): 0 until y0, tot at y1
export const turnYaw = (len, y0, y1, tot) => Array.from({length: len}, (_, t) => +(tot * smooth((t - y0) / (y1 - y0))).toFixed(2));
const W = (a, f, h = 0, o = {}) => [a, 'W', 'rest', {h, ...o}];
const Wp = (a, pos, o = {}) => [a, 'W', pos, o];
const Kf = (a, o = {}) => [a, 'K', null, o];
const Rf = (a, o = {}) => [a, 'R', 'rest', o];
const Sf = (a, off, e = [0, 0, 0], o = {}) => [a, 'S', {off, e}, o];   // fixed in the chest (fores) / pelvis (hinds) frame, offset from the shoulder / hip
const breath = (amp = 1.2, period = 80, dy = .05) => (a, P) => {
  const s = Math.sin(2 * Math.PI * a / period);
  P.chest = add(P.chest, [amp * s * .6, 0, 0]); P.spine = add(P.spine, [amp * s * .4, 0, 0]); P.pos = add(P.pos, [0, dy * s, 0]);
  P.neck1 = add(P.neck1, [-amp * s * .4, 0, 0]);
};
// tremor on channels between authored a0..a1 (faded over 4 t at both ends)
const tremor = (a0, a1, amp, period, chs) => (a, P) => {
  if (a < a0 || a > a1) return;
  const f = Math.min(1, (a - a0) / 4, (a1 - a) / 4), s = Math.sin(2 * Math.PI * (a - a0) / period) * amp * f;
  for (const [ch, k] of chs) P[ch] = Array.isArray(P[ch]) ? add(P[ch], [s * k[0], s * (k[1] || 0), s * (k[2] || 0)]) : P[ch] + s * k;
};
// travelling tail wave (yaw), phase lag per segment (ticks)
const tailWave = (amp, period, lagSeg = 3, a0 = -1e9, a1 = 1e9) => (a, P) => {
  if (a < a0 || a > a1) return;
  const f = a0 < -1e8 ? 1 : Math.min(1, (a - a0) / 6, (a1 - a) / 6);
  for (let i = 0; i < 8; i++) P['t' + (i + 1)] = add(P['t' + (i + 1)], [0, amp * f * Math.sin(2 * Math.PI * (a - lagSeg * i) / period) * (i < 2 ? .4 : 1), 0]);
};

// =============================================================================================================================
// The clips (authored ticks; footage = az/understand/motion.md §5 and its key-pose sheets; played events of the table).
// Abbreviations: W(a, foot, heading) = planted at the rest spot of an anchor turned to `heading`, Wp(a, [x,y,z]) =
// planted at a world point (wrist / hock target, rig frame), Kf(a) = the body keys' fw*/hk* target, Rf(a) = riding with
// the root at rest. Key options on the ARRIVING key: lift (b), curl (deg, claws), ease, peak.
const WR = J.wrist, HK = J.hock;
const F_ = (x, y, z) => [x, y, z];
const ups = (a, k = 1) => tailUp(a.map(v => v * k));
const S = [];

// ---- idle: breathing, head drift, the snarl at 30, the tail wave (motion.md §5.1) -------------------------------------------
S.push({name: 'idle', keys: [[0, {jaw: 3}], [30, {jaw: 3}], [40, {jaw: 8, head: [2, 0, 0]}], [50, {jaw: 3}], [80, {jaw: 3}]],
  over: [breath(1.2, 80, .05), (a, P) => { P.head = add(P.head, [2.5 * Math.sin(2 * Math.PI * a / 40), 3 * Math.sin(2 * Math.PI * a / 80), 0]); P.neck2 = add(P.neck2, [0, 1.5 * Math.sin(2 * Math.PI * (a - 6) / 80), 0]); },
    tailWave(4, 80, 3)],
  note: 'breathing (chest +-1.2, root +-0.05, 80 t), head drift (pitch +-2.5 / 40 t, yaw +-3 / 80 t), the snarl (jaw 3 -> 8 -> 3 over 30-50), the tail wave (+-4, 3 t lag per segment), feet planted'});

// ---- pose_ref: the portrait (low roaring crouch, fores braced wide, head thrust forward, jaw 45) -------------------------------
const REF = {pos: [0, -.25, 0], rot: [-2, 0, 0], pelvis: [-2, 0, 0], chest: [3, 0, 0], neck1: [4, 0, 0], neck2: [4, 0, 0], head: [16, 0, 0], jaw: 45,
  flS: 6, flM: 4, ...ups(TAIL_REST, 1.05)};
S.push({name: 'pose_ref', keys: [[0, REF], [20, REF]], feet: {fl: [Wp(0, F_(3.45, .5, -2.6))], fr: [Wp(0, F_(-3.45, .5, -2.6))]},
  over: [tremor(0, 20, .8, 5, [['head', [1]], ['chest', [.5]]])], springs: false,
  note: 'the portrait: a low roaring crouch, the fores braced wide, the head thrust up, jaw 45, the tail high'});

// ---- walk: lateral-sequence walk under the module's glide of 0.13 b/t (plants LH 0, LF 10, RH 20, RF 30; motion.md §5.3) --------
// A foot stands while the anchor glides (it slides back in the anchor frame at the glide speed) and swings forward over the
// rest of the 40-t cycle. Fores stand 22 t (the columnar fore leg reaches +-1.4 b), hinds 26 t; lift 0.6 / 0.45 b.
const gaitFoot = (f, plant, stand, cycle, v, lift, curl, zc = 0) => (a) => {
  const r = REST_FEET[f], half = v * stand / 2;
  const t = ((a - plant) % cycle + cycle) % cycle;           // 0 = plant
  if (t <= stand) return {A: [r[0], r[1], r[2] + zc - half + v * t], E: [0, 0, 0]};
  const u = (t - stand) / (cycle - stand), e = smooth(u);
  return {A: [r[0], r[1] + lift * Math.sin(Math.PI * u), r[2] + zc + half - 2 * half * e], E: [curl * Math.sin(Math.PI * u), 0, 0]};
};
{
  const v = .13, base = {pos: [0, -.12, 0], neck1: [8, 0, 0], neck2: [4, 0, 0], head: [-6, 0, 0]};
  const plantDip = (a, P) => {
    let dy = 0;
    for (const tp of [10, 30]) { const d = ((a - tp) % 40 + 40) % 40; dy -= .06 * Math.exp(-(((d - 2) / 3) ** 2)); }
    const w = 2 * Math.PI * a / 40;
    P.pos = add(P.pos, [0, dy - .04 * Math.cos(2 * w), 0]);
    P.chest = add(P.chest, [0, -1.5 * Math.sin(w), 1.5 * Math.sin(w - 1)]);
    P.spine = add(P.spine, [0, 2.5 * Math.sin(w), 0]);
    P.pelvis = add(P.pelvis, [0, -1.2 * Math.sin(w - .6), -1 * Math.sin(w - 1.6)]);
    P.neck1 = add(P.neck1, [1.2 * Math.sin(2 * w - 1.4), -1.5 * Math.sin(w), 0]);
    P.head = add(P.head, [-1.2 * Math.sin(2 * w - 1.9), 0, 0]);
  };
  S.push({name: 'walk', keys: [[0, base], [40, base]], drive: 0,
    feet: {hl: [[0, 'F', gaitFoot('hl', 0, 22, 40, v, .45, -15, -.3)]], fl: [[0, 'F', gaitFoot('fl', 10, 22, 40, v, .6, -25, .1)]],
      hr: [[0, 'F', gaitFoot('hr', 20, 22, 40, v, .45, -15, -.3)]], fr: [[0, 'F', gaitFoot('fr', 30, 22, 40, v, .6, -25, .1)]]},
    over: [plantDip, tailWave(5, 40, 2)], plants: {lh: 'hl', lf: 'fl', rh: 'hr', rf: 'fr'},
    note: 'lateral-sequence walk for the module glide of 0.13 b/t (stride 5.2 b): plants LH 0, LF 10, RH 20, RF 30, fore lift 0.6, hind 0.45; root -0.12 with a dip after each fore plant, chest roll +-1.5, spine yaw +-2.5 against the chest, a head counter-bob, the tail swinging +-5'});
}
// ---- walk_stop: the last fore plants at 4, the others square up, the body pitches forward 2 and settles ----------------------
{
  const r = REST_FEET;
  S.push({name: 'walk_stop', keys: [[0, {pos: [0, -.12, 0], neck1: [8, 0, 0], neck2: [4, 0, 0], head: [-6, 0, 0]}], [4, {rot: [-2, 0, 0], pos: [0, -.18, 0], head: [-8, 0, 0], neck1: [5, 0, 0]}, 'i'],
    [9, {rot: [.5, 0, 0], pos: [0, -.02, 0], head: [2, 0, 0], neck1: [2, 0, 0]}, 'o'], [16, {rot: [0, 0, 0], pos: [0, 0, 0], head: [0, 0, 0], neck1: [0, 0, 0], neck2: [0, 0, 0]}]],
    feet: {fr: [Wp(0, add(r.fr, [0, .35, 1.1])), Wp(4, r.fr, {ease: 'i'})],
      fl: [Wp(0, add(r.fl, [0, 0, -.7])), Wp(8, add(r.fl, [0, 0, -.7])), Wp(13, r.fl, {lift: .35, curl: -15})],
      hl: [Wp(0, add(r.hl, [0, 0, 1.0])), Wp(5, add(r.hl, [0, 0, 1.0])), Wp(11, r.hl, {lift: .35, curl: -10})],
      hr: [Wp(0, add(r.hr, [0, 0, -.8])), Wp(9, add(r.hr, [0, 0, -.8])), Wp(14, r.hr, {lift: .3, curl: -10})]},
    over: [tailWave(5, 24, 2, 0, 16)], plants: {plant: 'fr'},
    note: 'from the walk: the right fore plants at 4 (the last stride), the left fore and both hinds square up 5-14, the body pitches forward 2 and settles, the head bobs once, the tail swings through'});
}

// ---- turns: diagonal pairs step in turn while the anchor yaws by the exported schedule; every planted foot is
// counter-rotated (it stays put in the world), every step lands on the rest spot of a heading a little ahead of the
// anchor, the last steps on the final heading (motion.md §5.2; contract §4.5: _l turns toward the boss's left, negative).
// pairs: A = the outer fore + the inner hind, B = the inner fore + the outer hind (left turn: outer = right side).
function turnFeet(steps, dur) {
  const feet = {fl: [W(0, 'fl', 0)], fr: [W(0, 'fr', 0)], hl: [W(0, 'hl', 0)], hr: [W(0, 'hr', 0)]};
  const pair = {A: ['fr', 'hl'], B: ['fl', 'hr']};
  for (const [land, p, h] of steps) for (const f of pair[p]) {
    const prev = feet[f][feet[f].length - 1], fore = f[0] === 'f';
    feet[f].push(W(land - dur, f, prev[3].h), W(land, f, h, {lift: fore ? .55 : .45, curl: fore ? -25 : -15, peak: .4}));
  }
  return feet;
}
function turnClip(name, total, steps, dur, head, note) {
  const T = TABLE[name], y = turnYaw(T.len, T.events.yaw0, T.events.yaw1, total);
  const s = Math.sign(total), [y0, y1] = [T.events.yaw0, T.events.yaw1], L = T.len;
  const lead = {neck1: [0, s * head * .3, 0], neck2: [0, s * head * .3, 0], head: [-3, s * head * .4, 0], chest: [0, s * head * .12, 0]};
  const keys = [[0, {}], [Math.max(2, y0 - 2), lead, 'io'], [Math.round((y0 + y1) / 2), {...lead, pos: [0, -.08, 0], pelvis: [0, -s * 4, 0]}],
    [y1, {neck1: [0, -s * 2, 0], neck2: [0, -s * 2, 0], head: [1, -s * 3, 0], chest: [0, 0, 0], pos: [0, -.04, 0], pelvis: [0, s * 2, 0]}, 'o'], [L, {}]];
  // the tail drags outward while the anchor turns (a lagging tail shows on the side the turn comes from), then swings through
  const drag = (a, P) => {
    const k = Math.max(0, Math.min(1, (a - y0) / (y1 - y0)));
    const lagv = Math.sin(Math.PI * k) * 18 - (a > y1 ? Math.sin(Math.PI * Math.min(1, (a - y1) / Math.max(4, L - y1))) * 7 : 0);
    for (let i = 0; i < 8; i++) P['t' + (i + 1)] = add(P['t' + (i + 1)], [0, -s * lagv * (.06 + .02 * i), 0]);
  };
  return {name, keys, yaw: y, feet: turnFeet(steps, dur), over: [drag], lag: {pelvis: 3, spine: 2, chest: 1},
    plants: Object.fromEntries(steps.map(([land, p], i) => [`plant_${i + 1}`, p === 'A' ? 'fr' : 'fl'])), note};
}
S.push(turnClip('turn45_l', -45, [[10, 'A', -45], [17, 'B', -45]], 6, 14,
  'a 45 degree turn to its left in two diagonal steps (the outer fore + the inner hind at 10, then the other pair at 17), the head leading 14 degrees, the pelvis 3 t behind, the tail dragging out and swinging through'));
S.push(turnClip('turn90_l', -90, [[12, 'A', -35], [18, 'B', -65], [24, 'A', -90], [30, 'B', -90]], 6, 22,
  'a 90 degree turn to its left in four diagonal steps (12, 18, 24, 30), the head leading 22 degrees'));
S.push(turnClip('turn180', -180, [[12, 'A', -18], [18, 'B', -45], [24, 'A', -78], [30, 'B', -110], [36, 'A', -140], [42, 'B', -163], [48, 'A', -180], [54, 'B', -180]], 6, 40,
  'a 180 degree turn to its left in eight diagonal steps (12 ... 54, each foot four times), the head leading 40 degrees (the module mirrors the sign for the other way)'));

// ---- the rear-up family (roar_rear, chin_slam, intro, landslide wave 6, absorb ends): the pelvis pitches up about the hip
// line, the hind feet stay planted, the fore paws leave the floor with the chest (keyed in the root frame), the tail root
// braces on the floor as a third leg.
// (R3b, r3_critique 3.3 / 10: the apron swings toward the vertical as the chest rears, so the glyph panel covers the rearing
// chest down toward the belly instead of lying flat under the jaw)
const REAR = (deg, o = {}) => ({pelvis: [deg, 0, 0], spine: [deg * .1, 0, 0], chest: [deg * .07, 0, 0], apron: [-.8 * deg, 0, 0], ...ups(TAIL_BRACE, Math.min(1, deg / 50)), ...o});
// fore wrists folded up and out at chest height (root frame) for a pelvis pitch of about 40-60
const FORE_UP = (y = 5.6, z = -3.0, x = 3.3, e = [-55, 0, -10]) => fore([x, y, z], e);
// (R3b, r3_critique 10: in the roar_rear / intro rear-ups the fores hang down and a little forward from the shoulders with
// the paws curled (chest-frame offsets [1.5, -1.65, 1.9] / [1.45, -1.85, 1.7]: about 2.4 b below the shoulder in the world),
// the bracers within ~30 degrees of the body axis, no longer raised across the throat and the face)

// ---- intro (150): sealed crouch, eyes 25, rise 30, rear-up roar, cracks 50 / 70, drop, land 116, low roar 120, blast 130 ---------
{
  const crouch = {pos: [0, -.35, 0], rot: [-2, 0, 0], neck1: [-3, 0, 0], neck2: [-2, 0, 0], head: [2, 0, 0], flS: -3, flM: -3, ...ups(TAIL_REST, .82)};
  const rear = REAR(48, {neck1: [-12, 0, 0], neck2: [2, 0, 0], head: [24, 0, 0], jaw: 30, flS: 10, flM: 8, ...FORE_UP(5.4, -3.2, 3.4)});
  S.push({name: 'intro', keys: [[0, crouch], [24, crouch], [26, {head: [5, 0, 0]}], [32, {pos: [0, -.55, 0], head: [8, 0, 0], neck1: [0, 0, 0]}, 'io'],
    [56, {...rear, pos: [0, 0, 0], rot: [0, 0, 0]}, 'o'], [62, {jaw: 42}], [96, {jaw: 40, head: [20, 0, 0]}], [100, {jaw: 12}],
    [114, {...REAR(4, {neck1: [-4, 0, 0], neck2: [0, 0, 0], head: [-4, 0, 0], jaw: 8, flS: 4, flM: 4}), ...ups(TAIL_REST, .9)}, 'i'],
    [119, {pos: [0, -.32, 0], chest: [-3, 0, 0], head: [-6, 0, 0]}, 'o'],
    [124, {pos: [0, -.25, 0], chest: [2, 0, 0], neck1: [6, 0, 0], neck2: [4, 0, 0], head: [22, 0, 0], jaw: 50, pelvis: [-3, 0, 0]}, 'o'],
    [134, {jaw: 46}], [140, {jaw: 12, head: [6, 0, 0], neck1: [2, 0, 0]}], [150, {pos: [0, 0, 0], chest: [0, 0, 0], neck1: [0, 0, 0], neck2: [0, 0, 0], head: [0, 0, 0], jaw: 3, pelvis: [0, 0, 0], flS: 0, flM: 0}]],
    feet: {fl: [W(0, 'fl'), W(32, 'fl'), Sf(40, [1.45, -1.85, 1.7], [-32, 0, -12]), Sf(108, [1.45, -1.85, 1.7], [-32, 0, -12]), W(116, 'fl', 0, {ease: 'i'})],
      fr: [W(0, 'fr'), W(32, 'fr'), Sf(41, [1.45, -1.85, 1.7], [-32, 0, -12]), Sf(108, [1.45, -1.85, 1.7], [-32, 0, -12]), W(116, 'fr', 0, {ease: 'i'})]},
    over: [tremor(58, 100, 1.6, 4, [['chest', [1]], ['head', [1.2, .6]], ['jaw', 2]]), tremor(124, 136, 1.2, 4, [['head', [1]], ['jaw', 2]])],
    lag: {pelvis: 2}, note: 'sealed crouch, still (0-30); a dip, then the rear-up (pelvis +48, 32-56) with the fores folded at chest height; the rear-up roar held with a tremor (58-100); the drop to all fours, fores landing at 116; the low roar (jaw 50, head thrust up) 120-136; settle into idle by 150'});
}
// ---- roar_low (50 -> 40): back onto the haunches, fores braced, head thrust up, roar 10, blast 12, hold, close -----------------
{
  const roar = {pos: [0, -.25, 0], pelvis: [6, 0, 0], chest: [2, 0, 0], neck1: [6, 0, 0], neck2: [5, 0, 0], head: [20, 0, 0], jaw: 50, flS: 8, flM: 6, flN: 6};
  S.push({name: 'roar_low', keys: [[0, {}], [10, {...roar, jaw: 46}, 'o'], [12, roar], [34, {...roar, jaw: 48}], [44, {jaw: 8, head: [4, 0, 0], neck1: [2, 0, 0], pelvis: [1, 0, 0], pos: [0, -.06, 0], flS: 1, flM: 1, flN: 1}],
    [50, {pos: [0, 0, 0], pelvis: [0, 0, 0], chest: [0, 0, 0], neck1: [0, 0, 0], neck2: [0, 0, 0], head: [0, 0, 0], jaw: 3, flS: 0, flM: 0, flN: 0}]],
    feet: {fl: [W(0, 'fl'), W(2, 'fl'), Wp(8, F_(3.5, .5, -2.65), {lift: .2})], fr: [W(0, 'fr'), W(3, 'fr'), Wp(9, F_(-3.5, .5, -2.65), {lift: .2})]},
    over: [tremor(12, 36, 1.4, 4, [['chest', [1]], ['head', [1.2, .5]], ['jaw', 2.5]])], anchors: {roar: ['nose']},
    note: 'the body pushes back onto the haunches (root -0.25, pelvis +6), the fores step out wide, the head thrusts up 20; roar at 10 (jaw 50), the blast at 12, a held tremor to 36, close and settle'});
}
// ---- roar_rear (100 -> 82): load, rise 8-20 (pelvis +55), roar 20, hold with tremor, drop, fores land 90 -----------------------
{
  const top = REAR(55, {neck1: [-14, 0, 0], neck2: [0, 0, 0], head: [26, 0, 0], jaw: 46, flS: 14, flM: 12, flN: 10, flH: 8, ...FORE_UP(5.6, -3.0, 3.5, [-50, 0, -15])});
  S.push({name: 'roar_rear', keys: [[0, {}], [8, {pos: [0, -.3, 0], neck1: [-4, 0, 0], head: [-6, 0, 0], pelvis: [-3, 0, 0], ...ups(TAIL_LOW, .5)}, 'io'],
    [20, top, 'o'], [74, {...top, jaw: 40}], [76, {...top, jaw: 30}],
    [89, {...REAR(2, {neck1: [-3, 0, 0], neck2: [0, 0, 0], head: [-6, 0, 0], jaw: 10, flS: 6, flM: 6, flN: 4, flH: 4}), ...ups(TAIL_REST, .9)}, 'i'],
    [92, {pos: [0, -.35, 0], chest: [-3, 0, 0], head: [-9, 0, 0]}, 'o'], [100, {pos: [0, 0, 0], pelvis: [0, 0, 0], spine: [0, 0, 0], chest: [0, 0, 0], neck1: [0, 0, 0], head: [0, 0, 0], jaw: 3, flS: 0, flM: 0, flN: 0, flH: 0, ...tailUp(TAIL_REST)}]],
    feet: {fl: [W(0, 'fl'), W(8, 'fl'), Sf(13, [1.5, -1.65, 1.9], [-35, 0, -14]), Sf(84, [1.5, -1.65, 1.9], [-35, 0, -14]), W(90, 'fl', 0, {ease: 'i'})],
      fr: [W(0, 'fr'), W(8, 'fr'), Sf(14, [1.5, -1.65, 1.9], [-35, 0, -14]), Sf(84, [1.5, -1.65, 1.9], [-35, 0, -14]), W(90, 'fr', 0, {ease: 'i'})]},
    over: [tremor(22, 74, 1.5, 4, [['chest', [1]], ['head', [1, .6]], ['jaw', 2]]), tremor(92, 100, 2.5, 8, [['head', [0, 1]]])],
    lag: {pelvis: 2}, anchors: {roar: ['nose']}, note: 'load (root -0.3, head down, tail pressed), the rise 8-20 (pelvis +55, the fores leave the floor at 12 and fold up and out at chest height, head thrown back, jaw 46), roar at 20, the hold with a 4-t tremor and the tail braced, the drop 76-89, fores land at 90, compression, a head shake'});
}

// ---- chin_slam (84 -> 65): anticipation (head up and to its left, jaw snarl), rear-up 14-22 (pelvis +48, the left fore
// highest: the wiki tell), hold looking down 22-42, the slam 42-47 (the chin into the floor 6-7 b ahead), impact 47,
// compression, the head low to played 55 (head column top <= 3.5), the head lifting last (motion.md §5.5, v2 E).
{
  const up = REAR(48, {t1: [-52, 0, 0], neck1: [-8, 0, 0], neck2: [-4, 0, 0], head: [-24, 0, 0], jaw: 14, flS: 10, flM: 8, flN: 6,
    fwL: [3.4, 5.8, -3.3], fpL: [-60, 0, -14], fwR: [-3.3, 5.0, -3.4], fpR: [-50, 0, 12]});
  const hit = {pos: [0, -.3, 0], rot: [-9, 0, 0], pelvis: [-2, 0, 0], spine: [-2, 0, 0], chest: [-3, 0, 0], neck1: [26, 0, 0], neck2: [6, 0, 0], head: [-4, 0, 0], jaw: 0,
    beard1: [-28, 0, 0], beard2: [-16, 0, 0], apron: [10, 0, 0], flS: 8, flM: 8, flN: 10, ...ups(TAIL_REST, .85)};
  S.push({name: 'chin_slam', keys: [[0, {}], [3, {pos: [0, -.08, 0]}], [14, {pos: [0, -.18, 0], pelvis: [-3, 0, 0], neck1: [10, -8, 0], neck2: [6, -6, 0], head: [16, -12, 0], jaw: 18}, 'io'],
    [22, up, 'o'], [30, {...up, head: [-26, 0, 0]}], [41, {...up, pelvis: [50, 0, 0], head: [-22, 0, 0], jaw: 10}, 'io'],
    [47, hit, 'i'], [50, {...hit, pos: [0, -.38, 0], neck1: [24, 0, 0], head: [-6, 0, 0], spine: [-4, 0, 0]}, 'o'],
    [70, {...hit, pos: [0, -.18, 0], rot: [-5, 0, 0], neck1: [18, 0, 0], neck2: [4, 0, 0], head: [-2, 0, 0], beard1: [-8, 0, 0], beard2: [-6, 0, 0], apron: [4, 0, 0], flS: 3, flM: 3, flN: 3}, 'o'],
    [84, {pos: [0, 0, 0], rot: [0, 0, 0], pelvis: [0, 0, 0], spine: [0, 0, 0], chest: [0, 0, 0], neck1: [0, 0, 0], neck2: [0, 0, 0], head: [0, 0, 0], jaw: 3,
      beard1: [0, 0, 0], beard2: [0, 0, 0], apron: [0, 0, 0], flS: 0, flM: 0, flN: 0, ...tailUp(TAIL_REST)}, 'io']],
    feet: {fl: [W(0, 'fl'), W(13, 'fl'), Sf(18, [1.25, -1.6, .7], [-35, 0, -14]), Sf(41, [1.25, -1.6, .7], [-35, 0, -14]), Wp(47, F_(3.3, .5, -2.7), {ease: 'i'})],
      fr: [W(0, 'fr'), W(13, 'fr'), Sf(18, [1.15, -2.2, .9], [-25, 0, -10]), Sf(41, [1.15, -2.2, .9], [-25, 0, -10]), Wp(47, F_(-3.3, .5, -2.7), {ease: 'i'})]},
    over: [tremor(22, 41, 1.2, 10, [['rot', [0, 0, 1]], ['head', [.6, .8]]])], lag: {head: 1}, contact: [[45, 54, .22]],
    anchors: {impact: ['impact', 'nose']},
    note: 'anticipation 0-14 (head up and to its left, jaw 18, weight back), the rear-up 14-22 (pelvis +48, the left fore highest), the hold 22-41 looking down with a sway, the slam 41-47 (ease in: the chin into the floor, the neck stretched), impact at 47, compression to 50, the head kept low to 70 (played 55), recovered by 84'});
}
// ---- jump_slam (60 -> 53): crouch 0-6, take-off 8, apex 18, fores land 28 (wave 1), the hinds 39 (wave 2). The module raises
// and glides the anchor (mv/leap, played 6 -> 21); the clip only poses (no root height in the air).
{
  const crouch = {pos: [0, -.55, 0], rot: [-3, 0, 0], pelvis: [-5, 0, 0], neck1: [6, 0, 0], head: [-4, 0, 0], jaw: 8, ...ups(TAIL_LOW, .6)};
  const air = {pos: [0, 0, 0], rot: [9, 0, 0], pelvis: [-4, 0, 0], neck1: [10, 0, 0], neck2: [4, 0, 0], head: [-10, 0, 0], jaw: 20, flS: 8, flM: 8,
    ...fore([3.2, .7, -3.6], [-30, 0, 0]), ...hind([2.5, 1.0, 4.2], [30, 0, 0]), ...ups(TAIL_LOW, .4)};
  const fall = {...air, rot: [-12, 0, 0], neck1: [4, 0, 0], head: [-6, 0, 0], jaw: 12, ...fore([3.3, .3, -3.0], [-8, 0, 0]), ...hind([2.5, 1.6, 4.0], [20, 0, 0]), ...ups(TAIL_REST, .6)};
  const land = {pos: [0, -.45, 0], rot: [-8, 0, 0], pelvis: [6, 0, 0], neck1: [10, 0, 0], neck2: [4, 0, 0], head: [-6, 0, 0], jaw: 6, flS: 10, flM: 10, flH: 8,
    ...hind([2.5, 2.5, 3.6], [24, 0, 0]), ...ups(TAIL_REST, .92)};
  S.push({name: 'jump_slam', floorFree: [[7, 20]], keys: [[0, {}], [6, crouch, 'io'], [8, {...crouch, rot: [6, 0, 0], pelvis: [-8, 0, 0], neck1: [10, 0, 0], head: [0, 0, 0]}, 'o'],
    [12, air, 'o'], [18, {...air, rot: [2, 0, 0]}], [27, fall, 'i'], [28, land, 'i'], [32, {...land, pos: [0, -.55, 0], chest: [-3, 0, 0]}, 'o'],
    [37, {...land, pos: [0, -.25, 0], rot: [-4, 0, 0], ...hind([2.5, 2.0, 3.2], [16, 0, 0])}], [39, {pos: [0, -.42, 0], rot: [0, 0, 0], pelvis: [-2, 0, 0], ...hind(HK)}, 'i'],
    [43, {pos: [0, -.3, 0], flS: 4, flM: 4, flH: 4}, 'o'], [60, {pos: [0, 0, 0], rot: [0, 0, 0], pelvis: [0, 0, 0], neck1: [0, 0, 0], neck2: [0, 0, 0], head: [0, 0, 0], jaw: 3, flS: 0, flM: 0, flH: 0, ...tailUp(TAIL_REST)}, 'io']],
    feet: {fl: [W(0, 'fl'), W(7, 'fl'), Sf(12, [.95, -2.6, -1.3], [-30, 0, 0]), Sf(25, [1.0, -2.85, -.9], [-10, 0, 0]), Wp(28, F_(3.3, .5, -2.6), {ease: 'i'}), Wp(46, F_(3.3, .5, -2.6)), W(52, 'fl', 0, {lift: .25})],
      fr: [W(0, 'fr'), W(7, 'fr'), Sf(12, [.95, -2.6, -1.3], [-30, 0, 0]), Sf(25, [1.0, -2.85, -.9], [-10, 0, 0]), Wp(28, F_(-3.3, .5, -2.6), {ease: 'i'}), Wp(48, F_(-3.3, .5, -2.6)), W(54, 'fr', 0, {lift: .25})],
      hl: [W(0, 'hl'), W(8, 'hl'), Sf(12, [.5, -1.0, 1.3], [30, 0, 0]), Sf(30, [.5, -1.1, 1.0], [24, 0, 0]), Sf(36, [.5, -1.3, .6], [10, 0, 0]), W(39, 'hl', 0, {ease: 'i'})],
      hr: [W(0, 'hr'), W(8, 'hr'), Sf(12, [.5, -1.0, 1.3], [30, 0, 0]), Sf(30, [.5, -1.1, 1.0], [24, 0, 0]), Sf(36, [.5, -1.3, .6], [10, 0, 0]), W(39, 'hr', 0, {ease: 'i'})]},
    lag: {head: 1, pelvis: 1}, anchors: {land: ['nose'], wave2: ['nose']},
    note: 'deep crouch 0-6 (root -0.55), the front lifts and the hinds push at 8 (take-off), the body pitched up +16 rising, level at the apex, nose down falling with the fores reaching; the fores and chest land at 28 (wave 1, compression), the rear comes down with a heave, the hinds land at 39 (wave 2); settle, the head up last'});
}

// ---- charge: coil (a lateral C toward its right flank, the right shoulder dropped, root -0.4, the tail swung round), a
// low bound gallop under the module's 1.0 b/t glide, the skid (motion.md §5.7, v3 G).
{
  const coil = {pos: [0, -.3, 0], rot: [-3, 0, 2], pelvis: [0, -8, 2], spine: [0, 14, 2], chest: [-2, 18, 4], neck1: [-2, 14, 0], neck2: [0, 10, 0], head: [-6, 8, 4], jaw: 14,
    flS: 6, flM: 6, flH: 4, tSweep: -55, ...ups(TAIL_REST, .7)};
  S.push({name: 'charge_coil', wristCap: .35, keys: [[0, {}], [8, {pos: [0, -.15, 0], neck1: [-3, 0, 0], head: [-8, 0, 0], jaw: 10}, 'io'], [14, coil, 'io'], [31, {...coil, jaw: 18}],
    [34, {pos: [0, -.3, 0], rot: [-6, 0, 0], pelvis: [4, 0, 0], spine: [0, 6, 0], chest: [-2, 6, 0], neck1: [2, 6, 0], neck2: [0, 4, 0], head: [-12, 6, 0], jaw: 22, flS: 4, flM: 4, flH: 4,
      tSweep: -15, ...ups(TAIL_LOW, .8)}, 'i']],
    feet: {fl: [W(0, 'fl'), W(31, 'fl'), Wp(34, F_(3.25, .5, -3.0), {lift: .3})], fr: [W(0, 'fr'), W(30, 'fr'), Wp(34, F_(-3.25, .5, -3.2), {lift: .3})]},
    over: [tremor(16, 31, 1.2, 3, [['chest', [.6, 1, .6]], ['head', [0, 1.4, 0]], ['jaw', 2]])], lag: {pelvis: 3, spine: 1}, tailLag: 2,
    note: 'the head lowers (0-8), the lateral C-curl to its right flank 8-14 (spine / chest / neck yaw, the right shoulder dropped, root -0.4, the tail swung round), a trembling hold to 31 (the tell), the release 31-34 (launch at 32: the body straightens low, the fores reach)'});
  // gallop: hinds push 0-3 (the right 1 t later), fores land 6 (the right at 7) and stand 3 t; the glide of 1.0 b/t slides the
  // standing feet back 3 b; the swing carries them forward with a 0.8 / 0.6 b lift
  const v = 1.0, run = {pos: [0, -.3, 0], rot: [-3, 0, 0], neck1: [-4, 6, 0], neck2: [-2, 5, 0], head: [-12, 5, 0], jaw: 12, flS: 2, flM: 2, ...ups(TAIL_LOW, .9)};
  const bob = (a, P) => {
    const w = 2 * Math.PI * a / 12;
    P.pos = add(P.pos, [0, .22 * Math.cos(w - 1.2), 0]);
    P.rot = add(P.rot, [5 * Math.sin(w - .3), 0, 0]);
    P.spine = add(P.spine, [-3 * Math.sin(w + .8), 0, 0]);
    P.neck1 = add(P.neck1, [2 * Math.sin(w - 1.5), 0, 0]);
  };
  S.push({name: 'charge_run', wristCap: .3, keys: [[0, run], [12, run]], over: [bob, tailWave(4, 12, 1)],
    feet: {hl: [[0, 'F', gaitFoot('hl', 0, 3, 12, v, .35, -20, -.2)]], hr: [[0, 'F', gaitFoot('hr', 1, 3, 12, v, .35, -20, -.2)]],
      fl: [[0, 'F', gaitFoot('fl', 6, 3, 12, v, .8, -35, -.3)]], fr: [[0, 'F', gaitFoot('fr', 7, 3, 12, v, .8, -35, -.3)]]},
    plants: {plant: 'fl'}, springs: true,
    note: 'a low bound gallop (12 t) under the module glide of 1.0 b/t: hinds push 0-3, fores land at 6 / 7 and stand 3 t, body pitch +-5, root +-0.22 about -0.3, head low with the horns forward and still turned 5 degrees to the curl side, the tail streaming low'});
  S.push({name: 'charge_stop', wristCap: .3, keys: [[0, {...run, pelvis: [0, 10, 0]}], [6, {pos: [0, -.38, 0], rot: [-5, 0, -3], pelvis: [2, 22, -2], spine: [0, -8, 0], chest: [-2, -4, 0], neck1: [2, -4, 0], head: [-4, -6, 0], jaw: 16, tSweep: 30, ...ups(TAIL_LOW, .6)}, 'o'],
    [8, {pos: [0, -.42, 0], rot: [-6, 0, -3]}], [16, {pos: [0, -.1, 0], rot: [1, 0, 0], pelvis: [0, 6, 0], spine: [0, -2, 0], chest: [0, 0, 0], neck1: [4, 0, 0], neck2: [2, 0, 0], head: [4, 0, 0], jaw: 6, tSweep: -10, ...ups(TAIL_REST, .85)}, 'io'],
    [24, {pos: [0, 0, 0], rot: [0, 0, 0], pelvis: [0, 0, 0], spine: [0, 0, 0], neck1: [0, 0, 0], neck2: [0, 0, 0], head: [0, 0, 0], jaw: 3, flS: 0, flM: 0, tSweep: 0, ...tailUp(TAIL_REST)}]],
    feet: {fl: [Wp(0, F_(3.3, .5, -3.4)), Wp(10, F_(3.3, .5, -3.4)), W(16, 'fl', 0, {lift: .45, curl: -20})], fr: [Wp(0, F_(-3.3, .5, -3.6)), Wp(12, F_(-3.3, .5, -3.6)), W(18, 'fr', 0, {lift: .45, curl: -20})],
      hl: [Wp(0, F_(3.2, 1.5, 2.2)), Wp(13, F_(3.2, 1.5, 2.2)), W(19, 'hl', 0, {lift: .4, curl: -12})], hr: [Wp(0, F_(-1.6, 1.5, 3.8)), Wp(15, F_(-1.6, 1.5, 3.8)), W(21, 'hr', 0, {lift: .4, curl: -12})]},
    tailLag: 2.5, lag: {pelvis: 1},
    note: 'the skid 0-8 (fores braced forward, the rear swung out by pelvis yaw +22, root -0.4), stop at 8, the recovery 8-24 (the feet square up one by one, the head lifts, the tail swings through)'});
}
// ---- spikes / 천동만상 (48 -> 40): brace 0-14 (crouch, back humped, plates bristling), heave 16-18, launch 18, launch_last 24,
// relax, settle (motion.md §5.8, v1 C); the gold flares 15 from gold_on to gold_off (glow/gold_*).
{
  const brace = {pos: [0, -.35, 0], rot: [-2, 0, 0], pelvis: [3, 0, 0], spine: [5, 0, 0], chest: [-7, 0, 0], neck1: [8, 0, 0], neck2: [2, 0, 0], head: [-4, 0, 0], jaw: 6,
    flN: 8, flS: 12, flM: 12, flH: 10, flK: 1.04};
  S.push({name: 'spikes', keys: [[0, {}], [10, brace, 'io'], [15, {...brace, flS: 16, flM: 16, flH: 13, flN: 10}], [18, {...brace, pos: [0, -.18, 0], spine: [8, 0, 0], chest: [-4, 0, 0], neck1: [12, 0, 0], head: [4, 0, 0], jaw: 24, flS: 22, flM: 22, flH: 18, flN: 14, flK: 1.1}, 'o'],
    [24, {pos: [0, -.25, 0], spine: [6, 0, 0], jaw: 18, flS: 20, flM: 20, flH: 16, flK: 1.08}], [34, {pos: [0, -.1, 0], pelvis: [1, 0, 0], spine: [2, 0, 0], chest: [-2, 0, 0], neck1: [3, 0, 0], head: [0, 0, 0], jaw: 5, flN: 3, flS: 4, flM: 4, flH: 3, flK: 1.02}, 'io'],
    [48, {pos: [0, 0, 0], rot: [0, 0, 0], pelvis: [0, 0, 0], spine: [0, 0, 0], chest: [0, 0, 0], neck1: [0, 0, 0], neck2: [0, 0, 0], head: [0, 0, 0], jaw: 3, flN: 0, flS: 0, flM: 0, flH: 0, flK: 1}]],
    over: [tremor(10, 18, .8, 3, [['flM', 1.5], ['flS', 1.5], ['chest', [.5]]])],
    anchors: {launch: ['launch_1', 'launch_2', 'launch_3', 'launch_4'], launch_last: ['launch_4']}, gold: [['gold_on', 'on'], ['gold_off', 'off']],
    note: 'brace 0-14 (crouch root -0.35, back humped, the plates bristling +12 with a shiver), the heave 15-18 (flare +22, scale 1.1, jaw open), the launch at 18, the secondary burst at 24, relax 24-34, settle by 48'});
}

// ---- stomps / 산명곡응 (72 -> 63): weight shift away 0-6, the lift 6-15 (the paw to the hang: elbow high, the front up and
// rolled away, head toward the foot), the hang 15-17 (the tell), the slam 17-22 (ease in) = wave 1, compression, waves 2
// and 3 at 37 / 52 as shoulder pushes, recover (motion.md §5.9, v3 K). The hind variant lifts the hock knee-high, rolls the
// pelvis away and swings the tail to the other side.
{
  const shift = {rot: [0, 0, 4], chest: [0, 0, 4], pos: [0, -.06, 0]};
  const hang = {rot: [0, 0, 5], pelvis: [3, 0, 0], chest: [6, 0, 9], neck1: [2, -6, 0], neck2: [2, -4, 0], head: [2, -10, 0], jaw: 10,
    fwL: [3.5, 2.95, -2.85], fpL: [-34, 0, 0], flS: 6, flM: 4};
  const slam = {rot: [-2, 0, 1], pos: [0, -.22, 0], pelvis: [0, 0, 0], chest: [-4, 0, 2], neck1: [-2, -4, 0], neck2: [0, -2, 0], head: [-5, -6, 0], jaw: 16, flS: 10, flM: 8};
  const push = (a) => [[a - 3, {chest: [-1, 0, 1], pos: [0, -.1, 0]}], [a, {chest: [-4, 0, 1], pos: [0, -.2, 0], head: [-6, -4, 0], jaw: 14}, 'i'], [a + 4, {chest: [-1, 0, 1], pos: [0, -.1, 0], head: [-3, -4, 0], jaw: 8}, 'o']];
  S.push({name: 'stomp_fl', keys: [[0, {}], [6, shift, 'io'], [15, hang, 'o'], [17, {...hang, fwL: [3.5, 3.05, -2.88]}], [22, slam, 'i'], [26, {...slam, pos: [0, -.14, 0], chest: [-2, 0, 1], head: [-3, -5, 0]}, 'o'],
    ...push(37), ...push(52), [72, {rot: [0, 0, 0], pos: [0, 0, 0], chest: [0, 0, 0], neck1: [0, 0, 0], neck2: [0, 0, 0], head: [0, 0, 0], jaw: 3, flS: 0, flM: 0}, 'io']],
    feet: {fl: [W(0, 'fl'), W(6, 'fl'), Kf(15, {ease: 'o'}), Kf(17), Wp(22, F_(3.3, .5, -2.55), {ease: 'i'}), Wp(60, F_(3.3, .5, -2.55)), W(68, 'fl', 0, {lift: .2})]},
    over: [tremor(22, 30, 1.5, 3, [['chest', [.6]], ['flM', 2], ['flS', 2]])], lag: {pelvis: 2, head: 1},
    anchors: {slam: ['paw'], w1: ['paw'], w2: ['paw'], w3: ['paw']}, plants: {slam: 'fl', w1: 'fl', w2: 'fl', w3: 'fl'},
    note: 'weight shift to the right 0-6, the left fore lifts 6-15 to the hang (wrist 2.95 b, elbow high, the front rolled away, head turned to the foot), hang 15-17, the slam 17-22 = wave 1, compression and a shiver, two shoulder pushes for waves 2 / 3 at 37 / 52, recover'});
  const hshift = {rot: [0, 0, 3], pelvis: [0, 0, 5], pos: [0, -.05, 0], neck1: [4, 0, 0], tSweep: -12};
  const hhang = {rot: [-1, 0, 4], pelvis: [-2, -4, 8], spine: [0, 0, 2], neck1: [6, 6, 0], neck2: [2, 4, 0], head: [2, 8, 0], jaw: 8, hkL: [2.75, 2.65, 2.55], hfL: [-22, 0, 0], tSweep: -24, flH: 6};
  const hslam = {rot: [0, 0, 1], pos: [0, -.2, 0], pelvis: [2, 0, 1], spine: [0, 0, 0], neck1: [3, 2, 0], head: [-2, 4, 0], jaw: 14, tSweep: 6, flH: 10, flM: 6};
  S.push({name: 'stomp_hl', keys: [[0, {}], [6, hshift, 'io'], [15, hhang, 'o'], [17, {...hhang, hkL: [2.75, 2.72, 2.55]}], [22, hslam, 'i'], [26, {...hslam, pos: [0, -.12, 0]}, 'o'],
    [34, {pelvis: [1, 0, 1], pos: [0, -.08, 0]}], [37, {pelvis: [3, 0, 1], pos: [0, -.18, 0], jaw: 12}, 'i'], [41, {pelvis: [1, 0, 1], pos: [0, -.08, 0], jaw: 6}, 'o'],
    [49, {pelvis: [1, 0, 1], pos: [0, -.08, 0]}], [52, {pelvis: [3, 0, 1], pos: [0, -.18, 0], jaw: 12}, 'i'], [56, {pelvis: [1, 0, 1], pos: [0, -.08, 0], jaw: 6}, 'o'],
    [72, {rot: [0, 0, 0], pos: [0, 0, 0], pelvis: [0, 0, 0], spine: [0, 0, 0], neck1: [0, 0, 0], neck2: [0, 0, 0], head: [0, 0, 0], jaw: 3, tSweep: 0, flH: 0, flM: 0}, 'io']],
    feet: {hl: [W(0, 'hl'), W(6, 'hl'), Kf(15, {ease: 'o'}), Kf(17), Wp(22, F_(2.55, 1.5, 2.85), {ease: 'i'}), Wp(60, F_(2.55, 1.5, 2.85)), W(68, 'hl', 0, {lift: .15})]},
    over: [tremor(22, 30, 1.5, 3, [['pelvis', [.6]], ['flH', 2], ['flM', 2]])], lag: {head: 2}, tailLag: 2,
    anchors: {slam: ['paw'], w1: ['paw'], w2: ['paw'], w3: ['paw']}, plants: {slam: 'hl', w1: 'hl', w2: 'hl', w3: 'hl'},
    note: 'the hind variant: the pelvis rolls away, the left hock lifts knee-high (2.65 b) with the foot curled, the tail swings to the other side as a counterweight; the slam at 22, two haunch pushes for waves 2 / 3'});
  // stomp3 (90 -> 85): three separate front stomps, A / B / A: lifts 0-20, 30-40, 52-62, slams 22, 45, 68 (v9 C); every lift
  // is visible >= 12 played ticks before its slam (change note 1)
  const sideHang = s => ({rot: [0, 0, 4 * s], chest: [5, 0, 8 * s], pelvis: [2, 0, 0], neck1: [2, -5 * s, 0], head: [1, -8 * s, 0], jaw: 10, flS: 5});
  const sideSlam = s => ({rot: [-2, 0, s], pos: [0, -.22, 0], chest: [-4, 0, 2 * s], pelvis: [0, 0, 0], neck1: [-2, -3 * s, 0], head: [-5, -5 * s, 0], jaw: 16, flS: 10, flM: 8});
  const rest3 = {rot: [0, 0, 0], pos: [0, -.05, 0], chest: [0, 0, 0], neck1: [0, 0, 0], head: [0, 0, 0], jaw: 6, flS: 2, flM: 2};
  S.push({name: 'stomp3_fl', keys: [[0, {}], [5, {rot: [0, 0, 4], chest: [0, 0, 4]}], [18, sideHang(1), 'o'], [22, sideSlam(1), 'i'], [27, {...rest3, rot: [0, 0, -2], chest: [0, 0, -3]}, 'o'],
    [40, sideHang(-1), 'o'], [45, sideSlam(-1), 'i'], [50, {...rest3, rot: [0, 0, 2], chest: [0, 0, 3]}, 'o'],
    [63, sideHang(1), 'o'], [68, sideSlam(1), 'i'], [74, {...rest3, pos: [0, -.12, 0]}, 'o'], [90, {...rest3, pos: [0, 0, 0], jaw: 3, flS: 0, flM: 0}, 'io']],
    feet: {fl: [W(0, 'fl'), W(4, 'fl'), Kf(18, {ease: 'o'}), Wp(22, F_(3.3, .5, -2.55), {ease: 'i'}), Wp(52, F_(3.3, .5, -2.55)), Kf(63, {ease: 'o'}), Wp(68, F_(3.3, .5, -2.5), {ease: 'i'}), Wp(80, F_(3.3, .5, -2.5)), W(86, 'fl', 0, {lift: .2})],
      fr: [W(0, 'fr'), W(29, 'fr'), Kf(40, {ease: 'o'}), Wp(45, F_(-3.3, .5, -2.55), {ease: 'i'}), Wp(76, F_(-3.3, .5, -2.55)), W(83, 'fr', 0, {lift: .2})]},
    over: [(a, P) => { const L = a < 26 || a > 50 ? [3.5, 2.9, -2.85] : null, R = a >= 26 && a <= 50 ? [-3.5, 2.9, -2.85] : null; if (L) { P.fwL = L; P.fpL = [-34, 0, 0]; } if (R) { P.fwR = R; P.fpR = [-34, 0, 0]; } },
      tremor(22, 28, 1.4, 3, [['flS', 2], ['chest', [.5]]]), tremor(45, 51, 1.4, 3, [['flS', 2], ['chest', [.5]]]), tremor(68, 74, 1.4, 3, [['flS', 2], ['chest', [.5]]])],
    lag: {pelvis: 2, head: 1}, anchors: {s1: ['paw'], s2: ['paw'], s3: ['paw']}, plants: {s1: 'fl', s2: 'fr', s3: 'fl'},
    note: 'three front stomps A / B / A (the left fore lifts 4-18 and slams at 22, the right lifts 29-40 and slams at 45, the left again 52-63 / 68); the body rolls away from each lifted paw and the head turns to it; a shiver after every slam'});
}
// ---- feint / 성동격서 (56 -> 50): sway to its right 0-12, back past the centre 12-18, the heave and drop 18-22 (burst: rock
// spikes along both flanks), shudder, recover (motion.md §5.10, v3 H). Two clear sways before the burst (change note 1).
{
  S.push({name: 'feint', keys: [[0, {}], [11, {rot: [0, 0, 8], chest: [0, 6, 4], pelvis: [0, -4, 2], neck1: [0, 8, 0], neck2: [0, 5, 0], head: [2, 10, 0], jaw: 8, pos: [0, -.08, 0], tSweep: -14}, 'io'],
    [17, {rot: [0, 0, -9], chest: [0, -5, -4], pelvis: [0, 4, -2], neck1: [0, -6, 0], neck2: [0, -3, 0], head: [2, -6, 0], jaw: 10, pos: [0, -.06, 0], tSweep: 16}, 'io'],
    [19.5, {rot: [3, 0, -3], pos: [0, .14, 0], chest: [3, 0, 0], neck1: [4, 0, 0], head: [6, 0, 0], jaw: 18, flS: 6, flM: 6, flH: 6}, 'o'],
    [22, {rot: [-3, 0, 0], pos: [0, -.42, 0], chest: [-4, 0, 0], pelvis: [-2, 0, 0], neck1: [-2, 0, 0], neck2: [0, 0, 0], head: [-6, 0, 0], jaw: 20, flS: 16, flM: 16, flH: 14, flN: 10, flK: 1.06, tSweep: 0}, 'i'],
    [30, {rot: [-1, 0, 0], pos: [0, -.3, 0], chest: [-2, 0, 0], head: [-3, 0, 0], jaw: 10, flS: 10, flM: 10, flH: 8, flN: 6, flK: 1.03}, 'o'],
    [56, {rot: [0, 0, 0], pos: [0, 0, 0], chest: [0, 0, 0], pelvis: [0, 0, 0], neck1: [0, 0, 0], neck2: [0, 0, 0], head: [0, 0, 0], jaw: 3, flS: 0, flM: 0, flH: 0, flN: 0, flK: 1}, 'io']],
    over: [tremor(22, 32, 1.6, 3, [['rot', [0, 0, 1]], ['flM', 2], ['flS', 2]])], lag: {pelvis: 2, head: 1}, tailLag: 2,
    anchors: {burst: ['nose', 'tail_root']},
    note: 'the feint: sway to its right 0-11 (roll 8, head 10 right), sway back past the centre to the left 11-17, the heave (root +0.14) and the drop to root -0.42 at 22 (burst, the plates bristling), a shudder 22-32, recover'});
}

// ---- tail_whip_l (64): the tail raised high (the tell) 0-12, cocked to its right 12-20, dropped flat 20-23, the sweep 23-31
// while the anchor turns +115 (to its right: the tail swings from behind into its LEFT flank; contract §4.5), the erupt at
// 33, the overshoot to 122 at 35 with the tail counter-swinging, settled at 115 by 42, the tail back to its arc by 62
// (motion.md §5.11, v3 I; P7 of plan §5). The tail lags a little and its root-to-tip line is straight back by sweep_end, so
// the swept wedge ends 65 degrees from the front axis; the follow-through comes after the hazard.
{
  const T = TABLE.tail_whip_l, n = T.len;
  const yaw = Array.from({length: n}, (_, t) => {
    let v;
    if (t <= 20) v = 0; else if (t <= 31) v = 115 * smooth((t - 20) / 11); else if (t <= 35) v = 115 + 7 * smooth((t - 31) / 4);
    else if (t <= 42) v = 122 - 7 * smooth((t - 35) / 7); else v = 115;
    return +v.toFixed(2);
  });
  const high = {pos: [0, -.08, 0], rot: [-2, 0, 0], chest: [0, -8, 0], neck1: [0, -8, 0], neck2: [0, -4, 0], head: [2, -12, 0], jaw: 8, ...ups(TAIL_HIGH, .95), flH: 6};
  const flat = {pos: [0, -.22, 0], rot: [-3, 0, 0], apron: [12, 0, 0], chest: [0, -16, 0], spine: [0, -6, 0], pelvis: [0, 6, 0], neck1: [0, -10, 0], head: [-2, -12, 0], jaw: 14, ...ups(TAIL_WHIP), flH: 10};
  S.push({name: 'tail_whip_l', yaw, keys: [[0, {}], [10, {...high, tSweep: -6}, 'o'], [14, {...high, tSweep: -26, chest: [0, -12, 0], head: [2, -16, 0]}, 'io'], [20, {...high, tSweep: -30, chest: [0, -14, 0], head: [2, -18, 0], jaw: 12}],
    [23, {...flat, tSweep: -44}, 'i'], [27, {...flat, tSweep: -22, chest: [0, -8, 0], spine: [0, -2, 0]}, 'l'], [31, {...flat, tSweep: 6, chest: [0, 4, 0], spine: [0, 2, 0], pelvis: [0, -2, 0], head: [-2, 2, 0]}, 'l'],
    [35, {...flat, tSweep: 20, chest: [0, 6, 0], spine: [0, 3, 0], pelvis: [0, -4, 0], head: [-4, 6, 0], jaw: 18, pos: [0, -.3, 0]}, 'o'], [42, {...flat, tSweep: -2, chest: [0, 0, 0], spine: [0, 0, 0], pelvis: [0, 0, 0], head: [-2, 0, 0], jaw: 6, pos: [0, -.12, 0]}, 'io'],
    [62, {pos: [0, 0, 0], rot: [0, 0, 0], apron: [0, 0, 0], chest: [0, 0, 0], spine: [0, 0, 0], pelvis: [0, 0, 0], neck1: [0, 0, 0], neck2: [0, 0, 0], head: [0, 0, 0], jaw: 3, tSweep: 0, flH: 0, ...tailUp(TAIL_REST)}, 'io'], [64, {}]],
    tailLag: .6, lag: {head: 1},
    feet: {fl: [W(0, 'fl'), W(21, 'fl'), W(26, 'fl', 62, {lift: .35, curl: -15}), W(31, 'fl', 115, {lift: .3, curl: -15})],
      fr: [W(0, 'fr'), W(22, 'fr'), W(27, 'fr', 66, {lift: .35, curl: -15}), W(32, 'fr', 115, {lift: .3, curl: -15})],
      hl: [W(0, 'hl'), W(20, 'hl'), W(25, 'hl', 58, {lift: .45, curl: -10}), W(31, 'hl', 115, {lift: .4, curl: -10})],
      hr: [W(0, 'hr'), W(21, 'hr'), W(26, 'hr', 62, {lift: .45, curl: -10}), W(32, 'hr', 115, {lift: .4, curl: -10})]},
    anchors: {sweep: ['tail_root', 'tail_tip'], sweep_end: ['tail_root', 'tail_tip'], erupt: ['tail_root', 'tail_tip']},
    note: 'the tail raised high (the tell) 0-10 with the body coiled to its left, cocked to its right 14-20, dropped flat 20-23, the sweep 23-31 (the anchor +115 by the exported schedule, the fores stepping round twice, the hinds swinging round), the follow-through overshoot 31-35, settled 42, the tail back to its arc by 62'});
}
// ---- tail_slam (90 -> 70): the tail rises high over the back 0-12, the long hold 12-48 (the tip quivering), the slam 48-52
// straight back along the rear axis, impact 52, the spikes 54, the drag 30 degrees aside and lift 58-70, settle (v3 J, P8).
{
  const high = {pos: [0, -.06, 0], rot: [-3, 0, 0], pelvis: [2, 0, 0], neck1: [2, 0, 0], head: [-2, 0, 0], jaw: 6, flH: 8, flM: 4, ...ups(TAIL_HIGH)};
  const hit = {pos: [0, -.18, 0], rot: [-1, 0, 0], pelvis: [-4, 0, 0], neck1: [4, 0, 0], head: [2, 0, 0], jaw: 14, flH: 14, flM: 8, ...ups(TAIL_FLAT)};
  S.push({name: 'tail_slam', keys: [[0, {}], [12, high, 'o'], [44, {...high, ...ups(TAIL_HIGH, 1.06)}], [48, {...high, pelvis: [3, 0, 0], ...ups(TAIL_HIGH, 1.1), jaw: 10}, 'io'],
    [52, hit, 'i'], [55, {...hit, pos: [0, -.12, 0], ...ups(TAIL_FLAT.map((v, i) => v + (i > 1 ? 4 : 1)))}, 'o'], [58, {...hit, pos: [0, -.1, 0], jaw: 8}, 'io'],
    [70, {pos: [0, -.04, 0], pelvis: [0, 0, 0], rot: [0, 0, 0], neck1: [2, 0, 0], head: [0, 0, 0], jaw: 5, flH: 4, flM: 2, tSweep: 30, tLift: 10, ...ups(TAIL_LOW, .8)}, 'io'],
    [90, {pos: [0, 0, 0], neck1: [0, 0, 0], jaw: 3, flH: 0, flM: 0, tSweep: 0, tLift: 0, ...tailUp(TAIL_REST)}, 'io']],
    tailLag: 1.2, lag: {head: 2},
    over: [tremor(14, 47, 2.5, 4, [['t6', [1, 1.5]], ['t7', [1.5, 2]], ['t8', [2, 2.5]]])],
    anchors: {slam: ['tail_root', 'tail_tip'], impact: ['tail_root', 'tail_tip'], spikes: ['tail_root', 'tail_tip']},
    note: 'the tail rises high over the rump 0-12 (a near straight pole, the tip ~12 b up, the body leaning onto the fores), held 12-48 with the tip quivering, slammed 48-52 straight back along the floor (impact 52), a bounce, the spikes 54, dragged 30 degrees aside and lifted 58-70, settled by 90'});
}

// ---- burrows (phase 1 P9; rigtech §4): the rig sinks below the opaque floor (every part under y 0 before it is hidden), the
// hidden spans scale every part to 0 (contract §4.6), the anchor (husk) never goes into blocks.
const HID = {visBody: 0, visTail: 0};
const SHOW = {visBody: 1, visTail: 1};
{
  // burrow_dive (44 -> 40): the snarl 0-12 (head up, jaw 40), the head to the floor 12-18, the dive 18-30 (nose-down 50 about
  // the chest, root -3.5, a 20 degree twist, the hinds push), the rear and the tail slide under 30-44 (v2 F, motion §5.13)
  S.push({name: 'burrow_dive', floorFree: [[12, 40]], keys: [[0, {}], [4, {neck1: [10, 0, 0], neck2: [6, 0, 0], head: [12, 0, 0], jaw: 30}, 'o'], [12, {neck1: [14, 0, 0], neck2: [8, 0, 0], head: [18, 4, 0], jaw: 40, pos: [0, -.1, 0]}],
    [18, {neck1: [-6, 0, 0], neck2: [-4, 0, 0], head: [-10, 0, 0], jaw: 18, pos: [0, -.35, 0], rot: [-6, 0, 0], flS: 8, flM: 8, flH: 8}, 'io'],
    [30, {pos: [0, -3.6, 0], rot: [-48, 0, 16], pelvis: [-6, 0, 0], neck1: [-10, 0, 0], head: [-12, 0, 0], jaw: 22, ...ups(TAIL_TUCK, .6)}, 'i'],
    [38, {pos: [0, -7.5, 0], rot: [-34, 0, 12], pelvis: [-14, 0, 0], ...ups(TAIL_TUCK, 1.6)}],
    [44, {pos: [0, -11, 0], rot: [-24, 0, 8], pelvis: [-18, 0, 0], ...ups(TAIL_TUCK, 2.2)}]],
    feet: {fl: [W(0, 'fl'), W(20, 'fl'), Rf(28)], fr: [W(0, 'fr'), W(20, 'fr'), Rf(28)], hl: [W(0, 'hl'), W(18, 'hl'), Rf(24)], hr: [W(0, 'hr'), W(18, 'hr'), Rf(24)]},
    tailLag: 2.5, anchors: {}, state: [[40, 'burrowed']],
    note: 'the snarl (head up, jaw 40), the head to the floor, the dive (nose-down 48 about the chest, root -3.6, a 16 degree twist, the hinds pushing), the rear and the tail slide under (root -11, the tail tucked after it); everything is under the floor by played 39 and hidden at the hand-over (40, state burrowed)'});
  const under = {pos: [0, -9, 0], rot: [0, 0, 0], ...HID};
  S.push({name: 'burrow_travel', keys: [[0, under], [20, under]], hidden: [[0, 19, 'all']], springs: false, stateCalls: [[0, 'burrowed']],
    note: 'underground: root -9, every part at scale 0 (hidden 0-19); tick 0 also records the burrowed state (the hand-over of burrow_dive)'});
  // burrow_breach (36): hidden 0-7, the head and chest breach at +50 pitch 8-14 (root -7 -> -2.4, jaw open), hang, fall back
  // under 18-29, hidden 30-35 (v2 F, motion §5.13)
  const sub = {pos: [0, -7.4, 0], rot: [48, 0, 0], neck1: [10, 0, 0], head: [16, 0, 0], jaw: 34, flS: 14, flM: 12, ...ups(TAIL_TUCK, 2)};
  S.push({name: 'burrow_breach', floorFree: [[0, 36]], keys: [[0, {...sub, ...HID}], [7, {...sub, ...HID}], [8, {...sub, ...SHOW}, 'l'], [14, {...sub, pos: [0, -2.4, 0], rot: [50, 0, -4], neck1: [6, 0, 0], head: [6, 0, 0], jaw: 44}, 'o'],
    [18, {...sub, pos: [0, -2.6, 0], rot: [46, 0, 4], head: [2, 0, 0], jaw: 38}], [29, {...sub, pos: [0, -8.6, 0], rot: [40, 0, 0], jaw: 16}, 'i'], [30, {...sub, pos: [0, -8.6, 0], ...HID}, 'l'], [36, {...sub, pos: [0, -8.6, 0], ...HID}]],
    feet: {fl: [Rf(0)], fr: [Rf(0)], hl: [Rf(0)], hr: [Rf(0)]}, hidden: [[0, 7, 'all'], [30, 35, 'all']], state: [[8, 'normal'], [30, 'burrowed']], springs: false,
    note: 'a surfacing: hidden to 7; at 8 the head and chest burst up nose-first (pitch +50, root -7.4 -> -2.4, jaw 44), hang 14-18, fall back under by 29, hidden 30-35'});
  // burrow_emerge (56 -> 53): hidden to 23 (the module's dust and burst 8 show the spot), from fore 24 the body rises
  // nose-first, the fores claw out and plant 24-30, the hinds climb out 30-38 (out), the shake 40-50, settle (v3 F)
  const e0 = {pos: [0, -8.4, 0], rot: [34, 0, 0], neck1: [8, 0, 0], head: [10, 0, 0], jaw: 20, flS: 10, flM: 10, ...ups(TAIL_TUCK, 1.6), ...fore([3.4, 1.6, -3.6], [-40, 0, 0])};
  S.push({name: 'burrow_emerge', floorFree: [[0, 32]], keys: [[0, {...e0, ...HID}], [23, {...e0, ...HID}], [24, {...e0, ...SHOW}, 'l'],
    [30, {...e0, pos: [0, -1.8, 0], rot: [18, 0, 0], neck1: [6, 0, 0], head: [6, 0, 0], jaw: 26, ...ups(TAIL_TUCK, .8)}, 'o'],
    [38, {pos: [0, -.2, 0], rot: [0, 0, 0], neck1: [2, 0, 0], head: [0, 0, 0], jaw: 10, flS: 6, flM: 6, ...ups(TAIL_REST, .7)}, 'io'],
    [40, {pos: [0, -.12, 0]}], [50, {pos: [0, -.08, 0], jaw: 6, flS: 3, flM: 3}], [56, {pos: [0, 0, 0], neck1: [0, 0, 0], jaw: 3, flS: 0, flM: 0, ...tailUp(TAIL_REST)}, 'io']],
    feet: {fl: [Rf(0), Rf(24), Kf(27), Wp(30, F_(3.35, .5, -3.3), {ease: 'i'}), Wp(44, F_(3.35, .5, -3.3)), W(50, 'fl', 0, {lift: .35, curl: -15})],
      fr: [Rf(0), Rf(25), Kf(28), Wp(31, F_(-3.35, .5, -3.3), {ease: 'i'}), Wp(46, F_(-3.35, .5, -3.3)), W(52, 'fr', 0, {lift: .35, curl: -15})],
      hl: [Rf(0), Rf(30), W(38, 'hl', 0, {lift: .3, ease: 'i'})], hr: [Rf(0), Rf(31), W(38, 'hr', 0, {lift: .3, ease: 'i'})]},
    over: [tremor(40, 50, 5, 4, [['rot', [0, 0, 1]], ['chest', [0, 0, .6]], ['head', [0, 1.4, 0]]])], tailLag: 2,
    hidden: [[0, 23, 'all']], state: [[24, 'normal']],
    note: 'hidden to 23 (the module shows the dust and the burst at 8); from 24 the body rises nose-first through the floor (root -5.2 -> 0, pitch +34 -> 0), the fores claw out and plant at 30 / 31, the hinds climb out by 38 (out), the shake 40-50 (roll +-5, 4 t), the fores step back, settle'});
}

// ---- landslide / 파멸의 산사태 (270 -> 203): the tell (head low, growl, the slow lift of the right fore 20-40 and the right
// hind 36-56; the module turns the anchor in place, played 0-45), the crouch, wave 1 (both fores) at 76, then one fore per
// wave lifted from the previous wave to its slam (each lift >= 20 played ticks, change note 1): right 104, left 132, right
// 156, left 186; the gather, the big rear-up (top at 212 = rear), the hang, the body slam at 240 (wave 6), the heavy settle.
{
  const low = {pos: [0, -.12, 0], neck1: [-3, 0, 0], neck2: [-2, 0, 0], head: [-4, 0, 0], jaw: 10};
  const LIFT_R = [-3.45, 2.2, -2.8], LIFT_L = [3.45, 2.2, -2.8], BOTH = [[3.35, 1.7, -2.9], [-3.35, 1.7, -2.9]];
  // s = +1: the left fore lifts (the body rolls away from it: the top toward its right, roll +), -1 the right fore
  const slamPose = s => ({pos: [0, -.42, 0], rot: [-2, 0, s], chest: [-5, 0, 2 * s], pelvis: [0, 0, 0], neck1: [-3, 0, 0], head: [-6, -3 * s, 0], jaw: 18, flS: 12, flM: 10, flH: 8});
  const liftPose = s => ({pos: [0, -.06, 0], rot: [0, 0, 4 * s], chest: [5, 0, 8 * s], pelvis: [2, 0, 0], neck1: [2, -3 * s, 0], head: [0, -6 * s, 0], jaw: 10, flS: 6, flM: 4, flH: 2});
  const after = s => ({pos: [0, -.2, 0], rot: [0, 0, 0], chest: [-1, 0, 0], neck1: [0, 0, 0], head: [-3, 0, 0], jaw: 8});
  const top = REAR(60, {neck1: [-16, 0, 0], neck2: [0, 0, 0], head: [28, 0, 0], jaw: 50, flS: 16, flM: 14, flN: 12, flH: 10, ...FORE_UP(6.0, -2.8, 3.8, [-45, 0, -20])});
  const keys = [[0, {}], [10, low, 'io'], [20, {...low, rot: [0, 0, 3]}], [30, {...low, rot: [0, 0, 4], chest: [2, 0, 5]}, 'io'], [40, {...low, rot: [0, 0, 2]}], [46, {...low, pelvis: [0, 0, 5]}], [56, low],
    [62, {...low, pos: [0, -.3, 0], rot: [-3, 0, 0], chest: [4, 0, 0], neck1: [2, 0, 0], jaw: 14}], [72, {pos: [0, -.1, 0], rot: [1, 0, 0], chest: [8, 0, 0], neck1: [3, 0, 0], head: [2, 0, 0], jaw: 16, flS: 6}, 'o'],
    [76, slamPose(0), 'i'], [80, after(0), 'o'],
    [97, liftPose(-1), 'o'], [104, slamPose(-1), 'i'], [108, after(-1), 'o'],
    [125, liftPose(1), 'o'], [132, slamPose(1), 'i'], [136, after(1), 'o'],
    [150, liftPose(-1), 'o'], [156, slamPose(-1), 'i'], [160, after(-1), 'o'],
    [179, liftPose(1), 'o'], [186, slamPose(1), 'i'], [190, after(1), 'o'],
    [198, {pos: [0, -.35, 0], rot: [-2, 0, 0], pelvis: [-4, 0, 0], neck1: [-2, 0, 0], head: [-4, 0, 0], jaw: 12}, 'io'],
    [212, top, 'o'], [233, {...top, jaw: 46}], [236, {...top, pelvis: [56, 0, 0], jaw: 40}],
    [240, {...REAR(0, {pos: [0, -.62, 0], rot: [-4, 0, 0], chest: [-6, 0, 0], neck1: [-4, 0, 0], neck2: [0, 0, 0], head: [-8, 0, 0], jaw: 26, flS: 20, flM: 18, flN: 14, flH: 14, flK: 1.06}), ...tailUp(TAIL_REST)}, 'i'],
    [246, {pos: [0, -.42, 0], chest: [-3, 0, 0], jaw: 14, flS: 12, flM: 10, flN: 8, flH: 8, flK: 1.03}, 'o'],
    [270, {pos: [0, -.06, 0], rot: [0, 0, 0], chest: [0, 0, 0], neck1: [-2, 0, 0], head: [-3, 0, 0], jaw: 4, flS: 0, flM: 0, flN: 0, flH: 0, flK: 1}, 'io']];
  // fore paws per wave (K = carried by the channel set in the overlay below)
  const fl = [W(0, 'fl'), W(64, 'fl'), Kf(72, {ease: 'o'}), Wp(76, F_(3.3, .5, -2.6), {ease: 'i'}), Wp(105, F_(3.3, .5, -2.6)), Kf(125, {ease: 'o'}), Wp(132, F_(3.3, .5, -2.55), {ease: 'i'}),
    Wp(157, F_(3.3, .5, -2.55)), Kf(179, {ease: 'o'}), Wp(186, F_(3.3, .5, -2.6), {ease: 'i'}), Wp(197, F_(3.3, .5, -2.6)), Sf(203, [1.5, -2.0, 1.1], [-25, 0, -20]), Sf(238, [1.5, -2.0, 1.1], [-25, 0, -20]), W(240, 'fl', 0, {ease: 'i'})];
  const fr = [W(0, 'fr'), W(20, 'fr'), Kf(30, {ease: 'o'}), W(40, 'fr', 0, {ease: 'io'}), W(64, 'fr'), Kf(72, {ease: 'o'}), Wp(76, F_(-3.3, .5, -2.6), {ease: 'i'}), Wp(78, F_(-3.3, .5, -2.6)),
    Kf(97, {ease: 'o'}), Wp(104, F_(-3.3, .5, -2.55), {ease: 'i'}), Wp(133, F_(-3.3, .5, -2.55)), Kf(150, {ease: 'o'}), Wp(156, F_(-3.3, .5, -2.6), {ease: 'i'}), Wp(197, F_(-3.3, .5, -2.6)), Sf(203, [1.5, -2.0, 1.1], [-25, 0, -20]), Sf(238, [1.5, -2.0, 1.1], [-25, 0, -20]), W(240, 'fr', 0, {ease: 'i'})];
  const hr = [W(0, 'hr'), W(36, 'hr'), Wp(46, F_(-2.6, 2.3, 2.7), {ease: 'o'}), W(56, 'hr', 0, {ease: 'io'})];
  const paws = (a, P) => {
    if (a < 60) { P.fwR = [-3.4, 1.3, -2.6]; P.fpR = [-20, 0, 0]; }
    else if (a < 90) { P.fwL = BOTH[0]; P.fwR = BOTH[1]; P.fpL = [-25, 0, 0]; P.fpR = [-25, 0, 0]; }
    else if (a < 200) { P.fwL = LIFT_L; P.fwR = LIFT_R; P.fpL = [-30, 0, 0]; P.fpR = [-30, 0, 0]; }
  };
  S.push({name: 'landslide', keys, feet: {fl, fr, hr}, over: [paws, tremor(214, 236, 1.5, 4, [['chest', [1]], ['head', [1, .6]], ['jaw', 2]]),
    ...[76, 104, 132, 156, 186].map(a => tremor(a, a + 7, 1.6, 3, [['flS', 2], ['flM', 2], ['chest', [.4]]])), tremor(240, 252, 2.4, 3, [['flS', 2], ['flM', 2], ['rot', [.6, 0, .4]]])],
    lag: {head: 1},
    note: 'the tell 0-60 (head low, a growl, the right fore lifted 20-40 and the right hind 36-56); the crouch 60-72 and wave 1 at 76 (both fores); one fore per wave lifted from the previous wave to its slam (right 104, left 132, right 156, left 186); the gather 186-198, the big rear-up to 212 (pelvis +60, fores high, roaring), the hang to 236, the body slam at 240 (wave 6, plates flared), the heavy settle'});
}

// ---- absorbs (motion.md §5.15): absorb (108 -> 94): the head pressed to the floor, the back and the plate crown to the
// sky, fores wide; the hold with a slow heave; push up; the left fore stamps 76, the right 100; the gold flares from
// gold_on to gold_off. absorb_p3 (70 -> 52): it stands tall, the plates flared, the head up to the orb, the gather at 60.
{
  const press = {pos: [0, -.32, 0], rot: [-5, 0, 0], pelvis: [6, 0, 0], spine: [4, 0, 0], chest: [-6, 0, 0], neck1: [-2, 0, 0], neck2: [-4, 0, 0], head: [-8, 0, 0], jaw: 6,
    flN: 12, flS: 18, flM: 18, flH: 14, flK: 1.06, ...ups(TAIL_REST, 1.04)};
  const lifted = s => ({pos: [0, -.08, 0], rot: [0, 0, 4 * s], chest: [5, 0, 7 * s], pelvis: [2, 0, 0], spine: [0, 0, 0], neck1: [4, 3 * -s, 0], neck2: [2, 0, 0], head: [4, 5 * -s, 0], jaw: 10, flS: 10, flM: 10, flH: 8, flN: 8, flK: 1.03});
  const stamp = s => ({pos: [0, -.3, 0], rot: [-2, 0, s], chest: [-4, 0, s], pelvis: [0, 0, 0], neck1: [-2, 0, 0], head: [-4, 0, 0], jaw: 16, flS: 14, flM: 14, flH: 10, flN: 10, flK: 1.05});
  S.push({name: 'absorb', keys: [[0, {}], [12, press, 'io'], [58, press], [68, {pos: [0, -.04, 0], rot: [1, 0, 0], pelvis: [2, 0, 0], spine: [0, 0, 0], chest: [3, 0, 0], neck1: [4, 0, 0], neck2: [2, 0, 0], head: [6, 0, 0], jaw: 12, flS: 12, flM: 12, flH: 10, flN: 10, flK: 1.04}, 'io'],
    [73, lifted(1), 'o'], [76, stamp(1), 'i'], [82, {pos: [0, -.12, 0], rot: [0, 0, 0], chest: [0, 0, 0], head: [0, 0, 0], jaw: 8}, 'o'], [97, lifted(-1), 'o'], [100, stamp(-1), 'i'],
    [108, {pos: [0, -.06, 0], rot: [0, 0, 0], chest: [0, 0, 0], pelvis: [0, 0, 0], neck1: [0, 0, 0], neck2: [0, 0, 0], head: [0, 0, 0], jaw: 5, flS: 4, flM: 4, flH: 3, flN: 3, flK: 1.01, ...tailUp(TAIL_REST)}, 'o']],
    feet: {fl: [W(0, 'fl'), W(2, 'fl'), Wp(10, F_(3.75, .5, -2.7), {lift: .3, curl: -12}), Wp(68, F_(3.75, .5, -2.7)), Kf(73, {ease: 'o'}), Wp(76, F_(3.4, .5, -2.6), {ease: 'i'})],
      fr: [W(0, 'fr'), W(3, 'fr'), Wp(11, F_(-3.75, .5, -2.7), {lift: .3, curl: -12}), Wp(86, F_(-3.75, .5, -2.7)), Kf(97, {ease: 'o'}), Wp(100, F_(-3.4, .5, -2.6), {ease: 'i'})]},
    over: [(a, P) => { if (a < 90) { P.fwL = [3.6, 2.1, -2.75]; P.fpL = [-28, 0, 0]; } P.fwR = [-3.6, 2.1, -2.75]; P.fpR = [-28, 0, 0]; },
      (a, P) => { if (a > 12 && a < 60) { const s = Math.sin(2 * Math.PI * (a - 12) / 20); P.chest = add(P.chest, [1.5 * s, 0, 0]); P.pos = add(P.pos, [0, .06 * s, 0]); P.flM += 2 * s; P.flS += 2 * s; } }],
    lag: {pelvis: 2, head: 1}, anchors: {burst: ['back']}, gold: [['gold_on', 'on'], ['gold_off', 'off']], contact: [[8, 60, .05]],
    note: 'the head pressed low to the floor with the rump and the plate crown up (flare +18) 0-12, the fores stepping wide; the hold 12-58 with a 20-t heave; push up 58-68; the left fore lifts and stamps at 76, the right at 100; settle'});
  const tall = {pos: [0, -.32, 0], pelvis: [5, 0, 0], spine: [1, 0, 0], chest: [2, 0, 0], neck1: [12, 0, 0], neck2: [7, 0, 0], head: [12, 0, 0], jaw: 8, flN: 10, flS: 15, flM: 15, flH: 12, flK: 1.05, ...ups(TAIL_REST, 1.06)};
  S.push({name: 'absorb_p3', keys: [[0, {}], [20, tall, 'io'], [58, {...tall, head: [18, 0, 0], neck1: [12, 0, 0]}], [63, {...tall, pos: [0, -.2, 0], pelvis: [4, 0, 0], head: [6, 0, 0], jaw: 14, flS: 18, flM: 18}, 'io'],
    [66, {...tall, pos: [0, -.36, 0], pelvis: [6, 0, 0], neck1: [16, 0, 0], head: [22, 0, 0], jaw: 30, flN: 16, flS: 24, flM: 24, flH: 20, flK: 1.1}, 'o'], [70, {...tall, pos: [0, -.34, 0], pelvis: [6, 0, 0], neck1: [15, 0, 0], head: [20, 0, 0], jaw: 26, flN: 14, flS: 22, flM: 22, flH: 18, flK: 1.08}]],
    over: [(a, P) => { if (a > 18 && a < 60) { const s = Math.sin(2 * Math.PI * (a - 18) / 20); P.chest = add(P.chest, [2 * s, 0, 0]); P.pos = add(P.pos, [0, .07 * s, 0]); P.head = add(P.head, [-1.5 * s, 0, 0]); } }],
    lag: {pelvis: 2}, anchors: {burst: ['back']}, gold: [['gold_on', 'on'], ['gold_off', 'off']],
    note: 'it stands tall 0-20 (the front up, the head lifted to the orb over its back, the plates flared +15), the hold 20-58 with the chest heaving, a dip 58-63 and the gather at 60-66 (head up, jaw 30, plates +24), held for the roar the module plays next'});
}
// ---- the phase-3 sink and the tail-only pillar (motion.md §5.16, plan §3.4, Rig decision change 1) --------------------------
// p3_sink (80 -> 66): crouch 0-8, sink 8-32 (root -4, nose-down 25, rocking), everything under by played 39; from played 40
// the body is hidden and the root offset puts the tail root under the anchor (root_z), the pillar rises out of the floor
// 62-71 (played 50-58: pillar) and settles. tail_pillar / _strike / _sink: the pillar at the anchor (columns stacked).
{
  const pil = {...restPose(), ...PILLAR_ROOT, ...ups(TAIL_PILLAR), visBody: 0, visTail: 1};
  const deep = {...pil, pos: [0, -8.55 - 11.6, -J.t1[2]]};
  S.push({name: 'p3_sink', floorFree: [[8, 66]], keys: [[0, {}], [8, {pos: [0, -.3, 0], neck1: [-2, 0, 0], head: [-4, 0, 0], jaw: 8, ...ups(TAIL_REST, .85)}, 'io'],
    [32, {pos: [0, -4.2, 0], rot: [-25, 0, 0], neck1: [-6, 0, 0], head: [-8, 0, 0], jaw: 4, ...ups(TAIL_TUCK, .4)}, 'io'],
    [49.9, {pos: [0, -10.5, 0], rot: [-14, 0, 0], pelvis: [-10, 0, 0], ...ups(TAIL_TUCK, 2.0)}, 'i'], [50, {...deep, visTail: 0}, 'l'], [56, {...deep, visTail: 0}], [57, deep, 'l'], [62, deep], [71, pil, 'o'], [80, pil]],
    feet: {fl: [W(0, 'fl'), W(10, 'fl'), Rf(20)], fr: [W(0, 'fr'), W(10, 'fr'), Rf(20)], hl: [W(0, 'hl'), W(14, 'hl'), Rf(24)], hr: [W(0, 'hr'), W(14, 'hr'), Rf(24)]},
    over: [tremor(10, 32, 4, 10, [['rot', [0, 0, 1]]]), (a, P) => { if (a >= 71) { const s = Math.sin(2 * Math.PI * (a - 71) / 80); P.t8 = add(P.t8, [-4 * s, 3 * s, 0]); } }],
    tailLag: 0, hidden: [[40, 65, 'body']], state: [[40, 'tail_only']], anchors: {pillar: ['tail_root', 'tail_tip']},
    note: 'crouch 0-8, the sink 8-32 (root -4.2, nose-down 25, rocking +-4), under 32-50 (everything below the floor by played 39); from played 40 the body is hidden, the root is offset forward 4.75 b so the tail root lies under the anchor (Rig decision change 1), the pillar rises straight out of the floor 62-71 (played 50-58: pillar) and settles'});
  const sway = (amp, lagSeg = 3) => (a, P) => {
    const w = 2 * Math.PI / 80;
    for (let i = 0; i < 8; i++) {
      const k = i < 6 ? .02 : i < 7 ? .12 : 1;              // the column stays put (the four columns within 0.3 b), the crown sways
      P['t' + (i + 1)] = add(P['t' + (i + 1)], [amp * k * Math.sin(w * (a - lagSeg * i)), amp * k * .7 * Math.sin(w * (a - lagSeg * i) + 1.3), amp * k * .5 * Math.sin(w * (a - lagSeg * i) + .4)]);
    }
  };
  S.push({name: 'tail_pillar', keys: [[0, pil], [80, pil]], over: [sway(6)], tailLag: 0, hidden: [[0, 79, 'body']], springs: false,
    note: 'the tail-only pillar on the anchor (body hidden, root offset): the column straight, the crown swaying +-6 (pitch, yaw, roll; 3 t lag up the chain); pulse at 0 / 40 (module fx)'});
  S.push({name: 'tail_pillar_strike', keys: [[0, pil], [6, {...pil, ...ups(TAIL_PILLAR.map((v, i) => v + (i === 6 ? -3 : i === 7 ? -14 : 0)))}, 'io'], [10, {...pil, ...ups(TAIL_PILLAR.map((v, i) => v + (i === 6 ? 4 : i === 7 ? 30 : 0)))}, 'i'],
    [14, {...pil, ...ups(TAIL_PILLAR.map((v, i) => v + (i === 6 ? 2 : i === 7 ? 22 : 0)))}, 'o'], [24, pil, 'io']], tailLag: 0, hidden: [[0, 23, 'body']], springs: false,
    over: [sway(2)], anchors: {strike: ['tail_tip']},
    note: 'a strike cue: the crown cocks back 0-6 and nods 30 degrees forward at 10 (strike), back by 24; the column stays on the anchor'});
  S.push({name: 'tail_pillar_sink', keys: [[0, pil], [17, {...pil, pos: [0, -8.55 - 10.5, -J.t1[2]]}, 'i'], [18, {...pil, pos: [0, -8.55 - 10.5, -J.t1[2]], visTail: 0}, 'l'], [20, {...pil, pos: [0, -8.55 - 10.5, -J.t1[2]], visTail: 0}]],
    tailLag: 0, hidden: [[0, 17, 'body'], [18, 19, 'all']], state: [[18, 'burrowed']], springs: false,
    note: 'the pillar drops straight down into the floor (ease in), under by 17, gone (hidden) at 18 (state burrowed)'});
}
// ---- tail_cast (40 -> 34): the scorpion raise 0-12, the charge 12-24 (the tip coils tighter and quivers), fire 24 (recoil and
// snap), hold, lower 32-40 (replaces motion.md tail_shells; v7 A1, v8 D; the module's sphere / shells leave the tip)
{
  const cast = {pos: [0, -.1, 0], rot: [-2, 0, 0], pelvis: [-2, 0, 0], neck1: [4, 0, 0], head: [2, 0, 0], jaw: 8, flH: 8, flM: 6, ...ups(TAIL_CAST)};
  const coil = {...cast, ...ups(TAIL_CAST.map((v, i) => v + (i >= 4 ? 6 : 0))), jaw: 12};
  S.push({name: 'tail_cast', keys: [[0, {}], [12, cast, 'o'], [16, coil, 'io'], [22, {...coil, ...ups(TAIL_CAST.map((v, i) => v + (i >= 4 ? 10 : 0)))}], [24, {...cast, ...ups(TAIL_CAST.map((v, i) => v + (i >= 4 ? -6 : 0))), jaw: 18}, 'i'],
    [27, {...cast, jaw: 10}, 'o'], [32, cast], [40, {pos: [0, 0, 0], rot: [0, 0, 0], pelvis: [0, 0, 0], neck1: [0, 0, 0], head: [0, 0, 0], jaw: 3, flH: 0, flM: 0, ...tailUp(TAIL_REST)}, 'io']],
    over: [tremor(14, 23, 2, 2, [['t7', [1, 1]], ['t8', [1.5, 1.5]]])], tailLag: 1.2, anchors: {charge: ['tail_tip'], fire: ['tail_tip']},
    note: 'the scorpion raise 0-12 (the column vertical over the rump, the leafy crown curled forward over the shoulders), the charge 12-22 (coiling tighter, quivering), fire at 24 (a recoil and snap), hold, lowered to the rest arc by 40'});
}
// ---- death (120, no footage; motion.md §5.19): stagger, the fores buckle and the chin hits the floor at 34, the hinds fold,
// the slump onto its right flank, the tail falls flat at 66, the head lifts weakly (last 80) and falls at 92, still from 96
// (the module calls look/petrify at 96).
{
  const down = {pos: [0, -1.25, 0], rot: [-6, 0, 0], pelvis: [-2, 0, 0], spine: [-2, 0, 0], chest: [-3, 0, 0], neck1: [10, 0, 0], neck2: [4, 0, 0], head: [2, 0, 0], jaw: 8};
  const slump = {pos: [0, -1.85, 0], rot: [-3, 0, 14], pelvis: [-4, 0, 2], chest: [-2, 0, 2], neck1: [8, 6, 4], neck2: [2, 4, 0], head: [0, 6, 6], jaw: 6};
  S.push({name: 'death', keys: [[0, {}], [6, {rot: [5, 0, 0], neck1: [14, 0, 0], neck2: [8, 0, 0], head: [12, 0, 0], jaw: 34, flS: 6, flM: 6}, 'o'], [14, {rot: [2, 0, -2], pos: [0, -.1, 0], neck1: [10, 0, 0], head: [8, 0, 0], jaw: 26}, 'io'],
    [34, down, 'i'], [38, {...down, pos: [0, -1.35, 0], head: [-2, 0, 0], neck1: [8, 0, 0]}, 'o'], [52, {...down, pos: [0, -1.75, 0], pelvis: [-6, 0, 0], ...ups(TAIL_REST, .8)}, 'io'],
    [64, {...slump, ...ups(TAIL_LOW, .9), tSweep: 18}, 'io'], [66, {...slump, ...ups(TAIL_FLAT), tSweep: 22}, 'i'], [72, {...slump, ...ups(TAIL_FLAT), tSweep: 20}, 'o'],
    [82, {...slump, neck1: [16, 4, 4], neck2: [6, 2, 0], head: [8, 4, 4], jaw: 16, ...ups(TAIL_FLAT), tSweep: 20}, 'o'], [92, {...slump, neck1: [6, 6, 6], neck2: [0, 4, 0], head: [-3, 6, 8], jaw: 4, ...ups(TAIL_FLAT), tSweep: 20}, 'i'],
    [96, {...slump, neck1: [5, 6, 6], neck2: [0, 4, 0], head: [-4, 6, 8], jaw: 3, ...ups(TAIL_FLAT), tSweep: 20}, 'o'], [120, {...slump, neck1: [5, 6, 6], neck2: [0, 4, 0], head: [-4, 6, 8], jaw: 3, ...ups(TAIL_FLAT), tSweep: 20}]],
    feet: {fl: [W(0, 'fl'), W(16, 'fl'), Wp(32, F_(4.0, .5, -2.8), {ease: 'i'})], fr: [W(0, 'fr'), W(18, 'fr'), Wp(34, F_(-3.9, .5, -2.9), {ease: 'i'})],
      hl: [W(0, 'hl'), W(36, 'hl'), Wp(50, F_(3.0, 1.5, 3.4)), Wp(64, F_(3.3, 1.5, 3.5))], hr: [W(0, 'hr'), W(38, 'hr'), Wp(52, F_(-2.8, 1.5, 3.4)), Wp(64, F_(-2.9, 1.5, 3.3))]},
    lag: {pelvis: 4, head: 1}, tailLag: 2, contact: [[30, 120, .12]],
    note: 'stagger 0-14 (rearing back, the head jerks up, jaw open); the fores buckle and slide out, the chest drops, the chin hits the floor at 34; the hinds fold, the belly on the floor by 52; the slump onto its right flank 52-64 with the tail falling flat at 66; the head lifts weakly at 80-82 and falls at 92; still from 96'});
}

// ---- assembly: the 35 authored clips baked, the 6 mirrors, in the table order (clip ids 0..40), then the R1 debug poses as
// dbg_<name> (static 2-tick loops; renders and checks only, ignored by the module, contract §4).
const BAKED = Object.fromEntries(S.map(s => [s.name, bake(s)]));
for (const [m, src] of Object.entries(MIRRORS)) BAKED[m] = mirrorClip(BAKED[src], m);
for (const [name] of CLIP_TABLE) if (!BAKED[name]) throw new Error(`clip ${name} is not authored`);
const plantedAt = dy => ({...fore([J.wrist[0], J.wrist[1] + dy, J.wrist[2]]), ...hind([J.hock[0], J.hock[1] + dy, J.hock[2]])});
const dbg = (name, p, note, extra = {}) => ({name: 'dbg_' + name, len: 2, loop: true, keys: [[0, p], [2, {}]], events: {}, note, dbg: true, hidden: [], state: [], anchors: {}, plants: {}, gold: [], stateCalls: [], retime: [], authoredLen: 2, ...extra});
const DBG = [
  dbg('rest', {}, 'DEFAULT_POSE: the idle stance, head low'),
  dbg('head_up', {neck1: [42, 0, 0], neck2: [16, 0, 0], head: [-38, 0, 0], jaw: 6}, 'head raised: the neck up, the face still forward, eyes about 3 b'),
  dbg('roar', {neck1: [8, 0, 0], neck2: [6, 0, 0], head: [18, 0, 0], jaw: 45, beard1: [-12, 0, 0]}, 'low roar: jaw 45, head thrust up'),
  dbg('rear_up', {pos: [0, -.1, 0], pelvis: [45, 0, 0], spine: [6, 0, 0], chest: [4, 0, 0], neck1: [-10, 0, 0], neck2: [5, 0, 0], head: [22, 0, 0], jaw: 40,
    apron: [-18, 0, 0], beard1: [-15, 0, 0], beard2: [-10, 0, 0], flS: 10, flM: 8, ...fore([3.2, 4.6, -3.3], [-55, 0, 0]), ...tailUp([36, 6, 4, 0, 0, 6, 12, 18]), ...hind([J.hock[0], J.hock[1] + .1, J.hock[2]])}, 'rear-up peak: pelvis +45, fore paws at chest height'),
  dbg('stomp_lift', {pelvis: [3, 0, 0], spine: [2, 0, 4], chest: [6, 0, 10], neck1: [0, -6, 0], head: [0, -10, 0], ...fore([3.45, 2.4, -2.75], [-30, 0, 0], [-3.15, .5, -2.4], [0, 0, 0])}, 'stomp_fl hang'),
  dbg('whip_mid', {pos: [0, -.2, 0], apron: [12, 0, 0], chest: [0, 12, 0], spine: [0, 6, 0], pelvis: [0, -6, 0], head: [0, 10, 0], ...tailUp(TAIL_WHIP), tSweep: 110, ...plantedAt(.2)}, 'tail whip mid-sweep'),
  dbg('loop', {...tailUp(TAIL_LOOP)}, 'phase-3 tail loop over the back'),
  dbg('tail_low', {...tailUp(TAIL_LOW)}, 'the tail laid out behind'),
];
export const CLIPS = [...CLIP_TABLE.map(([name]) => BAKED[name]), ...DBG];
export const SPECS = Object.fromEntries(S.map(s => [s.name, s]));
