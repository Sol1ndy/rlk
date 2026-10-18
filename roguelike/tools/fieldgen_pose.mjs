// Pose -> part transforms for the experimental field generator (실험성 역장 발생 장치) rig: a set of free bodies round
// one root (scratchpad mb3/understand/model.md §0, §7.6, §8). Shared math: mboss_rig_math.mjs.
//
// Rig frame: +X = the device's LEFT, +Y up, -Z forward (the keystone iris side), blocks; the origin is the floor
// point under the ring axis (the boss body). Euler triples are degrees (X, then Y, then Z; mboss_rig_math q): pitch +
// tips the front up, yaw + turns the front toward the device's left (+X), roll + tips the top toward the left.
// Azimuths (az) are degrees round the ring axis from the front (-Z) toward the left (+X).
//
// A pose is a full set of channels (DEFAULT_POSE below merged with the clip keys):
//   pos [0, H, 0]      ring centre (H the hover height; x / z stay 0: the module moves the body)
//   rot [p, y, r]      root rotation about the ring centre (tilts, rolls, nose-down runs)
//   vis                everything scaled about the ring centre (warp, death)
//   haloO haloE haloS  halo offset (from the ring centre), euler, scale; halo2O halo2S the inner glow ring
//   hub                keystone iris spike roll about the forward axis (0 down, 180 up)
//   coreO coreE coreS  core group offset, euler and scale (sphere, eye, arch, brim, glows); eye [pitch, yaw] the eye aim on
//                      the sphere; arch [p, y, r] the gear ring; brim [pitch, roll] the brim tilt
//   glowS shellS       core_glow (charge / flash / gold) and core_shell (the field bubble) scales
//   spLO spLE          left spike: pivot (the dock, the centre of its X frame) and euler; spRO spRE the right one
//                      (author them with spikes(): the right side mirrors [x,y,z] -> [-x,y,z], [p,y,r] -> [p,-y,-r])
//   meAz meR meY meE   eye medallion: azimuth, radius, height and euler in its radial frame (local -Z = radially
//                      out); mgAz mgR mgY mgE the gear medallion (medals() mirrors az and yaw)
//   drR drY drS drSp drAz   drill pods: radius, height, scale, spread from the +-X axis (45 = azimuths +-45 / +-135),
//                      orbit offset
//   plY plS pl2Y pl2S  plate / plate2 height and scale
//   pdY pdSw           pendulum hang point height and swing [pitch, roll]; the pendulum hangs plumb (it ignores the
//                      root pitch and roll); pglow its Ousia flame scale
//   blLen blW blPd blYo  beam_l (from the eye medallion): length, width (b), angle from straight down, yaw offset
//                      from the radial direction; brLen brW brPd brYo beam_r (from the gear medallion)
//   colLen colW        column length and width from the core centre; colDir 'down' | 'up' (discrete)
//   twExt twT1Y twT1S twT2Y twT2S   tower column extension 0..1 and the two tier discs
//   wHalo wHalo2 wBrim wMedE wMedG wDrill wT1 wT2 wArch wPlate   spin rates (degrees per tick); the sampler integrates
//                      them per clip into whole turns (fieldgen_clips.mjs), solve() reads p.spin
//   lk glowLook beamLook colLook   discrete looks (fieldgen_clips.mjs)
import {add, sub, times, mul, q, rot, toDisplayT, toDisplayQ} from './mboss_rig_math.mjs';

// Display scale per part (blocks per 16 model units).
export const PART_SCALE = {
  ring: 2.4, ring_glow: 2.4, hub_eye: 1, halo: 1.25, halo2: 1,
  core: 1, core_eye: 1, core_arch: 1.1, core_brim: 1.3, core_glow: 1, core_shell: 1,
  spike_l: 1.4, spike_r: 1.4, medal_eye: 1, medal_gear: 1,
  drill_fl: 1, drill_fr: 1, drill_bl: 1, drill_br: 1,
  plate: 1.25, plate2: 1.25, pendulum: 1.6, pend_glow: 1.6,
  beam_l: 1, beam_r: 1, column: 1, tower_col: 2, tower_t1: 1.3, tower_t2: 1.4,
};
// The keystone iris sits on the socket in front of the band (ring units 23.7 x 0.15 b).
export const HUB_AT = [0, .05, -3.56];
export const CORE_R = 1.25;               // sphere radius, blocks
export const mirrorE = e => [e[0], -e[1], -e[2]];
const D2R = Math.PI / 180;
export const radial = az => [Math.sin(az * D2R), 0, -Math.cos(az * D2R)];
const qY = deg => q([0, deg, 0]);

