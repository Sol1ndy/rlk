// Display-entity rig of the experimental field generator (실험성 역장 발생 장치, nameplate 브레게 프로토타입), the third
// mid-boss: a floating brass gravity device (D = 7.0 b).
// node tools/build_mboss_fieldgen_rig.mjs --resourcepack <unpacked pack> [--datapack <pack>] [--no-paint | --paint a,b]
//                                         [--debug-dp <scratch dir> [--debug-clips a,b | all]] [--allow-steps]
//
// Writes
//   RP  assets/rlk/textures/mboss/fieldgen/*.png (fieldgen_paint.mjs) + item atlas entries
//       assets/rlk/models/item/mboss/fieldgen/*.json, assets/rlk/items/mboss/fieldgen/*.json
//       (also the props: the falling bomb and the drill missile, not rig parts)
//   DP  data/rlk/function/mboss/fieldgen/rig/** (owned by this generator, rebuilt from scratch on every run)
//   tools/mboss_fieldgen_rig_manifest.json (parts, clips, events, anchors, form switches, hidden spans, form states,
//   looks, crack stages, props, objectives)
//
// Runtime model (the contract for the pattern code is tools/mboss_fieldgen_rig_api.md):
//   * One superset rig for the seven body configurations (dormant, cruise, field, core-up, tower, laser, deployed): 29
//     item_display parts with FIXED UUIDs 524c4b4d-4647-4400-8000-0000000000NN, every one a free body round the ring
//     centre (model.md §0: nothing is connected). Unused parts sit at scale 0. All parts carry rlk_room, rlk_mb_aux,
//     rlk_mb_part, rlk_mb_fieldgen_part, rlk_mb_fg_<part>.
//   * The anchor (the boss body, on the floor under the ring axis) runs rig/tick each tick: the parts follow its
//     position and yaw (tp, teleport_duration 1) and the current clip applies its keys (the shared compiler
//     mboss_rig_compile.mjs: interpolation segments, rotation checks, binary dispatch).
//   * Rig state on the anchor: fgRigForm (the stored form, for respawns), fgRigLook (the module look: 0 idle,
//     1 charge, 2 field, 3 groggy, 4 off), fgRigCrack (the 20-hit bubble stage 0-4), fgRigTmp (1 while a clip shows a
//     temporary look).
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {paintFieldgenTextures, spriteId, fieldgenSprites} from './fieldgen_paint.mjs';
import {partModels, checkBounds, RING, EMPTY, SPIKE_TIP} from './fieldgen_geometry.mjs';
import {solve, toDisplay, PART_SCALE, FORMS, radial} from './fieldgen_pose.mjs';
import {CLIPS, accumulate, sampleClip as sample, restPose, FORM_HOLD, spinTurns} from './fieldgen_clips.mjs';
import {add, rot} from './mboss_rig_math.mjs';
import {createRigCompiler, nbt} from './mboss_rig_compile.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const arg = n => { const i = process.argv.indexOf(n); return i < 0 ? null : process.argv[i + 1]; };
const flag = n => process.argv.includes(n);
const dp = path.resolve(arg('--datapack') || path.join(here, '..'));
const rp = arg('--resourcepack') && path.resolve(arg('--resourcepack'));
if (!rp) throw new Error('--resourcepack <unpacked pack> is required');
const put = (p, s) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, s.endsWith('\n') ? s : s + '\n'); };
const json = (p, o) => put(p, JSON.stringify(o, null, 2));
const NS = 'rlk:mboss/fieldgen/rig';
const rigDir = path.join(dp, 'data/rlk/function/mboss/fieldgen/rig');
fs.rmSync(rigDir, {recursive: true, force: true});
const fn = (n, lines) => put(path.join(rigDir, n + '.mcfunction'), (Array.isArray(lines) ? lines : [lines]).join('\n'));
const assets = path.join(rp, 'assets/rlk');

