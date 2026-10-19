// Part models of the Moonlit Butterfly (달빛 환영 나비) rig, used by build_mboss_butterfly_rig.mjs.
//
// Authoring frame ("A-frame", the rig's frame): +X = her LEFT (screen right in a front view), +Y up, -Z forward;
// units are model units relative to the display pivot (model [8,8,8]); 16 units = the part's display scale in
// blocks (butterfly_pose.mjs PART_SCALE). Paired parts are authored for her left side and mirrored for the right
// (mboss_model_lib.mjs mirrorModel), never with a negative display scale. Limbs hang along -Y from their joint
// with their front toward -Z.
//
// Construction (model.md §7): painted cutout cards for everything flat or fluffy (wings, fur, blades, crescents,
// helmet facets, streamers, ribbons), smooth turned solids (smooth3 below) under wrap textures for the round body
// parts and the props, thin boxes for the antenna rods. Constraints: coordinates within -16..32, single-axis element
// rotations in 22.5 degree steps within +-45 (checkBounds / rotM).
import {abox, cardZ as cardZRect, cardX, cardY, mirrorModel, shiftModel, lathe, faceEl, checkBounds,
  vadd, vsc, vdot, rotA, faceOfDir, DK} from './mboss_model_lib.mjs';
import {CARD, BODY, PROPS, profile} from './butterfly_paint.mjs';
import {LEG_LEN, TENDRIL_END} from './butterfly_pose.mjs';

export {checkBounds};

