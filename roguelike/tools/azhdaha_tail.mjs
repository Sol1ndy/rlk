// TAIL region of the 야타용왕 (Azhdaha) rig (model.md §3.9, R2 critique §5): 8 segments (14.5 b) and the leafy tip.
//   * t1..t5: a broad, flattened body. The cross-section is a wide lens (2.0 b x 1.3 b at the root, 0.7 x 0.5 at t5):
//     the cream VENTRAL face (lower facets) carries the gold leaf veins (a midrib and nested chevrons opening toward
//     the root); the dark umber flanks and top carry overlapping scale plates. A row of big dark blades runs along the
//     ridge (0.95 b at the root) and a row of long feather plates lies along each flank, pointing back so each one
//     overlaps the next joint (the chain reads continuous when it curls 25-30 degrees per joint). Every segment starts
//     with a collar sunk in the previous one, so the outer side of a bend never opens.
//   * t6..t8 + tip: the last ~40 % is a dark gnarled branch (knots, broken twig stubs, gold flecks) with side twigs and
//     leaf clusters, densest at the tip: orange-gold Geo leaves; white-cyan crystal sprays under Cryo, violet blossoms
//     with sparks under Electro (the tail look).
//   * tail_skirt: the cream rump plate under the tail root, rigid with the PELVIS (not the tail: it still hangs between
//     the hind legs when the tail stands vertical, v3 f1560): a convex bell from the tail root down to ~0.7 b with a
//     lobed hem and the gold Y-fork of the midrib.
// Region interface: see azhdaha_body.mjs. Segment frames (azhdaha_pose.mjs solve): the joint at the origin, the segment
// along +Z (back), up = +Y (the dorsal ridge), the ventral face -Y; the tip continues t8's frame from its end. The skirt
// frame is the pelvis frame moved to the tail root.
import {loft, slab, toUnits, stroke, registerTile, registerWrap, rockBox, hash} from './azhdaha_shape.mjs';
import {PART_SCALE, TAIL_LEN, TAIL_PARTS} from './azhdaha_pose.mjs';
import {PAL, LOOK_PAL, C, clamp, smooth, mix, sink, lift, N, TRANSPARENT, creamPx, cells, onRect, r16} from './azhdaha_materials.mjs';
import {cardX, cardZ, faceEl} from './mboss_model_lib.mjs';

export const REGION = 'tail';
// [part, default model, brightness]: the body segments 13, the leafy branch 14 (warm-bright leaves, model.md §4.3)
export const PARTS = [...TAIL_PARTS.map(n => [n, n, ['t6', 't7', 't8', 'tip'].includes(n) ? 14 : 13]), ['tail_skirt', 'tail_skirt', 13]];
const TLOOKS = ['cryo', 'electro'];
const sfx = l => (l ? '_' + l : '');
// Per-part culling box (rigtech §2.5; R2 critique 1.8): the distal tail reaches past the rig-wide 30 x 12 box when it
// is laid out, swept or raised (tail_low, whip, tail slam, the pillar). Read by the builder via azhdaha_geometry.mjs.
export const CULL_BOX = Object.fromEntries(['t4', 't5', 't6', 't7', 't8', 'tip'].map(n => [n, {width: 44, height: 18}]));

// ---- profile ----------------------------------------------------------------------------------------------------------------
const CUM = TAIL_LEN.reduce((a, l) => [...a, a[a.length - 1] + l], [0]);          // joint positions along the chain
const BRANCH = 5;                                                                  // t6.. are the branch
// body cross-section at the joints of t1..t5 (blocks): half width, up (ridge), down (ventral)
const PW = [1.0, .86, .72, .6, .48, .36], PU = [.74, .63, .53, .44, .35, .27], PD = [.56, .48, .41, .34, .27, .2];
// branch radius at the joints of t6..t8 and the tip
const PB = [.34, .3, .26, .2, .14];
// piecewise-linear value of A (given at CUM[base], CUM[base + 1], ...) at chain position s
function at(A, s, base = 0) {
  const n = Math.min(A.length, CUM.length - base);
  let k = 0;
  while (k < n - 2 && CUM[base + k + 1] < s) k++;
  const s0 = CUM[base + k], s1 = CUM[base + k + 1];
  return A[k] + (A[k + 1] - A[k]) * clamp((s - s0) / (s1 - s0));
}
const prof = (s, k = 1) => { const w = at(PW, s), u = at(PU, s), d = at(PD, s); return [w * k, u * k, w * k, d * k]; };
export const tailProfile = s => (s <= CUM[BRANCH] ? prof(s) : Array(4).fill(at(PB, s, BRANCH)));

