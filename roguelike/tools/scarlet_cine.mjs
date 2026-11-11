// The 8 cinematic clips of the 홍련 (Scarlet) rig, rebuilt for the 11-11 cutscenes (OWNER: lane H2c; contract
// tools/dev/plan/combat/hr_design.md §3 (the shot tables), §4.1 (names, lengths, event ticks, hand-over poses), §4.3 (contacts), §8).
// tools/build_scarlet_rig.mjs imports it: CLIPS (the eight clip objects), CONTRACT (the §4.1 table this file is authored to: the
// builder cross-checks it against api.py and, until H1's api.py carries it, builds to it), ROOTS / rootAt (her root in the stage
// frame per sequence tick, as §3 moves her: what the poses are choreographed to), CONTACTS (§4.3, her side: a build gate) and
// SEQ_OF. The builder writes her points per clip tick in the stage frame to tools/dev/sim/hr/cine/her_tracks.json (for
// test_contact.py and the shot renders). Format, pose channels and helpers: tools/scarlet_rig_api.md §5-§6, tools/scarlet_pose.mjs.
//
// Root motion is never in a clip: the sequences (H2's tools/mboss_scarlet/seq.py) move and turn the body (mboss/mv/glide|leap, rig
// face/*); the clips pose her about the anchor, time their motion to the contract events and key the hat / sword / scabbard / face /
// hands / cup / bottle states at their own ticks. Walks are walks in place whose planted foot travels back at the body's glide
// speed. Hand-overs (§4.1): intro 1290 = intro_end 0 (crouched from the landing, hat low); intro_end 150 = idle; cs1 720 = lead60 0
// (rising from the post-slash crouch); lead60 / lead5 / lead_re end in g_brim's hold (g_tell starts from it); repel 0 = g_dive's
// last pose (head down, blade down); repel 129 = ending 0 (on her back, her right hand on the hat beside her); repel 140 = idle2;
// ending 1372 = H_POSE (tick 0 of ev_give / ev_toast).
//
// Native keys: the clips of this rig are authored on S2a's 2.55-b skeleton and retargeted per sample (scarlet_retarget.mjs). The
// contacts are points in blocks, so the helpers below write channels that land on native targets after the retarget: nP (the
// pelvis offset), nF (a sole), nH (a planted hand), blade() (the sword's grip point and direction in the rig frame; `gN 1` tells
// the retarget that gD is already native).
import {K, B, SW, ST, ST2, CROUCH, LOW, AIR, LOCK, DOWN, H_POSE, DEFAULT_POSE, F_ST, F_WIDE, F_LUNGE, F_TOG} from './scarlet_clips.mjs';
import {hipDirChannels, bladeChannels, S_LEG, K_ARC, HAT_REST} from './scarlet_retarget.mjs';
import {SK, HIP_Y, bladeQ} from './scarlet_pose.mjs';
import {q as quat} from './mboss_rig_math.mjs';

const DEG = Math.PI / 180;
// a flip about her centre of mass (c b above the pelvis pivot): the pelvis offset keeping it in place at pitch pt; y0 lifts it
const flipPos = (pt, c = .5, y0 = 0) => [0, +(y0 + c * (1 - Math.cos(pt * DEG))).toFixed(3), +(-c * Math.sin(pt * DEG)).toFixed(3)];
// the clips' base pose: DEFAULT_POSE + gN (0: gD in S2a units, retargeted; 1: gD native, blocks)
// (round W: lipL / botW / botH = the bottle at her lips, scarlet_pose.mjs; 0 everywhere but the CS1 drink)
const BASE = {...DEFAULT_POSE, gN: 0, lipL: 0, botW: 0, botH: 0};
const FULL = p => ({...BASE, ...p});               // a key that resets every channel (hand-over poses)

// ---- the contract (hr_design.md §4.1; 'end' = the length) ----------------------------------------------------------------------
export const CONTRACT = {
  intro: {len: 1290, events: {l1: 258, take_bottle: 326, pour: 352, l2: 340, bottle_down: 414, l3: 462, raise: 470, l4: 540, drink: 600, l5: 690,
    cup_down: 700, grip: 756, glint: 764, stand: 792, l6: 838, turn: 840, l7: 906, smile: 912, l8: 980, off_rock: 1040, l9: 1044, walk: 1052, l10: 1140,
    stop: 1148, tip: 1160, crouch: 1230, leap: 1234, land: 1258}},
  intro_end: {len: 150, events: {l11: 4, brim: 40, smile: 60, draw: 66, stance: 90, music: 130}},
  cs1: {len: 720, events: {lunge: 6, lock: 10, push: 30, leap: 34, land: 50, l13: 110, sheathe: 200, bottle: 216, l14: 232, hat_off: 240, hat_on: 258,
    smile: 280, raise: 300, offer: 404, drink: 458, props_off: 500, wipe: 506, l15: 578, iai: 610, l16: 618, draw: 642, slash: 650, recolour: 660, music: 676}},
  lead60: {len: 56, events: {rise: 0, stand: 20, brim: 40}},
  lead5: {len: 116, events: {stagger: 0, back: 8, refill: 60, glow: 84, brim: 100}},
  lead_re: {len: 60, events: {refill: 10, brim: 44}},
  repel: {len: 140, events: {lock: 0, heave: 22, wide: 26, grab: 36, strike: 49, cut1: 56, cut2: 62, hook: 70, throw: 78, hat_off: 84, over: 88, land: 101,
    lie: 104, kick: 129, roll: 133, hat_on: 139}},
  ending: {len: 1372, events: {up: 6, hat_on: 20, raise: 28, lunge: 50, graze: 52, lock: 56, burst: 70, shove: 80, back: 116, run: 150, clash: 190, rise: 204,
    a1: 228, a2: 262, a3: 286, a4: 298, off: 304, fly: 314, land: 334, scab_up: 388, swing: 398, l17: 420, music: 420, sheathe: 426, sheathed: 452, l18: 486,
    l19: 628, head_down: 640, turn: 650, l20: 716, look_back: 760, hand: 800, l21: 910, gaze: 990, pivot: 1072, l22: 1082, walk: 1094, stop: 1154,
    gesture: 1160, brim: 1216, l23: 1230, eyes: 1240, pull: 1290, open: 1360}},
};
const E = Object.fromEntries(Object.entries(CONTRACT).map(([n, c]) => [n, {...c.events, end: c.len}]));

// ---- her root in the stage frame (hr_design.md §3: ST(r, u, f), origin = the avatar's feet, f toward her, r to the actor's right) --
// What the poses are choreographed to: the sequence moves her (mv/glide: linear over its ticks; mv/leap: + a parabola of apex h at
// mid-move; a move started at #sq a over n ticks stands at (s - a) / n at #sq s). yaw 0 faces +f, 180 faces the actor.
// [t0, t1, from, to, h, yaw0, yaw1]: #sq ticks; a row holds its end until the next one starts.
const R = (t0, t1, from, to = from, h = 0, y0 = 180, y1 = y0) => ({t0, t1, from, to, h, y0, y1});
// (HF-B, HB-01) the throw's root arc (= seq.py `toss`, leap h in tenths): low, so her body goes over the actor's shoulder, not over
// its head (her pelvis rides THROW.P, the actor's hands hold her sword forearm on THROW.G)
export const THROW_H = .6;
export const ROOTS = {
  // CS0 (§3.1): seated at f 20.73 facing the moon; turned to the actor 840-880; walks 1052-1148 to f 13.5; the leap 1234-1258 to 6.5
  intro: [R(0, 840, [0, 0, 20.73], undefined, 0, 0), R(840, 880, [0, 0, 20.73], undefined, 0, 0, 180), R(880, 1052, [0, 0, 20.73]),
    R(1052, 1148, [0, 0, 20.73], [0, 0, 13.5]), R(1234, 1258, [0, 0, 13.5], [0, 0, 6.5], 4.5), R(1258, 1440, [0, 0, 6.5])],
  // CS1 (§3.2): f 9.0; the lunge 6-10 to 1.5; the leap back 34-50 (apex 1.2) to 9.0
  cs1: [R(0, 6, [0, 0, 9]), R(6, 10, [0, 0, 9], [0, 0, 2.25]), R(34, 50, [0, 0, 2.25], [0, 0, 9], 1.2), R(50, 720, [0, 0, 9])],
  // the repel (§3.4): 1 b above ST(0, 0, 1.0), down to f 1.3 by 6; yanked in to 1.1 (30-36); staggers to 1.2 (56-64); thrown 78-101 over
  // the actor's shoulder (HF-B: a low arc, apex THROW_H; her pelvis rides its own path over the shoulder) to 3.0; kicked 129:
  // slides to 8.0 by 135, on to 9.0 by 140 (at 5 % the sequence ends at 129: the ending)
  repel: [R(0, 6, [0, 1, 1], [0, 0, 1.95]), R(30, 36, [0, 0, 1.95], [0, 0, 1.1]), R(56, 64, [0, 0, 1.1], [0, 0, 1.2]), R(78, 101, [0, 0, 1.2], [0, 0, 3], THROW_H),
    R(129, 135, [0, 0, 3], [0, 0, 8]), R(135, 140, [0, 0, 8], [0, 0, 9])],
  // the ending (§3.5; ST, from E8 = 338 on ST2 with her landing mark 9.0 b ahead; = lane H2's seq.py moves): placed on her back at
  // 4.8 at tick 0 (under the seam's white); up to 5.2 (6-22); the lunge to 3.5 (50-54: at the graze tick 52 she is half way, 4.35);
  // shoved to 6.6 (80-86); springs back to 11 (116-136, apex 1.2); runs in to 4.75 (150-188); round W: the exchange on the ground
  // (the aerial duel is gone): a step in to 4.35 for the overhead (254-262) and back (266-274); pushed off to 5.3 (304-310); a low
  // spring back 314-334 (apex 1.0) to the mark 9.0; turned away 650-700, back to the actor 1072-1094; walks in 1094-1154 to 4.5
  ending: [R(0, 6, [0, 0, 4.8]), R(6, 22, [0, 0, 4.8], [0, 0, 5.2]), R(50, 54, [0, 0, 5.2], [0, 0, 3.5]), R(80, 86, [0, 0, 3.5], [0, 0, 6.6]),
    R(116, 136, [0, 0, 6.6], [0, 0, 11], 1.2), R(150, 188, [0, 0, 11], [0, 0, 4.75]), R(254, 262, [0, 0, 4.75], [0, 0, 4.35]), R(266, 274, [0, 0, 4.35], [0, 0, 4.75]),
    R(304, 310, [0, 0, 4.75], [0, 0, 5.3]), R(314, 334, [0, 0, 5.3], [0, 0, 9], 1.0),
    R(650, 700, [0, 0, 9], undefined, 0, 180, 360), R(700, 1072, [0, 0, 9], undefined, 0, 0), R(1072, 1094, [0, 0, 9], undefined, 0, 0, 180),
    R(1094, 1154, [0, 0, 9], [0, 0, 4.5]), R(1154, 1372, [0, 0, 4.5])],
};
// the sequence and the #sq tick of each clip's tick 0 (the lead-ins are not staged: the fight is open there)
export const SEQ_OF = {intro: {seq: 'intro', t0: 0}, intro_end: {seq: 'intro', t0: 1290}, cs1: {seq: 'cs1', t0: 0}, repel: {seq: 'repel', t0: 0},
  ending: {seq: 'ending', t0: 0}};
export function rootAt(clip, t) {
  const s = SEQ_OF[clip]; if (!s) return null;
  const rows = ROOTS[s.seq], T = s.t0 + t;
  let r = rows[0];
  for (const x of rows) if (T >= x.t0) r = x;
  const u = Math.max(0, Math.min(1, (T - r.t0) / Math.max(1, r.t1 - r.t0)));
  const p = r.from.map((a, i) => a + (r.to[i] - a) * u);
  p[1] += 4 * r.h * u * (1 - u);
  return {p, yaw: r.y0 + (r.y1 - r.y0) * u};
}
// stage <-> rig for a root (rig frame: +X her left, +Y up, -Z forward)
const toRig = (Rt, S) => { const a = Rt.yaw * DEG, c = Math.cos(a), s = Math.sin(a), dr = S[0] - Rt.p[0], df = S[2] - Rt.p[2]; return [-dr * c + df * s, S[1] - Rt.p[1], -dr * s - df * c]; };
const rigOf = (clip, t, S) => toRig(rootAt(clip, t), S);

// ---- the contacts (hr_design.md §4.3; her side; tolerance 0.08 b for blades, 0.12 b for hands, feet and her body) -----------------
export const TOL = {blade: .08, body: .12};
// (round W, lane WC: w_brief §4.5 / §4.6) the locks a swordfighter's distance apart (her root 1.3 b beyond K, the actor's hilt 0.55 b
// before it: the torsos >= 1.2 b apart, test_contact.py GAP), and the exchange on the ground instead of the aerial duel (KA1-KA4)
const KP = {K1: [0, 1.45, .95], KR: [0, 1.55, .65], KW: [.15, 1.95, .85], KH: [0, 2.2, 1.1], KS: [.2, 1.5, 1.6], KT1: [.28, 1.4, 2.0], KT2: [0, .25, 3], KK: [0, .35, 2.7],
  KG: [0, 2.05, 2.95], KE2: [0, 1.5, 2.2], KE5: [0, 1.5, 3.45], KA1: [0, 1.45, 3.5], KA2: [0, 1.85, 3.05], KA3: [0, 1.25, 3.55], KA4: [0, 1.5, 3.45]};
const CT = (id, clip, t0, t1, kind, key = id) => ({id, clip, t0, t1, kind, p: KP[key], tol: kind === 'blade' ? TOL.blade : TOL.body});
// (HF-B, HB-01) the mutual rows: her points against the actor's (lane H3's tools/player_motion/cine/manifest.json), so that
// neither side can meet a contact on its own. what: [her point | segment, the actor's point], tol (b); `over`: her pelvis no
// more than `up` b over the actor's right shoulder and within `r` b of it on the floor plane, at its highest tick of t0..t1.
// The same table is in tools/player_motion/cine/clips.mjs (MUTUAL) and tools/dev/sim/hr/tests/test_contact.py.
export const MUTUAL = [
  {id: 'KW.grip', clip: 'repel', t0: 36, t1: 48, her: 'hand_l', actor: 'hand_l', tol: .2},
  {id: 'KH.hilt', clip: 'repel', t0: 49, t1: 49, her: 'hat_crown', actor: ['pommel', 'hilt'], tol: .2},
  {id: 'KS.hook', clip: 'repel', t0: 70, t1: 78, her: ['elbow_l', 'hand_l'], actor: 'shoulder_r', tol: .3},
  {id: 'KT.grip_l', clip: 'repel', t0: 86, t1: 91, her: ['elbow_l', 'hand_l'], actor: 'hand_l', tol: .15},
  {id: 'KT.grip_r', clip: 'repel', t0: 78, t1: 96, her: ['elbow_l', 'hand_l'], actor: 'hand_r', tol: .15},
  {id: 'KT.over', clip: 'repel', t0: 84, t1: 92, over: true, up: .6, r: .5},
  {id: 'KK.kick', clip: 'repel', t0: 129, t1: 129, her: 'pelvis', actor: 'foot_r', tol: .5},
];
export const CONTACTS = [
  CT('K1', 'cs1', 10, 30, 'blade'), CT('KR', 'repel', 0, 26, 'blade'), CT('KW', 'repel', 36, 48, 'hand_l'), CT('KH', 'repel', 49, 49, 'hat_crown'),
  CT('KS', 'repel', 70, 78, 'forearm_l'), CT('KT.over', 'repel', 88, 88, 'pelvis', 'KT1'), CT('KT.land', 'repel', 101, 101, 'pelvis', 'KT2'),
  CT('KK', 'repel', 129, 129, 'body'), CT('KG', 'ending', 52, 52, 'brim'), CT('KE2', 'ending', 56, 80, 'blade'), CT('KE5', 'ending', 190, 204, 'blade'),
  CT('KA1', 'ending', 228, 228, 'blade'), CT('KA2', 'ending', 262, 262, 'blade'), CT('KA3', 'ending', 286, 286, 'blade'), CT('KA4', 'ending', 298, 304, 'blade'),
];

