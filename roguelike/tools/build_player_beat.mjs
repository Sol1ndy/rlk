// Round V, lane VP (tools/dev/plan/combat/v_brief.md 3 "VP", 5): the avatar side of the perfect parry / perfect dodge beat.
// Invoked by build_player_rig.mjs (not run on its own). From tools/player_motion/beat/clips.json (one body track for all seven
// characters, sparse keys) it makes
//   rig characters (arle, skirk, navia)   dense clips pparry / pdodge (+ _i for the second loco weapon: scythe, cryo sword),
//                                         compiled by build_player_rig.mjs like any other clip (drawn, yaw locked, no fx)
//   mannequin characters (lumine, clorinde, ronova, nefer)   the same motion on a stand-in rig, char/motion/lite/**: the
//                                         cutscene actor's part models of that character (build_player_cine.mjs) + the weapon
//                                         the mannequin holds; the mannequin is hidden while it plays
//   char/motion/beat/**   the entry points player/def/beat/* calls: parry, dodge0, dodge, face, wglow_on / _off (the weapon
//                         glows yellow-white), tint_on / _off (the red-pink body glow of the perfect dodge), off
//   RP   the glow variants: <weapon>_glow for the five rig weapon models a beat clip shows (its own elements + an emissive
//        shell of the same elements on yellow-white "hot" copies of its own sprites), wg/<vanilla sword> for the swords a mannequin holds (the vanilla model + a glow card along
//        the blade), wg/orb for a catalyst character's hand, and their three small sprites
// Checks (throw): no body part below the floor on any tick, the weapon solve is finite.
// --beat-allow: report floor failures instead of stopping (authoring only).
// --beat-debug-dp <dir>: beat_dbg/spawn_<char>, beat_dbg/<char>/<clip>/<t> and <dir>/rp (a stand-in sword model) for the
// drawing tool tools/dev/sim/cb/beat_sheet.py.
import fs from 'node:fs';
import path from 'node:path';
import {png, paint, WEAPON_SPRITES} from './weapon_paint.mjs';
import {naviaWeaponSprites} from './navia_weapon_paint.mjs';

const rad = d => d * Math.PI / 180;
const mul = (a, b) => { const [x, y, z, w] = a, [X, Y, Z, W] = b; return [w * X + x * W + y * Z - z * Y, w * Y - x * Z + y * W + z * X, w * Z + x * Y - y * X + z * W, w * W - x * X - y * Y - z * Z]; };
const quat = (e = [0, 0, 0]) => { const [x, y, z] = e.map(a => rad(a) / 2); return mul(mul([0, 0, Math.sin(z), Math.cos(z)], [0, Math.sin(y), 0, Math.cos(y)]), [Math.sin(x), 0, 0, Math.cos(x)]); };
const conj = q => [-q[0], -q[1], -q[2], q[3]];
const rot = (q, v) => mul(mul(q, [...v, 0]), conj(q)).slice(0, 3);
const norm = v => { const l = Math.hypot(...v); return v.map(x => x / l); };
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
// shortest rotation taking unit u to unit d
function fromTo(u, d) {
  const c = dot(u, d);
  if (c < -0.999999) { const a = norm(Math.abs(u[0]) < 0.9 ? cross(u, [1, 0, 0]) : cross(u, [0, 0, 1])); return [...a, 0]; }
  const x = cross(u, d), q = [...x, 1 + c], l = Math.hypot(...q);
  return q.map(v => v / l);
}
// euler [x, y, z] degrees with quat(e) = qz * qy * qx (the rig's order)
function eulerOf(q) {
  const [x, y, z, w] = q;
  const r20 = 2 * (x * z - w * y), r21 = 2 * (y * z + w * x), r22 = 1 - 2 * (x * x + y * y), r10 = 2 * (x * y + w * z), r00 = 1 - 2 * (y * y + z * z);
  const sy = Math.max(-1, Math.min(1, -r20));
  let ex, ey = Math.asin(sy), ez;
  if (Math.abs(sy) > 0.99999) { ex = Math.atan2(-2 * (y * z - w * x), 1 - 2 * (x * x + z * z)); ez = 0; }
  else { ex = Math.atan2(r21, r22); ez = Math.atan2(r10, r00); }
  return [ex, ey, ez].map(a => Math.round(a * 180 / Math.PI * 1000) / 1000);
}
const BODY = ['shift', 'root', 'torso', 'head', 'right_arm', 'right_elbow', 'left_arm', 'left_elbow', 'right_leg', 'right_knee', 'left_leg', 'left_knee'];
const lerp = (a, b, t) => a.map((x, i) => x + (b[i] - x) * t);
const r3 = v => v.map(x => Math.round(x * 1000) / 1000);

