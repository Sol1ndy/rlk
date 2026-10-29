// The 41 clips of the 타키 (Tachy) rig (S:tk/PLAN.md §2.4, §3; contract tools/mboss_tachy/api.py CLIPS: names, lengths,
// loops and event ticks are frozen, this file only authors the motion). Format and sampling: mboss_rig_clips.mjs
// (keys [tick, sparse pose, ease] merged onto DEFAULT_POSE; ease of the segment arriving at a key: 'io' smooth, 'i'
// accelerate into the key (strikes, falls), 'o' decelerate (leaps, settles), 'l' linear (spins)). Pose channels:
// tachy_pose.mjs. Clip ticks are played ticks; the module schedules its hits on the events.
//
// Per clip (beyond keys):
//   looks   [[t, channel, value]]: temporary look swaps at a tick ('edge' glint / yellow / pyro / electro / off,
//           'chest' amber / red / gold / off, 'visor' pyro / electro / abyss / off, value 'restore' = back to the stored
//           look), or a stored look ('set:<channel>/<value>' = the rig's look/<channel>/<value>)
//   formAt  {t: form}: the form the solver uses from tick t (t1_wings cape -> winged, t2_abyss winged -> abyss)
//   swapAt  {t: form}: the wing / tendril model swap (look/form/<form>) at tick t
//   cuts    ticks where every part takes a 1-tick key (model swaps)
//   lines   {t: [commands]}: extra commands (the intro's cable props)
import {accumulate as accumulateLib, sampleClip as sampleLib} from './mboss_rig_clips.mjs';

// ---- default pose: the P1 combat stance (v8 0-3, fx_a v8 6.2): weight back, the long sword low in the right hand with
// its tip forward-right near the floor, the left arm loose, the cape hanging --------------------------------------------
export const DEFAULT_POSE = {
  pos: [0, -.03, 0], rot: [0, 0, 0], tor: [-4, -6, 0], head: [-4, 6, 0], helm: 0,
  fL: [.14, .085, -.1], fR: [-.15, .085, .12], fpL: 0, fpR: 0, fyL: 6, fyR: 14, kL: [.15, 0, -1], kR: [-.15, 0, -1],
  hold: 1, gB: 38, gE: -42, gD: .52, gF: 0, gL: .55, cB: 18, cR: 0, th: -34, ed: -1, tw: 0, lh: 0,
  aL: [-6, 12, .97], aR: [8, 14, .95], pL: [.55, -.35, .75], pR: [.55, -.35, .75], hwL: [0, 0, 0], hwR: [0, 0, 0],
  plL: [.3, .06, -.45], plR: [-.3, .06, -.45], plwL: 0, plwR: 0,
  wS: 0, wF: 0, wW: 0, wFl: 0, td: [30, 0, 35], tdS: 1, hairF: 0, hairS: 0, vis: 1, drawn: 1,
  scab: 'empty', hL: 'open', hR: 'grip',
};
export const DISCRETE = ['scab', 'hL', 'hR'];
const V = (...a) => a;
const K = (t, pose, ease = 'io') => [t, pose, ease];

// ---- clip table ----
const clips = [];
const C = (name, keys, extra = {}) => clips.push({name, keys, ...extra});
// ---- building blocks -----------------------------------------------------------------------------------------------------------
// The blade (tachy_pose.mjs): plane bearing cB, roll cR (0 vertical through the bearing, 90 horizontal: th + toward her
// left; -45 = the plane's up tilted to her right: high-right <-> low-left diagonals; +45 high-left <-> low-right), angle th
// in the plane (vertical plane: 0 forward, 90 up, 180 back), edge leading toward +th (ed 1) or -th (ed -1). Grip: gF 1 =
// on the lever gL from the right shoulder (one hand; the chest centre with lh 1) along the blade.
const B = (cB, cR, th, ed, x = {}) => ({cB, cR, th, ed, gF: 1, ...x});
const F_ST = {fL: [.14, .085, -.1], fR: [-.15, .085, .12], fyL: 6, fyR: 14, fpL: 0, fpR: 0};
const F_WIDE = {fL: [.25, .085, -.22], fR: [-.25, .085, .26], fyL: 14, fyR: 24, fpL: 0, fpR: 0};
const F_LUNGE = {fL: [.16, .085, -.6], fR: [-.18, .085, .46], fyL: 0, fyR: 30, fpL: 0, fpR: 0};       // left foot forward
const F_LUNGE_R = {fL: [.18, .085, .42], fR: [-.15, .085, -.56], fyL: 30, fyR: 0, fpL: 0, fpR: 0};   // right foot forward
const F_TOG = {fL: [.1, .085, -.03], fR: [-.1, .085, .04], fyL: 4, fyR: 4, fpL: 0, fpR: 0};
// the P1 combat stance (= DEFAULT_POSE)
const ST = {pos: [0, -.03, 0], rot: [0, 0, 0], tor: [-4, -6, 0], head: [-4, 6, 0], ...F_ST, hold: 1, lh: 0, gB: 38, gE: -42, gD: .52, gF: 0, gL: .55,
  cB: 18, cR: 0, th: -34, ed: -1, tw: 0, aL: [-6, 12, .97], aR: [8, 14, .95], pL: [.55, -.35, .75], pR: [.55, -.35, .75], wS: 0, wF: 0, wW: 0, wFl: 0,
  hairF: 0, hairS: 0, vis: 1, plwL: 0, plwR: 0, helm: 0, drawn: 1, tdS: 1, kL: [.15, 0, -1], kR: [-.15, 0, -1], hwL: [0, 0, 0], hwR: [0, 0, 0]};
const CROUCH = {pos: [0, -.2, 0], tor: [-14, -8, 0], head: [-2, 8, 0], ...F_WIDE};
const LOW = {pos: [0, -.34, 0], tor: [-24, -8, 0], head: [8, 8, 0], fL: [.25, .085, -.3], fR: [-.25, .085, .32], fyL: 14, fyR: 24};
// airborne (leaps, hover): legs hanging bent, toes down
const AIR = {pos: [0, .02, 0], tor: [-6, -6, 0], fL: [.13, .3, -.12], fR: [-.13, .2, .1], fpL: -40, fpR: -45, fyL: 6, fyR: 10, kL: [.15, -.2, -1], kR: [-.15, -.2, -1]};
// kneel on the right knee, left foot planted forward (stun, T1, death)
const KNEEL = {pos: [0, -.5, .02], tor: [-26, -4, 0], head: [-24, 4, 0], fL: [.17, .085, -.38], fR: [-.15, .1, .5], fpL: 0, fpR: -60, fyL: 8, fyR: 10,
  kL: [.2, 0, -1], kR: [-.1, -1, -.4], aL: [42, 8, .78]};
const hold = (a, b) => ({...a, ...b});

