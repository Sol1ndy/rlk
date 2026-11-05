// Display-entity rig of 홍련 (Scarlet, the special boss; S:hr/PLAN.md §2, contract S:hr/contract.md §3.2, frozen table
// tools/mboss_scarlet/api.py §6-§7). An ORIGINAL design (PLAN §1.5, §2.2). Built on the shared RIGLIB (mboss_rig_compile.mjs,
// mboss_rig_clips.mjs, mboss_model_lib.mjs, mboss_shape_lib.mjs, mboss_paint_lib.mjs, mboss_rig_math.mjs, all unchanged).
// API note: tools/scarlet_rig_api.md.
//
// node tools/build_scarlet_rig.mjs --resourcepack <unpacked RP> [--datapack <dp>] [--no-paint] [--allow-steps] [--allow-missing]
//                                  [--debug-dp <scratch dir> [--debug-clips a,b | all] [--debug-step N]]
//
// Writes (owned, rebuilt from scratch on every run)
//   DP  data/rlk/function/boss/scarlet/rig/**
//   RP  assets/rlk/textures/mboss/scarlet/*, assets/rlk/models/item/mboss/scarlet/*, assets/rlk/items/mboss/scarlet/* and the
//       items-atlas entries rlk:mboss/scarlet/* (filter-then-push by id); incl. the ghost texture rlk:mboss/scarlet/ghost
//       and the item / thrown-sword model rlk:mboss/scarlet/item_sword (api.ITEM_MODEL)
//   tools/scarlet_rig_manifest.json (the stub's schema + transforms, models, budgets, sprites; api.check_manifest passes)
// Clips: the 39 owned by S2a from tools/scarlet_clips.mjs; the 8 cinematic clips from S2b's tools/scarlet_cine.mjs when it
// exists (export CLIPS: the eight clip objects in the scarlet_clips format), else scarlet_clips.CINE_PLACEHOLDER.
// The build throws on: a part / blade tip / scabbard tip / brim / hair / skirt below the floor at any compiled tick, a clip /
// event / loop that differs from the contract, a rotation above 120 degrees per tick or per key, the atlas over 0.15 M px,
// more than 6 500 elements at rest, a model outside -16..32 (--allow-steps turns the motion checks into warnings while
// authoring; --allow-missing builds stand-ins for clips not authored yet).
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {PART_NAMES, PART_SCALE, PART_BRIGHT, DEFAULT_MODEL, HAND_MODELS, FACE_MODELS, PHASE_MODELS, BLADE_MODELS, ghostOf, TINTS, allModels,
  ITEM_SWORD} from './scarlet_geometry.mjs';
import {scarletSprites, paintScarlet, spriteId, PAINT_ROLES} from './scarlet_paint.mjs';
import {solve, toDisplay, fromDisplay, setModels, worldPoints, modelOn, HIP_Y} from './scarlet_pose.mjs';
import {CLIPS as AUTHORED, CINE_PLACEHOLDER, accumulate, sampleClip, DEFAULT_POSE, H_POSE} from './scarlet_clips.mjs';
import {createRigCompiler, createRigFollow, nbt, written, interp, shown, summonPart, summonShadow, cullOverhang} from './mboss_rig_compile.mjs';
import {qAngle, len, sub, add, rot} from './mboss_rig_math.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const arg = n => { const i = process.argv.indexOf(n); return i < 0 ? null : process.argv[i + 1]; };
const flag = n => process.argv.includes(n);
const dp = path.resolve(arg('--datapack') || path.join(here, '..'));
const rp = arg('--resourcepack') && path.resolve(arg('--resourcepack'));
if (!rp) throw new Error('--resourcepack <unpacked pack> is required');
const put = (p, s) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, s.endsWith('\n') ? s : s + '\n'); };
const json = (p, o) => put(p, JSON.stringify(o, null, 1));
const t0 = Date.now();
const NS = 'rlk:boss/scarlet/rig';
const rigDir = path.join(dp, 'data/rlk/function/boss/scarlet/rig');
fs.rmSync(rigDir, {recursive: true, force: true});
const fn = (n, lines) => put(path.join(rigDir, n + '.mcfunction'), (Array.isArray(lines) ? lines : [lines]).join('\n'));
const OBJ = 'hrRig';

// ---- contract (api.py itself: api.stub_manifest(), the stub file's generator) -------------------------------------------------
const STUB = JSON.parse(execFileSync('python3', ['-c', 'import json, sys; sys.path.insert(0, "tools"); from mboss_scarlet import api; ' +
  'print(json.dumps(api.stub_manifest(), ensure_ascii=False))'], {cwd: path.join(here, '..'), encoding: 'utf8'}));
if (JSON.stringify(STUB.parts.map(p => p.name)) !== JSON.stringify(PART_NAMES)) throw new Error('parts differ from the contract');
const CONTRACT = STUB.clips;                    // {name: {id, len, loop, events, owner}}
const CLIP_NAMES = Object.keys(CONTRACT).sort((a, b) => CONTRACT[a].id - CONTRACT[b].id);
const LOOKS = STUB.looks;
const ANCHORS = STUB.anchors;

// ---- ids, UUIDs, tags --------------------------------------------------------------------------------------------------------
const UUID_HI = [0x524c4b4d | 0, 0x48524400 | 0, 0x80000000 | 0];
const NN = n => (n === 'shadow' ? STUB.shadow.nn : PART_NAMES.indexOf(n));
const uuidOf = n => STUB.uuid.replace('{:02x}', NN(n).toString(16).padStart(2, '0'));
if (uuidOf('cup') !== STUB.parts[27].uuid || uuidOf('shadow') !== STUB.shadow.uuid) throw new Error('UUID scheme differs from the contract');
const uuidInts = n => [...UUID_HI, NN(n)];
const itemId = m => `rlk:mboss/scarlet/${m}`;
const TAGS = n => ['rlk_room', 'rlk_mb_aux', 'rlk_mb_part', 'rlk_hr_part', 'rlk_hr_' + n];
const SHADOW_TAGS = STUB.shadow.tags;
const CULL = {width: 8, height: 8}, VIEW_RANGE = 2;
const swap = (n, model) => `data modify entity ${uuidOf(n)} item.components."minecraft:item_model" set value "${itemId(model)}"`;