export function loadBeat(here) {
  return JSON.parse(fs.readFileSync(path.join(here, 'player_motion/beat/clips.json'), 'utf8')).clips;
}
// Keys are sticky like the rig's frames; every tick 0..length gets a body pose and a blade direction.
function dense(clip) {
  let prev = Object.fromEntries(BODY.map(k => [k, [0, 0, 0]]));
  const keys = clip.keys.map(k => { prev = {...prev, ...k.pose}; return {tick: k.tick, pose: structuredClone(prev), blade: k.blade}; });
  if (keys[0].tick !== 0 || keys.at(-1).tick !== clip.length) throw new Error('beat clip keys must start at tick 0 and end at the clip length');
  const out = [];
  for (let t = 0; t <= clip.length; t++) {
    let a = keys[0], b = keys[0];
    for (const k of keys) { if (k.tick <= t) a = k; if (k.tick >= t) { b = k; break; } }
    const u = b.tick === a.tick ? 0 : (t - a.tick) / (b.tick - a.tick), pose = {};
    for (const f of BODY) pose[f] = lerp(a.pose[f], b.pose[f], u);
    // grounded ticks: the lower foot (the end of the shin's centre line) stands exactly on the floor
    if ((clip.ground || []).some(([t0, t1]) => t >= t0 && t <= t1)) pose.shift = [pose.shift[0], pose.shift[1] - footY(pose), pose.shift[2]];
    out.push({pose, a, b, u});
  }
  return out;
}
// height of the lower foot above the floor (hips at 0.75 + shift Y; thigh and shin 0.375 each; the root turns about the hips)
function footY(p) {
  const root = quat(p.root), ys = ['right', 'left'].map(side => {
    const leg = quat(p[side + '_leg']), shin = mul(leg, quat(p[side + '_knee']));
    return 0.75 + p.shift[1] + rot(root, [0, -0.375, 0].map((v, i) => rot(leg, [0, -0.375, 0])[i] + rot(shin, [0, -0.375, 0])[i]))[1];
  });
  return Math.min(...ys);
}
const foreQ = p => mul(quat(p.root), mul(mul(quat(p.torso), quat(p.right_arm)), quat(p.right_elbow)));
// The weapon fields that put the model's blade axis along the wanted direction: axis / grip are the model's blade axis and
// grip point in the rig's authoring frame (a rig weapon: +Y, the origin; the vanilla sword sprite: its diagonal, its handle).
function solve(frame, axis, grip, scale) {
  const {pose, a, b, u} = frame, qf = foreQ(pose);
  const dir = k => k.blade === 'arm' ? rot(foreQ(k.pose), [0, -1, 0]) : norm(k.blade);
  const d = norm(lerp(dir(a), dir(b), u));
  const qw = mul(conj(qf), fromTo(norm(axis), d));
  const weapon = eulerOf(qw), shift = rot(quat(weapon), grip.map(x => -x * scale));
  if (![...weapon, ...shift].every(Number.isFinite)) throw new Error('beat: weapon solve is not finite');
  return {...Object.fromEntries(BODY.map(f => [f, r3(pose[f])])), weapon, weapon_shift: r3(shift), weapon_scale: [scale, scale, scale]};
}
const SWORD_AXIS = [-Math.SQRT1_2, Math.SQRT1_2, 0], SWORD_GRIP = [0.28, -0.28, 0], SWORD_SCALE = 0.85;
export const BEAT_CLIPS = ['pparry', 'pdodge'];
// Round W (lane WP): the dodge itself (the reference game's dodge set; the old dash is gone). dash = the plain dodge with no
// direction held (a twist on the spot), dash_l = with a direction held (a low lunge-step), dash_b = the move turned into a
// back-step away from the attacker when the dodge avoided an attack, dash2 = the second move of a double dodge (an aerial
// cartwheel). Rig characters: compiled clips, weapon on the back ("sheathed", as the old dash clip was); the mannequin
// characters: the mannequin's own crouch pose for dash / dash_l / dash_b (player/dodge/crouch), dash2 = the stand-in rig (lite/f).
export const DODGE_CLIPS = ['dash', 'dash_l', 'dash_b', 'dash2'];
const DODGE_ACTIVE = DODGE_CLIPS.map(c => `unless data storage rlk:player_motion active{clip:"${c}"}`).join(' ');
const LITE_CLIPS = [['pparry', 'p'], ['pdodge', 'd'], ['dash2', 'f']];        // clip, its lite/<short>/ folder; plClip = index + 1
const bodyOnly = f => Object.fromEntries(BODY.map(k => [k, r3(f.pose[k])]));
export const LITE = [                          // #charN, the cutscene actor's part models, what the mannequin holds
  {n: 1, key: 'lumine', hold: 'sword'}, {n: 4, key: 'clorinde', hold: 'sword'},
  {n: 7, key: 'ronova', hold: 'catalyst', cat: 'rlk_rncat'}, {n: 8, key: 'nefer', hold: 'catalyst', cat: 'rlk_nfcat'}];
export const HELD_SWORDS = ['iron_sword', 'diamond_sword', 'netherite_sword'];
const variantsOf = info => info.locoWeapons.map((w, i) => ({suffix: i ? '_i' : '', weapon: w.weapon, cond: w.if}));

// Clips for one rig character, merged into its clip set by build_player_rig.mjs before compiling.
export function beatFragments(here, char, info) {
  const src = loadBeat(here), clips = {};
  for (const name of BEAT_CLIPS) for (const v of variantsOf(info)) {
    clips[name + v.suffix] = {
      length: src[name].length, weapon: v.weapon, weapon_state: 'drawn', draw_fx: false, locked_yaw: true, basis: 'body', audio: false,
      note: `GENERATED by build_player_beat.mjs from player_motion/beat/clips.json (${name}); edit that file.`,
      frames: dense(src[name]).map((f, t) => ({tick: t, pose: solve(f, [0, 1, 0], [0, 0, 0], 1)}))};
  }
  for (const name of DODGE_CLIPS) clips[name] = {
    length: src[name].length, weapon: info.weapon, weapon_state: 'sheathed', draw_fx: false, locked_yaw: true, basis: 'body', audio: false,
    note: `GENERATED by build_player_beat.mjs from player_motion/beat/clips.json (${name}); edit that file.`,
    frames: dense(src[name]).map((f, t) => ({tick: t, pose: bodyOnly(f)}))};
  return clips;
}