// ---- smooth turned solids (the body, the legs, the props) ---------------------------------------------------------
// The rings of mboss_model_lib turned() meet in ledge discs; on a soft body those discs and the radius steps read as
// stacked tins. Here each ring is a circumscribed 16-gon of an ELLIPSE (semi-axes r*kx across, r*kz front-back,
// tangent facets at 22.5 degree steps, single-axis element turns as lathe()), the stations are spaced so the radius
// changes by at most `step` units between rings, and a ring reaches into a wider neighbour by `reach` of the
// neighbour's length instead of being closed by a disc: looking into the thin step one sees the same surface go on
// (it is hidden inside the wider ring otherwise). Only the open ends get caps (polar sprites, like the Guardian's
// ledges). u of the wrap = azimuth (0 front, .25 her left, .5 back, .75 her right), v = position along the axis.
const AX = {y: {A: [0, 1, 0], e0: [0, 0, -1], e1: [1, 0, 0]}, z: {A: [0, 0, 1], e0: [0, 1, 0], e1: [1, 0, 0]}, x: {A: [1, 0, 0], e0: [0, 0, -1], e1: [0, 1, 0]}};
function ovalRing(axis, c, a0, a1, r, tex, V, {kx = 1, kz = 1, n = 16, u0 = 0, u1 = 1} = {}) {
  const {A, e0, e1} = AX[axis], dirs = [e0, e1, vsc(e0, -1), vsc(e1, -1)], els = [];
  const nr = k => { const p = k * 2 * Math.PI / n; return [Math.cos(p), Math.sin(p)]; };
  const h = k => { const [a, b] = nr(k); return r * Math.hypot(kz * a, kx * b); };
  const vert = k => {                                  // corner between facet k and k + 1 (coordinates along e0, e1)
    const [a, b] = nr(k), [cc, d] = nr(k + 1), det = a * d - b * cc, h1 = h(k), h2 = h(k + 1);
    return [(h1 * d - b * h2) / det, (a * h2 - cc * h1) / det];
  };
  const mid = (a0 + a1) / 2;
  for (let k = 0; k < n; k++) {
    const [ca, sa] = nr(k), sOf = v => -sa * v[0] + ca * v[1];
    const s0 = sOf(vert(k - 1)) - .012, s1 = sOf(vert(k)) + .012;
    const phi = k * 360 / n, q = Math.round(phi / 90), g = phi - 90 * q, d = dirs[q % 4], t = dirs[(q + 1) % 4], hk = h(k);
    const P = (a, s) => vadd(vadd(c, vsc(A, a)), vadd(vsc(d, hk), vsc(t, s)));
    const fn = X => { const rel = X.map((x, i) => x - c[i]); return [16 * (u0 + (u1 - u0) * (k + (vdot(rel, t) - s0) / (s1 - s0)) / n), 16 * (vdot(rel, A) - V.vFrom) / (V.vTo - V.vFrom)]; };
    const sg = vdot(rotA(axis, 10, d), t) > 0 ? 1 : -1;
    els.push(faceEl([P(a0, s0), P(a1, s1)], {[faceOfDir(d)]: {tex, fn}}, {shade: false, rot: g ? [axis, sg * g, vadd(c, vsc(A, mid))] : undefined}));
  }
  return els;
}
// Elliptic cap across the axis at a (side '+' or '-'), inscribed in the ring it closes; polar sprite (sprite angle =
// azimuth, as the Guardian's ledge sprites).
function ovalCap(axis, c, a, r, side, tex, {kx = 1, kz = 1} = {}) {
  const {A, e0, e1} = AX[axis], O = vadd(c, vsc(A, a)), rx = r * kx * DK, rz = r * kz * DK;
  const P = (i, j) => vadd(O, vadd(vsc(e0, i * rz), vsc(e1, j * rx)));
  const fn = X => { const rel = X.map((x, i) => x - O[i]); return [16 * (.5 + vdot(rel, e1) / (2 * rx)), 16 * (.5 + vdot(rel, e0) / (2 * rz))]; };
  return faceEl([P(-1, -1), P(1, 1)], {[faceOfDir(vsc(A, side === '+' ? 1 : -1))]: {tex, fn}}, {shade: false});
}
// Stations from a0 to a1 (ascending) so that neighbouring rings differ by at most `step` units of radius and no ring
// is longer than `maxLen`.
function smoothStations(a0, a1, prof, {step = .14, maxLen = 2.4, minLen = .35} = {}) {
  const out = [a0];
  let a = a0;
  while (a < a1 - 1e-6) {
    let L = Math.min(maxLen, a1 - a);
    while (L > minLen && Math.abs(prof(a + L) - prof(a)) > step) L *= .8;
    a = Math.min(a1, a + Math.max(L, Math.min(minLen, a1 - a)));
    if (a1 - a < minLen * .5) a = a1;
    out.push(a);
  }
  return out;
}
// Smooth turned solid along `axis` through c: radius prof(a) between a0 and a1, wrap tex (v from V.vFrom to V.vTo
// along the axis), ends '-' / '+' capped with capTex.
function smooth3(axis, c, a0, a1, prof, tex, V, {kx = 1, kz = 1, step, maxLen, minLen, reach = .55, ends = '', capTex = tex + '_cap', u0, u1} = {}) {
  const at = smoothStations(a0, a1, prof, {step, maxLen, minLen});
  const rs = at.slice(1).map((x, i) => prof((at[i] + x) / 2)), els = [];
  rs.forEach((r, i) => {
    const dn = i > 0 && rs[i - 1] > r + 1e-3 ? (at[i] - at[i - 1]) * reach : 0;
    const up = i < rs.length - 1 && rs[i + 1] > r + 1e-3 ? (at[i + 2] - at[i + 1]) * reach : 0;
    els.push(...ovalRing(axis, c, at[i] - dn, at[i + 1] + up, r, tex, V, {kx, kz, u0, u1}));
  });
  if (ends.includes('-')) els.push(ovalCap(axis, c, at[0], rs[0], '-', capTex, {kx, kz}));
  if (ends.includes('+')) els.push(ovalCap(axis, c, at[at.length - 1], rs[rs.length - 1], '+', capTex, {kx, kz}));
  return els;
}
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
const both = (els, mirrored) => [...els, ...mirrorModel(mirrored ?? els)];

