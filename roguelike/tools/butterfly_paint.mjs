// Painted sprites of the Moonlit Butterfly (달빛 환영 나비, 달빛의 화신) rig: tools/build_mboss_butterfly_rig.mjs.
// Written to assets/rlk/textures/mboss/butterfly/<name>.png and merged into the item atlas.
//
// Every sprite is drawn in card units as seen from the front of the boss (X = screen right = her LEFT, Y up) on
// the rectangle CARD[name] the geometry places it on (paired parts are painted for her left side; the geometry
// mirrors them). Palette and proportions: scratchpad mb2/understand/model.md §3-§4 (the PDF render, the boss icon
// and the v1-v4 frames). The plates are sculpted: each shape is a signed-distance field, its bevel (plus embossed
// grooves) is a height field, and a fixed light from the upper left gives the cel-like rim highlights and shadows
// of the reference (mboss_paint_lib.mjs Grid / litAt).
//
// Looks of the wing cards (model.md §3.12, §4.2, §7.3):
//   dendro  the in-game look: lime scroll frames, pale white-mint membranes with lime swirls and cyan/violet rims
//   pyro    every membrane, the hindwing blade and the ribbons gold/orange -> magenta (frames unchanged)
//   flat    flat lime (transform and dissolve)
// The holographic overlay of the forewing membranes (fwg_<look>) is a translucent animated strip (8 frames,
// .mcmeta interpolate): the PDF holographic ramp drifts across the lobes like oil on a soap film. Without sprite
// animation the first frame shows, which is a complete static look.
import {
  C, hex, clamp, smooth, mix, fbm, TRANSPARENT, spline, Path, Shape, rng, paintSpriteSet,
  Grid, sdPoly, sdStroke, sdUnion, sdSub, sdInter, sdCircle, sdEllipse, bevel, litAt, tone,
  Feather, bladeProfile, featherPath, featherColour, firstHit, onCard, cubic,
} from './mboss_paint_lib.mjs';
import {ramp} from './weapon_paint.mjs';

// ---- palette (model.md §4.1) ------------------------------------------------------------------------------------
export const PAL = {
  furHi: '#F4FAFC', fur: '#E2F0F3', furShade: '#C0CED9', furLilac: '#A1B1D0', furDeep: '#8C9BAD', furLine: '#66738A',
  capeBlue: '#5671C5', capeDeep: '#3B54A8', capeLit: '#7F95D8', tabardV: '#97A7E0',
  skinHi: '#DFEFFA', skin: '#CFD8EA', skinLilac: '#B9C4E3', skinShade: '#A0B4C7', skinDeep: '#7D96A6', stripe: '#8E9FD4', swirl: '#2F485F',
  bootHi: '#E2F3FB', bootShade: '#8099AA', bootBlue: '#4B83BC', bootDeep: '#5A749F', hoof: '#E8DFC4', hoofShade: '#C8C0A6', hoofDeep: '#98A896', claw: '#F0E0D0',
  helmLit: '#8594AE', helm: '#5A6A88', helmShade: '#3C4757', helmDeep: '#252E35', helmRim: '#ABC4E0', helmTeal: '#286E80',
  antHi: '#B8CAE4', ant: '#83A0E3', antShade: '#566796', chev: '#E1FAAB', chevSat: '#C8E840',
  strHi: '#FAF98D', strLime: '#E6E867', str: '#C7D878', strShade: '#96A564', olive: '#42523F', oliveDeep: '#2F3A22',
  eyeCore: '#FFF4D8', eyeHot: '#FFDAA8', eyeYellow: '#F8E898', coral: '#E3807C', violetHalo: '#C5BAFC', socket: '#89A1E9',
  navyDeep: '#1C2A4D', navy: '#394B75', navyMid: '#5C6B8C', navyRim: '#8A95C9', violetTip: '#7462B5', inlay: '#C8D040', inlayHi: '#DBE9A1',
  steelHi: '#ACC5E9', steelLit: '#8EA6CD', steel: '#5C6F97', steelMid: '#475A80', steelDeep: '#273368', steelShadow: '#1A2A48',
  limeHi: '#E0E4A8', limeGame: '#DFF1A4', lime: '#C7D878', limeMid: '#A4BD6A', limeShade: '#738C3B', limeDeep: '#455326', spiralNavy: '#1B275A',
  ribHi: '#DDF392', rib: '#AACF66', ribMid: '#95B753', ribTeal: '#408970', ribTealDeep: '#30897C',
  tipCore: '#E4F0FF', tipGlow: '#C1DFFA', tipSky: '#86B8EA', tipBlue: '#284AA4', tipDeep: '#1028B6',
  sheenSky: '#76ADDD', sheenPink: '#EBC6F8', sheenLilac: '#D5BCED', sheenViolet: '#AB99EC', sheenPurple: '#7652B6', sheenIndigo: '#3F397B',
  fxCore: '#F1FCC3', fxHi: '#DAFB92', fxLime: '#BEF565', fxMid: '#9DE85C', fxShade: '#83CA5D', fxTeal: '#4DA5A9',
  cocoon: '#374B45', cocoonLit: '#4E6D5C', cocoonWin: '#CADE48', cocoonWinHi: '#D5F086', cocoonSpike: '#BAF74A',
};
for (const k of Object.keys(PAL)) PAL[k] = C(PAL[k]);
const P = PAL;
const white = [255, 255, 255, 255];

// ---- materials --------------------------------------------------------------------------------------------------
// A material is a tone ramp over the diffuse term of litAt (about 0.62 for a flat plate facing the viewer), a
// specular colour and an outline colour.
const mat = (stops, line, spec = white, specK = .55) => ({tone: tone(stops), line, spec, specK});
const M = {
  steel: mat([[-.2, P.steelShadow], [.2, P.steelDeep], [.45, P.steelMid], [.62, P.steel], [.8, P.steelLit], [.95, P.steelHi]], P.steelShadow, C('#E8F0FF')),
  lime: mat([[-.2, P.limeDeep], [.2, P.limeShade], [.45, P.limeMid], [.62, P.lime], [.8, P.limeGame], [.95, P.limeHi]], C('#3A4A1E'), C('#F8FCE0'), .45),
  navy: mat([[-.2, C('#101830')], [.2, P.navyDeep], [.5, P.navy], [.66, P.navyMid], [.85, P.navyRim], [1, C('#B8C2EA')]], C('#0E1428'), C('#DCE4FF')),
  helm: mat([[-.2, P.helmDeep], [.25, P.helmShade], [.55, P.helm], [.74, P.helmLit], [.92, P.helmRim]], C('#161C24'), C('#E0ECFF'), .4),
  rib: mat([[-.2, P.ribTealDeep], [.2, P.ribTeal], [.4, P.ribMid], [.55, P.rib], [.72, C('#C6E46E')], [.88, P.ribHi], [1, C('#F2FFC8')]], C('#2C5A3C'), C('#FAFFE8'), .4),
  cocoon: mat([[-.2, C('#1C2824')], [.25, C('#2A3934')], [.55, P.cocoon], [.75, P.cocoonLit], [.95, C('#7A9A86')]], C('#141C1A'), C('#C8E8D0'), .35),
  hoof: mat([[-.2, P.hoofDeep], [.3, P.hoofShade], [.6, P.hoof], [.9, P.claw]], C('#6A6658'), white, .5),
};
// Shade a sculpted point: material, lighting {diff, spec}, distance to the shape edge d (< 0 inside), pixel size.
function shadeAt(m, L, d, px, {outline = 1.1, shadeMul = 1} = {}) {
  let c = m.tone(L.diff * shadeMul);
  c = mix(c, m.spec, clamp(L.spec * m.specK));
  if (outline && d > -px * outline) c = mix(c, m.line, .85);
  return c;
}
// Height of a bevelled plate with optional grooves (grooveFn returns 0..1 depth).
const plateH = (sd, w, grooves = null, depth = .55) => (x, y) => {
  const d = sd(x, y);
  if (d > .05) return 0;
  let h = bevel(d, w);
  if (grooves) h -= depth * grooves(x, y);
  return h;
};
// Groove profile around a set of paths: depth 1 on the path falling to 0 at half-width hw.
function grooveOf(paths, hw) {
  const P2 = paths.map(p => (p instanceof Path ? p : new Path(p)));
  return (x, y) => {
    let g = 0;
    for (const pth of P2) {
      const [a, b, c, d] = pth.box;
      if (x < a - hw || x > c + hw || y < b - hw || y > d + hw) continue;
      const n = pth.near(x, y);
      if (n.d < hw) g = Math.max(g, Math.cos(n.d / hw * Math.PI / 2) ** 2);
    }
    return g;
  };
}
// Archimedean spiral path about (cx, cy): from radius r0 at angle a0 (deg) outward to r1 over `turns`.
function spiralPts(cx, cy, r0, r1, turns, a0 = 90, dir = 1, n = 64) {
  const out = [];
  for (let i = 0; i <= n; i++) {
    const t = i / n, a = (a0 + dir * 360 * turns * t) * Math.PI / 180, r = r0 + (r1 - r0) * t;
    out.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]);
  }
  return out;
}
const closed = (pts, n = 8) => { const s = spline([...pts, pts[0]], n); s.pop(); return s; };
// Signed distance of a closed smooth outline (Catmull-Rom through the points).
const sdSmooth = (pts, n = 10) => sdPoly(closed(pts, n));
// A tapered stroke: path points, half widths w0 at the start -> w1 at the end (pow shapes the taper).
const taper = (w0, w1, p = 1) => t => w0 + (w1 - w0) * Math.pow(t, p);
const sdTaper = (pts, w0, w1, p = 1, n = 10) => sdStroke(new Path(spline(pts, n)), taper(w0, w1, p));

// ---- card rectangles and sprite sizes ----------------------------------------------------------------------------
// CARD[name] = card rect in card units; SIZE[name] = [w, h] px (multiples of 16). Rects are widened to the pixel
// aspect at the end so texels stay square.
export const CARD = {}, SIZE = {};
const def = (name, rect, size) => { CARD[name] = rect; SIZE[name] = size; };
// forewing (her left; 1 card u = 0.109 b, see butterfly_geometry.mjs WING_FIT): hook top ≈ (21.9, 23.6) u
def('fw', {X0: -2.6, X1: 23.6, Y0: -3.2, Y1: 24.6}, [320, 336]);
def('fwg', {X0: -2.6, X1: 23.6, Y0: -3.2, Y1: 24.6}, [128, 128]);   // overlay frame (strip of FW_FRAMES; mapped over CARD.fw)
def('fwf', {X0: -2.6, X1: 23.6, Y0: -3.2, Y1: 24.6}, [160, 176]);   // flat look
// hindwing (her left; 1 card u = 0.075 b): lime scroll lobe at the root, blade tip ≈ (22.4, -4.2) u
def('hw', {X0: -1, X1: 23, Y0: -7, Y1: 5}, [256, 128]);
def('hwf', {X0: -1, X1: 23, Y0: -7, Y1: 5}, [128, 64]);
export const FW_FRAMES = 8;