// ---- tiles ------------------------------------------------------------------------------------------------------------------
for (const l of ['', '_cryo', '_electro']) { registerTile('tailskin' + l, 64, 64, 32); registerTile('tbark' + l, 64, 64, 48); }
// the ventral face: a wrap-round sprite (u = around the 16 facets, v = along the segment); the cream facets are k = 9..15
registerWrap('tailbelly'); registerTile('tailbelly', 256, 128, 40);
const VENTRAL = th => Math.sin(th * Math.PI / 180) < -.5;      // facets k = 10..14

// ---- body segments ---------------------------------------------------------------------------------------------------------
function core(i, look) {
  const L = TAIL_LEN[i], s0 = CUM[i], s1 = CUM[i + 1];
  if (i >= BRANCH) {
    // the branch: an octagon with a gnarled wobble (offset middle station)
    const r0 = at(PB, s0, BRANCH), r1 = at(PB, s1, BRANCH), rm = (r0 + r1) / 2 * 1.08, j = (hash(i, 3) - .5) * .08, k2 = (hash(i, 7) - .5) * .06;
    return loft('z', [{a: -.28, r: r0 * .9}, {a: 0, r: r0}, {a: L * .5, r: rm, c: [j, k2]}, {a: L + .03, r: r1}],
      {n: 8, tex: 'tbark' + sfx(look), caps: i === TAIL_LEN.length - 1 ? '+' : '', seed: 401 + i * 7});
  }
  // a collar sunk in the previous segment (or the rump), three equal sections (each takes the profile at its middle,
  // so the taper steps by ~4 % only and needs no ledge rings), then a narrowed, capped end that tucks into the next
  // segment's collar: at a 25-30 degree curl the outer side shows a crease, not a protruding lip or an open end
  const st = [{a: -.4, r: prof(s0, .97)}, {a: 0, r: prof(s0, 1.02)}, {a: L / 3, r: prof(s0 + L / 3)}, {a: L * 2 / 3, r: prof(s0 + L * 2 / 3)},
    {a: L - .08, r: prof(s1)}, {a: L + .28, r: prof(s1, .84)}];
  for (const s of st) s.box = .12;
  // (the cap, hidden in the next collar, takes one dark tile: its ring quads overlap near the axis)
  return loft('z', st, {n: 16, ledges: false, caps: '+', ledgeTex: 'tailskin' + sfx(look), tex: (k, th) => (VENTRAL(th) ? 'tailbelly' : 'tailskin' + sfx(look)), seed: 201 + i * 7});
}

