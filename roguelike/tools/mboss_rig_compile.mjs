// Clip compiler shared by the mid-boss display-entity rigs (Corrupted Guardian, Moonlit Butterfly). Moved out of
// build_mboss_guardian_rig.mjs; each rig generator supplies its parts, its pose sampler and its names.
//
// Runtime model: the anchor (the boss body) runs rig/tick each tick; the parts follow its position and yaw, and the
// current clip applies its keys. Clips are compiled per part into interpolation segments: at tick a a part
// receives the pose of tick b with interpolation_duration b-a, where b is the furthest tick whose in-between poses
// the client's lerp/slerp reproduces within tolerance (spins, arcs and fast strikes get a key every tick; holds get
// one key). Dispatch is two binary trees (clip id, then key tick), with no macros on the hot path.
//
// createRigCompiler(cfg) -> {nbt, segments, stepViolations, compileClip, writeDispatch, writeFace}
//   cfg.ns        function namespace of the rig, e.g. 'rlk:mboss/guardian/rig'
//   cfg.obj       objective prefix ('gdRig': gdRigC clip id, gdRigT clip tick, gdRigY face scratch)
//   cfg.fn        (name, lines) writer of a function file below the rig directory
//   cfg.parts     part names in UUID order; cfg.uuidOf(part) -> UUID string
//   cfg.tol       {t, s, r: {part: degrees}, rDefault}: client-interpolation tolerances (display space)
//   cfg.skipStep  part -> true for parts the rotation checks skip (afterimages that follow another part)
//   cfg.modelOf   {channel: [part, {value: model}]}: discrete pose channels that swap a part's item model
//   cfg.swapLine  (part, model) -> the item-model swap command
//   cfg.debug     optional {put(name, lines), dir}: exact per-tick poses <dir>/<clip>/<t> for the offline renderer
import {slerp, lerp, qAngle, len, sub} from './mboss_rig_math.mjs';

// Per-tick rotation check: no part may turn more than maxStep degrees between two ticks (the client slerps each
// step the short way; near 180 degrees that path is undefined and a twist or an IK flip shows as a pop through the
// body). A segment never spans more than maxSeg degrees of rotation: near 180 degrees the client's shortest-path
// slerp has no stable direction (the sign of a cosine of about 1e-9 decides it), so spins get a key every tick. The
// fit is checked on the values as written (5 decimals). A segment that still turns more than this (a 1-tick step,
// or the forced blend-in) fails the build. Large 1-tick steps are also checked at the half tick: where the client's
// slerp leaves the authored path by more than subTol degrees (an elbow passing through the body) it warns.
export const shown = v => v.s.some(x => Math.abs(x) > 1e-4);
export const r5 = x => (Math.abs(x) < 5e-7 ? 0 : +x.toFixed(5));
export const written = v => ({t: v.t.map(r5), q: v.q.map(r5), s: v.s.map(r5)});
export const f6 = x => (Math.abs(x) < 5e-7 ? 0 : x).toFixed(5).replace(/\.?0+$/, '') + 'f';
export const arr = a => '[' + a.map(f6).join(',') + ']';
export const nbt = v => `{translation:${arr(v.t)},left_rotation:${arr(v.q)},scale:${arr(v.s)},right_rotation:[0f,0f,0f,1f]}`;
export function interp(a, b, u) { return {t: lerp(a.t, b.t, u), q: slerp(a.q, b.q, u), s: lerp(a.s, b.s, u)}; }