// ---- locomotion ----------------------------------------------------------------------------------------------------------------
C('idle', [K(0, {...ST, wFl: 4}), K(20, {pos: [0, -.05, 0], tor: [-6, -7, 0], head: [-5, 4, 0], gE: -43, th: -35, aL: [-4, 13, .97], wFl: 4}), K(40, {...ST, wFl: 4})],
  {src: 'v8 0-3 (P1 stance), v7 0.4 / v4 38.0 (winged rest)'});
{
  const W0 = {...ST, pos: [0, -.07, 0], tor: [-6, -10, 0], fL: [.12, .085, -.3], fR: [-.12, .11, .28], fpL: 0, fpR: -25, aL: [-20, 12, .97], th: -36, wFl: 6};
  C('walk', [K(0, W0), K(3, {pos: [0, -.04, 0], fL: [.12, .085, -.16], fR: [-.12, .2, .08], fpR: 5}), K(6, {pos: [0, -.02, 0], tor: [-6, -6, 0], fL: [.12, .085, -.02], fR: [-.12, .19, -.14], fpR: 12, aL: [0, 12, .97], th: -33}),
    K(9, {pos: [0, -.04, 0], fL: [.12, .11, .12], fR: [-.12, .12, -.28], fpL: -5, fpR: 6}), K(12, {pos: [0, -.07, 0], tor: [-6, -2, 0], fL: [.12, .11, .28], fR: [-.12, .085, -.3], fpL: -25, fpR: 0, aL: [18, 12, .97], th: -36}),
    K(15, {pos: [0, -.04, 0], fL: [.12, .2, .08], fR: [-.12, .085, -.16], fpL: 5}), K(18, {pos: [0, -.02, 0], tor: [-6, -6, 0], fL: [.12, .19, -.14], fR: [-.12, .085, -.02], fpL: 12, aL: [0, 12, .97], th: -33}),
    K(21, {pos: [0, -.04, 0], fL: [.12, .12, -.28], fR: [-.12, .11, .12], fpL: 6, fpR: -5}), K(24, W0)], {src: 'v6 / v8 prowl between attacks'});
  const strafe = s => {
    // s = +1 toward her left; the leading foot steps out (0-6), the trailing foot closes (10-16), the sword ready in front
    const lead = s > 0 ? 'fL' : 'fR', trail = s > 0 ? 'fR' : 'fL', lp = s > 0 ? 'fpL' : 'fpR', tp = s > 0 ? 'fpR' : 'fpL';
    const S0 = {...ST, pos: [0, -.08, 0], tor: [-8, -6, 3 * s], head: [-4, 6, -3 * s], gB: 25, gE: -30, gD: .55, th: -22, aL: [10, 22, .95], wFl: 6,
      [lead]: [s * .14, .085, s > 0 ? -.08 : .1], [trail]: [-s * .14, .085, s > 0 ? .1 : -.08]};
    return [K(0, S0), K(3, {[lead]: [s * .22, .17, s > 0 ? -.08 : .1], [lp]: -10, pos: [0, -.05, 0]}), K(6, {[lead]: [s * .3, .085, s > 0 ? -.08 : .1], [lp]: 0, pos: [0, -.1, 0]}),
      K(10, {[lead]: [s * .26, .085, s > 0 ? -.08 : .1], [trail]: [-s * .3, .085, s > 0 ? .1 : -.08], pos: [0, -.09, 0]}),
      K(13, {[trail]: [-s * .22, .16, s > 0 ? .1 : -.08], [tp]: -10, pos: [0, -.05, 0]}), K(16, {[trail]: [-s * .14, .085, s > 0 ? .1 : -.08], [tp]: 0, pos: [0, -.08, 0]}),
      K(20, S0)];
  };
  C('strafe_l', strafe(1), {src: 'v5 / v6 circling'}); C('strafe_r', strafe(-1), {src: 'v5 / v6 circling'});
}
C('backstep', [K(0, ST), K(3, {...CROUCH, pos: [0, -.18, 0]}, 'o'), K(5, {pos: [0, .04, .05], tor: [2, -6, 0], fL: [.15, .22, -.12], fR: [-.16, .2, .1], fpL: -25, fpR: -30, aL: [30, 40, .95], wF: .5}, 'o'),
  K(8, {pos: [0, .02, 0], fL: [.15, .16, -.1], fR: [-.16, .14, .06], fpL: -10, fpR: -15}), K(10, {...CROUCH, pos: [0, -.22, 0], aL: [12, 30, .95], wF: .2}, 'i'), K(12, {pos: [0, -.14, 0], tor: [-10, -6, 0], wF: 0})],
  {src: 'v4 / v3 hop back before W1'});
C('flinch', [K(0, ST), K(2, {tor: [8, -10, 4], head: [10, 0, 6], pos: [0, -.05, .04], aL: [12, 32, .95], th: -42}, 'o'), K(6, ST)], {src: 'hit reaction'});
{
  const A = {pos: [0, -.24, .06], rot: [0, 0, 4], tor: [-26, -10, 8], head: [-28, 12, 10], ...F_WIDE, gB: 40, gE: -60, gD: .5, gF: 0, th: -50, aL: [24, 8, .95], wF: .1};
  const Bp = {pos: [0, -.28, .04], rot: [0, 0, -3], tor: [-30, -6, -4], head: [-32, 6, -6], gE: -62, th: -52, aL: [30, 4, .95]};
  C('stagger', [K(0, ST), K(4, {...A, tor: [6, -14, 10], head: [12, 10, 12], pos: [0, -.12, .1], aL: [30, 50, .95]}, 'o'), K(10, A), K(30, Bp), K(50, A)],
    {src: 'v10 3.6-4.0 (staggered by the reaction), G3 backfire'});
}
{
  const KN = {...ST, ...KNEEL, gB: 55, gE: -66, gD: .62, th: -78, cB: 30, aL: [44, 6, .8], hairF: .3, wF: .1};
  C('stun', [K(0, ST), K(6, {...CROUCH, tor: [-20, -6, 6], head: [-16, 10, 6], pos: [0, -.25, .04]}, 'o'), K(20, KN, 'io'), K(45, {pos: [0, -.53, .02], tor: [-30, -4, 0], head: [-28, 4, 0]}),
    K(70, {pos: [0, -.5, .02], tor: [-26, -4, 0], head: [-24, 4, 0]}), K(100, KN), K(108, {...CROUCH, pos: [0, -.24, 0], hairF: 0}, 'o'), K(120, ST)],
    {src: 'v11 (drop to a knee), G2 mantle break stun'});
}
{
  const swap = () => [K(0, ST),
    K(6, {pos: [0, -.16, 0], tor: [-10, 24, 0], head: [-6, -16, 0], ...F_WIDE, ...B(105, 0, -32, 1, {gL: .55}), aL: [22, 35, .95], wF: .25}, 'o'),   // the tip dragged on the floor behind-right
    K(10, {tor: [-4, 8, 0], ...B(60, 0, 10, 1, {gL: .55})}),
    K(14, {pos: [0, -.05, 0], tor: [2, -10, 0], head: [-2, 4, 0], ...B(20, 0, 84, 1, {gL: .5}), aL: [10, 26, .95], wF: .35}, 'o'),                     // flung up vertical: the element takes
    K(19, {tor: [-2, -8, 0], ...B(20, 0, 58, 1, {gL: .5})}), K(24, ST)];
  C('swap_pyro', swap(), {looks: [[14, 'edge', 'set:edge/pyro'], [14, 'visor', 'set:visor/down_pyro']], src: 'v6 / v7 blade drag + flare (G1 swap)'});
  C('swap_electro', swap(), {looks: [[14, 'edge', 'set:edge/electro'], [14, 'visor', 'set:visor/down_electro']], src: 'v6 / v7 blade drag + crackle (G1 swap)'});
}
C('blink_out', [K(0, ST), K(3, {...CROUCH, pos: [0, -.14, 0], wF: .35}, 'o'), K(6, {vis: 0, pos: [0, -.06, 0]}, 'i'), K(8, {vis: 0})], {src: 'v4 29.6-30.2, v6 0-0.4 (vanish)'});
C('blink_in', [K(0, {...ST, ...CROUCH, vis: 0, wF: .5, ...B(70, 0, -30, 1, {gL: .55})}), K(3, {vis: 1}, 'o'), K(8, {pos: [0, -.12, 0], tor: [-10, -6, 0], wF: .2}), K(10, {pos: [0, -.1, 0]})],
  {src: 'v4 36.4 (reappears, wings spread, blade low)'});

// ---- airborne ------------------------------------------------------------------------------------------------------------------
const HOV = {...ST, ...AIR, gB: 40, gE: -30, gD: .55, gF: 0, cB: 30, th: -45, aL: [10, 40, .95], wFl: 20, wS: .1, wF: .2};
C('leap_up', [K(0, ST), K(5, {...LOW, wF: .4}, 'o'), K(6, {pos: [0, .06, 0], tor: [-2, -6, 0], fL: [.13, .085, -.06], fR: [-.13, .085, .1], fpL: -30, fpR: -30, aL: [30, 30, .95], wF: .7}, 'i'),
  K(10, {...HOV, fL: [.14, .42, -.22], fR: [-.14, .34, .12], wFl: 26}, 'o'), K(16, HOV)], {src: 'v3 29-30 (leaps up for W2)', preview: 'winged'});
C('hover', [K(0, HOV), K(10, {pos: [0, .06, 0]}), K(20, {pos: [0, .07, 0], th: -48}), K(30, {pos: [0, .03, 0]}), K(40, HOV)], {src: 'v3 30-35 hovering', preview: 'winged'});
const IMPACT = {...ST, pos: [0, -.32, -.02], rot: [0, 0, 0], tor: [-26, -4, 0], head: [6, 4, 0], ...F_WIDE, lh: .7, gF: 1, gL: .45, cB: 0, cR: 0, th: -70, ed: -1,
  aL: [30, 30, .9], wF: .5, wFl: 0, kL: [.15, 0, -1], kR: [-.15, 0, -1]};
