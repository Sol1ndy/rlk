// Display-entity rig of 야타용왕 (Azhdaha, 봉인된 바위 용의 왕), the chapter-1 boss: a huge stone quadruped dragon,
// H = 7.0 b to the tallest dorsal plate, 10.2 b nose to rump, a 14.5 b tail (scratchpad az/plan.md R1-R11,
// az/understand/model.md, motion.md, rigtech.md).
// node tools/build_mboss_azhdaha_rig.mjs --resourcepack <unpacked pack> [--datapack <pack>] [--no-paint | --paint a,b]
//                                        [--debug-dp <scratch dir> [--debug-clips a,b | all]] [--allow-steps]
//
// Writes
//   RP  assets/rlk/textures/mboss/azhdaha/*.png (azhdaha_paint.mjs) + item atlas entries
//       assets/rlk/models/item/mboss/azhdaha/*.json, assets/rlk/items/mboss/azhdaha/*.json (models + tinted overlays)
//   DP  data/rlk/function/mboss/azhdaha/rig/** (owned by this generator, rebuilt from scratch on every run)
//   tools/mboss_azhdaha_rig_manifest.json (parts, clips, events, looks, states, hit-proxy points, budgets, objectives)
//
// Runtime model (the contract for the pattern code is tools/mboss_azhdaha_rig_api.md):
//   * 46 item_display parts with FIXED UUIDs 524c4b4d-415a-4400-8000-0000000000NN (plan.md R9), split by region
//     (head / body / legs / tail: azhdaha_{head,body,legs,tail}.mjs). Tags rlk_room, rlk_mb_aux, rlk_mb_part,
//     rlk_mb_azhdaha_part, rlk_mb_az_<part>, rlk_mb_az_g_<region>. Culling box width 30, height 12 on every part and
//     view_range 3 (plan.md R4): the parts sit at the anchor, the tail reaches 15 b behind it.
//   * The anchor (the boss body, on the floor under the centre of the four feet) runs rig/tick each tick: the parts
//     follow its position and yaw (tp, teleport_duration 1) and the current clip applies its keys (the shared compiler
//     mboss_rig_compile.mjs: interpolation segments, rotation checks, binary dispatch).
//   * Element looks (plan.md R6): two independent channels stored on the anchor, azRigLegs (0 geo, 1 hydro, 2 pyro:
//     bracers, paws, gaiters, feet, apron, belly cracks + the tinted glow overlays) and azRigTail (0 geo, 1 cryo,
//     2 electro: the four plate groups and the tail chain). Item-model swaps, re-applied after a respawn.
//   * Body states (plan.md R7): azRigState 0 normal, 1 burrowed (every part at scale 0, the root sunk), 2 tail-only
//     (the body parts at scale 0; the tail clips raise the chain). The clips carry the poses; state/<name> records the
//     state for respawns and the hit-proxy layer.
//   * Hit proxies (plan.md R5): the rig publishes 12 ground points per pose (manifest `proxies`, per clip `px`); the
//     framework side (interaction entities, rigtech.md §3.3) comes later.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {paintAzhdahaTextures, spriteId, azhdahaSpriteSizes, ATLAS_BUDGET} from './azhdaha_paint.mjs';
import {partModels, checkBounds, PARTS, LOOKS, TINTED, LOOK_BRIGHT, EMPTY, REGION_OF} from './azhdaha_geometry.mjs';
import {solve, toDisplay, PART_SCALE, TAIL_PARTS, proxyPoints, PROXIES, pointOf, J} from './azhdaha_pose.mjs';
import {CLIPS, accumulate, sampleClip as sample, restPose} from './azhdaha_clips.mjs';
import {add, rot} from './mboss_rig_math.mjs';
import {createRigCompiler, nbt} from './mboss_rig_compile.mjs';
import {abox} from './mboss_model_lib.mjs';
import {png} from './weapon_paint.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const arg = n => { const i = process.argv.indexOf(n); return i < 0 ? null : process.argv[i + 1]; };
const flag = n => process.argv.includes(n);
const dp = path.resolve(arg('--datapack') || path.join(here, '..'));
const rp = arg('--resourcepack') && path.resolve(arg('--resourcepack'));
if (!rp) throw new Error('--resourcepack <unpacked pack> is required');
const put = (p, s) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, s.endsWith('\n') ? s : s + '\n'); };
const json = (p, o) => put(p, JSON.stringify(o, null, 2));
const NS = 'rlk:mboss/azhdaha/rig';
const rigDir = path.join(dp, 'data/rlk/function/mboss/azhdaha/rig');
fs.rmSync(rigDir, {recursive: true, force: true});
const fn = (n, lines) => put(path.join(rigDir, n + '.mcfunction'), (Array.isArray(lines) ? lines : [lines]).join('\n'));
const assets = path.join(rp, 'assets/rlk');

