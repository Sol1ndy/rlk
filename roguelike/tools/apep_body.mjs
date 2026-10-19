// BODY region of the 아펩의 오아시스 파수꾼 rig (plan R4 parts 1-8 and 18-21): the trunk of both forms.
//   abdomen   P1 the rear body (dark plates on top, pale belly scales below) | P3 the robe stem hanging from the waist
//             to the water: dark teal front panel with the olive-gold curl inlay and white diamonds, a green back
//   hem_a/b   P1 the dark belly ribbons (upper / tips) | P3 the lower robe with its pointed flaps, the hem flare
//   chest     P1 the ribcage (pale rib slabs under the belly), the belly shell, the drooping lobes over the sac
//             | P3 the lower chest: lime plates in front, bottle-green back, pale rib-blades curling round the sides
//   shoulders P1 the hump (cowl continuation), the shoulder hooks with the square gold gems in raised frames, the pale
//             bark side plates | P3 the upper chest, gold square shoulder plates
//   core      P1 the belly sac Ø 1.4 (one model: near-opaque glass + the emissive seed) | P3 the gold sternum + navel
//   crys_low / crys_back   P1 the gold spine and shoulder cones | P3 the lower / upper back emeralds, shoulder spikes
//   mantle_<s>_a/b   the shoulder flaps (P1) / carapace plates (P3): ONE model for both forms, tinted per form
// The f1104 "umbrella" (plan R2): identified as the B arms seen from behind / below (the up-turned gold-coned tips and the
// dark back with the lime rim are the B arms of v5 f1908), not the mantle; the mantle keeps its R4 scales (1.7 / 1.5).
//
// Region interface (every region module): REGION, PARTS, models() -> {model name: elements in model units},
// FORM_MODELS {part: {p1: model, p3: model}}, sprites() -> {name: sprite record (apep_materials sprite())}.
// Frames (apep_pose FRAMES): 'w' parts are authored in world axes about their joint as they sit in the reference stance
// (P1: CROUCH, P3: UPRIGHT); hem / mantle in their bone frame 'y' (model -Y along the bone). Blocks; toUnits() at the end.
import {loft, slab, rockBox, toUnits, mirrorX, stroke, sdUnion} from './mboss_shape_lib.mjs';
import {PART_SCALE} from './apep_pose.mjs';
import {PAL, C, clamp, mix, N, lift, sink, grey, autoSlot, sprite, onRect, spriteSize, sdLeaf, cone, ball, secC} from './apep_materials.mjs';
import {cardZ} from './mboss_model_lib.mjs';

export const REGION = 'body';
export const PARTS = ['abdomen', 'hem_a', 'hem_b', 'chest', 'shoulders', 'core', 'crys_low', 'crys_back', 'mantle_l_a', 'mantle_r_a', 'mantle_l_b', 'mantle_r_b'];
const SP = {};
const card = (name, rect, fn, ppb, forms, use = 'unique') => { const [w, h] = spriteSize(rect, ppb); SP[name] = sprite(w, h, ppb, onRect(rect, fn), forms, 'body', {use}); return name; };
const sinD = th => Math.sin(th * Math.PI / 180), cosD = th => Math.cos(th * Math.PI / 180);
const lineOut = (c, d, w, L) => (d > -w ? mix(c, L, .85) : c);
const oneSided = (els, keep) => { for (const e of els) for (const f of Object.keys(e.faces)) if (!keep.includes(f)) delete e.faces[f]; return els; };