C('dive', [K(0, HOV), K(4, {rot: [-38, 0, 0], tor: [-8, 0, 0], ...B(0, 0, -80, -1, {gL: .5}), lh: 1, wS: -.5, wF: .3, wFl: 0, fL: [.12, .32, .26], fR: [-.12, .26, .3], fpL: -45, fpR: -45}, 'i'),
  K(8, {rot: [-20, 0, 0], ...B(0, 0, -75, -1, {gL: .5}), fL: [.2, .2, -.1], fR: [-.2, .2, .15]}), K(10, IMPACT, 'i'), K(12, {pos: [0, -.3, -.02]})], {src: 'v4 13.0-13.5 (dark streak, blade down)', preview: 'winged'});
C('land', [K(0, IMPACT), K(6, {pos: [0, -.24, 0], lh: .3, th: -55}), K(14, {...ST, wF: 0}, 'o'), K(16, ST)], {src: 'v4 13.5-14.5', preview: 'winged'});
const HOVH = {...HOV, wS: .28, wF: .4, wFl: 14, ...B(0, 0, -86, -1, {gL: .5}), lh: .6, tor: [-12, 0, 0]};
C('leap_high', [K(0, ST), K(6, {...LOW, pos: [0, -.4, 0], wF: .5}, 'o'), K(8, {pos: [0, .08, 0], tor: [4, -6, 0], fL: [.12, .085, -.04], fR: [-.12, .085, .08], fpL: -35, fpR: -35, aL: [60, 30, .95], wF: .8, wS: .2}, 'i'),
  K(12, {...HOVH, fL: [.13, .5, -.15], fR: [-.13, .45, .1], wFl: 24}, 'o'), K(16, HOVH)], {src: 'v4 5.8-7 (launches high)', preview: 'winged'});
C('hover_high', [K(0, HOVH), K(20, {pos: [0, .06, 0], wF: .5}), K(40, HOVH)], {src: 'v4 7-12 (glinting high above)', preview: 'winged'});

