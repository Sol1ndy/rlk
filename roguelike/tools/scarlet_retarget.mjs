// The retarget of 홍련's clips (S2d, 11-05; S:hr/s2d/design.md §2): every clip of tools/scarlet_clips.mjs and S2b's
// tools/scarlet_cine.mjs is authored on S2a's skeleton (hip line 1.36, legs 1.18 from the hip joint to the ankle, arms 0.82 from
// the shoulder to the grip); since S2d her body is the player avatar's (scarlet_pose.mjs SK: hip line 0.766, legs 0.766, arms
// 0.594). Per sample, between sampleClip and solve (tools/build_scarlet_rig.mjs):
//   retarget(p, clip, t)   angles / directions / fractions / discrete states kept; the pelvis offset scaled by k(lf) (the leg
//                          factor on the ground, 1 in the air: flips keep the body frame); the sole targets scaled about the
//                          hip joint (S_LEG: every bend ratio kept); the grip distances by S_ARM (+ the lock rule); the planted
//                          hand targets by S_LEG; the scabbard grip by S_SCAB; the world-hat spots mapped onto HAT_REST; the
//                          derived weights (wLie lying, wSeat seated on the kit's stone) and the stone-rule flags
//   overlay(q, clip, t, ctx)  the declared patches (PATCHES: the floor pickup kneels, the iai turn, the sip, the sheathe
//                          entry SH0'), the hat hand-overs (hatX), the re-anchored world-hat flights (hwF)
// Nothing else changes a source angle (test: node tools/scarlet_retarget.mjs --dump all, every angle channel == the source
// outside the PATCHES spans). Pure: no file I/O except the CLI.
import {add, sub, times, len, unit, mul, q, rot, ik, lerp, dot, cross, perp, aimQ, armFront, slerp, basisQ} from './mboss_rig_math.mjs';
import {SK, HIP_Y, SUP, HAT_FLOOR_HOLD, dirBE, bladeQ, qa, conj, BOX, hatVisPts} from './scarlet_pose.mjs';
import {HAT, SWORD} from './scarlet_geometry.mjs';

// ---- factors -------------------------------------------------------------------------------------------------------------------
export const S_LEG = .765625 / 1.18;      // hip joint -> sole: the avatar's straight leg / S2a's (0.648835)
export const S_ARM = .59375 / .82;        // shoulder -> grip (0.724085)
export const S_SCAB = 1.52 / 1.82;        // the scabbard (0.835165)
export const K_ARC = 2.00 / 2.42;         // the bulge of the thrown-hat paths (head tops, 0.826)
const D = Math.PI / 180;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { const t = clamp01(x); return t * t * (3 - 2 * t); };
// R(x; a -> b): the smoothstep ramp from a to b (a > b: falling)
export const ramp = (x, a, b) => smooth((x - a) / (b - a));
const wrap = a => ((((a + 180) % 360) + 360) % 360) - 180;
const r6 = x => Math.round(x * 1e6) / 1e6;

