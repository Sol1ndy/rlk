// Materials of the 타키 (Tachy) rig (S:tk/PLAN.md §1.3, §2.2): the palette read from the footage (ref/model_a.jpg,
// v2 6.0-16.4, v8 6.2, v9 1.5), the tile sprites the lofted / boxed parts sample at a fixed texel density (registerTile:
// a face of w x h b shows a (w ppb) x (h ppb) px window), and small painting helpers shared by tachy_paint.mjs.
//
// Looks of the footage, as painted here: a black carbon-weave bodysuit (twill), gunmetal plate armour with bevelled
// panel lines, hazard-yellow paint bands (#F2C230) and gold trim, silver hexagon plates (left side, back, collar,
// shoulders, hips), orange ring lights (#FF8A1E), a copper-red glossy helmet dome with a gold rim, dark ash-brown hair.
import {C, clamp, smooth, mix, fbm, TRANSPARENT} from './mboss_paint_lib.mjs';
import {registerTile} from './mboss_shape_lib.mjs';

export {C, clamp, smooth, mix, fbm, TRANSPARENT};
export const ramp = list => { const cs = list.map(C); return t => { const x = clamp(t) * (cs.length - 1), i = Math.min(cs.length - 2, Math.floor(x)); return mix(cs[i], cs[i + 1], x - i); }; };
// ---- palette (light -> deep) -------------------------------------------------------------------------------------------
export const PAL = {
  suit: ramp(['#3E3E46', '#2A2A31', '#1E1E24', '#151519', '#0D0D10']),
  metal: ramp(['#8C919C', '#5C616B', '#40444C', '#2C2F36', '#1B1D22', '#0F1013']),
  yellow: ramp(['#FFE27A', '#F2C230', '#D9A622', '#A8801C', '#6E5410']),
  gold: ramp(['#FFE9A6', '#E8C25A', '#C99A3A', '#8A6420', '#4A3410']),
  hex: ramp(['#E4E6EA', '#B8BCC4', '#8E939C', '#666A73', '#3E414A']),
  copper: ramp(['#E89A6A', '#B85A34', '#8A3A22', '#5A2418', '#2E120C']),
  hair: ramp(['#9C8A82', '#6E5A50', '#4E3E38', '#3B2E2A', '#241B19']),
  skin: ramp(['#F6E6DE', '#E9D3C8', '#D4B2A4', '#B08878', '#7A5448']),
  flesh: ramp(['#C24A4E', '#9A2A30', '#5E1018', '#3E0A10', '#1E0408']),
  bronze: ramp(['#F2D488', '#D8B45A', '#A8823A', '#6E5224', '#3A2A12']),
  wingm: ramp(['#6A6A78', '#4A4A55', '#2A2A32', '#16161B', '#0B0B0E']),
  ring: ramp(['#FFF4C8', '#FFD27A', '#FF8A1E', '#C2560C', '#4A1E06']),
};
export const N = {a: fbm(4101), b: fbm(4211), c: fbm(4307), d: fbm(4409), e: fbm(4513), f: fbm(4621)};
export const lift = (c, k) => mix(c, [255, 250, 240, 255], clamp(k));
export const sink = (c, k) => mix(c, [6, 6, 8, 255], clamp(k));
const fr = x => x - Math.floor(x);
const h2 = (i, j, s) => { let n = (i * 374761393 + j * 668265263 + s * 2246822519) | 0; n = (n ^ (n >>> 13)) * 1274126177 | 0; return ((n ^ (n >>> 16)) >>> 0) / 4294967295; };

