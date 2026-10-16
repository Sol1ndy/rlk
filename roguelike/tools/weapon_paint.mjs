// Painted weapon textures for Arlecchino's scythe (붉은 달의 형상 / Crimson Moon's Semblance,
// scythe form) and Skirk's sword (창백한 섬광 / Azurelight). Pure Node (zlib only), so
// `node tools/build_player_rig.mjs --resourcepack <rp>` keeps working without extra tools.
//
// Every sprite is written to assets/rlk/textures/player_motion/weapons/<name>.png and merged
// into assets/minecraft/atlases/items.json (append only; the pack's other entries stay).
// Colours are smooth gradients sampled per pixel (4x supersampled), so the blades read as
// lacquer, steel and glowing edges rather than flat concrete blocks.
//
// Sprites and how the models map them (u = texture x 0..1 left -> right, v = y top -> bottom):
//   sk_blade*      alpha-cut blade silhouette on a card spanning SK (x CX+-HM, y ROOT..TIP);
//                  the thin core boxes inside it reuse the same mapping on their broad faces
//   sk_wing*       alpha-cut hilt wings on a card spanning WING; hub at (8, WING.HY)
//   sk_side*       silver bevel for the blade core's narrow faces
//   sk_guard       dark navy metal with a silver border and filigree (any face)
//   sk_star*       four-pointed dawn star gem (guard centre and pommel)
//   sk_grip        navy wrap with silver diamonds, v along the grip
//   ar_shaft       black lacquer with crimson pinstripes, v along the shaft
//   ar_crescent*   alpha-cut crescent on a card spanning CRES (scaled for the smaller form)
//   ar_crown*      alpha-cut crimson moon with eight radiating blades, CROWN.S wide
//   ar_tip         alpha-cut gold lance point on two crossed cards spanning TIP
//   ar_metal / ar_gold / ar_gem  dark silver and gold fittings, a red gem
//   nv_* / np_*    Navia's halberd and parasol, painted in navia_weapon_paint.mjs
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import {naviaWeaponSprites} from './navia_weapon_paint.mjs';

const CRC = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    t[n] = c >>> 0;
  }
  return t;
})();
const crc32 = buf => {
  let c = 0xffffffff;
  for (const b of buf) c = CRC[(c ^ b) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
};
export function png(w, h, rgba) {
  const chunk = (type, data) => {
    const len = Buffer.alloc(4); len.writeUInt32BE(data.length);
    const td = Buffer.concat([Buffer.from(type, 'ascii'), data]);
    const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(td));
    return Buffer.concat([len, td, crc]);
  };
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4); ihdr[8] = 8; ihdr[9] = 6;
  const raw = Buffer.alloc((w * 4 + 1) * h);
  for (let y = 0; y < h; y++) {
    raw[y * (w * 4 + 1)] = 0;
    rgba.copy(raw, y * (w * 4 + 1) + 1, y * w * 4, (y + 1) * w * 4);
  }
  return Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk('IHDR', ihdr),
    chunk('IDAT', zlib.deflateSync(raw, {level: 9})), chunk('IEND', Buffer.alloc(0))]);
}

// ---- small colour helpers --------------------------------------------------------------
export const hex = s => [parseInt(s.slice(1, 3), 16), parseInt(s.slice(3, 5), 16), parseInt(s.slice(5, 7), 16), 255];
export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const smooth = (e0, e1, x) => { const t = clamp((x - e0) / (e1 - e0)); return t * t * (3 - 2 * t); };
export const mix = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);
export function ramp(stops) {
  // stops: [[pos, '#rrggbb'], ...] sorted by pos
  const s = stops.map(([p, c]) => [p, typeof c === 'string' ? hex(c) : c]);
  return x => {
    if (x <= s[0][0]) return s[0][1];
    for (let i = 1; i < s.length; i++) if (x <= s[i][0]) {
      const t = (x - s[i - 1][0]) / (s[i][0] - s[i - 1][0]);
      return mix(s[i - 1][1], s[i][1], t * t * (3 - 2 * t));
    }
    return s[s.length - 1][1];
  };
}
export const over = (base, top, a) => mix(base, [...top.slice(0, 3), 255], clamp(a));
// Deterministic value noise.
export function noise2(seed) {
  const h = (x, y) => { let n = (x * 374761393 + y * 668265263 + seed * 2246822519) | 0; n = (n ^ (n >>> 13)) * 1274126177 | 0; return ((n ^ (n >>> 16)) >>> 0) / 4294967295; };
  return (x, y) => {
    const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
    const sx = xf * xf * (3 - 2 * xf), sy = yf * yf * (3 - 2 * yf);
    const a = h(xi, yi), b = h(xi + 1, yi), c = h(xi, yi + 1), d = h(xi + 1, yi + 1);
    return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy;
  };
}
export function fbm(seed) { const n = noise2(seed); return (x, y) => .5 * n(x, y) + .25 * n(2 * x + 7, 2 * y + 3) + .125 * n(4 * x + 1, 4 * y + 9) + .125 * n(8 * x + 5, 8 * y + 2); }

