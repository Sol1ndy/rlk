// Painted sprites of the experimental field generator (실험성 역장 발생 장치, nameplate 브레게 프로토타입), the third
// mid-boss: tools/build_mboss_fieldgen_rig.mjs. Written to assets/rlk/textures/mboss/fieldgen/<name>.png and merged
// into the item atlas.
//
// Palette and proportions: scratchpad mb3/understand/model.md §3-§4 (the PDF render, the icon, v1-v4 frames). The
// device is cel-shaded brass: matte cream ceramic blocks over worn bronze, interlocked by a square wave with a
// glowing seam, gold facets, dark-red linings, cream clamps; violet only for the field.
//
// Kinds of sprite:
//   * tiles     shown whole on every facet / segment of a lathe or annulus (mboss_model_lib tile option): u across
//               the facet as seen from outside, v from the top (lathe vFrom) or from the outer edge (annulus).
//               The large walls come in light levels a-d (the light is baked per facet azimuth in the device frame,
//               the device turns to face the player), because the facets are unshaded;
//   * wraps     one sprite round a whole lathe (u = azimuth slice, v along the axis), e.g. the 8 alternating
//               gold facets of the spikes;
//   * polar     discs and annulus cards (u, v = x, z across the disc, alpha-cut outside the ring);
//   * cards     front-view pictures (the eyes, the medallion faces, the cog, the iris);
//   * glows     translucent (paintT), brightness-15 parts.
// Coordinates inside a painter: x, y in pixels (x right, y down) unless stated; every painter is sampled 4x4 (opaque,
// alpha cut at 0.5) or 3x3 (glows).
import {C, clamp, smooth, mix, fbm, TRANSPARENT, paintSpriteSet, rng} from './mboss_paint_lib.mjs';

// ---- palette (model.md §4) ------------------------------------------------------------------------------------------
const ramp = list => { const cs = list.map(C); return t => { const x = clamp(t) * (cs.length - 1), i = Math.min(cs.length - 2, Math.floor(x)); return mix(cs[i], cs[i + 1], x - i); }; };
export const RAMP = {
  cream: ramp(['#F7EDD8', '#EADAB9', '#D2BE9C', '#B19C79', '#7A6545', '#45311A']),
  bronze: ramp(['#EDC694', '#D09F64', '#B4814B', '#966537', '#744822', '#4E2C0F']),
  gold: ramp(['#FFF1C2', '#F8DA8A', '#EDBE52', '#D09A3A', '#A8772E', '#77501A']),
  dbronze: ramp(['#C9A77A', '#A17A4A', '#816651', '#624127', '#4E2D15', '#2E1A0C']),
  plum: ramp(['#9C7F84', '#7A5A62', '#5E414C', '#4A3140', '#3A2436', '#22141E']),
  red: ramp(['#C2785E', '#A04A33', '#8A3523', '#64200F', '#48180A', '#2E0E08']),
  silver: ramp(['#F2F1F2', '#D7D6D8', '#B8B7BA', '#989899', '#72695D', '#4E4840']),
  prot: ramp(['#F0E4C2', '#DCCBA3', '#BFAA7E', '#907C50', '#624C23', '#3F2F14']),
  violet: ramp(['#F2ECFF', '#D9CFF2', '#B6A2F0', '#896CC7', '#6A55C8', '#45286B']),
};
const P = {
  seamIdle: ['#FFF0C4', '#FFD081', '#F4C165', '#DBA978', '#C99468'].map(C),
  seamHot: ['#FFFFF4', '#FFF4C8', '#FFE9A0', '#FBD27A', '#F2B65C'].map(C),
  seamOff: ['#9C7C55', '#8A6A46', '#76583A', '#5E4630', '#46331F'].map(C),
  black: C('#100904'), white: [255, 255, 255, 255],
};
const T = x => [x[0], x[1], x[2], 255];
const scale = (c, k) => [c[0] * k, c[1] * k, c[2] * k, c[3] ?? 255];
const lift = (c, k) => mix(c, [255, 250, 238, 255], k);       // toward a warm white (highlights)
const sink = (c, k) => mix(c, [40, 22, 10, 255], k);           // toward a warm black (shadows, grooves)
const N = {a: fbm(11), b: fbm(23), c: fbm(37), d: fbm(51), e: fbm(67)};
// Light levels baked per facet azimuth (unshaded facets): a lit, b half, c turned away, d back.
export const LEVELS = {a: 1.0, b: .9, c: .8, d: .72};

// ---- tiny geometry helpers (pixel space) ------------------------------------------------------------------------------
const sat = x => clamp(x);
// distance-based bevel rim of a rectangle: returns {in, top, bot, left, right} edge weights for the cel highlights
function rect(x, y, x0, y0, x1, y1) {
  if (x < x0 || x > x1 || y < y0 || y > y1) return null;
  return {t: y - y0, b: y1 - y, l: x - x0, r: x1 - x};
}
// cel-shaded block face: base colour, a lit top/left rim, a dark bottom/right rim and an outline (pixels)
function block(c, e, {hi = 1.6, lo = 1.6, line = .9, hiK = .38, loK = .35, lineK = .55} = {}) {
  let o = c;
  if (e.t < hi) o = lift(o, hiK * (1 - e.t / hi));
  if (e.l < hi * .8) o = lift(o, hiK * .5 * (1 - e.l / (hi * .8)));
  if (e.b < lo) o = sink(o, loK * (1 - e.b / lo));
  if (e.r < lo * .8) o = sink(o, loK * .6 * (1 - e.r / (lo * .8)));
  const m = Math.min(e.t, e.b, e.l, e.r);
  if (m < line) o = sink(o, lineK * (1 - m / line));
  return o;
}
const grain = (c, x, y, k = .05, f = .08, n = N.a) => scale(c, 1 + k * (n(x * f, y * f) - .5) * 2);
const groove = (c, d, w = 1, k = .6) => (Math.abs(d) < w ? sink(c, k * (1 - Math.abs(d) / w)) : c);

// ---- square wave (the band joint) --------------------------------------------------------------------------------------
// Two waves per tile; the joint runs high (yHi) over the cream "teeth" and low (yLo) between them, with slanted risers
// (rise px wide). u in 0..1 across the facet; returns the joint height in v units and the signed distance in px.
const WAVE = {yHi: .22, yLo: .78, rise: .03, on0: .1, on1: .5};
function waveV(u) {
  const p = ((u % .5) + .5) % .5 * 2;                       // 0..1 within one wave
  const {yHi, yLo, rise, on0, on1} = WAVE, r = rise * 2;
  if (p < on0 - r / 2) return yLo;
  if (p < on0 + r / 2) return yLo + (yHi - yLo) * (p - on0 + r / 2) / r;
  if (p < on1 - r / 2) return yHi;
  if (p < on1 + r / 2) return yHi + (yLo - yHi) * (p - on1 + r / 2) / r;
  return yLo;
}
// distance (px) from (x, y) to the wave polyline over a tile W x H (H = the band height the wave lives in)
function waveDist(x, y, W, H, v0, v1) {
  let best = 1e9;
  const pts = [];
  for (let k = -1; k <= 2; k++) {
    const base = k * .5, {yHi, yLo, rise, on0, on1} = WAVE, r = rise;
    for (const [pu, pv] of [[on0 / 2 - r / 2, yLo], [on0 / 2 + r / 2, yHi], [on1 / 2 - r / 2, yHi], [on1 / 2 + r / 2, yLo]])
      pts.push([(base + pu) * W, (v0 + (v1 - v0) * pv) * H]);
  }
  for (let i = 0; i < pts.length - 1; i++) {
    const [ax, ay] = pts[i], [bx, by] = pts[i + 1], dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy;
    const t = clamp(((x - ax) * dx + (y - ay) * dy) / l2);
    best = Math.min(best, Math.hypot(x - ax - t * dx, y - ay - t * dy));
  }
  return best;
}

