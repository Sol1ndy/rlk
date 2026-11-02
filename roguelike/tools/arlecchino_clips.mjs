// Clips of the 아를레키노 (Arlecchino) rig: DEFAULT_POSE (the phase-1 fight stance, v1 4.6) and every clip of the contract
// (tools/mboss_arlecchino/api.py CLIPS; lengths / events / loops / forms frozen). Pose channels: tools/arlecchino_pose.mjs.
// Keys: [tick, pose (merged onto the previous key), ease] with the RIGLIB eases (mboss_rig_clips.mjs): 'io' smooth
// (default), 'i' accelerate into the key (strikes), 'o' decelerate, 'l' linear (spins, twirls). Swings are keyed as the
// scythe angle th in its cutting plane, so every cut sweeps on an arc (the compiler then keys each tick where the client's
// slerp would cut the corner); the crescent's point leads the swing (ed), as the avatar's calibrated scythe strikes.
// looks: [[tick, 'channel/value'], ...] run the rig's look functions at that tick (wings open for the wing attacks, the
// tea props of the intro, the form swap of t_p2); cuts: ticks where a part may snap (0-tick key; a scythe appearing).
import {accumulate as acc0, sampleClip as samp0} from './mboss_rig_clips.mjs';

// ---- the phase-1 stance (v1 4.6-5.0, ref/intro_v1_stance.jpg): the crescent low by her right foot, the haft rising across
// her body to above the left shoulder, the right hand at the hip, the left hand open at her side, weight on the back leg ----
export const DEFAULT_POSE = {
  sh: [0, .0156, 0], rt: [0, 0, 0], to: [-2, 6, 0], hd: [2, -6, 0],
  fR: [-.17, 0, -.07], fL: [.15, 0, .09], kR: [.15, 0, -1], kL: [.15, 0, -1], fy: 0,
  wR: 1, gR: [14, -60, .44], gfR: 0, glR: .585, spR: [0, 0, 0], thR: 128, edR: -1, twR: 35, slR: 0, ssR: [1, 1, 1], wdR: 0, wpR: [0, 0, 0],
  wL: 0, gL: [8, -64, .5], gfL: 0, glL: .585, spL: [0, -8, 0], thL: 158, edL: 1, twL: 0, slL: 0, ssL: [1, 1, 1], wdL: 0, wpL: [0, 0, 0],
  aR: [0, 10, 1], aL: [8, 14, 1], hR: [0, 0, 0], hRw: 0, hL: [0, 0, 0], hLw: 0, pR: [.55, -.35, .75], pL: [.55, -.35, .75], onL: 0, onR: 0, onD: -.3,
  lS: 0, lF: 0, lW: 0, lFl: 0, lV: 0, lP: [1, 1, 1], tea: 0, cupT: 0, vis: 1,
};
// phase 2 (v4 22.4-23.0, v6 7.4): the twin scythes held low at both sides, the crescents out by her feet, the hafts rising
// across her front (a low X); the six blade legs folded up behind her shoulders
export const P2_POSE = {...DEFAULT_POSE, gR: [14, -54, .44], thR: 130, twR: 30, wL: 1, gL: [14, -54, .44], spL: [0, 0, 0], thL: 130, edL: -1, twL: 30, lS: .15};

export const accumulate = (c, base = c.base || DEFAULT_POSE) => acc0(c, base);
export const sampleClip = (c, t, ks, base = c.base || DEFAULT_POSE) => samp0(c, t, ks, {defaults: base, phase: (cl, tt) => ((tt + (cl.phase0 || 0)) % 40) / 40});


// ---- helpers ---------------------------------------------------------------------------------------------------------------
const K = (t, p, e) => (e ? [t, p, e] : [t, p]);
const REST = (x = {}) => ({...DEFAULT_POSE, ...x});
const REST2 = (x = {}) => ({...P2_POSE, ...x});
// cutting planes (torso frame; the scythe angle th in them): FR frontal (0 up, 90 out, -90 across her body, 180 down),
// HZ horizontal, a little low in front (0 forward, 90 out, -90 across, 180 back), SG sagittal (0 up, 90 forward, 180 down)
const FR = [0, 0, 0], HZ = [-96, 0, 0], SG = [0, 90, 0];
const WIDE = {fR: [-.24, 0, -.12], fL: [.22, 0, .14]};
const HANG = (y, dz = 0) => ({fR: [-.12, y + .02, .03 + dz], fL: [.12, y - .02, .1 + dz], kR: [.15, 0, -1], kL: [.15, 0, -1]});   // feet off the floor
const LEV = {gfR: 1, glR: .56}, LEVL = {gfL: 1, glL: .56};
const OFF_LEV = {gfR: 0, gfL: 0};

// ===== base clips (P1) =========================================================================================================
const idle = {name: 'idle', src: 'v1 4.6-5.0 (the stance after the intro), v2 16.3: crescent low by the right foot', keys: [
  K(0, {}), K(20, {sh: [0, .0216, 0], to: [-3, 7, 0], hd: [3, -6, 0], thR: 131, aL: [11, 15, 1]}), K(40, {})]};
const walkKeys = (two = false) => [
  K(0, {sh: [0, -.03, 0], fR: [-.15, 0, -.24], fL: [.15, .02, .24], to: [-6, -6, 0], ...(two ? {} : {aL: [26, 12, 1]}), thR: 126}, 'l'),
  K(6, {sh: [0, .016, 0], fR: [-.15, 0, 0], fL: [.15, .15, 0], to: [-6, 0, 0], ...(two ? {} : {aL: [6, 12, 1]}), thR: 129}, 'l'),
  K(12, {sh: [0, -.03, 0], fR: [-.15, .02, .24], fL: [.15, 0, -.24], to: [-6, 6, 0], ...(two ? {} : {aL: [-14, 12, 1]}), thR: 132}, 'l'),
  K(18, {sh: [0, .016, 0], fR: [-.15, .15, 0], fL: [.15, 0, 0], to: [-6, 0, 0], ...(two ? {} : {aL: [6, 12, 1]}), thR: 129}, 'l'),
  K(24, {sh: [0, -.03, 0], fR: [-.15, 0, -.24], fL: [.15, .02, .24], to: [-6, -6, 0], ...(two ? {} : {aL: [26, 12, 1]}), thR: 126}, 'l')];
const walk = {name: 'walk', src: 'v5 13-39 (her prowl toward the player), stride with the scythe trailing low', keys: walkKeys()};
const strafeKeys = (s, two = false) => {
  const out = s > 0 ? 'fL' : 'fR', inn = s > 0 ? 'fR' : 'fL', ox = s > 0 ? 1 : -1;
  const F = (o, i) => ({[out]: o, [inn]: i});
  return [K(0, {...F([.13 * ox, 0, .06], [-.13 * ox, 0, -.04]), to: [-3, 6, -3 * ox]}),
    K(5, {...F([.27 * ox, .13, .06], [-.13 * ox, 0, -.04]), sh: [.03 * ox, .022, 0], to: [-3, 6, -5 * ox]}),
    K(10, {...F([.32 * ox, 0, .06], [-.09 * ox, 0, -.04]), sh: [.05 * ox, .0, 0], to: [-3, 6, -3 * ox]}),
    K(15, {...F([.22 * ox, 0, .06], [.02 * ox, .12, -.04]), sh: [.02 * ox, .022, 0], to: [-3, 6, -1 * ox]}),
    K(20, {...F([.13 * ox, 0, .06], [-.13 * ox, 0, -.04]), sh: [0, .0156, 0], to: [-3, 6, -3 * ox]})];
};
const strafe_l = {name: 'strafe_l', src: 'v2 12.5-27 (side steps between strings)', keys: strafeKeys(1)};
const strafe_r = {name: 'strafe_r', src: 'v2 12.5-27 (side steps between strings)', keys: strafeKeys(-1)};
// ===== base clips (P2) =========================================================================================================
const idle2 = {name: 'idle2', src: 'v4 22.4-23.0, v6 7.4: twin scythes low, the blade legs folded and swaying', keys: [
  K(0, {}), K(20, {sh: [0, .0216, 0], to: [-3, 0, 0], hd: [3, 0, 0], thR: 132, thL: 132, lF: 6}), K(40, {})]};
const walk2 = {name: 'walk2', src: 'v4 23.5-28 (her approach in P2)', keys: walkKeys(true)};
const strafe2_l = {name: 'strafe2_l', src: 'v6 5-14 (circling)', keys: strafeKeys(1, true)};
const strafe2_r = {name: 'strafe2_r', src: 'v6 5-14 (circling)', keys: strafeKeys(-1, true)};
// ===== form-agnostic reactions (base = the form's stance) =========================================================================
const backstep = {name: 'backstep', src: 'v2 37.5 (the hop back before 와리가리)', keys: [
  K(0, {}), K(2, {sh: [0, -.1, 0], to: [-8, 0, 0]}),
  K(4, {sh: [0, .03, 0], ...HANG(.2), to: [-4, 0, 0], thR: 120, thL: 132}, 'o'),
  K(9, {sh: [0, .0, 0], ...HANG(.1, -.06), to: [-6, 0, 0]}),
  K(10, {sh: [0, -.1, 0], fR: [-.17, 0, -.07], fL: [.15, 0, .09], to: [-8, 6, 0]}, 'i'),
  K(12, {sh: [0, -.03, 0], to: [-4, 6, 0], thR: 128, thL: 140})]};
