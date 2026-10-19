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
//             from the HOOD (not the head, plan R2): the swing of the hood carries the hair roots from the cowl sides
//             (crouch) to the hood sides beside the face (upright), which the residual table needs (≤ 0.25 b).
// Region interface: see apep_body.mjs. P1 parts in world axes about the joint at the CROUCH stance, P3 at the UPRIGHT
// stance (solved here from apep_clips STANCES so the offsets follow the skeleton); the hair in its bone frame 'y'.
import {loft, slab, rockBox, crossCards, toUnits, mirrorX, stroke, sdUnion, registerTile} from './mboss_shape_lib.mjs';
import {PART_SCALE, J, solve, FORM_POINTS} from './apep_pose.mjs';
import {STANCES} from './apep_clips.mjs';
import {PAL, C, clamp, mix, N, lift, sink, grey, autoSlot, sprite, onRect, spriteSize, sdLeaf, cone, ball} from './apep_materials.mjs';
import {cardZ} from './mboss_model_lib.mjs';

export const REGION = 'head';
export const PARTS = ['neck', 'head', 'face', 'hood', 'crown', 'hair_l_1', 'hair_r_1', 'hair_l_2', 'hair_r_2'];
const SP = {};
const card = (name, rect, fn, ppb, forms, use = 'unique') => { const [w, h] = spriteSize(rect, ppb); SP[name] = sprite(w, h, ppb, onRect(rect, fn), forms, 'head', {use}); return name; };
const tile = (name, w, h, ppb, fn, forms) => { registerTile(name, w, h, ppb); SP[name] = sprite(w, h, ppb, (s, t) => fn(s, t), forms, 'head'); return name; };
const sinD = th => Math.sin(th * Math.PI / 180);
const lineOut = (c, d, w, L) => (d > -w ? mix(c, L, .85) : c);
const oneSided = (els, keep) => { for (const e of els) for (const f of Object.keys(e.faces)) if (!keep.includes(f)) delete e.faces[f]; return els; };
const sub = (a, b) => a.map((v, i) => v - b[i]);
const dist = (a, b) => Math.hypot(...sub(a, b));
const oU = solve(STANCES.UPRIGHT);
const UJ = n => oU[n].t;

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
  const els = loft('y', [{a: -.3, r: [.72, .42, .72, .7]}, {a: .5, r: [.8, .45, .8, .85]}, {a: 1.2, r: [.78, .42, .78, .82]}, {a: 1.72, r: [.5, .25, .5, .55]}], {tex: 'g_plate', caps: '-+', seed: 821});
  els.push(...slab({plane: 'z', at: f[2] - .02, rect: SCARF_R, sd: scarfSd, half: .05, sprite: card('p3_scarf', SCARF_R, scarfPaint, 48, 'p3'), edge: 'p3_lime', cell: .08}));
  return els;
}
// ================================================= face ==================================================================
const CRES_R = {u0: -.18, u1: .18, v0: -.08, v1: .08};
const cresPaint = (u, v) => { const a = Math.hypot(u, v + .2) - .25, b = Math.hypot(u, v + .26) - .25; if (a > 0 || b < 0) return null; return PAL.p1_seam(.15 + .3 * clamp(-a * 8)); };
function faceP1() {
  const f = FORM_POINTS.face.p1[1];
  const els = ball(f, .5, 'p1_bud', {sy: 1.25, seed: 831, n: 16});
  const sp = card('p1_crescent', CRES_R, cresPaint, 64, 'p1');
  for (const s of [1, -1]) els.push(cardZ(sp, -2.12, {X0: s * .32 - .18, X1: s * .32 + .18, Y0: -.5, Y1: -.34}, {flipU: s < 0}));
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
// ================================================= hood (the cowl; CROUCH frame about the hinge) ==============================
const COWL = [{a: .45, r: [1.0, .5, 1.0, .35], c: [0, .05]}, {a: -.3, r: [1.42, .62, 1.42, .62], c: [0, .02]}, {a: -.9, r: [1.55, .62, 1.55, .85], c: [0, -.02]},
  {a: -1.55, r: [1.25, .45, 1.25, .78], c: [0, -.3]}, {a: -2.12, r: [.42, .18, .42, .25], c: [0, -.74]}];
const EAR_R = {u0: -1.55, u1: -.2, v0: -.85, v1: .35};
const EAR = stroke([[-.3, .2], [-.8, -.05], [-1.2, -.4], [-1.48, -.78]], t => .3 * (1 - t) + .02);
const earPaint = (u, v) => { const n = EAR.near(u, v), hw = .3 * (1 - n.t) + .02; if (n.d > hw) return null; let g = .55 + .1 * (N.c(u * 6, v * 6) - .5) - .1 * n.t; if (n.d > hw - .04) g = .85; return grey(g); };
const FACEPLATE_R = {u0: -.75, u1: .75, v0: -1.0, v1: .12};
const faceplateSd = (u, v) => Math.max(Math.abs(u) - (.7 - .55 * clamp((-.2 - v) / .8)), v - .1, -.98 - v);
const faceplateP1 = (u, v) => { const d = faceplateSd(u, v); if (d > 0) return null; let c = PAL.p1_slate(clamp(.45 + .2 * (N.a(u * 6, v * 6) - .5))); const row = ((v * 3.2) % 1 + 1) % 1; if (row < .08) c = lift(c, .2); if (Math.abs(Math.abs(u) - (v + .82) * .55) < .045 && v < -.45 && v > -.82) c = PAL.p1_gold(.2); return lineOut(c, d, .04, PAL.p1_line(.7)); };
const faceplateP3 = (u, v) => { const d = faceplateSd(u, v); if (d > 0) return null; let c = PAL.p3_bottle(clamp(.4 + .2 * (N.a(u * 6, v * 6) - .5))); if (Math.abs(((u * 2.5 + v * 1.5) % 1 + 1) % 1 - .5) < .04) c = PAL.p3_rim(.4); return lineOut(c, d, .045, PAL.p3_rim(.3)); };
function hood(form) {
  const els = loft('z', COWL, {tex: (k, th) => (sinD(th) < -.35 ? (form === 'p1' ? 'p1_inner' : 'p3_inner') : 'g_plate'), caps: '+', seed: 841});
  // the cowl sides: plates hanging below the dome beside the face (P1: the cheek guards round the bud-skull; UPRIGHT: the
  // swing turns them into the hood rims reaching forward past the mask on both sides, so the face sits inside the cowl)
  const inner = form === 'p1' ? 'p1_inner' : 'p3_inner';
  const side = loft('z', [{a: .38, r: [.09, .22, .09, .3], c: [.98, -.3]}, {a: -.35, r: [.13, .4, .13, .62], c: [1.22, -.55]}, {a: -1.2, r: [.13, .42, .13, .66], c: [1.26, -.6]},
    {a: -1.9, r: [.1, .3, .1, .42], c: [1.0, -.52]}], {tex: (k, th) => (Math.cos(th * Math.PI / 180) < -.3 ? inner : 'g_plate'), caps: '-+', seed: 848});
  els.push(...side, ...mirrorX(side));
  const es = card('g_earcard', EAR_R, earPaint, 32, 'both', 'tinted');
  const ear = slab({plane: 'x', at: 1.42, rect: EAR_R, sd: EAR.sd, half: .05, sprite: es, edge: 'g_plate', cell: .09, rot: ['y', -22.5, [1.42, 0, -.3]]});
  els.push(...ear, ...mirrorX(ear));
  els.push(...slab({plane: 'z', at: -2.02, rect: FACEPLATE_R, sd: faceplateSd, half: .05, sprite: card(`${form}_faceplate`, FACEPLATE_R, form === 'p1' ? faceplateP1 : faceplateP3, 48, form), edge: 'g_plate', cell: .09}));
  if (form === 'p1') els.push(...cone([0, -.3, -2.06], .11, .42, 'p1_gold', {axis: 'z', sign: -1, seed: 842}));
  else {
    els.push(rockBox([-.2, -.48, -2.16], [.2, -.12, -2.06], 'g_plate', {seed: 843}), rockBox([-.14, -.42, -2.22], [.14, -.18, -2.12], 'p3_gem', {seed: 844}));
    for (const [x, y, z] of [[.55, .52, -.75], [-.55, .52, -.75], [0, .58, -.3]]) els.push(...cone([x, y, z], .1, .36, 'p3_emerald', {seed: 845 + x}));
  }
  return els;
}
// ================================================= crown ======================================================================
const SPRIG_R = {u0: -.38, u1: .38, v0: 0, v1: .7};
const sprigPaint = (u, v) => { for (const [cx, cy, a] of [[0, .45, 0], [-.18, .32, -.6], [.18, .32, .6], [-.25, .15, -1.0], [.25, .15, 1.0]]) { const ca = Math.cos(a), sa = Math.sin(a), x = (u - cx) * ca - (v - cy) * sa, y = (u - cx) * sa + (v - cy) * ca; const e = Math.hypot(x / .07, y / .2); if (e < 1) return e > .75 ? PAL.p1_sprig(.75) : PAL.p1_sprig(.1 + .3 * e); } if (Math.abs(u) < .02 && v < .4) return PAL.p1_sprig(.6); return null; };
function crownP1() {
  const b = sub([0, 4.33, -2.62], J.crown);
  const els = cone(b, .2, .72, 'p1_gold', {seed: 851});
  els.push(...crossCards(card('p1_sprig', SPRIG_R, sprigPaint, 48, 'p1'), [b[0], b[1] + .02, b[2] + .08], .76, .7, {y0: 0}));
  els.push(rockBox([b[0] - .09, b[1] + .36, b[2] - .14], [b[0] + .09, b[1] + .54, b[2] + .04], 'p1_seed', {seed: 852}));
  return els;
}
const FAN_R = {u0: -1.02, u1: 1.02, v0: -.25, v1: 1.02};
const FAN = Array.from({length: 9}, (_, i) => -1.4 + i * 2.8 / 8);
const fanSd = (u, v) => { let d = Infinity; for (const a of FAN) { const x = u * Math.cos(a) - v * Math.sin(a), y = u * Math.sin(a) + v * Math.cos(a); d = Math.min(d, sdLeaf(0, .12, .98, .14, {p: .9})(x, y)); } return Math.min(d, Math.hypot(u, v) - .2); };
const fanPaint = (u, v) => { const d = fanSd(u, v); if (d > 0) return null; const r = Math.hypot(u, v); let c = PAL.p3_crown(clamp(.1 + .45 * r + .1 * (N.b(u * 8, v * 8) - .5))); const a = Math.atan2(u, v); if (FAN.some(f => Math.abs(a + f) < .025)) c = PAL.p3_crown(.75); return lineOut(c, d, .025, PAL.p3_crown(.85)); };
function crownP3() {
  const F = FORM_POINTS.crown.p3[1];
  const rect = {u0: FAN_R.u0, u1: FAN_R.u1, v0: F[1] + FAN_R.v0, v1: F[1] + FAN_R.v1};
  const els = slab({plane: 'z', at: F[2] + .06, rect, sd: (u, v) => fanSd(u, v - F[1]), half: .03, sprite: card('p3_fan', FAN_R, fanPaint, 64, 'p3'), edge: 'p3_gold', cell: .08, core: false});
  els.push(...ball(F, .17, 'p3_bud', {seed: 861}));
  for (const s of [1, -1]) els.push(rockBox([s * .48 - .12, .08, -1.29], [s * .48 + .12, .32, -1.05], 'p3_emerald', {rot: ['z', 45, [s * .48, .2, -1.17]], seed: 862}));
  return els;
}
// ================================================= hair (bone frame 'y') =====================================================
const DRAPE_R = {u0: -.24, u1: .24, v0: -1.6, v1: .08};
const drapePaint = (tip, R, edge) => (u, v) => { const t = clamp(-v / 1.6), hw = tip ? .22 * (1 - t) + .015 : .22 - .04 * t; if (Math.abs(u) > hw) return null; let c = R(clamp(.55 + .2 * t + .1 * (N.d(u * 9, v * 5) - .5))); if (Math.abs(u) > hw - .035) c = edge(c); if (Math.abs(u - .05) < .03) c = mix(c, PAL.p3_hair(.1), R === PAL.p3_hair ? .7 : 0); return c; };
function hair(form, seg) {
  const L = seg === 1 ? dist(J.hair_l_2, J.hair_l_1) : dist([1.7, .2, -2.8], J.hair_l_2);
  const tip = seg === 2, R = form === 'p1' ? PAL.p1_slate : PAL.p3_hair, edge = form === 'p1' ? c => lift(c, .15) : c => mix(c, PAL.p3_rim(.4), .5);
  const sp = card(`${form}_hair${seg}`, DRAPE_R, drapePaint(tip, R, edge), 32, form);
  const strands = form === 'p1' ? [[0, .02]] : [[-.12, .03], [.13, -.03]];
  return strands.flatMap(([x, z]) => oneSided([cardZ(sp, z, {X0: x - .24, X1: x + .24, Y0: -L - .05, Y1: .08})], ['north']));
}
// ---- region interface ------------------------------------------------------------------------------------------------------
let built = null;
export function models() {
  if (built) return built;
  const u = (els, n) => toUnits(autoSlot(els), PART_SCALE[n]);
  const out = {
    neck_p1: u(neckP1(), 'neck'), neck_p3: u(neckP3(), 'neck'), head_p1: u(headP1(), 'head'), head_p3: u(headP3(), 'head'),
    face_p1_bud: u(faceP1(), 'face'), face_p3: u(faceP3(), 'face'),
    hood_p1: u(hood('p1'), 'hood'), hood_p3: u(hood('p3'), 'hood'), crown_p1: u(crownP1(), 'crown'), crown_p3: u(crownP3(), 'crown'),
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