// ---- native keys ---------------------------------------------------------------------------------------------------------------
// the pelvis offset in blocks while she stands (lf 0: the retarget scales it by S_LEG); airborne / lying keys (lf >= .8) are native
const nP = (x, y, z) => [+(x / S_LEG).toFixed(4), +(y / S_LEG).toFixed(4), +(z / S_LEG).toFixed(4)];
// ... between (lf .3 .. .8) the retarget's own factor: a native offset there is pos / kOf(lf)
const kOf = lf => { const u = Math.max(0, Math.min(1, (lf - .3) / .5)); return S_LEG + (1 - S_LEG) * u * u * (3 - 2 * u); };
// a sole target in blocks (the yaw frame, from the floor point under the pelvis; y 0 = planted)
const nF = (side, x, y, z) => { const s = side === 'L' ? 1 : -1; return [+((x - s * SK.hipJ[0]) / S_LEG + s * .105).toFixed(4), +(y / S_LEG + .1).toFixed(4), +(z / S_LEG).toFixed(4)]; };
// a planted hand target in blocks (the yaw frame, from the floor point under the pelvis)
const nH = (x, y, z) => [+(x / S_LEG).toFixed(4), +(y / S_LEG).toFixed(4), +(z / S_LEG).toFixed(4)];
const vsub = (a, b) => a.map((x, i) => x - b[i]), vadd = (a, b) => a.map((x, i) => x + b[i]), vmul = (a, k) => a.map(x => x * k);
const vlen = a => Math.hypot(...a), vunit = a => vmul(a, 1 / vlen(a));
// the sword held with its grip centre at G pointing along dir (rig frame, blocks), the edge toward `edge`, for a pose whose pelvis
// offset is posN (native blocks, as nP takes it) and whose pelvis yaw is yaw: the grip-sphere channels (gF 0, gN 1)
function blade(G, dir, {pos = [0, 0, 0], yaw = 0, edge = [0, -1, 0]} = {}) {
  const Rp = [pos[0], HIP_Y + pos[1], pos[2]], d = vunit(dir);
  const e = Math.abs(d[0] * edge[0] + d[1] * edge[1] + d[2] * edge[2]) > .98 ? [0, 0, -1] : edge;
  const ch = bladeChannels(G, bladeQ(d, e), Rp, quat([0, yaw, 0]));
  return {gF: 0, gN: 1, gB: +ch.gB.toFixed(2), gE: +ch.gE.toFixed(2), gD: +ch.gD.toFixed(4), cB: +ch.cB.toFixed(2), cR: 0, th: +ch.th.toFixed(2), ed: -1, tw: +ch.tw.toFixed(2)};
}
// a direction turned from a to b (unit vectors) by the fraction u of the angle between them
function slerpDir(a, b, u) {
  const A = vunit(a), Bv = vunit(b), c = Math.max(-1, Math.min(1, A[0] * Bv[0] + A[1] * Bv[1] + A[2] * Bv[2])), w = Math.acos(c);
  if (w < 1e-4) return A;
  const s0 = Math.sin((1 - u) * w) / Math.sin(w), s1 = Math.sin(u * w) / Math.sin(w);
  return A.map((x, i) => x * s0 + Bv[i] * s1);
}
// ... through the point Kp at distance d from the grip (a contact: the blade's centre line passes Kp)
const bladeThru = (G, Kp, o) => blade(G, vsub(Kp, G), o);

// a key list built in any order, sorted by tick; duplicate ticks merge (later wins per channel)
function Keys() {
  const m = new Map();
  const api = {
    k(t, pose, ease = 'io') {
      if (!Number.isInteger(t) || t < 0) throw new Error(`key tick ${t}`);
      const o = m.get(t);
      m.set(t, o ? [t, {...o[1], ...pose}, ease] : [t, pose, ease]);
      return api;
    },
    all(list) { for (const [t, p, e] of list) api.k(t, p, e); return api; },
    done(len) {
      const ks = [...m.values()].sort((a, b) => a[0] - b[0]);
      if (ks[0][0] !== 0 || ks[ks.length - 1][0] !== len) throw new Error(`keys must run 0..${len}`);
      return ks;
    },
  };
  return api;
}

// ---- shared pieces -----------------------------------------------------------------------------------------------------------
// the sheathed sword at the right hip, the left arm free
const SHEATHED = {hold: 0, sword: 'sheathed', scab: 'hip', hL: 'open'};
// the sheathed sword carried in the right hand by the throat (the mouth / hilt forward of the hand), trailing back at her side
const CARRY = {scab: 'hand', hR: 'grip', scB: 172, scE: -16, scR: 0, scOff: .2, aR: [14, 16, .95], hsR: 0, pR: [.55, -.35, .75]};
// raised upright before her right shoulder (hilt up; PLAN §3.1 E10 = intro_end 0)
const UPRIGHT = {scab: 'hand', hR: 'grip', scB: 18, scE: -68, scR: 0, scOff: .25, aR: [84, -8, .62], pR: [.6, -.4, .4], hsR: 0};
// the hip scabbard (scarlet_pose SK.scabHipDir, edge up) as a hand bearing / elevation / roll and the throat grip: the hip <->
// hand hand-over key (S2d: derived from the skeleton, scarlet_retarget.mjs hipDirChannels, so the hand-overs have no jump)
const HIP_DIR = hipDirChannels();
// g_brim's hold (the right hand at the brim; S2a's BR) = the end pose of sq1 / lead_down / lead_stand (g_tell starts from it)
const BRIM_R = {...ST2, hR: 'brim', bwR: 1, bzR: 30, pR: [.8, -.2, .3], head: [-8, -6, 0], hat: 'worn'};
// the iai stance under the brim (CS1 C4-C5): the left hand on the sheathed hilt at the right hip, the right on the throat
const IAI = {...ST, pos: [0, -.26, 0], ...F_WIDE, fL: [.27, .1, -.34], fR: [-.25, .1, .3], tor: [-18, -22, 0], head: [-20, 18, 0],
  ...SHEATHED, hL: 'grip', hR: 'grip', hiL: 1, hsR: 1, aL: [40, 10, .8], aR: [20, 10, .8], skF: 1.1};
// the twisted post-slash crouch of 홍련일섬 (CS1 C8 = sq1 0): the blade swept out low to her left, the body twisted
const SLASHED = {...ST, pos: [0, -.42, 0], fL: [.32, .1, -.4], fR: [-.26, .1, .36], tor: [-24, -44, 0], head: [-4, 30, 0], hold: 1,
  sword: 'hand', scab: 'hip', hL: 'grip', hR: 'open', gF: 0, gB: -112, gE: -28, gD: .72, cB: -118, cR: 0, th: -14, ed: -1, tw: 0, rh: 0,
  aR: [40, 40, .9], hiL: 0, hsR: 0, hairS: -.3, skW: .3};

// a walk in place over (t0, t1] (the sequence glides the body at 2 s / (P / 2) b/t): contacts every P / 2 (left foot forward at
// t0), keys every P / 4, linear so a planted foot travels back at the glide speed; the free left arm swings against the legs
function walk(t0, t1, {P = 16, s = .6, armL = true, lean = -4} = {}) {
  const q = P / 4, out = [];
  for (let i = 1, t = t0 + q; t <= t1; i++, t += q) {
    const ph = i % 4;
    const legs = [
      {fL: [.12, .1, -s], fR: [-.12, .12, s * .85], pos: [0, -.07, 0], rot: [0, -3, 0]},
      {fL: [.12, .1, 0], fR: [-.12, .27, -.05], pos: [0, -.02, 0], rot: [0, 0, 0]},
      {fL: [.12, .12, s * .85], fR: [-.12, .1, -s], pos: [0, -.07, 0], rot: [0, 3, 0]},
      {fL: [.12, .27, -.05], fR: [-.12, .1, 0], pos: [0, -.02, 0], rot: [0, 0, 0]},
    ][ph];
    const sw = [-1, 0, 1, 0][ph];
    out.push([t, {...legs, tor: [lean, 4 * sw, 0], ...(armL ? {aL: [16 * sw, 8, .97]} : {})}, 'l']);
  }
  return out;
}
// side steps to her right (dir -1) or left (1) over (t0, t1], one step every P / 2 (the sequence glides the body sideways)
function side(t0, t1, {P = 16, w = .34, dir = -1} = {}) {
  const q = P / 4, out = [];
  const lead = dir < 0 ? 'fR' : 'fL', trail = dir < 0 ? 'fL' : 'fR', sx = dir;
  for (let i = 1, t = t0 + q; t <= t1; i++, t += q) {
    const ph = i % 4;
    const k = [
      {[lead]: [sx * .14, .1, 0], [trail]: [-sx * .14, .1, 0], pos: [0, -.08, 0]},                 // together
      {[lead]: [sx * (.14 + w), .2, 0], [trail]: [-sx * (.14 - w / 2), .1, 0], pos: [0, -.05, 0]},  // the lead foot steps out
      {[lead]: [sx * (.14 + w / 2), .1, 0], [trail]: [-sx * (.14 + w / 2), .1, 0], pos: [0, -.1, 0]}, // wide (both planted)
      {[lead]: [sx * (.14 - w / 2), .1, 0], [trail]: [-sx * (.14 - w), .2, 0], pos: [0, -.05, 0]},  // the trail foot closes
    ][ph];
    out.push([t, k, 'l']);
  }
  return out;
}
// every tick from t0 to t1 (inclusive) a pose from f(u) (u 0..1): big swings keyed every tick
function every(t0, t1, f, ease = 'l') {
  const out = [];
  for (let t = t0; t <= t1; t++) out.push([t, f((t - t0) / Math.max(1, t1 - t0)), ease]);
  return out;
}
const lerp = (a, b, u) => a + (b - a) * u;
const lerp3 = (a, b, u) => a.map((x, i) => +(x + (b[i] - x) * u).toFixed(3));
const sm = u0 => { const u = Math.max(0, Math.min(1, u0)); return u * u * (3 - 2 * u); };      // smoothstep, clamped to 0..1


const clips = [];
const C = (name, keys, extra = {}) => clips.push({name, keys: keys.done(CONTRACT[name].len), base: BASE, ...extra});

// =================================================================================================================================
// The post-slash poses of 홍련일섬 (CS1 S13): SLASHED (the twisted crouch at the slash, the blade swept out low to her left; shared
// pieces) and SLASH_UP, the half-risen pose cs1 ends in at 720 (= lead60 0: she is still coming up from it)
const SLASH_UP = {...SLASHED, pos: [0, -.26, 0], tor: [-14, -26, 0], head: [-4, 18, 0], fL: [.28, .1, -.3], fR: [-.26, .1, .3], gB: -96, gE: -34, gD: .86, cB: -80,
  th: -18, aR: [28, 34, .92], hat: 'worn'};      // (the grip 0.86 out, the blade forward of her left: clear of her body without a guard)

// =================================================================================================================================
// lead60 (56 t; §3.3: after CS1, in the open fight, 9 b from the player): from the half-risen post-slash pose (rise 0) she
// straightens 0-20 into the P2 stance (stand 20), stands off with the blade low 20-40, the right hand rises to the brim 40-46 and
// stays (g_brim's hold; G1's T0 at 56).
{
  const k = Keys().k(0, FULL(SLASH_UP)).k(8, {pos: [0, -.2, 0], tor: [-11, -8, 0], head: [-3, 6, 0], gB: -70, gE: -38, cB: -40, th: -24}, 'io')
    .k(20, {...ST2, hat: 'worn', hR: 'open'}, 'io').k(30, {pos: [0, -.13, 0], tor: [-10, 11, 0]}).k(40, {...ST2})
    .k(46, {...BRIM_R}, 'o').k(51, {...BRIM_R, head: [-9, -7, 0], pos: [0, -.13, 0]}).k(56, {...BRIM_R});
  C('lead60', k, {src: 'v 203.0-205.8 (the stand-off before the lilac flash; cr_pretell_hand: the hand to the brim)'});
}

// =================================================================================================================================
// lead5 (116 t; §3.3: the 5 % floor reached in P2): a staggering step back 0-8 (stagger 0), backs off facing the player 8-60 (back 8:
// the sequence glides her 0.12 b/t; a 16-t backward walk in place, the blade held low before her), settles 60-66 (refill 60: the
// gauge returns), stands 66-84, lifts the blade level before her and looks along it while it glows 84-98 (glow 84: the module's
// blade look), lowers it 98-100, the right hand to the brim 100-106 (brim 100), held to 116 (G2's T0).
{
  const k = Keys().k(0, {...ST2, hat: 'worn'}).k(3, {pos: [0, -.06, .1], tor: [6, 8, 0], head: [8, -8, 0], fR: [-.14, .1, .32], fL: [.14, .2, -.02], aR: [30, 30, .9]}, 'o')
    .k(6, {pos: [0, -.14, .12], tor: [-6, 6, 0], fL: [.15, .1, .16], fR: [-.15, .1, .34], head: [0, -6, 0]}, 'io')
    .k(8, {...ST2, pos: [0, -.1, 0], ...F_ST, aR: [10, 14, .95]}, 'io');
  // backing off 8-60: the walk in place played backward (the planted foot travels forward at the glide speed), guard held
  {
    const fw = walk(8, 60, {P: 16, s: .5, armL: false, lean: -6});
    const legsAt = i => fw[fw.length - 1 - i][1];
    fw.forEach(([t], i) => { const L = legsAt(i); k.k(t, {fL: L.fL, fR: L.fR, pos: L.pos, rot: L.rot, tor: [-7, 8, 0]}, 'l'); });
  }
  k.k(60, {}).k(66, {...ST2}, 'io').k(76, {pos: [0, -.13, 0], tor: [-10, 11, 0]}).k(84, {...ST2})
    .k(90, {gF: 0, gB: -30, gE: 4, gD: .62, cB: 70, cR: 0, th: 4, ed: -1, tw: 80, tor: [-6, -10, 0], head: [-8, 18, 0], aR: [40, -10, .7]}, 'io')
    .k(97, {gB: -32, gE: 6, th: 6, head: [-9, 20, 0]}).k(100, {...ST2}, 'io')
    .k(106, {...BRIM_R}, 'o').k(111, {...BRIM_R, head: [-9, -7, 0], pos: [0, -.13, 0]}).k(116, {...BRIM_R});
  C('lead5', k, {src: 'v 272.0-277.8 (backs off at the floor HP, the gauge refills 275.0, the lilac flash 277.8); cr_pretell_v3: the hand to the brim'});
}

// =================================================================================================================================
// lead_re (60 t; §3.3: a gauntlet restart after a pause / revive, 8 b from the player): the P2 stance, a slow breath (refill 10),
// the right hand to the brim 44-50 (brim 44), held to 60 (T0).
{
  const k = Keys().k(0, {...ST2, hat: 'worn'}).k(10, {pos: [0, -.13, 0], tor: [-10, 11, 0]}).k(24, {pos: [0, -.11, 0], tor: [-8, 9, 0], head: [-3, -6, 0]})
    .k(44, {...ST2}).k(50, {...BRIM_R}, 'o').k(55, {...BRIM_R, head: [-9, -7, 0], pos: [0, -.13, 0]}).k(60, {...BRIM_R});
  C('lead_re', k, {src: 'hr_design §3.3 (the lead5 beats from standing; cr_pretell_v3)'});
}

