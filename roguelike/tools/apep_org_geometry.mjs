// Models of the Apep phase-2 objects (plan §5, AP-ORG): the six organisms, the Heart of the Oasis, the 소생의 찬가 domes,
// the 둥지 wall blades, the 생명의 손 stalks and the death seed. Used by build_mboss_apep_org.mjs.
//
// Structure (ORG): owners (kinds = organisms riding their aux husk as passengers; objects = fixed or multi displays at
// a marker / spot) -> displays. A display has a joint (its model origin = its pivot) in its parent's frame (root
// displays: the object frame, origin on the floor under the object, +X = its left, +Y up, -Z its facing), a display
// scale (reach = 1.5 x scale blocks round the joint, checkBounds), looks (item ids) and a brightness. Models are authored
// in blocks with the shared shape helpers (mboss_shape_lib.mjs, mboss_model_lib.mjs): root displays with frame 'object'
// are authored in the object frame and shifted by their joint here; frame 'joint' models are authored round the joint.
// Element rotations stay single-axis on the 22.5 degree grid.
import {abox, cardZ, cardX, cardY, faceEl, faceOfDir, lathe, annulus, checkBounds, r4} from './mboss_model_lib.mjs';
import {loft, slab, crossCards, toUnits, mirrorX, retex, rockBox} from './mboss_shape_lib.mjs';
import {SH} from './apep_org_paint.mjs';

export {checkBounds};
export const RIDE_Y = 2.0;           // the husk passenger point above its feet (org manifest passenger.ride_y)
const D2R = Math.PI / 180;

// ---- small geometry helpers (blocks, A-frame) --------------------------------------------------------------------------
const shift = (els, [dx, dy, dz]) => els.map(e => {
  const o = {...e, from: [r4(e.from[0] - dx), r4(e.from[1] + dy), r4(e.from[2] + dz)], to: [r4(e.to[0] - dx), r4(e.to[1] + dy), r4(e.to[2] + dz)]};
  if (e.rotation) o.rotation = {...e.rotation, origin: [r4(e.rotation.origin[0] - dx), r4(e.rotation.origin[1] + dy), r4(e.rotation.origin[2] + dz)]};
  return o;
});
const tint = els => els.map(e => ({...e, faces: Object.fromEntries(Object.entries(e.faces).map(([k, f]) => [k, {...f, tintindex: 0}]))}));
// unshaded faces (no game face shading): the painted tones carry the light, so loft ledges blend into the surface
const flat = els => els.map(e => ({...e, shade: false}));
// stations from profile functions: a0..a1 in n steps; r(a) number or [e1+, e2+, e1-, e2-]; c(a) -> [c1, c2]
const prof = (a0, a1, n, r, c = null, box = 0) => Array.from({length: n + 1}, (_, i) => { const a = a0 + (a1 - a0) * i / n; return {a, r: r(a), c: c ? c(a) : [0, 0], box}; });
const stops = (as, rs, cs = null) => as.map((a, i) => ({a, r: rs[i], c: cs ? cs[i] : [0, 0]}));
// a two-sided card in an axis-aligned plane: corner P0 (blocks), edge vectors du (sprite s) and dv (sprite t, t = 0 at
// P0), both axis-aligned; rot = one element rotation [axis, deg, pivot]. Any in-plane sprite orientation (solveUV).
function quad(sprite, P0, du, dv, {rot, uvr = [0, 0, 1, 1], tint: tn = false} = {}) {
  const P1 = P0.map((x, i) => x + du[i] + dv[i]);
  const n = [du[1] * dv[2] - du[2] * dv[1], du[2] * dv[0] - du[0] * dv[2], du[0] * dv[1] - du[1] * dv[0]];
  const L2 = d => d[0] * d[0] + d[1] * d[1] + d[2] * d[2];
  const fn = X => { const r = X.map((x, i) => x - P0[i]); const s = (r[0] * du[0] + r[1] * du[1] + r[2] * du[2]) / L2(du), t = (r[0] * dv[0] + r[1] * dv[1] + r[2] * dv[2]) / L2(dv);
    return [16 * (uvr[0] + (uvr[2] - uvr[0]) * s), 16 * (uvr[1] + (uvr[3] - uvr[1]) * t)]; };
  const ax = n.map(Math.abs).indexOf(Math.max(...n.map(Math.abs))), dir = [0, 0, 0];
  dir[ax] = 1; const f1 = faceOfDir(dir); dir[ax] = -1; const f2 = faceOfDir(dir);
  const el = faceEl([P0, P1], {[f1]: {tex: sprite, fn}, [f2]: {tex: sprite, fn}}, {shade: false, rot});
  if (tn) for (const f of Object.values(el.faces)) f.tintindex = 0;
  return el;
}
// azimuth th (deg, 0 = forward -Z, 90 = left +X, the 22.5 grid) -> [base quadrant, residual y rotation]
const baseAz = th => { const b = Math.round(th / 90) * 90, g = b - th; if (![-45, -22.5, 0, 22.5, 45].includes(g)) throw new Error('azimuth ' + th); return [((b % 360) + 360) % 360, g]; };
const unitAz = b => [Math.round(Math.sin(b * D2R)), 0, -Math.round(Math.cos(b * D2R))];
const tanAz = b => [-Math.round(Math.cos(b * D2R)), 0, -Math.round(Math.sin(b * D2R))];   // the tangent 90 degrees clockwise from above
// a card in the radial plane at azimuth th: sprite s along the radius (rho0 -> rho1), t down from y1 to y0
function radialCard(sprite, th, rho0, rho1, y0, y1, opt = {}) {
  const [b, g] = baseAz(th), d = unitAz(b);
  return quad(sprite, [d[0] * rho0, y1, d[2] * rho0], [d[0] * (rho1 - rho0), 0, d[2] * (rho1 - rho0)], [0, y0 - y1, 0], {...opt, rot: g ? ['y', g, [0, 0, 0]] : opt.rot});
}
// a card tangent to the circle rho at azimuth th, facing outward: s across (w wide), t from the top yTop down by h;
// tilt (cardinal azimuths only, deg) leans its far end outward about the pivot edge (top, unless pivot 'bottom')
function tangentCard(sprite, th, rho, yTop, w, h, {tilt = 0, pivot = 'top', uvr, tint: tn} = {}) {
  const [b, g] = baseAz(th), d = unitAz(b), tg = tanAz(b);
  const P0 = [d[0] * rho - tg[0] * w / 2, yTop, d[2] * rho - tg[2] * w / 2];
  let rot = g ? ['y', g, [0, 0, 0]] : undefined;
  if (tilt) {
    if (g) throw new Error('tilted tangent cards only at cardinal azimuths');
    const axis = Math.abs(d[2]) > .5 ? 'x' : 'z', py = pivot === 'top' ? yTop : yTop - h;
    // outward lean of the far end: for the top pivot the bottom swings out, for the bottom pivot the top does
    const sgnOut = (axis === 'x' ? (d[2] < 0 ? 1 : -1) : (d[0] > 0 ? 1 : -1)) * (pivot === 'top' ? 1 : -1);
    rot = [axis, sgnOut * tilt, [d[0] * rho, py, d[2] * rho]];
  }
  return quad(sprite, P0, [tg[0] * w, 0, tg[2] * w], [0, -h, 0], {rot, uvr, tint: tn});
}
// a slab from a shared shape (SH): plane 'x' (u = Z, v = Y), 'z' (u = X, v = Y), 'y' (u = X, v = Z) at `at`
const shapeSlab = (name, sprite, plane, at, opt = {}) => slab({plane, at, rect: SH[name].rect, sd: SH[name].sd, sprite, edge: opt.edge || sprite, ...opt});
// mirror images in Z (z -> -z about the joint): faces north / south swap, textures flip, rotations about x and y negate
function mirrorZ(els) {
  return els.map(e => {
    const faces = {};
    for (const [f, face] of Object.entries(e.faces)) {
      const uv = face.uv.slice(), rot = face.rotation || 0;
      if (f === 'north' || f === 'south') { if (rot === 0 || rot === 180) [uv[0], uv[2]] = [uv[2], uv[0]]; else [uv[1], uv[3]] = [uv[3], uv[1]]; }
      else if (f === 'up' || f === 'down') { if (rot === 0 || rot === 180) [uv[1], uv[3]] = [uv[3], uv[1]]; else [uv[0], uv[2]] = [uv[2], uv[0]]; }
      else { if (rot === 0 || rot === 180) [uv[0], uv[2]] = [uv[2], uv[0]]; else [uv[1], uv[3]] = [uv[3], uv[1]]; }
      faces[f === 'north' ? 'south' : f === 'south' ? 'north' : f] = {...face, uv};
    }
    const out = {...e, from: [e.from[0], e.from[1], r4(16 - e.to[2])], to: [e.to[0], e.to[1], r4(16 - e.from[2])], faces};
    if (e.rotation) out.rotation = {...e.rotation, origin: [e.rotation.origin[0], e.rotation.origin[1], r4(16 - e.rotation.origin[2])], angle: e.rotation.axis === 'z' ? e.rotation.angle : -e.rotation.angle};
    return out;
  });
}
// a slab of a shared shape standing in the radial plane at azimuth th (shape u = the distance from the axis, v = height):
// quadrants 90 / 180 are built directly (u = +X / +Z), 270 and 0 as mirror images of 90 and 180
function radialSlab(name, sprite, th, opt = {}) {
  th = ((th % 360) + 360) % 360;
  const [b] = baseAz(th);
  if (b === 270) return mirrorX(radialSlab(name, sprite, 360 - th, opt));
  if (b === 0) return mirrorZ(radialSlab(name, sprite, (540 - th) % 360, opt));
  const [, g] = baseAz(th);
  return shapeSlab(name, sprite, b === 90 ? 'z' : 'x', 0, {...opt, rot: g ? ['y', g, [0, 0, 0]] : null});
}
// a 3-box rounded orb (glow balls): reads round at the sizes used here
const orb = (c, r, tex) => [abox([c[0] - r, c[1] - r * .62, c[2] - r * .62], [c[0] + r, c[1] + r * .62, c[2] + r * .62], tex),
  abox([c[0] - r * .62, c[1] - r, c[2] - r * .62], [c[0] + r * .62, c[1] + r, c[2] + r * .62], tex), abox([c[0] - r * .62, c[1] - r * .62, c[2] - r], [c[0] + r * .62, c[1] + r * .62, c[2] + r], tex)];
