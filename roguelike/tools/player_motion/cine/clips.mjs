// The cutscene actor's 5 clips (lane H3; tools/dev/plan/combat/hr_design.md §3 shot tables, §4.2, §4.3), as channel tracks for
// tools/player_motion/cine/lib.mjs. The player plays Eve's part of the reference video (video_notes.md §2.3-§2.6): walking in
// and standing in CS0; the blade lock, the shove, the hit and the knee in CS1; the deflect, the grab, the hilt strike, the two
// cuts, the throw and the kick in the repel; the ground and aerial duel of the ending. The clips run on the sequence clock
// (`#sq hr` -> `#cavT cine`), so every tick below is a tick of §3's tables. Positions are ST(r, u, f): r to the actor's right, u up,
// f forward (toward her); the stage origin is the avatar's feet.
//
// Everything a sequence or her clip relies on is data here: LIMIT (api.ACTOR_LIMIT), CONTACT (§4.3, the actor's side of each
// row), and per clip len / grip / beats / handback / two (two-hand spans) / slides (spans where the soles may drag) / steps
// (footfall ticks, for the step sounds) / her (where the shot table puts her feet: the sheets' stand-in post, nothing else).
import {REST, SWORD, Tracks, solve, frames, points, shoulders, groundHip, A, rot} from './lib.mjs';

export const LIMIT = {fwd: 2.5, back: 1.5, side: 1.5, cs0_back: 6.0, air: 7.0};
const add = (a, b) => a.map((x, i) => x + b[i]);
const sub = (a, b) => a.map((x, i) => x - b[i]);
const mulv = (a, s) => a.map(x => x * s);
const norm = v => { const m = Math.hypot(...v); return v.map(x => x / m); };
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const mix = (a, b, u) => a.map((x, i) => x + (b[i] - x) * u);

// §4.3, the actor's side: `blade` = the blade's centre line (root..tip) through the point, `tip` = the blade's point there,
// `hilt` = the hilt (pommel..guard) there, hand_l / foot_r = that grip point / sole there, `under` = the named point under it
// (within r sideways, below[0]..below[1] lower: her forearm lies on the shoulder).
export const K = {
  K1: [0, 1.45, .75], KR: [0, 1.55, .65], KW: [.15, 1.95, .85], KH: [0, 2.20, 1.10], KS: [.20, 1.50, 1.60], KK: [0, .35, 2.7],
  KG: [0, 2.05, 2.35], KE2: [0, 1.5, 2.1], KE5: [0, 1.5, 3.25], KA1: [0, 6.9, 2.55], KA2: [0, 7.3, 2.6], KA3: [0, 6.8, 2.5], KA4: [0, 6.9, 2.6],
};
export const CONTACT = {
  K1: {clip: 'cs1', ticks: [10, 30], p: K.K1, what: 'blade', tol: .08},
  KR: {clip: 'repel', ticks: [0, 26], p: K.KR, what: 'blade', tol: .08},
  KW: {clip: 'repel', ticks: [36, 48], p: K.KW, what: 'hand_l', tol: .12},
  KH: {clip: 'repel', ticks: [49, 49], p: K.KH, what: 'hilt', tol: .12},
  KS: {clip: 'repel', ticks: [70, 78], p: K.KS, what: 'under', point: 'shoulder_r', r: .25, below: [.08, .40], tol: .001},
  KK: {clip: 'repel', ticks: [129, 129], p: K.KK, what: 'foot_r', tol: .12},
  KG: {clip: 'ending', ticks: [52, 52], p: K.KG, what: 'tip', tol: .08},
  KE2: {clip: 'ending', ticks: [56, 80], p: K.KE2, what: 'blade', tol: .08},
  KE5: {clip: 'ending', ticks: [190, 204], p: K.KE5, what: 'blade', tol: .08},
  KA1: {clip: 'ending', ticks: [228, 228], p: K.KA1, what: 'blade', tol: .08},
  KA2: {clip: 'ending', ticks: [262, 262], p: K.KA2, what: 'blade', tol: .08},
  KA3: {clip: 'ending', ticks: [286, 286], p: K.KA3, what: 'blade', tol: .08},
  KA4: {clip: 'ending', ticks: [298, 304], p: K.KA4, what: 'blade', tol: .08},
};

// ---- the vocabulary ---------------------------------------------------------------------------------------------------------
// arms by angles [x, y, z, elbow]: x + swings forward, z lifts outward (right arm -, left arm +)
const ARM = {
  lowR: [8, 0, -7, 14], lowL: [3, 0, 7, 9],          // hanging; the right hand carries the sword low
  balL: [-18, 0, 22, 38],                              // the free left arm of a stance: a little back and out, bent
  outL: [10, 0, 55, 30], backL: [-45, 0, 30, 25], guardL: [35, 10, 15, 80],
};
const SW_LOW = [-130, 0, 0];                           // in the low right hand: the point forward and down
// the avatar's idle: what every clip hands back in (standing, facing her, the arms down, the sword low)
export const IDLE_CHANNELS = {...REST, aR: ARM.lowR, aL: ARM.lowL, sw: SW_LOW};

const feet = (root, R, L) => ({fR: [root[0] + R[0], 0, root[2] + R[1]], fL: [root[0] + L[0], 0, root[2] + L[1]]});
const STAND = {R: [.125, 0], L: [-.125, 0]};
// the fighting stance: the right (sword) foot leads, the feet apart; flatHip() puts the pelvis where both shins stand upright
const READY = {R: [.2, .26], L: [-.2, -.24]};
// a sword held in space: the grip point, the blade's direction, the side its edge faces (the broad face's normal follows)
const blade = (hilt, dir, edge = [0, 0, 1]) => { const d = norm(dir); return {hR: hilt, wR: 1, bd: d, bn: norm(cross(d, edge)), ws: 1}; };
// the blade-lock convention of §3.0, the actor's half of the X: hilt 0.3 below K, 0.3 to its right, 0.25 before it
const ELBOWS_OUT = {pL: [-1, -.4, .35], pR: [1, -.45, .1]};       // two hands on the hilt: the elbows point out and forward, clear of the chest
const lock = Kp => { const hilt = add(Kp, [.3, -.3, -.25]); return {...blade(hilt, sub(Kp, hilt), [0, 0, 1]), ...ELBOWS_OUT}; };
const pommelOf = c => add(c.hR, mulv(norm(c.bd), SWORD.left));

// The pelvis offset (hip) that keeps both shins upright over planted feet at the given drop: with no ankle the sole only lies
// flat under an upright shin. Solves the two knee circles in the plan view; falls back to the midpoint when they do not meet.
function flatHip(c, drop) {
  const yaw = c.rot[1] * Math.PI / 180, R = Math.sqrt(Math.max(0, .375 ** 2 - (.375 - drop) ** 2));
  // hip joints in the plan (r, f) relative to the pelvis centre, the figure turned by yaw (+ = to its right)
  const jr = [.125 * Math.cos(yaw), -.125 * Math.sin(yaw)], jl = [-jr[0], -jr[1]];
  const a = [c.fR[0] - jr[0], c.fR[2] - jr[1]], b = [c.fL[0] - jl[0], c.fL[2] - jl[1]];     // pelvis centre must be R from both
  const d = Math.hypot(b[0] - a[0], b[1] - a[1]), m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
  let P = m;
  if (d > 1e-6 && d <= 2 * R) { const h = Math.sqrt(R * R - d * d / 4), n = [-(b[1] - a[1]) / d, (b[0] - a[0]) / d]; const s = n[1] <= 0 ? 1 : -1; P = [m[0] + s * n[0] * h, m[1] + s * n[1] * h]; }
  // into the yaw frame, relative to the root
  const w = [P[0] - c.root[0], P[1] - c.root[2]];
  return [w[0] * Math.cos(yaw) - w[1] * Math.sin(yaw), -drop, w[0] * Math.sin(yaw) + w[1] * Math.cos(yaw)];
}
// Fit the body to a grip: move the pelvis (r, f) and turn / lean the torso until the right hand reaches the hilt and, with two
// hands, the left reaches its place under it. A fixed pattern search (deterministic), kept near the pose it starts from.
function fit(c, {two = c.two > .5, reach = .55, vars = ['hr', 'hf', 'ty', 'tp', 'tr'], left = null} = {}) {
  const tR = c.hR, tL = two ? pommelOf(c) : left;
  const get = x => ({...c, hip: [c.hip[0] + x.hr, c.hip[1], c.hip[2] + x.hf], tor: [c.tor[0] + x.tp, c.tor[1] + x.ty, c.tor[2] + x.tr]});
  const cost = x => {
    const s = shoulders(get(x)), e = (S, T) => { const d = Math.hypot(...sub(S, T)); return Math.max(0, d - reach) ** 2 + Math.max(0, .26 - d) ** 2; };
    return 60 * (e(s.R, tR) + (tL ? e(s.L, tL) : 0)) + .15 * (x.hr ** 2 + x.hf ** 2) + 2e-5 * (x.ty ** 2 + x.tp ** 2 + 2 * x.tr ** 2);
  };
  let x = {hr: 0, hf: 0, ty: 0, tp: 0, tr: 0}, best = cost(x);
  for (let step = 1; step > .01; step /= 2) {
    for (let pass = 0; pass < 4; pass++) for (const v of vars) for (const s of [1, -1]) {
      const y = {...x, [v]: x[v] + s * step * (v[0] === 'h' ? .12 : 14)}, cy = cost(y);
      if (cy < best - 1e-12) { x = y; best = cy; }
    }
  }
  return get(x);
}
// a step: the sole lifts and lands (a parabola `lift` high) between t0 and t1
const step = (tr, side, t0, t1, to, lift = .12) => tr.mv(t0, t1, {['f' + side]: [to[0], 0, to[1]]}, 'io', {['f' + side]: [0, lift, 0]});
// set a full pose at a tick: every channel of the pose is keyed (the others keep running)
const pose = (tr, t, p, ease = 'io') => tr.at(t, p, ease);
const move = (tr, t0, t1, p, ease = 'io') => tr.mv(t0, t1, p, ease);

