// Sprites of the 타키 (Tachy) rig: the tiles of tachy_materials.mjs plus the unique cards of tachy_geometry.mjs (face,
// hair locks, chest / abdomen / pelvis fronts with the yellow tie and the 3x3 light grid, the visor, ring lights, cape
// panels, blade-feather wing segments in the winged and abyss looks, the tendril, the blade flats, the edge glows, the
// skull and grid glows). Painted procedurally (no external art); every sprite is u, v in 0..1, v down the sprite.
// Coordinates follow the card that shows the sprite (tachy_geometry.mjs): cardZ / front-facing cards read as painted from
// the front (u = her right -> her left, i.e. screen left -> right), the blade flats u = edge -> spine, v = tip -> guard.
import {paintSpriteSet} from './mboss_paint_lib.mjs';
import {PAL, N, TILES, C, clamp, smooth, mix, lift, sink, glow, carbon, hexCells, yellowPaint, hairStrands, fleshTex, steelTex, TRANSPARENT} from './tachy_materials.mjs';
import {CAPE} from './tachy_geometry.mjs';

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
// face (visor up: the intro before E7, any up_off look; v2 10.5): I1 rework in an anime / subculture-game style (the user's
// request: a clearly pretty face; realism is impossible at this scale). 64 x 64 over the 0.176 x 0.2 b card (u 0 screen
// left, v 0 the hairline under the fringe, 1 the chin). Clean pale skin with soft cel shading, a soft V jaw, large almond
// eyes (dark lash line with a flick at the outer corner, a warm brown iris darker at the top, a dark pupil, two catch
// lights, a soft lower lash, a lid crease), thin arched brows, a one-pixel nose hint, a small rose mouth, a light blush.
// Symmetric except the catch lights (one light from the upper left). Everything outside the face outline is clear: the
// hair locks and the head loft behind frame it.
const FC = {skin: C('#FFEFE6'), skin2: C('#F6D5C6'), skin3: C('#E8B4A2'), blush: C('#F78F92'), lash: C('#1C1110'),
  lash2: C('#5A3A34'), crease: C('#D9A598'), white: C('#FFFBFA'), whiteSh: C('#E3D6DC'), irisTop: C('#24120F'),
  irisMid: C('#6E2C22'), irisLow: C('#C46E3E'), pupil: C('#110706'), shine: C('#FFFFFF'), brow: C('#4B3430'),
  lipLine: C('#A8323C'), lip: C('#D9606B'), lipHi: C('#F2A0A4'), nose: C('#E0AFA2'), corner: C('#E9A6A2')};
