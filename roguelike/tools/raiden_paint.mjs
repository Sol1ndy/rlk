// Painted sprites of the Raiden rig (마가츠 미타케 나루카미노 미코토): the Shogun extras (sleeves, drape, braid, obi knot,
// flower, halo arch, katana, polearm, guard aura), the Tenma form (lacquer puppet arms, eye sigils, tan gauntlets,
// glaive, disc halo, horns, dagger, tassets, the dark Tenma skin) and the props (eye orb, vajra crystal, lotus,
// dome glass, clap facets, switch hoop and vortex). Scratchpad rd/plan.md §C.1, §C.2, §C.6 (rig sprites <= 0.45 M px,
// props <= 0.25 M px); palette from rd/footage/{A,B}_catalog.md "Model".
//
// Files: assets/rlk/textures/raiden/rig/<name>.png, sprite ids rlk:raiden/rig/<name> (single sources in the items
// atlas, merged; the generator owns the directory). Painters take (u, v) in 0..1 (u right, v down) and return rgba.
// Opaque sprites are alpha-cut at 0.5 (paint), glow sprites keep their alpha (paintT).
// skin_tenma is derived from the supplied 64x64 skin (textures/raiden/skin.png, never edited): the kimono and arms turn
// into the black bodysuit with violet glow lines, face and hair stay.
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import {paintSpriteSet, C, mix, clamp, smooth, fbm, TRANSPARENT} from './mboss_paint_lib.mjs';
import {DOME} from './raiden_geometry.mjs';

export const SPRITE_DIR = 'assets/rlk/textures/raiden/rig';
export const spriteId = n => 'rlk:raiden/rig/' + n;
const T = TRANSPARENT;
const A = (c, a) => [c[0], c[1], c[2], Math.round(255 * clamp(a))];
const n1 = fbm(11), n2 = fbm(23), n3 = fbm(37);
const PAL = {
  ink: '#120e1c', dark: '#1d1b2b', hair: '#2e2a4f', hairHi: '#4b4580', violet: '#5b3a8f', deep: '#3a1f6b',
  electro: '#9b5cff', lilacRim: '#c9a6ff', flash: '#f6e0ff', charge: '#d8e8ff', pale: '#d8cfe6', paleShade: '#9b8cc0',
  plum: '#5a2a40', plumDk: '#3a1a2a', gold: '#c9a35a', goldDk: '#8a6a30', red: '#c0392b', orange: '#e0703a',
  lacquer: '#d8b4e2', lacquerSh: '#9a6fb0', lacquerDk: '#6e4a86', tan: '#c9a27a', tanDk: '#8a6a4a', tanBand: '#6e5038',
  magenta: '#ff4fd8', pink: '#ff9ad8', shaft: '#2b1d4a', suit: '#15121f',
};
const P = Object.fromEntries(Object.entries(PAL).map(([k, v]) => [k, C(v)]));

// ---- flat swatches (16 x 16, faint value noise so large faces do not read as plastic) ------------------------------
const swatch = (c, k = .06) => (u, v) => { const n = n1(u * 5.3, v * 5.3) - .5; return [...c.slice(0, 3).map(x => clamp(x * (1 + n * k * 2), 0, 255)), 255]; };
const SWATCHES = {
  sw_ink: P.ink, sw_violet: P.violet, sw_deep: P.deep, sw_plum: P.plum, sw_pale: P.pale,
  sw_paleshade: P.paleShade, sw_gold: P.gold, sw_golddk: P.goldDk, sw_lacquersh: P.lacquerSh,
  sw_lacquerdk: P.lacquerDk, sw_tan: P.tan, sw_tandk: P.tanBand, sw_shaft: P.shaft, sw_suit: P.suit, sw_glow: P.lilacRim,
  sw_white: P.flash, sw_electro: P.electro,
};

