// The clips of the 홍련 (Scarlet) rig (S:hr/PLAN.md §2.5, §4.3-4.5, §7.3.2; contract tools/mboss_scarlet/api.py CLIPS:
// names, lengths, loops and event ticks are frozen, this file only authors the motion). S2a authors the 39 fight /
// gauntlet / event clips here (api.CLIP_OWNER 'S2a'); the 8 cinematic clips belong to S2b's tools/scarlet_cine.mjs, and
// until it exists build_scarlet_rig.mjs uses CINE_PLACEHOLDER below (static poses with the contract lengths / events).
// Format and sampling: mboss_rig_clips.mjs (keys [tick, sparse pose, ease] merged onto DEFAULT_POSE; ease of the segment
// arriving at a key: 'io' smooth, 'i' accelerate into the key (strikes, falls), 'o' decelerate (leaps, settles), 'l'
// linear (spins)). Pose channels: scarlet_pose.mjs. Clip ticks are played ticks; the module schedules its hits on the
// events. Root motion is never in a clip (the module / sequence moves the body); a clip only poses her about the anchor.
//
// Per clip (beyond keys): cuts (ticks where every part takes a 1-tick key), src (the footage the motion follows), note.
import {accumulate as accumulateLib, sampleClip as sampleLib} from './mboss_rig_clips.mjs';

// ---- default pose: the fight stance (model.md §3: upright, hat on, the blade low at her left side pointing down and
// across her front; left-handed: the sword in the left hand, the scabbard at the right hip) ---------------------------------
export const DEFAULT_POSE = {
  pos: [0, -.04, 0], rot: [0, 0, 0], tor: [-4, 6, 0], head: [-4, -4, 0],
  fL: [.13, .1, -.12], fR: [-.14, .1, .1], kL: [.12, 0, -1], kR: [-.12, 0, -1], lf: 0,
  hold: 1, gB: -32, gE: -50, gD: .6, gF: 0, gL: .5, cB: 38, cR: 0, th: -40, ed: -1, tw: 0, rh: 0,
  aL: [0, 8, .97], aR: [6, 10, .96], plL: [.3, .1, -.4], plR: [-.3, .1, -.4], plwL: 0, plwR: 0,
  pL: [.55, -.35, .75], pR: [.55, -.35, .75], frL: 0, frR: 0, bwL: 0, bwR: 0, bzL: 35, bzR: 35, hiL: 0, hsR: 0, scHip: [0, 0],
  hairF: 0, hairS: 0, vis: 1, sh: 0, shW: 0, skF: 1, skG: 0, skIF: 0, skIB: 0,
  hwP: [.95, .02, -.35], hwE: [0, 0, 0], hhB: 0, hhE: -90, hhN: [90, 0], scB: 0, scE: 80, scR: 0, scOff: 0, skW: 0,
  cupP: [.32, .46, -.18], botP: [-.3, .46, -.16], cupT: 0, botT: 0,
  hat: 'worn', sword: 'hand', scab: 'hip', face: 'calm', hL: 'grip', hR: 'open', cup: 'none', bottle: 'none',
};
export const DISCRETE = ['hat', 'sword', 'scab', 'face', 'hL', 'hR', 'cup', 'bottle'];
export const K = (t, pose, ease = 'io') => [t, pose, ease];
const DEG = Math.PI / 180;
// the blade: plane bearing cB, roll cR (0 vertical through the bearing, 90 horizontal: th + toward her left; -45 = the plane's
// up tilted to her right: high-right <-> low-left diagonals; +45 high-left <-> low-right), angle th in the plane (vertical:
// 0 forward, 90 up, 180 back), edge leading toward +th (ed 1) or -th (ed -1). Grip: gF 1 = on the lever gL from her LEFT
// shoulder along the blade (one hand; the chest centre with rh 1)
export const B = (cB, cR, th, ed, x = {}) => ({cB, cR, th, ed, gF: 1, ...x});
// a flat sweep: the blade at bearing b (+ = her right) d deg below the horizontal, its edge leading a sweep toward her left
// (dir -1) or her right (dir 1); the hand on the swing sphere (gF 0) at bearing hb, elevation he, distance hd (waist-level
// cuts; the B lever from the shoulder puts flat blades at shoulder height)
export const SW = (b, d, dir, hb, he, hd, x = {}) => ({cB: b, cR: 0, th: -d, ed: 1, tw: dir < 0 ? 90 : -90, gF: 0, gB: hb, gE: he, gD: hd, ...x});
// feet
export const F_ST = {fL: [.13, .1, -.12], fR: [-.14, .1, .1]};
export const F_WIDE = {fL: [.25, .1, -.2], fR: [-.25, .1, .24]};
export const F_LUNGE = {fL: [.16, .1, -.58], fR: [-.17, .1, .46]};      // left foot forward (her sword side leads)
export const F_LUNGE_R = {fL: [.17, .1, .44], fR: [-.15, .1, -.55]};    // right foot forward
export const F_TOG = {fL: [.1, .1, -.03], fR: [-.1, .1, .04]};
// the stance (= DEFAULT_POSE's body) and the low / crouched / airborne families
export const ST = {pos: [0, -.04, 0], rot: [0, 0, 0], tor: [-4, 6, 0], head: [-4, -4, 0], ...F_ST, kL: [.12, 0, -1], kR: [-.12, 0, -1], lf: 0,
  hold: 1, gB: -32, gE: -50, gD: .6, gF: 0, gL: .5, cB: 38, cR: 0, th: -40, ed: -1, tw: 0, rh: 0, aL: [0, 8, .97], aR: [6, 10, .96],
  pL: [.55, -.35, .75], pR: [.55, -.35, .75], frL: 0, frR: 0, bwL: 0, bwR: 0, hiL: 0, hsR: 0, scHip: [0, 0], plwL: 0, plwR: 0, hairF: 0, hairS: 0, vis: 1, sh: 0, shW: 0,
  skF: 1, skG: 0, hat: 'worn', sword: 'hand', scab: 'hip', face: 'calm', hL: 'grip', hR: 'open'};
export const CROUCH = {pos: [0, -.24, 0], tor: [-16, 6, 0], head: [-2, -4, 0], ...F_WIDE};
export const LOW = {pos: [0, -.42, 0], tor: [-26, 6, 0], head: [10, -4, 0], fL: [.25, .1, -.3], fR: [-.25, .1, .32]};
export const AIR = {pos: [0, .02, 0], tor: [-6, 4, 0], lf: 1, fL: [.13, .6, -.22], fR: [-.13, .5, .08], kL: [.12, -.2, -1], kR: [-.12, -.2, -1]};
// the P2 stance (idle2: lower, the blade further out)
export const ST2 = {...ST, pos: [0, -.12, 0], tor: [-9, 10, 0], head: [-2, -8, 0], ...F_WIDE, gB: -40, gE: -42, gD: .7, cB: 52, th: -30};

// the blade lock (g_deflect's end = the pose S2b's `repel` starts from, PLAN §3.4 R0): leaning in, both hands on the grip, the
// blade crossed vertically against the player's position
export const LOCK = {...ST, pos: [0, -.14, -.04], tor: [-14, -6, 0], head: [-8, 6, 0], ...F_LUNGE, ...B(0, 0, 96, -1, {gF: 0, gB: -6, gE: 6, gD: .5}), rh: 1, aR: [60, 0, .9], hR: 'grip',
  pL: [.75, -.65, .1], pR: [.75, -.65, .1]};
// lying on her back (the down window, CS3 / CS4's start): the feet toward her front, the head turned aside, the sword along the
// ground at her left, the hat beside her right leg (hat world)
export const DOWN = {...ST, rot: [88, 0, 0], pos: [0, -1.04, 0], tor: [2, 0, 0], head: [-12, 24, 0], lf: 1, fL: [.15, .1, -.06], fR: [-.15, .1, -.02],
  kL: [.12, 0, -1], kR: [-.12, 0, -1], gF: 0, gB: -90, gE: -58, gD: .62, cB: 0, cR: 90, th: 6, ed: -1, aR: [6, 24, 1], hairF: 1, skG: .5, skIB: .08,
  hat: 'world', hwP: [-1.05, .02, -.5], hwE: [0, 30, 0], scHip: [-70, 0]};
