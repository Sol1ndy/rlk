// Apep phase-2 objects (plan §5, stage AP-ORG): the six organisms, the Heart of the Oasis, the 소생의 찬가 domes, the
// 둥지 wall blades, the 생명의 손 stalks and the death seed — models, sprites, clips, key functions and the org manifest.
// node tools/build_mboss_apep_org.mjs --resourcepack <unpacked pack> [--datapack <pack>] [--no-paint]
//                                     [--debug-dp <scratch dir>]
//
// Writes (and owns: rebuilt from scratch on every run)
//   RP  assets/rlk/textures/mboss/apep_om/*.png (apep_org_paint.mjs) + item atlas entries rlk:mboss/apep_om/*
//       assets/rlk/models/item/mboss/apep_om/*.json, assets/rlk/items/mboss/apep_om/*.json
//   DP  data/rlk/function/mboss/apep/om/** (the runtime below; API: tools/mboss_apep_org_api.md)
//   tools/mboss_apep_org_manifest.json (org manifest v1, S:ap/spec/org_manifest.schema.json, ap_contract.md §0.5)
//
// Runtime
//   * Organisms: item_display passengers of the framework aux husk (riding ≈ 2 b up, translated down to the feet,
//     culling off). The husk holds the clip clock (apOI clip id, apOC tick). om/<kind>/tick (as the husk, once per
//     tick) applies tick apOC of clip apOI and then advances apOC; key functions run
//     `execute on passengers if entity @s[tag=rlk_ap_om_<display>] run data merge entity @s {...}`.
//   * Objects (the Heart, domes, stalks: fixed UUIDs; wall blades: multi): every display holds its own clock; the
//     object's tick runs each display's clip as that display (`data merge entity @s`), so independent clips (the
//     cradle rising while the egg is lowered) never collide. A display whose clip ends stops (apOI -1), or chains
//     itself into `next` when it is one of next's displays.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {ORG, KINDS, OBJECTS, RIDE_Y, allModels, allItems, checkBounds, restJoint} from './apep_org_geometry.mjs';
import {paintOrgTextures, spriteId, spriteSizes, spriteOwner} from './apep_org_paint.mjs';
import {CLIPS, SPAWN, HANG, clipKeys, poseAt, solve, displayXf, withTwins} from './apep_org_clips.mjs';
import {createRigCompiler, nbt, written, shown} from './mboss_rig_compile.mjs';
import {qAngle} from './mboss_rig_math.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const arg = n => { const i = process.argv.indexOf(n); return i < 0 ? null : process.argv[i + 1]; };
const flag = n => process.argv.includes(n);
const dp = path.resolve(arg('--datapack') || path.join(here, '..'));
const rp = arg('--resourcepack') && path.resolve(arg('--resourcepack'));
if (!rp) throw new Error('--resourcepack <unpacked pack> is required');
const put = (p, s) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, s.endsWith('\n') ? s : s + '\n'); };
const json = (p, o) => put(p, JSON.stringify(o, null, 2));
const NS = 'rlk:mboss/apep/om';
const fnDir = path.join(dp, 'data/rlk/function/mboss/apep/om');
fs.rmSync(fnDir, {recursive: true, force: true});
const FILES = new Map();
const fn = (n, lines) => { if (FILES.has(n)) throw new Error('function written twice: ' + n); const L = Array.isArray(lines) ? lines : [lines]; FILES.set(n, L.length); put(path.join(fnDir, n + '.mcfunction'), L.join('\n')); };
const itemId = m => 'rlk:mboss/apep_om/' + m;
const UUID_BLOCK = '524c4b4d-4150-4800-8000-0000000000', UUID_INTS = [1380731725, 1095780352, -2147483648];
const uuidOf = idx => UUID_BLOCK + idx.toString(16).padStart(2, '0');
const uuidNbt = idx => `[I;${UUID_INTS.join(',')},${idx}]`;
const BASE_TAGS = ['rlk_room', 'rlk_mb_aux'];
const SCALE_IN = {ticks: 4, from: .85};
const SPAWN_CLIP = {basic: 'org_spawn', nurt: 'nurt_idle', guard: 'guard_idle', nest: 'nest_fly', destr: 'destr_roll', pred: 'pred_swim'};
const fnum = v => String(+(+v).toFixed(4)).replace(/^(-?)0\./, '$1.');
const errors = [], warns = [];

// ---- resource pack ----------------------------------------------------------------------------------------------------
const SPR = spriteSizes(), SOWN = spriteOwner();
if (!flag('--no-paint')) paintOrgTextures(rp);
const models = allModels(), items = allItems();
const modelDir = path.join(rp, 'assets/rlk/models/item/mboss/apep_om'), itemDir = path.join(rp, 'assets/rlk/items/mboss/apep_om');
fs.rmSync(modelDir, {recursive: true, force: true});
fs.rmSync(itemDir, {recursive: true, force: true});
const usedSprites = new Set();
for (const [name, {els}] of Object.entries(models)) {
  checkBounds(name, els);
  const used = [...new Set(els.flatMap(e => Object.values(e.faces).map(f => f.texture.slice(1))))];
  for (const u of used) { if (!SPR[u]) throw new Error(`model ${name}: unknown sprite ${u}`); usedSprites.add(u); }
  json(path.join(modelDir, name + '.json'), {ambientocclusion: false, textures: {...Object.fromEntries(used.map(t => [t, spriteId(t)])), particle: spriteId(used[0] || 'bo_bell')}, elements: els});
}
for (const [item, {model, tint}] of Object.entries(items)) {
  if (!models[model]) throw new Error(`item ${item}: no model ${model}`);
  json(path.join(itemDir, item + '.json'), {model: {type: 'minecraft:model', model: 'rlk:item/mboss/apep_om/' + model, ...(tint === null ? {} : {tints: [{type: 'minecraft:constant', value: tint}]})}});
}
for (const s of Object.keys(SPR)) if (!usedSprites.has(s)) warns.push(`sprite ${s} is painted but unused`);
for (const [n, [w, h]] of Object.entries(SPR)) if (w > 512 || h > 512 || w % 16 || h % 16) errors.push(`sprite ${n} ${w}x${h}: sides <= 512, multiples of 16`);
// untinted faces on tinted models (every face of a tint-look model must carry tintindex 0)
for (const [item, {model, tint}] of Object.entries(items)) if (tint !== null) {
  const n = models[model].els.reduce((a, e) => a + Object.values(e.faces).filter(f => f.tintindex !== 0).length, 0);
  if (n) errors.push(`model ${model} (tinted look ${item}): ${n} faces without tintindex 0`);
}

