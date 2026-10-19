// HEAD region of the 아펩의 오아시스 파수꾼 rig (plan R4 parts 9-17): neck, head, face, hood, crown and the four hair parts.
//   neck      P1 the dark plate neck | P3 neck + the grey-green collar
//   head      P1 the skull base (inside the cowl) | P3 the skull behind the mask + the lime leaf scarf under the chin
//   face      P1 the closed pale bud-skull + the two pale-gold crescents on the cowl front (model.md §3.1)
//             | P3 the glowing oval mask 1.6 x 1.9 (centre (0, 6.9, -0.9) in the UPRIGHT stance) with the gold lily
//             emblem and the lime vein lines (model_p3 §2.1 item 1). The looks p3_idle / p3_charge (orange-gold, w1 f127) /
//             p3_dim are ONE model under three constant colours (apep_materials FACE_MUL); `hidden` is the empty model
//   hood      the cowl, authored once as it sits over the skull in the CROUCH stance for both forms (the hood_hinge
//             swings it back ~107 deg in the UPRIGHT stance: its front tip becomes the 8.5 b peak behind the face).
//             P1 dark slate plates, ear flares, the mid-face cone and the gold V | P3 bottle-green carapace, the
//             lime-gold front gem in a raised frame, emerald shards
//   crown     P1 the gold crown cone + leaf sprig + lime seed bulb on the cowl top | P3 the fan of gold leaves framing
//             the top of the face, the glowing bud at its centre, the brow emeralds (it rides the hood's front edge)
//   hair_<s>_1/2   P1 the dark drapes from the cowl sides to the ground | P3 the hair strands to the waist. The hair hangs
//             from the HOOD (not from the head as the plan R2 tree draws it): the swing of the hood carries the hair roots from the cowl sides
//             (crouch) to the hood sides beside the face (upright), which the residual table needs (≤ 0.25 b).
// Region interface: see apep_body.mjs. P1 parts in world axes about the joint at the CROUCH stance, P3 at the UPRIGHT
// stance (solved here from apep_clips STANCES so the offsets follow the skeleton); the hair in its bone frame 'y'.
import {loft, slab, rockBox, crossCards, toUnits, mirrorX, stroke, sdUnion, registerTile} from './mboss_shape_lib.mjs';
import {PART_SCALE, J, solve, FORM_POINTS} from './apep_pose.mjs';
import {STANCES} from './apep_clips.mjs';
import {PAL, C, clamp, mix, N, lift, sink, grey, autoSlot, sprite, onRect, onRectY, spriteSize, sdLeaf, cone, ball, TRANSPARENT} from './apep_materials.mjs';
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
const UJ = n => oU[n].t;
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
  const sF = card(`${name}_f`, R, paint(1), ppb, forms), sS = card(`${name}_s`, R, paint(-1), ppb, forms);
  const tanL = Math.tan(22.5 * D2R);
  const els = slab({plane: 'z', at: b[2], rect: {u0: b[0] + R.u0, u1: b[0] + R.u1, v0: b[1] + R.v0, v1: b[1] + R.v1}, sd: (u, v) => sdF(u - b[0], v - b[1]), half: .03, sprite: sF, edge: edge || sF, cell: .05, rot: lean ? ['x', -22.5, b] : null});
  // side card (plane x): the same outline sheared forward by the lean (u = z, toward -z with height)
  const RS = {u0: b[2] - w - tanL * h, u1: b[2] + w, v0: b[1] - .02, v1: b[1] + h};
  const sdS = (u, v) => sdF((u - b[2]) + (lean ? tanL * (v - b[1]) : 0), v - b[1]);
  const sS2 = card(`${name}_x`, {u0: RS.u0 - b[2], u1: RS.u1 - b[2], v0: -.02, v1: h}, (u, v) => paint(-1)(u + (lean ? tanL * v : 0), v), ppb, forms);
  els.push(...slab({plane: 'x', at: b[0], rect: RS, sd: sdS, half: .012, sprite: sS2, core: false}));
  void sS; void seed;
  return els;
}

