// Item models of the 타키 (Tachy) rig (S:tk/PLAN.md §2.1-2.3; footage ref/model_a.jpg, v2 6.0-16.4, v8 6.2, v9 1.5).
// Every model is authored in BLOCKS in the A-frame of its part (+X = her LEFT, +Y up, -Z forward; the joint at the
// origin, the rest orientation of the part = torso upright, limbs hanging along -Y, feet along -Z, the sword's blade
// along +Y with its edge toward -Z) and converted once by toUnits(els, PART_SCALE) (mboss_shape_lib.mjs).
//
// Proportions (2.25 b to the helmet top, ×1.25 the player): pelvis centre 1.10, waist 1.20, chest base 1.44, shoulder
// joints 1.71 (top of the pauldrons 1.80), neck 1.79, head pivot (jaw) 1.87, head top 2.13, helmet top 2.24, hip joints
// 1.03, knees 0.55, ankles 0.085; arms 0.32 + 0.29 (left) / 0.31 (right gauntlet); the long sword 2.30 (grip 0.40,
// guard Ø 0.24, blade 1.90); the cape (folded wings) 0.95 × 1.55 from the shoulder blades to 0.12 above the floor;
// spread wings 3 segments 0.95 / 0.95 / 0.80 each side (span ≈ 5.8 b), chord 1.3.
import {abox, cardZ, cardX, faceEl, mirrorModel, checkBounds} from './mboss_model_lib.mjs';
import {loft, toUnits, rockBox} from './mboss_shape_lib.mjs';

// ---- parts (api.PARTS order) -----------------------------------------------------------------------------------------------
// [name, default model, block brightness, display scale]
export const PARTS = [
  ['pelvis', 'pelvis', 13, 1], ['abdomen', 'abdomen', 13, 1], ['chest', 'chest', 13, 1], ['chest_glow', 'empty', 15, 1],
  ['neck', 'neck', 13, 1], ['head', 'head', 13, 1], ['hair_top', 'hair_top', 13, 1], ['hair_1', 'hair_1', 13, 1],
  ['hair_2', 'hair_2', 13, 1], ['hair_3', 'hair_3', 13, 1], ['helmet', 'helmet', 13, 1], ['visor_glow', 'empty', 15, 1],
  ['collar', 'collar', 13, 1], ['shoulder_l', 'shoulder_l', 14, 1], ['upper_arm_l', 'upper_arm_l', 13, 1],
  ['forearm_l', 'forearm_l', 13, 1], ['hand_l', 'hand_l_open', 13, 1], ['shoulder_r', 'shoulder_r', 13, 1],
  ['upper_arm_r', 'upper_arm_r', 13, 1], ['forearm_r', 'forearm_r', 13, 1], ['hand_r', 'hand_r_grip', 13, 1],
  ['spine_pack', 'spine_pack', 13, 1], ['tassets', 'tassets', 13, 1], ['thigh_l', 'thigh_l', 13, 1], ['shin_l', 'shin_l', 13, 1],
  ['foot_l', 'foot_l', 13, 1], ['thigh_r', 'thigh_r', 13, 1], ['shin_r', 'shin_r', 13, 1], ['foot_r', 'foot_r', 13, 1],
  ['wing_l1', 'cape_l1', 13, 1], ['wing_l2', 'cape_l2', 13, 1], ['wing_l3', 'cape_l3', 13, 1],
  ['wing_r1', 'cape_r1', 13, 1], ['wing_r2', 'cape_r2', 13, 1], ['wing_r3', 'cape_r3', 13, 1],
  ['sword', 'sword', 13, 1.5], ['sword_edge', 'empty', 15, 1.5], ['scabbard', 'scabbard_full', 13, 1.5],
  ['tendril_l', 'tendril', 12, 1.25], ['tendril_r', 'tendril', 12, 1.25],
];
export const PART_NAMES = PARTS.map(p => p[0]);
export const PART_SCALE = Object.fromEntries(PARTS.map(p => [p[0], p[3]]));
export const PART_BRIGHT = Object.fromEntries(PARTS.map(p => [p[0], p[2]]));
export const WINGS = ['wing_l1', 'wing_l2', 'wing_l3', 'wing_r1', 'wing_r2', 'wing_r3'];
export const TENDRILS = ['tendril_l', 'tendril_r'];

