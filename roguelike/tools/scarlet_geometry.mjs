// Item models of the 홍련 (Scarlet) rig (S:hr/PLAN.md §2.1-2.3; S2c: the body wears the user's Minecraft skin). Every model is
// authored in BLOCKS in the A-frame of its part (+X = her LEFT, +Y up, -Z forward; the joint at the origin; the rest
// orientation of the part = torso upright, limbs hanging along -Y, the sword / scabbard along +Y with the edge toward -Z)
// and converted once by toUnits(els, PART_SCALE) (mboss_shape_lib.mjs). Elements stay inside -16..32 with one rotation
// axis of -45 / -22.5 / 0 / 22.5 / 45 (RP README §4).
//
// The body (S2c, 11-05; the user's request "마인크래프트 스킨을 이용해서 만들라고. 아를이나 라이덴처럼"): head, torso, pelvis,
// upper arms, forearms (+ hands), thighs and shins are skin boxes wearing the user's 64 x 64 skin (tools/scarlet_skin.mjs,
// texture rlk:mboss/scarlet/skin; base layer + the outer layer one box out, the vanilla face rects of build_player_rig.mjs)
// stretched onto S2a's skeleton, so every pivot and limb length of scarlet_pose.mjs stays: one skin pixel is 0.0525 b
// across (torso 8 x 4 px = 0.42 x 0.21, limbs 4 x 4 px = 0.21 x 0.21; the head 0.05: 8 px = 0.40); the rows stretch to the bones.
// The hair falls behind as a slab of the skin's own back hair; the side locks and the skirt panels are in the skin
// already (hidden: model `empty`). What the rig makes itself keeps S2a's shapes in colours matched to the skin: the hat
// (a white 백립-style gat), its bead strings, the sash tails, the sword, the scabbard, the hilt, the cup and the bottle.
//
// Proportions (S2a's skeleton; PLAN §2.1): sole 0, ankle 0.10, knee 0.68, hip joints 1.28, pelvis pivot 1.36, waist
// (torso pivot) 1.50, shoulder joints 1.93, neck base (head pivot) 2.05, head top 2.42 (the box head sits 0.03 b into the
// neck so its hat layer stays under the brim); hat brim centre 2.50 (crown top 2.81, brim D 1.60); arms 0.40 + 0.34
// (+ hand, grip 0.08 below the wrist); thighs 0.60, shins 0.58 (+ 0.10 to the sole); sword 2.10 (grip 0.33, guard D 0.13,
// blade 1.75), scabbard 1.82.
import {abox, cardZ, cardX, cardY, faceEl, checkBounds, lathe, disc, r4} from './mboss_model_lib.mjs';
import {loft, toUnits, rockBox, registerTile, registerWrap} from './mboss_shape_lib.mjs';

