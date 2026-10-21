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
//   tools/mboss_azhdaha_rig_manifest.json (schema v1 of scratchpad az/contract/manifest.md: the 41 clips with their events,
//       anchors, tail tracks, proxy-column keys, yaw schedules, hidden spans, root offsets and states; parts, UUIDs, looks,
//       the framework's proxy layout, state sets and push capsules, budgets, objectives)
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
//     (the body parts at scale 0; the tail clips raise the chain). The clips carry the poses and their hidden spans; the
//     clips call state/<name> at their recorded state ticks (respawns restore it) and select the follow list of each
//     span (RIGLIB createRigFollow: all / tail / none, with the static-anchor skip).
//   * Clips (R3a, azhdaha_clips.mjs): the 41 clips of plan.md §3.2 baked into dense played-tick keys; the anchor yaw of the
//     turns and the tail whips is the module's, by the schedule exported in the manifest.
//   * Hit proxies (plan.md R5, §3.3): the rig publishes the 12 ground columns per clip (manifest `px` keys); the framework
//     owns the interaction entities.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {paintAzhdahaTextures, spriteId, azhdahaSprites, azhdahaSpriteSizes, spriteRegions, ATLAS_BUDGET} from './azhdaha_paint.mjs';
import {partModels, checkBounds, PARTS, LOOKS, TINTED, LOOK_BRIGHT, EMPTY, REGION_OF, CULL_BOX} from './azhdaha_geometry.mjs';
import {solve, toDisplay, PART_SCALE, TAIL_PARTS, proxyPoints, PROXIES, pointOf, J, SOLE} from './azhdaha_pose.mjs';
import {CLIPS, CLIP_TABLE, TABLE, RESPAWN_CLIP, TRACK_CLIPS, accumulate, sampleClip as sample, restPose} from './azhdaha_clips.mjs';
import {add, rot} from './mboss_rig_math.mjs';
import {createRigCompiler, nbt, summonPart, summonShadow, createRigFollow, cullOverhang, fitTracks} from './mboss_rig_compile.mjs';
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
// Part names stay out of the module's rlk_mb_az_* tag space (contract manifest.md §3, s2.md §12) and the rig's own tags
// (rlk_mb_az_shadow, rlk_mb_az_face, rlk_mb_az_g_<region>).
for (const [n] of PARTS) {
  if (!/^[a-z][a-z0-9_]*$/.test(n)) throw new Error(`part name ${n}: lower-case letters, digits and _`);
  if (/^(p\d|x|ap_|fld|lock|kept|pat|orbc|seal|g_)/.test(n) || ['shadow', 'face'].includes(n)) throw new Error(`part name ${n} collides with the module / rig tag space`);
}
// Per-region budgets (plan.md §3.1; atlas px rebalanced by plan change note 1): parts and painted sprite px per region,
// the material tiles shared by several regions as their own line. The totals (R3 part cap, R8 atlas) are asserted too.
const REGION_BUDGET = {head: {parts: 8, px: .24e6}, body: {parts: 14, px: .42e6}, legs: {parts: 16, px: .32e6}, tail: {parts: 10, px: .16e6}, shared: {parts: 0, px: .06e6}};
const regionParts = Object.fromEntries(Object.keys(REGION_BUDGET).map(r => [r, PARTS.filter(p => p[3] === r).length]));
for (const [r, k] of Object.entries(regionParts)) if (k > REGION_BUDGET[r].parts) throw new Error(`region ${r}: ${k} parts (budget ${REGION_BUDGET[r].parts})`);
for (const [n, , , r] of PARTS) if (!REGION_BUDGET[r] || r === 'shared') throw new Error(`part ${n}: unknown region ${r}`);
// Fixed, append-only part name -> UUID low byte (Rig decision change 3; contract cm.md §14): R1's order head 1 ... tip 46,
// then the parts added in R2 in R3's merge order (tail_skirt 47). Never renumber or reuse an index; a new part takes the
// next free one. Parts 0x01-0x3F; 0x40 is the shadow helper, 0x41-0x50 the hit proxies (pose PROXIES order), 0x60-0x8F
// module props.
const UUID_INDEX = {
  head: 1, jaw: 2, eyes: 3, horn_l: 4, horn_r: 5, beard1: 6, beard2: 7,
  chest: 8, belly: 9, pelvis: 10, neck1: 11, neck2: 12, apron: 13, glow_apron: 14,
  plates_neck: 15, plates_sh: 16, plates_mid: 17, plates_hip: 18, crys_sh: 19, crys_mid: 20, crys_hip: 21,
  uarm_l: 22, bracer_l: 23, paw_l: 24, uarm_r: 25, bracer_r: 26, paw_r: 27,
  thigh_l: 28, gaiter_l: 29, foot_l: 30, thigh_r: 31, gaiter_r: 32, foot_r: 33,
  glow_bracer_l: 34, glow_bracer_r: 35, glow_gaiter_l: 36, glow_gaiter_r: 37,
  t1: 38, t2: 39, t3: 40, t4: 41, t5: 42, t6: 43, t7: 44, t8: 45, tip: 46,
  tail_skirt: 47,
};
const PROXY_BASE = 0x41, SHADOW_INDEX = 0x40;
{
  const seen = new Map();
  for (const [n, i] of Object.entries(UUID_INDEX)) {
    if (!(Number.isInteger(i) && i >= 1 && i <= 0x3F)) throw new Error(`UUID table: ${n} -> ${i} outside 0x01-0x3F`);
    if (seen.has(i)) throw new Error(`UUID table: ${n} and ${seen.get(i)} share index ${i}`);
    seen.set(i, n);
  }
  for (const [n] of PARTS) if (!UUID_INDEX[n]) throw new Error(`part ${n} has no UUID index: append it to UUID_INDEX (next free ${Math.max(...seen.keys()) + 1})`);
  if (PROXIES.length > 16) throw new Error(`${PROXIES.length} hit proxies: at most 16 (cm.md pxBase + 15)`);
}
const PART_INDEX = Object.fromEntries(PARTS.map(([n]) => [n, UUID_INDEX[n]]));
const uuidOf = n => `524c4b4d-415a-4400-8000-${PART_INDEX[n].toString(16).padStart(12, '0')}`;
const uuidInts = n => `[I;1380731725,1096434688,-2147483648,${PART_INDEX[n]}]`;
const SHADOW_UUID = '524c4b4d-415a-4400-8000-000000000040', SHADOW_INTS = '[I;1380731725,1096434688,-2147483648,64]';
const itemId = m => `rlk:mboss/azhdaha/${m}`;
const CULL = {width: 30, height: 12}, VIEW_RANGE = 3;
const cullOf = n => CULL_BOX[n] || CULL;   // per-part boxes (the distal tail: azhdaha_tail.mjs CULL_BOX)

