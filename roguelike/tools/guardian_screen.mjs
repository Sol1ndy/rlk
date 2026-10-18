// Screen-space overlays of the Corrupted Guardian's pull (P4, plan K21): diamond vignette closing -> white flash ->
// orange field with a 4-point star -> red diamond -> vignette reopening. Drawn as font glyphs shown with /title, so
// they sit on the camera in every view (first person, the F5 seat view whose camera is 3.5-6 b behind the seat,
// shoulder view) instead of world-space quads in front of the player's eyes (which only lined up in first person).
// Called by build_mboss_guardian_rig.mjs (--resourcepack); the frame texts go to the rig manifest (screen), where
// tools/mboss_guardian/api.py reads them for p34.py.
//
// RP output (owned, rewritten on every run):
//   assets/rlk/font/mboss_gd.json                     font rlk:mboss_gd: bitmap tiles U+E500.., 2 spaces U+E5F0..
//   assets/rlk/textures/font/mboss_gd/<frame>_<k>.png  256 x 144 tiles (4 per frame), flash.png 16 x 9
//
// The glyph engine (tile geometry, ref units, font writer, codepoint collision check) is the shared
// mboss_screen_lib.mjs; this file holds the Guardian's frames.
import {paintT, C, clamp, smooth, mix, star4in} from './guardian_paint_lib.mjs';
import {writeScreenFont, rgba, over, CLEAR} from './mboss_screen_lib.mjs';

export const SCREEN_FONT = 'rlk:mboss_gd';
const CP0 = 0xE500, CP_SPACE = 0xE5F0;    // free in every font of the pack (checked at build time)
const VIG = [1.95, 1.7, 1.48, 1.28, 1.1, 0.95];      // vignette aperture: vertical half-diagonal per frame (ref)
const ASPECT = 1.75;                      // aperture horizontal / vertical half-diagonal (16:9 screen)

// vignette: dark crimson outside a soft-edged diamond aperture (closing as k shrinks)
function vignette(k, x, y) {
  const d = Math.abs(x) / (k * ASPECT) + Math.abs(y) / k;           // 1 on the aperture edge
  const a = smooth(0.86, 1.08, d) * (0.5 + 0.34 * smooth(1.08, 1.9, d));
  return a <= 0.004 ? CLEAR : rgba(d > 1.5 ? '#6A0814' : '#820C19', a);
}
// 4-point star with a soft glow (white-gold), r = point length (ref)
function star(x, y, r) {
  const s = star4in(x, y, r, r, .12);
  const g = Math.exp(-(x * x + y * y) / (0.18 * r * r)) * 0.7;
  if (s > 0) return mix(rgba('#F6C86A', 1), rgba('#FFFBEA', 1), smooth(0, .55, s));
  return g < .01 ? CLEAR : rgba('#FFF2C8', g);
}
function diamond(x, y, cx, cy, s, rotDeg, colour, alpha) {
  const t = rotDeg * Math.PI / 180, dx = x - cx, dy = y - cy;
  const u = dx * Math.cos(t) + dy * Math.sin(t), v = -dx * Math.sin(t) + dy * Math.cos(t);
  const d = (Math.abs(u) + Math.abs(v)) / s;
  return d > 1 ? CLEAR : rgba(colour, alpha * smooth(1, .92, d));
}

// tiled frames (x right, y up, ref units)
const FRAMES = {
  ...Object.fromEntries(VIG.map((k, i) => [`vig${i}`, (x, y) => vignette(k, x, y)])),
  field: (x, y) => {
    let c = rgba('#EE8262', .82);
    for (const [px, py, s, a] of [[1.08, .56, .22, 22], [-1.17, -.43, .26, -28], [.87, -.65, .17, 35], [-.78, .69, .19, 14]]) {
      const d = diamond(x, y, px, py, s, a, '#FABF9F', .55);
      if (d[3]) c = over(d, c);
    }
    const st = star(x, y, .65);
    return st[3] ? over(st, c) : c;
  },
  diamond: (x, y) => {
    const d = diamond(x, y, 0, 0, .82, 0, '#B92C39', .78);
    const v = vignette(VIG[VIG.length - 1], x, y);
    return d[3] ? over(d, v) : v;
  },
};
// flat frames: one small glyph stretched over the same 256 x 144 units
const FLAT = {flash: ['#FFF4E2', .93]};

// Paint every frame, write the font; returns the manifest entry {font, frames: {name: title component}, ...}.
export function writeGuardianScreen(rp) {
  const r = writeScreenFont(rp, {name: 'mboss_gd', cp0: CP0, cpSpace: CP_SPACE, frames: FRAMES, flat: FLAT});
  return {font: SCREEN_FONT, frames: r.frames, vig: VIG.length, codepoints: r.codepoints, spaces: r.spaces,
    tile_px: r.tile_px, tile_units: r.tile_units, ref_units: r.ref_units};
}
