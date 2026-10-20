// Painted sprites of the Apep phase-2 objects (아펩의 오아시스 파수꾼, plan §5): the six organisms (기본 / 양육 / 수호 / 둥지 /
// 파괴 / 포식성), the Heart of the Oasis, the 소생의 찬가 domes, the 둥지 wall blades, the 생명의 손 stalks and the death seed.
// Used by build_mboss_apep_org.mjs; written to assets/rlk/textures/mboss/apep_om/<name>.png and merged into the item
// atlas (ids rlk:mboss/apep_om/<name>).
//
// This module also owns the 2D shapes (SH) that the slabs of apep_org_geometry.mjs extrude: a slab's card shows the sprite
// painted from the same signed-distance shape, so the alpha-cut outline and the extruded core always agree.
//
// Palette: understand/model.md §7.3 and model_p3.md §7 (org_bell_v2, egg_green), painted ~10 % less yellow than sampled
// (the phase-2 haze, plan §5.1). Materials that several looks share are painted once and tinted per look
// (tintindex 0 + constant-tint item definitions; plan R13): the basic bulb, the Heart bulb, the 파괴 husk.
import {C, clamp, smooth, mix, fbm, TRANSPARENT, paintSpriteSet} from './mboss_paint_lib.mjs';
import {registerTile, registerWrap, sdPoly, sdCircle, sdUnion, sdSub, stroke, bez} from './mboss_shape_lib.mjs';

export {C, clamp, smooth, mix};
export const spriteId = name => 'rlk:mboss/apep_om/' + name;
const ramp = list => { const cs = list.map(C); return t => { const x = clamp(t) * (cs.length - 1), i = Math.min(cs.length - 2, Math.floor(x)); return mix(cs[i], cs[i + 1], x - i); }; };
const A = (c, a) => [c[0], c[1], c[2], Math.round(clamp(a) * 255)];
const lift = (c, k) => mix(c, [255, 255, 250, 255], clamp(k));
const sink = (c, k) => mix(c, [14, 20, 16, 255], clamp(k));
const N = {a: fbm(11), b: fbm(23), c: fbm(37), d: fbm(41), e: fbm(53)};
const h1 = x => { const s = Math.sin(x * 127.1) * 43758.5453; return s - Math.floor(s); };

// ---- palette (hi -> deep) ------------------------------------------------------------------------------------------
export const PAL = {
  bell: ramp(['#F4F3EC', '#E2E0D7', '#C9C8BC', '#ADAEA2', '#8E9084', '#6C6F64']),        // org_bell_v2, lifted for the tints
  teal: ramp(['#73A29C', '#527F79', '#3E625E', '#2F4B4A', '#223838', '#152626']),        // org_teal
  pale: ramp(['#F0F2EA', '#DADFD3', '#C0C9BC', '#A3AFA0', '#869283', '#687464']),        // org_pale
  core: ramp(['#FFFFE2', '#FBFF94', '#E6F26E', '#D0DB58', '#AEBB40', '#808C2C']),        // org_core
  olive: ramp(['#B7BC78', '#959A58', '#767C40', '#5A6030', '#404622']),
  gem: ramp(['#FFFCC0', '#FEF68E', '#F7EC58', '#EED54C', '#D4B83A', '#9C842A']),         // p3_gem
  lime: ramp(['#EAF9B4', '#CDEC8A', '#AAD86A', '#86BC52', '#64983E', '#46722C']),        // p3_rim / shield panes, walls
  hood: ramp(['#F0EFD8', '#DEDDBC', '#C5C4A0', '#A6A584', '#838262', '#5E5D44']),        // pred_hood, de-yellowed
  fin: ramp(['#E8F8D6', '#C9EAAE', '#ABD08E', '#89AC74', '#687F5C', '#4A5C42']),         // pred_fin
  eye: ramp(['#DCFFFB', '#A4E0DC', '#62B2AE', '#2E7579', '#1A4A4C', '#0A1A1A']),         // pred_eye
  destr: ramp(['#C9CCB8', '#8E9478', '#4E5B52', '#3A4A44', '#2A3633', '#1A2220']),
  dface: ramp(['#FFFFF4', '#FEFFD2', '#FBFFAE', '#EEF38C', '#D8DD6E', '#B4B848']),
  root: ramp(['#8A7C48', '#6A5E36', '#52482A', '#3E3720', '#2D2817', '#1D1A0F']),         // heart_root
  tip: ramp(['#FFFCC4', '#FBEF6C', '#E9DB58', '#D8CA4E', '#B8AD44', '#8C8432']),          // heart_tip
  vine: ramp(['#5E6E44', '#475634', '#364428', '#28321D', '#1B2214', '#10150C']),
  vineL: ramp(['#D2E0A6', '#ADC283', '#88A062', '#667E48', '#485E34', '#2E3E22']),     // the vine hand (v2 f2200)
  stalk: ramp(['#ECEEE6', '#D6D9CF', '#BDC2B4', '#9FA698', '#7E867A', '#5C6458']),        // p3_pale
  dome: ramp(['#F6FFDA', '#E2F8AA', '#C4EC7A', '#A0D656', '#7CB63C', '#5A902A']),
  gold: ramp(['#FFF6C2', '#F9E48A', '#EDCB5A', '#D6AC3C', '#B08A2C', '#7C601E']),
  black: ramp(['#4A4E46', '#34382F', '#24271F', '#181A14', '#0E100C']),
};

// ---- the item-display light and light-corrected lofts -------------------------------------------------------------
// (the Azhdaha R2 torso method, azhdaha_body.mjs): F(ny) = the item-display light (two world-fixed lights, ambient 0.4;
// minecraft entity lighting) averaged over the yaw, for a unit normal with up component ny. A stepped loft's vertical
// facets get F(0) and its ledges F(+-1) (up ledges 1.6x brighter than the facets: the terraced bands of AP-ORG1). A lit
// loft paints every facet and ledge albedo x B(ny of the smooth surface there) / F(ny of the face), B = the smooth
// shading at contrast g (1 = full), so the steps shade like one smooth body: no light stripes, a lit top, a dim belly.
const nrm3 = v => { const l = Math.hypot(...v); return v.map(x => x / l); };
const dot3 = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const ML0 = nrm3([.2, 1, -.7]), ML1 = nrm3([-.2, 1, .7]);
const mcShade = n => Math.min(1, .6 * (Math.max(0, dot3(n, ML0)) + Math.max(0, dot3(n, ML1))) + .4);
const FLT = Array.from({length: 201}, (_, i) => { const ny = -1 + i / 100, h = Math.sqrt(Math.max(0, 1 - ny * ny)); let s = 0;
  for (let j = 0; j < 72; j++) { const a = j * Math.PI / 36; s += mcShade([h * Math.cos(a), ny, h * Math.sin(a)]); } return s / 72; });
export const FL = ny => { const x = (Math.max(-1, Math.min(1, ny)) + 1) * 100, i = Math.min(199, Math.floor(x)); return FLT[i] + (FLT[i + 1] - FLT[i]) * (x - i); };
export const litB = (ny, g) => FL(0) * (1 + g * (FL(ny) / FL(0) - 1));
export const litK = (nyS, nyF, g) => litB(nyS, g) / FL(nyF);
// loft frames (mboss_shape_lib): A along the loft, theta measured from e1 toward e2
export const LFR = {z: {A: [0, 0, 1], e1: [1, 0, 0], e2: [0, 1, 0]}, y: {A: [0, 1, 0], e1: [1, 0, 0], e2: [0, 0, -1]}, x: {A: [1, 0, 0], e1: [0, 0, -1], e2: [0, 1, 0]}};
const suppSec = (st, th) => { const c = Math.cos(th * D2R_), s = Math.sin(th * D2R_), r = Array.isArray(st.r) ? st.r : [st.r, st.r, st.r, st.r];
  const a = c >= 0 ? r[0] : r[2], b = s >= 0 ? r[1] : r[3], ell = Math.hypot(a * c, b * s); return ell + (st.box || 0) * (Math.abs(a * c) + Math.abs(b * s) - ell); };
