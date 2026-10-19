// TAIL region of the 아펩의 오아시스 파수꾼 rig (plan R4 parts 40-47; model.md §3.6, model_p3.md §2.4 item 24, §3 item 7):
// the twisted two-band ribbon tail, 9.1 b in both forms, 7 segments + the tip.
//   tail_1 .. tail_7  ONE model per segment for both forms: a round 8-facet loft whose facets alternate between the pale
//                     band (slot band_a) and the dark band (slot band_b) with the band pattern shifted 45 deg per
//                     segment, so the two bands spiral round the tail (model.md §11 "the tail helix"). P1 pale + slate,
//                     P3 pale grey-white + dark green: the slot colours (apep_materials SLOT_COLOR). Closed solids, so a
//                     camera inside the tail region sees no inner card (plan R18).
//   tail_tip          P1 the curled dark scythe hook + a pale leaf curl; P3 a thin whip ending in a pale leaf tip.
// Frames (apep_pose FRAMES): every tail part is authored in its bone frame 'z' at the CROUCH stance: +Z along the
// segment toward the next joint, +Y up; the joint at the origin. Region interface: see apep_body.mjs.
import {loft, slab, toUnits, mirrorX} from './mboss_shape_lib.mjs';
import {PART_SCALE, TAIL_C} from './apep_pose.mjs';
import {PAL, C, clamp, smooth, mix, N, sink, lift, autoSlot, sprite, onRect, onRectY, spriteSize, sdLeaf, stroke} from './apep_materials.mjs';
import {registerTile, registerWrap} from './mboss_shape_lib.mjs';