// =================================================================================================================
// FOREWING (sheet 07 L1-L3, M1-M2, F1-F2; the PDF render traced with the in-game proportions)
// =================================================================================================================
const FW = (() => {
  // the PDF outline, slightly widened: every point goes through T
  const SX = 1.06, SY = 1, T = pts => pts.map(([x, y]) => [x * SX, y * SY]);
  // steel leading-edge spar: from the top of the scroll plate up to the curled hook (shepherd's crook)
  const spar = T([[3.4, 13.9], [6.4, 14.5], [9.4, 15.4], [12.2, 16.8], [14.8, 18.6], [16.9, 20.5], [18.5, 22.2], [19.6, 23.3], [20.7, 23.7], [21.5, 23.1], [21.4, 22.1], [20.7, 21.6], [20.1, 21.95]]);
  const sparPath = new Path(spline(spar, 10));
  const sparW = t => (t < .72 ? .95 - .3 * t / .72 : t < .9 ? .65 - .17 * (t - .72) / .18 : .48 - .26 * (t - .9) / .1);
  // membrane lobes: the big outer lobe (two bumps on its trailing edge) and the round inner lobe
  const outer = T([[6.5, 11.6], [8.6, 12.7], [11.3, 13.9], [13.9, 15.7], [16.1, 17.7], [17.6, 19.2], [17.6, 17.0], [17.0, 14.9], [16.2, 12.9], [15.1, 11.0], [13.6, 9.4], [12.0, 8.3],
    [10.4, 8.6], [9.2, 9.0], [8.0, 9.2], [7.0, 9.8]]);
  const inner = T([[5.4, 4.6], [6.3, 6.1], [7.9, 6.8], [9.7, 6.3], [10.9, 4.8], [11.0, 2.8], [10.1, 1.1], [8.4, .3], [6.7, .6], [5.6, 1.7], [5.1, 3.1]]
    .map(([x, y]) => [8.2 + (x - 8.2) * 1.22, 3.4 + (y - 3.4) * 1.22]));            // the lower lobe, a little larger than the trace
  const sdO0 = sdSmooth(outer), sdI = sdSmooth(inner);
  // lime tongue curling up into the outer lobe from the border between the lobes (the PDF's S flourish)
  const tongue = sdTaper(T([[9.3, 8.4], [10.3, 9.8], [10.4, 11.1], [9.6, 11.8], [8.8, 11.3], [9.1, 10.6]]), .66, .14, .8);
  const sdO = (x, y) => Math.max(sdO0(x, y), -tongue(x, y));
  const lobes = sdUnion(sdO, sdI);
  const lobeC = T([[12.0, 12.6], [8.1, 3.6]]);
  // lime scroll plate between the root and the lobes (PDF), and the lime tube border round both lobes
  const plate = T([[-.9, 3.2], [-.7, 6.8], [-.1, 9.8], [.6, 12.4], [.2, 14.9], [1.8, 13.9], [3.2, 14.2], [4.6, 14.7], [6.6, 13.3], [6.4, 10.4], [5.4, 7.4], [4.6, 5.0], [4.4, 2.0], [4.9, .1],
    [4.0, -1.0], [2.6, -1.4], [1.7, -2.3], [1.2, -1.2], [.2, .3]]);
  const sdPlate = sdUnion(sdSmooth(plate), tongue);
  const border = .9;
  const sdF = sdSub(sdUnion(sdPlate, (x, y) => lobes(x, y) - border), lobes);
  const sdSpar = (x, y) => { const n = sparPath.near(x, y); return n.d - sparW(n.t); };
  const claws = [
    sdTaper(T([[18.9, 21.4], [18.9, 19.0], [18.3, 16.8], [17.4, 15.0], [16.5, 14.4]]), .58, .07, 1.2),   // hanging claw under the hook
    sdTaper(T([[16.9, 14.3], [18.1, 13.5], [19.2, 13.4], [19.7, 14.1]]), .5, .06, 1.1),                  // trailing claws (3)
    sdTaper(T([[15.3, 10.6], [16.5, 9.5], [17.7, 9.2], [18.3, 9.8]]), .48, .06, 1.1),
    sdTaper(T([[11.2, 2.2], [12.4, 1.2], [13.5, .9], [14.0, 1.4]]), .42, .06, 1.1),
  ];
  const sdClaws = sdUnion(...claws);
  // steel inner frame claw rising behind the plate at the root (drawn behind the lime)
  const sdRootBlade = sdTaper(T([[.1, 3.6], [-.4, 7.0], [-.2, 10.6], [.7, 13.8], [1.8, 16.2], [2.5, 17.8]]), .9, .06, .85);
  // scroll embossing: a spiral eye near the root, a big C-scroll between the plate and the lobes, flourishes
  // raised scroll ridges (sculpted tubes) and finer engraved grooves
  const ridges = grooveOf([
    T(spiralPts(1.9, 3.5, .3, 1.8, 1.6, 90, 1)),
    T(spiralPts(4.0, 8.9, .25, 1.35, 1.25, 250, -1)),
    spline(T([[.3, 6.0], [.6, 9.2], [1.6, 11.6], [3.4, 13.2], [5.2, 13.6]]), 8),
    spline(T([[3.0, -.6], [4.2, 1.0], [4.0, 3.4], [2.8, 5.6], [2.6, 7.4], [3.2, 8.6]]), 8),
  ], .42);
  const grooves = grooveOf([
    spline(T([[1.4, 12.9], [.9, 13.9], [.4, 14.6]]), 6),
    spline(T([[2.0, -1.6], [1.8, -.6], [1.0, .4]]), 6),
    spline(T([[5.6, 11.0], [5.2, 12.2], [4.4, 13.0]]), 6),
  ], .2);
  const silhouette = sdUnion(sdF, lobes, sdSpar, sdClaws, sdRootBlade);
  return {sdO, sdI, lobes, lobeC, sdF, sdPlate, sdSpar, sparPath, sparW, sdClaws, sdRootBlade, ridges, grooves, silhouette, border};
})();
// lazily built grids (shared by the looks)
let FWG = null;
function fwGrids() {
  if (FWG) return FWG;
  const r = CARD.fw, res = 14;
  const lobeRidge = (x, y) => { const d = FW.lobes(x, y); return d > 0 && d < FW.border ? Math.sin(d / FW.border * Math.PI) : 0; };
  FWG = {
    frame: new Grid(r, res, (x, y) => { const d = FW.sdF(x, y); return d > .05 ? 0 : .7 * bevel(d, .8) + .6 * lobeRidge(x, y) + .55 * FW.ridges(x, y) - .35 * FW.grooves(x, y); }),
    steel: new Grid(r, res, (x, y) => Math.max(plateH(FW.sdSpar, .55)(x, y), plateH(FW.sdClaws, .3)(x, y), plateH(FW.sdRootBlade, .45)(x, y))),
    lobes: new Grid(r, res, FW.lobes),
    sil: new Grid(r, res, FW.silhouette),
    spar: new Grid(r, res, FW.sdSpar), claws: new Grid(r, res, FW.sdClaws), root: new Grid(r, res, FW.sdRootBlade), fr: new Grid(r, res, FW.sdF),
  };
  return FWG;
}
// Membrane ramps (core -> rim): in game (dendro), the PDF holographic ramp (overlay), Pyro.
const RAMP = {
  dendro: ramp([[0, '#F0FAE4'], [.14, '#E8F9DE'], [.3, '#DFF1A4'], [.44, '#C2EAB8'], [.56, '#A3D19B'], [.66, '#B2DDEB'], [.76, '#86ACE8'], [.86, '#B6C1E5'], [.94, '#D5BCED'], [1, '#7462B5']]),
  holo: ramp([[0, '#E5E6F5'], [.11, '#B6C1E5'], [.22, '#86ACE8'], [.33, '#6BCBD5'], [.44, '#73A5A3'], [.55, '#6CA57E'], [.66, '#B0B786'], [.77, '#E3E0C9'], [.88, '#EBC6F8'], [1, '#AB99EC']]),
  pyro: ramp([[0, '#FCE2CF'], [.12, '#F9D0B2'], [.3, '#FAD77C'], [.48, '#F2B076'], [.62, '#DF9258'], [.76, '#C680A2'], [.88, '#A35D83'], [1, '#6D5985']]),
  holoPyro: ramp([[0, '#FFF0DC'], [.15, '#FAD77C'], [.3, '#FCE2CF'], [.45, '#F2B076'], [.6, '#EBC6F8'], [.75, '#C680A2'], [.88, '#FAD77C'], [1, '#B17EA3']]),
  sheen: ramp([[0, '#76ADDD'], [.2, '#EBC6F8'], [.42, '#AB99EC'], [.62, '#7652B6'], [.82, '#3F397B'], [1, '#5C6F97']]),
  sheenPyro: ramp([[0, '#FAD77C'], [.25, '#FCE2CF'], [.5, '#C680A2'], [.75, '#A35D83'], [1, '#6D5985']]),
};
const swirlN = fbm(4117);
// Membrane colour: a pearly opal film (the PDF render): white with drifting bands of mint, sky, lilac, pink and
// pale gold, faint lime swirl lines, cyan toward the leading edge, the violet trailing rim. Pyro: gold/peach film,
// orange swirls, magenta rims.
const OPAL = ramp([[0, '#F4F2FF'], [.14, '#B8EEDC'], [.28, '#98D2F4'], [.42, '#C4B2F2'], [.56, '#F0B6DE'], [.7, '#F3E3A2'], [.84, '#C4EA92'], [1, '#F4F2FF']]);
function membrane(look, x, y, d, depth) {
  const rimT = clamp(1 + d / depth);                         // 0 deep inside .. 1 on the edge
  const pyro = look === 'pyro';
  // domain-warped marble: pale patches, base film, swirl lines on the band edges
  const n = swirlN(x * .3, y * .3) - .5;
  const m = Math.sin(.62 * x + 2.3 * Math.sin(.42 * y + 1.5 * Math.sin(.55 * x + .3 * y)) + 3.2 * n);
  const patch = smooth(.15, .55, m);
  let c;
  if (pyro) {
    c = mix(C('#F2B076'), C('#FAD77C'), .5 + .3 * n);
    c = mix(c, C('#FFF1DE'), patch * .95);
    const sw2 = Math.sin(x * 1.3 + y * .8 + 1.8 * Math.sin(y * .6));
    c = mix(c, C('#F9D0B2'), .45 * patch * Math.abs(sw2));
  } else {
    // opal bands follow the warped marble, so the colours swirl like the PDF's holographic film
    const k = (((.09 * x + .06 * y + .22 * m + .5 * n) % 1) + 1) % 1;
    c = mix(C('#F4F8F4'), OPAL(k), .72 + .2 * (1 - patch));
    c = mix(c, C('#FBFDFA'), .28 * patch * (1 - rimT));
  }
  // leading-edge zone of the outer lobe: cool cyan/periwinkle (gold-peach in Pyro)
  const lead = smooth(12.6, 15.8, y + x * .1);
  c = mix(c, pyro ? C('#F9D0B2') : C('#A9DDF0'), .45 * lead);
  // swirl lines where the marble crosses zero
  const lineK = smooth(.12, .02, Math.abs(m - .05)) * (1 - smooth(.7, .9, rimT));
  c = mix(c, pyro ? C('#C96839') : C('#A8CF6A'), (pyro ? .55 : .42) * lineK);
  // rim: through the ramp's outer stops to violet (magenta in Pyro)
  const rg = smooth(.55, 1, rimT);
  c = mix(c, (pyro ? RAMP.pyro : RAMP.dendro)(.64 + .36 * rg), rg * .85);
  return c;
}
function fwPainter(look) {
  const G = fwGrids(), r = CARD.fw, px = (r.X1 - r.X0) / SIZE[look === 'flat' ? 'fwf' : 'fw'][0];
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0);
    const sil = G.sil.at(x, y);
    if (sil > 0) return TRANSPARENT;
    const dSp = G.spar.at(x, y), dCl = G.claws.at(x, y), dL = G.lobes.at(x, y), dF = G.fr.at(x, y), dRB = G.root.at(x, y);
    if (look === 'flat') {
      // flat lime: windows lighter, a soft darker edge so the silhouette reads
      let c = dL < 0 ? mix(P.fxHi, P.fxCore, clamp(-dL / 2)) : P.fxLime;
      if (sil > -px * 1.2) c = mix(c, P.fxShade, .8);
      return c;
    }
    // steel in front: spar, claws and the inner frame claw at the root
    if (dSp < 0 || dCl < 0 || dRB < 0) {
      const L = litAt(G.steel, x, y, {k: 1.4});
      const d = Math.min(dSp, dCl, dRB);
      let c = shadeAt(M.steel, L, d, px, {outline: 0});
      if (dSp < 0) {
        // iridescent sheen strip along the spar's lower edge; a green-teal glint near the hook
        const n = FW.sparPath.near(x, y), w = FW.sparW(n.t), s = n.s / w;      // s < 0: below the spar centre line
        if (s < -.05 && s > -.85 && n.t < .9) {
          const k = smooth(-.05, -.3, s) * smooth(-.85, -.6, s);
          c = mix(c, (look === 'pyro' ? RAMP.sheenPyro : RAMP.sheen)(clamp(n.t * 1.2 + (s + .4) * .4)), .8 * k);
        }
        const g = Math.hypot(x - 19.4, y - 18.6);
        if (g < .9) c = mix(c, C('#33C27A'), .75 * (1 - g / .9));
      }
      if (d > -px * 1.2) c = mix(c, M.steel.line, .85);
      return c;
    }
    if (dL < 0) {
      let c = membrane(look, x, y, dL, 2.2);
      if (dL > -px * 1.3) c = mix(c, C('#4A3C6A'), .65);
      return c;
    }
    if (dF < 0) {
      // lime frame; the tube border on the lobes' trailing side turns dark violet (the glowing pink-violet rim)
      const L = litAt(G.frame, x, y, {k: 1.15});
      let c = shadeAt(M.lime, L, dF, px, {outline: 0});
      const dl = dL;
      if (dl < FW.border) {
        const [gx, gy] = G.lobes.grad(x, y), gm = Math.hypot(gx, gy) || 1;
        const trail = (gx * .62 - gy * .78) / gm;                             // outward normal toward the lower right
        const k = smooth(.05, .5, trail) * smooth(FW.border, FW.border * .3, dl);
        if (k > 0) {
          const vio = mat([[-.2, C('#1E1430')], [.3, C('#3A2C5C')], [.6, look === 'pyro' ? C('#7A3A5A') : C('#5E4A8E')], [.85, look === 'pyro' ? C('#C680A2') : C('#A48ADC')], [1, C('#E8D8FF')]], C('#140C22'));
          c = mix(c, shadeAt(vio, L, dF, px, {outline: 0}), k);
        }
      }
      // contact shadow under the spar and the claws
      const near = Math.min(dSp, dCl, dRB);
      if (near < .6) c = mix(c, P.limeDeep, .45 * (1 - near / .6));
      if (sil > -px * 1.2) c = mix(c, M.lime.line, .85);
      return c;
    }
    // steel root blade behind the plate
    const L = litAt(G.steel, x, y, {k: 1.4});
    let c = shadeAt(M.steel, L, dRB, px, {outline: 0});
    if (dF < .5) c = mix(c, P.steelShadow, .5 * (1 - dF / .5));
    if (sil > -px * 1.2) c = mix(c, M.steel.line, .85);
    return c;
  };
}
// Holographic overlay frame f of FW_FRAMES: translucent PDF ramp over the lobes (alpha 0.30 -> 0.55 at the rim)
// and the spar's leading-edge sheen (0.55), a drifting phase per frame; alpha fades to 0 well inside the edges.
function fwgPainter(look, f) {
  const G = fwGrids(), ph = f / FW_FRAMES;
  const holo = look === 'pyro' ? RAMP.holoPyro : RAMP.holo, sheen = look === 'pyro' ? RAMP.sheenPyro : RAMP.sheen;
  return (u, v) => {
    const r = CARD.fw, x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0);
    const dL = G.lobes.at(x, y);
    if (dL < -.22) {
      const rimT = clamp(1 + dL / 2.4);
      const k = ((x * .085 + y * .055 + .18 * Math.sin(y * .5 + x * .3) + .1 * Math.sin(x * .8 - y * .2 + ph * 6.283) + ph) % 1 + 1) % 1;
      const c = holo(k);
      const a = (.16 + .3 * Math.pow(rimT, 1.8)) * smooth(-.22, -.7, dL);
      return [c[0], c[1], c[2], Math.round(a * 255)];
    }
    const dS = G.spar.at(x, y);
    if (dS < -.18) {
      const n = FW.sparPath.near(x, y), s = n.s / FW.sparW(n.t);
      if (s < -.1 && n.t < .88) {
        const k = ((n.t * 1.4 - ph + 1) % 1);
        const c = sheen(k);
        const a = .55 * smooth(-.1, -.35, s) * smooth(-.95, -.6, s) * smooth(.88, .7, n.t);
        if (a > .02) return [c[0], c[1], c[2], Math.round(a * 255)];
      }
    }
    return TRANSPARENT;
  };
}
// Flat-look overlay: a soft lime glow on the whole wing (the dissolve's emissive sheen).
function fwgFlatPainter() {
  const G = fwGrids();
  return (u, v) => {
    const r = CARD.fw, x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0);
    const d = G.sil.at(x, y);
    if (d > -.25) return TRANSPARENT;
    const c = mix(P.fxCore, P.fxHi, clamp(-G.lobes.at(x, y) / 3));
    return [c[0], c[1], c[2], Math.round(.3 * smooth(-.25, -.8, d) * 255)];
  };
}
// vertical strip of frames for an animated sprite
function strip(w, h, frames, painterOf) {
  const ps = Array.from({length: frames}, (_, f) => painterOf(f));
  return (u, v) => { const f = Math.min(frames - 1, Math.floor(v * frames)); return ps[f](u, v * frames - f); };
}

