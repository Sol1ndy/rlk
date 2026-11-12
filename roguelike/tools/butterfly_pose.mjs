// Pose -> part transforms for the Moonlit Butterfly (달빛 환영 나비) rig: forward kinematics of her
// skeleton (scratchpad mb2/understand/model.md §1, §6, §8). Shared math: mboss_rig_math.mjs.
//
// Rig frame: +X = her LEFT, +Y up, -Z forward, blocks; the origin is the floor point under her hips.
// BH (hoof sole to helmet crown, standing) = 2.8 b. Euler triples are degrees (X, then Y, then Z; see
// mboss_rig_math.mjs q): pitch + leans back / swings a hanging segment forward, yaw + turns her to her right,
// roll + tips the top toward her right.
//
// PAIRED channels (legL/legR, fanL/fanR, fwL/fwR, hwL/hwR, tuL/tuR, tlL/tlR, the hand rotations) are authored
// in her LEFT side's sense and mirrored for the right side ([p, y, r] -> [p, -y, -r]), so equal values give a
// symmetric pose. For the wings that means: roll + raises the wing (flap up), yaw + sweeps it forward (cup),
// pitch + leans its top back. For the legs: pitch + swings the leg forward, roll + splays it outward.
//
// A pose is a full set of channels (DEFAULT_POSE in butterfly_clips.mjs merged with the clip keys):
//   pos [x,y,z]      root offset from the anchor (the boss body); y is the hover (butterfly form ≈ 1.2 b + leg fold)
//   rot [p,y,r]      root rotation about ROOT_PIVOT (flips, banks, dives, the back-turned groggy)
//   pelvis, torso    eulers relative to the root; head relative to the torso; crest (antennae + streamers)
//                    relative to the head; collar (the fur mane) relative to the torso
//   legL / legR      hip eulers; kneeL/kneeR, hockL/hockR bends in degrees (+ swings the lower segment forward)
//   fanL / fanR      shoulder plate + side-blade fan, relative to the torso (roll + flares the blades up)
//   hRA hRB hLA hLB  the floating crescent "hands": positions in the torso frame relative to WAIST (raw rig
//                    axes: x < 0 is her right); hRAe hRBe hLAe hLBe their eulers (paired, relative to the torso)
//   lockR / lockL    0..1: the big crescent of that side snaps onto the shin of that side as a blade (kicks)
//   hands, flakes    scales of the four crescent pieces / the four diamond flakes (0 hides them)
//   fwL fwR hwL hwR  fore- and hindwing eulers at their roots, relative to the torso; fwS / hwS their scales
//   glow             holographic overlay scale factor (1 = with the wing)
//   tuL tuR tlL tlR  upper / lower ribbon tendril eulers (upper relative to the torso, lower to the upper);
//   tS               tendril scale
//   core             chest glow scale (0 = hidden; 1-3 for the transform sheath, the wrap core, the blast)
//   vis              everything scaled about the body centre (entrance, death)
//   form 'h' | 'b'   discrete: the rig form score at that tick (human / butterfly)
//   wlook 'el'|'flat' discrete: the wing look ('el' = the stored element look, 'flat' = flat lime)
//   ph               (sampler) idle phase 0..1 per 40 t: crescent and flake bob
import {add, sub, times, len, unit, mul, q, rot, aimQ, toDisplayT, toDisplayQ} from './mboss_rig_math.mjs';

