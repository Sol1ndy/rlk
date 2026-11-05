// Sprites of the 홍련 (Scarlet) rig (S:hr/PLAN.md §2.2 paint guide, §2.8 atlas share). S2c (11-05): the body wears the
// user's own Minecraft skin (tools/scarlet_skin.mjs, written unchanged by build_scarlet_rig.mjs as
// textures/mboss/scarlet/skin.png; never repainted), so this file paints only what the rig makes itself: the hat (brim
// weave, crown, knot), its bead strings, the sash tails, the sword (blade, guard, grip, glow overlays), the scabbard, the
// cup and the bottle, the ghost texture and the small face overlays (face_fx). Their shapes are S2a's; their colours are
// matched to the skin (its whites, lilacs, blacks, crimson and pale gold) — a palette match, not the original character's
// props (PLAN §1.5). Painted procedurally (no external art); every painter is (u, v) in 0..1, v down the sprite. Card
// conventions (mboss_model_lib / scarlet_geometry): a front card reads as painted from the front (u = her right -> her
// left = screen left -> right), a back card from behind (u = her left -> her right); v = top -> bottom. Lighting is not
// baked (the arena lights her).
import {paintSpriteSet, C, clamp, smooth, mix, fbm, TRANSPARENT} from './mboss_paint_lib.mjs';
import {TILE_SIZES, WRAP_SPRITES} from './scarlet_geometry.mjs';

export const TEX_DIR = 'assets/rlk/textures/mboss/scarlet';
export const spriteId = n => `rlk:mboss/scarlet/${n}`;
const T = TRANSPARENT;
const fr = x => x - Math.floor(x);
const N = {a: fbm(7101), b: fbm(7213), c: fbm(7307), d: fbm(7411), e: fbm(7529)};
const sink = (c, k) => mix(c, [8, 6, 10, 255], clamp(k));
const withA = (c, a) => [c[0], c[1], c[2], Math.round(clamp(a) * 255)];

// ---- palette (base / shade / highlight). S2c: the props' colours follow the skin — white / lilac-white (its cap and
// outfit), black (its bands), crimson #A73041 (its sash), violet #8168B9 / #6A5B9B (its accents), pale gold #F4EAB8 (its
// trims). The hat keeps CIE76 dE >= 10 from the original's parchment hat #E6DCCF and the gold from its gold strip #CDB78C
// (PLAN §1.5; test_rig.py checks the declared and the painted means) -----------------------------------------------------
export const PAL = {
  crimson: [C('#A73041'), C('#78202E'), C('#C9475A')],
  lotus: [C('#B83448'), C('#7E1E30'), C('#F08AA0')], gold: C('#F2E3B0'),
  weave: [C('#ECE9F4'), C('#CFC8DD'), C('#B9A6DA')], crown: C('#F2F0F7'), band: [C('#2C292E'), C('#1A181C'), C('#4E4A55')],
  knot: [C('#D23A55'), C('#FF5A78'), C('#8E1C30'), C('#FF9AB0')],
  jasper: C('#8168B9'), amber: C('#F4EAB8'), blade: [C('#CCC8D2'), C('#9C7BC8'), C('#F4F2F8'), C('#6E6874')],
  iron: C('#2C2A2E'), brass: [C('#EEDFAA'), C('#B9A472'), C('#FFF6D8')], cord: C('#6A5B9B'), ray: C('#EEE9DE'),
  scab: [C('#1C1A1E'), C('#8168B9'), C('#4A4652')], porcelain: C('#F4F3F8'), cobalt: C('#6A5B9B'),
  skinFx: [C('#F0C9CA'), C('#302A2A'), C('#D99A9E')],
  ghost: [C('#C97EDD'), C('#9A4FB8'), C('#F0C8FA')],
};
// the base paints per role, for the palette-distance check (test_rig.py reads the manifest's paint_roles): the hat and the
// gold are ours; the body roles are the user's skin (its own pixels, the user's choice: exempt, value 'skin')
export const PAINT_ROLES = {hat_top: ['#ECE9F4', '#F2F0F7'], bodysuit: 'skin', thigh_highs: 'skin', tasset: 'skin', gold_strip: '#EEDFAA', hair: 'skin'};