// =================================================================================================================
// HINDWING (sheet 07 H1-H2): lime scroll lobe with a navy spiral eye, then a long tapering blade, its lower half
// iridescent, ending in a hot blue glowing tip.
// =================================================================================================================
const HW = (() => {
  const lobe = [[-.6, -.4], [-.6, 1.8], [.2, 3.4], [1.4, 4.2], [2.6, 3.6], [3.8, 3.5], [5.4, 3.2], [7.6, 2.4], [10.2, 1.0], [12.6, .0],
    [11.6, -1.3], [9.4, -2.0], [7.4, -2.9], [5.2, -3.4], [3.2, -3.0], [1.4, -2.2]];
  // the curled crest at the top of the scroll (a hooked flame tip pointing up and back toward the body)
  const crest = sdTaper([[2.6, 3.0], [1.6, 4.4], [.2, 5.0], [-.6, 4.4], [-.2, 3.8]], .62, .1, .8);
  const sdLobe = sdUnion(sdSmooth(lobe), crest);
  const bladeTop = [[8.0, 1.6], [11.4, .4], [14.6, -.8], [17.6, -2.0], [20.4, -3.3], [22.6, -4.5]];
  const bladeBot = [[22.6, -4.5], [20.0, -4.1], [17.0, -3.7], [14.0, -3.3], [11.0, -2.9], [8.0, -2.6]];
  const bl = [...spline(bladeTop, 8), ...spline(bladeBot, 8).slice(1)];
  const sdBlade = sdPoly(bl);
  const spine = new Path(spline([[8.0, -.5], [11.5, -1.25], [15.0, -2.2], [18.5, -3.15], [22.6, -4.5]], 8));
  const sdEye = sdCircle(4.0, .25, 2.05);
  // the volute: a raised spiral tube (the grooves between its turns are the dark navy gaps), flourishes
  const volute = grooveOf([spiralPts(4.0, .25, .35, 2.0, 1.55, 80, 1)], .4);
  const grooves = grooveOf([spline([[1.0, 3.2], [2.6, 2.2], [5.6, 2.4], [8.6, 1.4]], 8), spline([[1.6, -1.6], [3.6, -2.4], [6.6, -2.2], [9.6, -1.5]], 8)], .22);
  const sil = sdUnion(sdLobe, sdBlade);
  return {sdLobe, sdBlade, spine, sdEye, volute, grooves, sil};
})();
let HWG = null;
function hwGrids() {
  if (HWG) return HWG;
  const r = CARD.hw, res = 14;
  HWG = {
    h: new Grid(r, res, (x, y) => Math.max(plateH(HW.sdLobe, .75, HW.grooves, .5)(x, y) + (HW.sdEye(x, y) < 0 ? .55 * HW.volute(x, y) - .35 : 0), .9 * plateH(HW.sdBlade, .5)(x, y))),
    sil: new Grid(r, res, HW.sil), lobe: new Grid(r, res, HW.sdLobe), blade: new Grid(r, res, HW.sdBlade), eye: new Grid(r, res, HW.sdEye),
  };
  return HWG;
}
function hwPainter(look) {
  const G = hwGrids(), r = CARD.hw, px = (r.X1 - r.X0) / SIZE[look === 'flat' ? 'hwf' : 'hw'][0];
  const tipRamp = ramp([[0, '#A4BD6A'], [.35, '#86B8EA'], [.6, '#284AA4'], [.72, '#1028B6'], [.84, '#86B8EA'], [.93, '#C1DFFA'], [1, '#E4F0FF']]);
  const tipPyro = ramp([[0, '#F2B076'], [.4, '#DF9258'], [.62, '#C05C6F'], [.76, '#C680A2'], [.9, '#FCE2CF'], [1, '#FFF6E8']]);
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0);
    const ds = G.sil.at(x, y);
    if (ds > 0) return TRANSPARENT;
    if (look === 'flat') {
      let c = mix(P.fxLime, P.fxHi, smooth(14, 22, x));
      if (ds > -px * 1.2) c = mix(c, P.fxShade, .8);
      return c;
    }
    const L = litAt(G.h, x, y, {k: 1.2});
    const dLobe = G.lobe.at(x, y), dB = G.blade.at(x, y);
    let c;
    if (dLobe < 0 && !(dB < 0 && x > 10.5)) {
      c = shadeAt(M.lime, L, ds, px, {outline: 0});
      // the volute: a raised lime spiral tube over a sunken dark navy disc (the "eye")
      const de = G.eye.at(x, y);
      if (de < 0) {
        const tube = HW.volute(x, y);
        c = tube > .25 ? c : mix(c, P.spiralNavy, .9 * smooth(.25, .05, tube) * smooth(0, -.25, de));
      }
    } else {
      // blade: lime upper half, iridescent lower half, glowing blue tip
      const n = HW.spine.near(x, y), t = n.t;
      const upper = n.s > 0;
      c = shadeAt(M.lime, L, ds, px, {outline: 0});
      if (!upper) {
        const k = clamp((x * .11 + y * .2 + 10) % 1);
        c = mix(c, (look === 'pyro' ? RAMP.pyro : RAMP.holo)(k), .7);
        c = mix(c, look === 'pyro' ? C('#F9D0B2') : C('#E8F4FF'), .25 * Math.pow(Math.max(0, L.diff - .5) * 2, 2));
      }
      const tip = smooth(.62, 1, t);
      if (tip > 0) c = mix(c, (look === 'pyro' ? tipPyro : tipRamp)(tip), smooth(0, .25, tip));
    }
    if (ds > -px * 1.2) c = mix(c, x > 19 ? (look === 'pyro' ? C('#8A3A3A') : P.tipDeep) : M.lime.line, .85);
    return c;
  };
}

