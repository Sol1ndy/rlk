// The cutscene actor of the 홍련 (Scarlet) rebuild (lane H3; tools/dev/plan/combat/hr_design.md §3.0, §4.2, §4.3, §5.3): the
// player's stand-in in the locked cutscenes. Called by build_player_rig.mjs (cineAtlas before the atlas is written, buildCine
// at its end); it adds outputs and changes none of the player rig's own.
//
//   node tools/build_player_rig.mjs --datapack <dp> --resourcepack <unpacked RP> [--cine-allow] [--cine-debug-dp <dir>
//                                   [--cine-debug-clips a,b | all] [--cine-debug-step N]]
//
// One rig for all 7 characters: the avatar's skeleton (transform() of build_player_rig.mjs) at scale 1.0, 11 item displays
// (the rig's part list), the current character's skin and one sword (`cine_sword` = the player rig's `sword` model). The 5
// clips (cs0, cs1, repel, ending, coda) are written as channel tracks in tools/player_motion/cine/clips.mjs and solved by
// tools/player_motion/cine/lib.mjs; they play on the sequence clock: the module writes its tick into `#cavT cine` and calls
// char/cine/tick. The whole displacement of a clip (the manifest's `shift`) is inside the display transforms: the entities
// stay at the stage origin, so the root only carries the stage's place and yaw.
//
// Writes (owned, rebuilt from scratch on every run)
//   DP  data/rlk/function/char/cine/**            spawn, play {clip}, tick, face {yaw}, stop + the compiled clips
//   RP  assets/rlk/textures/skin/lumine.png      copied from tools/player_motion/cine/skin/lumine.png (her profile texture)
//       assets/rlk/{models/item,items}/player_motion/{lumine,clorinde,ronova,nefer}/<part>.json   (bodyModels(), as the rig
//       characters' parts)   assets/rlk/items/player_motion/weapons/cine_sword.json   (the `sword` model: 0 new atlas px)
//       items-atlas entries rlk:skin/{lumine,clorinde,ronova,nefer} (added once, before the rig's block aliases)
//   tools/player_motion/cine/<clip>.json          the solved clips in the player_motion format (generated: edit clips.mjs)
//   tools/player_motion/cine/manifest.json        per clip the length and, per tick, the root shift, the blade's hilt and
//                                                 tip and both hands in the stage frame (+ calls, tags, contacts, checks)
//
// Runtime (fake players on the objective `cine`, which spawn / play add and stop removes):
//   #cavT  the clip tick to show (the module's `#sq hr`)      #cavC  the clip (1 cs0, 2 cs1, 3 repel, 4 ending, 5 coda)
//   #cavP  the tick shown last                                #cavR  the sync tick whose running segments wait to be re-armed
//   #cavF, #cavFy  the face turn: ticks left, the target yaw x 100;   #cavCh  the character the parts were made for
// A part gets a key only when its transform changes: at tick a the pose of tick b with interpolation_duration b - a (the
// client's lerp / slerp reproduces the ticks between within tolerance). A hold sends nothing: in 26.3 any NBT write to a
// display restarts its interpolation clock, and with an unchanged transform the client replays the last interpolation
// (Display.readAdditionalSaveData always sets start_interpolation; verified in the 26.3 server jar). A jump of #cavT (a
// skip, a new clip, the first tick) snaps every part to the pose of the last sync tick at or before it (every 20 ticks, the
// skip targets and each clip's end are sync ticks) and re-arms the running segments on the next tick; a short forward jump
// replays the keys between.
import fs from 'node:fs';
import path from 'node:path';
import {Tracks, solve, frames, points, lowest, bladeInBody, SWORD, HIP_Y} from './player_motion/cine/lib.mjs';
import {CLIPS, IDLE_CHANNELS, CONTACT, LIMIT, MUTUAL, herTrack} from './player_motion/cine/clips.mjs';
import {len, sub, slerp, lerp} from './mboss_rig_math.mjs';
// the angle between two rotations in degrees (the written quaternions are rounded: normalised here)
const qAngle = (a, b) => { const d = Math.abs(a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3]) / (Math.hypot(...a) * Math.hypot(...b)); return 2 * Math.acos(Math.min(1, d)) * 180 / Math.PI; };

export const CINE_CHARS = [                      // #charN -> the part models' folder and the skin
  {n: 1, id: 'lumine', key: 'lumine', skin: 'lumine', rig: false},
  {n: 3, id: 'skirk', key: 'skirk', skin: 'skirk', rig: true},
  {n: 4, id: 'clorinde', key: 'clorinde', skin: 'clorinde', rig: false},
  {n: 5, id: 'arlecchino', key: 'arle', skin: 'arlecchino', rig: true},
  {n: 6, id: 'navia', key: 'navia', skin: 'navia', rig: true},
  {n: 7, id: 'ronova', key: 'ronova', skin: 'ronova', rig: false},
  {n: 8, id: 'nefer', key: 'nefer', skin: 'nefer', rig: false},
];
const NEW_SKINS = CINE_CHARS.filter(c => !c.rig).map(c => 'rlk:skin/' + c.skin);
// The 4 skins the item atlas does not have yet. Called before the rig's block aliases are re-appended, so the entry order
// is the same on every run.
export function cineAtlas(atlas) {
  for (const resource of NEW_SKINS) if (!atlas.sources.some(s => s.type === 'minecraft:single' && s.resource === resource && !s.sprite)) atlas.sources.push({type: 'minecraft:single', resource});
}