// ---- stances at a root -----------------------------------------------------------------------------------------------------------
// standing with the sword low (the idle's channels at a root)
const standAt = root => ({root, ...feet(root, STAND.R, STAND.L), hip: [0, 0, 0], rot: [0, 0, 0], tor: [0, 0, 0], head: [0, 0, 0],
  aR: ARM.lowR, aL: ARM.lowL, wR: 0, wL: 0, ws: 0, sw: SW_LOW, two: 0, lfR: 0, lfL: 0, kR: REST.kR, kL: REST.kL});
// the ready stance: feet apart, the right foot leading, the knees soft, the body a quarter turned, the sword in a middle guard
function readyAt(root, {drop = .07, yaw = -12, hand = [.16, .98, .40], dir = [-.12, .42, .9]} = {}) {
  const c = {...REST, root, ...feet(root, READY.R, READY.L), rot: [0, yaw, 0], tor: [-6, 4, 0], head: [2, -yaw - 4, 0], aL: ARM.balL, wL: 0, two: 0,
    kR: [.25, 0, 1], kL: [-.45, 0, 1], lfR: 0, lfL: 0, ...blade(add(root, hand), dir, [0, -1, 0]), pR: [.7, -.6, -.5]};
  c.hip = flatHip(c, drop);
  return c;
}


const O = [0, 0, 0];
const EZ = {l: u => u, io: u => u * u * (3 - 2 * u), i: u => u * u, o: u => 1 - (1 - u) ** 2};
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const slerpDir = (a, b, u) => { a = norm(a); b = norm(b); const th = Math.acos(Math.max(-1, Math.min(1, dot(a, b)))); if (th < 1e-4) return a; const s = Math.sin(th); return a.map((x, i) => (x * Math.sin((1 - u) * th) + b[i] * Math.sin(u * th)) / s); };
// A cut: the grip and the blade's direction swept between two held poses with a key on every tick (a sparse key would let the
// client cut the corner: a swing would read as a thrust). The broad face lies in the swing's plane, so the edge leads.
function sweep(tr, t0, t1, from, to, {ease = 'io', via = null, n = null, hvia = null} = {}) {
  const axis = n || norm(cross(norm(from.bd), norm(via || to.bd)));
  tr.hold(t0, 'hR', 'bd', 'bn');
  for (let t = t0 + 1; t <= t1; t++) {
    const u = EZ[ease]((t - t0) / (t1 - t0));
    const dir = via ? (u < .5 ? slerpDir(from.bd, via, u * 2) : slerpDir(via, to.bd, u * 2 - 1)) : slerpDir(from.bd, to.bd, u);
    const h = hvia ? (u < .5 ? mix(from.hR, hvia, u * 2) : mix(hvia, to.hR, u * 2 - 1)) : mix(from.hR, to.hR, u);
    tr.at(t, {hR: h, bd: dir, bn: axis}, 'l');
  }
}
// The switch from the sword carried by the arm's angles to the sword held in space: at tick t the held values are set to
// what is shown, then the weights rise over n ticks, so nothing jumps.
function toIK(tr, t, n = 2) {
  const p = solve(tr.sample(t), t).pose, f = frames(p), P = points(p);
  tr.hold(t - 1, 'hR', 'bd', 'bn');
  tr.at(t, {hR: P.hilt, bd: norm(sub(P.tip, P.hilt)), bn: A(rot(f.weapon.q, [0, 0, -1]))}, 'l');
  tr.hold(t, 'wR', 'ws');
  tr.at(t + n, {wR: 1, ws: 1}, 'l');
}
// the low carry as a held pose at a root (what the arm's angles of the idle show), for the moves that end in the idle
const LOW_HELD = root => ({hR: add(root, [.413, .829, .164]), bd: norm([.038, -.307, .951]), bn: norm([0, .951, .307])});
// back to the arm's angles of the idle over t0..t1 (the held pose first comes to the low carry)
function toIdleArms(tr, t0, t1, root) {
  tr.mv(t0, t1 - 3, LOW_HELD(root), 'io');
  tr.hold(t1 - 4, 'aR', 'sw');
  tr.hold(t1 - 3, 'wR', 'ws', 'two', 'wL');
  tr.at(t1 - 3, {aR: ARM.lowR, sw: SW_LOW}, 'l');
  tr.at(t1, {wR: 0, ws: 0, two: 0, wL: 0}, 'l');
}
// the grip carried with a moving root: a key on every tick at root(t) + the offset blended from relA to relB
function carry(tr, t0, t1, relA, relB, ease = 'io') {
  tr.hold(t0, 'hR');
  for (let t = t0 + 1; t <= t1; t++) tr.at(t, {hR: add(tr.val('root', t), mix(relA, relB, EZ[ease]((t - t0) / (t1 - t0))))}, 'l');
}
// the switch back to the arm's angles (a flip, a hang): the angles first, then the weights fall over n ticks
function toFK(tr, t, aR, sw, n = 2) { tr.hold(t - 1, 'aR', 'sw'); tr.at(t, {aR, sw}, 'l'); tr.hold(t, 'wR', 'ws'); tr.at(t + n, {wR: 0, ws: 0}, 'l'); }
const stance = (root, R, L, {drop = .06, yaw = 0} = {}) => { const c = {root, ...feet(root, R, L), rot: [0, yaw, 0]}; return {...c, hip: flatHip({...REST, ...c}, drop)}; };