export function createRigCompiler({ns, obj, fn, parts, uuidOf, tol, skipStep = () => false, modelOf = {}, swapLine, debug = null,
  maxStepDeg = 120, maxSegDeg = 120, subTol = 35}) {
  function close(x, y, n) {
    const big = Math.max(...y.s.map(Math.abs), ...x.s.map(Math.abs));
    if (big < 1e-4) return true;           // hidden both ways
    if (len(sub(x.t, y.t)) > tol.t) return false;
    if (Math.max(...x.s.map((v, i) => Math.abs(v - y.s[i]))) > tol.s * Math.max(1, big)) return false;
    return qAngle(x.q, y.q) <= (tol.r[n] ?? tol.rDefault);
  }
  function segments(raw, n, minFirst) {
    const seq = raw.map(written), L = seq.length - 1, out = [];
    let a = 0;
    while (a < L) {
      let b = a + 1;
      const fits = bb => {
        if (qAngle(seq[a].q, seq[bb].q) > maxSegDeg - 2) return false;
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
  function stepViolations(clip, frames) {
    const out = [];
    for (const n of parts) {
      if (skipStep(n)) continue;
      for (let t = 1; t < frames.length; t++) {
        const a = frames[t - 1].d[n], b = frames[t].d[n];
        if (!shown(a) || !shown(b)) continue;
        const ang = qAngle(a.q, b.q);
        if (ang > maxStepDeg) out.push(`${clip.name} ${n} t${t - 1}->${t}: ${ang.toFixed(0)} degrees`);
      }
    }
    return out;
  }
  // One clip: key files c/<clip>/k/<t>, its runner c/<clip>/run (+ b/ subtrees), play/<clip> and start/<clip>.
  // frames[t] = {d: {part: display transform}, p: sampled pose}; halfFrame(a) = the frame at tick a + 0.5;
  // extraLines(t) (optional) = further commands for tick t (after the keys and model swaps), e.g. state switches.
  // Returns {info (manifest entry), motionErrors, warns}.
  function compileClip(c, frames, halfFrame, extraLines = null) {
    const motionErrors = stepViolations(c, frames), warns = [];
    const byTick = new Map();
    const add = (t, line) => { if (!byTick.has(t)) byTick.set(t, []); byTick.get(t).push(line); };
    let keyCount = 0;
    for (const n of parts) {
      const seq = frames.map(f => f.d[n]);
      for (const [a, b] of segments(seq, n, c.blend ?? 3)) {
        const turn = qAngle(seq[a].q, seq[b].q);
        if (turn > maxSegDeg && shown(seq[b]) && shown(seq[a]) && !skipStep(n))
          motionErrors.push(`${c.name} ${n} t${a}-${b}: ${turn.toFixed(0)} degree key (ambiguous slerp)`);
        if (b - a === 1 && turn > 45 && shown(seq[a]) && shown(seq[b])) {
          const mid = halfFrame(a).d[n];
          const dev = qAngle(slerp(seq[a].q, seq[b].q, .5), mid.q);
          if (dev > subTol) warns.push(`${c.name} ${n} t${a}-${b}: the client path leaves the authored one by ${dev.toFixed(0)} degrees at the half tick`);
        }
        add(a, `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:${b - a},transformation:${nbt(seq[b])}}`);
        keyCount++;
      }
    }
    for (const [ch, [part, map]] of Object.entries(modelOf)) {
      frames.forEach((f, t) => { if (t === 0 || f.p[ch] !== frames[t - 1].p[ch]) add(t, swapLine(part, map[f.p[ch]])); });
    }
    if (extraLines) frames.forEach((f, t) => { for (const line of extraLines(t) || []) add(t, line); });
    if (debug) frames.forEach((f, t) => debug.put(`${debug.dir}/${c.name}/${t}`, [...parts.map(n => `data merge entity ${uuidOf(n)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(f.d[n])}}`),
      ...Object.entries(modelOf).map(([ch, [part, map]]) => swapLine(part, map[f.p[ch]]))]));
    const ticks = [...byTick.keys()].sort((x, y) => x - y);
    for (const t of ticks) fn(`c/${c.name}/k/${t}`, byTick.get(t));
    // per-clip runner: wrap / chain / hold, then a binary dispatch over the key ticks
    const head = [`# ${c.name}: ${c.len} t${c.loop ? ', loop' : c.next ? `, then ${c.next}` : ', holds the last pose'}. @s = rig anchor.`];
    if (c.loop) head.push(`execute if score @s ${obj}T matches ${c.len}.. run scoreboard players set @s ${obj}T 0`);
    else if (c.next) head.push(`execute if score @s ${obj}T matches ${c.len}.. run return run function ${ns}/start/${c.next}`);
    else head.push(`execute if score @s ${obj}T matches ${c.len + 1}.. run return run scoreboard players set @s ${obj}T ${c.len + 1}`);
    const tree = list => {
      if (list.length <= 6) return list.map(t => `execute if score @s ${obj}T matches ${t} run return run function ${ns}/c/${c.name}/k/${t}`);
      const mid = list[Math.floor(list.length / 2) - 1];
      const L = list.filter(t => t <= mid), R = list.filter(t => t > mid);
      fn(`c/${c.name}/b/${L[0]}_${L[L.length - 1]}`, tree(L));
      fn(`c/${c.name}/b/${R[0]}_${R[R.length - 1]}`, tree(R));
      return [`execute if score @s ${obj}T matches ..${mid} run return run function ${ns}/c/${c.name}/b/${L[0]}_${L[L.length - 1]}`,
        `function ${ns}/c/${c.name}/b/${R[0]}_${R[R.length - 1]}`];
    };
    fn(`c/${c.name}/run`, [...head, ...tree(ticks)]);
    fn(`play/${c.name}`, [`# Play clip ${c.name} (${c.len} t) from its tick 0 at the next rig/tick (the same game tick when rig/tick runs later). @s = rig anchor.`, `scoreboard players set @s ${obj}C ${c.id}`, `scoreboard players set @s ${obj}T -1`]);
    fn(`start/${c.name}`, [`# Internal: chain into ${c.name} now (tick 0 applied immediately). @s = rig anchor.`, `scoreboard players set @s ${obj}C ${c.id}`, `scoreboard players set @s ${obj}T 0`, `function ${ns}/c/${c.name}/k/0`]);
    const info = {id: c.id, name: c.name, len: c.len, loop: !!c.loop, next: c.next || null, events: c.events || {}, keyFiles: ticks.length, keys: keyCount, note: c.note || '',
      ...(c.retime ? {authoredLen: c.authoredLen, retime: c.retime} : {})};
    return {info, motionErrors, warns};
  }
  // Global dispatch on the clip id: run -> d/<lo>_<hi> subtrees -> c/<clip>/run.
  function writeDispatch(clips) {
    const ids = clips.map(c => c.id);
    const tree = list => {
      if (list.length <= 6) return list.map(i => `execute if score @s ${obj}C matches ${i} run return run function ${ns}/c/${clips[i].name}/run`);
      const mid = list[Math.floor(list.length / 2) - 1], L = list.filter(i => i <= mid), R = list.filter(i => i > mid);
      fn(`d/${L[0]}_${L[L.length - 1]}`, tree(L)); fn(`d/${R[0]}_${R[R.length - 1]}`, tree(R));
      return [`execute if score @s ${obj}C matches ..${mid} run return run function ${ns}/d/${L[0]}_${L[L.length - 1]}`, `function ${ns}/d/${R[0]}_${R[R.length - 1]}`];
    };
    fn('run', ['# Current clip -> its runner. @s = rig anchor.', ...tree(ids)]);
  }
  // Facing helpers (the parts take the anchor's yaw every tick): face/player, face/track (at most maxDeg per
  // call, both yaws normalised into [-180, 180) first), face/set {yaw}. marker = the temporary marker's tag.
  function writeFace({marker, maxDeg = 12}) {
    const Y = `${obj}Y`, cap = Math.round(maxDeg * 100);
    fn('face/player', ['# Turn the anchor to face the nearest player (yaw only). @s = rig anchor.',
      'execute facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0']);
    fn('face/track', [`# Turn the anchor toward the nearest player by at most ${maxDeg} degrees per call. @s = rig anchor.`,
      '# Both yaws are normalised into [-180, 180) first, so the stored yaw never drifts past one turn.',
      `scoreboard players set #c36000 ${Y} 36000`,
      `execute store result score #yaw ${Y} run data get entity @s Rotation[0] 100`,
      `scoreboard players add #yaw ${Y} 18000`,
      `scoreboard players operation #yaw ${Y} %= #c36000 ${Y}`,
      `execute if score #yaw ${Y} matches ..-1 run scoreboard players add #yaw ${Y} 36000`,
      `scoreboard players remove #yaw ${Y} 18000`,
      `execute facing entity @p[gamemode=!spectator] feet run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_aux","${marker}"]}`,
      `execute as @e[type=marker,tag=${marker},limit=1] at @s facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0`,
      `execute store result score #yawT ${Y} run data get entity @e[type=marker,tag=${marker},limit=1] Rotation[0] 100`,
      `kill @e[type=marker,tag=${marker}]`,
      `scoreboard players operation #yawT ${Y} -= #yaw ${Y}`,
      `execute if score #yawT ${Y} matches 18000.. run scoreboard players remove #yawT ${Y} 36000`,
      `execute if score #yawT ${Y} matches ..-18001 run scoreboard players add #yawT ${Y} 36000`,
      `execute if score #yawT ${Y} matches ${cap + 1}.. run scoreboard players set #yawT ${Y} ${cap}`,
      `execute if score #yawT ${Y} matches ..-${cap + 1} run scoreboard players set #yawT ${Y} -${cap}`,
      `scoreboard players operation #yaw ${Y} += #yawT ${Y}`,
      `execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw ${Y}`]);
    fn('face/set', [`# Set the anchor yaw: function ${ns}/face/set {yaw:<degrees>}. @s = rig anchor.`, '$rotate @s $(yaw) 0']);
  }
  return {close, segments, stepViolations, compileClip, writeDispatch, writeFace};
}