// ---- parts (api.PARTS order) -----------------------------------------------------------------------------------------------
// [name, default model, block brightness, display scale]; `empty` = hidden (in the skin already)
export const PARTS = [
  ['pelvis', 'pelvis', 13, 1], ['torso', 'torso', 13, 1], ['head', 'head', 13, 1], ['face', 'face_calm', 13, 1],
  ['hair_tail_1', 'hair_tail_1', 13, 1], ['hair_tail_2', 'hair_tail_2', 13, 1], ['lock_r', 'empty', 13, 1], ['lock_l', 'empty', 13, 1],
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
// parts the skin already shows (S2c): always the empty model, held at scale 0 by the solver (no keys after a clip's tick 0)
export const HIDDEN = ['lock_r', 'lock_l', 'skirt_fl', 'skirt_fr', 'skirt_bl', 'skirt_br'];

// ---- looks -> item models (api.LOOKS, HANDS) -----------------------------------------------------------------------------
// the hands are the lower end of the skin's arm (one box for open / grip / brim: the swaps stay, the look is the arm's)
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

// ---- the user's skin on the body (S2c) --------------------------------------------------------------------------------------
// Regions of the 64 x 64 classic skin [u, v, w, h, d] (px): [base layer, outer layer] (the vanilla layout)
export const SKIN_REGIONS = {
  head: [[0, 0, 8, 8, 8], [32, 0, 8, 8, 8]], body: [[16, 16, 8, 12, 4], [16, 32, 8, 12, 4]],
  arm_r: [[40, 16, 4, 12, 4], [40, 32, 4, 12, 4]], arm_l: [[32, 48, 4, 12, 4], [48, 48, 4, 12, 4]],
  leg_r: [[0, 16, 4, 12, 4], [0, 32, 4, 12, 4]], leg_l: [[16, 48, 4, 12, 4], [0, 48, 4, 12, 4]],
};
// px: one skin pixel across (blocks); headPx: a head pixel (the 8 x 8 x 8 head = 0.40 b, a hair smaller than the torso's
// 0.42 so a blade held level under the brim in the lock poses passes over it); bodyPx: a body row (neck base 2.05 -> hip
// joints 1.28 over the skin's 12 rows); head0: the head box's floor below the neck base (its top 0.37 and its hat layer stay
// under the brim); the outer layer one box out by inflHead (head) / infl (the rest) px
// laterally and at the free ends (the cut ends of split limbs stay flush: no coplanar overlap); the right leg's pants a
// hair wider than the left's (the two legs touch at x 0)
export const SKIN = {px: .0525, headPx: .05, bodyPx: .77 / 12, head0: -.03, torsoRows: 9, armTop: .12, armSplit: 6, foreLen: .48, legSplit: 6,
  shinLen: .68, inflHead: .5, infl: .25, inflLegR: .275,
  hairRoot: .2, hairSeg1: .42, hairEnd: 11};
const P = SKIN.px;
// the vanilla face rects of a skin box (px u, v, w, h, d; rows start..end of its height) keyed by the A-frame face (front =
// model north, back = south, right (her right) = east, left = west: build_player_rig.mjs skinFaces on the same model faces)
export function skinUV([u, v, w, h, d], start = 0, end = h) {
  const f = (a, b, c, e) => [a / 4, b / 4, c / 4, e / 4].map(r4);
  return {right: f(u, v + d + start, u + d, v + d + end), front: f(u + d, v + d + start, u + d + w, v + d + end),
    left: f(u + d + w, v + d + start, u + 2 * d + w, v + d + end), back: f(u + 2 * d + w, v + d + start, u + 2 * d + 2 * w, v + d + end),
    up: f(u + d, v, u + d + w, v + d), down: f(u + d + w, v + d, u + d + 2 * w, v)};
}
const skinBox = (lo, hi, uv) => abox(lo, hi, {all: 'skin', uv});
// a body part: the base box [lo, hi] (blocks) and its outer-layer box; ends {lo, hi}: the free ends that grow too
function skinPart(lo, hi, [base, over], start, end, inflPx, ends = {}, px = P) {
  const g = inflPx * px, a = [lo[0] - g, lo[1] - (ends.lo ? g : 0), lo[2] - g], b = [hi[0] + g, hi[1] + (ends.hi ? g : 0), hi[2] + g];
  return [skinBox(lo, hi, skinUV(base, start, end)), skinBox(a, b, skinUV(over, start, end))];
}
// head (pivot = the neck base): the 8 x 8 x 8 box (headPx) from head0 up, the hat layer round it
function head() {
  const y0 = SKIN.head0, h = SKIN.headPx;
  return skinPart([-4 * h, y0, -4 * h], [4 * h, y0 + 8 * h, 4 * h], SKIN_REGIONS.head, 0, 8, SKIN.inflHead, {lo: true, hi: true}, h);
}
// torso (pivot = the waist, the neck base 0.55 above): body rows 0..9 down from the neck base (the seam 0.0275 below the waist)
const NECK = .55;
function torso() {
  const B = SKIN.bodyPx, n = SKIN.torsoRows;
  return skinPart([-4 * P, NECK - n * B, -2 * P], [4 * P, NECK, 2 * P], SKIN_REGIONS.body, 0, n, SKIN.infl, {hi: true});
}
// pelvis (pivot 1.36; the hip joints 0.08 below): body rows 9..12 from the hip joints up to the seam
function pelvis() {
  const B = SKIN.bodyPx, n = SKIN.torsoRows;
  return skinPart([-4 * P, -.08, -2 * P], [4 * P, -.08 + (12 - n) * B, 2 * P], SKIN_REGIONS.body, n, 12, SKIN.infl);
}
// arms (pivot = the shoulder joint): the box one pixel outward of the bone (the vanilla arm pivot), from the shoulder top
// (0.12 above the joint, level with the neck base) to the elbow (rows 0..6); the forearm from the elbow to the hand's end
// (0.48; the grip point 0.42) rows 6..12. side +1 = her left
export const ARM = {upper: .40, fore: .34, grip: .08};
function arm(side) {
  const c = side * P, reg = SKIN_REGIONS[side > 0 ? 'arm_l' : 'arm_r'];
  return skinPart([c - 2 * P, -ARM.upper, -2 * P], [c + 2 * P, SKIN.armTop, 2 * P], reg, 0, SKIN.armSplit, SKIN.infl, {hi: true});
}
function forearm(side) {
  const c = side * P, reg = SKIN_REGIONS[side > 0 ? 'arm_l' : 'arm_r'];
  return skinPart([c - 2 * P, -SKIN.foreLen, -2 * P], [c + 2 * P, 0, 2 * P], reg, SKIN.armSplit, 12, SKIN.infl, {lo: true});
}
// legs (pivot = the hip joint / the knee): centred boxes, thigh rows 0..6 to the knee (0.60), shin rows 6..12 to the sole
export const LEG = {thigh: .60, shin: .58};
function thigh(side) {
  return skinPart([-2 * P, -LEG.thigh, -2 * P], [2 * P, 0, 2 * P], SKIN_REGIONS[side > 0 ? 'leg_l' : 'leg_r'], 0, SKIN.legSplit,
    side > 0 ? SKIN.infl : SKIN.inflLegR);
}
function shin(side) {
  return skinPart([-2 * P, -SKIN.shinLen, -2 * P], [2 * P, 0, 2 * P], SKIN_REGIONS[side > 0 ? 'leg_l' : 'leg_r'], SKIN.legSplit, 12,
    side > 0 ? SKIN.infl : SKIN.inflLegR, {lo: true});
}
// the hair (parts hair_tail_1 / hair_tail_2): a 1-px slab of the skin's back hair (body back rows 0..11 = the hair above the
// belt; the jacket back's strands as its outer layer) hanging from the nape just behind the back. Segment 1 (pivot = the
// hair root, 0.20 above the neck base inside the head) shows rows 0..3.43 from the neck-base level to its end (0.42),
// segment 2 rows 3.43..11 (0.49): at rest it lies over the skin's own back hair at the body's row height, in motion it
// swings out. Faces: back = the hair as painted, front = mirrored, sides / ends = its edge columns / rows.
export const HAIR = {z0: .012, th: P};
function hairUV(v0, r0, r1) {
  const f = (a, b, c, e) => [a / 4, b / 4, c / 4, e / 4].map(r4), y0 = v0 + r0, y1 = v0 + r1;
  return {back: f(32, y0, 40, y1), front: f(40, y0, 32, y1), right: f(39, y0, 40, y1), left: f(32, y0, 33, y1),
    up: f(32, y0, 40, Math.min(y1, y0 + 1)), down: f(32, Math.max(y0, y1 - 1), 40, y1)};
}
function hairSlab(i) {
  const B = SKIN.bodyPx, rMid = (SKIN.hairSeg1 - SKIN.hairRoot) / B;
  const [yTop, yBot, r0, r1] = i === 1 ? [-SKIN.hairRoot, -SKIN.hairSeg1, 0, rMid] : [0, -(SKIN.hairEnd - rMid) * B, rMid, SKIN.hairEnd];
  const z0 = HAIR.z0 - HAIR.th / 2, z1 = HAIR.z0 + HAIR.th / 2, g = SKIN.infl * P;
  return [abox([-4 * P, yBot, z0], [4 * P, yTop, z1], {all: 'skin', uv: hairUV(20, r0, r1)}),
    abox([-4 * P - g, yBot, z0 - g], [4 * P + g, yTop, z1 + g], {all: 'skin', uv: hairUV(36, r0, r1)})];
}
// the skin map (manifest skin.map; test_rig.py checks every face of these models against it): model -> [skin region, rows]
// (rows = the base / outer box's rows of the region's height; the hair slabs: rows of the body's BACK face only)
const RM = (SKIN.hairSeg1 - SKIN.hairRoot) / SKIN.bodyPx;
export const SKIN_MAP = {
  head: ['head', 0, 8], torso: ['body', 0, SKIN.torsoRows], pelvis: ['body', SKIN.torsoRows, 12],
  arm_l: ['arm_l', 0, SKIN.armSplit], arm_r: ['arm_r', 0, SKIN.armSplit],
  ...Object.fromEntries(['open', 'grip', 'brim'].flatMap(k => [[`forearm_l_${k}`, ['arm_l', SKIN.armSplit, 12]], [`forearm_r_${k}`, ['arm_r', SKIN.armSplit, 12]]])),
  thigh_l: ['leg_l', 0, SKIN.legSplit], thigh_r: ['leg_r', 0, SKIN.legSplit], shin_l: ['leg_l', SKIN.legSplit, 12], shin_r: ['leg_r', SKIN.legSplit, 12],
  hair_tail_1: ['body_back', 0, +RM.toFixed(4)], hair_tail_2: ['body_back', +RM.toFixed(4), SKIN.hairEnd],
};
// face overlays (part face, the head's frame): calm = none (the skin's own face); smile = the eyes narrowed (the upper lash
// row lowered onto the iris row, the amber row kept) and a small closed-lip mouth; closed = eyelids over both eyes and a lash
// line on their lower row. One sprite face_fx (32 x 16: the 8 x 8 face at 2 x 2 px per skin pixel, closed | smile), cards
// 0.003 b in front of the face (inside the hat layer)
export const FACE_FX = {smile: [[1, 4, 2, 2], [5, 4, 2, 2], [3, 7, 2, 1]], closed: [[1, 4, 2, 3], [5, 4, 2, 3]]};   // [col, row, cols, rows] of the 8 x 8 face
function faceOverlay(kind) {
  const H = SKIN.headPx, z = -4 * H - .003, top = SKIN.head0 + 8 * H, u0 = kind === 'smile' ? 8 : 0;
  return (FACE_FX[kind] || []).map(([c, r, w, h]) => cardZ('face_fx', z, {X0: -4 * H + c * H, X1: -4 * H + (c + w) * H, Y0: top - (r + h) * H, Y1: top - r * H},
    {uvr: [(u0 + c) / 16, r / 8, (u0 + c + w) / 16, (r + h) / 8]}));
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
// tinted lilac-grey by the item definition (tintindex 0). The crown: a 16-facet lacquered drum (D 0.44 x 0.31) with the silk
// band and the red-lotus knot at the back; P2 knot = brighter (hat_p2). S2c colours (matched to the skin's white cap and
// black band): a white 백립-style weave and crown, a black band, the knot in the skin's crimson.
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
  e.push(disc('y', [0, 0, 0], y1, HAT.crownR * .995, '+', 'lacquer_w'));
  e.push(disc('y', [0, 0, 0], y0 + .001, HAT.crownR * .995, '-', 'lacquer_w'));
  // the red-lotus knot at the back of the band (faces +Z, her back), centred behind the crown
  e.push(card1(p2 ? 'knot_p2' : 'knot_p1', HAT.crownR + .012, {X0: -.075, X1: .075, Y0: y0 - .025, Y1: y0 + .1}, 'back'));
  e.push(box([-.03, y0 + .01, HAT.crownR - .01], [.03, y0 + .055, HAT.crownR + .01], 'crimson'));
  return e;
}
// hat strings (pivot = the brim centre, the part follows the hat with a lag): two bead strings from the brim's underside
// hanging straight down in front of the box head's side columns (x +-0.23), meeting in a small loop under the chin (0.56
// below the brim, just under the head), then a short strand turned toward the chest. S2c refit for the skin's box head
// (0.40 b): S2a's V in front of the cheeks would have run inside the head; the strand shapes and beads stay.
export const STRINGS = {Z: -.262, X: .245, LOOP: .56, L: .64};
function hatStrings() {
  const z = STRINGS.Z;
  const up = cardZ('strings', z, {X0: -STRINGS.X, X1: STRINGS.X, Y0: -STRINGS.LOOP - .01, Y1: -.01}, {uvr: [0, 0, 1, .75]});
  const lo = cardZ('strings', z, {X0: -.025, X1: .025, Y0: -STRINGS.L, Y1: -STRINGS.LOOP + .005}, {uvr: [.42, .75, .58, 1], rot: ['x', -22.5, [0, -STRINGS.LOOP, z]]});
  return [up, lo];
}

// ---- sword, glow, scabbard, sheathed hilt, item_sword (scale 1.5; pivot = the grip centre / the scabbard's mouth) -----------
// sword: +Y toward the tip, the edge toward -Z, the spine +Z, flats +-X. Grip -0.165..0.165, guard 0.17, blade 0.18..1.93,
// pommel to -0.2 (2.13 in all).
export const SWORD = {gripLo: -.165, gripHi: .165, guard: .175, bladeLo: .185, tip: 1.93, pommel: -.2};
function sword() {
  const e = limb([[SWORD.gripLo, .021], [SWORD.gripHi, .019]], 'grip', {n: 8, caps: ''});
  e.push(...limb([[SWORD.pommel, .02], [SWORD.gripLo, .025]], 'brass', {n: 8}));
  // the lotus guard (eight petals; dark iron with a pale-gold rim), a disc across the blade, both faces
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
// scabbard: pivot = its mouth; the body runs +Y 1.82 (edge side -Z, as the sword in it); black lacquer, the spine line,
// pale-gold ('brass' sprite) lotus-leaf fittings at the mouth, the middle and the tip, two crimson cord hangers
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
// ---- intro props (white porcelain with violet) -----------------------------------------------------------------------------
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

// ---- assembly ---------------------------------------------------------------------------------------------------------------
// block models keyed by item model name (before toUnits)
function blockModels() {
  const M = {empty: []};
  M.pelvis = pelvis(); M.torso = torso(); M.head = head();
  for (const [k, m] of Object.entries(FACE_MODELS)) M[m] = faceOverlay(k);
  M.hair_tail_1 = hairSlab(1); M.hair_tail_2 = hairSlab(2);
  M.arm_l = arm(1); M.arm_r = arm(-1);
  for (const k of ['open', 'grip', 'brim']) { M['forearm_l_' + k] = forearm(1); M['forearm_r_' + k] = forearm(-1); }
  M.thigh_l = thigh(1); M.thigh_r = thigh(-1); M.shin_l = shin(1); M.shin_r = shin(-1);
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
  const B = blockModels(), M = {};
  for (const [n, els] of Object.entries(B)) {
    M[n] = toUnits(els, MODEL_SCALE[n] || 1); checkBounds(n, M[n]);
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
// S2a's skirt constants: the solver still places the (hidden) panels (scarlet_pose.mjs PANELS); kept for it
export const SKIRT = {L: 1.0, R0: .205, W: .27, dr: [0, .006, .012, .018]};
void cardX; void card2;