// ============================================================================================================================
// cs0: 1440 t (§3.1). Stands at f -6.0 under the arrival blindness 0-20; walks in 20-100 (0.075 b/t; a 16-tick cycle: the 24
// of the design cannot plant a sole at this speed with these legs); stops, looks ahead 100-110; idle to 666; lifts the head
// toward her 670-690, the weight forward 690-700; idle to 1230; the head follows her leap 1236-1258, a guarded half step back
// 1250-1259 (f -0.3); raises the sword into a middle guard 1262-1284; steps forward to the mark 1390-1400; lowers into the
// idle 1430-1440.
const CS0_PLANTS = Array.from({length: 10}, (_, k) => 24 + 8 * k);
function cs0(tr) {
  const v = .075, f0 = -6, rootAt = t => [0, 0, f0 + v * (t - 20)];
  pose(tr, 0, {...standAt([0, 0, f0]), head: [-4, 0, 0], br: 1});
  tr.hold(20, 'root'); tr.at(100, {root: O}, 'l');
  step(tr, 'L', 20, 24, [-.11, rootAt(24)[2] + .3], .07);
  CS0_PLANTS.slice(1).forEach((T, i) => { const side = i % 2 === 0 ? 'R' : 'L'; step(tr, side, T - 8, T, [side === 'R' ? (T === 96 ? .125 : .11) : -.11, rootAt(T)[2] + .3], .11); });
  step(tr, 'L', 96, 102, [-.125, 0], .07);
  tr.hold(20, 'hip', 'tor', 'aL', 'aR', 'head');
  for (let t = 22; t <= 100; t += 2) {
    const w = Math.min(1, (t - 20) / 4, (104 - t) / 8), a = 2 * Math.PI * (t - 24) / 16;
    tr.at(t, {hip: [-.025 * Math.sin(a) * w, -(.0675 + .0175 * Math.cos(2 * a)) * w, 0], tor: [-3 * w, -5 * Math.cos(a) * w, 0],
      aL: [3 - 16 * Math.cos(a) * w, 0, 7, 9 + 8 * w], aR: [8 + 5 * Math.cos(a) * w, 0, -7, 14], head: [-4 + 3 * w, 5 * Math.cos(a) * w, 0]}, 'l');
  }
  tr.at(106, {hip: [0, 0, 0], tor: [0, 0, 0], aL: ARM.lowL, aR: ARM.lowR, head: [1, 0, 0]}, 'o');
  tr.at(110, {head: [-3, 0, 0]}, 'io');
  // 670-700 the guest looks up at her; the weight comes forward with a half step
  tr.mv(670, 690, {head: [4, 0, 0]}, 'io');
  step(tr, 'L', 690, 698, [-.125, .14], .05);
  tr.mv(690, 700, {hip: [0, -.012, .06], tor: [-3, 0, 0]}, 'io');
  // 1234-1258 the head follows her leap; 1250-1259 a guarded half step back
  tr.mv(1232, 1236, {wl: 1, look: [0, 1.7, 13.5]}, 'io');
  tr.at(1246, {look: [0, 6.0, 10.2]}, 'io'); tr.at(1258, {look: [0, 1.0, 6.5]}, 'io'); tr.at(1284, {look: [0, 1.6, 6.5]}, 'io');
  const R1 = [0, 0, -.3], g = readyAt(R1, {drop: .05, yaw: -10});
  tr.mv(1250, 1258, {root: R1}, 'io');
  step(tr, 'L', 1250, 1255, [g.fL[0], g.fL[2]], .06);
  step(tr, 'R', 1255, 1259, [g.fR[0], g.fR[2]], .04);
  tr.mv(1250, 1259, {hip: g.hip, rot: g.rot, tor: [-4, 4, 0], kR: g.kR, kL: g.kL}, 'io');
  // 1262-1284 the sword comes up into a middle guard
  toIK(tr, 1262, 2);
  tr.mv(1264, 1284, {hR: g.hR, bd: g.bd, bn: g.bn, pR: g.pR, aL: ARM.balL, tor: g.tor, br: .4}, 'io');
  // 1390-1400 steps forward to the mark, the guard held
  const g0 = readyAt(O, {drop: .05, yaw: -10});
  tr.mv(1390, 1400, {root: O, hR: g0.hR}, 'io');
  step(tr, 'R', 1390, 1395, [g0.fR[0], g0.fR[2]], .08);
  step(tr, 'L', 1395, 1400, [g0.fL[0], g0.fL[2]], .08);
  // 1430-1440 lowers into the avatar's idle
  step(tr, 'L', 1430, 1434, [-.125, 0], .06);
  step(tr, 'R', 1434, 1438, [.125, 0], .05);
  tr.mv(1430, 1439, {hip: [0, 0, 0], rot: [0, 0, 0], tor: [0, 0, 0], kR: REST.kR, kL: REST.kL, aL: ARM.lowL, wl: 0, head: [0, 0, 0], br: 0}, 'io');
  toIdleArms(tr, 1430, 1440, O);
}

// ============================================================================================================================
// cs1: 720 t (§3.2). ready 0-6; guard up 6-10; the cut on the blade at K1 at 10 (two hands, the knees and elbows give 10-14);
// lock 10-30, pushing 24-30; the shove 30-34; slides back 34-44 (f -1.2), the feet dragging; recovers, steps forward 60-82;
// the sword lowered by 84, stands to 340; a half guard 350-370, held; the slash: the chest snaps back 650-653, staggers
// 652-664 (f -0.5), down on the right knee with the sword planted 664-694 (the head low), pushes up 694-716, the idle at 720.
function cs1(tr) {
  const rdy = readyAt(O);
  pose(tr, 0, rdy);
  const feetLock = feet(O, READY.R, READY.L);
  const lk = fit({...rdy, ...feetLock, ...lock(K.K1), two: 1, rot: [0, -6, 0], tor: [-10, 8, 0], hip: [.05, -.06, .06], head: [6, 4, 0], kL: [-.4, 0, 1]});
  tr.hold(6, ...Object.keys(lk));
  pose(tr, 10, lk, 'o');
  const give = fit({...lk, hip: [lk.hip[0], -.15, lk.hip[2] - .05], tor: [lk.tor[0] + 4, lk.tor[1], lk.tor[2]]}, {reach: .5});
  pose(tr, 14, give, 'o');
  pose(tr, 23, fit({...give, hip: [give.hip[0], -.13, give.hip[2] - .02]}, {reach: .5}), 'io');
  const push = fit({...lk, hip: [lk.hip[0] + .02, -.11, lk.hip[2] + .03], tor: [-22, 6, 0], head: [14, 2, 0]}, {reach: .56});
  pose(tr, 30, push, 'i');
  // 30-34 the shove: the blade swings up and through as she springs off
  const thr = fit({...push, ...blade([.24, 1.5, .72], [-.45, .8, .4], [0, 0, 1]), two: 1, tor: [-10, -4, 0], hip: [.02, -.09, .04], head: [4, 2, 0]});
  pose(tr, 34, thr, 'o');
  // 34-44 slides back, the feet dragging, low and braced; the left hand leaves the hilt
  const B = [0, 0, -1.2];
  const brace = {...readyAt(B, {drop: .16, yaw: -18, hand: [.42, .78, .30], dir: [.25, -.12, .95]}), tor: [-24, 6, 0], head: [16, 14, 0], aL: [20, 0, 35, 50]};
  pose(tr, 44, brace, 'o');
  pose(tr, 58, {...readyAt(B, {drop: .08, yaw: -14}), aL: ARM.balL}, 'io');
  // 60-82 two steps forward to the mark, the sword coming down to the low carry
  tr.hold(60, ...Object.keys(REST));
  tr.at(68, {root: [0, 0, -.62], hip: [0, -.04, .02], rot: [0, -8, 0]}, 'l');
  step(tr, 'L', 60, 68, [-.14, -.30]);
  tr.at(76, {root: [0, 0, -.06], hip: [0, -.03, .02], rot: [0, -2, 0]}, 'l');
  step(tr, 'R', 68, 76, [.125, 0]);
  step(tr, 'L', 76, 82, [-.125, 0], .07);
  tr.at(82, {root: O, hip: [0, 0, 0], rot: [0, 0, 0], kR: REST.kR, kL: REST.kL}, 'o');
  tr.at(74, {tor: [-3, 2, 0], head: [0, 0, 0], aL: ARM.lowL}, 'io');
  tr.at(82, {tor: [0, 0, 0]}, 'io');
  toIdleArms(tr, 60, 84, O);
  tr.at(90, {br: 1}, 'l');
  // 350-370 the sword hand tightens; the blade comes up to a half guard
  tr.mv(350, 370, {aR: [22, 0, -12, 55], sw: [-104, 10, 0], tor: [-2, -5, 0], aL: [6, 0, 9, 16]}, 'io');
  // 650-653 the slash crosses the chest: it snaps back, the sword arm is flung wide
  tr.hold(648, ...Object.keys(REST));
  tr.at(650, {tor: [-6, 0, 0], br: 0}, 'i');
  tr.at(653, {tor: [26, 10, -4], head: [22, -6, 0], aR: [-30, 0, -70, 30], sw: [-70, 30, 0], aL: [-25, 0, 60, 35], hip: [0, -.03, -.08]}, 'o');
  // 652-664 staggers back half a block, folding over the cut
  const H1 = [0, 0, -.5];
  step(tr, 'R', 652, 657, [.2, -.56], .06);
  step(tr, 'L', 657, 663, [-.17, -.34], .06);
  tr.mv(652, 664, {root: H1}, 'o');
  tr.at(664, {tor: [-22, 6, 0], head: [20, 0, 0], aR: [20, 0, -25, 40], sw: [-100, 0, 0], aL: [15, 0, 20, 45], hip: [0, -.1, -.02]}, 'io');
  // 664-694 down on the right knee, the sword planted before it (the hand goes up first, then the point comes down), the head low
  toIK(tr, 664, 2);
  const grip = add(H1, [.36, 1.42, .34]);
  tr.at(670, {hR: add(grip, [0, -.06, -.04]), bd: norm([0, -.25, .97]), bn: [1, 0, 0], pR: [.8, -.4, -.2]}, 'io');
  tr.at(676, {hR: grip, bd: norm([0, -.95, .31])}, 'i');
  const kneel = {lfR: 1, lR: [-14, 0, -6, 78], kL: [-.2, 0, 1], rot: [0, 0, 0], tor: [-16, 10, 0], head: [28, -6, 0], aL: [28, 0, 12, 70], hip: [0, 0, .06]};
  kneel.hip = [0, groundHip({...REST, root: H1, ...feet(H1, [.2, -.42], [-.17, .16]), ...kneel}), .06];
  tr.mv(664, 676, kneel, 'io');
  tr.at(684, {head: [34, -6, 0], tor: [-20, 10, 0]}, 'io');
  // 694-716 pushes up on the sword, steps back to the mark
  const up = readyAt(H1, {drop: .05, yaw: -6, hand: [.36, 1.0, .34], dir: [.05, -.45, .9]});
  for (const k of ['fR', 'fL', 'root']) delete up[k];
  tr.hold(694, ...Object.keys(REST));
  tr.at(694, {fR: [.2, 0, -.94]});
  tr.at(704, {...up, lfR: 0}, 'io');
  step(tr, 'R', 705, 711, [.125, 0], .1);
  tr.mv(705, 712, {root: [0, 0, -.12]}, 'io');
  step(tr, 'L', 711, 716, [-.125, 0], .08);
  tr.at(716, {root: O}, 'o');
  tr.mv(706, 717, {hip: [0, 0, 0], rot: [0, 0, 0], tor: [0, 0, 0], head: [0, 0, 0], aL: ARM.lowL, kR: REST.kR, kL: REST.kL}, 'io');
  toIdleArms(tr, 706, 720, O);
}

