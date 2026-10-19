// HANDS region of the 아펩의 오아시스 파수꾼 rig (plan R8: the hands change SHAPE with the stance; one display shows one model,
// so the shapes are discrete item-model variants swapped at fixed events with a 0.9 -> 1 scale pulse). 20 models:
//   A  p1_planted  3-lobe pale claw flat on the floor + square gold gem in a raised frame + gold cone (model.md §3.3)
//      p1_raised   the same claw curled (the arms up)
//      p3_fork     the forked leafy tip of the antler arm + gold cone (model_p3 §2.3 item 13)
//   B  p1_open     5-petal hand (3 front + 2 side petals) splayed flat, Ø 1.8, cream cone on the back (model.md §3.4)
//      p1_curl     the petals curled up (lifted >= 0.3 b)
//      p3_curl     the fiddlehead-curled leaf hand (the crawl foot, the fold) + cream cone
//      p3_open     the big lobed butter-yellow leaf hand, 2.2 b, over the white-grey under-leaf fin (v6 f480)
//   C  p1_open / p1_curl  as B, Ø 1.5, the petals pointing back (rear feet)
//      p3_curl     the curled leaf hand 1.5 with the square-spiral glyph + cream cone (v5 f588)
// Frames (apep_pose FRAMES): world axes about the wrist joint, P1 variants as they sit in the CROUCH stance (planted on
// the floor), P3 variants as they sit in the UPRIGHT stance. The P3 crawl orients its hands through the IK hand eulers
// (hf_*), so a P3 hand shows the same in the crawl as authored. Region interface: see apep_body.mjs.
import {slab, rockBox, toUnits, mirrorX, stroke, sdUnion} from './mboss_shape_lib.mjs';
import {PART_SCALE} from './apep_pose.mjs';
import {PAL, C, clamp, mix, N, lift, sink, autoSlot, sprite, onRect, onRectY, spriteSize, sdLeaf, cone, ball} from './apep_materials.mjs';

export const REGION = 'hands';
export const PARTS = ['a_hand_l', 'a_hand_r', 'b_hand_l', 'b_hand_r', 'c_hand_l', 'c_hand_r'];
export const VARIANTS = {a: ['p1_planted', 'p1_raised', 'p3_fork'], b: ['p1_open', 'p1_curl', 'p3_curl', 'p3_open'], c: ['p1_open', 'p1_curl', 'p3_curl']};
const SP = {};
const card = (name, rect, fn, ppb, forms, y = false) => { const [w, h] = spriteSize(rect, ppb); SP[name] = sprite(w, h, ppb, (y ? onRectY : onRect)(rect, fn), forms, 'hands'); return name; };
const lineOut = (c, d, w, L) => (d > -w ? mix(c, L, .85) : c);

