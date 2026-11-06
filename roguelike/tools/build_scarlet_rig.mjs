// Display-entity rig of 홍련 (Scarlet, the special boss; S:hr/PLAN.md §2, contract S:hr/contract.md §3.2, frozen table
// tools/mboss_scarlet/api.py §6-§7). S2c (11-05): the body wears the user's own Minecraft skin (tools/scarlet_skin.mjs, the
// user's request "마인크래프트 스킨을 이용해서 만들라고. 아를이나 라이덴처럼"). S2d (11-05, "팔다리가 너무 기괴하게 긴데 그냥
// 플레이어 크기랑 똑같게해"): her body is the player avatar's (scarlet_geometry.mjs: the avatar's boxes and skin faces, its slim
// arms, display scale 1; scarlet_pose.mjs: the avatar's skeleton, head top 2.00 b) and every clip is retargeted per sample
// (scarlet_retarget.mjs: angles kept, translations scaled, contacts kept: feet, knees, hands, the lying back, the seat). The
// hat, the strings, the sash tails, the sword, the scabbard, the cup and the bottle stay S2a's own shapes in S2c's colours,
// resized to the new body. Built on the shared RIGLIB (mboss_rig_compile.mjs, mboss_rig_clips.mjs, mboss_model_lib.mjs,
// mboss_shape_lib.mjs, mboss_paint_lib.mjs, mboss_rig_math.mjs, all unchanged). API note: tools/scarlet_rig_api.md.
//
// node tools/build_scarlet_rig.mjs --resourcepack <unpacked RP> [--datapack <dp>] [--no-paint] [--allow-steps] [--allow-missing]
//                                  [--debug-dp <scratch dir> [--debug-clips a,b | all] [--debug-step N]]
//
// Writes (owned, rebuilt from scratch on every run)
//   DP  data/rlk/function/boss/scarlet/rig/**
//   RP  assets/rlk/textures/mboss/scarlet/*, assets/rlk/models/item/mboss/scarlet/*, assets/rlk/items/mboss/scarlet/* and the
//       items-atlas entries rlk:mboss/scarlet/* (filter-then-push by id); incl. the user's skin rlk:mboss/scarlet/skin (the
//       embedded PNG bytes, unchanged), the ghost texture rlk:mboss/scarlet/ghost and the item / thrown-sword model
//       rlk:mboss/scarlet/item_sword (api.ITEM_MODEL)
//   tools/scarlet_rig_manifest.json (the stub's schema + transforms, models, budgets, sprites; api.check_manifest passes)
// Clips: the 39 owned by S2a from tools/scarlet_clips.mjs; the 8 cinematic clips from S2b's tools/scarlet_cine.mjs when it
// exists (export CLIPS: the eight clip objects in the scarlet_clips format), else scarlet_clips.CINE_PLACEHOLDER.
// The build throws on: a part / blade tip / scabbard tip / brim below the floor at any compiled tick, a clip / event / loop
// that differs from the contract, a rotation above 120 degrees per tick or per key, the blade inside her body at a clip event,
// a correction guard planned at its bound, a contract dimension (api HEIGHT / HAT_TOP / BRIM_D / SWORD_LEN / SCABBARD_LEN /
// ITEM_SWORD_LEN / ITEM_SWORD_SCALE, the registry hit box) that differs from the built rig, the atlas over 0.15 M px, more than
// 6 500 elements at rest, a model outside -16..32, a damaged embedded skin (--allow-steps turns the motion checks into warnings
// while authoring; --allow-missing builds stand-ins for clips not authored yet).
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {PART_NAMES, PART_SCALE, PART_BRIGHT, DEFAULT_MODEL, HAND_MODELS, FACE_MODELS, PHASE_MODELS, BLADE_MODELS, ghostOf, TINTS, allModels,
  ITEM_SWORD, ICON, HIDDEN, SKIN, SKIN_REGIONS, SKIN_MAP, FACE_FX, SWORD, SCAB, HAT, STRINGS, SASH, CUP, BOTTLE, MODEL_SCALE, BODY_SPECS, stringPoints} from './scarlet_geometry.mjs';
const SWORD_BLADE = [SWORD.bladeLo, SWORD.tip];
import {scarletSprites, paintScarlet, spriteId, PAINT_ROLES, TEX_DIR} from './scarlet_paint.mjs';
import {SKIN_B64, SKIN_BYTES, SKIN_SHA1} from './scarlet_skin.mjs';
import {solve, toDisplay, fromDisplay, setModels, worldPoints, modelOn, boxDepth, HIP_Y, SK, GUARD_BOUND, GUARD_SLOPE, CORE, minY, hullOf, freeBlade, dirBE, bladeQ, HAT_FLOOR_HOLD,
  BOX, ARM_REACH} from './scarlet_pose.mjs';
import {retarget, overlay, refCore, hatSwitches, bladeChannels, setHatFace, faceSpot, PATCHES, HAT_REST, HAT_FLIGHTS, SUPPORTS, S_LEG, S_ARM, S_SCAB, K_ARC,
  IAI_DELTA, ASIDE, hipDirChannels} from './scarlet_retarget.mjs';
import {CLIPS as AUTHORED, CINE_PLACEHOLDER, accumulate, sampleClip, DEFAULT_POSE, H_POSE} from './scarlet_clips.mjs';
import {createRigCompiler, createRigFollow, nbt, written, interp, shown, summonPart, summonShadow, cullOverhang} from './mboss_rig_compile.mjs';
import {qAngle, len, sub, add, rot, mul, q, times, unit, cross, dot, perp, basisQ} from './mboss_rig_math.mjs';

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
  'm = api.stub_manifest(); m["_api"] = {k: getattr(api, k, None) for k in ("HEIGHT", "HAT_TOP", "BRIM_D", "SWORD_LEN", "SCABBARD_LEN", "SHADOW_R", ' +
  '"ITEM_SWORD_LEN", "ITEM_SWORD_SCALE")}; m["_api"]["BOSS"] = {"scale": api.BOSS["scale"], "hit": api.BOSS["hit"]}; ' +
  'print(json.dumps(m, ensure_ascii=False))'], {cwd: path.join(here, '..'), encoding: 'utf8'}));