// ---- supports and world-hat spots (rig frame, her yaw; blocks) ------------------------------------------------------------------
// the kit's seat stone (request s2d-2: tuff 1.2 x 0.24 x 0.64 b) and its item spots: the bottle at her left, the cup at her right
export const SUPPORTS = {stone: SUP};
// the world hat at rest: beside her (look/hat/world, DEFAULT_POSE), beside her lying right leg (DOWN / the kip-ups), over her
// face (LY, the ending's start; HAT_REST.face is set by the builder from a probe solve of LY: setHatFace)
export const HAT_REST = {side: {t: [1.00, .02, -.35]}, leg: {t: [-1.00, .02, -.40]}, face: null};
// the source spots (S2a's hwP values) that map onto them; any other world-hat value outside a flight is a build error
const HAT_SOURCE = [[[.95, .02, -.35], 'side'], [[-1.05, .02, -.5], 'leg'], [[0, .52, .96], 'face']];
// the thrown paths: repel 60-75 (from the hat on her back at 59 to the leg spot), ending 26-39 (from her face to her right
// hand at 40); P'(t) = A' + (B' - A') u + K_ARC (P(t) - (A + (B - A) u)), u = (t - t0) / (t1 - t0)
export const HAT_FLIGHTS = {
  repel: {t0: 60, t1: 75, from: {state: 'back', t: 59}, to: {spot: 'leg'}},
  ending: {t0: 26, t1: 39, from: {spot: 'face'}, to: {state: 'hand', t: 40}},
};
export function setHatFace(spot) { HAT_REST.face = spot; }
// lane H1c (11-11): grog_in, the balance break (hr_design.md §1.4): the hat leaves her head as she topples backward (6) and lands on
// DOWN's spot beside her right leg (10), where `down` and `kipup` expect it
HAT_FLIGHTS.grog_in = {t0: 6, t1: 10, from: {state: 'worn', t: 5}, to: {spot: 'leg'}};
// the face spot from probe solves of the ending (probe(t) -> {o}: LY, the hat over her face): parallel to the face at the probe
// where the face stands highest (0 / 13 / 26), its front toward her feet (as the source's face hat and the flight that lifts it
// at 27: no spin as it leaves), 0.012 off the face's outer layer; then
// the smallest lift off the face (0.012-0.05) and tilt about its left-right axis (the chest-side rim up, whole degrees) that
// keep the visible brim 0.01 out of every body box over the rest ticks 0-26 (her forearms lie across her chest under the
// 1.32-b brim; the hand comes up to it before the lift at 27)
const FACE_CLEAR = ['head', 'torso', 'pelvis', 'arm_l', 'arm_r', 'forearm_l', 'forearm_r', 'thigh_l', 'thigh_r', 'shin_l', 'shin_r'];
export function faceSpot(probe) {
  let best = null;
  for (const t of [0, 13, 26]) {
    const {o} = probe(t);
    const n = unit(rot(o.head.q, [0, 0, -1])), fp = add(o.head.t, rot(o.head.q, [0, .25, -.28125]));
    if (!best || dot(fp, n) > dot(best.fp, best.n)) best = {fp, n, hq: o.head.q};
  }
  const Y = best.n, Zf = unit(perp(rot(best.hq, [0, 1, 0]), Y)), X = cross(Y, Zf), base = basisQ(X, Y, Zf);
  const frames = [0, 4, 8, 12, 16, 20, 23, 24, 25, 26].map(t => probe(t).o), hp = hatVisPts();
  const deep = (T, Q) => {
    let w = -1;
    for (const o of frames) for (const n of FACE_CLEAR) {
      const v = o[n]; if (!v || v.s[0] < 1e-4) continue;
      const [lo, hi] = BOX[n], iq = conj(v.q);
      for (const P0 of hp) {
        const L = rot(iq, sub(add(T, rot(Q, P0)), v.t));
        w = Math.max(w, Math.min(L[0] - lo[0], hi[0] - L[0], L[1] - lo[1], hi[1] - L[1], L[2] - lo[2], hi[2] - L[2]));
      }
    }
    return w;
  };
  let out = null;
  for (const lift of [.012, .02, .03, .04, .05]) {
    const T = add(best.fp, times(Y, lift)).map(x => +x.toFixed(4));
    for (let a = 0; a <= 20; a++) {
      const Q = mul(qa(times(X, -1), a), base), d = deep(T, Q);
      if (!out || d < out.d - 1e-9) out = {t: T, q: Q, tilt: a, lift, d};
      if (d <= -.01) return out;
    }
  }
  return out;
}
const same = (a, b) => a && b && Math.abs(a[0] - b[0]) < 1e-6 && Math.abs(a[1] - b[1]) < 1e-6 && Math.abs(a[2] - b[2]) < 1e-6;
export const hatSpotOf = hwP => (HAT_SOURCE.find(([v]) => same(v, hwP)) || [])[1] || null;

// ---- the channel retarget ------------------------------------------------------------------------------------------------------
const SEAT_CLIP = 'intro', SEAT_END = [214, 226];
export function retarget(p, clip, t) {
  const o = {...p};
  const lf = clamp01(p.lf || 0);
  // the pelvis offset: crouch depth scales with the legs; airborne / flipping / lying offsets keep the body frame
  const k = S_LEG + (1 - S_LEG) * ramp(lf, .3, .8);
  o.pos = p.pos.map(v => v * k);
  // the sole targets about the hip joint (one rule for the yaw and the pelvis frame)
  for (const [ch, s] of [['fL', 1], ['fR', -1]]) {
    const F = p[ch];
    let y = S_LEG * (F[1] - .10);
    if (lf < .5) y = Math.max(0, y);
    o[ch] = [s * SK.hipJ[0] + S_LEG * (F[0] - s * .105), y, S_LEG * F[2]];
  }
  // the grip distances: the lever gL x S_ARM (shoulder-relative already); the grip sphere's gD x S_ARM, moved out along the
  // same bearing / elevation where that would fold the sword arm below S2a's extension (|grip - left shoulder| / arm: the
  // avatar's wide shoulders bring a plainly scaled grip at her left side within 0.2 b of the shoulder); then the lock rule: the two-hand
  // upright blade before her face 0.46 b out (a 0.594 arm reaches 0.48 from a 0.34375 shoulder at x 0), deterministic so
  // every LOCK hand-over gets the same grip
  o.gD = gripDistance(p, o.pos); o.gL = (p.gL ?? .55) * S_ARM;
  const wl = ramp(p.rh || 0, .6, .9) * ramp(p.gE, -10, 0) * ramp(p.gE, 40, 20) * ramp(Math.abs(p.th - 95), 20, 10) * (1 - (p.gF || 0));
  o.gD += (Math.max(o.gD, .46) - o.gD) * wl;
  o.plL = p.plL.map(v => v * S_LEG); o.plR = p.plR.map(v => v * S_LEG);
  o.scOff = Math.max(SK.throat, (p.scOff || 0) * S_SCAB);
  // derived weights (from the source sample)
  o.wLie = ramp(Math.abs(wrap(p.rot[0]) - 88), 35, 15) * ramp(lf, .6, .9) * ramp(-p.pos[1], .6, .8);
  o.wSeat = clip === SEAT_CLIP ? (t <= SEAT_END[0] ? 1 : 1 - ramp(t, SEAT_END[0], SEAT_END[1])) : 0;
  o.wKnee = 0; o.wLip = 0;
  // the stone rule (seated, a planted hand on S2a's rock top, y >= 0.5): the item spots of the kit's stone
  if (o.wSeat > .5) {
    const st = {};
    if ((p.plwL || 0) > 0 && p.plL[1] >= .5) st.l = p.bottle === 'hand' ? 'bottle' : 'empty';
    if ((p.plwR || 0) > 0 && p.plR[1] >= .5) st.r = p.cup === 'hand' ? 'cup' : 'empty';
    if (st.l || st.r) o.stone = st;
  }
  if (p.cup === 'rock' || p.bottle === 'rock') throw new Error(`${clip} t${t}: the prop state rock is never keyed (S2d)`);
  // the world hat: a rest spot (hwS) or a flight (overlay)
  if (p.hat === 'world') {
    const spot = hatSpotOf(p.hwP);
    if (spot) { const s = HAT_REST[spot]; if (!s) throw new Error(`HAT_REST.${spot} is not set`); o.hwS = s.t; if (s.q) o.hwSq = s.q; o.hwSpot = spot; }
    else if (!(HAT_FLIGHTS[clip] && t > HAT_FLIGHTS[clip].t0 - 1 && t <= HAT_FLIGHTS[clip].t1)) throw new Error(`${clip} t${t}: world-hat value ${p.hwP} is neither a rest spot nor in a flight`);
  }
  return o;
}