// ---- resource pack: models, items, sprites, atlas ----------------------------------------------------------------------------
const models = allModels();
setModels(models);
const assets = path.join(rp, 'assets/rlk');
const modelDir = path.join(assets, 'models/item/mboss/scarlet'), itemDir = path.join(assets, 'items/mboss/scarlet');
for (const d of [modelDir, itemDir]) fs.rmSync(d, {recursive: true, force: true});
const sprites = scarletSprites();
if (!flag('--no-paint')) paintScarlet(rp, sprites);
// item_sword: the vanilla handheld display transforms (the model lies on the diagonal like a vanilla sword), a gui icon, flat
// on the ground, upright in a frame; display scale 1.5 in an item_display (item_display "none") = the rig's size
const ITEM_DISPLAY = {
  thirdperson_righthand: {rotation: [0, -90, 55], translation: [0, 4, .5], scale: [.62, .62, .62]},
  thirdperson_lefthand: {rotation: [0, 90, -55], translation: [0, 4, .5], scale: [.62, .62, .62]},
  firstperson_righthand: {rotation: [0, -90, 25], translation: [1.13, 3.2, 1.13], scale: [.5, .5, .5]},
  firstperson_lefthand: {rotation: [0, 90, -25], translation: [1.13, 3.2, 1.13], scale: [.5, .5, .5]},
  gui: {rotation: [0, 0, 0], translation: [0, 0, 0], scale: [.9, .9, .9]},
  ground: {rotation: [90, 0, 0], translation: [0, 1.5, 0], scale: [.55, .55, .55]},
  fixed: {rotation: [0, 180, 0], translation: [0, 0, 0], scale: [.9, .9, .9]},
  head: {rotation: [0, 180, 0], translation: [0, 13, 7], scale: [1, 1, 1]},
};
const usedSprites = new Set();
for (const [name, els] of Object.entries(models)) {
  const used = [...new Set(els.flatMap(e => Object.values(e.faces).map(f => f.texture.slice(1))))].sort();
  const tex = {};
  for (const u of used) { if (!sprites[u]) throw new Error(`model ${name}: unknown sprite ${u}`); tex[u] = spriteId(u); usedSprites.add(u); }
  const m = {ambientocclusion: false, textures: {...tex, particle: tex[used[0]] || spriteId('lacquer')}, elements: els};
  if (name === 'item_sword') m.display = ITEM_DISPLAY;
  json(path.join(modelDir, name + '.json'), m);
  const def = {type: 'minecraft:model', model: 'rlk:item/mboss/scarlet/' + name};
  if (TINTS[name] !== undefined) def.tints = [{type: 'minecraft:constant', value: TINTS[name]}];
  json(path.join(itemDir, name + '.json'), {model: def});
}
const unused = Object.keys(sprites).filter(n => !usedSprites.has(n));
if (unused.length) throw new Error(`painted but unused sprites: ${unused.join(', ')}`);
const ledger = {}; let atlasPx = 0;
for (const [n, [w, h]] of Object.entries(sprites)) {
  if (w > 512 || h > 1024 || w % 16 || h % 16) throw new Error(`sprite ${n} ${w}x${h}: sides multiples of 16`);
  ledger[n] = w * h; atlasPx += w * h;
}
const ATLAS_BUDGET = 150000;
if (atlasPx > ATLAS_BUDGET) throw new Error(`atlas ${atlasPx} px > ${ATLAS_BUDGET}`);
// the ghost twins use only the ghost texture
for (const [n, els] of Object.entries(models)) if (n.endsWith('_g') && els.some(e => Object.values(e.faces).some(f => f.texture !== '#ghost'))) throw new Error(`ghost model ${n}: a face not textured ghost`);
// elements shown at rest (every part's default model; normal form); the ghost form has the same geometry
const ecount = m => (models[m] || []).length;
const ELEMENTS = {normal: PART_NAMES.reduce((a, n) => a + ecount(DEFAULT_MODEL[n]), 0)};
ELEMENTS.ghost = PART_NAMES.reduce((a, n) => a + ecount(ghostOf(DEFAULT_MODEL[n])), 0);
const EL_BUDGET = 6500;
for (const [f, n] of Object.entries(ELEMENTS)) if (n > EL_BUDGET) throw new Error(`form ${f}: ${n} elements at rest > ${EL_BUDGET}`);

// ---- clips: contract + authored motion (S2a) + the cinematic clips (S2b's scarlet_cine.mjs, else the placeholder) -----------
const CINE_FILE = path.join(here, 'scarlet_cine.mjs');
const cineMod = fs.existsSync(CINE_FILE) ? await import('./scarlet_cine.mjs') : null;
const CINE = cineMod ? cineMod.CLIPS : CINE_PLACEHOLDER;
const CINE_SOURCE = cineMod ? 'tools/scarlet_cine.mjs' : 'placeholder (scarlet_clips.CINE_PLACEHOLDER)';
const cineNames = Object.keys(CONTRACT).filter(n => CONTRACT[n].owner === 'S2b');
if (JSON.stringify(CINE.map(c => c.name).sort()) !== JSON.stringify([...cineNames].sort())) throw new Error(`cinematic clips ${CINE.map(c => c.name)} != the contract's S2b clips ${cineNames}`);
for (const c of AUTHORED) if (CONTRACT[c.name]?.owner !== 'S2a') throw new Error(`clip ${c.name}: not an S2a clip of the contract`);
const byName = Object.fromEntries([...AUTHORED, ...CINE].map(c => [c.name, c]));
const missing = CLIP_NAMES.filter(n => !byName[n]);
if (missing.length && !flag('--allow-missing')) throw new Error(`clips not authored: ${missing.join(', ')}`);
const CLIPS = CLIP_NAMES.map(n => {
  const k = CONTRACT[n], a = byName[n] || {keys: [[0, {}], [k.len, {}]], note: 'stand-in (not authored)'};
  const keys = a.placeholder ? [[0, a.keys[0][1], 'io'], [k.len, a.keys[0][1], 'io']] : a.keys;
  const c = {...a, keys, name: n, id: k.id, len: k.len, loop: k.loop, events: k.events, owner: k.owner};
  if (c.keys[0][0] !== 0 || c.keys[c.keys.length - 1][0] !== c.len) throw new Error(`clip ${n}: keys must run 0..${c.len} (got ${c.keys[0][0]}..${c.keys[c.keys.length - 1][0]})`);
  c.keys.forEach(([t], i) => { if (i && t <= c.keys[i - 1][0]) throw new Error(`clip ${n}: keys not increasing at ${t}`); });
  if (a.events && JSON.stringify(a.events) !== JSON.stringify(k.events)) throw new Error(`clip ${n}: authored events differ from the contract`);
  return c;
});

