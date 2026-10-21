// Geometry and forward kinematics of the Raiden rig (마가츠 미타케 나루카미노 미코토): both forms on one superset rig of
// 30 item_display parts (scratchpad rd/plan.md §C.1, §C.2, §C.4), plus the props (separate entities, §C.2).
//
// Frames. Models are authored in the A-frame of mboss_model_lib.mjs (+X = her LEFT, +Y up, -Z forward, model units
// about the display pivot [8, 8, 8]); the skin boxes keep the old rig's model-space boxes and UV layout (64 x 64 player
// skin, second layer inflated). Poses are solved in the rig frame (+X her left, +Y up, -Z forward, blocks; the origin is
// the floor point under her hips) and converted by toDisplay (z mirror, mboss_rig_math.mjs) with PART_SCALE applied.
//
// Parts (30; plan §C.4): 10 body boxes (looks: shogun / tenma), Shogun 6 (braid, drape, weapon, weapon_fx, halo,
// aura), Tenma 14 (disc, g_upper, g_fore, g_hand, glaive, glaive_fx, ra1_up/ra1_fo .. ra3_up/ra3_fo, gaunt_l, gaunt_r).
// The braid shows in both forms; the other Shogun extras hide in the Tenma form (pose sS = 0) and the Tenma parts in
// the Shogun form (pose tS = 0).
import {abox, cardZ, cardX, cardY, lathe, turned, mirrorModel, checkBounds, r4} from './mboss_model_lib.mjs';
import {add, sub, times, len, unit, mul, q, rot, aimQ, ik, basisQ, cross, dot, perp, steadyPerp, toDisplayT, toDisplayQ} from './mboss_rig_math.mjs';

// ---- part table ---------------------------------------------------------------------------------------------------------
// [name, default item model (shogun look), block brightness, group]
export const PARTS = [
  ['head', 'head', 13, 'body'], ['body', 'body', 13, 'body'],
  ['right_arm', 'right_arm', 13, 'body'], ['right_forearm', 'right_forearm', 13, 'body'],
  ['left_arm', 'left_arm', 13, 'body'], ['left_forearm', 'left_forearm', 13, 'body'],
  ['right_leg', 'right_leg', 13, 'body'], ['right_shin', 'right_shin', 13, 'body'],
  ['left_leg', 'left_leg', 13, 'body'], ['left_shin', 'left_shin', 13, 'body'],
  ['braid', 'braid', 13, 'shared'], ['drape', 'drape', 13, 'shogun'], ['weapon', 'katana', 15, 'shogun'], ['weapon_fx', 'katana_fx', 15, 'shogun'],
  ['halo', 'halo', 15, 'shogun'], ['aura', 'aura', 15, 'shogun'],
  ['disc', 'disc', 14, 'tenma'], ['g_upper', 'g_upper', 14, 'tenma'], ['g_fore', 'g_fore', 14, 'tenma'], ['g_hand', 'g_hand', 14, 'tenma'],
  ['glaive', 'glaive', 14, 'tenma'], ['glaive_fx', 'glaive_fx', 15, 'tenma'],
  ['ra1_up', 'ra_up', 14, 'tenma'], ['ra1_fo', 'ra1_fo', 14, 'tenma'], ['ra2_up', 'ra_up', 14, 'tenma'], ['ra2_fo', 'ra2_fo', 14, 'tenma'],
  ['ra3_up', 'ra_up', 14, 'tenma'], ['ra3_fo', 'ra3_fo', 14, 'tenma'], ['gaunt_l', 'gaunt_l', 14, 'tenma'], ['gaunt_r', 'gaunt_r', 14, 'tenma'],
];
export const PART_NAMES = PARTS.map(p => p[0]);
export const BODY = PART_NAMES.slice(0, 10);
export const SHOGUN_EXTRA = ['drape', 'weapon', 'weapon_fx', 'halo', 'aura'];
export const TENMA_PARTS = PARTS.filter(p => p[3] === 'tenma').map(p => p[0]);
// Display scale per part, [x, y, z] in the part's own axes (skin boxes are stretched: slim arms, long legs).
const ARM = [.72, 1.05, .72], LEG = [.8, 1.15, .8];
export const PART_SCALE = {
  head: [.85, .85, .85], body: [.9, 1, .85], right_arm: ARM, right_forearm: ARM, left_arm: ARM, left_forearm: ARM,
  right_leg: LEG, right_shin: LEG, left_leg: LEG, left_shin: LEG,
  braid: [1, 1, 1], drape: [1, 1, 1], weapon: [1, 1, 1], weapon_fx: [1, 1, 1], halo: [1.25, 1.25, 1.25], aura: [2.4, 2.4, 2.4],
  disc: [1, 1, 1], g_upper: [1.5, 1.5, 1.5], g_fore: [1.5, 1.5, 1.5], g_hand: [1.4, 1.4, 1.4], glaive: [3.6, 3.6, 3.6], glaive_fx: [3.6, 3.6, 3.6],
  ra1_up: [1, 1, 1], ra1_fo: [1, 1, 1], ra2_up: [1, 1, 1], ra2_fo: [1, 1, 1], ra3_up: [1, 1, 1], ra3_fo: [1, 1, 1], gaunt_l: [1, 1, 1], gaunt_r: [1, 1, 1],
};

// ---- skin boxes (model space, the old rig's layout) ---------------------------------------------------------------------
const FACES6 = ['north', 'south', 'east', 'west', 'up', 'down'];
function skinFaces(tex, u, v, w, h, d, start = 0, end = h) {
  const f = (a, b, c, e) => ({uv: [a / 4, b / 4, c / 4, e / 4], texture: '#' + tex});
  return {east: f(u, v + d + start, u + d, v + d + end), north: f(u + d, v + d + start, u + d + w, v + d + end), west: f(u + d + w, v + d + start, u + 2 * d + w, v + d + end),
    south: f(u + 2 * d + w, v + d + start, u + 2 * d + 2 * w, v + d + end), up: f(u + d, v, u + d + w, v + d), down: f(u + d + w, v + d, u + d + 2 * w, v)};
}
const sb = (tex, a, b, uv, start, end, inflate = 0) => ({from: a.map(x => r4(x - inflate)), to: b.map(x => r4(x + inflate)), faces: skinFaces(tex, ...uv, start, end)});
// [from, to, base uv, overlay uv, rows start, rows end, overlay inflate]; pivots: head at the neck (box above it),
// body at the neck (box below), upper arm 2 px below its top, forearm / legs / shins at their tops.
const SKIN = {
  head: [[4, 8, 4], [12, 16, 12], [0, 0, 8, 8, 8], [32, 0, 8, 8, 8], 0, 8, .45],
  body: [[4, -4, 6], [12, 8, 10], [16, 16, 8, 12, 4], [16, 32, 8, 12, 4], 0, 12, .22],
  right_arm: [[6, 4, 6], [10, 10, 10], [40, 16, 4, 12, 4], [40, 32, 4, 12, 4], 0, 6, .22],
  right_forearm: [[6, 2, 6], [10, 8, 10], [40, 16, 4, 12, 4], [40, 32, 4, 12, 4], 6, 12, .22],
  left_arm: [[6, 4, 6], [10, 10, 10], [32, 48, 4, 12, 4], [48, 48, 4, 12, 4], 0, 6, .22],
  left_forearm: [[6, 2, 6], [10, 8, 10], [32, 48, 4, 12, 4], [48, 48, 4, 12, 4], 6, 12, .22],
  right_leg: [[6, 2, 6], [10, 8, 10], [0, 16, 4, 12, 4], [0, 32, 4, 12, 4], 0, 6, .22],
  right_shin: [[6, 2, 6], [10, 8, 10], [0, 16, 4, 12, 4], [0, 32, 4, 12, 4], 6, 12, .22],
  left_leg: [[6, 2, 6], [10, 8, 10], [16, 48, 4, 12, 4], [0, 48, 4, 12, 4], 0, 6, .22],
  left_shin: [[6, 2, 6], [10, 8, 10], [16, 48, 4, 12, 4], [0, 48, 4, 12, 4], 6, 12, .22],
};
const skinPart = (n, tex) => { const [a, b, uv, ov, s, e, inf] = SKIN[n]; return [sb(tex, a, b, uv, s, e), sb(tex, a, b, ov, s, e, inf)]; };