// =====================================================================================================================
// Ring (scale 2.4)
// =====================================================================================================================
// Outer band facet (1.37 x 0.77 b): a cream lip on top, cream ceramic blocks over bronze joined by the square wave
// (dark joint groove; ring_glow lays the glowing seam on it), an engraved recess line, the lower bronze strip with
// block joints and rivets, a dark foot. Band zone v 0.06..0.6.
function bandTile(W, H, level, inner = false) {
  const L = LEVELS[level];
  const B0 = .07, B1 = .62, G = .66;
  return (u, v) => {
    const x = u * W, y = v * H;
    let c;
    if (v < B0) {                                             // top lip (raised): a bright cream edge
      c = RAMP.cream(.12 + .5 * v / B0);
      if (y < 1.2) c = lift(c, .35);
      if (B0 * H - y < 1.0) c = sink(c, .45);
    } else if (v < B1) {
      const jv = B0 + (B1 - B0) * waveV(u), jy = jv * H, d = waveDist(x, y, W, H, B0, B1);
      const above = y < jy;
      if (above) {                                            // cream ceramic tooth
        c = RAMP.cream(.16 + .18 * (y - B0 * H) / ((B1 - B0) * H));
        // block joints: a vertical joint in each tooth's middle; inset panel line
        const p = ((u % .5) + .5) % .5 * 2;
        const jx = Math.abs(p - .215) * W / 2;
        if (jx < .7) c = sink(c, .35);
        c = grain(c, x, y, .04, .15, N.b);
      } else {                                                // bronze body
        c = RAMP.bronze(.32 + .3 * (y - jy) / Math.max(1, B1 * H - jy));
        c = grain(c, x, y, .06, .12, N.c);
        // engraved horizontal lines on the bronze
        if (Math.abs(y - (jy + B1 * H) / 2) < .5 && B1 * H - jy > 6) c = sink(c, .25);
      }
      // the joint: a dark groove 2.4 px wide with a lit lower lip (the cream steps down onto the bronze)
      if (d < 1.4) c = sink(RAMP.bronze(.85), .3 * (1 - d / 1.4));
      else if (d < 2.4 && !above) c = lift(c, .22 * (1 - (d - 1.4)));
      else if (d < 2.4 && above) c = sink(c, .18 * (1 - (d - 1.4)));
      if (B1 * H - y < 1.1) c = sink(c, .3);
    } else if (v < G) {                                       // recess line
      c = sink(RAMP.bronze(.6), .45);
    } else {                                                  // lower bronze strip: blocks, rivets, foot
      const s = (v - G) / (1 - G);
      c = RAMP.bronze(.22 + .45 * s);
      const bx = ((u * 2) % 1 + 1) % 1, e = {t: (v - G) * H, b: (1 - v) * H, l: bx * W / 2, r: (1 - bx) * W / 2};
      c = block(c, e, {hi: 1.6, lo: 1.8, line: .9, hiK: .42});
      c = grain(c, x, y, .06, .1, N.d);
      // rivets
      for (const rx of [.12, .38, .62, .88]) {
        const dd = Math.hypot(x - rx * W, y - (G + .45 * (1 - G)) * H);
        if (dd < 1.6) c = dd < 1.0 ? lift(RAMP.gold(.3), .1) : sink(c, .35);
      }
    }
    // the facet joint at the tile edges
    const ex = Math.min(x, W - x);
    if (ex < .8) c = sink(c, .35 * (1 - ex / .8));
    // wear: lighter edges near the top, dirt toward the foot
    c = scale(c, (inner ? .93 : 1) * L * (1.04 - .1 * v));
    return T(c);
  };
}
// The glowing seam over the joint (ring_glow): only the wave line, a 1.5 px core and a soft 3 px halo; the facet
// joints stay dark. look: idle / hot / off.
function seamTile(W, H, look) {
  const pal = look === 'hot' ? P.seamHot : look === 'off' ? P.seamOff : P.seamIdle;
  const B0 = .07, B1 = .62;
  return (u, v) => {
    const x = u * W, y = v * H, d = waveDist(x, y, W, H, B0, B1);
    const core = look === 'off' ? .75 : 1.0, halo = look === 'hot' ? 3.4 : look === 'off' ? 1.2 : 2.6;
    if (d > halo) return TRANSPARENT;
    const ex = Math.min(x, W - x);
    let a = d < core ? 1 : Math.pow(1 - (d - core) / (halo - core), 1.6) * (look === 'off' ? .5 : .75);
    a *= smooth(0, 1.5, ex);
    const c = d < core * .5 ? pal[0] : d < core ? pal[1] : mix(pal[2], pal[4], (d - core) / (halo - core));
    return [c[0], c[1], c[2], Math.round(255 * a)];
  };
}
// Top face segment (1.37 x 0.83 b, v 0 at the outer edge): the outer lip, cream ceramic panels between bronze
// brackets, engraved panel lines, the inner gold crenellated rim.
function topTile(W, H) {
  return (u, v) => {
    const x = u * W, y = v * H;
    let c;
    if (v < .1) {                                             // outer lip (continues the band's top lip)
      c = RAMP.cream(.1 + .3 * v / .1);
      if (y < 1) c = sink(c, .35);
    } else if (v < .78) {
      // two ceramic panels separated by a bronze bracket at the segment middle; brackets at the edges
      const bw = .09, ub = Math.abs(u - .5);
      if (ub < bw / 2 || u < bw / 2 || u > 1 - bw / 2) {
        c = RAMP.bronze(.35 + .25 * (v - .1) / .68);
        const ex = ub < bw / 2 ? bw / 2 - ub : Math.min(u, 1 - u) < bw / 2 ? bw / 2 - Math.min(u, 1 - u) : 0;
        if (ex * W < 1) c = sink(c, .3);
        // bolt heads on the brackets
        for (const by of [.28, .6]) if (Math.hypot((ub < bw / 2 ? u - .5 : u < .5 ? u : u - 1) * W, y - by * H) < 1.7) c = lift(RAMP.gold(.35), .1);
      } else {
        const x0 = u < .5 ? bw / 2 : .5 + bw / 2, x1 = u < .5 ? .5 - bw / 2 : 1 - bw / 2;
        c = RAMP.cream(.14 + .12 * (v - .1) / .68);
        c = block(c, {t: (v - .1) * H, b: (.78 - v) * H, l: (u - x0) * W, r: (x1 - u) * W}, {hi: 1.5, lo: 1.5, hiK: .3});
        // inset panel line
        const inset = Math.min((v - .1) * H, (.78 - v) * H, (u - x0) * W, (x1 - u) * W);
        if (Math.abs(inset - 4.2) < .55) c = sink(c, .22);
        c = grain(c, x, y, .04, .14, N.b);
      }
    } else {                                                  // inner gold crenellated rim
      const cren = Math.floor(u * 8) % 2 === 0;
      c = cren ? RAMP.gold(.28 + .3 * (v - .78) / .22) : RAMP.gold(.55 + .2 * (v - .78) / .22);
      const ex = Math.abs((u * 8) % 1 - .5) * W / 8;
      if (ex > W / 16 - .8) c = sink(c, .3);
      if ((v - .78) * H < 1.1) c = sink(c, .5);
      if (cren && (v - .78) * H < 2.6) c = lift(c, .2);
    }
    return T(scale(c, 1.0));
  };
}
// Underside of the band beyond the lower tier (narrow) and the lower tier's bottom (bomb-port plate): bronze with
// radial ribs, slots and bolts; baked a little darker (seen from below).
function bottomTile(W, H, tier) {
  return (u, v) => {
    const x = u * W, y = v * H;
    let c = RAMP.bronze(.42 + .25 * v);
    if (tier) {
      // cream gear ribs with dark slots (the lower tier reads as a gear from below)
      const p = (u * 4) % 1;
      if (v < .3) { c = p < .55 ? mix(RAMP.cream(.3), RAMP.bronze(.2), .35) : sink(RAMP.bronze(.62), .25); if (p < .55) c = block(c, {t: v * H, b: (.3 - v) * H, l: p * W / 4, r: (.55 - p) * W / 4}, {hi: 1.2, lo: 1.2}); }
      else {
        const ring = Math.abs(v - .62);
        if (ring < .025) c = sink(c, .4);
        if (Math.abs(u - .5) < .02) c = sink(c, .3);
      }
    } else {
      if (Math.abs(u - .5) < .03) c = sink(c, .3);
      for (const bx of [.25, .75]) if (Math.hypot(x - bx * W, y - .5 * H) < 1.6) c = lift(RAMP.gold(.4), .05);
    }
    c = grain(c, x, y, .07, .1, N.e);
    const ex = Math.min(x, W - x);
    if (ex < .8) c = sink(c, .3);
    return T(scale(c, .86));
  };
}
// Lower tier outer wall (1.25 x 0.36 b): cream gear ribs with dark slots between, a bronze band top and foot.
function tierTile(W, H, level) {
  const L = LEVELS[level];
  return (u, v) => {
    const x = u * W, y = v * H;
    let c;
    if (v < .16) c = sink(RAMP.bronze(.5), .1);
    else if (v > .86) c = RAMP.bronze(.6);
    else {
      const p = (u * 4 + .5) % 1;
      if (p < .62) {
        c = mix(RAMP.cream(.3 + .2 * (v - .16) / .7), RAMP.bronze(.2), .35);
        c = block(c, {t: (v - .16) * H, b: (.86 - v) * H, l: p * W / 4, r: (.62 - p) * W / 4}, {hi: 1.3, lo: 1.3, hiK: .35});
      } else c = sink(RAMP.bronze(.62), .25);
    }
    c = grain(c, x, y, .05, .12, N.c);
    return T(scale(c, L * .95));
  };
}
// Generic block faces: a cream ceramic block (tooth, keystone), a gold-capped tooth top, a cream grid panel (the
// keystone's 4 panels), the stepped bronze bell, plain bronze / dark bronze / gold / dark red / clamp tiles.
const faceTile = (W, H, base, opt = {}) => (u, v) => {
  const x = u * W, y = v * H;
  let c = base(.18 + .22 * v);
  c = block(c, {t: y, b: H - y, l: x, r: W - x}, {hi: 2.2 * W / 32, lo: 2.2 * W / 32, line: .9, hiK: .4, ...opt});
  return T(grain(c, x, y, .05, .14 * 32 / W, N.d));
};
function gridTile(W, H) {
  return (u, v) => {
    const x = u * W, y = v * H, cx = Math.floor(u * 2), cy = Math.floor(v * 2);
    const x0 = cx * W / 2, y0 = cy * H / 2;
    let c = RAMP.cream(.12 + .2 * v);
    c = block(c, {t: y - y0, b: y0 + H / 2 - y, l: x - x0, r: x0 + W / 2 - x}, {hi: 2.4, lo: 2.4, line: 1.2, hiK: .35, loK: .4});
    return T(grain(c, x, y, .04, .1, N.b));
  };
}
function pillarTile(W, H) {
  return (u, v) => {
    const x = u * W, y = v * H;
    let c = RAMP.cream(.1 + .25 * v);
    c = block(c, {t: y, b: H - y, l: x, r: W - x}, {hi: 2.4, lo: 2.4, line: 1.1, hiK: .4});
    const g = Math.abs(u - .5) * W;                        // the central vertical groove
    if (g < 3) c = sink(RAMP.bronze(.6), .25 + .3 * (1 - g / 3));
    if (Math.abs(g - 3) < .7) c = lift(c, .25);
    if (Math.abs(v - .38) * H < .7 && g > 3) c = sink(c, .3);  // horizontal joint
    return T(grain(c, x, y, .04, .1, N.c));
  };
}
function bellTile(W, H) {
  return (u, v) => {
    const x = u * W, y = v * H;
    let c = RAMP.bronze(.35 + .4 * v);
    c = block(c, {t: y, b: H - y, l: x, r: W - x}, {hi: 2, lo: 2.2, line: 1, hiK: .35, loK: .45});
    if (Math.abs(v - .5) * H < .6) c = sink(c, .3);
    for (const bx of [.25, .75]) if (Math.hypot(x - bx * W, y - .25 * H) < 1.6) c = lift(RAMP.gold(.3), .1);
    return T(grain(c, x, y, .06, .15, N.e));
  };
}
const plainTile = (W, H, base, t0 = .3, t1 = .6, k = .06, edge = true) => (u, v) => {
  const x = u * W, y = v * H;
  let c = base(t0 + (t1 - t0) * v);
  if (edge) { const ex = Math.min(x, W - x); if (ex < .7) c = sink(c, .25); }
  return T(grain(c, x, y, k, .15 * 32 / W, N.a));
};
// Engraved bronze: fine horizontal engraving lines and a dotted border (shafts, spindles, mount brackets).
const engravedTile = (W, H, base, t0 = .25, t1 = .55) => (u, v) => {
  const x = u * W, y = v * H;
  let c = base(t0 + (t1 - t0) * v);
  if (Math.abs(((y / H) * 6) % 1 - .5) < .06) c = sink(c, .25);
  if (Math.min(y, H - y) < 1.2) c = lift(c, .25);
  return T(grain(c, x, y, .05, .2, N.b));
};
// Round port discs (polar, alpha outside): the top eye-ports (dark red centre, orange rim) and the bomb ports (gold
// rim, dark core, a dim ember).
function portDisc(W, kind) {
  return (u, v) => {
    const r = Math.hypot(u - .5, v - .5) * 2, x = u * W, y = v * W;
    if (r > 1) return TRANSPARENT;
    let c;
    if (kind === 'eye') {
      if (r > .8) c = RAMP.bronze(.4 + .3 * (r - .8) / .2);
      else if (r > .62) c = mix(C('#F2B65C'), C('#C97A3A'), (r - .62) / .18);
      else c = mix(C('#3A0E06'), C('#7C3521'), smooth(0, .62, r));
      if (Math.abs(r - .8) < .03) c = sink(c, .4);
    } else {
      if (r > .7) c = RAMP.gold(.25 + .5 * (r - .7) / .3);
      else c = mix(C('#2A1206'), C('#743B01'), smooth(.1, .7, r));
      if (Math.abs(r - .7) < .03) c = sink(c, .5);
      if (r < .3) c = mix(c, C('#B5651D'), .4 * (1 - r / .3));
    }
    return T(grain(c, x, y, .04, .3, N.a));
  };
}
// Glowing rims of the ports (ring_glow): a ring with soft edges.
function portRim(W, look, kind) {
  const pal = look === 'hot' ? P.seamHot : look === 'off' ? P.seamOff : P.seamIdle;
  const R0 = kind === 'eye' ? .71 : .64, w = kind === 'eye' ? .09 : .08;
  return (u, v) => {
    const r = Math.hypot(u - .5, v - .5) * 2, d = Math.abs(r - R0);
    if (d > w * 1.8 || r > .98) return TRANSPARENT;
    const a = d < w * .6 ? 1 : 1 - (d - w * .6) / (w * 1.2);
    const c = mix(pal[0], pal[3], smooth(0, w * 1.8, d));
    let al = a * (look === 'off' ? .6 : .95);
    // the bomb ports glow inside too when hot
    return [c[0], c[1], c[2], Math.round(255 * al)];
  };
}
function portCore(W, look) {
  // inner glow of a bomb port (hot: a bright ember; idle: dim; off: transparent)
  return (u, v) => {
    const r = Math.hypot(u - .5, v - .5) * 2;
    if (r > .62 || look === 'off') return TRANSPARENT;
    const k = look === 'hot' ? 1 : .35, c = mix(C('#FFF4C8'), C('#F2B65C'), r / .62);
    return [c[0], c[1], c[2], Math.round(255 * k * (1 - smooth(.3, .62, r)))];
  };
}

