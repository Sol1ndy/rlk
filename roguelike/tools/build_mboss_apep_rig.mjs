// Display-entity rig of 아펩의 오아시스 파수꾼 (Guardian of Apep's Oasis), the chapter-3 boss: BOTH forms (종막 phase 1, 기원
// phase 3) and BOTH stances (CROUCH, UPRIGHT) on one superset skeleton of 49 parts (scratchpad ap/plan.md R1-R22,
// ap/ap_contract.md §0.4, ap/understand/model.md, model_p3.md).
// node tools/build_mboss_apep_rig.mjs --resourcepack <unpacked pack> [--datapack <pack>] [--no-paint | --paint a,b]
//                                     [--debug-dp <scratch dir> [--debug-clips a,b | all]] [--allow-steps]
//
// Writes
//   RP  assets/rlk/textures/mboss/apep/*.png (apep_paint.mjs) + item atlas entries
//       assets/rlk/models/item/mboss/apep/*.json, assets/rlk/items/mboss/apep/*.json (one item per part model x form x
//       tint look; every item carries the five tint-slot colours, apep_materials.mjs)
//   DP  data/rlk/function/mboss/apep/rig/** (owned by this generator, rebuilt from scratch on every run)
//   tools/mboss_apep_rig_manifest.json (the contract of ap_contract.md §0.4: parts, skeleton, stances, clips, events,
//       looks, hands, proxies, px sets, capsules, park, sprites, elements, budgets, objectives)
//
// Runtime model (the module's contract: tools/mboss_apep_rig_api.md):
//   * 49 item_display parts with FIXED UUIDs 524c4b4d-4150-4400-8000-0000000000NN (NN = 0x00-0x30, plan R4), split by
//     region (head / body / limbs / hands / tail). Tags rlk_room, rlk_mb_aux, rlk_mb_part, rlk_mb_apep_part,
//     rlk_mb_ap_<part>. Culling box 30 x 16 and view_range 3 (R6). The shadow helper at 0x40.
//   * The anchor (the boss body, on the floor under the thorax) runs rig/tick each tick: the parts follow its position
//     and yaw (createRigFollow: static-anchor skip, the follow_y burrow sinks, the burrowed list) and the current clip
//     applies its keys (mboss_rig_compile.mjs). Parked (R10): rig/tick returns at once, every part at scale 0.
//   * Looks (R12): channels form / face / core / core_glow / tint / bright and the hand sets (R8), stored on the anchor
//     (apRig*), re-applied by look_apply after a respawn or an unpark. The display transform of a part depends on the
//     form (each form's models are authored in their own reference stance, apep_pose FRAMES), so every clip is
//     authored for one form and the module swaps the form only while the body is hidden (the CS white-out).
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {paintApepTextures, spriteId, apepSprites, ATLAS_BUDGET} from './apep_paint.mjs';
import {partModels, checkBounds, FORM_MODELS, HAND_VARIANTS, FACE_ITEMS, CORE_MODELS, EMPTY, REGION_OF} from './apep_geometry.mjs';
import {solve, modelFrames, toDisplay, modelPoint, carry, PART_NAMES, PART_SCALE, PART_REGION, PART_BRIGHT, PART_BRIGHT_P3, BONES, BONE, J, POSE_ONLY,
  PROXIES, proxyPoints, pxLocal, CAPSULES, ANCHOR_POINTS, FORM_POINTS, toLocal, TAIL_C, LIMB_C, HAND_PARTS, TAIL_PARTS, FRAMES} from './apep_pose.mjs';
import {CLIPS as ALL_CLIPS, accumulate, sampleClip as sample, STANCES, denseYaw, sinkAt, SINK_TABLE, CLIP_TABLE} from './apep_clips.mjs';
import {itemTints, TINT_IDS, TINT_COLOR, TINT_FORMS, SLOTS, SLOT_COLOR, FACE_MUL} from './apep_materials.mjs';
import {createRigCompiler, createRigFollow, summonPart, summonShadow, cullOverhang, fitTracks, nbt} from './mboss_rig_compile.mjs';
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
const NS = 'rlk:mboss/apep/rig';
const rigDir = path.join(dp, 'data/rlk/function/mboss/apep/rig');
fs.rmSync(rigDir, {recursive: true, force: true});
const fn = (n, lines) => put(path.join(rigDir, n + '.mcfunction'), (Array.isArray(lines) ? lines : [lines]).join('\n'));
const assets = path.join(rp, 'assets/rlk');
const r2 = x => +x.toFixed(2) || 0, r3 = x => +x.toFixed(3) || 0;

// ---- parts, UUIDs (plan R4: 49 parts, cap 56, slots 0x00-0x37) -----------------------------------------------------------------
if (PART_NAMES.length > 56) throw new Error(`${PART_NAMES.length} parts: the hard cap is 56`);
if (PART_NAMES.length !== 49) console.warn(`warn: ${PART_NAMES.length} parts (plan R4: 49)`);
const BLOCK = '524c4b4d-4150-4400-8000-0000000000', INTS = [1380731725, 1095779328, -2147483648];
const IDX = Object.fromEntries(PART_NAMES.map((n, i) => [n, i]));
const hex2 = i => i.toString(16).padStart(2, '0');
const uuidOf = n => (n === 'shadow' ? BLOCK + '40' : BLOCK + hex2(IDX[n]));
const uuidInts = i => [...INTS, i];
const SHADOW_IDX = 0x40;
const itemId = m => `rlk:mboss/apep/${m}`;
const CULL = {width: 30, height: 16}, VIEW_RANGE = 3;

// ---- items: models x forms x tint looks (plan R12 / R13, apep_materials TINT SLOTS) -----------------------------------------
// item id -> {model, form, face?}; tint variants `${item}_t${id}` for the tint looks of that form
const ITEMS = {[EMPTY]: {model: EMPTY, form: null}};
for (const [part, fm] of Object.entries(FORM_MODELS)) for (const f of ['p1', 'p3']) ITEMS[`${part}_${f}`] = {model: fm[f], form: f};
for (const [part, vars] of Object.entries(HAND_VARIANTS)) for (const [v, m] of Object.entries(vars)) ITEMS[`${part}_${v}`] = {model: m, form: v.slice(0, 2)};
for (const [look, it] of Object.entries(FACE_ITEMS)) if (it) ITEMS[`face_${look}`] = {model: it.model, form: it.form, face: it.face};
for (const [look, m] of Object.entries(CORE_MODELS)) ITEMS[`core_${look}`] = {model: m, form: look.slice(0, 2)};
const tintItem = (item, tint) => (!tint || tint === 'none' || item === EMPTY || !ITEMS[item] || !TINT_FORMS[tint].includes(ITEMS[item].form) ? item : `${item}_t${TINT_IDS[tint]}`);
const FORM_PART_ITEMS = Object.fromEntries(Object.keys(FORM_MODELS).map(p => [p, {p1: `${p}_p1`, p3: `${p}_p3`}]));
const HAND_ITEMS = Object.fromEntries(Object.entries(HAND_VARIANTS).map(([p, vars]) => [p, Object.fromEntries(Object.keys(vars).map(v => [v, `${p}_${v}`]))]));

// ---- resource pack: textures, models, item definitions ---------------------------------------------------------------------
const spriteRecs = apepSprites();
const sprites = flag('--no-paint') ? null : paintApepTextures(rp, arg('--paint') ? arg('--paint').split(',') : null);
const models = partModels();
for (const [name, els] of Object.entries(models)) checkBounds(name, els);
const modelDir = path.join(assets, 'models/item/mboss/apep'), itemDir = path.join(assets, 'items/mboss/apep');
fs.rmSync(modelDir, {recursive: true, force: true});
fs.rmSync(itemDir, {recursive: true, force: true});
let untinted = 0;
for (const [name, els] of Object.entries(models)) {
  const used = [...new Set(els.flatMap(e => Object.values(e.faces).map(f => f.texture.slice(1))))];
  for (const u of used) if (!spriteRecs[u]) throw new Error(`model ${name}: unknown sprite ${u}`);
  for (const e of els) for (const f of Object.values(e.faces)) if (f.tintindex === undefined) untinted++;
  const tex = used.length ? used : ['g_shell'];
  json(path.join(modelDir, name + '.json'), {ambientocclusion: false, textures: {...Object.fromEntries(used.map(t => [t, spriteId(t)])), particle: spriteId(tex[0])}, elements: els});
}
if (untinted) throw new Error(`${untinted} faces without a tintindex (plan R12: every painted face is tinted)`);
const hexOf = v => '#' + v.toString(16).padStart(6, '0').toUpperCase();
const tintedItems = {};
const writeItem = (id, model, tints) => {
  if (!models[model]) throw new Error(`item ${id}: unknown model ${model}`);
  json(path.join(itemDir, id + '.json'), {model: {type: 'minecraft:model', model: 'rlk:item/mboss/apep/' + model, ...(tints ? {tints: tints.map(v => ({type: 'minecraft:constant', value: v}))} : {})}});
};
let itemCount = 0;
for (const [id, it] of Object.entries(ITEMS)) {
  if (!it.form) { writeItem(id, it.model, null); itemCount++; continue; }
  writeItem(id, it.model, itemTints(it.form, {face: it.face})); itemCount++;
  if (it.face && it.face !== 'p3_idle') tintedItems[id] = {model: it.model, tint: FACE_MUL[it.face], tints: itemTints(it.form, {face: it.face}).map(hexOf)};
  for (const [t, forms] of Object.entries(TINT_FORMS)) if (forms.includes(it.form)) {
    const tid = `${id}_t${TINT_IDS[t]}`, tints = itemTints(it.form, {tint: t, face: it.face});
    writeItem(tid, it.model, tints); itemCount++;
    tintedItems[tid] = {model: it.model, tint: TINT_COLOR[t], tints: tints.map(hexOf)};
  }
}
// atlas budget (plan R13) and the sprite ledger
let atlasPx = 0;
const ledger = [];
for (const [n, s] of Object.entries(spriteRecs)) {
  if (s.w > 512 || s.h > 512 || s.w % 16 || s.h % 16) throw new Error(`sprite ${n} ${s.w}x${s.h}: sides <= 512, multiples of 16`);
  atlasPx += s.w * s.h;
  ledger.push({name: n, region: s.region, w: s.w, h: s.h, px: s.w * s.h, px_per_b: s.ppb, use: s.use, forms: s.forms});
}
ledger.sort((a, b) => a.name.localeCompare(b.name));
if (atlasPx > ATLAS_BUDGET) throw new Error(`Apep sprites use ${atlasPx} px of the atlas (budget ${ATLAS_BUDGET})`);
const elementCount = Object.fromEntries(Object.entries(models).map(([n, e]) => [n, e.length]));

