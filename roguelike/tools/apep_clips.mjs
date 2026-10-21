// Clips of the 아펩의 오아시스 파수꾼 rig (stage AP-RC2, clips v2): DEFAULT_POSE (= the CROUCH stance, the bind pose), the
// two stance rest poses (STANCES, frozen with the skeleton), the binding clip table of ap_contract.md §0.4.10 (names,
// lengths, authored lengths, RETIME knots, events, hidden spans, stances, px sets, look / hand events, yaw knots, required
// anchors and tracks: CLIP_TABLE, copied from the AP-SPEC stub, never re-ticked without a change note), the pose library
// (POSES: the phase-1 poses of motion.md §5 rebuilt on the R2 skeleton and the plan §6.2 phase-3 glossary) and the keyed
// motion of every clip (CLIP_KEYS), with its burrow sinks, hidden spans, hand-variant events and debug poses.
//
// Timeline. Keys are written on the PLAYED timeline: the binding events are played ticks (plan §6.1, after the -25 %
// wind-up RETIME), so every key sits on the event it serves; the authored (footage) timeline is the inverse of the RETIME
// knots, which stay on the clip for the manifest (`retime`, `authored`). Wind-ups therefore play 25 % faster than the
// footage and strikes / follow-throughs at full speed, exactly as the knots say.
// Format (mboss_rig_clips.mjs): {name, len, loop?, next?, blend?, keys: [[tick, full pose, ease]], events, note} + the
// Apep fields of the table. Every key is a FULL pose (a pose of POSES or a blend of two), so no channel leaks between keys.
// Channels: apep_pose.mjs. No horizontal root travel and no root yaw (the module moves and turns the anchor along the
// exported yaw schedules, R16); vertical travel is pelT.y (and the follow_y sink); the 이동 돌진 hoop roll is the keyed
// root pitch `rot` (keyed_pitch 49-61).
// Phase-1 limbs run on IK (targets in the rig frame, planted hands flat; a lifted hand keeps its bind relation to the
// forearm, `hr`), so the body can rear, twist and sink while the feet stay put. Phase-3 upright arms are FK offsets on
// the UPRIGHT eulers; the crawl uses the CROUCH pose with the CRAWL hand orientation. Hand variants (R8) follow the
// motion: a phase-1 hand lifted >= 0.3 b shows its lifted variant (p1_raised / p1_curl), swapped with the 0.9 -> 1 pulse.
import {accumulate as acc, sampleClip as sampleShared} from './mboss_rig_clips.mjs';
import {J, LIMB_C, SIDES, LIMBS, BONES, BONE, mirrorE, solve, eulerOf, carry} from './apep_pose.mjs';
import {mul, q, rot, sub, add, cross, dot, len, times} from './mboss_rig_math.mjs';

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
  // the crawl hair (AP-RC2): the P3 strands swept back and out off the B forearms and curl hands they hung through in
  // the CROUCH hair pose (R3 open item; hair edges through the B / C arm faces 1742 -> 0 per side, fewer through the
  // hood and chest, the strand tips 0.23 b above the water at rest and no new dips in the clips that leave the crawl)
  Object.assign(STANCES.CRAWL, {hair_l_1: [-16, 0, -15], hair_l_2: [-40, 0, 10], hair_r_1: [-16, 0, 15], hair_r_2: [-40, 0, -10]});
  // UPRIGHT keeps its FK arms (ik 0); its IK targets are set to its own FK wrists and its hand eulers to the crawl's, so
  // a stance blend lerps the targets wrist to wrist and the hands keep one world orientation (nothing changes at rest)
  for (const s of SIDES) for (const L of LIMBS) STANCES.UPRIGHT[`tg_${L}_${s}`] = oU[`${L}_hand_${s}`].t.slice();
  Object.assign(STANCES.UPRIGHT, structuredClone(hf));
}
// The halfway key of every stance blend (stand_p3 / crouch_p3 and the blends inside clips): the body halfway, every limb
// still on IK with the B and C wrists lifted off the water (a plain IK -> FK lerp swings the hands through the floor)
{
  const a = STANCES.CRAWL, b = STANCES.UPRIGHT, mid = {};
  for (const k of Object.keys(a)) { const x = a[k], y = b[k]; mid[k] = typeof x === 'number' ? x + (y - x) / 2 : x.map((v, i) => v + (y[i] - v) / 2); }
  for (const s of SIDES) for (const L of LIMBS) {
    mid[`ik_${L}_${s}`] = 1;
    if (L !== 'a') mid[`tg_${L}_${s}`] = [mid[`tg_${L}_${s}`][0], mid[`tg_${L}_${s}`][1] + 1.2, mid[`tg_${L}_${s}`][2]];
  }
  STANCES.MID = mid;
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

// ==== the pose toolkit =================================================================================================
const deep = o => structuredClone(o);
const isNum = x => typeof x === 'number';
const C0 = STANCES.CROUCH, U0 = STANCES.UPRIGHT, W0 = STANCES.CRAWL, M0 = STANCES.MID;
// channel-wise blend of two full poses (u = 0 -> a, 1 -> b)
export function lerpPose(a, b, u) {
  const o = {};
  for (const k of Object.keys(a)) { const x = a[k], y = k in b ? b[k] : x; o[k] = isNum(x) ? x + (y - x) * u : x.map((v, i) => v + (y[i] - v) * u); }
  return o;
}
// A lifted IK hand keeps a given relation to its forearm: hr_<L>_<s> = the hand euler relative to the lower bone (the
// FK convention; [0, 0, 0] = the bind relation), resolved here into the absolute IK hand euler hf_<L>_<s>.
// hr_* may also be 'keep' (the base's hand euler: a planted hand next to a lifted one, never mirrored from the other
// side), 'P1' (flat on the floor as authored) or 'P3' (the crawl hand orientation).
function finish(p) {
  const hr = Object.keys(p).filter(k => k.startsWith('hr_'));
  if (hr.length) {
    const o = hr.some(k => Array.isArray(p[k])) ? solve(p) : null;
    for (const k of hr) {
      const [, L, s] = k.split('_'), v = p[k], hf = `hf_${L}_${s}`;
      if (Array.isArray(v)) p[hf] = eulerOf(mul(o[`${L}_lo_${s}`].R, q(v)));
      else if (v === 'P1') p[hf] = [0, 0, 0];
      else if (v === 'P3') p[hf] = STANCES.CRAWL[hf].slice();
      delete p[k];
    }
  }
  return floorGuard(p);
}
// Floor guard: the tail, the hem chain and the P1 drapes keep every joint at or above a floor height (the rest pose's
// own heights: the tail lies at 0.19-0.27 b with its model 0.45 b below the line). Each segment, from the root, turns by
// the smallest angle (pitch for the tail / hem, roll outward for the drapes) that lifts its end there. Only lifts.
// (counter: a tail segment turned up by the guard turns the next one back by the same angle, so the tail settles onto
// the floor after the kink instead of rising along the slope of the lifted segment)
const GUARD = [
  {bones: ['tail_1', 'tail_2', 'tail_3', 'tail_4', 'tail_5', 'tail_6', 'tail_7', 'tail_tip'], ax: 0, sg: -1, y: .17, counter: true},
  {bones: ['hem_a', 'hem_b'], ax: 0, sg: -1, y: .14},
  {bones: ['hair_l_1', 'hair_l_2'], ax: 2, sg: 1, y: .18}, {bones: ['hair_r_1', 'hair_r_2'], ax: 2, sg: -1, y: .18},
];
// nearest = the smallest turn in either direction, or with ref the solution closest to ref's angle (the floor pass
// between keys: a blend that dips stays continuous instead of jumping sides); the key poses use the preferred
// direction first. With a form (the clip assembly, AP-RC2) the chains' model probes count too (PROBE below): a part's
// probe points must stay at or above its model floor YM as well as its joint end at y.
function floorGuard(p, nearest = false, ref = null, form = null) {
  for (const g of GUARD) {
    guardChain(p, g, g.bones, nearest, ref, form);
    // with probes: a chain whose later segment still dips (a drape pressed into the ground beside the body) turns its
    // first segment against the whole chain's probes, then the later segments again
    if (form && g.bones.length > 1 && chainProbes(form, g.bones[0]) && chainLow(p, g, form) < g.y - .02) {
      guardChain(p, g, [g.bones[0]], nearest, ref, form, g.bones);
      guardChain(p, g, g.bones.slice(1), nearest, ref, form);
    }
  }
  return p;
}
// the chains with model probes: the hem and the hair (the tail models stay within the joint guard's margin)
const chainProbes = (form, b) => (form && /^(hem|hair)_/.test(b) ? probesOf(form, b) : null);
const probeEnd = (o, b, form, y) => {
  let v = carry(o, b, BONE[b].tip)[1];
  const pr = chainProbes(form, b), ym = pr && PROBE_YM[form][b.replace(/_r(_|$)/, '_l$1')];
  if (pr) for (const P of pr) v = Math.min(v, carry(o, b, P)[1] - ym + y);
  return v;
};
const chainLow = (p, g, form) => { const o = solve(p); return Math.min(...g.bones.map(b => probeEnd(o, b, form, g.y))); };
function guardChain(p, {ax, sg, y, counter}, bones, nearest, ref, form, along = null) {
  { let prevD = 0; for (const b of bones) {
    const pr = form && (along || chainProbes(form, b));
    const end = () => { const o = solve(p); return Math.min(...(along || [b]).map(x => probeEnd(o, x, form, y))); };
    if (counter && prevD) p[b] = p[b].map((v, i) => (i === ax ? v - prevD : v));
    prevD = 0;
    const b0 = p[b][ax];
    const e0 = end();
    if (e0 >= y - (ref && pr ? .05 : 1e-3)) continue;   // (per tick: a marginal dip stays, no flicker of the guard)
    const base = p[b].slice(), set = d => { p[b] = base.slice(); p[b][ax] += d; prevD = p[b][ax] - b0; };
    // per tick (ref = the previous tick's guarded pose): if the previous angle still clears the floor, the smallest
    // fraction of the way back to it that does (the guard releases smoothly and never jumps sides between ticks)
    if (ref && pr) {
      const dR = ref[b][ax] - base[ax];
      set(dR);
      if (Math.abs(dR) > 1e-6 && end() >= y) {
        // (scanned, not bisected: a wide drape rolled a little can dip further before it rises)
        let m = .1; for (; m < 1; m += .1) { set(dR * m); if (end() >= y) break; }
        set(dR * Math.min(1, m));
        continue;
      }
      set(0);
    }
    // the preferred direction first, then the other; if neither reaches the floor height, the highest end of either
    // (with probes: within 30 deg, and only for a real gain, since a probe next to the joint cannot be lifted by a turn)
    const sol = [], R = pr ? Math.min(150, Math.max(45, ref ? Math.abs(ref[b][ax] - base[ax]) + 30 : 0)) : 75;
    for (const dir of [sg, -sg]) {
      set(dir * R); if (end() < y) continue;
      let lo = 0, hi = R;
      for (let i = 0; i < 9; i++) { const m = (lo + hi) / 2; set(dir * m); if (end() >= y) hi = m; else lo = m; }
      sol.push(dir * Math.round(hi * 10) / 10);
      if (!nearest) break;
    }
    const cost = d => (ref ? Math.abs(base[ax] + d - ref[b][ax]) : Math.abs(d));
    let pick = null;
    if (sol.length) pick = sol.reduce((a, d) => (cost(d) < cost(a) ? d : a));
    else {
      const W = pr ? 30 : 75;
      let best = [e0, 0]; for (let d = -W; d <= W; d += 5) { set(d); const e = end(); if (e > best[0] + (pr ? .05 : 0)) best = [e, d]; } pick = best[1];
    }
    set(pick);
  } }
  return p;
}
// ---- the model floor (AP-RC2) -------------------------------------------------------------------------------------------
// The joint guard keeps the chains' joints over the floor, but the R2 models reach past their joints: the P1 drapes splay
// on the ground beside the bone, the P3 hem flaps, the flared leg roots, the P1 hull underside, the P3 tail-root sheath.
// PROBE holds a few model extremes per part (left side; the right mirrors) and form in BIND space (carry() places them):
// farthest-point samples of the R3 model corners from the joint plus the lowest corners at the reference stance
// (rigwork/rc2/tools/probes.mjs; re-derive after a geometry change). PROBE_YM is each part's model floor (its rest low
// less 0.05, at most -0.08; the hair -0.5 / -0.3: cloth may lie in the water, a drape held out flat reads worse). The clip
// assembly lifts the body (pelT y, at most BODY_LIFT) when the hull / sheath probes
// dip under BODY_YM, turns the hem and hair chains (floorGuard with the form) and raises an IK leg's wrist (at most
// LEG_LIFT) when its lower-leg flare dips under its floor.
const PROBE = {
  p1: {
    hair_l_1: [[2.64, 1.99, -3.1], [.74, 3.31, -2.54], [1.52, 2.84, -3.45], [1.82, 3.64, -2.54], [2.31, 3.09, -3.11], [1.86, 1.75, -3.44], [.99, 2.49, -3.38], [2.07, 2.83, -3.38]],
    hair_l_2: [[3.22, .19, -4.28], [2.1, 2.02, -3.68], [2.97, 1.11, -3.46], [2.8, 2.12, -3.39], [2.27, 1.01, -3.76], [2.57, .36, -4.01], [3.23, .14, -3.67], [3.18, .44, -3.76], [2.77, .47, -3.64]],
    hem_a: [[.2, .66, .89], [-.65, 2.09, 1.16], [.65, 2.09, 1.16], [-.3, .84, .96], [.2, 2.17, 1.13], [-.28, 2.24, 1.18]],
    hem_b: [[.2, .08, 1.93], [-.65, .72, .96], [.65, .72, .96], [.2, .73, .87], [-.19, .2, 1.81], [-.2, .73, .87]],
    chest: [[.16, .91, -1.18], [-.46, 4.15, 1.25], [1.67, 3.49, -.72], [-1.58, 2.81, -.72], [1.08, 2.62, 1.25], [-.52, 4.48, -.72], [-.16, .91, -.94]],
    shoulders: [[-1.99, 2.38, .85], [2.55, 4.16, -2], [-1.22, 2.52, -3.33], [1.88, 2.34, .85], [-.52, 4.84, -.89], [.64, 2.23, -1.32], [1.78, 2.09, -2.14], [1.32, 2.09, -2.14], [-1.32, 2.09, -2.14]],
    abdomen: [[.36, 3.88, 2.75], [-1.39, 2.85, .62], [1.39, 2.85, .62], [-.38, 4.3, 1.17], [-.75, 2.56, 2.44], [.75, 2.56, 1.88], [.23, 2.29, 2.43], [.23, 2.29, 2.95], [-.23, 2.29, 2.43]],
    b_lo_l: [[2.52, .42, -3.66], [3.19, 2.12, -2.03], [1.78, 1.67, -2.64], [2.85, .92, -2.48], [2.11, -.01, -2.6], [2.63, 2.22, -2.9], [2.55, -.01, -2.52]],
    c_lo_l: [[3.07, .01, 2.05], [2.45, 2.52, 2.33], [2.88, 1.23, 2.74], [3.48, 2.38, 1.58], [2.6, 1.65, 1.53], [2.64, .26, 3.02], [2.69, -.03, 2.12]],
  },
  p3: {
    hair_l_1: [[2.19, 1.68, -2.72], [.02, 3.93, -3.31], [.74, 2.31, -3.6], [1.54, 3.85, -3.2], [1.9, 2.67, -3.19], [1.16, 1.43, -2.97], [1.69, 1.53, -2.74]],
    hair_l_2: [[2.61, .16, -3.03], [1.12, 1.72, -3.07], [2.21, 1.95, -2.6], [1.55, .63, -3.02], [2.32, 1.17, -3.08], [1.76, 1.5, -2.84], [2.12, .09, -3.28], [1.58, .06, -3.18]],
    hem_a: [[.23, .13, 2.39], [-.17, 2.39, 1.06], [.98, .51, .19], [-.98, .51, .19], [-1, 1.04, 1.7], [.77, 1.54, 2.05], [-.23, .13, 2.39], [-.65, .16, 2.22], [.65, .16, 2.22]],
    hem_b: [[1.74, 1.98, 3.06], [-2.41, .39, 2.25], [.25, .86, .66], [-.71, 1.98, 3.06], [1.59, -.38, 1.68], [-.61, -.38, 1.68], [.61, -.38, 1.68], [-1.59, -.38, 1.68], [2.41, .39, 2.25]],
    tail_1: [[.43, 1.39, 3.74], [-.68, 1.96, 2.38], [.41, 2.7, 2.93], [-.66, 2.08, 3.5], [.01, 1.17, 2.64], [.66, 1.95, 2.37], [-.1, 1.15, 3.43], [.27, 1.19, 3.49]],
    abdomen: [[-.75, 2.31, 3.17], [.61, 2.66, .5], [.73, 1.77, 2.16], [-.71, 2.38, 1.49], [.44, 3.08, 1.83], [.54, 2.51, 3.25], [.87, 1.67, 2.85], [.87, 2.06, 3.04], [.56, 1.27, 2.66]],
    b_lo_l: [[2.34, .22, -3.76], [2.78, 1.95, -1.89], [2.29, 2.21, -3.35], [2.52, .42, -2.25], [1.97, 1.24, -2.82], [2.82, 1.29, -3.34], [2.15, 1.62, -1.75], [2.22, 1.11, -1.85], [2.46, 1.38, -1.89]],
    c_lo_l: [[3.54, .37, 2.74], [1.91, 1.78, 1.48], [2.06, .94, 2.89], [3.42, 1.84, 2.27], [2.64, .89, 1.76], [2.51, 2.44, 2.28], [2.78, .02, 2.05], [2.53, .27, 2.47]],
  },
};
const PROBE_YM = {
  p1: {hair_l_1: -.5, hair_l_2: -.5, hem_a: -.08, hem_b: -.08, b_lo_l: -.08, c_lo_l: -.08},
  p3: {hair_l_1: -.3, hair_l_2: -.3, hem_a: -.08, hem_b: -.43, b_lo_l: -.15, c_lo_l: -.08},
};
const BODY_PROBE = {p1: ['chest', 'shoulders', 'abdomen'], p3: ['tail_1', 'abdomen']}, BODY_YM = -.12, BODY_LIFT = .45, LEG_LIFT = .12;
// the floor envelope's rate: degrees (chain turns) and blocks (body height, leg wrists) per tick
const FLOOR_RATE = {a: 14, h: .06};
const PROBE_R = {};
function probesOf(form, n) {
  const k = form + n;
  if (!(k in PROBE_R)) { const l = n.replace(/_r(_|$)/, '_l$1'), P = PROBE[form][l]; PROBE_R[k] = P ? (l === n ? P : P.map(mx)) : null; }
  return PROBE_R[k];
}
const probeLow = (o, form, n) => { let v = Infinity; for (const P of probesOf(form, n) || []) v = Math.min(v, carry(o, n, P)[1]); return v; };
// the model floor of a full pose for one form (keys and the per-tick floor pass of the clip assembly)
function modelFloor(p, form, nearest = false, ref = null) {
  let o = solve(p);
  const body = Math.min(...BODY_PROBE[form].map(n => probeLow(o, form, n)));
  if (body < BODY_YM) { p.pelT = [p.pelT[0], p.pelT[1] + Math.min(BODY_LIFT, BODY_YM - body), p.pelT[2]]; o = null; }
  floorGuard(p, nearest, ref, form);
  for (const s of SIDES) for (const L of ['b', 'c']) {
    if ((p[`ik_${L}_${s}`] ?? 0) < .5) continue;
    o = o || solve(p);
    const n = `${L}_lo_${s}`, lo = probeLow(o, form, n), ym = PROBE_YM[form][`${L}_lo_l`];
    if (lo < ym) { const k = `tg_${L}_${s}`; p[k] = [p[k][0], p[k][1] + Math.min(LEG_LIFT, ym - lo), p[k][2]]; o = null; }
  }
  return p;
}
// a full pose: the base with both-sided overrides (left channels mirror to the right unless the right one is given)
const P = (base, o = {}) => finish({...deep(base), ...both(o)});
// a full pose: the base plus both-sided DELTAS (eulers / targets added), then overrides
function Pd(base, d = {}, o = {}) {
  const p = deep(base);
  for (const [k, v] of Object.entries(both(d))) p[k] = isNum(v) ? p[k] + v : p[k].map((x, i) => x + v[i]);
  return finish(Object.assign(p, both(o)));
}
const mix = (a, b, u, o = {}) => finish(Object.assign(lerpPose(a, b, u), both(o)));
// the phase-1 bind wrists (left) and an IK wrist target; hr = [0, 0, 0] marks a lifted hand
const WB = {a: [4.8, .6, -2.4], b: [2.4, .4, -3.0], c: [2.9, .4, 2.5]};
const Z = [0, 0, 0];
// A planted phase-1 A wrist sits at 0.6 b (AP-RC2: the R2 claw stands on its finger tips 0.59 b under the wrist, the
// rest height); B / C plant at 0.4 (the petal feet), the phase-3 forks at 0.4-0.45.
const A_PLANT = .6;
const tg = (L, x, y, z, hr = null) => ({[`tg_${L}_l`]: [x, y, z], ...(hr ? {[`hr_${L}_l`]: hr} : {})});
const tgR = (L, x, y, z, hr = 'keep') => ({[`tg_${L}_r`]: [x, y, z], [`hr_${L}_r`]: hr});
// A phase-1 rear of strength r (0 = the crouch, 1 = the thorax stood up as in UPRIGHT) with the hood kept over the head:
// the UPRIGHT body angles scaled by r, the head pitched to a total of `head` degrees (0 = level as in the crouch,
// + = up), the tail root levelled (tail = extra droop), the thorax bent by `lean` (+ = forward over the player).
const BODY = ['pelvis', 'abdomen', 'hem_a', 'hem_b', 'chest', 'shoulders', 'neck'];
function rear(r, {head = -6, lean = 0, tail = 0, y = 0, z = 0} = {}) {
  const o = {pelT: [0, U0.pelT[1] * r + y, U0.pelT[2] * r + z]};
  for (const k of BODY) o[k] = U0[k].map(v => v * r);
  o.chest = [o.chest[0] - lean * .6, 0, 0];
  o.shoulders = [o.shoulders[0] - lean * .4, 0, 0];
  o.head = [head - (o.pelvis[0] + o.chest[0] + o.shoulders[0] + o.neck[0]), 0, 0];
  o.hood_hinge = [0, 0, 0];
  o.tail_1 = [-o.pelvis[0] + tail, 0, 0];
  return o;
}
// a phase-3 upright head pitch delta that keeps the mask facing forward when the thorax bends by `d` degrees in total
const keepFace = d => ({head: [-d, 0, 0]});

// ==== POSES: phase 1 (motion.md §5 on the R2 skeleton) =================================================================
export const POSES = {};
const def = (name, p) => { POSES[name] = p; return p; };
const CROUCH = def('CROUCH', deep(C0));
const CROUCH_IN = def('CROUCH_IN', P(C0, {pelT: [0, -.1, 0], pelvis: [-1.5, 0, 0], chest: [1.5, 0, 0], neck: [1, 0, 0], head: [1.5, 0, 0], tail_2: [2, 0, 0], mantle_l_a: [0, 0, -3]}));
const LOW = def('LOW', P(C0, {pelT: [0, -.45, .1], pelvis: [-3, 0, 0], chest: [-3, 0, 0], neck: [4, 0, 0], head: [3, 0, 0], tail_1: [3, 0, 0], mantle_l_a: [0, 0, -6]}));
const CROUCH_LOW = def('CROUCH_LOW', P(C0, {pelT: [0, -.6, .1], pelvis: [-2, 0, 0], chest: [-2, 0, 0], neck: [5, 0, 0], head: [6, 0, 0], ...tg('a', 5.1, A_PLANT, -2.2), ...tg('b', 2.6, .4, -3.1), ...tg('c', 3.1, .4, 2.6)}));
const HALF = def('HALF', P(C0, {...rear(.3, {head: -4}), ...tg('b', 2.3, .4, -2.4), ...tg('c', 2.9, .4, 1.6), ...tg('a', 3.7, 1.5, -1.9, Z)}));
const REAR = def('REAR', P(C0, {...rear(.45, {head: -12}), ...tg('b', 2.5, 1.4, -2.8, Z), ...tg('c', 2.9, .4, 1.3), ...tg('a', 4.4, 4.6, -2.0, Z)}));
const DIVE = def('DIVE', P(C0, {pelT: [0, -.35, -.25], pelvis: [-20, 0, 0], chest: [-10, 0, 0], shoulders: [-4, 0, 0], neck: [10, 0, 0], head: [14, 0, 0], tail_1: [10, 0, 0],
  ...tg('a', 3.0, A_PLANT, -4.6), ...tg('b', 2.3, .4, -3.5)}));
const SPLAY = def('SPLAY', P(C0, {pelT: [0, -1.2, 0], pelvis: [-5, 0, 0], chest: [-4, 0, 0], neck: [6, 0, 0], head: [6, 0, 0], tail_1: [12, 0, 0],
  ...tg('a', 5.9, A_PLANT, -1.6), ...tg('b', 3.4, .35, -3.1), ...tg('c', 3.7, .35, 2.7), mantle_l_a: [0, 0, -15], mantle_l_b: [0, 0, -10]}));
const EMERGE = def('EMERGE', P(C0, {...rear(.55, {head: 20, y: -.3}), ...tg('a', 2.4, 1.6, -1.2, Z), ...tg('b', 1.9, 1.5, -1.8, Z), ...tg('c', 2.5, .4, 1.1)}));
const ERUPT = def('ERUPT', P(C0, {...rear(.95, {head: -25, y: 1.3, tail: -10}), ...tg('a', 2.4, 9.2, .6, Z), ...tg('b', 2.6, 3.2, -1.8, Z), ...tg('c', 2.4, 1.3, .2, Z), mantle_l_a: [0, 0, 30]}));
const LOOM = def('LOOM', P(C0, {...rear(.75, {head: -22, lean: 14, y: .5}), ...tg('b', 2.4, 7.0, -3.4, Z), ...tg('a', 5.2, 5.4, -2.2, Z), ...tg('c', 2.9, .4, 1.2)}));
const LOOM_WIND = def('LOOM_WIND', P(LOOM, {chest: [LOOM.chest[0], 16, 0], shoulders: [LOOM.shoulders[0], 8, 0], ...tg('a', 4.2, 3.6, .9, Z), ...tgR('a', -5.0, 2.8, 1.6, Z)}));
const LUNGE = def('LUNGE', P(C0, {pelT: [0, -.7, -.5], pelvis: [-12, 0, 0], chest: [-6, -16, 0], shoulders: [0, -6, 0], neck: [8, 0, 0], head: [8, 0, 0], tail_1: [6, 0, 0],
  ...tg('a', 5.0, 1.2, -3.0, Z), ...tgR('a', 2.0, 1.2, -5.4, Z), ...tg('b', 2.6, .9, -1.6, Z), ...tg('c', 2.8, 1.0, 3.8, Z)}));
const LAND = def('LAND', P(C0, {pelT: [0, -.6, 0], pelvis: [-6, 0, 0], chest: [-4, 0, 0], neck: [6, 0, 0], head: [5, 0, 0], ...tg('a', 5.4, A_PLANT, -2.2), ...tg('b', 2.8, .4, -3.1), ...tg('c', 3.3, .4, 2.6)}));
const SPREAD = def('SPREAD', P(C0, {...rear(.35, {head: -10}), ...tg('a', 6.0, 2.8, -.8, Z), ...tg('b', 2.5, .4, -2.5), ...tg('c', 2.9, .4, 1.5), mantle_l_a: [0, 25, 15]}));
const SWIRL = def('SWIRL', P(SPREAD, {chest: [SPREAD.chest[0], -12, 0], shoulders: [SPREAD.shoulders[0], -10, 0], ...tg('a', 5.0, 3.4, 1.8, Z), ...tgR('a', -4.4, 3.0, -3.8, Z), mantle_l_a: [0, 35, 30], mantle_r_a: [0, -10, -5]}));
const OVERHEAD = def('OVERHEAD', P(C0, {...rear(.62, {head: -22, y: .45}), ...tg('a', .7, 8.4, -2.4, Z), ...tg('b', 2.4, 2.2, -2.6, Z), ...tg('c', 2.9, .4, 1.0)}));
const PLUNGE = def('PLUNGE', P(C0, {pelT: [0, -.5, -.3], pelvis: [-16, 0, 0], chest: [-12, 0, 0], shoulders: [-6, 0, 0], neck: [14, 0, 0], head: [14, 0, 0], tail_1: [6, 0, 0],
  ...tg('a', 1.1, A_PLANT, -4.4), ...tg('b', 2.1, .4, -2.9), ...tg('c', 2.9, .4, 2.3)}));
const PLUNGE_DEEP = def('PLUNGE_DEEP', P(PLUNGE, {pelT: [0, -.52, -.2], pelvis: [-18, 0, 0], chest: [-12, 0, 0], head: [16, 0, 0]}));
const PLUNGE_DIP = def('PLUNGE_DIP', P(PLUNGE_DEEP, {pelT: [0, -.56, -.25], chest: [-15, 0, 0], neck: [17, 0, 0]}));
const CROSS = def('CROSS', P(C0, {...rear(.5, {head: -8}), ...tg('a', 1.2, A_PLANT, -4.2), ...tg('b', 2.4, .4, -2.4), ...tg('c', 2.9, .4, 1.3), mantle_l_a: [0, 0, 60], mantle_l_b: [0, 0, 20]}));
const FLOWER = def('FLOWER', P(C0, {...rear(.95, {head: -18, y: .9, lean: -5}), ...tg('a', 3.4, 7.6, -1.2, Z), ...tg('b', 2.8, 3.6, -2.2, Z), ...tg('c', 2.8, .4, .8),
  mantle_l_a: [-20, 0, 70], mantle_l_b: [0, 0, 30]}));
const COLUMN = def('COLUMN', (() => {
  const p = P(C0, {...rear(1.0, {head: -15, y: 1.3}), ...tg('c', 2.6, .4, .6), tSweep: 40, tCurl: -4});
  p.chest = [p.chest[0], 22, 0]; p.shoulders = [p.shoulders[0], 22, 0]; p.neck = [p.neck[0], 16, 0];
  Object.assign(p, {tg_a_l: [-1.4, 6.4, -1.2], tg_a_r: [1.6, 7.4, .8], tg_b_l: [-.6, 4.6, -1.6], tg_b_r: [.9, 3.8, .9], hr_a_l: Z, hr_a_r: Z, hr_b_l: Z, hr_b_r: Z});
  return finish(p);
})());
const SLAM = def('SLAM', P(C0, {pelT: [0, -.55, -.4], pelvis: [-18, 0, 0], chest: [-12, 0, 0], shoulders: [-6, 0, 0], neck: [12, 0, 0], head: [12, 0, 0], tail_1: [8, 0, 0],
  ...tg('a', 2.4, A_PLANT, -4.9), ...tg('b', 2.5, .4, -3.5), ...tg('c', 3.0, .4, 2.4)}));
const CROUCH_LOAD = def('CROUCH_LOAD', P(C0, {pelT: [0, -.75, .1], pelvis: [4, 0, 0], chest: [2, 0, 0], neck: [-3, 0, 0], head: [-4, 0, 0], tail_1: [4, 0, 0]}));
const LEAP_UP = def('LEAP_UP', P(C0, {...rear(.4, {head: -10, y: 2.0}), ...tg('a', 4.0, 4.0, -1.5, Z), ...tg('b', 2.2, 2.4, -2.2, Z), ...tg('c', 2.6, 2.0, 2.0, Z)}));
const AIR = def('AIR', P(C0, {pelT: [0, 4.6, 0], pelvis: [8, 0, 0], chest: [-4, 0, 0], neck: [-4, 0, 0], head: [-4, 0, 0], tCurl: 10,
  ...tg('a', 5.2, 8.6, -1.0, Z), ...tg('b', 2.0, 5.6, -2.4, Z), ...tg('c', 2.4, 5.6, 1.8, Z), mantle_l_a: [0, 0, 25]}));
const DIVEDOWN = def('DIVEDOWN', P(C0, {pelT: [0, 3.4, -.6], pelvis: [-62, 0, 0], chest: [-8, 0, 0], neck: [6, 0, 0], head: [8, 0, 0], tail_1: [20, 0, 0],
  ...tg('a', 2.2, .9, -4.6, Z), ...tg('b', 2.0, 1.8, -3.6, Z), ...tg('c', 2.0, 3.6, 2.2, Z)}));
const ARMSUP = def('ARMSUP', P(C0, {...rear(.85, {head: -18, y: .2}), ...tg('a', 3.2, 7.6, -1.8, Z), ...tg('b', 2.8, 2.6, -2.0, Z), ...tg('c', 2.8, .4, .9)}));
const LEAN = def('LEAN', P(C0, {...rear(.9, {head: -26, lean: 20, y: .6}), ...tg('a', 3.6, 3.8, -3.6, Z), ...tg('b', 3.6, 4.6, -2.6, Z), ...tg('c', 2.9, .4, 1.2)}));
const LEAN_L = def('LEAN_L', P(LEAN, {pelvis: [LEAN.pelvis[0], 0, -5], chest: [LEAN.chest[0], 0, -3]}));
const LEAN_R = def('LEAN_R', P(LEAN, {pelvis: [LEAN.pelvis[0], 0, 5], chest: [LEAN.chest[0], 0, 3]}));
const HOODED = def('HOODED', P(C0, {...rear(.9, {head: -12, y: -.2}), ...tg('a', 2.6, 1.6, -1.2, Z), ...tg('b', 2.0, 1.8, -1.6, Z), ...tg('c', 2.6, .4, .6)}));
const HOODED_SWAY = def('HOODED_SWAY', P(HOODED, {pelvis: [HOODED.pelvis[0], 0, 3], neck: [HOODED.neck[0], 0, -3]}));
// sideways crash to its right (roll + tips the top toward the boss's right): the right limbs on the ground, the left flung up
const CRASH = def('CRASH', P(C0, {pelT: [0, -.55, 0], pelvis: [0, 0, 46], chest: [-4, 0, 8], neck: [4, 0, 0], tSweep: -30,
  ...tg('a', 2.6, 4.2, -3.2, Z), ...tgR('a', -6.2, A_PLANT, -1.8), ...tg('b', 3.0, 3.0, -2.6, Z), ...tgR('b', -3.8, .4, -3.6), ...tg('c', 3.0, 2.6, 2.2, Z), ...tgR('c', -3.6, .4, 2.6),
  mantle_l_a: [0, 0, 40], mantle_l_b: [0, 0, 20]}));
const CRASH_B = def('CRASH_B', P(CRASH, {chest: [-8, 0, 12], tSweep: -45, tg_a_l: [3.4, 4.6, -1.6], tg_a_r: [-6.4, A_PLANT, .2]}));
// (the right drapes roll the same way as in the crash, so the blend from the crash stays over the floor; the guard's
// preferred outward roll folds them into an S here)
const SPRAWL = def('SPRAWL', P(C0, {pelT: [0, -1.1, 0], pelvis: [0, 0, 22], chest: [-3, 0, 4], ...tg('a', 5.8, A_PLANT, -1.4), ...tg('b', 3.5, .4, -3.6), ...tg('c', 3.6, .4, 2.9),
  ...tgR('b', -3.3, .4, -2.6), ...tgR('c', -4.0, .4, 3.5),
  hair_r_1: [0, 0, 30], hair_r_2: [0, 0, 46]}));
const PUSHUP = def('PUSHUP', P(C0, {pelT: [0, -.35, 0], pelvis: [8, 0, 8], chest: [4, 0, 2], neck: [-4, 0, 0], head: [-2, 0, 0], ...tg('a', 5.0, A_PLANT, -2.0), ...tg('b', 2.3, .4, -2.6)}));
// tail: pitch - raises a back-pointing segment; yaw + swings it to the boss's left (tSweep spreads a yaw over the chain)
const TAIL_S = def('TAIL_S', P(C0, {pelT: [0, .15, 0], pelvis: [-5, 0, 0], chest: [2, 0, 0], neck: [-4, 0, 0], head: [-2, 0, 0],
  // a tall S over the back (v2 f980-f1019): the segments climb at 55-65 deg, the last three curl forward (tip ~10 b)
  tail_1: [-107, 0, 0], tail_2: [-1, 0, 0], tail_3: [38, 0, 0], tail_4: [41, 0, 0], tail_5: [-16, 0, 0], tail_6: [-29, 0, 0], tail_7: [-26, 0, 0], tail_tip: [-24, 0, 0]}));
// swing 1 turns the anchor clockwise (+ yaw, toward the boss's right): the tail cocks raised to the boss's LEFT (v2 f1036)
// and lags there
const tailYaw = (base, lift, yaws, o = {}) => P(base, {...Object.fromEntries(['tail_1', 'tail_2', 'tail_3', 'tail_4', 'tail_5', 'tail_6', 'tail_7', 'tail_tip'].map((k, i) => [k, [i ? lift[1] ?? 0 : lift[0], yaws[i] ?? 0, 0]])), ...o});
const BRACE = {pelT: [0, -.25, 0], pelvis: [-4, 0, 0], ...tg('a', 5.2, A_PLANT, -2.0), ...tg('b', 2.6, .4, -3.0), ...tg('c', 3.2, .4, 2.7)};
const TAIL_COCK = def('TAIL_COCK', tailYaw(C0, [-60, -10], [34, 22, 18, 14, 10, 8, 6, 6], {...BRACE, pelvis: [-4, -10, 0], chest: [0, 8, 0]}));
const TAIL_WHIP = def('TAIL_WHIP', tailYaw(C0, [-12, 2], [28, 14, 10, 6, 4, 2, 0, 0], {...BRACE, pelvis: [-4, 4, 0], chest: [0, -4, 0]}));
const TAIL_FOLLOW = def('TAIL_FOLLOW', tailYaw(C0, [-8, 2], [-30, -14, -10, -8, -6, -4, -2, -2], {...BRACE, pelvis: [-4, 8, 0], chest: [0, -8, 0]}));
const TAIL_COCK2 = def('TAIL_COCK2', tailYaw(C0, [-60, -10], [-34, -22, -18, -14, -10, -8, -6, -6], {...BRACE, pelvis: [-4, 10, 0], chest: [0, -8, 0]}));
const TAIL_WHIP2 = def('TAIL_WHIP2', tailYaw(C0, [-10, 2], [-28, -14, -10, -6, -4, -2, 0, 0], {...BRACE, pelvis: [-4, -4, 0], chest: [0, 4, 0]}));
const TAIL_FOLLOW2 = def('TAIL_FOLLOW2', tailYaw(C0, [-6, 2], [30, 14, 10, 8, 6, 4, 2, 2], {...BRACE, pelvis: [-4, -8, 0], chest: [0, 8, 0]}));
// (the right drapes keep the swing's side of the roll: -32 / -52 clears the floor; the guard's own pick runs out of range)
const TAIL_REST = def('TAIL_REST', P(SPRAWL, {pelvis: [0, 0, 8], tail_1: [6, 0, 0], hair_r_1: [0, 0, -32], hair_r_2: [0, 0, -52]}));
// the melee combo (4 segments)
const SWEEP_BACK = def('SWEEP_BACK', P(C0, {...rear(.15, {head: -4}), chest: [rear(.15).chest[0], 18, 0], shoulders: [rear(.15).shoulders[0], 8, 0], ...tgR('a', -4.8, 1.6, 1.8, Z), ...tg('a', 4.8, .6, -2.4)}));
const SWEEP_THRU = def('SWEEP_THRU', P(C0, {pelT: [0, -.3, -.2], pelvis: [-4, 0, 0], chest: [-4, -22, 0], shoulders: [0, -8, 0], ...tgR('a', 2.6, 1.0, -5.6, Z), ...tg('a', 4.8, .6, -2.4)}));
const SWEEP_END = def('SWEEP_END', P(C0, {pelT: [0, -.3, -.1], chest: [-2, -28, 0], ...tgR('a', 5.2, 1.0, -2.4, Z), ...tg('a', 5.0, .6, -1.6)}));
const COMBO_HIGH = def('COMBO_HIGH', P(C0, {...rear(.95, {head: -20, y: .6}), ...tg('b', 2.0, 7.6, -2.0, Z), ...tg('a', 4.0, 7.0, -1.0, Z), ...tg('c', 2.8, .4, .9)}));
const DOUBLE_SLAM = def('DOUBLE_SLAM', P(C0, {pelT: [0, -.3, -.8], pelvis: [-15, 0, 0], chest: [-12, 0, 0], shoulders: [-4, 0, 0], neck: [10, 0, 0], head: [10, 0, 0],
  ...tg('b', 1.3, .4, -4.4), ...tg('a', 2.2, A_PLANT, -5.0), ...tg('c', 2.9, .4, 1.8)}));
const TWIST = def('TWIST', P(C0, {pelT: [0, -.3, 0], pelvis: [-3, -8, 0], chest: [0, -18, 0], shoulders: [0, -8, 0], ...tg('a', 5.0, 1.2, 1.4, Z), ...tgR('a', -3.6, 1.2, -4.6, Z)}));
const SPIN_OUT = def('SPIN_OUT', P(C0, {pelT: [0, -.25, 0], chest: [0, 10, 0], ...tg('a', 6.0, 1.0, -.6, Z), ...tg('b', 3.4, .9, -2.6, Z), tSweep: 25, mantle_l_a: [0, 0, 30]}));
const TALLEST = def('TALLEST', P(C0, {...rear(1.0, {head: -15, y: 1.0, lean: -6}), ...tg('a', 4.4, 8.6, -.6, Z), ...tg('b', 2.6, 7.2, -1.6, Z), ...tg('c', 2.7, .4, .6)}));
const SLAM_FAR = def('SLAM_FAR', P(C0, {pelT: [0, -.3, -1.6], pelvis: [-22, 0, 0], chest: [-12, 0, 0], neck: [10, 0, 0], head: [12, 0, 0], tail_1: [17, 0, 0],
  ...tg('a', 2.2, A_PLANT, -6.2), ...tg('b', 1.6, .4, -5.2), ...tg('c', 2.9, .4, 1.8)}));
const STAGGER = def('STAGGER', P(C0, {pelT: [0, -.35, .2], pelvis: [-3, 0, -6], chest: [-4, 0, -4], neck: [18, 0, 0], head: [14, 0, 0], ...tg('a', 4.6, .6, -2.0)}));
const STAGGER2 = def('STAGGER2', P(STAGGER, {pelvis: [-4, 0, 7], chest: [-5, 0, 4]}));
const ROAR = def('ROAR', P(C0, {...rear(.4, {head: 16}), ...tg('a', 5.6, 1.8, -1.4, Z), ...tg('b', 2.4, .4, -2.5), ...tg('c', 2.9, .4, 1.5), mantle_l_a: [0, 20, 20]}));
const REACH = def('REACH', P(C0, {...rear(.8, {head: 20, y: .3}), ...tgR('a', -.6, 9.0, -1.2, Z), ...tg('a', 3.8, 1.2, -1.6, Z), ...tg('b', 2.3, 1.6, -2.0, Z), ...tg('c', 2.8, .4, .9)}));
const REACH_LOW = def('REACH_LOW', P(REACH, {...tgR('a', -2.2, 6.6, -2.4, Z)}));

// ==== POSES: phase 3, the plan §6.2 glossary (UPRIGHT = T, the crawl = CROUCH with the P3 hands) =========================
// The elbow twist (bn) that puts each IK limb's elbow where the UPRIGHT FK elbow is: U0K = UPRIGHT with the C limbs on IK
// (identical at rest), so a lowered upright pose keeps the C hands planted on the water and blends with UPRIGHT cleanly.
const BN_U = {};
{
  const oF = solve(U0), d = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
  for (const L of LIMBS) for (const s of SIDES) {
    const k = `${L}_${s}`, err = bn => d(solve({...U0, [`ik_${k}`]: 1, [`bn_${k}`]: bn})[`${L}_lo_${s}`].t, oF[`${L}_lo_${s}`].t);
    let best = 0;
    for (let bn = -180; bn < 180; bn += 4) if (err(bn) < err(best)) best = bn;
    for (let bn = best - 4; bn <= best + 4; bn += .25) if (err(bn) < err(best)) best = bn;
    BN_U[k] = best;
  }
}
const ikU = (...Ls) => Object.fromEntries(Ls.flatMap(L => SIDES.flatMap(s => [[`ik_${L}_${s}`, 1], [`bn_${L}_${s}`, BN_U[`${L}_${s}`]]])));
const U0K = {...deep(U0), ...ikU('c')};
// a free P3 hand keeps its UPRIGHT relation to the forearm
const HR3 = L => U0[`${L}_hand_l`].slice();
const UPRIGHT = def('UPRIGHT', deep(U0));
const CRAWL = def('CRAWL', deep(W0));
const MID = def('MID', deep(M0));
const SWAY_L = def('SWAY_L', Pd(U0, {pelvis: [0, 0, 3], chest: [0, 0, -2], shoulders: [0, 0, -2], a_lo_l: [0, 0, 8], b_lo_l: [0, 0, 6]}));
const SWAY_R = def('SWAY_R', Pd(U0, {pelvis: [0, 0, -3], chest: [0, 0, 2], shoulders: [0, 0, 2], a_lo_l: [0, 0, -4], b_lo_l: [0, 0, -3]}));
const TALL = def('TALL', Pd(U0, {pelT: [0, .1, 0], a_lo_l: [0, 0, 6], b_lo_l: [0, 0, 6]}));
// HUNCH (v6 f780): the thorax bent forward, head down, arms forward (the upright fold's first half; face still shown)
const HUNCH = def('HUNCH', Pd(U0K, {pelT: [0, -.35, -.1], pelvis: [-14, 0, 0], chest: [-10, 0, 0], shoulders: [-8, 0, 0], neck: [-4, 0, 0], head: [-6, 0, 0],
  a_up_l: [0, 18, -14], a_lo_l: [0, 0, -12], b_up_l: [0, 28, -10], b_lo_l: [0, 10, -10]}));
// HUNCH_CURL (shells t14): arms curled in under the hunched thorax
const HUNCH_CURL = def('HUNCH_CURL', Pd(HUNCH, {a_up_l: [0, 16, -22], a_lo_l: [0, 0, -30], b_up_l: [0, 18, -26], b_lo_l: [0, 20, 30], b_hand_l: [0, 0, 20]}));
// MOUND (v5 f816): collapsed into a low leaf mound on the water, hood closed, limbs pulled in
const MOUND = def('MOUND', P(W0, {pelT: [0, -1.0, .2], pelvis: [-6, 0, 0], chest: [-6, 0, 0], neck: [6, 0, 0], head: [8, 0, 0], tSweep: 30, tCurl: -2,
  ...tg('a', 3.4, .4, -2.2), ...tg('b', 2.2, .4, -2.6), ...tg('c', 2.6, .4, 2.0), mantle_l_a: [0, 0, -12]}));
// HOOP / wheel (v5 f930-f951, w1 f96): the body arched into a ring round the root pivot, hood leading, tail closing it
const HOOP = def('HOOP', P(W0, {pelT: [0, .8, 1.0], pelvis: [38, 0, 0], abdomen: [20, 0, 0], chest: [-42, 0, 0], shoulders: [-40, 0, 0], neck: [-40, 0, 0], head: [-30, 0, 0],
  tCurl: -33, tLift: -10, ...tg('a', 2.2, 4.6, 0, HR3('a')), ...tg('b', 1.8, 4.0, -.4, HR3('b')), ...tg('c', 1.8, 3.4, 2.2, HR3('c')), mantle_l_a: [0, 0, -10]}));
// BELLY_FLOP (v5 f960): the body flat on the water after the wheel, limbs flat out, tail straight back
const BELLY_FLOP = def('BELLY_FLOP', P(W0, {pelT: [0, -1.0, -.5], pelvis: [-6, 0, 0], chest: [-8, 0, 0], neck: [4, 0, 0], head: [6, 0, 0],
  ...tg('a', 5.8, .45, -1.8), ...tg('b', 3.4, .45, -3.2), ...tg('c', 3.6, .45, 2.8)}));
// the 360-degree ground whip (the anchor spins 66-72): the tail trails flat to the boss's left
const TAIL_SWEEP = def('TAIL_SWEEP', P(BELLY_FLOP, {tSweep: 45, tail_1: [4, 0, 0]}));
// SCOIL (v6 f306): a tall S of thorax and abdomen with the hood closed, tail raised behind (the crawl look: face hidden)
const SCOIL = def('SCOIL', Pd(U0K, {pelT: [0, -.2, .1], pelvis: [-12, 0, 6], chest: [14, 0, -4], shoulders: [-14, 0, 0], neck: [14, 0, 0], head: [-36, 0, 0],
  hood_hinge: [-84, 0, 0], tail_1: [-28, 10, 0], tail_2: [-30, 6, 0], tail_3: [26, 0, 0], tail_4: [20, 0, 0],
  a_up_l: [0, -8, -6], b_up_l: [0, -10, -6]}));
const SCOIL_LOW = def('SCOIL_LOW', Pd(SCOIL, {pelT: [0, -.6, -.4], pelvis: [-18, 0, -6], chest: [-12, 0, 0], neck: [6, 0, 0], head: [8, 0, 0], tail_1: [12, 0, 0]}));
// CURL (spikes t4, v6 f540): a dark low curl, the hood half over, arms wrapped in, tail coiled
const CURL = def('CURL', Pd(U0K, {pelT: [0, -.8, -.3], pelvis: [-27, 0, 0], chest: [-6, 0, 0], shoulders: [-8, 0, 0], neck: [-6, 0, 0], head: [-14, 0, 0], hood_hinge: [-45, 0, 0],
  a_up_l: [0, 34, -40], a_lo_l: [0, 0, -40], b_up_l: [0, 30, -40], b_lo_l: [0, 20, 20], tSweep: 40}));
// BALL (v5 f2094, the shell launch): every limb and plate wrapped round the body, a curled ball of leaves
const BALL = def('BALL', Pd(CURL, {pelT: [0, .5, 0], hood_hinge: [20, 0, 0], a_up_l: [0, 10, -10], a_lo_l: [0, 0, -20], b_up_l: [0, 10, -12], b_lo_l: [0, 10, 20], mantle_l_a: [0, 0, -20]}));
// V (arms up): the A antlers and the B arms raised, the face up toward the light column
const V = def('V', Pd(U0, {a_up_l: [0, 0, 16], a_lo_l: [0, 0, 12], b_up_l: [0, 0, 34], b_lo_l: [0, 0, -12], clav_a_l: [0, 0, 6], ...keepFace(-6), mantle_l_a: [0, 0, 15]}));
const T_WIDE = def('T_WIDE', Pd(U0, {a_up_l: [0, -10, -4], b_up_l: [0, -14, 10], b_lo_l: [0, 0, -10], c_up_l: [0, -6, 6]}));
const LAUNCH = def('LAUNCH', Pd(V, {head: [12, 0, 0], hood_hinge: [8, 0, 0], a_lo_l: [0, 0, 16], b_up_l: [0, 0, 10], chest: [4, 0, 0]}));
const AIM = def('AIM', Pd(T_WIDE, {chest: [4, 0, 0], a_up_l: [0, -16, 0], b_up_l: [0, -18, 0], b_lo_l: [0, 0, 14]}));
const THRUST = def('THRUST', Pd(U0, {chest: [-6, 0, 0], shoulders: [-4, 0, 0], head: [10, 0, 0], a_up_l: [0, 30, -12], a_lo_l: [0, 10, -10], b_up_l: [0, 36, 0], b_lo_l: [0, 10, -20]}));
const FLICK_L = def('FLICK_L', (() => { const p = Pd(T_WIDE); for (const [k, d] of [['b_up_l', [0, 26, 14]], ['b_lo_l', [0, 0, -18]], ['a_up_l', [0, 12, 6]]]) p[k] = p[k].map((v, i) => v + d[i]); return p; })());
const FLICK_R = def('FLICK_R', (() => { const p = Pd(T_WIDE); for (const [k, d] of [['b_up_r', [0, -26, -14]], ['b_lo_r', [0, 0, 18]], ['a_up_r', [0, -12, -6]]]) p[k] = p[k].map((v, i) => v + d[i]); return p; })());
// CROUCH_OVER (v5 f1086-f1140, the umbrella): half upright, the B arms spread over the player
const CROUCH_OVER = def('CROUCH_OVER', mix(W0, U0, .62, {ik_b_l: 0, b_up_l: [40, -30, 40], b_lo_l: [10, -20, 30], b_hand_l: [-20, 0, 0], ik_a_l: 0, ik_c_l: 1}));
// the 종말의 여파 cast: seated after the whirl (w1 f123-f135: a tall hunched mass over the field, every arm curved down to
// the water round it, the hood forward), aloft in a V, the blast
const SEATED = def('SEATED', Pd(lerpPose(M0, U0, .35), {pelT: [0, -.35, -.25], chest: [-14, 0, 0], shoulders: [-8, 0, 0], neck: [6, 0, 0], head: [8, 0, 0], tail_1: [-6, 0, 0]},
  {ik_a_l: 1, ik_b_l: 1, ik_c_l: 1, ...tg('a', 5.6, .6, -1.8), ...tg('b', 4.0, .45, -2.2), ...tg('c', 3.4, .4, 2.2), mantle_l_a: [0, 0, -10]}));
const WHIRL = def('WHIRL', mix(M0, U0, .35, {pelT: [0, .9, -.6], ik_a_l: 0, ik_b_l: 0, a_up_l: [0, -30, 70], a_lo_l: [0, 0, 20], b_up_l: [0, -40, 60], b_lo_l: [0, 0, 10], tSweep: -40}));
const ALOFT = def('ALOFT', Pd(V, {pelT: [0, 3.4, 0], tail_1: [30, 0, 0], tCurl: -6, c_up_l: [0, 0, -16], c_lo_l: [10, 0, 0], hem_a: [8, 0, 0]}));
const ALOFT_HI = def('ALOFT_HI', Pd(ALOFT, {pelT: [0, .25, 0], a_lo_l: [0, 0, 6], b_up_l: [0, 0, 6]}));
const BLAST = def('BLAST', Pd(ALOFT, {chest: [8, 0, 0], head: [10, 0, 0], a_up_l: [0, -20, 10], b_up_l: [0, -30, 20], b_lo_l: [0, 0, -20], c_up_l: [0, -10, 20]}));
// the cut-scene emergence and reveal (revival)
const REACH_P3 = def('REACH_P3', (() => { const p = Pd(HUNCH, {pelT: [0, .3, 0], hood_hinge: [-40, 0, 0]}); p.a_up_r = [p.a_up_r[0] - 10, p.a_up_r[1] - 10, p.a_up_r[2] - 40]; p.a_lo_r = [p.a_lo_r[0], p.a_lo_r[1], p.a_lo_r[2] - 20]; return p; })());
// death: the snap back, the droop, the kneel and the fall onto the water
const HIT_SNAP = def('HIT_SNAP', Pd(U0, {pelvis: [6, 0, 0], chest: [6, 0, 0], neck: [-10, 0, 0], head: [18, 0, 0], hood_hinge: [8, 0, 0], a_up_l: [0, -10, 10], b_up_l: [0, -16, 8]}));
const DROOP = def('DROOP', Pd(U0K, {pelT: [0, -.4, -.1], pelvis: [-8, 0, 0], chest: [-8, 0, 0], shoulders: [-6, 0, 0], neck: [-6, 0, 0], head: [-26, 0, 0], hood_hinge: [-20, 0, 0],
  a_up_l: [0, 8, -30], a_lo_l: [0, 0, -16], b_up_l: [0, 8, -22], b_lo_l: [0, 0, -10]}));
const KNEEL = def('KNEEL', Pd(DROOP, {pelT: [0, -.6, -.2], pelvis: [-14, 0, 0], chest: [-6, 0, 0], head: [-10, 0, 0], hood_hinge: [-20, 0, 0], b_up_l: [0, 0, 8], a_up_l: [0, 0, 6]}, {tg_c_l: [3.0, .5, -1.4]}));
const FALLEN = def('FALLEN', P(W0, {pelT: [0, -1.3, -.6], pelvis: [-8, 0, 0], chest: [-8, 0, 0], neck: [5, 0, 0], head: [10, 0, 0],
  ...tg('a', 5.9, .45, -1.6), ...tg('b', 3.5, .45, -3.0), ...tg('c', 3.7, .45, 2.7), mantle_l_a: [0, 0, -15], tSweep: 20}));
// the surfacing shot (surface_p3): the crawl with the hood raised at the player, then the thrust
const SURF_AIM = def('SURF_AIM', P(W0, {pelT: [0, .2, 0], pelvis: [10, 0, 0], chest: [6, 0, 0], neck: [-6, 0, 0], head: [-10, 0, 0], tail_1: [-10, 0, 0], ...tg('b', 2.4, .4, -2.6)}));
const SURF_FIRE = def('SURF_FIRE', P(W0, {pelT: [0, -.2, -.3], pelvis: [-4, 0, 0], chest: [-4, 0, 0], neck: [6, 0, 0], head: [2, 0, 0]}));
// the P3 crawl gait base (A raised, model_p3 §3: "A stays raised"), and the low crouch with the tail cocked (tail_p3)
const CRAWL_A = def('CRAWL_A', P(W0, {pelT: [0, .1, 0], ...tg('a', 4.0, 3.8, -2.4, Z)}));
const P3_COCK = def('P3_COCK', tailYaw(W0, [-55, -8], [34, 22, 18, 14, 10, 8, 6, 6], {pelT: [0, -.5, 0], pelvis: [-6, -10, 0], chest: [-4, 8, 0], neck: [6, 0, 0], head: [6, 0, 0]}));
const P3_WHIP = def('P3_WHIP', tailYaw(W0, [-10, 2], [28, 14, 10, 6, 4, 2, 0, 0], {pelT: [0, -.5, 0], pelvis: [-6, 4, 0], chest: [-4, -4, 0]}));
const P3_FOLLOW = def('P3_FOLLOW', tailYaw(W0, [-6, 2], [-30, -14, -10, -8, -6, -4, -2, -2], {pelT: [0, -.4, 0], pelvis: [-5, 8, 0], chest: [-4, -8, 0]}));
const P3_COCK2 = def('P3_COCK2', tailYaw(W0, [-50, -8], [-34, -22, -18, -14, -10, -8, -6, -6], {pelT: [0, -.6, -.4], pelvis: [-8, 10, 0], chest: [-4, -8, 0], neck: [6, 0, 0], head: [6, 0, 0]}));
const P3_WHIP2 = def('P3_WHIP2', tailYaw(W0, [-4, 2], [-28, -14, -10, -6, -4, -2, 0, 0], {pelT: [0, -.6, -.4], pelvis: [-8, -4, 0], chest: [-4, 4, 0]}));
const P3_FOLLOW2 = def('P3_FOLLOW2', tailYaw(W0, [-2, 2], [30, 14, 10, 8, 6, 4, 2, 2], {pelT: [0, -.5, -.2], pelvis: [-6, -8, 0], chest: [-4, 8, 0]}));
// the unfold (stand_p3, v6 f522-f600): the head lifts first and the hood swings back while the body is still low
const UNF_4 = def('UNF_4', mix(W0, M0, .55, {hood_hinge: [40, 0, 0], head: [-14, 0, 0], neck: [10, 0, 0]}));
const UNF_8 = def('UNF_8', mix(M0, U0, .35, {hood_hinge: [80, 0, 0]}));
const UNF_11 = def('UNF_11', mix(M0, U0, .8));
// the fold (crouch_p3, v6 f756-f804): hunch, then down onto the hands
const FOLD_3 = def('FOLD_3', mix(HUNCH, M0, .45));

// ==== procedural layers: the travelling tail sine (R17), breathing, gaits =============================================
const TAILS = ['tail_1', 'tail_2', 'tail_3', 'tail_4', 'tail_5', 'tail_6', 'tail_7', 'tail_tip'];
const K = (t, p, e) => (e ? [t, p, e] : [t, p]);
// the idle tail (R17): a travelling sine on the tail yaws, amp degrees, period t, lag t per segment
function tailWave(p, t, {amp = 6, period = 60, lag = 8} = {}) {
  const o = deep(p);
  TAILS.forEach((k, i) => { o[k] = [o[k][0], o[k][1] + amp * Math.sin(2 * Math.PI * (t - lag * i) / period), o[k][2]]; });
  return floorGuard(o);
}
// a breathing loop: A -> B -> A over len (cosine), linear keys every step ticks, with the tail sine
function breathe(A, B, len, step, wave = {}) {
  const keys = [];
  for (let t = 0; t <= len; t += step) keys.push(K(t, tailWave(lerpPose(A, B, (1 - Math.cos(2 * Math.PI * t / len)) / 2), t, wave), 'l'));
  return keys;
}
// a sway loop: A -> L -> A -> R -> A (sine), linear keys every step ticks, with the tail sine
function sway(A, L, R, len, step, wave = {}) {
  const keys = [];
  for (let t = 0; t <= len; t += step) { const u = Math.sin(2 * Math.PI * t / len); keys.push(K(t, tailWave(u >= 0 ? lerpPose(A, L, u) : lerpPose(A, R, -u), t, wave), 'l')); }
  return keys;
}
// A gait loop: every listed foot swings once per cycle (start tick, duration) along z (stride, toward -z = forward)
// with a sine lift, and slides back linearly during its stance (the module moves the anchor forward at stride / len
// per tick, so planted feet stay put on the ground); body = (base, t) -> pose. Keys every `step` ticks, linear.
function gait(len, step, feet, body) {
  const keys = [];
  for (let t = 0; t <= len; t += step) {
    const p = body(t);
    for (const [L, s, t0, dur, stride, lift, at] of feet) {
      const W = at || p[`tg_${L}_${s}`], tau = ((t - t0) % len + len) % len;
      let dz, dy = 0;
      if (tau < dur) { const u = tau / dur; dz = stride / 2 - stride * (1 - Math.cos(Math.PI * u)) / 2; dy = lift * Math.sin(Math.PI * u); }
      else dz = -stride / 2 + stride * (tau - dur) / (len - dur);
      p[`tg_${L}_${s}`] = [W[0], W[1] + dy, W[2] + dz];
    }
    keys.push(K(t, finish(p), 'l'));
  }
  return keys;
}
// in-place steps (turns, the crab walk): each foot lifts by `lift` over its window and replants where it was
function steps(len, step, feet, body) {
  const keys = [];
  for (let t = 0; t <= len; t += step) {
    const p = body(t);
    for (const [L, s, t0, dur, lift, out = 0] of feet) {
      const tau = ((t - t0) % len + len) % len;
      if (tau >= dur) continue;
      const u = Math.sin(Math.PI * tau / dur), W = p[`tg_${L}_${s}`], sx = s === 'l' ? 1 : -1;
      p[`tg_${L}_${s}`] = [W[0] + sx * out * u, W[1] + lift * u, W[2]];
    }
    keys.push(K(t, finish(p), 'l'));
  }
  return keys;
}
const withRot = (p, r) => Object.assign(deep(p), {rot: r});
// a blend keyed on every tick with the floor guard on each key (a long curled tail unrolling onto the floor would dip
// through it in a plain channel blend)
const EASEF = {io: u => u * u * (3 - 2 * u), i: u => u * u, o: u => 1 - (1 - u) * (1 - u), l: u => u};
const guarded = (A, B, t0, t1, e = 'io') => Array.from({length: t1 - t0}, (_, i) => { const u = EASEF[e]((i + 1) / (t1 - t0)); return K(t0 + i + 1, floorGuard(lerpPose(A, B, u)), 'l'); });
const ARMS_LIFT = def('ARMS_LIFT', P(C0, {...rear(.3, {head: -8}), ...tg('a', 5.2, 4.4, -1.2, Z), ...tg('b', 2.4, .4, -2.6), ...tg('c', 2.9, .4, 1.6)}));
const COIL = def('COIL', mix(ARMS_LIFT, COLUMN, .55));
const COLUMN_REL = def('COLUMN_REL', P(COLUMN, {chest: [COLUMN.chest[0] + 6, 0, 0], shoulders: [COLUMN.shoulders[0], 0, 0], neck: [COLUMN.neck[0], 0, 0], tSweep: 10,
  ...tg('a', 1.4, 8.6, -2.6, Z), ...tg('b', 2.2, 3.6, -2.4, Z)}));
const COLUMN2 = def('COLUMN2', P(COLUMN, {chest: [COLUMN.chest[0], 28, 0], shoulders: [COLUMN.shoulders[0], 28, 0], pelT: [0, COLUMN.pelT[1] + .2, COLUMN.pelT[2]]}));
const LUNGE_END = def('LUNGE_END', P(LUNGE, {chest: [-6, -26, 0], ...tgR('a', 4.6, 1.0, -2.6, Z), ...tg('a', 5.6, 1.0, -1.2, Z)}));
const CROSS_PULL = def('CROSS_PULL', P(CROSS, {...tg('a', 1.8, 1.8, -3.6, Z)}));
const SWIRL2 = def('SWIRL2', P(SWIRL, {chest: [SWIRL.chest[0], -20, 0], shoulders: [SWIRL.shoulders[0], -14, 0]}));
const REACH_FLASH = def('REACH_FLASH', P(REACH, {head: [REACH.head[0] - 10, 0, 0], ...tgR('a', -.9, 8.6, -.6, Z)}));
const TALLEST_FWD = def('TALLEST_FWD', P(TALLEST, {...rear(.85, {head: -24, y: .8, lean: 16}), ...tg('a', 3.8, 7.0, -3.4, Z), ...tg('b', 2.4, 6.0, -3.6, Z), ...tg('c', 2.7, .4, .6)}));
const BURST_P3 = def('BURST_P3', mix(MOUND, HOOP, .5, {pelT: [0, 1.8, -.1]}));
const MOUND_LIT = def('MOUND_LIT', P(MOUND, {pelT: [0, -.8, .2], pelvis: [-2, 0, 0], head: [4, 0, 0], hood_hinge: [20, 0, 0]}));
const WHIRL_A = def('WHIRL_A', mix(MOUND_LIT, WHIRL, .5));
const WHIRL_B = def('WHIRL_B', P(WHIRL, {tSweep: -60, a_up_l: [0, -40, 80], b_up_l: [0, -50, 70]}));
const SEATED_LIT = def('SEATED_LIT', Pd(SEATED, {hood_hinge: [8, 0, 0], head: [-4, 0, 0], chest: [2, 0, 0]}));
const ALOFT_RISE = def('ALOFT_RISE', mix(SEATED_LIT, ALOFT, .35));
const KNEEL_LEAN = def('KNEEL_LEAN', Pd(KNEEL, {pelvis: [-10, 0, 0], chest: [-8, 0, 0], head: [-8, 0, 0]}));
const FALLING = def('FALLING', mix(KNEEL_LEAN, FALLEN, .45));
const HUNCH_MID = def('HUNCH_MID', mix(HUNCH, M0, .5));
const SURF_DOWN = def('SURF_DOWN', P(MOUND, {pelT: [0, -1.2, .2]}));
// tail_p3: the coil comes down with the tail already cocked for swing 2
const SCOIL_LOW2 = def('SCOIL_LOW2', finish(Object.assign(deep(SCOIL_LOW), Object.fromEntries(TAILS.map(k => [k, P3_COCK2[k].slice()])))));
// move_strike_p3: the wheel slams down with the tail still curled, then the tail unrolls onto the water (61-66)
const BELLY_TAILUP = def('BELLY_TAILUP', P(BELLY_FLOP, {tCurl: 10, tLift: -62}));
// the ring opening after the slam (61 -> 65): the tail uncurls while it swings out sideways (tSweep), so no tail segment
// turns more than ~110 deg per tick (a straight uncurl in 4 t either exceeds that or passes 3-6 b under the floor)
// The wheel rolls on the water (v5 f936-f954): from 55 the roll is keyed per tick with the height that keeps the ring's
// lowest joint 0.62 b over the floor, the R2 tail-root sheath and plates clear of the water (the roll pivot is not the
// ring's centre, so a plain blend bobs 0.2-1.4 b).
const groundY = p => { const o = solve(p); return Math.min(...BONES.filter(b => b.name !== 'root').map(b => (b.tip ? carry(o, b.name, b.tip) : o[b.name].t)[1])); };
const wheelAt = deg => { const p = withRot(HOOP, [deg, 0, 0]); p.pos = [0, +(0.62 - groundY(p)).toFixed(3), 0]; return p; };
const HOOP_DOWN = wheelAt(-360), FLOP_SW = withRot(P(BELLY_FLOP, {tSweep: 45}), [-360, 0, 0]);
const RING_OPEN_A = Object.assign(lerpPose(HOOP_DOWN, FLOP_SW, .25), {tCurl: -18, tLift: -10, tSweep: 175});
const RING_OPEN_B = Object.assign(lerpPose(HOOP_DOWN, FLOP_SW, .75), {tCurl: -2, tLift: 10, tSweep: 120});

// ==== CLIP_KEYS: the motion of every clip on the played timeline (events: CLIP_TABLE) ==================================
export const CLIP_KEYS = {
  // E (v1 0-107): rises out of the dark pool hood first (the follow_y rise, SINK_KNOTS), half-stands, the right A arm
  // reaches up and touches the hanging Heart at 47, flash 60, the arm comes down, crouch 91, roar 100
  entrance_p1: () => [K(0, EMERGE), K(3, EMERGE), K(16, mix(EMERGE, HALF, .45)), K(29, HALF, 'o'), K(33, mix(HALF, REACH, .25)), K(47, REACH, 'o'), K(57, REACH),
    K(60, REACH_FLASH, 'o'), K(70, REACH_LOW, 'io'), K(84, HALF), K(91, CROUCH, 'i'), K(96, CROUCH_LOW, 'o'), K(100, ROAR, 'o'), K(106, ROAR), K(110, CROUCH)],
  idle_p1: () => breathe(CROUCH, CROUCH_IN, 60, 5),
  // pivot steps (v1 15.10): B_L, C_R, B_R, C_L lift in turn, the pelvis counter-rolls
  turn_p1: () => steps(20, 1, [['b', 'l', 0, 5, .55, .15], ['c', 'r', 5, 5, .5, .15], ['b', 'r', 10, 5, .55, .15], ['c', 'l', 15, 5, .5, .15]],
    t => P(C0, {pelvis: [0, 0, 2.5 * Math.sin(2 * Math.PI * t / 10)], chest: [0, -2 * Math.sin(2 * Math.PI * t / 20), 0], pelT: [0, -.08, 0]})),
  turn_p1_step: () => steps(10, 1, [['b', 'l', 0, 5, .6, .2], ['c', 'r', 5, 5, .55, .2]], t => P(C0, {pelvis: [0, 0, 2.5 * Math.sin(Math.PI * t / 5)], chest: [0, 4 * Math.sin(Math.PI * t / 10), 0], pelT: [0, -.08, 0]})),
  // the spider crawl (v1 15.60): diagonal tripods {B_L, C_R, A_R} 0-8 and {B_R, C_L, A_L} 8-16, stride 2 b (0.25 b/t)
  crawl_p1: () => gait(16, 2, [['b', 'l', 0, 8, 2.0, .6, [2.4, .4, -2.9]], ['c', 'r', 0, 8, 2.0, .6, [-2.9, .4, 2.6]], ['a', 'r', 0, 8, 2.2, .8, [-4.8, .6, -2.4]],
    ['b', 'r', 8, 8, 2.0, .6, [-2.4, .4, -2.9]], ['c', 'l', 8, 8, 2.0, .6, [2.9, .4, 2.6]], ['a', 'l', 8, 8, 2.2, .8, [4.8, .6, -2.4]]],
    t => P(LOW, {pelvis: [-3, 0, 2 * Math.sin(2 * Math.PI * t / 16)], pelT: [0, -.45 + .05 * Math.cos(4 * Math.PI * t / 16), .1], chest: [-3, 2 * Math.sin(2 * Math.PI * t / 16), 0], tail_1: [3, -4 * Math.sin(2 * Math.PI * t / 16), 0]})),
  // stops (LOW -> CROUCH at the plant 8), rises into the half-stand with the core lit (v1 17.40)
  crawl_stop_p1: () => [K(0, LOW), K(8, CROUCH, 'o'), K(16, HALF, 'o'), K(24, HALF), K(32, CROUCH)],
  // the crab side-walk (v2 13.50): C_L 0, B_L 9, C_R 18, B_R 27, heavy thumps, the hump rolls toward the planted side
  walk_p1: () => steps(36, 3, [['c', 'l', 0, 8, .6, .3], ['b', 'l', 9, 8, .7, .3], ['c', 'r', 18, 8, .6, .3], ['b', 'r', 27, 8, .7, .3]],
    t => P(C0, {pelvis: [0, 0, 4 * Math.sin(2 * Math.PI * (t - 4) / 36)], pelT: [0, .12 * Math.abs(Math.sin(2 * Math.PI * t / 18)) - .05, 0], chest: [1.5 * Math.sin(2 * Math.PI * t / 18), 0, -2 * Math.sin(2 * Math.PI * (t - 4) / 36)]})),
  // 잠복 돌진 (v1 6.30): rear 0-4, dive 4-8, sink 8-22 (follow_y), hidden, burst 44, erupt 44-49, loom 49-61, wind, the
  // lunge-sweep 64 (the module glides 7 b), land 77
  burrow_strike: () => [K(0, CROUCH), K(3, REAR, 'o'), K(7, DIVE, 'i'), K(13, SPLAY, 'l'), K(21, SPLAY), K(43, EMERGE), K(49, ERUPT, 'o'), K(56, LOOM, 'io'),
    K(61, LOOM_WIND, 'io'), K(64, LUNGE, 'l'), K(71, LUNGE_END, 'o'), K(77, LAND, 'i'), K(82, CROUCH, 'o')],
  // R (v2 4.62): crouch lower 0-4, sink 4-14 as brown root chunks
  sink_p1: () => [K(0, CROUCH), K(4, CROUCH_LOW, 'o'), K(13, SPLAY, 'l'), K(17, SPLAY)],
  // R (v2 5.60): appears on the player as the upright hooded figure (scale-in 1-4), settles; then rotation
  emerge_on_p1: () => [K(0, HOODED), K(1, HOODED), K(12, HOODED_SWAY, 'o'), K(24, HOODED)],
  burrow_in_p1: () => [K(0, CROUCH), K(4, REAR, 'o'), K(8, DIVE, 'i'), K(14, SPLAY, 'l'), K(23, SPLAY)],
  // 발광 (v1 30.80): the crown pokes out at 5, the hood at 10 (SINK_KNOTS), out 21, settles into the crouch
  emerge_crown_p1: () => [K(0, EMERGE), K(10, EMERGE), K(21, HALF, 'o'), K(30, HALF), K(40, CROUCH)],
  // 생명의 손 (v1 18.60): spread, swirl 5-27 (the anchor spins 360), hands overhead 27, plunge 30, buried while the four
  // remote stalks slam (body dips 62/69/75/82), upright on the buried hands 100, pull out, the mantle flower 118, fold
  hands: () => [K(0, CROUCH), K(5, SPREAD, 'o'), K(16, SWIRL), K(24, SWIRL2), K(27, OVERHEAD, 'io'), K(30, PLUNGE, 'i'), K(36, PLUNGE_DEEP, 'o'), K(60, PLUNGE_DEEP),
    ...[62, 69, 75, 82].flatMap(s => [K(s, PLUNGE_DIP, 'i'), K(s + 3, PLUNGE_DEEP, 'o')]), K(100, CROSS, 'io'), K(108, CROSS_PULL), K(118, FLOWER, 'o'), K(124, FLOWER),
    K(134, CROUCH_LOW, 'i'), K(140, CROUCH, 'o')],
  // 발광하는 파수꾼 (v1 34.60): arms lift, coil into the spiral column (36), slam 1 (47), re-rear straight out of the slam
  // (52-65: readable 18 t before slam 2, plan §14 10-20 rule), slam 2 (70), leap (77),
  // apex (83), head-first dive (90), slam 3 (101), settle
  glow_slams: () => [K(0, CROUCH), K(9, ARMS_LIFT, 'o'), K(23, COIL), K(36, COLUMN, 'o'), K(42, COLUMN2), K(45, COLUMN_REL, 'o'), K(47, SLAM, 'i'), K(52, SLAM), K(57, HALF, 'io'), K(65, ARMSUP, 'o'),
    K(70, SLAM, 'i'), K(73, SLAM), K(75, CROUCH_LOAD, 'io'), K(77, LEAP_UP, 'o'), K(83, AIR, 'o'), K(90, AIR), K(97, DIVEDOWN, 'i'), K(101, SLAM, 'i'), K(108, SLAM),
    K(121, CROUCH, 'o'), K(131, CROUCH)],
  // 초목이 시든 풍경 (v2 6.75): from the hooded figure, arms up 0-8, rears over the player, sways while the disc fills,
  // crashes sideways at 40, spins on the ground 47-71 (the anchor), sprawls, pushes up, stands
  rotation: () => [K(0, HOODED), K(8, ARMSUP, 'o'), K(18, LEAN, 'o'), K(26, LEAN_L), K(32, LEAN_R), K(36, LEAN), K(40, CRASH, 'i'), K(47, CRASH), K(59, CRASH_B), K(71, CRASH),
    K(80, SPRAWL, 'o'), K(92, PUSHUP), K(100, HALF, 'o'), K(115, CROUCH), K(130, CROUCH)],
  // 생명의 꼬리 x2 (v2 15.73): brace, the tail rises into an S, cocks to the left (23), swing 1 28-35 (the anchor turns
  // +200: the tail lags, then whips through), recoil, cock to the right (48), swing 2 52-59 (reverse), sprawl, rise
  tail_p1x2: () => [K(0, CROUCH), K(8, CROUCH_LOW), K(20, TAIL_S, 'o'), K(23, TAIL_COCK), K(27, TAIL_COCK), K(31, TAIL_WHIP, 'i'), K(35, TAIL_WHIP), K(39, TAIL_FOLLOW, 'o'),
    K(45, TAIL_COCK2, 'io'), K(51, TAIL_COCK2), K(55, TAIL_WHIP2, 'i'), K(59, TAIL_WHIP2), K(63, TAIL_FOLLOW2, 'o'), K(72, TAIL_REST, 'io'), K(86, TAIL_REST), K(106, PUSHUP, 'io'),
    K(127, CROUCH)],
  // 근접 콤보 (v2 24.45): a low right-arm sweep (hit 14) / b rear + double slam (17) / c twist + spin (the anchor) / d the
  // tallest rear and the leaping slam (27, the module glides 2.5 b) / back to the crouch
  combo_a: () => [K(0, CROUCH), K(9, SWEEP_BACK, 'o'), K(14, SWEEP_THRU, 'i'), K(18, SWEEP_END, 'o'), K(29, CROUCH)],
  combo_b: () => [K(0, CROUCH), K(12, COMBO_HIGH, 'o'), K(17, DOUBLE_SLAM, 'i'), K(22, DOUBLE_SLAM), K(34, CROUCH_LOW, 'io'), K(44, CROUCH)],
  combo_c: () => [K(0, CROUCH), K(4, TWIST, 'o'), K(8, SPIN_OUT, 'io'), K(15, SPIN_OUT), K(20, CROUCH, 'o')],
  combo_d: () => [K(0, CROUCH), K(20, TALLEST, 'o'), K(22, TALLEST_FWD), K(27, SLAM_FAR, 'i'), K(33, SLAM_FAR), K(43, CROUCH_LOW, 'io'), K(60, CROUCH), K(77, CROUCH)],
  combo_end: () => [K(0, CROUCH_IN), K(20, CROUCH)],
  // 소생 단계 진입: staggers, flickers, sinks as root chunks 20-45
  sink_revive: () => [K(0, CROUCH), K(4, STAGGER, 'o'), K(10, STAGGER2), K(16, STAGGER), K(22, SPLAY, 'io'), K(44, SPLAY), K(60, SPLAY)],
  // CS (w2, v5 4.4-12.45): hidden 0-59, bursts out of the water as a curled ball (60), rises hunched, reaches with A_r
  // (88), flash 96, unfurls arms up (104) into T (118), sways
  revival: () => [K(0, MOUND), K(59, MOUND), K(64, BALL, 'o'), K(72, CURL), K(80, HUNCH, 'io'), K(88, REACH_P3, 'o'), K(96, REACH_P3), K(104, V, 'o'), K(118, UPRIGHT, 'o'),
    K(130, SWAY_L), K(145, SWAY_R), K(160, UPRIGHT)],
  idle_p3: () => sway(UPRIGHT, SWAY_L, SWAY_R, 60, 5, {amp: 5}),
  // the C hands shuffle on the water while the module turns the anchor (<= 6 deg/t), the spine counter-lags
  turn_p3: () => { const keys = []; for (let t = 0; t <= 20; t += 5) { const u = Math.sin(2 * Math.PI * t / 20), p = deep(U0);
    p.c_up_l = [U0.c_up_l[0], U0.c_up_l[1], U0.c_up_l[2] + 7 * Math.max(0, Math.sin(2 * Math.PI * (t - 15) / 20))]; p.c_up_r = [U0.c_up_r[0], U0.c_up_r[1], U0.c_up_r[2] - 7 * Math.max(0, Math.sin(2 * Math.PI * (t - 5) / 20))];
    p.b_up_l = [U0.b_up_l[0], U0.b_up_l[1], U0.b_up_l[2] + 4 * u]; p.b_up_r = [U0.b_up_r[0], U0.b_up_r[1], U0.b_up_r[2] + 4 * u];
    p.chest = [U0.chest[0], -3 * u, 0]; p.shoulders = [U0.shoulders[0], -2 * u, 0]; keys.push(K(t, p, 'l')); } return keys; },
  // the crawl walk (v5 f1176-f1260): a spider on B and C with A raised, steps B_L 0, C_R 8, B_R 16, C_L 24
  walk_p3: () => gait(32, 2, [['b', 'l', 0, 8, 2.0, .6, [2.4, .4, -2.9]], ['c', 'r', 8, 8, 2.0, .6, [-2.9, .4, 2.6]], ['b', 'r', 16, 8, 2.0, .6, [-2.4, .4, -2.9]], ['c', 'l', 24, 8, 2.0, .6, [2.9, .4, 2.6]]],
    t => P(CRAWL_A, {pelvis: [0, 0, 3 * Math.sin(2 * Math.PI * t / 32)], pelT: [0, .1 + .06 * Math.cos(4 * Math.PI * t / 32), 0], tail_1: [0, -5 * Math.sin(2 * Math.PI * t / 32), 0], tail_3: [0, 5 * Math.sin(2 * Math.PI * (t - 8) / 32), 0]})),
  // the fold (v6 f756-f804, 7 t): hunch, down onto the hands; the face hides at 6 under the closing hood
  crouch_p3: () => [K(0, UPRIGHT), K(3, FOLD_3, 'io'), K(5, mix(FOLD_3, W0, .55)), K(7, CRAWL, 'o'), K(8, CRAWL)],
  // the unfold (v6 f522-f600, 14 t): the head lifts and the hood swings back first, the body stands, the arms unroll
  stand_p3: () => [K(0, CRAWL), K(4, UNF_4, 'io'), K(8, UNF_8), K(11, UNF_11), K(13, UPRIGHT, 'o'), K(14, UPRIGHT)],
  // 이동 돌진 (v5 12.45): fold 0-7, mound 8, sink (follow_y) and travel hidden 16-41, burst 44, hoop 44-49, the wheel roll
  // 49-61 (keyed root pitch -360), slam 61, the tail lands 65, the 360-degree ground whip 66-72 (the anchor), rise, stand
  move_strike_p3: () => [K(0, UPRIGHT), K(4, HUNCH_MID, 'io'), K(7, CRAWL, 'o'), K(10, MOUND, 'i'), K(15, MOUND), K(41, MOUND), K(44, BURST_P3, 'o'), K(49, Object.assign(deep(HOOP), {pos: [0, 1.2, 0]}), 'o'),
    ...[55, 56, 57, 58, 59, 60, 61].map(t => K(t, wheelAt(-180 - 30 * (t - 55)), 'l')),
    // the ring opens sideways: the tail half swings out to the boss's left (62-64) and lands trailing there at the tail
    // event (65), ready for the ground whip (FLOOR_SKIP: it grazes up to ~2.5 b under the water at 62-64, inside the
    // belly-flop splash of the slam (plan §8.3 Q1 fx); no 4-tick opening of the under-curled ring stays over the floor
    // within 120 deg per tick: a straight uncurl passes 3-6 b under it, a lifted one more)
    K(62, RING_OPEN_A, 'l'), K(64, RING_OPEN_B, 'l'), K(65, withRot(TAIL_SWEEP, [-360, 0, 0]), 'l'), K(69, withRot(TAIL_SWEEP, [-360, 0, 0]), 'io'),
    K(72, withRot(TAIL_SWEEP, [-360, 0, 0])), K(78, withRot(CRAWL, [-360, 0, 0]), 'o'), K(85, withRot(CRAWL, [-360, 0, 0])), K(88, withRot(MID, [-360, 0, 0]), 'io'),
    K(91, withRot(UPRIGHT, [-360, 0, 0]), 'o'), K(92, withRot(UPRIGHT, [-360, 0, 0]))],
  // 종말의 여파 (w1, v5): charge curled on the water (lit), whirl up 18-36 (the anchor spins 360), land seated 40 (the
  // field), the domes 44-62, rise aloft 76-84 (px aloft), hover in a V, rain 134, the blast 156, descend 162-176, the
  // domes pop 189 with a burst at the boss, stand
  aftermath: () => [K(0, CRAWL), K(12, MOUND_LIT, 'o'), K(18, MOUND_LIT), K(23, WHIRL_A, 'o'), K(29, WHIRL, 'io'), K(36, WHIRL_B), K(40, SEATED_LIT, 'i'), K(72, SEATED_LIT),
    K(77, ALOFT_RISE, 'io'), K(84, ALOFT, 'o'), K(100, ALOFT_HI, 'io'), K(118, ALOFT, 'io'), K(134, ALOFT_HI, 'io'), K(150, ALOFT, 'io'), K(156, BLAST, 'i'), K(162, BLAST),
    K(176, UPRIGHT, 'io'), K(186, HUNCH, 'io'), K(190, V, 'o'), K(205, TALL, 'io'), K(224, UPRIGHT)],
  // 증폭의 풀 (v5 32.40): hunch, arms curl in, rise lit, V at the crown, the launch flick (35), the curled ball, cool and
  // idle open (punish window), flicks for locks 2 / 3 (79 / 82), arms up V
  shells: () => [K(0, UPRIGHT), K(8, HUNCH, 'o'), K(14, HUNCH_CURL), K(26, TALL, 'o'), K(33, V, 'io'), K(35, LAUNCH, 'i'), K(38, BALL, 'o'), K(45, BALL), K(52, UPRIGHT, 'io'),
    K(64, SWAY_L), K(74, T_WIDE, 'io'), K(79, FLICK_L, 'i'), K(82, FLICK_R, 'i'), K(88, V, 'o'), K(100, V), K(113, UPRIGHT)],
  // 수면 포격 sink: fold 0-7, mound, sink 8-11 (hidden 12)
  sink_p3: () => [K(0, UPRIGHT), K(4, HUNCH_MID, 'io'), K(7, CRAWL, 'o'), K(10, MOUND, 'i'), K(19, MOUND), K(20, MOUND)],
  // 수면 포격 surface: rises out of the water in the crawl (0-4), aims the hood, the flat shot at 10, recoils, settles
  surface_p3: () => [K(0, SURF_DOWN), K(4, SURF_AIM, 'o'), K(9, SURF_AIM), K(10, SURF_FIRE, 'i'), K(13, SURF_FIRE), K(24, CRAWL, 'io'), K(40, CRAWL)],
  // 생명의 꼬리 P3 (v6 2.50): low crouch with the tail cocked left (3), swing 1 14-21 (the anchor +200), rise into the
  // tall S-coil (24-36), lunge down (36-40), cock right, swing 2 46-53 (reverse, low), rise 57-86 into UPRIGHT
  tail_p3: () => [K(0, CRAWL), K(3, mix(CRAWL, P3_COCK, .7), 'o'), K(7, P3_COCK, 'io'), K(11, P3_COCK), K(15, P3_WHIP, 'i'), K(19, P3_WHIP), K(23, P3_FOLLOW, 'o'), K(30, SCOIL, 'io'), K(34, SCOIL), K(40, SCOIL_LOW2, 'io'),
    K(43, P3_COCK2, 'io'), K(47, P3_WHIP2, 'i'), K(51, P3_WHIP2), K(55, P3_FOLLOW2, 'o'), K(57, P3_FOLLOW2), K(64, UNF_4, 'io'), K(72, UNF_8), K(79, UNF_11), K(86, UPRIGHT, 'o'),
    K(87, UPRIGHT)],
  // 생명의 나선 (v6 8.75): dark curl (4-10), rise, V + light column (14), arms wide while the seed-orbs gather (19),
  // aim / thrust A (37 / 42), aim / thrust B (43 / 48), hold, recover
  spikes: () => [K(0, UPRIGHT), K(4, UPRIGHT), K(8, CURL, 'io'), K(10, CURL), K(14, V, 'o'), K(19, T_WIDE, 'io'), K(28, mix(T_WIDE, SWAY_L, .6)), K(37, AIM, 'io'), K(42, THRUST, 'i'),
    K(45, AIM, 'o'), K(48, THRUST, 'i'), K(54, THRUST), K(65, TALL, 'io'), K(72, UPRIGHT)],
  // death (proposal, MO §6.17): the hood snaps back, flicker, droop (30), kneel (55), topple onto the water (70-82),
  // wither (85), sink 100-117
  death: () => [K(0, UPRIGHT), K(3, HIT_SNAP, 'o'), K(8, HIT_SNAP), K(18, mix(HIT_SNAP, DROOP, .4)), K(30, DROOP, 'io'), K(55, KNEEL, 'io'), K(64, KNEEL_LEAN), K(72, FALLING, 'i'),
    K(82, FALLEN, 'i'), K(100, FALLEN), K(119, FALLEN), K(120, FALLEN)],
};
// spans the floor pass leaves alone (see the clip's keys)
const FLOOR_SKIP = {move_strike_p3: [[62, 64]]};
// first-segment blends (the compiler's minimum first segment; a clip entered from any pose eases in over these ticks)
const BLEND = {combo_end: 10, death: 6, idle_p1: 4, idle_p3: 6, crawl_stop_p1: 4};
// hand / look events beyond the stub (plan R8 / R12): the revival keeps the crawl hands and the face covered until the
// hood swings back before the flash
const EXTRA_HANDS = {revival: [[0, 'p3_curl']]};
const LOOK_FIX = {revival: [[0, 'face', 'hidden'], [92, 'face', 'p3_idle']]};

// ==== burrow sinks (plan R9) ===========================================================================================
// The root sinks to SINK_DEPTH under the opaque floor through the follow_y offsets (no part keys), fully buried parts at
// scale 0 inside the hidden span; the default emergence rises back in RISE ticks. SINK_KNOTS overrides the default with
// the footage pacing (the entrance and the crown emergence rise slowly, hood first; the relocate appears in place).
export const SINK_DEPTH = -6, SINK_STEP = .25, RISE = 6;
export const SINK_TABLE = Array.from({length: Math.round(-SINK_DEPTH / SINK_STEP) + 2}, (_, i) => -(i + 1) * SINK_STEP);   // -0.25 .. -6.5
const SINK_START = {burrow_strike: 6, sink_p1: 4, burrow_in_p1: 6, sink_revive: 20, move_strike_p3: 8, sink_p3: 8, death: 100};
const SINK_KNOTS = {
  entrance_p1: [[0, -6], [3, -6], [16, -4.5], [31, 0]],
  emerge_crown_p1: [[0, -6], [4, -5.75], [10, -3.75], [21, 0]],
  emerge_on_p1: [[0, -6], [.5, 0]],
  surface_p3: [[0, -6], [4, 0]],
};
function sinkKnots(c) {
  if (SINK_KNOTS[c.name]) return SINK_KNOTS[c.name];
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

// ==== hand variants of the phase-1 clips (R8), from the motion ========================================================
// A phase-1 hand counts as lifted while its IK target is >= 0.3 b over its bind wrist (A p1_raised, B / C p1_curl).
// The variant swaps a quarter of the way into the lift and one tick before the touch-down; loops state every hand at 0.
const HAND_LIFT = {a: WB.a[1] + .3, b: WB.b[1] + .3, c: WB.c[1] + .3}, HAND_SWAP = {a: WB.a[1] + .45, b: WB.b[1] + .45, c: WB.c[1] + .45};
const VAR = {a: ['p1_planted', 'p1_raised'], b: ['p1_open', 'p1_curl'], c: ['p1_open', 'p1_curl']};
function autoHands(c, keys) {
  const ev = [];
  for (const L of LIMBS) for (const s of SIDES) {
    const part = `${L}_hand_${s}`, lifted = p => (p[`ik_${L}_${s}`] ?? 0) >= .5 && p[`tg_${L}_${s}`][1] >= HAND_SWAP[L] - 1e-6;
    let st = lifted(keys[0][1]);
    if (st || c.loop) ev.push([0, part, VAR[L][+st]]);
    for (let i = 1; i < keys.length; i++) {
      const [t0] = keys[i - 1], [t1, p] = keys[i], now = lifted(p);
      if (now === st) continue;
      const te = now ? t0 + Math.max(1, Math.round(.25 * (t1 - t0))) : t1;
      ev.push([Math.min(te, c.len), part, VAR[L][+now]]);
      st = now;
    }
  }
  return ev.sort((x, y) => x[0] - y[0] || x[1].localeCompare(y[1]));
}

// ==== R17 secondary motion (AP-RC2) ======================================================================================
// The soft parts follow the body with inertia: each chain bone's tip is a damped spring follower (damping SEC_DAMP per
// tick, stiffness k: a lag of 2-4 t, an overshoot after a stop, the whip of the second segment that follows the lagging
// first) of where the keyed pose puts it, in the world (the anchor-yaw schedules included, so the anchor spins and the
// tail swings drag and fling the soft parts; FLING adds the spin's centrifugal pull). The follower's offset turns the
// bone (the smallest turn that moves its tip there, at most max degrees); it is keyed per tick where it shows (>
// SEC_MIN deg) and faded out over the last SEC_FADE ticks of a clip, so a chained clip starts from the keyed pose.
// Loops run three cycles and keep the last (periodic). The floor pass runs after it.
const SECONDARY = [
  {bones: ['mantle_l_a', 'mantle_l_b'], k: .32, max: 12}, {bones: ['mantle_r_a', 'mantle_r_b'], k: .32, max: 12},
  {bones: ['hair_l_1', 'hair_l_2'], k: .24, max: 18}, {bones: ['hair_r_1', 'hair_r_2'], k: .24, max: 18},
  {bones: ['hem_a', 'hem_b'], k: .26, max: 14, axes: [0]},   // (pitch only: the floor guard turns the hem in pitch)
  {bones: ['beads_l'], k: .18, max: 24, form: 'p3'}, {bones: ['beads_r'], k: .18, max: 24, form: 'p3'},
];
const SEC_DAMP = .82, SEC_K2 = .75, SEC_FLING = .9, SEC_MIN = 2, SEC_FADE = 8;
// rig frame (forward -Z) -> the world as the anchor's yaw turns it (Minecraft yaw, degrees); toRigV is the inverse for vectors
const yawRot = (v, yaw, inv = false) => { const a = (inv ? 1 : -1) * yaw * Math.PI / 180, c = Math.cos(a), s = Math.sin(a); return [v[0] * c + v[2] * s, v[1], -v[0] * s + v[2] * c]; };
const toWorld = (P, yaw) => yawRot([P[0], P[1], -P[2]], yaw);
const toRigV = (v, yaw) => { const w = yawRot(v, yaw, true); return [w[0], w[1], -w[2]]; };
const axisAngleQ = (ax, ang) => { const s = Math.sin(ang / 2); return [ax[0] * s, ax[1] * s, ax[2] * s, Math.cos(ang / 2)]; };
const qInv = Q => [-Q[0], -Q[1], -Q[2], Q[3]];
const wrap180 = x => ((x + 540) % 360) - 180;
function secondary(c, keys) {
  const chains = SECONDARY.filter(ch => !ch.form || ch.form === c.form);
  const N = c.len + 1, ks = acc({keys}, DEFAULT_POSE), yawD = denseYaw(c);
  const plain = Array.from({length: N}, (_, t) => { const p = sampleShared({keys}, t, ks, {defaults: DEFAULT_POSE}); delete p.ph; return p; });
  const yawAt = t => (yawD ? yawD[Math.min(t, yawD.length - 1)] : 0);
  const sk = {sink: sinkKnots(c)}, off = (t => t)(Object.fromEntries(chains.flatMap(ch => ch.bones).map(b => [b, Array.from({length: N}, () => [0, 0, 0])])));
  const reset = t => (c.hidden || []).some(([a, b]) => t >= a && t <= b) || sinkAt(sk, t) < -.01;
  const cycles = c.loop ? 3 : 1;
  for (const ch of chains) {
    const st = ch.bones.map(() => ({Y: null, V: [0, 0, 0]}));
    for (let u = 0; u < cycles * c.len + (c.loop ? 0 : 1); u++) {
      const t = c.loop ? u % c.len : u, rec = u >= (cycles - 1) * c.len || !c.loop;
      const p = deep(plain[t]);
      if (reset(t)) { st.forEach(x => { x.Y = null; x.V = [0, 0, 0]; }); continue; }
      const yaw = yawAt(t), w = yawD ? (yawAt(t) - yawAt(Math.max(0, t - 1))) * Math.PI / 180 : 0;
      ch.bones.forEach((b, i) => {
        const o = solve(p), X = carry(o, b, BONE[b].tip), Xw = toWorld(X, yaw), S = st[i];
        if (!S.Y) S.Y = Xw.slice();
        else {
          const k = ch.k * (i ? SEC_K2 : 1), fl = [Xw[0], 0, Xw[2]].map(v => v * w * w * SEC_FLING);
          S.V = add(add(times(S.V, SEC_DAMP), times(sub(Xw, S.Y), k)), fl);
          S.Y = add(S.Y, S.V);
        }
        // the follower's offset as the smallest turn of the bone about its joint (in the rig frame)
        const d = sub(X, o[b].t), sR = toRigV(sub(S.Y, Xw), yaw), dd = dot(d, d);
        const perp = sub(sR, times(d, dot(sR, d) / dd)), ax = cross(d, perp), al = len(ax);
        let E = p[b];
        if (al > 1e-6) {
          const ang = Math.min(ch.max * Math.PI / 180, len(perp) / Math.sqrt(dd));
          const R1 = mul(axisAngleQ(times(ax, 1 / al), ang), o[b].R);
          const e1 = eulerOf(mul(qInv(o[BONE[b].parent].R), R1));
          E = e1.map((v, j) => (ch.axes && !ch.axes.includes(j) ? p[b][j] : p[b][j] + wrap180(v - p[b][j])));
        }
        if (rec) off[b][t] = E.map((v, j) => v - p[b][j]);
        p[b] = E;
      });
    }
    if (c.loop) for (const b of ch.bones) off[b][c.len] = off[b][0].slice();
  }
  // fade-out at the end of a non-looping clip, then key every tick where an offset shows
  if (!c.loop) for (const b of Object.keys(off)) for (let t = 0; t < N; t++) { const f = Math.min(1, (c.len - t) / SEC_FADE), g = f * f * (3 - 2 * f); off[b][t] = off[b][t].map(v => v * g); }
  const live = new Uint8Array(N);
  for (const b of Object.keys(off)) for (let t = 0; t < N; t++) if (off[b][t].some(v => Math.abs(v) > SEC_MIN)) live[t] = 1;
  const adds = [];
  for (let t = 0; t < N; t++) {
    if (!(live[t] || live[t - 1] || live[t + 1])) continue;
    const p = deep(plain[t]);
    for (const b of Object.keys(off)) p[b] = p[b].map((v, j) => +(v + off[b][t][j]).toFixed(2));
    const kk = keys.find(x => x[0] === t);
    if (kk) kk[1] = p; else adds.push([t, p, 'l']);
  }
  if (adds.length) { keys.push(...adds); keys.sort((x, y) => x[0] - y[0]); }
}

// Eased segments as linear pieces (AP-RC2): an eased segment of L >= EASE_MIN ticks becomes n = L / 4 (2-4) linear pieces
// through its own eased values at whole ticks, so the speed still builds and settles (slow - fast - slow for 'io',
// accelerating into an impact for 'i') while the client's linear interpolation follows it with a few keys per part
// instead of one per tick; the path through the poses is unchanged.
const EASE_MIN = 4;
function easeKnots(keys) {
  const out = [keys[0]];
  for (let i = 1; i < keys.length; i++) {
    const [t0, p0] = keys[i - 1], [t1, p1, e = 'io'] = keys[i], L = t1 - t0;
    if (e === 'l' || L < EASE_MIN) { out.push(keys[i]); continue; }
    const n = Math.min(4, Math.max(2, Math.round(L / 4)));
    for (let k = 1; k < n; k++) { const tk = t0 + Math.round(L * k / n); if (tk > out[out.length - 1][0] && tk < t1) out.push([tk, lerpPose(p0, p1, EASEF[e]((tk - t0) / L)), 'l']); }
    out.push([t1, p1, 'l']);
  }
  return out;
}

// ==== assembly ==========================================================================================================
// Keys: the clip's CLIP_KEYS (full poses), the hidden spans as vis keys (inserted as sampled poses so the motion is not
// disturbed), a last key at len. Self-checks (thrown at import): keys inside 0..len, strictly increasing, the first at
// 0, every event of the binding table unchanged, hand events inside the clip.
function buildKeys(c) {
  let keys = CLIP_KEYS[c.name]().map(([t, p, e]) => [t, deep(p), e]);
  for (const [, p] of keys) for (const k of Object.keys(p)) if (!(k in DEFAULT_POSE)) delete p[k];
  if (keys[0][0] !== 0) throw new Error(`clip ${c.name}: the first key must be tick 0`);
  if (keys[keys.length - 1][0] < c.len) keys.push([c.len, deep(keys[keys.length - 1][1])]);
  keys.forEach(([t], i) => { if (t > c.len || (i && t <= keys[i - 1][0])) throw new Error(`clip ${c.name}: key ${t} out of order or past len ${c.len}`); });
  const at = t => { const ks = acc({keys}, DEFAULT_POSE); const p = sampleShared({keys}, t, ks, {defaults: DEFAULT_POSE}); delete p.ph; return p; };
  // Phase-1 lift-offs and touch-downs: a lifted hand turns with its forearm, so a straight blend between a planted and a
  // lifted key would tip the fingers through the floor. A key 0.35 b over the planted spot with the planted hand
  // orientation is inserted 30 % into each lift-off and 30 % before each touch-down (the hand leaves and lands flat).
  if (c.form === 'p1') {
    const lifted = (p, L, s) => (p[`ik_${L}_${s}`] ?? 0) >= .5 && p[`tg_${L}_${s}`][1] >= HAND_LIFT[L] - 1e-6;
    const adds = new Map();
    for (let i = 1; i < keys.length; i++) {
      const [t0, p0] = keys[i - 1], [t1, p1, e1] = keys[i], dt = t1 - t0;
      if (dt < 3) continue;
      for (const L of LIMBS) for (const s of SIDES) {
        const a = lifted(p0, L, s), b = lifted(p1, L, s);
        if (a === b) continue;
        const pl = a ? p1 : p0, ta = a ? t1 - Math.max(1, Math.round(.3 * dt)) : t0 + Math.max(1, Math.round(.3 * dt));
        if (!adds.has(ta)) adds.set(ta, {e: e1, o: {}});
        const W = pl[`tg_${L}_${s}`];
        Object.assign(adds.get(ta).o, {[`tg_${L}_${s}`]: [W[0], W[1] + .35, W[2]], [`hf_${L}_${s}`]: pl[`hf_${L}_${s}`].slice()});
      }
    }
    const extra = [...adds].map(([t, {e, o}]) => [t, at(t), e || 'io', o]);
    for (const [t, p, e, o] of extra) { const k = keys.find(x => x[0] === t); if (k) Object.assign(k[1], deep(o)); else keys.push([t, floorGuard(Object.assign(p, deep(o)), true), e]); }
    keys.sort((x, y) => x[0] - y[0]);
  }
  keys = easeKnots(keys);
  // hand eulers: each key's triple is re-expressed (wraps and the (p + 180, 180 - y, r + 180) twin) closest to the previous
  // key's, so the channel blend never takes the long way round (before the floor pass samples the blend, and again after)
  const near = (e, ref) => {
    let best = null;
    for (const c of [e, [e[0] + 180, 180 - e[1], e[2] + 180]]) {
      const u = c.map((v, i) => { let x = v; while (x - ref[i] > 180) x -= 360; while (x - ref[i] < -180) x += 360; return x; });
      const d = u.reduce((a, v, i) => a + Math.abs(v - ref[i]), 0);
      if (!best || d < best[0]) best = [d, u];
    }
    return best[1].map(v => Math.round(v * 100) / 100);
  };
  const nearFix = () => { for (let i = 1; i < keys.length; i++) for (const k of Object.keys(keys[i][1])) if (k.startsWith('hf_')) keys[i][1][k] = near(keys[i][1][k], keys[i - 1][1][k]); };
  nearFix();
  secondary(c, keys);
  // Floor pass: the key poses are guarded at their joints (finish), but the channel blend between them and the R2 models
  // beyond the joints can still dip under the floor (a drape rolled outward one way at one key and the other way at the
  // next passes through the floor). The timing of the motion is kept exactly (the corrections are keyed per tick).
  {
    // (ticks with the burrow sink under way are skipped: parts are meant to be under the floor there)
    // AP-RC2: every visible tick is guarded (modelFloor with the clip's form, continuous from the previous tick); the
    // correction of each guarded channel (the chains, the body height, the IK leg wrists) against the plain blend is
    // then smoothed into an envelope that changes by at most FLOOR_RATE per tick (it starts a little early and lets go
    // late, so a lift never pops), and every tick where it is not zero is keyed (one plain tick either side).
    const sk = {sink: sinkKnots(c)}, skip = [...(c.hidden || []), ...(FLOOR_SKIP[c.name] || [])];
    const hidF = t => skip.some(([a, b]) => t >= a && t <= b) || sinkAt(sk, t) < 0;
    const GC = [...GUARD.flatMap(g => g.bones), 'pelT', ...SIDES.flatMap(s => ['b', 'c'].map(L => `tg_${L}_${s}`))];
    const ks = acc({keys}, DEFAULT_POSE), N = c.len + 1;
    const plain = Array.from({length: N}, (_, t) => { const p = sampleShared({keys}, t, ks, {defaults: DEFAULT_POSE}); delete p.ph; return p; });
    const delta = {};
    for (const ch of GC) delta[ch] = [0, 1, 2].map(() => new Float64Array(N));
    let ref = null;
    for (let t = 0; t < N; t++) {
      if (hidF(t)) { ref = null; continue; }
      const g = modelFloor(deep(plain[t]), c.form, true, ref);
      ref = g;
      for (const ch of GC) for (let j = 0; j < 3; j++) delta[ch][j][t] = g[ch][j] - plain[t][ch][j];
    }
    const live = new Uint8Array(N);
    for (const ch of GC) for (let j = 0; j < 3; j++) {
      const d = delta[ch][j], R = /^(pelT|tg_)/.test(ch) ? FLOOR_RATE.h : FLOOR_RATE.a, eps = /^(pelT|tg_)/.test(ch) ? .005 : .2;
      if (!d.some(v => Math.abs(v) > eps)) continue;
      const env = new Float64Array(N);
      for (let t = 0; t < N; t++) {
        let hi = 0, lo = 0;
        for (let u = 0; u < N; u++) { const w = R * Math.abs(u - t); if (d[u] > 0) hi = Math.max(hi, d[u] - w); else lo = Math.min(lo, d[u] + w); }
        env[t] = hi + lo;
      }
      delta[ch][j] = env;
      for (let t = 0; t < N; t++) if (Math.abs(env[t]) > eps) live[t] = 1;
    }
    const adds = [];
    for (let t = 0; t < N; t++) {
      if (!(live[t] || live[t - 1] || live[t + 1])) continue;
      const p = deep(plain[t]);
      for (const ch of GC) p[ch] = p[ch].map((v, j) => v + delta[ch][j][t]);
      const k = keys.find(x => x[0] === t);
      if (k) k[1] = p; else adds.push([t, p, 'l']);
    }
    if (adds.length) { keys.push(...adds); keys.sort((x, y) => x[0] - y[0]); }
  }
  const vis = [];
  for (const [a, b] of c.hidden || []) { if (a > 0) vis.push([a - 1, 1]); vis.push([a, 0], [b, 0]); if (b < c.len) vis.push([b + 1, 1]); }
  for (const [t, v] of vis) {
    let k = keys.find(x => x[0] === t);
    if (!k) { k = [t, at(t), 'l']; keys.push(k); keys.sort((x, y) => x[0] - y[0]); }
    k[1] = {...k[1], vis: v};
    if (t === vis[0]?.[0] || true) k[2] = k[2] || 'l';
  }
  nearFix();
  // inside a hidden span vis stays 0 on every key; outside it 1
  const hid = t => (c.hidden || []).some(([a, b]) => t >= a && t <= b);
  for (const k of keys) k[1].vis = hid(k[0]) ? 0 : 1;
  return keys;
}
export const CLIPS_REAL = CLIP_TABLE.map(t => {
  const c = {...deep(t), note: ''};
  if (LOOK_FIX[c.name]) c.look_events = [...c.look_events.filter(([, ch]) => ch !== 'face'), ...LOOK_FIX[c.name]].sort((x, y) => x[0] - y[0]);
  c.keys = buildKeys(c);
  c.sink = sinkKnots(c);
  if (BLEND[c.name]) c.blend = BLEND[c.name];
  if (c.form === 'p1') c.hand_events = autoHands(c, c.keys);
  if (EXTRA_HANDS[c.name]) c.hand_events = [...EXTRA_HANDS[c.name], ...(c.hand_events || [])].sort((x, y) => x[0] - y[0]);
  for (const ev of c.hand_events || []) if (ev[0] < 0 || ev[0] > c.len) throw new Error(`clip ${c.name}: hand event ${ev} outside the clip`);
  c.note = `AP-RC2 keys ${c.keys.map(k => k[0]).join(' ')}`;
  return c;
});

// ==== debug poses (static 2-tick loops; dbg_<name>, ignored by the module): the coverage-gate poses, the views and the
// pose glossary (dbg_g_<pose>) for the key-pose renders =====================================================================
const dbg = (name, form, p, note, s = 'CROUCH', hands = []) => ({name: 'dbg_' + name, form, len: 2, loop: true, next: null, events: {}, stance: [s, s],
  px_sets: [[0, form === 'p1' ? 'p1' : 'p3c']], keys: [[0, modelFloor(deep(p), form)], [2, {}]], note, dbg: true,
  hand_events: form === 'p1' ? autoHands({len: 2}, [[0, p]]) : hands});
const GLOSSARY_P3 = ['UPRIGHT', 'CRAWL', 'HUNCH', 'MOUND', 'HOOP', 'SCOIL', 'CURL', 'BALL', 'V', 'CROUCH_OVER', 'BELLY_FLOP', 'KNEEL', 'FALLEN', 'SEATED_LIT', 'ALOFT', 'BLAST',
  'T_WIDE', 'THRUST', 'LAUNCH', 'P3_COCK', 'P3_WHIP', 'SURF_AIM', 'WHIRL', 'UNF_4', 'UNF_8', 'DROOP', 'HIT_SNAP', 'REACH_P3', 'TAIL_SWEEP', 'BURST_P3'];
// the stance (face shown, open B hands) each glossary pose is used with in the clips; the rest show the crawl look
const UPRIGHT_FAMILY = new Set(['UPRIGHT', 'HUNCH', 'CURL', 'BALL', 'V', 'CROUCH_OVER', 'ALOFT', 'BLAST', 'T_WIDE', 'THRUST', 'LAUNCH', 'UNF_8', 'DROOP', 'HIT_SNAP']);
const CURL_HANDS = new Set(['KNEEL', 'FALLEN', 'REACH_P3', 'SCOIL']);
const GLOSSARY_P1 = ['CROUCH', 'CROUCH_IN', 'LOW', 'HALF', 'REAR', 'DIVE', 'SPLAY', 'EMERGE', 'ERUPT', 'LOOM', 'LOOM_WIND', 'LUNGE', 'LUNGE_END', 'LAND', 'SPREAD', 'SWIRL',
  'OVERHEAD', 'PLUNGE', 'CROSS', 'FLOWER', 'COLUMN', 'SLAM', 'LEAP_UP', 'AIR', 'DIVEDOWN', 'ARMSUP', 'LEAN', 'HOODED', 'CRASH', 'SPRAWL', 'PUSHUP', 'TAIL_S', 'TAIL_COCK',
  'TAIL_WHIP', 'TAIL_FOLLOW', 'SWEEP_BACK', 'SWEEP_THRU', 'COMBO_HIGH', 'DOUBLE_SLAM', 'TWIST', 'SPIN_OUT', 'TALLEST', 'SLAM_FAR', 'STAGGER', 'ROAR', 'REACH', 'ARMS_LIFT'];
const UPRIGHT_LOW_P = P(STANCES.UPRIGHT, {pelT: [0, .03, -.91], chest: [3.5, 0, 0]});
export const DBG = [
  dbg('crouch', 'p1', C0, 'CROUCH rest, phase-1 look (the bind pose)'),
  dbg('crawl', 'p3', W0, 'CROUCH rest, phase-3 look (the crawl form)'),
  dbg('upright', 'p3', U0, 'UPRIGHT rest, phase-3 look', 'UPRIGHT'),
  dbg('upright_low', 'p3', UPRIGHT_LOW_P, 'the R1 camera fallback (pose only): waist and thorax lowered', 'UPRIGHT'),
  dbg('rear_p1', 'p1', REAR, 'phase-1 rear (the underside: rib slabs, belly shell, bud face; v2 f2040)'),
  dbg('hoop', 'p3', HOOP, 'the 이동 돌진 hoop / wheel (v5 f930-f951): body arched into a ring'),
  dbg('crouch_over', 'p3', CROUCH_OVER, 'crouch over the player (v5 f1086-f1140): half-upright, the B arms spread overhead like an umbrella', 'UPRIGHT'),
  ...GLOSSARY_P1.map(n => dbg('g_' + n.toLowerCase(), 'p1', POSES[n], `pose glossary (phase 1): ${n}`)),
  ...GLOSSARY_P3.map(n => dbg('g_' + n.toLowerCase(), 'p3', POSES[n], `pose glossary (phase 3, plan §6.2): ${n}`, UPRIGHT_FAMILY.has(n) || CURL_HANDS.has(n) ? 'UPRIGHT' : 'CROUCH',
    CURL_HANDS.has(n) ? [[0, 'p3_curl']] : [])),
];
// ---- the clip list ---------------------------------------------------------------------------------------------------
export const CLIPS = [...CLIPS_REAL, ...DBG];
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