// ---- parts --------------------------------------------------------------------------------------------------------
// [part, default item model, block brightness]
const PARTS = [
  ['ring', 'ring', 14], ['ring_glow', 'ring_glow_idle', 15], ['hub_eye', 'hub_shut', 14], ['halo', 'halo', 14], ['halo2', 'halo2', 15],
  ['core', 'core', 13], ['core_eye', 'eye_idle', 15], ['core_arch', 'core_arch', 13], ['core_brim', 'core_brim', 14], ['core_glow', 'glow_charge', 15], ['core_shell', EMPTY, 15],
  ['spike_l', 'spike_l', 14], ['spike_r', 'spike_r', 14], ['medal_eye', 'medal_eye', 14], ['medal_gear', 'medal_gear', 14],
  ['drill_fl', 'drill', 14], ['drill_fr', 'drill', 14], ['drill_bl', 'drill', 14], ['drill_br', 'drill', 14],
  ['plate', 'plate', 14], ['plate2', 'plate2', 14], ['pendulum', 'pendulum', 14], ['pend_glow', 'pend_glow', 15],
  ['beam_l', 'beam_gold', 15], ['beam_r', 'beam_gold', 15], ['column', 'col_gold', 15],
  ['tower_col', 'tower_col', 14], ['tower_t1', 'tower_t1', 14], ['tower_t2', 'tower_t2', 15],
];
if (PARTS.length > 32) throw new Error(`${PARTS.length} parts: the budget is 32`);
const PART_INDEX = Object.fromEntries(PARTS.map(([n], i) => [n, i + 1]));
const uuidOf = n => `524c4b4d-4647-4400-8000-${PART_INDEX[n].toString(16).padStart(12, '0')}`;
const uuidInts = n => `[I;1380731725,1179075584,-2147483648,${PART_INDEX[n]}]`;
const itemId = m => `rlk:mboss/fieldgen/${m}`;
const FORM_ID = {dormant: 1, cruise: 2, field: 3, coreup: 4, tower: 5, laser: 6, deployed: 7};
// Module looks (look/<name>): the item models of the look parts. The shell shows the bubble at the stored crack stage
// in the field look only.
const LOOK_ID = {idle: 0, charge: 1, field: 2, groggy: 3, off: 4};
const LOOKS = {
  idle: {ring_glow: 'ring_glow_idle', hub_eye: 'hub_shut', core_eye: 'eye_idle', halo: 'halo', halo2: 'halo2', medal_eye: 'medal_eye', medal_gear: 'medal_gear'},
  charge: {ring_glow: 'ring_glow_hot', hub_eye: 'hub_hot', core_eye: 'eye_charge', halo: 'halo', halo2: 'halo2', medal_eye: 'medal_eye_hot', medal_gear: 'medal_gear_hot'},
  field: {ring_glow: 'ring_glow_hot', hub_eye: 'hub_open', core_eye: 'eye_field', halo: 'halo_v', halo2: 'halo2_v', medal_eye: 'medal_eye', medal_gear: 'medal_gear'},
  groggy: {ring_glow: 'ring_glow_off', hub_eye: 'hub_shut', core_eye: 'eye_dim', halo: 'halo', halo2: 'halo2', medal_eye: 'medal_eye', medal_gear: 'medal_gear'},
  off: {ring_glow: 'ring_glow_off', hub_eye: 'hub_shut', core_eye: 'eye_dim', halo: 'halo', halo2: 'halo2', medal_eye: 'medal_eye', medal_gear: 'medal_gear'},
};
const LOOK_NOTE = {
  idle: 'seam and ports idle gold, the keystone iris shut (sunburst fan), the core eye gold, copper halo + gold inner ring',
  charge: 'seam, ports and bomb ports hot white-gold, the iris hot, the eye white-gold, the medallion faces hot (attacks)',
  field: 'seam hot, the iris open, the eye red-orange, both halos violet, the white-gold bubble round the core at the stored crack stage (역장)',
  groggy: 'seam off, the iris shut, the eye dim amber',
  off: 'seam off, the iris shut, the eye dim (dormant, death)',
};
const SHELL = s => (s >= 4 ? 'bubble_burst' : 'bubble_' + s);
// Clip-driven model channels: core_glow (charge sphere / white-gold flash / the exposed gold sphere), the beams (gold
// laser / link beam), the column (gold / violet).
const MODEL_OF = {glowLook: ['core_glow', {charge: 'glow_charge', flash: 'glow_flash', gold: 'glow_gold'}],
  beamLook: ['beam_l', {gold: 'beam_gold', link: 'beam_link'}], beamLook2: ['beam_r', {gold: 'beam_gold', link: 'beam_link'}],
  colLook: ['column', {gold: 'col_gold', violet: 'col_violet'}]};

