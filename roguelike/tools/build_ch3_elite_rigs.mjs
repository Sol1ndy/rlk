// Chapter-3 elite rigs (part B): 성수 전갈 (cs), 성수 붉은 독수리 (rv), 원시 정령 기계·재구성자 (pc).
// Original block-model geometry, palette and keyframes authored for roguelike (Sumeru look); nothing is copied.
//
//   node tools/build_ch3_elite_rigs.mjs --resourcepack <unpacked resource pack>
//
// Writes (all owned by this generator):
//   RP  assets/rlk/textures/cm/c3e/pal.png              32x32 palette (16 swatches of 8x8, faint grain)
//       assets/rlk/models/item/cm/{cs,rv,pc}/*.json     part models (joint at [8,8,8])
//       assets/rlk/items/cm/{cs,rv,pc}/*.json           item definitions (custom_model_data tint 0 = hurt flash)
//       assets/minecraft/atlases/items.json             our sprite, filter-then-push by id (idempotent)
//   DP  tools/ch3_elite_poses.json                      runtime transforms of every pose; ch3mob/elite.py turns them into
//                                                       the rig/pose/<id> functions (functions are written by python only)
//
// Authoring space = Minecraft model space for the whole creature: forward = -Z (north), right = +X, up = +Y, units =
// model pixels at size 1, feet plane y = 0. Every part is a child of the root or of another part (joint offset + Euler
// rotation [x,y,z] degrees, applied x then y then z). The runtime item_display transform is that frame turned 180 deg
// about Y (vanilla's own Y180 on item displays), so the entity's facing (+Z at yaw 0) is the creature's forward.
// Every pose is checked: no visible geometry below the feet plane (a pose that dips is lifted by exactly that much).
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {png, hex, noise2} from './weapon_paint.mjs';

const base = path.dirname(fileURLToPath(import.meta.url));
const arg = n => { const i = process.argv.indexOf(n); return i < 0 ? undefined : process.argv[i + 1]; };
if (!arg('--resourcepack')) throw Error('Provide --resourcepack <unpacked resource pack>.');
const rpRoot = path.resolve(arg('--resourcepack'));
if (!fs.existsSync(path.join(rpRoot, 'pack.mcmeta'))) throw Error('resource pack must contain pack.mcmeta');
const rp = path.join(rpRoot, 'assets/rlk');
const put = (p, s) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, s); };
const json = (p, o) => put(p, JSON.stringify(o, null, 2) + '\n');

// ------------------------------------------------------------------ palette (16 swatches, 8x8 px each)
const PAL = {
  red: '#b04a32', dark: '#4a1c18', sand: '#d9b47c', rsand: '#b8693c',
  gold: '#d6ad4c', ele: '#c890ff', core: '#fff0c8', vred: '#b52e26',
  vdark: '#4e1414', bone: '#e9d9b4', flame: '#ff8a2a', fcore: '#ffe070',
  stone: '#ece6d8', stone2: '#b8ae9a', cyan: '#86f0e6', hot: '#ff5030'};
const SW = Object.fromEntries(Object.keys(PAL).map((k, i) => [k, i]));
const GLOWSW = new Set(['ele', 'core', 'flame', 'fcore', 'cyan', 'hot']);
{
  const N = noise2(31), buf = Buffer.alloc(32 * 32 * 4);
  const names = Object.keys(PAL);
  for (let y = 0; y < 32; y++) for (let x = 0; x < 32; x++) {
    const k = (y >> 3) * 4 + (x >> 3), name = names[k], c = hex(PAL[name]);
    const lx = x & 7, ly = y & 7;
    let g = 1;
    if (!GLOWSW.has(name)) {
      g = 0.93 + 0.12 * N(x * 0.9, y * 0.9);                                   // grain
      if (lx === 1 || ly === 1) g *= 1.05;                                      // soft top-left bevel
      if (lx === 6 || ly === 6) g *= 0.9;
    } else if (lx >= 3 && lx <= 4 && ly >= 3 && ly <= 4) g = 1.04;              // hot centre
    const o = (y * 32 + x) * 4;
    for (let i = 0; i < 3; i++) buf[o + i] = Math.max(0, Math.min(255, Math.round(c[i] * g)));
    buf[o + 3] = 255;
  }
  put(path.join(rp, 'textures/cm/c3e/pal.png'), png(32, 32, buf));
}
const swUV = name => { const k = SW[name], x = (k % 4) * 8, y = Math.floor(k / 4) * 8; return [(x + 1) / 2, (y + 1) / 2, (x + 7) / 2, (y + 7) / 2]; };

// element from two joint-relative corners (model px); tinted unless a glow swatch
function E(a, b, sw, o = {}) {
  const from = a.map((v, i) => +(Math.min(v, b[i]) + 8).toFixed(3)), to = a.map((v, i) => +(Math.max(v, b[i]) + 8).toFixed(3));
  for (const v of [...from, ...to]) if (v < -16 || v > 32) throw Error(`element outside the model box: ${a} ${b}`);
  const tint = !GLOWSW.has(sw) && !o.bright;
  const el = {from, to, faces: Object.fromEntries(['north', 'south', 'east', 'west', 'up', 'down']
    .map(f => [f, {texture: '#pal', uv: swUV(sw), ...(tint ? {tintindex: 0} : {})}]))};
  if (o.rot) el.rotation = {origin: o.rot[0].map(v => v + 8), axis: o.rot[1], angle: o.rot[2]};
  return el;
}
const mirrorX = els => els.map(e => {
  const m = {...e, from: [16 - e.to[0], e.from[1], e.from[2]], to: [16 - e.from[0], e.to[1], e.to[2]]};
  if (e.rotation) m.rotation = {...e.rotation, origin: [16 - e.rotation.origin[0], e.rotation.origin[1], e.rotation.origin[2]],
    angle: e.rotation.axis === 'x' ? e.rotation.angle : -e.rotation.angle};
  return m;
});
const bright = els => els.map(e => ({...e, faces: Object.fromEntries(Object.entries(e.faces).map(([k, f]) => {
  const {tintindex, ...rest} = f; return [k, rest];
}))}));