const flinch = {name: 'flinch', src: 'hit reaction (designed)', keys: [
  K(0, {}), K(2, {to: [10, 8, -4], hd: [12, -10, 0], sh: [0, -.02, .04], aL: [22, 30, 1]}, 'o'), K(6, {to: [-2, 6, 0], hd: [2, -6, 0], sh: [0, .0156, 0], aL: [8, 14, 1]})]};
const brk = {name: 'brk', src: 'v3 27.05-28.3 (the counter: she reels, then sinks to the knee)', keys: [
  K(0, {}),
  K(3, {to: [18, 14, 8], hd: [16, -14, 6], sh: [0, -.04, .08], aL: [20, 70, 1], gR: [44, -20, .5], thR: 152, gL: [44, -20, .5], thL: 152, fR: [-.2, 0, .02], fL: [.18, 0, .26], lF: 25}, 'o'),
  K(8, {sh: [0, -.12, .1], to: [10, 10, 4], hd: [8, -6, 0], fL: [.18, 0, .32]}),
  K(14, {sh: [0, -.22, .06], to: [-14, 4, 2], hd: [-18, 0, 0], fR: [-.17, 0, -.02], gR: [20, -50, .5], thR: 165, gL: [20, -50, .5], thL: 165, lF: -10}),
  K(20, {sh: [0, -.28, .05], to: [-20, 0, 0], hd: [-22, 0, 0], gR: [18, -45, .48], thR: 172, gL: [18, -45, .48], thL: 172})]};
// kneeling with the scythe planted beside her (stun, the transition)
const KNEEL = {sh: [0, -.36, .04], to: [-18, 4, 0], hd: [-24, 0, 0], fR: [-.13, .16, .36], kR: [.1, -1, -.3], fL: [.16, 0, -.2], kL: [.1, 0, -1],
  spR: FR, thR: 168, edR: -1, twR: 0, gR: [28, -22, .48], slR: .62, gfR: 0, aL: [40, 10, .9]};
const stun = {name: 'stun', src: 'v3 27.3-29.5 (groggy after the counter: on one knee, the scythe planted)', keys: [
  K(0, {}), K(10, KNEEL, 'o'), K(20, {...KNEEL}), K(70, {sh: [0, -.35, .04], hd: [-20, 4, 0], to: [-16, 6, 0]}), K(120, {...KNEEL}),
  K(132, {sh: [0, -.1, 0], to: [-6, 6, 0], hd: [0, -6, 0], fR: [-.17, .06, -.04], fL: [.15, 0, .09], kR: [.15, 0, -1], aL: [8, 14, 1], slR: .2, thR: 132, gR: [14, -50, .44]}),
  K(140, REST())]};
const KNEEL2 = {...KNEEL, gL: [28, -22, .48], spL: FR, thL: 168, edL: -1, twL: 0, slL: .62, gfL: 0, fL: [.16, 0, -.2], lS: 0, lF: -10};
const stun2 = {name: 'stun2', src: 'v7 24.15-27 (the P2 counter: on one knee, both scythes planted, the legs drooping)', keys: [
  K(0, {}), K(10, KNEEL2, 'o'), K(20, {...KNEEL2}), K(70, {sh: [0, -.35, .04], hd: [-20, 4, 0], to: [-16, 6, 0], lF: -20}), K(120, {...KNEEL2}),
  K(132, {sh: [0, -.1, 0], to: [-6, 0, 0], hd: [0, 0, 0], fR: [-.17, .06, -.04], fL: [.15, 0, .09], kR: [.15, 0, -1], slR: .2, slL: .2, thR: 132, thL: 132, gR: [14, -50, .44], gL: [14, -50, .44], lS: .1, lF: 0}),
  K(140, REST2())]};

// ===== the battle-entry motion (PLAN §3.1, 150 t; footage v5 33-39.5, v1 0.0-5.2; ref/intro_v1_*.jpg) ============================
// E0 tea 0-30: standing tall, weight on the left leg, the saucer in the left hand at the sternum, the right hand lifts the cup
//   to her lips (8-14), sips (14-22), lowers it to the saucer (22-30), the head tilted down (v1 0.0-0.6)
// E1 30-44: both hands drop to the hips, the head lifts to the player; at 34 cup and saucer burst into embers (props none)
// E2 reach 44-52: the right arm swings out sideways to shoulder height, palm down (v1 1.2-1.3)
// E3 summon 52-60: a slight crouch, the torso turns 20 degrees right, she looks at her hand (v1 1.35-1.5)
// E4 form 60-72: the haft grows out of the palm both ways (scale y 0.2 -> 1), the crescent ignites last (x 0.06 -> 1 at 70),
//   while the arm draws the scythe in to her chest (v1 1.5-1.75)
// E5 hold 72-92: the haft horizontal across her chest, the crescent hanging at her left; title at 80 (v1 1.77-2.4)
// E6 twirl 92-104: one-handed 360 degrees in the frontal plane (the lower half swung forward, clear of the floor): the head
//   from her left up over her head, down her right side, low in front, back to her left; the hook trails as in the footage
//   (v1 2.45-2.95: 2.52 rising, 2.58 overhead, 2.65 at her right, 2.80 low in front, 2.95 back); 30 degrees a tick
// E7 hold 2 104-110 (v1 3.0-3.3)   E8 flip 110-116: the head from her left over the top to her right while the crescent rolls
//   through her hand (hook down at both ends; v1 3.35-3.55)   E9 stance 116-150: the head lowers to her right foot, the haft
//   rises across her body to the left shoulder, the right hand to the hip (v1 3.6-5.0); breathing from 130
const TEA = {wR: 0, ssR: [0, 0, 0], tea: 1, sh: [.035, .0156, 0], to: [-2, 4, 2], hd: [-10, -4, 0],
  fR: [-.15, 0, -.13], fL: [.1, 0, .03], kR: [.25, 0, -1], kL: [.1, 0, -1],
  hRw: 1, hR: [-.03, -.33, -.27], hLw: 1, hL: [.02, -.405, -.26], pR: [.7, -.6, .3], pL: [.7, -.6, .3], cupT: 0};
const HOLD = {wR: 1, ssR: [1, 1, 1], hRw: 0, gR: [24, -18, .34], gfR: 0, spR: FR, thR: -90, edR: -1, twR: 0, slR: -.05, to: [0, 4, 0], hd: [0, -2, 0],
  fR: [-.2, 0, -.06], fL: [.17, 0, .1], kR: [.15, 0, -1], kL: [.15, 0, -1], sh: [0, .0156, 0], aL: [8, 16, 1]};
const intro = {name: 'intro', src: 'v5 33-39.5, v1 0.0-5.2 (ref/intro_v1_tea, _summon, _fine, _twirl, _stance)', cuts: [34, 60],
  looks: [[0, 'props/tea'], [34, 'props/none']], edgeOk: [[92, 105], [110, 117]], keys: [
    K(0, TEA),
    K(8, {hd: [-8, -3, 0]}),
    K(14, {hR: [-.04, -.05, -.31], cupT: 34, hd: [8, -2, 0], pR: [.6, -.8, .1]}),          // sip
    K(18, {hR: [-.04, -.04, -.31], cupT: 38, hd: [9, -2, 0]}),
    K(22, {hR: [-.03, -.33, -.27], cupT: 0, hd: [-8, -4, 0], pR: [.7, -.6, .3]}),          // lower
    K(30, {hd: [-3, -2, 0]}),
    K(34, {hRw: .35, hLw: .35, hR: [-.06, -.45, -.22], hL: [.06, -.48, -.2], hd: [0, 0, 0], tea: 0}),   // embers
    K(40, {hRw: 0, hLw: 0, aR: [6, 12, 1], aL: [6, 12, 1], hd: [2, 0, 0], sh: [.02, .0156, 0], pR: [.55, -.35, .75], pL: [.55, -.35, .75]}),
    K(44, {aR: [8, 16, 1]}),
    K(50, {aR: [16, 88, 1], to: [0, 8, 0], hd: [0, 8, 0], sh: [0, .0156, 0]}, 'o'),      // reach
    K(52, {aR: [18, 90, 1]}),
    K(59, {sh: [0, -.04, 0], to: [-4, 20, 0], hd: [-6, 30, 0], fR: [-.2, 0, -.06], fL: [.17, 0, .1], aR: [22, 92, 1]}),  // summon
    // E4: the scythe appears in the outstretched hand, horizontal across her front (the haft through the palm both ways)
    K(60, {wR: 1, ssR: [.06, .25, 1], gR: [62, 4, .58], gfR: 0, spR: FR, thR: -90, edR: -1, twR: 0, slR: 0}),
    K(66, {ssR: [.06, 1, 1], gR: [48, -2, .5], to: [-2, 14, 0], hd: [-2, 18, 0]}),
    K(70, {ssR: [1, 1, 1], gR: [32, -12, .38]}),
    K(72, HOLD, 'o'),                                                                      // hold
    K(80, {hd: [2, 0, 0], sh: [0, .02, 0]}),
    K(88, {hd: [0, -2, 0], sh: [0, .0156, 0], spR: FR}),
    K(92, {spR: [32, 0, 0], thR: -90, gR: [24, -14, .36]}),
    K(98, {thR: 90, gR: [14, 6, .42], to: [0, -4, -3], hd: [0, 4, 0], spR: [40, 0, 0]}, 'l'),   // twirl: overhead at 95, her right 98
    K(101, {thR: 180, gR: [18, 10, .44], spR: [46, 0, 0], sh: [0, .03, 0]}, 'l'),                // low in front, the haft out forward
    K(104, {thR: 270, gR: [24, -14, .35], to: [0, 6, 2], hd: [0, -2, 0], spR: [32, 0, 0], sh: [0, .0156, 0]}, 'l'),   // back to her left
    K(108, {spR: FR, thR: 270}),
    K(110, {thR: 270, edR: -1}),
    K(116, {thR: 450, edR: 1, gR: [30, -10, .38]}, 'l'),                                  // flip: over the top, rolled in the hand
    K(126, {thR: 488, edR: 1, twR: -145, gR: [14, -60, .44], slR: 0, to: [-2, 6, 0], hd: [2, -6, 0], fR: [-.17, 0, -.07], fL: [.15, 0, .09], aL: [8, 14, 1]}),
    K(130, {}),
    K(140, {sh: [0, .0216, 0], to: [-3, 7, 0], hd: [3, -6, 0], thR: 491}),
    K(150, {sh: [0, .0156, 0], to: [-2, 6, 0], hd: [2, -6, 0], thR: 488, aL: [8, 14, 1]})]};

