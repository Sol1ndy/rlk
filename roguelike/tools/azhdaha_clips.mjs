// Clips of the 야타용왕 (Azhdaha) rig (stage R1 stub): DEFAULT_POSE (the idle stance, head low, model.md §1.2) and a
// set of static debug poses for the model renders and the bounds checks. The motion clips of motion.md §6 come in a
// later stage; their format is the shared one (mboss_rig_clips.mjs): {name, len, loop?, next?, blend?, keys: [[tick,
// sparse pose, ease]], events, note}. Channels: azhdaha_pose.mjs. The clip carries no horizontal root travel and no
// root yaw (the module moves and turns the anchor).
import {accumulate as acc, sampleClip as sampleShared, applyRetime} from './mboss_rig_clips.mjs';
import {J} from './azhdaha_pose.mjs';

const mx = v => [-v[0], v[1], v[2]];
// Tail helpers: per-segment UP angles (deg, + raises the segment; negative pitch internally) -> t1..t8 channels.
export const tailUp = (ups, yaw = [], roll = []) => Object.fromEntries(ups.map((u, i) => ['t' + (i + 1), [-u, yaw[i] || 0, roll[i] || 0]]));
// Paired limb targets: the left value and its mirror for the right ([x, y, z] -> [-x, y, z]; eulers [p, y, r] -> [p, -y, -r]).
export const fore = (w, e = [0, 0, 0], wr = null, er = null) => ({fwL: w, fpL: e, fwR: wr || mx(w), fpR: er || [e[0], -e[1], -e[2]]});
export const hind = (h, e = [0, 0, 0], hr = null, er = null) => ({hkL: h, hfL: e, hkR: hr || mx(h), hfR: er || [e[0], -e[1], -e[2]]});

// Idle stance (model.md §1.2 / §2): head carried low (snout 0.85 b, crest 2.65 b), fore columns at x +-3.15,
// wheelbase 5.0 b, the tail rising behind the rump in a high curl with the leafy tip hanging forward (motion.md §5.1).
// Tail curls (per-segment up angles, the tail region's constants; R2 critique 5.1-5.3, 5.7, 1.9). Bends of 25-30
// degrees are covered by the segment collars and the overlapping flank plates.
// TAIL_REST: the idle carry, a big arc rising from the rump, back and over, the leafy tip forward over the mid-back at
// ~10 b (v3 23.6 s, v3 f1365, v1 idle front: the "tree" above the plates).
export const TAIL_REST = [22, 25, 27, 28, 27, 25, 23, 21];
// TAIL_LOOP: the phase-3 loop / shells carry (v8 f2280 trace: top 11.3-11.8 b, rear z ~9, the tip over the shoulders).
export const TAIL_LOOP = [29, 28, 29, 29, 26, 22, 19, 18];
// TAIL_LOW: laid out behind, the branch just off the floor (v3 f1680); TAIL_WHIP: flat on the floor for the sweep.
export const TAIL_LOW = [-8, -6, -2, 4, 7, 5, 3, 1];
export const TAIL_WHIP = [-9, -10, 1, 6, 9, 4, 0, -3];
// TAIL_PILLAR: the tail-only pillar. The root pose (TAIL_PILLAR_ROOT) pitches the buried body nose-down 90 degrees
// so the tail rises at the anchor's x / z (critique 1.9), the root 4 b under the floor; a slight S, the crown nodding.
export const TAIL_PILLAR = [0, -6, -6, -2, 4, 8, 12, 16];
export const TAIL_PILLAR_ROOT = {pos: [0, -11.15, 0], rot: [-90, 0, 0]};
export const DEFAULT_POSE = {
  pos: [0, 0, 0], rot: [0, 0, 0],
  pelvis: [0, 0, 0], spine: [0, 0, 0], chest: [0, 0, 0], neck1: [0, 0, 0], neck2: [0, 0, 0], head: [0, 0, 0], jaw: 0,
  beard1: [0, 0, 0], beard2: [0, 0, 0], apron: [0, 0, 0],
  flN: 0, flS: 0, flM: 0, flH: 0, flK: 1,
  ...fore(J.wrist), ...hind(J.hock),
  ...tailUp(TAIL_REST), tLift: 0, tCurl: 0, tSweep: 0, tTwist: 0,
  vis: 1, visBody: 1, visTail: 1,
};
const pose = (name, len, p, note, extra = {}) => ({name, len, loop: true, keys: [[0, p], [len, {}]], events: {}, note, ...extra});