// ---- Shogun -----------------------------------------------------------------------------------------------------------
// Kimono sleeve, painted on a card that hangs from the shoulder (v 0) to the hem (v 1): flaring, rounded hem, a violet
// hem band and faint lozenge weave. dark: the longer right sleeve (deep violet with a pale trim).
const sleeve = dark => (u, v) => {
  const half = .3 + .2 * smooth(0, 1, v);                 // flares from 0.6 to 1.0 of the width
  const x = Math.abs(u - .5);
  const hem = 1 - .07 * (1 - (x / half) ** 2);            // rounded hem
  if (x > half || v > hem) return T;
  const edge = Math.min(half - x, hem - v);
  const fold = .5 + .5 * Math.sin((u - .5) * 26 + 2 * n1(u * 3, v * 2));
  const base = dark ? mix(P.deep, P.violet, .25 + .3 * fold) : mix(P.paleShade, P.pale, .45 + .5 * fold);
  let c = base;
  const weave = (Math.abs(((u * 9 + v * 9) % 1) - .5) < .04 || Math.abs(((u * 9 - v * 9 + 9) % 1) - .5) < .04) ? 1 : 0;
  if (weave && !dark) c = mix(c, P.paleShade, .25);
  if (hem - v < .09) c = dark ? mix(P.pale, P.lilacRim, .3) : mix(P.violet, P.deep, .3);
  if (edge < .018) c = dark ? P.ink : mix(P.paleShade, P.deep, .4);
  return [...c.slice(0, 3), 255];
};
// Translucent train (60-70 % opacity) from the waist (v 0) to the ankles: folds, darker edges, pale lilac hem line.
const drape = (u, v) => {
  const half = .28 + .22 * v, x = Math.abs(u - .5);
  if (x > half) return T;
  const folds = .5 + .5 * Math.sin(u * 30 + 3 * n2(u * 2, v * 3));
  let c = mix(C('#2c2248'), C('#5a4888'), .35 + .45 * folds);
  let a = .62 + .12 * folds;
  const side = (half - x) / half;
  if (side < .08) { c = mix(c, P.ink, .5); a = .78; }
  if (v > .93) { c = mix(c, P.lilacRim, .55); a = .8; }
  if (v < .05) { c = P.deep; a = .9; }
  return A(c, a);
};
// Long single braid, hanging from v 0 (nape) to the tied tip: overlapping lobes, indigo with violet highlights.
const braid = (u, v) => {
  const w = .34 - .16 * v + .05 * Math.cos(v * 22) * (v < .9 ? 1 : 0), x = u - .5;
  if (v > .985 || Math.abs(x) > w) return T;
  const lobe = (v * 11) % 1, side = Math.floor(v * 11) % 2 ? 1 : -1;
  const shade = .5 + .5 * Math.sin(lobe * Math.PI) * (1 - Math.abs(x / w - side * .35));
  let c = mix(P.ink, P.hairHi, .15 + .55 * shade);
  if (v > .86 && v < .9) c = mix(P.electro, P.lilacRim, .4);                  // violet tie
  if (v >= .9) c = mix(P.hair, P.hairHi, .3 * (1 - (v - .9) * 10));          // tassel tip
  return [...c.slice(0, 3), 255];
};
// Pale violet flower ornament (five petals, gold centre).
const flower = (u, v) => {
  const x = u - .5, y = v - .5, r = Math.hypot(x, y), a = Math.atan2(y, x);
  const R = .3 + .17 * Math.abs(Math.cos(2.5 * a));
  if (r > R) return T;
  if (r < .1) return [...P.gold.slice(0, 3), 255];
  const c = mix(P.lilacRim, P.flash, clamp(1 - r / R) * .8);
  return [...mix(c, P.violet, r > R - .05 ? .5 : 0).slice(0, 3), 255];
};
// Obi knot rosette: plum loops, gold cord, violet centre.
const obiKnot = (u, v) => {
  const x = u - .5, y = v - .5, r = Math.hypot(x, y), a = Math.atan2(y, x);
  const loops = .32 + .14 * Math.cos(2 * a);
  if (r > loops) return T;
  if (r < .1) return [...P.electro.slice(0, 3), 255];
  if (Math.abs(r - .18) < .03) return [...P.gold.slice(0, 3), 255];
  return [...mix(P.plumDk, P.plum, .5 + .5 * Math.cos(a * 4)).slice(0, 3), 255];
};
// Short red-orange tassel with a gold cap.
const tassel = (u, v) => {
  const w = v < .2 ? .2 : .28 - .08 * (v - .2);
  if (Math.abs(u - .5) > w || v > .97) return T;
  if (v < .2) return [...P.gold.slice(0, 3), 255];
  const strand = .5 + .5 * Math.sin(u * 40);
  return [...mix(P.red, P.orange, .3 * strand).slice(0, 3), 255];
};
// Halo eye emblem: a winged diamond lens, violet with a white rim and a dark core with a tomoe swirl (glow card).
const haloEye = (u, v) => {
  const x = (u - .5) * 2, y = (v - .5) * 2;
  const wing = Math.abs(y) < .16 * (1 - Math.abs(x)) && Math.abs(x) < 1;      // thin horizontal wings
  const d = Math.abs(x) / .62 + Math.abs(y) / .9;                              // diamond
  if (d > 1 && !wing) return T;
  if (d > 1) return A(mix(P.lilacRim, P.flash, .5), .9 * (1 - Math.abs(x)));
  if (d > .86) return A(P.flash, 1);
  const r = Math.hypot(x / .62, y / .9), ang = Math.atan2(y, x);
  const swirl = Math.sin(ang * 3 + r * 9) > .45 && r > .2 && r < .7;
  const c = r < .2 ? P.ink : swirl ? mix(P.lilacRim, P.flash, .3) : mix(P.deep, P.electro, .2 + .6 * (1 - r));
  return A(c, 1);
};
// Tomoe orb (glow): violet glowing ball with a darker core comma.
const tomoeOrb = (u, v) => {
  const x = (u - .5) * 2, y = (v - .5) * 2, r = Math.hypot(x, y);
  if (r > 1) return T;
  const ang = Math.atan2(y, x);
  const comma = Math.abs(r - .45 - .15 * Math.sin(ang)) < .14 && Math.cos(ang - 1) > -.3;
  let c = mix(C('#8f5cff'), P.flash, clamp(1 - r * 1.2) * .5);
  if (comma) c = mix(P.ink, P.deep, .4);
  return A(c, r > .82 ? 1.6 * (1 - r) / .18 * .6 + .2 : 1);
};
// Thin lightning thread (glow): a jagged bright line along v with a soft violet halo.
const thread = (u, v) => {
  const cx = .5 + .18 * Math.sin(v * 23) + .1 * Math.sin(v * 61 + 1);
  const d = Math.abs(u - cx);
  if (d > .45) return T;
  const core = clamp(1 - d / .07), glow = clamp(1 - d / .45) ** 2;
  return A(mix(P.electro, P.flash, core), core + .55 * glow);
};
// Katana blade (alpha cut, curved toward the spine): pale violet-white glowing steel, darker spine line and crackle.
const katanaBlade = (u, v) => {
  const t = 1 - v;                                                            // 0 at the habaki, 1 at the tip
  const c0 = .5 + .12 * t * t;                                               // curve toward +u (spine side)
  const hw = (.36 - .1 * t) * (t > .9 ? Math.sqrt(clamp((1 - t) / .1)) : 1);
  const x = u - c0;
  if (Math.abs(x) > hw) return T;
  const s = (x + hw) / (2 * hw);                                             // 0 edge .. 1 spine
  let c = mix(P.flash, P.lilacRim, s * .8);
  if (s > .78) c = mix(P.violet, P.deep, .3);
  const crack = Math.abs(((v * 7 + n3(u * 4, v * 12) * .8) % 1) - .5) < .03 && s < .5;
  if (crack) c = P.charge;
  return [...c.slice(0, 3), 255];
};
// Polearm blade (alpha cut): a curved glaive head, glowing violet with a pale edge.
const polearmBlade = (u, v) => {
  const t = 1 - v, cx = .35 + .3 * t * t;
  const hw = (.22 + .1 * Math.sin(t * Math.PI)) * (t > .85 ? clamp((1 - t) / .15) ** .6 : 1);
  const x = u - cx;
  if (Math.abs(x) > hw) return T;
  const s = (x + hw) / (2 * hw);
  let c = mix(P.electro, C('#b98cff'), s);
  if (s < .18) c = mix(P.flash, P.lilacRim, .3);
  if (s > .85) c = P.deep;
  return [...c.slice(0, 3), 255];
};
// Weapon lightning (glow card along the blade): a jagged bolt with forks and a wide soft halo.
const weaponGlow = (u, v) => {
  const cx = .5 + .14 * Math.sin(v * 31) + .06 * Math.sin(v * 83 + 2);
  const d = Math.abs(u - cx), fork = Math.abs(u - (cx + .25 * Math.sin(v * 9))) < .03 && Math.sin(v * 13) > .6;
  const core = clamp(1 - d / .06), glow = clamp(1 - d / .5) ** 2;
  const fade = smooth(0, .08, v) * smooth(1, .9, v);
  return A(mix(P.electro, P.flash, core), (core + .45 * glow + (fork ? .8 : 0)) * fade);
};
// Guard stance aura: a crackling ring on the floor (glow, top view).
const auraRing = (u, v) => {
  const x = (u - .5) * 2, y = (v - .5) * 2, r = Math.hypot(x, y), a = Math.atan2(y, x);
  const jag = .86 + .04 * Math.sin(a * 23) + .03 * Math.sin(a * 57 + 1);
  const d = Math.abs(r - jag);
  if (d > .14) return T;
  return A(mix(P.electro, P.flash, clamp(1 - d / .03)), clamp(1 - d / .14) ** 1.5);
};