// ---- parts (plan.md R3: 44-48 display parts, hard cap 56) ---------------------------------------------------------------
if (PARTS.length > 56) throw new Error(`${PARTS.length} parts: the hard cap is 56`);
if (PARTS.length < 44 || PARTS.length > 48) console.warn(`warn: ${PARTS.length} parts, outside the 44-48 budget`);
for (const [n] of PARTS) if (!PART_SCALE[n]) throw new Error(`part ${n} has no display scale`);
const PART_INDEX = Object.fromEntries(PARTS.map(([n], i) => [n, i + 1]));
const uuidOf = n => `524c4b4d-415a-4400-8000-${PART_INDEX[n].toString(16).padStart(12, '0')}`;
const uuidInts = n => `[I;1380731725,1096434688,-2147483648,${PART_INDEX[n]}]`;
const SHADOW_UUID = '524c4b4d-415a-4400-8000-000000000040', SHADOW_INTS = '[I;1380731725,1096434688,-2147483648,64]';
const itemId = m => `rlk:mboss/azhdaha/${m}`;
const CULL = {width: 30, height: 12}, VIEW_RANGE = 3;

// ---- resource pack: textures, models, item definitions ---------------------------------------------------------------------
const sprites = flag('--no-paint') ? null : paintAzhdahaTextures(rp, arg('--paint') ? arg('--paint').split(',') : null);
const models = partModels();
for (const [name, els] of Object.entries(models)) checkBounds(name, els);
const modelDir = path.join(assets, 'models/item/mboss/azhdaha'), itemDir = path.join(assets, 'items/mboss/azhdaha');
fs.rmSync(modelDir, {recursive: true, force: true});
fs.rmSync(itemDir, {recursive: true, force: true});
const spriteTable = azhdahaSpriteSizes();
for (const [name, els] of Object.entries(models)) {
  const used = [...new Set(els.flatMap(e => Object.values(e.faces).map(f => f.texture.slice(1))))];
  for (const u of used) if (!spriteTable[u]) throw new Error(`model ${name}: unknown sprite ${u}`);
  const tex = used.length ? used : ['cream'];
  json(path.join(modelDir, name + '.json'), {ambientocclusion: false, textures: {...Object.fromEntries(used.map(t => [t, spriteId(t)])), particle: spriteId(tex[0])}, elements: els});
  json(path.join(itemDir, name + '.json'), {model: {type: 'minecraft:model', model: 'rlk:item/mboss/azhdaha/' + name}});
}
for (const [item, [model, rgb]] of Object.entries(TINTED)) {
  if (!models[model]) throw new Error(`tinted item ${item}: unknown model ${model}`);
  json(path.join(itemDir, item + '.json'), {model: {type: 'minecraft:model', model: 'rlk:item/mboss/azhdaha/' + model, tints: [{type: 'minecraft:constant', value: rgb}]}});
}
const ITEMS = new Set([...Object.keys(models), ...Object.keys(TINTED)]);
for (const [ch, parts] of Object.entries(LOOKS)) for (const [part, looks] of Object.entries(parts)) for (const [l, m] of Object.entries(looks)) {
  if (!PART_INDEX[part]) throw new Error(`look ${ch}/${l}: unknown part ${part}`);
  if (!ITEMS.has(m)) throw new Error(`look ${ch}/${l}: part ${part} item ${m} missing`);
}
// atlas budget (plan.md R8)
let atlasPx = 0;
for (const [n, [w, h]] of Object.entries(spriteTable)) {
  if (w > 512 || h > 512 || w % 16 || h % 16) throw new Error(`sprite ${n} ${w}x${h}: sides <= 512, multiples of 16`);
  atlasPx += w * h;
}
if (atlasPx > ATLAS_BUDGET) throw new Error(`Azhdaha sprites use ${atlasPx} px of the atlas (budget ${ATLAS_BUDGET / 1e6} M)`);
const elementCount = Object.fromEntries(Object.entries(models).map(([n, e]) => [n, e.length]));