// a two-sided ring band (lathe outward + inward) round the y axis
const band = (c, r, y0, y1, tex, n = 16) => [...lathe('y', c, [{a: [y0, y1], r, tex}], {vFrom: y1, vTo: y0, n}), ...lathe('y', c, [{a: [y0, y1], r: r - .004, tex}], {vFrom: y1, vTo: y0, n, inward: true})];
// a cone spike as two crossed triangle cards along an axis-aligned direction dir from base point P (length L, width w);
// rot = an extra single-axis rotation about P (diagonal spikes)
function spike(sprite, P, dir, L, w, rot) {
  const a = dir.map(Math.abs).indexOf(1), o1 = [0, 0, 0], o2 = [0, 0, 0];
  const others = [0, 1, 2].filter(i => i !== a); o1[others[0]] = 1; o2[others[1]] = 1;
  const tip = dir.map(x => x * L), r = rot ? [rot[0], rot[1], P] : undefined;
  const mk = o => quad(sprite, P.map((x, i) => x + tip[i] - o[i] * w / 2), o.map(x => x * w), tip.map(x => -x), {rot: r});
  return [mk(o1), mk(o2)];
}

// ================================================================================================================
// 기본 basic: bell (melee, walks) / bag (ranged, lying), a petal crown at the bag neck, the 수호 shield overlay
// ================================================================================================================
const BELL = {y: [.15, .28, .44, .58, .7, .8, .88, .95, 1.01, 1.06], r: [.4, .44, .452, .44, .405, .352, .29, .222, .148, .07]};
function bellModel() {
  const els = [...loft('y', stops(BELL.y, BELL.r), {n: 16, tex: 'bo_bell', ledgeTex: 'bo_bell_l', caps: '+', tint: true, seed: 3})];
  for (let k = 0; k < 8; k++) {
    const th = k * 45 + 22.5 * (k % 2);
    els.push(radialCard('bo_lobe', k * 45, .26, .66, 0, .26, {tint: true}));
    if (k % 2 === 0) els.push(tangentCard('bo_lobeF', k * 45, .38, .2, .24, .24, {tilt: 45, tint: true}));
  }
  els.push(...tint(shapeSlab('b_stem', 'bo_stem', 'x', 0, {half: .028, cell: .03, inset: .4})));
  return els;
}
// the bag: the same bulb lying, the neck forward (-Z) and raised; a drawstring ring at the neck
const BAG = {z: [-.53, -.42, -.24, 0, .26, .46, .58], r: [.1, .16, .31, .43, .43, .3, .1], up: [.24, .19, .09, .02, 0, 0, 0]};
function bagModel() {
  const els = loft('z', BAG.z.map((a, i) => ({a, r: BAG.r[i], c: [0, .45 + BAG.up[i]]})), {n: 16, tex: 'bo_bell', ledgeTex: 'bo_bell_l', caps: '-+', tint: true, seed: 5});
  els.push(...tint(loft('z', [{a: -.5, r: .14, c: [0, .45 + .225]}, {a: -.44, r: .14, c: [0, .45 + .21]}], {n: 8, tex: 'bo_stem', caps: ''})));
  return els;
}
// the crown (joint at the bag neck, its +Y along the neck): 4 cardinal petals leaning out, 4 diagonal ones
function crownModel(open) {
  const els = [];
  for (let k = 0; k < 8; k++) {
    const th = k * 45, card = k % 2 === 0;
    els.push(tangentCard('bo_petal', th, card ? .06 : .075, open ? .44 : .42, .32, .44, {tilt: card ? (open ? 45 : 22.5) : 0, pivot: 'bottom', uvr: [0, 0, 1, 1]}));
  }
  // tangentCard hangs from yTop; the petals rise from the neck: shift them so their bottom edge sits at y 0
  const out = shift(els, [0, 0, 0]);
  if (open) out.push(...crossCards('bo_glow', [0, .1, 0], .26, .26, {y0: -.13}));
  return out;
}
// the shield overlay: 3 vesica panes, the bubble rim band, the yellow 3-leaf crown
function shieldModel() {
  const els = [];
  for (const th of [67.5, 180, 292.5]) els.push(tangentCard('bo_pane', th, .64, 1.47, .62, 1.42));
  els.push(...band([0, 0, 0], .8, 0, .42, 'bo_bubble'));
  els.push(...crossCards('bo_lcrown', [0, 1.42, 0], .48, .26, {y0: 0}));
  return els;
}

