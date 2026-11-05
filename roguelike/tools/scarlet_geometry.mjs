// Item models of the 홍련 (Scarlet) rig (S:hr/PLAN.md §2.1-2.3; an ORIGINAL design, §1.5 / §2.2: a Joseon wandering
// swordswoman with a red-lotus motif). Every model is authored in BLOCKS in the A-frame of its part (+X = her LEFT, +Y up,
// -Z forward; the joint at the origin; the rest orientation of the part = torso upright, limbs hanging along -Y, feet
// along -Z, the sword / scabbard along +Y with the edge toward -Z) and converted once by toUnits(els, PART_SCALE)
// (mboss_shape_lib.mjs). Elements stay inside -16..32 with one rotation axis of -45 / -22.5 / 0 / 22.5 / 45 (RP README §4).
//
// Proportions (2.55 b to the head top; PLAN §2.1): sole 0, ankle 0.10, knee 0.68, hip joints 1.28, pelvis pivot 1.36,
// waist (torso pivot) 1.50, shoulder joints 1.93, neck base (head pivot) 2.05, chin 2.17, eyes 2.36, head top 2.55; hat
// brim centre 2.50 (crown top 2.81, brim D 1.60); arms 0.40 + 0.34 (+ hand, grip 0.08 below the wrist); thighs 0.60,
// shins 0.58; the robe skirt from the belt (1.40) to mid-shin (0.40), flaring 0.42 -> 0.80; sword 2.10 (grip 0.33, guard
// D 0.13, blade 1.75), scabbard 1.82.
import {abox, cardZ, cardX, cardY, faceEl, mirrorModel, checkBounds, lathe, disc} from './mboss_model_lib.mjs';
import {loft, toUnits, rockBox, retex, registerTile, registerWrap} from './mboss_shape_lib.mjs';

// ---- parts (api.PARTS order) -----------------------------------------------------------------------------------------------
// [name, default model, block brightness, display scale]
export const PARTS = [
  ['pelvis', 'pelvis', 13, 1], ['torso', 'torso', 13, 1], ['head', 'head', 13, 1], ['face', 'face_calm', 13, 1],
  ['hair_tail_1', 'hair_tail_1', 13, 1], ['hair_tail_2', 'hair_tail_2', 13, 1], ['lock_r', 'lock_r', 13, 1], ['lock_l', 'lock_l', 13, 1],
  ['arm_r', 'arm_r', 13, 1], ['forearm_r', 'forearm_r_open', 13, 1], ['arm_l', 'arm_l', 13, 1], ['forearm_l', 'forearm_l_grip', 13, 1],
  ['thigh_r', 'thigh_r', 13, 1], ['shin_r', 'shin_r', 13, 1], ['thigh_l', 'thigh_l', 13, 1], ['shin_l', 'shin_l', 13, 1],
  ['skirt_fl', 'skirt_fl', 13, 1], ['skirt_fr', 'skirt_fr', 13, 1], ['skirt_bl', 'skirt_bl', 13, 1], ['skirt_br', 'skirt_br', 13, 1],
  ['sash_tails', 'sash_p1', 13, 1], ['hat', 'hat_p1', 13, 1], ['hat_strings', 'hat_strings', 13, 1],
  ['sword', 'sword', 13, 1.5], ['sword_glow', 'empty', 15, 1.5], ['scabbard', 'scabbard', 13, 1.5], ['hilt_sheathed', 'hilt', 13, 1.5],
  ['cup', 'cup', 13, 1], ['bottle', 'bottle', 13, 1],
];
export const PART_NAMES = PARTS.map(p => p[0]);
export const PART_SCALE = Object.fromEntries(PARTS.map(p => [p[0], p[3]]));
export const PART_BRIGHT = Object.fromEntries(PARTS.map(p => [p[0], p[2]]));
export const DEFAULT_MODEL = Object.fromEntries(PARTS.map(p => [p[0], p[1]]));

// ---- looks -> item models (api.LOOKS, HANDS) -----------------------------------------------------------------------------
export const HAND_MODELS = {
  forearm_r: {open: 'forearm_r_open', grip: 'forearm_r_grip', brim: 'forearm_r_brim'},
  forearm_l: {open: 'forearm_l_open', grip: 'forearm_l_grip', brim: 'forearm_l_brim'},
};
export const FACE_MODELS = {calm: 'face_calm', smile: 'face_smile', closed: 'face_closed'};
export const PHASE_MODELS = {hat: {p1: 'hat_p1', p2: 'hat_p2'}, sash_tails: {p1: 'sash_p1', p2: 'sash_p2'}};
export const BLADE_MODELS = {off: 'empty', lilac: 'glow_lilac', pink: 'glow_pink', violet: 'glow_violet', gold: 'glow_gold'};
// the ghost twin of a model (same geometry, every face the texture rlk:mboss/scarlet/ghost); glows / empty have none
export const ghostOf = m => (m === 'empty' || m.startsWith('glow_') ? m : m + '_g');
export const GHOST_TEX = 'ghost';
// the brim's underside carries tintindex 0: the item definitions of the hat models darken it (one shared sprite)
export const TINTS = {hat_p1: 0x6A6470, hat_p2: 0x6A6470};

