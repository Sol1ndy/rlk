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
// in 22.5 degree steps within +-45, painted cards and the facets of turned (lathe) parts
// shade:false (the sprites carry the shading), voxel/metal boxes and armour-step discs shade:true.
import {CARD} from './guardian_paint.mjs';
import {rng} from './guardian_paint_lib.mjs';
import {q as qE, rot as qRot, mul as qMul} from './guardian_rig_math.mjs';
import {DEFAULT_POSE} from './guardian_clips.mjs';

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
// ---- lower-body voxels: the two legs and the trail under the hem ------------------------------
// ref.png / the guide render / m1 f340 / m2 f1085 / m3 f1530: no two neat columns, but one broken,
// glitchy stack of dark cubes of very different sizes (small chips to 0.27 b blocks), each turned
// its own way (some corner-on), packed and overlapping high up, breaking apart lower down,
// sticking out past the front panels on her right, a loose cube beside the shins, a big diamond
// foot with a swirl rune and a second, smaller diamond under it, then cubes thinning and drifting
// outward as they fall. Nothing is mirrored: the right leg is the longer, more broken one; the
// left leg ends higher with its foot tucked behind the right foot (the "pair" of m2 f1085).
//
// Item-model elements turn about one axis only (22.5 degree steps), so each of the three
// displays carries a fixed compound turn VOX_REST (applied by the pose after the leg swing);
// each cube's own single-axis turn composes with it, giving every cube its own 3D tilt.
// Positions are authored in the rig frame (blocks, foot bottom y = 0, legs as they hang in idle,
// see VOX_FRAME) and taken into each display's model frame here. The table is art-directed to
// fit between the front panels, the side panels and the back panel without cutting through
// their feathers; a seeded PRNG picks the turns left open and the trail's drift phases, so
// builds are reproducible.
export const VOX_REST = {leg_r: [10, 16, -13], leg_l: [24, -12, 9], cubes_b: [-15, 38, 19]};
// display pivots at rest; they must match the leg and trail pivots in guardian_pose.mjs solve()
export const VOX_PIVOT = {leg_r: [-.10, 1.60, .02], leg_l: [.10, 1.60, .02], cubes_b: [.04, .16, .02]};
export const CUBES_B_VARIANTS = 8;                  // drift frames of the trail, one per 5 t
const VOX_TURNS = [null, ['x', 22.5], ['x', -22.5], ['x', 45], ['x', -45], ['y', 22.5], ['y', -22.5], ['y', 45], ['y', -45],
  ['z', 22.5], ['z', -22.5], ['z', 45], ['z', -45]];
