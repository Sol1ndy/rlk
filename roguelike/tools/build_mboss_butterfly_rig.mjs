// Articulated display-entity rig of the Moonlit Butterfly (달빛 환영 나비, title 달빛의 화신), the second mid-boss.
// node tools/build_mboss_butterfly_rig.mjs --resourcepack <unpacked pack> [--datapack <pack>] [--no-paint | --paint a,b]
//                                          [--debug-dp <scratch dir>] [--allow-steps]
//
// Writes
//   RP  assets/rlk/textures/mboss/butterfly/*.png (butterfly_paint.mjs) + item atlas entries
//       assets/rlk/models/item/mboss/butterfly/*.json, assets/rlk/items/mboss/butterfly/*.json
//       (also the props: entrance cocoon, wrapped pod, orb and gyroscope ring, not rig parts)
//   DP  data/rlk/function/mboss/butterfly/rig/** (owned by this generator, rebuilt from scratch on every run)
//   tools/mboss_butterfly_rig_manifest.json (parts, clips, events, anchors, looks, props, API)
//
// Runtime model (the contract for the pattern code is tools/mboss_butterfly_rig_api.md):
//   * One superset rig for both forms: 30 item_display parts with FIXED UUIDs 524c4b4d-4246-4c00-8000-0000000000NN.
//     The wings, the holographic overlays and the ribbon tendrils sit at scale 0 in human form. All parts carry
//     rlk_room, rlk_mb_aux, rlk_mb_part, rlk_mb_butterfly_part, rlk_mb_bf_<part>.
//   * The anchor (the boss body) runs rig/tick each tick: the parts follow its position and yaw (tp,
//     teleport_duration 1) and the current clip applies its keys (the shared compiler mboss_rig_compile.mjs:
//     interpolation segments, rotation checks, binary dispatch).
//   * Rig state on the anchor: bfRigForm (1 human, 2 butterfly; the transform/release/revert/death clips switch it
//     at the tick the wings appear or vanish), bfRigLook (0 dendro, 1 pyro, 2 flat), bfRigFlat (a clip's temporary
//     flat-lime look), bfRigTell (crescent tell glow).
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {paintButterflyTextures, spriteId, butterflySprites} from './butterfly_paint.mjs';
import {partModels, checkBounds, LOOKS, wingPoint} from './butterfly_geometry.mjs';
import {solve, toDisplay, PART_SCALE, toeHeight} from './butterfly_pose.mjs';
import {CLIPS, accumulate, sampleClip as sample, restPose} from './butterfly_clips.mjs';
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
const NS = 'rlk:mboss/butterfly/rig';
const rigDir = path.join(dp, 'data/rlk/function/mboss/butterfly/rig');
fs.rmSync(rigDir, {recursive: true, force: true});
const fn = (n, lines) => put(path.join(rigDir, n + '.mcfunction'), (Array.isArray(lines) ? lines : [lines]).join('\n'));
const assets = path.join(rp, 'assets/rlk');

