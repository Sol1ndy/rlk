// The 45 motion clips of the Raiden rig (scratchpad rd/plan.md §C.5; §B.2 gives the pattern timelines the events
// belong to). Format and sampling: mboss_rig_clips.mjs. Clip ticks are played ticks; the events are the ticks the
// pattern code schedules its hits, cues and props on (binding: S1-RIG may retime inside a clip, never an event tick).
//
// Pose channels (raiden_geometry.mjs solve; rig frame +X her left, +Y up, -Z forward, blocks / degrees):
//   pos [x,y,z]          root offset (crouch, the Tenma float 1.0)       rot [p,y,r]   root euler about the hips
//   torso, head          eulers (torso relative to the root, head to the torso; pitch + leans back)
//   armL/armR legL/legR  paired eulers authored in her LEFT side's sense (the right side mirrors [p,-y,-r]):
//                        pitch + swings the limb forward, roll + raises it outward
//   elbowL/R             forearm pitch relative to the upper arm (+ bends forward); kneeL/R + bends the knee
//   braid, drape, halo   eulers (braid and halo relative to the torso, drape to the root); drapeF the drape's flare
//   wpn                  weapon quaternion in the torso frame (blade() below); wS weapon scale, wfx its glow card
//   sS / tS              Shogun extras / Tenma parts scale (form fade); haloS, aura (guard floor ring) scales
//   disc                 Tenma disc halo euler (torso frame)
//   gH, glv, gPole       giant-arm grip point (root frame, unfloated), glaive quaternion (glaive()), elbow pole
//   glvS, gfx            glaive shown (0 = thrown) and its edge glow
//   rU1..3, rF1..3       thin right arms: upper / forearm directions (root frame)
//   gtL, gtR, gtLe, gtRe gauntlet positions and eulers (paired)
//   bob, tBob            Shogun halo bob / Tenma float bob amplitude (phase = loop phase)
//   vis                  everything scaled about the body centre (blinks)
//   form 's' | 't' | 'k' discrete: the form a clip shows (k = keep the current one: death)
import {accumulate as accumulateLib, sampleClip as sampleLib} from './mboss_rig_clips.mjs';
import {bladeQ} from './raiden_geometry.mjs';
import {basisQ, cross, unit} from './mboss_rig_math.mjs';

// ---- helpers ------------------------------------------------------------------------------------------------------------
const N = v => unit(v);
// katana / polearm frame in the torso frame: blade tip (+Y) along tip, the edge (-Z face) toward edge
export const blade = (tip, edge) => bladeQ(N(tip), edge);
// glaive frame in the root frame: shaft toward the blade tip (+Y) along tip, the blade's edge side (+X) toward side
// The puppet's giant arm and glaive sit on her RIGHT and the thin arms on her LEFT (B_v7 / B_v9 with her facing the
// camera); the Tenma constants below were authored the other way round and are mirrored in X by mx().
const mx = v => [-v[0], v[1], v[2]];
export function glaive(tip0, side0) {
  const tip = mx(tip0), side = mx(side0);
  const Y = N(tip); let X = side.map((x, i) => x - Y[i] * (side[0] * Y[0] + side[1] * Y[1] + side[2] * Y[2])); X = N(X);
  return basisQ(X, Y, cross(X, Y));
}
const K = (t, pose, ease = 'l') => [t, pose, ease];

// ---- default pose: the Shogun idle with the katana (sword look) --------------------------------------------------------
const W_IDLE = blade([-.35, -.5, -.79], [0, -1, .3]);          // katana low on her right, tip down and forward near the floor
const G_IDLE = glaive([-1, -.06, -.12], [0, 1, -.2]);           // glaive across the front at hip height, blade to her right
export const DEFAULT_POSE = {
  pos: [0, 0, 0], rot: [0, 0, 0], torso: [0, 0, 0], head: [-6, 0, 0],
  armL: [2, 0, 7], armR: [10, 0, 9], elbowL: 10, elbowR: 16,
  legL: [0, 0, 3], legR: [-3, 0, 5], kneeL: 0, kneeR: 6,
  braid: [-5, 0, 0], drape: [-3, 0, 0], drapeF: 1, halo: [0, 0, 0], haloS: 1, aura: 0,
  wpn: W_IDLE, wS: 1, wfx: 0, sS: 1, tS: 0, bob: 0, tBob: 0, vis: 1,
  disc: [0, 0, 0], gH: [-1.6, .78, -1.05], glv: G_IDLE, gPole: [-1, -.35, .25], glvS: 1, gfx: 0,
  rU1: [.45, .85, .22], rF1: [.12, 1, -.12], rU2: [.82, .45, .2], rF2: [.75, .55, -.35], rU3: [.92, -.05, .15], rF3: [.78, .28, -.5],
  gtL: [.95, -.3, -1.25], gtR: [-.95, -.3, -1.25], gtLe: [-6, 8, -6], gtRe: [-6, 8, -6],
  form: 's',
};
export const DISCRETE = ['form'];

// ---- named poses --------------------------------------------------------------------------------------------------------
const S_IDLE = {torso: [0, -4, 0], head: [-6, 2, 0], armL: [2, 0, 7], armR: [10, 0, 9], elbowL: 10, elbowR: 16, legL: [0, 0, 3], legR: [-3, 0, 5], kneeL: 0, kneeR: 6,
  pos: [0, 0, 0], rot: [0, 0, 0], wpn: W_IDLE, wfx: 0, braid: [-5, 0, 0], drape: [-3, 0, 0], drapeF: 1, aura: 0, haloS: 1, vis: 1, sS: 1, tS: 0};
const W_PIDLE = blade([-.4, -.42, -.81], [0, -.4, -1]);         // polearm: blade low in front on her right, spike up behind the shoulder
const P_IDLE = {...S_IDLE, armR: [18, 0, 12], elbowR: 34, wpn: W_PIDLE};
// iai stance (sword at the left hip, edge up, low wide stance, torso turned)
const W_SHEATH = blade([.25, -.12, 1], [0, 1, 0]);
const S_IAI = {pos: [0, -.12, 0], torso: [-12, 28, 0], head: [-4, -24, 0], armR: [38, -20, -38], elbowR: 62, armL: [26, 0, -12], elbowL: 70,
  legL: [-22, 0, 10], legR: [30, 0, 8], kneeL: 26, kneeR: 34, wpn: W_SHEATH, braid: [-12, 0, 0], drapeF: 1.15};
// sword swept to her right after a horizontal draw, arm extended
const W_RIGHT = blade([-1, -.08, -.25], [0, 0, -1]);
const S_DRAWN = {pos: [0, -.1, 0], torso: [-8, -38, 0], head: [-4, 30, 0], armR: [10, -10, 82], elbowR: 6, armL: [-10, 0, 30], elbowL: 18,
  legL: [-26, 0, 8], legR: [34, 0, 10], kneeL: 20, kneeR: 30, wpn: W_RIGHT, braid: [-30, 0, 10], drapeF: 1.3};
// sword raised overhead, two-handed
const W_UP = blade([.05, 1, .15], [0, 0, -1]);
const S_RAISE = {pos: [0, 0, 0], torso: [6, 0, 0], head: [-2, 0, 0], armR: [168, 0, 6], elbowR: 14, armL: [160, 0, 10], elbowL: 26,
  legL: [-6, 0, 6], legR: [10, 0, 6], kneeL: 6, kneeR: 10, wpn: W_UP, braid: [-8, 0, 0]};
// sword brought down in front (overhead slash follow-through)
const W_DOWN = blade([0, -.55, -.84], [0, -.84, .55]);
const S_CHOP = {pos: [0, -.14, 0], torso: [-22, 0, 0], head: [-8, 0, 0], armR: [70, 0, 4], elbowR: 6, armL: [62, 0, 10], elbowL: 18,
  legL: [-18, 0, 6], legR: [28, 0, 6], kneeL: 22, kneeR: 34, wpn: W_DOWN, braid: [-20, 0, 0]};