// ---- budgets ------------------------------------------------------------------------------------------------------------
const pxOf = owner => Object.entries(SPR).filter(([n]) => SOWN[n] === owner).reduce((a, [, [w, h]]) => a + w * h, 0);
const elementsOf = owner => ORG[owner].displays.reduce((a, d) => a + Math.max(0, ...Object.values(d.looks).map(it => models[items[it].model].els.length)), 0);
const BUDGET = {basic: [500, 14000], nurt: [500, 16000], guard: [500, 16000], nest: [500, 12000], destr: [500, 8000], pred: [500, 20000],
  heart: [800, 40000], dome: [500, 24000], wall: [60, 8000], stalk: [400, 16000], seed: [40, 2000]};
let pxTotal = 0;
for (const o of Object.keys(ORG)) {
  const el = elementsOf(o), px = pxOf(o); pxTotal += px;
  if (el > BUDGET[o][0]) errors.push(`${o}: ${el} elements over ${BUDGET[o][0]}`);
  if (px > BUDGET[o][1]) errors.push(`${o}: ${px} px over ${BUDGET[o][1]}`);
}
if (pxTotal > 200000) errors.push(`org sprites ${pxTotal} px over 0.2 M`);

// ---- clip compilation -------------------------------------------------------------------------------------------------
const TOL = {t: .012, s: .015, rDefault: 1.0, r: {}};
// per-tick display transforms of a clip: frames[t] = {name: {t, q, s, look}}
function clipFrames(owner, c) {
  const ks = clipKeys(owner, c);
  return Array.from({length: c.len + 1}, (_, t) => {
    const P = poseAt(owner, c, t, ks), W = solve(owner, P);
    // a follow display (a turned copy of its parent) needs parent scales that commute with its turn
    for (const d of ORG[owner].displays.filter(x => x.follow)) { const f = d.follow(P[d.name].look), s = W[d.parent].s, i = f[1] ? 2 : f[2] ? 1 : 0;
      if (!models[items[d.looks[P[d.name].look]].model].els.length) continue;
      if (Math.abs(s[0] - s[i]) > 1e-6 && Math.max(...s) > 1e-6) errors.push(`${owner}/${c.name} t${t}: ${d.parent} scale ${s.map(x => x.toFixed(3))} does not commute with ${d.name}'s turn ${f}`); }
    return Object.fromEntries(Object.entries(W).map(([n, w]) => [n, {...displayXf(owner, n, w), look: w.look}]));
  });
}
// segments of one display: a key at tick a sets the pose of tick b (duration b - a); cuts (look changes, explicit) set
// the cut tick's pose instantly and start the next run one tick later; breaks only end a segment
function displaySegments(compiler, name, frames, c, from = 0) {
  const seq = frames.map(f => ({t: f[name].t, q: f[name].q, s: f[name].s}));
  const cuts = new Set(c.cuts || []);
  if (c.cut0) cuts.add(0);
  for (let t = Math.max(1, from); t < frames.length; t++) if (frames[t][name].look !== frames[t - 1][name].look) cuts.add(t);
  const stops = [...new Set([from, ...[...cuts].filter(t => t > from), ...(c.breaks || []).filter(t => t > from && t < c.len), c.len])].sort((a, b) => a - b);
  const out = [];
  for (let i = 0; i < stops.length - 1; i++) {
    let a = stops[i]; const b = stops[i + 1];
    let held = null;
    if (cuts.has(a)) { out.push([a, a]); held = seq[a]; a += 1; if (a > b) continue; if (a === b && i < stops.length - 2) continue; }
    if (a >= b) continue;
    // after a cut the client still shows the cut tick's pose at a: fit the run from that pose
    const run = seq.slice(a, b + 1); if (held) run[0] = held;
    for (const [x, y] of compiler.segments(run, name, 1)) out.push([a + x, a + y]);
  }
  // the last tick of a hold clip is reached by the last segment; a cut there needs its own instant key
  if (cuts.has(c.len) && !out.some(([x, y]) => x === c.len)) out.push([c.len, c.len]);
  return {seq, out: out.sort((p, q2) => p[0] - q2[0])};
}
const xfNbt = (v, dur) => `{start_interpolation:0,interpolation_duration:${dur},transformation:${nbt(v)}}`;
// look switches of one display at tick t (with the variants of plan §5.1: the bag keeps the buff, dying keeps the form)
function lookLines(owner, d, look, sel) {
  const items0 = d.looks, alt = (d.variants || {})[look] || {}, lines = [];
  const has = it => `if data entity @s {item:{components:{"minecraft:item_model":"${itemId(it)}"}}}`;
  const set = it => `data modify entity @s item.components."minecraft:item_model" set value "${itemId(it)}"`;
  for (const [fromLook, toLook] of Object.entries(alt)) lines.push(`${sel}${has(items0[fromLook])} run ${set(items0[toLook])}`);
  const guard = [...new Set(Object.values(alt))].map(l => `unless${has(items0[l]).slice(2)}`).join(' ');
  lines.push(`${sel}${guard ? guard + ' ' : ''}run ${set(items0[look])}`.replace(/run run/, 'run'));
  return lines;
}
const tree = (dir, obj, items2) => {       // binary dispatch over [value, function] pairs on score obj of @s
  if (items2.length <= 6) return items2.map(([v, f]) => `execute if score @s ${obj} matches ${v} run return run function ${f}`);
  const mid = items2[Math.floor(items2.length / 2) - 1][0], L = items2.filter(([v]) => v <= mid), R = items2.filter(([v]) => v > mid);
  const sub = p => `${dir}/${p[0][0]}_${p[p.length - 1][0]}`;
  fn(sub(L), tree(dir, obj, L)); fn(sub(R), tree(dir, obj, R));
  return [`execute if score @s ${obj} matches ..${mid} run return run function ${NS}/${sub(L)}`, `function ${NS}/${sub(R)}`];
};
const keyStats = {};
// compile one clip for a kind (husk clock; passengers by tag)
function compileKindClip(owner, c) {
  const o = ORG[owner], compiler = createRigCompiler({ns: NS, obj: 'apO', fn: () => {}, parts: o.displays.map(d => d.name), uuidOf: () => '', tol: TOL});
  const frames = clipFrames(owner, c), byTick = new Map(), addL = (t, l) => { if (!byTick.has(t)) byTick.set(t, []); byTick.get(t).push(l); };
  let keys = 0;
  for (const d of o.displays) {
    const sel = `execute on passengers if entity @s[tag=rlk_ap_om_${d.name}] `;
    const {seq, out} = displaySegments(compiler, d.name, frames, c);
    for (const [a, b] of out) { addL(a, `${sel}run data merge entity @s ${xfNbt(written(seq[b]), b - a)}`); keys++; }
    frames.forEach((f, t) => { if ((t > 0 && f[d.name].look !== frames[t - 1][d.name].look) || (t === 0 && (c.force || []).includes(d.name))) for (const l of lookLines(owner, d, f[d.name].look, sel)) addL(t, l); });
    stepCheck(owner, c, d.name, seq);
  }
  const ticks = [...byTick.keys()].sort((x, y) => x - y);
  for (const t of ticks) fn(`${owner}/c/${c.name}/k/${t}`, byTick.get(t));
  const head = [`# ${owner} clip ${c.name} (id ${c.id}): ${c.len} t${c.loop ? ', loop' : c.next ? `, then ${c.next}` : ', holds'}. @s = the husk; apOC = the tick to apply now.`];
  if (c.loop) head.push(`execute if score @s apOC matches ${c.len}.. run scoreboard players set @s apOC 0`);
  else if (c.next) head.push(`execute if score @s apOC matches ${c.len}.. run return run function ${NS}/${owner}/c/${c.next}/enter`);
  else head.push(`execute if score @s apOC matches ${c.len + 1}.. run return run scoreboard players set @s apOC ${c.len + 1}`);
  fn(`${owner}/c/${c.name}/run`, [...head, ...tree(`${owner}/c/${c.name}/b`, 'apOC', ticks.map(t => [t, `${NS}/${owner}/c/${c.name}/k/${t}`]))]);
  fn(`${owner}/c/${c.name}/enter`, [`# Chain into ${c.name} now (its tick 0); ${owner}/tick then advances to 1. @s = the husk.`, `scoreboard players set @s apOI ${c.id}`, `scoreboard players set @s apOC 0`, `function ${NS}/${owner}/c/${c.name}/k/0`]);
  fn(`${owner}/play/${c.name}`, [`# Play ${c.name} (${c.len} t) from its tick 0 at the next ${owner}/tick. @s = the husk.`, `scoreboard players set @s apOI ${c.id}`, `scoreboard players set @s apOC 0`]);
  fn(`${owner}/start/${c.name}`, [`# Start ${c.name} now: tick 0 applied immediately, ${owner}/tick continues with tick 1. @s = the husk.`, `function ${NS}/${owner}/c/${c.name}/enter`, `scoreboard players set @s apOC 1`]);
  keyStats[`${owner}/${c.name}`] = {keys, keyFiles: ticks.length, len: c.len};
  return frames;
}
// compile one clip for an object (per-display clocks, @s = the display)
function compileObjectClip(owner, c) {
  const o = ORG[owner], ds = c.displays || o.displays.map(d => d.name);
  const compiler = createRigCompiler({ns: NS, obj: 'apO', fn: () => {}, parts: o.displays.map(d => d.name), uuidOf: () => '', tol: {...TOL, tp: Object.fromEntries(o.displays.map(d => [d.name, d.name.startsWith('vine') || d.name.startsWith('heart_bulb') ? .03 : TOL.t]))}});
  const frames = clipFrames(owner, c);
  let keys = 0, files = 0;
  const nextC = c.next ? CLIPS[owner].find(x => x.name === c.next) : null;
  // a twin of a single object (the bulb's diagonal facets) has no clock of its own: its keys ride its parent's key
  // functions, addressed by UUID (one clock less per tick)
  const riding = d => d.twinOf && o.kind === 'single';
  const keyLines = new Map();
  const linesOf = name => { if (!keyLines.has(name)) keyLines.set(name, new Map()); return keyLines.get(name); };
  for (const name of [...ds].sort((x, y) => (riding(o.displays.find(q => q.name === x)) ? 1 : 0) - (riding(o.displays.find(q => q.name === y)) ? 1 : 0))) {
    const d = o.displays.find(x => x.name === name), rides = riding(d), byTick = linesOf(rides ? d.twinOf : name);
    const sel = rides ? uuidOf(d.idx) : '@s', addL = (t, l) => { if (!byTick.has(t)) byTick.set(t, []); byTick.get(t).push(l); };
    const {seq, out} = displaySegments(compiler, name, frames, c);
    for (const [a, b] of out) { addL(a, `data merge entity ${sel} ${xfNbt(written(seq[b]), b - a)}`); keys++; }
    frames.forEach((f, t) => { if ((t > 0 && f[name].look !== frames[t - 1][name].look) || (t === 0 && (c.force || []).includes(name))) for (const l of lookLines(owner, d, f[name].look, rides ? `execute as ${sel} ` : 'execute ').map(x => x.replace(/^execute run /, ''))) addL(t, l); });
    stepCheck(owner, c, name, seq);
  }
  for (const name of ds) {
    const d = o.displays.find(x => x.name === name);
    if (riding(d)) continue;
    const byTick = linesOf(name);
    const ticks = [...byTick.keys()].sort((x, y) => x - y);
    for (const t of ticks) fn(`${owner}/c/${c.name}/${name}/k/${t}`, byTick.get(t));
    files += ticks.length;
    const head = [`# ${owner} clip ${c.name} (id ${c.id}) on ${name}: ${c.len} t${c.loop ? ', loop' : c.next ? `, then ${c.next}` : ', then stops'}. @s = the display; apOC = the tick to apply now.`];
    if (c.loop) head.push(`execute if score @s apOC matches ${c.len}.. run scoreboard players set @s apOC 0`);
    else if (nextC && (nextC.displays || o.displays.map(x => x.name)).includes(name)) head.push(`execute if score @s apOC matches ${c.len}.. run return run function ${NS}/${owner}/c/${c.next}/${name}/enter`);
    else head.push(`execute if score @s apOC matches ${c.next ? c.len : c.len + 1}.. run return run scoreboard players set @s apOI -1`);
    fn(`${owner}/c/${c.name}/${name}/run`, [...head, ...tree(`${owner}/c/${c.name}/${name}/b`, 'apOC', ticks.map(t => [t, `${NS}/${owner}/c/${c.name}/${name}/k/${t}`]))]);
    fn(`${owner}/c/${c.name}/${name}/enter`, [`# Chain ${name} into ${c.name} now (tick 0). @s = the display.`, `scoreboard players set @s apOI ${c.id}`, `scoreboard players set @s apOC 0`, `function ${NS}/${owner}/c/${c.name}/${name}/k/0`]);
  }
  keyStats[`${owner}/${c.name}`] = {keys, keyFiles: files, len: c.len};
  return frames;
}
// per-tick rotation check (a slerp past ~120 degrees between two ticks has no stable direction)
function stepCheck(owner, c, name, seq) {
  for (let t = 1; t < seq.length; t++) {
    if (!shown(seq[t]) || !shown(seq[t - 1])) continue;
    const a = qAngle(seq[t - 1].q, seq[t].q);
    if (a > 100) errors.push(`${owner}/${c.name} ${name} t${t - 1}->${t}: ${a.toFixed(0)} degrees in one tick`);
  }
}

