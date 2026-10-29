// Sprites of the 타키 (Tachy) rig: the tiles of tachy_materials.mjs plus the unique cards of tachy_geometry.mjs (face,
// hair locks, chest / abdomen / pelvis fronts with the yellow tie and the 3x3 light grid, the visor, ring lights, cape
// panels, blade-feather wing segments in the winged and abyss looks, the tendril, the blade flats, the edge glows, the
// skull and grid glows). Painted procedurally (no external art); every sprite is u, v in 0..1, v down the sprite.
// Coordinates follow the card that shows the sprite (tachy_geometry.mjs): cardZ / front-facing cards read as painted from
// the front (u = her right -> her left, i.e. screen left -> right), the blade flats u = edge -> spine, v = tip -> guard.
import {paintSpriteSet} from './mboss_paint_lib.mjs';
import {PAL, N, TILES, C, clamp, smooth, mix, lift, sink, glow, carbon, hexCells, yellowPaint, hairStrands, fleshTex, steelTex, TRANSPARENT} from './tachy_materials.mjs';

export const TEX_DIR = 'assets/rlk/textures/mboss/tachy';
export const spriteId = n => `rlk:mboss/tachy/${n}`;
const T = TRANSPARENT;
const fr = x => x - Math.floor(x);
const h1 = (i, s = 1) => { let n = (i * 374761393 + s * 668265263) | 0; n = (n ^ (n >>> 13)) * 1274126177 | 0; return ((n ^ (n >>> 16)) >>> 0) / 4294967295; };
const segD = (px, py, ax, ay, bx, by) => { const dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy || 1e-9, t = clamp(((px - ax) * dx + (py - ay) * dy) / l2); return [Math.hypot(px - ax - t * dx, py - ay - t * dy), t]; };