// ---- A: the 3-lobed claw (plane y: u = X outward, v = Z; the floor 0.48 under the wrist) ------------------------------------
const CLAW_R = {u0: -.15, u1: 1.05, v0: -.75, v1: .65};
const FING = [[[.15, -.12], [.55, -.42], [.85, -.62]], [[.2, 0], [.6, .02], [.98, .04]], [[.15, .1], [.5, .36], [.78, .52]]].map(p => stroke(p, t => .17 - .07 * t));
const clawSd = sdUnion(...FING.map(f => f.sd), (u, v) => Math.hypot(u - .1, v) - .28);
const clawPaint = (u, v) => { const d = clawSd(u, v); if (d > 0) return null; let c = PAL.p1_bark(clamp(.18 + .2 * (N.a(u * 7, v * 7) - .5) + .15 * u)); const s = Math.abs(Math.sin((u * 7 + v * 3) * Math.PI)); if (s < .08) c = sink(c, .18); return lineOut(c, d, .035, PAL.p1_line(.75)); };
function clawP1(curl) {
  const y = -.42, els = [rockBox([-.28, -.5, -.3], [.42, -.16, .26], 'g_shell', {seed: 401})];
  els.push(...slab({plane: 'y', at: y, rect: CLAW_R, sd: clawSd, half: .06, sprite: card('p1_claw', CLAW_R, clawPaint, 48, 'p1', true), edge: 'g_shell', cell: .08,
    rot: curl ? ['z', -45, [.3, y, 0]] : null}));
  els.push(rockBox([0, -.19, -.18], [.38, -.1, .18], 'g_plate', {seed: 402}), rockBox([.06, -.12, -.12], [.32, -.04, .12], 'p1_gem', {seed: 403}));
  els.push(...cone([-.08, -.16, 0], .11, .38, 'p1_gold', {seed: 404}));
  return els;
}
// ---- A phase 3: the forked leafy tip (plane z facing the front: u = X, v = Y) ------------------------------------------------
const FORK_R = {u0: -.2, u1: .2, v0: 0, v1: .9};
const forkSd = sdLeaf(0, 0, .9, .17, {p: .8});
const forkPaint = (u, v) => { const d = forkSd(u, v); if (d > 0) return null; let c = PAL.p3_lime(clamp(.12 + .4 * (1 - v) + .1 * (N.b(u * 9, v * 9) - .5))); if (Math.abs(u) < .016) c = PAL.p3_line(.3); return lineOut(c, d, .02, PAL.p3_line(.6)); };
function forkP3() {
  const els = [rockBox([-.12, -.15, -.12], [.12, .15, .12], 'g_shell', {seed: 411})];
  const sp = card('p3_forkleaf', FORK_R, forkPaint, 48, 'p3');
  for (const [dx, r] of [[0, 0], [.08, -22.5], [-.08, 22.5]]) {
    const rect = {u0: FORK_R.u0 + dx, u1: FORK_R.u1 + dx, v0: .05, v1: .95}, sd = (u, v) => forkSd(u - dx, v - .05);
    els.push(...slab({plane: 'z', at: 0, rect, sd, half: .03, sprite: sp, edge: 'p3_lime', cell: .06, core: false, rot: r ? ['z', r, [dx, .05, 0]] : null}));
  }
  els.push(...cone([.04, .82, 0], .09, .3, 'p3_gold', {seed: 412}));
  return els;
}
// ---- B / C phase 1: the petal hand (plane y; the petals radiate from the hand centre) --------------------------------------
// front petal: along -Z from the centre (rect v = Z); side petal: along +X (rect u = X)
const PETAL_F = {u0: -.3, u1: .3, v0: -1.0, v1: -.08};
const petalF = sdLeaf(0, -1.0, -.08, .27, {p: .75});
const PETAL_S = {u0: .08, u1: 1.0, v0: -.3, v1: .3};
const petalS = (u, v) => sdLeaf(0, .08, 1.0, .27, {p: .75})(v, u);
const petalPaintF = (sd, along) => (u, v) => { const d = sd(u, v); if (d > 0) return null; const t = along === 'v' ? -v : u, w = along === 'v' ? u : v; let c = PAL.p1_bark(clamp(.12 + .25 * t + .12 * (N.c(u * 8, v * 8) - .5))); if (Math.abs(w) < .02) c = PAL.p1_line(.45); return lineOut(c, d, .03, PAL.p1_line(.8)); };
function petalHand(k, back, curl) {
  // k = petal length scale (B 1.0, C 0.83); back = the petals point back (+Z: the rear feet); curl = lifted / curled
  const y = -.27, cz = back ? .3 : -.3, sz = back ? -1 : 1, els = [];
  els.push(rockBox([-.32 * k, -.32, cz - .3 * k], [.38 * k, -.06, cz + .3 * k], 'g_shell', {seed: 421 + k}));
  const spF = card('p1_petal', PETAL_F, petalPaintF(petalF, 'v'), 48, 'p1', true), spS = card('p1_petal_s', PETAL_S, petalPaintF(petalS, 'u'), 48, 'p1', true);
  const front = (rot) => {
    const rect = {u0: PETAL_F.u0 * k, u1: PETAL_F.u1 * k, v0: back ? cz + .08 * k : cz - 1.0 * k, v1: back ? cz + 1.0 * k : cz - .08 * k};
    const sd = (u, v) => petalF(u / k, (sz * (v - cz)) / k) * k;
    return slab({plane: 'y', at: y, rect, sd, half: .045, sprite: spF, edge: 'g_shell', cell: .08, core: true, rot});
  };
  const side = (s, rot) => {
    const rect = s > 0 ? {u0: PETAL_S.u0 * k, u1: PETAL_S.u1 * k, v0: cz + PETAL_S.v0 * k, v1: cz + PETAL_S.v1 * k} : {u0: -PETAL_S.u1 * k, u1: -PETAL_S.u0 * k, v0: cz + PETAL_S.v0 * k, v1: cz + PETAL_S.v1 * k};
    const sd = (u, v) => petalS((s * u) / k, (v - cz) / k) * k;
    return slab({plane: 'y', at: y, rect, sd, half: .045, sprite: spS, edge: 'g_shell', cell: .08, core: true, rot});
  };
  if (!curl) {
    els.push(...front(null), ...front(['y', 45, [0, y, cz]]), ...front(['y', -45, [0, y, cz]]), ...side(1, null), ...side(-1, null));
  } else {
    els.push(...front(['x', sz * 45, [0, y, cz + sz * -.08 * k]]), ...side(1, ['z', 45, [.08 * k, y, cz]]), ...side(-1, ['z', -45, [-.08 * k, y, cz]]));
    els.push(...ball([0, -.05, cz], .3 * k, 'g_shell', {seed: 431}));
  }
  els.push(...cone([.04, -.08, cz], .12 * k, .38 * k, 'p1_cone', {seed: 432}));
  return els;
}
// ---- B / C phase 3 curl: a fiddlehead (plane z facing the front: u = X outward, v = Y) ----------------------------------------
// the curl grows up and out of the wrist (its lowest point ~0.45 b under the wrist: the crawl wrists at 0.4 b touch the water)
const CURL_R = {u0: -.55, u1: 1.05, v0: -.55, v1: 1.1};
const SPIRAL = (() => { const pts = []; for (let i = 0; i <= 40; i++) { const t = i / 40, a = -2.0 + t * 9.0, r = .55 * (1 - t * .85); pts.push([.25 + r * Math.cos(a), .3 + r * Math.sin(a)]); } return stroke(pts, t => .17 * (1 - t) + .03); })();
const curlSd = (u, v) => SPIRAL.sd(u, v);
const curlPaint = glyph => (u, v) => { const n = SPIRAL.near(u, v), hw = .17 * (1 - n.t) + .03; if (n.d > hw) return null; let c = PAL.p3_leafhand(clamp(.15 + .5 * n.t + .1 * (N.a(u * 8, v * 8) - .5))); if (n.t > .82) c = mix(c, C('#F2EE7A'), .6); if (glyph && n.t < .45) { const gx = Math.abs(((u * 9) % 1 + 1) % 1 - .5), gy = Math.abs(((v * 9) % 1 + 1) % 1 - .5); if (Math.max(gx, gy) > .38 && Math.max(gx, gy) < .46) c = PAL.p3_line(.4); } return lineOut(c, n.d - hw, .025, PAL.p3_line(.65)); };
function curlP3(k, glyph) {
  const rect = {u0: CURL_R.u0 * k, u1: CURL_R.u1 * k, v0: CURL_R.v0 * k, v1: CURL_R.v1 * k};
  const els = [rockBox([-.18 * k, -.2 * k, -.18 * k], [.2 * k, .16 * k, .18 * k], 'g_shell', {seed: 441})];
  els.push(...slab({plane: 'z', at: 0, rect, sd: (u, v) => curlSd(u / k, v / k) * k, half: .09 * k, sprite: card(glyph ? 'p3_curl_c' : 'p3_curl', CURL_R, curlPaint(glyph), 48, 'p3'), edge: 'p3_lime', cell: .08}));
  els.push(...cone([-.05 * k, .14 * k, .05], .11 * k, .36 * k, 'p3_cone', {seed: 442}));
  return els;
}
// ---- B phase 3 open: the big lobed leaf hand (plane z facing the front: u = X outward, v = Y), held out up and out ----------
const LEAF_R = {u0: -.35, u1: 2.15, v0: -.8, v1: 1.45};
const AX = t => [.05 + 1.72 * t, .02 + .98 * t];
const LOBES = [[.18, .42, 1], [.38, .58, -1], [.58, .6, 1], [.76, .5, -1], [.92, .32, 1]];
const leafSd = (u, v) => {
  let d = Infinity;
  for (const [t, r, s] of LOBES) { const [x, y] = AX(t), nx = -.5, ny = .87; d = Math.min(d, Math.hypot(u - x - s * .14 * nx, v - y - s * .14 * ny) - r); }
  const [x0, y0] = AX(0), [x1, y1] = AX(1.08);
  return Math.min(d, stroke([[x0, y0], [x1, y1]], t => .14 * (1 - t) + .02).sd(u, v));
};
const leafPaint = (u, v) => { const d = leafSd(u, v); if (d > 0) return null; const [ax, ay] = AX(0), t = clamp(((u - ax) * 1.72 + (v - ay) * .98) / (1.72 * 1.72 + .98 * .98)); let c = PAL.p3_leafhand(clamp(.08 + .3 * t + .12 * (N.d(u * 6, v * 6) - .5))); const ribD = Math.abs((u - ax) * .98 - (v - ay) * 1.72) / 1.98; if (ribD < .03) c = PAL.p3_line(.25); else { const vs = Math.abs(((t * 9 + ribD * 3) % 1) - .5); if (vs < .05 && ribD < .55) c = mix(c, PAL.p3_line(.35), .45); } return lineOut(c, d, .035, PAL.p3_line(.55)); };
const FIN_R = {u0: -.3, u1: 2.45, v0: -.95, v1: 1.6};
const finSd = (u, v) => stroke([[.0, -.05], [.9, .45], [1.75, 1.0], [2.38, 1.5]], t => .62 * Math.sin(Math.PI * Math.min(1, .15 + .85 * t)) * (1 - .6 * t) + .02).sd(u, v);
const finPaint = (u, v) => { const d = finSd(u, v); if (d > 0) return null; let c = PAL.p3_pale(clamp(.1 + .2 * (N.e(u * 6, v * 6) - .5) + .1 * u / 2.4)); return lineOut(c, d, .03, PAL.p3_line(.5)); };
function openP3() {
  const els = [rockBox([-.2, -.22, -.2], [.25, .2, .2], 'g_shell', {seed: 451})];
  els.push(...slab({plane: 'z', at: -.04, rect: LEAF_R, sd: leafSd, half: .05, sprite: card('p3_leafhand', LEAF_R, leafPaint, 48, 'p3'), edge: 'p3_lime', cell: .1}));
  els.push(...slab({plane: 'z', at: .1, rect: FIN_R, sd: finSd, half: .025, sprite: card('p3_underleaf', FIN_R, finPaint, 32, 'p3'), edge: 'g_shell', cell: .1, core: false}));
  els.push(...cone([.1, .18, .0], .1, .32, 'p3_cone', {seed: 452}));
  return els;
}
// ---- region interface ------------------------------------------------------------------------------------------------------
const BUILD = {
  a: {p1_planted: () => clawP1(false), p1_raised: () => clawP1(true), p3_fork: forkP3},
  b: {p1_open: () => petalHand(1, false, false), p1_curl: () => petalHand(1, false, true), p3_curl: () => curlP3(1, false), p3_open: openP3},
  c: {p1_open: () => petalHand(.83, true, false), p1_curl: () => petalHand(.83, true, true), p3_curl: () => curlP3(.85, true)},
};
let built = null;
export function models() {
  if (built) return built;
  const out = {};
  for (const [L, vars] of Object.entries(BUILD)) for (const [v, fn] of Object.entries(vars)) {
    const m = toUnits(autoSlot(fn()), PART_SCALE[`${L}_hand_l`]);
    out[`${L}_hand_l_${v}`] = m; out[`${L}_hand_r_${v}`] = mirrorX(m);
  }
  return (built = out);
}
// the form look's default hand per form (the sets p1_rest / p3_open of the contract; hands.sets in the manifest)
export const FORM_MODELS = Object.fromEntries(PARTS.map(n => { const L = n[0]; return [n, {p1: `${n}_${L === 'a' ? 'p1_planted' : 'p1_open'}`, p3: `${n}_${L === 'a' ? 'p3_fork' : L === 'b' ? 'p3_open' : 'p3_curl'}`}]; }));
export function sprites() { models(); return {...SP}; }
void [lift];