// ---- the H pose: the ending's last pose (PLAN §3.7 C3 at 1030-1042) = tick 0 of ev_give / ev_toast (§7.3.2). S2b's `ending`
// must end exactly in it: standing, facing the player, the left hand at the brim (hand brim), the hat worn, eyes open (face
// calm), the sheathed sword (the scabbard with the hilt seated) upright-ish in her right hand
export const H_POSE = {...ST, pos: [0, -.02, 0], tor: [-2, 0, 0], head: [-6, 0, 0], ...F_TOG, hold: 0, sword: 'sheathed', scab: 'hand',
  hR: 'grip', hL: 'brim', bwL: 1, bzL: 40, aL: [120, 30, .9], pL: [.7, -.2, .2], aR: [14, 14, .94], scB: 8, scE: -22, scR: 0, face: 'calm'};

// ---- clip table ------------------------------------------------------------------------------------------------------------------
const clips = [];
const C = (name, keys, extra = {}) => clips.push({name, keys, ...extra});

// ---- locomotion ----------------------------------------------------------------------------------------------------------------
// the guard sway (sine 40 t, PLAN §2.3 secondary motion); idle2 lower with the blade further out (P2)
C('idle', [K(0, ST), K(20, {pos: [0, -.06, 0], tor: [-5, 7, 0], head: [-5, -3, 0], gE: -51, th: -41, aR: [8, 11, .96]}), K(40, ST)],
  {src: 'v1 8.0-9.6 / v3 6.5-8.2 (the stance: blade low across her front); sway sine 40 t'});
C('idle2', [K(0, ST2), K(20, {pos: [0, -.14, 0], tor: [-10, 11, 0], head: [-3, -7, 0], gE: -43, th: -31, aR: [10, 14, .95]}), K(40, ST2)],
  {src: 'P2: lower, the blade further out (PLAN §2.5)'});
{
  // a long gliding walk: contacts at 0 (left foot forward) and 12 (right); the blade carried low across her front; the free
  // right arm swings against the right leg
  const W0 = {...ST, pos: [0, -.05, 0], rot: [0, -3, 0], tor: [-5, 9, 0], fL: [.12, .1, -.5], fR: [-.12, .13, .46], aR: [-12, 10, .96]};
  C('walk', [K(0, W0), K(3, {pos: [0, -.03, 0], fL: [.12, .1, -.28], fR: [-.12, .2, .24]}), K(6, {pos: [0, -.01, 0], rot: [0, 0, 0], fL: [.12, .1, 0], fR: [-.12, .22, -.04], aR: [0, 10, .96]}),
    K(9, {pos: [0, -.03, 0], fL: [.12, .12, .26], fR: [-.12, .16, -.3]}),
    K(12, {pos: [0, -.05, 0], rot: [0, 3, 0], tor: [-5, 5, 0], fL: [.12, .13, .46], fR: [-.12, .1, -.5], aR: [14, 10, .96]}),
    K(15, {pos: [0, -.03, 0], fL: [.12, .2, .24], fR: [-.12, .1, -.28]}), K(18, {pos: [0, -.01, 0], rot: [0, 0, 0], fL: [.12, .22, -.04], fR: [-.12, .1, 0], aR: [0, 10, .96]}),
    K(21, {pos: [0, -.03, 0], fL: [.12, .16, -.3], fR: [-.12, .12, .26]}), K(24, W0)], {src: 'v1 8-26 (P1 walking between attacks), v5 9-13.5 (the walk-in)'});
  // P2 walk-in (glide): leaning forward, feet close, sliding; the blade trailing low behind her left side
  const G0 = {...ST2, pos: [0, -.16, 0], rot: [-10, 0, 0], tor: [-14, 4, 0], head: [6, -2, 0], fL: [.1, .1, -.22], fR: [-.1, .12, .2], gB: -110, gE: -40, gD: .62,
    cB: -150, th: -14, aR: [-28, 18, .96], hairS: -.55, skW: .6};
  C('glide', [K(0, G0), K(8, {pos: [0, -.13, 0], fL: [.1, .12, -.18], fR: [-.1, .1, .24], tor: [-13, 5, 0]}), K(16, G0)], {src: 'P2 walk-in (PLAN §2.5; the ghost glide D2 on foot)'});
  const strafe = sd => {
    // sd = +1 toward her left: the leading foot steps out (0-5), the trailing foot closes (10-15); facing the player
    const lead = sd > 0 ? 'fL' : 'fR', trail = sd > 0 ? 'fR' : 'fL';
    const S0 = {...ST, pos: [0, -.1, 0], tor: [-7, 6, -3 * sd], head: [-4, -4, 3 * sd], [lead]: [sd * .14, .1, sd > 0 ? -.1 : .1], [trail]: [-sd * .14, .1, sd > 0 ? .1 : -.1], aR: [10, 18, .95]};
    return [K(0, S0), K(3, {[lead]: [sd * .28, .2, sd > 0 ? -.1 : .1], pos: [0, -.06, 0]}), K(6, {[lead]: [sd * .36, .1, sd > 0 ? -.1 : .1], pos: [0, -.12, 0]}),
      K(10, {[lead]: [sd * .3, .1, sd > 0 ? -.1 : .1], [trail]: [-sd * .34, .1, sd > 0 ? .1 : -.1], pos: [0, -.11, 0]}),
      K(13, {[trail]: [-sd * .24, .19, sd > 0 ? .1 : -.1], pos: [0, -.06, 0]}), K(16, {[trail]: [-sd * .14, .1, sd > 0 ? .1 : -.1], pos: [0, -.1, 0]}), K(20, S0)];
  };
  C('strafe_l', strafe(1), {src: 'circling the player (P1 / P2 recoveries)'}); C('strafe_r', strafe(-1), {src: 'circling the player'});
}
C('backstep', [K(0, ST), K(2, {...CROUCH, pos: [0, -.2, 0]}, 'o'),
  K(4, {pos: [0, .06, .04], tor: [4, 6, 0], lf: .6, fL: [.13, .32, -.06], fR: [-.13, .28, .12], aR: [26, 34, .95], hairS: .4, skW: -.5}, 'o'),
  K(8, {pos: [0, .02, 0], lf: .3, fL: [.13, .2, -.1], fR: [-.13, .18, .08]}), K(10, {...CROUCH, pos: [0, -.22, 0], lf: 0, aR: [12, 26, .95], hairS: 0, skW: 0}, 'i'),
  K(12, {pos: [0, -.14, 0], tor: [-10, 6, 0]})], {src: 'a hop back (recovery spacing)'});
C('flinch', [K(0, ST), K(2, {tor: [10, 2, 5], head: [12, -8, 6], pos: [0, -.06, .04], aR: [14, 34, .95], th: -46}, 'o'), K(6, ST)], {src: 'hit reaction'});