// ---- small helpers (A-frame) ----------------------------------------------------------------------------------------------
const crossCards = (sprite, c, w, h, y0) => [cardZ(sprite, c[2], {X0: c[0] - w / 2, X1: c[0] + w / 2, Y0: c[1] + y0, Y1: c[1] + y0 + h}),
  cardX(sprite, c[0], {Z0: c[2] - w / 2, Z1: c[2] + w / 2, Y0: c[1] + y0, Y1: c[1] + y0 + h})];
const sq = (sprite, c, s, plane = 'z', opt = {}) => (plane === 'z' ? cardZ(sprite, c[2], {X0: c[0] - s / 2, X1: c[0] + s / 2, Y0: c[1] - s / 2, Y1: c[1] + s / 2}, opt)
  : cardX(sprite, c[0], {Z0: c[2] - s / 2, Z1: c[2] + s / 2, Y0: c[1] - s / 2, Y1: c[1] + s / 2}, opt));
const LIMB_V = {vFrom: 0, vTo: 1, n: 8};
// Light ball joint: an 8-facet turned sphere in 4 bands (the shared knob() is 12 x 16 facets).
const ballJ = (c, R, tex, ledge, n = 8) => turned('y', c, [-R, -R * .72, 0, R * .72, R], a => R * Math.sqrt(Math.max(.05, 1 - (a / R) ** 2)), tex, ledge, {vFrom: R, vTo: -R, n}, '-+');

// Kimono sleeve round the upper arm (A-frame, arm box X +-2, Z +-2, Y -4..2): an outer panel flaring away from the body,
// front and back panels; side +1 = her left arm. Long = the right sleeve (to Y -17), else to Y -13.
function sleeve(side, dark) {
  const spr = dark ? 'sleeve_dark' : 'sleeve_pale', y1 = 1.6, y0 = dark ? -18 : -14, xo = 2.45 * side;
  return [
    cardX(spr, xo, {Z0: -4.6, Z1: 4.6, Y0: y0, Y1: y1}, {rot: ['z', side > 0 ? 22.5 : -22.5, [xo, y1, 0]]}),
    cardZ(spr, -2.5, {X0: side > 0 ? -2.3 : -5.4, X1: side > 0 ? 5.4 : 2.3, Y0: y0, Y1: y1}, {rot: ['x', -22.5, [0, y1, -2.5]]}),
    cardZ(spr, 2.5, {X0: side > 0 ? -2.3 : -5.4, X1: side > 0 ? 5.4 : 2.3, Y0: y0, Y1: y1}, {rot: ['x', 22.5, [0, y1, 2.5]], flipU: true}),
  ];
}

// ---- body looks -------------------------------------------------------------------------------------------------------------
function bodyModels() {
  const M = {};
  for (const n of BODY) { M[n] = skinPart(n, 'skin'); M['t_' + n] = skinPart(n, 'skin_tenma'); }
  // Shogun extras inside the body models
  M.head.push(cardX('flower', 4.7, {Z0: -1.2, Z1: 2.2, Y0: 4.2, Y1: 7.6}), cardZ('flower', .4, {X0: 3.3, X1: 6.3, Y0: 4.6, Y1: 7.6}));
  M.body.push(
    cardZ('obi_knot', -2.45, {X0: .6, X1: 4.0, Y0: -9.6, Y1: -6.2}),
    cardZ('tassel', -2.5, {X0: 1.6, X1: 3.0, Y0: -14.6, Y1: -8.6}),
    abox([-4.1, -15.2, -2.45], [-.35, -11.4, -2.2], {all: 'sw_pale', front: 'sw_pale', up: 'sw_paleshade'}),
    abox([.35, -15.2, -2.45], [4.1, -11.4, -2.2], {all: 'sw_pale', up: 'sw_paleshade'}),
    abox([-4.05, -10.2, -2.38], [4.05, -7.4, 2.38], {all: 'sw_plum', up: 'sw_golddk', down: 'sw_golddk'}));
  M.right_arm.push(...sleeve(-1, true));
  M.left_arm.push(...sleeve(1, false));
  // Tenma: pale hip and leg plates, dark tassets, pale breast plates, dark gauntlet cuffs
  M.t_body.push(cardZ('plate_pale', -2.35, {X0: -3.6, X1: -.4, Y0: -5.2, Y1: -1.4}), cardZ('plate_pale', -2.35, {X0: .4, X1: 3.6, Y0: -5.2, Y1: -1.4}),
    abox([-4.05, -10.6, -2.36], [4.05, -8.8, 2.36], {all: 'sw_suit', front: 'sw_violet', up: 'sw_violet', down: 'sw_violet'}));
  for (const [n, side] of [['t_right_leg', -1], ['t_left_leg', 1]]) M[n].push(
    cardX('plate_pale', 2.35 * side, {Z0: -2.4, Z1: 2.4, Y0: -5.6, Y1: .6}),
    cardZ('tasset', -2.5, {X0: -2.4, X1: 2.4, Y0: -7.5, Y1: .8}, {rot: ['x', -22.5, [0, .8, -2.5]]}),
    cardX('tasset', 2.6 * side, {Z0: -1.8, Z1: 3.4, Y0: -8.5, Y1: 1}, {rot: ['z', side > 0 ? 22.5 : -22.5, [2.6 * side, 1, 0]]}));
  for (const n of ['t_right_shin', 't_left_shin']) M[n].push(cardZ('plate_pale', -2.4, {X0: -1.9, X1: 1.9, Y0: -4.6, Y1: -.2}));
  for (const n of ['t_right_forearm', 't_left_forearm']) M[n].push(abox([-2.35, -4.6, -2.35], [2.35, -2.2, 2.35], {all: 'sw_suit', up: 'sw_violet', down: 'sw_violet'}));
  return M;
}

