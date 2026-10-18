// Motion clips of the experimental field generator (실험성 역장 발생 장치) rig, authored from the footage: the pattern
// timelines of scratchpad mb3/plan.md (Rotation), the frame-accurate reports mb3/understand/v1..v4.md and model.md §5
// (spinners, hover, the core flip-up, the transitions) and §8 (the rest poses of the seven forms). Format and
// sampling: mboss_rig_clips.mjs; channels: fieldgen_pose.mjs.
//
// Authoring. A clip is written as sparse keys (eased segments), then baked to one key per tick: overlays add the
// cyclic motion (bob, wobble, the arch rocking, link-beam pulses) or set exact formulas (the laser orbit, the drill
// orbit, the stack following the rise), and the pendulum swing is simulated (a damped pendulum, period about 40 t,
// driven by the hang point's acceleration from the clip's own heights and tilts plus the module's travel where the
// clip knows it). The compiler only sees integer ticks, so baking costs nothing in the output.
//
// Rules every clip keeps (checked by build_mboss_fieldgen_rig.mjs):
//   * no horizontal root travel: pos x / z stay 0 (the module moves the body; the clips carry heights, tilts and
//     rolls, the stack spacing and every part's own motion) and no root yaw (the module turns the anchor);
//   * spinners (halo, inner ring, brim, medallions, drill pods, tower tiers, the arch gyroscope, the plates) turn at
//     the rate channels w*; per clip each spinner's integrated angle is scaled to a whole number of its symmetry
//     steps (SYM below: halo 45, inner ring 22.5, drill pods 90, gear medallion 180, tower tiers 22.5 / 90, the rest
//     360), so every clip ends each spinner on a pose that looks exactly like its rest angle. A clip that loops or
//     chains (next) also snaps those parts at its last tick by the symmetry multiple (snapPose: an instant,
//     invisible step), so the next clip's first key continues the spin without unwinding it;
//   * the pendulum hangs plumb (pdSw is a world-frame swing) and every low point (pendulum tip, drill tips, the
//     ring's low rim, the core, the spike tips, the halo) stays over the floor while visible.
import {accumulate as accumulateClip, sampleClip as sampleAt} from './mboss_rig_clips.mjs';
import {add as vadd, rot, q} from './mboss_rig_math.mjs';
import {DEFAULT_POSE, FORMS, CRUISE, FIELD, DORMANT, COREUP, TOWER, LASER, DEPLOYED, RATES, DOCK, spikes, medals, FACE_FRONT} from './fieldgen_pose.mjs';

export const DISCRETE = ['colDir', 'lk', 'glowLook', 'beamLook', 'colLook'];
const k = (t, pose = {}, e = 'io', from = null) => [t, pose, e, from];
const STILL = Object.fromEntries(Object.keys(RATES).map(n => [n, 0]));
const scaled = f => Object.fromEntries(Object.entries(RATES).map(([n, v]) => [n, v * f]));
const TAU = 2 * Math.PI;
const sm = u => { const x = Math.max(0, Math.min(1, u)); return x * x * (3 - 2 * x); };
const lerp = (a, b, u) => a + (b - a) * u;

// ---- overlays: (t, p) => mutate the sampled pose of tick t ---------------------------------------------------------
const bump = (p, ch, i, v) => { if (typeof p[ch] === 'number') p[ch] += v; else { p[ch] = p[ch].slice(); p[ch][i] += v; } };
// envelope: 1 inside [a, b], smooth ramps of r ticks at both ends, 0 outside
const win = (t, a, b, r) => (t <= a || t >= b ? 0 : Math.min(1, sm((t - a) / r), sm((b - t) / r)));
// a sine on one channel (index i of a vector channel), optionally inside [a, b]
// (t0: the tick where the sine is 0, so a clip can end exactly where a loop starts)
const osc = (ch, i, amp, period, {phase = 0, a = null, b = null, r = 8, t0 = 0} = {}) => (t, p) => {
  const e = a === null ? 1 : win(t, a, b, r);
  if (e) bump(p, ch, i, amp * e * Math.sin(TAU * (t - t0) / period + phase));
};
// a damped kick: amplitude amp at t0, then cosine ringing (period, decay ticks), for jolts and wobbles
const ring = (ch, i, amp, t0, period, decay) => (t, p) => {
  if (t < t0) return;
  const u = t - t0;
  bump(p, ch, i, amp * Math.exp(-u / decay) * Math.sin(TAU * u / period) * sm(u / 1.5));
};
// the plate pair follows the pendulum hang point (cruise spacing) once the pendulum has dropped past the plate
const stackFollow = (lo, hi) => (t, p) => { p.plY = Math.max(lo, Math.min(hi, p.pdY + .28)); p.pl2Y = p.plY + .12; };

// ---- the pendulum: a damped pendulum per axis (pdSw = [pitch: tip toward -z, roll: tip toward +x]) -----------------
// Driven by the acceleration of the hang point (rig frame, from the clip's heights and tilts) and by the module's
// travel where a clip declares it (drive: [[t0, t1, ax, az]] in blocks per tick^2, device frame: +x left, -z
// forward; a visual drive, much gentler than the module's real glide). A stiff, damped pendulum: period about 26 t
// (l 1.0 b, g 0.06 b/t^2), damping 0.09 per tick. Loops are simulated three times and the last pass kept, so they close.
// The forcing is halved (pendGain: a semi-rigid mechanism, not a free bob) and the simulated swing is soft-limited to
// about 28 degrees (tanh), so big root tilts (the pack-up roll, the break) read as a lively sway, not a flail.
const PEND_G = .06, PEND_L = 1.0, PEND_C = .09, PEND_GAIN = .5, PEND_MAX = 28;
function hangPoint(p) { return vadd(p.pos, rot(q(p.rot), [0, p.pdY, 0])); }
function simulatePendulum(c, poses) {
  const n = poses.length, H = poses.map(hangPoint);
  const acc = H.map((h, t) => (t === 0 || t === n - 1 ? [0, 0, 0] : [0, 1, 2].map(i => H[t + 1][i] - 2 * h[i] + H[t - 1][i])));
  for (const [t0, t1, ax, az] of c.drive || []) for (let t = t0; t < Math.min(t1, n); t++) { acc[t][0] += ax; acc[t][2] += az; }
  let th = [0, 0], om = [0, 0];
  const out = [];
  for (let pass = 0; pass < (c.loop ? 3 : 1); pass++) {
    out.length = 0;
    for (let t = 0; t < n; t++) {
      out.push(th.slice());
      const gain = c.pendGain ?? PEND_GAIN, [ax, ay, az] = acc[t].map(x => x * gain), g = PEND_G + ay;
      for (let s = 0; s < 4; s++) {
        const a0 = -g / PEND_L * Math.sin(th[0]) + az / PEND_L * Math.cos(th[0]) - PEND_C * om[0];
        const a1 = -g / PEND_L * Math.sin(th[1]) - ax / PEND_L * Math.cos(th[1]) - PEND_C * om[1];
        om = [om[0] + a0 / 4, om[1] + a1 / 4];
        th = [th[0] + om[0] / 4, th[1] + om[1] / 4];
      }
    }
  }
  const deg = x => PEND_MAX * Math.tanh(x * 180 / Math.PI / PEND_MAX);
  poses.forEach((p, t) => { p.pdSw = [p.pdSw[0] + deg(out[t][0]), p.pdSw[1] + deg(out[t][1])]; });
}