// ---- per-form model frames and model key points (for the pose checks) -------------------------------------------------------------
const REF = {CROUCH: solve(STANCES.CROUCH), UPRIGHT: solve(STANCES.UPRIGHT)};
const M = modelFrames(REF);
// model key points in the part's authoring frame (blocks): the element corners, deduplicated and thinned
const KEY = {};
for (const [n, els] of Object.entries(models)) {
  const pts = new Map();
  // element corners with the element rotation applied (one axis, about its origin; Minecraft's sense: +angle turns
  // y about x as (y cos - z sin, y sin + z cos), and likewise for the other axes)
  const turn = (p, r) => {
    if (!r || !r.angle) return p;
    const a = r.angle * Math.PI / 180, c = Math.cos(a), s = Math.sin(a), o = r.origin, d = p.map((v, i) => v - o[i]);
    const q = r.axis === 'x' ? [d[0], d[1] * c - d[2] * s, d[1] * s + d[2] * c] : r.axis === 'y' ? [d[0] * c + d[2] * s, d[1], -d[0] * s + d[2] * c] : [d[0] * c - d[1] * s, d[0] * s + d[1] * c, d[2]];
    return q.map((v, i) => +(v + o[i]).toFixed(4));
  };
  for (const e of els) for (const x of [e.from[0], e.to[0]]) for (const y of [e.from[1], e.to[1]]) for (const z of [e.from[2], e.to[2]]) { const P = turn([x, y, z], e.rotation); pts.set(P.join(','), P); }
  let arr = [...pts.values()];
  if (arr.length > 120) arr = arr.filter((_, i) => i % Math.ceil(arr.length / 120) === 0);
  KEY[n] = arr;   // model units; converted per part scale below
}
const toBlocks = (u, k) => [(8 - u[0]) * k / 16, (u[1] - 8) * k / 16, (u[2] - 8) * k / 16];
// the item model a part shows under a look state {form, hands: {part: variant}, face, core}
const restLook = f => ({form: f, hands: Object.fromEntries(HAND_PARTS.map(p => [p, f === 'p1' ? (p[0] === 'a' ? 'p1_planted' : 'p1_open') : (p[0] === 'a' ? 'p3_fork' : p[0] === 'b' ? 'p3_open' : 'p3_curl')])),
  face: f === 'p1' ? 'p1_bud' : 'p3_idle', core: f === 'p1' ? 'p1_bulb' : 'p3_sternum'});
function modelOfPart(n, L) {
  if (HAND_PARTS.includes(n)) return HAND_VARIANTS[n][L.hands[n]];
  if (n === 'face') return L.face === 'hidden' ? EMPTY : FACE_ITEMS[L.face].model;
  if (n === 'core') return CORE_MODELS[L.core];
  return FORM_MODELS[n][L.form];
}
// world points of a posed part (rig frame), dy = the follow_y sink
function partPoints(o, n, f, model, dy = 0) {
  if (!model || o[n].s < 1e-4) return [];
  const k = PART_SCALE[n];
  return KEY[model].map(u => { const P = modelPoint(o, M, f, n, toBlocks(u, k)); P[1] += dy; return P; });
}

// ---- clip frames, pose checks ---------------------------------------------------------------------------------------------------
const HANDS_SET = {
  p1_rest: {a_hand_l: 'p1_planted', a_hand_r: 'p1_planted', b_hand_l: 'p1_open', b_hand_r: 'p1_open', c_hand_l: 'p1_open', c_hand_r: 'p1_open'},
  p1_lift: {a_hand_l: 'p1_raised', a_hand_r: 'p1_raised', b_hand_l: 'p1_curl', b_hand_r: 'p1_curl', c_hand_l: 'p1_curl', c_hand_r: 'p1_curl'},
  p3_open: {a_hand_l: 'p3_fork', a_hand_r: 'p3_fork', b_hand_l: 'p3_open', b_hand_r: 'p3_open', c_hand_l: 'p3_curl', c_hand_r: 'p3_curl'},
  p3_curl: {a_hand_l: 'p3_fork', a_hand_r: 'p3_fork', b_hand_l: 'p3_curl', b_hand_r: 'p3_curl', c_hand_l: 'p3_curl', c_hand_r: 'p3_curl'},
};
const HAND_SET_IDS = {p1_rest: 0, p1_lift: 1, p3_open: 2, p3_curl: 3};
const PULSE = {from: .9, to: 1.0, ticks: 2};
// hand-model swap pulses (R8) and the scale-in (R12): a per-part scale multiplier at tick t
function scaleMul(c, t, n) {
  let k = 1;
  if (c.scale_in) { const [a, b, from] = c.scale_in; if (t >= a && t <= b) k *= from + (1 - from) * (t - a) / Math.max(1, b - a); }
  if (HAND_PARTS.includes(n)) for (const ev of c.hand_events || []) {
    const te = ev[0], hit = ev.length === 2 || ev[1] === n;
    if (hit && t >= te && t < te + PULSE.ticks) k *= PULSE.from + (PULSE.to - PULSE.from) * (t - te) / PULSE.ticks;
  }
  return k;
}
function frame(c, t, ks, prev) {
  const p = sample(c, t, ks);
  const o = solve(p, {prev: prev && prev.o._bend});
  const d = {}, ti = Math.floor(t);
  for (const n of PART_NAMES) d[n] = toDisplay(n, o, M, c.form, scaleMul(c, ti, n));
  return {d, p, o};
}
const clipFrames = (c, ks = accumulate(c)) => { const out = []; for (let t = 0; t <= c.len; t++) out.push(frame(c, t, ks, out[t - 1])); return out; };
// the look state of a clip at tick t (start from the form's rest looks; the clip's look / hand events applied in order)
function lookAt(c, t) {
  const L = restLook(c.form);
  if (c.form === 'p3' && c.stance[0] === 'CROUCH') { L.face = 'hidden'; L.hands = {...HANDS_SET.p3_curl}; }
  for (const [te, ch, lk] of c.look_events || []) if (te <= t) { if (ch === 'face') L.face = lk; if (ch === 'core') L.core = lk; if (ch === 'form') L.form = lk; }
  for (const ev of c.hand_events || []) if (ev[0] <= t) { if (ev.length === 2) Object.assign(L.hands, HANDS_SET[ev[1]]); else L.hands[ev[1]] = ev[2]; }
  return L;
}
// Pose checks (every frame of every clip): no horizontal root travel; every shown part inside the culling box (radial,
// cullOverhang); the hands never under the floor outside the hidden spans; every part's top <= -0.1 b at each hidden-span
// start (R9, with the follow_y sink); events inside the clip. Extents per clip.
function poseChecks(c, frames) {
  const errs = [], over = {};
  const ext = [[Infinity, -Infinity], [Infinity, -Infinity], [Infinity, -Infinity]];
  const hidden = t => (c.hidden || []).some(([a, b]) => t >= a && t <= b);
  frames.forEach((f, t) => {
    if (Math.abs(f.p.pos[0]) > 1e-9 || Math.abs(f.p.pos[2]) > 1e-9) errs.push(`${c.name} t${t}: root travel (x/z must be 0)`);
    const L = lookAt(c, t), dy = sinkAt(c, t);
    for (const n of PART_NAMES) {
      const pts = partPoints(f.o, n, c.form, modelOfPart(n, L), dy);
      for (const P of pts) {
        for (let i = 0; i < 3; i++) { ext[i][0] = Math.min(ext[i][0], P[i]); ext[i][1] = Math.max(ext[i][1], P[i]); }
        const ov = cullOverhang(P, CULL);
        if (ov > 0) over[n] = Math.max(over[n] || 0, r2(ov));
      }
      if (HAND_PARTS.includes(n) && !hidden(t) && dy > -.01 && pts.length) {
        const lo = Math.min(...pts.map(P => P[1]));
        if (lo < -.2) errs.push(`${c.name} t${t}: ${n} ${lo.toFixed(2)} b below the floor`);
      }
    }
  });
  for (const [a] of c.hidden || []) {
    const f = frames[a], L = lookAt(c, a), dy = sinkAt(c, a), o = solve(sample(c, Math.max(0, a - 1), accumulate(c)));
    let top = -Infinity;
    for (const n of PART_NAMES) for (const P of partPoints(o, n, c.form, modelOfPart(n, L), dy)) top = Math.max(top, P[1]);
    if (top > -.1) errs.push(`${c.name}: a part top at ${top.toFixed(2)} b (> -0.1) at the hidden-span start t${a} (R9)`);
    void f;
  }
  for (const [e, t] of Object.entries(c.events || {})) if (!(t >= 0 && t <= c.len)) errs.push(`${c.name}: event ${e} at ${t} outside 0..${c.len}`);
  return {errors: errs, over, extents: ext.map(([a, b]) => [r2(a), r2(b)])};
}

