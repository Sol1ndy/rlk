// Item models of the 홍련 (Scarlet) rig (S:hr/PLAN.md §2.1-2.3; S2c: the body wears the user's Minecraft skin; S2d: the body is
// the player avatar's). Body models are the avatar's own boxes in model units (pivot [8, 8, 8]); every other model is authored
// in BLOCKS in the A-frame of its part (+X = her LEFT, +Y up, -Z forward; the joint at the origin; the rest orientation of the
// part = torso upright, limbs hanging along -Y, the sword / scabbard along +Y with the edge toward -Z) and converted once by
// toUnits(els, MODEL_SCALE) (mboss_shape_lib.mjs). Elements stay inside -16..32 with one rotation axis of -45 / -22.5 / 0 /
// 22.5 / 45 (RP README §4).
//
// The body (S2d, 11-05; the user's request "팔다리가 너무 기괴하게 긴데 그냥 플레이어 크기랑 똑같게해"): exactly the player
// avatar's body (tools/build_player_rig.mjs bodyModels / skinFaces / skinBox; the classic 4-px arms of 아를레키노's P2 layout,
// tools/arlecchino_geometry.mjs P2_SPECS) wearing the user's 64 x 64 skin (tools/scarlet_skin.mjs, texture
// rlk:mboss/scarlet/skin) at display scale 1: one skin pixel = 1/16 b; head 8 x 8 x 8 px, body 8 x 12 x 4 (split at body row 9
// into the torso, rows 0..9, and the pelvis, rows 9..12: torso + pelvis = the avatar's body box), arms and legs 4 x 12 x 4
// (upper arm / forearm and thigh / shin split at row 6, as the avatar's elbows and knees); the outer layers inflated as the
// avatar's (head 0.5 px, the rest 0.25 px). Nothing is stretched. The hair, the side locks and the skirt panels are in the
// skin already (hidden: model `empty`). What the rig makes itself keeps S2a's shapes in S2c's colours, resized to the new body:
// the hat (a white 백립-style gat), its bead strings, the sash tails, the sword, the scabbard, the hilt, the cup and the bottle.
//
// Proportions (the avatar's skeleton; scarlet_pose.mjs SK): overlay soles 0, knees 0.39, hip line 0.77, seam 0.95, shoulder
// pivots 1.39, neck 1.52, head top 2.02 (outer layer 2.05) with every angle 0; hat brim Ø 1.32 (crown Ø 0.50 x 0.30 on the
// head); arms 0.25 + 0.34 (shoulder -> grip, the avatar's weapon point); thighs 0.375, shins 0.39 (to the overlay sole);
// sword 1.94 (grip 0.45, guard Ø 0.20, blade 1.435), scabbard 1.52.
import {abox, cardZ, cardX, cardY, faceEl, checkBounds, lathe, disc, r4} from './mboss_model_lib.mjs';
import {loft, toUnits, rockBox, registerTile, registerWrap} from './mboss_shape_lib.mjs';
import {bodyElements, P2_SPECS} from './arlecchino_geometry.mjs';