// ---- per-clip solve ------------------------------------------------------------------------------------------------------------
// two passes: the floor guards (scabbard, hat, sash, skirt panels) are planned over the whole clip so a guard angle never
// changes faster than GUARD_SLOPE degrees per tick (a dilation of the first pass's angles), then solved again
const GUARD_SLOPE = 22;
const baseOf = c => c.base || DEFAULT_POSE;
function solveClip(c) {
  const run = plan => {
    const ks = accumulate(c, baseOf(c)), out = [];
    const warm = c.loop && c.loop[1] === c.len ? c.len : 0;   // loops settle their secondary motion over one silent cycle
    const hist = k => out[out.length - k]?.o || null;
    for (let i = 0; i <= warm + c.len; i++) {
      const t = i - warm, tt = t < 0 ? t + c.len : t;
      const p = sampleClip(c, tt, ks, baseOf(c));
      const o = solve(p, hist, plan ? plan[tt] : {});
      out.push({o, p, t: tt});
    }
    return out.slice(warm);
  };
  let fr = run(null);
  const names = [...new Set(fr.flatMap(f => Object.keys(f.o._guard)))];
  if (names.some(n => fr.some(f => (f.o._guard[n] || 0) > .5))) {
    const plan = fr.map(() => ({}));
    for (const n of names) {
      const a = fr.map(f => f.o._guard[n] || 0);
      for (let t = 0; t < a.length; t++) { let m = 0; for (let k = 0; k < a.length; k++) m = Math.max(m, a[k] - GUARD_SLOPE * Math.abs(k - t)); plan[t][n] = m; }
    }
    fr = run(plan);
  }
  return fr.map(f => ({o: f.o, p: f.p, d: Object.fromEntries(PART_NAMES.map(n => [n, toDisplay(n, f.o[n])]))}));
}
// ---- compile -----------------------------------------------------------------------------------------------------------------
// tolerances (display space): translation 0.012 b (0.025-0.03 on the long / soft parts), rotation by the part's reach
const TOL = {t: .012, s: .015, rDefault: 1.2,
  r: {sword: .5, sword_glow: .5, scabbard: .6, hilt_sheathed: .6, hat: .8, hat_strings: 2, hair_tail_1: 2, hair_tail_2: 2.5, skirt_fl: 1.5, skirt_fr: 1.5,
    skirt_bl: 1.5, skirt_br: 1.5, sash_tails: 2.5, thigh_l: 1, thigh_r: 1, shin_l: 1, shin_r: 1, arm_l: 1, arm_r: 1, forearm_l: 1, forearm_r: 1},
  tp: {sword: .02, sword_glow: .02, scabbard: .02, hilt_sheathed: .02, hair_tail_1: .025, hair_tail_2: .03, skirt_fl: .025, skirt_fr: .025, skirt_bl: .025, skirt_br: .025, sash_tails: .03}};