// ---- resource pack: textures, models, item definitions --------------------------------------------------------------
const sprites = flag('--no-paint') ? null : paintFieldgenTextures(rp, arg('--paint') ? arg('--paint').split(',') : null);
const models = partModels();
for (const [name, els] of Object.entries(models)) checkBounds(name, els);
const modelDir = path.join(assets, 'models/item/mboss/fieldgen'), itemDir = path.join(assets, 'items/mboss/fieldgen');
fs.rmSync(modelDir, {recursive: true, force: true});
fs.rmSync(itemDir, {recursive: true, force: true});
const spriteTable = fieldgenSprites();
for (const [name, els] of Object.entries(models)) {
  const used = [...new Set(els.flatMap(e => Object.values(e.faces).map(f => f.texture.slice(1))))];
  for (const u of used) if (!spriteTable[u]) throw new Error(`model ${name}: unknown sprite ${u}`);
  const tex = used.length ? used : ['cream'];
  json(path.join(modelDir, name + '.json'), {ambientocclusion: false, textures: {...Object.fromEntries(used.map(t => [t, spriteId(t)])), particle: spriteId(tex[0])}, elements: els});
  json(path.join(itemDir, name + '.json'), {model: {type: 'minecraft:model', model: 'rlk:item/mboss/fieldgen/' + name}});
}
// atlas budget (0.5 M px, sides <= 512, multiples of 16)
let atlasPx = 0;
for (const [n, [w, h]] of Object.entries(spriteTable)) {
  if (w > 512 || h > 512 || w % 16 || h % 16) throw new Error(`sprite ${n} ${w}x${h}: sides <= 512, multiples of 16`);
  atlasPx += w * h;
}
if (atlasPx > 5e5) throw new Error(`field generator sprites use ${atlasPx} px of the atlas (budget 0.5 M)`);
const elementCount = Object.fromEntries(Object.entries(models).map(([n, e]) => [n, e.length]));

// ---- clip sampling ------------------------------------------------------------------------------------------------
function frame(clip, t, ks) {
  const p = sample(clip, t, ks);
  p.beamLook2 = p.beamLook;
  const o = solve(p);
  const d = {};
  for (const [n] of PARTS) d[n] = toDisplay(n, o[n]);
  return {d, p, o};
}
const clipFrames = (clip, ks = accumulate(clip)) => Array.from({length: clip.len + 1}, (_, t) => frame(clip, t, ks));
// Fx anchors (rig coordinates, blocks from the anchor: x the device's left, y up, -z its front; body frame ^x ^y ^-z).
const r3 = v => v.map(x => +x.toFixed(3) || 0);
function at(o, n, pt) {
  const v = o[n], k = PART_SCALE[n] / 16;
  return add(v.t, rot(v.q, [pt[0] * v.s[0] * k, pt[1] * v.s[1] * k, pt[2] * v.s[2] * k]));
}
// a point of the ring model at facet azimuth k * 22.5, radius rad and height y (ring model units)
const ringAt = (o, k, rad, y) => { const a = k * 22.5 * Math.PI / 180; return at(o, 'ring', [Math.sin(a) * rad, y, -Math.cos(a) * rad]); };
function anchors(o) {
  const A = {
    ring_centre: o.ring.t, core: o.core.t, eye: at(o, 'core_eye', [0, 0, -22]),
    spike_tip_l: at(o, 'spike_l', [SPIKE_TIP, 0, 0]), spike_tip_r: at(o, 'spike_r', [-SPIKE_TIP, 0, 0]),
    medal_e: at(o, 'medal_eye', [0, 0, -2.8]), medal_g: at(o, 'medal_gear', [0, 0, -2.6]),
    beam_spot_l: at(o, 'beam_l', [0, -16, 0]), beam_spot_r: at(o, 'beam_r', [0, -16, 0]),
    col_end: at(o, 'column', [0, -16, 0]),
    vent_l: ringAt(o, 5, 20.25, RING.yTop + .2), vent_r: ringAt(o, -3, 20.25, RING.yTop + .2),
    pend_tip: at(o, 'pendulum', [0, -21, 0]), tower_top: at(o, 'tower_col', [0, 21.8, 0]),
  };
  for (let i = 0; i < 8; i++) A['port_' + i] = ringAt(o, 2 * i + 1, 18.25, RING.yTier - .2);
  return Object.fromEntries(Object.entries(A).map(([k2, v]) => [k2, r3(v)]));
}