// ---- Shogun extras -----------------------------------------------------------------------------------------------------------
function shogunModels() {
  const M = {};
  // braid: hangs 1 b along -Y from the nape; crossed cards (back view + side view)
  M.braid = [cardZ('braid', 0, {X0: -1.6, X1: 1.6, Y0: -16, Y1: 0}), cardX('braid', 0, {Z0: -1.3, Z1: 1.3, Y0: -16, Y1: 0}, {flipU: true}),
    abox([-.9, -14.2, -.9], [.9, -13.5, .9], 'sw_electro')];
  // drape: translucent train from the waist back (pivot) to the ankles, back panel + two side panels flaring
  M.drape = [cardZ('drape', 1.2, {X0: -6.4, X1: 6.4, Y0: -15.4, Y1: 0}, {rot: ['x', -22.5, [0, 0, 1.2]]}),
    cardX('drape', 4.3, {Z0: -1.6, Z1: 5.2, Y0: -14.6, Y1: 0}, {rot: ['z', 22.5, [4.3, 0, 0]]}),
    cardX('drape', -4.3, {Z0: -1.6, Z1: 5.2, Y0: -14.6, Y1: 0}, {rot: ['z', -22.5, [-4.3, 0, 0]], flipU: true})];
  // katana: grip at the pivot, blade along +Y, edge toward -Z
  M.katana = [abox([-.55, -3.4, -.7], [.55, 1.6, .7], 'sw_ink'),
    ...[-2.4, -.8].map(y => abox([-.62, y, -.78], [.62, y + .5, .78], 'sw_violet')),
    abox([-.7, -3.9, -.85], [.7, -3.4, .85], 'sw_gold'),
    abox([-1.35, 1.6, -1.55], [1.35, 2.15, 1.55], {all: 'sw_deep', up: 'sw_violet', down: 'sw_violet'}),
    abox([-.32, 2.15, -.85], [.32, 19.2, .45], 'sw_pale'),
    cardX('katana_blade', .34, {Z0: -1.25, Z1: .85, Y0: 2.15, Y1: 20.6}), cardX('katana_blade', -.34, {Z0: -1.25, Z1: .85, Y0: 2.15, Y1: 20.6})];
  M.katana_fx = [cardX('weapon_glow', 0, {Z0: -2.8, Z1: 2.2, Y0: 1.6, Y1: 21.4}), cardZ('weapon_glow', -.2, {X0: -2.2, X1: 2.2, Y0: 1.6, Y1: 21.4})];
  // polearm: grip at the pivot; the curved blade toward +Y (like the katana's tip, so a shared clip's katana hold shows
  // the polearm blade low in front and the spike above her shoulder), the dark ringed shaft toward -Y, a short spike
  M.polearm = [abox([-.5, -20.6, -.5], [.5, 5.0, .5], 'sw_shaft'),
    ...[3.6, -3, -9.6, -16.2, -20.4].map(y => abox([-.68, y, -.68], [.68, y + .55, .68], 'sw_gold')),
    abox([-.85, 4.8, -1.2], [.85, 5.8, 1.2], {all: 'sw_deep', up: 'sw_violet'}),
    cardX('polearm_blade', .2, {Z0: -2.6, Z1: 1.0, Y0: 5.6, Y1: 14.8}), cardX('polearm_blade', -.2, {Z0: -2.6, Z1: 1.0, Y0: 5.6, Y1: 14.8}),
    abox([-.4, -22.8, -.4], [.4, -20.6, .4], 'sw_glow'), abox([-.2, -23.6, -.2], [.2, -22.8, .2], 'sw_white')];
  M.polearm_fx = [cardX('weapon_glow', 0, {Z0: -3.6, Z1: 2.2, Y0: 1.4, Y1: 15.2}), cardZ('weapon_glow', -.3, {X0: -2.4, X1: 2.4, Y0: 1.4, Y1: 15.2})];
  // halo arch (scale 1.25; pivot behind the upper back): eye emblem on top, 4 tomoe orbs, lightning threads between
  const O = [[0, 17.2], [-11.4, 7.4], [11.4, 7.4], [-12.4, -5.2], [12.4, -5.2]];
  M.halo = [...crossCards('halo_eye', [0, 17.2, 0], 7.2, 7.2, -3.6), cardZ('halo_eye', -.05, {X0: -3.6, X1: 3.6, Y0: 13.6, Y1: 20.8})];
  for (const [x, y] of O.slice(1)) M.halo.push(sq('tomoe_orb', [x, y, 0], 4.6), sq('tomoe_orb', [x, y, 0], 4.6, 'x'));
  // threads: eye -> upper orbs -> lower orbs (each piece one card, turned by +-45 / 22.5 degrees about Z)
  const thread = (a, b, ang) => { const c = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], L = Math.hypot(b[0] - a[0], b[1] - a[1]);
    return cardZ('thread', .3, {X0: c[0] - 1.1, X1: c[0] + 1.1, Y0: c[1] - L / 2, Y1: c[1] + L / 2}, ang ? {rot: ['z', ang, [c[0], c[1], .3]]} : {}); };
  M.halo.push(thread([0, 17.2], [-11.4, 7.4], -45), thread([0, 17.2], [11.4, 7.4], 45), thread([-11.4, 7.4], [-12.4, -5.2], 0), thread([11.4, 7.4], [12.4, -5.2], 0));
  // guard aura: crackling floor ring (scale 2.4; r 1.8 b)
  M.aura = [cardY('aura_ring', .5, {X0: -12, X1: 12, Z0: -12, Z1: 12})];
  return M;
}