const MODELS = {};
function model(id, part, elements) {
  MODELS[`${id}/${part}`] = elements;
  json(path.join(rp, `models/item/cm/${id}/${part}.json`), {ambientocclusion: false, textures: {pal: 'rlk:cm/c3e/pal', particle: 'rlk:cm/c3e/pal'}, elements});
  const tint = elements.some(e => Object.values(e.faces).some(f => f.tintindex === 0));
  json(path.join(rp, `items/cm/${id}/${part}.json`), {model: {type: 'minecraft:model', model: `rlk:item/cm/${id}/${part}`,
    ...(tint ? {tints: [{type: 'minecraft:custom_model_data', index: 0, default: 16777215}]} : {})}});
}

// =================================================================================================== 성수 전갈
{
  const body = [
    E([-5, -3, -7], [5, -0.5, 6.5], 'dark'),                                   // belly
    E([-5.5, -1, -8], [5.5, 2, 7.5], 'red'),                                   // core
  ];
  const plates = [[-8.6, -4.9, 5.4], [-4.5, -0.9, 6.3], [-0.5, 3.1, 6.3], [3.5, 7.3, 5.5]];
  for (const [z0, z1, w] of plates) {
    body.push(E([-w, 1.6, z0], [w, 3.2, z1], 'red'));
    body.push(E([-w - 0.3, 0.8, z0 + 0.4], [-w + 0.6, 2.4, z1 - 0.4], 'rsand'));   // plate flanks
    body.push(E([w - 0.6, 0.8, z0 + 0.4], [w + 0.3, 2.4, z1 - 0.4], 'rsand'));
    body.push(E([-0.8, 3.2, z0 + 0.5], [0.8, 3.6, z1 - 0.5], 'gold'));            // consecrated midline
  }
  body.push(E([-3.2, 3.2, -3.4], [-2.2, 3.5, -2], 'gold'), E([2.2, 3.2, -3.4], [3.2, 3.5, -2], 'gold'),
    E([-3.2, 3.2, 0.6], [-2.2, 3.5, 2], 'gold'), E([2.2, 3.2, 0.6], [3.2, 3.5, 2], 'gold'));
  // prosoma (head) with glowing eyes, mandibles and a gold crest
  body.push(E([-4.6, -1.6, -12], [4.6, 2.6, -8], 'red'), E([-3.6, -1.1, -12.5], [3.6, 1.1, -12], 'dark'),
    E([-2.3, 2.6, -11.2], [-0.9, 3.3, -10], 'ele'), E([0.9, 2.6, -11.2], [2.3, 3.3, -10], 'ele'),
    E([-1, 2.6, -9.6], [1, 3.8, -8], 'gold'),
    E([-2.6, -1.6, -13.8], [-0.8, 0.1, -12], 'dark'), E([0.8, -1.6, -13.8], [2.6, 0.1, -12], 'dark'));
  model('cs', 'body', body);
  const seg = (w, l) => [E([-w, 0, -w], [w, l, w], 'red'), E([-w - 0.3, 0, -w - 0.3], [w + 0.3, 1, w + 0.3], 'dark'),
    E([-0.8, 1.5, w - 0.1], [0.8, l - 1, w + 0.4], 'gold')];
  model('cs', 't1', seg(3, 7.5));
  model('cs', 't2', seg(2.6, 7));
  model('cs', 't3', seg(2.3, 6.5));
  model('cs', 'sting', [E([-2.4, 0, -2.4], [2.4, 4, 2.4], 'vdark'), E([-2.6, 0, -2.6], [2.6, 0.8, 2.6], 'dark'),
    E([-0.7, 3.6, -0.7], [0.7, 7.8, 0.7], 'dark'), E([-0.45, 7.4, -1.9], [0.45, 8.3, -0.5], 'dark')]);
  model('cs', 'sglow', [E([-2.65, 1, -0.6], [2.65, 3, 0.6], 'ele'), E([-0.6, 1, -2.65], [0.6, 3, 2.65], 'ele'),
    E([-0.35, 5.6, -0.35], [0.35, 8.1, 0.35], 'ele'), E([-1.2, 4, -1.2], [1.2, 4.6, 1.2], 'ele')]);
  // right arm (+X side) reaches forward; claw: palm + outer fixed finger + stepped (open) inner finger
  const arm = [E([-1.7, -1.7, -7.5], [1.7, 1.7, 0], 'red'), E([-2.1, -2.1, -1.6], [2.1, 2.1, 1], 'dark'),
    E([-2, -1.4, -5], [2, 1.4, -4.2], 'dark')];
  model('cs', 'arm_r', arm);
  model('cs', 'arm_l', mirrorX(arm));
  const claw = [E([-3, -2.3, -6], [3, 2.7, 0.2], 'red'), E([-3.2, 1.6, -5.4], [3.2, 2.9, -0.4], 'rsand'),
    E([0.4, -1.7, -12], [3.1, 1.7, -6], 'red'), E([0.8, -1.3, -13.4], [2.7, 1.3, -12], 'dark'),
    E([-3.2, -1.5, -9], [-0.8, 1.5, -6], 'red'), E([-4.3, -1.2, -11.6], [-1.9, 1.2, -9], 'red'),
    E([-4.4, -1, -12.6], [-2.6, 1, -11.6], 'dark'), E([-0.6, 2.7, -4], [0.6, 3.1, -1], 'gold')];
  model('cs', 'claw_r', claw);
  model('cs', 'claw_l', mirrorX(claw));
  // legs (right side, outward +X): pair A = 1st + 3rd, pair B = 2nd + 4th
  const leg = z => [E([0, -0.6, z - 0.8], [3.6, 1, z + 0.8], 'red'), E([3, 0.4, z - 0.8], [6.6, 2.4, z + 0.8], 'red'),
    E([5.8, 1, z - 1], [7.7, 3.1, z + 1], 'dark'), E([6.6, -4, z - 0.75], [8.1, 1.4, z + 0.75], 'red'),
    E([6.9, -5.5, z - 0.5], [7.9, -4, z + 0.5], 'dark')];
  const legsA = [...leg(-5.5), ...leg(1)], legsB = [...leg(-2.2), ...leg(4.3)];
  model('cs', 'legs_ra', legsA); model('cs', 'legs_rb', legsB);
  model('cs', 'legs_la', mirrorX(legsA)); model('cs', 'legs_lb', mirrorX(legsB));
  // sand mound (burrow trail head / eruption tell): a low dome of sand and red sand
  model('cs', 'mound', [E([-10, 0, -7], [10, 1.2, 7], 'sand'), E([-7, 0, -10], [7, 1.2, 10], 'sand'),
    E([-7.5, 1.2, -6], [7.5, 2.5, 6], 'sand'), E([-5.5, 1.2, -7.5], [5.5, 2.5, 7.5], 'rsand'),
    E([-4.5, 2.5, -4], [4.5, 3.6, 4], 'sand'), E([-2, 3.6, -2.5], [2.5, 4.3, 1.5], 'rsand'),
    E([6, 1.2, 3], [8.5, 2, 5.5], 'rsand'), E([-8.5, 1.2, -4], [-6.5, 2, -1.5], 'rsand')]);
}