// the sphere grip distance keeping the sword arm's extension: S2a's FK (hip 1.36, waist .14, shoulder [.25, .43, .01], swing .5,
// arm .82) -> the extension f; the avatar's (hip HIP_Y, seam .1875, shoulder SK.shoulder, swing .55, arm .594) -> the
// distance x along the same direction with |Cw + d x - SL| = f * .594 (the far root)
function gripDistance(p, pos2) {
  const Ryaw = q([0, p.rot[1], 0]), Pq = mul(Ryaw, q([p.rot[0], 0, p.rot[2]])), Cq = mul(Pq, q(p.tor)), d = rot(Ryaw, dirBE(p.gB, p.gE));
  const R1 = [p.pos[0], 1.36 + p.pos[1], p.pos[2]], SL1 = add(add(R1, rot(Pq, [0, .14, 0])), rot(Cq, [.25, .43, .01]));
  const G1 = add(add(R1, rot(Ryaw, [0, .5, 0])), times(d, p.gD)), f = len(sub(G1, SL1)) / .82;
  const R2 = [pos2[0], HIP_Y + pos2[1], pos2[2]], SL2 = add(add(R2, rot(Pq, SK.waist)), rot(Cq, SK.shoulder)), Cw = add(R2, rot(Ryaw, SK.swing));
  const s = sub(Cw, SL2), b = dot(d, s), c = dot(s, s) - (f * (SK.armU + SK.fore)) ** 2, disc = b * b - c;
  const plain = p.gD * S_ARM;
  if (disc < 0) return plain;
  // the far root (the grip out along the ray beyond the shoulder), never closer than the plain scaling (overhead / across-the-
  // body grips stay where S_ARM puts them; only a grip the plain scaling would fold against the shoulder moves out)
  const x = -b + Math.sqrt(disc);
  return x > plain && x < 1.0 ? x : plain;
}

// ---- declared patches (native units; applied by overlay after retarget) --------------------------------------------------------
// weight w = R(t; in) rising, 1 between, R(t; out) falling; `set` lerps a channel toward the value by w, `add` adds w * delta
// the fist on the brim's near edge (the brim lies 0.02 up; the grip point HAT_FLOOR_HOLD above it: the fist's end rests on it)
const HAT_LEG_EDGE = [HAT_REST.leg.t[0] + (HAT.R - .02), HAT_REST.leg.t[1] + HAT_FLOOR_HOLD, HAT_REST.leg.t[2]];
// kneeling on the right knee (the source crouch's legs, the hips lowered): the right foot behind as LOW's with the shin lying flat
// on the floor (its sole end 0.15 up), the right thigh down-forward to the knee on the floor (the hip line ~0.48 up), the left
// foot planted forward; the deep bow (pelvis -25, torso -55) brings the right shoulder within an arm of the brim's edge
const KNEEL = {pos: [0, -.29, -.02], rot: [-25, 0, 0], tor: [-55, -10, 0], head: [40, 10, 0], fL: [.15, 0, -.35], fR: [-.16, .15, .21],
  kL: [.12, .3, -1], kR: [-.12, -.2, -1], plR: HAT_LEG_EDGE, wKnee: 1};