// ---- resource pack: textures, models, item definitions ---------------------------------------------------------------------
const ALL_SPRITES = Object.keys(azhdahaSprites());     // every defined sprite (constructed before the models, as always)
const models = partModels();
for (const [name, els] of Object.entries(models)) checkBounds(name, els);
// only the sprites some model shows are painted and enter the atlas (R3: 7 R1 material tiles and one ledge sprite
// were left unused by the R2 regions)
const USED = new Set(Object.values(models).flatMap(els => els.flatMap(e => Object.values(e.faces).map(f => f.texture.slice(1)))));
const unusedSprites = ALL_SPRITES.filter(n => !USED.has(n));
const sprites = flag('--no-paint') ? null : paintAzhdahaTextures(rp, arg('--paint') ? arg('--paint').split(',') : null, USED);
const modelDir = path.join(assets, 'models/item/mboss/azhdaha'), itemDir = path.join(assets, 'items/mboss/azhdaha');
fs.rmSync(modelDir, {recursive: true, force: true});
fs.rmSync(itemDir, {recursive: true, force: true});
const spriteTable = azhdahaSpriteSizes(USED);
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
const SPRITE_REGION = spriteRegions();
const regionPx = Object.fromEntries(Object.keys(REGION_BUDGET).map(r => [r, 0]));
for (const [n, [w, h]] of Object.entries(spriteTable)) regionPx[SPRITE_REGION[n]] += w * h;
for (const [r, px] of Object.entries(regionPx)) if (px > REGION_BUDGET[r].px) throw new Error(`region ${r}: ${px} sprite px (budget ${REGION_BUDGET[r].px / 1e6} M)`);
const elementCount = Object.fromEntries(Object.entries(models).map(([n, e]) => [n, e.length]));
// Elements shown at once (client cost, rigtech.md §2.2: about 6-8 k for a detailed dragon) in every look combination.
const ELEMENT_BUDGET = 8000;
const itemElements = item => elementCount[item] ?? elementCount[(TINTED[item] || [])[0]] ?? 0;
const shownIn = (lg, tl) => PARTS.reduce((a, [n, m]) => a + itemElements((LOOKS.legs[n] || {})[lg] || (LOOKS.tail[n] || {})[tl] || m), 0);
const elementsByLook = {};
for (const lg of ['geo', 'hydro', 'pyro']) for (const tl of ['geo', 'cryo', 'electro']) elementsByLook[`${lg}_${tl}`] = shownIn(lg, tl);
const elementsMax = Math.max(...Object.values(elementsByLook));
if (elementsMax > ELEMENT_BUDGET) throw new Error(`${elementsMax} elements shown at once (budget ${ELEMENT_BUDGET}): ${JSON.stringify(elementsByLook)}`);
const regionElements = Object.fromEntries(['head', 'body', 'legs', 'tail'].map(r => [r, PARTS.filter(p => p[3] === r).reduce((a, [, m]) => a + (elementCount[m] || 0), 0)]));

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
const n3 = x => +x.toFixed(3) || 0;
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
// Pose checks (every frame of every clip): no horizontal root travel and no root yaw (the module moves and turns the
// anchor), except the root z offset of a hidden body (Rig decision change 1: allowed only on ticks where no body part,
// i.e. no non-tail part, is shown); every shown part inside its culling box (the radial check of the shared
// cullOverhang: the box is world-aligned and does not turn with the yaw; buried points do not count); the soles of the
// feet on or above the floor unless the rig is buried or the clip frees the floor (airborne / sinking spans); the hidden
// spans of the clip (contract manifest.md §4.6) exactly: "all" = every part at scale 0, "body" = every non-tail part at
// scale 0 and the tail shown, and every part with a model shown outside them.
const BODY_PARTS = PARTS.map(([n]) => n).filter(n => !TAIL_PARTS.includes(n));
const SHOWN_PARTS = PARTS.filter(([, m]) => m !== EMPTY).map(([n]) => n);
function poseChecks(c, frames) {
  const out = [], over = {}, rootZ = [];
  let ext = [[Infinity, -Infinity], [Infinity, -Infinity], [Infinity, -Infinity]];
  const span = t => (c.hidden || []).find(([a, b]) => t >= a && t <= b);
  const free = t => (c.floorFree || []).some(([a, b]) => t >= a && t <= b);
  frames.forEach((f, t) => {
    if (Math.abs(f.p.pos[0]) > 1e-9) out.push(`${c.name} t${t}: root x travel ${f.p.pos[0]} (must be 0)`);
    if (Math.abs(f.p.rot[1]) > 1e-9) out.push(`${c.name} t${t}: root yaw ${f.p.rot[1]} (must be 0: the module turns the anchor)`);
    const shownBody = BODY_PARTS.filter(n => f.o[n].s[0] > 1e-4);
    if (Math.abs(f.p.pos[2]) > 1e-9) {
      if (shownBody.length) out.push(`${c.name} t${t}: root z offset ${f.p.pos[2]} while body parts are shown (${shownBody.slice(0, 3).join(', ')}...; Rig decision change 1)`);
      if (t < c.len) rootZ.push([t, n3(-f.p.pos[2])]);
    }
    for (const [n] of PARTS) for (const P of partCorners(f.o, n, MODEL_OF_PART[n])) {
      for (let i = 0; i < 3; i++) { ext[i][0] = Math.min(ext[i][0], P[i]); ext[i][1] = Math.max(ext[i][1], P[i]); }
      // culling-box overhang (blocks past the box): recorded, not fatal (the box is plan.md R4's 30 x 12, per part for the distal tail)
      const o = cullOverhang(P, cullOf(n));
      if (o > 0) over[n] = Math.max(over[n] || 0, +o.toFixed(2));
    }
    if (f.p.pos[1] >= -.6 && !free(t) && !span(t)) for (const n of ['paw_l', 'paw_r', 'foot_l', 'foot_r']) {
      const y = pointOf(f.o, n, [0, n.startsWith('paw') ? SOLE.paw : SOLE.foot, 0])[1];
      if (y < -.08) out.push(`${c.name} t${t}: ${n} sole ${y.toFixed(2)} b below the floor`);
    }
    if (t < c.len) {
      const sp = span(t), hiddenParts = SHOWN_PARTS.filter(n => f.o[n].s[0] < 1e-4);
      const want = !sp ? [] : sp[2] === 'all' ? SHOWN_PARTS : sp[2] === 'body' ? SHOWN_PARTS.filter(n => !TAIL_PARTS.includes(n)) : SHOWN_PARTS.filter(n => TAIL_PARTS.includes(n));
      // inside a span more parts may hide (contract §4.6: e.g. the tail under the floor while the root moves), never fewer
      const extra = sp ? [] : hiddenParts, missing = want.filter(n => !hiddenParts.includes(n));
      if (missing.length) out.push(`${c.name} t${t}: hidden span ${sp[2]} but ${missing.slice(0, 3).join(', ')} shown`);
      if (extra.length) out.push(`${c.name} t${t}: ${extra.slice(0, 3).join(', ')} at scale 0 outside a hidden span of that kind`);
    }
  });
  // events: the binding table (contract §5), inside 0..len
  const T = TABLE[c.name];
  if (T) {
    for (const [e, t] of Object.entries(T.events)) if (c.events[e] !== t) out.push(`${c.name}: event ${e} at ${c.events[e]}, the table says ${t}`);
    if (Object.keys(c.events).length !== Object.keys(T.events).length) out.push(`${c.name}: events ${Object.keys(c.events)} vs the table ${Object.keys(T.events)}`);
  }
  for (const [e, t] of Object.entries(c.events || {})) if (!(t >= 0 && t <= c.len)) out.push(`${c.name}: event ${e} at ${t} outside 0..${c.len}`);
  // root_z spans [t0, t1, dz] (inclusive; dz in the local frame, + = forward; contract manifest.md §4.7)
  const spans = [];
  for (const [t, dz] of rootZ) { const s = spans[spans.length - 1]; if (s && s[1] === t - 1 && s[2] === dz) s[1] = t; else spans.push([t, t, dz]); }
  return {errors: out, over, rootZ: spans, extents: ext.every(([a, b]) => isFinite(a) && isFinite(b)) ? ext.map(([a, b]) => [+a.toFixed(2), +b.toFixed(2)]) : null};  // null: nothing visible in the whole clip
}

