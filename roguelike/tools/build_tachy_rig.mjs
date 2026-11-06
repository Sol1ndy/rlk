// Display-entity rig of 타키 (Tachy, the special boss; S:tk/PLAN.md §2-3, contract S:tk/contract.md §3.2, frozen table
// tools/mboss_tachy/api.py §7 via tools/mboss_tachy/stub_rig_manifest.json). Built on the shared RIGLIB
// (mboss_rig_compile.mjs, mboss_rig_clips.mjs, mboss_model_lib.mjs, mboss_shape_lib.mjs, mboss_paint_lib.mjs,
// mboss_rig_math.mjs, all unchanged). API note: tools/tachy_rig_api.md.
//
// node tools/build_tachy_rig.mjs --resourcepack <unpacked RP> [--datapack <dp>] [--no-paint] [--allow-steps]
//                                [--debug-dp <scratch dir> [--debug-clips a,b | all] [--debug-step N]]
//
// Writes (owned, rebuilt from scratch on every run)
//   DP  data/rlk/function/boss/tachy/rig/**
//   RP  assets/rlk/textures/mboss/tachy/*, assets/rlk/models/item/mboss/tachy/*, assets/rlk/items/mboss/tachy/* and the
//       items-atlas entries rlk:mboss/tachy/*
//   tools/tachy_rig_manifest.json (the stub's schema + transforms, budgets, sprites; api.check_manifest passes)
// The build throws on: a part or prop below the feet at any compiled tick, a clip / event / loop that differs from the
// contract, a rotation above 120 degrees per tick or per key, the atlas over 0.52 M px, more than 6 500 elements at
// rest, a model outside -16..32 (--allow-steps turns the motion checks into warnings while authoring).
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {PARTS, PART_NAMES, PART_SCALE, PART_BRIGHT, WINGS, TENDRILS, FORM_MODELS, VISOR_MODELS, EDGE_MODELS, CHEST_MODELS, HAND_MODELS,
  SCABBARD_MODELS, TINTED, TINTED_MODELS, allModels} from './tachy_geometry.mjs';
import {tachySprites, paintTachy, spriteId} from './tachy_paint.mjs';
import {solve, toDisplay, fromDisplay, setModels, worldPoints, modelOn, SK, HIP_Y} from './tachy_pose.mjs';
import {CLIPS as AUTHORED, accumulate, sampleClip, DEFAULT_POSE} from './tachy_clips.mjs';
import {createRigCompiler, createRigFollow, nbt, written, interp, shown, summonPart, summonShadow, cullOverhang} from './mboss_rig_compile.mjs';
import {qAngle, len, sub, add, rot, unit, times, basisQ, cross, perp} from './mboss_rig_math.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const arg = n => { const i = process.argv.indexOf(n); return i < 0 ? null : process.argv[i + 1]; };
const flag = n => process.argv.includes(n);
const dp = path.resolve(arg('--datapack') || path.join(here, '..'));
const rp = arg('--resourcepack') && path.resolve(arg('--resourcepack'));
if (!rp) throw new Error('--resourcepack <unpacked pack> is required');
const put = (p, s) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, s.endsWith('\n') ? s : s + '\n'); };
const json = (p, o) => put(p, JSON.stringify(o, null, 1));
const t0 = Date.now();
const NS = 'rlk:boss/tachy/rig';
const rigDir = path.join(dp, 'data/rlk/function/boss/tachy/rig');
fs.rmSync(rigDir, {recursive: true, force: true});
let fnCount = 0;
const runnerPatch = {};
const fn = (n, lines) => {
  let L = Array.isArray(lines) ? lines : [lines];
  const m = /^c\/([a-z0-9_]+)\/run$/.exec(n);
  if (m && runnerPatch[m[1]]) L = runnerPatch[m[1]](L);
  put(path.join(rigDir, n + '.mcfunction'), L.join('\n')); fnCount++;
};
const OBJ = 'tkRig';

// ---- contract (D0 stub = api.py) ---------------------------------------------------------------------------------------------
const STUB = JSON.parse(fs.readFileSync(path.join(here, 'mboss_tachy/stub_rig_manifest.json'), 'utf8'));
if (JSON.stringify(STUB.parts.map(p => p.name)) !== JSON.stringify(PART_NAMES)) throw new Error('parts differ from the contract');
const CONTRACT = STUB.clips;                    // {name: {id, len, loop, events, form}}
const CLIP_NAMES = Object.keys(CONTRACT).sort((a, b) => CONTRACT[a].id - CONTRACT[b].id);
const LOOKS = STUB.looks;
const FORMS = LOOKS.form;                        // cape, winged, abyss
const FORM_ID = Object.fromEntries(FORMS.map((f, i) => [f, i]));

// ---- ids, UUIDs, tags --------------------------------------------------------------------------------------------------------
const UUID_HI = [0x524c4b4d | 0, 0x544b4900 | 0, 0x80000000 | 0];
const NN = n => (n === 'shadow' ? 0x40 : PART_NAMES.indexOf(n));
const uuidOf = n => `524c4b4d-544b-4900-8000-${NN(n).toString(16).padStart(12, '0')}`;
const uuidInts = n => [...UUID_HI, NN(n)];
const itemId = m => `rlk:mboss/tachy/${m}`;
const TAGS = n => ['rlk_room', 'rlk_mb_aux', 'rlk_mb_part', 'rlk_tk_part', 'rlk_tk_' + n];
const SHADOW_TAGS = ['rlk_room', 'rlk_mb_aux', 'rlk_tk_part', 'rlk_tk_shadow'];
const CULL = {width: 10, height: 12.5}, VIEW_RANGE = 2;   // R2: x FIG (the figure 1.25 x the D0 design)
const swap = (n, model) => `data modify entity ${uuidOf(n)} item.components."minecraft:item_model" set value "${itemId(model)}"`;