// ---- Tenma ------------------------------------------------------------------------------------------------------------
// Lacquer tile (puppet arms): pale lilac with soft violet shading toward the sides (u), faint seams.
const lacquer = (u, v) => {
  const sh = Math.cos((u - .45) * Math.PI) ** .8, n = n2(u * 4, v * 4) - .5;
  let c = mix(P.lacquerSh, P.lacquer, clamp(.15 + .85 * sh + n * .15));
  if (Math.abs(v - .5) > .46) c = mix(c, P.lacquerDk, .5);                  // joint rims
  if (Math.abs(((u * 3) % 1) - .5) < .02) c = mix(c, P.lacquerSh, .4);       // panel seams
  return [...c.slice(0, 3), 255];
};
// Glowing violet eye sigil (glow card): almond eye, dark pupil, radiating ticks.
const sigil = (u, v) => {
  const x = (u - .5) * 2, y = (v - .5) * 2;
  const eye = Math.abs(y) < .55 * Math.cos(x * Math.PI / 2) && Math.abs(x) < 1;
  const r = Math.hypot(x * .9, y * 1.4);
  if (!eye) { const tick = Math.abs(Math.sin(Math.atan2(y, x) * 4)) > .97 && r < 1 && r > .7; return tick ? A(P.electro, .8) : T; }
  const edge = .55 * Math.cos(x * Math.PI / 2) - Math.abs(y);
  if (edge < .1) return A(P.flash, 1);
  if (r < .22) return A(P.ink, 1);
  if (r < .42) return A(mix(P.electro, P.flash, .3), 1);
  return A(mix(P.deep, P.electro, .5), .95);
};
// Tan gauntlet tile with darker horizontal bands.
const gauntlet = (u, v) => {
  const sh = Math.cos((u - .5) * Math.PI) ** .7, n = n3(u * 5, v * 5) - .5;
  let c = mix(P.tanDk, P.tan, clamp(.3 + .7 * sh + n * .2));
  const band = (v * 4) % 1;
  if (band < .12) c = mix(c, P.tanBand, .75);
  return [...c.slice(0, 3), 255];
};
// Glaive blade (alpha cut, 64 x 256): a long single-edged curved blade, dark violet body, glowing magenta edge line.
const glaiveBlade = (u, v) => {
  const t = 1 - v, spine = .22 + .18 * t * t;                              // spine curves toward +u
  const w = (.5 - .14 * t) * (t > .86 ? Math.sqrt(clamp((1 - t) / .14)) : 1);
  const x = u - spine;
  if (x < 0 || x > w) return T;
  const s = x / w;                                                          // 0 spine .. 1 edge
  let c = mix(C('#7a34b8'), C('#c060e8'), s * .8 + .1 * n1(u * 3, v * 9));
  if (s > .82) c = mix(P.magenta, P.pink, (s - .82) / .18);                  // edge line
  if (s < .07) c = mix(P.deep, P.ink, .5);
  if (Math.abs(s - .38) < .025 && t < .8) c = mix(P.magenta, c, .4);       // fuller line
  return [...c.slice(0, 3), 255];
};
// Glaive shaft tile: dark violet with a magenta pinstripe (wraps round the shaft, v along it).
const glaiveShaft = (u, v) => {
  let c = mix(P.ink, P.shaft, .5 + .5 * Math.cos((u - .4) * Math.PI));
  if (Math.abs(u - .5) < .05) c = mix(P.magenta, c, .3);
  if (Math.abs(((v * 4) % 1) - .5) < .05) c = mix(P.gold, P.goldDk, .5);
  return [...c.slice(0, 3), 255];
};
// Round pink guard ornament (alpha cut): ring with three tomoe, dark core.
const glaiveGuard = (u, v) => {
  const x = (u - .5) * 2, y = (v - .5) * 2, r = Math.hypot(x, y), a = Math.atan2(y, x);
  if (r > 1) return T;
  if (r > .82) return [...mix(P.pink, P.magenta, .4).slice(0, 3), 255];
  if (r < .25) return [...P.ink.slice(0, 3), 255];
  const tomoe = Math.sin(a * 3 + r * 6) > .5;
  return [...(tomoe ? P.pink : mix(P.deep, P.magenta, .25)).slice(0, 3), 255];
};
// Disc halo (alpha cut, 128 x 128): dark disc with a thin outer ring and a violet tomoe-eye emblem at the centre.
const disc = (u, v) => {
  const x = (u - .5) * 2, y = (v - .5) * 2, r = Math.hypot(x, y), a = Math.atan2(y, x);
  if (r > 1) return T;
  if (r > .93) return [...mix(P.electro, P.lilacRim, .5).slice(0, 3), 255];
  if (r > .88) return [...P.ink.slice(0, 3), 255];
  let c = mix(C('#1a1430'), C('#2a1f48'), .5 + .5 * Math.cos(r * 9));
  if (Math.abs(r - .62) < .015) c = mix(P.electro, c, .4);
  if (r < .42) {
    const sw = Math.sin(a * 3 - r * 10) > .35 && r > .12;
    c = sw ? mix(P.electro, P.lilacRim, .4) : mix(P.deep, P.ink, .4);
    if (r < .12) c = P.flash;
  }
  return [...c.slice(0, 3), 255];
};
// Crescent horn (alpha cut): dark curved horn with a violet rim.
const horn = (u, v) => {
  const t = 1 - v, cx = .25 + .45 * t * t, w = .22 * (1 - t) + .02;
  const x = u - cx;
  if (Math.abs(x) > w || t > .98) return T;
  const rim = Math.abs(x) > w - .05;
  return [...(rim ? P.violet : mix(P.ink, P.dark, .5)).slice(0, 3), 255];
};
// Short dagger / spearhead (alpha cut), point up.
const dagger = (u, v) => {
  const t = 1 - v, x = Math.abs(u - .5);
  if (t < .3) return x < .1 ? [...P.shaft.slice(0, 3), 255] : x < .3 && t > .24 ? [...P.gold.slice(0, 3), 255] : T;
  const w = .32 * (1 - (t - .3) / .7) ** .7;
  if (x > w) return T;
  return [...mix(P.lilacRim, P.flash, 1 - x / Math.max(w, 1e-3)).slice(0, 3), 255];
};
// Tasset plate (alpha cut): dark plate, violet glow line, gold rim; pale variant for hip / leg plates.
const plate = pale => (u, v) => {
  const x = Math.abs(u - .5), w = .48 - .1 * v;
  if (x > w || v > .97) return T;
  let c = pale ? mix(C('#b8acd0'), C('#ece6f6'), .3 + .5 * Math.cos(x * Math.PI)) : mix(P.ink, P.dark, .4 + .4 * Math.cos(x * Math.PI));
  if (w - x < .05 || v > .92) c = pale ? P.paleShade : P.goldDk;
  if (!pale && x < .03 && v > .1 && v < .85) c = P.electro;
  return [...c.slice(0, 3), 255];
};

