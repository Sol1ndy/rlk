// Shared materials of the 아펩의 오아시스 파수꾼 rig: the palette ramps of both forms (model.md §7.1, model_p3.md §7, de-hazed),
// the TINT SLOTS that let one grey sprite serve both forms (plan R13), the tint looks (R12), the tile sprites several
// regions use, and small painting / shape helpers. Co-owned by the region modules (apep_{head,body,limbs,hands,tail}.mjs):
// a change here repaints every region, so keep the names and the texel densities (ppb) stable.
//
// TINT SLOTS (plan R12 / R13). Every face of every model carries a tintindex = its material slot:
//   0 paint   a unique, full-colour sprite (white in the plain item, so it shows as painted)
//   1 shell   grey shell / bark plates: P1 pale bark, P3 pale grey (limbs, rib slabs, side plates, belly scales)
//   2 plate   grey dark plates: P1 slate, P3 bottle green (hump, dorsal plates, hood shell, mantle, leg armour)
//   3 band_a  the tail's pale band (P1 pale, P3 pale grey-white)
//   4 band_b  the tail's dark band (P1 slate, P3 dark green)
// An item definition carries one constant tint per slot: the form's slot colours, multiplied by the tint look's colour
// (p1_dark, p1_brown, withered, p3_dim) and by the face look's colour (p3_charge, p3_dim). No face is ever untinted (the
// builder counts them per look), so a tint look darkens the whole body, the glows included.
import {C, clamp, smooth, mix, fbm, TRANSPARENT} from './mboss_paint_lib.mjs';
import {registerTile, registerWrap} from './mboss_shape_lib.mjs';