const D2R_ = Math.PI / 180;
// Lit loft profiles: name -> {axis, n, sec(a) -> {r, c, box}, as (station positions), g (contrast), W, H (facet wrap px),
// albedo(u, v) (u round the facets 0..1, v along the wrap 0..1: from the top for 'y' lofts, from a0 for 'z' / 'x'),
// owner, translucent}. The sprite is the facet wrap (W px) plus a swatch column (SWW px) of 4 px cells: the ledge and
// cap colours, albedo of a v band x a quantised K (KQ levels).
export const PROF = {};
export const SWW = 16, KQ = {n: 16, k0: .4, dk: .08};
const profV = (p, a) => { const a0 = Math.min(...p.as), a1 = Math.max(...p.as); return p.axis === 'y' ? (a1 - a) / (a1 - a0) : (a - a0) / (a1 - a0); };
const profA = (p, v) => { const a0 = Math.min(...p.as), a1 = Math.max(...p.as); return p.axis === 'y' ? a1 - v * (a1 - a0) : a0 + v * (a1 - a0); };
// the support distance (with the centre offset) of the smooth surface at azimuth th, axial a
const hAt = (p, th, a) => { const s = p.sec(a), F = LFR[p.axis], c = s.c || [0, 0]; return suppSec(s, th) + c[0] * Math.cos(th * D2R_) + c[1] * Math.sin(th * D2R_); };
export function smoothNy(p, th, a) {
  const F = LFR[p.axis], da = .02 * (Math.max(...p.as) - Math.min(...p.as)) + 1e-3;
  const lo = Math.min(...p.as), hi = Math.max(...p.as), a0 = Math.max(lo, a - da), a1 = Math.min(hi, a + da);
  const ha = (hAt(p, th, a1) - hAt(p, th, a0)) / Math.max(1e-6, a1 - a0);
  const ry = F.e1[1] * Math.cos(th * D2R_) + F.e2[1] * Math.sin(th * D2R_);
  return (ry - ha * F.A[1]) / Math.hypot(1, ha);
}
export const facetNy = (p, th) => { const F = LFR[p.axis]; return F.e1[1] * Math.cos(th * D2R_) + F.e2[1] * Math.sin(th * D2R_); };
const kIndex = K => Math.max(0, Math.min(KQ.n - 1, Math.round((K - KQ.k0) / KQ.dk)));
const nBands = p => Math.max(1, Math.floor((SWW / 4) * (p.H / 4) / KQ.n));
// the swatch cell UV (0..16 over the whole sprite) for a ledge / cap with factor K at axial a
export function swatchUV(name, K, a) {
  const p = PROF[name], nb = nBands(p), iv = Math.max(0, Math.min(nb - 1, Math.floor(profV(p, a) * nb))), idx = iv * KQ.n + kIndex(K);
  const cols = SWW / 4, cx = idx % cols, cy = Math.floor(idx / cols), W = spriteW(p);
  const u0 = (p.W + cx * 4 + 1) / W * 16, v0 = (cy * 4 + 1) / p.H * 16;
  return [u0, v0, u0 + 2 / W * 16, v0 + 2 / p.H * 16].map(x => Math.round(x * 1e4) / 1e4);
}
export const spriteW = p => p.W + SWW + (p.card ? p.card.P : 0);
export const facetFrac = name => PROF[name].W / spriteW(PROF[name]);
// the profile card region (silhouette cards, y lofts): u 0..1 = the distance 0 .. card.R from the axis, v as the wrap
export const cardUV = name => { const p = PROF[name], W = spriteW(p); return [(p.W + SWW) / W * 16, 0, 16, 16]; };
const clampRGB = (c, k) => [Math.min(255, c[0] * k), Math.min(255, c[1] * k), Math.min(255, c[2] * k), c[3] ?? 255];
// the card's half width: the polyline through the outer corners of the stepped outline (a section's vertex radius is
// the mean of its two station radii; a station's corner is the larger of the two sections there)
function cardR(p, a) {
  const as = p.as, rs = as.map(x => { const r = p.sec(x).r; return Array.isArray(r) ? r[0] : r; }), vr = as.slice(1).map((x, i) => (rs[i] + rs[i + 1]) / 2);
  const cs = as.map((x, i) => Math.max(i > 0 ? vr[i - 1] : 0, i < vr.length ? vr[i] : 0));
  const lo = as[0] < as[as.length - 1];
  for (let i = 0; i < as.length - 1; i++) { const x0 = as[i], x1 = as[i + 1]; if ((a - x0) * (a - x1) <= 0) { const u = (a - x0) / (x1 - x0 || 1); return cs[i] + (cs[i + 1] - cs[i]) * u; } }
  return 0;
}
function litPainter(name) {
  const p = PROF[name], W = spriteW(p), fw = p.W / W, sw = (p.W + SWW) / W, nb = nBands(p), g = p.g ?? .8, pre = p.pre ?? 1;
  const meanBand = Array.from({length: nb}, (_, iv) => { const v = (iv + .5) / nb, acc = [0, 0, 0, 0]; for (let j = 0; j < 16; j++) { const c = p.albedo((j + .5) / 16, v); for (let q = 0; q < 4; q++) acc[q] += (c[q] ?? 255) / 16; } return acc; });
  return (s, t) => {
    if (s < fw) {
      const u = s / fw, th = (u * p.n - .5) * 360 / p.n, k = Math.floor(u * p.n), thF = k * 360 / p.n, a = profA(p, t);
      const c = p.albedo(u, t);
      if (!c || c[3] === 0) return c || TRANSPARENT;
      return clampRGB(c, pre * litK(smoothNy(p, th, a), facetNy(p, thF), g));
    }
    if (s >= sw) {
      // the silhouette card: inside the smooth profile (half width at the card's azimuth = the support there), the
      // colour of a facet at the silhouette, a touch darker (the soft grey outline of the reference bells)
      const x = (s - sw) / (1 - sw) * p.card.R, a = profA(p, t), r = cardR(p, a);
      if (x > r) return TRANSPARENT;
      const c = p.albedo(p.card.u ?? .06, t);
      if (!c || c[3] === 0) return TRANSPARENT;
      return clampRGB(c, pre * (p.card.k ?? .92) * litK(smoothNy(p, p.card.th ?? 0, a), 0, g));
    }
    const px = Math.floor((s - fw) * W), py = Math.floor(t * p.H), idx = Math.floor(py / 4) * (SWW / 4) + Math.floor(px / 4), iv = Math.floor(idx / KQ.n), iK = idx % KQ.n;
    if (iv >= nb) return meanBand[nb - 1];
    return clampRGB(meanBand[iv], pre * (KQ.k0 + iK * KQ.dk));
  };
}

// ---- sprite helpers -------------------------------------------------------------------------------------------------
export const r16 = x => Math.min(512, Math.max(16, Math.ceil(x / 16) * 16));
// A card painter over a shape rect (blocks): u across (u0..u1), v up (v0 bottom .. v1 top) for the 'x' / 'z' planes;
// for the 'y' plane v runs along +Z from the sprite top (cardY / slab 'y').
const onRect = (rect, fn, plane = 'z') => (s, t) => fn(rect.u0 + s * (rect.u1 - rect.u0), plane === 'y' ? rect.v0 + t * (rect.v1 - rect.v0) : rect.v1 - t * (rect.v1 - rect.v0)) || TRANSPARENT;
// Bevel light of a signed-distance shape: rim 1 at the edge .. 0 at depth w; lit > 0 on the rim facing the upper left.
function bevel(sd, u, v, w = .05, e = .006) {
  const d = sd(u, v), gx = (sd(u + e, v) - sd(u - e, v)) / (2 * e), gy = (sd(u, v + e) - sd(u, v - e)) / (2 * e);
  return {d, rim: clamp(1 + d / w), lit: -.6 * gx + .8 * gy};
}
// Generic leaf / plate shader: base tone t0, a lit rim, a dark outline (outlined edge in blocks).
function shadeShape(sd, u, v, R, {t0 = .3, rimLit = .25, rimDark = .25, edge = .012, line = .75, w = .05, noise = .06, sx = 6} = {}) {
  const b = bevel(sd, u, v, w);
  if (b.d > 0) return null;
  let c = R(clamp(t0 + noise * (N.a(u * sx + 3, v * sx) - .5)));
  if (b.lit > 0) c = mix(c, R(0), rimLit * b.rim * b.lit); else c = mix(c, R(1), rimDark * b.rim * -b.lit);
  if (-b.d < edge) c = mix(c, R(1), line);
  return c;
}