const compiler = createRigCompiler({ns: NS, obj: OBJ, fn, parts: PART_NAMES, uuidOf, tol: TOL});
const debugDp = arg('--debug-dp') && path.resolve(arg('--debug-dp'));
const debugClips = (arg('--debug-clips') || 'all').split(',');
const debugStep = +(arg('--debug-step') || 1);
if (debugDp) fs.rmSync(path.join(debugDp, 'data/rlk/function/hr_dbg'), {recursive: true, force: true});
const putDebug = (n, lines) => put(path.join(debugDp, 'data/rlk/function', n + '.mcfunction'), lines.join('\n'));
function segmentsCut(seq, n, cuts, minFirst) {
  const bounds = [...new Set([0, ...cuts.filter(t => t > 0 && t < seq.length - 1), seq.length - 1])].sort((a, b) => a - b), out = [];
  for (let i = 0; i < bounds.length - 1; i++) {
    const a = bounds[i], b = bounds[i + 1];
    let mf = i === 0 ? minFirst : 1;
    if (mf > 1 && shown(seq[a]) && shown(seq[Math.min(b, a + mf)]) && qAngle(seq[a].q, seq[Math.min(b, a + mf)].q) > 110) mf = 1;
    for (const [x, y] of compiler.segments(seq.slice(a, b + 1), n, mf)) out.push([x + a, y + a]);
  }
  return out;
}
// discrete channels the clips key: model swaps through rig/m/<part>/<value> (form-aware), stored states (bookkeeping)
const HAND_PART = {hL: 'forearm_l', hR: 'forearm_r'};
const STATE_STORE = {hat: 'Hat', sword: 'Sw', scab: 'Sc', cup: 'Cu', bottle: 'Bo'};
const STATE_VALUES = {hat: LOOKS.hat, sword: LOOKS.sword, scab: LOOKS.scabbard, cup: STUB.prop_states, bottle: STUB.prop_states};
const fmtA = v => { const r = x => { const s = (Math.round(x * 100) / 100).toString(); return s === '-0' ? '0' : s.replace(/^(-?)0\./, '$1.'); }; return `^${r(v[0])} ^${r(v[1])} ^${r(-v[2])}`; };
const clipInfo = {}, motionErrors = [], floorErrors = [], cullWarn = [];
let keyFiles = 0, keyLines = 0;
const anchorTable = {};
// the points the floor gate names (PLAN §2.1: blade tip, scabbard tip, brim, hair, skirt; every other part by its hull)
const tipOf = (fr, n) => {
  const v = fr.o[n]; if (!v || v.s[0] < 1e-4) return null;
  if (n === 'sword') return add(v.t, rot(v.q, [0, 1.93, 0]));
  if (n === 'scabbard') return add(v.t, rot(v.q, [0, 1.82, 0]));
  return null;
};
for (const c of CLIPS) {
  const F = solveClip(c);
  const cuts = [...(c.cuts || [])];
  const byTick = new Map(), add_ = (t, l) => { if (!byTick.has(t)) byTick.set(t, []); byTick.get(t).push(l); };
  let keys = 0;
  const compiledD = {};
  for (const n of PART_NAMES) {
    const seq = F.map(fr => fr.d[n]);
    let segs = segmentsCut(seq, n, cuts, c.blend ?? 3);
    // a segment whose client interpolation dips below the floor is split at its lowest tick (until none dips)
    const lowAt = (t, v) => { const P = worldPoints(modelOn(n, F[t].p), n, fromDisplay(n, v)); return P.length ? Math.min(...P.map(x => x[1])) : 1; };
    for (let guard = 0; guard < 400; guard++) {
      const W = seq.map(written); let worst = null;
      for (const [a, b] of segs) for (let t = a + 1; t < b; t++) {
        const y = lowAt(t, interp(W[a], W[b], (t - a) / (b - a)));
        if (y < -.005 && (!worst || y < worst.y)) worst = {a, b, t, y};
      }
      if (!worst) break;
      segs = segs.flatMap(([a, b]) => (a === worst.a && b === worst.b ? [[a, worst.t], [worst.t, b]] : [[a, b]]));
    }
    // the keys as shipped {at, dur, to}: a 1-tick segment ending on a cut tick and turning > 60 deg (or showing a hidden part)
    // snaps (a 0-tick key at b; the next segment starts one tick later)
    const snapAt = new Set(cuts), keyList = [];
    let snapped = -1;
    for (const [a, b] of segs) {
      const turn = qAngle(seq[a].q, seq[b].q);
      const pop = !shown(seq[a]) && shown(seq[b]);
      if (b - a === 1 && snapAt.has(b) && (turn > 60 || pop || len(sub(seq[a].t, seq[b].t)) > .25)) { keyList.push({at: b, dur: 0, to: b}); snapped = b; continue; }
      if (turn > 118 && shown(seq[a]) && shown(seq[b])) motionErrors.push(`${c.name} ${n} t${a}-${b}: ${turn.toFixed(0)} degree key (ambiguous slerp)`);
      if (a === snapped) { if (b - a > 1) keyList.push({at: a + 1, dur: b - a - 1, to: b}); }
      else keyList.push({at: a, dur: b - a, to: b});
    }
    // what the client shows each tick (the first key starts from the clip's own tick-0 pose)
    const W = seq.map(written), cv = new Array(seq.length);
    {
      let from = W[0], k0 = 0, d = 0, tgt = W[0];
      const byAt = new Map(keyList.map(k => [k.at, k]));
      for (let t = 0; t < seq.length; t++) {
        const cur = d > 0 && t < k0 + d ? interp(from, tgt, (t - k0) / d) : tgt;
        const k = byAt.get(t);
        if (k) { from = t === 0 ? W[0] : cur; tgt = W[k.to]; k0 = t; d = k.dur; }
        cv[t] = d > 0 && t < k0 + d ? interp(from, tgt, (t - k0) / d) : tgt;
      }
    }
    compiledD[n] = cv;
    for (const k of keyList) { add_(k.at, `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:${k.dur},transformation:${nbt(seq[k.to])}}`); keys++; }
  }
  // per-tick checks on what ships: floor (every shown model point; the blade / scabbard tips), culling, 1-tick turns
  for (let t = 0; t <= c.len; t++) {
    for (const n of PART_NAMES) {
      const v = compiledD[n][t];
      if (!shown(v)) continue;
      const pts = worldPoints(modelOn(n, F[t].p), n, fromDisplay(n, v));
      if (!pts.length) continue;
      const y = Math.min(...pts.map(P => P[1]));
      if (y < -.01) floorErrors.push(`${c.name} t${t} ${n}: lowest point ${y.toFixed(3)} b`);
      const over = Math.max(...pts.map(P => cullOverhang(P, CULL)));
      if (over > 0) cullWarn.push(`${c.name} t${t} ${n} ${over.toFixed(2)} b`);
      if (t && !cuts.includes(t) && shown(compiledD[n][t - 1])) { const a = qAngle(compiledD[n][t - 1].q, v.q); if (a > 120) motionErrors.push(`${c.name} ${n} t${t - 1}->${t}: ${a.toFixed(0)} degrees`); }
    }
    for (const n of ['sword', 'scabbard']) { const P = tipOf(F[t], n); if (P && P[1] < (n === 'sword' ? .0 : 0)) floorErrors.push(`${c.name} t${t} ${n} tip ${P[1].toFixed(3)} b`); }
  }
  // discrete channels: hands and face (model swaps through rig/m/*), the re-parent states (stored), at tick 0 and changes
  F.forEach((fr, t) => {
    const prv = t ? F[t - 1].p : null;
    for (const [ch, part] of Object.entries(HAND_PART)) if (!prv || fr.p[ch] !== prv[ch]) add_(t, `function ${NS}/m/${part}/${fr.p[ch]}`);
    if (!prv || fr.p.face !== prv.face) add_(t, `function ${NS}/m/face/${fr.p.face}`);
    for (const [ch, st] of Object.entries(STATE_STORE)) if (!prv || fr.p[ch] !== prv[ch]) {
      const i = STATE_VALUES[ch].indexOf(fr.p[ch]);
      if (i < 0) throw new Error(`clip ${c.name} t${t}: ${ch} = ${fr.p[ch]} is not a contract value`);
      add_(t, `scoreboard players set @s ${OBJ}${st} ${i}`);
    }
  });
  // tick 0: show a hidden rig
  const head0 = `execute if score @s ${OBJ}S matches 1 run scoreboard players set @s ${OBJ}S 0`;
  byTick.has(0) ? byTick.get(0).unshift(head0) : add_(0, head0);
  for (const [t, L] of Object.entries(c.lines || {})) for (const l of L) add_(+t, l);
  const ticks = [...byTick.keys()].sort((x, y) => x - y);
  for (const t of ticks) fn(`c/${c.name}/k/${t}`, byTick.get(t));
  keyFiles += ticks.length; keyLines += keys;
  // runner: loop (whole clip) / plays a hold span through then holds / holds the last pose
  const lp = c.loop;
  const head = [`# ${c.name}: ${c.len} t${lp ? (lp[1] === c.len ? `, loops ${lp[0]}-${lp[1]}` : ` (hold span ${lp[0]}-${lp[1]})`) : ', holds the last pose'}. @s = rig anchor.`];
  if (lp && lp[1] === c.len) head.push(`execute if score @s ${OBJ}T matches ${c.len}.. run scoreboard players set @s ${OBJ}T ${lp[0]}`);
  else head.push(`execute if score @s ${OBJ}T matches ${c.len + 1}.. run return run scoreboard players set @s ${OBJ}T ${c.len + 1}`);
  const leaf = list => list.map(t => `execute if score @s ${OBJ}T matches ${t} run return run function ${NS}/c/${c.name}/k/${t}`);
  const tree = list => {
    if (list.length <= 8) return leaf(list);
    const g = Math.ceil(list.length / Math.ceil(list.length / 8)), out = [];
    for (let i = 0; i < list.length; i += g) {
      const part = list.slice(i, i + g), name = `c/${c.name}/b/${part[0]}_${part[part.length - 1]}`;
      fn(name, leaf(part));
      out.push(`execute if score @s ${OBJ}T matches ..${part[part.length - 1]} run return run function ${NS}/${name}`);
    }
    if (out.length > 12) {
      const out2 = [], g2 = Math.ceil(out.length / Math.ceil(out.length / 8));
      for (let i = 0; i < out.length; i += g2) {
        const part = out.slice(i, i + g2), last = /matches \.\.(\d+)/.exec(part[part.length - 1])[1], first = /b\/(\d+)_/.exec(part[0])[1];
        const name = `c/${c.name}/b2/${first}_${last}`;
        fn(name, part);
        out2.push(`execute if score @s ${OBJ}T matches ..${last} run return run function ${NS}/${name}`);
      }
      return out2;
    }
    return out;
  };
  fn(`c/${c.name}/run`, [...head, ...tree(ticks)]);
  fn(`play/${c.name}`, [`# Play clip ${c.name} (${c.len} t) from its tick 0 at the next rig/tick (event e lands on the e-th rig/tick after this call). @s = rig anchor.`,
    `scoreboard players set @s ${OBJ}C ${c.id}`, `scoreboard players set @s ${OBJ}T -1`]);
  fn(`start/${c.name}`, [`# Start clip ${c.name} now (tick 0 applied immediately). @s = rig anchor.`, `scoreboard players set @s ${OBJ}C ${c.id}`,
    `scoreboard players set @s ${OBJ}T 0`, `function ${NS}/c/${c.name}/k/0`]);
  anchorTable[c.name] = Object.fromEntries(ANCHORS.map(a => [a, [...F.map(fr => fmtA(fr.o._anchors[a])), fmtA(F[c.len].o._anchors[a])]]));
  clipInfo[c.name] = {id: c.id, len: c.len, loop: lp ? [...lp] : null, events: c.events, owner: c.owner, key_files: ticks.length, keys,
    keys_per_tick: +(keys / (c.len + 1)).toFixed(1), source: c.src || '', note: c.note || '', authored: !!byName[c.name] && !byName[c.name].placeholder};
  if (debugDp && (debugClips.includes('all') || debugClips.includes(c.name))) {
    for (let t = 0; t <= c.len; t += debugStep) {
      const p = F[t].p;
      putDebug(`hr_dbg/${c.name}/${t}`, [...PART_NAMES.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(written(compiledD[n][t]))}}`),
        swap('forearm_l', HAND_MODELS.forearm_l[p.hL]), swap('forearm_r', HAND_MODELS.forearm_r[p.hR]), swap('face', FACE_MODELS[p.face])]);
    }
  }
}
const fail = (title, list) => { if (list.length) { const m = `${title}:\n  ${list.slice(0, +(arg('--show') || 40)).join('\n  ')}${list.length > 40 ? `\n  ... ${list.length} in all` : ''}`; if (flag('--allow-steps')) console.warn(m); else throw new Error(m); } };
fail('floor (no shown element below the feet)', floorErrors);
fail('rotations above 120 degrees per tick or per key', motionErrors);
fail('culling box overhang', cullWarn);
compiler.writeDispatch(CLIPS.map(c => ({id: c.id, name: c.name})));

// ---- follow, init, spawn, tick, kill, uninstall, state, flash, face -----------------------------------------------------------
const follow = createRigFollow({ns: NS, obj: OBJ, fn, uuidOf, lists: {all: PART_NAMES}, fixed: ['shadow'], staticSkip: true,
  comment: '# Parts follow the anchor position and yaw (run as and rotated as the boss at its feet, pitch 0).'});
follow.write();
// stored looks (indices of api.LOOKS / HANDS / PROP_STATES): form, phase, blade, face, the two hands; the re-parent states
// the clips set (hat, sword, scabbard, cup, bottle) are bookkeeping for tests and look_apply
const STORE = {form: 'Form', phase: 'Ph', blade: 'Bl', face: 'Fc', hR: 'HR', hL: 'HL', hat: 'Hat', sword: 'Sw', scabbard: 'Sc', props: 'Pr', cup: 'Cu', bottle: 'Bo'};
const OBJS = [`${OBJ}C`, `${OBJ}T`, `${OBJ}F`, `${OBJ}Y`, `${OBJ}S`, ...Object.values(STORE).map(s => OBJ + s), ...follow.objectives];
const anJson = JSON.stringify(anchorTable), anVer = parseInt(crypto.createHash('sha1').update(anJson).digest('hex').slice(0, 7), 16);
fn('init', ['# Rig objectives (safe on every load). hrRigC clip id, hrRigT clip tick (-1 = queued), hrRigF hit flash, hrRigY face scratch,',
  '# hrRigS state (0 normal, 1 hidden), stored looks hrRigForm / Ph / Bl / Fc / HR / HL / Hat / Sw / Sc / Pr / Cu / Bo (indices of',
  '# api.LOOKS, HANDS, PROP_STATES); hrRigQ* the follow cache. The anchor table (storage rlk:hr rig.an) loads once per version.',
  ...OBJS.map(o => `scoreboard objectives add ${o} dummy`),
  `execute unless data storage rlk:hr rig{anv:${anVer}} run function ${NS}/an/load`]);
// rest transforms: the idle clip's tick 0 for each re-parent state the look functions apply
const idleClip = CLIPS.find(c => c.name === 'idle');
const restOf = over => {
  const c = {...idleClip, keys: [[0, {...idleClip.keys[0][1], ...over}, 'io'], [1, {...idleClip.keys[0][1], ...over}, 'io']], len: 1, loop: null};
  return solveClip(c)[0];
};
const REST = restOf({});
const REST_STATE = {
  hat: Object.fromEntries(LOOKS.hat.map(v => [v, restOf({hat: v, ...(v === 'hand' ? {aR: [80, 40, .9]} : {})})])),
  scabbard: Object.fromEntries(LOOKS.scabbard.map(v => [v, restOf({scab: v, ...(v === 'hand' ? {hR: 'grip', scE: -60} : {})})])),
  sword: Object.fromEntries(LOOKS.sword.map(v => [v, restOf({sword: v})])),
};
const summon = n => summonPart({uuid: uuidInts(n), tags: TAGS(n), item: itemId(DEFAULT_MODEL[n]), brightness: PART_BRIGHT[n], pose: written(REST.d[n]),
  viewRange: VIEW_RANGE, cull: CULL});
const defaults = [['form', 0, 1], ['phase', 0, 1], ['blade', 0, 4], ['face', 0, 2], ['hR', 0, 2], ['hL', 1, 2], ['hat', 0, 4], ['sword', 0, 2], ['scabbard', 1, 2], ['props', 0, 0], ['cup', 0, 2], ['bottle', 0, 2]];
fn('spawn', ['# @s = the boss (the anchor), at its feet. Kills old parts, summons the 29 parts (fixed UUIDs 524c4b4d-4852-4400-8000-0000000000NN) and the',
  '# shadow helper (…40) in the rest pose, re-applies the stored form / phase / blade / face / hands, and queues idle.', `function ${NS}/init`, `function ${NS}/kill`,
  ...defaults.map(([k, d, hi]) => `execute unless score @s ${OBJ}${STORE[k]} matches 0..${hi} run scoreboard players set @s ${OBJ}${STORE[k]} ${d}`),
  `scoreboard players set @s ${OBJ}S 0`, `scoreboard players set @s ${OBJ}F 0`,
  ...PART_NAMES.map(summon), summonShadow({uuid: uuidInts('shadow'), tags: SHADOW_TAGS, item: itemId('empty'), radius: STUB.shadow.radius, strength: .7, viewRange: VIEW_RANGE, cull: CULL}),
  `function ${NS}/look_apply`, `function ${NS}/play/idle`, `execute rotated as @s rotated ~ 0 run function ${NS}/follow_now`]);
fn('spawn_hidden', ['# As spawn, then hidden (every part at scale 0 until the next play / start). @s = the boss, at its feet.', `function ${NS}/spawn`, `function ${NS}/state/hidden`]);
fn('tick', ['# @s = the boss (the anchor), at its feet, once per game tick (the core calls it). Missing parts respawn; hidden: only the',
  '# follow runs until a clip is queued (its tick 0 shows the rig again).',
  `execute unless entity ${uuidOf('pelvis')} run function ${NS}/spawn`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow`,
  `execute if score @s ${OBJ}F matches 1.. run function ${NS}/flash_tick`,
  `execute if score @s ${OBJ}S matches 1 unless score @s ${OBJ}T matches -1 run return 0`,
  `scoreboard players add @s ${OBJ}T 1`, `function ${NS}/run`]);
fn('kill', ['# Removes every rig part, the shadow helper and the anchor marker.', 'kill @e[type=item_display,tag=rlk_hr_part]', 'kill @e[type=marker,tag=rlk_hr_anchor]']);
fn('uninstall', ['# Removes the rig, the anchor marker, the face marker, the rig objectives and the rig storage (rlk:hr rig).', `function ${NS}/kill`,
  'kill @e[type=marker,tag=rlk_hr_face]', ...OBJS.map(o => `scoreboard objectives remove ${o}`), 'data remove storage rlk:hr rig']);
fn('state/hidden', ['# Hidden: every part at scale 0 where it stands (never moved, never below the floor), no clip runs, the parts keep following',
  '# the anchor. The next play/start shows the rig again. @s = the boss.', `scoreboard players set @s ${OBJ}S 1`, `scoreboard players set @s ${OBJ}T 0`,
  ...PART_NAMES.map(n => `data modify entity ${uuidOf(n)} transformation.scale set value [0f,0f,0f]`)]);
fn('state/normal', ['# Visible again. From hidden: the current clip restarts from its tick 0 at the next rig/tick (its keys show every part);',
  '# already visible: nothing changes (pattern cancels call it freely). @s = the boss.',
  `execute if score @s ${OBJ}S matches 1 run scoreboard players set @s ${OBJ}T -1`, `scoreboard players set @s ${OBJ}S 0`]);
const FLASH = PART_NAMES.filter(n => !['sword_glow', 'cup', 'bottle', 'hilt_sheathed'].includes(n));
fn('flash', ['# Hit feedback: the body outlines white-pink for 3 ticks. @s = the boss.', `scoreboard players set @s ${OBJ}F 3`,
  ...FLASH.map(n => `data merge entity ${uuidOf(n)} {Glowing:1b,glow_color_override:16767725}`)]);
fn('flash_tick', ['# Internal: counts the flash down.', `scoreboard players remove @s ${OBJ}F 1`, `execute if score @s ${OBJ}F matches ..0 run function ${NS}/flash_off`]);
fn('flash_off', ['# Internal: end of the hit flash.', `scoreboard players set @s ${OBJ}F 0`, ...FLASH.map(n => `data merge entity ${uuidOf(n)} {Glowing:0b}`)]);
compiler.writeFace({marker: 'rlk_hr_face', maxDeg: 12});

// ---- models by look (form-aware swaps) ----------------------------------------------------------------------------------------
// m/<part>/<value>: the hand / face model of the current form (the clips call these at their own ticks); m/hat, m/sash: the
// phase variant of the current form; m/body: every fixed part of the current form; m/glow: the blade look of the current form
const ghostIf = (n, model) => [`execute if score @s ${OBJ}Form matches 1 run return run ${swap(n, ghostOf(model))}`, swap(n, model)];
for (const [part, map] of Object.entries(HAND_MODELS)) {
  const st = part === 'forearm_r' ? 'HR' : 'HL';
  STUB.hands.forEach((v, i) => fn(`m/${part}/${v}`, [`# The ${part} hand '${v}' (stored ${OBJ}${st} = ${i}) in the current form. @s = the boss.`, `scoreboard players set @s ${OBJ}${st} ${i}`, ...ghostIf(part, map[v])]));
}
LOOKS.face.forEach((v, i) => fn(`m/face/${v}`, [`# The face '${v}' (stored ${OBJ}Fc = ${i}) in the current form. @s = the boss.`, `scoreboard players set @s ${OBJ}Fc ${i}`, ...ghostIf('face', FACE_MODELS[v])]));
for (const [part, nm] of [['hat', 'hat'], ['sash_tails', 'sash']]) {
  fn(`m/${nm}`, [`# Internal: the ${part} model of the stored phase and form.`,
    ...LOOKS.phase.map((ph, i) => `execute if score @s ${OBJ}Ph matches ${i} if score @s ${OBJ}Form matches 1 run ${swap(part, ghostOf(PHASE_MODELS[part][ph]))}`),
    ...LOOKS.phase.map((ph, i) => `execute if score @s ${OBJ}Ph matches ${i} unless score @s ${OBJ}Form matches 1 run ${swap(part, PHASE_MODELS[part][ph])}`)]);
}
const FIXED = PART_NAMES.filter(n => !['forearm_r', 'forearm_l', 'face', 'hat', 'sash_tails', 'sword_glow'].includes(n));
fn('m/body', ['# Internal: every fixed part\'s model in the stored form (normal: its own; ghost: its twin textured rlk:mboss/scarlet/ghost).',
  ...FIXED.map(n => `execute if score @s ${OBJ}Form matches 1 run ${swap(n, ghostOf(DEFAULT_MODEL[n]))}`),
  ...FIXED.map(n => `execute unless score @s ${OBJ}Form matches 1 run ${swap(n, DEFAULT_MODEL[n])}`)]);
fn('m/glow', ['# Internal: the blade glow (sword_glow): lilac in the ghost form, else the stored blade look.',
  `execute if score @s ${OBJ}Form matches 1 run return run ${swap('sword_glow', BLADE_MODELS.lilac)}`,
  ...LOOKS.blade.map((v, i) => `execute if score @s ${OBJ}Bl matches ${i} run ${swap('sword_glow', BLADE_MODELS[v])}`)]);
fn('m/bright', ['# Internal: block brightness: 15 for every part in the ghost form; else 13 (sword_glow 15, sash_tails 14 in phase p2).',
  ...PART_NAMES.map(n => `execute if score @s ${OBJ}Form matches 1 run data merge entity ${uuidOf(n)} {brightness:{block:15,sky:15}}`),
  ...PART_NAMES.filter(n => n !== 'sash_tails').map(n => `execute unless score @s ${OBJ}Form matches 1 run data merge entity ${uuidOf(n)} {brightness:{block:${PART_BRIGHT[n]},sky:15}}`),
  `execute unless score @s ${OBJ}Form matches 1 if score @s ${OBJ}Ph matches 1 run data merge entity ${uuidOf('sash_tails')} {brightness:{block:14,sky:15}}`,
  `execute unless score @s ${OBJ}Form matches 1 unless score @s ${OBJ}Ph matches 1 run data merge entity ${uuidOf('sash_tails')} {brightness:{block:13,sky:15}}`]);
fn('m/hands', ['# Internal: both hands and the face in the stored form.',
  ...STUB.hands.map((v, i) => `execute if score @s ${OBJ}HR matches ${i} run function ${NS}/m/forearm_r/${v}`),
  ...STUB.hands.map((v, i) => `execute if score @s ${OBJ}HL matches ${i} run function ${NS}/m/forearm_l/${v}`),
  ...LOOKS.face.map((v, i) => `execute if score @s ${OBJ}Fc matches ${i} run function ${NS}/m/face/${v}`)]);
fn('m/all', ['# Internal: every part\'s model and brightness from the stored form, phase, blade, face and hands.',
  `function ${NS}/m/body`, `function ${NS}/m/hands`, `function ${NS}/m/hat`, `function ${NS}/m/sash`, `function ${NS}/m/glow`, `function ${NS}/m/bright`]);
// ---- looks (rig/look/<channel>/<value>) ---------------------------------------------------------------------------------------
const tf = (n, v) => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:2,transformation:${nbt(written(v))}}`;
LOOKS.form.forEach((v, i) => fn(`look/form/${v}`, [`# Form ${v}${v === 'ghost' ? ': every part its ghost twin (one flat glowing lilac, rlk:mboss/scarlet/ghost), brightness 15, sword_glow lilac' : ': every part its own model, brightness 13 (sword_glow 15, sash_tails 14 in p2), the stored blade look'}. @s = the boss.`,
  `scoreboard players set @s ${OBJ}Form ${i}`, `function ${NS}/m/all`]));