// =================================================================================================== 성수 붉은 독수리
{
  model('rv', 'body', [E([-4, -3.5, -6], [4, 3.5, 6], 'vred'), E([-3.4, -3.9, -5.6], [3.4, -1, 3], 'vdark'),
    E([-4.6, -0.5, -8.2], [4.6, 4.6, -4.8], 'bone'), E([-4.75, 1.4, -8.4], [4.75, 2.4, -7.6], 'gold'),
    E([-3.2, 3.5, -4.5], [3.2, 4.2, 4.5], 'vdark'), E([-0.6, 4.2, -3], [0.6, 4.5, 3], 'gold')]);
  model('rv', 'head', [E([-1.5, -1, -3], [1.5, 2.2, 0.5], 'bone'), E([-2.2, 1, -6.5], [2.2, 4.4, -2.5], 'bone'),
    E([-1.1, 1, -9.6], [1.1, 3, -6.5], 'gold'), E([-0.8, -0.2, -9.8], [0.8, 1.2, -8.5], 'dark'),
    E([-2.35, 3, -5.6], [-1.6, 3.8, -4.6], 'flame'), E([1.6, 3, -5.6], [2.35, 3.8, -4.6], 'flame'),
    E([-0.6, 4.4, -6], [0.6, 6.2, -2.4], 'vred'), E([-0.5, 5.2, -2.6], [0.5, 6.8, -1], 'vred')]);
  const w1 = [E([0, -0.8, -4], [10, 1.2, 6], 'vred'), E([0, 0.2, -4.6], [10, 1.9, -3], 'vdark'),
    E([1, 1.2, -2.5], [9, 1.6, 4], 'vred'), E([2, -1.1, 2], [9.5, -0.8, 6], 'vdark')];
  const w2 = [E([0, -0.6, -3.5], [10, 0.8, 5.5], 'vred'), E([6.5, -0.7, -3.5], [10, 0.9, 5.5], 'vdark')];
  for (let k = 0; k < 4; k++) w2.push(E([9.5, -0.4, -3 + 2.2 * k], [14.6 - 0.8 * k, 0.5, -1.4 + 2.2 * k], 'vdark'));
  const fl = [];
  for (let k = 0; k < 4; k++) {
    fl.push(E([-0.4 - 0.8 * k, -0.65, -3.15 + 2.2 * k], [2.6 - 0.8 * k, 0.75, -1.25 + 2.2 * k], 'flame'));
    fl.push(E([0.8 - 0.8 * k, -0.3, -2.75 + 2.2 * k], [3.6 - 0.8 * k, 0.4, -1.65 + 2.2 * k], 'fcore'));
    if (k % 2 === 0) fl.push(E([1.6 - 0.8 * k, -0.2, -2.6 + 2.2 * k], [4.4 - 0.8 * k, 0.3, -2 + 2.2 * k], 'flame'));
  }
  model('rv', 'wr1', w1); model('rv', 'wl1', mirrorX(w1));
  model('rv', 'wr2', w2); model('rv', 'wl2', mirrorX(w2));
  model('rv', 'flr', fl); model('rv', 'fll', mirrorX(fl));
  model('rv', 'tail', [E([-3.5, -0.6, 0], [3.5, 0.8, 6.5], 'vred'), E([-4.2, -0.7, 5], [4.2, 0.9, 8.5], 'vdark'),
    E([-3, -0.75, 7.8], [3, 0.95, 9.4], 'flame')]);
  model('rv', 'legs', [E([-2.6, -6, -0.8], [-1, 0, 0.8], 'bone'), E([1, -6, -0.8], [2.6, 0, 0.8], 'bone'),
    E([-3.1, -7, -2.2], [-0.5, -6, 1], 'dark'), E([0.5, -7, -2.2], [3.1, -6, 1], 'dark'),
    E([-3, -1, -1.6], [3, 1.4, 1.6], 'vred')]);
  // projectile: a burning feather (drawn bright), pointing along -Z (its flight direction after the vanilla Y180)
  model('rv', 'feather', bright([E([-0.3, -0.3, -5.5], [0.3, 0.3, 5], 'bone'), E([-1.7, -0.2, -3], [1.7, 0.2, 4.5], 'vred'),
    E([-1.2, -0.25, -5], [1.2, 0.25, -2.6], 'flame'), E([-0.6, -0.3, -6.2], [0.6, 0.3, -4.6], 'fcore')]));
}