// =================================================================================================================================
// intro (1290 t = CS0 #sq 0-1290; §3.1 I1-I17; v 0-94.8: ref/cs_intro.jpg). Her root: ROOTS.intro (seated at f 20.73 with her back to
// the actor, facing the moon; turned to the actor 840-880; walks 1052-1148; the leap 1234-1258 to f 6.5).
// I1-I5 0-320 seated on the kit's seat_rock, the cup in her right hand resting on her knee, the sheathed sword at her right hip
//    (the petal on her hand 190-216 is the sequence's); line 1 (258): a slow breath, the head a little up;
// I6 the left hand takes the bottle from the rock (take_bottle 326), lifts it 334-350, pours into the cup 352-384 (pour 352), lowers
//    it 388-404; line 2 (340);
// I7 sets the bottle down 414-424 (bottle_down 414: the kit's rock shows it again at 424), turns the cup in her fingers 430-456;
// I8 raises the cup toward the moon 470-500 (raise 470; line 3 at 462), holds;
// I9 the arm out with the cup 536-590 (line 4 at 540), brings it back 592-600, drinks 600-650 (drink 600: head back), lowers 650-664;
// I10 sets the cup down 700-712 (cup_down 700; line 5 at 690);
// I11 both hands on the sheathed sword at her right hip: the right grips the throat (grip 756), the left thumb slides the blade a
//    hand's width out and back 764-786 (glint 764);
// I12 stands up on the rock 792-820 (stand 792), the hat brim low; line 6 (838); turned to the actor 840-880 (turn 840: the
//    sequence turns the body; the feet step on the stone's top);
// I13 the smile (smile 912; line 7 at 906), a small head tilt 930-950; I14 line 8 (980);
// I15 steps down off the rock 1040-1052 (off_rock 1040; line 9 at 1044), walks 1052-1148 with her right hand on the brim (walk 1052:
//    a 16-t cycle at the sequence's 0.075 b/t; line 10 at 1140), stops (stop 1148), tips the hat back 1160-1180 (tip 1160: her face);
// I16 the crouch (crouch 1230), the leap 1234-1258 (leap 1234: airborne, legs tucked, the hat held low by the brim);
// I17 lands crouched under the hat (land 1258), the left hand on the ground, holds, rises a little 1276-1290 (= intro_end 0).
// the pelvis offset that stands her on the stone's top (0.24 b)
const ROCK_T = .24;
const LANDED = {...ST, ...LOW, pos: [0, -.5, 0], tor: [-30, 6, 0], head: [-18, -4, 0], fL: [.26, .1, -.28], fR: [-.26, .1, .3], ...SHEATHED, hL: 'open', hR: 'brim', bwR: 1, bzR: 30,
  aR: [120, 30, .9], pR: [.8, -.2, .3], aL: [20, 20, .9], hat: 'worn', face: 'calm', cup: 'none', bottle: 'none', gN: 0};
const INTRO_END0 = {...LANDED, pos: [0, -.4, 0], tor: [-24, 6, 0], head: [-20, -4, 0]};
{
  // sitting at her knee height (the stone's top ~0.75 b in S2a units): the pelvis 0.96 b, the knees forward over the planted feet
  const SEAT = {...ST, pos: [0, -.40, .10], rot: [0, 0, 0], tor: [-6, 0, 0], head: [-6, 0, 0], fL: [.12, .1, -.30], fR: [-.12, .1, -.26],
    kL: [.08, 0, -1], kR: [-.08, 0, -1], ...SHEATHED, hR: 'grip', aR: [70, 12, .55], aL: [35, 8, .62], pL: [.55, -.35, .75],
    pR: [.55, -.35, .75], cup: 'hand', bottle: 'none', cupT: 0, botT: 0, skG: .6, plwL: 0, plwR: 0, hsR: 0, hiL: 0, hat: 'worn', face: 'calm', gN: 0};
  const k = Keys().k(0, FULL(SEAT));
  for (let t = 40; t <= 240; t += 80) k.k(t, {tor: [-5, 0, 1]}).k(t + 40, {tor: [-6, 0, 0]});
  k.k(258, {}).k(272, {head: [-2, 4, 0], tor: [-5, 2, 0]}, 'io').k(300, {head: [-6, 0, 0], tor: [-6, 0, 0]}, 'io').k(318, {});
  // I6: the bottle (on the rock at her left): reach 320-326, lift 334-350, pour 352-384, lowered 388-404
  k.k(325, {aL: [24, 34, .8], tor: [-9, -10, -4], head: [-12, -16, 0]}, 'o')
    .k(326, {hL: 'grip', bottle: 'hand', plL: [.5, .84, .04], plwL: 1, tor: [-11, -14, -6]}).k(334, {})
    .k(350, {plwL: 0, aL: [72, -32, .6], tor: [-8, -4, 0], head: [-14, -4, 0], botT: -20}, 'io')
    .k(358, {aL: [76, -36, .58], botT: -58}, 'io').k(384, {aL: [78, -38, .58], botT: -72, head: [-16, -2, 0]})
    .k(388, {}).k(404, {botT: -6, aL: [56, -10, .62], head: [-10, -6, 0]}, 'io');
  // I7: the bottle set down 414-424; the cup turned in her right hand 430-456
  k.k(414, {}).k(423, {plwL: 1, plL: [.5, .84, .04], tor: [-11, -14, -6], head: [-12, -16, 0]}, 'i')
    .k(424, {bottle: 'none', hL: 'open', botT: 0}).k(430, {plwL: 0, aL: [35, 8, .62], tor: [-6, 0, 0], head: [-10, 8, 0]}, 'io')
    .k(438, {cupT: 14, aR: [74, 8, .55]}).k(446, {cupT: -10, aR: [72, 16, .55]}).k(456, {cupT: 0, aR: [70, 12, .55], head: [-6, 0, 0]});
  // I8: the cup raised to the moon 470-500, held
  k.k(470, {}).k(500, {aR: [150, 10, .95], head: [22, 0, 0], tor: [6, 4, 0], cupT: 8}, 'io').k(518, {head: [24, -2, 0], tor: [7, 4, 1]}).k(536, {aR: [152, 8, .96], head: [24, -2, 0], tor: [6, 4, 0]});
  // I9: the arm out with the cup 536-590; the drink (round W: the cup comes to her lips LEVEL 590-602, then the cup and the head
  // tip back together 602-615, held with a second sip 624, both come level again 636-644, lowered 644-664; the rim at her mouth
  // 602-644: the SIP patch of scarlet_retarget.mjs, test_cine D2)
  k.k(560, {aR: [118, 30, .97], head: [10, 8, 0], tor: [2, 8, 0], cupT: 0}, 'io').k(590, {aR: [116, 34, .97], head: [8, 10, 0]})
    .k(600, {aR: [116, -36, .44], cupT: 0, head: [2, 2, 0], tor: [-4, 0, 0]}, 'io').k(603, {})
    .k(615, {aR: [120, -36, .43], cupT: 52, head: [12, 2, 0], tor: [1, 0, 0]}, 'io').k(624, {cupT: 58, head: [13, 2, 0], tor: [2, 0, 0]}, 'io')
    .k(636, {cupT: 54, head: [12, 2, 0], tor: [1, 0, 0]}, 'io').k(644, {cupT: 0, head: [3, 2, 0], tor: [-4, 0, 0]}, 'io')
    .k(664, {aR: [70, 12, .55], cupT: 0, head: [-6, 0, 0], tor: [-6, 0, 0]}, 'io');
  // I10: the cup set down at her right 700-712
  k.k(700, {}).k(706, {aR: [40, 30, .8], tor: [-8, 8, 2]}, 'io').k(711, {plR: [-.5, .84, .06], plwR: 1, tor: [-10, 14, 6], head: [-10, 16, 0]}, 'i')
    .k(712, {cup: 'none', hR: 'open'}).k(722, {plwR: 0, aR: [24, 12, .7], tor: [-8, 2, 0], head: [-8, 2, 0]}, 'io');
  // I11: the right hand to the scabbard's throat 750-756, the left to the hilt 756-764; the blade a hand's width out and back 764-786
  k.k(750, {}).k(756, {hR: 'grip', hsR: 1, tor: [-10, 10, 0], head: [-16, 14, 0]}, 'io').k(763, {hL: 'grip', hiL: 1, tor: [-12, 4, 0]}, 'io')
    .k(764, {sword: 'hand', hold: 1, shW: 1, sh: 1}).k(772, {sh: .86}, 'io').k(780, {sh: .86}).k(786, {sh: 1}, 'io').k(787, {sword: 'sheathed', hold: 0, shW: 0, sh: 0})
    .k(791, {hiL: 0, hsR: 0, hL: 'open', hR: 'open', aL: [30, 8, .7], aR: [30, 8, .7]}, 'io');
  // I12: stands up on the rock 792-820 (the feet drawn up onto its top), the brim low
  k.k(792, {}).k(800, {pos: [0, -.3, .06], tor: [-22, 0, 0], head: [-2, 0, 0], aL: [40, 6, .62], aR: [40, 6, .62], skG: .3}, 'io')
    .k(808, {pos: [...nP(0, ROCK_T - .3, .02)], tor: [-20, 0, 0], fL: nF('L', .13, ROCK_T, .02), fR: nF('R', -.13, ROCK_T * .5, -.2), kL: [.12, 0, -1], kR: [-.12, 0, -1]}, 'io')
    .k(814, {pos: [...nP(0, ROCK_T - .14, 0)], tor: [-12, 0, 0], fR: nF('R', -.13, ROCK_T, -.04), aL: [10, 8, .9], aR: [10, 10, .9], skG: 0}, 'io')
    .k(820, {pos: [...nP(0, ROCK_T - .03, 0)], tor: [-4, 0, 0], head: [-14, 0, 0], aL: [0, 8, .97], aR: [6, 10, .96]}, 'io').k(838, {head: [-12, 0, 0]});
  // the turn 840-880 (the sequence turns the body): four small steps on the stone's top
  const ROCKF = (side, x, lift = 0, z = 0) => nF(side, x, ROCK_T + lift, z);
  k.k(840, {});
  for (let i = 0; i < 4; i++) { const t = 842 + i * 10, sd = i % 2 ? 'R' : 'L', x = i % 2 ? -.13 : .13, ch = i % 2 ? 'fR' : 'fL';
    k.k(t + 3, {[ch]: ROCKF(sd, x, .08)}, 'io').k(t + 7, {[ch]: ROCKF(sd, x, 0, i % 2 ? -.04 : .02)}, 'io'); }
  k.k(880, {head: [-10, 0, 0]}).k(906, {});
  // I13: the smile, a small head tilt 930-950
  k.k(912, {face: 'smile', head: [-6, -4, 4]}).k(930, {}).k(940, {head: [-4, -8, 10]}, 'io').k(950, {head: [-6, -4, 4]}, 'io').k(1030, {face: 'calm', head: [-8, 0, 0]});
  // I15: down off the rock 1040-1052 (the left foot down before it, the right after it), the right hand to the brim
  // (the sole targets are relative to the floor point under the pelvis: REL turns a rig-frame foot into that)
  const REL = (side, A, P) => nF(side, A[0] - P[0], A[1], A[2] - P[2]);
  const STEP = (t, P, L, Rf, x = {}, e = 'io') => k.k(t, {pos: [...nP(...P)], fL: REL('L', L, P), fR: REL('R', Rf, P), ...x}, e);
  k.k(1040, {});
  STEP(1044, [0, ROCK_T - .06, -.1], [.13, ROCK_T + .1, -.3], [-.13, ROCK_T, -.04], {tor: [-8, 0, 0], hR: 'brim', bwR: 1, bzR: 30, aR: [120, 30, .9], pR: [.8, -.2, .3]});
  STEP(1048, [0, -.06, -.36], [.13, 0, -.62], [-.13, ROCK_T, -.04], {tor: [-12, 0, 0]}, 'i');
  STEP(1050, [0, -.06, -.46], [.13, 0, -.62], [-.13, ROCK_T * .6, -.3]);
  STEP(1052, [0, -.04, -.52], [.13, 0, -.62], [-.14, 0, -.44], {tor: [-5, 0, 0], head: [-12, 0, 0]}, 'i');
  // walks 1052-1148 (16-t cycle; the planted foot travels back at the glide speed), the hand on the brim; the first steps bring the
  // pelvis back over the root
  k.all(walk(1052, 1148, {P: 16, s: .5, lean: -5}));
  k.k(1056, {pos: [...nP(0, -.04, -.39)]}, 'l').k(1060, {pos: [...nP(0, -.06, -.26)]}, 'l').k(1064, {pos: [...nP(0, -.03, -.13)]}, 'l');
  k.k(1150, {...F_ST, pos: [0, -.04, 0], rot: [0, 0, 0], tor: [-4, 0, 0], aL: [2, 8, .97], head: [-12, 0, 0]}, 'io');
  // the hat tipped back 1160-1180 (her face, smiling), the hand down 1196-1206
  k.k(1160, {}).k(1180, {head: [8, 0, 0], bzR: 46, aR: [128, 26, .9], face: 'smile', tor: [-2, 0, 0]}, 'io').k(1196, {})
    .k(1206, {hR: 'open', bwR: 0, aR: [6, 10, .96], pR: [.55, -.35, .75], head: [4, 0, 0]}, 'io').k(1226, {face: 'calm'});
  // I16: the crouch 1230, the leap 1234-1258 (airborne), I17 the landing 1258 crouched under the hat, the left hand on the ground
  k.k(1230, {...CROUCH, pos: [0, -.3, 0], tor: [-18, 0, 0], head: [-6, 0, 0], aL: [-20, 14, .9], aR: [-20, 14, .9]}, 'io').k(1233, {pos: [0, -.42, 0], tor: [-24, 0, 0]}, 'io')
    .k(1238, {...AIR, pos: [0, .06, 0], rot: [-8, 0, 0], tor: [4, 0, 0], head: [-10, 0, 0], fL: [.13, .4, -.1], fR: [-.13, .34, .12], lf: .8, aL: [150, 30, .9], hR: 'brim', bwR: 1, bzR: 30,
      aR: [120, 30, .9], pR: [.8, -.2, .3], skW: .6}, 'o')
    .k(1246, {rot: [0, 0, 0], fL: [.13, .56, -.26], fR: [-.13, .5, -.1], aL: [120, 60, .9], tor: [-6, 0, 0], skW: -.2}, 'io')
    .k(1254, {rot: [8, 0, 0], fL: [.14, .36, -.3], fR: [-.14, .3, .1], aL: [60, 50, .9], tor: [-12, 0, 0], head: [-16, 0, 0], skW: -.6}, 'io')
    .k(1258, {...FULL(LANDED), plL: [.3, .16, -.36], plwL: 1, tor: [-50, 10, 0], pos: [0, -.8, 0]}, 'i')
    .k(1262, {pos: [0, -.84, 0]}, 'o')   /* the deep landing crouch: the left palm on the ground 1258-1276 */.k(1276, {pos: [0, -.82, 0], plwL: 1}).k(1290, {...FULL(INTRO_END0)}, 'io');
  C('intro', k, {src: 'v 0-94.8 (ref/cs_intro.jpg; hr_design §3.1 I1-I17): seated with the cup, the bottle poured, the cup to the moon, the drink, the thumb on the guard, up on the rock, the walk with a hand on the brim, the hat tipped, the leap and the landing'});
}