// ---- props -------------------------------------------------------------------------------------------------------------
// Eye orb face (glow): round violet orb with an almond eye.
const orbEye = (u, v) => {
  const x = (u - .5) * 2, y = (v - .5) * 2, r = Math.hypot(x, y);
  if (r > 1) return T;
  const s = sigil(.5 + x * .42, .5 + y * .42);
  const base = A(mix(P.deep, P.electro, clamp(1 - r) * .8 + .1), .95);
  return s[3] > 128 ? s : base;
};
// Vajra crystal facet (glow): translucent violet with bright edges and an inner spark.
const crystal = (u, v) => {
  const x = Math.abs(u - .5), w = .48 * (1 - Math.abs(v - .35) / .65 * .9);
  if (x > w || v < 0) return T;
  const e = clamp(1 - (w - x) / .07);
  return A(mix(mix(P.deep, P.electro, .5 + .5 * (1 - v)), P.flash, e), .55 + .4 * e);
};
// Magenta lotus petal (alpha cut).
const petal = (u, v) => {
  const x = (u - .5) * 2, t = 1 - v, w = Math.sin(t * Math.PI) ** .7 * .9 * (1 - .3 * t);
  if (Math.abs(x) > w || t < .02) return T;
  return [...mix(C('#a02a8a'), P.pink, t * .7 + .2 * (1 - Math.abs(x) / Math.max(w, 1e-3))).slice(0, 3), 255];
};
// 만겁 safe dome (glow): the footage's pale blue-violet bubble (B-17), see-through everywhere: a faint tint (alpha
// ~0.15), soft white cloud patches and two thin drifting light bands, brighter and denser where it meets the floor (the
// soft rim) and a little toward the crown. The look is a function of the point on the sphere (a = azimuth in turns of the
// 90-degree period, e = elevation 0..1), so it runs on across the facet seams (DOME in raiden_geometry.mjs).
const dA = fbm(71), dC = fbm(79);
const DOME_TINT = C('#b2bcff'), DOME_LILAC = C('#d0b8ff'), DOME_WHITE = C('#f8f4ff');
// soft cloud patches: [a, e, angular size in radians], repeated every 90 degrees of azimuth (nearest copy)
const DOME_CLOUDS = [[.04, .10, .30], [.33, .28, .24], [.63, .06, .26], [.82, .40, .25], [.18, .55, .21], [.52, .66, .22],
  [.93, .78, .17], [.40, .93, .15], [.70, .24, .14], [.10, .86, .14], [.27, .02, .12], [.60, .45, .12]];