// ================================================= phase 1 (CROUCH, world axes about the joint) ================================
// abdomen (joint = the waist (0, 2.8, 1.0)): the rear body back to the tail root (0, 2.39, 2.89)
function abdomenP1() {
  return loft('z', [{a: -.45, r: [1.05, .9, 1.05, .95], c: [0, .1]}, {a: .45, r: [1.1, .95, 1.1, .95], c: [0, .02]}, {a: 1.25, r: [.88, .8, .88, .78], c: [0, -.2]},
    {a: 2.0, r: [.55, .52, .55, .5], c: [0, -.42]}], {tex: (k, th) => (sinD(th) < -.3 ? 'g_shell' : 'g_plate'), caps: '-+', seed: 501});
}
// the dark belly ribbons: three alpha strips hanging along -Y (the bone frame 'y'), one-sided (the front face; plan R18)
const RIB_R = {u0: -.2, u1: .2, v0: -1.5, v1: .05};
const ribbonPaint = tip => (u, v) => { const t = clamp(-v / 1.5), hw = tip ? .19 * (1 - t) + .01 : .19 - .03 * t; if (Math.abs(u) > hw) return null; let c = PAL.p1_slate(clamp(.55 + .25 * t + .1 * (N.a(u * 9, v * 6) - .5))); if (Math.abs(u) > hw - .03) c = lift(c, .18); if (Math.abs(u) < .015) c = sink(c, .25); return c; };
function ribbons(tip, len) {
  const sp = card(tip ? 'p1_ribbon_tip' : 'p1_ribbon', RIB_R, ribbonPaint(tip), 32, 'p1'), els = [];
  for (const [x, r, z] of [[-.45, 22.5, .02], [0, 0, -.02], [.45, -22.5, .02]]) {
    const e = cardZ(sp, z, {X0: x - .2, X1: x + .2, Y0: -len, Y1: .05}, {rot: r ? ['z', r, [x, 0, z]] : undefined});
    els.push(...oneSided([e], ['north']));
  }
  return els;
}
// chest (joint (0, 3.16, 0)): the lower thorax, the rib slabs, the drooping lobes over the sac
const RIBS_R = {u0: -1.5, u1: 1.5, v0: -1.6, v1: -.1};
const ribSd = (u, v) => { const o = Math.hypot(u / 1.48, (v + .12) / 1.45) - 1, i = Math.hypot(u / 1.12, (v + .12) / 1.1) - 1; return Math.max(o * 1.3, -i * 1.1, v + .35); };
const ribPaint = (u, v) => { const d = ribSd(u, v); if (d > 0) return null; const s = Math.abs(Math.sin((Math.hypot(u, v + .1) * 7 + N.b(u * 3, v * 3)) * Math.PI)); let g = .88 + .06 * (N.a(u * 6, v * 6) - .5); if (s < .1) g -= .15; if (d > -.04) g = .38; return grey(g); };
const LOBE_R = {u0: -.3, u1: .3, v0: -.95, v1: 0};
const lobeSd = sdLeaf(0, -.95, 0, .26, {p: .6});
const lobePaint = (u, v) => { const d = lobeSd(u, v); if (d > 0) return null; let g = .86 + .08 * (N.c(u * 8, v * 8) - .5) - .12 * (-v); if (d > -.035) g = .4; return grey(g); };
function chestP1() {
  const els = loft('z', [{a: .65, r: [1.15, .75, 1.15, 1.0], c: [0, -.1]}, {a: 0, r: [1.4, .82, 1.4, 1.32], c: [0, -.12]}, {a: -.8, r: [1.45, .82, 1.45, 1.35], c: [0, -.1]},
    {a: -1.4, r: [1.2, .68, 1.2, 1.1], c: [0, -.02]}], {tex: (k, th) => (sinD(th) < -.2 ? 'g_shell' : 'g_plate'), caps: '+', seed: 511});
  const rs = card('g_ribcard', RIBS_R, ribPaint, 32, 'both', 'tinted');
  for (const z of [.35, -.05, -.45, -.85, -1.2]) els.push(...slab({plane: 'z', at: z, rect: RIBS_R, sd: ribSd, half: .07, sprite: rs, edge: 'g_shell', cell: .1}));
  const ls = card('g_lobe', LOBE_R, lobePaint, 32, 'both', 'tinted');
  for (const [x, r] of [[-.55, -22.5], [0, 0], [.55, 22.5]]) els.push(...slab({plane: 'z', at: -1.62, rect: {u0: x - .3, u1: x + .3, v0: -1.45, v1: -.5}, sd: (u, v) => lobeSd(u - x, v + .5), half: .04, sprite: ls, edge: 'g_shell', cell: .08, core: false, rot: ['x', 22.5, [x, -.5, -1.62]]}));
  return els;
}
// shoulders (joint (0, 3.31, -1.2)): the hump, the hooks + gems, the pale bark side plates
const HOOK_R = {u0: -1.15, u1: .35, v0: -.95, v1: .55};
const HOOK = stroke([[.25, .35], [-.2, .42], [-.65, .28], [-.95, -.05], [-.98, -.45], [-.78, -.72]], t => .3 - .17 * t);
const hookPaint = (u, v) => { const n = HOOK.near(u, v), hw = .3 - .17 * n.t; if (n.d > hw) return null; let c = PAL.p1_slate(clamp(.42 + .25 * (N.a(u * 7, v * 7) - .5) + .1 * n.t)); if (n.d > hw - .05) c = PAL.p1_seam(.5); const gx = u + .32, gy = v - .18; if (Math.abs(gx) < .2 && Math.abs(gy + .1) < .08 && gy < 0) c = mix(c, PAL.p1_seam(.15), .8); return c; };
const SIDE_R = {u0: -.9, u1: .9, v0: -.75, v1: .65};
const sideSd = (u, v) => Math.hypot(u / .85, v / .68) - 1;
const sidePaint = (u, v) => { const d = sideSd(u, v); if (d > 0) return null; const s = Math.abs(Math.sin((Math.hypot(u * .9, v) * 6 + .6 * N.d(u * 2, v * 2)) * Math.PI)); let g = .9 + .05 * (N.e(u * 5, v * 5) - .5); if (s < .1) g -= .2; if (d > -.06) g = .36; return grey(g); };
function shouldersP1() {
  const els = loft('z', [{a: .75, r: [1.2, .95, 1.2, .6], c: [0, .18]}, {a: 0, r: [1.62, 1.1, 1.62, .78], c: [0, .1]}, {a: -.5, r: [1.55, 1.0, 1.55, .72], c: [0, .05]},
    {a: -.82, r: [1.08, .7, 1.08, .52], c: [0, .02]}], {tex: (k, th) => (sinD(th) < -.4 ? 'g_shell' : 'g_plate'), caps: '+', seed: 521});
  const hs = card('p1_hook', HOOK_R, hookPaint, 48, 'p1'), ss = card('g_sidecard', SIDE_R, sidePaint, 32, 'both', 'tinted');
  for (const s of [1, -1]) {
    const half = [...slab({plane: 'x', at: 1.5, rect: HOOK_R, sd: HOOK.sd, half: .08, sprite: hs, edge: 'g_plate', cell: .1}),
      rockBox([1.52, -.05, -.62], [1.66, .32, -.28], 'g_plate', {seed: 522}), rockBox([1.6, .02, -.56], [1.72, .25, -.34], 'p1_gem', {seed: 523}),
      ...slab({plane: 'x', at: 1.38, rect: {u0: SIDE_R.u0 + .1, u1: SIDE_R.u1 + .1, v0: SIDE_R.v0 - .55, v1: SIDE_R.v1 - .55}, sd: (u, v) => sideSd(u - .1, v + .55), half: .05, sprite: ss, edge: 'g_shell', cell: .1})];
    els.push(...(s > 0 ? half : mirrorEls(half)));
  }
  return els;
}
// the mirror image of block-authored elements (mirrorModel mirrors about the pivot, so it works before toUnits too)
const mirrorEls = els => mirrorX(els);
// core (joint (0, 2.2, -0.85)): the belly sac at (0, -0.5, -0.15), r 0.7
function coreP1() { return ball([0, -.5, -.15], .7, 'p1_core', {seed: 531, n: 16}); }
// spine and shoulder cones
function crysLowP1() { return [...cone([0, .38, .2], .15, .48, 'p1_gold', {seed: 541}), ...cone([0, .3, .72], .12, .36, 'p1_gold', {seed: 542})]; }
function crysBackP1() {
  const els = [...cone([0, .3, .55], .17, .62, 'p1_gold', {seed: 551}), ...cone([0, .42, 0], .19, .72, 'p1_gold', {seed: 552}), ...cone([0, .3, -.5], .16, .56, 'p1_gold', {seed: 553})];
  for (const s of [1, -1]) els.push(...cone([s * 1.22, -.02, -.3], .14, .46, 'p1_gold', {seed: 554 + s}));
  return els;
}
// ================================================= phase 3 (UPRIGHT, world axes about the joint) ===============================
// abdomen (joint the waist (0, 3.11, 0.07)): the robe stem hanging to y 1.0 (loft 'y': e2 = the front)
function abdomenP3() {
  return loft('y', [{a: .4, r: [.66, .6, .66, .62]}, {a: -.3, r: [.62, .58, .62, .6]}, {a: -1.3, r: [.74, .66, .74, .7]}, {a: -2.15, r: [.86, .76, .86, .8]}],
    {tex: (k, th) => (sinD(th) > .25 ? 'p3_robe' : 'g_plate'), caps: '+', seed: 561});
}
// hem_a (bone frame 'y' upright, the joint in front of the stem axis by ~0.55): the lower robe + the pointed front flaps
const FLAP_R = {u0: -.32, u1: .32, v0: -1.0, v1: 0};
const flapSd = (u, v) => { const t = clamp(-v / 1.0); return Math.abs(u) - .3 * Math.pow(1 - t, .8) + (v > 0 ? v : 0); };
const flapPaint = (u, v) => { const d = flapSd(u, v); if (d > 0) return null; let c = PAL.p3_robe(clamp(.3 + .2 * (N.a(u * 8, v * 8) - .5) - .1 * v)); if (d > -.04) c = mix(c, C('#C9C27A'), .7); if (Math.abs(u) < .02) c = mix(c, C('#7F8345'), .6); return c; };
function hemAP3() {
  const els = loft('y', [{a: .2, r: [.84, .74, .84, .78], c: [0, -.55]}, {a: -.7, r: [.95, .84, .95, .88], c: [0, -.55]}, {a: -1.35, r: [1.08, .95, 1.08, .98], c: [0, -.55]}],
    {tex: (k, th) => (sinD(th) > .25 ? 'p3_robe' : 'g_plate'), seed: 571});
  const fs = card('p3_hemflap', FLAP_R, flapPaint, 32, 'p3');
  for (const [x, r] of [[-.5, 22.5], [0, 0], [.5, -22.5]]) els.push(...slab({plane: 'z', at: -.42, rect: {u0: x - .32, u1: x + .32, v0: -1.4, v1: -.4}, sd: (u, v) => flapSd(u - x, v + .4), half: .03, sprite: fs, edge: 'g_plate', cell: .08, core: false, rot: r ? ['z', r, [x, -.4, -.52]] : null}));
  return els;
}
// hem_b (bone frame 'y' upright, from 1.3 b down to the water): the hem flare, pointed dark flaps splayed onto the water
function hemBP3() {
  const fs = card('p3_hemflap', FLAP_R, flapPaint, 32, 'p3'), els = [], cz = .85;
  els.push(...loft('y', [{a: .1, r: 1.06, c: [0, -cz]}, {a: -.6, r: 1.22, c: [0, -cz]}, {a: -.95, r: 1.42, c: [0, -cz]}], {tex: (k, th) => (sinD(th) > .25 ? 'p3_robe' : 'g_plate'), seed: 581}));
  // four flaps flaring outward 45 deg (front, back, sides) + four upright diagonal flaps
  const F = (plane, at, x, axis, deg, piv) => slab({plane, at, rect: {u0: x - .34, u1: x + .34, v0: -1.15, v1: -.15}, sd: (u, v) => flapSd(u - x, v + .15), half: .03, sprite: fs, edge: 'g_plate', cell: .08, core: false, rot: [axis, deg, piv]});
  els.push(...F('z', -1.35 + cz, 0, 'x', -45, [0, -.55, -1.35 + cz]), ...F('z', 1.35 + cz, 0, 'x', 45, [0, -.55, 1.35 + cz]));
  els.push(...F('x', 1.35, cz, 'z', 45, [1.35, -.55, cz]), ...F('x', -1.35, cz, 'z', -45, [-1.35, -.55, cz]));
  for (const [x, z, r] of [[.95, -.95, 45], [-.95, -.95, -45], [.95, .95, -45], [-.95, .95, 45]]) els.push(...slab({plane: 'z', at: z + cz, rect: {u0: x - .3, u1: x + .3, v0: -1.1, v1: -.2}, sd: (u, v) => flapSd(u - x, v + .2), half: .03, sprite: fs, edge: 'g_plate', cell: .08, core: false, rot: ['y', r, [x, 0, z + cz]]}));
  return els;
}
// chest (joint (0, 4.18, -0.03)): the lower chest plates + pale rib-blades (loft 'y': e2 = front)
const BLADE_R = {u0: -.55, u1: .55, v0: -.2, v1: .2};
const BLADE = stroke([[-.5, .1], [-.15, .1], [.2, 0], [.52, -.16]], t => .15 * Math.sin(Math.PI * t) + .02);   // sweeping out and down round the ribs
const bladePaint = (u, v) => { const n = BLADE.near(u, v), hw = .15 * Math.sin(Math.PI * n.t) + .02; if (n.d > hw) return null; const s = Math.abs(Math.sin((n.t * 6 + n.d * 9) * Math.PI)); let g = .9 + .05 * (N.b(u * 7, v * 7) - .5); if (s < .1) g -= .16; if (n.d > hw - .03) g = .35; return grey(g); };
function chestP3() {
  const els = loft('y', [{a: -.85, r: [.7, .6, .7, .64]}, {a: 0, r: [.98, .72, .98, .8]}, {a: .8, r: [1.18, .78, 1.18, .86]}, {a: 1.3, r: [1.18, .72, 1.18, .84]}],
    {tex: (k, th) => (sinD(th) > .3 ? 'p3_lime' : 'g_plate'), caps: '-', seed: 591});
  const bs = card('g_bladecard', BLADE_R, bladePaint, 32, 'both', 'tinted');
  const half = [];
  for (const [y, x] of [[.8, .95], [.3, .82], [-.2, .62]]) half.push(...slab({plane: 'z', at: -.62, rect: {u0: x - .55, u1: x + .55, v0: y - .2, v1: y + .2}, sd: (u, v) => BLADE.sd(u - x, v - y), half: .03, sprite: bs, edge: 'g_shell', cell: .08, core: false, rot: ['y', 45, [x - .45, y, -.62]]}));
  els.push(...half, ...mirrorEls(half));
  return els;
}
// shoulders (joint (0, 5.39, -0.06)): the upper chest, the gold square shoulder plates
function shouldersP3() {
  const els = loft('y', [{a: -.45, r: [1.32, .74, 1.32, .86]}, {a: .25, r: [1.48, .72, 1.48, .88]}, {a: .58, r: [1.05, .5, 1.05, .62]}], {tex: (k, th) => (sinD(th) > .3 ? 'p3_lime' : 'g_plate'), caps: '+', seed: 601});
  for (const s of [1, -1]) els.push(rockBox([s * 1.15 - .24, .05, -.42], [s * 1.15 + .24, .45, -.24], 'g_plate', {seed: 602}), rockBox([s * 1.15 - .18, .1, -.48], [s * 1.15 + .18, .4, -.4], 'p3_gem', {seed: 603}));
  return els;
}
// core (joint (0, 4.82, -1.12)): the gold sternum (6-8 chevrons, a diamond at the top) on the chest front + the navel glow
const STERN_R = {u0: -.42, u1: .42, v0: -1.55, v1: .72};
const sternSd = (u, v) => { const w = .4 - .12 * clamp((-.42 - v) / 1.1) - .25 * clamp((v - .3) / .42); return Math.max(Math.abs(u) - w, v - .7, -1.52 - v); };
const sternPaint = (u, v) => { const d = sternSd(u, v); if (d > 0) return null; let c = PAL.p3_sternum(clamp(.1 + .25 * (N.c(u * 6, v * 6) - .5))); const ch = ((v - Math.abs(u) * .7) * 3.4 % 1 + 1) % 1; if (ch < .12) c = PAL.p3_sternum(.75); if (v > .25 && Math.abs(u) + Math.abs(v - .48) < .16) c = C('#FCFCC4'); return lineOut(c, d, .03, PAL.p3_sternum(.85)); };
function coreP3() {
  const els = slab({plane: 'z', at: .3, rect: STERN_R, sd: sternSd, half: .07, sprite: card('p3_sternum', STERN_R, sternPaint, 48, 'p3'), edge: 'p3_gold', cell: .1});
  els.push(...ball([0, -1.72, .3], .16, 'p3_gold', {seed: 611}));
  return els;
}
// emeralds: a diamond prism (a box turned 45 deg about z) facing back
const diamond = (c, s, d, seed) => rockBox([c[0] - s / 2, c[1] - s / 2, c[2] - d / 2], [c[0] + s / 2, c[1] + s / 2, c[2] + d / 2], 'p3_emerald', {rot: ['z', 45, c], seed});
function crysLowP3() { return [diamond([0, -.35, .5], .55, .26, 621)]; }
function crysBackP3() { return [diamond([0, -.1, .42], .72, .3, 631), ...[1, -1].flatMap(s => cone([s * .95, .08, .25], .13, .5, 'p3_emerald', {seed: 632 + s}))]; }
// ================================================= the mantle (both forms, bone frame 'y') ==================================
// a pointed leaf flap along -Y: the outer side (model -Z: up in the crouch, back in the upright) dark, the inner pale
const MANTLE_R = {u0: -.62, u1: .62, v0: -2.05, v1: .1};
const mantleSd = L => sdLeaf(0, -L, .05, .58, {p: .7});
const mantleOut = L => (u, v) => { const d = mantleSd(L)(u, v); if (d > 0) return null; let g = .5 + .1 * (N.a(u * 6, v * 4) - .5) - .1 * (-v / L); const vein = Math.abs(((v * 3 + Math.abs(u) * 2) % 1) - .5); if (vein < .05 && Math.abs(u) > .06) g -= .1; if (Math.abs(u) < .03) g -= .12; if (d > -.06) g = .85; return grey(g); };
const mantleIn = L => (u, v) => { const d = mantleSd(L)(u, v); if (d > 0) return null; let g = .88 + .05 * (N.b(u * 6, v * 6) - .5); if (Math.abs(u) < .025) g -= .2; if (d > -.04) g = .45; return grey(g); };
function mantle(L, tag) {
  const sdf = mantleSd(L), rect = {...MANTLE_R, v0: -L - .05};
  return [...slab({plane: 'z', at: 0, rect, sd: sdf, half: .06, sprite: card(`g_flap_${tag}`, rect, mantleOut(L), 32, 'both', 'tinted'), edge: 'g_plate', cell: .1, cards: '-'}),
    ...slab({plane: 'z', at: 0, rect, sd: sdf, half: .06, sprite: card(`g_flapin_${tag}`, rect, mantleIn(L), 32, 'both', 'tinted'), edge: 'g_plate', cell: .1, cards: '+', core: false})];
}
// ---- region interface ------------------------------------------------------------------------------------------------------
let built = null;
export function models() {
  if (built) return built;
  const u = (els, n) => toUnits(autoSlot(els), PART_SCALE[n]);
  const out = {
    abdomen_p1: u(abdomenP1(), 'abdomen'), abdomen_p3: u(abdomenP3(), 'abdomen'),
    hem_a_p1: u(ribbons(false, 1.48), 'hem_a'), hem_a_p3: u(hemAP3(), 'hem_a'),
    hem_b_p1: u(ribbons(true, 1.2), 'hem_b'), hem_b_p3: u(hemBP3(), 'hem_b'),
    chest_p1: u(chestP1(), 'chest'), chest_p3: u(chestP3(), 'chest'),
    shoulders_p1: u(shouldersP1(), 'shoulders'), shoulders_p3: u(shouldersP3(), 'shoulders'),
    core_p1_bulb: u(coreP1(), 'core'), core_p3_sternum: u(coreP3(), 'core'),
    crys_low_p1: u(crysLowP1(), 'crys_low'), crys_low_p3: u(crysLowP3(), 'crys_low'),
    crys_back_p1: u(crysBackP1(), 'crys_back'), crys_back_p3: u(crysBackP3(), 'crys_back'),
  };
  // the mantle: one model per flap for both forms (tinted per form by its slots)
  const ma = u(mantle(1.95, 'a'), 'mantle_l_a'), mb = u(mantle(1.85, 'b'), 'mantle_l_b');
  Object.assign(out, {mantle_l_a: ma, mantle_r_a: mirrorX(ma), mantle_l_b: mb, mantle_r_b: mirrorX(mb)});
  return (built = out);
}
export const FORM_MODELS = {
  abdomen: {p1: 'abdomen_p1', p3: 'abdomen_p3'}, hem_a: {p1: 'hem_a_p1', p3: 'hem_a_p3'}, hem_b: {p1: 'hem_b_p1', p3: 'hem_b_p3'},
  chest: {p1: 'chest_p1', p3: 'chest_p3'}, shoulders: {p1: 'shoulders_p1', p3: 'shoulders_p3'},
  crys_low: {p1: 'crys_low_p1', p3: 'crys_low_p3'}, crys_back: {p1: 'crys_back_p1', p3: 'crys_back_p3'},
  mantle_l_a: {p1: 'mantle_l_a', p3: 'mantle_l_a'}, mantle_r_a: {p1: 'mantle_r_a', p3: 'mantle_r_a'},
  mantle_l_b: {p1: 'mantle_l_b', p3: 'mantle_l_b'}, mantle_r_b: {p1: 'mantle_r_b', p3: 'mantle_r_b'},
};
// the core's own look channel (contract §0.4.7): p1_bulb / p3_sternum
export const CORE_MODELS = {p1_bulb: 'core_p1_bulb', p3_sternum: 'core_p3_sternum'};
export function sprites() { models(); return {...SP}; }
void [cosD, secC, sdUnion, sink];