// ---- organisms ----------------------------------------------------------------------------------------------------------
const summonDisplay = ({uuid, tags, item, bright, xf, cull = [0, 0], view = 1.5, rotation}) =>
  `summon minecraft:item_display ~ ~ ~ {${uuid !== undefined ? `UUID:${uuidNbt(uuid)},` : ''}Tags:${JSON.stringify(tags)},billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:${fnum(view)}f,width:${fnum(cull[0])}f,height:${fnum(cull[1])}f,shadow_radius:0f,brightness:{block:${bright},sky:15},${rotation ? `Rotation:[${rotation}],` : ''}transformation:${nbt(xf)},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${itemId(item)}"}}}`;
const scaled = (v, k) => ({t: v.t, q: v.q, s: v.s.map(x => x * k)});
const allFrames = {};
for (const owner of KINDS) {
  const o = ORG[owner];
  allFrames[owner] = {};
  for (const c of CLIPS[owner]) allFrames[owner][c.name] = compileKindClip(owner, c);
  fn(`${owner}/run`, [`# ${o.name} (${owner}): the current clip (apOI) at tick apOC. @s = the husk.`, ...tree(`${owner}/d`, 'apOI', CLIPS[owner].map(c => [c.id, `${NS}/${owner}/c/${c.name}/run`]))]);
  fn(`${owner}/tick`, [`# Once per tick for every ${o.name} husk (the module's organism tick): apply tick apOC of clip apOI, then advance. @s = the husk.`, `function ${NS}/${owner}/run`, `scoreboard players add @s apOC 1`]);
  // spawn: the start clip's tick-0 pose (organisms other than the basic at the scale-in factor)
  const sc = CLIPS[owner].find(c => c.name === SPAWN_CLIP[owner]), f0 = allFrames[owner][sc.name][0];
  const sumLines = [];
  for (const d of o.displays) {
    if (d.overlay) continue;
    const xf = owner === 'basic' ? f0[d.name] : scaled(f0[d.name], SCALE_IN.from);
    sumLines.push(`execute positioned ~ ~${RIDE_Y} ~ run ${summonDisplay({tags: [...BASE_TAGS, 'rlk_ap_om', 'rlk_ap_om_' + d.name, 'rlk_ap_om_new'], item: d.looks[f0[d.name].look], bright: d.bright, xf: written(xf)})}`);
  }
  fn(`${owner}/spawn`, [`# The ${o.name} models riding @s (the aux husk, at it): ${o.displays.filter(d => !d.overlay).map(d => d.name).join(', ')}; then clip ${sc.name} from tick 0`,
    `# (${owner === 'basic' ? 'org_spawn is the emergence pop' : `scale-in ${SCALE_IN.from} -> 1 over the first ${SCALE_IN.ticks} t`}). Call once, right after aux/spawn.`,
    `function ${NS}/${owner}/kill`, 'tag @s add rlk_ap_om_v', ...sumLines,
    'execute as @e[type=minecraft:item_display,tag=rlk_ap_om_new] run ride @s mount @e[tag=rlk_ap_om_v,limit=1]',
    'tag @e[type=minecraft:item_display,tag=rlk_ap_om_new] remove rlk_ap_om_new', 'tag @s remove rlk_ap_om_v', `function ${NS}/face`,
    `scoreboard players set @s apOI ${sc.id}`, 'scoreboard players set @s apOC 0']);
  fn(`${owner}/kill`, [`# Remove the ${o.name} models (passengers tagged rlk_ap_om) of @s (the husk). Run before killing the husk.`, 'execute on passengers if entity @s[tag=rlk_ap_om] run kill @s']);
  for (const d of o.displays) for (const look of Object.keys(d.looks))
    fn(`${owner}/look/${d.name}/${look}`, [`# ${o.name} ${d.name}: look ${look} (${d.looks[look]}). @s = the husk.`, `execute on passengers if entity @s[tag=rlk_ap_om_${d.name}] run data modify entity @s item.components."minecraft:item_model" set value "${itemId(d.looks[look])}"`]);
  // overlays (basic shield, nurt ring): summoned riding the husk in their rest pose
  for (const d of o.displays.filter(x => x.overlay)) {
    const key = owner === 'basic' ? 'shield' : 'ring', rest = solve(owner, poseAt(owner, {name: 'rest', len: 0, keys: [[0, {}]]}, 0));
    const xf = displayXf(owner, d.name, rest[d.name]);
    fn(`${owner}/${key}/on`, [`# Show the ${d.name} overlay (riding @s, the husk). Idempotent.`, `function ${NS}/${owner}/${key}/off`, 'tag @s add rlk_ap_om_v',
      `execute positioned ~ ~${RIDE_Y} ~ run ${summonDisplay({tags: [...BASE_TAGS, 'rlk_ap_om', 'rlk_ap_om_' + d.name, 'rlk_ap_om_new'], item: d.looks[d.def], bright: d.bright, xf: written(xf)})}`,
      'execute as @e[type=minecraft:item_display,tag=rlk_ap_om_new] run ride @s mount @e[tag=rlk_ap_om_v,limit=1]', 'tag @e[type=minecraft:item_display,tag=rlk_ap_om_new] remove rlk_ap_om_new', 'tag @s remove rlk_ap_om_v',
      `execute rotated as @s on passengers if entity @s[tag=rlk_ap_om_${d.name}] run rotate @s ~ 0`]);
    fn(`${owner}/${key}/off`, [`# Remove the ${d.name} overlay of @s (the husk).`, `execute on passengers if entity @s[tag=rlk_ap_om_${d.name}] run kill @s`]);
  }
  // FN-29 fallback: the overhead HP bar (rlk_hb_* passengers, mob/hb_spawn) at hp_bar_y above the husk's feet
  const dy = o.hp_bar_y - (RIDE_Y + .25), Y = v => fnum(v + dy) + 'f';
  fn(`${owner}/bars`, [`# FN-29 fallback: move the rlk_hb_* HP-bar passengers of @s (the husk) so the bar sits ${o.hp_bar_y} b above its feet.`,
    `execute on passengers if entity @s[tag=rlk_hb_bg] run data merge entity @s {transformation:{translation:[-0.8f,${Y(.25)},0f]}}`,
    `execute on passengers if entity @s[tag=rlk_hb_fg] run data merge entity @s {transformation:{translation:[-0.8f,${Y(.25)},0.01f]}}`,
    `execute on passengers if entity @s[tag=rlk_hb_num] run data merge entity @s {transformation:{translation:[0f,${Y(.25)},0.06f]}}`,
    `execute on passengers if entity @s[tag=rlk_hb_lv] run data merge entity @s {transformation:{translation:[0f,${Y(.43)},0.06f]}}`,
    `execute on passengers if entity @s[tag=rlk_hb_icon] run data merge entity @s {transformation:{translation:[0f,${Y(.82)},0.06f]}}`]);
}
// the 포식성 forms outside its clips (the closed face between bites; fish / bud / pod restore): body look + jaw / fin shown
for (const [form, show] of [['fish', 1], ['bud', 0], ['pod', 0], ['face', 0]]) {
  const rest = allFrames.pred.pred_swim[0];
  fn(`pred/form/${form}`, [`# 포식성: switch to the ${form} form now (body look ${form}, jaw and tail fin ${show ? 'shown' : 'hidden'}). @s = the husk.`, `function ${NS}/pred/look/body/${form}`,
    ...['jaw', 'fin'].map(n => `execute on passengers if entity @s[tag=rlk_ap_om_${n}] run data merge entity @s ${xfNbt(written(show ? rest[n] : {...rest[n], s: [0, 0, 0]}), 2)}`)]);
}
fn('face', ['# Turn every Apep model passenger of @s (an organism husk) to its yaw (a tp would dismount them). @s = the husk.', 'execute rotated as @s on passengers if entity @s[tag=rlk_ap_om] run rotate @s ~ 0']);
fn('tick', ['# The per-tick clip step of any organism husk (dispatch on apK). @s = the husk.', ...KINDS.map(k => `execute if score @s apK matches ${ORG[k].id} run return run function ${NS}/${k}/tick`)]);
fn('kill', ['# Remove the model passengers of @s (any organism husk).', 'execute on passengers if entity @s[tag=rlk_ap_om] run kill @s']);

