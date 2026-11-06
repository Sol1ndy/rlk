// Shared materials of the 야타용왕 (Azhdaha) rig: the palette ramps (model.md §4) and the tile sprites that several
// regions use (rock hide, cream stone, plate umber, gold, dark horn, talon, bark), plus small painting helpers.
// Co-owned by the region modules: a change here repaints every region, so keep the names and the texel densities
// (ppb) stable. Region-specific sprites live in azhdaha_{head,body,legs,tail}.mjs.
import {C, clamp, smooth, mix, fbm, TRANSPARENT} from './mboss_paint_lib.mjs';
import {registerTile} from './azhdaha_shape.mjs';

export {C, clamp, smooth, mix, fbm, TRANSPARENT};
// ---- palette (model.md §4.1 base ramps hi -> deep; §4.2 element looks) ------------------------------------------------
export const ramp = list => { const cs = list.map(C); return t => { const x = clamp(t) * (cs.length - 1), i = Math.min(cs.length - 2, Math.floor(x)); return mix(cs[i], cs[i + 1], x - i); }; };
export const PAL = {
  hide: ramp(['#8C7B5E', '#77674D', '#655640', '#554733', '#433827', '#2E261A']),
  plate: ramp(['#8E6B55', '#6E4C3B', '#573A2C', '#452C22', '#34211A', '#221510']),
  plateOr: ramp(['#E39A48', '#C47A2E', '#A35E22', '#7E4219', '#5A2C12']),
  horn: ramp(['#5E4A3E', '#46362E', '#352823', '#2A201C', '#1F1815', '#141010']),
  gold: ramp(['#FFE7A0', '#F7C957', '#E6A93A', '#C98625', '#9E5E1A', '#6A3A12']),
  inlay: ramp(['#A65A24', '#8A4A1E', '#6B3719', '#4A2412']),
  crystal: ramp(['#FFD98A', '#F4A845', '#E07A2A', '#B9521C', '#7E3014']),
  cream: ramp(['#EFE8D4', '#DCD2BA', '#C3B89D', '#A69B80', '#857B63', '#625946']),
  groove: ramp(['#6E6352', '#4E463A', '#3A3329']),
  bracer: ramp(['#B08A68', '#946E50', '#77543C', '#5E402D', '#4A3022', '#24150F']),
  gaiter: ramp(['#C7BBA0', '#ADA086', '#918469', '#756A54', '#5A5142', '#3E382E']),
  talon: ramp(['#6E655A', '#554C43', '#3E3631', '#2D2723', '#1F1A18']),
  pad: ramp(['#9C8E78', '#7A6E5C']),
  mask: ramp(['#8A6650', '#6A4A3A', '#523629', '#3E281F', '#2E1D17', '#21140F']),
  gum: ramp(['#C9505E', '#A73A48', '#7A2733']), tongue: C('#B45A62'), teeth: ramp(['#F2EAD6', '#D8CDB4']),
  eye: ramp(['#FFE0E0', '#FF8A8E', '#F04352', '#C81A2C', '#8E0E1B', '#4E070E']),
  branch: ramp(['#5A4434', '#45342A', '#34271F', '#261C16']),
  leaf: ramp(['#FFD98A', '#F7B54A', '#E58F2E', '#C06A1E', '#8A4515']),
};
// Element looks: glow lines (core -> edge) and the base recolours (model.md §4.2).
export const LOOK_PAL = {
  hydro: {glow: ramp(['#F0F8FF', '#CDE6FF', '#9CC4F2', '#6E96D8', '#4A66B4']), stone: ramp(['#566982', '#3F5472', '#302F4B', '#202036']), tint: 0xCDE6FF},
  pyro: {glow: ramp(['#FFF0D0', '#FFC98A', '#F9A761', '#E5703A', '#B8401E']), stone: ramp(['#C03124', '#96271D', '#6E1C15', '#46120D']), tint: 0xFFB070},
  cryo: {glow: ramp(['#F2FFFF', '#CFF6FF', '#9EE3F5', '#6CC4E2', '#3F95BE']), stone: ramp(['#4E5A70', '#3E4A60', '#2B3A50', '#1E2A3E']),
    bloom: ramp(['#F4FFFF', '#C9F9FC', '#95DCEC', '#6CBFD9', '#4E9BBB'])},
  electro: {glow: ramp(['#F6E2FF', '#DDB0F6', '#B97CEB', '#8F55D6', '#6438B0']), stone: ramp(['#5A4060', '#463050', '#34243E', '#24182C']),
    bloom: ramp(['#C7B4F2', '#9C7FD6', '#7657B8', '#5A40A0', '#3D2A6C']), spark: C('#E4A6F0')},
};
export const lift = (c, k) => mix(c, [255, 248, 232, 255], clamp(k));
export const sink = (c, k) => mix(c, [24, 16, 10, 255], clamp(k));
export const scale = (c, k) => [c[0] * k, c[1] * k, c[2] * k, c[3] ?? 255];
export const N = {a: fbm(101), b: fbm(211), c: fbm(307), d: fbm(401), e: fbm(503), f: fbm(613)};