// ---- tiles (texel density per block for the lofted / boxed parts) -----------------------------------------------------------
// [w, h, px per block]; WRAP sprites map u round a loft and v along its whole length (bands at fixed places)
export const TILE_SIZES = {
  robe: [32, 32, 40], robe_in: [16, 16, 32], vest: [32, 32, 40], crimson: [16, 16, 48], trouser: [16, 16, 32],
  boot: [16, 16, 32], sole: [16, 16, 32], skin: [16, 16, 48], hair: [32, 32, 48], brass: [16, 16, 64], iron: [16, 16, 64],
  lacquer: [16, 16, 48], steel: [16, 16, 64], porcelain: [16, 16, 96],
};
export const WRAP_SPRITES = {wrap: [32, 32], guard_arm: [32, 32], sash: [32, 16], crown: [64, 32], grip: [16, 32]};
for (const [n, [w, h, ppb]] of Object.entries(TILE_SIZES)) registerTile(n, w, h, ppb);
for (const n of Object.keys(WRAP_SPRITES)) registerWrap(n);

// ---- helpers (blocks) -----------------------------------------------------------------------------------------------------
const box = (a, b, tex, opt) => rockBox(a, b, tex, opt);
const ell = (l, f, r = l, b = f) => [l, f, r, b];
// a lofted segment along Y: stations [y, r | [left, front, right, back], c?]
const limb = (sts, tex, opt = {}) => loft('y', sts.map(([a, r, c]) => ({a, r, c: c || [0, 0]})), {n: opt.n || 16, tex, caps: opt.caps ?? '-+', seed: opt.seed || 0, stagger: opt.stagger ?? .004});
// one-sided card (a single face) in the plane z: 'front' (seen from -Z) or 'back' (seen from +Z)
function card1(sprite, z, {X0, X1, Y0, Y1}, side = 'front', {flipU = false, rot, uvr = [0, 0, 1, 1]} = {}) {
  const fn = P => { let s = (P[0] - X0) / (X1 - X0); if (side === 'back') s = 1 - s; if (flipU) s = 1 - s;
    return [16 * (uvr[0] + (uvr[2] - uvr[0]) * s), 16 * (uvr[1] + (uvr[3] - uvr[1]) * (Y1 - P[1]) / (Y1 - Y0))]; };
  return faceEl([[X0, Y0, z], [X1, Y1, z]], {[side]: {tex: sprite, fn}}, {shade: false, rot});
}
// a one-sided card whose sprite spans the global X range gx0..gx1 (a strip of a wider card, turned by rot about its pivot)
function strip1(sprite, z, {X0, X1, Y0, Y1}, side, gx0, gx1, rot, shade = false) {
  const fn = P => { let s = (P[0] - gx0) / (gx1 - gx0); if (side === 'back') s = 1 - s; return [16 * s, 16 * (Y1 - P[1]) / (Y1 - Y0)]; };
  return faceEl([[X0, Y0, z], [X1, Y1, z]], {[side]: {tex: sprite, fn}}, {shade, rot});
}
// a card folded at +-fx: the middle flat, the two outer strips turned back by 22.5 deg (reads round from three quarters)
function folded(sprite, z, {X0, X1, Y0, Y1}, fx, side = 'front') {
  const s = side === 'front' ? 1 : -1;
  return [strip1(sprite, z, {X0: -fx, X1: fx, Y0, Y1}, side, X0, X1),
    strip1(sprite, z, {X0: fx, X1, Y0, Y1}, side, X0, X1, ['y', -s * 22.5, [fx, 0, z]]),
    strip1(sprite, z, {X0, X1: -fx, Y0, Y1}, side, X0, X1, ['y', s * 22.5, [-fx, 0, z]])];
}
// a two-faced card: outer face (seen from -Z) sprite `out`, inner face `inn`
function card2(out, inn, z, rect, opt = {}) {
  const el = cardZ(out, z, rect, opt);
  el.faces.south = {...el.faces.south, texture: '#' + inn};
  return el;
}

