// Clip format, retiming and sampling shared by the mid-boss display-entity rigs (Corrupted Guardian,
// Moonlit Butterfly). Moved out of guardian_clips.mjs; each rig keeps its own CLIPS, DEFAULT_POSE and RETIME
// table and binds these functions to them.
//
// Clip: {name, len, loop?, next?, blend?, keys: [[tick, pose, ease?], ...], events, note}
//   keys are sparse; each merges onto the previous accumulated pose (the rig's default pose first).
//   ease of the segment arriving at a key: 'io' smooth (default), 'i' accelerate into the key
//   (strikes, falls), 'o' decelerate (leaps, settles), 'l' linear (spins, twirls).
//   events: ticks the pattern code schedules hits, hazards, props and sounds on.
//   blend: the first key segment lasts at least this many ticks (default 3) so a clip started
//   from any pose eases in.
// Pose channels: numbers lerp, 3-vectors lerp, 4-vectors (quaternions) slerp, strings switch at their key.
import {slerp as qSlerp, lerp as vLerp} from './mboss_rig_math.mjs';

// ---- retiming ---------------------------------------------------------------------------------------------------
// A retime maps a clip onto the played timeline with piecewise-linear knots [authored tick, played tick] from [0, 0]
// to [authored len, played len]. Keys and events are mapped and rounded to whole ticks (half up); the authored
// length and the knots stay on the clip (authoredLen, retime) for the manifest.
export function warp(knots, t) {
  for (let i = 1; i < knots.length; i++) {
    const [a0, b0] = knots[i - 1], [a1, b1] = knots[i];
    if (t <= a1) return b0 + (b1 - b0) * (t - a0) / (a1 - a0);
  }
  const [a, b] = knots[knots.length - 1];
  return b + (t - a);
}
export const warpTick = (knots, t) => Math.floor(warp(knots, t) + .5);
export function retime(clip, knots) {
  const [k0, kn] = [knots[0], knots[knots.length - 1]];
  if (k0[0] !== 0 || k0[1] !== 0 || kn[0] !== clip.len) throw new Error(`retime ${clip.name}: knots must run from [0, 0] to [${clip.len}, ...]`);
  for (let i = 1; i < knots.length; i++) {
    if (!(knots[i][0] > knots[i - 1][0] && knots[i][1] > knots[i - 1][1])) throw new Error(`retime ${clip.name}: knots not increasing`);
    if (knots[i][1] - knots[i - 1][1] > knots[i][0] - knots[i - 1][0]) throw new Error(`retime ${clip.name}: a knot segment slows the clip down`);
  }
  const keys = clip.keys.map(([t, p, e]) => [warpTick(knots, t), p, e]);
  keys.forEach(([t], i) => { if (i && t <= keys[i - 1][0]) throw new Error(`retime ${clip.name}: keys ${clip.keys[i - 1][0]} and ${clip.keys[i][0]} collide at ${t}`); });
  clip.keys = keys;
  clip.events = Object.fromEntries(Object.entries(clip.events || {}).map(([n, t]) => [n, warpTick(knots, t)]));
  clip.authoredLen = clip.len;
  clip.len = warpTick(knots, clip.len);
  clip.retime = knots;
}
// Applies a {clip name: knots} table to a clip list (unknown names throw).
export function applyRetime(clips, table) {
  for (const c of clips) if (table[c.name]) retime(c, table[c.name]);
  for (const n of Object.keys(table)) if (!clips.some(c => c.name === n)) throw new Error(`RETIME: unknown clip ${n}`);
}

// ---- sampling ---------------------------------------------------------------------------------------------------
export const EASE = {io: u => u * u * (3 - 2 * u), i: u => u * u, o: u => 1 - (1 - u) * (1 - u), l: u => u};
// Accumulated keys: every key's full pose (the defaults, then each sparse key merged on in order).
export function accumulate(clip, defaults) {
  let prev = structuredClone(defaults);
  return clip.keys.map(([tick, pose, ease]) => { prev = {...prev, ...structuredClone(pose)}; return {tick, p: prev, ease: ease || 'io'}; });
}
// Channel-wise blend of two full poses over the channels of `defaults`.
export function blendPose(a, b, u, defaults) {
  const o = {};
  for (const key of Object.keys(defaults)) {
    const x = a[key], y = b[key];
    if (typeof x === 'string') o[key] = u < 1 ? x : y;
    else if (typeof x === 'number') o[key] = x + (y - x) * u;
    else if (x.length === 4) o[key] = qSlerp(x, y, u);
    else o[key] = vLerp(x, y, u);
  }
  return o;
}
// Pose at tick t (fractional ticks allowed). opts: defaults (the default pose), discrete (channels that switch
// exactly at their key), phase(clip, t) (an extra cyclic channel `ph`, e.g. the drift of floating parts).
export function sampleClip(clip, t, ks, {defaults, discrete = [], phase = () => 0}) {
  const ph = phase(clip, Math.max(0, t));
  if (t <= ks[0].tick) return {...ks[0].p, ph};
  for (let i = 1; i < ks.length; i++) if (t <= ks[i].tick) {
    const a = ks[i - 1], b = ks[i], u = (t - a.tick) / Math.max(1e-9, b.tick - a.tick);
    const p = blendPose(a.p, b.p, EASE[b.ease](u), defaults);
    for (const key of discrete) p[key] = t >= b.tick ? b.p[key] : a.p[key];
    return {...p, ph};
  }
  return {...ks[ks.length - 1].p, ph};
}