// the sword (left hand) held out at her left side during the kneels, the blade low toward her left back: clear of the bowed
// torso, and the grip comes forward with the kip (a grip left in the yaw frame would let the shoulder swing past it)
const KNEEL_BLADE = {gF: 0, gB: -80, gE: -25, gD: .42, cB: -115, cR: 0, th: -12, ed: -1, tw: 0};
export const IAI_DELTA = 14;
// V1 (HR-47): a10's airborne crouch (9-19, both hands on the grip, the torso bowed 24 deg) raised S2a's blade laid back over the
// head (th 120): the player-size arms put the fists behind and in the head, and the dive strike at 20-21 had to bring them through
// it. Held instead as a high guard before her face: the grip on the swing sphere ahead of her chin, the blade upright (S2a units)
const A10_HIGH = {gF: 0, gB: 0, gE: 25, gD: .55, th: 95};
// V1 (HR-47): intro_end's cross-draw (the left hand to the hilt of the scabbard her right hand holds upright before her right
// shoulder, 52-56, drawn at 56): the player-size left arm crossed her chest to a hilt at her chin and the fist sank into her torso
// and head. The right hand holds the scabbard lower and further out before her chest instead (S2a units: aR pitch / roll / reach; the scabbard across her front, its body toward her right and down, the hilt up to
// her left: the cross-draw pulls the blade out to her left)
const DRAW_E = {aR: [40, -15, .9], scB: 90, scE: -45};
// S2d round 2: the step aside off the seat stone. seq.py glides her root SEAT_ASIDE 1.1 b to her right over intro 226-246 (one linear
// 20-t glide, 0.055 b/t); the clip stands still there, so the feet step with the glide: four side steps of 0.55 b (right, left, right,
// left foot, 5 t each, the swing sole lifted <= 0.08 b) while the stance sole's target counter-moves 0.055 b/t in the rig frame: every
// planted sole keeps its spot in the world (the feet 0.8 b apart at most). seq.py's fallback to her left (her right blocked) is
// not stepped (the soles slide as before).
export const ASIDE = {t0: 226, len: 20, d: 1.1, lift: .08};
function asideFeet(o, t) {
  const u = t - ASIDE.t0, n = ASIDE.len, st = n / 4, v = ASIDE.d / n, sl = ASIDE.d / 2;
  if (u <= 0 || u >= n) return;
  // the soles' steps done by u (right foot at 0-5 and 10-15, left at 5-10 and 15-20), the swing phase, the lift
  const done = (k0) => [0, 1].reduce((a, i) => a + smooth((u - (k0 + 2 * i) * st) / st), 0);
  const swing = k0 => [0, 1].map(i => (u - (k0 + 2 * i) * st) / st).find(x => x > 0 && x < 1);
  for (const [ch, k0] of [['fR', 0], ['fL', 1]]) {
    const ph = swing(k0), lift = ph === undefined ? 0 : ASIDE.lift * Math.sin(Math.PI * ph);
    o[ch] = [o[ch][0] - sl * done(k0) + v * u, o[ch][1], o[ch][2]];
    // the swing sole's lift: added by the solver over the planted sole's height (after its boot loop), so a crouched, inclined shin
    // clears the floor too
    if (lift > 0) o[ch === 'fR' ? 'fLiftR' : 'fLiftL'] = lift;
  }
}
// V1 (HR-49): the walk and the strafes (api.WALK_SPEED 0.12 b/t, the module's root glide; clip timing frozen: the walk's contacts at
// 0 / 12, the strafe's steps at 0 / 10). S2a's feet, scaled by S_LEG, swept 0.4 b per stance (the walk's planted foot slid ~58 %,
// jittering) and the strafe never lifted a foot (both soles skated, a 0.11-b pop four times a cycle).
// WALK: a longer stride, each sole planted 0.38 b ahead of the hip joint at its contact and swept back steadily to 0.38 behind over
// its 12-t stance (0.063 b/t: the player-size leg reaches no further with the hips dipped 0.10 b at the contacts; holding the full
// 0.12 b/t would need 6-t steps), then swung forward lifted <= 0.08 b over the 12 t to its next contact; the hips bob 0.10 -> 0.045 b
// down (contacts -> mid-stance)
export const WALK = {len: 24, Z: .38, lift: .08, dip: [.10, .045]};
function walkFeet(o, t) {
  const {len: n, Z, lift, dip} = WALK, h = n / 2;
  for (const [ch, c] of [['fL', 0], ['fR', h]]) {
    const u = (((t - c) % n) + n) % n;
    let z, l = 0;
    if (u < h) z = -Z + 2 * Z * u / h;
    else { const w = (u - h) / h; z = Z - 2 * Z * smooth(w); l = lift * Math.sin(Math.PI * w); }
    o[ch] = [o[ch][0], 0, z];
    if (l > 0) o[ch === 'fL' ? 'fLiftL' : 'fLiftR'] = l;
  }
  o.pos = [o.pos[0], -(dip[0] + dip[1]) / 2 - (dip[0] - dip[1]) / 2 * Math.cos(2 * Math.PI * t / h), o.pos[2]];
}
// STRAFE-L / STRAFE-R: ASIDE's side steps at the strafe's speed, four a cycle (5 t each: the leading foot out, the trailing foot in,
// as step1 @ 0 and step2 @ 10 open each half): the feet from 0.13 b off the centre (closed, the legs side by side) to 0.485 (wide,
// the hips 0.10 b down: the lateral reach), the stance sole swept in steadily over its 5 t (0.071 b/t), the swing sole lifted
// <= 0.08 b over its planted height; the source's fore-aft foot offsets kept
export const STRAFE = {len: 20, step: 5, xin: .13, xout: .485, lift: .08, dip: .10};
const strafeFeet = sd => (o, t) => {
  const {len: n, step: st, xin, xout, lift, dip} = STRAFE;
  // the leading foot (sd +1: her left) swings out over [0, 5) and [10, 15), the trailing foot in over [5, 10) and [15, 20)
  const lead = sd > 0 ? 'fL' : 'fR', trail = sd > 0 ? 'fR' : 'fL', u = ((t % n) + n) % n, ph = u % (2 * st);
  for (const [ch, sgn, swingFirst] of [[lead, sd, true], [trail, -sd, false]]) {
    // swing first: out during [0, st) (in -> out), stance [st, 2 st) (out -> in); the trailing foot the other way round
    let x, l = 0;
    const inSwing = swingFirst ? ph < st : ph >= st, w = (swingFirst ? ph : ph - st) / st;
    if (swingFirst) x = inSwing ? xin + (xout - xin) * smooth(w) : xout - (xout - xin) * ((ph - st) / st);
    else x = inSwing ? xout - (xout - xin) * smooth(w) : xin + (xout - xin) * (ph / st);
    if (inSwing) l = lift * Math.sin(Math.PI * w);
    o[ch] = [sgn * x, 0, o[ch][2]];
    if (l > 0) o[ch === 'fL' ? 'fLiftL' : 'fLiftR'] = l;
  }
  o.pos = [o.pos[0], -dip, o.pos[2]];
};
export const PATCHES = [
  {id: 'KNEEL-K', clip: 'kipup', in: [6, 8], out: [10, 12], set: KNEEL, why: 'the floor pickup of the hat on the right knee'},
  {id: 'KNEEL-K-B', clip: 'kipup', in: [3, 8], out: [10, 16], set: KNEEL_BLADE, why: 'the sword out at her left through the kneel (5- / 6-tick ramps: no whip)'},
  {id: 'KNEEL-L', clip: 'lead_down', in: [5, 7], out: [9, 11], set: KNEEL, why: 'the floor pickup of the hat on the right knee'},
  {id: 'KNEEL-L-B', clip: 'lead_down', in: [1, 6], out: [11, 17], set: KNEEL_BLADE, why: 'the sword out at her left through the kip and the kneel (a 5-tick ramp in; out over 6 ticks after the kneel: no whip, the elbow never crosses the shoulder)'},
  {id: 'IAI', clip: 'cs1', in: [104, 106], out: [161, 164], add: {tor: [0, IAI_DELTA, 0], head: [0, -IAI_DELTA, 0]},
    why: 'the cross-draw reach to the hip hilt (V1: held through the draw at 162, so the turning torso does not sweep over the hilt)'},
  {id: 'SIP', clip: 'intro', in: [66, 70], out: [86, 94], set: {wLip: 1}, why: 'the cup at her lips'},
  {id: 'SH0', clip: 'ending', in: [297, 297], out: [326, 326], sh0: true, why: 'the sheathe entry on the new scabbard axis (SH0\')'},
  {id: 'A10-HIGH', clip: 'a10', in: [4, 8], out: [19, 20], set: A10_HIGH,
    why: 'V1 (HR-47): the airborne two-hand guard held as a high guard before her face (the player-size arms cannot hold the blade laid back over her head)'},
  {id: 'DRAW-E', clip: 'intro_end', in: [47, 51], out: [57, 60], set: DRAW_E,
    why: 'V1 (HR-47): the scabbard held further out before her chest for the cross-draw (the fist off her torso and head)'},
  {id: 'WALK', clip: 'walk', in: [0, 0], out: [24, 24], fn: walkFeet,
    why: 'V1 (HR-49): a longer stride (each sole planted 0.38 b ahead, swept steadily 0.76 b back over its 12-t stance, swung forward lifted), the hips bobbing with it'},
  {id: 'STRAFE-L', clip: 'strafe_l', in: [0, 0], out: [20, 20], fn: strafeFeet(1),
    why: 'V1 (HR-49): ASIDE-like lifted side steps at the strafe speed (four a cycle, the feet 0.26 -> 0.97 b apart, the hips 0.10 b down)'},
  {id: 'STRAFE-R', clip: 'strafe_r', in: [0, 0], out: [20, 20], fn: strafeFeet(-1),
    why: 'V1 (HR-49): ASIDE-like lifted side steps at the strafe speed (four a cycle, the feet 0.26 -> 0.97 b apart, the hips 0.10 b down)'},
  {id: 'ASIDE', clip: 'intro', in: [ASIDE.t0, ASIDE.t0], out: [ASIDE.t0 + ASIDE.len, ASIDE.t0 + ASIDE.len], fn: asideFeet,
    why: 'the feet step with seq.py\'s 1.1-b glide aside off the seat stone (4 side steps of 0.55 b, the stance sole kept on its world spot)'},
];
const patchW = (P, t) => (t < P.in[0] || t > P.out[1] ? 0 : t < P.in[1] ? ramp(t, P.in[0], P.in[1]) : t <= P.out[0] ? 1 : 1 - ramp(t, P.out[0], P.out[1]));
export const patchSpans = clip => PATCHES.filter(P => P.clip === clip).map(P => [P.id, P.in[0], P.out[1]]);
const L1 = (a, b, u) => a + (b - a) * u;
// the angle channels the dump compares (identity outside the patch spans)
export const ANGLE_CH = ['rot', 'tor', 'head', 'cB', 'cR', 'th', 'ed', 'tw', 'gB', 'gE', 'aL', 'aR', 'scHip', 'hhB', 'hhE', 'hhN', 'scB', 'scE', 'scR',
  'cupT', 'botT', 'hwE', 'bzL', 'bzR', 'frL', 'frR', 'kL', 'kR', 'pL', 'pR', 'rh', 'gF', 'hold', 'lf', 'plwL', 'plwR', 'bwL', 'bwR', 'hiL', 'hsR', 'sh',
  'shW', 'vis', 'hairF', 'hairS', 'skF'];

