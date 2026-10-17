// Articulated display-entity rig of the Corrupted Guardian (파수꾼・타락), the first mid-boss.
// node tools/build_mboss_guardian_rig.mjs --resourcepack <unpacked pack> [--datapack <pack>] [--no-paint]
//
// Writes
//   RP  assets/rlk/textures/mboss/guardian/*.png (guardian_paint.mjs) + item atlas entries
//       assets/rlk/models/item/mboss/guardian/*.json, assets/rlk/items/mboss/guardian/*.json
//   DP  data/rlk/function/mboss/guardian/rig/** (this directory is owned by the generator and
//       rebuilt from scratch on every run)
//   tools/mboss_guardian_rig_manifest.json (parts, clips, events, API)
//
// Runtime model (see scratchpad mboss/rig_api.md for the contract):
//   * 29 item_display parts with FIXED UUIDs 524c4b4d-4247-4400-8000-0000000000NN, so every
//     per-tick command addresses a part directly (no selector scan). All parts also carry
//     rlk_room, rlk_mb_aux, rlk_mb_part, rlk_mb_guardian_part, rlk_mb_gp_<part>.
//   * The anchor (the boss body) runs rig/tick each tick: the parts follow its position and
//     yaw (tp, teleport_duration 1), and the current clip applies its keys.
//   * Clips are compiled per part into interpolation segments: at tick a a part receives the
//     pose of tick b with interpolation_duration b-a, where b is the furthest tick whose
//     in-between poses the client's lerp/slerp reproduces within tolerance (spins, arcs and
//     fast strikes get a key every tick; holds get one key).
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {paintGuardianTextures, spriteId, CARD} from './guardian_paint.mjs';
import {partModels, PART_SCALE, checkBounds} from './guardian_geometry.mjs';
import {solve, toDisplay} from './guardian_pose.mjs';
import {CLIPS, DEFAULT_POSE} from './guardian_clips.mjs';
import {slerp, lerp, qAngle, len, sub} from './guardian_rig_math.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const arg = n => { const i = process.argv.indexOf(n); return i < 0 ? null : process.argv[i + 1]; };
const flag = n => process.argv.includes(n);
const dp = path.resolve(arg('--datapack') || path.join(here, '..'));
const rp = arg('--resourcepack') && path.resolve(arg('--resourcepack'));
if (!rp) throw new Error('--resourcepack <unpacked pack> is required');
const put = (p, s) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, s.endsWith('\n') ? s : s + '\n'); };
const json = (p, o) => put(p, JSON.stringify(o, null, 2));
const NS = 'rlk:mboss/guardian/rig';
const rigDir = path.join(dp, 'data/rlk/function/mboss/guardian/rig');
fs.rmSync(rigDir, {recursive: true, force: true});
const fn = (n, lines) => put(path.join(rigDir, n + '.mcfunction'), (Array.isArray(lines) ? lines : [lines]).join('\n'));
const assets = path.join(rp, 'assets/rlk');

// ---- parts ------------------------------------------------------------------------------
// [part, default item model, block brightness]
const PARTS = [
  ['pelvis', 'pelvis', 13], ['skirt_f', 'skirt_f', 13], ['skirt_o', 'skirt_o', 13], ['tail', 'tail', 13],
  ['leg_r', 'leg_r', 13], ['leg_l', 'leg_l', 13], ['torso', 'torso', 13], ['head', 'head', 15],
  ['halo', 'halo', 15], ['halo_glow', 'halo_glow', 15],
  ['r_upper', 'r_upper', 12], ['r_fore', 'r_fore', 12], ['r_hand', 'r_hand_fist', 12],
  ['l_upper', 'l_upper', 13], ['l_fore', 'l_fore', 15], ['l_hand', 'l_hand_open', 13],
  ['bracket', 'bracket', 13], ['shield', 'shield', 14], ['shield_eye', 'shield_eye', 15],
  ['wing_cov', 'wing_cov', 13], ['wing_sec', 'wing_sec', 13], ['wing_pri', 'wing_pri', 13],
  ['spear', 'spear', 15], ['spear_glow', 'spear_glow_geo', 15], ['trail_1', 'trail', 15], ['trail_2', 'trail', 15],
  ['cubes_a', 'cubes_a', 13], ['cubes_b', 'cubes_b', 13], ['cubes_c', 'cubes_c', 13],
];
const PART_INDEX = Object.fromEntries(PARTS.map(([n], i) => [n, i + 1]));
const uuidOf = n => `524c4b4d-4247-4400-8000-${PART_INDEX[n].toString(16).padStart(12, '0')}`;
const uuidInts = n => `[I;1380731725,1111966720,-2147483648,${PART_INDEX[n]}]`;
const itemId = m => `rlk:mboss/guardian/${m}`;