// ---- bake: per-channel tracks + overlays + pendulum -> one key per tick --------------------------------------------
// A key k(t, pose, ease, from) is a keyframe only of the channels it names: each channel interpolates between its own
// keyframes (ease = that of the arriving keyframe; discrete channels switch at the keyframe), and a channel no key
// names holds. `from` makes the named channels hold their value until that tick (the move runs from..t).
const EASES = {io: u => u * u * (3 - 2 * u), i: u => u * u, o: u => 1 - (1 - u) * (1 - u), l: u => u};
const mix = (a, b, u) => (typeof a === 'number' ? a + (b - a) * u : a.map((x, i) => x + (b[i] - x) * u));
function trackAt(tr, t, discrete) {
  if (t <= tr[0][0]) return tr[0][1];
  for (let i = 1; i < tr.length; i++) if (t <= tr[i][0]) {
    const [t0, v0] = tr[i - 1], [t1, v1, e] = tr[i];
    if (discrete) return t >= t1 ? v1 : v0;
    return t1 === t0 ? v1 : mix(v0, v1, EASES[e]((t - t0) / (t1 - t0)));
  }
  return tr[tr.length - 1][1];
}
function bake(c) {
  const [t0k, p0] = c.keys[0];
  if (t0k !== 0) throw new Error(`clip ${c.name}: the first key must be tick 0`);
  const first = {...DEFAULT_POSE, ...p0}, tracks = Object.fromEntries(Object.keys(DEFAULT_POSE).map(ch => [ch, [[0, first[ch], 'io']]]));
  let last = 0;
  for (const [t, pose, ease = 'io', from = null] of c.keys.slice(1)) {
    if (t < last) throw new Error(`clip ${c.name}: key ${t} after ${last}`);
    last = t;
    for (const [ch, v] of Object.entries(pose)) {
      const tr = tracks[ch];
      if (!tr) throw new Error(`clip ${c.name}: unknown channel ${ch}`);
      if (from !== null && from > tr[tr.length - 1][0] && from < t) tr.push([from, trackAt(tr, from, DISCRETE.includes(ch)), 'io']);
      if (tr[tr.length - 1][0] === t) tr.pop();
      tr.push([t, v, ease]);
    }
  }
  if (last !== c.len) throw new Error(`clip ${c.name}: the last key ${last} != len ${c.len}`);
  const poses = [];
  for (let t = 0; t <= c.len; t++) {
    const p = Object.fromEntries(Object.entries(tracks).map(([ch, tr]) => [ch, trackAt(tr, t, DISCRETE.includes(ch))]));
    for (const o of c.over || []) o(t, p);
    poses.push(p);
  }
  if (c.pend !== false) simulatePendulum(c, poses);
  c.keys = poses.map((p, t) => [t, p, 'l']);
  delete c.over;
  return c;
}

// ---- poses used by several clips -------------------------------------------------------------------------------------
// The groggy slump (model.md §9): ring centre 3.3 b, roll 25 and pitch 8, the core sunk under the ring with the arch
// upright, halo slid and tilted, pods slow and low, medallions sunk beside the core, the flame out.
const GROGGY = {...CRUISE, ...scaled(.25), pos: [0, 3.3, 0], rot: [8, 0, 25], haloO: [.6, 1.4, 0], haloE: [0, 0, 30], coreO: [0, -.9, 0],
  arch: [0, 0, 0], eye: [-25, 0], brim: [-10, 6], drY: -.9, drR: 2.6, plY: -1.12, plS: .9, pl2Y: -1.0, pl2S: .8, pdY: -.9, pglow: 0,
  ...medals(90, 3.2, -1.0), wHalo: .56, wArch: 0, wPlate: 0};
const CRUISE_STACK = {coreO: [0, 0, 0], eye: [0, 0], arch: [-35, 0, 0], brim: CRUISE.brim, drR: CRUISE.drR, drY: CRUISE.drY, drS: 1, drSp: 45,
  plY: CRUISE.plY, plS: 1, pl2Y: CRUISE.pl2Y, pl2S: 1, pdY: CRUISE.pdY, haloO: CRUISE.haloO, haloE: [0, 0, 0], haloS: 1, halo2O: CRUISE.halo2O, halo2S: 1};
const FIELD_LINKS = {blLen: FIELD.blLen, brLen: FIELD.brLen, blW: FIELD.blW, brW: FIELD.brW, blPd: 90, brPd: 90, blYo: 180, brYo: 180, beamLook: 'link'};

// ---- the clips ------------------------------------------------------------------------------------------------------
export const CLIPS = [];
const add = c => { CLIPS.push(bake(c)); return c; };
// the cruise hover: bob +-0.12 over 80 t, a pitch wobble +-1.5 over 120 t and a roll wobble +-1.1 over 240 t, the
// arch rocking +-20 about its 35 degree tilt over 80 t, the halo floating 0.04 b behind the bob. Every term is 0 at
// t0, so a clip that ends in the cruise pose meets idle_cruise's first tick exactly.
const cruiseHover = (a = null, b = null, r = 10, t0 = 0) => [osc('pos', 1, .12, 80, {a, b, r, t0}), osc('rot', 0, 1.5, 120, {a, b, r, t0}),
  osc('rot', 2, -1.1, 240, {a, b, r, t0}), osc('arch', 0, 20, 80, {phase: Math.PI, a, b, r, t0}), osc('haloO', 1, -.04, 40, {a, b, r, t0})];

add({name: 'idle_cruise', len: 240, loop: true, keys: [k(0, {...CRUISE}), k(240, {})], over: cruiseHover(),
  note: 'Cruise hover (loop): ring centre 4.5 b, bob +-0.12 b over 80 t, a +-1.5 degree pitch wobble over 120 t and a +-1.1 roll wobble over 240 t, the arch tilted 35 and rocking +-20 over 80 t, the halo floating behind the bob, the pendulum swinging with the wobble (simulated). Spinners: halo 2.25, inner ring -4.5, brim 4.5, eye medallion 4.5, gear medallion -6, drill pods 11.25, plates 1.5 degrees per tick (exact whole symmetry steps in 240 t).'});

add({name: 'glide', len: 80, loop: true, keys: [k(0, {...CRUISE, rot: [-3, 0, 0], pdSw: [-3, 0], drY: -1.0}), k(80, {})],
  over: [osc('pos', 1, .07, 40), osc('rot', 2, 1.5, 80), osc('rot', 0, .8, 40), osc('arch', 0, 15, 80, {phase: Math.PI}),
    osc('haloO', 1, -.03, 40), osc('drAz', 0, 3, 40)],
  note: 'Travel (loop, while the module glides the body in or out at 0.15-0.18 b/t): nose down 3 degrees, a quicker bob +-0.07 over 40 t, a +-1.5 degree roll sway, the pendulum trailing 3 degrees, the drill pods 0.05 b lower and swaying round the axis.'});

