// Display-entity rig of 마가츠 미타케 나루카미노 미코토 (Raiden): the Shogun (sword / polearm) and the Tenma form on one
// superset rig, built on the shared RIGLIB (mboss_rig_compile.mjs, mboss_rig_clips.mjs, mboss_model_lib.mjs,
// mboss_paint_lib.mjs). Scratchpad rd/plan.md §C (model, clips, budgets) and §E.0 (ownership).
//
// node tools/build_raiden_rig.mjs --resourcepack <unpacked pack> [--datapack <pack>] [--skin <png>] [--no-paint]
//                                 [--debug-dp <scratch dir>] [--allow-steps]
//
// Writes
//   RP  assets/rlk/textures/raiden/rig/*.png (raiden_paint.mjs) + item atlas entries;
//       assets/rlk/models/item/raiden/** and assets/rlk/items/raiden/** except fx_* and the illusion models
//       (parts, looks, props)
//   DP  data/rlk/function/boss/raiden/rig/** (rebuilt from scratch on every run); judgment/ and judgment_rig/ belong to
//       build_raiden_judgment_rig.mjs (the 만겁 rift and arm, restored 10-22a)
//   tools/raiden_rig_manifest.json (manifest v2: parts, looks, states, clips with events, props, px ledger, budgets)
//
// Runtime (contract: tools/raiden_rig_api.md):
//   * 30 item_display parts with FIXED UUIDs 524c4b4d-5244-4900-8000-0000000000NN (append-only table below), tags
//     rlk_room, rlk_raiden_part, rlk_raiden_aux, rlk_rd_<part>. The boss (the anchor) runs rig/tick each tick, at its feet.
//   * rig/play/<clip> queues a clip (tick 0 at the next rig/tick); the clips carry the form: a clip of the other form
//     switches the state at its tick 0, transform / t_collapse switch it at their form tick.
//   * rig/state/{shogun,tenma,hidden}, rig/look/{sword,polearm,tenma}, rig/flash, rig/kill, rig/face/*, rig/prop/<kind>.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {paintRaidenTextures, raidenSprites, spriteId, PROP_SPRITES} from './raiden_paint.mjs';
import {PARTS, PART_NAMES, BODY, TENMA_PARTS, PART_SCALE, allModels, LOOK_MODELS, PROPS, PROP_TINTS, FORMER_ITEMS, GHOST, solve, toDisplay, modelPoints} from './raiden_geometry.mjs';
import {CLIPS, CLIP_BY_NAME, C5, accumulate, sampleClip, restPose, loopStart} from './raiden_clips.mjs';
import {add, rot, slerp, lerp, qAngle, len, sub} from './mboss_rig_math.mjs';
import {createRigCompiler, createRigFollow, nbt, written, summonPart, cullOverhang} from './mboss_rig_compile.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const arg = n => { const i = process.argv.indexOf(n); return i < 0 ? null : process.argv[i + 1]; };
const flag = n => process.argv.includes(n);
const dp = path.resolve(arg('--datapack') || path.join(here, '..'));
const rp = arg('--resourcepack') && path.resolve(arg('--resourcepack'));
if (!rp) throw new Error('--resourcepack <unpacked pack> is required');
const put = (p, s) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, s.endsWith('\n') ? s : s + '\n'); };
const json = (p, o) => put(p, JSON.stringify(o, null, 2));
const NS = 'rlk:boss/raiden/rig';
const FN_ROOT = path.join(dp, 'data/rlk/function/boss/raiden');
const rigDir = path.join(FN_ROOT, 'rig');
fs.rmSync(rigDir, {recursive: true, force: true});
// the stagger clip loops from tick 20: its runner head is rewritten (the shared compiler loops whole clips only)
const runnerPatch = {};
const fn = (n, lines) => {
  let L = Array.isArray(lines) ? lines : [lines];
  const m = /^c\/([a-z0-9_]+)\/run$/.exec(n);
  if (m && runnerPatch[m[1]]) L = runnerPatch[m[1]](L);
  put(path.join(rigDir, n + '.mcfunction'), L.join('\n'));
};
const assets = path.join(rp, 'assets/rlk');
const t0 = Date.now();

// ---- parts and UUIDs (append-only: never renumber or reuse an index; a new part takes the next free one) ------------------
if (PARTS.length > 34) throw new Error(`${PARTS.length} parts: the cap is 34 (plan §C.4)`);
const UUID_INDEX = {
  head: 1, body: 2, right_arm: 3, right_forearm: 4, left_arm: 5, left_forearm: 6, right_leg: 7, right_shin: 8, left_leg: 9, left_shin: 10,
  braid: 11, drape: 12, weapon: 13, weapon_fx: 14, halo: 15, aura: 16,
  disc: 17, g_upper: 18, g_fore: 19, g_hand: 20, glaive: 21, glaive_fx: 22, ra1_up: 23, ra1_fo: 24, ra2_up: 25, ra2_fo: 26, ra3_up: 27, ra3_fo: 28,
  gaunt_l: 29, gaunt_r: 30,
};
for (const n of PART_NAMES) if (!UUID_INDEX[n]) throw new Error(`part ${n} has no UUID index (append it)`);
const UUID_HI = [1380731725, 1380206848, -2147483648];          // 524c4b4d-5244-4900-8000-
const uuidOf = n => `524c4b4d-5244-4900-8000-${UUID_INDEX[n].toString(16).padStart(12, '0')}`;
const uuidInts = n => [...UUID_HI, UUID_INDEX[n]];
const itemId = m => `rlk:raiden/${m}`;
const CULL = {width: 16, height: 10}, VIEW_RANGE = 3;