// ---- blades (dark umber, orange bases): one sheet of 4 cells, 64 x 64 each ----------------------------------------------------
// shapes in cell units (u along +Z = back, v up), each a tapered quadratic stroke from its base
const BL = [
  {p: [[.18, .02], [.3, .6], [.78, .98]], w: .2, pw: .9},       // 0 dorsal blade, broad base, curving back
  {p: [[.15, .02], [.42, .5], [.92, .82]], w: .19, pw: .8},     // 1 dorsal blade, lower and longer
  {p: [[.03, .2], [.45, .26], [.98, .6]], w: .13, pw: .7},      // 2 flank feather plate, long and low
  {p: [[.05, .1], [.35, .45], [.75, .9]], w: .16, pw: 1.1},     // 3 small jagged spur (branch stubs, distal)
].map(b => ({...b, S: stroke(Array.from({length: 17}, (_, i) => { const t = i / 16; return [0, 1].map(k => (1 - t) ** 2 * b.p[0][k] + 2 * (1 - t) * t * b.p[1][k] + t * t * b.p[2][k]); }), t => b.w * (1 - t) ** b.pw + .006)}));
// A blade of shape k, size S (blocks), its base at `base` on the plane X = base[0]; rot = [axis, deg] about the base.
function blade(look, k, base, S, {rot = null, half = .055, edge} = {}) {
  const spr = 'tblades' + sfx(look), [x, y, z] = base, b = BL[k];
  const rect = {u0: z - b.p[0][0] * S, u1: z + (1 - b.p[0][0]) * S, v0: y - b.p[0][1] * S, v1: y + (1 - b.p[0][1]) * S};
  const sd = (u, v) => b.S.sd((u - rect.u0) / S, (v - rect.v0) / S) * S;
  const els = slab({plane: 'x', at: x, rect, sd, half, sprite: spr, edge: edge || 'tailskin' + sfx(look), cell: Math.max(.07, S / 9), core: S > .35, inset: .7,
    rot: rot ? [rot[0], rot[1], base] : null});
  for (const e of els) for (const f of Object.values(e.faces)) if (f.texture === '#' + spr) { const [a, bb, c2, d] = f.uv; f.uv = [k * 4 + a / 4, bb, k * 4 + c2 / 4, d].map(v => +v.toFixed(4)); }
  return els;
}
// per body segment: the ridge row [frac along, size, shape]; the two side rows of the V-fan [frac, size] (upper flank,
// leaning out 45 degrees, set between the ridge blades, sizes alternating so the edge reads ragged, v3 23.6 s); the low
// flank plates [frac, size] (45 degrees, t1..t4)
const DORSAL = [[[.16, 1.05, 0], [.64, .97, 1]], [[.18, .96, 0], [.66, .88, 1]], [[.2, .9, 0], [.68, .8, 1]], [[.24, .8, 0], [.72, .7, 1]], [[.3, .7, 0], [.76, .58, 1]]];
const SIDE = [[[.4, 1.0], [.88, .82]], [[.42, .92], [.9, .74]], [[.45, .84], [.92, .66]], [[.45, .74], [.92, .58]], [[.55, .6]]];
const FLANK = [[[.25, 1.3]], [[.3, 1.15]], [[.35, 1.0]], [[.4, .85]], []];
function spikes(i, look) {
  if (i >= BRANCH) return [];
  const els = [], L = TAIL_LEN[i];
  DORSAL[i].forEach(([f, S, k], j) => {
    const s = CUM[i] + f * L, u = at(PU, s);
    // alternate a hair off the midline so the blades of neighbouring segments never share a plane
    els.push(...blade(look, k, [((i * 2 + j) % 2 ? -.03 : .03), u * .82, f * L], S));
  });
  for (const [f, S] of SIDE[i]) for (const side of [1, -1]) {
    const s = CUM[i] + f * L, w = at(PW, s), u = at(PU, s);
    els.push(...blade(look, (i + (side > 0 ? 0 : 1)) % 2, [side * w * .55, u * .5, f * L], S * (side > 0 ? 1 : .9), {rot: ['z', -side * 45], half: .05}));
  }
  for (const [f, S] of FLANK[i]) for (const side of [1, -1]) {
    const s = CUM[i] + f * L, w = at(PW, s), u = at(PU, s);
    // a long plate on the flank, leaning out 45 degrees, pointing back over the next joint
    els.push(...blade(look, 2, [side * w * .78, u * .1, f * L], S, {rot: ['z', -side * 45], half: .045}));
  }
  return els;
}