// ---- the entrance: dormant -> clank (16) -> pods unfold (20-30) -> crown assembly (30-50) -> eye (60) -> the arch
// turns (60-78) -> the rise 2.8 -> 4.5 b (64-94, untargetable until risen) -> settle (94-110). v1 0.0-5.5 s.
{
  const H0 = 2.15, H1 = 2.8;
  add({name: 'entrance', len: 110, next: 'idle_cruise', forms: [[0, 'dormant'], [94, 'cruise']],
    events: {clank: 16, pods: 20, unfold: 30, eye: 60, turn: 60, rise: 64, risen: 94, face: 99, settled: 110},
    keys: [k(0, {...DORMANT, lk: 'off', pdY: .1, glowLook: 'flash', glowS: 0, eye: [75, 0]}),
      k(17, {pos: [0, H0 - .07, 0], rot: [0, 0, -1.6]}, 'i', 15), k(19, {pos: [0, H0 + .03, 0], rot: [0, 0, 1.0]}, 'o'),
      k(22, {pos: [0, H0, 0], rot: [0, 0, 0]}),
      k(23, {glowS: .9}, 'o', 20), k(26, {glowS: .45}), k(29, {glowS: 0}),
      k(30, {drR: 2.95, drY: -.95, drS: 1, drSp: 45, wDrill: 11.25, plS: .9}, 'o', 20),
      k(40, {haloO: [0, 1.1, 0], haloS: .75, halo2O: [0, .9, 0], halo2S: .6}, 'o', 31),
      k(50, {pos: [0, H1, 0], haloO: [0, 1.6, 0], haloS: 1, halo2O: [0, 1.35, 0], halo2S: 1, coreS: 1, coreO: [0, .35, 0], brim: [-16, 14],
        plS: 1, pl2S: 1, eye: [40, 0], ...RATES}, 'io', 30),
      k(59, {lk: 'off'}), k(60, {lk: 'el'}),
      k(70, {arch: [30, 0, 0], eye: [30, 0]}, 'i', 60), k(78, {arch: [-35, 0, 0], eye: [0, 0], coreO: [0, 0, 0]}, 'o', 64),
      k(94, {pos: [0, 4.5, 0]}, 'io', 64), k(99, {pos: [0, 4.57, 0]}, 'o'), k(104, {pos: [0, 4.47, 0]}), k(110, {pos: [0, 4.5, 0]}, 'io')],
    over: [(t, p) => { p.pdY = Math.max(CRUISE.pdY, 2.25 - p.pos[1]); }, stackFollow(CRUISE.plY, -.95), ...cruiseHover(98, 400, 10, 110)],
    note: 'Dormant -> cruise (untargetable until risen): folded at ring centre 2.15 b (temporary off look), the clank jolt (16), a gold flare at the hub (20-29), the four pods drop and spin up (20-30), the halo and the inner ring rise out of the hole, the core drum grows on top and the ring lifts to 2.8 b with the plate and pendulum hanging under it, the dagger near the floor (30-50), the eye opens (60: call look/idle; the clip ends its temporary off look there), the arch turns from flat to its 35 degree tilt and the eye swings from up to the front (60-78), the rise 2.8 -> 4.5 b (64-94, eased) with the stack spreading as it leaves the floor, a small overshoot and settle (94-110). The module turns the body to the player (face/track) from risen.'});
}

// ---- C1 일점 상쇄 (폭격): the run (bomb_run 0-57), then the finisher (slam, chained at 57 and played by the module at the same
// tick): turn 0-10, ports 10-12, drop 12-57 | column 57-70, plunge 70-74, slam 74, rise 74-94. v1 5.75-10.6 s.
add({name: 'bomb_run', len: 57, next: 'slam', events: {turn: 0, ports: 10, run: 12, drop: 12, end: 57},
  keys: [k(0, {...CRUISE}), k(10, {rot: [-16, 0, 0], pos: [0, 4.8, 0], haloO: [0, 1.6, .1], lk: 'charge'}, 'io'),
    k(57, {rot: [0, 0, 0], pos: [0, 4.5, 0], haloO: [0, 1.6, 0]}, 'io', 48)],
  over: [osc('rot', 2, 3, 28, {a: 12, b: 52, r: 6}), osc('pos', 1, .05, 20, {a: 12, b: 52, r: 6}), osc('haloO', 2, .04, 20, {a: 12, b: 52, r: 6})],
  drive: [[12, 22, 0, -.012], [52, 57, 0, .02]],
  note: 'C1 bombing run: turn to the player and nose down 16 degrees while rising to 4.8 b (0-10), the bomb ports glow (10-12: temporary charge look), the run 12-57 (the module glides the body at 0.55 b/t and drops the bombs at port_0..7; the pendulum trails the acceleration, a 3 degree roll sway), level out and back to 4.5 b (48-57). It chains into slam at 57 (the module plays slam on the same tick): the finisher column 57-70, plunge 70-74, slam 74, rise 74-94 on the combined clock.'});

// ---- C2 내려찍기 (also the C1 finisher): the column tell 13 t from the face-down core, the plunge 4 t, the slam, the rise
add({name: 'slam', len: 37, next: 'idle_cruise', events: {column: 0, plunge: 13, slam: 17, impact: 17, rise: 22, risen: 37},
  keys: [k(0, {...CRUISE, lk: 'charge', colDir: 'down', colLen: 0, colW: 1.0, colLook: 'gold'}),
    k(4, {eye: [-90, 0], arch: [90, 0, 0], coreO: [0, -.35, 0], rot: [-5, 0, 0]}, 'o'),
    k(8, {colLen: 4.2}, 'o', 4),
    k(13, {pos: [0, 4.75, 0], colLen: 4.42, rot: [-3, 0, 0], haloO: [0, 1.7, 0]}, 'o', 8),
    k(15, {haloO: [0, 1.95, 0]}),
    k(17, {pos: [0, 2.1, 0], rot: [0, 0, 0], colLen: 1.75, pdY: .15, plY: -.72, pl2Y: -.6, pl2S: .9, drY: -.55, drR: 3.1,
      haloO: [0, 1.15, 0], halo2O: [0, 1.0, 0]}, 'i', 13),
    k(18, {pos: [0, 2.02, 0], rot: [0, 0, -1.8], colLen: .3, haloO: [0, 1.05, 0]}, 'o'), k(19, {colLen: 0}),
    k(20, {pos: [0, 2.1, 0], rot: [0, 0, 1.0], haloO: [0, 1.25, 0]}), k(22, {rot: [0, 0, 0], lk: 'el'}),
    k(37, {pos: [0, 4.5, 0], ...CRUISE_STACK}, 'io', 22)],
  note: 'C2 slam (and the C1 finisher): the eye turns face down, the arch flat, the core sinks 0.35 b (0-4) and the gold column reaches the floor (4-8), the tell holds while the device lifts 0.25 b (8-13), the plunge to ring centre 2.1 b (13-17, ease in) with the stack compressed and the halo lagging, the slam (17: the module hits r 5), the bounce and sit (17-22), the rise back to 4.5 b (22-37). Temporary charge look 0-22.'});

