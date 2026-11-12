// Chapter-2 elite rigs (part B): 카이라기·뇌전 (kr), 그림자 닌자 (nj), 우인단 번개 시킨 술사 (cc), 번개 시킨 (ci).
// Original geometry, skins and keyframes authored for roguelike (Inazuma look); nothing is copied from a reference pack.
//
//   node tools/build_ch2_elite_rigs.mjs --resourcepack <unpacked resource pack>
//
// Writes (all owned by this generator):
//   RP  assets/rlk/textures/skin/mob_{kr,nj,cc}.png     64x64 painted skins
//       assets/rlk/textures/cm/c2e/pal.png               16x16 palette (16 swatches of 4x4)
//       assets/rlk/models/item/cm/{kr,nj,cc,ci}/*.json   part models (pivot [8,8,8])
//       assets/rlk/items/cm/{kr,nj,cc,ci}/*.json         item definitions (custom_model_data tint 0 = hurt flash)
//       assets/minecraft/atlases/items.json              our 4 sprites, filter-then-push by id (idempotent)
//   DP  tools/ch2_elite_poses.json                       runtime transforms of every pose; ch2mob/elite.py turns them into
//                                                        the rig/pose/<id> functions (functions are written by python only)
// Every pose is checked: no part's geometry may reach below the feet plane (throws otherwise).
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {png, hex, mix, noise2} from './weapon_paint.mjs';

const base = path.dirname(fileURLToPath(import.meta.url));
const arg = n => { const i = process.argv.indexOf(n); return i < 0 ? undefined : process.argv[i + 1]; };
if (!arg('--resourcepack')) throw Error('Provide --resourcepack <unpacked resource pack>.');
const rpRoot = path.resolve(arg('--resourcepack'));
if (!fs.existsSync(path.join(rpRoot, 'pack.mcmeta'))) throw Error('resource pack must contain pack.mcmeta');
const rp = path.join(rpRoot, 'assets/rlk');
const put = (p, s) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, s); };
const json = (p, o) => put(p, JSON.stringify(o, null, 2) + '\n');

// ------------------------------------------------------------------ palette (16 swatches, 4x4 px each)
const PAL = ['#20212c', '#7b4bc4', '#d4ad55', '#c9ced8', '#6d7380', '#b77dff', '#f2e2ff', '#3a2350',
  '#121216', '#7a2a24', '#eceae4', '#d8d2c8', '#4a3324', '#8f5ad8', '#4a2a78', '#2b1846'];
const SW = {lacquer: 0, trim: 1, gold: 2, steel: 3, steeld: 4, glow: 5, core: 6, wrap: 7, black: 8, cord: 9,
  white: 10, fur: 11, wood: 12, glow2: 13, wing: 14, wingd: 15};
{
  const buf = Buffer.alloc(16 * 16 * 4);
  for (let y = 0; y < 16; y++) for (let x = 0; x < 16; x++) {
    const k = (y >> 2) * 4 + (x >> 2), c = hex(PAL[k]);
    // a faint 1 px bevel keeps flat boxes from reading as plastic
    const edge = (x & 3) === 0 || (y & 3) === 0 ? 0.92 : (x & 3) === 3 || (y & 3) === 3 ? 0.86 : 1;
    const g = k === SW.glow || k === SW.core || k === SW.glow2 ? 1 : edge;
    const o = (y * 16 + x) * 4;
    buf[o] = Math.round(c[0] * g); buf[o + 1] = Math.round(c[1] * g); buf[o + 2] = Math.round(c[2] * g); buf[o + 3] = 255;
  }
  put(path.join(rp, 'textures/cm/c2e/pal.png'), png(16, 16, buf));
}
const swUV = k => { const x = (k % 4) * 4, y = Math.floor(k / 4) * 4; return [x + .5, y + .5, x + 3.5, y + 3.5]; };
const solid = (from, to, sw, tint = true) => ({from, to, faces: Object.fromEntries(['north', 'south', 'east', 'west', 'up', 'down']
  .map(f => [f, {texture: '#pal', uv: swUV(SW[sw]), ...(tint ? {tintindex: 0} : {})}]))});

// ------------------------------------------------------------------ skins (64x64, standard player layout)
const L = {head: [0, 0, 8, 8, 8], hat: [32, 0, 8, 8, 8], body: [16, 16, 8, 12, 4], jacket: [16, 32, 8, 12, 4],
  rarm: [40, 16, 4, 12, 4], rsleeve: [40, 32, 4, 12, 4], larm: [32, 48, 4, 12, 4], lsleeve: [48, 48, 4, 12, 4],
  rleg: [0, 16, 4, 12, 4], rpants: [0, 32, 4, 12, 4], lleg: [16, 48, 4, 12, 4], lpants: [0, 48, 4, 12, 4]};
function faceRects(u, v, w, h, d) {
  return {top: [u + d, v, w, d], bottom: [u + d + w, v, w, d], right: [u, v + d, d, h], front: [u + d, v + d, w, h],
    left: [u + d + w, v + d, d, h], back: [u + 2 * d + w, v + d, w, h]};
}
function skin(painter) {
  const buf = Buffer.alloc(64 * 64 * 4);
  for (const [reg, box] of Object.entries(L)) for (const [face, [x0, y0, w, h]] of Object.entries(faceRects(...box)))
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const c = painter(reg, face, x, y, w, h);
      if (!c) continue;
      const o = ((y0 + y) * 64 + x0 + x) * 4;
      buf[o] = Math.round(c[0]); buf[o + 1] = Math.round(c[1]); buf[o + 2] = Math.round(c[2]); buf[o + 3] = c[3] ?? 255;
    }
  return buf;
}
const shade = (c, k) => [c[0] * k, c[1] * k, c[2] * k, 255];
const N = noise2(7);
const grain = (c, x, y, s = 0.08) => shade(c, 1 - s / 2 + s * N(x * 1.7, y * 1.7));
const base_ = reg => reg.replace(/hat|jacket|sleeve|pants/, '');