// ===== phase 1 patterns (PLAN §5.2) ==============================================================================================
// A 사형장으로의 초대 (v2 13-16.6 two hits, 19-26.8 five): h1 a wide sweep right -> left at waist height, h2 the backhand
// left -> right; the arm straight along the haft (lever grip), the torso winding and unwinding; h3 / h5 a full spin with the
// scythe out at her side (the spin ring), h4 an overhead two-handed slam into the floor in front
const WIND_R = {spR: HZ, thR: 132, edR: -1, twR: -18, ...LEV, to: [-4, 34, 0], rt: [0, 6, 0], hd: [0, -30, 0], ...WIDE, aL: [50, 35, 1], sh: [0, -.06, 0], slR: 0};
const aOpen = [
  K(0, {}),
  K(4, WIND_R),
  K(10, {thR: 142, to: [-4, 44, 0], hd: [0, -36, 0]}),
  K(14, {thR: -5, to: [-6, -20, 0], rt: [0, -8, 0], hd: [0, 14, 0], aL: [30, 55, 1]}, 'i'),    // h1
  K(17, {thR: -82, to: [-4, -36, 0], hd: [0, 26, 0], edR: -1}, 'o'),
  K(21, {thR: -100, edR: 1, twR: 18}),
  K(24, {thR: 5, to: [-6, 14, 0], rt: [0, 6, 0], hd: [0, -10, 0], aL: [40, 20, 1]}, 'i'),        // h2
  K(27, {thR: 95, to: [-4, 32, 0], hd: [0, -24, 0]}, 'o')];
const a2 = {name: 'a2', src: 'v2 13.0-16.6 (ref/p1_A_normal_2hit.jpg)', keys: [...aOpen,
  K(34, {thR: 112, to: [-2, 16, 0], sh: [0, -.02, 0]}), K(46, REST())]};
const SPIN_PREP = {spR: [-92, 0, 0], thR: 90, edR: 1, twR: 15, ...LEV, sh: [0, -.1, 0], to: [-6, 10, 0], hd: [0, -6, 0], aL: [12, 80, 1]};
const SLAM_UP = {spR: SG, thR: -38, edR: 1, twR: 0, gfR: 0, gR: [-6, 62, .42], onL: 1, onD: -.32, to: [14, 0, 0], hd: [8, 0, 0], sh: [0, .02, 0]};
const aMid = (r0) => [
  K(32, {...SPIN_PREP, rt: [0, r0, 0]}),
  K(38, {sh: [0, -.12, 0]}),
  K(50, {rt: [0, r0 + 360, 0], sh: [0, -.1, 0]}, 'l'),                                          // h3 spin ring (44 = half way)
  K(53, {to: [-2, 4, 0], aL: [40, 40, 1]}),
  K(58, {...SLAM_UP, rt: [0, r0 + 360, 0]}),
  K(60, {thR: -46, to: [16, 0, 0]}),
  K(64, {thR: 124, to: [-26, 0, 0], sh: [0, -.18, -.04], hd: [-14, 0, 0]}, 'l'),                // h4 overhead slam
  K(67, {thR: 128, sh: [0, -.2, -.04]}, 'o'),
  K(74, {thR: 128})];
const a4 = {name: 'a4', src: 'v2 19-24.5 (ref/p1_A_normal_5hit.jpg: sweep, backhand, spin ring 21.05, slam burst 22.25)', edgeOk: [[58, 62]], keys: [...aOpen, ...aMid(0),
  K(86, {onL: 0, sh: [0, -.04, 0], to: [-6, 4, 0], hd: [0, -4, 0], spR: FR, thR: 140, gR: [14, -50, .44]}), K(100, REST({rt: [0, 360, 0]}))]};
const a5 = {name: 'a5', src: 'v2 19-26.8 (ref/p1_A_normal_5hit.jpg: + the second spin ring 23.3-23.9)', edgeOk: [[58, 62]], keys: [...aOpen, ...aMid(0).slice(0, -1),
  K(72, {thR: 128, onL: 0, aL: [55, 25, .9], sh: [0, -.14, -.02]}),
  K(77, {...SPIN_PREP, onL: 0, rt: [0, 360, 0]}),
  K(78, {sh: [0, -.12, 0]}),
  K(90, {rt: [0, 720, 0], sh: [0, -.1, 0]}, 'l'),                                               // h5 spin ring (84 = half way)
  K(94, {to: [-2, 4, 0], aL: [30, 30, 1]}),
  K(108, {sh: [0, -.03, 0], to: [-6, 4, 0], hd: [0, -4, 0], spR: FR, thR: 140, edR: -1, twR: 35, gfR: 0, gR: [14, -50, .44]}),
  K(124, REST({rt: [0, 720, 0]}))]};

// B 붉은 달의 낫 (v1 15.4-18.1, 19.5-24.6): the scythe raised, spun into a vertical flaming wheel in front of her (two turns,
// the point leading forward over the top), flung at the player (release: the rig scythe vanishes, the kit's wheel flies), the
// arm held out until the catch; b2 throws twice, then reaches with the open right hand and closes it (the crimson grab)
const WHEEL0 = {spR: SG, thR: 20, edR: 1, twR: 0, gfR: 0, gR: [8, 46, .5], to: [6, 10, 0], hd: [2, -6, 0], aL: [30, 40, 1], ...WIDE, sh: [0, -.03, 0]};
const bThrow = (t0, tr, first = true) => [
  ...(first ? [K(t0 - 4, WHEEL0)] : []),
  K(t0, {thR: 60, gR: [8, 46, .5]}),
  K(tr - 1, {thR: 60 + 720 - 40, gR: [3, 30, .585], to: [-9, -5, 0], hd: [0, 2, 0], ssR: [1, 1, 1]}, 'l'),
  K(tr, {thR: 60 + 720, gR: [2, 26, .585], to: [-10, -6, 0], ssR: [0, 0, 0]}, 'l')];        // release: the kit's wheel flies
const b1 = {name: 'b1', src: 'v1 15.4-18.1 (ref/p1_B_throw.jpg: the wheel spin 16.0-16.9, release 17.0, the catch)', cuts: [28, 52], keys: [
  K(0, {}), ...bThrow(10, 28),
  K(36, {gR: [12, 0, .5], to: [-4, 0, 0]}),
  K(50, {gR: [4, 12, .56], to: [-6, 0, 0]}),
  K(51, {ssR: [0, 0, 0], thR: 780}),
  K(52, {ssR: [1, 1, 1], thR: 800}),
  K(56, {thR: 830, to: [0, 6, 0], gR: [10, 10, .5]}, 'o'),
  K(60, REST({thR: 848, edR: 1, twR: -145}))]};
