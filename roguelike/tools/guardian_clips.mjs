// Motion clips of the Corrupted Guardian (파수꾼・타락) rig, authored from the reference videos
// (scratchpad mboss/understand/m1..m4 frames and sheets; timelines in patterns.md §1-§11).
// Ticks are game ticks (20/s); the rel ticks of patterns.md map 1:1 onto clip ticks.
//
// Clip: {name, len, loop?, next?, blend?, keys: [[tick, pose, ease?], ...], events, note}
//   keys are sparse; each merges onto the previous accumulated pose (DEFAULT_POSE first).
//   ease of the segment arriving at a key: 'io' smooth (default), 'i' accelerate into the key
//   (strikes, falls), 'o' decelerate (leaps, settles), 'l' linear (spins, twirls).
//   events: ticks the pattern code schedules hits, hazards, props and sounds on.
//   blend: the first key segment lasts at least this many ticks (default 3) so a clip started
//   from any pose eases in.
// Pose channels: guardian_pose.mjs. Body space: +X her left, +Y up, -Z forward, blocks. pos is
// the offset from the anchor (the boss body): pattern code moves the body for horizontal
// travel, the clip carries heights, leans, limbs and the spear.
import {sp, unit, basisQ, cross, sub, times, dot, rot, q, slerp as qSlerp, lerp as vLerp} from './guardian_rig_math.mjs';

const H = .35;                                       // idle hover (feet above the floor)
// Free hand frame: fingers along f, the claw curling toward c (palm side).
export function hand(f, c) {
  const Y = times(unit(f), -1), C = sub(c, times(Y, dot(c, Y))), Z = times(unit(C), -1);
  return basisQ(cross(Y, Z), Y, Z);
}
const FWD = [0, 0, -1];
// Spear directions (tip) used by several clips; face = blade-plane normal shown to the camera.
// Idle (m1 f0 / f640, m4 f469): the corrupted arm reaches out and down to her right, nearly
// straight, so it reads as a limb from the front; the claw holds the shaft at the crescent
// (the hand slides 0.8 b up the shaft), the tip points to her right-front-down, the shaft
// passes over the right shoulder and behind the halo, and the butt star ends at the halo's
// upper edge on her LEFT.
const S_IDLE = sp([-.74, -.57, -.35], [.08, .05, -1]);
const IDLE_GRIP = [-1.2, 2.05, -.3], IDLE_SAT = .8;
const S_UP = sp([-.05, 1, .05], FWD), S_DOWN = sp([0, -1, .02], FWD);
const S_RIGHT = sp([-1, .04, -.15], FWD);             // level, tip to her right
const S_FWD = sp([-.15, -.02, -1], [0, -1, 0]);       // level, tip forward, blade plane horizontal
const S_BEHIND = sp([1, .06, .12], FWD);              // level behind the shoulders, tip to her left
// Free-hand frames at rest: the right claw hanging (when free), the left claw open and relaxed.
const RQ_REST = hand([0, -1, -.2], [.3, 0, -1]), LQ_REST = hand([.05, -1, -.1], [-.6, 0, -.6]);
// The vertical-blade spin: the blade plane follows the tip round (normal = tip x up).
const spinSp = tip => sp(tip, cross(unit(tip), [0, 1, 0]));
// A free-hand frame halfway between the rest claw and a measured grip frame: grabs and releases
// that would turn the hand about 180 degrees in one blend go through it in two halves.
const halfTo = (rest, f, c) => qSlerp(rest, hand(f, c), .5);
export const DEFAULT_POSE = {
  pos: [0, H, 0], rot: [0, 0, 0], pelvis: [0, 0, 0], skirtF: [0, 0, 0], skirtO: [0, 0, 0], tail: [0, 0, 0],
  legR: [3, 0, -3], legL: [1, 0, 3], torso: [-3, 0, 0], head: [-6, 0, 0],
  grip: IDLE_GRIP, spear: S_IDLE, sAt: 0, spearS: 1,
  rFree: 0, rw: [-.6, 1.6, -.4], rq: RQ_REST, rPole: [-.6, -.5, .5], rPalm: [0, 0, 0],
  lOn: 0, lAt: .6, lw: [.48, 1.62, -.1], lq: LQ_REST, lPole: [.7, -.4, .4],
  bracket: [0, 0, 0], shield: [0, 0, 0], wing: [0, 0, 0], wc: 0, ws: 0, wp: 0,
  halo: 1, glow: 1, fx: .55, trail: 0, vis: 1, bodyVis: 1, cubes: 1,
  rHand: 'fist', lHand: 'open',
};
const k = (t, pose = {}, e) => [t, pose, e];
const IDLE = {pos: [0, H, 0], rot: [0, 0, 0], torso: [-3, 0, 0], head: [-6, 0, 0], grip: IDLE_GRIP, spear: S_IDLE, sAt: IDLE_SAT, spearS: 1,
  rFree: 0, lOn: 0, lw: [.48, 1.62, -.1], rq: RQ_REST, lq: LQ_REST, wing: [0, 0, 0], wc: 0, ws: 0, wp: 0, bracket: [0, 0, 0], shield: [0, 0, 0],
  skirtF: [0, 0, 0], skirtO: [0, 0, 0], tail: [0, 0, 0], legR: [3, 0, -3], legL: [1, 0, 3], fx: .55, trail: 0, halo: 1, glow: 1,
  rHand: 'fist', lHand: 'open', pelvis: [0, 0, 0], vis: 1, bodyVis: 1};
// Poses shared by several clips.
const WING_UP = {wing: [0, 0, 72], wc: 10, ws: 14, wp: 22};                 // wind-ups: the fan swings up
const WING_GUARD = {wing: [0, 0, 38], wc: 24, ws: 38, wp: 52, bracket: [0, 0, 12]};
const WING_WIDE = {wing: [0, 0, 55], wc: 30, ws: 52, wp: 74};
const WING_BACK = {wing: [-10, -48, 22], wc: -6, ws: 8, wp: 18};            // flight: swept back
const WING_DROOP = {wing: [0, 0, -16], wc: -10, ws: -14, wp: -10};
const TRAIL_LEGS = {legR: [-28, 0, -5], legL: [-22, 0, 5], skirtF: [-16, 0, 0], skirtO: [-10, 0, 0], tail: [-14, 0, 6]};
const GUARD = {grip: [-.62, 2.22, -.5], spear: sp([-.62, .62, -.45], [.4, .2, -1]), sAt: 0, lw: [.6, 1.95, -.35], lq: hand([.3, -1, -.4], [-.5, 0, -.8]),
  torso: [-2, -8, 0], head: [-4, 6, 0], ...WING_GUARD, fx: 1.0};