// ---- parts (api.PARTS order) -----------------------------------------------------------------------------------------------
// [name, default model, block brightness, display scale]; `empty` = hidden (in the skin already: the hair, the side locks, the
// skirt panels)
export const PARTS = [
  ['pelvis', 'pelvis', 13, 1], ['torso', 'torso', 13, 1], ['head', 'head', 13, 1], ['face', 'face_calm', 13, 1],
  ['hair_tail_1', 'empty', 13, 1], ['hair_tail_2', 'empty', 13, 1], ['lock_r', 'empty', 13, 1], ['lock_l', 'empty', 13, 1],
  ['arm_r', 'arm_r', 13, 1], ['forearm_r', 'forearm_r_open', 13, 1], ['arm_l', 'arm_l', 13, 1], ['forearm_l', 'forearm_l_grip', 13, 1],
  ['thigh_r', 'thigh_r', 13, 1], ['shin_r', 'shin_r', 13, 1], ['thigh_l', 'thigh_l', 13, 1], ['shin_l', 'shin_l', 13, 1],
  ['skirt_fl', 'empty', 13, 1], ['skirt_fr', 'empty', 13, 1], ['skirt_bl', 'empty', 13, 1], ['skirt_br', 'empty', 13, 1],
  ['sash_tails', 'sash_p1', 13, 1], ['hat', 'hat_p1', 13, 1], ['hat_strings', 'hat_strings', 13, 1],
  ['sword', 'sword', 13, 1.5], ['sword_glow', 'empty', 15, 1.5], ['scabbard', 'scabbard', 13, 1.5], ['hilt_sheathed', 'hilt', 13, 1.5],
  ['cup', 'cup', 13, 1], ['bottle', 'bottle', 13, 1],
];
export const PART_NAMES = PARTS.map(p => p[0]);
export const PART_SCALE = Object.fromEntries(PARTS.map(p => [p[0], p[3]]));
export const PART_BRIGHT = Object.fromEntries(PARTS.map(p => [p[0], p[2]]));
export const DEFAULT_MODEL = Object.fromEntries(PARTS.map(p => [p[0], p[1]]));
// parts the skin already shows (S2c; S2d adds the hair: the skin's own back hair on the body box reads as the player model's,
// a slab behind it would double it and swing like a cape): always the empty model, held at scale 0 by the solver (no keys
// after a clip's tick 0)
export const HIDDEN = ['hair_tail_1', 'hair_tail_2', 'lock_r', 'lock_l', 'skirt_fl', 'skirt_fr', 'skirt_bl', 'skirt_br'];

// ---- looks -> item models (api.LOOKS, HANDS) -----------------------------------------------------------------------------
// the hands are the lower end of the avatar's forearm box (one box for open / grip / brim: the swaps stay, the look is the arm's)
export const HAND_MODELS = {
  forearm_r: {open: 'forearm_r_open', grip: 'forearm_r_grip', brim: 'forearm_r_brim'},
  forearm_l: {open: 'forearm_l_open', grip: 'forearm_l_grip', brim: 'forearm_l_brim'},
};
// calm = the skin's own face (no overlay); smile / closed = small overlays in the skin's colours (sprite face_fx)
export const FACE_MODELS = {calm: 'face_calm', smile: 'face_smile', closed: 'face_closed'};
export const PHASE_MODELS = {hat: {p1: 'hat_p1', p2: 'hat_p2'}, sash_tails: {p1: 'sash_p1', p2: 'sash_p2'}};
export const BLADE_MODELS = {off: 'empty', lilac: 'glow_lilac', pink: 'glow_pink', violet: 'glow_violet', gold: 'glow_gold'};
// the ghost twin of a model (same geometry, every face the texture rlk:mboss/scarlet/ghost); glows / empty have none
export const ghostOf = m => (m === 'empty' || m.startsWith('glow_') ? m : m + '_g');
export const GHOST_TEX = 'ghost';
// the brim's underside carries tintindex 0: the item definitions of the hat models shade it lilac-grey (one shared sprite)
export const TINTS = {hat_p1: 0xA8A0BC, hat_p2: 0xA8A0BC};

// ---- tiles (texel density per block for the boxed props) -------------------------------------------------------------------
// [w, h, px per block]; WRAP sprites map u round a loft and v along its whole length (bands at fixed places)
export const TILE_SIZES = {crimson: [16, 16, 48], brass: [16, 16, 64], iron: [16, 16, 64], lacquer: [16, 16, 48], lacquer_w: [16, 16, 48],
  steel: [16, 16, 64], porcelain: [16, 16, 96]};
export const WRAP_SPRITES = {crown: [64, 32], grip: [16, 32]};
for (const [n, [w, h, ppb]] of Object.entries(TILE_SIZES)) registerTile(n, w, h, ppb);
for (const n of Object.keys(WRAP_SPRITES)) registerWrap(n);