// ================================================================================================================
// 양육 nurturing: S ribbon stalk + fronds + gold shard, the hood cap, the orb, the immune ring overlay
// ================================================================================================================
function nurtStalk() {
  const els = [...shapeSlab('n_rib', 'nu_ribS', 'x', 0, {half: .07, cell: .08, inset: .5, edge: 'nu_rib'}),
    ...shapeSlab('n_rib2', 'nu_ribT', 'z', .02, {half: .045, cell: .08, inset: .5, edge: 'nu_rib'})];
  for (let k = 0; k < 6; k++) {
    const th = [0, 67.5, 112.5, 180, 247.5, 292.5][k], [b, g] = baseAz(th), d = unitAz(b), tg = tanAz(b);
    // a frond lying outward on the ground, tip slightly raised (cardinal ones tilted 22.5 up)
    const L = .56, w = .2, P0 = [d[0] * .08 - tg[0] * w / 2, .03, d[2] * .08 - tg[2] * w / 2];
    let rot = g ? ['y', g, [0, 0, 0]] : null;
    if (!g) { const axis = Math.abs(d[2]) > .5 ? 'x' : 'z'; rot = [axis, axis === 'x' ? (d[2] < 0 ? 22.5 : -22.5) : (d[0] > 0 ? 22.5 : -22.5), [d[0] * .08, .03, d[2] * .08]]; }
    els.push(quad('nu_frond', P0.map((x, i) => x + d[i] * L), [tg[0] * w, 0, tg[2] * w], [-d[0] * L, 0, -d[2] * L], {rot}));
  }
  els.push(...crossCards('nu_gem', [0, 1.66, .2], .18, .3, {y0: -.15}));
  return els;
}
function nurtCap(t) {
  const name = t ? 'n_hoodT' : 'n_hood', spr = t ? 'nu_hoodT' : 'nu_hood';
  return [...shapeSlab(name, spr, 'x', 0, {half: .22, cell: .07, inset: .45, edge: 'nu_hoodF'}),
    ...shapeSlab('n_hoodF', 'nu_hoodF', 'z', t ? -.2 : -.14, {half: .03, core: false})];
}
const nurtOrb = () => [...orb([0, 0, 0], .15, 'nu_orb'), ...crossCards('nu_orb', [0, 0, 0], .44, .44, {y0: -.22})];
const nurtRing = () => band([0, 0, 0], 1.3, 0, .5, 'nu_ring');

// ================================================================================================================
// 수호 guarding: helix spire (spire / bud / wisp looks, mid pivot) + the hovering orb
// ================================================================================================================
const SHEATH = {y: [0, .2, .42, .62, .8, .95], r: [.38, .36, .33, .28, .21, .13]};
function guardBase() {
  const els = [...loft('y', stops(SHEATH.y, SHEATH.r), {n: 16, tex: 'gu_sheath', ledgeTex: 'gu_sheath_l', caps: '-+', seed: 7})];
  for (let k = 0; k < 8; k++) els.push(radialCard('gu_lobe', k * 45 + 22.5, .14, .62, 0, .34));
  els.push(abox([-.12, .3, -.42], [.12, .58, -.32], 'gu_gem', {rot: ['x', -22.5, [0, .44, -.37]]}));
  return els;
}
function guardSpire() {
  return [...guardBase(), ...shapeSlab('g_ribA', 'gu_ribA', 'z', 0, {half: .03, cell: .1, inset: .5, edge: 'gu_ribA'}),
    ...shapeSlab('g_ribB', 'gu_ribB', 'x', 0, {half: .03, cell: .1, inset: .5, edge: 'gu_ribB'}),
    ...shapeSlab('g_ribB', 'gu_ribB', 'z', 0, {half: .02, core: false, rot: ['y', 45, [0, 0, 0]]})];
}
function guardBud() {
  const els = [...loft('y', stops([.95, 1.2, 1.45, 1.65, 1.82, 1.95, 2.04], [.4, .38, .33, .26, .17, .09, .03]), {n: 16, tex: 'gu_bud', ledgeTex: 'gu_bud_l', caps: '-+', seed: 9})];
  for (let k = 0; k < 8; k++) els.push(tangentCard('gu_drape', k * 45, .34, 1.3, .58, 1.3));
  for (let k = 0; k < 8; k++) els.push(radialCard('gu_lobe', k * 45 + 22.5, .14, .62, 0, .34));
  els.push(abox([-.12, .22, -.44], [.12, .5, -.34], 'gu_gem'));
  return els;
}
const guardWisp = () => [...shapeSlab('g_wisp', 'gu_wisp', 'z', 0, {half: .05, cell: .08, inset: .5, edge: 'gu_wisp'}), ...shapeSlab('g_wisp', 'gu_wisp', 'x', 0, {half: .04, core: false})];
const guardOrb = () => [...orb([0, 0, 0], .2, 'gu_orb'), ...crossCards('gu_orb', [0, 0, 0], .6, .6, {y0: -.3})];