// ---- resource pack: models, items, sprites, atlas ----------------------------------------------------------------------------
const models = allModels();
setModels(models);
const assets = path.join(rp, 'assets/rlk');
const modelDir = path.join(assets, 'models/item/mboss/tachy'), itemDir = path.join(assets, 'items/mboss/tachy');
for (const d of [modelDir, itemDir]) fs.rmSync(d, {recursive: true, force: true});
const sprites = tachySprites();
if (!flag('--no-paint')) paintTachy(rp, sprites);
const usedSprites = new Set();
for (const [name, els] of Object.entries(models)) {
  const used = [...new Set(els.flatMap(e => Object.values(e.faces).map(f => f.texture.slice(1))))].sort();
  const tex = {};
  for (const u of used) { if (!sprites[u]) throw new Error(`model ${name}: unknown sprite ${u}`); tex[u] = spriteId(u); usedSprites.add(u); }
  json(path.join(modelDir, name + '.json'), {ambientocclusion: false, textures: {...tex, particle: tex[used[0]] || spriteId('tk_black')}, elements: els});
  if (!TINTED_MODELS.has(name)) json(path.join(itemDir, name + '.json'), {model: {type: 'minecraft:model', model: 'rlk:item/mboss/tachy/' + name}});
}
for (const [item, [m, rgb]] of Object.entries(TINTED)) json(path.join(itemDir, item + '.json'), {model: {type: 'minecraft:model', model: 'rlk:item/mboss/tachy/' + m, tints: [{type: 'minecraft:constant', value: rgb}]}});
const unused = Object.keys(sprites).filter(n => !usedSprites.has(n));
if (unused.length) throw new Error(`painted but unused sprites: ${unused.join(', ')}`);
const ledger = {}; let atlasPx = 0;
for (const [n, [w, h]] of Object.entries(sprites)) {
  if (w > 512 || h > 1024 || w % 16 || h % 16) throw new Error(`sprite ${n} ${w}x${h}: sides multiples of 16`);
  ledger[n] = w * h; atlasPx += w * h;
}
const ATLAS_BUDGET = 520000;
if (atlasPx > ATLAS_BUDGET) throw new Error(`atlas ${atlasPx} px > ${ATLAS_BUDGET}`);
// elements shown at rest per form (every part's default model, the form's wings, sword + edge, the visor / chest glows)
const ecount = m => (models[m] || []).length;
const restModels = form => PART_NAMES.map(n => (WINGS.includes(n) ? FORM_MODELS[form][n] : n === 'sword_edge' ? 'edge_p' : n === 'visor_glow' ? 'skull' : n === 'chest_glow' ? 'grid'
  : TENDRILS.includes(n) ? (form === 'abyss' ? 'tendril' : 'empty') : PARTS.find(p => p[0] === n)[1]));
const ELEMENTS = Object.fromEntries(FORMS.map(f => [f, restModels(f).reduce((a, m) => a + ecount(m), 0)]));
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