// =====================================================================================================================
// Gold, spikes, iris
// =====================================================================================================================
// 8 alternating facets (bright gold #EBC263 / pale cream-gold #EBD9B1) for a lathe of n = 8 (or n = 4 with 2 stripes
// per facet): each facet has a centre ridge highlight and dark facet edges; v runs from the base (0) to the tip (1),
// with a polished band near the base. Used by the rim spikes, the iris spike, the dagger and the missiles.
function gold8(W, H, {stripes = 8, base = .0, tipDark = .15} = {}) {
  return (u, v) => {
    const x = u * W, y = v * H, k = Math.floor(u * stripes), f = (u * stripes) % 1;
    const bright = k % 2 === 0;
    let c = bright ? mix(C('#F4CF6C'), C('#E1B04E'), f) : mix(C('#F3E6C4'), C('#DCC79A'), f);
    // a ridge highlight near each facet's leading edge, a dark trailing edge
    if (f < .12) c = lift(c, .35 * (1 - f / .12));
    if (f > .9) c = sink(c, .3 * (f - .9) / .1);
    c = mix(c, sink(c, .25), tipDark * v);
    if (v > base && v < base + .06) c = lift(c, .2);
    return T(grain(c, x, y, .035, .2, N.c));
  };
}
// Ribbed collar rings (cream/gold), tile: 3 ribs along v.
function collarTile(W, H) {
  return (u, v) => {
    const x = u * W, y = v * H, p = (v * 3) % 1;
    let c = p < .62 ? RAMP.gold(.18 + .3 * p) : RAMP.cream(.3 + .3 * (p - .62));
    if (p < .08) c = lift(c, .35);
    if (p > .55 && p < .62) c = sink(c, .5);
    const ex = Math.min(x, W - x);
    if (ex < .7) c = sink(c, .25);
    return T(grain(c, x, y, .04, .2, N.d));
  };
}
// The keystone iris (front of the band), 64 px over 1.1 b: a gear/ray frame round the eye.
//   shut  a gold sunburst fan of radial ribs covers the eye;
//   open  a cream ring round a red-orange pupil (deep centre) with a glint;
//   hot   white-gold ring and a bright pupil core (charging, 지면 충격).
function irisCard(W, look) {
  return (u, v) => {
    const dx = u - .5, dy = v - .5, r = Math.hypot(dx, dy) * 2, a = Math.atan2(dy, dx);
    if (r > 1) return TRANSPARENT;
    // gear frame: 12 rays/teeth at the rim
    const tooth = (Math.cos(a * 12) > .25) ? 1 : 0;
    if (r > .86) {
      if (!tooth) return TRANSPARENT;
      let c = RAMP.gold(.3 + .3 * (r - .86) / .14);
      if (r > .96) c = sink(c, .3);
      return T(c);
    }
    if (r > .74) {
      let c = RAMP.bronze(.3 + .4 * (r - .74) / .12);
      if (Math.abs(r - .74) < .02) c = sink(c, .5);
      if (Math.cos(a * 24) > .92) c = sink(c, .3);
      return T(c);
    }
    if (look === 'shut') {
      // sunburst fan: 16 radial gold ribs meeting at a small boss
      const f = ((a / (Math.PI * 2)) * 16 % 1 + 1) % 1;
      let c = f < .5 ? RAMP.gold(.15 + .4 * r) : RAMP.gold(.45 + .35 * r);
      if (f < .08 || (f > .5 && f < .56)) c = lift(c, .3);
      if (r < .14) c = r < .1 ? RAMP.gold(.1) : sink(RAMP.gold(.5), .3);
      return T(c);
    }
    const hot = look === 'hot';
    if (r > .5) {                                               // cream ring
      let c = hot ? mix(C('#FFFBEA'), C('#FCE7B0'), (r - .5) / .24) : mix(C('#FCE6C6'), C('#DAAD8B'), Math.pow((r - .5) / .24, 1.5));
      if (r > .7) c = sink(c, .15);
      if (dy < -.1 && r < .62 && !hot) c = lift(c, .25);
      return T(c);
    }
    // pupil: red-orange, deep centre, a bright glint upper-left
    let c = hot ? mix(C('#FFFFF0'), C('#FBD27A'), smooth(0, .5, r)) : mix(C('#3A140E'), C('#B1846A'), smooth(.05, .5, r));
    if (!hot) c = mix(c, C('#975942'), .35 * smooth(.15, .4, r));
    if (Math.abs(r - .5) < .03) c = sink(c, .5);
    const g = Math.hypot(dx + .1, dy + .11);
    if (g < .055) c = lift(c, .8 * (1 - g / .055));
    return T(c);
  };
}