// ---- P1 attacks (S3 p1.py; PLAN §4.3). Left-handed: the sword in her left hand. Edge sense: a cut that sweeps th upward keys
// ed 1, downward ed -1 (the edge leads). Flat blades: B(0, -88, th, -1) has th + toward her right (90 = right, edge forward) ----
// a flip about her centre of mass (c b above the pelvis pivot): the pelvis offset keeping it in place at pitch pt; y0 lifts it
const flipPos = (pt, c = .5, y0 = 0) => [0, +(y0 + c * (1 - Math.cos(pt * DEG))).toFixed(3), +(-c * Math.sin(pt * DEG)).toFixed(3)];
{
  // A1 turning crescent: the pivot (the brim swings round) 0-5, the blade low at her right with a glint 6, lock 7, the rising
  // vertical fan 8-10, the blade tipped over to her right 11-12 and the flat backhand crescent across her front (hit 14), the
  // follow-through to her left back, recovery
  const COIL = {pos: [0, -.18, 0], tor: [-12, 42, 0], head: [-6, -30, 0], ...F_WIDE, ...B(70, 0, -55, 1, {gL: .55}), aR: [20, 50, .95], hairS: .3};
  C('a1', [K(0, ST), K(3, {pos: [0, -.12, 0], tor: [-10, 30, 0], head: [-4, -40, 0], ...F_WIDE, ...B(56, 0, -48, 0, {gL: .53}), aR: [16, 40, .95], hairS: .4}),
    K(6, COIL, 'o'), K(7, {...COIL, pos: [0, -.2, 0], tor: [-13, 46, 0]}),
    K(8, {...B(40, 0, -10, 1, {gL: .58}), tor: [-8, 30, 0], pos: [0, -.12, 0]}, 'i'), K(9, {...B(15, 0, 45, 1, {gL: .6}), tor: [-2, 16, 0], pos: [0, -.06, 0]}, 'l'),
    K(10, {...B(0, 0, 92, .4, {gL: .6}), tor: [4, 6, 0], pos: [0, -.03, 0], head: [-10, -10, 0], aR: [10, 40, .95]}, 'l'),
    K(11, {...B(0, -44, 106, -.4, {gL: .58}), tor: [0, 22, 0], pos: [0, -.08, 0]}, 'l'),
    K(12, {...SW(125, 8, -1, 110, -28, .62), tor: [-18, 38, 0], pos: [0, -.28, 0], head: [-6, -20, 0], ...F_WIDE}, 'l'),
    K(13, {...SW(70, 8, -1, 58, -30, .64), tor: [-20, 22, 0]}, 'l'), K(14, {...SW(10, 6, -1, 0, -30, .66), tor: [-20, 0, 0], head: [-4, 0, 0]}, 'l'),
    K(15, {...SW(-50, 6, -1, -55, -28, .64), tor: [-20, -22, 0], head: [-4, 14, 0], hairS: -.3}, 'l'),
    K(17, {...SW(-100, 4, -1, -100, -24, .6), tor: [-18, -34, 0], aR: [-10, 30, .95]}, 'o'),
    K(24, {...SW(-75, 20, -1, -80, -35, .58), pos: [0, -.12, 0], tor: [-8, -20, 0], hairS: 0}), K(34, ST)],
    {src: 'v1 9.667-10.400 (cr_v1_a1, v1s_a2_*): pivot, magenta glint, rising fan, flat crescent; footage glint -> hit 6 t, stretched to 14'});
  // A2 combo-breaker: glints 0, the blade drawn up across to her upper right 2-4 (the white streak), lock 5, the glow 6-9 (held
  // high right, coiled), the diagonal cut upper-right -> lower-left 10-13 (hit 12); recovery: raised diagonally up-right 16-22,
  // lowered to the guard
  const HIGH = {pos: [0, -.06, 0], tor: [-4, 34, 0], head: [-6, -26, 0], ...B(0, -45, 140, -1, {gL: .5}), aR: [24, 30, .95], ...F_ST};
  C('a2', [K(0, ST), K(2, {...B(10, -45, 40, -1, {gL: .55}), tor: [-6, 16, 0]}), K(4, HIGH, 'o'), K(6, {...HIGH, tor: [-4, 38, 0], ...B(0, -45, 148, -1, {gL: .5})}),
    K(9, {...HIGH, tor: [-6, 40, 0], pos: [0, -.1, 0], ...B(0, -45, 152, -1, {gL: .5})}),
    K(10, {...B(0, -45, 118, -1, {gL: .54}), tor: [-6, 30, 0], pos: [0, -.12, 0]}, 'i'),
    K(11, {...B(0, -45, 62, -1, {gL: .6}), tor: [-8, 14, 0], pos: [0, -.16, -.02], ...F_LUNGE}, 'l'),
    K(12, {...B(0, -45, 2, -1, {gL: .64}), tor: [-12, -4, 0], head: [-4, 6, 0]}, 'l'),
    K(13, {...B(0, -45, -58, -1, {gL: .6}), tor: [-14, -18, 0], pos: [0, -.2, -.02]}, 'l'), K(15, {...B(0, -45, -100, -1, {gL: .56}), tor: [-14, -24, 0]}, 'o'),
    K(19, {...B(0, -45, 55, 1, {gL: .55}), tor: [-4, 10, 0], pos: [0, -.08, 0], ...F_ST}), K(22, {...B(0, -45, 62, 1, {gL: .55}), tor: [-4, 12, 0]}), K(30, ST)],
    {src: 'v1 19.050-19.500 (cr_v1_a2a6a5, v1s_a8_*): glint -> hit 4.3 t (the fastest), stretched to 12; recovery v1 19.65-19.90'});
}
{
  // A3 five crescents (hits 14 / 30 / 45 / 57 / 69, locks at hit - 7): 1 a vertical downward cut, 2 a short lunge + the downward
  // diagonal (her upper left -> lower right), 3 a rising vertical from low at her right front, 4 an overhead two-handed chop,
  // 5 a rising diagonal wedge (her lower left -> upper right); recovery open after hit 5
  C('a3', [K(0, ST), K(4, {...B(0, 0, 60, -1, {gL: .5}), tor: [-2, 14, 0], pos: [0, -.06, 0]}),
    K(9, {...B(0, 0, 118, -1, {gL: .48}), tor: [6, 10, 0], head: [-10, -6, 0], pos: [0, -.02, 0], aR: [30, 40, .95]}, 'o'),
    K(12, {...B(0, 0, 124, -1, {gL: .48}), tor: [8, 8, 0]}), K(13, {...B(0, 0, 62, -1, {gL: .56}), tor: [-4, 6, 0], pos: [0, -.1, 0]}, 'i'),
    K(14, {...B(0, 0, 0, -1, {gL: .64}), tor: [-16, 4, 0], pos: [0, -.18, -.02], ...F_WIDE}, 'l'), K(15, {...B(0, 0, -38, -1, {gL: .6}), tor: [-20, 4, 0]}, 'o'),
    // 2
    K(19, {...B(0, 45, -40, -1, {gL: .58}), tor: [-16, 0, 0]}), K(24, {...B(0, 45, 120, -1, {gL: .5}), tor: [0, -24, 0], head: [-8, 14, 0], pos: [0, -.06, 0], ...F_ST}, 'o'),
    K(28, {...B(0, 45, 128, -1, {gL: .48}), tor: [2, -28, 0]}), K(29, {...B(0, 45, 68, -1, {gL: .58}), tor: [-6, -8, 0], pos: [0, -.14, -.04], ...F_LUNGE}, 'i'),
    K(30, {...B(0, 45, 8, -1, {gL: .64}), tor: [-14, 12, 0], pos: [0, -.22, -.06]}, 'l'), K(31, {...B(0, 45, -48, -1, {gL: .6}), tor: [-18, 22, 0]}, 'o'),
    // 3
    K(36, {...B(30, 0, -36, 1, {gL: .56}), tor: [-14, 26, 0], pos: [0, -.18, 0], ...F_WIDE}), K(41, {...B(30, 0, -36, 1, {gL: .54}), tor: [-16, 34, 0], pos: [0, -.22, 0]}),
    K(44, {...B(15, 0, -4, 1, {gL: .6}), tor: [-10, 14, 0], pos: [0, -.14, 0]}, 'i'), K(45, {...B(0, 0, 40, 1, {gL: .64}), tor: [-4, 4, 0], pos: [0, -.08, 0]}, 'l'),
    K(46, {...B(0, 0, 95, 1, {gL: .6}), tor: [4, -4, 0], head: [-14, 0, 0]}, 'o'),
    // 4
    K(49, {...B(0, 0, 112, -1, {gL: .45}), rh: .8, tor: [10, 0, 0], pos: [0, 0, 0], ...F_ST}), K(53, {...B(0, 0, 122, -1, {gL: .44}), rh: 1, tor: [12, 0, 0]}),
    K(56, {...B(0, 0, 62, -1, {gL: .54}), rh: 1, tor: [-8, 0, 0], pos: [0, -.14, -.04], ...F_LUNGE}, 'i'), K(57, {...B(0, 0, 2, -1, {gL: .6}), rh: 1, tor: [-22, 0, 0], pos: [0, -.26, -.06]}, 'l'),
    K(58, {...B(0, 0, -30, -1, {gL: .56}), rh: .6, tor: [-24, 0, 0]}, 'o'),
    // 5
    K(63, {...B(0, -45, -130, 1, {gL: .56}), rh: 0, tor: [-16, -26, 0], head: [-6, 18, 0], pos: [0, -.2, 0], ...F_WIDE}), K(67, {...B(0, -45, -136, 1, {gL: .54}), tor: [-18, -30, 0]}),
    K(68, {...B(0, -45, -70, 1, {gL: .6}), tor: [-10, -12, 0], pos: [0, -.12, -.04]}, 'i'), K(69, {...B(0, -45, -8, 1, {gL: .64}), tor: [-2, 6, 0], pos: [0, -.04, -.06], ...F_LUNGE}, 'l'),
    K(70, {...B(0, -45, 55, 1, {gL: .62}), tor: [6, 22, 0], head: [-12, -10, 0]}, 'l'), K(72, {...B(0, -45, 100, 1, {gL: .58}), tor: [8, 30, 0], hairS: -.4}, 'o'),
    K(84, {...B(0, -45, 90, 1, {gL: .55}), tor: [4, 26, 0], pos: [0, -.06, -.04], hairS: 0}), K(96, ST)],
    {src: 'v1 23.150-26.300 (cr_v1_a3_leads, v1s_a12*, v1s_combo5): gaps 16 / 15 / 12 / 12; open after hit 5'});
}
{
  // A4 moon-leap dive + A5 aerial ring spin (the module leaps her 6 b and dives her onto the locked spot): crouch 0, leap 2,
  // apex 6-11 (the blade pointed at the target, the glint 7), raised over the shoulder 12, the forward flip about her centre
  // 12-18 (the blade carried by the body, swinging forward), feet first onto the spot, the low two-handed blade (hit 20);
  // A5: crouch2 22, the slash up to her right 25, lock2 27, the spin to her left 28-34 (a flat ring at head height, hit2 34),
  // land 38. Pitch and th stay in the -360 range after the flip (the same rotations)
  const APEX = {...ST, ...AIR, pos: [0, .1, 0], tor: [-4, 10, 0], head: [-4, -10, 0], ...B(-10, 0, 4, -1, {gL: .62}), aR: [30, 60, .9], hairS: -.2, skW: .3};
  const flipK = (t, pt, thRel) => K(t, {rot: [pt, 0, 0], pos: flipPos(pt, .5, .12), tor: [-16, 0, 0], head: [-10, 0, 0], lf: 1, fL: [.12, .72, -.32], fR: [-.12, .68, -.22],
    ...B(0, 0, thRel + pt, -1, {gL: .48}), aR: [100, 30, .9]}, 'l');
  C('a4', [K(0, ST), K(2, {...CROUCH, pos: [0, -.3, 0], tor: [-20, 6, 0], aR: [10, 30, .95]}),
    K(4, {pos: [0, .06, 0], tor: [6, 6, 0], lf: .5, fL: [.12, .2, -.04], fR: [-.12, .18, .08], aR: [60, 30, .95], hairS: -.5, skW: .4, ...B(-10, 0, -20, -1, {gL: .58})}, 'o'),
    K(7, APEX, 'o'), K(9, {...APEX, pos: [0, .12, 0], tor: [-2, 12, 0]}),
    K(12, {...APEX, ...B(0, 0, 150, -1, {gL: .46}), tor: [-10, 4, 0], head: [-8, -4, 0], aR: [80, 30, .9], fL: [.12, .7, -.3], fR: [-.12, .66, -.2], pos: [0, .12, 0]}),
    flipK(13, -60, 140), flipK(14, -120, 130), flipK(15, -180, 120), flipK(16, -240, 110), flipK(17, -300, 100),
    K(18, {rot: [-360, 0, 0], pos: [0, .14, 0], tor: [-12, 0, 0], head: [-4, 0, 0], lf: .9, fL: [.12, .58, -.24], fR: [-.12, .54, -.12], ...B(0, 0, -270, -1, {gL: .5}), rh: .6, aR: [60, 10, .9], hairS: .3, skW: -.3}, 'l'),
    K(19, {pos: [0, .02, 0], lf: .5, fL: [.14, .3, -.2], fR: [-.14, .27, .08], ...B(0, 0, -330, -1, {gL: .56}), rh: .8}, 'l'),
    K(20, {...LOW, rot: [-360, 0, 0], lf: 0, ...B(0, 0, -386, -1, {gL: .62}), rh: .8, pos: [0, -.44, -.04], tor: [-30, 0, 0], head: [8, 0, 0], hairS: 0, skW: 0}, 'i'),
    K(22, {pos: [0, -.46, -.04], tor: [-32, 4, 0], rh: 0, ...B(0, 0, -390, -1, {gL: .6})}),
    K(25, {...CROUCH, rot: [-360, 0, 0], pos: [0, -.3, 0], tor: [-14, 30, 0], ...B(0, -88, -264, -1, {gL: .58}), aR: [10, 50, .95]}, 'o'),
    K(27, {pos: [0, -.32, 0], tor: [-16, 36, 0], ...B(0, -88, -252, -1, {gL: .58})}),
    K(28, {pos: [0, .04, 0], rot: [-360, -20, 0], tor: [-4, 10, 0], lf: .8, fL: [.13, .45, -.12], fR: [-.13, .4, .1], ...B(0, -88, -268, -1, {gL: .64}), hairS: -.3}, 'o'),
    K(29, {rot: [-360, -90, 0]}, 'l'), K(30, {rot: [-360, -160, 0]}, 'l'), K(31, {rot: [-360, -230, 0]}, 'l'), K(32, {rot: [-360, -300, 0]}, 'l'), K(33, {rot: [-360, -350, 0]}, 'l'),
    K(34, {rot: [-360, -360, 0], tor: [-6, -10, 0]}, 'o'),
    K(38, {...CROUCH, rot: [-360, -360, 0], lf: 0, pos: [0, -.28, 0], ...B(0, -60, -300, -1, {gL: .55}), hairS: 0}, 'i'),
    K(48, {pos: [0, -.16, 0], tor: [-10, 4, 0], ...B(20, -30, -340, -1, {gL: .55})}), K(60, {...ST, rot: [-360, -360, 0], th: -400})],
    {src: 'v1 10.800-12.550 (cr_v1_a4, v1s_a3_*, v1s_a4_*): leap, apex glint, flip, the S-ribbon dive; the ring spin; apex 7 t'});
}
{
  // A6 back-blink: inside the bubble she pulls back 0-2 (the module glides her 12 b back in 3 t: leaning back, the hair and
  // the skirt streaming forward), appears in her stance at 4, settles 10
  C('a6', [K(0, ST), K(2, {pos: [0, -.12, .04], tor: [8, 4, 0], head: [6, -4, 0], fL: [.12, .14, .06], fR: [-.12, .1, .16], hairS: .7, skW: -.7, aR: [-10, 20, .95]}, 'o'),
    K(4, {...ST, pos: [0, -.1, 0], tor: [-8, 8, 0], hairS: .3, skW: -.3}, 'o'), K(10, {...ST, hairS: 0, skW: 0}), K(20, ST)],
    {src: 'v1 16.233-16.367 (cr_v1_a6, v1s_a7_*): the back-blink, then line 12'});
}
{
  // A9 yellow-ring grand slash: the turn 0-3 (a lilac streak at her right), the spin to her left 3-8 with the blade flat at the
  // waist (the ring at 4), crouched in its centre, the blade drawn back at her right for the iai dash (the yellow tell 8-16, the
  // star 17), lock 22, the full-screen magenta 24, go 26 (the dash), the cut 28 (back-right -> front-left at the waist), then
  // she stands beyond the player, the blade out behind her left (the module turns her)
  const DRAWN = {...LOW, pos: [0, -.36, 0], tor: [-20, 46, 0], head: [-10, -40, 0], ...SW(150, 10, -1, 125, -30, .6), aR: [40, 40, .9], hairS: 0};
  C('a9', [K(0, ST), K(3, {pos: [0, -.12, 0], tor: [-8, 30, 0], head: [-4, -20, 0], ...SW(100, 8, -1, 85, -25, .6), ...F_WIDE}),
    K(4, {rot: [0, -70, 0], ...SW(90, 8, -1, 80, -25, .62)}, 'l'), K(5, {rot: [0, -145, 0]}, 'l'), K(6, {rot: [0, -220, 0]}, 'l'), K(7, {rot: [0, -295, 0]}, 'l'),
    K(8, {rot: [0, -360, 0], tor: [-14, 30, 0]}, 'l'),
    K(10, {...DRAWN, rot: [0, -360, 0]}, 'o'), K(16, {...DRAWN, rot: [0, -360, 0], pos: [0, -.38, 0]}), K(22, {...DRAWN, rot: [0, -360, 0], pos: [0, -.4, 0], tor: [-22, 48, 0]}),
    K(25, {rot: [-14, -360, 0], pos: [0, -.3, -.08], tor: [-16, 40, 0], ...F_LUNGE, ...SW(160, 10, -1, 135, -30, .6), hairS: -.6, skW: .8}, 'i'),
    K(26, {rot: [-18, -360, 0], ...SW(115, 8, -1, 100, -28, .62), tor: [-14, 30, 0]}, 'l'), K(27, {...SW(50, 6, -1, 40, -28, .64), tor: [-10, 8, 0]}, 'l'),
    K(28, {...SW(-20, 6, -1, -20, -28, .66), tor: [-8, -16, 0], head: [-4, 12, 0]}, 'l'), K(29, {...SW(-85, 6, -1, -80, -26, .62), tor: [-6, -32, 0]}, 'l'),
    K(31, {rot: [-6, -360, 0], ...SW(-140, 8, -1, -125, -24, .58), tor: [-4, -42, 0], head: [-4, 24, 0], hairS: -.2, skW: .3}, 'o'),
    K(44, {rot: [0, -360, 0], pos: [0, -.12, 0], tor: [-4, -34, 0], ...SW(-130, 25, -1, -110, -35, .56), ...F_ST, hairS: 0, skW: 0}),
    K(64, {...ST, rot: [0, -360, 0]})],
    {src: 'v1 13.067-14.733 (cr_v1_a9_ring*, cr_yellow_cmp, v1s_a5_*, v1s_a6_*): spin, the ring, the yellow tell, the star, the magenta screen, the iai cut'});
}
{
  // A10 yellow plunge: crouch 0, spring 2 (the module lifts her 5 b), crouched in the air with the blade raised in both hands
  // 8-19 (the yellow tell 10-18), the plunge 19-22 (the blade swung down in front), the landing burst 22 (the blade low in
  // front, two hands), recovery
  const AIRC = {...ST, ...AIR, lf: .9, pos: [0, .3, 0], tor: [-24, 4, 0], head: [8, -4, 0], fL: [.13, .78, -.2], fR: [-.13, .72, -.08], ...B(0, 0, 120, -1, {gL: .5}), rh: 1, aR: [60, 30, .9]};
  C('a10', [K(0, ST), K(2, {...LOW, pos: [0, -.36, 0], ...B(30, 0, -30, -1, {gL: .55})}),
    K(5, {pos: [0, .1, 0], tor: [4, 4, 0], lf: .5, fL: [.12, .26, -.04], fR: [-.12, .22, .06], hairS: -.4, skW: .4, ...B(10, 0, 30, -1, {gL: .55})}, 'o'), K(9, AIRC, 'o'),
    K(19, {...AIRC, tor: [-26, 4, 0], pos: [0, .32, 0]}),
    K(20, {rot: [-20, 0, 0], tor: [-14, 0, 0], ...B(0, 0, 62, -1, {gL: .52}), rh: 1, lf: .7, pos: [0, .2, 0], fL: [.12, .5, .1], fR: [-.12, .46, .18], hairS: .5, skW: -.5}, 'i'),
    K(21, {rot: [-10, 0, 0], ...B(0, 0, 4, -1, {gL: .56}), lf: .3, pos: [0, -.05, 0]}, 'l'),
    K(22, {...LOW, rot: [0, 0, 0], lf: 0, ...B(0, 0, -28, -1, {gL: .6}), rh: 1, pos: [0, -.46, -.04], tor: [-34, 0, 0], head: [10, 0, 0], hairS: 0, skW: 0}, 'i'),
    K(26, {pos: [0, -.44, -.04], tor: [-30, 0, 0]}), K(40, {pos: [0, -.18, 0], tor: [-12, 4, 0], rh: 0, ...B(30, 0, -40, -1, {gL: .55})}), K(56, ST)],
    {src: 'v1 20.000-21.700 (v1s_a10_*, cr_yellow_cmp): spring, the yellow tell in the air, the dive, the radial burst'});
}
{
  // A7 moon disc (R2, A13): a7_tell: a step back 0, the yellow tell 2-10 (blade raised across), the retreat 4-14 (the module glides
  // her 6 b back), settle 14. a7_throw: crouch with the sword flat to her right 0, blade up 4, the crescent over her right 6, the
  // spin to her left 7-11 (the ring thickens into the disc), release 12 (the throw toward the player)
  C('a7_tell', [K(0, ST), K(3, {pos: [0, -.1, .04], tor: [4, 20, 0], head: [-8, -14, 0], ...B(-10, -45, 78, -1, {gL: .52}), fR: [-.14, .1, .22], aR: [20, 30, .95]}),
    K(4, {pos: [0, -.14, .06], tor: [10, 18, 0], fL: [.12, .12, .04], fR: [-.12, .1, .2], hairS: .6, skW: -.6}, 'o'),
    K(10, {pos: [0, -.12, .04], tor: [8, 16, 0]}), K(13, {...B(20, -20, 20, -1, {gL: .55}), pos: [0, -.12, 0], tor: [-2, 14, 0], hairS: .2, skW: -.2}), K(16, {...ST2})],
    {src: 'v3 14.63-15.10 (cr_v3_tell_zoom, mg_yellow_cmp): the yellow tell, the retreat'});
  C('a7_throw', [K(0, {...ST2, ...CROUCH, ...B(0, -88, 90, -1, {gL: .6}), tor: [-14, 30, 0]}), K(4, {...B(0, 0, 100, -1, {gL: .5}), tor: [0, 20, 0], pos: [0, -.12, 0]}),
    K(6, {...B(30, 0, -20, -1, {gL: .58}), tor: [-8, 30, 0], pos: [0, -.2, 0]}, 'l'),
    K(7, {rot: [0, -40, 0], ...B(0, -88, 70, -1, {gL: .62}), tor: [-6, 22, 0]}, 'l'), K(8, {rot: [0, -120, 0], ...B(0, -88, 90, -1, {gL: .64})}, 'l'),
    K(9, {rot: [0, -200, 0]}, 'l'), K(10, {rot: [0, -275, 0]}, 'l'), K(11, {rot: [0, -345, 0], ...B(0, -88, 66, -1, {gL: .64}), tor: [-8, 26, 0]}, 'l'),
    K(12, {rot: [0, -360, 0], ...B(0, -88, 0, -1, {gL: .66}), tor: [-10, -10, 0], ...F_LUNGE}, 'l'), K(13, {...B(0, -88, -64, -1, {gL: .62}), tor: [-10, -22, 0]}, 'o'),
    K(16, {...B(0, -70, -70, -1, {gL: .58}), tor: [-8, -16, 0], pos: [0, -.16, 0]})],
    {src: 'v3 15.10-16.90 (v3r_d1/d2/d3_*, cr_v3_disc1_gold): crouch, blade up, the crescent, the spin, the release'});
}