// =================================================================================================== 원시 정령 기계·재구성자
{
  const cubeT = (h, sw = 'stone') => [E([-h, -h, -h], [h, h, h], sw), E([-h - 0.2, h - 0.6, -h - 0.2], [h + 0.2, h + 0.2, h + 0.2], 'gold')];
  model('pc', 'core', [E([-2.6, -2.6, -2.6], [2.6, 2.6, 2.6], 'core'), E([-3.6, -1.1, -1.1], [3.6, 1.1, 1.1], 'core'),
    E([-1.1, -3.6, -1.1], [1.1, 3.6, 1.1], 'core'), E([-1.1, -1.1, -3.6], [1.1, 1.1, 3.6], 'core'),
    E([-1.8, -1.8, -3.1], [1.8, 1.8, 3.1], 'fcore')]);
  model('pc', 'core_hot', [E([-2.6, -2.6, -2.6], [2.6, 2.6, 2.6], 'hot'), E([-3.8, -1.1, -1.1], [3.8, 1.1, 1.1], 'flame'),
    E([-1.1, -3.8, -1.1], [1.1, 3.8, 1.1], 'flame'), E([-1.1, -1.1, -3.8], [1.1, 1.1, 3.8], 'flame'),
    E([-1.8, -1.8, -3.2], [1.8, 1.8, 3.2], 'fcore')]);
  const chest = [E([0.6, -5, 1.6], [6.5, 6, 5], 'stone'), E([3.8, -4.2, -3.4], [7.6, 5, 2], 'stone'),
    E([0.6, 3.6, -5], [5.4, 6.6, -1.4], 'stone'), E([0.6, -6.2, -4.6], [4.4, -3.4, -1], 'stone2'),
    E([0.4, 5.6, 1.4], [6.7, 6.4, 5.2], 'gold'), E([3.6, 4.6, -3.6], [7.8, 5.3, 2.2], 'gold'),
    E([4.2, 0.4, -3.6], [6, 1.2, -3.3], 'cyan'), E([1.4, 4.4, -5.3], [4.6, 5.2, -5], 'cyan')];
  model('pc', 'chest_r', chest); model('pc', 'chest_l', mirrorX(chest));
  model('pc', 'head', [E([-3.5, 0, -3.5], [3.5, 6, 3.5], 'stone'), E([-2.6, 2.4, -3.8], [2.6, 3.4, -3.4], 'cyan'),
    E([-3.7, 5.4, -3.7], [3.7, 6.3, 3.7], 'gold'), E([-1, 6.3, -1], [1, 7.6, 1], 'gold')]);
  model('pc', 'sh_r', [...cubeT(3), E([3, -1, -1], [3.3, 1, 1], 'cyan')]);
  model('pc', 'sh_l', mirrorX([...cubeT(3), E([3, -1, -1], [3.3, 1, 1], 'cyan')]));
  model('pc', 'arm_l', [E([-2.2, -7, -2.2], [2.2, 0, 2.2], 'stone'), E([-2.9, -11.4, -2.9], [2.9, -7, 2.9], 'stone2'),
    E([-3, -8, -3], [3, -7.4, 3], 'gold')]);
  model('pc', 'hammer', [E([-2.2, -5, -2.2], [2.2, 0, 2.2], 'stone'), E([-5, -14.5, -5], [5, -5, 5], 'stone'),
    E([-5.2, -10.4, -5.2], [5.2, -9.2, 5.2], 'gold'), E([-5.15, -13.5, -1], [-4.9, -6, 1], 'cyan'),
    E([4.9, -13.5, -1], [5.15, -6, 1], 'cyan'), E([-1, -13.5, -5.15], [1, -6, -4.9], 'cyan'),
    E([-4, -15.2, -4], [4, -14.5, 4], 'stone2')]);
  model('pc', 'base', [E([-5, -3, -4], [5, 2, 4], 'stone2'), E([-5.2, 1.4, -4.2], [5.2, 2.2, 4.2], 'gold'),
    E([-6.5, -7.5, -2.2], [-2.5, -3.5, 2.2], 'stone'), E([2.5, -7.5, -2.2], [6.5, -3.5, 2.2], 'stone')]);
  model('pc', 'cube', [...cubeT(1.7), E([-0.6, -0.6, -1.95], [0.6, 0.6, -1.75], 'cyan')]);
}

// atlas: our sprite, filter-then-push by id
{
  const atlasPath = path.join(rpRoot, 'assets/minecraft/atlases/items.json');
  const atlas = fs.existsSync(atlasPath) ? JSON.parse(fs.readFileSync(atlasPath, 'utf8')) : {sources: []};
  for (const res of ['rlk:cm/c3e/pal']) {
    atlas.sources = atlas.sources.filter(s => (s.sprite || s.resource) !== res);
    atlas.sources.push({type: 'minecraft:single', resource: res});
  }
  json(atlasPath, atlas);
}

// ------------------------------------------------------------------ pose math
const rad = x => x * Math.PI / 180;
function mul(a, b) { const [x, y, z, w] = a, [X, Y, Z, W] = b; return [w * X + x * W + y * Z - z * Y, w * Y - x * Z + y * W + z * X, w * Z + x * Y - y * X + z * W, w * W - x * X - y * Y - z * Z]; }
function q(e = [0, 0, 0]) { const [x, y, z] = e.map(a => rad(a) / 2); return mul(mul([0, 0, Math.sin(z), Math.cos(z)], [0, Math.sin(y), 0, Math.cos(y)]), [Math.sin(x), 0, 0, Math.cos(x)]); }
function rot(a, v) { return mul(mul(a, [...v, 0]), [-a[0], -a[1], -a[2], a[3]]).slice(0, 3); }
const add = (a, b) => a.map((v, i) => v + b[i]);
const fl = v => { const x = Math.abs(v) < 5e-7 ? 0 : Number(v.toFixed(5)); return x; };