// ---- 2D shapes (blocks) shared with the geometry ---------------------------------------------------------------------
// Each: {rect: {u0, u1, v0, v1}, sd(u, v)}. Plane conventions in the comments; the geometry passes plane / at.
const SHP = (rect, sd) => ({rect, sd});
// the 양육 hood arcs ([y, z] round the cap joint; the geometry lays strips along them, the cheeks follow them inward)
export const HOOD = {
  idle: [[-.06, .1], [.16, .08], [.32, -.04], [.38, -.22], [.32, -.42], [.16, -.58], [-.06, -.66], [-.22, -.62]],
  tilt: [[-.06, .1], [.18, .06], [.36, -.08], [.44, -.28], [.42, -.48], [.32, -.66], [.16, -.78], [.02, -.8]],
};
// the inner offset of an arc (toward the curl) as [u = z, v = y] points
const hoodIn = (P, k) => P.map(([y, z], i) => { const j = Math.min(P.length - 1, i + 1), m = Math.max(0, i - 1), ty = P[j][0] - P[m][0], tz = P[j][1] - P[m][1], L = Math.hypot(ty, tz);
  return [z - k * ty / L, y + k * tz / L]; });
const sdLens = (w, h, y0 = 0) => (u, v) => { const R = (h * h / 4 + w * w / 4) / w, c = R - w / 2; return Math.max(Math.hypot(u - c, v - y0 - h / 2), Math.hypot(u + c, v - y0 - h / 2)) - R; };
const pts = (...a) => a;
export const SH = {
  // 기본: a skirt foot in a radial plane (u = distance from the axis, v = height): hangs from the bell rim, curls up
  // a foot seen face-on (tangential plane, u across, v up from the ground along the card)
  // the curled sprout on the bell top (x plane: u = Z, v = Y)
  b_stem: SHP({u0: -.1, u1: .2, v0: 1.0, v1: 1.36}, stroke(bez([0, 1.02], [-.02, 1.28], [.09, 1.31], 12).concat([[.15, 1.28], [.16, 1.23]]), t => .03 - .016 * t).sd),
  // a jagged crown petal of the bag (tangential card; u across, v up from the neck)
  // a crumpled crown petal of the bag (v3 f900: pale papery petals tied at the neck, wavy tips)
  b_petal: SHP({u0: -.16, u1: .16, v0: 0, v1: .32}, (u, v) => { const w = .05 + .1 * Math.sin(Math.PI / 2 * clamp(v / .22)) - .03 * smooth(.24, .32, v), top = .27 + .04 * Math.cos(u * 30) - .03 * Math.abs(u) / .15;
    return Math.max(Math.abs(u + .015 * Math.sin(v * 25)) - w, -v, v - top); }),
  // 수호 shield: a vesica pane 0.6 x 1.4 and the small 3-leaf crown
  b_pane: SHP({u0: -.31, u1: .31, v0: 0, v1: 1.42}, sdLens(.6, 1.4, .01)),
  b_lcrown: SHP({u0: -.24, u1: .24, v0: 0, v1: .26}, sdUnion(sdLens(.11, .25, 0), (u, v) => sdLens(.1, .22, 0)(u * .8 + v * .6 - .02, -u * .6 + v * .8 + .04),
    (u, v) => sdLens(.1, .22, 0)(u * .8 - v * .6 + .02, u * .6 + v * .8 + .04))),
  // 양육: the S ribbon in profile (x plane: u = Z, v = Y) and its lower twist face-on (z plane: u = X)
  // the hood leaf in profile (x plane, cap frame: joint at the origin; it arches forward over the orb) and face-on
  // the hood cheeks (plane 'x': u = Z, v = Y round the cap joint): a crescent just inside the arc
  n_cheek: SHP({u0: -.8, u1: .2, v0: -.5, v1: .5}, stroke(hoodIn(HOOD.idle, .08).slice(1, -1), t => .02 + .06 * Math.sin(Math.PI * t)).sd),
  n_cheekT: SHP({u0: -.9, u1: .2, v0: -.4, v1: .55}, stroke(hoodIn(HOOD.tilt, .08).slice(1, -1), t => .02 + .06 * Math.sin(Math.PI * t)).sd),
  n_base: SHP({u0: -.21, u1: .21, v0: 0, v1: .56}, sdLens(.42, .56, 0)),
  n_frond: SHP({u0: -.11, u1: .11, v0: 0, v1: .56}, sdLens(.2, .56, 0)),
  // 수호: two helix ribbons (u across, v up; shape centre wanders sideways), the hem lobe, the death wisp
  g_lobe: SHP({u0: .14, u1: .62, v0: 0, v1: .34}, stroke(bez([.2, .32], [.3, .02], [.56, .05], 10), t => .09 - .05 * t).sd),
  g_wisp: SHP({u0: -.5, u1: .5, v0: 0, v1: 1.7}, sdUnion(stroke([[0, 0], [.08, .4], [-.06, .8], [.04, 1.1]], t => .14 - .08 * t).sd,
    stroke([[.04, 1.1], [-.14, 1.3], [-.3, 1.62]], t => .05 - .04 * t).sd, stroke([[.04, 1.1], [.2, 1.32], [.38, 1.58]], t => .05 - .04 * t).sd)),
  g_drape: SHP({u0: -.42, u1: .42, v0: 0, v1: 1.3}, (u, v) => { const w = .26 + .14 * (1 - v / 1.3), sc = .035 * Math.cos(u * 26); return Math.max(Math.abs(u) - w, -(v - .02 - sc), v - 1.3); }),
  // 둥지: a sepal wing in front view (z plane, wing frame: hinge at the origin, +u = outward), the eye ring
  w_wing: SHP({u0: -.06, u1: 1.36, v0: -.8, v1: .4}, sdUnion(stroke([[0, 0], [.22, .22], [.48, .28], [.74, .14], [.94, -.12], [1.06, -.42]], t => .13 - .07 * t).sd,
    stroke([[1.06, -.42], [1.18, -.6], [1.3, -.56]], t => .07 - .04 * t).sd, stroke([[1.04, -.4], [1.0, -.64], [1.08, -.74]], t => .06 - .035 * t).sd,
    stroke([[1.05, -.4], [1.22, -.42], [1.32, -.32]], t => .05 - .03 * t).sd)),
  w_ring: SHP({u0: -.25, u1: .25, v0: -.25, v1: .25}, (u, v) => Math.abs(Math.hypot(u, v) - .19) - .05),
  w_drop: SHP({u0: -.07, u1: .07, v0: -.22, v1: 0}, sdLens(.12, .22, -.22)),
  // 파괴: a cone spike as a triangle card (u across, v out from the shell)
  d_spike: SHP({u0: -.1, u1: .1, v0: -.04, v1: .26}, sdPoly(pts([-.085, -.04], [.085, -.04], [.006, .26], [-.006, .26]))),
  // 포식성: horn (triangle), the long front fin, the bottom sepals, the tail fin, the flare spikes, the bud petals
  p_horn: SHP({u0: -.2, u1: .2, v0: -.05, v1: .62}, sdPoly(pts([-.17, -.05], [.17, -.05], [.03, .62], [-.01, .6]))),
  p_hornS: SHP({u0: -.12, u1: .12, v0: -.04, v1: .32}, sdPoly(pts([-.1, -.04], [.1, -.04], [.01, .32]))),
  p_finL: SHP({u0: -.12, u1: .12, v0: -.05, v1: 1.1}, (u, v) => sdLens(.2, 1.12, -.04)(u + .03 * Math.sin(v * 3), v)),
  p_sepal: SHP({u0: -.14, u1: .14, v0: -.05, v1: .62}, sdPoly(pts([-.12, -.05], [.12, -.05], [.06, .3], [.01, .62], [-.04, .3]))),
  p_tail: SHP({u0: -.04, u1: .9, v0: -.5, v1: .5}, sdUnion(stroke([[0, 0], [.42, .18], [.86, .42]], t => .13 * Math.sin(Math.PI * Math.min(1, t * 1.15)) + .015).sd,
    stroke([[0, 0], [.42, -.18], [.86, -.42]], t => .13 * Math.sin(Math.PI * Math.min(1, t * 1.15)) + .015).sd)),
  p_flare: SHP({u0: -.07, u1: .07, v0: -.02, v1: .55}, sdPoly(pts([-.06, -.02], [.06, -.02], [.004, .55]))),
  p_petal: SHP({u0: -.42, u1: .42, v0: 0, v1: .78}, (u, v) => { const w = .4 * Math.sin(Math.PI * clamp(v / .78)) ** .7 + .02, notch = .06 * Math.max(0, Math.cos(u * 22)) * smooth(.1, 0, v); return Math.max(Math.abs(u) - w, -v + notch, v - .78); }),
  // the Heart: a leaf-flame sprout, a petal clump, a vine tendril, a vine stem strip
  h_tip: SHP({u0: -.16, u1: .16, v0: 0, v1: .62}, (u, v) => { const t = clamp(v / .62), w = .13 * Math.sin(Math.PI * Math.pow(t, .7)) + .008; return Math.abs(u - .05 * Math.sin(t * 4)) - w; }),
  h_petal: SHP({u0: -.3, u1: .3, v0: 0, v1: .36}, (u, v) => { const r = Math.hypot(u / .28, v / .34), lob = .12 * Math.cos(Math.atan2(v, u) * 7); return (r - 1 + lob) * .25; }),
  h_sprout: SHP({u0: -.12, u1: .12, v0: 0, v1: .7}, sdUnion(stroke([[0, 0], [.02, .3], [-.02, .5]], t => .025).sd, sdLens(.11, .22, .48), (u, v) => sdLens(.09, .18, 0)(u * .7 - (v - .28) * .7 - .02, u * .7 + (v - .28) * .7))),
  h_stem: SHP({u0: -.3, u1: .3, v0: -6.2, v1: .1}, sdUnion(stroke([[0, 0], [.06, -1.5], [-.08, -3.0], [.07, -4.5], [-.02, -6.1]], t => .08).sd,
    stroke([[.02, -1.0], [.2, -1.25], [.24, -1.45]], t => .03 - .02 * t).sd, stroke([[-.04, -3.6], [-.22, -3.85], [-.25, -4.0]], t => .03 - .02 * t).sd)),
  // the Heart cradle: a knobbly root finger (radial plane: u = distance from the centre, v = height) and a tall root arm
  wa_blade: SHP({u0: -.5, u1: .5, v0: 0, v1: 2.86}, (u, v) => { const t = clamp(v / 2.86), w = .46 * Math.sin(Math.PI * Math.pow(t, .8)) ** .8 + .01, c = .1 * Math.sin(t * 3.2);
    const blade = Math.abs(u - c) - w, win = (cx, cy) => Math.hypot((u - c - cx) / .1, (v - cy) / .3) - 1; return Math.max(blade, -Math.min(win(-.2, 1.35), win(.2, 1.85)) * .1); }),
  // 생명의 손 stalk: the hooked tip in profile (x plane: u = Z, v = Y, tip frame from the joint up)
  s_hook: SHP({u0: -.75, u1: .5, v0: -.1, v1: 1.55}, sdUnion(stroke(bez([0, 0], [.08, .9], [-.3, 1.3], 14).concat([[-.55, 1.22], [-.64, 1.02]]), t => .26 - .2 * t).sd,
    stroke([[-.3, 1.3], [-.12, 1.46], [.08, 1.42]], t => .09 - .06 * t).sd)),
  // the seed prop (a 'y'-axis lens), the dome sprout
  se_seed: SHP({u0: -.13, u1: .13, v0: 0, v1: .34}, sdLens(.24, .34, 0)),
  do_sprout: SHP({u0: -.3, u1: .3, v0: 0, v1: .7}, sdUnion(stroke([[0, 0], [.01, .5]], t => .03).sd, (u, v) => sdLens(.16, .34, 0)(u * .7 - (v - .3) * .7 - .06, u * .7 + (v - .3) * .7),
    (u, v) => sdLens(.16, .34, 0)(-u * .7 - (v - .3) * .7 - .06, -u * .7 + (v - .3) * .7), sdLens(.12, .24, .48))),
};