const b2 = {name: 'b2', src: 'v1 19.5-24.6 (ref/p1_B_throw2_grab.jpg: two wheels, then the crimson grab 23.9-24.4)', cuts: [28, 34, 58, 100], keys: [
  K(0, {}), ...bThrow(10, 28),
  K(30, {gR: [20, -10, .45], to: [0, 4, 0], thR: 790}),
  K(33, {ssR: [0, 0, 0], thR: 40, gR: [8, 46, .5]}),
  K(34, {ssR: [.1, .3, 1], thR: 40}),
  K(38, {ssR: [1, 1, 1]}),
  ...bThrow(40, 58, false),
  K(64, {to: [0, 6, 0], gR: [20, -20, .45]}),
  K(72, {gR: [40, 0, .3], to: [2, 14, 0], sh: [0, -.02, 0]}),
  K(76, {gR: [0, 8, .59], to: [-8, -10, 0], hd: [0, 0, 0], sh: [0, -.05, -.04], aL: [20, 30, 1]}, 'i'),   // reach: the open hand
  K(80, {gR: [0, 7, .59]}),
  K(92, {gR: [2, 6, .55]}),
  K(96, {gR: [10, 4, .42], to: [-2, 10, 0]}, 'i'),                                              // grab: the hand closes, pulled back
  K(99, {ssR: [0, 0, 0], thR: 60}),
  K(100, {ssR: [1, 1, 1], thR: 60, spR: SG, edR: 1, gR: [10, 30, .45]}),                        // the scythe comes back to the hand
  K(106, {thR: 100, gR: [12, 10, .45]}, 'o'),
  K(130, REST())]};

// C 불꽃 도약 (v1 26.5-29.0, 32.0-35.0): a deep crouch, the jump (+9 b by the module), at the apex the scythe whirls round her
// in flame while she hangs tucked, then the two-handed dive slash down to the locked spot; c2 adds the crimson wings bursting
// open (v1 35.4-39.9) and the wing strike sweeping round her front
const cOpen = [
  K(0, {}),
  K(6, {sh: [0, -.26, .04], to: [-18, 6, 0], hd: [12, 0, 0], fR: [-.2, 0, -.1], fL: [.2, 0, .12], kR: [.2, 0, -1], kL: [.2, 0, -1],
    spR: FR, thR: 152, gR: [30, -50, .5], aL: [50, 40, 1]}),
  K(8, {sh: [0, .05, 0], to: [4, 0, 0], fR: [-.15, .02, .05], fL: [.15, .02, .1]}, 'o'),           // jump
  K(12, {sh: [0, .1, 0], fR: [-.14, .38, -.08], fL: [.14, .42, .02], to: [-10, 0, 0], thR: 20, gR: [10, 40, .5], spR: FR, edR: 1, twR: 0}),
  K(18, {spR: [-60, 0, 0], thR: 20}),                                                            // apex: the flaming whirl
  K(44, {thR: 20 + 720, rt: [0, 0, 0]}, 'l'),
  K(46, {spR: SG, thR: -40, gR: [0, 55, .4], onL: 1, onD: -.3, to: [10, 0, 0], rt: [-10, 0, 0]}),  // lock: raised overhead
  K(48, {thR: -30, rt: [-40, 0, 0], fR: [-.14, .3, .25], fL: [.14, .34, .3]}),                     // dive
  K(50, {thR: 30, rt: [-28, 0, 0]}, 'l'),
  K(54, {thR: 124, rt: [0, 0, 0], sh: [0, -.22, -.04], to: [-24, 0, 0], hd: [-10, 0, 0], fR: [-.22, 0, -.12], fL: [.2, 0, .16]}, 'l'),  // impact
  K(60, {thR: 126, sh: [0, -.2, -.04]})];
const c1 = {name: 'c1', src: 'v1 26.5-29.0, 32.0-35.0 (ref/p1_C_leap.jpg)', edgeOk: [[44, 48]], keys: [...cOpen,
  K(68, {onL: 0, sh: [0, -.06, 0], to: [-6, 4, 0], hd: [0, -4, 0], spR: FR, thR: 132, edR: -1, twR: 35, gR: [14, -50, .44]}), K(80, REST())]};
const c2 = {name: 'c2', src: 'v1 26.5-39.9 (ref/p1_C_leap.jpg, ref/p1_C_wing.jpg: the wings burst 36.6, the wing strike 36.8-37.2)', edgeOk: [[44, 48]],
  looks: [[80, 'wings/open'], [138, 'wings/off']], keys: [...cOpen,
    K(72, {onL: 0, sh: [0, .0, 0], to: [0, 0, 0], hd: [0, 0, 0], spR: FR, thR: 132, edR: -1, twR: 35, gR: [14, -50, .44]}),
    K(80, {sh: [0, -.06, 0], to: [-6, 0, 0], aL: [30, 50, 1], lV: 0, lS: .2, thR: 120, gR: [40, -20, .48]}),
    K(84, {lV: 1, lS: 1, lF: 12, thR: 128, gR: [60, -6, .5], twR: 0}, 'o'),                       // wing_open
    K(86, {lF: 26, to: [8, 20, 0], spR: HZ, thR: 130, edR: -1, twR: -18, ...LEV, ...WIDE}),
    K(90, {lW: .85, lF: 0, to: [-12, -20, 0], thR: -20}, 'l'),                                     // wing strike
    K(94, {lW: .2, lF: 12, thR: -70}, 'o'),
    K(100, {lW: 0, lF: 10, lFl: 6, to: [-2, 0, 0], spR: FR, thR: 140, edR: -1, twR: 35, gfR: 0, gR: [14, -50, .44]}),
    K(130, {lF: 8}),
    K(134, {lV: .4, lS: .3, lFl: 0}),
    K(138, {lV: 0, lS: 0, lF: 0}),
    K(140, REST())]};

// D 블러드 돌진 (v2 0-11.5): the red flare tell, crouched low, the scythe drawn back low behind her right, the left arm
// forward; the dash (the module moves her) ends in a rising horizontal slash; d2 adds the rising follow-up slash (v2 9.9-10.2)
const dOpen = [
  K(0, {}),
  K(8, {sh: [0, -.2, .04], to: [-22, 20, 0], hd: [14, -16, 0], fL: [.22, 0, -.14], fR: [-.24, 0, .16], kL: [.2, 0, -1], kR: [.2, 0, -1],
    spR: [-84, 0, 0], thR: 160, edR: -1, twR: -10, ...LEV, aL: [60, 10, 1]}),
  K(22, {sh: [0, -.24, .05], thR: 168}),
  K(26, {rt: [-22, 0, 0], sh: [0, -.18, -.04], fR: [-.18, .1, .3], fL: [.18, .05, -.08], thR: 166}),   // go
  K(30, {thR: -24, to: [-14, -24, 0], rt: [-10, 0, 0], hd: [0, 18, 0]}, 'l'),                    // hit
  K(33, {thR: -80, to: [-8, -34, 0], rt: [0, 0, 0], fR: [-.22, 0, -.08], fL: [.22, 0, .14]}, 'o'),
  K(40, {thR: -86})];
const d1 = {name: 'd1', src: 'v2 0-11.5 (ref/p1_D_dash.jpg: the flare 7.8, the dash 8.6-9.0)', keys: [...dOpen, K(56, REST())]};
const d2 = {name: 'd2', src: 'v2 0-11.5 (ref/p1_D_dash.jpg, ref/p1_D_follow.jpg: the follow-up 9.9-10.2)', keys: [...dOpen.slice(0, -1),
  K(36, {spR: FR, thR: -150, edR: 1, twR: 0, gfR: .5, to: [-10, -30, 0], sh: [0, -.16, 0]}),
  K(42, {thR: -158, sh: [0, -.2, 0]}),
  K(46, {thR: 20, to: [10, 20, 0], sh: [0, .04, 0], hd: [10, 0, 0]}, 'i'),                       // fhit: the rising slash
  K(50, {thR: 60, to: [12, 26, 0]}, 'o'),
  K(62, {thR: 120, to: [0, 10, 0], sh: [0, 0, 0], hd: [0, -4, 0], gfR: 0, gR: [14, -50, .44]}),
  K(76, REST({edR: 1, twR: -145}))]};

// E 와리가리 베기 (v2 37.5-40, v3 0-7.25): the hop back, hovering 2.5 b up (the module), five lateral dashes leaning into each,
// the dive at the player, a sweep, then a vertical wheel slash in front of her
const AIR = {sh: [0, .05, 0], ...HANG(.24), to: [6, 0, 0], spR: [-80, 0, 0], thR: 150, edR: -1, twR: 0, ...LEV, aL: [40, 60, 1]};
const zig = (t, s) => [K(t, {rt: [0, 0, -22 * s], thR: 165, to: [4, 10 * s, 0]}, 'i'), K(t + 4, {rt: [0, 0, 0], thR: 150, to: [6, 0, 0]}, 'o')];
const e1 = {name: 'e1', src: 'v2 37.5-40, v3 0-7.25 (ref/p1_E_zigzag_a.jpg, _b.jpg, _far.jpg)', edgeOk: [[84, 99]], keys: [
  K(0, {}), K(4, {sh: [0, -.12, 0], to: [-6, 0, 0]}), K(10, AIR, 'o'),
  ...zig(16, 1), ...zig(26, -1), ...zig(36, 1), ...zig(46, -1), ...zig(56, 1),
  K(64, {thR: 140, to: [8, 30, 0]}),                                                              // lock
  K(70, {rt: [-30, 0, 0], ...HANG(.3, .3), thR: 150}),                                             // go: the dive
  K(72, {rt: [-6, 0, 0], sh: [0, -.12, 0], ...WIDE, kR: [.2, 0, -1], kL: [.2, 0, -1], thR: 146}),
  K(76, {thR: -24, to: [-8, -30, 0], rt: [0, 0, 0]}, 'l'),                                       // sweep
  K(80, {thR: -90}, 'o'),
  K(84, {spR: [20, 90, 0], thR: -60, edR: 1, gfR: 0, gR: [8, 55, .45], to: [6, 0, 0], sh: [0, .02, 0]}),
  K(86, {thR: -50}),
  K(98, {thR: 430, sh: [0, -.02, 0], to: [-8, 0, 0], gR: [8, 40, .45]}, 'l'),                    // spin: the vertical wheel (92)
  K(112, REST({thR: 488, edR: 1, twR: -145}))]};