export {C, clamp, smooth, mix, fbm, TRANSPARENT};
export const ramp = list => { const cs = list.map(C); return t => { const x = clamp(t) * (cs.length - 1), i = Math.min(cs.length - 2, Math.floor(x)); return mix(cs[i], cs[i + 1], x - i); }; };
// ---- palette (hi -> deep) ----------------------------------------------------------------------------------------------
export const PAL = {
  // phase 1 (model.md §7.1)
  p1_slate: ramp(['#7E8572', '#5E665C', '#47504A', '#39413B', '#2C332E', '#1D231F']),
  p1_bark: ramp(['#E2DCC8', '#CFC9B2', '#B9B49C', '#9F9A82', '#7E7A64', '#5A5745']),
  p1_line: ramp(['#696D4F', '#5A6459', '#4A4C3C', '#3E3D30', '#2C2B20', '#1A1A12']),
  p1_gold: ramp(['#FFF9B0', '#FCEB6A', '#EED64C', '#D2BA3A', '#A8902C', '#6E5A12']),
  p1_cone: ramp(['#FEF2AB', '#F1D68B', '#DDBF7A', '#C4A86A', '#A08A55', '#6F5F38']),
  p1_gem: ramp(['#FFFFA0', '#FEFD61', '#F8EC55', '#EAD849', '#D8C546', '#B8A242']),
  p1_sprig: ramp(['#F4E3A0', '#ECD585', '#D6BE71', '#AC9C69', '#8B7A47', '#62532C']),
  p1_core: ramp(['#F4FBE4', '#E2F4BA', '#CBDB99', '#AEB877', '#808C53', '#394435']),
  p1_seam: ramp(['#F2F0C8', '#E2E2B0', '#C8CC94', '#A7AE78', '#848C5C', '#5E6542']),
  p1_tail: ramp(['#C9C6B4', '#B0AE9C', '#8A8874', '#4B5348', '#3B4236', '#282D21']),
  // phase 3 (model_p3.md §7)
  p3_bottle: ramp(['#8DB878', '#5E8C4E', '#436F39', '#2F5A2E', '#1E4426', '#12301B']),
  p3_rim: ramp(['#E2F7A0', '#C3EA7C', '#A0D45E', '#7EB548', '#5E9238', '#416E28']),
  p3_lime: ramp(['#E6EE98', '#CFDC7C', '#B2C25C', '#91A444', '#6C7B2F', '#4A5A18']),
  p3_leafhand: ramp(['#F0EDB0', '#DCDA8C', '#C5C770', '#A7AE55', '#808A3A', '#5A6326']),
  p3_pale: ramp(['#E8EAE2', '#D3D6CB', '#BBC0B2', '#9EA597', '#7C8478', '#5A6258']),
  p3_line: ramp(['#7A8A3C', '#5E6E28', '#4A5A1E', '#3A4716', '#2A3410', '#1A2209']),
  p3_emerald: ramp(['#E2FF9C', '#BCF53E', '#8FE23E', '#5CC72E', '#3A991A', '#1F6614']),
  p3_face: ramp(['#FBFCC8', '#EEF29A', '#D8E27A', '#B9C95A', '#96A840', '#6E7F2A']),
  p3_sternum: ramp(['#FCFCC4', '#F4F2A0', '#DCDC74', '#BABB52', '#94963A', '#686A24']),
  p3_crown: ramp(['#F6E9AE', '#EEDE92', '#D9C47A', '#BBA45E', '#8F7D3E', '#5F5226']),
  p3_bud: ramp(['#FAFDD0', '#F5F9A7', '#E7EF8A', '#D3E169', '#A9C24A', '#7CA041']),
  p3_gem: ramp(['#FFFBB0', '#FEF585', '#F9F04B', '#F3DA49', '#E2C439', '#A8902C']),
  p3_cone: ramp(['#F7F3C4', '#F2EFB1', '#E2D79C', '#CEC58B', '#B0A570', '#857B4E']),
  p3_cone_gold: ramp(['#FBF8A8', '#F4F07A', '#E9E042', '#D3C93A', '#AFA230', '#7C7222']),
  p3_robe: ramp(['#5E7E68', '#476C55', '#34503F', '#263D33', '#1A2B25', '#101B17']),
  p3_hair: ramp(['#B8E084', '#8DBC5D', '#5F8C40', '#3A6229', '#234519', '#132E0F']),
  p3_beads: ramp(['#F6FAF4', '#E2EDE0', '#C3D3BF', '#6E9A58', '#4C7340', '#30502C']),
};
export const lift = (c, k) => mix(c, [255, 252, 238, 255], clamp(k));
export const sink = (c, k) => mix(c, [14, 16, 10, 255], clamp(k));
export const N = {a: fbm(1101), b: fbm(1211), c: fbm(1307), d: fbm(1401), e: fbm(1503)};
export const grey = v => { const g = Math.round(clamp(v) * 255); return [g, g, g, 255]; };

