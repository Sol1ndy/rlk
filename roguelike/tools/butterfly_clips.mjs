// Motion clips of the Moonlit Butterfly (달빛 환영 나비) rig: the contract clips of scratchpad mb2/plan.md
// "Rig clips" (names, lengths and event ticks are what the module reads from the manifest). The keys are first
// passes authored from the timelines in mb2/understand/v1..v4.md and the poses of model.md §5/§8; the clip author
// refines them here. Format, retime and sampling: mboss_rig_clips.mjs. Channels: butterfly_pose.mjs.
//
// Two rest poses: HUMAN (standing, crescent chains at her sides, wings and tendrils at scale 0) and BUTTERFLY
// (hovering with the toes 1.2 b up, wings spread). Every clip states its form at tick 0 (channel `form`); the
// transform, release and revert clips switch it at the tick the wings appear or vanish.
import {q, rot} from './mboss_rig_math.mjs';
import {accumulate as accumulateClip, sampleClip as sampleAt, applyRetime} from './mboss_rig_clips.mjs';

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
// and out (hook tops ≈ 5.7 b over the floor, the two wing sets apart), hindwings sweeping out and down, ribbons hanging, crescents docked at
// the wing roots as the inner frame claws, fans 15 degrees lower.
const B_TORSO = [2, 0, 0];
const B_HANDS = {
  hRA: inTorso([-.36, 2.52, .34], B_TORSO), hRAe: [-12, 0, 14],
  hRB: inTorso([-.42, 2.02, .3], B_TORSO), hRBe: [-8, 0, 34],
  hLA: inTorso([.36, 2.52, .34], B_TORSO), hLAe: [-12, 0, 14],
  hLB: inTorso([.42, 2.02, .3], B_TORSO), hLBe: [-8, 0, 34],
};
export const B_WINGS = {fwL: [14, -6, 0], fwR: [14, -6, 0], hwL: [10, -6, 0], hwR: [10, -6, 0], fwS: 1, hwS: 1, tuL: [0, 0, 0], tuR: [0, 0, 0], tlL: [4, 0, 0], tlR: [4, 0, 0], tS: 1};
export const BUTTERFLY = {
  ...DEFAULT_POSE, pos: [0, 1.13, 0], torso: B_TORSO, head: [4, 0, 0], ...B_HANDS,
  legL: [6, 4, -5], legR: [6, 4, -5], kneeL: -12, kneeR: -9, hockL: 22, hockR: 19,
  fanL: [0, 0, -15], fanR: [0, 0, -15], ...B_WINGS, form: 'b',
};
const WINGS_OFF = {fwS: 0, hwS: 0, tS: 0, core: 0};

// ---- shared poses ----------------------------------------------------------------------------------------------
const H_CROUCH = {pos: [0, -.22, 0], torso: [-22, 0, 0], head: [16, 0, 0], legL: [26, 0, 2], legR: [26, 0, 2], kneeL: -34, kneeR: -34, hockL: 22, hockR: 22, fanL: [0, 0, 14], fanR: [0, 0, 14]};
const H_RUN_LEAN = {torso: [-30, 0, 0], head: [22, 0, 0], fanL: [0, -30, 8], fanR: [0, -30, 8], crest: [-18, 0, 0]};
// flap amplitude about the rest (roll 0): the upstroke stops short of the midline so the two wing sets stay apart
const FLAP_UP = {fwL: [12, -6, 22], fwR: [12, -6, 22], hwL: [8, -4, 12], hwR: [8, -4, 12]};
const FLAP_DOWN = {fwL: [14, -6, -24], fwR: [14, -6, -24], hwL: [8, -4, -14], hwR: [8, -4, -14]};
const WINGS_V = {fwL: [10, -8, 62], fwR: [10, -8, 62], hwL: [6, -4, 30], hwR: [6, -4, 30]};
const WINGS_CUP = {fwL: [10, 64, -8], fwR: [10, 64, -8], hwL: [6, 60, -10], hwR: [6, 60, -10], tuL: [0, 30, 0], tuR: [0, 30, 0]};
const WINGS_POD = {fwL: [-150, 30, -10], fwR: [-150, 30, -10], hwL: [-118, 40, -6], hwR: [-118, 40, -6], tuL: [0, 50, -20], tuR: [0, 50, -20], tlL: [0, 0, -30], tlR: [0, 0, -30]};
const WINGS_FOLDED = {fwL: [40, -60, 70], fwR: [40, -60, 70], hwL: [30, -50, 40], hwR: [30, -50, 40], fwS: .4, hwS: .4, tS: .4};
const WINGS_FLUNG = {fwL: [6, -10, 2], fwR: [6, -10, 2], hwL: [4, -6, -10], hwR: [4, -6, -10], tuL: [0, 0, 60], tuR: [0, 0, 60], tlL: [0, 0, 20], tlR: [0, 0, 20]};
const GLIDE = {rot: [-34, 0, 0], fwL: [24, -30, 8], fwR: [24, -30, 8], hwL: [16, -24, -4], hwR: [16, -24, -4], legL: [-28, 0, -3], legR: [-24, 0, -3], tuL: [-26, 0, 0], tuR: [-26, 0, 0], tlL: [-20, 0, 0], tlR: [-20, 0, 0]};
// a full root spin about one axis in n keys (at most 90 degrees per key)
function spin(t0, t1, axis, from, turns = 1, base = {}) {
  const out = [], n = Math.max(1, Math.round(Math.abs(turns) * 4));
  for (let i = 1; i <= n; i++) {
    const a = from + 360 * turns * i / n, r = [0, 0, 0];
    r[axis] = a;
    out.push(k(Math.round(t0 + (t1 - t0) * i / n), {...base, rot: r}, 'l'));
  }
  return out;
}