// ---- clip sampling, per-pose checks -------------------------------------------------------------------------------------------
function frame(clip, t, ks, prev) {
  const p = sample(clip, t, ks);
  const o = solve(p, {prev: prev && prev.o._bend});
  const d = {};
  for (const [n] of PARTS) d[n] = toDisplay(n, o[n]);
  return {d, p, o};
}
const clipFrames = (clip, ks = accumulate(clip)) => { const out = []; for (let t = 0; t <= clip.len; t++) out.push(frame(clip, t, ks, out[t - 1])); return out; };
const r3 = v => v.map(x => +x.toFixed(3) || 0);
// model-space bounding box of every model (units), for the world extents of a posed part
const BOX = Object.fromEntries(Object.entries(models).map(([n, els]) => {
  if (!els.length) return [n, null];
  const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
  for (const e of els) for (const v of [e.from, e.to]) for (let i = 0; i < 3; i++) { const a = i === 0 ? 8 - v[0] : v[i] - 8; lo[i] = Math.min(lo[i], a); hi[i] = Math.max(hi[i], a); }
  return [n, [lo, hi]];
}));
// world (rig-frame) corners of a posed part's default model box
function partCorners(o, n, model) {
  const b = BOX[model];
  if (!b || o[n].s[0] < 1e-4) return [];
  const k = PART_SCALE[n] / 16, out = [];
  for (const x of [b[0][0], b[1][0]]) for (const y of [b[0][1], b[1][1]]) for (const z of [b[0][2], b[1][2]]) out.push(pointOf(o, n, [x * k, y * k, z * k]));
  return out;
}
const MODEL_OF_PART = Object.fromEntries(PARTS.map(([n, m]) => [n, m === EMPTY ? null : m]));
// Pose checks (every frame of every clip): no horizontal root travel; every shown part inside the culling box (x/z
// within +-15, y below 12 above the anchor); the soles of the planted feet on or above the floor unless the clip is
// buried (pos y < 0); the tail-only state hides every non-tail part.
function poseChecks(c, frames) {
  const out = [], over = {};
  let ext = [[Infinity, -Infinity], [Infinity, -Infinity], [Infinity, -Infinity]];
  frames.forEach((f, t) => {
    if (Math.abs(f.p.pos[0]) > 1e-9 || Math.abs(f.p.pos[2]) > 1e-9) out.push(`${c.name} t${t}: root travel (x/z must be 0)`);
    for (const [n] of PARTS) for (const P of partCorners(f.o, n, MODEL_OF_PART[n])) {
      for (let i = 0; i < 3; i++) { ext[i][0] = Math.min(ext[i][0], P[i]); ext[i][1] = Math.max(ext[i][1], P[i]); }
      // culling-box overhang (blocks past the box): recorded, not fatal (the box is plan.md R4's fixed 30 x 12)
      const o = Math.max(Math.abs(P[0]) - CULL.width / 2, Math.abs(P[2]) - CULL.width / 2, P[1] - CULL.height);
      if (o > 0) over[n] = Math.max(over[n] || 0, +o.toFixed(2));
    }
    if (f.p.pos[1] >= -.01) for (const n of ['paw_l', 'paw_r', 'foot_l', 'foot_r']) {
      const y = pointOf(f.o, n, [0, n.startsWith('paw') ? -.5 : -.72, 0])[1];
      if (y < -.08) out.push(`${c.name} t${t}: ${n} sole ${y.toFixed(2)} b below the floor`);
    }
    if (c.state === 'tail_only') for (const [n] of PARTS) if (!TAIL_PARTS.includes(n) && f.o[n].s[0] > 1e-4) out.push(`${c.name} t${t}: ${n} shown in the tail-only state`);
  });
  for (const [e, t] of Object.entries(c.events || {})) if (!(t >= 0 && t <= c.len)) out.push(`${c.name}: event ${e} at ${t} outside 0..${c.len}`);
  return {errors: out, over, extents: ext.map(([a, b]) => [+a.toFixed(2), +b.toFixed(2)])};
}