// ---- body --------------------------------------------------------------------------------------------------------------------
// pelvis: pivot 1.36 (y 0); the robe over the hips (-0.15 .. +0.06), the vest's lower edge, the crimson sash wrapped twice
// (+0.03 .. +0.15) and its knot at the left hip
function pelvis() {
  const e = limb([[-.15, ell(.17, .12, .17, .14)], [-.06, ell(.205, .135, .205, .15)], [.03, ell(.19, .125, .19, .14)], [.1, ell(.17, .115, .17, .125)]], 'robe');
  // the sash: two wraps (the lower one a hair wider), crimson with fold lines (WRAP sprite)
  e.push(...limb([[.035, ell(.198, .133, .198, .148)], [.095, ell(.186, .127, .186, .138)]], 'sash', {caps: ''}));
  e.push(...limb([[.09, ell(.182, .124, .182, .134)], [.15, ell(.172, .118, .172, .126)]], 'sash', {caps: ''}));
  // the knot at her left hip (front-side): a squashed loop over a flat bow
  e.push(box([.16, .03, -.1], [.22, .13, -.02], 'crimson', {rot: ['y', -22.5, [.19, .08, -.06]]}));
  e.push(box([.185, .055, -.125], [.235, .105, -.085], 'crimson'));
  return e;
}
// torso: pivot = the waist (1.50); robe body to the neck base (+0.55); the vest (open front) over it; the crossed collar and
// the roundels on the painted cards (torso_front / torso_back)
export const TORSO = {FZ: -.156, BZ: .142, FY0: .0, FY1: .5};
function torso() {
  const e = limb([[-.02, ell(.158, .114, .158, .12)], [.1, ell(.165, .122, .165, .124)], [.22, ell(.188, .152, .188, .13)], [.33, ell(.2, .142, .2, .135)],
    [.41, ell(.212, .12, .212, .126)], [.47, ell(.16, .096, .16, .104)], [.52, ell(.1, .075, .1, .08)], [.56, ell(.068, .062, .068, .066)]], 'robe');
  // the vest shell: the back and the sides (open front: facets of the front quarter left out), down to the waist
  const vest = loft('y', [{a: -.03, r: ell(.166, .12, .166, .127)}, {a: .1, r: ell(.173, .128, .173, .131)}, {a: .22, r: ell(.196, .158, .196, .137)},
    {a: .33, r: ell(.208, .148, .208, .142)}, {a: .41, r: ell(.22, .126, .22, .133)}, {a: .465, r: ell(.17, .104, .17, .112)}],
  {n: 16, tex: 'vest', caps: '', skip: (k, th) => th > 45 && th < 135, ledges: true});
  e.push(...vest);
  // front card: the robe's crossed collar (right over left), the white collar band, the vest's open edges with the brass
  // thread, the small lotus roundel on her left breast
  e.push(...folded('torso_front', TORSO.FZ, {X0: -.2, X1: .2, Y0: TORSO.FY0, Y1: TORSO.FY1}, .11));
  // back card: the vest's back with the red-lotus roundel between the shoulder blades
  e.push(...folded('torso_back', TORSO.BZ, {X0: -.2, X1: .2, Y0: TORSO.FY0, Y1: TORSO.FY1}, .11, 'back'));
  return e;
}
// head: pivot = the neck base (2.05); neck 0..0.14, the skull to the top (0.50); the hair cap from the brow line up and
// down the back to the nape; the bangs (fringe card) to the brows; ears under the side locks
export const FACE = {Z: -.152, X0: -.12, X1: .12, Y0: .12, Y1: .38, FX: .055};   // the face card (part `face`)
function head() {
  const e = limb([[-.02, .06], [.13, .058]], 'skin', {n: 8});
  e.push(...limb([[.11, ell(.07, .085, .07, .07), [0, .02]], [.15, ell(.11, .125, .11, .11), [0, .01]], [.24, ell(.142, .148, .142, .15)],
    [.33, ell(.15, .152, .15, .158)], [.41, ell(.14, .14, .14, .148)], [.47, ell(.1, .1, .1, .108)], [.5, ell(.04, .04, .04, .045)]], 'skin'));
  // the hair cap: over the skull from the brow line (0.37 at the front) up, and down the back of the head to the nape
  e.push(...limb([[.18, ell(.152, .02, .152, .163), [0, .02]], [.27, ell(.158, .06, .158, .168), [0, .01]], [.37, ell(.158, .158, .158, .166)],
    [.43, ell(.146, .148, .146, .155)], [.48, ell(.112, .112, .112, .118)], [.515, ell(.05, .05, .05, .055)]], 'hair', {caps: '+'}));
  // the fringe: blunt bangs to the brows, folded round the forehead, from the hairline over the crown's front
  e.push(...folded('fringe', -.166, {X0: -.15, X1: .15, Y0: .3, Y1: .47}, .07));
  return e;
}
// the face card (part face): calm / smile / closed sprites, folded like the head's front (cheeks turned back 22.5 deg)
function face(sprite) { return folded(sprite, FACE.Z, {X0: FACE.X0, X1: FACE.X1, Y0: FACE.Y0, Y1: FACE.Y1}, FACE.FX); }
// the ponytail (pivot at the nape knot; hangs along -Y): upper half with the crimson 댕기 knot, lower half with the ribbon tails
function hairTail(i) {
  const L = i === 1 ? .42 : .44;
  const e = i === 1
    ? limb([[.02, ell(.06, .045, .06, .05)], [-.12, ell(.075, .035, .075, .04)], [-L, ell(.065, .03, .065, .035)]], 'hair', {n: 8})
    : limb([[.0, ell(.065, .03, .065, .035)], [-.25, ell(.055, .026, .055, .03)], [-L, ell(.018, .012, .018, .014)]], 'hair', {n: 8});
  // the visible flats (the hair strands sprite): toward her back (+Z) and toward her body (-Z)
  const w = i === 1 ? .078 : .066;
  e.push(card1(i === 1 ? 'tail_1' : 'tail_2', .036 + (i === 1 ? .012 : 0), {X0: -w, X1: w, Y0: -L - (i === 2 ? .03 : .01), Y1: .03}, 'back'));
  if (i === 1) {
    // the 댕기 knot round the base of the tail (crimson, a gold-stamped band) and a small bow
    e.push(...limb([[.03, ell(.068, .055, .068, .06)], [-.035, ell(.07, .052, .07, .058)]], 'crimson', {n: 8}));
    e.push(box([-.075, -.03, .04], [.075, .035, .07], 'crimson'));
  }
  // the ribbon's two tails along the hair (crimson strips with a gold stamp; one each side of the middle)
  if (i === 1) for (const s of [1, -1]) e.push(card1('ribbon', .066, {X0: s > 0 ? .008 : -.034, X1: s > 0 ? .034 : -.008, Y0: s > 0 ? -.3 : -.24, Y1: -.03}, 'back', {flipU: s < 0}));
  return e;
}
// side locks (pivot at the temple; hang along -Y to the collarbones)
function lock(side) {
  const e = limb([[.02, ell(.028, .02, .028, .02)], [-.16, ell(.032, .019, .032, .019)], [-.3, ell(.012, .008, .012, .008)]], 'hair', {n: 8});
  e.push(card1('lock', -.03, {X0: -.04, X1: .04, Y0: -.34, Y1: .03}, 'front', {flipU: side < 0}));
  return e;
}
// arms: the narrow robe sleeve (pivot = the shoulder joint, 0.40 to the elbow)
function arm(side) {
  const e = limb([[.04, ell(.066, .066, .066, .066)], [-.02, ell(.068, .068, .068, .068)], [-.2, ell(.062, .06, .062, .06)], [-.41, ell(.056, .054, .056, .054)]], 'robe');
  return e;
}
// forearm (pivot = the elbow): the sleeve's end, the leather 토시 guard bound by three crimson cords to the wrist (0.34),
// then the hand: open / grip (a fist round the hilt; the grip point 0.08 below the wrist) / brim (flat fingers, thumb under)
export const ARM = {upper: .40, fore: .34, grip: .08};
function forearm(side, kind) {
  const e = limb([[.02, ell(.058, .056, .058, .056)], [-.08, ell(.06, .058, .06, .058)]], 'robe', {caps: '+'});
  e.push(...limb([[-.06, ell(.056, .054, .056, .054)], [-.2, ell(.054, .052, .054, .052)], [-.335, ell(.044, .042, .044, .042)]], 'guard_arm'));
  e.push(...hand(side, kind));
  return e;
}
// the hand hangs from the wrist (y -0.34) along -Y; the palm faces her body's side (+X for her right hand toward the body's
// centre... the solver turns the forearm so the knuckles lead): open = a relaxed flat hand; grip = a fist whose hole runs along
// the hand frame's Z through (0, wrist - 0.08, 0); brim = fingers straight and together, the thumb tucked (holding an edge)
function hand(side, kind) {
  // authored for her LEFT hand (side +1; the right hand is the mirror image): the palm faces -X (her body's centre line
  // when the arm hangs), the back of the hand +X, the thumb on the -Z (front) side of the palm
  const w = -.34, e = [];
  if (kind === 'open') {
    e.push(box([-.02, w - .085, -.034], [.022, w + .005, .034], 'skin'));
    e.push(box([-.016, w - .155, -.03], [.014, w - .085, .03], 'skin'));
    e.push(box([-.034, w - .075, -.046], [-.006, w - .02, -.028], 'skin'));
  } else if (kind === 'grip') {
    // a fist round the hilt: the hole runs along Z through (0, w - 0.08, 0); the curled fingers wrap its palm side
    e.push(box([-.03, w - .118, -.036], [.034, w + .005, .036], 'skin'));
    e.push(box([-.042, w - .122, -.039], [-.014, w - .058, .039], 'skin'));
    e.push(box([-.04, w - .1, -.05], [-.008, w - .05, -.03], 'skin'));
  } else {
    // brim: the fingers straight and together, the thumb tucked under (the edge of the brim between them)
    e.push(box([-.02, w - .085, -.034], [.022, w + .005, .034], 'skin'));
    e.push(box([-.014, w - .175, -.031], [.012, w - .085, .031], 'skin'));
    e.push(box([-.036, w - .1, -.03], [-.012, w - .04, .0], 'skin'));
  }
  return e;
}
// thigh (pivot = the hip joint): dark plum trousers to the knee (0.60)
function thigh(side) {
  return limb([[.04, ell(.098, .1, .092, .1)], [-.18, ell(.094, .096, .088, .096)], [-.42, ell(.078, .08, .074, .08)], [-.61, ell(.066, .07, .066, .07)]], 'trouser');
}
// shin (pivot = the knee): the ivory 행전 wrap (two crimson ties) to the ankle (0.58), the black 목화 boot with a thick
// white sole; the foot points -Z (0.30 long)
export const LEG = {thigh: .60, shin: .58};
function shin(side) {
  const e = limb([[.03, ell(.07, .074, .07, .072)], [-.04, ell(.071, .075, .071, .073)]], 'trouser', {caps: '+'});
  e.push(...limb([[-.02, ell(.072, .076, .072, .072)], [-.2, ell(.07, .074, .07, .07)], [-.42, ell(.056, .058, .056, .056)], [-.5, ell(.052, .054, .052, .052)]], 'wrap'));
  // the boot shaft (ankle-high 목화 reaching the lower shin), the foot and the sole
  e.push(...limb([[-.46, ell(.06, .062, .06, .06)], [-.56, ell(.064, .066, .064, .064)]], 'boot', {caps: ''}));
  e.push(box([-.055, -.63, -.25], [.055, -.53, .07], 'boot'));
  e.push(box([-.05, -.62, -.3], [.05, -.555, -.235], 'boot', {rot: ['x', 22.5, [0, -.62, -.25]]}));
  e.push(box([-.06, -.675, -.27], [.06, -.625, .08], 'sole'));
  return e;
}
// ---- skirt panels (pivot = the top centre of the panel on the belt line; the panel's -Z faces outward) ----------------------
// Each panel covers a quarter of an octagonal skirt: two facets at -22.5 / +22.5 deg about the panel's centre line, 1.0 b
// long; the outer face shows the sprite (front: ivory knife pleats + the crimson lotus band at the hem; back: the vest's
// long back hem over the pleats), the inner face the lining. The solver tilts the panel outward (the flare) and swings it.
export const SKIRT = {L: 1.0, R0: .205, W: .27, dr: [0, .006, .012, .018]};   // dr: each panel's radial offset (no coplanar overlap)
function skirtPanel(sprite, inner = 'robe_in', dr = 0) {
  // in the panel frame the pivot sits on the panel's centre line at the octagon's inradius R0: the facet edge at x 0,
  // the two facets reach to x +-W (before their 22.5 deg turn about the centre line's crease at x 0)
  const W = SKIRT.W, L = SKIRT.L, z = -dr;
  const e = [];
  for (const s of [1, -1]) {
    const el = cardZ(sprite, z, s > 0 ? {X0: 0, X1: W, Y0: -L, Y1: .02} : {X0: -W, X1: 0, Y0: -L, Y1: .02},
      {uvr: s > 0 ? [.5, 0, 1, 1] : [0, 0, .5, 1], rot: ['y', -s * 22.5, [0, 0, z]]});
    el.faces.south = {...el.faces.south, texture: '#' + inner};
    e.push(el);
  }
  return e;
}
// sash tails (pivot = the knot at the left hip): two crimson tails 0.52 with brass end caps; p2: a glowing crimson edge
function sashTails(p2) {
  const e = [];
  for (const [x, L] of [[-.03, .52], [.035, .46]]) {
    e.push(card2(p2 ? 'sash_tail_p2' : 'sash_tail', p2 ? 'sash_tail_p2' : 'sash_tail', -.01 - (x > 0 ? .006 : 0), {X0: x - .028, X1: x + .028, Y0: -L, Y1: .0}));
    e.push(box([x - .03, -L - .04, -.022], [x + .03, -L, .006], 'brass'));
  }
  return e;
}