// ---- follow (RIGLIB createRigFollow): per-state lists (all / tail-only / none while burrowed) and the static-anchor skip ---------
const FOLLOW_LIST = {normal: 'all', tail_only: 'tail', burrowed: 'none'};
const F = createRigFollow({ns: NS, obj: 'azRig', fn, uuidOf: n => (n === 'shadow' ? SHADOW_UUID : uuidOf(n)),
  lists: {all: PARTS.map(([n]) => n), tail: PARTS.map(([n]) => n).filter(n => TAIL_PARTS.includes(n)), none: []}, fixed: ['shadow'], staticSkip: true,
  comment: '# Parts (and the shadow helper) follow the anchor position and yaw (run as and rotated as the anchor, pitch 0); the list is the body state\'s (azRigFl: 0 all, 1 tail, 2 none), skipped while the anchor stands still.'});
F.write();

// ---- compile clips --------------------------------------------------------------------------------------------------------------
const debugDp = arg('--debug-dp') && path.resolve(arg('--debug-dp'));
const debugClips = (arg('--debug-clips') || '').split(',').filter(Boolean);
const debugOf = c => debugDp && (debugClips.includes('all') || debugClips.includes(c.name));
if (debugDp) fs.rmSync(path.join(debugDp, 'data/rlk/function/az_dbg'), {recursive: true, force: true});
const putDebug = (n, lines) => put(path.join(debugDp, 'data/rlk/function', n + '.mcfunction'), lines.join('\n'));
// Tolerances: translation 0.012 b (0.03 b on the long tail segments and the torso masses, RIGLIB tol.tp); rotation per
// part (long parts tighter: a tail segment 2 b long turned 0.5 degree moves its tip 0.017 b).
const TOL = {t: .012, s: .015, rDefault: 1.0, r: {chest: .4, belly: .4, pelvis: .4, plates_sh: .4, plates_mid: .4, plates_hip: .5, crys_sh: .5, crys_mid: .5,
  t1: .3, t2: .3, t3: .35, t4: .4, t5: .45, t6: .5, t7: .55, t8: .6, tip: .7, horn_l: .6, horn_r: .6, head: .6},
  tp: Object.fromEntries(['t3', 't4', 't5', 't6', 't7', 't8', 'tip', 'pelvis', 'belly', 'plates_mid', 'plates_hip'].map(n => [n, .02]))};
const swapLine = (part, model) => `data modify entity ${uuidOf(part)} item.components."minecraft:item_model" set value "${itemId(model)}"`;
const mkCompiler = debug => createRigCompiler({ns: NS, obj: 'azRig', fn, parts: PARTS.map(([n]) => n), uuidOf, tol: TOL, swapLine,
  debug: debug ? {put: putDebug, dir: 'az_dbg'} : null});