// skeleton: part -> {parent, at (px, parent frame), r0 (rest Euler), model}
// pose: {dur, root: {t, r}, P: {part: {r, t, s}}, model: {part: modelName}}
function solve(sk, size, pose) {
  const W = {};
  const rootQ = q(pose.root?.r), rootT = pose.root?.t || [0, 0, 0];
  const done = part => {
    if (W[part]) return W[part];
    const s = sk[part], p = pose.P?.[part] || {};
    const par = s.parent ? done(s.parent) : {t: rootT, q: rootQ};
    const at = add(s.at, p.t || [0, 0, 0]);
    const t = add(par.t, rot(par.q, at));
    const qq = mul(mul(par.q, q(s.r0 || [0, 0, 0])), q(p.r || [0, 0, 0]));
    W[part] = {t, q: qq, s: p.S ?? (p.s ?? 1) * (pose.s ?? 1)};
    return W[part];
  };
  for (const part of Object.keys(sk)) done(part);
  // a whole-pose scale (sinking into the sand, fading) shrinks the creature toward its feet point, not each part in place
  if (pose.s !== undefined) for (const part of Object.keys(sk)) if (pose.P?.[part]?.S === undefined) W[part].t = W[part].t.map(v => v * pose.s);
  return W;
}
function minYpx(modelKey, w) {
  let m = Infinity;
  for (const e of MODELS[modelKey]) for (const x of [e.from[0], e.to[0]]) for (const y of [e.from[1], e.to[1]]) for (const z of [e.from[2], e.to[2]]) {
    const v = rot(w.q, [(x - 8) * w.s, (y - 8) * w.s, (z - 8) * w.s]);
    m = Math.min(m, v[1] + w.t[1]);
  }
  return m;
}
const OUT = {};
function rigSet(id, sk, size, poses, defaults = {}) {
  const parts = Object.keys(sk);
  const list = [];
  for (const [pid, name, dur, pose0] of poses) {
    const pose = {...pose0, P: {...defaults, ...(pose0.P || {})}};
    for (const [k, v] of Object.entries(defaults)) if (pose0.P?.[k]) pose.P[k] = {...v, ...pose0.P[k]};
    const W = solve(sk, size, pose);
    const mk = part => `${id}/${pose.model?.[part] || sk[part].model || part}`;
    let lo = Infinity;
    for (const part of parts) if (W[part].s > 0) lo = Math.min(lo, minYpx(mk(part), W[part]));
    if (lo < 0 && !pose.air) for (const part of parts) W[part].t[1] -= lo;
    for (const part of parts) if (!pose.air && W[part].s > 0 && minYpx(mk(part), W[part]) < -1e-4) throw Error(`${id} pose ${pid} ${name}: ${part} below the feet`);
    const rig = {};
    for (const part of parts) {
      const w = W[part], k = size / 16;
      rig[part] = {t: [-w.t[0] * k, w.t[1] * k, -w.t[2] * k].map(fl), q: [-w.q[0], w.q[1], -w.q[2], w.q[3]].map(fl), s: [w.s * size, w.s * size, w.s * size].map(fl)};
    }
    const entry = {id: pid, name, dur, rig};
    const swaps = Object.fromEntries(Object.entries(pose.model || {}).map(([p, m]) => [p, `rlk:cm/${id}/${m}`]));
    if (Object.keys(swaps).length) entry.model = swaps;
    list.push(entry);
  }
  OUT[id] = {parts, models: Object.fromEntries(parts.map(p => [p, `rlk:cm/${id}/${sk[p].model || p}`])), poses: list};
}
const S = Math.sin, C = Math.cos, PI = Math.PI;