const API = STUB._api; delete STUB._api;
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
// the user's skin: the embedded bytes unchanged (paintSpriteSet drops it with the stale files; written again here) and its
// items-atlas entry (filter-then-push by id: removed with the stale ids above, pushed back at the end)
const SKIN_ID = spriteId('skin');
{
  const bytes = Buffer.from(SKIN_B64, 'base64');
  if (bytes.length !== SKIN_BYTES || crypto.createHash('sha1').update(bytes).digest('hex') !== SKIN_SHA1) throw new Error('scarlet_skin.mjs: the embedded skin is damaged');
  if (bytes.readUInt32BE(16) !== 64 || bytes.readUInt32BE(20) !== 64) throw new Error('scarlet_skin.mjs: the skin is not 64 x 64');
  fs.mkdirSync(path.join(rp, TEX_DIR), {recursive: true});
  fs.writeFileSync(path.join(rp, TEX_DIR, 'skin.png'), bytes);
  const atlasPath = path.join(rp, 'assets/minecraft/atlases/items.json');
  const atlas = JSON.parse(fs.readFileSync(atlasPath, 'utf8'));
  atlas.sources = atlas.sources.filter(s => (s.sprite || s.resource) !== SKIN_ID);
  atlas.sources.push({type: 'minecraft:single', resource: SKIN_ID});
  fs.writeFileSync(atlasPath, JSON.stringify(atlas, null, 2) + '\n');
}
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
// F-I (HR-03): the slot icon item_sword_icon (scarlet_geometry ICON, drawn in GUI px) and the contexts that show it instead of
// the rig model: the inventory / hotbar / codex screens (gui), an item frame (fixed) and the dropped item (ground) - the
// vanilla generated item's transforms (gui as drawn, upright in a frame, half size and bobbing on the ground); the hands and
// the coda's thrown prop (item_display "none") keep item_sword
const ICON_CONTEXTS = ['gui', 'fixed', 'ground'];
const ICON_DISPLAY = {
  gui: {rotation: [0, 0, 0], translation: [0, 0, 0], scale: [1, 1, 1]},
  fixed: {rotation: [0, 180, 0], translation: [0, 0, 0], scale: [1, 1, 1]},
  ground: {rotation: [0, 0, 0], translation: [0, 2, 0], scale: [.5, .5, .5]},
};
const usedSprites = new Set();
for (const [name, els] of Object.entries(models)) {
  const used = [...new Set(els.flatMap(e => Object.values(e.faces).map(f => f.texture.slice(1))))].sort();
  const tex = {};
  for (const u of used) { if (u !== 'skin' && !sprites[u]) throw new Error(`model ${name}: unknown sprite ${u}`); tex[u] = spriteId(u); usedSprites.add(u); }
  // a model with no faces (empty, the calm face and its twin) takes the particle of its kind (the ghost twin the ghost texture)
  const m = {ambientocclusion: false, textures: {...tex, particle: tex[used[0]] || spriteId(name.endsWith('_g') ? 'ghost' : 'lacquer')}, elements: els};
  if (name === 'item_sword') m.display = ITEM_DISPLAY;
  if (name === 'item_sword_icon') { m.display = ICON_DISPLAY; m.gui_light = 'front'; }     // lit flat in the slot like a vanilla item
  json(path.join(modelDir, name + '.json'), m);
  let def = {type: 'minecraft:model', model: 'rlk:item/mboss/scarlet/' + name};
  if (TINTS[name] !== undefined) def.tints = [{type: 'minecraft:constant', value: TINTS[name]}];
  if (name === 'item_sword') def = {type: 'minecraft:select', property: 'minecraft:display_context',
    cases: [{when: ICON_CONTEXTS, model: {type: 'minecraft:model', model: 'rlk:item/mboss/scarlet/item_sword_icon'}}], fallback: def};
  json(path.join(itemDir, name + '.json'), {model: def});
}
const unused = [...Object.keys(sprites), 'skin'].filter(n => !usedSprites.has(n));
if (unused.length) throw new Error(`painted but unused sprites: ${unused.join(', ')}`);
const ledger = {skin: 64 * 64}; let atlasPx = 64 * 64;
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