// ---- melee patterns (S3) ---------------------------------------------------------------------------------------------------------
{
  // A1 gap-close dash (v8 4.0-4.4, fx_a 2): coil with the blade low back-right (0-14), dash, the slash crossing her front at 20
  const TELL = {pos: [0, -.24, .02], tor: [-20, 30, 0], head: [-6, -24, 0], fL: [.16, .085, -.42], fR: [-.2, .085, .36], fyL: 0, fyR: 30,
    ...B(0, 75, -150, 1, {gL: .55}), aL: [62, 18, .9], wF: .35};
  C('a1_dash', [K(0, ST), K(6, TELL, 'o'), K(14, {...TELL, pos: [0, -.27, .04], tor: [-22, 32, 0]}),
    K(16, {rot: [-14, 0, 0], pos: [0, -.2, -.1], fL: [.14, .14, -.45], fR: [-.18, .085, .42], fpL: -10, tor: [-12, 34, 0], wF: .9}, 'i'),
    K(18, {...B(0, 75, -118, 1, {gL: .52}), tor: [-10, 36, 0], fL: [.15, .085, -.55], fpL: 0}, 'i'),
    K(20, {...B(0, 75, 0, 1, {gL: .58}), rot: [-8, 0, 0], tor: [-8, 0, 0], head: [-4, 0, 0], pos: [0, -.2, -.14], ...F_LUNGE, aL: [-30, 55, .95]}, 'l'),
    K(23, {...B(0, 75, 98, 1, {gL: .55}), tor: [-6, -38, 0], head: [-4, 22, 0], aL: [-40, 62, .95], wF: .5}, 'o'),
    K(28, {pos: [0, -.12, -.06], rot: [0, 0, 0], tor: [-6, -20, 0], ...B(0, 40, 60, 1, {gL: .55}), wF: .2}), K(34, ST)],
    {looks: [[0, 'chest', 'red'], [0, 'visor', 'abyss'], [20, 'chest', 'restore'], [20, 'visor', 'restore']], src: 'v8 4.0-4.4'});
}
{
  // B1 wing-wrap double (v5 5.8-8.5): wrapped 0-22 (blade low behind), the wings snap open at 22, h1 horizontal at 24, a step in
  // while the blade drops low left, h2 rising diagonal at 40
  const WRAP = {pos: [0, -.12, 0], tor: [-14, 14, 0], head: [-8, -10, 0], ...F_WIDE, ...B(0, 80, -160, 1, {gL: .5}), aL: [40, -10, .75], wW: 1, wS: -.4, hairF: 0};
  C('b1_wrap2', [K(0, ST), K(8, WRAP, 'o'), K(20, {...WRAP, pos: [0, -.15, 0], tor: [-16, 18, 0]}),
    K(22, {wW: .45, wF: .6, wS: 0, ...B(0, 80, -130, 1, {gL: .55}), tor: [-12, 20, 0]}, 'l'),
    K(23, {wW: .1, wF: 1, wS: .2, ...B(0, 80, -95, 1, {gL: .55}), tor: [-10, 20, 0]}, 'l'),
    K(24, {...B(0, 80, -10, 1, {gL: .6}), wW: 0, tor: [-8, 2, 0], head: [-4, 2, 0], ...F_LUNGE, pos: [0, -.18, -.08]}, 'l'),
    K(27, {...B(0, 80, 92, 1, {gL: .55}), tor: [-8, -34, 0], head: [-4, 22, 0], aL: [-30, 60, .95], wF: .6}, 'o'),
    K(33, {...B(0, -50, -150, 1, {gL: .55}), pos: [0, -.26, -.04], tor: [-18, -28, 0], ...F_WIDE, aL: [10, 40, .95], wF: .3}),
    K(37, {...B(0, -50, -120, 1, {gL: .55}), pos: [0, -.3, -.06], tor: [-22, -30, 0]}),
    K(40, {...B(0, -50, 20, 1, {gL: .6}), pos: [0, -.1, -.1], tor: [2, 12, 0], head: [-6, -6, 0], ...F_LUNGE, aL: [-20, 50, .95], wF: .8}, 'l'),
    K(43, {...B(0, -50, 78, 1, {gL: .55}), pos: [0, -.04, -.08], tor: [8, 26, 0], wF: .5}, 'o'), K(50, {...ST, wF: 0})],
    {src: 'v5 5.8-8.5', preview: 'winged'});
}
{
  // B2 side-step four-chain (v5 18-30): lateral hop with the sword vertical behind (0-14), h1 lunge slash 22, raise 30-44
  // (two hands, glow), h2 overhead heavy 44, h3 quick sweep 54, h4 back 64
  const HIDE = {...B(180, 0, 78, -1, {gL: .45}), aL: [30, 45, .95]};
  C('b2_side4', [K(0, ST), K(3, {...CROUCH, ...HIDE, pos: [0, -.2, 0], tor: [-12, 10, 0]}, 'o'),
    K(6, {...HIDE, pos: [0, .12, 0], tor: [-4, 10, -6], fL: [.16, .3, -.1], fR: [-.16, .26, .1], fpL: -25, fpR: -30, wF: .6}, 'o'),
    K(11, {pos: [0, .04, 0], fL: [.2, .16, -.12], fR: [-.2, .14, .14]}), K(14, {...CROUCH, ...HIDE, pos: [0, -.24, 0], tor: [-14, 10, 4], wF: .3}, 'i'),
    K(18, {...B(0, -45, 112, -1, {gL: .5}), tor: [-6, 20, 0], head: [-4, -12, 0], aL: [40, 40, .95]}, 'o'),
    K(22, {...B(0, -45, -38, -1, {gL: .6}), pos: [0, -.2, -.12], tor: [-16, -16, 0], head: [-6, 10, 0], ...F_LUNGE, aL: [-20, 50, .95], wF: .6}, 'i'),
    K(25, {...B(0, -45, -70, -1, {gL: .55}), tor: [-18, -22, 0]}, 'o'),
    K(30, {...F_ST, pos: [0, -.08, -.04], tor: [-4, -6, 0], ...B(0, 0, 40, 1, {gL: .45}), lh: .6, aL: [60, 10, .9], wF: .2}),
    K(36, {...B(0, 0, 118, -1, {gL: .45}), lh: 1, pos: [0, .0, 0], tor: [8, -4, 0], head: [-8, 4, 0], wF: .3, pL: [.9, .1, .2], pR: [.9, .1, .2]}, 'o'),
    K(40, {...B(0, 0, 126, -1, {gL: .45}), lh: 1, tor: [10, -4, 0], pos: [0, .01, 0]}),
    K(42, {...B(0, 0, 70, -1, {gL: .48}), lh: 1, pos: [0, -.12, -.05], tor: [-8, -4, 0]}, 'i'),
    K(44, {...B(0, 0, -30, -1, {gL: .5}), lh: 1, pos: [0, -.26, -.1], tor: [-26, -4, 0], head: [2, 4, 0], ...F_LUNGE, wF: .7}, 'l'),
    K(47, {...B(0, 0, -48, -1, {gL: .5}), lh: 1, pos: [0, -.28, -.1], tor: [-28, -4, 0]}, 'o'),
    K(51, {...B(0, 85, -105, 1, {gL: .55}), lh: 0, pos: [0, -.16, -.04], tor: [-10, 30, 0], head: [-4, -20, 0], ...F_WIDE, aL: [40, 40, .95], wF: .2}),
    K(54, {...B(0, 85, 25, 1, {gL: .58}), tor: [-8, -10, 0], head: [-4, 8, 0]}, 'l'),
    K(57, {...B(0, 85, 105, 1, {gL: .55}), tor: [-8, -36, 0], head: [-4, 22, 0], aL: [-20, 55, .95]}, 'o'),
    K(61, {...B(0, 85, 112, -1, {gL: .55}), tor: [-8, -40, 0]}),
    K(64, {...B(0, 85, -25, -1, {gL: .58}), tor: [-8, 10, 0], head: [-4, -6, 0]}, 'l'),
    K(67, {...B(0, 85, -100, -1, {gL: .55}), tor: [-8, 32, 0], head: [-4, -18, 0], aL: [30, 40, .95]}, 'o'), K(78, {...ST, wF: 0})],
    {looks: [[30, 'edge', 'glint'], [44, 'edge', 'restore']], src: 'v5 18-30'});
}
{
  // B3 charged six-chain (v5 30.4-40, P3): red core charge (0-30), dash-in, wide fire arc 40, backhand 50, 60, raise, three
  // heavy two-handed chops 76 / 88 / 100 (re-aimed: small body turns between)
  const CH = {pos: [0, -.1, 0], tor: [-10, 10, 0], head: [-10, -6, 0], ...F_WIDE, ...B(0, 80, -140, 1, {gL: .55}), aL: [30, 40, .9], wF: .3};
  const chop = (t, yaw) => [K(t - 7, {...B(0, 0, 116, -1, {gL: .45}), lh: 1, pos: [0, -.02, 0], rot: [0, yaw, 0], tor: [8, -4, 0], head: [-8, 4, 0], ...F_ST, wF: .3, pL: [.9, .1, .2], pR: [.9, .1, .2]}, 'o'),
    K(t - 4, {...B(0, 0, 126, -1, {gL: .45}), lh: 1, tor: [10, -4, 0]}),
    K(t - 2, {...B(0, 0, 70, -1, {gL: .48}), lh: 1, pos: [0, -.14, -.05], tor: [-10, -4, 0]}, 'i'),
    K(t, {...B(0, 0, -28, -1, {gL: .5}), lh: 1, pos: [0, -.28, -.1], tor: [-28, -4, 0], ...F_LUNGE, wF: .8}, 'l'),
    K(t + 1, {...B(0, 0, -36, -1, {gL: .5}), lh: 1, pos: [0, -.3, -.1], tor: [-30, -4, 0]}, 'o')];
  C('b3_six', [K(0, ST), K(10, CH, 'o'), K(30, {...CH, pos: [0, -.14, 0], tor: [-12, 14, 0]}),
    K(34, {rot: [-10, 0, 0], pos: [0, -.18, -.1], fL: [.15, .14, -.45], fR: [-.18, .085, .42], fpL: -10, wF: .8}, 'i'),
    K(37, {...B(0, 80, -125, 1, {gL: .55}), tor: [-12, 34, 0], ...F_LUNGE, rot: [-6, 0, 0], pos: [0, -.2, -.12]}),
    K(40, {...B(0, 80, -5, 1, {gL: .62}), tor: [-10, -6, 0], rot: [0, 0, 0], head: [-4, 4, 0]}, 'l'),
    K(43, {...B(0, 80, 100, 1, {gL: .55}), tor: [-8, -38, 0], head: [-4, 22, 0], aL: [-30, 60, .95], wF: .5}, 'o'),
    K(47, {...B(0, 85, 112, -1, {gL: .55}), tor: [-8, -40, 0]}),
    K(50, {...B(0, 85, -15, -1, {gL: .58}), tor: [-8, 8, 0], head: [-4, -4, 0]}, 'l'),
    K(53, {...B(0, 85, -105, -1, {gL: .55}), tor: [-8, 32, 0], head: [-4, -18, 0], aL: [30, 40, .95]}, 'o'),
    K(57, {...B(0, 85, -118, 1, {gL: .55}), tor: [-8, 36, 0]}),
    K(60, {...B(0, 85, 10, 1, {gL: .58}), tor: [-8, -8, 0], head: [-4, 6, 0]}, 'l'),
    K(63, {...B(0, 85, 95, 1, {gL: .55}), tor: [-8, -32, 0], aL: [-20, 50, .95]}, 'o'),
    ...chop(76, -8), ...chop(88, 6), ...chop(100, 0), K(112, {...ST, wF: 0})],
    {looks: [[0, 'chest', 'red'], [0, 'visor', 'abyss'], [30, 'chest', 'restore'], [30, 'visor', 'restore'], [64, 'edge', 'glint'], [76, 'edge', 'restore']],
      src: 'v5 30.4-40', preview: 'abyss'});
}
{
  // C1 combo + blink-strike (v6 14-22): h1 diagonal 14, h2 spin (a full turn 26-36, the blade out to her right), h3 46,
  // h4 big two-handed diagonal 58, glint 68 (the blade drawn back level at the shoulder), thrust 86 (a long lunge)
  const R = 360;
  const GLINT = (yaw) => ({...B(0, 0, 4, -1, {gF: 0, gB: 70, gE: 8, gD: .45}), tw: 90, rot: [0, yaw, 0], pos: [0, -.16, .08], tor: [-8, 34, 0], head: [-4, -30, 0],
    fL: [.16, .085, -.45], fR: [-.2, .085, .38], fyL: 0, fyR: 30, aL: [80, 10, .9], wF: .2});
  const THRUST = (yaw) => ({...B(0, 0, -2, -1, {gF: 0, gB: 4, gE: -2, gD: .82}), tw: 90, rot: [-12, yaw, 0], pos: [0, -.22, -.2], tor: [-14, 10, 0], head: [6, -6, 0],
    ...F_LUNGE, fL: [.16, .085, -.75], aL: [-40, 40, .95], wF: .8});
  C('c1_combo', [K(0, ST), K(8, {...B(0, -45, 118, -1, {gL: .5}), tor: [-4, 22, 0], head: [-4, -14, 0], aL: [40, 40, .95], pos: [0, -.08, 0]}, 'o'),
    K(14, {...B(0, -45, -30, -1, {gL: .6}), pos: [0, -.18, -.1], tor: [-14, -16, 0], head: [-4, 10, 0], ...F_LUNGE, aL: [-20, 50, .95], wF: .5}, 'i'),
    K(17, {...B(0, -45, -62, -1, {gL: .55}), tor: [-16, -20, 0]}, 'o'),
    K(24, {...B(0, 88, -90, 1, {gL: .6}), pos: [0, -.12, 0], rot: [0, 0, 0], tor: [-6, 0, 0], head: [-4, 0, 0], ...F_WIDE, aL: [0, 70, .95], wF: .4}),
    K(26, {rot: [0, 10, 0]}), K(28, {rot: [0, 80, 0], wF: .8}, 'l'), K(30, {rot: [0, 160, 0]}, 'l'), K(32, {rot: [0, 240, 0]}, 'l'), K(34, {rot: [0, 310, 0]}, 'l'),
    K(37, {rot: [0, R, 0], ...B(0, 88, -60, 1, {gL: .6}), wF: .4}, 'o'),
    K(42, {...B(0, 85, 112, -1, {gL: .55}), rot: [0, R, 0], tor: [-8, -36, 0], head: [-4, 22, 0], aL: [-20, 50, .95], wF: .2}),
    K(46, {...B(0, 85, -15, -1, {gL: .58}), tor: [-8, 10, 0], head: [-4, -6, 0], wF: .5}, 'l'),
    K(49, {...B(0, 85, -100, -1, {gL: .55}), tor: [-8, 32, 0], head: [-4, -18, 0], aL: [30, 40, .95], pL: [.8, -.3, .3]}, 'o'),
    K(54, {...B(0, -45, 118, -1, {gL: .45}), lh: 1, pos: [0, -.02, 0], tor: [6, 18, 0], head: [-8, -8, 0], ...F_ST, wF: .3, pL: [.9, .1, .2], pR: [.9, .1, .2]}, 'o'),
    K(56, {...B(0, -45, 60, -1, {gL: .48}), lh: 1, pos: [0, -.14, -.05], tor: [-8, 0, 0]}, 'i'),
    K(58, {...B(0, -45, -35, -1, {gL: .52}), lh: 1, pos: [0, -.26, -.1], tor: [-24, -18, 0], head: [-2, 10, 0], ...F_LUNGE, wF: .8}, 'l'),
    K(61, {...B(0, -45, -58, -1, {gL: .5}), lh: 1, tor: [-26, -22, 0]}, 'o'),
    K(68, {...GLINT(R), lh: 0, pL: [.55, -.35, .75]}, 'io'), K(80, {...GLINT(R), pos: [0, -.2, .1], tor: [-10, 38, 0]}),
    K(86, THRUST(R), 'i'), K(88, {...THRUST(R), pos: [0, -.24, -.22]}), K(92, {...THRUST(R), pos: [0, -.18, -.16], rot: [-6, R, 0], wF: .4}, 'o')],
    {looks: [[68, 'edge', 'glint'], [86, 'edge', 'restore']], src: 'v6 14-22 (h2 = the full fire ring, glint v6 20.2)'});
  // C2 (v7 0-6): h1 12, h2 24, h3 rising 38, glint 50, thrust 68
  C('c2_combo', [K(0, ST), K(6, {...B(0, 85, -112, 1, {gL: .55}), tor: [-8, 30, 0], head: [-4, -18, 0], aL: [30, 40, .95], pos: [0, -.1, 0]}, 'o'),
    K(12, {...B(0, 85, 15, 1, {gL: .58}), tor: [-10, -10, 0], head: [-4, 8, 0], pos: [0, -.16, -.08], ...F_LUNGE, wF: .5}, 'l'),
    K(15, {...B(0, 85, 100, 1, {gL: .55}), tor: [-8, -34, 0], head: [-4, 20, 0], aL: [-20, 50, .95]}, 'o'),
    K(19, {...B(0, 85, 112, -1, {gL: .55}), tor: [-8, -38, 0]}),
    K(24, {...B(0, 85, -20, -1, {gL: .58}), tor: [-8, 10, 0], head: [-4, -6, 0], wF: .5}, 'l'),
    K(27, {...B(0, 85, -100, -1, {gL: .55}), tor: [-8, 30, 0], head: [-4, -16, 0], aL: [30, 40, .95]}, 'o'),
    K(33, {...B(0, 45, -140, 1, {gL: .55}), pos: [0, -.26, -.04], tor: [-20, 26, 0], ...F_WIDE, wF: .3}),
    K(38, {...B(0, 45, 25, 1, {gL: .6}), pos: [0, -.1, -.1], tor: [0, -8, 0], head: [-6, 4, 0], ...F_LUNGE, aL: [-20, 50, .95], wF: .7}, 'l'),
    K(41, {...B(0, 45, 80, 1, {gL: .55}), pos: [0, -.04, -.08], tor: [6, -20, 0]}, 'o'),
    K(50, {...GLINT(0), lh: 0}, 'io'), K(62, {...GLINT(0), pos: [0, -.2, .1], tor: [-10, 38, 0]}),
    K(68, THRUST(0), 'i'), K(70, {...THRUST(0), pos: [0, -.24, -.22]}), K(74, {...THRUST(0), pos: [0, -.18, -.16], rot: [-6, 0, 0], wF: .4}, 'o')],
    {looks: [[50, 'edge', 'glint'], [68, 'edge', 'restore']], src: 'v7 0-6', preview: 'winged'});
  // C3 (v7 9.6-15, P3): red core flare 0-22, h1 22, h2 32, h3 44, a flourish 44-60, h4 60, h5 70, glint 80, thrust 98
  C('c3_combo', [K(0, ST), K(8, {pos: [0, -.06, 0], tor: [6, -6, 0], head: [6, 4, 0], aL: [20, 50, .9], ...B(20, 0, -40, -1, {gL: .55}), wF: .6}, 'o'),
    K(18, {...B(0, -45, 112, -1, {gL: .5}), pos: [0, -.1, 0], tor: [-6, 22, 0], head: [-4, -14, 0], aL: [40, 40, .95]}),
    K(22, {...B(0, -45, -30, -1, {gL: .6}), pos: [0, -.18, -.1], tor: [-14, -16, 0], ...F_LUNGE, aL: [-20, 50, .95], wF: .5}, 'i'),
    K(25, {...B(0, -45, -66, -1, {gL: .55}), tor: [-16, -20, 0]}, 'o'),
    K(28, {...B(0, 45, -150, -1, {gL: .55}), pos: [0, -.22, -.06], tor: [-16, -20, 0], ...F_WIDE}),
    K(32, {...B(0, 45, 30, 1, {gL: .6}), pos: [0, -.08, -.08], tor: [0, 10, 0], head: [-4, -6, 0]}, 'l'),
    K(36, {...B(0, 85, 112, -1, {gL: .55}), tor: [-6, -30, 0], head: [-4, 18, 0]}, 'o'),
    K(44, {...B(0, 85, -20, -1, {gL: .58}), tor: [-8, 10, 0], head: [-4, -6, 0], ...F_LUNGE, pos: [0, -.18, -.08], wF: .5}, 'l'),
    K(48, {...B(0, 85, -95, -1, {gL: .55}), tor: [-8, 30, 0], aL: [30, 40, .95]}, 'o'),
    K(54, {...B(0, 0, 120, 1, {gL: .5}), pos: [0, -.04, 0], tor: [4, -10, 0], head: [-6, 6, 0], ...F_WIDE, aL: [90, 60, .9], wF: .6}, 'o'),
    K(56, {...B(0, -45, 125, -1, {gL: .5})}),
    K(60, {...B(0, -45, -32, -1, {gL: .6}), pos: [0, -.2, -.1], tor: [-16, -16, 0], ...F_LUNGE, aL: [-20, 50, .95], wF: .5}, 'i'),
    K(65, {...B(0, 85, -112, 1, {gL: .55}), tor: [-8, 30, 0], ...F_WIDE, pos: [0, -.14, 0]}),
    K(70, {...B(0, 85, 20, 1, {gL: .6}), tor: [-10, -10, 0], ...F_LUNGE, pos: [0, -.18, -.1], wF: .6}, 'l'),
    K(73, {...B(0, 85, 98, 1, {gL: .55}), tor: [-8, -34, 0], aL: [-20, 50, .95]}, 'o'),
    K(80, {...GLINT(0), lh: 0}, 'io'), K(92, {...GLINT(0), pos: [0, -.2, .1], tor: [-10, 38, 0]}),
    K(98, THRUST(0), 'i'), K(100, {...THRUST(0), pos: [0, -.24, -.22]}), K(104, {...THRUST(0), pos: [0, -.18, -.16], rot: [-6, 0, 0], wF: .4}, 'o')],
    {looks: [[0, 'chest', 'red'], [0, 'visor', 'abyss'], [22, 'chest', 'restore'], [22, 'visor', 'restore'], [80, 'edge', 'glint'], [98, 'edge', 'restore']],
      src: 'v7 9.6-15 (red core flash v7 9.6)', preview: 'abyss'});
}

