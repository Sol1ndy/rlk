// LEGS region of the 야타용왕 (Azhdaha) rig: the fore legs (upper arm, engraved stone bracer with gold studs and
// amber elbow crystals, paw with 4 talons + a dew claw) and the hind legs (haunch, ribbed gaiter with the orange heel
// spur, foot with 3 talons + 1), plus the phase-2 glow overlays of the bracers and gaiters (model.md §3.7, §3.8, §4.2,
// §7.3 option 2). Region interface: see azhdaha_body.mjs. Paired parts are authored for the LEFT leg (+X = outer) and
// mirrored for the right (azhdaha_shape mirrorX).
//
// Part frames (azhdaha_pose.mjs solve): uarm / bracer / thigh / gaiter hang along -Y from their joint toward the next
// joint (front = -Z); paw and foot sit at the wrist / hock with their own orientation (sole at y -0.5 / -0.72).
import {loft, slab, crossCards, rockBox, toUnits, retex, mirrorX, stroke, registerTile, registerWrap} from './azhdaha_shape.mjs';
import {PART_SCALE, ARM, LEG, J} from './azhdaha_pose.mjs';
import {PAL, LOOK_PAL, C, clamp, smooth, mix, lift, sink, N, spriteSize, onRect, TRANSPARENT, hidePx, ramp} from './azhdaha_materials.mjs';
import {cardX, cardZ} from './mboss_model_lib.mjs';

export const REGION = 'legs';
export const PARTS = [
  ['uarm_l', 'uarm_l', 13], ['bracer_l', 'bracer_l', 13], ['paw_l', 'paw_l', 13],
  ['uarm_r', 'uarm_r', 13], ['bracer_r', 'bracer_r', 13], ['paw_r', 'paw_r', 13],
  ['thigh_l', 'thigh_l', 13], ['gaiter_l', 'gaiter_l', 13], ['foot_l', 'foot_l', 13],
  ['thigh_r', 'thigh_r', 13], ['gaiter_r', 'gaiter_r', 13], ['foot_r', 'foot_r', 13],
  ['glow_bracer_l', 'empty', 15], ['glow_bracer_r', 'empty', 15], ['glow_gaiter_l', 'empty', 15], ['glow_gaiter_r', 'empty', 15],
];
const LOOKS_EL = ['hydro', 'pyro'];
const sfx = look => (look ? '_' + look : '');
for (const n of ['bracer', 'gaiter', 'bracer_hydro', 'gaiter_hydro', 'bracer_pyro', 'gaiter_pyro', 'bracer_mask', 'gaiter_mask']) registerWrap(n);
for (const l of ['', '_hydro', '_pyro']) registerTile('pawstone' + l, 64, 64, 32);
registerTile('pad', 32, 32, 32);
const R4 = (o, f, i, b) => [o, f, i, b];     // r = [outer +X, front -Z, inner -X, back +Z] for axis y