// ---- look -> item model per part (the rig's look channels; S:tk/contract.md §3.2, api.LOOKS) -----------------------------
export const FORM_MODELS = {
  cape: Object.fromEntries(WINGS.map(w => [w, w.replace('wing_', 'cape_')])),
  winged: Object.fromEntries(WINGS.map(w => [w, w])),
  abyss: Object.fromEntries(WINGS.map(w => [w, w + '_a'])),
};
export const VISOR_MODELS = {up_off: 'empty', down_off: 'empty', down_pyro: 'skull_p', down_electro: 'skull_e', down_abyss: 'skull_a'};
export const EDGE_MODELS = {off: 'empty', yellow: 'edge_y', pyro: 'edge_p', electro: 'edge_e', glint: 'edge_g'};
export const CHEST_MODELS = {off: 'empty', amber: 'grid_a', red: 'grid_r', gold: 'grid_g'};
export const HAND_MODELS = {
  hand_l: {open: 'hand_l_open', grip: 'hand_l_grip', fist: 'hand_l_grip'},
  hand_r: {open: 'hand_r_open', grip: 'hand_r_grip', fist: 'hand_r_fist'},
};
export const SCABBARD_MODELS = {full: 'scabbard_full', empty: 'scabbard'};
// tinted item definitions over a grey glow model: item -> [model, rgb]
export const TINTED = {
  skull_p: ['skull', 0xFFB21E], skull_e: ['skull', 0xFFF0A0], skull_a: ['skull', 0xFF3A2A],
  grid_a: ['grid', 0xFFB040], grid_r: ['grid', 0xFF3A2A], grid_g: ['grid', 0xFFE070],
  edge_y: ['edge', 0xFFE35A], edge_g: ['edge', 0xFFF6C8],
};

// ---- helpers (blocks) -----------------------------------------------------------------------------------------------------
const box = (a, b, tex, opt) => rockBox(a, b, tex, opt);
// a lofted segment along -Y from y0 (top) to y1 (bottom): radii [left, front, right, back] or r, per station
const limb = (sts, tex, opt = {}) => loft('y', sts.map(([a, r, c]) => ({a, r, c: c || [0, 0]})), {n: opt.n || 16, tex, caps: opt.caps ?? '-+', seed: opt.seed || 0});
const ell = (l, f, r = l, b = f) => [l, f, r, b];
// one-sided card (a single face) in the plane z: face 'front' (seen from -Z) or 'back' (seen from +Z)
function cardZ1(sprite, z, {X0, X1, Y0, Y1}, side = 'back', {flipU = false, rot, tint = false} = {}) {
  const fn = P => { let s = (P[0] - X0) / (X1 - X0); if (side === 'back') s = 1 - s; if (flipU) s = 1 - s; return [16 * s, 16 * (Y1 - P[1]) / (Y1 - Y0)]; };
  const el = faceEl([[X0, Y0, z], [X1, Y1, z]], {[side]: {tex: sprite, fn}}, {shade: false, rot});
  if (tint) for (const f of Object.values(el.faces)) f.tintindex = 0;
  return el;
}
const tinted = els => { for (const e of els) for (const f of Object.values(e.faces)) f.tintindex = 0; return els; };
// ring light: a small disc card facing direction ('left' = +X, 'right' = -X, 'front' = -Z, 'back' = +Z) at c, size s
function ringLight(c, s, face) {
  const [x, y, z] = c, h = s / 2;
  if (face === 'front' || face === 'back') return cardZ1('ring', z, {X0: x - h, X1: x + h, Y0: y - h, Y1: y + h}, face);
  const fn = P => [16 * ((face === 'left' ? -1 : 1) * (P[2] - z) / s + .5), 16 * ((y + h - P[1]) / s)];
  return faceEl([[x, y - h, z - h], [x, y + h, z + h]], {[face]: {tex: 'ring', fn}}, {shade: false});
}

