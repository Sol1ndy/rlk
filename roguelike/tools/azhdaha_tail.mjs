// TAIL region of the 야타용왕 (Azhdaha) rig: 8 segments (14.5 b) and the leafy tip (model.md §3.9): a dark umber
// tapering chain with a row of blade spikes on top that shrink toward the tip, the broad cream ventral fin with gold
// leaf veins under t1-t5 (3.1 b wide at the root), and the last ~40 % as a dark gnarled branch with side twigs and leaf
// clusters (orange-gold Geo leaves; white-cyan crystal blossoms under Cryo, violet blossoms under Electro).
// Region interface: see azhdaha_body.mjs. Segment frames (azhdaha_pose.mjs solve): the joint at the origin, the segment
// along +Z (back), up = +Y; the tip continues t8's frame from its end.
import {loft, slab, crossCards, rockBox, toUnits, retex, stroke, registerTile, hash} from './azhdaha_shape.mjs';
import {PART_SCALE, TAIL_LEN, TAIL_PARTS} from './azhdaha_pose.mjs';
import {PAL, LOOK_PAL, C, clamp, smooth, mix, lift, sink, N, onRect, TRANSPARENT, creamPx, platePx, goldPx, cells} from './azhdaha_materials.mjs';
import {abox} from './mboss_model_lib.mjs';

export const REGION = 'tail';
export const PARTS = TAIL_PARTS.map(n => [n, n, n === 'tip' || n === 't8' ? 14 : 13]);
const TLOOKS = ['cryo', 'electro'];
const sfx = l => (l ? '_' + l : '');
for (const l of ['', '_cryo', '_electro']) registerTile('tailskin' + l, 64, 64, 32);
// core radius along the chain: 0.75 at the root, 0.13 at the tip (model.md §3.9: core 1.4 -> 0.8 mid -> 0.25 branch)
const RAD = [.75, .65, .56, .47, .39, .31, .24, .18, .13];
const CUM = TAIL_LEN.reduce((a, l) => [...a, a[a.length - 1] + l], [0]);
const FIN_END = CUM[5];               // the fin runs under t1..t5 (9.8 b)
const finHalf = z => 1.55 - 1.0 * (z / FIN_END) ** .8 - .3 * smooth(.75, 1, z / FIN_END);   // 1.55 -> ~0.25
const BRANCH = 5;                     // t6.. are the branch

// ---- segment core ---------------------------------------------------------------------------------------------------------------
function core(i, look) {
  const L = TAIL_LEN[i], r0 = RAD[i], r1 = RAD[i + 1], br = i >= BRANCH;
  const R = (r, k = 1) => [r * k, r * (br ? .95 : .9) * k, r * k, r * (br ? .95 : .72) * k];
  const tex = br ? 'bark' + sfx(look) : (k, th) => (Math.sin(th * Math.PI / 180) < -.5 ? 'cream' : 'tailskin' + sfx(look));
  // a collar reaching back into the previous segment hides the outer gap when the chain bends
  return loft('z', [{a: -.45 * r0, r: R(r0, .72)}, {a: -.12, r: R(r0, 1.0)}, {a: L * .5, r: R((r0 + r1) / 2, 1.03)}, {a: L + .04, r: R(r1, .98)}],
    {n: br ? 8 : 16, tex, caps: i === TAIL_LEN.length - 1 ? '+' : '', seed: 201 + i * 7});
}
// ---- ventral fin (plane y under the core): one long leaf sprite, each segment shows its slice ---------------------------------
const FIN_RECT = {u0: -1.6, u1: 1.6, v0: -.2, v1: FIN_END + .2};   // u = X, v = Z along the straightened tail
const finSd = (x, z) => {
  if (z < -.15 || z > FIN_END + .1) return 1;
  const h = finHalf(clamp(z, 0, FIN_END)) * (1 - .06 * Math.cos(z * 4.2) ** 2);     // a gently lobed edge
  return Math.abs(x) - h;
};
function fin(i) {
  if (i >= 5) return [];
  const z0 = CUM[i], L = TAIL_LEN[i], y = -RAD[i] * .62;
  const rect = {u0: FIN_RECT.u0, u1: FIN_RECT.u1, v0: FIN_RECT.v0 - z0, v1: FIN_RECT.v1 - z0};
  return slab({plane: 'y', at: y, rect, sd: (x, z) => finSd(x, z + z0), half: .09, sprite: 'fin', edge: 'cream', cell: .14, clip: {v0: -.12, v1: L + .06}});
}
function finPaint() {
  return (x, z) => {
    if (finSd(x, z) > 0) return null;
    let c = creamPx(x * 50 + 9, z * 50, PAL.cream, .5);
    const h = finHalf(clamp(z, 0, FIN_END)), a = Math.abs(x) / Math.max(.05, h);
    c = mix(c, PAL.cream(.55), .45 * a ** 3);                                // curls away at the edges
    // gold veins: a midrib and nested chevrons opening toward the root (upward when the tail is raised)
    const mid = Math.abs(x);
    const chev = Math.abs(((z - Math.abs(x) * .9) / .75) % 1);
    let d = Math.min(mid / .05, Math.min(chev, 1 - chev) * .75 / .045);
    if (a > .85) d = 9;
    if (d < 1) c = mix(PAL.gold(.25), PAL.gold(.55), d);
    if (finSd(x, z) > -.04) c = sink(c, .25);
    return c;
  };
}
// ---- top spikes (blade sheet of 4 shapes, cells 64 x 64) ------------------------------------------------------------------------
const TSP = [{c: [.42, .5], t: [.82, .95], w: .25}, {c: [.4, .55], t: [.92, .8], w: .27}, {c: [.45, .5], t: [.7, 1], w: .2}, {c: [.4, .5], t: [.95, .7], w: .3}];
const TS = TSP.map(b => { const pts = Array.from({length: 13}, (_, i) => { const t = i / 12; return [0, 1].map(k => (1 - t) ** 2 * [.3, 0][k] + 2 * (1 - t) * t * b.c[k] + t * t * b.t[k]); });
  const S = stroke(pts, t => b.w * (1 - t) ** .85); return {...b, S}; });