const domeLook = (a, e) => {
  const lat = e * Math.PI / 2;
  let cloud = 0;
  for (const [ab, eb, size] of DOME_CLOUDS) {
    const dphi = (((a - ab + .5) % 1 + 1) % 1 - .5) * Math.PI / 2, lb = eb * Math.PI / 2;
    // stretched along the azimuth (drifting bands, footage), edges broken up by noise
    const du = Math.cos((lat + lb) / 2) * dphi, dv = 1.9 * (lat - lb), d = Math.hypot(du, dv);
    if (d > size * 1.7) continue;
    const warp = dA(4 * du + 7 * ab, 4 * dv + 11 * eb) - .5;
    cloud = Math.max(cloud, smooth(1.05, .2, d / size + 1.1 * warp));
  }
  const wob = .05 * (dC(3 * a + 2, 2 * e + 7) - .5);
  const band = Math.max(0, 1 - Math.abs(e - .47 - wob) / .01);
  const rim = 1 - smooth(0, .1, e), crown = smooth(.82, 1, e);
  const c = mix(mix(DOME_TINT, DOME_LILAC, .35 + .3 * Math.sin(2 * Math.PI * a)), DOME_WHITE, clamp(.12 + .75 * cloud + .5 * band + .75 * rim + .25 * crown));
  return A(c, .2 + .3 * cloud + .14 * band + .4 * rim * rim + .06 * crown);
};
// Row r: DOME.PARTS slices (part j = slice j), u across the facet's bounding rectangle (its bottom width), v from the top
// edge (0) to the bottom edge (1); outside the trapezoid (plus half a texel, so neighbours meet without a gap) alpha 0.
const domeRow = r => (u, v) => {
  const {ra, ya, rb, yb, wa, wb} = DOME.rows[r], n = DOME.PARTS, j = Math.min(n - 1, Math.floor(u * n)), s = u * n - j - .5;
  const l = 1 - v, w = wa + (wb - wa) * l, x = s * wa;
  if (Math.abs(x) > w / 2 + wa * .5 / 32) return T;
  const frac = clamp(x / w, -.5, .5), rho = ra + (rb - ra) * l, y = ya + (yb - ya) * l;
  return domeLook(((j + .5 + frac) / n) % 1, Math.atan2(y, rho) / (Math.PI / 2));
};
// Cap (part 0, horizontal at the crown): the DOME.N-gon of the profile's top edge; sprite (u, v) = A-frame (X, Z).
const domeCap = (u, v) => {
  const {c, r, y} = DOME.cap, X = (u - .5) * 2 * c, Z = (v - .5) * 2 * c, rho = Math.hypot(X, Z), step = 2 * Math.PI / DOME.N;
  const al = Math.atan2(X, -Z), ak = Math.round(al / step) * step;
  if (rho * Math.cos(al - ak) > r + c / 64) return T;
  return domeLook((((al / (Math.PI / 2) + 1 / 16) % 1) + 1) % 1, Math.atan2(y, rho) / (Math.PI / 2));
};
// Dark orb of the flower and the shadow seed: the round ledge discs of the turned ball (opaque, alpha-cut circle).
const orbDark = (u, v) => {
  const r = Math.hypot(u - .5, v - .5) * 2;
  return r > .98 ? T : [...mix(P.ink, P.deep, .25 + .55 * smooth(.55, .98, r)).slice(0, 3), 255];
};
// Clap hand facets (glow tile): translucent faceted violet.
const clapFacet = (u, v) => {
  const d = Math.min(u, 1 - u, v, 1 - v), f = n1(Math.floor(u * 8) + .5, Math.floor(v * 8) + .5);
  if (d < .045) return A(mix(P.lilacRim, P.flash, .5), .95);
  const rim = clamp(1 - (d - .045) / .2);
  return A(mix(mix(P.ink, P.deep, .6 + .2 * f), P.electro, .15 + .55 * rim * rim), .62 + .2 * rim);
};
// Switch hoop (glow): dark vertical hoop ring with violet rim light.
const hoop = (u, v) => {
  const x = (u - .5) * 2, y = (v - .5) * 2, r = Math.hypot(x, y), d = Math.abs(r - .85);
  if (d > .13) return T;
  return A(mix(P.ink, P.electro, clamp(1 - d / .05) * .7 + (d < .02 ? .3 : 0)), clamp(1 - d / .13) ** 1.2);
};
// Vortex disc (glow): violet spiral arms fading to the rim.
const vortex = (u, v) => {
  const x = (u - .5) * 2, y = (v - .5) * 2, r = Math.hypot(x, y), a = Math.atan2(y, x);
  if (r > 1) return T;
  const arm = .5 + .5 * Math.sin(a * 3 + r * 10);
  return A(mix(P.deep, P.lilacRim, arm * (1 - r)), (arm * .7 + .3) * clamp(1 - r) ** .7);
};