const PARTS = ['head', 'body', 'right_arm', 'right_forearm', 'left_arm', 'left_forearm', 'right_leg', 'right_shin', 'left_leg', 'left_shin', 'weapon'];
const NS = 'rlk:char/cine', OBJ = 'cine';
const TAG = {root: 'rlk_cine_root', part: 'rlk_cine_part', hidden: 'rlk_cine_hid'};
const BLANK_SKIN = 'rlk:skin/blank';      // a fully transparent skin (tools/build_blank_tex.py): the hidden avatar's ghost draws nothing
const UUID = i => `524c4b4d-4349-4e45-8000-0000000000${i.toString(16).padStart(2, '0')}`;
const UUID_INTS = i => `[I;1380731725,1128877637,-2147483648,${i}]`;
const GRID = 20;                                 // a sync tick every GRID ticks
const TOL = {t: .008, s: .015, r: {weapon: .4}, rDefault: 1};
const MAX_STEP = 120;
const FIELDS = ['shift', 'root', 'torso', 'head', 'right_arm', 'right_elbow', 'left_arm', 'left_elbow', 'right_leg', 'right_knee', 'left_leg', 'left_knee', 'weapon'];
const r5 = x => (Math.abs(x) < 5e-7 ? 0 : +x.toFixed(5));
const r3 = x => (Math.abs(x) < 5e-5 ? 0 : +x.toFixed(3));
const f5 = x => (Math.abs(x) < 5e-7 ? 0 : x).toFixed(5).replace(/\.?0+$/, '') + 'f';
const arr = a => '[' + a.map(f5).join(',') + ']';
const nbt = v => `{translation:${arr(v.t)},left_rotation:${arr(v.q)},scale:${arr(v.s)},right_rotation:[0f,0f,0f,1f]}`;
const written = v => ({t: v.t.map(r5), q: v.q.map(r5), s: v.s.map(r5)});
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const dist = (a, b) => len(sub(a, b));
// distance of a point to the segment a-b
function segDist(P, a, b) {
  const ab = sub(b, a), u = Math.max(0, Math.min(1, ab.reduce((s, x, i) => s + x * (P[i] - a[i]), 0) / ab.reduce((s, x) => s + x * x, 0)));
  return dist(P, a.map((x, i) => x + ab[i] * u));
}