// ---- the branch: knots, stubs, twigs, leaf clusters ------------------------------------------------------------------------
// leaf clusters per branch part (5 = t6, 6 = t7, 7 = t8, 8 = tip): [z frac, angle round the axis (deg, 270 = ventral),
// out (blocks from the axis), size, sprite cell, twig]
const LEAVES = {
  5: [[.45, 200, .4, .85, 0, 1], [.85, 320, .45, .95, 1, 1]],
  6: [[.15, 255, .45, 1.0, 1, 1], [.45, 35, .38, .85, 0, 0], [.65, 290, .5, 1.05, 0, 1], [.9, 150, .48, 1.0, 1, 1]],
  7: [[.1, 225, .5, 1.05, 0, 1], [.35, 315, .5, 1.1, 1, 1], [.55, 95, .32, .9, 1, 0], [.75, 200, .48, 1.05, 0, 1], [.95, 330, .45, 1.0, 1, 1]],
  8: [[.15, 250, .38, 1.1, 1, 0], [.45, 30, .32, 1.0, 0, 0], [.7, 150, .34, 1.0, 1, 0], [.95, 275, .3, 1.15, 0, 0]],
};
const LEAF_SPR = l => 'leaf' + sfx(l || 'geo');
// one cluster: three crossed cut-out cards (front, side, flat), each turned a little for an irregular bush
function cluster(look, c, S, cell, seed) {
  const spr = LEAF_SPR(look), uvr = [cell * .5, 0, cell * .5 + .5, 1], h = S / 2, [x, y, z] = c;
  const g = a => (hash(seed, a) < .5 ? -22.5 : 22.5);
  const flat = faceEl([[x - h, y, z - h], [x + h, y, z + h]], {up: {tex: spr, fn: ([X, , Z]) => [16 * (uvr[0] + .5 * (X - x + h) / S), 16 * (Z - z + h) / S]},
    down: {tex: spr, fn: ([X, , Z]) => [16 * (uvr[0] + .5 * (X - x + h) / S), 16 * (Z - z + h) / S]}}, {shade: false, rot: ['x', g(3), c]});
  return [cardZ(spr, z, {X0: x - h, X1: x + h, Y0: y - h, Y1: y + h}, {uvr, flipU: hash(seed, 1) < .5, rot: ['y', g(1), c]}),
    cardX(spr, x, {Z0: z - h, Z1: z + h, Y0: y - h, Y1: y + h}, {uvr: [uvr[0], 0, uvr[2], 1], flipU: hash(seed, 2) < .5, rot: ['z', g(2), c]}), flat];
}
function branchBits(i, look, L) {
  const els = [], bark = 'tbark' + sfx(look), s0 = CUM[Math.min(i, 8)] || CUM[8];
  for (const [f, ang, out, S, cell, twig] of LEAVES[i] || []) {
    const z = f * L, a = ang * Math.PI / 180, dx = Math.cos(a), dy = Math.sin(a), c = [dx * out, dy * out, z + .05];
    if (twig) {
      // a side twig from the bark out to the cluster: a thin box turned 45 degrees toward its side
      const sx = Math.abs(dx) > Math.abs(dy);
      els.push(sx ? rockBox([0, dy * out * .6 - .035, z - .035], [dx * out * 1.05, dy * out * .6 + .035, z + .035], bark, {rot: ['z', (dx > 0 ? 1 : -1) * (dy > 0 ? 22.5 : -22.5), [0, 0, z]], seed: z * 13 + i})
        : rockBox([dx * out * .6 - .035, 0, z - .035], [dx * out * .6 + .035, dy * out * 1.05, z + .035], bark, {rot: ['x', (dy > 0 ? -1 : 1) * 22.5, [0, 0, z]], seed: z * 13 + i}));
    }
    els.push(...cluster(look, c, S, cell, i * 31 + f * 100));
  }
  return els;
}
// gnarls of a branch segment: knots on the bark and jagged black thorns (broken twig stubs) round the top and sides
function gnarl(i, look) {
  const L = TAIL_LEN[i], els = [], bark = 'tbark' + sfx(look);
  const n = i === 5 ? 4 : 3;
  for (let j = 0; j < n; j++) {
    const f = (j + .4) / n, s = CUM[i] + f * L, r = at(PB, s, BRANCH), side = (j + i) % 2 ? 1 : -1, h = hash(i, j, 5);
    if (j % 2 === 0) els.push(rockBox([side * r * .5, -r * .55, f * L - .13], [side * (r + .08), r * .4, f * L + .11], bark, {seed: 77 + i * 9 + j}));
    const S = (.5 + .25 * h) * (i === 7 ? .85 : 1);
    els.push(...blade(look, 3, [side * .02, r * .7, f * L - .08], S, {half: .035, edge: bark, rot: h < .5 ? ['z', side * 22.5] : null}));
    if (j < n - 1) els.push(...blade(look, 3, [side * r * .8, 0, (f + .5 / n) * L], S * .75, {half: .03, edge: bark, rot: ['z', -side * 45]}));
  }
  return els;
}
function tipPart(look) {
  // the terminal tuft: a tapering forked twig and the densest clusters (the leafy crown, the shells' muzzle)
  const bark = 'tbark' + sfx(look);
  return [...loft('z', [{a: -.2, r: .17}, {a: 0, r: .14}, {a: .45, r: .1, c: [.02, .03]}, {a: .85, r: .05}], {n: 8, tex: bark, caps: '+', seed: 501}),
    rockBox([-.03, -.03, .3], [.03, .32, .36], bark, {rot: ['x', -22.5, [0, 0, .33]], seed: 503}),
    ...branchBits(8, look, .9)];
}