// ---- compile clips --------------------------------------------------------------------------------------------------------------
const debugDp = arg('--debug-dp') && path.resolve(arg('--debug-dp'));
const debugClips = (arg('--debug-clips') || '').split(',').filter(Boolean);
const debugOf = c => debugDp && (debugClips.includes('all') || debugClips.includes(c.name));
if (debugDp) fs.rmSync(path.join(debugDp, 'data/rlk/function/az_dbg'), {recursive: true, force: true});
const putDebug = (n, lines) => put(path.join(debugDp, 'data/rlk/function', n + '.mcfunction'), lines.join('\n'));
// Tolerances: translation 0.012 b; rotation per part (long parts tighter: a tail segment 2 b long turned 0.5 degree
// moves its tip 0.017 b).
const TOL = {t: .012, s: .015, rDefault: 1.0, r: {chest: .4, belly: .4, pelvis: .4, plates_sh: .4, plates_mid: .4, plates_hip: .5, crys_sh: .5, crys_mid: .5,
  t1: .3, t2: .3, t3: .35, t4: .4, t5: .45, t6: .5, t7: .55, t8: .6, tip: .7, horn_l: .6, horn_r: .6, head: .6}};
const swapLine = (part, model) => `data modify entity ${uuidOf(part)} item.components."minecraft:item_model" set value "${itemId(model)}"`;
const mkCompiler = debug => createRigCompiler({ns: NS, obj: 'azRig', fn, parts: PARTS.map(([n]) => n), uuidOf, tol: TOL, swapLine,
  debug: debug ? {put: putDebug, dir: 'az_dbg'} : null});
const compiler = mkCompiler(false), debugCompiler = debugDp ? mkCompiler(true) : null;
const clipInfo = [], motionErrors = [], poseErrors = [], warns = new Set(), extents = {};
CLIPS.forEach((c, id) => { c.id = id; });
const byName = Object.fromEntries(CLIPS.map(c => [c.name, c]));
const pxTrack = (frames, ticks) => Object.fromEntries(ticks.map(t => [t, proxyPoints(frames[Math.min(t, frames.length - 1)].o)]));
for (const c of CLIPS) {
  if (c.keys[0][0] !== 0) throw new Error(`clip ${c.name}: first key must be tick 0`);
  if (c.keys[c.keys.length - 1][0] !== c.len) throw new Error(`clip ${c.name}: last key ${c.keys[c.keys.length - 1][0]} != len ${c.len}`);
  if (c.next && !byName[c.next]) throw new Error(`clip ${c.name}: unknown next ${c.next}`);
  const ks = accumulate(c), frames = clipFrames(c, ks);
  const chk = poseChecks(c, frames);
  poseErrors.push(...chk.errors);
  extents[c.name] = chk.extents;
  const r = (debugOf(c) ? debugCompiler : compiler).compileClip(c, frames, a => frame(c, a + .5, ks, frames[a]));
  motionErrors.push(...r.motionErrors);
  r.warns.forEach(w => warns.add(w));
  const evTicks = [...new Set([0, ...Object.values(c.events || {}), c.len])].sort((a, b) => a - b);
  if (Object.keys(chk.over).length) warns.add(`${c.name}: outside the ${CULL.width} x ${CULL.height} culling box by ${JSON.stringify(chk.over)}`);
  clipInfo.push({...r.info, state: c.state || 'normal', extents: chk.extents, ...(Object.keys(chk.over).length ? {cull_overhang: chk.over} : {}), px: pxTrack(frames, evTicks)});
}
if (poseErrors.length) {
  const msg = `pose checks:\n  ` + poseErrors.slice(0, 60).join('\n  ') + (poseErrors.length > 60 ? `\n  ... ${poseErrors.length} in all` : '');
  if (flag('--allow-steps')) console.warn(msg); else throw new Error(msg);
}
if (motionErrors.length) {
  const msg = `part rotations above 120 degrees per tick or per key:\n  ` + motionErrors.slice(0, 120).join('\n  ');
  if (flag('--allow-steps')) console.warn(msg); else throw new Error(msg);
}
compiler.writeDispatch(CLIPS);