export function buildCine({dpRoot, rpRoot, here, transform, bodyModels, argv = process.argv}) {
  const arg = n => { const i = argv.indexOf(n); return i < 0 ? null : argv[i + 1]; };
  const allow = argv.includes('--cine-allow');
  const debugDp = arg('--cine-debug-dp') && path.resolve(arg('--cine-debug-dp'));
  const debugClips = (arg('--cine-debug-clips') || 'all').split(','), debugStep = +(arg('--cine-debug-step') || 1);
  const put = (p, s) => { fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, s.endsWith('\n') ? s : s + '\n', 'utf8'); };
  const fnDir = path.join(dpRoot, 'data/rlk/function/char/cine');
  fs.rmSync(fnDir, {recursive: true, force: true});
  const fn = (n, lines) => put(path.join(fnDir, n + '.mcfunction'), (Array.isArray(lines) ? lines : [lines]).join('\n'));
  const cineDir = path.join(here, 'player_motion/cine');
  const errors = [], warns = [];
  const fail = (what, list) => { if (list.length) (allow ? warns : errors).push(`${what} (${list.length}): ${list.slice(0, 8).join('; ')}${list.length > 8 ? '; ...' : ''}`); };

  // ---- resource pack: Lumine's skin, the part models of the 4 characters without a rig, the one sword -----------------------
  const assets = path.join(rpRoot, 'assets/rlk');
  fs.mkdirSync(path.join(assets, 'textures/skin'), {recursive: true});
  fs.copyFileSync(path.join(cineDir, 'skin/lumine.png'), path.join(assets, 'textures/skin/lumine.png'));
  for (const c of CINE_CHARS) if (!c.rig) bodyModels(c.key, c.skin);
  put(path.join(assets, 'items/player_motion/weapons/cine_sword.json'), JSON.stringify({model: {type: 'minecraft:model', model: 'rlk:item/player_motion/weapons/sword'}}, null, 2));

  // ---- the display transform of a pose (the player rig's transform(): hand attach, the sword at scale 1) -------------------
  const display = pose => {
    const d = transform({...pose, weapon_attach: 'hand', weapon_scale: [1, 1, 1]});
    return Object.fromEntries(PARTS.map(n => [n, {t: d[n].t, q: d[n].q, s: d[n].s || [1, 1, 1]}]));
  };
  // the skeleton has one definition: lib.frames() (the checks, the manifest) == transform() before its display mirror
  {
    const probe = solve({...IDLE_CHANNELS, rot: [12, 35, -8], tor: [-20, 15, 6], head: [10, -30, 5], aR: [70, 10, -40, 60], aL: [-30, 5, 50, 20], lfR: 1, lR: [50, 5, -10, 70], hip: [.1, -.2, .05]}, 7).pose;
    const f = frames(probe), d = display(probe);
    for (const n of PARTS) {
      const t = [f[n].t[0], f[n].t[1], -f[n].t[2]], qd = [-f[n].q[0], -f[n].q[1], f[n].q[2], f[n].q[3]];
      if (dist(t, d[n].t) > 1e-9 || qAngle(qd, d[n].q) > 1e-4) throw new Error(`cine: lib.frames() differs from transform() at ${n}`);
    }
  }
  const idlePose = solve(IDLE_CHANNELS, 0).pose;
  const roundPose = p => Object.fromEntries(FIELDS.map(k => [k, p[k].map(k === 'shift' ? r5 : r3)]));
  const IDLE_D = display(roundPose(idlePose));

  // ---- clips -----------------------------------------------------------------------------------------------------------------
  const manifest = {
    schema: 1, id: 'cine', _doc: 'The cutscene actor (tools/build_player_cine.mjs; hr_design.md §4.2, §4.3, §5.3). Generated: do not edit. Points are in the stage frame ST(r, u, f): r to the actor\'s right, u up, f forward, the origin at the avatar\'s feet. Per tick: shift = the root\'s displacement, hilt = the grip point in the right hand, tip = the blade\'s point, hand_r / hand_l = the grip points of the hands (also pommel, foot_r, foot_l, head, shoulder_r; round W: chest, waist = the torso\'s axis for the gap check of test_contact.py).',
    source: 'tools/player_motion/cine/clips.mjs', parts: PARTS, uuid: UUID(0).slice(0, -2) + '{:02x}',
    tags: {root: TAG.root, part: TAG.part, per_part: 'rlk_cine_<part>', hidden: TAG.hidden, all: ['rlk_room', 'rlk_mb_aux']},
    objective: OBJ, fake_players: {tick: '#cavT', clip: '#cavC', shown: '#cavP', rearm: '#cavR', face: '#cavF', face_yaw: '#cavFy', char: '#cavCh'},
    storage: 'rlk:cine',
    calls: {spawn: `${NS}/spawn`, play: `${NS}/play {clip:"<id>"}`, tick: `${NS}/tick`, face: `${NS}/face {yaw:<deg>}`, stop: `${NS}/stop`},
    characters: CINE_CHARS.map(c => ({n: c.n, id: c.id, models: `rlk:player_motion/${c.key}/<part>`, skin: 'rlk:skin/' + c.skin, rig: c.rig})),
    sword: {model: 'rlk:player_motion/weapons/cine_sword', of: 'rlk:item/player_motion/weapons/sword', scale: 1, hilt_to_tip: +SWORD.tip.toFixed(4), hilt_to_pommel: +(-SWORD.pommel).toFixed(4), blade_root: SWORD.root, left_hand: SWORD.left},
    hip_y: HIP_Y, height: 2, sync_grid: GRID, limit: LIMIT, contact: CONTACT, mutual: MUTUAL, clips: {}, checks: {},
  };
  const dbgPut = (n, lines) => put(path.join(debugDp, 'data/rlk/function', n + '.mcfunction'), lines.join('\n'));
  if (debugDp) fs.rmSync(path.join(debugDp, 'data/rlk/function/cine_dbg'), {recursive: true, force: true});
  const ends = {}, hists = {};
  CLIPS.forEach((clip, ci) => {
    const id = ci + 1, L = clip.len, name = clip.id;
    // 1. solve the tracks, tick by tick (the limbs keep their bend side from the tick before)
    const tr = new Tracks(L, clip.start || IDLE_CHANNELS);
    clip.build(tr);
    fail(`${name}: a channel drifts over a long gap (hold it first)`, tr.slow().filter(x => !(clip.slow || []).includes(x)));
    const solved = [], shortAll = [];
    // a clip that takes over from another without a respawn starts from that clip's solve (the limbs' bend sides carry on)
    let hist = clip.after ? hists[clip.after[0]][clip.after[1]] : null;
    hists[name] = {};
    for (let t = 0; t <= L; t++) {
      const s = solve(tr.sample(t), t, hist);
      hist = s.hist; solved.push(roundPose(s.pose));
      if ((clip.keep || []).includes(t)) hists[name][t] = hist;
      for (const [k, v] of Object.entries(s.info.short)) if (v > .03) shortAll.push(`t${t} ${k} ${v.toFixed(3)}`);
    }
    // 2. the clip file: keys whose linear interpolation gives every tick back (eulers 0.02 degrees, the shift 0.0004 b)
    const keys = [0];
    {
      const fits = (a, b) => {
        for (let t = a + 1; t < b; t++) {
          const u = (t - a) / (b - a);
          for (const k of FIELDS) { const tol = k === 'shift' ? 4e-4 : .02; for (let i = 0; i < 3; i++) if (Math.abs(solved[a][k][i] + (solved[b][k][i] - solved[a][k][i]) * u - solved[t][k][i]) > tol) return false; }
        }
        return true;
      };
      let a = 0;
      while (a < L) { let b = a + 1; while (b + 1 <= L && fits(a, b + 1)) b++; keys.push(b); a = b; }
    }
    const frameLines = keys.map((t, i) => {
      const prev = i ? solved[keys[i - 1]] : null;
      const pose = Object.fromEntries(FIELDS.filter(k => !prev || !same(prev[k], solved[t][k])).map(k => [k, solved[t][k]]));
      return JSON.stringify({tick: t, pose: i ? pose : {...pose, weapon_shift: [0, 0, 0], weapon_scale: [1, 1, 1]}});
    });
    put(path.join(cineDir, name + '.json'), `{"_doc": ${JSON.stringify(`Actor clip ${name} (${L} t): generated by tools/build_player_cine.mjs from tools/player_motion/cine/clips.mjs; the player_motion clip format (sticky pose fields, linear between frames). Do not edit.`)},\n "id": ${JSON.stringify(name)}, "length": ${L}, "weapon": "cine_sword", "grip": ${JSON.stringify(clip.grip)}, "beats": ${JSON.stringify(clip.beats)},\n "frames": [\n  ${frameLines.join(',\n  ')}\n ]}`);
    // what ships is the clip file sampled per tick
    const pose = [];
    for (let i = 0; i + 1 < keys.length; i++) {
      const a = keys[i], b = keys[i + 1];
      for (let t = a; t <= b; t++) { const u = (t - a) / (b - a); pose[t] = Object.fromEntries(FIELDS.map(k => [k, solved[a][k].map((x, j) => x + (solved[b][k][j] - x) * u)])); pose[t].weapon_shift = [0, 0, 0]; }
    }
    const disp = pose.map(p => { const d = display(p); for (const n of PARTS) d[n] = written(d[n]); return d; });
    const pts = pose.map(points);
    const rootAt = Array.from({length: L + 1}, (_, t) => tr.val('root', t).map(r3));
    // 3. checks
    const floor = [], steps = [], lim = [], blade = [], slide = [];
    for (let t = 0; t <= L; t++) {
      const low = lowest(pose[t]);
      if (low.body < -.006) floor.push(`t${t} ${low.part} ${low.body.toFixed(3)}`);
      if (low.sword < -.006) floor.push(`t${t} sword ${low.sword.toFixed(3)}`);
      const [r, u, f] = rootAt[t], cs0 = name === 'cs0';
      if (f > LIMIT.fwd + 1e-6 || f < -(cs0 ? LIMIT.cs0_back : LIMIT.back) - 1e-6 || Math.abs(r) > LIMIT.side + 1e-6 || u < -1e-6 || u > (name === 'ending' ? LIMIT.air : 0) + 1e-6) lim.push(`t${t} [${rootAt[t]}]`);
      if (t) for (const n of PARTS) { const ang = qAngle(disp[t - 1][n].q, disp[t][n].q); if (ang > MAX_STEP) steps.push(`t${t - 1}->${t} ${n} ${ang.toFixed(0)}`); }
      const bi = bladeInBody(pose[t]);
      if (bi > .03) blade.push(`t${t} ${bi.toFixed(2)}`);
      // a sole on the floor at both ticks does not travel, outside the clip's declared slides
      if (t && !(clip.slides || []).some(([a, b]) => t > a && t <= b)) for (const s of ['foot_r', 'foot_l']) {
        const p0 = pts[t - 1][s], p1 = pts[t][s];
        if (p0[1] < .012 && p1[1] < .012 && Math.hypot(p1[0] - p0[0], p1[2] - p0[2]) > .012) slide.push(`t${t} ${s} ${Math.hypot(p1[0] - p0[0], p1[2] - p0[2]).toFixed(3)}`);
      }
    }
    fail(`${name}: under the floor`, floor); fail(`${name}: more than ${MAX_STEP} degrees in a tick`, steps); fail(`${name}: shift outside the limits`, lim);
    fail(`${name}: a planted sole slides`, slide); fail(`${name}: IK target out of reach`, shortAll);
    if (blade.length) warns.push(`${name}: the blade inside the head / torso (${blade.length}): ${blade.slice(0, 10).join('; ')}`);
    for (const t of clip.handback) {
      if (!same(rootAt[t], [0, 0, 0])) fail(`${name}: shift at the hand-back tick ${t}`, [`[${rootAt[t]}]`]);
      // (the sword may be rolled half round its blade: the same picture)
      const roll = Q => [-Q[2], Q[3], Q[0], -Q[1]];           // Q * (a half turn about the blade, model Y)
      const off = PARTS.filter(n => dist(disp[t][n].t, IDLE_D[n].t) > 2e-4 || (qAngle(disp[t][n].q, IDLE_D[n].q) > .02 && !(n === 'weapon' && qAngle(roll(disp[t][n].q), IDLE_D[n].q) < .02)));
      if (off.length) fail(`${name}: tick ${t} is not the avatar's idle`, off);
    }
    for (const [a, b] of clip.grounded || []) for (let t = a; t <= b; t++) if (!same(rootAt[t], [0, 0, 0])) { fail(`${name}: shift in ${a}-${b}`, [`t${t} [${rootAt[t]}]`]); break; }
    const two = [];
    for (const [a, b] of clip.two || []) for (let t = a; t <= b; t++) {
      const want = pts[t].hilt.map((x, i) => x + (pts[t].tip[i] - x) * (SWORD.left / SWORD.tip)), d = dist(pts[t].hand_l, want);
      if (d > .06) two.push(`t${t} ${d.toFixed(3)}`);
    }
    fail(`${name}: the left hand off the hilt on two-hand ticks`, two);
    const contact = {};
    for (const [k, c] of Object.entries(CONTACT)) if (c.clip === name) {
      if (c.ticks[c.ticks.length - 1] > L) { fail(`${name}: contact ${k}`, [`its ticks run past the clip`]); continue; }
      let worst = 0, at = 0;
      for (let t = c.ticks[0]; t <= c.ticks[c.ticks.length - 1]; t++) {
        if (c.ticks.length === 2 && c.only && t !== c.ticks[0] && t !== c.ticks[1]) continue;
        const P = pts[t], bladeRoot = P.hilt.map((x, i) => x + (P.tip[i] - x) * (SWORD.root / SWORD.tip));
        const d = c.what === 'blade' ? segDist(c.p, bladeRoot, P.tip) : c.what === 'tip' ? dist(c.p, P.tip) : c.what === 'hilt' ? segDist(c.p, P.pommel, P.guard)
          : c.what === 'under' ? Math.max(0, dist([P[c.point][0], P[c.point][2]], [c.p[0], c.p[2]]) - c.r, P[c.point][1] - c.p[1] + c.below[0], c.p[1] - c.below[1] - P[c.point][1]) : dist(c.p, P[c.what]);
        if (d > worst) { worst = d; at = t; }
      }
      contact[k] = {worst: r3(worst), at, tol: c.tol};
      if (worst > c.tol) fail(`${name}: contact ${k}`, [`${worst.toFixed(3)} > ${c.tol} at t${at}`]);
    }
    ends[name] = {first: solved[0], last: solved[L], rootFirst: rootAt[0], rootLast: rootAt[L]};
    // 4. compile: per part, interpolation segments; a segment whose target is the part's current transform sends nothing
    const close = (x, y, n) => dist(x.t, y.t) <= TOL.t && Math.max(...x.s.map((v, i) => Math.abs(v - y.s[i]))) <= TOL.s && qAngle(x.q, y.q) <= (TOL.r[n] ?? TOL.rDefault);
    const interp = (a, b, u) => ({t: lerp(a.t, b.t, u), q: slerp(a.q, b.q, u), s: lerp(a.s, b.s, u)});
    const segs = {}, byTick = new Map();
    let keyCount = 0;
    for (const n of PARTS) {
      const seq = disp.map(d => d[n]), out = [];
      let a = 0;
      while (a < L) {
        let b = a + 1;
        const fits = bb => { if (qAngle(seq[a].q, seq[bb].q) > MAX_STEP - 2) return false; for (let t = a + 1; t < bb; t++) if (!close(interp(seq[a], seq[bb], (t - a) / (bb - a)), seq[t], n)) return false; return true; };
        while (b + 1 <= L && fits(b + 1)) b++;
        out.push([a, b]); a = b;
      }
      segs[n] = out;
      for (const [a2, b2] of out) {
        if (a2 === 0 || same(seq[a2], seq[b2])) continue;       // tick 0 is reached by a seek only (s/0 + r/0); a hold sends nothing
        if (!byTick.has(a2)) byTick.set(a2, []);
        byTick.get(a2).push(`data merge entity ${UUID(PARTS.indexOf(n))} {start_interpolation:0,interpolation_duration:${b2 - a2},transformation:${nbt(seq[b2])}}`);
        keyCount++;
      }
    }
    const base = `c/${name}`, keyTicks = [...byTick.keys()].sort((x, y) => x - y);
    for (const t of keyTicks) fn(`${base}/k/${t}`, byTick.get(t));
    const sync = [...new Set([...Array.from({length: Math.floor(L / GRID) + 1}, (_, i) => i * GRID), L, ...(clip.sync || [])])].sort((x, y) => x - y);
    for (const S of sync) {
      fn(`${base}/s/${S}`, [`# ${name}: the pose of tick ${S}, no interpolation (a jump of #cavT lands here); the next tick re-arms the running segments.`,
        ...PARTS.map((n, i) => `data merge entity ${UUID(i)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(disp[S][n])}}`),
        `scoreboard players set #cavP ${OBJ} ${S}`, `scoreboard players set #cavR ${OBJ} ${S}`]);
      const lines = [];
      for (const n of PARTS) { const sg = segs[n].find(([a, b]) => a <= S && S < b); if (sg && !same(disp[S][n], disp[sg[1]][n])) lines.push(`data merge entity ${UUID(PARTS.indexOf(n))} {start_interpolation:0,interpolation_duration:${Math.max(0, sg[1] - S - 1)},transformation:${nbt(disp[sg[1]][n])}}`); }
      fn(`${base}/r/${S}`, [`# ${name}: the segments running across tick ${S}, sent one tick after the snap.`, ...lines]);
    }
    // binary dispatch (at most 6 leaves per file), as the boss rigs' key trees
    const tree = (dir, score, items, leaf) => {
      if (items.length <= 6) return items.map(leaf);
      const mid = items[Math.floor(items.length / 2) - 1], lo = items.filter(x => x[0] <= mid[0]), hi = items.filter(x => x[0] > mid[0]);
      const sub2 = part => `${dir}/${part[0][0]}_${part[part.length - 1][0]}`;
      fn(sub2(lo), tree(dir, score, lo, leaf)); fn(sub2(hi), tree(dir, score, hi, leaf));
      return [`execute if score ${score} ${OBJ} matches ..${mid[0]} run return run function ${NS}/${sub2(lo)}`, `function ${NS}/${sub2(hi)}`];
    };
    fn(`${base}/keys`, [`# ${name}: the keys of tick #cavP.`, ...tree(`${base}/b`, '#cavP', keyTicks.map(t => [t]), ([t]) => `execute if score #cavP ${OBJ} matches ${t} run return run function ${NS}/${base}/k/${t}`)]);
    fn(`${base}/seek`, [`# ${name}: a jump. Snap to the last sync tick at or before #t.`,
      ...tree(`${base}/sb`, '#t', sync.map((S, i) => [S, (sync[i + 1] ?? L + 1) - 1]), ([S, hi]) => `execute if score #t ${OBJ} matches ${S === hi ? S : `${S}..${hi}`} run return run function ${NS}/${base}/s/${S}`)]);
    fn(`${base}/rearm`, [`# ${name}: the tick after a snap to sync tick #cavR.`,
      ...tree(`${base}/rb`, '#cavR', sync.map(S => [S]), ([S]) => `execute if score #cavR ${OBJ} matches ${S} run return run function ${NS}/${base}/r/${S}`)]);
    fn(`${base}/catch`, [`# ${name}: advance the shown tick to #t, key by key.`, `scoreboard players add #cavP ${OBJ} 1`, `function ${NS}/${base}/keys`,
      `execute if score #cavP ${OBJ} < #t ${OBJ} run function ${NS}/${base}/catch`]);
    fn(`${base}/run`, [`# ${name} (${L} t; clip ${id}): show tick #cavT, held at 0 and at ${L}. From char/cine/tick.`,
      `scoreboard players operation #t ${OBJ} = #cavT ${OBJ}`,
      `execute unless score #t ${OBJ} matches 0.. run scoreboard players set #t ${OBJ} 0`,
      `execute if score #t ${OBJ} matches ${L + 1}.. run scoreboard players set #t ${OBJ} ${L}`,
      `execute if score #cavR ${OBJ} matches 0.. run function ${NS}/${base}/rearm`,
      `scoreboard players set #cavR ${OBJ} -1`,
      `scoreboard players operation #d ${OBJ} = #t ${OBJ}`, `scoreboard players operation #d ${OBJ} -= #cavP ${OBJ}`,
      `execute if score #d ${OBJ} matches 0 run return 0`,
      `execute if score #d ${OBJ} matches 1..${GRID} run return run function ${NS}/${base}/catch`,
      `function ${NS}/${base}/seek`]);
    fn(`${base}/sel`, [`# play {clip:"${name}"}: the next char/cine/tick snaps to tick #cavT of ${name}.`, `scoreboard players set #cavC ${OBJ} ${id}`, `scoreboard players set #cavP ${OBJ} -99`, `scoreboard players set #cavR ${OBJ} -1`]);
    if (debugDp && (debugClips.includes('all') || debugClips.includes(name))) for (let t = 0; t <= L; t += debugStep)
      dbgPut(`cine_dbg/${name}/${t}`, PARTS.map((n, i) => `data merge entity ${UUID(i)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(disp[t][n])}}`));
    // (HF-B, HB-01) the mutual rows: her points (lane H2c's her_tracks.json) against this clip's, so that a grab / hold / throw
    // meets on both bodies, not each side on its own stage point (the throw passed its one-sided rows with 2 b between them)
    const mutual = {};
    for (const m of MUTUAL.filter(x => x.clip === name)) {
      const her = herTrack(name);
      if (!her?.staged) { fail(`${name}: mutual ${m.id}`, ['her_tracks.json has no staged track of this clip']); continue; }
      let worst = 0, at = m.t0;
      if (m.over) {
        let top = m.t0;
        for (let t = m.t0; t <= m.t1; t++) if (her.pelvis[t][1] > her.pelvis[top][1]) top = t;
        const P = her.pelvis[top], Sh = pts[top].shoulder_r, du = P[1] - Sh[1], dxz = Math.hypot(P[0] - Sh[0], P[2] - Sh[2]);
        worst = Math.max(0, du - m.up, -du, dxz - m.r); at = top;
        mutual[m.id] = {top, over: r3(du), off: r3(dxz), up: m.up, r: m.r};
        if (worst > 0) fail(`${name}: mutual ${m.id}`, [`her pelvis ${du.toFixed(3)} b over the actor's right shoulder (0..${m.up}), ${dxz.toFixed(3)} b off it (<= ${m.r}) at t${top}`]);
        continue;
      }
      for (let t = m.t0; t <= m.t1; t++) {
        const A_ = [m.actor].flat().map(k => pts[t][k]);
        const d = Math.min(...A_.map(a => Array.isArray(m.her) ? segDist(a, her[m.her[0]][t], her[m.her[1]][t]) : dist(a, her[m.her][t])));
        if (d > worst) { worst = d; at = t; }
      }
      mutual[m.id] = {worst: r3(worst), at, tol: m.tol};
      if (worst > m.tol) fail(`${name}: mutual ${m.id}`, [`${worst.toFixed(3)} > ${m.tol} at t${at}`]);
    }
    const col = k => pts.map(P => P[k].map(r3));
    manifest.clips[name] = {id, len: L, grip: clip.grip, beats: clip.beats, steps: clip.steps || [], handback: clip.handback, slides: clip.slides || [], two_hands: clip.two || [], her: clip.her || [],
      sync, keys: keyCount, key_files: keyTicks.length, json_frames: keys.length, contact, mutual,
      tick: {shift: rootAt, hilt: col('hilt'), tip: col('tip'), hand_r: col('hand_r'), hand_l: col('hand_l'), pommel: col('pommel'), foot_r: col('foot_r'), foot_l: col('foot_l'), head: col('head'), shoulder_r: col('shoulder_r'), chest: col('chest'), waist: col('waist')}};
  });
  // the clips that follow each other without a respawn meet in one pose
  for (const [a, ta, b] of [['repel', 129, 'ending'], ['ending', 1372, 'coda']]) {
    const ma = manifest.clips[a], mb = manifest.clips[b];
    if (ta > ma.len) continue;
    const d = Math.max(...['shift', 'hilt', 'tip', 'hand_r', 'hand_l', 'foot_r', 'foot_l', 'head'].map(k => dist(ma.tick[k][ta], mb.tick[k][0])));
    manifest.checks[`${a}_${ta}_to_${b}_0`] = r3(d);
    if (d > .02) fail(`${a} ${ta} -> ${b} 0: the poses differ`, [d.toFixed(3)]);
  }

  // ---- runtime ----------------------------------------------------------------------------------------------------------------
  const rest = display(idlePose);
  const AV = '@e[tag=rlk_av,limit=1]', ROOT = `@e[type=minecraft:marker,tag=${TAG.root},limit=1]`, PARTSEL = `@e[type=minecraft:item_display,tag=${TAG.part}]`;
  const partTags = n => JSON.stringify(['rlk_room', 'rlk_mb_aux', TAG.part, 'rlk_cine_' + n]);
  const summon = (n, i, item) => `summon minecraft:item_display ~ ~ ~ {UUID:${UUID_INTS(i)},Tags:${partTags(n)},billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:2f,shadow_radius:0f,brightness:{block:13,sky:15},transformation:${nbt(written(rest[n]))},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${item}"}}}`;
  fn('spawn', ['# The cutscene actor. @s = the player, at the stage marker, rotated as the stage (hr_design.md §5.3). The root and the 11',
    '# displays in the avatar\'s idle pose with the current character\'s skin and the one sword; the avatar (and a rig character\'s own',
    '# displays, a floating catalyst) hidden. Called again it only moves the actor to the new stage.',
    `scoreboard objectives add ${OBJ} dummy`,
    `execute ${PARTS.map((n, i) => `if entity ${UUID(i)}`).join(' ')} if entity ${ROOT} if score #cavCh ${OBJ} = #charN tmp run return run function ${NS}/place`,
    `function ${NS}/clear`,
    `summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","${TAG.root}"]}`,
    `data modify storage rlk:cine sp set value {k:"${CINE_CHARS[0].key}"}`,
    ...CINE_CHARS.slice(1).map(c => `execute if score #charN tmp matches ${c.n} run data modify storage rlk:cine sp.k set value "${c.key}"`),
    `function ${NS}/parts with storage rlk:cine sp`,
    `scoreboard players operation #cavCh ${OBJ} = #charN tmp`,
    `scoreboard players set #cavP ${OBJ} -99`, `scoreboard players set #cavR ${OBJ} -1`, `scoreboard players set #cavF ${OBJ} 0`,
    `function ${NS}/place`]);
  fn('parts', ['# Internal (macro k = the character\'s part folder): the 11 displays at the execution position.',
    ...PARTS.map((n, i) => (n === 'weapon' ? summon(n, i, 'rlk:player_motion/weapons/cine_sword') : '$' + summon(n, i, `rlk:player_motion/$(k)/${n}`)))]);
  fn('place', ['# Internal: the root and the parts to the execution position and yaw; the avatar hidden.',
    `execute rotated ~ 0 run tp ${ROOT} ~ ~ ~ ~ 0`, `execute rotated ~ 0 run tp ${PARTSEL} ~ ~ ~ ~ 0`, `function ${NS}/hide`]);
  fn('clear', ['# Internal: the actor\'s entities.', `kill ${PARTSEL}`, `kill @e[type=minecraft:marker,tag=${TAG.root}]`]);
  fn('hide', ['# Internal, every tick while the actor stands: the avatar invisible with empty hands (1 s at a time: it shows again by',
    '# itself if the ticks stop), a rig character\'s displays, a stand-in rig and a floating catalyst out of view range until stop.',
    '# Round V (lane VC): the player watches a locked sequence as a spectator, and a spectator sees an invisible living',
    '# entity as a 15 % ghost drawn with its own texture: the avatar\'s skin is the blank one until stop (blank / show).',
    `execute as @e[tag=rlk_av,tag=!${TAG.hidden},limit=1] run function ${NS}/blank`,
    `effect give ${AV} minecraft:invisibility 1 0 true`,
    `item replace entity ${AV} weapon.mainhand with minecraft:air`, `item replace entity ${AV} weapon.offhand with minecraft:air`,
    `tag ${AV} add ${TAG.hidden}`,
    `execute as @e[type=minecraft:item_display,tag=rlk_pm,tag=!${TAG.hidden}] run function ${NS}/hide_one`,
    // round V integration: lane VP's stand-in rig of a mannequin character (char/motion/lite, tag rlk_pl) plays for the rest
    // of the tick a sequence starts in when a perfect parry / dodge beat was running (player/def/beat/post, after this): out
    // of view at once; the beat's own end (one tick later: player/def/beat/clock sees the lock) removes it
    `execute as @e[type=minecraft:item_display,tag=rlk_pl,tag=!${TAG.hidden}] run function ${NS}/hide_one`,
    `execute as @e[type=minecraft:block_display,tag=rlk_rncat,tag=!${TAG.hidden}] run function ${NS}/hide_one`,
    `execute as @e[type=minecraft:block_display,tag=rlk_nfcat,tag=!${TAG.hidden}] run function ${NS}/hide_one`]);
  fn('hide_one', [`data merge entity @s {view_range:0f}`, `tag @s add ${TAG.hidden}`]);
  fn('blank', ['# Internal (@s = the avatar, once per hide): its profile kept in storage rlk:cine av ({} when it has none: the default skin),',
    `# the skin texture replaced by the fully transparent ${BLANK_SKIN} (tools/build_blank_tex.py writes it into the pack): the`,
    '# ghost a spectator would see of the invisible avatar has nothing to draw.',
    'data modify storage rlk:cine av set value {}',
    'data modify storage rlk:cine av set from entity @s profile',
    `data modify entity @s profile.texture set value "${BLANK_SKIN}"`]);
  fn('play', ['# function rlk:char/cine/play {clip:"cs0"|"cs1"|"repel"|"ending"|"coda"}: selects the clip; #cavT is the module\'s.',
    `scoreboard objectives add ${OBJ} dummy`, `$function ${NS}/c/$(clip)/sel`]);
  fn('tick', ['# @s = the player, once per tick of a locked sequence, after the module wrote the clip tick into #cavT cine: shows that',
    '# tick of the selected clip (past the length: the last frame). Without an actor it restores the avatar (stop).',
    `execute unless entity ${ROOT} run return run function ${NS}/stop`,
    `function ${NS}/hide`,
    `execute if score #cavF ${OBJ} matches 1.. run function ${NS}/face_step`,
    ...CLIPS.map((c, i) => `execute if score #cavC ${OBJ} matches ${i + 1} run return run function ${NS}/c/${c.id}/run`)]);
  fn('face', ['# function rlk:char/cine/face {yaw:<degrees>}: turns the root to that absolute yaw over 12 ticks (the ending\'s ST -> ST2).',
    '# The clip\'s own root yaw is inside the pose and adds to it.',
    `scoreboard objectives add ${OBJ} dummy`,
    '$data modify storage rlk:cine face set value {yaw:$(yaw)}',
    `execute store result score #cavFy ${OBJ} run data get storage rlk:cine face.yaw 100`,
    `scoreboard players set #cavF ${OBJ} 12`]);
  fn('face_step', ['# Internal: one step of the face turn (the short way round), the parts take the root\'s yaw.',
    `execute store result score #y ${OBJ} run data get entity ${ROOT} Rotation[0] 100`,
    `scoreboard players operation #dy ${OBJ} = #cavFy ${OBJ}`, `scoreboard players operation #dy ${OBJ} -= #y ${OBJ}`,
    `scoreboard players set #c36000 ${OBJ} 36000`, `scoreboard players add #dy ${OBJ} 18000`, `scoreboard players operation #dy ${OBJ} %= #c36000 ${OBJ}`, `scoreboard players remove #dy ${OBJ} 18000`,
    `scoreboard players operation #dy ${OBJ} /= #cavF ${OBJ}`, `scoreboard players operation #y ${OBJ} += #dy ${OBJ}`,
    `execute as ${ROOT} store result entity @s Rotation[0] float 0.01 run scoreboard players get #y ${OBJ}`,
    `scoreboard players remove #cavF ${OBJ} 1`,
    `execute as ${ROOT} at @s run tp ${PARTSEL} ~ ~ ~ ~ 0`]);
  fn('stop', ['# Any executor, no position: the actor gone, the avatar visible again (a rig character\'s displays, the catalyst too). Does',
    '# nothing when there is no actor; the framework\'s camera release and every exit path of a sequence call it.',
    `function ${NS}/clear`,
    `execute as @e[type=minecraft:item_display,tag=rlk_pm,tag=${TAG.hidden}] run data merge entity @s {view_range:1.5f}`,
    `execute as @e[type=minecraft:block_display,tag=${TAG.hidden}] run data merge entity @s {view_range:1f}`,
    `tag @e[type=!minecraft:mannequin,tag=${TAG.hidden}] remove ${TAG.hidden}`,
    `execute as @a[tag=player,limit=1] run function ${NS}/show`,
    `tag @e[tag=${TAG.hidden}] remove ${TAG.hidden}`,
    'data remove storage rlk:cine sp', 'data remove storage rlk:cine face',
    `scoreboard objectives remove ${OBJ}`]);
  fn('show', ['# Internal (@s = the player): the avatar the actor hid shows again. A rig character\'s avatar stays hidden under its rig.',
    `execute unless entity @e[tag=rlk_av,tag=${TAG.hidden},limit=1] run return 0`,
    `execute if data storage rlk:cine av run data modify entity ${AV} profile set from storage rlk:cine av`,
    'data remove storage rlk:cine av',
    'execute if score @s pmVisible matches 1 run return 0', 'execute if score @s pmActive matches 1 run return 0',
    `effect clear ${AV} minecraft:invisibility`,
    `item replace entity ${AV} weapon.mainhand from entity @s hotbar.0`, 'function rlk:view/av_unwrap',
    `execute if score #charN tmp matches 7..8 run item replace entity ${AV} weapon.mainhand with minecraft:air`]);
  if (debugDp) {
    for (const c of CINE_CHARS) dbgPut(`cine_dbg/spawn_${c.id}`, PARTS.map((n, i) => summon(n, i, n === 'weapon' ? 'rlk:player_motion/weapons/cine_sword' : `rlk:player_motion/${c.key}/${n}`)));
    if (!fs.existsSync(path.join(debugDp, 'pack.mcmeta'))) fs.copyFileSync(path.join(dpRoot, 'pack.mcmeta'), path.join(debugDp, 'pack.mcmeta'));
  }
  manifest.checks.warnings = warns;
  put(path.join(cineDir, 'manifest.json'), JSON.stringify(manifest, (k, v) => v, 0).replace(/("(?:shift|hilt|tip|hand_r|hand_l|pommel|foot_r|foot_l|head|shoulder_r|chest|waist)":)/g, '\n  $1').replace(/("(?:cs0|cs1|repel|ending|coda)":\{"id")/g, '\n $1'));
  for (const w of warns) console.log('cine warning: ' + w);
  if (errors.length) throw new Error('cine actor:\n  ' + errors.join('\n  '));
  console.log(`Built the cutscene actor: ${CLIPS.length} clips, ${Object.values(manifest.clips).reduce((s, c) => s + c.keys, 0)} keys in ${Object.values(manifest.clips).reduce((s, c) => s + c.key_files, 0)} files.`);
}