// ---- Tenma parts -------------------------------------------------------------------------------------------------------------
// A limb segment hanging along -Y from a ball joint: turned taper in lacquer, a joint ring, optional sigils.
function limb(L, r0, r1, {ball = 0, sig = false, ring = true, n = 8} = {}) {
  const st = [0, 1, 2, 3].map(i => -L + L * i / 3);
  const els = [...turned('y', [0, 0, 0], st, y => r1 + (r0 - r1) * (y + L) / L, 'lacquer', 'sw_lacquersh', {...LIMB_V, n}, '-+')];
  if (ball) els.push(...ballJ([0, 0, 0], ball, 'lacquer', 'sw_lacquersh', n));
  if (ring) els.push(abox([-r1 * 1.08, -L + .2, -r1 * 1.08], [r1 * 1.08, -L + 1.1, r1 * 1.08], {all: 'sw_lacquerdk'}));
  if (sig) els.push(cardZ('sigil', -r0 * 1.02 - .05, {X0: -r0 * .9, X1: r0 * .9, Y0: -L * .55, Y1: -L * .3}), cardX('sigil', r0 * 1.02 + .05, {Z0: -r0 * .9, Z1: r0 * .9, Y0: -L * .6, Y1: -L * .35}));
  return els;
}
// A lacquer hand hanging along -Y from the wrist; kind 'fist' (grips a shaft along X at Y -5.6), 'open', 'claw', 'dagger'.
function puppetHand(kind, s = 1) {
  const e = [abox([-2.6 * s, -6.2 * s, -1.3 * s], [2.6 * s, 0, 1.3 * s], {all: 'lacquer', front: 'sw_lacquersh', back: 'sw_lacquersh'})];
  e.push(cardZ('sigil', -1.36 * s, {X0: -1.5 * s, X1: 1.5 * s, Y0: -4.6 * s, Y1: -1.6 * s}));
  for (let i = 0; i < 4; i++) {
    const x = (-1.95 + i * 1.3) * s, w = .55 * s;
    if (kind === 'fist' || kind === 'dagger') e.push(abox([x - w, -8.6 * s, -1.4 * s], [x + w, -6.2 * s, 1.5 * s], {all: 'lacquer', down: 'sw_lacquersh'}),
      abox([x - w, -8.9 * s, 1.0 * s], [x + w, -7.4 * s, 3.0 * s], 'sw_lacquersh'));
    else if (kind === 'open') e.push(abox([x - w, -(10.2 - Math.abs(i - 1.5) * .9) * s, -.9 * s], [x + w, -6.2 * s, .9 * s], {all: 'lacquer', down: 'sw_lacquerdk'}));
    else e.push(abox([x - w, -9.0 * s, -.9 * s], [x + w, -6.2 * s, .9 * s], 'lacquer'), abox([x - w * .8, -10.4 * s, -2.6 * s], [x + w * .8, -8.6 * s, -.4 * s], {all: 'sw_lacquersh', front: 'sw_glow'}));
  }
  e.push(abox([2.4 * s, -4.4 * s, -1.6 * s], [3.6 * s, -1 * s, .6 * s], 'sw_lacquersh'), abox([2.6 * s, -6.6 * s, -2.4 * s], [3.4 * s, -4.4 * s, -.8 * s], 'lacquer'));
  return e;
}
function tenmaModels() {
  const M = {};
  // disc halo: dark disc 1.7 b, tomoe-eye emblem, thin outer ring; two crescent horns behind the head, up and out
  M.disc = [cardZ('disc', 0, {X0: -13.6, X1: 13.6, Y0: -13.6, Y1: 13.6}), abox([-1.2, -1.2, .1], [1.2, 1.2, 1.4], 'sw_ink'),
    cardZ('horn', -.4, {X0: -7.6, X1: -2.2, Y0: 9.0, Y1: 18.6}, {rot: ['z', 22.5, [-4.9, 9, -.4]], flipU: true}),
    cardZ('horn', -.4, {X0: 2.2, X1: 7.6, Y0: 9.0, Y1: 18.6}, {rot: ['z', -22.5, [4.9, 9, -.4]]})];
  // giant left arm (scale 1.5: upper and forearm 2 b = 21.3 units, r ~0.3 b) and the gripping fist (scale 1.4)
  M.g_upper = limb(21.3, 3.4, 2.9, {ball: 3.9, ring: true, n: 16});
  M.g_fore = [...limb(21.3, 2.9, 2.3, {ball: 3.0, sig: true, n: 16}), abox([-3.0, -16, -3.0], [3.0, -14.6, 3.0], 'sw_lacquerdk')];
  M.g_hand = puppetHand('fist', 1.3);
  // glaive (scale 3.6): shaft along +Y from the grip (butt -7.1 .. tip 21.8 units = 6.5 b), single-edged curved blade toward
  // +X in the Z = 0 plane (2.2 b), round pink guard ornament
  M.glaive = [abox([-.3, -7.1, -.3], [.3, 11.8, .3], 'glaive_shaft'),
    ...[-7, -1.7, 5, 10.3].map(y => abox([-.42, y, -.42], [.42, y + .4, .42], 'sw_gold')),
    cardZ('glaive_guard', 0, {X0: -1.25, X1: 1.25, Y0: 10.5, Y1: 13}), cardX('glaive_guard', 0, {Z0: -1.25, Z1: 1.25, Y0: 10.5, Y1: 13}),
    cardZ('glaive_blade', .05, {X0: -.33, X1: 2.83, Y0: 11.8, Y1: 21.8}), cardZ('glaive_blade', -.05, {X0: -.33, X1: 2.83, Y0: 11.8, Y1: 21.8}),
    abox([-.17, 11.8, -.15], [.42, 20, .15], 'sw_ink')];
  M.glaive_fx = [cardZ('weapon_glow', -.13, {X0: 1, X1: 3.8, Y0: 11.3, Y1: 22.2}), cardX('weapon_glow', 2.2, {Z0: -1.5, Z1: 1.5, Y0: 11.3, Y1: 22.2})];
  // three thin right arms: upper 1.3 b (20.8 units), forearm-with-hand 1.0 + 0.6 b
  M.ra_up = limb(20.8, 1.35, 1.1, {ball: 1.7});
  // the dagger arm's spearhead points on past the fist (up while the forearm points up)
  M.ra1_fo = [...limb(12, 1.1, .9, {ball: 1.3, sig: true}), ...puppetHand('dagger', .55).map(e => shiftY(e, -12)),
    abox([-.3, -18.6, -.3], [.3, -15.6, .3], 'sw_shaft'), abox([-.7, -18.9, -.7], [.7, -18.5, .7], 'sw_gold'),
    cardZ('dagger', 0, {X0: -1.4, X1: 1.4, Y0: -23.8, Y1: -18.6}, {flipU: false}), cardX('dagger', 0, {Z0: -1.4, Z1: 1.4, Y0: -23.8, Y1: -18.6})];
  M.ra2_fo = [...limb(12, 1.1, .9, {ball: 1.3}), ...puppetHand('open', .55).map(e => shiftY(e, -12))];
  M.ra3_fo = [...limb(12, 1.1, .9, {ball: 1.3, sig: true}), ...puppetHand('claw', .55).map(e => shiftY(e, -12))];
  // tan gauntlets: palm up, fingers forward (-Z), 1.3 b wide, violet sigil on the palm; pivot at the palm centre
  M.gaunt_l = gauntlet();
  M.gaunt_r = mirrorModel(gauntlet());
  return M;
}
const shiftY = (e, dy) => ({...e, from: [e.from[0], r4(e.from[1] + dy), e.from[2]], to: [e.to[0], r4(e.to[1] + dy), e.to[2]],
  ...(e.rotation ? {rotation: {...e.rotation, origin: [e.rotation.origin[0], r4(e.rotation.origin[1] + dy), e.rotation.origin[2]]}} : {})});
function gauntlet() {
  const T = {all: 'gauntlet', up: 'sw_tan', down: 'sw_tandk'};
  const e = [abox([-6.4, -1.6, -5.6], [6.4, 1.4, 5.8], T), cardY('sigil', 1.45, {X0: -3.6, X1: 3.6, Z0: -3.4, Z1: 3.4}),
    abox([-5.2, -2.0, 5.2], [5.2, 1.0, 9.6], {all: 'gauntlet', back: 'sw_tandk'}), abox([-5.6, -2.2, 8.2], [5.6, 1.4, 9.2], 'sw_tandk')];
  for (let i = 0; i < 4; i++) {
    const x = -4.8 + i * 3.2, L = [7.2, 8.4, 8.0, 6.4][i];
    e.push(abox([x - 1.25, -1.2, -5.6 - L * .55], [x + 1.25, 1.2, -5.4], T), abox([x - 1.15, -.6, -5.6 - L], [x + 1.15, 2.6, -5.6 - L * .55], T),
      abox([x - 1.0, 2.6, -5.6 - L - .2], [x + 1.0, 3.6, -5.6 - L * .62], 'sw_tandk'));
  }
  e.push(abox([6.2, -1.2, -3.6], [8.6, 1.2, 1.6], T), abox([7.6, -.8, -7.2], [9.6, 2.4, -3.4], T));
  return e;
}