// 카이라기·뇌전: lacquered dark armour in bands, purple lacing, dark oni mask with glowing violet eyes and gold fangs.
function paintKr(reg, face, x, y, w, h) {
  const lac = hex('#22232f'), lac2 = hex('#2f3142'), trim = hex('#7b4bc4'), gold = hex('#d4ad55'), cord = hex('#7a2a24');
  const hak = hex('#2b2233'), blk = hex('#141418'), eye = hex('#d9a8ff');
  if (reg === 'head') {
    if (face !== 'front') return grain(face === 'top' ? lac : blk, x, y);
    if (y >= 3 && y <= 4 && (x === 1 || x === 2 || x === 5 || x === 6)) return y === 3 ? eye : hex('#9a5fe0');
    if (y === 2 && (x === 1 || x === 6)) return trim;                         // angry brow ridges
    if (y === 6 && x >= 2 && x <= 5) return x % 2 ? gold : hex('#a8873a');      // fangs
    if (y === 7 && x >= 1 && x <= 6) return hex('#3b1e24');
    return grain(hex('#2d1f30'), x, y, .14);                                    // oni mask lacquer
  }
  if (reg === 'hat') {
    if (face === 'front') return y === 0 ? gold : null;                         // brow plate rim
    if (face === 'top' || face === 'back' || face === 'right' || face === 'left') return y < 2 || face === 'top' ? grain(lac2, x, y) : null;
    return null;
  }
  if (reg === 'body') {
    if (y >= 8 && y <= 9) return y === 8 ? cord : shade(cord, .8);              // rope belt
    const band = (y >> 1) % 2 ? lac : lac2;
    if (face === 'front' && (x === 3 || x === 4) && y < 8 && y % 2 === 0) return trim; // lacing
    if (y >= 10) return grain(hak, x, y);
    return grain(band, x, y);
  }
  if (reg === 'rarm' || reg === 'larm') {
    if (y >= 10) return blk;                                                    // gloves
    if (y % 3 === 2) return trim;
    return grain((y >> 1) % 2 ? lac : lac2, x, y);
  }
  if (reg === 'rleg' || reg === 'lleg') {
    if (y >= 10) return blk;
    if (face === 'front' && y >= 1 && y <= 6) return grain(y % 2 ? lac2 : lac, x, y);
    return grain(hak, x, y, .12);
  }
  return null;
}
// 그림자 닌자: black gi with grey wrap bands, a purple sash, a skin-tone eye strip in a black hood.
function paintNj(reg, face, x, y, w, h) {
  const blk = hex('#16161b'), gry = hex('#2b2b34'), sash = hex('#5b3a8c'), skinc = hex('#d9b08e'), eye = hex('#2a1838');
  if (reg === 'head') {
    if (face === 'front' && y >= 3 && y <= 4 && x >= 1 && x <= 6) {
      if (y === 4 && (x === 2 || x === 5)) return eye;
      return skinc;
    }
    return grain(blk, x, y, .1);
  }
  if (reg === 'hat') {
    if (face === 'back' && y >= 2 && y <= 3) return sash;                       // headband
    if ((face === 'right' || face === 'left') && y >= 2 && y <= 3) return sash;
    if (face === 'front' && y === 2) return sash;
    return null;
  }
  if (reg === 'body') {
    if (y >= 8 && y <= 9) return y === 8 ? sash : shade(sash, .75);
    if (face === 'front' && Math.abs((x - 0) - (y - 0)) <= 0 && y < 8) return gry;  // crossed wrap
    if (face === 'front' && Math.abs((7 - x) - y) <= 0 && y < 8) return gry;
    return grain(blk, x, y, .1);
  }
  if (reg === 'rarm' || reg === 'larm') return (y === 4 || y === 7 || y === 9) ? gry : grain(blk, x, y, .1);
  if (reg === 'rleg' || reg === 'lleg') return (y >= 6 && y <= 10 && y % 2 === 0) ? gry : grain(blk, x, y, .1);
  return null;
}
// 우인단 번개 시킨 술사: violet coat, white fur trim, gold centre line, hood; the Fatui mask is geometry on the head model.
function paintCc(reg, face, x, y, w, h) {
  const vio = hex('#5a3a82'), vio2 = hex('#47306a'), fur = hex('#e2dbd0'), gold = hex('#c9a24a'), blk = hex('#1c1622'), skinc = hex('#e6c7aa');
  if (reg === 'head') {
    if (face === 'front') return y < 2 ? vio2 : skinc;                          // hood rim over the mask
    return grain(vio2, x, y, .12);
  }
  if (reg === 'hat') return face === 'front' ? null : (face === 'bottom' ? null : grain(vio, x, y, .1));
  if (reg === 'body') {
    if (y <= 1) return grain(fur, x, y, .1);
    if (face === 'front' && (x === 3 || x === 4)) return y % 3 === 0 ? gold : shade(gold, .85);
    if (y >= 8 && y <= 8) return blk;
    return grain(y > 8 ? vio2 : vio, x, y, .1);
  }
  if (reg === 'rarm' || reg === 'larm') {
    if (y >= 9 && y <= 10) return grain(fur, x, y, .1);
    if (y === 11) return skinc;
    return grain(vio, x, y, .1);
  }
  if (reg === 'rleg' || reg === 'lleg') {
    if (y >= 11) return blk;
    if (face === 'front' && y === 0) return gold;
    return grain(vio2, x, y, .1);
  }
  return null;
}
for (const [id, p] of [['kr', paintKr], ['nj', paintNj], ['cc', paintCc]])
  put(path.join(rp, `textures/skin/mob_${id}.png`), png(64, 64, skin(p)));