// guard stance: blade held across the front, upright, left hand behind the blade
const W_GUARD = blade([.15, .95, -.25], [0, 0, -1]);
const S_GUARD = {pos: [0, -.08, 0], torso: [-6, 10, 0], head: [-6, -6, 0], armR: [52, 0, -14], elbowR: 64, armL: [40, 0, -6], elbowL: 74,
  legL: [-12, 0, 10], legR: [16, 0, 8], kneeL: 16, kneeR: 20, wpn: W_GUARD, aura: 1, haloS: 1.12, braid: [-8, 0, 0]};
// casting: left hand raised palm forward
const S_CAST = {torso: [4, 8, 0], head: [-2, -8, 0], armL: [130, 0, 24], elbowL: 18, armR: [12, 0, 12], elbowR: 18, legL: [-6, 0, 4], legR: [6, 0, 6], kneeR: 8, wpn: W_IDLE};
// kneel (stagger, exhausted, death): right knee down, head bowed, weapon held low
const KNEEL = {pos: [0, -.33, 0], torso: [-30, 0, 4], head: [-22, 0, -4], armR: [44, 0, 14], elbowR: 20, armL: [64, 4, 18], elbowL: 36,
  legR: [52, 0, -4], kneeR: 104, legL: [-6, 0, 6], kneeL: 92, wpn: blade([-.2, -.35, -.92], [0, -1, .3]), braid: [-30, 0, 0], drape: [-10, 0, 0]};
// polearm overhead twirl hand position (blade up, held above the head)
const P_OVER = {torso: [4, 0, 0], head: [2, 0, 0], armR: [170, 0, 10], elbowR: 10, armL: [30, 0, 30], elbowL: 30, legL: [-8, 0, 8], legR: [10, 0, 8], kneeL: 8, kneeR: 10};
const twirl = a => blade([Math.cos(a * Math.PI / 180), .05, Math.sin(a * Math.PI / 180)], [0, -1, 0]);   // shaft horizontal, spinning about Y
// polearm thrust forward (blade ahead), lunge
const W_THRUST = blade([-.05, -.08, -1], [0, -1, 0]);
const P_LUNGE = {pos: [0, -.16, -.1], torso: [-24, 6, 0], head: [12, -4, 0], armR: [88, 0, -6], elbowR: 4, armL: [70, 0, -8], elbowL: 30,
  legL: [-34, 0, 6], legR: [44, 0, 6], kneeL: 16, kneeR: 50, wpn: W_THRUST, braid: [-40, 0, 0], drapeF: 1.35, drape: [-18, 0, 0]};
// polearm sweep, blade to her left / right at waist height
const W_PSWEEP_L = blade([1, -.05, -.4], [0, 0, -1]), W_PSWEEP_R = blade([-1, -.05, -.4], [0, 0, -1]);
const P_SWEEP_L = {pos: [0, -.1, 0], torso: [-8, 34, 0], head: [-4, -26, 0], armR: [80, 0, -40], elbowR: 10, armL: [30, 0, 40], elbowL: 30,
  legL: [-18, 0, 10], legR: [24, 0, 8], kneeL: 18, kneeR: 26, wpn: W_PSWEEP_L, braid: [-20, 0, -12]};
const P_SWEEP_R = {...P_SWEEP_L, torso: [-8, -36, 0], head: [-4, 26, 0], armR: [60, 0, 60], elbowR: 6, armL: [20, 0, -10], wpn: W_PSWEEP_R, braid: [-20, 0, 12]};

// Tenma base: floating core figure, the giant arm holding the glaive across the front, the fan of thin arms
const T_IDLE = {form: 't', pos: [0, 1, 0], rot: [0, 0, 0], torso: [0, 0, 0], head: [-6, 0, 0], armL: [12, 0, 22], armR: [12, 0, 22], elbowL: 24, elbowR: 24,
  legL: [10, 0, 4], legR: [4, 0, 4], kneeL: 16, kneeR: 8, braid: [-10, 0, 0], sS: 0, tS: 1, vis: 1, disc: [0, 0, 0], glvS: 1, gfx: 0,
  gH: [-1.6, .78, -1.05], glv: G_IDLE, gPole: [-1, -.35, .25]};
// glaive positions
const G_HIGH_L = glaive([.35, .55, .75], [0, 0, -1]);           // raised high on her left, blade back-up (sweep wind-up)
const G_FRONT_R = glaive([-1, .05, -.55], [0, 1, 0]);           // swept across to her right-front
const G_FRONT_L = glaive([1, .05, -.55], [0, 1, 0]);            // swept back to her left-front
const G_COCK = glaive([-.1, .25, -1], [0, 1, 0]);               // cocked over the shoulder, blade pointing forward for the throw
const G_UP = glaive([0, 1, .05], [-1, 0, 0]);                   // held overhead, vertical
const G_SLAM = glaive([0, -.32, -1], [0, 0, 1]);                // slammed down in front, tip forward-down (kept above the floor)
const G_SHEATH = glaive([.3, -.12, 1], [0, 1, 0]);              // iai: drawn back along her left side

// ---- clips --------------------------------------------------------------------------------------------------------------
// [name, len, {loop, next, form, keys, events, note}]
const IDLE_BREATH = (base, extra = {}) => [K(0, {...base}), K(20, {...base, torso: [base.torso[0] - 1, base.torso[1] + 2, 1], head: [base.head[0] + 3, base.head[1] - 2, 0],
  armL: [base.armL[0] + 2, 0, base.armL[2] + 2], ...extra}, 'io'), K(40, {...base}, 'io')];