// ---- helpers (blocks) -----------------------------------------------------------------------------------------------------
const box = (a, b, tex, opt) => rockBox(a, b, tex, opt);
// a lofted segment along Y: stations [y, r | [left, front, right, back], c?]
const limb = (sts, tex, opt = {}) => loft('y', sts.map(([a, r, c]) => ({a, r, c: c || [0, 0]})), {n: opt.n || 16, tex, caps: opt.caps ?? '-+', seed: opt.seed || 0, stagger: opt.stagger ?? .004});
// one-sided card (a single face) in the plane z: 'front' (seen from -Z) or 'back' (seen from +Z)
function card1(sprite, z, {X0, X1, Y0, Y1}, side = 'front', {flipU = false, rot, uvr = [0, 0, 1, 1]} = {}) {
  const fn = P => { let s = (P[0] - X0) / (X1 - X0); if (side === 'back') s = 1 - s; if (flipU) s = 1 - s;
    return [16 * (uvr[0] + (uvr[2] - uvr[0]) * s), 16 * (uvr[1] + (uvr[3] - uvr[1]) * (Y1 - P[1]) / (Y1 - Y0))]; };
  return faceEl([[X0, Y0, z], [X1, Y1, z]], {[side]: {tex: sprite, fn}}, {shade: false, rot});
}
// a two-faced card: outer face (seen from -Z) sprite `out`, inner face `inn`
function card2(out, inn, z, rect, opt = {}) {
  const el = cardZ(out, z, rect, opt);
  el.faces.south = {...el.faces.south, texture: '#' + inn};
  return el;
}