export function solve(p) {
  const o = {}, s = p.spin || {};
  const part = (n, t, Q, sc = 1) => { o[n] = {t, q: Q, s: Array.isArray(sc) ? sc : [sc, sc, sc]}; };
  // ---- local transforms about the ring centre (root frame) ----
  part('ring', [0, 0, 0], [0, 0, 0, 1]);
  part('ring_glow', [0, 0, 0], [0, 0, 0, 1]);
  part('hub_eye', HUB_AT, q([0, 0, p.hub]));
  part('halo', p.haloO, mul(q(p.haloE), qY(s.halo || 0)), p.haloS);
  part('halo2', p.halo2O, qY(s.halo2 || 0), p.halo2S);
  // core group
  const Qc = q(p.coreE), c = p.coreO, cs = p.coreS;
  part('core', c, Qc, cs);
  part('core_eye', c, mul(Qc, q([p.eye[0], p.eye[1], 0])), cs);
  part('core_arch', c, mul(Qc, mul(qY(s.arch || 0), q(p.arch))), cs);
  part('core_brim', c, mul(Qc, mul(qY(s.brim || 0), q([p.brim[0], 0, p.brim[1]]))), cs);
  part('core_glow', c, Qc, p.glowS * cs);
  part('core_shell', c, Qc, p.shellS * cs);
  // spikes (pivot = the X frame centre = the dock)
  part('spike_l', p.spLO, q(p.spLE));
  part('spike_r', p.spRO, q(p.spRE));
  // medallions: polar position, orientation in the radial frame (local -Z = out), spin about the face axis
  const medal = (n, az, r, y, e, w) => {
    const pos = add(times(radial(az), r), [0, y, 0]);
    part(n, pos, mul(mul(qY(-az), q(e)), q([0, 0, w])));
    return pos;
  };
  const mE = medal('medal_eye', p.meAz, p.meR, p.meY, p.meE, s.medE || 0);
  const mG = medal('medal_gear', p.mgAz, p.mgR, p.mgY, p.mgE, s.medG || 0);
  // drill pods
  const pods = {drill_fl: 90 - p.drSp, drill_bl: 90 + p.drSp, drill_fr: -(90 - p.drSp), drill_br: -(90 + p.drSp)};
  for (const [n, a] of Object.entries(pods)) part(n, add(times(radial(a + p.drAz), p.drR), [0, p.drY, 0]), qY((s.drill || 0) + a), p.drS);
  // plates
  part('plate', [0, p.plY, 0], qY(s.plate || 0), p.plS);
  part('plate2', [0, p.pl2Y, 0], qY(-(s.plate || 0)), p.pl2S);
  // beams (from the medallions)
  const beam = (n, from, az, len, w, pd, yo) => {
    if (len < .02 || w < .01) { part(n, from, [0, 0, 0, 1], 0); return; }
    const dir = add(times([0, -1, 0], Math.cos(pd * D2R)), times(radial(az + yo), Math.sin(pd * D2R)));
    part(n, from, beamQ(dir), [w, len, w]);
  };
  beam('beam_l', mE, p.meAz, p.blLen, p.blW, p.blPd, p.blYo);
  beam('beam_r', mG, p.mgAz, p.brLen, p.brW, p.brPd, p.brYo);
  // column from the core centre (vertical in the device frame)
  if (p.colLen < .02) part('column', c, [0, 0, 0, 1], 0);
  else part('column', c, p.colDir === 'up' ? q([180, 0, 0]) : [0, 0, 0, 1], [p.colW, p.colLen, p.colW]);
  // tower
  part('tower_col', [0, 0, 0], qY(s.t1 || 0), p.twExt < .01 ? 0 : [1, p.twExt, 1]);
  part('tower_t1', [0, p.twT1Y, 0], qY(s.t1 || 0), p.twT1S);
  part('tower_t2', [0, p.twT2Y, 0], qY(s.t2 || 0), p.twT2S);
  // ---- root: position, rotation about the ring centre ----
  const R0 = q(p.rot), Ryaw = qY(p.rot[1]), C0 = p.pos;
  for (const v of Object.values(o)) { v.t = add(C0, rot(R0, v.t)); v.q = mul(R0, v.q); }
  // the pendulum and its flame hang plumb from their hang point (they keep only the root yaw)
  const hang = add(C0, rot(R0, [0, p.pdY, 0])), Qp = mul(Ryaw, q([p.pdSw[0], 0, p.pdSw[1]]));
  part('pendulum', hang, Qp);
  part('pend_glow', hang, Qp, p.pglow);
  // visibility about the ring centre
  if (p.vis !== 1) for (const v of Object.values(o)) { v.t = add(C0, times(sub(v.t, C0), p.vis)); v.s = times(v.s, p.vis); }
  Object.defineProperty(o, '_anchor', {value: {mE, mG, R0, C0}, enumerable: false});
  return o;
}
// Frame with model -Y along dir (the beams hang along -Y) and its card faces kept upright where possible.
function beamQ(dir) {
  const L = Math.hypot(...dir), Y = times(dir, -1 / L);
  let F = sub([0, 0, -1], times(Y, -Y[2]));
  if (Math.hypot(...F) < 1e-3) F = sub([1, 0, 0], times(Y, Y[0]));
  const Z = times(F, -1 / Math.hypot(...F)), X = [Y[1] * Z[2] - Y[2] * Z[1], Y[2] * Z[0] - Y[0] * Z[2], Y[0] * Z[1] - Y[1] * Z[0]];
  return basis(X, Y, Z);
}
function basis(X, Y, Z) {
  const m = [[X[0], Y[0], Z[0]], [X[1], Y[1], Z[1]], [X[2], Y[2], Z[2]]], tr = m[0][0] + m[1][1] + m[2][2];
  let s, r;
  if (tr > 0) { s = Math.sqrt(tr + 1) * 2; r = [(m[2][1] - m[1][2]) / s, (m[0][2] - m[2][0]) / s, (m[1][0] - m[0][1]) / s, s / 4]; }
  else if (m[0][0] > m[1][1] && m[0][0] > m[2][2]) { s = Math.sqrt(1 + m[0][0] - m[1][1] - m[2][2]) * 2; r = [s / 4, (m[0][1] + m[1][0]) / s, (m[0][2] + m[2][0]) / s, (m[2][1] - m[1][2]) / s]; }
  else if (m[1][1] > m[2][2]) { s = Math.sqrt(1 + m[1][1] - m[0][0] - m[2][2]) * 2; r = [(m[0][1] + m[1][0]) / s, s / 4, (m[1][2] + m[2][1]) / s, (m[0][2] - m[2][0]) / s]; }
  else { s = Math.sqrt(1 + m[2][2] - m[0][0] - m[1][1]) * 2; r = [(m[0][2] + m[2][0]) / s, (m[1][2] + m[2][1]) / s, s / 4, (m[1][0] - m[0][1]) / s]; }
  const n = Math.hypot(...r);
  return r.map(x => x / n);
}
// Rig frame -> display transform {t, q, s} with the part's display scale applied.
export function toDisplay(name, v) {
  const k = PART_SCALE[name];
  return {t: toDisplayT(v.t), q: toDisplayQ(v.q), s: v.s.map(x => x * k)};
}