// ---- material helpers -----------------------------------------------------------------------------------------------------
const sheen = (c3, u, v, k = 1) => { const [b, s, h] = c3; const x = Math.sin((u * 1.3 + v * .4) * Math.PI * 2); return x > 0 ? mix(b, h, .5 * x * x * k) : mix(b, s, -.5 * x * k); };
// a stylised red lotus (five petals with pink tips round a gold-thread centre) inside a roundel of radius 1 at (dx, dy)
function lotusAt(dx, dy, {petals = 5, rot = -90, ring = true, bg = null} = {}) {
  const r = Math.hypot(dx, dy);
  if (r > 1) return null;
  const ang = Math.atan2(dy, dx) * 180 / Math.PI - rot, seg = 360 / petals;
  const a = ((ang % seg) + seg) % seg - seg / 2;                          // angle to the nearest petal's axis
  const pw = .58 * Math.cos(Math.min(Math.PI / 2, Math.abs(a) * Math.PI / seg));
  if (ring && r > .88) return mix(PAL.gold, PAL.brass[2], .3);
  if (r < .2) return mix(PAL.gold, PAL.brass[2], .4 * (1 - r / .2));
  const t = (r - .2) / .62;
  if (t < 1 && Math.abs(a) / (seg / 2) < pw * (1 - .35 * t) + .25 * (1 - t)) {
    let c = mix(PAL.lotus[1], PAL.lotus[0], smooth(0, .5, t));
    c = mix(c, PAL.lotus[2], smooth(.62, 1, t));
    if (Math.abs(a) < 2.5) c = mix(c, PAL.lotus[1], .35);
    return c;
  }
  return bg;
}

// ---- tiles ----------------------------------------------------------------------------------------------------------------
const TILE_PAINT = {
  crimson: (u, v) => sheen(PAL.crimson, u, v, .7),
  brass: (u, v) => mix(PAL.brass[0], v < .3 ? PAL.brass[2] : PAL.brass[1], v < .3 ? .4 * (1 - v / .3) : .35 * (v - .3) / .7),
  iron: (u, v) => mix(PAL.iron, C('#4A4550'), .3 * N.b(u * 4, v * 4)),
  lacquer: (u, v) => mix(PAL.scab[0], PAL.scab[2], .35 * Math.pow(Math.max(0, Math.sin((u * .8 + v * .3) * Math.PI * 2)), 6)),
  // white lacquer (the hat crown's top and bottom discs): a soft lilac sheen
  lacquer_w: (u, v) => mix(PAL.crown, PAL.weave[1], .35 * Math.pow(Math.max(0, Math.sin((u * .8 + v * .3) * Math.PI * 2)), 6) + .08 * N.a(u * 3, v * 3)),
  steel: (u, v) => mix(PAL.blade[0], PAL.blade[2], .3 * Math.abs(Math.sin(u * 7 + v * 2))),
  porcelain: (u, v) => mix(PAL.porcelain, C('#E4E2F0'), .25 * N.c(u * 3, v * 3)),
};
// ---- WRAP sprites (u round the loft: 0..1 = facet 0..n; v along the loft: 0 = its first station) -------------------------------
const WRAP_PAINT = {
  // the crown: white lacquer with one lilac highlight stripe; the black silk band at the bottom (v > 0.81)
  crown: (u, v) => { if (v > .81) { let c = sheen(PAL.band, u * 4, v, .7); if (v < .83 || v > .985) c = sink(c, .35); return c; }
    let c = mix(PAL.crown, PAL.weave[1], .22 * N.a(u * 8, v * 3));
    const s = Math.abs(fr(u) - .58); if (s < .025) c = mix(c, PAL.weave[2], .5 * (1 - s / .025) * (.6 + .4 * (1 - v)));
    if (v < .03) c = mix(c, PAL.weave[1], .4);
    return c; },
  // the grip: violet cord in a diamond pattern over ivory ray skin
  grip: (u, v) => { const a = fr(u * 4 + v * 6), b = fr(u * 4 - v * 6); const cord = Math.min(Math.abs(a - .5), Math.abs(b - .5)) > .32;
    let c = cord ? mix(PAL.cord, C('#8A78BE'), .3 * N.b(u * 8, v * 8)) : mix(PAL.ray, C('#D2CCC0'), .4 * N.c(u * 12, v * 12));
    if (!cord && fr(u * 24) < .12) c = mix(c, C('#BAB4A8'), .3); return c; },
};