const compiler = mkCompiler(false), debugCompiler = debugDp ? mkCompiler(true) : null;
CLIPS.forEach((c, id) => { c.id = id; });
const byName = Object.fromEntries(CLIPS.map(c => [c.name, c]));
for (const [name] of CLIP_TABLE) if (!byName[name]) throw new Error(`clip ${name} of the table is missing`);
CLIP_TABLE.forEach(([name], i) => { if (byName[name].id !== i) throw new Error(`clip ${name}: id ${byName[name].id}, the table order wants ${i}`); });
// commands a clip runs on its own ticks (extraLines of the compiler, after the keys): the recorded body state (contract
// §4.6; a state at t = len applies at the hand-over, i.e. on the next clip's tick 0 through its stateCalls), the follow list
// of each hidden span (selected at its first tick; the full list again two ticks before its last tick), the list of tick
// 0, and the gold flare of the gold_on / gold_off events (glow/gold_*).
// Why two ticks (a real-client timing, 10-21c): the key of tick b already starts the parts' scale-up toward tick b + 1
// (interpolation 1), and the follow runs at the start of the rig tick, so a list selected at b moved the parts only at
// b + 1 (teleport_duration 1: they arrived at b + 2). The client then showed the surfacing body for a tick or two where
// the parts were left (the dive spot, the pre-B3 spot) and slid it over. Selected at b - 2, the follow at b - 1 moves
// the still invisible parts, and they sit on the anchor when they scale up.
function clipLines(c) {
  const at = new Map(), add = (t, ...l) => { if (t < 0 || t > c.len) return; if (!at.has(t)) at.set(t, []); at.get(t).push(...l); };
  const sp0 = (c.hidden || []).find(([a]) => a === 0);
  add(0, ...F.listLines(sp0 ? (sp0[2] === 'body' ? 'tail' : 'none') : 'all'));
  for (const [a, b, kind] of c.hidden || []) {
    if (a > 0) add(a, ...F.listLines(kind === 'body' ? 'tail' : 'none'));
    if (b < c.len - 1) add(Math.max(a, b - 2), ...F.listLines('all'));
  }
  for (const [t, st] of [...(c.state || []), ...(c.stateCalls || [])]) if (t < c.len) add(t, `function ${NS}/state/${st}`);
  for (const [ev, what] of c.gold || []) add(c.events[ev], `function ${NS}/glow/gold_${what}`);
  return t => at.get(t) || [];
}
const clipInfo = [], motionErrors = [], poseErrors = [], warns = new Set(), extents = {}, framesOf = {};
for (const c of CLIPS) {
  if (c.keys[0][0] !== 0) throw new Error(`clip ${c.name}: first key must be tick 0`);
  if (c.keys[c.keys.length - 1][0] !== c.len) throw new Error(`clip ${c.name}: last key ${c.keys[c.keys.length - 1][0]} != len ${c.len}`);
  if (c.next && !byName[c.next]) throw new Error(`clip ${c.name}: unknown next ${c.next}`);
  const ks = accumulate(c), frames = clipFrames(c, ks);
  framesOf[c.name] = frames;
  const chk = poseChecks(c, frames);
  poseErrors.push(...chk.errors);
  extents[c.name] = chk.extents;
  const r = (debugOf(c) ? debugCompiler : compiler).compileClip(c, frames, a => frame(c, a + .5, ks, frames[a]), clipLines(c));
  motionErrors.push(...r.motionErrors);
  r.warns.forEach(w => warns.add(w));
  if (Object.keys(chk.over).length) warns.add(`${c.name}: outside the culling box (${CULL.width} x ${CULL.height}; per part for the distal tail) by ${JSON.stringify(chk.over)}`);
  c._chk = chk; c._r = r;
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

// ---- the manifest records of the clips (contract manifest.md §4; local frame x = s, y up, z = f: local = (x, y, -z)) ---------
const loc = P => [n3(P[0]), n3(P[1]), n3(-P[2])];
const flr = P => [n3(P[0]), 0, n3(-P[2])];
// named points (bone-local, rig frame): the muzzle tip (nose), the chin (the floor point under it is the chin-slam impact),
// the end of the leafy tip, the dorsal launch area, the four spike launch points (the gold crystal clusters' tips), the soles
const NAMED = {nose: ['head', [0, -1.0, -1.42]], chin: ['jaw', [0, -1.08, -1.11]], tip_end: ['tip', [0, -.35, 1.45]], back: ['belly', [0, .65, -.1]],
  launch_1: ['crys_sh', [1.2, 2.2, -.4]], launch_2: ['crys_sh', [-1.2, 2.2, -.4]], launch_3: ['crys_mid', [1.1, 2.4, .2]], launch_4: ['crys_mid', [-1.1, 2.4, .2]],
  paw_fl: ['paw_l', [0, SOLE.paw, 0]], paw_fr: ['paw_r', [0, SOLE.paw, 0]], foot_hl: ['foot_l', [0, SOLE.foot, 0]], foot_hr: ['foot_r', [0, SOLE.foot, 0]]};
const PAW_POINT = {fl: 'paw_fl', fr: 'paw_fr', hl: 'foot_hl', hr: 'foot_hr'};
const named = (o, n) => pointOf(o, NAMED[n][0], NAMED[n][1]);
// the tail root: the t1 joint; while it is under the floor and the tail shows (the tail-only pillar), where the chain
// leaves the floor
function tailRoot(o) {
  const T = o.t1.t;
  if (T[1] >= 0 || o.t1.s[0] < 1e-4) return T;
  const pts = [o.t1.t, o.t2.t, o.t3.t, o.t4.t, o.t5.t, o.t6.t, o.t7.t, o.t8.t, o.tip.t, named(o, 'tip_end')];
  for (let i = 1; i < pts.length; i++) if (pts[i][1] >= 0) { const a = pts[i - 1], b = pts[i], u = -a[1] / (b[1] - a[1]); return [a[0] + (b[0] - a[0]) * u, 0, a[2] + (b[2] - a[2]) * u]; }
  return T;
}
function pointAt(c, name, t) {
  const o = framesOf[c.name][Math.min(t, c.len)].o;
  if (name === 'tail_root') return loc(tailRoot(o));
  if (name === 'tail_tip') return loc(named(o, 'tip_end'));
  if (name === 'impact') return flr(named(o, 'chin'));
  if (name === 'paw') return flr(named(o, PAW_POINT[c.plants[Object.keys(c.plants).find(e => c.events[e] === t)] || 'fl']));
  return loc(named(o, name));
}
// proxy columns [x, z, top] (local; top 0 = hidden bone or under the floor)
const PXN = PROXIES.map(p => p[0]);
function pxCols(o) {
  const out = {};
  for (const [nm, part, at, , top] of PROXIES) {
    const v = o[part], P = add(v.t, rot(v.q, at)), hidden = v.s[0] < 1e-3;
    out[nm] = {x: n3(P[0]), z: n3(-P[2]), top: hidden ? 0 : n3(Math.max(0, P[1] + top))};
  }
  return out;
}
const mirrorPx = cols => Object.fromEntries(Object.entries(cols).map(([n, v]) => [{paw_l: 'paw_r', paw_r: 'paw_l', foot_l: 'foot_r', foot_r: 'foot_l'}[n] || n, [n3(-v[0]), v[1], v[2]]]));
const mirrorPt = v => [n3(-v[0]), v[1], v[2]];
function clipRecord(c) {
  const L = c.len, frames = framesOf[c.name];
  const anchors = {};
  for (const [ev, pts] of Object.entries(c.anchors || {})) anchors[ev] = Object.fromEntries(pts.map(pt => [pt, pointAt(c, pt, c.events[ev])]));
  for (const ev of Object.keys(c.plants || {})) if (c.events[ev] !== undefined) anchors[ev] = {...(anchors[ev] || {}), paw: pointAt(c, 'paw', c.events[ev])};
  const tracks = c.tracks ? {tail_root: Array.from({length: L}, (_, t) => pointAt(c, 'tail_root', t)), tail_tip: Array.from({length: L}, (_, t) => pointAt(c, 'tail_tip', t))} : {};
  // px: fitted keys (tol 0.1 b, contract §4.4) + tick 0, len-1 and the hidden-span edges; every proxy in every key
  const samples = Array.from({length: L}, (_, t) => pxCols(frames[t].o));
  const fit = fitTracks(samples, {tol: .1});
  const kt = new Set([0, L - 1]);
  for (const keys of Object.values(fit)) for (const [t] of keys) kt.add(t);
  for (const [a, b] of c.hidden || []) for (const t of [a - 1, a, b, b + 1]) if (t >= 0 && t <= L - 1) kt.add(t);
  const keys = Object.fromEntries([...kt].sort((a, b) => a - b).map(t => [String(t), Object.fromEntries(PXN.map(n => [n, [samples[t][n].x, samples[t][n].z, samples[t][n].top]]))]));
  return {id: c.id, name: c.name, len: L, authored: c.authoredLen || L, loop: !!c.loop, next: c.next || null, mirror_of: c.mirror_of || null, retime: c.retime || [],
    events: {...c.events}, anchors, tracks, px: {lerp: true, keys}, yaw: c.yaw || null, hidden: (c.hidden || []).map(h => [...h]), root_z: c._chk.rootZ, state: (c.state || []).map(s => [...s]),
    extents: c._chk.extents, cull_overhang: Object.keys(c._chk.over).length ? c._chk.over : null, keyFiles: c._r.info.keyFiles, keys: c._r.info.keys, note: c.note || ''};
}
const records = Object.fromEntries(CLIPS.map(c => [c.name, clipRecord(c)]));
// mirrors: the records of the source mirrored exactly (s negated, names swapped, yaw negated); the mirror's own pose must agree
for (const c of CLIPS.filter(x => x.mirror_of)) {
  const src = records[c.mirror_of], own = records[c.name];
  let worst = 0;
  for (const [t, cols] of Object.entries(src.px.keys)) {
    const m = mirrorPx(cols), o = own.px.keys[t] || Object.fromEntries(Object.entries(pxCols(framesOf[c.name][+t].o)).map(([n, v]) => [n, [v.x, v.z, v.top]]));
    for (const n of PXN) worst = Math.max(worst, ...m[n].map((v, i) => Math.abs(v - o[n][i])));
  }
  if (worst > .08) throw new Error(`mirror ${c.name}: its own proxy columns differ from the mirrored ${c.mirror_of} by ${worst.toFixed(3)} b`);
  records[c.name] = {...own, px: {lerp: true, keys: Object.fromEntries(Object.entries(src.px.keys).map(([t, cols]) => [t, mirrorPx(cols)]))},
    anchors: Object.fromEntries(Object.entries(src.anchors).map(([ev, pts]) => [ev, Object.fromEntries(Object.entries(pts).map(([k, v]) => [k, mirrorPt(v)]))])),
    tracks: src.tracks.tail_root ? {tail_root: src.tracks.tail_root.map(mirrorPt), tail_tip: src.tracks.tail_tip.map(mirrorPt)} : {},
    yaw: src.yaw ? src.yaw.map(v => +(-v).toFixed(2) || 0) : null, mirror_check: +worst.toFixed(3)};
}
// contract checks the module relies on (manifest.md §4.4 / §4.6 / §4.7 / §5 pose notes)
{
  const errs = [];
  const chin = records.chin_slam;
  for (let t = 35; t <= 55; t++) { const v = pxCols(framesOf.chin_slam[t].o).head.top; if (v > 3.5) errs.push(`chin_slam t${t}: head column top ${v} > 3.5 (the head must stay low 35-55)`); }
  for (const nm of ['p3_sink', 'tail_pillar', 'tail_pillar_strike', 'tail_pillar_sink']) {
    const r = records[nm];
    for (const [t, cols] of Object.entries(r.px.keys)) {
      if ((nm === 'p3_sink' && +t < 40) || (nm === 'tail_pillar_sink' && +t >= 18)) continue;
      for (const k of ['tail1', 'tail2', 'tail3', 'tail4']) if (Math.hypot(cols[k][0], cols[k][1]) > .3) errs.push(`${nm} t${t}: ${k} column ${Math.hypot(cols[k][0], cols[k][1]).toFixed(2)} b off the anchor (tail-only: stacked within 0.3 b)`);
      for (const k of PXN.filter(k => !k.startsWith('tail'))) if (cols[k][2] !== 0) errs.push(`${nm} t${t}: body proxy ${k} not hidden in the tail-only state`);
    }
    // the pillar base (where the tail leaves the floor) on the anchor
    for (let t = 0; t < r.len; t++) { if ((nm === 'p3_sink' && t < 58) || (nm === 'tail_pillar_sink' && t >= 10)) continue; const b = r.tracks.tail_root[t]; if (Math.hypot(b[0], b[2]) > .3 || Math.abs(b[1]) > .05) errs.push(`${nm} t${t}: pillar base ${b} not on the anchor`); }
  }
  for (const r of Object.values(records)) if (r.tracks.tail_root && r.tracks.tail_root.length !== r.len) errs.push(`${r.name}: tracks with ${r.tracks.tail_root.length} entries`);
  for (const nm of TRACK_CLIPS) if (!records[nm].tracks.tail_root) errs.push(`${nm}: no tail tracks`);
  if (errs.length) { const msg = 'contract checks:\n  ' + errs.slice(0, 40).join('\n  '); if (flag('--allow-steps')) console.warn(msg); else throw new Error(msg); }
  void chin;
}

// ---- API functions ------------------------------------------------------------------------------------------------------------
const REST = (() => { const o = solve(restPose()); return Object.fromEntries(PARTS.map(([n]) => [n, toDisplay(n, o[n])])); })();
const REGION_TAG = n => `rlk_mb_az_g_${REGION_OF[n]}`;
const TAGS = n => `["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_azhdaha_part","rlk_mb_az_${n}","${REGION_TAG(n)}"]`;
const summon = ([n, model, bright], pose) => summonPart({uuid: uuidInts(n), tags: TAGS(n), item: itemId(model), brightness: bright, pose, viewRange: VIEW_RANGE, cull: cullOf(n)});
const SHADOW_R = 4.5;
const shadowSummon = summonShadow({uuid: SHADOW_INTS, tags: ['rlk_room', 'rlk_mb_aux', 'rlk_mb_azhdaha_part', 'rlk_mb_az_shadow'], item: itemId(EMPTY), radius: SHADOW_R, strength: .8, viewRange: VIEW_RANGE, cull: CULL});
const RIG_OBJ = ['azRigC', 'azRigT', 'azRigF', 'azRigY', 'azRigLegs', 'azRigTail', 'azRigState', ...F.objectives];
fn('init', ['# Rig objectives. Safe to call on every load.', ...RIG_OBJ.map(o => `scoreboard objectives add ${o} dummy`)]);
const setPose = (pose, dur = 0) => PARTS.map(([n]) => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:${dur},transformation:${nbt(pose[n])}}`);
const stored = ['execute unless score @s azRigLegs matches 0..2 run scoreboard players set @s azRigLegs 0',
  'execute unless score @s azRigTail matches 0..2 run scoreboard players set @s azRigTail 0',
  'execute unless score @s azRigState matches 0..2 run scoreboard players set @s azRigState 0'];
// The clip a (re)spawn queues per stored body state (contract manifest.md §4.6: a respawn restores the state): idle, or
// the looping clip that holds the hidden state.
const STATE_IDS = {normal: 0, burrowed: 1, tail_only: 2};
for (const [s, n] of Object.entries(RESPAWN_CLIP)) {
  const c = byName[n];
  if (!c) throw new Error(`respawn clip ${n} of state ${s} missing`);
  if (s !== 'normal' && !(c.loop && (c.hidden || []).some(([a, b, k]) => a === 0 && b === c.len - 1 && k === (s === 'burrowed' ? 'all' : 'body')))) throw new Error(`respawn clip ${n} does not hold the state ${s} on every tick`);
}
fn('spawn', ['# @s = rig anchor (the boss body, on the floor under the centre of the four feet), positioned and rotated where the',
  `# boss should appear. Kills old parts, summons the ${PARTS.length} parts in the rest pose (+ the shadow helper), re-applies the`,
  '# stored element looks (azRigLegs, azRigTail) and the body state (azRigState: its visibility, follow list and shadow), and',
  `# queues the clip that holds that state (normal: ${RESPAWN_CLIP.normal}, burrowed: ${RESPAWN_CLIP.burrowed}, tail-only: ${RESPAWN_CLIP.tail_only}).`,
  `function ${NS}/init`, `function ${NS}/kill`, ...stored, ...PARTS.map(p => summon(p, REST[p[0]])), shadowSummon,
  'scoreboard players set @s azRigT -1', 'scoreboard players set @s azRigF 0',
  ...Object.entries(STATE_IDS).map(([s, i]) => `execute if score @s azRigState matches ${i} run scoreboard players set @s azRigC ${byName[RESPAWN_CLIP[s]].id}`),
  `function ${NS}/look_apply`, ...Object.entries(STATE_IDS).map(([s, i]) => `execute if score @s azRigState matches ${i} run function ${NS}/state/${s}`),
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow_now`]);
fn('tick', ['# @s = rig anchor, at its feet. Once per game tick. Missing parts respawn (stored looks and body state kept; see spawn).',
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
// body states: the scale-0 masks (the clips own the poses; these record the state, hide what must not show, select the follow
// list and size the ground shadow: none underground, a small one under the tail pillar)
const hideParts = list => list.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:{scale:[0f,0f,0f]}}`);
const nonTail = PARTS.map(([n]) => n).filter(n => !TAIL_PARTS.includes(n));
const shadowR = r => `data merge entity ${SHADOW_UUID} {shadow_radius:${r}f}`;
fn('state/normal', ['# Normal body state (the clip keys show every part). @s = rig anchor. The parts are brought to the anchor at once',
  '# (follow_now): a module state change (a cancelled burrow, px/state normal) shows them right after this.',
  'scoreboard players set @s azRigState 0', ...F.listLines('all'), shadowR(SHADOW_R),
  `execute at @s rotated as @s rotated ~ 0 run function ${NS}/follow_now`]);