// ---- objects --------------------------------------------------------------------------------------------------------------
const objTags = (owner, d, extra = []) => [...BASE_TAGS, 'rlk_ap_om', 'rlk_ap_om_obj', `rlk_mb_ap_${d.name}`, ...extra];
const restFrame = owner => { const W = solve(owner, poseAt(owner, {name: 'rest', len: 0, keys: [[0, {}]]}, 0)); return Object.fromEntries(Object.entries(W).map(([n, w]) => [n, {...displayXf(owner, n, w), look: w.look}])); };
for (const owner of OBJECTS) {
  const o = ORG[owner];
  allFrames[owner] = {};
  for (const c of CLIPS[owner]) allFrames[owner][c.name] = compileObjectClip(owner, c);
  const rides = d => d.twinOf && o.kind === 'single';
  for (const d of o.displays) {
    const cs = CLIPS[owner].filter(c => (c.displays || o.displays.map(x => x.name)).includes(d.name));
    if (!cs.length || rides(d)) continue;
    fn(`${owner}/d/${d.name}/run`, [`# ${owner} ${d.name}: its clip (apOI) at tick apOC. @s = the display.`, ...tree(`${owner}/d/${d.name}/t`, 'apOI', cs.map(c => [c.id, `${NS}/${owner}/c/${c.name}/${d.name}/run`]))]);
    fn(`${owner}/d/${d.name}/tick`, [`# ${owner} ${d.name}: apply tick apOC of clip apOI, then advance. @s = the display.`, `function ${NS}/${owner}/d/${d.name}/run`, 'scoreboard players add @s apOC 1']);
  }
  // a display's look (and its twins' with it: they show the leader's look)
  const looksFn = (d, sel, inst, twinSel = () => null) => { for (const look of Object.keys(d.looks)) {
    const br = owner === 'heart' && (d.twinOf || d.name) === 'heart_bulb' ? (look === 'withered' ? 10 : 15) : null;
    const set = (x, item) => [`data modify entity ${x} item.components."minecraft:item_model" set value "${itemId(item)}"`, ...(br ? [`data merge entity ${x} {brightness:{block:${br},sky:15}}`] : [])];
    const tw = d.twinOf ? [] : o.displays.filter(t => t.twinOf === d.name).flatMap(t => set(twinSel(t), t.looks[look]));
    fn(`${owner}/look/${inst}${d.name}/${look}`, [`# ${owner} ${d.name}: look ${look}${tw.length ? ' (and its twin)' : ''}.`, ...set(sel, d.looks[look]), ...tw]);
  } };
  if (o.kind === 'single' || o.kind === 'fixed_set') {
    const n = o.kind === 'single' ? 1 : o.count, idxOf = (d, k) => (o.kind === 'single' ? d.idx : d.idxs[k]);
    const inst = k => (o.kind === 'single' ? '' : `i${k}/`);
    const tickLines = [];
    for (let k = 0; k < n; k++) for (const d of o.displays) if (!rides(d) && CLIPS[owner].some(c => (c.displays || []).includes(d.name)))
      tickLines.push(`execute as ${uuidOf(idxOf(d, k))} if score @s apOI matches 0.. run function ${NS}/${owner}/d/${d.name}/tick`);
    if (tickLines.length) fn(`${owner}/tick`, [`# Once per tick while the ${owner} exists: each display runs its own clip. Any executor.`, ...tickLines]);
    for (let k = 0; k < n; k++) {
      const I = inst(k), at = o.kind === 'single' ? '' : ` ${k}`;
      for (const c of CLIPS[owner]) fn(`${owner}/${I}play/${c.name}`, [`# Play ${c.name} on the ${owner}${at} (${(c.displays || []).join(', ')}) from tick 0 at the next ${owner}/tick. Any executor.`,
        ...(c.displays || []).filter(dn => !rides(o.displays.find(x => x.name === dn))).flatMap(dn => { const u = uuidOf(idxOf(o.displays.find(x => x.name === dn), k)); return [`scoreboard players set ${u} apOI ${c.id}`, `scoreboard players set ${u} apOC 0`]; })]);
      fn(`${owner}/${I}kill`, [`# Remove the ${owner}${at} displays${owner === 'heart' ? ' and the Heart marker' : ''}.`, ...(owner === 'heart' ? ['kill @e[type=minecraft:marker,tag=rlk_mb_ap_heart]'] : []), ...o.displays.map(d => `kill ${uuidOf(idxOf(d, k))}`)]);
      for (const d of o.displays) looksFn(d, uuidOf(idxOf(d, k)), I, t => uuidOf(idxOf(t, k)));
    }
    if (o.kind === 'fixed_set') {
      fn(`${owner}/spawn`, [`# function ${NS}/${owner}/spawn {i:<0..${n - 1}>} at the ${owner} spot, rotated as wanted.`, `$function ${NS}/${owner}/i$(i)/spawn`]);
      fn(`${owner}/play`, [`# function ${NS}/${owner}/play {i:<0..${n - 1}>,clip:"<clip>"}.`, `$function ${NS}/${owner}/i$(i)/play/$(clip)`]);
      fn(`${owner}/kill_all`, [`# Remove every ${owner} display.`, ...Array.from({length: n}, (_, k) => `function ${NS}/${owner}/i${k}/kill`)]);
    }
  }
}
// spawns of the objects
{ // the Heart: states entrance / canopy / play (SPAWN.heart), the marker at the centre
  const o = ORG.heart, sp = SPAWN.heart;
  for (const [state, {note, from}] of Object.entries(sp)) {
    const lines = [`# The Heart of the Oasis in its ${state} state at the arena centre (the floor point), rotated as wanted: ${note}.`, `function ${NS}/heart/kill`,
      `summon minecraft:marker ~ ~ ~ {Tags:${JSON.stringify(['rlk_mb_ap_heart', ...BASE_TAGS])}}`];
    for (const d of o.displays) {
      const [cn, t] = from[d.name], f = allFrames.heart[cn][t][d.name];
      lines.push(summonDisplay({uuid: d.idx, tags: objTags('heart', d), item: d.looks[f.look], bright: f.look === 'withered' ? 10 : d.bright, xf: written(f), cull: o.cull, view: 3}));
      lines.push(`rotate ${uuidOf(d.idx)} ~ 0`, `scoreboard players set ${uuidOf(d.idx)} apOI -1`, `scoreboard players set ${uuidOf(d.idx)} apOC 0`);
    }
    const loopOn = state === 'canopy' ? ['heart_hang', CLIPS.heart.find(c => c.name === 'heart_hang').displays] : state === 'play' ? ['heart_idle', withTwins('heart', ['heart_bulb', 'heart_tips'])] : null;
    if (loopOn) { const id = CLIPS.heart.find(c => c.name === loopOn[0]).id; for (const dn of loopOn[1]) { const d = o.displays.find(x => x.name === dn); if (!d.twinOf) lines.push(`scoreboard players set ${uuidOf(d.idx)} apOI ${id}`); } }
    fn(`heart/spawn/${state}`, lines);
  }
}
for (const owner of ['dome', 'stalk']) {
  const o = ORG[owner], first = CLIPS[owner][0], f0 = allFrames[owner][first.name][0];
  for (let k = 0; k < o.count; k++) fn(`${owner}/i${k}/spawn`, [`# ${owner} ${k} at the execution point (its yaw from the execution rotation), hidden at ${first.name} tick 0; play ${first.name} next.`, `function ${NS}/${owner}/i${k}/kill`,
    ...o.displays.flatMap(d => [summonDisplay({uuid: d.idxs[k], tags: objTags(owner, d), item: d.looks[d.def], bright: d.bright, xf: written(f0[d.name]), cull: o.cull, view: 2}), `rotate ${uuidOf(d.idxs[k])} ~ 0`,
      `scoreboard players set ${uuidOf(d.idxs[k])} apOI -1`, `scoreboard players set ${uuidOf(d.idxs[k])} apOC 0`])]);
}
{ // wall blades (multi, no fixed UUIDs): spawn one blade, rising
  const o = ORG.wall, d = o.displays[0], rise = CLIPS.wall[0], f0 = allFrames.wall[rise.name][0];
  fn('wall/spawn', [`# One wall blade at the execution point, facing the execution yaw; it plays wall_rise now. Tag it into its group with rlk_ap_om_new right after.`,
    'tag @e[type=minecraft:item_display,tag=rlk_ap_om_new] remove rlk_ap_om_new', summonDisplay({tags: objTags('wall', d, ['rlk_ap_om_new']), item: d.looks[d.def], bright: d.bright, xf: written(f0[d.name]), cull: o.cull, view: 2}),
    'execute as @e[type=minecraft:item_display,tag=rlk_ap_om_new,limit=1] run rotate @s ~ 0', `scoreboard players set @e[type=minecraft:item_display,tag=rlk_ap_om_new,limit=1] apOI ${rise.id}`,
    'scoreboard players set @e[type=minecraft:item_display,tag=rlk_ap_om_new,limit=1] apOC 0']);
  fn('wall/tick', ['# Once per tick while walls stand: every blade runs its clip.', `execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_wall_blade,scores={apOI=0..}] run function ${NS}/wall/d/wall_blade/tick`]);
  for (const c of CLIPS.wall) fn(`wall/play/${c.name}`, [`# Play ${c.name} on @s (a wall blade) from tick 0 at the next wall/tick.`, `scoreboard players set @s apOI ${c.id}`, 'scoreboard players set @s apOC 0']);
  fn('wall/kill_all', ['# Remove every wall blade display (the barrier blocks are the module\'s).', 'kill @e[type=minecraft:item_display,tag=rlk_mb_ap_wall_blade]']);
}
{ // the death seed
  const d = ORG.seed.displays[0], xf = restFrame('seed').seed;
  fn('seed/spawn', ['# The golden seed at the execution point (cosmetic; removed by cleanup).', `function ${NS}/seed/kill`, summonDisplay({uuid: d.idx, tags: objTags('seed', d), item: d.looks[d.def], bright: d.bright, xf: written(xf), cull: ORG.seed.cull, view: 2}), `rotate ${uuidOf(d.idx)} ~ 0`]);
}
fn('objects_tick', ['# Every object clip step (Heart, domes, stalks, walls); any executor, once per tick while any exists.', `function ${NS}/heart/tick`, `function ${NS}/dome/tick`, `function ${NS}/stalk/tick`, `function ${NS}/wall/tick`]);
fn('kill_all', ['# Remove every Apep phase-2 object display and organism model (cleanup paths kill them as rlk_mb_aux too).', 'kill @e[type=minecraft:marker,tag=rlk_mb_ap_heart]', 'kill @e[type=minecraft:item_display,tag=rlk_ap_om]']);
fn('init', ['# The objectives the org runtime uses (the module\'s init creates them too; idempotent).', ...['apK', 'apS', 'apT', 'apOC', 'apOI'].map(o => `scoreboard objectives add ${o} dummy`)]);