// ---- cards ----------------------------------------------------------------------------------------------------------------------
// sash tails (16 x 64): the skin's crimson, folds; p2 a glowing edge
function sashTail(p2) {
  return (u, v) => {
    if (v > .985) return T;
    let c = sheen(PAL.crimson, u, v * 2, .6);
    if (Math.abs(fr(v * 5) - .5) < .06) c = mix(c, PAL.crimson[1], .4);
    if (u < .14 || u > .86) c = p2 ? mix(PAL.knot[1], C('#FFC0CC'), .25) : sink(c, .25);
    return c;
  };
}
const BRIM_PX = 128, BRIM_R = .8;
// coverage of a brim square at (u, v) on a px x px grid, decided at the pixel centre: 'weave', 'rib' (the 1.2-px radial rib
// on a wedge boundary, painted by both neighbours), 'rim' (the opaque inner / outer bands) or null (clear)
function brimMask(u, v, px) {
  const pxu = (Math.floor(u * px) + .5) / px, pxv = (Math.floor(v * px) + .5) / px;
  const X = (pxu - .5) * 2 * BRIM_R, Z = (pxv - .5) * 2 * BRIM_R, r = Math.hypot(X, Z);
  if (r > BRIM_R - .004 || r < .2) return null;
  const ang = ((Math.atan2(Z, X) * 180 / Math.PI) % 360 + 360) % 360;
  const off = ((ang - 45) % 90 + 90) % 90, d = Math.min(off, 90 - off);
  const perp = Math.abs(Math.sin((d - 11.25) * Math.PI / 180)) * r * px / (2 * BRIM_R);
  const inWedge = d <= 11.25, onRib = Math.abs(d - 11.25) < 3 && perp < 1.2;
  if (!inWedge && !onRib) return null;
  if (onRib) return 'rib';
  return r > BRIM_R - .022 || r < .225 ? 'rim' : 'weave';
}
// the brim (128 x 128 over X, Z -0.8..0.8, translucent): a white 백립-style weave (fine lilac-white horsehair / ramie),
// concentric rings and radial ribs in lilac-grey, a lilac sheen on the outer rim; ONLY the corner wedges (|angle - 45 - 90 n|
// <= 11.25) and the 1.2-px ribs on their boundaries are painted (the four squares tile the disc); the centre r < 0.2 is
// clear. Coverage is decided at the pixel centre (hard edges, no seam of partial alpha); the weave alpha 215, the ribs and
// the rim opaque.
function brim(u, v) {
  const m = brimMask(u, v, BRIM_PX);
  if (!m) return T;
  const pxPerB = BRIM_PX / (2 * BRIM_R);
  const Xs = (u - .5) * 2 * BRIM_R, Zs = (v - .5) * 2 * BRIM_R, rs = Math.hypot(Xs, Zs), as = Math.atan2(Zs, Xs);
  let c = mix(PAL.weave[0], PAL.weave[1], .3 * N.c(Xs * 9, Zs * 9));
  const ring = Math.abs(fr(rs * pxPerB / 8) - .5);
  if (ring < .12) c = mix(c, C('#C2BAD2'), .55);
  const rib = Math.abs(fr(as / (2 * Math.PI) * 64) - .5);
  if (rib > .42) c = mix(c, C('#B4ABC6'), .5);
  if (rs > BRIM_R - .03) c = mix(c, PAL.weave[2], .6 * smooth(BRIM_R - .03, BRIM_R - .005, rs));
  if (m === 'rib') return mix(C('#B0A6C4'), PAL.weave[0], .25);
  if (m === 'rim') return c;
  return withA(c, 215 / 255);
}
// face_fx (32 x 16 = two 8 x 8 faces at 2 x 2 px per skin pixel; scarlet_geometry FACE_FX places the cards), colours taken from
// the skin's own face: left half 'closed' = eyelids (the skin tone #F0C9CA) over the eyes' rows 4-5 and a lash line (#302A2A)
// on row 6; right half 'smile' = the eyes narrowed (row 4 skin, the lash on row 5 over the iris; row 6 the skin's own amber)
// and a thin closed-lip mouth (the upper half of row 7, columns 3-4, a soft rose); clear elsewhere
function faceFx(u, v) {
  const smile = u >= .5, c = Math.floor((smile ? u - .5 : u) * 16), r = Math.floor(v * 8);
  const eye = c === 1 || c === 2 || c === 5 || c === 6;
  if (!smile) { if (eye && r >= 4 && r <= 6) return r === 6 ? PAL.skinFx[1] : PAL.skinFx[0]; return T; }
  if (eye && r === 4) return PAL.skinFx[0];
  if (eye && r === 5) return PAL.skinFx[1];
  if (r === 7 && (c === 3 || c === 4) && v * 8 - 7 < .5) return PAL.skinFx[2];
  return T;
}
// the knot at the back of the hatband: five crimson petals with pink tips round a gold-thread centre (P2 brighter)
function knot(p2) { return (u, v) => { const r = Math.hypot(u - .5, v - .5) * 2, lo = lotusAt((u - .5) * 2.1, (v - .5) * 2.1, {petals: 5, ring: false, bg: null});
  if (!lo) return p2 && r < 1 ? mix(PAL.knot[1], C('#FFE0E8'), .3) : T;
  return p2 ? mix(mix(lo, PAL.knot[1], .55), C('#FFF0F4'), .35 * smooth(.6, 0, r)) : lo; }; }