export const REGION = 'tail';
export const PARTS = ['tail_1', 'tail_2', 'tail_3', 'tail_4', 'tail_5', 'tail_6', 'tail_7', 'tail_tip'];
const SEG = PARTS.slice(0, 7);
const LEN = TAIL_C.slice(0, 8).map((p, i) => Math.hypot(...TAIL_C[i + 1].map((v, k) => v - p[k])));
// ribbon width (blocks) along the tail: 0.95 at the root (model.md: base 0.7 -> 0.3; model_p3: about 1 b thick at the
// root) down to 0.34 at the tip joint
const W = i => .95 - .61 * i / 7;
registerTile('g_tail_a', 64, 64, 32);
registerTile('g_tail_b', 64, 64, 32);
// grey band tiles (tinted per form by their slots): the pale band with dark segment lines; the dark band, darker grain
const bandA = (u, v) => { const s = ((v * 4) % 1 + 1) % 1; let g = .9 + .06 * (N.a(u * 6, v * 6) - .5); if (s < .06) g = .45; else if (s < .12) g -= .15; return [g * 255, g * 255, g * 255, 255].map(Math.round); };
const bandB = (u, v) => { const s = ((v * 4 + .5) % 1 + 1) % 1; let g = .34 + .08 * (N.b(u * 8, v * 3) - .5); if (s < .05) g = .2; return [g * 255, g * 255, g * 255, 255].map(Math.round); };
function segment(i) {
  const L = LEN[i], w0 = W(i) / 2, w1 = W(i + 1) / 2, n = 8;
  // facet k of segment i shows band A when (k + i) mod 4 < 2: the bands advance 45 deg per segment
  const tex = k => ((k + i) % 4 < 2 ? 'g_tail_a' : 'g_tail_b');
  return loft('z', [{a: -.06, r: w0 * 1.02}, {a: L * .5, r: (w0 + w1) / 2 * 1.04}, {a: L + .04, r: w1}], {n, tex: k => tex(k), caps: i === 0 ? '-' : '', seed: 700 + i * 13, ledges: true});
}
// ---- the tip ---------------------------------------------------------------------------------------------------------------
const TIP_L = LEN[7];
// P1: a curled dark scythe hook in the vertical plane (x = 0; u = Z along the tail, v = Y), the pale leaf curl beside it
const HOOK = stroke([[0, 0], [.35, .12], [.7, .3], [.98, .58], [1.05, .9], [.9, 1.12], [.68, 1.1]], t => .2 * (1 - t) + .03);
const HOOK_R = {u0: -.15, u1: 1.3, v0: -.25, v1: 1.35};
const CURL = stroke([[.2, 0], [.55, -.18], [.85, -.12], [.95, .1], [.8, .22]], t => .14 * Math.sin(Math.PI * Math.min(1, t * 1.15)) + .02);
const CURL_R = {u0: .05, u1: 1.15, v0: -.4, v1: .4};
const hookPaint = (u, v) => { const n = HOOK.near(u, v); if (n.d > .2 * (1 - n.t) + .03) return null; let c = PAL.p1_slate(clamp(.35 + .3 * n.t + .15 * (N.a(u * 9, v * 9) - .5))); if (n.d > .2 * (1 - n.t) - .01) c = PAL.p1_line(.8); else if (n.s > 0 && n.d > .1 * (1 - n.t)) c = lift(c, .12); return c; };
const curlPaint = (u, v) => { const n = CURL.near(u, v), hw = .14 * Math.sin(Math.PI * Math.min(1, n.t * 1.15)) + .02; if (n.d > hw) return null; let c = PAL.p1_bark(clamp(.15 + .35 * n.t)); if (n.d > hw - .02) c = PAL.p1_line(.6); return c; };
function tipP1() {
  const els = loft('z', [{a: -.05, r: W(7) / 2}, {a: .45, r: W(7) * .38}, {a: .75, r: .1}], {n: 8, tex: k => ((k + 7) % 4 < 2 ? 'g_tail_a' : 'g_tail_b'), seed: 790});
  els.push(...slab({plane: 'x', at: 0, rect: HOOK_R, sd: HOOK.sd, half: .07, sprite: 'p1_tailhook', edge: 'g_tail_b', cell: .08}));
  els.push(...slab({plane: 'x', at: .12, rect: CURL_R, sd: (u, v) => CURL.sd(u, v), half: .04, sprite: 'p1_tailcurl', edge: 'g_tail_a', cell: .07, core: false}));
  return els;
}
// P3: the thin whip (a long taper) ending in a pale leaf tip lying flat (plane y: u = X, v = Z)
const LEAF_R = {u0: -.28, u1: .28, v0: .55, v1: 1.45};
const leafSd = sdLeaf(0, .6, 1.42, .24, {p: .8});
const leafPaint = (u, v) => { if (leafSd(u, v) > 0) return null; let c = PAL.p3_pale(clamp(.12 + .3 * (v - .6) + .1 * (N.c(u * 9, v * 9) - .5))); if (Math.abs(u) < .018) c = PAL.p3_line(.3); if (leafSd(u, v) > -.025) c = PAL.p3_line(.55); return c; };
function tipP3() {
  const els = loft('z', [{a: -.05, r: W(7) / 2}, {a: .3, r: W(7) * .3}, {a: .7, r: .06}], {n: 8, tex: k => ((k + 7) % 4 < 2 ? 'g_tail_a' : 'g_tail_b'), seed: 791});
  els.push(...slab({plane: 'y', at: 0, rect: LEAF_R, sd: leafSd, half: .03, sprite: 'p3_tailleaf', edge: 'g_tail_a', cell: .07, core: false}));
  return els;
}
// ---- region interface ------------------------------------------------------------------------------------------------------
// models(): {model name: elements in model units}; FORM_MODELS {part: {p1, p3}}; sprites(): the region's card sprites.
export function models() {
  const out = {};
  SEG.forEach((n, i) => { out[n] = toUnits(autoSlot(segment(i)), PART_SCALE[n]); });
  out.tail_tip_p1 = toUnits(autoSlot(tipP1()), PART_SCALE.tail_tip);
  out.tail_tip_p3 = toUnits(autoSlot(tipP3()), PART_SCALE.tail_tip);
  return out;
}
export const FORM_MODELS = {...Object.fromEntries(SEG.map(n => [n, {p1: n, p3: n}])), tail_tip: {p1: 'tail_tip_p1', p3: 'tail_tip_p3'}};
export function sprites() {
  const [hw, hh] = spriteSize(HOOK_R, 48), [cw, ch] = spriteSize(CURL_R, 48), [lw, lh] = spriteSize(LEAF_R, 48);
  return {
    g_tail_a: sprite(64, 64, 32, bandA, 'both', 'tail', {use: 'tinted'}),
    g_tail_b: sprite(64, 64, 32, bandB, 'both', 'tail', {use: 'tinted'}),
    p1_tailhook: sprite(hw, hh, 48, onRect(HOOK_R, hookPaint), 'p1', 'tail'),
    p1_tailcurl: sprite(cw, ch, 48, onRect(CURL_R, curlPaint), 'p1', 'tail'),
    p3_tailleaf: sprite(lw, lh, 48, onRectY(LEAF_R, leafPaint), 'p3', 'tail'),
  };
}
export const NOTES = {tail_1: 'segments share one model per segment for both forms (slot tints)', tail_tip: 'P1 scythe hook + leaf curl; P3 whip + leaf tip'};
void [C, smooth, mix, sink, registerWrap, mirrorX];