// ---- parts --------------------------------------------------------------------------------------------------------
// [part, default item model, block brightness]; wing-side parts take the look suffix (_dendro by default).
const PARTS = [
  ['pelvis', 'pelvis', 13], ['torso', 'torso', 13], ['collar', 'collar', 14], ['head', 'head', 13], ['head_glow', 'head_glow', 15], ['crest', 'crest', 14],
  ['fan_r', 'fan_r', 13], ['fan_l', 'fan_l', 13],
  ['thigh_r', 'thigh_r', 13], ['shin_r', 'shin_r', 14], ['foot_r', 'foot_r', 14], ['thigh_l', 'thigh_l', 13], ['shin_l', 'shin_l', 14], ['foot_l', 'foot_l', 14],
  ['hand_r_a', 'crescent_r', 13], ['hand_r_b', 'shard_r', 13], ['hand_l_a', 'crescent_l', 13], ['hand_l_b', 'shard_l', 13], ['flakes', 'flakes', 12],
  ['fwing_l', 'fwing_l_dendro', 14], ['fwing_r', 'fwing_r_dendro', 14], ['fwglow_l', 'fwglow_l_dendro', 15], ['fwglow_r', 'fwglow_r_dendro', 15],
  ['hwing_l', 'hwing_l_dendro', 14], ['hwing_r', 'hwing_r_dendro', 14],
  ['tendril_ul', 'tendril_ul_dendro', 14], ['tendril_ur', 'tendril_ur_dendro', 14], ['tendril_ll', 'tendril_ll_dendro', 14], ['tendril_lr', 'tendril_lr_dendro', 14],
  ['core', 'core', 15],
];
if (PARTS.length > 34) throw new Error(`${PARTS.length} parts: the budget is 34`);
const PART_INDEX = Object.fromEntries(PARTS.map(([n], i) => [n, i + 1]));
const uuidOf = n => `524c4b4d-4246-4c00-8000-${PART_INDEX[n].toString(16).padStart(12, '0')}`;
const uuidInts = n => `[I;1380731725,1111903232,-2147483648,${PART_INDEX[n]}]`;
const itemId = m => `rlk:mboss/butterfly/${m}`;
const LOOK_PARTS = ['fwing_l', 'fwing_r', 'fwglow_l', 'fwglow_r', 'hwing_l', 'hwing_r', 'tendril_ul', 'tendril_ur', 'tendril_ll', 'tendril_lr'];
const LOOK_ID = {dendro: 0, pyro: 1, flat: 2};

// ---- resource pack: textures, models, item definitions --------------------------------------------------------------
const sprites = flag('--no-paint') ? null : paintButterflyTextures(rp, arg('--paint') ? arg('--paint').split(',') : null);
const models = partModels();
for (const [name, els] of Object.entries(models)) checkBounds(name, els);
const modelDir = path.join(assets, 'models/item/mboss/butterfly'), itemDir = path.join(assets, 'items/mboss/butterfly');
fs.rmSync(modelDir, {recursive: true, force: true});
fs.rmSync(itemDir, {recursive: true, force: true});
for (const [name, els] of Object.entries(models)) {
  const used = [...new Set(els.flatMap(e => Object.values(e.faces).map(f => f.texture.slice(1))))];
  json(path.join(modelDir, name + '.json'), {ambientocclusion: false, textures: {...Object.fromEntries(used.map(t => [t, spriteId(t)])), particle: spriteId(used[0])}, elements: els});
  json(path.join(itemDir, name + '.json'), {model: {type: 'minecraft:model', model: 'rlk:item/mboss/butterfly/' + name}});
}
// atlas budget (2 M px, sides <= 512, multiples of 16)
const spriteTable = butterflySprites();
let atlasPx = 0;
for (const [n, [w, h]] of Object.entries(spriteTable)) {
  if (w > 512 || h > 1024 || w % 16 || h % 16) throw new Error(`sprite ${n} ${w}x${h}: sides <= 512 (animated strips: frames <= 512), multiples of 16`);
  atlasPx += w * h;
}
if (atlasPx > 2e6) throw new Error(`butterfly sprites use ${atlasPx} px of the atlas (budget 2 M)`);