// =================================================================================================================
// FUR: stylised clumps (short lanceolate tufts with outlines and fine strands, the Guardian's feather technique)
// in the cool off-white of the mane with lilac-blue creases; capelet tufts end in royal blue.
// =================================================================================================================
const FUR = {base: P.fur, light: P.furHi, shadeC: P.furShade, deep: P.furLilac, line: P.furLine, sky: P.furLilac};
const furR = seed => rng(seed);
// Tuft list -> painter. tuft: {r: [x, y] root, a: angle from straight down (deg, + toward +X), L, w, bend, tip}
// (tip: colour the last part of the tuft takes, e.g. the capelets' royal blue). First in the list = in front.
function furPainter(rect, tufts, {px = .08, shadow = .9, tipK = .55} = {}) {
  const grain = fbm(977);
  // keep every tuft inside the card (a tuft cut by the card edge shows as a straight line): shorten it until its
  // tip and its sides fit, with a small margin
  const m = .25;
  for (const t of tufts) {
    for (let i = 0; i < 30; i++) {
      const ar = t.a * Math.PI / 180, tx = t.r[0] + Math.sin(ar) * t.L, ty = t.r[1] - Math.cos(ar) * t.L;
      const okTip = tx > rect.X0 + m && tx < rect.X1 - m && ty > rect.Y0 + m && ty < rect.Y1 - m;
      const okSide = t.r[0] - t.w > rect.X0 + m && t.r[0] + t.w < rect.X1 - m && t.r[1] + t.w < rect.Y1 - m && t.r[1] - t.w > rect.Y0 + m;
      if (okTip && okSide) break;
      t.L *= .9; if (!okSide) t.w *= .9;
    }
  }
  const list = tufts.filter(t => t.L > .6).map(t => ({
    f: new Feather(featherPath(t.r, t.a, t.L, t.bend || [0, 0, 0], 12), bladeProfile({w: t.w, lead: .5, root: .62, peak: .3, tip: .5, tipPow: 1.35})),
    col: (h, x, y) => {
      // a soft rounded clump: lilac in the crease at its root and along its edges, bright toward the middle and tip
      const e = Math.pow(h.e, .7);
      let c = mix(P.furShade, P.fur, clamp(.5 + .8 * e));
      c = mix(c, P.furHi, clamp((e - .5) * 1.6) * (.45 + .55 * h.t));
      c = mix(c, P.furLilac, (1 - h.t) * .15);
      // strands along the clump
      const st = Math.sin(h.s * 9 + h.t * 3 + 6 * grain(x * .6, y * .6));
      c = mix(c, P.furShade, smooth(.75, 1, st) * .15 * (1 - h.t * .5));
      if (t.tip) c = mix(c, t.tip, Math.min(1, tipK * smooth(.4, .85, h.t) * (.7 + .3 * e)));
      if (t.shade) c = mix(c, P.furLilac, t.shade);
      // a soft light edge so the clumps separate without outlines (soft fur, not shingles)
      if (h.edge < px * 1.1) c = mix(c, C('#B2BFD4'), .45);
      return c;
    },
  }));
  return onCard(rect, (x, y) => {
    for (let i = 0; i < list.length; i++) {
      const h = list[i].f.sample(x, y);
      if (!h) continue;
      let c = list[i].col(h, x, y);
      // soft contact shadow of the clumps in front
      for (let j = Math.max(0, i - 40); j < i; j++) {
        const g = list[j].f.sample(x, y, shadow);
        if (g) { c = mix(c, P.furLilac, .2 * clamp(1 + g.edge / shadow)); break; }
      }
      return c;
    }
    return null;
  });
}
// Rows of tufts filling an envelope: top(x) / bot(x) bound the roots; tufts hang down (fanned by `fan` deg per
// unit of x), the bottom row longer; an upper fringe of short tufts points up so the top edge is fluffy too.
function furRows(seed, {x0, x1, top, bot, L = 3, Lb = 4.6, w = 1.25, dx = 1.15, dy = 1.25, fan = 2.5, fringe = true, tip = null, tipRows = 0, spread = 14}) {
  const R = furR(seed), out = [], rows = [];
  for (let y = 0; ; y++) {
    const row = [];
    for (let x = x0 + (y % 2 ? dx / 2 : 0); x <= x1 + 1e-6; x += dx) {
      const yt = top(x) - y * dy;
      if (yt < bot(x) - .2) continue;
      const last = yt - dy < bot(x) - .2;
      const j = (R() - .5) * spread;
      row.push({r: [x + (R() - .5) * dx * .4, yt + (R() - .5) * .3], a: x * fan + j, L: (last ? Lb : L) * (.82 + .36 * R()), w: w * (.85 + .3 * R()),
        bend: [(R() - .5) * .14, (R() - .5) * .18, (R() - .5) * .22], last});
    }
    if (!row.length) break;
    rows.push(row);
    if (y > 40) break;
  }
  // tip colour on the last rows (capelets), slight lilac shade deeper in
  rows.forEach((row, i) => row.forEach(t => {
    if (tip && i >= rows.length - tipRows) t.tip = tip;
    t.shade = .12 * (i / Math.max(1, rows.length - 1));
  }));
  for (const row of rows) out.push(...row);
  if (fringe) {
    const R2 = furR(seed + 7);
    for (let x = x0 + .3; x <= x1; x += dx * 1.1) out.unshift({r: [x, top(x) - .5], a: 180 + x * fan * .6 + (R2() - .5) * 40, L: 1.3 + R2() * .9, w: w * .7});
  }
  return out;
}
// Fur tile for turned (lathe) cores: strands and clumps, not cut out.
function furTile(seed, base = P.fur, shade = P.furShade, lines = P.furLilac) {
  const n = fbm(seed);
  return (u, v) => {
    const s = Math.sin(u * 40 + 6 * n(u * 3, v * 3) + v * 3) * .5 + .5;
    let c = mix(base, shade, smooth(.3, 1, v) * .5 + (n(u * 6, v * 6) - .5) * .35);
    c = mix(c, lines, smooth(.85, 1, s) * .35);
    c = mix(c, P.furHi, smooth(.2, 0, v) * .4);
    return c;
  };
}

// ---- mane cards (the collar display, scale 1, pivot 2.25 b; an octagonal shell of cards round the neck) --------
def('mane_f', {X0: -11.2, X1: 11.2, Y0: -7.2, Y1: 6.4}, [256, 160]);     // front ruff (chest tufts to 1.89 b)
def('mane_fs', {X0: -5.8, X1: 5.8, Y0: -6.2, Y1: 6.0}, [128, 128]);      // front corners (turned 45 deg)
def('mane_s', {X0: -6.4, X1: 6.4, Y0: -5.6, Y1: 6.0}, [128, 128]);       // sides (cardX: X here runs front -> back)
def('mane_bs', {X0: -5.8, X1: 5.8, Y0: -7.0, Y1: 6.0}, [128, 144]);      // back corners: capelets with blue tips
def('mane_b', {X0: -9.6, X1: 9.6, Y0: -17.6, Y1: 7.6}, [192, 256]);      // back: hood, capelets, blue V, tabard
const capeTip = mix(P.capeBlue, P.capeDeep, .35);
function maneFront() {
  // top: dips under the chin, rises beside the head and over the shoulders; bottom: pointed chest tufts
  // a fluffy ball from the front: dips under the chin, rounded shoulders, pointed chest tufts lowest in the middle
  const top = x => { const a = Math.abs(x); return .3 + 5.0 * smooth(.8, 4.6, a) - 4.4 * smooth(6.6, 10.8, a) * smooth(6.6, 10.8, a); };
  const bot = x => -4.6 + 3.6 * smooth(0, 9.5, Math.abs(x));        // a V of chest tufts, lowest in the middle
  return furPainter(CARD.mane_f, furRows(311, {x0: -10.0, x1: 10.0, top, bot, L: 3.6, Lb: 4.8, w: 1.9, dx: 1.55, dy: 1.45, fan: 3.6, spread: 18}));
}
function maneCorner(seed, back) {
  // a rounded clump of fur (dome on top, rounded tufted bottom), not a rectangle
  const top = x => 3.9 - 3.2 * (x / 4.6) ** 2, bot = x => (back ? -3.4 : -2.2) - .25 * x + 2.6 * (x / 4.6) ** 4;
  return furPainter(CARD[back ? 'mane_bs' : 'mane_fs'], furRows(seed, {x0: -4.3, x1: 4.3, top, bot, L: 3.4, Lb: back ? 4.4 : 4.0, w: 1.85, dx: 1.5, dy: 1.45, fan: 2.4, spread: 18,
    tip: back ? capeTip : null, tipRows: back ? 3 : 0}), {tipK: 1});
}
function maneSide() {
  // side silhouette: front edge (X -6) under the chin, back edge (X +6) with capelets hanging lower
  const top = x => 3.4 - 2.6 * (x / 5.4) ** 2, bot = x => -1.6 - .22 * (x + 6) + 2.2 * (x / 5.4) ** 4;
  return furPainter(CARD.mane_s, furRows(331, {x0: -5.0, x1: 5.0, top, bot, L: 3.4, Lb: 4.2, w: 1.85, dx: 1.5, dy: 1.45, fan: 1.6, spread: 18, tip: capeTip, tipRows: 1}), {tipK: .7});
}
function maneBack() {
  // hood behind the head (top), layered capelets with royal-blue tips, the blue V down the spine, the tabard
  const hood = furRows(347, {x0: -4.0, x1: 4.0, top: x => 6.6 - .12 * x * x, bot: () => 3.4, L: 3.0, Lb: 3.4, w: 1.8, dx: 1.5, dy: 1.4, fan: 3.4, spread: 18});
  const capes = furRows(353, {x0: -8.8, x1: 8.8, top: x => 3.4 - .02 * x * x, bot: x => -3.2 - .12 * Math.abs(x), L: 3.6, Lb: 5.0, w: 2.0, dx: 1.6, dy: 1.5, fan: 3.8, spread: 16, tip: capeTip, tipRows: 3, fringe: false});
  // spine tuft (deep blue) and the tabard below the capes
  const spine = [{r: [0, 1.0], a: 0, L: 6.4, w: 1.6, tip: P.capeDeep}, {r: [-.9, .4], a: -8, L: 5.2, w: 1.2, tip: P.capeBlue}, {r: [.9, .4], a: 8, L: 5.2, w: 1.2, tip: P.capeBlue}];
  const fur = furPainter(CARD.mane_b, [...hood, ...spine, ...capes], {tipK: 1});
  const tab = sdSmooth([[-3.0, -3.6], [3.0, -3.6], [2.6, -9.0], [1.4, -13.6], [0, -17.2], [-1.4, -13.6], [-2.6, -9.0]]);
  const vIn = sdUnion(sdTaper([[-2.2, -5.0], [-1.0, -10.0], [0, -14.4]], .32, .12), sdTaper([[2.2, -5.0], [1.0, -10.0], [0, -14.4]], .32, .12));
  const r = CARD.mane_b;
  return (u, v) => {
    const c = fur(u, v);
    if (c[3]) return c;
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = tab(x, y);
    if (d > 0) return TRANSPARENT;
    let k = mix(P.fur, P.furShade, smooth(-3.6, -15, y) * .6 + smooth(-1.5, 0, d) * .3);
    if (vIn(x, y) < 0) k = mix(k, C(PAL.tabardV), .85);
    if (d > -.12) k = mix(k, P.furLine, .8);
    return k;
  };
}