// ---- body ------------------------------------------------------------------------------------------------------------------
function pelvis() {
  // pivot = pelvis centre (1.10 b): wide hips (-0.13 .. +0.10), the yellow Y down to the crotch on the front card
  const e = limb([[.10, ell(.15, .095, .15, .11)], [.03, ell(.185, .11, .185, .135)], [-.06, ell(.195, .105, .195, .15)], [-.13, ell(.13, .075, .13, .1)]], 'tk_suit', {n: 16});
  e.push(cardZ1('pelvis_front', -.112, {X0: -.13, X1: .13, Y0: -.13, Y1: .085}, 'front'));
  // belt: gunmetal band with a gold buckle plate
  e.push(...limb([[.10, ell(.158, .1, .158, .118)], [.06, ell(.172, .107, .172, .128)]], 'tk_metal_dk', {n: 16}));
  e.push(box([-.045, .055, -.118], [.045, .1, -.098], 'tk_gold'));
  return e;
}
function abdomen() {
  // pivot = waist (1.20); a narrow waist up to the chest base (1.44)
  const e = limb([[-.02, ell(.15, .098, .15, .112)], [.1, ell(.128, .09, .128, .1)], [.25, ell(.15, .1, .15, .11)]], 'tk_suit', {n: 16});
  e.push(cardZ1('abdomen_front', -.097, {X0: -.1, X1: .1, Y0: -.02, Y1: .25}, 'front'));
  // silver hex plates on her left flank (v9 1.5, v2 13.0) and a darker pair on the right
  e.push(box([.11, .0, -.06], [.15, .2, .07], 'tk_hex'), box([-.145, .04, -.03], [-.12, .18, .07], 'tk_hex_dk'));
  return e;
}
function chest() {
  // pivot = chest base (1.44); shoulders at +0.27, top +0.35; the bust, the yellow tie between it (chest_front card)
  const e = limb([[-.02, ell(.15, .1, .15, .11)], [.09, ell(.175, .11, .175, .12)], [.2, ell(.205, .115, .205, .13)], [.28, ell(.215, .1, .215, .13)], [.35, ell(.14, .075, .14, .09)]], 'tk_suit', {n: 16});
  e.push(cardZ1('chest_front', -.117, {X0: -.1, X1: .1, Y0: -.01, Y1: .33}, 'front'));
  for (const s of [1, -1]) e.push(...loft('z', [{a: -.152, r: [.035, .03, .035, .04], c: [s * .085, .158]}, {a: -.138, r: [.06, .05, .06, .06], c: [s * .086, .162]}, {a: -.09, r: [.068, .058, .068, .066], c: [s * .087, .166]}], {n: 16, tex: 'tk_black', caps: '-+'}));
  // side ribs: hex plates on the left side, gunmetal plates on the right
  e.push(box([.18, .02, -.07], [.215, .22, .09], 'tk_hex'), box([-.215, .02, -.05], [-.18, .22, .1], 'tk_metal'));
  // back plate under the spine pack
  e.push(box([-.16, .06, .1], [.16, .32, .135], 'tk_metal_dk'));
  return e;
}
function neck() { return limb([[-.02, .055], [.10, .05]], 'tk_suit', {n: 8}); }
function head() {
  // pivot = jaw / neck top (1.87): face, skull, ears hidden under the hair
  const e = limb([[0, ell(.055, .07, .055, .05), [0, .015]], [.05, ell(.085, .1, .085, .09), [0, .01]], [.13, ell(.098, .11, .098, .11)], [.21, ell(.09, .1, .09, .105)], [.26, ell(.05, .06, .05, .06)]], 'tk_skin', {n: 16});
  e.push(cardZ1('face', -.112, {X0: -.088, X1: .088, Y0: .0, Y1: .2}, 'front'));
  return e;
}
function hairTop() {
  // scalp cap (slightly over the skull), side locks framing the face, a parted fringe; the long hair hangs from hair_1
  const e = limb([[.12, ell(.105, .1, .105, .125), [0, -.005]], [.2, ell(.103, .105, .103, .123)], [.25, ell(.08, .08, .08, .1)], [.285, ell(.03, .03, .03, .04)]], 'tk_hair', {n: 16});
  e.push(...limb([[.13, ell(.1, .02, .1, .12), [0, -.01]], [.03, ell(.085, .01, .085, .11), [0, -.02]]], 'tk_hair', {n: 16, caps: ''}));
  for (const s of [1, -1]) {
    e.push(cardX('hair_lock', .1 * s, {Z0: -.1, Z1: .06, Y0: -.16, Y1: .2}, {flipU: s < 0}));
    e.push(cardZ('hair_lock', -.095, {X0: s > 0 ? .055 : -.105, X1: s > 0 ? .105 : -.055, Y0: -.12, Y1: .2}, {flipU: s < 0}));
  }
  e.push(cardZ1('hair_fringe', -.118, {X0: -.1, X1: .1, Y0: .12, Y1: .245}, 'front'));
  return e;
}
// long hair: three flat locks hanging from the back of the head (each 0.26 wide, 0.25 long)
function hairSeg(i) {
  const w = [.13, .125, .11][i], w1 = [.125, .11, .07][i], L = .25;
  const e = limb([[0, ell(w, .03, w, .035)], [-L, ell(w1, .025, w1, .03)]], 'tk_hair', {n: 8, caps: ''});
  // the visible side faces away from her back: the pose turns the model's -Z (front) backward
  e.push(cardZ1('hair_back', -.036, {X0: -w - .01, X1: w + .01, Y0: -L - (i === 2 ? .1 : .02), Y1: .01}, 'front'));
  if (i === 2) e.push(cardZ1('hair_tip', -.03, {X0: -w1 - .02, X1: w1 + .02, Y0: -L - .12, Y1: -L + .04}, 'front'));
  return e;
}
function helmet() {
  // closed: a copper-red glossy dome round the head (pivot = the head pivot); the front facets of the middle sections are
  // the dark visor glass, ringed by a lit gold rim (v2 11.0-12.5, v9 1.5); a gold band at the neck line; it opens (hood)
  // by turning about a hinge behind the crown (pose channel helm)
  const st = [[-.015, ell(.112, .125, .112, .13)], [.035, ell(.132, .142, .132, .145)], [.1, ell(.147, .153, .147, .153)], [.165, ell(.145, .152, .145, .152)],
    [.215, ell(.133, .14, .133, .142)], [.26, ell(.11, .115, .11, .12)], [.3, ell(.07, .075, .07, .08)], [.325, ell(.025, .025, .025, .03)]];
  const visor = (k, th, i) => (i >= 1 && i <= 3 && th >= 45 && th <= 135 ? (th === 45 || th === 135 ? 'tk_gold' : 'tk_visor') : i === 4 && th >= 67.5 && th <= 112.5 ? 'tk_gold' : 'tk_copper');
  const e = loft('y', st.map(([a, r]) => ({a, r})), {n: 16, tex: visor, caps: '-+'});
  e.push(...limb([[-.03, ell(.118, .13, .118, .135)], [.0, ell(.12, .133, .12, .137)]], 'tk_gold', {n: 16, caps: ''}));
  // the crest ridge and the side discs (the yellow ring lights at the temples, v9 1.5)
  e.push(box([-.014, .25, -.06], [.014, .31, .12], 'tk_copper'), box([-.018, .29, -.02], [.018, .318, .09], 'tk_gold'));
  e.push(ringLight([.152, .1, .0], .085, 'left'), ringLight([-.152, .1, .0], .085, 'right'));
  return e;
}
function collar() {
  // pivot = neck base (chest top): a high collar of dark hex plates with gold edging
  const e = limb([[-.04, ell(.17, .12, .17, .14)], [.03, ell(.15, .11, .15, .13)], [.09, ell(.1, .08, .1, .1)]], 'tk_hex_dk', {n: 16});
  e.push(...limb([[.09, ell(.1, .08, .1, .1)], [.105, ell(.098, .078, .098, .098)]], 'tk_gold', {n: 16, caps: '+'}));
  return e;
}
// left shoulder (slim arm side): a rounded pauldron with an orange ring light on its outer face (v2 10.5)
function shoulderL() {
  const e = limb([[.11, ell(.06, .1, .07, .11), [.035, 0]], [.06, ell(.115, .13, .1, .13), [.035, 0]], [-.03, ell(.13, .135, .105, .135), [.035, 0]], [-.11, ell(.11, .115, .09, .115), [.035, 0]]], 'tk_metal', {n: 16});
  e.push(box([.13, -.1, -.1], [.165, .05, .1], 'tk_hex_dk'));
  e.push(ringLight([.168, -.02, .0], .11, 'left'));
  return e;
}
// right shoulder: the massive hex pauldron with two yellow bands (v2 6.0, 10.5)
function shoulderR() {
  const e = limb([[.16, ell(.08, .14, .1, .15), [-.06, 0]], [.1, ell(.155, .19, .14, .19), [-.06, 0]], [0, ell(.19, .2, .15, .2), [-.06, 0]], [-.11, ell(.185, .185, .14, .185), [-.06, 0]], [-.18, ell(.15, .14, .12, .14), [-.06, 0]]], 'tk_hex_dk', {n: 16});
  for (const y of [-.07, -.13]) e.push(...limb([[y + .025, ell(.19, .19, .145, .19), [-.06, 0]], [y, ell(.192, .192, .147, .192), [-.06, 0]]], 'tk_yellow', {n: 16, caps: ''}));
  e.push(box([-.26, -.06, -.14], [-.22, .1, .14], 'tk_metal'), ringLight([-.262, .02, 0], .1, 'right'));
  return e;
}
function upperArm(side) {
  const R = side > 0;
  const e = limb([[.02, R ? .055 : .066], [-.16, R ? .05 : .062], [-.32, R ? .043 : .055]], 'tk_suit', {n: 8});
  if (!R) for (const y of [-.1, -.17]) e.push(...limb([[y, .068], [y - .04, .066]], 'tk_yellow', {n: 8, caps: ''}));
  else e.push(box([.045, -.3, -.012], [.058, -.02, .012], 'tk_gold'));
  e.push(...limb([[-.29, R ? .052 : .063], [-.34, R ? .05 : .061]], 'tk_metal_dk', {n: 8}));   // elbow cop
  return e;
}
function forearmL() {
  const e = limb([[.0, .047], [-.15, .046], [-.29, .036]], 'tk_suit', {n: 8});
  e.push(...limb([[-.17, .05], [-.29, .042]], 'tk_metal', {n: 8}));
  e.push(box([.03, -.27, -.012], [.052, -.02, .012], 'tk_gold'));
  return e;
}
// right gauntlet: bulky armoured forearm with plates, yellow trim and an orange ring light (v2 6.0, 14.4)
function forearmR() {
  const e = limb([[.02, ell(.07, .075, .07, .075)], [-.12, ell(.085, .085, .08, .085)], [-.24, ell(.08, .08, .075, .08)], [-.31, ell(.06, .062, .058, .062)]], 'tk_metal_dk', {n: 16});
  e.push(box([-.105, -.25, -.06], [-.07, -.02, .06], 'tk_metal'), box([-.11, -.2, -.04], [-.1, -.08, .04], 'tk_yellow'));
  e.push(...limb([[-.03, ell(.075, .08, .075, .08)], [-.06, ell(.076, .081, .076, .081)]], 'tk_yellow', {n: 16, caps: ''}));
  e.push(ringLight([.0, -.14, -.088], .08, 'front'), ringLight([.088, -.14, 0], .08, 'left'));
  return e;
}
// hands hang along -Y from the wrist (pivot); 'grip': a fist round a grip along the hand's +Z.. the sword's axis runs
// through the fist centre 0.06 below the wrist along the hand frame's -Z (pose: the hand takes the sword frame)
function hand(side, kind, big) {
  const k = big ? 1.2 : 1, T = big ? 'tk_metal_dk' : 'tk_metal', e = [];
  if (kind === 'open') {
    e.push(box([-.045 * k, -.09 * k, -.02 * k], [.045 * k, 0, .022 * k], T));
    for (let i = 0; i < 4; i++) { const x = (-.033 + i * .022) * k; e.push(box([x - .009 * k, (-.16 + Math.abs(i - 1.5) * .012) * k, -.015 * k], [x + .009 * k, -.09 * k, .015 * k], 'tk_suit')); }
    e.push(box([side * .04 * k, -.075 * k, -.03 * k], [side * .062 * k, -.02 * k, .0], 'tk_suit'));
  } else {
    // fist (grip): the fist wraps a grip whose axis is the hand frame's Z through (0, -0.06, 0)
    e.push(box([-.048 * k, -.1 * k, -.04 * k], [.048 * k, 0, .04 * k], T));
    e.push(box([-.05 * k, -.11 * k, -.045 * k], [.05 * k, -.07 * k, .03 * k], 'tk_suit'));
    e.push(box([side * .035 * k, -.075 * k, -.055 * k], [side * .058 * k, -.035 * k, -.02 * k], 'tk_suit'));
  }
  if (big) e.push(box([-.052, -.045, .02], [.052, -.005, .05], 'tk_yellow'));
  return e;
}
function spinePack() {
  // pivot on the upper back (chest frame z +0.145): a flat mechanical spine column, hex plates, the wing mounts
  const e = [box([-.15, -.22, -.01], [.15, .19, .045], 'tk_hex_dk')];
  for (let i = 0; i < 6; i++) { const y = .16 - i * .072; e.push(box([-.03, y - .052, .035], [.03, y, .075], i % 2 ? 'tk_metal' : 'tk_metal_dk')); }
  for (const s of [1, -1]) e.push(box([s * .07, .03, .03], [s * .15, .16, .085], 'tk_metal'), box([s * .09, .12, .075], [s * .14, .17, .1], 'tk_gold'));
  e.push(box([-.015, -.19, .07], [.015, .17, .08], 'tk_yellow'));
  return e;
}
function tassets() {
  // pivot = pelvis centre: armoured hip plates on both sides and the back (front open: the yellow Y shows)
  const e = [];
  for (const s of [1, -1]) {
    e.push(box([s * .2, -.2, -.1], [s * .235, .07, .12], s > 0 ? 'tk_hex' : 'tk_metal_y', {rot: ['z', s * 22.5, [s * .2, .07, 0]]}));
    e.push(box([s * .17, -.12, -.13], [s * .215, .06, -.06], 'tk_metal', {rot: ['y', s * -22.5, [s * .19, 0, -.1]]}));
  }
  e.push(box([-.17, -.19, .12], [.17, .07, .155], 'tk_metal_dk', {rot: ['x', 22.5, [0, .07, .13]]}));
  e.push(box([-.15, -.205, .135], [.15, -.17, .16], 'tk_yellow', {rot: ['x', 22.5, [0, .07, .13]]}));
  return e;
}
function thigh(side) {
  const R = side < 0;
  const e = limb([[.03, ell(.085, .09, .08, .09)], [-.2, ell(.08, .085, .075, .085)], [-.42, ell(.062, .068, .06, .068)], [-.49, .056]], 'tk_suit', {n: 16});
  // outer armour plate with a yellow edge line, the inner seam
  e.push(box([side * .07, -.38, -.07], [side * .1, .0, .07], 'tk_metal_y'));
  if (R) e.push(...limb([[-.08, ell(.088, .093, .083, .093)], [-.14, ell(.089, .094, .084, .094)]], 'tk_yellow', {n: 16, caps: ''}));
  else e.push(box([side * .1, -.3, -.03], [side * .108, -.06, .03], 'tk_gold'));
  return e;
}
function shin(side) {
  // armoured greave; knee guard with the orange ring light (v2 8.0)
  const e = limb([[.04, ell(.07, .085, .07, .07)], [-.12, ell(.07, .08, .068, .072)], [-.3, ell(.06, .07, .058, .065)], [-.44, ell(.05, .055, .05, .055)], [-.47, .048]], 'tk_metal_dk', {n: 16});
  e.push(box([-.065, -.05, -.115], [.065, .08, -.06], 'tk_metal'), ringLight([0, .02, -.117], .07, 'front'));
  e.push(box([side * .06, -.36, -.04], [side * .077, -.08, .04], 'tk_metal'));
  return e;
}
function foot(side) {
  // pivot = ankle (0.085 above the sole): armoured boot toward -Z
  const e = [box([-.055, -.085, -.2], [.055, -.02, .07], 'tk_metal_dk'), box([-.05, -.03, -.17], [.05, .03, .06], 'tk_metal'),
    box([-.045, -.085, -.25], [.045, -.035, -.19], 'tk_metal'), box([-.06, -.02, .02], [.06, .06, .075], 'tk_metal_dk'),
    box([side * .052, -.06, -.12], [side * .062, .0, .0], 'tk_yellow')];
  return e;
}

