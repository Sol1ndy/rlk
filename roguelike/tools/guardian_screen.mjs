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
// Geometry (vanilla Gui.renderTitle: translate to the screen centre, scale 4, text at y = -10, x = -width / 2). A
// bitmap glyph of height H and ascent A is drawn from y = -10 + 7 - A, its advance is round(px width x H / px
// height) + 1. A frame is 2 x 2 tiles of 256 x 144 px drawn at 128 x 72 title units each (H 72, scale 0.5):
// top row A 69 (y -72..0), bottom row A -3 (y 0..72); the 1-unit gap of every advance is taken back with a -1
// space and the second row starts with a -(2 x 128 + 1) space, so the four tiles meet exactly and the whole text
// is 256 units wide (x -128..128). The overlay spans 1024 x 576 GUI px: the whole screen at every GUI scale >= 2
// on 1080p (and at the automatic scale of every common screen). Frames are painted in "ref units": 1 ref = 32
// title units = half the screen height at the automatic GUI scale of a 1080p screen (4). A texel is 2 GUI px.
// Text shadow off (shadow_color 0 in the title component); the text shader drops pixels under 10 % alpha.
import fs from 'node:fs';
import path from 'node:path';
import {png} from './weapon_paint.mjs';
import {paintT, C, clamp, smooth, mix, star4in} from './guardian_paint_lib.mjs';

export const SCREEN_FONT = 'rlk:mboss_gd';
const TW = 256, TH = 144;                 // tile, px
const GH = 72;                            // tile glyph height, title units (scale 0.5)
const UNIT = GH / TH;                     // title units per px
const REF = 32;                           // title units per ref unit
const XR = TW * UNIT / REF, YR = TH * UNIT / REF;   // half extent of the frame in ref units (4 x 2.25)
const CP0 = 0xE500, CP_SPACE = 0xE5F0;    // free in every font of the pack (checked at build time)
const VIG = [1.95, 1.7, 1.48, 1.28, 1.1, 0.95];      // vignette aperture: vertical half-diagonal per frame (ref)
const ASPECT = 1.75;                      // aperture horizontal / vertical half-diagonal (16:9 screen)

const rgba = (h, a) => { const c = C(h); return [c[0], c[1], c[2], Math.round(clamp(a) * 255)]; };
const over = (top, bot) => {               // straight-alpha "over"
  const ta = top[3] / 255, ba = bot[3] / 255, oa = ta + ba * (1 - ta);
  if (oa <= 0) return [0, 0, 0, 0];
  return [0, 1, 2].map(i => (top[i] * ta + bot[i] * ba * (1 - ta)) / oa).concat([oa * 255]);
};
const CLEAR = [0, 0, 0, 0];

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

const esc = cp => '\\u' + cp.toString(16);
const component = text => `[{"text":"${text}","font":"${SCREEN_FONT}","color":"white","shadow_color":0}]`;

// Codepoints already used by other fonts of the resource pack (they must not collide with ours).
function usedElsewhere(rp, own) {
  const used = new Map();
  for (const ns of fs.existsSync(path.join(rp, 'assets')) ? fs.readdirSync(path.join(rp, 'assets')) : []) {
    const dir = path.join(rp, 'assets', ns, 'font');
    if (!fs.existsSync(dir)) continue;
    for (const f of fs.readdirSync(dir)) {
      if (!f.endsWith('.json') || path.join(dir, f) === own) continue;
      const font = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
      for (const p of font.providers || []) {
        for (const row of p.chars || []) for (const ch of row) used.set(ch.codePointAt(0), `${ns}:${f}`);
        for (const ch of Object.keys(p.advances || {})) used.set(ch.codePointAt(0), `${ns}:${f}`);
      }
    }
  }
  return used;
}

