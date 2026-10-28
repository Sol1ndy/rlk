// Chapter-2 swarm mob rigs (Inazuma): 떠돌이 무사 졸개 (ns), 번개 슬라임 (sl/ss), 반란군 창병 (sp), 오니 북잡이 (dr).
// Original geometry and procedurally painted textures; no reference-pack assets are copied.
// Run: node tools/build_ch2_swarm_rigs.mjs --resourcepack <unpacked resource pack>
// Writes only resource-pack files: models/item/cm/c2/**, items/cm/c2/**, textures/skin/mob_c2_*.png,
// textures/cm/c2/*.png, and merges its sprites into assets/minecraft/atlases/items.json (filter-then-push by id).
// The datapack side (rig poses, AI) is written by tools/build_ch2_mobs.py; the part lists below must match
// tools/ch2mob/swarm.py (PARTS).
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';

const arg = name => { const i = process.argv.indexOf(name); return i < 0 ? undefined : process.argv[i + 1]; };
const rpArg = arg('--resourcepack');
if (!rpArg) throw new Error('Provide --resourcepack pointing to an unpacked resource pack.');
const rpRoot = path.resolve(rpArg);
if (!fs.existsSync(path.join(rpRoot, 'pack.mcmeta'))) throw new Error('The resource pack must contain pack.mcmeta.');
const rp = path.join(rpRoot, 'assets/rlk');
const put = (p, s) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, s); };
const json = (p, o) => put(p, JSON.stringify(o, null, 2) + '\n');

// ---------------------------------------------------------------- png
const CRC = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
const crc32 = b => { let c = 0xffffffff; for (const x of b) c = CRC[(c ^ x) & 0xff] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; };
function png(w, h, rgba) {
  const chunk = (type, data) => { const len = Buffer.alloc(4); len.writeUInt32BE(data.length); const td = Buffer.concat([Buffer.from(type, 'ascii'), data]); const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(td)); return Buffer.concat([len, td, crc]); };
  const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4); ihdr[8] = 8; ihdr[9] = 6;
  const raw = Buffer.alloc((w * 4 + 1) * h);
  for (let y = 0; y < h; y++) { raw[y * (w * 4 + 1)] = 0; rgba.copy(raw, y * (w * 4 + 1) + 1, y * w * 4, (y + 1) * w * 4); }
  return Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk('IHDR', ihdr), chunk('IDAT', zlib.deflateSync(raw, {level: 9})), chunk('IEND', Buffer.alloc(0))]);
}