// ---- tile / wrap sprites (loft facets) ------------------------------------------------------------------------------
// bell wrap (u around 0..1, v top 0 .. bottom 1 of the loft): large faint facet diamonds (model_p3 §9: "faint large facets")
function bellPx(u, v) {
  const x = u * 6, y = v * 2.4, a = Math.floor(x + y), b = Math.floor(x - y), fa = (x + y) - a, fb = (x - y) - b;
  const id = h1(a * 7.3 + b * 3.1);
  let t = .08 + .12 * id + .26 * smooth(.25, 1, v) + .04 * (N.a(u * 9, v * 9) - .5);
  const seam = Math.min(fa, 1 - fa, fb, 1 - fb);
  if (seam < .04) t += .06 * (1 - seam / .04);
  let c = PAL.bell(t);
  c = mix(c, PAL.bell(0), .25 * (1 - smooth(0, .35, v)));                  // milky top
  if (v > .96) c = mix(c, PAL.bell(.85), .6);                             // rim line at the bottom
  return c;
}
// the bag wrap (loft along z: v from the back 0 .. the neck 1): the same facets + gathered folds toward the neck
function bagPx(u, v) {     // v 0 = the neck .. 1 = the round back
  let c = bellPx(u, .1 + v * .85);
  const fold = Math.abs(Math.sin(u * Math.PI * 10 + v * 2));
  if (v < .3) c = mix(c, PAL.bell(.6), .35 * smooth(.3, 0, v) * (1 - fold));
  return c;
}
const tealPx = (u, v, k = 0) => { let c = PAL.teal(.35 + .3 * (N.b(u * 6, v * 12) - .5) + k); const g = Math.abs(Math.sin(u * Math.PI * 8)); if (g < .08) c = sink(c, .25); return c; };
// a ribbon strap with pale rims along both edges (u across 0..1)
const ribbonPx = (u, v, R = PAL.teal, rim = PAL.pale, rw = .14, ra = .9) => {
  const e = Math.min(u, 1 - u);
  let c = R(.35 + .18 * (N.c(u * 4, v * 20) - .5) + .1 * Math.sin(v * 9));
  if (e < rw) c = mix(c, rim(.1 + .2 * e / rw), ra * smooth(rw, rw * .35, e));
  return c;
};
function shellPx(u, v) {     // 파괴: dark armour plates with pale grey bands at the seams
  const x = u * 8, y = v * 4, fx = x - Math.floor(x), fy = y - Math.floor(y);
  let c = PAL.destr(.3 + .14 * (N.d(u * 12, v * 12) - .5) + .08 * h1(Math.floor(x) * 3 + Math.floor(y) * 11));
  const band = Math.min(fx, 1 - fx);
  if (band < .09) c = mix(c, PAL.destr(.12), .75 * (1 - band / .09));
  if (Math.min(fy, 1 - fy) < .06) c = sink(c, .3);
  return c;
}
function stalkPx(u, v) {     // summoned stalk: pale grey shell with dark branching veins
  let c = PAL.stalk(.22 + .12 * (N.b(u * 6, v * 6) - .5) + .1 * v);
  const vein = Math.abs(N.e(u * 5 + v * 1.5, v * 7) - .5);
  if (vein < .022) c = mix(c, C('#47504A'), .8 * (1 - vein / .022));
  else if (vein < .04) c = mix(c, PAL.stalk(.6), .25);
  return c;
}
// glow ball (u, v over the sprite; r 0..1 from the centre)
const glowPx = (R, core = .35) => (u, v) => { const r = Math.hypot(u - .5, v - .5) * 2; return r > 1 ? TRANSPARENT : mix(R(0), R(.45), smooth(core, 1, r)); };