const HOVER = {grip: [-.58, 2.98, .22], spear: S_BEHIND, sAt: -.1, lOn: 1, lAt: 1.15, torso: [6, 0, 0], head: [-2, 0, 0], ...WING_WIDE,
  legR: [-6, 0, -4], legL: [-4, 0, 4], fx: .9};
const PLANTED = {grip: [-.62, 1.95, -.32], spear: sp([.02, -1, -.04], FWD), sAt: 0};
// A baton twirl: the spear spins about its middle (the hand slides there, sAt) in a plane given
// by its normal, `turns` full turns from t0 to t1, keys every quarter turn (90 deg per key).
function twirl(t0, t1, grip, normal = FWD, turns = 1, from = [0, 1, 0]) {
  const keys = [], n = Math.round(turns * 4), N = unit(normal);
  for (let i = 0; i <= n; i++) {
    const a = i * Math.PI / 2, Q = qAxis(N, a), tip = rot(Q, unit(from));
    keys.push(k(Math.round(t0 + (t1 - t0) * i / n), {grip, sAt: .88, spear: sp(tip, N)}, 'l'));
  }
  return keys;
}
function qAxis(axis, a) { const s = Math.sin(a / 2); return [axis[0] * s, axis[1] * s, axis[2] * s, Math.cos(a / 2)]; }