// ---- aerial / ranged patterns (S4) -------------------------------------------------------------------------------------------------
{
  // K blink ambush (v4 29.6-40, v6 0-6): hold low with the wings spread, glint, thrust; leap; sky plunge
  const KH = {...ST, pos: [0, -.2, 0], tor: [-16, 18, 0], head: [-8, -12, 0], ...F_WIDE, ...B(0, 80, -150, 1, {gL: .55}), aL: [30, 50, .9], wS: .2, wF: .3, wFl: 6};
  C('k_hold', [K(0, KH), K(10, {pos: [0, -.22, 0], tor: [-17, 19, 0], wF: .35}), K(20, KH)], {src: 'v4 36.4-39.6 (waits, blade low and glowing)', preview: 'winged'});
  const KG = {...KH, ...B(0, 0, 4, -1, {gF: 0, gB: 70, gE: 8, gD: .45}), tw: 90, pos: [0, -.18, .08], tor: [-8, 34, 0], head: [-4, -30, 0], fL: [.16, .085, -.45], fR: [-.2, .085, .38], fyL: 0, fyR: 30, aL: [80, 10, .9]};
  C('k_glint', [K(0, KH), K(6, KG, 'o'), K(12, {...KG, pos: [0, -.2, .12], tor: [-10, 38, 0]}),
    K(16, {...B(0, 0, -2, -1, {gF: 0, gB: 4, gE: -2, gD: .82}), tw: 90, rot: [-12, 0, 0], pos: [0, -.22, -.2], tor: [-14, 10, 0], head: [6, -6, 0], ...F_LUNGE, fL: [.16, .085, -.75], aL: [-40, 40, .95], wF: .8}, 'i'),
    K(18, {pos: [0, -.22, -.2]})], {looks: [[0, 'edge', 'glint'], [16, 'edge', 'restore']], src: 'v4 32.0 (glint), v6 0-6', preview: 'winged'});
  const KUP = {...ST, ...AIR, pos: [0, .05, 0], tor: [4, 0, 0], head: [-14, 0, 0], ...B(0, 0, 100, 1, {gF: 0, gB: 10, gE: 70, gD: .5}), lh: 1, wS: .28, wF: .8, wFl: 18, fL: [.14, .45, -.15], fR: [-.14, .4, .12]};
  C('k_leap', [K(0, KH), K(6, {...LOW, ...B(0, 80, -150, 1, {gL: .55}), wF: .5}, 'o'), K(8, {pos: [0, .08, 0], tor: [4, 0, 0], fL: [.12, .085, -.04], fR: [-.12, .085, .08], fpL: -35, fpR: -35, wF: .9}, 'i'),
    K(14, KUP, 'io')], {src: 'v4 33.0 (leaps to the sky)', preview: 'winged'});
  const PL = {...KUP, ...B(0, 0, -88, -1, {gF: 0, gB: 0, gE: 62, gD: .45}), lh: 1, tor: [-4, 0, 0], head: [-30, 0, 0], wS: .1, wF: .5};
  C('k_plunge', [K(0, KUP), K(6, PL, 'o'), K(12, {...PL, rot: [-10, 0, 0], wS: -.45, wF: .2, fL: [.14, .3, .1], fR: [-.14, .3, .14]}),
    K(16, {...IMPACT, ...B(0, 0, -88, -1, {gF: 0, gB: 0, gE: -40, gD: .55}), lh: 1, pos: [0, -.42, -.04], tor: [-34, 0, 0]}, 'i'),
    K(20, {pos: [0, -.38, -.04], tor: [-30, 0, 0]})], {src: 'v4 33.3-33.9 (sky arcs), 34 (plunge)', preview: 'winged'});
}
{
  // W1 ground crescents (v3 9.6-28): planted, the blade level to her right charging (0-40), three horizontal releases
  const PLANT = {...ST, pos: [0, -.16, 0], tor: [-6, 34, 0], head: [-6, -30, 0], ...F_WIDE, ...B(0, 88, -115, 1, {gL: .6}), aL: [70, 40, .9], wF: .3};
  C('w1_wave', [K(0, ST), K(6, PLANT, 'o'), K(30, {...PLANT, pos: [0, -.2, 0], tor: [-8, 38, 0], wF: .4}), K(40, {...PLANT, pos: [0, -.22, 0], tor: [-8, 40, 0], ...B(0, 88, -125, 1, {gL: .6})}),
    K(46, {...B(0, 88, 15, 1, {gL: .62}), tor: [-8, -8, 0], head: [-4, 6, 0], ...F_LUNGE, pos: [0, -.2, -.1], aL: [-20, 60, .95], wF: .7}, 'i'),
    K(49, {...B(0, 88, 100, 1, {gL: .55}), tor: [-8, -36, 0], head: [-4, 20, 0]}, 'o'),
    K(53, {...B(0, 88, 115, -1, {gL: .55}), tor: [-8, -40, 0]}),
    K(58, {...B(0, 88, -15, -1, {gL: .62}), tor: [-8, 8, 0], head: [-4, -6, 0], wF: .7}, 'i'),
    K(61, {...B(0, 88, -100, -1, {gL: .55}), tor: [-8, 34, 0], head: [-4, -20, 0], aL: [40, 40, .95]}, 'o'),
    K(65, {...B(0, 88, -118, 1, {gL: .55}), tor: [-8, 38, 0]}),
    K(70, {...B(0, 88, 15, 1, {gL: .62}), tor: [-8, -8, 0], head: [-4, 6, 0], wF: .7}, 'i'),
    K(73, {...B(0, 88, 98, 1, {gL: .55}), tor: [-8, -34, 0], aL: [-20, 60, .95]}, 'o'), K(88, {...ST, wF: 0})],
    {looks: [[6, 'edge', 'yellow'], [46, 'edge', 'restore']], src: 'v3 9.6-28 (charge v3 19.4, crescents v3 13.6)'});
  // W2 air crescents + dive (v3 29-35, v4 0-3.2): three vertical slashes in the air, pull back, then the dive slash
  const AIRC = (t, roll) => [K(t - 6, {...HOV, ...B(0, roll, 120, -1, {gL: .45}), lh: .5, tor: [6, -4, 0], head: [-10, 0, 0], wFl: 14}, 'o'),
    K(t, {...HOV, ...B(0, roll, -55, -1, {gL: .55}), lh: 0, tor: [-16, 6, 0], head: [-14, 0, 0], wF: .6, wFl: 10}, 'i'),
    K(t + 3, {...B(0, roll, -75, -1, {gL: .5}), tor: [-18, 6, 0]}, 'o')];
  C('w2_air', [K(0, HOV), ...AIRC(14, -30), ...AIRC(28, 30), ...AIRC(42, -20),
    K(52, {...HOV, ...B(0, 80, -150, 1, {gL: .55}), tor: [-10, 30, 0], head: [-10, -24, 0], wS: .28, wF: 1, wFl: 4, fL: [.14, .45, -.2], fR: [-.14, .4, .1]}, 'o'),
    K(66, {...HOV, ...B(0, 80, -158, 1, {gL: .55}), tor: [-12, 34, 0], head: [-10, -28, 0], wS: .28, wF: 1, wFl: 0, rot: [-10, 0, 0], fL: [.14, .45, -.2], fR: [-.14, .4, .1]})],
    {src: 'v3 29-35 (air crescents), v4 0-1 (pull)', preview: 'winged'});
  C('w2_dive', [K(0, {...HOV, ...B(0, 80, -158, 1, {gL: .55}), tor: [-12, 34, 0], wS: .28, wF: 1, wFl: 0, rot: [-10, 0, 0], fL: [.14, .45, -.2], fR: [-.14, .4, .1]}),
    K(3, {wS: .02, wF: .7, rot: [-22, 0, 0]}),
    K(5, {rot: [-36, 0, 0], tor: [-8, 36, 0], wS: -.3, wF: .4, fL: [.12, .3, .26], fR: [-.12, .26, .3], fpL: -45, fpR: -45}, 'i'),
    K(8, {...B(0, 80, -110, 1, {gL: .55}), rot: [-20, 0, 0], tor: [-10, 34, 0]}),
    K(10, {...B(0, 80, 5, 1, {gL: .62}), rot: [-6, 0, 0], tor: [-10, -6, 0], ...F_LUNGE, pos: [0, -.24, -.1], wS: .1, wF: .8}, 'l'),
    K(13, {...B(0, 80, 100, 1, {gL: .55}), rot: [0, 0, 0], tor: [-10, -36, 0], aL: [-20, 60, .95]}, 'o'), K(16, {pos: [0, -.22, -.08], tor: [-10, -30, 0], wF: .4})],
    {src: 'v4 1.2-3.2 (dive fire arc)', preview: 'winged'});
  // L sky landing: the shock after the dive (v4 13.9): crouched over the planted blade, the burst at 10
  const PLANTED = {...IMPACT, ...B(0, 0, -88, -1, {gF: 0, gB: 0, gE: -36, gD: .55}), lh: 1, pos: [0, -.42, -.04], tor: [-32, 0, 0], head: [-6, 0, 0], wS: .1, wF: .4};
  C('l_shock', [K(0, PLANTED), K(8, {...PLANTED, pos: [0, -.46, -.04], tor: [-36, 0, 0], wF: .2}, 'io'), K(10, {pos: [0, -.3, -.04], tor: [-20, 0, 0], head: [-14, 0, 0], wS: .28, wF: 1}, 'o'),
    K(14, {pos: [0, -.32, -.04], tor: [-24, 0, 0]}), K(20, {...ST, wF: .2})], {src: 'v4 13.5-14.5 (lightning shockwave)', preview: 'winged'});
}

