// HEAD region of the 아펩의 오아시스 파수꾼 rig (plan R4 parts 9-17): neck, head, face, hood, crown and the four hair parts.
//   neck      P1 the dark plate neck | P3 a slim neck under the collar ruff: two rings of pale grey petals drooping over the
//             chest (short at the back, which turns up under the hood's rear edge in the crawl)
//   head      P1 the skull base (the back of the head; the bud-skull stands in front of it) | P3 the skull behind the mask
//             + the lime leaf scarf: broad leaves rooted on the mask's lower rim, drooping over the chin and the ruff
//   face      P1 the closed pale bud-skull (petals round a bud, seen from below and in the rear-up) + the two pale-gold
//             crescents on the cowl's brow lobes (model.md §3.1) | P3 the glowing oval mask 1.6 x 1.9 (centre (0, 6.9, -0.9)
//             in the UPRIGHT stance): the rosette (pale leaves fanning down with dark lime outlines and midribs, radiating
//             veins, darker rim) and the gold lily emblem (a drop-shaped bud between two curled fronds, a trefoil above);
//             the middle stands 0.07 b proud as a second layer (model_p3 §2.1 item 1). The looks p3_idle / p3_charge
//             (orange-gold, w1 f127) / p3_dim are ONE model under three constant colours (apep_materials FACE_MUL);
//             `hidden` is the empty model
//   hood      the cowl, authored once as it sits over the skull in the CROUCH stance for both forms (the hood_hinge swings it
//             back ~107 deg in the UPRIGHT stance: its front tip becomes the 8.5 b peak behind the face).
//             P1 rows of dark slate leaf plates (a rounded dome, top 4.4 b), broad ear flares, pale bark cheek guards, the
//             pointed face shield with the mid-face crystal, the gold V and the dark brow lobes | P3 bottle-green / grey
//             carapace rows with lime rims and grey peel, the dark visor over the mask top, the jagged leaf crest at the
//             peak (it hooks down from the carapace tip in the crawl), dark horns, the brow emeralds, emerald shards and
//             the square lime-gold gem in its raised frame on the ridge (the crawl's front gem)
//   crown     P1 the gold crown cone + two cream-gold sprigs + the lime seed bulb on the cowl top | P3 the glowing bud with a
//             3D fan of gold leaves (nine leaning toward the face, six leaning back over the hood) round the top of the face
//   hair_<s>_1/2   P1 broad dark ribbons from under the ear flares, out over the long arms and down to the ground, the
//             ends splayed (one-sided, R18) | P3 per side an outer dark strand with a lime streak sweeping out from the hood
//             top past the face, a second dark strand from the chin to the chest, and an inner lime strand along the mask
//             edge to the chest. The hair hangs from the HOOD (not from the head as the plan R2 tree draws it): the swing of
//             the hood carries the hair roots from the cowl sides (crouch) to the hood sides beside the face (upright), which
//             the residual table needs (<= 0.25 b).
// Strands, petals, leaves and the crest are RIBBONS: centrelines designed in world space at the part's authoring stance,
// split into flat painted panels, each in the single-axis 22.5-degree element plane closest to the wanted facing that keeps
// the card inside the model bounds (ribbon() below).
// Region interface: see apep_body.mjs. P1 parts in world axes about the joint at the CROUCH stance, P3 at the UPRIGHT
// stance (solved here from apep_clips STANCES so the offsets follow the skeleton); the hair in its bone frame 'y'.
import {loft, slab, toUnits, mirrorX, stroke, registerTile} from './mboss_shape_lib.mjs';
import {PART_SCALE, J, solve, FORM_POINTS, modelFrames, modelPoint} from './apep_pose.mjs';
import {STANCES} from './apep_clips.mjs';
import {PAL, C, clamp, mix, N, lift, sink, autoSlot, sprite, onRect, onRectY, spriteSize, sdLeaf, ball, TRANSPARENT} from './apep_materials.mjs';
import {cardZ, rotA} from './mboss_model_lib.mjs';
import {rot, add} from './mboss_rig_math.mjs';
const invQ = Q => [-Q[0], -Q[1], -Q[2], Q[3]];

export const REGION = 'head';
export const PARTS = ['neck', 'head', 'face', 'hood', 'crown', 'hair_l_1', 'hair_r_1', 'hair_l_2', 'hair_r_2'];
const SP = {};
const card = (name, rect, fn, ppb, forms, use = 'unique') => { const [w, h] = spriteSize(rect, ppb); SP[name] = sprite(w, h, ppb, onRect(rect, fn), forms, 'head', {use}); return name; };
// a card sprite for a plane 'y' slab (its rows run along +z from rect.v0)
const cardY = (name, rect, fn, ppb, forms) => { const [w, h] = spriteSize(rect, ppb); SP[name] = sprite(w, h, ppb, onRectY(rect, fn), forms, 'head'); return name; };
const tile = (name, w, h, ppb, fn, forms) => { registerTile(name, w, h, ppb); SP[name] = sprite(w, h, ppb, (s, t) => fn(s, t), forms, 'head'); return name; };
const sinD = th => Math.sin(th * Math.PI / 180);
const D2R = Math.PI / 180;
const lineOut = (c, d, w, L) => (d > -w ? mix(c, L, .85) : c);
const oneSided = (els, keep) => { for (const e of els) for (const f of Object.keys(e.faces)) if (!keep.includes(f)) delete e.faces[f]; return els; };
const sub = (a, b) => a.map((v, i) => v - b[i]);
const dist = (a, b) => Math.hypot(...sub(a, b));
const oU = solve(STANCES.UPRIGHT);
// the P1 face front: the shield and brow lobes are the hood's, turned 22.5 deg about x round SHIELD_PIV (hood frame); the
// face part's crescents sit on the lobes, so they use the same turn about the same point carried into the face frame
const HOOD2FACE = sub(J.hood_hinge, J.face);
const SHIELD_PIV = [0, -.62, -1.98], LOBE = {x: .27, y: -.33, z: -2.08, rx: .16, ry: .27, tilt: .25};
// the brow lobe as a tilted oval (top leaning out): normalised coordinates (x across inward-positive, y along) for side sx
const lobeXY = (u, v, sx) => { const dx = (u - sx * LOBE.x) * sx, dy = v - LOBE.y, c = Math.cos(LOBE.tilt), s = Math.sin(LOBE.tilt); return [(dx * c - dy * s) / LOBE.rx, (dx * s + dy * c) / LOBE.ry]; };
// a crystal: two crossed painted slabs (side card: the cone outline leaning toward -z by `lean` per block of height;
// front card: turned 22.5 deg about x round the base when it leans) over a thin core; lit / shade halves
function crystal(name, b, w, h, ramp, {lean = 0, forms = 'p1', ppb = 64, seed = 0, edge} = {}) {
  const R = {u0: -w, u1: w, v0: -.02, v1: h};
  const sdF = (u, v) => { const t = clamp(v / h); const hw = w * Math.pow(1 - t, .85) * (v < .06 ? .85 + 2.5 * v : 1); return v < 0 || v > h ? Math.max(-v, v - h) + .01 : Math.abs(u) - hw; };
  const paint = side => (u, v) => {
    const d = -sdF(u, v); if (d < 0) return null;
    const t = clamp(v / h); let c = u * side < 0 ? ramp(clamp(.12 + .35 * t + .12 * (1 - d / w))) : ramp(clamp(.45 + .3 * t));
    if (Math.abs(u) < .012) c = ramp(.05);
    if (u * side < 0 && Math.abs(u + side * w * .45 * (1 - t)) < .018 && t > .2 && t < .7) c = lift(c, .6);
    if (d < .014) c = ramp(.85);
    if (v < .05) c = ramp(.9);
    return c;
  };
  const sF = card(`${name}_f`, R, paint(1), ppb, forms);
  const tanL = Math.tan(22.5 * D2R);
  const els = slab({plane: 'z', at: b[2], rect: {u0: b[0] + R.u0, u1: b[0] + R.u1, v0: b[1] + R.v0, v1: b[1] + R.v1}, sd: (u, v) => sdF(u - b[0], v - b[1]), half: .03, sprite: sF, edge: edge || sF, cell: .05, rot: lean ? ['x', -22.5, b] : null});
  // side card (plane x): the same outline sheared forward by the lean (u = z, toward -z with height)
  const RS = {u0: b[2] - w - tanL * h, u1: b[2] + w, v0: b[1] - .02, v1: b[1] + h};
  const sdS = (u, v) => sdF((u - b[2]) + (lean ? tanL * (v - b[1]) : 0), v - b[1]);
  const sS2 = card(`${name}_x`, {u0: RS.u0 - b[2], u1: RS.u1 - b[2], v0: -.02, v1: h}, (u, v) => paint(-1)(u + (lean ? tanL * v : 0), v), ppb, forms);
  els.push(...slab({plane: 'x', at: b[0], rect: RS, sd: sdS, half: .012, sprite: sS2, core: false}));
  void seed;
  return els;
}

// ---- tiles ------------------------------------------------------------------------------------------------------------------
tile('p1_bud', 64, 64, 48, (u, v) => { const r = ((u * 5 + .4 * Math.sin(v * 7)) % 1 + 1) % 1; let c = PAL.p1_bark(clamp(.05 + .3 * v + .1 * (N.a(u * 8, v * 8) - .5))); if (r < .07) c = PAL.p1_line(.55); return c; }, 'p1');
tile('p1_inner', 32, 32, 32, (u, v) => sink(PAL.p1_slate(.62 + .2 * N.a(u * 6, v * 6)), .4), 'p1');
tile('p1_seed', 16, 16, 32, (u, v) => PAL.p1_core(clamp(.15 + .4 * Math.hypot(u - .5, v - .5))), 'p1');
tile('p3_bud', 32, 32, 32, (u, v) => PAL.p3_bud(clamp(.05 + .5 * Math.hypot(u - .5, v - .5) + .1 * N.c(u * 6, v * 6))), 'p3');