// ---- resource pack ------------------------------------------------------------------------------------------------------------
if (arg('--skin')) { fs.mkdirSync(path.join(assets, 'textures/raiden'), {recursive: true}); fs.copyFileSync(arg('--skin'), path.join(assets, 'textures/raiden/skin.png')); }
if (!fs.existsSync(path.join(assets, 'textures/raiden/skin.png'))) throw new Error('the pack has no textures/raiden/skin.png (pass --skin)');
const spriteTable = raidenSprites(rp);
if (!flag('--no-paint')) paintRaidenTextures(rp);
const models = allModels();
const modelDir = path.join(assets, 'models/item/raiden'), itemDir = path.join(assets, 'items/raiden');
// Former outputs of this generator and of the release rig (the old armour, katana and puppet items): dropped. The
// fx_* trees belong to the kit generators except fx_weapon (only the old rig made it); illusion* is the illusions
// generator's, judgment/ the 만겁 rig's (build_raiden_judgment_rig.mjs).
const FORMER = ['armor', 'chakra', 'crown', 'ribbon', 'ribbon_dull', 'katana', 'polearm', 'giant_katana', 'puppet_upper', 'puppet_forearm',
  ...['open', 'closed', 'claw'].flatMap(k => [`puppet_hand_${k}`, `puppet_hand_${k}_l`]), 'support_upper', 'support_forearm', 'support_hand_r', 'support_hand_l',
  'electro_orb', 'lightning_stake', 'remembrance_flower', 'death_shard_0', 'death_shard_1', 'death_shard_2', ...BODY.flatMap(n => [n, n + '_dull'])];
for (const d of [modelDir, itemDir]) {
  for (const n of FORMER) fs.rmSync(path.join(d, n + '.json'), {force: true});
  for (const sub of ['fx_weapon', 'prop']) fs.rmSync(path.join(d, sub), {recursive: true, force: true});
  for (const f of fs.existsSync(d) ? fs.readdirSync(d) : []) if (/^t_.*\.json$/.test(f) || /^(g_|ra\d|gaunt|glaive|disc|halo|aura|braid|drape|katana|polearm)/.test(f)) fs.rmSync(path.join(d, f), {force: true});
}
const usedSprites = new Set();
for (const [name, els] of Object.entries(models)) {
  const used = [...new Set(els.flatMap(e => Object.values(e.faces).map(f => f.texture.slice(1))))];
  const tex = {};
  for (const u of used) {
    if (u === 'skin') tex[u] = 'rlk:raiden/skin';
    else { if (!spriteTable[u]) throw new Error(`model ${name}: unknown sprite ${u}`); tex[u] = spriteId(u); usedSprites.add(u); }
  }
  const tinted = Object.values(PROP_TINTS).some(([m]) => m === name);
  const els2 = tinted ? els.map(e => ({...e, faces: Object.fromEntries(Object.entries(e.faces).map(([k, f]) => [k, {...f, tintindex: 0}]))})) : els;
  json(path.join(modelDir, name + '.json'), {ambientocclusion: false, textures: {...tex, particle: tex[used[0]]}, elements: els2});
  if (!tinted) json(path.join(itemDir, name + '.json'), {model: {type: 'minecraft:model', model: 'rlk:item/raiden/' + name}});
}
for (const [item, [m, rgb]] of Object.entries(PROP_TINTS)) json(path.join(itemDir, item + '.json'), {model: {type: 'minecraft:model', model: 'rlk:item/raiden/' + m, tints: [{type: 'minecraft:constant', value: rgb}]}});
for (const item of FORMER_ITEMS) fs.rmSync(path.join(itemDir, item + '.json'), {force: true});   // the S1-S2 legacy item ids
const unusedSprites = Object.keys(spriteTable).filter(n => !usedSprites.has(n));
if (unusedSprites.length) throw new Error(`painted but unused sprites: ${unusedSprites.join(', ')}`);
// px ledger (plan §C.6): rig sprites <= 0.45 M, props <= 0.25 M
const px = {rig: 0, props: 0}, ledger = {};
for (const [n, [w, h]] of Object.entries(spriteTable)) {
  if (w > 512 || h > 512 || w % 16 || h % 16) throw new Error(`sprite ${n} ${w}x${h}: sides <= 512, multiples of 16`);
  ledger[n] = w * h; px[PROP_SPRITES.has(n) ? 'props' : 'rig'] += w * h;
}
if (px.rig > .45e6) throw new Error(`rig sprites ${px.rig} px > 0.45 M`);
if (px.props > .25e6) throw new Error(`prop sprites ${px.props} px > 0.25 M`);
// elements shown at once (client cost; plan §C.3: <= 3.5 k Shogun, <= 6 k Tenma)
const ecount = m => (models[m] || []).length;
const shogunEls = BODY.reduce((a, n) => a + ecount(n), 0) + ['braid', 'drape', 'katana', 'katana_fx', 'halo', 'aura'].reduce((a, m) => a + ecount(m), 0);
const shogunElsP = shogunEls - ecount('katana') - ecount('katana_fx') + ecount('polearm') + ecount('polearm_fx');
const tenmaEls = BODY.reduce((a, n) => a + ecount('t_' + n), 0) + ecount('braid') + PARTS.filter(p => p[3] === 'tenma').reduce((a, p) => a + ecount(p[1]), 0);
if (Math.max(shogunEls, shogunElsP) > 3500) throw new Error(`Shogun shows ${Math.max(shogunEls, shogunElsP)} elements (budget 3.5 k)`);
if (tenmaEls > 6000) throw new Error(`Tenma shows ${tenmaEls} elements (budget 6 k)`);