export function paint(w, h, fn, ss = 4) {
  const buf = Buffer.alloc(w * h * 4);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const acc = [0, 0, 0, 0];
    for (let j = 0; j < ss; j++) for (let i = 0; i < ss; i++) {
      const c = fn((x + (i + .5) / ss) / w, (y + (j + .5) / ss) / h);
      const a = c[3] / 255;
      acc[0] += c[0] * a; acc[1] += c[1] * a; acc[2] += c[2] * a; acc[3] += a;
    }
    const o = (y * w + x) * 4, n = ss * ss;
    const alpha = acc[3] / n;
    buf[o + 3] = alpha < .5 ? 0 : 255;   // cutout: opaque or fully transparent
    for (let k = 0; k < 3; k++) buf[o + k] = Math.round(clamp(acc[3] > 0 ? acc[k] / acc[3] : 0, 0, 255));
  }
  return buf;
}

// Four-pointed star intensity at (dx, dy) in units of its radius.
export const star4 = (dx, dy, r) => {
  const ax = Math.abs(dx), ay = Math.abs(dy);
  const arm = Math.max(1 - (ax / r) - ay * 9 / r, 1 - (ay / r) - ax * 9 / r, 0);
  const core = Math.max(0, 1 - Math.hypot(dx, dy) / (r * .28));
  return clamp(arm * 1.4 + core);
};

// ---- Shared silhouettes (model units; the geometry files place cards on exactly these boxes) ---
// Skirk's blade card: x CX±HM, y ROOT..TIP. Half-width (fraction of HM) along t = 0 root .. 1 tip:
// a long gentle taper, then an ogive point.
export const SK = {CX: 8, HM: 1.22, ROOT: 11.0, TIP: 31.8};
export function skProfile(t) {
  if (t < 0) return 0;
  if (t <= .8) return .94 - .2 * t;
  const s = (t - .8) / .2, base = .94 - .16;
  return s >= 1 ? 0 : base * Math.pow(1 - Math.pow(s, 1.7), .7);
}
// Skirk's winged guard card: x WING.X0..X1, y WING.Y0..Y1, hub at (8, WING.HY).
export const WING = {X0: 2.2, X1: 13.8, Y0: 8.9, Y1: 15.2, HY: 10.9};
// Feathers per wing: [angle above horizontal (deg), length, half-width], top (leading) first.
const FEATHERS = [[50, 5.2, .6], [37, 5.1, .6], [24, 4.8, .58], [11, 4.3, .55], [-2, 3.7, .5], [-15, 3.0, .45]];
// Arlecchino's crescent: an elliptical arc (centre CX,CY, radii A,B) from the haft (TH0)
// to the point (TH1); the blade hangs inward from the outer arc by W0 tapering to 0.
export const CRES = {CX: 5.0, CY: 15.5, A: 15, B: 12.8, TH0: 76.1, TH1: 193, W0: 3.3,
  X0: -10.6, X1: 9.0, Y0: 12.2, Y1: 28.6};
export function cresWidth(s) {
  return CRES.W0 * (.9 + .1 * Math.sin(Math.min(s / .25, 1) * Math.PI / 2)) * Math.pow(Math.max(0, 1 - Math.pow(s, 1.5)), .85);
}
// Crown of the head: the crimson moon ringed by eight blades, card CROWN.S wide at (8, CROWN.Y).
export const CROWN = {Y: 25.4, S: 6.4};
// Gold lance point above the crown, shown on two crossed cards: x/z 8+-TIP.HW, y TIP.Y0..Y1.
export const TIP = {HW: 1.0, Y0: 27.0, Y1: 32.0};

export const TRANSPARENT = [0, 0, 0, 0];