// ---- hat (pivot = the brim centre; the brim in the XZ plane, the crown up +Y, the front -Z) --------------------------------
// The brim: four flat squares (side 1.60) turned 0 / 22.5 / 45 / -22.5 deg about Y, stacked 0.003 b apart; each shows the
// one brim sprite, which paints only its corner wedges (22.5 deg each round the 45 deg diagonals) and the radial ribs on
// their boundaries, so the four tile the disc with no coplanar faces and no stacked translucency (PLAN §2.3, FE-16). The
// centre (r < 0.20) is clear on all four: the crown's bottom closes it. Top face = the weave; the underside the same sprite,
// tinted darker by the item definition (tintindex 0). The crown: a 16-facet lacquered drum (D 0.44 x 0.31) with the crimson
// band and the red-lotus knot at the back; P2 knot = brighter (hat_p2).
export const HAT = {R: .8, crownR: .22, crownH: .31, gap: .003, rots: [0, 22.5, 45, -22.5], band: .06};
function hat(p2) {
  const e = [], R = HAT.R;
  HAT.rots.forEach((a, i) => {
    const y = i * HAT.gap, fnU = ([X, , Z]) => [16 * (X + R) / (2 * R), 16 * (Z + R) / (2 * R)];
    const el = faceEl([[-R, y, -R], [R, y + .0005, R]], {up: {tex: 'brim', fn: fnU}, down: {tex: 'brim', fn: fnU}}, {shade: false, rot: a ? ['y', a, [0, y, 0]] : undefined});
    el.faces.down.tintindex = 0;
    e.push(el);
  });
  // the crown: 16 facets (u round the drum, v top -> bottom), its top disc and the closing bottom disc
  const y0 = HAT.gap * 3 + .002, y1 = y0 + HAT.crownH;
  e.push(...lathe('y', [0, 0, 0], [{a: [y0, y1], r: HAT.crownR, tex: 'crown'}], {vFrom: y1, vTo: y0, n: 16}));
  e.push(disc('y', [0, 0, 0], y1, HAT.crownR * .995, '+', 'lacquer'));
  e.push(disc('y', [0, 0, 0], y0 + .001, HAT.crownR * .995, '-', 'lacquer'));
  // the red-lotus knot at the back of the band (faces +Z, her back), centred behind the crown
  e.push(card1(p2 ? 'knot_p2' : 'knot_p1', HAT.crownR + .012, {X0: -.075, X1: .075, Y0: y0 - .025, Y1: y0 + .1}, 'back'));
  e.push(box([-.03, y0 + .01, HAT.crownR - .01], [.03, y0 + .055, HAT.crownR + .01], 'crimson'));
  return e;
}
// hat strings (pivot = the brim centre, the part follows the hat with a lag): two bead strings from the brim's inner sides
// (x +-0.17) meeting in a loop under the chin (0.33 below the brim), then one strand to the chest; the upper V in the
// plane z -0.09 (in front of the neck, beside the cheeks), the lower strand turned 22.5 deg forward off the chest
export const STRINGS = {Z: -.118, X: .155, LOOP: .47, L: .6};
function hatStrings() {
  const z = STRINGS.Z;
  const up = cardZ('strings', z, {X0: -STRINGS.X, X1: STRINGS.X, Y0: -STRINGS.LOOP - .01, Y1: -.01}, {uvr: [0, 0, 1, .75]});
  const lo = cardZ('strings', z, {X0: -.025, X1: .025, Y0: -STRINGS.L, Y1: -STRINGS.LOOP + .005}, {uvr: [.42, .75, .58, 1], rot: ['x', 22.5, [0, -STRINGS.LOOP, z]]});
  return [up, lo];
}