LOOKS.phase.forEach((v, i) => fn(`look/phase/${v}`, [`# Phase ${v}: the hat knot and the sash tails' edge ${v === 'p2' ? 'glow crimson' : 'as painted'} (models in the current form). @s = the boss.`,
  `scoreboard players set @s ${OBJ}Ph ${i}`, `function ${NS}/m/hat`, `function ${NS}/m/sash`, `function ${NS}/m/bright`]));
LOOKS.blade.forEach((v, i) => fn(`look/blade/${v}`, [`# Blade look ${v} (stored ${OBJ}Bl = ${i}): the glow overlay on the blade${v === 'off' ? ' hidden' : ''} (the ghost form keeps lilac until form normal). @s = the boss.`,
  `scoreboard players set @s ${OBJ}Bl ${i}`, `function ${NS}/m/glow`]));
LOOKS.face.forEach((v, i) => fn(`look/face/${v}`, [`# Face ${v} (stored ${OBJ}Fc = ${i}; clips key their own faces). @s = the boss.`, `function ${NS}/m/face/${v}`]));
LOOKS.hat.forEach((v, i) => fn(`look/hat/${v}`, [`# Hat ${v} (stored ${OBJ}Hat = ${i}): the rest-pose transform of that state until the running clip keys the hat again (clips key their`,
  '# own hat states; PLAN §2.4). @s = the boss.', `scoreboard players set @s ${OBJ}Hat ${i}`,
  ...['hat', 'hat_strings'].map(n => tf(n, REST_STATE.hat[v].d[n]))]));
