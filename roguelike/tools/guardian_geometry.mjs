// Part models of the Corrupted Guardian (파수꾼・타락) rig, used by build_mboss_guardian_rig.mjs.
//
// Authoring frame ("A-frame", the rig's frame): +X = her LEFT (screen right in a front view),
// +Y up, -Z forward; units are model units relative to the display pivot (model [8,8,8]).
// Item models render x-mirrored in that frame (see build_raiden_rig.mjs), so every element is
// converted with model = (8 - X, 8 + Y, 8 + Z); element rotations about y/z flip sign. Cards
// show their sprite as painted (front view) from -Z; texture coordinates are solved per face
// from the A-frame position of each corner, so the conversion never mirrors a sprite.
//
// Constraints kept by every model: coordinates within -16..32, element rotations single-axis
// in 22.5 degree steps within +-45, painted cards shade:false (the sprites carry the shading),
// voxel/metal boxes shade:true.
import {CARD} from './guardian_paint.mjs';

const r4 = v => Math.round(v * 1e4) / 1e4;
const toM = ([X, Y, Z]) => [8 - X, 8 + Y, 8 + Z];
const FACE_OF = {front: 'north', back: 'south', left: 'west', right: 'east', up: 'up', down: 'down'};
const corners = (face, [x0, y0, z0], [x1, y1, z1]) => ({
  north: [[x1, y1, z0], [x0, y1, z0], [x0, y0, z0], [x1, y0, z0]],
  south: [[x0, y1, z1], [x1, y1, z1], [x1, y0, z1], [x0, y0, z1]],
  east: [[x1, y1, z1], [x1, y1, z0], [x1, y0, z0], [x1, y0, z1]],
  west: [[x0, y1, z0], [x0, y1, z1], [x0, y0, z1], [x0, y0, z0]],
  up: [[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]],
  down: [[x0, y0, z1], [x1, y0, z1], [x1, y0, z0], [x0, y0, z0]],
})[face];
function solveUV(face, lo, hi, fn) {
  const D = corners(face, lo, hi).map(fn), eq = (a, b) => Math.abs(a - b) < 1e-5;
  for (let k = 0; k < 4; k++) {
    const u = [0, 1, 2, 3].map(j => D[(j + k) % 4]);
    if (eq(u[0][1], u[1][1]) && eq(u[1][0], u[2][0]) && eq(u[2][1], u[3][1]) && eq(u[3][0], u[0][0]))
      return [[u[0][0], u[0][1], u[2][0], u[2][1]].map(v => r4(Math.min(16, Math.max(0, v)))), k * 90];
  }
  throw new Error('no uv solution for ' + face);
}
const rotM = rot => {
  if (!rot) return undefined;
  const [axis, angle, origin] = rot;
  if (![-45, -22.5, 22.5, 45].includes(angle)) throw new Error('element rotation ' + angle);
  return {origin: toM(origin).map(r4), axis, angle: axis === 'x' ? angle : -angle};
};
// Box in the A-frame. tex: sprite name, or {all, front, back, left, right, up, down, uv}.
export function abox(a, b, tex, {rot, shade = true, uv = [0, 0, 16, 16], drop = []} = {}) {
  const lo = a.map((v, i) => Math.min(v, b[i])), hi = a.map((v, i) => Math.max(v, b[i]));
  const from = [8 - hi[0], 8 + lo[1], 8 + lo[2]].map(r4), to = [8 - lo[0], 8 + hi[1], 8 + hi[2]].map(r4);
  const spec = typeof tex === 'string' ? {all: tex} : tex;
  const faces = {};
  for (const [af, mf] of Object.entries(FACE_OF)) {
    if (drop.includes(af)) continue;
    const t = spec[af] || spec.all;
    if (!t) continue;
    faces[mf] = {texture: '#' + t, uv: (spec.uv && spec.uv[af]) || uv};
  }
  const el = {from, to, faces};
  if (!shade) el.shade = false;
  const r = rotM(rot);
  if (r) el.rotation = r;
  return el;
}
// Card in the plane Z = z, spanning rect {X0,X1,Y0,Y1} (A-frame), sprite as painted, seen from -Z.
// uvr = sprite sub-rectangle [u0, v0, u1, v1] in 0..1; flipU mirrors the sprite left-right.
export function cardZ(sprite, z, rect = CARD[sprite], {uvr = [0, 0, 1, 1], flipU = false, rot, shade = false, tint = false} = {}) {
  const {X0, X1, Y0, Y1} = rect;
  const from = [8 - X1, 8 + Y0, 8 + z].map(r4), to = [8 - X0, 8 + Y1, 8 + z].map(r4);
  const fn = p => {
    const X = 8 - p[0], Y = p[1] - 8;
    let s = (X - X0) / (X1 - X0);
    if (flipU) s = 1 - s;
    const t = (Y1 - Y) / (Y1 - Y0);
    return [16 * (uvr[0] + (uvr[2] - uvr[0]) * s), 16 * (uvr[1] + (uvr[3] - uvr[1]) * t)];
  };
  const faces = {};
  for (const f of ['north', 'south']) {
    const [uv, r] = solveUV(f, from, to, fn);
    faces[f] = {texture: '#' + sprite, uv, ...(r ? {rotation: r} : {}), ...(tint ? {tintindex: 0} : {})};
  }
  const el = {from, to, faces};
  if (!shade) el.shade = false;
  const r = rotM(rot);
  if (r) el.rotation = r;
  return el;
}
// Card in the plane X = x: u runs along +Z (toward her back) over Z0..Z1, v top to bottom.
export function cardX(sprite, x, {Z0, Z1, Y0, Y1}, {uvr = [0, 0, 1, 1], flipU = false, rot, shade = false, tint = false} = {}) {
  const from = [8 - x, 8 + Y0, 8 + Z0].map(r4), to = [8 - x, 8 + Y1, 8 + Z1].map(r4);
  const fn = p => {
    const Z = p[2] - 8, Y = p[1] - 8;
    let s = (Z - Z0) / (Z1 - Z0);
    if (flipU) s = 1 - s;
    const t = (Y1 - Y) / (Y1 - Y0);
    return [16 * (uvr[0] + (uvr[2] - uvr[0]) * s), 16 * (uvr[1] + (uvr[3] - uvr[1]) * t)];
  };
  const faces = {};
  for (const f of ['east', 'west']) {
    const [uv, r] = solveUV(f, from, to, fn);
    faces[f] = {texture: '#' + sprite, uv, ...(r ? {rotation: r} : {}), ...(tint ? {tintindex: 0} : {})};
  }
  const el = {from, to, faces};
  if (!shade) el.shade = false;
  const r = rotM(rot);
  if (r) el.rotation = r;
  return el;
}
const shiftRect = (r, dx = 0, dy = 0) => ({X0: r.X0 + dx, X1: r.X1 + dx, Y0: r.Y0 + dy, Y1: r.Y1 + dy});
const mirrorRect = r => ({X0: -r.X1, X1: -r.X0, Y0: r.Y0, Y1: r.Y1});
const plate = (sprite, cx, cy, size, z, opt) => cardZ(sprite, z, {X0: cx - size / 2, X1: cx + size / 2, Y0: cy - size / 2, Y1: cy + size / 2}, opt);
const cube = (c, s, tex, rot) => abox([c[0] - s / 2, c[1] - s / 2, c[2] - s / 2], [c[0] + s / 2, c[1] + s / 2, c[2] + s / 2], tex, {rot: rot ? [rot[0], rot[1], c] : undefined});