// ---- the ghost gauntlet move set (S4 p_ghost.py; PLAN §4.5): one clip per move; the scripts play the next over the previous ----
{
  // g_brim: the right hand rises to the brim (the "ultimate incoming" pose) and stays (loop 6-14)
  const BR = {...ST2, hR: 'brim', bwR: 1, bzR: 30, pR: [.8, -.2, .3], head: [-8, -6, 0]};
  C('g_brim', [K(0, ST2), K(6, BR, 'o'), K(10, {...BR, head: [-9, -7, 0], pos: [0, -.13, 0]}), K(14, BR)], {src: 'v2 f540-f550, v3 f440-f448 (cr_pretell_*): the hand to the brim'});
  // g_tell: the pose holds (the lilac switch is the module's look/form/ghost at 0), the mist burst 3 (a flinch outward), gone 4
  C('g_tell', [K(0, BR), K(3, {...BR, pos: [0, -.1, 0], tor: [-2, 6, 0], aL: [20, 40, .95]}, 'o'), K(4, {vis: 0}), K(12, {vis: 0})],
    {src: 'v2 f582-f620, v3 f492-f523 (cr_tell_T0): one-tick lilac switch, burst, ribbons', cuts: [4]});
  // g_reform: appears crouched (landing), solid 4, rises into the guard
  C('g_reform', [K(0, {...ST2, ...CROUCH, vis: .4, pos: [0, -.3, 0]}), K(3, {vis: 1}, 'o'), K(4, {pos: [0, -.26, 0]}), K(10, {...ST2})], {src: 'the ghost reforms (R1 / R3, A8 fail)'});
  // D1 g_dash: a compact ghost far away, hovering / growing 0-6, the straight dash 6-10 (leaning forward, the sword trailing), arrive
  // crouched at the player's right 10
  const HOV = {...ST, ...AIR, lf: .8, pos: [0, .03, 0], tor: [-10, 6, 0], fL: [.13, .55, -.15], fR: [-.13, .5, -.02], ...B(0, 88, -150, 1, {gL: .6}), aR: [10, 40, .9]};
  C('g_dash', [K(0, {...HOV, vis: .55}), K(6, {...HOV, vis: 1}, 'o'),
    K(8, {...HOV, rot: [-40, 0, 0], tor: [-10, 0, 0], ...B(0, 88, -168, 1, {gL: .62}), hairS: -.8, skW: 1, aR: [-40, 30, .95]}, 'i'), K(9, {rot: [-46, 0, 0]}),
    K(10, {...ST2, ...CROUCH, rot: [0, 0, 0], lf: 0, pos: [0, -.32, 0], ...B(0, 30, 150, 1, {gL: .55}), tor: [-14, -20, 0], hairS: 0, skW: 0}, 'i'), K(12, {pos: [0, -.3, 0]})],
    {src: 'v2 10.433 / 15.00, v3 8.933 / 11.550 (v2f_b1_dash): far reappear, hover, straight dash'});
  // D2 g_glide: appears low 0, glides in legs forward 2-9 (a sliding stop), the sword arm back
  C('g_glide', [K(0, {...ST, ...LOW, vis: .5, ...B(0, 88, -150, 1, {gL: .6})}), K(2, {vis: 1, pos: [0, -.4, 0], rot: [12, 0, 0], tor: [-24, 10, 0], fL: [.13, .1, -.6], fR: [-.13, .12, .3], hairS: -.7, skW: .8}, 'o'),
    K(9, {pos: [0, -.42, 0], rot: [6, 0, 0], tor: [-26, 14, 0], fL: [.15, .1, -.5], fR: [-.15, .1, .28], ...B(0, 88, -160, 1, {gL: .6}), hairS: -.2, skW: .2}, 'o'),
    K(12, {...LOW, rot: [0, 0, 0], pos: [0, -.38, 0], hairS: 0, skW: 0})], {src: 'v2 13.350, v3 13.100 (v3 f810-f813): side reappear, the glide'});
  // D3 g_drop: the white-violet flash 0 (a tense crouch), dissolves 2 (gone 2-6), rematerialises up-right of the player 7 (sword
  // raised), drops diagonally onto them 7-12, lands 12
  C('g_drop', [K(0, {...ST, ...CROUCH, pos: [0, -.2, 0], aR: [30, 40, .95]}), K(2, {vis: 0}), K(6, {vis: 0}),
    K(7, {...ST, ...AIR, vis: 1, lf: .8, pos: [0, .05, 0], tor: [4, -10, 0], ...B(0, 0, 130, 1, {gF: 0, gB: -20, gE: 40, gD: .6}), rh: .5, fL: [.13, .55, -.1], fR: [-.13, .5, .02]}),
    K(10, {rot: [-24, 0, 0], ...B(0, 0, 40, 1, {gF: 0, gB: 0, gE: 20, gD: .6}), rh: .5, hairS: .5}, 'i'),
    K(12, {...LOW, rot: [0, 0, 0], lf: 0, pos: [0, -.42, 0], ...B(0, 0, -70, 1, {gF: 0, gB: 10, gE: -40, gD: .6}), rh: 0, hairS: 0}, 'i'), K(14, {pos: [0, -.4, 0]})],
    {src: 'v2 16.067-16.733 (mg_v2_blink): flash, blink, drop', cuts: [2, 7]});
  // D4 g_run: appears 0, runs in on foot 2-10 (the sword trailing at her right back; two strides), lunges with the sword raised
  // overhead in both hands 10
  const RUN = {...ST, rot: [-14, 0, 0], tor: [-10, 4, 0], head: [8, 0, 0], ...B(0, -88, 160, -1, {gL: .6}), aR: [-40, 20, .95], hairS: -.7, skW: .7};
  C('g_run', [K(0, {...RUN, vis: .5, fL: [.12, .1, -.3], fR: [-.12, .3, .4]}), K(2, {...RUN, vis: 1, fL: [.12, .1, .3], fR: [-.12, .26, -.2]}),
    K(4, {fL: [.12, .3, .3], fR: [-.12, .1, -.45], aR: [40, 20, .95]}), K(6, {fL: [.12, .26, -.4], fR: [-.12, .1, .3], aR: [-40, 20, .95]}),
    K(8, {fL: [.12, .1, -.2], fR: [-.12, .3, .3], ...B(0, -60, 145, -1, {gL: .56}), rh: .3}),
    K(10, {rot: [-6, 0, 0], ...F_LUNGE, pos: [0, -.12, -.04], tor: [6, 0, 0], ...B(0, 0, 118, -1, {gL: .48}), rh: .8, hairS: -.2, skW: .3}, 'o'),
    K(14, {...B(0, 0, 124, -1, {gL: .46}), rh: .9, pos: [0, -.1, -.04]})], {src: 'v3 17.667 (v3r_s7..): the run-in'});
  // A8.1 g_ring: the arc wraps down from her upper left into a flat ring round the player at waist / knee height (hit 3, sweeping
  // her left -> right), then a spin in place to her right 4-14 that carries the sweep on
  C('g_ring', [K(0, {...ST2, ...CROUCH, ...B(0, 30, 150, -1, {gL: .55}), tor: [-14, -20, 0]}),
    K(1, {...B(0, 60, 105, -1, {gL: .58}), tor: [-14, -10, 0]}, 'l'), K(2, {...SW(-90, 15, 1, -80, -40, .62), tor: [-16, -14, 0], pos: [0, -.4, 0]}, 'l'),
    K(3, {...SW(-15, 15, 1, -10, -40, .66), tor: [-18, 10, 0]}, 'l'), K(4, {...SW(55, 15, 1, 50, -38, .64), tor: [-16, 30, 0]}, 'l'),
    K(5, {rot: [0, 40, 0], ...SW(95, 15, 1, 85, -36, .64)}, 'l'), K(7, {rot: [0, 120, 0]}, 'l'), K(9, {rot: [0, 200, 0]}, 'l'), K(11, {rot: [0, 280, 0]}, 'l'),
    K(13, {rot: [0, 350, 0], tor: [-12, 20, 0]}, 'l'), K(14, {rot: [0, 360, 0], tor: [-12, 18, 0]}, 'o')], {src: 'v2 11.050, v3 9.583 (v2f_s1_1f): the ring cut'});
  // A8.2 g_rise: spins in place to her left 0-7, the sword held low behind at her right, the rising diagonal from the player's
  // lower left (her lower right) to the upper right (her upper left) 7-10 (hit 9), riding its upper end (rising, legs tucked)
  C('g_rise', [K(0, {...ST2, ...CROUCH, ...B(0, 45, -150, 1, {gL: .56}), tor: [-10, 24, 0], aR: [40, 40, .9]}), K(2, {rot: [0, -90, 0]}, 'l'), K(4, {rot: [0, -200, 0]}, 'l'),
    K(6, {rot: [0, -300, 0], tor: [-6, 30, 0], aR: [60, 40, .9]}, 'l'), K(7, {rot: [0, -360, 0], ...B(0, 45, -150, 1, {gL: .55}), pos: [0, -.32, 0]}, 'o'),
    K(8, {...B(0, 45, -80, 1, {gL: .62}), tor: [-4, 14, 0], pos: [0, -.2, 0]}, 'i'), K(9, {...B(0, 45, 0, 1, {gL: .66}), tor: [2, -4, 0], pos: [0, -.06, 0]}, 'l'),
    K(10, {...B(0, 45, 75, 1, {gL: .62}), tor: [8, -20, 0], lf: .6, pos: [0, .04, 0], fL: [.13, .4, -.1], fR: [-.13, .34, .06], hairS: .4}, 'l'),
    K(14, {...B(0, 45, 105, 1, {gL: .58}), tor: [6, -26, 0], pos: [0, .06, 0]}, 'o')], {src: 'v2 11.683, v3 10.200 (cr_a82_windup): spin, arms up, the band'});
  // A8.3 g_leap: coil 0-5 (the sword overhead, blade up-left, the body arched back), raise 5, the leaping diagonal (her upper left
  // -> lower right) 8-10 (hit 9), a forward tumble above the player about her centre 10-16 (the blade carried by the body), gone 17
  const tumK = (t, pt, thRel, x = {}) => K(t, {rot: [pt, 0, 0], pos: flipPos(pt, .5, .6), tor: [-16, 0, 0], lf: 1, fL: [.12, .7, -.3], fR: [-.12, .66, -.2], ...B(0, 0, thRel + pt, -1, {gL: .5}), ...x}, 'l');
  C('g_leap', [K(0, {...ST2, ...CROUCH, ...B(0, 45, 130, -1, {gL: .5}), tor: [8, -14, 0], rh: .4}), K(5, {...B(0, 45, 150, -1, {gL: .48}), tor: [14, -18, 0], head: [-12, 10, 0], pos: [0, -.24, 0]}, 'o'),
    K(7, {...AIR, lf: .8, pos: [0, .1, 0], fL: [.13, .5, -.1], fR: [-.13, .44, .04], ...B(0, 45, 115, -1, {gL: .52}), tor: [10, -14, 0]}, 'o'),
    K(8, {...B(0, 45, 55, -1, {gL: .6}), tor: [-4, -4, 0]}, 'i'), K(9, {...B(0, 45, -5, -1, {gL: .64}), tor: [-14, 10, 0]}, 'l'),
    K(10, {...B(0, 45, -60, -1, {gL: .6}), tor: [-18, 16, 0], rh: 0, pos: [0, .3, 0]}, 'l'),
    tumK(11, -40, -50), tumK(12, -100, -50), tumK(13, -160, -50), tumK(14, -220, -50), tumK(15, -280, -50), tumK(16, -330, -50, {vis: .3}), K(17, {vis: 0}), K(18, {vis: 0})],
    {src: 'v2 12.450, v3 10.92 (v2f_s3_*): coil, the leaping cut, tumbling, vanishes', cuts: [17]});
  // A8.4 g_sweep: the sword arm back 0, the very wide flat sweep at ground level (hit 3), springs straight up and hangs upright,
  // turning 4-14
  C('g_sweep', [K(0, {...ST, ...LOW, pos: [0, -.42, 0], ...SW(160, 20, -1, 140, -45, .62), tor: [-24, 30, 0]}),
    K(2, {...SW(85, 20, -1, 80, -48, .66), tor: [-26, 14, 0]}, 'i'), K(3, {...SW(0, 20, -1, 0, -50, .68), tor: [-24, -4, 0]}, 'l'), K(4, {...SW(-70, 18, -1, -65, -45, .64), tor: [-20, -22, 0]}, 'l'),
    K(6, {...AIR, lf: .7, pos: [0, .06, 0], tor: [0, -10, 0], head: [-6, 0, 0], fL: [.08, .35, -.02], fR: [-.08, .32, .04], ...SW(-100, 15, -1, -95, -20, .6), hairS: .3}, 'o'),
    K(10, {rot: [0, 60, 0], ...SW(-100, 25, -1, -95, -30, .58)}), K(14, {rot: [0, 110, 0], pos: [0, .05, 0], ...SW(-100, 35, -1, -95, -35, .56)})], {src: 'v2 13.700, v3 13.583 (v2f_s4_*): the low sweep, the spring'});
  // A8.5 g_x: drops at the player's right 0, the sword swung up behind her right 0-3, the big crescent her upper right -> lower
  // left (hit 6) crossing the sweep into an X, stays close 7-13, gone 14 (th in the -360 range: the backswing runs on)
  C('g_x', [K(0, {...ST, ...CROUCH, pos: [0, -.3, 0], ...B(0, -45, -50, -1, {gL: .55})}),
    K(3, {...B(0, -45, -212, -1, {gL: .5}), tor: [6, 30, 0], head: [-10, -20, 0], pos: [0, -.16, 0], aR: [40, 40, .9]}, 'l'),
    K(4, {...B(0, -45, -220, -1, {gL: .48}), tor: [8, 34, 0]}), K(5, {...B(0, -45, -290, -1, {gL: .6}), tor: [-4, 14, 0], pos: [0, -.24, 0]}, 'i'),
    K(6, {...B(0, -45, -358, -1, {gL: .66}), tor: [-14, -8, 0]}, 'l'), K(7, {...B(0, -45, -410, -1, {gL: .62}), tor: [-20, -24, 0], pos: [0, -.32, 0]}, 'o'),
    K(13, {...B(0, -45, -412, -1, {gL: .6}), pos: [0, -.3, 0], tor: [-18, -20, 0]}), K(14, {vis: 0}), K(16, {vis: 0})],
    {src: 'v2 14.317, v3 14.183 (v2f_s5_*): the X', cuts: [14]});
  // A8.6 g_wrap: lands at the player's side, the blade drawn back 0, the flat crescent from the lower left round the legs rising
  // to the right (hit 3), twisting / crouching over the player
  C('g_wrap', [K(0, {...ST, ...CROUCH, pos: [0, -.34, 0], ...B(0, 70, 140, -1, {gL: .55}), tor: [-12, -30, 0]}),
    K(2, {...B(0, 70, 60, -1, {gL: .62}), tor: [-16, -10, 0], pos: [0, -.38, 0]}, 'i'), K(3, {...B(0, 70, -20, -1, {gL: .66}), tor: [-16, 10, 0]}, 'l'),
    K(4, {...B(0, 60, -90, -1, {gL: .62}), tor: [-14, 28, 0], pos: [0, -.32, 0]}, 'l'), K(6, {...B(0, 45, -130, -1, {gL: .58}), tor: [-10, 36, 0]}, 'o'), K(12, {pos: [0, -.3, 0], tor: [-14, 30, 0]})],
    {src: 'v2 ~16.91, v3 ~18.300 (v2f_s6_*): the wrap-around'});
  // A8.7 g_dome: the swirl over her right 0-2 (the blade lowered into the flat), the spin to her left with the blade out at the
  // waist 1-6 (hit 3), settle
  C('g_dome', [K(0, {...ST, pos: [0, -.18, 0], ...SW(60, -50, -1, 40, 30, .55), tor: [4, 10, 0]}),
    K(1, {rot: [0, -30, 0], ...SW(95, -15, -1, 75, 0, .6), tor: [-2, 14, 0], pos: [0, -.2, 0]}, 'l'), K(2, {rot: [0, -100, 0], ...SW(90, 8, -1, 80, -25, .62), tor: [-6, 18, 0]}, 'l'),
    K(3, {rot: [0, -180, 0]}, 'l'), K(4, {rot: [0, -260, 0]}, 'l'), K(5, {rot: [0, -330, 0], tor: [-8, 10, 0]}, 'l'), K(6, {rot: [0, -360, 0]}, 'l'),
    K(9, {rot: [0, -380, 0], ...SW(70, 15, -1, 60, -30, .6), pos: [0, -.2, 0]}, 'o'), K(12, {rot: [0, -380, 0], ...SW(60, 25, -1, 50, -35, .58)})],
    {src: 'v2 ~17.36, v3 18.767 (v2f_s7_*): the spin dome'});
  // A8.8 g_vert: crouched low at the player's right, the blade low in front (the pink glow 1-4 is the module's look/blade/pink),
  // springs up cutting vertically (hit 5), rises up and out of view turning head-first 6-17 (the blade carried by the body), gone 18
  C('g_vert', [K(0, {...ST, ...LOW, pos: [0, -.44, 0], ...B(20, 0, -35, 1, {gL: .58}), tor: [-26, 20, 0]}), K(4, {pos: [0, -.46, 0], tor: [-28, 22, 0], ...B(20, 0, -38, 1, {gL: .58})}),
    K(5, {...B(10, 0, 30, 1, {gL: .64}), tor: [-10, 10, 0], pos: [0, -.2, 0]}, 'i'),
    K(6, {...B(0, 0, 95, 1, {gL: .62}), tor: [6, 0, 0], pos: [0, .05, 0], lf: .6, fL: [.12, .3, -.04], fR: [-.12, .26, .06]}, 'l'),
    K(9, {rot: [-55, 0, 0], pos: [0, .3, 0], ...B(0, 0, 75, 1, {gL: .55}), tor: [-10, 0, 0], lf: 1, fL: [.12, .6, -.2], fR: [-.12, .56, -.1]}, 'l'),
    K(12, {rot: [-110, 0, 0], pos: [0, .7, 0], ...B(0, 0, 50, 1)}, 'l'), K(15, {rot: [-165, 0, 0], pos: [0, 1, 0], ...B(0, 0, 10, 1)}, 'l'),
    K(17, {rot: [-200, 0, 0], pos: [0, 1.1, 0], ...B(0, 0, -20, 1), vis: .4}, 'l'), K(18, {vis: 0}), K(20, {vis: 0})],
    {src: 'v2 ~18.11, v3 ~19.500 (mg_pink_glint): the pink glow, the rising vertical cut, rising out of view', cuts: [18]});
  // A8.9 g_dive: reappears high in her normal colours, the sword overhead in both hands 0, swung down in front as she dives
  // head-first 1-3, the blade leading down along the dive (hit 6)
  const DV = {...ST, ...AIR, lf: .9, rot: [-50, 0, 0], pos: [0, .9, .1], tor: [-10, 0, 0], head: [-20, 0, 0], ...B(0, 0, -50, -1, {gL: .55}), rh: 1, fL: [.12, .6, .25], fR: [-.12, .56, .3], hairS: .6, skW: -.8};
  C('g_dive', [K(0, {...ST, ...AIR, lf: .8, pos: [0, .5, 0], ...B(0, 0, 120, -1, {gL: .5}), rh: 1, tor: [6, 0, 0]}),
    K(1, {...B(0, 0, 80, -1, {gL: .5}), rot: [-15, 0, 0], pos: [0, .6, 0]}), K(2, {...B(0, 0, 15, -1, {gL: .52}), rot: [-35, 0, 0], pos: [0, .75, .05]}, 'l'),
    K(3, DV, 'l'), K(6, {...DV, rot: [-60, 0, 0], ...B(0, 0, -70, -1, {gL: .55})}), K(10, {...DV, rot: [-60, 0, 0], ...B(0, 0, -70, -1, {gL: .55})})],
    // blend 1 (S2d round 3, C3-1): the module plays g_dive right after hiding the rig (g_vert's 'gone'), so there is no pose to
    // blend from: the whole body shows at t1 (S2c's figure)
    {src: 'v2 19.083, v3 20.483 (v2f_s9_dive, v3r_s10_dive_1f): the diving overhead strike, blade down', blend: 1});
  // g_deflect: halts 1 b above the player 0 (recoiling upright), falls into the blade lock 2-10 (both hands, the blade crossed
  // vertically against the player's position, leaning in) = the pose `repel` (S2b) starts from
  C('g_deflect', [K(0, {...ST, ...AIR, lf: .8, rot: [-60, 0, 0], ...B(0, 0, 60, -1, {gF: 0, gB: 0, gE: 10, gD: .5}), rh: 1, hairS: -.3}), K(2, {rot: [-10, 0, 0], tor: [10, 0, 0], ...B(0, 0, 110, -1, {gF: 0, gB: 0, gE: 30, gD: .5}), hairS: 0, pL: [.75, -.65, .1], pR: [.75, -.65, .1]}, 'o'),
    K(6, {...ST, ...CROUCH, rot: [0, 0, 0], lf: 0, pos: [0, -.3, 0], ...B(0, 0, 100, -1, {gF: 0, gB: 0, gE: 4, gD: .55}), rh: 1}, 'i'),
    K(10, {...LOCK}), K(12, {...LOCK, pos: [0, -.12, -.04]})], {src: 'v2 19.10-19.28 (the parried dive), v2f_c1 (the lock)'});
}

