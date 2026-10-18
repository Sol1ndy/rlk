// BODY region of the 야타용왕 (Azhdaha) rig: torso (chest, belly, pelvis), the neck, the chest apron (+ its glow
// overlay), the four dorsal plate groups and the three gold crystal groups (model.md §3.2-§3.6).
//
// Region interface (the same in azhdaha_{head,body,legs,tail}.mjs; aggregated by azhdaha_geometry / azhdaha_paint):
//   PARTS      [part, default item model, block brightness] owned by this region (pose: azhdaha_pose.mjs solve())
//   models()   {model: elements (model units)}: the default models, every look variant, the overlays
//   sprites()  {sprite: [w, h, painter (s, t in 0..1) -> rgba, translucent]}: this region's own sprites
//   LOOKS      {legs|tail: {part: {look: item model}}}: the element looks this region answers (model.md §4.2)
//   TINTED     {item: [model, rgb]}: extra item definitions = a model with a constant tint (glow overlays)
// Geometry is authored in blocks in each part's frame (its joint at the origin, the rest skeleton of
// azhdaha_pose.mjs J) and converted with toUnits(els, PART_SCALE[part]).
import {loft, slab, crossCards, rockBox, toUnits, retex, stroke, sdPoly, registerTile, hash} from './azhdaha_shape.mjs';
import {PART_SCALE, J, PLATE_LEAN} from './azhdaha_pose.mjs';
import {q, rot} from './mboss_rig_math.mjs';
import {cardX, cardZ, abox} from './mboss_model_lib.mjs';
import {PAL, LOOK_PAL, C, clamp, smooth, mix, lift, sink, N, creamPx, platePx, goldPx, spriteSize, onRect, TRANSPARENT, bevelLight} from './azhdaha_materials.mjs';

export const REGION = 'body';
export const PARTS = [
  ['chest', 'chest', 13], ['belly', 'belly', 13], ['pelvis', 'pelvis', 13], ['neck1', 'neck1', 13], ['neck2', 'neck2', 13],
  ['apron', 'apron', 13], ['glow_apron', 'empty', 15],
  ['plates_neck', 'plates_neck', 13], ['plates_sh', 'plates_sh', 13], ['plates_mid', 'plates_mid', 13], ['plates_hip', 'plates_hip', 13],
  ['crys_sh', 'crys_sh', 14], ['crys_mid', 'crys_mid', 14], ['crys_hip', 'crys_hip', 14],
];
const rel = (bone, p) => [p[0] - J[bone][0], p[1] - J[bone][1], p[2] - J[bone][2]];
const U = (part, els) => toUnits(els, PART_SCALE[part]);
const down = th => Math.sin(th * Math.PI / 180) < -.55;
const up = th => Math.sin(th * Math.PI / 180) > .3;