export const BH = 2.8;
export const ROOT_PIVOT = [0, 1.5, 0];
export const HIP = [0, 1.33, 0], WAIST = [0, 1.61, 0];
// Display scale per part (blocks per 16 model units).
export const PART_SCALE = {
  pelvis: 1, torso: 1, collar: .82, head: 1, head_glow: 1, crest: 1, fan_r: 1.25, fan_l: 1.25,
  thigh_r: 1, shin_r: 1, foot_r: 1, thigh_l: 1, shin_l: 1, foot_l: 1,
  hand_r_a: 1, hand_r_b: 1, hand_l_a: 1, hand_l_b: 1, flakes: 1,
  fwing_l: 3.5, fwing_r: 3.5, fwglow_l: 3.5, fwglow_r: 3.5, hwing_l: 2.4, hwing_r: 2.4,   // half-size wing models (WING_FIT)
  tendril_ul: 1.1, tendril_ur: 1.1, tendril_ll: 1.55, tendril_lr: 1.55, core: 1,
};
// Body attachment points (torso frame, from WAIST) and the leg skeleton (her left side, rig frame).
export const ATTACH = {
  collar: [0, .64, .02], neck: [0, .77, -.04], crest: [0, .37, .02],        // crest from the neck (head frame)
  fan: [.42, .61, .05], flakes: [0, 1.04, .25], core: [0, .49, -.25],
  // wing roots on the upper back, 0.42 b beside the spine (the cards start further out: WING_FIT)
  fwing: [.42, .79, .30], hwing: [.42, .58, .36],
  tendril: [.50, .30, .18],                                                   // beside the chest (torso frame)
};
const LEG = {hip: [.16, 1.33, 0], knee: [.24, .90, -.14], hock: [.33, .42, .10], hoof: [.42, 0, -.06]};   // a slight A-stance
export const LEG_LEN = {thigh: len(sub(LEG.knee, LEG.hip)), shin: len(sub(LEG.hock, LEG.knee)), foot: len(sub(LEG.hoof, LEG.hock))};
// Rest frames: model -Y along the segment, model -Z toward the front.
const FRONT = [0, 0, -1];
const legRest = side => {
  const m = v => [v[0] * side, v[1], v[2]];
  const T = aimQ(m(sub(LEG.knee, LEG.hip)), FRONT), S = aimQ(m(sub(LEG.hock, LEG.knee)), FRONT), F = aimQ(m(sub(LEG.hoof, LEG.hock)), FRONT);
  const inv = Q => [-Q[0], -Q[1], -Q[2], Q[3]];
  return {hip: m(sub(LEG.hip, HIP)), T, S: mul(inv(T), S), F: mul(inv(S), F)};
};
const LEG_REST = {l: legRest(1), r: legRest(-1)};
// End of the upper ribbon tendril (model units of tendril_ul at its scale) = the lower ribbon's pivot.
export const TENDRIL_END = [9.6, -9.4, 0];
// The big crescent locked onto a shin as a blade (shin frame, blocks; euler of the crescent model in it).
const SHIN_BLADE = {t: [.02, -.26, -.1], e: [8, 0, 0]};
export const mirrorE = e => [e[0], -e[1], -e[2]];
const sideE = (e, side) => (side > 0 ? e : mirrorE(e));

