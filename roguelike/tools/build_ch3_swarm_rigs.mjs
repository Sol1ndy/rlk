// Chapter-3 (Sumeru) swarm mob rigs: 둥실 버섯 (fu) + 포자 주머니 (fp), 에르미타 단검 용병 (em), 모래 전갈 새끼 (sb),
// 에르미타 맑은물 술사 (cw). Original geometry and procedurally painted textures; no reference-pack assets are copied.
// Run: node tools/build_ch3_swarm_rigs.mjs --resourcepack <unpacked resource pack>
// Writes only resource-pack files: models/item/cm/c3/{fu,fp,em,sb,cw}/**, items/cm/c3/**, textures/skin/mob_c3_{em,cw}.png,
// textures/cm/c3/props.png, and merges its sprites into assets/minecraft/atlases/items.json (filter-then-push by id).
// Painter and box-model helpers: tools/ch2mob/paint.mjs (shared with the chapter-2 generator). The datapack side
// (poses, AI) is tools/build_ch3_mobs.py; the part lists here must match tools/ch3mob/swarm.py.
import fs from 'node:fs';
import path from 'node:path';
import {Canvas, cl, hex, R, boxPaint, all, box, r6, SHAPES} from './ch2mob/paint.mjs';

const arg = name => { const i = process.argv.indexOf(name); return i < 0 ? undefined : process.argv[i + 1]; };
const rpArg = arg('--resourcepack');
if (!rpArg) throw new Error('Provide --resourcepack pointing to an unpacked resource pack.');
const rpRoot = path.resolve(rpArg);
if (!fs.existsSync(path.join(rpRoot, 'pack.mcmeta'))) throw new Error('The resource pack must contain pack.mcmeta.');
const rp = path.join(rpRoot, 'assets/rlk');
const put = (p, s) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, s); };
const json = (p, o) => put(p, JSON.stringify(o, null, 2) + '\n');

// ---------------------------------------------------------------- props sheet 64x64: 8x8 tiles
const TILE = {
  capG: [0, 0], capT: [1, 0], capD: [2, 0], stem: [3, 0], stemD: [4, 0], spot: [5, 0], face: [6, 0], podG: [7, 0],
  podL: [0, 1], sandL: [1, 1], sandM: [2, 1], sandD: [3, 1], chit: [4, 1], chitD: [5, 1], chitL: [6, 1], sting: [7, 1],
  eye: [0, 2], steel: [1, 2], steelB: [2, 2], grip: [3, 2], leather: [4, 2], cloth: [5, 2], clothD: [6, 2], red: [7, 2],
  water: [0, 3], waterB: [1, 3], gold: [2, 3], white: [3, 3], blue: [4, 3], blueD: [5, 3], teal: [6, 3], gill: [7, 3],
  moss: [0, 4], tendril: [1, 4], vein: [2, 4], ivory: [3, 4]};