// ---- 성수 전갈: size 1.45 (16 px = 1.45 b). Body 0.63 b up on four leg pairs, tail arched over the back.
{
  const sk = {
    body: {at: [0, 7, 0]},
    legs_ra: {parent: 'body', at: [5, -1.5, 0]}, legs_rb: {parent: 'body', at: [5, -1.5, 0]},
    legs_la: {parent: 'body', at: [-5, -1.5, 0]}, legs_lb: {parent: 'body', at: [-5, -1.5, 0]},
    arm_r: {parent: 'body', at: [4.5, 0, -10.5], r0: [8, -26, 0]}, arm_l: {parent: 'body', at: [-4.5, 0, -10.5], r0: [8, 26, 0]},
    claw_r: {parent: 'arm_r', at: [0, 0, -7.5], r0: [0, 22, 0]}, claw_l: {parent: 'arm_l', at: [0, 0, -7.5], r0: [0, -22, 0]},
    t1: {parent: 'body', at: [0, 1.2, 7.2], r0: [48, 0, 0]}, t2: {parent: 't1', at: [0, 7.5, 0], r0: [-14, 0, 0]},
    t3: {parent: 't2', at: [0, 7, 0], r0: [-58, 0, 0]}, sting: {parent: 't3', at: [0, 6.5, 0], r0: [-60, 0, 0]},
    sglow: {parent: 'sting', at: [0, 0, 0]},
    mound: {at: [0, 0, 0]},
  };
  const D = {mound: {s: 0}};
  const P = [];
  const tailD = (a, b, c, d) => ({t1: {r: [a, 0, 0]}, t2: {r: [b, 0, 0]}, t3: {r: [c, 0, 0]}, sting: {r: [d, 0, 0]}});
  const tail = (a, b, c, d) => tailD(a - 48, b + 14, c + 58, d + 60);   // absolute joint angles
  for (let i = 0; i < 4; i++) {
    const s = S(i * PI / 2);
    P.push([i, 'idle_' + i, 6, {P: {body: {t: [0, s * 0.35, 0]}, ...tailD(s * 3, 0, s * 4, -s * 3),
      arm_r: {r: [s * 4, 0, 0]}, arm_l: {r: [-s * 4, 0, 0]}, claw_r: {r: [0, s * 4, 0]}, claw_l: {r: [0, -s * 4, 0]}}}]);
  }
  for (let i = 0; i < 8; i++) {
    const a = i * PI / 4, s = S(a), lift = Math.max(0, s) * 0.9, lift2 = Math.max(0, -s) * 0.9;
    P.push([10 + i, 'walk_' + i, 3, {P: {body: {t: [0, Math.abs(C(a)) * 0.3, 0], r: [0, s * 3, 0]},
      legs_ra: {r: [0, 13 * s, 0], t: [0, lift, 0]}, legs_lb: {r: [0, -13 * s, 0], t: [0, lift, 0]},
      legs_rb: {r: [0, -13 * s, 0], t: [0, lift2, 0]}, legs_la: {r: [0, 13 * s, 0], t: [0, lift2, 0]},
      arm_r: {r: [s * 5, 0, 0]}, arm_l: {r: [-s * 5, 0, 0]}, ...tailD(0, 0, s * 5, 0)}}]);
  }
  // burrow: crouch -> squash into the sand -> hidden (only the travelling mound)
  P.push([20, 'dig_crouch', 3, {P: {body: {t: [0, -2.2, 0], r: [9, 0, 0]}, arm_r: {r: [-25, 10, 0]}, arm_l: {r: [-25, -10, 0]},
    ...tail(75, -10, -10, -10), mound: {S: 0.4}}}]);
  P.push([21, 'dig_sink', 5, {s: 0.45, P: {body: {t: [0, -4, 0], r: [12, 0, 0]}, ...tail(85, 0, 0, 0), mound: {S: 0.9}}}]);
  P.push([22, 'under', 2, {s: 0, P: {mound: {S: 0.6}}}]);
  P.push([23, 'mound_a', 2, {s: 0, P: {mound: {S: 1.5, r: [5, 0, 4]}}}]);
  P.push([24, 'mound_b', 2, {s: 0, P: {mound: {S: 1.62, r: [-5, 0, -4]}}}]);
  P.push([25, 'erupt', 2, {root: {t: [0, 5, 3], r: [38, 0, 0]}, P: {arm_r: {r: [55, -25, -15]}, arm_l: {r: [55, 25, 15]},
    claw_r: {r: [10, 15, 0]}, claw_l: {r: [10, -15, 0]}, ...tail(20, -20, -40, -60)}}]);
  P.push([26, 'erupt_land', 3, {root: {r: [-6, 0, 0]}, P: {body: {t: [0, -1.4, 0]}, arm_r: {r: [-20, 0, 0]}, arm_l: {r: [-20, 0, 0]}}}]);
  for (const [k, z, h] of [[27, 7, 1], [28, -7, -1]])
    P.push([k, 'stuck_' + (k - 26), 8, {P: {body: {t: [0, -1.8, 0], r: [-4, 0, z]}, arm_r: {r: [-22, -8 * h, 0]}, arm_l: {r: [-22, -8 * h, 0]},
      claw_r: {r: [0, 10, 0]}, claw_l: {r: [0, -10, 0]}, ...tail(80, -10, -15 + 4 * h, -20), sglow: {s: 0.5}}}]);
  // pincer combo
  P.push([30, 'pinch_tell', 3, {P: {body: {r: [-7, 0, 0], t: [0, 0.6, 1]}, arm_r: {r: [38, -40, 0]}, arm_l: {r: [38, 40, 0]},
    claw_r: {r: [-12, 30, 0]}, claw_l: {r: [-12, -30, 0]}, ...tail(42, -12, -55, -62)}}]);
  P.push([31, 'pinch_1', 2, {P: {body: {r: [6, -10, 0], t: [0, 0, -1.5]}, arm_r: {r: [-4, 20, 0]}, claw_r: {r: [0, -10, 0]},
    arm_l: {r: [38, 40, 0]}, claw_l: {r: [-12, -30, 0]}}}]);
  P.push([32, 'pinch_2', 2, {P: {body: {r: [6, 10, 0], t: [0, 0, -1.8]}, arm_l: {r: [-4, -20, 0]}, claw_l: {r: [0, 10, 0]},
    arm_r: {r: [20, -20, 0]}}}]);
  P.push([33, 'pinch_rec', 4, {P: {body: {r: [3, 0, 0]}}}]);
  // tail stab
  P.push([40, 'tail_tell', 3, {P: {body: {r: [-6, 0, 0], t: [0, 0.4, 1.2]}, ...tail(32, 6, -50, -98), sting: {r: [-98 + 60, 0, 0], s: 1.2},
    sglow: {s: 1.45}, arm_r: {r: [15, -10, 0]}, arm_l: {r: [15, 10, 0]}}}]);
  P.push([41, 'tail_stab', 2, {root: {t: [0, 0, -3]}, P: {body: {r: [8, 0, 0]}, ...tail(-14, -58, -30, -12), sting: {r: [-12 + 60, 0, 0], s: 1.15},
    sglow: {s: 1.3}, arm_r: {r: [-10, -15, 0]}, arm_l: {r: [-10, 15, 0]}}}]);
  P.push([42, 'tail_rec', 5, {P: {...tail(50, -30, -45, -50)}}]);
  P.push([50, 'hit_recoil', 2, {root: {t: [0, 0, 1.5]}, P: {body: {r: [-7, 0, 0]}, ...tail(66, -24, -50, -55)}}]);
  P.push([51, 'hit_recover', 3, {root: {t: [0, 0, 0.6]}, P: {body: {r: [-3, 0, 0]}}}]);
  // death: legs splay -> flips belly-up -> curls -> fades
  P.push([60, 'death_slump', 3, {P: {body: {t: [0, -2.5, 0], r: [6, 0, 8]}, legs_ra: {r: [0, 0, 20]}, legs_rb: {r: [0, 0, 20]},
    legs_la: {r: [0, 0, -20]}, legs_lb: {r: [0, 0, -20]}, ...tail(85, -10, -10, -10), sglow: {s: 0.4}}}]);
  P.push([61, 'death_flip', 5, {root: {r: [0, 0, 100]}, P: {...tail(88, 0, 0, 0), sglow: {s: 0.3}}}]);
  P.push([62, 'death_belly', 5, {root: {r: [0, 0, 178]}, P: {legs_ra: {r: [0, 0, -35]}, legs_rb: {r: [0, 0, -35]},
    legs_la: {r: [0, 0, 35]}, legs_lb: {r: [0, 0, 35]}, ...tail(92, 2, 2, 0), arm_r: {r: [-10, 0, 0]}, arm_l: {r: [-10, 0, 0]}, sglow: {s: 0.2}}}]);
  P.push([63, 'death_fade', 6, {s: 0.05, root: {r: [0, 0, 178]}, P: {...tail(92, 2, 2, 0)}}]);
  rigSet('cs', sk, 1.45, P, D);
}