// ---- tiles ------------------------------------------------------------------------------------------------------------------
tile('p1_bud', 64, 64, 48, (u, v) => { const r = ((u * 5 + .4 * Math.sin(v * 7)) % 1 + 1) % 1; let c = PAL.p1_bark(clamp(.05 + .3 * v + .1 * (N.a(u * 8, v * 8) - .5))); if (r < .07) c = PAL.p1_line(.55); return c; }, 'p1');
tile('p1_inner', 32, 32, 32, (u, v) => sink(PAL.p1_slate(.62 + .2 * N.a(u * 6, v * 6)), .4), 'p1');
tile('p3_inner', 32, 32, 32, (u, v) => { let c = sink(PAL.p3_bottle(.6 + .2 * N.b(u * 6, v * 6)), .3); if (Math.abs(((u * 3 + v) % 1) - .5) < .04) c = mix(c, PAL.p3_rim(.5), .5); return c; }, 'p3');
tile('p1_seed', 16, 16, 32, (u, v) => PAL.p1_core(clamp(.15 + .4 * Math.hypot(u - .5, v - .5))), 'p1');
tile('p3_bud', 32, 32, 32, (u, v) => PAL.p3_bud(clamp(.05 + .5 * Math.hypot(u - .5, v - .5) + .1 * N.c(u * 6, v * 6))), 'p3');
tile('p3_collar', 32, 32, 32, (u, v) => { let c = mix(PAL.p3_pale(.55), PAL.p3_bottle(.4), .45 + .2 * N.d(u * 5, v * 5)); if ((u * 6) % 1 < .1) c = sink(c, .2); return c; }, 'p3');