// ---- per-part hull points (A-frame units) for the floor and culling checks ---------------------------------------------------
const HULL = {};
for (const [name, els] of Object.entries(models)) {
  const seen = new Set(), pts = [];
  for (const P of modelPoints(els)) { const k = P.map(v => v.toFixed(2)).join(','); if (!seen.has(k)) { seen.add(k); pts.push(P); } }
  HULL[name] = pts;
}
// the item model a part shows at a frame (looks: form + weapon); the floor check takes the worst of both weapons
const partModels = (n, form) => {
  if (BODY.includes(n)) return [form === 't' ? 't_' + n : n];
  if (n === 'weapon') return ['katana', 'polearm'];
  if (n === 'weapon_fx') return ['katana_fx', 'polearm_fx'];
  return [PARTS.find(p => p[0] === n)[1]];
};
const worldPts = (o, n, form) => {
  const v = o[n], S = v.s.map((x, i) => x * PART_SCALE[n][i] / 16);
  if (Math.max(...v.s.map(Math.abs)) < 1e-4) return [];
  return partModels(n, form).flatMap(m => HULL[m].map(P => add(v.t, rot(v.q, [P[0] * S[0], P[1] * S[1], P[2] * S[2]]))));
};

// ---- clip compile -------------------------------------------------------------------------------------------------------------
const debugDp = arg('--debug-dp') && path.resolve(arg('--debug-dp'));
if (debugDp) fs.rmSync(path.join(debugDp, 'data/rlk/function/rd_dbg'), {recursive: true, force: true});
const putDebug = (n, lines) => put(path.join(debugDp, 'data/rlk/function', n + '.mcfunction'), lines.join('\n'));
const TOL = {t: .02, s: .02, rDefault: 1.5, r: {glaive: .7, glaive_fx: .7, g_upper: .9, g_fore: .9, ra1_up: 1.2, ra2_up: 1.2, ra3_up: 1.2, disc: 1.2, weapon: 1, weapon_fx: 1},
  tp: {glaive: .035, glaive_fx: .035, g_upper: .03, g_fore: .03, g_hand: .03, gaunt_l: .03, gaunt_r: .03}};
let debugFrames = null;
const compiler = createRigCompiler({ns: NS, obj: 'rdRig', fn, parts: PART_NAMES, uuidOf, tol: TOL});
const debugLook = p => [`function ${NS}/look/${p.form === 't' ? 'tenma_models' : 'shogun_models'}`];
// follow lists per state; the static-anchor skip keeps a standing boss at 5 commands
const LISTS = {shogun: PART_NAMES.filter(n => !TENMA_PARTS.includes(n)), tenma: PART_NAMES.filter(n => !['drape', 'weapon', 'weapon_fx', 'halo', 'aura'].includes(n)), all: PART_NAMES};
const follow = createRigFollow({ns: NS, obj: 'rdRig', fn, uuidOf, lists: LISTS, staticSkip: true,
  comment: '# Parts follow the anchor position and yaw (run as and rotated as the boss at its feet, pitch 0).'});
const STATE_ID = {shogun: 0, tenma: 1, hidden: 2};