// ---- the R3 residual table (UPRIGHT joints vs model_p3 §6.2) ----------------------------------------------------------------------
const TAIL_U = [[0, 1.2, .5], [0, .3, 1.3], [0, .2, 2.4], [.6, .2, 3.4], [1.6, .2, 4.1], [2.7, .2, 4.2], [3.6, .2, 3.5], [4.0, .2, 2.4], [3.9, .2, 1.4]];
const LIMB_U = {a: [[1.1, 5.5, .1], [2.3, 7.4, .2], [3.6, 9.65, 0], [3.8, 10.4, -.2]], b: [[1.2, 5.0, -.4], [2.8, 5.1, -.9], [4.4, 5.6, -1.0], [5.2, 6.2, -1.0]], c: [[1.1, 3.0, -.3], [2.6, 2.4, -.8], [3.5, .7, -.9], [3.9, .15, -.8]]};
const TAILN = ['tail_1', 'tail_2', 'tail_3', 'tail_4', 'tail_5', 'tail_6', 'tail_7', 'tail_tip'];
const RESID = [
  ['pelvis', 'pelvis', null, [0, 3.1, .2]], ['abdomen (tail root end)', 'abdomen', [0, 2.39, 2.89], [0, 1.2, .45]],
  ...TAIL_U.map((u, i) => [i < 8 ? TAILN[i] : 'tail end', i < 8 ? TAILN[i] : 'tail_tip', i < 8 ? null : TAIL_C[8], u]),
  ['hem_a', 'hem_a', null, [0, 2.6, -.5]], ['hem end', 'hem_b', [0, .15, 1.85], [0, .15, -.7]],
  ['chest', 'chest', null, [0, 4.2, 0]], ['shoulders', 'shoulders', null, [0, 5.3, -.1]], ['neck', 'neck', null, [0, 5.6, -.2]], ['head', 'head', null, [0, 6.0, -.3]],
  ['hood peak', 'hood', [0, 3.0, -4.0], [0, 8.5, -.3]],
  ...['l', 'r'].flatMap(s => { const m = v => (s === 'l' ? v : [-v[0], v[1], v[2]]); return ['a', 'b', 'c'].flatMap(L => LIMB_U[L].map((u, i) => [`${L}_${['up', 'lo', 'hand', 'tip'][i]}_${s}`, i < 3 ? `${L}_${['up', 'lo', 'hand'][i]}_${s}` : `${L}_hand_${s}`, i < 3 ? null : m(LIMB_C[L][3]), m(u)])); }),
  ...['l', 'r'].flatMap(s => { const m = v => (s === 'l' ? v : [-v[0], v[1], v[2]]); return [[`mantle_${s}_a`, `mantle_${s}_a`, null, m([1.2, 5.6, .6])], [`mantle_${s}_a tip`, `mantle_${s}_a`, m([3.0, 3.4, .4]), m([1.9, 3.7, 1.2])],
    [`mantle_${s}_b`, `mantle_${s}_b`, null, m([.9, 5.2, .7])], [`mantle_${s}_b tip`, `mantle_${s}_b`, m([2.6, 3.1, 1.3]), m([1.3, 3.2, 1.2])],
    [`hair_${s}_1`, `hair_${s}_1`, null, m([.8, 7.4, -.6])], [`hair_${s}_2`, `hair_${s}_2`, null, m([1.0, 6.0, -1.0])], [`hair_${s} end`, `hair_${s}_2`, m([1.7, .2, -2.8]), m([1.1, 4.6, -1.0])],
    [`beads_${s}`, `beads_${s}`, null, m([1.4, 5.5, -.3])], [`beads_${s} end`, `beads_${s}`, m([1.81, 1.35, -.69]), m([2.0, 3.5, -.6])]]; }),
];
const oU = REF.UPRIGHT;
const residuals = RESID.map(([lab, b, pt, u]) => { const Q = pt ? carry(oU, b, pt) : oU[b].t; return {joint: lab, target: u, fk: Q.map(r2), d: r3(Math.hypot(...Q.map((v, i) => v - u[i])))}; });
const residMax = Math.max(...residuals.map(r => r.d));
// per-form model points (exact by authoring) and the hood swing (§6.1: hinge >= 100 deg, the face visible)
const faceU = modelPoint(oU, M, 'p3', 'face', FORM_POINTS.face.p3[1]), coreU = modelPoint(oU, M, 'p3', 'core', FORM_POINTS.core.p3[1]);
const hoodSwing = (() => { const a = [0, -.76, -2.08], C0 = a, U0 = (() => { const P = carry(oU, 'hood', [0, 3.0, -4.0]); return P.map((v, i) => v - oU.hood.t[i]); })();
  const ang = v => Math.atan2(v[1], -v[2]) * 180 / Math.PI; return r2(ang(U0) - ang(C0)); })();
const hoodTopU = Math.max(...partPoints(oU, 'hood', 'p3', FORM_MODELS.hood.p3).map(P => P[1]), ...partPoints(oU, 'crown', 'p3', FORM_MODELS.crown.p3).map(P => P[1]));
const residErr = [];
if (residMax > .25) residErr.push(`R3 residual ${residMax} b > 0.25 (${residuals.filter(r => r.d > .25).map(r => r.joint).join(', ')})`);
if (hoodSwing < 100) residErr.push(`the hood swings ${hoodSwing} deg in UPRIGHT (< 100: the face would be covered)`);
if (hoodTopU > 9.0) residErr.push(`the UPRIGHT hood / crown top ${hoodTopU.toFixed(2)} b > 9.0`);

// ---- follow (RIGLIB): the burrowed list, the sink offsets, the static skip, the shadow --------------------------------------------
const F = createRigFollow({ns: NS, obj: 'apRig', fn, uuidOf, lists: {all: PART_NAMES, burrowed: []}, fixed: ['shadow'], sink: SINK_TABLE, staticSkip: true,
  comment: '# Parts and the shadow helper follow the anchor (run as and rotated as the anchor at its feet, pitch 0).'});
F.write();

// ---- compile clips -------------------------------------------------------------------------------------------------------------
const debugDp = arg('--debug-dp') && path.resolve(arg('--debug-dp'));
const debugClips = (arg('--debug-clips') || '').split(',').filter(Boolean);
const debugOf = c => debugDp && (debugClips.includes('all') || debugClips.includes(c.name) || (c.dbg && debugClips.includes('dbg')));
if (debugDp) fs.rmSync(path.join(debugDp, 'data/rlk/function/ap_dbg'), {recursive: true, force: true});
const putDebug = (n, lines) => put(path.join(debugDp, 'data/rlk/function', n + '.mcfunction'), lines.join('\n'));
// tolerances (plan R16): 0.03 b on the arms, tail, hair, mantle, hem; 0.012 b on the hood, hands, face (and the rest)
const LONG = PART_NAMES.filter(n => /^(a_up|a_lo|b_up|b_lo|c_up|c_lo|tail_|hair_|mantle_|hem_|beads_|abdomen)/.test(n));
const TOL = {t: .012, s: .015, rDefault: .8, r: Object.fromEntries(PART_NAMES.map(n => [n, /^(a_lo|a_up|tail_[5-7]|tail_tip|beads)/.test(n) ? .35 : /^(hood|chest|shoulders|abdomen)/.test(n) ? .4 : .6])),
  tp: Object.fromEntries(LONG.map(n => [n, .03]))};