// ---- resource pack: textures, models, item definitions -----------------------------------
// --no-paint skips the sprites; --paint a,b repaints only those (both for quick iteration).
const sprites = flag('--no-paint') ? null : paintGuardianTextures(rp, arg('--paint') ? arg('--paint').split(',') : null);
const models = partModels();
for (const [name, els] of Object.entries(models)) checkBounds(name, els);
function writeModel(name, els) {
  const used = [...new Set(els.flatMap(e => Object.values(e.faces).map(f => f.texture.slice(1))))];
  const textures = Object.fromEntries(used.map(t => [t, spriteId(t)]));
  json(path.join(assets, 'models/item/mboss/guardian', name + '.json'), {ambientocclusion: false, textures: {...textures, particle: spriteId(used[0])}, elements: els});
}
const item = (name, model, tint = null) => json(path.join(assets, 'items/mboss/guardian', name + '.json'),
  {model: {type: 'minecraft:model', model: 'rlk:item/mboss/guardian/' + model, ...(tint === null ? {} : {tints: [{type: 'minecraft:constant', value: tint}]})}});
for (const [name, els] of Object.entries(models)) writeModel(name, els);
const PLAIN = ['pelvis', 'skirt_f', 'skirt_o', 'tail', 'leg_r', 'leg_l', 'torso', 'head', 'halo', 'halo_glow', 'r_upper', 'r_fore', 'r_hand_fist', 'r_hand_open',
  'l_upper', 'l_fore', 'l_hand_open', 'l_hand_fist', 'bracket', 'shield', 'shield_eye', 'wing_cov', 'wing_sec', 'wing_pri', 'spear', 'cubes_a', 'cubes_b', 'cubes_c'];
for (const n of PLAIN) item(n, n);
// Element looks (model.md section 4). Eye: the gem/iris/field of the shield; spear: the head
// enchanted in the element colour; glow: the aura card along the blade and shaft.
export const ELEMENTS = {
  geo: {id: 0, eye: null, spear: null, glow: 0xE4B43C},
  pyro: {id: 1, eye: 0xFF8A4C, spear: 0xFFB088, glow: 0xFF7A3C},
  hydro: {id: 2, eye: 0x5CC8FF, spear: 0x9CDCFF, glow: 0x4CB8FF},
  electro: {id: 3, eye: 0xE484FC, spear: 0xEEB4FF, glow: 0xD46CFC},
  cryo: {id: 4, eye: 0xA2FEFD, spear: 0xD4FFFE, glow: 0x8CF0FF},
  gold: {id: 5, eye: 0xFCE484, spear: 0xFFF2B8, glow: 0xFCD84C},
  red: {id: 6, eye: 0xE03A3A, spear: 0xFF7A6A, glow: 0xE0303C},
};
for (const [el, c] of Object.entries(ELEMENTS)) {
  item('shield_eye_' + el, c.eye === null ? 'shield_eye' : 'shield_eye_t', c.eye);
  item('spear_' + el, c.spear === null ? 'spear' : 'spear_e', c.spear);
  item('spear_glow_' + el, 'spear_glow', c.glow);
}
item('trail', 'trail', 0xF4D27A);
// Props share the spear model (not rig parts): javelin flight, planted spear, giant fail spears.
item('prop_spear', 'spear');
for (const el of ['red', 'gold', 'hydro', 'electro', 'cryo', 'pyro']) item('prop_spear_' + el, el === 'gold' ? 'spear' : 'spear_e', el === 'gold' ? null : ELEMENTS[el].spear);

