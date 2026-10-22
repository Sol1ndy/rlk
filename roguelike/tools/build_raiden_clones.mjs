// The 찰나의 포영 clones (rd-sync): animated copies of Raiden built from the rig's own part models, so their arms
// and katana stay joined in every pose (the baked clone props turned each skin box about its own corner with
// +-22.5 / 45 degree element rotations, so the forearms floated off the upper arms and the katana was missing).
//
// node tools/build_raiden_clones.mjs --resourcepack <unpacked pack> [--datapack <pack>]      (after build_raiden_rig.mjs)
//
// RP  assets/rlk/models/item/raiden/clone/<model>.json   the rig part models with tintindex 0 on every face
//     assets/rlk/items/raiden/clone/{dark,glow}/<model>.json   constant tints (dark smoky violet / the revealed glow)
// DP  boss/raiden/clone/summon {id}           as a clone husk at its feet: its 14 part displays (rlk_rd_clp), each
//                                              carrying its own pose table (custom_data P.<pose>) and model ids
//     boss/raiden/clone/pose {sel,p,d,look}    every part of the clones matching `sel` (a selector argument, e.g.
//                                              tag=rlk_rd_clfake) eases to pose p over d ticks in look dark|glow
// Cost: 14 displays per clone (56 for the pattern), 3 commands per part per pose change, no new texture.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {solve, toDisplay} from './raiden_geometry.mjs';
import {POSES, DEFAULT_POSE, withBlade} from './raiden_clips.mjs';
import {written} from './mboss_rig_compile.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const arg = n => { const i = process.argv.indexOf(n); return i < 0 ? null : process.argv[i + 1]; };
const dp = path.resolve(arg('--datapack') || path.join(here, '..'));
const rp = arg('--resourcepack') && path.resolve(arg('--resourcepack'));
if (!rp) throw new Error('--resourcepack <unpacked pack> is required');
const put = (p, s) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, s.endsWith('\n') ? s : s + '\n'); };

// part -> rig model (the sword look)
const PARTS = {head: 'head', body: 'body', right_arm: 'right_arm', right_forearm: 'right_forearm', left_arm: 'left_arm',
  left_forearm: 'left_forearm', right_leg: 'right_leg', right_shin: 'right_shin', left_leg: 'left_leg', left_shin: 'left_shin',
  braid: 'braid', drape: 'drape', weapon: 'katana', weapon_fx: 'katana_fx'};
const TINT = {dark: 0x3a2a5a, glow: 0xd8b8ff};
const {S_IDLE, S_RAISE, S_DRAWN, S_CHOP} = POSES;
// The cuts (bearings of the katana tip about her feet, + = her right): the diagonal from her upper right to her lower
// left (every clone, volley tick V), and the real one's second stroke from her upper left to her lower right (V + 4):
// an X. `cross_*` is the blade at her facing, chest high: the wave leaves it there.
const CROSS = {...S_DRAWN, torso: [-10, 0, 0], head: [-4, 0, 0], armR: [86, 0, 10], elbowR: 6, armL: [60, 0, 10], elbowL: 20};
export const CLONE_POSES = {
  idle: {...S_IDLE},
  ready: withBlade({...S_RAISE, torso: [6, 0, 0]}, [10, 75], [0, 165]),                                   // raised, the glint
  high_r: withBlade({...S_RAISE, torso: [4, 24, 0], head: [-2, -14, 0], armR: [150, 0, 60], elbowR: 14, armL: [120, 0, 30], elbowL: 30}, [60, 48], [-120, -30]),
  cross_d: withBlade(CROSS, [0, 4], [-45, -45]),
  low_l: withBlade({...S_CHOP, torso: [-18, -28, 0], head: [-6, 20, 0], armR: [50, 0, -30], elbowR: 8, armL: [40, 0, 10]}, [-55, -38], [-90, -60]),
  high_l: withBlade({...S_RAISE, torso: [4, -40, 0], head: [-2, 26, 0], armR: [120, 0, -60], elbowR: 30, armL: [100, 0, 40], elbowL: 30}, [-80, 40], [110, -30]),
  cross_x: withBlade(CROSS, [0, 4], [45, -45]),
  low_r: withBlade({...S_CHOP, torso: [-18, 26, 0], head: [-6, -20, 0], armR: [46, 0, 50], elbowR: 8, armL: [40, 0, 10]}, [55, -38], [90, -60]),
  rest: {...S_IDLE, torso: [-4, -6, 0]},
};
const WFX = {ready: .8, high_r: .9, cross_d: 1, low_l: .7, high_l: .9, cross_x: 1, low_r: .7};