// ---- sword, glow, scabbard, sheathed hilt, item_sword (scale 1.5; pivot = the grip centre / the scabbard's mouth) -----------
// sword: +Y toward the tip, the edge toward -Z, the spine +Z, flats +-X. Grip -0.165..0.165, guard 0.17, blade 0.18..1.93,
// pommel to -0.2 (2.13 in all).
export const SWORD = {gripLo: -.165, gripHi: .165, guard: .175, bladeLo: .185, tip: 1.93, pommel: -.2};
function sword() {
  const e = limb([[SWORD.gripLo, .021], [SWORD.gripHi, .019]], 'grip', {n: 8, caps: ''});
  e.push(...limb([[SWORD.pommel, .02], [SWORD.gripLo, .025]], 'brass', {n: 8}));
  // the lotus guard (eight petals; dark iron with a brass rim), a disc across the blade, both faces
  e.push(cardY('guard', SWORD.guard, {X0: -.065, X1: .065, Z0: -.065, Z1: .065}));
  e.push(box([-.012, SWORD.guard - .012, -.04], [.012, SWORD.guard + .006, .04], 'iron'));
  e.push(box([-.014, SWORD.gripHi - .01, -.032], [.014, SWORD.gripHi + .006, .032], 'brass'));
  // the blade: a thin core (0.022, tapering) and the painted flats (blade: steel, the violet temper line, the bright edge)
  const Y = [SWORD.bladeLo, .8, 1.4, 1.8, SWORD.tip];
  const Wd = [[-.034, .034], [-.032, .032], [-.029, .029], [-.024, .02], [-.01, .006]];
  for (let k = 0; k < Y.length - 1; k++) e.push(box([-.008, Y[k], Wd[k][0] + .006], [.008, Y[k + 1], Wd[k][1] - .006], 'steel'));
  for (const s of [1, -1]) e.push(cardX('blade', s * .0105, {Z0: -.04, Z1: .04, Y0: SWORD.bladeLo, Y1: SWORD.tip + .01}, {flipU: s < 0}));
  return e;
}
// the glow overlay on the blade flats, 0.004 off both faces (translucent emissive-looking sprite per look)
function glow(sprite) {
  return [1, -1].map(s => cardX(sprite, s * .0155, {Z0: -.048, Z1: .042, Y0: SWORD.bladeLo, Y1: SWORD.tip + .02}, {flipU: s < 0}));
}
// scabbard: pivot = its mouth; the body runs +Y 1.82 (edge side -Z, as the sword in it); black lacquer, the red spine line,
// brass lotus-leaf fittings at the mouth, the middle and the tip, two crimson cord hangers
export const SCAB = {L: 1.82, w: .045, d: .045};
function scabbard() {
  const L = SCAB.L, e = [];
  e.push(box([-.02, 0, -.045], [.02, L - .06, .045], 'lacquer'));
  e.push(box([-.016, L - .06, -.04], [.016, L, .03], 'lacquer'));
  for (const s of [1, -1]) e.push(cardX('scab', s * .0215, {Z0: -.047, Z1: .047, Y0: 0, Y1: L}, {flipU: s < 0}));
  // fittings (brass): the mouth collar, the middle band, the chape at the tip
  for (const [a, b] of [[0, .07], [.62, .67], [L - .1, L + .005]]) e.push(box([-.024, a, -.049], [.024, b, .049], 'brass'));
  // the two cord hangers (crimson loops on the spine side)
  for (const y of [.18, .5]) e.push(box([-.012, y, .045], [.012, y + .04, .075], 'crimson'));
  return e;
}
// the hilt seated at the scabbard's mouth (shown only while sheathed): guard, grip, pommel below the mouth (-Y)
function hiltSheathed() {
  const off = -(SWORD.guard + .01), e = [];
  e.push(...limb([[off + SWORD.gripLo, .021], [off + SWORD.gripHi, .019]], 'grip', {n: 8, caps: ''}));
  e.push(...limb([[off + SWORD.pommel, .02], [off + SWORD.gripLo, .025]], 'brass', {n: 8}));
  e.push(cardY('guard', off + SWORD.guard, {X0: -.065, X1: .065, Z0: -.065, Z1: .065}));
  e.push(box([-.012, off + SWORD.guard - .012, -.04], [.012, off + SWORD.guard + .006, .04], 'iron'));
  return e;
}
// item_sword (PLAN §7.3.2, api.ITEM_MODEL): the rig's own scabbard with the hilt seated, ONE piece, the rig's texture only (0
// extra px). Boxes only (no lathe facets), every element turned -45 deg about Z round the model's centre, so the item lies on
// the diagonal like a vanilla sword (hilt lower-left, chape upper-right) and the vanilla handheld display transforms read
// right. Its length: the pommel 1.105 b below the centre .. the chape 1.105 b above (display scale 1.5 = the rig's size).
export const ITEM_SWORD = {shift: -.72, len: 2.21};
function itemSword() {
  const s = ITEM_SWORD.shift, L = SCAB.L, e = [], rot = ['z', 45, [0, 0, 0]];
  const bx = (a, b, tex) => box([a[0], a[1] + s, a[2]], [b[0], b[1] + s, b[2]], tex, {rot});
  e.push(bx([-.02, 0, -.045], [.02, L - .06, .045], 'lacquer'), bx([-.016, L - .06, -.04], [.016, L, .03], 'lacquer'));
  for (const sg of [1, -1]) e.push(cardX('scab', sg * .0215, {Z0: -.047, Z1: .047, Y0: s, Y1: L + s}, {flipU: sg < 0, rot}));
  for (const [a, b] of [[0, .07], [.62, .67], [L - .1, L + .005]]) e.push(bx([-.024, a, -.049], [.024, b, .049], 'brass'));
  for (const y of [.18, .5]) e.push(bx([-.012, y, .045], [.012, y + .04, .075], 'crimson'));
  // the seated hilt: guard plate, the corded grip, the brass pommel (below the mouth)
  const off = -(SWORD.guard + .01);
  e.push(bx([-.022, off + SWORD.gripLo, -.022], [.022, off + SWORD.gripHi, .022], 'grip'));
  e.push(bx([-.026, off + SWORD.pommel, -.026], [.026, off + SWORD.gripLo, .026], 'brass'));
  e.push(bx([-.06, off + SWORD.guard - .008, -.06], [.06, off + SWORD.guard + .008, .06], 'iron'));
  e.push(cardY('guard', off + SWORD.guard + .0085, {X0: -.066, X1: .066, Z0: -.066, Z1: .066}));
  e[e.length - 1].rotation = {origin: [8, 8, 8], axis: 'z', angle: -45};
  return e;
}
// ---- intro props (white porcelain with blue) -------------------------------------------------------------------------------
// cup (pivot = the base centre): D 0.07 x 0.05; bottle (pivot = the base centre): 0.12 x 0.26, a lotus-scroll belly
function cup() {
  const e = lathe('y', [0, 0, 0], [{a: [0, .05], r: .036, tex: 'porcelain'}], {vFrom: .05, vTo: 0, n: 8});
  e.push(disc('y', [0, 0, 0], .002, .034, '-', 'porcelain'));
  e.push(disc('y', [0, 0, 0], .04, .033, '+', 'cup_in'));
  e.push(...lathe('y', [0, 0, 0], [{a: [.044, .052], r: .038, tex: 'cup_rim'}], {vFrom: .052, vTo: .044, n: 8}));
  return e;
}
function bottle() {
  const prof = [[0, .045], [.03, .058], [.09, .062], [.15, .05], [.19, .028], [.235, .02], [.26, .026]];
  const e = [];
  for (let i = 0; i < prof.length - 1; i++) e.push(...lathe('y', [0, 0, 0], [{a: [prof[i][0], prof[i + 1][0]], r: (prof[i][1] + prof[i + 1][1]) / 2, tex: 'bottle'}],
    {vFrom: .26, vTo: 0, n: 8}));
  e.push(disc('y', [0, 0, 0], .002, .044, '-', 'porcelain'), disc('y', [0, 0, 0], .26, .025, '+', 'porcelain'));
  return e;
}