// ================================================================================================================
// 둥지 nesting: the pointed cap with the eye, two sepal wings (children of the cap)
// ================================================================================================================
function nestCap() {
  const els = [...loft('y', stops([.1, .26, .42, .58, .72, .86, .98, 1.12], [.3, .29, .25, .19, .13, .08, .045, .02]).map(s => ({...s, c: [0, -.04]})), {n: 16, tex: 'ne_cap', ledgeTex: 'ne_cap_l', caps: '-', seed: 11}),
    ...loft('y', stops([-.3, -.1, .12], [.17, .21, .22]).map(s => ({...s, c: [0, -.08]})), {n: 8, tex: 'ne_cap', ledgeTex: 'ne_cap_l', caps: '-', seed: 13})];
  els.push(...shapeSlab('w_ring', 'ne_ring', 'z', -.17, {half: .035, cell: .04, inset: .4}));
  els.push(...orb([0, 0, -.13], .12, 'ne_orb'));
  els.push(quad('ne_drop', [-.07, -.24, -.19], [.14, 0, 0], [0, -.22, 0]));
  for (let k = 0; k < 8; k++) els.push(radialCard('ne_thorn', k * 45 + 22.5, .24, .34, .02, .14));
  return els;
}
const nestWing = () => shapeSlab('w_wing', 'ne_wing', 'z', 0, {half: .03, cell: .05, inset: .5});

// ================================================================================================================
// 파괴 destruction: the armoured ball (open front), its glowing face + beak; the split husk
// ================================================================================================================
const BALL = {z: [-.44, -.3, -.08, .16, .36, .52, .6], R: .6};
function destrShell(husk) {
  const st = BALL.z.map(z => ({a: z, r: Math.sqrt(Math.max(.0025, BALL.R * BALL.R - z * z)) * (z === -.44 ? 1 : 1)}));
  if (husk) {
    // two half shells, split along x and pushed apart, the halves tipped open
    const half = side => loft('z', st, {n: 16, tex: 'de_shell', ledgeTex: 'de_shell_l', caps: '+', tint: true, skip: k => (side > 0 ? (k > 4 && k < 12) : (k < 4 || k > 12))});
    return [...shift(half(1), [.12, 0, 0]), ...shift(half(-1), [-.12, 0, 0])];
  }
  const els = [...loft('z', st, {n: 16, tex: 'de_shell', ledgeTex: 'de_shell_l', caps: '+', seed: 17}), ...annulus('z', [0, 0, 0], -.44, .3, .41, '-', 'de_rim', {n: 16, stagger: .002})];
  // 12 cone spikes on the axis-aligned and 45-degree directions (none on the open front)
  const S = (dir, rot) => spike('de_spike', dir.map(x => x * .5), dir, .3, .17, rot);
  els.push(...S([0, 1, 0]), ...S([0, -1, 0]), ...S([1, 0, 0]), ...S([-1, 0, 0]), ...S([0, 0, 1]));
  for (const [dir, rot] of [[[0, 1, 0], ['x', 45]], [[0, -1, 0], ['x', -45]], [[0, 1, 0], ['z', 45]], [[0, 1, 0], ['z', -45]], [[0, -1, 0], ['z', 45]], [[0, -1, 0], ['z', -45]], [[1, 0, 0], ['y', -45]], [[-1, 0, 0], ['y', 45]]])
    els.push(...S(dir, rot));
  return els;
}
function destrFace() {
  return [cardZ('de_face', -.33, {X0: -.33, X1: .33, Y0: -.33, Y1: .33}),
    ...loft('z', stops([-.33, -.45, -.58, -.72], [.12, .1, .06, .015]), {n: 8, tex: 'de_beak', caps: '+', seed: 19})];
}