// ---- fore leg ---------------------------------------------------------------------------------------------------------------
function uarm() {
  // a big rounded muscle mass from inside the shoulder to the bracer top (length ARM[0])
  const a = ARM[0];
  return loft('y', [{a: .8, r: R4(.5, .55, .45, .55)}, {a: .3, r: R4(.82, .86, .7, .88)}, {a: -.3, r: R4(.92, .86, .74, .9)}, {a: -.85, r: R4(.86, .78, .7, .82)},
    {a: -a, r: R4(.72, .66, .62, .7)}, {a: -a - .35, r: .55}], {tex: 'hide_lg', seed: 61, caps: '+'});
}
// the bracer column: an 8-sided rounded column, flared rim at the elbow, wrap sprite with the carved lines
const BR = [{a: .3, r: .58, box: .35}, {a: .08, r: .8, box: .35}, {a: -.12, r: .74, box: .35}, {a: -.9, r: .78, box: .35}, {a: -1.6, r: .76, box: .35}, {a: -ARM[1] - .1, r: .68, box: .35}];
function bracer(look) {
  const els = loft('y', BR, {n: 8, tex: 'bracer' + sfx(look), ledgeTex: 'pawstone' + sfx(look), seed: 71});
  // gold studs on the front face near the top
  for (const x of [-.32, 0, .32]) els.push(rockBox([x - .08, -.42, -.9], [x + .08, -.26, -.74], 'gold', {seed: x * 10}));
  els.push(...elbowCrystals());
  return els;
}
// 3-4 amber hexagonal prisms jutting back and up from the elbow: crossed cards (side profile + a card tilted back
// 45 degrees showing the prism face-on) round a thin core box tilted the same way.
function prism([x, y, z], L, w, tilt = -45) {
  const els = [];
  const rectX = {Z0: z - .15 * L, Z1: z + .85 * L, Y0: y, Y1: y + .85 * L};
  els.push(cardX('crystal_lean', x, rectX));
  els.push(cardZ('crystal_up', z, {X0: x - w / 2, X1: x + w / 2, Y0: y, Y1: y + L}, {rot: ['x', tilt, [x, y, z]]}));
  els.push(rockBox([x - w * .22, y, z - w * .22], [x + w * .22, y + L * .8, z + w * .22], 'crystal', {rot: ['x', tilt, [x, y, z]]}));
  return els;
}
registerTile('crystal', 32, 32, 48);
function elbowCrystals() {
  return [...prism([.35, -.05, .45], 1.0, .3), ...prism([-.05, .0, .55], .9, .28), ...prism([.6, -.3, .25], .75, .24), ...prism([.15, -.35, .6], .65, .22)];
}
// paw: a broad pad mass, 4 toes with pale pads, 4 big curved talons and a dew claw on the inside
const TOES = [-.62, -.21, .21, .62];
// Talon: one canonical hooked claw (side profile) scaled per toe: a card pair on its sides painted with the same
// shape (talon_card), over a core of boxes. Normalized frame: u 0 (tip, front) .. 1 (root, back), v 0 (tip) .. 1 (top).
const TALON_PTS = Array.from({length: 13}, (_, i) => { const t = i / 12; return [0, 1].map(k => (1 - t) ** 2 * [.9, .66][k] + 2 * (1 - t) * t * [.36, .9][k] + t * t * [.05, .04][k]); });
const TALON_S = stroke(TALON_PTS, t => .26 * (1 - t) ** .85 + .012);
const talonSdN = (u, v) => TALON_S.sd(u, v);
function talon(x, root, L, h0, look) {
  // root [z, y] = the back-top of the claw (where it leaves the toe); the claw reaches L forward and h0 * 2.2 down
  const [z0, y0] = root, H = h0 * 1.7;
  const rect = {u0: z0 - L, u1: z0 + .08 * L, v0: y0 - H * .75, v1: y0 + H * .25};
  const W = rect.u1 - rect.u0, Hh = rect.v1 - rect.v0;
  const sd = (u, v) => talonSdN((u - rect.u0) / W, (v - rect.v0) / Hh) * Math.min(W, Hh);
  return slab({plane: 'x', at: x, rect, sd, half: .1 * Math.min(1.4, h0 / .3 + .3), sprite: 'talon_card' + sfx(look), edge: 'talon' + sfx(look), cell: .07, inset: .5});
}
registerTile('talon_hydro', 32, 32, 48); registerTile('talon_pyro', 32, 32, 48);
function paw(look) {
  const ps = 'pawstone' + sfx(look);
  const els = loft('z', [{a: .55, r: [.55, .2, .55, .35], c: [0, -.12]}, {a: .2, r: [.84, .32, .84, .4], c: [0, -.1]}, {a: -.35, r: [.9, .27, .9, .27], c: [0, -.23]},
    {a: -.8, r: [.86, .2, .86, .2], c: [0, -.3]}], {tex: (k, th) => (Math.sin(th * Math.PI / 180) < -.6 ? 'pad' : ps), caps: '-+', seed: 81});
  for (const x of TOES) {
    els.push(...loft('z', [{a: -.6, r: [.2, .17, .2, .17], c: [x, -.3]}, {a: -.95, r: [.19, .16, .19, .16], c: [x, -.32]}, {a: -1.12, r: [.14, .12, .14, .12], c: [x, -.33]}],
      {n: 8, tex: (k, th) => (Math.sin(th * Math.PI / 180) < -.5 ? 'pad' : ps), caps: '+', seed: 83 + x * 10}));
    els.push(...talon(x, [-.98, -.15], .62, .3, look));
  }
  // dew claw on the inner side (-X for the left paw)
  els.push(...talon(-.9, [-.15, -.12], .32, .17, look));
  return els;
}