// ---- glow geometry ---------------------------------------------------------------------------------------------------------
// The emissive shell of a rig weapon: every element once more, 0.3 px larger on each side, with the same faces and UVs on the
// "hot" copy of each sprite (the weapon's own painting pushed to yellow-white, a little transparent), light emission 15, no
// shading: the model itself turns yellow-white and follows every cut-out of its sprites (a flat-colour shell would turn the
// scythe's crescent quad into a rectangle).
export const GLOW_MODELS = ['spear', 'scythe', 'sword', 'cryo_sword', 'navia_halberd'];     // what a beat clip can show
export function glowShell(elements, inflate = 0.3) {
  return elements.map(el => ({
    from: el.from.map(x => Math.max(-16, x - inflate)), to: el.to.map(x => Math.min(32, x + inflate)),
    ...(el.rotation ? {rotation: el.rotation} : {}), shade: false, light_emission: 15,
    faces: Object.fromEntries(Object.entries(el.faces).map(([k, f]) => [k, {...f, texture: f.texture + '_hot'}]))}));
}
export const hotTextures = textures => Object.fromEntries(Object.entries(textures).filter(([k]) => k !== 'particle').map(([k, v]) => [k + '_hot', v + '_hot']));
const SPR = n => 'rlk:player_motion/weapons/' + n;
const HOT = [255, 246, 196];
function sprites(rpRoot, hot) {
  const dir = path.join(rpRoot, 'assets/rlk/textures/player_motion/weapons');
  fs.mkdirSync(dir, {recursive: true});
  const px = (w, h, f) => { const a = Buffer.alloc(w * h * 4); for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) a.set(f(x, y).map(v => Math.max(0, Math.min(255, Math.round(v)))), (y * w + x) * 4); return png(w, h, a); };
  // <sprite>_hot: the sprite at half resolution (the UVs are relative), 90 % toward yellow-white (ref_pd.md: #FDF7D4 /
  // #F5C058), alpha 235 where the sprite is opaque (round W, review T3-07: at 72 % / 205 the dark red scythe read orange-brown)
  const all = {...WEAPON_SPRITES, ...naviaWeaponSprites()}, names = [];
  for (const name of hot) {
    const [w, h, fn] = all[name], hw = Math.max(8, w >> 1), hh = Math.max(8, h >> 1), buf = paint(hw, hh, fn);
    for (let i = 0; i < hw * hh; i++) {
      if (!buf[i * 4 + 3]) continue;
      for (let k = 0; k < 3; k++) buf[i * 4 + k] = Math.round(buf[i * 4 + k] + (HOT[k] - buf[i * 4 + k]) * 0.9);
      buf[i * 4 + 3] = 235;
    }
    fs.writeFileSync(path.join(dir, name + '_hot.png'), png(hw, hh, buf));
    names.push(name + '_hot');
  }
  // wglow_blade: for the vanilla sword sprite (blade on the texture diagonal): a hot line along the blade in a soft halo
  fs.writeFileSync(path.join(dir, 'wglow_blade.png'), px(64, 64, (x, y) => {
    const u = (x + 0.5) / 64, v = 1 - (y + 0.5) / 64, along = (u + v) / 2, off = Math.abs(u - v) / Math.SQRT2;
    const span = Math.max(0, Math.min(1, (along - 0.2) / 0.12)) * Math.max(0, Math.min(1, (1.0 - along) / 0.06));
    const core = Math.exp(-((off / 0.035) ** 2)), halo = Math.exp(-((off / 0.13) ** 2)) * 0.55;
    const al = Math.max(core, halo) * span;
    return [255, 247 - 30 * (1 - core), 205 - 90 * (1 - core), 235 * al];
  }));
  // wglow_orb: a round yellow-white light (a catalyst character's hand)
  fs.writeFileSync(path.join(dir, 'wglow_orb.png'), px(32, 32, (x, y) => {
    const r = Math.hypot(x - 15.5, y - 15.5) / 15.5, core = Math.exp(-((r / 0.28) ** 2)), halo = Math.exp(-((r / 0.62) ** 2)) * 0.6;
    return [255, 248 - 26 * (1 - core), 210 - 95 * (1 - core), r > 1 ? 0 : 240 * Math.max(core, halo)];
  }));
  return [...names, 'wglow_blade', 'wglow_orb'];
}
// Atlas entries, appended once after the weapon sprites (weapon_paint.mjs) and before the rig's block aliases are re-appended.
// hot = the sprite names the glow models use (build_player_rig.mjs collects them from the models' faces).
export function beatAtlas(rpRoot, hot) {
  const names = sprites(rpRoot, hot), p = path.join(rpRoot, 'assets/minecraft/atlases/items.json');
  const atlas = JSON.parse(fs.readFileSync(p, 'utf8')), known = new Set(atlas.sources.map(s => s.sprite || s.resource));
  for (const n of names) if (!known.has(SPR(n))) atlas.sources.push({type: 'minecraft:single', resource: SPR(n)});
  fs.writeFileSync(p, JSON.stringify(atlas, null, 2) + '\n');
}