// Paint every frame, write the font; returns the manifest entry {font, frames: {name: title component}, ...}.
export function writeGuardianScreen(rp) {
  const tex = path.join(rp, 'assets/rlk/textures/font/mboss_gd');
  const fontPath = path.join(rp, 'assets/rlk/font/mboss_gd.json');
  fs.rmSync(tex, {recursive: true, force: true});
  fs.mkdirSync(tex, {recursive: true});
  const providers = [], frames = {}, cps = [];
  let cp = CP0;
  const back1 = String.fromCodePoint(CP_SPACE), backRow = String.fromCodePoint(CP_SPACE + 1);
  const tileW = Math.round(TW * UNIT);                       // 128 units
  Object.entries(FRAMES).forEach(([name, fn]) => {
    const W = 2 * TW, H = 2 * TH;
    const buf = paintT(W, H, (u, v) => fn((u - .5) * 2 * XR, (.5 - v) * 2 * YR), 2);
    const chars = [];
    for (const [r, c] of [[0, 0], [0, 1], [1, 0], [1, 1]]) {
      const t = Buffer.alloc(TW * TH * 4);
      for (let y = 0; y < TH; y++) buf.copy(t, y * TW * 4, ((r * TH + y) * W + c * TW) * 4, ((r * TH + y) * W + c * TW + TW) * 4);
      // keep the full advance: vanilla measures a glyph to its rightmost non-transparent column (alpha 1/255 is
      // below the text shader's cut, so it never shows)
      if (t[(TW - 1) * 4 + 3] === 0) t[(TW - 1) * 4 + 3] = 1;
      const file = `${name}_${r}${c}`;
      fs.writeFileSync(path.join(tex, file + '.png'), png(TW, TH, t));
      providers.push({type: 'bitmap', file: `rlk:font/mboss_gd/${file}.png`, ascent: r === 0 ? GH - 3 : -3, height: GH,
        chars: [String.fromCodePoint(cp)]});
      chars.push(cp);
      cps.push(cp++);
    }
    // TL, TR, back to the left edge, BL, BR; every advance's 1-unit gap taken back
    frames[name] = component([esc(chars[0]), esc(CP_SPACE), esc(chars[1]), esc(CP_SPACE + 1), esc(chars[2]), esc(CP_SPACE),
      esc(chars[3]), esc(CP_SPACE)].join(''));
  });
  for (const [name, [hexc, a]] of Object.entries(FLAT)) {
    const w = 16, h = 9, t = Buffer.alloc(w * h * 4), c = rgba(hexc, a);
    for (let i = 0; i < w * h; i++) t.set(c, i * 4);
    fs.writeFileSync(path.join(tex, name + '.png'), png(w, h, t));
    providers.push({type: 'bitmap', file: `rlk:font/mboss_gd/${name}.png`, ascent: GH - 3, height: 2 * GH, chars: [String.fromCodePoint(cp)]});
    frames[name] = component(esc(cp) + esc(CP_SPACE));
    cps.push(cp++);
  }
  assert(cp < CP_SPACE, 'too many screen glyphs');
  providers.push({type: 'space', advances: {[back1]: -1, [backRow]: -(2 * tileW + 1)}});
  cps.push(CP_SPACE, CP_SPACE + 1);
  const clash = usedElsewhere(rp, fontPath);
  const hit = cps.filter(x => clash.has(x));
  if (hit.length) throw new Error(`screen glyphs collide with ${hit.map(x => esc(x) + ' (' + clash.get(x) + ')').join(', ')}`);
  fs.mkdirSync(path.dirname(fontPath), {recursive: true});
  fs.writeFileSync(fontPath, JSON.stringify({providers}, null, 1) + '\n');
  return {font: SCREEN_FONT, frames, vig: VIG.length, codepoints: [esc(CP0), esc(cp - 1)], spaces: [esc(CP_SPACE), esc(CP_SPACE + 1)],
    tile_px: [TW, TH], tile_units: [tileW, GH], ref_units: REF};
}
function assert(ok, msg) { if (!ok) throw new Error(msg); }
