// The clips of the 홍련 (Scarlet) rig (S:hr/PLAN.md §2.5, §4.3-4.5, §7.3.2; contract tools/mboss_scarlet/api.py CLIPS:
// names, lengths, loops and event ticks are frozen, this file only authors the motion). S2a authors the 39 fight /
// gauntlet / event clips here (api.CLIP_OWNER 'S2a'); the 8 cinematic clips belong to S2b's tools/scarlet_cine.mjs, and
// until it exists build_scarlet_rig.mjs uses CINE_PLACEHOLDER below (static poses with the contract lengths / events).
// HR rebuild (11-11, hr_design.md §2.3 / §8.3): lane H1c authors the 12 new fight clips (api.CLIP_OWNER 'H1': grog_in d4 tri rings
// ult hcut blue kcut mx nb q_grab q_air) in the section "the rebuilt fight kit" below; a7_tell, a7_throw and g_deflect stay in the
// rig unused.
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

// ---- the rebuilt fight kit (lane H1c, 11-11; tools/dev/plan/combat/hr_design.md §2.2-§2.3, §8.2): the 12 new fight clips.
// Names, lengths and event ticks are the contract's (api.CLIPS); the reference is the user's video (video_notes.md §2.2:
// P-d, P-i, P-j, U, P-h, P-blue, P-k, P-m, P-n, P-q), its wind-ups stretched to the telegraph rule. The poses are drawn for the
// raised F5 camera (she is seen from the front, a little above): big silhouettes, one idea per beat. Left-handed as ever; a
// parry cue (the pink glint at blade_mid, hit - 7) falls on a coiled pose with the blade clear of her body.
// Bz: B after a flat sweep (SW leaves tw +-90 on the blade)
const Bz = (cB, cR, th, ed, x = {}) => B(cB, cR, th, ed, {tw: 0, ...x});
// SWr: SW sweeping toward her right, its roll written with ed -1 (the same blade: 90 (1 - ed) + tw = -90 = 270), so the keys to and
// from the stance and the B cuts (ed -1) roll the blade the short way
const SWr = (b, d, hb, he, hd, x = {}) => ({...SW(b, d, 1, hb, he, hd), ed: -1, tw: 90, ...x});
const mix = (a, b, u) => +(a + (b - a) * u).toFixed(2);
// one turn of the body keyed every tick: yaw y0 -> y1 at a steady rate over t0 .. t0 + n while the flat blade opens from bearing
// b0 to b1 (relative to her; its edge leading toward her left: dir -1, her right: +1); x(u) adds channels
const spin = (t0, n, y0, y1, b0, b1, dir, he, hd, x = () => ({})) => Array.from({length: n + 1}, (_, i) => {
  const u = i / n, b = mix(b0, b1, u);
  return K(t0 + i, {rot: [0, mix(y0, y1, u), 0], ...SW(b, 4, dir, +(b * .8).toFixed(1), he, hd), ...x(u)}, 'l');
});
// a cut keyed every tick: the blade in the plane (cB, cR) from th0 to th1 over t0 .. t0 + n (linear), the hit at t0 + n / 2
const cut = (t0, n, cB, cR, th0, th1, ed, gl, x = () => ({})) => Array.from({length: n + 1}, (_, i) => {
  const u = i / n;
  return K(t0 + i, {...Bz(cB, cR, mix(th0, th1, u), ed, {gL: mix(gl[0], gl[1], Math.sin(Math.PI * u))}), ...x(u)}, 'l');
});
{
  // grog_in (the balance break): the guard smashed open 0-2 (both arms flung wide, the head thrown back), the knees buckle 3, she
  // topples backward, the hat leaving her head 6 and landing beside her right leg 10 (DOWN's spot), flat on her back 10, DOWN 12
  // (= `down` 0). blend 2: the snap out of whatever she was doing is the hit
  const OPEN = {pos: [0, -.02, .05], tor: [16, -12, 6], head: [20, 10, 4], ...F_ST, gF: 0, gB: -75, gE: 24, gD: .7, cB: -80, cR: 0, th: 62, ed: -1, tw: 0, rh: 0,
    aR: [50, 80, .95], hR: 'open', hairS: .3};
  const HATP = [[0, 2.05, .78], [-.5, 2.25, .56], [-.95, 1.85, .2], [-1.25, 1.05, -.22], [-1.05, .02, -.5]];
  C('grog_in', [K(0, ST), K(2, OPEN, 'o'),
    K(3, {pos: [0, -.14, .1], rot: [10, 0, 0], tor: [20, -8, 4], head: [14, 8, 2], fL: [.15, .1, -.08], fR: [-.15, .1, .06], gE: 30, aR: [70, 70, .95], scHip: [-10, 0]}, 'l'),
    K(5, {pos: [0, -.42, .16], rot: [34, 0, 0], lf: .4, tor: [14, -4, 2], head: [4, 6, 0], gB: -84, gE: 8, cR: 30, th: 44, aR: [84, 50, .95], scHip: [-38, 0]}, 'l'),
    K(6, {pos: [0, -.56, .16], rot: [46, 0, 0], lf: .5, gE: -6, cR: 45, th: 34, scHip: [-52, 0], hat: 'world', hwP: HATP[0], hwE: [50, 0, 0]}, 'l'),
    K(7, {hwP: HATP[1], hwE: [70, 10, 8]}, 'l'),
    K(8, {pos: [0, -.84, .1], rot: [68, 0, 0], lf: .55, tor: [6, 0, 0], head: [-6, 14, 0], gB: -90, gE: -36, cR: 72, th: 16, aR: [50, 30, 1], scHip: [-70, 0], hwP: HATP[2], hwE: [60, 18, 12]}, 'l'),
    K(9, {hwP: HATP[3], hwE: [26, 26, 6]}, 'l'),
    K(10, {...DOWN, hwP: HATP[4], hwE: [0, 30, 0]}, 'i'),
    K(12, DOWN, 'o')],
    {blend: 2, cuts: [6], src: 'no footage (video_notes §1.7: the video never reaches a balance break); the fall = repel 68-75 (v2f_c_throw) from her feet'});
}
{
  // d4 (P-d, v 112.40-114.8): the chest glint 0 (the blade laid flat across her chest), the coil to her right 3-9 (cue 7), the turn
  // to her left 9-15 with the blade flat at chest height (the ring, h1 14); the blade low at her right front 20-31 (cue 27), the
  // rising vertical fan 32-35 (h2 34), carried up over her head (cue 37), the two-handed vertical cut 42-45 (h3 44), the blade
  // round to her left hip 46-51 (cue 47), the flat forehand slash across her front 52-56 (h4 54), the follow-through, recovery
  const COIL = {pos: [0, -.16, 0], tor: [-8, 42, 0], head: [-4, -36, 0], ...F_WIDE, ...SW(120, 4, -1, 96, -12, .66), aR: [20, 50, .95]};
  const LOWF = {rot: [0, -360, 0], pos: [0, -.2, 0], tor: [-14, 26, 0], head: [-4, -20, 0], ...F_WIDE, ...Bz(30, 0, -36, 1, {gL: .56}), rh: 0, aR: [16, 40, .95]};
  const LHIP = {rot: [0, -360, 0], pos: [0, -.2, 0], tor: [-10, -38, 0], head: [-4, 32, 0], ...F_WIDE, ...SWr(-125, 6, -100, -28, .6), rh: 0, aR: [30, 40, .95]};
  C('d4', [K(0, ST), K(3, {pos: [0, -.06, 0], tor: [-4, 18, 0], head: [-4, -14, 0], ...SW(70, 0, -1, 55, -8, .56)}), K(6, COIL, 'o'), K(8, {...COIL, pos: [0, -.2, 0], tor: [-9, 46, 0]}),
    ...spin(9, 6, 0, -360, 120, 20, -1, -12, .68, u => ({tor: [-6, mix(46, 0, u), 0], head: [-4, mix(-36, 0, u), 0], pos: [0, -.14, 0], ...F_ST, aR: [30, 60, .95]})),
    K(17, {rot: [0, -360, 0], ...SW(-30, 14, -1, -24, -20, .64), tor: [-8, -10, 0], pos: [0, -.16, 0]}, 'l'),
    K(20, LOWF), K(27, {...LOWF, pos: [0, -.24, 0], tor: [-16, 32, 0]}), K(31, {...LOWF, pos: [0, -.26, 0], tor: [-17, 34, 0]}),
    K(32, {...Bz(22, 0, -22, 1, {gL: .58}), tor: [-12, 24, 0], pos: [0, -.2, 0]}, 'i'), K(33, {...Bz(10, 0, 8, 1, {gL: .62}), tor: [-8, 12, 0], pos: [0, -.14, 0]}, 'l'),
    K(34, {...Bz(0, 0, 44, 1, {gL: .64}), tor: [-2, 2, 0], pos: [0, -.08, 0], head: [-8, -2, 0]}, 'l'),
    K(35, {...Bz(0, 0, 92, 1, {gL: .6}), tor: [6, -4, 0], pos: [0, -.03, 0], head: [-12, 0, 0]}, 'l'),
    K(36, {...Bz(0, 0, 100, .1, {gL: .52}), rh: .4, tor: [8, -2, 0], pos: [0, -.01, 0]}, 'l'),
    K(37, {...Bz(0, 0, 104, -1, {gL: .48}), rh: .8, tor: [10, 0, 0], pos: [0, 0, 0], ...F_ST}, 'l'), K(41, {...Bz(0, 0, 108, -1, {gL: .46}), rh: 1, tor: [12, 0, 0]}),
    K(43, {...Bz(0, 0, 62, -1, {gL: .54}), rh: 1, tor: [-8, 0, 0], pos: [0, -.14, -.04], ...F_LUNGE}, 'i'),
    K(44, {...Bz(0, 0, 2, -1, {gL: .6}), rh: 1, tor: [-22, 0, 0], pos: [0, -.26, -.06], head: [-2, 0, 0]}, 'l'),
    K(45, {...Bz(0, 0, -30, -1, {gL: .56}), rh: .6, tor: [-24, 0, 0]}, 'o'),
    K(46, {...SWr(-40, 24, -30, -30, .6), rh: .2, tor: [-20, -14, 0], pos: [0, -.24, -.04]}, 'l'), K(47, {...SWr(-88, 12, -70, -28, .6), rh: 0, tor: [-14, -28, 0], pos: [0, -.21, -.02], ...F_WIDE}, 'l'),
    K(48, LHIP, 'l'), K(51, {...LHIP, pos: [0, -.24, 0], tor: [-11, -42, 0]}),
    K(52, {...SWr(-95, 6, -78, -28, .62), tor: [-12, -28, 0]}, 'i'), K(53, {...SWr(-45, 6, -36, -26, .64), tor: [-12, -10, 0], head: [-4, 12, 0]}, 'l'),
    K(54, {...SWr(5, 5, 4, -24, .66), tor: [-12, 8, 0], head: [-4, 0, 0], pos: [0, -.22, -.05], ...F_LUNGE}, 'l'),
    K(55, {...SWr(55, 5, 45, -24, .64), tor: [-12, 24, 0], head: [-4, -12, 0]}, 'l'), K(56, {...SWr(100, 4, 82, -24, .62), tor: [-10, 36, 0], head: [-4, -24, 0]}, 'l'),
    K(58, {...SWr(118, 8, 96, -26, .6), tor: [-9, 40, 0]}, 'o'), K(66, {...SWr(105, 18, 88, -32, .58), pos: [0, -.14, 0], tor: [-7, 30, 0], ...F_ST}), K(80, {...ST, rot: [0, -360, 0]})],
    {src: 'v 112.40-114.80 (P-d; vid d4): the chest glint, the flat ring, the rising fan, the vertical, the small slash; video gaps 20 / 8 / 8 -> 20 / 10 / 10'});
}
{
  // tri (P-i, v 146.9-149.4): the glint 0 (the blade drawn back level at her left hip, a thrust chamber), cue + lock 7, the lunge
  // 12-14 (the module glides her <= 6 b): the thrust at full reach h0 14; she rises, the blade carried high to her right 22-35 (cue
  // 31), three big descending crescents: 1 her upper right -> lower left 36-40 (h1 38), 2 her upper left -> lower right 46-50 (h2
  // 48; cue 41 as the blade swings up at her left), 3 upper right -> lower left, two-handed, with the lunging step 58-62 (h3 60;
  // cue 53), recovery
  const CH = {pos: [0, -.34, .05], rot: [0, 0, 0], tor: [-16, -36, 0], head: [0, 32, 0], fL: [.2, .1, .34], fR: [-.2, .1, -.4], gF: 0, gB: -100, gE: -34, gD: .5,
    cB: -16, cR: 0, th: 14, ed: -1, tw: 0, rh: 0, aR: [70, 10, .8]};
  // (the wound blade stands up and out over her shoulder, th 118: laid further back it is hidden behind her from the front)
  const HR = {pos: [0, -.12, 0], rot: [0, 0, 0], tor: [-2, 38, 0], head: [-8, -30, 0], ...F_WIDE, ...Bz(0, -58, 118, -1, {gL: .52}), rh: 0, aR: [24, 44, .95]};
  const body = (sd, lunge) => u => ({tor: [mix(-4, -20, u), mix(36, -38, u) * sd, 0], head: [-6, mix(-28, 22, u) * sd, 0], pos: [0, mix(-.14, -.32, Math.min(1, u * 2)), mix(0, -.08, u)],
    ...(u >= .25 ? lunge : {})});
  C('tri', [K(0, ST), K(2, {pos: [0, -.14, .02], tor: [-8, -14, 0], gF: 0, gB: -60, gE: -44, gD: .56, cB: 12, cR: 0, th: -14, ed: -1, tw: 0}, 'l'), K(5, CH, 'o'),
    K(7, {...CH, pos: [0, -.37, .06], tor: [-17, -40, 0]}), K(11, {...CH, pos: [0, -.4, .08], tor: [-18, -44, 0], gB: -108}),
    K(12, {rot: [-14, 0, 0], pos: [0, -.34, 0], gB: -70, gE: -26, gD: .52, cB: -8, th: 6, tor: [-14, -20, 0], head: [6, 16, 0], lf: .2, fL: [.16, .16, -.2], fR: [-.17, .12, .3], hairS: -.6, skW: .8}, 'i'),
    K(13, {rot: [-22, 0, 0], gB: -30, gE: -14, gD: .6, cB: -2, th: 2, tor: [-14, 4, 0], head: [12, -4, 0], fL: [.16, .12, -.54], fR: [-.17, .2, .46], aR: [20, 60, .95]}, 'l'),
    K(14, {rot: [-20, 0, 0], pos: [0, -.34, -.1], lf: 0, fL: [.16, .1, -.64], fR: [-.17, .1, .52], ...Bz(0, 0, 0, -1, {gL: .7}), tor: [-12, 28, 0], head: [12, -24, 0], aR: [-10, 80, .98], hairS: -.3,
      skW: .3}, 'l'),
    K(17, {rot: [-16, 0, 0], pos: [0, -.35, -.1], tor: [-13, 30, 0], hairS: 0, skW: 0}), K(25, HR, 'io'), K(31, {...HR, pos: [0, -.16, 0], tor: [-3, 42, 0]}), K(35, {...HR, pos: [0, -.18, 0], tor: [-4, 44, 0]}),
    ...cut(36, 4, 0, -58, 118, -112, -1, [.52, .66], body(1, F_LUNGE)),
    // (the blade swings out round her left side on its way up: at the cue 41 it is side-on to the viewer, not end-on)
    K(41, {...Bz(-96, 0, -24, -1, {gL: .6}), tor: [-16, -40, 0], pos: [0, -.26, -.05]}, 'l'), K(42, {...Bz(-104, 20, 50, -1, {gL: .54}), tor: [-8, -42, 0], pos: [0, -.18, -.02]}, 'l'),
    K(43, {...Bz(0, 58, -242, -1, {gL: .52}), tor: [-3, -40, 0], pos: [0, -.12, 0], head: [-8, 30, 0], fL: [.25, .1, .2], fR: [-.25, .1, -.24], aR: [30, 50, .95]}, 'l'),
    K(45, {...Bz(0, 58, -240, -1, {gL: .52}), tor: [-3, -43, 0], pos: [0, -.14, 0]}),
    ...cut(46, 4, 0, 58, -242, -472, -1, [.52, .66], body(-1, F_LUNGE_R)),
    K(51, {...Bz(0, 20, -512, -1, {gL: .56}), tor: [-16, 40, 0], pos: [0, -.26, -.05]}, 'l'), K(52, {...Bz(0, -20, -566, -1, {gL: .52}), tor: [-8, 44, 0], pos: [0, -.18, -.02]}, 'l'),
    K(53, {...Bz(0, -52, -602, -1, {gL: .52}), tor: [-2, 44, 0], pos: [0, -.14, .02], head: [-8, -30, 0], ...F_WIDE}, 'l'),
    K(57, {...Bz(0, -52, -598, -1, {gL: .52}), tor: [-1, 48, 0], pos: [0, -.2, .05]}),
    ...cut(58, 4, 0, -52, -602, -838, -1, [.52, .68], u => ({...body(1, {fL: [.16, .1, -.64], fR: [-.17, .1, .5]})(u), pos: [0, mix(-.2, -.4, Math.min(1, u * 2)), mix(.05, -.12, u)]})),
    K(70, {...Bz(0, -52, -828, -1, {gL: .56}), pos: [0, -.3, -.08], tor: [-17, -34, 0]}), K(84, {...ST, th: -760})],
    {src: 'v 146.9-149.4 (P-i; vid tri): the lunge, then three big crescents descending across the frame; video gaps 24 / 10 / 12'});
}
{
  // rings (P-j, v 150.0-151.9; P2 262.6-264.2): the glint 0 (the blade laid flat out at her right at chest height), cue 7, then one
  // turn per ring with the blade flat at chest height, alternating: r1 14 to her left, r2 24 to her right, r3 34, r4 44, r5 54
  // (P2 only). A turn runs h - 5 .. h + 1; the blade then swings on to the other side into the next coil (h + 4, the edge turned):
  // the cue (h + 3 = the next h - 7) falls as it settles there. After r4 the P1 pattern has no fifth ring: the module plays the next
  // clip (or `ult`) before the fifth turn starts at 49
  const CR = {pos: [0, -.18, 0], tor: [-8, 44, 0], head: [-4, -38, 0], ...F_WIDE, ...SW(120, 4, -1, 96, -10, .66), aR: [20, 50, .95]};
  const CL = {pos: [0, -.18, 0], tor: [-8, -44, 0], head: [-4, 38, 0], ...F_WIDE, ...SW(-120, 4, 1, -96, -10, .66), aR: [36, 44, .95]};
  const turn = (t, y0, sd) => [...spin(t, 6, y0, y0 - 360 * sd, 120 * sd, 0, -sd, -10, .68, u => ({tor: [-6, mix(44, -10, u) * sd, 0], head: [-4, mix(-38, 8, u) * sd, 0],
    pos: [0, mix(-.2, -.1, Math.sin(Math.PI * u)), 0], ...F_ST, aR: [30, 60, .95]})),
    K(t + 7, {...SW(-45 * sd, 4, -sd, -36 * sd, -10, .68), tw: 54 * sd, tor: [-7, -24 * sd, 0], head: [-4, 20 * sd, 0], pos: [0, -.14, 0]}, 'l'),
    K(t + 8, {...SW(-90 * sd, 4, -sd, -72 * sd, -10, .67), tw: -18 * sd, tor: [-8, -36 * sd, 0], head: [-4, 32 * sd, 0], pos: [0, -.17, 0], ...F_WIDE}, 'l'),
    K(t + 9, {...(sd > 0 ? CL : CR), rot: [0, y0 - 360 * sd, 0]}, 'l')];
  C('rings', [K(0, ST), K(3, {pos: [0, -.08, 0], tor: [-4, 20, 0], head: [-4, -16, 0], ...SW(75, 0, -1, 60, -8, .56)}), K(6, CR, 'o'), K(8, {...CR, pos: [0, -.2, 0], tor: [-9, 48, 0]}),
    ...turn(9, 0, 1), ...turn(19, -360, -1), ...turn(29, 0, 1), ...turn(39, -360, -1), ...turn(49, 0, 1).slice(0, 7),
    K(58, {rot: [0, -360, 0], ...SW(-60, 10, -1, -50, -20, .64), pos: [0, -.16, 0], tor: [-8, -24, 0], head: [-4, 20, 0], ...F_WIDE}, 'o'),
    K(66, {rot: [0, -360, 0], ...SW(-70, 22, -1, -60, -34, .6), pos: [0, -.12, 0], tor: [-6, -18, 0], head: [-4, 12, 0], ...F_ST}), K(78, {...ST, rot: [0, -360, 0]})],
    {src: 'v 150.0-151.9 (P-j; vid rings): flat rings at her chest height while she turns, one every 8-12 t -> 10 t'});
}
{
  // ult (U, v 151.93-155.2): the iai stance 0-22 (deep and side-on, the blade laid back along the scabbard at her right hip, the
  // right hand on its throat; yellow 0, star1 12), the draw 22-24: the blade whips out across her front (cut1 24, the white), held
  // out at full reach to her left through the web 26-43 (the edge turned over at star2 34), the return cut back across 43-48 (cut2
  // 46), the blade brought back to the hip 48-56 (settle 56), held, then the stance
  const IAI = {pos: [0, -.34, .02], tor: [-18, 50, 0], head: [-10, -44, 0], fL: [.27, .1, -.36], fR: [-.25, .1, .32], ...SW(150, 24, -1, 62, -50, .62), rh: 0, hR: 'grip', hsR: 1,
    aR: [20, 10, .8]};
  const OUT = {pos: [0, -.3, -.04], tor: [-12, -34, 0], head: [-6, 26, 0], fL: [.3, .1, -.42], fR: [-.26, .1, .36], ...SW(-112, -14, -1, -100, 2, .78), hsR: 1};
  C('ult', [K(0, ST), K(4, {...IAI, pos: [0, -.2, 0], tor: [-12, 34, 0], ...SW(130, 20, -1, 70, -40, .6)}, 'o'), K(8, IAI, 'o'), K(12, {...IAI, pos: [0, -.37, .02], tor: [-19, 52, 0]}),
    K(21, {...IAI, pos: [0, -.4, .03], tor: [-21, 55, 0], head: [-12, -48, 0]}),
    K(22, {...SW(128, 14, -1, 74, -42, .66), tor: [-18, 40, 0], pos: [0, -.36, 0]}, 'i'), K(23, {...SW(62, 6, -1, 44, -26, .72), tor: [-15, 10, 0], head: [-8, -10, 0], pos: [0, -.32, -.03]}, 'l'),
    K(24, {...SW(-14, 0, -1, -12, -12, .76), tor: [-13, -14, 0], head: [-6, 12, 0], pos: [0, -.3, -.04], fL: [.3, .1, -.42], fR: [-.26, .1, .36]}, 'l'),
    K(25, {...SW(-76, -8, -1, -66, -4, .78), tor: [-12, -28, 0], head: [-6, 22, 0]}, 'l'), K(26, OUT, 'l'), K(31, {...OUT, pos: [0, -.32, -.04], tor: [-13, -36, 0]}),
    K(33, {tw: 150}, 'l'), K(35, {tw: 270}, 'l'), K(42, {...OUT, ...SW(-116, -16, 1, -103, 4, .78), tw: 270, pos: [0, -.33, -.04], tor: [-13, -38, 0]}),
    K(43, {...SW(-108, -12, 1, -96, 0, .78), tw: 270}, 'i'), K(44, {...SW(-64, -6, 1, -56, -6, .77), tw: 270, tor: [-13, -22, 0], head: [-6, 14, 0]}, 'l'),
    K(45, {...SW(-6, 0, 1, -6, -14, .76), tw: 270, tor: [-14, -2, 0], head: [-6, -4, 0]}, 'l'),
    K(46, {...SW(50, 6, 1, 38, -24, .72), tw: 270, tor: [-15, 18, 0], head: [-8, -18, 0]}, 'l'),
    K(47, {...SW(100, 12, 1, 62, -36, .68), tw: 270, tor: [-17, 36, 0], head: [-10, -32, 0]}, 'l'),
    K(48, {...SW(132, 18, 1, 66, -44, .64), tw: 270, tor: [-18, 44, 0], head: [-10, -40, 0], pos: [0, -.32, 0]}, 'o'),
    K(56, {...IAI, ...SW(150, 24, 1, 62, -50, .62), tw: 270, pos: [0, -.3, .02], tor: [-16, 48, 0]}, 'io'), K(68, {pos: [0, -.28, .02], tor: [-15, 46, 0]}),
    K(86, ST)],
    {src: 'v 151.93-155.2 / 264.40-267.6 (U; ref ult_space_cut): yellow, the star, the slash into the white, the web, the star, the second white'});
}
{
  // hcut (P-h, v 129.0-130.2 / 231.2-232.6): from far: she drops into a long low stance, the blade trailing level behind her left
  // side (yellow 2), held and sinking (the sparkle 8-16, lock 19), go 24 (the module dashes her <= 16 b in 2 t): the flat forehand
  // cut at knee-to-waist height from behind her left across her front (cut 26) round to her right 24-28, held low, recovery
  const RUN = {pos: [0, -.5, .05], rot: [-12, 0, 0], tor: [-24, -36, 0], head: [16, 32, 0], fL: [.22, .1, .5], fR: [-.2, .1, -.56], ...SWr(-118, 14, -100, -48, .64), rh: 0, aR: [70, 16, .85],
    hR: 'open'};
  C('hcut', [K(0, ST), K(2, {pos: [0, -.24, .02], rot: [-4, 0, 0], tor: [-12, -14, 0], head: [6, 12, 0], fL: [.18, .1, .2], fR: [-.17, .1, -.3], ...SWr(-34, 32, -30, -50, .58), rh: 0,
      aR: [40, 12, .9], hR: 'open'}, 'l'), K(5, RUN, 'io'), K(16, {...RUN, pos: [0, -.54, .06], tor: [-26, -40, 0]}),
    K(19, {...RUN, pos: [0, -.56, .07], tor: [-27, -42, 0], aR: [56, 20, .8]}), K(23, {...RUN, pos: [0, -.58, .09], rot: [-16, 0, 0], tor: [-28, -46, 0], ...SWr(-128, 12, -108, -48, .64), aR: [44, 24, .8]}),
    K(24, {rot: [-24, 0, 0], pos: [0, -.42, -.04], ...SWr(-118, 12, -100, -46, .66), tor: [-22, -34, 0], head: [16, 22, 0], lf: .25, fL: [.18, .16, .2], fR: [-.18, .12, -.44], hairS: -.8, skW: 1}, 'i'),
    K(25, {rot: [-26, 0, 0], ...SWr(-62, 9, -52, -44, .68), tor: [-20, -12, 0], head: [16, 6, 0], fL: [.18, .12, -.3], fR: [-.18, .2, .3]}, 'l'),
    K(26, {rot: [-22, 0, 0], ...SWr(4, 7, 4, -44, .7), tor: [-20, 12, 0], head: [14, -10, 0], lf: 0, ...F_LUNGE, pos: [0, -.42, -.08]}, 'l'),
    K(27, {rot: [-16, 0, 0], ...SWr(70, 6, 58, -42, .68), tor: [-19, 32, 0], head: [12, -26, 0]}, 'l'),
    K(28, {rot: [-10, 0, 0], ...SWr(122, 6, 98, -40, .64), tor: [-18, 46, 0], head: [10, -38, 0], hairS: -.2, skW: .3, aR: [-20, 40, .95]}, 'o'),
    K(38, {rot: [-6, 0, 0], ...SWr(128, 14, 102, -44, .62), pos: [0, -.38, -.06], tor: [-16, 42, 0], hairS: 0, skW: 0}), K(52, ST)],
    {src: 'v 129.0-130.2, 231.2-232.6 (P-h): the far yellow, the sparkle at her, the huge flat disc swept at knee-to-waist height; video yellow -> cut 18 t -> 24'});
}
{
  // blue (P-blue, v 136.80-137.85): she draws herself up, feet together, the blade presented high and out at her left, the arm
  // straight (the yellow ring 0, inside the blue sphere 4-19: a long diagonal clear of the brim, flat to the viewer), draws it
  // back into a thrust chamber beside her left cheek pointing at the player 11-15 (lock 15), the lunge 20 (the module, <= 9
  // b): the thrust at full reach (hit 22), held, recovery
  const UP = {pos: [0, -.01, 0], tor: [-2, -8, 0], head: [-6, 6, 0], ...F_TOG, ...Bz(-90, 0, 50, -1, {gL: .7}), tw: 90, rh: 0, hR: 'open', aR: [-14, 16, .96]};
  const CHM = {pos: [0, -.2, .08], tor: [-8, -46, 0], head: [-4, 42, 0], fL: [.16, .1, .38], fR: [-.14, .1, -.34], gF: 0, gB: -66, gE: 24, gD: .46, cB: -24, cR: 0, th: 10, ed: -1, tw: 90,
    rh: 0, hR: 'open', aR: [84, -16, .7]};
  C('blue', [K(0, ST), K(2, {...Bz(-40, 0, -4, -1, {gL: .6}), tw: 45, pos: [0, -.02, 0]}, 'l'), K(4, UP, 'o'), K(10, {...UP, pos: [0, 0, 0], ...Bz(-90, 0, 54, -1, {gL: .7}), tw: 90}), K(15, CHM, 'io'), K(19, {...CHM, pos: [0, -.24, .11], tor: [-9, -50, 0], gB: -72}),
    K(20, {rot: [-12, 0, 0], pos: [0, -.26, 0], gB: -40, gE: 16, gD: .56, cB: -12, th: 5, tor: [-9, -20, 0], head: [4, 18, 0], lf: .2, fL: [.16, .14, -.1], fR: [-.15, .12, .2], aR: [40, 30, .8], hairS: -.6,
      skW: .8}, 'i'),
    K(21, {rot: [-18, 0, 0], gB: -16, gE: 8, gD: .7, cB: -4, th: 2, tor: [-10, 8, 0], head: [10, -6, 0], fL: [.16, .12, -.52], fR: [-.16, .18, .44], aR: [0, 60, .9]}, 'l'),
    K(22, {rot: [-18, 0, 0], pos: [0, -.36, -.12], lf: 0, fL: [.16, .1, -.64], fR: [-.17, .1, .52], ...Bz(0, 0, 0, -1, {gL: .7}), tw: 90, tor: [-10, 34, 0], head: [12, -30, 0], aR: [-16, 84, .98],
      hairS: -.3, skW: .3}, 'l'),
    K(26, {pos: [0, -.37, -.12], tor: [-11, 36, 0], hairS: 0, skW: 0}), K(32, {rot: [-12, 0, 0], pos: [0, -.32, -.1]}), K(46, ST)],
    {src: 'v 136.80-137.85 (P-blue; ref unblockable_flashes 136.88-137.85): the yellow ring turns into the blue sphere round her, then the lunge'});
}
{
  // kcut (P-k, v 158.20-159.30): the low crouch 0-3 (a sprinter's set: the right hand reaching down before her, the blade hidden
  // behind her, its tip up over her back; yellow 3), the sparkle 9, the charge 12-19 (she sinks and trembles: the lilac glow is the
  // module's look), lock 15, the dash through 20 (the module): the blade whipped round flat from behind her left across her front
  // 19-22 (cut 22), up to her right 23, the return cut down across 24-27, the blade flicked out low at her left, recovery
  const SET = {pos: [0, -.5, .02], rot: [-6, 0, 0], tor: [-32, 24, 0], head: [20, -20, 0], fL: [.26, .1, .4], fR: [-.24, .1, -.34], gF: 0, gB: -150, gE: -34, gD: .52, cB: 172, cR: 0, th: 34,
    ed: 1, tw: 0, rh: 0, hR: 'open', aR: [58, 4, 1]};
  C('kcut', [K(0, ST), K(1, {pos: [0, -.2, 0], tor: [-12, 10, 0], gF: 0, gB: -70, gE: -46, gD: .58, cB: 80, cR: 0, th: -14, ed: 0, tw: 0}, 'l'), K(3, SET, 'l'), K(9, {...SET, pos: [0, -.52, .02]}), K(12, {...SET, pos: [0, -.54, .03], tor: [-33, 26, 0]}), K(14, {...SET, pos: [0, -.51, .03]}), K(15, {...SET, pos: [0, -.55, .04]}),
    K(17, {...SET, pos: [0, -.52, .04]}), K(18, {...SET, pos: [0, -.56, .05], tor: [-34, 28, 0], th: 28}),
    K(19, {...SET, pos: [0, -.5, .02], rot: [-16, 0, 0], ...SW(-170, 6, 1, -140, -40, .6), tor: [-28, -20, 0], head: [20, 14, 0], aR: [30, 30, .9]}, 'l'),
    K(20, {rot: [-28, 0, 0], pos: [0, -.42, -.06], ...SW(-100, 8, 1, -84, -40, .66), tor: [-24, -26, 0], head: [22, 20, 0], lf: .25, fL: [.18, .14, -.2], fR: [-.18, .14, .3], hairS: -.8, skW: 1}, 'l'),
    K(21, {...SW(-14, 6, 1, -12, -38, .7), tor: [-22, 0, 0], head: [20, 0, 0], fL: [.18, .12, -.46], fR: [-.18, .2, .42]}, 'l'),
    K(22, {rot: [-20, 0, 0], ...SW(70, 2, 1, 58, -32, .68), tor: [-18, 28, 0], head: [14, -22, 0], lf: 0, ...F_LUNGE, pos: [0, -.36, -.1]}, 'l'),
    K(23, {rot: [-10, 0, 0], ...Bz(0, -50, 124, 1, {gL: .56}), tor: [-8, 42, 0], head: [2, -34, 0], pos: [0, -.26, -.08], hairS: -.2, skW: .3}, 'l'),
    K(24, {rot: [-7, 0, 0], ...Bz(0, -50, 128, 0, {gL: .54}), tor: [-5, 42, 0], pos: [0, -.22, -.07]}, 'l'),
    K(25, {rot: [-6, 0, 0], ...Bz(0, -50, 122, -1, {gL: .52}), tor: [-4, 40, 0], pos: [0, -.2, -.06]}, 'l'),
    K(26, {...Bz(0, -50, 60, -1, {gL: .6}), tor: [-10, 16, 0], pos: [0, -.26, -.08]}, 'l'), K(27, {...Bz(0, -50, 0, -1, {gL: .66}), tor: [-16, -10, 0], head: [2, 8, 0], pos: [0, -.32, -.1]}, 'l'),
    K(28, {...Bz(0, -50, -60, -1, {gL: .62}), tor: [-20, -30, 0], head: [2, 22, 0]}, 'l'), K(29, {...Bz(0, -50, -104, -1, {gL: .58}), tor: [-20, -38, 0], hairS: 0, skW: 0}, 'o'),
    K(34, {rot: [-4, 0, 0], ...Bz(0, -50, -100, -1, {gL: .56}), pos: [0, -.28, -.08], tor: [-17, -34, 0]}), K(50, ST)],
    {src: 'v 158.20-159.30 (P-k; ref tells_p2 158.45-159.20): the crouch, the big yellow, the lilac charge, the dash through with long cut lines; video yellow -> cuts 15 t -> 19'});
}
{
  // mx (P-m, v 236.25-236.9, 244.40-246.2): the iai crouch 0 (low, the blade drawn back low behind her left; the purple star 4, lock
  // 9), go 14 (the module streaks her to 1.6 b from the lock): the X in two strokes about its tick, the rising diagonal her lower left ->
  // upper right 13-15, the blade turned over above her 16 (x 16), the falling one her upper left -> lower right 17-20; the blade swirled up over her right 19-23 (cue
  // 21), the turn to her left with the blade out flat 24-30 (the dome, 28), settling, the P2 stance
  const MC = {pos: [0, -.4, .03], tor: [-22, -38, 0], head: [8, 32, 0], fL: [.26, .1, .3], fR: [-.24, .1, -.34], ...Bz(0, -45, -138, 1, {gL: .56}), rh: 0, aR: [50, 30, .9]};
  const SWIRL = {rot: [0, 0, 0], pos: [0, -.18, 0], ...SW(62, -48, -1, 42, 28, .58), tor: [4, 12, 0], head: [-8, -8, 0], ...F_ST, aR: [20, 40, .95]};
  C('mx', [K(0, ST2), K(2, {pos: [0, -.26, .02], tor: [-16, -20, 0], ...Bz(20, -30, -84, 0, {gL: .56})}, 'l'), K(4, MC, 'o'), K(9, {...MC, pos: [0, -.43, .04], tor: [-23, -42, 0]}), K(12, {...MC, pos: [0, -.46, .06], rot: [-6, 0, 0], tor: [-24, -46, 0]}),
    K(13, {rot: [-12, 0, 0], ...Bz(0, -45, -132, 1, {gL: .56}), pos: [0, -.42, 0]}, 'i'),
    K(14, {rot: [-18, 0, 0], ...Bz(0, -45, -24, 1, {gL: .64}), tor: [-16, -12, 0], head: [10, 8, 0], pos: [0, -.32, -.06], lf: .3, fL: [.16, .14, -.3], fR: [-.17, .2, .34], hairS: -.7, skW: .8}, 'l'),
    K(15, {rot: [-12, 0, 0], ...Bz(0, -45, 80, 1, {gL: .58}), tor: [-4, 20, 0], head: [-2, -16, 0], pos: [0, -.22, -.08], fL: [.16, .12, -.5], fR: [-.17, .14, .4]}, 'l'),
    K(16, {rot: [-10, 0, 0], ...Bz(0, 0, 102, 0, {gL: .5}), tor: [0, 0, 0], head: [-6, 0, 0], pos: [0, -.2, -.1], lf: 0, ...F_LUNGE}, 'l'),
    K(17, {rot: [-8, 0, 0], ...Bz(0, 45, 118, -1, {gL: .52}), tor: [-2, -20, 0], head: [-6, 16, 0], pos: [0, -.22, -.1]}, 'l'),
    K(18, {rot: [-6, 0, 0], ...Bz(0, 45, 24, -1, {gL: .66}), tor: [-14, 4, 0], head: [0, -4, 0], pos: [0, -.32, -.1], hairS: -.2, skW: .2}, 'l'),
    K(19, {rot: [-3, 0, 0], ...Bz(0, 45, -66, -1, {gL: .62}), tor: [-20, 26, 0], head: [2, -18, 0], pos: [0, -.36, -.1]}, 'l'), K(20, {rot: [-2, 0, 0], ...Bz(0, 45, -102, -1, {gL: .58}), tor: [-20, 32, 0]}, 'o'),
    K(22, SWIRL, 'io'), K(23, {...SWIRL, pos: [0, -.2, 0], tor: [5, 16, 0]}),
    K(24, {rot: [0, -30, 0], ...SW(95, -15, -1, 75, 0, .6), tor: [-2, 14, 0], pos: [0, -.2, 0]}, 'l'), K(25, {rot: [0, -95, 0], ...SW(90, 8, -1, 78, -24, .64), tor: [-6, 18, 0]}, 'l'),
    K(26, {rot: [0, -165, 0]}, 'l'), K(27, {rot: [0, -235, 0]}, 'l'), K(28, {rot: [0, -300, 0]}, 'l'), K(29, {rot: [0, -345, 0], tor: [-8, 10, 0]}, 'l'), K(30, {rot: [0, -360, 0]}, 'l'),
    K(33, {rot: [0, -376, 0], ...SW(70, 15, -1, 60, -30, .6), pos: [0, -.2, 0]}, 'o'), K(40, {rot: [0, -372, 0], ...SW(60, 25, -1, 50, -35, .58), pos: [0, -.16, 0]}), K(60, {...ST2, rot: [0, -360, 0]})],
    {src: 'v 236.25-236.9, 244.40-246.2 (P-m; ref tells_p2): the purple star, two crossing crescents with a star burst, the dome'});
}
{
  // nb (P-n, v 261.00-262.05): the crouch 0, the leap 2 (the module: 5 b up, <= 6 b toward the player), at the apex 8 she hangs
  // bowed over the player, the blade wound high at her right (cue + lock 13); three bands thrown down: the cut from her upper
  // right down to her left front 18-22 (b1 20; its plane 30 deg to the left of her aim), wound high at her left (cue 23), the cut
  // from her upper left down to her right front 28-32 (b2 30; 30 deg to the right), the
  // blade raised before her in both hands (cue 33), the straight chop 38-41 (b3 40); she drops 41-46 and lands low 46, the P2 stance
  const HANG = {...ST2, ...AIR, lf: 1, pos: [0, .34, 0], rot: [-16, 0, 0], tor: [-10, 34, 0], head: [-14, -28, 0], fL: [.14, .72, -.28], fR: [-.13, .6, -.04], ...Bz(-30, -40, 108, -1, {gL: .52}),
    rh: 0, aR: [40, 60, .9], hR: 'open', hairS: .2, skW: -.2};
  const airCut = (t, cR, sd) => cut(t, 4, -30 * sd, cR, 108, -80, -1, [.52, .66], u => ({tor: [mix(-10, -22, u), mix(34, -30, u) * sd, 0], head: [-14, mix(-28, 22, u) * sd, 0]}));
  C('nb', [K(0, ST2), K(2, {...CROUCH, pos: [0, -.32, 0], tor: [-22, 8, 0], ...Bz(30, 0, -30, -1, {gL: .55})}),
    K(4, {pos: [0, .06, 0], tor: [6, 6, 0], head: [-10, -4, 0], lf: .5, fL: [.12, .2, -.04], fR: [-.12, .18, .08], aR: [60, 30, .95], hairS: -.5, skW: .4, ...Bz(-10, 0, -20, -1, {gL: .58})}, 'o'),
    K(8, HANG, 'o'), K(13, {...HANG, pos: [0, .36, 0], tor: [-9, 38, 0]}), K(17, {...HANG, pos: [0, .37, 0], tor: [-8, 40, 0]}),
    ...airCut(18, -40, 1), K(23, {...Bz(-10, -10, -132, -1, {gL: .56}), tor: [-18, -34, 0]}, 'l'), K(24, {...Bz(15, 20, -196, -1, {gL: .52}), tor: [-12, -38, 0]}, 'l'),
    K(25, {...Bz(30, 40, -252, -1, {gL: .52}), tor: [-10, -38, 0], head: [-14, 28, 0], fL: [.13, .6, -.04], fR: [-.14, .72, -.28]}, 'l'), K(27, {...Bz(30, 40, -250, -1, {gL: .52}), tor: [-8, -40, 0]}),
    ...cut(28, 4, 30, 40, -252, -440, -1, [.52, .66], u => ({tor: [mix(-10, -22, u), mix(-38, 30, u), 0], head: [-14, mix(28, -22, u), 0]})),
    // (the blade back up before her the short way, both hands: the chop's wind-up; flat to the viewer)
    K(33, {...Bz(16, 20, -404, -1, {gF: .6, gB: 0, gE: 10, gD: .55, gL: .56}), tor: [-18, 16, 0], rh: .3}, 'l'),
    K(34, {...Bz(0, 0, -338, -1, {gF: .2, gB: 0, gE: 20, gD: .55}), tw: 45, tor: [-12, 6, 0], head: [-16, -4, 0], rh: .7}, 'l'),
    K(35, {...Bz(0, 0, -268, -1, {gF: 0, gB: 0, gE: 28, gD: .56}), tw: 90, tor: [-6, 0, 0], head: [-18, 0, 0], rh: 1, hR: 'grip', fL: [.13, .7, -.2], fR: [-.13, .66, -.1]}, 'l'),
    K(38, {...Bz(0, 0, -264, -1, {gF: 0, gB: 0, gE: 30, gD: .56}), tw: 90, tor: [-4, 0, 0], pos: [0, .38, 0]}),
    K(39, {...Bz(0, 0, -312, -1, {gF: .6, gL: .56}), tw: 40, tor: [-14, 0, 0]}, 'i'), K(40, {...Bz(0, 0, -362, -1, {gL: .62}), rh: 1, tor: [-24, 0, 0], head: [-10, 0, 0], pos: [0, .3, 0]}, 'l'),
    K(41, {...Bz(0, 0, -392, -1, {gL: .6}), rh: .8, tor: [-26, 0, 0]}, 'o'),
    K(44, {rot: [-6, 0, 0], pos: [0, .12, 0], lf: .6, fL: [.14, .34, -.16], fR: [-.14, .3, .1], tor: [-18, 0, 0], head: [0, 0, 0], hairS: .5, skW: -.5}, 'l'),
    K(46, {...LOW, rot: [0, 0, 0], lf: 0, pos: [0, -.44, -.04], ...Bz(0, 0, -388, -1, {gL: .6}), rh: .8, tor: [-30, 0, 0], head: [8, 0, 0], hairS: 0, skW: 0}, 'i'),
    K(50, {pos: [0, -.42, -.04], tor: [-28, 2, 0], rh: 0, hR: 'open'}), K(66, {...ST2, th: -390})],
    {src: 'v 261.00-262.05 (P-n; ref tells_p2 261.20 / 262.05): two huge diagonal bands from above, then a third; video gaps 6-12 t / 8 t -> 10 / 10'});
}
{
  // q_grab (P-q, v 247.00-247.60; ref hr_grab_4fps): from far: the glint 0, she sinks, the blade trailing behind her left, the open
  // right hand reaching out at the player (the ghost form 4 and the purple star 8 are the module's; lock 13), the ghost lunge 16-20
  // (the module, <= 14 b): flat out, the arm stretched ahead; the hand closes at the player's chest (grab 20), held 21. From 21
  // the miss (landed -> q_air at 21): she snatches at the air, pulls the empty fist in, straightens, the P2 stance at 34
  const REACH = {...ST2, pos: [0, -.34, .04], rot: [-6, 0, 0], tor: [-18, -30, 0], head: [8, 26, 0], fL: [.2, .1, .36], fR: [-.2, .1, -.44], ...SWr(-116, 22, -100, -44, .6), rh: 0,
    hR: 'open', aR: [118, -10, .86], pR: [.3, -.6, .4]};
  const FLY = {rot: [-44, 0, 0], pos: [0, .03, 0], lf: .8, tor: [-8, -8, 0], head: [34, 6, 0], fL: [.13, .55, .1], fR: [-.13, .5, .22], ...SWr(-165, 4, -140, -30, .62), aR: [150, -6, 1],
    hairS: -.8, skW: 1};
  C('q_grab', [K(0, ST2), K(2, {pos: [0, -.24, .02], tor: [-12, -12, 0], ...SWr(-50, 30, -44, -48, .58), rh: 0, aR: [60, 0, .7], hR: 'open'}, 'l'), K(4, REACH, 'o'),
    K(8, {...REACH, pos: [0, -.37, .05], aR: [120, -10, .9]}), K(13, {...REACH, pos: [0, -.4, .06], tor: [-19, -34, 0], aR: [122, -8, .96]}),
    K(15, {...REACH, pos: [0, -.42, .08], rot: [-12, 0, 0], tor: [-20, -36, 0], aR: [124, -8, 1]}),
    K(16, {...FLY, rot: [-30, 0, 0], lf: .4, pos: [0, -.14, 0], fL: [.16, .2, -.1], fR: [-.16, .3, .3]}, 'i'), K(17, FLY, 'l'), K(19, {...FLY, rot: [-40, 0, 0], aR: [146, -4, 1]}),
    K(20, {rot: [-8, 0, 0], lf: 0, pos: [0, -.2, -.08], ...F_LUNGE_R, tor: [-12, -26, 0], head: [2, 22, 0], ...SWr(-140, 14, -116, -40, .6), aR: [98, -18, .74], hR: 'grip', hairS: -.2, skW: .3}, 'i'),
    K(21, {}),      // (held: the module takes the landed branch at 21 = api.Q_AIR_T0; q_air 0 is this pose)
    K(22, {pos: [0, -.22, -.08], tor: [-13, -22, 0], aR: [92, -22, .6], hairS: 0, skW: 0}), K(26, {rot: [-2, 0, 0], pos: [0, -.16, -.04], tor: [-8, -10, 0], head: [-2, 2, 0], aR: [70, -10, .5], hR: 'open'}),
    K(34, {...ST2, pos: [0, -.13, 0]}), K(40, ST2)],
    {src: 'v 247.00-247.60 (P-q; ref hr_grab_4fps 246.80-247.55): the far lilac glint, the lilac ghost lunge = the grab'});
}
{
  // q_air (P-q, v 247.8-258.2; ref hr_grab_4fps, p2_aerial_grab): from the grab: both arms heave upward (throw 0), she rises with
  // the motion 2-10 (the module); hanging, the blade wound high at her right (cue + lock 15), the diagonal beam cut 20-24 (beam
  // 22); the blade raised before her in both hands (cue + lock 31), the dive 34 (the module): the blade driven down (hit 38),
  // landing low 40; the second leap 46, at the apex 52 the blade thrust straight up at the sky, the free arm spread (the purple
  // star 62, lock 67), brought down to point at the player 72-74 (the pillar 74); she drops 78, lands 84, the P2 stance
  const G0 = {...ST2, rot: [-8, 0, 0], lf: 0, pos: [0, -.2, -.08], ...F_LUNGE_R, tor: [-12, -26, 0], head: [2, 22, 0], ...SWr(-140, 14, -116, -40, .6), rh: 0, aR: [98, -18, .74],
    hR: 'grip'};     // (= q_grab 20-21)
  const HANG = {...ST2, ...AIR, rot: [-14, 0, 0], lf: 1, pos: [0, .34, 0], tor: [-10, 34, 0], head: [-14, -28, 0], fL: [.14, .72, -.28], fR: [-.13, .6, -.04], ...Bz(0, -42, 108, -1, {gL: .52}),
    rh: 0, aR: [40, 60, .9], hR: 'open', hairS: .2, skW: -.2};
  // (the dive's wind-up: the blade reversed, point down before her in both hands, the fists before her brow: a plunging stab)
  const GUARD = {...ST2, ...AIR, rot: [-8, 0, 0], lf: .9, pos: [0, .8, 0], tor: [-2, 2, 0], head: [-16, -2, 0], fL: [.13, .76, -.2], fR: [-.13, .7, -.08], ...Bz(0, 0, -82, -1, {gF: 0, gB: 0, gE: -40, gD: .8}),
    tw: 90, rh: 1, hR: 'grip', aR: [60, 30, .9]};
  const SKY = {...ST2, ...AIR, rot: [0, 0, 0], lf: 1, pos: [0, .34, 0], tor: [6, -6, 0], head: [-16, 6, 0], fL: [.12, .5, -.16], fR: [-.13, .66, -.02], ...Bz(0, 0, 92, -1, {gL: .68}), tw: 90, rh: 0, hR: 'open',
    aR: [24, 84, .96], hairS: 0, skW: 0};
  C('q_air', [K(0, G0), K(1, {rot: [-4, 0, 0], pos: [0, -.1, -.04], tor: [0, -12, 0], head: [8, 10, 0], cB: -124, th: 30, gB: -100, gE: -14, gD: .62, aR: [140, 0, .9], hR: 'open'}, 'l'),
    K(2, {rot: [0, 0, 0], pos: [0, .02, 0], lf: .4, fL: [.13, .16, -.06], fR: [-.13, .14, .08], tor: [12, 0, 0], head: [16, 0, 0], cB: -108, th: 72, gB: -84, gE: 14, gD: .64, aR: [168, 16, 1],
      hR: 'open', hairS: -.5, skW: .5}, 'l'),
    K(5, {...AIR, pos: [0, .2, 0], lf: 1, tor: [2, 12, 0], head: [-4, -10, 0], fL: [.13, .6, -.2], fR: [-.13, .5, .04], ...Bz(-10, -30, 120, -1, {gL: .56}), aR: [90, 40, .95]}, 'io'),
    K(10, HANG, 'o'), K(15, {...HANG, pos: [0, .36, 0], tor: [-9, 38, 0]}), K(19, {...HANG, pos: [0, .37, 0], tor: [-8, 40, 0]}),
    ...cut(20, 4, 0, -42, 108, -84, -1, [.52, .66], u => ({tor: [mix(-10, -24, u), mix(34, -30, u), 0], head: [-14, mix(-28, 22, u), 0]})),
    K(27, {...Bz(0, -16, -84, -1, {gF: .3, gB: -10, gE: 0, gD: .7, gL: .6}), tw: 40, tor: [-12, -10, 0], head: [-12, 8, 0], rh: .4}), K(30, GUARD, 'io'), K(33, {...GUARD, pos: [0, .82, 0], tor: [0, 2, 0]}),
    K(34, GUARD), K(36, {rot: [-10, 0, 0], tor: [-2, 0, 0], head: [-10, -2, 0], ...Bz(0, 0, -64, -1, {gF: 0, gB: 0, gE: -37, gD: .78}), tw: 90, rh: 1, lf: .8, pos: [0, .62, 0], fL: [.12, .56, .1], fR: [-.12, .5, .18], hairS: .5,
      skW: -.5}, 'i'),
    K(37, {rot: [-12, 0, 0], ...Bz(0, 0, -50, -1, {gF: 0, gB: 0, gE: -34, gD: .72}), tw: 60, tor: [-12, 0, 0], lf: .6, pos: [0, .34, 0], fL: [.13, .4, 0], fR: [-.13, .36, .1]}, 'l'),
    K(38, {rot: [-8, 0, 0], ...Bz(0, 0, -36, -1, {gF: 0, gB: 0, gE: -30, gD: .66}), tw: 30, lf: .4, pos: [0, 0, 0], tor: [-24, 0, 0], head: [4, 0, 0], fL: [.2, .22, -.16], fR: [-.2, .2, .2]}, 'l'),
    K(40, {...LOW, rot: [0, 0, 0], lf: 0, ...Bz(0, 0, -30, -1, {gL: .6}), rh: 1, pos: [0, -.46, -.04], tor: [-34, 0, 0], head: [10, 0, 0], hairS: 0, skW: 0}, 'i'),
    K(44, {pos: [0, -.44, -.04], tor: [-30, 0, 0], rh: .5}), K(46, {pos: [0, -.48, -.02], tor: [-32, 4, 0], rh: 0, hR: 'open', ...Bz(20, 0, -34, -1, {gL: .56})}),
    K(48, {pos: [0, .06, 0], tor: [6, 4, 0], head: [-8, 0, 0], lf: .5, fL: [.12, .2, -.04], fR: [-.12, .18, .08], ...Bz(0, 0, 30, -1, {gL: .6}), aR: [50, 50, .95], hairS: -.5, skW: .4}, 'o'),
    K(52, SKY, 'o'), K(62, {...SKY, pos: [0, .36, 0], tor: [8, -6, 0]}), K(67, {...SKY, pos: [0, .37, 0], tor: [9, -6, 0], head: [-20, 6, 0]}), K(71, {...SKY, pos: [0, .38, 0], tor: [10, -4, 0]}),
    K(72, {...Bz(0, 0, 84, -1, {gL: .68}), tw: 90, tor: [6, 0, 0]}, 'i'), K(73, {...Bz(0, 0, 30, -1, {gL: .68}), tw: 45, tor: [-8, 4, 0], head: [-18, 0, 0]}, 'l'),
    K(74, {...Bz(0, 0, -32, -1, {gL: .66}), tor: [-18, 8, 0], head: [-14, -4, 0], aR: [-20, 50, .95]}, 'l'), K(75, {...Bz(0, 0, -40, -1, {gL: .64}), tor: [-20, 8, 0]}, 'o'),
    K(78, {pos: [0, .34, 0], tor: [-18, 6, 0]}), K(82, {rot: [-4, 0, 0], pos: [0, .1, 0], lf: .6, fL: [.14, .34, -.16], fR: [-.14, .3, .1], tor: [-14, 4, 0], head: [-2, 0, 0], hairS: .5, skW: -.5}, 'l'),
    K(84, {...CROUCH, rot: [0, 0, 0], lf: 0, pos: [0, -.36, 0], tor: [-22, 6, 0], head: [4, -4, 0], ...Bz(30, 0, -34, -1, {gL: .56}), aR: [20, 30, .95], hairS: 0, skW: 0}, 'i'),
    K(88, {pos: [0, -.32, 0], tor: [-18, 6, 0]}), K(96, ST2)],
    {src: 'v 247.8-258.2 (P-q; ref hr_grab_4fps 247.80-257.80): the throw upward, the diagonal beam 252.80, the dive 254.00, she floats high 256.4, the pillar 257.40'});
}
// ---- the cinematic placeholder (S2b replaces it with tools/scarlet_cine.mjs): every cine clip holds a static pose with the
// contract's length and events; the looks keyed where the plan's table says (hat / sword / scabbard / face) -----------------------
const P = (name, pose, extra = {}) => ({name, keys: [K(0, pose), K(1, pose)], placeholder: true, note: 'placeholder (S2b: tools/scarlet_cine.mjs)', ...extra});
// HR rebuild (hr_design §4.1): the cinematic clips of the new contract (the three lead-ins replace sq1 / lead_down / lead_stand).
// build_scarlet_rig.mjs uses an entry while scarlet_cine.mjs (lane H2c) does not author that clip at the contract's length.
export const CINE_PLACEHOLDER = [
  P('intro', H_POSE),
  P('intro_end', ST),
  P('cs1', {...ST, ...CROUCH}),
  P('lead60', ST),
  P('lead5', ST),
  P('lead_re', ST),
  P('repel', LOCK),
  P('ending', H_POSE),
];
// ---- export --------------------------------------------------------------------------------------------------------------------
export const CLIPS = clips;
export const accumulate = (c, defaults = DEFAULT_POSE) => accumulateLib(c, defaults);
export const sampleClip = (c, t, ks, defaults = DEFAULT_POSE) => sampleLib(c, t, ks, {defaults, discrete: DISCRETE,
  phase: (cl, x) => (cl.loop ? x / cl.len : x / 40) % 1});
export const restPose = () => ({...structuredClone(DEFAULT_POSE), ph: 0});