// ---- the down window (core-driven; PLAN §3.5): lying on her back, the hat beside her; the kip-up (the natural end) -------------
{
  C('down', [K(0, DOWN), K(20, {...DOWN, tor: [3, 0, 0], head: [-12, 22, 0]}), K(40, DOWN)], {src: 'v2 24.95 -> v3 4.10 (v2f_d_*, cr_v2_down): lying on her back, the hat beside her'});
  // kipup: the legs swing up 0-4, the kip 4-8 (up 8), crouched 10 with the right hand on the hat's brim (picked up), the hat raised
  // over her head 14-17 and on at 17, standing 20
  C('kipup', [K(0, DOWN), K(4, {...DOWN, lf: 1, fL: [.13, .9, -.4], fR: [-.13, .86, -.3], tor: [-20, 0, 0], head: [-20, 10, 0], pos: [0, -1.12, 0]}, 'o'),
    K(6, {rot: [40, 0, 0], pos: [0, -.8, 0], lf: .6, tor: [-30, 0, 0], fL: [.13, .5, -.5], fR: [-.13, .46, -.4], hairF: .6, skG: .3}, 'i'),
    K(8, {...ST, ...LOW, rot: [0, 0, 0], lf: 0, pos: [0, -.46, 0], tor: [-30, -10, 0], head: [6, 10, 0], hat: 'world', hwP: [-1.05, .02, -.5], hwE: [0, 30, 0],
      hR: 'grip', plR: [-.32, .06, -.5], plwR: 1, hairF: .2, skG: 0, skIB: 0}, 'o'),
    K(10, {hat: 'hand', hhB: 90, hhE: 0, hhN: [0, 90], plR: [-.3, .1, -.5], plwR: 1}),
    K(14, {...ST, pos: [0, -.1, 0], hR: 'grip', hat: 'hand', hhB: 30, hhE: -20, hhN: [0, 80], plwR: 0, aR: [150, 20, .9], pR: [.7, .2, -.2], hairF: 0}, 'o'),
    K(17, {hat: 'worn', hR: 'brim', bwR: 1, bzR: 30, aR: [120, 30, .9]}), K(20, {...ST, bwR: 0})],
    {src: 'v3 4.10 (v3r_a_kipup, cr_v3_kipup): the kip-up; the hat picked up and put on (v3 4.7-6.5)'});
}

