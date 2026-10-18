// Part models of the Moonlit Butterfly (달빛 환영 나비) rig, used by build_mboss_butterfly_rig.mjs.
//
// Authoring frame ("A-frame", the rig's frame): +X = her LEFT (screen right in a front view), +Y up, -Z forward;
// units are model units relative to the display pivot (model [8,8,8]); 16 units = the part's display scale in
// blocks (butterfly_pose.mjs PART_SCALE). Paired parts are authored for her left side and mirrored for the right
// (mboss_model_lib.mjs mirrorModel), never with a negative display scale. Limbs hang along -Y from their joint
// with their front toward -Z.
//
// Construction (model.md §7): painted cutout cards for everything flat or fluffy (wings, fur, blades, crescents,
// helmet facets, streamers, ribbons), turned (lathe) solids under wrap textures for the round limbs, the torso and
// the cores. Constraints: coordinates within -16..32, single-axis element rotations in 22.5 degree steps within
// +-45 (checkBounds / rotM).
import {abox, cardZ as cardZRect, cardX, cardY, mirrorModel, shiftModel, turned, stations, lathe, faceEl, checkBounds} from './mboss_model_lib.mjs';
import {CARD} from './butterfly_paint.mjs';
import {LEG_LEN, TENDRIL_END} from './butterfly_pose.mjs';

export {checkBounds};
const cardZ = (sprite, z, rect = CARD[sprite], opt) => cardZRect(sprite, z, rect, opt);
const scaleRect = (r, k, [cx, cy] = [0, 0]) => ({X0: cx + (r.X0 - cx) * k, X1: cx + (r.X1 - cx) * k, Y0: cy + (r.Y0 - cy) * k, Y1: cy + (r.Y1 - cy) * k});
const moveRect = (r, dx, dy) => ({X0: r.X0 + dx, X1: r.X1 + dx, Y0: r.Y0 + dy, Y1: r.Y1 + dy});
const half = (r, side) => (side > 0 ? {X0: 0, X1: r.X1, Y0: r.Y0, Y1: r.Y1} : {X0: r.X0, X1: 0, Y0: r.Y0, Y1: r.Y1});
const uvHalf = (r, side) => { const m = -r.X0 / (r.X1 - r.X0); return side > 0 ? [m, 0, 1, 1] : [0, 0, m, 1]; };
// Card turned about the vertical axis through its own rect centre (deg as cardZ's rot).
const cardTurned = (sprite, z, rect, deg, opt = {}) => cardZ(sprite, z, rect, {...opt, rot: ['y', deg, [(rect.X0 + rect.X1) / 2, (rect.Y0 + rect.Y1) / 2, z]]});
// Four cards crossing on the vertical axis (0, 90, +-45 degrees): a fluffy or crystalline volume from every side.
function star(sprite, rect, {x = 0, z = 0, flip = false} = {}) {
  const c = [x, (rect.Y0 + rect.Y1) / 2, z], w = (rect.X1 - rect.X0) / 2, rx = {X0: x - w, X1: x + w, Y0: rect.Y0, Y1: rect.Y1};
  return [
    cardZ(sprite, z, rx, {flipU: flip}),
    cardX(sprite, x, {Z0: z - w, Z1: z + w, Y0: rect.Y0, Y1: rect.Y1}, {flipU: !flip}),
    cardZ(sprite, z, rx, {flipU: !flip, rot: ['y', 45, c]}),
    cardZ(sprite, z, rx, {flipU: flip, rot: ['y', -45, c]}),
  ];
}
// Turned solid along Y from y0 down to y1 with radius r(y) (n sections), wrap texture tex.
const limb = (y0, y1, r, n, tex, ends = '') => turned('y', [0, 0, 0], stations(y1, y0, n), r, tex, tex, {vFrom: y0, vTo: y1}, ends);
const both = (els, mirrored) => [...els, ...mirrorModel(mirrored ?? els)];