// ---- C3 코어 (레이저 빔): dock 0-4, charge 4-22, aim lines 20, fire 22-155 (counter-orbit 5 degrees per tick), retract 155-165
{
  const F0 = 22, F1 = 155, R = 165, DOWN = medals(90, 2.8, -2.0, [-42, 0, 0]);
  add({name: 'laser', len: R, next: 'idle_cruise', forms: [[4, 'laser'], [R, 'cruise']],
    events: {dock: 0, drop: 0, charge: 4, aim: 20, fire: F0, off: F1, retract: F1, end: R},
    orbit: {from: F0, to: F1, rate: 5, medal_eye: {az0: 90, sense: -1}, medal_gear: {az0: -90, sense: 1}, beam: {from_down: 48, length: 3.74, spot_r: 5.58},
      note: 'azimuths in degrees round the ring axis from the device front toward its left (+x): eye = 90 - 5 (t - from), gear = -90 + 5 (t - from)'},
    keys: [k(0, {...CRUISE}), k(4, {...DOWN, lk: 'charge'}, 'o'),
      k(19, {blLen: 0, brLen: 0, blW: .12, brW: .12}), k(20, {blLen: 3.74, brLen: 3.74}, 'l'),
      k(F0, {blW: .5, brW: .5, pos: [0, 4.55, 0]}, 'l'), k(F0 + 3, {blW: 1.0, brW: 1.0, pos: [0, 4.66, 0]}, 'o'), k(F0 + 9, {pos: [0, 4.6, 0]}),
      k(F1, {blW: .5, brW: .5, pos: [0, 4.6, 0]}, 'io', F1 - 7), k(F1 + 2, {blLen: 0, brLen: 0, blW: .1, brW: .1, lk: 'el'}),
      k(R, {...medals(90, DOCK[0], DOCK[1], FACE_FRONT), pos: [0, 4.5, 0]}, 'io', F1)],
    over: [(t, p) => {
      const a = t < F0 ? 0 : t <= F1 ? 5 * (t - F0) : 5 * (F1 - F0) + 5.5 * (t - F1);
      p.meAz = 90 - a; p.mgAz = -90 + a;
    }, osc('pos', 1, .05, 35, {a: F0 + 10, b: F1, r: 8}), osc('meY', 0, .04, 4, {a: 6, b: F0, r: 3}), osc('mgY', 0, .04, 4, {phase: 1.6, a: 6, b: F0, r: 3})],
    note: 'C3 lasers: the medallions drop from the ring-end docks to r 2.8 b, 2 b under the ring, faces turned down-out (0-4), the charge (4-22: temporary charge look, the medallions trembling), thin aim lines (20), the beams fire at 22 (48 degrees from straight down: floor spots on r 5.58 b at ring centre 4.5) with a width bloom 0.5 -> 1.0 b (22-25) and a recoil lift, then both medallions orbit the ring axis in opposite directions at exactly 5 degrees per tick for 133 t (manifest orbit: the eye medallion from the left toward the front, the gear from the right toward the front; the spots meet in front 18 t after fire, then every 36 t, back and front), the width back to 0.5 (148-155), the beams off (155-157), the medallions rise back into the docks while finishing their second turn (155-165).'});
}

// ---- C4 바위 폭탄 (미사일): tell 0-23 (tip flares 0-8, the vent column 8-23), launches 23-37, recover to 60
add({name: 'missiles', len: 60, next: 'idle_cruise', events: {flare: 0, tell: 0, vent: 8, launch: 23, last: 37, end: 60},
  keys: [k(0, {...CRUISE, lk: 'charge'}), k(8, {...spikes(DOCK, [0, 0, 10]), eye: [90, 0], arch: [90, 0, 0], coreO: [0, .2, 0],
      colDir: 'up', colLen: 0, colW: 1.5, colLook: 'gold'}, 'o'),
    k(12, {colLen: 6.0, haloO: [0, 2.0, 0]}, 'o', 8), k(25, {pos: [0, 4.42, 0]}, 'o', 23), k(37, {pos: [0, 4.44, 0]}),
    k(41, {colLen: 0}, 'i', 38), k(42, {colDir: 'down', lk: 'el'}),
    k(60, {...spikes(DOCK), eye: [0, 0], arch: [-35, 0, 0], coreO: [0, 0, 0], pos: [0, 4.5, 0], haloO: [0, 1.6, 0]}, 'io', 42)],
  over: [osc('rot', 2, .8, 4, {a: 0, b: 9, r: 2}), osc('pos', 1, .025, 3, {a: 23, b: 38, r: 2}), osc('rot', 0, .6, 3, {phase: 1, a: 23, b: 38, r: 2}),
    osc('colW', 0, .12, 5, {a: 12, b: 38, r: 3}), ...cruiseHover(44, 400, 10, 60)],
  note: 'C4 missiles: the spikes tip up 10 degrees and tremble while their tips flare (0-8: the module\'s fx at spike_tip_l / r), the eye turns up, the arch lies flat and the gold vent column rises 6 b from the core, lifting the halo 0.4 b (8-12), held and flickering (12-23), ten launches 23-37 from vent_l / vent_r (the module\'s missiles) with a 0.08 b recoil sag and pitch shudder, the column drops away (38-41), everything back to cruise by 60. Temporary charge look 0-42.'});

// ---- C5 지면 충격 (중력 폭발): the core flip-up (model.md §5.3; v4 P0 = 2.55 s)
add({name: 'coreup', len: 130, next: 'idle_cruise', forms: [[15, 'coreup'], [120, 'cruise']],
  events: {spark: 0, eye: 1, rim: 3, lift: 5, up: 15, beam: 29, column: 41, blast: 48, sink: 81, end: 130},
  keys: [k(0, {...CRUISE, lk: 'charge'}), k(4, {arch: [0, 0, 0], eye: [0, 0]}, 'o'),
    k(5, {glowS: 0, glowLook: 'flash'}), k(7, {glowS: 1.6}, 'o'), k(8, {glowS: 1.1}), k(9, {glowS: 0, glowLook: 'gold'}), k(10, {glowS: 1.0}, 'o'),
    k(15, {pos: [0, 5.0, 0], rot: [0, 0, 10], coreO: [0, 2.8, 0], brim: [-22, -12], hub: 180,
      ...spikes([3.6, .3, 0], [0, 0, 90]), ...medals(90, 3.6, .3), drR: 2.4, drY: -1.0, plY: -2.95, pl2Y: -2.75, pdY: -2.6, pglow: 1, glowS: 1.02}, 'o', 6),
    k(28, {colDir: 'up', colLen: 0, colW: 1.3, colLook: 'gold'}), k(32, {colLen: 6.0}, 'o'), k(40, {colLen: 6.0}), k(41, {colDir: 'down', colLen: 0}),
    k(44, {coreO: [0, .6, 0], colLen: 5.6}, 'i', 41),
    k(48, {colLen: 5.6}), k(49, {pos: [0, 5.14, 0], rot: [0, 0, 12.5], colLen: 2.0}, 'o', 48), k(50, {colLen: 0}),
    k(54, {pos: [0, 5.0, 0], rot: [0, 0, 10]}), k(62, {glowS: 0}, 'io', 56),
    k(81, {glowLook: 'charge', lk: 'el'}),
    k(96, {coreO: [0, 0, 0], arch: [-20, 0, 0], rot: [0, 0, -9], pos: [0, 4.8, 0], hub: 90}, 'io', 81),
    k(108, {...spikes(DOCK), ...medals(90, DOCK[0], DOCK[1]), hub: 0, rot: [0, 0, 5], arch: [-35, 0, 0], brim: CRUISE.brim}, 'io', 90),
    k(120, {...CRUISE, rot: [0, 0, -2]}, 'io', 100), k(130, {rot: [0, 0, 0]}, 'io')],
  over: [osc('pos', 1, .05, 24, {a: 16, b: 41, r: 4}), osc('pos', 1, .05, 30, {a: 54, b: 81, r: 6})],
  note: 'C5 ground impact: the spark (0; module fx at core), the arch stands upright and the eye faces out (1-4), the gold flash (5-8: core_glow 0 -> 1.6 -> 1.1), the lift (6-15, ease out): the exposed gold sphere rises 2.8 b over the ring, the device rises to 5.0 b and rolls 10 degrees, the spikes roll to vertical, the medallions slide to the ring ends facing out and the iris spike flips up (three eyes in a row), hold (15-28), the up-beam (28-40: gold column up 6 b), the core drops back to +0.6 b in 3 t and the column goes down to the floor (41-44), the blast (48: the module hits; a recoil jolt), hold (49-81), the return: the core sinks into the hole, the arch swings back, the iris spike flips down, spikes and medallions re-dock, a roll rock (81-130).'});