// Debug poses (static, 2-tick loops): the shapes the patterns need, for renders and checkBounds on every pose.
export const CLIPS = [
  pose('rest', 2, {}, 'DEFAULT_POSE: the idle stance, head low'),
  pose('head_up', 2, {neck1: [42, 0, 0], neck2: [16, 0, 0], head: [-38, 0, 0], jaw: 6}, 'head raised (walk, v1 f2130): the neck up, the face still forward, eyes about 3 b'),
  pose('roar', 2, {neck1: [8, 0, 0], neck2: [6, 0, 0], head: [18, 0, 0], jaw: 45, beard1: [-12, 0, 0]}, 'low roar: jaw 45, head thrust up (the portrait)'),
  pose('rear_up', 2, {pos: [0, -.1, 0], pelvis: [45, 0, 0], spine: [6, 0, 0], chest: [4, 0, 0], neck1: [-10, 0, 0], neck2: [5, 0, 0], head: [22, 0, 0], jaw: 40,
    apron: [-18, 0, 0], beard1: [-15, 0, 0], beard2: [-10, 0, 0], flS: 10, flM: 8,
    ...fore([2.9, 6.6, -4.6], [-55, 0, 0]), ...tailUp([36, 6, 4, 0, 0, 6, 12, 18])}, 'rear-up roar peak (roar_rear t20, chin_slam t30): pelvis +45, fore paws at chest height'),
  pose('stomp_lift', 2, {pelvis: [3, 0, 0], spine: [2, 0, 4], chest: [6, 0, 10], neck1: [0, -6, 0], head: [0, -10, 0],
    ...fore([3.45, 2.4, -2.75], [-30, 0, 0], [-3.15, .5, -2.4], [0, 0, 0])}, 'stomp_fl hang (t15): the front rises (pelvis +3, chest +6) and rolls away, the left elbow high, the bracer a hanging column (18 deg from vertical), wrist 2.4 b, claws curled; weight on the right'),
  pose('whip_mid', 2, {pos: [0, -.2, 0], chest: [0, 12, 0], spine: [0, 6, 0], pelvis: [0, -6, 0], head: [0, 10, 0],
    ...tailUp(TAIL_WHIP), tSweep: 110}, 'tail whip mid-sweep: the tail flat on the floor, swept 110 to the left (root-weighted)'),
  pose('loop', 2, {...tailUp(TAIL_LOOP)}, 'phase-3 tail loop over the back (v8 f2280 / v7 f0600 silhouette)'),
  pose('tail_low', 2, {...tailUp(TAIL_LOW)}, 'the tail laid out behind (v3 f1680): the leafy branch near the floor'),
  pose('burrow', 2, {pos: [0, -3.4, 0], rot: [-22, 0, 0], head: [-15, 0, 0], ...tailUp([-10, -5, 0, 0, 5, 5, 5, 5]), flS: 6, flM: 6}, 'burrow dive mid-sink: root -3.4, nose down 22; the opaque floor hides the buried part'),
  pose('burrowed', 2, {pos: [0, -7.5, 0], visBody: 0, visTail: 0}, 'underground (burrow_travel): root -7.5, every part at scale 0', {state: 'burrowed'}),
  pose('tail_only', 2, {...TAIL_PILLAR_ROOT, visBody: 0, ...tailUp(TAIL_PILLAR)}, 'phase-3 tail-only state: the body pitched nose-down 90 and sunk, the tail a pillar rising at the anchor, the body at scale 0', {state: 'tail_only'}),
];
// RETIME table (authored -> played ticks), empty in R1.
export const RETIME = {};
applyRetime(CLIPS, RETIME);
export const accumulate = clip => acc(clip, DEFAULT_POSE);
export const sampleClip = (clip, t, ks) => sampleShared(clip, t, ks, {defaults: DEFAULT_POSE});
export const restPose = () => structuredClone(DEFAULT_POSE);

// ---- legs (R2) -----------------------------------------------------------------------------------------------------------
// The limb targets are root-frame, so the debug poses that dip the root (rear_up -0.1, whip_mid -0.2) lift their planted
// targets by the dip to keep the paws and feet on the floor (r1_critique §1.2: they sank 0.15-0.25 b). Motion clips
// that dip the root need the same compensation.
const plantedAt = dy => ({...fore([J.wrist[0], J.wrist[1] + dy, J.wrist[2]]), ...hind([J.hock[0], J.hock[1] + dy, J.hock[2]])});
for (const [name, dy, chans] of [['rear_up', .1, ['hkL', 'hkR']], ['whip_mid', .2, ['fwL', 'fwR', 'hkL', 'hkR']]]) {
  const c = CLIPS.find(x => x.name === name), k = c && c.keys[0][1], P = plantedAt(dy);
  if (k) for (const ch of chans) if (!(ch in k)) k[ch] = P[ch];
}