// ---- Skirk: 창백한 섬광 (Azurelight) ----------------------------------------------------------
// "Once pure and pristine as a white dawn star, since tinted a deep, dark blue": silver-white
// edges, a deep navy-indigo body whose dawn-white fuller glows along the centre and fades into
// the blue toward the point, dawn-star glints, and a white root where the old colour remains.
function skBlade(cryo) {
  const body = cryo
    ? ramp([[0, '#e4fbff'], [.10, '#9fe3ff'], [.26, '#3f9be6'], [.55, '#1f4fae'], [1, '#13246a']])
    : ramp([[0, '#f4f7ff'], [.09, '#b8c9f4'], [.24, '#3d63c9'], [.52, '#1d2c86'], [1, '#0e1552']]);
  const n = fbm(cryo ? 41 : 17);
  const stars = [[.5, .12, .03], [.48, .27, .022], [.52, .41, .026], [.49, .56, .02], [.51, .7, .024], [.5, .83, .018]];
  return (u, v) => {
    const t = 1 - v, x = (u - .5) * 2, f = skProfile(t);
    if (Math.abs(x) > f) return TRANSPARENT;
    const e = (f - Math.abs(x)) / Math.max(f, .05);            // 0 at the edge .. 1 on the axis
    const edgeBand = .2;
    if (e < edgeBand) {
      const k = e / edgeBand;
      return mix(hex('#ffffff'), hex(cryo ? '#a9dcff' : '#aebbe0'), smooth(.1, 1, k));
    }
    // Inner bevel line where the edge meets the body.
    let c = body(1 - (e - edgeBand) / (1 - edgeBand) * .999);
    c = mix(c, hex(cryo ? '#6fcfff' : '#7d93d8'), Math.max(0, 1 - Math.abs(e - edgeBand - .03) / .03) * .7);
    // The dawn-white root fading into the blue over the first fifth of the blade.
    c = mix(c, hex('#f1f5ff'), (1 - smooth(.02, .2, t)) * .85 * (1 - Math.abs(x) * .4));
    // Soft diagonal sheen and steel grain.
    c = mix(c, hex('#ffffff'), Math.pow(Math.max(0, Math.sin((u * 1.3 + v * 3.1) * Math.PI)), 10) * .18);
    c = mix(c, hex('#050a2a'), (n(u * 5, v * 34) - .5) * .22);
    // Dawn-star glints on the fuller.
    for (const [sx, sy, r] of stars) {
      const s = star4((u - sx) * .3, v - sy, r);
      if (s > 0) c = over(c, hex(cryo ? '#eafcff' : '#ffffff'), s);
    }
    return c;
  };
}
const skSide = (cryo) => (u, v) => mix(hex('#e8eefc'), hex(cryo ? '#7ec8f2' : '#8e9cc0'), Math.abs(u - .5) * 2);
function skGuard() {
  const n = fbm(5);
  return (u, v) => {
    const e = Math.min(u, v, 1 - u, 1 - v);
    if (e < .08) return mix(hex('#e3e9f6'), hex('#8c97b4'), e / .08);
    let c = mix(hex('#24305e'), hex('#121838'), n(u * 4, v * 4) * .9);
    const f1 = Math.abs(Math.sin(u * 7 + Math.sin(v * 6) * 1.3) * .5 + .5 - v);
    const f2 = Math.abs(Math.cos(v * 7 + Math.sin(u * 6) * 1.3) * .5 + .5 - u);
    const line = Math.max(0, 1 - Math.min(f1, f2) / .035);
    return mix(c, hex('#b8c4de'), line * .85);
  };
}
// The hilt wings (Skirk's wielding of Azurelight grows wings at the grip): two swept wings of
// layered feathers, white-silver tips over azure and a navy root, outlined in deep navy, with
// silver coverts over the roots.
function skWing(cryo) {
  const tip = hex(cryo ? '#f2fdff' : '#f7f9ff'), mid = hex(cryo ? '#86d6ff' : '#9cb6f2'), root = hex('#22306f');
  const rim = hex('#101848');
  const n = fbm(cryo ? 63 : 61);
  // Primary feathers on top of a row of shorter secondaries that fill the gaps between them.
  const primaries = FEATHERS.map(([ang, L, w], k) => ({ang, L, w, k, ox: .5, oy: .1 + k * .05}));
  const secondaries = FEATHERS.slice(0, -1).map(([ang, L, w], k) =>
    ({ang: ang - 6.5, L: L * .72, w: w * .85, k: k + .5, ox: .45, oy: .05 + k * .05}));
  const feathers = [...secondaries, ...primaries.slice().reverse()]
    .map(f => ({...f, ang: f.ang * Math.PI / 180}));
  function feather(f, lx, ly) {
    const dx = lx - f.ox, dy = ly - f.oy;
    const a = dx * Math.cos(f.ang) + dy * Math.sin(f.ang), b = -dx * Math.sin(f.ang) + dy * Math.cos(f.ang);
    if (a < 0 || a > f.L) return null;
    const s = a / f.L;
    // Gently curved, widest past the middle, ending in a fine point that curls upward.
    const bow = .22 * f.w * Math.sin(Math.PI * s) + .25 * f.w * s * s;
    const h = f.w * Math.pow(Math.sin(Math.PI * Math.min(1, .1 + s * .9)), .55) * (1 - .2 * s);
    const off = b - bow, d = Math.abs(off) / Math.max(h, 1e-3);
    if (d > 1) return null;
    let c = s < .45 ? mix(root, mid, smooth(.05, .45, s)) : mix(mid, tip, smooth(.45, .92, s));
    c = mix(c, hex('#ffffff'), Math.max(0, 1 - Math.abs(off) / (.07 * f.w)) * .55 * (s < .92 ? 1 : 0));   // rachis
    // Fine barbs slanting toward the tip, and a soft shade on the trailing vane.
    const barb = Math.abs(((a * 7 - Math.abs(off) * 4) % 1 + 1) % 1 - .5);
    if (barb < .05) c = mix(c, root, .18);
    if (off < 0) c = mix(c, root, .12);
    c = mix(c, hex('#000020'), (n(a * 6, b * 6) - .5) * .14);
    if (d > .82) c = mix(c, rim, (d - .82) / .18 * .9);                                            // outline
    return c;
  }
  return (u, v) => {
    const X = WING.X0 + u * (WING.X1 - WING.X0), Y = WING.Y1 - v * (WING.Y1 - WING.Y0);
    const lx = Math.abs(X - 8), ly = Y - WING.HY;               // mirrored local coords
    let col = null;
    for (const f of feathers) {
      const c = feather(f, lx, ly);
      if (c) col = c;
    }
    // Silver coverts over the roots: rows of small rounded scales, outlined in navy.
    const cx = lx - 1.2, cy = ly - .55, rot = .5;
    const ex = cx * Math.cos(rot) + cy * Math.sin(rot), ey = -cx * Math.sin(rot) + cy * Math.cos(rot);
    const er = Math.hypot(ex / 1.2, ey / .6);
    if (er <= 1) {
      let c = mix(hex('#f4f7ff'), hex('#9eabd0'), smooth(.15, 1, er));
      const fx = ((ex * 3.4 + 10) % 1 + 1) % 1, fy = ((ey * 3.0 + 10 + (Math.floor(ex * 3.4) % 2) * .5) % 1 + 1) % 1;
      const scale = Math.abs(Math.hypot(fx - .15, fy - .5) - .5);
      if (scale < .07) c = mix(c, hex('#4a5c9c'), .65);
      if (er > .86) c = mix(c, rim, (er - .86) / .14);
      col = c;
    }
    return col || TRANSPARENT;
  };
}
function skStar(cryo) {
  return (u, v) => {
    const dx = u - .5, dy = v - .5;
    let c = mix(hex('#1b2550'), hex('#0e1430'), Math.hypot(dx, dy) * 1.6);
    const glow = Math.max(0, 1 - Math.hypot(dx, dy) / .5) ** 2;
    c = mix(c, hex(cryo ? '#4fd0ff' : '#3b6fe0'), glow * .8);
    const s = star4(dx, dy, .5);
    c = over(c, mix(hex(cryo ? '#bdf3ff' : '#a9c4ff'), hex('#ffffff'), s), s);
    return c;
  };
}
function skGrip() {
  return (u, v) => {
    const a = (u * 3 + v * 8) % 1, b = (-u * 3 + v * 8 + 10) % 1;
    const band = Math.min(Math.abs(a - .5), Math.abs(b - .5));
    let c = mix(hex('#1c2550'), hex('#2e3c7a'), smooth(.5, 0, Math.abs(u - .5) * 2));
    if (band < .07) c = mix(c, hex('#c8d2ea'), 1 - band / .07);
    return c;
  };
}