// ------------------------------------------------------------------ models
function faces(u, v, w, h, d) {
  const face = (x1, y1, x2, y2) => ({uv: [x1 / 4, y1 / 4, x2 / 4, y2 / 4], texture: '#skin', tintindex: 0});
  return {east: face(u, v + d, u + d, v + d + h), north: face(u + d, v + d, u + d + w, v + d + h), west: face(u + d + w, v + d, u + 2 * d + w, v + d + h),
    south: face(u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h), up: face(u + d, v, u + d + w, v + d), down: face(u + d + w, v + d, u + d + 2 * w, v)};
}
const box = (from, to, uv, i = 0) => ({from: from.map(v => v - i), to: to.map(v => v + i), faces: faces(...uv)});
const HUM = {
  head: {from: [4, 8, 4], to: [12, 16, 12], uv: [0, 0, 8, 8, 8], over: [32, 0, 8, 8, 8], inflate: .5},
  body: {from: [4, -4, 6], to: [12, 8, 10], uv: [16, 16, 8, 12, 4], over: [16, 32, 8, 12, 4], inflate: .25},
  right_arm: {from: [6, -2, 6], to: [10, 10, 10], uv: [40, 16, 4, 12, 4], over: [40, 32, 4, 12, 4], inflate: .25},
  left_arm: {from: [6, -2, 6], to: [10, 10, 10], uv: [32, 48, 4, 12, 4], over: [48, 48, 4, 12, 4], inflate: .25},
  right_leg: {from: [6, -4, 6], to: [10, 8, 10], uv: [0, 16, 4, 12, 4], over: [0, 32, 4, 12, 4], inflate: .25},
  left_leg: {from: [6, -4, 6], to: [10, 8, 10], uv: [16, 48, 4, 12, 4], over: [0, 48, 4, 12, 4], inflate: .25},
};
const EXTRA = {
  kr: {
    head: [solid([5, 15, 3], [6, 19.5, 4], 'gold'), solid([10, 15, 3], [11, 19.5, 4], 'gold'), solid([4.2, 18.5, 3], [6, 19.5, 4], 'gold'),
      solid([10, 18.5, 3], [11.8, 19.5, 4], 'gold'), solid([7.2, 15.2, 2.9], [8.8, 16.6, 3.6], 'glow'),
      solid([3.4, 15.6, 3.4], [12.6, 17, 12.6], 'lacquer'), solid([2.6, 8.6, 4], [3.5, 13.5, 13.2], 'lacquer'),
      solid([12.5, 8.6, 4], [13.4, 13.5, 13.2], 'lacquer'), solid([3, 8.6, 12.5], [13, 13.5, 13.4], 'lacquer'),
      solid([2.5, 8.4, 3.9], [13.5, 9, 13.5], 'trim')],
    body: [solid([3.4, -7, 5.4], [12.6, -2.5, 10.6], 'lacquer'), solid([3.3, -7.3, 5.3], [12.7, -6.6, 10.7], 'trim'),
      solid([7.4, -2.6, 5.2], [8.6, -6.6, 5.5], 'cord')],
    right_arm: [solid([4.8, 5, 4.8], [11.2, 10.6, 11.2], 'lacquer'), solid([4.7, 4.6, 4.7], [11.3, 5.2, 11.3], 'trim')],
    left_arm: [solid([4.8, 5, 4.8], [11.2, 10.6, 11.2], 'lacquer'), solid([4.7, 4.6, 4.7], [11.3, 5.2, 11.3], 'trim')],
  },
  nj: {
    head: [solid([5.5, 13, 3.5], [10.5, 14, 4.1], 'steeld'), solid([6.6, 9.6, 12], [7.6, 10.4, 17], 'trim'), solid([8.4, 9.2, 12], [9.4, 10, 16], 'trim')],
    body: [solid([5, 4, 10], [7, 6.5, 14.5], 'wrap'), solid([9, 3, 10], [11, 5.5, 13.5], 'wrap')],
  },
  cc: {
    head: [solid([4.4, 9, 3.2], [11.6, 14.6, 3.8], 'white'), solid([5.4, 11.4, 3], [7.4, 12.3, 3.3], 'black'),
      solid([8.6, 11.4, 3], [10.6, 12.3, 3.3], 'black'), solid([4.4, 14.2, 3], [11.6, 14.8, 3.6], 'gold'),
      solid([7.6, 9.4, 3], [8.4, 11, 3.25], 'gold'), solid([3.4, 15.6, 3.4], [12.6, 17, 13.4], 'wrap'),
      solid([3.3, 8.5, 3.4], [4, 16, 13.2], 'wrap'), solid([12, 8.5, 3.4], [12.7, 16, 13.2], 'wrap'), solid([3.4, 8.5, 12.4], [12.6, 16, 13.4], 'wrap')],
    body: [solid([3, 6, 5], [13, 8.8, 11], 'fur'), solid([3.5, -9, 5.5], [12.5, -3.5, 10.5], 'wrap'), solid([7.5, -9, 5.3], [8.5, -3.5, 5.6], 'gold')],
  },
};
const WEAPON = {
  kr: [solid([7.2, 2.4, 7.2], [8.8, 3, 8.8], 'gold'), solid([7.4, 3, 7.4], [8.6, 9.5, 8.6], 'wrap'), solid([6, 9.5, 6], [10, 10.3, 10], 'gold'),
    solid([7.6, 10.3, 7.3], [8.4, 27, 8.6], 'steel'), solid([7.65, 10.3, 8.55], [8.35, 26.6, 8.8], 'glow2'), solid([7.7, 27, 7.5], [8.3, 28.2, 8.4], 'steel')],
  nj: [solid([7.4, 4.5, 7.4], [8.6, 9, 8.6], 'black'), solid([6.5, 9, 6.5], [9.5, 9.6, 9.5], 'steeld'), solid([7.6, 9.6, 7.4], [8.4, 20, 8.6], 'steel'),
    solid([7.75, 20, 7.6], [8.25, 21.2, 8.4], 'steel')],
  cc: [solid([7.5, -6, 7.5], [8.5, 22, 8.5], 'wood'), solid([6.6, 21.6, 6.6], [9.4, 22.6, 9.4], 'gold'), solid([6.2, 22.6, 6.2], [6.8, 27, 6.8], 'gold'),
    solid([9.2, 22.6, 6.2], [9.8, 27, 6.8], 'gold'), solid([6.2, 22.6, 9.2], [6.8, 27, 9.8], 'gold'), solid([9.2, 22.6, 9.2], [9.8, 27, 9.8], 'gold'),
    solid([6.2, 26.6, 6.2], [9.8, 27.4, 9.8], 'gold'), solid([7, 23.2, 7], [9, 26, 9], 'glow', false), solid([7.6, 27.4, 7.6], [8.4, 28.4, 8.4], 'gold')],
};
// glow overlays (no tint: they stay bright during the red hurt flash)
const GLOW = {
  kr_aura: [solid([7.05, 10.2, 6.9], [8.95, 28.6, 9.1], 'glow', false), solid([7.35, 10.2, 7.2], [8.65, 28.9, 8.8], 'core', false)],
  nj_glint: [solid([7.25, 9.6, 7.1], [8.75, 21.6, 8.9], 'core', false)],
  cc_flare: [solid([6.4, 22.8, 6.4], [9.6, 26.8, 9.6], 'core', false), solid([7.3, 26.8, 7.3], [8.7, 29, 8.7], 'glow', false)],
};
const MODELS = {};
function model(id, part, textures, elements) {
  MODELS[`${id}/${part}`] = elements;
  json(path.join(rp, `models/item/cm/${id}/${part}.json`), {ambientocclusion: false, textures: {...textures, particle: textures.skin || textures.pal}, elements});
  const tint = elements.some(e => Object.values(e.faces).some(f => f.tintindex === 0));
  json(path.join(rp, `items/cm/${id}/${part}.json`), {model: {type: 'minecraft:model', model: `rlk:item/cm/${id}/${part}`,
    ...(tint ? {tints: [{type: 'minecraft:custom_model_data', index: 0, default: 16777215}]} : {})}});
}
for (const id of ['kr', 'nj', 'cc']) {
  const tex = {skin: `rlk:skin/mob_${id}`, pal: 'rlk:cm/c2e/pal'};
  for (const [name, s] of Object.entries(HUM))
    model(id, name, tex, [box(s.from, s.to, s.uv), box(s.from, s.to, s.over, s.inflate), ...((EXTRA[id] || {})[name] || [])]);
  model(id, 'weapon', {pal: 'rlk:cm/c2e/pal'}, WEAPON[id]);
}
model('kr', 'aura', {pal: 'rlk:cm/c2e/pal'}, GLOW.kr_aura);
model('nj', 'glint', {pal: 'rlk:cm/c2e/pal'}, GLOW.nj_glint);
model('cc', 'flare', {pal: 'rlk:cm/c2e/pal'}, GLOW.cc_flare);
// shuriken: a flat four-point star in the XZ plane
model('nj', 'shuriken', {pal: 'rlk:cm/c2e/pal'}, [solid([2, 7.7, 7.1], [14, 8.3, 8.9], 'steel', false), solid([7.1, 7.7, 2], [8.9, 8.3, 14], 'steel', false),
  solid([6.4, 7.6, 6.4], [9.6, 8.4, 9.6], 'steeld', false), solid([7.6, 7.5, 7.6], [8.4, 8.5, 8.4], 'trim', false)]);