// =================================================================================================================
// HEAD (scale 1, pivot = the neck 2.38 b): faceted steel-blue helmet-mask pointing down like a beak, the lime
// chevron, cheek blades, crown spikes (the boss icon, sheet 02)
// =================================================================================================================
def('helm', {X0: -3.3, X1: 3.3, Y0: -.6, Y1: 7.6}, [96, 128]);
def('cheek', {X0: 1.4, X1: 7.8, Y0: -.4, Y1: 6.6}, [96, 96]);
def('crown', {X0: -3.8, X1: 3.8, Y0: 2.8, Y1: 10.4}, [96, 96]);
def('helm_side', {X0: -2.8, X1: 2.8, Y0: -.6, Y1: 7.6}, [64, 96]);       // side of the helmet (cardX: X = front -> back)
def('eye', {X0: -.7, X1: .7, Y0: -.45, Y1: .45}, [32, 32]);
def('chev', {X0: -1.2, X1: 1.2, Y0: -.7, Y1: .7}, [48, 32]);
// facets of the mask (her left half; the right half mirrors): polygon, facet normal (x, y, z), the right half
// takes (-x, y, z). Light from the upper left, so her right half is a shade darker as on the icon.
const HELM_FACETS = [
  {p: [[0, 7.4], [.9, 5.6], [0, 4.9]], n: [.35, .55, .76]},                         // crown spike, left face
  {p: [[0, 4.9], [.9, 5.6], [1.9, 4.6], [1.4, 3.6], [0, 3.2]], n: [.3, .45, .84]},   // brow plate
  {p: [[.9, 5.6], [2.6, 4.4], [3.1, 3.0], [1.9, 4.6]], n: [.62, .45, .64]},           // temple
  {p: [[1.9, 4.6], [3.1, 3.0], [2.6, 1.9], [1.4, 3.6]], n: [.55, .15, .82]},          // upper cheek
  {p: [[0, 3.2], [1.4, 3.6], [2.6, 1.9], [1.6, .9], [0, 1.6]], n: [.32, -.1, .94]},   // eye plate (the eye sits here)
  {p: [[0, 1.6], [1.6, .9], [0, -.4]], n: [.3, -.5, .81]},                           // beak, left face
  {p: [[2.6, 1.9], [3.1, 3.0], [3.2, 1.6], [1.6, .9]], n: [.7, -.25, .67]},           // jaw side
];
function helmPainter() {
  const facets = [];
  for (const f of HELM_FACETS) {
    facets.push({sd: sdPoly(f.p), n: f.n});
    facets.push({sd: sdPoly(f.p.map(([x, y]) => [-x, y])), n: [-f.n[0], f.n[1], f.n[2]]});
  }
  const L = (() => { const v = [-.48, .62, .62], m = Math.hypot(...v); return v.map(x => x / m); })();
  const r = CARD.helm, px = (r.X1 - r.X0) / SIZE.helm[0];
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0);
    let best = null;
    for (const f of facets) { const d = f.sd(x, y); if (d < 0 && (!best || d < best.d)) best = {d, n: f.n}; }
    if (!best) return TRANSPARENT;
    const diff = best.n[0] * L[0] + best.n[1] * L[1] + best.n[2] * L[2];
    let c = M.helm.tone(diff);
    // a teal bounce on the lower facets (game light), lit rim on facet edges facing the light
    c = mix(c, P.helmTeal, .25 * smooth(2.5, 0, y));
    if (best.d > -px * 2.2) c = mix(c, diff > .6 ? P.helmRim : P.helmDeep, .55);
    // the centre ridge highlight and the eye sockets (violet glow round the eyes)
    if (Math.abs(x) < px * 1.2 && y > 1.6) c = mix(c, P.helmRim, .6);
    const e = Math.hypot((Math.abs(x) - 1.45) / 1.0, (y - 2.0) / .62);
    if (e < 1) c = mix(c, P.socket, .55 * (1 - e));
    // the outer silhouette line
    let sil = Infinity; for (const f of facets) sil = Math.min(sil, f.sd(x, y));
    return c;
  };
}
function cheekPainter() {
  // two angular dark-steel blades sweeping out and up from beside the eye
  const b1 = sdPoly([[1.8, 1.0], [3.4, 2.4], [7.4, 6.2], [4.6, 2.0], [3.0, .6]]);
  const b2 = sdPoly([[2.2, 2.6], [3.6, 3.6], [6.0, 5.0], [3.9, 2.6]]);
  const sd = sdUnion(b1, b2);
  const G = new Grid(CARD.cheek, 16, plateH(sd, .45));
  const r = CARD.cheek, px = (r.X1 - r.X0) / SIZE.cheek[0];
  const m = mat([[-.2, P.helmDeep], [.3, C('#2E3A4E')], [.55, C('#485162')], [.8, C('#6E7E9C')], [1, P.helmRim]], C('#10141C'));
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    let c = shadeAt(m, litAt(G, x, y, {k: 1.6}), d, px, {outline: 1.3});
    // a cool rim light along the upper edges
    if (d > -px * 3 && y > 2.2) c = mix(c, P.helmRim, .35);
    return c;
  };
}
function crownPainter() {
  // 5 navy crown spikes with lavender rims fanning behind the crown
  const sp = [[0, 10.0, 0, 1.0], [-1.8, 8.4, -22, .8], [1.8, 8.4, 22, .8], [-3.0, 6.6, -45, .7], [3.0, 6.6, 45, .7]];
  const shapes = sp.map(([tx, ty, a, w]) => {
    const bx = tx * .35, by = 4.2;
    return sdPoly([[bx - w, by], [tx, ty], [bx + w, by], [bx, by - .8]]);
  });
  const sd = sdUnion(...shapes);
  const G = new Grid(CARD.crown, 14, plateH(sd, .4));
  const r = CARD.crown, px = (r.X1 - r.X0) / SIZE.crown[0];
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    let c = shadeAt(M.navy, litAt(G, x, y, {k: 1.4}), d, px, {outline: 0});
    if (d > -px * 2.6) c = mix(c, C('#B9AEEA'), .7);
    return c;
  };
}
function helmSidePainter() {
  // the helmet seen from the side: the beak profile in front, the crown spike, dark back (covered by the hood)
  const sd = sdSmooth([[-2.6, 2.2], [-2.0, .4], [-1.0, -.4], [.4, .2], [1.8, 1.6], [2.6, 3.6], [2.0, 5.8], [.6, 7.2], [-.6, 6.4], [-1.6, 4.6]]);
  const G = new Grid(CARD.helm_side, 14, plateH(sd, .9));
  const r = CARD.helm_side, px = (r.X1 - r.X0) / SIZE.helm_side[0];
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    return shadeAt(M.helm, litAt(G, x, y, {k: 1.2}), d, px);
  };
}
function eyePainter() {
  // almond eye: hot cream core, yellow, coral ring, violet halo (glow card, brightness 15)
  return (u, v) => {
    const x = (u - .5) * 2, y = (v - .5) * 2;
    const e = Math.hypot(x / 1.0, y / (.62 - .2 * Math.abs(x)));
    if (e > 1) return TRANSPARENT;
    if (e < .32) return mix(P.eyeCore, P.eyeHot, e / .32);
    if (e < .55) return mix(P.eyeHot, P.eyeYellow, (e - .32) / .23);
    if (e < .8) return mix(P.coral, C('#D86A78'), (e - .55) / .25);
    return mix(P.violetHalo, P.socket, (e - .8) / .2);
  };
}
function chevPainter() {
  const sd = sdUnion(sdTaper([[-1.0, .55], [0, -.5]], .2, .26), sdTaper([[1.0, .55], [0, -.5]], .2, .26));
  return (u, v) => {
    const x = -1.2 + u * 2.4, y = .7 - v * 1.4, d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    return mix(P.chev, C('#F6FFD8'), smooth(-.05, -.18, d));
  };
}

// ---- crest (scale 1, pivot 2.75 b on the head): periwinkle antennae and the lime flame streamers ---------------
def('antenna', {X0: -.6, X1: 4.6, Y0: -1.0, Y1: 8.4}, [48, 96]);
def('streamer', {X0: -1.2, X1: 8.4, Y0: -2.0, Y1: 13.6}, [96, 160]);
function antennaPainter() {
  const pth = new Path(spline([[.4, -.6], [1.2, 2.6], [2.0, 5.4], [3.0, 7.3], [3.9, 7.9]], 10));
  const r = CARD.antenna, px = (r.X1 - r.X0) / SIZE.antenna[0];
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0);
    const n = pth.near(x, y), w = .36 - .22 * n.t;
    if (n.d > w) return TRANSPARENT;
    const s = n.s / w;                                  // -1..1 across
    let c = mix(P.ant, P.antHi, smooth(.2, .9, s));
    c = mix(c, P.antShade, smooth(-.2, -.9, s));
    if (n.d > w - px * 1.1) c = mix(c, C('#34406A'), .7);
    return c;
  };
}
function streamerPainter() {
  // broad flame blade: S-curved, the tip curling outward; lime -> pale -> dark olive tip (last quarter)
  const spine = [[.2, -1.6], [1.3, 1.2], [1.9, 4.0], [1.5, 6.8], [1.8, 9.4], [3.2, 11.5], [5.2, 12.9], [6.9, 13.1]];
  const pth = new Path(spline(spine, 10));
  const w = t => .3 + .78 * Math.sin(Math.min(1, t / .55) * Math.PI / 2) * (t < .55 ? 1 : 1 - Math.pow((t - .55) / .45, 1.25));
  const sd = (x, y) => { const n = pth.near(x, y); return n.d - w(n.t) * (n.s > 0 ? 1 : .8); };
  const G = new Grid(CARD.streamer, 14, plateH(sd, .9));
  const r = CARD.streamer, px = (r.X1 - r.X0) / SIZE.streamer[0];
  const colOf = tone([[0, P.str], [.35, P.strLime], [.55, P.strHi], [.72, P.strLime], [.8, P.strShade], [.9, P.olive], [1, P.oliveDeep]]);
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    const n = pth.near(x, y), L = litAt(G, x, y, {k: 1.0});
    let c = colOf(n.t);
    c = mix(c, n.t > .8 ? P.oliveDeep : P.limeShade, clamp((.62 - L.diff) * 1.4));
    c = mix(c, n.t > .8 ? C('#6E7E5A') : C('#FBFCC8'), clamp((L.diff - .72) * 2.4));
    // a vein along the spine
    if (Math.abs(n.s) < px * 1.2 && n.t < .82) c = mix(c, P.strShade, .5);
    if (d > -px * 1.2) c = mix(c, n.t > .8 ? C('#1E2614') : C('#5E6E2E'), .8);
    return c;
  };
}