// ---- API functions ------------------------------------------------------------------------------------------------------------
const REST = (() => { const o = solve(restPose()); return Object.fromEntries(PARTS.map(([n]) => [n, toDisplay(n, o[n])])); })();
const REGION_TAG = n => `rlk_mb_az_g_${REGION_OF[n]}`;
const TAGS = n => `["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_azhdaha_part","rlk_mb_az_${n}","${REGION_TAG(n)}"]`;
const summon = ([n, model, bright], pose) => `summon minecraft:item_display ~ ~ ~ {UUID:${uuidInts(n)},Tags:${TAGS(n)},billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:${VIEW_RANGE}f,width:${CULL.width}f,height:${CULL.height}f,shadow_radius:0f,brightness:{block:${bright},sky:15},transformation:${nbt(pose)},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${itemId(model)}"}}}`;
const shadowSummon = `summon minecraft:item_display ~ ~ ~ {UUID:${SHADOW_INTS},Tags:["rlk_room","rlk_mb_aux","rlk_mb_azhdaha_part","rlk_mb_az_shadow"],billboard:"fixed",item_display:"none",teleport_duration:1,view_range:${VIEW_RANGE}f,width:${CULL.width}f,height:${CULL.height}f,shadow_radius:4.5f,shadow_strength:.8f,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${itemId(EMPTY)}"}}}`;
const RIG_OBJ = ['azRigC', 'azRigT', 'azRigF', 'azRigY', 'azRigLegs', 'azRigTail', 'azRigState'];
fn('init', ['# Rig objectives. Safe to call on every load.', ...RIG_OBJ.map(o => `scoreboard objectives add ${o} dummy`)]);
const setPose = (pose, dur = 0) => PARTS.map(([n]) => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:${dur},transformation:${nbt(pose[n])}}`);
const stored = ['execute unless score @s azRigLegs matches 0..2 run scoreboard players set @s azRigLegs 0',
  'execute unless score @s azRigTail matches 0..2 run scoreboard players set @s azRigTail 0',
  'execute unless score @s azRigState matches 0..2 run scoreboard players set @s azRigState 0'];
fn('spawn', ['# @s = rig anchor (the boss body, on the floor under the centre of the four feet), positioned and rotated where the',
  `# boss should appear. Kills old parts, summons the ${PARTS.length} parts in the rest pose (+ the shadow helper), queues rest and`,
  '# re-applies the stored element looks (azRigLegs, azRigTail) and the body state (azRigState).',
  `function ${NS}/init`, `function ${NS}/kill`, ...stored, ...PARTS.map(p => summon(p, REST[p[0]])), shadowSummon,
  'scoreboard players set @s azRigT -1', 'scoreboard players set @s azRigF 0', `scoreboard players set @s azRigC ${byName.rest.id}`,
  `function ${NS}/look_apply`, `execute if score @s azRigState matches 1 run function ${NS}/state/burrowed`, `execute if score @s azRigState matches 2 run function ${NS}/state/tail_only`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow`]);
fn('follow', ['# Parts (and the shadow helper) follow the executor position and yaw (run rotated as the anchor, pitch 0).', ...PARTS.map(([n]) => `tp ${uuidOf(n)} ~ ~ ~ ~ ~`), `tp ${SHADOW_UUID} ~ ~ ~ ~ ~`]);
fn('tick', ['# @s = rig anchor, at its feet. Once per game tick. Missing parts respawn in the rest pose (stored looks and state kept).',
  `execute unless entity ${uuidOf('chest')} run function ${NS}/spawn`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow`,
  'scoreboard players add @s azRigT 1',
  `function ${NS}/run`,
  `execute if score @s azRigF matches 1.. run function ${NS}/flash_tick`]);