// ---- cape (folded wings, P1) and wings ------------------------------------------------------------------------------------
// The left half; the right halves are mirror images. Segment i hangs along -Y from its joint: cape panels 0.52 / 0.52 /
// 0.51 long, spanning X -0.36 (toward her spine) .. +0.12 (outer edge, which wraps round her side by 22.5 deg).
const CAPE = [{L: .53, X0: -.14, X1: .32}, {L: .53, X0: -.14, X1: .34}, {L: .5, X0: -.14, X1: .36}];
function capeSeg(i) {
  const {L, X0, X1} = CAPE[i], s = 'cape_' + (i + 1), w = X1 - X0, sp = X0 + w * .72;
  const e = [cardZ(s, 0, {X0, X1: sp, Y0: -L - .01, Y1: .01}, {uvr: [0, 0, .72, 1]}),
    cardZ(s, 0, {X0: sp, X1, Y0: -L - .01, Y1: .01}, {uvr: [.72, 0, 1, 1], rot: ['y', 22.5, [sp, 0, 0]]})];
  if (i === 0) e.push(box([-.1, -.04, -.025], [.12, .03, .025], 'tk_metal_dk'));
  return e;
}
// winged: a metal arm bone along -Y (X 0..0.07) with the blade feathers fanning toward -X (down when spread); two
// layers 0.04 b apart for depth; segment lengths 0.95 / 0.95 / 0.80, chord 1.3
const WSEG = [{L: .95, C: 1.15}, {L: .95, C: 1.3}, {L: .8, C: 1.25}];
function wingSeg(i, abyss) {
  const {L, C} = WSEG[i], s = (abyss ? 'wing_a' : 'wing_') + (i + 1);
  const e = [cardZ(s, -.02, {X0: -C, X1: .1, Y0: -L - .04, Y1: .04}), cardZ(s + 'b', .025, {X0: -C + .04, X1: .1, Y0: -L - .02, Y1: .03})];
  e.push(box([-.01, -L, -.035], [.075, .0, .035], 'tk_metal_dk'), box([.06, -L * .9, -.03], [.085, -L * .1, .03], 'tk_gold'));
  if (abyss) e.push(box([-.06, -L * .8, -.05], [.0, -L * .2, .05], 'tk_flesh'));
  return e;
}
function tendril() {
  // dark red flesh tentacle 1.4 b along -Y from the wing root, black tip (crossed cards over a tapering core)
  const e = limb([[.02, .06], [-.4, .05], [-.8, .035], [-1.1, .02]], 'tk_flesh', {n: 8});
  e.push(cardZ('tendril', 0, {X0: -.09, X1: .09, Y0: -1.42, Y1: .02}), cardX('tendril', 0, {Z0: -.09, Z1: .09, Y0: -1.42, Y1: .02}));
  return e;
}