// ---- torso ---------------------------------------------------------------------------------------------------------------
// Stations in WORLD z / y (rest), converted to the bone frame: [z, half width, top y, bottom y, box]
const st = (bone, rows) => rows.map(([z, w, top, bot, box = .25]) => {
  const c = J[bone], cy = (top + bot) / 2 - c[1], h = (top - bot) / 2;
  return {a: z - c[2], r: [w, h, w, h], c: [0, cy], box};
});
// the belly sprite fits each underside facet across (one rib per facet)
for (const n of ['belly', 'belly_hydro', 'belly_pyro']) registerTile(n, 64, 128, 32, {fitU: true});
const torsoTex = (belly, top) => (k, th) => (down(th) ? belly : up(th) ? top : 'hide');
function chest(belly = 'hide_dk') {
  return loft('z', st('chest', [[-3.35, 1.45, 3.25, 1.95, .2], [-2.9, 2.2, 3.85, 1.65], [-2.2, 2.65, 4.25, 1.5], [-1.4, 2.85, 4.35, 1.45],
    [-.6, 2.9, 4.3, 1.42], [.1, 2.95, 4.2, 1.4]]), {tex: torsoTex(belly, 'hide_lg'), caps: '-', seed: 11});
}
function belly(look = '') {
  const b = 'belly' + (look ? '_' + look : '');
  return [...loft('z', st('spine1', [[-1.2, 2.95, 4.2, 1.42], [-.4, 3.05, 4.15, 1.38], [.5, 3.0, 4.05, 1.4], [1.3, 2.9, 3.95, 1.45], [2.0, 2.75, 3.85, 1.55]]),
    {tex: torsoTex(b, 'hide'), seed: 23})];
}
function pelvis() {
  return loft('z', st('pelvis', [[1.2, 2.8, 3.95, 1.5], [2.0, 2.7, 3.75, 1.65], [2.9, 2.45, 3.6, 1.85], [3.8, 2.05, 3.45, 2.0], [4.6, 1.55, 3.3, 2.15], [5.2, .95, 3.15, 2.3, .1], [5.5, .45, 3.0, 2.45, 0]]),
    {tex: torsoTex('hide_dk', 'hide_lg'), caps: '+', seed: 37});
}
// neck: two lofts sloping down to the head (world stations), the ruff covers the top
function neck1() {
  return loft('z', st('neck1', [[-1.85, 1.6, 4.1, 2.1], [-2.3, 1.55, 3.9, 1.95], [-2.8, 1.45, 3.55, 1.85], [-3.2, 1.35, 3.25, 1.75]]), {tex: (k, th) => (down(th) ? 'hide_dk' : 'hide'), seed: 41});
}
function neck2() {
  return loft('z', st('neck2', [[-2.75, 1.4, 3.45, 1.7], [-3.1, 1.3, 3.2, 1.55], [-3.45, 1.15, 2.95, 1.4], [-3.75, 1.0, 2.75, 1.3]]), {tex: (k, th) => (down(th) ? 'hide_dk' : 'hide'), seed: 43, caps: '+'});
}