export function overlay(q0, clip, t, ctx = {}) {
  const o = {...q0};
  for (const P of PATCHES) {
    if (P.clip !== clip) continue;
    const w = patchW(P, t);
    if (w <= 0) continue;
    if (P.set) for (const [ch, v] of Object.entries(P.set)) o[ch] = Array.isArray(v) ? o[ch].map((x, i) => x + (v[i] - x) * w) : (o[ch] ?? 0) + (v - (o[ch] ?? 0)) * w;
    if (P.add) for (const [ch, v] of Object.entries(P.add)) o[ch] = o[ch].map((x, i) => x + v[i] * w);
    if (P.fn) P.fn(o, t);
    if (P.id.startsWith('KNEEL') && w > 0) o.kneelHat = true;
    if (P.sh0 && ctx.sh0) {
      const S = ctx.sh0;
      if (t <= 304) {
        const s = smooth((t - 297) / 7);
        Object.assign(o, {gF: 0, gB: L1(-32, S.gB, s), gE: L1(-50, S.gE, s), gD: L1(.6 * S_ARM, S.gD, s), cB: L1(38, S.cB, s), cR: 0, th: L1(-40, S.th, s), ed: -1,
          tw: L1(0, S.tw, s)});
      } else Object.assign(o, {gF: 0, gB: S.gB, gE: S.gE, gD: S.gD, cB: S.cB, cR: 0, th: S.th, ed: -1, tw: S.tw});
      if (S.sh && t >= 304 && t <= 306) o.sh = Math.max(o.sh || 0, S.sh);
    }
  }
  // the hat hand-overs (from the source key ticks of `hat`; ctx.hatSwitches, cut ticks snap)
  if (ctx.hatSwitches) {
    const X = {};
    for (const s of ctx.hatSwitches) {
      if ((ctx.cuts || []).includes(s.t)) continue;
      const A = s.from, B = s.to;
      if (B === 'hand' && ['worn', 'back', 'world'].includes(A)) {
        // the right hand pre-rolls to the hat's hold point, takes it at the switch, the hat blends into the hand
        if (t >= s.t - 4 && t <= s.t - 1) { X.hold = A; X.hw = smooth((t - s.t + 5) / 4); }
        if (t >= s.t && t <= s.t + 3) { X.from = {k: t - s.t + 1, bw: smooth((t - s.t) / 3)}; if (A !== 'world') { X.hold = A; X.hw = 1 - smooth((t - s.t) / 3); } }
      } else if (A === 'hand' && (B === 'worn' || B === 'back')) {
        // the hat blends onto the destination and the hand to its hold point before the release
        if (t >= s.t - 4 && t <= s.t - 1) { const w = smooth((t - s.t + 5) / 4); X.to = {dest: B, bw: w, path: 'line'}; X.hold = B; X.hw = w; }
      } else if ((A === 'worn' && B === 'back') || (A === 'back' && B === 'worn')) {
        // the swing over the back of her head
        if (t >= s.t - 4 && t <= s.t - 1) X.to = {dest: B, bw: smooth((t - s.t + 5) / 4), path: 'arc'};
      }
    }
    if (Object.keys(X).length) o.hatX = X;
  }
  // a re-anchored world-hat flight (pass 2: ctx.flight = {A, Aq, B, Bq} from pass 1; pass 1: the source path, scaled)
  const F = HAT_FLIGHTS[clip];
  if (F && o.hat === 'world' && t > F.t0 - 1 && t <= F.t1 && !o.hwSpot) {
    const u = (t - F.t0) / (F.t1 - F.t0), Pt = q0.hwP, PA = ctx.flightSrc?.A, PB = ctx.flightSrc?.B;
    const Ryaw = q([0, o.rot[1], 0]);
    let Q = mul(Ryaw, q(o.hwE || [0, 0, 0]));
    if (ctx.flight && PA && PB) {
      const {A, B, Aq, Bq} = ctx.flight;
      const lin = add(PA, times(sub(PB, PA), u));
      const T = add(add(A, times(sub(B, A), u)), times(sub(Pt, lin), K_ARC));
      if (Aq && t <= F.t0 + 2) Q = slerp(Aq, Q, smooth((t - F.t0) / 3));
      if (Bq && t >= F.t1 - 2) Q = slerp(Q, Bq, smooth((t - F.t1 + 3) / 3));
      o.hwF = {t: T, q: Q};
    } else o.hwF = {t: [Pt[0] * K_ARC, Pt[1] * K_ARC, Pt[2] * K_ARC], q: Q};
  }
  return o;
}
// the hat switches of a clip from its accumulated keys (discrete channels switch at their key)
export function hatSwitches(ks) {
  const out = [];
  for (let i = 1; i < ks.length; i++) if (ks[i].p.hat !== ks[i - 1].p.hat) out.push({t: ks[i].tick, from: ks[i - 1].p.hat, to: ks[i].p.hat});
  return out;
}