// ---- the derived Tenma skin ---------------------------------------------------------------------------------------------
function readPng(file) {
  const buf = fs.readFileSync(file);
  let o = 8, w = 0, h = 0, ct = 0, idat = [];
  while (o < buf.length) {
    const len = buf.readUInt32BE(o), type = buf.toString('ascii', o + 4, o + 8), data = buf.subarray(o + 8, o + 8 + len);
    if (type === 'IHDR') { w = data.readUInt32BE(0); h = data.readUInt32BE(4); ct = data[9]; if (data[8] !== 8 || data[12]) throw new Error(`${file}: only 8-bit non-interlaced PNGs`); }
    else if (type === 'IDAT') idat.push(data);
    o += 12 + len;
  }
  const bpp = {6: 4, 2: 3}[ct];
  if (!bpp) throw new Error(`${file}: colour type ${ct} unsupported`);
  const raw = zlib.inflateSync(Buffer.concat(idat)), out = Buffer.alloc(w * h * 4), stride = w * bpp, prev = Buffer.alloc(stride);
  for (let y = 0; y < h; y++) {
    const f = raw[y * (stride + 1)], line = Buffer.from(raw.subarray(y * (stride + 1) + 1, (y + 1) * (stride + 1)));
    for (let i = 0; i < stride; i++) {
      const a = i >= bpp ? line[i - bpp] : 0, b = prev[i], c = i >= bpp ? prev[i - bpp] : 0;
      const p = a + b - c, pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c);
      line[i] = (line[i] + [0, a, b, (a + b) >> 1, pa <= pb && pa <= pc ? a : pb <= pc ? b : c][f]) & 255;
    }
    line.copy(prev);
    for (let x = 0; x < w; x++) for (let k = 0; k < 4; k++) out[(y * w + x) * 4 + k] = k < bpp ? line[x * bpp + k] : 255;
  }
  return {w, h, px: out};
}
// Body, arm and leg regions (y >= 16) of a 64 x 64 skin: light, low-saturation kimono pixels -> black bodysuit,
// mid violets -> violet glow lines, dark stockings / boots stay. The head (y < 16) keeps the face and hair.
function tenmaSkinPainter(skinFile) {
  const {w, h, px} = readPng(skinFile);
  if (w !== 64 || h !== 64) throw new Error(`${skinFile}: ${w}x${h}, the rig expects the 64x64 player skin`);
  return (u, v) => {
    const x = Math.min(63, Math.floor(u * 64)), y = Math.min(63, Math.floor(v * 64)), i = (y * 64 + x) * 4;
    const c = [px[i], px[i + 1], px[i + 2], px[i + 3]];
    if (y < 16 || c[3] < 128) return c;
    const L = (Math.max(c[0], c[1], c[2]) + Math.min(c[0], c[1], c[2])) / 510, S = (Math.max(c[0], c[1], c[2]) - Math.min(c[0], c[1], c[2])) / 255;
    const skinTone = c[0] > c[2] + 20 && c[0] > 150;                       // bare skin (thighs, shoulders): keep, a bit darker
    if (skinTone) return [c[0] * .85, c[1] * .8, c[2] * .85, 255];
    if (L > .55) return [...P.suit.slice(0, 3), 255];                      // pale kimono -> bodysuit
    if (S > .3 && L > .3) return [...mix(P.electro, P.lilacRim, .3).slice(0, 3), 255];   // violet trims -> glow lines
    return [c[0] * .55, c[1] * .5, c[2] * .65, 255];                        // the rest darker
  };
}