// 번개 시킨: one display; the wing beat is a model swap (frames with the wings turned about the body axis), so a cicin
// costs a single entity. Element rotations stay on the vanilla-safe 22.5 / 45 degree steps.
const CI_CORE = [solid([6, 6, 6], [10, 10, 10], 'glow', false), solid([6.7, 6.7, 5.6], [9.3, 9.3, 10.4], 'core', false),
  solid([6, 10, 7.4], [7.1, 11.8, 8.6], 'wingd', false), solid([8.9, 10, 7.4], [10, 11.8, 8.6], 'wingd', false),
  solid([7.5, 4.6, 9], [8.5, 6.2, 11.6], 'wing', false), solid([6.9, 8.2, 5.5], [7.5, 8.8, 5.7], 'wingd', false), solid([8.5, 8.2, 5.5], [9.1, 8.8, 5.7], 'wingd', false)];
const rotEl = (e, axis, angle) => angle ? {...e, rotation: {origin: [8, 8.5, 8], axis, angle}} : e;
function ciFrame(name, zAng, yAng = 0, span = 1) {
  const L1 = [solid([10, 7.2, 7.6], [10 + 5.5 * span, 9.8, 8.4], 'wing', false), solid([9 + 5.5 * span, 8.4, 7.7], [12.3 + 5.5 * span, 11, 8.3], 'wingd', false),
    solid([10.5, 6.4, 7.7], [10 + 4 * span, 7.2, 8.3], 'glow2', false)];
  const R1 = L1.map(e => ({...e, from: [16 - e.to[0], e.from[1], e.from[2]], to: [16 - e.from[0], e.to[1], e.to[2]]}));
  const axis = yAng ? 'y' : 'z', aL = yAng ? -yAng : zAng, aR = yAng ? yAng : -zAng;
  model('ci', name, {pal: 'rlk:cm/c2e/pal'}, [...CI_CORE, ...L1.map(e => rotEl(e, axis, aL)), ...R1.map(e => rotEl(e, axis, aR))]);
}
ciFrame('f_up', 45); ciFrame('f_down', -22.5); ciFrame('f_tell', 0, 0, 1.25); ciFrame('f_ram', 0, 45);