// ---- fans (scale 1.25, pivot at the shoulder): navy side blades, lime inner strokes, periwinkle tips -------------
def('fan', {X0: -1.2, X1: 19.6, Y0: -15.2, Y1: 3.2}, [176, 160]);
def('fanb', {X0: -1.2, X1: 15.6, Y0: -11.2, Y1: 3.2}, [144, 128]);
def('shplate', {X0: -2.6, X1: 3.0, Y0: -1.4, Y1: 9.2}, [64, 112]);
// a curved sickle blade from root r at angle a (deg below the horizontal, outward +X), length L, width w
function sickle(r, a, L, w, curl = .18) {
  const ar = a * Math.PI / 180, d = [Math.cos(ar), -Math.sin(ar)], nrm = [Math.sin(ar), Math.cos(ar)];
  const P2 = (f, b) => [r[0] + d[0] * L * f + nrm[0] * L * b, r[1] + d[1] * L * f + nrm[1] * L * b];
  const pts = cubic(r, P2(.35, curl * .25), P2(.7, curl * .7), P2(1, curl * 1.3), 14);
  return {path: new Path(pts), w: t => w * (t < .25 ? .55 + .45 * t / .25 : 1 - Math.pow((t - .25) / .75, 1.5) * .97)};
}
function bladePainter(rect, size, blades, {inlay = true, tips = true} = {}) {
  const sds = blades.map(b => (x, y) => { const n = b.path.near(x, y); return n.d - b.w(n.t); });
  const G = new Grid(rect, 12, (x, y) => Math.max(...sds.map(f => plateH(f, .38)(x, y))));
  const px = (rect.X1 - rect.X0) / size[0];
  return (u, v) => {
    const x = rect.X0 + u * (rect.X1 - rect.X0), y = rect.Y1 - v * (rect.Y1 - rect.Y0);
    for (let i = 0; i < blades.length; i++) {
      const d = sds[i](x, y);
      if (d > 0) continue;
      const n = blades[i].path.near(x, y), L = litAt(G, x, y, {k: 1.5});
      let c = shadeAt(M.navy, L, d, px, {outline: 0});
      if (tips) c = mix(c, C('#B4C0EE'), smooth(.7, .98, n.t) * .8);
      if (inlay && n.t > .12 && n.t < .62) {
        const s = n.s / Math.max(1e-6, blades[i].w(n.t));
        if (s > .05 && s < .38) c = mix(c, P.inlay, .85 * smooth(.05, .14, s) * smooth(.38, .28, s));
      }
      if (d > -px * 1.2) c = mix(c, M.navy.line, .85);
      return c;
    }
    return TRANSPARENT;
  };
}
const FAN_BLADES = () => [sickle([.2, .2], 6, 15.8, 1.05, -.16), sickle([.1, -.5], 22, 15.0, 1.0, -.2), sickle([-.1, -1.2], 40, 13.2, .95, -.22)];
const FANB_BLADES = () => [sickle([.2, 0], 30, 12.6, .9, -.2), sickle([0, -.8], 52, 10.8, .85, -.22)];
function shplatePainter() {
  // upright navy leaf blade pointing up and out with a lime spiral "eye"
  const sd = sdSmooth([[-1.9, .2], [-1.2, 3.6], [-.2, 6.6], [1.2, 8.8], [1.6, 6.2], [2.4, 3.4], [2.0, .6], [.4, -1.0]]);
  const G = new Grid(CARD.shplate, 14, plateH(sd, .6, grooveOf([spiralPts(.2, 2.4, .2, 1.1, 1.3, 90, 1)], .22), .55));
  const r = CARD.shplate, px = (r.X1 - r.X0) / SIZE.shplate[0];
  const spiral = new Path(spiralPts(.2, 2.4, .2, 1.1, 1.3, 90, 1));
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    let c = shadeAt(M.navy, litAt(G, x, y, {k: 1.4}), d, px);
    if (spiral.near(x, y).d < .2) c = mix(c, P.inlay, .9);
    if (d > -px * 3 && d < -px * 1.2) c = mix(c, P.navyRim, .45);
    return c;
  };
}

// ---- crescent hands, shards, flakes (scale 1) ---------------------------------------------------------------------
def('crescent', {X0: -5.2, X1: 5.2, Y0: -9.6, Y1: 9.6}, [80, 144]);
def('crescent_tell', {X0: -5.2, X1: 5.2, Y0: -9.6, Y1: 9.6}, [80, 144]);
def('shard', {X0: -2.2, X1: 6.2, Y0: -9.4, Y1: 1.4}, [64, 80]);
def('diamond', {X0: -1.6, X1: 1.6, Y0: -2.6, Y1: 2.6}, [32, 48]);
// The big crescent (her left side: convex edge outward +X, both tips curving back toward the body).
function crescentShape() {
  const outerArc = cubic([-1.6, 9.0], [6.4, 6.4], [6.6, -6.2], [-1.0, -9.2], 30);
  const innerArc = cubic([-1.0, -9.2], [1.6, -4.4], [1.6, 4.2], [-1.6, 9.0], 30);
  return [...outerArc, ...innerArc.slice(1, -1)];
}
function crescentPainter(tell) {
  const sd = sdPoly(crescentShape());
  const inC = new Path(cubic([-.6, 6.8], [3.0, 4.2], [3.2, -4.0], [-.3, -7.0], 24));
  const G = new Grid(CARD.crescent, 12, plateH(sd, .7, grooveOf([inC], .32), .4));
  const r = CARD.crescent, px = (r.X1 - r.X0) / SIZE.crescent[0];
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    let c = shadeAt(M.navy, litAt(G, x, y, {k: 1.4}), d, px, {outline: 0});
    // lime C inlay along the inner curve, violet tips
    const n = inC.near(x, y);
    if (n.d < .3) c = mix(c, tell ? C('#F4FFC8') : P.inlay, .92 * smooth(.3, .16, n.d));
    const tipK = Math.max(smooth(5.5, 8.6, y), smooth(-5.6, -8.8, y));
    c = mix(c, P.violetTip, .7 * tipK);
    if (tell) c = mix(c, P.fxHi, .35);
    if (d > -px * 1.2) c = mix(c, M.navy.line, .85);
    else if (d > -px * 3) c = mix(c, P.navyRim, .4);
    return c;
  };
}
function shardPainter() {
  // the tail blade under the crescent: a long curved scimitar shard with a lime streak
  const b = sickle([.2, .8], 78, 10.0, .9, -.18);
  const sd = (x, y) => { const n = b.path.near(x, y); return n.d - b.w(n.t); };
  const G = new Grid(CARD.shard, 12, plateH(sd, .4));
  const r = CARD.shard, px = (r.X1 - r.X0) / SIZE.shard[0];
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    const n = b.path.near(x, y), s = n.s / Math.max(1e-6, b.w(n.t));
    let c = shadeAt(M.navy, litAt(G, x, y, {k: 1.5}), d, px);
    if (s > .1 && s < .4 && n.t > .1 && n.t < .7) c = mix(c, P.inlay, .85);
    c = mix(c, P.violetTip, .6 * smooth(.75, 1, n.t));
    return c;
  };
}
function diamondPainter() {
  const sd = sdPoly([[0, 2.5], [1.4, 0], [0, -2.5], [-1.4, 0]]);
  const G = new Grid(CARD.diamond, 16, plateH(sd, .6));
  return (u, v) => {
    const x = -1.6 + u * 3.2, y = 2.6 - v * 5.2, d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    let c = shadeAt(mat([[-.2, C('#141C30')], [.3, C('#1E2B44')], [.6, C('#2D4058')], [.85, C('#5A6E8C')], [1, C('#839E9E')]], C('#0A0E18')), litAt(G, x, y, {k: 1.4}), d, .1);
    if (Math.abs(x) < .1) c = mix(c, C('#839E9E'), .4);
    return c;
  };
}

// ---- torso, pelvis, legs (wrap textures of the turned limbs + cards) ---------------------------------------------
// Wrap textures: u = azimuth (0 = front, .25 = her left / outward, .5 = back, .75 = inward), v = down the limb.
def('skin', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [64, 64]);
def('thigh', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [64, 64]);
def('boot', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [64, 64]);
def('hoofw', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [32, 32]);
def('furw', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [64, 64]);
def('helmw', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [32, 32]);
const azShade = u => Math.pow(.5 + .5 * Math.cos((u - .1) * 2 * Math.PI), 1.4);   // lit toward the front-left
function skinTex() {
  const n = fbm(733);
  return (u, v) => {
    let c = mix(mix(P.skinShade, P.skinDeep, .35), P.skinHi, azShade(u));
    c = mix(c, P.skinLilac, .2 + .15 * n(u * 5, v * 5));
    const du = Math.min(Math.abs(u), Math.abs(u - 1));
    if (du < .035) c = mix(c, P.stripe, .9);                                 // lavender centre stripe
    // navy tribal swirls on the flanks
    for (const uc of [.25, .75]) {
      const a = (u - uc) * 14, b = (v - .55) * 6;
      const sw = Math.abs(Math.sin(Math.hypot(a, b) * 2.2 - Math.atan2(b, a) * 1.0));
      if (Math.hypot(a, b) < 2.2 && sw < .22) c = mix(c, P.swirl, .8);
    }
    return c;
  };
}
function thighTex() {
  const n = fbm(741);
  return (u, v) => {
    let c = mix(mix(P.skinShade, P.skinDeep, .35), P.skinHi, azShade(u));
    c = mix(c, P.skinLilac, .18);
    if (Math.abs(Math.sin(u * 18 + v * 2 + 3 * n(u * 4, v * 2))) < .08) c = mix(c, C('#8C9CB8'), .45);   // steel streaks
    if (Math.abs(u - .25) < .07 && v < .85) c = mix(c, mix(P.navy, P.navyMid, azShade(u)), .92);       // navy armour strip, outer thigh
    if (Math.abs(u - .25) < .085 && Math.abs(u - .25) > .07) c = mix(c, P.navyRim, .8);
    return c;
  };
}
function bootTex() {
  const n = fbm(751);
  return (u, v) => {
    let c = mix(mix(P.bootShade, P.bootDeep, .3), P.bootHi, azShade(u) * .7);
    c = mix(c, P.furLilac, .2 + .2 * n(u * 6, v * 3));
    const strand = Math.sin(u * 60 + 8 * n(u * 3, v * 4));
    c = mix(c, P.furShade, smooth(.8, 1, strand) * .35);
    if (Math.abs(u - .75) < .06) c = mix(c, P.bootBlue, .9);                 // vivid blue inner stripe
    else if (Math.abs(u - .75) < .1) c = mix(c, P.bootDeep, .6);
    return c;
  };
}
function hoofTex() { return (u, v) => mix(mix(P.hoofShade, P.claw, azShade(u)), P.hoofDeep, smooth(.6, 1, v) * .4); }
function helmTex() { return (u, v) => mix(P.helmShade, P.helm, azShade(u) * .7); }

