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
  stalk: ramp(['#ECEEE6', '#D6D9CF', '#BDC2B4', '#9FA698', '#7E867A', '#5C6458']),        // p3_pale
  dome: ramp(['#F6FFDA', '#E2F8AA', '#C4EC7A', '#A0D656', '#7CB63C', '#5A902A']),
  gold: ramp(['#FFF6C2', '#F9E48A', '#EDCB5A', '#D6AC3C', '#B08A2C', '#7C601E']),
  black: ramp(['#4A4E46', '#34382F', '#24271F', '#181A14', '#0E100C']),
};

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
const sdLens = (w, h, y0 = 0) => (u, v) => { const R = (h * h / 4 + w * w / 4) / w, c = R - w / 2; return Math.max(Math.hypot(u - c, v - y0 - h / 2), Math.hypot(u + c, v - y0 - h / 2)) - R; };
const pts = (...a) => a;
export const SH = {
  // 기본: a skirt foot in a radial plane (u = distance from the axis, v = height): hangs from the bell rim, curls up
  b_lobe: SHP({u0: .26, u1: .66, v0: 0, v1: .26}, stroke(bez([.36, .22], [.4, .02], [.58, .05], 14).concat([[.62, .11]]), t => .06 - .032 * t).sd),
  // a foot seen face-on (tangential plane, u across, v up from the ground along the card)
  b_lobeF: SHP({u0: -.12, u1: .12, v0: 0, v1: .24}, (u, v) => { const t = 1 - v / .24, w = .05 + .062 * Math.sin(Math.PI * Math.min(1, t * .85 + .1)); return Math.max(Math.abs(u) - w * (t > .85 ? Math.sqrt(Math.max(0, 1 - ((t - .85) / .17) ** 2)) : 1), v - .24, -v); }),
  // the curled sprout on the bell top (x plane: u = Z, v = Y)
  b_stem: SHP({u0: -.12, u1: .24, v0: .98, v1: 1.36}, stroke(bez([0, 1.0], [-.03, 1.3], [.12, 1.31], 12).concat([[.19, 1.27], [.2, 1.21]]), t => .042 - .024 * t).sd),
  // a jagged crown petal of the bag (tangential card; u across, v up from the neck)
  b_petal: SHP({u0: -.17, u1: .17, v0: 0, v1: .46}, sdPoly(pts([-.04, 0], [.04, 0], [.11, .2], [.16, .3], [.12, .33], [.14, .42], [.07, .37], [.04, .46], [-.01, .38], [-.07, .44], [-.09, .34], [-.15, .36], [-.12, .25]))),
  // 수호 shield: a vesica pane 0.6 x 1.4 and the small 3-leaf crown
  b_pane: SHP({u0: -.31, u1: .31, v0: 0, v1: 1.42}, sdLens(.6, 1.4, .01)),
  b_lcrown: SHP({u0: -.24, u1: .24, v0: 0, v1: .26}, sdUnion(sdLens(.11, .25, 0), (u, v) => sdLens(.1, .22, 0)(u * .8 + v * .6 - .02, -u * .6 + v * .8 + .04),
    (u, v) => sdLens(.1, .22, 0)(u * .8 - v * .6 + .02, u * .6 + v * .8 + .04))),
  // 양육: the S ribbon in profile (x plane: u = Z, v = Y) and its lower twist face-on (z plane: u = X)
  n_rib: SHP({u0: -.5, u1: .5, v0: 0, v1: 2.24}, stroke([[.12, .02], [.24, .32], [.22, .62], [.05, .95], [-.16, 1.25], [-.22, 1.52], [-.12, 1.8], [.04, 2.0], [.06, 2.2]], t => .17 - .1 * t).sd),
  n_rib2: SHP({u0: -.4, u1: .4, v0: 0, v1: 1.3}, stroke([[-.04, .02], [-.2, .35], [-.14, .7], [.08, 1.02], [.12, 1.28]], t => .15 - .08 * t).sd),
  // the hood leaf in profile (x plane, cap frame: joint at the origin; it arches forward over the orb) and face-on
  n_hood: SHP({u0: -.74, u1: .26, v0: -.34, v1: .44}, sdUnion(stroke([[.08, -.04], [.1, .2], [-.08, .36], [-.36, .34], [-.56, .16], [-.64, -.08], [-.6, -.3]], t => .07 + .06 * Math.sin(Math.PI * t)).sd)),
  n_hoodF: SHP({u0: -.36, u1: .36, v0: -.3, v1: .42}, (u, v) => Math.max(Math.hypot(u / .33, (v - .06) / .34) - 1, -(v + .3)) * .3),
  n_hoodT: SHP({u0: -.6, u1: .32, v0: -.2, v1: .62}, stroke([[.08, -.04], [.12, .24], [.0, .46], [-.24, .56], [-.46, .48], [-.56, .3], [-.52, .12]], t => .07 + .06 * Math.sin(Math.PI * t)).sd),
  n_frond: SHP({u0: -.11, u1: .11, v0: 0, v1: .56}, sdLens(.2, .56, 0)),
  // 수호: two helix ribbons (u across, v up; shape centre wanders sideways), the hem lobe, the death wisp
  g_ribA: SHP({u0: -.5, u1: .5, v0: .45, v1: 4.45}, (u, v) => { const t = (v - .45) / 4, c = .22 * Math.sin(t * 7.2), w = .2 * (1 - .55 * t) * smooth(-.02, .05, t) + .012; const tip = v > 4.0 ? (v - 4.0) / .45 : 0;
    const split = tip > 0 ? Math.abs(Math.abs(u - c) - .07 * tip) - w * (1 - tip) : Math.abs(u - c) - w; return Math.max(split, .45 - v, v - 4.45); }),
  g_ribB: SHP({u0: -.5, u1: .5, v0: .45, v1: 4.2}, (u, v) => { const t = (v - .45) / 3.75, c = .2 * Math.sin(t * 6.4 + 2.2), w = .17 * (1 - .6 * t) + .012; return Math.max(Math.abs(u - c) - w, .45 - v, v - 4.2); }),
  g_lobe: SHP({u0: .14, u1: .62, v0: 0, v1: .34}, stroke(bez([.2, .32], [.3, .02], [.56, .05], 10), t => .09 - .05 * t).sd),
  g_wisp: SHP({u0: -.5, u1: .5, v0: 0, v1: 1.7}, sdUnion(stroke([[0, 0], [.08, .4], [-.06, .8], [.04, 1.1]], t => .14 - .08 * t).sd,
    stroke([[.04, 1.1], [-.14, 1.3], [-.3, 1.62]], t => .05 - .04 * t).sd, stroke([[.04, 1.1], [.2, 1.32], [.38, 1.58]], t => .05 - .04 * t).sd)),
  g_drape: SHP({u0: -.42, u1: .42, v0: 0, v1: 1.3}, (u, v) => { const w = .26 + .14 * (1 - v / 1.3), sc = .035 * Math.cos(u * 26); return Math.max(Math.abs(u) - w, -(v - .02 - sc), v - 1.3); }),
  // 둥지: a sepal wing in front view (z plane, wing frame: hinge at the origin, +u = outward), the eye ring
  w_wing: SHP({u0: -.06, u1: 1.06, v0: -.62, v1: .32}, sdUnion(stroke([[0, 0], [.2, .17], [.42, .2], [.64, .06], [.8, -.16], [.88, -.38]], t => .085 - .045 * t).sd,
    stroke([[.88, -.38], [.97, -.5], [1.02, -.42]], t => .04 - .02 * t).sd, stroke([[.86, -.36], [.78, -.54], [.84, -.6]], t => .035 - .02 * t).sd)),
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
  p_podlid: SHP({u0: -.95, u1: .95, v0: 0, v1: 1.8}, (u, v) => { const r = .9 * Math.sin(Math.PI * clamp(v / 1.8)) ** .55 + .01, sc = .05 * Math.abs(Math.sin(v * 14)); return Math.abs(u) - r + sc; }),
  // the Heart: a leaf-flame sprout, a petal clump, a vine tendril, a vine stem strip
  h_tip: SHP({u0: -.16, u1: .16, v0: 0, v1: .62}, (u, v) => { const t = clamp(v / .62), w = .13 * Math.sin(Math.PI * Math.pow(t, .7)) + .008; return Math.abs(u - .05 * Math.sin(t * 4)) - w; }),
  h_petal: SHP({u0: -.3, u1: .3, v0: 0, v1: .36}, (u, v) => { const r = Math.hypot(u / .28, v / .34), lob = .12 * Math.cos(Math.atan2(v, u) * 7); return (r - 1 + lob) * .25; }),
  h_sprout: SHP({u0: -.12, u1: .12, v0: 0, v1: .7}, sdUnion(stroke([[0, 0], [.02, .3], [-.02, .5]], t => .025).sd, sdLens(.11, .22, .48), (u, v) => sdLens(.09, .18, 0)(u * .7 - (v - .28) * .7 - .02, u * .7 + (v - .28) * .7))),
  h_tendril: SHP({u0: -.5, u1: .5, v0: -1.1, v1: .1}, sdUnion(...[[-.1, -.45], [.1, -.4], [-.3, -.3], [.32, -.28], [0, -.5]].map(([x, b], i) =>
    stroke(bez([x * .3, 0], [x * 1.4, b], [x * 1.1 - (i % 2 ? .08 : -.08), b * 2.1], 10).concat([[x * .7, b * 2.1 + .06]]), t => .05 - .035 * t).sd))),
  h_stem: SHP({u0: -.3, u1: .3, v0: -6.2, v1: .1}, sdUnion(stroke([[0, 0], [.06, -1.5], [-.08, -3.0], [.07, -4.5], [-.02, -6.1]], t => .08).sd,
    stroke([[.02, -1.0], [.2, -1.25], [.24, -1.45]], t => .03 - .02 * t).sd, stroke([[-.04, -3.6], [-.22, -3.85], [-.25, -4.0]], t => .03 - .02 * t).sd)),
  // the Heart cradle: a knobbly root finger (radial plane: u = distance from the centre, v = height) and a tall root arm
  h_root: SHP({u0: .55, u1: 2.3, v0: -.04, v1: 1.6}, (() => { const P = [[2.08, 0], [1.88, .42], [1.5, .98], [1.27, 1.3], [1.02, 1.38], [.8, 1.24]]; const st = stroke(P, t => .21 - .14 * t + .035 * Math.sin(t * 17));
    return (u, v) => Math.max(st.sd(u, v), -v - .02); })()),
  h_arm: SHP({u0: .05, u1: 2.85, v0: -.04, v1: 4.5}, (() => { const P = [[2.3, 0], [2.48, 1.2], [2.24, 2.6], [1.78, 3.6], [1.12, 4.2], [.58, 4.08], [.36, 3.72]]; const st = stroke(P, t => .27 - .2 * t + .03 * Math.sin(t * 13));
    return (u, v) => Math.max(st.sd(u, v), -v - .02); })()),
  // 둥지 wall: a leaf blade 0.9 x 2.8 with a midrib and two windows (z plane, u across, v up)
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
const ribbonPx = (u, v, R = PAL.teal, rim = PAL.pale) => {
  const e = Math.min(u, 1 - u);
  let c = R(.35 + .18 * (N.c(u * 4, v * 20) - .5) + .1 * Math.sin(v * 9));
  if (e < .14) c = mix(c, rim(.1 + .2 * e / .14), .9 * smooth(.14, .05, e));
  return c;
};
function shellPx(u, v) {     // 파괴: dark armour plates with pale grey bands at the seams
  const x = u * 8, y = v * 4, fx = x - Math.floor(x), fy = y - Math.floor(y);
  let c = PAL.destr(.62 + .14 * (N.d(u * 12, v * 12) - .5) + .08 * h1(Math.floor(x) * 3 + Math.floor(y) * 11));
  const band = Math.min(fx, 1 - fx);
  if (band < .09) c = mix(c, PAL.destr(.12), .75 * (1 - band / .09));
  if (Math.min(fy, 1 - fy) < .06) c = sink(c, .3);
  return c;
}
function rootPx(u, v) {      // Heart roots: knobbly dark bark with long grain and pale knots
  const g = N.c(u * 5, v * 18), k = N.d(u * 14, v * 14);
  let c = PAL.root(.42 + .3 * (g - .5) + .12 * (N.a(u * 30, v * 3) - .5));
  if (Math.abs(g - .5) < .025) c = sink(c, .45);
  if (k > .72) c = mix(c, PAL.root(.12), .55 * smooth(.72, .85, k));
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
const shapeSprite = (name, shape, ppb, owner, fn, {plane = 'z', translucent = false, min = 16} = {}) => {
  const {rect} = shape, w = Math.max(min, r16((rect.u1 - rect.u0) * ppb)), h = Math.max(min, r16((rect.v1 - rect.v0) * ppb));
  add(name, w, h, onRect(rect, (u, v) => (shape.sd(u, v) > 0 ? null : fn(u, v)), plane), owner, translucent);
};

// 기본 basic (12 k)
add('bo_bell', 96, 48, bellPx, 'basic');
// loft ledges / caps face up: the game's up-face light is ~1.4x the side faces', so their tone is painted darker
const ledgeOf = (c, k = .7) => [c[0] * k, c[1] * k, c[2] * k, 255];
add('bo_bell_l', 16, 16, (s, t) => ledgeOf(PAL.bell(.14 + .05 * N.a(s * 4, t * 4))), 'basic');
shapeSprite('bo_lobe', SH.b_lobe, 64, 'basic', (u, v) => { const R = PAL.bell, b = bevel(SH.b_lobe.sd, u, v, .03); let c = R(.22 + .3 * smooth(.6, .78, u)); if (-b.d < .01) c = mix(c, R(.95), .8); else if (b.lit > 0) c = mix(c, R(0), .3 * b.rim); return c; });
shapeSprite('bo_lobeF', SH.b_lobeF, 64, 'basic', (u, v) => { let c = PAL.bell(.2 + .35 * smooth(.2, 0, v) + .08 * Math.abs(u) / .15); if (-SH.b_lobeF.sd(u, v) < .012) c = mix(c, PAL.bell(.95), .75); return c; });
shapeSprite('bo_stem', SH.b_stem, 48, 'basic', (u, v) => shadeShape(SH.b_stem.sd, u, v, PAL.olive, {t0: .45, edge: .008, w: .02}));
shapeSprite('bo_petal', SH.b_petal, 64, 'basic', (u, v) => { let c = shadeShape(SH.b_petal.sd, u, v, PAL.bell, {t0: .16 + .25 * smooth(.25, 0, v), edge: .008, w: .04, line: .6});
  if (Math.abs(u) < .012 && v < .3) c = mix(c, PAL.bell(.55), .5); return c; });
add('bo_glow', 16, 16, glowPx(PAL.core), 'basic');
shapeSprite('bo_pane', SH.b_pane, 22, 'basic', (u, v) => { const d = -SH.b_pane.sd(u, v); const rib = Math.abs(u) < .018;
  return A(mix(PAL.lime(.3), PAL.lime(0), smooth(.06, 0, d)), clamp(.26 + .6 * smooth(.08, 0, d) + (rib ? .3 : 0))); }, {translucent: true});
add('bo_bubble', 32, 16, (s, t) => A(mix(PAL.lime(.05), PAL.lime(.35), t), clamp(.08 + .55 * smooth(.25, 0, t) + .25 * smooth(.75, 1, t))), 'basic', true);
shapeSprite('bo_lcrown', SH.b_lcrown, 64, 'basic', (u, v) => shadeShape(SH.b_lcrown.sd, u, v, PAL.gem, {t0: .2, edge: .006, w: .02, line: .5}));

// 양육 nurturing (16 k)
add('nu_rib', 32, 64, (s, t) => ribbonPx(s, t), 'nurt');
shapeSprite('nu_ribS', SH.n_rib, 28, 'nurt', (u, v) => { const n = SH.n_rib.sd; const b = bevel(n, u, v, .07); let c = PAL.teal(.42 + .1 * Math.sin(v * 5) + .06 * (N.a(u * 8, v * 8) - .5));
  if (-b.d < .045) c = mix(c, PAL.pale(.12), .9); else if (b.lit > 0) c = mix(c, PAL.teal(0), .35 * b.rim * b.lit); return c; });
shapeSprite('nu_ribT', SH.n_rib2, 28, 'nurt', (u, v) => { const b = bevel(SH.n_rib2.sd, u, v, .07); let c = PAL.teal(.48 + .08 * Math.sin(v * 6)); if (-b.d < .04) c = mix(c, PAL.pale(.15), .9); return c; });
shapeSprite('nu_hood', SH.n_hood, 40, 'nurt', (u, v) => { let c = shadeShape(SH.n_hood.sd, u, v, PAL.hood, {t0: .14, edge: .01, w: .06, rimDark: .35});
  const vein = Math.abs(Math.sin((u * 1.2 + v) * 16)); if (vein < .06) c = mix(c, PAL.hood(.45), .35); return c; });
shapeSprite('nu_hoodF', SH.n_hoodF, 40, 'nurt', (u, v) => { const d = -SH.n_hoodF.sd(u, v); let c = mix(PAL.hood(.1), PAL.hood(.5), smooth(.25, -.25, v) * .6 + .25 * smooth(.08, 0, d)); if (d < .008) c = mix(c, PAL.hood(.8), .6); return c; });
shapeSprite('nu_hoodT', SH.n_hoodT, 40, 'nurt', (u, v) => shadeShape(SH.n_hoodT.sd, u, v, PAL.hood, {t0: .12, edge: .01, w: .06, rimDark: .35}));
shapeSprite('nu_frond', SH.n_frond, 40, 'nurt', (u, v) => { let c = shadeShape(SH.n_frond.sd, u, v, PAL.pale, {t0: .18, edge: .008, w: .03}); if (Math.abs(u) < .01) c = mix(c, PAL.pale(.5), .5); return c; });
add('nu_gem', 16, 16, (s, t) => { const d = Math.abs(s - .5) + Math.abs(t - .5); return d > .5 ? TRANSPARENT : PAL.gem(clamp(.1 + .7 * (s > .5 ? .6 : .2) * (t > .5 ? 1.2 : .6) + .2 * d)); }, 'nurt');
add('nu_orb', 16, 16, glowPx(PAL.core, .2), 'nurt');
add('nu_ring', 64, 16, (s, t) => A(mix(PAL.lime(0), PAL.lime(.35), t), clamp(.16 + .62 * smooth(.3, 0, t) + .22 * smooth(.7, 1, t) + .06 * Math.sin(s * Math.PI * 16) ** 8)), 'nurt', true);

// 수호 guarding (16 k)
const ribPale = (sd, k = 0) => (u, v) => { const b = bevel(sd, u, v, .08); let c = PAL.pale(.14 + .14 * (N.b(u * 4, v * 3) - .5) + k);
  if (b.lit < -.1) c = mix(c, PAL.teal(.25), .45 * b.rim); else if (b.lit > 0) c = mix(c, PAL.pale(0), .4 * b.rim * b.lit); if (-b.d < .012) c = mix(c, PAL.pale(.7), .6); return c; };
shapeSprite('gu_ribA', SH.g_ribA, 28, 'guard', ribPale(SH.g_ribA.sd));
shapeSprite('gu_ribB', SH.g_ribB, 28, 'guard', ribPale(SH.g_ribB.sd, .06));
add('gu_sheath', 64, 32, (s, t) => { let c = tealPx(s, t, .12 * t); const sc = Math.abs(Math.sin(s * Math.PI * 6)); if (t > .82) c = mix(c, PAL.pale(.45), smooth(.82, .95, t) * (1 - sc * .5)); return c; }, 'guard');
shapeSprite('gu_lobe', SH.g_lobe, 56, 'guard', (u, v) => shadeShape(SH.g_lobe.sd, u, v, ramp(['#C8D2D6', '#A4B2BA', '#84949E', '#66767E', '#4A585E']), {t0: .25, edge: .01, w: .04}));
shapeSprite('gu_drape', SH.g_drape, 32, 'guard', (u, v) => { let c = PAL.pale(.12 + .1 * Math.abs(Math.sin(u * 18)) + .2 * smooth(.4, 0, v)); if (-SH.g_drape.sd(u, v) < .02) c = mix(c, PAL.pale(.6), .5); return c; });
add('gu_bud', 48, 32, (s, t) => { let c = tealPx(s, t, -.04); const slit = Math.abs(s - .25) < .02 && t > .25 && t < .85; if (slit) c = PAL.core(.1); else if (Math.abs(s - .25) < .045 && t > .2 && t < .9) c = mix(c, PAL.core(.3), .5); return c; }, 'guard');
shapeSprite('gu_wisp', SH.g_wisp, 28, 'guard', (u, v) => { let c = PAL.black(.4 + .3 * (N.a(u * 6, v * 6) - .5)); if (-SH.g_wisp.sd(u, v) < .012) c = mix(c, C('#8E2A1E'), .5); return c; });
add('gu_gem', 16, 16, (s, t) => { const d = Math.abs(s - .5) * 1.2 + Math.abs(t - .5); return d > .55 ? TRANSPARENT : PAL.gem(clamp(.05 + (s < .5 ? .1 : .45) + (t > .5 ? .25 : 0))); }, 'guard');
add('gu_orb', 16, 16, glowPx(PAL.core, .15), 'guard');

// 둥지 nesting (12 k)
add('ne_cap', 64, 32, (s, t) => { let c = tealPx(s, t, -.06 + .1 * t); if (t > .9) c = mix(c, PAL.pale(.4), .5); return c; }, 'nest');
shapeSprite('ne_wing', SH.w_wing, 48, 'nest', (u, v) => { const b = bevel(SH.w_wing.sd, u, v, .05); let c = mix(PAL.pale(.2), C('#9DB3B0'), .45 * smooth(.2, .7, u));
  if (u > .82) c = mix(c, PAL.hood(.1), .7 * smooth(.82, .9, u)); if (b.lit < 0) c = mix(c, PAL.teal(.3), .35 * b.rim); if (-b.d < .01) c = mix(c, PAL.pale(.75), .6); return c; });
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
shapeSprite('pr_podlid', SH.p_podlid, 22, 'pred', (u, v) => { const d = -SH.p_podlid.sd(u, v); return A(mix(PAL.fin(.2 + .2 * clamp(v / 1.8)), PAL.fin(0), smooth(.06, 0, d)), clamp(.82 + .15 * smooth(.06, 0, d))); }, {translucent: true});
add('pr_face', 32, 32, (s, t) => PAL.teal(.38 + .2 * t + .08 * (N.a(s * 5, t * 5) - .5)), 'pred');

// the Heart of the Oasis (40 k): the bulb is painted as grey values and tinted per look (idle / egg / withered / blaze)
add('he_bulb', 128, 64, (s, t) => {
  const rib = Math.pow(Math.abs(Math.cos(s * Math.PI * 6)), 6);                     // 6 soft vertical ribs
  const spec = smooth(.16, .02, Math.hypot((s - .32) * 2.4, (t - .28) * 1.3));        // the big specular band, upper left
  let g = .9 + .07 * (N.a(s * 8, t * 6) - .5) - .12 * rib + .1 * smooth(.6, 1, Math.abs(t - .5) * 2);
  const swirl = Math.abs(Math.sin(s * Math.PI * 4 + t * 6 + 1.2)) < .1 && t > .2 && t < .8;
  if (swirl) g -= .1;
  g = clamp(g + .35 * spec);
  return A([255 * g, 255 * g, 255 * g, 255], .86);
}, 'heart', true);
add('he_swirl', 32, 32, (s, t) => { const x = s - .5, y = t - .5, r = Math.hypot(x, y) * 2, a = Math.atan2(y, x); if (r > 1) return TRANSPARENT;
  const arm = Math.abs(Math.sin(a * 2 + r * 7)); return A([200, 200, 196, 255], clamp(.5 * smooth(.25, 0, arm) * smooth(1, .4, r))); }, 'heart', true);
add('he_root', 32, 64, rootPx, 'heart');
const rootCard = sd => (u, v) => { const b = bevel(sd, u, v, .12); let c = rootPx(u * .45, v * .3); if (b.lit > 0) c = mix(c, PAL.root(.1), .45 * b.rim * b.lit); else c = sink(c, .35 * b.rim * -b.lit); if (-b.d < .02) c = sink(c, .4); return c; };
shapeSprite('he_rootc', SH.h_root, 30, 'heart', rootCard(SH.h_root.sd));
shapeSprite('he_armc', SH.h_arm, 21, 'heart', rootCard(SH.h_arm.sd));
shapeSprite('he_tip', SH.h_tip, 64, 'heart', (u, v) => { const d = -SH.h_tip.sd(u, v); return mix(PAL.tip(.05 + .3 * clamp(v / .62)), PAL.tip(0), smooth(.05, 0, d) * .5); });
shapeSprite('he_petal', SH.h_petal, 48, 'heart', (u, v) => shadeShape(SH.h_petal.sd, u, v, PAL.pale, {t0: .1, edge: .01, w: .05}));
shapeSprite('he_sprout', SH.h_sprout, 48, 'heart', (u, v) => shadeShape(SH.h_sprout.sd, u, v, PAL.gold, {t0: .2, edge: .008, w: .03}));
shapeSprite('he_tendril', SH.h_tendril, 40, 'heart', (u, v) => shadeShape(SH.h_tendril.sd, u, v, PAL.vine, {t0: .35, edge: .01, w: .03, rimLit: .35}));
shapeSprite('he_stem', SH.h_stem, 20, 'heart', (u, v) => shadeShape(SH.h_stem.sd, u, v, PAL.vine, {t0: .4, edge: .015, w: .04, rimLit: .3}));

// 소생의 찬가 domes (24 k)
add('do_shell', 64, 64, (s, t) => { const seam = Math.pow(Math.abs(Math.cos(s * Math.PI * 4)), 30); const hex = Math.abs(Math.sin(s * Math.PI * 16 + t * 3)) < .05 ? .08 : 0;
  return A(mix(PAL.dome(.35), PAL.dome(0), .5 * seam + .3 * smooth(.7, 1, t)), clamp(.16 + .16 * seam + hex + .18 * smooth(.85, 1, t))); }, 'dome', true);
add('do_vine', 128, 64, (s, t) => { const x = s * 8, y = t * 4, wav = Math.abs(y - 2 - .9 * Math.sin(x * Math.PI * .5) - .4 * Math.sin(x * 3.1));
  const leaf = (fx, fy) => Math.hypot((x - fx) * 2.2, (y - fy) * 4) < .5; let on = wav < .07;
  for (let k = 0; k < 8; k++) { const fx = k + .5, fy = 2 + .9 * Math.sin(fx * Math.PI * .5) + .4 * Math.sin(fx * 3.1); if (leaf(fx + .22, fy - .28) || leaf(fx - .2, fy + .3)) on = true; }
  if (!on) return TRANSPARENT; return PAL.dome(.15 + .25 * (N.a(x, y) - .5)); }, 'dome');
add('do_rim', 64, 16, (s, t) => A(mix(PAL.dome(0), PAL.dome(.3), t), clamp(.95 - .7 * t)), 'dome', true);
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
add('de_shell_l', 16, 16, (s, t) => ledgeOf(PAL.destr(.6)), 'destr');
add('pr_hood_l', 16, 16, (s, t) => ledgeOf(PAL.hood(.2)), 'pred');
add('pr_bowl_l', 16, 16, (s, t) => A(ledgeOf(PAL.fin(.3)), .75), 'pred', true);
add('pr_face_l', 16, 16, (s, t) => ledgeOf(PAL.teal(.42)), 'pred');
add('he_bulb_l', 16, 16, (s, t) => A([190, 190, 186, 255], .86), 'heart', true);
add('he_root_l', 16, 16, (s, t) => ledgeOf(PAL.root(.4 + .2 * N.c(s * 3, t * 3))), 'heart');
add('st_bark_l', 16, 16, (s, t) => ledgeOf(PAL.stalk(.3 + .1 * N.b(s * 3, t * 3))), 'stalk');
// loft tiles / wraps: texel density per block for the tileUV windows; wraps map u = facet k / n, v along the loft
for (const n of ['bo_bell', 'nu_rib', 'gu_sheath', 'gu_bud', 'ne_cap', 'de_shell', 'pr_hood', 'pr_bowl', 'pr_face', 'he_bulb', 'do_shell', 'do_vine', 'nu_ring', 'bo_bubble', 'do_rim', 'de_rim']) registerWrap(n);
registerTile('he_root', 32, 64, 28);
registerTile('st_bark', 64, 64, 22);

export const orgSprites = () => Object.fromEntries(Object.entries(S).map(([k, [w, h, fn, tr]]) => [k, [w, h, fn, tr]]));
export const spriteOwner = () => Object.fromEntries(Object.entries(S).map(([k, v]) => [k, v[4]]));
export const spriteSizes = () => Object.fromEntries(Object.entries(S).map(([k, [w, h]]) => [k, [w, h]]));
export function paintOrgTextures(rp, only = null) {
  return paintSpriteSet(rp, 'assets/rlk/textures/mboss/apep_om', orgSprites(), spriteId, only);
}