// ---- the event clips (PLAN §7.3.2): tick 0 = the ending's last pose (H_POSE) -----------------------------------------------------
{
  // ev_give: the left hand leaves the brim, the right hand raises the sheathed sword 0-8 (lift); both hands hold it out horizontally
  // at chest height, the hilt to the player's right (= her left) 12 (present); an underhand toss 26-30, the scabbard and the hilt
  // hidden at 30 (scab gone: the event's thrown-sword display takes over at hand_r)
  const PRES = {...H_POSE, hL: 'grip', bwL: 0, hiL: 1, aL: [70, 10, .8], pL: [.6, -.3, .4], scB: 90, scE: 4, scOff: .55, aR: [62, -8, .9], pR: [.7, -.4, .3], head: [-2, 0, 0]};
  C('ev_give', [K(0, H_POSE), K(6, {...H_POSE, hL: 'open', bwL: 0, aL: [10, 14, .96], scB: 20, scE: 30, aR: [40, 10, .9]}, 'o'),
    K(12, PRES, 'o'), K(22, {...PRES, pos: [0, -.04, 0]}), K(26, {...PRES, hiL: 0, hL: 'open', aL: [20, 20, .96], scB: 40, scE: -20, aR: [10, 20, .95], pos: [0, -.08, 0]}, 'io'),
    K(30, {hiL: 0, scB: 10, scE: 50, aR: [80, 10, .95], scab: 'gone', sword: 'gone'}, 'i'), K(34, {aR: [60, 14, .95]})],
    {src: 'PLAN §7.3.2 item branch E0-E34 (lift, present, toss)'});
  // ev_toast: the left hand leaves the brim, she looks up at the moon, the left hand rises palm up 0-14 (palm), the palm extends to
  // the player 30 (offer: the moonlight orb leaves it)
  const PALM = {...H_POSE, hL: 'open', bwL: 0, aL: [70, 6, .7], frL: 90, pL: [.6, -.5, .3], head: [10, 0, 0]};
  C('ev_toast', [K(0, H_POSE), K(6, {...H_POSE, hL: 'open', bwL: 0, aL: [40, 10, .8], head: [14, 4, 0], frL: 40}, 'o'), K(14, PALM, 'o'), K(24, {...PALM, head: [6, 0, 0]}),
    K(30, {...PALM, aL: [84, 2, .96], head: [0, 0, 0]}, 'io'), K(34, {...PALM, aL: [86, 2, .97], head: [0, 0, 0]})],
    {src: 'PLAN §7.3.2 buff branch E0-E34 (look, palm, offer)'});
  // ev_leave: a quarter turn away 0-6 (the sequence hides the rig at 6: gone)
  C('ev_leave', [K(0, {...H_POSE, hL: 'open', bwL: 0, aL: [10, 14, .96]}), K(6, {...H_POSE, hL: 'open', bwL: 0, aL: [6, 14, .96], rot: [0, 90, 0], tor: [-2, -10, 0], head: [-6, -20, 0], hairS: .3}, 'io'),
    K(10, {rot: [0, 96, 0], hairS: .2})], {src: 'PLAN §7.3.2 E34-E40 (the turn away; petals and wind hide her)'});
}