// ---- apron (model.md §3.2): a convex cream shield between the fore legs, lobed pebble hem, gold drop spike --------------
// plane z, u = X, v = Y (apron frame: the throat pivot J.apron; top -0.05 .. hem -1.8)
const AP = {u0: -1.05, u1: 1.05, v0: -1.95, v1: 0};
const apronHem = u => -1.62 - .1 * Math.cos(u * Math.PI / .52) ** 2 + .12 * (Math.abs(u) / 1.05) ** 2;   // 4 lobes
const apronSd = (u, v) => Math.max(Math.abs(u) - (1.0 - .08 * (-v / 1.8)), v - (-.02), apronHem(u) - v);
const APRON_CUT = [[-1.05, -.36], [-.36, .36], [.36, 1.05]];
function apronEls(sprite, {tint = false, glow = false} = {}) {
  const els = [];
  // centre panel forward, the side panels turned back 22.5 degrees round the panel edges (convex)
  const z0 = -.34;
  els.push(...slab({plane: 'z', at: z0, rect: AP, sd: apronSd, half: .1, sprite, edge: 'cream', cell: .12, clip: {u0: -.36, u1: .36}, core: !glow, cards: glow ? '-' : 'both', tint, eps: glow ? .03 : .012}));
  for (const s of [1, -1]) {
    const piv = [s * .36, -1, z0];
    els.push(...slab({plane: 'z', at: z0, rect: AP, sd: apronSd, half: .1, sprite, edge: 'cream', cell: .12, clip: s > 0 ? {u0: .36} : {u1: -.36},
      core: !glow, cards: glow ? '-' : 'both', tint, eps: glow ? .03 : .012, rot: ['y', s * 22.5, piv]}));
  }
  if (!glow) {
    // the gold drop spike under the hem centre and the pebble bumps along the hem (small cream knobs)
    els.push(rockBox([-.08, -1.92, z0 - .1], [.08, -1.66, z0 + .06], 'gold'), rockBox([-.045, -2.1, z0 - .06], [.045, -1.9, z0 + .02], 'gold'));
    for (let i = -3; i <= 3; i++) { const u = i * .27, v = apronHem(u); els.push(rockBox([u - .1, v - .02, z0 - .16], [u + .1, v + .16, z0 + .12], 'cream', {seed: i})); }
  }
  return els;
}
// glyph engraving of the apron (and its glow mask): vertical zigzag bands + square meander hooks (model.md §3.2)
function apronLine(u, v) {
  const a = Math.abs(u);
  // two vertical zigzags either side of the centre
  const zz = Math.abs(a - (.42 + .08 * Math.abs(((v * 3.2) % 1 + 1) % 1 - .5) * 4 - .08));
  let d = zz;
  // central spine line with a diamond near the top
  d = Math.min(d, Math.abs(u) + (v < -.35 && v > -1.4 ? 0 : 9));
  const dm = Math.abs(Math.abs(u) + Math.abs(v + .55) - .2);
  d = Math.min(d, dm);
  // square meander hooks on the side panels
  const hu = a - .78, hv = v + 1.0;
  const sq = Math.max(Math.abs(hu), Math.abs(hv));
  if (sq < .2) d = Math.min(d, Math.abs(sq - .17), Math.abs(sq - .1) + (hv > 0 && hu < 0 ? 9 : 0));
  return d;
}
function apronPaint(look) {
  const L = look ? LOOK_PAL[look] : null;
  return (u, v) => {
    const s = apronSd(u, v);
    if (s > 0) return null;
    let c = creamPx(u * 64 + 40, v * 64 + 40);
    c = mix(c, PAL.cream(.55), .3 * smooth(.5, 1.05, Math.abs(u)));       // the sides curve away
    if (s > -.05) c = sink(c, .35);
    const d = apronLine(u, v);
    if (d < .022) c = L ? L.glow(.15 + d / .022 * .5) : mix(c, PAL.groove(.5), .85);
    else if (L && d < .06) c = mix(c, L.glow(.6), .35 * (1 - d / .06));
    if (v < apronHem(u) + .14) c = mix(c, PAL.cream(.1), .3 * N.a(u * 9, v * 9));   // pebbly hem
    return c;
  };
}
const apronMask = (u, v) => { if (apronSd(u, v) > 0) return null; const d = apronLine(u, v); return d < .03 ? [255, 255, 255, 255] : d < .055 ? [255, 255, 255, Math.round(255 * (1 - (d - .03) / .025))] : null; };