function solveFrame(clip, t, ks, prev) { const p = sampleClip(clip, t, ks); const o = solve(p, prev); const d = {}; for (const n of PART_NAMES) d[n] = toDisplay(n, o[n]); return {d, p, o}; }
// Key reduction ("knots"): every part keys on the same ticks. The authored key ticks (and quarter loops) are knots; an
// interval splits at its worst tick while the true pose (forward kinematics, eased) leaves the client's interpolation
// between the knots (lerp / slerp in display space) by more than KNOT_DEV, or a part turns more than KNOT_TURN degrees
// in it. The compiled frames are those interpolations, so the shipped motion is exactly what the checks see.
const KNOT_DEV = {r: 30, t: .24, s: .25}, KNOT_TURN = 115, BLEND = 3;
const FLOOR_SPLIT = new Set(['weapon', 'weapon_fx', 'glaive', 'glaive_fx', 'drape', 'right_shin', 'left_shin', 'g_hand', 'gaunt_l', 'gaunt_r']);
const lerpD = (a, b, u) => ({t: lerp(a.t, b.t, u), q: slerp(a.q, b.q, u), s: lerp(a.s, b.s, u)});
const shownD = v => v.s.some(x => Math.abs(x) > 1e-4);
const fromDisplay = (n, v) => ({t: [v.t[0], v.t[1], -v.t[2]], q: [-v.q[0], -v.q[1], v.q[2], v.q[3]], s: v.s.map((x, i) => x / PART_SCALE[n][i])});
function knotsOf(c, truth) {
  const K = new Set([0, c.len, ...c.keys.map(k => k[0])]);
  if (c.loopFrom != null) K.add(c.loopFrom);
  if (c.loop) for (let i = 1; i < 4; i++) K.add(Math.round(c.len * i / 4));
  // the blend-in: the first key interval lasts >= BLEND ticks (a clip starts from any pose)
  const ks = [...K].filter(t => t === 0 || t >= Math.min(BLEND, c.len)).sort((a, b) => a - b);
  const worst = (a, b) => {
    let best = null, bw = 0;
    for (const n of PART_NAMES) {
      const A = truth[a].d[n], B = truth[b].d[n];
      if (!shownD(A) && !shownD(B)) continue;
      const turn = shownD(A) && shownD(B) ? qAngle(A.q, B.q) : 0;
      if (turn > KNOT_TURN && b - a > 1) { const w = turn / KNOT_TURN; if (w > bw) { bw = w; best = a + Math.floor((b - a) / 2); } }
      for (let t = a + 1; t < b; t++) {
        const I = lerpD(A, B, (t - a) / (b - a)), T = truth[t].d[n];
        const big = Math.max(...T.s.map(Math.abs), ...I.s.map(Math.abs));
        const w = Math.max(big > 1e-4 ? qAngle(I.q, T.q) / KNOT_DEV.r : 0, len(sub(I.t, T.t)) / KNOT_DEV.t, Math.max(...I.s.map((x, i) => Math.abs(x - T.s[i]))) / Math.max(1, big) / KNOT_DEV.s);
        if (w > bw) { bw = w; best = t; }
        // the interpolated pose must not dip below the floor where the true one stays above it
        if (FLOOR_SPLIT.has(n) && shownD(I)) {
          const yi = Math.min(...worldPts({[n]: fromDisplay(n, I)}, n, truth[t].p.form).map(P => P[1]));
          if (yi < -.01) { const yt = Math.min(...worldPts({[n]: fromDisplay(n, T)}, n, truth[t].p.form).map(P => P[1])); if (yt > yi + .02 && 50 > bw) { bw = 50; best = t; } }
        }
      }
    }
    return bw > 1 ? best : null;
  };
  const out = [ks[0]];
  for (let i = 1; i < ks.length; i++) {
    const stack = [[out[out.length - 1], ks[i]]];
    while (stack.length) {
      const [a, b] = stack.pop();
      const m = b - a > 1 ? worst(a, b) : null;
      if (m !== null && a === 0 && m < BLEND) { out.push(b); continue; }
      if (m === null) { out.push(b); continue; }
      stack.push([m, b], [a, m]);
    }
  }
  return [...new Set(out)].sort((a, b) => a - b);
}
function clipFrames(c, ks) {
  const truth = [];
  for (let t = 0; t <= c.len; t++) truth.push(solveFrame(c, t, ks, t ? truth[t - 1].o._prev : null));
  const knots = knotsOf(c, truth);
  const at = x => {
    let i = 0; while (i < knots.length - 2 && knots[i + 1] <= x) i++;
    const a = knots[i], b = knots[i + 1], u = Math.min(1, Math.max(0, (x - a) / (b - a)));
    const d = {}, o = {};
    for (const n of PART_NAMES) { d[n] = lerpD(truth[a].d[n], truth[b].d[n], u); o[n] = fromDisplay(n, d[n]); }
    return {d, p: truth[Math.min(c.len, Math.floor(x))].p, o};
  };
  return {frames: Array.from({length: c.len + 1}, (_, t) => (knots.includes(t) ? {...truth[t], o: Object.fromEntries(PART_NAMES.map(n => [n, fromDisplay(n, truth[t].d[n])]))} : at(t))), half: a => at(a + .5), knots};
}
// Key emission aligned to the knots (the shared compiler's per-part greedy segments would end anywhere between them):
// every part keys at a knot only when it moves in the next knot interval (all parts at tick 0, the blend-in); the clip
// runner, play/<clip> and start/<clip> are written as mboss_rig_compile.mjs compileClip writes them.
const close0 = (a, b) => len(sub(a.t, b.t)) < 1e-4 && qAngle(a.q, b.q) < .05 && Math.max(...a.s.map((x, i) => Math.abs(x - b.s[i]))) < 1e-4;
function compileKnots(c, frames, knots, extraLines) {
  const motionErrors = compiler.stepViolations(c, frames);
  const byTick = new Map(), add = (t, l) => { if (!byTick.has(t)) byTick.set(t, []); byTick.get(t).push(l); };
  let keyCount = 0;
  for (const n of PART_NAMES) for (let i = 0; i < knots.length - 1; i++) {
    const a = knots[i], b = knots[i + 1], A = frames[a].d[n], B = frames[b].d[n];
    if (i > 0 && close0(A, B)) continue;
    if (shownD(A) && shownD(B) && qAngle(A.q, B.q) > 118) motionErrors.push(`${c.name} ${n} t${a}-${b}: ${qAngle(A.q, B.q).toFixed(0)} degree key (ambiguous slerp)`);
    add(a, `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:${b - a},transformation:${nbt(written(B))}}`);
    keyCount++;
  }
  frames.forEach((f, t) => { for (const line of extraLines(t) || []) add(t, line); });
  if (debugDp) frames.forEach((f, t) => putDebug(`rd_dbg/${c.name}/${t}`, [...PART_NAMES.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(written(f.d[n]))}}`), ...debugLook(f.p)]));
  const ticks = [...byTick.keys()].sort((x, y) => x - y);
  for (const t of ticks) fn(`c/${c.name}/k/${t}`, byTick.get(t));
  const obj = 'rdRig';
  const head = [`# ${c.name}: ${c.len} t${c.loop ? ', loop' : ', holds the last pose'}. @s = rig anchor.`];
  if (c.loop) head.push(`execute if score @s ${obj}T matches ${c.len}.. run scoreboard players set @s ${obj}T 0`);
  else head.push(`execute if score @s ${obj}T matches ${c.len + 1}.. run return run scoreboard players set @s ${obj}T ${c.len + 1}`);
  // dispatch: up to 10 key ticks inline, else one level of groups of <= 8 (<= 6 + 8 checks per tick)
  const leaf = list => list.map(t => `execute if score @s ${obj}T matches ${t} run return run function ${NS}/c/${c.name}/k/${t}`);
  const tree = list => {
    if (list.length <= 10) return leaf(list);
    const g = Math.ceil(list.length / Math.ceil(list.length / 8)), out = [];
    for (let i = 0; i < list.length; i += g) {
      const part = list.slice(i, i + g), name = `c/${c.name}/b/${part[0]}_${part[part.length - 1]}`;
      fn(name, leaf(part));
      out.push(`execute if score @s ${obj}T matches ..${part[part.length - 1]} run return run function ${NS}/${name}`);
    }
    return out;
  };
  fn(`c/${c.name}/run`, [...head, ...tree(ticks)]);
  fn(`play/${c.name}`, [`# Play clip ${c.name} (${c.len} t) from its tick 0 at the next rig/tick. @s = rig anchor.`, `scoreboard players set @s ${obj}C ${c.id}`, `scoreboard players set @s ${obj}T -1`]);
  fn(`start/${c.name}`, [`# Start clip ${c.name} now (tick 0 applied immediately). @s = rig anchor.`, `scoreboard players set @s ${obj}C ${c.id}`, `scoreboard players set @s ${obj}T 0`, `function ${NS}/c/${c.name}/k/0`]);
  return {info: {id: c.id, name: c.name, len: c.len, loop: !!c.loop, events: c.events || {}, keyFiles: ticks.length, keys: keyCount, note: c.note || ''}, motionErrors, warns: []};
}
const clipInfo = [], motionErrors = [], floorErrors = [], cullWarn = [], eventErrors = [], warns = new Set();
let keyFiles = 0;
for (const c of CLIPS) {
  const [len, ev] = C5[c.name] || [];
  if (len === undefined) eventErrors.push(`${c.name}: not in plan §C.5`);
  else {
    if (c.len !== len) eventErrors.push(`${c.name}: len ${c.len}, §C.5 ${len}`);
    for (const [k, v] of Object.entries(ev)) if (c.events[k] !== v) eventErrors.push(`${c.name}: event ${k} ${c.events[k]}, §C.5 ${v}`);
    for (const k of Object.keys(c.events)) if (!(k in ev)) eventErrors.push(`${c.name}: event ${k} not in §C.5`);
  }
  if (c.keys[0][0] !== 0 || c.keys[c.keys.length - 1][0] !== c.len) throw new Error(`clip ${c.name}: keys must run 0..${c.len}`);
  const ks = accumulate(c);
  const {frames, half, knots} = clipFrames(c, ks);
  debugFrames = frames;
  // floor: no shown element of any part below y 0 (2 cm slack); the Tenma gauntlets keep 0.3 b
  frames.forEach((f, t) => {
    for (const n of PART_NAMES) {
      const pts = worldPts(f.o, n, f.p.form);
      if (!pts.length) continue;
      const y = Math.min(...pts.map(P => P[1])), lim = n.startsWith('gaunt') ? .3 : -.02;
      if (y < lim) floorErrors.push(`${c.name} t${t} ${n}: lowest point ${y.toFixed(3)} b`);
      const over = Math.max(...pts.map(P => cullOverhang(P, CULL)));
      if (over > 0) cullWarn.push(`${c.name} t${t} ${n} ${over.toFixed(2)} b`);
    }
  });
  // state lines: tick 0 enforces the clip's form (a played clip also unhides the rig); form ticks switch it
  const extra = t => {
    const out = [], p = frames[t].p;
    if (t === 0) {
      if (c.form === 's') out.push(`execute unless score @s rdRigS matches 0 run function ${NS}/state/shogun`);
      else if (c.form === 't') out.push(`execute unless score @s rdRigS matches 1 run function ${NS}/state/tenma`);
      else out.push(`execute if score @s rdRigS matches 2 run function ${NS}/state/shogun`);
      if (c.name === 'death' || c.name === 'transform' || c.name === 't_collapse') out.push(...follow.listLines('all'));
    } else if (c.form !== 'k' && p.form !== frames[t - 1].p.form) out.push(`function ${NS}/state/${p.form === 't' ? 'tenma' : 'shogun'}`, ...follow.listLines('all'));
    if (c.swap && c.swap[t]) out.push(`function ${NS}/look/${c.swap[t]}`);
    return out;
  };
  const ls = loopStart(c);
  if (c.loopFrom != null) runnerPatch[c.name] = L => L.map(l => l.replace(`execute if score @s rdRigT matches ${c.len + 1}.. run return run scoreboard players set @s rdRigT ${c.len + 1}`,
    `execute if score @s rdRigT matches ${c.len}.. run scoreboard players set @s rdRigT ${c.loopFrom}`).replace(`holds the last pose`, `loops ${c.loopFrom}-${c.len}`));
  const r = compileKnots(c, frames, knots, extra);
  keyFiles += r.info.keyFiles;
  clipInfo.push({...r.info, knots: knots.length, form: c.form === 'k' ? 'keep' : c.form === 't' ? 'tenma' : 'shogun', loopFrom: ls,
    formSwitch: c.formAt ? Object.fromEntries(Object.entries(c.formAt).map(([k, v]) => [k, v === 't' ? 'tenma' : 'shogun'])) : null,
    weaponSwap: c.swap || null});
}
const fail = (title, list) => { if (list.length) { const m = `${title}:\n  ${list.slice(0, 50).join('\n  ')}${list.length > 50 ? `\n  ... ${list.length} in all` : ''}`; if (flag('--allow-steps')) console.warn(m); else throw new Error(m); } };
fail('clip events vs plan §C.5', eventErrors);
fail('floor (no shown element below y 0; gauntlets >= 0.3 b)', floorErrors);
fail('part rotations above 120 degrees per tick or per key', motionErrors);
compiler.writeDispatch(CLIPS);
follow.write();

// ---- API functions -------------------------------------------------------------------------------------------------------------
const restD = which => { const o = solve(restPose(which)); return Object.fromEntries(PART_NAMES.map(n => [n, toDisplay(n, o[n])])); };
const REST = {s: restD('s'), t: restD('t')};
const swap = (part, model) => `data modify entity ${uuidOf(part)} item.components."minecraft:item_model" set value "${itemId(model)}"`;
const OBJ = ['rdRigC', 'rdRigT', 'rdRigY', 'rdRigS', 'rdRigW', 'rdRigF', ...follow.objectives];
fn('init', ['# Rig objectives (safe on every load). rdRigC clip id, rdRigT clip tick, rdRigS state (0 shogun, 1 tenma, 2 hidden),',
  '# rdRigW weapon (0 sword, 1 polearm), rdRigF hit flash, rdRigY face scratch.',
  ...OBJ.map(o => `scoreboard objectives add ${o} dummy`)]);
const TAGS = n => ['rlk_room', 'rlk_raiden_part', 'rlk_raiden_aux', 'rlk_rd_' + n];
const summon = (n, which) => summonPart({uuid: uuidInts(n), tags: TAGS(n), item: itemId(PARTS.find(p => p[0] === n)[1]), brightness: PARTS.find(p => p[0] === n)[2],
  pose: REST[which][n], viewRange: VIEW_RANGE, cull: CULL});
const CLIP_ID = Object.fromEntries(CLIPS.map(c => [c.name, c.id]));
fn('spawn', ['# @s = the boss (the anchor), at its feet. Summons the 30 parts (fixed UUIDs) in the rest pose of the stored state',
  '# (rdRigS: 1 = Tenma, else Shogun), re-applies the looks and queues the state\'s idle clip.',
  `function ${NS}/init`, `function ${NS}/kill`,
  'execute unless score @s rdRigS matches 0..2 run scoreboard players set @s rdRigS 0',
  'execute unless score @s rdRigW matches 0..1 run scoreboard players set @s rdRigW 0',
  'execute if score @s rdRigS matches 2 run scoreboard players set @s rdRigS 0',
  `execute if score @s rdRigS matches 1 run function ${NS}/spawn_tenma`,
  `execute unless score @s rdRigS matches 1 run function ${NS}/spawn_shogun`,
  'scoreboard players set @s rdRigF 0',
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow_now`]);
fn('spawn_shogun', ['# Internal (spawn): the Shogun rest pose, the stored weapon, idle.', ...PART_NAMES.map(n => summon(n, 's')),
  `function ${NS}/state/shogun`, `execute if score @s rdRigW matches 1 run function ${NS}/play/idle_polearm`, `execute unless score @s rdRigW matches 1 run function ${NS}/play/idle_sword`]);
fn('spawn_tenma', ['# Internal (spawn): the Tenma rest pose, idle.', ...PART_NAMES.map(n => summon(n, 't')), `function ${NS}/state/tenma`, `function ${NS}/play/t_idle`]);
fn('tick', ['# @s = the boss (the anchor), at its feet, once per game tick. Missing parts respawn.',
  `execute unless entity ${uuidOf('body')} run function ${NS}/spawn`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow`,
  'execute if score @s rdRigF matches 1.. run scoreboard players remove @s rdRigF 1',
  `execute if score @s rdRigF matches 0 run function ${NS}/flash_off`,
  '# hidden: nothing runs until a clip is queued (its tick 0 shows the rig again)',
  'execute if score @s rdRigS matches 2 unless score @s rdRigT matches -1 run return 0',
  'scoreboard players add @s rdRigT 1',
  `function ${NS}/run`]);
fn('kill', ['# Removes every rig part.', 'kill @e[type=item_display,tag=rlk_raiden_part]']);
fn('cleanup', ['# Kept for callers of the old rig: same as kill.', `function ${NS}/kill`]);
// looks
const lookLines = which => Object.entries(LOOK_MODELS[which]).map(([n, m]) => swap(n, m));
fn('look/shogun_models', ['# Internal: the Shogun body models.', ...lookLines('shogun')]);
fn('look/tenma_models', ['# Internal: the Tenma body models.', ...lookLines('tenma')]);
fn('look/sword', ['# Shogun with the katana (rdRigW 0). Call from the Shogun state; a Tenma clip keeps its own look.', 'scoreboard players set @s rdRigW 0', ...lookLines('sword'),
  `execute unless score @s rdRigS matches 1 run function ${NS}/look/shogun_models`]);
fn('look/polearm', ['# Shogun with the polearm (rdRigW 1).', 'scoreboard players set @s rdRigW 1', ...lookLines('polearm'),
  `execute unless score @s rdRigS matches 1 run function ${NS}/look/shogun_models`]);
fn('look/tenma', ['# The Tenma body look (dark bodysuit, pale plates, tassets).', `function ${NS}/look/tenma_models`]);
// states
fn('state/shogun', ['# Shogun state: follow list, Shogun body look and the stored weapon (rdRigW). @s = the boss.', 'scoreboard players set @s rdRigS 0',
  ...follow.listLines('shogun'), `function ${NS}/look/shogun_models`, `execute if score @s rdRigW matches 1 run function ${NS}/look/polearm`,
  `execute unless score @s rdRigW matches 1 run function ${NS}/look/sword`]);
fn('state/tenma', ['# Tenma state: follow list and the Tenma body look. @s = the boss.', 'scoreboard players set @s rdRigS 1', ...follow.listLines('tenma'), `function ${NS}/look/tenma_models`]);
fn('state/hidden', ['# Hidden (blinks, 찰나의 포영, 만겁): every part at scale 0 where it stands (never moved below the floor) and no clip',
  '# runs; the parts keep following the boss. The next rig/play shows the rig again (its tick 0 sets the clip\'s state). @s = the boss.',
  'scoreboard players set @s rdRigS 2', ...follow.listLines('all'), 'scoreboard players set @s rdRigT 0',
  ...PART_NAMES.map(n => `data modify entity ${uuidOf(n)} transformation.scale set value [0f,0f,0f]`)]);
// hit flash: the body group glows for 3 ticks
const FLASH = [...BODY, 'braid'];
fn('flash', ['# Hit feedback: the body glows violet-white for 3 ticks. @s = the boss.', 'scoreboard players set @s rdRigF 3',
  ...FLASH.map(n => `data merge entity ${uuidOf(n)} {Glowing:1b,glow_color_override:13383423}`)]);
fn('flash_off', ['# Internal: end of the hit flash.', 'scoreboard players reset @s rdRigF', ...FLASH.map(n => `data merge entity ${uuidOf(n)} {Glowing:0b}`)]);
compiler.writeFace({marker: 'rlk_rd_face', maxDeg: 12});
// props (separate entities, never rig parts): tags rlk_room, rlk_raiden_aux, rlk_rd_prop, rlk_rd_prop_<kind>, rlk_rd_prop_new (this call)
const f4 = x => String(+x.toFixed(4));
const propSummon = (kind, P, model, rotation = '') => `summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_prop","rlk_rd_prop_${kind}","rlk_rd_prop_new"],${rotation}billboard:"${P.billboard || 'fixed'}",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:3f,width:${P.scale > 4 ? 20 : 8}f,height:${P.scale > 4 ? 12 : 8}f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,${f4(P.lift || 0)}f,0f],left_rotation:[0f,0f,0f,1f],scale:[${f4(P.scale)}f,${f4(P.scale)}f,${f4(P.scale)}f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${itemId(model)}"}}}`;
for (const [kind, P] of Object.entries(PROPS)) {
  // a multi-part prop (the dome) puts each part on its own fixed yaw (entity Rotation) and ignores the execution yaw
  fn(`prop/${kind}`, P.parts
    ? [`# Summons the prop ${kind}: ${P.note}. At the execution position (rotationally symmetric: the execution yaw is not used).`,
      'tag @e[tag=rlk_rd_prop_new] remove rlk_rd_prop_new', ...P.parts.map(q => propSummon(kind, P, q.model, `Rotation:[${f4(((q.yaw % 360) + 360) % 360)}f,0f],`))]
    : [`# Summons the prop ${kind}: ${P.note}. At the execution position, facing the execution yaw.`,
      'tag @e[tag=rlk_rd_prop_new] remove rlk_rd_prop_new', propSummon(kind, P, P.model),
      'execute rotated ~ 0 run tp @e[type=item_display,tag=rlk_rd_prop_new] ~ ~ ~ ~ 0']);
}
fn('prop/clear', ['# Removes every rig prop.', 'kill @e[type=item_display,tag=rlk_rd_prop]']);

// the Tenma puppet's rest outline for the blink silhouettes (build_raiden_movement.py): rig frame, blocks, float included
const tenmaGhost = (() => {
  const o = solve(restPose('t'));
  const P = (n, pt) => { const v = o[n], k = PART_SCALE[n].map(x => x / 16); return add(v.t, rot(v.q, [pt[0] * k[0], pt[1] * k[1], pt[2] * k[2]])).map(x => +x.toFixed(3)); };
  return {note: 'Tenma rest pose (rig frame: +X her left, +Y up, -Z forward, blocks): polylines and thicknesses of the puppet for the blink silhouettes',
    limbs: GHOST.limbs.map(l => ({points: l.pts.map(([n, pt]) => P(n, pt)), thickness: l.th})), disc: {centre: P(GHOST.disc.part, [0, 0, 0]), radius: GHOST.disc.radius}};
})();

// ---- manifest v2 ---------------------------------------------------------------------------------------------------------------
const manifestPath = path.join(here, 'raiden_rig_manifest.json');
const fnFiles = (() => { let n = 0, b = 0; const walk = d => { for (const f of fs.readdirSync(d, {withFileTypes: true})) { const p = path.join(d, f.name); if (f.isDirectory()) walk(p); else { n++; b += fs.statSync(p).size; } } }; walk(rigDir); return {files: n, bytes: b}; })();
json(manifestPath, {
  schema: 2,
  note: 'Raiden rig (rd/plan.md §C). Clip events are played ticks of the clip; the pattern code takes its hit ticks from them.',
  parts: PARTS.map(([n, m, b, g]) => ({name: n, uuid: uuidOf(n), tag: 'rlk_rd_' + n, model: m, brightness: b, group: g, scale: PART_SCALE[n]})),
  looks: {sword: {...LOOK_MODELS.shogun, ...LOOK_MODELS.sword}, polearm: {...LOOK_MODELS.shogun, ...LOOK_MODELS.polearm}, tenma: LOOK_MODELS.tenma},
  states: {shogun: {id: 0, follow: 'shogun', idle: ['idle_sword', 'idle_polearm']}, tenma: {id: 1, follow: 'tenma', idle: 't_idle'}, hidden: {id: 2, follow: 'all', note: 'all parts at scale 0; the next play shows the rig'}},
  clips: clipInfo,
  follow: follow.info(),
  props: Object.fromEntries(Object.entries(PROPS).map(([k, P]) => [k, {...P, item: itemId(P.model), function: `${NS}/prop/${k}`}])),
  objectives: Object.fromEntries(OBJ.map(o => [o, o])),
  functions: {init: `${NS}/init`, spawn: `${NS}/spawn`, tick: `${NS}/tick`, play: `${NS}/play/<clip>`, start: `${NS}/start/<clip>`, state: `${NS}/state/{shogun,tenma,hidden}`,
    look: `${NS}/look/{sword,polearm,tenma}`, flash: `${NS}/flash`, kill: `${NS}/kill`, face: `${NS}/face/{player,track,set}`, prop: `${NS}/prop/<kind>`},
  px: {rig: px.rig, props: px.props, total: px.rig + px.props, sprites: ledger},
  elements: {shogun_sword: shogunEls, shogun_polearm: shogunElsP, tenma: tenmaEls},
  tenma_ghost: tenmaGhost,
  budgets: {parts: [PARTS.length, 34], key_files: keyFiles, rig_files: fnFiles.files, rig_bytes: fnFiles.bytes, models: Object.keys(models).length,
    culling: CULL, view_range: VIEW_RANGE, cull_overhang_ticks: cullWarn.length},
});
for (const w of [...warns].slice(0, 30)) console.warn('warn:', w);
if (cullWarn.length) console.warn(`warn: ${cullWarn.length} part-ticks outside the culling box, e.g. ${cullWarn.slice(0, 4).join('; ')}`);
console.log(`Built the Raiden rig: ${PARTS.length} parts, ${CLIPS.length} clips, ${keyFiles} key files, ${fnFiles.files} rig files (${(fnFiles.bytes / 1e6).toFixed(2)} MB), ` +
  `${Object.keys(models).length} models, ${Object.keys(spriteTable).length} sprites (rig ${(px.rig / 1e6).toFixed(3)} M + props ${(px.props / 1e6).toFixed(3)} M px), ` +
  `elements Shogun ${shogunEls}/${shogunElsP} Tenma ${tenmaEls} [${((Date.now() - t0) / 1000).toFixed(1)} s]`);
if (debugDp) {
  fs.cpSync(rigDir, path.join(debugDp, 'data/rlk/function/boss/raiden/rig'), {recursive: true});
  for (const w of ['s', 't']) putDebug(`rd_dbg/rest_${w}`, [...PART_NAMES.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(REST[w][n])}}`),
    `function ${NS}/look/${w === 't' ? 'tenma_models' : 'shogun_models'}`]);
  for (const look of ['sword', 'polearm']) putDebug(`rd_dbg/weapon_${look}`, lookLines(look));
  putDebug('rd_dbg/spawn', PART_NAMES.map(n => summon(n, 's')));
  // the props on a grid (each at its catalogue scale), for the prop sheet; the dome alone
  const grid = Object.entries(PROPS).filter(([k]) => k !== 'dome');
  putDebug('rd_dbg/props', grid.map(([k, P], i) => { const x = (i % 5) * 4.2 - 8.4, z = Math.floor(i / 5) * 5 - 5, s2 = f4(P.scale);
    return `summon minecraft:item_display ~${f4(x)} ~ ~${f4(z)} {Tags:["rd_prop_${k}"],item_display:"none",brightness:{block:15,sky:15},transformation:{translation:[0f,${f4(P.lift || (['eye_orb', 'seed', 'musou_orb', 'blade_eye'].includes(k) ? 1 : P.model.includes('clap') || k === 'slam_palm' ? 2.4 : 0))}f,0f],left_rotation:[0f,0f,0f,1f],scale:[${s2}f,${s2}f,${s2}f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${itemId(P.model)}"}}}`; }));
  putDebug('rd_dbg/dome', PROPS.dome.parts.map(q => `summon minecraft:item_display ~ ~ ~ {Tags:["rd_prop_dome"],Rotation:[${f4(((q.yaw % 360) + 360) % 360)}f,0f],item_display:"none",brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8f,8f,8f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${itemId(q.model)}"}}}`));
}
