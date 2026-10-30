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
import {LEG_LEN} from './butterfly_pose.mjs';

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
  // the blade: a sickle whose back bulges up and whose point (kept at the FX anchor 22.6, -4.5) bends down (PDF)
  const bladeTop = [[8.0, 1.6], [11.4, .7], [14.6, -.3], [17.6, -1.3], [20.3, -2.7], [22.6, -4.5]];
  const bladeBot = [[22.6, -4.5], [20.2, -4.6], [17.2, -4.4], [14.2, -3.9], [11.0, -3.2], [8.0, -2.6]];
  const bl = [...spline(bladeTop, 8), ...spline(bladeBot, 8).slice(1)];
  const sdBlade = sdPoly(bl);
  const spine = new Path(spline([[8.0, -.5], [11.3, -1.25], [14.6, -2.1], [17.6, -2.9], [20.4, -3.7], [22.6, -4.5]], 8));
  // the glow flaring round the point: an opaque light-blue aura just past the blade (the card is cut out, so the
  // haze is painted as a soft-coloured fringe that reads as light)
  const flare = sdTaper([[18.6, -3.4], [20.6, -4.0], [22.4, -4.5], [23.3, -4.8]], .55, .3, 1);
  const sdEye = sdCircle(4.0, .25, 2.05);
  // the volute: a raised spiral tube (the grooves between its turns are the dark navy gaps), flourishes
  const volute = grooveOf([spiralPts(4.0, .25, .35, 2.0, 1.55, 80, 1)], .4);
  const grooves = grooveOf([spline([[1.0, 3.2], [2.6, 2.2], [5.6, 2.4], [8.6, 1.4]], 8), spline([[1.6, -1.6], [3.6, -2.4], [6.6, -2.2], [9.6, -1.5]], 8)], .22);
  const sil = sdUnion(sdLobe, sdBlade, flare);
  return {sdLobe, sdBlade, spine, sdEye, volute, grooves, sil, flare};
})();
let HWG = null;
function hwGrids() {
  if (HWG) return HWG;
  const r = CARD.hw, res = 14;
  HWG = {
    h: new Grid(r, res, (x, y) => Math.max(plateH(HW.sdLobe, .75, HW.grooves, .5)(x, y) + (HW.sdEye(x, y) < 0 ? .55 * HW.volute(x, y) - .35 : 0), .9 * plateH(HW.sdBlade, .5)(x, y))),
    sil: new Grid(r, res, HW.sil), lobe: new Grid(r, res, HW.sdLobe), blade: new Grid(r, res, HW.sdBlade), eye: new Grid(r, res, HW.sdEye), flare: new Grid(r, res, HW.flare),
  };
  return HWG;
}
function hwPainter(look) {
  const G = hwGrids(), r = CARD.hw, px = (r.X1 - r.X0) / SIZE[look === 'flat' ? 'hwf' : 'hw'][0];
  // the point glows: lime -> sky -> ice -> white-hot, ringed in saturated blue (Pyro: orange -> rose -> peach-white)
  const tipRamp = ramp([[0, '#A4BD6A'], [.28, '#8EC6EE'], [.5, '#C1DFFA'], [.75, '#E8F3FF'], [1, '#FFFFFF']]);
  const tipPyro = ramp([[0, '#F2B076'], [.3, '#E59A62'], [.55, '#F2A0A8'], [.8, '#FCE2CF'], [1, '#FFF8EE']]);
  const rimTip = look === 'pyro' ? C('#C0485A') : C('#2F57D8'), aura = look === 'pyro' ? C('#F6B2B0') : C('#9DC2FA');
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0);
    const ds = G.sil.at(x, y);
    if (ds > 0) return TRANSPARENT;
    const dLobe = G.lobe.at(x, y), dB = G.blade.at(x, y);
    if (look === 'flat') {
      let c = mix(P.fxLime, P.fxHi, smooth(14, 22, x));
      if (ds > -px * 1.2) c = mix(c, P.fxShade, .8);
      return c;
    }
    if (dLobe > 0 && dB > 0) {
      // the aura round the point: pale blue fading to a deeper blue at its rim
      const k = smooth(0, .5, -G.flare.at(x, y));
      let c = mix(mix(aura, rimTip, .55), mix(aura, C('#FFFFFF'), .5), k);
      if (ds > -px * 1.2) c = mix(c, rimTip, .7);
      return c;
    }
    const L = litAt(G.h, x, y, {k: 1.2});
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
      // blade: lime upper half, iridescent lower half with a violet-pink edge glow, the glowing point
      const n = HW.spine.near(x, y), t = n.t;
      c = shadeAt(M.lime, L, ds, px, {outline: 0});
      if (n.s < .15) {
        const k = clamp(((x * .1 + y * .24 + 10) % 1 + 1) % 1);
        c = mix(c, (look === 'pyro' ? RAMP.pyro : RAMP.holo)(k), .82 * smooth(.15, -.25, n.s));
        c = mix(c, look === 'pyro' ? C('#F9D0B2') : C('#F0F6FF'), .3 * Math.pow(Math.max(0, L.diff - .5) * 2, 2));
        if (dB > -.35) c = mix(c, look === 'pyro' ? C('#C680A2') : C('#C9A8F4'), .7);
      }
      const tip = smooth(.58, 1, t);
      if (tip > 0) c = mix(c, (look === 'pyro' ? tipPyro : tipRamp)(tip), smooth(0, .2, tip));
      if (tip > .2 && dB > -.28) c = mix(c, rimTip, .75);
    }
    if (ds > -px * 1.2) c = mix(c, x > 19 ? rimTip : M.lime.line, .85);
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
// pal: the clump colours (default the mane's cool white); fit false keeps tufts that leave the card (wrap textures,
// whose tufts repeat across the seam); light(x, y) -> 0..1 darkens the clump colour toward pal.deep (wrap shading).
const FUR_PAL = {shade: P.furShade, base: P.fur, hi: P.furHi, lilac: P.furLilac, edge: C('#B2BFD4')};
function furPainter(rect, tufts, {px = .08, shadow = .9, tipK = .55, pal = FUR_PAL, fit = true, light = null, deep = null} = {}) {
  const grain = fbm(977);
  // keep every tuft inside the card (a tuft cut by the card edge shows as a straight line): shorten it until its
  // tip and its sides fit, with a small margin
  const m = .25;
  if (fit) for (const t of tufts) {
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
      let c = mix(pal.shade, pal.base, clamp(.5 + .8 * e));
      c = mix(c, pal.hi, clamp((e - .5) * 1.6) * (.45 + .55 * h.t));
      c = mix(c, pal.lilac, (1 - h.t) * .15);
      // strands along the clump
      const st = Math.sin(h.s * 9 + h.t * 3 + 6 * grain(x * .6, y * .6));
      c = mix(c, pal.shade, smooth(.75, 1, st) * .15 * (1 - h.t * .5));
      if (t.tip) c = mix(c, t.tip, Math.min(1, tipK * smooth(.4, .85, h.t) * (.7 + .3 * e)));
      if (t.shade) c = mix(c, pal.lilac, t.shade);
      if (light) c = mix(c, deep || pal.lilac, 1 - light(x, y));
      // a soft light edge so the clumps separate without outlines (soft fur, not shingles)
      if (h.edge < px * 1.1) c = mix(c, pal.edge, .45);
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
        if (g) { c = mix(c, pal.lilac, .2 * clamp(1 + g.edge / shadow)); break; }
      }
      return c;
    }
    return null;
  });
}
// Rows of tufts filling an envelope: top(x) / bot(x) bound the roots; tufts hang down (fanned by `fan` deg per
// unit of x), the bottom row longer; an upper fringe of short tufts points up so the top edge is fluffy too.
function furRows(seed, {x0, x1, top, bot, L = 3, Lb = 4.6, w = 1.25, dx = 1.15, dy = 1.25, fan = 2.5, fringe = true, tip = null, tipRows = 0, spread = 14, noFringe = null}) {
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
    for (let x = x0 + .3; x <= x1; x += dx * 1.1) {
      const t = {r: [x, top(x) - .5], a: 180 + x * fan * .6 + (R2() - .5) * 40, L: 1.3 + R2() * .9, w: w * .7};
      if (!noFringe || !noFringe(x)) out.unshift(t);
    }
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
  // the dip under the chin stays below the beak tip (2.35 b) so the whole mask shows above the ruff, also seen
  // from below up close; no upright fringe in the dip
  const top = x => { const a = Math.abs(x); return -.9 + 6.0 * smooth(2.2, 6.0, a) - 4.2 * smooth(6.6, 10.8, a) * smooth(6.6, 10.8, a); };
  const bot = x => -4.6 + 3.6 * smooth(0, 9.5, Math.abs(x));        // a V of chest tufts, lowest in the middle
  return furPainter(CARD.mane_f, furRows(311, {x0: -10.0, x1: 10.0, top, bot, L: 3.6, Lb: 4.8, w: 1.9, dx: 1.55, dy: 1.45, fan: 3.6, spread: 18, noFringe: x => Math.abs(x) < 2.8}));
}
function maneCorner(seed, back) {
  // a rounded clump of fur (dome on top, rounded tufted bottom), not a rectangle
  // the front corners slope down on their inner side (x < 0, toward the chin), so they never hide the mask from a
  // three-quarter view or from below
  const dip = x => (back ? 0 : 3.6 * smooth(.6, -3.8, x));
  const top = x => 3.9 - 3.2 * (x / 4.6) ** 2 - dip(x), bot = x => (back ? -3.4 : -2.2) - .25 * x + 2.6 * (x / 4.6) ** 4 - .5 * dip(x);
  return furPainter(CARD[back ? 'mane_bs' : 'mane_fs'], furRows(seed, {x0: -4.3, x1: 4.3, top, bot, L: 3.4, Lb: back ? 4.4 : 4.0, w: 1.85, dx: 1.5, dy: 1.45, fan: 2.4, spread: 18,
    tip: back ? capeTip : null, tipRows: back ? 3 : 0, noFringe: back ? null : x => x < -1.2}), {tipK: 1});
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

// ---- torso, pelvis, legs (smooth turned solids under wrap textures, fur cards) ------------------------------------
// BODY holds the radius profiles (model units at scale 1; a = position along the part's axis, 0 at its pivot joint,
// limbs hang along -a; r = the radius across, kz = depth / width of the elliptic sections). butterfly_geometry.mjs
// turns them (smooth rings, no ledge discs); the fur cards below are painted on the same profiles. Wrap textures:
// u = azimuth (0 front, .25 her left / the outside of her left leg, .5 back, .75 inward), v from the top of the part
// (a1) to its bottom (a0). Their light is painted (the facets are unshaded): lit from the front, a soft falloff to
// the sides, the back in lilac shade, so neighbouring rings and parts meet without seams.
const TH = LEG_LEN.thigh * 16, SH = LEG_LEN.shin * 16, FT = LEG_LEN.foot * 16;
// Monotone cubic through control points [[a, r], ...] (ascending a), flat outside them.
export function profile(pts) {
  const n = pts.length, d = [];
  for (let i = 0; i < n - 1; i++) d.push((pts[i + 1][1] - pts[i][1]) / (pts[i + 1][0] - pts[i][0]));
  const m = pts.map((_, i) => (i === 0 ? d[0] : i === n - 1 ? d[n - 2] : d[i - 1] * d[i] <= 0 ? 0 : 2 / (1 / d[i - 1] + 1 / d[i])));
  return a => {
    if (a <= pts[0][0]) return pts[0][1];
    if (a >= pts[n - 1][0]) return pts[n - 1][1];
    let i = 0;
    while (a > pts[i + 1][0]) i++;
    const [x0, y0] = pts[i], [x1, y1] = pts[i + 1], hh = x1 - x0, t = (a - x0) / hh, t2 = t * t, t3 = t2 * t;
    return (2 * t3 - 3 * t2 + 1) * y0 + (t3 - 2 * t2 + t) * hh * m[i] + (-2 * t3 + 3 * t2) * y1 + (t3 - t2) * hh * m[i + 1];
  };
}
export const BODY = {
  // waist 0.42 b at 1.61 b, the chest ending inside the mane (2.06 b, behind the front ruff and below the face);
  // its lower end sits inside the pelvis
  torso: {a: [-3.8, 7.2], kz: .76, pts: [[-3.8, 3.6], [-2.2, 3.48], [-.3, 3.38], [1.5, 3.42], [3.5, 3.8], [5.6, 4.22], [7.2, 4.3]]},
  // hips (0.57 b) flaring out of the waist at 1.50 b (the two profiles cross there, so each part's open end stays
  // inside the other however the torso leans) and rounding into the crotch (1.18 b) between the thigh tops
  pelvis: {a: [-4.0, 3.6], kz: .75, pts: [[-4.0, .35], [-3.6, 1.0], [-3.0, 1.75], [-2.2, 2.6], [-1.3, 3.35], [-.4, 3.9], [.6, 4.15], [1.6, 4.0], [2.6, 3.62], [3.6, 3.25]]},
  // thigh: wide at the hip, slim at the knee, a rounded knee end (it turns inside the boot cuff)
  thigh: {a: [-TH - 1.2, 1.6], pts: [[-TH - 1.2, .3], [-TH - .95, .82], [-TH - .45, 1.08], [-TH + .4, 1.17], [-TH * .72, 1.33], [-TH * .42, 1.58], [-TH * .12, 1.8], [.5, 1.86], [1.6, 1.7]]},
  // fur boot: from a cuff over the knee, flaring toward the hock; it reaches on into the foot's boot
  shin: {a: [-SH - 1.5, .2], pts: [[-SH - 1.5, 2.3], [-SH, 2.26], [-SH * .7, 2.02], [-SH * .4, 1.8], [-SH * .1, 1.66], [.2, 1.6]]},
  // lower boot: widest at the ankle cuff (0.37 b with the fur), closing over the hoof
  foot: {a: [-5.0, 1.0], pts: [[-5.0, 1.75], [-4.6, 2.55], [-3.7, 2.95], [-2.4, 2.86], [-1.0, 2.56], [0, 2.4], [1.0, 2.3]]},
  // cream hoof: a blunt cone pointing along the foot (down and forward), its top inside the boot
  hoof: {a: [-FT - .15, -3.9], pts: [[-FT - .15, .3], [-FT + .25, .82], [-FT + 1.0, 1.28], [-FT + 2.1, 1.62], [-3.9, 1.78]]},
};
for (const b of Object.values(BODY)) b.r = profile(b.pts);
const azL = (u, k = 1) => Math.pow(.5 + .5 * Math.cos(u * 2 * Math.PI), k);       // front-lit
const wrapD = (a, b) => { const d = ((a - b) % 1 + 1) % 1; return Math.min(d, 1 - d); };
// Polar sprite (end caps): col(azimuth 0..1 like the wraps' u, radius 0..1).
const polarSprite = col => (u, v) => {
  const r = Math.hypot(u - .5, v - .5) * 2;
  return r > 1 ? TRANSPARENT : col(((Math.atan2(u - .5, v - .5) / (2 * Math.PI)) + 1) % 1, r);
};
def('torso_w', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [128, 128]);
def('pelvis_w', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [128, 64]);
def('pelvis_w_cap', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [32, 32]);
def('thigh_w', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [128, 64]);
def('thigh_w_cap', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [16, 16]);
def('boot_s', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [128, 128]);
def('boot_s_cap', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [32, 32]);
def('boot_f', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [128, 48]);
def('boot_f_cap', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [32, 32]);
def('hoof_w', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [64, 32]);
def('hoof_w_cap', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [16, 16]);
def('furw', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [64, 64]);
def('helmw', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [64, 32]);
def('antw', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [16, 16]);
def('helmw_cap', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [16, 16]);
def('furw_cap', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [32, 32]);
const SKIN = {
  base: t => mix(mix(P.skinLilac, P.skinShade, .55), P.skinHi, t),   // t = painted light 0..1
};
// a tribal swirl stroke field in (x, y) units: an open spiral curling into a tail
function swirlField(cx, cy, r0, r1, turns, a0, dir, tail) {
  const paths = [spiralPts(cx, cy, r0, r1, turns, a0, dir, 48)];
  if (tail) paths.push(spline(tail, 8));
  const P2 = paths.map(p => new Path(p));
  return (x, y) => Math.min(...P2.map(p => p.near(x, y).d));
}
// Torso and pelvis share one painter keyed to the height above the floor (y, blocks at rest), so the lavender belly
// band, the light and the shading run on unbroken where the hips flare out of the waist.
function skinAt(n) {
  return (u, y, sw) => {
    const du = wrapD(u, 0), db = wrapD(u, .5);
    let c = SKIN.base(.25 + .75 * azL(u, .8));
    c = mix(c, P.skinLilac, .1 + .14 * n(u * 7, y * 9));
    // the belly: a soft lavender band down the front, widening toward the crotch, a finer darker centre
    const bw = .03 + .03 * smooth(1.85, 1.3, y), fade = smooth(2.06, 1.88, y);
    c = mix(c, C('#B3BDEA'), .6 * smooth(bw * 1.9, bw * .7, du) * fade);
    c = mix(c, P.stripe, .75 * smooth(bw * .75, bw * .3, du) * smooth(2.0, 1.86, y));
    // the chest under the mane in its shadow; the crotch and the seat underneath in shade; the spine darker
    c = mix(c, P.furLilac, .45 * smooth(1.9, 2.06, y));
    c = mix(c, P.skinShade, .45 * smooth(1.28, 1.1, y));
    c = mix(c, P.skinShade, .22 * smooth(.2, 0, db) * smooth(1.6, 1.4, y));
    // periwinkle tribal swirls on the flanks and hips (sw: distance to their strokes)
    if (sw < .2) c = mix(c, C('#6F7FB8'), .62 * smooth(.2, .1, sw));
    return c;
  };
}
function torsoTex() {
  const n = fbm(733), {a: [a0, a1]} = BODY.torso, per = 22, skin = skinAt(n);
  // navy swirls on the flanks (her left; u .25 side): x = (u - .25) * per (toward the back +), y = a
  const sw = swirlField(-.5, -.6, .22, 1.15, 1.3, 120, -1, [[-1.4, -.1], [-2.1, 1.2], [-2.3, 2.7], [-1.8, 3.9]]);
  const sw2 = swirlField(1.5, 2.4, .2, .72, 1.1, 300, 1, [[2.1, 3.0], [1.9, 4.2], [1.2, 4.9]]);
  return (u, v) => {
    const a = a1 - v * (a1 - a0), x = (u < .5 ? u - .25 : .75 - u) * per;
    return skin(u, 1.61 + a / 16, Math.min(sw(x, a), sw2(x, a)));
  };
}
function pelvisTex() {
  const n = fbm(733), {a: [a0, a1]} = BODY.pelvis, per = 24, skin = skinAt(n);
  const sw = swirlField(.5, .5, .2, 1.0, 1.25, 60, 1, [[-1.0, 1.3], [-1.6, 2.3]]);
  return (u, v) => {
    const a = a1 - v * (a1 - a0), x = (u < .5 ? u - .25 : .75 - u) * per;
    return skin(u, 1.33 + a / 16, sw(x, a));
  };
}
const pelvisCap = () => polarSprite((az, r) => mix(P.skinShade, P.skinDeep, .3 + .3 * r));
function thighTex() {
  const n = fbm(741), {a: [a0, a1]} = BODY.thigh;
  return (u, v) => {
    const a = a1 - v * (a1 - a0);
    // lit from the front, the inner side (u .75) in a lilac shade, a cool rim on the outside
    let c = SKIN.base(.22 + .78 * azL(u - .04, .9));
    c = mix(c, P.skinLilac, .2 * smooth(.12, 0, wrapD(u, .75)));
    c = mix(c, P.skinLilac, .1 + .12 * n(u * 6, v * 3));
    // steel streaks curving round the thigh
    const st = Math.abs(Math.sin(u * 2 * Math.PI * 3 + a * .55 + 2.5 * n(u * 4, v * 2)));
    if (st < .06 && wrapD(u, .5) > .12) c = mix(c, C('#8C9CB8'), .38);
    // navy armour strip on the outer thigh (u .25) with a periwinkle rim and a lime inlay line
    const half = .075 * smooth(-TH * .78, -TH * .3, a) * smooth(1.2, -.4, a);
    const dd = wrapD(u, .25);
    if (half > .01 && dd < half) {
      c = mix(mix(P.navy, P.navyMid, azL(u - .1)), P.navyDeep, .3 * smooth(-TH * .3, -TH * .75, a));
      if (dd > half - .016) c = mix(c, P.navyRim, .8);
      else if (Math.abs(dd - half * .35) < .009 && a < -1 && a > -TH * .65) c = mix(c, P.inlay, .85);
    }
    // the knee end in shade (it turns inside the boot cuff)
    c = mix(c, P.skinShade, .4 * smooth(-TH + .2, -TH - .9, a));
    return c;
  };
}
const thighCap = () => polarSprite(() => mix(P.skinShade, P.skinDeep, .35));
// Fur palette of the boots: blue-white clumps, blue-grey creases, the vivid blue stripe on the inner side.
const BOOT_PAL = {shade: C('#93A5C6'), base: C('#CFDCEE'), hi: C('#F2F8FC'), lilac: C('#8495BA'), edge: C('#A3B3D0')};
const BOOT_DEEP = C('#64759A');
// Fur wrap: rows of hanging tufts in wrap coordinates (x = u * per, y = -v * H), repeated across the seam.
function furWrap(seed, per, H, {dy = 1.5, dx = 1.15, L = 3.8, w = .86, blueU = .84, top = .3, light = 1, rows = null} = {}) {
  const R = rng(seed), tufts = [];
  for (let y = top, i = 0; y > -H - L * .3; y -= dy, i++) {
    for (let x = (i % 2 ? dx / 2 : 0); x < per - 1e-6; x += dx) {
      const r = [x + (R() - .5) * dx * .35, y + (R() - .5) * .3], uu = r[0] / per;
      const t = {r, a: (R() - .5) * 24, L: L * (.75 + .5 * R()), w: w * (.8 + .4 * R()), bend: [(R() - .5) * .16, (R() - .5) * .22, (R() - .5) * .28]};
      if (wrapD(uu, blueU) < .07) t.tip = P.bootBlue;
      else if (wrapD(uu, blueU) < .13) t.tip = C('#7E9CC8');
      if (rows) rows(t, i, uu);
      tufts.push(t);
    }
  }
  const all = [];
  for (const t of tufts) {
    all.push(t);
    if (t.r[0] < 2.5) all.push({...t, r: [t.r[0] + per, t.r[1]]});
    if (t.r[0] > per - 2.5) all.push({...t, r: [t.r[0] - per, t.r[1]]});
  }
  const rect = {X0: 0, X1: per, Y0: -H, Y1: 0};
  return furPainter(rect, all, {pal: BOOT_PAL, fit: false, tipK: .75, px: per / 128, deep: BOOT_DEEP,
    light: (x) => .76 + .24 * light * azL(x / per - .03, 1.1) + (1 - light) * .24});
}
function bootShin() {
  const {a: [a0, a1]} = BODY.shin;
  const f = furWrap(853, 12, a1 - a0, {top: .2});
  return (u, v) => { const c = f(u, v); return c[3] ? c : mix(BOOT_PAL.shade, BOOT_DEEP, .3); };
}
function bootFoot() {
  const {a: [a0, a1]} = BODY.foot;
  const f = furWrap(859, 17, a1 - a0, {top: .2, dy: 1.3, L: 3.2});
  return (u, v) => { const c = f(u, v); return c[3] ? c : mix(BOOT_PAL.shade, BOOT_DEEP, .3); };
}
const bootCapTop = () => polarSprite((az, r) => mix(mix(BOOT_PAL.base, BOOT_PAL.hi, azL(az)), BOOT_PAL.shade, .5 * smooth(.5, 1, r)));
const bootCapBot = () => polarSprite((az, r) => mix(BOOT_DEEP, BOOT_PAL.shade, .4 * azL(az)));
function hoofTex() {
  const {a: [a0, a1]} = BODY.hoof;
  return (u, v) => {
    const a = a1 - v * (a1 - a0);
    let c = mix(mix(P.hoofShade, P.hoofDeep, .25), mix(P.hoof, P.claw, .5), azL(u - .03, .8));
    c = mix(c, P.hoofDeep, .45 * smooth(-FT + 1.4, -FT - .1, a));
    c = mix(c, C('#FFF7EA'), .35 * smooth(.08, 0, wrapD(u, .04)) * smooth(-FT + .6, -4.4, a));
    // claw grooves splitting the toe at the front
    for (const g of [-.065, .065]) if (Math.abs(wrapD(u, 0) - Math.abs(g)) < .012 && a < -4.6) c = mix(c, C('#8C846E'), .7);
    // the top under the boot fringe in shade
    c = mix(c, P.hoofDeep, .5 * smooth(-4.6, -3.9, a));
    return c;
  };
}
const hoofCap = () => polarSprite(() => mix(P.hoofDeep, P.hoofShade, .3));

// Fur silhouette cards of the boots: four cards cross on the leg axis; each paints the boot's outline (the profile)
// plus a fringe of tufts that stands just past the turned core, so the outline is shaggy from every side while the
// round core carries the volume. Shin: spiky white tufts at the knee; foot: a pointed fringe over the hoof.
def('fur_s', {X0: -3.5, X1: 3.5, Y0: -SH - 1.2, Y1: 1.9}, [96, 176]);
def('fur_f', {X0: -4.3, X1: 4.3, Y0: -6.2, Y1: 1.4}, [112, 96]);
function furCard(seed, rect, size, prof, y0, y1, {L = 1.9, w = .7, out = .55, dy = .9, fringe = null, cuff = null, blue = false} = {}) {
  const R = rng(seed), tufts = [];
  // edge tufts rooted just inside the profile, hanging down and out; top rows first (in front)
  for (let y = y1, i = 0; y > y0; y -= dy, i++) {
    for (const s of [1, -1]) {
      const r0 = prof(y - L * .5) + out - L * .45;
      const t = {r: [s * Math.max(.2, r0 + (R() - .5) * .25), y + (R() - .5) * .3], a: s * (14 + 14 * R()), L: L * (.85 + .3 * R()), w: w * (.85 + .3 * R()),
        bend: [s * .03, s * (R() - .3) * .1, s * (R() - .2) * .14]};
      if (blue && s < 0) t.tip = C('#8FA9D2');
      tufts.push(t);
    }
    // a few tufts across the face (visible where the card is in front of the core: the ends)
    for (let x = -prof(y) + .6; x < prof(y) - .5; x += 1.1) tufts.push({r: [x + (R() - .5) * .4, y], a: (R() - .5) * 16, L: L * (.8 + .3 * R()), w: w * 1.1, bend: [0, (R() - .5) * .1, 0]});
  }
  if (cuff) cuff(tufts, R);
  if (fringe) fringe(tufts, R);
  return furPainter(rect, tufts, {pal: BOOT_PAL, px: (rect.X1 - rect.X0) / size, tipK: .7, deep: BOOT_DEEP, fit: true});
}
function furShin() {
  const B = BODY.shin;
  return furCard(877, CARD.fur_s, SIZE.fur_s[0], B.r, -SH - 1.0, .6, {
    cuff: (t, R) => {
      // spiky white tufts at the knee pointing up and out (in front of everything: unshift)
      for (const [x, a, L] of [[-1.7, 206, 2.4], [-1.1, 194, 2.1], [-.4, 184, 1.8], [.3, 174, 1.9], [1.0, 165, 2.2], [1.7, 152, 2.6]])
        t.unshift({r: [x * .95, -.55 + (R() - .5) * .25], a: a + (R() - .5) * 10, L: L * (.8 + .25 * R()), w: .66, tip: C('#F6FBFF')});
    },
  });
}
function furFoot() {
  const B = BODY.foot;
  return furCard(881, CARD.fur_f, SIZE.fur_f[0], B.r, -4.4, 1.0, {L: 2.0, w: .78, out: .65,
    fringe: (t, R) => {
      // the pointed fringe hanging over the hoof: longest in the middle, cream-white tips
      for (let x = -2.7; x <= 2.71; x += .62) {
        const L = 1.9 + .9 * (1 - Math.abs(x) / 2.9) + R() * .3;
        t.push({r: [x, -4.0 + .25 * Math.abs(x) / 2.9], a: x * 7 + (R() - .5) * 8, L, w: .72, tip: C('#F1EEE2')});
      }
    },
  });
}

// Back of the helmet (a smooth dome behind the mask; v from its crown (0) to its jaw line (1)): slate, lit from the
// front and above, a cool rim along the crown, the underside in deep shade.
function helmTex() {
  return (u, v) => {
    let c = mix(P.helmShade, P.helmLit, .25 + .65 * azL(u, 1.0) * (1 - .45 * v));
    c = mix(c, P.helmRim, .55 * smooth(.35, .05, v) * (.4 + .6 * azL(u, .6)));
    // facet lines of the plates (a few meridians and one ring)
    if (Math.abs(((u * 6 + .5) % 1) - .5) < .03 && v < .8) c = mix(c, P.helmDeep, .45);
    if (Math.abs(v - .45) < .025) c = mix(c, P.helmDeep, .35);
    c = mix(c, P.helmDeep, .5 * smooth(.65, 1, v));
    return c;
  };
}
const helmCap = () => polarSprite((az, r) => mix(P.helmShade, P.helmDeep, .5));
const furCap = () => polarSprite((az, r) => { const s = Math.sin(az * 2 * Math.PI * 9 + r * 4) * .5 + .5; return mix(mix(P.fur, P.furShade, .35 * r), P.furLilac, .25 * smooth(.7, 1, s)); });

def('knee', {X0: -2.4, X1: 3.6, Y0: -1.6, Y1: 4.2}, [64, 64]);         // white knee spikes with a lime one
def('hoof_claws', {X0: -2.0, X1: 2.0, Y0: -2.0, Y1: 1.0}, [48, 32]);   // cream hoof claws (front)
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

def('hipplate', {X0: -.6, X1: 3.4, Y0: -5.0, Y1: 1.2}, [48, 80]);      // navy tasset blade over the outer thigh (her left)
def('fin', {X0: -.4, X1: 2.6, Y0: -3.2, Y1: .8}, [32, 48]);             // small steel hip fin
function hipPlate() {
  // a navy tasset blade hanging from the hip over the outer thigh: lime inlay stroke, pale rim, violet point
  const b = sickle([.2, .55], 74, 4.9, .85, -.3);
  const sd = (x, y) => { const n = b.path.near(x, y); return n.d - b.w(n.t); };
  const G = new Grid(CARD.hipplate, 16, plateH(sd, .38));
  const r = CARD.hipplate, px = (r.X1 - r.X0) / SIZE.hipplate[0];
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    const n = b.path.near(x, y), s = n.s / Math.max(1e-6, b.w(n.t));
    let c = shadeAt(M.navy, litAt(G, x, y, {k: 1.5}), d, px, {outline: 0});
    if (s > .08 && s < .42 && n.t > .12 && n.t < .72) c = mix(c, P.inlay, .9 * smooth(.08, .16, s) * smooth(.42, .32, s));
    c = mix(c, P.violetTip, .7 * smooth(.72, 1, n.t));
    if (d > -px * 1.2) c = mix(c, M.navy.line, .85);
    else if (d > -px * 2.6) c = mix(c, P.navyRim, .45);
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
def('tu', {X0: -4.2, X1: 12.6, Y0: -12.2, Y1: 4.6}, [128, 128]);
def('tl', {X0: -4.4, X1: 8.0, Y0: -20.6, Y1: 1.8}, [80, 144]);
def('tuf', {X0: -4.2, X1: 12.6, Y0: -12.2, Y1: 4.6}, [64, 64]);
def('tlf', {X0: -4.4, X1: 8.0, Y0: -20.6, Y1: 1.8}, [48, 80]);
// spiral "eye" curl at the hip (0, 0) whose outer turn leaves as the ribbon toward the end point (9.6, -9.4)
const TU_PATH = () => {
  const sp = spiralPts(0, 0, .55, 2.4, 1.15, 200, 1, 40);
  const tail = spline([sp[sp.length - 1], [3.2, -1.6], [5.0, -4.6], [7.2, -7.2], [9.6, -9.4]], 10);
  return new Path([...sp, ...tail.slice(1)]);
};
const TL_PATH = () => new Path(spline([[0, 0], [1.6, -3.4], [1.0, -7.2], [-1.0, -10.6], [-.4, -14.4], [1.8, -17.2], [3.6, -19.6]], 10));
// A flat ribbon that twists: its lit edge (yellow-white) and its shaded edge (teal underside) swap sides past the
// S-bend (twist > 0: the t where the twist happens), a fine vein down the middle (Pyro: gold, magenta underside).
function ribbonPainter(rect, size, pth, w, look, {twist = 2} = {}) {
  const sd = (x, y) => { const n = pth.near(x, y); return n.d - w(n.t); };
  const G = new Grid(rect, 12, plateH(sd, .22));
  const px = (rect.X1 - rect.X0) / size[0];
  const pyro = look === 'pyro', flat = look === 'flat';
  const m = pyro ? mat([[-.2, C('#6D3A4A')], [.25, C('#A35D83')], [.48, C('#C96839')], [.64, C('#F2B076')], [.86, C('#FAD77C')], [1, C('#FCE2CF')]], C('#5A2A2A'), white, .4)
    : mat([[-.2, C('#2F5A3A')], [.15, C('#4E7F3A')], [.35, C('#8DB043')], [.52, C('#B5D24E')], [.68, C('#D2E668')], [.84, C('#EAF59A')], [1, C('#FAFFD8')]], C('#2C5A3C'), C('#FFFFF0'), .4);
  const under = pyro ? C('#A35D83') : P.ribTeal, lit = pyro ? C('#FFF0C8') : C('#F4FCB8');
  return (u, v) => {
    const x = rect.X0 + u * (rect.X1 - rect.X0), y = rect.Y1 - v * (rect.Y1 - rect.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    if (flat) return d > -px * 1.2 ? P.fxShade : P.fxLime;
    const n = pth.near(x, y), L = litAt(G, x, y, {k: 1.3}), ww = Math.max(1e-3, w(n.t));
    const side = clamp(n.s / ww, -1, 1) * (n.t > twist ? -1 : 1);
    let c = shadeAt(m, L, d, px, {outline: 0});
    c = mix(c, under, .7 * smooth(-.05, -.7, side));
    c = mix(c, lit, .7 * smooth(.3, .75, side));
    // the twist itself: the ribbon turns edge-on, a narrow bright band across it
    const tw = Math.abs(n.t - twist) * pth.L;
    if (twist < 1 && tw < .5) c = mix(c, lit, .45 * smooth(.5, 0, tw));
    if (Math.abs(n.s) < px * 1.3 && n.t > .05 && n.t < .92) c = mix(c, pyro ? C('#C96839') : C('#6E9A3A'), .5);
    if (d > -px * 1.2) c = mix(c, pyro ? C('#5A2A2A') : C('#2C5A3C'), .85);
    return c;
  };
}
function tendrilUp(look) {
  // the spiral "eye" scroll at the hip (a flat ribbon curling in, round a navy core), then the broad ribbon
  const pth = TU_PATH();
  const w = t => (t < .42 ? .5 + .72 * t / .42 : 1.22 + .38 * Math.sin(Math.min(1, (t - .42) / .58) * Math.PI * .5));
  const base = ribbonPainter(CARD.tu, SIZE[look === 'flat' ? 'tuf' : 'tu'], pth, w, look, {twist: 2});
  const r = CARD.tu;
  return (u, v) => {
    const c = base(u, v);
    if (c[3]) return c;
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), rr = Math.hypot(x, y);
    if (rr < 1.2 && look !== 'flat') return mix(P.spiralNavy, C('#2E3E7A'), smooth(1.2, .3, rr));
    return TRANSPARENT;
  };
}
function tendrilLo(look) {
  // the ribbon's long lower half: an S that swells, twists once and tapers to a sharp point
  const pth = TL_PATH();
  return ribbonPainter(CARD.tl, SIZE[look === 'flat' ? 'tlf' : 'tl'], pth, t => 1.12 * (1 + .45 * Math.sin(Math.min(1, t / .7) * Math.PI)) * (1 - Math.pow(t, 1.7) * .97), look, {twist: .48});
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
// ---- props: the entrance cocoon and the wrapped pod (turned shells, butterfly_geometry.mjs) -----------------------
// PROPS holds their profiles (model units at the prop's display scale; a along the vertical axis from the model
// centre, r the radius across, kz depth / width). Each prop is two smooth turned solids: a glowing lime inner core
// and, just outside it, a cut-out shell of wrapped wing plates; where the shell's plates part (the windows, the seams)
// the core's light shows, with the plates' real thickness at the edges.
export const PROPS = {
  // entrance cocoon (scale 3, 1 u = 0.19 b, 4 b tall): a diamond, widest a third from the top, a knot and a crystal spike below
  cocoonCore: {a: [-10.8, 10.6], kz: .86, pts: [[-10.8, .05], [-9.8, .42], [-8.9, .8], [-8.3, 1.05], [-7.4, 1.0], [-5.0, 1.75], [-2.0, 2.6], [1.0, 3.2], [3.0, 3.35],
    [5.0, 3.0], [7.0, 2.25], [8.8, 1.3], [10.0, .5], [10.6, .05]]},
  cocoonShell: {a: [-8.4, 8.8], kz: .86, pts: [[-8.4, 1.25], [-7.4, 1.35], [-5.0, 2.1], [-2.0, 2.95], [1.0, 3.55], [3.0, 3.72], [5.0, 3.35], [7.0, 2.55], [8.8, 1.6]]},
  // wrapped pod (scale 2.5, 1 u = 0.156 b): an egg r 1.4 b, 3.5 b tall
  podCore: {a: [-10.0, 10.0], kz: .92, pts: [[-10.0, .6], [-9.3, 3.0], [-7.4, 5.6], [-4.0, 7.2], [0, 7.6], [4.0, 7.2], [7.4, 5.6], [9.3, 3.0], [10.0, .6]]},
  podShell: {a: [-11.2, 11.2], kz: .92, pts: [[-11.2, .7], [-10.5, 3.2], [-8.6, 6.2], [-4.6, 8.4], [0, 8.95], [4.6, 8.4], [8.6, 6.2], [10.5, 3.2], [11.2, .7]]},
};
for (const b of Object.values(PROPS)) b.r = profile(b.pts);
def('cocoon_core', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [128, 256]);
def('cocoon_shell', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [256, 256]);
def('cocoon_hook', {X0: -1.0, X1: 7.0, Y0: -1.6, Y1: 4.6}, [96, 80]);
def('pod_core', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [64, 64]);
def('pod_shell', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [512, 256]);
def('pod_hook', {X0: -.6, X1: 5.6, Y0: -.8, Y1: 6.8}, [64, 80]);
// signed azimuth of a wrap u in degrees: 0 front, + toward her left, -180..180
const azDeg = u => ((u + .5) % 1 + 1) % 1 * 360 - 180;
// The inner bud of the cocoon: hot white-lime at the front and back windows, nested lime V petals rising to the tip,
// a bright crystal spike below.
function cocoonCoreTex() {
  const {a: [a0, a1]} = PROPS.cocoonCore, n = fbm(1201);
  return (u, v) => {
    const a = a1 - v * (a1 - a0), s = azDeg(u), sf = Math.min(Math.abs(s), 180 - Math.abs(s)) / 90;   // 0 at the windows .. 1 at the sides
    let c = mix(P.cocoonWin, C('#9FC33A'), .55 * sf);
    // nested V petals (chevrons pointing down), brighter toward the window centre lines
    const ph = (a * .55 + sf * 2.6 + .3 * n(u * 6, v * 6)) % 1;
    c = mix(c, C('#7FA324'), .55 * smooth(.08, 0, Math.abs(ph - .5) - .38) * (1 - .4 * sf));
    c = mix(c, C('#F4FFD0'), .75 * smooth(.35, 0, sf) * smooth(-6, 2, a) * smooth(10.4, 6.0, a));
    c = mix(c, C('#FBFFE8'), .6 * smooth(7.5, 10.4, a));
    // the knot and the spike: a pale lime crystal with facet lines
    if (a < -7.3) {
      const f = Math.abs(Math.sin(s * Math.PI / 45));
      c = mix(mix(P.cocoonSpike, C('#F1FCC3'), .55 * (1 - f)), C('#7FB82A'), .35 * smooth(.85, 1, f));
    }
    return c;
  };
}
// The wrapped wing plates: two dark slate-green plates crossing in an X low on the front and the back; above the
// crossing their lime leading edges part into the glowing V window, at the top the plates end in a scalloped rim.
// Shapes are drawn in surface units: x = arc length round the axis at the widest ring, y = a.
function cocoonShellTex() {
  const {a: [a0, a1]} = PROPS.cocoonShell, n = fbm(1213), K = Math.PI * 3.5 / 180;
  // the V window (v1 f120): a diamond of glowing bud between the plates' lime leading edges, widest at the corners
  // (a = 4, half-width 2.8 u of arc), narrowing to the lime tip at the top and closing where the plates cross at
  // a = -2; below it plate B lies over plate A and its edge runs on down to the knot (an X of lime edges)
  const ww = y => (y < -2 ? 0 : y < 4 ? 2.8 * Math.sin(Math.PI / 2 * (y + 2) / 6) : 2.8 - 1.7 * Math.pow((y - 4) / 4.8, 1.3));
  const eA = y => (y >= -2 ? -ww(y) : 2.6 * (-2 - y) / 5.6), eB = y => (y >= -2 ? ww(y) : -2.6 * (-2 - y) / 5.6), XC = -2;
  // engraved scroll lines on the side plates (x from the side line at +-5.5)
  // (the back half folds onto the front, so the lines stay clear of the side line at 5.5)
  const grooves = grooveOf([spline([[3.6, 7.6], [4.5, 4.6], [4.8, .8], [4.6, -3.4], [3.9, -6.8]], 8), spline([[3.2, 6.0], [3.0, 4.4], [3.4, 3.4], [4.0, 3.6]], 6),
    spline([[2.6, -2.6], [3.2, -4.8], [2.8, -7.2]], 6)], .24);
  return (u, v) => {
    const y = a1 - v * (a1 - a0);
    let sd = azDeg(u);
    if (Math.abs(sd) > 90) sd = (sd > 0 ? 180 : -180) - sd;      // the back repeats the front, mirrored
    const x = sd * K, ea = eA(y), eb = eB(y);
    if (x > ea && x < eb) return TRANSPARENT;                      // the V window over the glowing core
    // scalloped top rim: low over the window, rising to the side corners under the hooks
    const top = 8.8 - .35 * Math.abs(Math.sin(x * 1.1));
    if (y > top) return TRANSPARENT;
    // distance to the visible leading edge: A's and B's edges above the crossing, only B's below it (B lies over A)
    const dE = y > XC ? Math.min(Math.abs(x - ea), Math.abs(x - eb)) : Math.abs(x - eb);
    const L = .35 + .65 * azL(u, 1);
    let c = mix(P.cocoon, P.cocoonLit, L);
    c = mix(c, C('#2A3934'), .35 * smooth(-4, -8.5, y));
    // A's plate under B below the crossing: a contact shadow beside B's edge
    if (y < XC && x < eb && eb - x < .8) c = mix(c, C('#16201C'), .5 * smooth(.8, 0, eb - x));
    const g = grooves(Math.abs(x), y);
    if (g > .2) c = mix(c, C('#22302B'), .6 * g);
    // the plates' lime leading edges and a lime rim at the top
    if (dE < .42 && !(y < XC && x < eb)) c = mix(c, mix(P.fxLime, C('#E8FFB0'), smooth(.42, 0, dE) * .6), .92 * smooth(.42, .22, dE));
    if (y > top - .32) c = mix(c, P.fxLime, .8);
    c = mix(c, C('#4E6D5C'), .15 * n(u * 9, v * 9));
    return c;
  };
}
function cocoonHook() {
  // a curled scroll horn at the upper corner: rises from the plate and curls outward and down (sheet 08 H)
  // grows out of the widest corner, sweeps out and up and rolls over outward and down (a ram's-horn scroll, sheet 08 H)
  const sd = sdTaper([[.1, -.2], [1.0, 1.5], [2.4, 2.8], [4.0, 3.1], [5.3, 2.2], [5.5, .8], [4.7, .1], [3.9, .5], [4.0, 1.3]], 1.25, .22, .8);
  const G = new Grid(CARD.cocoon_hook, 16, plateH(sd, .5));
  const inner = new Path(spline([[.5, .1], [1.3, 1.3], [2.5, 2.2], [3.8, 2.4], [4.6, 1.8]], 8));
  const r = CARD.cocoon_hook, px = (r.X1 - r.X0) / SIZE.cocoon_hook[0];
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    let c = shadeAt(M.cocoon, litAt(G, x, y, {k: 1.3}), d, px, {outline: 0});
    if (inner.near(x, y).d < .16) c = mix(c, P.fxLime, .9);
    if (d > -px * 1.2) c = mix(c, C('#0E1614'), .85);
    return c;
  };
}
// The pod's inner light: white-hot at the equator seams, lime toward the poles, soft radial streaks.
function podCoreTex() {
  const n = fbm(1229);
  return (u, v) => {
    const lat = Math.abs(v - .5) * 2, st = Math.sin(u * 2 * Math.PI * 7 + 3 * n(u * 4, v * 4)) * .5 + .5;
    let c = mix(C('#FBFFE8'), P.fxHi, smooth(.2, .9, lat));
    c = mix(c, P.fxLime, .5 * smooth(.6, 1, lat));
    return mix(c, C('#FFFFFF'), .25 * smooth(.7, 1, st) * (1 - lat));
  };
}
// The four wings folded round her: each forewing covers the front half of one side (s 3..104 degrees from the
// front seam), each hindwing the back half (96..177, under the forewing's rear edge), so the silhouette is solid
// plate from every side and the core's light shows only in the front and back seams and at the poles. Forewing
// panel: opal lobes in raised lime frames on the sculpted scroll plate, the steel spar sweeping along its lower edge,
// a violet rim on the seam; hindwing panel: the scroll lobe with its navy spiral eye, the blade along the lower edge
// with its glowing blue tip. The plates are height fields lit like the wing cards (litAt). Local units: X 0 at the
// panel's front edge .. 16 at its rear edge, Y = a.
function podShellTex() {
  const {a: [a0, a1]} = PROPS.podShell, H = 11.2;
  const FW = {s0: 3, s1: 104}, HW = {s0: 96, s1: 177}, rect = {X0: 0, X1: 16, Y0: -H, Y1: H};
  // the leading-edge spar crosses the panel in a long S from the top of the front seam to the rear-bottom; the outer
  // lobe sits above-behind it, the inner lobe below-in-front, scroll ridges and a spiral eye between
  const fwLobe = sdEllipse(10.4, 3.6, 3.6, 4.6, 24), fwLobe2 = sdEllipse(8.6, -7.6, 1.7, 1.3, -30);
  const fwLobes = sdUnion(fwLobe, fwLobe2);
  const fwSpar = new Path(spline([[.4, 10.4], [2.4, 7.2], [4.6, 2.6], [7.4, -1.6], [11.0, -5.0], [15.6, -7.0]], 10));
  const sparW = t => .8 + .25 * Math.sin(t * Math.PI);
  const fwEye = sdCircle(13.4, -2.4, 1.5), fwVol = grooveOf([spiralPts(13.4, -2.4, .25, 1.45, 1.4, 90, 1)], .3);
  const fwRidges = grooveOf([spline([[6.0, 9.8], [7.0, 7.4], [6.4, 4.8]], 6), spline([[14.8, 9.6], [14.4, 7.4], [15.2, 5.4]], 6),
    spiralPts(6.4, 9.0, .25, 1.15, 1.2, 250, -1), spline([[1.2, -1.6], [2.2, -3.4], [1.6, -5.4], [1.8, -8.6]], 6), spline([[7.4, -6.6], [9.0, -8.6], [12.0, -9.6]], 6)], .42);
  const hwEye = sdCircle(4.6, 3.4, 2.3), hwVol = grooveOf([spiralPts(4.6, 3.4, .3, 2.2, 1.5, 80, 1)], .42);
  const hwBlade = new Path(spline([[12.8, -1.2], [9.8, -4.4], [6.4, -7.0], [2.8, -8.8], [.4, -9.4]], 10));
  const bladeW = t => 1.3 - .85 * t;
  const hwRidges = grooveOf([spline([[8.2, 9.4], [9.8, 6.0], [8.6, 2.2], [10.2, -.6], [12.6, -2.4]], 8), spline([[1.4, 9.2], [3.2, 7.4], [6.2, 7.4]], 6),
    spiralPts(11.6, 6.8, .25, 1.3, 1.25, 90, 1)], .42);
  const dome = (X, Y) => .7 * Math.sqrt(Math.max(0, 1 - ((X - 8) / 9) ** 2 - (Y / 12) ** 2));
  const rim = (d, w) => (d > 0 && d < w ? Math.sin(Math.PI * d / w) : 0);
  const hF = (X, Y) => {
    const dl = fwLobes(X, Y), n = fwSpar.near(X, Y);
    let h = dome(X, Y) + .55 * rim(dl, .9) + .5 * fwRidges(X, Y) - (dl < 0 ? .35 : 0) + .4 * bevel(Math.min(X, 16 - X) - 16, .1) * 0;
    if (fwEye(X, Y) < 0) h += .5 * fwVol(X, Y) - .3;
    if (n.d < sparW(n.t)) h = Math.max(h, .9 + .5 * Math.sqrt(1 - (n.d / sparW(n.t)) ** 2));
    return h - .5 * smooth(1.2, 0, X);
  };
  const hH = (X, Y) => {
    const n = hwBlade.near(X, Y);
    let h = dome(X, Y) + .5 * hwRidges(X, Y);
    if (hwEye(X, Y) < 0) h += .55 * hwVol(X, Y) - .35;
    if (n.d < bladeW(n.t)) h = Math.max(h, .8 + .3 * Math.sqrt(1 - (n.d / bladeW(n.t)) ** 2));
    return h - .5 * smooth(1.2, 0, 16 - X);
  };
  const GF = new Grid(rect, 10, hF), GH = new Grid(rect, 10, hH), px = 16 / 256;
  const tipRamp = ramp([[0, '#86B8EA'], [.4, '#284AA4'], [.7, '#C1DFFA'], [1, '#F2F8FF']]);
  return (u, v) => {
    const a = a1 - v * (a1 - a0), py = a / H, s = Math.abs(azDeg(u)), Y = a;
    const inFW = s >= FW.s0 && s <= FW.s1, inHW = s >= HW.s0 && s <= HW.s1;
    if (!inFW && !inHW) return TRANSPARENT;                 // the front and back seams
    const cap = 1;                                           // (the seams stay narrow up to the poles)
    if (inFW && (s <= FW.s1 - 1.5 || !inHW)) {
      const pxl = (s - FW.s0) / (FW.s1 - FW.s0), X = pxl * 16;
      if (pxl < .55 * (1 - cap)) return TRANSPARENT;
      const L = litAt(GF, X, Y, {k: 1.1}), dl = fwLobes(X, Y), n = fwSpar.near(X, Y), sw = sparW(n.t);
      let c;
      if (n.d < sw) {
        c = shadeAt(M.steel, L, -1, px, {outline: 0});
        const k = n.s / sw;
        c = mix(c, RAMP.sheen(clamp(n.t * .9)), .5 * smooth(.45, .1, Math.abs(k + .4)));
        if (n.d > sw - px * 2) c = mix(c, M.steel.line, .8);
      } else if (dl < 0) {
        c = membrane('dendro', X * 1.2 + 6, Y * 1.1 + 12, dl, 2.0);
        if (dl > -.3) c = mix(c, C('#4A3C6A'), .65);
      } else {
        c = shadeAt(M.lime, L, -1, px, {outline: 0});
        if (dl < .9) {
          const vio = mat([[-.2, C('#1E1430')], [.3, C('#3A2C5C')], [.6, C('#5E4A8E')], [.85, C('#A48ADC')], [1, C('#E8D8FF')]], C('#140C22'));
          c = mix(c, shadeAt(vio, L, -1, px, {outline: 0}), .55 * smooth(.9, .3, dl) * smooth(-.2, .8, -(X - 7.6) * .6 - (Y - 3) * .8));
        }
        const de = fwEye(X, Y);
        if (de < 0 && fwVol(X, Y) < .25) c = mix(c, P.spiralNavy, .9 * smooth(.25, .05, fwVol(X, Y)));
        if (n.d < sw + .5) c = mix(c, P.limeDeep, .4 * smooth(sw + .5, sw, n.d));
      }
      if (pxl < .035) c = mix(c, C('#A48ADC'), .8 * smooth(.035, .01, pxl));
      if (pxl < .012 + .55 * (1 - cap)) c = mix(c, P.fxCore, .85);
      return c;
    }
    const pxl = (s - HW.s0) / (HW.s1 - HW.s0), X = pxl * 16;
    if (1 - pxl < .55 * (1 - cap)) return TRANSPARENT;
    const L = litAt(GH, X, Y, {k: 1.1}), n = hwBlade.near(X, Y), bw = bladeW(n.t);
    let c = shadeAt(M.lime, L, -1, px, {outline: 0});
    const de = hwEye(X, Y);
    if (de < 0 && hwVol(X, Y) < .25) c = mix(c, P.spiralNavy, .9 * smooth(.25, .05, hwVol(X, Y)));
    if (n.d < bw) {
      c = mix(c, RAMP.holo(clamp(.2 + n.t * .7 + n.s * .1)), .65);
      const tip = smooth(.6, 1, n.t);
      c = mix(c, tipRamp(tip), smooth(0, .3, tip));
      if (n.d > bw - px * 2) c = mix(c, P.limeDeep, .6);
    }
    if (X < 1.2) c = mix(c, P.limeDeep, .4 * smooth(1.2, 0, X));     // tucked under the forewing's rear edge
    if (pxl > .965) c = mix(c, C('#A48ADC'), .8 * smooth(.965, .99, pxl));
    if (1 - pxl < .012 + .55 * (1 - cap)) c = mix(c, P.fxCore, .85);
    return c;
  };
}
function podHook() {
  // a hindwing blade tip sticking out of the folded pod: lime root, iridescent body, a glowing blue point
  const pth = new Path(spline([[.2, 6.2], [1.4, 4.4], [2.8, 2.6], [4.2, .8], [5.3, -.6]], 10));
  const w = t => .9 * (1 - Math.pow(t, 1.6) * .96);
  const sd = (x, y) => { const n = pth.near(x, y); return n.d - w(n.t); };
  const G = new Grid(CARD.pod_hook, 16, plateH(sd, .5));
  const r = CARD.pod_hook, px = (r.X1 - r.X0) / SIZE.pod_hook[0];
  const tip = ramp([[0, '#A4BD6A'], [.35, '#86B8EA'], [.6, '#284AA4'], [.8, '#86B8EA'], [.92, '#C1DFFA'], [1, '#F2F8FF']]);
  return (u, v) => {
    const x = r.X0 + u * (r.X1 - r.X0), y = r.Y1 - v * (r.Y1 - r.Y0), d = sd(x, y);
    if (d > 0) return TRANSPARENT;
    const n = pth.near(x, y);
    let c = shadeAt(M.lime, litAt(G, x, y, {k: 1.2}), d, px, {outline: 0});
    if (n.s < 0) c = mix(c, RAMP.holo(clamp(n.t * .8 + .1)), .65);
    c = mix(c, tip(smooth(.3, 1, n.t)), smooth(.3, .6, n.t));
    if (d > -px * 1.2) c = mix(c, n.t > .7 ? P.tipDeep : M.lime.line, .85);
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
// Orb (B4): a translucent lime glass sphere (wrap texture of a turned sphere) with bright rim; gyroscope ring.
def('orb', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [64, 64]);
def('orb_cap', {X0: 0, X1: 1, Y0: 0, Y1: 1}, [32, 32]);
for (const k of [50, 70, 85, 95]) def('orb_a' + k, {X0: 0, X1: 1, Y0: 0, Y1: 1}, [32, 32]);
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
function orbCap(inner = 0) {
  // the orb's caps and step ledges: flat glass discs / annuli (inner = inner radius ratio), the orb's polar colour
  const c = mix(C('#D2FA8E'), C('#9CDB7D'), .6);
  return (u, v) => { const r = Math.hypot(u - .5, v - .5) * 2; return r > 1 || r < inner ? TRANSPARENT : [c[0], c[1], c[2], Math.round(255 * .66)]; };
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
  add('helm', 'helm', helmPainter()); add('cheek', 'cheek', cheekPainter()); add('crown', 'crown', crownPainter());
  add('eye', 'eye', eyePainter()); add('chev', 'chev', chevPainter());
  add('antenna', 'antenna', antennaPainter()); add('streamer', 'streamer', streamerPainter());
  add('fan', 'fan', bladePainter(CARD.fan, SIZE.fan, FAN_BLADES())); add('fanb', 'fanb', bladePainter(CARD.fanb, SIZE.fanb, FANB_BLADES())); add('shplate', 'shplate', shplatePainter());
  add('crescent', 'crescent', crescentPainter(false)); add('crescent_tell', 'crescent_tell', crescentPainter(true)); add('shard', 'shard', shardPainter()); add('diamond', 'diamond', diamondPainter());
  add('torso_w', 'torso_w', torsoTex()); add('pelvis_w', 'pelvis_w', pelvisTex()); add('pelvis_w_cap', 'pelvis_w_cap', pelvisCap());
  add('thigh_w', 'thigh_w', thighTex()); add('thigh_w_cap', 'thigh_w_cap', thighCap());
  add('boot_s', 'boot_s', bootShin()); add('boot_s_cap', 'boot_s_cap', bootCapTop()); add('boot_f', 'boot_f', bootFoot()); add('boot_f_cap', 'boot_f_cap', bootCapBot());
  add('hoof_w', 'hoof_w', hoofTex()); add('hoof_w_cap', 'hoof_w_cap', hoofCap());
  add('furw', 'furw', furTile(941)); add('helmw', 'helmw', helmTex()); add('antw', 'antw', (u, v) => mix(mix(P.antShade, P.ant, .6), P.antHi, Math.sin(u * Math.PI) ** 2)); add('helmw_cap', 'helmw_cap', helmCap()); add('furw_cap', 'furw_cap', furCap());
  add('fur_s', 'fur_s', furShin()); add('fur_f', 'fur_f', furFoot()); add('knee', 'knee', kneeSpikes()); add('hoof_claws', 'hoof_claws', hoofClaws());
  add('hipplate', 'hipplate', hipPlate()); add('fin', 'fin', finPainter());
  add('core', 'core', corePainter(), true);
  add('cocoon_core', 'cocoon_core', cocoonCoreTex()); add('cocoon_shell', 'cocoon_shell', cocoonShellTex()); add('cocoon_hook', 'cocoon_hook', cocoonHook());
  add('cocoon_glow', 'cocoon_glow', cocoonGlow(), true);
  add('pod_core', 'pod_core', podCoreTex()); add('pod_shell', 'pod_shell', podShellTex()); add('pod_hook', 'pod_hook', podHook());
  add('orb', 'orb', orbTex(), true); add('orb_cap', 'orb_cap', orbCap(), true);
  for (const k of [50, 70, 85, 95]) add('orb_a' + k, 'orb_a' + k, orbCap(k / 100), true); add('ring', 'ring', ringPainter(), true); add('ringw', 'ringw', ringBandTex(), true);
  return out;
}
export const spriteId = name => 'rlk:mboss/butterfly/' + name;
// sprite name -> card rect (looks share their base rect)
export const cardOf = name => CARD[name] || CARD[name.replace(/_(dendro|pyro|flat)$/, '')] || CARD[name.split('_')[0]];
export function paintButterflyTextures(rp, only = null) {
  return paintSpriteSet(rp, 'assets/rlk/textures/mboss/butterfly', butterflySprites(), spriteId, only);
}
export {P as BF_PAL};