// ================================================= neck, head =================================================================
function neckP1() { const L = dist(J.head, J.neck); return loft('z', [{a: .3, r: .7}, {a: -L * .5, r: [.66, .62, .66, .58]}, {a: -L - .25, r: [.62, .58, .62, .55]}], {tex: 'g_plate', seed: 801}); }
// P3 neck + the collar ruff (model_p3 §2.1 item 6, model.md §4 "collar ruff of pale lilac-grey petals"; v6 f480 zoom): a slim
// neck under two rings of pale grey petals drooping out over the chest; the back petals stay short, since in the crawl
// the neck's back turns up under the hood's rear edge
const ruffPaint = ({t, s, d}) => {
  let c = PAL.p3_pale(clamp(.38 + .3 * t + .15 * Math.abs(s) + .06 * (N.c(t * 7, s * 3) - .5)));
  if (Math.abs(s) < .08 && t > .1 && t < .85) c = mix(c, PAL.p3_pale(.85), .5);
  if (s > .45) c = mix(c, PAL.p3_pale(.2), .4);
  if (d < .02) c = PAL.p3_line(.55);
  return c;
};
function neckP3() {
  const els = loft('y', [{a: -.4, r: [.52, .46, .52, .4]}, {a: .3, r: [.48, .42, .48, .38]}, {a: .66, r: [.44, .38, .44, .34]}], {tex: 'g_plate', seed: 802});
  const fr = partFrame('neck', 'p3', oU), C = [0, 5.84, -.44];
  const ring = (phis, r0, r1, y0, drop, wk, tag) => phis.forEach((ph, i) => {
    const back = Math.abs(ph) > 100, dir = [Math.sin(ph * D2R), 0, -Math.cos(ph * D2R)], R1 = back ? r0 + (r1 - r0) * .45 : r1;
    const P = k => [C[0] + dir[0] * k[0], y0 + k[1], C[2] + dir[2] * k[0]];
    const pts = [P([r0, 0]), P([(r0 + R1) / 2, -drop * .35]), P([R1, -drop])];
    const w = t => wk * Math.pow(Math.sin(Math.PI * Math.min(1, .08 + t * .92)), .7) + .01;
    els.push(...ribbon(`p3_ruff${tag}${i}`, fr, pts, w, {cuts: [0, 1], face: () => [dir[0] * .6, .8, dir[2] * .6], paint: ruffPaint, ppb: 40, forms: 'p3', half: .025, edge: 'hd_p3_ruffedge'}));
  });
  ring([0, 40, -40, 80, -80, 125, -125], .4, 1.0, 5.8, .42, .17, 'a');
  ring([20, -20, 60, -60, 100, -100], .34, .78, 5.92, .3, .13, 'b');
  return els;
}
tile('hd_p3_ruffedge', 16, 16, 32, (u, v) => PAL.p3_pale(clamp(.45 + .1 * N.b(u * 4, v * 4))), 'p3');
// the skull base: only the back of the head (the bud-skull stands in front of it, under the cowl, seen from below / reared)
function headP1() { return loft('z', [{a: .25, r: [.66, .56, .66, .52]}, {a: -.35, r: [.66, .58, .66, .55], c: [0, -.02]}, {a: -.72, r: [.42, .4, .42, .36], c: [0, -.06]}], {tex: 'p1_inner', caps: '-+', seed: 811}); }
// the lime leaf scarf: broad lime leaves wrapping the chin under the mask's lower edge and hanging over the ruff
const scarfLeafPaint = ({t, s, d}) => {
  let c = PAL.p3_lime(clamp(.18 + .3 * t + .15 * Math.abs(s) + .06 * (N.a(t * 8, s * 3) - .5)));
  if (Math.abs(s) < .07 && t < .9) c = mix(c, PAL.p3_line(.3), .45);
  const sv = Math.abs(((t * 4 - Math.abs(s) * 1.2) % 1 + 1) % 1 - .5); if (sv < .05 && Math.abs(s) > .12) c = mix(c, PAL.p3_line(.4), .3);
  if (d < .018) c = PAL.p3_line(.55);
  return c;
};
function headP3() {
  const els = loft('y', [{a: -.3, r: [.62, .36, .62, .5]}, {a: .25, r: [.66, .38, .66, .56]}, {a: .62, r: [.5, .3, .5, .46]}], {tex: 'hd_p3_lining', caps: '-+', seed: 821});
  const fr = partFrame('head', 'p3', oU);
  // leaves rooted on the lower mask rim (the mask: 1.6 x 1.9 about (0, 6.9), front at z -0.97), drooping over the chin
  for (const [i, [x0, y0, x1, y1, wk]] of [[0, 6.22, 0, 5.55, .2], [.3, 6.25, .48, 5.62, .17], [-.3, 6.25, -.48, 5.62, .17], [.55, 6.38, .82, 5.85, .14], [-.55, 6.38, -.82, 5.85, .14]].entries()) {
    const zr = -1.12 - .02 * i, pts = [[x0, y0, zr], [(x0 + x1) / 2, (y0 + y1) / 2 - .03, zr - .08], [x1, y1, zr - .04]];
    const w = t => wk * Math.pow(Math.sin(Math.PI * Math.min(1, .1 + t * .9)), .75) + .01;
    els.push(...ribbon(`p3_scarf${i}`, fr, pts, w, {cuts: [0, 1], face: () => [x1 * .3, .25, -1], paint: scarfLeafPaint, ppb: 40, forms: 'p3', half: .025, edge: 'p3_lime'}));
  }
  return els;
}
// ================================================= face ==================================================================
// the closed flower-bud skull (v2 f0345: pale pointed petals closed round a rounded bud, tips toward the crown, no eyes),
// tilted with the face (its up axis leans forward 22.5 deg in the crouch); seen from below in the crouch and whole when
// the hood swings back. The pale-gold crescents lie on the hood's brow lobes (same turn as the shield, carried here).
const PET_R = {u0: -.36, u1: .36, v0: -.62, v1: .66};
const petSd = (u, v) => { const t = clamp((v + .6) / 1.24); const hw = .34 * Math.pow(Math.sin(Math.PI * Math.min(1, .2 + .8 * t)), .8) * (t < .2 ? .7 + 1.5 * t : 1); return v < -.6 || v > .64 ? 1 : Math.abs(u) - hw; };
const petPaint = (u, v) => {
  const d = -petSd(u, v); if (d < 0) return null;
  const t = clamp((v + .6) / 1.24);
  let c = PAL.p1_bark(clamp(.62 - .45 * t + .08 * (N.d(u * 7, v * 7) - .5) + .25 * clamp(Math.abs(u) / .34)));
  const vein = Math.abs(((Math.atan2(u, v + .7) * 7) % 1 + 1) % 1 - .5); if (vein < .05 && t > .15) c = mix(c, PAL.p1_bark(.85), .35);
  if (Math.abs(u) < .012 && t < .85) c = mix(c, PAL.p1_bark(.9), .5);
  if (d < .03) c = PAL.p1_line(.6);
  return c;
};
const CRESC_R = {u0: -.5, u1: .5, v0: -.7, v1: -.04};
const crescPaint = (u, v) => {
  for (const sx of [1, -1]) {
    const [x, y] = lobeXY(u, v, sx), r = Math.hypot(x, y), a = Math.atan2(y, -x);   // a = 0 toward the inner side
    const k = Math.abs(a - .05) / .8, th = .11 * (1 - k * k); if (k < 1 && Math.abs(r - .76) < th) return PAL.p1_seam(clamp(.0 + .3 * k * k + .3 * Math.abs(r - .76) / .1));
  }
  return null;
};
function faceP1() {
  const f = FORM_POINTS.face.p1[1];
  const els = ball(f, .4, 'p1_bud', {sy: 1.3, seed: 831, n: 8});
  const sp = card('hd_p1_petal', PET_R, petPaint, 48, 'p1');
  const pet = (plane, at, cx, rot, sc = 1) => slab({plane, at, rect: plane === 'z' ? {u0: cx + PET_R.u0 * sc, u1: cx + PET_R.u1 * sc, v0: f[1] + PET_R.v0 * sc, v1: f[1] + PET_R.v1 * sc}
    : {u0: cx + PET_R.u0 * sc, u1: cx + PET_R.u1 * sc, v0: f[1] + PET_R.v0 * sc, v1: f[1] + PET_R.v1 * sc}, sd: (u, v) => petSd((u - cx) / sc, (v - f[1]) / sc) * sc, half: .035, sprite: sp, edge: 'p1_bud', cell: .06, rot});
  const tilt = ['x', -22.5, f];
  els.push(...pet('z', f[2] + .36, 0, tilt, 1.05));                       // back petal
  els.push(...pet('x', .3, f[2], tilt, .95), ...pet('x', -.3, f[2], tilt, .95));   // side petals (in-plane tilt)
  for (const sx of [1, -1]) els.push(...pet('z', f[2] - .26, sx * .2, ['y', sx * 45, [sx * .2, f[1], f[2] - .26]], .9));   // front-side petals
  els.push(...pet('z', f[2] - .4, 0, tilt, .92));                          // the front petal
  // the crescents (the hood's brow lobes turned about SHIELD_PIV; carried into the face frame)
  const piv = SHIELD_PIV.map((v, i) => v + HOOD2FACE[i]), z = LOBE.z - .07 + HOOD2FACE[2];
  els.push(...slab({plane: 'z', at: z, rect: {u0: CRESC_R.u0, u1: CRESC_R.u1, v0: CRESC_R.v0 + HOOD2FACE[1], v1: CRESC_R.v1 + HOOD2FACE[1]}, sd: () => -1, half: .004, core: false,
    sprite: card('hd_p1_crescents', CRESC_R, crescPaint, 64, 'p1'), rot: ['x', 22.5, piv]}));
  return els;
}
const MASK_R = {u0: -.82, u1: .82, v0: -.97, v1: .97};
const maskSd = (u, v) => Math.hypot(u / .8, v / .95) - 1;
// a pointed leaf from (x0, y0) along angle a (rad, 0 = +u), length L, half width W: {e (< 0 inside, ~-1 at the rib), x (along 0..1), y (across)}
const leafAt = (u, v, x0, y0, a, L, W, p = .8) => {
  const ca = Math.cos(a), sa = Math.sin(a), x = ((u - x0) * ca + (v - y0) * sa) / L, y = (-(u - x0) * sa + (v - y0) * ca);
  const hw = W * Math.pow(Math.max(0, Math.sin(Math.PI * clamp(x))), p);
  return {e: x < 0 || x > 1 ? 1 : Math.abs(y) / Math.max(hw, 1e-4) - 1, x, y, hw};
};
// the face rosette (model_p3 §2.1 item 1; v5 f1074, v6 f480 zoom): a glowing gold-lime oval, the gold lily emblem in the upper
// half (a drop-shaped bud between two curled fronds, a small trefoil above), broad pale leaves fanning down over the lower
// face with darker lime outlines and midribs, fine radiating veins, a darker lime rim. One model, three looks (FACE_MUL).
const MASK_LEAVES = [[-90, .62, .2], [-58, .66, .19], [-122, .66, .19], [-28, .56, .16], [-152, .56, .16], [4, .42, .13], [176, .42, .13]];
function maskPaint(u, v) {
  const d = maskSd(u, v);
  if (d > 0) return null;
  const r = Math.hypot(u / .8, (v - .1) / .95);
  let c = PAL.p3_face(clamp(.38 + .42 * r * r + .07 * (N.a(u * 6, v * 6) - .5)));
  // fine veins radiating from the emblem
  const ang = Math.atan2(v - .3, u), vr = Math.abs(((ang * 9 / Math.PI) % 1 + 1) % 1 - .5);
  if (vr < .03 && Math.hypot(u, v - .3) > .3) c = mix(c, PAL.p3_face(.15), .5);
  // the leaf fan below the emblem (drawn back to front: the side leaves under the middle one)
  for (const [deg, L, W] of [...MASK_LEAVES].reverse()) {
    const q = leafAt(u, v, 0, .12, deg * D2R, L, W);
    if (q.e < 0) {
      c = PAL.p3_face(clamp(-.05 + .3 * q.x + .18 * Math.abs(q.y) / Math.max(q.hw, 1e-3) + .05 * (N.b(u * 7, v * 7) - .5)));
      if (Math.abs(q.y) < .012 && q.x > .08 && q.x < .9) c = mix(c, PAL.p3_face(.8), .6);                         // midrib
      const sv = Math.abs(((q.x * 5 - Math.abs(q.y) * 9) % 1 + 1) % 1 - .5); if (sv < .05 && q.x > .15 && Math.abs(q.y) > .02) c = mix(c, PAL.p3_face(.5), .5);    // side veins
      if (q.e > -.16) c = mix(c, PAL.p3_line(.05), .85);                                                           // outline
    }
  }
  // the lily emblem: the drop-shaped bud, the two fronds curling out and up, the trefoil above
  const bu = u, bv = v - .4, drop = Math.hypot(bu / .085, (bv + .02) / (bv > -.02 ? .17 : .1)) - 1;
  for (const sx of [1, -1]) {
    // frond: an arc from the bud foot curling out and up, ending in a curl
    const cx = sx * .2, cy = .38, rr = Math.hypot(u - cx, v - cy), an = Math.atan2(v - cy, (u - cx) * sx);
    if (Math.abs(rr - .16) < .035 * (1 - .4 * clamp((an + 1.4) / 3.6)) && an > -2.6 && an < 1.6) c = mix(PAL.p3_sternum(.2), PAL.p3_sternum(.5), clamp((rr - .13) / .07));
    const curl = Math.hypot(u - sx * .31, v - .5) - .045; if (curl < 0 && curl > -.025) c = PAL.p3_sternum(.45);
    const lf = leafAt(u, v, sx * .05, .58, (90 - sx * 40) * D2R, .2, .045); if (lf.e < 0) c = mix(PAL.p3_sternum(.1), PAL.p3_sternum(.4), clamp(-lf.e));
  }
  const top = leafAt(u, v, 0, .6, 90 * D2R, .2, .05); if (top.e < 0) c = mix(PAL.p3_sternum(.1), PAL.p3_sternum(.4), clamp(-top.e));
  if (drop < 0) c = mix(PAL.p3_sternum(.05), PAL.p3_sternum(.45), clamp(-drop * 1.5) * .5 + clamp(u * 4 + .3) * .5);
  else if (drop < .2) c = mix(c, PAL.p3_line(.3), .6 * (1 - drop / .2));
  // the darker lime rim and the outline
  if (d > -.14) c = mix(c, PAL.p3_face(.85), clamp((d + .14) / .14) * .75);
  return lineOut(c, d, .03, PAL.p3_line(.45));
}
function faceP3() {
  const f = FORM_POINTS.face.p3[1], sp = card('p3_mask', MASK_R, maskPaint, 72, 'p3');
  const rect = {u0: MASK_R.u0, u1: MASK_R.u1, v0: f[1] + MASK_R.v0, v1: f[1] + MASK_R.v1};
  const els = slab({plane: 'z', at: f[2], rect, sd: (u, v) => maskSd(u, v - f[1]), half: .06, sprite: sp, edge: 'p3_gold', cell: .1});
  // slightly domed: the middle of the face stands 0.07 b proud as a second layer of the same painting
  const k = .7, inner = (u, v) => Math.hypot(u / (.8 * k), (v - .08) / (.95 * k)) - 1;
  els.push(...slab({plane: 'z', at: f[2] - .1, rect: {u0: -.6, u1: .6, v0: f[1] - .62, v1: f[1] + .78}, sd: (u, v) => inner(u, v - f[1]) * .6, half: .025, cards: '-', core: false,
    sprite: card('p3_mask_in', {u0: -.6, u1: .6, v0: -.62, v1: .78}, (u, v) => (inner(u, v) > 0 ? null : maskPaint(u, v)), 72, 'p3')}));
  return els;
}
// ================================================= plate rings ================================================================
// A ring of leaf plates round a loft-like section (axis z, the section a 16-gon about [c1, c2] with the quarter-ellipse
// semi-axes r = [e1+, e2+, e1-, e2-], as mboss_shape_lib loft): one slab per facet k, lying on the facet (a horizontal
// slab turned about z for the facets facing up / down, a vertical one for the sides; the facet normals sit on the 22.5
// degree grid, so every plate is one element rotation). Each plate runs from zb (back) to zf (front) and overhangs the
// next row with a tongue (dir -1: toward the front, +1: toward the back); its outline (alpha-cut card + eroded core) is
// shape(s, t): s across (-1..1), t along (0 = the tucked end .. 1 = the tongue tip).
const suppR = (r, th) => { const c = Math.cos(th * D2R), s = Math.sin(th * D2R); return Math.hypot((c >= 0 ? r[0] : r[2]) * c, (s >= 0 ? r[1] : r[3]) * s); };
function ringV(r, n = 16, phase = 0) {
  const st = 360 / n, h = [], nn = [], V = [];
  for (let k = 0; k < n; k++) { const th = phase + k * st; h.push(suppR(r, th)); nn.push([Math.cos(th * D2R), Math.sin(th * D2R)]); }
  for (let k = 0; k < n; k++) { const j = (k + 1) % n, [a1, b1] = nn[k], [a2, b2] = nn[j], det = a1 * b2 - a2 * b1; V.push([(h[k] * b2 - h[j] * b1) / det, (a1 * h[j] - a2 * h[k]) / det]); }
  return {h, V, th: k => phase + k * st, facet: k => { const kk = ((k % n) + n) % n; return [V[(kk - 1 + n) % n], V[kk]]; }};
}
const rot2 = ([x, y], deg) => { const c = Math.cos(deg * D2R), s = Math.sin(deg * D2R); return [x * c - y * s, x * s + y * c]; };
function facetFrame(th0, V0, V1) {
  let th = (th0 % 360 + 360) % 360; if (th > 180) th -= 360;
  let plane, g, sgn;
  if (th >= 45 && th <= 135) { plane = 'y'; g = th - 90; sgn = 1; }
  else if (th <= -45 && th >= -135) { plane = 'y'; g = th + 90; sgn = -1; }
  else if (Math.abs(th) < 45) { plane = 'x'; g = th; sgn = 1; }
  else { plane = 'x'; g = th > 0 ? th - 180 : th + 180; sgn = -1; }
  const p0 = rot2(V0, -g), p1 = rot2(V1, -g), i = plane === 'y' ? 1 : 0, j = 1 - i;
  return {plane, g, sgn, th, at: (p0[i] + p1[i]) / 2, lo: Math.min(p0[j], p1[j]), hi: Math.max(p0[j], p1[j])};
}
// plate outlines: the tongue edge t_e(s) = tb + (1 - tb) prof(s)
const PROF = {
  tip: s => Math.pow(Math.max(0, 1 - Math.pow(Math.abs(s), 1.5)), .75),
  round: s => Math.sqrt(Math.max(0, 1 - s * s)) * .9 + .1,
  split: s => Math.pow(Math.max(0, 1 - Math.pow(1 - Math.min(1, Math.abs(s)), 1.5)), .75),
  wave: s => .55 + .45 * Math.cos(Math.abs(s) * Math.PI * 1.5) ** 2,
};
const OV = 1.06;   // plates reach 3 % past the facet edge (no slit at the vertices)
// normalised distance of (s, t) to the plate outline (negative inside), in blocks for nominal plate half width hw and length L
function plateD(shape, tb, s, t, hw, L) {
  const te = tb + (1 - tb) * PROF[shape](Math.min(1, Math.abs(s) / OV));
  return Math.max((Math.abs(s) - OV) * hw, (t - te) * L * .8, -t * L);
}
// the plate's sprite in either card layout ('y': u = X, rows = Z from the front; 'x': columns = Z from the front, rows
// = Y from the top); paint(s, t, d) with d the distance inside the outline (blocks, >= 0)
function plateSprite(name, layout, dir, shape, tb, hw, L, paint, forms) {
  if (SP[name]) return name;
  const W = layout === 'y' ? 32 : 48, H = layout === 'y' ? 48 : 32;
  SP[name] = sprite(W, H, 48, (x, y) => {
    let s, t;
    if (layout === 'y') { s = 2 * x - 1; t = dir < 0 ? 1 - y : y; } else { t = dir < 0 ? 1 - x : x; s = 1 - 2 * y; }
    const d = plateD(shape, tb, s, t, hw, L);
    if (d > 0) return TRANSPARENT;
    return paint(s, t, -d);
  }, forms, 'head');
  return name;
}
// one ring of plates. o: {z0 (the tucked end), z1 (the base of the tongue; the tongue runs on beyond it), tongue, r, c, n,
// phase, ks, shape (or k -> shape), half, lift, edge, paint, name, forms, core}
function plateRing(o) {
  const {z0, z1, tongue, r, c = [0, 0], ks, shape = 'tip', half = .045, lift = 0, edge, paint, paintOf = null, name, forms, core = true, cell = .07, n = 16, phase = 0} = o;
  const dir = Math.sign(z1 - z0), R = ringV(r, n, phase), els = [], L = Math.abs(z1 - z0) + tongue, tb = Math.abs(z1 - z0) / L;
  const zA = Math.min(z0, z1 + dir * tongue), zB = Math.max(z0, z1 + dir * tongue);
  const tOf = Z => (Z - z0) * dir / L;
  for (const k of ks) {
    const [V0, V1] = R.facet(k), f = facetFrame(R.th(k), V0, V1);
    const sh = typeof shape === 'function' ? shape(k) : shape, hw = (f.hi - f.lo) / 2;
    const [pk, pf] = paintOf ? paintOf(k) : ['', paint];
    const sp = plateSprite(`${name}${pk}_${sh}_${f.plane}_${dir < 0 ? 'f' : 'b'}`, f.plane, dir, sh, tb, hw, L, pf, forms);
    const rot = f.g ? ['z', f.g, [c[0], c[1], 0]] : null;
    if (f.plane === 'y') {
      const mid = c[0] + (f.lo + f.hi) / 2;
      const sd = (u, v) => plateD(sh, tb, (u - mid) / hw, tOf(v), hw, L);
      els.push(...slab({plane: 'y', at: c[1] + f.at + f.sgn * (half + lift), rect: {u0: mid - hw * OV, u1: mid + hw * OV, v0: zA, v1: zB}, sd, half, sprite: sp, edge, cell, rot, core}));
    } else {
      const mid = c[1] + (f.lo + f.hi) / 2;
      const sd = (u, v) => plateD(sh, tb, (v - mid) / hw, tOf(u), hw, L);
      els.push(...slab({plane: 'x', at: c[0] + f.at + f.sgn * (half + lift), rect: {u0: zA, u1: zB, v0: mid - hw * OV, v1: mid + hw * OV}, sd, half, sprite: sp, edge, cell, rot, core}));
    }
  }
  return els;
}
// ================================================= hood (the cowl; CROUCH frame about the hinge) ==============================
// P1 (model.md §3.1, v2 f2076 / f2040, v1 f1110): a dome of dark slate leaf plates in rows (each row's tongues overhang the
// next row toward the face), its top at 4.42 b (the crown cone sits on it), two broad ear flares sweeping out and up from
// the upper sides (3.6 b over the ears), pale bark cheek guards with lobed lower edges beside the bud-skull, and the
// pointed face shield in front: the mid-face crystal over two dark brow lobes, the gold V between them (the pale-gold
// crescents are the face part's), the shield tapering to a point at 2.6 b. The underside stays open over the bud-skull.
const P1PL = (s, t, d) => {
  let c = PAL.p1_slate(clamp(.5 + .1 * (N.a(s * 2 + t * 5, t * 7) - .5) + .12 * (1 - t)));
  if (t < .16) c = sink(c, .35 * (1 - t / .16));                                   // tucked under the row behind
  const vein = Math.abs(s) < .05 && t > .2; if (vein) c = sink(c, .2);
  const fl = Math.abs(((Math.abs(s) * 1.8 + t * 2.4) % 1) - .5); if (fl < .03 && t > .25) c = sink(c, .12);   // feather striations
  if (d < .055) c = mix(PAL.p1_slate(.02), PAL.p1_slate(.25), clamp(d / .055));      // the light bevel rim
  if (d < .018) c = PAL.p1_line(.85);                                                 // dark outline
  return c;
};
tile('hd_p1_hedge', 16, 16, 32, (u, v) => PAL.p1_slate(clamp(.12 + .1 * N.b(u * 4, v * 4))), 'p1');
const P1_ROWS = [
  // back row (tucked under the crest, tongues toward the back), the crest (a keeled octagon: the crown cone sits on its
  // ridge) and the rows stepping down to the face; each row stays inside the one before it (the tongues lie on top)
  {z0: -.15, z1: .42, tongue: .18, r: [.92, .7, .92, .3], c: [0, -.25], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'round'},
  {z0: .12, z1: -.5, tongue: .28, r: [1.2, .88, 1.2, .45], c: [0, -.25], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'tip'},
  {z0: -.42, z1: -.92, tongue: .26, r: [1.12, .8, 1.12, .48], c: [0, -.27], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'split'},
  {z0: -.84, z1: -1.28, tongue: .24, r: [1.02, .66, 1.02, .5], c: [0, -.32], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'tip'},
  {z0: -1.2, z1: -1.56, tongue: .22, r: [.96, .55, .96, .5], c: [0, -.36], ks: [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], shape: 'split'},
  {z0: -1.5, z1: -1.82, tongue: .16, r: [.76, .4, .76, .48], c: [0, -.42], ks: [0, 1, 2, 3, 4, 5, 6, 7, 8], shape: 'round'},
];
// the inner volume under the plates (fills the steps; its underside is the dark lining seen in the rear-up)
const P1_CORE = [{a: .5, r: [.8, .58, .8, .2], c: [0, -.25]}, {a: .05, r: [1.03, .72, 1.03, .36], c: [0, -.25]}, {a: -.5, r: [1.0, .68, 1.0, .4], c: [0, -.27]},
  {a: -.9, r: [.9, .57, .9, .42], c: [0, -.32]}, {a: -1.25, r: [.84, .44, .84, .44], c: [0, -.36]}, {a: -1.55, r: [.64, .3, .64, .42], c: [0, -.42]}, {a: -1.82, r: [.46, .16, .46, .3], c: [0, -.5]}];