// ---- the mantle (G2) -------------------------------------------------------------------------------------------------------------------
{
  const COC = {...ST, pos: [0, -.12, 0], tor: [-18, 0, 0], head: [-26, 0, 0], ...F_TOG, ...B(0, 0, 82, -1, {gF: 0, gB: 0, gE: -20, gD: .3}), lh: 1, aL: [70, -20, .7],
    wW: 1, wS: -.4, wF: 0, hairF: .4};
  const UP = {...COC, pos: [0, .3, 0], fL: [.09, .3, -.04], fR: [-.09, .28, .06], fpL: -50, fpR: -50};
  C('mantle_in', [K(0, ST), K(12, COC, 'o'), K(20, UP, 'o'), K(24, {pos: [0, .34, 0]})], {src: 'v7 / v10 wings fold into a cocoon (G2 mantle)'});
  C('mantle_hold', [K(0, {...UP, pos: [0, .34, 0]}), K(20, {pos: [0, .39, 0], tor: [-19, 0, 0]}), K(40, {...UP, pos: [0, .34, 0]})], {src: 'cocooned, floating'});
  C('mantle_break', [K(0, {...UP, pos: [0, .34, 0]}), K(3, {pos: [0, .4, 0], tor: [6, 0, 0], head: [10, 0, 0], wW: .7, wF: .5}, 'o'), K(16, {wW: .3, wF: .2, pos: [0, .3, 0]}),
    K(20, {...KNEEL, ...B(30, 0, -78, -1, {gF: 0, gB: 55, gE: -66, gD: .62}), lh: 0, wW: 0, wS: 0, wF: .1, hairF: .3}, 'i'), K(26, {pos: [0, -.53, .02]}), K(40, {pos: [0, -.5, .02]})],
    {src: 'mantle broken: drops to a knee (stun follows)'});
  C('mantle_nova', [K(0, {...UP, pos: [0, .34, 0]}), K(20, {wW: .6, wF: .3, tor: [-6, 0, 0], head: [-10, 0, 0], aL: [40, 50, .8]}),
    K(38, {wW: 0, wS: .28, wF: 1, tor: [12, 0, 0], head: [10, 0, 0], aL: [10, 110, .95], ...B(0, 0, 60, -1, {gF: 0, gB: 60, gE: 10, gD: .6}), lh: 0, pos: [0, .42, 0]}, 'io'),
    K(40, {tor: [16, 0, 0], pos: [0, .44, 0]}, 'o'), K(44, {tor: [14, 0, 0], pos: [0, .4, 0]})],
    {looks: [[0, 'chest', 'gold'], [44, 'chest', 'restore']], src: 'nova: the wings swell open, white-gold flash'});
}