// ---- SH0': the sheathe entry's free blade = the on-axis pose (the builder probes ending 304) --------------------------------------
// channels (gF 0, cR 0, ed -1) whose free blade frame is grip G / rotation SQ (rig frame) for a pose with root R and yaw Ryaw
export function bladeChannels(G, SQ, R, Ryaw) {
  const iy = conj(Ryaw), Cw = add(R, rot(Ryaw, SK.swing));
  const v = rot(iy, sub(G, Cw)), gD = len(v), gE = Math.asin(v[1] / gD) / D, gB = Math.atan2(-v[0], -v[2]) / D;
  const t = rot(iy, rot(SQ, [0, 1, 0])), th = Math.asin(Math.max(-1, Math.min(1, t[1]))) / D, cB = Math.atan2(-t[0], -t[2]) / D;
  const u0 = dirBE(cB, 0), v0 = [0, 1, 0], T0 = add(times(u0, Math.cos(th * D)), times(v0, Math.sin(th * D)));
  const Ed0 = add(times(u0, -Math.sin(th * D)), times(v0, Math.cos(th * D))), e = rot(iy, rot(SQ, [0, 0, -1]));
  const a = Math.atan2(dot(cross(Ed0, e), T0), dot(Ed0, e)) / D;
  let tw = a - 180; tw = ((tw + 540) % 360) - 180;
  return {gF: 0, gB: r6(gB), gE: r6(gE), gD: r6(gD), cB: r6(cB), cR: 0, th: r6(th), ed: -1, tw: r6(tw)};
}