// ---- clip sampling ------------------------------------------------------------------------------------------------
function frame(clip, t, ks) {
  const p = sample(clip, t, ks);
  const o = solve(p);
  const d = {};
  for (const [n] of PARTS) d[n] = toDisplay(n, o[n]);
  return {d, p, o};
}
const clipFrames = (clip, ks = accumulate(clip)) => Array.from({length: clip.len + 1}, (_, t) => frame(clip, t, ks));
// Fx anchor points: hoof tips, wing hook tips, hindwing blade tips, the chest core, the head, the two big crescents.
// Rig coordinates in blocks from the anchor: x her left, y up, -z her front (body frame: ^x ^y ^-z).
const FW_HOOK = wingPoint('fw', [21.9, 23.6]), HW_TIP = wingPoint('hw', [22.4, -4.4]);
function anchors(o) {
  // a model point p (units, her left side's model) of part n in rig blocks; the right side's models are mirrored
  const at = (n, p) => { const k = PART_SCALE[n] * o[n].s[0] / 16, m = n.endsWith('_r') ? -1 : 1; return add(o[n].t, rot(o[n].q, [p[0] * k * m, p[1] * k, p[2] * k])); };
  const r3 = v => v.map(x => +x.toFixed(3) || 0);
  return {foot_l: r3(o._legs.l.hoof), foot_r: r3(o._legs.r.hoof), fwtip_l: r3(at('fwing_l', FW_HOOK)), fwtip_r: r3(at('fwing_r', FW_HOOK)),
    hwtip_l: r3(at('hwing_l', HW_TIP)), hwtip_r: r3(at('hwing_r', HW_TIP)), core: r3(o.core.t), head: r3(o.head.t), hand_r_a: r3(o.hand_r_a.t), hand_l_a: r3(o.hand_l_a.t)};
}

// ---- compile clips --------------------------------------------------------------------------------------------------
// --debug-dp <dir>: also writes the exact per-tick poses (bf_dbg/<clip>/<t>) and a copy of the rig functions into a
// scratch datapack root, for the offline renderer. Never the real pack.
const debugDp = arg('--debug-dp') && path.resolve(arg('--debug-dp'));
if (debugDp) fs.rmSync(path.join(debugDp, 'data/rlk/function/bf_dbg'), {recursive: true, force: true});
const putDebug = (n, lines) => put(path.join(debugDp, 'data/rlk/function', n + '.mcfunction'), lines.join('\n'));
const TOL = {t: .012, s: .015, rDefault: 1.4, r: {fwing_l: .5, fwing_r: .5, fwglow_l: .5, fwglow_r: .5, hwing_l: .6, hwing_r: .6, tendril_ll: .9, tendril_lr: .9, core: 3, flakes: 2}};
const compiler = createRigCompiler({ns: NS, obj: 'bfRig', fn, parts: PARTS.map(([n]) => n), uuidOf, tol: TOL,
  debug: debugDp ? {put: putDebug, dir: 'bf_dbg'} : null});
const FORM_ID = {h: 1, b: 2};
const clipInfo = [], motionErrors = [], warns = new Set();
CLIPS.forEach((c, id) => { c.id = id; });
const byName = Object.fromEntries(CLIPS.map(c => [c.name, c]));
for (const c of CLIPS) {
  if (c.keys[0][0] !== 0) throw new Error(`clip ${c.name}: first key must be tick 0`);
  if (c.keys[c.keys.length - 1][0] !== c.len) throw new Error(`clip ${c.name}: last key ${c.keys[c.keys.length - 1][0]} != len ${c.len}`);
  if (c.next && !byName[c.next]) throw new Error(`clip ${c.name}: unknown next ${c.next}`);
  const ks = accumulate(c);
  const frames = clipFrames(c, ks);
  // state lines: the form at tick 0 and where it changes; the temporary flat look on/off (wlook)
  const extra = t => {
    const out = [], p = frames[t].p, q = t ? frames[t - 1].p : null;
    if (!q || p.form !== q.form) out.push(`scoreboard players set @s bfRigForm ${FORM_ID[p.form]}`);
    if (!q) out.push(p.wlook === 'flat' ? `function ${NS}/look/temp_flat` : `execute if score @s bfRigFlat matches 1 run function ${NS}/look_apply`);
    else if (p.wlook !== q.wlook) out.push(p.wlook === 'flat' ? `function ${NS}/look/temp_flat` : `function ${NS}/look_apply`);
    return out;
  };
  const r = compiler.compileClip(c, frames, a => frame(c, a + .5, ks), extra);
  motionErrors.push(...r.motionErrors);
  r.warns.forEach(w => warns.add(w));
  const ev = Object.fromEntries(Object.entries(c.events || {}).map(([n, t]) => [n, anchors(frames[Math.min(t, c.len)].o)]));
  const sw = frames.findIndex((f, t) => t > 0 && f.p.form !== frames[t - 1].p.form);
  const form = {start: frames[0].p.form, end: frames[c.len].p.form};
  if (sw > 0) form.switch = [sw, frames[sw].p.form === 'b' ? 'butterfly' : 'human'];
  clipInfo.push({...r.info, form, anchors: ev});
}
if (motionErrors.length) {
  const msg = `part rotations above 120 degrees per tick or per key:\n  ` + motionErrors.slice(0, 120).join('\n  ') + (motionErrors.length > 120 ? `\n  ... ${motionErrors.length} in all` : '');
  if (flag('--allow-steps')) console.warn(msg); else throw new Error(msg);
}
compiler.writeDispatch(CLIPS);