// ---- the rump skirt (pelvis frame at the tail root) --------------------------------------------------------------------------
// The bell outline in the skirt's plane (u = X, v = Y from the tail joint): 1.9 b wide at the top, 3.0 b at the
// hem, a lobed (scalloped) hem ~2.05 b below the joint. sd < 0 inside (not exact, monotone enough for the core cells).
const SK = {rect: {u0: -1.6, u1: 1.6, v0: -1.8, v1: .15}, top: .1, bot: -1.74, z: .3, tilt: 22.5};
const skHalf = v => .95 + .55 * clamp((SK.top - v) / (SK.top - SK.bot)) ** 1.4;
const skHem = u => SK.bot + .13 * (1 - Math.cos(Math.min(Math.abs(u), 1.45) / .5 * Math.PI)) / 2 + .1 * smooth(1.1, 1.5, Math.abs(u));
const skSd = (u, v) => Math.max(Math.abs(u) - skHalf(v), v - SK.top, skHem(u) - v, Math.hypot(Math.max(0, Math.abs(u) - skHalf(v) + .25), Math.max(0, skHem(u) + .25 - v)) - .25);
function skirt() {
  // a thick cream plate hung from the tail joint, the bottom tucked 22.5 degrees forward under the rump; the painted
  // card on its back face carries the exact bell outline, the veins and the lobed hem (v3 f1560)
  const plate = slab({plane: 'z', at: SK.z, rect: SK.rect, sd: skSd, half: .22, sprite: 'tskirt', edge: 'cream', cell: .16, inset: .8, cards: '+', rot: ['x', SK.tilt, [0, 0, SK.z]]});
  // the rounded mass in front of the plate (the side view reads a full rump, not a hanging board); its back stays
  // in front of the tilted plate, its front inside the haunches
  // R3 seam: the mass's top reaches 0.1-0.15 b into the pelvis hull at every station (its skipped top facets stay
  // inside), and its front end is capped: from above-behind no gap opened between the rump and the skirt
  const mass = loft('z', [{a: SK.z - .42, r: [.95, .62, .95, .45], c: [0, -.7]}, {a: SK.z - .75, r: [1.22, .82, 1.22, .6], c: [0, -1.02]},
    {a: SK.z - 1.45, r: [1.18, .62, 1.18, .55], c: [0, -.98]}], {n: 16, tex: (k, th) => 'cream', caps: '-', seed: 621, ledges: true, skip: (k, th) => Math.sin(th * Math.PI / 180) > .7});
  return [...plate, ...mass];
}