// ---- parts --------------------------------------------------------------------------------
// Display scale per part (blocks per 16 model units = scale).
export const PART_SCALE = {
  pelvis: 1, skirt_f: 1.35, skirt_o: 1.35, tail: 1.5, leg_r: 1.2, leg_l: 1.2, torso: 1, head: 1.2, halo: 1, halo_glow: 1,
  r_upper: 1, r_fore: 1, r_hand: 1, l_upper: 1, l_fore: 1, l_hand: 1, bracket: 1, shield: 1, shield_eye: 1,
  wing_cov: 2.0, wing_sec: 2.0, wing_pri: 2.2, spear: 2.2, spear_glow: 2.2, trail_1: 2.2, trail_2: 2.2, cubes_a: 1, cubes_b: 1, cubes_c: 1,
};

function pelvis() {
  return [
    abox([-2.5, -2.4, -1.8], [2.5, 2.4, 1.8], 'gd_redcore'),
    abox([-2.9, -.7, -2.15], [2.9, .5, 2.15], 'gd_gold'),
    cardZ('gd_belt', -2.3),
    cardZ('gd_belt', 2.3, CARD.gd_belt, {flipU: true}),
    // hip ornament on her left hip: gold boss with a red eye
    abox([2.5, -1.7, -1.5], [3.5, -.3, .3], 'gd_gold'),
    plate('gd_redstar', 3.0, -1.0, 1.3, -1.6),
    plate('gd_redstar', -3.0, -1.0, 1.0, -1.5),
  ];
}
// Front panels + tabard: one card (the sprite leaves the leg slit open).
const skirtFront = () => [cardZ('gd_skirt_front', -.75)];
// Outer flared panels hang straight from the hip sides (no roll at the belt; the flare is
// painted into the lower third), each turned 22.5 degrees back about Y for depth; the back
// panel; the hip feather-wings at the belt corners in front of the outer panels.
function skirtOuter() {
  const side = CARD.gd_skirt_side;
  const right = {X0: -2.4 - side.X1, X1: -2.4 - side.X0, Y0: side.Y0 - .2, Y1: side.Y1 - .2};
  const hip = CARD.gd_hip_wing, hipR = shiftRect(hip, -3.2, -.5);
  return [
    cardZ('gd_skirt_side', .5, right, {flipU: true, rot: ['y', 22.5, [-2.4, 0, .5]]}),
    cardZ('gd_skirt_side', .5, mirrorRect(right), {rot: ['y', -22.5, [2.4, 0, .5]]}),
    cardZ('gd_skirt_back', 2.0),
    cardZ('gd_hip_wing', -1.3, hipR, {rot: ['y', 22.5, [-3.2, 0, -1.3]]}),
    cardZ('gd_hip_wing', -1.3, mirrorRect(hipR), {flipU: true, rot: ['y', -22.5, [3.2, 0, -1.3]]}),
  ];
}
function tail() {
  const r = CARD.gd_tail;
  return [cardZ('gd_tail', 0), cardZ('gd_tail', .3), cardX('gd_tail', 1.2, {Z0: -1.8, Z1: 2.6, Y0: r.Y0, Y1: r.Y1}, {uvr: [.25, 0, .75, 1]})];
}
// Voxel leg: 5 stacked cubes (glitch-offset, some turned) and the 45 degree foot cube.
function leg(side) {
  const s = side, e = [];
  const cubes = [[.2, -1.6, 0, 2.5, 0], [-.3, -5.0, .2, 2.4, 22.5], [.25, -8.4, -.1, 2.4, 0], [-.2, -11.8, .25, 2.3, -22.5], [.15, -15.1, 0, 2.4, 0]];
  cubes.forEach(([x, y, z, w, r], i) => e.push(cube([x * s, y, z], w, i % 2 ? 'gd_vox_rune' : 'gd_vox', r ? ['y', r * s] : null)));
  e.push(cube([0, -18.9, -.2], 3.2, 'gd_vox_rune', ['y', 45]));
  return e;
}
function torso() {
  return [
    abox([-1.9, 0, -1.5], [1.9, 10.2, 1.5], 'gd_redcore'),
    abox([-2.6, 7.6, -1.6], [2.6, 10.8, 1.6], 'gd_dark'),
    cardZ('gd_chest', -1.8),
    cardZ('gd_chest_back', 1.8, CARD.gd_chest, {flipU: true}),
    // corrupted right shoulder: jagged crimson voxels
    abox([-4.0, 7.8, -1.7], [-2.0, 10.9, 1.5], 'gd_corrupt'),
    cube([-3.8, 11.0, -.3], 1.6, 'gd_corrupt_b', ['y', 22.5]),
    cube([-2.8, 11.4, .6], 1.3, 'gd_corrupt', ['x', 22.5]),
    // left gold pauldron: a rounded cap over the shoulder joint and a swept plate on top
    abox([2.0, 7.8, -1.6], [3.4, 10.8, 1.4], 'gd_gold'),
    ...cap([4.1, 9.8, -.1], 1.75),
    abox([2.8, 10.7, -1.3], [5.6, 11.6, 1.1], 'gd_gold', {rot: ['z', -22.5, [4.2, 11.1, 0]]}),
    // neck voxels
    abox([-.9, 10.6, -.8], [.9, 12.6, .8], 'gd_corrupt_b'),
    cube([.7, 12.0, -.5], 1.0, 'gd_corrupt', ['y', 45]),
  ];
}
function head() {
  const c = CARD.gd_crest;
  return [
    abox([-1.3, -.3, -1.2], [1.3, 2.7, 1.6], 'gd_dark'),
    cardZ('gd_crest', -1.6),
    cardZ('gd_crest', -1.3),
    cardZ('gd_crest_back', 1.9, c, {flipU: true}),
    cardX('gd_crest_side', -.55, {Z0: -3.2, Z1: 1.6, Y0: 1.8, Y1: 6.6}, {flipU: true}),
    cardX('gd_crest_side', .55, {Z0: -3.2, Z1: 1.6, Y0: 1.8, Y1: 6.6}, {flipU: true}),
  ];
}
const halo = () => [cardZ('gd_halo', 0)];
const haloGlow = () => [cardZ('gd_halo_glow', .6)];