function spike(look, [x, y, z], L, k, splay = 0) {
  const spr = 'tspikes' + sfx(look), rect = {u0: z - .3 * L, u1: z + .7 * L, v0: y, v1: y + L};
  const sd = (u, v) => TS[k].S.sd((u - rect.u0) / L, (v - y) / L) * L;
  const els = slab({plane: 'x', at: x, rect, sd, half: .07, sprite: spr, edge: 'tailskin' + sfx(look), cell: Math.max(.1, L / 7), core: L > .45, rot: splay ? ['z', splay, [x, y, z]] : null});
  for (const e of els) for (const f of Object.values(e.faces)) if (f.texture === '#' + spr) { const [a, b, c2, d] = f.uv; f.uv = [k * 4 + a / 4, b, k * 4 + c2 / 4, d].map(v => +v.toFixed(4)); }
  return els;
}
function spikeColour(b, x, y, look) {
  const d = b.S.sd(x, y);
  if (d > 0) return null;
  const n = b.S.near(x, y), R = look ? LOOK_PAL[look].stone : PAL.plate;
  let c = platePx(x * 40, y * 40, R);
  c = n.s > 0 ? mix(c, R(.2), .3) : mix(c, R(.75), .25);
  if (d > -.02) c = look ? LOOK_PAL[look].glow(.25) : sink(c, .4);
  return c;
}
const spikeSheet = look => (s, t) => { const k = Math.min(3, Math.floor(s * 4)); return spikeColour(TS[k], s * 4 - k, 1 - t, look) || TRANSPARENT; };
// per segment: [z (fraction of the length), L, shape] on the ridge; side pairs [z, L, shape] splayed 45
const SPK = [[[.2, .9, 0], [.68, .8, 1]], [[.2, .72, 2], [.7, .64, 0]], [[.25, .55, 1], [.75, .5, 3]], [[.45, .42, 0]], [[.5, .3, 2]]];
const SIDE = [[[.45, .5, 3]], [[.45, .42, 1]], [[.5, .32, 3]], [], []];
function spikes(i, look) {
  if (i >= 5) return [];
  const els = [], r0 = RAD[i], r1 = RAD[i + 1], L = TAIL_LEN[i];
  for (const [f, h, k] of SPK[i]) { const r = r0 + (r1 - r0) * f; els.push(...spike(look, [0, r * .78, f * L], h, k)); }
  for (const [f, h, k] of SIDE[i]) for (const s of [1, -1]) { const r = r0 + (r1 - r0) * f; els.push(...spike(look, [s * r * .6, r * .55, f * L], h, k, -s * 45)); }
  return els;
}
// ---- branch: twigs and leaf clusters ------------------------------------------------------------------------------------------
// leaves per segment (t6, t7, t8, tip): [x, y, z, size, twig dir] in the segment frame
const LEAVES = {
  5: [[.35, .15, 1.0, .85, 1]],
  6: [[-.38, .2, .45, .9, -1], [.32, .35, 1.25, .8, 1]],
  7: [[.36, .25, .55, .9, 1], [-.34, .4, 1.15, .85, -1]],
  8: [[0, .45, .35, 1.05, 0], [.42, .15, .55, .8, 1], [-.4, .2, .7, .8, -1], [0, .05, 1.0, .75, 0]],
};
const LEAF_SPR = {null: 'leaf_geo', cryo: 'leaf_cryo', electro: 'leaf_electro'};
function branchBits(i, look) {
  const els = [], bark = 'bark' + sfx(look);
  for (const [x, y, z, s, dir] of LEAVES[i] || []) {
    // a twig from the core out to the cluster (a thin box turned 45 degrees about Z toward its side)
    if (dir) els.push(rockBox([0, -.04, z - .04], [x * 1.1, .04, z + .04], bark, {rot: ['z', -dir * 22.5, [0, 0, z]], seed: z * 10}));
    else els.push(rockBox([-.04, 0, z - .04], [.04, y + .1, z + .04], bark, {seed: z * 10}));
    els.push(...crossCards(LEAF_SPR[look], [x, y, z], s, s, {three: true, flip: dir < 0}));
  }
  return els;
}
function tipPart(look) {
  // the terminal tuft: a short forked twig and four clusters
  const bark = 'bark' + sfx(look);
  return [...loft('z', [{a: -.1, r: .13}, {a: .5, r: .1}, {a: .9, r: .06}], {n: 8, tex: bark, caps: '+', seed: 301}), ...branchBits(8, look)];
}