// ---- compile clips --------------------------------------------------------------------------------------------------
// --debug-dp <dir>: also writes the rest poses (fg_dbg/rest_<form>), the exact per-tick poses of the --debug-clips
// (fg_dbg/<clip>/<t>; 'all' for every clip) and a link to the rig functions into a scratch datapack root, for the
// offline renderer. Never the real pack.
const debugDp = arg('--debug-dp') && path.resolve(arg('--debug-dp'));
const debugClips = (arg('--debug-clips') || '').split(',').filter(Boolean);
const debugOf = c => debugDp && (debugClips.includes('all') || debugClips.includes(c.name));
if (debugDp) fs.rmSync(path.join(debugDp, 'data/rlk/function/fg_dbg'), {recursive: true, force: true});
const putDebug = (n, lines) => put(path.join(debugDp, 'data/rlk/function', n + '.mcfunction'), lines.join('\n'));
let debugFrames = null;
const putDebugPose = (n, lines) => {
  const t = +n.slice(n.lastIndexOf('/') + 1), lk = debugFrames[t].p.lk;
  putDebug(n, [...lines, lk === 'el' ? `function ${NS}/look_apply` : `function ${NS}/look/${lk}_swap`]);
};
const TOL = {t: .012, s: .015, rDefault: 1.0, r: {ring: .25, ring_glow: .25, halo: .4, halo2: .5, spike_l: .4, spike_r: .4, pendulum: .5, pend_glow: .8,
  beam_l: .3, beam_r: .3, column: .5, core: .6, core_eye: .5, core_arch: .5, core_brim: .5, core_glow: 2, core_shell: 1.5, tower_t1: .5, tower_t2: .5}};
const swapLine = (part, model) => `data modify entity ${uuidOf(part)} item.components."minecraft:item_model" set value "${itemId(model)}"`;
const mkCompiler = debug => createRigCompiler({ns: NS, obj: 'fgRig', fn, parts: PARTS.map(([n]) => n), uuidOf, tol: TOL, modelOf: MODEL_OF, swapLine,
  debug: debug ? {put: putDebugPose, dir: 'fg_dbg'} : null});