def('boot_tuft', {X0: -2.8, X1: 2.8, Y0: -9.6, Y1: 1.0}, [64, 112]);   // shin fur (4 crossed cards)
def('boot_flare', {X0: -3.6, X1: 3.6, Y0: -8.6, Y1: 1.0}, [80, 96]);   // lower boot flaring to the ankle
def('knee', {X0: -2.4, X1: 3.6, Y0: -1.6, Y1: 4.2}, [64, 64]);         // white knee spikes with a lime one
def('hoof_claws', {X0: -2.0, X1: 2.0, Y0: -2.0, Y1: 1.0}, [48, 32]);   // cream hoof claws (front)
function bootTuft() {
  const t = furRows(811, {x0: -1.6, x1: 1.6, top: () => .2, bot: () => -5.8, L: 3.2, Lb: 3.8, w: 1.15, dx: 1.1, dy: 1.4, fan: 5, spread: 16, fringe: false})
    .filter(f => Math.abs(f.r[0]) < .7 + .15 * (-f.r[1]));                // narrow at the knee, wider toward the hock
  t.forEach(f => { if (Math.abs(f.r[0]) < .7) f.tip = P.bootBlue; else f.shade = .25; });
  return furPainter(CARD.boot_tuft, t, {tipK: .45});
}
function bootFlare() {
  const t = furRows(823, {x0: -2.2, x1: 2.2, top: () => .2, bot: () => -4.4, L: 3.0, Lb: 4.4, w: 1.4, dx: 1.15, dy: 1.4, fan: 12, spread: 18, fringe: false})
    .filter(f => Math.abs(f.r[0]) < 1.1 + .3 * (-f.r[1]));
  t.forEach(f => { f.shade = .3; if (f.last) f.shade = .05; if (Math.abs(f.r[0]) < .6 && !f.last) f.tip = P.bootBlue; });
  return furPainter(CARD.boot_flare, t, {tipK: .5});
}
function kneeSpikes() {
  const list = [{r: [0, 0], a: 160, L: 3.6, w: 1.0}, {r: [.8, 0], a: 140, L: 3.2, w: .9}, {r: [1.6, -.2], a: 120, L: 2.6, w: .8}, {r: [-.6, .1], a: 175, L: 2.6, w: .8}];
  const fur = furPainter(CARD.knee, list);
  const lime = sdTaper([[.4, .4], [1.4, 2.4], [2.6, 3.8]], .32, .03);
  const r = CARD.knee;
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = lime(x, y);
    if (d < 0) return mix(P.fxLime, P.ribHi, smooth(-.02, -.2, d));
    return fur(u, v);
  };
}
function hoofClaws() {
  // 3 large ivory claws splayed forward (seen from the front)
  const cl = [[-1.2, -.2, -12], [0, 0, 0], [1.2, -.2, 12]].map(([x, y, a]) => sdTaper([[x, .8], [x + Math.sin(a * Math.PI / 180) * 1.2, y - 1.0], [x + Math.sin(a * Math.PI / 180) * 1.6, y - 1.8]], .55, .06, .8));
  const sd = sdUnion(...cl);
  const G = new Grid(CARD.hoof_claws, 16, plateH(sd, .4));
  const r = CARD.hoof_claws, px = (r.X1 - r.X0) / SIZE.hoof_claws[0];
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    return shadeAt(M.hoof, litAt(G, x, y, {k: 1.4}), d, px);
  };
}
def('hipplate', {X0: -.6, X1: 4.0, Y0: -4.4, Y1: 1.0}, [48, 64]);      // navy hip plate with a lime swirl (her left)
def('fin', {X0: -.4, X1: 2.6, Y0: -3.2, Y1: .8}, [32, 48]);             // small steel hip fin
function hipPlate() {
  const sd = sdSmooth([[0, .6], [2.4, .2], [3.6, -1.6], [2.8, -4.0], [1.4, -2.6], [.2, -1.4]]);
  const sp = new Path(spiralPts(1.9, -1.2, .15, .8, 1.3, 90, 1));
  const G = new Grid(CARD.hipplate, 16, plateH(sd, .45));
  const r = CARD.hipplate, px = (r.X1 - r.X0) / SIZE.hipplate[0];
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    let c = shadeAt(M.navy, litAt(G, x, y, {k: 1.4}), d, px);
    if (sp.near(x, y).d < .16) c = mix(c, P.inlay, .9);
    return c;
  };
}
function finPainter() {
  const sd = sdTaper([[.2, .6], [1.0, -1.0], [2.2, -2.9]], .5, .04, .9);
  const G = new Grid(CARD.fin, 16, plateH(sd, .3));
  return (u, v) => {
    const x = -.4 + u * 3.0, y = .8 - v * 4.0, d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    return shadeAt(M.steel, litAt(G, x, y, {k: 1.4}), d, .07);
  };
}

// ---- ribbon tendrils (her left; the upper one scale 1, the lower one 1.25) ---------------------------------------
def('tu', {X0: -3.4, X1: 12.6, Y0: -12.2, Y1: 3.8}, [128, 128]);
def('tl', {X0: -4.0, X1: 8.0, Y0: -20.6, Y1: 1.4}, [80, 144]);
def('tuf', {X0: -3.4, X1: 12.6, Y0: -12.2, Y1: 3.8}, [64, 64]);
def('tlf', {X0: -4.0, X1: 8.0, Y0: -20.6, Y1: 1.4}, [48, 80]);
// spiral "eye" curl at the hip (0, 0) whose outer turn leaves as the ribbon toward the end point (9.6, -9.4)
const TU_PATH = () => {
  const sp = spiralPts(0, 0, .55, 2.4, 1.15, 200, 1, 40);
  const tail = spline([sp[sp.length - 1], [3.2, -1.6], [5.0, -4.6], [7.2, -7.2], [9.6, -9.4]], 10);
  return new Path([...sp, ...tail.slice(1)]);
};
const TL_PATH = () => new Path(spline([[0, 0], [1.6, -3.4], [1.0, -7.2], [-1.0, -10.6], [-.4, -14.4], [1.8, -17.2], [3.6, -19.6]], 10));
function ribbonPainter(rect, size, pth, w, look, {eye = false} = {}) {
  const sd = (x, y) => { const n = pth.near(x, y); return n.d - w(n.t); };
  const G = new Grid(rect, 12, plateH(sd, .5));
  const px = (rect.X1 - rect.X0) / size[0];
  const pyro = look === 'pyro', flat = look === 'flat';
  const m = pyro ? mat([[-.2, C('#6D3A4A')], [.25, C('#A35D83')], [.48, C('#C96839')], [.64, C('#F2B076')], [.86, C('#FAD77C')], [1, C('#FCE2CF')]], C('#5A2A2A'), white, .4) : M.rib;
  return (u, v) => {
    const x = rect.X0 + u * (rect.X1 - rect.X0), y = rect.Y1 - v * (rect.Y1 - rect.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    if (flat) return d > -px * 1.2 ? P.fxShade : P.fxLime;
    const n = pth.near(x, y), L = litAt(G, x, y, {k: 1.3});
    let c = shadeAt(m, L, d, px, {outline: 0});
    // teal underside on the lower edge of the ribbon (Dendro), magenta in Pyro
    if (n.s < 0) c = mix(c, pyro ? C('#A35D83') : P.ribTeal, .35 * smooth(0, -w(n.t), n.s));
    if (eye && n.t < .42) c = mix(c, P.spiralNavy, .0);
    if (d > -px * 1.2) c = mix(c, pyro ? C('#5A2A2A') : C('#2C5A3C'), .85);
    return c;
  };
}
function tendrilUp(look) {
  const pth = TU_PATH(), L = pth.L;
  const w = t => (t < .42 ? .6 + .6 * t / .42 : 1.2 - .45 * (t - .42) / .58);
  const base = ribbonPainter(CARD.tu, SIZE[look === 'flat' ? 'tuf' : 'tu'], pth, w, look, {eye: true});
  const r = CARD.tu;
  // the navy spiral core of the eye
  return (u, v) => {
    const c = base(u, v);
    if (c[3]) return c;
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), rr = Math.hypot(x, y);
    if (rr < 1.15 && look !== 'flat') return mix(P.spiralNavy, C('#2E3E7A'), smooth(1.15, .3, rr));
    return TRANSPARENT;
  };
}
function tendrilLo(look) {
  const pth = TL_PATH();
  return ribbonPainter(CARD.tl, SIZE[look === 'flat' ? 'tlf' : 'tl'], pth, t => 1.35 * (1 - Math.pow(t, 1.5) * .97), look);
}