// ---- region exports ---------------------------------------------------------------------------------------------------------
const U = (part, els) => toUnits(els, PART_SCALE[part]);
function segment(i, look) {
  if (i < BRANCH) return [...core(i, look), ...spikes(i, look)];
  return [...core(i, look), ...gnarl(i, look), ...branchBits(i, look, TAIL_LEN[i])];
}
export function models() {
  const M = {tail_skirt: U('tail_skirt', skirt())};
  for (const look of [null, ...TLOOKS]) {
    for (let i = 0; i < 8; i++) M['t' + (i + 1) + sfx(look)] = U('t' + (i + 1), segment(i, look));
    M['tip' + sfx(look)] = U('tip', tipPart(look));
  }
  return M;
}
export const LOOKS = {tail: Object.fromEntries(TAIL_PARTS.map(p => [p, {geo: p, cryo: p + '_cryo', electro: p + '_electro'}]))};
export const TINTED = {};
// phase 3: the blossoms glow (model.md §4.3); the dark bark and plates stay dark in their textures
export const LOOK_BRIGHT = {tail: {cryo: {t6: 15, t7: 15, t8: 15, tip: 15}, electro: {t6: 15, t7: 15, t8: 15, tip: 15}}};

// ---- sprites --------------------------------------------------------------------------------------------------------------------
const stoneOf = look => (look ? (t => LOOK_PAL[look].stone(clamp(.5 + t * .5))) : PAL.plate);   // phase 3 stays dark (critique 5.8)
const glowOf = look => (look ? LOOK_PAL[look].glow : null);
// overlapping scale plates, elongated along the axis (v), each lit toward its free (distal) edge with a dark crevice
function tailskin(look) {
  const R = stoneOf(look), G = glowOf(look);
  return (s, t) => {
    const cc = cells(s * 6, t * 3.2, 41, 0, .7);
    const k = clamp(1 - cc.d1 * 1.25);
    let c = R(.5 + .2 * (cc.id - .5) - .16 * k + .1 * (N.a(s * 9, t * 9) - .5));
    if (!look && cc.id > .8) c = mix(c, PAL.plateOr(.75), .35 * k);                   // a few amber-based plates (v3 f0705)
    const e = cc.d2 - cc.d1;
    if (e < .07) c = G && cc.id > .72 && e < .035 ? mix(c, G(.3), .6) : sink(c, .5 * (1 - e / .07));
    else if (e < .14) c = lift(c, .06);
    return c;
  };
}
// a blade: umber body lit along the leading edge, dark trailing edge, amber base, a pale (or glowing) rim
function bladeColour(b, x, y, look) {
  const d = b.S.sd(x, y);
  if (d > 0) return null;
  const n = b.S.near(x, y), R = stoneOf(look), G = glowOf(look);
  let c = R(.45 + .2 * (N.a(x * 30, y * 6) - .5));
  c = n.s > 0 ? mix(c, R(.18), .35 * clamp(1 + d / .05)) : mix(c, R(.85), .3);   // lit leading edge, dark trailing side
  if (Math.abs(n.s) < .012 && n.t > .08 && n.t < .9) c = mix(c, R(.2), .4);      // the ridge line
  if (!look) c = mix(c, PAL.plateOr(.35 + .4 * n.t), .75 * clamp(1 - n.t / .3));  // amber base
  if (d > -.016) c = G ? G(.15) : lift(c, .18);                                   // rim
  return c;
}
const bladeSheet = look => (s, t) => { const k = Math.min(3, Math.floor(s * 4)); return bladeColour(BL[k], s * 4 - k, 1 - t, look) || TRANSPARENT; };
// the ventral face of t1..t5: cream with the gold midrib and nested chevrons (apex toward the tip)
function tailbelly() {
  return (s, t) => {
    const th = (s * 16 - .5) * 22.5, x = (th - 270) / 90;                          // -0.75 .. 0.75 across the cream facets
    let c = mix(creamPx(s * 256, t * 128, PAL.cream, .6), PAL.cream(.42), .35);   // grey-cream (v3 f1560)
    c = mix(c, PAL.cream(.68), .6 * smooth(.2, .6, Math.abs(x)));                  // the face curls into the flanks
    if (Math.abs(x) > .64) return mix(c, PAL.cream(.8), .5);
    const mid = Math.abs(x) / .02;
    const ch = ((t + Math.abs(x) * .85) / .5) % 1, chev = Math.min(ch, 1 - ch) / .035;
    const d = Math.min(mid, Math.abs(x) < .6 ? chev : 9);
    if (d < 1) c = mix(PAL.gold(.25), PAL.gold(.55), d);
    else if (d < 1.9) c = mix(c, PAL.gold(.85), .35 * (1.9 - d));
    return c;
  };
}
// the rump skirt (painted in its plane, u = X, v = Y): grey-cream, darker to the sides and the hem, the midrib forking
// into a Y with a chevron above the fork, rounded pebble lobes along the hem
function skirtPaint() {
  return (u, v) => {
    const d = skSd(u, v);
    if (d > 0) return null;
    const ax = Math.abs(u), hw = skHalf(v), t = clamp((SK.top - v) / (SK.top - SK.bot));
    let c = mix(creamPx(u * 48 + 300, v * 48, PAL.cream, .8), PAL.cream(.42), .35);
    c = mix(c, PAL.cream(.72), .7 * smooth(.45, 1, ax / hw));
    c = mix(c, PAL.cream(.6), .3 * smooth(.35, .9, t));
    const hem = skHem(u), lobe = v - hem;
    if (lobe < .3) {
      // pebble lobes: lit tops, dark seams between them
      const k = lobe / .3, seam = Math.abs(((u + 1.45) / .5) % 1 - .5);
      c = mix(c, PAL.cream(.3 + .4 * (1 - k)), .55);
      if (seam > .44 || (lobe > .27 && lobe < .3)) c = sink(c, .35);
    }
    if (d > -.035) c = sink(c, .3);
    // veins
    const fork = v < -.95 ? Math.abs(ax - (-.95 - v) * .75) : 9, mid = v >= -1.0 ? ax : 9, chev = Math.abs(v + .55 + ax * .5);
    const dv = Math.min(mid / .03, fork / .034, ax < .8 ? chev / .026 : 9);
    if (dv < 1 && lobe > .32) c = mix(PAL.gold(.25), PAL.gold(.55), dv);
    else if (dv < 1.8 && lobe > .32) c = mix(c, PAL.gold(.85), .35 * (1.8 - dv));
    return c;
  };
}
// bark: near-black brown with long grain, knot rings, small gold flecks (v3 f1683); Cryo / Electro: cold dark with
// sparse glowing cracks
function tbark(look) {
  const R = look ? (t => LOOK_PAL[look].stone(clamp(.55 + t * .45))) : PAL.branch, G = glowOf(look);
  return (s, t) => {
    const g = N.c(s * 10, t * 2.5);
    let c = R(.45 + .5 * (g - .5) + .12 * (N.a(s * 30, t * 30) - .5));
    if (Math.abs(g - .5) < .025) c = G ? mix(c, G(.25), .7) : sink(c, .45);
    const fl = cells(s * 5, t * 9, 59, 0, .9);
    if (!look && fl.id > .86 && Math.abs((s * 5 % 1) - (t * 9 % 1) * .3 - .4) < .07 && fl.d1 < .3) c = PAL.gold(.35 + .3 * fl.d1);
    return c;
  };
}
// leaf sprays (alpha cut, two variants side by side): drooping twigs from the top centre with leaves along them and
// gaps between (v3 f1683): Geo autumn leaves; Cryo slim crystal shards; Electro 5-petal blossoms with sparks
const SPRAYS = [0, 1].map(v => {
  const tw = [[.5, .9, .14 + .06 * v, .3], [.5, .9, .5 + .05 * v, .06], [.5, .9, .86 - .05 * v, .32], [.5, .9, .3 + .1 * v, .62], [.5, .9, .72, .64 - .08 * v]];
  const leaves = [];
  tw.forEach(([x0, y0, x1, y1], j) => {
    const n = 8 + (j % 2);
    for (let i = 1; i <= n; i++) {
      const t = i / n, sag = .12 * Math.sin(t * Math.PI) * (j % 2 ? 1 : -1);
      const x = x0 + (x1 - x0) * t + sag * .3, y = y0 + (y1 - y0) * t - Math.abs(sag) * .4;
      const dir = Math.atan2(y1 - y0, x1 - x0) + (hash(v, j, i) - .5) * 1.6 + (i % 2 ? .5 : -.5);
      leaves.push({x: x + (hash(v, j, i, 6) - .5) * .1, y: y + (hash(v, j, i, 7) - .5) * .1, a: dir, s: .1 + .06 * hash(v, j, i, 2), h: hash(v, j, i, 3), d: hash(v, j, i, 4)});
    }
  });
  leaves.sort((a, b) => a.d - b.d);           // painted back to front
  return {tw, leaves};
});
function leafCluster(look) {
  const R = look === 'cryo' ? LOOK_PAL.cryo.bloom : look === 'electro' ? LOOK_PAL.electro.bloom : PAL.leaf;
  return (s, t) => {
    const v = s < .5 ? 0 : 1, x = (s - v * .5) * 2, y = 1 - t, sp = SPRAYS[v];
    for (let i = sp.leaves.length - 1; i >= 0; i--) {
      const P = sp.leaves[i], dx = x - P.x, dy = y - P.y, ca = Math.cos(P.a), sa = Math.sin(P.a);
      const u = (dx * ca + dy * sa) / P.s, w = (-dx * sa + dy * ca) / P.s;
      if (look === 'cryo') {
        // a slim crystal shard, pale core, cyan edges
        const half = .32 * (1 - Math.abs(u));
        if (Math.abs(u) < 1 && Math.abs(w) < half) return R(clamp(.05 + .55 * Math.abs(w) / half * .6 + .3 * P.h * Math.abs(u)));
      } else if (look === 'electro') {
        const r = Math.hypot(u, w) * 1.1, th = Math.atan2(w, u), petal = .5 + .5 * Math.abs(Math.cos(th * 2.5));
        if (r < petal) return r < .22 ? LOOK_PAL.electro.spark : R(clamp(.1 + r * .5 + .3 * P.h));
      } else {
        // a pointed leaf (lemon outline) with a midrib and a dark rim, tone by depth
        const q = u * u + (w * w) / (.16 * (1 - .55 * u * u));
        if (Math.abs(u) < 1 && q < 1) {
          let c = PAL.leaf(clamp(.08 + .55 * P.d * .7 + .25 * P.h + .18 * (u + 1) / 2));
          if (q > .72) c = PAL.leaf(clamp(.75 + .25 * P.h));
          else if (Math.abs(w) < .045 && u > -.85) c = PAL.leaf(clamp(.55 + .2 * P.h));
          return c;
        }
      }
    }
    // the twigs (drawn under the leaves)
    for (const [x0, y0, x1, y1] of sp.tw) {
      const ex = x1 - x0, ey = y1 - y0, l2 = ex * ex + ey * ey, k = clamp(((x - x0) * ex + (y - y0) * ey) / l2);
      if (Math.hypot(x - x0 - k * ex, y - y0 - k * ey) < .016 * (1.3 - k)) return look ? R(.95) : PAL.branch(.35);
    }
    return TRANSPARENT;
  };
}
export function sprites() {
  const S = {tailbelly: [256, 128, tailbelly(), false], tskirt: [r16((SK.rect.u1 - SK.rect.u0) * 48), r16((SK.rect.v1 - SK.rect.v0) * 48), onRect(SK.rect, skirtPaint()), false]};
  for (const look of [null, ...TLOOKS]) {
    S['tailskin' + sfx(look)] = [64, 64, tailskin(look), false];
    S['tblades' + sfx(look)] = [256, 64, bladeSheet(look), false];
    S['tbark' + sfx(look)] = [64, 64, tbark(look), false];
    S[LEAF_SPR(look)] = [128, 64, leafCluster(look), false];
  }
  return S;
}