fn('kill', ['# Removes every rig part and the shadow helper.', 'kill @e[type=item_display,tag=rlk_mb_azhdaha_part]']);
fn('uninstall', ['# Removes the rig and its objectives.', `function ${NS}/kill`, 'kill @e[type=marker,tag=rlk_mb_az_face]', ...RIG_OBJ.map(o => `scoreboard objectives remove ${o}`)]);
// element looks: two channels, item-model swaps + brightness per look
const LOOK_IDS = {legs: {geo: 0, hydro: 1, pyro: 2}, tail: {geo: 0, cryo: 1, electro: 2}};
const BASE_BRIGHT = Object.fromEntries(PARTS.map(([n, , b]) => [n, b]));
const LOOK_NOTE = {
  legs: {geo: 'phase 1: the base stone, no glow lines', hydro: 'phase 2 Hydro: bracers, gaiters, paws and feet in navy-black stone with white-cyan glowing lines, the apron lines blue-white (overlays tinted)', pyro: 'phase 2 Pyro: deep red stone with orange glowing lines, the apron lines and the belly cracks red-orange (overlays tinted)'},
  tail: {geo: 'phases 1-2: dark umber plates, orange-gold leaves', cryo: 'phase 3 Cryo: cool slate plates with white-cyan edges, the tail cooled, crystal blossoms at the tip', electro: 'phase 3 Electro: violet-dark plates with violet edges, violet blossoms at the tip'},
};
const obj = {legs: 'azRigLegs', tail: 'azRigTail'};
for (const [ch, looks] of Object.entries(LOOK_IDS)) for (const [look, id] of Object.entries(looks)) {
  const swaps = Object.entries(LOOKS[ch]).map(([part, m]) => swapLine(part, m[look]));
  const bright = Object.keys(LOOKS[ch]).map(part => `data merge entity ${uuidOf(part)} {brightness:{block:${(LOOK_BRIGHT[ch][look] || {})[part] ?? BASE_BRIGHT[part]},sky:15}}`);
  fn(`look/${ch}/${look}_swap`, [`# Internal: the ${ch} channel's ${look} models and brightness.`, ...swaps, ...bright]);
  fn(`look/${ch}/${look}`, [`# Element look, ${ch} channel: ${LOOK_NOTE[ch][look]}. Stored in ${obj[ch]} (kept over a respawn). @s = rig anchor.`,
    `scoreboard players set @s ${obj[ch]} ${id}`, `function ${NS}/look/${ch}/${look}_swap`]);
}
fn('look_apply', ['# Re-applies the stored looks azRigLegs and azRigTail (after a respawn). @s = rig anchor.',
  ...Object.entries(LOOK_IDS).flatMap(([ch, looks]) => Object.entries(looks).map(([l, id]) => `execute if score @s ${obj[ch]} matches ${id} run function ${NS}/look/${ch}/${l}_swap`))]);