// ---- dorsal plates (model.md §3.5) ---------------------------------------------------------------------------------------------
// Each plate is a crossed pair of painted cards: a side card (its profile, plane x) and a front card (its face, plane z),
// both turned out about Z by the plate's splay, so the fan reads from the side, the front and above. The group part
// leans every plate back (azhdaha_pose.mjs PLATE_LEAN); plates are authored upright in the group frame, their bases
// placed from world (rest) positions on the hide through the inverse lean.
// Sheet: 8 cells of 64 x 96 (aspect 2:3): 0-4 side profiles (upright, the tip curling back), 5-7 front faces.
const BLADES = [
  {kind: 's', tip: .14, w: .27}, {kind: 's', tip: .22, w: .25, orange: true}, {kind: 's', tip: .1, w: .32}, {kind: 's', tip: .24, w: .28, notch: true},
  {kind: 's', tip: .32, w: .34}, {kind: 'f', w: .34}, {kind: 'f', w: .28, orange: true}, {kind: 'f', w: .4},
];
const SHEET = {cw: 64, ch: 96, n: BLADES.length};
const AS = 2 / 3;   // cell aspect (width / height)
// half-width profile: a dagger / feather, widest at 40-45 % of the length, a long straight taper to the point
const bladeW = (b, t) => (b.kind === 'f' ? (t < .35 ? .55 + .45 * t / .35 : (1 - t) / .65) : 1.25 * (t < .42 ? .5 + .5 * t / .42 : Math.pow((1 - t) / .58, .9)));
const BL = BLADES.map(b => {
  // centre line in physical-normalized coords (x * AS, y): side blades rise from (.36, 0), curling back only in the
  // top third; front blades are symmetric about x .5
  const x0 = b.kind === 'f' ? .5 : .36;
  const top = b.kind === 'f' ? .8 : 1;   // front faces end at 80 % of the cell (their card shows the lower 80 %)
  const pts = Array.from({length: 17}, (_, i) => { const t = i / 16; return [(x0 + (b.tip || 0) * smooth(.55, 1, t) * t) * AS, t * top]; });
  const S = stroke(pts, t => b.w * AS * bladeW(b, t));
  return {...b, S, sd: (x, y) => { let d = S.sd(x * AS, y); if (b.notch) { const n = Math.hypot((x - .58) * AS, y - .6); d = Math.max(d, -(n - .04)); } return d; }};
});
function bladeColour(b, x, y, look) {
  const d = b.sd(x, y);
  if (d > 0) return null;
  const n = b.S.near(x * AS, y), across = Math.abs(n.s) / Math.max(1e-3, b.w * AS * bladeW(b, n.t));
  const R = look ? LOOK_PAL[look].stone : PAL.plate;
  let c = platePx(x * 60, y * 90, R);
  // a central ridge: one half lit, the other shaded (the blade is a shallow V); feather-like grain toward the tip
  c = n.s > 0 ? mix(c, R(.18), .4 * (1 - across)) : mix(c, R(.72), .35 * (1 - across));
  if (across < .06) c = mix(c, R(.1), .55);
  if (Math.abs(((n.t * 9 + across * 1.4) % 1) - .5) < .05 && across > .3) c = mix(c, R(.85), .25);
  if (b.orange && y < .42) c = mix(c, PAL.plateOr(.15 + 1.5 * y), smooth(.42, .12, y));
  if (d > -.014) c = look ? LOOK_PAL[look].glow(.15) : mix(c, PAL.plate(.0), .55);     // rim: greyish highlight / element glow
  else if (d > -.035 && look) c = mix(c, LOOK_PAL[look].glow(.45), .55);
  if (look && across < .05 && n.t > .25) c = mix(c, LOOK_PAL[look].glow(.3), .6);      // a glint streak on the ridge
  return c;
}
const plateSheet = look => (s, t) => { const k = Math.min(SHEET.n - 1, Math.floor(s * SHEET.n)); return bladeColour(BL[k], s * SHEET.n - k, 1 - t, look) || TRANSPARENT; };
const cellUV = (els, spr, k, n) => {
  for (const e of els) for (const f of Object.values(e.faces)) if (f.texture === '#' + spr) { const [a, b, c2, d] = f.uv; f.uv = [(k + a / 16) * 16 / n, b, (k + c2 / 16) * 16 / n, d].map(v => +v.toFixed(4)); }
  return els;
};
// One plate in its group frame: base [x, y, z], length L, side / front cells, splay (deg about Z; - tips toward +X).
function plate(spr, [x, y, z], L, ks, kf, splay = 0, wf = 1) {
  const W = L * AS, Wf = L * AS * .82 * wf, rot = splay ? ['z', splay, [x, y, z]] : undefined;
  const side = cardX(spr, x, {Z0: z - .36 * W, Z1: z + .64 * W, Y0: y, Y1: y + L}, {rot});
  const front = cardZ(spr, z, {X0: x - Wf / 2, X1: x + Wf / 2, Y0: y, Y1: y + L * .8}, {rot, uvr: [0, .2, 1, 1]});
  // the front card shows only the lower 80 % of its cell (the side profile curls back above that)
  cellUV([side], spr, ks, SHEET.n); cellUV([front], spr, kf, SHEET.n);
  const core = abox([x - .05, y, z - .05], [x + .05, y + L * .55, z + .05], spr === 'plates' ? 'plate' : spr.replace('plates', 'plate'), {rot});
  return [side, front, core];
}
// Plate layout per group in WORLD coordinates (rest): [x, base y, z, L, side cell, front cell, splay]; x > 0 entries
// are mirrored. Bases sit about 0.3 b inside the hide.
const G = {
  neck: {base: 'plN', g: 'neck', list: [[0, 3.05, -2.95, 2.4, 0, 5, 0], [.55, 3.00, -2.9, 2.4, 3, 7, -22.5], [1.05, 2.75, -2.75, 2.2, 4, 5, -45], [1.45, 2.35, -2.6, 1.9, 2, 7, -45],
    [1.7, 1.90, -2.5, 1.5, 4, 5, -45], [.3, 3.15, -2.45, 2.0, 2, 6, -22.5]]},
  sh: {base: 'plS', g: 'sh', list: [[0, 4.10, -1.5, 2.95, 0, 5, 0], [0, 4.00, -2.35, 2.3, 2, 7, 0], [.75, 4.05, -1.85, 2.8, 1, 6, -22.5], [.8, 4.00, -.95, 2.5, 3, 5, -22.5],
    [1.6, 3.70, -1.5, 2.6, 4, 7, -45], [1.7, 3.55, -.6, 2.0, 2, 5, -45], [2.25, 3.15, -1.05, 1.8, 0, 6, -45]]},
  mid: {base: 'plM', g: 'mid', list: [[0, 4.05, 1.0, 2.75, 1, 6, 0], [0, 4.10, .1, 2.4, 2, 5, 0], [.75, 4.00, .45, 2.6, 0, 7, -22.5], [.8, 3.95, 1.35, 2.2, 3, 5, -22.5],
    [1.6, 3.65, .7, 2.2, 4, 6, -45], [2.2, 3.10, .4, 1.6, 2, 7, -45]]},
  hip: {base: 'plH', g: 'hip', list: [[0, 3.65, 2.2, 2.6, 3, 5, 0], [0, 3.50, 3.2, 2.2, 1, 6, 0], [0, 3.30, 4.1, 1.7, 4, 7, 0], [.7, 3.55, 2.6, 2.2, 0, 7, -22.5],
    [.75, 3.35, 3.55, 1.6, 2, 5, -22.5], [1.45, 3.25, 2.9, 1.6, 4, 6, -45]]},
};
function plateGroup(key, spr) {
  const {base, g, list} = G[key], B = J[base], Ri = q([-PLATE_LEAN[g], 0, 0]), els = [];
  for (const [x, y, z, L, ks, kf, sp] of list) for (const sx of x ? [1, -1] : [1]) {
    const p = rot(Ri, [sx * x - B[0], y - B[1], z - B[2]]);
    els.push(...plate(spr, p, L, ks, kf, sx * sp));
  }
  return els;
}