const mkCompiler = debug => createRigCompiler({ns: NS, obj: 'apRig', fn, parts: PART_NAMES, uuidOf, tol: TOL, swapLine: () => '', debug: debug ? {put: putDebug, dir: 'ap_dbg'} : null});
const compiler = mkCompiler(false), debugCompiler = debugDp ? mkCompiler(true) : null;
// the shipped clips (the frozen contract's table) and the debug poses (dbg_*: renders and checks only, never in the rig)
const CLIPS = ALL_CLIPS.filter(c => !c.dbg), DBG_CLIPS = ALL_CLIPS.filter(c => c.dbg);
CLIPS.forEach((c, id) => { c.id = id; });
const byName = Object.fromEntries(ALL_CLIPS.map(c => [c.name, c]));
const STANCE_IDS = {CROUCH: 0, UPRIGHT: 1};
// commands a clip applies on its own ticks: looks, hands, visibility state, stance, the sink offset, the follow list
function clipLines(c) {
  const at = new Map(), add = (t, l) => { if (!at.has(t)) at.set(t, []); at.get(t).push(l); };
  for (const [t, ch, lk] of c.look_events || []) add(t, `function ${NS}/look/${ch}/${lk}`);
  for (const ev of c.hand_events || []) add(ev[0], ev.length === 2 ? `function ${NS}/hands/${ev[1]}` : `function ${NS}/hand/${ev[1]}/${ev[2]}`);
  for (const [t, v] of c.state || []) add(t, `function ${NS}/state/${v}`);
  for (const [t, s] of c.stance_events || []) add(t, `scoreboard players set @s apRigStance ${STANCE_IDS[s]}`);
  // the full follow list one tick before a hidden span ends, so the parts never slide in from where they were left
  for (const [, b] of c.hidden || []) if (b < c.len - 1) add(b, F.listLines('all').join('\n'));
  const sink = c.sink ? F.sinkExtra(t => sinkAt(c, t), c.len) : null;
  return t => [...(at.get(t) || []).flatMap(l => l.split('\n')), ...(sink ? sink(t) : [])];
}
const clipInfo = [], motionErrors = [], poseErrors = [], warns = new Set(), extents = {}, keysPerTick = {};
for (const c of DBG_CLIPS) {
  const frames = clipFrames(c), chk = poseChecks(c, frames);
  poseErrors.push(...chk.errors);
  extents[c.name] = chk.extents;
  if (debugDp) frames.forEach((f, t) => putDebug(`ap_dbg/${c.name}/${t}`, PART_NAMES.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(f.d[n])}}`)));
}
for (const c of CLIPS) {
  if (c.keys[0][0] !== 0) throw new Error(`clip ${c.name}: first key must be tick 0`);
  if (c.keys[c.keys.length - 1][0] !== c.len) throw new Error(`clip ${c.name}: last key ${c.keys[c.keys.length - 1][0]} != len ${c.len}`);
  if (c.next && !byName[c.next]) throw new Error(`clip ${c.name}: unknown next ${c.next}`);
  const ks = accumulate(c), frames = clipFrames(c, ks);
  const chk = poseChecks(c, frames);
  poseErrors.push(...chk.errors);
  extents[c.name] = chk.extents;
  const r = (debugOf(c) ? debugCompiler : compiler).compileClip(c, frames, a => frame(c, a + .5, ks, frames[a]), clipLines(c));
  motionErrors.push(...r.motionErrors);
  r.warns.forEach(w => warns.add(w));
  if (Object.keys(chk.over).length) warns.add(`${c.name}: outside the ${CULL.width} x ${CULL.height} culling box by ${JSON.stringify(chk.over)}`);
  keysPerTick[c.name] = r3(r.info.keys / Math.max(1, c.len));
  // ---- manifest record (contract §0.4.4)
  const L = c.len, oAt = t => frames[Math.min(t, L)].o;
  const dyAt = t => sinkAt(c, t);
  const local = (P, t) => toLocal([P[0], P[1] + dyAt(t), P[2]]);
  const point = (name, t) => {
    const o = oAt(t), f = c.form;
    if (name === 'impact') {
      if (c.name === 'combo_b') return [0, 0, 4.8];
      if (c.name === 'combo_d') return [0, 0, 7.2];
      const P = carry(o, 'hood', [0, 3.0, -4.0]); return toLocal([P[0], 0, P[2]]);
    }
    if (name === 'muzzle') return local(carry(o, 'hood', [0, 3.0, -4.0]), t);
    if (name in FORM_POINTS) return local(modelPoint(o, M, f, ...FORM_POINTS[name][f]), t);
    if (name === 'ball') { const P = modelPoint(o, M, f, ...FORM_POINTS.crown[f]); P[1] += 1.5; return local(P, t); }
    const [b, P] = ANCHOR_POINTS[name]; return local(carry(o, b, P), t);
  };
  const anchors = Object.fromEntries(Object.entries(c.anchors || {}).map(([ev, pts]) => [ev, Object.fromEntries(pts.map(pt => [pt, point(pt, c.events[ev])]))]));
  const tracks = Object.fromEntries((c.tracks || []).map(tr => [tr, Array.from({length: L}, (_, t) => point(tr, t))]));
  // px: proxy columns per tick -> fitted keys (+ the mandatory ticks), every proxy in every key
  const samples = Array.from({length: L}, (_, t) => { const pp = proxyPoints(oAt(t)), dy = dyAt(t); return Object.fromEntries(Object.entries(pp).map(([k, v]) => [k, {...v, top: v.top ? Math.max(0, r2(v.top + dy)) : 0}])); });
  const fit = fitTracks(samples, {tol: {x: .15, z: .15, top: .3, default: 0}});
  const kt = new Set([0, L - 1]);
  for (const keys of Object.values(fit)) for (const [t] of keys) kt.add(t);
  for (const [a, b] of c.hidden || []) for (const t of [a - 1, a, b, b + 1]) if (t >= 0 && t <= L - 1) kt.add(t);
  for (const [t] of c.px_sets || []) if (t <= L - 1) kt.add(t);
  const pxKeys = Object.fromEntries([...kt].sort((a, b) => a - b).map(t => [String(t), Object.fromEntries(Object.entries(samples[t]).map(([k, v]) => [k, pxLocal(v)]))]));
  const tbl = CLIP_TABLE.find(x => x.name === c.name);
  clipInfo.push({
    id: c.id, name: c.name, len: L, authored: c.authored || L, loop: !!c.loop, next: c.next || null, mirror_of: null, retime: c.retime || [],
    events: c.events || {}, anchors, tracks, px: {lerp: true, keys: pxKeys}, yaw: denseYaw(c), hidden: (c.hidden || []).map(([a, b]) => [a, b, 'all']),
    root_z: [], state: c.state || [], extents: chk.extents, ...(Object.keys(chk.over).length ? {cull_overhang: chk.over} : {}), keyFiles: r.info.keyFiles, keys: r.info.keys,
    note: c.note || '', form: c.form, stance: {start: c.stance[0], end: c.stance[1]}, stance_events: c.stance_events || [], px_sets: c.px_sets || [[0, c.form === 'p1' ? 'p1' : 'p3c']],
    look_events: c.look_events || [], hand_events: c.hand_events || [],
    ...(c.keyed_pitch ? {keyed_pitch: c.keyed_pitch} : {}), ...(c.scale_in ? {scale_in: c.scale_in} : {}), ...(c.blend_in ? {blend_in: c.blend_in} : {}), ...(c.blend_out ? {blend_out: c.blend_out} : {}),
    ...(tbl ? {} : {})});
}
if (poseErrors.length) {
  const msg = 'pose checks:\n  ' + poseErrors.slice(0, +(arg("--show") || 60)).join('\n  ') + (poseErrors.length > 60 ? `\n  ... ${poseErrors.length} in all` : '');
  if (flag('--allow-steps')) console.warn(msg); else throw new Error(msg);
}
if (motionErrors.length) {
  const msg = 'part rotations above 120 degrees per tick or per key:\n  ' + motionErrors.slice(0, 80).join('\n  ');
  if (flag('--allow-steps')) console.warn(msg); else throw new Error(msg);
}
if (residErr.length) { const msg = 'R3 / §6.1 checks:\n  ' + residErr.join('\n  '); if (flag('--allow-steps')) console.warn(msg); else throw new Error(msg); }
compiler.writeDispatch(CLIPS);

// ---- runtime / API functions ----------------------------------------------------------------------------------------------------
const OBJ = ['apRigC', 'apRigT', 'apRigF', 'apRigY', 'apRigState', 'apRigForm', 'apRigStance', 'apRigFace', 'apRigCore', 'apRigGlow', 'apRigTint', 'apRigBright', 'apRigHands', 'apRigPark', ...F.objectives];
const FORM_IDS = {p1: 0, p3: 1}, FACE_IDS = {p1_bud: 0, p3_idle: 1, p3_charge: 2, p3_dim: 3, hidden: 4}, CORE_IDS = {p1_bulb: 0, p3_sternum: 1}, GLOW_IDS = {idle: 0, lit: 1}, BRIGHT_IDS = {13: 0, 15: 1};
const swap = (part, item) => `data modify entity ${uuidOf(part)} item.components."minecraft:item_model" set value "${itemId(item)}"`;
const brightLine = (part, b) => `data merge entity ${uuidOf(part)} {brightness:{block:${b},sky:15}}`;
const TAGS = n => ['rlk_room', 'rlk_mb_aux', 'rlk_mb_part', 'rlk_mb_apep_part', `rlk_mb_ap_${n}`];
// rest poses per form and stance (display transforms)
const restDisplay = (stance, f) => { const o = solve(stance === 'CROUCH' && f === 'p3' ? STANCES.CRAWL : STANCES[stance]); return Object.fromEntries(PART_NAMES.map(n => [n, toDisplay(n, o, M, f)])); };
const REST = {p1: {CROUCH: restDisplay('CROUCH', 'p1'), UPRIGHT: restDisplay('UPRIGHT', 'p1')}, p3: {CROUCH: restDisplay('CROUCH', 'p3'), UPRIGHT: restDisplay('UPRIGHT', 'p3')}};
const setPose = (pose, dur = 0) => PART_NAMES.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:${dur},transformation:${nbt(pose[n])}}`);
const hideAll = () => PART_NAMES.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:{scale:[0f,0f,0f]}}`);
const defaults = ['execute unless score @s apRigForm matches 0..1 run scoreboard players set @s apRigForm 0',
  'execute unless score @s apRigStance matches 0..1 run scoreboard players set @s apRigStance 0',
  'execute unless score @s apRigFace matches 0..4 run scoreboard players set @s apRigFace 0', 'execute unless score @s apRigCore matches 0..1 run scoreboard players set @s apRigCore 0',
  'execute unless score @s apRigGlow matches 0..1 run scoreboard players set @s apRigGlow 0', 'execute unless score @s apRigTint matches 0..4 run scoreboard players set @s apRigTint 0',
  'execute unless score @s apRigBright matches 0..1 run scoreboard players set @s apRigBright 0', 'execute unless score @s apRigHands matches 0..3 run scoreboard players set @s apRigHands 0',
  'execute unless score @s apRigState matches 0..1 run scoreboard players set @s apRigState 0', 'execute unless score @s apRigPark matches 0..1 run scoreboard players set @s apRigPark 0'];
fn('init', ['# Rig objectives. Safe to call on every load.', ...OBJ.map(o => `scoreboard objectives add ${o} dummy`)]);
fn('spawn', ['# @s = rig anchor (the boss body, on the floor under the thorax), positioned and rotated where the boss should appear.',
  `# Kills old parts, summons the ${PART_NAMES.length} parts (+ the shadow helper) in the rest pose of the stored form and stance and`,
  '# re-applies every stored look (apRig*), the visibility state and the park flag.',
  `function ${NS}/init`, `function ${NS}/kill`, ...defaults,
  ...PART_NAMES.map(n => summonPart({uuid: uuidInts(IDX[n]), tags: TAGS(n), item: itemId(`${FORM_MODELS[n] ? n + '_p1' : HAND_PARTS.includes(n) ? HAND_ITEMS[n][n[0] === 'a' ? 'p1_planted' : 'p1_open'] : n === 'face' ? 'face_p1_bud' : 'core_p1_bulb'}`),
    brightness: PART_BRIGHT[n], pose: REST.p1.CROUCH[n], viewRange: VIEW_RANGE, cull: CULL})),
  summonShadow({uuid: uuidInts(SHADOW_IDX), tags: ['rlk_room', 'rlk_mb_aux', 'rlk_mb_apep_part', 'rlk_mb_ap_shadow'], item: itemId(EMPTY), radius: 4.5, strength: .8, viewRange: VIEW_RANGE, cull: CULL}),
  'scoreboard players set @s apRigT -1', 'scoreboard players set @s apRigF 0', `scoreboard players set @s apRigC ${byName[STANCE_REST_CLIP('p1')].id}`,
  `function ${NS}/stance/apply`, `function ${NS}/look_apply`,
  `execute if score @s apRigState matches 1 run function ${NS}/state/burrowed`, `execute if score @s apRigPark matches 1 run function ${NS}/park_apply`,
  ...F.listLines('all').map(l => `execute unless score @s apRigState matches 1 unless score @s apRigPark matches 1 run ${l}`),
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow_now`]);
function STANCE_REST_CLIP(f) { return f === 'p1' ? 'idle_p1' : 'idle_p3'; }
fn('tick', ['# @s = rig anchor, at its feet. Once per game tick. Parked (R10): nothing runs. Missing parts respawn in the rest',
  '# pose of the stored form and stance with every stored look.',
  'execute if score @s apRigPark matches 1.. run return 0',
  `execute unless entity ${uuidOf('chest')} run function ${NS}/spawn`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow`,
  'scoreboard players add @s apRigT 1',
  `function ${NS}/run`,
  `execute if score @s apRigF matches 1.. run function ${NS}/flash_tick`]);
