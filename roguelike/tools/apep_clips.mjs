// Clips of the 아펩의 오아시스 파수꾼 rig (stage AP-R1 block-out): DEFAULT_POSE (= the CROUCH stance, the bind pose),
// the two stance rest poses (STANCES), the binding clip table of ap_contract.md §0.4.10 (names, lengths, authored
// lengths, RETIME knots, events, hidden spans, stances, px sets, look / hand events, yaw knots, required anchors and
// tracks: CLIP_TABLE, copied from the AP-SPEC stub, never re-ticked without a change note) and the R1 STUB motion of
// every clip: the stance it starts in, the stance blends of stand_p3 / crouch_p3 (and of the clips that fold or rise),
// the burrow sinks (follow_y offsets) and the hidden spans. AP-RC1 replaces the stub keys with the real motion (motion.md,
// plan §6.2 P3 pose glossary); the format is the shared one (mboss_rig_clips.mjs): {name, len, loop?, next?, blend?,
// keys: [[tick, sparse pose, ease]], events, note} + the Apep fields of the table.
// Channels: apep_pose.mjs. No horizontal root travel and no root yaw (the module moves and turns the anchor, R16).
import {accumulate as acc, sampleClip as sampleShared} from './mboss_rig_clips.mjs';
import {J, LIMB_C, SIDES, LIMBS, BONES, mirrorE, solve, eulerOf} from './apep_pose.mjs';

const mx = v => [-v[0], v[1], v[2]];
const Z3 = [0, 0, 0];
// ---- DEFAULT_POSE = CROUCH: every euler 0 (the bind pose), the planted hands by IK on their bind wrists ---------------
export const DEFAULT_POSE = {pos: [0, 0, 0], rot: [0, 0, 0], pelT: [0, 0, 0], vis: 1, tLift: 0, tCurl: 0, tSweep: 0, tTwist: 0};
for (const b of BONES) if (b.name !== 'root') DEFAULT_POSE[b.name] = [0, 0, 0];
for (const s of SIDES) for (const L of LIMBS) {
  const k = `${L}_${s}`;
  Object.assign(DEFAULT_POSE, {['ik_' + k]: 1, ['tg_' + k]: (s === 'l' ? LIMB_C[L][2] : mx(LIMB_C[L][2])).slice(), ['hf_' + k]: [0, 0, 0], ['bn_' + k]: 0});
}
// Left-side channels -> both sides (the right mirrors: eulers [p, -y, -r], points [-x, y, z]).
export function both(p) {
  const o = {...p};
  for (const [k, v] of Object.entries(p)) {
    const r = k.replace(/_l(_|$)/, '_r$1');
    if (r === k || k in o && r in p) continue;
    if (/^tg_/.test(k)) o[r] = mx(v);
    else if (Array.isArray(v) && v.length === 3) o[r] = mirrorE(v);
    else o[r] = v;
  }
  return o;
}
// ---- the stance rest poses (plan R3; UPRIGHT fitted to model_p3 §6.2 by joint angles only, residuals in the builder) ----
const UPRIGHT_L = {
  pelT: [0, 0.31, -0.93],
  pelvis: [65.5, 0, 0],
  abdomen: [-1.5, 0, 0],
  hem_a: [-60.5, 0, 0],
  hem_b: [48.5, 0, 0],
  chest: [13.5, 0, 0],
  shoulders: [-46, 0, 0],
  neck: [42.5, 0, 0],
  head: [-52, 0, 0],
  hood_hinge: [84, 0, 0],
  tail_1: [-67, -1.5, 0],
  tail_2: [-33.5, 3.5, 0],
  tail_3: [8.5, 30, 0],
  tail_4: [8, 11, 0],
  tail_5: [-8.5, 21.5, 0],
  tail_6: [-18.5, 33, 0],
  tail_7: [-15.5, 39, 0],
  tail_tip: [-10.5, 28.5, 0],
  hair_l_1: [-88, -17, -2.5],
  hair_l_2: [-26.5, -1, 9.5],
  mantle_l_a: [34.5, -37, -18],
  mantle_l_b: [0, 6, 3],
  clav_a_l: [-15, 20.5, 46],
  a_up_l: [4.5, -18, 34],
  a_lo_l: [9.5, -2.5, 22.5],
  a_hand_l: [8, 9.5, -1.5],
  b_up_l: [6, -31, 20.5],
  b_lo_l: [32, -29.5, 37],
  b_hand_l: [-18, -1.5, -3],
  c_up_l: [-15, 23, -23.5],
  c_lo_l: [-40.5, 1.5, 8.5],
  c_hand_l: [17, 3.5, -2],
  ik_a_l: 0, ik_b_l: 0, ik_c_l: 0,
};
export const STANCES = {CROUCH: structuredClone(DEFAULT_POSE), UPRIGHT: {...structuredClone(DEFAULT_POSE), ...both(UPRIGHT_L)}};
export const STANCE_FORM_REF = {CROUCH: 'p1', UPRIGHT: 'p3'};
// The phase-3 crawl (CROUCH with the p3 looks, plan R1): the CROUCH pose with each IK hand turned to its UPRIGHT world
// orientation, so the P3 hand models (authored as they sit in the UPRIGHT stance) show as authored on the crawl's wrists.
{
  const oU = solve(STANCES.UPRIGHT), hf = {};
  for (const s of SIDES) for (const L of LIMBS) hf[`hf_${L}_${s}`] = eulerOf(oU[`${L}_hand_${s}`].R);
  STANCES.CRAWL = {...structuredClone(STANCES.CROUCH), ...hf};
}
// The camera fallback of plan R1 (pose only, never rescaled bones): thorax 10 deg back, waist lowered (hood ~ 8.0).
export const UPRIGHT_LOW = {...STANCES.UPRIGHT, pelT: [0, .03, -.91], chest: [3.5, 0, 0]};