export const CLIPS = [
  // ---- human form: idle and locomotion ---------------------------------------------------------------------------
  {name: 'idle_h', len: 40, loop: true, note: 'standing idle: breathing sway; the crescents and flakes bob (phase); crest sways', keys: [
    k(0, {...HUMAN}),
    k(20, {torso: [-12, 0, 0], head: [10, 0, 0], crest: [-4, 0, 2], pos: [0, -.02, 0], fanL: [0, 0, 4], fanR: [0, 0, 4], kneeL: -3, kneeR: -3}),
    k(40, {...HUMAN}),
  ]},
  {name: 'step_h', len: 16, loop: true, note: 'short strafing step (0.1-0.15 b/t, the module moves the anchor)', keys: [
    k(0, {...HUMAN, legL: [18, 0, 2], kneeL: -16, legR: [-12, 0, 0], kneeR: 4}),
    k(4, {pos: [0, .05, 0], legL: [8, 0, 2], kneeL: -26, hockL: 12}),
    k(8, {pos: [0, 0, 0], legL: [-12, 0, 0], kneeL: 4, hockL: 0, legR: [18, 0, 2], kneeR: -16}),
    k(12, {pos: [0, .05, 0], legR: [8, 0, 2], kneeR: -26, hockR: 12}),
    k(16, {pos: [0, 0, 0], legL: [18, 0, 2], kneeL: -16, legR: [-12, 0, 0], kneeR: 4, hockR: 0}),
  ]},
  {name: 'run_h', len: 8, loop: true, blend: 2, note: 'burst-run (0.6-0.8 b/t for about 5 t): body 30 degrees forward, fans swept back, crescents trailing', keys: [
    k(0, {...HUMAN, ...H_RUN_LEAN, legL: [48, 0, 2], kneeL: -40, hockL: 30, legR: [-34, 0, 0], kneeR: 10, hockR: -10}),
    k(2, {pos: [0, .18, 0]}),
    k(4, {pos: [0, 0, 0], legL: [-34, 0, 0], kneeL: 10, hockL: -10, legR: [48, 0, 2], kneeR: -40, hockR: 30}),
    k(6, {pos: [0, .18, 0]}),
    k(8, {pos: [0, 0, 0], legL: [48, 0, 2], kneeL: -40, hockL: 30, legR: [-34, 0, 0], kneeR: 10, hockR: -10}),
  ]},
  {name: 'back_h', len: 12, next: 'idle_h', note: 'backing off at walking pace (the anchor moves back)', keys: [
    k(0, {...HUMAN}),
    k(3, {legR: [-20, 0, 0], kneeR: -10, torso: [-6, 0, 0], pos: [0, .04, 0]}),
    k(6, {legR: [0, 0, 0], kneeR: 0, legL: [-20, 0, 0], kneeL: -10, pos: [0, 0, 0]}),
    k(9, {legL: [0, 0, 0], kneeL: 0, pos: [0, .03, 0]}),
    k(12, {...HUMAN}),
  ]},
  {name: 'turn_h', len: 24, next: 'idle_h', note: 'after groggy: turns from her back (root yaw 180, the groggy_h facing) to the anchor facing', keys: [
    k(0, {...HUMAN, rot: [0, 180, 0], torso: [-5, 0, 0], hands: 0}),
    k(8, {rot: [0, 120, 0], legL: [10, 0, 4], kneeL: -10}),
    k(16, {rot: [0, 50, 0], legL: [0, 0, 0], kneeL: 0, legR: [10, 0, 4], kneeR: -10}),
    k(24, {rot: [0, 0, 0], legR: [0, 0, 0], kneeR: 0, torso: H_TORSO}),
  ]},
  // ---- human form: patterns (H1-H4) ---------------------------------------------------------------------------
  {name: 'kick_combo', len: 51, next: 'idle_h', events: {run: 0, hit1: 8, backflip: 10, hop: 22, leap: 34, hit2: 40}, note: 'H1 달빛 발차기: burst-run in (0-5), rising flip kick at 8, backflip, 12 t sideways-hop wind-up, flying leap, axe kick at 40, landing', keys: [
    k(0, {...HUMAN, ...H_RUN_LEAN, legL: [40, 0, 2], kneeL: -36, legR: [-24, 0, 0]}),
    k(5, {...H_CROUCH, legR: [60, 0, 4], kneeR: -100, hockR: 20, lockR: 1}),
    k(8, {pos: [0, .5, 0], torso: [8, 0, 0], legR: [170, 0, 6], kneeR: 0, hockR: 0, legL: [-10, 0, 0], kneeL: 0, hockL: 0, lockR: 1, fanL: [0, 0, 30], fanR: [0, 0, 30]}, 'i'),
    ...spin(9, 17, 0, 0, -1, {pos: [0, 1.6, 0]}),
    k(20, {pos: [0, .1, 0], rot: [-360, 0, 0], ...H_CROUCH, lockR: 0}),
    k(26, {pos: [0, .3, 0], torso: [-14, -20, 0], legL: [20, 0, 20], legR: [10, 0, 20]}),
    k(32, {pos: [0, .1, 0], ...H_CROUCH, torso: [-24, 20, 0]}),
    k(36, {pos: [0, 1.6, 0], torso: [6, 0, 0], legR: [150, 0, 0], kneeR: 0, lockR: 1, legL: [-30, 0, 0], kneeL: -20}),
    k(40, {pos: [0, .3, 0], torso: [-30, 0, 0], legR: [40, 0, 0], kneeR: 0, hockR: 0, lockR: 1}, 'i'),
    k(44, {...H_CROUCH, pos: [0, -.18, 0], lockR: 0}),
    k(51, {...HUMAN, rot: [-360, 0, 0], pos: [0, 0, 0]}),
  ]},
  {name: 'kick_jump', len: 65, next: 'idle_h', events: {tell: 0, sweep: 13, sweep_end: 19, jump: 33, orb: 45, disc: 45, kick: 52, impact: 55, land: 59}, note: 'H2 달빛 점프: the crescent chain lines up at her left and glows (tell 0-13), 360 degree low sweep 13-19, spiral jump at 33, the orb forms at 45 (disc = orb), kicked down at 52, impact 55, landing 59', keys: [
    k(0, {...HUMAN, hLA: inTorso([.62, 2.6, -.1], H_TORSO), hLB: inTorso([.66, 2.1, -.1], H_TORSO), hRB: inTorso([.62, 1.6, -.1], H_TORSO), hRBe: [10, 0, -10]}),
    k(10, {...H_CROUCH, pos: [0, -.5, 0], legL: [70, 0, 30], kneeL: -20}),
    ...spin(13, 19, 1, 0, 1, {pos: [0, -.5, 0]}),
    k(26, {...H_CROUCH, rot: [0, 360, 0]}),
    k(33, {pos: [0, 1.2, 0], torso: [0, 0, 0], legL: [-20, 0, 0], kneeL: -30, legR: [40, 0, 0], kneeR: -60}, 'o'),
    ...spin(35, 43, 1, 360, 1, {pos: [0, 2.4, 0]}),
    k(45, {pos: [0, 2.5, 0], rot: [0, 720, 0], torso: [-12, 0, 0], legR: [40, 0, 0], kneeR: -50}),
    k(52, {pos: [0, 2.3, 0], torso: [-30, 0, 0], legR: [120, 0, 0], kneeR: 0, lockR: 1}, 'i'),
    k(55, {pos: [0, 1.6, 0], lockR: 0, legR: [20, 0, 0], kneeR: -30}),
    k(59, {...H_CROUCH}, 'i'),
    k(65, {...HUMAN, rot: [0, 720, 0]}),
  ]},
  {name: 'dash_kick', len: 50, next: 'idle_h', events: {charge: 0, dash: 10, dash_end: 12, kick: 15, ring: 19}, note: 'H3 달빛 돌진: mote charge 0-10, dash 5-6 b in 2 t (10-12, the module moves the anchor), lunge kick at 15, the ring at 19', keys: [
    k(0, {...HUMAN}),
    k(10, {...H_CROUCH, torso: [-34, 0, 0]}),
    k(12, {pos: [0, .3, 0], ...H_RUN_LEAN, legR: [70, 0, 0], kneeR: -20, legL: [-40, 0, 0], kneeL: 0, lockR: 1}, 'i'),
    k(15, {pos: [0, .4, 0], torso: [-10, 0, 0], legR: [95, 0, 0], kneeR: 0, hockR: 0, lockR: 1}, 'i'),
    k(24, {...H_CROUCH, lockR: 0}),
    k(50, {...HUMAN}),
  ]},
  {name: 'vacuum', len: 41, next: 'idle_h', events: {crouch: 0, tell: 9, stomp: 16, blade: 17, backflip: 17, land: 38}, note: 'H4 광폭한 진공: crouch 9 t, glint, stomp-kick launches the vertical blade at 17, backflip airborne 17-38', keys: [
    k(0, {...HUMAN}),
    k(9, {...H_CROUCH, legR: [50, 0, 0], kneeR: -80, hockR: 30}),
    k(14, {pos: [0, .3, 0], legR: [110, 0, 0], kneeR: -20, torso: [0, 0, 0]}),
    k(17, {pos: [0, .5, 0], legR: [40, 0, 0], kneeR: 0, torso: [-30, 0, 0]}, 'i'),
    ...spin(18, 34, 0, 0, 1, {pos: [0, 2.6, 0]}),
    k(38, {...H_CROUCH, rot: [360, 0, 0], pos: [0, -.2, 0]}, 'i'),
    k(41, {...HUMAN, rot: [360, 0, 0], pos: [0, 0, 0]}),
  ]},
  {name: 'groggy_h', len: 40, loop: true, note: 'groggy (300 t in the pattern): motionless idle with her back turned (root yaw 180), fans drooped, crescents hidden', keys: [
    k(0, {...HUMAN, rot: [0, 180, 0], torso: [-5, 0, 0], head: [2, 0, 0], fanL: [0, 0, -15], fanR: [0, 0, -15], hands: 0}),
    k(20, {torso: [-7, 0, 0], crest: [-3, 0, 2], kneeL: -4, kneeR: -4, pos: [0, -.03, 0]}),
    k(40, {torso: [-5, 0, 0], crest: [0, 0, 0], kneeL: 0, kneeR: 0, pos: [0, 0, 0]}),
  ]},
  // ---- entrance, transform ---------------------------------------------------------------------------------------
  {name: 'entrance', len: 106, next: 'idle_h', events: {nameplate: 57, glow: 61, whiteout: 71, burst: 79, land: 90, stand: 106}, note: 'hidden inside the cocoon prop until the burst at 79 (rig/prop/cocoon); she drops from 4 b, lands at 90 and stands up by 106', keys: [
    k(0, {...HUMAN, vis: 0, pos: [0, 4, 0]}),
    k(78, {vis: 0}),
    k(79, {vis: 1, pos: [0, 4, 0], torso: [10, 0, 0], legL: [-20, 0, 0], legR: [-14, 0, 0], kneeL: -30, kneeR: -30, fanL: [0, 0, 30], fanR: [0, 0, 30]}),
    k(90, {...H_CROUCH, pos: [0, -.35, 0], torso: [-34, 0, 0]}, 'i'),
    k(106, {...HUMAN}),
  ]},
  {name: 'transform', len: 30, next: 'idle_b', events: {glow: 0, open: 4, sphere: 6, rings: 9, spread: 12}, note: 'human -> butterfly: the cocoon glow (core), folded wings at 4, light sphere at 6 (달빛 고치 is applied there), the wings unfold over 8 t (4-12), hover lift; the form switches to butterfly at 4', keys: [
    k(0, {...HUMAN, core: 1}),
    k(3, {core: 1.6, ...WINGS_FOLDED, fwS: 0, hwS: 0, tS: 0, wlook: 'flat'}),
    k(4, {...WINGS_FOLDED, form: 'b'}),
    k(6, {core: 3}),
    k(12, {...BUTTERFLY, core: 1, wlook: 'flat'}),
    k(14, {wlook: 'el', core: 0}),
    k(30, {...BUTTERFLY}),
  ]},
  // ---- butterfly form: idle and travel -----------------------------------------------------------------------------
  {name: 'idle_b', len: 22, loop: true, note: 'hover flap: forewing leads, hindwing lags 2-3 t, ribbons lag 4 t; body bob ±0.15 b rising on the downstroke', keys: [
    k(0, {...BUTTERFLY}),
    k(6, {...FLAP_UP, pos: [0, 1.05, 0], tuL: [0, 0, 6], tuR: [0, 0, 6]}),
    k(9, {hwL: [8, -4, 10], hwR: [8, -4, 10]}),
    k(15, {...FLAP_DOWN, pos: [0, 1.25, 0], tuL: [0, 0, -6], tuR: [0, 0, -6], tlL: [4, 0, 8], tlR: [4, 0, 8]}),
    k(22, {...BUTTERFLY}),
  ]},
  {name: 'glide_b', len: 16, loop: true, blend: 4, note: 'gliding travel: body pitched forward, wings swept back, legs trailing, ribbons streaming', keys: [
    k(0, {...BUTTERFLY, ...GLIDE}),
    k(8, {fwL: [24, -30, 16], fwR: [24, -30, 16], pos: [0, 1.7, 0]}),
    k(16, {...BUTTERFLY, ...GLIDE}),
  ]},
  // ---- butterfly form: patterns (B1-B5) ---------------------------------------------------------------------------
  {name: 'wing_strike', len: 55, next: 'idle_b', events: {bank: 0, dive: 12, hit: 15}, note: 'B1 우아한 날개: bank and climb 0-9, dive 12-15, wing-edge arc hit at 15, climb and flutter', keys: [
    k(0, {...BUTTERFLY}),
    k(9, {...BUTTERFLY, ...WINGS_V, rot: [0, 0, -40], pos: [0, 2.6, 0]}),
    k(12, {rot: [-20, 0, -60], pos: [0, 2.3, 0], ...FLAP_UP}, 'i'),
    k(14, {rot: [-30, 0, -80], pos: [0, 1.0, 0], ...FLAP_DOWN}, 'i'),
    k(15, {rot: [-10, -60, -85], pos: [0, .8, 0]}, 'l'),
    k(22, {rot: [10, -30, -20], pos: [0, 2.2, 0], ...FLAP_UP}),
    k(30, {...FLAP_DOWN, rot: [0, 0, 0]}),
    k(40, {...FLAP_UP, pos: [0, 1.9, 0]}),
    k(55, {...BUTTERFLY}),
  ]},
  {name: 'wing_barrage', len: 117, next: 'idle_b', events: {swing1: 5, swing2: 31, swing3: 69, swing4: 94}, note: 'B2 화염 날개의 습격 (Pyro look): a 5 t wind-up, then four spinning wing swings at 5/31/69/94, each throwing 5 fire crescents', keys: [
    k(0, {...BUTTERFLY, ...WINGS_V}),
    k(7, {...FLAP_DOWN}),
    ...spin(7, 15, 1, 0, 1),
    k(23, {...BUTTERFLY, rot: [0, 360, 0], ...WINGS_V}),
    k(32, {...FLAP_DOWN}),
    ...spin(32, 40, 1, 360, -1),
    k(57, {...BUTTERFLY, rot: [0, 0, 0], ...WINGS_V}),
    k(71, {...FLAP_DOWN}),
    ...spin(71, 79, 1, 0, 1),
    k(85, {...BUTTERFLY, rot: [0, 360, 0], ...WINGS_V}),
    k(96, {...FLAP_DOWN}),
    ...spin(96, 104, 1, 360, -1),
    k(117, {...BUTTERFLY, rot: [0, 0, 0]}),
  ]},
  {name: 'flap_dive', len: 59, next: 'idle_b', events: {rise: 0, dive: 22, slam: 26, fan: 28, glide: 34}, note: 'B3 날개 휩쓸개 (Pyro look): two big flaps and a rise (0-22), head-first dive (22-26), wing slam at 26, flame fan 28-32, low glide', keys: [
    k(0, {...BUTTERFLY}),
    k(5, {...WINGS_V, pos: [0, 2.2, 0]}),
    k(8, {...FLAP_DOWN, pos: [0, 2.6, 0]}, 'i'),
    k(14, {...WINGS_V, pos: [0, 3.4, 0]}),
    k(17, {...FLAP_DOWN, pos: [0, 4.0, 0]}, 'i'),
    k(22, {...WINGS_V, rot: [-60, 0, 0], pos: [0, 4.2, 0]}),
    k(24, {rot: [-90, 0, 0], pos: [0, 2.0, 0]}, 'i'),
    k(26, {rot: [-20, 0, 0], pos: [0, .9, 0], ...WINGS_CUP}, 'i'),
    k(34, {...BUTTERFLY, ...GLIDE, pos: [0, .9, 0]}),
    k(50, {...GLIDE, pos: [0, 1.2, 0]}),
    k(59, {...BUTTERFLY}),
  ]},
  {name: 'coco', len: 76, next: 'idle_b', events: {wrap: 5, orb1: 19, ball: 30, ball_open: 42, orb2: 46}, note: 'B4 달빛 축복: wings wrap forward (charge), orb 1 launched at 19 (rig/prop/orb), the cocoon ball 30-42 (rig/prop/pod), orb 2 at 46', keys: [
    k(0, {...BUTTERFLY}),
    k(5, {...WINGS_CUP, core: .8}),
    k(17, {...WINGS_CUP, core: 1.6}),
    k(19, {...BUTTERFLY, ...FLAP_UP, core: 0}, 'i'),
    k(26, {...BUTTERFLY}),
    k(30, {...WINGS_POD, torso: [-30, 0, 0], legL: [60, 0, 0], legR: [60, 0, 0], kneeL: -90, kneeR: -90}),
    k(42, {...WINGS_POD, torso: [-30, 0, 0], legL: [60, 0, 0], legR: [60, 0, 0], kneeL: -90, kneeR: -90, core: 1.4}),
    k(46, {...BUTTERFLY, ...WINGS_FLUNG, core: 0}, 'i'),
    k(60, {...BUTTERFLY}),
    k(76, {...BUTTERFLY}),
  ]},
  {name: 'release', len: 96, next: 'idle_h', events: {swoop: 0, whirl: 28, cup: 31, flash: 35, glint: 37, rings: 38, wrap: 44, detonation: 53, hover: 56, shrink: 87, flat: 87, shatter: 91, revert: 92, land: 96},
    note: 'B5 달빛 해제: wings fold, swoop past (0-8), climb, mid-air whirl (2 tumbles 12-28, the star flare at 28), cup (31 = E-22), ground flash 35, X glint 37, ring cage 38-43, the pod wrap (44-52), DETONATION at 53, hover 2 b up, the wings go flat lime and shrink (87) and shatter (91), the human form drops (92) and lands (96); the form switches to human at 92', keys: [
      k(0, {...BUTTERFLY, ...WINGS_V}),
      k(6, {...GLIDE, pos: [0, .9, 0]}, 'i'),
      k(11, {...BUTTERFLY, pos: [0, 3.2, 0], ...WINGS_V}),
      ...spin(12, 28, 2, 0, 2, {pos: [0, 3.4, 0]}),
      k(31, {...BUTTERFLY, rot: [0, 0, 720], pos: [0, 3.2, 0]}),
      k(36, {...WINGS_CUP, pos: [0, 3.0, 0], core: .8}),
      k(44, {...WINGS_CUP, core: 1.4}),
      k(51, {...WINGS_POD, torso: [-14, 0, 0], legL: [40, 0, 0], legR: [40, 0, 0], kneeL: -70, kneeR: -70, core: 2.2}),
      k(52, {fwL: [-70, 10, -4], fwR: [-70, 10, -4], hwL: [-50, 20, -6], hwR: [-50, 20, -6], tuL: [0, 20, 20], tuR: [0, 20, 20], core: 2.6}, 'l'),
      k(53, {...BUTTERFLY, ...WINGS_FLUNG, rot: [0, 0, 720], pos: [0, 3.0, 0], core: 3}, 'l'),
      k(58, {core: 0}),
      k(87, {...BUTTERFLY, ...WINGS_FLUNG, rot: [0, 0, 720], pos: [0, 2.9, 0], wlook: 'flat'}),
      k(90, {fwS: .5, hwS: .5, tS: .5}),
      k(91, {fwS: .5, hwS: .5, tS: .5}),
      k(92, {...WINGS_OFF, form: 'h', wlook: 'el', ...H_HANDS, hands: 0, torso: H_TORSO, legL: [-10, 0, 0], legR: [-6, 0, 0], kneeL: -20, kneeR: -20, hockL: 10, hockR: 10, fanL: [0, 0, 0], fanR: [0, 0, 0], pos: [0, 2.6, 0]}),
      k(95, {...H_CROUCH, pos: [0, .1, 0], hands: 0}, 'i'),
      k(96, {...H_CROUCH, pos: [0, -.25, 0], hands: 0}),
    ]},
  {name: 'revert', len: 43, next: 'idle_h', events: {shrink: 30, flat: 34, shatter: 38, revert: 39, land: 43}, note: 'butterfly -> human without the blast (the end of 달빛 해제): hover, the wings shrink, go flat lime and shatter, she drops and lands; the form switches to human at 39', keys: [
    k(0, {...BUTTERFLY, ...WINGS_FLUNG}),
    k(30, {pos: [0, 2.0, 0]}),
    k(34, {fwS: .5, hwS: .5, tS: .5, wlook: 'flat'}),
    k(38, {fwS: .5, hwS: .5, tS: .5}),
    k(39, {...WINGS_OFF, form: 'h', wlook: 'el', ...H_HANDS, hands: 0, torso: H_TORSO, legL: [-10, 0, 0], legR: [-6, 0, 0], kneeL: -20, kneeR: -20, fanL: [0, 0, 0], fanR: [0, 0, 0]}),
    k(41, {pos: [0, .3, 0]}, 'i'),
    k(43, {...H_CROUCH, pos: [0, -.25, 0], hands: 0}),
  ]},
  {name: 'death', len: 100, blend: 6, events: {stagger: 0, shatter: 6, kneel: 24, dissolve: 40, gone: 100}, note: 'she staggers; from butterfly form the wings go flat lime and shrink away over 6 t (the shatter at 6) while she sinks to the floor; she kneels, then dissolves into rising motes (scale out); call kill after 100. Starts from either form', keys: [
    k(0, {torso: [8, 0, 0], head: [-10, 0, 0], fanL: [0, 0, 30], fanR: [0, 0, 30], ...WINGS_OFF, form: 'h', wlook: 'flat'}),
    k(6, {wlook: 'el', hands: .6}),
    k(24, {...HUMAN, ...H_CROUCH, pos: [0, -.55, 0], torso: [-40, 0, 0], head: [20, 0, 0], legL: [70, 0, 4], legR: [-20, 0, 0], kneeL: -110, kneeR: -100, hockL: 60, hockR: 60, hands: .3, fanL: [0, 0, -30], fanR: [0, 0, -30]}),
    k(40, {hands: .3}),
    k(56, {hands: 0, flakes: 0}),
    k(100, {vis: 0, pos: [0, .6, 0]}),
  ]},
  {name: 'chain_reform', len: 18, next: 'idle_h', note: 'the crescent chain re-forms after groggy (hands scale back in, with a flourish)', keys: [
    k(0, {...HUMAN, hands: 0}),
    k(6, {hands: .4, hRA: inTorso([-.7, 2.3, -.3], H_TORSO)}),
    k(12, {hands: 1.08}),
    k(18, {...HUMAN}),
  ]},
];
// Wind-up retiming table (as the Guardian's; empty until the patterns are tuned).
export const RETIME = {};
applyRetime(CLIPS, RETIME);

// ---- sampling ------------------------------------------------------------------------------------------------------
export const accumulate = clip => accumulateClip(clip, DEFAULT_POSE);
// idle phase of the crescent/flake bob: one cycle per 40 t (a loop: whole cycles per loop)
export const bobPhase = (clip, t) => (clip.loop ? t / clip.len * Math.max(1, Math.round(clip.len / 40)) : t / 40);
export const sampleClip = (clip, t, ks = accumulate(clip)) => sampleAt(clip, t, ks, {defaults: DEFAULT_POSE, discrete: ['form', 'wlook'], phase: bobPhase});
// The two rest poses as sampled poses (for spawn, renders and checks).
export const restPose = which => ({...(which === 'b' ? BUTTERFLY : HUMAN), ph: 0});