// Corrupted right arm: jagged crimson voxels; segments hang along -Y from their joint. In the
// segment frame -X is her right (the outside of the arm), -Z the inside of the bend. Thin shard
// plates turned 22.5-45 degrees stick out of the box outline so the limb reads jagged.
function rUpper() {
  return [
    abox([-1.7, -8.2, -1.7], [1.7, .9, 1.7], 'gd_corrupt'),
    cube([-1.8, -2.0, .5], 2.2, 'gd_corrupt_b', ['y', 22.5]),
    cube([1.5, -5.0, -.9], 1.9, 'gd_corrupt_b', ['x', 22.5]),
    cube([-.8, -7.0, 1.4], 1.7, 'gd_corrupt', ['z', 22.5]),
    cube([-1.5, -4.4, -1.3], 1.5, 'gd_corrupt', ['x', -22.5]),
    abox([-2.0, -4.8, -.9], [-1.5, -.6, 1.1], 'gd_corrupt_b', {rot: ['z', -45, [-1.7, -.8, 0]]}),
    abox([-.9, -6.8, 1.4], [1.0, -2.8, 1.9], 'gd_corrupt', {rot: ['x', -45, [0, -3.0, 1.6]]}),
    abox([-2.1, -7.6, -1.2], [-1.6, -5.0, .8], 'gd_corrupt', {rot: ['z', -22.5, [-1.8, -5.2, 0]]}),
  ];
}
function rFore() {
  return [
    abox([-1.55, -7.8, -1.55], [1.55, .6, 1.55], 'gd_corrupt_b'),
    cube([-1.7, -1.0, 0], 2.1, 'gd_corrupt', ['z', 22.5]),
    cube([1.3, -3.8, 1.0], 1.7, 'gd_corrupt', ['y', 22.5]),
    cube([-1.0, -6.2, -1.2], 1.6, 'gd_corrupt_b', ['x', -22.5]),
    cube([1.1, -7.0, -.8], 1.4, 'gd_corrupt', ['y', 45]),
    // jagged spike at the elbow pointing back, shards along the outside and the back
    abox([-.6, -.8, 1.2], [.6, .4, 4.2], 'gd_corrupt', {rot: ['x', 22.5, [0, 0, 1.2]]}),
    abox([-1.9, -5.8, -.8], [-1.4, -2.0, 1.0], 'gd_corrupt_b', {rot: ['z', -45, [-1.6, -2.2, 0]]}),
    abox([-.8, -7.4, 1.3], [.8, -4.4, 1.8], 'gd_corrupt', {rot: ['x', -45, [0, -4.6, 1.5]]}),
  ];
}
// Talon pair: a side card (claw profile) and a front card, rotated together.
const talonPair = (tal, x, z, y0, y1, w, rot) => [
  cardX(tal, x, {Z0: z - w, Z1: z + w, Y0: y1, Y1: y0}, {rot, flipU: true}),
  cardZ(tal, z, {X0: x - w, X1: x + w, Y0: y1, Y1: y0}, {rot}),
];
// Hands: wrist at the pivot, fingers toward -Y, the palm side toward -Z. Fist: the shaft
// passes along X at Y -2.2, Z 0, the fingers wrap in front of it and the talons hang past it.
function clawFist(gold) {
  const pal = gold ? 'gd_gold' : 'gd_corrupt', tal = gold ? 'gd_talon_gold' : 'gd_talon', e = [];
  e.push(abox([-1.35, -1.3, -.3], [1.35, .4, 1.5], pal));            // back of the hand
  e.push(abox([-1.4, -3.4, .95], [1.4, -1.1, 1.75], pal));           // knuckles behind the shaft
  for (let i = 0; i < 4; i++) {
    const x = -1.25 + i * .68;
    e.push(abox([x, -3.6, -1.5], [x + .5, -1.0, -.9], pal));         // fingers in front of the shaft
    // long talons hanging past the shaft, the outer ones fanned out (corrupted claw: >= 0.2 b)
    const L = gold ? 2.0 : 3.6, xc = x + .25;
    const rot = i === 0 ? ['z', 22.5, [xc, -3.5, -1.2]] : i === 3 ? ['z', -22.5, [xc, -3.5, -1.2]] : ['x', 22.5, [xc, -3.5, -1.2]];
    e.push(...talonPair(tal, xc, -1.2, -3.3, -3.3 - L, gold ? .28 : .36, rot));
  }
  e.push(abox([1.3, -2.8, -1.1], [2.1, -.6, .5], pal));               // thumb on her left side of the shaft
  return e;
}
// Open claw: slim back of the hand, four two-jointed fingers curling toward the palm, long talons.
// thumb = +1 puts the thumb on +X (the right hand's inside), -1 on -X (the left hand's inside).
function clawOpen(gold, thumb = 1) {
  const pal = gold ? 'gd_gold' : 'gd_corrupt', tal = gold ? 'gd_talon_gold' : 'gd_talon', e = [];
  e.push(abox([-.85, -.3, -.45], [.85, .7, .65], pal));               // wrist
  e.push(abox([-1.2, -1.95, -.35], [1.2, -.2, .55], pal));            // back of the hand
  const fx = [-.93, -.31, .31, .93], fl = [1.55, 1.9, 1.85, 1.45], tl = gold ? [2.2, 2.6, 2.5, 2.0] : [3.2, 3.8, 3.6, 3.0];
  fx.forEach((x, i) => {
    const L = fl[i];
    e.push(abox([x - .21, -1.85 - L, -.23], [x + .21, -1.75, .23], pal, {rot: ['x', 22.5, [x, -1.8, 0]]}));
    const jy = -1.8 - L * .924, jz = -L * .383;
    e.push(abox([x - .17, jy - 1.0, jz - .19], [x + .17, jy + .1, jz + .19], pal, {rot: ['x', 45, [x, jy, jz]]}));
    e.push(...talonPair(tal, x, jz, jy - .85, jy - .85 - tl[i], .3, ['x', 45, [x, jy, jz]]));
  });
  const tx = thumb * 1.25;
  e.push(abox([tx - .25, -1.7, -.6], [tx + .25, -.1, .1], pal, {rot: ['z', thumb * 22.5, [tx, -.2, 0]]}));
  e.push(...talonPair(tal, tx + thumb * .55, -.3, -1.4, -1.4 - tl[0] * .75, .26, ['z', thumb * 22.5, [tx, -.2, 0]]));
  return e;
}
// Rounded cap: sphere-painted disc cards in four vertical planes (0, 45, 90, 135 degrees about
// Y) and one horizontal disc, so the cap reads round from any side.
function cap(c, r, tex = 'gd_cap') {
  const [x, y, z] = c, rect = {X0: x - r, X1: x + r, Y0: y - r, Y1: y + r};
  return [
    cardZ(tex, z, rect), cardX(tex, x, {Z0: z - r, Z1: z + r, Y0: y - r, Y1: y + r}),
    cardZ(tex, z, rect, {rot: ['y', 45, c]}), cardZ(tex, z, rect, {rot: ['y', -45, c]}),
    abox([x - r, y, z - r], [x + r, y, z + r], {up: tex, down: tex}, {shade: false}),
  ];
}
// Left (gold) arm, model.md §3.4 and the binding feedback in plan.md: slim tapered segments made
// of two crossed painted silhouette cards, rounded gold shoulder and elbow caps; a white sleeve
// under a gold plate, then the glowing amber gauntlet with a gold flare and cuff.
const crossed = (sprite, r) => [cardZ(sprite, 0, r), cardX(sprite, 0, {Z0: r.X0, Z1: r.X1, Y0: r.Y0, Y1: r.Y1})];
const lUpper = () => [...crossed('gd_larm_up', CARD.gd_larm_up), ...cap([0, -.15, 0], 1.55)];
const lFore = () => [...crossed('gd_larm_fore', CARD.gd_larm_fore), ...cap([0, .05, 0], 1.3)];
function bracket() {
  // gold arm from the shoulder mount (0,0,0) toward the shield: two bars and two round joints;
  // it ends under the shield's inner rim (the shield centre sits 1.05 b out along the bar)
  return [
    abox([0, -.85, -.65], [6.6, .85, .65], 'gd_gold'),
    abox([6.6, -.7, -.55], [10.0, .7, .55], 'gd_gold'),
    abox([2.4, .7, -.4], [6.0, 1.4, .4], 'gd_gold_dark'),
    plate('gd_joint', 0, 0, 3.0, -.75), plate('gd_joint', 0, 0, 3.0, .75),
    plate('gd_joint', 6.6, 0, 3.4, -.7), plate('gd_joint', 6.6, 0, 3.4, .7),
    plate('gd_blackstar', 6.6, -2.6, 2.8, -.8), plate('gd_blackstar', 6.6, -2.6, 2.8, .8),
  ];
}
const shield = () => [cardZ('gd_shield', 0)];
// eye overlay: the colour (Geo) version and the luminance version tinted per element, which
// keeps a small untinted white-hot core plate on top.
const shieldEye = () => [cardZ('gd_shield_eye_geo', -.75, CARD.gd_shield_eye), cardZ('gd_shield_eye_geo', .75, CARD.gd_shield_eye)];
const shieldEyeTinted = () => [cardZ('gd_shield_eye', -.75, CARD.gd_shield_eye, {tint: true}), cardZ('gd_shield_eye', .75, CARD.gd_shield_eye, {tint: true}),
  plate('gd_core', -2.0, 0, 2.5, -.85), plate('gd_core', -2.0, 0, 2.5, .85)];