fn('kill', ['# Removes every rig part and the shadow helper.', 'kill @e[type=item_display,tag=rlk_mb_apep_part]']);
fn('uninstall', ['# Removes the rig and its objectives.', `function ${NS}/kill`, 'kill @e[type=marker,tag=rlk_mb_ap_face]', ...OBJ.map(o => `scoreboard objectives remove ${o}`)]);
// stances: snap to a rest pose (outside clips); stance/apply = the stored stance in the stored form
for (const [s, sid] of Object.entries(STANCE_IDS)) for (const f of ['p1', 'p3'])
  fn(`stance/r/${s.toLowerCase()}_${f}`, [`# Internal: the ${s} rest pose of the ${f} models.`, ...setPose(REST[f][s])]);
for (const [s, sid] of Object.entries(STANCE_IDS)) fn(`stance/${s.toLowerCase()}`, [`# Snap to the ${s} rest pose (outside clips) and store the stance. @s = rig anchor.`,
  `scoreboard players set @s apRigStance ${sid}`, `function ${NS}/stance/apply`]);
fn('stance/apply', ['# Internal: the stored stance (apRigStance) in the stored form (apRigForm).',
  ...Object.entries(STANCE_IDS).flatMap(([s, sid]) => Object.entries(FORM_IDS).map(([f, fid]) => `execute if score @s apRigStance matches ${sid} if score @s apRigForm matches ${fid} run function ${NS}/stance/r/${s.toLowerCase()}_${f}`))]);
// ---- looks (R12): internal refresh functions per channel x tint; the public look functions set the score and refresh
const TINTS = Object.keys(TINT_IDS);
for (const f of ['p1', 'p3']) for (const t of TINTS) fn(`look/r/form/${f}_${TINT_IDS[t]}`, [`# Internal: the ${f} models of every form part, tint ${t}.`, ...Object.keys(FORM_PART_ITEMS).map(p => swap(p, tintItem(FORM_PART_ITEMS[p][f], t)))]);
for (const [set, map] of Object.entries(HANDS_SET)) for (const t of TINTS) fn(`look/r/hands/${set}_${TINT_IDS[t]}`, [`# Internal: hand set ${set}, tint ${t}.`, ...Object.entries(map).map(([p, v]) => swap(p, tintItem(HAND_ITEMS[p][v], t)))]);
for (const look of Object.keys(FACE_IDS)) for (const t of TINTS) fn(`look/r/face/${look}_${TINT_IDS[t]}`, [`# Internal: face ${look}, tint ${t}.`, swap('face', look === 'hidden' ? EMPTY : tintItem(`face_${look}`, t))]);
for (const look of Object.keys(CORE_IDS)) for (const t of TINTS) fn(`look/r/core/${look}_${TINT_IDS[t]}`, [`# Internal: core ${look}, tint ${t}.`, swap('core', tintItem(`core_${look}`, t))]);
const tintTree = (ch, ids) => Object.entries(ids).flatMap(([lk, id]) => TINTS.map(t => `execute if score @s apRig${ch} matches ${id} if score @s apRigTint matches ${TINT_IDS[t]} run function ${NS}/look/r/${ch === 'Form' ? 'form' : ch === 'Hands' ? 'hands' : ch.toLowerCase()}/${lk}_${TINT_IDS[t]}`));
fn('look/r/form_apply', ['# Internal: the form models (apRigForm x apRigTint).', ...tintTree('Form', FORM_IDS)]);
fn('look/r/hands_apply', ['# Internal: the hand set (apRigHands x apRigTint).', ...tintTree('Hands', HAND_SET_IDS)]);
fn('look/r/face_apply', ['# Internal: the face (apRigFace x apRigTint).', ...tintTree('Face', FACE_IDS)]);
fn('look/r/core_apply', ['# Internal: the core (apRigCore x apRigTint).', ...tintTree('Core', CORE_IDS)]);
// brightness: own levels per form (crys 15 in phase 3), all 15 while lit (bright 15), the core glow
for (const f of ['p1', 'p3']) fn(`look/r/bright/${f}_13`, [`# Internal: every part at its own ${f} brightness.`, ...PART_NAMES.filter(n => n !== 'core').map(n => brightLine(n, f === 'p3' ? PART_BRIGHT_P3[n] : PART_BRIGHT[n]))]);
fn('look/r/bright/all_15', ['# Internal: every part at brightness 15 (the p3_lit charge).', ...PART_NAMES.filter(n => n !== 'core').map(n => brightLine(n, 15))]);
fn('look/r/bright_apply', ['# Internal: brightness from apRigBright x apRigForm, then the core glow.',
  `execute if score @s apRigBright matches 1 run function ${NS}/look/r/bright/all_15`,
  `execute if score @s apRigBright matches 0 if score @s apRigForm matches 0 run function ${NS}/look/r/bright/p1_13`,
  `execute if score @s apRigBright matches 0 if score @s apRigForm matches 1 run function ${NS}/look/r/bright/p3_13`,
  `execute if score @s apRigGlow matches 0 if score @s apRigBright matches 0 run ${brightLine('core', 12)}`,
  `execute if score @s apRigGlow matches 1 run ${brightLine('core', 15)}`, `execute if score @s apRigBright matches 1 run ${brightLine('core', 15)}`]);
fn('look_apply', ['# Re-applies every stored look: form, hands, face, core, tint (all through the per-tint items), brightness. @s = rig anchor.',
  `function ${NS}/look/r/form_apply`, `function ${NS}/look/r/hands_apply`, `function ${NS}/look/r/face_apply`, `function ${NS}/look/r/core_apply`, `function ${NS}/look/r/bright_apply`]);
const ALSO = {p1: {face: 'p1_bud', core: 'p1_bulb', hands: 'p1_rest', tint: 'none'}, p3: {face: 'p3_idle', core: 'p3_sternum', hands: 'p3_open', tint: 'none'}};
for (const [f, id] of Object.entries(FORM_IDS)) fn(`look/form/${f}`, [`# Form look ${f} (the CS white-out swap): every part's ${f} model; also face ${ALSO[f].face}, core ${ALSO[f].core}, hands ${ALSO[f].hands}, no tint. @s = rig anchor.`,
  `scoreboard players set @s apRigForm ${id}`, `scoreboard players set @s apRigFace ${FACE_IDS[ALSO[f].face]}`, `scoreboard players set @s apRigCore ${CORE_IDS[ALSO[f].core]}`,
  `scoreboard players set @s apRigHands ${HAND_SET_IDS[ALSO[f].hands]}`, 'scoreboard players set @s apRigTint 0', `function ${NS}/look_apply`]);
for (const [lk, id] of Object.entries(FACE_IDS)) fn(`look/face/${lk}`, [`# Face look ${lk}${lk === 'hidden' ? ' (the empty model: no glow through the crawl hood)' : ''}. @s = rig anchor.`, `scoreboard players set @s apRigFace ${id}`, `function ${NS}/look/r/face_apply`]);
for (const [lk, id] of Object.entries(CORE_IDS)) fn(`look/core/${lk}`, [`# Core look ${lk}. @s = rig anchor.`, `scoreboard players set @s apRigCore ${id}`, `function ${NS}/look/r/core_apply`]);
for (const [lk, id] of Object.entries(GLOW_IDS)) fn(`look/core_glow/${lk}`, [`# Core glow ${lk} (core brightness ${lk === 'idle' ? 12 : 15}). @s = rig anchor.`, `scoreboard players set @s apRigGlow ${id}`, `function ${NS}/look/r/bright_apply`]);
for (const [t, id] of Object.entries(TINT_IDS)) fn(`look/tint/${t}`, [`# Tint look ${t}${t === 'none' ? '' : ` (constant tint ${TINT_COLOR[t]} on every part of the ${TINT_FORMS[t].join('/')} models)`}. @s = rig anchor.`, `scoreboard players set @s apRigTint ${id}`, `function ${NS}/look_apply`]);
for (const [b, id] of Object.entries(BRIGHT_IDS)) {
  fn(`look/bright/${b}`, [`# Brightness ${b === '15' ? '15 on every part (the p3_lit charge)' : 'back to each part\'s own level'}. @s = rig anchor.`, `scoreboard players set @s apRigBright ${id}`, `function ${NS}/look/r/bright_apply`]);
  fn(`bright/${b}`, [`# = look/bright/${b}. @s = rig anchor.`, `function ${NS}/look/bright/${b}`]);
}
for (const [set, id] of Object.entries(HAND_SET_IDS)) fn(`hands/${set}`, [`# Hand set ${set} (R8). @s = rig anchor.`, `scoreboard players set @s apRigHands ${id}`, `function ${NS}/look/r/hands_apply`]);
for (const [p, vars] of Object.entries(HAND_ITEMS)) for (const v of Object.keys(vars)) fn(`hand/${p}/${v}`, [`# One hand: ${p} -> ${v} (the stored set is unchanged). @s = rig anchor.`,
  ...TINTS.map(t => `execute if score @s apRigTint matches ${TINT_IDS[t]} run ${swap(p, tintItem(vars[v], t))}`)]);
// visibility states: the scale-0 mask and the follow list (the clips own the poses)
fn('state/normal', ['# Normal visibility (the next clip key shows every part again). @s = rig anchor.', 'scoreboard players set @s apRigState 0', ...F.listLines('all')]);
fn('state/burrowed', ['# Burrowed: every part at scale 0, the parts stop following. @s = rig anchor.', 'scoreboard players set @s apRigState 1', ...hideAll(), ...F.listLines('burrowed')]);
// park (R10): built here on RIGLIB's static-anchor skip (contract §0.4.7, FN-25 fallback)
fn('park_apply', ['# Internal: the parked mask (every part at scale 0, the shadow off, no follow).', ...hideAll(), `data merge entity ${uuidOf('shadow')} {shadow_radius:0f}`, ...F.listLines('burrowed')]);
fn('park', ['# Park the body (phase 2, R10): every part at scale 0, the shadow off, rig/tick skipped; a respawn keeps the mask. @s = rig anchor.',
  'scoreboard players set @s apRigPark 1', `function ${NS}/park_apply`]);