// ---- API functions --------------------------------------------------------------------------------------------------
const restOf = which => { const o = solve(restPose(which)); return Object.fromEntries(PARTS.map(([n]) => [n, toDisplay(n, o[n])])); };
const REST = {h: restOf('h'), b: restOf('b')};
// alias tags: the fx anchors the module contract names (stub rig parts body, hand_r, hand_l) on the real parts
const ALIAS = {torso: 'body', hand_r_a: 'hand_r', hand_l_a: 'hand_l'};
const TAGS = n => `["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_butterfly_part","rlk_mb_bf_${n}"${ALIAS[n] ? `,"rlk_mb_bf_${ALIAS[n]}"` : ''}]`;
const summon = ([n, model, bright], pose) => `summon minecraft:item_display ~ ~ ~ {UUID:${uuidInts(n)},Tags:${TAGS(n)},billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:2.5f,width:16f,height:16f,shadow_radius:0f,brightness:{block:${bright},sky:15},transformation:${nbt(pose)},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${itemId(model)}"}}}`;
const swapLine = (part, model) => `data modify entity ${uuidOf(part)} item.components."minecraft:item_model" set value "${itemId(model)}"`;
const RIG_OBJ = ['bfRigC', 'bfRigT', 'bfRigF', 'bfRigY', 'bfRigForm', 'bfRigLook', 'bfRigFlat', 'bfRigTell'];
fn('init', ['# Rig objectives. Safe to call on every load.', ...RIG_OBJ.map(o => `scoreboard objectives add ${o} dummy`)]);
const setPose = (which, dur = 0) => PARTS.map(([n]) => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:${dur},transformation:${nbt(REST[which][n])}}`);
const spawnTail = ['scoreboard players set @s bfRigT -1', 'scoreboard players set @s bfRigF 0', 'scoreboard players set @s bfRigFlat 0',
  'execute unless score @s bfRigLook matches 0.. run scoreboard players set @s bfRigLook 0',
  'execute unless score @s bfRigTell matches 0.. run scoreboard players set @s bfRigTell 0',
  'execute unless score @s bfRigForm matches 1..2 run scoreboard players set @s bfRigForm 1',
  `function ${NS}/look_apply`,
  `execute if score @s bfRigForm matches 2 run function ${NS}/form/butterfly`,
  `execute unless score @s bfRigForm matches 2 run function ${NS}/form/human`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow`];
fn('spawn', ['# @s = rig anchor (the boss body), positioned and rotated where she should appear.',
  `# Summons the ${PARTS.length} parts with fixed UUIDs in the rest pose of the stored form (bfRigForm, human by default) and`,
  '# queues its idle clip; re-applies the stored looks.',
  `function ${NS}/init`, `function ${NS}/kill`, ...PARTS.map(p => summon(p, REST.h[p[0]])), ...spawnTail]);