// ---- debug datapack (renders): exact per-tick poses, plain summons at the object origin (no passengers) -----------------
const dbg = arg('--debug-dp') && path.resolve(arg('--debug-dp'));
if (dbg) {
  const dd = path.join(dbg, 'data/rlk/function/om_dbg');
  fs.rmSync(dd, {recursive: true, force: true});
  const dput = (n, lines) => put(path.join(dd, n + '.mcfunction'), lines.join('\n'));
  const objXf = (owner, frame) => Object.fromEntries(Object.entries(frame).map(([n, v]) => [n, ORG[owner].type === 'kind' ? {...v, t: [v.t[0], v.t[1] + RIDE_Y, v.t[2]]} : v]));
  for (const owner of Object.keys(ORG)) {
    const o = ORG[owner];
    for (const c of CLIPS[owner]) allFrames[owner][c.name].forEach((frame, t) => {
      const X = objXf(owner, frame), ds = c.displays || o.displays.map(d => d.name);
      const lines = [];
      for (const d of o.displays) {
        if (d.overlay) continue;
        const v = ds.includes(d.name) ? X[d.name] : null;
        if (!v || !shown(written(v))) continue;
        lines.push(summonDisplay({tags: ['om_dbg', 'om_' + owner, 'om_' + d.name], item: d.looks[v.look], bright: d.bright, xf: written(v)}));
      }
      dput(`${owner}/${c.name}/${t}`, lines);
    });
    const R = objXf(owner, restFrame(owner));
    for (const d of o.displays) for (const [look, item] of Object.entries(d.looks)) {
      if (!shown(written(R[d.name]))) continue;
      dput(`${owner}/rest/${d.name}/${look}`, [summonDisplay({tags: ['om_dbg', 'om_' + owner, 'om_' + d.name], item, bright: d.bright, xf: written(R[d.name])})]);
    }
  }
  // the Heart spawn states
  for (const [state, {from}] of Object.entries(SPAWN.heart)) dput(`heart/state/${state}`, ORG.heart.displays.flatMap(d => { const [cn, t] = from[d.name], f = allFrames.heart[cn][t][d.name]; return shown(written(f)) ? [summonDisplay({tags: ['om_dbg', 'om_heart', 'om_' + d.name], item: d.looks[f.look], bright: d.bright, xf: written(f)})] : []; }));
}