fn('unpark', ['# Unpark: re-apply the form, the stance, every look and the follow. @s = rig anchor, at its feet.',
  'scoreboard players set @s apRigPark 0', `execute unless entity ${uuidOf('chest')} run function ${NS}/spawn`, `data merge entity ${uuidOf('shadow')} {shadow_radius:4.5f}`,
  `function ${NS}/look_apply`, `function ${NS}/stance/apply`, 'scoreboard players set @s apRigState 0', ...F.listLines('all'), 'scoreboard players set @s apRigT -1',
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow_now`]);
// hit flash: a warm white outline for 3 ticks on one part group (never all 49 parts at once)
const GROUPS = {
  head: ['neck', 'head', 'face', 'hood', 'crown', 'hair_l_1', 'hair_r_1', 'hair_l_2', 'hair_r_2'],
  body: ['chest', 'shoulders', 'core', 'crys_low', 'crys_back', 'mantle_l_a', 'mantle_r_a', 'mantle_l_b', 'mantle_r_b'],
  front: ['b_up_l', 'b_up_r', 'b_lo_l', 'b_lo_r', 'b_hand_l', 'b_hand_r', 'beads_l', 'beads_r'],
  rear: ['abdomen', 'hem_a', 'hem_b', 'c_up_l', 'c_up_r', 'c_lo_l', 'c_lo_r', 'c_hand_l', 'c_hand_r'],
  tail: [...TAIL_PARTS],
  arms: ['a_up_l', 'a_up_r', 'a_lo_l', 'a_lo_r', 'a_hand_l', 'a_hand_r'],
};
for (const [g, list] of Object.entries(GROUPS)) fn(`flash/${g}`, [`# Hit feedback on the ${g} group: a warm white outline for 3 ticks. @s = rig anchor.`, 'scoreboard players set @s apRigF 4', ...list.map(n => `data merge entity ${uuidOf(n)} {Glowing:1b,glow_color_override:16774620}`)]);
const ALL_FLASH = Object.values(GROUPS).flat();
fn('flash_tick', ['scoreboard players remove @s apRigF 1', `execute if score @s apRigF matches 0 run function ${NS}/flash_off`]);
fn('flash_off', ['# End of the hit flash. @s = rig anchor.', ...ALL_FLASH.map(n => `data merge entity ${uuidOf(n)} {Glowing:0b}`)]);
compiler.writeFace({marker: 'rlk_mb_ap_face', maxDeg: 2});

// ---- proxies, coverage gate (R7) --------------------------------------------------------------------------------------------------
const pxOf = o => proxyPoints(o);
function coverage(o, f, L) {
  // floor footprint of the parts a player can reach (lowest point <= 2.2 b), the standing ring 0.4 b outside it, the
  // distance from every standing point to the nearest proxy column (RT §5.5, rigtech_cover.py)
  const res = .1, X0 = -16, X1 = 16, Z0 = -16, Z1 = 16, nx = Math.round((X1 - X0) / res), nz = Math.round((Z1 - Z0) / res);
  const inside = new Uint8Array(nx * nz);
  const hull = pts => { const P = [...new Map(pts.map(p => [`${p[0].toFixed(3)},${p[1].toFixed(3)}`, p])).values()].sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    const cr = (o2, a, b) => (a[0] - o2[0]) * (b[1] - o2[1]) - (a[1] - o2[1]) * (b[0] - o2[0]); const lo = [], up = [];
    for (const p of P) { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], p) <= 0) lo.pop(); lo.push(p); }
    for (const p of [...P].reverse()) { while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], p) <= 0) up.pop(); up.push(p); }
    return [...lo.slice(0, -1), ...up.slice(0, -1)]; };
  for (const n of PART_NAMES) {
    const pts = partPoints(o, n, f, modelOfPart(n, L));
    if (!pts.length || Math.min(...pts.map(P => P[1])) > 2.2) continue;
    const H = hull(pts.map(P => [P[0], P[2]]));
    if (H.length < 3) continue;
    const bx = [Math.min(...H.map(p => p[0])), Math.max(...H.map(p => p[0]))], bz = [Math.min(...H.map(p => p[1])), Math.max(...H.map(p => p[1]))];
    for (let i = Math.max(0, Math.floor((bx[0] - X0) / res)); i <= Math.min(nx - 1, Math.ceil((bx[1] - X0) / res)); i++)
      for (let k = Math.max(0, Math.floor((bz[0] - Z0) / res)); k <= Math.min(nz - 1, Math.ceil((bz[1] - Z0) / res)); k++) {
        const x = X0 + (i + .5) * res, z = Z0 + (k + .5) * res;
        let ok = true;
        for (let m = 0; m < H.length && ok; m++) { const a = H[m], b = H[(m + 1) % H.length]; if ((b[0] - a[0]) * (z - a[1]) - (b[1] - a[1]) * (x - a[0]) < 0) ok = false; }
        if (ok) inside[i * nz + k] = 1;
      }
  }
  const dil = r => { const out = new Uint8Array(nx * nz); for (let i = 0; i < nx; i++) for (let k = 0; k < nz; k++) { if (!inside[i * nz + k]) continue;
    for (let di = -r; di <= r; di++) for (let dk = -r; dk <= r; dk++) if (di * di + dk * dk <= r * r) { const a = i + di, b = k + dk; if (a >= 0 && a < nx && b >= 0 && b < nz) out[a * nz + b] = 1; } } return out; };
  const d4 = dil(4), d3 = dil(3), cols = Object.values(pxOf(o)).filter(c => c.top > 0);
  let n = 0, hit = 0, worst = 0;
  for (let i = 0; i < nx; i++) for (let k = 0; k < nz; k++) if (d4[i * nz + k] && !d3[i * nz + k]) {
    const x = X0 + (i + .5) * res, z = Z0 + (k + .5) * res;
    const d = Math.min(...cols.map(c => Math.hypot(c.x - x, c.z - z)));
    n++; if (d <= 3.0) hit++; worst = Math.max(worst, d);
  }
  return {points: n, covered: n ? r3(hit / n) : 1, worst: r2(worst)};
}
const COVER = {};
for (const [nm, clip] of [['CROUCH', 'dbg_crouch'], ['UPRIGHT', 'dbg_upright'], ['HOOP', 'dbg_hoop'], ['CROUCH_OVER', 'dbg_crouch_over'], ['CRAWL', 'dbg_crawl']]) {
  const c = byName[clip], o = solve(sample(c, 0, accumulate(c)));
  COVER[nm] = coverage(o, c.form, lookAt(c, 0));
}
const coverFail = Object.entries(COVER).filter(([k, v]) => k !== 'CRAWL' && v.covered < 1);
if (coverFail.length) warns.add(`coverage gate (R7, 100 % within 3.0 b): ${coverFail.map(([k, v]) => `${k} ${(v.covered * 100).toFixed(1)} % (worst ${v.worst} b)`).join(', ')}`);

// ---- manifest -------------------------------------------------------------------------------------------------------------------
const restC = REF.CROUCH, restU = REF.UPRIGHT;
const anchorsOf = (o, f) => {
  const out = {};
  for (const [k, [b, P]] of Object.entries(ANCHOR_POINTS)) out[k] = toLocal(carry(o, b, P));
  for (const [k, v] of Object.entries(FORM_POINTS)) out[k] = toLocal(modelPoint(o, M, f, ...v[f]));
  return out;
};
const restAnchors = {CROUCH: anchorsOf(restC, 'p1'), UPRIGHT: anchorsOf(restU, 'p3')};
const pxRest = {CROUCH: Object.fromEntries(Object.entries(pxOf(restC)).map(([k, v]) => [k, pxLocal(v)])), UPRIGHT: Object.fromEntries(Object.entries(pxOf(restU)).map(([k, v]) => [k, pxLocal(v)]))};
const shown = (f) => {
  const L = restLook(f);
  return PART_NAMES.reduce((a, n) => a + (elementCount[modelOfPart(n, L)] || 0), 0);
};
const perRegion = {};
for (const n of PART_NAMES) { const r = PART_REGION[n]; perRegion[r] = perRegion[r] || {p1: 0, p3: 0}; for (const f of ['p1', 'p3']) perRegion[r][f] += elementCount[modelOfPart(n, restLook(f))] || 0; }
const perPart = Object.fromEntries(PART_NAMES.map(n => [n, {p1: elementCount[modelOfPart(n, restLook('p1'))] || 0, p3: elementCount[modelOfPart(n, restLook('p3'))] || 0}]));
const regionsPx = {};
for (const e of ledger) regionsPx[e.region] = (regionsPx[e.region] || 0) + e.px;
const regionsParts = {};
for (const n of PART_NAMES) regionsParts[PART_REGION[n]] = (regionsParts[PART_REGION[n]] || 0) + 1;
const budgetRegions = Object.fromEntries([...new Set([...Object.keys(regionsParts), ...Object.keys(regionsPx)])].map(r => [r, {parts: regionsParts[r] || 0, px: regionsPx[r] || 0}]));
const manifestPath = path.join(here, 'mboss_apep_rig_manifest.json');
const lastTextures = (() => { try { return JSON.parse(fs.readFileSync(manifestPath, 'utf8')).textures; } catch { return undefined; } })();
const fnId = n => `${NS}/${n}`;
const handVariants = Object.fromEntries(Object.entries(HAND_ITEMS));
const objectives = {apRigC: 'current clip id (anchor)', apRigT: 'tick of the pose shown this tick (-1 = queued)', apRigF: 'hit flash countdown', apRigY: 'face/track scratch',
  apRigState: 'visibility: 0 normal, 1 burrowed', apRigForm: 'form look: 0 p1, 1 p3', apRigStance: 'stance: 0 CROUCH, 1 UPRIGHT', apRigFace: 'face look: 0 p1_bud, 1 p3_idle, 2 p3_charge, 3 p3_dim, 4 hidden',
  apRigCore: 'core look: 0 p1_bulb, 1 p3_sternum', apRigGlow: 'core glow: 0 idle, 1 lit', apRigTint: 'tint: 0 none, 1 p1_dark, 2 p1_brown, 3 withered, 4 p3_dim',
  apRigBright: 'body brightness: 0 = own levels, 1 = 15', apRigHands: 'hand set: 0 p1_rest, 1 p1_lift, 2 p3_open, 3 p3_curl', apRigPark: '1 while parked',
  apRigFl: 'follow list (RIGLIB): 0 all, 1 burrowed', apRigFy: 'follow_y sink offset index (0 none)', apRigQ: 'static follow skip (RIGLIB)', apRigQx: 'static skip: last x', apRigQy: 'static skip: last y', apRigQz: 'static skip: last z', apRigQw: 'static skip: last yaw'};