// ---- material functions (u, v in 0..1 over a tile; v grows down) ----------------------------------------------------------
// carbon twill: 2/2 weave, each tow a soft cylinder with a sheen that flips between warp and weft
export function carbon(u, v, n = 8, k = 1) {
  const x = u * n, y = v * n, i = Math.floor(x), j = Math.floor(y), fx = x - i, fy = y - j;
  const warp = ((i + j) % 4 + 4) % 4 < 2;
  const t = warp ? fx : fy, s = Math.sin(Math.PI * t);
  let c = PAL.suit(.62 - .38 * s * k);
  const sheen = Math.pow(s, 6) * (warp ? .55 : .3);
  c = lift(c, sheen * .22 * k);
  c = mix(c, PAL.suit(.9), .25 * (N.a(u * 6, v * 6) - .5));
  if ((warp ? fy : fx) < .06) c = sink(c, .35);
  return c;
}
// gunmetal panel: rows of rectangular panels with a bevel light on the upper-left, a dark seam, fine scratches
export function metalPanel(u, v, {cols = 2, rows = 2, base = .45, seed = 3, yTrim = 0} = {}) {
  const x = u * cols, y = v * rows, i = Math.floor(x), j = Math.floor(y), fx = x - i, fy = y - j;
  const id = h2(i, j, seed), e = Math.min(fx, 1 - fx, fy, 1 - fy);
  let t = base + .1 * (id - .5) + .12 * (N.b(u * 7, v * 7) - .5) + .08 * fy;
  if (e < .09) { const lit = (fx < .09 || fy < .09) ? -.32 : .16; t += lit * (1 - e / .09); }
  if (e < .025) t = .92;
  let c = PAL.metal(clamp(t));
  const sc = Math.abs(fr(u * 23 + v * 9 + 3 * N.c(u * 3, v * 3)) - .5);
  if (sc < .015) c = lift(c, .12);
  if (yTrim && fy > 1 - yTrim) c = PAL.yellow(.25 + .5 * (fy - (1 - yTrim)) / yTrim);
  return c;
}
// hexagon plates: silver cells with dark seams and a bevel per cell (pointy-top grid, `scale` cells across the tile)
export function hexCells(u, v, {scale = 4, dark = false, seed = 7} = {}) {
  const x = u * scale, y = v * scale * 1.1547;
  const r = Math.floor(y), off = (r % 2) * .5, q = Math.floor(x - off);
  // nearest of the candidate centres
  let best = 9, bi = 0, bj = 0, bx = 0, by = 0;
  for (let dj = -1; dj <= 1; dj++) for (let di = -1; di <= 1; di++) {
    const jj = r + dj, ii = q + di, cx = ii + .5 + (((jj % 2) + 2) % 2) * .5, cy = jj + .5;
    const d = Math.hypot((x - cx), (y - cy) * .866);
    if (d < best) { best = d; bi = ii; bj = jj; bx = x - cx; by = (y - cy) * .866; }
  }
  // hex distance (pointy top) of the offset
  const ax = Math.abs(bx), ay = Math.abs(by), hd = Math.max(ax * .866 + ay * .5, ay) / .5;
  const id = h2(bi, bj, seed);
  const R = dark ? PAL.metal : PAL.hex;
  let t = (dark ? .42 : .3) + .18 * (id - .5) + .1 * (N.d(u * 5, v * 5) - .5);
  t += .22 * (by + bx * .3);                                                      // a curved face: lighter at the top-left
  let c = R(clamp(t));
  if (hd > .78) c = PAL.metal(.85);                                              // seam
  else if (hd > .68) c = lift(c, .25 * (1 - (hd - .68) / .1));                   // bevel rim
  return c;
}
export function yellowPaint(u, v) {
  let c = PAL.yellow(.3 + .25 * (N.e(u * 6, v * 6) - .5) + .2 * v);
  const wear = N.f(u * 14, v * 14);
  if (wear > .72) c = mix(c, PAL.metal(.5), .7);
  if (v < .08 || v > .92) c = sink(c, .35);
  return c;
}
export function goldMetal(u, v) {
  const c = PAL.gold(clamp(.25 + .5 * Math.abs(v - .35) + .15 * (N.a(u * 8, v * 8) - .5)));
  return v < .12 ? lift(c, .3) : c;
}
export function visorGlass(u, v) {
  // dark tinted copper glass, a faint warm reflection band
  const c = mix(C('#170806'), C('#3E1A10'), clamp(.3 + .5 * v + .2 * (N.b(u * 3, v * 3) - .5)));
  return lift(c, .18 * Math.exp(-Math.pow((u - v * .4 - .3) / .08, 2)));
}
export function copperGloss(u, v) {
  // glossy copper-red lacquer: smooth, a soft warm sheen, fine dark hairline seams
  let c = PAL.copper(clamp(.42 + .12 * (N.a(u * 2, v * 2) - .5) + .1 * v));
  c = lift(c, .12 * Math.exp(-Math.pow((v - .3) / .15, 2)));
  if (Math.abs(fr(v * 2) - .5) < .012) c = sink(c, .35);
  return c;
}
export function hairStrands(u, v, {k = 1} = {}) {
  const s = N.a(u * 26, v * 2.2) * .7 + N.b(u * 60, v * 3) * .3;
  let c = PAL.hair(clamp(.45 + .6 * (s - .5) + .15 * v));
  const shine = Math.exp(-Math.pow((v - .25) / .12, 2)) * .5 * k;
  return lift(c, shine * s * .5);
}
export function fleshTex(u, v) {
  const n = N.c(u * 5, v * 9), vein = Math.abs(fr(u * 3 + .4 * Math.sin(v * 11)) - .5);
  let c = PAL.flesh(clamp(.35 + .5 * (n - .5) + .2 * Math.abs(u - .5)));
  if (vein < .05) c = PAL.flesh(.85);
  if (n > .7) c = lift(c, .12);
  return c;
}
export function steelTex(u, v) {
  return PAL.metal(clamp(.55 + .2 * (N.d(u * 3, v * 30) - .5) + .15 * Math.abs(u - .5)));
}

