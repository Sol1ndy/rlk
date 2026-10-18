// Motion clips of the Moonlit Butterfly (달빛 환영 나비) rig: the contract clips of scratchpad mb2/plan.md "Rig clips"
// (names, lengths, event ticks and the Stage-2 retimes that the module reads from the manifest), authored from the
// footage key frames (mb2/understand/v1..v4.md, model.md §5 motion and sheet 05 kick poses, §8 rest poses) and the
// per-tick pattern timelines of mb2/spec/*.md. Format, retime and sampling: mboss_rig_clips.mjs; channels:
// butterfly_pose.mjs.
//
// Rules every clip keeps (checked by build_mboss_butterfly_rig.mjs):
//   * no horizontal root travel: pos x/z is 0 in every key; the module moves the body (mv/*), the clips carry
//     heights, leans, spins and limbs only;
//   * grounded human poses plant the hooves with the leg IK below (`plant`), so crouches, landings and steps never
//     sink into the floor or slide;
//   * wing poses keep the two wing sets apart (the roots sit 0.42 b beside the spine and the forewing card reaches
//     2.9 b out, so a raised or cupped wing turns its top/front edge toward the midline): every pose below was
//     checked against the other wing set and the body with the textures' alpha.
//
// Two rest poses: HUMAN (standing, crescent chains at her sides, wings and tendrils at scale 0) and BUTTERFLY
// (hovering with the toes 1.2 b up, wings spread). Every clip states its form at tick 0 (channel `form`); the
// transform, release and revert clips switch it at the tick the wings appear or vanish.
import {q, rot, sub} from './mboss_rig_math.mjs';
import {accumulate as accumulateClip, sampleClip as sampleAt, applyRetime} from './mboss_rig_clips.mjs';
import {solve} from './butterfly_pose.mjs';

// world (rig frame) offset from WAIST -> the torso frame of a torso euler (hand positions are authored in it)
const inTorso = (w, torso) => { const Q = q(torso); return rot([-Q[0], -Q[1], -Q[2], Q[3]], [w[0], w[1] - 1.61, w[2]]); };
const k = (t, pose = {}, e) => [t, pose, e];

// ---- rest poses -----------------------------------------------------------------------------------------------
const H_TORSO = [-10, 0, 0];
const H_HANDS = {
  hRA: inTorso([-1.05, 2.92, -.08], H_TORSO), hRAe: [10, 0, -6],          // big crescent, high at her right
  hRB: inTorso([-.86, 2.12, -.12], H_TORSO), hRBe: [10, 0, 18],           // its tail blade below it
  hLA: inTorso([.84, 1.98, -.1], H_TORSO), hLAe: [10, 0, 12],             // smaller crescent at her left hip
  hLB: inTorso([1.0, 1.52, -.04], H_TORSO), hLBe: [10, 0, -24],           // a loose shard below it
};
export const DEFAULT_POSE = {
  pos: [0, 0, 0], rot: [0, 0, 0], pelvis: [0, 0, 0], torso: H_TORSO, head: [8, 0, 0], crest: [0, 0, 0], collar: [0, 0, 0],
  legL: [0, 0, 0], legR: [0, 0, 0], kneeL: 0, kneeR: 0, hockL: 0, hockR: 0,
  fanL: [0, 0, 0], fanR: [0, 0, 0],
  ...H_HANDS, lockR: 0, lockL: 0, hands: 1, flakes: 1,
  fwL: [0, 0, 0], fwR: [0, 0, 0], hwL: [0, 0, 0], hwR: [0, 0, 0], fwS: 0, hwS: 0, glow: 1,
  tuL: [0, 0, 0], tuR: [0, 0, 0], tlL: [0, 0, 0], tlR: [0, 0, 0], tS: 0,
  core: 0, vis: 1, form: 'h', wlook: 'el',
};
export const HUMAN = {...DEFAULT_POSE};
// Butterfly hover: toes 1.2 b above the floor, legs together and folded (hooves down), torso upright, forewings up
// and out (hook tops ≈ 6 b over the floor, the two wing sets 1.5 b apart), hindwings sweeping out and down, ribbons
// hanging, crescents docked at the wing roots as the inner frame claws, fans 15 degrees lower.
const B_TORSO = [2, 0, 0];
const B_HANDS = {
  hRA: inTorso([-.4, 2.4, .16], B_TORSO), hRAe: [-12, 0, 14],
  hRB: inTorso([-.42, 2.02, .3], B_TORSO), hRBe: [-8, 0, 34],
  hLA: inTorso([.36, 2.52, .34], B_TORSO), hLAe: [-12, 0, 14],
  hLB: inTorso([.42, 2.02, .3], B_TORSO), hLBe: [-8, 0, 34],
};
export const B_WINGS = {fwL: [14, -6, 0], fwR: [14, -6, 0], hwL: [10, -6, 0], hwR: [10, -6, 0], fwS: 1, hwS: 1, tuL: [0, 0, 0], tuR: [0, 0, 0], tlL: [4, 0, 0], tlR: [4, 0, 0], tS: 1};
const B_LEGS = {legL: [6, 4, -5], legR: [6, 4, -5], kneeL: -12, kneeR: -9, hockL: 22, hockR: 19};
export const BUTTERFLY = {
  ...DEFAULT_POSE, pos: [0, 1.13, 0], torso: B_TORSO, head: [4, 0, 0], ...B_HANDS, ...B_LEGS,
  fanL: [0, 0, -15], fanR: [0, 0, -15], ...B_WINGS, flakes: 0, form: 'b',
};
const WINGS_OFF = {fwS: 0, hwS: 0, tS: 0, core: 0};

// ---- helpers ---------------------------------------------------------------------------------------------------
// paired channels with the same value on both sides
const both = (L, R, v, w = v) => ({[L]: v, [R]: w});
// legs([hip pitch, knee, hock, hip roll?], right = left)
const legs = (l, r = l) => ({legL: [l[0], 0, l[3] || 0], kneeL: l[1], hockL: l[2], legR: [r[0], 0, r[3] || 0], kneeR: r[1], hockR: r[2]});
const fans = (v, w = v) => ({fanL: v, fanR: w});
const fw = (v, w = v) => ({fwL: v, fwR: w});
const hw = (v, w = v) => ({hwL: v, hwR: w});
const tu = (v, w = v) => ({tuL: v, tuR: w});
const tl = (v, w = v) => ({tlL: v, tlR: w});
const P = (x, y, z) => [0, y, 0];                     // root offset: height only (x/z are the module's travel)
// Leg IK: `plant: {l: [x, y, z], r: [x, y, z], tl, tr}` on a key puts that hoof tip at the rig point (blocks from the
// anchor) with the hoof segment tilted tl/tr degrees toe-forward past its rest tilt; the hip pitch and roll, the knee
// and the hock are solved on the key's accumulated pose (Gauss-Newton on the pose solver), the hip yaw is kept.
export const FEET = {l: [.42, 0, -.06], r: [-.42, 0, -.06]};
const FOOT_TILT0 = 20.85;
function legIK(p, s, target, tilt = 0) {
  const U = s === 'l' ? 'L' : 'R';
  const set = x => ({...p, ['leg' + U]: [x[0], p['leg' + U][1], x[1]], ['knee' + U]: x[2], ['hock' + U]: x[3], ph: 0});
  const res = x => {
    const o = solve(set(x)), hoof = o._legs[s].hoof, d0 = sub(hoof, o['foot_' + s].t);
    const d = rot(q([0, -p.rot[1], 0]), d0);          // measured in her heading (root yaw removed)
    const a = Math.atan2(-d[2], -d[1]) * 180 / Math.PI;
    return [hoof[0] - target[0], hoof[1] - target[1], hoof[2] - target[2], (a - FOOT_TILT0 - tilt) * .01];
  };
  const run = x0 => {
    let x = [...x0];
    for (let it = 0; it < 60; it++) {
      const r0 = res(x), err = Math.hypot(...r0);
      if (err < 1e-4) break;
      const J = [0, 1, 2, 3].map(j => { const y = [...x]; y[j] += .5; return res(y).map((v, i) => (v - r0[i]) / .5); });
      // damped least squares: (J^T J + l I) dx = -J^T r   (J[j][i] = d r_i / d x_j)
      const A = [0, 1, 2, 3].map(a => [0, 1, 2, 3].map(b => J[a].reduce((s2, v, i) => s2 + v * J[b][i], 0) + (a === b ? 1e-4 : 0)));
      const g = [0, 1, 2, 3].map(a => -J[a].reduce((s2, v, i) => s2 + v * r0[i], 0));
      const dx = gauss(A, g);
      const m = Math.max(...dx.map(Math.abs));
      const sc = m > 15 ? 15 / m : 1;
      x = x.map((v, i) => v + dx[i] * sc);
      x[2] = Math.max(-165, Math.min(25, x[2]));
      x[3] = Math.max(-40, Math.min(150, x[3]));
    }
    return x;
  };
  // the previous key's leg first, then a few seeds (a stance, a crouch, a deep fold, a stretched leg)
  const seeds = [[p['leg' + U][0], p['leg' + U][2], p['knee' + U], p['hock' + U]], [0, 0, 0, 0], [30, 0, -50, 30], [70, 0, -120, 80], [-30, 0, -20, 20], [40, 0, -140, 140]];
  let x = null, best = 1e9;
  for (const sd of seeds) {
    const y = run(sd), r = res(y), e = Math.hypot(r[0], r[1], r[2]) + Math.abs(r[3]) * .2;
    if (e < best - 1e-6) { best = e; x = y; }
    if (e < 2e-3) break;
  }
  const r0 = res(x);
  if (Math.hypot(r0[0], r0[1], r0[2]) > .03) throw new Error(`leg IK ${s}: target ${target} missed by ${Math.hypot(r0[0], r0[1], r0[2]).toFixed(3)} b`);
  const rd = v => Math.round(v * 100) / 100;
  return {['leg' + U]: [rd(x[0]), p['leg' + U][1], rd(x[1])], ['knee' + U]: rd(x[2]), ['hock' + U]: rd(x[3])};
}
function gauss(A, b) {
  const n = b.length, M = A.map((r, i) => [...r, b[i]]);
  for (let c = 0; c < n; c++) {
    let pv = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[pv][c])) pv = r;
    [M[c], M[pv]] = [M[pv], M[c]];
    for (let r = 0; r < n; r++) if (r !== c) { const f = M[r][c] / M[c][c]; for (let j = c; j <= n; j++) M[r][j] -= f * M[c][j]; }
  }
  return M.map((r, i) => r[n] / r[i]);
}
// Resolves the `plant` keys of a clip in place (after the clip's other channels are known).
function resolvePlants(clip) {
  let prev = structuredClone(DEFAULT_POSE);
  for (const key of clip.keys) {
    const pose = key[1];
    const acc = {...prev, ...structuredClone(pose)};
    if (pose.plant) {
      const pl = pose.plant;
      delete pose.plant;
      delete acc.plant;
      for (const s of ['l', 'r']) if (pl[s]) Object.assign(pose, legIK(acc, s, pl[s], pl['t' + s] || 0));
      Object.assign(acc, pose);
    }
    prev = acc;
  }
}
// Dense keys sampled from a function of the tick (cycles with per-channel phase lags), linear between ticks.
const cyc = (t0, t1, f, step = 1) => { const out = []; for (let t = t0; t <= t1; t += step) out.push(k(t, f(t), 'l')); return out; };
const wave = (t, period, lag = 0) => Math.cos(2 * Math.PI * (t - lag) / period);
// a root spin about one axis from `from` by `turns` (keys at most 90 degrees apart), other root angles held
function spin(t0, t1, axis, from, turns = 1, base = {}, rot0 = [0, 0, 0], ease = 'l') {
  const out = [], n = Math.max(1, Math.ceil(Math.abs(turns) * 4));
  for (let i = 1; i <= n; i++) {
    const r = [...rot0];
    r[axis] = from + 360 * turns * i / n;
    out.push(k(Math.round(t0 + (t1 - t0) * i / n), {...base, rot: r}, ease));
  }
  return out;
}