// atlas: our four sprites, filter-then-push by id
{
  const atlasPath = path.join(rpRoot, 'assets/minecraft/atlases/items.json');
  const atlas = fs.existsSync(atlasPath) ? JSON.parse(fs.readFileSync(atlasPath, 'utf8')) : {sources: []};
  for (const res of ['rlk:skin/mob_kr', 'rlk:skin/mob_nj', 'rlk:skin/mob_cc', 'rlk:cm/c2e/pal']) {
    atlas.sources = atlas.sources.filter(s => (s.sprite || s.resource) !== res);
    atlas.sources.push({type: 'minecraft:single', resource: res});
  }
  json(atlasPath, atlas);
}

// ------------------------------------------------------------------ pose math (same conventions as build_swordsman.mjs)
// Authored with -Z forward, right hand on -X; converted with F = diag(1,1,-1) for item_display (which turns geometry Y180).
const rad = x => x * Math.PI / 180;
function mul(a, b) { const [x, y, z, w] = a, [X, Y, Z, W] = b; return [w * X + x * W + y * Z - z * Y, w * Y - x * Z + y * W + z * X, w * Z + x * Y - y * X + z * W, w * W - x * X - y * Y - z * Z]; }
function q(e = [0, 0, 0]) { const [x, y, z] = e.map(a => rad(a) / 2); return mul(mul([0, 0, Math.sin(z), Math.cos(z)], [0, Math.sin(y), 0, Math.cos(y)]), [Math.sin(x), 0, 0, Math.cos(x)]); }
function rot(a, v) { return mul(mul(a, [...v, 0]), [-a[0], -a[1], -a[2], a[3]]).slice(0, 3); }
const add = (a, b) => a.map((v, i) => v + b[i]);
const HUMAN_PARTS = ['head', 'body', 'right_arm', 'left_arm', 'right_leg', 'left_leg', 'weapon'];

function humanoid(cfg, over) {
  const p = {...cfg.base, ...over};
  const hip = add([0, .75, 0], p.shift || [0, 0, 0]);
  const t = q(p.torso), root = q(p.root || [0, 0, 0]);
  const r = {};
  const shoulder = add(hip, rot(t, [0, .75, 0]));
  r.body = {t: shoulder, q: t};
  r.head = {t: shoulder, q: mul(t, q(p.head))};
  for (const [name, sign] of [['right_arm', -1], ['left_arm', 1]]) {
    const joint = mul(q([0, name === 'right_arm' ? (cfg.armOpen ?? 0) : 0, 0]), q(p[name]));
    r[name] = {t: add(hip, rot(t, [sign * .375, .625, 0])), q: mul(t, joint)};
  }
  for (const [name, sign] of [['right_leg', -1], ['left_leg', 1]]) r[name] = {t: add(hip, [sign * .125, 0, 0]), q: q(p[name])};
  const arm = r[cfg.weaponArm || 'right_arm'];
  r.weapon = {t: add(arm.t, rot(arm.q, cfg.grip || [0, -.535, -.015])), q: mul(arm.q, q(p.weapon))};
  for (const [name, dt] of Object.entries(cfg.attach || {})) r[name] = {t: r[dt].t, q: r[dt].q};
  const hide = new Set(p.hide || []), show = new Set(p.show || []);
  for (const [name, a] of Object.entries(r)) {
    a.t = add(p.rootShift || [0, 0, 0], rot(root, a.t).map(v => v * (p.size ?? cfg.size ?? 1)));
    a.q = mul(root, a.q);
    let s = p.size ?? cfg.size ?? 1;
    if (hide.has(name) || hide.has('*') || ((cfg.glowParts || []).includes(name) && !show.has(name))) s = 0;
    a.s = [s, s, s];
    a.t = [a.t[0], a.t[1], -a.t[2]];
    a.q = [-a.q[0], -a.q[1], a.q[2], a.q[3]];
  }
  for (const name of [cfg.weaponName || 'weapon', ...Object.keys(cfg.attach || {})]) r[name].q = mul(r[name].q, q([0, 90, 0]));
  return r;
}

// lowest geometry point of a part (relative to the feet plane), as item_display renders it
function minY(modelKey, tr) {
  const els = MODELS[modelKey];
  let m = Infinity;
  for (const e of els) for (const x of [e.from[0], e.to[0]]) for (const y of [e.from[1], e.to[1]]) for (const z of [e.from[2], e.to[2]]) {
    let v = [x / 16 - .5, y / 16 - .5, z / 16 - .5];
    v = [-v[0], v[1], -v[2]];                         // vanilla Y180
    v = v.map((c, i) => c * tr.s[i]);
    v = rot(tr.q, v);
    m = Math.min(m, v[1] + tr.t[1]);
  }
  return m;
}

const OUT = {};
function rigSet(id, cfg, poses) {
  const parts = [...HUMAN_PARTS, ...(cfg.glowParts || [])];
  const list = [];
  for (const [pid, name, dur, over] of poses) {
    const r = humanoid(cfg, over);
    // Feet stay planted: when a pose (bent limbs, inflated soles) would dip below the feet plane, the whole pose is
    // lifted by exactly that much, so no part is ever drawn under the floor.
    let lo = Infinity;
    for (const part of parts) if (r[part].s[0] !== 0) lo = Math.min(lo, minY(`${id}/${part}`, r[part]));
    if (lo < 0) for (const part of parts) r[part].t[1] -= lo;
    for (const part of parts) if (r[part].s[0] !== 0 && minY(`${id}/${part}`, r[part]) < -1e-4) throw Error(`${id} pose ${pid} ${name}: ${part} below the feet`);
    list.push({id: pid, name, dur, rig: Object.fromEntries(parts.map(pt => [pt, {t: r[pt].t.map(fl), q: r[pt].q.map(fl), s: r[pt].s.map(fl)}]))});
  }
  OUT[id] = {parts, poses: list};
}
const fl = v => { const x = Math.abs(v) < 5e-7 ? 0 : Number(v.toFixed(5)); return x; };