// =================================================================================================================================
// intro_end (150 t = CS0 #sq 1290-1440, the skip's target; §3.1 I18-I20; v 94.8-101.5). From the landing crouch (hat low) she rises
// 0-12 with her right hand still on the brim, speaks under it (l11 4), lifts the brim 40-56 (brim 40: her eyes), the smile (smile
// 60); the left hand crosses to the hilt at her right hip 58-65, the right steadies the scabbard's throat; the cross-draw at 66
// (draw 66; every tick 66-72), the blade brought upright before her 72-88; swung down into the stance 90-110 (stance 90: the sword
// out low to her left, the hat dipping), the scabbard hand let go; settles 110-150 into the fight stance (music 130; 150 = idle).
{
  const UP = {...ST, pos: [0, -.06, 0], tor: [-6, 4, 0], head: [-22, -2, 0], ...F_ST, ...SHEATHED, hR: 'brim', bwR: 1, bzR: 30, aR: [120, 30, .9], pR: [.8, -.2, .3], aL: [4, 10, .96], hat: 'worn'};
  const k = Keys().k(0, FULL(INTRO_END0)).k(12, {...UP}, 'io').k(26, {head: [-20, 0, 0], tor: [-5, 4, 0]}).k(40, {})
    .k(56, {head: [-2, 0, 0], bzR: 46, aR: [128, 26, .9], tor: [-3, 2, 0]}, 'io').k(58, {})
    .k(60, {face: 'smile', aL: [40, 34, .8]}).k(65, {hR: 'grip', bwR: 0, hsR: 1, aR: [20, 10, .8], hL: 'grip', hiL: 1, tor: [-10, -18, 0], head: [-8, 12, 0], pos: [0, -.14, 0]}, 'io');
  // the draw 66-72: the blade out of the hip scabbard up to her right, then round to upright before her (every tick)
  k.k(66, {sword: 'hand', hold: 1, hiL: 0, shW: 1, sh: 1, gF: 0, gB: 40, gE: -24, gD: .5, cB: 150, cR: 0, th: -10, ed: -1, rh: 0, hsR: 1}, 'l');
  k.all(every(67, 72, u => ({shW: +lerp(.7, 0, Math.min(1, u * 1.5)).toFixed(2), sh: +lerp(.5, 0, Math.min(1, u * 2)).toFixed(2), gB: +lerp(30, 0, u).toFixed(1), gE: +lerp(-20, 6, u).toFixed(1),
    gD: +lerp(.52, .58, u).toFixed(2), cB: +lerp(120, 10, u).toFixed(1), th: +lerp(4, 84, u).toFixed(1), tor: [+lerp(-10, -4, u).toFixed(1), +lerp(-18, 0, u).toFixed(1), 0],
    head: [-6, +lerp(12, 0, u).toFixed(1), 0], pos: [0, +lerp(-.14, -.06, u).toFixed(3), 0]})));
  k.k(76, {gB: 0, gE: 8, gD: .58, cB: 0, th: 90, hsR: 1}, 'io').k(88, {gE: 10, th: 92, head: [-4, 0, 2]});
  // the stance 90-110: the blade swept down to her left (every tick 90-100), the hat dipping, the right hand off the scabbard
  k.all(every(90, 100, u => ({gB: +lerp(0, -32, sm(u)).toFixed(1), gE: +lerp(10, -50, sm(u)).toFixed(1), gD: +lerp(.58, .6, u).toFixed(2), cB: +lerp(0, 38, sm(u)).toFixed(1),
    th: +lerp(92, -40, sm(u)).toFixed(1), tor: [+lerp(-4, -10, Math.sin(u * Math.PI)).toFixed(1), +lerp(0, 6, u).toFixed(1), 0], head: [+lerp(-4, -18, Math.sin(u * Math.PI)).toFixed(1), +lerp(0, -4, u).toFixed(1), 0],
    hsR: +lerp(1, 0, u).toFixed(2), pos: [0, +lerp(-.06, -.12, Math.sin(u * Math.PI)).toFixed(3), 0]})));
  k.k(104, {hR: 'open', aR: [6, 10, .96], face: 'calm'}, 'io').k(110, {...ST, hat: 'worn', hiL: 0, hsR: 0, shW: 0, sh: 0}, 'io').k(130, {pos: [0, -.06, 0], tor: [-5, 7, 0]}).k(150, {...FULL(ST)});
  C('intro_end', k, {src: 'v 94.8-101.5 (ref/cs_intro.jpg I18-I20; hr_design §3.1): under the brim, the brim lifted, the cross-draw, the blade upright, the stance'});
}

// =================================================================================================================================
// The lock of the ground clashes (§3.0 "Clash contact"): she stands 0.75 b beyond K turned 48 degrees to her right, leaning in, the
// hilt before her chest 0.3-0.45 b below K and 0.2-0.3 b beyond it, the blade up through K. G = the grip in the rig frame. The
// design's X has her hilt 0.3 b to the actor's left of K; the actor (H3's manifest) holds its head 0.3-0.45 b to its right of K
// and its blade runs up to its left past her head, so her hilt sits 0.1 b to the actor's RIGHT of K instead: her blade passes the
// actor's head on its left and the actor's blade passes hers (0.05-0.25 b clear of both head boxes; fit_x in hr2c_progress.md);
// from the side cameras the two blades still cross at K
const XL_YAW = 48;
const xLock = (clip, t, Kn, G, pos, x = {}) => ({...ST, pos: nP(...pos), rot: [0, XL_YAW, 0], tor: [-12, 14, 0], head: [-2, -40, 0], fL: nF('L', .22, 0, -.2), fR: nF('R', -.22, 0, .22),
  ...bladeThru(G, rigOf(clip, t, KP[Kn]), {pos, yaw: XL_YAW}), rh: 0, hR: 'open', aR: [20, 40, .8], hat: 'worn', ...x});

// =================================================================================================================================
// cs1 (720 t; §3.2 S1-S13; v 160.5-203.0: ref/cs1_60pct.jpg). Her root: ROOTS.cs1 (f 9.0; the lunge 6-10 to 1.5; the leap back 34-50).
// S1 0-6 the low ready stance; S2 the lunge 6-10 (lunge 6: the sequence glides her 7.5 b; the blade swung round from behind her,
//    every tick), stopped on the actor's blade at K1 at 10 (lock 10), the X lock 10-30 (leaning in; pushes 24-30: push 30);
// S3 shoved off 30-34, the leap back 34-50 (leap 34: airborne, legs tucked), lands low (land 50), the blade low to her left;
// S4 straightens 90-110, the hat on, the sword low; line 13 (110); a small nod 120-140;
// S5 180-220 (off screen: the grass from above): sheathes (sheathe 200: the sword to the hip scabbard, a cut tick), the white
//    bottle into her left hand (bottle 216);
// S6 220-276 (from behind her): line 14 (232); the right hand takes the brim 236, sweeps the hat off and round in a wide arc at
//    arm's length 240-252 (hat_off 240; every tick), sets it back on 256-262 (hat_on 258);
// S7 the smile (smile 280), the bottle raised to shoulder height 300-330 (raise 300);
// S9 the eyes-closed smile 384-400, the bottle offered toward the actor at arm's length 404-430 (offer 404), looks down at it
//    434-452, drinks from the bottle, head back 458-492 (drink 458);
// S10 the bottle gone (props_off 500); wipes her mouth with the right forearm 506-566 (wipe 506), lowers the arm 568-580, the head
//    lowered under the brim; line 15 (578);
// S11 600-610 into the iai stance (iai 610: the left hand on the sheathed hilt at the right hip, the right on the throat), held
//    under the brim 610-641; line 16 (618);
// S12 the draw 642-649 under the overlays (draw 642; every tick): the blade out of the hip scabbard, sweeping round to her left;
// S13 홍련일섬 650 (slash 650): the twisted post-slash crouch, the blade swept out low to her left, held; (recolour 660, music 676);
//    rises half way 700-720 (= lead60 0).
const K1_G = {10: [.1, .99, -.55], 16: [.1, .99, -.55], 24: [.1, 1.0, -.56], 30: [.1, 1.01, -.57]};
const K1_POS = {10: [0, -.1, .06], 16: [0, -.1, .05], 24: [0, -.1, .03], 30: [0, -.09, .01]};
const cs1Lock = (t, G = K1_G[t]) => xLock('cs1', t, 'K1', G, K1_POS[t], {tor: [t >= 24 ? -9 : -6, 14, 0], head: [-2, -40, 0]});
{
  const READY = {...ST2, pos: [0, -.2, 0], tor: [-12, 10, 0], head: [-2, -8, 0], hat: 'worn', scab: 'hip', sword: 'hand'};
  const DASH = {pos: [0, -.18, 0], rot: [-24, 0, 0], tor: [-14, 4, 0], head: [10, -2, 0], fL: [.14, .16, -.5], fR: [-.14, .3, .4], lf: .3,
    ...B(0, 70, -150, 1, {gL: .6}), gN: 0, aR: [-40, 20, .95], hairS: -.8, skW: 1};
  const LOWR = {...ST, ...LOW, rot: [0, 0, 0], lf: 0, pos: [0, -.38, 0], fL: [.3, .1, -.36], fR: [-.28, .1, .34], tor: [-22, 14, 0], head: [6, -10, 0],
    hold: 1, sword: 'hand', hL: 'grip', hR: 'open', gF: 0, gN: 0, gB: -60, gE: -38, gD: .66, cB: -84, cR: 0, th: -24, ed: -1, rh: 0, aR: [30, 40, .9],
    hairS: 0, skW: 0, hat: 'worn'};
  // the lunge 6-9 (the sequence glides her): leaning into it, the blade trailing low behind her left side, swung forward and up
  // into the lock (native blades, every tick; 10 = the lock on K1)
  const LUNGE = (t, pitch, yaw, posN, lf, G, d, x = {}) => k.k(t, {...DASH, rot: [pitch, yaw, 0], lf, pos: posN.map(v => +(v / kOf(lf)).toFixed(4)), ...blade(G, d, {pos: posN, yaw}), ...x}, 'l');
  const k = Keys().k(0, FULL(READY)).k(4, {pos: [0, -.24, 0], tor: [-14, 10, 0]});
  LUNGE(6, -24, 0, [0, -.12, 0], .3, [.42, .8, .28], [-.25, -.2, .95]);
  LUNGE(7, -28, 8, [0, -.12, 0], .3, [.44, .78, .2], [-.1, -.3, .95], {tor: [-16, 4, 0]});
  LUNGE(8, -18, 22, [0, -.13, 0], .15, [.2, .85, -.25], [.7, -.35, .1], {tor: [-15, 8, 0], aR: [10, 20, .9], hairS: -.5, skW: .6});
  LUNGE(9, -8, 36, [0, -.14, 0], 0, [-.2, 1.0, -.45], [.62, .1, -.78], {tor: [-14, 12, 0], aR: [20, 30, .85], hairS: -.3, skW: .3});
  for (const t of [10, 16, 24, 30]) k.k(t, {...cs1Lock(t), hairS: t === 10 ? -.2 : 0, skW: t === 10 ? .2 : 0, lf: 0}, t === 10 ? 'l' : 'io');
  // shoved off 30-34: rocked back, the blade knocked up and out to her left
  k.k(32, {pos: nP(0, -.06, .06), rot: [0, 30, 0], tor: [2, 4, 0], head: [4, -24, 0], ...blade([.2, 1.3, -.3], [.3, .8, -.5], {pos: [0, -.06, .06], yaw: 30}), aR: [40, 50, .9]}, 'o')
    .k(34, {...CROUCH, rot: [0, 0, 0], pos: [0, -.26, 0], tor: [-12, 0, 0], head: [-2, -4, 0], gF: 0, gN: 0, gB: -50, gE: -20, gD: .6, cB: -40, cR: 0, th: 30, ed: -1, tw: 0, aR: [30, 40, .9]}, 'io');
  // the leap back 34-50 (airborne, legs tucked) and the landing 50; the low stance held
  k.k(38, {...AIR, pos: [0, .06, .04], rot: [10, 0, 0], tor: [-2, 6, 0], fL: [.13, .55, -.25], fR: [-.13, .5, -.1], lf: .8, ...B(-40, 0, 40, -1, {gL: .58}), aR: [60, 50, .9], hairS: .5, skW: -.6}, 'o')
    .k(44, {rot: [6, 0, 0], fL: [.13, .45, -.3], fR: [-.13, .4, -.15]}).k(50, {...LOWR}, 'i').k(54, {pos: [0, -.4, 0]})
    .k(74, {pos: [0, -.37, 0], tor: [-21, 15, 0]}).k(90, {pos: [0, -.38, 0], tor: [-22, 14, 0]});
  // S4: straightens 90-110 (the sword low), a small nod 120-140
  k.k(110, {...ST2, hat: 'worn', hR: 'open'}, 'io').k(120, {}).k(128, {head: [-12, -8, 0], tor: [-11, 10, 0]}, 'io').k(140, {head: [-2, -8, 0], tor: [-9, 10, 0]}, 'io')
    .k(160, {pos: [0, -.13, 0]}).k(180, {pos: [0, -.12, 0]});
  // S5 (off screen): the sword to the hip scabbard at 200 (cut), the bottle into the left hand at 216; stands easy
  const EASY = {...ST, pos: [0, -.04, 0], tor: [-4, 4, 0], head: [-6, -2, 0], ...F_ST, ...SHEATHED, aL: [6, 10, .96], aR: [6, 10, .96], hat: 'worn', gN: 0};
  k.k(199, {}).k(200, {...EASY}).k(215, {aL: [30, 6, .7]}).k(216, {bottle: 'hand', hL: 'grip', botT: 0, aL: [24, 8, .8]}).k(224, {aL: [14, 10, .9]}).k(232, {});
  // S6: the hat swung off and round (240-252, every tick; the hat at arm's length in the right hand), back on 256-262
  // (HI, hi_todo 11) the head pitched -5 at 236, not -10: the worn brim, pulled by the hand, cleared the head's top corner by
  // -1.7 mm (test_rig `hats: worn`); now >= 1 mm on every tick
  k.k(236, {hR: 'brim', bwR: 1, bzR: 30, aR: [120, 30, .9], pR: [.8, -.2, .3], head: [-5, 6, 0]}, 'io')
    .k(240, {hat: 'hand', hR: 'grip', bwR: 0, hhB: 40, hhE: 30, hhN: [40, 70], aR: [130, 36, .9], head: [-6, 8, 0], tor: [-4, 8, 0]}, 'l');
  // the hand's bearing round her right side (from her front): 40 -> 150 (behind her right shoulder: toward the lens) -> 40, the
  // hat radially beyond the hand, its crown tipped outward as it swings
  k.all(every(241, 252, u => { const w = Math.sin(u * Math.PI), a = lerp(40, 150, w);
    return {aR: [+lerp(124, 92, sm(Math.min(1, u * 3))).toFixed(1), +a.toFixed(1), .97], hhB: +a.toFixed(1), hhE: +lerp(26, 6, w).toFixed(1),
      hhN: [+a.toFixed(1), +lerp(70, 38, w).toFixed(1)], tor: [-4, +lerp(8, 30, w).toFixed(1), 0], head: [-4, +lerp(8, 34, w).toFixed(1), 0]}; }));
  k.k(254, {aR: [130, 34, .92], hhB: 30, hhE: 30, hhN: [30, 74], tor: [-4, 6, 0], head: [-6, 4, 0]}, 'l')
    .k(256, {hhB: 20, hhE: 30, hhN: [0, 80], aR: [150, 20, .9], tor: [-4, 6, 0], head: [-6, 2, 0]}, 'io')
    .k(258, {hat: 'worn', hR: 'brim', bwR: 1, bzR: 24, aR: [120, 30, .9]}).k(262, {head: [-10, 0, 0]}).k(270, {...EASY, bottle: 'hand', hL: 'grip', aL: [14, 10, .9], hR: 'open', bwR: 0}, 'io');
  // S7: the smile, the bottle raised to shoulder height 300-330. The bottle rides the left forearm (its neck in the fist, botT
  // about the elbow's hinge): the elbow kept under the hand (pL down) so botT stands it upright (-120 raised, -90 at arm's length)
  const ELB = [.1, -1, .3];
  k.k(280, {face: 'smile', head: [-4, -4, 4]}).k(300, {pL: ELB}).k(316, {aL: [70, 20, .62], botT: -100, tor: [-3, -4, 0]}, 'io').k(330, {aL: [86, 24, .6], botT: -120, head: [-2, -8, 6]}, 'io')
    .k(360, {aL: [84, 24, .6], head: [-3, -6, 5]}).k(384, {});
  // S9 (round W; the user: "the drinking motion looks odd" - the bottle hung beside her ear with the arm out to the side, after a
  // nod that hid her face under the brim): eyes closed 384-400; the offer 404-430 (the bottle upright at arm's length, a little
  // to her left so the arm is not end-on to the lens); she draws it back 434-446 with a glance at it; lifts it to her lips
  // UPRIGHT 446-457 (lipL: the fist, with the rim a finger above it, comes to her mouth; botW 1: the bottle stands in her head's
  // frame); from the drink event 458 the bottle and the head tip back TOGETHER (botH 0 -> 98: the base swings forward and up
  // about the rim; head 26 back), held 466-486 with two swallows (the sequence's sips 464 / 478); 486-491 both come level again,
  // 491-499 the bottle is lowered. The rim stays within 0.06 b of her mouth point 457-490 (test_cine D1).
  const SIP = (t, h, hd) => k.k(t, {botH: h, head: [hd, 0, 0]}, 'io');
  k.k(384, {face: 'closed', head: [-2, -4, 8]}).k(400, {face: 'smile'}).k(404, {})
    .k(418, {aL: [80, 22, .93], botW: 1, botH: 0, tor: [-6, -8, 0], head: [-4, -6, 2]}, 'io').k(430, {aL: [82, 20, .94]})
    .k(434, {}).k(446, {aL: [74, 16, .62], head: [-8, -6, 0], tor: [-3, -4, 0]}, 'io')
    .k(457, {lipL: 1, aL: [100, -20, .5], pL: [.8, -.75, .15], head: [-1, 0, 0], tor: [-2, 0, 0], face: 'calm'}, 'io').k(458, {});
  SIP(466, 98, 26); SIP(472, 92, 23); SIP(478, 102, 27); SIP(486, 98, 26);
  k.k(466, {tor: [5, 0, 0]}).k(486, {tor: [5, 0, 0]})
    .k(491, {botH: 0, head: [1, 0, 0], tor: [-1, 0, 0]}, 'io').k(492, {lipL: 1})
    .k(499, {lipL: 0, aL: [44, 10, .78], head: [-6, 0, 0], tor: [-4, 2, 0]}, 'io');
  // S10: the bottle gone; the right forearm across her mouth 506-566, lowered 568-580; the head under the brim
  k.k(500, {bottle: 'none', hL: 'open', face: 'calm', aL: [8, 10, .96], pL: [.55, -.35, .75], botT: 0, botW: 0, botH: 0, lipL: 0}).k(506, {}).k(516, {aR: [112, -44, .5], pR: [.8, .3, .3], head: [-14, 10, 0], tor: [-6, 4, 0]}, 'io')
    .k(540, {aR: [112, -14, .5], head: [-14, -8, 0]}, 'io').k(566, {aR: [108, -4, .52], head: [-16, -10, 0]}).k(580, {aR: [6, 10, .96], pR: [.55, -.35, .75], head: [-20, 0, 0], tor: [-8, 0, 0]}, 'io')
    .k(600, {head: [-20, 0, 0]}).k(605, {aL: [40, 30, .8], aR: [20, 24, .9]}, 'io');
  // S11: the iai stance 610, held; S12 the draw 642-649 (every tick); S13 the slash 650
  k.k(610, {...IAI, hat: 'worn'}, 'io').k(626, {head: [-20, 16, 0], tor: [-17, -22, 0]}).k(639, {head: [-22, 18, 0], tor: [-19, -22, 0]})
    .k(641, {pos: [0, -.3, 0], tor: [-20, -26, 0]});
  k.k(642, {sword: 'hand', hold: 1, hiL: 0, shW: 1, sh: 1, gF: 0, gN: 0, gB: 40, gE: -24, gD: .5, cB: 150, cR: 0, th: -10, ed: -1, rh: 0, hsR: 1}, 'l');
  // (round W: the cut is LEVEL at her waist through the petal - the sequence's S11 petal falls onto the blade's line at
  // CUT_T = 647, seq.py - not a sweep along the ground: the grip rises and the point comes up to level 646-648, then both
  // drop into the post-slash crouch; DRAW_GE / DRAW_TH per tick 643..649)
  const DRAW_GE = [-26, -26, -24, -20, -14, -10, -18], DRAW_TH = [-12, -10, -4, 2, 12, 6, -4];
  k.all(every(643, 649, u => ({shW: +lerp(.7, 0, Math.min(1, u * 1.3)).toFixed(2), sh: +lerp(.5, 0, Math.min(1, u * 2)).toFixed(2),
    gB: +lerp(20, -100, u).toFixed(1), gE: DRAW_GE[Math.round(u * 6)], gD: +lerp(.55, .7, u).toFixed(2), cB: +lerp(110, -110, u).toFixed(1), th: DRAW_TH[Math.round(u * 6)],
    tor: [-22, +lerp(-24, -40, u).toFixed(1), 0], pos: [0, +lerp(-.32, -.4, u).toFixed(3), 0], hsR: +lerp(1, 0, u).toFixed(2)})));
  k.k(650, {...SLASHED, hat: 'worn', shW: 0, sh: 0, gN: 0}, 'o').k(656, {tor: [-24, -48, 0]}).k(670, {pos: [0, -.41, 0], tor: [-23, -46, 0], head: [-2, 32, 0]})
    .k(700, {pos: [0, -.42, 0], tor: [-24, -44, 0], head: [-4, 30, 0]}).k(720, FULL(SLASH_UP), 'io');
  C('cs1', k, {cuts: [200, 566, 567], src: 'v 160.5-203.0 (ref/cs1_60pct.jpg; hr_design §3.2): the lunge and the blade lock, shoved apart, the hat swing, the bottle offered and drunk, the mouth wiped, the iai, 홍련일섬'});
}