// ---- HIP_DIR (scarlet_cine.mjs): the hip scabbard as a hand-held direction ---------------------------------------------------------
// scB / scE: the bearing / elevation of SK.scabHipDir; scR: the roll (0.1-degree search) that makes the hand state's frame
// qa(d, scR) bladeQ(d, forward) equal the hip frame bladeQ(d, up) at pelvis pitch / roll 0; scOff: the throat (SK.throat)
export function hipDirChannels() {
  const d = SK.scabHipDir, scB = Math.atan2(-d[0], -d[2]) / D, scE = Math.asin(d[1]) / D;
  const hipQ = bladeQ(d, [0, 1, 0]), handQ = bladeQ(d, [0, 0, -1]);
  let best = 0, bv = Infinity;
  for (let r = -1800; r <= 1800; r++) {
    const Q = mul(qa(d, r / 10), handQ), dd = 1 - Math.abs(dot(Q, hipQ) + Q[3] * hipQ[3]);
    if (dd < bv - 1e-15) { bv = dd; best = r / 10; }
  }
  return {scB: +scB.toFixed(2), scE: +scE.toFixed(2), scR: best, scOff: SK.throat};
}

// ---- refCore: S2a's own contact truth per tick (the source pose on S2a's skeleton and S2c's core boxes) ------------------------
// FK + leg IK with S2a's frozen constants; low = the lowest corner of the pelvis / torso / head / thigh / shin boxes (their outer
// layers) BEFORE any lift (arms excluded); prev carries the knee bend directions. The support pass (scarlet_pose.mjs step 14)
// keeps "touched -> touches, airborne -> stays up"; the manifest `support` table holds it per tick (the tests' air / touch spans).
const S2A = {HIP_Y: 1.36, hipJ: [.105, -.08, 0], waist: [0, .14, 0], neckB: [0, .55, 0], thigh: .60, shin: .58};
const S2A_BOX = {pelvis: [[-.2231, -.08, -.1181], [.2231, .1125, .1181]], torso: [[-.2231, -.0275, -.1181], [.2231, .5631, .1181]],
  head: [[-.225, -.055, -.225], [.225, .395, .225]], thigh: [[-.1181, -.60, -.1181], [.1181, 0, .1181]], shin: [[-.1181, -.6931, -.1181], [.1181, 0, .1181]]};