// ---- props (separate entities; plan §C.2). Display scale in PROPS[...].scale gives the intended size. --------------------------
function propModels() {
  const M = {};
  // eye orb (single and multi eyes): crossed glow cards, a dark core; centre 12.3 units above the pivot (0.77 b at scale 1)
  M['prop/eye_orb'] = [...crossCards('orb_eye', [0, 12.3, 0], 13, 13, -6.5), abox([-2, 10.3, -2], [2, 14.3, 2], 'sw_ink'),
    cardZ('orb_eye', 0, {X0: -6.5, X1: 6.5, Y0: 5.8, Y1: 18.8}, {rot: ['y', 45, [0, 12.3, 0]]}), cardZ('orb_eye', 0, {X0: -6.5, X1: 6.5, Y0: 5.8, Y1: 18.8}, {rot: ['y', -45, [0, 12.3, 0]]})];
  // blade-eye sigil (polearm after-effect): an upright almond eye card 1.2 b wide (scale 1.2)
  M['prop/blade_eye'] = [cardZ('sigil', 0, {X0: -8, X1: 8, Y0: -6, Y1: 6}), cardX('sigil', 0, {Z0: -4, Z1: 4, Y0: -3, Y1: 3})];
  // Musou crystal orb: a crystal bundle round a glow core (scale 1.4)
  M['prop/musou_orb'] = [...crossCards('crystal', [0, 0, 0], 10, 16, -8), cardZ('crystal', 0, {X0: -5, X1: 5, Y0: -8, Y1: 8}, {rot: ['y', 45, [0, 0, 0]]}),
    cardZ('crystal', 0, {X0: -5, X1: 5, Y0: -8, Y1: 8}, {rot: ['y', -45, [0, 0, 0]]}), ...crossCards('tomoe_orb', [0, 0, 0], 6, 6, -3)];
  // vajra: a crystalline spike bundle (scale 2.5 -> 3.5 b); base at the pivot (floor)
  const spikes = [[0, 0, 0, 22.4, 7], [3, 0, 0, 15, 5, ['z', -22.5]], [-3, 0, 0, 15, 5, ['z', 22.5]], [0, 0, 3, 13, 5, ['x', 22.5]], [0, 0, -3, 13, 5, ['x', -22.5]]];
  M['prop/vajra'] = [abox([-3.4, 0, -3.4], [3.4, 1.4, 3.4], {all: 'sw_ink', up: 'sw_deep'}), abox([-2.4, 1.4, -2.4], [2.4, 2.4, 2.4], 'sw_gold')];
  for (const [x, , z, h, w, r] of spikes) for (const pl of ['z', 'x']) M['prop/vajra'].push(pl === 'z'
    ? cardZ('crystal', z, {X0: x - w / 2, X1: x + w / 2, Y0: 1.4, Y1: 1.4 + h}, r ? {rot: [r[0], r[1], [x, 1.4, z]]} : {})
    : cardX('crystal', x, {Z0: z - w / 2, Z1: z + w / 2, Y0: 1.4, Y1: 1.4 + h}, r ? {rot: [r[0], r[1], [x, 1.4, z]]} : {}));
  // remembrance flower: magenta lotus round a dark orb (scale 1.2), floor pivot
  M['prop/flower'] = [...ballJ([0, 6.2, 0], 3.2, 'sw_ink', 'sw_deep'), abox([-.6, 0, -.6], [.6, 3, .6], 'sw_violet')];
  for (let k = 0; k < 8; k++) {
    const a = k * 45, r = 4.6, x = Math.sin(a * Math.PI / 180) * r, z = -Math.cos(a * Math.PI / 180) * r;
    const el = k % 2 === 0 ? cardZ('petal', z, {X0: x - 3, X1: x + 3, Y0: 2, Y1: 10}) : cardX('petal', x, {Z0: z - 3, Z1: z + 3, Y0: 2, Y1: 10});
    if (k % 2) { const e2 = cardZ('petal', 0, {X0: -3, X1: 3, Y0: 2, Y1: 10}, {rot: ['y', k === 1 || k === 5 ? 45 : -45, [0, 6, 0]]}); M['prop/flower'].push(shiftXZ(e2, x, z)); }
    else M['prop/flower'].push(el);
  }
  // safe dome r 8 b (scale 8: 1 unit = 0.5 b): glass hemisphere, outer and inner facets
  const at = [0, 4, 8, 11.5, 14, 15.6, 16];
  const secs = at.slice(1).map((y, i) => ({a: [at[i], y], r: 16 * Math.cos(Math.asin(Math.min(1, ((at[i] + y) / 2) / 16))), tex: 'dome_glass'}));
  M['prop/dome'] = [...lathe('y', [0, 0, 0], secs, {vFrom: 0, vTo: 1, n: 16}), ...lathe('y', [0, 0, 0], secs, {vFrom: 0, vTo: 1, n: 16, inward: true})];
  // clap hands: translucent faceted violet hands, 4.5 b at scale 3.6 (palm toward +X for the left hand)
  M['prop/clap_hand_l'] = clapHand();
  M['prop/clap_hand_r'] = mirrorModel(clapHand());
  // slam palm: a pale lacquer open hand from above, palm down (scale 3.2 -> about 4 b)
  M['prop/slam_palm'] = puppetHand('open', 1.6).map(e => e);
  // planted glaive: the glaive's shaft rising out of the floor at 22.5 degrees, blade buried (scale 3)
  M['prop/glaive_planted'] = [abox([-.35, .4, -.35], [.35, 20, .35], 'glaive_shaft', {rot: ['x', 22.5, [0, 0, 0]]}),
    abox([-.5, 6, -.5], [.5, 6.45, .5], 'sw_gold', {rot: ['x', 22.5, [0, 0, 0]]}), abox([-.5, 14, -.5], [.5, 14.45, .5], 'sw_gold', {rot: ['x', 22.5, [0, 0, 0]]}),
    cardZ('glaive_guard', 0, {X0: -1.5, X1: 1.5, Y0: .6, Y1: 3.6}, {rot: ['x', 22.5, [0, 0, 0]]}),
    cardZ('glaive_blade', .06, {X0: -.4, X1: 3.4, Y0: .4, Y1: 3.2}, {rot: ['x', 22.5, [0, 0, 0]], uvr: [0, .78, 1, 1]})];
  // shadow seed: dark orb with an eye (scale 1)
  M['prop/seed'] = [...ballJ([0, 0, 0], 3.4, 'sw_ink', 'sw_deep'), ...crossCards('sigil', [0, 0, 0], 6, 4, -2)];
  // weapon switch: dark vertical hoop (scale 2 -> 3 b) and the vortex disc at her feet (scale 3)
  M['prop/hoop'] = [cardZ('hoop', 0, {X0: -12, X1: 12, Y0: 0, Y1: 24}), cardX('hoop', 0, {Z0: -12, Z1: 12, Y0: 0, Y1: 24})];
  M['prop/vortex'] = [cardY('vortex', .4, {X0: -15, X1: 15, Z0: -15, Z1: 15})];
  // clone silhouettes (boss scale): the skin figure in the sword raise (ready) and the follow-through (slash) poses;
  // tinted items give the dark smoky clone and the glowing revealed one (PROP_TINTS)
  M['prop/clone_ready'] = clone('ready');
  M['prop/clone_slash'] = clone('slash');
  return M;
}
const shiftXZ = (e, dx, dz) => ({...e, from: [r4(e.from[0] - dx), e.from[1], r4(e.from[2] + dz)], to: [r4(e.to[0] - dx), e.to[1], r4(e.to[2] + dz)],
  ...(e.rotation ? {rotation: {...e.rotation, origin: [r4(e.rotation.origin[0] - dx), e.rotation.origin[1], r4(e.rotation.origin[2] + dz)]}} : {})});