// =================================================================================================================================
// repel (140 t; §3.4 R0-R9, the same for both gauntlets; v 215.6-222.6: ref/hr_repel_5fps.jpg, gauntlet_repel.jpg). Her root: ROOTS.repel.
// R0 0-6 the dive stopped on the actor's raised blade: from g_dive's last pose (head down, the blade down along the dive) she comes
//    upright as the root drops to the floor at f 1.3, the blade sliding down its length on KR (every tick);
// R1 6-22 side-on and tall, the sword hand high before her face, the blade pressed down across the actor's guard at KR (the forte
//    on it, the point past the actor's right side); 22-26 heaved up and back (heave 22), still on KR;
// R2 26-30 her blade beaten wide to her left (wide 26); 30-36 yanked in (the root to 1.1), the sword wrist seized at KW (grab 36):
//    the arm straight up, side-on, the head tipped away from it, held 36-48;
// R3 49 the hilt on her hat's crown at KH (strike 49): the knees give, the head driven down, reels 49-52;
// R4 52-68 staggers under the two cuts (cut1 56: thrown up and back; cut2 62: folded and turned as the actor passes her right side),
//    still facing the stage origin (the root to 1.2, 56-62);
// R5 68-78 the actor's back against hers: tipped backward, the sword forearm drawn back over the actor's right shoulder at KS (hook 70);
// R6 78-101 pulled over the shoulder (throw 78; every tick): tipped onto its back, head first over the top with the legs flying
//    (over 88: the pelvis at KT.over), the hat off at 84 (hat world: its own arc out to her right, landing with her), falling back
//    to slam onto her back at f 3.0 (land 101: the pelvis at KT.land, the head toward +f);
// R7 101-128 lies on her back (lie 104), the sword along the ground at her left; the right hand lifts weakly 112-118 and falls on the
//    brim of the hat beside her 118-124;
// R8 129 kicked (kick 129: KK on her hip); 129-133 the body jolts and skids on its back (the root slides to 8.0), the right hand
//    takes the hat (hat hand 131);
// R9 133-139 a backward roll onto her feet (roll 133; every tick), the hat back on at 139 (hat_on), into the P2 stance at 140 (= idle2).
const DIVE0 = {...ST, ...AIR, lf: .9, rot: [-60, 0, 0], pos: [0, .9, .2], tor: [-10, 0, 0], head: [-20, 0, 0], ...B(0, 0, -70, -1, {gL: .55}), rh: 1, fL: [.12, .6, .25], fR: [-.12, .56, .3],
  hairS: .6, skW: -.8, hat: 'worn', hR: 'grip'};
// lying after the throw (repel 104-129 = ending 0): DOWN with the hat at the hold spot beside her head and the right hand on its brim
// HOLD_HAND: her right fist on the hat's rim (0.64 in from its centre), as low as a fist lying on the floor goes from any history
// (0.17: repel 129 = ending 0); the elbow out to her side toward her feet (pR), never into the floor
const HAT_HOLD = HAT_REST.hold.t, HOLD_HAND = nH(HAT_HOLD[0] + .64, .17, HAT_HOLD[2] - .02);
const LIE = {...DOWN, hat: 'world', hwP: [...HAT_HOLD], hwE: [0, 20, 0], head: [-10, -18, 0], tor: [2, 0, 0], hR: 'grip', plR: HOLD_HAND, plwR: 1, aR: [20, 60, .9], pR: [-.8, .1, -.4], gN: 0};
// R0-R1 (the rig frame; the root drops to the floor at 6). Tick 0: the dive's body (g_dive's last pose), the sword in the left hand
// alone on the dive's line through KR, its grip clear of her body (g_dive's own two-hand grip sits in her chest: the solver's clear
// guards carry it up to 0.7 b off the line). 1-2 (never shown: the rig blends from g_dive's pose to the key at 3 under the gold
// wash): she comes upright, the blade turning about KR. 3-6: a landing crouch turned 48 degrees to her right (her chest to the
// side camera A stands on), the hilt before her chest and still in the stage, the blade up across the actor's guard at KR, while
// the root comes down to the floor (6); 6-22 she rises into it and leans her weight on the lock; 22-26 heaved back (heave 22).
// The hilt is BELOW KR (design: above it, the blade down): a hand above KR sits under her own 1.3-b hat brim with the pommel
// through it, and a blade pointing down past the guard ends in the actor (hr2c_progress.md).
const LOCK_YAW = 48, LOCK_HS = [.1, 1.09, 1.5];      // (round W: she lands 1.3 b beyond KR, a swordfighter's distance)           // the hilt in the stage through the landing (ST r, u, f)
// [pelvis pitch, yaw, pelvis height above the root, lf, torso, head]
const R0_BODY = {0: [-60, 0, 1.666, .9, [-10, 0, 0], [-20, 0, 0]], 1: [-40, 16, 1.27, .9, [-10, 6, 0], [-14, -10, 0]], 2: [-20, 32, .87, .6, [-12, 12, 0], [-8, -24, 0]],
  3: [0, LOCK_YAW, .47, 0, [-6, 14, 0], [2, -40, 0]], 4: [0, LOCK_YAW, .5, 0, [-6, 14, 0], [2, -40, 0]], 5: [0, LOCK_YAW, .55, 0, [-4, 14, 0], [0, -40, 0]],
  6: [0, LOCK_YAW, .62, 0, [-2, 14, 0], [-2, -40, 0]]};
const R0_GRIP = {0: [.25, 1.73, .1], 1: [.3, 1.4, .05], 2: [.1, .85, -.15]};
function r0Pose(t, G = R0_GRIP[t]) {
  const [pt, yaw, h, lf, tor, head] = R0_BODY[t], w = sm(t / 3), posN = [0, h - HIP_Y, lerp(.2, .06, w)], kk = kOf(lf);
  // (round W: the hilt rides 0.45 b before her root as she lands back from the guard: the stage height of LOCK_HS)
  const Gt = G || rigOf('repel', t, [LOCK_HS[0], LOCK_HS[1], rootAt('repel', t).p[2] - .45]);
  return {rot: [pt, yaw, 0], pos: posN.map(x => +(x / kk).toFixed(4)), lf, tor, head, fL: t >= 3 ? nF('L', .22, 0, -.2) : lerp3([.12, .6, .25], [.16, .3, -.1], w),
    fR: t >= 3 ? nF('R', -.22, 0, .22) : lerp3([-.12, .56, .3], [-.16, .26, .2], w), kL: [.12, 0, -1], kR: [-.12, 0, -1],
    ...bladeThru(Gt, rigOf('repel', t, KP.KR), {pos: posN, yaw}), rh: 0, hR: 'open', aR: t >= 3 ? [20, 40, .8] : [-30, 30, .9], hairS: +lerp(.6, 0, w).toFixed(2), skW: +lerp(-.8, 0, w).toFixed(2),
    hat: 'worn'};
}
// R1: the lock (leaning in from her turned stance; the hilt before her chest, the blade up across the guard at KR)
const lockPose = (t, G, pos, x = {}) => ({...ST, pos: nP(...pos), rot: [0, LOCK_YAW, 0], tor: [0, 14, 0], head: [-2, -40, 0], fL: nF('L', .22, 0, -.2), fR: nF('R', -.22, 0, .22),
  ...bladeThru(G, rigOf('repel', t, KP.KR), {pos, yaw: LOCK_YAW}), rh: 0, hR: 'open', aR: [20, 40, .8], hat: 'worn', ...x});