// ---- tint slots and looks ---------------------------------------------------------------------------------------------------
export const SLOTS = ['paint', 'shell', 'plate', 'band_a', 'band_b'];
export const SLOT = Object.fromEntries(SLOTS.map((s, i) => [s, i]));
// form colours per slot (multiplied onto the grey sprites; the sprites keep their own light and dark)
export const SLOT_COLOR = {
  p1: {paint: '#FFFFFF', shell: '#E9E1C8', plate: '#8C9583', band_a: '#D6D2BE', band_b: '#8E9888'},
  p3: {paint: '#FFFFFF', shell: '#EDF0E5', plate: '#6FA45C', band_a: '#B6E6B4', band_b: '#5E7A66'},
};
// tint looks (R12): ids and colours as the contract (§0.4.7); the forms each applies to
export const TINT_IDS = {none: 0, p1_dark: 1, p1_brown: 2, withered: 3, p3_dim: 4};
export const TINT_COLOR = {p1_dark: '#2D2A04', p1_brown: '#605D37', withered: '#8C8458', p3_dim: '#6F8A73'};
export const TINT_FORMS = {p1_dark: ['p1'], p1_brown: ['p1'], withered: ['p3'], p3_dim: ['p3']};
// face looks that are the same model under a constant colour (one mask sprite, three looks: R13)
export const FACE_MUL = {p3_idle: '#FFFFFF', p3_charge: '#FFC06A', p3_dim: '#9AA88A'};
const rgb = h => [parseInt(h.slice(1, 3), 16) / 255, parseInt(h.slice(3, 5), 16) / 255, parseInt(h.slice(5, 7), 16) / 255];
const toInt = c => (Math.round(clamp(c[0]) * 255) << 16) | (Math.round(clamp(c[1]) * 255) << 8) | Math.round(clamp(c[2]) * 255);
// the tints list of an item: form slot colours x the face-look colour (optional) x the tint look's colour (optional)
export function itemTints(form, {tint = null, face = null} = {}) {
  const k = [1, 1, 1].map((v, i) => v * (tint ? rgb(TINT_COLOR[tint])[i] : 1) * (face ? rgb(FACE_MUL[face])[i] : 1));
  return SLOTS.map(s => toInt(rgb(SLOT_COLOR[form][s]).map((v, i) => v * k[i])));
}
// Set the slot of every face of a model's elements (all faces: no untinted face).
export const slotted = (els, slot) => { for (const e of els) for (const f of Object.values(e.faces)) f.tintindex = typeof slot === 'number' ? slot : SLOT[slot]; return els; };
// Slot of a sprite name (sprites listed in TINTED_SPRITES are grey and take their slot; everything else is paint).
export const TINTED_SPRITES = {g_shell: 'shell', g_plate: 'plate', g_tail_a: 'band_a', g_tail_b: 'band_b', g_flap_a: 'plate', g_flap_b: 'plate', g_flapin_a: 'shell', g_flapin_b: 'shell',
  g_ribcard: 'shell', g_lobe: 'shell', g_sidecard: 'shell', g_bladecard: 'shell', g_platecard: 'plate', g_earcard: 'plate'};
export function autoSlot(els) {
  for (const e of els) for (const f of Object.values(e.faces)) { const t = f.texture.slice(1); f.tintindex = SLOT[TINTED_SPRITES[t] || 'paint']; }
  return els;
}