// ---- 카이라기·뇌전: low two-hand guard, katana forward; long lunges; a wound-up spin.
const KR = {size: 1.08, armOpen: 18, glowParts: ['aura'], attach: {aura: 'weapon'},
  base: {torso: [8, -14, 0], head: [-6, 14, 0], right_arm: [52, -8, -6], left_arm: [48, 30, 20], right_leg: [-12, 0, -4], left_leg: [14, 0, 4], weapon: [-128, 6, -6], shift: [0, -.03, 0]}};
const krPoses = [];
for (let i = 0; i < 4; i++) { const a = i * Math.PI / 2, s = Math.sin(a); krPoses.push([i, 'guard_breath_' + i, 6, {shift: [0, -.03 + s * .012, 0], torso: [8 + s * 1.5, -14, 0], right_arm: [52 + s * 2, -8, -6], left_arm: [48 + s * 2, 30, 20]}]); }
for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4, s = Math.sin(a); krPoses.push([10 + i, 'stalk_' + i, 3, {shift: [0, -.02 + Math.abs(Math.cos(a)) * .03, 0], torso: [14, -12 + s * 4, -s * 2], head: [-10, 12 - s * 4, 0], right_leg: [s * 34, 0, -3], left_leg: [-s * 34, 0, 3], right_arm: [40, -10, -8], left_arm: [36, 26, 18], weapon: [-118, 6, -10]}]); }
krPoses.push([20, 'dash_tell', 2, {show: ['aura'], shift: [0, -.12, .04], torso: [26, 34, -6], head: [-22, -34, 4], right_arm: [24, 10, -40], left_arm: [40, -10, 26], right_leg: [-26, 0, -8], left_leg: [40, 0, 8], weapon: [-150, 20, -20]}]);
krPoses.push([21, 'dash_cut', 2, {show: ['aura'], shift: [0, -.1, -.08], torso: [24, -36, 6], head: [-20, 36, -4], right_arm: [80, -50, 30], left_arm: [30, 20, 30], right_leg: [40, 0, -6], left_leg: [-28, 0, 6], weapon: [-80, -10, -10]}]);
krPoses.push([22, 'dash_follow', 3, {shift: [0, -.08, -.06], torso: [18, -30, 6], head: [-14, 30, -4], right_arm: [40, -60, 34], left_arm: [24, 14, 24], right_leg: [30, 0, -6], left_leg: [-22, 0, 6], weapon: [-125, -10, -16]}]);
krPoses.push([30, 'spent_low', 4, {shift: [0, -.17, 0], torso: [34, -6, 4], head: [-8, 6, 0], right_arm: [20, -6, -10], left_arm: [44, 0, 26], right_leg: [-22, 0, -8], left_leg: [30, 0, 8], weapon: [158, 0, -8]}]);
krPoses.push([31, 'spent_breath', 8, {shift: [0, -.19, 0], torso: [38, -6, 2], head: [-4, 6, 0], right_arm: [16, -6, -10], left_arm: [48, 0, 28], right_leg: [-22, 0, -8], left_leg: [30, 0, 8], weapon: [162, 0, -8]}]);
krPoses.push([40, 'spin_wind', 4, {show: ['aura'], shift: [0, -.1, .03], torso: [12, 60, -8], head: [-6, -50, 4], right_arm: [120, 30, -30], left_arm: [70, -20, 40], right_leg: [-18, 0, -10], left_leg: [24, 0, 10], weapon: [-110, 10, 10]}]);
for (const [k, deg] of [[41, 100], [42, 220], [43, 340]]) krPoses.push([k, 'spin_' + deg, 2, {show: ['aura'], root: [0, -deg, 0], shift: [0, -.08, 0], torso: [10, -20, 0], head: [-6, 20, 0], right_arm: [90, -70, 0], left_arm: [60, 30, 30], right_leg: [-12, 0, -10], left_leg: [16, 0, 10], weapon: [-90, 0, 0]}]);
krPoses.push([44, 'spin_finish', 3, {shift: [0, -.1, 0], torso: [16, -26, 4], head: [-10, 26, 0], right_arm: [60, -60, 20], left_arm: [30, 20, 24], right_leg: [-16, 0, -8], left_leg: [22, 0, 8], weapon: [-125, -10, -10]}]);
krPoses.push([50, 'hit_recoil', 2, {shift: [0, -.07, .04], torso: [-12, -10, -6], head: [12, 10, 4], right_arm: [36, -8, -20], left_arm: [36, 20, 26]}]);
krPoses.push([51, 'hit_recover', 3, {shift: [0, -.04, .02], torso: [0, -12, -2], head: [4, 12, 2]}]);
krPoses.push([60, 'death_kneel', 3, {shift: [0, -.3, 0], torso: [30, -6, -10], head: [24, 6, -6], right_arm: [10, 0, -24], left_arm: [30, 0, 30], right_leg: [-80, 0, -6], left_leg: [70, 0, 6], weapon: [-10, 0, -40]}]);
krPoses.push([61, 'death_fall', 5, {root: [0, 0, -50], rootShift: [0, .18, 0], shift: [0, -.1, 0], torso: [10, 0, -6], head: [14, 4, 4], right_arm: [10, 0, -20], left_arm: [20, 0, 30], right_leg: [-10, 0, -4], left_leg: [16, 0, 4], weapon: [-30, 0, -40]}]);
krPoses.push([62, 'death_land', 4, {root: [0, 0, -88], rootShift: [0, .32, 0], torso: [4, 0, 0], head: [12, 8, 4], right_arm: [4, 0, -10], left_arm: [26, 8, 25], right_leg: [-7, 0, 0], left_leg: [16, 0, 3], weapon: [-10, 0, -20]}]);
krPoses.push([63, 'death_dissolve', 5, {root: [0, 0, -88], rootShift: [0, .1, 0], torso: [4, 0, 0], head: [12, 8, 4], right_arm: [4, 0, -10], left_arm: [26, 8, 25], right_leg: [-7, 0, 0], left_leg: [16, 0, 3], weapon: [-10, 0, -20], size: .04}]);
rigSet('kr', KR, krPoses);