// ---- the sprites ------------------------------------------------------------------------------------------------------
// [w, h, painter (s, t in 0..1), translucent, owner]
const S = {};
const add = (name, w, h, fn, owner, translucent = false) => { if (S[name]) throw new Error('sprite ' + name + ' twice'); S[name] = [w, h, fn, translucent, owner]; };
// sprites registered by the geometry (facet-body masks: their polygons are computed there)
export const addSprite = add;
const shapeSprite = (name, shape, ppb, owner, fn, {plane = 'z', translucent = false, min = 16} = {}) => {
  const {rect} = shape, w = Math.max(min, r16((rect.u1 - rect.u0) * ppb)), h = Math.max(min, r16((rect.v1 - rect.v0) * ppb));
  add(name, w, h, onRect(rect, (u, v) => (shape.sd(u, v) > 0 ? null : fn(u, v)), plane), owner, translucent);
};
// a lit loft profile and its sprite (facet wrap + swatch column); the geometry builds the loft with litLoft(name)
function litProfile(name, p) {
  PROF[name] = p;
  registerWrap(name);
  add(name, spriteW(p), p.H, litPainter(name), p.owner, !!p.translucent);
}
// stations sampled along a profile with steps bounded in both the axis (da) and the radius (dr): the stair outline of
// a dome then has even steps (no wide terraces where the surface turns flat)
export function evenStations(a0, a1, rOf, da, dr, n0 = 400) {
  const out = [a0]; let last = a0, lr = rOf(a0);
  for (let i = 1; i <= n0; i++) { const a = a0 + (a1 - a0) * i / n0, r = rOf(a); if (Math.abs(a - last) >= da || Math.abs(r - lr) >= dr) { out.push(a); last = a; lr = r; } }
  if (Math.abs(out[out.length - 1] - a1) > 1e-6) { if (Math.abs(out[out.length - 1] - a1) < da * .35) out.pop(); out.push(a1); }
  return out.map(x => Math.round(x * 1e4) / 1e4);
}

// 기본 basic (14 k): the bell and the bag are lit lofts (profiles shared with the geometry)
// the bell (v4 f186 / f2310: a pale ghost-bell 1.15 b, the sides nearly straight, widest low, a round top): the dome
// radius over y; the skirt below y .3 is its own lit loft
export const smooth01 = x => { const t = Math.min(1, Math.max(0, x)); return t * t * (3 - 2 * t); };
// (v4 f2310 / v3 f900: an egg standing on its narrow end - the waist r .3 at y .14 over the skirt, widest .4 at y .66,
// a tall round top at 1.16; the skirt flares from r .29 at y .2 to the lobed hem r .49 on the ground)
export const bellR = y => (y < .66 ? .3 + .1 * Math.sin(Math.PI / 2 * smooth01((y - .14) / .52)) : .4 * Math.sqrt(Math.max(0, 1 - ((y - .66) / .5) ** 2)));
export const skirtR = y => (y > .1 ? .28 + .4 * (.32 - y) : .368 + (.1 - y));
// the bell's facet body (apep_org_geometry facetBody): pale cream-grey facets, a milky top, faint grey creases along
// the facet edges (v4 f186: the soft grey lines between the large facets); cls 1 = the skirt faces with a rounded lobe
// cut into the hem and darker lobe rims, cls 2 = the dark underside
export function bellFacetPx({el, cls}, s, t, d) {
  if (cls === 2) return PAL.bell(.9);
  const x = Math.abs(s - .5) * 2;
  if (cls === 1 || cls === 4) {
    // the lobes: V notches between them (the upper ring's lower corners, carried on through the tips), the tips' rounded
    // hem; a darker grey-blue rim along every cut edge (v3 f900: the outlined lobes)
    const nx = cls === 1 ? 1 - .3 * smooth01((t - .45) / .55) : .7 - .08 * t;            // the notch edge (half widths)
    const hem = cls === 4 ? 1 - .55 * Math.pow(x / nx, 2) : 2;
    if (x > nx || t > hem) return [0, 0, 0, 0];
    const e = Math.min((nx - x) * .5, cls === 4 ? (hem - t) * .4 : 1);
    let tt = .14 + .08 * t * (cls === 1 ? .5 : 1) + .04 * x * x + .03 * (N.a(s * 9, t * 5 + cls) - .5);
    if (cls === 4 || t > .45) tt += .3 * smooth(.06, 0, e);
    return PAL.bell(tt);
  }
  // cls 0 body / 3 bag: soft pillow facets (a touch darker toward the edges), a milky top
  let tt = .08 - .05 * el / 90 + .04 * t + .02 * (N.a(s * 7 + el, t * 7) - .5) + .08 * smooth(.06, 0, d);
  if (cls === 3) tt += .04;
  const c = PAL.bell(tt);
  return el > 80 && cls === 0 ? mix(c, PAL.bell(0), .3 * smooth(.45, .1, Math.hypot(s - .5, t - .5))) : c;
}
// the bag (v3 f900): a pear lying along z, the round belly behind (+z), the neck forward; level axis at y BAG.y
export const BAG = {zc: .13, a: .45, R: .45, y: .45, z0: -.62};
export const bagR = z => {
  const e = z0 => BAG.R * Math.sqrt(Math.max(0, 1 - ((z0 - BAG.zc) / BAG.a) ** 2));
  return z >= -.12 ? e(z) : .085 + (e(-.12) - .085) * smooth01((z - BAG.z0) / (-.12 - BAG.z0)) ** 1.5;
};
// loft ledges / caps face up: the game's up-face light is ~1.4x the side faces', so their tone is painted darker
const ledgeOf = (c, k = .7) => [c[0] * k, c[1] * k, c[2] * k, 255];
shapeSprite('bo_petal', SH.b_petal, 96, 'basic', (u, v) => { let c = shadeShape(SH.b_petal.sd, u, v, PAL.bell, {t0: .04 + .22 * smooth(.16, 0, v), edge: .006, w: .04, line: .35, rimDark: .15});
  const fold = Math.abs(Math.sin(u * 26 + v * 7)); if (fold < .14 && v > .06) c = mix(c, PAL.bell(.45), .28); return c; });
add('bo_glow', 16, 16, glowPx(PAL.core), 'basic');
add('bo_stemT', 16, 16, (u, v) => PAL.olive(.35 + .25 * (N.c(u * 4, v * 9) - .5) + .15 * Math.abs(u - .5)), 'basic');
// the 수호 shield panes (v4 f186): bright translucent lime leaves, a brighter rim and a faint midrib
shapeSprite('bo_pane', SH.b_pane, 22, 'basic', (u, v) => { const d = -SH.b_pane.sd(u, v); const rib = Math.abs(u) < .02 && v > .1 && v < 1.3;
  return A(mix(PAL.lime(.12), [250, 255, 200, 255], .6 * smooth(.07, 0, d) + (rib ? .3 : 0)), clamp(.32 + .5 * smooth(.08, 0, d) + (rib ? .2 : 0))); }, {translucent: true});
add('bo_bubble', 32, 16, (s, t) => A(mix(PAL.lime(.05), PAL.lime(.35), t), clamp(.08 + .55 * smooth(.25, 0, t) + .25 * smooth(.75, 1, t))), 'basic', true);
shapeSprite('bo_lcrown', SH.b_lcrown, 64, 'basic', (u, v) => shadeShape(SH.b_lcrown.sd, u, v, PAL.gem, {t0: .2, edge: .006, w: .02, line: .5}));