// ---- region exports -------------------------------------------------------------------------------------------------------------
const U = (part, els) => toUnits(els, PART_SCALE[part]);
function segment(i, look) { return [...core(i, look), ...fin(i), ...spikes(i, look), ...branchBits(i, look)]; }
export function models() {
  const M = {};
  for (const look of [null, ...TLOOKS]) {
    for (let i = 0; i < 8; i++) M['t' + (i + 1) + sfx(look)] = U('t' + (i + 1), segment(i, look));
    M['tip' + sfx(look)] = U('tip', tipPart(look));
  }
  return M;
}
export const LOOKS = {tail: Object.fromEntries(TAIL_PARTS.map(p => [p, {geo: p, cryo: p + '_cryo', electro: p + '_electro'}]))};
export const TINTED = {};
export const LOOK_BRIGHT = {tail: {cryo: {t6: 15, t7: 15, t8: 15, tip: 15}, electro: {t6: 15, t7: 15, t8: 15, tip: 15}}};

// ---- sprites --------------------------------------------------------------------------------------------------------------------
function tailskin(look) {
  const R = look ? LOOK_PAL[look].stone : PAL.plate;
  return (s, t) => {
    const cc = cells(s * 7, t * 7, 21, 7);
    let c = R(.42 + .18 * (cc.id - .5) - .12 * clamp(1 - cc.d1 * 1.3));
    if (cc.d2 - cc.d1 < .08) c = look ? mix(c, LOOK_PAL[look].glow(.4), .45) : sink(c, .45);
    return c;
  };
}
// leaf clusters (alpha cut): Geo autumn leaves, Cryo crystal blossoms, Electro violet blossoms with sparks
function leafCluster(look) {
  const R = look === 'cryo' ? LOOK_PAL.cryo.bloom : look === 'electro' ? LOOK_PAL.electro.bloom : PAL.leaf;
  const leaves = Array.from({length: 13}, (_, i) => ({x: .5 + .36 * Math.cos(i * 2.4) * Math.sqrt((i + 1) / 13), y: .5 + .34 * Math.sin(i * 2.4) * Math.sqrt((i + 1) / 13), a: i * 1.7, s: .14 + .05 * hash(i, 3)}));
  return (s, t) => {
    const x = s, y = 1 - t;
    // stem twigs
    if (Math.abs(x - .5) < .02 && y < .5) return look ? R(.85) : PAL.branch(.4);
    for (let i = leaves.length - 1; i >= 0; i--) {
      const L = leaves[i], dx = x - L.x, dy = y - L.y, ca = Math.cos(L.a), sa = Math.sin(L.a);
      const u = (dx * ca + dy * sa) / L.s, v = (-dx * sa + dy * ca) / L.s;
      if (look) {
        // crystal / blossom: a 5-petal star
        const r = Math.hypot(u, v), th = Math.atan2(v, u), petal = .55 + .45 * Math.abs(Math.cos(th * 2.5));
        if (r < petal) { let c = R(clamp(.1 + r * .7)); if (r < .2) c = look === 'electro' ? LOOK_PAL.electro.spark : R(0); return c; }
      } else {
        // a pointed oval leaf with a midrib
        if (u * u / 1 + v * v / .2 < 1 && Math.abs(u) < 1) { let c = PAL.leaf(clamp(.15 + .5 * hash(i, 9) + .3 * (u + 1) / 2)); if (Math.abs(v) < .05) c = PAL.leaf(.85); return c; }
      }
    }
    return TRANSPARENT;
  };
}
export function sprites() {
  const S = {};
  for (const look of [null, ...TLOOKS]) {
    S['tailskin' + sfx(look)] = [64, 64, tailskin(look), false];
    S['tspikes' + sfx(look)] = [256, 64, spikeSheet(look), false];
    S[LEAF_SPR[look]] = [64, 64, leafCluster(look), false];
  }
  const fr = FIN_RECT;
  S.fin = [r16((fr.u1 - fr.u0) * 40), r16((fr.v1 - fr.v0) * 40), (s, t) => finPaint()(fr.u0 + s * (fr.u1 - fr.u0), fr.v0 + t * (fr.v1 - fr.v0)) || TRANSPARENT, false];
  return S;
}
const r16 = x => Math.min(512, Math.max(16, Math.ceil(x / 16) * 16));