// ear flare (plane z, turned 22.5 deg about x so it faces forward-up): a leaf sweeping out and up from the dome side
const EAR1_R = {u0: .78, u1: 2.36, v0: -.16, v1: 1.12};
const EAR1_W = t => .28 * Math.pow(Math.sin(Math.PI * Math.min(1, .2 + t * .82)), .65) + .012;
const EAR1 = stroke([[.92, .22], [1.3, .27], [1.68, .35], [1.98, .5], [2.16, .72], [2.22, 1.0]], EAR1_W);
const ear1Paint = (u, v) => {
  const n = EAR1.near(u, v), hw = EAR1_W(n.t), d = hw - n.d;
  if (d < 0) return null;
  let c = PAL.p1_slate(clamp(.45 + .12 * (N.c(u * 5, v * 5) - .5) + .15 * n.t));
  if (Math.abs(n.s) < .02 && n.t < .9) c = sink(c, .25);                        // midrib
  if (n.s > 0 && d < .06) c = mix(c, C('#ABAC6B'), .8);   // the yellow-green rim line on the upper edge
  else if (d < .045) c = PAL.p1_slate(.08);
  if (d < .016) c = PAL.p1_line(.85);
  return c;
};
// the face shield (plane z, turned 22.5 deg about x: faces forward-up): brow plate + the long pointed muzzle plate
const SHIELD_R = {u0: -.7, u1: .7, v0: -1.42, v1: .06};
const shieldSd = (u, v) => { const w = v > -.5 ? .64 - .1 * clamp((v + .1) / .16) : .64 * Math.pow(clamp((v + 1.4) / .9), .8); return Math.max(Math.abs(u) - w, v - .04, -1.4 - v); };
const shieldPaint = (u, v) => {
  const d = -shieldSd(u, v);
  if (d < 0) return null;
  let c = PAL.p1_slate(clamp(.55 + .1 * (N.a(u * 6, v * 6) - .5) - .15 * clamp((v + 1.1) / 1.1)));
  // the raised inner frame (a lighter line inset 0.08) down the muzzle
  const fi = -shieldSd(u * 1.18, (v + .1) * 1.12 - .1);
  if (v < -.56 && Math.abs(fi - .02) < .022) c = PAL.p1_slate(.2);
  if (v < -.6 && Math.abs(u) < .018) c = sink(c, .3);
  // the gold V (a drop pointing down between the brow lobes)
  const vv = Math.abs(u) - .1 * Math.pow(clamp((v + .8) / .32), .8);
  if (v < -.48 && v > -.8 && vv < 0) c = mix(PAL.p1_gold(.1), PAL.p1_gold(.6), clamp((-.48 - v) / .32) * .7 + (u > 0 ? .3 : 0));
  if (d < .05) c = PAL.p1_slate(.12);
  if (d < .018) c = PAL.p1_line(.85);
  return c;
};
// brow lobes (the two dark "eyes" either side of the V; the face part's crescents sit on their lower inner edges)
const LOBE_R = {u0: -.3, u1: .3, v0: -.32, v1: .32};
const lobeSdS = sx => (u, v) => { const [x, y] = lobeXY(u + sx * LOBE.x, v + LOBE.y, sx); return (Math.hypot(x, y) - 1) * .18; };
const lobePaint = sx => (u, v) => { const [x, y] = lobeXY(u + sx * LOBE.x, v + LOBE.y, sx), e = Math.hypot(x, y) - 1; if (e > 0) return null; let c = PAL.p1_slate(clamp(.7 - .28 * clamp(y * .6 + .5) + .06 * N.b(u * 9, v * 9))); if (e > -.2 && y > .2 && x < .3) c = PAL.p1_slate(.2); if (e > -.08) c = PAL.p1_line(.8); return c; };
// cheek guards: pale bark plates hanging beside the bud-skull, the lower edge in rounded lobes (sheet 02 #32 / #37)
const CHEEK_R = {u0: -1.9, u1: -.45, v0: -1.1, v1: -.1};
const cheekSd = (u, v) => { const lobes = -1.0 + .1 * Math.abs(Math.sin((u + 1.9) * Math.PI / .36)); const top = -.12; const fr = -1.86 + .5 * clamp((-.4 - v) / .7); return Math.max(lobes - v, v - top, fr - u, u + .48); };
const cheekPaint = (u, v) => {
  const d = -cheekSd(u, v);
  if (d < 0) return null;
  let c = PAL.p1_bark(clamp(.3 + .15 * (N.b(u * 5, v * 5) - .5) + .25 * clamp((-.2 - v) / .8)));
  const sw = Math.abs(Math.sin((Math.hypot(u + 1.2, v + .5) * 9 + 2 * N.c(u * 3, v * 3)) * Math.PI));
  if (sw < .1) c = mix(c, PAL.p1_line(.3), .45);                                   // wood-grain contour swirls
  if (v > -.32) c = mix(c, PAL.p1_slate(.55), clamp((v + .32) / .2));                // shadowed under the dome
  if (d < .03) c = PAL.p1_line(.75);
  return c;
};
function hoodP1() {
  const els = [];
  P1_ROWS.forEach((row, i) => els.push(...plateRing({...row, half: .045, edge: 'hd_p1_hedge', paint: P1PL, name: `hd_p1_hp${i}`, forms: 'p1'})));
  els.push(...loft('z', P1_CORE, {tex: (k, th) => (sinD(th) < -.35 ? 'p1_inner' : 'hd_p1_hedge'), caps: '-+', seed: 841}));
  // ears
  const es = card('hd_p1_ear', EAR1_R, ear1Paint, 40, 'p1');
  const ear = slab({plane: 'z', at: -.7, rect: EAR1_R, sd: EAR1.sd, half: .05, sprite: es, edge: 'hd_p1_hedge', cell: .07, rot: ['x', 22.5, [1.2, .3, -.7]]});
  els.push(...ear, ...mirrorX(ear));
  // cheek guards (plane x, the lower edge tucked in: turned about z)
  const cs = card('hd_p1_cheek', CHEEK_R, cheekPaint, 40, 'p1');
  const cheek = slab({plane: 'x', at: 1.06, rect: CHEEK_R, sd: cheekSd, half: .045, sprite: cs, edge: 'hd_p1_hedge', cell: .07, rot: ['z', -22.5, [1.06, -.2, 0]]});
  els.push(...cheek, ...mirrorX(cheek));
  // face shield + brow lobes + the mid-face crystal
  const piv = SHIELD_PIV;
  els.push(...slab({plane: 'z', at: piv[2], rect: SHIELD_R, sd: shieldSd, half: .05, sprite: card('hd_p1_shield', SHIELD_R, shieldPaint, 48, 'p1'), edge: 'hd_p1_hedge', cell: .07, rot: ['x', 22.5, piv]}));
  for (const sx of [1, -1]) els.push(...slab({plane: 'z', at: LOBE.z, rect: {u0: sx * LOBE.x + LOBE_R.u0, u1: sx * LOBE.x + LOBE_R.u1, v0: LOBE.y + LOBE_R.v0, v1: LOBE.y + LOBE_R.v1}, sd: (u, v) => lobeSdS(sx)(u - sx * LOBE.x, v - LOBE.y),
    half: .04, sprite: card(`hd_p1_lobe_${sx > 0 ? 'l' : 'r'}`, LOBE_R, lobePaint(sx), 48, 'p1'), edge: 'hd_p1_hedge', cell: .05, rot: ['x', 22.5, piv]}));
  // the mid-face crystal rises from behind the brow (between the front plates), leaning forward
  els.push(...crystal('hd_p1_brow', [0, -.2, -1.92], .15, .52, PAL.p1_gold, {lean: 1, forms: 'p1', edge: 'p1_gold'}));
  return els;
}
// P3 (model_p3 §2.1 item 3, §3 item 1; v6 f480 / v5 f1074 upright, v6 f90 / v5 f450 crawl): the same cowl plan as a
// sleeker carapace of bottle-green leaf plates with lime rims (lime leaf plates with dark lime lines and grey peel on the
// crest), pointed at the front (the upright peak), open underneath. Upright the swing turns it into a hood standing behind
// the mask: its side rims (lime-edged lips turned in toward the face) reach >= 0.2 b in front of the mask plane, the
// jagged leaf crest closes over the mask top and curls forward, emerald cut crystals sit at the brows on the rims and
// emerald shards along the back; in the crawl it is the long carapace with the square lime-gold gem in a raised frame
// near its front, the emerald shards on top. Anything under the mask window (|x| < 0.85 between the chin and the mask
// top) stays behind the mask plane: hood-model y >= -0.85 + 0.315 (z + 0.26) - 0.08.
const oCr = solve(STANCES.CROUCH);
const hoodU = P => rot(oCr.hood.R, rot(invQ(oU.hood.R), sub(P, oU.hood.t)));             // UPRIGHT world -> hood model
const maskY = z => -.85 + .315 * (z + .26);
const P3PL = (lime, peel, grey = 0) => (s, t, d) => {
  const g = N.a(s * 2 + t * 5, t * 7) - .5;
  let c = lime ? PAL.p3_lime(clamp(.42 + .15 * g + .15 * (1 - t))) : mix(PAL.p3_bottle(clamp(.66 + .12 * g + .12 * (1 - t))), PAL.p1_slate(clamp(.32 + .1 * g + .12 * (1 - t))), .45 + .35 * grey);
  if (t < .16) c = sink(c, .35 * (1 - t / .16));
  if (Math.abs(s) < .05 && t > .2) c = mix(c, PAL.p3_line(.5), .35);
  const fl = Math.abs(((Math.abs(s) * 1.6 + t * 2.2) % 1) - .5); if (fl < .035 && t > .25) c = mix(c, lime ? PAL.p3_line(.45) : PAL.p3_bottle(.85), .5);
  if (peel) { const pe = N.e(s * 1.1 + 3, t * 1.5 + 1); if (pe > .56 && t > .22 && d > .06) c = mix(mix(PAL.p3_pale(.45), PAL.p3_bottle(.5), .25), PAL.p3_pale(.7), clamp((pe - .56) * 5)); }
  if (d < .04) c = mix(PAL.p3_rim(.35), PAL.p3_bottle(.5), clamp(d / .04));             // the lime rim
  if (d < .016) c = PAL.p3_bottle(.95);                                                  // near-black outline
  return c;
};
tile('hd_p3_hedge', 16, 16, 32, (u, v) => mix(PAL.p3_rim(.55), PAL.p3_bottle(.7), .55 + .15 * N.b(u * 4, v * 4)), 'p3');
tile('hd_p3_lining', 32, 32, 32, (u, v) => { let c = PAL.p3_bottle(clamp(.72 + .12 * N.b(u * 6, v * 6))); if (Math.abs(((u * 2 + v * .5) % 1) - .5) < .03) c = mix(c, PAL.p3_rim(.6), .35); return c; }, 'p3');
// rows (tongues toward the front = up the hood when upright); the bottom facets (k -2 / 5) are left open
const P3_ROWS = [
  {z0: -.1, z1: .52, tongue: .2, r: [.84, .48, .84, .55], c: [0, -.42], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'round'},
  {z0: .14, z1: -.55, tongue: .3, r: [1.16, .64, 1.16, .62], c: [0, -.45], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'tip'},
  {z0: -.45, z1: -1.08, tongue: .28, r: [1.06, .57, 1.06, .6], c: [0, -.5], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'split'},
  {z0: -.98, z1: -1.5, tongue: .26, r: [.86, .46, .86, .52], c: [0, -.58], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'tip'},
  {z0: -1.4, z1: -1.86, tongue: .32, r: [.58, .33, .58, .4], c: [0, -.68], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'tip'},
];
const P3_CORE = [{a: .55, r: [.72, .38, .72, .3], c: [0, -.42]}, {a: .1, r: [1.0, .5, 1.0, .36], c: [0, -.45]}, {a: -.5, r: [.98, .48, .98, .36], c: [0, -.5]},
  {a: -1.0, r: [.78, .38, .78, .34], c: [0, -.58]}, {a: -1.45, r: [.52, .26, .52, .26], c: [0, -.68]}, {a: -1.84, r: [.3, .16, .3, .16], c: [0, -.74]}];