// ---- Arlecchino: 붉은 달의 형상 (Crimson Moon's Semblance), her dark-red great scythe ----------
function arShaft() {
  const n = fbm(9);
  return (u, v) => {
    const r = Math.abs(u - .5) * 2;
    let c = mix(hex('#3a2a34'), hex('#0d090c'), smooth(0, .9, r));
    c = mix(c, hex('#000000'), (n(u * 3, v * 40) - .5) * .3);
    const s = Math.abs(((u * .6 + v * 18) % 1) - .5);
    if (s < .035) c = mix(c, hex('#a8122a'), (1 - s / .035) * .9);
    return c;
  };
}
// Crescent: black lacquered spine engraved with crimson moon scrolls, a deep crimson body, a
// scarlet cutting edge (orange-gold and flickering on the infused blade).
function arCrescent(fire) {
  const ramp_ = fire
    ? ramp([[0, '#120a0d'], [.30, '#1d0b10'], [.48, '#5a0c16'], [.70, '#b0182a'], [.86, '#ff5a32'], [.95, '#ffb45a'], [1, '#fff0b8']])
    : ramp([[0, '#110a0e'], [.30, '#1c0c13'], [.50, '#4e0a15'], [.72, '#9a1426'], [.88, '#e2283a'], [.96, '#ff8a8a'], [1, '#ffe4e4']]);
  const n = fbm(fire ? 77 : 23);
  const {CX, CY, A, B, TH0, TH1} = CRES;
  return (u, v) => {
    const X = CRES.X0 + u * (CRES.X1 - CRES.X0), Y = CRES.Y1 - v * (CRES.Y1 - CRES.Y0);
    const ex = (X - CX) / A, ey = (Y - CY) / B, rho = Math.hypot(ex, ey);
    let th = Math.atan2(ey, ex) * 180 / Math.PI;
    if (th < 0) th += 360;
    if (th < TH0 || th > TH1 || rho > 1) return TRANSPARENT;
    const s = (th - TH0) / (TH1 - TH0);
    const R = Math.hypot(A * Math.cos(th * Math.PI / 180), B * Math.sin(th * Math.PI / 180));
    const w = cresWidth(s), rin = 1 - w / R;
    if (rho < rin) return TRANSPARENT;
    const q = (1 - rho) / (1 - rin);              // 0 spine .. 1 cutting edge
    let c = ramp_(q);
    // Engraved scrolls in the black spine, repeated along the blade.
    if (q < .42) {
      const k = (s * 7) % 1, depth = q / .42;
      const ring = Math.abs(Math.hypot(k - .5, (depth - .5) * .9) - .3);
      const cut = Math.hypot(k - .62, (depth - .42) * .9) < .26;
      if (ring < .045 && !cut) c = mix(c, hex(fire ? '#c0302a' : '#9a1a2a'), (1 - ring / .045) * .9);
    }
    // A fine groove just inside the edge, hammered grain, hot flicker on the infused edge.
    c = mix(c, hex('#20040a'), Math.max(0, 1 - Math.abs(q - .8) / .018) * .6);
    c = mix(c, hex('#000000'), (n(s * 40, q * 5) - .5) * .22);
    if (fire) c = mix(c, hex('#ffe08a'), Math.max(0, n(s * 22 + 3, q * 3) - .55) * 1.6 * smooth(.8, 1, q));
    // Dark rim along the spine.
    if (q < .035) c = mix(c, hex('#3a0710'), .8);
    return c;
  };
}
// The crimson moon at the head: an eclipsed blood-red disc in a gold-trimmed ring, with eight
// radiating crimson blades (long on the axes, short on the diagonals) on a black sunburst.
function arCrown(fire) {
  const MOON = .2, RING = .235, BASE = .27;
  return (u, v) => {
    const dx = u - .5, dy = .5 - v, r = Math.hypot(dx, dy);
    let a = Math.atan2(dy, dx) * 180 / Math.PI; if (a < 0) a += 360;
    const k = Math.round(a / 45) % 8;
    let da = Math.abs(a - k * 45); if (da > 180) da = 360 - da;
    if (r <= MOON) {
      let c = mix(hex(fire ? '#ff6a3a' : '#ff3b47'), hex('#6e0512'), smooth(0, MOON, r));
      const e = Math.hypot(dx + .04, dy - .036);
      c = mix(c, hex('#140508'), smooth(MOON * .8, MOON * .7, e));
      return c;
    }
    if (r <= RING) return mix(hex('#ffe6a0'), hex('#a8781e'), Math.abs(r - (MOON + RING) / 2) / ((RING - MOON) / 2));
    if (r <= BASE) return mix(hex('#1a0d10'), hex('#050304'), (r - RING) / (BASE - RING));
    const tipR = k % 2 === 0 ? .5 : .43;
    if (r > tipR) return TRANSPARENT;
    const half = 19 * (tipR - r) / (tipR - BASE + .02);
    if (da > half) return TRANSPARENT;
    const ridge = da / Math.max(half, 1e-3);
    let c = mix(hex(fire ? '#ff7a3a' : '#e0243a'), hex('#5a0812'), smooth(.3, 1, ridge));
    c = mix(c, hex('#0c0306'), Math.max(0, 1 - ridge / .16) * .75);                           // black ridge
    if (r > tipR - .035) c = mix(c, hex('#ffd27a'), .85);                                     // gilded points
    return c;
  };
}
const arMetal = () => (u, v) => mix(hex('#c6cad3'), hex('#4c505a'), smooth(.1, .9, Math.abs(u - .35) * 1.4 + v * .3));
const arGold = () => (u, v) => mix(hex('#fff0b0'), hex('#8a5a12'), smooth(.05, .95, Math.abs(u - .3) * 1.3 + v * .25));
// Gold lance point: a slim leaf blade with a crimson fuller and a dark collar notch.
const arTip = () => (u, v) => {
  const x = Math.abs(u - .5) * 2, t = 1 - v;                    // t: 0 collar .. 1 point
  const half = t < .12 ? .55 : t < .3 ? .55 + (t - .12) / .18 * .45 : Math.pow(Math.max(0, (1 - t) / .7), .9);
  if (x > half) return TRANSPARENT;
  const e = 1 - x / Math.max(half, 1e-3);
  let c = mix(hex('#8a5a12'), hex('#fff2b8'), smooth(0, .55, e));
  if (t > .14 && x < .16 * half + .02) c = mix(c, hex('#a3121f'), .85);
  if (t < .12) c = mix(c, hex('#3a2208'), .35);
  return c;
};
const arGem = () => (u, v) => {
  const r = Math.hypot(u - .5, v - .5);
  return mix(mix(hex('#ff8a8a'), hex('#c0102a'), smooth(0, .3, r)), hex('#3a0208'), smooth(.3, .5, r));
};