fn('state/burrowed', ['# Burrowed (underground): every part at scale 0 until a clip shows them, no follow, no shadow. @s = rig anchor.', 'scoreboard players set @s azRigState 1',
  ...hideParts(PARTS.map(([n]) => n)), ...F.listLines('none'), shadowR(0)]);
fn('state/tail_only', ['# Tail-only (the phase-3 pillar): the body parts at scale 0, the tail chain shown by the tail clips, only the tail follows. @s = rig anchor.',
  'scoreboard players set @s azRigState 2', ...hideParts(nonTail), ...F.listLines('tail'), shadowR(1.2)]);
// hit flash: a warm white outline for 3 ticks on one part group (rigtech.md §2.6: never all 46 parts at once)
const GROUPS = {head: ['head', 'jaw', 'horn_l', 'horn_r'], front: ['chest', 'neck1', 'neck2', 'apron', 'uarm_l', 'uarm_r', 'bracer_l', 'bracer_r', 'paw_l', 'paw_r'],
  rear: ['belly', 'pelvis', 'thigh_l', 'thigh_r', 'gaiter_l', 'gaiter_r', 'foot_l', 'foot_r', 'tail_skirt'], tail: ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 'tip']};
for (const [g, list] of Object.entries(GROUPS)) {
  fn(`flash/${g}`, [`# Hit feedback on the ${g} group: a warm white outline for 3 ticks. @s = rig anchor.`, 'scoreboard players set @s azRigF 4', ...list.map(n => `data merge entity ${uuidOf(n)} {Glowing:1b,glow_color_override:16774620}`)]);
}
// Gold (plan.md §3.5, contract manifest.md §7): the horns and the gold crystal clusters are matte (block 13, like the
// hide) in every phase; glow/gold_on lifts them to 15 for the 천동만상 tell and the absorbs, glow/gold_off restores 13.
// The eyes stay red at 15 in every look. No look channel touches these parts, so their level is always the base level.
const GOLD = ['horn_l', 'horn_r', 'crys_sh', 'crys_mid', 'crys_hip'];
const GOLD_RIM = 16762960;    // #FFC850, the petrify rim pulse
for (const n of GOLD) {
  if (BASE_BRIGHT[n] !== 13) throw new Error(`gold part ${n}: brightness ${BASE_BRIGHT[n]}, matte gold is 13`);
  if (LOOKS.legs[n] || LOOKS.tail[n]) throw new Error(`gold part ${n} is in a look channel (glow/gold_off restores the base level)`);
}
if (BASE_BRIGHT.eyes !== 15 || Object.values(LOOK_BRIGHT).some(ch => Object.values(ch).some(l => 'eyes' in l))) throw new Error('the eyes stay at 15 in every look');
fn('glow/gold_on', ['# Gold flare (the 천동만상 tell, the absorbs; the spikes / absorb / absorb_p3 clips call it at gold_on): horns and gold crystals 13 -> 15. Not stored: re-call after a respawn. @s = rig anchor.',
  ...GOLD.map(n => `data merge entity ${uuidOf(n)} {brightness:{block:15,sky:15}}`)]);