// ---- tiles (registered for loft / rockBox windows): name -> [w, h, ppb, painter] ----------------------------------------
const per = f => (u, v) => f(fr(u), fr(v));
export const TILES = {
  tk_suit: [64, 64, 96, per((u, v) => carbon(u, v, 8))],
  tk_metal: [64, 64, 64, per((u, v) => metalPanel(u, v, {cols: 2, rows: 2}))],
  tk_metal_dk: [64, 64, 64, per((u, v) => metalPanel(u, v, {cols: 2, rows: 3, base: .62, seed: 9}))],
  tk_metal_y: [64, 64, 64, per((u, v) => metalPanel(u, v, {cols: 1, rows: 1, base: .5, seed: 11, yTrim: .2}))],
  tk_hex: [64, 64, 80, per((u, v) => hexCells(u, v, {scale: 3}))],
  tk_hex_dk: [64, 64, 80, per((u, v) => hexCells(u, v, {scale: 3, dark: true, seed: 13}))],
  tk_yellow: [32, 32, 64, per(yellowPaint)],
  tk_gold: [32, 32, 64, per(goldMetal)],
  tk_copper: [64, 64, 48, per(copperGloss)],
  tk_visor: [32, 32, 48, per(visorGlass)],
  tk_hair: [64, 64, 64, per((u, v) => hairStrands(u, v))],
  tk_flesh: [64, 64, 48, per(fleshTex)],
  tk_steel: [32, 64, 64, per(steelTex)],
  tk_black: [16, 16, 32, (u, v) => PAL.suit(.85 + .1 * N.a(u * 4, v * 4))],
  tk_skin: [16, 16, 64, (u, v) => PAL.skin(.3 + .1 * N.b(u * 4, v * 4))],
};
for (const [n, [w, h, ppb]] of Object.entries(TILES)) registerTile(n, w, h, ppb);

// ---- sprite helpers -------------------------------------------------------------------------------------------------------
// A glow pixel: colour c with alpha a (0..1).
export const glow = (c, a) => { const x = C(c); return [x[0], x[1], x[2], Math.round(clamp(a) * 255)]; };
export const r16 = x => Math.min(512, Math.max(16, Math.ceil(x / 16) * 16));