// ================================================================================================================
// 포식성 predatory: body looks fish / fish_flare / bud / pod / face; the jaw bowl, the tail fin, the core (children)
// ================================================================================================================
const HOOD = {z: [-1.25, -.85, -.4, .1, .58, .95, 1.2], w: [.05, .32, .54, .6, .5, .24, .04], h: [.04, .24, .39, .44, .36, .18, .04]};
function predFish(flare) {
  const st = HOOD.z.map((a, i) => ({a, r: [HOOD.w[i], HOOD.h[i], HOOD.w[i], .07], c: [0, 0], box: .2}));
  const els = [...loft('z', st, {n: 16, tex: 'pr_hood', ledgeTex: 'pr_hood_l', caps: '-+', seed: 23})];
  for (const [z, big] of [[-.25, 1], [.22, 1], [.66, 0]]) {
    const y = big ? .4 : .3, sp = big ? 'pr_horn' : 'pr_hornS', H = big ? .67 : .36, W = big ? .4 : .24;
    els.push(quad(sp, [-W / 2, y + H - .05, z], [W, 0, 0], [0, -H, 0], {rot: ['x', 22.5, [0, y, z]]}), quad(sp, [0, y + H - .05, z - W / 2], [0, 0, W], [0, -H, 0], {rot: ['x', 22.5, [0, y, z]]}));
  }
  for (const s of [1, -1]) els.push(quad('pr_eye', [s * .5, .26, -.66], [0, 0, .22], [0, -.22, 0]));
  if (flare) {
    for (const [dir, rot] of [[[0, 1, 0]], [[1, 0, 0]], [[-1, 0, 0]], [[0, 1, 0], ['z', 45]], [[0, 1, 0], ['z', -45]], [[0, -1, 0], ['z', 45]], [[0, -1, 0], ['z', -45]]])
      for (const z of [-.55, -.1]) els.push(...spike('pr_flare', [dir[0] * .3, dir[1] * .25, z], dir, .55, .14, rot ? rot : undefined));
  }
  return els;
}
function predJaw() {
  // the translucent bowl under the hood (hinge frame: hinge at body z +0.4), two bottom sepals, the long front fin + gem
  const z0 = -.4, st = HOOD.z.map((a, i) => ({a: a + z0, r: [HOOD.w[i] * .93, .05, HOOD.w[i] * .93, HOOD.h[i] * 1.05], c: [0, 0], box: .3}));
  const els = [...loft('z', st, {n: 16, tex: 'pr_bowl', ledgeTex: 'pr_bowl_l', caps: '-+', seed: 29})];
  for (const s of [1, -1]) els.push(quad('pr_sepal', [s * .25 - .07, -.94, -.2 + z0], [.14, 0, 0], [0, .62, 0], {rot: ['z', s * 22.5, [s * .25, -.32, -.2 + z0]]}));
  els.push(quad('pr_fin', [.34, -.12, -.62 + z0], [.24, 0, 0], [0, 0, -1.15], {rot: ['y', -22.5, [.46, -.12, -.62 + z0]]}));
  els.push(abox([.38, -.2, -.72 + z0], [.56, -.04, -.56 + z0], 'pr_gem'));
  return els;
}
const predTail = () => [quad('pr_tail', [0, .5, -.04], [0, 0, .94], [0, -1.0, 0])];
const predCore = () => [...orb([0, 0, 0], .22, 'pr_core'), ...crossCards('pr_core', [0, 0, 0], .6, .6, {y0: -.3})];
function predBud() {
  const els = [];
  for (let k = 0; k < 8; k++) els.push(tangentCard('pr_petal', k * 45, .5, .78, .84, .78, {tilt: k % 2 ? 0 : 22.5, pivot: 'bottom'}));
  els.push(...shift(crossCards('pr_horn', [0, 0, 0], .4, .66, {y0: 0}), [0, .74, 0]));
  for (let k = 0; k < 8; k++) els.push(tangentCard('pr_sepal', k * 45 + 22.5, .42, .02, .5, .7));
  els.push(...crossCards('pr_hornS', [0, -.62, 0], .24, .36, {y0: -.36}));
  return els;
}
function predPod() {
  // a tall double-lobed clam (centre frame: the floor at y -1.3): the round lower lobe with the core opening at the
  // front, the scalloped translucent lid standing open behind
  const low = prof(-1.3, .3, 6, y => { const t = (y + 1.3) / 1.6; return .1 + .78 * Math.sin(Math.PI * Math.min(1, t * .95 + .03)) ** .7; });
  const els = [...loft('y', low, {n: 16, tex: 'pr_bowl', ledgeTex: 'pr_bowl_l', caps: '-', seed: 31, skip: (k, th, i) => i >= 2 && i <= 4 && k >= 3 && k <= 5})];
  els.push(quad('pr_podlid', [-.95, 2.1, .3], [1.9, 0, 0], [0, -1.8, 0], {rot: ['x', -22.5, [0, .3, .3]]}));
  els.push(quad('pr_podlid', [-.8, 1.9, .12], [1.6, 0, 0], [0, -1.6, 0], {rot: ['x', 22.5, [0, .3, .12]]}));
  return els;
}
function predFace() {
  const els = [...loft('z', prof(-.62, .5, 6, z => { const t = (z + .62) / 1.12; return .75 * Math.sin(Math.PI * Math.min(1, .15 + t * .85)) ** .5 + .02; }), {n: 16, tex: 'pr_face', ledgeTex: 'pr_face_l', caps: '-+', seed: 37})];
  els.push(...crossCards('pr_horn', [0, .66, -.1], .34, .6, {y0: 0}));
  els.push(abox([-.16, -.52, -.6], [.16, -.2, -.5], 'pr_gem', {rot: ['z', 45, [0, -.36, -.55]]}));
  els.push(quad('pr_eye', [-.08, .3, -.66], [.16, 0, 0], [0, -.16, 0]));
  return els;
}

// ================================================================================================================
// the Heart of the Oasis: lemon bulb (looks by tint), root cradle (pedestal / full), two root arms, glow tips, vine
// hand (idle / wrap) and four vine stem segments
// ================================================================================================================
const LEMON = {L: 1.6, W: 1.3, H: 1.15};
function heartBulb() {
  const z = [-1.6, -1.5, -1.33, -1.05, -.62, -.12, .4, .86, 1.2, 1.44, 1.6];
  const f = a => { const t = Math.abs(a) / LEMON.L; return Math.pow(Math.max(0, 1 - t * t), .62) * (1 - .55 * Math.pow(t, 6)) + .035; };
  const els = [...loft('z', z.map(a => ({a, r: [LEMON.W * f(a), LEMON.H * f(a), LEMON.W * f(a), LEMON.H * f(a)]})), {n: 16, tex: 'he_bulb', ledgeTex: 'he_bulb_l', caps: '-+', tint: true, seed: 41})];
  els.push(...tint([cardZ('he_swirl', 0, {X0: -.9, X1: .9, Y0: -.85, Y1: .85}), cardX('he_swirl', 0, {Z0: -1.1, Z1: 1.1, Y0: -.8, Y1: .8}), cardY('he_swirl', 0, {X0: -.9, X1: .9, Z0: -1.1, Z1: 1.1})]));
  return els;
}
function heartCradle(pedestal) {
  const els = [...loft('y', prof(0, .55, 4, y => 1.45 * Math.sqrt(Math.max(0, 1 - (y / .58) ** 2)) + .03), {n: 16, tex: 'he_root', ledgeTex: 'he_root_l', caps: '+', seed: 43})];
  for (const th of [22.5, 90, 157.5, 225, 292.5]) els.push(...radialSlab('h_root', 'he_rootc', th, {half: .13, cell: .1, inset: .5, edge: 'he_root'}));
  if (pedestal) {
    for (let k = 0; k < 6; k++) { const a = (k * 60 + 15) * D2R; els.push(...crossCards('he_petal', [Math.sin(a) * .9, .42, -Math.cos(a) * .9], .56, .34, {y0: 0})); }
    for (const a of [20, 140, 260]) els.push(...crossCards('he_sprout', [Math.sin(a * D2R) * .45, .5, -Math.cos(a * D2R) * .45], .24, .7, {y0: 0}));
  }
  return els;
}
const heartArms = () => [...radialSlab('h_arm', 'he_armc', 90, {half: .17, cell: .12, inset: .5, edge: 'he_root'}), ...radialSlab('h_arm', 'he_armc', 247.5, {half: .16, cell: .12, inset: .5, edge: 'he_root'})];
function heartTips() {
  const els = [];
  for (const [x, y, z, s] of [[.4, 4.25, .05, 1.1], [.08, 4.05, .1, .8], [-.45, 4.15, -.35, 1.05], [1.9, 2.55, .3, .7], [-.3, 1.5, -1.95, .75], [1.25, 1.6, 1.55, .7], [-1.75, 1.4, .55, .7], [.2, 1.45, 1.9, .65]])
    els.push(...crossCards('he_tip', [x, y, z], .32 * s, .62 * s, {y0: 0}));
  return els;
}
function vineHand(wrap) {
  const els = [abox([-.12, -.1, -.12], [.12, .16, .12], 'he_root')];
  const s = wrap ? 1.25 : 1.0;
  for (const [th, k] of [[0, 1], [67.5, .9], [112.5, 1], [180, .85], [247.5, .95], [292.5, 1]]) {
    const [b, g] = baseAz(th), d = unitAz(b), tg = tanAz(b);
    const L = 1.1 * k * s, w = 1.0 * (wrap ? .7 : 1);
    els.push(quad('he_tendril', [d[0] * .05 - tg[0] * w / 2, .1, d[2] * .05 - tg[2] * w / 2], [tg[0] * w, 0, tg[2] * w], [0, -L * 1.1, 0], {rot: g ? ['y', g, [0, 0, 0]] : undefined}));
  }
  return els;
}
const vineStem = () => [quad('he_stem', [-.3, .1, 0], [.6, 0, 0], [0, -6.3, 0]), quad('he_stem', [0, .1, -.3], [0, 0, .6], [0, -6.3, 0]), abox([-.07, -6.2, -.07], [.07, .05, .07], 'he_root')];