// ---- human-form poses -------------------------------------------------------------------------------------------
// fighting stance (v1 f560, sheet 05): knees a little bent, torso 12 degrees forward, crescents ready
const STANCE = {pos: P(0, -.06, 0), torso: [-12, 0, 0], head: [10, 0, 0], ...fans([0, 0, 4]), plant: FEET};
const CROUCH = (dy, extra = {}) => ({pos: P(0, dy, 0), torso: [-26, 0, 0], head: [20, 0, 0], ...fans([0, 0, 14]),
  plant: {l: [.5, 0, -.12], r: [-.5, 0, .08]}, ...extra});
const RUN_LEAN = {torso: [-30, 0, 0], head: [24, 0, 0], ...fans([0, -32, 6]), crest: [-16, 0, 0]};
// crescents trailing behind her while she runs or dashes (torso frame of a -30 degree lean)
const TRAIL_HANDS = {
  hRA: inTorso([-1.0, 2.7, .55], [-30, 0, 0]), hRAe: [40, 0, -10], hRB: inTorso([-.85, 2.05, .5], [-30, 0, 0]), hRBe: [40, 0, 20],
  hLA: inTorso([.8, 2.0, .45], [-30, 0, 0]), hLAe: [40, 0, 14], hLB: inTorso([.95, 1.55, .5], [-30, 0, 0]), hLBe: [40, 0, -20],
};
// the crescent chain lined up vertically at her left side (달빛 점프 tell, chain re-form): three pieces stacked,
// the big crescent stays at her right
const CHAIN_L = {
  hLA: inTorso([1.0, 2.78, -.14], H_TORSO), hLAe: [6, 0, 4], hLB: inTorso([1.08, 2.3, -.14], H_TORSO), hLBe: [6, 0, -8],
  hRB: inTorso([1.0, 1.84, -.14], H_TORSO), hRBe: [6, 0, 172],
};
// the tail blade's way across her front between its idle place at her right and the chain at her left (in front of
// the mane, never through it)
const CHAIN_PASS = {hRB: inTorso([.15, 1.98, -.78], H_TORSO), hRBe: [6, 0, 90]};
// crescents scattered wide (chain re-form start, the entrance burst)
const SCATTER = {
  hRA: inTorso([-1.9, 3.4, -.4], H_TORSO), hRB: inTorso([-1.7, 1.4, .5], H_TORSO), hLA: inTorso([1.9, 3.2, .3], H_TORSO), hLB: inTorso([1.8, 1.2, -.5], H_TORSO),
};
// ---- wing poses (her left side; the right mirrors) ------------------------------------------------------------------
// Each pose was checked with the textures' alpha against the other wing set and the body (gap = the closest approach
// of the two wing sets). A raised or cupped forewing turns its upper inner edge toward the midline, so the raised
// poses lean the tops back or sweep them forward instead of rolling them past about 25 degrees.
const W_REST = {...fw([14, -6, 0]), ...hw([10, -6, 0])};                         // spread hover (gap 1.47 b)
const W_UP = {...fw([13, -6, 16]), ...hw([9, -5, 9])};                           // flap top (gap ≈ 0.8 b)
const W_DOWN = {...fw([14, -6, -18]), ...hw([10, -6, -22])};                     // flap bottom
const W_V = {...fw([34, 14, 32]), ...hw([10, -2, 18])};                          // big-flap top: raised V, faces to the front, tips 7 b up (gap 0.60 b)
const W_CLOSED = {...fw([36, 74, 46]), ...hw([10, -2, 18]), crest: [24, 0, 0]};   // closed up above her head, backs nearly together, the crest leans back (gap 0.43 b)
const W_SNAP = {...fw([10, -12, -32]), ...hw([6, -8, -44])};                     // the snap downstroke
const W_FLAT = {...fw([18, -24, 0]), ...hw([12, -20, -6])};                      // flat, slightly swept (bank, glide entry)
const W_GLIDE = {...fw([24, -30, 8]), ...hw([16, -24, -4])};                     // swept back 30 degrees (gap 0.62 b)
const W_CUP = {...fw([0, 70, 10]), ...hw([0, 65, -20])};                         // cupped forward round her chest (gap 0.62 b)
const W_POD = {...fw([20, 72, 38]), ...hw([25, 62, -44]), fwS: .9, hwS: .9};     // wrapped round her: hooks meet over her head, blades under her (gap 0.16 b)
const W_FOLD = {...fw([36, -18, 38]), ...hw([30, -30, 20]), fwS: .4, hwS: .4, tS: .4};   // folded panels behind the shoulders (transform)
const W_FLUNG = {...fw([6, -10, -22]), ...hw([0, -16, -34]), ...tu([0, 0, 50]), ...tl([0, 0, 20])};   // flung wide, ribbons out (gap 1.7 b)
const W_DART = {...fw([90, -24, 62]), ...hw([-30, -72, 2])};                     // swept back over her back like a dart (dives; gap 0.65 b)
const W_DART_IN = {...fw([63, 25, 54]), ...hw([-10, -36, 10])};                  // between the closed-up wings and the dart
const W_SLAM = {...fw([-20, 55, -40]), ...hw([-10, 55, -40])};                   // slammed forward and down (B3)

// crescents held in front of her chest (the wings close round her root claws in the pod and closed-up poses)
const HANDS_IN = {
  hRA: inTorso([-.34, 2.18, -.42], B_TORSO), hRAe: [-70, 0, 30], hRB: inTorso([-.3, 1.8, -.36], B_TORSO), hRBe: [-60, 0, 50],
  hLA: inTorso([.34, 2.18, -.42], B_TORSO), hLAe: [-70, 0, 30], hLB: inTorso([.3, 1.8, -.36], B_TORSO), hLBe: [-60, 0, 50],
};
// idle_b as a function of the tick (22 t): forewing ±14, hindwing 2.5 t late at 60 %, ribbons 4-6 t late, body bob
const idleB = t => {
  const c = lag => wave(t, 22, lag);
  return {
    ...fw([14, -6, 14 * c(0)]), ...hw([10, -6, 8.4 * c(2.5)]),
    ...tu([0, 0, 8 * c(4)]), ...tl([4 + 4 * c(5), 0, 10 * c(6)]),
    pos: P(0, 1.13 - .12 * c(1), 0), torso: [2 + 1.2 * c(1), 0, 0], head: [4 - c(2), 0, 0], crest: [3 * c(4), 0, 0],
    legL: [6 + 3 * c(3), 4, -5], legR: [6 + 3 * c(3.5), 4, -5], kneeL: -12 - 4 * c(3), kneeR: -9 - 4 * c(3.5),
    ...fans([0, 0, -15 + 3 * c(2)]),
  };
};
const IDLE_B0 = {...BUTTERFLY, ...idleB(0)};
// glide_b as a function of the tick (16 t): held swept wings with a small flutter, legs trailing, ribbons streaming
const glideB = t => {
  const c = lag => wave(t, 16, lag);
  return {
    rot: [-16, 0, 0], ...fw([24, -30, 8 + 4 * c(0)]), ...hw([16, -24, -4 + 3 * c(2)]), pos: P(0, 1.3 + .06 * c(1), 0),
    torso: [4, 0, 0], head: [10, 0, 0], crest: [6 + 3 * c(4), 0, 0], legL: [-22 + 3 * c(3), 4, -5], legR: [-18 + 3 * c(3.5), 4, -5], kneeL: -18, kneeR: -15,
    ...tu([-28 + 4 * c(3), 0, 4 * c(4)]), ...tl([-18 + 6 * c(5), 0, 8 * c(6)]), ...fans([0, -10, -12]),
  };
};
// B2 swing at s, direction d (+1 turns to her right), tilt (root roll during the spin, 0 = flat): a 5 t wind-up
// (turned 75 degrees away, wings swept back and raised, torso coiled) and one full turn with the wings flung wide.
const SWING_YAW = {};
// the wing swept back and raised for the wind-up (her left one when she will spin to her right), the other low
const lead = (d, back, low) => (d > 0 ? [back, low] : [low, back]);
function swing(s, d, tilt) {
  const from = d > 0 ? 0 : 360, wound = d > 0 ? -75 : 435, to = d > 0 ? 360 : 0;
  const y = f => wound + (to - wound) * f;
  SWING_YAW[s] = to;
  return [
    k(s - 3, {rot: [0, from + (wound - from) * .6, tilt * .3], ...fw(...lead(d, [26, -32, 14], [14, -6, -14])), ...hw(...lead(d, [18, -24, 2], [10, -6, -20])), torso: [0, -d * 10, 0], head: [4, d * 14, 0], pos: P(0, 1.25, 0), ...tu([-20, 0, 0])}, 'o'),
    k(s, {rot: [0, wound, tilt * .6], ...fw(...lead(d, [30, -40, 18], [14, -6, -20])), ...hw(...lead(d, [20, -30, 4], [10, -6, -24])), torso: [-2, -d * 16, 0], head: [6, d * 24, 0], pos: P(0, 1.32, 0)}, 'o'),
    k(s + 1, {rot: [0, y(.12), tilt], ...fw([16, -24, 0]), ...hw([8, -20, -22]), ...tu([0, 0, 24]), ...tl([0, 0, 10]), torso: [0, -d * 6, 0], head: [4, d * 8, 0]}, 'i'),
    k(s + 2, {rot: [0, y(.3), tilt], ...W_FLUNG, torso: [2, d * 4, 0], head: [4, 0, 0]}, 'l'),
    k(s + 3, {rot: [0, y(.52), tilt]}, 'l'),
    k(s + 5, {rot: [0, y(.74), tilt], pos: P(0, 1.36, 0)}, 'l'),
    k(s + 7, {rot: [0, y(.92), tilt * .6]}, 'l'),
    k(s + 9, {rot: [0, to, 0], ...W_REST, ...tu([0, 0, 0]), ...tl([4, 0, 0]), torso: B_TORSO, head: [4, 0, 0], pos: P(0, 1.25, 0)}, 'o'),
  ];
}
// hover flaps between the swings (yaw held)
function flapsBetween(a, b) {
  const out = [];
  for (let t = a + 3, up = false; t <= b - 3; t += 5, up = !up) out.push(k(t, {...(up ? W_UP : W_DOWN), pos: P(0, up ? 1.08 : 1.22, 0)}, up ? 'io' : 'i'));
  return out;
}
// hoof targets turned with a root yaw (her stance follows a body turned side-on)
const turnFeet = (yaw, f = FEET) => ({l: rot(q([0, yaw, 0]), f.l), r: rot(q([0, yaw, 0]), f.r)});