// prev is unused (kept for the shared clip compiler's signature: no IK continuity is needed here).
export function solve(p) {
  const o = {};
  const part = (n, t, Q, s = 1) => { o[n] = {t, q: Q, s: Array.isArray(s) ? s : [s, s, s]}; };
  const P = q(p.pelvis), Tq = q(p.torso);
  const fromWaist = v => add(WAIST, rot(Tq, v));
  part('pelvis', HIP, P);
  part('torso', WAIST, Tq);
  part('collar', fromWaist(ATTACH.collar), mul(Tq, q(p.collar)));
  const neck = fromWaist(ATTACH.neck), Hq = mul(Tq, q(p.head));
  part('head', neck, Hq);
  part('head_glow', neck, Hq);
  part('crest', add(neck, rot(Hq, ATTACH.crest)), mul(Hq, q(p.crest)));
  // legs
  const legs = {};
  for (const [s, side] of [['l', 1], ['r', -1]]) {
    const R = LEG_REST[s], up = s === 'l' ? 'L' : 'R';
    const hipJ = add(HIP, rot(P, R.hip));
    const thighQ = mul(mul(P, q(sideE(p['leg' + up], side))), R.T);
    const shinQ = mul(mul(thighQ, q([p['knee' + up], 0, 0])), R.S);
    const footQ = mul(mul(shinQ, q([p['hock' + up], 0, 0])), R.F);
    const knee = add(hipJ, rot(thighQ, [0, -LEG_LEN.thigh, 0])), hock = add(knee, rot(shinQ, [0, -LEG_LEN.shin, 0]));
    part('thigh_' + s, hipJ, thighQ);
    part('shin_' + s, knee, shinQ);
    part('foot_' + s, hock, footQ);
    legs[s] = {knee, shinQ, hoof: add(hock, rot(footQ, [0, -LEG_LEN.foot, 0]))};
  }
  // fans, crescents, flakes
  part('fan_l', fromWaist(ATTACH.fan), mul(Tq, q(sideE(p.fanL, 1))));
  part('fan_r', fromWaist([-ATTACH.fan[0], ATTACH.fan[1], ATTACH.fan[2]]), mul(Tq, q(sideE(p.fanR, -1))));
  const w = p.ph * 2 * Math.PI;
  const bob = (ph, a = .05) => [0, Math.sin(w + ph) * a, 0];
  const hand = (n, key, side, ph, lock = 0, leg = null) => {
    let t = add(fromWaist(p[key]), rot(Tq, bob(ph))), Q = mul(Tq, q(sideE(p[key + 'e'], side)));
    if (lock > 1e-4 && leg) {
      const lt = add(leg.knee, rot(leg.shinQ, SHIN_BLADE.t)), lq = mul(leg.shinQ, q(sideE(SHIN_BLADE.e, side)));
      t = add(times(t, 1 - lock), times(lt, lock));
      Q = lock >= 1 ? lq : slerpQ(Q, lq, lock);
    }
    part(n, t, Q, p.hands);
  };
  hand('hand_r_a', 'hRA', -1, 0, p.lockR, legs.r);
  hand('hand_r_b', 'hRB', -1, 1.7);
  hand('hand_l_a', 'hLA', 1, 3.1, p.lockL, legs.l);
  hand('hand_l_b', 'hLB', 1, 4.4);
  part('flakes', add(fromWaist(ATTACH.flakes), rot(Tq, bob(.8, .04))), mul(Tq, q([0, 8 * Math.sin(w + .5), 0])), p.flakes);
  // wings: the overlay follows the forewing; scale 0 hides them (human form)
  const wingRoot = (a, side) => fromWaist([a[0] * side, a[1], a[2]]);
  part('fwing_l', wingRoot(ATTACH.fwing, 1), mul(Tq, q(sideE(p.fwL, 1))), p.fwS);
  part('fwing_r', wingRoot(ATTACH.fwing, -1), mul(Tq, q(sideE(p.fwR, -1))), p.fwS);
  part('fwglow_l', o.fwing_l.t, o.fwing_l.q, p.fwS * p.glow);
  part('fwglow_r', o.fwing_r.t, o.fwing_r.q, p.fwS * p.glow);
  part('hwing_l', wingRoot(ATTACH.hwing, 1), mul(Tq, q(sideE(p.hwL, 1))), p.hwS);
  part('hwing_r', wingRoot(ATTACH.hwing, -1), mul(Tq, q(sideE(p.hwR, -1))), p.hwS);
  // ribbon tendrils: from beside the chest, outside the body; the lower ribbon hangs from the end of the upper one
  for (const [s, side, U, L] of [['l', 1, 'tuL', 'tlL'], ['r', -1, 'tuR', 'tlR']]) {
    const root = fromWaist([ATTACH.tendril[0] * side, ATTACH.tendril[1], ATTACH.tendril[2]]);
    const uq = mul(Tq, q(sideE(p[U], side)));
    const end = add(root, times(rot(uq, [TENDRIL_END[0] * side, TENDRIL_END[1], TENDRIL_END[2]]), PART_SCALE.tendril_ul / 16 * p.tS));
    part('tendril_u' + s, root, uq, p.tS);
    part('tendril_l' + s, end, mul(uq, q(sideE(p[L], side))), p.tS);
  }
  part('core', fromWaist(ATTACH.core), Tq, p.core);
  // root transform, then visibility about the body centre
  const R0 = q(p.rot);
  for (const v of Object.values(o)) {
    v.t = add(add(ROOT_PIVOT, rot(R0, sub(v.t, ROOT_PIVOT))), p.pos);
    v.q = mul(R0, v.q);
  }
  for (const L of Object.values(legs)) L.hoof = add(add(ROOT_PIVOT, rot(R0, sub(L.hoof, ROOT_PIVOT))), p.pos);
  if (p.vis !== 1) {
    const c = add(ROOT_PIVOT, p.pos);
    for (const v of Object.values(o)) { v.t = add(c, times(sub(v.t, c), p.vis)); v.s = times(v.s, p.vis); }
  }
  Object.defineProperty(o, '_legs', {value: legs, enumerable: false});
  return o;
}
function slerpQ(a, b, t) {
  let d = a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3];
  if (d < 0) { b = b.map(x => -x); d = -d; }
  if (d > .9995) { const r = a.map((x, i) => x + (b[i] - x) * t), m = Math.hypot(...r); return r.map(x => x / m); }
  const th = Math.acos(d), s = Math.sin(th);
  return a.map((x, i) => (x * Math.sin((1 - t) * th) + b[i] * Math.sin(t * th)) / s);
}
// Rig frame -> display transform {t, q, s} with the part's display scale applied.
export function toDisplay(name, v) {
  const k = PART_SCALE[name];
  return {t: toDisplayT(v.t), q: toDisplayQ(v.q), s: v.s.map(x => x * k)};
}
// Lowest hoof tip height of a solved pose (blocks above the anchor's floor).
export const toeHeight = o => Math.min(o._legs.l.hoof[1], o._legs.r.hoof[1]);
export {unit};