// ---- the cinematic placeholder (S2b replaces it with tools/scarlet_cine.mjs): every cine clip holds a static pose with the
// contract's length and events; the looks keyed where the plan's table says (hat / sword / scabbard / face) -----------------------
const P = (name, pose, extra = {}) => ({name, keys: [K(0, pose), K(1, pose)], placeholder: true, note: 'placeholder (S2b: tools/scarlet_cine.mjs)', ...extra});
export const CINE_PLACEHOLDER = [
  P('intro', {...H_POSE, hL: 'open', bwL: 0, aL: [0, 8, .97], scB: 0, scE: 80, cup: 'none'}),
  P('intro_end', ST),
  P('cs1', {...ST, ...CROUCH}),
  P('sq1', {...ST, hR: 'brim', bwR: 1, aR: [120, 30, .9], pR: [.7, -.2, .2]}),
  P('repel', LOCK),
  P('lead_down', DOWN),
  P('lead_stand', ST),
  P('ending', H_POSE),
];
// ---- export --------------------------------------------------------------------------------------------------------------------
export const CLIPS = clips;
export const accumulate = (c, defaults = DEFAULT_POSE) => accumulateLib(c, defaults);
export const sampleClip = (c, t, ks, defaults = DEFAULT_POSE) => sampleLib(c, t, ks, {defaults, discrete: DISCRETE,
  phase: (cl, x) => (cl.loop ? x / cl.len : x / 40) % 1});
export const restPose = () => ({...structuredClone(DEFAULT_POSE), ph: 0});
