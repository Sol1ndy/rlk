// Display-entity rig of 아를레키노 (Arlecchino, the chapter-4 boss; S:ar/PLAN.md §2-3, contract S:ar/contract.md §3.2, frozen
// table tools/mboss_arlecchino/api.py §7 via tools/mboss_arlecchino/stub_rig_manifest.json). Built on the shared RIGLIB
// (mboss_rig_compile.mjs, mboss_rig_clips.mjs, mboss_rig_math.mjs, mboss_paint_lib.mjs, all unchanged). API note:
// tools/arlecchino_rig_api.md.
//
// node tools/build_arlecchino_rig.mjs --resourcepack <unpacked RP> [--datapack <dp>] [--no-paint] [--allow-steps]
//                                     [--debug-dp <scratch dir> [--debug-clips a,b | all] [--debug-step N]]
//
// Writes (owned, rebuilt from scratch on every run)
//   DP  data/rlk/function/boss/arlecchino/rig/**
//   RP  assets/rlk/textures/mboss/arlecchino/*, assets/rlk/models/item/mboss/arlecchino/**, assets/rlk/items/mboss/arlecchino/**
//       and the items-atlas entries rlk:mboss/arlecchino/*
//   tools/arlecchino_rig_manifest.json (the stub's schema + transforms, budgets, sprites; api.check_manifest passes)
// Reads, never writes: the avatar's item models rlk:player_motion/arle/<part> and rlk:player_motion/weapons/scythe (phase 1
// body and both scythes), tools/scythe_geometry.mjs (the scythe's hull for the floor checks).
// The build throws on: a part / prop / blade tip below the feet at any compiled tick, a clip / event / loop / form that
// differs from the contract, a rotation above 120 degrees per tick or per key, the atlas over 0.15 M px, more than 6 500
// elements at rest, a model outside -16..32 (--allow-steps turns the motion checks into warnings while authoring).
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {PART_NAMES, BODY, LEGS, rigModels, itemId, AVATAR, SCYTHE, SPRITES} from './arlecchino_geometry.mjs';
import {arlecchinoSprites, paintArlecchino, TEX_DIR} from './arlecchino_paint.mjs';
import {solve, toDisplay, fromDisplay, worldPoints, SIZE} from './arlecchino_pose.mjs';
import {CLIPS as AUTHORED, accumulate, sampleClip, DEFAULT_POSE, P2_POSE} from './arlecchino_clips.mjs';
import {SKIN_P2_B64} from './arlecchino_skin_p2.mjs';
import {buildScytheGeometry} from './scythe_geometry.mjs';
import {createRigCompiler, createRigFollow, nbt, written, interp, shown, summonShadow, cullOverhang} from './mboss_rig_compile.mjs';
import {qAngle, len, sub} from './mboss_rig_math.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const arg = n => { const i = process.argv.indexOf(n); return i < 0 ? null : process.argv[i + 1]; };
const flag = n => process.argv.includes(n);
const dp = path.resolve(arg('--datapack') || path.join(here, '..'));
const rp = arg('--resourcepack') && path.resolve(arg('--resourcepack'));
if (!rp) throw new Error('--resourcepack <unpacked pack> is required');
const put = (p, s) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, s.endsWith('\n') ? s : s + '\n'); };
const json = (p, o) => put(p, JSON.stringify(o, null, 1));
const t0 = Date.now();
const NS = 'rlk:boss/arlecchino/rig';
const rigDir = path.join(dp, 'data/rlk/function/boss/arlecchino/rig');
fs.rmSync(rigDir, {recursive: true, force: true});
let fnCount = 0;
const fn = (n, lines) => { put(path.join(rigDir, n + '.mcfunction'), (Array.isArray(lines) ? lines : [lines]).join('\n')); fnCount++; };
const OBJ = 'knRig';

// ---- contract (api.py) ---------------------------------------------------------------------------------------------
// the contract is api.py itself (api.stub_manifest(), the stub file's generator): a lead-approved api.py change (h1 at I1 / R-S3-1)
// reaches the build before the lead rewrites stub_rig_manifest.json
const STUB = JSON.parse(execFileSync('python3', ['-c', 'import json, sys; sys.path.insert(0, "tools"); from mboss_arlecchino import api; ' +
  'print(json.dumps(api.stub_manifest(), ensure_ascii=False))'], {cwd: path.join(here, '..'), encoding: 'utf8'}));
if (JSON.stringify(STUB.parts.map(p => p.name)) !== JSON.stringify(PART_NAMES)) throw new Error('parts differ from the contract');
if (STUB.size !== SIZE) throw new Error(`SIZE ${SIZE} differs from the contract ${STUB.size}`);
const CONTRACT = STUB.clips;
const CLIP_NAMES = Object.keys(CONTRACT).sort((a, b) => CONTRACT[a].id - CONTRACT[b].id);
const LOOKS = STUB.looks;
const FORMS = LOOKS.form;                                  // p1, p2
const FORM_ID = Object.fromEntries(FORMS.map((f, i) => [f, i]));

