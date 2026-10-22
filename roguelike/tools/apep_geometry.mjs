// Part models of the 아펩의 오아시스 파수꾼 rig: a thin aggregator over the five region modules apep_{head,body,limbs,hands,tail}.mjs
// (plan R19: each region owns its parts' geometry, sprites and looks; one refiner per region in AP-R2), used by
// build_mboss_apep_rig.mjs. Shape helpers: mboss_shape_lib.mjs; shared materials and tint slots: apep_materials.mjs.
//
// Authoring frame ("A-frame", the rig's frame): +X = the boss's LEFT, +Y up, -Z forward; geometry in blocks about each
// part's joint, in the part's per-form authoring frame (apep_pose.mjs FRAMES), converted to model units for the part's
// display scale. Constraints kept by every model: coordinates within -16..32 (checkBounds: reach 1.5 x scale blocks
// per axis), single-axis element rotations in 22.5 degree steps within +-45, a tint slot on every face.
import * as head from './apep_head.mjs';
import * as body from './apep_body.mjs';
import * as limbs from './apep_limbs.mjs';
import * as hands from './apep_hands.mjs';
import * as tail from './apep_tail.mjs';
import {checkBounds} from './mboss_model_lib.mjs';
import {PART_NAMES, PART_REGION} from './apep_pose.mjs';

export {checkBounds};
export const REGIONS = [head, body, limbs, hands, tail];
export const EMPTY = 'empty';
const merge = (what, get) => {
  const out = {};
  for (const r of REGIONS) for (const [k, v] of Object.entries(get(r) || {})) {
    if (k in out) throw new Error(`${what} ${k} defined twice (region ${r.REGION})`);
    out[k] = v;
  }
  return out;
};
// every part belongs to exactly one region, as apep_pose PART_ROWS says
for (const r of REGIONS) for (const p of r.PARTS) if (PART_REGION[p] !== r.REGION) throw new Error(`part ${p}: region ${r.REGION} != ${PART_REGION[p]}`);
const listed = REGIONS.flatMap(r => r.PARTS);
for (const p of PART_NAMES) if (!listed.includes(p)) throw new Error(`part ${p} has no region module`);
export const partModels = () => ({[EMPTY]: [], ...merge('model', r => r.models())});
// the form look (form channel): {part: {p1: model, p3: model}} for every part but the hands, the face and the core
export const FORM_MODELS = merge('form model of', r => r.FORM_MODELS && Object.fromEntries(Object.entries(r.FORM_MODELS).filter(([p]) => !hands.PARTS.includes(p))));
// the hands (R8): {part: {variant: model}}
export const HAND_VARIANTS = Object.fromEntries(hands.PARTS.map(p => [p, Object.fromEntries(hands.VARIANTS[p[0]].map(v => [v, `${p}_${v}`]))]));
// the face look (item records: model + form + face colour) and the core look
export const FACE_ITEMS = head.FACE_ITEMS;
export const CORE_MODELS = body.CORE_MODELS;
export const REGION_OF = PART_REGION;