const compiler = mkCompiler(false), debugCompiler = debugDp ? mkCompiler(true) : null;
const clipInfo = [], motionErrors = [], alignErrors = [], warns = new Set();
// Alignment checks per frame: no horizontal root travel (the module moves the body), the pendulum tip, the drill tips
// and the ring above the floor while visible, events inside the clip.
function alignment(c, frames) {
  const out = [];
  frames.forEach((f, t) => {
    if (Math.abs(f.p.pos[0]) > 1e-9 || Math.abs(f.p.pos[2]) > 1e-9) out.push(`${c.name} t${t}: root travel (x/z must be 0)`);
    if (f.p.vis < .5) return;
    const tip = at(f.o, 'pendulum', [0, -21, 0])[1];
    if (tip < .02) out.push(`${c.name} t${t}: pendulum tip ${tip.toFixed(2)} b`);
    for (const n of ['drill_fl', 'drill_fr', 'drill_bl', 'drill_br']) { const y = at(f.o, n, [0, -16, 0])[1]; if (y < .02 && f.o[n].s[0] > .05) out.push(`${c.name} t${t}: ${n} tip ${y.toFixed(2)} b`); }
    const ringLow = f.o.ring.t[1] - Math.abs(Math.sin(Math.max(Math.abs(f.p.rot[0]), Math.abs(f.p.rot[2])) * Math.PI / 180)) * 3.5 - .72;
    if (ringLow < -.05) out.push(`${c.name} t${t}: ring rim ${ringLow.toFixed(2)} b`);
  });
  for (const [e, t] of Object.entries(c.events || {})) if (!(t >= 0 && t <= c.len)) out.push(`${c.name}: event ${e} at ${t} outside 0..${c.len}`);
  return out;
}
CLIPS.forEach((c, id) => { c.id = id; });
const byName = Object.fromEntries(CLIPS.map(c => [c.name, c]));
for (const c of CLIPS) {
  if (c.keys[0][0] !== 0) throw new Error(`clip ${c.name}: first key must be tick 0`);
  if (c.keys[c.keys.length - 1][0] !== c.len) throw new Error(`clip ${c.name}: last key ${c.keys[c.keys.length - 1][0]} != len ${c.len}`);
  if (c.next && !byName[c.next]) throw new Error(`clip ${c.name}: unknown next ${c.next}`);
  const ks = accumulate(c);
  const frames = clipFrames(c, ks);
  debugFrames = frames;
  alignErrors.push(...alignment(c, frames));
  // temporary looks (lk): a look name shows that look's models without touching fgRigLook; back to 'el' re-applies it
  const extra = t => {
    const out = [], p = frames[t].p, q0 = t ? frames[t - 1].p : null;
    if (!q0) out.push(p.lk === 'el' ? `execute if score @s fgRigTmp matches 1 run function ${NS}/look_apply` : `function ${NS}/look/temp_${p.lk}`);
    else if (p.lk !== q0.lk) out.push(p.lk === 'el' ? `function ${NS}/look_apply` : `function ${NS}/look/temp_${p.lk}`);
    return out;
  };
  const r = (debugOf(c) ? debugCompiler : compiler).compileClip(c, frames, a => frame(c, a + .5, ks), extra);
  motionErrors.push(...r.motionErrors);
  r.warns.forEach(w => warns.add(w));
  const ev = Object.fromEntries(Object.entries(c.events || {}).map(([n, t]) => [n, anchors(frames[Math.min(t, c.len)].o)]));
  for (const [t, f] of c.forms || []) if (!(t >= 0 && t <= c.len) || !FORM_ID[f]) throw new Error(`clip ${c.name}: bad form switch ${t} ${f}`);
  clipInfo.push({...r.info, anchors: ev, ...(c.forms ? {forms: c.forms} : {}), ...(c.hidden ? {hidden: c.hidden} : {}), ...(c.orbit ? {orbit: c.orbit} : {}), spin_turns: spinTurns(c)});
}
if (alignErrors.length) {
  const msg = `clip alignment:\n  ` + alignErrors.slice(0, 60).join('\n  ') + (alignErrors.length > 60 ? `\n  ... ${alignErrors.length} in all` : '');
  if (flag('--allow-steps')) console.warn(msg); else throw new Error(msg);
}
if (motionErrors.length) {
  const msg = `part rotations above 120 degrees per tick or per key:\n  ` + motionErrors.slice(0, 120).join('\n  ') + (motionErrors.length > 120 ? `\n  ... ${motionErrors.length} in all` : '');
  if (flag('--allow-steps')) console.warn(msg); else throw new Error(msg);
}
compiler.writeDispatch(CLIPS);

// ---- API functions --------------------------------------------------------------------------------------------------
const restOf = name => { const o = solve(restPose(name)); return Object.fromEntries(PARTS.map(([n]) => [n, toDisplay(n, o[n])])); };
const REST = Object.fromEntries(Object.keys(FORMS).map(f => [f, restOf(f)]));
// alias tags (short fx-anchor names the module may select by): pend, medal_e, medal_g
const ALIAS = {pend: 'pendulum', medal_e: 'medal_eye', medal_g: 'medal_gear'};
const TAGS = n => `["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_fieldgen_part","rlk_mb_fg_${n}"${Object.entries(ALIAS).filter(([, of]) => of === n).map(([a]) => `,"rlk_mb_fg_${a}"`).join('')}]`;
const summon = ([n, model, bright], pose) => `summon minecraft:item_display ~ ~ ~ {UUID:${uuidInts(n)},Tags:${TAGS(n)},billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:3f,width:16f,height:16f,shadow_radius:0f,brightness:{block:${bright},sky:15},transformation:${nbt(pose)},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${itemId(model)}"}}}`;
const RIG_OBJ = ['fgRigC', 'fgRigT', 'fgRigF', 'fgRigY', 'fgRigForm', 'fgRigLook', 'fgRigCrack', 'fgRigTmp'];
fn('init', ['# Rig objectives. Safe to call on every load.', ...RIG_OBJ.map(o => `scoreboard objectives add ${o} dummy`)]);
const setPose = (form, dur = 0) => PARTS.map(([n]) => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:${dur},transformation:${nbt(REST[form][n])}}`);
const formByScore = Object.entries(FORM_ID);
const stored = ['execute unless score @s fgRigForm matches 1..7 run scoreboard players set @s fgRigForm 2',
  'execute unless score @s fgRigLook matches 0..4 run scoreboard players set @s fgRigLook 0',
  'execute unless score @s fgRigCrack matches 0..4 run scoreboard players set @s fgRigCrack 0'];
fn('spawn', ['# @s = rig anchor (the boss body, on the floor under the ring axis), positioned and rotated where the device',
  `# should appear. Kills old parts, summons the ${PARTS.length} parts in the rest pose of the stored form (fgRigForm, cruise by`,
  '# default), queues that form\'s hold clip and re-applies the stored look and crack stage.',
  `function ${NS}/init`, `function ${NS}/kill`, ...stored, ...PARTS.map(p => summon(p, REST.cruise[p[0]])),
  'scoreboard players set @s fgRigT -1', 'scoreboard players set @s fgRigF 0', 'scoreboard players set @s fgRigTmp 0',
  ...formByScore.map(([f, id]) => `execute if score @s fgRigForm matches ${id} run function ${NS}/form/${f}`),
  `function ${NS}/look_apply`, `execute rotated as @s rotated ~ 0 run function ${NS}/follow`]);