const LOCK_G = [.1, 1.09, -.45];
// R5: tipped backward against the actor's back, the torso rolled to her right (the head past the actor's left shoulder), the sword
// hand drawn back over the actor's right shoulder: the forearm through KS, the blade out past the shoulder
const HOOK = {H68: [.42, 1.5, .45], H: [.33, 1.48, .54], d: [.42, -.3, .86], pole: [.2, .9, -.5]};
const hookBody = {68: [[0, -.06, .1], 4, 10, 12], 70: [[-.1, -.06, .13], 5, 15, 30], 74: [[-.1, -.06, .135], 5.5, 16, 30], 78: [[-.1, -.055, .14], 6, 17, 30]};
const hookPose = (t, H = t === 68 ? HOOK.H68 : HOOK.H) => { const [pos, pitch, tp, roll] = hookBody[t];
  return {...ST, pos: nP(...pos), rot: [pitch, 0, 0], tor: [tp, -4, roll], head: [10, 4, 12], fL: nF('L', .16, 0, -.16), fR: nF('R', -.16, 0, -.02),
    ...blade(H, HOOK.d, {pos, yaw: 0}), rh: 0, hR: 'open', aR: [0, 44, .9], pL: HOOK.pole, hat: 'worn'}; };
{
  const k = Keys().k(0, FULL({...DIVE0, ...r0Pose(0)}));
  for (let t = 1; t <= 6; t++) k.k(t, r0Pose(t), 'l');
  const PRESS = (t, dG, pos, x = {}) => k.k(t, lockPose(t, vadd(LOCK_G, dG), pos, x), 'io');
  PRESS(10, [0, 0, 0], [0, -.1, .06]);
  PRESS(16, [0, .02, -.02], [0, -.08, .04], {tor: [-2, 15, 0], head: [-4, -40, 0]});
  PRESS(22, [0, .02, -.02], [0, -.08, .04], {tor: [-2, 15, 0], head: [-4, -40, 0]});
  PRESS(24, [0, .05, .01], [0, -.07, .08], {tor: [2, 12, 0], head: [2, -38, 0]});
  PRESS(26, [0, .08, .04], [0, -.07, .12], {tor: [6, 8, 0], head: [6, -34, 0], aR: [-10, 50, .9]});
  const G6 = vadd(LOCK_G, [0, .08, .04]);
  // R2: the blade beaten wide to her left 26-30 (every tick), the body opened
  const WIDE = {G: [.58, 1.42, -.05], d: [.55, .62, .56], mid: [-.1, .9, -.42]};
  const D26 = vunit(vsub(rigOf('repel', 26, KP.KR), G6));
  // (the edge directions the default edge gives at both ends: turned from one to the other with the swing)
  const edgeOf = d => vunit(vsub([0, -1, 0], vmul(d, -d[1])));
  WIDE.e0 = edgeOf(D26); WIDE.e1 = edgeOf(vunit(WIDE.d));
  k.all(every(27, 30, u => { const s = sm(u), pos = [0, lerp(-.07, -.03, s), lerp(.12, .1, s)], yaw = +lerp(LOCK_YAW, 25, s).toFixed(1);
    const d = u <= .5 ? slerpDir(D26, WIDE.mid, u * 2) : slerpDir(WIDE.mid, WIDE.d, u * 2 - 1), edge = slerpDir(WIDE.e0, WIDE.e1, u);
    return {pos: nP(...pos), rot: [0, yaw, 0], tor: [+lerp(4, 8, s).toFixed(1), +lerp(8, -24, s).toFixed(1), 0], head: [+lerp(6, 0, s).toFixed(1), +lerp(-34, -10, s).toFixed(1), 0],
      ...blade(lerp3(G6, WIDE.G, s), d, {pos, yaw, edge}), aR: [+lerp(-30, 20, s).toFixed(1), 50, .9]}; }));
  // 30-36 yanked in: the wrist dragged up to KW, side-on
  const GRAB = {pos: [0, 0, .02], yaw: 60, d: [.74, -.3, .6]};
  k.all(every(31, 36, u => { const s = sm(u), t = 30 + Math.round(u * 6), pos = lerp3([0, -.03, .1], GRAB.pos, s), yaw = +lerp(25, GRAB.yaw, s).toFixed(1);
    const G = lerp3(WIDE.G, rigOf('repel', 36, KP.KW), s);
    return {pos: nP(...pos), rot: [0, yaw, 0], tor: [+lerp(8, 4, s).toFixed(1), +lerp(-24, 4, s).toFixed(1), +lerp(0, 8, s).toFixed(1)], head: [+lerp(0, -4, s).toFixed(1), +lerp(-10, -50, s).toFixed(1), +lerp(0, 20, s).toFixed(1)],
      ...blade(G, lerp3(WIDE.d, GRAB.d, s), {pos, yaw}), fL: nF('L', .2, 0, lerp(-.14, -.1, s)), fR: nF('R', -.2, 0, lerp(.14, .1, s)), aR: [+lerp(20, -10, s).toFixed(1), +lerp(50, 30, s).toFixed(1), .9], void: t}; }));
  const HELD = (t, pos, x = {}) => k.k(t, {pos: nP(...pos), ...blade(rigOf('repel', t, KP.KW), GRAB.d, {pos, yaw: GRAB.yaw}), ...x}, 'io');
  HELD(40, [.01, 0, .03], {tor: [5, 6, 9], head: [-5, -52, 22], aR: [10, 36, .9]});
  HELD(44, [-.01, 0, .02], {tor: [3, 2, 7], head: [-3, -48, 18], aR: [-14, 28, .9]});
  HELD(48, [0, 0, .02], {tor: [4, 4, 8], head: [-4, -50, 20], aR: [0, 30, .9]});
  // R3: the hilt on the crown at 49 (the crown at KH), reels 49-52
  k.k(49, {pos: nP(0, -.14, -.06), rot: [0, 40, 0], tor: [2, -6, 2], head: [-1, -30, 0], ...blade([.5, 1.5, -.1], [.6, -.5, .55], {pos: [0, -.14, -.06], yaw: 40}), aR: [30, 40, .9],
    fL: nF('L', .2, 0, -.1), fR: nF('R', -.2, 0, .1)}, 'i')
    .k(50, {pos: nP(0, -.22, .1), rot: [0, 30, 0], tor: [-4, -10, 0], head: [-30, -16, 4], ...blade([.52, 1.2, -.05], [.5, -.72, .4], {pos: [0, -.22, .1], yaw: 30})}, 'o')
    .k(52, {pos: nP(0, -.26, .14), rot: [0, 20, 0], tor: [-6, -12, 0], head: [-34, -10, 6], ...blade([.5, 1.05, -.08], [.45, -.8, .35], {pos: [0, -.26, .14], yaw: 20}), aR: [40, 30, .8]}, 'io');
  // R4: cut 1 (56, rising): thrown up and back; cut 2 (62, level, the actor passing her right side): folded and turned; stumbles
  k.k(55, {pos: nP(0, -.16, .12), rot: [0, 12, 0], tor: [-4, -6, 0], head: [-14, -6, 0]}, 'io')
    .k(56, {pos: nP(0, -.04, .1), rot: [4, 6, 0], tor: [16, -14, -4], head: [14, 4, 0], ...blade([.6, 1.5, .1], [.5, .6, .6], {pos: [0, -.04, .1], yaw: 6}), aR: [70, 60, .9], pL: HOOK.pole,
      fL: nF('L', .18, 0, -.1), fR: nF('R', -.2, 0, .24)}, 'o')
    .k(59, {pos: nP(0, -.08, .12), rot: [2, 0, 0], tor: [10, -8, -2], head: [6, 0, 0], ...blade([.58, 1.3, .08], [.6, .1, .78], {pos: [0, -.08, .12], yaw: 0}), aR: [40, 50, .9]}, 'io')
    .k(61, {pos: nP(0, -.1, .1), rot: [0, 0, 0], tor: [2, 0, 0], head: [0, 10, 0]}, 'io')
    .k(62, {pos: nP(.04, -.18, .04), rot: [0, -14, 0], tor: [-22, 26, 6], head: [-10, 30, 0], ...blade([.5, 1.0, -.25], [.7, -.5, -.5], {pos: [.04, -.18, .04], yaw: -14}), aR: [70, -30, .5],
      fL: nF('L', .2, 0, -.06), fR: nF('R', -.22, 0, .18)}, 'i')
    .k(65, {pos: nP(.02, -.14, .08), rot: [0, -6, 0], tor: [-10, 14, 2], head: [-4, 18, 0], ...blade([.56, 1.15, -.05], [.75, -.2, .3], {pos: [.02, -.14, .08], yaw: -6}), aR: [60, -20, .6]}, 'io');
  // R5: back to back 68-78: tipped backward over the actor's right shoulder (her head past its left one), the sword forearm drawn
  // back over the shoulder at KS (hook 70)
  k.k(68, {...hookPose(68), head: [8, 0, 4], aR: [10, 40, .9]}, 'io');
  k.k(70, hookPose(70), 'io');
  k.k(74, {...hookPose(74), head: [11, 6, 12], aR: [-10, 50, .9]}, 'io');
  k.k(78, {...hookPose(78), head: [12, 8, 12], aR: [-16, 56, .9]}, 'io');
  // R6 (HF-B, HB-01): the throw as a throw (every tick 79-100). The actor (tools/player_motion/cine/clips.mjs) holds her sword
  // forearm - its right fist from the hook to 96, its left hand round her wrist 86-91 - and pulls it forward and down over its
  // right shoulder as it bends: she is levered up onto its back face up and rolled over that shoulder head first, low: her pelvis
  // on THROW.P (stage frame; 0.35 b over the shoulder at the top, 88: KT.over), pitched back on THROW.PT, her sword hand on
  // THROW.G (the actor's hands on the forearm behind it: MUTUAL KT.grip_l / _r); let go at 96 she drops off in front onto her back
  // at f 3.0 (101: KT.land), the blade swung up and down beside her as she falls (97-100). Her root arcs only THROW_H (the rig's
  // floor is the root: nothing hangs below it).
  const THROW = {
    P: {78: [-.10, .71, 1.34], 80: [0, .93, 1.45], 82: [.12, 1.13, 1.58], 84: [.2, 1.28, 1.72], 86: [.26, 1.37, 1.86], 88: [.28, 1.4, 2.0],
      90: [.28, 1.35, 2.13], 92: [.28, 1.24, 2.26], 94: [.27, 1.07, 2.38], 96: [.24, .85, 2.5], 98: [.15, .53, 2.76], 100: [.05, .3, 2.96]},
    PT: {78: 6, 80: 35, 82: 62, 84: 82, 86: 95, 88: 102, 90: 106, 92: 108, 94: 108, 96: 106, 98: 100, 100: 94},
    G: {78: [.33, 1.48, 1.74], 80: [.28, 1.4, 1.84], 82: [.24, 1.31, 1.96], 84: [.21, 1.21, 2.08], 86: [.2, 1.12, 2.19], 88: [.2, 1.04, 2.29],
      90: [.2, .97, 2.37], 92: [.22, .9, 2.43], 94: [.24, .83, 2.48], 96: [.26, .77, 2.52]},
    D: [.85, -.2, -.45], E: [-1, 0, 0],
  };
  const keyed = (tab, t) => {
    if (tab[t] !== undefined) return tab[t];
    const ts = Object.keys(tab).map(Number).sort((x, y) => x - y), b = ts.find(x => x > t), a = ts[ts.indexOf(b) - 1], u = (t - a) / (b - a);
    return Array.isArray(tab[a]) ? lerp3(tab[a], tab[b], u) : lerp(tab[a], tab[b], u);
  };
  for (let t = 79; t <= 100; t++) {
    const u = (t - 78) / 23, pt = keyed(THROW.PT, t), lf = t === 79 ? .6 : 1, Rt = rootAt('repel', t), Ps = keyed(THROW.P, t);
    const posN = [Ps[0] - Rt.p[0], Ps[1] - Rt.p[1] - HIP_Y, Ps[2] - Rt.p[2]];      // (her yaw 180: rig x = stage r, rig z = stage f)
    // the legs: up as she goes over (78-86), kept up through the fall and flopping down as she lands (98-101)
    const fly = t <= 86 ? Math.sin(Math.PI / 2 * (t - 78) / 8) : t <= 97 ? 1 : lerp(1, .55, (t - 97) / 3);
    const wb = sm((t - 78) / 4), w = sm((t - 90) / 6), w2 = sm((t - 96) / 4);
    // the sword hand: held on THROW.G to 96; 97-98 let go, the blade swung up; 99-100 down beside her as she lands (LIE's blade
    // at 100 = 101). Held, the blade sticks out to her left past the actor's right side, level and a little back (THROW.D, its
    // edge THROW.E back and down), turned there from the hook's line over 79-82: across her held forearm (which runs back from
    // her elbow to the actor's hands), so the wrist is not bent back past the held-prop limit (test_rig: the tip at least the
    // grip's distance + 0.62 of the blade from the elbow), the hilt keeps out of her own torso (V1 gripClear: pushes <= 0.2 b),
    // and the point clears both bodies and the root's floor
    const Gs = keyed(THROW.G, Math.min(t, 96));
    const bdir = vunit(slerpDir(HOOK.d, THROW.D, wb)), bedge = vunit(vadd(vmul([0, -1, 0], 1 - wb), vmul(THROW.E, wb)));
    // (97-100: let go, the blade swings up over her and down beside her left side, its edge to her right all the way (no roll),
    // to where it lies at 101: along the ground at her left, the point toward her feet. It passes 17 degrees to her left of
    // straight up: through the vertical itself the rig's sword channels turn it over (146 degrees in a tick))
    const LAND = {G: [.416, .183, 3.035], d: [.1, 0, -.99]}, wl = (t - 96) / 5;
    const swing = () => { const up = vunit([.3, 1, 0]), d0 = vunit(THROW.D), d = wl <= .5 ? slerpDir(d0, up, wl * 2) : slerpDir(up, LAND.d, wl * 2 - 1);
      return blade(lerp3(toRig(Rt, Gs), toRig(Rt, LAND.G), sm(wl)), d, {pos: posN, yaw: 0, edge: [-1, 0, 0]}); };
    const sw = t <= 96 ? blade(toRig(Rt, Gs), bdir, {pos: posN, yaw: 0, edge: bedge}) : swing();
    k.k(t, {rot: [+pt.toFixed(1), 0, 0], pos: posN.map(x => +(x / kOf(lf)).toFixed(4)), lf,
      tor: [+lerp(17, lerp(-4, 2, w2), wb).toFixed(1), +lerp(-4, 0, wb).toFixed(1), +lerp(30, 0, wb).toFixed(1)],
      head: [+lerp(12, lerp(-14, -10, w2), wb).toFixed(1), +lerp(8, lerp(0, -18, w2), wb).toFixed(1), +lerp(12, 0, wb).toFixed(1)],
      fL: [.15, +lerp(.1, .62, fly).toFixed(3), +lerp(-.06, -.34, fly).toFixed(3)], fR: [-.15, +lerp(.1, .4, fly).toFixed(3), +lerp(-.02, -.12, fly).toFixed(3)],
      ...sw, aR: [+lerp(-16, lerp(110, 30, w2), w).toFixed(1), +lerp(56, 70, w).toFixed(1), .95], hR: 'open',
      pL: [.55, -.35, .75], skG: +(u * .5).toFixed(2), skIB: +(u * .08).toFixed(3), scHip: [+lerp(0, -70, Math.min(1, u * 2)).toFixed(1), 0]}, 'l');
  }
  // the hat: off her head at 84, thrown with her (the rig's floor is the root: it cannot fall below her while she is in the air;
  // HF-B: a lower toss over the low throw):
  // up and out to her right, turning over, landing flat at the hold spot as she lands. hwP = the rig-frame path whose bulge the
  // retarget carries between the solved hat at 83 and the spot
  {
    const A1 = [0, 1.6, 1.0], t0 = 84, t1 = 101, B1 = HAT_HOLD, PA = [0, 1.75, 1.0];
    for (let t = t0; t < t1; t++) {
      const w = (t - t0) / (t1 - t0), lin = lerp3(PA, B1, w), dev = [-.35 * Math.sin(Math.PI * w), .5 * 4 * w * (1 - w) + .25 * (1 - w), .1 * Math.sin(Math.PI * w)];
      const P = t === t0 ? PA : vadd(lin, vmul(dev, 1 / K_ARC));
      k.k(t, {hat: 'world', hwP: P.map(x => +x.toFixed(3)), hwE: [+(100 * (1 - sm(w * 1.25))).toFixed(1), +lerp(0, 20, w).toFixed(1), +(40 * Math.sin(w * Math.PI * 2) * (1 - w) ** 1.5).toFixed(1)]}, 'l');
    }
    void A1;
  }
  // land 101: the slam, a short bounce, then lying
  k.k(101, {...FULL(LIE), plwR: 0, hR: 'open', aR: [70, 80, .95], pos: [0, -1.0, 0], tor: [6, 0, 0], head: [-18, -10, 0]}, 'i')
    .k(102, {tor: [-3, 0, 0], head: [-4, -12, 0], pos: [0, -1.04, 0]}, 'o').k(104, {tor: [2, 0, 0], head: [-10, -18, 0], aR: [40, 76, .95]}, 'io')
    .k(112, {tor: [3, 0, 0]}).k(118, {aR: [118, 40, .8], head: [-6, -8, 0], tor: [3, 2, 0]}, 'io')       // the right hand lifts weakly
    .k(124, {...LIE, tor: [2, 0, 0]}, 'io').k(128, {...LIE, tor: [3, 0, 0]});
  // R8: the kick at 129 (the pose still the lying one: = ending 0); the jolt 130-133: the body skids on its back (the root slides
  // away), the legs thrown up; the right hand takes the hat (hat hand 131)
  const KIP_BLADE = {gF: 0, gN: 1, gB: -80, gE: -25, gD: .42, cB: -115, cR: 0, th: -12, ed: -1, tw: 0};
  const LIE_BLADE = {gF: 0, gN: 0, gB: -90, gE: -58, gD: .62, cB: 0, cR: 90, th: 6, ed: -1, tw: 0}, UP_BLADE = {gF: 0, gN: 0, gB: -40, gE: -42, gD: .7, cB: 52, cR: 0, th: -30, ed: -1, tw: 0};
  const mixB = (a, b, u) => Object.fromEntries(Object.keys(a).map(n => [n, +(a[n] + (b[n] - a[n]) * u).toFixed(3)]));
  k.k(129, {...FULL(LIE)}).k(130, {tor: [-8, 4, -14], head: [-22, -8, 0], fL: [.15, .4, -.14], fR: [-.15, .3, -.08], pos: [0, -1.0, 0], ...mixB(LIE_BLADE, KIP_BLADE, .25)}, 'l')
    .k(131, {hat: 'hand', hhB: 90, hhE: 0, hhN: [0, 90], tor: [-14, 2, 0], head: [-20, -4, 0], fL: [.14, .7, -.3], fR: [-.14, .6, -.22], pos: [0, -1.06, 0], ...mixB(LIE_BLADE, KIP_BLADE, .5)}, 'l')
    .k(132, {tor: [-20, 0, 0], head: [-20, 0, 0], fL: [.13, .9, -.4], fR: [-.13, .86, -.3], pos: [0, -1.12, 0], plwR: .5, pR: [.2, -.5, .6], ...mixB(LIE_BLADE, KIP_BLADE, .75)}, 'l')
    // R9: the kip-up with it 133-137 (roll 133; every tick), crouched 137, up 139 with the hat set back on (worn 139), the P2
    // stance at 140 (= idle2)
    .k(133, {rot: [70, 0, 0], pos: [0, -1.0, 0], lf: 1, tor: [-28, 0, 0], head: [-10, 0, 0], fL: [.13, .8, -.5], fR: [-.13, .76, -.42], plwR: 0, aR: [60, 50, .9], hhB: 80, hhE: 0, hhN: [0, 90],
      ...KIP_BLADE, skG: .3}, 'l')
    .k(134, {rot: [48, 0, 0], pos: [0, -.84, 0], lf: .8, tor: [-30, 0, 0], fL: [.13, .56, -.52], fR: [-.13, .5, -.42], aR: [80, 44, .9], pR: [.55, -.35, .75], hhB: 70, hhE: 6, hhN: [20, 80]}, 'l')
    .k(135, {rot: [24, 0, 0], pos: [0, -.62, 0], lf: .5, tor: [-30, -4, 0], head: [-2, 4, 0], fL: [.14, .3, -.46], fR: [-.14, .26, -.36], aR: [100, 38, .9], hhB: 60, hhE: 10, hhN: [40, 70], skG: 0,
      skIB: 0, scHip: [-30, 0]}, 'l')
    .k(136, {...ST2, ...LOW, rot: [6, 0, 0], lf: .2, pos: [0, -.5, 0], tor: [-30, -6, 0], head: [4, 6, 0], fL: [.2, .14, -.3], fR: [-.2, .12, -.1], aR: [120, 30, .9], hat: 'hand', hR: 'grip',
      hhB: 40, hhE: 16, hhN: [20, 78], ...KIP_BLADE, scHip: [0, 0], skG: 0, skIB: 0, hairF: 0}, 'l')
    .k(137, {rot: [0, 0, 0], lf: 0, pos: [0, -.44, 0], tor: [-26, -4, 0], head: [6, 4, 0], fL: [.25, .1, -.22], fR: [-.25, .1, .2], aR: [150, 20, .9], hhB: 10, hhE: 26, hhN: [0, 74], ...mixB(KIP_BLADE, UP_BLADE, .33)}, 'l')
    .k(138, {pos: [0, -.3, 0], tor: [-18, 4, 0], head: [0, -4, 0], aR: [150, 20, .9], hhB: 0, hhE: 15, hhN: [0, 88], ...mixB(KIP_BLADE, UP_BLADE, .66)}, 'l')
    // (hat_on 139 and the idle2 pose at 140 are one tick apart: the hand leaves the brim as the hat settles and is still on its
    // way down at 140; the next clip's 3-tick blend carries it)
    .k(139, {...ST2, pos: [0, -.14, 0], tor: [-10, 9, 0], hat: 'worn', hR: 'open', bwR: 0, aR: [70, 24, .9], gN: 0}, 'l')
    .k(140, {...FULL(ST2), hat: 'worn'}, 'o');
  C('repel', k, {src: 'v 215.6-222.6 (ref/hr_repel_5fps.jpg, gauntlet_repel.jpg; hr_design §3.4): the deflected dive, the lock, the seized wrist, the hilt on the hat, two cuts, back to back, the shoulder throw, the kick, up again'});
}