const wingTier = (name, z) => [cardZ(name, z)];

// Spear (scale 2.2, 7.27 units per block): grip at the pivot (sprite Y 8), tip toward +Y.
const SPY = -8;    // sprite Y -> A-frame Y
function spear(enchanted) {
  const head = enchanted ? 'gd_spear_head_e' : 'gd_spear_head', edge = enchanted ? 'gd_spear_edge_e' : 'gd_spear_edge';
  const H = shiftRect(CARD.gd_spear_head, 0, SPY), E = CARD.gd_spear_edge;
  const t = enchanted;
  return [
    // one double-sided head card (stacked copies read as triple outlines off-axis)
    cardZ(head, 0, H, {tint: t}),
    cardX(edge, 0, {Z0: E.X0, Z1: E.X1, Y0: E.Y0 + SPY, Y1: E.Y1 + SPY}, {tint: t}),
    abox([-.26, 2.3 + SPY, -.26], [.26, 14.3 + SPY, .26], 'gd_shaft', {shade: false}),
    abox([-.5, 14.2 + SPY, -.5], [.5, 15.05 + SPY, .5], 'gd_gold'),
    abox([-.4, -.7, -.4], [.4, .7, .4], 'gd_gold_dark'),
    // butt finial star (crossed) and the small orbiting star
    cardZ('gd_spear_star', 0, {X0: -1.3, X1: 1.3, Y0: -.3 + SPY, Y1: 2.5 + SPY}),
    cardX('gd_spear_star', 0, {Z0: -1.3, Z1: 1.3, Y0: -.3 + SPY, Y1: 2.5 + SPY}),
    abox([-.42, 2.2 + SPY, -.42], [.42, 2.9 + SPY, .42], 'gd_gold'),
    cardZ('gd_spear_star', 0, {X0: -.5, X1: .5, Y0: -1.9 + SPY, Y1: -.9 + SPY}),
    cardX('gd_spear_star', 0, {Z0: -.5, Z1: .5, Y0: -1.9 + SPY, Y1: -.9 + SPY}),
  ];
}
// Glow cards sit just off the head plane (z/x +0.3) so they never z-fight the head card.
function spearGlow() {
  const r = {X0: CARD.gd_spear_glow.X0, X1: CARD.gd_spear_glow.X1, Y0: 1.2 + SPY, Y1: 31.8 + SPY};
  return [cardZ('gd_spear_glow', .3, r, {tint: true}), cardX('gd_spear_glow', .3, {Z0: r.X0, Z1: r.X1, Y0: r.Y0, Y1: r.Y1}, {tint: true})];
}
function trail() {
  const r = {X0: -2.6, X1: 2.6, Y0: 1.2 + SPY, Y1: 31.8 + SPY};
  return [cardZ('gd_trail', 0, r, {tint: true}), cardX('gd_trail', 0, {Z0: r.X0, Z1: r.X1, Y0: r.Y0, Y1: r.Y1}, {tint: true})];
}
// Floating body cubes: small solid voxels around the attach point.
const cubesA = () => [cube([0, 0, 0], 3.2, 'gd_vox'), cube([3.6, 2.4, -1.0], 2.2, 'gd_corrupt', ['y', 22.5]), cube([-2.8, 3.6, 1.4], 2.0, 'gd_vox_rune', ['x', 22.5]),
  cube([1.4, 5.6, .6], 1.6, 'gd_corrupt_b', ['z', 45]), cube([-4.0, -1.6, -1.2], 1.8, 'gd_vox', ['y', 45])];