fn('follow', ['# Parts follow the executor position and yaw (run rotated as the anchor, pitch 0).', ...PARTS.map(([n]) => `tp ${uuidOf(n)} ~ ~ ~ ~ ~`)]);
fn('tick', ['# @s = rig anchor, at its feet. Once per game tick. Missing parts respawn in the rest pose of the stored form',
  '# (the clip restarts as that form\'s hold).',
  `execute unless entity ${uuidOf('ring')} run function ${NS}/spawn`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow`,
  'scoreboard players add @s fgRigT 1',
  `function ${NS}/run`,
  `execute if score @s fgRigF matches 1.. run function ${NS}/flash_tick`]);
fn('kill', ['# Removes every rig part (the props have their own tag).', 'kill @e[type=item_display,tag=rlk_mb_fieldgen_part]']);
fn('uninstall', ['# Removes the rig, its props and its objectives.', `function ${NS}/kill`, `function ${NS}/prop/clear`, 'kill @e[type=marker,tag=rlk_mb_fg_face]',
  ...RIG_OBJ.map(o => `scoreboard objectives remove ${o}`)]);
// forms: instant (the clips animate the changes themselves)
const FORM_NOTE = {
  dormant: 'folded on the floor: ring centre 2.15 b, halo and inner ring folded away, core sunk with the arch flat, pods tucked under the ring ends, only the dagger below',
  cruise: 'the compact hover: ring centre 4.5 b, halo +1.6, core tucked in the ring hole, medallions docked at the ring ends, pods under the ring, pendulum tip 0.55 b over the floor',
  field: 'the stack spread: ring centre 5.8 b, the core hanging 1.7 b under the ring, medallions beside it on link beams, pods at core level, plates spread round the violet column, Ousia flame on the cog',
  coreup: 'the core lifted 2.8 b over the ring, the iris and both medallions in a row with their spikes up, roll 10',
  tower: 'the column with two tiers telescoped up, the halo x1.7 at +3.2, the medallions on the column top, end spikes up 45, iris spike up',
  laser: 'the medallions dropped to r 2.8, 2 b under the ring, with the gold beams down-out at 48 degrees (the hold clip counter-orbits them)',
  deployed: 'the lances: spikes and medallions 5.6 b out on both sides, the core hanging, ring centre 5.6 b',
};
for (const [f, id] of Object.entries(FORM_ID)) fn(`form/${f}`, [`# Instant ${f} form: ${FORM_NOTE[f]}; ${FORM_HOLD[f]} queued. Looks are separate (look/*). @s = rig anchor.`,
  `scoreboard players set @s fgRigForm ${id}`, ...setPose(f), `scoreboard players set @s fgRigC ${byName[FORM_HOLD[f]].id}`, 'scoreboard players set @s fgRigT -1']);