// F 붉은 피의 연회 (v3 7.5-29.5): the scythe raised upright, the left hand reaching for the player while the sigil closes (6-22),
// the brand (22: the hand clenches and pulls), she glides to the centre with her arms out (40), raises both arms (100) while
// the floor floods (110), throws them down for the threads and thorns (160), rises 1 b on opened wings (166), gathers and
// flings her arms wide for the blast (196), settles and folds the wings (232)
const f1 = {name: 'f1', src: 'v3 7.5-29.5 (ref/p1_F_banquet.jpg, _sigil.jpg, _field.jpg, _counter.jpg)', looks: [[163, 'wings/open'], [228, 'wings/off']], keys: [
  K(0, {}),
  K(6, {spR: FR, thR: 2, edR: -1, twR: 30, gR: [20, 10, .5], to: [4, 0, 0], hd: [6, 0, 0], aL: [80, 20, 1]}),
  K(18, {thR: -4, aL: [92, 10, 1], hd: [2, 0, 0]}),
  K(22, {aL: [70, 12, .7], to: [-4, -8, 0]}, 'i'),                                                     // brand
  K(28, {aL: [60, 20, .8], to: [0, -4, 0]}),
  K(40, {aL: [4, 84, 1], gR: [80, 0, .56], thR: 10, to: [0, 0, 0], hd: [4, 0, 0], fR: [-.16, 0, -.02], fL: [.16, 0, .04]}),   // centre
  K(70, {aL: [6, 82, 1], hd: [6, 0, 0]}),
  K(100, {aL: [10, 140, 1], gR: [60, 50, .55], thR: 0}),                                                // arms
  K(110, {hd: [16, 0, 0], to: [8, 0, 0]}),                                                              // flood
  K(150, {hd: [18, 0, 0]}),
  K(156, {aL: [60, 20, .5], gR: [30, 0, .35], thR: 20, sh: [0, -.05, 0], hd: [4, 0, 0], to: [0, 0, 0]}),
  K(160, {aL: [20, 60, 1], gR: [70, -40, .58], thR: 150, sh: [0, -.1, 0], to: [-10, 0, 0], hd: [-6, 0, 0], lV: 0}, 'i'),   // hit1
  K(164, {lV: 0, lS: .3}),
  K(170, {sh: [0, .45, 0], ...HANG(.4), lV: 1, lS: 1, lF: 15, aL: [6, 86, 1], gR: [80, 10, .55], thR: 120, to: [0, 0, 0], hd: [4, 0, 0]}, 'o'),   // wings
  K(176, {sh: [0, .7, 0], ...HANG(.66)}),
  K(190, {aL: [80, -20, .6], gR: [-10, 0, .4], thR: -60, edR: 1, twR: 0, lF: 25, lS: .9, to: [-6, 0, 0]}),
  K(196, {aL: [10, 100, 1], gR: [90, 10, .58], thR: 70, lF: -6, lS: 1, to: [10, 0, 0], hd: [10, 0, 0]}, 'i'),   // hit2: the blast
  K(206, {sh: [0, .3, 0], ...HANG(.26), lF: 8, to: [0, 0, 0], hd: [0, 0, 0]}),
  K(214, {sh: [0, .0156, 0], fR: [-.17, 0, -.07], fL: [.15, 0, .09], aL: [20, 30, 1], gR: [14, -50, .44], thR: 140, edR: -1, twR: 35}, 'o'),
  K(222, {lV: .3, lS: .2}),
  K(226, {lV: 0, lS: 0}),
  K(232, REST())]};

// G 죽음의 칼날 (v3 29.5-40, v4 0-3.4): she drives the scythe into the floor before her (two hands on the haft), pushes on it
// as each blade cross erupts (34, 62), turns with the relock (40), wrenches it out and lifts it overhead (70), slams it down
// for the field (104)
const PLANT = {spR: SG, thR: 158, edR: -1, twR: 0, gR: [8, -16, .5], slR: .3, gfR: 0, onL: .9, onD: -.2, sh: [0, -.08, 0], to: [-12, 6, 0], hd: [4, -6, 0], ...WIDE};
const g1 = {name: 'g1', src: 'v3 29.5-40, v4 0-3.4 (ref/p1_G_blades.jpg, _cross.jpg, _rim.jpg, _field.jpg)', edgeOk: [[98, 106]], keys: [
  K(0, {}),
  K(4, {spR: SG, thR: 40, edR: -1, twR: 0, gR: [6, 20, .5], to: [6, 0, 0], ...WIDE}),
  K(7, PLANT, 'i'),                                                                                     // plant / blades (6)
  K(10, {sh: [0, -.04, 0], to: [-8, 6, 0]}),
  K(34, {to: [-16, 6, 0], sh: [0, -.1, 0]}, 'i'),                                                       // cross1
  K(37, {to: [-8, 6, 0], sh: [0, -.05, 0]}),
  K(40, {to: [-8, -14, 0], hd: [0, 14, 0]}),                                                            // relock
  K(58, {to: [-8, -10, 0]}),
  K(62, {to: [-16, -10, 0], sh: [0, -.1, 0]}, 'i'),                                                     // cross2
  K(66, {to: [-8, 0, 0], sh: [0, -.05, 0], hd: [0, 0, 0]}),
  K(70, {thR: 120, slR: .1, gR: [8, 0, .5], onL: .5}),                                                  // rim: wrenched out
  K(78, {spR: FR, thR: 0, edR: -1, twR: 0, gR: [20, 40, .5], onL: 0, slR: 0, aL: [8, 165, 1], to: [8, 0, 0], hd: [10, 0, 0], sh: [0, .0156, 0]}),
  K(98, {thR: -6, hd: [12, 0, 0]}),
  K(104, {spR: SG, thR: 150, gR: [8, -16, .52], slR: .25, sh: [0, -.16, 0], to: [-18, 0, 0], aL: [40, 50, 1], hd: [-6, 0, 0], onL: .6}, 'l'),   // field
  K(110, {thR: 156}),
  K(124, {onL: 0, slR: 0, spR: FR, thR: 140, edR: -1, twR: 35, gR: [14, -50, .44], sh: [0, -.02, 0], to: [-4, 6, 0], hd: [0, -6, 0]}),
  K(140, REST())]};

// H 연옥 그림자 분신 (v4 0-13): up the thread to the web (the module moves her), perched in a crouch looking down, the left
// hand flung at the player as the clones dive (20), the backward drop to the player (96), the wing strike (104) and a sweep (112)
const PERCH = {sh: [0, -.3, 0], fR: [-.14, 0, -.04], fL: [.14, 0, .06], kR: [.3, 0, -1], kL: [.3, 0, -1], to: [-24, 0, 0], hd: [-20, 0, 0],
  spR: [-80, 0, 0], thR: -60, edR: -1, twR: 20, gfR: 0, gR: [0, -30, .4], aL: [40, 20, .7]};
const h1 = {name: 'h1', src: 'v4 0-13 (ref/p1_H_clones.jpg, _launch.jpg, _leapback.jpg); timing R-S3-1 (drop 64, wing 72, sweep 84, end 124)',
  looks: [[68, 'wings/open'], [118, 'wings/off']], keys: [
  K(0, {}),
  K(3, {sh: [0, -.2, 0], to: [-14, 0, 0]}),
  K(6, {sh: [0, .1, 0], ...HANG(.06), to: [6, 0, 0]}, 'o'),                                              // leap
  K(10, PERCH),                                                                                          // perch
  K(20, {aL: [72, 30, 1], to: [-20, -10, 0]}, 'i'),                                                       // clones
  K(26, {aL: [40, 20, .7], to: [-24, 0, 0]}),
  K(34, {to: [-26, 4, 0]}),                                                                              // strike
  K(48, {to: [-22, -4, 0], hd: [-18, 4, 0]}),
  K(60, {sh: [0, -.34, 0], to: [-24, 0, 0], hd: [-20, 0, 0]}),
  K(64, {rt: [24, 0, 0], sh: [0, .2, 0], fR: [-.14, .25, -.3], fL: [.14, .3, -.24], aL: [10, 160, 1], spR: FR, thR: 0, edR: 1, twR: 0, gR: [30, 40, .5], to: [0, 0, 0], hd: [0, 0, 0]}, 'o'),   // drop
  K(68, {rt: [0, 0, 0], sh: [0, -.16, 0], ...WIDE, kR: [.2, 0, -1], kL: [.2, 0, -1], lV: 0, lS: .4, aL: [40, 50, 1], thR: 100, gR: [40, 0, .5]}, 'i'),
  K(72, {lV: 1, lS: 1, lW: .8, lF: 6, to: [-10, -20, 0]}, 'i'),                                            // wing
  K(77, {lW: .2, lF: 12, spR: HZ, thR: 130, edR: -1, twR: -18, ...LEV, to: [0, 30, 0], sh: [0, -.08, 0]}),
  K(84, {thR: -40, to: [-8, -24, 0]}, 'i'),                                                                // sweep
  K(88, {thR: -80}, 'o'),
  K(96, {lW: 0, lF: 10, lFl: 6, spR: FR, thR: 140, edR: -1, twR: 35, gfR: 0, gR: [14, -50, .44], to: [-2, 0, 0], sh: [0, -.02, 0]}),
  K(108, {lF: 8}),
  K(114, {lV: .3, lS: .2, lFl: 0}),
  K(118, {lV: 0, lS: 0, lF: 0}),
  K(124, REST())]};