// ---- manifest ---------------------------------------------------------------------------------------------------------
const r3 = v => v.map(x => +x.toFixed(3) || 0);
const clipRec = (owner, c) => ({id: c.id, name: c.name, len: c.len, loop: !!c.loop, next: c.next || null, events: c.events || {}, ...(c.displays ? {displays: c.displays} : {}),
  keys: keyStats[`${owner}/${c.name}`].keys, key_files: keyStats[`${owner}/${c.name}`].keyFiles, ...(c.note ? {note: c.note} : {})});
const restOf = Object.fromEntries(Object.keys(ORG).map(o => [o, restFrame(o)]));
const dispRec = (owner, d) => ({name: d.name, tag: ORG[owner].type === 'kind' ? 'rlk_ap_om_' + d.name : 'rlk_mb_ap_' + d.name, model: d.looks[d.def], looks: d.looks, default_look: d.def,
  brightness: d.bright, scale: d.scale, pivot: d.pivot, ...(ORG[owner].type === 'kind' ? {offset: r3(restOf[owner][d.name].t), overlay: !!d.overlay} : {}),
  ...(d.idx !== undefined ? {idx: d.idx, uuid: uuidOf(d.idx)} : {}), ...(d.idxs ? {idxs: d.idxs} : {}), ...(d.parent ? {parent: d.parent} : {}),
  joint: r3(restJoint(owner, d.name)), elements: Math.max(...Object.values(d.looks).map(it => models[items[it].model].els.length)), ...(d.note ? {note: d.note} : {})});