// ---- per-clip solve (S2d: sample -> refCore (S2a's contact truth) -> retarget -> overlay -> solve) ---------------------------------
// The correction guards (scarlet_pose.mjs GUARD_BOUND: the floor guards of the scabbard / hat / strings / sash, the planted-feet
// drop, the hip scabbard's closeY, the lying incline / chin tip / rock, the reach assists, the blade push / turn, the prop
// closure, the back hat's head clearance) are planned over the whole clip so no value changes faster than its GUARD_SLOPE per
// tick (a dilation of the measured values, circular for loops; the vector guards keep the direction of the tick that set the
// maximum); pass 2 applies the plan; a guard that needed more than planned re-plans from both passes (pass 3).
const baseOf = c => c.base || DEFAULT_POSE;
const gv = v => (v == null ? 0 : typeof v === 'number' ? v : v.v);
function planOf(passes, c) {
  const N = passes[0].length, loop = c.loop && c.loop[1] === c.len, period = c.len;
  const dist = (a, b) => { const d = Math.abs(a - b); return loop ? Math.min(d, period - d) : d; };
  const names = new Set(passes.flatMap(fr => fr.flatMap(f => Object.keys(f.o._guard))));
  const plan = Array.from({length: N}, () => ({}));
  for (const n of names) {
    const slope = GUARD_SLOPE[n.replace(/[+-]$/, '')] ?? 22;
    const vals = Array.from({length: N}, (_, t) => { let best = null; for (const fr of passes) { const v = fr[t].o._guard[n]; if (v != null && (!best || gv(v) > gv(best))) best = v; } return best; });
    const a = vals.map(gv);
    if (!a.some(x => x > 1e-6)) continue;
    for (let t = 0; t < N; t++) {
      let m = 0, arg = -1;
      for (let k = 0; k < N; k++) { const v = a[k] - slope * dist(k, t); if (v > m + 1e-12) { m = v; arg = k; } }
      if (m > 1e-6) plan[t][n] = typeof vals[arg] === 'object' ? {v: m, dir: vals[arg].dir} : m;
    }
  }
  return plan;
}
// SH0': the sheathe entry's free blade on the new scabbard axis (probe: ending 304, the hand-held scabbard, sh at 304)
let SH0P = null, HAT_FACE = null;
const FLIGHT_SRC = {};
function solveClip(c) {
  const base = baseOf(c), ks = accumulate(c, base);
  const switches = hatSwitches(ks), cuts = c.cuts || [], loop = c.loop && c.loop[1] === c.len;
  const flight = HAT_FLIGHTS[c.name];
  const flightSrc = flight ? {A: sampleClip(c, flight.t0, ks, base).hwP, B: sampleClip(c, flight.t1, ks, base).hwP} : null;
  const run = (plan, pass, fctx) => {
    const out = [];
    const warm = loop ? c.len : 0;   // loops settle their secondary motion over one silent cycle
    const hist = k => out[out.length - k]?.o || null;
    let refPrev = {};
    for (let i = 0; i <= warm + c.len; i++) {
      const t = i - warm, tt = t < 0 ? t + c.len : t;
      const p = sampleClip(c, tt, ks, base);
      const ref = refCore(p, refPrev); refPrev = ref.prev;
      const qq = overlay(retarget(p, c.name, tt), c.name, tt, {sh0: c.name === 'ending' ? SH0P : null, hatSwitches: switches, cuts, flight: fctx, flightSrc});
      const o = solve(qq, hist, plan ? plan[tt] : {}, {pass, clip: c.name, t: tt, ref});
      out.push({o, p, q: qq, t: tt, ref});
    }
    return out.slice(warm);
  };
  const flightCtx = fr => {
    if (!flight) return null;
    const f = flight;
    const A = f.from.state ? fr[f.from.t].o.hat : HAT_REST[f.from.spot];
    const B = f.to.state ? fr[f.to.t].o.hat : HAT_REST[f.to.spot];
    return {A: A.t, Aq: A.q || null, B: B.t, Bq: B.q || null};
  };
  const p1 = run(null, 1, null);
  let fr = p1, plan = null, passes = 1;
  const big = f => Object.values(f.o._guard).some(v => gv(v) > .5);
  if (flight || p1.some(big)) {
    const fctx = flightCtx(p1);
    plan = planOf([p1], c);
    let p2 = run(plan, 2, fctx); passes = 2;
    const over = p2.some((f, t) => Object.entries(f.o._guard).some(([n, v]) => gv(v) > gv(plan[t][n]) + .5));
    if (over) { plan = planOf([p1, p2], c); p2 = run(plan, 3, fctx); passes = 3; }
    fr = p2;
  }
  return fr.map(f => ({o: f.o, p: f.p, q: f.q, ref: f.ref, passes, d: Object.fromEntries(PART_NAMES.map(n => [n, toDisplay(n, f.o[n])]))}));
}
// the probes the clips need before they are solved: the world hat's face spot (LY = ending 0: the hat over her face, parallel to it,
// 0.012 off the face layer) and SH0' (ending 304)
function probe(name, t) {
  const c = CLIPS.find(x => x.name === name), base = baseOf(c), ks = accumulate(c, base);
  const p = sampleClip(c, t, ks, base);
  const qq = overlay(retarget(p, name, t), name, t, {});
  return {p, q: qq, o: solve(qq, () => null, {}, {pass: 1, clip: name, t, ref: refCore(p, {})})};
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
// big swings keyed every tick (PLAN §2.5): the runs of >= 4 consecutive authored key ticks (the swings, spins, draws and flips
// the clips author tick by tick); every part that moves there keys at each of those ticks (S2c: the hidden skirt / lock parts
// no longer key, so the moving parts' own keys carry the run)
function denseTicks(c) {
  const ts = c.keys.map(k => k[0]), out = new Set();
  let s = 0;
  for (let i = 1; i <= ts.length; i++) {
    if (i < ts.length && ts[i] === ts[i - 1] + 1) continue;
    if (ts[i - 1] - ts[s] >= 3) for (let k = ts[s]; k <= ts[i - 1]; k++) out.add(k);
    s = i;
  }
  return out;
}
// no blade through her body at the clip events (S2c): the base boxes of the skin parts (part frame, blocks) the blade samples
// (guard -> tip) must stay out of, 1 cm in from every face; the hands (forearms) hold the hilt and the scabbard by design
const BODY_BOX_PARTS = ['torso', 'pelvis', 'head', 'arm_l', 'arm_r', 'thigh_l', 'thigh_r', 'shin_l', 'shin_r'];
// S2d: the right forearm too where the right hand is free (not on the scabbard, the throat, the grip or the hat)
const freeRight = q => (q.scab || 'hip') !== 'hand' && (q.hsR || 0) < .5 && (q.rh || 0) < .5 && (q.hat || 'worn') !== 'hand';
const BODY_BOX = Object.fromEntries([...BODY_BOX_PARTS, 'forearm_r'].map(n => {
  const e = models[DEFAULT_MODEL[n]][0], X = [(8 - e.from[0]) / 16, (8 - e.to[0]) / 16], Z = [(e.from[2] - 8) / 16, (e.to[2] - 8) / 16];
  return [n, [[Math.min(...X), (e.from[1] - 8) / 16, Math.min(...Z)], [Math.max(...X), (e.to[1] - 8) / 16, Math.max(...Z)]]];
}));
const conjQ = Q => [-Q[0], -Q[1], -Q[2], Q[3]];
// S2d round 3 (C3-1): what ships on a tick is near the solved frame: within TOL x 1.25 (the margin covers the 5-decimal rounding
// of the written keys, which leaves |q| a little off 1 so qAngle of such a quaternion with itself reads up to ~0.5 deg, and the
// boundary of the compiler's own fit); the quaternions are compared normalized
const unitQ = v => { const m = Math.hypot(...v.q); return {...v, q: v.q.map(x => x / m)}; };
const nearSolved = (x, y, n) => {
  const big = Math.max(...y.s.map(Math.abs), ...x.s.map(Math.abs));
  if (big < 1e-4) return true;
  return len(sub(x.t, y.t)) <= 1.25 * (TOL.tp[n] ?? TOL.t) && Math.max(...x.s.map((v, i) => Math.abs(v - y.s[i]))) <= 1.25 * TOL.s * Math.max(1, big) &&
    qAngle(unitQ(x).q, unitQ(y).q) <= 1.25 * (TOL.r[n] ?? TOL.rDefault);
};
// the parts riding a body part (S2d round 2): keyed with it where the event check re-keys it
const RIDERS = {head: ['face', 'hat', 'hat_strings']};
const bladeErrors = [], wornErrors = [], tolErrors = [];
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
  if (n === 'sword') return add(v.t, rot(v.q, [0, SWORD.tip, 0]));
  if (n === 'scabbard') return add(v.t, rot(v.q, [0, SCAB.L, 0]));
  return null;
};
// ---- the probes (S2d): the world hat's face spot (LY), SH0' (the sheathe entry) -------------------------------------------------
{
  setHatFace({t: [0, .45, .5]});                         // provisional (the probe of ending 0 maps the face spot)
  // the hat parallel to the face, 0.012 off the face layer, its front toward the top of her head, the chest-side rim tilted up
  // over her forearms (scarlet_retarget.mjs faceSpot)
  const fs = faceSpot(t => probe('ending', t));
  HAT_FACE = {tilt: fs.tilt, lift: fs.lift};
  setHatFace({t: fs.t, q: fs.q});
}
{
  const {q: q304, o} = probe('ending', 304);
  const ax = rot(o.scabbard.q, [0, 1, 0]), Ryaw = q([0, q304.rot[1], 0]), R0 = o.pelvis.t;
  const SLp = add(o.torso.t, rot(o.torso.q, SK.shoulder));
  let sh = q304.sh || 0;
  const Gof = s => sub(o.scabbard.t, times(ax, SWORD.tip - s * (SWORD.tip - SWORD.guard)));
  let G = Gof(sh);
  const extra = {};
  if (len(sub(G, SLp)) > ARM_REACH) { sh = .30; G = Gof(sh); extra.sh = .30; }
  const SQ = bladeQ(ax, rot(o.scabbard.q, [0, 0, -1]));
  SH0P = {...bladeChannels(G, SQ, R0, Ryaw), ...extra};
  // the free blade of SH0' reproduces the on-axis frame
  const fb = freeBlade({...q304, ...SH0P}, R0, Ryaw, SLp, add(R0, rot(Ryaw, SK.swing)));
  const da = qAngle(fb.SQ, SQ), dg = len(sub(fb.G, G));
  if (da > 1 || dg > .01) throw new Error(`SH0': the free blade at ending 304 is ${dg.toFixed(3)} b / ${da.toFixed(2)} deg off the scabbard axis`);
}
const supportTable = {}, retargetTable = {}, boundErrors = [], KEEP_F = {};
const spansOf = flags => { const out = []; let a = -1; flags.forEach((f, t) => { if (f && a < 0) a = t; if (!f && a >= 0) { out.push([a, t - 1]); a = -1; } }); if (a >= 0) out.push([a, flags.length - 1]); return out; };
const clipTime = {};
for (const c of CLIPS) {
  const tc0 = Date.now();
  const F = solveClip(c);
  clipTime[c.name] = Date.now() - tc0;
  // the guards' bounds (hard: a value at its bound is an error; the scabbard's first axis may give way to the second)
  F.forEach((fr, t) => {
    for (const [n, v] of Object.entries(fr.o._guard)) {
      const base = n.replace(/[+-]$/, ''), b = GUARD_BOUND[base];
      if (b !== undefined && gv(v) >= b - 1e-6 && !(base === 'scab' && gv(fr.o._guard.scabY) > 0)) boundErrors.push(`${c.name} t${t} ${n} ${gv(v).toFixed(1)} at its bound ${b}`);
    }
  });
  // the support table (the tests' contact / air spans) and the retarget table (corrections, contacts, stretch)
  {
    const fl = (fn) => F.map((fr, t) => !!fn(fr, t));
    const vis1 = fr => (fr.q.vis ?? 1) >= .999;
    // planted: the source's foot on the floor where S2a's body touched it (refCore; an S2a foot short of its floor target
    // hovered with the body: those ticks are `air` or between)
    const planted = (fr, k) => vis1(fr) && (fr.q.lf || 0) < .5 && fr.q[k][1] <= .0066 && !fr.q[k === 'fL' ? 'fLiftL' : 'fLiftR'] && (fr.q.wSeat || 0) < .5 && (fr.q.wKnee || 0) < .5 && fr.ref.low < .012;
    supportTable[c.name] = {
      low_ref: F.map(fr => +fr.ref.low.toFixed(3)),
      // lie: every full lying root (the body rests on the floor whatever S2a's height: its LY sat 9 cm up, its kip roll-back
      // lifted off the arms); touch: S2a touched, no full root (a partial lying / kneeling root is finished by the support pass's
      // touch rule); air: S2a's body >= 0.05 up, no seat / kneel / full lying root (w_root: the root weight per tick, the float
      // test's share of the airborne height)
      seat: spansOf(fl(fr => (fr.q.wSeat || 0) >= .999)), lie: spansOf(fl(fr => (fr.q.wLie || 0) >= .999)),
      kneel: spansOf(fl(fr => (fr.q.wKnee || 0) >= .999)),
      feet_l: spansOf(fl(fr => planted(fr, 'fL'))), feet_r: spansOf(fl(fr => planted(fr, 'fR'))),
      touch: spansOf(fl(fr => vis1(fr) && fr.ref.low < .012 && (fr.q.wSeat || 0) < .001 && (fr.q.wLie || 0) < .999 && (fr.q.wKnee || 0) < .999)),
      air: spansOf(fl(fr => vis1(fr) && fr.ref.low >= .05 && (fr.q.wSeat || 0) < .001 && (fr.q.wKnee || 0) < .001 && (fr.q.wLie || 0) < .999)),
      w_root: F.map(fr => +Math.max(fr.q.wSeat || 0, fr.q.wLie || 0, fr.q.wKnee || 0).toFixed(3)),
      ghost: spansOf(fl(fr => !vis1(fr))),
      // held: the sword in the left hand outside a sheathe blend (its pivot = the left grip); cuts: the clip's cut ticks;
      // lift: the support pass's last-resort lift per tick (only the ticks that needed one)
      held: spansOf(fl(fr => (fr.q.sword || 'hand') === 'hand' && (fr.q.hold ?? 1) > .5 && (fr.q.shW || 0) < .5)),
      // free_r: the right hand free (not on the scabbard, the throat, the grip or the hat): the blade keeps out of its forearm
      free_r: spansOf(fl(fr => freeRight(fr.q))),
      cuts: [...(c.cuts || [])],
      lift: Object.fromEntries(F.map((fr, t) => [t, +fr.o._lift.toFixed(3)]).filter(([, v]) => v > 0)),
      // hat_push: the hat moved clear of her head / torso (scarlet_pose.mjs guard hatClear, cm) where it held / handed over
      hat_push: Object.fromEntries(F.map((fr, t) => [t, +gv(fr.o._guard.hatClear).toFixed(1)]).filter(([, v]) => v > .5)),
      contacts: F.flatMap((fr, t) => fr.o._support.cts.map(x => [t, x.kind, x.side, ...(x.az !== undefined ? [+x.az.toFixed(2)] : [])])),
    };
    const mx = {}, cts = {};
    let st = 1, res = 0, dyM = 0, liftM = 0;
    for (const fr of F) {
      for (const [n, v] of Object.entries(fr.o._guard)) mx[n] = Math.max(mx[n] || 0, +gv(v).toFixed(2));
      for (const [k, v] of Object.entries(fr.o._contacts)) cts[k] = Math.max(cts[k] || 0, +v.toFixed(3));
      st = Math.max(st, fr.o._stretch.arm, fr.o._stretch.leg); res = Math.max(res, fr.o._support.bladeResidue);
      dyM = Math.max(dyM, Math.abs(fr.o._support.dy)); liftM = Math.max(liftM, fr.o._lift);
    }
    retargetTable[c.name] = {passes: F[0].passes, corrections: Object.fromEntries(Object.entries(mx).filter(([, v]) => v > 0).sort()), contacts: cts,
      stretch: +st.toFixed(4), blade_residue: +res.toFixed(3), support_dy: +dyM.toFixed(3), lift: +liftM.toFixed(3)};
  }
  const cuts = [...(c.cuts || [])];
  const byTick = new Map(), add_ = (t, l) => { if (!byTick.has(t)) byTick.set(t, []); byTick.get(t).push(l); };
  let keys = 0;
  const compiledD = {}, dense = denseTicks(c);
  const keyLists = {}, extraSplit = Object.fromEntries(PART_NAMES.map(n => [n, new Set()]));
  // S2d round 2: the forced blend-in ends at the first clip event from tick 2 on, and EVERY part's first key ends exactly there
  // (f0): a one-shot clip blends the whole body in from the previous clip's pose over the same ticks, so no part (the sword at
  // its event key, the face / the worn hat on the head) leaves another during the blend-in
  const evT = [...new Set(Object.values(c.events))].filter(t => t >= 2 && t < c.len).sort((x, y) => x - y);
  const f0 = Math.min(c.blend ?? 3, ...evT, c.len);
  // no dense / event / re-key split falls inside a one-shot clip's blend-in (its ticks before f0 come from the previous clip's pose
  // in game); a floor or planted-foot split may, and then the parts riding that part's group split with it (syncFirst)
  const free = t => c.loop || t >= f0;
  const syncFirst = Object.fromEntries(PART_NAMES.map(n => [n, new Set()])), firstEnd = {};
  const compilePart = n => {
    const seq = F.map(fr => fr.d[n]);
    // S2d round 3 (C3-1): a rider-group sync end m before f0 (syncFirst: a floor / planted-foot split of a part in the group) ends
    // the first key at m and starts a fitted segmentation there (the rest of [m, f0] is checked against TOL like any other span)
    const m0 = syncFirst[n].size ? Math.min(...syncFirst[n]) : null;
    let segs = m0 != null && m0 < f0
      ? [[0, m0], ...segmentsCut(seq.slice(m0), n, cuts.filter(t => t > m0).map(t => t - m0), 1).map(([x, y]) => [x + m0, y + m0])]
      : segmentsCut(seq, n, cuts, f0);
    if (dense.size) {
      const W0 = seq.map(v => JSON.stringify(written(v)));
      segs = segs.flatMap(([a, b]) => {
        const inner = [...dense].filter(k => k > a && k < b && free(k) && (W0[k] !== W0[k - 1] || W0[k] !== W0[k + 1])).sort((x, y) => x - y);
        const pts = [a, ...inner, b];
        return pts.slice(1).map((y, i) => [pts[i], y]);
      });
    }
    // the blade keys at the clip events (S2d: the hits, the clashes; the event check runs on what ships), and a body part the
    // shipped blade enters at an event keys there too (extraSplit, filled by the event check below)
    {
      const evs = n === 'sword' || n === 'sword_glow' ? evT : [];
      const xs = [...new Set([...[...evs, ...extraSplit[n]].filter(free), ...(f0 < c.len ? [f0] : [])])];
      if (xs.length) segs = segs.flatMap(([a, b]) => { const pts = [a, ...xs.filter(t => t > a && t < b).sort((x, y) => x - y), b]; return pts.slice(1).map((y, i) => [pts[i], y]); });
    }
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
    // S2d: a planted foot's shin (the support table's feet spans) whose interpolation moves its lowest point > 0.006 off the
    // solved one is split there too (a planted foot keeps its floor contact on what ships, not only at the keys)
    if (n === 'shin_l' || n === 'shin_r') {
      const plantedT = new Set(supportTable[c.name][n === 'shin_l' ? 'feet_l' : 'feet_r'].flatMap(([a, b]) => Array.from({length: b - a + 1}, (_, i) => a + i)));
      for (let guard = 0; plantedT.size && guard < 200; guard++) {
        const W = seq.map(written); let worst = null;
        for (const [a, b] of segs) for (let t = a + 1; t < b; t++) {
          if (!plantedT.has(t)) continue;
          const e = Math.abs(lowAt(t, interp(W[a], W[b], (t - a) / (b - a))) - lowAt(t, W[t]));
          if (e > .006 && (!worst || e > worst.e)) worst = {a, b, t, e};
        }
        if (!worst) break;
        segs = segs.flatMap(([a, b]) => (a === worst.a && b === worst.b ? [[a, worst.t], [worst.t, b]] : [[a, b]]));
      }
    }
    // S2d round 3 (C3-1): every span after the first key reproduces the solved frames within TOL: a split inside a forced or
    // fitted span (the forced first key's floor / planted-foot split, an event or a dense tick) can leave the rest of it unfitted,
    // and such a span is fitted again (subdivided by the compiler's own segmentation)
    {
      const W = seq.map(written);
      segs = segs.flatMap(([a, b], i) => {
        if (i === 0 || b - a < 2) return [[a, b]];
        let ok = true;
        for (let t = a + 1; t < b && ok; t++) ok = nearSolved(interp(W[a], W[b], (t - a) / (b - a)), W[t], n);
        return ok ? [[a, b]] : compiler.segments(seq.slice(a, b + 1), n, 1).map(([x, y]) => [x + a, y + a]);
      });
    }
    // the keys as shipped {at, dur, to}: a 1-tick segment ending on a cut tick and turning > 60 deg (or showing a hidden part)
    // snaps (a 0-tick key at b; the next segment starts one tick later)
    const snapAt = new Set(cuts), keyList = [], partMotion = [];
    let snapped = -1;
    for (const [a, b] of segs) {
      const turn = qAngle(seq[a].q, seq[b].q);
      const pop = !shown(seq[a]) && shown(seq[b]);
      if (b - a === 1 && snapAt.has(b) && (turn > 60 || pop || len(sub(seq[a].t, seq[b].t)) > .25)) { keyList.push({at: b, dur: 0, to: b}); snapped = b; continue; }
      if (turn > 118 && shown(seq[a]) && shown(seq[b])) partMotion.push(`${c.name} ${n} t${a}-${b}: ${turn.toFixed(0)} degree key (ambiguous slerp)`);
      if (a === snapped) { if (b - a > 1) keyList.push({at: a + 1, dur: b - a - 1, to: b}); }
      else keyList.push({at: a, dur: b - a, to: b});
    }
    // S2c: a hidden part (in the skin already: one fixed scale-0 transform from the solver) keys once, at tick 0
    if (HIDDEN.includes(n)) {
      if (seq.some(v => JSON.stringify(written(v)) !== JSON.stringify(written(seq[0])))) throw new Error(`hidden part ${n} moves in ${c.name}`);
      keyList.splice(0, keyList.length, {at: 0, dur: 0, to: 0});
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
    compiledD[n] = cv; keyLists[n] = {keyList, seq, partMotion}; firstEnd[n] = segs[0][1];
  };
  for (const n of PART_NAMES) compilePart(n);
  // the riders' groups end their first keys together (the earliest of the group: a floor split of one splits all)
  const RIDE_GROUPS = [['head', 'face', 'hat', 'hat_strings'], ['arm_l', 'forearm_l', 'sword', 'sword_glow']];
  const syncRiders = () => {
    if (c.loop) return;
    for (const G of RIDE_GROUPS) for (let k = 0; k < 4; k++) {
      const m = Math.min(...G.map(n => firstEnd[n]));
      const late = G.filter(n => firstEnd[n] > m);
      if (!late.length) break;
      for (const n of late) { syncFirst[n].add(m); compilePart(n); }
    }
  };
  syncRiders();
  // S2d round 2 (VB3): while the hat is worn (no hand-over blend), the shipped brim (its lowest square, the hat's pivot plane)
  // stays >= 0.001 b above the head's top corners: a tick where the two interpolations drift closer keys head, face and hat
  // there (the solved frames hold it 0.002 above the base head's top; a cut tick and the tick after it, which holds the snap,
  // are exempt, and so is the blend-in before f0: in game it starts from the previous clip's pose, the three parts together)
  const wornT = F.map((fr, t) => t >= f0 && (fr.q.hat || 'worn') === 'worn' && !fr.q.hatX && (fr.q.vis ?? 1) >= .999 && !cuts.includes(t) && !cuts.includes(t - 1));
  const [hbLo, hbHi] = BOX.head;
  const wornGap = t => {
    const hv = compiledD.head[t], tv = compiledD.hat[t];
    if (!shown(hv) || !shown(tv)) return Infinity;
    const hd = fromDisplay('head', hv), ht = fromDisplay('hat', tv);
    let m = Infinity;
    for (const x of [hbLo[0], hbHi[0]]) for (const z of [hbLo[2], hbHi[2]]) m = Math.min(m, -rot(conjQ(ht.q), sub(add(hd.t, rot(hd.q, [x, hbHi[1], z])), ht.t))[1]);
    return m;
  };
  // a rider check on what ships: measure(t) >= 0 on every active tick, else the parts key together at the worst tick
  const riderSplit = (parts, active, measure) => {
    for (let guard = 0; guard < 200; guard++) {
      let worst = null;
      for (let t = 0; t <= c.len; t++) if (active[t]) { const g = measure(t); if (g < 0 && (!worst || g < worst.g)) worst = {t, g}; }
      if (!worst || parts.every(n => extraSplit[n].has(worst.t))) return worst;
      for (const n of parts) { extraSplit[n].add(worst.t); compilePart(n); }
    }
    return null;
  };
  // the cup in her right hand (S2d round 2): no cup point more than 0.03 inside the shipped right forearm's box
  const cupT = F.map((fr, t) => t >= f0 && fr.q.cup === 'hand' && (fr.q.vis ?? 1) >= .999 && !cuts.includes(t) && !cuts.includes(t - 1));
  const cupFit = t => {
    const fv = compiledD.forearm_r[t], cv = compiledD.cup[t];
    if (!shown(fv) || !shown(cv)) return 0;
    const fa = fromDisplay('forearm_r', fv);
    return .03 - Math.max(...worldPoints(modelOn('cup', F[t].p), 'cup', fromDisplay('cup', cv)).map(P => boxDepth(P, fa, BOX.forearm_r)));
  };
  const wornSplit = () => {
    const w = riderSplit(['head', 'face', 'hat'], wornT, t => wornGap(t) - .001);
    riderSplit(['forearm_r', 'cup'], cupT, cupFit);
    return w && {t: w.t, g: w.g + .001};
  };
  wornSplit(); syncRiders();
  // the blade at the clip events (as shipped): no sample inside a body box (1 cm in); a failing event keys the blade, the part it
  // enters (with the parts riding it: the face, the worn hat and its strings on the head) and the sword arm at that tick (up to
  // three rounds), then reports what is left
  const eventFails = () => {
    const out = [];
  for (const [ev, te] of Object.entries(c.events)) {
    const sw = fromDisplay('sword', compiledD.sword[te]);
    if (!shown(compiledD.sword[te])) continue;
    const ax = rot(sw.q, [0, 1, 0]);
    for (const n of freeRight(F[te].q) ? [...BODY_BOX_PARTS, 'forearm_r'] : BODY_BOX_PARTS) {
      const v = fromDisplay(n, compiledD[n][te]);
      if (Math.min(...v.s) < 1e-4) continue;
      const [lo, hi] = BODY_BOX[n];
      let deep = 0;
      for (let k = 0; k <= 40; k++) {
        const y = SWORD_BLADE[0] + (SWORD_BLADE[1] - SWORD_BLADE[0]) * k / 40, P = add(sw.t, ax.map(x => x * y * sw.s[1]));
        const L = rot(conjQ(v.q), sub(P, v.t)).map((x, i) => x / v.s[i]);
        deep = Math.max(deep, Math.min(...[0, 1, 2].flatMap(i => [L[i] - lo[i], hi[i] - L[i]])));
      }
      if (deep > .01) out.push({n, te, msg: `${c.name} ${ev}@${te} ${n}: the blade ${deep.toFixed(3)} b inside`});
    }
  }
    return out;
  };
  for (let round = 0; round < 3; round++) {
    const fails = eventFails();
    if (!fails.length) break;
    const redo = new Set();
    for (const f of fails) for (const n of [f.n, ...(RIDERS[f.n] || []), 'sword', 'sword_glow', 'arm_l', 'forearm_l']) if (!extraSplit[n].has(f.te)) { extraSplit[n].add(f.te); redo.add(n); }
    if (!redo.size) break;
    for (const n of redo) compilePart(n);
    wornSplit(); syncRiders();
  }
  for (const f of eventFails()) bladeErrors.push(f.msg);
  { const w = wornSplit(); if (w) wornErrors.push(`${c.name} t${w.t}: the worn brim ${w.g.toFixed(4)} b over the head's top corners as shipped (< 0.001)`); }
  // S2d round 3 (C3-1): after each part's first key (before it: the blend-in from the previous clip's pose), what ships stays
  // near the solved frame (nearSolved: TOL x 1.25) on every tick; a cut tick and the tick after it (the snap) are exempt
  for (const n of PART_NAMES) {
    if (HIDDEN.includes(n)) continue;
    const seq = keyLists[n].seq;
    for (let t = firstEnd[n] + 1; t <= c.len; t++) {
      if (cuts.includes(t) || cuts.includes(t - 1) || nearSolved(compiledD[n][t], written(seq[t]), n)) continue;
      const x = compiledD[n][t], y = written(seq[t]);
      tolErrors.push(`${c.name} ${n} t${t}: ${qAngle(x.q, y.q).toFixed(1)} deg / ${len(sub(x.t, y.t)).toFixed(3)} b off the solved frame`);
    }
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
  // the keys as shipped and the 1-key turn errors of the final compile of every part
  for (const n of PART_NAMES) {
    const {keyList, seq, partMotion} = keyLists[n];
    motionErrors.push(...partMotion);
    for (const k of keyList) { add_(k.at, `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:${k.dur},transformation:${nbt(seq[k.to])}}`); keys++; }
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
  if (c.name === 'idle' || c.name === 'ev_give') KEEP_F[c.name] = F.map(fr => ({o: fr.o, p: fr.p, q: fr.q, d: fr.d}));
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
fail('the blade through her body at a clip event', bladeErrors);
fail('the worn hat on the head as shipped', wornErrors);
fail('what ships off the solved frame after the first key (beyond TOL x 1.25)', tolErrors);
fail('rotations above 120 degrees per tick or per key', motionErrors);
fail('a correction guard at its bound (scarlet_pose.mjs GUARD_BOUND)', boundErrors);
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
// ---- the built dimensions (S2d) and the contract asserts (api.py is the contract: S:hr/contract.md §7) ----------------------------
const DIMS = (() => {
  const F0 = KEEP_F.idle[0].o, worldOf = (n, fr) => worldPoints(modelOn(n, fr.p), n, fr.o[n]);
  const headTop = add(F0.head.t, rot(F0.head.q, [0, .5, 0]))[1];      // the head's base box, its top face centre
  let hullTop = 0;
  for (const fr of KEEP_F.idle) for (const n of PART_NAMES) { const v = fr.o[n]; if (!v || v.s[0] < 1e-4) continue; for (const P of worldOf(n, fr)) hullTop = Math.max(hullTop, P[1]); }
  // the thrown sword's summon offset from the right hand at the toss (seq.py S23): the item's centre in her yaw frame, measured
  // at ev_give 29 (the last tick the scabbard is in her hand; the clip keys it gone at the toss, 30)
  const g = KEEP_F.ev_give[29].o, yaw = q([0, KEEP_F.ev_give[29].p.rot[1], 0]);
  const ctr = add(g.scabbard.t, rot(g.scabbard.q, [0, -ITEM_SWORD.shift, 0])), rel = rot([-yaw[0], -yaw[1], -yaw[2], yaw[3]], sub(ctr, g._anchors.hand_r));
  return {height_idle: +headTop.toFixed(4), hat_top: +F0._anchors.hat_crown[1].toFixed(4), hull_top: +hullTop.toFixed(4),
    hat: {R: HAT.R, crownR: HAT.crownR, crownH: HAT.crownH, crown_y0: +(HAT.gap * 3 + .002).toFixed(4), brim: SK.brim, tilt: SK.brimTilt, hand: SK.hatHand, back: SK.hatBack},
    strings: {...STRINGS, painted: stringPoints()}, sash: SASH.tails,
    sword: {len: +(SWORD.tip - SWORD.pommel).toFixed(4), tip: SWORD.tip, blade_lo: SWORD.bladeLo, guard: SWORD.guard, pommel: SWORD.pommel, grip_lo: SWORD.gripLo, grip_hi: SWORD.gripHi,
      display_scale: PART_SCALE.sword},
    scabbard: {L: SCAB.L, display_scale: PART_SCALE.scabbard},
    item_sword: {len: ITEM_SWORD.len, scale: MODEL_SCALE.item_sword, units: +(ITEM_SWORD.len * 16 / MODEL_SCALE.item_sword).toFixed(2),
      toss_offset: [+rel[0].toFixed(2), +rel[1].toFixed(2), +(-rel[2]).toFixed(2)]},
    seat_top: SUPPORTS.stone.T, stone: SUPPORTS.stone, seat_items: {bottle: SUPPORTS.stone.bottle, cup: SUPPORTS.stone.cup},
    hat_rest: Object.fromEntries(Object.entries(HAT_REST).map(([k, v]) => [k, v.t])), hat_face: HAT_FACE, shadow_r: STUB.shadow.radius,
    contacts: {grip: SK.fore, brim_hold: SK.brimHold, hilt: SK.hilt, throat: SK.throat, lip_mouth: SK.lipMouth, cup_hand: CUP.hand, cup_centre: CUP.centre,
      bottle_neck: BOTTLE.neck, two_hand: SK.twoHand, hat_floor_hold: {inset: .02, up: HAT_FLOOR_HOLD}}};
})();
{
  const bad = [];
  if (Math.abs(API.HEIGHT - DIMS.height_idle) > .02) bad.push(`api.HEIGHT ${API.HEIGHT} vs the idle-t0 head top ${DIMS.height_idle}`);
  if (Math.abs(API.HAT_TOP - DIMS.hat_top) > .01) bad.push(`api.HAT_TOP ${API.HAT_TOP} vs the idle-t0 hat crown ${DIMS.hat_top}`);
  if (Math.abs(API.BRIM_D - 2 * HAT.R) > 1e-9) bad.push(`api.BRIM_D ${API.BRIM_D} vs 2 x HAT.R ${2 * HAT.R}`);
  if (Math.abs(API.SWORD_LEN - DIMS.sword.len) > .01) bad.push(`api.SWORD_LEN ${API.SWORD_LEN} vs the sword ${DIMS.sword.len}`);
  if (Math.abs(API.SCABBARD_LEN - SCAB.L) > .01) bad.push(`api.SCABBARD_LEN ${API.SCABBARD_LEN} vs SCAB.L ${SCAB.L}`);
  if (API.ITEM_SWORD_LEN !== ITEM_SWORD.len || API.ITEM_SWORD_SCALE !== MODEL_SCALE.item_sword) bad.push(`api.ITEM_SWORD_LEN / SCALE ${API.ITEM_SWORD_LEN} / ${API.ITEM_SWORD_SCALE} vs ${ITEM_SWORD.len} / ${MODEL_SCALE.item_sword}`);
  const m = API.BOSS.hit.h - DIMS.hull_top;
  if (!(m >= .05 - 1e-9 && m <= .12 + 1e-9)) bad.push(`the registry hit h ${API.BOSS.hit.h} - the idle hull top ${DIMS.hull_top} = ${m.toFixed(3)} (want 0.05..0.12)`);
  if (bad.length) throw new Error('contract (api.py) differs from the built rig:\n  ' + bad.join('\n  '));
}
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
  ghost_texture: itemId('ghost'),
  skin: {texture: SKIN_ID, file: `${TEX_DIR}/skin.png`, source: 'tools/scarlet_skin.mjs: the user\'s own skin (11-05), bytes written unchanged',
    bytes: SKIN_BYTES, sha1: SKIN_SHA1, size: [64, 64],
    layout: 'player avatar (tools/build_player_rig.mjs bodyModels = tools/arlecchino_geometry.mjs P1_SPECS) with its slim 3-px arms (the user\'s skin is a slim skin)',
    regions: SKIN_REGIONS, px: SKIN.px, body_px: SKIN.bodyPx, head0: SKIN.head0, inflate_px: {head: SKIN.inflHead, body: SKIN.infl}, inflate_ends: 'all',
    specs: BODY_SPECS, map: SKIN_MAP, hidden: HIDDEN, face_overlays: FACE_FX,
    _doc: 'map: model -> [region, row start, row end] (the base box shows the region\'s base layer, the second box its outer layer, inflated on all six sides). specs: the avatar\'s box specs (from / to in model units about the pivot [8, 8, 8], uv / over = [u, v, w, h, d], rows start..end). hidden: parts the skin already shows (model empty, scale 0). face_overlays: [col, row, cols, rows] of the 8 x 8 face painted by face_fx.'},
  item_sword: {model: itemId('item_sword'), length: ITEM_SWORD.len, display_scale: MODEL_SCALE.item_sword, display: ITEM_DISPLAY, toss_offset: DIMS.item_sword.toss_offset,
    icon: {model: itemId('item_sword_icon'), contexts: ICON_CONTEXTS, display: ICON_DISPLAY, dims: ICON,
      _doc: 'F-I (HR-03): items/item_sword.json selects on display_context: these contexts show the icon model (drawn in GUI px), every other one (the hands, item_display none) the rig model'}},
  skeleton: {hip_y: HIP_Y, hipJ: SK.hipJ, waist: SK.waist, neckB: SK.neckB, shoulder: SK.shoulder, armU: SK.armU, fore: SK.fore, thigh: SK.thigh, shin: SK.shin,
    ankleY: SK.ankleY, swing: SK.swing, brim: SK.brim, brimTilt: SK.brimTilt, hatBack: SK.hatBack, hatHand: SK.hatHand, brimHold: SK.brimHold, sashKnot: SK.sashKnot,
    scabHip: SK.scabHip, scabHipDir: SK.scabHipDir.map(x => +x.toFixed(6)), twoHand: SK.twoHand, hilt: SK.hilt, throat: SK.throat, anchors: SK.anchors, vis: SK.vis,
    _doc: 'the player avatar\'s skeleton (blocks; rig frame +X her left, +Y up, -Z forward): hip_y = the hip line at pos 0; waist = the torso pivot (the seam, body row 9) from the hip line; neckB / shoulder from the seam; armU / fore = shoulder -> elbow -> grip; thigh / shin = hip joint -> knee -> the outer-layer sole'},
  dims: DIMS,
  support: supportTable,
  retarget: {factors: {S_LEG: +S_LEG.toFixed(6), S_ARM: +S_ARM.toFixed(6), S_SCAB: +S_SCAB.toFixed(6), K_ARC: +K_ARC.toFixed(6)},
    patches: PATCHES.map(P => ({id: P.id, clip: P.clip, in: P.in, out: P.out, ...(P.set ? {set: P.set} : {}), ...(P.add ? {add: P.add} : {}), why: P.why})),
    iai_delta: IAI_DELTA, sh0: SH0P, hip_dir: hipDirChannels(), hat_flights: HAT_FLIGHTS, aside: ASIDE, bounds: GUARD_BOUND, slopes: GUARD_SLOPE, clips: retargetTable,
    _doc: 'per sample: retarget (angles kept; pos x k(lf); soles about the hip joint x S_LEG; grip distances x S_ARM + the lock rule; planted hands x S_LEG; scOff x S_SCAB; world-hat spots) -> overlay (PATCHES, the hat hand-overs, the flights) -> solve. clips: per clip the solver passes, the largest value of every correction guard (degrees, or cm for drop / bPush / close / hatBackZ / hatPush / hatClear, percent for armUp; +/- = the two senses), the largest contact distance per kind, the largest IK stretch, the blade residue inside the body (b), the largest support move and lift'},
  paint_roles: PAINT_ROLES,
  budgets: {atlas_px: atlasPx, atlas_budget: ATLAS_BUDGET, sprites: Object.keys(sprites).length, elements_at_rest: ELEMENTS, elements_budget: EL_BUDGET,
    parts: PART_NAMES.length, models: Object.keys(models).length, key_files: keyFiles, keys: keyLines, rig_functions: fnFiles.files, rig_bytes: fnFiles.bytes,
    cull_overhang_ticks: cullWarn.length},
  sprites: ledger,
};
json(path.join(here, 'scarlet_rig_manifest.json'), manifest);
if (process.env.HR_TIMES) console.log('solve ms per clip', JSON.stringify(clipTime));
console.log(`Built the Scarlet rig: ${PART_NAMES.length} parts, ${CLIPS.length} clips (${missing.length} stand-ins; cine: ${CINE_SOURCE}), ${keyFiles} key files, ${keyLines} keys, ` +
  `${fnFiles.files} rig functions (${(fnFiles.bytes / 1e6).toFixed(2)} MB), ${Object.keys(models).length} models, ${Object.keys(sprites).length} sprites ${(atlasPx / 1e6).toFixed(3)} M px, ` +
  `elements at rest ${ELEMENTS.normal} / ghost ${ELEMENTS.ghost} [${((Date.now() - t0) / 1000).toFixed(1)} s]`);
if (debugDp) {
  fs.rmSync(path.join(debugDp, 'data/rlk/function/boss/scarlet/rig'), {recursive: true, force: true});
  fs.cpSync(rigDir, path.join(debugDp, 'data/rlk/function/boss/scarlet/rig'), {recursive: true});
  if (!fs.existsSync(path.join(debugDp, 'pack.mcmeta'))) fs.copyFileSync(path.join(dp, 'pack.mcmeta'), path.join(debugDp, 'pack.mcmeta'));
  putDebug('hr_dbg/rest', PART_NAMES.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(written(REST.d[n]))}}`));
  // the player avatar beside her (Skirk's idle frame 0 from the pack's own avatar rig: tools/player_motion/locomotion.json) and the
  // kit's seat stone with its items (debug renders only)
  const loco = JSON.parse(fs.readFileSync(path.join(here, 'player_motion/locomotion.json'), 'utf8'));
  const av = (await import('./arlecchino_pose.mjs')).avatarTransform(loco.characters.skirk.idle.frames[0].pose);
  const avNbt = v => `{translation:[${v.t.map(x => x.toFixed(5) + 'f').join(',')}],left_rotation:[${v.q.map(x => x.toFixed(5) + 'f').join(',')}],scale:[${(v.s || [1, 1, 1]).map(x => x.toFixed(5) + 'f').join(',')}],right_rotation:[0f,0f,0f,1f]}`;
  putDebug('hr_dbg/avatar', Object.entries(av).map(([n, v]) => `summon minecraft:item_display ~1.4 ~ ~ {Tags:["hr_dbg_avatar"],item_display:"none",transformation:${avNbt(v)},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/${n === 'weapon' ? 'weapons/sword' : 'skirk/' + n}"}}}`));
  const st = SUPPORTS.stone, sz = [2 * st.half, st.T, st.back - st.front], ctr = [0, st.T / 2, (st.back + st.front) / 2];
  // stand-ins of the kit's tuff stone (centred box) and its potion / bowl (base at the pivot) for the offline renderer
  const disp = (item, P, s) => `summon minecraft:item_display ~ ~ ~ {Tags:["hr_dbg_seat"],item_display:"none",transformation:{translation:[${P[0].toFixed(4)}f,${P[1].toFixed(4)}f,${(-P[2]).toFixed(4)}f],left_rotation:[0f,0f,0f,1f],scale:[${s.map(x => x.toFixed(4) + 'f').join(',')}],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:hr_dbg/${item}"}}}`;
  putDebug('hr_dbg/seat', [disp('tuff', ctr, sz), disp('potion', st.bottle, [.42, .42, .42]), disp('bowl', st.cup, [.42, .42, .42])]);
  putDebug('hr_dbg/seat_bottle', [disp('tuff', ctr, sz), disp('potion', st.bottle, [.42, .42, .42])]);
  putDebug('hr_dbg/seat_cup', [disp('tuff', ctr, sz), disp('bowl', st.cup, [.42, .42, .42])]);
  putDebug('hr_dbg/seat_stone', [disp('tuff', ctr, sz)]);
}
void H_POSE;