// 양육 nurturing (16 k)
// the 양육 ribbon (v3 f1240 / f1300): one broad dark-teal leaf ribbon with white rims, swept wide at its base, narrow
// where it twists, broad again under the hood; the sprite is the ribbon unrolled (u = across, W blocks; v = from its top
// NURT.top down to the floor), each twisted panel shows its slice
export const NURT = {top: 2.12, W: .66};
export const nurtW = y => .27 + .33 * Math.pow(smooth01(1 - y / .75), 1.4) + .18 * smooth01((y - .95) / .75) - .06 * smooth01((y - 1.85) / .3);
add('nu_rib', 32, 144, (s, t) => {
  const y = NURT.top * (1 - t), x = (s - .5) * NURT.W, hw = nurtW(y) / 2, e = hw - Math.abs(x);
  if (e < 0) return TRANSPARENT;
  let c = PAL.teal(.42 + .12 * (x / hw) + .06 * (N.c(s * 3, t * 30) - .5) + .08 * Math.sin(y * 7 + x * 9) * smooth(.04, .1, e));
  const vein = Math.abs(Math.sin((x / hw) * 3.2 + y * 1.5)); if (vein < .07 && e > .05) c = mix(c, PAL.teal(.2), .35);
  if (e < .034) c = mix(c, PAL.pale(.08 + 1.5 * e), .9 * smooth(.034, .012, e));
  return c;
}, 'nurt');
// the hood leaf along its arc (s across, t from the stalk to the drooping tip): narrow at the stalk, broad, a round tip
add('nu_hoodL', 32, 64, (s, t) => {
  const x = Math.abs(s - .5) * 2, hw = t < .6 ? .42 + .58 * smooth(0, .6, t) : Math.sqrt(Math.max(0, 1 - ((t - .6) / .4) ** 2));
  if (x > hw) return TRANSPARENT;
  const e = (hw - x) / Math.max(.05, hw);
  let c = PAL.hood(.12 + .14 * (1 - e) + .05 * (N.a(s * 6, t * 12) - .5) - .06 * smooth(.5, 1, t));
  if (Math.abs(Math.sin((x * .8 + t) * 15)) < .07 && e > .15) c = mix(c, PAL.hood(.4), .3);   // veins
  if (x < .04) c = mix(c, PAL.hood(.38), .4);                                               // midrib
  if (e < .1) c = mix(c, PAL.hood(.65), .7);                                               // rim
  return c;
}, 'nurt');
shapeSprite('nu_cheek', SH.n_cheek, 40, 'nurt', (u, v) => shadeShape(SH.n_cheek.sd, u, v, PAL.hood, {t0: .3, edge: .008, w: .03, rimDark: .4}));
shapeSprite('nu_cheekT', SH.n_cheekT, 40, 'nurt', (u, v) => shadeShape(SH.n_cheekT.sd, u, v, PAL.hood, {t0: .3, edge: .008, w: .03, rimDark: .4}));
shapeSprite('nu_base', SH.n_base, 40, 'nurt', (u, v) => { const b = bevel(SH.n_base.sd, u, v, .06); if (b.d > 0) return null; let c = PAL.teal(.38 + .25 * smooth(.5, 0, v) + .05 * (N.b(u * 9, v * 9) - .5));
  if (-b.d < .035) c = mix(c, PAL.pale(.15), .9); return c; });
shapeSprite('nu_frond', SH.n_frond, 40, 'nurt', (u, v) => { let c = shadeShape(SH.n_frond.sd, u, v, PAL.pale, {t0: .18, edge: .008, w: .03}); if (Math.abs(u) < .01) c = mix(c, PAL.pale(.5), .5); return c; });
add('nu_gem', 16, 16, (s, t) => { const d = Math.abs(s - .5) + Math.abs(t - .5); return d > .5 ? TRANSPARENT : PAL.gem(clamp(.1 + .7 * (s > .5 ? .6 : .2) * (t > .5 ? 1.2 : .6) + .2 * d)); }, 'nurt');
add('nu_orb', 16, 16, glowPx(PAL.core, .2), 'nurt');
add('nu_ring', 64, 16, (s, t) => A(mix(PAL.lime(0), PAL.lime(.35), t), clamp(.16 + .62 * smooth(.3, 0, t) + .22 * smooth(.7, 1, t) + .06 * Math.sin(s * Math.PI * 16) ** 8)), 'nurt', true);

// 수호 guarding (16 k)
const ribPale = (sd, k = 0) => (u, v) => { const b = bevel(sd, u, v, .08); let c = PAL.pale(.14 + .14 * (N.b(u * 4, v * 3) - .5) + k);
  if (b.lit < -.1) c = mix(c, PAL.teal(.25), .45 * b.rim); else if (b.lit > 0) c = mix(c, PAL.pale(0), .4 * b.rim * b.lit); if (-b.d < .012) c = mix(c, PAL.pale(.7), .6); return c; };
// the helix ribbons (s across, t from the tip 0 to the base 1): pale with a grey-teal shade on one half, a fine dark
// edge, narrowing to a point over the top tenth
add('gu_rib', 16, 128, (s, t) => {
  const x = (s - .5) * 2, hw = t < .14 ? Math.sqrt(t / .14) : 1;
  if (Math.abs(x) > hw) return TRANSPARENT;
  const e = hw - Math.abs(x);
  let c = PAL.pale(.12 + .08 * (N.b(s * 3, t * 30) - .5) + .1 * smooth(.2, 1, x));
  if (x > .35) c = mix(c, PAL.teal(.2), .35 * smooth(.35, .9, x));
  if (e < .16) c = mix(c, PAL.pale(.62), .7 * smooth(.16, .04, e));
  return c;
}, 'guard');
add('gu_sheath', 64, 32, (s, t) => { let c = tealPx(s, t, .12 * t); const sc = Math.abs(Math.sin(s * Math.PI * 6)); if (t > .82) c = mix(c, PAL.pale(.45), smooth(.82, .95, t) * (1 - sc * .5)); return c; }, 'guard');
shapeSprite('gu_lobe', SH.g_lobe, 56, 'guard', (u, v) => shadeShape(SH.g_lobe.sd, u, v, ramp(['#C8D2D6', '#A4B2BA', '#84949E', '#66767E', '#4A585E']), {t0: .25, edge: .01, w: .04}));
// the bud's drape wrap (u round 8 facets, v top 0 .. hem 1): pale folds, a wavy hem cut into soft lobes at the bottom
add('gu_drapeW', 64, 64, (s, t) => {
  const f = (s * 8) % 1, x = Math.abs(f - .5) * 2, hem = .9 + .07 * Math.cos(f * Math.PI * 2) - .03 * Math.cos(f * Math.PI * 6);
  if (t > hem) return TRANSPARENT;
  let c = PAL.pale(.1 + .16 * Math.abs(Math.sin(s * Math.PI * 24 + t * 2)) ** 2 + .12 * smooth(.3, 1, t) + .06 * x);
  if (hem - t < .03) c = mix(c, PAL.pale(.55), .6);
  return c;
}, 'guard');
shapeSprite('gu_drape', SH.g_drape, 32, 'guard', (u, v) => { let c = PAL.pale(.12 + .1 * Math.abs(Math.sin(u * 18)) + .2 * smooth(.4, 0, v)); if (-SH.g_drape.sd(u, v) < .02) c = mix(c, PAL.pale(.6), .5); return c; });
add('gu_bud', 48, 32, (s, t) => { let c = tealPx(s, t, -.04); const slit = Math.abs(s - .25) < .02 && t > .25 && t < .85; if (slit) c = PAL.core(.1); else if (Math.abs(s - .25) < .045 && t > .2 && t < .9) c = mix(c, PAL.core(.3), .5); return c; }, 'guard');
shapeSprite('gu_wisp', SH.g_wisp, 28, 'guard', (u, v) => { let c = PAL.black(.4 + .3 * (N.a(u * 6, v * 6) - .5)); if (-SH.g_wisp.sd(u, v) < .012) c = mix(c, C('#8E2A1E'), .5); return c; });
add('gu_gem', 16, 16, (s, t) => { const d = Math.abs(s - .5) * 1.2 + Math.abs(t - .5); return d > .55 ? TRANSPARENT : PAL.gem(clamp(.05 + (s < .5 ? .1 : .45) + (t > .5 ? .25 : 0))); }, 'guard');
add('gu_orb', 16, 16, glowPx(PAL.core, .15), 'guard');

// 둥지 nesting (12 k)
add('ne_cap', 64, 32, (s, t) => { let c = tealPx(s, t, -.06 + .1 * t); if (t > .9) c = mix(c, PAL.pale(.4), .5); return c; }, 'nest');
shapeSprite('ne_wing', SH.w_wing, 48, 'nest', (u, v) => { const b = bevel(SH.w_wing.sd, u, v, .05); let c = mix(PAL.pale(.2), C('#9DB3B0'), .45 * smooth(.2, .8, u));
  if (u > 1.0) c = mix(c, PAL.hood(.1), .7 * smooth(1.0, 1.1, u)); if (b.lit < 0) c = mix(c, PAL.teal(.3), .35 * b.rim); if (-b.d < .01) c = mix(c, PAL.pale(.75), .6); return c; });