const tileUV = t => { const [i, j] = TILE[t]; return [i * 2, j * 2, i * 2 + 2, j * 2 + 2]; };
function props() {
  const cv = new Canvas(64, 64, 307);
  const T = (name, c, n = 10, g = 0, extra) => { const [i, j] = TILE[name]; cv.rect(i * 8, j * 8, 8, 8, c, n, g); if (extra) extra(i * 8, j * 8); };
  // fungus: pale green cap with mint speckles, teal crown, dark teal gills, cream stem; the stem front has two eyes
  T('capG', hex('#a9d8a2'), 8, -10, (x, y) => { for (let k = 0; k < 6; k++) cv.px(x + (k * 5 + 1) % 8, y + (k * 3 + 2) % 8, hex('#d6f3cf')); });
  T('capT', hex('#5fbfae'), 8, -12, (x, y) => { for (let k = 0; k < 4; k++) cv.px(x + (k * 3 + 2) % 8, y + (k * 5 + 1) % 8, hex('#a5eadb')); });
  T('capD', hex('#2c6f6a'), 6, 0, (x, y) => { for (let i = 0; i < 8; i += 2) cv.line(x + i, y, x + i, y + 7, hex('#3c8c84')); });
  T('stem', hex('#ece4cf'), 6, 8); T('stemD', hex('#c7bb9c'), 6);
  T('spot', hex('#e9fff4'), 3);
  T('face', hex('#ece4cf'), 5, 0, (x, y) => { cv.rect(x + 1, y + 3, 2, 2, hex('#1f2b2a'), 2); cv.rect(x + 5, y + 3, 2, 2, hex('#1f2b2a'), 2); cv.px(x + 1, y + 3, hex('#9ff5e0')); cv.px(x + 5, y + 3, hex('#9ff5e0')); cv.rect(x + 3, y + 6, 2, 1, hex('#8f826a')); });
  T('podG', hex('#6fae4a'), 10, -14, (x, y) => { cv.line(x + 1, y, x + 3, y + 7, hex('#9ad86a')); cv.line(x + 6, y, x + 5, y + 7, hex('#9ad86a')); });
  T('podL', hex('#e6ff8a'), 4, -8);
  // sand + scorpion chitin
  T('sandL', hex('#ead7a0'), 10, 0, (x, y) => { for (let k = 0; k < 5; k++) cv.px(x + (k * 3) % 8, y + (k * 5 + 3) % 8, hex('#f6ebc8')); });
  T('sandM', hex('#d8bd7c'), 12, 0, (x, y) => { for (let k = 0; k < 5; k++) cv.px(x + (k * 7 + 2) % 8, y + (k * 3 + 1) % 8, hex('#b89c5f')); });
  T('sandD', hex('#a8875a'), 10);
  T('chit', hex('#c99a5b'), 8, -10, (x, y) => { cv.rect(x, y + 6, 8, 1, hex('#a27840'), 3); });
  T('chitD', hex('#8a6237'), 6, -6, (x, y) => { cv.rect(x, y + 3, 8, 1, hex('#6c4a28'), 3); });
  T('chitL', hex('#e3bf86'), 6, -8);
  T('sting', hex('#6b3a1f'), 6, 10, (x, y) => { cv.px(x + 3, y + 1, hex('#f0a24a')); cv.px(x + 4, y + 1, hex('#f0a24a')); });
  T('eye', hex('#121014'), 3, 0, (x, y) => { cv.px(x + 2, y + 2, hex('#7a6a5a')); });
  // mercenary kit
  T('steel', hex('#c3c8cc'), 6, 18); T('steelB', hex('#f2f6f8'), 4, 8);
  T('grip', hex('#4a2f1e'), 4, 0, (x, y) => { for (let j = 0; j < 8; j += 2) cv.line(x, y + j, x + 7, y + j + 1, hex('#7d5636')); });
  T('leather', hex('#7a5232'), 8, -6);
  T('cloth', hex('#b98f5a'), 9, -10, (x, y) => { for (let j = 1; j < 8; j += 3) cv.line(x, y + j, x + 7, y + j, hex('#a37a48')); });
  T('clothD', hex('#5c4330'), 7, -6);
  T('red', hex('#a8322b'), 8, -8, (x, y) => { cv.rect(x, y + 3, 8, 1, hex('#e0b54a'), 4); });
  // water mage kit (water is translucent)
  T('water', [76, 160, 232, 165], 10, -20);
  T('waterB', [196, 240, 255, 235], 6, 0);
  T('gold', hex('#e2b545'), 10, 16); T('white', hex('#efece4'), 5, -6);
  T('blue', hex('#2f5fa8'), 8, -12, (x, y) => { cv.line(x, y + 6, x + 7, y + 6, hex('#5c8fd6')); });
  T('blueD', hex('#1d3b6e'), 6, -6);
  T('teal', hex('#2fa7a0'), 6, -8);
  T('gill', hex('#7ff0d8'), 4, 0, (x, y) => { for (let i = 0; i < 8; i += 2) cv.line(x + i, y, x + i, y + 7, hex('#c7fff0')); });
  T('moss', hex('#4f7d36'), 10);
  T('tendril', hex('#9fcfa5'), 6, 10);
  T('vein', hex('#d4ff7a'), 3);
  T('ivory', hex('#efe2c4'), 6, -10);
  return cv;
}