const cubesB = () => [cube([0, 0, 0], 3.4, 'gd_vox_rune', ['y', 45]), cube([2.6, -4.2, 1.2], 2.6, 'gd_vox', ['x', 22.5]), cube([-2.2, -7.6, -.8], 2.2, 'gd_vox', ['y', 22.5]),
  cube([.8, -11.4, .6], 2.0, 'gd_vox_rune', ['z', 45]), cube([-3.8, -2.6, 1.6], 1.6, 'gd_corrupt', ['y', 45]), cube([3.6, -9.0, -1.6], 1.4, 'gd_vox')];
const cubesC = () => [cube([0, 0, 0], 1.8, 'gd_corrupt', ['y', 22.5]), cube([-2.2, 1.6, .6], 1.4, 'gd_vox'), cube([1.6, 2.6, -.8], 1.1, 'gd_corrupt_b', ['x', 45]),
  cube([-3.6, -.6, -.6], 1.2, 'gd_vox', ['z', 22.5])];

// name -> elements. Variants share the display of their part (item model swaps).
export function partModels() {
  return {
    pelvis: pelvis(), skirt_f: skirtFront(), skirt_o: skirtOuter(), tail: tail(), leg_r: leg(-1), leg_l: leg(1),
    torso: torso(), head: head(), halo: halo(), halo_glow: haloGlow(),
    r_upper: rUpper(), r_fore: rFore(), r_hand_fist: clawFist(false), r_hand_open: clawOpen(false, 1),
    l_upper: lUpper(), l_fore: lFore(), l_hand_open: clawOpen(true, -1), l_hand_fist: clawFist(true),
    bracket: bracket(), shield: shield(), shield_eye: shieldEye(), shield_eye_t: shieldEyeTinted(),
    wing_cov: wingTier('gd_wing_cov', -.9), wing_sec: wingTier('gd_wing_sec', 0), wing_pri: wingTier('gd_wing_pri', .8),
    spear: spear(false), spear_e: spear(true), spear_glow: spearGlow(), trail: trail(),
    cubes_a: cubesA(), cubes_b: cubesB(), cubes_c: cubesC(),
  };
}
// Mirror a hand for the other side is not needed: the left hand has its own gold models.
export function checkBounds(name, els) {
  for (const e of els) for (const v of [...e.from, ...e.to]) if (v < -16 || v > 32) throw new Error(`model ${name} leaves -16..32: ${e.from} ${e.to}`);
}