// ---- gold crystals (model.md §3.6): trident clusters along the crest's lower edge, a big spike on each shoulder ---------
// Shard sheet: 4 crystal shapes in cells of 32 x 64 (aspect 1:2), each a pointed blade with a facet line; a shard is a
// crossed pair of cards (side + front) turned out by its splay round its base.
const SHARDS = [{tip: .1, w: .3}, {tip: .22, w: .26}, {tip: 0, w: .36}, {tip: .16, w: .32}];
const SH = SHARDS.map(b => {
  const pts = Array.from({length: 13}, (_, i) => { const t = i / 12; return [(.5 + b.tip * t * t) / 2, t]; });
  const S = stroke(pts, t => b.w / 2 * (t < .08 ? .6 + 5 * t : 1) * (1 - t) ** .75);
  return {...b, S, sd: (x, y) => S.sd(x / 2, y)};
});
function shardColour(b, x, y) {
  const d = b.sd(x, y);
  if (d > 0) return null;
  const n = b.S.near(x / 2, y), side = n.s > 0;
  let c = goldPx(side ? .12 + .3 * n.t : .4 + .25 * n.t, x * 30, y * 60);
  if (d > -.012) c = PAL.gold(side ? .5 : .78);            // darker amber edges
  if (Math.abs(n.s) < .008) c = PAL.gold(.02);              // the bright facet line
  return c;
}
const shardSheet = (s, t) => { const k = Math.min(3, Math.floor(s * 4)); return shardColour(SH[k], s * 4 - k, 1 - t) || TRANSPARENT; };
function shard([x, y, z], L, k, splay = 0, {thick = .05} = {}) {
  const W = L * .5, rot = splay ? ['z', splay, [x, y, z]] : undefined;
  const els = [cardX('shards', x, {Z0: z - W / 2, Z1: z + W / 2, Y0: y, Y1: y + L}, {rot}), cardZ('shards', z, {X0: x - W / 2, X1: x + W / 2, Y0: y, Y1: y + L * .92}, {rot, uvr: [0, .08, 1, 1]})];
  for (const e of els) for (const f of Object.values(e.faces)) { const [a, b, c2, d] = f.uv; f.uv = [k * 4 + a / 4, b, k * 4 + c2 / 4, d].map(v => +v.toFixed(4)); }
  if (thick > .06) els.push(abox([x - thick, y, z - thick], [x + thick, y + L * .45, z + thick], 'gold', {rot}));
  return els;
}
// A trident cluster: three crystals fanned from one base (the centre at the splay, the others toward vertical / out).
function cluster(at, L, k, o) {
  const [x, y, z] = at, ang = Math.abs(o) >= 45 ? [o, o / 2, 0] : [o, 0, 2 * o];
  return [...shard([x, y, z], L, k, ang[0]), ...shard([x - Math.sign(x) * .05, y, z + .16], L * .75, (k + 1) % 4, ang[1]), ...shard([x + Math.sign(x) * .05, y - .05, z - .14], L * .66, (k + 2) % 4, ang[2])];
}
const CRYS = {
  sh: {base: 'plS', list: [[2.35, 3.6, -1.95, 1.85, 2, -45, 'spike'], [1.95, 3.55, -1.05, 1.45, 1, -45], [1.2, 3.95, -2.55, 1.2, 3, -22.5], [2.55, 2.95, -.45, 1.2, 0, -45], [1.25, 3.95, -.3, 1.05, 2, -22.5]]},
  mid: {base: 'plM', list: [[2.0, 3.4, -.1, 1.5, 1, -45], [2.15, 3.2, 1.05, 1.35, 0, -45], [1.25, 3.8, .85, 1.2, 3, -22.5], [2.5, 2.7, .55, 1.0, 2, -45]]},
  hip: {base: 'plH', list: [[1.9, 3.0, 2.2, 1.25, 2, -45], [1.8, 2.85, 3.15, 1.1, 1, -45], [1.15, 3.15, 3.7, .9, 0, -22.5], [2.2, 2.4, 2.75, .9, 3, -45]]},
};
function crystalGroup(g) {
  const {base, list} = CRYS[g], B = J[base], els = [];
  for (const [x, y, z, L, k, sp, kind] of list) for (const s of [1, -1]) {
    const p = [s * x - B[0], y - B[1], z - B[2]];
    if (kind === 'spike') els.push(...shard(p, L, k, s * sp / 2, {thick: .14}), ...shard([p[0] + s * .2, p[1] - .1, p[2] + .25], L * .65, 3, s * sp));
    else els.push(...cluster(p, L, k, s * sp));
  }
  return els;
}