// the bead strings (32 x 64): two strands straight down the box head's front sides, converging under the chin into the
// loop (v 0.64-0.75), then one strand to the bottom; violet and pale-gold beads (the skin's accents) with black spacers
function strings(u, v) {
  const bead = (t, s) => { const k = Math.floor(t * 18 + s); return k % 3 === 2 ? C('#141216') : k % 3 === 0 ? PAL.jasper : PAL.amber; };
  const at = (cx, t, s, w = .045) => { const d = Math.abs(u - cx), ph = fr(t * 18), r = Math.abs(ph - .5) * 2;
    return d < w * (1 - .45 * r * r) ? mix(bead(t, s), C('#FFFFFF'), .18 * (1 - r)) : null; };
  if (v <= .75) {
    // the two strands: straight down beside the face (v < 0.64), then converging to the loop under the chin (v 0.64-0.75)
    const t = v / .75, k = smooth(.86, 1, t);
    for (const s of [0, 1]) { const cx = s ? .955 - .455 * k : .045 + .455 * k, c = at(cx, t, s); if (c) return c; }
    return T;
  }
  const t = (v - .75) / .25;
  return t < .95 ? (at(.5, t * .6, 0, .32) || T) : T;
}
// the lotus guard seen along the blade (32 x 32): eight dark-iron petals with a pale-gold rim, the blade slot in the middle
function guardSpr(u, v) {
  const dx = (u - .5) * 2, dy = (v - .5) * 2, r = Math.hypot(dx, dy), a = Math.atan2(dy, dx), seg = Math.PI / 4;
  const k = ((a % seg) + seg) % seg - seg / 2, pr = .72 + .26 * Math.cos(k * 4);
  if (r > pr) return T;
  if (Math.abs(dx) < .09 && Math.abs(dy) < .55) return C('#0A090B');
  let c = mix(PAL.iron, C('#4A4452'), .35 * N.a(u * 6, v * 6));
  if (r > pr - .1) c = mix(PAL.brass[0], PAL.brass[2], .3);
  if (Math.abs(k) < .03) c = mix(c, PAL.brass[1], .5);
  return c;
}
// blade flats (16 x 128): u 0 = the edge (-Z) .. 1 = the spine; v 0 = the tip .. 1 = the guard. A 환도 point; the bright edge,
// the violet temper line (a soft wave), the steel body, the darker spine
function blade(u, v) {
  const w = v < .07 ? smooth(0, .07, v) : 1;
  const e0 = (1 - w) * .62;                                                    // the point: the edge curves up to the spine
  if (u < e0 || (v < .02 && u < .9)) return T;
  let c = mix(PAL.blade[0], PAL.blade[2], .25 * Math.abs(Math.sin(v * 40)));
  const hm = .2 + .05 * Math.sin(v * 70) + .03 * Math.sin(v * 23);
  if (u < e0 + .08) c = PAL.blade[2];
  else if (u < hm + e0 * .5) c = mix(PAL.blade[1], PAL.blade[2], .25);
  else if (u < hm + e0 * .5 + .05) c = mix(PAL.blade[1], PAL.blade[0], .5);
  if (u > .84) c = PAL.blade[3];
  if (Math.abs(u - .72) < .02 && v > .1) c = mix(c, PAL.blade[3], .4);         // the fuller line
  return c;
}
// the glow overlays (16 x 128, translucent): the edge side bright, fading to the spine
function glowSpr(col, core = '#FFFFFF') {
  return (u, v) => {
    const a = Math.pow(clamp(1 - u * 1.25), 1.5) * smooth(0, .06, v) * smooth(0, .03, 1 - v);
    return withA(mix(C(core), C(col), clamp(u * 2.2)), a * .92);
  };
}
// scabbard flats (16 x 128): u 0 = the edge side .. 1 = the spine; v 0 = the tip .. 1 = the mouth. Black lacquer, the violet
// lacquer line along the spine, a soft gloss stripe, pale-gold lotus-leaf fittings at the tip, the middle and the mouth
function scabSpr(u, v) {
  let c = mix(PAL.scab[0], PAL.scab[2], .5 * Math.pow(Math.max(0, 1 - Math.abs(u - .3) / .12), 2));
  if (Math.abs(u - .86) < .04) c = PAL.scab[1];
  const leaf = (v0, v1, up) => { if (v < v0 || v > v1) return false; const t = (v - v0) / (v1 - v0), x = Math.abs(u - .5) * 2; const tt = up ? t : 1 - t; return x < .25 + .75 * Math.sin(Math.PI * Math.min(1, tt * 1.2)); };
  if (leaf(0, .07, false) || leaf(.64, .69, true) || leaf(.955, 1, true)) { c = mix(PAL.brass[0], PAL.brass[2], .25 * Math.abs(Math.sin(u * 9))); if (Math.abs(u - .5) < .03) c = PAL.brass[1]; }
  return c;
}
// cup / bottle: white porcelain with violet (the cup's inside, its violet rim; the bottle's violet lotus scroll)
const cupIn = (u, v) => mix(C('#E8E4EE'), C('#C4B8E0'), .3 * smooth(.6, 0, Math.hypot(u - .5, v - .5)));
const cupRim = (u, v) => (v < .5 ? PAL.cobalt : mix(PAL.porcelain, PAL.cobalt, .3));
function bottleSpr(u, v) {
  let c = mix(PAL.porcelain, C('#E8E6F2'), .2 * N.d(u * 4, v * 4));
  if (v < .1 || (v > .82 && v < .86)) c = mix(c, PAL.cobalt, .7);
  const sc = Math.abs(Math.sin(u * Math.PI * 6 + Math.sin(v * 9) * 1.2) - (v - .45) * 4);
  if (v > .3 && v < .78 && sc < .25) c = mix(c, PAL.cobalt, .75);
  const lo = lotusAt((fr(u * 3) - .5) * 4, (v - .55) * 8, {petals: 6, ring: false, bg: null});
  if (lo) c = mix(lo, PAL.cobalt, .85);
  return c;
}
// the ghost texture (96 x 32, alpha 200; PLAN §2.2: core #9A4FB8 -> body #C97EDD -> rim #F0C8FA). Three regions, so every ghost
// twin uses this one texture and keeps its silhouette: u 0..1/3 the body gradient (every face), 1/3..2/3 the brim's wedge mask
// (the four brim squares of the hat), 2/3..1 the bead strings' mask (scarlet_geometry.allModels remaps the UVs)
function ghostGrad(u, v) { const d = Math.max(Math.abs(u - .5), Math.abs(v - .5)) * 2;
  return d < .35 ? mix(PAL.ghost[1], PAL.ghost[0], d / .35) : mix(PAL.ghost[0], PAL.ghost[2], smooth(.55, 1, d)); }