// ---- ids, UUIDs, tags --------------------------------------------------------------------------------------------------------
const UUID_HI = [0x524c4b4d | 0, 0x4b4e4100 | 0, 0x80000000 | 0];
const NN = n => (n === 'shadow' ? 0x40 : PART_NAMES.indexOf(n));
const uuidOf = n => `524c4b4d-4b4e-4100-8000-${NN(n).toString(16).padStart(12, '0')}`;
if (uuidOf('cup') !== STUB.uuid.replace('{:02x}', '18')) throw new Error('UUID scheme differs from the contract');
const TAGS = n => ['rlk_room', 'rlk_mb_aux', 'rlk_mb_part', 'rlk_kn_part', 'rlk_kn_' + n];
const SHADOW_TAGS = ['rlk_room', 'rlk_mb_aux', 'rlk_kn_part', 'rlk_kn_shadow'];
const CULL = {width: 10, height: 10}, VIEW_RANGE = 2;
const BRIGHT = n => (n.startsWith('scythe') ? 15 : LEGS.includes(n) ? 15 : n === 'cup' || n === 'saucer' ? 14 : 13);
const swap = (n, model) => `data modify entity ${uuidOf(n)} item.components."minecraft:item_model" set value "${model}"`;
const EMPTY = itemId('empty');

// ---- resource pack: models, items, sprites, atlas ----------------------------------------------------------------------------
const assets = path.join(rp, 'assets/rlk');
const modelDir = path.join(assets, 'models/item/mboss/arlecchino'), itemDir = path.join(assets, 'items/mboss/arlecchino');
for (const d of [modelDir, itemDir]) fs.rmSync(d, {recursive: true, force: true});
const models = rigModels();
for (const [name, m] of Object.entries(models)) {
  json(path.join(modelDir, name + '.json'), {ambientocclusion: false, textures: m.textures, elements: m.elements});
  json(path.join(itemDir, name + '.json'), {model: {type: 'minecraft:model', model: 'rlk:item/mboss/arlecchino/' + name}});
}
const sprites = arlecchinoSprites();
if (!flag('--no-paint')) paintArlecchino(rp, sprites);
// the P2 skin: the embedded skin_33 bytes unchanged
const skinBytes = Buffer.from(SKIN_P2_B64, 'base64');
fs.mkdirSync(path.join(rp, TEX_DIR), {recursive: true});
fs.writeFileSync(path.join(rp, TEX_DIR, 'skin_p2.png'), skinBytes);
{
  const atlasPath = path.join(rp, 'assets/minecraft/atlases/items.json');
  const atlas = JSON.parse(fs.readFileSync(atlasPath, 'utf8'));
  if (!atlas.sources.some(s => s.resource === itemId('skin_p2'))) { atlas.sources.push({type: 'minecraft:single', resource: itemId('skin_p2')}); fs.writeFileSync(atlasPath, JSON.stringify(atlas, null, 2) + '\n'); }
}
const ledger = {skin_p2: 64 * 64};
for (const [n, [w, h]] of Object.entries(SPRITES)) {
  if (w > 512 || h > 1024 || w % 16 || h % 16) throw new Error(`sprite ${n} ${w}x${h}: sides multiples of 16`);
  ledger[n] = w * h;
}
const atlasPx = Object.values(ledger).reduce((a, b) => a + b, 0);
const ATLAS_BUDGET = 150000;
if (atlasPx > ATLAS_BUDGET) throw new Error(`atlas ${atlasPx} px > ${ATLAS_BUDGET}`);
// elements shown at rest per form (the avatar's body models are 2 boxes each; the scythe model from scythe_geometry)
const SCY_EL = buildScytheGeometry().scythe.length;
const ELEMENTS = {p1: BODY.length * 2 + SCY_EL, p2: BODY.length * 2 + 2 * SCY_EL + 6 * (models.leg_a.elements.length + models.leg_b.elements.length)};
const EL_BUDGET = 6500;
for (const [f, n] of Object.entries(ELEMENTS)) if (n > EL_BUDGET) throw new Error(`form ${f}: ${n} elements at rest > ${EL_BUDGET}`);

// ---- clips: contract + authored motion --------------------------------------------------------------------------------------
const byName = Object.fromEntries(AUTHORED.map(c => [c.name, c]));
const missing = CLIP_NAMES.filter(n => !byName[n]);
if (missing.length && !flag('--allow-missing')) throw new Error(`clips not authored: ${missing.join(', ')}`);
for (const n of Object.keys(byName)) if (!CONTRACT[n]) throw new Error(`clip ${n} is not in the contract`);
const CLIPS = CLIP_NAMES.map(n => {
  const k = CONTRACT[n], a = byName[n] || {keys: [[0, {}], [k.len, {}]], note: 'stand-in (not authored)'};
  const c = {...a, name: n, id: k.id, len: k.len, loop: k.loop, events: k.events, form: k.form};
  if (c.keys[0][0] !== 0 || c.keys[c.keys.length - 1][0] !== c.len) throw new Error(`clip ${n}: keys must run 0..${c.len} (got ${c.keys[0][0]}..${c.keys[c.keys.length - 1][0]})`);
  c.keys.forEach(([t], i) => { if (i && t <= c.keys[i - 1][0]) throw new Error(`clip ${n}: keys not increasing at ${t}`); });
  if (a.events && JSON.stringify(a.events) !== JSON.stringify(k.events)) throw new Error(`clip ${n}: authored events differ from the contract`);
  return c;
});

// ---- per-clip solve ---------------------------------------------------------------------------------------------------------
const formAt = (c, t, base) => { let f = base; for (const [tt, ff] of Object.entries(c.formAt || {}).sort((a, b) => a[0] - b[0])) if (t >= +tt) f = ff; return f; };
const variantsOf = c => (c.form ? [c.form] : FORMS);
const baseOf = (c, f) => c.base || (f === 'p2' ? P2_POSE : DEFAULT_POSE);
function solveClip(c, form) {
  const base = baseOf(c, form), ks = accumulate(c, base), out = [];
  const warm = c.loop && c.loop[1] === c.len ? c.len : 0;
  let prev = null;
  for (let i = 0; i <= warm + c.len; i++) {
    const t = i - warm, tt = t < 0 ? t + c.len : t;
    const p = sampleClip(c, tt, ks, base), f = formAt(c, tt, form);
    const r = solve(p, f, prev);
    prev = r.keep;
    out.push({p, f, r, d: Object.fromEntries(PART_NAMES.map(n => [n, toDisplay(r.parts[n])])), m: Object.fromEntries(PART_NAMES.map(n => [n, r.parts[n].model]))});
  }
  return out.slice(warm);
}