// ---- hind leg ---------------------------------------------------------------------------------------------------------------
function thigh() {
  const a = LEG[0];
  return loft('y', [{a: 1.0, r: R4(.75, .8, .6, .95)}, {a: .45, r: R4(1.15, 1.0, .85, 1.3)}, {a: -.2, r: R4(1.2, .95, .85, 1.2)}, {a: -.8, r: R4(1.0, .85, .78, .95)},
    {a: -a, r: R4(.72, .68, .62, .7)}, {a: -a - .3, r: .55}], {tex: 'hide_lg', seed: 91, caps: '+'});
}
// the gaiter: the knee in hide, then 5 stacked stone rings (4-5 horizontal ribs, model.md §3.8)
const RINGS = (() => { const out = []; const y0 = -.7, y1 = -LEG[1] - .1, n = 5, h = (y0 - y1) / n;
  for (let i = 0; i <= n; i++) { const y = y0 - i * h; out.push({a: y, r: .64 - .03 * i / n, box: .15}); if (i < n) out.push({a: y - h * .18, r: .69 - .03 * i / n, box: .15}, {a: y - h * .82, r: .69 - .03 * i / n, box: .15}); }
  return out; })();
function gaiter(look) {
  const els = loft('y', [{a: .35, r: .5}, {a: .1, r: .66}, {a: -.35, r: .64}, {a: -.72, r: .6}], {tex: 'hide', seed: 101, caps: '-'});
  els.push(...loft('y', RINGS, {tex: 'gaiter' + sfx(look), ledgeTex: 'gaiter' + sfx(look), seed: 103, caps: '-+'}));
  // the orange heel spur on the back of the gaiter, jutting back and up
  els.push(...prism([0, -1.55, .55], .8, .26, -45));
  return els;
}
const FOOT_TOES = [[.48, .3], [0, .32], [-.48, .3], [-.74, .16]];
function foot(look) {
  const ps = 'pawstone' + sfx(look);
  const els = loft('z', [{a: .45, r: [.55, .45, .55, .45], c: [0, -.2]}, {a: .15, r: [.72, .5, .72, .55], c: [0, -.17]}, {a: -.35, r: [.78, .32, .78, .35], c: [0, -.37]},
    {a: -.85, r: [.74, .22, .74, .22], c: [0, -.5]}], {tex: (k, th) => (Math.sin(th * Math.PI / 180) < -.6 ? 'pad' : ps), caps: '-+', seed: 111});
  for (const [x, h] of FOOT_TOES) {
    const small = h < .2;
    els.push(...loft('z', [{a: small ? -.5 : -.7, r: [.18, .15, .18, .15], c: [x, -.5]}, {a: small ? -.75 : -1.05, r: [.16, .13, .16, .13], c: [x, -.52]}], {n: 8, tex: ps, caps: '+', seed: 113 + x * 10}));
    els.push(...talon(x, [small ? -.72 : -1.0, small ? -.5 : -.36], small ? .32 : .55, h, look));
  }
  return els;
}

// ---- glow overlays (tinted white line masks 0.025 b proud, front and sides only) -------------------------------------------
const glowBracer = () => loft('y', BR.slice(1, 5), {n: 8, tex: 'bracer_mask', grow: .025, ledges: false, tint: true, skip: k => k >= 5});
const glowGaiter = () => loft('y', RINGS, {tex: 'gaiter_mask', grow: .025, ledges: false, tint: true, skip: k => k >= 10 && k <= 14});

// ---- region exports -------------------------------------------------------------------------------------------------------------
const U = (part, els) => toUnits(els, PART_SCALE[part]);
export function models() {
  const M = {};
  const pair = (name, els) => { M[name + '_l'] = U(name + '_l', els); M[name + '_r'] = U(name + '_r', mirrorX(els)); };
  pair('uarm', uarm()); pair('thigh', thigh());
  for (const look of [null, ...LOOKS_EL]) {
    const s = sfx(look);
    for (const [n, f] of [['bracer', bracer], ['paw', paw], ['gaiter', gaiter], ['foot', foot]]) {
      const els = f(look);
      M[n + '_l' + s] = U(n + '_l', els); M[n + '_r' + s] = U(n + '_r', mirrorX(els));
    }
  }
  pair('glow_bracer', glowBracer()); pair('glow_gaiter', glowGaiter());
  return M;
}
const legLook = p => ({geo: p, hydro: p + '_hydro', pyro: p + '_pyro'});
export const LOOKS = {
  legs: Object.fromEntries([...['bracer', 'paw', 'gaiter', 'foot'].flatMap(n => [n + '_l', n + '_r']).map(p => [p, legLook(p)]),
    ...['glow_bracer_l', 'glow_bracer_r', 'glow_gaiter_l', 'glow_gaiter_r'].map(p => [p, {geo: 'empty', hydro: p + '_hydro', pyro: p + '_pyro'}])]),
};
export const TINTED = Object.fromEntries(['glow_bracer_l', 'glow_bracer_r', 'glow_gaiter_l', 'glow_gaiter_r'].flatMap(p => LOOKS_EL.map(l => [p + '_' + l, [p, LOOK_PAL[l].tint]])));
export const LOOK_BRIGHT = {legs: {hydro: {}, pyro: {}}};