// ---------------------------------------------------------------- skins (64x64, player box layout)
function skinMerc() {
  const cv = new Canvas(64, 64, 401);
  const skin = hex('#b9835a'), skinD = hex('#93623f'), cloth = hex('#b48a55'), clothD = hex('#6e5136'), sash = hex('#a8322b'), wrap = hex('#d9c9a4');
  const strap = hex('#4a2f1e'), boot = hex('#3d2a1d'), pants = hex('#8c6a45'), gold = hex('#e0b54a');
  all(cv, R.head, skin, 7);
  boxPaint(cv, R.head, (f, x, y, w, h) => {
    if (f === 'top' || f === 'back') cv.rect(x, y, w, h, hex('#2a1d17'), 6);
    if (f === 'right' || f === 'left') cv.rect(x, y, w, 3, hex('#2a1d17'), 6);
    if (f === 'front') {
      cv.rect(x, y, w, 2, hex('#2a1d17'), 6);
      cv.rect(x + 1, y + 3, 2, 1, hex('#f2ead8')); cv.rect(x + 5, y + 3, 2, 1, hex('#f2ead8'));
      cv.px(x + 2, y + 3, hex('#3a5a3a')); cv.px(x + 5, y + 3, hex('#3a5a3a'));
      cv.rect(x + 1, y + 2, 2, 1, skinD); cv.rect(x + 5, y + 2, 2, 1, skinD);
      cv.rect(x + 2, y + 6, 4, 1, skinD); cv.px(x + 6, y + 4, hex('#c9503c')); // war paint dot
    }
  });
  cv.clear(32, 0, 32, 16);
  all(cv, R.body, cloth, 8, -12);
  boxPaint(cv, R.body, (f, x, y, w, h) => {
    if (f === 'top' || f === 'bottom') return;
    if (f === 'front') { cv.rect(x + 2, y, 4, 3, skin, 6); cv.line(x, y, x + 7, y + 8, strap); cv.line(x + 1, y, x + 7, y + 7, strap); }
    if (f === 'back') { cv.line(x + 7, y, x, y + 8, strap); }
    cv.rect(x, y + 8, w, 2, sash, 6); cv.px(x + 1, y + 9, gold);
    cv.rect(x, y + 10, w, 2, clothD, 5);
  });
  cv.clear(16, 32, 24, 16);
  for (const [reg, sl] of [[R.rarm, R.rsleeve], [R.larm, R.lsleeve]]) {
    all(cv, reg, skin, 7, -6);
    boxPaint(cv, reg, (f, x, y, w, h) => {
      if (f === 'top') { cv.rect(x, y, w, h, cloth, 6); return; }
      if (f === 'bottom') return;
      cv.rect(x, y, w, 4, cloth, 7); cv.rect(x, y + 4, w, 1, clothD, 4);
      cv.rect(x, y + 6, w, 5, wrap, 8); for (let j = 6; j < 11; j += 2) cv.line(x, y + j, x + w - 1, y + j + 1, hex('#b5a37c'));
      cv.rect(x, y + 11, w, 1, skinD, 4);
    });
    cv.clear(sl[0], sl[1], 16, 16);
  }
  for (const [reg, ov] of [[R.rleg, R.rpants], [R.lleg, R.lpants]]) {
    all(cv, reg, pants, 8, -10);
    boxPaint(cv, reg, (f, x, y, w, h) => {
      if (f === 'bottom') { cv.rect(x, y, w, h, boot, 4); return; }
      if (f === 'top') return;
      cv.rect(x, y + 4, w, 1, clothD, 3); cv.rect(x, y + 8, w, 4, boot, 5); cv.rect(x, y + 8, w, 1, strap, 3);
    });
    cv.clear(ov[0], ov[1], 16, 16);
  }
  return cv;
}