// ---- C6 파쇄 (바위 날리기): dip 0-12, vent flare 12-20, tower 20-38, flame band 38-55, bursts 55..97 every 6 t, throws
// 100..132 every 8 t, revert 140-155 (v3 17.0-24.85 s)
{
  const BURSTS = [55, 61, 67, 73, 79, 85, 91, 97], THROWS = [100, 108, 116, 124, 132];
  add({name: 'tower_throw', len: 155, next: 'idle_cruise', forms: [[38, 'tower'], [150, 'cruise']],
    events: {dip: 0, flare: 12, vent: 12, tower: 20, band: 38, charge: 38, burst: 55, burst_last: 97, throw: 100, throw_last: 132, revert: 140, end: 155},
    bursts: BURSTS, throws: THROWS,
    keys: [k(0, {...CRUISE}), k(10, {lk: 'charge'}),
      k(12, {pos: [0, 2.9, 0], rot: [-24, 0, 8], pdY: -.6, plY: -.95, pl2Y: -.83, drY: -.75, haloO: [0, 1.75, 0]}, 'io'),
      k(13, {colDir: 'up', colLen: 0, colW: 1.2, colLook: 'gold'}), k(16, {colLen: 4.5}, 'o'),
      k(20, {...medals(90, 5.5, 2.2, FACE_FRONT), ...spikes(DOCK, [0, 0, 15])}, 'o', 12), k(22, {colLen: 0}, 'io', 18),
      k(36, {...medals(90, .5, 3.15)}, 'io', 26),
      k(38, {...TOWER, pos: [0, 4.5, 0], rot: [0, 0, 0], colDir: 'up', colLen: 0, lk: 'charge'}, 'io', 20),
      k(46, {wT1: 4.5, wT2: -4.5}, 'io', 38), k(104, {wT1: RATES.wT1, wT2: RATES.wT2}, 'io', 97),
      k(142, {lk: 'el'}), k(146, {rot: [0, 0, -18]}, 'io', 140), k(150, {...CRUISE, rot: [0, 0, 9]}, 'io', 140), k(155, {rot: [0, 0, 0]}, 'io')],
    over: [...BURSTS.map(b => ring('pos', 1, -.06, b, 6, 3)), ...BURSTS.map(b => ring('twT2S', 0, .07, b, 6, 3)),
      ...THROWS.map((b, i) => ring('rot', 2, i % 2 ? 2.5 : -2.5, b, 8, 4)), osc('pos', 1, .04, 18, {a: 38, b: 55, r: 4}),
      osc('rot', 2, .6, 5, {a: 40, b: 55, r: 3}), osc('pos', 1, .06, 40, {a: 100, b: 140, r: 8})],
    note: 'C6 rock throw: the dip toward the player to ring centre 2.9 b, nose down 24 and rolled 8 (0-12, the stack compressed), the vent: the gold column up 4.5 b and the medallions flung up and out to +-5.5 b (12-20), the rise and level while the tower telescopes up (20-38: column, tiers +1.35 / +2.0, the halo x1.7 at +3.2, the inner ring at +2.5, the end spikes up 45, the iris spike up, the medallions docking on the column top by 36, the Ousia flame), the flame band charge (38-55: the tiers counter-rotate at 4.5 degrees per tick, the device trembles), eight bursts 55..97 every 6 t (manifest bursts: a dip and a tier pulse each), five throws 100..132 every 8 t (manifest throws: a roll twitch each), the revert: the tower folds back with a roll wobble -18 -> 9 -> 0 (140-155). Temporary charge look 10-142.'});
}

// ---- the field opener: warp_out (halo flip, hidden from 12; the module moves the body at out = 13 and plays
// warp_in_field at 34) and warp_in_field (shown again at 0-2, the unfold into the field form 1-17, links 17-21)
add({name: 'warp_out', len: 34, next: null, hidden: [12, -1], events: {flip: 0, hide: 12, out: 13, end: 34},
  keys: [k(0, {...CRUISE}), k(11, {rot: [35, 0, 0], haloE: [90, 0, 0], haloO: [0, 2.0, 0], wHalo: 12}, 'io'),
    k(12, {vis: 0}, 'i', 11), k(34, {vis: 0})],
  note: 'Warp out: the halo flips upright and spins like a wheel while the device pitches nose up 35 degrees, showing its underside (0-11), the rig scales to 0 in 1 t (11-12; the module\'s warp flash at hide 12) and stays hidden to the end; it holds hidden until the module plays warp_in_field (34). Moving the body is invisible from 12 (the module moves it at out 13).'});
add({name: 'warp_in_field', len: 40, next: 'field_idle', hidden: [-1, 1], forms: [[17, 'field']],
  events: {in: 0, unfold: 1, field: 17, links: 17, banner: 22, settled: 40},
  keys: [k(0, {...CRUISE, ...STILL, vis: 0, pos: [0, 5.8, 0], glowLook: 'flash', glowS: 1.6}), k(2, {vis: 1, ...RATES, wArch: 1}, 'o'), k(5, {glowS: 0}),
    k(12, {...FIELD, glowS: 0, coreO: [0, -2.05, 0], plY: -3.5, pl2Y: -3.3, pdY: -3.55, haloO: [0, 1.8, 0], halo2O: [0, 1.5, 0], drY: -2.2,
      ...medals(90, 4.1, -2.0), blLen: 0, brLen: 0, colLen: 0, wArch: 3}, 'o', 1),
    k(17, {...FIELD, blLen: 0, brLen: 0, colLen: 0}, 'io'), k(21, {...FIELD_LINKS, colLen: FIELD.colLen}, 'o'), k(40, {...FIELD}, 'io')],
  over: [osc('pos', 1, .1, 120, {a: 22, b: 400, r: 10, t0: 40})],
  note: 'Warp in at the arena centre: a white-gold flash and vis 0 -> 1 (0-2) at ring centre 5.8 b, then the unfold like a spring (1-17): the core drops out of the hole and hangs, the plates and pendulum spread, the pods move out to core level, the medallions slide out beside the core, the arch starts its gyroscope turn, overshooting at 12 and settling at 17; the gold link beams and the violet column appear (17-21); settle (21-40). Call crack/0 + look/field at unfold (the violet halos and the bubble).'});