const corners = ([lo, hi]) => { const out = []; for (const x of [lo[0], hi[0]]) for (const y of [lo[1], hi[1]]) for (const z of [lo[2], hi[2]]) out.push([x, y, z]); return out; };
const S2A_PTS = Object.fromEntries(Object.entries(S2A_BOX).map(([k, b]) => [k, corners(b)]));
const lowAt = (pts, t, Q) => { let m = Infinity; for (const P of pts) m = Math.min(m, t[1] + rot(Q, P)[1]); return m; };
export function refCore(p, prev = {}) {
  const Ryaw = q([0, p.rot[1], 0]), Pq = mul(Ryaw, q([p.rot[0], 0, p.rot[2]]));
  const R = [p.pos[0], S2A.HIP_Y + p.pos[1], p.pos[2]], floorP = [p.pos[0], 0, p.pos[2]];
  const Wst = add(R, rot(Pq, S2A.waist)), Cq = mul(Pq, q(p.tor)), Nb = add(Wst, rot(Cq, S2A.neckB)), Hq = mul(Cq, q(p.head));
  let low = Math.min(lowAt(S2A_PTS.pelvis, R, Pq), lowAt(S2A_PTS.torso, Wst, Cq), lowAt(S2A_PTS.head, Nb, Hq));
  const lf = clamp01(p.lf || 0), next = {};
  for (const [s, k, F, kp] of [[1, 'l', p.fL, p.kL], [-1, 'r', p.fR, p.kR]]) {
    const H = add(R, rot(Pq, [S2A.hipJ[0] * s, S2A.hipJ[1], S2A.hipJ[2]]));
    const Aw = add(floorP, rot(Ryaw, F)), Ab = add(R, rot(Pq, [F[0], F[1] - S2A.HIP_Y, F[2]]));
    let A = lerp(Aw, Ab, lf);
    const pole = rot(lf > .5 ? Pq : Ryaw, kp || [s * .12, 0, -1]), fwd = rot(lf > .5 ? Pq : Ryaw, [0, 0, -1]);
    let sol, thQ, shQ;
    for (let it = 0; it < 3; it++) {
      sol = ik(H, A, S2A.thigh, S2A.shin, pole, prev[k] || null);
      const kv = times(sol.v, -1);
      thQ = aimQ(sub(sol.E, H), armFront(sub(sol.E, H), kv, fwd));
      shQ = aimQ(sub(sol.W, sol.E), armFront(sub(sol.W, sol.E), kv, fwd));
      const lo = lowAt(S2A_PTS.shin, sol.E, shQ);
      if (lo >= .004) break;
      A = add(A, [0, .006 - lo, 0]);
    }
    next[k] = sol.v;
    low = Math.min(low, lowAt(S2A_PTS.thigh, H, thQ), lowAt(S2A_PTS.shin, sol.E, shQ));
  }
  return {low, prev: next};
}

// ---- CLI: node tools/scarlet_retarget.mjs --dump <clip|all>: per tick the source and the retarget+overlay angle channels (JSON) ---
// (an async function, not a top-level await: scarlet_cine.mjs imports this module, so the dump starts once it has evaluated)
if (process.argv[1] && process.argv[1].endsWith('scarlet_retarget.mjs') && process.argv.includes('--dump')) (async () => {
  const which = process.argv[process.argv.indexOf('--dump') + 1] || 'all';
  const C = await import('./scarlet_clips.mjs');
  const cine = (await import('./scarlet_cine.mjs')).CLIPS;
  const out = {patches: PATCHES.map(P => ({id: P.id, clip: P.clip, span: [P.in[0], P.out[1]]})), clips: {}};
  // a stand-in for the builder's face spot and SH0' (the dump compares angles; the patched SH0 span is exempt)
  if (!HAT_REST.face) HAT_REST.face = {t: [0, .43, .5]};
  const api = JSON.parse((await import('node:child_process')).execFileSync('python3', ['-c', 'import json, sys; sys.path.insert(0, "tools"); from mboss_scarlet import api; ' +
    'print(json.dumps({n: {"len": c[0]} for n, c in api.CLIPS.items()}))'], {cwd: new URL('..', import.meta.url).pathname, encoding: 'utf8'}));
  for (const c of [...C.CLIPS, ...cine]) {
    if (which !== 'all' && c.name !== which) continue;
    const L = api[c.name].len, cc = {...c, len: L}, base = c.base || C.DEFAULT_POSE, ks = C.accumulate(cc, base);
    const rows = [];
    for (let t = 0; t <= L; t++) {
      const p = C.sampleClip(cc, t, ks, base);
      const qq = overlay(retarget(p, c.name, t), c.name, t, {hatSwitches: hatSwitches(ks), cuts: c.cuts || []});
      rows.push({t, src: Object.fromEntries(ANGLE_CH.map(k => [k, p[k]])), out: Object.fromEntries(ANGLE_CH.map(k => [k, qq[k]]))});
    }
    out.clips[c.name] = rows;
  }
  process.stdout.write(JSON.stringify(out));
})();
void perp; void basisQ; void HIP_Y; void SWORD;