// name: [w, h, painter, translucent]
export function raidenSprites(rp) {
  const S = {};
  for (const [n, c] of Object.entries(SWATCHES)) S[n] = [16, 16, swatch(c), false];
  Object.assign(S, {
    sleeve_pale: [64, 128, sleeve(false), false], sleeve_dark: [64, 128, sleeve(true), false], drape: [128, 128, drape, true],
    braid: [32, 128, braid, false], flower: [32, 32, flower, false], obi_knot: [32, 32, obiKnot, false], tassel: [16, 64, tassel, false],
    halo_eye: [64, 64, haloEye, true], tomoe_orb: [32, 32, tomoeOrb, true], thread: [16, 64, thread, true],
    katana_blade: [32, 128, katanaBlade, false], polearm_blade: [64, 128, polearmBlade, false], weapon_glow: [32, 128, weaponGlow, true],
    aura_ring: [128, 128, auraRing, true],
    lacquer: [64, 64, lacquer, false], sigil: [64, 64, sigil, true], gauntlet: [64, 64, gauntlet, false],
    glaive_blade: [64, 256, glaiveBlade, false], glaive_shaft: [16, 64, glaiveShaft, false], glaive_guard: [64, 64, glaiveGuard, false],
    disc: [128, 128, disc, false], horn: [32, 64, horn, false], dagger: [32, 64, dagger, false],
    tasset: [32, 64, plate(false), false], plate_pale: [32, 64, plate(true), false],
    orb_eye: [64, 64, orbEye, true], crystal: [64, 128, crystal, true], petal: [64, 64, petal, false], orb_dark: [32, 32, orbDark, false],
    dome_r0: [256, 32, domeRow(0), true], dome_r1: [256, 64, domeRow(1), true], dome_r2: [256, 64, domeRow(2), true], dome_r3: [256, 64, domeRow(3), true],
    dome_cap: [64, 64, domeCap, true],
    clap_facet: [64, 64, clapFacet, true], hoop: [128, 128, hoop, true], vortex: [128, 128, vortex, true],
  });
  const skin = rp && path.join(rp, 'assets/rlk/textures/raiden/skin.png');
  S.skin_tenma = [64, 64, skin && fs.existsSync(skin) ? tenmaSkinPainter(skin) : () => [21, 18, 31, 255], false];
  return S;
}
// Rig sprite px by group (plan §C.6 ledger): props are the prop_* families, everything else is the rig.
export const PROP_SPRITES = new Set(['orb_eye', 'crystal', 'petal', 'orb_dark', 'dome_r0', 'dome_r1', 'dome_r2', 'dome_r3', 'dome_cap', 'clap_facet', 'hoop', 'vortex']);
export function paintRaidenTextures(rp, only = null) {
  const sprites = raidenSprites(rp);
  // skin_tenma samples the skin per texel: paint it without supersampling blur (nearest) by painting at 1x.
  return paintSpriteSet(rp, SPRITE_DIR, sprites, spriteId, only);
}