export const CLIPS = [
  // ---- idle and movement (patterns.md §1) ---------------------------------------------------
  // The legs dangle out of step: the right leg leads the swing (peak t10), the left one lags a
  // quarter cycle (peak t20-30) with its own roll, so the voxel stacks never move in lockstep.
  {name: 'idle', len: 40, loop: true, note: 'hover bob +0.05 b at t20; wing tiers breathe; skirt and tail sway; legs swing out of step; cubes drift', keys: [
    k(0, {...IDLE}),
    k(10, {skirtF: [2, 0, 0], tail: [0, 0, 3], wp: 2, ws: 1, legR: [5, 0, -3.4], legL: [1.4, 0, 2.4]}),
    k(20, {pos: [0, H + .05, 0], torso: [-2, 0, 0], head: [-5, 0, 0], grip: [-1.2, 2.09, -.3], wc: 2, wp: 4, ws: 2.5, skirtF: [0, 0, 0], skirtO: [1.5, 0, 0], tail: [0, 0, -2], legR: [3.6, 0, -2.8], legL: [3, 0, 3.2], lw: [.48, 1.66, -.1]}),
    k(30, {skirtF: [-1.5, 0, 0], tail: [0, 0, 2], wp: 2, ws: 1, legR: [2.4, 0, -2.6], legL: [2.6, 0, 3.8]}),
    k(40, {pos: [0, H, 0], torso: [-3, 0, 0], head: [-6, 0, 0], grip: IDLE_GRIP, wc: 0, wp: 0, ws: 0, skirtF: [0, 0, 0], skirtO: [0, 0, 0], tail: [0, 0, 0], legR: [3, 0, -3], legL: [1, 0, 3], lw: [.48, 1.62, -.1]}),
  ]},
  {name: 'glide', len: 24, loop: true, blend: 5, note: 'moving pose (approach, guard drift, reposition): leaning into the travel, spear level toward the target, wing swept back', keys: [
    k(0, {rot: [-14, 0, 0], grip: [-.72, 1.95, -.45], spear: sp([-.3, -.08, -1], [0, -1, 0]), ...WING_BACK, ...TRAIL_LEGS, fx: .7}),
    k(12, {pos: [0, H + .06, 0], wp: 24, ws: 12, tail: [-18, 0, 3]}),
    k(24, {pos: [0, H, 0], wp: 18, ws: 8, tail: [-14, 0, 6]}),
  ]},
  // ---- P1 공간 찌르기: two thrusts (§3, m1 0.00-4.73 s) ------------------------------------------
  {name: 'thrust', len: 91, next: 'idle', events: {glow: 4, glint: 19, hit1: 28, rise: 38, dive: 54, hit2: 58, land: 65, flourish: 72},
    note: 'body travel by the pattern code: lunge 2-3 b forward at 27-28; fly back 4-6 b at 38-54; dash 5-6 b at 57-58', keys: [
      k(0, {sAt: IDLE_SAT}),
      k(4, {sAt: 0, torso: [-2, 24, 0], head: [-4, -14, 0], grip: [-.86, 2.3, .02], spear: sp([-.96, .03, -.28], FWD), ...WING_UP, fx: .9}),
      k(16, {grip: [-.82, 2.33, .12], fx: 1.35, wp: 28}),
      k(21, {pos: [0, H + .1, .05]}),
      k(26, {pos: [0, .8, .32], torso: [8, 16, 0], grip: [-.55, 2.36, .18], spear: sp([-.15, -.45, -.88], [-.4, 0, -1]), fx: 1.5, wing: [0, 0, 52], wp: 18}),
      k(27, {grip: [-.72, 2.2, -.3], trail: 1}, 'l'),
      k(28, {pos: [0, .42, -.7], rot: [-12, 0, 0], torso: [-18, -12, 0], head: [-8, 6, 0], grip: [-.28, 1.95, -.98], spear: sp([-.05, -.33, -.94], [-.3, 0, -1]),
        trail: 1, wing: [0, -22, 28], wp: 10, ...TRAIL_LEGS}, 'l'),
      k(32, {trail: 0}),
      k(38, {pos: [0, 1.25, -.3], rot: [0, 0, 0], torso: [-4, 0, 0], head: [-14, 0, 0], grip: [-.6, 2.1, -.5], spear: sp([-.3, -.86, -.4], FWD), wing: [0, 0, 34], wp: 20, fx: .9,
        legR: [3, 0, -3], legL: [1, 0, 3], skirtF: [0, 0, 0], skirtO: [0, 0, 0], tail: [0, 0, 0]}),
      k(54, {pos: [0, 2.8, 0], rot: [-18, 0, 0], grip: [-.45, 2.15, -.62], spear: sp([0, -.72, -.7], FWD), ...WING_BACK, ...TRAIL_LEGS, fx: 1.2}),
      k(57, {pos: [0, 2.35, -.3], rot: [-46, 0, 0], grip: [-.34, 2.02, -.82], spear: sp([0, -.12, -1], [0, -1, 0]), fx: 1.5}),
      k(58, {pos: [0, .55, -1.0], rot: [-38, 0, 0], trail: 1}, 'i'),
      k(62, {trail: 0}),
      k(65, {pos: [0, .22, -.6], rot: [-5, 0, 0], torso: [-12, 0, 0], grip: [-.64, 1.5, -.55], spear: sp([-.45, -.85, -.25], FWD), ...WING_DROOP, fx: .8,
        legR: [8, 0, -3], legL: [6, 0, 3], skirtF: [4, 0, 0], skirtO: [0, 0, 0], tail: [0, 0, 0]}),
      k(72, {pos: [0, H, -.4], rot: [0, 0, 0], torso: [-2, 0, 0], grip: [-.5, 2.6, -.42], spear: sp([-.3, .95, 0], FWD), wing: [0, 0, 12], wc: 0, ws: 4, wp: 8, fx: 1.1}),
      ...twirl(73, 85, [-.42, 2.45, -.6], FWD, 1, [-.3, .95, 0]).slice(1),
      k(91, {...IDLE}),
    ]},
  // ---- P2 공간 투창: javelin (§4, m1 5.30-9.47 s) -------------------------------------------
  {name: 'javelin', len: 76, next: 'idle', events: {spin: 0, vanish: 10, glyph: 11, beam: 28, rematerialise: 31, release: 35, launch: 36, return: 58, catch: 63},
    note: 'the rig spear is hidden from 10 to 31 and from 36 to 63; the flying spear is a prop (rig/prop/spear) moved by the pattern code', keys: [
      k(0, {sAt: IDLE_SAT}),
      k(5, {grip: [-.42, 2.2, -.65], sAt: .88, spear: spinSp([-1, .02, -.1]), rPalm: [0, -1, 0], wing: [0, 0, 30], wp: 16, torso: [-2, 10, 0]}),
      // one full horizontal turn round her (about 100 degrees per tick, the blade upright):
      // right, front, left, back, then swept on round and down to her right-front
      k(6, {spear: spinSp([.28, .02, -.96])}, 'l'),
      k(7, {spear: spinSp([.9, .02, .44]), torso: [-2, -6, 0]}, 'l'),
      k(8, {spear: spinSp([-.59, .02, .81])}, 'l'),
      k(9, {spear: spinSp([-.6, -.55, -.55]), grip: [-.62, 1.95, -.6], sAt: 0, rPalm: [0, 0, 0], torso: [-6, 14, 0], wing: [0, 0, 8], trail: 1}, 'l'),
      k(10, {spearS: 0, trail: 0, rFree: 1, rw: [-.75, 1.9, -.55], rq: hand([-.3, -.6, -1], [0, -1, 0]), rHand: 'open'}, 'l'),
      k(16, {rw: [-.72, 2.32, -.62], rq: hand([-.2, .3, -1], [0, 0, -1]), torso: [-2, 12, 0], head: [-4, -8, 0], lw: [.55, 1.85, -.35], wing: [0, 0, 20], wp: 10}),
      k(24, {rw: [-.68, 2.42, -.66]}),
      k(31, {rFree: 0, rHand: 'fist', grip: [-.56, 2.86, .42], spear: sp([.05, .14, -1], [-1, 0, 0]), spearS: .05, torso: [10, 26, 0], head: [-6, -16, 0], ...WING_UP, fx: 1.4}),
      k(33, {spearS: 1}),
      k(34, {grip: [-.74, 2.72, -.2]}, 'l'),
      k(35, {grip: [-.26, 2.5, -.86], torso: [-12, -14, 0], head: [-6, 6, 0], wing: [0, -12, 40], fx: 1.6, trail: 1}, 'l'),
      k(36, {spearS: 0, rFree: 1, rw: [-.26, 2.42, -.9], rq: hand([-.55, .35, -.75], [.35, .9, -.25]), rHand: 'open', trail: 0}, 'l'),
      k(45, {rw: [-.62, 1.82, -.48], rq: hand([0, -1, -.2], [.3, 0, -1]), torso: [-3, 0, 0], head: [-6, 0, 0], wing: [0, 0, 6], wc: 0, ws: 0, wp: 2, fx: .55}),
      k(58, {rw: [-.36, 2.95, -.25], rq: hand([-.5, .25, -.82], [-.82, 0, .55])}),
      k(62, {spearS: 0}),
      k(63, {spearS: 1, rFree: 0, rHand: 'fist', grip: [-.3, 3.0, -.22], spear: S_UP, sAt: 0, torso: [4, 0, 0]}, 'l'),
      k(68, {grip: [-.62, 2.4, -.5], spear: sp([-.62, -.3, -.7], FWD), torso: [-3, 0, 0]}),
      k(76, {...IDLE}),
    ]},
  // ---- P3 공간을 집행하는 시련: melee slam (§5, m1 9.85-14.50 s) -------------------------------------
  {name: 'slam', len: 70, next: 'idle', events: {raise: 0, ring: 9, glint: 12, down: 22, impact: 26, pull: 48, twirl: 54},
    note: 'disc r 5 centred 3.5 b in front; the spear stays planted (rig part) 26-48, so the body must not move then', keys: [
      k(0, {sAt: IDLE_SAT}),
      k(4, {sAt: 0, grip: [-.72, 2.32, -.42], spear: S_RIGHT, torso: [-2, 12, 0], wing: [0, 0, 20], wp: 10, lw: [.42, 2.15, -.7]}),
      k(7, {grip: [-.12, 3.02, .1], spear: sp([-.1, .95, -.3], FWD), lOn: 1, lAt: -.45, torso: [14, 0, 0], head: [4, 0, 0], ...WING_UP, fx: 1.0}),
      k(12, {pos: [0, .5, 0], grip: [-.1, 3.08, .0], spear: sp([-.05, 1, -.1], FWD), fx: 1.5}),
      k(21, {pos: [0, .55, .05], torso: [18, 0, 0]}),
      k(23, {grip: [-.1, 2.8, -.4], spear: sp([0, .45, -.9], [0, -1, 0]), torso: [4, 0, 0], trail: 1}, 'i'),
      k(26, {pos: [0, .15, 0], grip: [-.1, 1.9, -.8], spear: sp([.03, -.71, -.71], [0, -.7, .7]), torso: [-25, 0, 0], head: [-15, 0, 0], lAt: -.35, wing: [0, 0, 22], wp: 6, ws: 2, wc: 0,
        skirtF: [6, 0, 0], legR: [10, 0, -3], legL: [8, 0, 3]}, 'i'),
      k(30, {trail: 0, fx: 1.2}),
      k(40, {pos: [0, .2, .02], torso: [-20, 0, 0], head: [-12, 0, 0]}),
      k(48, {pos: [0, .18, 0], torso: [-22, 0, 0]}),
      k(54, {pos: [0, H, 0], grip: [-.5, 2.5, -.5], spear: sp([-.3, .62, -.72], FWD), lOn: 0, torso: [0, 0, 0], head: [-6, 0, 0], wing: [0, 0, 8], fx: .9, skirtF: [0, 0, 0], legR: [3, 0, -3], legL: [1, 0, 3]}),
      ...twirl(55, 64, [-.45, 2.4, -.62], FWD, 1, [-.3, .62, -.72]).slice(1),
      k(70, {...IDLE}),
    ]},
  // ---- P4 어둠 속에서 퍼지는 공간: pull + two 360° swings (§6, m1 14.73-17.50, 22.50-25.05 s) --------
  {name: 'pull', len: 40, next: 'idle', events: {aura: 0, cage: 11, relocate: 32},
    note: 'the corrupted claw casts (the left hand takes the shaft); the player is relocated at 32; follow with swing after 10-14 t (K15)', keys: [
      k(0, {sAt: IDLE_SAT}),
      k(6, {sAt: 0, lOn: 1, lAt: -.25, grip: [-.15, 1.88, -.55], spear: sp([-.66, -.62, -.42], FWD)}),
      k(9, {rFree: 1, rHand: 'open', rw: [-.36, 2.56, -.78], rq: hand([0, 1, -.25], FWD), grip: [.05, 1.9, -.52], spear: sp([-.66, -.62, -.42], FWD), lAt: -.3,
        torso: [-4, -10, 0], head: [-4, 8, 0], wing: [0, 0, 18], wp: 12}),
      k(20, {rw: [-.3, 2.62, -.96], rq: hand([0, .9, -.6], FWD), torso: [-8, -14, 0]}),
      k(28, {rw: [-.46, 2.46, -.58], rq: hand([.2, .6, .4], [.3, .2, 1]), torso: [6, 6, 0], head: [2, 0, 0], wing: [0, 0, 26], wp: 18}, 'i'),
      k(32, {rw: [-.5, 2.4, -.5], lq: halfTo(LQ_REST, [.65, -.19, -.74], [.38, -.76, .53])}),
      k(36, {rq: hand([-.61, .77, .17], [.14, .32, -.94])}),
      k(40, {...IDLE, lq: halfTo(LQ_REST, [.65, -.19, -.74], [.38, -.76, .53])}),
    ]},
  {name: 'swing', len: 51, next: 'idle', events: {windup: 0, swing1: 20, swing1_end: 24, swing2: 33, swing2_end: 39},
    note: 'two full 360 degree spins with the spear level at waist height: forehand (left to right) 20-24, backhand 33-39 rising low-right to high-left', keys: [
      k(0, {sAt: IDLE_SAT}),
      k(5, {sAt: 0, grip: [-.52, 2.72, .36], spear: S_BEHIND, lOn: 1, lAt: .62, lq: hand([-.13, .58, .8], [-.02, -.81, .59]), torso: [6, 22, 0], head: [-4, -10, 0], ...WING_UP, wp: 30, fx: 1.2}),
      // the left hand lets go during the hold and drops out to her left side; the forehand is
      // one-handed
      k(12, {lOn: 1}),
      k(17, {grip: [-.5, 2.76, .4], torso: [8, 26, 0], fx: 1.5, lOn: 0, lw: [.72, 2.0, .2]}),
      k(18, {grip: [-.6, 2.5, .1], spear: sp([.64, 0, -.77], [0, -.5, -.87]), torso: [4, 16, 0], trail: 1}, 'l'),
      k(19, {grip: [-.72, 2.15, -.2], spear: sp([-.17, 0, -.98], [0, -.87, -.5]), torso: [-2, 4, 0]}, 'l'),
      k(20, {rot: [0, 0, 0], grip: [-.78, 1.92, -.42], spear: sp([-.86, -.02, -.5], [0, -1, 0]), lw: [.55, 1.75, -.05], torso: [-8, -8, 0], head: [-6, 0, 0], wing: [0, -10, 40], wp: 20, trail: 1}, 'l'),
      k(21, {rot: [0, 72, 0]}, 'l'), k(22, {rot: [0, 144, 0]}, 'l'), k(23, {rot: [0, 216, 0]}, 'l'), k(24, {rot: [0, 288, 0]}, 'l'),
      k(25, {rot: [0, 360, 0], trail: 0}, 'o'),
      k(29, {grip: [-.8, 1.95, -.2], spear: sp([-.9, -.25, .2], [0, -1, 0]), torso: [-4, 10, 0], wing: [0, 0, 30], lq: LQ_REST}),
      k(33, {grip: [-.82, 1.75, -.35], spear: sp([-.8, -.42, -.42], [0, -1, 0]), trail: 1}, 'i'),
      k(34, {rot: [0, 300, 0]}, 'l'), k(35, {rot: [0, 240, 0]}, 'l'), k(36, {rot: [0, 180, 0], spear: sp([-.86, -.05, -.5], [0, -1, 0]), grip: [-.8, 2.05, -.4]}, 'l'),
      k(37, {rot: [0, 120, 0]}, 'l'), k(38, {rot: [0, 60, 0]}, 'l'),
      k(39, {rot: [0, 0, 0], grip: [-.7, 2.5, -.45], spear: sp([-.62, .5, -.6], [0, -1, 0]), trail: 0}, 'l'),
      k(44, {grip: [-.5, 2.6, -.42], spear: S_UP, fx: .9}),
      k(51, {...IDLE}),
    ]},
  // ---- P5 하늘을 심판하는 자: fly-slam (§7, m1 26.45-31.52 s) ----------------------------------------
  {name: 'flyslam', len: 101, next: 'idle', events: {raise: 0, glint: 6, beam: 16, takeoff: 19, ring: 21, gone: 23, dive: 39, impact: 41, spikes: 47, pull: 71, twirl: 79},
    note: 'rises to +8 b at 19-23 and stays up; move the body under the locked ring during 23-39; dives at 39-41; the spear stays planted 41-71', keys: [
      k(0, {sAt: IDLE_SAT}),
      k(4, {sAt: 0, grip: [-.62, 2.3, -.45], spear: sp([-.6, .45, -.65], FWD), fx: 1.3}),
      k(6, {grip: [-.5, 2.32, -.5], spear: S_UP, torso: [0, 0, 0], head: [-2, 0, 0], fx: 1.6, wing: [0, 0, 18], wp: 10}),
      k(12, {grip: [-.48, 2.36, -.48], fx: 1.3}),
      k(16, {fx: 2.0, wing: [0, 0, 40], wp: 30, ws: 14}),
      k(19, {pos: [0, .18, 0], torso: [-10, 0, 0], legR: [20, 0, -4], legL: [18, 0, 4]}, 'o'),
      k(23, {pos: [0, 8.0, 0], torso: [6, 0, 0], ...WING_WIDE, legR: [-10, 0, -4], legL: [-8, 0, 4], skirtF: [-10, 0, 0], tail: [-12, 0, 0]}, 'i'),
      k(36, {pos: [0, 8.1, 0], lq: hand([-.84, 0, -.54], [.54, 0, -.84])}),
      k(38, {grip: [-.2, 2.7, -.35], spear: S_DOWN, lOn: 1, lAt: .35, torso: [-6, 0, 0], head: [-14, 0, 0], ...WING_BACK, legR: [-4, 0, -3], legL: [-3, 0, 3]}),
      k(39, {pos: [0, 7.6, 0]}, 'l'),
      k(41, {pos: [0, .16, 0], grip: [-.25, 2.36, -.42], torso: [-18, 0, 0], ...WING_WIDE, skirtF: [6, 0, 0], tail: [6, 0, 0], legR: [12, 0, -3], legL: [10, 0, 3]}, 'i'),
      k(47, {pos: [0, .12, 0], torso: [-14, 0, 0], wing: [0, 0, 20], wc: 8, ws: 14, wp: 20, skirtF: [0, 0, 0], tail: [0, 0, 0]}),
      k(71, {pos: [0, .14, 0], torso: [-12, 0, 0]}),
      k(79, {pos: [0, H, 0], grip: [-.5, 2.62, -.45], spear: sp([-.3, .9, -.2], FWD), lOn: 0, torso: [-2, 0, 0], head: [-6, 0, 0], wing: [0, 0, 6], wc: 0, ws: 2, wp: 4, legR: [3, 0, -3], legL: [1, 0, 3]}),
      ...twirl(80, 92, [-.45, 2.45, -.6], FWD, 1, [-.3, .9, -.2]).slice(1),
      k(101, {...IDLE}),
    ]},
  // ---- P6 파수 모드: guard entry, hold, sweeps (§8, m2) --------------------------------------------
  {name: 'guard_entry', len: 50, next: 'guard', events: {twirl: 0, discs: 16, ring: 35, settle: 44, guard: 50},
    note: 'baton twirl in front (0-16), vertical spin discs to her right and front (16-35), ground ring (35-44), settle into the guard pose', keys: [
      k(0, {sAt: IDLE_SAT}),
      k(3, {grip: [-.45, 2.5, -.55], sAt: .88, spear: sp([-1, .05, 0], FWD), torso: [-2, 6, 0]}),
      ...twirl(4, 16, [-.32, 2.35, -.62], FWD, 1.5, [-1, .05, 0]).slice(1),
      // spin discs: the spear wheels in a vertical plane at her right side, then in front
      ...twirl(18, 26, [-.95, 2.1, -.25], [1, 0, 0], 1, [0, 1, -.1]).map(([t, p, e]) => [t, {...p, torso: [-4, 24, 0], wing: [0, 0, 26], wp: 18}, e]),
      ...twirl(27, 35, [-.25, 2.1, -.82], FWD, 1, [0, 1, 0]).map(([t, p, e]) => [t, {...p, torso: [-6, -4, 0]}, e]),
      k(40, {grip: [-.66, 1.5, -.48], sAt: 0, spear: sp([-.7, -.7, -.15], FWD), pos: [0, .28, 0], torso: [-10, 0, 0], wing: [0, 0, 20], wp: 20}),
      k(50, {...GUARD, pos: [0, H, 0]}),
    ]},
  {name: 'guard', len: 40, loop: true, note: 'guard mode hold (100 t in the pattern): spear diagonal up-right, wing raised and opened, slight bob', keys: [
    k(0, {...GUARD}),
    k(20, {pos: [0, H + .06, 0], grip: [-.62, 2.26, -.5], wp: 56, ws: 41, wc: 26, head: [-2, 6, 0]}),
    k(40, {pos: [0, H, 0], grip: [-.62, 2.22, -.5], wp: 52, ws: 38, wc: 24, head: [-4, 6, 0]}),
  ]},
  {name: 'sweep', len: 44, next: 'idle', events: {windup: 0, active: 19, active_end: 24},
    note: 'gold sweep: 19 t wind-up (spear cocked behind her right shoulder, tip toward her left), 180-210 degree front arc from her left to her right, active 19-24', keys: [
      k(0, {...GUARD}),
      k(8, {grip: [-.4, 3.0, .05], spear: sp([.2, .95, .2], FWD), torso: [4, 10, 0], ...WING_UP, fx: 1.3}),
      k(19, {grip: [-.52, 2.75, .32], spear: sp([.86, .14, .48], [0, -1, 0]), torso: [6, 34, 0], head: [-6, -18, 0], fx: 1.6, wing: [0, 0, 62], wp: 28}),
      k(20, {grip: [-.68, 2.48, -.22], spear: sp([.9, .02, -.42], [0, -1, 0]), torso: [-2, 20, 0]}, 'l'),
      k(21, {grip: [-.12, 2.05, -.78], spear: sp([.62, -.06, -.78], [0, -1, 0]), torso: [-10, 8, 0], head: [-6, 0, 0], trail: 1}, 'l'),
      k(23, {grip: [-.6, 2.0, -.7], spear: sp([-.62, -.06, -.78], [0, -1, 0]), torso: [-10, -22, 0], wing: [0, -8, 40]}, 'l'),
      k(24, {grip: [-.86, 2.02, -.32], spear: sp([-.97, -.04, .2], [0, -1, 0]), torso: [-8, -30, 0]}, 'o'),
      k(28, {trail: 0}),
      k(34, {grip: [-.8, 2.1, -.4], spear: sp([-1, 0, -.1], FWD), torso: [-4, -12, 0], head: [-6, 0, 0], wing: [0, 0, 16], wc: 6, ws: 10, wp: 12, fx: .8}),
      k(44, {...IDLE}),
    ]},
  {name: 'sweep_e', len: 50, next: 'idle', events: {enchant: 0, windup: 7, active: 19, active_end: 27},
    note: 'enchanted sweep (call rig/spear/<element> first): enchant line 0-6, wind-up raised high to her left 7-19, active 19-27', keys: [
      k(0, {...GUARD}),
      k(6, {grip: [-.5, 2.35, -.62], spear: sp([-1, .02, -.05], FWD), torso: [0, 0, 0], fx: 2.0}),
      k(19, {grip: [-.06, 2.98, .12], spear: sp([.75, .5, .45], [0, -1, 0]), lOn: 0, torso: [6, 30, 0], head: [-4, -16, 0], ...WING_UP, fx: 2.0}),
      k(22, {grip: [-.14, 2.05, -.8], spear: sp([.55, -.08, -.83], [0, -1, 0]), torso: [-10, 8, 0], head: [-6, 0, 0], trail: 1}, 'i'),
      k(25, {grip: [-.62, 2.0, -.68], spear: sp([-.62, -.08, -.78], [0, -1, 0]), torso: [-10, -24, 0], wing: [0, -8, 40]}, 'l'),
      k(27, {grip: [-.86, 2.0, -.3], spear: sp([-.97, -.06, .2], [0, -1, 0]), torso: [-8, -32, 0]}, 'o'),
      k(31, {trail: 0}),
      k(40, {grip: [-.8, 2.1, -.4], spear: sp([-1, 0, -.1], FWD), torso: [-4, -12, 0], head: [-6, 0, 0], wing: [0, 0, 16], wc: 6, ws: 10, wp: 12, fx: 1.0}),
      k(50, {...IDLE}),
    ]},
  // ---- P7 혼돈: chaos entry, hover, fail, fall (§9, m2 / m3 / m4) -----------------------------------
  {name: 'chaos_leap', len: 32, next: 'chaos_charge', events: {leap: 0, land: 32},
    note: 'leap 0-9, arcing flight 9-31 (move the body to the arena centre meanwhile), landing 32', keys: [
      k(0, {sAt: IDLE_SAT}),
      k(9, {sAt: 0, pos: [0, 3.0, 0], grip: [-.48, 2.35, -.5], spear: S_UP, ...WING_WIDE, legR: [-6, 0, -4], legL: [-4, 0, 4], fx: 1.0}, 'io'),
      k(14, {pos: [0, 3.6, 0], rot: [-26, 0, 0], grip: [-.7, 1.95, -.2], spear: sp([-.4, -.15, -.9], [0, -1, 0]), ...WING_BACK, ...TRAIL_LEGS}),
      k(28, {pos: [0, 1.4, 0], rot: [-22, 0, 0]}),
      k(32, {pos: [0, .22, 0], rot: [0, 0, 0], torso: [-14, 0, 0], ...WING_WIDE, legR: [14, 0, -3], legL: [12, 0, 3], skirtF: [6, 0, 0], skirtO: [0, 0, 0], tail: [4, 0, 0]}, 'i'),
    ]},
  {name: 'chaos_charge', len: 36, next: 'chaos_hover', events: {charge: 0, flare: 7, rise: 30, hover: 36},
    note: 'charge on the centre with the spear level (30 t), then the rise to the chaos hover (feet 3 b up)', keys: [
      k(0, {pos: [0, .22, 0], torso: [-10, 0, 0], grip: [-.72, 2.15, -.45], spear: sp([-.95, .02, -.3], FWD), ...WING_WIDE, legR: [6, 0, -3], legL: [4, 0, 3]}),
      k(7, {pos: [0, .26, 0], torso: [-6, 0, 0], fx: 1.6}),
      k(30, {pos: [0, .3, 0], grip: [-.72, 2.2, -.45], fx: 1.8, halo: 1.15, glow: 1.6}),
      k(36, {pos: [0, 3.0, 0], ...HOVER, halo: 1, glow: 1.4}, 'o'),
    ]},
  {name: 'chaos_hover', len: 40, loop: true, note: 'chaos hold (350 t timer): arms up, spear horizontal behind the shoulders, wing spread, slow bob', keys: [
    k(0, {pos: [0, 3.0, 0], ...HOVER, glow: 1.4}),
    k(20, {pos: [0, 3.08, 0], grip: [-.58, 3.0, .22], wp: 78, ws: 55, head: [0, 0, 0]}),
    k(40, {pos: [0, 3.0, 0], grip: [-.58, 2.98, .22], wp: 74, ws: 52, head: [-2, 0, 0]}),
  ]},
  {name: 'chaos_fail', len: 40, events: {twist: 10, rise: 21, high: 25},
    note: 'timeout (tick 0 = timer full): twist with the wing swept across the front (10-14), rise 0.5-0.7 BH (21-25) and hold; play chaos_land at tick 33 (lands at +55, between fail spear 1 at +49 and spear 2 at +80)', keys: [
    k(0, {pos: [0, 3.0, 0], ...HOVER}),
    k(10, {torso: [-6, -26, 0], wing: [0, 52, 30], wc: 10, ws: 20, wp: 30}),
    k(14, {torso: [-8, -42, 0], wing: [0, 70, 20]}, 'i'),
    k(21, {torso: [0, 0, 0], ...WING_WIDE}),
    k(25, {pos: [0, 4.8, 0], ...HOVER}, 'o'),
    k(40, {pos: [0, 4.85, 0]}),
  ]},
  {name: 'chaos_land', len: 26, events: {land: 22},
    note: 'fail: descends from the chaos height to stand on the floor at the centre, the spear still held across the shoulders (patterns.md §9.4); holds the stance. Then chaos_raise for a second fail spear, or idle / glide when the spears are done', keys: [
      k(0, {pos: [0, 4.8, 0], ...HOVER}),
      k(8, {wing: [0, 0, 30], wc: 10, ws: 20, wp: 30, torso: [2, 0, 0]}),
      k(22, {pos: [0, .12, 0], torso: [-8, 0, 0], legR: [10, 0, -3], legL: [8, 0, 3]}, 'io'),
      k(26, {pos: [0, .14, 0], torso: [-4, 0, 0], legR: [4, 0, -3], legL: [3, 0, 3], wing: [0, 0, 22], wc: 8, ws: 14, wp: 22}),
    ]},
  {name: 'chaos_fall', len: 20, next: 'groggy_a', events: {hang: 0, fall: 6, land: 18},
    note: 'second star broken: hangs 6 t, falls about 1 BH and lands on the floor (no impact), then groggy', keys: [
      k(0, {pos: [0, 3.0, 0], ...HOVER}),
      k(6, {pos: [0, 3.05, 0], torso: [-14, 0, 6], head: [-18, 0, 0], ...WING_DROOP, wp: 10, lOn: 0, lw: [.75, 2.2, .15]}),
      // the spear arm comes down round her right side (not past the shoulder)
      k(12, {pos: [0, 2.2, 0], grip: [-.95, 2.45, -.1], spear: sp([-.55, -.35, -.75], FWD), sAt: 0}, 'i'),
      k(18, {pos: [0, .05, 0], torso: [-20, 0, 6], head: [-24, 0, 0], grip: [-.66, 1.85, -.4], spear: sp([0, -1, -.1], FWD), lOn: 0, sAt: 0, ...WING_DROOP,
        legR: [14, 0, -4], legL: [10, 0, 4]}, 'i'),
      k(20, {...PLANTED, pos: [0, .05, 0]}),
    ]},
  // ---- groggy (§10, m3 16.75-27.1 s) ---------------------------------------------------------
  {name: 'groggy_a', len: 40, loop: true, note: 'pose A: slumped, the spear planted head-down at her right, wing drooped, halo blazing', keys: [
    k(0, {pos: [0, .05, 0], ...PLANTED, torso: [-14, 0, 6], head: [-22, 0, 4], ...WING_DROOP, halo: 1.3, glow: 1.7, fx: .4, legR: [6, 0, -4], legL: [4, 0, 4]}),
    k(20, {torso: [-16, 0, 6], head: [-24, 0, 4], glow: 1.85, wp: -12}),
    k(40, {torso: [-14, 0, 6], head: [-22, 0, 4], glow: 1.7, wp: -10}),
  ]},
  {name: 'groggy_b', len: 34, next: 'getup', events: {fold: 0, getup: 34},
    note: 'pose B: head bowed, torso folded forward, the shield swung in front of her body', keys: [
      k(0, {pos: [0, .05, 0], ...PLANTED, torso: [-14, 0, 6], head: [-22, 0, 4], ...WING_DROOP, halo: 1.3, glow: 2.0, fx: .4, legR: [6, 0, -4], legL: [4, 0, 4]}),
      k(10, {torso: [-38, 0, 2], head: [-30, 0, 0], bracket: [-10, 122, 0], shield: [0, -95, 20], wing: [0, 10, -8], halo: 1.1, glow: 1.4}),
      k(34, {torso: [-42, 0, 2], head: [-32, 0, 0]}),
    ]},
  {name: 'getup', len: 40, next: 'idle', events: {spread: 0, lift: 6, stance: 12},
    note: 'get-up: the wing sweeps out to its widest, she lifts into the hover and takes the spear forward', keys: [
      k(0, {pos: [0, .05, 0], ...PLANTED, torso: [-42, 0, 2], head: [-32, 0, 0], bracket: [-10, 122, 0], shield: [0, -95, 20], ...WING_DROOP, halo: 1.1, glow: 1.4}),
      k(8, {torso: [-6, 0, 0], head: [-8, 0, 0], bracket: [0, 0, 0], shield: [0, 0, 0], ...WING_WIDE, halo: 1, glow: 1.1}),
      k(12, {pos: [0, .5, 0], grip: [-.72, 2.0, -.6], spear: sp([-.4, -.62, -.68], FWD)}, 'o'),
      k(26, {wing: [0, 0, 14], wc: 4, ws: 8, wp: 12}),
      k(40, {...IDLE}),
    ]},
  // ---- entrance and death (§2, §11; not in the footage: PDF + K19 / K20) ---------------------
  {name: 'entrance', len: 60, next: 'idle', blend: 1, events: {fall: 0, impact: 14, appear: 14, grab: 26, pull: 34},
    note: 'the spear plunges from 7 b above to the floor at 14 (damage), she fades in beside it (14-24), grabs it at 26 and pulls it out (26-34)', keys: [
      k(0, {...IDLE, bodyVis: 0, grip: [-.62, 9.2, -.7], spear: sp([.02, -1, -.04], FWD), rFree: 1, rw: [-.6, 1.6, -.4], fx: 1.6}),
      k(10, {grip: [-.62, 8.6, -.7]}),
      k(14, {grip: [-.62, 2.05, -.7], fx: 2.0}, 'i'),
      k(15, {bodyVis: .05, pos: [0, .5, .15], torso: [-10, 0, 0], ...WING_WIDE}),
      k(24, {bodyVis: 1, rw: [-.62, 2.0, -.5], rq: hand([0, -.5, -1], [-1, 0, 0]), rHand: 'open', fx: 1.2}, 'o'),
      k(26, {rFree: 0, rHand: 'fist', pos: [0, .45, .1]}),
      k(34, {grip: [-.66, 2.62, -.62], pos: [0, H, .05], torso: [-2, 0, 0], wing: [0, 0, 20], wc: 6, ws: 12, wp: 18}),
      ...twirl(36, 48, [-.45, 2.45, -.62], FWD, 1, [.02, -1, -.04]).slice(1),
      k(60, {...IDLE}),
    ]},
  {name: 'death', len: 80, events: {slump: 0, takeoff: 22, gone: 76},
    note: 'death line, slump (0-20), then the fly-away: rises out of the arena and fades (22-76); call rig/kill after 80', keys: [
      k(0, {sAt: IDLE_SAT}),
      k(14, {sAt: 0, pos: [0, .18, 0], torso: [-26, 0, 8], head: [-26, 0, 6], grip: [-.66, 1.75, -.45], spear: sp([-.2, -.95, -.2], FWD), ...WING_DROOP, halo: 1.3, glow: 1.8, fx: .3,
        legR: [8, 0, -4], legL: [6, 0, 4]}),
      k(22, {pos: [0, .22, 0], torso: [-20, 0, 6]}),
      k(30, {pos: [0, 1.6, 0], torso: [6, 0, 0], head: [-4, 0, 0], grip: [-.5, 2.35, -.45], spear: S_UP, ...WING_WIDE, ...TRAIL_LEGS, glow: 1.4}, 'o'),
      k(56, {pos: [0, 9.0, 0], wing: [0, -20, 40], wp: 60}, 'i'),
      k(76, {pos: [0, 15.0, 0], vis: 0}, 'l'),
      k(80, {pos: [0, 15.0, 0], vis: 0}),
    ]},
  // ---- showcase: the pose of the official render (ref.png / guide.pdf p.2) --------------------
  {name: 'pose_ref', len: 20, loop: true, note: 'the official render pose (hand at mid-shaft, spear crossing the body); for screenshots and the entrance end pose', keys: [
    k(0, {grip: [-.85, 1.95, -.38], spear: sp([-.36, -.9, -.24], [.3, -.1, -1]), sAt: .62, torso: [-2, -6, 0], head: [-8, 4, 3], lw: [.52, 1.6, -.18],
      wing: [0, 0, 4], wp: 4, ws: 2}),
    k(20, {}),
  ]},
  // ---- added after the first release (ids stay stable): chaos fail, spear 2 -----------------
  {name: 'chaos_raise', len: 24, next: 'idle', events: {raise: 0, overhead: 6},
    note: 'fail spear 2: from the across-the-shoulders stance she raises the spear vertically overhead in the last 0.3 s before the drop (start 6 t before it), holds, then idle', keys: [
      k(0, {pos: [0, .14, 0], ...HOVER, torso: [-4, 0, 0], legR: [4, 0, -3], legL: [3, 0, 3], wing: [0, 0, 22], wc: 8, ws: 14, wp: 22}),
      k(6, {grip: [-.12, 3.08, .02], spear: sp([-.05, 1, -.08], FWD), sAt: 0, lOn: 1, lAt: -.42, torso: [10, 0, 0], head: [6, 0, 0], ...WING_UP, fx: 1.4}, 'o'),
      k(12, {grip: [-.12, 3.1, .02], fx: 1.2}),
      k(24, {...IDLE}),
    ]},
];

