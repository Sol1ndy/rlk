// Shared painter + box-model helpers for the chapter-2/3 mob rig generators (tools/build_ch2_swarm_rigs.mjs,
// tools/build_ch3_swarm_rigs.mjs). Pure functions: no file IO. Deterministic (seeded LCG), PNG via node:zlib.
import zlib from 'node:zlib';

// ---------------------------------------------------------------- png
const CRC = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
const crc32 = b => { let c = 0xffffffff; for (const x of b) c = CRC[(c ^ x) & 0xff] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; };
export function png(w, h, rgba) {
  const chunk = (type, data) => { const len = Buffer.alloc(4); len.writeUInt32BE(data.length); const td = Buffer.concat([Buffer.from(type, 'ascii'), data]); const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(td)); return Buffer.concat([len, td, crc]); };
  const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4); ihdr[8] = 8; ihdr[9] = 6;
  const raw = Buffer.alloc((w * 4 + 1) * h);
  for (let y = 0; y < h; y++) { raw[y * (w * 4 + 1)] = 0; rgba.copy(raw, y * (w * 4 + 1) + 1, y * w * 4, (y + 1) * w * 4); }
  return Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk('IHDR', ihdr), chunk('IDAT', zlib.deflateSync(raw, {level: 9})), chunk('IEND', Buffer.alloc(0))]);
}

// ---------------------------------------------------------------- tiny deterministic painter
export class Canvas {
  constructor(w, h, seed = 1) { this.w = w; this.h = h; this.d = Buffer.alloc(w * h * 4); this.s = seed >>> 0; }
  rnd() { this.s = (Math.imul(this.s, 1664525) + 1013904223) >>> 0; return this.s / 4294967296; }
  px(x, y, c) { if (x < 0 || y < 0 || x >= this.w || y >= this.h) return; const i = (y * this.w + x) * 4; this.d[i] = c[0]; this.d[i + 1] = c[1]; this.d[i + 2] = c[2]; this.d[i + 3] = c[3] ?? 255; }
  // filled rect with per-pixel value noise (+-n) and optional vertical gradient (top -> bottom factor)
  rect(x, y, w, h, c, n = 10, g = 0) {
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
      const k = (this.rnd() * 2 - 1) * n + (h > 1 ? g * (j / (h - 1) - 0.5) : 0);
      this.px(x + i, y + j, [cl(c[0] + k), cl(c[1] + k), cl(c[2] + k), c[3] ?? 255]);
    }
  }
  line(x0, y0, x1, y1, c) { const n = Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0)) || 1; for (let i = 0; i <= n; i++) this.px(Math.round(x0 + (x1 - x0) * i / n), Math.round(y0 + (y1 - y0) * i / n), c); }
  clear(x, y, w, h) { for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) this.px(x + i, y + j, [0, 0, 0, 0]); }
  png() { return png(this.w, this.h, this.d); }
}
export const cl = v => Math.max(0, Math.min(255, Math.round(v)));
export const hex = s => [parseInt(s.slice(1, 3), 16), parseInt(s.slice(3, 5), 16), parseInt(s.slice(5, 7), 16), 255];
export const A = (c, a) => [c[0], c[1], c[2], a];

// Standard 64x64 skin regions: [u, v, w, h, d] box layout (same as the player skin).
export const R = {head: [0, 0, 8, 8, 8], hat: [32, 0, 8, 8, 8], body: [16, 16, 8, 12, 4], jacket: [16, 32, 8, 12, 4],
  rarm: [40, 16, 4, 12, 4], rsleeve: [40, 32, 4, 12, 4], larm: [32, 48, 4, 12, 4], lsleeve: [48, 48, 4, 12, 4],
  rleg: [0, 16, 4, 12, 4], rpants: [0, 32, 4, 12, 4], lleg: [16, 48, 4, 12, 4], lpants: [0, 48, 4, 12, 4]};
// paint every face of a box region with fn(face, x, y, w, h)
export function boxPaint(cv, [u, v, w, h, d], fn) {
  fn('top', u + d, v, w, d); fn('bottom', u + d + w, v, w, d);
  fn('right', u, v + d, d, h); fn('front', u + d, v + d, w, h); fn('left', u + d + w, v + d, d, h); fn('back', u + 2 * d + w, v + d, w, h);
}
export const all = (cv, reg, c, n = 10, g = 0) => boxPaint(cv, reg, (f, x, y, w, h) => cv.rect(x, y, w, h, c, n, g));

// ---------------------------------------------------------------- model helpers (same box UV as tools/build_swordsman.mjs)
export function faces(u, v, w, h, d, tex = '#skin') {
  const face = (x1, y1, x2, y2) => ({uv: [x1 / 4, y1 / 4, x2 / 4, y2 / 4], texture: tex, tintindex: 0});
  return {east: face(u, v + d, u + d, v + d + h), north: face(u + d, v + d, u + d + w, v + d + h), west: face(u + d + w, v + d, u + 2 * d + w, v + d + h),
    south: face(u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h), up: face(u + d, v, u + d + w, v + d), down: face(u + d + w, v + d, u + d + 2 * w, v)};
}
export const box = (from, to, uv, inflate = 0) => ({from: from.map(x => x - inflate), to: to.map(x => x + inflate), faces: faces(...uv)});
export const r6 = v => Number(v.toFixed(4));
// solid box with one props tile on all faces; rot = {axis, angle, origin}
export const SHAPES = {
  head: {from: [4, 8, 4], to: [12, 16, 12], uv: [0, 0, 8, 8, 8], over: [32, 0, 8, 8, 8], inflate: .5},
  body: {from: [4, -4, 6], to: [12, 8, 10], uv: [16, 16, 8, 12, 4], over: [16, 32, 8, 12, 4], inflate: .25},
  right_arm: {from: [6, -2, 6], to: [10, 10, 10], uv: [40, 16, 4, 12, 4], over: [40, 32, 4, 12, 4], inflate: .25},
  left_arm: {from: [6, -2, 6], to: [10, 10, 10], uv: [32, 48, 4, 12, 4], over: [48, 48, 4, 12, 4], inflate: .25},
  right_leg: {from: [6, -4, 6], to: [10, 8, 10], uv: [0, 16, 4, 12, 4], over: [0, 32, 4, 12, 4], inflate: .25},
  left_leg: {from: [6, -4, 6], to: [10, 8, 10], uv: [16, 48, 4, 12, 4], over: [0, 48, 4, 12, 4], inflate: .25}
};
