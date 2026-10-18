// Painted sprites of the 야타용왕 (Azhdaha) rig: a thin aggregator over the shared material tiles
// (azhdaha_materials.mjs) and the region sprites (azhdaha_{head,body,legs,tail}.mjs sprites()), used by
// build_mboss_azhdaha_rig.mjs. Written to assets/rlk/textures/mboss/azhdaha/<name>.png and merged into the item atlas.
// Budget (plan.md R8): <= 1.2 M atlas px for the rig, sides multiples of 16 and <= 512.
import {paintSpriteSet} from './mboss_paint_lib.mjs';
import {tileSprites} from './azhdaha_materials.mjs';
import {REGIONS} from './azhdaha_geometry.mjs';

export const spriteId = name => 'rlk:mboss/azhdaha/' + name;
export const ATLAS_BUDGET = 1.2e6;
// {name: [w, h, painter (s, t in 0..1) -> rgba, translucent]}
export function azhdahaSprites() {
  const out = {...tileSprites()};
  for (const r of REGIONS) for (const [k, v] of Object.entries(r.sprites())) {
    if (k in out) throw new Error(`sprite ${k} defined twice (region ${r.REGION})`);
    out[k] = v;
  }
  return out;
}
// {name: [w, h]} without painting
export const azhdahaSpriteSizes = () => Object.fromEntries(Object.entries(azhdahaSprites()).map(([k, [w, h]]) => [k, [w, h]]));
export function paintAzhdahaTextures(rp, only = null) {
  return paintSpriteSet(rp, 'assets/rlk/textures/mboss/azhdaha', azhdahaSprites(), spriteId, only);
}