const manifest = {
  schema: 1, boss: 'apep', source: 'org', manifest: 'org', generator: 'tools/build_mboss_apep_org.mjs',
  runtime: {ns: 'rlk:mboss/apep/om/', kind_obj: 'apK', clip_obj: 'apOI', tick_obj: 'apOC', note: 'organisms: the husk holds apOI / apOC (om/<kind>/tick as the husk applies tick apOC then advances); objects: every display holds its own apOI / apOC (-1 = stopped), om/<object>/tick runs them'},
  uuids: {block: UUID_BLOCK, ints: UUID_INTS},
  objectives: {apK: 'organism kind id (kinds.<k>.id)', apS: 'organism state', apT: 'state clock', apL: 'link id (buffed basic -> its 양육)', apShd: 'shield pool', apOC: 'org clip clock (the tick applied at the next tick call)', apOI: 'org clip id (clips[].id; -1 = a stopped object display)', apSock: 'Heart socket (0-2, -1 none)', apTok: 'attack token'},
  passenger: {ride_y: RIDE_Y, tag_prefix: 'rlk_ap_om_', tags: BASE_TAGS, face: 'rotate', key: 'execute on passengers if entity @s[tag=rlk_ap_om_<display>] run data merge entity @s {..}',
    note: 'every model passenger also carries rlk_ap_om; culling off (width / height 0); om/face turns them to the husk yaw; om/<kind>/bars moves the rlk_hb_* bar to hp_bar_y (FN-29 fallback)'},
  spawn: {marker_ticks: 20, scale_in: SCALE_IN, untargetable_until: 'solid', clips: SPAWN_CLIP},
  kinds: Object.fromEntries(KINDS.map(k => { const o = ORG[k]; return [k, {id: o.id, name: o.name, tag: 'rlk_mb_ap_' + k, size: o.size, hover_y: o.hover, hp_bar_y: o.hp_bar_y, shield: o.shield,
    displays: o.displays.map(d => dispRec(k, d)), clips: CLIPS[k].map(c => clipRec(k, c)), budget: {elements: BUDGET[k][0], px: BUDGET[k][1]}, elements: elementsOf(k), px: pxOf(k),
    functions: {spawn: `${NS}/${k}/spawn`, tick: `${NS}/${k}/tick`, kill: `${NS}/${k}/kill`, play: `${NS}/${k}/play/<clip>`, start: `${NS}/${k}/start/<clip>`, look: `${NS}/${k}/look/<display>/<look>`, bars: `${NS}/${k}/bars`,
      ...(k === 'basic' ? {shield: `${NS}/basic/shield/on|off`} : {}), ...(k === 'nurt' ? {ring: `${NS}/nurt/ring/on|off`} : {}), ...(k === 'pred' ? {form: `${NS}/pred/form/<fish|bud|pod|face>`} : {})}}]; })),
  objects: {
    heart: {kind: 'single', tag: 'rlk_mb_ap_heart', marker: {tags: ['rlk_mb_ap_heart', ...BASE_TAGS], not: ['rlk_mob', 'rlk_zmob']},
      displays: ORG.heart.displays.map(d => dispRec('heart', d)), egg: {scale: .7, pitch: 0, land_ticks: 6, note: 'upright (pose pitch 90 about x of the lying lemon); scales to 1 and pitches to lying over the landing (heart_drop 0-6)'},
      clips: CLIPS.heart.map(c => clipRec('heart', c)), budget: {elements: BUDGET.heart[0], px: BUDGET.heart[1]}, elements: elementsOf('heart'), px: pxOf('heart'),
      states: Object.fromEntries(Object.entries(SPAWN.heart).map(([s, v]) => [s, {function: `${NS}/heart/spawn/${s}`, note: v.note}])),
      footprint: {centre: 'the arena centre (cx, cz) = theme POINTS["heart"]', note: 'bearings are compass degrees round the centre: 0 = north (-z), 90 = east (+x), 180 = south (+z); hang = the egg\'s lowest point above the floor',
        bulb_box: {l: 3.2, w: 2.6, h: 2.3, centre_y: 1.6, yaw: 0}, root_radius: 2.5,
        sockets: [{id: 0, bearing: 0, r: 3.4}, {id: 1, bearing: 120, r: 3.4}, {id: 2, bearing: 240, r: 3.4}], wait_ring: 4.5, destr_stop: {r: 2.6, bearings: [60, 180, 300]},
        wall_exclusion: 4.6, bolt_end: {r: 1.5, from: 'bulb_box'}, swirl_r: 3.5, hang: {entrance_y: HANG.entrance, canopy_y: HANG.canopy, lowered_y: HANG.lowered, cs_y: HANG.cs},
        arms_r: 2.6, arms_h: 4.3},
      functions: {spawn: `${NS}/heart/spawn/<entrance|canopy|play>`, tick: `${NS}/heart/tick`, play: `${NS}/heart/play/<clip>`, look: `${NS}/heart/look/<display>/<look>`, kill: `${NS}/heart/kill`}},
    dome: {kind: 'fixed_set', count: 3, radius: 4.5, tag: 'rlk_mb_ap_dome', displays: ORG.dome.displays.map(d => dispRec('dome', d)), clips: CLIPS.dome.map(c => clipRec('dome', c)),
      budget: {elements: BUDGET.dome[0], px: BUDGET.dome[1]}, elements: elementsOf('dome'), px: pxOf('dome'),
      functions: {spawn: `${NS}/dome/spawn {i}`, play: `${NS}/dome/play {i,clip}`, tick: `${NS}/dome/tick`, kill: `${NS}/dome/i<k>/kill`, kill_all: `${NS}/dome/kill_all`}},
    wall: {kind: 'multi', max: 15, tag: 'rlk_mb_ap_wall', blocks: ORG.wall.blocks, displays: ORG.wall.displays.map(d => dispRec('wall', d)), clips: CLIPS.wall.map(c => clipRec('wall', c)),
      budget: {elements: BUDGET.wall[0], px: BUDGET.wall[1]}, elements: elementsOf('wall'), px: pxOf('wall'),
      functions: {spawn: `${NS}/wall/spawn`, tick: `${NS}/wall/tick`, play: `${NS}/wall/play/<clip> (as the blade)`, kill_all: `${NS}/wall/kill_all`}},
    stalk: {kind: 'fixed_set', count: 4, height: [5.5, 6.0], tag: 'rlk_mb_ap_stalk', displays: ORG.stalk.displays.map(d => dispRec('stalk', d)), clips: CLIPS.stalk.map(c => clipRec('stalk', c)),
      budget: {elements: BUDGET.stalk[0], px: BUDGET.stalk[1]}, elements: elementsOf('stalk'), px: pxOf('stalk'), reach: 6.0,
      functions: {spawn: `${NS}/stalk/spawn {i} (positioned at the root, facing the lock)`, play: `${NS}/stalk/play {i,clip}`, tick: `${NS}/stalk/tick`, kill_all: `${NS}/stalk/kill_all`}},
    seed: {kind: 'single', tag: 'rlk_mb_ap_seed', displays: ORG.seed.displays.map(d => dispRec('seed', d)), clips: [], budget: {elements: BUDGET.seed[0], px: BUDGET.seed[1]}, elements: elementsOf('seed'), px: pxOf('seed'),
      functions: {spawn: `${NS}/seed/spawn`, kill: `${NS}/seed/kill`}},
  },
  budgets: {px_total: 200000, organism_elements: 500, heart_elements: 800, px: pxTotal},
  sprites: Object.fromEntries(Object.entries(SPR).map(([n, [w, h]]) => [n, {w, h, owner: SOWN[n]}])),
  functions: {face: `${NS}/face`, tick: `${NS}/tick`, objects_tick: `${NS}/objects_tick`, kill: `${NS}/kill`, kill_all: `${NS}/kill_all`, init: `${NS}/init`, files: FILES.size},
};
json(path.join(here, 'mboss_apep_org_manifest.json'), manifest);