// ---- 성수 붉은 독수리: size 1.25. The brain hovers; the rig's feet anchor is the brain position.
{
  const sk = {
    body: {at: [0, 11, 0]},
    head: {parent: 'body', at: [0, 2.6, -7.6]},
    wr1: {parent: 'body', at: [4, 2, -2]}, wl1: {parent: 'body', at: [-4, 2, -2]},
    wr2: {parent: 'wr1', at: [10, 0, 0]}, wl2: {parent: 'wl1', at: [-10, 0, 0]},
    flr: {parent: 'wr2', at: [14, 0, 0]}, fll: {parent: 'wl2', at: [-14, 0, 0]},
    tail: {parent: 'body', at: [0, 0.5, 6], r0: [-8, 0, 0]},
    legs: {parent: 'body', at: [0, -3.4, 1.5]},
  };
  const wings = (a, b, sw = 0, sw2 = 0, fs = 1) => ({wr1: {r: [0, sw, a]}, wl1: {r: [0, -sw, -a]}, wr2: {r: [0, sw2, b]}, wl2: {r: [0, -sw2, -b]},
    flr: {s: fs}, fll: {s: fs}});
  const P = [];
  const flap = [[42, 22, 0.8], [12, 6, 0], [-28, -16, -0.9], [8, -6, 0]];
  flap.forEach(([a, b, y], i) => P.push([i, 'flap_' + i, 3, {air: true, root: {t: [0, y, 0], r: [4, 0, 0]},
    P: {...wings(a, b, i === 2 ? -6 : 0), legs: {r: [55, 0, 0]}, head: {r: [-6 + y * 3, 0, 0]}}}]));
  P.push([10, 'shriek', 3, {air: true, root: {r: [22, 0, 0], t: [0, 1, 0]}, P: {...wings(72, 30, 10, 0, 1.35), head: {r: [42, 0, 0]}, legs: {r: [50, 0, 0]},
    tail: {r: [-20, 0, 0]}}}]);
  P.push([11, 'aim', 3, {air: true, root: {r: [-24, 0, 0]}, P: {...wings(24, 4, -32, -10, 1.2), head: {r: [-12, 0, 0]}, legs: {r: [20, 0, 0]}}}]);
  P.push([12, 'dive', 2, {air: true, root: {r: [-44, 0, 0]}, P: {...wings(16, 0, -62, -40, 1.5), head: {r: [8, 0, 0]}, legs: {r: [-55, 0, 0]},
    tail: {r: [10, 0, 0]}}}]);
  for (const [k, h] of [[20, 1], [21, -1]])
    P.push([k, 'crashed_' + (k - 19), 7, {root: {t: [0, -6.8, 0], r: [-12, 0, 16 * h]}, P: {...wings(-12, -8, 15, 10, 0.55),
      wl1: {r: [0, -15, 10]}, wl2: {r: [0, -10, 6]}, head: {r: [-28, 22 * h, 0]}, legs: {r: [70, 0, 0]}, tail: {r: [6, 0, 0]}}}]);
  P.push([22, 'takeoff', 3, {air: true, root: {r: [16, 0, 0], t: [0, 1.5, 0]}, P: {...wings(62, 28, 0, 0, 1.1), legs: {r: [20, 0, 0]}}}]);
  P.push([30, 'fan_tell', 3, {air: true, root: {r: [12, 0, 0]}, P: {...wings(26, 10, 34, 18, 1.75), head: {r: [22, 0, 0]}, legs: {r: [50, 0, 0]}}}]);
  P.push([31, 'fan_release', 2, {air: true, root: {r: [-10, 0, 0]}, P: {...wings(-18, -10, 46, 26, 1.3), head: {r: [-8, 0, 0]}, legs: {r: [50, 0, 0]}}}]);
  P.push([50, 'hit_recoil', 2, {air: true, root: {r: [14, 0, 0], t: [0, 0.4, 1.2]}, P: {...wings(30, 10), legs: {r: [55, 0, 0]}}}]);
  P.push([51, 'hit_recover', 3, {air: true, root: {r: [7, 0, 0]}, P: {...wings(20, 8), legs: {r: [55, 0, 0]}}}]);
  P.push([52, 'g_recoil', 2, {root: {t: [0, -6.4, 1], r: [-4, 0, 10]}, P: {...wings(-6, -4, 15, 10, 0.55), head: {r: [-10, 0, 0]}, legs: {r: [70, 0, 0]}}}]);
  P.push([60, 'death_fall', 3, {air: true, root: {r: [-20, 0, 40]}, P: {...wings(55, 20, -30, -20, 0.4), head: {r: [-40, 0, 0]}, legs: {r: [10, 0, 0]}}}]);
  P.push([61, 'death_ground', 4, {root: {r: [-8, 0, 14], t: [0, -8, 0]}, P: {...wings(-10, -6, 10, 6, 0.25), head: {r: [-35, 34, 0]}, legs: {r: [70, 0, 0]}}}]);
  P.push([62, 'death_fade', 6, {s: 0.05, root: {r: [-8, 0, 14], t: [0, -8, 0]}, P: {flr: {s: 0}, fll: {s: 0}}}]);
  rigSet('rv', sk, 1.25, P);
}