// ============================================================================================================================
// repel: 140 t (§3.4). The high guard at KR 0-4 (two hands, the knees bent); holds 4-22; heaves up 22-26; beats her blade
// aside 26-30; steps in (f +0.5) 30-36, the left hand seizes her sword wrist at KW 36 and holds it high 36-48; the hilt
// strike on her hat at KH 49 (a short hop: the crown is 2.2 b up); the rising cut 56, the level cut 62 that carries past
// her right side (f 1.8, through r -0.55) 62-68; back to her 68, the right arm hooks her sword arm over the right shoulder
// 70-76 (KS on the shoulder); bends and throws 78-96, straightens 96-102; looks down at her, the blade pointed at her 104-118;
// the right leg back 120-128, the kick at KK 129; back-flip to the mark 132-138, lands, the idle at 140. `{at:5}` shows
// ticks 0-129 only (the ending's tick 0 is the kick's pose).
function repel(tr) {
  const hiltR = add(K.KR, [.35, -.2, -.2]), gR = {...blade(hiltR, sub(K.KR, hiltR), [0, 1, .3]), ...ELBOWS_OUT};
  const st0 = stance(O, [.27, .14], [-.25, -.2], {drop: .1});
  const base = {...REST, ...st0, ...gR, two: 1, tor: [-4, 6, 0], head: [10, 0, 0], kR: [.3, 0, 1], kL: [-.4, 0, 1], look: [0, 2.2, 1.3], wl: .5};
  const g0 = fit(base);
  pose(tr, 0, g0);
  pose(tr, 4, fit({...base, hip: [g0.hip[0], -.2, g0.hip[2] - .04], tor: [0, 6, 0]}, {reach: .5}), 'o');
  pose(tr, 13, fit({...base, hip: [g0.hip[0], -.23, g0.hip[2] - .05], tor: [1, 6, 0]}, {reach: .49}), 'io');
  pose(tr, 22, fit({...base, hip: [g0.hip[0], -.19, g0.hip[2] - .03], tor: [-1, 6, 0]}, {reach: .5}), 'io');
  // 22-26 heaves up under her blade (the hands stay: the legs and the back lift)
  pose(tr, 26, fit({...base, hip: [g0.hip[0], -.1, g0.hip[2] + .01], tor: [-8, 4, 0], head: [6, 0, 0]}, {reach: .57}), 'i');
  // 26-30 beats her blade up and wide
  const wide = blade([.5, 1.55, .5], [.55, .8, .22], [1, 0, 0]);
  sweep(tr, 26, 30, gR, wide, {ease: 'o'});
  tr.at(28, {two: 0}, 'l');
  tr.at(30, {hip: [.04, -.08, .04], tor: [-4, 14, 0], aL: [30, 0, 20, 60]}, 'o');
  // 30-36 steps in, the body turned behind the reaching left arm; 36 the left hand has her sword wrist, held high to 48
  const A1 = [0, 0, .5];
  tr.mv(30, 36, {root: A1}, 'io');
  step(tr, 'L', 30, 34, [-.16, .62], .08);
  const cock = blade([.56, 1.5, .28], [.25, .9, -.35], [1, 0, 0]);
  const grab = fit({...REST, root: A1, ...feet(O, [.27, .14], [-.16, .62]), rot: [0, 20, 0], tor: [-2, 30, 0], hip: [.06, -.02, .16], head: [10, -40, 0], ...cock, hL: K.KW, wL: 1,
    pL: [-.8, -.3, -.3], kR: [.4, 0, 1], kL: [-.1, 0, 1]}, {two: false, left: K.KW, reach: .57, vars: ['hr', 'hf', 'ty', 'tr']});
  tr.hold(30, 'rot', 'head', 'hL', 'wL', 'pL', 'kR', 'kL', 'wl', 'pR');
  tr.at(31, {hL: [-.1, 1.3, .7]}, 'l');
  tr.at(36, {hip: grab.hip, tor: grab.tor, rot: grab.rot, head: grab.head, hL: K.KW, wL: 1, pL: grab.pL, kR: grab.kR, kL: grab.kL, hR: cock.hR, bd: cock.bd, bn: cock.bn, wl: 0}, 'o');
  step(tr, 'R', 33, 38, [.3, .36], .05);
  tr.at(43, {hip: add(grab.hip, [0, .015, .02])}, 'io');
  // 46-49 the hilt strike: a short hop, the pommel driven forward and down onto her hat
  const pd = norm([.6, -.6, -.53]), hand49 = sub(add(K.KH, [0, -.04, -.02]), mulv(pd, SWORD.pommel));
  const hit = fit({...REST, root: A1, ...feet(O, [.3, .36], [-.16, .62]), rot: [0, 0, 0], tor: [-4, -14, 0], hip: [0, .14, .04], ...blade(hand49, pd, [1, 0, 0])}, {reach: .58, vars: ['hr', 'ty', 'tr']});
  tr.hold(43, 'hR', 'bd', 'bn');
  tr.at(47, {hR: [.5, 1.92, .46], bd: norm([.3, .35, -.89])}, 'io');
  tr.hold(46, 'hip', 'tor', 'rot', 'head', 'lfR', 'lfL', 'lR', 'lL');
  tr.hold(48, 'wL', 'hL', 'aL');
  tr.at(49, {hip: hit.hip, tor: hit.tor, rot: hit.rot, head: [14, 0, 0], hR: hand49, bd: pd, bn: [1, 0, 0], lfR: 1, lfL: 1, lR: [8, 0, -4, 14], lL: [-6, 0, 4, 20]}, 'i');
  tr.at(49, {aL: [110, 0, 64, 30]}, 'l');
  tr.at(51, {wL: 0}, 'l');
  tr.at(55, {aL: ARM.balL}, 'io');
  // 49-52 lands, the blade dropping to the low left for the rising cut
  const lowL = blade(add(A1, [-.1, .94, .42]), [-.62, -.4, .68], [0, 1, 0]);
  tr.at(52, {hip: [0, -.1, .1], tor: [-12, -24, 0], rot: [0, 0, 0], head: [4, 20, 0], lfR: 0, lfL: 0, hR: lowL.hR, bd: lowL.bd, bn: lowL.bn}, 'o');
  // 52-56 the rising cut, lower left to upper right; 56-62 the blade comes round level; 62-68 the level cut carries past her
  const highR = blade(add(A1, [.42, 1.56, .42]), [.5, .82, .28], [0, 1, 0]);
  sweep(tr, 52, 56, lowL, highR, {ease: 'io', via: norm([-.1, .25, .96])});
  tr.at(56, {hip: [.02, -.03, .12], tor: [-4, 18, 0], head: [2, -14, 0]}, 'o');
  const lvl0 = blade(add(A1, [.4, 1.12, .0]), [.95, .02, -.3], [0, 0, 1]);
  sweep(tr, 56, 61, highR, lvl0, {ease: 'io', n: [0, 1, 0]});
  tr.at(61, {hip: [.02, -.1, .02], tor: [-8, 30, 0], head: [2, -26, 0]}, 'io');
  const A2 = [0, 0, 1.8], lvl1 = blade(add(A2, [.36, 1.1, .2]), [.6, 0, -.8], [0, 0, -1]);
  const lvlm = blade([-.2, 1.1, 1.3], [.86, 0, .5], [0, 0, 1]);
  tr.hold(61, 'root', 'fR', 'fL', 'rot');
  tr.at(64, {root: [-.5, 0, 1.0]}, 'i'); tr.at(66, {root: [-.42, 0, 1.5]}, 'l'); tr.at(68, {root: A2}, 'o');
  sweep(tr, 61, 64, lvl0, lvlm, {ease: 'l', n: [0, 1, 0]});
  sweep(tr, 64, 68, lvlm, lvl1, {ease: 'l', n: [0, 1, 0]});
  tr.hold(61, 'lfR', 'lfL', 'lR', 'lL', 'kR', 'kL');
  tr.at(62, {lfR: 1, lfL: 1, lR: [-20, 0, -4, 30], lL: [36, 0, 4, 40], hip: [0, .0, .04]}, 'l');
  tr.at(63, {hip: [0, .04, .05]}, 'l');
  tr.at(65, {lR: [44, 0, -4, 40], lL: [-30, 0, 4, 44], hip: [0, .03, .06], tor: [-10, 8, 0], head: [2, 30, 0]}, 'l');
  tr.at(67, {lR: [30, 0, -4, 24], lL: [-22, 0, 4, 30], hip: [0, .0, .02]}, 'l');
  tr.at(67, {fR: [.16, 0, 1.94], fL: [-.2, 0, 1.52]});
  tr.hold(67, 'lfR', 'lfL');
  tr.at(68, {lfR: 0, lfL: 0, hip: [0, -.07, 0], tor: [-4, -14, 0], head: [0, 40, 0], kR: [.2, 0, 1], kL: [-.3, 0, 1]}, 'o');
  step(tr, 'L', 68, 72, [-.2, 1.76], .05);
  // 68-78 back to her: the right fist goes back over the shoulder and hooks her sword arm, the knees under her
  const hook = blade([.26, 1.6, 1.74], [.7, .68, -.2], [0, 0, 1]);
  tr.at(70, {head: [0, 20, 0], tor: [8, 0, 0], hip: [0, -.1, -.06]}, 'io');
  tr.at(76, {hip: [0, -.14, -.02], tor: [10, 4, 0], head: [-6, 24, 0], hR: hook.hR, bd: hook.bd, bn: hook.bn, pR: [.9, -.2, .3]}, 'io');
  tr.mv(72, 78, {hL: [-.02, 1.2, 2.12], wL: 1, pL: [-1, -.4, .1]}, 'io');
  // 78-96 bends and throws: the hips under her, both arms pull her over and down; 96-102 straightens
  tr.hold(78, 'hip', 'tor', 'head', 'hR', 'bd', 'bn', 'rot');
  tr.at(84, {hip: [0, -.2, -.14], tor: [-48, 0, 0], head: [-14, 0, 0], hR: [.3, 1.0, 2.48], bd: norm([.8, .55, .2]), hL: [-.12, .84, 2.5]}, 'i');
  tr.at(90, {hip: [0, -.16, -.2], tor: [-78, 0, 0], head: [-10, 0, 0], hR: [.32, .6, 2.5], bd: norm([.85, -.1, .5]), hL: [-.12, .52, 2.48]}, 'l');
  tr.at(96, {hip: [0, -.1, -.12], tor: [-58, 0, 0], head: [10, 0, 0], hR: [.38, .62, 2.4], bd: norm([.7, -.28, .66]), hL: [-.24, .6, 2.36], wL: 1}, 'o');
  const over = blade(add(A2, [.32, 1.06, .34]), [-.3, -.6, .74], [0, 0, 1]);
  tr.at(102, {hip: [0, -.02, .02], tor: [-10, 0, 0], head: [16, 0, 0], hR: add(A2, [.4, .9, .2]), bd: norm([.2, -.5, .84]), wL: 0, aL: ARM.balL, pR: REST.pR}, 'io');
  // 104-118 stands over her, the point at her
  tr.mv(104, 112, {hR: over.hR, bd: over.bd, bn: over.bn, tor: [-14, 6, 0], head: [26, -4, 0], hip: [0, -.03, .04]}, 'io');
  // 120-128 the right leg goes back; 129 the kick lands on her flank
  tr.hold(120, 'hip', 'tor', 'head', 'fR', 'hR', 'bd', 'aL', 'kR');
  tr.at(126, {fR: [.2, .3, 1.36], kR: [.3, 0, 1], hip: [-.05, -.03, .04], tor: [-6, 10, 0], head: [22, -8, 0], hR: add(A2, [.5, 1.0, .0]), bd: norm([.5, -.2, .84]), aL: [30, 0, 30, 40]}, 'io', {fR: [0, .1, 0]});
  tr.at(129, {fR: add(K.KK, [0, 0, 0]), kR: [.2, .3, 1], hip: [-.04, -.07, .3], tor: [6, -8, 0], head: [24, 4, 0], hR: add(A2, [.56, 1.0, -.1]), bd: norm([.7, .2, .7]), aL: [-30, 0, 34, 30]}, 'i');
  // 129-132 the leg comes back under; 132-137 the back-flip to the mark; lands, rises into the idle
  tr.at(132, {fR: [.14, 0, 1.86], kR: REST.kR, hip: [0, -.2, -.06], tor: [-20, 0, 0], head: [10, 0, 0], hR: add(A2, [.44, .8, .1]), bd: norm([.3, -.2, .93]), aL: [10, 0, 20, 40]}, 'io', {fR: [0, .12, 0]});
  toFK(tr, 130, [6, 0, -80, 12], [180, 0, 0]);
  tr.hold(132, 'root', 'rot', 'lfR', 'lfL', 'lR', 'lL', 'fL', 'kL');
  tr.at(133, {lfR: 1, lfL: 1, lR: [40, 0, -4, 70], lL: [40, 0, 4, 70], hip: [0, .2, -.06], tor: [-10, 0, 0], aL: [20, 0, 24, 60]}, 'l');
  tr.at(135.5, {hip: [0, .8, 0]}, 'o');
  tr.at(135, {lR: [80, 0, -6, 108], lL: [80, 0, 6, 108], tor: [-26, 0, 0], head: [-6, 0, 0]}, 'l');
  tr.at(138, {root: O, rot: [360, 0, 0], hip: [0, -.09, -.08], lR: [50, 0, -4, 78], lL: [50, 0, 4, 78], tor: [-22, 0, 0], head: [8, 0, 0]}, 'l');
  tr.at(138, {fR: [.125, 0, 0], fL: [-.125, 0, 0], kL: REST.kL});
  tr.hold(138, 'lfR', 'lfL', 'aR', 'sw', 'aL');
  tr.at(139, {lfR: 0, lfL: 0, hip: [0, -.12, -.16], tor: [-12, 0, 0], aR: [10, 0, -44, 20], sw: [-150, 0, 0], aL: [8, 0, 12, 20]}, 'l');
  tr.at(140, {hip: [0, 0, 0], tor: [0, 0, 0], head: [0, 0, 0], aL: ARM.lowL, aR: ARM.lowR, sw: SW_LOW}, 'o');
}