// =====================================================================================================================
// Core
// =====================================================================================================================
// Plum shell wrap (16 facets round, v pole to pole): dark plum with lighter bronze meridian ribs every 45 degrees,
// a latitude rib, small cream rivets; the wrap is lit from the front-upper-left (the eye side faces the player).
function shellWrap(W, H) {
  return (u, v) => {
    const x = u * W, y = v * H, az = u * 2 * Math.PI, lat = (v - .5) * Math.PI;
    const front = .5 + .5 * Math.cos(az - .5), up = .5 - .5 * Math.sin(lat);
    let c = RAMP.plum(.7 - .32 * front * up - .1 * front);
    // meridian ribs
    const m = (u * 8) % 1, md = Math.min(m, 1 - m) * W / 8;
    if (md < 1.6) c = mix(RAMP.bronze(.4 + .3 * (1 - front)), C('#CFB895'), .3 * (1 - md / 1.6) * front);
    else if (md < 2.4) c = sink(c, .3);
    // latitude rib at the equator and two tropics
    for (const lv of [.5, .3, .7]) {
      const dd = Math.abs(v - lv) * H;
      if (dd < 1.1) c = mix(c, RAMP.bronze(.45), .7 * (1 - dd / 1.1));
    }
    // glossy highlight band
    c = lift(c, .12 * Math.pow(front * up, 3));
    return T(grain(c, x, y, .05, .1, N.a));
  };
}
// The eye frame: a cream gear-tooth ring (annulus segments, tile per segment: one tooth each), and its tube wall.
function eyeFrameTile(W, H) {
  return (u, v) => {
    const x = u * W, y = v * H;
    let c = RAMP.cream(.08 + .25 * v);
    const tooth = Math.abs(u - .5) < .28 && v < .45;
    if (!tooth && v < .45) return TRANSPARENT;                 // gaps between the teeth (the frame's outer edge)
    c = block(c, {t: y, b: H - y, l: tooth ? (u - .22) * W : x, r: tooth ? (.78 - u) * W : W - x}, {hi: 1.4, lo: 1.4, line: .8, hiK: .45});
    if (Math.abs(v - .45) * H < .6) c = sink(c, .25);
    return T(c);
  };
}
// The core eye glow card (pupil + glow ring + the orange streak), per look:
//   idle   gold ring #F6E998 -> #AE6A11, black pupil, orange streak (the icon);
//   charge white-gold ring and a hot core; field red-orange (#FBE7A3 -> #833810, dark-red pupil);
//   dim    amber, low (groggy, dormant); gold: the exposed gold sphere with the white-gold glyph (an ε mark).
function eyeGlow(W, look) {
  const pal = {
    idle: {hi: '#FBF5D8', ring: '#F6E998', mid: '#F2DA8E', lo: '#CFA659', deep: '#AE6A11', pupil: '#100904', streak: '#FF9A3A'},
    charge: {hi: '#FFFFFF', ring: '#FFF4C8', mid: '#FFE9A0', lo: '#FBD27A', deep: '#F2B65C', pupil: '#5A2A08', streak: '#FFF0B0'},
    field: {hi: '#FBE7A3', ring: '#E8B57A', mid: '#C98A4A', lo: '#9D5E2F', deep: '#833810', pupil: '#3A0E06', streak: '#FFB45A'},
    dim: {hi: '#C8A070', ring: '#A87C48', mid: '#8A6234', lo: '#6A4422', deep: '#4A2A12', pupil: '#120804', streak: '#7A4A20'},
  }[look];
  const c = Object.fromEntries(Object.entries(pal).map(([k, s]) => [k, C(s)]));
  return (u, v) => {
    const dx = u - .5, dy = v - .5, r = Math.hypot(dx, dy) * 2, a = Math.atan2(dy, dx);
    if (r > 1) return TRANSPARENT;
    let o;
    if (r > .6) {                                               // the glow ring, brighter at the top
      const t = Math.abs(r - .8) / .2, lit = .5 - .5 * Math.sin(a);
      o = mix(c.ring, c.deep, smooth(0, 1, t));
      o = mix(o, c.hi, .5 * (1 - t) * lit);
      if (r > .96) o = mix(o, c.deep, .6);
    } else {                                                    // the pupil with the streak
      o = mix(c.pupil, mix(c.pupil, c.deep, .5), smooth(.35, .6, r));
      const sd = Math.abs((dy + .03) * Math.cos(.35) - dx * Math.sin(.35));      // a streak across the pupil
      const along = dx * Math.cos(.35) + (dy + .03) * Math.sin(.35);
      if (sd < .05 && Math.abs(along) < .3) o = mix(o, c.streak, (1 - sd / .05) * (1 - Math.abs(along) / .3));
      if (look === 'charge') o = mix(o, c.mid, .5 * (1 - r / .6));
    }
    return T(o);
  };
}
// The arch (vertical gear ring): bronze outer tile with tick marks, dark-red lining, bronze sides, cream clamps.
function archOut(W, H) {
  return (u, v) => {
    const x = u * W, y = v * H;
    let c = RAMP.dbronze(.42 + .25 * Math.abs(v - .35));
    if (Math.abs(u - .5) * W < .8) c = sink(c, .35);
    if (Math.abs(u - .25) * W < .5 || Math.abs(u - .75) * W < .5) if (v < .3 || v > .7) c = lift(RAMP.cream(.4), .0);
    if (Math.min(y, H - y) < 1.2) c = lift(c, .2);
    return T(grain(c, x, y, .06, .2, N.a));
  };
}
const archIn = (W, H) => (u, v) => {
  const x = u * W, y = v * H;
  let c = RAMP.red(.45 + .2 * Math.abs(v - .5));
  if (Math.min(y, H - y) < 1.2) c = sink(c, .35);
  if (Math.abs(u - .5) * W < .6) c = sink(c, .25);
  return T(grain(c, x, y, .06, .25, N.c));
};
// Brim: a polar card (128 px over the whole disc): tan grooved annulus from the sphere (r 0.6) out to the rim, five
// concentric grooves, dark tick marks on the outer band, a dark rim edge; transparent inside r 0.56.
function brimCard(W) {
  return (u, v) => {
    const dx = u - .5, dy = v - .5, r = Math.hypot(dx, dy) * 2, a = Math.atan2(dy, dx);
    if (r > 1 || r < .56) return TRANSPARENT;
    let c = RAMP.bronze(.12 + .35 * Math.abs(Math.sin(a * .5 + .6)) * .5 + .15 * (1 - r));
    c = mix(c, C('#D6B693'), .45);
    const g = ((r - .56) / .44 * 6) % 1;
    if (g < .14) c = sink(c, .32);
    else if (g < .24) c = lift(c, .18);
    if (r > .9 && Math.cos(a * 48) > .82) c = sink(c, .55);            // tick marks on the rim band
    if (r > .97) c = sink(c, .4);
    return T(grain(c, u * W, v * W, .05, .25, N.d));
  };
}
// Orbit wire (polar card): a thin dark-bronze ring; the bead is a box.
function wireCard(W) {
  return (u, v) => {
    const r = Math.hypot(u - .5, v - .5) * 2;
    const d = Math.abs(r - .955);
    if (d > .03) return TRANSPARENT;
    let c = RAMP.dbronze(.45 + .3 * d / .03);
    if (d < .008) c = lift(c, .2);
    return T(c);
  };
}
// Red side pads (cushions) and the cream clamp / Y bracket.
const padTile = (W, H) => (u, v) => {
  const x = u * W, y = v * H, e = Math.min(x, W - x, y, H - y);
  let c = RAMP.red(.25 + .3 * v);
  if (e < 2) c = sink(c, .3 * (1 - e / 2));
  if (Math.abs(u - .5) * W < .8) c = sink(c, .25);
  if (v < .2) c = lift(c, .12);
  return T(grain(c, x, y, .06, .2, N.b));
};