fn('spawn_hidden', ['# Like spawn, but every part starts at scale 0 (nothing shows) and the form is human. Play the opening clip in the same',
  '# tick (play/entrance): its keys bring the parts in. @s = rig anchor.',
  `function ${NS}/init`, `function ${NS}/kill`, 'scoreboard players set @s bfRigForm 1',
  ...PARTS.map(p => summon(p, {...REST.h[p[0]], s: [0, 0, 0]})),
  'scoreboard players set @s bfRigT -1', 'scoreboard players set @s bfRigF 0', 'scoreboard players set @s bfRigFlat 0',
  'execute unless score @s bfRigLook matches 0.. run scoreboard players set @s bfRigLook 0', 'scoreboard players set @s bfRigTell 0',
  `function ${NS}/look_apply`, `scoreboard players set @s bfRigC ${byName.entrance.id}`, `execute rotated as @s rotated ~ 0 run function ${NS}/follow`]);
fn('follow', ['# Parts follow the executor position and yaw (run rotated as the anchor, pitch 0).', ...PARTS.map(([n]) => `tp ${uuidOf(n)} ~ ~ ~ ~ ~`)]);
fn('tick', ['# @s = rig anchor, at its feet. Once per game tick. Missing parts respawn in the rest pose of the stored form',
  '# (the clip restarts as that form\'s idle).',
  `execute unless entity ${uuidOf('torso')} run function ${NS}/spawn`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow`,
  'scoreboard players add @s bfRigT 1',
  `function ${NS}/run`,
  `execute if score @s bfRigF matches 1.. run function ${NS}/flash_tick`]);
fn('kill', ['# Removes every rig part (the props have their own tag).', 'kill @e[type=item_display,tag=rlk_mb_butterfly_part]']);
fn('uninstall', ['# Removes the rig, its props and its objectives.', `function ${NS}/kill`, `function ${NS}/prop/clear`, 'kill @e[type=marker,tag=rlk_mb_bf_face]',
  ...RIG_OBJ.map(o => `scoreboard objectives remove ${o}`)]);
// forms: instant show/hide (the transform, release, revert and death clips animate the change themselves)
fn('form/human', ['# Instant human form: wings, overlays and tendrils hidden, the human rest pose, idle_h queued. @s = rig anchor.',
  'scoreboard players set @s bfRigForm 1', ...setPose('h'), `scoreboard players set @s bfRigC ${byName.idle_h.id}`, 'scoreboard players set @s bfRigT -1']);
fn('form/butterfly', ['# Instant butterfly form: wings spread, hovering (toes 1.2 b up), idle_b queued. @s = rig anchor.',
  'scoreboard players set @s bfRigForm 2', ...setPose('b'), `scoreboard players set @s bfRigC ${byName.idle_b.id}`, 'scoreboard players set @s bfRigT -1']);
// looks: wing element looks swap the item models of the wing-side parts
const lookSwaps = look => LOOK_PARTS.map(n => swapLine(n, `${n}_${look}`));
for (const look of ['dendro', 'pyro', 'flat']) {
  fn(`look/${look}`, [`# Wing look: ${look} (${{dendro: 'lime frames, white-mint/lime membranes, opal shimmer', pyro: 'orange-gold to magenta membranes, blades and ribbons', flat: 'flat lime, for the transform and the dissolve'}[look]}). @s = rig anchor.`,
    `scoreboard players set @s bfRigLook ${LOOK_ID[look]}`, 'scoreboard players set @s bfRigFlat 0', ...lookSwaps(look)]);
}
fn('look/temp_flat', ['# Internal (clips): flat lime wings without changing the stored look; look_apply restores it. @s = rig anchor.',
  'scoreboard players set @s bfRigFlat 1', ...lookSwaps('flat')]);
fn('look_apply', ['# Re-applies the stored wing look bfRigLook and the crescent tell (after a respawn or a temporary flat look). @s = rig anchor.',
  'scoreboard players set @s bfRigFlat 0',
  ...Object.entries(LOOK_ID).map(([look, id]) => `execute if score @s bfRigLook matches ${id} run function ${NS}/look/${look}_swap`),
  `execute if score @s bfRigTell matches 1 run function ${NS}/tell/on`]);