function clapHand() {
  const F = {all: 'clap_facet'};
  const e = [abox([-1.4, -6, -4.2], [1.4, 4, 4.2], F)];
  for (let i = 0; i < 4; i++) { const z = -3.2 + i * 2.1; e.push(abox([-1.0, 4, z - .9], [1.0, 4 + [5.6, 6.6, 6.2, 5][i], z + .9], F)); }
  e.push(abox([-1, -2.6, -6.4], [1.2, 1.6, -4.2], F), abox([-.8, 1.6, -7.4], [1.0, 4.6, -5.4], F));
  return e;
}
// A static skin figure (model units; pivot at the waist, feet 22 units = 1.375 b below it at scale 1, 2 b tall) in a fixed pose: limbs are
// boxes turned by single-axis element rotations (+-22.5 / 45), the katana as in the rig.
function clone(pose) {
  const e = [], tex = 'skin', R = pose === 'ready';
  const put = (n, dx, dy, rotEl) => { for (const el of skinPart(n, tex)) e.push(moveEl(el, dx, dy, rotEl)); };
  put('right_leg', 2, -10, R ? null : ['x', -22.5]); put('right_shin', 2, -16, R ? null : ['x', 22.5]);
  put('left_leg', -2, -10, R ? ['x', 22.5] : null); put('left_shin', -2, -16, null);
  put('body', 0, 0, null); put('head', 0, 0, null);
  put('left_arm', -6, -2, R ? ['x', 45] : ['z', 22.5]); put('left_forearm', -6, -8, R ? ['x', 45] : ['z', 22.5]);
  put('right_arm', 6, -2, R ? ['x', -45] : ['x', 45]); put('right_forearm', 6, -8, R ? ['x', -45] : ['x', 45]);
  return e;
}
function moveEl(el, dx, dy, r) {
  const out = {...el, from: [r4(el.from[0] + dx), r4(el.from[1] + dy), el.from[2]], to: [r4(el.to[0] + dx), r4(el.to[1] + dy), el.to[2]]};
  if (r) out.rotation = {origin: [8 + dx, 8 + dy, 8], axis: r[0], angle: r[1]};
  return out;
}
// Tinted item definitions over prop models: [model, rgb]
export const PROP_TINTS = {'prop/clone_ready_dark': ['prop/clone_ready', 0x3a2a5a], 'prop/clone_slash_dark': ['prop/clone_slash', 0x3a2a5a],
  'prop/clone_ready_glow': ['prop/clone_ready', 0xd8b8ff], 'prop/clone_slash_glow': ['prop/clone_slash', 0xd8b8ff]};
// Prop catalogue for the manifest and the prop/<kind> summon functions: models, display scale, billboard, pivot note.
export const PROPS = {
  eye_orb: {model: 'prop/eye_orb', scale: 1, note: 'eye orb (10 single / 4 multi); centre 0.77 b above the pivot'},
  blade_eye: {model: 'prop/blade_eye', scale: 1.2, billboard: 'center', note: 'blade-eye sigil (6b), 1.2 b wide, centred'},
  musou_orb: {model: 'prop/musou_orb', scale: 1.4, note: 'Musou crystal orb, centred'},
  vajra: {model: 'prop/vajra', scale: 2.5, note: 'vajra spike bundle 3.5 b tall, base at the pivot (floor)'},
  flower: {model: 'prop/flower', scale: 2.2, note: 'remembrance flower (lotus + dark orb, about 2 b tall), floor pivot'},
  dome: {model: 'prop/dome', scale: 8, note: 'safe dome r 8 b (glass, outer and inner facets), floor pivot; animate the scale to grow it'},
  clap_l: {model: 'prop/clap_hand_l', scale: 3.6, note: 'left clap hand (palm toward +X of the display), 4.5 b'},
  clap_r: {model: 'prop/clap_hand_r', scale: 3.6, note: 'right clap hand (palm toward -X), 4.5 b'},
  slam_palm: {model: 'prop/slam_palm', scale: 3.2, note: 'pale open hand hanging from the pivot (fingers -Y); turn it palm down'},
  glaive_planted: {model: 'prop/glaive_planted', scale: 3, note: 'planted glaive rising from the floor at 22.5 degrees, blade buried'},
  seed: {model: 'prop/seed', scale: 1, note: 'shadow seed: dark orb with an eye, centred'},
  hoop: {model: 'prop/hoop', scale: 2, note: 'switch hoop, 3 b, standing on the pivot'},
  vortex: {model: 'prop/vortex', scale: 3, note: 'switch vortex disc r 2.8 b on the floor'},
  clone_ready: {model: 'prop/clone_ready_dark', scale: 1, lift: 1.375, note: 'dark clone, sword raised (2 b tall at scale 1, boss scale); pivot at the waist, 1.375 b above the feet'},
  clone_slash: {model: 'prop/clone_slash_dark', scale: 1, lift: 1.375, note: 'dark clone, follow-through'},
  clone_ready_glow: {model: 'prop/clone_ready_glow', scale: 1, lift: 1.375, note: 'revealed (glowing) clone, sword raised'},
  clone_slash_glow: {model: 'prop/clone_slash_glow', scale: 1, lift: 1.375, note: 'revealed clone, follow-through'},
};
// Legacy item ids the release encounter still uses, served by the restyled props (item definitions only).
export const LEGACY_ITEMS = {electro_orb: 'prop/eye_orb', lightning_stake: 'prop/vajra', remembrance_flower: 'prop/flower', support_hand_l: 'prop/clap_hand_l', support_hand_r: 'prop/clap_hand_r'};