// ---- the body: the player avatar's boxes wearing the user's skin (S2d) ------------------------------------------------------
// Regions of the 64 x 64 classic skin [u, v, w, h, d] (px): [base layer, outer layer] (the vanilla layout)
export const SKIN_REGIONS = {
  head: [[0, 0, 8, 8, 8], [32, 0, 8, 8, 8]], body: [[16, 16, 8, 12, 4], [16, 32, 8, 12, 4]],
  arm_r: [[40, 16, 4, 12, 4], [40, 32, 4, 12, 4]], arm_l: [[32, 48, 4, 12, 4], [48, 48, 4, 12, 4]],
  leg_r: [[0, 16, 4, 12, 4], [0, 32, 4, 12, 4]], leg_l: [[16, 48, 4, 12, 4], [0, 48, 4, 12, 4]],
};
// px: one skin pixel (blocks) everywhere (the avatar's 1/16 b); head0: the head box's floor at the neck pivot; torsoRows: the
// body row the torso / pelvis split runs along; the outer layer inflated by inflHead (head) / infl (the rest) px on all six
// sides (the avatar's skinBox)
export const SKIN = {px: 1 / 16, headPx: 1 / 16, bodyPx: 1 / 16, head0: 0, torsoRows: 9, inflHead: .5, infl: .25};
// The avatar's body specs (tools/build_player_rig.mjs bodyModels, classic arms = tools/arlecchino_geometry.mjs P2_SPECS); the
// body box split at row 9: the torso (pivot = the seam, body row 9, 3 px above the hip line) runs rows 0..9 up to the neck, the
// pelvis (pivot = the hip line) rows 9..12 up to the seam. In the avatar's own frame (neck pivot) the torso is
// [4, -1, 6] -> [12, 8, 10] and the pelvis [4, -4, 6] -> [12, -1, 10]: together exactly the avatar's body box.
export const BODY_SPECS = {
  head: P2_SPECS.head,
  torso: {...P2_SPECS.body, from: [4, 8, 6], to: [12, 17, 10], start: 0, end: 9},
  pelvis: {...P2_SPECS.body, from: [4, 8, 6], to: [12, 11, 10], start: 9, end: 12},
  arm_r: P2_SPECS.right_arm, arm_l: P2_SPECS.left_arm, forearm_r: P2_SPECS.right_forearm, forearm_l: P2_SPECS.left_forearm,
  thigh_r: P2_SPECS.right_leg, thigh_l: P2_SPECS.left_leg, shin_r: P2_SPECS.right_shin, shin_l: P2_SPECS.left_shin,
};
// the 15 body models (model units, display scale 1): [base box, outer-layer box] each
export function bodyModels() {
  const M = {};
  for (const n of ['head', 'torso', 'pelvis', 'arm_l', 'arm_r', 'thigh_l', 'thigh_r', 'shin_l', 'shin_r']) M[n] = bodyElements(BODY_SPECS[n]);
  for (const k of ['open', 'grip', 'brim']) { M['forearm_l_' + k] = bodyElements(BODY_SPECS.forearm_l); M['forearm_r_' + k] = bodyElements(BODY_SPECS.forearm_r); }
  return M;
}
// the skin map (manifest skin.map; test_rig.py checks every face of these models against it): model -> [skin region, rows]
// (rows = the base / outer box's rows of the region's height)
export const SKIN_MAP = {
  head: ['head', 0, 8], torso: ['body', 0, SKIN.torsoRows], pelvis: ['body', SKIN.torsoRows, 12],
  arm_l: ['arm_l', 0, 6], arm_r: ['arm_r', 0, 6],
  ...Object.fromEntries(['open', 'grip', 'brim'].flatMap(k => [[`forearm_l_${k}`, ['arm_l', 6, 12]], [`forearm_r_${k}`, ['arm_r', 6, 12]]])),
  thigh_l: ['leg_l', 0, 6], thigh_r: ['leg_r', 0, 6], shin_l: ['leg_l', 6, 12], shin_r: ['leg_r', 6, 12],
};
const IN_UNITS = new Set(Object.keys(SKIN_MAP));
// face overlays (part face, the head's frame): calm = none (the skin's own face); smile = the eyes narrowed (the upper lash
// row lowered onto the iris row, the amber row kept) and a small closed-lip mouth; closed = eyelids over both eyes and a lash
// line on their lower row. One sprite face_fx (32 x 16: the 8 x 8 face at 2 x 2 px per skin pixel, closed | smile), cards
// 0.003 b in front of the face, on the skin's face pixels (1/16 b cells; inside the head's outer layer at -0.281)
export const FACE_FX = {smile: [[1, 4, 2, 2], [5, 4, 2, 2], [3, 7, 2, 1]], closed: [[1, 4, 2, 3], [5, 4, 2, 3]]};   // [col, row, cols, rows] of the 8 x 8 face
function faceOverlay(kind) {
  const H = SKIN.headPx, z = -4 * H - .003, top = SKIN.head0 + 8 * H, u0 = kind === 'smile' ? 8 : 0;
  return (FACE_FX[kind] || []).map(([c, r, w, h]) => cardZ('face_fx', z, {X0: -4 * H + c * H, X1: -4 * H + (c + w) * H, Y0: top - (r + h) * H, Y1: top - r * H},
    {uvr: [(u0 + c) / 16, r / 8, (u0 + c + w) / 16, (r + h) / 8]}));
}
// sash tails (pivot = the knot at the left hip): two crimson tails 0.32 / 0.29 with brass end caps (they end 62 % / 52 % down
// the thigh, as S2c's did on its longer leg); p2: a glowing crimson edge
export const SASH = {tails: [[-.03, .32], [.035, .29]]};
function sashTails(p2) {
  const e = [];
  for (const [x, L] of SASH.tails) {
    e.push(card2(p2 ? 'sash_tail_p2' : 'sash_tail', p2 ? 'sash_tail_p2' : 'sash_tail', -.01 - (x > 0 ? .006 : 0), {X0: x - .028, X1: x + .028, Y0: -L, Y1: .0}));
    e.push(box([x - .03, -L - .04, -.022], [x + .03, -L, .006], 'brass'));
  }
  return e;
}