// ---- 원시 정령 기계·재구성자: size 1.2. Floating white-gold blocks around a glowing core; the cubes orbit.
{
  const ORB = 4, R = 13;
  const sk = {
    core: {at: [0, 19, 0]}, chest_r: {at: [0, 19, 0]}, chest_l: {at: [0, 19, 0]}, head: {at: [0, 26.5, 0]},
    sh_r: {at: [10.5, 23, 0]}, sh_l: {at: [-10.5, 23, 0]},
    hammer: {parent: 'sh_r', at: [0, -3.6, 0]}, arm_l: {parent: 'sh_l', at: [0, -3.6, 0]},
    base: {at: [0, 9.5, 0]},
  };
  for (let k = 0; k < ORB; k++) sk['o' + k] = {at: [0, 0, 0], model: 'cube'};
  const orb = (ang, r = R, y0 = 17, dy = 3, sc = 1) => {
    const o = {};
    for (let k = 0; k < ORB; k++) {
      const a = rad(ang + 90 * k);
      o['o' + k] = {t: [r * C(a), y0 + dy * S(a * 2 + k), r * S(a)], r: [0, ang + 30 * k, 22], s: sc};
    }
    return o;
  };
  const bob = (i, amp = 0.6) => ({head: {t: [0, amp * S(i * PI / 4), 0]}, sh_r: {t: [0, amp * S(i * PI / 4 + 1), 0]},
    sh_l: {t: [0, amp * S(i * PI / 4 + 2), 0]}, base: {t: [0, amp * 0.7 * S(i * PI / 4 + 3), 0]}, core: {r: [0, i * 45, 0]}});
  const P = [];
  for (let i = 0; i < 8; i++) P.push([i, 'idle_' + i, 4, {P: {...bob(i), ...orb(i * 45), hammer: {r: [S(i * PI / 4) * 4, 0, 0]}}}]);
  for (let i = 0; i < 8; i++) {
    const s = S(i * PI / 4);
    P.push([10 + i, 'glide_' + i, 3, {root: {r: [-6, 0, s * 3]}, P: {...bob(i, 0.9), ...orb(i * 45, 12), hammer: {r: [s * 12, 0, 0]},
      arm_l: {r: [-s * 12, 0, 0]}, base: {t: [0, 0.5, 1.5]}}}]);
  }
  const spread = (k, up = 0, sc = 0.7) => {
    const o = {};
    for (const [p, v] of Object.entries({head: [0, 9, -2], chest_r: [6, 2, -3], chest_l: [-6, 2, 3], sh_r: [12, 5, 4], sh_l: [-12, 5, -4],
      base: [3, -1, 10]})) o[p] = {t: v.map((x, i) => x * k + (i === 1 ? up : 0)), s: sc, r: [k * 25, k * 40, 0]};
    return o;
  };
  P.push([20, 'scatter', 6, {P: {...spread(1.5, 3), ...orb(30, 26, 22, 4, 0.7), core: {s: 0.5}}}]);
  P.push([21, 'gather_hi', 1, {P: {...spread(1.8, 18, 0.55), ...orb(80, 28, 34, 3, 0.6), core: {s: 0.6, t: [0, 10, 0]}}}]);
  P.push([22, 'gather', 8, {P: {...orb(160, 15, 19, 2, 1), core: {s: 1.15}}}]);
  // hammer slam (right arm); the ring is drawn by the function in front of it
  P.push([30, 'slam_raise', 5, {root: {r: [10, 0, 0]}, P: {...bob(0), sh_r: {r: [168, 0, 18], t: [0, 2, 1]}, sh_l: {r: [30, 0, -20]},
    ...orb(20, 14, 22, 2), head: {r: [12, 0, 0]}}}]);
  P.push([31, 'slam_hit', 2, {root: {r: [-18, 0, 0], t: [0, 0, -2]}, P: {sh_r: {r: [72, 8, 6], t: [0, -2, -3]}, sh_l: {r: [-20, 0, -10]},
    ...orb(60, 16, 12, 1), head: {r: [-10, 0, 0]}}}]);
  P.push([32, 'slam_rec', 6, {root: {r: [-6, 0, 0]}, P: {sh_r: {r: [40, 0, 6]}, ...orb(90, 13)}}]);
  // cube spin
  P.push([40, 'spin_tell', 4, {root: {t: [0, 1.5, 0]}, P: {sh_r: {r: [0, 0, 84]}, sh_l: {r: [0, 0, -84]}, ...orb(0, 20, 18, 1),
    core: {s: 1.25}}}]);
  for (const [k, a] of [[41, 120], [42, 240], [43, 355]])
    P.push([k, 'spin_' + a, 2, {root: {r: [0, a, 0], t: [0, 1.5, 0]}, P: {sh_r: {r: [0, 0, 84]}, sh_l: {r: [0, 0, -84]}, ...orb(a, 22, 15, 1),
      core: {s: 1.25}}}]);
  P.push([44, 'spin_end', 4, {P: {sh_r: {r: [0, 0, 40]}, sh_l: {r: [0, 0, -40]}, ...orb(30, 15)}}]);
  // overheated: the chest halves slide open, the core swells red-hot, the cubes sag (core exposed = x1.5 damage)
  for (const [k, cs] of [[50, 1.65], [51, 1.45]])
    P.push([k, 'overheat_' + (k - 49), 6, {model: {core: 'core_hot'}, root: {t: [0, -2, 0]}, P: {chest_r: {t: [5.5, -0.5, 1], r: [0, -18, 0]},
      chest_l: {t: [-5.5, -0.5, 1], r: [0, 18, 0]}, head: {t: [0, 3.5, 1.5], r: [-18, 0, 0]}, sh_r: {t: [2.5, -3, 0], r: [10, 0, 25]},
      sh_l: {t: [-2.5, -3, 0], r: [10, 0, -25]}, core: {s: cs}, ...orb(k * 9, 14, 6, 1, 0.9)}}]);
  P.push([55, 'hit_recoil', 2, {root: {r: [10, 0, 0], t: [0, 0, 1.2]}, P: {...orb(10, 14)}}]);
  P.push([56, 'hit_recover', 3, {root: {r: [4, 0, 0]}, P: {...orb(20, 13)}}]);
  // death: every block drops to the floor around the dimming core, then fades
  const drop = {core: {t: [0, -16, 0], s: 0.55}, chest_r: {t: [5, -15, -3], r: [0, 30, 80]}, chest_l: {t: [-6, -15.5, 2], r: [0, -20, -80]},
    head: {t: [3, -23, -7], r: [20, 40, 0]}, sh_r: {t: [4, -19, 5], r: [30, 0, 40]}, sh_l: {t: [-5, -19, -4], r: [10, 30, 0]},
    hammer: {r: [0, 0, 0]}, base: {t: [0, -5.5, 0]}};
  P.push([60, 'collapse', 6, {P: {...drop, ...orb(45, 15, 2, 0, 1)}}]);
  P.push([61, 'fade', 6, {s: 0.05, P: {...drop, ...orb(45, 15, 2, 0, 1)}}]);
  rigSet('pc', sk, 1.2, P);
}

fs.writeFileSync(path.join(base, 'ch3_elite_poses.json'), JSON.stringify({
  authoring: 'Original keyframes for the chapter-3 elites (build_ch3_elite_rigs.mjs); 20 ticks/second.',
  space: 'Runtime item_display transformations: +Z forward, right hand on -X (vanilla Y180 applies after).', mobs: OUT}, null, 1) + '\n');
console.log(JSON.stringify({models: Object.keys(MODELS).length, parts: Object.fromEntries(Object.entries(OUT).map(([k, v]) => [k, v.parts.length])),
  poses: Object.fromEntries(Object.entries(OUT).map(([k, v]) => [k, v.poses.length])), texturePixels: 32 * 32}));