// ================================================================================================================
// domes, wall blade, stalks, seed
// ================================================================================================================
const DOME = [[0, 1.1, 4.42], [1.1, 2.1, 4.02], [2.1, 3.0, 3.3], [3.0, 3.7, 2.36], [3.7, 4.22, 1.3]];
function domeShell() {
  const els = [];
  for (const [y0, y1, r] of DOME) els.push(...band([0, 0, 0], r, y0, y1, 'do_shell'));
  for (let i = 0; i < DOME.length - 1; i++) els.push(...annulus('y', [0, 0, 0], DOME[i][1], DOME[i + 1][2] - .01, DOME[i][2], '+-', 'do_shell', {n: 16, stagger: .003}));
  els.push(...annulus('y', [0, 0, 0], 4.22, 0, 1.3, '+-', 'do_shell', {n: 8, stagger: .003}));
  return els;
}
function domeDecor() {
  const els = [];
  for (const [y0, y1, r] of DOME.slice(0, 3)) els.push(...band([0, 0, 0], r - .05, y0, y1, 'do_vine'));
  els.push(...band([0, 0, 0], 4.47, 0, .32, 'do_rim'));
  els.push(...crossCards('do_sprout', [0, 4.2, 0], .6, .7, {y0: 0}));
  return els;
}
function wallBlade() {
  // a slightly cupped blade: three strips (the side ones turned 22.5 degrees), the midrib as a thin box
  const R = SH.wa_blade.rect, W = R.u1 - R.u0, H = R.v1 - R.v0, w3 = W / 3;
  return [quad('wa_blade', [-w3 / 2, H, 0], [w3, 0, 0], [0, -H, 0], {uvr: [1 / 3, 0, 2 / 3, 1]}),
    quad('wa_blade', [w3 / 2, H, 0], [w3, 0, 0], [0, -H, 0], {uvr: [2 / 3, 0, 1, 1], rot: ['y', -22.5, [w3 / 2, 0, 0]]}),
    quad('wa_blade', [-w3 * 1.5, H, 0], [w3, 0, 0], [0, -H, 0], {uvr: [0, 0, 1 / 3, 1], rot: ['y', 22.5, [-w3 / 2, 0, 0]]})];
}
const stalkLow = () => loft('y', stops([-.4, .3, 1.0, 1.7, 2.3, 2.7], [.56, .5, .46, .43, .41, .4]), {n: 16, tex: 'st_bark', ledgeTex: 'st_bark_l', caps: '-+', seed: 47});
const stalkHigh = () => loft('y', stops([-.05, .6, 1.2, 1.7, 2.1], [.4, .38, .35, .31, .28]), {n: 16, tex: 'st_bark', ledgeTex: 'st_bark_l', caps: '-+', seed: 53});
const stalkTip = () => [...shapeSlab('s_hook', 'st_hook', 'x', 0, {half: .17, cell: .1, inset: .5, edge: 'st_bark'}), ...spike('st_cone', [0, 1.3, -.3], [0, 1, 0], .3, .16, ['x', 45])];
const seedModel = () => [...crossCards('se_seed', [0, .17, 0], .26, .34, {y0: -.17, three: true}), quad('se_seed', [-.13, .02, .17], [.26, 0, 0], [0, 0, -.34])];