// ================================================= neck, head =================================================================
function neckP1() { const L = dist(J.head, J.neck); return loft('z', [{a: .3, r: .7}, {a: -L * .5, r: [.66, .62, .66, .58]}, {a: -L - .25, r: [.62, .58, .62, .55]}], {tex: 'g_plate', seed: 801}); }
function neckP3() {
  return [...loft('y', [{a: -.4, r: [.64, .56, .64, .62]}, {a: .3, r: [.6, .52, .6, .58]}, {a: .72, r: [.55, .48, .55, .55]}], {tex: 'g_plate', seed: 802}),
    ...loft('y', [{a: -.3, r: .9}, {a: -.05, r: .86}, {a: .12, r: .7}], {tex: 'p3_collar', caps: '-+', seed: 803})];
}
function headP1() { return loft('z', [{a: .25, r: [.7, .6, .7, .55]}, {a: -.6, r: [.74, .64, .74, .6], c: [0, -.05]}, {a: -1.3, r: [.55, .45, .55, .48], c: [0, -.15]}], {tex: 'p1_inner', caps: '-+', seed: 811}); }
// the P3 skull: behind the mask, from the chin to the face top; the leaf scarf wraps the chin and throat
const SCARF_R = {u0: -.82, u1: .82, v0: -.42, v1: .3};
const scarfSd = (u, v) => { const outer = Math.hypot(u / .8, (v - .3) / .7) - 1, inner = Math.hypot(u / .52, (v - .32) / .42) - 1; return Math.max(outer, -inner); };
const scarfPaint = (u, v) => { const d = scarfSd(u, v); if (d > 0) return null; let c = PAL.p3_lime(clamp(.15 + .25 * (N.a(u * 7, v * 7) - .5) + .3 * (-v))); const lf = Math.abs(((Math.atan2(v - .3, u) * 3) % 1 + 1) % 1 - .5); if (lf < .05) c = mix(c, PAL.p3_line(.4), .6); return lineOut(c, d, .03, PAL.p3_line(.6)); };
function headP3() {
  const f = FORM_POINTS.face.p3[1];   // the mask centre offset from the head joint (upright)
  const els = loft('y', [{a: -.3, r: [.62, .36, .62, .5]}, {a: .25, r: [.66, .38, .66, .56]}, {a: .62, r: [.5, .3, .5, .46]}], {tex: 'hd_p3_lining', caps: '-+', seed: 821});
  els.push(...slab({plane: 'z', at: f[2] - .02, rect: SCARF_R, sd: scarfSd, half: .05, sprite: card('p3_scarf', SCARF_R, scarfPaint, 48, 'p3'), edge: 'p3_lime', cell: .08}));
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
function maskPaint(u, v) {
  const d = maskSd(u, v);
  if (d > 0) return null;
  let c = PAL.p3_face(clamp(.1 + .35 * (d + 1) * .5 + .08 * (N.a(u * 6, v * 6) - .5)));
  // vein lines radiating from the emblem, darker lime
  const ang = Math.atan2(v - .25, u), vr = Math.abs(((ang * 4 / Math.PI) % 1 + 1) % 1 - .5);
  if (vr < .035 && Math.hypot(u, v - .25) > .35) c = mix(c, PAL.p3_line(.2), .55);
  // the gold lily emblem in the upper half: three leaves round a drop
  const lx = u, ly = v - .32;
  const leaf = (cx, cy, rot) => { const ca = Math.cos(rot), sa = Math.sin(rot), x = (lx - cx) * ca + (ly - cy) * sa, y = -(lx - cx) * sa + (ly - cy) * ca; return Math.hypot(x / .09, y / .22) - 1; };
  const em = Math.min(leaf(0, .14, 0), leaf(-.15, .02, -.9), leaf(.15, .02, .9), Math.hypot(lx / .08, (ly + .12) / .11) - 1);
  if (em < 0) c = mix(PAL.p3_sternum(.15), PAL.p3_sternum(.5), clamp(-em * 2));
  else if (em < .25) c = mix(c, PAL.p3_line(.35), .5 * (1 - em / .25));
  // two leaf shapes framing the lower half
  for (const s of [1, -1]) { const x = u - s * .42, y = v + .45; if (Math.hypot(x / .2, y / .38) < 1 && Math.hypot((x + s * .08) / .14, y / .3) > 1) c = mix(c, PAL.p3_line(.25), .5); }
  return lineOut(c, d, .05, PAL.p3_line(.5));
}
function faceP3() {
  const f = FORM_POINTS.face.p3[1];
  const rect = {u0: MASK_R.u0, u1: MASK_R.u1, v0: f[1] + MASK_R.v0, v1: f[1] + MASK_R.v1};
  const els = slab({plane: 'z', at: f[2], rect, sd: (u, v) => maskSd(u, v - f[1]), half: .07, sprite: card('p3_mask', MASK_R, maskPaint, 64, 'p3'), edge: 'p3_gold', cell: .1});
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
  {z0: -.15, z1: .42, tongue: .18, r: [.98, .6, .98, .3], c: [0, -.25], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'round'},
  {z0: .12, z1: -.5, tongue: .28, r: [1.28, .775, 1.28, .45], c: [0, -.25], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'tip'},
  {z0: -.42, z1: -.92, tongue: .26, r: [1.19, .7, 1.19, .48], c: [0, -.27], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'split'},
  {z0: -.84, z1: -1.28, tongue: .24, r: [1.07, .58, 1.07, .5], c: [0, -.32], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'tip'},
  {z0: -1.2, z1: -1.56, tongue: .22, r: [.96, .55, .96, .5], c: [0, -.36], ks: [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], shape: 'split'},
  {z0: -1.5, z1: -1.82, tongue: .16, r: [.76, .4, .76, .48], c: [0, -.42], ks: [0, 1, 2, 3, 4, 5, 6, 7, 8], shape: 'round'},
];
// the inner volume under the plates (fills the steps; its underside is the dark lining seen in the rear-up)
const P1_CORE = [{a: .5, r: [.84, .48, .84, .2], c: [0, -.25]}, {a: .05, r: [1.1, .62, 1.1, .36], c: [0, -.25]}, {a: -.5, r: [1.06, .58, 1.06, .4], c: [0, -.27]},
  {a: -.9, r: [.95, .5, .95, .42], c: [0, -.32]}, {a: -1.25, r: [.84, .44, .84, .44], c: [0, -.36]}, {a: -1.55, r: [.64, .3, .64, .42], c: [0, -.42]}, {a: -1.82, r: [.46, .16, .46, .3], c: [0, -.5]}];
// ear flare (plane z, turned 22.5 deg about x so it faces forward-up): a leaf sweeping out and up from the dome side
const EAR1_R = {u0: .8, u1: 2.3, v0: -.1, v1: 1.0};
const EAR1_W = t => .2 * Math.pow(Math.sin(Math.PI * Math.min(1, .22 + t * .8)), .6) + .012;
const EAR1 = stroke([[.95, .22], [1.3, .3], [1.65, .38], [1.95, .52], [2.12, .72], [2.2, .9]], EAR1_W);
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
const P3PL = (lime, peel) => (s, t, d) => {
  const g = N.a(s * 2 + t * 5, t * 7) - .5;
  let c = lime ? PAL.p3_lime(clamp(.42 + .15 * g + .15 * (1 - t))) : mix(PAL.p3_bottle(clamp(.62 + .12 * g + .12 * (1 - t))), PAL.p1_slate(clamp(.4 + .1 * g)), .45);
  if (t < .16) c = sink(c, .35 * (1 - t / .16));
  if (Math.abs(s) < .05 && t > .2) c = mix(c, PAL.p3_line(.5), .35);
  const fl = Math.abs(((Math.abs(s) * 1.6 + t * 2.2) % 1) - .5); if (fl < .035 && t > .25) c = mix(c, lime ? PAL.p3_line(.45) : PAL.p3_bottle(.85), .5);
  if (peel) { const pe = N.e(s * 2.2 + 3, t * 3.1 + 1); if (pe > .62 && t > .2) c = mix(PAL.p3_pale(.35), PAL.p3_pale(.6), clamp((pe - .62) * 6)); }
  if (d < .05) c = mix(PAL.p3_rim(.1), PAL.p3_rim(.4), clamp(d / .05));                // the lime rim
  if (d < .016) c = PAL.p3_bottle(.95);                                                  // near-black outline
  return c;
};
tile('hd_p3_hedge', 16, 16, 32, (u, v) => PAL.p3_rim(clamp(.3 + .15 * N.b(u * 4, v * 4))), 'p3');
tile('hd_p3_lining', 32, 32, 32, (u, v) => { let c = PAL.p3_bottle(clamp(.72 + .12 * N.b(u * 6, v * 6))); if (Math.abs(((u * 2 + v * .5) % 1) - .5) < .03) c = mix(c, PAL.p3_rim(.6), .35); return c; }, 'p3');
// rows (tongues toward the front = up the hood when upright); the bottom facets (k -2 / 5) are left open
const P3_ROWS = [
  {z0: -.1, z1: .52, tongue: .2, r: [.98, .5, .98, .55], c: [0, -.42], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'round'},
  {z0: .14, z1: -.55, tongue: .3, r: [1.16, .64, 1.16, .62], c: [0, -.45], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'tip'},
  {z0: -.45, z1: -1.08, tongue: .28, r: [1.06, .57, 1.06, .6], c: [0, -.5], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'split'},
  {z0: -.98, z1: -1.5, tongue: .26, r: [.86, .46, .86, .52], c: [0, -.58], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'tip'},
  {z0: -1.4, z1: -1.86, tongue: .32, r: [.58, .33, .58, .4], c: [0, -.68], n: 8, phase: 22.5, ks: [-1, 0, 1, 2, 3, 4], shape: 'tip'},
];
const P3_CORE = [{a: .55, r: [.86, .4, .86, .3], c: [0, -.42]}, {a: .1, r: [1.06, .52, 1.06, .36], c: [0, -.45]}, {a: -.5, r: [.98, .48, .98, .36], c: [0, -.5]},
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
// the veil frame round the mask: the hole a little larger than the mask (0.8 x 0.95 about (0, 6.9)), the outer edge
// running from the peak (8.55) out over the brows and down the cheeks to the shoulders (open under the chin)
const holeE = (x, H) => Math.hypot(x / .88, (H - 6.92) / 1.02) - 1;
const archOut = H => (H > 8.55 ? -1 : H > 7.7 ? 1.08 * Math.pow((8.55 - H) / .85, .6) : H > 6.4 ? 1.08 + .04 * Math.sin((7.7 - H) * 2.4) : 1.08 - .5 * Math.pow((6.4 - H) / .7, 1.4));
const archSd = (x, H) => Math.max(Math.abs(x) - archOut(H), -holeE(x, H) * .9, 5.7 - H);
const archPaint = (x, H, d) => {
  const e = holeE(x, H);
  let c = PAL.p3_bottle(clamp(.62 - .18 * clamp((H - 6) / 2.5) + .08 * (N.a(x * 4, H * 4) - .5)));
  const vein = Math.abs(((Math.atan2(x, H - 9.2) * 9) % 1 + 1) % 1 - .5); if (vein < .035 && e > .2) c = mix(c, PAL.p3_bottle(.3), .4);
  if (e < .1) c = mix(PAL.p3_rim(.05), PAL.p3_rim(.4), clamp(e / .1));                // the lime rim round the face
  else if (Math.abs(x) > archOut(H) - .07) c = mix(c, PAL.p3_rim(.45), .7);             // the outer lime line
  if (d < .014) c = PAL.p3_bottle(.95);
  return c;
};
// the side walls joining the frame back to the shell sides (plane x; u = model z, v = model y)
const WALL_R = {u0: -1.12, u1: .72, v0: -1.42, v1: -.74};
const wallY = z => -.83 - .54 * clamp((.68 - z) / 1.72) / 1 * 1;     // the frame's model y along z (chin .68 .. brow -1.04)
const wallSd = (u, v) => Math.max(v - (-.76), wallY(u) + .02 - v, u - .7, -1.1 - u);
const wallPaint = (u, v) => { const d = -wallSd(u, v); if (d < 0) return null; let c = PAL.p3_bottle(clamp(.72 + .1 * (N.b(u * 6, v * 6) - .5))); if (Math.abs(((u * 2.2 + v * 3) % 1 + 1) % 1 - .5) < .03) c = mix(c, PAL.p3_rim(.6), .3); if (v - wallY(u) < .07) c = mix(PAL.p3_rim(.1), PAL.p3_rim(.4), clamp((v - wallY(u)) / .07)); return c; };
// the horns: the P1 ear flares grown into dark leaf horns sweeping out and up from the upper sides of the hood
const HORN = stroke([[.82, 7.62], [1.15, 7.85], [1.42, 8.15], [1.56, 8.5], [1.52, 8.86]], t => .2 * Math.pow(Math.sin(Math.PI * Math.min(1, .25 + .78 * t)), .7) + .015);
const hornSd = (x, H) => HORN.sd(Math.abs(x), H);
const hornPaint = (x, H, d) => { const n = HORN.near(Math.abs(x), H); let c = PAL.p3_bottle(clamp(.58 + .1 * (N.c(x * 5, H * 5) - .5) - .2 * n.t)); if (Math.abs(n.s) < .015) c = mix(c, PAL.p3_bottle(.85), .5); if (n.s < 0 && d < .06) c = mix(PAL.p3_rim(.1), PAL.p3_rim(.4), d / .06); if (d < .014) c = PAL.p3_bottle(.95); return c; };
// the brow emeralds: cut crystals on the frame beside the mask's upper half (lit facets up-left)
const browGemSd = (x, H) => Math.abs(Math.abs(x) - .98) / .19 + Math.abs(H - 7.62) / .3 - 1;
const browGemPaint = (x, H) => { const dx = Math.abs(x) - .98, dy = H - 7.62; let t = dx < 0 ? (dy > 0 ? .1 : .35) : (dy > 0 ? .25 : .55); if (Math.abs(dx) < .012 || Math.abs(dy) < .012) t += .15; if (Math.abs(dx) / .19 + Math.abs(dy) / .3 > .82) t = .75; return PAL.p3_emerald(t); };
function hoodP3() {
  const els = [];
  P3_ROWS.forEach((row, i) => els.push(...plateRing({...row, half: .045, edge: 'hd_p3_hedge', name: `hd_p3_hp${i}`, forms: 'p3',
    paintOf: k => ((k === 1 || k === 2) && i === 4 ? ['l', P3PL(true, false)] : ['', P3PL(false, (k === 1 && i === 1) || (k === 2 && i === 3) || (k === 0 && i === 2))])})));
  els.push(...loft('z', P3_CORE, {tex: 'hd_p3_lining', caps: '+', seed: 861, skip: (k, th) => Math.sin(th * D2R) < -.3}));
  // the veil frame round the mask (>= 0.2 b in front of it), the horns behind its upper corners, the brow emeralds
  els.push(...frontPlate('hd_p3_arch', -1.16, 6.9, archSd, archPaint, {box: [-1.25, 1.25, 5.7, 8.6]}));
  const wall = slab({plane: 'x', at: 1.02, rect: WALL_R, sd: wallSd, half: .03, sprite: card('hd_p3_wall', WALL_R, wallPaint, 32, 'p3'), edge: 'hd_p3_lining', cell: .07});
  els.push(...wall, ...mirrorX(wall));
  els.push(...frontPlate('hd_p3_horns', -.82, 8.2, hornSd, hornPaint, {box: [-1.8, 1.8, 7.4, 8.95]}));
  els.push(...frontPlate('hd_p3_browgem', -1.3, 7.62, browGemSd, browGemPaint, {box: [-1.2, 1.2, 7.28, 7.96], half: .07, edge: 'p3_emerald', ppb: 64}));
  // the square lime-gold gem in its raised dark frame near the carapace front, emerald shards along the crest / back
  els.push(rockBox([-.2, -.3, -1.78], [.2, -.16, -1.38], 'hd_p3_hedge', {seed: 863}), rockBox([-.14, -.2, -1.72], [.14, -.1, -1.44], 'p3_gem', {seed: 864}));
  for (const [x, y, z, h] of [[0, .14, -.3, .42], [.38, .08, -.65, .32], [-.38, .08, -.65, .32], [.5, -.02, .05, .3], [-.5, -.02, .05, .3], [0, .02, -1.05, .3]]) els.push(...crystal(`hd_p3_shard`, [x, y, z], .07, h, PAL.p3_emerald, {forms: 'p3', ppb: 48, edge: 'p3_emerald'}));
  return els;
}
// ================================================= crown ======================================================================
// P1 crown (model.md §3.1, v1 f255): the lemon-gold cone (0.78 b, leaning 22.5 deg forward; its tip is FORM_POINTS
// crown p1) rising from a dark collar on the crest ridge, two gold leaf sprigs fanned round its foot and the small glowing
// lime seed bulb in front of it
const SPRIG_R = {u0: -.42, u1: .42, v0: 0, v1: .62};
const SPRIGS = [[0, .02, 0], [-.05, .04, -.75], [.05, .04, .75]];
const sprigPaint = (u, v) => {
  for (const [x0, y0, a] of SPRIGS) {
    const ca = Math.cos(a), sa = Math.sin(a), x = (u - x0) * ca - (v - y0) * sa, y = (u - x0) * sa + (v - y0) * ca;   // y along the branch
    if (y < 0 || y > .56) continue;
    if (Math.abs(x) < .012) return PAL.p1_sprig(.55);
    for (let i = 0; i < 5; i++) {
      const ly = .12 + i * .1, side = i % 2 ? 1 : -1, ang = side * .9, lx = x - side * .015, yy = y - ly;
      const px = lx * Math.cos(ang) - yy * Math.sin(ang), py = lx * Math.sin(ang) + yy * Math.cos(ang);
      const e = Math.hypot(px / .032, (py - side * .0) / .075);
      if (e < 1 && px * side * 0 === 0 && Math.hypot(lx, yy) < .11) return e > .7 ? PAL.p1_sprig(.75) : PAL.p1_sprig(.05 + .3 * e + .1 * i / 5);
    }
    if (y > .5 && Math.hypot(x, y - .53) < .04) return PAL.p1_sprig(.15);
  }
  return null;
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
const goldLeafPaint = (a, r) => { const d = -goldLeafSd(a, r); if (d < 0) return null; let c = PAL.p3_crown(clamp(.5 - .4 * (r / .98) + .12 * Math.abs(a) / .12 + .06 * (N.b(a * 9, r * 9) - .5))); if (Math.abs(a) < .012 && r < .85) c = PAL.p3_crown(.75); const vein = Math.abs(((r * 7 - Math.abs(a) * 10) % 1 + 1) % 1 - .5); if (vein < .06 && Math.abs(a) > .02 && r > .15) c = mix(c, PAL.p3_crown(.6), .4); if (d < .014) c = PAL.p3_crown(.9); return c; };
function crownP3() {
  const F = FORM_POINTS.crown.p3[1];
  const els = [...ball(F, .19, 'p3_bud', {seed: 861, n: 8})];
  const sv = card('hd_p3_leaf_v', LEAF_V, (u, v) => goldLeafPaint(u, v), 64, 'p3'), sh = card('hd_p3_leaf_h', LEAF_H, (u, v) => goldLeafPaint(v, Math.abs(u)), 64, 'p3');
  const r0 = .12;
  [-90, -67.5, -45, -22.5, 0, 22.5, 45, 67.5, 90].forEach((phi, i) => {
    const z = F[2] + .05 + (i % 2) * .05, piv = [F[0], F[1], z];
    if (Math.abs(phi) <= 45) {
      const k = .8 + .2 * Math.abs(phi) / 90;   // the upright leaves shorter (the fan stays under the 9.0 b top)
      const rect = {u0: F[0] + LEAF_V.u0, u1: F[0] + LEAF_V.u1, v0: F[1] + r0, v1: F[1] + r0 + LEAF_V.v1 * k};
      els.push(...slab({plane: 'z', at: z, rect, sd: (u, v) => goldLeafSd(u - F[0], (v - F[1] - r0) / k), half: .02, sprite: sv, edge: 'p3_gold', cell: .05, rot: phi ? ['z', -phi, piv] : null}));
    } else {
      const sx = Math.sign(phi), g = sx > 0 ? 90 - phi : -(90 + phi);
      const rect = sx > 0 ? {u0: F[0] + r0, u1: F[0] + r0 + .98, v0: F[1] - .13, v1: F[1] + .13} : {u0: F[0] - r0 - .98, u1: F[0] - r0, v0: F[1] - .13, v1: F[1] + .13};
      const sp = sx > 0 ? sh : card('hd_p3_leaf_h2', {u0: -.98, u1: 0, v0: -.13, v1: .13}, (u, v) => goldLeafPaint(v, Math.abs(u)), 64, 'p3');
      els.push(...slab({plane: 'z', at: z, rect, sd: (u, v) => goldLeafSd(v - F[1], Math.abs(u - F[0]) - r0), half: .02, sprite: sp, edge: 'p3_gold', cell: .05, rot: g ? ['z', g, piv] : null}));
    }
  });
  // three leaves swept back over the hood (plane x, tilted back about x)
  for (const [x, tilt] of [[0, 45], [.1, 22.5], [-.1, 22.5]]) {
    const k = .85, rect = {u0: F[2] - .13, u1: F[2] + .13, v0: F[1] + r0, v1: F[1] + r0 + .98 * k};
    els.push(...slab({plane: 'x', at: F[0] + x, rect, sd: (u, v) => goldLeafSd(u - F[2], (v - F[1] - r0) / k), half: .02, sprite: card('hd_p3_leaf_x', {u0: -.13, u1: .13, v0: 0, v1: .98}, (u, v) => goldLeafPaint(u, v), 64, 'p3'), edge: 'p3_gold', cell: .05, rot: ['x', tilt, [F[0] + x, F[1], F[2]]]}));
  }
  return els;
}
// ================================================= hair (bone frame 'y') =====================================================
const DRAPE_R = {u0: -.24, u1: .24, v0: -1.6, v1: .08}, DRAPE_W = {p1: 1.9, p3: 1};
const drapePaint = (tip, R, edge) => (u, v) => { const t = clamp(-v / 1.6), hw = tip ? .22 * (1 - t) + .015 : .22 - .04 * t; if (Math.abs(u) > hw) return null; let c = R(clamp(.55 + .2 * t + .1 * (N.d(u * 9, v * 5) - .5))); if (Math.abs(u) > hw - .035) c = edge(c); if (Math.abs(u - .05) < .03) c = mix(c, PAL.p3_hair(.1), R === PAL.p3_hair ? .7 : 0); return c; };
function hair(form, seg) {
  const L = seg === 1 ? dist(J.hair_l_2, J.hair_l_1) : dist([1.7, .2, -2.8], J.hair_l_2);
  const tip = seg === 2, R = form === 'p1' ? PAL.p1_slate : PAL.p3_hair, edge = form === 'p1' ? c => lift(c, .15) : c => mix(c, PAL.p3_rim(.4), .5);
  const sp = card(`${form}_hair${seg}`, DRAPE_R, drapePaint(tip, R, edge), 32, form), w = .24 * DRAPE_W[form];
  const strands = form === 'p1' ? [[0, .02]] : [[-.12, .03], [.13, -.03]];
  return strands.flatMap(([x, z]) => oneSided([cardZ(sp, z, {X0: x - w, X1: x + w, Y0: -L - .05, Y1: .08})], ['north']));
}
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
void [C, sdUnion, UJ, grey];