LOOKS.sword.forEach((v, i) => fn(`look/sword/${v}`, [`# Sword ${v} (stored ${OBJ}Sw = ${i}): ${v === 'hand' ? 'the drawn sword shown' : v === 'sheathed' ? 'the blade hidden, the hilt seated at the scabbard\'s mouth' : 'sword and hilt hidden'} (rest-pose transforms until the clip keys them). @s = the boss.`,
  `scoreboard players set @s ${OBJ}Sw ${i}`, ...['sword', 'sword_glow', 'hilt_sheathed'].map(n => tf(n, REST_STATE.sword[v].d[n]))]));
LOOKS.scabbard.forEach((v, i) => fn(`look/scabbard/${v}`, [`# Scabbard ${v} (stored ${OBJ}Sc = ${i})${v === 'gone' ? ': the scabbard and the sheathed hilt hidden (§7\'s sword toss)' : ''} (rest-pose transforms until the clip keys them). @s = the boss.`,
  `scoreboard players set @s ${OBJ}Sc ${i}`, ...['scabbard', 'hilt_sheathed'].map(n => tf(n, REST_STATE.scabbard[v].d[n]))]));
fn('look/props/none', ['# Props none: the intro cup and bottle hidden (the intro clip keys them). @s = the boss.', `scoreboard players set @s ${OBJ}Pr 0`,
  `scoreboard players set @s ${OBJ}Cu 0`, `scoreboard players set @s ${OBJ}Bo 0`,
  ...['cup', 'bottle'].map(n => `data modify entity ${uuidOf(n)} transformation.scale set value [0f,0f,0f]`)]);