// ---- 그림자 닌자: low crouch, reverse-grip blade; vanishes (all parts scale 0) and reappears crouched.
const NJ = {size: 0.96, armOpen: 10, glowParts: ['glint'], attach: {glint: 'weapon'},
  base: {torso: [24, 10, 0], head: [-20, -10, 0], right_arm: [10, 0, -24], left_arm: [56, 10, 16], right_leg: [-40, 0, -8], left_leg: [30, 0, 8], weapon: [-200, 0, 0], shift: [0, -.14, 0]}};
const njPoses = [];
for (let i = 0; i < 4; i++) { const s = Math.sin(i * Math.PI / 2); njPoses.push([i, 'crouch_' + i, 6, {shift: [0, -.14 + s * .01, 0], torso: [24 + s * 2, 10, 0]}]); }
for (let i = 0; i < 8; i++) { const s = Math.sin(i * Math.PI / 4); njPoses.push([10 + i, 'dash_run_' + i, 3, {shift: [0, -.08 + Math.abs(Math.cos(i * Math.PI / 4)) * .04, 0], torso: [40, s * 6, 0], head: [-34, -s * 6, 0], right_arm: [-60, 0, -12], left_arm: [-60, 0, 12], right_leg: [s * 50, 0, -4], left_leg: [-s * 50, 0, 4], weapon: [-200, 0, 0]}]); }
njPoses.push([20, 'hidden', 0, {hide: ['*']}]);
njPoses.push([21, 'appear', 2, {shift: [0, -.22, 0], torso: [36, 0, 0], head: [-28, 0, 0], right_arm: [20, 0, -40], left_arm: [40, 0, 36], right_leg: [-60, 0, -10], left_leg: [50, 0, 10]}]);
njPoses.push([22, 'glint', 3, {show: ['glint'], shift: [0, -.12, .03], torso: [10, 40, -4], head: [-4, -40, 2], right_arm: [150, 20, -20], left_arm: [60, -20, 30], right_leg: [-30, 0, -8], left_leg: [34, 0, 8], weapon: [-165, 0, 0]}]);
njPoses.push([23, 'slash', 2, {show: ['glint'], shift: [0, -.12, -.06], torso: [30, -40, 6], head: [-24, 40, -4], right_arm: [40, -60, 50], left_arm: [20, 20, 20], right_leg: [36, 0, -6], left_leg: [-24, 0, 6], weapon: [-90, 0, -10]}]);
njPoses.push([24, 'slash_follow', 3, {shift: [0, -.14, -.05], torso: [28, -44, 6], head: [-22, 44, -4], right_arm: [10, -70, 50], left_arm: [16, 16, 18], right_leg: [30, 0, -6], left_leg: [-20, 0, 6], weapon: [-100, 0, -14]}]);
njPoses.push([30, 'exhausted', 4, {shift: [0, -.2, 0], torso: [52, 0, 0], head: [-20, 0, 0], right_arm: [40, 0, -10], left_arm: [40, 0, 10], right_leg: [-30, 0, -6], left_leg: [30, 0, 6], weapon: [-140, 0, 0]}]);
njPoses.push([31, 'exhausted_b', 8, {shift: [0, -.23, 0], torso: [58, 0, 0], head: [-14, 0, 0], right_arm: [46, 0, -10], left_arm: [46, 0, 10], right_leg: [-32, 0, -6], left_leg: [32, 0, 6], weapon: [-140, 0, 0]}]);
njPoses.push([40, 'throw_tell', 3, {show: ['glint'], shift: [0, -.1, .03], torso: [6, 30, -4], head: [-2, -30, 2], right_arm: [10, 0, -30], left_arm: [150, 20, 50], right_leg: [-24, 0, -6], left_leg: [26, 0, 6]}]);
njPoses.push([41, 'throw_release', 2, {shift: [0, -.1, -.04], torso: [20, -30, 4], head: [-16, 30, -2], right_arm: [10, 0, -30], left_arm: [70, -40, -10], right_leg: [20, 0, -6], left_leg: [-16, 0, 6]}]);
njPoses.push([50, 'hit_recoil', 2, {shift: [0, -.12, .04], torso: [4, 10, -6], head: [10, -10, 4]}]);
njPoses.push([51, 'hit_recover', 3, {shift: [0, -.13, .02], torso: [16, 10, -2], head: [-10, -10, 2]}]);
njPoses.push([60, 'death_kneel', 3, {shift: [0, -.3, 0], torso: [40, 0, -10], head: [20, 0, -6], right_leg: [-80, 0, -6], left_leg: [70, 0, 6]}]);
njPoses.push([61, 'death_smoke', 6, {shift: [0, -.3, 0], torso: [40, 0, -10], head: [20, 0, -6], right_leg: [-80, 0, -6], left_leg: [70, 0, 6], size: .05}]);
rigSet('nj', NJ, njPoses);

// ---- 시킨 술사: upright caster, staff in the right hand with a caged electro lantern.
const CC = {size: 1.0, armOpen: 10, glowParts: ['flare'], attach: {flare: 'weapon'},
  base: {torso: [2, 0, 0], head: [-2, 0, 0], right_arm: [24, -6, -8], left_arm: [8, 0, 10], right_leg: [-3, 0, -2], left_leg: [3, 0, 2], weapon: [-24, 0, 8]}};