// ---- the intro cables (computed from the intro's hang pose, tick 0): 6 strands from the lamp machine 25 b up to her wrists,
// shoulders and hips; 3 segments each. At a snap a strand's segments recoil toward the lamp (to 30 % of their length).
const f4 = x => String(+(+x).toFixed(4));
const qArr = Q => `[${Q.map(v => f4(v) + 'f').join(',')}]`;
const CAB_W = .05, LAMP_Y = 25, RECOIL = .3;
function cableSeg(A, B, w = CAB_W) {
  // the unit cable model from A to B (rig frame, blocks from the anchor), display frame = z mirrored
  const d = sub(B, A), L = len(d), Y = unit(d);
  let X = perp([1, 0, 0], Y); X = len(X) < 1e-3 ? unit(perp([0, 0, 1], Y)) : unit(X);
  const Q = basisQ(X, Y, cross(X, Y));
  return `{translation:[${f4(A[0])}f,${f4(A[1])}f,${f4(-A[2])}f],left_rotation:${qArr([-Q[0], -Q[1], Q[2], Q[3]])},scale:[${f4(w)}f,${f4(L)}f,${f4(w)}f],right_rotation:[0f,0f,0f,1f]}`;
}
let CABLES = {strands: [], lampY: LAMP_Y, recoil: RECOIL};
function computeCables(o) {
  const at = [o.hand_l.t, o.hand_r.t, o.upper_arm_l.t, o.upper_arm_r.t, add(o.pelvis.t, [.22, 0, .06]), add(o.pelvis.t, [-.22, 0, .06])];
  CABLES = {lampY: LAMP_Y, recoil: RECOIL, strands: at.map((P, i) => {
    const a = (i * 60 + 30) * Math.PI / 180, top = [1.3 * Math.sin(a), LAMP_Y, 1.3 * Math.cos(a)];
    const pts = [0, 1, 2, 3].map(j => { const u = j / 3, sag = .35 * Math.sin(Math.PI * u); return add(add(top, times(sub(P, top), u)), [sag * Math.sin(a + 1), 0, sag * Math.cos(a + 1)]); });
    return {top, at: P, segs: [[pts[0], pts[1]], [pts[1], pts[2]], [pts[2], pts[3]]]};
  })};
}
const cableSnapLines = i => CABLES.strands[i].segs.map(([A, B], j) => {
  const k = RECOIL, top = CABLES.strands[i].top;
  return `data merge entity @e[type=item_display,tag=rlk_tk_cbl_${i}_${j},limit=1,sort=nearest] {start_interpolation:0,interpolation_duration:6,transformation:${cableSeg(add(top, times(sub(A, top), k)), add(top, times(sub(B, top), k)))}}`;
});
// ---- per-clip solve -------------------------------------------------------------------------------------------------------
// forms a clip is compiled for: its contract form (+ formAt switches) or all three (the wing / tendril parts differ)
const formAt = (c, t, base) => { let f = base; for (const [tt, ff] of Object.entries(c.formAt || {}).sort((a, b) => a[0] - b[0])) if (t >= +tt) f = ff; return f; };
const variantsOf = c => (c.form ? [c.form] : FORMS);
const CHAIN = new Set([...WINGS, ...TENDRILS]);
// two passes: the floor guards of the chains (cape / wing segments, tendrils) are planned over the whole clip so that a guard
// angle never changes faster than GUARD_SLOPE degrees per tick (a dilation of the first pass's angles), then solved again
const GUARD_SLOPE = 22;
function solveClip(c, form) {
  const run = plan => {
    const ks = accumulate(c), out = [];
    const warm = c.loop && c.loop[1] === c.len ? c.len : 0;   // loops settle their secondary motion over one silent cycle
    const hist = k => out[out.length - k] || null;
    for (let i = 0; i <= warm + c.len; i++) {
      const t = i - warm, tt = t < 0 ? t + c.len : t;
      const p = sampleClip(c, tt, ks);
      const o = solve(p, formAt(c, tt, form), k => hist(k)?.o || null, plan ? plan[tt] : {});
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
// tolerances (display space): translation 0.012 b (0.03 on the long / soft parts), rotation by the part's reach
const TOL = {t: .012, s: .015, rDefault: 1.2,
  r: {sword: .5, sword_edge: .5, scabbard: .8, wing_l1: 1, wing_r1: 1, wing_l2: 1.2, wing_r2: 1.2, wing_l3: 1.5, wing_r3: 1.5, hair_1: 2.5, hair_2: 2.5, hair_3: 3,
    tendril_l: 2, tendril_r: 2, thigh_l: 1, thigh_r: 1, shin_l: 1, shin_r: 1, upper_arm_l: 1, upper_arm_r: 1, forearm_l: 1, forearm_r: 1},
  tp: {sword: .02, sword_edge: .02, hair_1: .025, hair_2: .03, hair_3: .03, wing_l2: .03, wing_r2: .03, wing_l3: .04, wing_r3: .04, tendril_l: .03, tendril_r: .03}};
const compiler = createRigCompiler({ns: NS, obj: OBJ, fn, parts: PART_NAMES, uuidOf, tol: TOL});
const debugDp = arg('--debug-dp') && path.resolve(arg('--debug-dp'));
const debugClips = (arg('--debug-clips') || 'all').split(',');
const debugStep = +(arg('--debug-step') || 1);
if (debugDp) fs.rmSync(path.join(debugDp, 'data/rlk/function/tk_dbg'), {recursive: true, force: true});
const putDebug = (n, lines) => put(path.join(debugDp, 'data/rlk/function', n + '.mcfunction'), lines.join('\n'));
// segments with forced boundaries
function segmentsCut(seq, n, cuts, minFirst) {
  const bounds = [...new Set([0, ...cuts.filter(t => t > 0 && t < seq.length - 1), seq.length - 1])].sort((a, b) => a - b), out = [];
  for (let i = 0; i < bounds.length - 1; i++) {
    const a = bounds[i], b = bounds[i + 1];
    // the blend-in (first segment >= minFirst ticks) only where it turns less than 110 degrees
    let mf = i === 0 ? minFirst : 1;
    if (mf > 1 && shown(seq[a]) && shown(seq[Math.min(b, a + mf)]) && qAngle(seq[a].q, seq[Math.min(b, a + mf)].q) > 110) mf = 1;
    for (const [x, y] of compiler.segments(seq.slice(a, b + 1), n, mf)) out.push([x + a, y + a]);
  }
  return out;
}
// the value the client shows at each tick for a segment list (interp of the written keys)
function compiled(seq, segs) {
  const W = seq.map(written), out = new Array(seq.length);
  out[0] = W[0];
  for (const [a, b] of segs) for (let t = a + 1; t <= b; t++) out[t] = interp(W[a], W[b], (t - a) / (b - a));
  return out;
}
const sameD = (x, y) => len(sub(x.t, y.t)) < 1e-5 && qAngle(x.q, y.q) < .01 && x.s.every((v, i) => Math.abs(v - y.s[i]) < 1e-5);
const lookLines = [];   // filled below (look functions are written after the clips)
const clipInfo = {}, motionErrors = [], floorErrors = [], cullWarn = [], warns = [];
let keyFiles = 0, keyLines = 0;
const STORE = {visor: 'V', edge: 'E', chest: 'G', hands: 'H'};
const LOOK_MODELS = {visor: VISOR_MODELS, edge: EDGE_MODELS, chest: CHEST_MODELS};
const LOOK_PART = {visor: 'visor_glow', edge: 'sword_edge', chest: 'chest_glow'};
// temporary look value names of a clip (lk/<channel>/<value>): edge glint / yellow / pyro / electro / off, chest amber / red /
// gold / off, visor pyro / electro / abyss / off (down_* models)
const tmpModel = (ch, v) => (ch === 'visor' ? VISOR_MODELS[v === 'off' ? 'down_off' : 'down_' + v] : LOOK_MODELS[ch][v]);
const usedTmp = new Set();
const previewForm = c => c.form || c.preview || 'cape';
computeCables(solveClip(CLIPS.find(c => c.name === 'intro'), 'cape')[0].o);
for (const c of CLIPS) {
  const vars = variantsOf(c), F = Object.fromEntries(vars.map(f => [f, solveClip(c, f)]));
  const base = F[vars[0]];
  const cuts = [...(c.cuts || []), ...Object.keys(c.swapAt || {}).map(Number)];
  const byTick = new Map(), add_ = (t, l) => { if (!byTick.has(t)) byTick.set(t, []); byTick.get(t).push(l); };
  let keys = 0;
  const compiledD = {};               // per form: {part: [display per tick]}
  for (const f of vars) compiledD[f] = {};
  for (const n of PART_NAMES) {
    const isChain = CHAIN.has(n) && vars.length > 1;
    // group forms whose sequences are identical for this part
    const groups = [];
    for (const f of (isChain ? vars : [vars[0]])) {
      const seq = F[f].map(fr => fr.d[n]);
      const g = groups.find(G => G.seq.every((v, i) => sameD(v, seq[i])));
      if (g) g.forms.push(f); else groups.push({seq, forms: [f]});
    }
    for (const G of groups) {
      let segs = segmentsCut(G.seq, n, CHAIN.has(n) || n.startsWith('hand') ? cuts : cuts.filter(t => (c.cutAll || []).includes(t)), c.blend ?? 3);
      // a segment whose client interpolation dips below the floor is split at its lowest tick (until none dips)
      const fr0 = F[G.forms[0]];
      const lowAt = (t, v) => { const P = worldPoints(modelOn(n, fr0[t].p, formAt(c, t, G.forms[0])), n, fromDisplay(n, v)); return P.length ? Math.min(...P.map(x => x[1])) : 1; };
      for (let guard = 0; guard < 400; guard++) {
        const W = G.seq.map(written); let worst = null;
        for (const [a, b] of segs) for (let t = a + 1; t < b; t++) {
          const y = lowAt(t, interp(W[a], W[b], (t - a) / (b - a)));
          if (y < -.005 && (!worst || y < worst.y)) worst = {a, b, t, y};
        }
        if (!worst) break;
        segs = segs.flatMap(([a, b]) => (a === worst.a && b === worst.b ? [[a, worst.t], [worst.t, b]] : [[a, b]]));
      }
      // the keys as shipped: {at, dur, to}. A model swap at a cut tick b (a 1-tick segment turning > 60 deg) is a snap: a
      // 0-tick key at b, and the segment that starts at b starts one tick later (two keys in one tick would merge into one)
      const snapAt = new Set(cuts), keyList = [];
      let snapped = -1;
      for (const [a, b] of segs) {
        const turn = qAngle(G.seq[a].q, G.seq[b].q);
        if (b - a === 1 && snapAt.has(b) && turn > 60) { keyList.push({at: b, dur: 0, to: b}); snapped = b; continue; }
        if (turn > 118 && shown(G.seq[a]) && shown(G.seq[b])) motionErrors.push(`${c.name} ${n} t${a}-${b}: ${turn.toFixed(0)} degree key (ambiguous slerp)`);
        if (a === snapped) keyList.push({at: a + 1, dur: b - a - 1, to: b});
        else keyList.push({at: a, dur: b - a, to: b});
      }
      // what the client shows each tick (the first key starts from the clip's own tick-0 pose)
      const W = G.seq.map(written), cv = new Array(G.seq.length);
      {
        let st = W[0], from = W[0], k0 = 0, d = 0, tgt = W[0];
        const byAt = new Map(keyList.map(k => [k.at, k]));
        for (let t = 0; t < G.seq.length; t++) {
          const cur = d > 0 && t < k0 + d ? interp(from, tgt, (t - k0) / d) : tgt;
          const k = byAt.get(t);
          if (k) { from = t === 0 ? W[0] : cur; tgt = W[k.to]; k0 = t; d = k.dur; }
          st = d > 0 && t < k0 + d ? interp(from, tgt, (t - k0) / d) : tgt;
          cv[t] = st;
        }
      }
      for (const f of (isChain ? G.forms : vars)) compiledD[f][n] = cv;
      const ids = G.forms.map(f => FORM_ID[f]), lo = Math.min(...ids), hi = Math.max(...ids);
      const guard = isChain && groups.length > 1 ? `execute if score @s ${OBJ}Form matches ${lo === hi ? lo : lo + '..' + hi} run ` : '';
      for (const k of keyList) { add_(k.at, `${guard}data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:${k.dur},transformation:${nbt(G.seq[k.to])}}`); keys++; }
    }
  }
  // per-tick checks on what ships: floor, culling, 1-tick turns
  for (const f of vars) {
    const fr = F[f];
    for (let t = 0; t <= c.len; t++) {
      for (const n of PART_NAMES) {
        const v = compiledD[f][n][t];
        if (!shown(v)) continue;
        const pts = worldPoints(modelOn(n, fr[t].p, formAt(c, t, f)), n, fromDisplay(n, v));
        if (!pts.length) continue;
        const y = Math.min(...pts.map(P => P[1]));
        if (y < -.01) floorErrors.push(`${c.name}[${f}] t${t} ${n}: lowest point ${y.toFixed(3)} b`);
        const over = Math.max(...pts.map(P => cullOverhang(P, CULL)));
        if (over > 0) cullWarn.push(`${c.name}[${f}] t${t} ${n} ${over.toFixed(2)} b`);
        if (t && !cuts.includes(t) && shown(compiledD[f][n][t - 1])) { const a = qAngle(compiledD[f][n][t - 1].q, v.q); if (a > 120) motionErrors.push(`${c.name}[${f}] ${n} t${t - 1}->${t}: ${a.toFixed(0)} degrees`); }
      }
    }
  }
  // discrete channels: hands, scabbard (at tick 0 and where they change)
  const handModel = (k, p) => modelOn('hand_' + k, p, 'cape');
  base.forEach((fr, t) => {
    for (const k of ['l', 'r']) if (t === 0 || handModel(k, fr.p) !== handModel(k, base[t - 1].p)) add_(t, swap('hand_' + k, handModel(k, fr.p)));
    const sc = modelOn('scabbard', fr.p, 'cape');
    if (t === 0 || sc !== modelOn('scabbard', base[t - 1].p, 'cape')) add_(t, swap('scabbard', sc));
  });
  // tick 0: show a hidden rig, enforce the clip's form
  const head0 = [`execute if score @s ${OBJ}S matches 1 run scoreboard players set @s ${OBJ}S 0`];
  if (c.form) head0.push(`execute unless score @s ${OBJ}Form matches ${FORM_ID[c.form]} run function ${NS}/look/form/${c.form}`);
  for (const l of head0.reverse()) byTick.has(0) ? byTick.get(0).unshift(l) : add_(0, l);
  for (const [t, f] of Object.entries(c.swapAt || {})) add_(+t, `function ${NS}/look/form/${f}`);
  for (const [t, ch, v] of c.looks || []) {
    if (v.startsWith('set:')) add_(t, `function ${NS}/look/${v.slice(4)}`);
    else if (v === 'restore') add_(t, `function ${NS}/lk/${ch}/restore`);
    else { usedTmp.add(`${ch}/${v}`); add_(t, `function ${NS}/lk/${ch}/${v}`); }
  }
  for (const [t, L] of Object.entries(c.lines || {})) for (const l of L) add_(+t, l);
  for (const [t, I] of Object.entries(c.cableSnaps || {})) for (const i of I) for (const l of cableSnapLines(i)) add_(+t, l);
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
      if (part.length > 8) throw new Error('dispatch group too large');
      fn(name, leaf(part));
      out.push(`execute if score @s ${OBJ}T matches ..${part[part.length - 1]} run return run function ${NS}/${name}`);
    }
    if (out.length > 12) {   // two levels
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
  clipInfo[c.name] = {id: c.id, len: c.len, loop: c.loop, events: c.events, form: c.form, compiled_forms: vars, key_files: ticks.length, keys,
    keys_per_tick: +(keys / (c.len + 1)).toFixed(1), preview_form: previewForm(c), source: c.src || ''};
  // debug: exact compiled values every debugStep ticks for the preview form
  if (debugDp && (debugClips.includes('all') || debugClips.includes(c.name))) {
    const f = vars.includes(previewForm(c)) ? previewForm(c) : vars[0];
    const looks = lookTimeline(c);
    for (let t = 0; t <= c.len; t += debugStep) {
      const p = F[f][t].p, ff = formAt(c, t, f), L = looks(t);
      putDebug(`tk_dbg/${c.name}/${t}`, [...PART_NAMES.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(written(compiledD[f][n][t]))}}`),
        ...WINGS.map(n => swap(n, FORM_MODELS[t >= swapTick(c, ff) ? ff : (c.formBefore || ff)][n])),
        swap('hand_l', modelOn('hand_l', p, ff)), swap('hand_r', modelOn('hand_r', p, ff)), swap('scabbard', modelOn('scabbard', p, ff)),
        swap('visor_glow', L.visor), swap('sword_edge', L.edge), swap('chest_glow', L.chest),
        // the intro's cable props as the seq shows them: summoned at the start, the snapped strands recoiled, cleared at stance
        ...(c.cableSnaps && t < (c.events.stance ?? 1e9) ? [`function ${NS}/prop/cables`, ...Object.entries(c.cableSnaps).filter(([tt]) => +tt <= t)
          .flatMap(([, I]) => I.flatMap(i => cableSnapLines(i).map(l => l.replace('interpolation_duration:6', 'interpolation_duration:0'))))] : [])]);
    }
  }
}
function swapTick(c, f) { const e = Object.entries(c.swapAt || {}).find(([, ff]) => ff === f); return e ? +e[0] : 0; }
// the look models over a clip's ticks (debug renders): the fight defaults (visor pyro, edge pyro, chest off) and the clip's events
function lookTimeline(c) {
  const st = {visor: c.lookStart?.visor || 'down_pyro', edge: c.lookStart?.edge || 'pyro', chest: c.lookStart?.chest || 'off'};
  const ev = (c.looks || []).slice().sort((a, b) => a[0] - b[0]);
  return t => {
    const s = {...st}, tmp = {};
    for (const [tt, ch, v] of ev) {
      if (tt > t) break;
      if (v.startsWith('set:')) { const [cc, vv] = v.slice(4).split('/'); s[cc] = vv; delete tmp[cc]; } else if (v === 'restore') delete tmp[ch]; else tmp[ch] = v;
    }
    return {visor: tmp.visor ? tmpModel('visor', tmp.visor) : VISOR_MODELS[s.visor], edge: tmp.edge ? EDGE_MODELS[tmp.edge] : EDGE_MODELS[s.edge],
      chest: tmp.chest ? CHEST_MODELS[tmp.chest] : CHEST_MODELS[s.chest]};
  };
}
const fail = (title, list) => { if (list.length) { const m = `${title}:\n  ${list.slice(0, +(arg('--show') || 40)).join('\n  ')}${list.length > 40 ? `\n  ... ${list.length} in all` : ''}`; if (flag('--allow-steps')) console.warn(m); else throw new Error(m); } };
fail('floor (no shown element below the feet)', floorErrors);
fail('rotations above 120 degrees per tick or per key', motionErrors);
if (cullWarn.length) fail('culling box overhang', cullWarn);
compiler.writeDispatch(CLIPS.map(c => ({id: c.id, name: c.name})));

// ---- follow, init, spawn, tick ----------------------------------------------------------------------------------------------
const follow = createRigFollow({ns: NS, obj: OBJ, fn, uuidOf, lists: {all: PART_NAMES}, fixed: ['shadow'], staticSkip: true,
  comment: '# Parts follow the anchor position and yaw (run as and rotated as the boss at its feet, pitch 0).'});
follow.write();
const OBJS = [`${OBJ}C`, `${OBJ}T`, `${OBJ}F`, `${OBJ}Y`, `${OBJ}S`, `${OBJ}Form`, `${OBJ}V`, `${OBJ}E`, `${OBJ}G`, `${OBJ}H`, ...follow.objectives];
fn('init', ['# Rig objectives (safe on every load). tkRigC clip id, tkRigT clip tick (-1 = queued), tkRigF hit flash, tkRigY face scratch,',
  '# tkRigS state (0 normal, 1 hidden), tkRigForm (0 cape, 1 winged, 2 abyss), stored looks tkRigV visor, tkRigE edge, tkRigG chest,',
  '# tkRigH hands (indices of api.LOOKS); tkRigQ* the follow cache.', ...OBJS.map(o => `scoreboard objectives add ${o} dummy`)]);
// rest pose of each form (the idle clip's tick 0)
const idleClip = CLIPS.find(c => c.name === 'idle');
const REST = Object.fromEntries(FORMS.map(f => { const fr = solveClip(idleClip, f)[0]; return [f, Object.fromEntries(PART_NAMES.map(n => [n, fr.d[n]]))]; }));
const summon = n => summonPart({uuid: uuidInts(n), tags: TAGS(n), item: itemId(n === 'scabbard' ? 'scabbard' : PARTS.find(p => p[0] === n)[1]), brightness: PART_BRIGHT[n],
  pose: REST.cape[n], viewRange: VIEW_RANGE, cull: CULL});
fn('spawn', ['# @s = the boss (the anchor), at its feet. Kills old parts, summons the 40 parts (fixed UUIDs 524c4b4d-544b-4900-8000-0000000000NN) and the',
  '# shadow helper (…40) in the rest pose, re-applies the stored form and looks, and queues idle.', `function ${NS}/init`, `function ${NS}/kill`,
  `execute unless score @s ${OBJ}Form matches 0..2 run scoreboard players set @s ${OBJ}Form 0`,
  `execute unless score @s ${OBJ}V matches 0..4 run scoreboard players set @s ${OBJ}V 1`,
  `execute unless score @s ${OBJ}E matches 0..4 run scoreboard players set @s ${OBJ}E 2`,
  `execute unless score @s ${OBJ}G matches 0..3 run scoreboard players set @s ${OBJ}G 0`,
  `execute unless score @s ${OBJ}H matches 0..2 run scoreboard players set @s ${OBJ}H 1`,
  `scoreboard players set @s ${OBJ}S 0`, `scoreboard players set @s ${OBJ}F 0`,
  ...PART_NAMES.map(summon), summonShadow({uuid: uuidInts('shadow'), tags: SHADOW_TAGS, item: itemId('empty'), radius: 1.4, strength: .7, viewRange: VIEW_RANGE, cull: CULL}),
  `function ${NS}/look_apply`, `function ${NS}/play/idle`, `execute rotated as @s rotated ~ 0 run function ${NS}/follow_now`]);
fn('tick', ['# @s = the boss (the anchor), at its feet, once per game tick (the core calls it). Missing parts respawn; hidden: only the',
  '# follow runs until a clip is queued (its tick 0 shows the rig again).',
  `execute unless entity ${uuidOf('pelvis')} run function ${NS}/spawn`,
  `execute rotated as @s rotated ~ 0 run function ${NS}/follow`,
  `execute if score @s ${OBJ}F matches 1.. run function ${NS}/flash_tick`,
  `execute if score @s ${OBJ}S matches 1 unless score @s ${OBJ}T matches -1 run return 0`,
  `scoreboard players add @s ${OBJ}T 1`, `function ${NS}/run`]);
fn('kill', ['# Removes every rig part and the shadow helper (props: prop/clear).', 'kill @e[type=item_display,tag=rlk_tk_part]']);
fn('uninstall', ['# Removes the rig, its props, the face marker and the rig objectives.', `function ${NS}/kill`, `function ${NS}/prop/clear`,
  'kill @e[type=marker,tag=rlk_tk_face]', ...OBJS.map(o => `scoreboard objectives remove ${o}`)]);
// state
fn('state/hidden', ['# Hidden (blink gone, the high hover out of sight): every part at scale 0 where it stands (never moved, never below the floor),',
  '# no clip runs, the parts keep following the anchor. The next play/start shows the rig again. @s = the boss.',
  `scoreboard players set @s ${OBJ}S 1`, `scoreboard players set @s ${OBJ}T 0`,
  ...PART_NAMES.map(n => `data modify entity ${uuidOf(n)} transformation.scale set value [0f,0f,0f]`)]);
fn('state/normal', ['# Visible again. From hidden: the current clip restarts from its tick 0 at the next rig/tick (its keys show every part);',
  '# already visible: nothing changes (pattern cancels call it freely). @s = the boss.',
  `execute if score @s ${OBJ}S matches 1 run scoreboard players set @s ${OBJ}T -1`, `scoreboard players set @s ${OBJ}S 0`]);
// flash (hit feedback 3 t)
const FLASH = PART_NAMES.filter(n => !['visor_glow', 'chest_glow', 'sword_edge', 'tendril_l', 'tendril_r'].includes(n));
fn('flash', ['# Hit feedback: the body outlines white-gold for 3 ticks. @s = the boss.', `scoreboard players set @s ${OBJ}F 3`,
  ...FLASH.map(n => `data merge entity ${uuidOf(n)} {Glowing:1b,glow_color_override:16774320}`)]);
fn('flash_tick', ['# Internal: counts the flash down.', `scoreboard players remove @s ${OBJ}F 1`, `execute if score @s ${OBJ}F matches ..0 run function ${NS}/flash_off`]);
fn('flash_off', ['# Internal: end of the hit flash.', `scoreboard players set @s ${OBJ}F 0`, ...FLASH.map(n => `data merge entity ${uuidOf(n)} {Glowing:0b}`)]);
compiler.writeFace({marker: 'rlk_tk_face', maxDeg: 12});

// ---- looks ----------------------------------------------------------------------------------------------------------------------
// form: wing models, tendril visibility, and the form's rest pose for the wings / tendrils (4 t) until the next clip key
for (const f of FORMS) {
  fn(`look/form/${f}`, [`# Form ${f}: the wing models${f === 'abyss' ? ' (+ dark red flesh) and the tendrils shown' : f === 'cape' ? ' as the folded-wing cape' : ' (blade feathers)'}; wings and tendrils ease to the form's rest pose (the next clip key takes over). @s = the boss.`,
    `scoreboard players set @s ${OBJ}Form ${FORM_ID[f]}`, ...WINGS.map(n => swap(n, FORM_MODELS[f][n])),
    ...[...WINGS, ...TENDRILS].map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:4,transformation:${nbt(written(REST[f][n]))}}`)]);
}
const lookFn = (ch, vals, part, models) => vals.forEach((v, i) => fn(`look/${ch}/${v}`, [`# Look ${ch} = ${v} (stored in ${OBJ}${STORE[ch]} = ${i}). @s = the boss.`,
  `scoreboard players set @s ${OBJ}${STORE[ch]} ${i}`, swap(part, models[v])]));
lookFn('visor', LOOKS.visor, 'visor_glow', VISOR_MODELS);
lookFn('edge', LOOKS.edge, 'sword_edge', EDGE_MODELS);
lookFn('chest', LOOKS.chest, 'chest_glow', CHEST_MODELS);
LOOKS.hands.forEach((v, i) => fn(`look/hands/${v}`, [`# Hands ${v} (stored in ${OBJ}H = ${i}; clips set their own hands). @s = the boss.`, `scoreboard players set @s ${OBJ}H ${i}`,
  swap('hand_l', HAND_MODELS.hand_l[v]), swap('hand_r', HAND_MODELS.hand_r[v])]));
// temporary looks of the clips (no store) and their restore
for (const k of usedTmp) { const [ch, v] = k.split('/'); fn(`lk/${ch}/${v}`, [`# Internal (clips): ${ch} shows ${v} for a moment; lk/${ch}/restore puts the stored look back.`, swap(LOOK_PART[ch], tmpModel(ch, v))]); }
for (const ch of ['visor', 'edge', 'chest']) fn(`lk/${ch}/restore`, [`# Internal (clips): the stored ${ch} look (${OBJ}${STORE[ch]}).`,
  ...LOOKS[ch].map((v, i) => `execute if score @s ${OBJ}${STORE[ch]} matches ${i} run ${swap(LOOK_PART[ch], LOOK_MODELS[ch][v])}`)]);
fn('look_apply', ['# Re-applies every stored look (spawn). @s = the boss.',
  ...FORMS.map((f, i) => `execute if score @s ${OBJ}Form matches ${i} run function ${NS}/look/form/${f}`),
  ...['visor', 'edge', 'chest'].map(ch => `function ${NS}/lk/${ch}/restore`),
  ...LOOKS.hands.map((v, i) => `execute if score @s ${OBJ}H matches ${i} run function ${NS}/look/hands/${v}`)]);

// ---- props: cables (the intro hang, PLAN §3 E0-E1) --------------------------------------------------------------------------------
fn('prop/cables', ['# The intro cables (PLAN §3 E0): 6 strands x 3 thin black segments from the overhead lamp machine (25 b up) to her body in the',
  '# hang (7 b up), at the execution position and yaw (run as / at the boss on the arena floor). Tags rlk_room rlk_mb_aux rlk_tk_prop',
  '# rlk_tk_prop_cables rlk_tk_cbl_<strand>_<segment>. The intro clip whips them up at its snap ticks; prop/clear removes them.',
  'kill @e[type=item_display,tag=rlk_tk_prop_cables]',
  ...CABLES.strands.flatMap((S, i) => S.segs.map(([A, B], j) => `summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_prop","rlk_tk_prop_cables","rlk_tk_cbl_${i}_${j}","rlk_tk_new"],billboard:"fixed",item_display:"none",view_range:2f,width:6f,height:28f,shadow_radius:0f,brightness:{block:7,sky:12},interpolation_duration:1,teleport_duration:0,transformation:${cableSeg(A, B)},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${itemId('cable')}"}}}`)),
  'execute rotated ~ 0 run tp @e[type=item_display,tag=rlk_tk_new] ~ ~ ~ ~ 0', 'tag @e[tag=rlk_tk_new] remove rlk_tk_new']);
fn('prop/clear', ['# Removes every rig prop.', 'kill @e[tag=rlk_tk_prop]']);

// ---- manifest ---------------------------------------------------------------------------------------------------------------------
const fnFiles = (() => { let n = 0, b = 0; const walk = d => { for (const f of fs.readdirSync(d, {withFileTypes: true})) { const p = path.join(d, f.name); if (f.isDirectory()) walk(p); else { n++; b += fs.statSync(p).size; } } }; walk(rigDir); return {files: n, bytes: b}; })();
const manifest = {
  schema: 1, id: 'tachy', source: 'rig',
  _doc: 'Tachy rig (tools/build_tachy_rig.mjs, API tools/tachy_rig_api.md): the D0 stub schema (parts, clips with id / len / loop / events / form, looks, props, calls) plus transforms, models, budgets and sprites. Generated: do not edit.',
  height: STUB.height, hip_y: STUB.hip_y, uuid: STUB.uuid,
  parts: STUB.parts.map(p => ({...p, uuid: uuidOf(p.name), tag: 'rlk_tk_' + p.name, model: PARTS.find(q => q[0] === p.name)[1], brightness: PART_BRIGHT[p.name], scale: PART_SCALE[p.name],
    rest: Object.fromEntries(FORMS.map(f => [f, written(REST[f][p.name])]))})),
  shadow: {uuid: uuidOf('shadow'), tags: SHADOW_TAGS},
  clips: Object.fromEntries(CLIP_NAMES.map(n => [n, clipInfo[n]])),
  looks: LOOKS, look_models: {form: FORM_MODELS, visor: VISOR_MODELS, edge: EDGE_MODELS, chest: CHEST_MODELS, hands: HAND_MODELS, scabbard: SCABBARD_MODELS},
  props: STUB.props, prop_info: {cables: {function: `${NS}/prop/cables`, strands: CABLES.strands.length, segments: CABLES.strands.length * 3, lamp_y: CABLES.lampY, tags: ['rlk_tk_prop', 'rlk_tk_prop_cables']}},
  calls: STUB.calls, macro_calls: STUB.macro_calls,
  tags: {part: 'rlk_tk_part', prop: 'rlk_tk_prop', per_part: 'rlk_tk_<part>', all: ['rlk_room', 'rlk_mb_aux', 'rlk_mb_part', 'rlk_tk_part']},
  objectives: OBJS, culling: CULL, view_range: VIEW_RANGE,
  budgets: {atlas_px: atlasPx, atlas_budget: ATLAS_BUDGET, sprites: Object.keys(sprites).length, elements_at_rest: ELEMENTS, elements_budget: EL_BUDGET,
    parts: PART_NAMES.length, models: Object.keys(models).length, key_files: keyFiles, keys: keyLines, rig_functions: fnFiles.files, rig_bytes: fnFiles.bytes,
    cull_overhang_ticks: cullWarn.length},
  sprites: ledger,
};
json(path.join(here, 'tachy_rig_manifest.json'), manifest);
for (const w of warns.slice(0, 20)) console.warn('warn:', w);
console.log(`Built the Tachy rig: ${PART_NAMES.length} parts, ${CLIPS.length} clips (${missing.length} stand-ins), ${keyFiles} key files, ${keyLines} keys, ${fnFiles.files} rig functions ` +
  `(${(fnFiles.bytes / 1e6).toFixed(2)} MB), ${Object.keys(models).length} models, ${Object.keys(sprites).length} sprites ${(atlasPx / 1e6).toFixed(3)} M px, elements at rest ` +
  `${FORMS.map(f => f + ' ' + ELEMENTS[f]).join(' / ')} [${((Date.now() - t0) / 1000).toFixed(1)} s]`);
if (debugDp) {
  fs.rmSync(path.join(debugDp, 'data/rlk/function/boss/tachy/rig'), {recursive: true, force: true});
  fs.cpSync(rigDir, path.join(debugDp, 'data/rlk/function/boss/tachy/rig'), {recursive: true});
  if (!fs.existsSync(path.join(debugDp, 'pack.mcmeta'))) fs.copyFileSync(path.join(dp, 'pack.mcmeta'), path.join(debugDp, 'pack.mcmeta'));
  for (const f of FORMS) putDebug(`tk_dbg/rest_${f}`, [...PART_NAMES.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(written(REST[f][n]))}}`),
    ...WINGS.map(n => swap(n, FORM_MODELS[f][n])), ...TENDRILS.map(n => `data modify entity ${uuidOf(n)} transformation.scale set value ${f === 'abyss' ? '[1.25f,1.25f,1.25f]' : '[0f,0f,0f]'}`)]);
  for (const [k, v] of Object.entries(VISOR_MODELS)) putDebug(`tk_dbg/visor_${k}`, [swap('visor_glow', v)]);
  for (const [k, v] of Object.entries(EDGE_MODELS)) putDebug(`tk_dbg/edge_${k}`, [swap('sword_edge', v)]);
  for (const [k, v] of Object.entries(CHEST_MODELS)) putDebug(`tk_dbg/chest_${k}`, [swap('chest_glow', v)]);
  putDebug('tk_dbg/player', ['summon minecraft:item_display ~1.6 ~ ~ {Tags:["tk_dbg_player"],item_display:"none",transformation:{translation:[0f,0.9f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,1.8f,0.3f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"minecraft:light_blue_concrete"}}}']);
}
void HIP_Y; void SK; void DEFAULT_POSE;