// ---- fronts: the yellow tie (v2 13.0, v9 1.5) ------------------------------------------------------------------------------
// chest: two yellow straps from the collar corners converging toward the bottom centre, the 3x3 grid of light sockets on
// the upper sternum, carbon suit; a darker band at the bust underline
function chestFront(u, v) {
  // card X -0.1..0.1, Y -0.01..0.33 (blocks): the straps run from the collar (x ±0.085, y 0.33) to the sternum (±0.012,
  // y 0.12) and down; the 3x3 light sockets centred at y 0.265 between them
  const x = -.1 + .2 * u, y = .33 - .34 * v;
  let c = carbon(u * .9, v * 1.5, 8);
  for (const s of [-1, 1]) {
    const [d1] = segD(x, y, s * .085, .34, s * .014, .12), [d2] = segD(x, y, s * .014, .12, s * .012, -.02);
    const d = Math.min(d1, d2);
    if (d < .014) c = d > .01 ? PAL.yellow(.75) : yellowPaint(u * 2, v);
  }
  const gx = x, gy = y - .265;
  if (Math.abs(gx) < .034 && Math.abs(gy) < .034) {
    c = PAL.metal(.78);
    const cx = Math.round(gx / .022) * .022, cy = Math.round(gy / .022) * .022;
    if (Math.hypot(gx - cx, gy - cy) < .0075) c = C('#4A2E0C');
  }
  return c;
}
function abdomenFront(u, v) {
  let c = carbon(u * 1.1, v * 1.1, 8);
  const x = Math.abs(u - .5), w = .07 - .02 * v;
  if (x < w) c = x > w - .018 ? PAL.yellow(.7) : yellowPaint(u * 2, v);
  return c;
}
function pelvisFront(u, v) {
  let c = carbon(u * 1.2, v * 1.0, 8);
  const x = u - .5;
  const [d0] = segD(x, v, 0, -.02, 0, .55);
  let d = d0;
  for (const s of [-1, 1]) d = Math.min(d, segD(x, v, 0, .55, s * .18, 1.02)[0]);
  if (d < .05) c = d > .035 ? PAL.yellow(.7) : yellowPaint(u * 2, v);
  if (v < .2) c = mix(c, PAL.metal(.8), .3);
  return c;
}
// face: pale, dark brows, almond eyes (lowered lids), a straight nose, red lips (v2 10.5)
function face(u, v) {
  const x = u - .5, ax = Math.abs(x);
  // outline: oval, narrower at the chin (v = 1 is the jaw)
  const half = .5 * Math.sqrt(Math.max(0, 1 - Math.pow((v - .42) / .62, 2))) * (1 - .35 * smooth(.55, 1, v));
  if (ax > half) return T;
  let c = PAL.skin(clamp(.25 + .25 * smooth(.25, .5, ax) + .1 * (N.a(u * 6, v * 6) - .5) + .12 * smooth(.7, 1, v)));
  if (Math.abs(v - .34) < .022 && ax > .08 && ax < .36) c = mix(c, PAL.hair(.85), .8 * smooth(.36, .3, ax));   // brows
  const ey = .45, ex = .2;
  const e = Math.pow((ax - ex) / .12, 2) + Math.pow((v - ey) / .035, 2);
  if (e < 1) c = e < .45 && Math.abs(ax - ex) < .05 ? C('#2A1C1A') : C('#F2ECEA');
  if (Math.abs(v - (ey - .035)) < .014 && Math.abs(ax - ex) < .13) c = C('#3A2622');                                 // upper lid line
  if (ax < .035 && v > .48 && v < .66) c = mix(c, PAL.skin(.7), .35 * (1 - ax / .035));                             // nose shade
  const ly = .78, lw = .16 - .4 * Math.pow(v - ly, 2) * 10;
  if (Math.abs(v - ly) < .045 && ax < lw) c = mix(C('#9C2A2E'), C('#C2464A'), smooth(ly + .04, ly - .04, v));       // lips
  if (Math.abs(v - ly) < .007 && ax < lw) c = C('#5A1418');
  return c;
}
// ---- hair cards ---------------------------------------------------------------------------------------------------------------
function hairLock(u, v) {
  // a wavy lock: wide at the top, splitting into points at the bottom
  const w = .45 - .12 * v + .05 * Math.sin(v * 9), cx = .5 + .08 * Math.sin(v * 5 + 1);
  if (Math.abs(u - cx) > w) return T;
  if (v > .75) { const k = fr((u - cx) * 7 + .5), tip = (v - .75) / .25; if (Math.abs(k - .5) < tip * .5) return T; }
  return hairStrands(u * .5, v, {k: .8});
}
function hairFringe(u, v) {
  // parted fringe: two curtains sweeping from the parting (u 0.5) outward, alpha-cut bottom edge in points
  const x = Math.abs(u - .5), bottom = .55 + .45 * smooth(0, .5, x) - .12 * Math.abs(Math.sin(x * 22));
  if (v > bottom) return T;
  if (x < .03 && v < .5) return sink(PAL.skin(.3), .2);
  return hairStrands(u * .7 + x, v * .6, {k: 1});
}
function hairBack(u, v) {
  const edge = .04 + .05 * Math.abs(Math.sin(v * 7 + u * 3));
  if (u < edge || u > 1 - edge) return T;
  return hairStrands(u, v * .8, {k: .7});
}
function hairTip(u, v) {
  const k = fr(u * 6 + .2 * Math.sin(v * 6)), w = .5 * (1 - v);
  if (Math.abs(k - .5) > w) return T;
  return hairStrands(u, .8 + v * .2, {k: .4});
}
// ---- ring light (orange, v2 10.5 / 14.4) ----------------------------------------------------------------------------------------
function ring(u, v) {
  const r = Math.hypot(u - .5, v - .5) * 2;
  if (r > 1) return T;
  if (r > .86) return PAL.metal(.8);
  if (r > .58) return PAL.ring(clamp(.15 + 1.4 * Math.abs(r - .72)));
  if (r > .5) return PAL.metal(.9);
  return mix(PAL.metal(.7), PAL.ring(.35), .25 * (1 - r));
}
// ---- cape (folded wings, P1): black lining with overlapping bronze-gold feather plates (v2 8.0-9.5, v8 6.2) ---------------------
// seg 1..3 top to bottom of the left panel (u 0 = the spine side, 1 = the outer edge). Rows of rounded plates pointing
// down, offset per row; the bottom segment ends in long ragged feather tips.
function cape(seg) {
  return (u, v) => {
    const Y = (seg - 1) + v;                                  // 0..3 down the cape
    if (seg === 3) {
      const k = fr(u * 5 + .3), tipLen = .45 + .3 * h1(Math.floor(u * 5 + .3), 3);
      if (v > (1 - tipLen) + tipLen * (1 - Math.abs(k - .5) * 2)) return T;
    }
    const rows = 5, r = Y * rows, ri = Math.floor(r), fy = r - ri, off = (ri % 2) * .5;
    const cu = u * 4 + off, ci = Math.floor(cu), fx = cu - ci;
    const id = h1(ci * 31 + ri, 5);
    const w = .5 - Math.abs(fx - .5), tip = smooth(.45, 1, fy);
    const inPlate = w > .04 + .44 * tip * tip;
    let c;
    if (inPlate) {
      const t = .2 + .45 * fy + .2 * (id - .5) + .15 * (N.b(u * 9, Y * 7) - .5) - .25 * (1 - w * 2) * 0;
      c = PAL.bronze(clamp(t + .2 * (u - .5)));
      if (Math.abs(fx - .5) < .03) c = sink(c, .35);                          // rachis
      if (w < .1 + .44 * tip * tip) c = lift(c, .25);                         // bright rim
      c = mix(c, PAL.suit(.8), .35 * smooth(.6, 1, Y / 3) * (1 - id));        // darker toward the hem
    } else c = PAL.suit(.75 + .1 * N.c(u * 8, Y * 8));
    if (u > .95) c = sink(c, .3);
    return c;
  };
}
// ---- blade-feather wings (P2 winged, P3 abyss; v9 2.7-4.5, v7 0.4) --------------------------------------------------------------
// u 0 = the far edge (feather tips), u 1 = the arm bone; v 0 = the segment root, 1 = its end. Long black metallic blade
// feathers leave the arm and sweep toward the far edge and the segment end, gold glints on their leading edges; the
// abyss look adds dark red fleshy tendrils among them.
function wing(seg, back, abyss) {
  const n = 7, F = [];
  for (let i = 0; i < n; i++) {
    const r0 = (i + .3 + (back ? .5 : 0)) / n, ang = .55 + .25 * h1(i * 7 + seg, back ? 9 : 3);
    const len = (.9 + .25 * h1(i * 5 + seg, 11)) * (seg === 3 ? .95 - .35 * r0 : 1);
    F.push({x0: 1, y0: r0 * .85, dx: -len, dy: len * ang * .55, w: .055 + .02 * h1(i, seg)});
  }
  const flesh = abyss ? [0, 1, 2].map(i => ({x0: .95, y0: (i + .6) / 3.3, dx: -.7 - .2 * h1(i, seg + 20), dy: .35, w: .035})) : [];
  return (u, v) => {
    let best = null;
    for (let i = F.length - 1; i >= 0; i--) {
      const f = F[i], [d, t] = segD(u, v, f.x0, f.y0, f.x0 + f.dx, f.y0 + f.dy);
      const half = f.w * (t < .15 ? .6 + t * 2.6 : 1 - Math.pow((t - .15) / .85, 1.6) * .95);
      if (d < half) { best = {f, d, t, half, i}; break; }
    }
    if (abyss) for (const f of flesh) {
      const wav = .03 * Math.sin(v * 25 + f.y0 * 9);
      const [d, t] = segD(u, v + wav, f.x0, f.y0, f.x0 + f.dx, f.y0 + f.dy);
      if (d < f.w * (1 - t * .7)) return fleshTex(u * 2, v * 3);
    }
    if (u > .93) return PAL.metal(.75);
    if (!best) return T;
    const {f, d, t, half} = best, side = (u - f.x0) * f.dy - (v - f.y0) * f.dx;
    let c = PAL.wingm(clamp(.55 + .25 * (d / half) - .25 * smooth(.3, 0, d / half) + .08 * N.d(u * 9, v * 9)));
    if (side > 0 && d > half * .7) c = mix(c, PAL.gold(.3), .55 * smooth(.2, .9, t));   // gold glint on the leading edge
    if (d < half * .12) c = lift(c, .18);
    if (d > half * .9) c = sink(c, .5);
    return c;
  };
}
function tendrilSpr(u, v) {
  const w = .42 * (1 - .8 * v) + .05, cx = .5 + .12 * Math.sin(v * 7);
  if (Math.abs(u - cx) > w) return T;
  if (v > .85) return PAL.suit(.9);
  return fleshTex(u, v * 4);
}
// ---- blade (v2 14.0: steel flats, a serrated mechanical spine, the yellow glowing edge band) ------------------------------------
function bladeFlat(u, v) {
  // u 0 = edge, 1 = spine; v 0 = tip, 1 = guard. The width narrows to the tip; the spine has teeth.
  const Y = 1 - v, wE = .06 + .35 * smooth(0, .25, v), wS = .45 + .45 * smooth(0, .15, v);
  const x = u;
  const tooth = Math.abs(fr(v * 22) - .5) * 2;                                // spine teeth
  if (x < .44 - wE * .9) return T;
  if (x > .44 + wS * .55 * (.85 + .15 * tooth)) return T;
  let c = steelTex(u, v);
  if (x < .44 - wE * .9 + .07) c = mix(PAL.yellow(.15), C('#FFF2A0'), .4);     // the edge band
  else if (x > .44 + wS * .4) c = PAL.metal(.85 - .2 * tooth);                  // spine
  if (Math.abs(x - .58) < .02 && v > .05) c = sink(c, .3);                      // fuller line
  void Y;
  return c;
}
// ---- glows (translucent; tinted per look) ---------------------------------------------------------------------------------------
function edgeGlow(u, v) {
  const d = Math.abs(u - .5) * 2, a = Math.pow(clamp(1 - d), 1.6) * (.6 + .4 * smooth(0, .1, v)) * smooth(0, .03, 1 - v);
  return glow(mix(C('#FFFFFF'), C('#E8E8E8'), d), a);
}
// pyro: flames licking off the edge (4 frames); electro: crackling white-gold arcs (4 frames)
function edgeFire(u, V) {
  const f = Math.floor(V * 4), v = V * 4 - f;
  const d = Math.abs(u - .5) * 2, n = N.e(u * 3 + f * 1.7, v * 18 - f * 2.3);
  const a = clamp((1 - d) * 1.3 - .25 + .55 * (n - .5)) * smooth(0, .05, 1 - v);
  const col = mix(C('#FF4A10'), C('#FFE08A'), clamp(1.2 - d * 1.4 + .3 * n));
  return glow(col, a);
}
function edgeVolt(u, V) {
  const f = Math.floor(V * 4), v = V * 4 - f;
  const d = Math.abs(u - .5) * 2;
  let a = Math.pow(clamp(1 - d), 2.2) * .8;
  const arc = Math.abs(u - .5 - .28 * (N.f(v * 14 + f * 3.1, f * 5.3) - .5));
  if (arc < .045) a = Math.max(a, .95);
  return glow(mix(C('#FFE35A'), C('#FFFFFF'), clamp(1 - d * 1.2)), a * smooth(0, .05, 1 - v));
}
function skullGlow(u, v) {
  // the glowing skull inside the visor (v2 12.5): cranium, eye sockets, nasal cavity, teeth, burning wisps
  const x = u - .5, ax = Math.abs(x);
  const cran = Math.hypot(x / .4, (v - .4) / .38) < 1, jaw = v > .62 && v < .9 && ax < .26 - .2 * (v - .62);
  if (!cran && !jaw) { const w = N.a(u * 6, v * 9); return glow('#FFFFFF', clamp(.35 * (w - .45)) * smooth(.9, .2, v)); }
  let a = .92 - .25 * N.b(u * 8, v * 8);
  const eye = Math.hypot((ax - .16) / .1, (v - .48) / .085);
  if (eye < 1) a = .12 + .5 * (1 - eye) * 0;
  if (ax < .04 && v > .58 && v < .68) a = .15;
  if (v > .72 && v < .82 && fr(u * 10) < .18 && ax < .2) a = .25;
  return glow(mix(C('#FFFFFF'), C('#D8D8D8'), clamp(Math.hypot(x, v - .4) * 1.5)), a);
}
function gridGlow(u, v) {
  // 3x3 dots + a soft core glow under them
  const x = u - .5, y = v - .45;
  let a = .25 * Math.exp(-(x * x + y * y) / .03);
  const cx = Math.round(x / .2) * .2, cy = Math.round(y / .2) * .2;
  if (Math.abs(cx) < .21 && Math.abs(cy) < .21) { const d = Math.hypot(x - cx, y - cy); a = Math.max(a, clamp(1 - d / .07)); }
  return glow('#FFFFFF', a);
}