// ---- compile -----------------------------------------------------------------------------------------------------------------
const TOL = {t: .012, s: .015, rDefault: 1.2, r: {scythe_r: .5, scythe_l: .5, right_forearm: 1, left_forearm: 1, right_arm: 1, left_arm: 1},
  tp: {scythe_r: .02, scythe_l: .02, ...Object.fromEntries(LEGS.map(n => [n, .03]))}};
const compiler = createRigCompiler({ns: NS, obj: OBJ, fn, parts: PART_NAMES, uuidOf, tol: TOL});
const SCY_MAX_SEG = 8;          // a scythe key at least every 8 ticks (look/weapon_*/world -> hand catches up within 8 t)
function segmentsCut(seq, n, cuts, minFirst) {
  const bounds = [...new Set([0, ...cuts.filter(t => t > 0 && t < seq.length - 1), seq.length - 1])].sort((a, b) => a - b), out = [];
  for (let i = 0; i < bounds.length - 1; i++) {
    const a = bounds[i], b = bounds[i + 1];
    let mf = i === 0 ? minFirst : 1;
    if (mf > 1 && shown(seq[a]) && shown(seq[Math.min(b, a + mf)]) && qAngle(seq[a].q, seq[Math.min(b, a + mf)].q) > 110) mf = 1;
    for (const [x, y] of compiler.segments(seq.slice(a, b + 1), n, mf)) {
      if (n.startsWith('scythe') && y - x > SCY_MAX_SEG) { let s = x; while (y - s > SCY_MAX_SEG) { out.push([s + a, s + SCY_MAX_SEG + a]); s += SCY_MAX_SEG; } out.push([s + a, y + a]); }
      else out.push([x + a, y + a]);
    }
  }
  return out;
}
const sameD = (x, y) => len(sub(x.t, y.t)) < 1e-5 && qAngle(x.q, y.q) < .01 && x.s.every((v, i) => Math.abs(v - y.s[i]) < 1e-5);
const clipInfo = {}, motionErrors = [], floorErrors = [], cullWarn = [], edgeWarn = [];
let keyFiles = 0, keyLines = 0;
const ANCHOR_NAMES = STUB.anchors;
const anchorTable = {};                 // clip -> {anchor: [strings per tick 0..len+1]}
const debugDp = arg('--debug-dp') && path.resolve(arg('--debug-dp'));
const debugClips = (arg('--debug-clips') || 'all').split(',');
const debugStep = +(arg('--debug-step') || 1);
if (debugDp) fs.rmSync(path.join(debugDp, 'data/rlk/function/kn_dbg'), {recursive: true, force: true});
const putDebug = (n, lines) => put(path.join(debugDp, 'data/rlk/function', n + '.mcfunction'), lines.join('\n'));
const guardOf = n => (n === 'scythe_r' ? `unless score @s ${OBJ}Wr matches 2 ` : n === 'scythe_l' ? `unless score @s ${OBJ}Wl matches 2 ` : '');
const fmtA = v => { const r = x => { const s = (Math.round(x * 100) / 100).toString(); return s === '-0' ? '0' : s.replace(/^(-?)0\./, '$1.'); }; return `^${r(v[0])} ^${r(v[1])} ^${r(-v[2])}`; };