// ---- hat (pivot = the brim centre; the brim in the XZ plane, the crown up +Y, the front -Z) --------------------------------
// The brim: four flat squares (side 1.32) turned 0 / 22.5 / 45 / -22.5 deg about Y, stacked 0.003 b apart; each shows the
// one brim sprite, which paints only its corner wedges (22.5 deg each round the 45 deg diagonals) and the radial ribs on
// their boundaries, so the four tile the disc with no coplanar faces and no stacked translucency (PLAN §2.3, FE-16). The
// centre (r < 0.20) is clear on all four: the crown's bottom closes it. Top face = the weave; the underside the same sprite,
// tinted lilac-grey by the item definition (tintindex 0). The crown: a 16-facet lacquered drum (D 0.50 x 0.30, the 8-px head's
// width; S2d) with the silk
// band and the red-lotus knot at the back; P2 knot = brighter (hat_p2). S2c colours (matched to the skin's white cap and
// black band): a white 백립-style weave and crown, a black band, the knot in the skin's crimson.
// S2d: brim Ø 1.32 (in proportion to her height: 1.60 x 2.00 / 2.42), the crown on the 8-px head
export const HAT = {R: .66, crownR: .25, crownH: .30, gap: .003, rots: [0, 22.5, 45, -22.5], band: .06};
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
  e.push(disc('y', [0, 0, 0], y1, HAT.crownR * .995, '+', 'lacquer_w'));
  e.push(disc('y', [0, 0, 0], y0 + .001, HAT.crownR * .995, '-', 'lacquer_w'));
  // the red-lotus knot at the back of the band (faces +Z, her back), centred behind the crown
  e.push(card1(p2 ? 'knot_p2' : 'knot_p1', HAT.crownR + .012, {X0: -.085, X1: .085, Y0: y0 - .028, Y1: y0 + .114}, 'back'));
  e.push(box([-.034, y0 + .011, HAT.crownR - .011], [.034, y0 + .063, HAT.crownR + .011], 'crimson'));
  return e;
}
// hat strings (pivot = the brim centre, the part follows the hat with a lag): two bead strings from the brim's underside
// hanging straight down in front of the box head's side columns (x +-0.30: 0.019 outside the head layer's sides), meeting in a
// small loop under the chin (0.60 below the brim, 0.033 under the head), then a short strand turned toward the chest. S2d
// refit for the avatar's 8-px head: Z 0.044 ahead of the face layer at the brim, so the -6 deg tilt and the 45 % gravity pull
// keep the loop >= 0.005 ahead of the face; the strand shapes and beads stay.
export const STRINGS = {Z: -.325, X: .30, LOOP: .60, L: .68};
function hatStrings() {
  const z = STRINGS.Z;
  const up = cardZ('strings', z, {X0: -STRINGS.X, X1: STRINGS.X, Y0: -STRINGS.LOOP - .01, Y1: -.01}, {uvr: [0, 0, 1, .75]});
  const lo = cardZ('strings', z, {X0: -.025, X1: .025, Y0: -STRINGS.L, Y1: -STRINGS.LOOP + .005}, {uvr: [.42, .75, .58, 1], rot: ['x', -22.5, [0, -STRINGS.LOOP, z]]});
  return [up, lo];
}