// ---- cell noise (plates, scales) -------------------------------------------------------------------------------------------
const h2 = (i, j, s) => { let n = (i * 374761393 + j * 668265263 + s * 2246822519) | 0; n = (n ^ (n >>> 13)) * 1274126177 | 0; return ((n ^ (n >>> 16)) >>> 0) / 4294967295; };
export function cells(x, y, seed = 1, per = 0, jit = .8) {
  const xi = Math.floor(x), yi = Math.floor(y);
  let d1 = 9, d2 = 9, id = 0;
  for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) {
    const ci = xi + i, cj = yi + j;
    const wi = per ? ((ci % per) + per) % per : ci, wj = per ? ((cj % per) + per) % per : cj;
    const px = ci + .5 + (h2(wi, wj, seed) - .5) * jit, py = cj + .5 + (h2(wj, wi, seed + 7) - .5) * jit;
    const d = Math.hypot(x - px, y - py);
    if (d < d1) { d2 = d1; d1 = d; id = h2(wi, wj, seed + 13); } else if (d < d2) d2 = d;
  }
  return {d1, d2, id};
}
// periodic value: wrap u, v (0..1) for tiles
const per = (f, p) => (u, v) => f(((u % 1) + 1) % 1, ((v % 1) + 1) % 1);
// Grey shell plates: smooth pale plates with dark contour outlines and faint wood-grain swirls (value 0.55 .. 1).
export function shellGrey(u, v, {cell = 4, seed = 3} = {}) {
  const c = cells(u * cell, v * cell, seed, cell, .7), edge = c.d2 - c.d1;
  let g = .9 + .06 * (c.id - .5) + .05 * (N.a(u * 9, v * 9) - .5);
  const sw = Math.abs(Math.sin((c.d1 * 9 + 2 * N.b(u * 4, v * 4)) * Math.PI));   // contour swirls round each plate centre
  if (sw < .12 && c.d1 > .12) g -= .12 * (1 - sw / .12);
  if (edge < .06) g = .42 + 2 * edge;                                           // the dark outline
  else if (edge < .1) g -= .1 * (1 - (edge - .06) / .04);
  return grey(g);
}
// Grey plate rows: overlapping leaf plates in rows along v, bevel highlight at each plate's top edge, dark gaps (0.2 .. 1).
export function plateGrey(u, v, {rows = 4, cols = 3, seed = 5} = {}) {
  const r = v * rows, ri = Math.floor(r), fr = r - ri, off = (ri % 2) * .5;
  const cu = u * cols + off, ci = Math.floor(cu), fc = cu - ci;
  const id = h2(ci, ri, seed);
  // each plate: a rounded tongue pointing down (v grows down the sprite)
  const w = .5 - Math.abs(fc - .5), tip = fr > .55 ? (fr - .55) / .45 : 0;
  const inside = w > .06 + .38 * tip * tip;
  let g = .55 + .12 * (id - .5) + .08 * (N.c(u * 12, v * 12) - .5) - .18 * fr;
  if (fr < .14) g += .35 * (1 - fr / .14);                                       // bevel light on the upper rim
  if (!inside) g = .22 + .06 * N.d(u * 20, v * 20);                              // the gap between plates
  else if (w < .1 + .38 * tip * tip) g = Math.max(g, .78);                        // thin pale rim
  return grey(g);
}
// ---- shared tiles ------------------------------------------------------------------------------------------------------------
// name -> [w, h, ppb, painter (u, v in 0..1), forms, region]. Grey tiles are tinted per form by their slot.
const T = (w, h, ppb, fn, forms = 'both', region = 'shared') => ({w, h, ppb, fn, forms, region});
export const TILES = {
  g_shell: T(128, 128, 32, per((u, v) => shellGrey(u, v), 1)),
  g_plate: T(128, 128, 32, per((u, v) => plateGrey(u, v), 1)),
  p1_gold: T(32, 64, 48, (u, v) => PAL.p1_gold(clamp(.15 + .55 * v + .25 * Math.abs(u - .5) * 2 - .1 * N.b(u * 8, v * 8))), 'p1'),
  p1_cone: T(32, 32, 48, (u, v) => PAL.p1_cone(clamp(.2 + .5 * v + .2 * Math.abs(u - .5) * 2)), 'p1'),
  p1_leg: T(64, 128, 32, (u, v) => { const t = smooth(.3, .85, v); const a = PAL.p1_slate(.45 + .2 * N.a(u * 8, v * 8)), b = PAL.p1_bark(.3 + .25 * N.b(u * 6, v * 10)); let c = mix(a, b, t); const g = Math.abs(Math.sin((u * 3 + .4 * N.c(u * 3, v * 5)) * Math.PI)); if (g < .07) c = sink(c, .35); return c; }, 'p1', 'limbs'),
  p3_gold: T(32, 64, 48, (u, v) => PAL.p3_cone_gold(clamp(.15 + .55 * v + .25 * Math.abs(u - .5) * 2 - .1 * N.b(u * 8, v * 8))), 'p3'),
  p3_cone: T(32, 32, 48, (u, v) => PAL.p3_cone(clamp(.2 + .5 * v + .2 * Math.abs(u - .5) * 2)), 'p3'),
  p1_gem: T(32, 32, 48, (u, v) => { const f = Math.hypot(u - .35, v - .3); return PAL.p1_gem(clamp(.05 + 1.1 * f + .08 * N.a(u * 6, v * 6))); }, 'p1'),
  p1_core: T(32, 32, 48, (u, v) => { const f = Math.hypot(u - .45, v - .4); const vein = Math.abs(Math.sin((u * 5 + 2 * N.a(u * 3, v * 3)) * Math.PI)); return PAL.p1_core(clamp(.05 + .9 * f + (vein < .08 ? .35 : 0) + .06 * N.b(u * 8, v * 8))); }, 'p1', 'body'),
  p3_gem: T(32, 32, 48, (u, v) => { const f = Math.hypot(u - .35, v - .3); return PAL.p3_gem(clamp(.05 + 1.1 * f + .08 * N.a(u * 6, v * 6))); }, 'p3'),
  p3_emerald: T(32, 32, 48, (u, v) => { const f = Math.abs(u - .5) + Math.abs(v - .5); return PAL.p3_emerald(clamp(.1 + .9 * f + .1 * N.a(u * 6, v * 6))); }, 'p3'),
  p3_lime: T(64, 64, 32, per((u, v) => { const c = cells(u * 3, v * 2, 21, 3, .5); let col = PAL.p3_lime(.25 + .3 * c.id + .15 * (v - .5)); const vein = Math.abs(((u * 6 + .3 * Math.sin(v * 9)) % 1) - .5); if (vein < .04) col = mix(col, PAL.p3_line(.3), .55); if (c.d2 - c.d1 < .06) col = mix(col, PAL.p3_line(.5), .7); return col; }, 1), 'p3'),
  p3_robe: T(64, 128, 32, per((u, v) => { let col = PAL.p3_robe(.35 + .2 * N.a(u * 6, v * 6)); const cu = Math.abs(Math.sin((u * 3 + Math.sin(v * 12) * .2) * Math.PI)); if (cu < .06) col = mix(col, C('#C9C27A'), .75); else if (cu < .12) col = mix(col, C('#7F8345'), .6); const d = Math.abs(u - .5) * 1.4 + Math.abs(((v * 4) % 1) - .5); if (d < .14) col = mix(col, C('#F2F4EE'), .9); return col; }, 1), 'p3', 'body'),
};
for (const [n, t] of Object.entries(TILES)) registerTile(n, t.w, t.h, t.ppb);
registerWrap('p1_leg');
export const tileSprites = () => Object.fromEntries(Object.entries(TILES).map(([n, t]) => [n, {w: t.w, h: t.h, ppb: t.ppb, fn: t.fn, translucent: false, forms: t.forms, region: t.region, use: TINTED_SPRITES[n] ? 'tinted' : 'unique'}]));