// ---- region exports ---------------------------------------------------------------------------------------------------------
export function models() {
  const M = {
    chest: U('chest', chest()), belly: U('belly', belly()), pelvis: U('pelvis', pelvis()), neck1: U('neck1', neck1()), neck2: U('neck2', neck2()),
    apron: U('apron', apronEls('apron')),
    crys_sh: U('crys_sh', crystalGroup('sh')), crys_mid: U('crys_mid', crystalGroup('mid')), crys_hip: U('crys_hip', crystalGroup('hip')),
  };
  for (const look of ['hydro', 'pyro']) {
    M['belly_' + look] = U('belly', belly(look));
    M['apron_' + look] = U('apron', apronEls('apron_' + look));
  }
  M.glow_apron = U('glow_apron', apronEls('apron_mask', {tint: true, glow: true}));
  for (const [g, part] of [['neck', 'plates_neck'], ['sh', 'plates_sh'], ['mid', 'plates_mid'], ['hip', 'plates_hip']]) {
    M[part] = U(part, plateGroup(g, 'plates'));
    for (const look of ['cryo', 'electro']) M[part + '_' + look] = U(part, plateGroup(g, 'plates_' + look));
  }
  return M;
}
export const LOOKS = {
  legs: {
    belly: {geo: 'belly', hydro: 'belly_hydro', pyro: 'belly_pyro'},
    apron: {geo: 'apron', hydro: 'apron_hydro', pyro: 'apron_pyro'},
    glow_apron: {geo: 'empty', hydro: 'glow_apron_hydro', pyro: 'glow_apron_pyro'},
  },
  tail: Object.fromEntries(['plates_neck', 'plates_sh', 'plates_mid', 'plates_hip'].map(p => [p, {geo: p, cryo: p + '_cryo', electro: p + '_electro'}])),
};
export const TINTED = {glow_apron_hydro: ['glow_apron', LOOK_PAL.hydro.tint], glow_apron_pyro: ['glow_apron', LOOK_PAL.pyro.tint]};
// brightness per look (the bright parts of a look; others keep their PARTS level)
export const LOOK_BRIGHT = {legs: {hydro: {apron: 14, belly: 13}, pyro: {apron: 14, belly: 14}}, tail: {cryo: Object.fromEntries(Object.keys(LOOKS.tail).map(p => [p, 15])), electro: Object.fromEntries(Object.keys(LOOKS.tail).map(p => [p, 15]))}};