// =================================================================================================================================
// ending (1372 t = H; §3.5 E1-E17; v 296.5-373.1: ref/cs_ending.jpg, hr_duel_2_5fps.jpg). Her root: ROOTS.ending.
// E1 0-50: on her back with her hand on the hat (= repel 129; the root skids 0-4); the kip-up 6-16 taking the hat (up 6; every
//    tick), rising 16-22 with the hat set back on (hat_on 20), stands; raises the sword high 28-42 (raise 28), holds;
// E2 the lunge 50-54 (lunge 50; the sequence glides the root to f 3.5): at 52 the actor's point grazes her brim (graze 52: the near edge of the brim at
//    KG, the head knocked back); the X lock at KE2 56-80 (lock 56), a jolt at the burst (burst 70); shoved back 80-86 (shove 80);
// E3 86-116 a turned guard (off screen); springs back 116-136 (back 116: airborne, legs tucked), lands low;
// E4 the run in 150-188 (run 150: a 8-t cycle at the sequence's 0.18 b/t), the sword trailing;
// E5 the cut into the clash at 190 (clash 190), the X lock at KE5 190-204;
// E6 (round W: the aerial duel is gone) the exchange on the ground 204-310, 2.25 b apart: the lock broken, three clashes - a1 228 the
//    diagonal onto the actor's block at KA1, a2 262 the overhead onto its raised guard at KA2 (stepping in), a3 286 cut on cut at
//    KA3 (the big flash) - and the X lock at KA4 298-304 (a4 298); pushed off (off 304) to f 5.3;
// E7 springs back low 314-334 (fly 314; seen as the launch and the landing), lands crouched at the mark (land 334);
// E8 338-378 rises, the blade lowered;
// E9 the scabbard from the hip into the right hand (scab_up 388), raised upright 388-398, swung down to her right while the left
//    hand lifts the blade across to its mouth 398-418 (swing 398; every tick), the blade on its axis 418-426, slid in 426-450
//    (sheathe 426), seated (sheathed 452: the click); line 17 (420); the sheathed sword carried in the right hand from here on;
// E10 the smile 476-556 (line 18 at 486); E12 the head lowered (head_down 640; line 19 at 628), turned away 650-700 (turn 650: the
//    sequence turns the body; the feet step, the hat swaying), her back 700-760 (line 20 at 716), her face over her left shoulder
//    (look_back 760), one open hand chest-high 800-820 (hand 800), the smile 820-846; E14 half turned (line 21 at 910);
// E15 the moon gaze: head up 990-1060 (gaze 990); E16 the pivot 1072-1094 (pivot 1072; the feet step), the walk in 1094-1154 (walk
//    1094; line 22 at 1082), stops (stop 1154), the open-palm "let me see" 1160-1196 (gesture 1160);
// E17 the left hand to the brim 1216-1232 (brim 1216; line 23 at 1230), eyes closed (eyes 1240), the brim pulled down with a
//    10-degree bow 1290-1330 (pull 1290), held, the face rises under the held brim with open eyes (open 1360) = H_POSE at 1372.
const KE2_G = {56: [.1, 1.04, -.6], 68: [.1, 1.04, -.6], 72: [.1, 1.06, -.58], 80: [.1, 1.04, -.6]};
const KE2_POS = {56: [0, -.1, .06], 68: [0, -.1, .05], 72: [0, -.09, .07], 80: [0, -.1, .04]};
const ke2Lock = (t, G = KE2_G[t]) => xLock('ending', t, 'KE2', G, KE2_POS[t]);
const KE5_G = {190: [.1, 1.2, -.55], 197: [.1, 1.2, -.55], 204: [.1, 1.21, -.54]};
const KE5_POS = {190: [0, -.1, .06], 197: [0, -.1, .05], 204: [0, -.09, .04]};
const ke5Lock = (t, G = KE5_G[t]) => xLock('ending', t, 'KE5', G, KE5_POS[t], {tor: [0, 14, 0]});
// E6 (round W, w_brief §4.6: the aerial duel is gone): the exchange on the ground, her root 2.25 b from the actor's (4.75 / 2.5).
// The guard GRD: the wide stance turned 18 degrees to her right, the blade up and forward; a cut = the grip and the blade's
// direction at its contact tick (through its K), wound up 8 t before and followed through 4 t after (every tick around it)
const GRD_N = [0, -.12, 0], GRD_Y = 18;
const GRD = {...ST2, rot: [0, GRD_Y, 0], pos: nP(...GRD_N), ...F_WIDE, tor: [-8, 10, 0], head: [-4, -22, 0], lf: 0, hat: 'worn', hR: 'open', aR: [20, 40, .85]};
const gBlade = (G, d, x = {}, edge = [0, -1, 0]) => ({...blade(G, d, {pos: GRD_N, yaw: GRD_Y, edge}), ...x});
const GUARD = gBlade([.1, 1.05, -.42], [-.1, .7, -.7]);
const KA_G = {228: [-.05, 1.12, -.5], 262: [.05, 1.42, -.5], 286: [.45, .92, -.5], 298: [.1, 1.2, -.55], 304: [.1, 1.21, -.54]};
const KA_OF = {228: 'KA1', 262: 'KA2', 286: 'KA3', 298: 'KA4', 304: 'KA4'};
const kaPose = (t, G = KA_G[t], edge = [0, -1, 0]) => ({...GRD, ...gBlade(G, vsub(rigOf('ending', t, KP[KA_OF[t]]), G), {}, edge)});
const ka4Lock = t => xLock('ending', t, 'KA4', KA_G[t], [0, -.1, .05], {tor: [0, 14, 0]});
{
  const k = Keys().k(0, FULL(LIE)).k(4, {tor: [3, 0, 0]}).k(5, {});
  const KIP_BLADE = {gF: 0, gN: 1, gB: -80, gE: -25, gD: .42, cB: -115, cR: 0, th: -12, ed: -1, tw: 0};
  const LIE_BLADE = {gF: 0, gN: 0, gB: -90, gE: -58, gD: .62, cB: 0, cR: 90, th: 6, ed: -1, tw: 0}, UP_BLADE = {gF: 0, gN: 0, gB: -40, gE: -42, gD: .7, cB: 52, cR: 0, th: -30, ed: -1, tw: 0};
  const mixB = (a, b, u) => Object.fromEntries(Object.keys(a).map(n => [n, +(a[n] + (b[n] - a[n]) * u).toFixed(3)]));
  // E1: the kip-up 6-16 (every tick): the legs swung up 6-9, the hat taken up (hand 9), rolled forward onto her feet 10-15
  const KIPR = [[6, 88, -1.04, 1, [.15, .3, -.1], [-.15, .2, -.06], -4], [7, 88, -1.06, 1, [.14, .56, -.24], [-.14, .46, -.16], -10], [8, 88, -1.1, 1, [.13, .8, -.36], [-.13, .74, -.28], -18],
    [9, 86, -1.12, 1, [.13, .9, -.4], [-.13, .86, -.3], -22], [10, 76, -1.04, 1, [.13, .84, -.48], [-.13, .8, -.4], -26], [11, 62, -.94, 1, [.13, .7, -.52], [-.13, .64, -.44], -30],
    [12, 46, -.82, .8, [.13, .54, -.52], [-.13, .48, -.42], -30], [13, 30, -.68, .6, [.14, .36, -.48], [-.14, .3, -.38], -30], [14, 16, -.56, .35, [.18, .2, -.38], [-.18, .16, -.2], -30],
    [15, 6, -.5, .15, [.22, .12, -.3], [-.22, .1, 0], -28]];
  // (6-11: she rolls a little toward the hat as she takes it at 9: the fist reaches its rim from above)
  const KROLL = {6: -6, 7: -10, 8: -14, 9: -12, 10: -6, 11: -2};
  for (const [t, pt, y, lf, fL, fR, tp] of KIPR) k.k(t, {rot: [pt, 0, 0], pos: [0, y, 0], lf, fL, fR, tor: [tp, 0, KROLL[t] || 0], head: [-16, 0, 0], ...mixB(LIE_BLADE, KIP_BLADE, Math.min(1, (t - 5) / 4)),
    skG: +(.5 * (1 - (t - 6) / 9)).toFixed(2), skIB: 0, scHip: [+(-70 * (1 - (t - 6) / 9)).toFixed(1), 0]}, 'l');
  k.k(9, {hat: 'hand', hhB: 90, hhE: 0, hhN: [0, 90]}, 'l').k(11, {plwR: 0, aR: [60, 50, .9], pR: [.55, -.35, .75], hhB: 80, hhE: 4, hhN: [10, 86]}, 'l')
    .k(13, {aR: [90, 40, .9], hhB: 64, hhE: 10, hhN: [30, 74]}, 'l').k(15, {aR: [120, 30, .9], hhB: 40, hhE: 16, hhN: [20, 78]}, 'l');
  k.k(16, {...ST2, ...LOW, rot: [0, 0, 0], lf: 0, pos: [0, -.44, 0], tor: [-26, -4, 0], head: [6, 4, 0], fL: [.25, .1, -.22], fR: [-.25, .1, .2], aR: [150, 20, .9], hat: 'hand', hR: 'grip',
    hhB: 10, hhE: 26, hhN: [0, 74], ...KIP_BLADE, scHip: [0, 0], skG: 0, skIB: 0, plwR: 0}, 'l')
    .k(18, {pos: [0, -.3, 0], tor: [-18, 4, 0], head: [0, -4, 0], hhB: 0, hhE: 15, hhN: [0, 88], ...mixB(KIP_BLADE, UP_BLADE, .5)}, 'l')
    .k(20, {...ST2, pos: [0, -.18, 0], tor: [-12, 8, 0], hat: 'worn', hR: 'brim', bwR: 1, bzR: 24, aR: [120, 30, .9], gN: 0}, 'l')
    .k(24, {...ST2, hR: 'open', bwR: 0, aR: [10, 14, .95]}, 'io').k(28, {});
  // the sword raised high 28-42 (the module's violet glow), held
  k.k(42, {...ST, pos: [0, -.06, 0], ...F_WIDE, tor: [-4, 0, 0], head: [-4, 0, 0], aR: [40, 70, .95], gF: 0, gB: -60, gE: 40, gD: .7, cB: -40, cR: 0, th: 130, ed: -1, rh: 0}, 'io')
    .k(48, {gE: 44, th: 136});
  // E2: the lunge 50-54 (the sequence glides her 5.2 -> 3.5): forward on the left foot; 52 = the graze half way (root 4.35): the
  // body thrown 0.45 b ahead of the root, the head knocked back (the brim's near edge at KG); 54 over her feet at 3.5
  k.k(50, {pos: [0, -.2, -.06], tor: [-14, 6, 0], head: [0, -6, 0], ...F_LUNGE, gB: -20, gE: 10, gD: .62, cB: -10, th: 60, aR: [10, 30, .9]}, 'i')
    // 51-53 a fleche: off the ground for three ticks, the body thrown ahead of the gliding root (52: 0.55 b), the right leg trailing
    .k(51, {...AIR, lf: .9, pos: [0, .05, -.3], rot: [0, 10, 0], tor: [-10, 8, 0], fL: [.15, .22, -.32], fR: [-.15, .3, .3], gB: -24, gE: 4, cB: 0, th: 30}, 'l')
    .k(52, {...AIR, lf: .9, pos: [0, .1, -.55], rot: [0, 20, 0], tor: [-19, 4, 0], head: [16, -18, 0], fL: [.15, .32, -.3], fR: [-.15, .42, .42],
      ...blade([.12, 1.05, -.95], [-.08, .78, -.62], {pos: [0, .1, -.55], yaw: 20}), aR: [30, 40, .85]}, 'l')
    .k(53, {...AIR, lf: .9, pos: [0, .04, -.3], rot: [0, 28, 0], tor: [-4, 6, 0], head: [6, -24, 0], fL: [.15, .12, -.28], fR: [-.15, .28, .3]}, 'l')
    .k(54, {lf: 0, kL: ST.kL, kR: ST.kR, fL: nF('L', .2, 0, -.2), fR: nF('R', -.2, 0, .2), pos: nP(0, -.08, .04), rot: [0, 36, 0], tor: [-6, 10, 0], head: [0, -30, 0], ...blade([.1, 1.02, -.55], [-.1, .72, -.68], {pos: [0, -.08, .04], yaw: 36})}, 'l');
  for (const t of [56, 68, 72, 80]) k.k(t, {...ke2Lock(t), ...(t === 72 ? {tor: [-6, 12, 0], head: [4, -40, 0]} : {})}, t === 56 ? 'l' : 'io');
  k.k(70, {...ke2Lock(68), tor: [-14, 14, 0]}, 'l');
  // shoved back 80-86 (the root to 6.0): heels dug in, the blade knocked up; 86-116 a turned guard
  k.k(83, {pos: nP(0, -.16, .1), rot: [0, 30, 0], tor: [6, 4, 0], head: [6, -24, 0], ...blade([.1, 1.35, -.3], [.3, .85, -.4], {pos: [0, -.16, .1], yaw: 30}), aR: [50, 50, .9],
    fL: nF('L', .2, 0, -.3), fR: nF('R', -.22, 0, .26)}, 'o')
    .k(92, {...ST2, rot: [0, 30, 0], pos: [0, -.2, 0], tor: [-8, -10, 0], head: [-2, -24, 0], ...F_WIDE, gF: 0, gN: 0, gB: -20, gE: 10, gD: .62, cB: -30, cR: 0, th: 50, ed: -1, aR: [30, 50, .9]}, 'io')
    .k(112, {pos: [0, -.24, 0]}).k(115, {...CROUCH, rot: [0, 0, 0], pos: [0, -.34, 0], tor: [-18, 0, 0], head: [-2, -4, 0]}, 'io');
  // the spring back 116-136 (airborne), the landing 136, the ready crouch
  k.k(120, {...AIR, pos: [0, .06, .04], rot: [10, 0, 0], tor: [-2, 6, 0], fL: [.13, .55, -.25], fR: [-.13, .5, -.1], lf: .8, ...B(-40, 0, 40, -1, {gL: .58}), gN: 0, aR: [60, 50, .9], hairS: .5, skW: -.6}, 'o')
    .k(130, {rot: [6, 0, 0], fL: [.13, .45, -.3], fR: [-.13, .4, -.15]})
    .k(136, {...ST, ...LOW, rot: [0, 0, 0], lf: 0, pos: [0, -.38, 0], fL: [.3, .1, -.36], fR: [-.28, .1, .34], tor: [-22, 14, 0], head: [6, -10, 0], gF: 0, gN: 0, gB: -60, gE: -38, gD: .66, cB: -84,
      cR: 0, th: -24, ed: -1, rh: 0, aR: [30, 40, .9], hairS: 0, skW: 0}, 'i')
    .k(146, {pos: [0, -.34, 0]});
  // E4: the run in 150-188, the sword trailing low behind her left side
  const RUNB = {gF: 0, gN: 0, gB: -110, gE: -40, gD: .62, cB: -150, cR: 0, th: -14, ed: -1, tw: 0};
  k.k(150, {...ST2, pos: [0, -.14, 0], rot: [-12, 0, 0], tor: [-14, 4, 0], head: [8, -2, 0], ...F_ST, ...RUNB, aR: [-28, 18, .96], hairS: -.55, skW: .6}, 'io');
  walk(150, 188, {P: 8, s: .62, armL: false, lean: -14}).forEach(([t, p, e]) => k.k(t, {fL: p.fL, fR: p.fR, pos: [0, p.pos[1] - .1, 0], rot: [-12, p.rot[1], 0], tor: p.tor}, e));
  // E5: the cut swung up into the clash 188-190, the X lock at KE5 190-204
  k.k(189, {rot: [0, 30, 0], pos: nP(0, -.14, 0), tor: [-12, 10, 0], head: [0, -30, 0], fL: nF('L', .22, 0, -.2), fR: nF('R', -.22, 0, .22),
    ...blade([-.1, .95, -.4], [.7, 0, -.7], {pos: [0, -.14, 0], yaw: 30}), aR: [20, 40, .8], hairS: -.3, skW: .3}, 'l');
  for (const t of [190, 197, 204]) k.k(t, {...ke5Lock(t), hairS: 0, skW: 0}, t === 190 ? 'l' : 'io');
  // E6 (round W): the lock broken 204-212 into the guard; a1 228 the diagonal from high on her right onto the actor's block; a2 262
  // the overhead cut down onto its raised guard (the sequence steps her in to 4.35 254-262 and back 266-274); a3 286 the rising
  // cut from low on her left on its descending cut (the big flash); the X lock at KA4 298-304; pushed off 304-310 (to 5.3)
  k.k(212, {...GRD, ...GUARD}, 'io');
  // (edge: the side the blade's edge faces, kept for the whole cut: a direction that passes the default edge's line flips the blade)
  const CUT = (t, wind, follow, edge = [0, -1, 0]) => {   // wind / follow: [G, dir] 8 t before and 4 t after the contact tick t
    const Gk = KA_G[t], dk = vunit(vsub(rigOf('ending', t, KP[KA_OF[t]]), Gk));
    k.k(t - 8, {...GRD, ...gBlade(wind[0], wind[1], {}, edge), tor: [-2, 22, 0]}, 'io');
    for (let i = 3; i >= 1; i--) { const u = 1 - i / 4; k.k(t - i, {...gBlade(lerp3(wind[0], Gk, u), slerpDir(wind[1], dk, u), {}, edge), tor: [+lerp(-2, -12, u).toFixed(1), +lerp(22, 4, u).toFixed(1), 0]}, 'l'); }
    k.k(t, {...kaPose(t, Gk, edge), tor: [-12, 4, 0]}, 'l').k(t + 1, {...gBlade(lerp3(Gk, follow[0], .35), slerpDir(dk, follow[1], .35), {}, edge)}, 'l')
      .k(t + 4, {...gBlade(follow[0], follow[1], {}, edge), tor: [-8, -6, 0]}, 'o');
  };
  CUT(228, [[-.4, 1.55, -.1], [-.35, .75, .55]], [[.3, .85, -.35], [.6, -.55, -.55]]);
  k.k(240, {...GRD, ...GUARD}, 'io');
  CUT(262, [[0, 1.65, -.05], [0, .65, .75]], [[.05, 1.2, -.55], [0, -.1, -1]], [0, 0, -1]);
  k.k(274, {...GRD, ...GUARD}, 'io');
  CUT(286, [[.35, .7, -.15], [.5, -.55, .45]], [[-.15, 1.35, -.45], [-.55, .7, -.45]]);
  k.k(295, {...GRD, ...gBlade([.05, 1.15, -.5], [.15, .45, -.9])}, 'io').k(298, ka4Lock(298), 'l').k(304, {...ka4Lock(304), tor: [-12, 10, 0]}, 'io');
  // pushed off 304-310 (the heels dug in, the blade knocked up), crouched 313; the spring back 314-334 (low, apex 1.0), lands crouched
  k.k(308, {...GRD, pos: nP(0, -.18, .08), rot: [0, 26, 0], tor: [6, 4, 0], head: [6, -20, 0], ...blade([.1, 1.3, -.28], [.3, .85, -.4], {pos: [0, -.18, .08], yaw: 26}), aR: [50, 50, .9]}, 'o')
    .k(313, {...CROUCH, rot: [0, 0, 0], pos: [0, -.34, 0], tor: [-18, 0, 0], head: [-2, -4, 0], gF: 0, gN: 0, gB: -50, gE: -20, gD: .6, cB: -40, cR: 0, th: 30, ed: -1, tw: 0}, 'io')
    .k(318, {...AIR, pos: [0, .06, .04], rot: [10, 0, 0], tor: [-2, 6, 0], fL: [.13, .55, -.25], fR: [-.13, .5, -.1], lf: .8, ...B(-40, 0, 40, -1, {gL: .58}), gN: 0, aR: [60, 50, .9], hairS: .5, skW: -.6}, 'o')
    .k(328, {rot: [6, 0, 0], fL: [.13, .45, -.3], fR: [-.13, .4, -.15]})
    .k(334, {...LOW, ...ST2, rot: [0, 0, 0], lf: 0, pos: [0, -.44, 0], ...F_WIDE, tor: [-26, 6, 0], head: [10, -6, 0], gF: 0, gN: 0, gB: -100, gE: -40, gD: .66,
      cB: -110, cR: 0, th: -30, ed: -1, rh: 0, aR: [20, 50, .9], hairS: 0, skW: 0, kL: [.12, 0, -1], kR: [-.12, 0, -1]}, 'i').k(338, {pos: [0, -.42, 0]});
  // E8: rises, the blade lowered at her left
  k.k(352, {...ST, pos: [0, -.04, 0], tor: [-4, 0, 0], head: [-4, 0, 0], gN: 0, hat: 'worn'}, 'io').k(378, {});
  // E9: the scabbard from the hip into the right hand 380-388, upright 398; the swing 399-418; on the axis 418-426; in 426-450
  const L1 = (a, b, u) => +lerp(a, b, u).toFixed(1), L2 = (a, b, u) => +lerp(a, b, u).toFixed(2);
  const SH0 = {gF: 0, gB: -58.4, gE: 21.3, gD: 1.01, cB: 90, cR: 0, th: -25, ed: -1, tw: -60};   // the free blade = the on-axis pose at sh .22
  k.k(380, {hR: 'grip', hsR: 1}).k(388, {scab: 'hand', ...HIP_DIR, hsR: 1})
    .k(391, {hsR: 0, scB: 95, scE: -32, scR: -80, scOff: .2, aR: [28, 34, .8], pR: [.6, -.4, .4]})
    .k(394, {scB: 40, scE: 24, scR: -20, scOff: .28, aR: [62, 18, .72]})
    .k(398, {...F_ST, pos: [0, -.04, 0], rot: [0, 0, 0], tor: [-4, 0, 0], aR: [84, 10, .66], scB: 20, scE: 76, scR: 0, scOff: .3, sh: .22});
  k.all(every(399, 418, u => { const sv = sm(u);
    return {scB: L1(20, 90, sv), scE: L1(76, -25, sv), aR: [L1(84, 40, u), L1(10, 50, u), L2(.66, .95, u)], scOff: L2(.3, .12, u), gF: 0, gB: L1(-32, SH0.gB, sv),
      gE: L1(-50, SH0.gE, sv), gD: L2(.6, SH0.gD, sv), cB: L1(38, SH0.cB, sv), cR: 0, th: L1(-40, SH0.th, sv), ed: -1, tw: L1(0, SH0.tw, sv),
      pL: [L2(.55, .9, u), L2(-.35, .3, u), L2(.75, .2, u)], tor: [-4, 0, 0]}; }));
  // the left hand stays on the seated hilt at the click (452) and lets go at 453
  k.k(426, {shW: 1, sh: .22}, 'io').k(450, {sh: .97}, 'io').k(452, {sword: 'sheathed', sh: 1}).k(453, {hold: 0, hL: 'open', aL: [34, -70, 1]}, 'l')
    .k(460, {aR: [20, 14, .92], scB: 8, scE: -22, scOff: .2, aL: [4, 10, .97], pL: [.55, -.35, .75], shW: 0, sh: 0, tor: [-3, 0, 0], head: [-6, 0, 0]}, 'io')
    .k(468, {...F_TOG, pos: [0, -.02, 0]});
  // E10 the smile (head a little tilted) 476-560
  k.k(476, {face: 'smile', head: [-4, -4, 6]}).k(516, {head: [-3, -6, 7]}).k(556, {head: [-4, -4, 6]}).k(566, {face: 'calm', head: [-6, 0, 2]});
  // E12: the head lowered 632-640; the turn away 650-700 (the sequence turns the body; the feet step, the hat swaying); her face
  // over her left shoulder 760-774, one open hand chest-high 800-820, the smile 820-846
  k.k(628, {}).k(640, {head: [-22, 0, 0], tor: [-6, 0, 0]}, 'io').k(650, {});
  for (let i = 0; i < 5; i++) { const t = 652 + i * 10, ch = i % 2 ? 'fR' : 'fL', x = i % 2 ? -.13 : .13;
    k.k(t + 3, {[ch]: [x, .24, i % 2 ? .08 : -.1], head: [-18, i % 2 ? 6 : -6, i % 2 ? 3 : -3]}, 'io').k(t + 7, {[ch]: [x, .1, i % 2 ? .04 : -.06]}, 'io'); }
  k.k(702, {...F_TOG, head: [-10, 0, 0], tor: [-4, 0, 0]}).k(730, {head: [-6, 0, 0]}).k(760, {})
    .k(774, {head: [-4, -70, 0], tor: [-3, -20, 0]}, 'io').k(800, {}).k(812, {hL: 'open', aL: [70, -10, .62], frL: 60, pL: [.6, -.4, .5]}, 'io')
    .k(820, {face: 'smile'}).k(846, {}).k(858, {face: 'calm', aL: [4, 10, .97], frL: 0, pL: [.55, -.35, .75], head: [-4, -46, 0], tor: [-3, -24, 0]}, 'io')
    .k(972, {head: [-4, -44, 0]});
  // E15: the moon gaze: faces it, head up 990-1060
  k.k(990, {head: [-4, 0, 0], tor: [-2, 0, 0]}, 'io').k(1004, {head: [15, 0, 0]}, 'io').k(1060, {head: [16, 2, 0]}).k(1070, {head: [4, 2, 0]}, 'io');
  // E16: the pivot 1072-1094 (the sequence turns the body): the feet step, the sheathed sword sweeps flat behind her legs
  k.k(1076, {fL: [.13, .24, -.08]}).k(1080, {fL: [.13, .1, -.04], scB: 40, scE: -14, aR: [10, 20, .94]});
  k.all(every(1081, 1089, u => ({scB: +lerp(40, 178, u).toFixed(1), scE: -12, aR: [+lerp(10, -20, u).toFixed(1), +lerp(20, 24, u).toFixed(1), .94]})));
  k.k(1090, {fR: [-.13, .24, .06]}).k(1094, {...F_ST, fR: [-.14, .1, .1], head: [-4, 0, 0], tor: [-2, 0, 0], pos: [0, -.04, 0], scB: 172, scE: -16, aR: [14, 16, .95]});
  // the walk in 1094-1154 (16-t cycle at 0.075 b/t), the sheathed sword carried at her side; stops
  k.all(walk(1094, 1154, {P: 16, s: .5, lean: -4}));
  k.k(1158, {...F_TOG, pos: [0, -.02, 0], rot: [0, 0, 0], tor: [-2, 0, 0], aL: [4, 10, .97], scB: 8, scE: -22, aR: [14, 14, .94]}, 'io');
  // the open-palm "let me see" 1160-1196, the closed-lip smile after
  k.k(1160, {}).k(1170, {hL: 'open', aL: [70, 6, .7], frL: 90, pL: [.6, -.4, .5], head: [-2, -4, 3]}, 'io').k(1190, {aL: [74, 4, .72]})
    .k(1200, {aL: [6, 10, .97], frL: 0, head: [-4, 0, 0]}, 'io').k(1206, {face: 'smile'}).k(1216, {});
  // E17: the hat tip: the left hand to the brim 1216-1232, eyes closed 1240; the bow and the brim pulled down 1290-1330, held; the
  // face rises under the held brim, eyes open 1360; H_POSE 1372
  k.k(1232, {hL: 'brim', bwL: 1, bzL: 40, aL: [120, 30, .9], pL: [.7, -.2, .2], frL: 0, head: [-4, 0, 0]}, 'o').k(1240, {face: 'closed'}).k(1290, {})
    .k(1330, {tor: [-10, 0, 0], head: [-16, 0, 0], bzL: 24, pos: [0, -.04, 0]}, 'io').k(1350, {tor: [-10, 0, 0], head: [-15, 0, 0]})
    .k(1360, {face: 'calm', tor: [-2, 0, 0], head: [-6, 0, 0], bzL: 40, pos: [0, -.02, 0]}, 'io').k(1372, FULL(H_POSE));
  C('ending', k, {src: 'v 296.5-373.1 (ref/cs_ending.jpg, hr_duel_2_5fps.jpg; hr_design §3.5): the kip-up, the lock, the run and the clash, the aerial duel, the sheathing, the turn away, the moon, the greeting and the hat tip'});
}

// (authoring: the native-key helpers for tools/dev/sim/hr/cine scratch scripts)
export const _t = {nP, nF, nH, blade, bladeThru, rigOf, toRig, KP, r0Pose, lockPose, LOCK_G, R0_GRIP, hookPose, HOOK, cs1Lock, K1_G, xLock, ke2Lock, KE2_G, ke5Lock, KE5_G, kaPose, KA_G, ka4Lock};

// ---- export ------------------------------------------------------------------------------------------------------------------
const ORDER = ['intro', 'intro_end', 'cs1', 'lead60', 'lead5', 'lead_re', 'repel', 'ending'];
for (const n of ORDER) if (!clips.find(c => c.name === n)) clips.push({name: n, keys: [K(0, FULL(ST)), K(CONTRACT[n].len, {})], base: BASE, note: 'not authored yet'});
export const CLIPS = ORDER.map(n => clips.find(c => c.name === n));
void SW; void F_TOG; void B; void CROUCH; void LOW; void AIR; void LOCK; void DOWN; void H_POSE; void F_ST; void F_WIDE; void F_LUNGE; void E; void flipPos;
void nP; void nF; void nH; void bladeThru; void rigOf; void vadd; void hipDirChannels;