// body hull points (A-frame units) over both looks, for the floor lift in solve
let BODY_HULL = null;
function bodyHull(n) {
  if (!BODY_HULL) {
    const M = bodyModels();
    BODY_HULL = Object.fromEntries(BODY.map(b => { const seen = new Set(); return [b, [...modelPoints(M[b]), ...modelPoints(M['t_' + b])].filter(P => { const k = P.map(v => v.toFixed(1)).join(); if (seen.has(k)) return false; seen.add(k); return true; })]; }));
  }
  return BODY_HULL[n];
}
export function allModels() {
  const M = {...bodyModels(), ...shogunModels(), ...tenmaModels(), ...propModels()};
  for (const [n, els] of Object.entries(M)) checkBounds(n, els);
  return M;
}
// Item models per look: the body parts' models in each look, the weapon pair.
export const LOOK_MODELS = {
  shogun: Object.fromEntries(BODY.map(n => [n, n])),
  tenma: Object.fromEntries(BODY.map(n => [n, 't_' + n])),
  sword: {weapon: 'katana', weapon_fx: 'katana_fx'},
  polearm: {weapon: 'polearm', weapon_fx: 'polearm_fx'},
};

// ---- skeleton and forward kinematics ---------------------------------------------------------------------------------------
const PX = 1 / 16;
export const HIP_Y = 12 * LEG[1] * PX + .035;              // the hip joint above the soles (0.8625 + the overlay and a stance margin)
export const SK = {
  hipJ: [.1, HIP_Y, 0],                                    // her left hip joint (mirror for the right)
  legU: 6 * LEG[1] * PX, legS: 6 * LEG[1] * PX,            // thigh, shin (0.431 b each)
  neck: [0, .75, 0],                                       // torso frame from the hip
  shoulder: [.315, .75 - 2 * ARM[1] * PX, 0],              // torso frame (her left)
  armU: 4 * ARM[1] * PX, grip: .335,                       // shoulder -> elbow; elbow -> fist centre
  braid: [0, .28, .225],                                   // head frame: the nape
  drape: [0, .14, .14],                                    // root frame from the hip: back of the obi
  halo: [0, .62, .40],                                     // torso frame from the hip: behind the upper back
  disc: [0, .98, .38],                                     // torso frame from the hip: behind the head
  gRoot: [-1.25, 2.55, .6], gU: 2.0, gF: 2.0, gWrist: .62,  // giant arm root (root frame from the floor point), lengths, wrist -> grip
  raRoot: [[.42, 1.62, .36], [.48, 1.44, .40], [.46, 1.26, .36]], raU: 1.3, raF: .94,
};
export const mirrorE = e => [e[0], -e[1], -e[2]];
// the four sole corners of a shin box (blocks, shin frame: overlay-inflated 4 x 4 px box, 6 px below the knee) and the
// drape's length (its model hangs 15.4 units at scale 1)
const SOLE = [[-1, -1], [-1, 1], [1, -1], [1, 1]].map(([a, b]) => [a * 2.22 * LEG[0] / 16, -6.22 * LEG[1] / 16, b * 2.22 * LEG[2] / 16]);
const DRAPE_LEN = 15.4 / 16;
const sideE = (e, side) => (side > 0 ? e : mirrorE(e));
export const ROOT_PIVOT = [0, HIP_Y, 0];

// A weapon whose ends would reach below the floor is tipped up about the grip (the katana tip 1.3 b along +Y, the
// polearm spike 1.48 b along -Y): the smallest rotation that keeps both ends 0.05 b above the floor.
const W_ENDS = [[1.31, 1, .22], [1.49, -1, .1]], G_ENDS = [[4.95, 1, .9], [1.62, -1, .2]];
function groundBlade(g, Q, ends = W_ENDS) {
  let out = Q;
  for (const [L, sgn, clear] of ends) {
    const d = times(rot(out, [0, sgn, 0]), 1), minY = (clear - g[1]) / L;
    if (d[1] >= minY) continue;
    const h = [d[0], 0, d[2]], hl = len(h) || 1e-6, sy = Math.min(1, minY), cy = Math.sqrt(Math.max(0, 1 - sy * sy));
    const d2 = [h[0] / hl * cy, sy, h[2] / hl * cy];
    const ax = cross(d, d2), sa = len(ax), ca = dot(d, d2);
    if (sa < 1e-9) continue;
    const ang = Math.atan2(sa, ca), u = times(ax, 1 / sa), sn = Math.sin(ang / 2);
    out = mul([u[0] * sn, u[1] * sn, u[2] * sn, Math.cos(ang / 2)], out);
  }
  return out;
}
// Blade frame helper for pose channels: model +Y along `tip`, model -Z (the edge / front face) toward `edge`.
export function bladeQ(tip, edge) {
  const Y = unit(tip); let Z = perp(times(edge, -1), Y);
  if (len(Z) < 1e-6) Z = perp([0, 0, 1], Y);
  Z = unit(Z);
  return basisQ(cross(Y, Z), Y, Z);
}