// ---- cell noise (pebble scales) ----------------------------------------------------------------------------------------
// Jittered grid cells, periodic over `per` cells: returns {d1, d2, id} for the two nearest seeds (cell units).
const h2 = (i, j, s) => { let n = (i * 374761393 + j * 668265263 + s * 2246822519) | 0; n = (n ^ (n >>> 13)) * 1274126177 | 0; return ((n ^ (n >>> 16)) >>> 0) / 4294967295; };
export function cells(x, y, seed = 1, per = 0, jit = .8) {
  const xi = Math.floor(x), yi = Math.floor(y);
  let d1 = 9, d2 = 9, id = 0;
  for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) {
    let ci = xi + i, cj = yi + j;
    const wi = per ? ((ci % per) + per) % per : ci, wj = per ? ((cj % per) + per) % per : cj;
    const px = ci + .5 + (h2(wi, wj, seed) - .5) * jit, py = cj + .5 + (h2(wj, wi, seed + 7) - .5) * jit;
    const d = Math.hypot(x - px, y - py);
    if (d < d1) { d2 = d1; d1 = d; id = h2(wi, wj, seed + 13); } else if (d < d2) d2 = d;
  }
  return {d1, d2, id};
}
// Rock hide: rounded pebble scales with dark crevices, lit from the upper left (u, v in px of a W-wide tile).
export function hidePx(u, v, {ramp: R = PAL.hide, cell = 9, seed = 3, per = 0, warm = 0} = {}) {
  const c = cells(u / cell, v / cell, seed, per);
  const edge = c.d2 - c.d1;                                   // 0 at the crevice
  const bump = clamp(1 - c.d1 * 1.25);
  // smooth stone areas alternate with pebbled ones (model.md §3.4: pebbles larger on the shoulders and haunches)
  const sm = smooth(.38, .62, N.e(u * .025 + seed, v * .025));
  let t = .27 + .16 * (c.id - .5) * (1 - .6 * sm) + .1 * (N.a(u * .05, v * .05) - .5) - .14 * bump * (1 - sm);
  let col = R(t);
  if (edge < .09) col = sink(col, .5 * (1 - .75 * sm) * (1 - edge / .09));
  else if (edge < .2) col = sink(col, .1 * (1 - sm) * (1 - (edge - .09) / .11));
  col = mix(col, R(.08), .22 * smooth(.55, .9, N.c(u * .08, v * .08)));    // pale dust patches
  if (warm) col = mix(col, C('#7E6A4C'), warm * N.d(u * .05, v * .05));
  return col;
}
// Torso skin (body region; R3b: shared with the legs' masses): smooth warm grey-brown skin with big soft light / dark
// masses, a fine grain, faint wrinkles, optional low warts (u, v in px at 32 ppb).
// R3b (r3_critique 3.4): one ramp step darker and a touch greener (it read khaki next to the plastron at distance)
export const SKIN = ramp(['#8A7F64', '#736A50', '#605842', '#4E4736', '#3C372A', '#29251C']);
export function skinPx(u, v, {seed = 3, base = .36, warts = 0} = {}) {
  const m1 = N.e(u * .012 + seed, v * .012), m2 = N.a(u * .035 + seed * 3, v * .035), m3 = N.c(u * .25 + seed, v * .25);
  let t = base + .22 * (m1 - .5) + .1 * (m2 - .5) + .035 * (m3 - .5);
  // wrinkles: thin wavy lines, slightly darker with a lit lip above
  const w = Math.abs(N.f(u * .022 + seed, v * .06) - .5);
  if (w < .012) t += .07 * (1 - w / .012); else if (w < .022) t -= .025 * (1 - (w - .012) / .01);
  let col = SKIN(clamp(t, .03, .97));
  if (warts > 0) {
    const c = cells(u / 11, v / 11, seed + 9, 0, .8), cl = cells((u - 1.5) / 11, (v - 1.5) / 11, seed + 9, 0, .8);
    if (c.id < warts && c.d1 < .3) col = SKIN(clamp(t - .9 * (cl.d1 - c.d1) + .06 * c.d1 / .3, .03, .97));
  }
  return mix(col, SKIN(.15), .12 * smooth(.6, .9, N.b(u * .05 + seed, v * .05)));     // pale dust
}
// Cream stone: smooth with faint cracks and grain.
export function creamPx(u, v, R = PAL.cream, k = 1) {
  let col = R(.2 + .14 * N.b(u * .05, v * .05) + .06 * (N.e(u * .3, v * .3) - .5));
  const cr = Math.abs(N.d(u * .045 + 3, v * .03) - .5);
  if (cr < .012 * k) col = mix(col, PAL.groove(.4), .5);
  return col;
}
// Dark plate stone: long grain along v with soft streaks.
export function platePx(u, v, R = PAL.plate) {
  const g = N.a(u * .25, v * .02), s = N.b(u * .08, v * .08);
  return R(.48 + .25 * (g - .5) + .15 * (s - .5));
}
// Gold: polished, a broad gradient with fine speckle (t 0 bright .. 1 deep).
export const goldPx = (t, u, v) => PAL.gold(clamp(t + .05 * (N.c(u * .4, v * .4) - .5)));