// body states: the scale-0 masks (the clips own the poses; these record the state and hide what must not show)
const hideParts = list => list.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:{scale:[0f,0f,0f]}}`);
const nonTail = PARTS.map(([n]) => n).filter(n => !TAIL_PARTS.includes(n));
fn('state/normal', ['# Normal body state (the next clip key shows every part again). @s = rig anchor.', 'scoreboard players set @s azRigState 0']);
fn('state/burrowed', ['# Burrowed (underground travel): every part at scale 0 until a clip shows them. @s = rig anchor.', 'scoreboard players set @s azRigState 1', ...hideParts(PARTS.map(([n]) => n))]);
fn('state/tail_only', ['# Tail-only (phase-3 sink): the body parts at scale 0, the tail chain shown by the tail clips. @s = rig anchor.', 'scoreboard players set @s azRigState 2', ...hideParts(nonTail)]);
// hit flash: a warm white outline for 3 ticks on one part group (rigtech.md §2.6: never all 46 parts at once)
const GROUPS = {head: ['head', 'jaw', 'horn_l', 'horn_r'], front: ['chest', 'neck1', 'neck2', 'apron', 'uarm_l', 'uarm_r', 'bracer_l', 'bracer_r', 'paw_l', 'paw_r'],
  rear: ['belly', 'pelvis', 'thigh_l', 'thigh_r', 'gaiter_l', 'gaiter_r', 'foot_l', 'foot_r'], tail: ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 'tip']};
for (const [g, list] of Object.entries(GROUPS)) {
  fn(`flash/${g}`, [`# Hit feedback on the ${g} group: a warm white outline for 3 ticks. @s = rig anchor.`, 'scoreboard players set @s azRigF 4', ...list.map(n => `data merge entity ${uuidOf(n)} {Glowing:1b,glow_color_override:16774620}`)]);
}
const ALL_FLASH = Object.values(GROUPS).flat();
fn('flash_tick', ['scoreboard players remove @s azRigF 1', `execute if score @s azRigF matches 0 run function ${NS}/flash_off`]);
fn('flash_off', ['# End of the hit flash. @s = rig anchor.', ...ALL_FLASH.map(n => `data merge entity ${uuidOf(n)} {Glowing:0b}`)]);
compiler.writeFace({marker: 'rlk_mb_az_face', maxDeg: 2});