for (const o of F.objectives) if (!objectives[o]) objectives[o] = 'RIGLIB follow';
const manifest = {
  schema: 1, boss: 'apep', source: 'rig', apep: 1,
  runtime: {ns: NS + '/', clip_obj: 'apRigC', tick_obj: 'apRigT', state_obj: 'apRigState', form_obj: 'apRigForm', stance_obj: 'apRigStance', face_obj: 'apRigFace', core_obj: 'apRigCore',
    glow_obj: 'apRigGlow', tint_obj: 'apRigTint', bright_obj: 'apRigBright', hands_obj: 'apRigHands', park_obj: 'apRigPark'},
  functions: {init: fnId('init'), spawn: fnId('spawn'), tick: fnId('tick'), kill: fnId('kill'), uninstall: fnId('uninstall'), look_apply: fnId('look_apply'),
    play: Object.fromEntries(CLIPS.map(c => [c.name, fnId('play/' + c.name)])), face: {player: fnId('face/player'), track: fnId('face/track'), set: fnId('face/set')},
    state: {normal: fnId('state/normal'), burrowed: fnId('state/burrowed')}, flash: Object.fromEntries(Object.keys(GROUPS).map(g => [g, fnId('flash/' + g)])),
    park: fnId('park'), unpark: fnId('unpark'), stance: {CROUCH: fnId('stance/crouch'), UPRIGHT: fnId('stance/upright')},
    hands: Object.fromEntries(Object.keys(HANDS_SET).map(s => [s, fnId('hands/' + s)])),
    hand: Object.fromEntries(Object.entries(HAND_ITEMS).map(([p, v]) => [p, Object.fromEntries(Object.keys(v).map(x => [x, fnId(`hand/${p}/${x}`)]))])),
    look: {form: Object.fromEntries(Object.keys(FORM_IDS).map(k => [k, fnId('look/form/' + k)])), face: Object.fromEntries(Object.keys(FACE_IDS).map(k => [k, fnId('look/face/' + k)])),
      core: Object.fromEntries(Object.keys(CORE_IDS).map(k => [k, fnId('look/core/' + k)])), core_glow: Object.fromEntries(Object.keys(GLOW_IDS).map(k => [k, fnId('look/core_glow/' + k)])),
      tint: Object.fromEntries(Object.keys(TINT_IDS).map(k => [k, fnId('look/tint/' + k)])), bright: Object.fromEntries(Object.keys(BRIGHT_IDS).map(k => [k, fnId('look/bright/' + k)]))},
    bright: {13: fnId('bright/13'), 15: fnId('bright/15')}},
  parts: PART_NAMES.map(n => ({name: n, region: PART_REGION[n], uuid: uuidOf(n), idx: IDX[n], tag: 'rlk_mb_ap_' + n,
    model: FORM_MODELS[n] ? n + '_p1' : HAND_PARTS.includes(n) ? HAND_ITEMS[n][n[0] === 'a' ? 'p1_planted' : 'p1_open'] : n === 'face' ? 'face_p1_bud' : 'core_p1_bulb',
    brightness: PART_BRIGHT[n], scale: PART_SCALE[n], elements: perPart[n].p1 || perPart[n].p3, parent: BONE[n].parent, tol_tp: TOL.tp[n] ?? TOL.t,
    ...(PART_BRIGHT_P3[n] !== PART_BRIGHT[n] ? {brightness_p3: PART_BRIGHT_P3[n]} : {}), reach: r2(1.5 * PART_SCALE[n]),
    frames: {p1: `${FRAMES[n].p1.ref} ${FRAMES[n].p1.kind}`, p3: `${FRAMES[n].p3.ref} ${FRAMES[n].p3.kind}`}})),
  shadow: {uuid: uuidOf('shadow'), idx: SHADOW_IDX, tag: 'rlk_mb_ap_shadow', shadow_radius: 4.5, shadow_strength: .8},
  uuids: {block: BLOCK, ints: INTS, parts: IDX, shadow: SHADOW_IDX, proxies: Object.fromEntries(PROXIES.map(([n], i) => [n, 0x41 + i])), props: {}},
  skeleton: {joints: Object.fromEntries(BONES.map(b => [b.name, b.j.map(r3)])), scale_H: 4.4,
    joints_by_stance: {CROUCH: Object.fromEntries(BONES.map(b => [b.name, restC[b.name].t.map(r3)])), UPRIGHT: Object.fromEntries(BONES.map(b => [b.name, restU[b.name].t.map(r3)]))},
    bones: Object.fromEntries(BONES.map(b => [b.name, {parent: b.parent, pose_only: b.po}]))},
  rest_anchors: restAnchors.CROUCH, torso_hw: 1.5,
  proxies: {layout: PROXIES.map(([name, part, flash, w, [gb, gp]], i) => ({name, part, point: gp.map(r3), w, top_margin: 0, tail_only: false, idx: 0x41 + i, uuid: BLOCK + hex2(0x41 + i), flash, plan: 'px_' + name, bone: gb})),
    rest: pxRest.CROUCH, rest_by_stance: pxRest, coverage: {within: 3.0, target: 1.0, poses: ['CROUCH', 'UPRIGHT', 'HOOP', 'CROUCH_OVER'], result: COVER},
    note: 'ground columns [x, f, top] (local: x = the boss left, f = forward); the per-clip tracks in clips[].px'},
  states: {
    p1: {px: PROXIES.map(p => p[0]), vis: 'normal', inv: false, capsules: ['sac', 'hips']}, p3u: {px: PROXIES.map(p => p[0]), vis: 'normal', inv: false, capsules: ['stem']},
    p3c: {px: PROXIES.map(p => p[0]), vis: 'normal', inv: false, capsules: ['sac', 'hips']}, burrowed: {px: [], vis: null, inv: true, capsules: []},
    aloft: {px: ['head', 'chest'], vis: 'normal', inv: false, capsules: [], tops: {head: 10, chest: 10}}, parked: {px: [], vis: null, inv: true, capsules: []},
    inv: {px: [], vis: null, inv: true, capsules: []}, dead: {px: [], vis: null, inv: true, capsules: []}},
  capsules: CAPSULES,
  flash_groups: GROUPS,
  looks: {
    form: {objective: 'apRigForm', ids: FORM_IDS, parts: FORM_PART_ITEMS, also: ALSO, brightness: {p3: Object.fromEntries(PART_NAMES.filter(n => PART_BRIGHT_P3[n] !== PART_BRIGHT[n]).map(n => [n, PART_BRIGHT_P3[n]]))},
      functions: Object.fromEntries(Object.keys(FORM_IDS).map(k => [k, fnId('look/form/' + k)]))},
    face: {objective: 'apRigFace', ids: FACE_IDS, parts: {face: Object.fromEntries(Object.keys(FACE_IDS).map(k => [k, k === 'hidden' ? null : `face_${k}`]))},
      functions: Object.fromEntries(Object.keys(FACE_IDS).map(k => [k, fnId('look/face/' + k)])), note: 'hidden = the empty model (the effect of scale 0, kept through the clip keys)'},
    core: {objective: 'apRigCore', ids: CORE_IDS, parts: {core: Object.fromEntries(Object.keys(CORE_IDS).map(k => [k, `core_${k}`]))}, functions: Object.fromEntries(Object.keys(CORE_IDS).map(k => [k, fnId('look/core/' + k)]))},
    core_glow: {objective: 'apRigGlow', ids: GLOW_IDS, brightness: {idle: {core: 12}, lit: {core: 15}}, functions: Object.fromEntries(Object.keys(GLOW_IDS).map(k => [k, fnId('look/core_glow/' + k)]))},
    tint: {objective: 'apRigTint', ids: TINT_IDS, colors: TINT_COLOR, forms: TINT_FORMS, item_pattern: '{model}_t{id}', slots: SLOTS, slot_colors: SLOT_COLOR, untinted_faces: untinted,
      functions: Object.fromEntries(Object.keys(TINT_IDS).map(k => [k, fnId('look/tint/' + k)]))},
    bright: {objective: 'apRigBright', ids: BRIGHT_IDS, brightness: {15: Object.fromEntries(PART_NAMES.map(n => [n, 15]))}, functions: Object.fromEntries(Object.keys(BRIGHT_IDS).map(k => [k, fnId('look/bright/' + k)]))},
  },
  tinted_items: tintedItems,
  clips: clipInfo,
  culling: {width: CULL.width, height: CULL.height, view_range: VIEW_RANGE},
  rest_extents: extents.dbg_crouch,
  budgets: {parts: PART_NAMES.length, part_cap: 56, models: Object.keys(models).length, hand_models: Object.values(HAND_ITEMS).reduce((a, v) => a + Object.keys(v).length, 0), items: itemCount,
    atlas_px: atlasPx, atlas_budget: ATLAS_BUDGET, elements_shown_rest: {p1: shown('p1'), p3: shown('p3')}, elements_budget: {p1: 7000, p3: 8000}, regions: budgetRegions},
  objectives,
  textures: sprites ? sprites.length : (typeof lastTextures === 'number' ? lastTextures : ledger.length),
  stances: {objective: 'apRigStance', ids: STANCE_IDS, default: {p1: 'CROUCH', p3: 'UPRIGHT'}, rest_anchors: restAnchors, torso_hw: {CROUCH: 1.5, UPRIGHT: 1.3},
    heights: {CROUCH: {hood_top: 4.4, crown_tip: 5.0, length: 15.0}, UPRIGHT: {hood_top: 8.5, face_low: 6.0, face_high: 7.85}},
    transitions: {stand_p3: {from: 'CROUCH', to: 'UPRIGHT'}, crouch_p3: {from: 'UPRIGHT', to: 'CROUCH'}}, px_set: {p1: {CROUCH: 'p1'}, p3: {CROUCH: 'p3c', UPRIGHT: 'p3u'}},
    residuals: {max: residMax, limit: .25, table: residuals}, hood_swing_deg: hoodSwing, upright_top: r2(hoodTopU), face_centre_upright: faceU.map(r2), sternum_centre_upright: coreU.map(r2),
    poses: {CROUCH: STANCES.CROUCH, UPRIGHT: STANCES.UPRIGHT, CRAWL: STANCES.CRAWL}},
  hands: {objective: 'apRigHands', parts: HAND_PARTS, variants: handVariants, sets: HANDS_SET, ids: HAND_SET_IDS,
    functions: {set: fnId('hands/<set>'), part: fnId('hand/<part>/<variant>')},
    pulse: PULSE},
  park: {objective: 'apRigPark', px_set: 'parked', shadow: false, tick: 'skip', respawn: 'keeps scale 0 while the flag is set', reapply: ['form', 'stance', 'looks', 'hands', 'follow'],
    functions: {park: fnId('park'), unpark: fnId('unpark')}},
  sprites: {budget: ATLAS_BUDGET, total: atlasPx, regions: regionsPx, ledger, planned: false, densities: {face: 64, crown: 64, b_hand: 64, hood: 48, default: 32}},
  elements: {budget: {p1: 7000, p3: 8000}, visible_rest: {p1: shown('p1'), p3: shown('p3')}, per_region: perRegion, per_part: perPart,
    densest: Object.entries(perPart).sort((a, b) => Math.max(b[1].p1, b[1].p3) - Math.max(a[1].p1, a[1].p3)).slice(0, 8).map(([n]) => n)},
  follow: F.info(), keys_per_tick: keysPerTick,
};
json(manifestPath, manifest);