const toU = P => add(oU.hood.t, rot(oU.hood.R, rot(invQ(oCr.hood.R), P)));              // hood model -> UPRIGHT world
// FRONT PLATES: slabs in the hood's plane y turned -22.5 deg about x (5 deg off the upright world vertical), drawn in
// front-view coordinates (x, H) = (world x, world height) of the UPRIGHT stance; d = world depth z of the plate
function frontPlate(name, dWorld, Hc, shape, paint, {half = .045, ppb = 40, edge = 'hd_p3_hedge', box = [-1.3, 1.3, 5.6, 9.0], core = true} = {}) {
  const piv = hoodU([0, Hc, dWorld]);
  const toW = (u, v) => { const r = rotA('x', -22.5, [u - piv[0], 0, v - piv[2]]); return toU([piv[0] + r[0], piv[1] + r[1], piv[2] + r[2]]); };
  // v range from the height box (H falls as v grows)
  const vOf = H => { let lo = piv[2] - 4, hi = piv[2] + 4; for (let i = 0; i < 40; i++) { const m = (lo + hi) / 2; if (toW(0, m)[1] > H) lo = m; else hi = m; } return (lo + hi) / 2; };
  const rect = {u0: box[0], u1: box[1], v0: vOf(box[3]), v1: vOf(box[2])};
  const sd = (u, v) => { const W = toW(u, v); return shape(W[0], W[1]); };
  const sp = cardY(name, rect, (u, v) => { const W = toW(u, v); return shape(W[0], W[1]) > 0 ? null : paint(W[0], W[1], -shape(W[0], W[1])); }, ppb, 'p3');
  return slab({plane: 'y', at: piv[1], rect, sd, half, sprite: sp, edge, cell: .07, rot: ['x', -22.5, piv], core});
}
// the visor round the mask top (the hood's front rim, >= 0.2 b in front of the mask): the hole a little larger than the
// mask (0.8 x 0.95 about (0, 6.9)), the outer edge from the peak (8.55) out over the brows, ending at the temples (7.0) where
// the hair strands take over the sides; dark inside (the shadow over the glowing face) with a thin lime lip
const holeE = (x, H) => Math.hypot(x / .88, (H - 6.92) / 1.02) - 1;
const archOut = H => (H > 8.55 ? -1 : H > 7.75 ? 1.04 * Math.sqrt(1 - Math.pow((H - 7.75) / .8, 2.2)) : 1.04);
const archSd = (x, H) => Math.max(Math.abs(x) - archOut(H), -holeE(x, H) * .9, 6.95 + .25 * (1.04 - Math.abs(x)) - H);
const archPaint = (x, H, d) => {
  const e = holeE(x, H);
  let c = PAL.p3_bottle(clamp(.8 - .1 * clamp((8.5 - H) / 1.5) + .06 * (N.a(x * 4, H * 4) - .5)));
  const vein = Math.abs(((Math.atan2(x, H - 9.2) * 9) % 1 + 1) % 1 - .5); if (vein < .035 && e > .15) c = mix(c, PAL.p3_bottle(.55), .4);
  if (e < .05) c = mix(PAL.p3_rim(.35), PAL.p3_rim(.6), clamp(e / .05));                // the lime lip round the face
  else if (e < .12) c = mix(c, PAL.p3_bottle(.95), .5);                                   // its shadow
  else if (Math.abs(x) > archOut(H) - .04 && H > 7.6) c = mix(c, PAL.p3_rim(.5), .6);     // the outer line over the brow
  if (d < .014) c = PAL.p3_bottle(.95);
  return c;
};
// the side walls joining the frame back to the shell sides (plane x; u = model z, v = model y)
const WALL_R = {u0: -1.12, u1: .72, v0: -1.42, v1: -.74};
const wallY = z => -.83 - .54 * clamp((.68 - z) / 1.72) / 1 * 1;     // the frame's model y along z (chin .68 .. brow -1.04)
const wallSd = (u, v) => Math.max(v - (-.76), wallY(u) + .02 - v, u - .7, -1.1 - u);
const wallPaint = (u, v) => { const d = -wallSd(u, v); if (d < 0) return null; let c = PAL.p3_bottle(clamp(.72 + .1 * (N.b(u * 6, v * 6) - .5))); if (Math.abs(((u * 2.2 + v * 3) % 1 + 1) % 1 - .5) < .03) c = mix(c, PAL.p3_rim(.6), .3); if (v - wallY(u) < .07) c = mix(PAL.p3_rim(.1), PAL.p3_rim(.4), clamp((v - wallY(u)) / .07)); return c; };
// the horns: the P1 ear flares grown into dark leaf horns sweeping out and up from the upper sides of the hood
const HORN = stroke([[.72, 7.78], [1.08, 7.98], [1.46, 8.2], [1.76, 8.5], [1.9, 8.86]], t => .24 * Math.pow(Math.sin(Math.PI * Math.min(1, .2 + .82 * t)), .75) + .015);
const hornSd = (x, H) => HORN.sd(Math.abs(x), H);
const hornPaint = (x, H, d) => { const n = HORN.near(Math.abs(x), H); let c = PAL.p3_bottle(clamp(.58 + .1 * (N.c(x * 5, H * 5) - .5) - .2 * n.t)); if (Math.abs(n.s) < .015) c = mix(c, PAL.p3_bottle(.85), .5); if (n.s < 0 && d < .06) c = mix(PAL.p3_rim(.1), PAL.p3_rim(.4), d / .06); if (d < .014) c = PAL.p3_bottle(.95); return c; };
// the brow emeralds: cut crystals on the frame beside the mask's upper half (lit facets up-left)
const GEM = [1.02, 8.08, .16, .25];   // the brow emeralds: x, H, half width, half height (over the outer strands' roots)
const browGemSd = (x, H) => Math.abs(Math.abs(x) - GEM[0]) / GEM[2] + Math.abs(H - GEM[1]) / GEM[3] - 1;
const browGemPaint = (x, H) => { const dx = Math.abs(x) - GEM[0], dy = H - GEM[1]; let t = dx < 0 ? (dy > 0 ? .1 : .35) : (dy > 0 ? .25 : .55); if (Math.abs(dx) < .012 || Math.abs(dy) < .012) t += .15; if (Math.abs(dx) / GEM[2] + Math.abs(dy) / GEM[3] > .82) t = .75; return PAL.p3_emerald(t); };
function hoodP3() {
  const els = [];
  P3_ROWS.forEach((row, i) => els.push(...plateRing({...row, half: .045, edge: 'hd_p3_hedge', name: `hd_p3_hp${i}`, forms: 'p3',
    paintOf: k => ((k === 1 || k === 2) && i === 4 ? ['l', P3PL(true, false)] : (k === 1 || k === 2) && i > 0 && i < 4 ? ['g', P3PL(false, (k === 1 && i === 1) || (k === 2 && i === 3), 1)] : ['', P3PL(false, k === 0 && i === 2)])})));
  els.push(...loft('z', P3_CORE, {tex: 'hd_p3_lining', caps: '+', seed: 861, skip: (k, th) => Math.sin(th * D2R) < -.3}));
  // the veil frame round the mask (>= 0.2 b in front of it), the horns behind its upper corners, the brow emeralds
  els.push(...frontPlate('hd_p3_arch', -1.16, 7.6, archSd, archPaint, {box: [-1.1, 1.1, 6.9, 8.6]}));
  const wall = slab({plane: 'x', at: 1.02, rect: WALL_R, sd: wallSd, half: .03, sprite: card('hd_p3_wall', WALL_R, wallPaint, 32, 'p3'), edge: 'hd_p3_lining', cell: .07});
  els.push(...wall, ...mirrorX(wall));
  const horn = frontPlate('hd_p3_horns', -.82, 8.2, hornSd, hornPaint, {box: [.5, 2.15, 7.45, 8.95]});
  els.push(...horn, ...mirrorX(horn));
  const bgem = frontPlate('hd_p3_browgem', -1.36, GEM[1], browGemSd, browGemPaint, {box: [GEM[0] - GEM[2] - .03, GEM[0] + GEM[2] + .03, GEM[1] - .27, GEM[1] + .27], half: .07, edge: 'p3_emerald', ppb: 64});
  els.push(...bgem, ...mirrorX(bgem));
  // the square lime-gold gem (a diamond pointing forward) in its raised dark frame on the carapace ridge near the front
  // (v6 f90; upright it faces back from the top of the hood), emerald shards along the crest / back
  const GEM_C = [0, -.2, -1.92], dia = r => (u, v) => (Math.abs(u) + Math.abs(v - GEM_C[2])) - r;
  const gemFrame = (u, v) => { const e = Math.abs(u) + Math.abs(v - GEM_C[2]); if (e > .25) return null; return e > .2 ? PAL.p3_rim(.5) : PAL.p3_bottle(clamp(.85 + .08 * (N.a(u * 9, v * 9) - .5))); };
  const gemPaint = (u, v) => { const x = u, y = v - GEM_C[2], e = Math.abs(x) + Math.abs(y); if (e > .155) return null; let t = x < 0 ? (y < 0 ? .05 : .3) : (y < 0 ? .2 : .55); if (Math.abs(x) < .01 || Math.abs(y) < .01) t += .15; if (e > .13) t = .75; return PAL.p3_gem(t); };
  const RG = {u0: -.26, u1: .26, v0: GEM_C[2] - .26, v1: GEM_C[2] + .26};
  els.push(...slab({plane: 'y', at: GEM_C[1], rect: RG, sd: dia(.25), half: .05, sprite: cardY('hd_p3_gemframe', RG, gemFrame, 48, 'p3'), edge: 'hd_p3_hedge', cell: .06}));
  els.push(...slab({plane: 'y', at: GEM_C[1] + .08, rect: RG, sd: dia(.155), half: .03, sprite: cardY('hd_p3_gemface', RG, gemPaint, 64, 'p3'), edge: 'p3_gem', cell: .05}));
  // the jagged leaf crest at the peak, curling forward over the visor top (upright) / hooking down from the carapace tip (crawl)
  const frH = partFrame('hood', 'p3', oU), saw = t => 1 - .35 * Math.abs(((t * 5) % 1) - .5) * 2;
  const crestPaint = ({t, s, d}) => { let c = PAL.p3_bottle(clamp(.78 + .1 * t + .05 * (N.c(t * 9, s * 3) - .5))); if (s > .45) c = mix(c, PAL.p3_rim(.45), .6); if (Math.abs(s) < .08 && t < .9) c = mix(c, PAL.p3_bottle(.95), .5); if (d < .014) c = PAL.p3_bottle(.98); return c; };
  els.push(...ribbon('hd_p3_crest', frH, [[0, 8.3, -.05], [0, 8.58, -.42], [0, 8.66, -.84], [0, 8.56, -1.22], [0, 8.34, -1.44]], t => (.06 + .14 * Math.pow(Math.sin(Math.PI * Math.min(1, .15 + t * .9)), .7)) * saw(t),
    {cuts: [0, .5, 1], face: () => [1, 0, 0], side: () => [0, 1, 0], paint: crestPaint, ppb: 48, forms: 'p3', half: .035, edge: 'hd_p3_hairout'}));
  for (const sx of [1, -1]) els.push(...ribbon(`hd_p3_crest_${sx > 0 ? 'l' : 'r'}`, frH, [[sx * .14, 8.2, -.2], [sx * .2, 8.42, -.55], [sx * .24, 8.48, -.92], [sx * .26, 8.36, -1.2]], t => (.04 + .1 * Math.pow(Math.sin(Math.PI * Math.min(1, .15 + t * .9)), .7)) * saw(t),
    {cuts: [0, 1], face: () => [1, .3 * sx, 0], side: () => [0, 1, 0], paint: crestPaint, ppb: 48, forms: 'p3', half: .03, edge: 'hd_p3_hairout'}));
  for (const [x, y, z, h] of [[0, .14, -.3, .42], [.38, .08, -.65, .32], [-.38, .08, -.65, .32], [.5, -.02, .05, .3], [-.5, -.02, .05, .3], [0, .02, -1.05, .3]]) els.push(...crystal(`hd_p3_shard`, [x, y, z], .07, h, PAL.p3_emerald, {forms: 'p3', ppb: 48, edge: 'p3_emerald'}));
  return els;
}
// ================================================= crown ======================================================================
// P1 crown (model.md §3.1, v1 f255): the lemon-gold cone (0.78 b, leaning 22.5 deg forward; its tip is FORM_POINTS
// crown p1) rising from a dark collar on the crest ridge, two gold leaf sprigs fanned round its foot and the small glowing
// lime seed bulb in front of it
const SPRIG_R = {u0: -.42, u1: .42, v0: 0, v1: .62};
// two branches in a V (v1 f255: cream-gold leaves in pairs along each twig, the tip leaf largest)
const SPRIGS = [[-.03, .02, -.42, .58], [.03, .02, .42, .58], [0, .02, 0, .36]];
const sprigPaint = (u, v) => {
  let best = null;
  for (const [x0, y0, a, L] of SPRIGS) {
    const ca = Math.cos(a), sa = Math.sin(a), x = (u - x0) * ca - (v - y0) * sa, y = (u - x0) * sa + (v - y0) * ca;   // y along the twig
    if (y < -.02 || y > L + .02) continue;
    if (Math.abs(x) < .014 && y < L - .08) return PAL.p1_sprig(.62);
    // leaf pairs at .3 / .55 / .8 of the twig, angled 50 deg off it, plus the tip leaf
    const leaves = [[.3, 1, .9, .11, .045], [.3, -1, .9, .11, .045], [.55, 1, .8, .13, .05], [.55, -1, .8, .13, .05], [.82, 1, .7, .12, .045], [.82, -1, .7, .12, .045], [1, 0, 0, .14, .055]];
    for (const [f, sd, an, ll, ww] of leaves) {
      const by = f * (L - .1), ang = sd * an, lx = x, yy = y - by;
      const px = lx * Math.cos(ang) - yy * Math.sin(ang), py = lx * Math.sin(ang) + yy * Math.cos(ang);   // py along the leaf
      if (py < 0 || py > ll) continue;
      const hw = ww * Math.pow(Math.sin(Math.PI * py / ll), .8), e = Math.abs(px) / Math.max(hw, 1e-4);
      if (e < 1 && (!best || e < best)) best = e;
    }
  }
  if (best === null) return null;
  return best > .72 ? PAL.p1_sprig(.8) : PAL.p1_sprig(clamp(.05 + .35 * best));
};
function crownP1() {
  const tip = FORM_POINTS.crown.p1[1], h = .78, lean = Math.tan(22.5 * D2R);
  const b = [tip[0], tip[1] - h, tip[2] + h * lean];
  const els = crystal('hd_p1_crown', b, .27, h, PAL.p1_gold, {lean: 1, forms: 'p1', ppb: 64, edge: 'p1_gold'});
  // the dark collar the cone stands in (on the ridge plates)
  els.push(...loft('y', [{a: b[1] + .2, r: .2, c: [0, -(b[2] - .08)]}, {a: b[1] + .34, r: .17, c: [0, -(b[2] - .14)]}], {n: 8, tex: 'hd_p1_hedge', caps: '+', seed: 853}));
  // sprigs: two crossed cards fanned round the cone foot, in front of it, and the lime seed bulb
  const sp = card('hd_p1_sprig', SPRIG_R, sprigPaint, 64, 'p1'), f = [b[0], b[1] + .26, b[2] - .26];
  els.push(cardZ(sp, f[2], {X0: f[0] - .42, X1: f[0] + .42, Y0: f[1], Y1: f[1] + .62}, {rot: ['x', -22.5, f]}));
  els.push(cardZ(sp, f[2] + .02, {X0: f[0] - .38, X1: f[0] + .38, Y0: f[1], Y1: f[1] + .56}, {rot: ['y', 45, f], flipU: true}));
  els.push(cardZ(sp, f[2] + .02, {X0: f[0] - .38, X1: f[0] + .38, Y0: f[1], Y1: f[1] + .56}, {rot: ['y', -45, f]}));
  els.push(...ball([f[0], f[1] + .12, f[2] - .04], .12, 'p1_seed', {seed: 852, sy: 1.2}));
  return els;
}
// P3 crown (model_p3 §2.1 item 2; w2 f436 from behind, v5 f450): the glowing yellow bud just above the mask top
// (FORM_POINTS crown p3: the charge-ball anchor) with a sunburst of gold leaves round the top of the head: nine in the
// face plane (every 22.5 deg from side to side, staggered in depth) and three swept back over the hood, so the fan
// reads from the front, the side and from behind (where it rises past the hood's silhouette)
const LEAF_V = {u0: -.13, u1: .13, v0: 0, v1: .98}, LEAF_H = {u0: 0, u1: .98, v0: -.13, v1: .13};
const goldLeafSd = (a, r) => sdLeaf(0, .0, .98, .12, {p: .85})(a, r);
const goldLeafPaint = (a, r) => { const d = -goldLeafSd(a, r); if (d < 0) return null; let c = PAL.p3_crown(clamp(.32 - .3 * (r / .98) + .14 * Math.abs(a) / .12 + .06 * (N.b(a * 9, r * 9) - .5))); if (Math.abs(a) < .012 && r < .85) c = PAL.p3_crown(.75); const vein = Math.abs(((r * 7 - Math.abs(a) * 10) % 1 + 1) % 1 - .5); if (vein < .06 && Math.abs(a) > .02 && r > .15) c = mix(c, PAL.p3_crown(.6), .4); if (d < .014) c = PAL.p3_crown(.9); return c; };
// leaves as world-space ribbons: a front layer of nine (from side to side, leaning 15 deg toward the face) and a back layer
// of six between them leaning 35 deg back over the hood, each curving out at the tip, so the fan reads from the front,
// the side and from behind (w2 f436), under the 9.0 b upright top
const crownLeafPaint = ({t, s, d}) => {
  let c = PAL.p3_crown(clamp(.36 - .3 * t + .18 * Math.abs(s) + .05 * (N.b(t * 9, s * 4) - .5)));
  if (Math.abs(s) < .1 && t < .88) c = PAL.p3_crown(.72);                                                       // the midrib
  const vein = Math.abs(((t * 6 - Math.abs(s) * 1.4) % 1 + 1) % 1 - .5); if (vein < .06 && Math.abs(s) > .16) c = mix(c, PAL.p3_crown(.6), .45);
  if (d < .014) c = PAL.p3_crown(.92);
  return c;
};
function crownP3() {
  const F = FORM_POINTS.crown.p3[1], fr = partFrame('crown', 'p3', oU), Fw = add(fr.O, [0, 1, 2].map(j => fr.ax[0][j] * F[0] + fr.ax[1][j] * F[1] + fr.ax[2][j] * F[2]));
  const els = [...ball(F, .19, 'p3_bud', {seed: 861, n: 8})];
  const leaf = (tag, phi, lean, L, w0) => {
    const dir = [Math.sin(phi * D2R) * Math.cos(lean * D2R), Math.cos(phi * D2R) * Math.cos(lean * D2R), Math.sin(lean * D2R)];   // world; lean > 0 = back
    const side = [Math.cos(phi * D2R), -Math.sin(phi * D2R), 0];
    const P = k => add(Fw, dir.map((v, j) => v * k));
    const pts = [P(.1), add(P(.1 + L * .5), side.map(v => v * .03 * Math.sign(phi || 1))), add(P(.1 + L), side.map(v => v * .1 * Math.sign(phi || 1)))];
    const w = t => w0 * Math.pow(Math.sin(Math.PI * Math.min(1, .06 + t * .94)), .85) + .008;
    const nrm = [dir[1] * side[2] - dir[2] * side[1], dir[2] * side[0] - dir[0] * side[2], dir[0] * side[1] - dir[1] * side[0]];   // across the leaf plane
    els.push(...ribbon(`hd_p3_crown_${tag}`, fr, pts, w, {face: () => nrm, paint: crownLeafPaint, ppb: 56, forms: 'p3', half: .018, edge: 'p3_gold'}));
  };
  [-96, -72, -48, -24, 0, 24, 48, 72, 96].forEach((phi, i) => leaf(`f${i}`, phi, -15, Math.abs(phi) > 50 ? .9 : Math.abs(phi) > 20 ? .82 : .76, .13));
  [-84, -60, -36, 36, 60, 84].forEach((phi, i) => leaf(`b${i}`, phi, 35, Math.abs(phi) > 70 ? .82 : .76, .11));
  return els;
}
// ================================================= ribbons (strands designed in world space) ===================================
// A part's model frame at a stance: model (A-frame blocks) <-> world (rig frame, blocks)
const MF = modelFrames({CROUCH: solve(STANCES.CROUCH), UPRIGHT: oU});
const dot3 = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const nrm3 = a => { const l = Math.hypot(...a) || 1; return a.map(v => v / l); };
function partFrame(part, form, o) {
  const O = modelPoint(o, MF, form, part, [0, 0, 0]), ax = [[1, 0, 0], [0, 1, 0], [0, 0, 1]].map(a => sub(modelPoint(o, MF, form, part, a), O));
  return {O, ax, toM: W => ax.map(a => dot3(sub(W, O), a)), dirM: D => ax.map(a => dot3(D, a)), lim: 1.5 * PART_SCALE[part] - .01};
}
// Catmull-Rom densified polyline through pts (3D) with n samples per span, plus the arc fraction of every sample
function spline(pts, n = 8) {
  const P = [pts[0], ...pts, pts[pts.length - 1]], out = [];
  for (let i = 1; i < P.length - 2; i++) for (let k = 0; k < n; k++) {
    const t = k / n, t2 = t * t, t3 = t2 * t;
    out.push([0, 1, 2].map(j => .5 * (2 * P[i][j] + (-P[i - 1][j] + P[i + 1][j]) * t + (2 * P[i - 1][j] - 5 * P[i][j] + 4 * P[i + 1][j] - P[i + 2][j]) * t2 + (-P[i - 1][j] + 3 * P[i][j] - 3 * P[i + 1][j] + P[i + 2][j]) * t3)));
  }
  out.push(pts[pts.length - 1]);
  const L = [0]; for (let i = 1; i < out.length; i++) L.push(L[i - 1] + dist(out[i], out[i - 1]));
  return {pts: out, t: L.map(l => l / L[L.length - 1]), len: L[L.length - 1]};
}
// nearest point of a 2D polyline with per-vertex values t: {t, s (signed side, + = left of the direction), d}; past either end
// the line runs on straight (t < 0 or > 1), so a clip by t cuts the ends square
function near2(P, T) {
  return (x, y) => {
    let best = null;
    for (let i = 0; i < P.length - 1; i++) {
      const [ax, ay] = P[i], [bx, by] = P[i + 1], dx = bx - ax, dy = by - ay, l = Math.hypot(dx, dy) || 1e-9, ux = dx / l, uy = dy / l;
      const qx = x - ax, qy = y - ay, p = qx * ux + qy * uy, a = (i === 0 && p < 0) || (i === P.length - 2 && p > l) ? p : Math.max(0, Math.min(l, p)), ex = qx - a * ux, ey = qy - a * uy, d2 = ex * ex + ey * ey;
      if (!best || d2 < best.d2) best = {d2, t: T[i] + (T[i + 1] - T[i]) * a / l, s: ux * qy - uy * qx};
    }
    return {t: best.t, s: best.s, d: Math.sqrt(best.d2)};
  };
}
const PLANE_N = {z: [0, 0, 1], x: [1, 0, 0], y: [0, 1, 0]}, PLANE_UV = {z: [0, 1], x: [2, 1], y: [0, 2]}, PLANE_I = {z: 2, x: 0, y: 1};
const ROTS = [0, 22.5, -22.5, 45, -45];
// A ribbon: a strand centreline in WORLD space (stance frame fr of the part) with half width w(t), split into flat panels at
// the arc fractions `cuts`; each panel is one painted slab in the element plane / single-axis 22.5-degree rotation closest
// to facing face(t) (a world direction) across the strand. paint({t, s, d, side}) -> colour (s: -1..1 across, d: blocks
// inside the edge). oneSide: a world direction; the panel keeps only its card facing that way and no core (R18).
function ribbon(name, fr, world, w, {cuts = [0, 1], face = () => [0, 0, -1], side = null, paint, ppb = 32, forms, half = .03, edge, core = true, oneSide = null, ov = .015, n = 8, lim = fr.lim}) {
  const S = spline(world.map(fr.toM), n), els = [];
  for (let i = 0; i < cuts.length - 1; i++) {
    const ta = Math.max(0, cuts[i] - ov), tb = Math.min(1, cuts[i + 1] + ov);
    const idx = S.t.map((t, k) => (t >= ta - .06 && t <= tb + .06 ? k : -1)).filter(k => k >= 0);
    const sub3 = idx.map(k => S.pts[k]), T = nrm3(sub(sub3[sub3.length - 1], sub3[0]));
    const F = fr.dirM(face((ta + tb) / 2)), nn = nrm3(sub(F, T.map(v => v * dot3(F, T))));
    const cands = [];
    for (const pl of ['z', 'x', 'y']) for (const ax of ['x', 'y', 'z']) for (const deg of ROTS) {
      if (ax === pl && deg) continue;
      if (deg === 0 && ax !== 'x') continue;
      const N = rotA(ax, deg, PLANE_N[pl]);
      cands.push({sc: Math.abs(dot3(N, nn)) - (deg ? .002 * Math.abs(deg) / 22.5 : 0), pl, ax, deg, N});
    }
    cands.sort((x, y) => y.sc - x.sc);
    const piv = [0, 1, 2].map(j => sub3.reduce((a, p) => a + p[j], 0) / sub3.length);
    // the panel in a candidate plane: the unrotated strand, its 2D outline and the tight card rect
    const build = best => {
      const unrot = P => add(piv, rotA(best.ax, -best.deg, sub(P, piv)));
      const Q = S.pts.map(unrot), [iu, iv] = PLANE_UV[best.pl], ia = PLANE_I[best.pl];
      const at = idx.reduce((a, k) => a + Q[k][ia], 0) / idx.length;
      const P2 = Q.map(q => [q[iu], q[iv]]), nr = near2(P2, S.t);
      const wmax = Math.max(...idx.map(k => w(S.t[k])));
      const us = idx.map(k => P2[k][0]), vs = idx.map(k => P2[k][1]);
      const R0 = {u0: Math.min(...us) - wmax - .04, u1: Math.max(...us) + wmax + .04, v0: Math.min(...vs) - wmax - .04, v1: Math.max(...vs) + wmax + .04};
      const sd = (u, v) => { const q = nr(u, v); return Math.max(q.d - w(q.t), (ta - q.t) * S.len, (q.t - tb) * S.len); };
      const rect = {u0: 9, u1: -9, v0: 9, v1: -9}, G = 60;
      for (let a = 0; a <= G; a++) for (let b = 0; b <= G; b++) {
        const u = R0.u0 + (R0.u1 - R0.u0) * a / G, v = R0.v0 + (R0.v1 - R0.v0) * b / G;
        if (sd(u, v) < .015) { rect.u0 = Math.min(rect.u0, u); rect.u1 = Math.max(rect.u1, u); rect.v0 = Math.min(rect.v0, v); rect.v1 = Math.max(rect.v1, v); }
      }
      rect.u0 -= .02; rect.u1 += .02; rect.v0 -= .02; rect.v1 += .02;
      const fits = !lim || (Math.max(Math.abs(rect.u0), Math.abs(rect.u1), Math.abs(rect.v0), Math.abs(rect.v1), Math.abs(at) + half + .02) <= lim);
      return {...best, iu, iv, at, P2, nr, sd, rect, fits};
    };
    let B = null;
    for (const c of cands) { const b = build(c); if (b.fits) { B = b; break; } if (!B) B = b; }
    const {iu, iv, at, P2, nr, sd, rect} = B;
    // s > 0 on the side of the world direction side(t) (default: the left of the 2D direction)
    let sg = 1;
    if (side) {
      const km = idx[Math.floor(idx.length / 2)], k2 = Math.min(S.pts.length - 1, km + 1), k1 = k2 - 1, dx = P2[k2][0] - P2[k1][0], dy = P2[k2][1] - P2[k1][1];
      const r3 = rotA(B.ax, -B.deg, fr.dirM(side(S.t[km]))), r2 = [r3[iu], r3[iv]];
      sg = Math.sign(-dy * r2[0] + dx * r2[1]) || 1;
    }
    const pt = (u, v) => { const q = nr(u, v), hw = w(q.t), d = hw - q.d; if (d < 0 || q.t < ta - .002 || q.t > tb + .002) return null; return paint({t: q.t, s: clamp(sg * q.s / Math.max(hw, 1e-3), -1, 1), d, len: S.len}); };
    const sname = `${name}_${i}`, sp = B.pl === 'y' ? cardY(sname, rect, pt, ppb, forms) : card(sname, rect, pt, ppb, forms);
    const rot = B.deg ? [B.ax, B.deg, piv] : null;
    if (oneSide) {
      const o = rotA(B.ax, -B.deg, fr.dirM(oneSide)), sgn = Math.sign(dot3(o, PLANE_N[B.pl])) || 1;
      const keep = {z: sgn > 0 ? 'south' : 'north', x: sgn > 0 ? 'west' : 'east', y: sgn > 0 ? 'up' : 'down'}[B.pl];
      els.push(...oneSided(slab({plane: B.pl, at, rect, sd, half, sprite: sp, edge, core: false, rot, cards: sgn > 0 ? '+' : '-'}), [keep]));
    } else els.push(...slab({plane: B.pl, at, rect, sd, half, sprite: sp, edge: edge || sp, cell: .06, rot, core}));
  }
  return els;
}