// ---- shared tiles --------------------------------------------------------------------------------------------------------
// name -> [w, h, ppb, painter (u, v in 0..1)]. Registered for the loft / rockBox uv maps.
const T = (w, h, ppb, fn) => [w, h, ppb, fn];
export const TILES = {
  hide: T(128, 128, 32, (u, v) => hidePx(u * 128, v * 128, {per: 14, cell: 128 / 14})),
  hide_lg: T(128, 128, 24, (u, v) => hidePx(u * 128, v * 128, {per: 9, cell: 128 / 9, seed: 5, warm: .25})),
  hide_dk: T(64, 64, 32, (u, v) => sink(hidePx(u * 64, v * 64, {per: 7, cell: 64 / 7, seed: 9}), .3)),
  cream: T(128, 128, 32, (u, v) => creamPx(u * 128, v * 128)),
  plate: T(64, 64, 32, (u, v) => platePx(u * 64, v * 64)),
  plate_cryo: T(64, 64, 32, (u, v) => platePx(u * 64, v * 64, LOOK_PAL.cryo.stone)),
  plate_electro: T(64, 64, 32, (u, v) => platePx(u * 64, v * 64, LOOK_PAL.electro.stone)),
  gold: T(64, 64, 48, (u, v) => goldPx(.25 + .3 * v, u * 64, v * 64)),
  gold_dk: T(32, 32, 48, (u, v) => goldPx(.62 + .2 * v, u * 32, v * 32)),
  horn: T(32, 64, 48, (u, v) => PAL.horn(.45 + .3 * (N.a(u * 6, v * 20) - .5) + .2 * v)),
  talon: T(32, 32, 48, (u, v) => PAL.talon(.45 + .3 * v + .2 * (N.b(u * 8, v * 8) - .5))),
  bark: T(64, 64, 48, (u, v) => { const g = N.c(u * 14, v * 3); let c = PAL.branch(.35 + .4 * (g - .5)); if (Math.abs(g - .5) < .03) c = sink(c, .4); return c; }),
  bark_cryo: T(64, 64, 48, (u, v) => { const g = N.c(u * 14, v * 3); let c = LOOK_PAL.cryo.stone(.4 + .4 * (g - .5)); if (Math.abs(g - .5) < .03) c = mix(c, LOOK_PAL.cryo.glow(.2), .7); return c; }),
  bark_electro: T(64, 64, 48, (u, v) => { const g = N.c(u * 14, v * 3); let c = LOOK_PAL.electro.stone(.4 + .4 * (g - .5)); if (Math.abs(g - .5) < .03) c = mix(c, LOOK_PAL.electro.glow(.2), .7); return c; }),
  mouth: T(32, 32, 48, (u, v) => PAL.gum(.4 + .4 * v)),
  dark: T(16, 16, 32, () => C('#1A120D')),
};
for (const [n, [w, h, ppb]] of Object.entries(TILES)) registerTile(n, w, h, ppb);
export const tileSprites = () => Object.fromEntries(Object.entries(TILES).map(([n, [w, h, , fn]]) => [n, [w, h, fn, false]]));

// ---- sprite helpers ------------------------------------------------------------------------------------------------------
// A card sprite over a shape rect (blocks): px per block -> size rounded up to multiples of 16 (<= 512).
export const r16 = x => Math.min(512, Math.max(16, Math.ceil(x / 16) * 16));
export const spriteSize = (rect, ppb) => [r16((rect.u1 - rect.u0) * ppb), r16((rect.v1 - rect.v0) * ppb)];
// Painter in shape coordinates: fn(u, v) with u across (rect u0..u1) and v up (v0 bottom .. v1 top) -> rgba or null.
export const onRect = (rect, fn) => (s, t) => fn(rect.u0 + s * (rect.u1 - rect.u0), rect.v1 - t * (rect.v1 - rect.v0)) || TRANSPARENT;
// Bevel light from a signed-distance field: k in 0..1 rising from the edge to depth w inside; light from the upper
// left of the shape plane (gradient of sd).
export function bevelLight(sd, u, v, w = .08, e = .01) {
  const d = sd(u, v);
  const gx = (sd(u + e, v) - sd(u - e, v)) / (2 * e), gy = (sd(u, v + e) - sd(u, v - e)) / (2 * e);
  const rim = clamp(1 + d / w);              // 1 at the edge, 0 deep inside
  const lit = gx * -.6 + gy * .8;            // > 0 on the rim that faces the upper left (-u, +v)
  return {d, rim, lit};
}