function skinMage() {
  const cv = new Canvas(64, 64, 433);
  const skin = hex('#d7a77f'), skinD = hex('#b58460'), blue = hex('#2f5fa8'), blueD = hex('#1d3b6e'), white = hex('#efece4'), gold = hex('#e2b545');
  const teal = hex('#2fa7a0'), hair = hex('#e9e2d4');
  all(cv, R.head, skin, 6);
  boxPaint(cv, R.head, (f, x, y, w, h) => {
    if (f === 'top' || f === 'back') cv.rect(x, y, w, h, hair, 6);
    if (f === 'right' || f === 'left') cv.rect(x, y, w, 4, hair, 6);
    if (f === 'front') {
      cv.rect(x, y, w, 2, hair, 6); cv.px(x, y + 2, hair); cv.px(x + 7, y + 2, hair);
      cv.rect(x + 1, y + 3, 2, 1, hex('#f4f8ff')); cv.rect(x + 5, y + 3, 2, 1, hex('#f4f8ff'));
      cv.px(x + 2, y + 3, hex('#2a7fd0')); cv.px(x + 5, y + 3, hex('#2a7fd0'));
      cv.rect(x + 3, y + 6, 2, 1, skinD); cv.px(x + 3, y + 1, hex('#5ec8f0')); cv.px(x + 4, y + 1, hex('#5ec8f0')); // water mark
    }
  });
  cv.clear(32, 0, 32, 16);
  all(cv, R.body, blue, 8, -14);
  boxPaint(cv, R.body, (f, x, y, w, h) => {
    if (f === 'top' || f === 'bottom') return;
    if (f === 'front') { cv.rect(x + 3, y, 2, 12, white, 4); cv.rect(x + 2, y, 4, 2, gold, 6); cv.px(x + 3, y + 4, hex('#7fd8ff')); cv.px(x + 4, y + 4, hex('#7fd8ff')); }
    cv.rect(x, y + 8, w, 2, teal, 5); cv.rect(x, y + 10, w, 2, blueD, 5);
  });
  cv.clear(16, 32, 24, 16);
  for (const [reg, sl] of [[R.rarm, R.rsleeve], [R.larm, R.lsleeve]]) {
    all(cv, reg, blue, 8, -8);
    boxPaint(cv, reg, (f, x, y, w, h) => {
      if (f === 'bottom') { cv.rect(x, y, w, h, skin, 4); return; }
      if (f === 'top') return;
      cv.rect(x, y + 7, w, 1, gold, 4); cv.rect(x, y + 8, w, 3, white, 5); cv.rect(x, y + 11, w, 1, skin, 3);
    });
    cv.clear(sl[0], sl[1], 16, 16);
  }
  for (const [reg, ov] of [[R.rleg, R.rpants], [R.lleg, R.lpants]]) {
    all(cv, reg, blueD, 6, -6);
    boxPaint(cv, reg, (f, x, y, w, h) => { if (f === 'bottom') cv.rect(x, y, w, h, hex('#c9b48a'), 4); else if (f !== 'top') cv.rect(x, y + 10, w, 2, hex('#c9b48a'), 4); });
    cv.clear(ov[0], ov[1], 16, 16);
  }
  return cv;
}

// ---------------------------------------------------------------- model helpers
const FACES = ['north', 'south', 'east', 'west', 'up', 'down'];
// solid box, one tile on every face (or {face: tile} overrides); rot = {axis, angle, origin}
function solid(from, to, tile, rot, over = {}) {
  const e = {from: from.map(r6), to: to.map(r6), faces: Object.fromEntries(FACES.map(f => [f, {texture: '#props', uv: tileUV(over[f] || tile), tintindex: 0}]))};
  if (rot) e.rotation = rot;
  return e;
}
const mirror = (from, to, tile, rot, over) => [solid(from, to, tile, rot, over), solid([16 - to[0], from[1], from[2]], [16 - from[0], to[1], to[2]], tile,
  rot ? {...rot, angle: -rot.angle, origin: [16 - rot.origin[0], rot.origin[1], rot.origin[2]]} : undefined, over)];