// belly ribs: one broad rib per underside facet (u across the facet), faint cross cracks; Pyro cracks glow red-orange
function bellyPaint(look) {
  const L = look ? LOOK_PAL[look] : null;
  return (s, t) => {
    const u = s * 64, v = t * 128;
    let c = creamPx(u * 1.3, v, PAL.cream, .6);
    c = mix(c, PAL.cream(.5), .55 * Math.pow(Math.abs(s - .5) * 2, 2.5));             // rib curvature
    if (s < .06 || s > .94) c = mix(c, PAL.groove(.3), .6);                              // the groove between ribs
    const cr = Math.abs(N.f(s * 3 + 1, t * 1.3) - .5);
    if (cr < .02) c = look === 'pyro' ? L.glow(.25 + cr * 20) : look === 'hydro' ? mix(c, L.glow(.4), .5) : mix(c, PAL.groove(.6), .6);
    return c;
  };
}
export function sprites() {
  const S = {};
  const card = (name, rect, ppb, fn, tr = false) => { const [w, h] = spriteSize(rect, ppb); S[name] = [w, h, onRect(rect, fn), tr]; };
  card('apron', AP, 96, apronPaint(null));
  card('apron_hydro', AP, 96, apronPaint('hydro'));
  card('apron_pyro', AP, 96, apronPaint('pyro'));
  card('apron_mask', AP, 96, apronMask, true);
  S.plates = [SHEET.cw * SHEET.n, SHEET.ch, plateSheet(null), false];
  S.plates_cryo = [SHEET.cw * SHEET.n, SHEET.ch, plateSheet('cryo'), false];
  S.plates_electro = [SHEET.cw * SHEET.n, SHEET.ch, plateSheet('electro'), false];
  S.shards = [128, 64, shardSheet, false];
  S.belly = [64, 128, bellyPaint(null), false];
  S.belly_hydro = [64, 128, bellyPaint('hydro'), false];
  S.belly_pyro = [64, 128, bellyPaint('pyro'), false];
  return S;
}