// ---- 「인력 충격파」: the charge sphere with 4 pulses (24 t; 40 t for the long one), the 1 t beam down, the burst
function waveClip(name, charge, note) {
  const b = charge - 1, keys = [k(0, {...FIELD, glowS: 0, glowLook: 'charge'})];
  for (let i = 0; i < 4; i++) {
    const t1 = Math.round(b * (i + .55) / 4), t2 = Math.round(b * (i + 1) / 4), g = 1.5 * (.3 + .7 * (i + 1) / 4);
    keys.push(k(t1, {glowS: g * 1.1}, 'o'));
    if (i < 3) keys.push(k(t2, {glowS: g}, 'i'));
  }
  keys.push(k(b - 1, {glowS: 1.45}), k(b, {colLen: 4.1, colW: .5, colLook: 'gold', glowS: 1.75}, 'i', b - 1),
    k(charge, {colLen: FIELD.colLen, colW: FIELD.colW, colLook: 'violet', glowS: .9, pos: [0, 5.96, 0]}, 'o', b),
    k(charge + 3, {glowS: 0}), k(charge + 12, {pos: [0, 5.8, 0]}, 'io'), k(charge + 16, {}));
  return {name, len: charge + 16, next: 'field_idle', events: {charge: 0, beam: b, burst: charge, impact: charge, end: charge + 16},
    keys, over: [osc('pos', 1, .04, 12, {a: 0, b: charge, r: 4})], note};
}
add(waveClip('wave', 24, '「인력 충격파」 one wave: the charge sphere (core_glow charge) grows round the core to 1.5 in four pulses (0-23), the 1 t gold beam from the core to the floor (beam 23), the burst (24 = impact: the module starts the front at 0.55 b/t), a 0.16 b recoil lift and settle (24-40).'));
add(waveClip('wave_long', 40, 'The long 「인력 충격파」 (the opening third wave): a 40 t charge in four pulses (0-39), the beam (39), the burst (impact 40), settle (40-56).'));
add({name: 'wave_drop', len: 84, next: 'field_idle', events: {charge: 0, beam: 39, burst: 40, impact: 40, drop: 40, land: 44, lift: 63, risen: 83, end: 84},
  keys: [k(0, {...FIELD, glowS: 0, glowLook: 'charge'}), k(20, {glowS: 1.1, pos: [0, 5.55, 0]}), k(39, {pos: [0, 5.3, 0], pdY: -3.0, glowS: 1.5}),
    k(40, {colLen: 3.6, colW: .5, colLook: 'gold', glowS: 1.75}, 'l', 39), k(41, {colLen: 0, colLook: 'violet'}),
    k(44, {pos: [0, 2.4, 0], coreO: [0, -1.1, 0], plY: -1.9, pl2Y: -1.65, pdY: -.2, drY: -1.2, ...medals(90, 3.6, -1.1), blLen: 2.3, brLen: 2.3, glowS: 0}, 'i', 40),
    k(46, {pos: [0, 2.35, 0], rot: [0, 0, 1.5]}, 'o'), k(49, {pos: [0, 2.4, 0], rot: [0, 0, 0]}),
    k(63, {glowS: 0, glowLook: 'flash'}), k(64, {pos: [0, 2.6, 0], glowS: 1.4}, 'o', 63), k(68, {glowS: 0}),
    k(83, {...FIELD, glowLook: 'charge'}, 'io', 64), k(84, {})],
  note: 'The closing third wave with the drop (v2 B3): the charge sinks the device 0.5 b (0-39), the beam (39) and the burst (impact 40), then the drop -2.9 b in 4 t onto the floor with the stack compressed (ring centre 2.4 b, the core resting on the floor; 40-44), grounded 19 t, the lift-off flash (63) and the rise (63-83).'});

// ---- the field form: hover, the 감소 영역 activation and its active hover, the field rock throw, the pack-up
// (every hover term is 0 at tick 0, so clips ending in the field pose meet field_idle exactly)
const fieldHover = () => [osc('pos', 1, .1, 120), osc('rot', 0, 1.0, 240), osc('rot', 2, -1.0, 120),
  osc('meY', 0, .08, 80), osc('mgY', 0, -.08, 80), osc('blW', 0, .04, 60), osc('brW', 0, -.04, 60),
  osc('haloO', 1, -.05, 60), osc('halo2O', 1, .04, 60)];
add({name: 'field_idle', len: 240, loop: true, keys: [k(0, {...FIELD}), k(240, {})],
  over: [...fieldHover(), (t, p) => { p.drAz = 360 * t / 240; }],
  note: 'Field hover (loop): ring centre 5.8 b, bob +-0.1 b over 120 t, a slow +-1 degree wobble, the core hanging with the arch turning round it like a gyroscope (3 degrees per tick), the medallions bobbing beside it on pulsing link beams, the four pods orbiting at core level (1.5 degrees per tick), the violet column and the Ousia flame.'});
add({name: 'field_erupt', len: 22, next: 'field_active', events: {activate: 0, lock: 12, erupt: 22},
  keys: [k(0, {...FIELD}), k(12, {arch: [0, 0, 0], wArch: 0, eye: [0, 0], pos: [0, 5.92, 0]}, 'o'),
    k(17, {glowS: 0, glowLook: 'flash'}),
    k(22, {...medals(90, 4.2, -1.7), blLen: 2.85, brLen: 2.85, blW: .5, brW: .5, pos: [0, 5.95, 0], glowS: 1.4}, 'o', 12)],
  over: [osc('meY', 0, .03, 3, {a: 4, b: 20, r: 2}), osc('mgY', 0, .03, 3, {phase: 1.5, a: 4, b: 20, r: 2})],
  note: 'F1 감소 영역 activation (22 t, the tell of the whole pattern): the gyroscope arch slows and locks facing the front, the eye looks out and the device rises 0.15 b (0-12), the medallions slide out to r 4.2 b on brightening link beams and the core flashes gold (12-22; erupt: the module starts the eruption events). Then it loops in field_active until the module plays another clip.'});