// ---- sword, glow, scabbard, sheathed hilt, item_sword (scale 1.5; pivot = the left fist's grip point / the scabbard's mouth) --
// sword: +Y toward the tip, the edge toward -Z, the spine +Z, flats +-X. S2d: the length of the avatar's own sword (1.94 b; a long
// katana): grip -0.31..0.14 (two box fists, 0.22 apart), guard 0.155 (the left fist, half-width 0.14 with its outer layer, ends
// 0.014 under it), blade 0.165..1.60 (1.435), pommel to -0.34.
export const SWORD = {gripLo: -.31, gripHi: .14, guard: .155, bladeLo: .165, tip: 1.60, pommel: -.34};
function sword() {
  const e = limb([[SWORD.gripLo, .021], [SWORD.gripHi, .019]], 'grip', {n: 8, caps: ''});
  e.push(...limb([[SWORD.pommel, .02], [SWORD.gripLo, .025]], 'brass', {n: 8}));
  // the lotus guard (eight petals; dark iron with a pale-gold rim), a disc across the blade, both faces
  e.push(cardY('guard', SWORD.guard, {X0: -.10, X1: .10, Z0: -.10, Z1: .10}));
  e.push(box([-.012, SWORD.guard - .012, -.04], [.012, SWORD.guard + .006, .04], 'iron'));
  e.push(box([-.014, SWORD.gripHi - .01, -.032], [.014, SWORD.gripHi + .006, .032], 'brass'));
  // the blade: a thin core (0.022, tapering) and the painted flats (blade: steel, the violet temper line, the bright edge)
  const Y = [SWORD.bladeLo, .671, 1.164, 1.493, SWORD.tip];
  const Wd = [[-.034, .034], [-.032, .032], [-.029, .029], [-.024, .02], [-.01, .006]];
  for (let k = 0; k < Y.length - 1; k++) e.push(box([-.008, Y[k], Wd[k][0] + .006], [.008, Y[k + 1], Wd[k][1] - .006], 'steel'));
  for (const s of [1, -1]) e.push(cardX('blade', s * .0105, {Z0: -.04, Z1: .04, Y0: SWORD.bladeLo, Y1: SWORD.tip + .01}, {flipU: s < 0}));
  return e;
}
// the glow overlay on the blade flats, 0.004 off both faces (translucent emissive-looking sprite per look)
function glow(sprite) {
  return [1, -1].map(s => cardX(sprite, s * .0155, {Z0: -.048, Z1: .042, Y0: SWORD.bladeLo, Y1: SWORD.tip + .02}, {flipU: s < 0}));
}
// scabbard: pivot = its mouth; the body runs +Y 1.52 (the blade 1.445 from the guard + 0.075; edge side -Z, as the sword in it);
// black lacquer, the spine line, pale-gold ('brass' sprite) lotus-leaf fittings at the mouth, the middle and the tip, two
// crimson cord hangers
export const SCAB = {L: 1.52, w: .045, d: .045, fittings: [[0, .06], [.50, .54], [1.52 - .085, 1.52 + .005]], hangers: [.15, .42]};
function scabbard() {
  const L = SCAB.L, e = [];
  e.push(box([-.02, 0, -.045], [.02, L - .06, .045], 'lacquer'));
  e.push(box([-.016, L - .06, -.04], [.016, L, .03], 'lacquer'));
  for (const s of [1, -1]) e.push(cardX('scab', s * .0215, {Z0: -.047, Z1: .047, Y0: 0, Y1: L}, {flipU: s < 0}));
  // fittings (brass): the mouth collar, the middle band, the chape at the tip
  for (const [a, b] of SCAB.fittings) e.push(box([-.024, a, -.049], [.024, b, .049], 'brass'));
  // the two cord hangers (crimson loops on the spine side)
  for (const y of SCAB.hangers) e.push(box([-.012, y, .045], [.012, y + .04, .075], 'crimson'));
  return e;
}
// the hilt seated at the scabbard's mouth (shown only while sheathed): guard, grip, pommel below the mouth (-Y); HILT_OFF = the
// seated sword's grip point below the mouth (scarlet_pose.mjs SK.hilt)
export const HILT_OFF = -(SWORD.guard + .01);
function hiltSheathed() {
  const off = HILT_OFF, e = [];
  e.push(...limb([[off + SWORD.gripLo, .021], [off + SWORD.gripHi, .019]], 'grip', {n: 8, caps: ''}));
  e.push(...limb([[off + SWORD.pommel, .02], [off + SWORD.gripLo, .025]], 'brass', {n: 8}));
  e.push(cardY('guard', off + SWORD.guard, {X0: -.10, X1: .10, Z0: -.10, Z1: .10}));
  e.push(box([-.012, off + SWORD.guard - .012, -.04], [.012, off + SWORD.guard + .006, .04], 'iron'));
  return e;
}
// item_sword (PLAN §7.3.2, api.ITEM_MODEL): the rig's own scabbard with the hilt seated, ONE piece, the rig's texture only (0
// extra px). Boxes only (no lathe facets), every element turned -45 deg about Z round the model's centre, so the item lies on
// the diagonal like a vanilla sword (hilt lower-left, chape upper-right) and the vanilla handheld display transforms read
// right. Its length (S2d): the pommel 1.015 b below the centre .. the chape 1.015 b above (2.03 = the scabbard 1.525 + the hilt
// 0.505) at display scale 1.375 (MODEL_SCALE.item_sword): 23.62 model units (S2c's 23.57), so ITEM_DISPLAY and the reward
// item's look stay.
export const ITEM_SWORD = {shift: -.51, len: 2.03};
function itemSword() {
  const s = ITEM_SWORD.shift, L = SCAB.L, e = [], rot = ['z', 45, [0, 0, 0]];
  const bx = (a, b, tex) => box([a[0], a[1] + s, a[2]], [b[0], b[1] + s, b[2]], tex, {rot});
  e.push(bx([-.02, 0, -.045], [.02, L - .06, .045], 'lacquer'), bx([-.016, L - .06, -.04], [.016, L, .03], 'lacquer'));
  for (const sg of [1, -1]) e.push(cardX('scab', sg * .0215, {Z0: -.047, Z1: .047, Y0: s, Y1: L + s}, {flipU: sg < 0, rot}));
  for (const [a, b] of SCAB.fittings) e.push(bx([-.024, a, -.049], [.024, b, .049], 'brass'));
  for (const y of SCAB.hangers) e.push(bx([-.012, y, .045], [.012, y + .04, .075], 'crimson'));
  // the seated hilt: guard plate, the corded grip, the brass pommel (below the mouth)
  const off = HILT_OFF;
  e.push(bx([-.022, off + SWORD.gripLo, -.022], [.022, off + SWORD.gripHi, .022], 'grip'));
  e.push(bx([-.026, off + SWORD.pommel, -.026], [.026, off + SWORD.gripLo, .026], 'brass'));
  e.push(bx([-.06, off + SWORD.guard - .008, -.06], [.06, off + SWORD.guard + .008, .06], 'iron'));
  e.push(cardY('guard', off + SWORD.guard + .0085, {X0: -.10, X1: .10, Z0: -.10, Z1: .10}));
  e[e.length - 1].rotation = {origin: [8, 8, 8], axis: 'z', angle: -45};
  return e;
}
// ---- intro props (white porcelain with violet) -----------------------------------------------------------------------------
// cup (pivot = the base centre): D 0.15 x 0.072 (S2d: it shows beside a 0.28-b box fist; S2c's sat inside its fist);
// bottle (pivot = the base centre): 0.14 x 0.30 (S2c's profile x 1.15), a lotus-scroll belly, held by the neck
export const CUP = {r: .074, h: .072, centre: .036, hand: .09};
export const BOTTLE = {h: .299, neck: .27};
function cup() {
  const e = lathe('y', [0, 0, 0], [{a: [0, .06], r: .0675, tex: 'porcelain'}], {vFrom: .06, vTo: 0, n: 8});
  e.push(disc('y', [0, 0, 0], .002, .065, '-', 'porcelain'));
  e.push(disc('y', [0, 0, 0], .05, .064, '+', 'cup_in'));
  e.push(...lathe('y', [0, 0, 0], [{a: [.06, .072], r: .074, tex: 'cup_rim'}], {vFrom: .072, vTo: .06, n: 8}));
  return e;
}
function bottle() {
  const prof = [[0, .052], [.0345, .0667], [.1035, .0713], [.1725, .0575], [.2185, .0322], [.2703, .023], [.299, .0299]];
  const e = [];
  for (let i = 0; i < prof.length - 1; i++) e.push(...lathe('y', [0, 0, 0], [{a: [prof[i][0], prof[i + 1][0]], r: (prof[i][1] + prof[i + 1][1]) / 2, tex: 'bottle'}],
    {vFrom: .299, vTo: 0, n: 8}));
  e.push(disc('y', [0, 0, 0], .002, .051, '-', 'porcelain'), disc('y', [0, 0, 0], .299, .029, '+', 'porcelain'));
  return e;
}