// ---- sampling (used by build_mboss_guardian_rig.mjs and offline checks) -------------------------
const EASE = {io: u => u * u * (3 - 2 * u), i: u => u * u, o: u => 1 - (1 - u) * (1 - u), l: u => u};
export function accumulate(clip) {
  let prev = structuredClone(DEFAULT_POSE);
  return clip.keys.map(([tick, pose, ease]) => { prev = {...prev, ...structuredClone(pose)}; return {tick, p: prev, ease: ease || 'io'}; });
}
function blendPose(a, b, u) {
  const o = {};
  for (const key of Object.keys(DEFAULT_POSE)) {
    const x = a[key], y = b[key];
    if (typeof x === 'string') o[key] = u < 1 ? x : y;
    else if (typeof x === 'number') o[key] = x + (y - x) * u;
    else if (x.length === 4) o[key] = qSlerp(x, y, u);
    else o[key] = vLerp(x, y, u);
  }
  return o;
}
// Drift phase of the floating cubes (one cycle per 40 t). A looping clip uses its own length
// (whole cycles per loop) so the cubes close seamlessly at the wrap.
export const cubePhase = (clip, t) => (clip.loop ? t / clip.len * Math.max(1, Math.round(clip.len / 40)) : t / 40);
export function sampleClip(clip, t, ks = accumulate(clip)) {
  const ph = cubePhase(clip, Math.max(0, t));
  if (t <= ks[0].tick) return {...ks[0].p, ph};
  for (let i = 1; i < ks.length; i++) if (t <= ks[i].tick) {
    const a = ks[i - 1], b = ks[i], u = (t - a.tick) / Math.max(1e-9, b.tick - a.tick);
    const p = blendPose(a.p, b.p, EASE[b.ease](u));
    // discrete channels switch exactly at their key
    for (const key of ['rHand', 'lHand']) p[key] = t >= b.tick ? b.p[key] : a.p[key];
    return {...p, ph};
  }
  return {...ks[ks.length - 1].p, ph};
}