// looks
const lookSwaps = look => Object.entries(LOOKS[look]).map(([part, m]) => swapLine(part, m));
const shellLines = look => (look === 'field' ? [0, 1, 2, 3, 4].map(s => `execute if score @s fgRigCrack matches ${s} run ${swapLine('core_shell', SHELL(s))}`) : [swapLine('core_shell', EMPTY)]);
for (const look of Object.keys(LOOKS)) {
  fn(`look/${look}`, [`# Look ${look}: ${LOOK_NOTE[look]}. Stored in fgRigLook (kept over a respawn). @s = rig anchor.`,
    `scoreboard players set @s fgRigLook ${LOOK_ID[look]}`, 'scoreboard players set @s fgRigTmp 0', ...lookSwaps(look), ...shellLines(look)]);
  fn(`look/${look}_swap`, [`# Internal: the ${look} models.`, ...lookSwaps(look), ...shellLines(look)]);
  fn(`look/temp_${look}`, [`# Internal (clips): the ${look} models without changing the stored look; look_apply restores it. @s = rig anchor.`,
    'scoreboard players set @s fgRigTmp 1', `function ${NS}/look/${look}_swap`]);
}
fn('look_apply', ['# Re-applies the stored look fgRigLook and crack stage (after a respawn or a temporary clip look). @s = rig anchor.',
  'scoreboard players set @s fgRigTmp 0',
  ...Object.entries(LOOK_ID).map(([look, id]) => `execute if score @s fgRigLook matches ${id} run function ${NS}/look/${look}_swap`)]);
// crack stages of the field bubble (the 20-hit meter): 0 clean .. 3 heavily cracked, 4 the burst
for (let s = 0; s <= 4; s++) fn(`crack/${s}`, [`# Bubble crack stage ${s} (${s < 4 ? `hits ${s * 5}-${s * 5 + 4} of 20` : 'the burst: play break with it'}). Shown in the field look; stored in fgRigCrack. @s = rig anchor.`,
  `scoreboard players set @s fgRigCrack ${s}`, `execute if score @s fgRigLook matches 2 run ${swapLine('core_shell', SHELL(s))}`]);
// hit flash: a warm white outline for 3 ticks on the solid parts
const OUTLINED = PARTS.filter(([n]) => !['ring_glow', 'halo2', 'core_glow', 'core_shell', 'pend_glow', 'beam_l', 'beam_r', 'column', 'core_eye', 'tower_t2'].includes(n));
fn('flash', ['# Hit feedback: a warm white outline for 3 ticks. @s = rig anchor.', 'scoreboard players set @s fgRigF 4',
  ...OUTLINED.map(([n]) => `data merge entity ${uuidOf(n)} {Glowing:1b,glow_color_override:16774620}`)]);
fn('flash_tick', ['scoreboard players remove @s fgRigF 1', `execute if score @s fgRigF matches 0 run function ${NS}/flash_off`]);
fn('flash_off', ['# End of the hit flash. @s = rig anchor.', ...OUTLINED.map(([n]) => `data merge entity ${uuidOf(n)} {Glowing:0b}`)]);
// facing (the device turns 45-90 degrees per second: 4 per tick)
compiler.writeFace({marker: 'rlk_mb_fg_face', maxDeg: 4});
// props: free item_displays, not rig parts; tags rlk_mb_fg_prop + rlk_mb_fg_prop_<kind>, rlk_mb_fg_prop_new for the
// call's own summons
const PROP_DEF = {bomb: [['bomb', 1, 15]], missile: [['missile', 1, 15]]};
const PROP_NOTE = {
  bomb: 'a falling bomb: a 0.65 b dark bronze sphere with a gold band and a glowing seam (summon at a port anchor, then tp it down with teleport_duration)',
  missile: 'a gold drill missile, 1.4 b, point down (-Y in its frame): turn it with its transformation or summon it rotated',
};
for (const [kind, list] of Object.entries(PROP_DEF)) {
  fn(`prop/${kind}`, [`# Summons ${PROP_NOTE[kind]}, at the execution position and yaw.`,
    '# Tags rlk_room, rlk_mb_aux, rlk_mb_fg_prop, rlk_mb_fg_prop_' + kind + ' and, for this call only, rlk_mb_fg_prop_new.',
    'tag @e[tag=rlk_mb_fg_prop_new] remove rlk_mb_fg_prop_new',
    ...list.map(([m, s, br]) => `summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_prop","rlk_mb_fg_prop_${kind}","rlk_mb_fg_prop_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:3f,width:4f,height:4f,shadow_radius:0f,brightness:{block:${br},sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[${s}f,${s}f,${s}f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${itemId(m)}"}}}`),
    'execute rotated ~ 0 run tp @e[type=item_display,tag=rlk_mb_fg_prop_new] ~ ~ ~ ~ 0']);
}
fn('prop/clear', ['# Removes every field generator prop.', 'kill @e[type=item_display,tag=rlk_mb_fg_prop]']);