add({name: 'field_active', len: 240, loop: true, keys: [k(0, {...FIELD, arch: [0, 0, 0], wArch: 0, ...medals(90, 4.2, -1.7), blLen: 2.85, brLen: 2.85, blW: .5, brW: .5, pos: [0, 5.95, 0]}), k(240, {})],
  over: [osc('pos', 1, .06, 80), osc('rot', 2, -.8, 120), osc('meY', 0, .06, 80), osc('mgY', 0, -.06, 80),
    osc('blW', 0, .06, 20), osc('brW', 0, -.06, 20), (t, p) => { p.drAz = 360 * t / 240; }],
  note: 'The activated field hover (loop, after field_erupt): the arch locked facing the front, the eye out, the medallions at r 4.2 b on bright pulsing link beams, a slower bob, the pods orbiting. Play field_idle (or any clip) when the pattern is over.'});
{
  const BURSTS = [25, 31, 37, 43, 49, 55, 61, 67], THROWS = [65, 73, 81, 89, 97];
  add({name: 'frock', len: 110, next: 'field_idle', events: {vent: 0, flame: 8, burst: 25, burst_last: 67, throw: 65, throw_last: 97, end: 100},
    bursts: BURSTS, throws: THROWS,
    keys: [k(0, {...FIELD}), k(4, {colDir: 'up', colLen: 0, colW: 1.2, colLook: 'gold', arch: [0, 0, 0], wArch: 0}),
      k(8, {colLen: 4.0, rot: [0, 0, 6]}, 'o', 4), k(12, {colLen: 0}), k(13, {colDir: 'down', colLook: 'violet', colW: FIELD.colW}),
      k(18, {colLen: FIELD.colLen}, 'io', 13), k(25, {rot: [0, 0, 0]}, 'io', 18),
      k(110, {...FIELD}, 'io', 100)],
    over: [...BURSTS.map(b => ring('pos', 1, -.05, b, 6, 3)), ...THROWS.map((b, i) => ring('rot', 2, i % 2 ? 2 : -2, b, 8, 4)),
      osc('rot', 2, .5, 5, {a: 9, b: 25, r: 3})],
    note: 'F2 rock throw in the field form (the module plays it for F2): the arch locks, the gold vent column up 4 b with a roll (0-12), back to the violet column (12-18), the flame band (8-25: module fx, the device trembles), eight bursts 25..67 every 6 t (manifest bursts: a dip each), five throws 65..97 every 8 t (manifest throws: a roll twitch each), end 100, back to the field hover (100-110).'});
}
// the field closes unbroken (v2 B4): lift-off flash, rise, lances (vertical, then horizontal), the pack-up roll with the
// core swinging up to the top, the lances dock, compact
add({name: 'field_end', len: 70, next: 'idle_cruise', archFlip: true, forms: [[20, 'deployed'], [70, 'cruise']],
  events: {lift: 0, rise: 2, lances: 20, horiz: 32, pack: 40, dock: 58, packed: 70},
  keys: [k(0, {...FIELD, glowS: 0, glowLook: 'flash', wArch: 0}), k(2, {glowS: 1.5}, 'o'), k(6, {glowS: 0, blLen: 0, brLen: 0}), k(10, {colLen: 0}, 'io', 4),
    k(20, {pos: [0, 6.3, 0], ...spikes(DOCK, [0, 0, -90])}, 'io', 2),
    k(28, {...spikes([5.6, -.6, 0], [0, 0, -90]), ...medals(90, 5.6, -.6), drR: 3.8, drY: -1.2, plY: -3.0, pl2Y: -2.6, pdY: -3.2}, 'o', 20),
    k(40, {...spikes([5.6, -.6, 0], [0, 0, 0])}, 'io', 32),
    k(44, {rot: [4, 0, 24], coreO: [0, -1.2, 0], arch: [-80, 0, 0], pdY: -2.6, plY: -2.4, pl2Y: -2.2}, 'io', 40),
    k(50, {rot: [-3, 0, -15], coreO: [0, -.4, 0], arch: [-160, 0, 0], pos: [0, 5.6, 0]}, 'io'),
    k(55, {rot: [2, 0, 8], coreO: [0, 0, 0], arch: [-215, 0, 0]}, 'io'),
    k(58, {...spikes([4.6, -.25, 0]), ...medals(90, 4.6, -.25)}, 'io', 50),
    k(62, {rot: [0, 0, 0], ...spikes(DOCK), ...medals(90, DOCK[0], DOCK[1]), drR: 2.95, drY: -.95, pos: [0, 4.9, 0]}, 'io'),
    k(70, {...CRUISE, arch: [-215, 0, 0]}, 'io', 55)],
  note: 'Unbroken field end (pack-up): the lift-off flash (0-6) and the rise to 6.3 b (2-20) while the link beams and the violet column go out and the gyroscope stops, the spikes turn spike-down in their docks (2-20), the lances: they move out to 5.6 b with the medallions in their X frames (20-28), then turn horizontal pointing outward (32-40: the deployed form), the pack-up roll 24 -> -15 -> 8 degrees while the core swings up from under the ring to the top (the arch turns 180 degrees over; 40-55), the lances dock as the rim spikes and the pods tuck (50-62), settle to 4.5 b (55-70). Call look/idle at dock (58).'});

// ---- 20 hits: the break (bubble burst, tilt, wobble, sink), the groggy slump, the recovery (re-level, core flip)
add({name: 'break', len: 40, next: 'groggy', events: {bubble: 0, burst: 5, tilt: 5, wobble: 14, sink: 14, slumped: 40},
  keys: [k(0, {...FIELD, shellS: 1, glowS: 0, glowLook: 'flash', wArch: 0}), k(5, {shellS: 1.12, glowS: 1.35}, 'i'),
    k(7, {shellS: 1.6, blLen: 0, brLen: 0, colLen: 0, glowS: 1.7}, 'o', 5), k(8, {shellS: 0, pglow: 0, lk: 'groggy'}, 'l'), k(9, {glowS: 0}),
    k(14, {rot: [6, 0, 28], pos: [0, 5.3, 0], arch: [0, 0, 0]}, 'o', 5),
    k(40, {...GROGGY, shellS: 1}, 'io', 14)],
  over: [ring('rot', 2, 8, 14, 10, 7), ring('rot', 0, 2.5, 15, 12, 7)],
  note: '역장 붕괴 (the 20th hit; the module calls crack/4 at burst): the bubble flares with the core (0-5), bursts (5-7: scale 1 -> 1.6 -> 0), the link beams, the violet column and the Ousia flame go out, the seam goes dark (temporary groggy look from 8), the whole device tilts 28 degrees in 9 t (5-14), a damped wobble +-8 -> 0 (14-34) while it sinks to the groggy slump at ring centre 3.3 b (14-40).'});
add({name: 'groggy', len: 160, loop: true, keys: [k(0, {...GROGGY}), k(160, {})],
  over: [osc('pos', 1, .06, 80), osc('rot', 2, 3, 160), osc('rot', 0, -1.5, 80), osc('pdSw', 1, 10, 40), osc('pdSw', 0, -3, 40), osc('haloO', 0, .05, 80)],
  note: 'Groggy slump (loop; hittable, no attacks): ring centre 3.3 b, roll 25 and pitch 8 with a slow +-3 wobble, the core sunk under the ring with the arch upright, the eye dim and the seam off (look/groggy), the halo slid and tilted, the pods spinning at a quarter speed, the medallions sunk beside the core, the pendulum swinging +-12 degrees.'});
add({name: 'recover', len: 15, next: 'idle_cruise', archFlip: true, forms: [[15, 'cruise']], events: {relevel: 0, flip: 6, done: 15},
  keys: [k(0, {...GROGGY}), k(6, {rot: [0, 0, 0], pos: [0, 4.1, 0], haloO: [0, 1.6, 0], haloE: [0, 0, 0], ...RATES, wArch: 0}, 'io'),
    k(9, {coreO: [0, -.5, 0], arch: [-90, 0, 0]}, 'i', 6), k(15, {...CRUISE, arch: [-215, 0, 0]}, 'o', 6)],
  note: 'Recovery: re-level and rise (0-6), the core flips to the top (6-15: it rises into the hole while the arch turns 180 degrees over), back in the cruise form. Call look/idle at 0.'});

// ---- death (model.md §9): the seam flickers out, the halo drops and rolls off, the pods stop and fall, the spikes
// droop, the ring tilts 40 degrees and sinks onto its low rim, the medallions clatter down, then everything scales out
add({name: 'death', len: 110, events: {flicker: 0, drop: 20, sink: 40, land: 62, out: 80, gone: 110},
  keys: [k(0, {...CRUISE, lk: 'charge'}), k(3, {lk: 'off'}), k(6, {lk: 'charge'}), k(9, {lk: 'off'}), k(12, {lk: 'charge'}), k(16, {lk: 'off'}),
    k(20, {...STILL, pos: [0, 4.6, 0]}, 'o', 14),
    k(30, {haloO: [-.8, 1.5, .2], haloE: [6, 0, -18]}, 'i', 20), k(32, {drY: -1.6, drR: 3.0}, 'i', 20),
    k(40, {rot: [6, 0, 14], pos: [0, 4.2, 0], halo2S: 0, ...spikes(DOCK, [0, 0, -30], null, [0, 0, 0])}, 'io', 26),
    k(44, {haloO: [-3.4, .6, .6], haloE: [10, 0, -40]}, 'i'),
    k(60, {pos: [0, 3.0, 0], rot: [8, 0, 40], coreO: [0, -.5, 0], eye: [-30, 0], ...spikes(DOCK, [0, 0, -45], null, [0, 0, -20]),
      ...medals(90, 2.0, -2.6, [-60, 90, 0], {r: 3.0, y: -.7}), drY: -.4, drR: 2.6, drS: .85, plY: -1.3, pl2Y: -1.15, pdY: -1.3,
      haloO: [-5.3, 1.1, 1.0], haloE: [6, 0, -36]}, 'i', 44),
    k(63, {pos: [0, 3.07, 0], rot: [8, 0, 37.5]}, 'o'), k(67, {pos: [0, 3.0, 0], rot: [8, 0, 40]}, 'i'), k(110, {vis: 0}, 'i', 80)],
  over: [(t, p) => { if (t >= 20) { const u = sm((t - 34) / 26); p.pdSw = [p.pdSw[0] + 10 * u, p.pdSw[1] - 80 * u]; } }],
  note: 'Death: the seam flickers hot / off three times (0-16) and goes dark, every spinner stops (14-20), the halo slides off the low side and lands flat on the floor (20-60), the pods drop, the spikes droop, the ring tilts 40 degrees and sinks until its low rim rests on the floor (ring centre 3.0 b; 26-60) with a small bounce (60-67), the pendulum topples over, the medallions clatter down beside the core; everything scales out (80-110). It holds there; call kill after 110.'});