// ============================================================================================================================
// ending: 1372 t (§3.5). Tick 0 = the repel's kick (f 1.8). Steps back to f 0.8 4-16, ready; lunges (f 1.3) 50-54, the cut's
// point grazes her brim at KG 52; lock at KE2 56-80 (two hands), pushing 76-80; shoved back to -0.6 80-90, skids to -1.5 by
// 104; crouches 104-116; the dash-cut to +1.0 118-124 finds only air, the follow-through held; runs to 2.5 150-188; the
// clash at KE5 190, lock to 204; springs up 204-216; in the air: the passing cut at KA1 228, a turn, the level guard over the
// head at KA2 262 (two hands), the big cut at KA3 286, the lock at KA4 298-304; pushed off, falls 304-330, lands in a crouch
// at the mark, rises; (turned to ST2 by `face` 338-350;) the sword lowered 380-400; the left hand half raised 566-584,
// lowered 590-606; a nod 860; stands to 1372 (= the coda's tick 0).
function ending(tr) {
  const A2 = [0, 0, 1.8], E1 = [0, 0, .8];
  // 0-16 the leg comes back, two steps back to f 0.8, the ready stance by 20
  const r1 = readyAt(E1);
  tr.at(4, {fR: [.16, 0, 1.9], kR: REST.kR, hip: [0, -.06, 0], tor: [-6, 0, 0], head: [8, 0, 0]}, 'io', {fR: [0, .08, 0]});
  tr.mv(4, 16, {root: E1}, 'io');
  step(tr, 'L', 4, 8, [-.18, 1.2], .07);
  step(tr, 'R', 8, 12, [r1.fR[0], r1.fR[2]], .07);
  step(tr, 'L', 12, 16, [r1.fL[0], r1.fL[2]], .07);
  tr.mv(4, 20, {hip: r1.hip, rot: r1.rot, tor: r1.tor, head: r1.head, hR: r1.hR, bd: r1.bd, bn: r1.bn, pR: r1.pR, aL: r1.aL, kR: r1.kR, kL: r1.kL, look: [0, 1.6, 4.6], wl: .5}, 'io');
  // 46-50 the sword goes back over the right shoulder; 50-54 the lunge, the cut's point on her brim at 52, down into the lock
  const E2 = [0, 0, 1.3], dG = norm([-.75, .75, 1.1]), hG = sub(K.KG, mulv(dG, SWORD.tip));
  const cock = blade(add(E1, [.5, 1.46, -.06]), [.55, .7, -.45], [0, 1, 0]);
  tr.mv(44, 50, {hR: cock.hR, bd: cock.bd, bn: cock.bn, tor: [-4, 16, 0], hip: add(r1.hip, [0, -.03, -.04])}, 'io');
  const lkE = lock(K.KE2);
  sweep(tr, 50, 52, cock, {hR: hG, bd: dG}, {ease: 'i', via: norm([.8, .5, .34])});
  const midE = {hR: [.56, 1.3, 1.74], bd: norm([-.68, .62, .4])};
  sweep(tr, 52, 54, {hR: hG, bd: dG}, midE, {ease: 'l'});
  sweep(tr, 54, 56, midE, lkE, {ease: 'l'});
  tr.mv(50, 54, {root: E2}, 'io');
  step(tr, 'R', 50, 54, [.24, 1.3 + .34], .06);
  const l2 = fit({...r1, root: E2, ...feet(E2, [.24, .34], [-.2, -.5 - .0]), ...lkE, two: 1, rot: [0, -6, 0], tor: [-12, 8, 0], hip: [.05, -.1, .0], head: [6, 4, 0], wl: 0});
  tr.hold(50, 'hip', 'rot', 'tor', 'head', 'two', 'wl', 'aL', 'pL', 'pR');
  tr.at(52, {hip: [.04, -.1, .04], tor: [-8, -6, 0]}, 'i');
  tr.hold(53, 'two');
  tr.at(56, {hip: l2.hip, rot: l2.rot, tor: l2.tor, head: l2.head, two: 1, wl: 0, pL: ELBOWS_OUT.pL, pR: ELBOWS_OUT.pR}, 'o');
  tr.mv(50, 56, {fL: [-.2, 0, 1.3 - .3]}, 'io');
  // 56-80 lock; the burst at 70 jolts both; 76-80 pushing
  tr.at(69, {hip: add(l2.hip, [0, -.03, -.02])}, 'io');
  tr.at(71, {hip: add(l2.hip, [0, -.07, -.06]), tor: add(l2.tor, [5, 0, 0])}, 'o');
  const p2 = fit({...l2, ...feet(E2, [.24, .34], [-.2, -.3]), hip: add(l2.hip, [0, -.02, .03]), tor: [-20, 6, 0]}, {reach: .56});
  tr.at(80, {hip: p2.hip, tor: p2.tor, head: [12, 2, 0]}, 'io');
  // 80-90 shoved back, sliding to f -0.6; 94-104 skids on to -1.5, low; 104-116 gathers in a crouch, the sword drawn back
  const E3 = [0, 0, -.6], E4 = [0, 0, -1.5];
  const sk = {...readyAt(E3, {drop: .12, yaw: -16, hand: [.4, .95, .28], dir: [.1, .5, .86]}), tor: [-14, 6, 0], head: [10, 12, 0], aL: [10, 0, 40, 40], two: 0};
  tr.hold(80, ...Object.keys(REST));
  tr.at(83, {two: 0}, 'l');
  pose(tr, 90, sk, 'o');
  const sk2 = {...readyAt(E4, {drop: .2, yaw: -20, hand: [.46, .7, .1], dir: [.5, -.1, .86]}), tor: [-26, 8, 0], head: [20, 14, 0], aL: [30, 0, 30, 60]};
  tr.hold(94, ...Object.keys(REST));
  pose(tr, 104, sk2, 'o');
  const back = blade(add(E4, [.5, .74, -.16]), [.45, .1, -.89], [0, 1, 0]);
  tr.at(114, {hip: add(sk2.hip, [0, -.06, -.04]), tor: [-34, 26, 0], head: [26, -10, 0], hR: back.hR, bd: back.bd, bn: back.bn, aL: [40, 0, 20, 70]}, 'io');
  // 118-124 the dash-cut: 2.5 b in 6 ticks, the blade sweeping level from behind the right hip across the front
  const E5 = [0, 0, 1.0];
  tr.hold(118, ...Object.keys(REST));
  tr.at(124, {root: E5}, 'io');
  const cutA = {hR: add(E4, [.5, .74, -.16]), bd: back.bd}, cutB = blade(add(E5, [-.3, 1.0, .5]), [-.9, .1, .42], [0, 1, 0]);
  sweep(tr, 118, 124, cutA, cutB, {ease: 'io', via: norm([.6, .05, .8]), n: [0, 1, 0], hvia: [.5, .98, .1]});
  tr.at(119, {lfR: 1, lfL: 1, lR: [60, 0, -6, 60], lL: [-40, 0, 6, 50], hip: [0, -.16, .04]}, 'l');
  tr.at(121, {hip: [0, -.13, .1], tor: [-30, -10, 0], head: [22, 6, 0], lR: [62, 0, -6, 62], lL: [-48, 0, 6, 22], aL: [-30, 0, 40, 30]}, 'l');
  const land5 = stance(E5, [.22, .42], [-.2, -.5], {drop: .22, yaw: 0});
  tr.at(123, {fR: land5.fR, fL: land5.fL, kR: [.2, 0, 1], kL: [-.5, 0, .8]});
  tr.hold(123, 'lfR', 'lfL');
  tr.at(124, {lfR: 0, lfL: 0, hip: [.0, -.19, .1], tor: [-26, -38, 0], head: [14, 30, 0], rot: [0, 0, 0], aL: [-40, 0, 50, 20]}, 'o');
  // 124-146 holds the follow-through, then comes up into the ready stance
  const r5 = readyAt(E5);
  tr.hold(132, ...Object.keys(REST));
  pose(tr, 146, {...r5, wl: .5, look: [0, 1.6, 11]}, 'io');
  // 150-188 runs in: gathers low 150-164, three driving steps 164-188
  const E6 = [0, 0, 2.5];
  tr.mv(150, 164, {hip: add(r5.hip, [0, -.08, .02]), tor: [-18, 6, 0], head: [14, 8, 0], hR: add(E5, [.44, .82, .1]), bd: norm([.3, -.3, .9]), aL: [30, 0, 20, 60]}, 'io');
  tr.hold(164, 'root');
  tr.hold(164, 'hR');
  tr.at(172, {root: [0, 0, 1.45], hR: [.44, .82, 1.55]}, 'i'); tr.at(180, {root: [0, 0, 2.02], hR: [.46, .9, 2.1]}, 'l'); tr.at(188, {root: E6}, 'o');
  step(tr, 'L', 164, 172, [-.14, 1.75], .12);
  step(tr, 'R', 172, 180, [.14, 2.36], .12);
  step(tr, 'L', 180, 187, [-.2, 2.5 - .46], .1);
  step(tr, 'R', 184, 189, [.24, 2.5 + .34], .06);
  for (const [t, y, ax] of [[168, 8, -20], [172, -4, 30], [176, -8, 34], [180, 4, -20], [184, 8, -24], [188, -2, 10]]) tr.at(t, {tor: [-20, y, 0], aL: [ax, 0, 22, 55], hip: [0, -.14 - (t % 8 ? 0 : .03), .04]}, 'l');
  // 188-190 the cut comes down into the clash at KE5 (two hands), lock to 204
  const lk5 = lock(K.KE5), up5 = blade(add(E6, [.56, 1.6, -.1]), [.3, .85, -.42], [1, 0, 0]);
  tr.mv(180, 186, {bd: up5.bd, bn: up5.bn}, 'io');
  tr.at(186, {hR: up5.hR}, 'io');
  const mid5 = blade(add(E6, [.52, 1.62, .38]), [-.1, .95, .3], [1, 0, 0]);
  sweep(tr, 186, 188, up5, mid5, {ease: 'i'});
  sweep(tr, 188, 190, mid5, lk5, {ease: 'l'});
  const l5 = fit({...r5, root: E6, ...feet(E6, [.24, .34], [-.2, -.46]), ...lk5, two: 1, rot: [0, -6, 0], tor: [-12, 8, 0], hip: [.05, -.1, .02], head: [6, 4, 0], wl: 0});
  tr.hold(187, 'two', 'rot', 'head', 'wl', 'pL', 'pR');
  tr.at(190, {hip: l5.hip, rot: l5.rot, tor: l5.tor, head: l5.head, two: 1, wl: 0, aL: ARM.balL, pL: ELBOWS_OUT.pL, pR: ELBOWS_OUT.pR}, 'i');
  tr.at(197, {hip: add(l5.hip, [0, -.06, -.03])}, 'io');
  tr.at(204, {hip: add(l5.hip, [0, -.12, -.02])}, 'io');
  // 204-216 springs up to (0, 6.0, 1.5); the legs trail, the sword ready at the right
  const air = (root, rest = {}) => ({root, lfR: 1, lfL: 1, hip: [0, 0, 0], ...rest});
  tr.hold(204, ...Object.keys(REST));
  tr.at(206, {two: 0, lfR: 1, lfL: 1, lR: [4, 0, -4, 10], lL: [-10, 0, 4, 24], hip: [0, .0, 0]}, 'l');
  const U0 = [0, 6.0, 1.5];
  const fly = blade(add(U0, [.46, 1.2, .2]), [.4, .6, -.7], [1, 0, 0]);
  tr.at(216, {...air(U0), rot: [0, 0, 0], tor: [-6, 14, 0], head: [-6, -10, 0], lR: [38, 0, -8, 70], lL: [-8, 0, 6, 40], aL: [-20, 0, 40, 40], look: [0, 7.6, 3.6], wl: .7}, 'o');
  carry(tr, 204, 216, sub(lk5.hR, E6), [.46, 1.2, .2], 'io');
  tr.at(210, {bd: norm([.3, .9, .3])}, 'l'); tr.at(216, {bd: fly.bd, bn: fly.bn}, 'l');
  // 216-228 the passing cut meets hers at KA1: level, right to left
  const U1 = [.1, 5.86, 1.62];
  const c1a = blade(add(U1, [.5, 1.12, .0]), [.86, .1, -.5], [0, 0, 1]), c1b = blade(add(U1, [.36, 1.04, .36]), sub(K.KA1, add(U1, [.36, 1.04, .36])), [0, 0, 1]);
  const c1c = blade(add(U1, [-.2, 1.0, .46]), [-.92, -.1, .38], [0, 0, 1]);
  tr.at(222, {root: [.06, 6.0, 1.5], hR: c1a.hR, bd: c1a.bd, bn: [0, 1, 0], tor: [-4, 34, 0], head: [-4, -30, 0], lR: [30, 0, -8, 50], lL: [-14, 0, 6, 50]}, 'io');
  tr.at(228, {root: U1}, 'io');
  sweep(tr, 224, 228, c1a, c1b, {ease: 'i', n: [0, 1, 0]});
  sweep(tr, 228, 232, c1b, c1c, {ease: 'o', n: [0, 1, 0]});
  tr.at(228, {tor: [-8, 4, 0], head: [-2, 0, 0], aL: [-34, 0, 44, 30]}, 'i');
  tr.at(232, {tor: [-10, -30, 0], head: [0, 26, 0], lR: [10, 0, -8, 40], lL: [26, 0, 6, 60]}, 'o');
  // 232-252 drifts back and up from the pass, the sword carried round over the right shoulder; 252-260 into the level guard
  const U2 = [-.5, 5.51, 2.17];
  tr.hold(232, 'root');
  tr.at(242, {root: [.12, 6.1, 1.36]}, 'o'); tr.at(252, {root: [-.2, 5.9, 1.8]}, 'io');
  tr.at(236, {hR: [.3, 7.0, 1.86], bd: norm([-.3, .7, .65]), tor: [-6, -10, 0], head: [0, 6, 0], aL: [10, 0, 30, 60]}, 'io');
  tr.at(243, {hR: [.6, 7.5, 1.3], bd: norm([.3, .9, -.3]), bn: [1, 0, 0], tor: [4, 16, 0], head: [-8, -12, 0], lR: [14, 0, -8, 40], lL: [30, 0, 6, 64]}, 'io');
  tr.at(252, {hR: [.26, 7.46, 2.1], bd: norm([.8, .58, .1]), tor: [2, -6, 0], lR: [20, 0, -8, 60], lL: [4, 0, 6, 50]}, 'io');
  const hA2 = add(K.KA2, [-.45, 0, -.05]), gA2 = blade(hA2, [1, 0, .08], [0, 1, 0]);
  const b262 = fit({...REST, ...air(U2), rot: [0, 0, 0], tor: [5, -22, 0], head: [-16, 16, 0], ...gA2, ...ELBOWS_OUT, two: 1, lR: [40, 0, -8, 76], lL: [14, 0, 6, 64]}, {reach: .57, vars: ['hr', 'hf', 'ty', 'tr', 'tp']});
  tr.at(256, {two: 0}, 'l');
  tr.hold(256, 'pL', 'pR');
  tr.at(260, {root: U2, hR: gA2.hR, bd: gA2.bd, bn: gA2.bn, pL: ELBOWS_OUT.pL, pR: ELBOWS_OUT.pR, hip: b262.hip, tor: b262.tor, head: b262.head, two: 1, lR: b262.lR, lL: b262.lL, wl: 0}, 'io');
  // 262 her cut falls on the guard: the arms give, the body drops; 266-286 swings out and round into the big cut at KA3
  tr.hold(262, 'root', 'hR', 'hip', 'tor', 'bd', 'bn', 'head', 'lR', 'lL');
  tr.at(265, {root: add(U2, [0, -.3, -.12]), hip: add(b262.hip, [0, -.06, 0]), hR: add(gA2.hR, [0, -.34, -.14]), tor: add(b262.tor, [8, 0, 0])}, 'o');
  const U3 = [0, 5.6, 1.6];
  const hi3 = blade(add(U3, [.5, 1.7, -.1]), [.3, .8, -.5], [1, 0, 0]);
  const h3 = add(U3, [.3, 1.34, .44]), d3 = norm(sub(K.KA3, h3)), c3 = blade(h3, d3, [1, 0, 0]);
  const lo3 = blade(add(U3, [-.1, .9, .5]), [-.5, -.6, .62], [1, 0, 0]);
  tr.hold(265, 'two'); tr.at(268, {two: 0}, 'l');
  tr.at(278, {root: [.1, 6.0, 1.3], hip: [0, 0, 0], hR: hi3.hR, bd: hi3.bd, bn: hi3.bn, tor: [8, 24, 0], head: [-10, -20, 0], lR: [10, 0, -8, 30], lL: [-20, 0, 6, 50], aL: [-10, 0, 50, 40]}, 'io');
  tr.at(286, {root: U3}, 'i');
  sweep(tr, 282, 286, hi3, c3, {ease: 'i'});
  sweep(tr, 286, 289, c3, lo3, {ease: 'o'});
  tr.at(286, {tor: [-12, -4, 0], head: [-2, 0, 0], lR: [44, 0, -8, 70], lL: [-6, 0, 6, 40]}, 'i');
  tr.at(289, {root: add(U3, [0, -.12, -.1]), tor: [-20, -20, 0]}, 'o');
  // 290-298 into the lock at KA4 (two hands), pressing to 304
  const U4 = [.0, 5.45, 1.85], lk4 = lock(K.KA4);
  const b4 = fit({...REST, ...air(U4), rot: [0, 0, 0], tor: [-10, 8, 0], head: [4, 4, 0], ...lk4, two: 1, hip: [.2, 0, .0], lR: [36, 0, -8, 70], lL: [-16, 0, 6, 44]});
  tr.mv(291, 298, {root: U4, hR: lk4.hR, bd: lk4.bd, bn: lk4.bn, pL: ELBOWS_OUT.pL, pR: ELBOWS_OUT.pR, hip: b4.hip, tor: b4.tor, head: b4.head, two: 1, lR: b4.lR, lL: b4.lL}, 'io');
  tr.at(304, {hip: add(b4.hip, [0, 0, .05]), tor: add(b4.tor, [-6, 0, 0])}, 'io');
  // 304-330 pushed off: falls back to the mark, lands in a crouch, rises by 338
  tr.hold(304, ...Object.keys(REST));
  tr.at(306, {two: 0}, 'l');
  tr.at(312, {root: [0, 5.2, 1.2], hip: [0, 0, 0], tor: [16, 0, 0], head: [-8, 0, 0], lR: [64, 0, -8, 70], lL: [24, 0, 6, 60], aL: [-30, 0, 60, 20], bd: norm([.5, .6, .62])}, 'o');
  tr.at(330, {root: O}, 'i');
  carry(tr, 304, 312, sub(lk4.hR, U4), [.5, 1.3, .3], 'o');
  carry(tr, 312, 330, [.5, 1.3, .3], [.46, .9, .3], 'io');
  tr.at(326, {tor: [-10, 0, 0], head: [6, 0, 0], lR: [30, 0, -6, 50], lL: [22, 0, 6, 44], aL: [10, 0, 40, 40]}, 'io');
  const ld = stance(O, [.2, .16], [-.2, -.14], {drop: .26});
  tr.at(329, {fR: ld.fR, fL: ld.fL, kR: [.25, 0, 1], kL: [-.3, 0, 1], rot: [0, 0, 0]});
  tr.hold(329, 'lfR', 'lfL');
  tr.at(330, {lfR: 0, lfL: 0, hip: [0, -.12, 0], lR: [20, 0, -6, 30], lL: [16, 0, 6, 30], bd: norm([.3, -.1, .95])}, 'l');
  tr.at(333, {hip: ld.hip, tor: [-24, 0, 0], head: [14, 0, 0], aL: [20, 0, 30, 60]}, 'o');
  const r9 = readyAt(O, {drop: .04, yaw: -6, hand: [.3, .95, .34], dir: [.0, .2, .98]});
  tr.at(342, {hip: r9.hip, rot: [0, -6, 0], tor: [-3, 3, 0], head: [0, 6, 0], aL: ARM.balL, hR: r9.hR, bd: r9.bd, bn: r9.bn}, 'io');
  step(tr, 'R', 338, 343, [r9.fR[0], r9.fR[2]], .04); step(tr, 'L', 343, 348, [r9.fL[0], r9.fL[2]], .04);
  // 380-400 the sword comes down, the feet together: stands as the avatar stands
  step(tr, 'L', 380, 386, [-.125, 0], .05); step(tr, 'R', 386, 392, [.125, 0], .05);
  tr.mv(380, 396, {hip: [0, 0, 0], rot: [0, 0, 0], tor: [0, 0, 0], head: [0, 0, 0], aL: ARM.lowL, kR: REST.kR, kL: REST.kL}, 'io');
  toIdleArms(tr, 380, 400, O);
  tr.mv(400, 410, {br: 1}, 'l');
  // 566-606 the left hand comes half way up, and down again; 856-864 a nod
  tr.mv(566, 584, {aL: [34, 0, 10, 72], head: [-2, 0, 0]}, 'io');
  tr.mv(590, 606, {aL: ARM.lowL, head: [0, 0, 0]}, 'io');
  tr.mv(856, 860, {head: [-9, 0, 0]}, 'io'); tr.at(865, {head: [0, 0, 0]}, 'io');
  tr.mv(1340, 1372, {br: 0}, 'l');
}