// [x, y, z, size] in blocks (dim [sx, sy, sz] makes a slab instead of a cube); t material
// (gd_lv_*); r turn (omitted = seeded pick); top: lit top face; front: front-face sprite; chunk:
// extra boxes glued to the cube in its own frame ([dx, dy, dz, sx, sy, sz], blocks) for broken,
// blocky chunks.
const LEG_R = [
  {c: [-.04, 1.42, 0, .16], t: 'd', r: ['y', -22.5]},
  {c: [-.07, 1.25, -.01, .17], t: 'c', top: true},
  {c: [-.38, 1.03, 0, .26], dim: [.2, .26, .09], t: 'd', r: ['z', 22.5], top: true, chunk: [[.08, -.13, 0, .13, .12, .08]]},
  {c: [-.05, .97, -.02, .13], t: 'k'},
  {c: [-.08, .80, .04, .17], t: 'c', r: ['x', -22.5]},
  {c: [-.36, .70, -.02, .07], t: 'e'},
  {c: [-.06, .50, .05, .14], t: 'k', r: ['y', 45]},
  {c: [-.20, .36, .03, .10], t: 'd', top: true},
  {c: [-.12, .17, -.03, .23], t: 'd', r: ['z', 45], front: 'gd_lv_rune'},
];
const LEG_L = [
  {c: [.05, 1.44, -.01, .14], t: 'k'},
  {c: [.05, 1.30, -.005, .16], t: 'c', r: ['y', 45]},
  {c: [.02, 1.13, -.02, .11], t: 'd'},
  {c: [.06, 1.04, .015, .18], t: 'd', top: true, chunk: [[-.06, .07, .02, .1, .09, .1]]},
  {c: [.34, .93, -.04, .08], t: 'e', r: ['x', 45]},
  {c: [.05, .83, -.02, .15], t: 'c'},
  {c: [.08, .60, -.01, .12], t: 'k', r: ['z', -22.5]},
  {c: [.03, .36, .02, .18], t: 'c', r: ['x', 22.5], top: true},
];
// Trail cubes: drift (amplitude, b) or fall {h: drop b, dx: outward drift}; each gets its own
// seeded phase, so no two move together (the display adds one slow tumble on top).
const TRAIL = [
  {c: [-.42, .50, .02, .10], t: 'c', r: ['y', 45], drift: .03},
  {c: [-.17, -.13, .03, .15], t: 'd', r: ['z', 45], drift: .02},
  {c: [.07, -.02, -.03, .07], t: 'k', drift: .025},
  {c: [-.03, -.20, .06, .09], t: 'c', fall: {h: .1, dx: -.03}},
  {c: [.18, -.17, -.01, .06], t: 'e', fall: {h: .09, dx: .04}},
  {c: [-.33, .05, .05, .05], t: 'lit', drift: .03},
  {c: [.27, .17, 0, .08], t: 'd', drift: .028},
  {c: [-.13, -.27, 0, .05], t: 'k', fall: {h: .06, dx: -.02}},
];
const conjQ = Q => [-Q[0], -Q[1], -Q[2], Q[3]];
// The legs are authored as they hang in the default (idle) pose, its small leg swing included,
// so the table is what the idle hover shows; the trail is authored unswung.
const VOX_FRAME = {leg_r: DEFAULT_POSE.legR, leg_l: DEFAULT_POSE.legL, cubes_b: [0, 0, 0]};
// Cube list of one display -> elements. off(i) / grow(i) / turn(i): per-cube drift (blocks),
// size factor and turn override for the trail frames.
function voxElements(disp, list, seed, {off = () => [0, 0, 0], grow = () => 1, turn = () => undefined} = {}) {
  const k = 16 / PART_SCALE[disp], piv = VOX_PIVOT[disp], iq = conjQ(qMul(qE(VOX_FRAME[disp]), qE(VOX_REST[disp]))), R = rng(seed);
  const els = [];
  let last = -1;
  list.forEach((cb, i) => {
    let ti = VOX_TURNS.findIndex(x => JSON.stringify(x) === JSON.stringify(cb.r ?? 'pick'));
    const pick = Math.floor(R() * (VOX_TURNS.length - 1));       // always drawn: stable sequence
    if (ti < 0) ti = pick >= last ? pick + 1 : pick;              // never the neighbour's turn
    last = ti;
    const r = turn(i) ?? VOX_TURNS[ti];
    const [x, y, z, s0] = cb.c, s = s0 * grow(i);
    if (s < .005) return;
    const m = qRot(iq, add3(sub3([x, y, z], piv), off(i))).map(v => v * k);
    const tex = {all: 'gd_lv_' + cb.t, ...(cb.top ? {up: 'gd_lv_lit'} : {}), ...(cb.front ? {front: cb.front} : {})};
    const half = (cb.dim || [s0, s0, s0]).map(v => v * grow(i) * k / 2);
    els.push(abox(sub3(m, half), add3(m, half), tex, {rot: r ? [r[0], r[1], m] : undefined}));
    for (const [dx, dy, dz, sx, sy, sz] of cb.chunk || []) {
      const cc = [m[0] + dx * k, m[1] + dy * k, m[2] + dz * k], h = [sx, sy, sz].map(v => v * k * grow(i) / 2);
      els.push(abox(sub3(cc, h), add3(cc, h), {all: 'gd_lv_' + cb.t}, {rot: r ? [r[0], r[1], m] : undefined}));
    }
  });
  return els;
}
const add3 = (a, b) => a.map((v, i) => v + b[i]), sub3 = (a, b) => a.map((v, i) => v - b[i]);
const legVox = side => (side < 0 ? voxElements('leg_r', LEG_R, 4111) : voxElements('leg_l', LEG_L, 4127));
// Trail frame v of CUBES_B_VARIANTS (the clips swap them every 5 t): drift cubes wander on
// their own Lissajous loops; fall cubes sink, drift outward, tumble and shrink away, then come
// back small at the top (the shed cubes that are "replaced", model.md 3.9).
function trailVox(v) {
  const R = rng(4153), ph = TRAIL.map(() => R() * 2 * Math.PI), w = 2 * Math.PI * v / CUBES_B_VARIANTS;
  const u = i => (((v / CUBES_B_VARIANTS + ph[i] / (2 * Math.PI)) % 1) + 1) % 1;
  return voxElements('cubes_b', TRAIL, 4139, {
    off: i => {
      const cb = TRAIL[i];
      if (cb.fall) return [cb.fall.dx * u(i), -cb.fall.h * u(i), 0];
      const a = cb.drift, p = ph[i];
      return [a * .6 * Math.sin(w + p), a * Math.sin(w + 1.7 * p + 1), a * .5 * Math.cos(w + p)];
    },
    grow: i => {
      if (!TRAIL[i].fall) return 1;
      const t = u(i);
      return t < .2 ? .45 + .55 * t / .2 : t > .7 ? 1 - .7 * (t - .7) / .3 : 1;
    },
    turn: i => (TRAIL[i].fall ? VOX_TURNS[1 + (Math.floor(u(i) * 4) + i * 3) % (VOX_TURNS.length - 1)] : undefined),
  });
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
    // left shoulder: the chest's gold side plate (the pauldron itself is the bracket's dome)
    abox([2.0, 7.8, -1.6], [3.4, 10.8, 1.4], 'gd_gold'),
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
// Corrupted right hand (crimson voxel claw): wrist at the pivot, fingers toward -Y, the palm
// side toward -Z. Fist: the shaft passes along X at Y -2.2, Z 0, the fingers wrap in front of it
// and the talons hang past it.
function clawFist() {
  const pal = 'gd_corrupt', tal = 'gd_talon', e = [];
  e.push(abox([-1.35, -1.3, -.3], [1.35, .4, 1.5], pal));            // back of the hand
  e.push(abox([-1.4, -3.4, .95], [1.4, -1.1, 1.75], pal));           // knuckles behind the shaft
  for (let i = 0; i < 4; i++) {
    const x = -1.25 + i * .68;
    e.push(abox([x, -3.6, -1.5], [x + .5, -1.0, -.9], pal));         // fingers in front of the shaft
    // long talons hanging past the shaft, the outer ones fanned out (>= 0.2 b)
    const L = 3.6, xc = x + .25;
    const rot = i === 0 ? ['z', 22.5, [xc, -3.5, -1.2]] : i === 3 ? ['z', -22.5, [xc, -3.5, -1.2]] : ['x', 22.5, [xc, -3.5, -1.2]];
    e.push(...talonPair(tal, xc, -1.2, -3.3, -3.3 - L, .36, rot));
  }
  e.push(abox([1.3, -2.8, -1.1], [2.1, -.6, .5], pal));               // thumb on her left side of the shaft
  return e;
}
// Open claw: slim back of the hand, four two-jointed fingers curling toward the palm, long
// talons, the thumb on +X (the right hand's inside).
function clawOpen() {
  const pal = 'gd_corrupt', tal = 'gd_talon', e = [];
  e.push(abox([-.85, -.3, -.45], [.85, .7, .65], pal));               // wrist
  e.push(abox([-1.2, -1.95, -.35], [1.2, -.2, .55], pal));            // back of the hand
  const fx = [-.93, -.31, .31, .93], fl = [1.55, 1.9, 1.85, 1.45], tl = [3.2, 3.8, 3.6, 3.0];
  fx.forEach((x, i) => {
    const L = fl[i];
    e.push(abox([x - .21, -1.85 - L, -.23], [x + .21, -1.75, .23], pal, {rot: ['x', 22.5, [x, -1.8, 0]]}));
    const jy = -1.8 - L * .924, jz = -L * .383;
    e.push(abox([x - .17, jy - 1.0, jz - .19], [x + .17, jy + .1, jz + .19], pal, {rot: ['x', 45, [x, jy, jz]]}));
    e.push(...talonPair(tal, x, jz, jy - .85, jy - .85 - tl[i], .3, ['x', 45, [x, jy, jz]]));
  });
  e.push(abox([1.0, -1.7, -.6], [1.5, -.1, .1], pal, {rot: ['z', 22.5, [1.25, -.2, 0]]}));
  e.push(...talonPair(tal, 1.8, -.3, -1.4, -1.4 - tl[0] * .75, .26, ['z', 22.5, [1.25, -.2, 0]]));
  return e;
}
// ---- turned (lathe) geometry --------------------------------------------------------------
// A round section is a ring of n flat facets (16 by default) about an axis. Each facet is a
// one-face card turned to its azimuth (single-axis element rotations in 22.5 degree steps), so
// the outline is round from every side. The facets are unshaded: their wrap-round texture
// carries the light (a metal highlight toward the side most views see), like the painted cards,
// so the gold keeps its colour instead of the game's dim side-face shading. All facets of one
// lathe share that texture: u = azimuth (facet k shows [k/n, (k+1)/n] of
// the sprite, azimuth 0 = e0 below), v = position along the axis (vFrom -> 0, vTo -> 1).
const AXV = {x: [1, 0, 0], y: [0, 1, 0], z: [0, 0, 1]};
const AZV = {y: [[0, 0, -1], [1, 0, 0]], x: [[0, 0, -1], [0, 1, 0]], z: [[0, 1, 0], [1, 0, 0]]};
const D2R = Math.PI / 180;
const vadd = (a, b) => a.map((x, i) => x + b[i]), vsub = (a, b) => a.map((x, i) => x - b[i]);
const vsc = (v, s) => v.map(x => x * s), vdot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
// Right-handed rotation about an A-frame axis (the sense of `rot` in abox / cardZ / cardX).
function rotA(axis, deg, [x, y, z]) {
  const c = Math.cos(deg * D2R), s = Math.sin(deg * D2R);
  if (axis === 'x') return [x, y * c - z * s, y * s + z * c];
  if (axis === 'y') return [x * c + z * s, y, -x * s + z * c];
  return [x * c - y * s, x * s + y * c, z];
}
const faceOfDir = d => (d[0] > .5 ? 'left' : d[0] < -.5 ? 'right' : d[1] > .5 ? 'up' : d[1] < -.5 ? 'down' : d[2] > .5 ? 'back' : 'front');
// Element spanning the A-frame points pts, with only the listed faces; a face's fn(P) maps its
// A-frame corner points (before the element rotation) to texture [u, v] in 0..16.
function faceEl(pts, faces, {rot, shade = true} = {}) {
  const lo = [0, 1, 2].map(i => Math.min(...pts.map(p => p[i]))), hi = [0, 1, 2].map(i => Math.max(...pts.map(p => p[i])));
  const from = [8 - hi[0], 8 + lo[1], 8 + lo[2]].map(r4), to = [8 - lo[0], 8 + hi[1], 8 + hi[2]].map(r4);
  const out = {};
  for (const [af, {tex, fn, uv}] of Object.entries(faces)) {
    const mf = FACE_OF[af];
    if (fn) {
      const [u, r] = solveUV(mf, from, to, p => fn([8 - p[0], p[1] - 8, p[2] - 8]));
      out[mf] = {texture: '#' + tex, uv: u, ...(r ? {rotation: r} : {})};
    } else out[mf] = {texture: '#' + tex, uv: uv || [0, 0, 16, 16]};
  }
  const el = {from, to, faces: out};
  if (!shade) el.shade = false;
  const r = rotM(rot);
  if (r) el.rotation = r;
  return el;
}
// sections: [{a: [a0, a1] along the axis from c, r: facet inradius, tex}]
function lathe(axis, c, sections, {vFrom, vTo, n = 16}) {
  const A = AXV[axis], [e0, e1] = AZV[axis], dirs = [e0, e1, vsc(e0, -1), vsc(e1, -1)], els = [];
  for (const {a: [a0, a1], r, tex} of sections) {
    const w = 2 * r * Math.tan(Math.PI / n);
    for (let k = 0; k < n; k++) {
      const phi = k * 360 / n, q = Math.round(phi / 90), g = phi - 90 * q, d = dirs[q % 4], t = dirs[(q + 1) % 4];
      const P = (a, s) => vadd(vadd(c, vsc(A, a)), vadd(vsc(d, r), vsc(t, s)));
      const fn = X => { const rel = vsub(X, c); return [16 * (k + .5 + vdot(rel, t) / w) / n, 16 * (vdot(rel, A) - vFrom) / (vTo - vFrom)]; };
      const sg = vdot(rotA(axis, 10, d), t) > 0 ? 1 : -1;
      els.push(faceEl([P(a0, -w / 2), P(a1, w / 2)], {[faceOfDir(d)]: {tex, fn}},
        {shade: false, rot: g ? [axis, sg * g, vadd(c, vsc(A, (a0 + a1) / 2))] : undefined}));
    }
  }
  return els;
}
// Round end/ledge disc across the axis at a; side '+', '-' or '+-'. Discs are inscribed in the
// ring they close (R = its facet inradius x 0.995) so they never show past the facets from the
// side. A plain disc (gold sprite, game-shaded) closes a real armour step; a polar disc is
// unshaded and maps its sprite so that the sprite angle atan2(u - .5, v - .5) is the lathe
// azimuth, so a polar sprite painted per azimuth matches the facets beside it.
function disc(axis, c, a, R, side, tex = 'gd_ldisc', polar = false) {
  const A = AXV[axis], [e0, e1] = AZV[axis], O = vadd(c, vsc(A, a));
  const P = (i, j) => vadd(O, vadd(vsc(e0, i * R), vsc(e1, j * R)));
  const fn = polar ? X => { const rel = vsub(X, O); return [16 * (.5 + vdot(rel, e1) / (2 * R)), 16 * (.5 + vdot(rel, e0) / (2 * R))]; } : undefined;
  const faces = {};
  for (const sd of side) faces[faceOfDir(vsc(A, sd === '+' ? 1 : -1))] = {tex, fn};
  return faceEl([P(-1, -1), P(1, 1)], faces, {shade: !polar});
}
const DK = .995;
// Smooth turned solid: the radius profile prof(a) sampled on the stations `at` (ascending along
// the axis). Section i spans [at[i], at[i+1]] at the radius of its midpoint and reaches 0.02 into
// a wider neighbour; each step is closed by a polar ledge disc painted like the surface, so the
// steps vanish and the outline follows the profile. ends '-' / '+' close the first / last station.
function turned(axis, c, at, prof, tex, ledge, V, ends = '') {
  const rs = at.slice(1).map((x, i) => prof((at[i] + x) / 2)), secs = [], els = [];
  rs.forEach((r, i) => secs.push({a: [at[i] - (i > 0 && rs[i - 1] > r ? .02 : 0), at[i + 1] + (i < rs.length - 1 && rs[i + 1] > r ? .02 : 0)], r, tex}));
  for (let i = 0; i < rs.length - 1; i++) if (Math.abs(rs[i] - rs[i + 1]) > 1e-3)
    els.push(disc(axis, c, at[i + 1], Math.max(rs[i], rs[i + 1]) * DK, rs[i] > rs[i + 1] ? '+' : '-', ledge, true));
  if (ends.includes('-')) els.push(disc(axis, c, at[0], rs[0] * DK, '-', ledge, true));
  if (ends.includes('+')) els.push(disc(axis, c, at[at.length - 1], rs[rs.length - 1] * DK, '+', ledge, true));
  return [...lathe(axis, c, secs, V), ...els];
}
const stations = (a0, a1, n) => Array.from({length: n + 1}, (_, i) => a0 + (a1 - a0) * i / n);
// Turned knob: a sphere of radius R in twelve bands of equal angle (shoulder, elbow).
function knob(axis, c, R) {
  const at = Array.from({length: 13}, (_, i) => R * Math.sin((-90 + 15 * i) * D2R));
  return turned(axis, c, at, a => R * Math.sqrt(Math.max(0, 1 - (a / R) ** 2)), 'gd_lknob', 'gd_ledge', {vFrom: R, vTo: -R}, '-+');
}
// Straight taper along Y from radius r0 at y0 down to r1 at y1 in n sections.
const taperY = (y0, y1, r0, r1, n, tex, ledge, V) => turned('y', [0, 0, 0], stations(y1, y0, n), y => r1 + (r0 - r1) * (y - y1) / (y0 - y1), tex, ledge, V);
// Left (gold) arm, model.md §3.4, ref.png and the binding feedback in plan.md: turned segments
// (no box corners from any side) under a wrap-round paint. Upper arm: a gold shoulder lame with a
// flared rim over a slim gold sleeve tapering to the elbow; forearm: a gold elbow flare, then a
// gauntlet tapering to the wrist whose side toward the viewer in most poses (azimuth about +45,
// see guardian_paint.mjs) glows amber with gold scrolls beside a gold back strip, a dark wrist
// wrap and a gold cuff. Smooth turned knobs round the shoulder and the elbow.
function lUpper() {
  const T = 'gd_lup', c = [0, 0, 0], V = {vFrom: 1.6, vTo: -7.9};
  return [
    ...knob('y', [0, -.1, 0], 1.5),
    ...lathe('y', c, [{a: [-3.2, -.6], r: 1.38, tex: T}, {a: [-3.36, -2.94], r: 1.47, tex: T}], V),
    disc('y', c, -3.36, 1.47 * DK, '-'),
    ...taperY(-3.1, -7.95, 1.28, 1.04, 6, T, 'gd_ledge_lup', V),
  ];
}
function lFore() {
  const T = 'gd_lfo', c = [0, 0, 0], V = {vFrom: 1.5, vTo: -7.7};
  return [
    ...knob('y', c, 1.38),
    ...lathe('y', c, [{a: [-1.9, -.9], r: 1.5, tex: T}], V), disc('y', c, -1.9, 1.5 * DK, '-'),
    ...taperY(-1.8, -6.1, 1.42, 1.06, 7, T, 'gd_ledge_lfo', V),
    ...lathe('y', c, [{a: [-6.86, -6.0], r: .95, tex: T}, {a: [-7.56, -6.8], r: 1.06, tex: T}], V),
    disc('y', c, -6.8, 1.06 * DK, '+'), disc('y', c, -7.56, 1.06 * DK, '-'),
  ];
}
// ---- left claw: slender gold talons -------------------------------------------------------
// Thin finger segment: a w x t box hanging from the joint J along -Y before its rotation about J;
// it reaches 0.16 above J into the previous segment so bent joints stay closed.
const phalanx = (J, L, w, t, rot) => abox([J[0] - w / 2, J[1] - L, J[2] - t / 2], [J[0] + w / 2, J[1] + .16, J[2] + t / 2], {all: 'gd_lfinger'},
  {rot: rot ? [rot[0], rot[1], J] : undefined, drop: ['up']});
// Finger from the knuckle K: the first segment fans out (rotation about Z), the next two and the
// painted talon curl toward the palm (-Z) by 22.5, 45 and 45 degrees plus the talon's own hook.
function talonFinger(K, fan, [L1, L2, L3], TL, s = 1) {
  const e = [phalanx(K, L1, .42 * s, .38 * s, fan ? ['z', fan] : null)];
  const P1 = vadd(K, [L1 * Math.sin(fan * D2R), -L1 * Math.cos(fan * D2R), 0]);
  e.push(phalanx(P1, L2, .34 * s, .3 * s, ['x', 22.5]));
  const P2 = vadd(P1, [0, -L2 * Math.cos(22.5 * D2R), -L2 * Math.sin(22.5 * D2R)]);
  e.push(phalanx(P2, L3, .27 * s, .24 * s, ['x', 45]));
  const P3 = vadd(P2, [0, -L3 * Math.SQRT1_2, -L3 * Math.SQRT1_2]);
  e.push(...talonPair('gd_talon_gold', P3[0], P3[2], P3[1] + .12, P3[1] - TL, .2 * s, ['x', 45, P3]));
  return e;
}
// Back-of-hand plate: the painted plate sprite on two cards that meet in a ridge at x = 0 and
// turn their outer edges 22.5 degrees toward the palm (a shallow sculpted roof), plus the palm.
function handPlate(z, Y0, Y1, palmZ) {
  const R = {X0: -1.4, X1: 1.4, Y0, Y1}, my = (Y0 + Y1) / 2;
  return [
    cardZ('gd_lhand', z, {...R, X0: 0}, {uvr: [.5, 0, 1, 1], rot: ['y', 22.5, [0, my, z]]}),
    cardZ('gd_lhand', z, {...R, X1: 0}, {uvr: [0, 0, .5, 1], rot: ['y', -22.5, [0, my, z]]}),
    cardZ('gd_lpalm', palmZ, {X0: -1.3, X1: 1.3, Y0: Y0 + .05, Y1: Y1 - .05}),
  ];
}
// Open claw (her left hand): wrist at the pivot, fingers toward -Y, palm toward -Z, the thumb on
// +X (a left hand's thumb side for that palm), index to pinky from +X to -X, the outer fingers
// fanned 22.5 degrees like the ref's bird-foot talons.
function lClawOpen() {
  const e = handPlate(.42, -2.7, .35, -.18);
  for (const [x, fan, L, TL, s] of [[-.97, -22.5, [1.15, .8, .62], 1.1, .86], [-.33, 0, [1.35, .9, .7], 1.25, .96], [.31, 0, [1.4, .92, .72], 1.3, 1], [.95, 22.5, [1.28, .86, .68], 1.2, .94]])
    e.push(...talonFinger([x, -2.38, .12], fan, L, TL, s));
  const R = [1.0, -.8, -.1], T1 = vadd(R, [.95 * Math.SQRT1_2, -.95 * Math.SQRT1_2, 0]), T2 = vadd(T1, [.7 * Math.sin(22.5 * D2R), -.7 * Math.cos(22.5 * D2R), 0]);
  e.push(phalanx(R, .95, .4, .36, ['z', 45]), phalanx(T1, .7, .32, .28, ['z', 22.5]));
  e.push(...talonPair('gd_talon_gold', T2[0], T2[2], T2[1] + .1, T2[1] - 1.05, .18, ['x', 45, T2]));
  return e;
}
// Finger ring round the spear shaft (the X axis through Y -2.24): box slabs one facet wide at
// the azimuths ks (0 = front -Z, 90 = up), w wide along X; widths alternate by 0.05 so the side
// faces of neighbouring slabs never share a plane.
const SHAFT_Y = -2.24;
function ringArc(x, w, rIn, rOut, ks) {
  const dirs = [[0, 0, -1], [0, 1, 0], [0, 0, 1], [0, -1, 0]], C = [x, SHAFT_Y, 0], wt = 2 * rOut * Math.tan(Math.PI / 16) + .02, T = {tex: 'gd_lfinger'};
  const lo = Math.min(...ks), hi = Math.max(...ks);
  return ks.map((k, i) => {
    const phi = (((k % 16) + 16) % 16) * 22.5, q = Math.round(phi / 90), g = phi - 90 * q, d = dirs[q % 4], t = dirs[(q + 1) % 4], hw = w / 2 + (i % 2 ? .025 : 0);
    const P = (dx, rr, s) => vadd(vadd(C, [dx, 0, 0]), vadd(vsc(d, rr), vsc(t, s)));
    const faces = {[faceOfDir(d)]: T, left: T, right: T};
    if (k === lo) faces[faceOfDir(vsc(t, -1))] = T;
    if (k === hi) faces[faceOfDir(t)] = T;
    const sg = vdot(rotA('x', 10, d), t) > 0 ? 1 : -1;
    return faceEl([P(-hw, rIn, -wt / 2), P(hw, rOut, wt / 2)], faces, {rot: g ? ['x', sg * g, C] : undefined});
  });
}
// Talon pointing up from its root (y0) toward y1, tilted back by `rot` (fist claws hooking over
// the shaft toward the palm).
const talonUp = (x, z, y0, y1, w, rot) => [
  cardX('gd_talon_gold', x, {Z0: z - w, Z1: z + w, Y0: y0, Y1: y1}, {rot, uvr: [0, 1, 1, 0]}),
  cardZ('gd_talon_gold', z, {X0: x - w, X1: x + w, Y0: y0, Y1: y1}, {rot, uvr: [0, 1, 1, 0]}),
];
// Fist round the shaft (two-hand grips): the plate behind the shaft, four fingers wrapping from
// the back under the shaft to its top-front with short claws hooking back over it, the thumb
// wrapping over the top from the other side.
function lClawFist() {
  const e = handPlate(.98, -2.85, .3, .6);
  const fing = [[-.95, .44], [-.32, .5], [.31, .5], [.93, .46]];
  for (const [x, w] of fing) {
    e.push(...ringArc(x, w, .6, 1.0, [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]));
    const a = 56.25 * D2R, root = [x, SHAFT_Y + .8 * Math.sin(a), -.8 * Math.cos(a)];
    e.push(...talonUp(x, root[2], root[1] - .1, root[1] + .85, .17, ['x', 45, root]));
  }
  e.push(...ringArc(1.5, .42, .6, .98, [2, 3, 4, 5, 6]));
  const a = 33.75 * D2R, tip = [1.5, SHAFT_Y + .8 * Math.sin(a), -.8 * Math.cos(a)];
  e.push(...talonPair('gd_talon_gold', tip[0], tip[2], tip[1] + .1, tip[1] - .85, .16, ['x', 22.5, tip]));
  return e;
}
// Shield brace (her left shoulder): a smooth gold pauldron dome turned about the brace axis
// (painted lame grooves) that flows into a slim round rod out to a hinge disc on the shield rim,
// and a painted swept gold fin above the rod with a spur below it that carries the black 4-point
// star (the wing-root ornament). The fin and the rod stay clear of the shield card,
// which lies in this part's z = 0 plane from about x = 6.7 (model units) outward.
function bracket() {
  const P = 'gd_paul', V = {vFrom: -1.0, vTo: 6.4};
  // half-ellipsoid dome (r 2.25 at x = -0.3, closing at x = 3.1) that flows into the 0.62 rod
  const dome = x => Math.max(.62, 2.25 * Math.sqrt(Math.max(0, 1 - ((x + .3) / 3.4) ** 2)));
  return [
    ...turned('x', [0, 0, 0], [...stations(-.95, 2.95, 13), 6.4], dome, P, 'gd_ledge_paul', V, '-'),
    ...lathe('z', [6.4, 0, 0], [{a: [-.78, .78], r: 1.28, tex: 'gd_lknob'}], {vFrom: .78, vTo: -.78}),
    plate('gd_joint', 6.4, 0, 2.7, -.8), plate('gd_joint', 6.4, 0, 2.7, .8),
    cardZ('gd_brace_fin', 0),
    plate('gd_blackstar', 5.5, -2.55, 2.5, -.45), plate('gd_blackstar', 5.5, -2.55, 2.5, .45),
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
const cubesC = () => [cube([0, 0, 0], 1.8, 'gd_corrupt', ['y', 22.5]), cube([-2.2, 1.6, .6], 1.4, 'gd_vox'), cube([1.6, 2.6, -.8], 1.1, 'gd_corrupt_b', ['x', 45]),
  cube([-3.6, -.6, -.6], 1.2, 'gd_vox', ['z', 22.5])];

// name -> elements. Variants share the display of their part (item model swaps).
export function partModels() {
  return {
    pelvis: pelvis(), skirt_f: skirtFront(), skirt_o: skirtOuter(), tail: tail(), leg_r: legVox(-1), leg_l: legVox(1),
    torso: torso(), head: head(), halo: halo(), halo_glow: haloGlow(),
    r_upper: rUpper(), r_fore: rFore(), r_hand_fist: clawFist(), r_hand_open: clawOpen(),
    l_upper: lUpper(), l_fore: lFore(), l_hand_open: lClawOpen(), l_hand_fist: lClawFist(),
    bracket: bracket(), shield: shield(), shield_eye: shieldEye(), shield_eye_t: shieldEyeTinted(),
    wing_cov: wingTier('gd_wing_cov', -.9), wing_sec: wingTier('gd_wing_sec', 0), wing_pri: wingTier('gd_wing_pri', .8),
    spear: spear(false), spear_e: spear(true), spear_glow: spearGlow(), trail: trail(),
    cubes_a: cubesA(), cubes_c: cubesC(),
    ...Object.fromEntries(Array.from({length: CUBES_B_VARIANTS}, (_, v) => [v ? 'cubes_b_' + v : 'cubes_b', trailVox(v)])),
  };
}
// Mirror a hand for the other side is not needed: the left hand has its own gold models.
export function checkBounds(name, els) {
  for (const e of els) for (const v of [...e.from, ...e.to]) if (v < -16 || v > 32) throw new Error(`model ${name} leaves -16..32: ${e.from} ${e.to}`);
}