// =====================================================================================================================
// Glows: the charge sphere, the gold flash, the field bubble with its crack stages, the burst
// =====================================================================================================================
// Radial glow card (crossed cards make a ball of light from any side).
function radialGlow(W, inner, outer, alpha = .8, rim = 0) {
  const ci = C(inner), co = C(outer);
  return (u, v) => {
    const r = Math.hypot(u - .5, v - .5) * 2;
    if (r > 1) return TRANSPARENT;
    const c = mix(ci, co, smooth(0, 1, r));
    let a = alpha * Math.pow(1 - r, 1.3);
    if (rim) a = Math.max(a, rim * Math.exp(-Math.pow((r - .82) / .08, 2)));
    return [c[0], c[1], c[2], Math.round(255 * clamp(a))];
  };
}
// Bubble shell wrap (a turned sphere, u = azimuth, v pole to pole): translucent white-gold with a brighter rim
// toward the poles, and the crack network of the 20-hit meter: stage 0 clean, 1-3 growing networks of white cracks
// (each stage adds branches); burst: bright, shattered.
const CRACKS = (() => {
  // glass cracks on the front hemisphere (u near 0 / 1 faces the eye side), in sphere units: x along the equator
  // (2 pi per turn), y up (+-1); each impact emits jagged radial cracks and concentric arcs, stage by stage
  const R = rng(4471), out = [];
  const jag = (x0, y0, ang, len, step = .07) => {
    const pts = [[x0, y0]];
    let x = x0, y = y0, a = ang;
    for (let d = 0; d < len; d += step) { a += (R() - .5) * .55; x += Math.cos(a) * step; y += Math.sin(a) * step; pts.push([x, y]); }
    return pts;
  };
  const impact = (lvl, x, y, n, len, a0 = 0) => {
    for (let i = 0; i < n; i++) {
      const a = a0 + i * 2 * Math.PI / n + (R() - .5) * .5, L = len * (.6 + .6 * R());
      out.push({lvl, pts: jag(x, y, a, L)});
      if (R() < .55) out.push({lvl: Math.min(3, lvl + 1), pts: jag(x + Math.cos(a) * L * .55, y + Math.sin(a) * L * .55, a + (R() < .5 ? .9 : -.9), L * .45)});
    }
    for (const [rr, l2] of [[len * .35, lvl], [len * .7, Math.min(3, lvl + 1)]]) {   // concentric pieces
      const k0 = R() * 6.28, span = 1.6 + R();
      const pts = [];
      for (let t = 0; t <= 1; t += .1) { const a = k0 + span * t; pts.push([x + Math.cos(a) * rr * (1 + (R() - .5) * .15), y + Math.sin(a) * rr * (1 + (R() - .5) * .15)]); }
      out.push({lvl: l2, pts});
    }
  };
  impact(1, .35, .15, 5, .75, .3);
  impact(2, -.45, -.25, 5, .7, 1.1);
  impact(2, .05, .6, 4, .55, 2.0);
  impact(3, -.2, .45, 5, .6, .7);
  impact(3, .55, -.5, 5, .6, 2.6);
  impact(3, -.75, .25, 4, .5, 0);
  impact(3, .9, .35, 4, .5, 1.5);
  return out;
})();
// distance (sphere units) from wrap point (u, v) to the cracks shown at stage s
function crackDist(u, v, stage) {
  const y = 1 - 2 * v, c = Math.sqrt(Math.max(.05, 1 - y * y));
  let x = (((u + .5) % 1) - .5) * 2 * Math.PI * c;            // around the front, scaled to the circle at this height
  let best = 1e9;
  for (const {lvl, pts} of CRACKS) {
    if (lvl > stage) continue;
    for (let i = 0; i < pts.length - 1; i++) {
      const [ax, ay] = pts[i], [bx, by] = pts[i + 1], dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy || 1e-9;
      const t = clamp(((x - ax) * dx + (y - ay) * dy) / l2);
      best = Math.min(best, Math.hypot(x - ax - t * dx, y - ay - t * dy));
    }
  }
  return best;
}
function bubbleWrap(W, H, stage) {
  const px = 2 / H;                                            // sphere units per pixel (v spans the height 2)
  return (u, v) => {
    const lat = Math.abs(v - .5) * 2;
    let c = mix(C('#FFFBF0'), C('#F1E2BE'), lat);
    let a = .26 + .34 * Math.pow(lat, 2.2);
    if (stage === 'burst') { c = mix(C('#FFFFFF'), C('#FFE9A0'), lat); a = .6 + .3 * lat; }
    const s = stage === 'burst' ? 3 : stage;
    if (s > 0) {
      const d = crackDist(u, v, s) / px, core = .75 + .2 * s, halo = 3.0;
      if (d < core) { c = C('#FFFFFF'); a = Math.max(a, .97); }
      else if (d < halo) { const f = (d - core) / (halo - core); c = mix(C('#FFFFFF'), C('#FFF0C0'), f); a = Math.max(a, .62 * (1 - f)); }
    }
    return [c[0], c[1], c[2], Math.round(255 * clamp(a))];
  };
}
// The exposed gold sphere (the field breaks and the core shows: gold with a white-gold ε glyph) as a shell wrap.
function goldShell(W, H) {
  return (u, v) => {
    const x = u * W, y = v * H, lat = Math.abs(v - .5) * 2;
    let c = mix(C('#FFF0B8'), C('#E2AE66'), lat);
    let a = .55 + .25 * lat;
    // the glyph on the front (u near 0 / 1)
    const du = ((u + .5) % 1) - .5, gx = du * 4, gy = (v - .5) * 2;
    const rr = Math.hypot(gx, gy);
    if (Math.abs(rr - .5) < .07 && gx < .2) { c = C('#FFFFFF'); a = .95; }
    if (Math.abs(gy) < .05 && gx > -.5 && gx < .2) { c = C('#FFFFFF'); a = .95; }
    return [c[0], c[1], c[2], Math.round(255 * a)];
  };
}

