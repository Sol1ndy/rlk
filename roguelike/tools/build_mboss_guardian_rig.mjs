// Articulated display-entity rig of the Corrupted Guardian (파수꾼・타락), the first mid-boss.
// node tools/build_mboss_guardian_rig.mjs --resourcepack <unpacked pack> [--datapack <pack>] [--no-paint]
//
// Writes
//   RP  assets/rlk/textures/mboss/guardian/*.png (guardian_paint.mjs) + item atlas entries
//       assets/rlk/models/item/mboss/guardian/*.json, assets/rlk/items/mboss/guardian/*.json
//       (also the chaos star crystals star_<kind>, not rig parts) and the P4 screen overlay font
//       assets/rlk/font/mboss_gd.json + textures/font/mboss_gd/* (guardian_screen.mjs)
//   DP  data/rlk/function/mboss/guardian/rig/** (this directory is owned by the generator and
//       rebuilt from scratch on every run)
//   tools/mboss_guardian_rig_manifest.json (parts, clips, events, API)
//
// Runtime model (the contract for the pattern code is tools/mboss_guardian_rig_api.md):
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
import {partModels, PART_SCALE, checkBounds, CUBES_B_VARIANTS, STAR_KINDS} from './guardian_geometry.mjs';
import {writeGuardianScreen} from './guardian_screen.mjs';
import {solve, toDisplay} from './guardian_pose.mjs';
import {CLIPS, accumulate, sampleClip as sample} from './guardian_clips.mjs';
import {slerp, lerp, qAngle, len, sub, add, rot, q as qEuler} from './guardian_rig_math.mjs';

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
// drift frames of the trail cubes (cubes_b is frame 0; the clips swap them, see MODEL_OF)
for (let v = 1; v < CUBES_B_VARIANTS; v++) item('cubes_b_' + v, 'cubes_b_' + v);
// Element looks (model.md section 4). Eye: the gem/iris/field of the shield; spear: the head
// enchanted in the element colour; glow: the aura card along the blade and shaft.
export const ELEMENTS = {
  geo: {id: 0, eye: null, spear: null, glow: 0xF4D07C},
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
// Afterimage cards take the spear look's glow colour (spear/<el> swaps them with the spear).
const TRAIL_GOLD = 0xF4D27A;
item('trail', 'trail', TRAIL_GOLD);
for (const [el, c] of Object.entries(ELEMENTS)) item('trail_' + el, 'trail', el === 'geo' ? TRAIL_GOLD : c.glow);
// Chaos element stars (summoned by the module as item_displays): 1-4 active element, 5/6 inert gold/blue, flash, dark.
for (const k of STAR_KINDS) item('star_' + k, 'star_' + k);
// P4 screen overlay (title font glyphs): frame texts go to the manifest for the pattern generator.
const screen = writeGuardianScreen(rp);
// Props share the spear model (not rig parts): javelin flight, planted spear, giant fail spears.
item('prop_spear', 'spear');
for (const el of ['red', 'gold', 'hydro', 'electro', 'cryo', 'pyro']) item('prop_spear_' + el, el === 'gold' ? 'spear' : 'spear_e', el === 'gold' ? null : ELEMENTS[el].spear);

// ---- clip sampling (guardian_clips.mjs) ------------------------------------------------------
const TRAIL_LAG = [1, 2].map(n => .55 * n), TRAIL_TAPER = [.72, .45];
// trail-cube drift frame: CUBES_B_VARIANTS per cube cycle (40 t, or the loop length)
const cubeFrame = ph => Math.floor(((ph % 1) + 1) % 1 * CUBES_B_VARIANTS + 1e-6) % CUBES_B_VARIANTS;
function frame(clip, t, ks, prev = null) {
  const warns = [];
  const p = sample(clip, t, ks);
  p.cubeV = cubeFrame(p.ph);
  const o = solve(p, {warn: m => warns.push(m), prev});
  for (const [i, lag] of TRAIL_LAG.entries()) {
    const tt = Math.max(0, t - lag), pp = sample(clip, tt, ks);
    const sp = solve(pp).spear;
    const on = p.trail > .5 && pp.spearS > .5 && t >= 1;
    o['trail_' + (i + 1)] = {t: sp.t, q: sp.q, s: on ? [TRAIL_TAPER[i] * p.trail, 1, TRAIL_TAPER[i] * p.trail] : [0, 0, 0]};
  }
  const d = {};
  for (const [n] of PARTS) d[n] = toDisplay(n, o[n], n.startsWith('trail') ? 'trail_1' : n);
  return {d, p, o, warns, bend: o._bend};
}
// All frames of a clip in order (the arm IK carries its bend plane from frame to frame).
function clipFrames(clip, ks = accumulate(clip)) {
  const out = [];
  for (let t = 0; t <= clip.len; t++) out.push(frame(clip, t, ks, t ? out[t - 1].bend : null));
  return out;
}
// Finial-on-face check (every clip, every tick): the butt finial is a red 4-point star like the
// face diamond, so it must never sit in front of the face, where it reads as a second face.
// Points on the spear axis below the grip (blocks): finial centre, finial end, orbit star.
const BUTT_POINTS = [-.95, -1.14, -1.29];
const FACE = [0, .158, -.12];                       // face diamond from the head pivot (rig frame)
function buttViolations(clip, frames) {
  const out = [];
  frames.forEach((f, t) => {
    const {o, p} = f, sp = o.spear;
    if (p.spearS < .5 || p.vis < .5 || p.bodyVis < .5) return;
    const R0 = qEuler(p.rot), inv = [-R0[0], -R0[1], -R0[2], R0[3]];
    const face = add(o.head.t, rot(o.head.q, FACE));
    for (const y of BUTT_POINTS) {
      const w = add(sp.t, rot(sp.q, [0, y * sp.s[1], 0]));
      const d = rot(inv, sub(w, face));                 // body frame, -Z forward
      if (Math.abs(d[0]) < .22 && d[1] > -.35 && d[1] < .12 && d[2] < .05) { out.push(`${clip.name} t${t}: spear butt ${y} b at [${d.map(v => v.toFixed(2))}] from the face`); break; }
    }
  });
  return out;
}
// Per-tick rotation check: no part may turn more than MAX_STEP_DEG between two ticks (the
// client slerps each step the short way; near 180 degrees that path is undefined and a twist
// or an IK flip shows as a pop through the body). Trails follow the spear and are skipped.
const MAX_STEP_DEG = 120;
const shown = v => v.s.some(x => Math.abs(x) > 1e-4);
function stepViolations(clip, frames) {
  const out = [];
  for (const [n] of PARTS) {
    if (n.startsWith('trail')) continue;
    for (let t = 1; t < frames.length; t++) {
      const a = frames[t - 1].d[n], b = frames[t].d[n];
      if (!shown(a) || !shown(b)) continue;
      const ang = qAngle(a.q, b.q);
      if (ang > MAX_STEP_DEG) out.push(`${clip.name} ${n} t${t - 1}->${t}: ${ang.toFixed(0)} degrees`);
    }
  }
  return out;
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
// A segment never spans more than MAX_SEG_DEG of rotation: near 180 degrees the client's
// shortest-path slerp has no stable direction (the sign of a cosine of about 1e-9 decides it),
// so spins get a key every tick. The fit is checked on the values as written (5 decimals).
// A segment that still turns more than this (a 1-tick step, or the forced blend-in) fails the
// build. Large 1-tick steps are also checked at the half tick: where the client's slerp leaves
// the authored path by more than SUB_TOL degrees (an elbow passing through the body) it warns.
const MAX_SEG_DEG = 120, SUB_TOL = 35;
const r5 = x => (Math.abs(x) < 5e-7 ? 0 : +x.toFixed(5));
const written = v => ({t: v.t.map(r5), q: v.q.map(r5), s: v.s.map(r5)});
function segments(raw, n, minFirst) {
  const seq = raw.map(written), L = seq.length - 1, out = [];
  let a = 0;
  while (a < L) {
    let b = a + 1;
    const fits = bb => {
      if (qAngle(seq[a].q, seq[bb].q) > MAX_SEG_DEG - 2) return false;
      for (let t = a + 1; t < bb; t++) if (!close(interp(seq[a], seq[bb], (t - a) / (bb - a)), seq[t], n)) return false;
      return true;
    };
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
const MODEL_OF = {rHand: ['r_hand', {fist: 'r_hand_fist', open: 'r_hand_open'}], lHand: ['l_hand', {fist: 'l_hand_fist', open: 'l_hand_open'}],
  cubeV: ['cubes_b', Object.fromEntries(Array.from({length: CUBES_B_VARIANTS}, (_, v) => [v, v ? 'cubes_b_' + v : 'cubes_b']))]};
const swapLine = (part, model) => `data modify entity ${uuidOf(part)} item.components."minecraft:item_model" set value "${itemId(model)}"`;

// ---- compile clips -------------------------------------------------------------------------
// --debug-dp <dir>: also writes the exact per-tick poses (gd_dbg/<clip>/<t>) and a copy of the
// rig functions into a scratch datapack root, for the offline renderer. Never the real pack.
const debugDp = arg('--debug-dp') && path.resolve(arg('--debug-dp'));
if (debugDp) fs.rmSync(path.join(debugDp, 'data/rlk/function/gd_dbg'), {recursive: true, force: true});
const putDebug = (n, lines) => put(path.join(debugDp, 'data/rlk/function', n + '.mcfunction'), lines.join('\n'));
const clipInfo = [], allWarn = new Set(), buttErrors = [], motionErrors = [];
CLIPS.forEach((c, id) => { c.id = id; });
const byName = Object.fromEntries(CLIPS.map(c => [c.name, c]));
for (const c of CLIPS) {
  if (c.keys[0][0] !== 0) throw new Error(`clip ${c.name}: first key must be tick 0`);
  if (c.keys[c.keys.length - 1][0] !== c.len) throw new Error(`clip ${c.name}: last key ${c.keys[c.keys.length - 1][0]} != len ${c.len}`);
  if (c.next && !byName[c.next]) throw new Error(`clip ${c.name}: unknown next ${c.next}`);
  const ks = accumulate(c);
  const frames = clipFrames(c, ks);
  frames.forEach((f, t) => f.warns.forEach(w => allWarn.add(`${c.name} t${t}: ${w}`)));
  buttErrors.push(...buttViolations(c, frames));
  motionErrors.push(...stepViolations(c, frames));
  const byTick = new Map();
  const add = (t, line) => { if (!byTick.has(t)) byTick.set(t, []); byTick.get(t).push(line); };
  let keyCount = 0;
  for (const [n] of PARTS) {
    const seq = frames.map(f => f.d[n]);
    for (const [a, b] of segments(seq, n, c.blend ?? 3)) {
      const turn = qAngle(seq[a].q, seq[b].q);
      if (turn > MAX_SEG_DEG && shown(seq[b]) && shown(seq[a]) && !n.startsWith('trail'))
        motionErrors.push(`${c.name} ${n} t${a}-${b}: ${turn.toFixed(0)} degree key (ambiguous slerp)`);
      if (b - a === 1 && turn > 45 && shown(seq[a]) && shown(seq[b])) {
        const mid = frame(c, a + .5, ks, frames[a].bend).d[n];
        const dev = qAngle(slerp(seq[a].q, seq[b].q, .5), mid.q);
        if (dev > SUB_TOL) allWarn.add(`${c.name} ${n} t${a}-${b}: the client path leaves the authored one by ${dev.toFixed(0)} degrees at the half tick`);
      }
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
  clipInfo.push({id: c.id, name: c.name, len: c.len, loop: !!c.loop, next: c.next || null, events: c.events || {}, keyFiles: ticks.length, keys: keyCount, note: c.note || '',
    ...(c.retime ? {authoredLen: c.authoredLen, retime: c.retime} : {})});
}
if (motionErrors.length) {
  const msg = `part rotations above ${MAX_STEP_DEG} degrees per tick or per key:\n  ` + motionErrors.slice(0, 120).join('\n  ') + (motionErrors.length > 120 ? `\n  ... ${motionErrors.length} in all` : '');
  if (flag('--allow-steps')) console.warn(msg); else throw new Error(msg);
}
if (buttErrors.length) {
  const msg = 'spear butt finial in front of the face:\n  ' + buttErrors.slice(0, 30).join('\n  ') + (buttErrors.length > 30 ? `\n  ... ${buttErrors.length} frames` : '');
  if (flag('--allow-butt')) console.warn(msg); else throw new Error(msg);
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
const rest = clipFrames(byName.idle)[0].d;
const TAGS = n => `["rlk_room","rlk_mb_aux","rlk_mb_part","rlk_mb_guardian_part","rlk_mb_gp_${n}"]`;
const summon = ([n, model, bright], hidden = false) => `summon minecraft:item_display ~ ~ ~ {UUID:${uuidInts(n)},Tags:${TAGS(n)},billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:2.5f,width:16f,height:16f,shadow_radius:0f,brightness:{block:${bright},sky:15},transformation:${nbt(hidden ? {...rest[n], s: [0, 0, 0]} : rest[n])},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${itemId(model)}"}}}`;
const RIG_OBJ = ['gdRigC', 'gdRigT', 'gdRigF', 'gdRigEye', 'gdRigSp', 'gdRigY', 'gdRigGl'];
fn('init', ['# Rig objectives. Safe to call on every load.', ...RIG_OBJ.map(o => `scoreboard objectives add ${o} dummy`)]);
const spawnTail = [`scoreboard players set @s gdRigC ${byName.idle.id}`, 'scoreboard players set @s gdRigT -1', 'scoreboard players set @s gdRigF 0',
  'execute unless score @s gdRigEye matches 0.. run scoreboard players set @s gdRigEye 0',
  'execute unless score @s gdRigSp matches 0.. run scoreboard players set @s gdRigSp 0',
  'execute unless score @s gdRigGl matches 0.. run scoreboard players set @s gdRigGl 0',
  `function ${NS}/look_apply`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow`];
fn('spawn', ['# @s = rig anchor (the boss body), positioned and rotated where she should appear.',
  '# Summons the 29 parts with fixed UUIDs in the idle pose and queues idle from its tick 0 (the next rig/tick).',
  `function ${NS}/init`, `function ${NS}/kill`, ...PARTS.map(summon), ...spawnTail]);
fn('spawn_hidden', ['# Like spawn, but every part starts at scale 0 (nothing shows). Play the opening clip in the',
  '# same tick (e.g. play/entrance): its first key brings the parts in. @s = rig anchor.',
  `function ${NS}/init`, `function ${NS}/kill`, ...PARTS.map(p => summon(p, true)), ...spawnTail]);
fn('follow', ['# Parts follow the executor position and yaw (run rotated as the anchor, pitch 0).', ...PARTS.map(([n]) => `tp ${uuidOf(n)} ~ ~ ~ ~ ~`)]);
fn('tick', ['# @s = rig anchor, at its feet. Once per game tick. Missing parts respawn in idle (the clip restarts as idle).',
  `execute unless entity ${uuidOf('torso')} run function ${NS}/spawn`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow`,
  'scoreboard players add @s gdRigT 1',
  `function ${NS}/run`,
  `execute if score @s gdRigF matches 1.. run function ${NS}/flash_tick`]);
fn('kill', ['# Removes every rig part (the props have their own tag).', 'kill @e[type=item_display,tag=rlk_mb_guardian_part]']);
fn('uninstall', ['# Removes the rig, its props and its objectives.', `function ${NS}/kill`, `function ${NS}/prop/clear`, 'kill @e[type=marker,tag=rlk_mb_gd_face]',
  ...RIG_OBJ.map(o => `scoreboard objectives remove ${o}`)]);
const OUTLINED = PARTS.filter(([n]) => !['halo_glow', 'spear_glow', 'trail_1', 'trail_2'].includes(n));
fn('flash', ['# Hit feedback: a white outline for 3 ticks (then back to the glow look). @s = rig anchor.', 'scoreboard players set @s gdRigF 4',
  ...OUTLINED.map(([n]) => `data merge entity ${uuidOf(n)} {Glowing:1b,glow_color_override:16772300}`)]);
fn('flash_tick', ['scoreboard players remove @s gdRigF 1', `execute if score @s gdRigF matches 0 run function ${NS}/flash_off`]);
fn('flash_off', ['# End of the hit flash: the persistent glow look (gdRigGl) or no outline. @s = rig anchor.', `function ${NS}/glow_apply`]);
// glow looks: a persistent outline on the whole body (guard mode's gold aura); the hit flash returns to it
const GLOW = {gold: [1, 0xFCD84C]};
fn('glow_apply', ['# Applies the stored glow look gdRigGl (0 none). @s = rig anchor.',
  ...Object.values(GLOW).flatMap(([id, col]) => OUTLINED.map(([n]) => `execute if score @s gdRigGl matches ${id} run data merge entity ${uuidOf(n)} {Glowing:1b,glow_color_override:${col}}`)),
  ...PARTS.map(([n]) => `execute if score @s gdRigGl matches 0 run data merge entity ${uuidOf(n)} {Glowing:0b}`)]);
for (const [el, [id]] of Object.entries(GLOW)) fn(`glow/${el}`, [`# Persistent ${el} outline on the whole body (until glow/off; a hit flash returns to it). @s = rig anchor.`,
  `scoreboard players set @s gdRigGl ${id}`, `execute unless score @s gdRigF matches 1.. run function ${NS}/glow_apply`]);
fn('glow/off', ['# Ends the glow look (the outline goes unless a hit flash is showing; flash_off then clears it). @s = rig anchor.',
  'scoreboard players set @s gdRigGl 0', `execute unless score @s gdRigF matches 1.. run function ${NS}/glow_apply`]);
// element looks: eye (shield gem/iris/field) and spear (head enchant + aura colour)
const elNames = Object.keys(ELEMENTS);
for (const el of elNames) {
  const id = ELEMENTS[el].id;
  fn(`eye/${el}`, [`# Shield eye in the ${el} colour. @s = rig anchor.`, `scoreboard players set @s gdRigEye ${id}`, swapLine('shield_eye', 'shield_eye_' + el)]);
  fn(`spear/${el}`, [`# Spear enchant: ${el}. @s = rig anchor.`, `scoreboard players set @s gdRigSp ${id}`, swapLine('spear', 'spear_' + el), swapLine('spear_glow', 'spear_glow_' + el),
    swapLine('trail_1', 'trail_' + el), swapLine('trail_2', 'trail_' + el)]);
  fn(`tint/${el}`, [`# Shield eye and spear both in the ${el} look. @s = rig anchor.`, `function ${NS}/eye/${el}`, `function ${NS}/spear/${el}`]);
}
fn('look_apply', ['# Re-applies the stored eye/spear/glow looks (after a respawn). @s = rig anchor.',
  `function ${NS}/glow_apply`,
  ...elNames.map(el => `execute if score @s gdRigEye matches ${ELEMENTS[el].id} run function ${NS}/eye/${el}`),
  ...elNames.map(el => `execute if score @s gdRigSp matches ${ELEMENTS[el].id} run function ${NS}/spear/${el}`)]);
fn('eye/by_elem', ['# Eye look from #elem-style ids in @s gdRigEye (0 geo, 1 pyro, 2 hydro, 3 electro, 4 cryo, 5 gold, 6 red).', `function ${NS}/look_apply`]);
// facing helpers (the parts take the anchor's yaw every tick)
fn('face/player', ['# Turn the anchor to face the nearest player (yaw only). @s = rig anchor.',
  'execute facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0']);
fn('face/track', ['# Turn the anchor toward the nearest player by at most 12 degrees per call. @s = rig anchor.',
  '# Both yaws are normalised into [-180, 180) first, so the stored yaw never drifts past one turn.',
  'scoreboard players set #c36000 gdRigY 36000',
  'execute store result score #yaw gdRigY run data get entity @s Rotation[0] 100',
  'scoreboard players add #yaw gdRigY 18000',
  'scoreboard players operation #yaw gdRigY %= #c36000 gdRigY',
  'execute if score #yaw gdRigY matches ..-1 run scoreboard players add #yaw gdRigY 36000',
  'scoreboard players remove #yaw gdRigY 18000',
  'execute facing entity @p[gamemode=!spectator] feet run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_aux","rlk_mb_gd_face"]}',
  'execute as @e[type=marker,tag=rlk_mb_gd_face,limit=1] at @s facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0',
  'execute store result score #yawT gdRigY run data get entity @e[type=marker,tag=rlk_mb_gd_face,limit=1] Rotation[0] 100',
  'kill @e[type=marker,tag=rlk_mb_gd_face]',
  'scoreboard players operation #yawT gdRigY -= #yaw gdRigY',
  'execute if score #yawT gdRigY matches 18000.. run scoreboard players remove #yawT gdRigY 36000',
  'execute if score #yawT gdRigY matches ..-18001 run scoreboard players add #yawT gdRigY 36000',
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
// --no-paint keeps the texture count of the last painted build (the sprites on disk are unchanged).
const manifestPath = path.join(here, 'mboss_guardian_rig_manifest.json');
const lastTextures = (() => { try { return JSON.parse(fs.readFileSync(manifestPath, 'utf8')).textures; } catch { return undefined; } })();
json(manifestPath, {
  parts: PARTS.map(([n, m, b]) => ({part: n, uuid: uuidOf(n), model: m, brightness: b, scale: PART_SCALE[n.startsWith('trail') ? 'trail_1' : n]})),
  clips: clipInfo,
  elements: Object.fromEntries(Object.entries(ELEMENTS).map(([k, v]) => [k, {id: v.id, eye: v.eye === null ? 'painted' : '#' + v.eye.toString(16).padStart(6, '0'), glow: '#' + v.glow.toString(16).padStart(6, '0')}])),
  objectives: {gdRigC: 'current clip id (anchor)', gdRigT: 'tick within the clip (anchor; -1 = queued by play)', gdRigF: 'hit flash countdown', gdRigEye: 'eye look id', gdRigSp: 'spear look id', gdRigY: 'face/track scratch', gdRigGl: 'glow look id (0 none, 1 gold)'},
  textures: sprites ? sprites.length : (typeof lastTextures === 'number' ? lastTextures : 'not repainted'),
  screen,
});
for (const w of [...allWarn].slice(0, 40)) console.warn('warn:', w);
const files = clipInfo.reduce((a, c) => a + c.keyFiles, 0);
console.log(`Built the Corrupted Guardian rig: ${PARTS.length} parts, ${CLIPS.length} clips, ${files} key files, ${clipInfo.reduce((a, c) => a + c.keys, 0)} part keys${allWarn.size ? `, ${allWarn.size} warnings` : ''}.`);
if (debugDp) fs.cpSync(rigDir, path.join(debugDp, 'data/rlk/function/mboss/guardian/rig'), {recursive: true});