fn('look_apply', ['# Re-applies every stored model look (spawn): form, phase, blade, face, hands. @s = the boss.', `function ${NS}/m/all`]);

// ---- anchors: rig/anchor/<name> moves the one rlk_hr_anchor marker to that point of the current clip tick ----------------------
fn('an/load', ['# Internal (init, once per table version): the anchor table rlk:hr rig.an[<clip id>].<anchor>[<tick 0..len+1>] = "^left ^up ^forward".',
  'data modify storage rlk:hr rig.an set value []',
  ...CLIPS.flatMap(c => ['data modify storage rlk:hr rig.an append value {}',
    ...ANCHORS.map(a => `data modify storage rlk:hr rig.an[${c.id}].${a} set value ${JSON.stringify(anchorTable[c.name][a])}`)]),
  `data modify storage rlk:hr rig.anv set value ${anVer}`]);
for (const a of ANCHORS) fn(`anchor/${a}`, [`# Moves the rlk_hr_anchor marker to ${a} of the current clip tick (yaw = the boss's). Effects run at / as it. @s = the boss, at its feet.`,
  `execute unless entity @e[type=marker,tag=rlk_hr_anchor,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_anchor"]}`,
  `execute store result storage rlk:hr rig.q.c int 1 run scoreboard players get @s ${OBJ}C`,
  `execute store result storage rlk:hr rig.q.t int 1 run scoreboard players get @s ${OBJ}T`,
  `execute if score @s ${OBJ}T matches ..-1 run data modify storage rlk:hr rig.q.t set value 0`,
  `data modify storage rlk:hr rig.q.a set value "${a}"`,
  `function ${NS}/anchor/r/get with storage rlk:hr rig.q`]);