for (const c of CLIPS) {
  const vars = variantsOf(c), F = Object.fromEntries(vars.map(f => [f, solveClip(c, f)]));
  const cuts = [...(c.cuts || []), ...Object.keys(c.formAt || {}).map(Number)];
  const byTick = new Map(), add_ = (t, l) => { if (!byTick.has(t)) byTick.set(t, []); byTick.get(t).push(l); };
  let keys = 0;
  const compiledD = {};
  for (const f of vars) compiledD[f] = {};
  for (const n of PART_NAMES) {
    const groups = [];
    for (const f of vars) {
      const seq = F[f].map(fr => fr.d[n]);
      const g = groups.find(G => G.seq.every((v, i) => sameD(v, seq[i])));
      if (g) g.forms.push(f); else groups.push({seq, forms: [f]});
    }
    for (const G of groups) {
      let segs = segmentsCut(G.seq, n, cuts, c.blend ?? 3);
      const fr0 = F[G.forms[0]];
      const lowAt = (t, v) => { const P = worldPoints(fr0[t].m[n], fromDisplay(v)); return P.length ? Math.min(...P.map(x => x[1])) : 1; };
      for (let guard = 0; guard < 400; guard++) {
        const W = G.seq.map(written); let worst = null;
        for (const [a, b] of segs) for (let t = a + 1; t < b; t++) {
          const y = lowAt(t, interp(W[a], W[b], (t - a) / (b - a)));
          if (y < -.005 && (!worst || y < worst.y)) worst = {a, b, t, y};
        }
        if (!worst) break;
        segs = segs.flatMap(([a, b]) => (a === worst.a && b === worst.b ? [[a, worst.t], [worst.t, b]] : [[a, b]]));
      }
      // keys as shipped {at, dur, to}; a 1-tick segment ending on a cut tick and turning > 60 deg (or showing a hidden part) snaps
      const snapAt = new Set(cuts), keyList = [];
      let snapped = -1;
      for (const [a, b] of segs) {
        const turn = qAngle(G.seq[a].q, G.seq[b].q);
        const pop = !shown(G.seq[a]) && shown(G.seq[b]);
        if (b - a === 1 && snapAt.has(b) && (turn > 60 || pop || len(sub(G.seq[a].t, G.seq[b].t)) > .25)) { keyList.push({at: b, dur: 0, to: b}); snapped = b; continue; }
        if (turn > 118 && shown(G.seq[a]) && shown(G.seq[b])) motionErrors.push(`${c.name} ${n} t${a}-${b}: ${turn.toFixed(0)} degree key (ambiguous slerp)`);
        if (a === snapped) { if (b - a > 1) keyList.push({at: a + 1, dur: b - a - 1, to: b}); }
        else keyList.push({at: a, dur: b - a, to: b});
      }
      const W = G.seq.map(written), cv = new Array(G.seq.length);
      {
        let from = W[0], k0 = 0, d = 0, tgt = W[0];
        const byAt = new Map(keyList.map(k => [k.at, k]));
        for (let t = 0; t < G.seq.length; t++) {
          const cur = d > 0 && t < k0 + d ? interp(from, tgt, (t - k0) / d) : tgt;
          const k = byAt.get(t);
          if (k) { from = t === 0 ? W[0] : cur; tgt = W[k.to]; k0 = t; d = k.dur; }
          cv[t] = d > 0 && t < k0 + d ? interp(from, tgt, (t - k0) / d) : tgt;
        }
      }
      for (const f of G.forms) compiledD[f][n] = cv;
      const ids = G.forms.map(f => FORM_ID[f]), lo = Math.min(...ids), hi = Math.max(...ids);
      const fg = groups.length > 1 ? `if score @s ${OBJ}Form matches ${lo === hi ? lo : lo + '..' + hi} ` : '';
      const wg = guardOf(n);
      const pre = fg || wg ? `execute ${fg}${wg}run ` : '';
      for (const k of keyList) { add_(k.at, `${pre}data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:${k.dur},transformation:${nbt(G.seq[k.to])}}`); keys++; }
    }
  }
  // per-tick checks on what ships: floor, culling, 1-tick turns
  for (const f of vars) {
    const fr = F[f];
    for (let t = 0; t <= c.len; t++) {
      for (const n of PART_NAMES) {
        const v = compiledD[f][n][t];
        if (!shown(v)) continue;
        const pts = worldPoints(fr[t].m[n], fromDisplay(v));
        if (!pts.length) continue;
        const y = Math.min(...pts.map(P => P[1]));
        if (y < -.01) floorErrors.push(`${c.name}[${f}] t${t} ${n}: lowest point ${y.toFixed(3)} b`);
        const over = Math.max(...pts.map(P => cullOverhang(P, CULL)));
        if (over > 0) cullWarn.push(`${c.name}[${f}] t${t} ${n} ${over.toFixed(2)} b`);
        if (t && !cuts.includes(t) && shown(compiledD[f][n][t - 1])) { const a = qAngle(compiledD[f][n][t - 1].q, v.q); if (a > 120) motionErrors.push(`${c.name}[${f}] ${n} t${t - 1}->${t}: ${a.toFixed(0)} degrees`); }
      }
    }
    // the edge check: in a swing (the shaft turning >= 8 deg / tick) the hook (the crescent's point) leads the motion of the
    // head, as the avatar's calibrated strikes; clips list footage flourishes where it trails (edgeOk)
    for (const X of ['R', 'L']) {
      for (let t = 1; t <= c.len; t++) {
        const a = fr[t - 1].r.edge[X], b = fr[t].r.edge[X];
        if (!a || !b || !shown(compiledD[f][X === 'R' ? 'scythe_r' : 'scythe_l'][t])) continue;
        const ang = Math.acos(Math.max(-1, Math.min(1, a.A[0] * b.A[0] + a.A[1] * b.A[1] + a.A[2] * b.A[2]))) * 180 / Math.PI;
        if (ang < 8) continue;
        const mv = sub(b.A, a.A), d = mv[0] * b.Hk[0] + mv[1] * b.Hk[1] + mv[2] * b.Hk[2];
        if (d < -.25 * len(mv) && !(c.edgeOk || []).some(([x, y]) => t >= x && t <= y)) edgeWarn.push(`${c.name}[${f}] ${X} t${t}`);
      }
    }
  }
  // tick 0: show a hidden rig, enforce the clip's form; the clip's look events
  const head0 = [`execute if score @s ${OBJ}S matches 1 run scoreboard players set @s ${OBJ}S 0`];
  if (c.form) head0.push(`execute unless score @s ${OBJ}Form matches ${FORM_ID[c.form]} run function ${NS}/look/form/${c.form}`);
  for (const l of head0.reverse()) byTick.has(0) ? byTick.get(0).unshift(l) : add_(0, l);
  for (const [t, f] of Object.entries(c.formAt || {})) add_(+t, `function ${NS}/look/form/${f}`);
  for (const [t, lk] of c.looks || []) { if (!LOOKS[lk.split('/')[0]]?.includes(lk.split('/')[1])) throw new Error(`clip ${c.name}: unknown look ${lk}`); add_(t, `function ${NS}/look/${lk}`); }
  const ticks = [...byTick.keys()].sort((x, y) => x - y);
  for (const t of ticks) fn(`c/${c.name}/k/${t}`, byTick.get(t));
  keyFiles += ticks.length; keyLines += keys;
  // runner: loop (whole clip) / hold the last pose; a loop span ending before the clip's end plays straight through
  const head = [`# ${c.name}: ${c.len} t${c.loop ? (c.loop[1] === c.len ? `, loops ${c.loop[0]}-${c.loop[1]}` : ` (hold span ${c.loop[0]}-${c.loop[1]} not looped: plays through, then holds)`) : ', holds the last pose'}. @s = rig anchor.`];
  if (c.loop && c.loop[1] === c.len) head.push(`execute if score @s ${OBJ}T matches ${c.len}.. run scoreboard players set @s ${OBJ}T ${c.loop[0]}`);
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
  // anchors (the clip's authored form; ticks 0..len, len + 1 = the held last pose)
  const af = F[vars[0]];
  anchorTable[c.name] = Object.fromEntries(ANCHOR_NAMES.map(a => [a, [...af.map(fr => fmtA(fr.r.anchors[a])), fmtA(af[c.len].r.anchors[a])]]));
  clipInfo[c.name] = {id: c.id, len: c.len, loop: c.loop, events: c.events, form: c.form, compiled_forms: vars, key_files: ticks.length, keys,
    keys_per_tick: +(keys / (c.len + 1)).toFixed(1), looks: c.looks || [], source: c.src || '', note: c.note || ''};
  if (debugDp && (debugClips.includes('all') || debugClips.includes(c.name))) {
    for (const f of vars) for (let t = 0; t <= c.len; t += debugStep) {
      const fr = F[f][t];
      putDebug(`kn_dbg/${c.name}${vars.length > 1 ? '_' + f : ''}/${t}`, [...PART_NAMES.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(written(compiledD[f][n][t]))}}`),
        ...PART_NAMES.map(n => swap(n, fr.m[n]))]);
    }
  }
}
const fail = (title, list) => { if (list.length) { const m = `${title}:\n  ${list.slice(0, +(arg('--show') || 40)).join('\n  ')}${list.length > 40 ? `\n  ... ${list.length} in all` : ''}`; if (flag('--allow-steps')) console.warn(m); else throw new Error(m); } };
fail('floor (no shown element below the feet)', floorErrors);
fail('rotations above 120 degrees per tick or per key', motionErrors);
fail('culling box overhang', cullWarn);
if (edgeWarn.length) console.warn(`edge: the hook trails in ${edgeWarn.length} swing ticks: ${edgeWarn.slice(0, 12).join(', ')}`);
compiler.writeDispatch(CLIPS.map(c => ({id: c.id, name: c.name})));

// ---- follow, init, spawn, tick ----------------------------------------------------------------------------------------------
const without = x => PART_NAMES.filter(n => !x.includes(n));
const follow = createRigFollow({ns: NS, obj: OBJ, fn, uuidOf, lists: {all: PART_NAMES, no_r: without(['scythe_r']), no_l: without(['scythe_l']), no_rl: without(['scythe_r', 'scythe_l'])},
  fixed: ['shadow'], staticSkip: true, comment: '# Parts follow the anchor position and yaw (run as and rotated as the boss at its feet, pitch 0).'});
follow.write();
const OBJS = [`${OBJ}C`, `${OBJ}T`, `${OBJ}F`, `${OBJ}Y`, `${OBJ}S`, `${OBJ}Form`, `${OBJ}Wi`, `${OBJ}Wr`, `${OBJ}Wl`, `${OBJ}Gl`, `${OBJ}Pr`, ...follow.objectives];
const anJson = JSON.stringify(anchorTable), anVer = parseInt(crypto.createHash('sha1').update(anJson).digest('hex').slice(0, 7), 16);
fn('init', ['# Rig objectives (safe on every load). knRigC clip id, knRigT clip tick (-1 = queued), knRigF hit flash, knRigY face scratch,',
  '# knRigS state (0 normal, 1 hidden), knRigForm (0 p1, 1 p2), stored looks knRigWi wings, knRigWr / knRigWl weapons, knRigGl glow,',
  '# knRigPr props (indices of api.LOOKS); knRigFl the follow list, knRigQ* the follow cache. The anchor table (storage rlk:kn rig.an)',
  '# is loaded once per version.', ...OBJS.map(o => `scoreboard objectives add ${o} dummy`),
  `execute unless data storage rlk:kn rig{anv:${anVer}} run function ${NS}/an/load`]);
// rest pose of each form (idle / idle2 tick 0)
const REST = Object.fromEntries(FORMS.map(f => { const fr = solveClip(CLIPS.find(c => c.name === (f === 'p2' ? 'idle2' : 'idle')), f)[0]; return [f, fr]; }));
const summon = n => `summon minecraft:item_display ~ ~ ~ {UUID:[I;${[...UUID_HI, NN(n)].join(',')}],Tags:${JSON.stringify(TAGS(n))},billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,` +
  `view_range:${VIEW_RANGE}f,width:${CULL.width}f,height:${CULL.height}f,shadow_radius:0f,brightness:{block:${BRIGHT(n)},sky:15},transformation:${nbt(written(REST.p1.d[n]))},` +
  `item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${BODY.includes(n) ? AVATAR(n) : n.startsWith('scythe') ? SCYTHE : EMPTY}"}}}`;
fn('spawn', ['# @s = the boss (the anchor), at its feet. Kills old parts, summons the 26 parts (fixed UUIDs 524c4b4d-4b4e-4100-8000-0000000000NN) and the',
  '# shadow helper (…40) in the rest pose, re-applies the stored form and looks, and queues idle (idle2 in form p2).', `function ${NS}/init`, `function ${NS}/kill`,
  `execute unless score @s ${OBJ}Form matches 0..1 run scoreboard players set @s ${OBJ}Form 0`,
  `execute unless score @s ${OBJ}Wi matches 0..1 run scoreboard players set @s ${OBJ}Wi 0`,
  `execute unless score @s ${OBJ}Wr matches 0..2 run scoreboard players set @s ${OBJ}Wr 0`,
  `execute unless score @s ${OBJ}Wl matches 0..2 run scoreboard players set @s ${OBJ}Wl 0`,
  `execute unless score @s ${OBJ}Gl matches 0..1 run scoreboard players set @s ${OBJ}Gl 0`,
  `execute unless score @s ${OBJ}Pr matches 0..1 run scoreboard players set @s ${OBJ}Pr 0`,
  `scoreboard players set @s ${OBJ}S 0`, `scoreboard players set @s ${OBJ}F 0`,
  ...PART_NAMES.map(summon), summonShadow({uuid: [...UUID_HI, 0x40], tags: SHADOW_TAGS, item: EMPTY, radius: 1.0, strength: .7, viewRange: VIEW_RANGE, cull: CULL}),
  `function ${NS}/look_apply`, `execute if score @s ${OBJ}Form matches 1 run function ${NS}/play/idle2`, `execute unless score @s ${OBJ}Form matches 1 run function ${NS}/play/idle`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow_now`]);
fn('spawn_hidden', ['# As spawn, then hidden (every part at scale 0 until the next play / start). @s = the boss, at its feet.', `function ${NS}/spawn`, `function ${NS}/state/hidden`]);
fn('tick', ['# @s = the boss (the anchor), at its feet, once per game tick (the core calls it). Missing parts respawn; hidden: only the',
  '# follow runs until a clip is queued (its tick 0 shows the rig again).',
  `execute unless entity ${uuidOf('body')} run function ${NS}/spawn`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow`,
  `execute if score @s ${OBJ}F matches 1.. run function ${NS}/flash_tick`,
  `execute if score @s ${OBJ}S matches 1 unless score @s ${OBJ}T matches -1 run return 0`,
  `scoreboard players add @s ${OBJ}T 1`, `function ${NS}/run`]);
fn('kill', ['# Removes every rig part, the shadow helper and the anchor marker.', 'kill @e[type=item_display,tag=rlk_kn_part]', 'kill @e[type=marker,tag=rlk_kn_anchor]']);
fn('uninstall', ['# Removes the rig, the anchor marker, the face marker, the rig objectives and the rig storage (rlk:kn rig).', `function ${NS}/kill`,
  'kill @e[type=marker,tag=rlk_kn_face]', ...OBJS.map(o => `scoreboard objectives remove ${o}`), 'data remove storage rlk:kn rig']);
fn('state/hidden', ['# Hidden: every part at scale 0 where it stands (never moved, never below the floor), no clip runs, the parts keep following',
  '# the anchor. The next play/start shows the rig again. @s = the boss.', `scoreboard players set @s ${OBJ}S 1`, `scoreboard players set @s ${OBJ}T 0`,
  ...PART_NAMES.map(n => `data modify entity ${uuidOf(n)} transformation.scale set value [0f,0f,0f]`)]);
fn('state/normal', ['# Visible again. From hidden: the current clip restarts from its tick 0 at the next rig/tick (its keys show every part);',
  '# already visible: nothing changes (pattern cancels call it freely). @s = the boss.',
  `execute if score @s ${OBJ}S matches 1 run scoreboard players set @s ${OBJ}T -1`, `scoreboard players set @s ${OBJ}S 0`]);
const FLASH = BODY;
fn('flash', ['# Hit feedback: the body outlines white-gold for 3 ticks (the scythes keep the glow look). @s = the boss.', `scoreboard players set @s ${OBJ}F 3`,
  ...FLASH.map(n => `data merge entity ${uuidOf(n)} {Glowing:1b,glow_color_override:16774320}`)]);
fn('flash_tick', ['# Internal: counts the flash down.', `scoreboard players remove @s ${OBJ}F 1`, `execute if score @s ${OBJ}F matches ..0 run function ${NS}/flash_off`]);
fn('flash_off', ['# Internal: end of the hit flash.', `scoreboard players set @s ${OBJ}F 0`, ...FLASH.map(n => `data merge entity ${uuidOf(n)} {Glowing:0b}`)]);
compiler.writeFace({marker: 'rlk_kn_face', maxDeg: 12});

// ---- looks ----------------------------------------------------------------------------------------------------------------------
const LEG_MODELS = {p2: {a: itemId('leg_a'), b: itemId('leg_b')}, wings: {a: itemId('wing_a'), b: itemId('wing_b')}};
const legSwaps = set => LEGS.map(n => swap(n, set ? set[n.endsWith('a') ? 'a' : 'b'] : EMPTY));
fn('look/r/legs', ['# Internal: the leg / wing models from the stored form and wings (p2: blade legs; p1 open: crimson wings; p1 off: empty).',
  ...legSwaps(LEG_MODELS.p2).map(l => `execute if score @s ${OBJ}Form matches 1 run ${l}`),
  ...legSwaps(LEG_MODELS.wings).map(l => `execute if score @s ${OBJ}Form matches 0 if score @s ${OBJ}Wi matches 1 run ${l}`),
  ...legSwaps(null).map(l => `execute if score @s ${OBJ}Form matches 0 unless score @s ${OBJ}Wi matches 1 run ${l}`)]);
fn('look/r/scythe_r', ['# Internal: scythe_r shown (hand / world) or the empty model (gone).',
  `execute if score @s ${OBJ}Wr matches 1 run ${swap('scythe_r', EMPTY)}`, `execute unless score @s ${OBJ}Wr matches 1 run ${swap('scythe_r', SCYTHE)}`]);
fn('look/r/scythe_l', ['# Internal: scythe_l shown in form p2 (hand / world), else the empty model (form p1 or gone).',
  `execute if score @s ${OBJ}Form matches 1 unless score @s ${OBJ}Wl matches 1 run ${swap('scythe_l', SCYTHE)}`,
  `execute if score @s ${OBJ}Form matches 1 if score @s ${OBJ}Wl matches 1 run ${swap('scythe_l', EMPTY)}`,
  `execute if score @s ${OBJ}Form matches 0 run ${swap('scythe_l', EMPTY)}`]);
fn('look/r/follow', ['# Internal: the follow list without the scythes set in the world (look/weapon_*/world).',
  ...[['all', 'unless score @s knRigWr matches 2 unless score @s knRigWl matches 2'], ['no_r', 'if score @s knRigWr matches 2 unless score @s knRigWl matches 2'],
    ['no_l', 'unless score @s knRigWr matches 2 if score @s knRigWl matches 2'], ['no_rl', 'if score @s knRigWr matches 2 if score @s knRigWl matches 2']]
    .flatMap(([l, cond]) => follow.listLines(l).map(x => `execute ${cond} run ${x}`))]);
fn('look/r/glow', ['# Internal: the crimson glow (BoL tells) on both scythes, or none.',
  ...['scythe_r', 'scythe_l'].map(n => `execute if score @s ${OBJ}Gl matches 1 run data merge entity ${uuidOf(n)} {Glowing:1b,glow_color_override:14692410}`),
  ...['scythe_r', 'scythe_l'].map(n => `execute unless score @s ${OBJ}Gl matches 1 run data merge entity ${uuidOf(n)} {Glowing:0b}`)]);
fn('look/r/props', ['# Internal: the cup and saucer models (tea) or empty.',
  `execute if score @s ${OBJ}Pr matches 1 run ${swap('cup', itemId('cup'))}`, `execute if score @s ${OBJ}Pr matches 1 run ${swap('saucer', itemId('saucer'))}`,
  `execute unless score @s ${OBJ}Pr matches 1 run ${swap('cup', EMPTY)}`, `execute unless score @s ${OBJ}Pr matches 1 run ${swap('saucer', EMPTY)}`]);
for (const f of FORMS) fn(`look/form/${f}`, [`# Form ${f}: the body models (${f === 'p1' ? 'the player avatar\'s rlk:player_motion/arle/*' : 'skin_33, rlk:mboss/arlecchino/p2/*'}), the ${f === 'p1' ? 'wings (shown only with look/wings/open)' : 'blade legs'}, scythe_l${f === 'p1' ? ' hidden' : ' in the left hand'}. @s = the boss.`,
  `scoreboard players set @s ${OBJ}Form ${FORM_ID[f]}`, ...BODY.map(n => swap(n, f === 'p2' ? itemId('p2/' + n) : AVATAR(n))), `function ${NS}/look/r/legs`, `function ${NS}/look/r/scythe_l`]);
const STORE = {wings: 'Wi', weapon_r: 'Wr', weapon_l: 'Wl', glow: 'Gl', props: 'Pr'};
const APPLY = {wings: ['legs'], weapon_r: ['scythe_r', 'follow'], weapon_l: ['scythe_l', 'follow'], glow: ['glow'], props: ['props']};
for (const [ch, vals] of Object.entries(LOOKS)) {
  if (ch === 'form') continue;
  vals.forEach((v, i) => fn(`look/${ch}/${v}`, [`# Look ${ch} = ${v} (stored in ${OBJ}${STORE[ch]} = ${i}). @s = the boss.`, `scoreboard players set @s ${OBJ}${STORE[ch]} ${i}`,
    ...APPLY[ch].map(a => `function ${NS}/look/r/${a}`)]));
}
fn('look_apply', ['# Re-applies every stored look (spawn). @s = the boss.',
  ...FORMS.map((f, i) => `execute if score @s ${OBJ}Form matches ${i} run function ${NS}/look/form/${f}`),
  ...['scythe_r', 'scythe_l', 'follow', 'glow', 'props'].map(a => `function ${NS}/look/r/${a}`)]);

// ---- anchors: rig/anchor/<name> moves the one rlk_kn_anchor marker to that point of the current clip tick ----------------------
fn('an/load', ['# Internal (init, once per table version): the anchor table rlk:kn rig.an[<clip id>].<anchor>[<tick 0..len+1>] = "^left ^up ^forward".',
  'data modify storage rlk:kn rig.an set value []',
  ...CLIPS.flatMap(c => ['data modify storage rlk:kn rig.an append value {}',
    ...ANCHOR_NAMES.map(a => `data modify storage rlk:kn rig.an[${c.id}].${a} set value ${JSON.stringify(anchorTable[c.name][a])}`)]),
  `data modify storage rlk:kn rig.anv set value ${anVer}`]);
for (const a of ANCHOR_NAMES) fn(`anchor/${a}`, [`# Moves the rlk_kn_anchor marker to ${a} of the current clip tick (yaw = the boss's). Effects run at / as it. @s = the boss, at its feet.`,
  `execute unless entity @e[type=marker,tag=rlk_kn_anchor,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_anchor"]}`,
  `execute store result storage rlk:kn rig.q.c int 1 run scoreboard players get @s ${OBJ}C`,
  `execute store result storage rlk:kn rig.q.t int 1 run scoreboard players get @s ${OBJ}T`,
  `execute if score @s ${OBJ}T matches ..-1 run data modify storage rlk:kn rig.q.t set value 0`,
  `data modify storage rlk:kn rig.q.a set value "${a}"`,
  `function ${NS}/anchor/r/get with storage rlk:kn rig.q`]);
fn('anchor/r/get', ['# Internal: the anchor string of clip $(c) tick $(t).', '$data modify storage rlk:kn rig.q.p set from storage rlk:kn rig.an[$(c)].$(a)[$(t)]',
  `function ${NS}/anchor/r/go with storage rlk:kn rig.q`]);
fn('anchor/r/go', ['# Internal: the marker to the point (local to the boss, yaw only).', '$execute rotated as @s rotated ~ 0 run tp @e[type=marker,tag=rlk_kn_anchor,limit=1] $(p) ~ 0']);

// ---- manifest ---------------------------------------------------------------------------------------------------------------------
const fnFiles = (() => { let n = 0, b = 0; const walk = d => { for (const f of fs.readdirSync(d, {withFileTypes: true})) { const p = path.join(d, f.name); if (f.isDirectory()) walk(p); else { n++; b += fs.statSync(p).size; } } }; walk(rigDir); return {files: n, bytes: b}; })();
const manifest = {
  schema: 1, id: 'arlecchino', source: 'rig',
  _doc: 'Arlecchino rig (tools/build_arlecchino_rig.mjs, API tools/arlecchino_rig_api.md): the D0 stub schema (parts, clips with id / len / loop / events / form, looks, anchors, calls) plus transforms, models, budgets and sprites. Generated: do not edit.',
  height: STUB.height, hip_y: STUB.hip_y, size: STUB.size, uuid: STUB.uuid,
  parts: STUB.parts.map(p => ({...p, uuid: uuidOf(p.name), tag: 'rlk_kn_' + p.name, brightness: BRIGHT(p.name),
    model: {p1: BODY.includes(p.name) ? AVATAR(p.name) : p.name.startsWith('scythe') ? SCYTHE : LEGS.includes(p.name) ? itemId('wing_' + p.name.slice(-1)) : itemId(p.name),
      p2: BODY.includes(p.name) ? itemId('p2/' + p.name) : p.name.startsWith('scythe') ? SCYTHE : LEGS.includes(p.name) ? itemId('leg_' + p.name.slice(-1)) : itemId(p.name)},
    rest: Object.fromEntries(FORMS.map(f => [f, written(REST[f].d[p.name])]))})),
  shadow: {uuid: uuidOf('shadow'), tags: SHADOW_TAGS},
  clips: Object.fromEntries(CLIP_NAMES.map(n => [n, clipInfo[n]])),
  looks: LOOKS, arm_layout: STUB.arm_layout, anchors: STUB.anchors, calls: STUB.calls, macro_calls: STUB.macro_calls,
  stored_looks: Object.fromEntries(Object.entries(STORE).map(([k, v]) => [k, OBJ + v])),
  tags: {part: 'rlk_kn_part', anchor: 'rlk_kn_anchor', per_part: 'rlk_kn_<part>', all: ['rlk_room', 'rlk_mb_aux', 'rlk_mb_part', 'rlk_kn_part']},
  objectives: OBJS, culling: CULL, view_range: VIEW_RANGE, storage: {anchors: 'rlk:kn rig.an', version: anVer},
  reused_models: {avatar: BODY.map(AVATAR), scythe: SCYTHE, skin: 'rlk:skin/arlecchino'},
  budgets: {atlas_px: atlasPx, atlas_budget: ATLAS_BUDGET, sprites: Object.keys(ledger).length, elements_at_rest: ELEMENTS, elements_budget: EL_BUDGET,
    parts: PART_NAMES.length, models: Object.keys(models).length, key_files: keyFiles, keys: keyLines, rig_functions: fnFiles.files, rig_bytes: fnFiles.bytes,
    edge_warn_ticks: edgeWarn.length},
  sprites: ledger,
};
json(path.join(here, 'arlecchino_rig_manifest.json'), manifest);
console.log(`Built the Arlecchino rig: ${PART_NAMES.length} parts, ${CLIPS.length} clips (${missing.length} stand-ins), ${keyFiles} key files, ${keyLines} keys, ${fnFiles.files} rig functions ` +
  `(${(fnFiles.bytes / 1e6).toFixed(2)} MB), ${Object.keys(models).length} models, ${Object.keys(ledger).length} sprites ${(atlasPx / 1e6).toFixed(3)} M px, elements at rest ` +
  `${FORMS.map(f => f + ' ' + ELEMENTS[f]).join(' / ')} [${((Date.now() - t0) / 1000).toFixed(1)} s]`);
if (debugDp) {
  fs.rmSync(path.join(debugDp, 'data/rlk/function/boss/arlecchino/rig'), {recursive: true, force: true});
  fs.cpSync(rigDir, path.join(debugDp, 'data/rlk/function/boss/arlecchino/rig'), {recursive: true});
  if (!fs.existsSync(path.join(debugDp, 'pack.mcmeta'))) fs.copyFileSync(path.join(dp, 'pack.mcmeta'), path.join(debugDp, 'pack.mcmeta'));
  for (const f of FORMS) putDebug(`kn_dbg/rest_${f}`, [...PART_NAMES.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(written(REST[f].d[n]))}}`),
    ...PART_NAMES.map(n => swap(n, REST[f].m[n]))]);
  putDebug('kn_dbg/player', ['summon minecraft:item_display ~2.2 ~ ~ {Tags:["kn_dbg_player"],item_display:"none",transformation:{translation:[0f,0.9f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,1.8f,0.3f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"minecraft:light_blue_concrete"}}}']);
}