// ---- assembly ---------------------------------------------------------------------------------------------------------------
// block models keyed by item model name (before toUnits)
function blockModels() {
  const M = {empty: []};
  M.pelvis = pelvis(); M.torso = torso(); M.head = head();
  for (const [k, sp] of Object.entries(FACE_MODELS)) M[sp] = face(sp);
  M.hair_tail_1 = hairTail(1); M.hair_tail_2 = hairTail(2);
  M.lock_l = lock(1); M.lock_r = mirrorModel(lock(1));
  M.arm_l = arm(1); M.arm_r = mirrorModel(arm(1));
  for (const k of ['open', 'grip', 'brim']) { M['forearm_l_' + k] = forearm(1, k); M['forearm_r_' + k] = mirrorModel(forearm(1, k)); }
  M.thigh_l = thigh(1); M.thigh_r = mirrorModel(thigh(1)); M.shin_l = shin(1); M.shin_r = mirrorModel(shin(1));
  M.skirt_fl = skirtPanel('skirt_f'); M.skirt_fr = mirrorModel(skirtPanel('skirt_f'));
  M.skirt_bl = skirtPanel('skirt_b'); M.skirt_br = mirrorModel(skirtPanel('skirt_b'));
  M.sash_p1 = sashTails(false); M.sash_p2 = sashTails(true);
  M.hat_p1 = hat(false); M.hat_p2 = hat(true); M.hat_strings = hatStrings();
  M.sword = sword(); M.scabbard = scabbard(); M.hilt = hiltSheathed(); M.item_sword = itemSword();
  for (const g of ['lilac', 'pink', 'violet', 'gold']) M['glow_' + g] = glow('glow_' + g);
  M.cup = cup(); M.bottle = bottle();
  return M;
}
// the display scale a model is shown at (the part that uses it)
export const MODEL_SCALE = {sword: 1.5, scabbard: 1.5, hilt: 1.5, item_sword: 1.5, glow_lilac: 1.5, glow_pink: 1.5, glow_violet: 1.5, glow_gold: 1.5};
// models with no ghost twin (glows, the item, empty)
const NO_GHOST = new Set(['empty', 'item_sword', 'glow_lilac', 'glow_pink', 'glow_violet', 'glow_gold']);
export function allModels() {
  const B = blockModels(), M = {};
  for (const [n, els] of Object.entries(B)) {
    M[n] = toUnits(els, MODEL_SCALE[n] || 1); checkBounds(n, M[n]);
    if (!NO_GHOST.has(n)) {
      // the ghost twin: every face the ghost texture, no tint, the faces unshaded (a flat glowing lilac, PLAN §2.2)
      // the ghost texture's three regions (scarlet_paint ghost): u 0..16/3 the body gradient, 16/3..32/3 the brim mask,
      // 32/3..16 the bead strings' mask; every other face maps into the gradient
      const g = M[n].map(e => ({...e, shade: false, faces: Object.fromEntries(Object.entries(e.faces).map(([k, f]) => {
        const o = {...f, texture: '#' + GHOST_TEX}; delete o.tintindex;
        const off = f.texture === '#brim' ? 16 / 3 : f.texture === '#strings' ? 32 / 3 : 0;
        o.uv = [off + f.uv[0] / 3, f.uv[1], off + f.uv[2] / 3, f.uv[3]].map(x => Math.round(x * 1e4) / 1e4);
        return [k, o];
      }))}));
      M[ghostOf(n)] = g;
    }
  }
  return M;
}
// A-frame model points (blocks at display scale 1; the caller multiplies by the part's PART_SCALE) of every element corner
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
void box; void abox; void card2; void ell;