for (const look of ['dendro', 'pyro', 'flat']) fn(`look/${look}_swap`, [`# Internal: the ${look} models on the wing-side parts.`, ...lookSwaps(look)]);
// crescent tell (달빛 점프: the crescent chain glows lime)
fn('tell/on', ['# The crescent pieces glow lime (tell). @s = rig anchor.', 'scoreboard players set @s bfRigTell 1',
  swapLine('hand_r_a', 'crescent_tell_r'), swapLine('hand_l_a', 'crescent_tell_l')]);
fn('tell/off', ['# The crescent pieces back to navy. @s = rig anchor.', 'scoreboard players set @s bfRigTell 0',
  swapLine('hand_r_a', 'crescent_r'), swapLine('hand_l_a', 'crescent_l')]);
// hit flash
const OUTLINED = PARTS.filter(([n]) => !['head_glow', 'fwglow_l', 'fwglow_r', 'core'].includes(n));
fn('flash', ['# Hit feedback: a pale lime outline for 3 ticks. @s = rig anchor.', 'scoreboard players set @s bfRigF 4',
  ...OUTLINED.map(([n]) => `data merge entity ${uuidOf(n)} {Glowing:1b,glow_color_override:15925200}`)]);
fn('flash_tick', ['scoreboard players remove @s bfRigF 1', `execute if score @s bfRigF matches 0 run function ${NS}/flash_off`]);
fn('flash_off', ['# End of the hit flash. @s = rig anchor.', ...OUTLINED.map(([n]) => `data merge entity ${uuidOf(n)} {Glowing:0b}`)]);
// facing helpers (shared compiler)
compiler.writeFace({marker: 'rlk_mb_bf_face'});
// props: free item_displays, not rig parts (the rig tp never moves them); tags rlk_mb_bf_prop + rlk_mb_bf_prop_<kind>,
// and rlk_mb_bf_prop_new for the call's own summons (removed from older props first)
const PROP_DEF = {
  cocoon: [['cocoon', 3, 'fixed', 14], ['cocoon_halo', 3, 'center', 15]],
  pod: [['pod', 2.5, 'fixed', 15]],
  orb: [['orb', 1, 'fixed', 15], ['ring', 1, 'fixed', 15, [.5, 0, 0, .866]], ['ring', 1, 'fixed', 15, [-.259, 0, .259, .933]]],
};
const PROP_NOTE = {
  cocoon: 'the entrance cocoon (3.8 b tall, wrapped wing plates, a glowing lime window, a lime spike) and its glow halo (billboard centre); the module hides it at the burst',
  pod: 'the wrapped wing pod (코코볼 ball, 달빛 해제 wrap; 3.4 b tall, r 1.4 b) centred on the execution point',
  orb: 'the 달빛 축복 orb: a 1.7 b lime glass sphere and two gyroscope rings (spin them with transformation keys)',
};
for (const [kind, list] of Object.entries(PROP_DEF)) {
  fn(`prop/${kind}`, [`# Summons ${PROP_NOTE[kind]}, at the execution position and yaw.`,
    '# Tags rlk_room, rlk_mb_aux, rlk_mb_bf_prop, rlk_mb_bf_prop_' + kind + ' and, for this call only, rlk_mb_bf_prop_new. Scale = the model scale.',
    'tag @e[tag=rlk_mb_bf_prop_new] remove rlk_mb_bf_prop_new',
    ...list.map(([m, s, bb, br, q]) => `summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_prop","rlk_mb_bf_prop_${kind}","rlk_mb_bf_prop_new"],billboard:"${bb}",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:3f,width:16f,height:16f,shadow_radius:0f,brightness:{block:${br},sky:15},transformation:{translation:[0f,0f,0f],left_rotation:${q ? '[' + q.map(x => x + 'f').join(',') + ']' : '[0f,0f,0f,1f]'},scale:[${s}f,${s}f,${s}f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${itemId(m)}"}}}`),
    'execute rotated ~ 0 run tp @e[type=item_display,tag=rlk_mb_bf_prop_new] ~ ~ ~ ~ 0']);
}
fn('prop/clear', ['# Removes every butterfly prop.', 'kill @e[type=item_display,tag=rlk_mb_bf_prop]']);