// ---------------------------------------------------------------- tiny deterministic painter
class Canvas {
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
const cl = v => Math.max(0, Math.min(255, Math.round(v)));
const hex = s => [parseInt(s.slice(1, 3), 16), parseInt(s.slice(3, 5), 16), parseInt(s.slice(5, 7), 16), 255];
const A = (c, a) => [c[0], c[1], c[2], a];

// Standard 64x64 skin regions: [u, v, w, h, d] box layout (same as the player skin).
const R = {head: [0, 0, 8, 8, 8], hat: [32, 0, 8, 8, 8], body: [16, 16, 8, 12, 4], jacket: [16, 32, 8, 12, 4],
  rarm: [40, 16, 4, 12, 4], rsleeve: [40, 32, 4, 12, 4], larm: [32, 48, 4, 12, 4], lsleeve: [48, 48, 4, 12, 4],
  rleg: [0, 16, 4, 12, 4], rpants: [0, 32, 4, 12, 4], lleg: [16, 48, 4, 12, 4], lpants: [0, 48, 4, 12, 4]};
// paint every face of a box region with fn(face, x, y, w, h)
function boxPaint(cv, [u, v, w, h, d], fn) {
  fn('top', u + d, v, w, d); fn('bottom', u + d + w, v, w, d);
  fn('right', u, v + d, d, h); fn('front', u + d, v + d, w, h); fn('left', u + d + w, v + d, d, h); fn('back', u + 2 * d + w, v + d, w, h);
}
const all = (cv, reg, c, n = 10, g = 0) => boxPaint(cv, reg, (f, x, y, w, h) => cv.rect(x, y, w, h, c, n, g));

// ---------------------------------------------------------------- skins
function skinRonin() {
  const cv = new Canvas(64, 64, 11);
  const skin = hex('#c99a74'), skinD = hex('#a57a58'), hair = hex('#1c1716'), kim = hex('#2f3550'), kimD = hex('#22263a');
  const under = hex('#b9b2a2'), hakama = hex('#5a5249'), hakD = hex('#433d36'), straw = hex('#c8a45a'), wrap = hex('#d8d0bc');
  // head: tanned face, stubble, tired eyes, messy topknot hair at the back
  all(cv, R.head, skin, 8);
  boxPaint(cv, R.head, (f, x, y, w, h) => {
    if (f === 'top' || f === 'back') cv.rect(x, y, w, h, hair, 8);
    if (f === 'right' || f === 'left') { cv.rect(x, y, w, 3, hair, 8); cv.rect(x + (f === 'right' ? 6 : 0), y + 3, 2, 3, hair, 6); }
    if (f === 'front') {
      cv.rect(x, y, w, 2, hair, 8); cv.px(x + 1, y + 2, hair); cv.px(x + 6, y + 2, hair);
      cv.rect(x + 1, y + 3, 2, 1, hex('#2a2220')); cv.rect(x + 5, y + 3, 2, 1, hex('#2a2220'));
      cv.px(x + 2, y + 4, hex('#f1e7d6')); cv.px(x + 5, y + 4, hex('#f1e7d6')); cv.px(x + 1, y + 4, hex('#3b2a25')); cv.px(x + 6, y + 4, hex('#3b2a25'));
      cv.rect(x + 1, y + 6, 6, 2, skinD, 10); cv.rect(x + 3, y + 6, 2, 1, hex('#6e4a3c'));
      cv.line(x + 2, y + 2, x + 3, y + 5, hex('#8a5e48')); // old scar
    }
  });
  // hat overlay: ragged headband tail at the back
  cv.clear(32, 0, 32, 16);
  boxPaint(cv, R.hat, (f, x, y, w, h) => { if (f === 'back') { cv.rect(x + 2, y + 5, 4, 1, hex('#7a2f2f'), 6); cv.rect(x + 3, y + 6, 2, 2, hex('#7a2f2f'), 6); } });
  // body: indigo kimono, crossed collar showing the pale undergarment, straw-rope obi
  all(cv, R.body, kim, 9, -14);
  boxPaint(cv, R.body, (f, x, y, w, h) => {
    if (f === 'front') {
      for (let j = 0; j < 6; j++) { cv.px(x + 3 - Math.floor(j / 2), y + j, under); cv.px(x + 4 + Math.floor(j / 2), y + j, under); cv.px(x + 3, y + j, j < 4 ? under : kimD); cv.px(x + 4, y + j, j < 4 ? under : kimD); }
      cv.line(x + 4, y, x + 1, y + 7, kimD);
    }
    if (f !== 'top' && f !== 'bottom') { cv.rect(x, y + 7, w, 2, straw, 12); for (let i = 0; i < w; i += 2) cv.px(x + i, y + 8, hex('#9c7c3e')); cv.rect(x, y + 9, w, 3, hakama, 8); }
  });
  // jacket overlay: torn hem flaps
  cv.clear(16, 32, 24, 16);
  boxPaint(cv, R.jacket, (f, x, y, w, h) => { if (f === 'front' || f === 'back') for (let i = 0; i < w; i++) if ((i * 7 + 3) % 5 < 2) cv.rect(x + i, y + 9, 1, 2 + (i % 2), kimD, 6); });
  // arms: indigo sleeves to the elbow, bandaged forearm, bare hand
  for (const [reg, sl] of [[R.rarm, R.rsleeve], [R.larm, R.lsleeve]]) {
    all(cv, reg, kim, 9);
    boxPaint(cv, reg, (f, x, y, w, h) => {
      if (f === 'top') return;
      if (f === 'bottom') { cv.rect(x, y, w, h, skin, 6); return; }
      cv.rect(x, y + 5, w, 5, wrap, 10); for (let j = 5; j < 10; j += 2) cv.line(x, y + j, x + w - 1, y + j + 1, hex('#aca38f'));
      cv.rect(x, y + 10, w, 2, skin, 6);
    });
    cv.clear(sl[0], sl[1], 16, 16);
    boxPaint(cv, sl, (f, x, y, w, h) => { if (f !== 'top' && f !== 'bottom') { cv.rect(x, y, w, 4, kim, 8); for (let i = 0; i < w; i++) if (i % 3 !== 1) cv.px(x + i, y + 4, kimD); } });
  }
  // legs: hakama, straw sandals
  for (const [reg, ov] of [[R.rleg, R.rpants], [R.lleg, R.lpants]]) {
    all(cv, reg, hakama, 8, -10);
    boxPaint(cv, reg, (f, x, y, w, h) => {
      if (f === 'bottom') { cv.rect(x, y, w, h, straw, 10); return; }
      if (f === 'top') return;
      cv.line(x + 1, y, x + 1, y + 8, hakD); cv.rect(x, y + 9, w, 2, wrap, 6); cv.rect(x, y + 11, w, 1, straw, 10);
    });
    cv.clear(ov[0], ov[1], 16, 16);
  }
  return cv;
}

function skinSpear() {
  const cv = new Canvas(64, 64, 23);
  const skin = hex('#d1a582'), hair = hex('#20232c'), plate = hex('#2c5a6e'), plateD = hex('#1d3b4a'), lace = hex('#c9c3b0');
  const under = hex('#53406e'), white = hex('#e7e3d8'), pants = hex('#3c3552'), greave = hex('#26414f');
  all(cv, R.head, skin, 7);
  boxPaint(cv, R.head, (f, x, y, w, h) => {
    if (f === 'top' || f === 'back') cv.rect(x, y, w, h, hair, 7);
    if (f === 'right' || f === 'left') cv.rect(x, y, w, 3, hair, 7);
    if (f !== 'top' && f !== 'bottom') cv.rect(x, y + 2, w, 1, white, 5); // hachimaki band
    if (f === 'back') { cv.rect(x + 3, y + 3, 2, 4, white, 5); }
    if (f === 'front') {
      cv.rect(x + 1, y + 4, 2, 1, hex('#1b1d24')); cv.rect(x + 5, y + 4, 2, 1, hex('#1b1d24'));
      cv.px(x + 2, y + 4, hex('#4f7d8c')); cv.px(x + 5, y + 4, hex('#4f7d8c'));
      cv.rect(x + 1, y + 6, 6, 2, plateD, 6); cv.rect(x + 2, y + 6, 4, 1, plate, 6); // menpo half-mask
    }
  });
  cv.clear(32, 0, 32, 16);
  // body: teal lamellar rows laced in pale cord, violet undercoat
  all(cv, R.body, plate, 6);
  boxPaint(cv, R.body, (f, x, y, w, h) => {
    if (f === 'top' || f === 'bottom') return;
    for (let j = 0; j < h; j += 3) { cv.rect(x, y + j + 2, w, 1, plateD, 4); for (let i = j % 2; i < w; i += 2) cv.px(x + i, y + j + 1, lace); }
    cv.rect(x, y + 9, w, 3, under, 6);
    if (f === 'front') { cv.rect(x + 3, y, 2, 2, under, 4); cv.rect(x + 3, y + 4, 2, 2, hex('#d8b34a'), 8); }
  });
  cv.clear(16, 32, 24, 16);
  boxPaint(cv, R.jacket, (f, x, y, w, h) => { if (f !== 'top' && f !== 'bottom') { for (let i = 0; i < w; i++) cv.px(x + i, y + 9, plateD); for (let i = 0; i < w; i += 2) cv.px(x + i, y + 10, plate); } });
  for (const [reg, sl] of [[R.rarm, R.rsleeve], [R.larm, R.lsleeve]]) {
    all(cv, reg, under, 7);
    boxPaint(cv, reg, (f, x, y, w, h) => {
      if (f === 'top') { cv.rect(x, y, w, h, plate, 5); return; }
      if (f === 'bottom') { cv.rect(x, y, w, h, skin, 5); return; }
      cv.rect(x, y, w, 4, plate, 6); cv.rect(x, y + 3, w, 1, plateD, 4);
      cv.rect(x, y + 7, w, 4, greave, 6); cv.rect(x, y + 11, w, 1, skin, 4);
    });
    cv.clear(sl[0], sl[1], 16, 16);
    boxPaint(cv, sl, (f, x, y, w, h) => { if (f !== 'top' && f !== 'bottom') { cv.rect(x, y, w, 3, plate, 5); for (let i = 0; i < w; i += 2) cv.px(x + i, y + 1, lace); } });
  }
  for (const [reg, ov] of [[R.rleg, R.rpants], [R.lleg, R.lpants]]) {
    all(cv, reg, pants, 7, -8);
    boxPaint(cv, reg, (f, x, y, w, h) => {
      if (f === 'bottom') { cv.rect(x, y, w, h, hex('#2a2a2a'), 5); return; }
      if (f === 'top') return;
      cv.rect(x, y + 6, w, 5, greave, 6); for (let j = 6; j < 11; j += 2) cv.rect(x, y + j, w, 1, plateD, 3);
      cv.rect(x, y + 11, w, 1, hex('#2a2a2a'), 4);
    });
    cv.clear(ov[0], ov[1], 16, 16);
  }
  return cv;
}

function skinDrummer() {
  const cv = new Canvas(64, 64, 37);
  const red = hex('#b3262a'), redD = hex('#7d171c'), gold = hex('#e6b33c'), mane = hex('#e9e4dc'), black = hex('#18141a');
  const skin = hex('#b7805e'), coat = hex('#3b2552'), coatD = hex('#2a1a3b'), wave = hex('#d9d2e6'), rope = hex('#e8dccb'), ropeR = hex('#b8282c');
  // head: oni mask on the face, wild white mane
  all(cv, R.head, mane, 10);
  boxPaint(cv, R.head, (f, x, y, w, h) => {
    if (f === 'front') {
      cv.rect(x, y, w, h, red, 10, 10);
      cv.rect(x, y + 1, 3, 1, black); cv.rect(x + 5, y + 1, 3, 1, black); // brows
      cv.rect(x + 1, y + 2, 2, 2, gold, 6); cv.rect(x + 5, y + 2, 2, 2, gold, 6); cv.px(x + 2, y + 3, black); cv.px(x + 5, y + 3, black);
      cv.rect(x + 3, y + 4, 2, 1, redD); cv.rect(x + 1, y + 5, 6, 2, black); // nose, mouth
      cv.px(x + 1, y + 5, hex('#f4efe6')); cv.px(x + 6, y + 5, hex('#f4efe6')); cv.px(x + 2, y + 6, hex('#f4efe6')); cv.px(x + 5, y + 6, hex('#f4efe6'));
      cv.rect(x, y + 7, w, 1, redD, 6);
    }
    if (f === 'right' || f === 'left') { cv.rect(x + (f === 'right' ? 6 : 0), y + 1, 2, 6, red, 8); cv.px(x + (f === 'right' ? 7 : 0), y + 3, black); }
  });
  cv.clear(32, 0, 32, 16);
  boxPaint(cv, R.hat, (f, x, y, w, h) => { if (f === 'back' || f === 'right' || f === 'left') for (let i = 0; i < w; i++) cv.rect(x + i, y + 6, 1, 2 + ((i * 5) % 3), mane, 10); });
  // body: open purple happi coat, bare chest, red-white tasuki rope crossing
  all(cv, R.body, coat, 8, -10);
  boxPaint(cv, R.body, (f, x, y, w, h) => {
    if (f === 'front') { cv.rect(x + 2, y, 4, 9, skin, 8); cv.line(x, y, x + 7, y + 7, rope); cv.line(x + 7, y, x, y + 7, ropeR); cv.rect(x, y + 8, w, 2, hex('#d8d0c4'), 6); }
    if (f === 'back') { for (let i = 0; i < w; i++) cv.px(x + i, y + 4 + Math.round(Math.sin(i * 1.1) * 1.2), wave); cv.line(x, y, x + 7, y + 7, rope); }
    if (f === 'right' || f === 'left') { cv.px(x + 1, y + 5, wave); cv.px(x + 2, y + 6, wave); }
    if (f !== 'top' && f !== 'bottom') cv.rect(x, y + 10, w, 2, coatD, 5);
  });
  cv.clear(16, 32, 24, 16);
  for (const [reg, sl] of [[R.rarm, R.rsleeve], [R.larm, R.lsleeve]]) {
    all(cv, reg, skin, 8, -8);
    boxPaint(cv, reg, (f, x, y, w, h) => {
      if (f === 'top') { cv.rect(x, y, w, h, coat, 6); return; }
      if (f === 'bottom') return;
      cv.rect(x, y, w, 3, coat, 6); for (let i = 0; i < w; i++) cv.px(x + i, y + 3, coatD);
      cv.rect(x, y + 8, w, 2, rope, 6); cv.rect(x, y + 9, w, 1, ropeR, 4);
    });
    cv.clear(sl[0], sl[1], 16, 16);
  }
  for (const [reg, ov] of [[R.rleg, R.rpants], [R.lleg, R.lpants]]) {
    all(cv, reg, black, 7, -6);
    boxPaint(cv, reg, (f, x, y, w, h) => { if (f === 'bottom') { cv.rect(x, y, w, h, hex('#a88a50'), 8); return; } if (f !== 'top') cv.rect(x, y + 10, w, 2, mane, 6); });
    cv.clear(ov[0], ov[1], 16, 16);
  }
  return cv;
}

// ---------------------------------------------------------------- props sheet (64x64): 8x8 tiles + drum head + banner
const TILE = {straw: [0, 0], strawD: [1, 0], steel: [2, 0], steelB: [3, 0], steelD: [4, 0], wood: [5, 0], woodD: [6, 0], rope: [7, 0],
  lacq: [0, 1], navy: [1, 1], gold: [2, 1], white: [3, 1], redL: [4, 1], hide: [5, 1], ivory: [6, 1], grip: [7, 1],
  tassel: [0, 2], teal: [1, 2], purple: [2, 2], iron: [3, 2], mane: [4, 2], black: [5, 2], glow: [6, 2], bamboo: [7, 2]};
const tileUV = t => { const [i, j] = TILE[t]; return [i * 2, j * 2, i * 2 + 2, j * 2 + 2]; };
const DRUMHEAD = [0, 8, 4, 12], BANNER = [4, 8, 8, 16];
function props() {
  const cv = new Canvas(64, 64, 51);
  const T = (name, c, n = 10, g = 0, extra) => { const [i, j] = TILE[name]; cv.rect(i * 8, j * 8, 8, 8, c, n, g); if (extra) extra(i * 8, j * 8); };
  T('straw', hex('#cfae63'), 14, 0, (x, y) => { for (let j = 0; j < 8; j += 2) cv.line(x, y + j, x + 7, y + j, hex('#a8873f')); });
  T('strawD', hex('#9f7f3c'), 12);
  T('steel', hex('#b8c0c8'), 8, 20); T('steelB', hex('#eef3f7'), 5, 10); T('steelD', hex('#4a4f58'), 6);
  T('wood', hex('#7a4e2c'), 10, 0, (x, y) => { cv.line(x + 2, y, x + 2, y + 7, hex('#5f3b20')); cv.line(x + 5, y, x + 5, y + 7, hex('#8d5f38')); });
  T('woodD', hex('#3e2717'), 8);
  T('rope', hex('#d7c49a'), 10, 0, (x, y) => { for (let j = 0; j < 8; j++) cv.px(x + (j % 4) * 2, y + j, hex('#a8925f')); });
  T('lacq', hex('#1d1a22'), 5, 12); T('navy', hex('#1f3550'), 6, 12); T('gold', hex('#e3b23c'), 10, 18); T('white', hex('#ece8df'), 6);
  T('redL', hex('#a8242b'), 8, 16); T('hide', hex('#e4d6b4'), 8); T('ivory', hex('#efe6cf'), 6, -16);
  T('grip', hex('#22263a'), 4, 0, (x, y) => { for (let j = 0; j < 8; j++) { cv.px(x + (j % 4), y + j, hex('#d8d0bc')); cv.px(x + 7 - (j % 4), y + j, hex('#d8d0bc')); } });
  T('tassel', hex('#c4282f'), 12); T('teal', hex('#2f7d8a'), 6); T('purple', hex('#6a3f99'), 6); T('iron', hex('#2d2d33'), 5);
  T('mane', hex('#efe9df'), 10); T('black', hex('#141216'), 4); T('glow', hex('#fff4c2'), 3); T('bamboo', hex('#a99a5c'), 8, 0, (x, y) => { cv.rect(x, y + 3, 8, 1, hex('#7d7040'), 2); });
  // drum head 16x16 at (0,32): cream hide, iron studs ring, black mitsudomoe-like swirl (original three-comma whirl)
  cv.rect(0, 32, 16, 16, hex('#e8dcbc'), 6);
  for (let a = 0; a < 16; a++) { const t = a / 16 * Math.PI * 2; cv.px(Math.round(7.5 + Math.cos(t) * 7), Math.round(39.5 + Math.sin(t) * 7), hex('#2d2d33')); }
  for (let k = 0; k < 3; k++) for (let s = 0; s < 14; s++) {
    const t = k * 2.094 + s * 0.17, r = 1 + s * 0.33;
    cv.px(Math.round(7.5 + Math.cos(t) * r), Math.round(39.5 + Math.sin(t) * r), hex('#1a1416'));
    if (s > 8) cv.px(Math.round(7.5 + Math.cos(t + 0.15) * (r - 0.8)), Math.round(39.5 + Math.sin(t + 0.15) * (r - 0.8)), hex('#1a1416'));
  }
  // banner 16x32 at (16,32): violet field, white border, a white wave crest (original)
  cv.rect(16, 32, 16, 32, hex('#5b3a8e'), 6, -16);
  cv.rect(16, 32, 16, 1, hex('#efe9df'), 3); cv.rect(16, 32, 1, 32, hex('#efe9df'), 3);
  for (let i = 0; i < 12; i++) { const yy = 44 + Math.round(Math.sin(i * 0.7) * 2); cv.px(18 + i, yy, hex('#efe9df')); cv.px(18 + i, yy + 1, hex('#efe9df')); cv.px(18 + i, yy + 5, hex('#c7b8e6')); }
  for (let a = 0; a < 20; a++) { const t = a / 20 * Math.PI * 2; cv.px(Math.round(24 + Math.cos(t) * 3), Math.round(38 + Math.sin(t) * 3), hex('#efe9df')); }
  for (let j = 0; j < 4; j++) cv.px(17 + (j * 4 + 2) % 15, 58 + j, hex('#3b2560')); // frayed hem
  return cv;
}

// slime sheet 32x32: front (eyes), side, top, core
function slimeSheet() {
  const cv = new Canvas(32, 32, 71);
  const jelly = [150, 92, 235, 150], jellyD = [104, 54, 190, 170], rim = [214, 176, 255, 190];
  const face = (x0, y0, eyes) => {
    cv.rect(x0, y0, 16, 16, jelly, 10, 30);
    for (let i = 0; i < 16; i++) { cv.px(x0 + i, y0, rim); cv.px(x0, y0 + i, rim); cv.px(x0 + i, y0 + 15, jellyD); cv.px(x0 + 15, y0 + i, jellyD); }
    for (let k = 0; k < 5; k++) cv.px(x0 + 2 + ((k * 7) % 11), y0 + 3 + ((k * 5) % 9), [235, 220, 255, 210]);
    if (eyes) {
      cv.rect(x0 + 3, y0 + 5, 3, 4, [28, 10, 52, 255], 4); cv.rect(x0 + 10, y0 + 5, 3, 4, [28, 10, 52, 255], 4);
      cv.px(x0 + 4, y0 + 5, [255, 246, 160, 255]); cv.px(x0 + 11, y0 + 5, [255, 246, 160, 255]);
      cv.rect(x0 + 6, y0 + 11, 4, 1, [40, 14, 70, 255], 3); cv.px(x0 + 5, y0 + 10, [40, 14, 70, 255]); cv.px(x0 + 10, y0 + 10, [40, 14, 70, 255]);
    }
  };
  face(0, 0, true); face(16, 0, false); face(0, 16, false);
  // core: bright electro crystal with a jagged bolt
  cv.rect(16, 16, 16, 16, [222, 150, 255, 255], 10, -20);
  cv.line(23, 17, 20, 24, [255, 250, 210, 255]); cv.line(20, 24, 26, 23, [255, 250, 210, 255]); cv.line(26, 23, 22, 30, [255, 250, 210, 255]);
  return cv;
}
function ringSheet() {
  const cv = new Canvas(32, 32, 83);
  for (let y = 0; y < 32; y++) for (let x = 0; x < 32; x++) {
    const r = Math.hypot(x - 15.5, y - 15.5), d = Math.abs(r - 13.5);
    if (d < 1.6) cv.px(x, y, [196, 120, 255, cl(255 - d * 80)]);
    else if (r < 13 && (Math.round(Math.atan2(y - 15.5, x - 15.5) * 6 / Math.PI + r) % 4 === 0) && r > 9) cv.px(x, y, [235, 190, 255, 110]);
    else cv.px(x, y, [0, 0, 0, 0]);
  }
  return cv;
}

// ---------------------------------------------------------------- model helpers (same box UV as tools/build_swordsman.mjs)
function faces(u, v, w, h, d, tex = '#skin') {
  const face = (x1, y1, x2, y2) => ({uv: [x1 / 4, y1 / 4, x2 / 4, y2 / 4], texture: tex, tintindex: 0});
  return {east: face(u, v + d, u + d, v + d + h), north: face(u + d, v + d, u + d + w, v + d + h), west: face(u + d + w, v + d, u + 2 * d + w, v + d + h),
    south: face(u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h), up: face(u + d, v, u + d + w, v + d), down: face(u + d + w, v + d, u + d + 2 * w, v)};
}
const box = (from, to, uv, inflate = 0) => ({from: from.map(x => x - inflate), to: to.map(x => x + inflate), faces: faces(...uv)});
const r6 = v => Number(v.toFixed(4));
// solid box with one props tile on all faces; rot = {axis, angle, origin}
function solid(from, to, tile, rot, uvOverride) {
  const uv = uvOverride || tileUV(tile);
  const e = {from: from.map(r6), to: to.map(r6), faces: Object.fromEntries(['north', 'south', 'east', 'west', 'up', 'down'].map(f => [f, {texture: '#props', uv, tintindex: 0}]))};
  if (rot) e.rotation = rot;
  return e;
}
const SHAPES = {
  head: {from: [4, 8, 4], to: [12, 16, 12], uv: [0, 0, 8, 8, 8], over: [32, 0, 8, 8, 8], inflate: .5},
  body: {from: [4, -4, 6], to: [12, 8, 10], uv: [16, 16, 8, 12, 4], over: [16, 32, 8, 12, 4], inflate: .25},
  right_arm: {from: [6, -2, 6], to: [10, 10, 10], uv: [40, 16, 4, 12, 4], over: [40, 32, 4, 12, 4], inflate: .25},
  left_arm: {from: [6, -2, 6], to: [10, 10, 10], uv: [32, 48, 4, 12, 4], over: [48, 48, 4, 12, 4], inflate: .25},
  right_leg: {from: [6, -4, 6], to: [10, 8, 10], uv: [0, 16, 4, 12, 4], over: [0, 32, 4, 12, 4], inflate: .25},
  left_leg: {from: [6, -4, 6], to: [10, 8, 10], uv: [16, 48, 4, 12, 4], over: [0, 48, 4, 12, 4], inflate: .25}
};
const written = [];
function model(mob, part, textures, elements) {
  const id = `cm/c2/${mob}/${part}`;
  json(path.join(rp, 'models/item', id + '.json'), {ambientocclusion: false, textures: {...textures, particle: Object.values(textures)[0]}, elements});
  json(path.join(rp, 'items', id + '.json'), {model: {type: 'minecraft:model', model: 'rlk:item/' + id, tints: [{type: 'minecraft:custom_model_data', index: 0, default: 16777215}]}});
  written.push(id);
}
const PROPS = 'rlk:cm/c2/props';
function humanoid(mob, extra) {
  for (const [name, s] of Object.entries(SHAPES)) {
    const els = [box(s.from, s.to, s.uv), box(s.from, s.to, s.over, s.inflate)];
    for (const e of (extra[name] || [])) els.push(e);
    model(mob, name, {skin: `rlk:skin/mob_c2_${mob}`, props: PROPS}, els);
  }
}

// ns: straw kasa (wide shallow cone) on the head
humanoid('ns', {head: [
  solid([-1.5, 15.6, -1.5], [17.5, 16.4, 17.5], 'straw'), solid([1, 16.4, 1], [15, 17.3, 15], 'straw'), solid([3.5, 17.3, 3.5], [12.5, 18.2, 12.5], 'strawD'),
  solid([6, 18.2, 6], [10, 18.9, 10], 'straw'), solid([7.4, 18.9, 7.4], [8.6, 19.4, 8.6], 'strawD'),
  solid([7.6, 10, 11.8], [8.4, 15.6, 12.4], 'rope') // chin cord at the back
]});
// katana: wrapped grip, round-ish tsuba, gently curved blade (three offset segments) along +Y
model('ns', 'katana', {props: PROPS}, [
  solid([7.45, 3.6, 7.45], [8.55, 9.8, 8.55], 'grip'), solid([7.3, 3.2, 7.3], [8.7, 3.7, 8.7], 'gold'),
  solid([6.3, 9.8, 7.1], [9.7, 10.4, 8.9], 'lacq'), solid([7.1, 9.8, 6.3], [8.9, 10.4, 9.7], 'lacq'), solid([7.5, 10.4, 7.35], [8.5, 11, 8.65], 'gold'),
  solid([7.65, 11, 7.4], [8.35, 16.5, 8.6], 'steel'), solid([7.65, 16.5, 7.55], [8.35, 22, 8.8], 'steel'), solid([7.65, 22, 7.75], [8.35, 26, 8.95], 'steel'),
  solid([7.7, 26, 8.0], [8.3, 27.2, 8.85], 'steelB'), solid([7.62, 11, 8.6], [8.38, 26, 8.68], 'steelB')
]);
// sp: lacquered jingasa with a gold crest
humanoid('sp', {head: [
  solid([-1, 15.6, -1], [17, 16.2, 17], 'navy'), solid([1.5, 16.2, 1.5], [14.5, 17, 14.5], 'navy'), solid([4.5, 17, 4.5], [11.5, 17.7, 11.5], 'lacq'),
  solid([7, 17.7, 7], [9, 18.3, 9], 'gold'), solid([7.6, 8.5, 3.2], [8.4, 15.6, 3.6], 'gold')
]});
// yari along +Y: long shaft, collar, leaf blade, red tassel
model('sp', 'yari', {props: PROPS}, [
  solid([7.5, -15, 7.5], [8.5, 25, 8.5], 'wood'), solid([7.3, -15.8, 7.3], [8.7, -14.6, 8.7], 'iron'),
  solid([7.2, 24.6, 7.2], [8.8, 26, 8.8], 'iron'), solid([8.6, 22, 7.7], [9.6, 24.6, 8.3], 'tassel'), solid([6.4, 22.4, 7.7], [7.4, 24.6, 8.3], 'tassel'),
  solid([7.75, 26, 7.25], [8.25, 30, 8.75], 'steel'), solid([7.8, 30, 7.55], [8.2, 31.4, 8.45], 'steelB'), solid([7.85, 31.4, 7.8], [8.15, 32, 8.2], 'steelB')
]);
// sashimono: bamboo pole on the back and a tall violet banner
model('sp', 'flag', {props: PROPS}, [
  solid([7.6, -6, 7.6], [8.4, 31, 8.4], 'bamboo'), solid([8.4, 30, 7.7], [15.6, 30.6, 8.3], 'bamboo'),
  {from: [8.4, 12, 7.9], to: [15.8, 30, 8.1], faces: Object.fromEntries(['north', 'south', 'east', 'west', 'up', 'down'].map(f => [f, {texture: '#props', uv: BANNER, tintindex: 0}]))}
]);
// dr: oni horns, fangs, mane on the head
humanoid('dr', {head: [
  solid([4.6, 15.5, 6.8], [6.2, 19.5, 8.4], 'ivory', {axis: 'z', angle: 22.5, origin: [5.4, 15.5, 7.6]}),
  solid([9.8, 15.5, 6.8], [11.4, 19.5, 8.4], 'ivory', {axis: 'z', angle: -22.5, origin: [10.6, 15.5, 7.6]}),
  solid([5.2, 9.0, 3.1], [6.0, 10.4, 3.6], 'ivory'), solid([10.0, 9.0, 3.1], [10.8, 10.4, 3.6], 'ivory'),
  solid([3.4, 9, 11.6], [12.6, 16.8, 13.4], 'mane')
]});
model('dr', 'stick_r', {props: PROPS}, [solid([7.4, 2, 7.4], [8.6, 17, 8.6], 'wood'), solid([7.3, 16, 7.3], [8.7, 17.4, 8.7], 'woodD')]);
model('dr', 'stick_l', {props: PROPS}, [solid([7.4, 2, 7.4], [8.6, 17, 8.6], 'wood'), solid([7.3, 16, 7.3], [8.7, 17.4, 8.7], 'woodD')]);
// taiko: barrel (red lacquer, gold bands), two hide heads facing +-Z, wooden stand. Model centre [8,8,8] = drum centre.
const head = (z0, z1) => ({from: [1.2, 1.2, z0], to: [14.8, 14.8, z1], faces: Object.fromEntries(['north', 'south', 'east', 'west', 'up', 'down'].map(f => [f, {texture: '#props', uv: (f === 'north' || f === 'south') ? DRUMHEAD : tileUV('hide'), tintindex: 0}]))});
model('dr', 'taiko', {props: PROPS}, [
  solid([0.4, 2.4, 2.2], [15.6, 13.6, 13.8], 'redL'), solid([2.4, 0.4, 2.2], [13.6, 15.6, 13.8], 'redL'),
  solid([0, 3.6, 3.2], [16, 12.4, 12.8], 'redL'), solid([3.6, 0, 3.2], [12.4, 16, 12.8], 'redL'),
  solid([0.2, 2.2, 7.4], [15.8, 13.8, 8.6], 'gold'), solid([2.2, 0.2, 7.4], [13.8, 15.8, 8.6], 'gold'),
  head(1.6, 2.2), head(13.8, 14.4),
  solid([-1.2, -7, 6.8], [0.6, 6, 9.2], 'woodD'), solid([15.4, -7, 6.8], [17.2, 6, 9.2], 'woodD'), solid([-1.2, -5.5, 7.2], [17.2, -4.3, 8.8], 'woodD')
]);
// slime: translucent jelly cube with face + inner electro core; the decal ring
const SLIME = 'rlk:cm/c2/slime';
const sf = {north: [0, 0, 8, 8], south: [8, 0, 16, 8], east: [8, 0, 16, 8], west: [8, 0, 16, 8], up: [0, 8, 8, 16], down: [8, 0, 16, 8]};
model('slime', 'body', {slime: SLIME}, [{from: [1, 0, 1], to: [15, 14, 15], faces: Object.fromEntries(Object.entries(sf).map(([f, uv]) => [f, {texture: '#slime', uv, tintindex: 0}]))}]);
model('slime', 'core', {slime: SLIME}, [{from: [5, 3, 5], to: [11, 9, 11], faces: Object.fromEntries(['north', 'south', 'east', 'west', 'up', 'down'].map(f => [f, {texture: '#slime', uv: [8, 8, 16, 16], tintindex: 0}]))}]);
model('fx', 'ring', {ring: 'rlk:cm/c2/ring'}, [{from: [0, 7.9, 0], to: [16, 8.1, 16], faces: {up: {texture: '#ring', uv: [0, 0, 16, 16], tintindex: 0}, down: {texture: '#ring', uv: [0, 16, 16, 0], tintindex: 0}}}]);

// ---------------------------------------------------------------- textures + atlas
const tex = {'skin/mob_c2_ns': skinRonin(), 'skin/mob_c2_sp': skinSpear(), 'skin/mob_c2_dr': skinDrummer(), 'cm/c2/props': props(), 'cm/c2/slime': slimeSheet(), 'cm/c2/ring': ringSheet()};
let px = 0;
for (const [id, cv] of Object.entries(tex)) { put(path.join(rp, 'textures', id + '.png'), cv.png()); px += cv.w * cv.h; }
const atlasPath = path.join(rpRoot, 'assets/minecraft/atlases/items.json');
const atlas = fs.existsSync(atlasPath) ? JSON.parse(fs.readFileSync(atlasPath, 'utf8')) : {sources: []};
for (const id of Object.keys(tex)) {
  const resource = 'rlk:' + id;
  atlas.sources = atlas.sources.filter(s => (s.sprite || s.resource) !== resource);
  atlas.sources.push({type: 'minecraft:single', resource});
}
json(atlasPath, atlas);
console.log(JSON.stringify({models: written.length, textures: Object.keys(tex).length, texturePixels: px}));