// ---- manifest -------------------------------------------------------------------------------------------------------
const manifestPath = path.join(here, 'mboss_fieldgen_rig_manifest.json');
const lastTextures = (() => { try { return JSON.parse(fs.readFileSync(manifestPath, 'utf8')).textures; } catch { return undefined; } })();
json(manifestPath, {
  parts: [...PARTS.map(([n, m, b]) => ({name: n, uuid: uuidOf(n), tag: 'rlk_mb_fg_' + n, model: m, brightness: b, scale: PART_SCALE[n], elements: elementCount[m]})),
    ...Object.entries(ALIAS).map(([a, of]) => ({name: a, tag: 'rlk_mb_fg_' + a, alias_of: of}))],
  clips: clipInfo,
  rig_forms: Object.keys(FORM_ID),
  forms: Object.fromEntries(CLIPS.filter(c => c.forms).map(c => [c.name, c.forms])),
  hidden: Object.fromEntries(CLIPS.filter(c => c.hidden).map(c => [c.name, c.hidden])),
  form_states: Object.fromEntries(Object.entries(FORM_ID).map(([f, id]) => [f, {id, function: `${NS}/form/${f}`, hold: FORM_HOLD[f], ring_centre: FORMS[f].pos[1], rest_anchors: anchors(solve(restPose(f)))}])),
  looks: Object.keys(LOOKS), look_ids: LOOK_ID, look_models: LOOKS,
  crack: {objective: 'fgRigCrack', stages: {0: 'hits 0-4', 1: 'hits 5-9', 2: 'hits 10-14', 3: 'hits 15-19', 4: 'burst (with play/break)'}, part: 'core_shell'},
  clip_models: Object.fromEntries(Object.entries(MODEL_OF).filter(([k2]) => k2 !== 'beamLook2').map(([k2, [part, map]]) => [k2, {part, models: map}])),
  props: Object.fromEntries(Object.entries(PROP_DEF).map(([k2, l]) => [k2, {function: `${NS}/prop/${k2}`, tag: 'rlk_mb_fg_prop_' + k2, displays: l.map(([m, s]) => ({model: itemId(m), scale: s})), note: PROP_NOTE[k2]}])),
  objectives: {fgRigC: 'current clip id (anchor)', fgRigT: 'tick within the clip (anchor; -1 = queued by play)', fgRigF: 'hit flash countdown', fgRigY: 'face/track scratch',
    fgRigForm: 'stored form: 1 dormant, 2 cruise, 3 field, 4 core-up, 5 tower, 6 laser, 7 deployed', fgRigLook: 'stored look: 0 idle, 1 charge, 2 field, 3 groggy, 4 off',
    fgRigCrack: 'bubble crack stage 0-4', fgRigTmp: '1 while a clip shows a temporary look'},
  textures: sprites ? sprites.length : (typeof lastTextures === 'number' ? lastTextures : 'not repainted'),
  atlas_px: atlasPx,
});
for (const w of [...warns].slice(0, 40)) console.warn('warn:', w);
const files = clipInfo.reduce((a, c) => a + c.keyFiles, 0);
console.log(`Built the field generator rig: ${PARTS.length} parts, ${CLIPS.length} clips, ${files} key files, ${clipInfo.reduce((a, c) => a + c.keys, 0)} part keys, ${Object.keys(models).length} models (${Object.values(elementCount).reduce((a, b) => a + b, 0)} elements), ${Object.keys(spriteTable).length} sprites (${(atlasPx / 1e6).toFixed(2)} M px)${warns.size ? `, ${warns.size} warnings` : ''}.`);
if (debugDp) {
  const link = path.join(debugDp, 'data/rlk/function/mboss/fieldgen/rig');
  fs.rmSync(link, {recursive: true, force: true});
  fs.mkdirSync(path.dirname(link), {recursive: true});
  fs.symlinkSync(rigDir, link);
  // rest poses for renders: fg_dbg/rest_<form>
  for (const f of Object.keys(FORMS)) putDebug(`fg_dbg/rest_${f}`, setPose(f));
}