shapeSprite('ne_ring', SH.w_ring, 64, 'nest', (u, v) => { const r = Math.hypot(u, v); let c = PAL.pale(.08 + .3 * smooth(.14, .24, r)); if (Math.abs(r - .19) > .04) c = mix(c, PAL.pale(.6), .4); return c; });
add('ne_orb', 16, 16, glowPx(PAL.core, .25), 'nest');
shapeSprite('ne_drop', SH.w_drop, 64, 'nest', (u, v) => shadeShape(SH.w_drop.sd, u, v, PAL.gem, {t0: .15, edge: .006, w: .03}));
add('ne_thorn', 16, 16, (s, t) => (Math.abs(s - .5) > .5 * t ? TRANSPARENT : PAL.teal(.5 + .3 * t)), 'nest');

// 파괴 destruction (8 k)
add('de_shell', 64, 32, shellPx, 'destr');
shapeSprite('de_spike', SH.d_spike, 64, 'destr', (u, v) => { let c = PAL.destr(.7 - .4 * clamp(v / .26) + (u > 0 ? .1 : -.05)); if (-SH.d_spike.sd(u, v) < .006) c = sink(c, .4); return c; });
add('de_face', 32, 32, (s, t) => { const r = Math.hypot(s - .5, t - .5) * 2; if (r > 1) return TRANSPARENT; return PAL.dface(clamp(.05 + .5 * smooth(.3, 1, r) - .15 * Math.cos(Math.atan2(t - .5, s - .5) * 6) * smooth(.6, .9, r))); }, 'destr');
add('de_beak', 16, 16, (s, t) => PAL.dface(.2 + .5 * t), 'destr');
add('de_rim', 32, 16, (s, t) => PAL.destr(.1 + .2 * t + .05 * Math.sin(s * 40)), 'destr');

// 포식성 predatory (20 k)
add('pr_hood', 64, 64, (s, t) => { let c = PAL.hood(.12 + .1 * (N.a(s * 6, t * 6) - .5) + .12 * smooth(.6, 1, Math.abs(s - .5) * 2));
  const wav = Math.abs(Math.sin(s * Math.PI * 7 + Math.sin(t * Math.PI * 5) * 1.2)); if (wav < .12) c = mix(c, PAL.hood(.6), .55 * (1 - wav / .12)); return c; }, 'pred');
add('pr_bowl', 64, 32, (s, t) => A(mix(PAL.fin(.15 + .2 * t), PAL.lime(.25), .3 * smooth(.85, 1, Math.abs(s - .5) * 2)), clamp(.62 + .3 * smooth(.85, 1, Math.abs(s - .5) * 2) + .2 * smooth(.85, 1, t))), 'pred', true);
shapeSprite('pr_horn', SH.p_horn, 48, 'pred', (u, v) => { let c = mix(C('#C9CBBE'), C('#8E9188'), clamp(v / .62) * .6 + (u > 0 ? .25 : 0)); if (-SH.p_horn.sd(u, v) < .01) c = mix(c, C('#5A5E56'), .6); return c; });
shapeSprite('pr_hornS', SH.p_hornS, 48, 'pred', (u, v) => mix(C('#C9CBBE'), C('#8E9188'), clamp(v / .32) * .6 + (u > 0 ? .25 : 0)));
shapeSprite('pr_fin', SH.p_finL, 40, 'pred', (u, v) => { const d = -SH.p_finL.sd(u, v); return A(mix(PAL.fin(.3), PAL.lime(.1), smooth(.04, 0, d)), clamp(.6 + .35 * smooth(.04, 0, d))); }, {translucent: true});
shapeSprite('pr_sepal', SH.p_sepal, 48, 'pred', (u, v) => { const d = -SH.p_sepal.sd(u, v); return A(mix(PAL.fin(.25), PAL.lime(.1), smooth(.03, 0, d)), clamp(.65 + .3 * smooth(.03, 0, d))); }, {translucent: true});
shapeSprite('pr_tail', SH.p_tail, 36, 'pred', (u, v) => { const d = -SH.p_tail.sd(u, v); return A(mix(PAL.fin(.3), PAL.lime(.1), smooth(.04, 0, d)), clamp(.6 + .35 * smooth(.04, 0, d))); }, {translucent: true});
add('pr_eye', 16, 16, (s, t) => { const r = Math.hypot(s - .5, t - .5) * 2; if (r > 1) return TRANSPARENT; return r < .42 ? C('#0B1414') : r < .6 ? PAL.eye(.05) : r < .86 ? PAL.eye(.75) : PAL.eye(.3); }, 'pred');
add('pr_core', 16, 16, glowPx(PAL.core, .2), 'pred');
add('pr_gem', 16, 16, (s, t) => { const d = Math.abs(s - .5) + Math.abs(t - .5) * .7; return d > .5 ? TRANSPARENT : PAL.gem(clamp(.08 + (s < .5 ? .1 : .4) + (t > .5 ? .2 : 0))); }, 'pred');
shapeSprite('pr_flare', SH.p_flare, 48, 'pred', (u, v) => A(mix(C('#FFFFF2'), PAL.lime(0), clamp(v / .55) * .6), 1));
shapeSprite('pr_petal', SH.p_petal, 40, 'pred', (u, v) => { let c = shadeShape(SH.p_petal.sd, u, v, PAL.hood, {t0: .14, edge: .012, w: .06});
  const st = Math.abs(Math.sin(u * 14 + v * 3)); if (st < .1) c = mix(c, PAL.hood(.55), .45); return c; });
add('pr_face', 32, 32, (s, t) => { let c = PAL.fin(.22 + .28 * t + .06 * (N.a(s * 5, t * 5) - .5)); const w = Math.abs(Math.sin(s * Math.PI * 8 + Math.sin(t * 6))); if (w < .1) c = mix(c, PAL.fin(.6), .35); return c; }, 'pred');

// the Heart of the Oasis (40 k): the bulb is painted as grey values and tinted per look (idle / egg / withered / blaze)
// the Heart bulb's facet faces (apep_org_geometry BULB_FACES): grey values (tinted per look), alpha ~0.86, a soft
// darker rib along every facet edge, a lighter milky middle; cls 1-3 = the faces toward the upper left (the specular
// band of v3 f270 / v4 f1650): whiter, the brightest with a white streak along the face
export function bulbFacetPx({cls, w, h}, s, t, d) {
  const e = smooth(.11, 0, d), mid = smooth(.5, 0, Math.hypot(s - .5, t - .5));
  let g = .9 + .04 * mid + [0, .03, .06, .09][cls] - .015 * e + .025 * (N.a(s * 5 + w, t * 5 + h) - .5);
  if (cls === 3) g += .08 * smooth(.16, 0, Math.abs((s - .5) * .8 + (t - .5) * .6));
  g = clamp(g);
  return A([255 * g, 255 * g, 252 * g, 255], .87);
}
add('he_swirl', 32, 32, (s, t) => { const x = s - .5, y = t - .5, r = Math.hypot(x, y) * 2, a = Math.atan2(y, x); if (r > 1) return TRANSPARENT;
  const arm = Math.abs(Math.sin(a * 2 + r * 7)); return A([200, 200, 196, 255], clamp(.5 * smooth(.25, 0, arm) * smooth(1, .4, r))); }, 'heart', true);
// the box faces of a root limb (apep_org_geometry rootLimb): u across the face (a rounded gradient, lit middle, dark
// edges), v along the root (long grain, a few pale knots)
const rootSidePx = R => (s, t) => { const x = Math.abs(s - .5) * 2, g = Math.abs(N.a(s * 2.5 + 7, t * 16) - .5);
  let c = R(.26 + .3 * x * x + .12 * (N.c(s * 2, t * 9) - .5));
  if (g < .035) c = sink(c, .28 * (1 - g / .035));
  if (N.d(s * 5 + 3, t * 7) > .8) c = mix(c, R(.1), .35);
  return c; };