fn('glow/gold_off', ['# Gold back to matte (13; the clips call it at gold_off). @s = rig anchor.', ...GOLD.map(n => `data merge entity ${uuidOf(n)} {brightness:{block:${BASE_BRIGHT[n]},sky:15}}`)]);
// Death seal (plan.md §3.5 / §5 death t96): both channels back to the base (geo) looks and stored so, every part 3 levels
// darker (block and sky, so the dimming shows by day as well), and a gold rim pulse on the gold parts for 12 ticks
// (the hit-flash countdown azRigF ends it through flash_off).
fn('look/petrify', ['# Death seal: the base looks at brightness -3 and a 12-tick gold rim pulse. A respawn restores the base looks at full',
  '# brightness (call look/petrify again). @s = rig anchor.',
  `function ${NS}/look/legs/geo`, `function ${NS}/look/tail/geo`,
  ...PARTS.map(([n]) => `data merge entity ${uuidOf(n)} {brightness:{block:${BASE_BRIGHT[n] - 3},sky:12}}`),
  ...GOLD.map(n => `data merge entity ${uuidOf(n)} {Glowing:1b,glow_color_override:${GOLD_RIM}}`),
  'scoreboard players set @s azRigF 13']);
const ALL_FLASH = [...new Set([...Object.values(GROUPS).flat(), ...GOLD])];
fn('flash_tick', ['scoreboard players remove @s azRigF 1', `execute if score @s azRigF matches 0 run function ${NS}/flash_off`]);
fn('flash_off', ['# End of the hit flash (and of the petrify rim pulse). @s = rig anchor.', ...ALL_FLASH.map(n => `data merge entity ${uuidOf(n)} {Glowing:0b}`)]);
compiler.writeFace({marker: 'rlk_mb_az_face', maxDeg: 2});