fn('anchor/r/get', ['# Internal: the anchor string of clip $(c) tick $(t) (the held last pose past the end).', '$data modify storage rlk:hr rig.q.p set from storage rlk:hr rig.an[$(c)].$(a)[$(t)]',
  `execute unless data storage rlk:hr rig.q.p run data modify storage rlk:hr rig.q.p set value "^ ^1.8 ^"`,
  `function ${NS}/anchor/r/go with storage rlk:hr rig.q`, 'data remove storage rlk:hr rig.q.p']);
fn('anchor/r/go', ['# Internal: the marker to the point (local to the boss, yaw only).', '$execute rotated as @s rotated ~ 0 run tp @e[type=marker,tag=rlk_hr_anchor,limit=1] $(p) ~ 0']);

// ---- manifest ---------------------------------------------------------------------------------------------------------------------
const fnFiles = (() => { let n = 0, b = 0; const walk = d => { for (const f of fs.readdirSync(d, {withFileTypes: true})) { const p = path.join(d, f.name); if (f.isDirectory()) walk(p); else { n++; b += fs.statSync(p).size; } } }; walk(rigDir); return {files: n, bytes: b}; })();
const manifest = {
  schema: 1, id: 'scarlet', source: 'rig',
  _doc: 'Scarlet rig (tools/build_scarlet_rig.mjs, API tools/scarlet_rig_api.md): the D0 stub schema (parts, re-parent table, shadow, clips with id / len / loop / events / owner, looks, hands, prop states, anchors, calls) plus transforms, models, budgets and sprites. Generated: do not edit.',
  height: STUB.height, hat_top: STUB.hat_top, brim_d: STUB.brim_d, hip_y: HIP_Y, uuid: STUB.uuid,
  parts: STUB.parts.map(p => ({...p, model: DEFAULT_MODEL[p.name], ghost_model: ghostOf(DEFAULT_MODEL[p.name]), brightness: PART_BRIGHT[p.name], scale: PART_SCALE[p.name],
    tags: TAGS(p.name), rest: written(REST.d[p.name])})),
  reparent: STUB.reparent, shadow: {...STUB.shadow, model: itemId('empty')},
  clips: Object.fromEntries(CLIP_NAMES.map(n => [n, clipInfo[n]])), cine_source: CINE_SOURCE,
  looks: LOOKS, hands: STUB.hands, prop_states: STUB.prop_states, anchors: ANCHORS, calls: STUB.calls, macro_calls: STUB.macro_calls,
  look_models: {hands: HAND_MODELS, face: FACE_MODELS, phase: PHASE_MODELS, blade: BLADE_MODELS, ghost: 'every model <m> has the twin <m>_g (texture rlk:mboss/scarlet/ghost)'},
  stored_looks: Object.fromEntries(Object.entries(STORE).map(([k, v]) => [k, OBJ + v])),
  tags: {part: 'rlk_hr_part', anchor: 'rlk_hr_anchor', per_part: 'rlk_hr_<part>', all: ['rlk_room', 'rlk_mb_aux', 'rlk_mb_part', 'rlk_hr_part'], face_marker: 'rlk_hr_face'},
  objectives: OBJS, culling: CULL, view_range: VIEW_RANGE, storage: {anchors: 'rlk:hr rig.an', version: anVer},
  ghost_texture: itemId('ghost'), item_sword: {model: itemId('item_sword'), length: ITEM_SWORD.len, display_scale: 1.5, display: ITEM_DISPLAY},
  paint_roles: PAINT_ROLES,
  budgets: {atlas_px: atlasPx, atlas_budget: ATLAS_BUDGET, sprites: Object.keys(sprites).length, elements_at_rest: ELEMENTS, elements_budget: EL_BUDGET,
    parts: PART_NAMES.length, models: Object.keys(models).length, key_files: keyFiles, keys: keyLines, rig_functions: fnFiles.files, rig_bytes: fnFiles.bytes,
    cull_overhang_ticks: cullWarn.length},
  sprites: ledger,
};
json(path.join(here, 'scarlet_rig_manifest.json'), manifest);
console.log(`Built the Scarlet rig: ${PART_NAMES.length} parts, ${CLIPS.length} clips (${missing.length} stand-ins; cine: ${CINE_SOURCE}), ${keyFiles} key files, ${keyLines} keys, ` +
  `${fnFiles.files} rig functions (${(fnFiles.bytes / 1e6).toFixed(2)} MB), ${Object.keys(models).length} models, ${Object.keys(sprites).length} sprites ${(atlasPx / 1e6).toFixed(3)} M px, ` +
  `elements at rest ${ELEMENTS.normal} / ghost ${ELEMENTS.ghost} [${((Date.now() - t0) / 1000).toFixed(1)} s]`);
if (debugDp) {
  fs.rmSync(path.join(debugDp, 'data/rlk/function/boss/scarlet/rig'), {recursive: true, force: true});
  fs.cpSync(rigDir, path.join(debugDp, 'data/rlk/function/boss/scarlet/rig'), {recursive: true});
  if (!fs.existsSync(path.join(debugDp, 'pack.mcmeta'))) fs.copyFileSync(path.join(dp, 'pack.mcmeta'), path.join(debugDp, 'pack.mcmeta'));
  putDebug('hr_dbg/rest', PART_NAMES.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(written(REST.d[n]))}}`));
  putDebug('hr_dbg/player', ['summon minecraft:item_display ~1.4 ~ ~ {Tags:["hr_dbg_player"],item_display:"none",transformation:{translation:[0f,0.9f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,1.8f,0.3f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"minecraft:light_blue_concrete"}}}']);
}
void H_POSE;