const FACE_W = .176, FACE_H = .2;                  // the card (blocks)
const EYE = {x: .4, v: .5, hw: .25, hh: .075};      // centre (|X|, v), half width (X units), half height (v units)
function faceHalf(v) {
  // half width of the face (X units, 1 = the card edge) at v: straight cheeks, a soft V to a rounded chin at 0.985
  if (v > .985) return 0;
  const t = clamp((v - .5) / .485);
  let hw = .98 - .78 * Math.pow(t, 1.6);
  if (v > .93) hw *= Math.sqrt(Math.max(0, 1 - Math.pow((v - .93) / .055, 2))) * .5 + .5;
  return hw;
}
function eyeShape(ex) {
  // the lids in eye units (ey -1 top .. +1 bottom) at ex (-1 inner .. +1 outer): almond, the outer corner lifted
  return [-.92 + .62 * ex * ex - .2 * ex, .78 - .5 * ex * ex - .22 * ex];
}
function eyePx(X, v) {
  // -> colour or null (not on the eye); X > 0 = either eye mirrored (ex toward the outer corner)
  const ax = Math.abs(X), ex = (ax - EYE.x) / EYE.hw, ey = (v - EYE.v) / EYE.hh;
  if (ex < -1.25 || ex > 1.55 || ey < -1.9 || ey > 1.4) return null;
  const [up, lo] = eyeShape(Math.max(-1, Math.min(1, ex)));
  // the lash line along the upper lid (thicker toward the outer corner) and its flick past the corner
  const th = .3 + .22 * smooth(-.3, 1, ex);
  if (ex >= -1 && ex <= 1 && ey > up - th && ey < up + .12) return FC.lash;
  if (ex > .95 && ex < 1.5) {
    const fy = eyeShape(1)[0] + (1 - ex) * .55 - .15, w = .28 * (1 - smooth(1, 1.5, ex));
    if (Math.abs(ey - fy) < w) return FC.lash;
  }
  // the lid crease
  if (ex > -.55 && ex < .85 && Math.abs(ey - (up - .75 + .1 * ex)) < .1) return 'crease';
  if (ex < -1 || ex > 1 || ey < up || ey > lo) {
    // the soft lower lash at the outer half, just under the opening
    if (ex > .05 && ex < 1.02 && ey > lo && ey < lo + .2) return 'lower';
    return null;
  }
  // inside the opening: the iris (clipped by the lids), else the white
  const ix = (ax - (EYE.x + .015)) / .16, iy = (v - (EYE.v + .012)) / .062, ir = Math.hypot(ix, iy);
  if (ir < 1) {
    if (ir > .86) return FC.irisTop;                                            // the dark limbal ring
    let c = iy < 0 ? mix(FC.irisTop, FC.irisMid, smooth(-.9, 0, iy)) : mix(FC.irisMid, FC.irisLow, smooth(0, .8, iy));
    if (Math.hypot(ix, iy * 1.1) < .42) c = mix(FC.pupil, c, .15);                // the pupil
    const sx = X < 0 ? 1 : -1;                                                  // catch lights from the upper left (screen)
    if (Math.hypot((ix - .38 * sx * (X < 0 ? 1 : -1)) * 1.1, iy + .42) < .3) return FC.shine;
    if (Math.hypot(ix + .32 * sx * (X < 0 ? 1 : -1), iy - .48) < .14) return mix(FC.shine, c, .25);
    return mix(c, FC.lash, .35 * smooth(-.2, -.95, iy));                        // the lid's shadow on the iris
  }
  if (ex < -.84) return FC.corner;                                              // the inner corner
  return mix(FC.white, FC.whiteSh, smooth(up + .65, up + .1, ey));               // the lid's shadow on the white
}
function face(u, v) {
  const X = (u - .5) * 2, ax = Math.abs(X), hw = faceHalf(v);
  if (ax > hw) return T;
  // soft cel shading: the outline rim, the fringe's shadow at the top, the jaw
  let c = FC.skin;
  const rim = smooth(hw - .2, hw, ax);
  // (the fringe's shadow only at the temples: the curtain bangs leave the middle of the forehead open)
  c = mix(c, FC.skin2, Math.max(.75 * rim, .9 * smooth(.16, 0, v) * smooth(.15, .6, ax), .5 * smooth(.86, .99, v) * smooth(.15, .5, ax)));
  c = mix(c, FC.skin3, .45 * smooth(hw - .07, hw, ax) * smooth(.45, .8, v));
  // blush under the eyes
  const bl = Math.pow((ax - .5) / .24, 2) + Math.pow((v - .675) / .055, 2);
  if (bl < 1) c = mix(c, FC.blush, .36 * (1 - bl));
  // brows: thin arcs, the arch at two thirds, tapering outward
  const bx = (ax - .18) / .55;
  if (bx > 0 && bx < 1) {
    const by = .35 - .042 * Math.sin(Math.PI * Math.pow(bx, .75)) + .012 * bx, bw = .0125 * (1 - .5 * bx) * smooth(0, .12, bx);
    if (Math.abs(v - by) < bw) c = mix(c, FC.brow, .9 - .35 * bx);
  }
  const e = eyePx(X, v);
  if (e === 'crease') c = mix(c, FC.crease, .45);
  else if (e === 'lower') c = mix(c, FC.lash2, .55);
  else if (e) c = e;
  // the nose: one soft shade under the tip
  if (ax < .05 && Math.abs(v - .695) < .012) c = mix(c, FC.nose, .7 * (1 - ax / .05));
  // the mouth: a small rose mouth, the lip line slightly curved, a fuller lower lip with a highlight
  const mw = .15, mx = ax / mw;
  if (mx < 1) {
    const ly = .815 - .012 * (1 - mx * mx);
    if (Math.abs(v - ly) < .009 * (1 - .5 * mx)) c = mix(c, FC.lipLine, .95 - .4 * mx);
    else if (v > ly && v < ly + .032 * (1 - mx * mx)) c = mix(c, mix(FC.lip, FC.lipHi, smooth(.35, 0, mx) * smooth(ly + .028, ly + .012, v)), .85);
    else if (v < ly && v > ly - .016 * (1 - mx * mx) && mx < .85) c = mix(c, FC.lip, .55);
  }
  return c;
}
// ---- hair cards ---------------------------------------------------------------------------------------------------------------
// I1 (with the face): anime-style hair shading. A clump is lighter in its middle and darker toward its edges, fine strand
// lines run along it, and a soft highlight band (the "angel ring") crosses near its top; dark ash brown (v2 10.5).
const HC = {deep: C('#1E1514'), base: C('#3B2C29'), mid: C('#5C4540'), hi: C('#A88A80'), part: C('#E9C9BE')};
function animeHair(u, v, edge, {hv = .28, hk = 1} = {}) {
  // edge: 0 at a clump edge .. 1 in its middle; hv: the highlight band's v
  let c = mix(HC.deep, HC.base, smooth(0, .55, edge));
  c = mix(c, HC.mid, .55 * smooth(.35, 1, edge) * (1 - smooth(.55, 1, v)));
  const str = N.a(u * 40, v * 1.5);
  c = mix(c, HC.deep, .3 * smooth(.55, .8, str));
  const band = Math.exp(-Math.pow((v - hv - .025 * Math.sin(u * 19)) / .055, 2)) * smooth(.15, .7, edge) * hk;
  return mix(c, HC.hi, .75 * band * (.6 + .4 * smooth(.3, .7, N.b(u * 30, v * 4))));
}
function hairLock(u, v) {
  // a lock framing the face: wavy, wide at the top, ending in two or three points
  const w = .44 - .1 * v + .04 * Math.sin(v * 9), cx = .5 + .07 * Math.sin(v * 5 + 1);
  const d = Math.abs(u - cx) / w;
  if (d > 1) return T;
  let edge = 1 - d;
  if (v > .7) {
    const k = fr((u - cx) * 3.4 + .5), tip = (v - .7) / .3, g = Math.abs(k - .5) * 2;
    if (g < tip * 1.05) return T;
    edge = Math.min(edge, (g - tip) * 2);
  }
  return animeHair(u, v, clamp(edge), {hv: .16});
}
// the scalp's half width (blocks) at height y over the head pivot (tachy_geometry.mjs hairTop stations)
const SCALP = [[.19, .106], [.235, .094], [.265, .07], [.283, .04], [.292, .012]];
const scalpHalf = y => { if (y <= SCALP[0][0]) return .106; for (let i = 1; i < SCALP.length; i++) if (y <= SCALP[i][0]) { const [a, ra] = SCALP[i - 1], [b, rb] = SCALP[i]; return ra + (rb - ra) * (y - a) / (b - a); } return 0; };
export const FRINGE = {X0: -.1, X1: .1, Y0: .12, Y1: .292};
function hairFringe(u, v) {
  // the front of the crown and curtain bangs (v2 10.5): a middle parting from the crown; from it the hair sweeps down and
  // out to both sides in pointed clumps, so the forehead shows as an inverted V and the outer clumps cover the temples and
  // the ends of the brows; the top follows the round crown
  const xb = Math.abs(u - .5) * (FRINGE.X1 - FRINGE.X0), yb = FRINGE.Y1 - v * (FRINGE.Y1 - FRINGE.Y0);
  if (xb > scalpHalf(yb) + .004) return T;
  const x = xb / .1, w = (.245 - yb) / .125;                                // the bangs' own coordinates (w 0 at y .245)
  const parting = Math.max(0, .03 - .02 * smooth(-.3, .2, w));
  if (w < 0) {
    if (xb < .004 + .006 * smooth(-.4, 0, w)) return mix(HC.part, HC.deep, .55);       // the parting line on the crown
    return animeHair(u * 1.3, w * .9 + .1, clamp(1 - x * .6), {hv: .02});
  }
  const ph = x / (.35 + .65 * w) * 2.2 + .35, k = fr(ph), g = Math.abs(k - .5) * 2;
  const tipV = .34 + .66 * smooth(.0, .55, x);                              // the curtain opens toward the parting
  const bottom = tipV - .22 * Math.pow(g, 1.3) * smooth(.1, .5, x);
  if (w > bottom) return T;
  if (x < parting * 10 && w < .2) return mix(HC.part, HC.deep, .4);
  const edge = Math.min(1 - g, (bottom - w) * 5, x * 8);
  return animeHair(u + Math.floor(ph) * .37, w * .9 + .1, clamp(edge), {hv: .02});
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
// ---- cape (folded wings, P1): a draped, layered dark-bronze feather cape (v2 7.5-9.5, v8 6.2; ref/model_a.jpg v2 8.0 / 9.0) ---
// I1 rework (the old plates on a black lining read as a see-through gold grid). One feather field over the whole cape in
// block coordinates of the unfolded panel (x across: the panel axis 0, toward her spine < 0, outer edge > 0, the same for
// the three segments; y down from the top of segment 1), so the rows run on across the segment joints. Long narrow
// feathers in staggered rows, ~2.8 rows deep: every point is covered (no lining shows), the upper rows lie over the lower
// ones and each feather over its inner neighbour; a soft shadow under every overlapping edge, a gold-bronze rim on the
// exposed tips, fine barbs, a lighter rachis; darker toward the hem, under the collar and on the wrapped sides. Only the
// hem (segment 3) ends in ragged feather tips. The inner face (toward her body) shows the dark lining cape_in.
const CAPE_TOP = [0, CAPE[0].L, CAPE[0].L + CAPE[1].L];
const CAPE_Y = CAPE[0].L + CAPE[1].L + CAPE[2].L;             // 1.56 b
const FR = {ry: .1, cx: .05, len: .27, hw: .033};
function capeFeather(r, c) {
  const k = r * 131 + c * 17 + 1000;
  const xc = c * FR.cx + (((r % 2) + 2) % 2) * FR.cx * .5 + (h1(k, 21) - .5) * .014;
  const y0 = r * FR.ry + (h1(k, 22) - .5) * .014;
  const len = FR.len * (.88 + .26 * h1(k, 23)), hw = FR.hw * (.86 + .28 * h1(k, 24));
  const lean = (5 * smooth(.04, .36, xc) + 4 * (h1(k, 25) - .5)) * Math.PI / 180;      // tips splay outward a little
  return {r, c, xc, y0, len, hw, sn: Math.sin(lean), cs: Math.cos(lean), tone: h1(k, 26), gild: h1(k, 27) < .13};
}
const featherWidth = t => t < 0 || t > 1 ? 0 : t < .1 ? .55 + 4.5 * t : t < .6 ? 1 : Math.pow(1 - Math.pow((t - .6) / .4, 1.8), .6);
// local coordinates of (x, y) on feather f: tt along it (0 base .. 1 tip), sx across (-1 .. 1), or null outside
function onFeather(f, x, y) {
  const dx = x - f.xc, dy = y - f.y0;
  const a = dy * f.cs + dx * f.sn, b = dx * f.cs - dy * f.sn;
  const tt = a / f.len, wd = f.hw * featherWidth(tt);
  if (wd <= 0 || Math.abs(b) > wd) return null;
  return {tt, sx: b / wd, a, b};
}
const FCACHE = new Map();
const feather = (r, c) => { const key = r * 1000 + c; let f = FCACHE.get(key); if (!f) FCACHE.set(key, f = capeFeather(r, c)); return f; };
// the topmost feather at (x, y): the highest row first, in a row the outer feather (larger c) over the inner one
function capeTop(x, y, rowMax = Infinity) {
  const r0 = Math.floor((y - FR.len * 1.2) / FR.ry), r1 = Math.min(Math.floor(y / FR.ry) + 1, rowMax);
  for (let r = r0; r <= r1; r++) {
    const off = (((r % 2) + 2) % 2) * FR.cx * .5, c0 = Math.round((x - off) / FR.cx);
    for (let c = c0 + 2; c >= c0 - 2; c--) {
      const f = feather(r, c);
      if (f.y0 + f.len > CAPE_Y - .004) continue;                // no feather hangs past the hem
      const L = onFeather(f, x, y);
      if (L) return {f, L};
    }
  }
  return null;
}
function capeColour(x, y, sp, x1) {
  const hit = capeTop(x, y);
  if (!hit) return null;
  const {f, L: {tt, sx, a, b}} = hit;
  let t = .74 + .16 * (f.tone - .5) - (f.gild ? .14 : 0);
  t -= .12 * smooth(.5, .98, tt);                               // the exposed tip catches the light
  if (Math.abs(sx) < .08 && tt > .12) t -= .07;                  // rachis
  const barb = fr((a - Math.abs(b) * 1.1) / .013);               // barbs slanting out from the rachis toward the tip
  t += .045 * (Math.abs(barb - .5) * 2 - .5);
  // shadows of the overlapping edges: an upper-row feather just above, the outer neighbour just beside
  for (const [d, k] of [[.016, .42], [.034, .26], [.055, .12]]) {
    const up = capeTop(x, y - d, f.r - 1);
    if (up && up.f.r < f.r) { t += k; break; }
  }
  const side = capeTop(x + .014, y);
  if (side && side.f !== f && side.f.r === f.r && side.f.c > f.c) t += .2;
  t += .12 * smooth(.55, 1.5, y) + .12 * (1 - smooth(.0, .1, y)) + .14 * smooth(sp, x1, x);
  // the drape: soft vertical folds that open toward the hem
  t += (.035 + .05 * smooth(.2, 1.4, y)) * Math.sin(2 * Math.PI * (x + .04 * Math.sin(y * 3.1)) / (.2 + .06 * y));
  let c = PAL.bronze(clamp(t));
  if (Math.abs(sx) > .8) c = mix(c, PAL.gold(.4 + .25 * clamp(t - .6)), .5 * smooth(.8, .95, Math.abs(sx)) * smooth(.25, .75, tt) * (1 - .6 * clamp(t - .7) * 3));
  if (Math.abs(sx) > .95) c = sink(c, .45);
  c = mix(c, PAL.suit(.85), .3 * smooth(.72, 1.05, t));
  return c;
}
function cape(seg) {
  const {L, X0, X1, sp} = CAPE[seg - 1];
  return (u, v) => {
    const x = X0 + u * (X1 - X0), y = CAPE_TOP[seg - 1] - .01 + v * (L + .02);
    const c = capeColour(x, y, sp, X1);
    if (c) return c;
    return seg === 3 && y > CAPE_Y - .26 ? T : PAL.bronze(.95);   // the ragged hem; elsewhere never reached
  };
}
// the lining (inner faces): near-black brown with the faint shafts of the feathers' undersides
function capeLining(u, v) {
  const k = fr(u * 7 + .2 * Math.sin(v * 9)), sh = Math.abs(k - .5) < .05 ? .08 : 0;
  return mix(PAL.suit(.86 - sh + .06 * (N.e(u * 5, v * 5) - .5)), PAL.bronze(.9), .18 + .1 * v);
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
    face: [64, 64, face, false], hair_lock: [32, 64, hairLock, false], hair_fringe: [64, 48, hairFringe, false],
    hair_back: [48, 48, hairBack, false], hair_tip: [48, 32, hairTip, false], ring: [32, 32, ring, false],
    tendril: [32, 192, tendrilSpr, false], sword_blade: [32, 320, bladeFlat, false],
    edge: [16, 256, edgeGlow, true], edge_fire: [32, 1024, edgeFire, true, {animation: {frametime: 2, width: 32, height: 256}}],
    edge_volt: [32, 1024, edgeVolt, true, {animation: {frametime: 2, width: 32, height: 256}}],
    skull: [32, 32, skullGlow, true], grid: [32, 32, gridGlow, true], cape_in: [32, 32, capeLining, false],
  });
  for (let i = 1; i <= 3; i++) {
    S['cape_' + i] = [128, 112, cape(i), false];
    S['wing_' + i] = [128, 96, wing(i, false, false), false]; S['wing_' + i + 'b'] = [128, 96, wing(i, true, false), false];
    S['wing_a' + i] = [128, 96, wing(i, false, true), false]; S['wing_a' + i + 'b'] = [128, 96, wing(i, true, true), false];
  }
  return S;
}
export function paintTachy(rp, sprites = tachySprites()) {
  const set = Object.fromEntries(Object.entries(sprites).map(([n, [w, h, fn, tr, meta]]) => [n, [w, h, fn, tr, meta]]));
  return paintSpriteSet(rp, TEX_DIR, set, spriteId);
}