// ---- report -----------------------------------------------------------------------------------------------------------------------
for (const w of [...warns].slice(0, 40)) console.warn('warn:', w);
const files = clipInfo.reduce((a, c) => a + c.keyFiles, 0);
console.log(`Built the Apep rig: ${PART_NAMES.length} parts, ${CLIPS.length} clips, ${files} key files, ${clipInfo.reduce((a, c) => a + c.keys, 0)} part keys, ${Object.keys(models).length} models, ${itemCount} items, ` +
  `${ledger.length} sprites (${(atlasPx / 1e6).toFixed(3)} M px), elements at rest p1 ${shown('p1')} / p3 ${shown('p3')}${warns.size ? `, ${warns.size} warnings` : ''}.`);
console.log(`R3 residuals (UPRIGHT vs model_p3 §6.2): max ${residMax} b over ${residuals.length} joints; hood swing ${hoodSwing} deg; upright top ${hoodTopU.toFixed(2)} b; face centre ${faceU.map(r2)}`);
console.log(`coverage (R7, within 3.0 b): ${Object.entries(COVER).map(([k, v]) => `${k} ${(v.covered * 100).toFixed(1)} %`).join(', ')}`);
console.log(`rest extents CROUCH x ${extents.dbg_crouch[0]}, y ${extents.dbg_crouch[1]}, z ${extents.dbg_crouch[2]}; UPRIGHT x ${extents.dbg_upright[0]}, y ${extents.dbg_upright[1]}, z ${extents.dbg_upright[2]}`);
if (flag('--part-extents')) for (const [st, f, o] of [['CROUCH', 'p1', REF.CROUCH], ['UPRIGHT', 'p3', REF.UPRIGHT]]) {
  console.log(`part extents ${st} (${f}): x / y / z min..max`);
  for (const n of PART_NAMES) { const P = partPoints(o, n, f, modelOfPart(n, restLook(f))); if (!P.length) continue; const e = [0, 1, 2].map(i => `${Math.min(...P.map(p => p[i])).toFixed(2)}..${Math.max(...P.map(p => p[i])).toFixed(2)}`); console.log(`  ${n.padEnd(11)} ${e.join('  ')}`); }
}
if (flag('--residuals')) for (const r of residuals) console.log(`  ${r.joint.padEnd(22)} ${r.d.toFixed(3)}  fk [${r.fk}] target [${r.target}]`);
if (debugDp) {
  const link = path.join(debugDp, 'data/rlk/function/mboss/apep/rig');
  fs.rmSync(link, {recursive: true, force: true});
  fs.mkdirSync(path.dirname(link), {recursive: true});
  fs.symlinkSync(rigDir, link);
  // look combinations for renders (models only, no scores): ap_dbg/look/<form>[_<tint>], faces, hand sets
  for (const f of ['p1', 'p3']) for (const t of TINTS) {
    if (t !== 'none' && !TINT_FORMS[t].includes(f)) continue;
    const hs = f === 'p1' ? 'p1_rest' : 'p3_open', face = f === 'p1' ? 'p1_bud' : 'p3_idle', core = f === 'p1' ? 'p1_bulb' : 'p3_sternum';
    putDebug(`ap_dbg/look/${f}${t === 'none' ? '' : '_' + t}`, [`function ${NS}/look/r/form/${f}_${TINT_IDS[t]}`, `function ${NS}/look/r/hands/${hs}_${TINT_IDS[t]}`,
      `function ${NS}/look/r/face/${face}_${TINT_IDS[t]}`, `function ${NS}/look/r/core/${core}_${TINT_IDS[t]}`]);
  }
  for (const lk of Object.keys(FACE_IDS)) putDebug(`ap_dbg/face/${lk}`, [`function ${NS}/look/r/face/${lk}_0`]);
  for (const s of Object.keys(HANDS_SET)) putDebug(`ap_dbg/hands/${s}`, [`function ${NS}/look/r/hands/${s}_0`]);
  putDebug('ap_dbg/crawl_look', [`function ${NS}/look/r/form/p3_0`, `function ${NS}/look/r/hands/p3_curl_0`, `function ${NS}/look/r/face/hidden_0`, `function ${NS}/look/r/core/p3_sternum_0`]);
  // a 0.6 x 1.8 b player reference in front of the hood (crouch) and one beside the left B hand
  const ref = (x, z) => `summon minecraft:item_display ^${x} ^ ^${z} {Tags:["rlk_ap_ref"],item_display:"none",transformation:{translation:[0f,0.9f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:ap_ref/player"}}}`;
  putDebug('ap_dbg/player_ref', ['# renders: a 1.8 b player 1.5 b in front of the hood and one beside the left B hand', ref(0, 5.8), ref(4.4, 3.6)]);
  putDebug('ap_dbg/player_front', ['# renders: a 1.8 b player 4 b in front of the anchor (the P3 fighting distance)', ref(0, 4.0)]);
  putDebug('ap_dbg/player_far', ['# renders: a 1.8 b player 6.5 b in front of the anchor (the reference camera frames)', ref(0, 6.5)]);
  // proxy columns and capsules overlay (thin translucent columns): ap_dbg/px/<pose>
  // x / z in the local frame (left, forward: contract §0.4.2), placed with ^left ^up ^forward
  const col = (x, z, w, top, tag, item) => `summon minecraft:item_display ^${x} ^ ^${z} {Tags:["rlk_ap_ref","${tag}"],item_display:"none",transformation:{translation:[0f,${(top / 2).toFixed(3)}f,0f],left_rotation:[0f,0f,0f,1f],scale:[${(w / 1).toFixed(3)}f,${top.toFixed(3)}f,${(w / 1).toFixed(3)}f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:ap_ref/${item}"}}}`;
  for (const [nm, clip] of [['CROUCH', 'dbg_crouch'], ['UPRIGHT', 'dbg_upright'], ['HOOP', 'dbg_hoop'], ['CROUCH_OVER', 'dbg_crouch_over']]) {
    const c = byName[clip], o = solve(sample(c, 0, accumulate(c)));
    putDebug(`ap_dbg/px/${nm.toLowerCase()}`, Object.values(pxOf(o)).map(v => col(v.x, -v.z, v.w, v.top, 'rlk_ap_px', 'px')));
  }
  for (const [nm, caps] of [['crouch', ['sac', 'hips']], ['upright', ['stem']]])
    putDebug(`ap_dbg/caps/${nm}`, caps.map(k => { const cp = CAPSULES[k]; return col(0, cp.col.f, 2 * cp.col.r, 3.0, 'rlk_ap_cap', 'cap'); }));
  // the burrow sink for the offline renderer: every part moved down by dy (the follow_y offset the rig applies)
  for (const dy of [1, 1.75, 2, 3.5, 4, 5.25]) putDebug(`ap_dbg/sink/${String(dy).replace('.', '_')}`, [`execute as @e[tag=rlk_mb_apep_part] at @s run tp @s ~ ~-${dy} ~`]);
  const rpRef = path.join(debugDp, 'rp_ref/assets/rlk');
  for (const [n, rgba] of [['player', [60, 120, 210, 255]], ['px', [240, 70, 70, 110]], ['cap', [70, 200, 240, 90]]]) {
    fs.mkdirSync(path.join(rpRef, 'textures/ap_ref'), {recursive: true});
    const buf = Buffer.alloc(16 * 16 * 4); for (let i = 0; i < 256; i++) buf.set(rgba, i * 4);
    fs.writeFileSync(path.join(rpRef, `textures/ap_ref/${n}.png`), png(16, 16, buf));
    const el = n === 'player' ? abox([-4.8, -14.4, -2.4], [4.8, 14.4, 2.4], 'ref') : abox([-8, -8, -8], [8, 8, 8], 'ref');
    json(path.join(rpRef, `models/item/ap_ref/${n}.json`), {textures: {ref: `rlk:ap_ref/${n}`}, elements: [el]});
    json(path.join(rpRef, `items/ap_ref/${n}.json`), {model: {type: 'minecraft:model', model: `rlk:item/ap_ref/${n}`}});
  }
  json(path.join(debugDp, 'rp_ref/pack.mcmeta'), {pack: {pack_format: 46, description: 'Apep render references'}});
  fs.mkdirSync(path.join(rpRef, '../minecraft/atlases'), {recursive: true});
  json(path.join(rpRef, '../minecraft/atlases/items.json'), {sources: ['player', 'px', 'cap'].map(n => ({type: 'minecraft:single', resource: `rlk:ap_ref/${n}`}))});
}
void [REGION_OF, J, POSE_ONLY, fitTracks, r3];