// =====================================================================================================================
// Halo pair
// =====================================================================================================================
// Halo outer wall (tile per facet, 0.6 x 0.14 b): copper-brown with a rose highlight, a dark joint at the facet edge
// (16 joints), a gold glow line along the inner (lower) edge; violet look: violet with a pale lilac rim.
function haloWall(W, H, violet, inner = false) {
  return (u, v) => {
    const x = u * W, y = v * H;
    let c;
    if (violet) c = mix(RAMP.violet(.35 + .3 * v), C('#E6DDF6'), v < .2 ? .4 : 0);
    else c = mix(RAMP.dbronze(.3 + .3 * v), C('#A6626E'), .18 * (1 - v));
    if (inner) c = violet ? mix(C('#D9CFF2'), C('#A18CEA'), v) : mix(C('#FFE6A8'), C('#E3BF73'), v);   // the inner glow
    const ex = Math.min(x, W - x);
    if (ex < 1.1 && !inner) c = sink(c, .45 * (1 - ex / 1.1));
    if (y < 1 && !inner) c = lift(c, .25);
    return T(c);
  };
}
function haloFace(W, H, violet) {
  return (u, v) => {
    const x = u * W, y = v * H;
    let c = violet ? RAMP.violet(.3 + .25 * v) : mix(RAMP.dbronze(.3 + .25 * v), C('#A6626E'), .15);
    if (v > .72) c = violet ? mix(c, C('#E6DDF6'), .5) : mix(c, C('#F4C165'), .55);       // the inner glow edge
    const ex = Math.min(x, W - x);
    if (ex < 1) c = sink(c, .45);
    if (Math.abs(u - .5) * W < .5) c = sink(c, .15);
    return T(grain(c, x, y, .05, .3, N.e));
  };
}
// Inner glow ring (halo2): a translucent polar ring card and its thin wall.
function glowRing(W, violet, alpha = .85) {
  const hi = C(violet ? '#F2ECFF' : '#FFF4C8'), lo = C(violet ? '#896CC7' : '#E3BF73');
  return (u, v) => {
    const r = Math.hypot(u - .5, v - .5) * 2, d = Math.abs(r - .9);
    if (d > .09) return TRANSPARENT;
    const c = mix(hi, lo, smooth(0, .09, d));
    return [c[0], c[1], c[2], Math.round(255 * alpha * (1 - smooth(.02, .09, d)))];
  };
}
function glowBand(W, H, violet) {
  const hi = C(violet ? '#F2ECFF' : '#FFF4C8'), lo = C(violet ? '#896CC7' : '#E3BF73');
  return (u, v) => { const d = Math.abs(v - .5) * 2, c = mix(hi, lo, d); return [c[0], c[1], c[2], Math.round(255 * .8 * (1 - d * .8))]; };
}