add('he_rootS', 32, 64, rootSidePx(PAL.root), 'heart');
add('he_vineS', 16, 64, rootSidePx(PAL.vineL), 'heart');
// the faces of a root limb that look up (the game lights them 1.6x the sides): the same grain, darker
const darker = (f, k) => (s, t) => { const c = f(s, t); return [c[0] * k, c[1] * k, c[2] * k, c[3] ?? 255]; };
add('he_rootSU', 16, 32, darker(rootSidePx(PAL.root), .66), 'heart');
add('he_vineSU', 16, 32, darker(rootSidePx(PAL.vineL), .7), 'heart');
// the skin card of a root limb: the smooth tapered silhouette (stroke st, half width w(t)), a rounded gradient across
// it (the side toward the upper left lit), a dark outline, grain along; registered by the geometry per root
export function skinSprite(name, rect, st, w, ppb, owner, R = PAL.root, plane = 'z') {
  shapeSprite(name, {rect, sd: st.sd}, ppb, owner, (u, v) => {
    const n = st.near(u, v), hw = Math.max(1e-3, w(n.t)), x = clamp(n.d / hw), side = n.s > 0 ? 1 : -1;
    let c = R(.24 + .3 * x * x - .08 * side * x + .1 * (N.c(n.t * 12, x * 2 + side) - .5));
    const g = Math.abs(N.a(n.t * 20, x * 3 * side + 5) - .5); if (g < .03) c = sink(c, .25);
    if (x > .86) c = sink(c, .35 * smooth(.86, 1, x));
    return c;
  }, {plane});
}
shapeSprite('he_tip', SH.h_tip, 64, 'heart', (u, v) => { const d = -SH.h_tip.sd(u, v); return mix(PAL.tip(.05 + .3 * clamp(v / .62)), PAL.tip(0), smooth(.05, 0, d) * .5); });
shapeSprite('he_petal', SH.h_petal, 48, 'heart', (u, v) => shadeShape(SH.h_petal.sd, u, v, PAL.pale, {t0: .1, edge: .01, w: .05}));
shapeSprite('he_sprout', SH.h_sprout, 48, 'heart', (u, v) => shadeShape(SH.h_sprout.sd, u, v, PAL.gold, {t0: .2, edge: .008, w: .03}));
shapeSprite('he_stem', SH.h_stem, 20, 'heart', (u, v) => shadeShape(SH.h_stem.sd, u, v, PAL.vine, {t0: .4, edge: .015, w: .04, rimLit: .3}));

// 소생의 찬가 domes (24 k)
// the dome's facet faces (apep_org_geometry DOME_FACES; s right, t down the face, d blocks to its edge): translucent
// lime (alpha ~0.24), brighter toward the base, faint lighter seams; light leaf sprigs (w1 f184 / f330) rising from the
// base ring through the next one, three variants (cls) round the dome
export function domeFacetPx({el, cls, w, f}, s, t, d) {
  const ys = f.poly.map(p => p[1]), y0 = Math.min(...ys), y1 = Math.max(...ys);
  const low = el < 30, x = (s - .5) * w, y = y1 - t * (y1 - y0);          // y: the height above the base
  let c = mix(PAL.dome(.22), PAL.dome(.06), .6 * smooth(1.2, 0, y)), a = .22 + .12 * smooth(1.0, 0, y) + .04 * smooth(.08, 0, d);
  if (d < .05) c = mix(c, PAL.dome(0), .3);
  if (low) {
    // a sprig: a stem wandering up from the base, leaves alternating along it
    const ph = cls * 2.1, sx = .55 * Math.sin(y * 1.3 + ph) * (w / 3.6) + (cls - 1) * .35, dx = x - sx;
    const top = 2.7 - .45 * cls, stem = Math.abs(dx) < .04 && y < top;
    let leaf = false;
    for (let k = 0; k < 7; k++) { const ly = .3 + k * .36 + .1 * cls, side = k % 2 ? 1 : -1, lx = sx + side * .19, u = (x - lx) * side, v = y - ly - .1;
      if (ly < top - .1 && Math.hypot(u / .2, (v - .25 * u) / .085) < 1) leaf = true; }
    if (stem || leaf) { c = mix(PAL.dome(0), [250, 255, 210, 255], .45); a = .78 * (1 - .45 * smooth(1.2, top, y)) + .12; }
  }
  return A(c, a);
}
add('do_rim', 64, 16, (s, t) => A(mix([250, 255, 200, 255], PAL.dome(.15), t), clamp(.85 - .55 * t)), 'dome', true);
shapeSprite('do_sprout', SH.do_sprout, 40, 'dome', (u, v) => shadeShape(SH.do_sprout.sd, u, v, PAL.dome, {t0: .25, edge: .01, w: .04}));

// 둥지 wall blade (8 k)
shapeSprite('wa_blade', SH.wa_blade, 34, 'wall', (u, v) => { const d = -SH.wa_blade.sd(u, v), c0 = .1 * Math.sin(clamp(v / 2.86) * 3.2); const mid = Math.abs(u - c0) < .025;
  return A(mix(PAL.lime(.22 + .15 * clamp(v / 2.86)), mid ? PAL.lime(.7) : PAL.lime(0), mid ? .8 : .5 * smooth(.04, 0, d)), clamp(.58 + .32 * smooth(.05, 0, d) + (mid ? .25 : 0))); }, {translucent: true});

// 생명의 손 stalks (16 k)
add('st_bark', 64, 64, stalkPx, 'stalk');
shapeSprite('st_hook', SH.s_hook, 36, 'stalk', (u, v) => { const b = bevel(SH.s_hook.sd, u, v, .1); let c = stalkPx((u + 1) * .6, v * .5); if (b.lit > 0) c = mix(c, PAL.stalk(0), .3 * b.rim * b.lit); else c = mix(c, PAL.stalk(.8), .35 * b.rim * -b.lit); if (-b.d < .015) c = sink(c, .35); return c; });
add('st_cone', 16, 16, (s, t) => PAL.gold(.15 + .55 * t + (s > .5 ? .15 : 0)), 'stalk');

// the death seed (2 k)
shapeSprite('se_seed', SH.se_seed, 64, 'seed', (u, v) => { const d = -SH.se_seed.sd(u, v); return mix(PAL.gold(.25), PAL.gold(0), .6 * smooth(.08, 0, Math.hypot(u + .04, v - .22))) ; });

// ledge / cap tones of the lofts (darker: they face up)
add('ne_cap_l', 16, 16, (s, t) => ledgeOf(PAL.teal(.42)), 'nest');
add('gu_sheath_l', 16, 16, (s, t) => ledgeOf(PAL.teal(.42)), 'guard');
add('gu_bud_l', 16, 16, (s, t) => ledgeOf(PAL.teal(.36)), 'guard');
add('gu_drape_l', 16, 16, (s, t) => ledgeOf(PAL.pale(.2)), 'guard');
add('de_shell_l', 16, 16, (s, t) => ledgeOf(PAL.destr(.32)), 'destr');
add('pr_hood_l', 16, 16, (s, t) => ledgeOf(PAL.hood(.2)), 'pred');
add('pr_bowl_l', 16, 16, (s, t) => A(ledgeOf(PAL.fin(.3)), .75), 'pred', true);
add('pr_face_l', 16, 16, (s, t) => ledgeOf(PAL.fin(.3)), 'pred');
add('he_root_l', 16, 16, (s, t) => ledgeOf(PAL.root(.4 + .2 * N.c(s * 3, t * 3))), 'heart');
add('st_bark_l', 16, 16, (s, t) => ledgeOf(PAL.stalk(.3 + .1 * N.b(s * 3, t * 3))), 'stalk');
// loft tiles / wraps: texel density per block for the tileUV windows; wraps map u = facet k / n, v along the loft
for (const n of ['gu_drapeW', 'gu_sheath', 'gu_bud', 'ne_cap', 'de_shell', 'pr_hood', 'pr_bowl', 'pr_face', 'nu_ring', 'bo_bubble', 'do_rim', 'de_rim']) registerWrap(n);
registerTile('he_rootS', 32, 64, 16);
registerTile('he_vineS', 16, 64, 24);
registerTile('he_rootSU', 16, 32, 8);
registerTile('he_vineSU', 16, 32, 12);
registerTile('bo_stemT', 16, 16, 64);
registerTile('st_bark', 64, 64, 22);

export const orgSprites = () => Object.fromEntries(Object.entries(S).map(([k, [w, h, fn, tr]]) => [k, [w, h, fn, tr]]));
export const spriteOwner = () => Object.fromEntries(Object.entries(S).map(([k, v]) => [k, v[4]]));
export const spriteSizes = () => Object.fromEntries(Object.entries(S).map(([k, [w, h]]) => [k, [w, h]]));
export function paintOrgTextures(rp, only = null) {
  return paintSpriteSet(rp, 'assets/rlk/textures/mboss/apep_om', orgSprites(), spriteId, only);
}