function ghost(u, v) {
  const a = 200 / 255;
  if (u < 1 / 3) return withA(ghostGrad(u * 3, v), a);
  if (u < 2 / 3) {
    const uu = (u - 1 / 3) * 3, c = brimMask(uu, v, 32);
    if (!c) return T;
    const r = Math.hypot(uu - .5, v - .5) * 2;
    return withA(mix(PAL.ghost[0], PAL.ghost[2], smooth(.8, .98, r) + .25 * (c === 'rib' ? 1 : 0)), a);
  }
  const c = strings((u - 2 / 3) * 3, v);
  return c === T || c[3] === 0 ? T : withA(mix(PAL.ghost[0], PAL.ghost[2], .4), a);
}
// ---- sprite table: name -> [w, h, painter, translucent] (the skin is not painted here: build_scarlet_rig.mjs writes its bytes) --
export function scarletSprites() {
  const S = {};
  for (const [n, [w, h]] of Object.entries(TILE_SIZES)) S[n] = [w, h, TILE_PAINT[n], false];
  for (const [n, [w, h]] of Object.entries(WRAP_SPRITES)) S[n] = [w, h, WRAP_PAINT[n], false];
  Object.assign(S, {
    face_fx: [32, 16, faceFx, false],
    sash_tail: [16, 64, sashTail(false), false], sash_tail_p2: [16, 64, sashTail(true), false],
    brim: [BRIM_PX, BRIM_PX, brim, true], knot_p1: [16, 16, knot(false), false], knot_p2: [16, 16, knot(true), false], strings: [32, 64, strings, false],
    guard: [32, 32, guardSpr, false], blade: [16, 128, blade, false], scab: [16, 128, scabSpr, false],
    glow_lilac: [16, 128, glowSpr('#C97EDD', '#FFE6FA'), true], glow_pink: [16, 128, glowSpr('#FF5AB4', '#FFE0F0'), true],
    glow_violet: [16, 128, glowSpr('#8A4CFF', '#E8DCFF'), true], glow_gold: [16, 128, glowSpr('#FFC83A', '#FFF6D0'), true],
    cup_in: [16, 16, cupIn, false], cup_rim: [16, 16, cupRim, false], bottle: [32, 32, bottleSpr, false], ghost: [96, 32, ghost, true],
  });
  return S;
}
export function paintScarlet(rp, sprites = scarletSprites()) {
  return paintSpriteSet(rp, TEX_DIR, sprites, spriteId);
}