// =====================================================================================================================
// Medallions, drill pods, plates, pendulum, tower
// =====================================================================================================================
// Eye medallion face (64 px over 1 b): a gold ring with bronze rim teeth, a dark spiral centre and the glowing
// orange C-ring (open toward the lower right); hot: white-gold.
function medalEyeFace(W, hot) {
  return (u, v) => {
    const dx = u - .5, dy = v - .5, r = Math.hypot(dx, dy) * 2, a = Math.atan2(dy, dx);
    if (r > 1) return TRANSPARENT;
    if (r > .84) { let c = RAMP.gold(.25 + .4 * (r - .84) / .16); if (r > .95) c = sink(c, .3); return T(c); }
    if (r > .76) return T(sink(RAMP.bronze(.5), .3));
    // the C ring: a glowing band r .5..68 with a gap from -20 to 60 degrees
    const ang = (a * 180 / Math.PI + 360) % 360, inGap = ang > 340 || ang < 50;
    if (r > .48 && r < .7 && !inGap) {
      const t = Math.abs(r - .59) / .11;
      const c = hot ? mix(C('#FFFFF0'), C('#FFE9A0'), t) : mix(C('#FFE6A8'), C('#F4A13C'), t);
      return T(c);
    }
    // dark spiral centre
    let c = mix(C('#2A2230'), C('#443B4C'), r / .76);
    const sp = Math.sin(a * 1 + r * 14);
    if (sp > .6 && r < .46) c = mix(c, C('#8C7A6A'), .5);
    if (r < .1) c = hot ? C('#FFF4C8') : C('#C98A4A');
    return T(c);
  };
}
// Gear medallion face: a 16-tooth bronze-gold gear outline (the teeth are boxes), a glowing gold hub.
function medalGearFace(W, hot) {
  return (u, v) => {
    const dx = u - .5, dy = v - .5, r = Math.hypot(dx, dy) * 2, a = Math.atan2(dy, dx);
    if (r > .82) return TRANSPARENT;
    let c = RAMP.gold(.3 + .35 * r);
    if (r > .76) c = sink(c, .25);
    // 6 spokes with lightening holes between
    const sp = ((a / (Math.PI * 2)) * 6 % 1 + 1) % 1;
    if (r > .34 && r < .66 && sp > .2 && sp < .8) c = sink(RAMP.dbronze(.7), .4);
    if (Math.abs(r - .34) < .025 || Math.abs(r - .66) < .025) c = sink(c, .3);
    if (r < .26) {                                              // glowing hub
      const t = r / .26;
      c = hot ? mix(C('#FFFFFF'), C('#FFE9A0'), t) : mix(C('#FFF0B8'), C('#E8A23C'), t);
    }
    return T(c);
  };
}
// Drill pod profile (tile per facet; v from the top cap (0) to the cone tip (1), stations in model units y +4 .. -16):
// cream cog cap, bronze, the gear disc rim (cream teeth with dark slots), the glowing collar ring, then the cone in
// dark bronze with glowing gold bands.
export const DRILL_V = {top: 4, bot: -16};
function drillTile(W, H) {
  const yAt = v => DRILL_V.top + (DRILL_V.bot - DRILL_V.top) * v;
  return (u, v) => {
    const x = u * W, y = yAt(v);
    let c;
    if (y > 1.6) c = block(RAMP.cream(.2 + .1 * (4 - y)), {t: (4 - y) * 8, b: (y - 1.6) * 8, l: x, r: W - x}, {hi: 2, lo: 2, line: .8});
    else if (y > -1.6) {                                       // gear disc rim
      c = RAMP.cream(.25);
      if (Math.abs(u - .5) * W < W * .18) c = sink(RAMP.bronze(.7), .35);
      if (Math.abs(y - 1.6) < .25 || Math.abs(y + 1.6) < .25) c = sink(c, .35);
    } else if (y > -3.2) {                                     // collar ring (glow)
      c = mix(C('#FFE6A8'), C('#F2B65C'), Math.abs(y + 2.4) / .8);
    } else {                                                   // striped cone
      const band = ((-3.2 - y) / 2.15) % 1;
      c = band < .55 ? RAMP.dbronze(.45 + .2 * band) : mix(C('#F8D27A'), C('#E09A45'), (band - .55) / .45);
      if (band < .06) c = sink(c, .3);
    }
    return T(grain(c, x, v * H, .04, .2, N.b));
  };
}
const drillTop = W => (u, v) => {
  const r = Math.hypot(u - .5, v - .5) * 2, a = Math.atan2(v - .5, u - .5);
  if (r > 1) return TRANSPARENT;
  let c = RAMP.cream(.2 + .2 * r);
  if (Math.cos(a * 8) > .6 && r > .5) c = sink(RAMP.bronze(.6), .2);
  if (r < .25) c = RAMP.gold(.3);
  if (Math.abs(r - .25) < .04) c = sink(c, .4);
  return T(c);
};
// Polar ledge discs (alpha-cut round, the colour of the facets beside them).
const ledge = (W, base, t = .4) => (u, v) => {
  const r = Math.hypot(u - .5, v - .5) * 2;
  if (r > 1) return TRANSPARENT;
  return T(base(t + .25 * r));
};
const plateRim = (W, H) => (u, v) => {
  const x = u * W, y = v * H;
  let c = RAMP.bronze(.4 + .2 * v);
  if (Math.abs(v - .5) < .16) c = mix(C('#FFE6A8'), C('#EEC170'), Math.abs(v - .5) / .16);
  if (y < 1) c = lift(c, .25);
  return T(c);
};
// Polar discs (plates, tower tiers): u, v across the disc, alpha-cut outside r 1 and inside the hole.
//   plate   bronze with a glowing groove ring near the rim, radial bars, a dark hole rim;
//   plate2  the smaller upper disc, plain bronze with an engraved ring;
//   t1      dark bronze tier with a gold edge; t2 the flat tier with a glowing gold edge ring.
function polarDisc(W, kind) {
  const hole = {plate: .2, plate2: .22, t1: .36, t2: .36}[kind];
  return (u, v) => {
    const dx = u - .5, dy = v - .5, r = Math.hypot(dx, dy) * 2, a = Math.atan2(dy, dx);
    if (r > 1 || r < hole) return TRANSPARENT;
    let c;
    if (kind === 'plate' || kind === 'plate2') {
      c = RAMP.bronze(.28 + .35 * (1 - r) + .08 * Math.cos(a - 2.3));
      if (kind === 'plate' && r > .78 && r < .88) c = mix(C('#FFE6A8'), C('#EEC170'), Math.abs(r - .83) / .05);
      if (kind === 'plate2' && Math.abs(r - .7) < .025) c = sink(c, .4);
      if (Math.cos(a * 8) > .985 && r > hole + .05 && r < .76) c = sink(c, .35);
      if (r > .95) c = sink(c, .3);
      if (r < hole + .04) c = sink(c, .45);
    } else if (kind === 't1') {
      c = RAMP.dbronze(.42 + .2 * (1 - r));
      if (r > .9) c = RAMP.gold(.3 + .3 * (r - .9) / .1);
      if (Math.abs(r - .62) < .02) c = sink(c, .4);
      if (Math.cos(a * 16) > .97 && r > .4 && r < .88) c = lift(c, .12);
    } else {
      c = RAMP.cream(.2 + .2 * (1 - r));
      if (r > .86) c = mix(C('#FFF4C8'), C('#F4C165'), (r - .86) / .14);
      if (Math.abs(r - .6) < .02) c = sink(c, .35);
      if (Math.cos(a * 12) > .98 && r < .84 && r > .4) c = sink(c, .25);
    }
    return T(grain(c, u * W, v * W, .05, .15, N.a));
  };
}
// Dagger card (32 x 128 over 0.3 x 1.2 b, hilt at the top): a gold kite blade with a centre ridge (lit left half,
// shaded right half), a knob and a short guard.
function daggerCard(W, H) {
  return (u, v) => {
    const x = (u - .5) * 2, y = v;
    if (y < .08) { const r = Math.hypot(x / .5, (y - .04) / .04); return r <= 1 ? T(RAMP.gold(.3 + .3 * r)) : TRANSPARENT; }
    if (y < .12) return Math.abs(x) < .8 ? T(sink(RAMP.gold(.4), .2)) : TRANSPARENT;
    const wpk = .26, w = y < wpk ? .45 + .55 * (y - .12) / (wpk - .12) : Math.pow(1 - (y - wpk) / (1 - wpk), .9);
    if (Math.abs(x) > w) return TRANSPARENT;
    let c = x < 0 ? mix(C('#F8E3A8'), C('#EBC263'), -x / Math.max(w, .01)) : mix(C('#D9B259'), C('#A3875F'), x / Math.max(w, .01));
    if (Math.abs(x) < .05) c = x < 0 ? lift(c, .4) : sink(c, .2);
    if (Math.abs(x) > w - .07) c = sink(c, .3);
    return T(c);
  };
}
// Pendulum cog (front view, 64 px over 0.7 b): a silver 6-tooth cog with a keyhole.
function cogCard(W) {
  return (u, v) => {
    const dx = u - .5, dy = v - .5, r = Math.hypot(dx, dy) * 2, a = Math.atan2(dy, dx);
    const tooth = Math.cos(a * 6) > .3;
    if (r > (tooth ? .98 : .72)) return TRANSPARENT;
    // keyhole: a round hole above a slot
    if (Math.hypot(dx, dy + .08) < .1 || (Math.abs(dx) < .045 && dy > -.08 && dy < .14)) return TRANSPARENT;
    let c = RAMP.silver(.15 + .45 * r + .2 * (dy + .5));
    if (r > .62 && r < .7) c = sink(c, .2);
    if (tooth && r > .9) c = sink(c, .25);
    if (dx < -.1 && dy < -.1) c = lift(c, .2);
    return T(c);
  };
}
// Protractor face (annulus tile, v from the outer edge): cream-gold with tick marks (long every 4th) and a scale line.
function arcFace(W, H) {
  return (u, v) => {
    const x = u * W, y = v * H;
    let c = RAMP.prot(.15 + .3 * v);
    for (let i = 0; i < 4; i++) {
      const tx = (i + .5) / 4, long = i === 1;
      if (Math.abs(u - tx) * W < .7 && v < (long ? .6 : .38)) c = sink(c, .55);
    }
    if (Math.abs(v - .7) * H < .6) c = sink(c, .35);
    if (y < 1) c = lift(c, .3);
    const ex = Math.min(x, W - x);
    if (ex < .6) c = sink(c, .2);
    return T(c);
  };
}
// Ousia flame (violet crystal flame round the cog), translucent card, 64 x 96 over 0.7 x 1.0 b.
function ousiaCard(W, H) {
  return (u, v) => {
    const dx = (u - .5) * 2, y = 1 - v;                   // y 0 bottom .. 1 top
    // a flame silhouette: wide at the cog (y .35), licking up in three tongues
    const tongues = .55 + .25 * Math.cos(dx * 7.5) * smooth(.4, .9, y);
    const w = y < .35 ? .55 + .45 * smooth(0, .35, y) : (1 - smooth(.35, 1, y)) * tongues + .1;
    const d = Math.abs(dx) / Math.max(.02, w);
    if (d > 1) return TRANSPARENT;
    const c = mix(C('#F2ECFF'), C('#7562D0'), smooth(.0, 1, d * .8 + (y > .6 ? (y - .6) : 0)));
    const crystal = Math.abs(Math.sin(dx * 9 + y * 6)) < .12 ? .25 : 0;
    const a = (1 - Math.pow(d, 2)) * (.85 - .4 * smooth(.6, 1, y)) + crystal;
    return [c[0], c[1], c[2], Math.round(255 * clamp(a))];
  };
}
// Beams and columns (translucent cards along -Y, fading to alpha 0 at the long edges and the far end).
function beamCard(W, H, core, body, edge, fadeEnd = true) {
  const cc = C(core), cb = C(body), ce = C(edge);
  return (u, v) => {
    const d = Math.abs(u - .5) * 2;
    const c = d < .3 ? mix(cc, cb, d / .3) : mix(cb, ce, (d - .3) / .7);
    let a = d < .3 ? 1 : 1 - smooth(.3, 1, d);
    if (fadeEnd) a *= 1 - smooth(.85, 1, v);
    a *= smooth(0, .04, v);
    return [c[0], c[1], c[2], Math.round(255 * .92 * a)];
  };
}
// Tower column (tile per facet; v from the base (0) up to the top (1)): stacked cream/gold blocks.
function towerColTile(W, H) {
  return (u, v) => {
    const x = u * W, y = v * H, row = Math.floor(v * 6), f = (v * 6) % 1;
    const gold = row % 3 === 2;
    let c = gold ? RAMP.gold(.25 + .3 * f) : RAMP.cream(.12 + .25 * f);
    const off = row % 2 ? .5 : 0, bx = ((u + off) % 1);
    c = block(c, {t: f * H / 6, b: (1 - f) * H / 6, l: bx * W, r: (1 - bx) * W}, {hi: 1.6, lo: 1.6, line: .9});
    return T(grain(c, x, y, .04, .15, N.d));
  };
}
const towerRim = (W, H) => (u, v) => { const c = mix(C('#FFFBE0'), C('#F2B65C'), Math.abs(v - .5) * 2); return T(c); };
// X frame of the spikes (front card, 64 px over 1.4 b): a bronze ring round the medallion with a dark-red inner
// ring and four prongs reaching in at the diagonals.
function xframeCard(W) {
  return (u, v) => {
    const dx = u - .5, dy = v - .5, r = Math.hypot(dx, dy) * 2, a = Math.atan2(dy, dx);
    if (r > 1) return TRANSPARENT;
    const diag = Math.abs(Math.sin(2 * a)) > .93;
    if (r > .82) { let c = RAMP.bronze(.25 + .3 * (r - .82) / .18); if (r > .95 || r < .84) c = sink(c, .35); return T(c); }
    if (r > .74) return T(RAMP.red(.4));
    if (diag && r > .56) { let c = RAMP.gold(.3 + .3 * (r - .56) / .18); return T(c); }
    return TRANSPARENT;
  };
}
// The bomb (prop): a gold-banded dark sphere with a glowing seam (wrap).
function bombWrap(W, H) {
  return (u, v) => {
    const x = u * W, y = v * H;
    let c = mix(C('#3A2416'), C('#6A4A2A'), .5 + .5 * Math.cos(u * 6.28));
    if (Math.abs(v - .5) < .1) c = RAMP.gold(.3);
    if (Math.abs(v - .5) < .025) c = C('#FFE9A0');
    if ((u * 4) % 1 < .06) c = RAMP.gold(.4);
    return T(grain(c, x, y, .05, .3, N.c));
  };
}