// ---- sword, edge, scabbard ------------------------------------------------------------------------------------------------
// pivot = the right hand's grip point; +Y toward the tip, the edge toward -Z, the serrated spine toward +Z, flats ±X.
export const SWORD = {gripLo: -.3, guard: [.05, .11], bladeLo: .11, tip: 2.0, twoHand: -.15};
function sword() {
  const e = limb([[-.3, .026], [.05, .024]], 'tk_suit', {n: 8});
  for (const y of [-.28, -.16, -.04]) e.push(...limb([[y, .03], [y + .018, .03]], 'tk_gold', {n: 8, caps: '-+'}));
  e.push(...limb([[-.34, .034], [-.3, .03]], 'tk_metal', {n: 8}));
  // guard: a round mechanical disc (its faces are the blade's flats) with the orange ring light
  e.push(...loft('x', [{a: -.032, r: .118}, {a: .032, r: .118}], {n: 16, tex: 'tk_metal_dk', caps: '-+'}));
  for (const s of [1, -1]) e.push(ringLight([s * .034, .0, 0], .2, s > 0 ? 'left' : 'right'));
  e.push(box([-.025, .1, -.075], [.025, .14, .09], 'tk_metal'));
  // blade: a stepped core (0.03 thick, tapering) and the painted flats (sword_blade: steel, yellow edge band, teeth)
  const Y = [.12, .7, 1.3, 1.75, 1.95];
  const W = [[-.065, .075], [-.06, .07], [-.055, .062], [-.045, .05], [-.03, .03]];
  for (let k = 0; k < Y.length - 1; k++) e.push(box([-.012, Y[k], W[k][0] + .01], [.012, Y[k + 1], W[k][1] - .02], 'tk_steel'));
  for (const s of [1, -1]) e.push(cardX('sword_blade', s * .0165, {Z0: -.075, Z1: .095, Y0: .11, Y1: 2.02}, {flipU: s < 0}));
  return e;
}
function edge() {
  // glow along the edge (-Z): a card in the blade plane and one across it; grey-white, tinted per look
  return tinted([cardX('edge', 0, {Z0: -.13, Z1: -.035, Y0: .12, Y1: 2.03}), cardZ('edge', -.068, {X0: -.035, X1: .035, Y0: .12, Y1: 2.03})]);
}
function edgeAnim(sp) {
  return [cardX(sp, 0, {Z0: -.17, Z1: -.03, Y0: .12, Y1: 2.05}), cardZ(sp, -.068, {X0: -.05, X1: .05, Y0: .12, Y1: 2.05})];
}
// scabbard: pivot = its mouth (at her right hip); the body runs +Y 1.95 b; 'full' shows the hilt below the mouth
function scabbard(full) {
  // sheathed (intro until the draw): a sheath rising from the right hip across the back under the cape (only the hilt at the
  // hip shows; the blade's length is hidden under the cape, the footage never shows a scabbard). Drawn: only the mouth
  // holster stays (a short mechanical clamp at the right hip).
  const L = full ? 1.15 : .34;
  const e = loft('y', full ? [{a: .0, r: [.03, .08, .03, .1]}, {a: .8, r: [.027, .075, .027, .09]}, {a: 1.05, r: [.022, .05, .022, .06]}, {a: L, r: [.012, .02, .012, .03]}]
    : [{a: .0, r: [.032, .085, .032, .1]}, {a: L, r: [.03, .08, .03, .095]}], {n: 8, tex: 'tk_black', caps: '-+'});
  for (const y of full ? [.02, .45, .95] : [.02, .27]) e.push(...loft('y', [{a: y, r: [.036, .088, .036, .106]}, {a: y + .05, r: [.036, .088, .036, .106]}], {n: 8, tex: 'tk_gold', caps: '-+'}));
  e.push(box([-.02, .08, .09], [.02, .24, .14], 'tk_metal_dk'));
  if (full) {
    // the sword's hilt below the mouth (the blade is inside): grip, gold bands, pommel, the guard disc
    e.push(...limb([[-.04, .026], [-.4, .024]], 'tk_suit', {n: 8}), ...limb([[-.4, .034], [-.44, .03]], 'tk_metal', {n: 8}));
    e.push(...loft('x', [{a: -.032, r: .11, c: [0, -.03]}, {a: .032, r: .11, c: [0, -.03]}], {n: 16, tex: 'tk_metal_dk', caps: '-+'}));
  }
  return e;
}