// ---- sprite table: name -> [w, h, painter, translucent, mcmeta] --------------------------------------------------------------
export function tachySprites() {
  const S = {};
  for (const [n, [w, h, , fn]] of Object.entries(TILES)) S[n] = [w, h, fn, false];
  Object.assign(S, {
    chest_front: [32, 64, chestFront, false], abdomen_front: [48, 48, abdomenFront, false], pelvis_front: [64, 48, pelvisFront, false],
    face: [48, 48, face, false], hair_lock: [32, 64, hairLock, false], hair_fringe: [48, 32, hairFringe, false],
    hair_back: [48, 48, hairBack, false], hair_tip: [48, 32, hairTip, false], ring: [32, 32, ring, false],
    tendril: [32, 192, tendrilSpr, false], sword_blade: [32, 320, bladeFlat, false],
    edge: [16, 256, edgeGlow, true], edge_fire: [32, 1024, edgeFire, true, {animation: {frametime: 2, width: 32, height: 256}}],
    edge_volt: [32, 1024, edgeVolt, true, {animation: {frametime: 2, width: 32, height: 256}}],
    skull: [32, 32, skullGlow, true], grid: [32, 32, gridGlow, true],
  });
  for (let i = 1; i <= 3; i++) {
    S['cape_' + i] = [96, 112, cape(i), false];
    S['wing_' + i] = [128, 96, wing(i, false, false), false]; S['wing_' + i + 'b'] = [128, 96, wing(i, true, false), false];
    S['wing_a' + i] = [128, 96, wing(i, false, true), false]; S['wing_a' + i + 'b'] = [128, 96, wing(i, true, true), false];
  }
  return S;
}
export function paintTachy(rp, sprites = tachySprites()) {
  const set = Object.fromEntries(Object.entries(sprites).map(([n, [w, h, fn, tr, meta]]) => [n, [w, h, fn, tr, meta]]));
  return paintSpriteSet(rp, TEX_DIR, set, spriteId);
}