export const CLIPS = [
  {name: 'idle_sword', len: 40, loop: true, keys: [K(0, {...S_IDLE, bob: 1}), ...IDLE_BREATH({...S_IDLE, bob: 1}).slice(1)], note: 'Shogun idle, katana low on her right'},
  {name: 'idle_polearm', len: 40, loop: true, keys: [K(0, {...P_IDLE, bob: 1}), ...IDLE_BREATH({...P_IDLE, bob: 1}).slice(1)], note: 'Shogun idle, polearm slanted, blade low'},
  {name: 'blink_out', len: 6, events: {gone: 4}, keys: [K(0, {}), K(2, {pos: [0, -.06, 0], torso: [-12, 0, 0], kneeL: 14, kneeR: 18, vis: .9}), K(4, {vis: 0}, 'i'), K(6, {vis: 0})],
    note: 'dissolve: crouch, then gone at 4'},
  {name: 'blink_in', len: 10, events: {appear: 0, settle: 8}, keys: [K(0, {...S_IDLE, vis: 0, torso: [-14, 0, 0], legR: [26, 0, 6], kneeR: 26, kneeL: 12, pos: [0, -.08, 0], drapeF: 1.3, braid: [-30, 0, 0]}),
    K(3, {vis: 1}, 'o'), K(8, {...S_IDLE}, 'io'), K(10, {...S_IDLE})], note: 'reappear in a forward lean, settle at 8'},
  {name: 'iai_dash', len: 36, events: {stance: 0, flash: 6, hit1: 18, hit2: 24}, keys: [
    K(0, {...S_IAI}, 'o'), K(6, {...S_IAI, torso: [-16, 30, 0], wfx: .6}), K(14, {...S_IAI, pos: [0, -.18, 0], torso: [-26, 34, 0], legR: [40, 0, 8], kneeR: 46, wfx: .8, braid: [-40, 0, 0], drapeF: 1.4}, 'i'),
    K(18, {...S_DRAWN, wfx: 1}, 'i'), K(21, {...S_DRAWN, torso: [-6, -20, 0], wpn: blade([-.7, .2, -.7], [0, .6, -.8]), wfx: 1}),
    K(24, {...S_DRAWN, torso: [-4, 30, 0], head: [-4, -20, 0], armR: [60, 0, -30], elbowR: 10, wpn: blade([.9, .1, -.4], [0, 0, -1]), wfx: 1}, 'i'),
    K(30, {...S_DRAWN, torso: [-4, 20, 0], armR: [40, 0, -10], wpn: blade([.6, -.4, -.7], [0, -1, 0]), wfx: 0}), K(36, {...S_IDLE}, 'io')],
    note: 'far 뇌명: iai stance, star flash 6, dash cut 18 (the pattern moves her 9 b), end crescent 24'},
  {name: 'iai_near', len: 28, events: {raise: 0, flash: 10, hit1: 22, hit2: 28}, keys: [
    K(0, {}), K(3, {wpn: blade([.1, -.05, -1], [0, -1, 0])}), K(6, {...S_IAI}, 'o'), K(10, {...S_IAI, wfx: .6}), K(19, {...S_IAI, torso: [-18, 36, 0], kneeR: 40, wfx: .8}, 'i'),
    K(22, {...S_DRAWN, wfx: 1}, 'i'), K(25, {...S_DRAWN, armR: [40, 0, 40], elbowR: 30, wpn: blade([-.3, -.3, -.9], [0, -1, .3]), wfx: .8}),
    K(28, {...S_RAISE, pos: [0, -.04, 0], torso: [8, -10, 0], armL: [20, 0, 20], wpn: blade([0, 1, -.35], [0, .35, -1]), wfx: 1}, 'i')],
    note: 'near 뇌명: draw at 22, rising crescent 28 (the pattern blends back to idle)'},
  {name: 'combo5', len: 74, events: {cue: 0, s1: 12, s2: 22, s3: 34, s4: 50, s5: 64}, keys: [
    K(0, {...S_IDLE, wfx: .4}), K(6, {...S_RAISE, torso: [6, 20, 0], armR: [150, 0, 30], wpn: blade([.4, .9, .2], [0, 0, -1]), wfx: .6}, 'o'),
    K(12, {...S_CHOP, torso: [-18, -16, 0], armR: [64, 0, 24], wpn: blade([-.4, -.5, -.77], [0, -.8, .5]), wfx: 1}, 'i'),
    K(17, {...S_DRAWN, torso: [-8, 30, 0], head: [-4, -20, 0], armR: [60, 0, -36], elbowR: 30, wpn: blade([.85, .1, .5], [0, 0, 1]), wfx: .7}),
    K(22, {...S_DRAWN, wfx: 1}, 'i'),
    K(28, {...S_IAI, pos: [0, -.06, 0], torso: [-6, -10, 0], armR: [40, 0, 50], elbowR: 80, wpn: blade([-.2, .1, 1], [0, 1, 0]), wfx: .6}),
    K(34, {...P_LUNGE, wpn: blade([0, -.35, -.94], [0, -.94, .35]), armR: [76, 0, 4], wfx: 1}, 'i'),
    K(42, {...S_IAI, torso: [-6, 34, 0], wfx: .7}), K(50, {...S_DRAWN, pos: [0, -.16, 0], torso: [-10, -46, 0], wfx: 1}, 'i'),
    K(57, {...S_RAISE, torso: [10, 6, 0], wfx: .8}, 'o'), K(64, {...S_CHOP, wfx: 1}, 'i'), K(70, {...S_CHOP, wfx: 0}), K(74, {...S_IDLE}, 'io')],
    note: 'sword 5-hit chain: V 12, right cut 22, stab 34, wide cut 50, overhead 64'},
  {name: 'disc_cast', len: 40, events: {cue: 0, d1: 6, d2: 10, d3: 18, wave: 34}, keys: [
    K(0, {...S_IDLE, wfx: .5}), K(4, {...S_DRAWN, pos: [0, -.04, 0], torso: [-4, 24, 0], armR: [70, 0, -20], elbowR: 20, wpn: blade([.6, .2, -.8], [0, 0, -1]), wfx: .8}),
    K(6, {...S_DRAWN, pos: [0, -.04, 0], torso: [-4, -14, 0], armR: [76, 0, 30], elbowR: 8, wpn: blade([-.6, .1, -.8], [0, 0, -1]), wfx: 1}, 'i'),
    K(10, {...S_DRAWN, pos: [0, -.04, 0], torso: [-4, 18, 0], armR: [80, 0, -24], elbowR: 8, wpn: blade([.6, .1, -.8], [0, 0, -1]), wfx: 1}, 'i'),
    K(14, {...S_RAISE, armR: [130, 0, 30], wpn: blade([.3, .8, -.5], [0, 0, -1]), wfx: .8}),
    K(18, {...S_CHOP, pos: [0, -.06, 0], torso: [-12, 0, 0], wfx: 1}, 'i'),
    K(26, {...S_IAI, wfx: .8}), K(32, {...S_IAI, pos: [0, -.18, 0], torso: [-18, 40, 0], kneeR: 46, wfx: 1}),
    K(34, {...S_DRAWN, pos: [0, -.2, 0], wpn: blade([-1, -.3, -.2], [0, -.4, -1]), wfx: 1}, 'i'), K(40, {...S_DRAWN, wfx: 0}, 'o')],
    note: '뇌전이 이끈 번개: flicks launch discs 6/10/18, wind-up 26-32, low wave 34'},
  {name: 'rear_iai', len: 30, events: {cue: 0, hit: 14}, keys: [
    K(0, {...S_IDLE, armL: [100, 0, 30], elbowL: 30, wfx: .4}),
    K(8, {...S_IDLE, pos: [0, -.06, 0], torso: [-6, -20, 0], armL: [110, 0, 34], elbowL: 26, armR: [-20, 0, 20], elbowR: 40, wpn: blade([.1, -.2, 1], [0, -1, 0]), wfx: .8}),
    K(14, {...S_IDLE, pos: [0, -.1, 0], torso: [8, -26, 0], armL: [60, 0, 30], elbowL: 20, armR: [-52, 0, 12], elbowR: 4, wpn: blade([-.05, -.05, 1], [0, -1, 0]), wfx: 1, braid: [10, 0, 0]}, 'i'),
    K(24, {...S_IDLE, torso: [4, -16, 0], armR: [-40, 0, 12], elbowR: 10, wpn: blade([0, -.3, 1], [0, -1, 0]), wfx: .3}), K(30, {...S_IDLE}, 'io')],
    note: '판결의 검: reverse thrust straight behind her at 14 (yaw locked by the pattern)'},
  {name: 'musou', len: 166, events: {appear: 6, raise: 10, arc: 20, dark: 110, slash: 130, end: 160}, keys: [
    K(0, {...S_IDLE, vis: 0}), K(6, {...S_IDLE, vis: 1}, 'o'), K(10, {...S_RAISE, armL: [110, 0, 60], elbowL: 10, wfx: .6}),
    K(20, {...S_RAISE, armR: [178, 0, 2], armL: [120, 0, 70], wpn: blade([0, 1, 0], [-1, 0, 0]), wfx: 1, haloS: 1.15}),
    K(60, {...S_RAISE, armR: [176, 0, 4], armL: [118, 0, 66], wpn: blade([0, 1, .05], [-1, 0, 0]), wfx: .8, haloS: 1.15}, 'io'),
    K(100, {...S_RAISE, armR: [178, 0, 2], armL: [120, 0, 70], wpn: blade([0, 1, 0], [-1, 0, 0]), wfx: 1, haloS: 1.15}, 'io'),
    K(110, {...S_IAI, wfx: .6}), K(126, {...S_IAI, pos: [0, -.2, 0], torso: [-24, 40, 0], kneeR: 48, wfx: 1}, 'io'),
    K(130, {...S_DRAWN, pos: [0, -.18, 0], torso: [-6, -50, 0], wfx: 1}, 'i'), K(150, {...S_DRAWN, pos: [0, -.16, 0], torso: [-6, -50, 0], wfx: .8}),
    K(160, {...S_DRAWN, torso: [-2, -30, 0], wfx: .4}, 'io'), K(166, {...S_IDLE}, 'io')],
    note: '몽상의 일심: embeds the blink-in (appear 6), blade to the sky 10-100, iai 110, giant slash 130'},
  {name: 'guard', len: 20, loop: true, keys: [K(0, {...S_GUARD}), K(10, {...S_GUARD, pos: [0, -.1, 0], torso: [-7, 12, 0], wfx: .3}, 'io'), K(20, {...S_GUARD}, 'io')],
    note: '번개 배리어 stance: blade upright across the front, floor aura on'},
  {name: 'parry', len: 6, events: {flash: 1}, keys: [K(0, {...S_GUARD}), K(1, {...S_GUARD, torso: [-4, 20, 0], wpn: blade([.4, .9, -.3], [-.3, 0, -1]), wfx: 1}, 'o'), K(6, {...S_GUARD}, 'io')],
    note: 'deflect flash at 1; returns to the guard pose'},
  {name: 'counter_sword', len: 46, events: {cue: 0, burst: 12, bolts: 24, lunge: 40}, keys: [
    K(0, {...S_GUARD, wfx: .6}), K(6, {...S_DRAWN, rot: [0, 0, 0], wfx: .8}),
    K(8, {...S_DRAWN, rot: [0, 90, 0], wfx: 1}), K(10, {...S_DRAWN, rot: [0, 180, 0], wfx: 1}), K(12, {...S_DRAWN, rot: [0, 270, 0], wfx: 1}), K(14, {...S_DRAWN, rot: [0, 360, 0], wfx: .8}),
    K(20, {...S_RAISE, rot: [0, 360, 0], wfx: .8}, 'o'), K(24, {...S_CHOP, rot: [0, 360, 0], wpn: blade([0, -.75, -.66], [0, -.66, .75]), wfx: 1}, 'i'),
    K(32, {...S_IAI, rot: [0, 360, 0], wfx: .6}), K(40, {...P_LUNGE, rot: [0, 360, 0], wpn: blade([-.05, -.05, -1], [0, -1, 0]), wfx: 1}, 'i'), K(46, {...S_IDLE, rot: [0, 360, 0]}, 'io')],
    note: 'in-guard counter (sword): spin 6-14 (burst 12), floor bolts 24, lunge 40'},
  {name: 'counter_spear', len: 26, events: {cue: 0, star: 8, sweep: 18}, keys: [
    K(0, {...S_GUARD, wfx: .5}), K(8, {...P_SWEEP_L, wfx: .8}, 'o'), K(14, {...P_SWEEP_L, torso: [-10, 44, 0], wfx: 1}),
    K(18, {...P_SWEEP_R, wfx: 1}, 'i'), K(26, {...P_IDLE}, 'io')], note: 'in-guard counter (polearm): star 8, wide sweep 18'},
  {name: 'karatake', len: 32, events: {retreat: 0, raise: 10, hit: 30}, keys: [
    K(0, {...S_IDLE, pos: [0, -.04, .1], torso: [8, 0, 0], drapeF: 1.3, braid: [10, 0, 0]}), K(10, {...S_RAISE, wfx: .7}, 'o'), K(26, {...S_RAISE, torso: [12, 0, 0], armR: [180, 0, 2], wfx: 1}, 'io'),
    K(30, {...S_CHOP, wfx: 1}, 'i'), K(32, {...S_CHOP, wfx: .6})], note: '카라타케: retreat 0, raise 10, two-handed slash 30'},
  {name: 'switch_sword', len: 34, events: {hoop: 2, vortex: 8, burst: 20, swap: 22}, swap: {22: 'sword'}, keys: [
    K(0, {...S_IDLE}), K(2, {...S_CAST, armL: [160, 0, 10], elbowL: 6, armR: [150, 0, 14]}, 'o'), K(8, {...S_CAST, pos: [0, -.1, 0], armL: [150, 0, 30], armR: [140, 0, 30], kneeL: 16, kneeR: 16}),
    K(18, {...S_CAST, pos: [0, -.16, 0], torso: [-10, 0, 0], armL: [40, 0, 50], armR: [40, 0, 50], kneeL: 26, kneeR: 26, wS: 1}),
    K(20, {...S_IDLE, torso: [10, 0, 0], armL: [70, 0, 80], armR: [70, 0, 80], elbowL: 4, elbowR: 4, wS: .2, haloS: 1.2}, 'o'),
    K(22, {...S_IDLE, torso: [6, 0, 0], armL: [60, 0, 70], armR: [60, 0, 70], wS: 1, wfx: 1}), K(34, {...S_IDLE}, 'io')],
    note: '무기 변경 (검): raise 2 (hoop), vortex 8, burst 20, model swap to the katana 22'},
  {name: 'switch_polearm', len: 32, events: {hoop: 0, burst: 20, swap: 22}, swap: {22: 'polearm'}, keys: [
    K(0, {...S_CAST, armL: [150, 0, 14], elbowL: 6}), K(8, {...S_CAST, pos: [0, -.1, 0], armL: [150, 0, 30], armR: [140, 0, 30], kneeL: 16, kneeR: 16}, 'o'),
    K(18, {...S_CAST, pos: [0, -.16, 0], torso: [-10, 0, 0], armL: [40, 0, 50], armR: [40, 0, 50], kneeL: 26, kneeR: 26}),
    K(20, {...S_IDLE, torso: [10, 0, 0], armL: [70, 0, 80], armR: [70, 0, 80], elbowL: 4, elbowR: 4, wS: .2, haloS: 1.2}, 'o'),
    K(22, {...P_IDLE, torso: [6, 0, 0], armL: [60, 0, 70], wS: 1, wfx: 1}), K(32, {...P_IDLE}, 'io')],
    note: '무기 변경 (창): hoop 0, burst 20, model swap to the polearm 22'},
  {name: 'p_4hit', len: 76, events: {raise: 4, star: 10, h1: 22, h2: 32, h3: 42, h4: 56}, keys: [
    K(0, {...P_IDLE}), K(4, {...P_OVER, wpn: blade([-.3, .3, -.9], [0, 1, 0]), wfx: .5}, 'o'), K(10, {...P_SWEEP_L, wfx: .8}),
    K(16, {...P_SWEEP_L, torso: [-8, 44, 0], wfx: .8}), K(22, {...P_SWEEP_R, wfx: 1}, 'i'), K(27, {...P_SWEEP_R, torso: [-8, -44, 0], wfx: .8}),
    K(32, {...P_SWEEP_L, wfx: 1}, 'i'), K(37, {...P_OVER, wpn: blade([0, .7, .7], [0, -.7, .7]), wfx: .8}),
    K(42, {...S_CHOP, wpn: blade([0, -.3, -.95], [0, -.95, .3]), wfx: 1}, 'i'),
    K(48, {...P_OVER, pos: [0, .25, 0], legL: [30, 0, 6], kneeL: 60, legR: [10, 0, 6], kneeR: 40, wpn: blade([0, .9, .4], [0, .4, -.9]), wfx: 1}, 'o'),
    K(56, {...S_CHOP, pos: [0, -.2, 0], wpn: blade([0, -.36, -.93], [0, -.93, .36]), wfx: 1}, 'i'), K(66, {...S_CHOP, pos: [0, -.18, 0], wfx: .4}), K(76, {...P_IDLE}, 'io')],
    note: '원류 4단: sweeps 22 / 32, chop 42, leaping slam 56 (bolt field 82 is the pattern\'s)'},
  {name: 'p_lance', len: 24, events: {raise: 0, glow: 6, hit: 14}, keys: [
    K(0, {...P_IDLE}), K(6, {...P_OVER, torso: [8, -10, 0], wpn: blade([-.1, .5, -.86], [0, -.86, -.5]), wfx: 1}, 'o'),
    K(14, {...P_LUNGE, wpn: blade([0, -.55, -.84], [0, -.84, .55]), wfx: 1}, 'i'), K(20, {...P_LUNGE, wfx: .4}), K(24, {...P_IDLE}, 'io')],
    note: '원거리 창: raise 0, tip glow 6 (aim lock), lance 14'},
  {name: 'p_twirl_slam', len: 52, events: {twirl: 0, flash: 38, hit: 40}, keys: [
    K(0, {...P_IDLE}), K(4, {...P_OVER, wpn: twirl(0)}, 'o'),
    ...Array.from({length: 11}, (_, i) => K(7 + i * 3, {...P_OVER, wpn: twirl(90 * (i + 1)), wfx: .6})),
    K(38, {...P_OVER, wpn: blade([0, .4, -.9], [0, -.9, -.4]), wfx: 1}),
    K(40, {...S_CHOP, pos: [0, -.22, 0], wpn: blade([0, -.4, -.92], [0, -.92, .4]), wfx: 1}, 'i'), K(46, {...S_CHOP, pos: [0, -.2, 0], wfx: .4}), K(52, {...P_IDLE}, 'io')],
    note: '수천수만의 염원: overhead twirl 4-37 (90 degrees per 3 t), flash 38, slam 40'},
  {name: 'p_twirl_dash', len: 58, events: {twirl: 0, d1: 20, d2: 32, d3: 44}, keys: [
    K(0, {...P_IDLE}), K(3, {...P_OVER, wpn: twirl(0)}, 'o'),
    ...Array.from({length: 4}, (_, i) => K(6 + i * 3, {...P_OVER, wpn: twirl(90 * (i + 1)), wfx: .6})),
    K(17, {...P_SWEEP_L, wpn: blade([.2, .1, 1], [0, -1, 0]), wfx: .8}),
    K(20, {...P_LUNGE, wfx: 1}, 'i'), K(26, {...P_SWEEP_L, wpn: blade([.2, .1, 1], [0, -1, 0]), wfx: .8}),
    K(32, {...P_LUNGE, wfx: 1}, 'i'), K(38, {...P_SWEEP_L, wpn: blade([.2, .1, 1], [0, -1, 0]), wfx: .8}),
    K(44, {...P_LUNGE, wfx: 1}, 'i'), K(50, {...P_LUNGE, wfx: .3}), K(58, {...P_IDLE}, 'io')],
    note: '돌진 3콤보: twirl 3-15, dash thrusts 20 / 32 / 44 (the pattern moves her)'},
  {name: 'p_zigzag', len: 64, events: {hip: 0, star: 8, dash: 14, ring: 34, lunge: 52}, keys: [
    K(0, {...P_SWEEP_L, pos: [0, -.12, 0], wpn: blade([.3, -.2, .93], [0, -1, 0]), wfx: .4}), K(8, {...P_SWEEP_L, pos: [0, -.16, 0], wpn: blade([.3, -.2, .93], [0, -1, 0]), wfx: 1}),
    K(14, {...P_LUNGE, wfx: 1}, 'i'), K(22, {...P_LUNGE, wfx: .6}),
    K(28, {...P_SWEEP_L, rot: [0, 0, 0], wfx: .8}), K(30, {...P_SWEEP_R, rot: [0, 90, 0], wfx: 1}), K(32, {...P_SWEEP_R, rot: [0, 180, 0], wfx: 1}),
    K(34, {...P_SWEEP_R, rot: [0, 270, 0], wfx: 1}), K(36, {...P_SWEEP_R, rot: [0, 360, 0], wfx: .8}),
    K(40, {...KNEEL, rot: [0, 360, 0], pos: [0, -.26, 0], wpn: blade([0, .2, -1], [0, -1, 0]), wfx: 1}, 'o'),
    K(52, {...P_LUNGE, rot: [0, 360, 0], torso: [-10, 0, 0], wpn: blade([0, .5, -.86], [0, .86, .5]), armR: [120, 0, -4], wfx: 1}, 'i'),
    K(58, {...P_LUNGE, rot: [0, 360, 0], wfx: .4}), K(64, {...P_IDLE, rot: [0, 360, 0]}, 'io')],
    note: '번개돌진 콤보: hip 0, star 8, zig-zag dash 14, ring spin 28-36 (ring 34), crouch 40, lunge 52'},
  {name: 'p_rear', len: 36, events: {twirl: 0, h1: 16, h2: 26}, keys: [
    K(0, {...P_IDLE}), K(3, {...P_OVER, wpn: twirl(0)}, 'o'), ...Array.from({length: 3}, (_, i) => K(6 + i * 3, {...P_OVER, wpn: twirl(90 * (i + 1)), wfx: .6})),
    K(16, {...P_SWEEP_L, torso: [-6, 60, 0], wpn: blade([.6, -.1, .8], [0, 0, 1]), wfx: 1}, 'i'), K(21, {...P_SWEEP_L, torso: [-6, 40, 0], wfx: .7}),
    K(26, {...P_SWEEP_R, torso: [-6, -64, 0], wpn: blade([-.6, -.1, .8], [0, 0, 1]), wfx: 1}, 'i'), K(36, {...P_IDLE}, 'io')],
    note: '창 뒤 견제: twirl 3-12, rear sweeps 16 / 26'},
  {name: 'cast', len: 20, events: {cast: 8}, keys: [K(0, {}), K(8, {...S_CAST}, 'o'), K(14, {...S_CAST, armL: [140, 0, 30]}), K(20, {...S_IDLE}, 'io')],
    note: 'cast gesture (eyes, field lightning, blade eyes): left hand raised at 8'},
  {name: 'stagger', len: 60, loopFrom: 20, events: {}, keys: [
    K(0, {}), K(4, {...S_IDLE, torso: [16, 0, -6], head: [18, 0, 8], armL: [-10, 0, 40], armR: [-10, 0, 40], drapeF: 1.2}, 'o'),
    K(12, {...KNEEL, pos: [0, -.3, 0]}, 'i'), K(20, {...KNEEL}), K(40, {...KNEEL, torso: [-27, 0, 4], head: [-20, 0, -4]}, 'io'), K(60, {...KNEEL}, 'io')],
    note: 'stagger 20 t into a 40 t kneeling loop (20-60)'},
  {name: 'stun_recover', len: 24, events: {burst: 24}, keys: [
    K(0, {...KNEEL}), K(10, {...KNEEL, pos: [0, -.2, 0], torso: [-14, 0, 0], kneeR: 70, kneeL: 60}), K(18, {...S_IDLE, pos: [0, -.06, 0], torso: [-10, 0, 0], armL: [20, 0, 30], armR: [20, 0, 30]}, 'io'),
    K(24, {...S_IDLE, torso: [10, 0, 0], armL: [60, 0, 80], armR: [60, 0, 80], wfx: 1, haloS: 1.2}, 'i')],
    note: 'rise from the stagger; recovery burst 24'},
  {name: 'transform', len: 60, events: {rise: 4, ring: 20, pillars: 44, form: 50}, form: 's', formAt: {50: 't'}, keys: [
    K(0, {...S_IDLE}), K(4, {...S_IDLE, torso: [10, 0, 0], head: [10, 0, 0], armL: [30, 0, 40], armR: [30, 0, 40]}, 'o'),
    K(20, {...S_CAST, pos: [0, .8, 0], torso: [-14, 0, 0], head: [-10, 0, 0], armL: [20, 0, 20], armR: [20, 0, 20], elbowL: 40, elbowR: 40, legL: [10, 0, 2], legR: [10, 0, 2], kneeL: 30, kneeR: 30}, 'o'),
    K(40, {...S_CAST, pos: [0, 1, 0], torso: [-4, 0, 0], armL: [150, 0, 30], armR: [150, 0, 30], elbowL: 10, elbowR: 10, legL: [10, 0, 2], legR: [10, 0, 2], kneeL: 20, kneeR: 20}, 'io'),
    K(44, {...S_CAST, pos: [0, 1, 0], torso: [8, 0, 0], armL: [120, 0, 70], armR: [120, 0, 70], elbowL: 4, elbowR: 4, legL: [10, 0, 2], legR: [10, 0, 2], kneeL: 20, kneeR: 20, sS: 1, tS: 0}, 'i'),
    K(49, {...T_IDLE, armL: [90, 0, 80], armR: [90, 0, 80], form: 's', sS: 0, tS: .15}), K(50, {...T_IDLE, armL: [80, 0, 70], armR: [80, 0, 70], tS: .3}),
    K(56, {...T_IDLE, tS: 1}, 'o'), K(60, {...T_IDLE})],
    note: '변신: rise 4-20 (float 1 b), ring 20, pillars 44, the Tenma form appears from 49 (look switch at 50)'},
  {name: 'death', len: 48, form: 'k', keys: [
    K(0, {}), K(4, {...S_IDLE, form: undefined, torso: [18, -3, -7], head: [15, 0, 8], armL: [-12, 0, 34], armR: [-8, 0, 30], elbowL: 16, elbowR: 20, tS: 0, sS: 1, pos: [0, 0, 0]}, 'o'),
    K(14, {...KNEEL, form: undefined, tS: 0, sS: 1}, 'i'), K(30, {...KNEEL, form: undefined, torso: [-46, 0, 6], head: [-30, 0, -6], armL: [70, 0, 10], elbowL: 50, tS: 0, sS: 1}, 'io'),
    K(48, {...KNEEL, form: undefined, torso: [-50, 0, 8], head: [-34, 0, -6], armL: [74, 0, 8], elbowL: 56, armR: [30, 0, 20], tS: 0, sS: 1}, 'io')],
    note: 'death: recoil 4, kneel 14, slump to 48 (the Tenma parts fall away; the look is kept)'},
  // ---- Tenma ----
  {name: 't_idle', len: 60, loop: true, form: 't', keys: [K(0, {...T_IDLE, tBob: 1}), K(30, {...T_IDLE, tBob: 1, rU1: [.5, .82, .26], rU2: [.85, .42, .24], rF2: [.7, .6, -.3],
    gH: [-1.6, .84, -1.0], head: [-4, 4, 0], armL: [14, 0, 24], armR: [10, 0, 20]}, 'io'), K(60, {...T_IDLE, tBob: 1}, 'io')], note: 'float bob +-0.2, arm drift'},
  {name: 't_blink_out', len: 6, form: 't', events: {gone: 4}, keys: [K(0, {}), K(2, {vis: .9, torso: [-10, 0, 0]}), K(4, {vis: 0}, 'i'), K(6, {vis: 0})], note: 'Tenma dissolve, gone 4'},
  {name: 't_blink_in', len: 10, form: 't', events: {appear: 0, settle: 8}, keys: [K(0, {...T_IDLE, vis: 0, torso: [-12, 0, 0]}), K(3, {vis: 1}, 'o'), K(8, {...T_IDLE}, 'io'), K(10, {...T_IDLE})],
    note: 'Tenma reappear (pink streak), settle 8'},
  {name: 't_combo3', len: 70, form: 't', events: {raise: 0, sw1: 14, sw2: 26, cock: 42, throw: 54, reform: 62}, keys: [
    K(0, {...T_IDLE}), K(8, {...T_IDLE, torso: [0, -20, 0], gH: [-2.0, 1.6, -.2], glv: G_HIGH_L, gfx: .6}, 'o'),
    K(14, {...T_IDLE, torso: [0, 20, 0], gH: [.4, .9, -2.0], glv: G_FRONT_R, gfx: 1}, 'i'), K(20, {...T_IDLE, torso: [0, 24, 0], gH: [1.2, 1.0, -1.4], glv: glaive([-.6, .1, .8], [0, 1, 0]), gfx: .6}),
    K(26, {...T_IDLE, torso: [0, -20, 0], gH: [-1.6, .9, -1.8], glv: G_FRONT_L, gfx: 1}, 'i'), K(34, {...T_IDLE, gH: [-1.5, .9, -1.2], glv: G_IDLE, gfx: .4}),
    K(42, {...T_IDLE, torso: [0, -16, 0], gH: [-1.7, 2.2, .4], glv: G_COCK, gfx: 1}, 'o'), K(50, {...T_IDLE, torso: [-4, -20, 0], gH: [-1.8, 2.3, .6], glv: G_COCK, gfx: 1}),
    K(54, {...T_IDLE, torso: [6, 10, 0], gH: [-1.0, 1.4, -1.8], glv: glaive([-.1, -.15, -1], [0, 1, 0]), glvS: 0, gfx: 0}, 'i'),
    K(62, {...T_IDLE, gH: [-1.6, .78, -1.05], glvS: 0}), K(70, {...T_IDLE, glvS: 1}, 'o')],
    note: '백안지륜: sweeps 14 / 26, cock 42, throw 54 (glaive hidden until 62), re-forms 62-70'},
  {name: 't_spin_throw', len: 46, form: 't', events: {glint: 0, spin: 13, throw: 31}, keys: [
    K(0, {...T_IDLE, gfx: .8}), K(5, {...T_IDLE, gH: [-2.2, 1.0, -.2], glv: glaive([1, .05, .3], [0, 1, 0]), gfx: 1}, 'o'),
    K(9, {...T_IDLE, rot: [0, -90, 0], gH: [-2.2, 1.0, -.2], glv: glaive([1, .05, .3], [0, 1, 0]), gfx: 1}), K(13, {...T_IDLE, rot: [0, -180, 0], gH: [-2.2, 1.0, -.2], glv: glaive([1, .05, .3], [0, 1, 0]), gfx: 1}),
    K(17, {...T_IDLE, rot: [0, -270, 0], gH: [-2.2, 1.0, -.2], glv: glaive([1, .05, .3], [0, 1, 0]), gfx: 1}), K(21, {...T_IDLE, rot: [0, -360, 0], gH: [-1.7, 2.2, .4], glv: G_COCK, gfx: 1}),
    K(27, {...T_IDLE, rot: [0, -360, 0], torso: [-4, -18, 0], gH: [-1.8, 2.3, .6], glv: G_COCK, gfx: 1}),
    K(31, {...T_IDLE, rot: [0, -360, 0], torso: [6, 10, 0], gH: [-1.0, 1.4, -1.8], glv: glaive([-.1, -.15, -1], [0, 1, 0]), glvS: 0}, 'i'),
    K(39, {...T_IDLE, rot: [0, -360, 0], glvS: 0}), K(46, {...T_IDLE, rot: [0, -360, 0], glvS: 1}, 'o')],
    note: '초월의 악요개안: glint 0, full spin 5-21 (spin 13), throw 31 (glaive back 39-46)'},
  {name: 't_iai', len: 40, form: 't', events: {crouch: 0, flash: 10, hit: 22}, keys: [
    K(0, {...T_IDLE}), K(10, {...T_IDLE, pos: [0, .7, 0], torso: [-16, -30, 0], kneeL: 50, kneeR: 40, legL: [40, 0, 6], legR: [30, 0, 6], gH: [-1.9, .5, .3], glv: G_SHEATH, gfx: .8}, 'o'),
    K(20, {...T_IDLE, pos: [0, .65, 0], torso: [-20, -34, 0], kneeL: 56, kneeR: 46, legL: [44, 0, 6], legR: [34, 0, 6], gH: [-1.9, .5, .4], glv: G_SHEATH, gfx: 1}),
    K(22, {...T_IDLE, rot: [0, -90, 0], pos: [0, .8, 0], torso: [-6, 20, 0], gH: [.6, .7, -2.2], glv: G_FRONT_R, gfx: 1}, 'i'),
    K(24, {...T_IDLE, rot: [0, -180, 0], pos: [0, .8, 0], torso: [-6, 20, 0], gH: [.6, .7, -2.2], glv: G_FRONT_R, gfx: 1}),
    K(26, {...T_IDLE, rot: [0, -270, 0], pos: [0, .85, 0], torso: [-6, 20, 0], gH: [.6, .7, -2.2], glv: G_FRONT_R, gfx: 1}),
    K(28, {...T_IDLE, rot: [0, -360, 0], pos: [0, .9, 0], torso: [-4, 16, 0], gH: [.2, .8, -2.0], glv: G_FRONT_R, gfx: .6}), K(40, {...T_IDLE, rot: [0, -360, 0]}, 'io')],
    note: '신속한 발도: crouch 0-10, flash 10, the 360 degree draw 22-28 (hit 22)'},
  {name: 't_waves', len: 70, form: 't', events: {glint: 0, swing1: 8, swing2: 53}, keys: [
    K(0, {...T_IDLE, gH: [-1.4, 2.5, -.2], glv: G_UP, gfx: .8}, 'o'), K(4, {...T_IDLE, gH: [-1.2, 2.7, .2], glv: glaive([0, .9, .45], [0, .45, -.9]), gfx: 1}),
    K(8, {...T_IDLE, torso: [-10, 0, 0], gH: [-.9, .6, -1.9], glv: G_SLAM, gfx: 1}, 'i'), K(18, {...T_IDLE, gH: [-1.0, .7, -1.8], glv: G_SLAM, gfx: .4}),
    K(40, {...T_IDLE, torso: [0, -30, 0], gH: [-2.0, .5, .2], glv: G_SHEATH, gfx: .8}, 'io'), K(50, {...T_IDLE, torso: [0, -36, 0], gH: [-2.0, .45, .4], glv: G_SHEATH, gfx: 1}),
    K(53, {...T_IDLE, torso: [0, 24, 0], gH: [.6, .3, -2.1], glv: glaive([-1, -.1, -.5], [0, 1, 0]), gfx: 1}, 'i'), K(62, {...T_IDLE, torso: [0, 10, 0], gH: [-.4, .6, -1.6], glv: G_IDLE, gfx: .3}),
    K(70, {...T_IDLE}, 'io')], note: '궤멸의 검기: glint 0, overhead swing 8 (slabs), low sweep 53 (wave)'},
  {name: 't_danjeol', len: 80, form: 't', events: {halo: 6, raise: 10, band: 24, slam: 64}, keys: [
    K(0, {...T_IDLE}), K(6, {...T_IDLE, disc: [0, 0, 0], head: [6, 0, 0]}), K(10, {...T_IDLE, gH: [-1.4, 1.6, -.6], glv: glaive([.1, .8, -.5], [-1, 0, 0]), gfx: .6}, 'o'),
    K(24, {...T_IDLE, torso: [6, 0, 0], gH: [-1.2, 2.8, .1], glv: G_UP, gfx: 1}, 'io'), K(56, {...T_IDLE, torso: [8, 0, 0], gH: [-1.2, 2.9, .2], glv: glaive([0, 1, .12], [-1, 0, 0]), gfx: 1}, 'io'),
    K(60, {...T_IDLE, torso: [10, 0, 0], gH: [-1.2, 3.0, .35], glv: glaive([0, .9, .4], [-1, 0, 0]), gfx: 1}),
    K(64, {...T_IDLE, torso: [-14, 0, 0], gH: [-.9, .55, -2.0], glv: G_SLAM, gfx: 1}, 'i'), K(72, {...T_IDLE, torso: [-10, 0, 0], gH: [-.9, .6, -1.9], glv: G_SLAM, gfx: .4}),
    K(80, {...T_IDLE}, 'io')], note: '단절: halo 6, raise 10-24, held overhead, slam 64'},
  {name: 't_summon', len: 24, form: 't', events: {sphere: 4, throw: 16}, keys: [
    K(0, {...T_IDLE}), K(4, {...T_IDLE, rU2: [.6, .8, -.1], rF2: [.1, .4, -.9]}, 'o'), K(12, {...T_IDLE, rU2: [.5, .85, .2], rF2: [-.1, .9, .4]}),
    K(16, {...T_IDLE, rU2: [.6, .3, -.75], rF2: [.2, -.1, -1]}, 'i'), K(24, {...T_IDLE}, 'io')], note: '흉장의 수안 (clap): sphere 4, throw 16'},
  {name: 't_seed', len: 20, form: 't', events: {twirl: 0, throw: 8}, keys: [
    K(0, {...T_IDLE, rU3: [.9, .2, .3], rF3: [.3, .9, .3]}, 'o'), K(5, {...T_IDLE, rU3: [.9, .3, .3], rF3: [.2, .8, .5]}),
    K(8, {...T_IDLE, rU3: [.7, -.1, -.7], rF3: [.2, -.3, -.95]}, 'i'), K(20, {...T_IDLE}, 'io')], note: '흉장의 수안 (shadow): twirl 0, throw 8'},
  {name: 't_vajra', len: 30, form: 't', events: {hurl: 6, hurl2: 12, hurl3: 18}, keys: [
    K(0, {...T_IDLE, rU1: [.4, .9, .3], rF1: [.1, .8, .6]}), K(6, {...T_IDLE, rU1: [.6, .6, -.5], rF1: [.4, -.1, -.9], rU2: [.8, .55, .3], rF2: [.4, .8, .45]}, 'i'),
    K(12, {...T_IDLE, rU2: [.7, .2, -.7], rF2: [.4, -.3, -.85], rU3: [.9, .25, .3], rF3: [.5, .7, .5]}, 'i'),
    K(18, {...T_IDLE, rU3: [.8, -.15, -.6], rF3: [.4, -.4, -.8]}, 'i'), K(30, {...T_IDLE}, 'io')], note: '금강괴멸파: the right arms hurl the vajras 6 / 12 / 18'},
  {name: 't_vanish', len: 14, form: 't', events: {gone: 14}, keys: [K(0, {...T_IDLE}), K(8, {...T_IDLE, pos: [0, 1.2, 0], vis: .8, armL: [40, 0, 50], armR: [40, 0, 50]}, 'o'), K(14, {...T_IDLE, pos: [0, 1.3, 0], vis: 0}, 'i')],
    note: '만겁: vanish (gone 14)'},
  {name: 't_reform', len: 20, form: 't', events: {appear: 0}, keys: [K(0, {...T_IDLE, vis: 0, pos: [0, 1.3, 0]}), K(6, {...T_IDLE, vis: 1, pos: [0, 1.15, 0]}, 'o'), K(20, {...T_IDLE}, 'io')],
    note: '만겁: reappear 0'},
  {name: 't_rush', len: 52, form: 't', events: {glint: 0, flash: 13, rush: 23, b1: 28, b2: 34, b3: 40}, keys: [
    K(0, {...T_IDLE, gH: [-2.0, 1.0, .3], glv: G_SHEATH, gfx: .8}, 'o'), K(13, {...T_IDLE, torso: [-10, -20, 0], gH: [-2.1, .9, .5], glv: G_SHEATH, gfx: 1}),
    K(23, {...T_IDLE, pos: [0, .9, -.2], torso: [-22, -10, 0], legL: [-30, 0, 4], legR: [-40, 0, 4], kneeL: 30, kneeR: 40, gH: [-1.4, .7, -2.0], glv: glaive([0, -.05, -1], [0, 1, 0]), gfx: 1}, 'i'),
    K(28, {...T_IDLE, torso: [-6, 26, 0], gH: [.6, .8, -2.1], glv: G_FRONT_R, gfx: 1}, 'i'), K(31, {...T_IDLE, torso: [-6, -10, 0], gH: [-.8, 1.6, -1.2], glv: G_HIGH_L, gfx: .8}),
    K(34, {...T_IDLE, torso: [-6, -26, 0], gH: [-1.6, .8, -2.0], glv: G_FRONT_L, gfx: 1}, 'i'), K(37, {...T_IDLE, torso: [-6, 10, 0], gH: [-.4, 1.7, -1.0], glv: glaive([-.5, .6, -.6], [0, 0, -1]), gfx: .8}),
    K(40, {...T_IDLE, torso: [-6, 26, 0], gH: [.6, .8, -2.1], glv: G_FRONT_R, gfx: 1}, 'i'), K(46, {...T_IDLE, gfx: .3}), K(52, {...T_IDLE}, 'io')],
    note: '강력한 돌진: glint 0, flash 13, rush 23 (the pattern moves her), barrage 28 / 34 / 40'},
  {name: 't_collapse', len: 46, form: 't', formAt: {20: 's'}, events: {form: 20, kneel: 46}, keys: [
    K(0, {...T_IDLE}), K(8, {...T_IDLE, torso: [16, 0, 6], head: [16, 0, 6], armL: [-10, 0, 40], armR: [-10, 0, 40], tS: .9}, 'o'),
    K(19, {...T_IDLE, form: 't', pos: [0, .12, 0], torso: [-20, 0, 0], tS: 0, sS: 0, glvS: 1}, 'i'),
    K(20, {...KNEEL, form: 's', pos: [0, .05, 0], tS: 0, sS: 0, wS: 0}), K(28, {...KNEEL, tS: 0, sS: 1, wS: 1}, 'o'), K(46, {...KNEEL, tS: 0, sS: 1})],
    note: 'armour broken: the puppet falls away, she drops and the Shogun look returns at 20, kneels 46'},
  {name: 'exhausted', len: 60, loop: true, keys: [K(0, {...KNEEL}), K(30, {...KNEEL, pos: [0, -.35, 0], torso: [-27, 0, 4], head: [-19, 0, -4], armL: [66, 4, 18]}, 'io'), K(60, {...KNEEL}, 'io')],
    note: 'kneeling, breathing'},
  {name: 'recover', len: 28, keys: [K(0, {...KNEEL}), K(8, {...KNEEL, pos: [0, -.28, 0], torso: [-44, 0, 2], head: [-8, 0, 0]}), K(16, {...KNEEL, pos: [0, -.14, 0], torso: [-22, 0, 0], kneeR: 54, kneeL: 48, legR: [28, 0, -4], legL: [10, 0, 4]}, 'io'),
    K(28, {...S_IDLE}, 'io')], note: 'stands up from the kneel'},
];
CLIPS.forEach((c, i) => { c.id = i; c.form = c.form || 's'; c.events = c.events || {}; });
export const CLIP_BY_NAME = Object.fromEntries(CLIPS.map(c => [c.name, c]));
// The binding event table (plan §C.5): the builder asserts every clip's events against it.
export const C5 = {
  idle_sword: [40, {}], idle_polearm: [40, {}], blink_out: [6, {gone: 4}], blink_in: [10, {appear: 0, settle: 8}],
  iai_dash: [36, {stance: 0, flash: 6, hit1: 18, hit2: 24}], iai_near: [28, {raise: 0, flash: 10, hit1: 22, hit2: 28}],
  combo5: [74, {cue: 0, s1: 12, s2: 22, s3: 34, s4: 50, s5: 64}], disc_cast: [40, {cue: 0, d1: 6, d2: 10, d3: 18, wave: 34}],
  rear_iai: [30, {cue: 0, hit: 14}], musou: [166, {appear: 6, raise: 10, arc: 20, dark: 110, slash: 130, end: 160}],
  guard: [20, {}], parry: [6, {flash: 1}], counter_sword: [46, {cue: 0, burst: 12, bolts: 24, lunge: 40}],
  counter_spear: [26, {cue: 0, star: 8, sweep: 18}], karatake: [32, {retreat: 0, raise: 10, hit: 30}],
  switch_sword: [34, {hoop: 2, vortex: 8, burst: 20, swap: 22}], switch_polearm: [32, {hoop: 0, burst: 20, swap: 22}],
  p_4hit: [76, {raise: 4, star: 10, h1: 22, h2: 32, h3: 42, h4: 56}], p_lance: [24, {raise: 0, glow: 6, hit: 14}],
  p_twirl_slam: [52, {twirl: 0, flash: 38, hit: 40}], p_twirl_dash: [58, {twirl: 0, d1: 20, d2: 32, d3: 44}],
  p_zigzag: [64, {hip: 0, star: 8, dash: 14, ring: 34, lunge: 52}], p_rear: [36, {twirl: 0, h1: 16, h2: 26}], cast: [20, {cast: 8}],
  stagger: [60, {}], stun_recover: [24, {burst: 24}], transform: [60, {rise: 4, ring: 20, pillars: 44, form: 50}], death: [48, {}],
  t_idle: [60, {}], t_blink_out: [6, {gone: 4}], t_blink_in: [10, {appear: 0, settle: 8}],
  t_combo3: [70, {raise: 0, sw1: 14, sw2: 26, cock: 42, throw: 54, reform: 62}], t_spin_throw: [46, {glint: 0, spin: 13, throw: 31}],
  t_iai: [40, {crouch: 0, flash: 10, hit: 22}], t_waves: [70, {glint: 0, swing1: 8, swing2: 53}], t_danjeol: [80, {halo: 6, raise: 10, band: 24, slam: 64}],
  t_summon: [24, {sphere: 4, throw: 16}], t_seed: [20, {twirl: 0, throw: 8}], t_vajra: [30, {hurl: 6, hurl2: 12, hurl3: 18}],
  t_vanish: [14, {gone: 14}], t_reform: [20, {appear: 0}], t_rush: [52, {glint: 0, flash: 13, rush: 23, b1: 28, b2: 34, b3: 40}],
  t_collapse: [46, {form: 20, kneel: 46}], exhausted: [60, {}], recover: [28, {}],
};
// Clips that stay on (the runtime wraps them): loop = whole clip, loopFrom = from that tick (stagger 20 + 40 L).
export const loopStart = c => (c.loop ? 0 : c.loopFrom ?? null);

// ---- sampling ------------------------------------------------------------------------------------------------------------
const clean = pose => Object.fromEntries(Object.entries(pose).filter(([, v]) => v !== undefined));
export const accumulate = clip => accumulateLib({...clip, keys: clip.keys.map(([t, p, e]) => [t, clean(p), e])}, DEFAULT_POSE);
// loop phase for the bob channels: one cycle per loop (looping clips), none elsewhere
const phase = (clip, t) => (clip.loop ? (t % clip.len) / clip.len : clip.loopFrom != null && t >= clip.loopFrom ? (t - clip.loopFrom) / (clip.len - clip.loopFrom) : 0);
export const sampleClip = (clip, t, ks) => sampleLib(clip, t, ks, {defaults: DEFAULT_POSE, discrete: DISCRETE, phase});
export const restPose = which => ({...DEFAULT_POSE, ...clean(which === 't' ? {...T_IDLE} : {...S_IDLE})});