// ---- assembly ---------------------------------------------------------------------------------------------------------------
// block models keyed by item model name (before toUnits); the body models (bodyModels) are already in model units
function blockModels() {
  const M = {empty: []};
  for (const [k, m] of Object.entries(FACE_MODELS)) M[m] = faceOverlay(k);
  M.sash_p1 = sashTails(false); M.sash_p2 = sashTails(true);
  M.hat_p1 = hat(false); M.hat_p2 = hat(true); M.hat_strings = hatStrings();
  M.sword = sword(); M.scabbard = scabbard(); M.hilt = hiltSheathed(); M.item_sword = itemSword();
  for (const g of ['lilac', 'pink', 'violet', 'gold']) M['glow_' + g] = glow('glow_' + g);
  M.cup = cup(); M.bottle = bottle();
  return M;
}
// the display scale a model is shown at (the part that uses it); item_sword: the event's thrown display and the reward item
export const MODEL_SCALE = {sword: 1.5, scabbard: 1.5, hilt: 1.5, item_sword: 1.375, glow_lilac: 1.5, glow_pink: 1.5, glow_violet: 1.5, glow_gold: 1.5};
// models with no ghost twin (glows, the item, empty)
const NO_GHOST = new Set(['empty', 'item_sword', 'glow_lilac', 'glow_pink', 'glow_violet', 'glow_gold']);
// the ghost texture's three regions (scarlet_paint ghost): u 0..16/3 the body gradient, 16/3..32/3 the brim mask, 32/3..16 the
// bead strings' mask. A tile / card face maps its own UV into the region; a skin face (a few pixels of the skin) shows the
// whole gradient, so every box face of the ghost body glows the same (core in the middle, rim at the edges)
function ghostUV(f) {
  if (f.texture === '#skin') {
    const [u0, v0, u1, v1] = f.uv;
    return [u0 <= u1 ? 0 : 16 / 3, v0 <= v1 ? 0 : 16, u0 <= u1 ? 16 / 3 : 0, v0 <= v1 ? 16 : 0].map(x => Math.round(x * 1e4) / 1e4);
  }
  const off = f.texture === '#brim' ? 16 / 3 : f.texture === '#strings' ? 32 / 3 : 0;
  return [off + f.uv[0] / 3, f.uv[1], off + f.uv[2] / 3, f.uv[3]].map(x => Math.round(x * 1e4) / 1e4);
}
export function allModels() {
  const B = {...bodyModels(), ...blockModels()}, M = {};
  for (const [n, els] of Object.entries(B)) {
    M[n] = IN_UNITS.has(n) ? els : toUnits(els, MODEL_SCALE[n] || 1); checkBounds(n, M[n]);
    if (!NO_GHOST.has(n)) {
      // the ghost twin: every face the ghost texture, no tint, the faces unshaded (a flat glowing lilac, PLAN §2.2)
      M[ghostOf(n)] = M[n].map(e => ({...e, shade: false, faces: Object.fromEntries(Object.entries(e.faces).map(([k, f]) => {
        const o = {...f, texture: '#' + GHOST_TEX, uv: ghostUV(f)}; delete o.tintindex;
        return [k, o];
      }))}));
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
void cardX; void card2;