// ---- clip sampling -------------------------------------------------------------------------
const EASE = {io: u => u * u * (3 - 2 * u), i: u => u * u, o: u => 1 - (1 - u) * (1 - u), l: u => u};
function accumulate(clip) {
  let prev = structuredClone(DEFAULT_POSE);
  return clip.keys.map(([tick, pose, ease]) => { prev = {...prev, ...structuredClone(pose)}; return {tick, p: prev, ease: ease || 'io'}; });
}
function blend(a, b, u) {
  const o = {};
  for (const key of Object.keys(DEFAULT_POSE)) {
    const x = a[key], y = b[key];
    if (typeof x === 'string') o[key] = u < 1 ? x : y;
    else if (typeof x === 'number') o[key] = x + (y - x) * u;
    else if (x.length === 4) o[key] = slerp(x, y, u);
    else o[key] = lerp(x, y, u);
  }
  return o;
}
function sample(clip, t, ks = accumulate(clip)) {
  if (t <= ks[0].tick) return {...ks[0].p, ph: t / 40};
  for (let i = 1; i < ks.length; i++) if (t <= ks[i].tick) {
    const a = ks[i - 1], b = ks[i], u = (t - a.tick) / Math.max(1e-9, b.tick - a.tick);
    const p = blend(a.p, b.p, EASE[b.ease](u));
    // discrete channels switch exactly at their key
    for (const key of ['rHand', 'lHand']) p[key] = t >= b.tick ? b.p[key] : a.p[key];
    return {...p, ph: t / 40};
  }
  return {...ks[ks.length - 1].p, ph: t / 40};
}
const TRAIL_LAG = [1, 2].map(n => .55 * n), TRAIL_TAPER = [.72, .45];
function frame(clip, t, ks) {
  const warns = [];
  const p = sample(clip, t, ks);
  const o = solve(p, {warn: m => warns.push(m)});
  for (const [i, lag] of TRAIL_LAG.entries()) {
    const tt = Math.max(0, t - lag), pp = sample(clip, tt, ks);
    const sp = solve(pp).spear;
    const on = p.trail > .5 && pp.spearS > .5 && t >= 1;
    o['trail_' + (i + 1)] = {t: sp.t, q: sp.q, s: on ? [TRAIL_TAPER[i] * p.trail, 1, TRAIL_TAPER[i] * p.trail] : [0, 0, 0]};
  }
  const d = {};
  for (const [n] of PARTS) d[n] = toDisplay(n, o[n], n.startsWith('trail') ? 'trail_1' : n);
  return {d, p, warns};
}
// Tolerances for the client-side interpolation check (display space).
const TOL_T = .012, TOL_S = .015;
const TOL_R = {spear: .5, spear_glow: .8, trail_1: .8, trail_2: .8, wing_pri: .9, wing_sec: 1, wing_cov: 1.2, shield: 1, bracket: 1, halo: 1.5, halo_glow: 2};
function interp(a, b, u) { return {t: lerp(a.t, b.t, u), q: slerp(a.q, b.q, u), s: lerp(a.s, b.s, u)}; }
function close(x, y, n) {
  const big = Math.max(...y.s.map(Math.abs), ...x.s.map(Math.abs));
  if (big < 1e-4) return true;           // hidden both ways
  if (len(sub(x.t, y.t)) > TOL_T) return false;
  if (Math.max(...x.s.map((v, i) => Math.abs(v - y.s[i]))) > TOL_S * Math.max(1, big)) return false;
  return qAngle(x.q, y.q) <= (TOL_R[n] ?? 1.6);
}
function segments(seq, n, minFirst) {
  const L = seq.length - 1, out = [];
  let a = 0;
  while (a < L) {
    let b = a + 1;
    const fits = bb => { for (let t = a + 1; t < bb; t++) if (!close(interp(seq[a], seq[bb], (t - a) / (bb - a)), seq[t], n)) return false; return true; };
    while (b + 1 <= L && fits(b + 1)) b++;
    if (a === 0 && b < minFirst) b = Math.min(L, minFirst);
    out.push([a, b]);
    a = b;
  }
  return out;
}
const f6 = x => (Math.abs(x) < 5e-7 ? 0 : x).toFixed(5).replace(/\.?0+$/, '') + 'f';
const arr = a => '[' + a.map(f6).join(',') + ']';
const nbt = v => `{translation:${arr(v.t)},left_rotation:${arr(v.q)},scale:${arr(v.s)},right_rotation:[0f,0f,0f,1f]}`;
const MODEL_OF = {rHand: ['r_hand', {fist: 'r_hand_fist', open: 'r_hand_open'}], lHand: ['l_hand', {fist: 'l_hand_fist', open: 'l_hand_open'}]};
const swapLine = (part, model) => `data modify entity ${uuidOf(part)} item.components."minecraft:item_model" set value "${itemId(model)}"`;