// p: a full pose (raiden_clips.mjs DEFAULT_POSE merged with clip keys). Returns {part: {t, q, s}} in the rig frame
// (blocks) and the hidden extras _grip (sword hand), _gHand.
export function solve(p, prev = null) {
  const o = {};
  const part = (n, t, Q, s = 1) => { o[n] = {t, q: Q, s: Array.isArray(s) ? s : [s, s, s]}; };
  const R0 = q(p.rot), Tq = mul(R0, q(p.torso));
  const hip = [0, HIP_Y, 0];
  const fromHip = v => add(hip, rot(Tq, v));
  // torso, head
  const neck = fromHip(SK.neck), Hq = mul(Tq, q(p.head));
  part('body', neck, Tq);
  part('head', neck, Hq);
  // arms
  const grip = {};
  for (const [s, side, A, E] of [['left', 1, 'armL', 'elbowL'], ['right', -1, 'armR', 'elbowR']]) {
    const sh = fromHip([SK.shoulder[0] * side, SK.shoulder[1], SK.shoulder[2]]);
    const aq = mul(Tq, q(sideE(p[A], side))), fq = mul(aq, q([p[E], 0, 0]));
    const el = add(sh, rot(aq, [0, -SK.armU, 0]));
    part(s + '_arm', sh, aq);
    part(s + '_forearm', el, fq);
    grip[s] = add(el, rot(fq, [0, -SK.grip, 0]));
  }
  // legs (root frame: the hips do not turn with the torso); footMin = the lowest sole corner (feet planting below)
  let footMin = Infinity;
  for (const [s, side, L, K] of [['left', 1, 'legL', 'kneeL'], ['right', -1, 'legR', 'kneeR']]) {
    const hj = add(hip, rot(R0, [SK.hipJ[0] * side, 0, 0]));
    const lq = mul(R0, q(sideE(p[L], side))), sq = mul(lq, q([-p[K], 0, 0]));
    const knee = add(hj, rot(lq, [0, -SK.legU, 0]));
    part(s + '_leg', hj, lq);
    part(s + '_shin', knee, sq);
    for (const c of SOLE) footMin = Math.min(footMin, add(knee, rot(sq, c))[1]);
    footMin = Math.min(footMin, add(hj, rot(lq, [0, -SK.legU - .03, 0]))[1] - .1);   // a knee on the floor
  }
  // Shogun extras
  const sS = p.sS;
  part('braid', add(o.head.t, rot(Hq, SK.braid)), mul(Tq, q(p.braid)));
  // the drape flares back on its own where it would reach the floor (crouches)
  const dRoot = add(add(hip, rot(R0, SK.drape)), [0, p.pos[1], 0]), dLen = DRAPE_LEN, need = (dRoot[1] - .04) / dLen;
  const dPitch = need < 1 ? -Math.acos(Math.max(-1, need)) * 180 / Math.PI : 0;
  part('drape', add(hip, rot(R0, SK.drape)), mul(R0, q([Math.min(p.drape[0], dPitch), p.drape[1], p.drape[2]])), [p.drapeF * sS, sS, sS]);
  const wq = groundBlade(add(grip.right, [0, p.pos[1], 0]), mul(Tq, p.wpn));
  part('weapon', grip.right, wq, p.wS * sS);
  part('weapon_fx', grip.right, wq, [p.wfx * sS, p.wS * sS * (p.wfx > 0 ? 1 : 0), p.wfx * sS]);
  const w = (p.ph || 0) * 2 * Math.PI;
  part('halo', add(fromHip(SK.halo), [0, .035 * Math.sin(w) * p.bob, 0]), mul(Tq, q(add(p.halo, [0, 0, 2.5 * Math.sin(w + 1) * p.bob]))), p.haloS * sS);
  part('aura', [0, 0, 0], R0, p.aura * sS);
  // Tenma parts (root frame; tS hides them)
  const tS = p.tS;
  part('disc', fromHip(SK.disc), mul(Tq, q(p.disc)), tS);
  const atRoot = v => rot(R0, v);
  // giant arm: the glaive grip point gH and orientation glv (root frame); the fist's X runs along the shaft, its +Y toward
  // the arm root; IK root -> wrist with the elbow pole gPole
  const gq = groundBlade(add(atRoot(p.gH), [0, p.pos[1], 0]), mul(R0, p.glv), G_ENDS), shaft = rot(gq, [0, 1, 0]);
  const gH = atRoot(p.gH), gRoot = atRoot(SK.gRoot);
  // the fist's +Y (toward the wrist) turns toward the arm root, kept continuous across frames (no one-tick roll flips)
  const up = steadyPerp(sub(gRoot, gH), shaft, prev && prev.gUp, [0, 1, 0]);
  const hq = basisQ(shaft, up, cross(shaft, up));
  const wrist = add(gH, times(up, SK.gWrist));
  const sol = ik(gRoot, wrist, SK.gU, SK.gF, atRoot(p.gPole), prev && prev.gV);
  part('g_upper', gRoot, aimQ(sub(sol.E, gRoot), atRoot([0, 0, -1])), tS);
  part('g_fore', sol.E, aimQ(sub(sol.W, sol.E), atRoot([0, 0, -1])), tS);
  part('g_hand', wrist, hq, tS);
  const glvS = tS * p.glvS;
  part('glaive', gH, gq, glvS);
  part('glaive_fx', gH, gq, [glvS * p.gfx, glvS * (p.gfx > 0 ? 1 : 0), glvS * p.gfx]);
  // thin right arms: direction channels (root frame) for the upper arm and the forearm
  for (let i = 0; i < 3; i++) {
    const r0 = atRoot(SK.raRoot[i]), du = atRoot(p['rU' + (i + 1)]), df = atRoot(p['rF' + (i + 1)]);
    const uq = aimQ(du, atRoot([-1, 0, -.4])), e = add(r0, times(unit(du), SK.raU));
    part(`ra${i + 1}_up`, r0, uq, tS);
    part(`ra${i + 1}_fo`, e, aimQ(df, atRoot([-1, 0, -.4])), tS);
  }
  // gauntlets (root frame positions and eulers; the right one mirrors the left's euler)
  part('gaunt_l', atRoot(p.gtL), mul(R0, q(p.gtLe)), tS);
  part('gaunt_r', atRoot(p.gtR), mul(R0, q(mirrorE(p.gtRe))), tS);
  // root offset (float, bob, body shifts), then visibility about the body centre; a pose whose body (soles, knees,
  // sleeves) would go below the floor is lifted onto it
  let bodyMin = footMin;
  for (const n of BODY) { const v = o[n], k = PART_SCALE[n].map(x => x / 16); for (const P of bodyHull(n)) bodyMin = Math.min(bodyMin, v.t[1] + rot(v.q, [P[0] * k[0], P[1] * k[1], P[2] * k[2]])[1]); }
  const lift = Math.max(0, -(bodyMin + p.pos[1]) + .004);
  const bob = [0, .2 * Math.sin(w) * p.tBob + lift, 0];
  for (const v of Object.values(o)) v.t = add(add(v.t, p.pos), bob);
  if (p.vis !== 1) {
    const c = add(hip, p.pos);
    for (const v of Object.values(o)) { v.t = add(c, times(sub(v.t, c), p.vis)); v.s = times(v.s, p.vis); }
  }
  o.aura.t = [o.aura.t[0], 0, o.aura.t[2]];                // the guard ring stays on the floor
  for (const g of ['gaunt_l', 'gaunt_r']) o[g].t = [o[g].t[0], Math.max(o[g].t[1], .58), o[g].t[2]];   // gauntlets >= 0.3 b clear
  Object.defineProperty(o, '_grip', {value: add(add(grip.right, p.pos), bob), enumerable: false});
  Object.defineProperty(o, '_prev', {value: {gUp: up, gV: sol.v}, enumerable: false});
  return o;
}
export function toDisplay(name, v) {
  const k = PART_SCALE[name];
  return {t: toDisplayT(v.t), q: toDisplayQ(v.q), s: v.s.map((x, i) => x * k[i])};
}
// A-frame model points of every element (8 corners after its element rotation), per model: for the floor and culling
// checks. Units -> blocks: times PART_SCALE / 16.
export function modelPoints(els) {
  const out = [];
  for (const e of els) {
    const [x0, y0, z0] = e.from, [x1, y1, z1] = e.to;
    for (const x of [x0, x1]) for (const y of [y0, y1]) for (const z of [z0, z1]) {
      let P = [x, y, z];
      if (e.rotation) {
        const {origin: O, axis, angle} = e.rotation, a = angle * Math.PI / 180, c = Math.cos(a), s = Math.sin(a);
        const d = [P[0] - O[0], P[1] - O[1], P[2] - O[2]];
        const r = axis === 'x' ? [d[0], d[1] * c - d[2] * s, d[1] * s + d[2] * c] : axis === 'y' ? [d[0] * c + d[2] * s, d[1], -d[0] * s + d[2] * c] : [d[0] * c - d[1] * s, d[0] * s + d[1] * c, d[2]];
        P = [r[0] + O[0], r[1] + O[1], r[2] + O[2]];
      }
      out.push([8 - P[0], P[1] - 8, P[2] - 8]);           // model -> A-frame
    }
  }
  return out;
}
export {checkBounds};