// ---- sprites ----------------------------------------------------------------------------------------------------------------------
// Wrap sprites: u = azimuth / 360 from the outer side (+X) through the front (u .25) and the inner side (u .5) to the
// back (u .75); v from the top down. Carved lines are light grooves in dark stone (phase 1) or the element glow.
const BRACER_STONE = {null: PAL.bracer, hydro: LOOK_PAL.hydro.stone, pyro: LOOK_PAL.pyro.stone};
function bracerLine(u, v) {
  // distance (sprite units, ~blocks/5) to the carved pattern: rim lines, a zigzag band round the column, a diamond glyph
  // with inner lines on the front, square meander hooks on the outer and inner faces
  const x = u * 5.0, y = v * 2.2;               // ~blocks round the circumference / down the column
  let d = Math.min(Math.abs(y - .3), Math.abs(y - 2.0));
  const zz = .75 + .16 * Math.abs(((x * 1.6) % 1 + 1) % 1 - .5) * 4 - .16;
  d = Math.min(d, Math.abs(y - zz), Math.abs(y - (zz + .55)));
  const fx = x - 1.25, fy = y - 1.45;           // front face centre (u .25)
  const dia = Math.abs(fx) + Math.abs(fy);
  d = Math.min(d, Math.abs(dia - .42), Math.abs(dia - .22) + (Math.abs(fx) < .05 ? 0 : .0));
  for (const cx of [.15, 2.65]) {
    const hx = x - cx, hy = y - 1.55, sq = Math.max(Math.abs(hx), Math.abs(hy));
    if (sq < .3) d = Math.min(d, Math.abs(sq - .26), Math.abs(sq - .14) + (hx > 0 && hy < 0 ? 1 : 0), Math.abs(hx) < .02 && hy > -.14 ? 0 : 9);
  }
  return d;
}
function bracerPaint(look) {
  const R = BRACER_STONE[look], L = look ? LOOK_PAL[look] : null;
  return (s, t) => {
    const u = s * 256, v = t * 112;
    let c = R((look ? .6 : .42) + .2 * (N.a(u * .05, v * .05) - .5) + .1 * (N.c(u * .2, v * .2) - .5));
    // vertical slab joints between the 8 faces and a soft light/shade per face
    const f = (s * 8) % 1;
    if (f < .03 || f > .97) c = sink(c, .45);
    c = mix(c, R(.15), .18 * Math.max(0, Math.cos((s - .2) * Math.PI * 2)));
    if (t < .06) c = lift(c, .25);                                             // the lit rim at the top
    const d = bracerLine(s, t);
    if (d < .035) c = L ? L.glow(.1 + d * 12) : mix(PAL.bracer(.05), PAL.bracer(.25), d / .035);
    else if (d < .06) c = L ? mix(c, L.glow(.7), .45 * (1 - (d - .035) / .025)) : sink(c, .3);
    // cracks
    if (Math.abs(N.e(s * 9, t * 4) - .5) < .012) c = sink(c, .4);
    return c;
  };
}
const linesMask = lineFn => (s, t) => { const d = lineFn(s, t); return d < .035 ? [255, 255, 255, 255] : d < .065 ? [255, 255, 255, Math.round(255 * (1 - (d - .035) / .03))] : TRANSPARENT; };
const GAITER_STONE = {null: PAL.gaiter, hydro: LOOK_PAL.hydro.stone, pyro: LOOK_PAL.pyro.stone};
function gaiterLine(u, v) {
  // the rings: 5 bands down the gaiter; on each ring a short engraved meander / zigzag segment
  const ring = v * 5, k = Math.floor(ring), r = ring - k;
  const x = u * 4.2;
  let d = 9;
  if (r > .25 && r < .75) {
    const yy = (r - .5) * .84;
    const zz = .12 * (Math.abs(((x * 2 + k * .5) % 1 + 1) % 1 - .5) * 4 - 1);
    d = Math.abs(yy - zz);
    if (Math.abs(((x + k * .3) % 1.05 + 1.05) % 1.05 - .52) < .2 && k % 2) d = Math.min(d, Math.abs(Math.abs(yy) - .12));
  }
  return d;
}
function gaiterPaint(look) {
  const R = GAITER_STONE[look], L = look ? LOOK_PAL[look] : null;
  return (s, t) => {
    const u = s * 256, v = t * 96;
    const ring = t * 5, r = ring - Math.floor(ring);
    let c = R((look ? .6 : .35) + .15 * (N.b(u * .06, v * .06) - .5));
    c = mix(c, R(.1), .3 * Math.max(0, Math.sin(r * Math.PI)) * Math.max(0, Math.cos((s - .2) * Math.PI * 2)));
    if (r < .12 || r > .88) c = sink(c, .35);
    const d = gaiterLine(s, t);
    if (d < .03) c = L ? L.glow(.15 + d * 15) : mix(c, PAL.groove(.4), .75);
    else if (L && d < .055) c = mix(c, L.glow(.6), .4);
    return c;
  };
}
function pawstone(look) {
  const R = BRACER_STONE[look], L = look ? LOOK_PAL[look] : null;
  return (s, t) => { let c = R((look ? .68 : .48) + .2 * (N.d(s * 6, t * 6) - .5)); const cr = Math.abs(N.f(s * 2.5, t * 2.5) - .5); if (cr < .02) c = L ? L.glow(.3) : sink(c, .4); return c; };
}
const TALON = {null: PAL.talon, hydro: ramp(['#5A6478', '#3A4258', '#262C40', '#181C2A', '#0E1018']), pyro: ramp(['#7A3A30', '#55241E', '#3A1814', '#26100D', '#160A08'])};
function talonCard(look) {
  const R = TALON[look];
  return (s, t) => {
    const u = s, v = 1 - t, d = talonSdN(u, v);
    if (d > 0) return TRANSPARENT;
    const n = TALON_S.near(u, v);
    let c = R(.2 + .5 * (1 - n.t) * .6 + .15 * (N.a(s * 5, t * 5) - .5));
    if (n.s > 0) c = lift(c, .12);                         // the upper face catches the light
    if (n.t > .78) c = mix(c, PAL.talon(0), (n.t - .78) / .22 * .8);   // pale tip
    if (d > -.015) c = sink(c, .3);
    return c;
  };
}
// amber crystal cards: the prism leaning back (side) and upright (face-on); tip amber, base orange-red (model.md §3.6)
function crystalCard(lean) {
  return (s, t) => {
    const y = 1 - t, x = lean ? s - .15 - .7 * y : s - .5;
    const w = .22 * (y < .78 ? 1 : (1 - y) / .22);
    if (Math.abs(x) > w || y < 0) return TRANSPARENT;
    let c = PAL.crystal(clamp(.9 - y * .95));
    if (x > 0) c = sink(c, .18);
    if (Math.abs(x) < w * .12) c = lift(c, .3);
    if (w - Math.abs(x) < .03) c = PAL.crystal(.95);
    return c;
  };
}
export function sprites() {
  const S = {};
  for (const look of [null, ...LOOKS_EL]) {
    const s = sfx(look);
    S['bracer' + s] = [256, 112, bracerPaint(look), false];
    S['gaiter' + s] = [256, 96, gaiterPaint(look), false];
    S['pawstone' + s] = [64, 64, pawstone(look), false];
    S['talon_card' + s] = [64, 48, talonCard(look), false];
  }
  S.talon_hydro = [32, 32, (u, v) => TALON.hydro(.3 + .5 * v), false];
  S.talon_pyro = [32, 32, (u, v) => TALON.pyro(.3 + .5 * v), false];
  S.bracer_mask = [256, 112, linesMask(bracerLine), true];
  S.gaiter_mask = [256, 96, linesMask(gaiterLine), true];
  S.pad = [32, 32, (u, v) => PAL.pad(.3 + .5 * N.b(u * 4, v * 4)), false];
  S.crystal_lean = [32, 64, crystalCard(true), false];
  S.crystal_up = [32, 64, crystalCard(false), false];
  S.crystal = [32, 32, (u, v) => PAL.crystal(.3 + .4 * v), false];
  return S;
}