// ---- everything else -------------------------------------------------------------------------------------------------------
export function buildBeat({fn, json, assets, rpRoot, here, transform, nbt, characters, modelIds, glowing, weaponSpan, arg}) {
  const src = loadBeat(here), M = 'rlk:char/motion';
  const parts = ['head', 'body', 'right_arm', 'right_forearm', 'left_arm', 'left_forearm', 'right_leg', 'right_shin', 'left_leg', 'left_shin', 'weapon'];
  const rig = Object.entries(characters);
  const GLOW = 'shadow_strength:0.99f,brightness:{sky:15,block:15}';
  // ---- RP: the mannequin swords' glow variants and the orb ----
  const card = (tex, a, b, z) => ({from: [a, a, z], to: [b, b, z], shade: false, light_emission: 15,
    faces: {north: {texture: '#glow', uv: [16, 0, 0, 16]}, south: {texture: '#glow', uv: [0, 0, 16, 16]}}});
  json(path.join(assets, 'models/item/player_motion/wg/blade.json'), {ambientocclusion: false, textures: {glow: SPR('wglow_blade'), particle: SPR('wglow_blade')},
    elements: [card('glow', -2, 18, 6.9), card('glow', -2, 18, 9.1)]});
  const orbEl = (ax) => ({from: ax === 'x' ? [8, 3, 3] : ax === 'y' ? [3, 8, 3] : [3, 3, 8], to: ax === 'x' ? [8, 13, 13] : ax === 'y' ? [13, 8, 13] : [13, 13, 8], shade: false, light_emission: 15,
    faces: Object.fromEntries((ax === 'x' ? ['east', 'west'] : ax === 'y' ? ['up', 'down'] : ['north', 'south']).map(k => [k, {texture: '#glow', uv: [0, 0, 16, 16]}]))});
  json(path.join(assets, 'models/item/player_motion/wg/orb.json'), {ambientocclusion: false, textures: {glow: SPR('wglow_orb'), particle: SPR('wglow_orb')}, elements: ['x', 'y', 'z'].map(orbEl)});
  json(path.join(assets, 'items/player_motion/wg/orb.json'), {model: {type: 'minecraft:model', model: 'rlk:item/player_motion/wg/orb'}});
  for (const s of HELD_SWORDS) json(path.join(assets, 'items/player_motion/wg', s + '.json'), {model: {type: 'minecraft:composite', models: [
    {type: 'minecraft:model', model: 'minecraft:item/' + s}, {type: 'minecraft:model', model: 'rlk:item/player_motion/wg/blade'}]}});

  // ---- floor check (display space: y is up; a part box corner c of the model sits at t + R(q)(-cx, cy, -cz) * s) ----
  const BOX = {head: [[-.28, 0, -.28], [.28, .53, .28]], body: [[-.27, -.77, -.14], [.27, .02, .14]],
    right_arm: [[-.11, -.26, -.14], [.11, .13, .14]], right_forearm: [[-.11, -.39, -.14], [.11, .01, .14]],
    left_arm: [[-.11, -.26, -.14], [.11, .13, .14]], left_forearm: [[-.11, -.39, -.14], [.11, .01, .14]],
    right_leg: [[-.14, -.39, -.14], [.14, .01, .14]], right_shin: [[-.14, -.39, -.14], [.14, .01, .14]],
    left_leg: [[-.14, -.39, -.14], [.14, .01, .14]], left_shin: [[-.14, -.39, -.14], [.14, .01, .14]]};
  const lowest = (vals, span) => {
    let lo = Infinity, who = '';
    const see = (name, v, c) => { const y = v.t[1] + rot(v.q, [-c[0], c[1], -c[2]].map((x, i) => x * (v.s ? v.s[i] : 1)))[1]; if (y < lo) { lo = y; who = name; } };
    // legs: the limb's centre line (a tilted foot's toe or heel corner dips a few centimetres in every clip of this rig);
    // head, torso and arms: the box corners
    for (const [name, [a, b]] of Object.entries(BOX)) {
      if (name.includes('leg') || name.includes('shin')) { see(name, vals[name], [0, a[1] + 0.015, 0]); continue; }
      for (const x of [a[0], b[0]]) for (const y of [a[1], b[1]]) for (const z of [a[2], b[2]]) see(name, vals[name], [x, y, z]);
    }
    if (span) for (const y of span) see('weapon', vals.weapon, [0, (y - 8) / 16, 0]);
    return [lo, who];
  };
  const report = [];
  // --beat-allow (authoring only): report the floor failures and go on
  const bad = msg => { if (arg('--beat-allow') !== undefined || process.argv.includes('--beat-allow')) console.log('ALLOWED: ' + msg); else throw new Error(msg); };
  const check = (label, vals, span) => {
    const [lo, who] = lowest(vals, null);
    if (lo < -0.02) bad(`beat ${label}: ${who} is ${(-lo).toFixed(3)} b below the floor`);
    const [wlo] = span ? lowest(vals, span) : [lo];
    report.push(`${label} body ${lo.toFixed(3)} weapon ${wlo.toFixed(3)}`);
    if (wlo < -0.12) bad(`beat ${label}: the weapon is ${(-wlo).toFixed(3)} b below the floor`);
  };
  const debugDp = arg('--beat-debug-dp') && path.resolve(arg('--beat-debug-dp'));
  const dbg = (n, lines) => { if (!debugDp) return; const p = path.join(debugDp, 'data/rlk/function', n + '.mcfunction'); fs.mkdirSync(path.dirname(p), {recursive: true}); fs.writeFileSync(p, lines.join('\n') + '\n'); };
  if (debugDp) fs.rmSync(path.join(debugDp, 'data/rlk/function/beat_dbg'), {recursive: true, force: true});
  const dbgSummon = (name, item, v) => `summon minecraft:item_display ~ ~ ~ {Tags:["rlk_pm","rlk_pm_${name}"],billboard:"fixed",item_display:"none",transformation:${nbt(v)},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"${item}"}}}`;
  const dbgPose = vals => parts.map(n => `data merge entity @e[tag=rlk_pm_${n},limit=1] {start_interpolation:0,interpolation_duration:0,transformation:${nbt(vals[n])}}`);

  // ---- rig characters: the per-tick floor check and the debug frames of the compiled clips ----
  for (const [char, info] of rig) for (const name of BEAT_CLIPS) for (const v of variantsOf(info)) {
    const frames = dense(src[name]).map(f => solve(f, [0, 1, 0], [0, 0, 0], 1));
    frames.forEach((pose, t) => {
      const vals = transform({...pose, weapon_attach: 'hand', weapon_scale: pose.weapon_scale.map(x => x * info.weaponScale)});
      check(`${char}/${name + v.suffix} t${t}`, vals, weaponSpan[v.weapon]);
      dbg(`beat_dbg/${char}/${name + v.suffix}/${t}`, dbgPose(vals));
      if (t === 0) dbg(`beat_dbg/spawn_${char}${v.suffix}`, parts.map(n => dbgSummon(n, n === 'weapon' ? `rlk:player_motion/weapons/${v.weapon}` : `rlk:player_motion/${char}/${n}`, vals[n])));
      if (t === 0) dbg(`beat_dbg/spawn_${char}${v.suffix}_glow`, parts.map(n => dbgSummon(n, n === 'weapon' ? `rlk:player_motion/weapons/${v.weapon}_glow` : `rlk:player_motion/${char}/${n}`, vals[n])));
    });
    for (const c of [name + v.suffix]) {
      fn(`${char}_fx/${c}`, `# Beat clip ${c} (build_player_beat.mjs): no particles of its own - the effects are player/def/fx/* on the beat's clock.`);
      fn(`events/${char}/${c}`, `# Beat clip ${c} (build_player_beat.mjs): no hit, step or lock events - presentation only, cut short by the player's next action.`);
    }
  }
  // the dodge clips of the rig characters (weapon on the back: checked and drawn without it)
  for (const [char] of rig) for (const name of DODGE_CLIPS) {
    dense(src[name]).forEach((f, t) => {
      const vals = transform({...bodyOnly(f), weapon_attach: 'hand', weapon_scale: [0, 0, 0]});
      check(`${char}/${name} t${t}`, vals, null);
      dbg(`beat_dbg/${char}/${name}/${t}`, dbgPose(vals));
    });
    fn(`${char}_fx/${name}`, `# Dodge clip ${name} (build_player_beat.mjs): no particles of its own - the puff and the sounds are player/dash_go's.`);
    fn(`events/${char}/${name}`, `# Dodge clip ${name} (build_player_beat.mjs): no hit, step or lock events - gameplay moves the body (player/dash_move_tick).`);
  }
  // ---- the stand-in rig of the mannequin characters (char/motion/lite) ----
  const liteFrames = Object.fromEntries(LITE_CLIPS.map(([name]) => [name, dense(src[name]).map(f => transform({...solve(f, SWORD_AXIS, SWORD_GRIP, SWORD_SCALE), weapon_attach: 'hand'}))]));
  const LP = n => `@e[tag=rlk_pl_${n},limit=1]`;
  LITE_CLIPS.forEach(([name, short], ci) => {
    liteFrames[name].forEach((vals, t) => {
      check(`lite/${name} t${t}`, vals, null);
      fn(`lite/${short}/${t}`, parts.map(n => `data merge entity ${LP(n)} {interpolation_duration:1,start_interpolation:0,transformation:${nbt(vals[n])}}`).join('\n'));
      for (const c of LITE) dbg(`beat_dbg/${c.key}/${name}/${t}`, dbgPose(vals));
    });
    fn(`lite/${short}/pose`, liteFrames[name].map((_, t) => `execute if score @s plTick matches ${t} run return run function ${M}/lite/${short}/${t}`).join('\n'));
  });
  for (const c of LITE) {
    const v0 = liteFrames.pparry[0];
    fn(`lite/spawn_${c.key}`, [`# ${c.key}'s stand-in rig at the avatar: the cutscene actor's part models + the weapon the mannequin holds (copied before it is hidden).`,
      ...parts.map(n => `summon minecraft:item_display ~ ~ ~ {Tags:["rlk_pet","rlk_pl","rlk_pl_${n}"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:8f,height:6f,shadow_radius:0f,transformation:${nbt(v0[n])}${n === 'weapon' ? '' : `,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/${c.key}/${n}"}}`}}`),
      ...(c.hold === 'sword' ? [`item replace entity ${LP('weapon')} contents from entity @e[tag=rlk_av,limit=1] weapon.mainhand`] : [])].join('\n'));
    for (const g of ['', '_glow']) dbg(`beat_dbg/spawn_${c.key}${g}`, parts.map(n => dbgSummon(n, n === 'weapon' ? (c.hold === 'sword' ? 'rlk:beat_dbg/sword' + g : g ? 'rlk:player_motion/wg/orb' : 'rlk:empty') : `rlk:player_motion/${c.key}/${n}`, v0[n])));
  }
  if (debugDp) {       // the stand-in for the vanilla sword sprite (same plane, blade on the same diagonal) and its glow composite
    const a = path.join(debugDp, 'rp/assets/rlk');
    const bar = []; for (let i = 0; i < 13; i++) bar.push({from: [1.5 + i, 1.5 + i, 7.5], to: [3.5 + i, 3.5 + i, 8.5], faces: Object.fromEntries(['north', 'south', 'east', 'west', 'up', 'down'].map(k => [k, {texture: '#t', uv: [0, 0, 16, 16]}]))});
    bar.push({from: [3, 5.5, 7.4], to: [5.5, 7, 8.6], faces: bar[0].faces}, {from: [5.5, 3, 7.4], to: [7, 5.5, 8.6], faces: bar[0].faces});
    json(path.join(a, 'models/item/beat_dbg/sword.json'), {textures: {t: 'rlk:player_motion/light_gray_concrete'}, elements: bar});
    json(path.join(a, 'items/beat_dbg/sword.json'), {model: {type: 'minecraft:model', model: 'rlk:item/beat_dbg/sword'}});
    json(path.join(a, 'items/beat_dbg/sword_glow.json'), {model: {type: 'minecraft:composite', models: [{type: 'minecraft:model', model: 'rlk:item/beat_dbg/sword'}, {type: 'minecraft:model', model: 'rlk:item/player_motion/wg/blade'}]}});
    fs.writeFileSync(path.join(debugDp, 'floor.txt'), report.join('\n') + '\n');
  }
  const liteIf = c => `execute if score #charN tmp matches ${c.n}`;
  const HIDE = ['effect give @e[tag=rlk_av,limit=1] minecraft:invisibility infinite 0 true', 'item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand with minecraft:air', 'item replace entity @e[tag=rlk_av,limit=1] weapon.offhand with minecraft:air'];
  fn('lite/hide', ['# The mannequin is hidden while its stand-in rig plays (as char/motion/hide_avatar does for the rig characters).', ...HIDE].join('\n'));
  LITE_CLIPS.forEach(([name, short], ci) => fn(`lite/start_${short}`, [
    `# @s = player (a mannequin character; from ${M}/${name === 'pparry' ? 'beat/parry' : name === 'pdodge' ? 'beat/dodge' : 'dash'}): play ${name} on the stand-in rig. Nothing in developer mode (no avatar).`,
    'execute unless entity @e[tag=rlk_av,limit=1] run return 0',
    '# parts left by another character or an unfinished run are not reused',
    'execute unless score @s plActive matches 1 run kill @e[tag=rlk_pl]',
    ...LITE.map(c => `${liteIf(c)} unless entity @e[tag=rlk_pl,limit=1] at @e[tag=rlk_av,limit=1] run function ${M}/lite/spawn_${c.key}`),
    'execute unless entity @e[tag=rlk_pl,limit=1] run return 0',
    'scoreboard players set @s plActive 1', 'scoreboard players set @s plTick -1', `scoreboard players set @s plClip ${ci + 1}`, `scoreboard players set @s plLen ${src[name].length}`,
    name === 'dash2' ? '# heading: as the avatar faces; char/motion/dash turns it to the dodge direction (lite/face)' : '# heading: toward the attacker (the beat\'s tag), else as the avatar faces; fixed for the clip',
    'kill @e[tag=rlk_pl_basis]', 'execute at @e[tag=rlk_av,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_pet","rlk_pl_basis"]}',
    'execute at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_av,limit=1] rotated ~ 0 run tp @e[tag=rlk_pl_basis,limit=1] ~ ~ ~ ~ ~',
    ...(name === 'dash2' ? [] : ['execute if entity @e[tag=rlk_bt_atk,limit=1] as @e[tag=rlk_pl_basis,limit=1] at @s facing entity @e[tag=rlk_bt_atk,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~']),
    'execute at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_pl_basis,limit=1] rotated ~ 0 run tp @e[tag=rlk_pl] ~ ~ ~ ~ 0',
    `function ${M}/lite/hide`].join('\n')));
  fn('lite/tick', ['# @s = player, once per game tick while the stand-in rig plays (player/def/beat/post, after the avatar moved).',
    `execute unless entity @e[tag=rlk_av,limit=1] run return run function ${M}/lite/stop`,
    `execute unless entity @e[tag=rlk_pl,limit=1] run return run function ${M}/lite/stop`,
    `execute if score @s dead matches 1 run return run function ${M}/lite/stop`,
    `execute if score @s pkMode matches 1.. run return run function ${M}/lite/stop`,
    'scoreboard players add @s plTick 1',
    `execute if score @s plTick > @s plLen run return run function ${M}/lite/stop`,
    `function ${M}/lite/hide`,
    'execute at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_pl_basis,limit=1] rotated ~ 0 run tp @e[tag=rlk_pl] ~ ~ ~ ~ 0',
    `execute if score @s plClip matches 1 run return run function ${M}/lite/p/pose`,
    `execute if score @s plClip matches 3 run return run function ${M}/lite/f/pose`,
    `function ${M}/lite/d/pose`].join('\n'));
  fn('lite/face', ['# The stand-in rig\'s heading -> the dodge direction (macro dx / dz = the unit vector, from char/motion/dash).',
    '$execute as @e[tag=rlk_pl_basis,limit=1] at @s run tp @s ~ ~ ~ facing ~$(dx) ~ ~$(dz)',
    'execute at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_pl_basis,limit=1] rotated ~ 0 run tp @e[tag=rlk_pl] ~ ~ ~ ~ 0'].join('\n'));
  fn('lite/stop', ['# @s = player. The stand-in rig goes, the mannequin shows again with its weapon (as char/motion/stop).',
    'scoreboard players set @s plActive 0', 'kill @e[tag=rlk_pl]', 'kill @e[tag=rlk_pl_basis]',
    'execute if entity @e[tag=rlk_av,limit=1] run effect clear @e[tag=rlk_av,limit=1] minecraft:invisibility',
    'execute if entity @e[tag=rlk_av,limit=1] run item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand from entity @s hotbar.0',
    'execute if entity @e[tag=rlk_av,limit=1] run function rlk:view/av_unwrap',
    'execute if score #charN tmp matches 7..8 run item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand with minecraft:air'].join('\n'));

  // ---- char/motion/beat: the entry points ----
  const startRig = clip => rig.flatMap(([char, info]) => variantsOf(info).map((v, i, all) =>
    `execute if score #charN tmp matches ${info.id} ${all.length === 1 ? '' : i ? 'if ' + v.cond + ' ' : 'unless ' + all[1].cond + ' '}run function ${M}/start {char:"${char}",clip:"${clip + v.suffix}"}`));
  fn('beat/face', ['# The beat clip\'s heading: toward the attacker (tag rlk_bt_atk) when there is one (the lunge goes at it, the handspring lands',
    '# facing it); the clip\'s yaw is locked on its basis marker.',
    'execute unless entity @e[tag=rlk_bt_atk,limit=1] run return 0',
    'execute as @e[tag=rlk_pm_basis,limit=1] at @s facing entity @e[tag=rlk_bt_atk,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~',
    'execute at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_pm_basis,limit=1] rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0'].join('\n'));
  fn('beat/parry', ['# @s = player, on the contact tick of a perfect parry (player/def/beat/start_p): the deflect -> lunge freeze -> ready guard motion',
    '# (clip pparry; ref_pd.md 4) and the weapon\'s yellow-white glow. Rig characters play their clip, mannequin characters the stand-in rig.',
    '# A rig character that has already started another action since the F (an attack clip, a skill) keeps it: only the guard clip',
    '# or no clip gives way to the lunge. The weapon glows either way.',
    `execute if score @s pmActive matches 1 unless data storage rlk:player_motion active{clip:"guard"} unless data storage rlk:player_motion active{clip:"pparry"} unless data storage rlk:player_motion active{clip:"pparry_i"} unless data storage rlk:player_motion active{clip:"pdodge"} unless data storage rlk:player_motion active{clip:"pdodge_i"} ${DODGE_ACTIVE} run return run function ${M}/beat/wglow_on`,
    ...startRig('pparry'),
    `execute if data storage rlk:player_motion active{clip:"pparry"} run function ${M}/beat/face`,
    `execute if data storage rlk:player_motion active{clip:"pparry_i"} run function ${M}/beat/face`,
    ...LITE.map(c => `${liteIf(c)} run function ${M}/lite/start_p`),
    `function ${M}/beat/wglow_on`].join('\n'));
  fn('beat/dodge', ['# @s = player, on the trigger tick of a perfect dodge (player/def/beat/start_d; round W: at once, no wind-up): the back',
    '# handspring - launch, 360 degrees backward in 6 ticks, landed facing the attacker on tick 7, the ready stance on tick 10 (clip',
    '# pdodge) - and the red-pink body glow. Rig characters play their clip, mannequin characters the stand-in rig.',
    '# Not while a move-locked action plays, nor over a rig clip other than the dodge\'s own (dash / dash2): the flip is presentation',
    '# and never cuts the player\'s own action. The glow starts either way.',
    `execute if score @s pmMoveLock matches 1 run return run function ${M}/beat/tint_on`,
    `execute if score @s pmActive matches 1 ${DODGE_ACTIVE} run return run function ${M}/beat/tint_on`,
    ...startRig('pdodge'),
    `execute if data storage rlk:player_motion active{clip:"pdodge"} run function ${M}/beat/face`,
    `execute if data storage rlk:player_motion active{clip:"pdodge_i"} run function ${M}/beat/face`,
    ...LITE.map(c => `${liteIf(c)} run function ${M}/lite/start_d`),
    `function ${M}/beat/tint_on`].join('\n'));
  // char/motion/dash: the dodge's avatar motion (player/dash_go). #dgMv cb 1 = the plain step, 2 = the second move.
  const faceArgs = ['execute store result storage rlk:player_motion face.dx double 0.01 run scoreboard players get @s dashUX',
    'execute store result storage rlk:player_motion face.dz double 0.01 run scoreboard players get @s dashUZ'];
  const stepClip = (clip, sign) => [
    ...rig.map(([char, info]) => `execute if score #charN tmp matches ${info.id} run function ${M}/start {char:"${char}",clip:"${clip}"}`),
    ...LITE.map(c => `${liteIf(c)} if entity @e[type=minecraft:mannequin,tag=rlk_av,limit=1] run function rlk:player/dodge/crouch`),
    `execute unless data storage rlk:player_motion active{clip:"${clip}"} run return 0`,
    ...faceArgs.map(l => sign < 0 ? l.replace('double 0.01', 'double -0.01') : l), `function ${M}/dash_face with storage rlk:player_motion face`];
  fn('dash', ['# @s = player, from player/dash_go: the avatar\'s dodge motion (round W: the reference game\'s dodge set; build_player_beat.mjs).',
    '# #dgMv cb 1 = the plain dodge with no direction held: a twist on the spot (clip dash, 6 ticks), 3 = with a direction held: a',
    '# low lunge-step (clip dash_l, 10 ticks), 2 = the second move of a double dodge (char/motion/dash2). Mannequin characters: the',
    '# mannequin\'s own crouch pose while the body moves (player/dodge/crouch -> stand). The clip\'s yaw is locked and its basis turned',
    '# to the dodge direction (player/dash_dir: dashUX / dashUZ, unit x 100).',
    `execute if score #dgMv cb matches 2 run return run function ${M}/dash2`,
    `execute if score #dgMv cb matches 3 run return run function ${M}/dash_l`,
    ...stepClip('dash', 1)].join('\n'));
  fn('dash_l', ['# @s = player (char/motion/dash): the lunge-step clip toward the dodge direction.', ...stepClip('dash_l', 1)].join('\n'));
  fn('dash_b', ['# @s = player (player/dodge/away: the dodge avoided an attack; not over the perfect dodge\'s handspring or the cartwheel):',
    '# the upright back-step (clip dash_b, 8 ticks) facing the attacker - the basis is turned against the move (dashUX / dashUZ x -1).',
    ...stepClip('dash_b', -1)].join('\n'));
  fn('dash2', ['# @s = player (char/motion/dash): the double dodge\'s second move, an aerial cartwheel along the dodge direction (9 ticks;',
    '# rig characters: clip dash2, mannequin characters: the stand-in rig, lite/f).',
    ...rig.map(([char, info]) => `execute if score #charN tmp matches ${info.id} run function ${M}/start {char:"${char}",clip:"dash2"}`),
    ...faceArgs,
    `execute if data storage rlk:player_motion active{clip:"dash2"} run return run function ${M}/dash_face with storage rlk:player_motion face`,
    ...LITE.map(c => `${liteIf(c)} run function ${M}/lite/start_f`),
    `execute if score @s plActive matches 1 if score @s plClip matches 3 run function ${M}/lite/face with storage rlk:player_motion face`].join('\n'));
  // The weapon glows yellow-white: the rig weapon's model -> its _glow variant (shell + full brightness); a mannequin's sword ->
  // the vanilla model + glow card; a catalyst character: a light in the hand of the stand-in rig and the floating catalyst lit.
  // Every write to a display carries a changed shadow_strength: a bare NBT write would replay its last interpolation
  // (Display.readAdditionalSaveData always re-sends start_interpolation; with a changed render property the client blends from
  // what it shows).
  const wsel = '@e[tag=rlk_pm_weapon,limit=1]', lsel = LP('weapon');
  fn('beat/wglow_on', ['# @s = player. The weapon model itself glows yellow-white (until beat/wglow_off).',
    'scoreboard players set @s pbGlow 1',
    ...Object.entries(modelIds).filter(([name]) => GLOW_MODELS.includes(name)).map(([name, id]) => `execute if score @s pmWModel matches ${id} if score @s pmRigChar = #charN tmp run data merge entity ${wsel} {${GLOW},item:{components:{"minecraft:item_model":"rlk:player_motion/weapons/${name}_glow"}}}`),
    ...HELD_SWORDS.map(s => `execute if data entity ${lsel} {item:{components:{"minecraft:item_model":"minecraft:${s}"}}} run data merge entity ${lsel} {${GLOW},item:{components:{"minecraft:item_model":"rlk:player_motion/wg/${s}"}}}`),
    ...LITE.filter(c => c.hold === 'catalyst').flatMap(c => [
      `${liteIf(c)} if entity ${lsel} run data merge entity ${lsel} {${GLOW},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/wg/orb"}}}`,
      `${liteIf(c)} as @e[tag=${c.cat}] run data merge entity @s {Glowing:1b,glow_color_override:16774020}`])].join('\n'));
  fn('beat/wglow_off', ['# @s = player. The weapon goes back to its own model and light.',
    'execute unless score @s pbGlow matches 1 run return 0', 'scoreboard players set @s pbGlow 0',
    ...Object.entries(modelIds).filter(([name]) => GLOW_MODELS.includes(name)).flatMap(([name, id]) => [
      `execute if score @s pmWModel matches ${id} if score @s pmRigChar = #charN tmp run data merge entity ${wsel} {shadow_strength:1f,item:{components:{"minecraft:item_model":"rlk:player_motion/weapons/${name}"}}}`,
      ...(glowing.has(name) ? [] : [`execute if score @s pmWModel matches ${id} if score @s pmRigChar = #charN tmp run data remove entity ${wsel} brightness`])]),
    ...HELD_SWORDS.flatMap(s => [`execute if data entity ${lsel} {item:{components:{"minecraft:item_model":"rlk:player_motion/wg/${s}"}}} run data merge entity ${lsel} {shadow_strength:1f,item:{components:{"minecraft:item_model":"minecraft:${s}"}}}`]),
    `execute if entity ${lsel} run data remove entity ${lsel} brightness`,
    ...LITE.filter(c => c.hold === 'catalyst').flatMap(c => [
      `${liteIf(c)} if entity ${lsel} run data remove entity ${lsel} item`,
      `${liteIf(c)} as @e[tag=${c.cat}] run data merge entity @s {Glowing:0b}`])].join('\n'));
  const TINT = 'Glowing:1b,glow_color_override:16747660,brightness:{sky:15,block:15},shadow_strength:0.99f,item:{components:{"minecraft:custom_model_data":{colors:[16755376]}}}';
  const UNTINT = 'Glowing:0b,shadow_strength:1f,item:{components:{"minecraft:custom_model_data":{colors:[16777215]}}}';
  fn('beat/tint_on', ['# @s = player. The perfect dodge\'s red-pink glow on the whole body: every body part of the showing rig (the rig character\'s,',
    '# or the stand-in rig) is tinted red-pink (the part models\' tint), drawn at full brightness and outlined in pink.',
    'scoreboard players set @s pbTint 1',
    `execute as @e[tag=rlk_pm,tag=!rlk_pm_weapon] run data merge entity @s {${TINT}}`,
    `execute as @e[tag=rlk_pl,tag=!rlk_pl_weapon] run data merge entity @s {${TINT}}`].join('\n'));
  fn('beat/tint_off', ['# @s = player. The red-pink glow goes (the landing, or the beat ended early).',
    'execute unless score @s pbTint matches 1 run return 0', 'scoreboard players set @s pbTint 0',
    `execute as @e[tag=rlk_pm,tag=!rlk_pm_weapon] run function ${M}/beat/untint`,
    `execute as @e[tag=rlk_pl,tag=!rlk_pl_weapon] run function ${M}/beat/untint`].join('\n'));
  fn('beat/untint', [`data merge entity @s {${UNTINT}}`, 'data remove entity @s brightness'].join('\n'));
  fn('beat/off', ['# @s = player (player/def/beat/end): the weapon glow and the body glow go, and the stand-in rig of a mannequin character',
    '# (its clips end before the beat does; a beat that is cut - death, the selection space, a cutscene, the next beat - removes it).',
    `function ${M}/beat/wglow_off`, `function ${M}/beat/tint_off`,
    `execute if score @s plActive matches 1 run function ${M}/lite/stop`].join('\n'));
  return report;
}