// =====================================================================================================================
// Sprite table
// =====================================================================================================================
// name -> [w, h, painter, translucent]
export function fieldgenSprites() {
  const S = {};
  const op = (n, w, h, f) => { S[n] = [w, h, f, false]; };
  const tr = (n, w, h, f) => { S[n] = [w, h, f, true]; };
  // ring
  for (const L of Object.keys(LEVELS)) {
    op('band_' + L, 96, 48, bandTile(96, 48, L));
    op('bandin_' + L, 64, 48, bandTile(64, 48, L, true));
    op('tier_' + L, 64, 32, tierTile(64, 32, L));
  }
  for (const look of ['idle', 'hot', 'off']) {
    tr('seam_' + look, 96, 48, seamTile(96, 48, look));
    tr('prim_' + look, 32, 32, portRim(32, look, 'eye'));
    tr('brim_' + look, 32, 32, portRim(32, look, 'bomb'));
    tr('bcore_' + look, 32, 32, portCore(32, look));
  }
  op('rtop', 96, 64, topTile(96, 64));
  op('rbot', 96, 16, bottomTile(96, 16, false));
  op('tbot', 96, 64, bottomTile(96, 64, true));
  op('tooth', 32, 32, faceTile(32, 32, RAMP.cream));
  op('tooth_top', 32, 32, (u, v) => { const e = Math.min(u, 1 - u, v, 1 - v) * 32; let c = RAMP.cream(.06 + .1 * v); if (e < 2.2) c = RAMP.gold(.3 + .2 * (1 - e / 2.2)); if (e < .8) c = sink(c, .3); return T(grain(c, u * 32, v * 32, .04, .15, N.b)); });
  op('kgrid', 64, 64, gridTile(64, 64));
  op('pillar', 64, 64, pillarTile(64, 64));
  op('bell', 32, 32, bellTile(32, 32));
  op('port', 32, 32, portDisc(32, 'eye'));
  op('bport', 32, 32, portDisc(32, 'bomb'));
  op('bronze', 32, 32, plainTile(32, 32, RAMP.bronze, .3, .55));
  op('dbronze', 32, 32, plainTile(32, 32, RAMP.dbronze, .35, .6));
  op('cream', 32, 32, faceTile(32, 32, RAMP.cream));
  op('gold', 32, 32, faceTile(32, 32, RAMP.gold, {hiK: .3}));
  op('engraved', 32, 32, engravedTile(32, 32, RAMP.bronze));
  op('red', 32, 32, padTile(32, 32));
  op('clamp', 16, 16, faceTile(16, 16, RAMP.cream, {hi: 1.3, lo: 1.3}));
  // gold, spikes, iris
  op('gold8', 128, 64, gold8(128, 64));
  op('collar', 32, 32, collarTile(32, 32));
  op('xframe', 64, 64, xframeCard(64));
  for (const look of ['shut', 'open', 'hot']) op('iris_' + look, 64, 64, irisCard(64, look));
  // core
  op('shell', 256, 128, shellWrap(256, 128));
  op('eyeframe', 32, 32, eyeFrameTile(32, 32));
  for (const look of ['idle', 'charge', 'field', 'dim']) op('eye_' + look, 96, 96, eyeGlow(96, look));
  op('arch_out', 32, 32, archOut(32, 32));
  op('arch_in', 32, 32, archIn(32, 32));
  op('brimc', 128, 128, brimCard(128));
  op('brim_edge', 32, 16, plainTile(32, 16, t => mix(RAMP.bronze(t), C('#D6B693'), .4), .3, .7));
  op('wire', 128, 128, wireCard(128));
  tr('glow_charge', 64, 64, radialGlow(64, '#FFFBE0', '#FBE483', .85, .5));
  tr('glow_flash', 64, 64, radialGlow(64, '#FFFFFF', '#FFE9A0', 1, .7));
  for (const s of [0, 1, 2, 3]) tr('bubble_' + s, 192, 96, bubbleWrap(192, 96, s));
  tr('bubble_burst', 192, 96, bubbleWrap(192, 96, 'burst'));
  tr('gold_shell', 128, 64, goldShell(128, 64));
  // halos
  op('halo_out', 32, 16, haloWall(32, 16, false)); op('halo_out_v', 32, 16, haloWall(32, 16, true));
  op('halo_in', 32, 16, haloWall(32, 16, false, true)); op('halo_in_v', 32, 16, haloWall(32, 16, true, true));
  op('halo_face', 32, 16, haloFace(32, 16, false)); op('halo_face_v', 32, 16, haloFace(32, 16, true));
  tr('ring2', 96, 96, glowRing(96, false)); tr('ring2_v', 96, 96, glowRing(96, true));
  tr('ring2_band', 16, 16, glowBand(16, 16, false)); tr('ring2_band_v', 16, 16, glowBand(16, 16, true));
  // medallions
  op('medal_eye', 64, 64, medalEyeFace(64, false)); op('medal_eye_hot', 64, 64, medalEyeFace(64, true));
  op('medal_gear', 64, 64, medalGearFace(64, false)); op('medal_gear_hot', 64, 64, medalGearFace(64, true));
  op('medal_back', 64, 64, medalGearFace(64, false));
  // drill pods, plates, pendulum, tower
  op('drill', 16, 128, drillTile(16, 128));
  op('drill_top', 32, 32, drillTop(32));
  op('ledge_dbronze', 16, 16, ledge(16, RAMP.dbronze, .45));
  op('ledge_cream', 16, 16, ledge(16, RAMP.cream, .2));
  op('ledge_gold', 16, 16, ledge(16, RAMP.gold, .25));
  op('plate_disc', 96, 96, polarDisc(96, 'plate'));
  op('plate2_disc', 96, 96, polarDisc(96, 'plate2'));
  op('dagger', 32, 128, daggerCard(32, 128));
  op('ledge_plum', 16, 16, ledge(16, RAMP.plum, .7));
  tr('bubble_ledge', 16, 16, (u, v) => { const r = Math.hypot(u - .5, v - .5) * 2; return r > 1 ? TRANSPARENT : [255, 250, 236, 45]; });
  op('plate_rim', 32, 16, plateRim(32, 16));
  op('cog', 64, 64, cogCard(64));
  op('silver', 16, 16, plainTile(16, 16, RAMP.silver, .2, .45, .04, false));
  op('arc_face', 32, 32, arcFace(32, 32));
  op('arc_edge', 32, 16, plainTile(32, 16, RAMP.prot, .2, .45));
  tr('ousia', 64, 96, ousiaCard(64, 96));
  tr('beam_gold', 32, 64, beamCard(32, 64, '#FFF6DA', '#FCD88F', '#D4A558'));
  tr('beam_link', 32, 64, beamCard(32, 64, '#FFF6DA', '#FADEA8', '#E4BB76', false));
  tr('col_gold', 32, 128, beamCard(32, 128, '#FFFBE6', '#FBE483', '#E2AE66'));
  tr('col_violet', 32, 128, beamCard(32, 128, '#F2ECFF', '#A18CEA', '#57337D'));
  op('tower_col', 32, 64, towerColTile(32, 64));
  op('tower_t1', 96, 96, polarDisc(96, 't1'));
  op('tower_t2', 96, 96, polarDisc(96, 't2'));
  op('tower_rim', 32, 16, towerRim(32, 16));
  op('bomb', 64, 32, bombWrap(64, 32));
  return S;
}
export const spriteId = name => 'rlk:mboss/fieldgen/' + name;
export function paintFieldgenTextures(rp, only = null) {
  const S = fieldgenSprites(), out = {};
  for (const [n, [w, h, f, tr]] of Object.entries(S)) out[n] = [w, h, f, tr];
  return paintSpriteSet(rp, 'assets/rlk/textures/mboss/fieldgen', out, spriteId, only);
}