const ccPoses = [];
for (let i = 0; i < 4; i++) { const s = Math.sin(i * Math.PI / 2); ccPoses.push([i, 'idle_' + i, 6, {shift: [0, s * .012, 0], torso: [2 + s, 0, 0], left_arm: [8 + s * 3, 0, 10 + s * 2]}]); }
for (let i = 0; i < 8; i++) { const s = Math.sin(i * Math.PI / 4); ccPoses.push([10 + i, 'walk_' + i, 3, {shift: [0, Math.abs(Math.cos(i * Math.PI / 4)) * .02, 0], torso: [5, s * 3, 0], right_leg: [s * 24, 0, -2], left_leg: [-s * 24, 0, 2], left_arm: [-s * 18, 0, 10]}]); }
ccPoses.push([20, 'cast_raise', 4, {show: ['flare'], shift: [0, .02, .02], torso: [-10, 0, 0], head: [-14, 0, 0], right_arm: [160, -10, -14], left_arm: [120, 20, 30], right_leg: [-6, 0, -4], left_leg: [8, 0, 4], weapon: [-172, 0, 0]}]);
ccPoses.push([21, 'cast_hold', 6, {show: ['flare'], shift: [0, .03, .02], torso: [-12, 0, 0], head: [-16, 0, 0], right_arm: [166, -10, -16], left_arm: [130, 20, 34], right_leg: [-6, 0, -4], left_leg: [8, 0, 4], weapon: [-178, 0, 0]}]);
ccPoses.push([22, 'cast_release', 2, {shift: [0, 0, -.04], torso: [14, 0, 0], head: [0, 0, 0], right_arm: [100, -10, -10], left_arm: [80, 30, 30], weapon: [-140, 0, 0]}]);
ccPoses.push([30, 'blink_fold', 2, {shift: [0, -.04, 0], torso: [10, 0, 0], right_arm: [30, 0, -4], left_arm: [30, 0, 4], weapon: [-30, 0, 0], size: .6}]);
ccPoses.push([31, 'dazed', 4, {shift: [0, -.08, 0], torso: [20, 0, 10], head: [20, 10, 14], right_arm: [10, 0, -20], left_arm: [16, 0, 24], right_leg: [-8, 0, -6], left_leg: [10, 0, 6], weapon: [-10, 0, 20]}]);
ccPoses.push([32, 'dazed_b', 6, {shift: [0, -.08, 0], torso: [20, 0, -10], head: [20, -10, -14], right_arm: [10, 0, -20], left_arm: [16, 0, 24], right_leg: [-8, 0, -6], left_leg: [10, 0, 6], weapon: [-10, 0, 20]}]);
ccPoses.push([50, 'hit_recoil', 2, {shift: [0, -.05, .04], torso: [-14, 0, -6], head: [12, 0, 4]}]);
ccPoses.push([51, 'hit_recover', 3, {shift: [0, -.02, .02], torso: [-4, 0, -2], head: [4, 0, 2]}]);
ccPoses.push([60, 'death_buckle', 3, {shift: [0, -.2, 0], torso: [26, 0, -14], head: [20, 0, -8], right_arm: [20, 0, -30], left_arm: [40, 0, 30], right_leg: [-24, 0, -10], left_leg: [30, 0, 10], weapon: [-40, 0, 40]}]);
ccPoses.push([61, 'death_fall', 5, {root: [0, 0, 52], rootShift: [0, .18, 0], shift: [0, -.06, 0], torso: [6, 0, 8], head: [14, 0, -6], right_arm: [10, 0, -20], left_arm: [20, 0, 20], right_leg: [-8, 0, -4], left_leg: [12, 0, 4], weapon: [-60, 0, 40]}]);
ccPoses.push([62, 'death_land', 4, {root: [0, 0, 88], rootShift: [0, .32, 0], torso: [4, 0, 0], head: [12, 0, -4], right_arm: [4, 0, -10], left_arm: [20, 0, 20], right_leg: [-6, 0, 0], left_leg: [12, 0, 0], weapon: [-80, 0, 40]}]);
ccPoses.push([63, 'death_dissolve', 5, {root: [0, 0, 88], rootShift: [0, .1, 0], torso: [4, 0, 0], head: [12, 0, -4], right_arm: [4, 0, -10], left_arm: [20, 0, 20], right_leg: [-6, 0, 0], left_leg: [12, 0, 0], weapon: [-80, 0, 40], size: .04}]);
rigSet('cc', CC, ccPoses);

// ---- 번개 시킨: a single display ("body") whose item model is the wing frame; the pose adds scale / pitch.
function ciPose(id, name, dur, frame, o = {}) {
  const size = o.size ?? 1.2, tr = {t: [0, 0.5, 0], q: q([o.pitch || 0, 0, 0]), s: [size, size, size]};
  tr.t = [tr.t[0], tr.t[1], -tr.t[2]]; tr.q = [-tr.q[0], -tr.q[1], tr.q[2], tr.q[3]];
  const lo = minY(`ci/${frame}`, tr);
  if (lo < -1e-4) throw Error(`ci pose ${id}: below the feet (${lo})`);
  return {id, name, dur, model: {body: `rlk:cm/ci/${frame}`}, rig: {body: {t: tr.t.map(fl), q: tr.q.map(fl), s: tr.s.map(fl)}}};
}
OUT.ci = {parts: ['body'], poses: [ciPose(0, 'flap_up', 2, 'f_up'), ciPose(1, 'flap_down', 2, 'f_down'), ciPose(2, 'tell_spread', 2, 'f_tell', {size: 1.5}),
  ciPose(3, 'ram', 1, 'f_ram', {pitch: 8}), ciPose(60, 'pop', 3, 'f_tell', {size: 0.02})]};

fs.writeFileSync(path.join(base, 'ch2_elite_poses.json'), JSON.stringify({
  authoring: 'Original keyframes for the chapter-2 elites (build_ch2_elite_rigs.mjs); 20 ticks/second.',
  space: 'Runtime item_display transformations: +Z forward, right hand on -X (vanilla Y180 applies after).', mobs: OUT}, null, 1) + '\n');
let px = 0;
for (const f of ['skin/mob_kr', 'skin/mob_nj', 'skin/mob_cc']) px += 64 * 64;
px += 16 * 16;
console.log(JSON.stringify({models: Object.keys(MODELS).length, poses: Object.fromEntries(Object.entries(OUT).map(([k, v]) => [k, v.poses.length])), texturePixels: px}));