// ---- body -------------------------------------------------------------------------------------------------------
function pelvis() {
  // hips (0.42 b) narrowing to the crotch, navy hip plates with lime swirls, small steel fins (both sides)
  const hips = limb(2.4, -3.0, y => Math.max(2.3, 3.4 - .12 * (y + .5) ** 2), 3, 'skin', '-');
  const side = [
    cardTurned('hipplate', -1.2, moveRect(CARD.hipplate, 2.4, .4), -22.5),
    cardZ('fin', .6, moveRect(CARD.fin, 3.1, -.6), {rot: ['y', -45, [3.6, -1, .6]]}),
    cardZ('fin', 1.4, moveRect(CARD.fin, 2.6, -1.8), {rot: ['y', -45, [3.1, -2.2, 1.4]]}),
  ];
  return [...hips, ...both(side)];
}
function torso() {
  // slim waist (0.3 b) widening to the chest under the collar and to the hips below; the lavender stripe runs down
  // the front (skin wrap u = 0)
  return limb(8.0, -2.6, y => 2.4 + (y > 1.2 ? .2 * (y - 1.2) : .3 * (1.2 - y)), 4, 'skin', '');
}
function collar() {
  // an octagonal shell of fur cards round a turned fur core: the front ruff, the front corners, the sides, the
  // blue-tipped back corners, the back (hood, capelets, spine V, tabard) and a fur ring on top round the neck
  // a rounded fur ball under the cards (no straight cylinder sides)
  const core = limb(3.8, -4.0, y => Math.max(2.6, 4.7 * Math.sqrt(Math.max(0, 1 - ((y + .1) / 5.2) ** 2))), 5, 'furw', '-+');
  const fs = CARD.mane_fs, bs = CARD.mane_bs, sd = CARD.mane_s;
  const left = [
    cardTurned('mane_fs', -3.6, moveRect(fs, 7.0, -.2), -45),
    cardX('mane_s', 9.4, {Z0: sd.X0 + .6, Z1: sd.X1 + .6, Y0: sd.Y0, Y1: sd.Y1}),
    cardTurned('mane_bs', 3.8, moveRect(bs, 6.6, -.4), 45, {flipU: true}),
  ];
  return [
    ...core,
    cardZ('mane_f', -5.7),
    cardZ('mane_b', 5.6, CARD.mane_b, {flipU: true}),
    ...both(left),
  ];
}
function head() {
  // faceted mask (two halves meeting in a forward ridge at z -1.0), helmet back, side plates, crown spikes,
  // cheek blades (the eyes and the chevron are head_glow)
  const H = CARD.helm, ridge = -1.0;
  const halfMask = side => cardZ('helm', ridge, half(H, side), {uvr: uvHalf(H, side), rot: ['y', side > 0 ? -22.5 : 22.5, [0, 3, ridge]]});
  const hs = CARD.helm_side;
  return [
    halfMask(1), halfMask(-1),
    abox([-1.9, 1.1, .1], [1.9, 5.0, 2.4], {all: 'helmw'}),
    cardX('helm_side', 2.45, {Z0: hs.X0 + .6, Z1: hs.X1 + .6, Y0: hs.Y0, Y1: hs.Y1}),
    cardX('helm_side', -2.45, {Z0: hs.X0 + .6, Z1: hs.X1 + .6, Y0: hs.Y0, Y1: hs.Y1}),
    cardZ('crown', .5), cardX('crown', 0, {Z0: CARD.crown.X0 + .5, Z1: CARD.crown.X1 + .5, Y0: CARD.crown.Y0, Y1: CARD.crown.Y1}),
    ...both([cardTurned('cheek', -.2, CARD.cheek, -22.5)]),
  ];
}
function headGlow() {
  // eyes on the eye plates of the mask, the chevron on the brow (each half turned with its facet)
  const ridge = -1.0, eps = .12;
  const eye = side => cardZ('eye', ridge - eps, moveRect(CARD.eye, 1.45 * side, 2.05), {rot: ['y', side > 0 ? -22.5 : 22.5, [0, 2, ridge]]});
  const C0 = moveRect(CARD.chev, 0, 4.15);
  const chev = side => cardZ('chev', ridge - eps, half(C0, side), {uvr: uvHalf(C0, side), rot: ['y', side > 0 ? -22.5 : 22.5, [0, 4, ridge]]});
  return [eye(1), eye(-1), chev(1), chev(-1)];
}
function crest() {
  // antennae from the brow (in front), the lime streamers from the back of the helmet; each with a side card
  const A = moveRect(CARD.antenna, .2, 0), S = moveRect(CARD.streamer, .2, 0);
  const left = [
    cardZ('antenna', -1.6, A),
    cardX('antenna', .5, {Z0: -1.6 - .5, Z1: -1.6 + (A.X1 - A.X0) - .5, Y0: A.Y0, Y1: A.Y1}, {flipU: true}),
    cardZ('streamer', .6, S),
    cardX('streamer', 1.1, {Z0: .2, Z1: .2 + (S.X1 - S.X0), Y0: S.Y0, Y1: S.Y1}, {flipU: true}),
  ];
  return both(left);
}
function fan() {
  // her left fan (scale 1.25): the frontal blade card, a second blade card swept back, the upright shoulder plate
  const sp = scaleRect(moveRect(CARD.shplate, -.4, .2), .8);
  return [
    cardZ('fan', 0),
    cardZ('fanb', .5, CARD.fanb, {rot: ['y', -45, [0, 0, .5]]}),
    cardTurned('shplate', -.7, sp, -22.5),
    cardX('shplate', .3, {Z0: sp.X0 - .7, Z1: sp.X1 - .7, Y0: sp.Y0, Y1: sp.Y1}),
  ];
}
// ---- legs (her left; the right ones mirror) -------------------------------------------------------------------------
const TH = LEG_LEN.thigh * 16, SH = LEG_LEN.shin * 16, FT = LEG_LEN.foot * 16;
function thigh() {
  return limb(.8, -TH - .4, y => 1.45 - .45 * (-y / TH), 2, 'thigh', '-');
}
function shin() {
  // upper fur boot: a turned core under a star of shaggy tuft cards; white spiky tufts at the outer knee
  const R = CARD.boot_tuft, r = {X0: R.X0, X1: R.X1, Y0: -SH - .6, Y1: 1.0};
  return [
    ...limb(.6, -SH, y => 1.1 + .55 * (-y / SH), 2, 'boot', '-+'),
    ...star('boot_tuft', r),
    cardTurned('knee', -.8, moveRect(CARD.knee, 1.4, -.6), -45),
  ];
}
function foot() {
  // lower boot flaring to the ankle, the cream hoof and its ivory claws pointing forward at the end
  const R = CARD.boot_flare, r = {X0: R.X0, X1: R.X1, Y0: -FT + .2, Y1: R.Y1};
  return [
    ...limb(.4, -FT + 1.6, y => 1.65 + .45 * (-y / FT), 2, 'boot', '-'),
    ...star('boot_flare', r),
    ...limb(-FT + 2.2, -FT - .2, y => .55 + 1.15 * ((y + FT + .2) / 2.4), 3, 'hoofw', '-+'),
    cardZ('hoof_claws', -1.5, moveRect(CARD.hoof_claws, 0, -FT + .9), {rot: ['x', 22.5, [0, -FT + .9, -1.5]]}),
  ];
}
// ---- crescent "hands" and flakes ------------------------------------------------------------------------------------
function crescent(k, sprite = 'crescent') {
  const r = scaleRect(CARD[sprite], k);
  return [cardZ(sprite, -.3, r), cardZ(sprite, .3, r)];
}
function shard(k) {
  const r = scaleRect(CARD.shard, k);
  return [cardZ('shard', -.2, r), cardZ('shard', .2, r), cardX('shard', .2 * k, {Z0: r.X0, Z1: r.X1, Y0: r.Y0, Y1: r.Y1})];
}
function flakes() {
  // 4 dark diamond plates hovering above the shoulders, each a crossed pair, turned their own ways
  const D = CARD.diamond, out = [];
  for (const [x, y, z, a] of [[14.4, 1.6, 0, 22.5], [17.6, -1.6, 1.2, -22.5], [-14.4, 1.6, .4, -22.5], [-17.6, -1.6, -.8, 22.5]]) {
    const r = moveRect(D, x, y);
    out.push(cardZ('diamond', z, r, {rot: ['z', a, [x, y, z]]}), cardX('diamond', x, {Z0: z + D.X0, Z1: z + D.X1, Y0: r.Y0, Y1: r.Y1}, {rot: ['x', a, [x, y, z]]}));
  }
  return out;
}
// ---- wings and tendrils (her left; looks swap the sprites) ----------------------------------------------------------
// Each wing pivots at its own root on the upper back (butterfly_pose.mjs ATTACH, 0.42 b beside the spine) and its
// card starts `dx` card units further out, so the two wing sets stay apart with the head and the crest in the gap
// between them (PDF render, v2 f2070). The cards are modelled at half size (k) so the shifted rect stays inside the
// model bounds; PART_SCALE doubles to match.
export const WING_FIT = {fw: {k: .5, dx: 3.6}, hw: {k: .5, dx: 8.7}};
const fit = (r, f) => scaleRect(moveRect(r, f.dx, 0), f.k);
export const wingPoint = (w, [x, y, z = 0]) => [(x + WING_FIT[w].dx) * WING_FIT[w].k, y * WING_FIT[w].k, z];
const fwing = look => [cardZ('fw_' + look, 0, fit(CARD.fw, WING_FIT.fw))];
const fwglow = look => [cardZ('fwg_' + look, -.14, fit(CARD.fw, WING_FIT.fw)), cardZ('fwg_' + look, .14, fit(CARD.fw, WING_FIT.fw))];
const hwing = look => [cardZ('hw_' + look, 0, fit(CARD.hw, WING_FIT.hw))];
const tendrilU = look => [cardZ('tu_' + look, 0, CARD.tu)];
const tendrilL = look => [cardZ('tl_' + look, 0, CARD.tl)];
function core() {
  const r = CARD.core, c = [0, 0, 0];
  return [cardZ('core', 0, r), cardX('core', 0, {Z0: r.X0, Z1: r.X1, Y0: r.Y0, Y1: r.Y1}), cardY('core', 0, {X0: r.X0, X1: r.X1, Z0: r.Y0, Z1: r.Y1}),
    cardZ('core', 0, r, {rot: ['y', 45, c]}), cardZ('core', 0, r, {rot: ['y', -45, c]})];
}
// ---- props (not rig parts) ------------------------------------------------------------------------------------------
function cocoon() {
  // scale 3: two crossed kite cards (3.8 b tall); the window glows on both. Crossed, not a star of four: from the
  // front it shows exactly its two horn hooks, as in the reference
  const R = CARD.cocoon, c = [0, 0, 0];
  return [cardZ('cocoon', 0, R), cardX('cocoon', 0, {Z0: R.X0, Z1: R.X1, Y0: R.Y0, Y1: R.Y1}, {flipU: true})];
}
function cocoonHalo() {
  // a soft lime glow card (summoned with billboard centre so it always faces the camera)
  return [cardZ('cocoon_glow', 0, scaleRect(CARD.cocoon_glow, 1.6))];
}
function pod() {
  // scale 2.5: eight curved wing panels in an octagon (r ≈ 1.4 b) round her, shoulder-plate caps on top, a lime core
  const R = CARD.pod, rad = 8.6, d = rad / Math.SQRT2, out = [];
  out.push(cardZ('pod', -rad), cardZ('pod', rad, R, {flipU: true}));
  out.push(cardX('pod', rad, {Z0: R.X0, Z1: R.X1, Y0: R.Y0, Y1: R.Y1}), cardX('pod', -rad, {Z0: R.X0, Z1: R.X1, Y0: R.Y0, Y1: R.Y1}, {flipU: true}));
  for (const [sx, sz] of [[1, -1], [-1, -1], [1, 1], [-1, 1]]) {
    const r = moveRect(R, sx * d, 0);
    out.push(cardZ('pod', sz * d, r, {rot: ['y', sx * sz > 0 ? 45 : -45, [sx * d, 0, sz * d]]}));
  }
  const cap = moveRect(CARD.shplate, 0, 9.6);
  for (const a of [0, 45, -45]) out.push(cardZ('shplate', 0, cap, {rot: a ? ['y', a, [0, 12, 0]] : undefined}));
  out.push(cardX('shplate', 0, {Z0: cap.X0, Z1: cap.X1, Y0: cap.Y0, Y1: cap.Y1}));
  return out;
}
function orb() {
  // translucent lime glass sphere, r 0.85 b at scale 1 (13.6 u): twelve bands of a turned sphere
  const R = 13.6, at = Array.from({length: 13}, (_, i) => R * Math.sin((-90 + 15 * i) * Math.PI / 180));
  return turned('y', [0, 0, 0], at, a => R * Math.sqrt(Math.max(0, 1 - (a / R) ** 2)), 'orb', 'orb', {vFrom: R, vTo: -R}, '-+');
}
function ring() {
  // gyroscope ring (r 16 u at scale 1): a flat annulus card plus a thin turned band, so it reads from every angle
  return [cardY('ring', 0, {X0: -17.8, X1: 17.8, Z0: -17.8, Z1: 17.8}), ...lathe('y', [0, 0, 0], [{a: [-.35, .35], r: 16, tex: 'ringw'}], {vFrom: -.35, vTo: .35})];
}

