// Painted sprites of the 아펩의 오아시스 파수꾼 rig: a thin aggregator over the shared tiles (apep_materials.mjs) and the region
// sprites (apep_{head,body,limbs,hands,tail}.mjs sprites()), used by build_mboss_apep_rig.mjs. Written to
// assets/rlk/textures/mboss/apep/<name>.png and merged into the item atlas. Budget (plan R13): <= 0.9 M atlas px for the
// rig with both looks; sides multiples of 16 and <= 512; grey sprites tinted per form share one texture (the ledger's
// use: "tinted").
import {paintSpriteSet} from './mboss_paint_lib.mjs';
import {tileSprites} from './apep_materials.mjs';
import {REGIONS} from './apep_geometry.mjs';

export const spriteId = name => 'rlk:mboss/apep/' + name;
export const ATLAS_BUDGET = 900000;
// {name: record {w, h, ppb, fn, translucent, forms, region, use}}
export function apepSprites() {
  const out = {...tileSprites()};
  for (const r of REGIONS) for (const [k, v] of Object.entries(r.sprites())) {
    if (k in out) throw new Error(`sprite ${k} defined twice (region ${r.REGION})`);
    out[k] = {...v, region: v.region || r.REGION};
  }
  return out;
}
export function paintApepTextures(rp, only = null) {
  const set = Object.fromEntries(Object.entries(apepSprites()).map(([k, v]) => [k, [v.w, v.h, v.fn, v.translucent]]));
  return paintSpriteSet(rp, 'assets/rlk/textures/mboss/apep', set, spriteId, only);
}