// ---- form holds (form/<name> queues these) -----------------------------------------------------------------------------
add({name: 'idle_dormant', len: 40, loop: true, pend: false, keys: [k(0, {...DORMANT, pdY: .1}), k(40, {})], note: 'Dormant (form/dormant): folded on the floor at ring centre 2.15 b, still.'});
add({name: 'hold_coreup', len: 80, loop: true, keys: [k(0, {...COREUP, glowLook: 'gold', glowS: 1.02}), k(80, {})], over: [osc('pos', 1, .05, 40)], note: 'Core-up rest pose (form/coreup): the gold sphere 2.8 b over the ring, three eyes in a row with their spikes up, roll 10; bob +-0.05.'});
add({name: 'hold_tower', len: 80, loop: true, keys: [k(0, {...TOWER}), k(80, {})], over: [osc('pos', 1, .06, 40)], note: 'Tower rest pose (form/tower); bob +-0.06.'});
add({name: 'hold_laser', len: 72, loop: true, keys: [k(0, {...LASER}), k(72, {})],
  over: [(t, p) => { p.meAz = 90 - 5 * t; p.mgAz = -90 + 5 * t; }, osc('pos', 1, .05, 36)],
  note: 'Laser rest pose (form/laser): the medallions counter-orbit at 5 degrees per tick with their beams (one turn per 72 t).'});
add({name: 'hold_deployed', len: 80, loop: true, keys: [k(0, {...DEPLOYED}), k(80, {})], over: [osc('pos', 1, .08, 80)], note: 'Deployed rest pose (form/deployed): the lances far out; bob +-0.08.'});

for (const c of CLIPS) if (!c.events) c.events = {};

// ---- sampling -------------------------------------------------------------------------------------------------------
export const accumulate = clip => accumulateClip(clip, DEFAULT_POSE);
// spinner -> rate channel, symmetry step (degrees; the part looks the same turned by any multiple) and its parts
export const SPIN = {halo: 'wHalo', halo2: 'wHalo2', brim: 'wBrim', medE: 'wMedE', medG: 'wMedG', drill: 'wDrill', t1: 'wT1', t2: 'wT2', arch: 'wArch', plate: 'wPlate'};
export const SYM = {halo: 45, halo2: 22.5, brim: 360, medE: 360, medG: 180, drill: 90, t1: 22.5, t2: 90, arch: 360, plate: 360};
export const SPIN_PARTS = {halo: ['halo'], halo2: ['halo2'], brim: ['core_brim'], medE: ['medal_eye'], medG: ['medal_gear'],
  drill: ['drill_fl', 'drill_fr', 'drill_bl', 'drill_br'], t1: ['tower_col', 'tower_t1'], t2: ['tower_t2'], arch: ['core_arch'], plate: ['plate', 'plate2']};
// Integrated spin angles per tick, scaled per spinner to a whole number of its symmetry steps over the clip.
const spinCache = new WeakMap();
function spinTable(clip, ks) {
  if (spinCache.has(clip)) return spinCache.get(clip);
  const rates = Array.from({length: clip.len + 1}, (_, t) => sampleAt(clip, t, ks, {defaults: DEFAULT_POSE, discrete: DISCRETE}));
  const tab = {}, steps = {}, deg = {};
  for (const [sp, ch] of Object.entries(SPIN)) {
    const a = [0];
    for (let t = 1; t <= clip.len; t++) a.push(a[t - 1] + (rates[t - 1][ch] + rates[t][ch]) / 2);
    const total = a[clip.len], n = Math.round(total / SYM[sp]);
    const sc = n === 0 || Math.abs(total) < 1e-9 ? 0 : n * SYM[sp] / total;
    tab[sp] = a.map(x => x * sc);
    steps[sp] = n;
    deg[sp] = n * SYM[sp];
  }
  const out = {tab, steps, deg};
  spinCache.set(clip, out);
  return out;
}
export function sampleClip(clip, t, ks = accumulate(clip)) {
  const p = sampleAt(clip, t, ks, {defaults: DEFAULT_POSE, discrete: DISCRETE});
  const {tab} = spinTable(clip, ks), tt = Math.max(0, Math.min(clip.len, t)), i = Math.min(clip.len - 1, Math.floor(tt)), f = tt - i;
  p.spin = Object.fromEntries(Object.keys(SPIN).map(sp => [sp, clip.len ? tab[sp][i] + (tab[sp][Math.min(clip.len, i + 1)] - tab[sp][i]) * f : 0]));
  return p;
}
export const spinInfo = clip => { const {steps, deg} = spinTable(clip, accumulate(clip)); return {steps, deg}; };
// The end-of-clip snap of a clip that loops or chains: at its last tick (len - 1) the parts of every spinner whose
// clip angle is not a whole turn are set (interpolation 0) to the same pose turned back by that angle, which looks
// identical (a multiple of the part's symmetry step), and so is the arch of a clip that turns it over (archFlip: its
// pitch back by 180, the ring's own symmetry). The next clip's first key (tick 0, at the chain tick) then starts from
// angle 0 and continues the spin forward. Returns {t, pose, parts} or null.
export function snapPose(clip) {
  if (!(clip.loop || clip.next)) return null;
  const ks = accumulate(clip), {deg} = spinTable(clip, ks), t = clip.len - 1;
  const p = sampleClip(clip, t, ks), parts = [];
  for (const sp of Object.keys(SPIN)) {
    const d = ((deg[sp] % 360) + 360) % 360;
    if (d < 1e-6 || 360 - d < 1e-6) continue;
    p.spin[sp] -= deg[sp];
    parts.push(...SPIN_PARTS[sp]);
  }
  if (clip.archFlip) { p.arch = [p.arch[0] + 180, p.arch[1], p.arch[2]]; if (!parts.includes('core_arch')) parts.push('core_arch'); }
  return parts.length ? {t, pose: p, parts} : null;
}
// Rest pose of a form (form/<name>, the debug renders): the form's channels with the spinners at their rest angle.
export const restPose = name => ({...FORMS[name], spin: {}});
export const FORM_HOLD = {dormant: 'idle_dormant', cruise: 'idle_cruise', field: 'field_idle', coreup: 'hold_coreup', tower: 'hold_tower', laser: 'hold_laser', deployed: 'hold_deployed'};