// name -> elements (item model). Variants share the display of their part (item model swaps).
export const LOOKS = ['dendro', 'pyro', 'flat'];
export function partModels() {
  const m = {
    pelvis: pelvis(), torso: torso(), collar: collar(), head: head(), head_glow: headGlow(), crest: crest(),
    fan_l: fan(), fan_r: mirrorModel(fan()),
    thigh_l: thigh(), shin_l: shin(), foot_l: foot(), thigh_r: mirrorModel(thigh()), shin_r: mirrorModel(shin()), foot_r: mirrorModel(foot()),
    crescent_l: crescent(.82), crescent_r: mirrorModel(crescent(1)), crescent_tell_l: crescent(.82, 'crescent_tell'), crescent_tell_r: mirrorModel(crescent(1, 'crescent_tell')),
    shard_l: shard(.72), shard_r: mirrorModel(shard(1)),
    flakes: flakes(), core: core(),
    cocoon: cocoon(), cocoon_halo: cocoonHalo(), pod: pod(), orb: orb(), ring: ring(),
  };
  for (const look of LOOKS) {
    m['fwing_l_' + look] = fwing(look); m['fwing_r_' + look] = mirrorModel(fwing(look));
    m['fwglow_l_' + look] = fwglow(look); m['fwglow_r_' + look] = mirrorModel(fwglow(look));
    m['hwing_l_' + look] = hwing(look); m['hwing_r_' + look] = mirrorModel(hwing(look));
    m['tendril_ul_' + look] = tendrilU(look); m['tendril_ur_' + look] = mirrorModel(tendrilU(look));
    m['tendril_ll_' + look] = tendrilL(look); m['tendril_lr_' + look] = mirrorModel(tendrilL(look));
  }
  return m;
}
export {shiftModel, TENDRIL_END};