// E70 재가 된 만상 (v2 28-37.7): she straightens and rises 1 b, the arms opening; the pool spreads under her (40-70); the
// left hand thrust at the player for the brand (70), the wings burst open (74), she lands (96) and folds them
const e70 = {name: 'e70', src: 'v2 28-37.7 (ref/p1_E70_event.jpg)', looks: [[72, 'wings/open'], [108, 'wings/off']], keys: [
  K(0, {}),
  K(6, {to: [6, 0, 0], hd: [10, 0, 0], aL: [30, 50, 1]}),
  K(20, {sh: [0, .7, 0], ...HANG(.66), aL: [8, 80, 1], gR: [70, -10, .55], thR: 128, to: [2, 0, 0]}, 'o'),   // rise
  K(40, {hd: [-12, 0, 0]}),                                                                                 // pool
  K(64, {aL: [60, -10, .5], to: [4, 6, 0]}),
  K(70, {aL: [86, 5, 1], to: [-4, -8, 0], hd: [0, 0, 0], lV: 0}, 'i'),                                     // brand
  K(74, {lV: 1, lS: 1, lF: 20, to: [-2, 0, 0]}, 'o'),                                                       // wings
  K(90, {lF: 14, aL: [20, 60, 1]}),
  K(96, {sh: [0, .0156, 0], fR: [-.17, 0, -.07], fL: [.15, 0, .09], kR: [.15, 0, -1], kL: [.15, 0, -1], lF: 0, aL: [20, 30, 1], gR: [30, -40, .48], thR: 128}, 'i'),   // land
  K(104, {lV: .3, lS: .3}),
  K(108, {lV: 0, lS: 0}),
  K(110, REST())]};

// ===== the transition T (PLAN §3.2, 180 t; designed: the footage cuts the cutscene; v4 13.5-21.4 the P2 opener) ===================
// 0-24 she staggers and sinks to one knee, the scythe planted; 24-50 head bowed (the crimson pillar builds); 50-70 blackout
// (the scythe gone); 70-110 she stands and rises 3 b inside the pillar, the form swaps p1 -> p2 at 90 (hidden by the pillar's
// peak); 110 / 116 / 122 the blade legs unfold a pair at a time; 130-140 the twin scythes form in the outstretched hands;
// 140 title; 150-180 she launches up and out of sight (vis 0 at 176: S4's q0 places the body at the hover spot and plays
// q0_hover, whose tick 0 shows her again)
const t_p2 = {name: 't_p2', src: 'designed (PLAN §3.2); v4 13.5-21.4 (ref/p2_T_transition.jpg), wiki: six legs, twin scythes', formAt: {90: 'p2'},
  cuts: [70, 90, 110, 116, 122, 130], keys: [
    K(0, {}),
    K(6, {to: [16, 12, 6], hd: [14, -10, 0], sh: [0, -.06, .08], fL: [.18, 0, .3], aL: [50, 60, 1], gR: [44, -20, .5], thR: 152}, 'o'),
    K(20, {...KNEEL, lP: [0, 0, 0]}),                                                                    // kneel, the scythe planted
    K(24, {hd: [-30, 0, 0]}),                                                                            // pillar
    K(50, {hd: [-32, 2, 0], to: [-20, 4, 0]}),                                                           // dark
    K(69, {ssR: [1, 1, 1]}),
    K(70, {ssR: [0, 0, 0], wR: 0, aR: [20, 20, .9]}),                                                    // rise: the scythe gone
    K(80, {sh: [0, .0156, 0], fR: [-.15, 0, -.04], fL: [.15, 0, .06], kR: [.15, 0, -1], kL: [.15, 0, -1], to: [-6, 0, 0], hd: [-20, 0, 0], aR: [10, 18, 1], aL: [10, 18, 1], slR: 0}),
    K(89, {sh: [0, 1.0, 0], ...HANG(1.0), to: [2, 0, 0], hd: [6, 0, 0], aR: [20, 30, 1], aL: [20, 30, 1]}),
    K(90, {lP: [0, 0, 0], lS: .6, lF: 20}),                                                               // swap (form p2)
    K(108, {sh: [0, 2.14, 0], ...HANG(2.12), hd: [20, 0, 0], to: [6, 0, 0]}, 'o'),
    K(110, {lP: [0, 0, 0]}),
    K(113, {lP: [1, 0, 0]}, 'o'),                                                                        // legs1
    K(116, {lP: [1, 0, 0], lS: .7}),
    K(119, {lP: [1, 1, 0]}, 'o'),                                                                        // legs2
    K(122, {lP: [1, 1, 0], lS: .85}),
    K(125, {lP: [1, 1, 1]}, 'o'),                                                                        // legs3
    K(129, {lS: 1, lF: 24, wR: 0, wL: 0, aR: [8, 85, 1], aL: [8, 85, 1]}),
    K(130, {wR: 1, wL: 1, ssR: [.06, .25, 1], ssL: [.06, .25, 1], gR: [78, 0, .58], gL: [78, 0, .58], gfR: 0, gfL: 0, spR: FR, spL: FR,
      thR: 180, thL: 180, edR: -1, edL: -1, twR: 0, twL: 0, slR: 0, slL: 0}),                            // scythes
    K(134, {ssR: [.06, 1, 1], ssL: [.06, 1, 1]}),
    K(138, {ssR: [1, 1, 1], ssL: [1, 1, 1], gR: [70, -6, .56], gL: [70, -6, .56]}),
    K(146, {hd: [6, 0, 0], lF: 30, thR: 172, thL: 172}),                                                // title 140
    K(150, {sh: [0, 1.9, 0], ...HANG(1.95, -.05), to: [-16, 0, 0], hd: [-10, 0, 0], gR: [40, -30, .5], gL: [40, -30, .5], thR: 150, thL: 150, lF: 10}),   // launch
    K(160, {sh: [0, 3.3, 0], ...HANG(3.15, .1), to: [6, 0, 0], hd: [12, 0, 0], lF: -20, lS: .5, gR: [20, -60, .5], gL: [20, -60, .5], thR: 175, thL: 175}, 'o'),
    K(170, {sh: [0, 4.0, 0], ...HANG(3.85, .1)}),
    K(176, {vis: 0}, 'i'),
    K(180, {vis: 0})]};

// ===== phase 2 patterns (PLAN §6; form p2: twin scythes, six blade legs) ==========================================================
const HOVER = {sh: [0, .1, 0], ...HANG(.12), to: [4, 0, 0], hd: [-10, 0, 0], lS: 1, lF: 12,
  spR: FR, spL: FR, gR: [76, -18, .55], gL: [76, -18, .55], thR: 138, thL: 138, edR: -1, edL: -1, twR: 0, twL: 0, gfR: 0, gfL: 0};
const q0_hover = {name: 'q0_hover', src: 'v4 17.6-19.5 (ref/p2_Q0_fall.jpg: her silhouette high, legs spread)', keys: [
  K(0, HOVER), K(20, {sh: [0, .16, 0], ...HANG(.18), lF: 18, thR: 134, thL: 134}), K(40, HOVER)]};
const q0_dive = {name: 'q0_dive', src: 'v4 19.5-21.4 (ref/p2_Q0_fall.jpg: the crimson streak, the impact, the blade eruption)', keys: [
  K(0, {...HOVER, to: [-20, 0, 0]}),
  K(4, {rt: [-40, 0, 0], spR: SG, spL: SG, thR: -24, thL: -24, edR: 1, edL: 1, gR: [40, 56, .5], gL: [40, 56, .5], lS: .6, lF: -10, ...HANG(.3, .3)}),
  K(14, {rt: [-40, 0, 0]}),
  K(17, {thR: 40, thL: 40}, 'l'),
  K(20, {rt: [0, 0, 0], thR: 128, thL: 128, sh: [0, -.22, 0], to: [-24, 0, 0], hd: [-8, 0, 0], ...WIDE, kR: [.2, 0, -1], kL: [.2, 0, -1], lS: 1, lF: -5}, 'i'),   // impact
  K(24, {sh: [0, -.2, 0], spR: FR, spL: FR, thR: 150, thL: 150, edR: -1, edL: -1, gR: [60, -30, .52], gL: [60, -30, .52]}),
  K(28, {sh: [0, -.08, 0], to: [-6, 0, 0], gR: [80, -20, .56], gL: [80, -20, .56], thR: 160, thL: 160, lF: 28}, 'o'),   // blades
  K(40, REST2())]};
