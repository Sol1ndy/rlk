// Part models of the 야타용왕 (Azhdaha) rig: a thin aggregator over the four region modules
// azhdaha_{head,body,legs,tail}.mjs (each owns its parts' geometry, sprites and element looks; plan.md R9), used by
// build_mboss_azhdaha_rig.mjs. Shape helpers: azhdaha_shape.mjs; shared materials: azhdaha_materials.mjs.
//
// Authoring frame ("A-frame", the rig's frame): +X = the boss's LEFT, +Y up, -Z forward; geometry is authored in blocks
// in each part's joint frame and converted to model units for the part's display scale (azhdaha_pose.mjs PART_SCALE).
// Constraints kept by every model: coordinates within -16..32 (checkBounds: reach 1.5 x scale blocks from the joint),
// single-axis element rotations in 22.5 degree steps within +-45.
import * as head from './azhdaha_head.mjs';
import * as body from './azhdaha_body.mjs';
import * as legs from './azhdaha_legs.mjs';
import * as tail from './azhdaha_tail.mjs';
import {checkBounds} from './mboss_model_lib.mjs';

export {checkBounds};
export const REGIONS = [head, body, legs, tail];
export const EMPTY = 'empty';
const merge = (what, get) => {
  const out = {};
  for (const r of REGIONS) for (const [k, v] of Object.entries(get(r) || {})) {
    if (k in out) throw new Error(`${what} ${k} defined twice (region ${r.REGION})`);
    out[k] = v;
  }
  return out;
};
// [part, default item model, block brightness, region] in UUID order (head, body, legs, tail)
export const PARTS = REGIONS.flatMap(r => r.PARTS.map(([n, m, b]) => [n, m, b, r.REGION]));
export const partModels = () => ({[EMPTY]: [], ...merge('model', r => r.models())});
// Element looks per channel: legs (geo / hydro / pyro: fore bracers + paws, hind gaiters + feet, apron, belly cracks)
// and tail (geo / cryo / electro: the four plate groups and the tail chain); {channel: {part: {look: item}}}.
export const LOOKS = {legs: merge('legs look of', r => r.LOOKS && r.LOOKS.legs), tail: merge('tail look of', r => r.LOOKS && r.LOOKS.tail)};
// Item definitions that tint a model (the glow overlays): {item: [model, rgb int]}.
export const TINTED = merge('tinted item', r => r.TINTED);
// Brightness per look: {channel: {look: {part: level}}} (parts not listed keep their PARTS level).
export const LOOK_BRIGHT = {legs: {}, tail: {}};
for (const r of REGIONS) for (const [ch, looks] of Object.entries(r.LOOK_BRIGHT || {})) for (const [l, parts] of Object.entries(looks)) LOOK_BRIGHT[ch][l] = {...(LOOK_BRIGHT[ch][l] || {}), ...parts};
export const REGION_OF = Object.fromEntries(PARTS.map(([n, , , r]) => [n, r]));