// ---- sequences: intro (PLAN §3, v1 + v2), T1 wing unfurl (v9 2.7-4.8), T2 abyss (v10 3.6-6.4), death (v11 32-39) ----------------
{
  // E0 hang: limp in the cables 7 b up, head down, the helmet pushed back as a hood, the sword sheathed across the lower back
  const HANG = {...ST, hold: 0, drawn: 0, scab: 'full', hL: 'open', hR: 'open', helm: -100, hairF: 1, pos: [0, 6.7, .05], rot: [-8, 0, 2], tor: [-16, 0, 4], head: [-46, 6, 8],
    aL: [-8, 26, .97], aR: [-4, 24, .97], fL: [.1, 6.86, .06], fR: [-.11, 6.82, .1], fpL: -55, fpR: -60, fyL: 4, fyR: 4, kL: [.1, 0, -1], kR: [-.1, 0, -1], wF: 0, wS: 0};
  // E2 prone on the floor, face down (v1 15-19, v2 1.6), the cape over the legs as a train
  const PRONE = {pos: [0, -.86, .1], rot: [-86, 0, 3], tor: [-2, 0, 0], head: [24, 16, 0], aL: [150, 30, .92], aR: [130, 34, .92],
    fL: [.13, .1, .86], fR: [-.15, .1, .9], fpL: -75, fpR: -75, fyL: 0, fyR: 0, kL: [.15, -.3, -1], kR: [-.15, -.3, -1], hairF: .5};
  // E3 onto hands and knees, head hanging (v2 1.6-4.0, intro_v2_rise.jpg)
  const CRAWL = {pos: [0, -.5, .1], rot: [-60, 0, 0], tor: [-22, 0, 0], head: [-34, 0, 0], plL: [.22, .06, -.62], plR: [-.22, .06, -.6], plwL: 1, plwR: 1,
    fL: [.14, .1, .52], fR: [-.15, .1, .55], fpL: -65, fpR: -65, kL: [.15, -1, -.3], kR: [-.15, -1, -.3], hairF: 1};
  const SQUAT = {pos: [0, -.46, .02], rot: [-16, 0, 0], tor: [-34, 0, 0], head: [-36, -6, 0], ...F_WIDE, fpL: 0, fpR: 0, plwL: .4, plwR: .4, plL: [.24, .06, -.4], plR: [-.24, .06, -.38],
    kL: [.15, 0, -1], kR: [-.15, 0, -1], aL: [10, 18, .95], aR: [12, 18, .95]};
  const UPB = {pos: [0, -.04, 0], rot: [0, 0, 0], tor: [-10, -4, 0], head: [-36, -14, 0], ...F_ST, plwL: 0, plwR: 0, aL: [-4, 14, .97], aR: [4, 16, .97], hairF: 1, wF: 0};
  // E9 the draw: the right hand at the hilt behind the right hip, then the blade out behind her and low to the right
  const GRAB = {plR: [-.36, 1.02, .22], plwR: 1, tor: [-4, 16, 0], head: [-6, -10, 0], aL: [10, 30, .95]};
  const DRAWN0 = {hold: 1, drawn: 1, scab: 'empty', plwR: 0, gF: 0, gB: 118, gE: -48, gD: .6, cB: 0, cR: 80, th: 90, ed: 1};
  C('intro', [
    K(0, HANG), K(15, {rot: [-7, 0, -1.5], head: [-44, 4, 6]}), K(29, {rot: [-8, 0, 2], head: [-46, 6, 8]}),
    K(30, {pos: [0, 6.55, .05], rot: [-18, 0, 4], head: [-40, 8, 10], aL: [10, 40, .97], fL: [.1, 6.7, .1]}, 'i'),
    K(33, {pos: [0, 6.3, .06], rot: [-40, 0, -4], tor: [-20, 0, -6], head: [-30, -6, -6], aR: [20, 50, .97], fL: [.1, 6.45, .2], fR: [-.11, 6.4, .25]}, 'i'),
    K(36, {pos: [0, 6.05, .08], rot: [-52, 0, 3], tor: [-14, 0, 2], head: [-20, 10, 4], aL: [40, 60, .97], aR: [50, 55, .97], fL: [.12, 6.2, .4], fR: [-.13, 6.15, .45]}, 'i'),
    K(42, {...PRONE, pos: [0, -.86, .1]}, 'i'), K(44, {...PRONE, pos: [0, -.84, .1], head: [26, 18, 0]}, 'o'),
    K(52, {...PRONE, tor: [0, 0, 0]}), K(60, {...PRONE, tor: [-2, 0, 0], aL: [90, 40, .7], aR: [80, 40, .7]}),
    K(66, {pos: [0, -.72, .1], rot: [-80, 0, 0], tor: [-10, 0, 0], head: [-10, 0, 0], plL: [.22, .06, -.6], plR: [-.22, .06, -.58], plwL: 1, plwR: 1}, 'io'),
    K(74, {pos: [0, -.58, .1], rot: [-70, 0, 0], tor: [-18, 0, 0], head: [-26, 0, 0], fL: [.14, .1, .62], fR: [-.15, .1, .66], kL: [.15, -1, -.3], kR: [-.15, -1, -.3], hairF: 1}),
    K(84, CRAWL, 'o'),
    K(92, SQUAT, 'io'), K(100, {pos: [0, -.24, 0], rot: [-6, 0, 0], tor: [-24, -2, 0], head: [-38, -10, 0], plwL: 0, plwR: 0, ...F_ST, fpL: 0, fpR: 0}),
    K(108, UPB, 'o'),
    K(112, {wF: 1, head: [-24, -6, 0], tor: [-6, -4, 0], hairF: .7}, 'o'), K(116, {wF: .6, head: [-14, 0, 0], tor: [-4, -2, 0], hairF: .4, pR: [.9, .1, .4]}),
    K(119, {plR: [-.16, 2.02, -.1], plwR: 1, pR: [.9, .3, .2], head: [-8, 4, 4], hairF: .2, wF: .3}, 'o'), K(123, {plR: [-.1, 2.18, .16], plwR: 1, pR: [1, .6, -.2], hairS: 1, head: [2, 2, 2]}),
    K(125, {plR: [-.45, 1.65, .05], pR: [1, .2, .2]}),
    K(127, {plwR: 0, pR: [.55, -.35, .75], hairS: .4, head: [0, 0, 0], tor: [-2, -2, 0], wF: .1}, 'o'),
    K(130, {helm: -60, hairS: 0}, 'i'), K(134, {helm: 0, head: [-4, 0, 0]}, 'i'), K(136, {head: [-2, 0, 0], hairF: 0}),
    K(142, {tor: [-2, -4, 0], head: [-2, 0, 0]}),
    K(146, {...GRAB}, 'io'),
    K(147, {...DRAWN0, tor: [-4, 18, 0], head: [-6, -12, 0]}),
    K(150, {...DRAWN0, gB: 100, gE: -40, gD: .62, th: 190, tor: [-6, 10, 0]}, 'l'),
    K(154, {...DRAWN0, gB: 72, gE: -32, gD: .62, th: 300, tor: [-8, -14, 0], head: [-4, 10, 0], pos: [0, -.1, 0], ...F_WIDE, aL: [20, 36, .95]}, 'o'),
    K(158, {gB: 45, gE: -8, gD: .58, cB: 0, cR: 30, th: 395, tor: [-4, -6, 0], head: [-2, 6, 0], pos: [0, -.06, 0]}, 'io'),
    K(162, {gB: 32, gE: 4, gD: .62, cB: 20, cR: 0, th: 440, tor: [0, -8, 0], head: [0, 6, 0], aL: [10, 30, .95], ...F_ST}, 'o'),
    K(170, {gB: 32, gE: 6, gD: .62, cB: 20, cR: 0, th: 436}),
    K(184, {...ST, th: 326}, 'io')],
  {lookStart: {visor: 'up_off', edge: 'off', chest: 'off'}, cableSnaps: {30: [0, 3], 33: [1, 4], 36: [2, 5]},
    looks: [[0, 'visor', 'set:visor/up_off'], [0, 'edge', 'set:edge/off'], [0, 'chest', 'set:chest/off'], [48, 'chest', 'amber'], [51, 'chest', 'restore'],
      [56, 'chest', 'amber'], [59, 'chest', 'restore'], [136, 'visor', 'set:visor/down_pyro'], [136, 'chest', 'set:chest/amber'], [147, 'edge', 'set:edge/yellow'],
      [156, 'edge', 'set:edge/pyro']],
    src: 'v1 0-5 / 13-19 (hang, prone), v2 1.6-16.5 (push up, rise, cape, hair, visor, skull, draw, ignite)'});
}
{
  const KN = {...ST, ...KNEEL, pos: [0, -.36, .02], tor: [-22, -4, 0], ...B(30, 0, -60, -1, {gF: 0, gB: 50, gE: -60, gD: .6}), lh: 0, wF: 0};
  C('t1_wings', [K(0, ST), K(8, KN, 'io'), K(10, {...KN, wS: -.95, wF: 0, wW: 0}), K(14, {wS: -.85, tor: [-24, -4, 0]}),
    K(30, {wS: .05, wF: .3, pos: [0, -.4, .02], tor: [-10, 0, 0], head: [-10, 0, 0], aL: [30, 50, .9]}, 'o'),
    K(46, {wS: .05, wF: .7, pos: [0, -.36, .02], tor: [6, 0, 0], head: [6, 0, 0], aL: [10, 80, .95]}),
    K(50, {wF: 1, tor: [12, 0, 0], head: [10, 0, 0]}, 'o'), K(58, {wF: .6, tor: [4, 0, 0]}),
    K(70, {...ST, pos: [0, -.12, 0], tor: [-6, -4, 0], wF: .3}, 'io'), K(80, {...ST, wF: 0})],
    {formAt: {10: 'winged'}, swapAt: {10: 'winged'}, looks: [[46, 'chest', 'gold'], [58, 'chest', 'restore']], src: 'v9 0-4.8 (kneels, the cape splits into the blade-feather wings)'});
  C('t2_abyss', [K(0, ST), K(4, {pos: [0, -.14, .12], tor: [10, -14, 8], head: [16, 10, 10], ...F_WIDE, aL: [30, 50, .95], wF: .5}, 'o'),
    K(12, {pos: [0, -.26, .08], tor: [-24, -8, 4], head: [-20, 8, 6], ...B(30, 0, -60, -1, {gF: 0, gB: 45, gE: -58, gD: .55}), wF: .2}),
    K(20, {tor: [-10, 0, 0], head: [6, 0, 0], pos: [0, -.2, .06], aL: [20, 40, .9], wF: .5}, 'o'),
    K(36, {tor: [-30, 0, 0], head: [-30, 0, 0], pos: [0, -.3, .06], tdS: 0, wS: -.4, wF: .2}),
    K(46, {tdS: 1, tor: [-20, 0, 6], head: [-14, 0, 0], wF: .4}, 'o'),
    K(50, {tor: [-34, 0, 0], head: [-34, 0, 0], pos: [0, -.34, .06], wS: -.5, wF: .1, hairF: .5}),
    K(76, {tor: [-30, 0, -4], head: [-30, 0, 0], pos: [0, -.32, .06]}),
    K(90, {...ST, pos: [0, -.04, 0], tor: [8, -4, 0], head: [6, 4, 0], wS: .28, wF: 1, aL: [10, 70, .95], hairF: 0}, 'o'),
    K(100, {wF: .5, tor: [-2, -6, 0]}), K(110, {...ST, wF: 0})],
    {formAt: {36: 'abyss'}, swapAt: {60: 'abyss'}, looks: [[20, 'visor', 'abyss'], [90, 'visor', 'restore']], src: 'v10 3.6-6.4 (stagger, red flare, tendrils, darkness)', formBefore: 'winged'});
  const PLANT = {...ST, ...KNEEL, ...B(0, 0, -88, -1, {gF: 0, gB: 0, gE: -30, gD: .62}), lh: 1, tor: [-30, 0, 0], head: [-20, 0, 0], wF: .1};
  C('death', [K(0, ST), K(6, {pos: [0, -.18, .1], tor: [8, -10, 6], head: [14, 8, 8], aL: [30, 40, .95], wF: .5}, 'o'),
    K(20, {...ST, ...KNEEL, ...B(30, 0, -80, -1, {gF: 0, gB: 52, gE: -60, gD: .6}), lh: 0, wF: .2}, 'io'),
    K(36, PLANT, 'io'), K(50, {...PLANT, tor: [-36, 0, 2], head: [-34, 0, 0], pos: [0, -.53, .02]}),
    K(70, {wS: -.5, wF: 0, tor: [-40, 0, 4], head: [-40, 0, 4], hairF: .5}),
    K(88, {wS: -.62, pos: [0, -.56, 0], tor: [-46, 0, 6], head: [-44, 0, 6], pR: [.6, -.6, .3]}),
    K(94, {pos: [0, -.7, -.06], rot: [-40, 0, 5], tor: [-30, 0, 4], pR: [.7, -.5, .5], pL: [.8, -.4, .3], kL: [.15, -1, -.3], kR: [-.15, -1, -.3]}),
    K(100, {pos: [0, -.86, -.12], rot: [-80, 0, 8], pR: [.7, -.5, .5], pL: [.8, -.4, .3], tor: [-6, 0, 4], head: [20, 20, 0], ...B(0, 85, -20, 1, {gF: 0, gB: 40, gE: -40, gD: .6}), lh: 0,
      fL: [.13, .1, .8], fR: [-.15, .1, .84], fpL: -70, fpR: -70, kL: [.15, -1, -.3], kR: [-.15, -1, -.3], aL: [130, 40, .9], hairF: .6}, 'i'),
    K(104, {pos: [0, -.88, -.12]}, 'o'), K(116, {vis: 1}), K(130, {vis: 0}, 'i')],
    {looks: [[50, 'visor', 'set:visor/down_off'], [50, 'chest', 'set:chest/off'], [70, 'edge', 'set:edge/off']], src: 'v11 32-39, v10 4-6'});
}
// ---- export -------------------------------------------------------------------------------------------------------------------
export const CLIPS = clips;
export const CLIP_BY_NAME = Object.fromEntries(clips.map(c => [c.name, c]));
export const accumulate = c => accumulateLib(c, DEFAULT_POSE);
export const sampleClip = (c, t, ks) => sampleLib(c, t, ks, {defaults: DEFAULT_POSE, discrete: DISCRETE,
  phase: (cl, x) => (cl.loop ? x / cl.len : x / 40) % 1});
export const restPose = () => ({...structuredClone(DEFAULT_POSE), ph: 0});
void V;