// ---- pose helpers -----------------------------------------------------------------------------------------------------
// both spikes: o = the left pivot [x, y, z], e = the left euler (the right mirrors)
export const spikes = (o, e = [0, 0, 0], or = null, er = null) => ({spLO: o, spLE: e, spRO: or || [-o[0], o[1], o[2]], spRE: er || mirrorE(e)});
// both medallions: the eye at az, the gear at -az (or gaz), the gear's euler mirrored
export const medals = (az, r, y, e = [0, 90, 0], g = {}) => ({meAz: az, meR: r, meY: y, meE: e,
  mgAz: g.az ?? -az, mgR: g.r ?? r, mgY: g.y ?? y, mgE: g.e ?? mirrorE(e)});
export const FACE_FRONT = [0, 90, 0];      // a medallion at az +90 facing the front (the gear mirrors it)

// ---- rest poses of the seven body configurations (model.md §8) ---------------------------------------------------------
// The dock: the medallion centre and the spike pivot at each ring end (the X frame round the medallion).
export const DOCK = [3.6, .05, 0];
export const RATES = {wHalo: 2.25, wHalo2: -4.5, wBrim: 4.5, wMedE: 4.5, wMedG: -6.75, wDrill: 11.25, wT1: 2.25, wT2: -2.25, wArch: 0, wPlate: .75};
const STILL = Object.fromEntries(Object.keys(RATES).map(k => [k, 0]));
export const CRUISE = {
  pos: [0, 4.5, 0], rot: [0, 0, 0], vis: 1,
  haloO: [0, 1.6, 0], haloE: [0, 0, 0], haloS: 1, halo2O: [0, 1.35, 0], halo2S: 1,
  hub: 0,
  coreO: [0, 0, 0], coreE: [0, 0, 0], coreS: 1, eye: [0, 0], arch: [-35, 0, 0], brim: [-16, 14],
  glowS: 0, shellS: 1,
  ...spikes(DOCK),
  ...medals(90, DOCK[0], DOCK[1]),
  drR: 2.95, drY: -.95, drS: 1, drSp: 45, drAz: 0,
  plY: -1.57, plS: 1, pl2Y: -1.45, pl2S: 1,
  pdY: -1.85, pdSw: [0, 0], pglow: 0,
  blLen: 0, blW: .6, blPd: 48, blYo: 0, brLen: 0, brW: .6, brPd: 48, brYo: 0,
  colLen: 0, colW: .9, colDir: 'down',
  twExt: 0, twT1Y: 1.35, twT1S: 0, twT2Y: 2.0, twT2S: 0,
  ...RATES,
  lk: 'el', glowLook: 'charge', beamLook: 'gold', colLook: 'gold',
};
export const DEFAULT_POSE = CRUISE;
// Folded on the floor before the entrance: the ring edge-on 2.15 b up, halo and inner ring folded into the hole, the
// core sunk into the ring with the arch flat, two pods tucked under each ring end, only the dagger below.
export const DORMANT = {
  ...CRUISE, ...STILL, pos: [0, 2.15, 0],
  haloO: [0, .1, 0], haloS: 0, halo2O: [0, .1, 0], halo2S: 0,
  coreO: [0, -.12, 0], coreS: .62, arch: [90, 0, 0], brim: [-10, 0],
  drR: 3.15, drY: -.5, drS: .72, drSp: 12,
  plY: -.86, plS: .8, pl2Y: -.7, pl2S: 0,
  pdY: .12,
};
// Field (역장): the stack opens downward; the core hangs with the eye out, the medallions beside it on the link beams,
// the pods at core level, the plates spread round the violet column, two violet halos (look/field).
export const FIELD = {
  ...CRUISE, pos: [0, 5.8, 0],
  haloO: [0, 1.55, 0], halo2O: [0, 1.3, 0],
  coreO: [0, -1.7, 0], arch: [0, 0, 0], brim: [-30, 10], wArch: 3,
  ...medals(90, 3.85, -1.7),
  drR: 3.5, drY: -1.9,
  plY: -3.22, plS: 1.4, pl2Y: -3.06, pl2S: 1.0,
  pdY: -3.4, pglow: 1,
  blLen: 2.5, blW: .32, blPd: 90, blYo: 180, brLen: 2.5, brW: .32, brPd: 90, brYo: 180, beamLook: 'link',
  colLen: 1.95, colW: .62, colLook: 'violet',
};
// Core-up (지면 충격): the core lifted 0.4 D over the ring, the three eyes in a row with their spikes up, roll 10.
export const COREUP = {
  ...CRUISE, pos: [0, 5.0, 0], rot: [0, 0, 10],
  hub: 180,
  coreO: [0, 2.8, 0], arch: [0, 0, 0], brim: [-22, -12],
  ...spikes([3.6, .3, 0], [0, 0, 90]),
  ...medals(90, 3.6, .3),
  drR: 2.4, drY: -1.0,
  plY: -2.95, pl2Y: -2.75,
  pdY: -2.6, pglow: 1,
};
// Tower (파쇄): the column with its two tiers telescoped up out of the hole, the halo x1.7 on top, the medallions
// docked on the column top, the end spikes and the iris spike up.
export const TOWER = {
  ...CRUISE,
  haloO: [0, 3.2, 0], haloS: 1.7, halo2O: [0, 2.5, 0],
  hub: 180,
  coreO: [0, -.4, 0], arch: [0, 0, 0],
  ...spikes(DOCK, [0, 0, 45]),
  ...medals(90, .5, 3.15),
  plY: -1.9, pl2Y: -1.75,
  pdY: -2.2, pglow: 1,
  twExt: 1, twT1Y: 1.35, twT1S: 1, twT2Y: 2.0, twT2S: 1,
};
// Laser (코어): the medallions dropped to r 2.8, 2 b under the ring, faces down-out along the gold beams (48 degrees
// from vertical: the floor spots on r 5.5 at H 4.5), counter-orbiting in the clip.
export const LASER = {
  ...CRUISE,
  ...medals(90, 2.8, -2.0, [-42, 0, 0]),
  blLen: 3.74, blW: .7, blPd: 48, blYo: 0, brLen: 3.74, brW: .7, brPd: 48, brYo: 0,
};
// Deployed (lances): the spikes with the medallions in their X frames far out on both sides, the core hanging.
export const DEPLOYED = {
  ...FIELD, pos: [0, 5.6, 0],
  ...spikes([5.6, -.6, 0]),
  ...medals(90, 5.6, -.6),
  drR: 3.8, drY: -1.2,
  plY: -3.0, pl2Y: -2.6, pdY: -3.2,
  blLen: 0, brLen: 0,
};
export const FORMS = {dormant: DORMANT, cruise: CRUISE, field: FIELD, coreup: COREUP, tower: TOWER, laser: LASER, deployed: DEPLOYED};