const written = [];
const PROPS = 'rlk:cm/c3/props';
function model(mob, part, textures, elements) {
  const id = `cm/c3/${mob}/${part}`;
  json(path.join(rp, 'models/item', id + '.json'), {ambientocclusion: false, textures: {...textures, particle: Object.values(textures)[0]}, elements});
  json(path.join(rp, 'items', id + '.json'), {model: {type: 'minecraft:model', model: 'rlk:item/' + id, tints: [{type: 'minecraft:custom_model_data', index: 0, default: 16777215}]}});
  written.push(id);
}
function humanoid(mob, extra) {
  for (const [name, s] of Object.entries(SHAPES)) {
    const els = [box(s.from, s.to, s.uv), box(s.from, s.to, s.over, s.inflate)];
    for (const e of (extra[name] || [])) els.push(e);
    model(mob, name, {skin: `rlk:skin/mob_c3_${mob}`, props: PROPS}, els);
  }
}
const P = {props: PROPS};

// ---- 둥실 버섯: stem (eyes on the north face), wide cap (pale green, teal crown), bright spots + glowing gills
model('fu', 'stem', P, [
  solid([6.2, 0, 6.2], [9.8, 6.6, 9.8], 'stem', null, {north: 'face', down: 'stemD'}),
  solid([5.7, 4.9, 5.7], [10.3, 5.7, 10.3], 'stemD'),
  solid([7.5, -4.2, 6.6], [8.3, 0, 7.4], 'tendril'), solid([6.5, -2.8, 8.4], [7.3, 0, 9.2], 'tendril'),
  solid([8.7, -3.4, 8.6], [9.5, 0, 9.4], 'tendril'), solid([7.8, -2.2, 9.0], [8.5, 0, 9.7], 'tendril')
]);
model('fu', 'cap', P, [
  solid([1, 6.6, 1], [15, 8.4, 15], 'capG', null, {down: 'capD'}),
  solid([2, 8.4, 2], [14, 10.3, 14], 'capG'),
  solid([3.5, 10.3, 3.5], [12.5, 11.7, 12.5], 'capT'),
  solid([5.5, 11.7, 5.5], [10.5, 12.5, 10.5], 'capT')
]);
model('fu', 'glow', P, [
  solid([1.7, 6.5, 1.7], [14.3, 6.6, 14.3], 'gill'),
  solid([2.6, 8.35, 3.2], [4.6, 8.75, 5.2], 'spot'), solid([11.0, 8.35, 10.6], [13.0, 8.75, 12.6], 'spot'),
  solid([10.6, 8.35, 2.4], [12.2, 8.75, 4.0], 'spot'), solid([3.4, 8.35, 11.4], [5.0, 8.75, 13.0], 'spot'),
  solid([4.6, 10.25, 4.4], [6.6, 10.65, 6.4], 'spot'), solid([9.2, 10.25, 9.6], [11.0, 10.65, 11.4], 'spot'),
  solid([7.2, 12.45, 6.6], [8.8, 12.75, 8.2], 'spot'),
  solid([0.95, 7.0, 6.4], [1.05, 8.0, 8.2], 'spot'), solid([14.95, 7.0, 8.0], [15.05, 8.0, 9.8], 'spot'),
  solid([7.0, 7.0, 0.95], [8.8, 8.0, 1.05], 'spot'), solid([5.4, 7.0, 14.95], [7.2, 8.0, 15.05], 'spot')
]);
// ---- 포자 주머니: a veined bulb on a moss collar (pivot on the floor), bright veins and tip
model('fp', 'pod', P, [
  solid([5, 8, 5], [11, 8.7, 11], 'moss'), solid([4, 8.7, 4], [12, 14.6, 12], 'podG'),
  solid([3.4, 9.6, 5], [12.6, 13.4, 11], 'podG'), solid([5, 9.6, 3.4], [11, 13.4, 12.6], 'podG'),
  solid([5, 14.6, 5], [11, 16.4, 11], 'podG'), solid([6.6, 16.4, 6.6], [9.4, 17.4, 9.4], 'podL'),
  solid([4.2, 8, 3.0], [6.4, 8.4, 5.6], 'moss', {axis: 'y', angle: 22.5, origin: [5.3, 8, 4.3]}),
  solid([9.6, 8, 10.4], [11.8, 8.4, 13], 'moss', {axis: 'y', angle: -22.5, origin: [10.7, 8, 11.7]})
]);
model('fp', 'glow', P, [
  solid([3.3, 10.2, 7.3], [3.4, 13.0, 8.7], 'vein'), solid([12.6, 10.2, 7.3], [12.7, 13.0, 8.7], 'vein'),
  solid([7.3, 10.2, 3.3], [8.7, 13.0, 3.4], 'vein'), solid([7.3, 10.2, 12.6], [8.7, 13.0, 12.7], 'vein'),
  solid([3.9, 13.4, 3.9], [5.1, 14.4, 4.0], 'vein'), solid([10.9, 13.4, 12.0], [12.1, 14.4, 12.1], 'vein'),
  solid([7.2, 17.4, 7.2], [8.8, 17.9, 8.8], 'waterB')
]);
// ---- 모래 전갈 새끼: body (head north, three leg pairs, pincers), tail (pivot = tail base, curls forward over the back), sand mound
const sbBody = [
  solid([5.5, 1.2, 1.0], [10.5, 3.6, 3.2], 'chitD', null, {north: 'chitD'}),
  solid([6.1, 2.9, 0.8], [7.1, 3.5, 1.1], 'eye'), solid([8.9, 2.9, 0.8], [9.9, 3.5, 1.1], 'eye'),
  solid([5, 1, 3], [11, 4, 8], 'chit'), solid([5.5, 1, 8], [10.5, 3.6, 12.6], 'chitD', null, {up: 'chit'}),
  solid([6.1, 1.1, 12.6], [9.9, 3.2, 15], 'chit')
];
for (const z of [3.6, 6.2, 8.8]) {
  sbBody.push(...mirror([2.4, 1.8, z], [5.1, 2.6, z + 0.8], 'chitL'));
  sbBody.push(...mirror([1.8, 0, z], [2.6, 2.4, z + 0.8], 'chitD'));
}
sbBody.push(...mirror([3.6, 1.6, -0.2], [5.0, 2.6, 3.0], 'chit'));
sbBody.push(...mirror([2.4, 1.2, -2.6], [5.4, 3.0, -0.2], 'chitL'));
sbBody.push(...mirror([2.4, 1.5, -3.8], [3.4, 2.7, -2.6], 'chitD'));
model('sb', 'body', P, sbBody);
model('sb', 'tail', P, [
  solid([7.0, 7.4, 7.6], [9.0, 9.8, 10.6], 'chit'),
  solid([7.1, 9.3, 9.4], [8.9, 12.8, 11.4], 'chitD'),
  solid([7.2, 12.3, 8.0], [8.8, 15.0, 10.2], 'chit'),
  solid([7.3, 14.4, 5.6], [8.7, 16.0, 8.4], 'chitD'),
  solid([7.2, 13.4, 3.8], [8.8, 15.2, 5.8], 'sting'),
  solid([7.7, 12.4, 3.0], [8.3, 13.6, 3.9], 'sting')
]);
model('sb', 'mound', P, [
  solid([2, 8, 2], [14, 9.4, 14], 'sandM'), solid([3.5, 9.4, 3.5], [12.5, 10.6, 12.5], 'sandL'),
  solid([5.5, 10.6, 5.5], [10.5, 11.5, 10.5], 'sandL'), solid([1.2, 8, 6], [2, 8.7, 10], 'sandD'), solid([14, 8, 5], [14.8, 8.7, 9], 'sandD'),
  solid([6, 8, 1.2], [10, 8.7, 2], 'sandD'), solid([3, 9.4, 9], [4.4, 10.1, 10.4], 'sandD'), solid([10.6, 10.6, 6.2], [11.6, 11.2, 7.2], 'sandD')
]);
// ---- 에르미타 단검 용병: headwrap + face veil, red sash, a short curved dagger in each hand, a sand cloak on the back
humanoid('em', {
  head: [solid([3.3, 13.2, 3.3], [12.7, 14.8, 12.7], 'cloth'), solid([3.6, 14.8, 3.6], [12.4, 16.8, 12.4], 'cloth'),
    solid([3.35, 8.0, 3.15], [12.65, 11.4, 3.6], 'clothD'), solid([6.2, 6.4, 12.6], [9.8, 13.4, 13.3], 'clothD'),
    solid([7.4, 15.4, 3.2], [8.6, 16.0, 3.5], 'gold')],
  body: [solid([3.7, -0.6, 5.7], [12.3, 0.9, 10.3], 'red')]
});
const dagger = () => [
  solid([7.4, 2.2, 7.4], [8.6, 6.0, 8.6], 'grip'), solid([7.3, 1.8, 7.3], [8.7, 2.3, 8.7], 'gold'),
  solid([6.5, 6.0, 7.2], [9.5, 6.7, 8.8], 'gold'),
  solid([7.6, 6.7, 7.45], [8.4, 10.2, 8.5], 'steel'), solid([7.6, 10.2, 7.7], [8.4, 12.6, 8.85], 'steel'),
  solid([7.7, 12.6, 8.0], [8.3, 13.8, 8.9], 'steelB'), solid([7.65, 7.0, 8.5], [8.35, 12.4, 8.75], 'steelB')
];
model('em', 'dagger_r', P, dagger());
model('em', 'dagger_l', P, dagger());
model('em', 'cloak', P, [
  solid([3.4, 6.2, 5.4], [12.6, 8.5, 10.9], 'cloth'),
  solid([3.2, -7.6, 10.3], [12.8, 8.5, 11.1], 'cloth', null, {north: 'clothD'}),
  solid([3.2, -8.6, 10.35], [5.4, -7.6, 11.05], 'clothD'), solid([6.6, -8.9, 10.35], [9.0, -7.6, 11.05], 'clothD'),
  solid([10.4, -8.4, 10.35], [12.8, -7.6, 11.05], 'clothD')
]);
// ---- 에르미타 맑은물 술사: hood with a gold circlet, long robe from the hips (pivot = hip), translucent water orb
humanoid('cw', {
  head: [solid([3.2, 16.0, 3.2], [12.8, 17.2, 12.8], 'blue'), solid([3.2, 8.4, 11.6], [12.8, 16.0, 12.8], 'blue'),
    solid([3.2, 8.4, 3.6], [4.2, 16.0, 11.6], 'blue'), solid([11.8, 8.4, 3.6], [12.8, 16.0, 11.6], 'blue'),
    solid([3.2, 15.0, 3.0], [12.8, 16.0, 4.2], 'white'), solid([3.4, 14.2, 2.9], [12.6, 14.8, 3.2], 'gold'),
    solid([7.4, 14.0, 2.7], [8.6, 15.0, 3.0], 'water')],
  body: [solid([3.7, -1.0, 5.7], [12.3, 0.4, 10.3], 'teal'), solid([5.5, 6.6, 5.6], [10.5, 8.3, 6.0], 'gold')]
});
model('cw', 'robe', P, [
  solid([3.6, 0.6, 5.4], [12.4, 8.0, 10.6], 'blue'),
  solid([3.2, -3.0, 5.0], [12.8, 0.6, 11.0], 'blue', null, {down: 'blueD'}),
  solid([3.1, -3.4, 4.9], [12.9, -2.6, 11.1], 'gold'),
  solid([6.9, -3.2, 4.7], [9.1, 7.6, 5.0], 'white')
]);
model('cw', 'orb', P, [
  solid([5.2, 5.2, 5.2], [10.8, 10.8, 10.8], 'water'), solid([4.4, 6.2, 6.2], [11.6, 9.8, 9.8], 'water'),
  solid([6.2, 4.4, 6.2], [9.8, 11.6, 9.8], 'water'), solid([6.2, 6.2, 4.4], [9.8, 9.8, 11.6], 'water'),
  solid([6.8, 6.8, 6.8], [9.2, 9.2, 9.2], 'waterB')
]);

// ---------------------------------------------------------------- textures + atlas
const tex = {'skin/mob_c3_em': skinMerc(), 'skin/mob_c3_cw': skinMage(), 'cm/c3/props': props()};
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