// ---- manifest -------------------------------------------------------------------------------------------------------
const manifestPath = path.join(here, 'mboss_butterfly_rig_manifest.json');
const lastTextures = (() => { try { return JSON.parse(fs.readFileSync(manifestPath, 'utf8')).textures; } catch { return undefined; } })();
const restH = solve(restPose('h')), restB = solve(restPose('b'));
json(manifestPath, {
  parts: [...PARTS.map(([n, m, b]) => ({name: n, uuid: uuidOf(n), tag: 'rlk_mb_bf_' + n, model: m, brightness: b, scale: PART_SCALE[n], look: LOOK_PARTS.includes(n)})),
    ...Object.entries(ALIAS).map(([n, a]) => ({name: a, tag: 'rlk_mb_bf_' + a, alias_of: n}))],
  clips: clipInfo,
  // {clip: [tick, form]}: the clip tick at which a clip switches the form itself (the module contract's shape)
  forms: Object.fromEntries(clipInfo.filter(c => c.form.switch).map(c => [c.name, c.form.switch])),
  form_states: {human: {id: 1, idle: 'idle_h', rest_anchors: anchors(restH), toe_height: +toeHeight(restH).toFixed(3)},
    butterfly: {id: 2, idle: 'idle_b', rest_anchors: anchors(restB), toe_height: +toeHeight(restB).toFixed(3)}},
  looks: ['dendro', 'pyro', 'flat'],
  look_ids: {dendro: 0, pyro: 1, flat: 2},
  look_parts: LOOK_PARTS,
  props: Object.fromEntries(Object.entries(PROP_DEF).map(([k, l]) => [k, {function: `${NS}/prop/${k}`, tag: 'rlk_mb_bf_prop_' + k, displays: l.map(([m, s, bb]) => ({model: itemId(m), scale: s, billboard: bb})), note: PROP_NOTE[k]}])),
  objectives: {bfRigC: 'current clip id (anchor)', bfRigT: 'tick within the clip (anchor; -1 = queued by play)', bfRigF: 'hit flash countdown', bfRigY: 'face/track scratch',
    bfRigForm: 'form: 1 human, 2 butterfly', bfRigLook: 'wing look: 0 dendro, 1 pyro, 2 flat', bfRigFlat: '1 while a clip shows the temporary flat look', bfRigTell: '1 while the crescents glow (tell)'},
  textures: sprites ? sprites.length : (typeof lastTextures === 'number' ? lastTextures : 'not repainted'),
  atlas_px: atlasPx,
});
for (const w of [...warns].slice(0, 40)) console.warn('warn:', w);
const files = clipInfo.reduce((a, c) => a + c.keyFiles, 0);
console.log(`Built the Moonlit Butterfly rig: ${PARTS.length} parts, ${CLIPS.length} clips, ${files} key files, ${clipInfo.reduce((a, c) => a + c.keys, 0)} part keys, ${Object.keys(models).length} models, ${Object.keys(spriteTable).length} sprites (${(atlasPx / 1e6).toFixed(2)} M px)${warns.size ? `, ${warns.size} warnings` : ''}.`);
console.log(`rest toe heights: human ${toeHeight(restH).toFixed(2)} b, butterfly ${toeHeight(restB).toFixed(2)} b`);
if (debugDp) {
  fs.cpSync(rigDir, path.join(debugDp, 'data/rlk/function/mboss/butterfly/rig'), {recursive: true});
  // rest poses for renders: bf_dbg/rest_h, bf_dbg/rest_b
  for (const w of ['h', 'b']) putDebug(`bf_dbg/rest_${w}`, setPose(w));
}