// Q1 사형장으로의 초대 (P2, v4 28.5-37): spin (h1), the inward cross slash (h2), a thrown crescent (h3: the right scythe leaves
// and re-forms), a right sweep (h4), a left sweep (h5), both thrown (h6)
const TWIN_OUT = {spR: [-92, 0, 0], spL: [-92, 0, 0], thR: 90, thL: 90, edR: 1, edL: -1, twR: 10, twL: -10, ...LEV, ...LEVL};
const q1 = {name: 'q1', src: 'v4 28.5-37 (ref/p2_Q1_twin.jpg)', cuts: [46, 52, 100, 108], edgeOk: [[38, 46], [92, 100]], keys: [
  K(0, {}),
  K(6, {...TWIN_OUT, sh: [0, -.1, 0], ...WIDE}),
  K(8, {rt: [0, 0, 0]}),
  K(20, {rt: [0, 360, 0]}, 'l'),                                                                         // h1 spin (14)
  K(24, {thR: 130, thL: 130, edR: -1, edL: -1, to: [8, 0, 0], rt: [0, 360, 0]}),
  K(30, {thR: -30, thL: -30, to: [-10, 0, 0], sh: [0, -.12, 0]}, 'i'),                                    // h2 the cross
  K(34, {thR: -42, thL: -42}, 'o'),
  K(40, {spR: SG, thR: -60, edR: 1, gfR: 0, gR: [20, 50, .5], spL: FR, thL: 150, edL: -1, gfL: 0, gL: [20, -50, .45], to: [4, 20, 0]}),
  K(45, {thR: 80, gR: [0, 12, .58], to: [-10, -14, 0], ssR: [1, 1, 1]}, 'i'),
  K(46, {thR: 90, ssR: [0, 0, 0]}),                                                                       // h3: thrown
  K(51, {ssR: [0, 0, 0], spR: FR, thR: 150, edR: -1, gR: [20, -45, .48], to: [0, 0, 0]}),
  K(52, {ssR: [.1, .3, 1]}),
  K(56, {ssR: [1, 1, 1]}),
  K(60, {spR: HZ, thR: 130, edR: -1, twR: -18, ...LEV, to: [6, 30, 0]}),
  K(66, {thR: -40, to: [-6, -20, 0]}, 'i'),                                                              // h4
  K(70, {thR: -60}, 'o'),
  K(76, {spL: HZ, thL: 130, edL: -1, twL: -18, ...LEVL, to: [6, -30, 0], spR: FR, thR: 150, gfR: 0, gR: [14, -50, .44], twR: 30}),
  K(82, {thL: -40, to: [-6, 20, 0]}, 'i'),                                                               // h5
  K(86, {thL: -60}, 'o'),
  K(92, {spR: SG, spL: SG, thR: -60, thL: -60, edR: 1, edL: 1, gfR: 0, gfL: 0, gR: [30, 50, .5], gL: [30, 50, .5], to: [10, 0, 0], twR: 0, twL: 0}),
  K(99, {thR: 80, thL: 80, gR: [15, 10, .58], gL: [15, 10, .58], to: [-12, 0, 0], ssR: [1, 1, 1], ssL: [1, 1, 1]}, 'i'),
  K(100, {thR: 90, thL: 90, ssR: [0, 0, 0], ssL: [0, 0, 0]}),                                             // h6: both thrown
  K(107, {ssR: [0, 0, 0], ssL: [0, 0, 0], ...REST2({rt: [0, 360, 0]})}),
  K(108, {ssR: [.1, .3, 1], ssL: [.1, .3, 1]}),
  K(114, {ssR: [1, 1, 1], ssL: [1, 1, 1]}),
  K(124, REST2({rt: [0, 360, 0]}))]};
// Q2 불꽃이 타오르는 낫 (v4 37-40, v6 0-5): the right scythe whirled into a flaming wheel and flung (20), the dash after it (34),
// the left sweep on arrival (42); the right scythe re-forms on the way
const q2 = {name: 'q2', src: 'v4 37-40, v6 0-5 (ref/p2_Q2_throw_a.jpg, _b.jpg)', cuts: [20, 38], keys: [
  K(0, {}),
  K(4, {spR: [24, 90, 0], thR: 0, edR: 1, twR: 0, gR: [40, 44, .5], gfR: 0, to: [4, 20, 0], ...WIDE}),
  K(19, {thR: 500, gR: [12, 36, .58], ssR: [1, 1, 1]}, 'l'),
  K(20, {thR: 540, ssR: [0, 0, 0]}),                                                                      // release
  K(26, {gR: [30, -30, .45], to: [0, 6, 0]}),
  K(30, {sh: [0, -.16, 0], to: [-20, 0, 0], spL: HZ, thL: 140, edL: -1, twL: -18, ...LEVL}),
  K(34, {rt: [-20, 0, 0], fR: [-.18, .1, .3], fL: [.18, .05, -.08]}),                                     // go
  K(37, {ssR: [0, 0, 0], spR: FR, thR: 150, edR: -1, twR: 30, gR: [14, -50, .44]}),
  K(38, {ssR: [.1, .3, 1]}),
  K(40, {ssR: [1, 1, 1], rt: [0, 0, 0], ...WIDE, thL: 136}),
  K(42, {thL: 40, to: [-8, 30, 0]}, 'l'),                                                                 // slash
  K(44, {thL: -36}, 'l'),
  K(46, {thL: -70}, 'o'),
  K(70, REST2())]};
// Q3 붉은 죽음의 무도회 (v6 5-15.5): the legs flare as she whips round (0), the spin (14)
const q3 = {name: 'q3', src: 'v6 5-15.5 (ref/p2_Q3_rear.jpg)', keys: [
  K(0, {}),
  K(3, {...TWIN_OUT, lF: 30, lS: 1, sh: [0, -.1, 0], ...WIDE}, 'o'),                                     // whip
  K(7, {rt: [0, 0, 0]}),
  K(21, {rt: [0, 360, 0]}, 'l'),                                                                          // spin (14)
  K(24, {lF: 10}),
  K(36, REST2({rt: [0, 360, 0]}))]};
// Q4 떠오르는 재액의 달 (v6 15.5-26.5): up 4 b, the scythes crossed before her chest while the legs spread behind her, the aim
// line and the reticle at her chest (0-20), the recoil of the beam (26), the landing
const AIM = {...HOVER, gR: [-12, 0, .42], gL: [-12, 0, .42], spR: FR, spL: FR, thR: 12, thL: 12, edR: -1, edL: -1, lS: 1, lF: 24, to: [-4, 0, 0], hd: [0, 0, 0]};
const q4_up = {name: 'q4_up', src: 'v6 15.5-17 (ref/p2_Q4_beam.jpg)', keys: [
  K(0, {}), K(4, {sh: [0, -.18, 0], to: [-12, 0, 0]}), K(8, {sh: [0, .1, 0], ...HANG(.1), to: [4, 0, 0]}, 'o'),
  K(14, {...HOVER, lF: 18}), K(20, AIM)]};
const q4_shot = {name: 'q4_shot', src: 'v6 17-25 (ref/p2_Q4_beam.jpg: shots 17.75 / 20.25 / 22.75)', keys: [
  K(0, AIM), K(18, {sh: [0, .13, 0], to: [-6, 0, 0]}), K(20, {}), K(24, {to: [-8, 0, 0]}),
  K(26, {to: [12, 0, 0], rt: [10, 0, 0], gR: [80, 10, .56], gL: [80, 10, .56], thR: 60, thL: 60, lF: 36}, 'i'),   // fire
  K(34, {to: [4, 0, 0], rt: [4, 0, 0], lF: 28}, 'o'),
  K(50, AIM)]};
const q4_land = {name: 'q4_land', src: 'v6 25-26.5 (ref/p2_Q4_beam.jpg)', keys: [
  K(0, AIM), K(8, {...HOVER, lS: .5, lF: 4, ...HANG(.08)}),
  K(12, {sh: [0, -.16, 0], ...WIDE, kR: [.2, 0, -1], kL: [.2, 0, -1], lS: .3, to: [-10, 0, 0]}, 'i'),   // land
  K(16, REST2({sh: [0, -.03, 0]}))]};
// Q5 붉은 피의 연회 (P2; v6 26-40, v7 0-27): both scythes raised and crossed overhead, the brand (22: the cross brought down);
// A 형벌의 핏값: the slam at her feet (95), the outward sweep (121), risen high on the spread legs and the great slam (158)
const qBrand = [
  K(0, {}),
  K(8, {spR: FR, spL: FR, thR: -20, thL: -20, edR: 1, edL: 1, twR: 0, twL: 0, gR: [10, 50, .5], gL: [10, 50, .5], lF: 15, lS: 1, hd: [10, 0, 0]}),
  K(20, {thR: -26, thL: -26, sh: [0, .03, 0]}),
  K(22, {thR: 120, thL: 120, gR: [60, -10, .55], gL: [60, -10, .55], to: [-6, 0, 0], hd: [0, 0, 0]}, 'i'),   // brand
  K(26, {thR: 128, thL: 128})];