// ---- compile clips -------------------------------------------------------------------------
// --debug-dp <dir>: also writes the exact per-tick poses (gd_dbg/<clip>/<t>) and a copy of the
// rig functions into a scratch datapack root, for the offline renderer. Never the real pack.
const debugDp = arg('--debug-dp') && path.resolve(arg('--debug-dp'));
if (debugDp) fs.rmSync(path.join(debugDp, 'data/rlk/function/gd_dbg'), {recursive: true, force: true});
const putDebug = (n, lines) => put(path.join(debugDp, 'data/rlk/function', n + '.mcfunction'), lines.join('\n'));
const clipInfo = [], allWarn = new Set();
CLIPS.forEach((c, id) => { c.id = id; });
const byName = Object.fromEntries(CLIPS.map(c => [c.name, c]));
for (const c of CLIPS) {
  if (c.keys[0][0] !== 0) throw new Error(`clip ${c.name}: first key must be tick 0`);
  if (c.keys[c.keys.length - 1][0] !== c.len) throw new Error(`clip ${c.name}: last key ${c.keys[c.keys.length - 1][0]} != len ${c.len}`);
  if (c.next && !byName[c.next]) throw new Error(`clip ${c.name}: unknown next ${c.next}`);
  const ks = accumulate(c);
  const frames = Array.from({length: c.len + 1}, (_, t) => frame(c, t, ks));
  frames.forEach((f, t) => f.warns.forEach(w => allWarn.add(`${c.name} t${t}: ${w}`)));
  const byTick = new Map();
  const add = (t, line) => { if (!byTick.has(t)) byTick.set(t, []); byTick.get(t).push(line); };
  let keyCount = 0;
  for (const [n] of PARTS) {
    const seq = frames.map(f => f.d[n]);
    for (const [a, b] of segments(seq, n, c.blend ?? 3)) {
      add(a, `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:${b - a},transformation:${nbt(seq[b])}}`);
      keyCount++;
    }
  }
  for (const [ch, [part, map]] of Object.entries(MODEL_OF)) {
    frames.forEach((f, t) => { if (t === 0 || f.p[ch] !== frames[t - 1].p[ch]) add(t, swapLine(part, map[f.p[ch]])); });
  }
  if (debugDp) frames.forEach((f, t) => putDebug(`gd_dbg/${c.name}/${t}`, [...PARTS.map(([n]) => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(f.d[n])}}`),
    ...Object.entries(MODEL_OF).map(([ch, [part, map]]) => swapLine(part, map[f.p[ch]]))]));
  const ticks = [...byTick.keys()].sort((x, y) => x - y);
  for (const t of ticks) fn(`c/${c.name}/k/${t}`, byTick.get(t));
  // per-clip runner: wrap / chain / hold, then a binary dispatch over the key ticks
  const head = [`# ${c.name}: ${c.len} t${c.loop ? ', loop' : c.next ? `, then ${c.next}` : ', holds the last pose'}. @s = rig anchor.`];
  if (c.loop) head.push(`execute if score @s gdRigT matches ${c.len}.. run scoreboard players set @s gdRigT 0`);
  else if (c.next) head.push(`execute if score @s gdRigT matches ${c.len}.. run return run function ${NS}/start/${c.next}`);
  else head.push(`execute if score @s gdRigT matches ${c.len + 1}.. run return run scoreboard players set @s gdRigT ${c.len + 1}`);
  const runTicks = ticks;
  const tree = (lo, hi, list, prefix) => {
    if (list.length <= 6) return list.map(t => `execute if score @s gdRigT matches ${t} run return run function ${NS}/c/${c.name}/k/${t}`);
    const mid = list[Math.floor(list.length / 2) - 1];
    const L = list.filter(t => t <= mid), R = list.filter(t => t > mid);
    fn(`c/${c.name}/b/${L[0]}_${L[L.length - 1]}`, tree(0, 0, L));
    fn(`c/${c.name}/b/${R[0]}_${R[R.length - 1]}`, tree(0, 0, R));
    return [`execute if score @s gdRigT matches ..${mid} run return run function ${NS}/c/${c.name}/b/${L[0]}_${L[L.length - 1]}`,
      `function ${NS}/c/${c.name}/b/${R[0]}_${R[R.length - 1]}`];
  };
  fn(`c/${c.name}/run`, [...head, ...tree(0, 0, runTicks)]);
  fn(`play/${c.name}`, [`# Play clip ${c.name} (${c.len} t) from its tick 0 at the next rig/tick (the same game tick when rig/tick runs later). @s = rig anchor.`, `scoreboard players set @s gdRigC ${c.id}`, 'scoreboard players set @s gdRigT -1']);
  fn(`start/${c.name}`, [`# Internal: chain into ${c.name} now (tick 0 applied immediately). @s = rig anchor.`, `scoreboard players set @s gdRigC ${c.id}`, 'scoreboard players set @s gdRigT 0', `function ${NS}/c/${c.name}/k/0`]);
  clipInfo.push({id: c.id, name: c.name, len: c.len, loop: !!c.loop, next: c.next || null, events: c.events || {}, keyFiles: ticks.length, keys: keyCount, note: c.note || ''});
}
// global dispatch on the clip id
{
  const ids = CLIPS.map(c => c.id);
  const tree = list => {
    if (list.length <= 6) return list.map(i => `execute if score @s gdRigC matches ${i} run return run function ${NS}/c/${CLIPS[i].name}/run`);
    const mid = list[Math.floor(list.length / 2) - 1], L = list.filter(i => i <= mid), R = list.filter(i => i > mid);
    fn(`d/${L[0]}_${L[L.length - 1]}`, tree(L)); fn(`d/${R[0]}_${R[R.length - 1]}`, tree(R));
    return [`execute if score @s gdRigC matches ..${mid} run return run function ${NS}/d/${L[0]}_${L[L.length - 1]}`, `function ${NS}/d/${R[0]}_${R[R.length - 1]}`];
  };
  fn('run', ['# Current clip -> its runner. @s = rig anchor.', ...tree(ids)]);
}

// ---- API functions -----------------------------------------------------------------------
const rest = frame(byName.idle, 0, accumulate(byName.idle)).d;
const TAGS = n => `["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_guardian_part","rlk_mb_gp_${n}"]`;
const summon = ([n, model, bright]) => `summon minecraft:item_display ~ ~ ~ {UUID:${uuidInts(n)},Tags:${TAGS(n)},billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:2.5f,width:16f,height:16f,shadow_radius:0f,brightness:{block:${bright},sky:15},transformation:${nbt(rest[n])},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${itemId(model)}"}}}`;
fn('init', ['# Rig objectives. Safe to call on every load.', ...['gdRigC', 'gdRigT', 'gdRigF', 'gdRigEye', 'gdRigSp', 'gdRigY'].map(o => `scoreboard objectives add ${o} dummy`)]);
fn('spawn', ['# @s = rig anchor (the boss body), positioned and rotated where she should appear.',
  '# Summons the 29 parts with fixed UUIDs in the idle pose and starts the idle clip.',
  `function ${NS}/init`, `function ${NS}/kill`, ...PARTS.map(summon),
  `scoreboard players set @s gdRigC ${byName.idle.id}`, 'scoreboard players set @s gdRigT 0', 'scoreboard players set @s gdRigF 0',
  'execute unless score @s gdRigEye matches 0.. run scoreboard players set @s gdRigEye 0',
  'execute unless score @s gdRigSp matches 0.. run scoreboard players set @s gdRigSp 0',
  `function ${NS}/look_apply`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow`]);
fn('follow', ['# Parts follow the executor position and yaw (run rotated as the anchor, pitch 0).', ...PARTS.map(([n]) => `tp ${uuidOf(n)} ~ ~ ~ ~ ~`)]);
fn('tick', ['# @s = rig anchor, at its feet. Once per game tick.',
  `execute unless entity ${uuidOf('torso')} run function ${NS}/spawn`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow`,
  'scoreboard players add @s gdRigT 1',
  `function ${NS}/run`,
  `execute if score @s gdRigF matches 1.. run function ${NS}/flash_tick`]);
fn('kill', ['# Removes every rig part (the props have their own tag).', 'kill @e[type=item_display,tag=rlk_mb_guardian_part]']);
fn('uninstall', ['# Removes the rig, its props and its objectives.', `function ${NS}/kill`, `function ${NS}/prop/clear`, 'kill @e[type=marker,tag=rlk_mb_gd_face]',
  ...['gdRigC', 'gdRigT', 'gdRigF', 'gdRigEye', 'gdRigSp', 'gdRigY'].map(o => `scoreboard objectives remove ${o}`)]);
fn('flash', ['# Hit feedback: a white outline for 3 ticks. @s = rig anchor.', 'scoreboard players set @s gdRigF 4',
  ...PARTS.filter(([n]) => !['halo_glow', 'spear_glow', 'trail_1', 'trail_2'].includes(n)).map(([n]) => `data merge entity ${uuidOf(n)} {Glowing:1b,glow_color_override:16772300}`)]);
fn('flash_tick', ['scoreboard players remove @s gdRigF 1', `execute if score @s gdRigF matches 0 run function ${NS}/flash_off`]);
fn('flash_off', PARTS.map(([n]) => `data merge entity ${uuidOf(n)} {Glowing:0b}`));
// element looks: eye (shield gem/iris/field) and spear (head enchant + aura colour)
const elNames = Object.keys(ELEMENTS);
for (const el of elNames) {
  const id = ELEMENTS[el].id;
  fn(`eye/${el}`, [`# Shield eye in the ${el} colour. @s = rig anchor.`, `scoreboard players set @s gdRigEye ${id}`, swapLine('shield_eye', 'shield_eye_' + el)]);
  fn(`spear/${el}`, [`# Spear enchant: ${el}. @s = rig anchor.`, `scoreboard players set @s gdRigSp ${id}`, swapLine('spear', 'spear_' + el), swapLine('spear_glow', 'spear_glow_' + el)]);
  fn(`tint/${el}`, [`# Shield eye and spear both in the ${el} look. @s = rig anchor.`, `function ${NS}/eye/${el}`, `function ${NS}/spear/${el}`]);
}
fn('look_apply', ['# Re-applies the stored eye/spear looks (after a respawn). @s = rig anchor.',
  ...elNames.map(el => `execute if score @s gdRigEye matches ${ELEMENTS[el].id} run function ${NS}/eye/${el}`),
  ...elNames.map(el => `execute if score @s gdRigSp matches ${ELEMENTS[el].id} run function ${NS}/spear/${el}`)]);
fn('eye/by_elem', ['# Eye look from #elem-style ids in @s gdRigEye (0 geo, 1 pyro, 2 hydro, 3 electro, 4 cryo, 5 gold, 6 red).', `function ${NS}/look_apply`]);
// facing helpers (the parts take the anchor's yaw every tick)
fn('face/player', ['# Turn the anchor to face the nearest player (yaw only). @s = rig anchor.',
  'execute facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0']);
fn('face/track', ['# Turn the anchor toward the nearest player by at most 12 degrees per call. @s = rig anchor.',
  'execute store result score #yaw gdRigY run data get entity @s Rotation[0] 100',
  'execute facing entity @p[gamemode=!spectator] feet run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_aux","rlk_mb_gd_face"]}',
  'execute as @e[type=marker,tag=rlk_mb_gd_face,limit=1] at @s facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0',
  'execute store result score #yawT gdRigY run data get entity @e[type=marker,tag=rlk_mb_gd_face,limit=1] Rotation[0] 100',
  'kill @e[type=marker,tag=rlk_mb_gd_face]',
  'scoreboard players operation #yawT gdRigY -= #yaw gdRigY',
  'execute if score #yawT gdRigY matches 18000.. run scoreboard players remove #yawT gdRigY 36000',
  'execute if score #yawT gdRigY matches ..-18000 run scoreboard players add #yawT gdRigY 36000',
  'execute if score #yawT gdRigY matches 1201.. run scoreboard players set #yawT gdRigY 1200',
  'execute if score #yawT gdRigY matches ..-1201 run scoreboard players set #yawT gdRigY -1200',
  'scoreboard players operation #yaw gdRigY += #yawT gdRigY',
  'execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw gdRigY']);
fn('face/set', ['# Set the anchor yaw: function rlk:mboss/guardian/rig/face/set {yaw:<degrees>}. @s = rig anchor.', '$rotate @s $(yaw) 0']);
// props: spear copies that are not rig parts (javelin flight, giant fail spears)
fn('prop/spear', ['# Summons a free spear prop at the execution position/rotation, tagged rlk_mb_gd_prop + rlk_mb_gd_prop_new.',
  '# The pattern code moves/poses it (model frame: grip at the origin, tip along +Y). Scale 2.2 = her spear.',
  'tag @e[tag=rlk_mb_gd_prop_new] remove rlk_mb_gd_prop_new',
  `summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_prop","rlk_mb_gd_prop_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:3f,width:16f,height:16f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${itemId('prop_spear')}"}}}`,
  'execute rotated ~ 0 run tp @e[type=item_display,tag=rlk_mb_gd_prop_new,limit=1] ~ ~ ~ ~ 0']);
fn('prop/clear', ['kill @e[type=item_display,tag=rlk_mb_gd_prop]']);

// ---- manifest ------------------------------------------------------------------------------
json(path.join(here, 'mboss_guardian_rig_manifest.json'), {
  parts: PARTS.map(([n, m, b]) => ({part: n, uuid: uuidOf(n), model: m, brightness: b, scale: PART_SCALE[n.startsWith('trail') ? 'trail_1' : n]})),
  clips: clipInfo,
  elements: Object.fromEntries(Object.entries(ELEMENTS).map(([k, v]) => [k, {id: v.id, eye: v.eye === null ? 'painted' : '#' + v.eye.toString(16).padStart(6, '0'), glow: '#' + v.glow.toString(16).padStart(6, '0')}])),
  objectives: {gdRigC: 'current clip id (anchor)', gdRigT: 'tick within the clip (anchor; -1 = queued by play)', gdRigF: 'hit flash countdown', gdRigEye: 'eye look id', gdRigSp: 'spear look id', gdRigY: 'face/track scratch'},
  textures: sprites ? sprites.length : 'not repainted',
});
for (const w of [...allWarn].slice(0, 40)) console.warn('warn:', w);
const files = clipInfo.reduce((a, c) => a + c.keyFiles, 0);
console.log(`Built the Corrupted Guardian rig: ${PARTS.length} parts, ${CLIPS.length} clips, ${files} key files, ${clipInfo.reduce((a, c) => a + c.keys, 0)} part keys${allWarn.size ? `, ${allWarn.size} reach warnings` : ''}.`);
if (debugDp) fs.cpSync(rigDir, path.join(debugDp, 'data/rlk/function/mboss/guardian/rig'), {recursive: true});