export const CLIP_TABLE = [
  {name: 'entrance_p1', form: 'p1', len: 110, authored: 110, loop: false, next: 'idle_p1', events: {'pool': 0, 'hood': 16, 'reach': 31, 'touch': 47, 'flash': 60, 'embers': 63, 'heart_up': 70, 'crouch': 91, 'roar': 100, 'end': 110}, hidden: [[0, 3]], stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'inv'], [110, 'p1']], look_events: [[0, 'tint', 'p1_dark'], [30, 'tint', 'none']], hand_events: [[31, 'a_hand_r', 'p1_raised'], [91, 'a_hand_r', 'p1_planted']], state: [[0, 'burrowed'], [4, 'normal']], anchors: {'touch': ['hand_a_r']}},
  {name: 'idle_p1', form: 'p1', len: 60, authored: 60, loop: true, next: null, events: {}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']]},
  {name: 'turn_p1', form: 'p1', len: 20, authored: 20, loop: true, next: null, events: {'step_1': 0, 'step_2': 5, 'step_3': 10, 'step_4': 15}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']]},
  {name: 'turn_p1_step', form: 'p1', len: 10, authored: 10, loop: false, next: 'idle_p1', events: {'step_1': 0, 'step_2': 5}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']], yaw: {knots: [[0, 0], [9, -90]], ease: 'smooth'}},
  {name: 'crawl_p1', form: 'p1', len: 16, authored: 16, loop: true, next: null, events: {'stepA': 0, 'stepB': 8}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']], hand_events: [[0, 'b_hand_l', 'p1_curl'], [0, 'c_hand_r', 'p1_curl'], [0, 'b_hand_r', 'p1_open'], [0, 'c_hand_l', 'p1_open'], [8, 'b_hand_l', 'p1_open'], [8, 'c_hand_r', 'p1_open'], [8, 'b_hand_r', 'p1_curl'], [8, 'c_hand_l', 'p1_curl']]},
  {name: 'crawl_stop_p1', form: 'p1', len: 32, authored: 32, loop: false, next: 'idle_p1', events: {'plant': 8, 'open': 16, 'end': 32}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']], hand_events: [[8, 'p1_rest']]},
  {name: 'walk_p1', form: 'p1', len: 36, authored: 36, loop: true, next: null, events: {'step_1': 0, 'step_2': 9, 'step_3': 18, 'step_4': 27}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']]},
  {name: 'burrow_strike', form: 'p1', len: 82, authored: 94, loop: false, next: 'idle_p1', retime: [[0, 0], [28, 22], [50, 44], [76, 64], [94, 82]], events: {'tell': 0, 'dive': 4, 'inv': 6, 'sink': 8, 'hide': 22, 'travel': 23, 'lock': 32, 'burst': 44, 'rise': 49, 'loom': 52, 'yawlock': 52, 'sweep': 64, 'sweep_end': 71, 'land': 77, 'end': 82}, hidden: [[22, 43]], stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1'], [6, 'burrowed'], [44, 'p1']], look_events: [[6, 'tint', 'p1_dark'], [44, 'tint', 'none']], state: [[22, 'burrowed'], [44, 'normal']], anchors: {'burst': ['impact']}},
  {name: 'sink_p1', form: 'p1', len: 17, authored: 18, loop: false, next: null, retime: [[0, 0], [5, 4], [18, 17]], events: {'tell': 0, 'sink': 4, 'chunks': 8, 'hide': 14}, hidden: [[14, 16]], stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1'], [4, 'burrowed']], look_events: [[4, 'tint', 'p1_brown']], state: [[14, 'burrowed']]},
  {name: 'emerge_on_p1', form: 'p1', len: 24, authored: 24, loop: false, next: 'rotation', events: {'show': 1, 'solid': 4, 'settle': 12, 'end': 24}, hidden: [[0, 0]], stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'burrowed'], [4, 'p1']], look_events: [[1, 'tint', 'none']], state: [[0, 'burrowed'], [1, 'normal']], scale_in: [1, 4, 0.85]},
  {name: 'burrow_in_p1', form: 'p1', len: 23, authored: 30, loop: false, next: null, retime: [[0, 0], [30, 23]], events: {'tell': 0, 'inv': 5, 'dive': 5, 'sink': 6, 'hide': 21}, hidden: [[21, 22]], stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1'], [5, 'burrowed']], look_events: [[6, 'tint', 'p1_dark']], state: [[21, 'burrowed']]},
  {name: 'emerge_crown_p1', form: 'p1', len: 40, authored: 40, loop: false, next: 'idle_p1', events: {'glow': 0, 'crown': 5, 'hood': 10, 'targetable': 11, 'out': 21, 'end': 40}, hidden: [[0, 4]], stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'burrowed'], [11, 'p1']], look_events: [[5, 'tint', 'p1_dark'], [20, 'tint', 'none']], state: [[0, 'burrowed'], [5, 'normal']]},
  {name: 'hands', form: 'p1', len: 140, authored: 160, loop: false, next: 'idle_p1', retime: [[0, 0], [40, 30], [82, 62], [102, 82], [160, 140]], events: {'spread': 0, 'swirl': 5, 'raise': 27, 'plunge': 30, 'lock': 33, 'legs': 36, 'lines': 40, 'slam1': 62, 'slam2': 69, 'slam3': 75, 'slam4': 82, 'sink': 83, 'stand': 100, 'pull': 108, 'flower': 118, 'fold': 128, 'end': 140}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']], anchors: {'plunge': ['impact']}, yaw: {knots: [[5, 0], [27, 360]], ease: 'smooth'}},
  {name: 'glow_slams', form: 'p1', len: 131, authored: 160, loop: false, next: 'idle_p1', retime: [[0, 0], [48, 36], [59, 47], [89, 70], [130, 101], [160, 131]], events: {'wind': 0, 'coil': 23, 'column': 36, 'slam1': 47, 'rear2': 65, 'slam2': 70, 'leap': 77, 'apex': 83, 'dive': 90, 'slam3': 101, 'settle': 121, 'end': 131}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']], look_events: [[0, 'core_glow', 'lit'], [47, 'core_glow', 'idle']], anchors: {'slam1': ['impact'], 'slam2': ['impact'], 'slam3': ['impact']}},
  {name: 'rotation', form: 'p1', len: 130, authored: 135, loop: false, next: 'idle_p1', retime: [[0, 0], [21, 16], [135, 130]], events: {'arms': 0, 'rear': 10, 'disc': 16, 'full': 39, 'crash': 40, 'spin': 47, 'flash': 57, 'spin_end': 71, 'rise': 85, 'stand': 100, 'end': 130}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']], anchors: {'crash': ['impact']}, yaw: {knots: [[47, 0], [71, 360]], ease: 'smooth'}},
  {name: 'tail_p1x2', form: 'p1', len: 127, authored: 141, loop: false, next: 'idle_p1', retime: [[0, 0], [37, 28], [46, 37], [66, 52], [73, 59], [141, 127]], events: {'turn': 0, 'raise': 8, 'cock': 23, 'swing1': 28, 'end1': 37, 'cock2': 48, 'swing2': 52, 'end2': 59, 'rise': 86, 'end': 127}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']], anchors: {'cock': ['tail_tip'], 'swing1': ['tail_root'], 'swing2': ['tail_root']}, tracks: ['tail_root', 'tail_tip'], yaw: {knots: [[27, 0], [35, 200], [51, 200], [59, 0]], ease: 'linear'}},
  {name: 'combo_a', form: 'p1', len: 29, authored: 29, loop: false, next: null, events: {'tell': 0, 'swing': 10, 'hit': 14}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']], anchors: {'hit': ['impact']}},
  {name: 'combo_b', form: 'p1', len: 44, authored: 48, loop: false, next: null, retime: [[0, 0], [18, 14], [48, 44]], events: {'rear': 0, 'high': 12, 'slam': 17}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']], anchors: {'slam': ['impact']}},
  {name: 'combo_c', form: 'p1', len: 20, authored: 20, loop: false, next: null, events: {'twist': 0, 'spin': 5, 'hit': 10}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']], anchors: {'hit': ['impact']}, yaw: {knots: [[5, 0], [15, 360]], ease: 'smooth'}},
  {name: 'combo_d', form: 'p1', len: 77, authored: 84, loop: false, next: null, retime: [[0, 0], [29, 22], [84, 77]], events: {'rear': 0, 'tall': 20, 'lunge': 22, 'slam': 27, 'recover': 43}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']], anchors: {'slam': ['impact']}},
  {name: 'combo_end', form: 'p1', len: 20, authored: 20, loop: false, next: 'idle_p1', events: {}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1']]},
  {name: 'sink_revive', form: 'p1', len: 60, authored: 60, loop: false, next: null, events: {'stagger': 0, 'flicker': 4, 'sink': 20, 'chunks': 30, 'hide': 45, 'park': 46, 'end': 60}, hidden: [[45, 59]], stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p1'], [6, 'burrowed'], [46, 'parked']], look_events: [[20, 'tint', 'p1_brown']], state: [[45, 'burrowed']]},
  {name: 'revival', form: 'p3', len: 160, authored: 160, loop: false, next: 'idle_p3', events: {'burst': 60, 'splash': 60, 'reach': 88, 'flash2': 96, 'reveal': 100, 'end': 160}, hidden: [[0, 59]], stance: ['UPRIGHT', 'UPRIGHT'], px_sets: [[0, 'inv'], [118, 'p3u']], look_events: [[0, 'form', 'p3'], [0, 'face', 'p3_idle'], [0, 'core', 'p3_sternum'], [0, 'tint', 'none']], hand_events: [[104, 'p3_open']], state: [[0, 'burrowed'], [60, 'normal']], blend_out: 6},
  {name: 'idle_p3', form: 'p3', len: 60, authored: 60, loop: true, next: null, events: {}, stance: ['UPRIGHT', 'UPRIGHT'], px_sets: [[0, 'p3u']]},
  {name: 'turn_p3', form: 'p3', len: 20, authored: 20, loop: true, next: null, events: {'step_1': 0, 'step_2': 5, 'step_3': 10, 'step_4': 15}, stance: ['UPRIGHT', 'UPRIGHT'], px_sets: [[0, 'p3u']], yaw: {knots: [[0, 0], [19, 114]], ease: 'linear'}},
  {name: 'walk_p3', form: 'p3', len: 32, authored: 32, loop: true, next: null, events: {'step_1': 0, 'step_2': 8, 'step_3': 16, 'step_4': 24}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'p3c']]},
  {name: 'crouch_p3', form: 'p3', len: 8, authored: 8, loop: false, next: null, events: {'closed': 6, 'end': 8}, stance: ['UPRIGHT', 'CROUCH'], stance_events: [[7, 'CROUCH']], px_sets: [[0, 'p3u'], [6, 'p3c']], look_events: [[6, 'face', 'hidden']], hand_events: [[2, 'p3_curl']]},
  {name: 'stand_p3', form: 'p3', len: 14, authored: 14, loop: false, next: 'idle_p3', events: {'open': 10, 'end': 14}, stance: ['CROUCH', 'UPRIGHT'], stance_events: [[13, 'UPRIGHT']], px_sets: [[0, 'p3c'], [10, 'p3u']], look_events: [[4, 'face', 'p3_idle']], hand_events: [[5, 'b_hand_l', 'p3_open'], [8, 'b_hand_r', 'p3_open'], [8, 'p3_open']]},
  {name: 'move_strike_p3', form: 'p3', len: 92, authored: 100, loop: false, next: 'idle_p3', retime: [[0, 0], [22, 16], [52, 44], [100, 92]], events: {'fold': 0, 'mound': 8, 'inv': 8, 'hide': 16, 'trail': 16, 'lock': 32, 'show': 42, 'burst': 44, 'hoop': 44, 'roll': 49, 'slam': 61, 'tail': 65, 'sweep': 69, 'rise': 71, 'stand': 85, 'end': 92}, hidden: [[16, 41]], stance: ['UPRIGHT', 'UPRIGHT'], stance_events: [[7, 'CROUCH'], [91, 'UPRIGHT']], px_sets: [[0, 'p3u'], [8, 'burrowed'], [44, 'p3c'], [85, 'p3u']], look_events: [[6, 'face', 'hidden'], [89, 'face', 'p3_idle']], hand_events: [[2, 'p3_curl'], [90, 'p3_open']], state: [[16, 'burrowed'], [42, 'normal']], keyed_pitch: [49, 61], anchors: {'burst': ['impact'], 'slam': ['impact'], 'sweep': ['tail_root']}, tracks: ['tail_root', 'tail_tip'], yaw: {knots: [[66, 0], [72, 360]], ease: 'linear'}},
  {name: 'aftermath', form: 'p3', len: 224, authored: 240, loop: false, next: 'idle_p3', retime: [[0, 0], [52, 40], [84, 68], [172, 156], [240, 224]], events: {'charge': 0, 'whirl': 18, 'land': 40, 'field': 40, 'pillar1': 44, 'pillar2': 48, 'pillar3': 52, 'dome1': 54, 'dome2': 58, 'dome3': 62, 'rise': 76, 'ticks': 80, 'aloft': 84, 'rain': 134, 'blast': 156, 'descend': 162, 'window_end': 176, 'pop': 189, 'burst': 190, 'end': 224}, stance: ['CROUCH', 'UPRIGHT'], stance_events: [[84, 'UPRIGHT']], px_sets: [[0, 'p3c'], [84, 'aloft'], [176, 'p3u']], look_events: [[0, 'bright', '15'], [18, 'face', 'p3_charge'], [189, 'face', 'p3_idle'], [189, 'bright', '13']], hand_events: [[76, 'p3_open']], anchors: {'charge': ['core'], 'blast': ['core']}, yaw: {knots: [[18, 0], [36, 360]], ease: 'smooth'}},
  {name: 'shells', form: 'p3', len: 113, authored: 140, loop: false, next: 'idle_p3', retime: [[0, 0], [46, 35], [56, 45], [120, 93], [123, 96], [140, 113]], events: {'hunch': 0, 'ring': 10, 'lit': 14, 'lock1': 33, 'launch': 35, 'ball': 36, 'hit1': 45, 'cool': 48, 'lock2': 79, 'lock3': 82, 'hit2': 93, 'hit3': 96, 'end': 113}, stance: ['UPRIGHT', 'UPRIGHT'], px_sets: [[0, 'p3u']], look_events: [[14, 'bright', '15'], [48, 'bright', '13']], anchors: {'launch': ['ball'], 'ball': ['ball']}},
  {name: 'sink_p3', form: 'p3', len: 20, authored: 20, loop: false, next: null, events: {'fold': 0, 'inv': 8, 'sink': 8, 'hide': 12, 'end': 20}, hidden: [[12, 19]], stance: ['UPRIGHT', 'CROUCH'], stance_events: [[7, 'CROUCH']], px_sets: [[0, 'p3u'], [8, 'burrowed']], look_events: [[6, 'face', 'hidden']], hand_events: [[2, 'p3_curl']], state: [[12, 'burrowed']]},
  {name: 'surface_p3', form: 'p3', len: 40, authored: 40, loop: false, next: 'stand_p3', events: {'show': 0, 'splash': 0, 'charge': 0, 'launch': 10, 'hit': 12, 'recover': 12, 'end': 40}, stance: ['CROUCH', 'CROUCH'], px_sets: [[0, 'burrowed'], [0, 'p3c']], look_events: [[0, 'bright', '15'], [10, 'bright', '13']], state: [[0, 'normal']], anchors: {'launch': ['muzzle']}},
  {name: 'tail_p3', form: 'p3', len: 87, authored: 100, loop: false, next: 'idle_p3', retime: [[0, 0], [14, 11], [18, 15], [58, 45], [62, 49], [100, 87]], events: {'crouch': 0, 'cock': 3, 'swing1': 14, 'rise': 24, 'coil': 36, 'lunge': 36, 'swing2': 46, 'rise2': 57, 'end': 87}, stance: ['CROUCH', 'UPRIGHT'], stance_events: [[86, 'UPRIGHT']], px_sets: [[0, 'p3c'], [57, 'p3u']], look_events: [[61, 'face', 'p3_idle']], hand_events: [[62, 'p3_open']], anchors: {'cock': ['tail_tip'], 'swing1': ['tail_root'], 'swing2': ['tail_root']}, tracks: ['tail_root', 'tail_tip'], yaw: {knots: [[13, 0], [21, 200], [45, 200], [53, 0]], ease: 'linear'}},
  {name: 'spikes', form: 'p3', len: 72, authored: 84, loop: false, next: 'idle_p3', retime: [[0, 0], [49, 37], [54, 42], [84, 72]], events: {'curl': 4, 'rise': 10, 'column': 14, 'summon': 19, 'lockA': 37, 'fireA': 42, 'lockB': 43, 'fireB': 48, 'hitA': 49, 'blades': 52, 'hitB': 55, 'skim': 64, 'recover': 65, 'end': 72}, stance: ['UPRIGHT', 'UPRIGHT'], px_sets: [[0, 'p3u']], look_events: [[10, 'bright', '15'], [48, 'bright', '13']], anchors: {'column': ['crown'], 'summon': ['crown']}},
  {name: 'death', form: 'p3', len: 120, authored: 120, loop: false, next: null, events: {'hit': 0, 'flicker': 8, 'droop': 30, 'kneel': 55, 'fall': 70, 'land': 82, 'wither': 85, 'sink': 100, 'gone': 118, 'end': 120}, hidden: [[118, 119]], stance: ['UPRIGHT', 'UPRIGHT'], px_sets: [[0, 'dead']], look_events: [[30, 'face', 'p3_dim'], [85, 'tint', 'withered']], hand_events: [[55, 'p3_curl']], state: [[118, 'burrowed']], blend_in: 6},
];

// ---- the stub motion ---------------------------------------------------------------------------------------------------
// Stance-move windows [from, to] (played ticks) of the clips that change stance: the pose blends STANCES[start] ->
// STANCES[end] over the window (eased); stand_p3 / crouch_p3 are the plan's continuous blends (no body look swap: R12).
const STANCE_MOVES = {crouch_p3: [0, 7], stand_p3: [0, 13], move_strike_p3: [[0, 7], [85, 91]], aftermath: [76, 84], sink_p3: [0, 7], tail_p3: [57, 86]};
// Burrow sinks (plan R9): the root sinks to SINK_DEPTH under the opaque floor through the follow_y offsets (no part keys),
// fully buried parts at scale 0 inside the hidden span; the emergence rises back in RISE ticks.
export const SINK_DEPTH = -6, SINK_STEP = .25, RISE = 6;
export const SINK_TABLE = Array.from({length: Math.round(-SINK_DEPTH / SINK_STEP) + 2}, (_, i) => -(i + 1) * SINK_STEP);   // -0.25 .. -6.5
const SINK_START = {burrow_strike: 6, sink_p1: 4, burrow_in_p1: 6, sink_revive: 20, move_strike_p3: 8, sink_p3: 8, death: 100};
function sinkKnots(c) {
  if (!c.hidden) return null;
  const k = [];
  for (const [a, b] of c.hidden) {
    if (a === 0) k.push([0, SINK_DEPTH], [b, SINK_DEPTH]);
    else { const s0 = Math.min(a - 2, SINK_START[c.name] ?? Math.max(0, a - 10)); k.push([s0, 0], [a - 1, SINK_DEPTH], [b, SINK_DEPTH]); }
    if (b < c.len - 1) k.push([Math.min(c.len - 1, b + RISE), 0]);
  }
  return k;
}
// dy (blocks, <= 0) at tick t from the sink knots, quantized to SINK_TABLE (0 above the first step).
export function sinkAt(c, t) {
  const k = c.sink;
  if (!k) return 0;
  let v = 0;
  if (t <= k[0][0]) v = k[0][1];
  else if (t >= k[k.length - 1][0]) v = k[k.length - 1][1];
  else for (let i = 1; i < k.length; i++) if (t <= k[i][0]) { const [t0, v0] = k[i - 1], [t1, v1] = k[i]; v = v0 + (v1 - v0) * (t - t0) / Math.max(1e-9, t1 - t0); break; }
  const q = Math.round(v / SINK_STEP) * SINK_STEP;
  return Math.abs(q) < 1e-9 ? 0 : Math.max(SINK_TABLE[SINK_TABLE.length - 1], q);
}
const stancePose = (s, form) => (s === 'CROUCH' && form === 'p3' ? STANCES.CRAWL : STANCES[s]);
function stubKeys(c) {
  const [s0, s1] = c.stance, L = c.len;
  const keys = [[0, structuredClone(stancePose(s0, c.form))]];
  const mv = STANCE_MOVES[c.name];
  const wins = !mv ? [] : Array.isArray(mv[0]) ? mv : [mv];
  let cur = s0;
  wins.forEach(([a, b], i) => {
    const to = i === wins.length - 1 ? s1 : (cur === 'UPRIGHT' ? 'CROUCH' : 'UPRIGHT');
    if (a > 0) keys.push([a, structuredClone(stancePose(cur, c.form))]);
    keys.push([b, structuredClone(stancePose(to, c.form))]);
    cur = to;
  });
  // hidden spans: every part at scale 0 inside (vis is a number channel: it lerps; hard switches use adjacent keys)
  for (const [a, b] of c.hidden || []) {
    if (a > 0) keys.push([a - 1, {vis: 1}, 'l']);
    keys.push([a, {vis: 0}, 'l'], [b, {vis: 0}, 'l']);
    if (b < L) keys.push([b + 1, {vis: 1}, 'l']);
  }
  keys.push([L, {}]);
  // merge keys on one tick (stance blends + vis), sorted
  const by = new Map();
  for (const [t, p, e] of keys) { if (!by.has(t)) by.set(t, [t, {}, e]); Object.assign(by.get(t)[1], p); if (e) by.get(t)[2] = e; }
  return [...by.values()].sort((x, y) => x[0] - y[0]);
}
// ---- debug poses (static 2-tick loops; dbg_<name>, ignored by the module): the coverage-gate poses and the views ------
const dbg = (name, form, p, note) => ({name: 'dbg_' + name, form, len: 2, loop: true, next: null, events: {}, stance: [p.__s || 'CROUCH', p.__s || 'CROUCH'],
  px_sets: [[0, form === 'p1' ? 'p1' : 'p3c']], keys: [[0, (({__s, ...q}) => q)(p)], [2, {}]], note, dbg: true});
const lerpPose = (a, b, u) => { const o = {}; for (const k of Object.keys(a)) { const x = a[k], y = b[k]; o[k] = typeof x === 'number' ? x + (y - x) * u : x.map((v, i) => v + (y[i] - v) * u); } return o; };
const C0 = STANCES.CROUCH, U0 = STANCES.UPRIGHT;
export const DBG = [
  dbg('crouch', 'p1', {...C0}, 'CROUCH rest, phase-1 look (the bind pose)'),
  dbg('crawl', 'p3', {...STANCES.CRAWL}, 'CROUCH rest, phase-3 look (the crawl form)'),
  dbg('upright', 'p3', {...U0, __s: 'UPRIGHT'}, 'UPRIGHT rest, phase-3 look'),
  dbg('upright_low', 'p3', {...UPRIGHT_LOW, __s: 'UPRIGHT'}, 'the R1 camera fallback (pose only): waist and thorax lowered'),
  dbg('rear_p1', 'p1', {...C0, ...both({pelT: [0, .5, .4], pelvis: [38, 0, 0], chest: [8, 0, 0], neck: [-12, 0, 0], head: [-14, 0, 0],
    ik_a_l: 0, a_up_l: [30, 0, 35], a_lo_l: [40, 0, 10], ik_b_l: 0, b_up_l: [55, 0, 10], b_lo_l: [40, 0, 0], tail_1: [12, 0, 0]})},
    'phase-1 rear-up (the underside: rib slabs, belly shell, bud face; v2 f2040)'),
  dbg('hoop', 'p3', {...lerpPose(C0, U0, 0), ...both({pelT: [0, 2.2, 0], pelvis: [70, 0, 0], abdomen: [-55, 0, 0], chest: [35, 0, 0], shoulders: [35, 0, 0], neck: [30, 0, 0],
    head: [40, 0, 0], tail_1: [-40, 0, 0], tail_2: [-40, 0, 0], tail_3: [-40, 0, 0], tail_4: [-35, 0, 0], tail_5: [-35, 0, 0], tail_6: [-30, 0, 0],
    ik_a_l: 0, a_up_l: [0, 0, 40], ik_b_l: 0, b_up_l: [40, 0, 20], ik_c_l: 0, c_up_l: [-40, 0, 20]})}, 'the 이동 돌진 hoop / wheel (v5 f930-f951): body arched into a ring'),
  dbg('crouch_over', 'p3', {...lerpPose(C0, U0, .62), ...both({ik_b_l: 0, b_up_l: [40, -30, 40], b_lo_l: [10, -20, 30], b_hand_l: [-20, 0, 0], ik_a_l: 0, ik_c_l: .5}), __s: 'UPRIGHT'},
    'crouch over the player (v5 f1086-f1140): half-upright, the B arms spread overhead like an umbrella (identified: the B arms, not the mantle)'),
];
// ---- the clip list ---------------------------------------------------------------------------------------------------
export const CLIPS = [...CLIP_TABLE.map(t => {
  const c = {...structuredClone(t), keys: null, note: 'R1 stub: the stance pose (+ stance blends, sinks); AP-RC1 authors the motion'};
  c.keys = stubKeys(c);
  c.sink = sinkKnots(c);
  return c;
}), ...DBG];
export const accumulate = clip => acc(clip, DEFAULT_POSE);
export const sampleClip = (clip, t, ks) => sampleShared(clip, t, ks, {defaults: DEFAULT_POSE});
export const restPose = (s = 'CROUCH') => structuredClone(STANCES[s]);
// Dense cumulative yaw schedule (Minecraft degrees, one per played tick) from the table knots.
export function denseYaw(c) {
  if (!c.yaw) return null;
  const {knots, ease} = c.yaw, sm = u => u * u * (3 - 2 * u), out = [];
  for (let t = 0; t < c.len; t++) {
    let v;
    if (t <= knots[0][0]) v = knots[0][1];
    else if (t >= knots[knots.length - 1][0]) v = knots[knots.length - 1][1];
    else for (let i = 1; i < knots.length; i++) if (t <= knots[i][0]) { const [t0, v0] = knots[i - 1], [t1, v1] = knots[i], u = (t - t0) / (t1 - t0); v = v0 + (v1 - v0) * (ease === 'smooth' ? sm(u) : u); break; }
    out.push(Math.round(v * 100) / 100 + 0);
  }
  return out;
}