// ---- manifest ---------------------------------------------------------------------------------------------------------------
const restO = solve(restPose());
const manifestPath = path.join(here, 'mboss_azhdaha_rig_manifest.json');
const lastTextures = (() => { try { return JSON.parse(fs.readFileSync(manifestPath, 'utf8')).textures; } catch { return undefined; } })();
const shownElements = PARTS.reduce((a, [, m]) => a + (elementCount[m] || 0), 0);
json(manifestPath, {
  parts: PARTS.map(([n, m, b, r]) => ({name: n, region: r, uuid: uuidOf(n), tag: 'rlk_mb_az_' + n, model: m, brightness: b, scale: PART_SCALE[n], elements: elementCount[m]})),
  shadow: {uuid: SHADOW_UUID, tag: 'rlk_mb_az_shadow', shadow_radius: 4.5, note: 'empty-model helper under the anchor, not a rig part'},
  clips: clipInfo,
  looks: Object.fromEntries(Object.entries(LOOK_IDS).map(([ch, ids]) => [ch, {objective: obj[ch], ids, parts: LOOKS[ch], brightness: LOOK_BRIGHT[ch], functions: Object.fromEntries(Object.keys(ids).map(l => [l, `${NS}/look/${ch}/${l}`]))}])),
  tinted_items: Object.fromEntries(Object.entries(TINTED).map(([k, [m, c]]) => [k, {model: m, tint: '#' + c.toString(16).padStart(6, '0')}])),
  states: {objective: 'azRigState', ids: {normal: 0, burrowed: 1, tail_only: 2}, functions: {normal: `${NS}/state/normal`, burrowed: `${NS}/state/burrowed`, tail_only: `${NS}/state/tail_only`}},
  flash_groups: GROUPS,
  proxies: {layout: PROXIES.map(([name, part, at, w, top, flags]) => ({name, part, point: at, w, top_margin: top, tail_only: flags === 'tail_only'})), rest: proxyPoints(restO),
    note: 'ground-anchored interaction columns (rigtech.md §3.3): x/z = the bone point projected on the floor (rig frame, +x = the boss left, -z = its front), base/top = the column; per clip in clips[].px at the events'},
  skeleton: {joints: J, scale_H: 7.0},
  culling: {width: CULL.width, height: CULL.height, view_range: VIEW_RANGE},
  rest_extents: extents.rest,
  budgets: {parts: PARTS.length, part_budget: '44-48 (cap 56)', models: Object.keys(models).length, elements_all_models: Object.values(elementCount).reduce((a, b) => a + b, 0),
    elements_shown_rest: shownElements, atlas_px: atlasPx, atlas_budget: ATLAS_BUDGET},
  objectives: {azRigC: 'current clip id (anchor)', azRigT: 'tick within the clip (anchor; -1 = queued by play)', azRigF: 'hit flash countdown', azRigY: 'face/track scratch',
    azRigLegs: 'legs look: 0 geo, 1 hydro, 2 pyro', azRigTail: 'tail look: 0 geo, 1 cryo, 2 electro', azRigState: 'body state: 0 normal, 1 burrowed, 2 tail-only'},
  textures: sprites ? sprites.length : (typeof lastTextures === 'number' ? lastTextures : 'not repainted'),
});
for (const w of [...warns].slice(0, 40)) console.warn('warn:', w);
const files = clipInfo.reduce((a, c) => a + c.keyFiles, 0);
console.log(`Built the Azhdaha rig: ${PARTS.length} parts, ${CLIPS.length} clips, ${files} key files, ${clipInfo.reduce((a, c) => a + c.keys, 0)} part keys, ${Object.keys(models).length} models (${Object.values(elementCount).reduce((a, b) => a + b, 0)} elements, ${shownElements} shown at rest), ${Object.keys(spriteTable).length} sprites (${(atlasPx / 1e6).toFixed(2)} M px)${warns.size ? `, ${warns.size} warnings` : ''}.`);
console.log(`rest extents x ${extents.rest[0]}, y ${extents.rest[1]}, z ${extents.rest[2]}`);
if (debugDp) {
  const link = path.join(debugDp, 'data/rlk/function/mboss/azhdaha/rig');
  fs.rmSync(link, {recursive: true, force: true});
  fs.mkdirSync(path.dirname(link), {recursive: true});
  fs.symlinkSync(rigDir, link);
  putDebug('az_dbg/rest', setPose(REST));
  // element-look combinations for renders: az_dbg/look_<legs>_<tail>
  for (const lg of Object.keys(LOOK_IDS.legs)) for (const tl of Object.keys(LOOK_IDS.tail))
    putDebug(`az_dbg/look_${lg}_${tl}`, [`function ${NS}/look/legs/${lg}_swap`, `function ${NS}/look/tail/${tl}_swap`]);
  // a 0.6 x 1.8 b player reference beside the left fore paw (outside it) and one in front of the snout (renders only)
  const ref = (x, z) => `summon minecraft:item_display ^${x} ^ ^${z} {Tags:["rlk_az_ref"],item_display:"none",transformation:{translation:[0f,0.9f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:az_ref/player"}}}`;
  putDebug('az_dbg/player_ref', ['# renders: a 1.8 b player beside the left fore paw and one 1.5 b in front of the snout', ref(4.6, 2.55), ref(0, 6.6)]);
  // its model lives in an overlay pack next to the debug datapack (render with --rp <debug>/rp_ref --rp <rp>), never in the real RP
  const rpRef = path.join(debugDp, 'rp_ref/assets/rlk');
  fs.mkdirSync(path.join(rpRef, 'textures/az_ref'), {recursive: true});
  const buf = Buffer.alloc(16 * 16 * 4); for (let i = 0; i < 256; i++) buf.set([60, 120, 210, 255], i * 4);
  fs.writeFileSync(path.join(rpRef, 'textures/az_ref/player.png'), png(16, 16, buf));
  json(path.join(rpRef, 'models/item/az_ref/player.json'), {textures: {ref: 'rlk:az_ref/player'}, elements: [abox([-4.8, -14.4, -2.4], [4.8, 14.4, 2.4], 'ref')]});
  json(path.join(rpRef, 'items/az_ref/player.json'), {model: {type: 'minecraft:model', model: 'rlk:item/az_ref/player'}});
  json(path.join(debugDp, 'rp_ref/pack.mcmeta'), {pack: {pack_format: 46, description: 'Azhdaha render references'}});
  fs.mkdirSync(path.join(rpRef, '../minecraft/atlases'), {recursive: true});
  json(path.join(rpRef, '../minecraft/atlases/items.json'), {sources: [{type: 'minecraft:single', resource: 'rlk:az_ref/player'}]});
}