// ---- RP: tinted copies of the part models -------------------------------------------------------------------------------
const mdir = path.join(rp, 'assets/rlk/models/item/raiden'), idir = path.join(rp, 'assets/rlk/items/raiden');
fs.rmSync(path.join(mdir, 'clone'), {recursive: true, force: true});
fs.rmSync(path.join(idir, 'clone'), {recursive: true, force: true});
for (const m of new Set(Object.values(PARTS))) {
  const src = path.join(mdir, m + '.json');
  if (!fs.existsSync(src)) throw new Error(`${src}: build the rig first (build_raiden_rig.mjs)`);
  const model = JSON.parse(fs.readFileSync(src, 'utf8'));
  for (const e of model.elements) for (const f of Object.values(e.faces)) f.tintindex = 0;
  put(path.join(mdir, 'clone', m + '.json'), JSON.stringify(model));
  for (const [look, rgb] of Object.entries(TINT))
    put(path.join(idir, 'clone', look, m + '.json'), JSON.stringify({model: {type: 'minecraft:model', model: `rlk:item/raiden/clone/${m}`,
      tints: [{type: 'minecraft:constant', value: rgb}]}}));
}

// ---- poses (the rig's own forward kinematics and display transforms) ----------------------------------------------------------
const f5 = x => (Math.abs(x) < 5e-6 ? 0 : x).toFixed(5).replace(/\.?0+$/, '') + 'f';
const arr = a => '[' + a.map(f5).join(',') + ']';
const tf = v => `{translation:${arr(v.t)},left_rotation:${arr(v.q)},scale:${arr(v.s)},right_rotation:[0f,0f,0f,1f]}`;
const table = {};
for (const [name, pose] of Object.entries(CLONE_POSES)) {
  const p = {...DEFAULT_POSE, ...pose, wfx: WFX[name] || 0, sS: 1, tS: 0, vis: 1, ph: 0, bob: 0};
  const o = solve(p);
  for (const n of Object.keys(PARTS)) (table[n] ||= {})[name] = written(toDisplay(n, o[n]));
}
// summon: as the clone husk at its feet; the parts keep its id (rdObjId) so object/break and the illusion remove them
const fn = (n, lines) => put(path.join(dp, 'data/rlk/function/boss/raiden/clone', n + '.mcfunction'), lines.join('\n'));
fs.rmSync(path.join(dp, 'data/rlk/function/boss/raiden/clone'), {recursive: true, force: true});
const TAGS = '"rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_sg","rlk_rd_objvisual","rlk_rd_ilvis","rlk_rd_clp","rlk_rd_clnew"';
fn('summon', ['# As a clone husk at its feet ({id}): its 14 part displays in the idle pose, dark, at its yaw. Each part keeps its',
  '# poses (custom_data P) and its dark / glow model ids, so clone/pose drives every clone with three commands per part.',
  ...Object.entries(PARTS).map(([n, m]) => {
    const P = Object.entries(table[n]).map(([k, v]) => `${k}:${tf(v)}`).join(',');
    return `summon minecraft:item_display ~ ~ ~ {Tags:[${TAGS}],billboard:"fixed",item_display:"none",teleport_duration:2,` +
      `interpolation_duration:0,view_range:2.5f,width:3f,height:3f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:${tf(table[n].idle)},` +
      `item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/clone/dark/${m}","minecraft:custom_data":` +
      `{n:"${n}",dark:"rlk:raiden/clone/dark/${m}",glow:"rlk:raiden/clone/glow/${m}",P:{${P}}}}}}`;
  }),
  '$scoreboard players set @e[tag=rlk_rd_clnew] rdObjId $(id)',
  'execute rotated as @s run tp @e[tag=rlk_rd_clnew] ~ ~ ~ ~ 0',
  'tag @e[tag=rlk_rd_clnew] remove rlk_rd_clnew']);
fn('pose', ['# {sel,p,d,look}: every clone part matching sel eases to pose p over d ticks, in look dark|glow.',
  '$execute as @e[type=minecraft:item_display,tag=rlk_rd_clp,$(sel)] run data modify entity @s transformation set from entity @s item.components."minecraft:custom_data".P.$(p)',
  '$execute as @e[type=minecraft:item_display,tag=rlk_rd_clp,$(sel)] run data merge entity @s {start_interpolation:0,interpolation_duration:$(d)}',
  '$execute as @e[type=minecraft:item_display,tag=rlk_rd_clp,$(sel)] run data modify entity @s item.components."minecraft:item_model" set from entity @s item.components."minecraft:custom_data".$(look)']);
console.log(`Built the clone figures: ${Object.keys(PARTS).length} parts, ${Object.keys(CLONE_POSES).length} poses, ` +
  `${new Set(Object.values(PARTS)).size} tinted models x 2 looks.`);