// ---- manifest (schema v1, contract manifest.md) -------------------------------------------------------------------------------
const restO = solve(restPose());
const manifestPath = path.join(here, 'mboss_azhdaha_rig_manifest.json');
const lastTextures = (() => { try { return JSON.parse(fs.readFileSync(manifestPath, 'utf8')).textures; } catch { return undefined; } })();
const shownElements = PARTS.reduce((a, [, m]) => a + (elementCount[m] || 0), 0);
const NSF = NS + '/';
const CLIP_NAMES = CLIP_TABLE.map(([n]) => n);
const functions = {
  init: NSF + 'init', spawn: NSF + 'spawn', tick: NSF + 'tick', kill: NSF + 'kill', uninstall: NSF + 'uninstall', look_apply: NSF + 'look_apply',
  play: Object.fromEntries(CLIP_NAMES.map(n => [n, `${NSF}play/${n}`])), play_dbg: Object.fromEntries(CLIPS.filter(c => c.dbg).map(c => [c.name, `${NSF}play/${c.name}`])),
  face: {player: NSF + 'face/player', track: NSF + 'face/track', set: NSF + 'face/set'},
  state: Object.fromEntries(Object.keys(STATE_IDS).map(s => [s, `${NSF}state/${s}`])),
  look_legs: Object.fromEntries(Object.keys(LOOK_IDS.legs).map(l => [l, `${NSF}look/legs/${l}`])), look_tail: Object.fromEntries(Object.keys(LOOK_IDS.tail).map(l => [l, `${NSF}look/tail/${l}`])),
  petrify: NSF + 'look/petrify', glow_on: NSF + 'glow/gold_on', glow_off: NSF + 'glow/gold_off',
  flash: Object.fromEntries(Object.keys(GROUPS).map(g => [g, `${NSF}flash/${g}`])),
  follow: NSF + 'follow', follow_now: NSF + 'follow_now',
};
// the frozen proxy layout (contract §6.1): bones, widths, margins, flash groups; idx = 0x41 + position
const PX_FLASH = {head: 'head', chest: 'front', belly: 'rear', hips: 'rear', tail1: 'tail', tail2: 'tail', tail3: 'tail', tail4: 'tail', paw_l: 'front', paw_r: 'front', foot_l: 'rear', foot_r: 'rear'};
// proxies.rest: the §6.1 rest columns, which the contract pins (check_az_manifest.py compares them to 0.01 b). The head,
// paw and foot points reproduce them exactly; the R2 tail carries its tail high over the back, so the real idle tail
// columns differ from the pinned R1 numbers: they are in proxies.rest_pose and in every clip's px keys.
const PX_REST_PINNED = {head: [0, 4.3, 3.05], chest: [0, 2.1, 4.85], belly: [0, -.5, 4.85], hips: [0, -3.4, 4.2], tail1: [0, -6.35, 3.94], tail2: [0, -10.12, 3.9],
  tail3: [0, -12.86, 5.81], tail4: [0, -11.9, 8.51], paw_l: [3.15, 2.95, 2.8], paw_r: [-3.15, 2.95, 2.8], foot_l: [2.5, -2.55, 2.92], foot_r: [-2.5, -2.55, 2.92]};
const restCols = pxCols(restO);
for (const n of ['head', 'chest', 'belly', 'hips', 'paw_l', 'paw_r', 'foot_l', 'foot_r']) {
  const r = restCols[n], w = PX_REST_PINNED[n];
  if (Math.abs(r.x - w[0]) > .011 || Math.abs(r.z - w[1]) > .011 || Math.abs(r.top - w[2]) > .011) throw new Error(`proxy ${n}: rest column ${[r.x, r.z, r.top]} != the contract's ${w}`);
}
const restAnchors = {nose: loc(named(restO, 'nose')), head_col: [restCols.head.x, 0, restCols.head.z], head_front: [restCols.head.x, 0, n3(restCols.head.z + 2.5)],
  chest: [restCols.chest.x, 0, restCols.chest.z], hips: [restCols.hips.x, 0, restCols.hips.z], tail_root: loc(restO.t1.t),
  paw_fl: flr(named(restO, 'paw_fl')), paw_fr: flr(named(restO, 'paw_fr')), foot_hl: flr(named(restO, 'foot_hl')), foot_hr: flr(named(restO, 'foot_hr')), back: loc(named(restO, 'back'))};