// ================================================================================================================
// the structure
// ================================================================================================================
// display: {name, scale, pivot, joint [x,y,z] (rest, in the parent frame), parent, frame ('object' | 'joint'), bright,
//   looks {look: item}, def, overlay, models {model: () => elements}, cull [w, h] (fixed objects), note}
const D = (name, o) => ({name, parent: null, frame: 'joint', overlay: false, bright: 14, scale: 1, pivot: 'feet', joint: [0, 0, 0], ...o});
export const ORG = {
  basic: {type: 'kind', id: 1, name: '기본', hover: 0, hp_bar_y: 1.6, shield: {w: 1.2, h: 1.6}, size: {h: 1.15, h_stem: 1.35, d: 0.9, bag: [1.43, 1.31]},
    displays: [
      D('bulb', {pivot: 'feet', frame: 'object', looks: {bell: 'basic_bulb_bell', bag: 'basic_bulb_bag', buffed: 'basic_bulb_buffed', bag_buffed: 'basic_bulb_bag_buffed', dying: 'basic_bulb_dying', bag_dying: 'basic_bulb_bag_dying'}, def: 'bell',
        // a clip's look switch keeps the bulb's variant: {to: {from: alt}} (bell -> bag keeps the buff; dying keeps the form)
        variants: {bag: {buffed: 'bag_buffed'}, dying: {bag: 'bag_dying', bag_buffed: 'bag_dying'}},
        models: {basic_bulb_m_bell: bellModel, basic_bulb_m_bag: bagModel},
        items: {basic_bulb_bell: ['basic_bulb_m_bell', 0xEFEEE8], basic_bulb_buffed: ['basic_bulb_m_bell', 0xF4FFE0], basic_bulb_dying: ['basic_bulb_m_bell', 0x8E8A76],
          basic_bulb_bag: ['basic_bulb_m_bag', 0xEFEEE8], basic_bulb_bag_buffed: ['basic_bulb_m_bag', 0xF4FFE0], basic_bulb_bag_dying: ['basic_bulb_m_bag', 0x8E8A76]}}),
      D('crown', {pivot: 'centre', joint: [0, .69, -.53], looks: {closed: 'basic_crown_closed', open: 'basic_crown_open'}, def: 'closed',
        models: {basic_crown_closed: () => crownModel(false), basic_crown_open: () => crownModel(true)}, note: 'the petal crown at the bag neck (scale 0 while a bell); the glow is painted emissive'}),
      D('shield', {pivot: 'feet', frame: 'object', overlay: true, scale: 1.15, looks: {on: 'basic_shield_on'}, def: 'on', models: {basic_shield_on: shieldModel},
        note: '3 cutout vesica panes 0.62 x 1.42 + a low-alpha bubble rim band + a yellow 3-leaf crown; only while shielded (om/basic/shield/on|off)'}),
    ]},
  nurt: {type: 'kind', id: 2, name: '양육', hover: 0, hp_bar_y: 2.8, shield: {w: 1.4, h: 2.6}, size: {h: 2.4},
    displays: [
      D('stalk', {pivot: 'feet', frame: 'object', scale: 1.6, looks: {idle: 'nurt_stalk_idle'}, def: 'idle', models: {nurt_stalk_idle: nurtStalk}, note: 'S-curved dark-teal ribbon with pale rims, fronds, the gold shard'}),
      D('cap', {pivot: 'centre', joint: [0, 2.18, .06], looks: {idle: 'nurt_cap_idle', tilt: 'nurt_cap_tilt'}, def: 'idle', models: {nurt_cap_idle: () => nurtCap(false), nurt_cap_tilt: () => nurtCap(true)}, note: 'cream hood-leaf; tilt = the hood lifted open'}),
      D('orb', {pivot: 'centre', joint: [0, 2.06, -.4], bright: 15, looks: {on: 'nurt_orb_on'}, def: 'on', models: {nurt_orb_on: nurtOrb}, note: 'pulse'}),
      D('ring', {pivot: 'feet', frame: 'object', overlay: true, looks: {on: 'nurt_ring_on'}, def: 'on', models: {nurt_ring_on: nurtRing}, note: 'translucent cylinder r 1.3, h 0.5, only while immune (om/nurt/ring/on|off)'}),
    ]},
  guard: {type: 'kind', id: 3, name: '수호', hover: 0, hp_bar_y: 3.0, shield: {w: 1.4, h: 3.0}, size: {h: 4.4, bud: 2.0, orb_d: 0.4},
    displays: [
      D('spire', {pivot: 'mid', frame: 'object', scale: 1.6, joint: [0, 2.2, 0], looks: {spire: 'guard_spire_spire', bud: 'guard_spire_bud', wisp: 'guard_spire_wisp'}, def: 'spire',
        models: {guard_spire_spire: guardSpire, guard_spire_bud: guardBud, guard_spire_wisp: guardWisp}}),
      D('orb', {pivot: 'mid', joint: [0, 5.05, 0], bright: 15, looks: {on: 'guard_orb_on'}, def: 'on', models: {guard_orb_on: guardOrb}, note: 'bobs 0.6-0.8 above the tip'}),
    ]},
  nest: {type: 'kind', id: 4, name: '둥지', hover: 1.0, hp_bar_y: 2.75, shield: {w: 1.6, h: 2.2}, size: {w: 2.2, h: 1.3},
    displays: [
      D('cap', {pivot: 'centre', joint: [0, 1.3, 0], looks: {idle: 'nest_cap_idle'}, def: 'idle', models: {nest_cap_idle: nestCap}, note: 'cap + the orb eye (painted emissive)'}),
      D('wing_l', {pivot: 'centre', parent: 'cap', joint: [.17, .02, .02], looks: {idle: 'nest_wing_l_idle'}, def: 'idle', models: {nest_wing_l_idle: nestWing}}),
      D('wing_r', {pivot: 'centre', parent: 'cap', joint: [-.17, .02, .02], looks: {idle: 'nest_wing_r_idle'}, def: 'idle', models: {nest_wing_r_idle: () => mirrorX(nestWing())}}),
    ]},
  destr: {type: 'kind', id: 5, name: '파괴', hover: 0, hp_bar_y: 1.75, shield: {w: 1.3, h: 1.3}, size: {d: 1.2, spikes: 0.2, beak: 0.4},
    displays: [
      D('shell', {pivot: 'centre', joint: [0, .62, 0], spinAxis: 'x', looks: {normal: 'destr_shell_normal', husk: 'destr_shell_husk'}, def: 'normal',
        models: {destr_shell_normal: () => destrShell(false), destr_shell_m_husk: () => destrShell(true)}, items: {destr_shell_husk: ['destr_shell_m_husk', 0x3A3833]}}),
      D('face', {pivot: 'centre', joint: [0, .62, 0], spinAxis: 'x', bright: 15, looks: {on: 'destr_face_on'}, def: 'on', models: {destr_face_on: destrFace}, note: 'pulse scale'}),
    ]},
  pred: {type: 'kind', id: 6, name: '포식성', hover: 1.2, hp_bar_y: 2.75, shield: {w: 1.6, h: 1.6}, size: {fish: [2.5, 1.3], bud: [2.1, 1.6], pod: [3.5, 1.8]},
    displays: [
      D('body', {pivot: 'centre', joint: [0, 1.3, 0], scale: 1.6, looks: {fish: 'pred_body_fish', fish_flare: 'pred_body_fish_flare', bud: 'pred_body_bud', pod: 'pred_body_pod', face: 'pred_body_face'}, def: 'fish',
        models: {pred_body_fish: () => predFish(false), pred_body_fish_flare: () => predFish(true), pred_body_bud: predBud, pred_body_pod: predPod, pred_body_face: predFace},
        note: 'fish = the leaf-shark hood; bud / pod / face are their own models (jaw and fin hidden)'}),
      D('jaw', {pivot: 'centre', parent: 'body', joint: [0, -.02, .4], scale: 1.6, looks: {idle: 'pred_jaw_idle'}, def: 'idle', models: {pred_jaw_idle: predJaw}, note: 'the translucent bowl, sepals and the long front fin; hinge behind the middle'}),
      D('fin', {pivot: 'centre', parent: 'body', joint: [0, .02, 1.12], looks: {idle: 'pred_fin_idle'}, def: 'idle', models: {pred_fin_idle: predTail}, note: 'the tail fin; yaw +-25 in pred_swim'}),
      D('core', {pivot: 'centre', parent: 'body', joint: [0, -.08, -.2], bright: 15, looks: {on: 'pred_core_on'}, def: 'on', models: {pred_core_on: predCore}}),
    ]},
  heart: {type: 'object', kind: 'single', tag: 'rlk_mb_ap_heart', cull: [9, 30],
    displays: [
      D('heart_bulb', {idx: 0x00, pivot: 'centre', joint: [0, 1.6, 0], scale: 1.2, bright: 15, looks: {idle: 'heart_bulb_idle', egg_gold: 'heart_bulb_egg_gold', egg_green: 'heart_bulb_egg_green', withered: 'heart_bulb_withered', blaze: 'heart_bulb_blaze'}, def: 'idle',
        models: {heart_bulb_m: heartBulb}, items: {heart_bulb_idle: ['heart_bulb_m', 0xEDF08A], heart_bulb_egg_gold: ['heart_bulb_m', 0xF8D862], heart_bulb_egg_green: ['heart_bulb_m', 0xB4DA64],
          heart_bulb_withered: ['heart_bulb_m', 0x8A8258], heart_bulb_blaze: ['heart_bulb_m', 0xFFFCD8]},
        note: 'translucent lemon seed 3.2 x 2.6 x 2.3, alpha ~0.86; the arrival egg = this model at scale 0.7, pitch 90 (upright)'}),
      D('heart_cradle', {idx: 0x01, pivot: 'mid', frame: 'object', joint: [0, .9, 0], scale: 2.2, looks: {pedestal: 'heart_cradle_pedestal', full: 'heart_cradle_full'}, def: 'pedestal',
        models: {heart_cradle_pedestal: () => heartCradle(true), heart_cradle_full: () => heartCradle(false)}, note: '5 knobbly root fingers + the mound; pedestal adds pale petal clumps + 3 gold sprouts'}),
      D('heart_arms', {idx: 0x02, pivot: 'mid', frame: 'object', joint: [0, 2.1, 0], scale: 2.2, looks: {idle: 'heart_arms_idle'}, def: 'idle', models: {heart_arms_idle: heartArms}, note: 'two root arms curling over the bulb to 4.0-4.3 b'}),
      D('heart_tips', {idx: 0x03, pivot: 'mid', frame: 'object', joint: [0, 2.1, 0], scale: 2.2, bright: 15, looks: {idle: 'heart_tips_idle'}, def: 'idle', models: {heart_tips_idle: heartTips}, note: 'leaf-flame sprouts, swaying'}),
      D('vine_hand', {idx: 0x04, pivot: 'centre', joint: [0, 11.2, 0], looks: {idle: 'vine_hand_idle', wrap: 'vine_hand_wrap'}, def: 'idle', models: {vine_hand_idle: () => vineHand(false), vine_hand_wrap: () => vineHand(true)}}),
      ...[0, 1, 2, 3].map(k => D('vine_stem_' + k, {idx: 0x05 + k, pivot: 'centre', joint: [0, 26, 0], scale: 4.4, looks: {idle: 'heart_vine_stem'}, def: 'idle', models: k ? {} : {heart_vine_stem: vineStem}, note: 'stretched along its length between the canopy rim and the hand'})),
    ]},
  dome: {type: 'object', kind: 'fixed_set', count: 3, radius: 4.5, tag: 'rlk_mb_ap_dome', cull: [10, 5],
    displays: [
      D('dome_shell', {idxs: [0x10, 0x12, 0x14], pivot: 'feet', frame: 'object', scale: 3.3, looks: {idle: 'dome_shell_idle'}, def: 'idle', models: {dome_shell_idle: domeShell}, note: 'two-sided shell, alpha <= 0.35'}),
      D('dome_decor', {idxs: [0x11, 0x13, 0x15], pivot: 'feet', frame: 'object', scale: 3.3, looks: {idle: 'dome_decor_idle'}, def: 'idle', models: {dome_decor_idle: domeDecor}, note: 'cutout vine band, bright base rim, sprout on top'}),
    ]},
  wall: {type: 'object', kind: 'multi', max: 15, tag: 'rlk_mb_ap_wall', cull: [2, 3.2], blocks: {block: 'minecraft:barrier', y: [201, 202], place: 'replace air'},
    displays: [D('wall_blade', {pivot: 'feet', frame: 'object', scale: 2.0, looks: {idle: 'wall_blade_idle'}, def: 'idle', models: {wall_blade_idle: wallBlade}, note: 'translucent yellow-green blade 0.9 x 2.86, midrib, two windows'})]},
  stalk: {type: 'object', kind: 'fixed_set', count: 4, height: [5.5, 6.0], tag: 'rlk_mb_ap_stalk', cull: [14, 7],
    displays: [
      D('stalk_low', {idxs: [0x20, 0x23, 0x26, 0x29], pivot: 'feet', joint: [0, 0, 0], scale: 1.9, bright: 13, looks: {idle: 'stalk_low_idle'}, def: 'idle', models: {stalk_low_idle: stalkLow}}),
      D('stalk_high', {idxs: [0x21, 0x24, 0x27, 0x2A], pivot: 'feet', parent: 'stalk_low', joint: [0, 2.62, 0], scale: 1.5, bright: 13, looks: {idle: 'stalk_high_idle'}, def: 'idle', models: {stalk_high_idle: stalkHigh}}),
      D('stalk_tip', {idxs: [0x22, 0x25, 0x28, 0x2B], pivot: 'feet', parent: 'stalk_high', joint: [0, 2.02, 0], scale: 1.1, looks: {idle: 'stalk_tip_idle'}, def: 'idle', models: {stalk_tip_idle: stalkTip}, note: 'hooked tip + small gold cone'}),
    ]},
  seed: {type: 'object', kind: 'single', tag: 'rlk_mb_ap_seed', cull: [1, 1],
    displays: [D('seed', {idx: 0x30, pivot: 'feet', bright: 15, looks: {idle: 'seed_idle'}, def: 'idle', models: {seed_idle: seedModel}, note: 'glowing golden seed at the death spot'})]},
};
export const KINDS = Object.keys(ORG).filter(k => ORG[k].type === 'kind');
export const OBJECTS = Object.keys(ORG).filter(k => ORG[k].type === 'object');
// rest world position of a display's joint (object frame), parents first
export function restJoint(owner, name) {
  const d = ORG[owner].displays.find(x => x.name === name);
  const p = d.parent ? restJoint(owner, d.parent) : [0, 0, 0];
  return p.map((v, i) => v + d.joint[i]);
}
// every model (block geometry converted to model units for its display's scale): {model: {els, owner, display}}
export function allModels() {
  const out = {};
  for (const [owner, o] of Object.entries(ORG)) for (const d of o.displays) for (const [m, build] of Object.entries(d.models || {})) {
    let els = build();
    if (d.frame === 'object') els = shift(els, restJoint(owner, d.name).map(v => -v));
    out[m] = {els: toUnits(els, d.scale), owner, display: d.name};
  }
  return out;
}
// item definitions: {item: {model, tint (int | null), owner, display, look}}; untinted looks point at their own model
export function allItems() {
  const out = {};
  for (const [owner, o] of Object.entries(ORG)) for (const d of o.displays) for (const [look, item] of Object.entries(d.looks)) {
    if (out[item]) continue;
    const t = d.items && d.items[item];
    out[item] = {model: t ? t[0] : item, tint: t ? t[1] : null, owner, display: d.name, look};
  }
  return out;
}