const q5a = {name: 'q5a', src: 'v7 4.2-12.3 (ref/p2_Q5_banquet_b.jpg: disc, donut, the wide disc)', keys: [...qBrand,
  K(40, {sh: [0, .3, 0], ...HANG(.3), gR: [80, 0, .56], gL: [80, 0, .56], thR: 150, thL: 150, lF: 10}),
  K(58, {thR: 30, thL: 30, edR: 1, edL: 1, gR: [70, 30, .55], gL: [70, 30, .55]}),                       // ring1 tell
  K(90, {thR: 26, thL: 26, sh: [0, .34, 0]}),
  K(95, {thR: 170, thL: 170, sh: [0, .05, 0], ...HANG(.06), to: [-14, 0, 0], lF: 0}, 'i'),             // hit1
  K(100, {spR: HZ, spL: HZ, thR: -40, thL: -40, edR: 1, edL: 1, ...LEV, ...LEVL, to: [0, 0, 0], lF: 6, sh: [0, .1, 0]}),   // donut
  K(117, {thR: -48, thL: -48, sh: [0, .14, 0]}),
  K(121, {thR: 100, thL: 100, lF: 20}, 'i'),                                                             // hit2: the outward sweep
  K(130, {sh: [0, .8, 0], ...HANG(.8), lF: 30, spR: FR, spL: FR, thR: 0, thL: 0, gfR: 0, gfL: 0, gR: [20, 60, .5], gL: [20, 60, .5]}, 'o'),   // ring3
  K(154, {to: [10, 0, 0], thR: -8, thL: -8, sh: [0, .86, 0]}),
  K(158, {sh: [0, .0156, 0], ...WIDE, kR: [.2, 0, -1], kL: [.2, 0, -1], thR: 172, thL: 172, to: [-20, 0, 0], lF: 6}, 'i'),   // hit3
  K(166, {sh: [0, -.04, 0]}),
  K(180, REST2())]};
// B 붉은 피의 사형: the vertical X carved before her (26-50: right then left diagonal), the rapid slashes all round her (s1-s9
// every 3 t, alternating hands, the torso turning with each), both raised and slammed for the final (96)
const rapid = [];
for (let i = 1; i <= 9; i++) {
  const t = 53 + 3 * i, R = i % 2 === 1;
  rapid.push(K(t, R ? {thR: -30, thL: 120, to: [-6, -20, 0]} : {thR: 120, thL: -30, to: [-6, 20, 0]}, 'i'));
}
const q5b = {name: 'q5b', src: 'v6 31.5-35.3, v7 16-19.3 (ref/p2_Q5_banquet_a.jpg, _b.jpg)', edgeOk: [[53, 82]], keys: [...qBrand,
  K(30, {spR: FR, thR: 40, edR: -1, gR: [60, 50, .55]}),
  K(34, {thR: -118, gR: [-30, -12, .5], to: [-6, -16, 0]}, 'l'),                                      // x: the right diagonal
  K(38, {spL: FR, thL: 40, edL: -1, gL: [60, 50, .55], spR: FR, thR: 130, gR: [24, -30, .5], to: [0, 0, 0]}),
  K(46, {thL: -118, gL: [-30, -12, .5], to: [-6, 16, 0]}, 'l'),                                        // the left diagonal
  K(50, {thR: 20, thL: 20, edR: -1, edL: -1, gR: [30, 30, .5], gL: [30, 30, .5], to: [0, 0, 0]}),    // mark
  K(53, {spR: HZ, spL: HZ, thR: 120, thL: 120, edR: -1, edL: -1, twR: -10, twL: -10, ...LEV, ...LEVL, sh: [0, -.1, 0], ...WIDE}),
  ...rapid,                                                                                             // s1..s9 (56..80)
  K(84, {spR: FR, spL: FR, thR: 0, thL: 0, gfR: 0, gfL: 0, gR: [20, 60, .5], gL: [20, 60, .5], edR: 1, edL: 1, sh: [0, .05, 0], to: [6, 0, 0]}),
  K(92, {lF: 25, thR: -6, thL: -6}),
  K(96, {thR: 170, thL: 170, sh: [0, -.2, 0], to: [-20, 0, 0], lF: 4}, 'i'),                            // final
  K(104, {sh: [0, -.18, 0]}),
  K(136, REST2())]};
// Q6 핏빛 연회 (v7 28-40): up over the arena on the fully spread legs (20), the moon (30), six feather volleys flicked from the
// legs (50-100), the orbs gathered overhead (110) and flung to the rim (125), the dive (160) and the impact (168)
const FLY = {sh: [0, .1, 0], ...HANG(.12), lS: 1, lF: 30, gR: [85, 10, .56], gL: [85, 10, .56], spR: FR, spL: FR, thR: 150, thL: 150, edR: -1, edL: -1, gfR: 0, gfL: 0,
  hd: [-14, 0, 0], to: [4, 0, 0], twR: 0, twL: 0};
const volleys = [];
for (let i = 1; i <= 6; i++) { const t = 40 + 10 * i; volleys.push(K(t - 3, {lF: 30}), K(t, {lF: 42, to: [8, 0, 0]}, 'i'), K(t + 4, {lF: 30, to: [4, 0, 0]}, 'o')); }
const q6 = {name: 'q6', src: 'v7 28-40 (ref/p2_Q6_feast.jpg)', keys: [
  K(0, {}), K(6, {sh: [0, -.2, 0], to: [-10, 0, 0], lF: 16}),
  K(12, {sh: [0, .2, 0], ...HANG(.2), lF: 4, lS: .6, to: [6, 0, 0]}, 'o'),                              // fly
  K(20, FLY),                                                                                           // gone (high)
  K(30, {hd: [10, 0, 0], gR: [70, 40, .55], gL: [70, 40, .55]}),                                         // moon
  ...volleys,
  K(110, {gR: [20, 70, .5], gL: [20, 70, .5], thR: 0, thL: 0, edR: 1, edL: 1, hd: [16, 0, 0]}),          // orbs
  K(122, {gR: [24, 74, .5], gL: [24, 74, .5]}),
  K(125, {gR: [90, -10, .58], gL: [90, -10, .58], thR: 120, thL: 120, lF: 40}, 'i'),                     // toss
  K(140, {to: [-10, 0, 0], hd: [-20, 0, 0], lF: 30}),                                                    // lock
  K(156, {spR: SG, spL: SG, thR: -30, thL: -30, gR: [30, 56, .5], gL: [30, 56, .5]}),
  K(160, {rt: [-40, 0, 0], lS: .5, lF: -20, ...HANG(.3, .3)}),                                            // dive
  K(165, {thR: 40, thL: 40}, 'l'),
  K(168, {rt: [0, 0, 0], thR: 128, thL: 128, sh: [0, -.22, 0], to: [-24, 0, 0], hd: [-8, 0, 0], ...WIDE, kR: [.2, 0, -1], kL: [.2, 0, -1], lS: 1, lF: 10}, 'i'),   // impact
  K(176, {sh: [0, -.2, 0]}),
  K(200, REST2())]};

// ===== death (PLAN §3.3, 110 t, form p2; wiki: no last words, she puts her scythes away and vanishes in flame) ====================
const death = {name: 'death', src: 'designed (PLAN §3.3, wiki 「자신의 낫을 집어넣는 모션과 함께 불꽃으로 사라진다」)', keys: [
  K(0, {}),
  K(3, {to: [10, 6, 0], hd: [10, 0, 0], sh: [0, -.03, .04]}, 'o'),                                      // stop
  K(10, {thR: 150, thL: 150, gR: [30, -50, .5], gL: [30, -50, .5], to: [-10, 0, 0], hd: [-16, 0, 0], sh: [0, -.06, 0], lS: 0, lF: -6}),   // lower
  K(30, {ssR: [1, 1, 1], ssL: [1, 1, 1]}),                                                              // fade: into embers
  K(36, {ssR: [.12, .12, .12], ssL: [.12, .12, .12]}, 'i'),
  K(38, {ssR: [0, 0, 0], ssL: [0, 0, 0]}),
  K(39, {wR: 0, wL: 0, aR: [8, 12, 1], aL: [8, 12, 1]}),
  K(50, {sh: [0, .0156, 0], to: [0, 0, 0], hd: [0, 0, 0], aR: [6, 10, 1], aL: [6, 10, 1], lF: -10}),     // stand
  K(70, {hd: [6, 0, 0], aR: [14, 24, 1], aL: [14, 24, 1], lP: [.7, .7, .7], lF: -8}),                    // flames
  K(92, {lP: [.3, .3, .3], vis: 1}),
  K(96, {vis: 0}, 'i'),                                                                                 // gone
  K(110, {vis: 0})]};

export const CLIPS = [idle, walk, strafe_l, strafe_r, idle2, walk2, strafe2_l, strafe2_r, backstep, flinch, brk, stun, stun2, intro,
  a2, a4, a5, b1, b2, c1, c2, d1, d2, e1, f1, g1, h1, e70, t_p2, q0_hover, q0_dive, q1, q2, q3, q4_up, q4_shot, q4_land, q5a, q5b, q6, death];