json(manifestPath, {
  schema: 1, boss: 'azhdaha', source: 'rig',
  runtime: {ns: NSF, clip_obj: 'azRigC', tick_obj: 'azRigT', state_obj: 'azRigState', legs_obj: 'azRigLegs', tail_obj: 'azRigTail'},
  functions,
  parts: PARTS.map(([n, m, b, r]) => ({name: n, region: r, uuid: uuidOf(n), idx: PART_INDEX[n], tag: 'rlk_mb_az_' + n, model: m, brightness: b, scale: PART_SCALE[n], elements: elementCount[m]})),
  shadow: {uuid: SHADOW_UUID, tag: 'rlk_mb_az_shadow', shadow_radius: SHADOW_R, note: 'empty-model helper under the anchor, not a rig part; radius 0 while burrowed, 1.2 under the tail pillar'},
  uuids: {block: '524c4b4d-415a-4400-8000-0000000000', ints: [1380731725, 1096434688, -2147483648], parts: UUID_INDEX, shadow: SHADOW_INDEX,
    proxies: Object.fromEntries(PROXIES.map(([nm], k) => [nm, PROXY_BASE + k])), props: {seal_prism: 0x80, crater: 0x81},
    note: 'Rig decision change 3 / cm.md §14: the part table is fixed and append-only; proxies take 0x41 + their position in proxies.layout'},
  skeleton: {joints: J, scale_H: 7, frame: 'rig (+x left, +y up, +z back)'},
  rest_anchors: restAnchors,
  torso_hw: 3.0,
  proxies: {layout: PROXIES.map(([name, part, at, w, top, flags], k) => ({name, part, point: at, w, top_margin: top, tail_only: flags === 'tail_only', idx: PROXY_BASE + k, uuid: `524c4b4d-415a-4400-8000-0000000000${(PROXY_BASE + k).toString(16)}`, flash: PX_FLASH[name]})),
    rest: PX_REST_PINNED, rest_pose: Object.fromEntries(PXN.map(n => [n, [restCols[n].x, restCols[n].z, restCols[n].top]])),
    note: 'ground columns [x, z, top] in the local frame (x = the boss left, z = forward, top above the floor incl. the margin, 0 = parked); rest = the contract §6.1 numbers (pinned), rest_pose = the R3a idle columns; per clip in clips[].px'},
  states: {normal: {px: PXN, vis: 'normal', inv: false, capsules: ['torso', 'head']}, jump: {px: [], vis: null, inv: false, capsules: []}, inv: {px: [], vis: null, inv: true, capsules: []},
    tail_only: {px: ['tail1', 'tail2', 'tail3', 'tail4'], vis: 'tail_only', inv: false, capsules: []}, dead: {px: [], vis: null, inv: true, capsules: []}},
  capsules: {torso: {f0: -3.8, f1: 2.6, hw: 2.8}, head: {f0: 2.6, f1: 5.4, hw: 1.6, px: 'head', top_max: 3.5}},
  rig_states: {objective: 'azRigState', ids: STATE_IDS, respawn_clip: RESPAWN_CLIP, follow_list: FOLLOW_LIST, follow: F.info()},
  flash_groups: GROUPS,
  looks: {...Object.fromEntries(Object.entries(LOOK_IDS).map(([ch, ids]) => [ch, {objective: obj[ch], ids, parts: LOOKS[ch], brightness: LOOK_BRIGHT[ch]}])),
    gold: {parts: GOLD, brightness: 13, glow: 15}, eyes: {part: 'eyes', brightness: 15},
    functions: {legs: functions.look_legs, tail: functions.look_tail, petrify: functions.petrify, glow_on: functions.glow_on, glow_off: functions.glow_off}},
  tinted_items: Object.fromEntries(Object.entries(TINTED).map(([k, [m, c]]) => [k, {model: m, tint: '#' + c.toString(16).padStart(6, '0')}])),
  clips: CLIPS.map(c => records[c.name]),
  culling: {width: CULL.width, height: CULL.height, view_range: VIEW_RANGE},
  culling_per_part: CULL_BOX,
  rest_extents: extents.idle,
  budgets: {parts: PARTS.length, part_budget: '44-48 (cap 56)', models: Object.keys(models).length, elements_all_models: Object.values(elementCount).reduce((a, b) => a + b, 0),
    elements_shown_rest: shownElements, elements_shown_max: elementsMax, elements_shown_by_look: elementsByLook, element_budget: ELEMENT_BUDGET, atlas_px: atlasPx, atlas_budget: ATLAS_BUDGET,
    sprites: Object.keys(spriteTable).length,
    regions: Object.fromEntries(Object.entries(REGION_BUDGET).map(([r, b]) => [r, {parts: regionParts[r], parts_budget: b.parts, px: regionPx[r], px_budget: b.px, ...(regionElements[r] !== undefined ? {elements_rest: regionElements[r]} : {})}]))},
  objectives: {azRigC: 'current clip id (anchor)', azRigT: 'tick within the clip (anchor; -1 = queued by play)', azRigF: 'hit flash countdown', azRigY: 'face/track scratch',
    azRigLegs: 'legs look: 0 geo, 1 hydro, 2 pyro', azRigTail: 'tail look: 0 geo, 1 cryo, 2 electro', azRigState: 'body state: 0 normal, 1 burrowed, 2 tail-only',
    azRigFl: 'follow list: 0 all, 1 tail, 2 none (RIGLIB)', azRigQ: 'static follow skip (RIGLIB)', azRigQx: 'static skip: last x', azRigQy: 'static skip: last y', azRigQz: 'static skip: last z', azRigQw: 'static skip: last yaw'},
  textures: sprites ? sprites.length : (typeof lastTextures === 'number' ? lastTextures : 'not repainted'),
});
for (const w of [...warns].slice(0, 40)) console.warn('warn:', w);
const files = CLIPS.reduce((a, c) => a + c._r.info.keyFiles, 0);
console.log(`Built the Azhdaha rig: ${PARTS.length} parts, ${CLIPS.length} clips (${CLIP_NAMES.length} + ${CLIPS.length - CLIP_NAMES.length} debug), ${files} key files, ${CLIPS.reduce((a, c) => a + c._r.info.keys, 0)} part keys, ${Object.keys(models).length} models (${Object.values(elementCount).reduce((a, b) => a + b, 0)} elements, ${shownElements} shown at rest), ${Object.keys(spriteTable).length} sprites (${(atlasPx / 1e6).toFixed(2)} M px)${warns.size ? `, ${warns.size} warnings` : ''}.`);
console.log(`rest extents x ${extents.idle[0]}, y ${extents.idle[1]}, z ${extents.idle[2]}`);
console.log(`budgets: ${Object.entries(REGION_BUDGET).map(([r, b]) => `${r} ${regionParts[r]}/${b.parts} parts ${(regionPx[r] / 1e6).toFixed(3)}/${b.px / 1e6} M px`).join('; ')}; ` +
  `elements shown max ${elementsMax}/${ELEMENT_BUDGET} (${Object.entries(elementsByLook).sort((x, y) => y[1] - x[1])[0][0]})` + (unusedSprites.length ? `; ${unusedSprites.length} unused sprites not painted (${unusedSprites.join(' ')})` : ''));
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
  // per-clip strip helpers: the anchor yaw of each played tick on every part (az_yaw/<clip>/<t>, renders only)
  for (const c of CLIPS) if (c.yaw) c.yaw.forEach((y, t) => putDebug(`az_dbg/yaw/${c.name}/${t}`, [`tp @e[type=item_display,tag=rlk_mb_azhdaha_part] ~ ~ ~ ${y} 0`]));
}