// coda: 120 t. The idle; the right forearm lifts a little as the gift arrives 44-56, back by 70.
function coda(tr) {
  tr.at(16, {br: 1}, 'l');
  tr.mv(44, 56, {aR: [12, 0, -9, 36], sw: [-116, 0, 0]}, 'io');
  tr.at(70, {aR: ARM.lowR, sw: SW_LOW}, 'io');
  tr.mv(100, 120, {br: 0}, 'l');
}

// the ending starts in the repel's kick
const repelTracks = new Tracks(140, IDLE_CHANNELS); repel(repelTracks);
const KICK = repelTracks.sample(129);
const mk = (id, len, build, extra = {}) => ({id, len, build, handback: [len], ...extra});
export const CLIPS = [
  mk('cs0', 1440, cs0, {grip: 'right hand, the point down until 1262', sync: [1290], slow: ['root 20-100'], steps: [...CS0_PLANTS, 102, 1255, 1259, 1395, 1400, 1434, 1438],
    beats: 'stands at f -6.0 0-20; walks in 20-100 (16-t cycle, 0.075 b/t); stops 100-110; idle; head up toward her 670-690, weight forward 690-700; idle; head follows her leap 1236-1258, half step back 1250-1259 (f -0.3); middle guard 1262-1284; steps forward to 0 1390-1400; idle 1430-1440',
    her: [[0, [0, 0, 20.73]], [1052, [0, 0, 20.7]], [1148, [0, 0, 13.5]], [1234, [0, 0, 13.5]], [1246, [0, 4.5, 10]], [1258, [0, 0, 6.5]]]}),
  mk('cs1', 720, cs1, {grip: 'right hand; two hands 6-34', two: [[10, 30]], slides: [[30, 44], [664, 676], [694, 704]], sync: [566], steps: [68, 76, 82, 657, 663, 671, 711, 716],
    beats: 'ready 0-6; guard up 6-10; the cut on the blade at K1 at 10; lock 10-30, pushing 24-30; the shove 30-34; slides back 34-44; recovers, steps forward 60-82; sword lowered by 84; half guard 350-370, held; hit 650-653; stagger 652-664 (f -0.5); on the right knee, the sword planted 664-694; up 694-716; idle 720',
    her: [[0, [0, 0, 9]], [6, [0, 0, 9]], [10, [0, 0, 1.5]], [34, [0, 0, 1.5]], [50, [0, 0, 9]]]}),
  mk('repel', 140, repel, {keep: [129], grip: 'two hands 0-30; left hand free 30-140 (on her wrist 36-48, on her arm 78-96)', two: [[0, 26]], slides: [[61, 68], [129, 139]], steps: [34, 38, 52, 68, 72, 132, 138],
    beats: 'high guard at KR 0-4; holds 4-22; heaves 22-26; beats her blade aside 26-30; steps in 30-36; left hand on her wrist at KW 36-48; hilt strike at KH 49; rising cut 56; level cut 62, past her right side 62-68 (r -0.5); back to her 68; hooks her arm over the right shoulder 70-76; throws 78-96; straightens 96-102; the point at her 104-118; leg back 120-128; kick at KK 129; back-flip 132-138; idle 140',
    her: [[0, [0, 1, 1.0]], [6, [0, 0, 1.3]], [52, [0, 0, 1.1]], [68, [0, 0, 1.2]], [78, [0, 0, 1.2]], [88, [0, 1.9, 1.9]], [101, [0, 0, 3.0]], [129, [0, 0, 3.0]], [135, [0, 0, 8]], [140, [0, 0, 9]]]}),
  mk('ending', 1372, ending, {start: KICK, after: ['repel', 129], grounded: [[330, 1372]],
    grip: 'right hand; two hands 56-80, 190-204, 260-266, 298-304; left hand free 556-616', two: [[56, 80], [190, 204], [262, 262], [298, 304]],
    slides: [[50, 56], [80, 104], [117, 124]], steps: [8, 12, 16, 54, 123, 172, 180, 187, 189, 330, 343, 348, 386, 392],
    beats: 'the kick\'s pose 0; steps back to f 0.8 4-16, ready; lunge 50-54, the point on her brim at KG 52; lock at KE2 56-80; shoved back 80-90, skids to -1.5 by 104; crouch 104-116; dash-cut to +1.0 118-124; follow-through; runs to 2.5 164-188; clash at KE5 190, lock to 204; springs up 204-216; KA1 228; a turn 232-252; level guard at KA2 262; KA3 286; lock at KA4 298-304; falls 304-330, lands, rises; sword lowered 380-400; left hand half raised 566-584, lowered 590-606; nod 860; stands to 1372',
    her: [[0, [0, 0, 4.2]], [22, [0, 0, 4.6]], [50, [0, 0, 4.6]], [54, [0, 0, 2.9]], [80, [0, 0, 2.9]], [86, [0, 0, 6]], [116, [0, 0, 6]], [136, [0, 0, 11]], [150, [0, 0, 11]], [188, [0, 0, 4.0]], [204, [0, 0, 4.0]], [216, [0, 6, 3.6]], [304, [0, 6, 3.6]], [334, [0, 0, 9]]]}),
  mk('coda', 120, coda, {grip: 'right hand, sword low', beats: 'idle; the right forearm lifts a little 44-56, back by 70', her: [[0, [0, 0, 4.5]]]}),
];