export const WEAPON_SPRITES = {
  sk_blade: [64, 512, skBlade(false)], sk_blade_cryo: [64, 512, skBlade(true)],
  sk_side: [16, 128, skSide(false)], sk_side_cryo: [16, 128, skSide(true)],
  sk_wing: [352, 192, skWing(false)], sk_wing_cryo: [352, 192, skWing(true)],
  sk_guard: [64, 64, skGuard()], sk_star: [64, 64, skStar(false)], sk_star_cryo: [64, 64, skStar(true)],
  sk_grip: [32, 64, skGrip()],
  ar_shaft: [32, 256, arShaft()],
  ar_crescent: [320, 272, arCrescent(false)], ar_crescent_fire: [320, 272, arCrescent(true)],
  ar_crown: [128, 128, arCrown(false)], ar_crown_fire: [128, 128, arCrown(true)],
  ar_metal: [32, 32, arMetal()], ar_gold: [32, 32, arGold()], ar_gem: [32, 32, arGem()], ar_tip: [48, 160, arTip()],
};
export const spriteId = name => 'rlk:player_motion/weapons/' + name;

export function paintWeaponTextures(rp) {
  const dir = path.join(rp, 'assets/rlk/textures/player_motion/weapons');
  fs.mkdirSync(dir, {recursive: true});
  // Navia's sprites live in navia_weapon_paint.mjs, which reuses the helpers above; they are
  // built here (not at module load) because the two modules import each other.
  const sprites = {...WEAPON_SPRITES, ...naviaWeaponSprites()};
  for (const [name, [w, h, fn]] of Object.entries(sprites)) fs.writeFileSync(path.join(dir, name + '.png'), png(w, h, paint(w, h, fn)));
  const atlasPath = path.join(rp, 'assets/minecraft/atlases/items.json');
  const atlas = fs.existsSync(atlasPath) ? JSON.parse(fs.readFileSync(atlasPath, 'utf8')) : {sources: []};
  const known = new Set(atlas.sources.map(s => s.sprite || s.resource));
  for (const name of Object.keys(sprites)) {
    const id = spriteId(name);
    if (!known.has(id)) atlas.sources.push({type: 'minecraft:single', resource: id});
  }
  fs.mkdirSync(path.dirname(atlasPath), {recursive: true});
  fs.writeFileSync(atlasPath, JSON.stringify(atlas, null, 2) + '\n');
  return Object.keys(sprites).length;
}