// ---- body -------------------------------------------------------------------------------------------------------
// Smooth turned solids on the BODY profiles (butterfly_paint.mjs), see smooth3: no section seams, elliptic torso and
// hips. The torso's bottom ring sits inside the pelvis, the pelvis's top ring inside the torso, so the two displays
// overlap with no visible edge when she bends.
const body = (k, tex, opt = {}) => { const B = BODY[k]; return smooth3('y', [0, 0, 0], B.a[0], B.a[1], B.r, tex, {vFrom: B.a[1], vTo: B.a[0]}, {kz: B.kz || 1, ...opt}); };
function pelvis() {
  // hips narrowing to the crotch (capped underneath), navy hip plates with lime swirls, small steel fins (both sides)
  const side = [
    cardTurned('hipplate', -1.2, moveRect(CARD.hipplate, 2.4, .4), -22.5),
    cardZ('fin', .6, moveRect(CARD.fin, 3.1, -.6), {rot: ['y', -45, [3.6, -1, .6]]}),
    cardZ('fin', 1.4, moveRect(CARD.fin, 2.6, -1.8), {rot: ['y', -45, [3.1, -2.2, 1.4]]}),
  ];
  return [...body('pelvis', 'pelvis_w', {ends: '-', step: .24, minLen: .4}), ...both(side)];
}
function torso() {
  // slim waist (0.42 b) widening to the chest under the mane and to the hips; the lavender belly band down the front
  return body('torso', 'torso_w', {step: .16});
}
function collar() {
  // an octagonal shell of fur cards round a turned fur core: the front ruff, the front corners, the sides, the
  // blue-tipped back corners, the back (hood, capelets, spine V, tabard) and a fur ring on top round the neck
  // a rounded fur ball under the cards (no straight cylinder sides)
  // the fur ball under the cards: elliptic, a little behind the pivot and domed low at the top, so it stays behind
  // the mask and under the chin
  const core = smooth3('y', [0, 0, .5], -4.0, 2.0, profile([[-4.0, 2.4], [-3.1, 3.9], [-1.6, 4.7], [0, 4.75], [1.0, 4.2], [1.6, 3.2], [2.0, 1.8]]), 'furw',
    {vFrom: 2.0, vTo: -4.0}, {kz: .78, ends: '-+', capTex: 'furw_cap', step: .3});
  const fs = CARD.mane_fs, bs = CARD.mane_bs, sd = CARD.mane_s;
  const left = [
    cardTurned('mane_fs', -3.6, moveRect(fs, 7.0, -.2), -45),
    cardX('mane_s', 9.4, {Z0: sd.X0 + .6, Z1: sd.X1 + .6, Y0: sd.Y0, Y1: sd.Y1}),
    cardTurned('mane_bs', 3.8, moveRect(bs, 6.6, -.4), 45, {flipU: true}),
  ];
  return [
    ...core,
    cardZ('mane_f', -4.9),
    cardZ('mane_b', 5.6, CARD.mane_b, {flipU: true}),
    ...both(left),
  ];
}
function head() {
  // faceted mask (two halves meeting in a forward ridge at z -1.0), helmet back, side plates, crown spikes,
  // cheek blades (the eyes and the chevron are head_glow)
  const H = CARD.helm, ridge = -1.0;
  const halfMask = side => cardZ('helm', ridge, half(H, side), {uvr: uvHalf(H, side), rot: ['y', side > 0 ? -22.5 : 22.5, [0, 3, ridge]]});
  // the back of the helmet: a smooth slate dome behind the mask (its front stays behind the facets), so the head
  // is a closed shell from the side and from behind
  const dome = smooth3('y', [0, 0, 1.4], 1.2, 6.4, profile([[1.2, 1.15], [1.6, 1.8], [2.4, 2.25], [3.4, 2.38], [4.4, 2.2], [5.2, 1.75], [5.9, 1.05], [6.4, .25]]), 'helmw',
    {vFrom: 6.4, vTo: 1.2}, {kz: .9, ends: '-+', capTex: 'helmw_cap', step: .17, minLen: .3});
  return [
    halfMask(1), halfMask(-1),
    ...dome,
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
  // antennae: thin periwinkle rods from the brow, built as a chain of three game-shaded boxes bending outward
  // (0, 22.5, 45 degrees) so they are one rod from every side (crossed cards showed two diverging rods in 3/4
  // views); streamers: one broad lime flame card each, rooted at the back of the helmet and turned 22.5 degrees so
  // the blades sweep back and keep their S-curve in the front view
  const S = moveRect(CARD.streamer, .2, 0), z = -1.6, out = [];
  let p = [.6, -.4];
  // [angle, length, half thickness]: thinning toward the tip; unshaded, the wrap carries the light
  for (const [deg, L, t] of [[0, 1.5, .19], [-22.5, 2.8, .17], [-22.5, 2.6, .15], [-45, 2.4, .12]]) {
    const a = deg * Math.PI / 180, e = .12;
    out.push(abox([p[0] - t, p[1] - e, z - t], [p[0] + t, p[1] + L + e, z + t], {all: 'antw'}, {shade: false, rot: deg ? ['z', deg, [p[0], p[1], z]] : undefined}));
    p = [p[0] - Math.sin(a) * L, p[1] + Math.cos(a) * L];
  }
  out.push(cardZ('streamer', .6, S, {rot: ['y', -22.5, [.4, -1.6, .6]]}));
  return both(out);
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
// Smooth turned thigh with a rounded knee end; the fur boot is a turned core (fur wrap) under four crossed fur cards
// painted on the same profile (a shaggy outline from every side), white spiky tufts round the knee, then the lower
// boot flaring to the ankle cuff with a pointed fringe over the cream hoof and its ivory claws.
const FT = LEG_LEN.foot * 16;
const furStar = sprite => star(sprite, CARD[sprite]);
function thigh() {
  return body('thigh', 'thigh_w', {ends: '-', step: .15, minLen: .45});
}
function shin() {
  return [
    ...body('shin', 'boot_s', {ends: '+', capTex: 'boot_s_cap', step: .13}),
    ...furStar('fur_s'),
    cardTurned('knee', -.8, moveRect(CARD.knee, 1.4, -.6), -45),
  ];
}
function foot() {
  return [
    ...body('foot', 'boot_f', {ends: '-', capTex: 'boot_f_cap', step: .2, minLen: .5}),
    ...furStar('fur_f'),
    ...body('hoof', 'hoof_w', {ends: '-', step: .22, minLen: .5}),
    cardZ('hoof_claws', -1.3, moveRect(CARD.hoof_claws, 0, -FT + .9), {rot: ['x', 22.5, [0, -FT + .9, -1.3]]}),
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
  // 4 dark diamond plates hovering above and behind the shoulders (v4 f720: two per side, fanning out like the top
  // feathers of a wing), each a crossed pair turned its own way. They float 0.27 b behind the spine: in butterfly
  // form that is behind the forewing roots, so the opaque wing plates hide them from the front instead of the
  // diamonds floating over the plates (they show beside the mane in human form, and over the shoulders from behind).
  const D = CARD.diamond, out = [];
  // the pairs sit at different depths and heights per side, so from the side they read as four separate plates
  for (const [x, y, z, a] of [[13.8, 1.8, 3.4, 22.5], [17.2, -1.6, 5.4, -22.5], [-13.8, 2.4, 4.6, -22.5], [-17.2, -1.0, 6.4, 22.5]]) {
    const r = moveRect(D, x, y), k = .62;
    out.push(cardZ('diamond', z, r, {rot: ['z', a, [x, y, z]]}),
      cardX('diamond', x, {Z0: z + D.X0 * k, Z1: z + D.X1 * k, Y0: y + (r.Y0 - y) * k, Y1: y + (r.Y1 - y) * k}, {rot: ['x', a, [x, y, z]]}));
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
// Turned prop solid on a PROPS profile (butterfly_paint.mjs).
const propSolid = (k, tex, opt = {}) => { const B = PROPS[k]; return smooth3('y', [0, 0, 0], B.a[0], B.a[1], B.r, tex, {vFrom: B.a[1], vTo: B.a[0]}, {kz: B.kz || 1, step: .5, maxLen: 2.6, minLen: .8, ...opt}); };
function cocoon() {
  // scale 3 (1 u = 0.19 b, 3.95 b tall): a glowing lime bud (its lower end the crystal spike) inside two wrapped wing
  // plates (a cut-out turned shell 0.07 b outside it: an X of lime-edged plates, a V window over the bud, a scalloped
  // top), and curled scroll horns at the upper corners as crossed cards (v1 f120-150, sheet 08 H)
  const H = CARD.cocoon_hook, k = .72, bx = 3.1, by = 2.6;
  const hook = side => {
    const r = {X0: bx + H.X0 * k, X1: bx + H.X1 * k, Y0: by + H.Y0 * k, Y1: by + H.Y1 * k};
    const m = side > 0 ? r : {X0: -r.X1, X1: -r.X0, Y0: r.Y0, Y1: r.Y1};
    return [cardZ('cocoon_hook', 0, m, {flipU: side < 0}),
      cardX('cocoon_hook', side * 3.0, {Z0: -(r.X1 - bx) * .7, Z1: -(r.X0 - bx) * .7, Y0: r.Y0, Y1: r.Y1}, {flipU: side > 0})];
  };
  return [...propSolid('cocoonCore', 'cocoon_core', {step: .4, minLen: .6}), ...propSolid('cocoonShell', 'cocoon_shell', {step: .25, minLen: .5}), ...hook(1), ...hook(-1)];
}
function cocoonHalo() {
  // a soft lime glow card (summoned with billboard centre so it always faces the camera)
  return [cardZ('cocoon_glow', 0, scaleRect(CARD.cocoon_glow, 1.6))];
}
function pod() {
  // scale 2.5 (1 u = 0.156 b): the four wings folded round her, a cut-out egg-shaped shell of wing panels (lime scroll
  // frames, opal windows, steel spars, violet rims) over a glowing core that leaks through the seams; the forewing
  // hindwing blade tips stick out below the sides (v3 f1314-1347, v4 f440)
  // the hindwing blade tips stick out of the lower sides with their glowing blue points (crossed cards)
  const H = CARD.pod_hook, bx = 6.6, by = -9.6;
  const hook = side => {
    const r = {X0: bx + H.X0, X1: bx + H.X1, Y0: by + H.Y0, Y1: by + H.Y1};
    const m = side > 0 ? r : {X0: -r.X1, X1: -r.X0, Y0: r.Y0, Y1: r.Y1};
    return [cardZ('pod_hook', 0, m, {flipU: side < 0}), cardX('pod_hook', side * 6.6, {Z0: -(r.X1 - bx) * .7, Z1: -(r.X0 - bx) * .7, Y0: r.Y0, Y1: r.Y1}, {flipU: side > 0})];
  };
  return [...propSolid('podCore', 'pod_core', {ends: '-+', capTex: 'pod_core', step: 1.2, minLen: 1.4, maxLen: 3.5}), ...propSolid('podShell', 'pod_shell', {step: .26, minLen: .5}), ...hook(1), ...hook(-1)];
}
// Annulus sprites for the orb's ledges (inner / outer radius ratios, see butterfly_paint.mjs orbAnnulus).
const ORB_ANN = [.5, .7, .85, .95];
function orb() {
  // translucent lime glass sphere, r 0.85 b at scale 1 (13.6 u): 16 bands of equal angle that meet edge to edge (no
  // overlaps, so the glass shows one layer), each step closed by a flat glass annulus (a polar sprite whose inner
  // ratio is the next smaller of ORB_ANN), polar caps at the poles
  const R = 13.6, at = Array.from({length: 17}, (_, i) => R * Math.sin((-90 + 180 * i / 16) * Math.PI / 180)), V = {vFrom: R, vTo: -R};
  const rs = at.slice(1).map((x, i) => Math.sqrt(Math.max(0, R * R - ((at[i] + x) / 2) ** 2)) * 1.01), els = [];
  rs.forEach((r, i) => els.push(...ovalRing('y', [0, 0, 0], at[i], at[i + 1], r, 'orb', V)));
  for (let i = 0; i < 15; i++) {
    const hi = Math.max(rs[i], rs[i + 1]), lo = Math.min(rs[i], rs[i + 1]);
    if (hi - lo < .05) continue;
    const k = [...ORB_ANN].reverse().find(x => x <= lo / hi) ?? ORB_ANN[0];
    els.push(ovalCap('y', [0, 0, 0], at[i + 1], hi, rs[i] > rs[i + 1] ? '+' : '-', 'orb_a' + Math.round(k * 100)));
  }
  els.push(ovalCap('y', [0, 0, 0], at[0], rs[0], '-', 'orb_cap'), ovalCap('y', [0, 0, 0], at[16], rs[15], '+', 'orb_cap'));
  return els;
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