// ---- sprite helpers ------------------------------------------------------------------------------------------------------
// A card sprite over a shape rect (blocks): px per block -> size rounded up to multiples of 16 (<= 512).
export const r16 = x => Math.min(512, Math.max(16, Math.ceil(x / 16) * 16));
export const spriteSize = (rect, ppb) => [r16((rect.u1 - rect.u0) * ppb), r16((rect.v1 - rect.v0) * ppb)];
// Painter in shape coordinates: fn(u, v) with u across (rect u0..u1) and v up (v0 bottom .. v1 top) -> rgba or null.
export const onRect = (rect, fn) => (s, t) => fn(rect.u0 + s * (rect.u1 - rect.u0), rect.v1 - t * (rect.v1 - rect.v0)) || TRANSPARENT;
// The same for a horizontal slab (plane 'y': u = X, v = Z; the card maps the sprite's top row to v0).
export const onRectY = (rect, fn) => (s, t) => fn(rect.u0 + s * (rect.u1 - rect.u0), rect.v0 + t * (rect.v1 - rect.v0)) || TRANSPARENT;
// A sprite record for the region modules' sprites(): {w, h, ppb, fn (s, t) -> rgba, translucent, forms, region, use}
export const sprite = (w, h, ppb, fn, forms, region, {translucent = false, use = null} = {}) => ({w, h, ppb, fn, translucent, forms, region, use: use || 'unique'});
// Bevel light of a signed-distance field at (u, v): rim 1 at the edge .. 0 deep inside; lit > 0 on the upper-left rim.
export function bevelLight(sd, u, v, w = .08, e = .01) {
  const d = sd(u, v);
  const gx = (sd(u + e, v) - sd(u - e, v)) / (2 * e), gy = (sd(u, v + e) - sd(u, v - e)) / (2 * e);
  return {d, rim: clamp(1 + d / w), lit: gx * -.6 + gy * .8};
}
// A generic painted leaf / plate card: base ramp, darker outline, a midrib along v, side veins, a bevel light.
export function leafPaint(sd, R, {line = PAL.p3_line, rib = true, veins = 6, ribX = 0, k = 1, outline = .035, base = .3} = {}) {
  return (u, v) => {
    const b = bevelLight(sd, u, v, .1);
    if (b.d > 0) return null;
    let c = R(clamp(base + .25 * (N.a(u * 5 * k, v * 5 * k) - .5) - .18 * b.lit * b.rim));
    if (rib && Math.abs(u - ribX) < .025 * k) c = mix(c, line(.35), .6);
    if (veins && rib) { const s = Math.abs(((v * veins + Math.abs(u - ribX) * 2.5) % 1) - .5); if (s < .04 && Math.abs(u - ribX) > .05) c = mix(c, line(.4), .4); }
    if (b.d > -outline * k) c = mix(c, line(.75), .85);
    return c;
  };
}
// ---- shape helpers (blocks, a part's authoring frame) -----------------------------------------------------------------------
import {loft, slab, sdPoly, stroke, sdUnion, sdSub, sdCircle} from './mboss_shape_lib.mjs';
// A cone / crystal spike from base point c along the authoring axis 'y' (up) with base radius r and height h (8 facets).
// Section centre [c1, c2] of a loft about `axis` for an A-frame point p (the shape lib's frames: 'z' e1 = left, e2 = up;
// 'y' e1 = left, e2 = forward (-Z); 'x' e1 = forward (-Z), e2 = up).
export const secC = (axis, p) => (axis === 'z' ? [p[0], p[1]] : axis === 'y' ? [p[0], -p[2]] : [-p[2], p[1]]);
// A cone / crystal spike from base point c along `axis` (sign +1: toward +axis) with base radius r and height h (8 facets).
export const cone = (c, r, h, tex, {seed = 0, axis = 'y', sign = 1} = {}) => {
  const ax = {x: 0, y: 1, z: 2}[axis], a0 = c[ax], cc = secC(axis, c);
  const st = [{a: a0, r, c: cc}, {a: a0 + sign * h * .55, r: r * .55, c: cc}, {a: a0 + sign * h, r: .02, c: cc}];
  return loft(axis, sign > 0 ? st : st.reverse(), {n: 8, tex, caps: sign > 0 ? '-' : '+', seed});
};
// A sphere-ish ball (loft along y) of radius r at c.
export const ball = (c, r, tex, {seed = 0, n = 8, sy = 1} = {}) => {
  const cc = secC('y', c), st = [-.97, -.7, -.3, .3, .7, .97].map(t => ({a: c[1] + t * r * sy, r: r * Math.sqrt(1 - t * t), c: cc}));
  return loft('y', st, {n, tex, caps: '-+', seed});
};
// Leaf outline (pointed ellipse along v from v0 to v1, half width w at its widest, centred on u0).
export const sdLeaf = (u0, v0, v1, w, {p = 1.2, tipW = 0} = {}) => (u, v) => {
  const t = clamp((v - v0) / (v1 - v0)), half = Math.max(tipW, w * Math.pow(Math.sin(Math.PI * t), p));
  const out = v < v0 ? v0 - v : v > v1 ? v - v1 : 0;
  return Math.max(Math.abs(u - u0) - half, out > 0 ? out : -1e9);
};
export {loft, slab, sdPoly, stroke, sdUnion, sdSub, sdCircle};