export const CLIPS = [
  // ---- human form: idle and locomotion ---------------------------------------------------------------------------
  {name: 'idle_h', len: 40, loop: true, note: 'fighting-stance idle (v1 5.3-7.3 s, f560): knees a little bent, torso 12-14 degrees forward, slow breathing and a weight shift from hip to hip; the crescents and flakes bob (phase), the crest sways', keys: [
    k(0, {...HUMAN, ...STANCE}),
    k(10, {pos: P(0, -.08, 0), pelvis: [0, 0, -2.5], torso: [-13, 0, 1.5], head: [11, 0, -1], crest: [-3, 0, 3], plant: FEET}),
    k(20, {pos: P(0, -.1, 0), pelvis: [0, 0, 0], torso: [-14, 0, 0], head: [12, 0, 0], crest: [-5, 0, 0], ...fans([0, 0, 9]), plant: FEET}),
    k(30, {pos: P(0, -.08, 0), pelvis: [0, 0, 2.5], torso: [-13, 0, -1.5], head: [11, 0, 1], crest: [-3, 0, -3], plant: FEET}),
    k(40, {...HUMAN, ...STANCE}),
  ]},
  {name: 'step_h', len: 16, loop: true, note: 'short strafing step (0.1-0.15 b/t, the module moves the anchor): two light steps in place, hooves lifted 0.3 b, the body dips on each contact and leans over the stance leg', keys: [
    k(0, {...HUMAN, ...STANCE, pos: P(0, -.09, 0)}),
    k(4, {pos: P(0, -.02, 0), pelvis: [0, 0, 3], torso: [-12, 0, 2.5], head: [10, 0, -2], crest: [-2, 0, -4], plant: {r: FEET.r, l: [.44, .3, -.16], tl: 10}}),
    k(8, {pos: P(0, -.09, 0), pelvis: [0, 0, 0], torso: [-13, 0, 0], head: [10, 0, 0], crest: [-4, 0, 0], plant: FEET}),
    k(12, {pos: P(0, -.02, 0), pelvis: [0, 0, -3], torso: [-12, 0, -2.5], head: [10, 0, 2], crest: [-2, 0, 4], plant: {l: FEET.l, r: [-.44, .3, -.16], tr: 10}}),
    k(16, {...HUMAN, ...STANCE, pos: P(0, -.09, 0)}),
  ]},
  // run_h (two strides): a hoof lands ahead of the hips (contact, planted with the leg IK), is pushed back under her
  // (mid-stance, the body at its lowest) and leaves the floor behind her (toe-off); a short flight while the other leg
  // reaches forward. The loop starts at a toe-off, so the forced 2 t blend-in segment (0-2) only skips the flight.
  {name: 'run_h', len: 8, loop: true, blend: 2, note: 'burst-run (0.6-0.8 b/t for about 5 t, v1 23.13-23.40 s): two bounding strides, body 30 degrees forward, fans swept back, crescents trailing; each hoof lands ahead of the hips (2, 6), is pushed back under her (3, 7) and leaves the floor behind her (4, 0), a short flight between the strides', keys: [
    k(0, {...HUMAN, ...RUN_LEAN, ...TRAIL_HANDS, pos: P(0, .02, 0), pelvis: [0, 0, 0], torso: [-28, 0, 0], legR: [62, 0, 0], kneeR: -100, hockR: 50, legL: [-34, 0, 0], kneeL: 10, hockL: 10}),
    k(1, {pos: P(0, .14, 0), pelvis: [0, 3, 0], torso: [-29, 0, 0], ...legs([-30, -96, 70], [48, -50, 32])}, 'l'),
    k(2, {pos: P(0, -.1, 0), pelvis: [0, 6, 0], torso: [-30, 0, 0], legL: [-40, 0, 0], kneeL: -60, hockL: 60, plant: {r: [-.44, 0, -.36], tr: -8}}, 'i'),
    k(3, {pos: P(0, -.16, 0), pelvis: [0, 3, 0], torso: [-31, 0, 0], legL: [16, 0, 0], kneeL: -112, hockL: 66, plant: {r: [-.42, 0, .14]}}, 'l'),
    k(4, {pos: P(0, .02, 0), pelvis: [0, 0, 0], torso: [-28, 0, 0], legL: [62, 0, 0], kneeL: -100, hockL: 50, legR: [-34, 0, 0], kneeR: 10, hockR: 10}, 'l'),
    k(5, {pos: P(0, .14, 0), pelvis: [0, -3, 0], torso: [-29, 0, 0], ...legs([48, -50, 32], [-30, -96, 70])}, 'l'),
    k(6, {pos: P(0, -.1, 0), pelvis: [0, -6, 0], torso: [-30, 0, 0], legR: [-40, 0, 0], kneeR: -60, hockR: 60, plant: {l: [.44, 0, -.36], tl: -8}}, 'i'),
    k(7, {pos: P(0, -.16, 0), pelvis: [0, -3, 0], torso: [-31, 0, 0], legR: [16, 0, 0], kneeR: -112, hockR: 66, plant: {l: [.42, 0, .14]}}, 'l'),
    k(8, {...HUMAN, ...RUN_LEAN, ...TRAIL_HANDS, pos: P(0, .02, 0), pelvis: [0, 0, 0], torso: [-28, 0, 0], legR: [62, 0, 0], kneeR: -100, hockR: 50, legL: [-34, 0, 0], kneeL: 10, hockL: 10}, 'l'),
  ]},
  {name: 'back_h', len: 12, next: 'idle_h', note: 'backing off at walking pace (the anchor moves back): two steps, each hoof lifted and set down behind, torso a little more upright, eyes on the player', keys: [
    k(0, {...HUMAN, ...STANCE}),
    k(3, {pos: P(0, -.02, 0), torso: [-8, 0, 2], head: [6, 0, -2], plant: {l: FEET.l, r: [-.42, .24, .12], tr: -6}}),
    k(6, {pos: P(0, -.08, 0), torso: [-10, 0, 0], head: [8, 0, 0], plant: {l: FEET.l, r: [-.42, 0, .1]}}),
    k(9, {pos: P(0, -.02, 0), torso: [-8, 0, -2], head: [6, 0, 2], plant: {r: [-.42, 0, .1], l: [.42, .24, .12], tl: -6}}),
    k(12, {...HUMAN, ...STANCE}),
  ]},
  {name: 'turn_h', len: 24, next: 'idle_h', note: 'after groggy (v4 27.0-27.5 s): the module turns the anchor (mv/turn, 9 degrees per tick); the clip steps her round from the drooped groggy stance into the fighting stance, crescents still hidden for chain_reform', keys: [
    k(0, {...HUMAN, pos: P(0, -.05, 0), torso: [-6, 0, 0], head: [4, 0, 0], ...fans([0, 0, -15]), hands: 0, plant: FEET}),
    k(4, {pos: P(0, 0, 0), torso: [-8, 0, 2], head: [8, 0, 0], plant: {r: FEET.r, l: [.46, .26, -.1], tl: 8}}),
    k(8, {pos: P(0, -.07, 0), torso: [-9, 0, 0], ...fans([0, 0, -6]), plant: FEET}),
    k(12, {pos: P(0, 0, 0), torso: [-10, 0, -2], head: [9, 0, 0], plant: {l: FEET.l, r: [-.46, .26, -.1], tr: 8}}),
    k(16, {pos: P(0, -.07, 0), torso: [-11, 0, 0], ...fans([0, 0, 0]), plant: FEET}),
    k(20, {pos: P(0, -.02, 0), torso: [-12, 0, 1.5], head: [10, 0, 0], plant: {r: FEET.r, l: [.44, .18, -.08], tl: 5}}),
    k(24, {...STANCE, hands: 0}),
  ]},
  // ---- human form: patterns (H1-H4) ---------------------------------------------------------------------------
  // H1 (v1 9.87-12.40 s, sheet 05): burst-run with the knee chambered from t2, plant at 5, the kick whips up to
  // vertical (hit1 8) and carries her over in a backflip (9-16, the module moves her 1.2 b back), two sideways hops
  // with the kicking leg stretched back (22, 28), the leap (32) into a horizontal flying kick (34), the leg raised
  // overhead with the foot swirl (36) and slammed down as a diagonal axe kick to her front-right (hit2 40), landing
  // (44). The root pitch counts from -360 before the backflip (the same orientation) so it ends at 0.
  {name: 'kick_combo', len: 51, next: 'idle_h', events: {run: 0, plant: 5, hit1: 8, backflip: 9, land1: 16, hop: 22, hop2: 28, leap: 32, swirl: 36, hit2: 40, land: 44},
    note: 'H1 달빛 발차기: burst-run with the knee chambered (0-5), plant, the rising kick whips up to vertical (hit1 8) and carries her over in a backflip (9-16), settle, two sideways hops with the kicking leg stretched back (22, 28), leap (32) into a horizontal flying kick (34), leg raised overhead (36), diagonal axe kick to her front-right (hit2 40), landing (44)', keys: [
      k(0, {...HUMAN, ...RUN_LEAN, ...TRAIL_HANDS, rot: [-360, 0, 0], pos: P(0, .06, 0), ...legs([30, -26, 20], [14, -60, 40])}),
      k(2, {pos: P(0, .2, 0), torso: [-18, 0, 0], head: [16, 0, 0], ...legs([-12, -40, 34], [78, -112, 44]), lockR: .5}),
      k(5, {pos: P(0, -.14, 0), torso: [-4, 0, 0], head: [8, 0, 0], ...fans([0, -10, 26]), ...H_HANDS, crest: [-8, 0, 0], legR: [138, 0, 6], kneeR: -122, hockR: 42, lockR: 1,
        plant: {l: [.36, 0, -.1]}}, 'o'),
      k(7, {rot: [-350, 0, 0], pos: P(0, .06, 0), torso: [0, 0, 0], ...legs([-8, -6, 10], [128, -4, -8, 6])}, 'i'),
      k(8, {rot: [-332, 0, 0], pos: P(0, .34, 0), torso: [2, 0, 0], head: [2, 0, 0], ...fans([0, 0, 36]), crest: [10, 0, 0], ...legs([-14, 30, -30], [125, 40, -40, 8])}, 'i'),
      k(9, {rot: [-296, 0, 0], pos: P(0, .78, 0), ...legs([10, -40, 20], [124, 20, -20, 6])}, 'l'),
      k(10, {rot: [-245, 0, 0], pos: P(0, 1.18, 0), ...legs([70, -110, 40], [110, -90, 30]), lockR: .7}, 'l'),
      k(11, {rot: [-190, 0, 0], pos: P(0, 1.45, 0), ...legs([96, -118, 50], [100, -116, 50])}, 'l'),
      k(12, {rot: [-135, 0, 0], pos: P(0, 1.55, 0), crest: [18, 0, 0]}, 'l'),
      k(13, {rot: [-85, 0, 0], pos: P(0, 1.42, 0), ...legs([80, -110, 40], [84, -114, 44]), lockR: .3}, 'l'),
      k(14, {rot: [-45, 0, 0], pos: P(0, 1.06, 0), ...legs([40, -60, 30], [44, -64, 32])}, 'l'),
      k(15, {rot: [-15, 0, 0], pos: P(0, .52, 0), torso: [-14, 0, 0], head: [16, 0, 0], ...legs([18, -24, 16], [20, -26, 18]), lockR: 0}, 'l'),
      k(16, {rot: [0, 0, 0], ...CROUCH(-.32), torso: [-30, 0, 0], head: [24, 0, 0], crest: [-10, 0, 0], ...fans([0, 0, 18])}, 'i'),
      k(20, {...CROUCH(-.2), torso: [-22, 0, 0], head: [18, 0, 0], crest: [0, 0, 0]}),
      k(21, {pos: P(0, -.24, 0), torso: [-23, -12, 2], head: [19, 11, 0], plant: {l: [.5, 0, -.2], r: [-.56, 0, .45], tr: -15}}),
      // wind-up: low stance, kicking leg stretched back with its hoof on the floor, body coiled to her left, fans flared
      k(22, {pos: P(0, -.26, 0), torso: [-24, -24, 4], head: [20, 22, 0], ...fans([0, -8, 26]), lockR: .6, plant: {l: [.5, 0, -.3], r: [-.55, 0, .72], tr: -30}}),
      k(23, {pos: P(0, .12, 0), torso: [-20, -26, 4], ...legs([40, -70, 40], [-10, -60, 50])}, 'o'),
      k(25, {pos: P(0, -.3, 0), torso: [-24, -24, 4], plant: {l: [.5, 0, -.3], r: [-.55, 0, .72], tr: -30}}, 'i'),
      k(28, {pos: P(0, -.26, 0), torso: [-25, -26, 4]}),
      k(29, {pos: P(0, .12, 0), torso: [-20, -28, 4], ...legs([40, -70, 40], [-10, -60, 50])}, 'o'),
      k(31, {pos: P(0, -.38, 0), torso: [-30, -30, 4], head: [24, 26, 0], ...fans([0, -12, 30]), lockR: 1, plant: {l: [.5, 0, -.3], r: [-.55, 0, .72], tr: -30}}, 'i'),
      // leap into the horizontal flying kick (sheet 05 v1 f694-696: body parallel to the floor, legs toward the target)
      k(32, {pos: P(0, .3, 0), rot: [20, 0, 20], torso: [-10, -10, 0], head: [10, 10, 0], ...legs([-30, -10, 10], [40, -60, 20])}, 'o'),
      k(34, {pos: P(0, .95, 0), rot: [72, 0, 64], torso: [0, 0, 0], head: [-10, -40, 0], crest: [20, 0, 0], ...legs([70, -110, 40], [4, 40, -40]), ...fans([0, -20, 30])}, 'o'),
      k(36, {pos: P(0, 1.3, 0), rot: [18, 0, 14], torso: [-6, 0, 0], head: [6, 0, 0], ...legs([20, -80, 40], [112, 30, -30, 6]), crest: [10, 0, 0]}, 'io'),
      k(38, {pos: P(0, 1.25, 0), rot: [24, 0, 6], torso: [-2, 0, 0], ...legs([12, -70, 40], [124, 40, -40, 6]), ...fans([0, 0, 38])}, 'o'),
      k(39, {pos: P(0, .95, 0), rot: [-4, 6, -4], torso: [-10, 0, 0], ...legs([0, -56, 34], [100, 40, -40, 4])}, 'i'),
      // the axe kick: the leg slams down in front, the body folds forward over it
      k(40, {pos: P(0, .42, 0), rot: [-30, 12, -12], torso: [-22, 0, 0], head: [26, 0, 0], crest: [-16, 0, 0], ...legs([-10, -40, 30], [70, 40, -40]), ...fans([0, -24, 20])}, 'i'),
      k(41, {pos: P(0, .26, 0), rot: [-36, 12, -14], ...legs([-6, -46, 32], [50, 30, -30])}, 'o'),
      k(44, {rot: [-8, 4, -4], ...CROUCH(-.36), torso: [-34, 0, 0], head: [26, 0, 0], crest: [-8, 0, 0], ...fans([0, -8, 20]), lockR: 0, plant: {l: [.5, 0, .15], r: [-.45, 0, -.35]}}, 'i'),
      k(47, {rot: [0, 0, 0], ...CROUCH(-.26), torso: [-26, 0, 0], head: [20, 0, 0], crest: [0, 0, 0], plant: {l: [.5, 0, .1], r: [-.45, 0, -.25]}}),
      k(51, {...HUMAN, ...STANCE}),
    ]},
  // H2 (v1 25.33-28.60 s, v4 28.45-31.30 s): the crescent chain lines up at her left (tell 0-13, the module adds
  // tell/on), pivot, the 360 degree low sweep with the left leg stretched at knee height (13-19), recovery, the
  // spiral jump (33, two rising turns, the module glides 3.5 b), the orb at her raised right foot (45) as she tips
  // into a forward somersault, the axe kick down (52), impact (55), landing (59). The root yaw counts up from -1080
  // and the pitch down from 360 (the same orientation) so both end at 0.
  {name: 'kick_jump', len: 65, next: 'idle_h', events: {tell: 0, sweep: 13, sweep_end: 19, jump: 33, orb: 45, disc: 45, kick: 52, impact: 55, land: 59},
    note: 'H2 달빛 점프: the crescent chain lines up at her left (tell 0-13), pivot, 360 degree low sweep with the left leg at knee height (13-19), recovery, spiral jump with two rising turns (33-44), the orb forms at her raised right foot (45, disc = orb) as she tips into a forward somersault, axe kick down (52), impact 55, landing 59', keys: [
      k(0, {...HUMAN, ...STANCE, rot: [360, -1080, 0], ...fans([0, 0, 10])}),
      k(3, {...CHAIN_PASS, hLA: CHAIN_L.hLA, hLAe: CHAIN_L.hLAe}, 'o'),
      k(6, {pos: P(0, -.16, 0), torso: [-18, -10, 0], head: [14, 10, 0], ...CHAIN_L, plant: {l: [.5, 0, -.08], r: [-.4, 0, .02]}}),
      k(10, {pos: P(0, -.36, 0), torso: [-26, -16, 0], head: [20, 16, 0], ...fans([0, -6, 18]), plant: {l: [.62, 0, -.2], r: [-.22, 0, .04]}}),
      // the sweep: pivot on the right hoof under her, the left leg stretched out low; the band starts at her left
      k(12, {pos: P(0, -.62, 0), torso: [-34, -10, 6], head: [26, 10, 0], ...fans([0, -18, 24]), ...CHAIN_L, legL: [20, 0, 78], kneeL: -6, hockL: 26, plant: {r: [-.18, 0, .02]}}),
      ...[[13, -1030], [14, -950], [15, -870], [16, -800], [17, -750], [18, -725]].map(([t, y], i) => k(t, {rot: [360, y, 0], plant: {r: [-.18, 0, .02]}}, i ? 'l' : 'i')),
      k(19, {rot: [360, -720, 0], pos: P(0, -.55, 0), legL: [20, 0, 60], kneeL: -20, plant: {r: [-.18, 0, .02]}}, 'o'),
      k(22, {...CROUCH(-.38), torso: [-28, 0, 0], ...H_HANDS, hRB: inTorso([-.15, 1.98, -.78], H_TORSO), hRBe: [6, 0, 90]}),
      k(27, {...CROUCH(-.16), torso: [-16, 0, 0], head: [12, 0, 0], hRB: H_HANDS.hRB, hRBe: H_HANDS.hRBe}),
      k(31, {...CROUCH(-.42), torso: [-24, 0, 0], head: [22, 0, 0], ...fans([0, 0, -10])}, 'i'),
      // the spiral jump: two rising turns, legs together, crescents flung out
      k(33, {pos: P(0, .55, 0), rot: [360, -700, 0], torso: [-4, 0, 0], head: [6, 0, 0], ...fans([0, -10, 24]), ...legs([-14, -20, 20], [6, -50, 30])}, 'o'),
      ...[35, 37, 39, 41, 43].map((t, i) => k(t, {rot: [360, -560 + 140 * i, 0], pos: P(0, [1.25, 1.75, 2.1, 2.3, 2.4][i], 0)}, 'l')),
      k(44, {rot: [350, 0, 0], pos: P(0, 2.45, 0), ...legs([-6, -40, 20], [70, -60, 20])}, 'l'),
      // the orb at her raised foot, the forward somersault carrying it overhead, the axe kick down
      k(45, {rot: [330, 0, 0], pos: P(0, 2.5, 0), torso: [-14, 0, 0], ...legs([0, -50, 30], [150, -10, 0]), lockR: 1}, 'o'),
      k(47, {rot: [260, 0, 0], pos: P(0, 2.55, 0), ...legs([60, -110, 40], [156, -6, 0])}, 'l'),
      k(49, {rot: [180, 0, 0], pos: P(0, 2.5, 0)}, 'l'),
      k(50, {rot: [130, 0, 0], pos: P(0, 2.42, 0), ...legs([50, -100, 40], [150, -6, 0])}, 'l'),
      k(51, {rot: [70, 0, 0], pos: P(0, 2.3, 0), torso: [-8, 0, 0], ...legs([36, -84, 40], [134, -4, 0])}, 'l'),
      k(52, {rot: [14, 0, 0], pos: P(0, 2.08, 0), torso: [-18, 0, 0], head: [24, 0, 0], crest: [-12, 0, 0], ...legs([14, -64, 34], [80, 0, 0]), ...fans([0, -24, 24])}, 'i'),
      k(53, {rot: [-16, 0, 0], pos: P(0, 1.8, 0), torso: [-20, 0, 0], ...legs([10, -56, 30], [54, -2, 0])}, 'o'),
      k(55, {rot: [-10, 0, 0], pos: P(0, 1.05, 0), torso: [-16, 0, 0], ...legs([14, -30, 20], [18, -24, 14]), lockR: 0}, 'i'),
      k(59, {rot: [0, 0, 0], ...CROUCH(-.38), torso: [-30, 0, 0], head: [24, 0, 0], crest: [0, 0, 0]}, 'i'),
      k(65, {...HUMAN, ...STANCE}),
    ]},
  // H3 (v2 2.95-6.47 s, sheet 05 v2 f262-276): the mote charge in a gathering crouch (0-8), coil side-on with the
  // kicking leg cocked (8-10), the dash low and stretched (10-12, the module moves her 5-6 b), the high side kick with
  // the crescent on the shin (kick 15), one full turn with the leg out (the ring 19), landing and recovery.
  {name: 'dash_kick', len: 50, next: 'idle_h', events: {charge: 0, dash: 10, dash_end: 12, kick: 15, ring: 19},
    note: 'H3 달빛 돌진: mote charge in a gathering crouch (0-8), coil side-on with the kicking leg cocked (8-10), dash low and stretched (10-12, the module moves the anchor 5-6 b), high side kick with the crescent on the shin (kick 15), one full turn with the leg out (ring 19), landing (22) and recovery', keys: [
      k(0, {...HUMAN, ...STANCE}),
      k(6, {...CROUCH(-.22), torso: [-20, 0, 0], ...fans([0, 0, 24]), hRA: inTorso([-.8, 2.6, -.3], H_TORSO), hLA: inTorso([.7, 2.0, -.3], H_TORSO)}),
      k(9, {rot: [0, -50, 0], pos: P(0, -.26, 0), torso: [-28, 10, 0], head: [22, 40, 0], ...fans([0, -18, 26]), legR: [70, 0, 6], kneeR: -110, hockR: 50,
        hRA: inTorso([-1.45, 2.2, .3], H_TORSO), lockR: .4, plant: {l: rot(q([0, -50, 0]), [.4, 0, 0])}}),
      k(11, {rot: [-24, -50, 0], pos: P(0, .14, 0), torso: [-30, 10, 0], head: [30, 40, 0], ...RUN_LEAN, ...TRAIL_HANDS, ...legs([-50, -24, 30], [84, -116, 46]), lockR: .8}, 'i'),
      k(13, {rot: [6, -76, 0], pos: P(0, .32, 0), torso: [-8, 0, -6], head: [6, 60, 0], ...fans([0, -30, 10]), ...H_HANDS, legL: [10, 0, 0], kneeL: -70, hockL: 40, legR: [30, 0, 60], kneeR: -120, hockR: 50, lockR: 1}, 'o'),
      // the side kick: the right leg straight out to her right (toward the player), the body leaning away
      k(15, {rot: [0, -86, 0], pos: P(0, .42, 0), torso: [-4, 0, -24], head: [0, 70, 20], crest: [0, 0, -18], legR: [8, 0, 92], kneeR: 40, hockR: -40, ...fans([0, -34, 20])}, 'i'),
      ...[[16, -40], [17, 50], [18, 140], [19, 220], [20, 290], [21, 340]].map(([t, y]) => k(t, {rot: [0, y, 0], pos: P(0, .42 - (t - 15) * .04, 0),
        ...(t === 20 ? {lockR: .5} : t === 21 ? {legR: [36, 0, 44], kneeR: 4, hockR: -6, lockR: .2, legL: [24, 0, 4], kneeL: -60, hockL: 30} : {})}, 'l')),
      k(22, {rot: [0, 360, 0], ...CROUCH(-.34), torso: [-30, 0, 0], head: [24, 0, 0], crest: [0, 0, 0], lockR: 0}, 'o'),
      k(26, {...CROUCH(-.3), torso: [-26, 0, 0]}),
      k(36, {...CROUCH(-.14), torso: [-18, 0, 0], head: [14, 0, 0]}),
      k(50, {...HUMAN, ...STANCE, rot: [0, 360, 0]}),
    ]},
  // H4 (v2 12.80-16.60 s): the low cat-like crouch with the kicking leg glowing (0-8), the glint (9), rear-up with the
  // leg raised high (12-14), the stomp (16) launches the vertical blade (17) and she pushes off into a slow, high
  // backflip (17-34, apex 2.6 b; the module moves her 2.5 b back), landing crouch (38).
  {name: 'vacuum', len: 41, next: 'idle_h', events: {crouch: 0, tell: 9, glint: 9, stomp: 16, blade: 17, backflip: 17, land: 38},
    note: 'H4 광폭한 진공: low cat-like crouch, the kicking leg glows (0-8), glint (9), rear-up with the leg raised high (12-14), stomp (16) launches the vertical blade (17), high slow backflip 17-34 (apex 2.6 b), landing crouch (38)', keys: [
      k(0, {...HUMAN, ...STANCE}),
      k(3, {...CROUCH(-.28), torso: [-24, 0, 0], head: [20, 0, 0], plant: {l: [.52, 0, -.14], r: [-.47, 0, .16], tr: 5}}),
      k(6, {...CROUCH(-.46), torso: [-36, 0, 0], head: [30, 0, 0], ...fans([0, -14, -8]), crest: [-6, 0, 0], plant: {l: [.6, 0, -.2], r: [-.5, 0, .3], tr: 10}}),
      k(9, {pos: P(0, -.5, 0), torso: [-38, 0, 0], head: [32, 0, 0], plant: {l: [.6, 0, -.2], r: [-.5, 0, .3], tr: 10}}),
      k(13, {pos: P(0, .28, 0), torso: [2, 0, 0], head: [6, 0, 0], ...fans([0, 0, 24]), legL: [-10, 0, 4], kneeL: -20, hockL: 20, legR: [124, 0, 6], kneeR: -70, hockR: 30, lockR: .6}, 'o'),
      k(14, {pos: P(0, .32, 0), torso: [6, 0, 0], legR: [134, 0, 6], kneeR: -50, hockR: 20}),
      k(16, {pos: P(0, -.24, 0), torso: [-26, 0, 0], head: [22, 0, 0], ...fans([0, -10, 30]), lockR: .9, plant: {l: [.5, 0, .25], r: [-.36, 0, -.6], tr: -10}}, 'i'),
      k(18, {rot: [24, 0, 0], pos: P(0, .5, 0), torso: [-6, 0, 0], head: [8, 0, 0], ...legs([-20, -20, 20], [-10, -14, 20]), lockR: .4}, 'o'),
      k(21, {rot: [70, 0, 0], pos: P(0, 1.5, 0), torso: [0, 0, 0], ...legs([40, -90, 40], [44, -94, 42]), lockR: 0}, 'o'),
      k(24, {rot: [130, 0, 0], pos: P(0, 2.25, 0), ...legs([96, -118, 50], [100, -118, 50])}, 'l'),
      k(27, {rot: [195, 0, 0], pos: P(0, 2.6, 0)}, 'l'),
      k(30, {rot: [260, 0, 0], pos: P(0, 2.45, 0)}, 'l'),
      k(33, {rot: [325, 0, 0], pos: P(0, 1.9, 0), ...legs([50, -80, 40], [54, -84, 40])}, 'l'),
      k(35, {rot: [352, 0, 0], pos: P(0, 1.2, 0), torso: [-12, 0, 0], head: [14, 0, 0], ...legs([14, -24, 16], [16, -26, 16])}, 'o'),
      k(38, {rot: [360, 0, 0], ...CROUCH(-.36), torso: [-30, 0, 0], head: [24, 0, 0]}, 'i'),
      k(41, {...CROUCH(-.24), torso: [-22, 0, 0], head: [18, 0, 0]}),
    ]},
  {name: 'groggy_h', len: 40, loop: true, note: 'groggy (300 t in the pattern, v4 11.45-26.60 s): the module turns the body away from the player; she stands slack, torso 6 degrees forward, head low, fans drooped, crescents hidden, a slow sway; the flakes drift', keys: [
    k(0, {...HUMAN, pos: P(0, -.05, 0), torso: [-6, 0, 0], head: [4, 0, 0], crest: [-6, 0, 0], ...fans([0, 0, -15]), hands: 0, plant: FEET}),
    k(20, {pos: P(0, -.08, 0), pelvis: [0, 0, 1.5], torso: [-8, 0, -1.5], head: [6, 0, 1.5], crest: [-8, 0, 3], ...fans([0, 0, -17]), plant: FEET}),
    k(40, {pos: P(0, -.05, 0), pelvis: [0, 0, 0], torso: [-6, 0, 0], head: [4, 0, 0], crest: [-6, 0, 0], ...fans([0, 0, -15]), plant: FEET}),
  ]},
  // ---- entrance --------------------------------------------------------------------------------------------------
  // v1 0.00-5.27 s: hidden in the cocoon prop until the burst (79); revealed curled 3.6 b up, the drop with a slight
  // tumble, legs reaching for the floor (80-89), the landing crouch with the legs wide and the crescents spread (90),
  // rising to the stance by 106.
  {name: 'entrance', len: 106, next: 'idle_h', events: {nameplate: 57, glow: 61, whiteout: 71, burst: 79, land: 90, stand: 106},
    note: 'hidden inside the cocoon prop until the burst at 79 (rig/prop/cocoon); revealed curled 3.6 b up, she drops with a slight tumble, lands in a wide crouch at 90 with the crescents spread and stands up by 106', keys: [
      k(0, {...HUMAN, vis: 0, pos: P(0, 3.6, 0), torso: [-40, 0, 0], head: [30, 0, 0], ...legs([100, -118, 60]), ...fans([0, 0, -30]), hands: .6}),
      k(78, {vis: 0}),
      k(79, {vis: 1}, 'l'),
      k(82, {pos: P(0, 3.35, 0), rot: [-14, 0, 4], torso: [-30, 0, 0], head: [22, 0, 0], ...legs([70, -110, 50], [80, -120, 50]), ...fans([0, 0, 10]), hands: 1, ...SCATTER}, 'o'),
      k(86, {pos: P(0, 2.0, 0), rot: [6, 0, -3], torso: [-16, 0, 0], head: [12, 0, 0], ...legs([20, -40, 30], [26, -46, 30]), ...fans([0, 0, 24])}, 'i'),
      k(89, {pos: P(0, .55, 0), rot: [0, 0, 0], torso: [-20, 0, 0], ...legs([12, -24, 20], [14, -26, 20])}, 'i'),
      k(90, {...CROUCH(-.5), torso: [-40, 0, 0], head: [30, 0, 0], ...fans([0, 0, 30]), crest: [-14, 0, 0],
        hRA: inTorso([-1.45, 2.6, -.2], H_TORSO), hRB: inTorso([-1.3, 1.7, .1], H_TORSO), hLA: inTorso([1.3, 2.2, -.1], H_TORSO), hLB: inTorso([1.45, 1.4, .1], H_TORSO),
        plant: {l: [.62, 0, -.12], r: [-.62, 0, .14]}}, 'i'),
      k(93, {pos: P(0, -.56, 0), torso: [-44, 0, 0], head: [32, 0, 0], crest: [-4, 0, 0], plant: {l: [.62, 0, -.12], r: [-.62, 0, .14]}}, 'o'),
      k(100, {pos: P(0, -.4, 0), torso: [-34, 0, 0], head: [26, 0, 0], ...fans([0, 0, 20]), plant: {l: [.62, 0, -.12], r: [-.62, 0, .14]}}),
      k(106, {...HUMAN, ...STANCE}),
    ]},
  // ---- transform -----------------------------------------------------------------------------------------------
  // v2 24.10-24.70 s (sheet 09 row 3): the lime sheath (core glow) while she sinks a little and rises, the folded
  // flat-lime wing panels behind the shoulders at 4 (form switch), the core flash (5), the light sphere (6), the
  // wings unfold over 8 t (4-12) while she lifts into the hover, the ripple rings (9), fully spread (12), the element
  // look from 14, then one big settling flap into the idle_b phase.
  {name: 'transform', len: 30, next: 'idle_b', events: {glow: 0, open: 4, sphere: 6, rings: 9, spread: 12},
    note: 'human -> butterfly: the cocoon glow (core) while she sinks and rises, the folded flat-lime wing panels behind the shoulders at 4 (form switch), core flash 5, light sphere at 6 (달빛 고치 is applied there), the wings unfold over 8 t (4-12) while she lifts into the hover, ripple rings 9, fully spread 12, element look from 14, one big settling flap', keys: [
      k(0, {...HUMAN, ...STANCE, core: 1, ...W_FOLD, fwS: 0, hwS: 0, tS: 0}),
      k(2, {pos: P(0, -.12, 0), torso: [-16, 0, 0], head: [14, 0, 0], core: 1.3, ...fans([0, 0, -6]), plant: {l: [.4, 0, -.06], r: [-.4, 0, -.06]}}),
      k(3, {pos: P(0, .08, 0), torso: [-4, 0, 0], head: [2, 0, 0], crest: [14, 0, 0], core: 1.6, ...legs([-4, -10, 10]), wlook: 'flat'}, 'o'),
      k(4, {form: 'b', ...W_FOLD, pos: P(0, .22, 0), torso: [0, 0, 0], ...legs([0, -12, 14]), ...B_HANDS, hands: .8, flakes: .7}, 'o'),
      k(5, {core: 2.4, ...fans([0, 0, 10])}),
      k(6, {core: 3, flakes: 0, pos: P(0, .42, 0), fwS: .6, hwS: .6, tS: .6, ...fw([24, -14, 14]), ...hw([22, -20, 10]), ...B_LEGS, legL: [4, 4, -5], legR: [4, 4, -5]}, 'l'),
      k(9, {core: 2, pos: P(0, .82, 0), fwS: .88, hwS: .88, tS: .88, ...fw([12, -10, -8]), ...hw([10, -10, -12]), ...tu([0, 0, 30]), crest: [8, 0, 0]}, 'l'),
      k(12, {...BUTTERFLY, ...W_FLUNG, core: 1.2, pos: P(0, 1.18, 0), wlook: 'flat', torso: [4, 0, 0], head: [0, 0, 0]}, 'o'),
      k(14, {wlook: 'el', core: 0}),
      k(18, {...W_V, pos: P(0, 1.02, 0), ...tu([0, 0, 0]), ...tl([4, 0, 0]), torso: B_TORSO, head: [4, 0, 0]}),
      k(21, {...W_SNAP, pos: P(0, 1.3, 0)}, 'i'),
      k(25, {...W_REST, pos: P(0, 1.18, 0)}),
      k(30, {...IDLE_B0}),
    ]},
  // ---- butterfly form: idle and travel -----------------------------------------------------------------------------
  // model.md §5.1: period 22 t, the forewing ±14 degrees about the root's forward axis, the hindwing 2.5 t behind at
  // 60 %, the ribbons 4 t behind swinging ±10 degrees, the body 0.12 b lower at the top of the upstroke and higher
  // after the downstroke, the dangling legs and the fans trail the beat.
  {name: 'idle_b', len: 22, loop: true, note: 'hover flap (22 t): forewing ±14 degrees, hindwing 2.5 t behind at 60 %, ribbons 4 t behind, body bob ±0.12 b rising on the downstroke, legs and fans trail the beat', keys: [
    k(0, {...BUTTERFLY, ...idleB(0)}),
    ...cyc(1, 22, idleB),
  ]},
  {name: 'glide_b', len: 16, loop: true, blend: 4, note: 'gliding travel (model.md §5.1): body pitched 16 degrees forward, wings held swept back 30 degrees with a small flutter, legs trailing, ribbons streaming and waving', keys: [
    k(0, {...BUTTERFLY, ...glideB(0)}),
    ...cyc(1, 16, glideB, 1),
  ]},
  // ---- butterfly form: patterns (B1-B5) ---------------------------------------------------------------------------
  // B1 (v2 35.20-37.92 s, v3 R): lift with one big flap (1-7), the bank to 80 degrees with the left wing hanging
  // like a blade (8-11), the swoop 0.5 b off the floor past the player's side with the wing edge sweeping through
  // (hit 15), the pull-up and climb to 3 b (16-26), fluttering rolls and quick flaps (28-48), back to the hover.
  {name: 'wing_strike', len: 55, next: 'idle_b', events: {bank: 0, dive: 8, hit: 15},
    note: 'B1 우아한 날개: lift with one big flap (0-7), bank 80 degrees with the left wing hanging as a blade (8-11), swoop low past the player (12-14, the module glides 7 t from dive 8), the wing edge sweeps through at hit 15, pull-up and climb to 3 b, fluttering rolls and quick flaps, back to the hover', keys: [
      k(0, {...IDLE_B0}),
      k(3, {...W_V, pos: P(0, 1.55, 0), rot: [8, 0, 0], ...tu([10, 0, 0])}, 'o'),
      k(6, {...W_SNAP, pos: P(0, 1.85, 0), rot: [0, 0, 0], ...tu([-10, 0, 0])}, 'i'),
      k(8, {...W_FLAT, rot: [-24, 0, -48], pos: P(0, 1.7, 0), ...tu([-20, 0, 10]), ...tl([-10, 0, 0]), ...legs([-20, -20, 20])}),
      k(11, {rot: [-46, 8, -76], pos: P(0, 1.2, 0), ...fw([20, -24, -2]), ...hw([12, -20, -16])}, 'i'),
      k(13, {rot: [-58, 18, -82], pos: P(0, 1.1, 0), ...tu([-30, 0, 10]), ...tl([-20, 0, 0])}, 'i'),
      k(15, {rot: [-56, 38, -84], pos: P(0, 1.06, 0), ...fw([20, -30, -4]), ...hw([12, -24, -18])}, 'l'),
      k(17, {rot: [-36, 46, -62], pos: P(0, 1.3, 0), ...W_FLAT}, 'o'),
      k(20, {rot: [-12, 34, -24], pos: P(0, 2.1, 0), ...W_V, ...tu([10, 0, 0]), ...tl([4, 0, 0]), ...B_LEGS}),
      k(23, {rot: [0, 20, 0], pos: P(0, 2.7, 0), ...W_SNAP}, 'i'),
      k(27, {rot: [4, 10, 0], pos: P(0, 3.0, 0), ...W_UP}),
      k(31, {rot: [0, -12, 24], pos: P(0, 2.9, 0), ...W_DOWN}, 'i'),
      k(35, {rot: [0, 8, -20], pos: P(0, 2.75, 0), ...W_UP}),
      k(38, {rot: [0, 14, -18], pos: P(0, 2.6, 0), ...W_DOWN}, 'i'),
      k(42, {rot: [0, -6, 14], pos: P(0, 2.3, 0), ...W_UP}),
      k(45, {rot: [0, -4, 8], pos: P(0, 1.95, 0), ...W_DOWN}, 'i'),
      k(49, {rot: [0, 0, 0], pos: P(0, 1.45, 0), ...W_UP}),
      k(52, {pos: P(0, 1.25, 0), ...W_DOWN}, 'i'),
      k(55, {...IDLE_B0}),
    ]},
  // B2 (v3 4.30-10.70 s): each swing has a 5 t wind-up (the body turned 75 degrees away, wings swept back, coiled),
  // then a full spinning turn with the wings flung wide that throws the fire crescents (s+2..s+6); swings 1 and 3 spin
  // on a diagonal (tilted 26 degrees), 2 and 4 flat at chest height, alternating directions; hover flaps between.
  {name: 'wing_barrage', len: 117, next: 'idle_b', events: {swing1: 5, swing2: 31, swing3: 69, swing4: 94},
    note: 'B2 화염 날개의 습격 (Pyro look): four spinning wing swings at 5/31/69/94, each after a 5 t wind-up (body turned 75 degrees away, wings swept back); one full turn with the wings flung wide throws the 5 fire crescents (s+2..s+6); swings 1 and 3 spin on a diagonal, 2 and 4 flat; alternating directions; hover flaps between', keys: [
      k(0, {...IDLE_B0}),
      ...swing(5, 1, 26), ...flapsBetween(14, 25),
      ...swing(31, -1, 0), ...flapsBetween(40, 63),
      ...swing(69, 1, -26), ...flapsBetween(78, 88),
      ...swing(94, -1, 0), ...flapsBetween(103, 112),
      k(117, {...IDLE_B0}),
    ]},
  // B3 (v3 10.70-14.60 s, sheet 09 row 5): the wings V-up and the lean back (tell, 0-6), a big downstroke (6-11) and
  // the upstroke (11-15), the rise with the wings closed above her (15-20), the head-first dive as a dart (20-25), the
  // wing slam forward-down (26), the flame fan (28-32), a low glide banked to her right (33-43, the module glides her
  // 4.5 b to her right), settling flaps back to the hover.
  {name: 'flap_dive', len: 59, next: 'idle_b', events: {rise: 0, dive: 20, slam: 26, fan: 28, glide: 33},
    note: 'B3 날개 휩쓸개 (Pyro look): wings V-up and lean back (tell 0-6), big downstroke (6-11), upstroke (11-15), rise with the wings closed above her (15-20), head-first dart dive (20-25), wing slam forward-down at 26, flame fan 28-32, low glide banked to her right (33-43), settling flaps', keys: [
      k(0, {...IDLE_B0}),
      k(4, {...W_V, rot: [12, 0, 0], pos: P(0, 1.3, 0), ...tu([12, 0, 0])}, 'o'),
      k(6, {rot: [10, 0, 0], pos: P(0, 1.32, 0)}),
      k(9, {...W_SNAP, rot: [0, 0, 0], pos: P(0, 1.62, 0), ...tu([-14, 0, 0])}, 'i'),
      k(11, {...W_DOWN, pos: P(0, 1.7, 0)}),
      k(15, {...W_V, pos: P(0, 1.95, 0), rot: [6, 0, 0], ...tu([10, 0, 0]), ...HANDS_IN}),
      k(18, {...W_CLOSED, ...HANDS_IN, pos: P(0, 2.3, 0), rot: [10, 0, 0], torso: [6, 0, 0], head: [-4, 0, 0]}, 'o'),
      k(19, {pos: P(0, 2.3, 0), rot: [6, 0, 0]}),
      k(20, {...W_DART_IN, rot: [-22, 0, 0], pos: P(0, 2.22, 0), torso: [0, 0, 0], head: [8, 0, 0], crest: [8, 0, 0]}, 'i'),
      k(22, {...W_DART, ...B_HANDS, rot: [-62, 0, 0], pos: P(0, 1.85, 0), torso: [-6, 0, 0], head: [16, 0, 0], crest: [0, 0, 0], ...tu([-30, 0, 0]), ...tl([-20, 0, 0]), ...legs([-30, -10, 10])}, 'i'),
      k(24, {rot: [-82, 0, 0], pos: P(0, 1.3, 0)}, 'i'),
      k(25, {rot: [-62, 0, 0], pos: P(0, 1.05, 0), ...fw([35, 15, 11]), ...hw([-15, -8, -19]), ...tu([0, 0, 0]), ...tl([0, 0, 0])}, 'i'),
      k(26, {...W_SLAM, rot: [-30, 0, 0], pos: P(0, .95, 0), torso: [-10, 0, 0], head: [20, 0, 0], ...tu([20, 0, 0]), ...tl([10, 0, 0]), ...B_LEGS}, 'i'),
      k(28, {rot: [-22, 0, 0], pos: P(0, 1.0, 0)}),
      k(32, {rot: [-16, 0, 0], pos: P(0, 1.02, 0), ...fw([-4, 46, -30]), ...hw([4, 50, -34])}),
      k(35, {...W_GLIDE, rot: [-12, 0, 22], pos: P(0, .82, 0), torso: B_TORSO, head: [6, 0, 0], ...tu([-24, 0, 10]), ...tl([-16, 0, 6]), ...legs([-24, -16, 16])}),
      k(41, {rot: [-10, 0, 18], pos: P(0, .86, 0), ...fw([24, -30, 2])}),
      k(44, {...W_V, rot: [0, 0, 0], pos: P(0, 1.0, 0), ...tu([6, 0, 0]), ...tl([4, 0, 0]), ...B_LEGS}),
      k(46, {...W_SNAP, pos: P(0, 1.25, 0)}, 'i'),
      k(50, {...W_UP, pos: P(0, 1.12, 0)}),
      k(52, {...W_DOWN, pos: P(0, 1.22, 0)}, 'i'),
      k(55, {...W_UP, pos: P(0, 1.08, 0)}),
      k(59, {...IDLE_B0}),
    ]},
  // B4 (v3 20.22-24.20 s, sheet 08 G): wings to flat while she glides in (0-4), the wrap: both pairs curl forward
  // into a ring round the chest core (5-15), snap open (16-18) and orb 1 (19), a hover beat, the cocoon ball: the
  // wings wrapped round her curled body (30-42), open (42-45), orb 2 from her side with a twist (46), recovery.
  {name: 'coco', len: 76, next: 'idle_b', events: {wrap: 5, orb1: 19, ball: 30, ball_open: 42, orb2: 46},
    note: 'B4 달빛 축복: wings to flat (0-4), the wings curl forward into a ring round the chest core (wrap 5-15, charge), snap open (16-18), orb 1 at 19 (rig/prop/orb), the cocoon ball: wings wrapped round her curled body (30-42; prop/pod optional), open (42-45), orb 2 from her side with a twist (46), recovery to the hover', keys: [
      k(0, {...IDLE_B0}),
      k(4, {...W_FLAT, rot: [-8, 0, 0], pos: P(0, 1.2, 0), ...tu([-10, 0, 0])}),
      k(7, {...W_CUP, rot: [0, 0, 0], pos: P(0, 1.15, 0), torso: [-8, 0, 0], head: [10, 0, 0], core: .8, ...tu([0, 30, 0]), ...tl([0, 0, -10])}),
      k(12, {...W_CUP, ...fw([-4, 74, 12]), core: 1.25, pos: P(0, 1.08, 0)}),
      k(16, {core: 1.6, pos: P(0, 1.05, 0), torso: [-10, 0, 0]}),
      k(18, {...W_FLUNG, core: .5, pos: P(0, 1.2, 0), torso: [4, 0, 0], head: [0, 0, 0]}, 'i'),
      k(21, {core: 0}),
      k(24, {...W_REST, pos: P(0, 1.15, 0), ...tu([0, 0, 0]), ...tl([4, 0, 0])}),
      k(26, {...W_UP, pos: P(0, 1.05, 0), ...fans([0, 8, -28])}),
      k(30, {...W_POD, ...HANDS_IN, pos: P(0, 1.2, 0), torso: [-24, 0, 0], head: [20, 0, 0], ...legs([56, -96, 50]), core: 1.2, ...fans([0, 12, -35]), ...tu([0, 40, -10]), ...tl([0, 0, -20])}),
      k(36, {pos: P(0, 1.28, 0), torso: [-26, 0, 0], core: 1.5}),
      k(42, {pos: P(0, 1.22, 0), torso: [-24, 0, 0], core: 1.6}),
      k(43, {...hw([12, 20, -62]), ...fw([14, 30, 10]), pos: P(0, 1.2, 0)}, 'i'),
      k(44, {...W_FLUNG, ...B_LEGS, ...B_HANDS, torso: [4, 0, 0], head: [2, 0, 0], ...fans([0, 6, -30]), core: .6, pos: P(0, 1.2, 0)}, 'i'),
      k(46, {rot: [0, -22, 0], torso: [2, 10, 0], core: 0, ...fans([0, 0, -15])}, 'o'),
      k(50, {rot: [0, -6, 0], ...W_REST, ...tu([0, 0, 0]), ...tl([4, 0, 0])}),
      k(56, {rot: [0, 0, 0], ...W_UP, pos: P(0, 1.05, 0)}),
      k(62, {...W_DOWN, pos: P(0, 1.22, 0)}, 'i'),
      k(68, {...W_UP, pos: P(0, 1.04, 0)}),
      k(72, {...W_DOWN, pos: P(0, 1.2, 0)}, 'i'),
      k(76, {...IDLE_B0}),
    ]},
  // B5 (v3 32.83-38.28 s, v4 replay): the wings closed up (0-5), the swoop as a dart past the player (5-9), the
  // climb (9-14), the whirl: two cartwheel turns with the wings flung and flicking (18-30), the cup (31), the flash,
  // the X glint and the ring cage (35-43), the pod wrap as she sinks a little (44-52), the snap open (52) and the
  // detonation with the wings flung wide and the ribbons streaming (53), the hover 2 b up with slow beats (63-87), the
  // wings shrink and go flat lime (87), shatter (91), the human form drops (92) and lands (96).
  {name: 'release', len: 96, next: 'idle_h', events: {fold: 0, swoop: 5, climb: 9, whirl: 18, cup: 31, flash: 35, glint: 37, xglint: 37, rings: 38, cage: 38, wrap: 44, snap: 52, detonation: 53, hover: 63, shrink: 87, flat: 87, shatter: 91, revert: 92, land: 96},
    note: 'B5 달빛 해제: wings closed up (fold 0-5), dart swoop past the player (5-9), climb (9-14), whirl: two cartwheel turns with the wings flung and flicking (18-30), cup (31), flash 35, X glint 37, ring cage 38-43, pod wrap while she sinks (44-52), snap open (52), DETONATION 53 with the wings flung wide and the ribbons streaming, hover 2 b up with slow beats (63-87), the wings shrink and go flat lime (87), shatter (91), the human form drops (92) and lands (96); the form switches to human at 92', keys: [
      k(0, {...IDLE_B0}),
      k(3, {...W_CLOSED, ...HANDS_IN, crest: [30, 0, 0], rot: [-8, 0, 0], pos: P(0, 1.35, 0), torso: [4, 0, 0], head: [-6, 0, 0]}, 'o'),
      k(4, {pos: P(0, 1.3, 0), rot: [-14, 0, 0], head: [12, 0, 0], crest: [10, 0, 0]}),
      k(5, {...W_DART_IN, pos: P(0, 1.2, 0), rot: [-24, 0, 0], head: [14, 0, 0], crest: [6, 0, 0]}, 'i'),
      k(7, {...W_DART, ...B_HANDS, rot: [-58, 0, 0], pos: P(0, .75, 0), torso: [-4, 0, 0], head: [14, 0, 0], crest: [0, 0, 0], ...tu([-30, 0, 0]), ...tl([-20, 0, 0]), ...legs([-26, -12, 12])}, 'i'),
      k(8, {...fw([90, -24, 30]), ...hw([-20, -60, 0]), rot: [-42, 0, 0], pos: P(0, .78, 0)}),
      k(9, {...fw([70, -24, 10]), ...hw([-10, -50, -4]), rot: [-26, 0, 0], pos: P(0, .95, 0), torso: B_TORSO, head: [6, 0, 0]}, 'o'),
      k(11, {...W_GLIDE, rot: [-10, 0, 0], pos: P(0, 1.4, 0)}),
      k(13, {...W_V, rot: [0, 0, 0], pos: P(0, 2.0, 0), ...tu([8, 0, 0]), ...tl([4, 0, 0]), ...B_LEGS, core: .6}),
      k(15, {...W_SNAP, pos: P(0, 2.55, 0)}, 'i'),
      k(17, {...W_FLUNG, pos: P(0, 2.9, 0), core: .8}),
      ...spin(18, 30, 2, 0, 2, {pos: P(0, 3.05, 0)}, [0, 0, 0], 'l').map(([t, p, e], i) => k(t, {...p, ...fw(i % 2 ? [6, -10, -30] : [8, -14, -12]), ...hw(i % 2 ? [2, -20, -50] : [4, -22, -36])}, e)),
      k(31, {...W_CUP, ...HANDS_IN, rot: [0, 0, 720], pos: P(0, 3.0, 0), torso: [-6, 0, 0], head: [8, 0, 0], core: .9, ...tu([0, 30, 0]), ...tl([0, 0, -10])}, 'o'),
      k(36, {pos: P(0, 2.96, 0), core: 1.1, ...HANDS_IN}),
      k(40, {...fw([-4, 74, 14]), pos: P(0, 2.9, 0), core: 1.3}),
      k(44, {...W_POD, ...HANDS_IN, pos: P(0, 2.84, 0), torso: [-22, 0, 0], head: [18, 0, 0], ...legs([50, -90, 46]), ...fans([0, 12, -35]), ...tu([0, 40, -10]), ...tl([0, 0, -20]), core: 1.5}),
      k(51, {pos: P(0, 2.66, 0), torso: [-26, 0, 0], core: 2.6}),
      k(52, {...fw([12, 20, 6]), ...hw([10, 20, -14]), ...tu([0, 16, 30]), ...tl([0, 0, 6]), torso: [-10, 0, 0], core: 2.8}, 'i'),
      k(53, {...W_FLUNG, ...B_HANDS, ...tu([0, 0, 64]), ...tl([0, 0, 24]), ...B_LEGS, ...fans([0, 0, -6]), torso: [10, 0, 0], head: [-8, 0, 0], crest: [16, 0, 0], pos: P(0, 2.82, 0), core: 3}, 'i'),
      k(58, {core: 0, pos: P(0, 2.7, 0)}),
      k(63, {...W_FLUNG, ...tu([0, 0, 30]), ...tl([0, 0, 12]), torso: B_TORSO, head: [4, 0, 0], crest: [0, 0, 0], ...fans([0, 0, -15]), pos: P(0, 2.3, 0)}),
      ...[69, 75, 81].flatMap(t => [k(t - 3, {...W_UP, ...tu([0, 0, 10]), pos: P(0, 2.12, 0)}), k(t, {...W_DOWN, pos: P(0, 2.24, 0)}, 'i')]),
      k(87, {...W_REST, pos: P(0, 2.18, 0), wlook: 'flat'}),
      k(90, {fwS: .5, hwS: .5, tS: .5, ...fw([8, -8, -10]), ...hw([6, -6, -14]), pos: P(0, 2.14, 0)}),
      k(91, {fwS: .45, hwS: .45, tS: .45}),
      k(92, {...WINGS_OFF, form: 'h', wlook: 'el', ...H_HANDS, hands: 0, flakes: 1, torso: [-6, 0, 0], head: [6, 0, 0], ...legs([8, -26, 20], [12, -30, 22]), ...fans([0, 0, 0]), pos: P(0, 1.75, 0)}),
      k(95, {pos: P(0, .4, 0), torso: [-14, 0, 0], ...legs([14, -20, 18], [16, -22, 18])}, 'i'),
      k(96, {...CROUCH(-.3), hands: 0, torso: [-26, 0, 0], head: [20, 0, 0]}, 'i'),
    ]},
  // butterfly -> human without the blast (S3 §D): hover rising to 2 b with slow flaps, the wings shrink (30), go
  // flat lime (32) and shatter (36), the human form drops (37) and lands (43).
  {name: 'revert', len: 43, next: 'idle_h', events: {shrink: 30, flat: 32, shatter: 36, revert: 37, land: 43},
    note: 'butterfly -> human without the blast: hover rising to 2 b with slow flaps, the wings shrink (30), go flat lime (32) and shatter (36), the human form drops (37) and lands (43); the form switches to human at 37', keys: [
      k(0, {...IDLE_B0}),
      ...[6, 18].flatMap(t => [k(t, {...W_DOWN, pos: P(0, 1.3 + t * .03, 0)}, 'i'), k(t + 6, {...W_UP, pos: P(0, 1.2 + t * .035, 0)})]),
      k(30, {...W_REST, pos: P(0, 2.0, 0)}),
      k(32, {fwS: .6, hwS: .6, tS: .6, wlook: 'flat'}),
      k(33, {fwS: .5, hwS: .5, tS: .5, ...fw([8, -8, -10]), ...hw([6, -6, -14])}),
      k(36, {fwS: .45, hwS: .45, tS: .45, pos: P(0, 1.98, 0)}),
      k(37, {...WINGS_OFF, form: 'h', wlook: 'el', ...H_HANDS, hands: 0, flakes: 1, torso: [-6, 0, 0], head: [6, 0, 0], ...legs([8, -26, 20], [12, -30, 22]), ...fans([0, 0, 0]), pos: P(0, 1.7, 0)}),
      k(42, {pos: P(0, .3, 0), torso: [-14, 0, 0], ...legs([14, -20, 18], [16, -22, 18])}, 'i'),
      k(43, {...CROUCH(-.3), hands: 0, torso: [-26, 0, 0], head: [20, 0, 0]}, 'i'),
    ]},
  // ---- death and the chain re-form ---------------------------------------------------------------------------------
  // Not in the footage (plan.md "Death", spec S4): from either form she staggers back (the wings go flat lime and
  // shrink away over the 10 t blend; the module's shatter at 10), staggers forward, the knees buckle (20), she sinks
  // to one knee (30), the crescents and flakes sink and fade (30-64), then she dissolves: everything scales out about
  // her hips while rising 0.6 b (50-100). The wing-side parts and the chest glow start at a small non-zero scale and
  // reach 0 at the blend tick, so their first key ends there (hidden throughout, they would form one 100 t key: from
  // the butterfly form the wings would shrink over 100 t and drift off the falling body).
  {name: 'death', len: 100, blend: 10, events: {stagger: 0, shatter: 10, kneel: 30, dissolve: 50, gone: 100},
    note: 'from either form: she staggers back while the wings go flat lime and shrink away over the 10 t blend (shatter 10), staggers forward, the knees buckle (20), she sinks to one knee (30), the crescents and flakes fade (30-64), then dissolves into the rising motes (scale out about her hips, 50-100); call kill after 100', keys: [
      k(0, {...HUMAN, ...WINGS_OFF, fwS: .1, hwS: .1, tS: .1, core: .1, form: 'h', wlook: 'flat', pos: P(0, 0, 0), torso: [6, 0, 0], head: [-8, 0, 0], ...fans([0, 0, 30]), plant: FEET}),
      k(10, {...WINGS_OFF, wlook: 'el', pos: P(0, -.04, 0), torso: [10, 0, 3], head: [-12, 0, -4], crest: [14, 0, 0], ...fans([0, -10, 34]), hands: .8, plant: {l: FEET.l, r: [-.46, 0, .34], tr: -10}}),
      k(18, {pos: P(0, -.22, 0), torso: [-24, 0, -2], head: [18, 0, 3], crest: [-10, 0, 0], ...fans([0, 0, 10]), hands: .7, plant: {l: [.44, 0, -.2], r: [-.46, 0, .3]}}, 'i'),
      k(21, {pos: P(0, -.3, 0), torso: [-27, 0, -2], head: [20, 0, 3], plant: {l: [.44, 0, -.24], r: [-.45, 0, .4], tr: -20}}),
      k(25, {pos: P(0, -.46, 0), torso: [-32, 0, -3], head: [24, 0, 4], hands: .55, plant: {l: [.43, 0, -.32], r: [-.44, .1, .55], tr: -50}}),
      k(30, {pos: P(0, -.72, 0), torso: [-38, 0, -3], head: [28, 0, 4], crest: [-14, 0, 0], ...fans([0, 0, -26]), hands: .45,
        plant: {l: [.42, 0, -.42], r: [-.42, .12, .75], tr: -100}}, 'i'),
      k(50, {pos: P(0, -.76, 0), torso: [-44, 0, -4], head: [34, 0, 4], ...fans([0, 0, -32]), hands: .25, plant: {l: [.42, 0, -.42], r: [-.42, .12, .75], tr: -100}}),
      k(64, {hands: 0, flakes: 0, torso: [-42, 0, -2], head: [30, 0, 2]}),
      k(100, {vis: 0, pos: P(0, -.16, 0), torso: [-30, 0, 0], head: [20, 0, 0]}, 'i'),
    ]},
  // v4 27.40-28.70 s: the four crescent plates fly in from around her and stack into a vertical chain at her left
  // side with a low thud (+6), a small flourish, then they take their idle places.
  {name: 'chain_reform', len: 18, next: 'idle_h', events: {stack: 6},
    note: 'the crescent chain re-forms after groggy: the four plates fly in from around her (scale 0 -> 1) and stack into a vertical chain at her left (stack 6, the thud), a small flourish, then they take their idle places', keys: [
      k(0, {...HUMAN, ...STANCE, hands: 0, ...SCATTER}),
      k(4, {hands: .7, hRA: inTorso([-1.4, 3.1, -.3], H_TORSO), hRB: inTorso([.2, 2.0, -.7], H_TORSO), hLA: inTorso([1.3, 3.0, .1], H_TORSO), hLB: inTorso([1.3, 1.4, -.3], H_TORSO), torso: [-12, -8, 0], head: [10, 8, 0]}, 'o'),
      k(6, {hands: 1.06, ...CHAIN_L, hRA: H_HANDS.hRA, torso: [-14, -10, 0], head: [12, 10, 0], ...fans([0, 0, 16]), pos: P(0, -.09, 0), plant: FEET}, 'i'),
      k(11, {hands: 1, torso: [-13, -6, 0], head: [11, 6, 0], ...fans([0, 0, 10]), pos: P(0, -.07, 0), plant: FEET}),
      k(18, {...HUMAN, ...STANCE}),
    ]},
];
// Wind-up retiming table (as the Guardian's; empty: the clips are authored on the pattern timelines).
export const RETIME = {};
applyRetime(CLIPS, RETIME);
for (const c of CLIPS) resolvePlants(c);

// ---- sampling ------------------------------------------------------------------------------------------------------
export const accumulate = clip => accumulateClip(clip, DEFAULT_POSE);
// idle phase of the crescent/flake bob: one cycle per 40 t (a loop: whole cycles per loop)
export const bobPhase = (clip, t) => (clip.loop ? t / clip.len * Math.max(1, Math.round(clip.len / 40)) : t / 40);
export const sampleClip = (clip, t, ks = accumulate(clip)) => sampleAt(clip, t, ks, {defaults: DEFAULT_POSE, discrete: ['form', 'wlook'], phase: bobPhase});
// The two rest poses as sampled poses (for spawn, renders and checks).
export const restPose = which => ({...(which === 'b' ? BUTTERFLY : HUMAN), ph: 0});