// ---- test fixture: the exact per-tick display transforms (as written) of every clip --------------------------------------
if (arg('--dump')) {
  const out = {};
  for (const [owner, cs] of Object.entries(allFrames)) {
    out[owner] = {};
    for (const [cn, frames] of Object.entries(cs)) out[owner][cn] = frames.map(f => Object.fromEntries(Object.entries(f).map(([n, v]) => [n, {...written(v), look: v.look}])));
  }
  out._spawn = {scale_in: SCALE_IN, clips: SPAWN_CLIP};
  out._items = Object.fromEntries(Object.entries(ORG).map(([o, v]) => [o, Object.fromEntries(v.displays.map(d => [d.name, d.looks]))]));
  json(path.resolve(arg('--dump')), out);
}

// ---- report -----------------------------------------------------------------------------------------------------------
const rows = Object.keys(ORG).map(o => `${o.padEnd(6)} ${String(elementsOf(o)).padStart(4)} el / ${String(BUDGET[o][0]).padStart(3)}   ${String(pxOf(o)).padStart(6)} px / ${BUDGET[o][1]}`);
console.log(rows.join('\n'));
console.log(`sprites ${Object.keys(SPR).length} (${pxTotal} px / 200000), models ${Object.keys(models).length}, items ${Object.keys(items).length}, functions ${FILES.size}`);
const ks = Object.entries(keyStats).map(([k, v]) => `${k} ${v.keys}k/${v.len}t`).join(', ');
if (flag('--keys')) console.log(ks);
for (const w of warns) console.log('warn: ' + w);
if (errors.length) { for (const e of errors) console.log('ERROR: ' + e); process.exit(1); }