// ---- chest core glow and the props --------------------------------------------------------------------------------
def('core', {X0: -4, X1: 4, Y0: -4, Y1: 4}, [64, 64]);
function corePainter() {
  return (u, v) => {
    const r = Math.hypot(u - .5, v - .5) * 2;
    if (r > 1) return TRANSPARENT;
    const c = mix(C('#FFFFF4'), P.fxHi, smooth(0, .6, r));
    return [c[0], c[1], c[2], Math.round(255 * Math.pow(1 - r, 1.6) * .95)];
  };
}
// Entrance cocoon (scale 3, 1 u = 0.1875 b; 3.8 b tall): a vertical lozenge of wrapped dark slate-green wing
// plates, curled hooks at the upper corners (the forewing hooks meeting at the top), lime leading edges, a glowing
// lime core window and a lime crystal spike pointing down (v1 f120-150, sheet 08 H).
def('cocoon', {X0: -5.2, X1: 5.2, Y0: -10.8, Y1: 10.6}, [112, 224]);
function cocoonPainter() {
  // kite outline: widest high up under two inward-curling horn hooks, a notch between them, tapering to the spike
  const shell = sdSmooth([[0, 6.6], [1.6, 7.6], [3.6, 7.4], [4.6, 5.6], [4.3, 2.6], [3.3, -1.6], [2.0, -5.2], [.8, -7.6], [0, -8.2], [-.8, -7.6], [-2.0, -5.2], [-3.3, -1.6], [-4.3, 2.6], [-4.6, 5.6], [-3.6, 7.4], [-1.6, 7.6]]);
  const hooks = sdUnion(sdTaper([[3.6, 6.4], [4.6, 8.4], [3.6, 9.8], [2.2, 9.6], [1.9, 8.6], [2.6, 8.2]], .75, .14, .9),
    sdTaper([[-3.6, 6.4], [-4.6, 8.4], [-3.6, 9.8], [-2.2, 9.6], [-1.9, 8.6], [-2.6, 8.2]], .75, .14, .9));
  const spike = sdPoly([[-1.0, -7.4], [0, -10.6], [1.0, -7.4]]);
  const win = sdSmooth([[0, 6.0], [1.7, 3.0], [1.4, -1.4], [0, -5.0], [-1.4, -1.4], [-1.7, 3.0]]);
  // two folded wing plates crossing low down (an X of seams), lime leading edges along them
  const seamL = new Path(spline([[-4.3, 4.6], [-2.2, 1.0], [.4, -3.6], [1.6, -6.6]], 8)), seamR = new Path(spline([[4.3, 4.6], [2.2, 1.0], [-.4, -3.6], [-1.6, -6.6]], 8));
  const seams = grooveOf([seamL, seamR, spline([[-3.8, 6.8], [-2.4, 5.0], [-1.9, 3.0]], 6), spline([[3.8, 6.8], [2.4, 5.0], [1.9, 3.0]], 6)], .34);
  const sd = sdUnion(shell, hooks, spike);
  const G = new Grid(CARD.cocoon, 10, (x, y) => Math.max(plateH(shell, 1.8, seams, .55)(x, y), plateH(hooks, .45)(x, y)));
  const r = CARD.cocoon, px = (r.X1 - r.X0) / SIZE.cocoon[0];
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    if (spike(x, y) < 0) return mix(P.cocoonSpike, C('#F1FCC3'), smooth(.5, -.1, Math.abs(x)) * .8);
    const dw = win(x, y);
    if (dw < 0) {
      // the glowing lime core window: a hot white-lime centre line, facets
      const k = smooth(0, -1.3, dw);
      return mix(mix(P.cocoonWin, P.cocoonWinHi, k), C('#F4FFD0'), smooth(.5, 0, Math.abs(x)) * k * .8);
    }
    const L = litAt(G, x, y, {k: 1.0});
    let c = shadeAt(hooks(x, y) < 0 ? M.navy : M.cocoon, L, d, px, {outline: 0});
    // lime leading edges on the seam ridges and round the window
    const sm = Math.min(seamL.near(x, y).d, seamR.near(x, y).d);
    if (sm < .16 && hooks(x, y) > 0) c = mix(c, P.fxLime, .85);
    if (dw < .5) c = mix(c, P.fxLime, .8 * smooth(.5, .15, dw));
    if (d > -px * 1.2) c = mix(c, C('#0E1614'), .85);
    return c;
  };
}
def('cocoon_glow', {X0: -3.0, X1: 3.0, Y0: -7.0, Y1: 8.0}, [48, 112]);
function cocoonGlow() {
  return (u, v) => {
    const x = (u - .5) * 2, y = (.5 - v) * 2, r = Math.hypot(x / .55, y);
    if (r > 1) return TRANSPARENT;
    const c = mix(C('#FBFFE8'), P.fxLime, smooth(0, .8, r));
    return [c[0], c[1], c[2], Math.round(255 * .7 * Math.pow(1 - r, 1.2))];
  };
}
// Wrapped pod (B4/B5, scale 2.5, 1 u = 0.156 b): panels of the folded wings closing round her, lime wing plates with
// navy frames outside and lime light leaking from the seams (v4 f440, v3 f1314).
def('pod', {X0: -4.6, X1: 4.6, Y0: -11.2, Y1: 11.2}, [80, 192]);
function podPainter() {
  // one leaf-shaped wing panel (pointed top and bottom): lime scroll frame with navy frame lines, a white-mint
  // iridescent lobe, a hot lime seam glow along its edges (light leaking between the panels)
  const shell = sdSmooth([[0, 10.8], [2.2, 8.4], [3.8, 3.6], [4.2, -1.2], [3.4, -6.2], [1.8, -9.4], [0, -10.8], [-1.8, -9.4], [-3.4, -6.2], [-4.2, -1.2], [-3.8, 3.6], [-2.2, 8.4]]);
  const lobe = sdSmooth([[-.6, 6.6], [1.8, 5.0], [2.4, 1.4], [1.2, -2.6], [-1.0, -1.6], [-1.8, 1.8], [-1.6, 4.8]]);
  const frames = grooveOf([spline([[0, 10.4], [-2.6, 6.0], [-3.0, 0], [-2.0, -6.0], [0, -10.4]], 8), spiralPts(1.2, -6.0, .2, 1.4, 1.2, 60, 1)], .32);
  const G = new Grid(CARD.pod, 10, (x, y) => plateH(shell, 1.2)(x, y) + .45 * frames(x, y) - (lobe(x, y) < 0 ? .3 : 0));
  const r = CARD.pod, px = (r.X1 - r.X0) / SIZE.pod[0];
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = shell(x, y);
    if (d > 0) return TRANSPARENT;
    const dl = lobe(x, y);
    if (dl < 0) return membrane('dendro', x * 1.5 + 9, y * 1.1 + 6, dl, 2.4);
    const L = litAt(G, x, y, {k: 1.0});
    let c = frames(x, y) > .5 ? shadeAt(M.navy, L, d, px, {outline: 0}) : shadeAt(M.lime, L, d, px, {outline: 0});
    if (dl < .4) c = mix(c, C('#4A3C6A'), .5 * smooth(.4, 0, dl));
    if (d > -px * 2.5) c = mix(c, P.fxCore, .85);                          // lime light leaking at the seams
    return c;
  };
}
// Orb (B4): a translucent lime glass sphere (wrap texture of a turned sphere) with bright rim; gyroscope ring.
def('orb', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [64, 64]);
def('ring', {X0: -8, X1: 8, Y0: -8, Y1: 8}, [128, 128]);
def('ringw', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [64, 16]);
function orbTex() {
  const n = fbm(907);
  return (u, v) => {
    const lat = Math.abs(v - .5) * 2;                                    // 0 at the equator .. 1 at the poles
    const sw = Math.sin(u * 25 + v * 9 + 4 * n(u * 4, v * 4));
    let c = mix(C('#D2FA8E'), C('#9CDB7D'), lat * .6);
    c = mix(c, C('#F4FFD8'), smooth(.6, 1, sw) * .6);
    return [c[0], c[1], c[2], Math.round(255 * (.42 + .3 * lat + .15 * smooth(.6, 1, sw)))];
  };
}
function ringPainter() {
  return (u, v) => {
    const r = Math.hypot(u - .5, v - .5) * 2;
    const d = Math.abs(r - .9);
    if (d > .07) return TRANSPARENT;
    const c = mix(C('#F2FFDC'), C('#ADE87F'), smooth(0, .07, d));
    return [c[0], c[1], c[2], Math.round(255 * (1 - smooth(.03, .07, d)) * .95)];
  };
}
function ringBandTex() {
  return (u, v) => { const c = mix(C('#F2FFDC'), C('#ADE87F'), Math.abs(v - .5) * 2); return [c[0], c[1], c[2], Math.round(255 * .85 * (1 - Math.abs(v - .5) * 1.2))]; };
}

// Widen every card rect to its pixel aspect (square texels); wrap textures (0..1) are left alone.
for (const [k, r] of Object.entries(CARD)) {
  if (r.X0 === 0 && r.X1 === 1) continue;
  const [w, h] = SIZE[k], ppu = Math.min(w / (r.X1 - r.X0), h / (r.Y1 - r.Y0));
  const cx = (r.X0 + r.X1) / 2, cy = (r.Y0 + r.Y1) / 2, hw = w / ppu / 2, hh = h / ppu / 2;
  CARD[k] = {X0: cx - hw, X1: cx + hw, Y0: cy - hh, Y1: cy + hh};
}

// =================================================================================================================
// Sprite table and writer
// =================================================================================================================
// name -> [w, h, painter, translucent, mcmeta]
export function butterflySprites() {
  const out = {};
  const add = (name, base, painter, translucent = false, meta) => { out[name] = [...SIZE[base], painter, translucent, meta]; };
  for (const look of ['dendro', 'pyro']) {
    add('fw_' + look, 'fw', fwPainter(look));
    const [w, h] = SIZE.fwg;
    out['fwg_' + look] = [w, h * FW_FRAMES, strip(w, h, FW_FRAMES, f => fwgPainter(look, f)), true, {animation: {frametime: 4, interpolate: true}}];
    add('hw_' + look, 'hw', hwPainter(look));
  }
  add('fw_flat', 'fwf', fwPainter('flat'));
  add('fwg_flat', 'fwg', fwgFlatPainter(), true);
  add('hw_flat', 'hwf', hwPainter('flat'));
  for (const look of ['dendro', 'pyro']) { add('tu_' + look, 'tu', tendrilUp(look)); add('tl_' + look, 'tl', tendrilLo(look)); }
  add('tu_flat', 'tuf', tendrilUp('flat')); add('tl_flat', 'tlf', tendrilLo('flat'));
  add('mane_f', 'mane_f', maneFront()); add('mane_fs', 'mane_fs', maneCorner(317, false)); add('mane_s', 'mane_s', maneSide());
  add('mane_bs', 'mane_bs', maneCorner(337, true)); add('mane_b', 'mane_b', maneBack());
  add('helm', 'helm', helmPainter()); add('cheek', 'cheek', cheekPainter()); add('crown', 'crown', crownPainter()); add('helm_side', 'helm_side', helmSidePainter());
  add('eye', 'eye', eyePainter()); add('chev', 'chev', chevPainter());
  add('antenna', 'antenna', antennaPainter()); add('streamer', 'streamer', streamerPainter());
  add('fan', 'fan', bladePainter(CARD.fan, SIZE.fan, FAN_BLADES())); add('fanb', 'fanb', bladePainter(CARD.fanb, SIZE.fanb, FANB_BLADES())); add('shplate', 'shplate', shplatePainter());
  add('crescent', 'crescent', crescentPainter(false)); add('crescent_tell', 'crescent_tell', crescentPainter(true)); add('shard', 'shard', shardPainter()); add('diamond', 'diamond', diamondPainter());
  add('skin', 'skin', skinTex()); add('thigh', 'thigh', thighTex()); add('boot', 'boot', bootTex()); add('hoofw', 'hoofw', hoofTex());
  add('furw', 'furw', furTile(941)); add('helmw', 'helmw', helmTex());
  add('boot_tuft', 'boot_tuft', bootTuft()); add('boot_flare', 'boot_flare', bootFlare()); add('knee', 'knee', kneeSpikes()); add('hoof_claws', 'hoof_claws', hoofClaws());
  add('hipplate', 'hipplate', hipPlate()); add('fin', 'fin', finPainter());
  add('core', 'core', corePainter(), true);
  add('cocoon', 'cocoon', cocoonPainter()); add('cocoon_glow', 'cocoon_glow', cocoonGlow(), true); add('pod', 'pod', podPainter());
  add('orb', 'orb', orbTex(), true); add('ring', 'ring', ringPainter(), true); add('ringw', 'ringw', ringBandTex(), true);
  return out;
}
export const spriteId = name => 'rlk:mboss/butterfly/' + name;
// sprite name -> card rect (looks share their base rect)
export const cardOf = name => CARD[name] || CARD[name.replace(/_(dendro|pyro|flat)$/, '')] || CARD[name.split('_')[0]];
export function paintButterflyTextures(rp, only = null) {
  return paintSpriteSet(rp, 'assets/rlk/textures/mboss/butterfly', butterflySprites(), spriteId, only);
}
export {P as BF_PAL};