// ================================================= hair (bone frame 'y') =====================================================
// P3 (model_p3 §2.1 item 5; v5 f1074, v6 f480 face zoom): per side an outer dark bottle-green strand with a lime streak
// that leaves the hood's upper side, sweeps out and down past the face to the shoulder and on down the chest, and an inner
// lime-olive strand along the mask edge. The strands are designed in UPRIGHT world space; hair_1 carries them down to its
// joint beside the chin, hair_2 on to the chest (<= 1.8 b from each joint, the part reach).
// P1 (model.md §3.5, v2 f2076 / f2040): broad dark slate ribbons from the cowl sides to the ground, turning outward as
// they fall, the ends splayed on the ground; one-sided below 2.5 b (R18).
// seg: which hair part carries the strand (1: the hood side down to the chin, 2: the chin down to the chest); [lo, hi] the arc
// span the part covers when a strand crosses the joint
const HAIR_P3 = {
  outer: {seg: [1], lime: false, cuts: [0, .3, .62, 1],
    w: t => .02 + .26 * Math.pow(Math.sin(Math.PI * Math.min(1, .06 + t * .9)), .9) * (1 - .3 * t),
    pts: [[.36, 8.48, -.8], [.76, 8.3, -1.06], [1.16, 7.86, -1.22], [1.43, 7.2, -1.26], [1.53, 6.5, -1.2], [1.5, 5.82, -1.12]]},
  outer2: {seg: [2], lime: false, cuts: [0, .5, 1],
    w: t => .02 + .2 * Math.pow(Math.sin(Math.PI * Math.min(1, .1 + t * .9)), .8),
    pts: [[1.28, 6.12, -1.14], [1.5, 5.5, -1.08], [1.76, 4.88, -.98], [1.92, 4.3, -.9]]},
  inner: {seg: [1, 2], lime: true, cut: 4,
    w: t => .04 + .17 * Math.pow(Math.sin(Math.PI * Math.min(1, .08 + t * .95)), .5),
    pts: [[.6, 8.02, -1.14], [.86, 7.56, -1.31], [.98, 6.9, -1.36], [.93, 6.3, -1.37], [.9, 5.96, -1.37],
      [.98, 5.45, -1.34], [1.13, 4.9, -1.26], [1.26, 4.35, -1.12]]},
};
const hairP3Paint = lime => ({t, s, d}) => {
  const R = PAL.p3_hair;
  let c = lime ? mix(PAL.p3_lime(clamp(.4 + .3 * t)), R(.5), .3) : R(clamp(.74 + .12 * t + .06 * (N.d(t * 9, s * 2) - .5)));
  if (!lime && s > .5) c = mix(c, R(clamp(.1 + .3 * t)), clamp((s - .5) / .15));        // the lime streak along the inner edge
  if (!lime && Math.abs(s + .25) < .08) c = mix(c, R(.95), .5);                          // a darker groove
  if (lime && Math.abs(s - .25) < .12) c = mix(c, PAL.p3_lime(.12), .5);                 // the lit ridge
  if (lime && s < -.5) c = mix(c, R(.6), .45);
  if (d < .018) c = PAL.p3_bottle(.95);
  return c;
};
function hairP3(seg) {
  const part = `hair_l_${seg}`, fr = partFrame(part, 'p3', oU), els = [];
  for (const [k, st] of Object.entries(HAIR_P3)) {
    if (!st.seg.includes(seg)) continue;
    const split = st.seg.length > 1, n = st.pts.length - 1;
    const P = !split ? st.pts : seg === 1 ? st.pts.slice(0, st.cut + 1) : st.pts.slice(st.cut);
    const T0 = !split || seg === 1 ? 0 : st.cut / n, T1 = !split ? 1 : seg === 1 ? st.cut / n : 1, g = t => T0 + (T1 - T0) * t;
    const cuts = st.cuts || [0, .5, 1];
    els.push(...ribbon(`p3_hair${seg}_${k}`, fr, P, t => st.w(g(t)), {cuts, paint: ({t, s, d}) => hairP3Paint(st.lime)({t: g(t), s, d}), ppb: 40, forms: 'p3', half: .03,
      face: t => (k === 'outer' && t < .45 ? [.15, .5, -1] : [.3, 0, -1]), side: () => [-1, -.3, 0], edge: st.lime ? 'hd_p3_hairin' : 'hd_p3_hairout'}));
  }
  return els;
}
tile('hd_p3_hairout', 16, 16, 32, (u, v) => PAL.p3_hair(clamp(.7 + .1 * N.b(u * 4, v * 4))), 'p3');
tile('hd_p3_hairin', 16, 16, 32, (u, v) => mix(PAL.p3_lime(.5), PAL.p3_hair(.45), .4), 'p3');
const DRAPE_P1 = {
  // from under the ear flare the ribbon sweeps out and down over the long arm, then falls to the ground and splays (v2 f2076)
  pts: [[.98, 3.28, -2.62], [1.5, 2.98, -2.72], [2.02, 2.52, -2.8], [2.4, 1.98, -2.84], [2.62, 1.38, -2.86], [2.8, .78, -2.88], [2.98, .28, -2.92], [3.12, .1, -2.96]],
  cut: 3, w: t => .13 + .2 * Math.pow(Math.sin(Math.PI * Math.min(1, .2 + .85 * t)), .6) + .08 * Math.pow(t, 4),
};
const drapeP1Paint = ({t, s, d}) => {
  let c = PAL.p1_slate(clamp(.55 + .2 * t + .08 * (N.d(t * 11, s * 3) - .5)));
  const gr = Math.abs(((s * 1.6 + t * .6) % 1 + 1) % 1 - .5); if (gr < .04) c = sink(c, .25);    // folds
  if (s > .55) c = mix(c, PAL.p1_slate(.2), clamp((s - .55) / .3) * .7);                         // the lit outer edge
  if (d < .05 && s < 0) c = mix(c, PAL.p1_bark(.55), .35);                                       // the pale underside peeking
  if (d < .018) c = PAL.p1_line(.85);
  return c;
};
function hairP1(seg) {
  const part = `hair_l_${seg}`, fr = partFrame(part, 'p1', solve(STANCES.CROUCH)), st = DRAPE_P1;
  const P = seg === 1 ? st.pts.slice(0, st.cut + 1) : st.pts.slice(st.cut);
  const T0 = seg === 1 ? 0 : st.cut / (st.pts.length - 1), T1 = seg === 1 ? st.cut / (st.pts.length - 1) : 1, w = t => st.w(T0 + (T1 - T0) * t);
  const faceOf = t => { const g = T0 + (T1 - T0) * t; return g < .4 ? [.25, .9, -1] : g < .82 ? [.6, .2, -1] : [.4, 1.2, -.5]; };
  const els = ribbon(`p1_hair${seg}`, fr, P, w, {cuts: seg === 1 ? [0, .5, 1] : [0, .45, .8, 1], face: faceOf, side: () => [0, 1, 0], paint: ({t, s, d}) => drapeP1Paint({t: T0 + (T1 - T0) * t, s, d}),
    ppb: 32, forms: 'p1', half: .035, edge: 'hd_p1_hedge', oneSide: seg === 2 ? [.6, .6, -.6] : [.3, .6, -1]});
  return els;
}
function hair(form, seg) { return form === 'p1' ? hairP1(seg) : hairP3(seg); }
// ---- region interface ------------------------------------------------------------------------------------------------------
let built = null;
export function models() {
  if (built) return built;
  const u = (els, n) => toUnits(autoSlot(els), PART_SCALE[n]);
  const out = {
    neck_p1: u(neckP1(), 'neck'), neck_p3: u(neckP3(), 'neck'), head_p1: u(headP1(), 'head'), head_p3: u(headP3(), 'head'),
    face_p1_bud: u(faceP1(), 'face'), face_p3: u(faceP3(), 'face'),
    hood_p1: u(hoodP1(), 'hood'), hood_p3: u(hoodP3(), 'hood'), crown_p1: u(crownP1(), 'crown'), crown_p3: u(crownP3(), 'crown'),
  };
  for (const f of ['p1', 'p3']) for (const seg of [1, 2]) { const m = u(hair(f, seg), `hair_l_${seg}`); out[`hair_l_${seg}_${f}`] = m; out[`hair_r_${seg}_${f}`] = mirrorX(m); }
  return (built = out);
}
export const FORM_MODELS = {
  neck: {p1: 'neck_p1', p3: 'neck_p3'}, head: {p1: 'head_p1', p3: 'head_p3'}, hood: {p1: 'hood_p1', p3: 'hood_p3'}, crown: {p1: 'crown_p1', p3: 'crown_p3'},
  ...Object.fromEntries(['l', 'r'].flatMap(s => [1, 2].map(g => [`hair_${s}_${g}`, {p1: `hair_${s}_${g}_p1`, p3: `hair_${s}_${g}_p3`}]))),
};
// the face look channel (contract §0.4.7): item -> model (+ the FACE_MUL colour); hidden = the empty model
export const FACE_ITEMS = {p1_bud: {model: 'face_p1_bud', form: 'p1'}, p3_idle: {model: 'face_p3', form: 'p3', face: 'p3_idle'},
  p3_charge: {model: 'face_p3', form: 'p3', face: 'p3_charge'}, p3_dim: {model: 'face_p3', form: 'p3', face: 'p3_dim'}, hidden: null};
export function sprites() { models(); return {...SP}; }