// ---- glow overlays ---------------------------------------------------------------------------------------------------------
function skull() {
  // inside the closed visor: the glowing skull (grey-white sprite, tinted per look), pivot = the head pivot
  return tinted([cardZ1('skull', -.153, {X0: -.105, X1: .105, Y0: .0, Y1: .23}, 'front')]);
}
function grid() {
  // the 3x3 light grid on the upper sternum + the core under it (pivot = chest base)
  return tinted([cardZ1('grid', -.121, {X0: -.05, X1: .05, Y0: .215, Y1: .315}, 'front')]);
}

// ---- assembly ---------------------------------------------------------------------------------------------------------------
// models in blocks (before toUnits), keyed by item model name; the display scale of each comes from the part using it
function blockModels() {
  const M = {};
  M.empty = [];
  M.pelvis = pelvis(); M.abdomen = abdomen(); M.chest = chest(); M.neck = neck(); M.head = head(); M.hair_top = hairTop();
  for (let i = 0; i < 3; i++) M['hair_' + (i + 1)] = hairSeg(i);
  M.helmet = helmet(); M.collar = collar();
  M.shoulder_l = shoulderL(); M.shoulder_r = shoulderR();
  M.upper_arm_l = upperArm(1); M.upper_arm_r = upperArm(-1); M.forearm_l = forearmL(); M.forearm_r = forearmR();
  M.hand_l_open = hand(1, 'open', false); M.hand_l_grip = hand(1, 'grip', false);
  M.hand_r_open = hand(-1, 'open', true); M.hand_r_grip = hand(-1, 'grip', true); M.hand_r_fist = hand(-1, 'fist', true);
  M.spine_pack = spinePack(); M.tassets = tassets();
  for (const [s, k] of [[1, 'l'], [-1, 'r']]) { M['thigh_' + k] = thigh(s); M['shin_' + k] = shin(s); M['foot_' + k] = foot(s); }
  for (let i = 0; i < 3; i++) {
    M['cape_l' + (i + 1)] = capeSeg(i); M['cape_r' + (i + 1)] = mirrorModel(capeSeg(i));
    M['wing_l' + (i + 1)] = wingSeg(i, false); M['wing_r' + (i + 1)] = mirrorModel(wingSeg(i, false));
    M['wing_l' + (i + 1) + '_a'] = wingSeg(i, true); M['wing_r' + (i + 1) + '_a'] = mirrorModel(wingSeg(i, true));
  }
  M.tendril = tendril();
  M.sword = sword(); M.edge = edge(); M.edge_p = edgeAnim('edge_fire'); M.edge_e = edgeAnim('edge_volt');
  M.scabbard = scabbard(false); M.scabbard_full = scabbard(true);
  M.skull = skull(); M.grid = grid();
  // the intro cable prop: a unit segment along +Y (display scale [w, length, w]), centred on its axis
  M.cable = [box([-.5, 0, -.5], [.5, 1, .5], 'tk_black')];
  return M;
}
// the display scale a model is shown at (the part that uses it)
export const MODEL_SCALE = {sword: 1.5, edge: 1.5, edge_p: 1.5, edge_e: 1.5, scabbard: 1.5, scabbard_full: 1.5, tendril: 1.25};
export const TINTED_MODELS = new Set(['skull', 'grid', 'edge']);
export function allModels() {
  const B = blockModels(), M = {};
  for (const [n, els] of Object.entries(B)) { M[n] = toUnits(els, MODEL_SCALE[n] || 1); checkBounds(n, M[n]); }
  return M;
}
// A-frame model points (blocks, part space at display scale 1 x PART_SCALE applied by the caller) of every element's corners
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
      out.push([8 - P[0], P[1] - 8, P[2] - 8]);
    }
  }
  return out;
}
