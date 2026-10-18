// Screen-space overlay engine shared by the mid-boss rigs: full-screen frames drawn as title-font glyphs, so they
// sit on the camera in every view (first person, the F5 seat view, shoulder view). Moved out of guardian_screen.mjs;
// a rig supplies its font id, texture directory, codepoint block and frame painters.
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
import {paintT, C, clamp} from './mboss_paint_lib.mjs';

export const TW = 256, TH = 144;                 // tile, px
export const GH = 72;                            // tile glyph height, title units (scale 0.5)
export const UNIT = GH / TH;                     // title units per px
export const REF = 32;                           // title units per ref unit
export const XR = TW * UNIT / REF, YR = TH * UNIT / REF;   // half extent of the frame in ref units (4 x 2.25)

export const rgba = (h, a) => { const c = C(h); return [c[0], c[1], c[2], Math.round(clamp(a) * 255)]; };
export const over = (top, bot) => {               // straight-alpha "over"
  const ta = top[3] / 255, ba = bot[3] / 255, oa = ta + ba * (1 - ta);
  if (oa <= 0) return [0, 0, 0, 0];
  return [0, 1, 2].map(i => (top[i] * ta + bot[i] * ba * (1 - ta)) / oa).concat([oa * 255]);
};
export const CLEAR = [0, 0, 0, 0];
const esc = cp => '\\u' + cp.toString(16);

// Codepoints already used by other fonts of the resource pack (they must not collide with ours).
export function usedElsewhere(rp, own) {
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

// Paint every frame and write the font rlk:<name> (assets/rlk/font/<name>.json, textures/font/<name>/*); returns
// the manifest entry {font, frames: {name: title component}, ...}.
//   frames: {name: (x, y) -> rgba} tiled frames in ref units (x right, y up); flat: {name: [hex, alpha]} one small
//   glyph stretched over the same 256 x 144 units; cp0 / cpSpace: the glyph block and its two spaces.
export function writeScreenFont(rp, {name, cp0, cpSpace, frames: FRAMES, flat: FLAT = {}}) {
  const font = `rlk:${name}`;
  const component = text => `[{"text":"${text}","font":"${font}","color":"white","shadow_color":0}]`;
  const tex = path.join(rp, `assets/rlk/textures/font/${name}`);
  const fontPath = path.join(rp, `assets/rlk/font/${name}.json`);
  fs.rmSync(tex, {recursive: true, force: true});
  fs.mkdirSync(tex, {recursive: true});
  const providers = [], frames = {}, cps = [];
  let cp = cp0;
  const back1 = String.fromCodePoint(cpSpace), backRow = String.fromCodePoint(cpSpace + 1);
  const tileW = Math.round(TW * UNIT);                       // 128 units
  Object.entries(FRAMES).forEach(([fname, fn]) => {
    const W = 2 * TW, H = 2 * TH;
    const buf = paintT(W, H, (u, v) => fn((u - .5) * 2 * XR, (.5 - v) * 2 * YR), 2);
    const chars = [];
    for (const [r, c] of [[0, 0], [0, 1], [1, 0], [1, 1]]) {
      const t = Buffer.alloc(TW * TH * 4);
      for (let y = 0; y < TH; y++) buf.copy(t, y * TW * 4, ((r * TH + y) * W + c * TW) * 4, ((r * TH + y) * W + c * TW + TW) * 4);
      // keep the full advance: vanilla measures a glyph to its rightmost non-transparent column (alpha 1/255 is
      // below the text shader's cut, so it never shows)
      if (t[(TW - 1) * 4 + 3] === 0) t[(TW - 1) * 4 + 3] = 1;
      const file = `${fname}_${r}${c}`;
      fs.writeFileSync(path.join(tex, file + '.png'), png(TW, TH, t));
      providers.push({type: 'bitmap', file: `rlk:font/${name}/${file}.png`, ascent: r === 0 ? GH - 3 : -3, height: GH,
        chars: [String.fromCodePoint(cp)]});
      chars.push(cp);
      cps.push(cp++);
    }
    // TL, TR, back to the left edge, BL, BR; every advance's 1-unit gap taken back
    frames[fname] = component([esc(chars[0]), esc(cpSpace), esc(chars[1]), esc(cpSpace + 1), esc(chars[2]), esc(cpSpace),
      esc(chars[3]), esc(cpSpace)].join(''));
  });
  for (const [fname, [hexc, a]] of Object.entries(FLAT)) {
    const w = 16, h = 9, t = Buffer.alloc(w * h * 4), c = rgba(hexc, a);
    for (let i = 0; i < w * h; i++) t.set(c, i * 4);
    fs.writeFileSync(path.join(tex, fname + '.png'), png(w, h, t));
    providers.push({type: 'bitmap', file: `rlk:font/${name}/${fname}.png`, ascent: GH - 3, height: 2 * GH, chars: [String.fromCodePoint(cp)]});
    frames[fname] = component(esc(cp) + esc(cpSpace));
    cps.push(cp++);
  }
  if (!(cp < cpSpace)) throw new Error('too many screen glyphs');
  providers.push({type: 'space', advances: {[back1]: -1, [backRow]: -(2 * tileW + 1)}});
  cps.push(cpSpace, cpSpace + 1);
  const clash = usedElsewhere(rp, fontPath);
  const hit = cps.filter(x => clash.has(x));
  if (hit.length) throw new Error(`screen glyphs collide with ${hit.map(x => esc(x) + ' (' + clash.get(x) + ')').join(', ')}`);
  fs.mkdirSync(path.dirname(fontPath), {recursive: true});
  fs.writeFileSync(fontPath, JSON.stringify({providers}, null, 1) + '\n');
  return {font, frames, codepoints: [esc(cp0), esc(cp - 1)], spaces: [esc(cpSpace), esc(cpSpace + 1)],
    tile_px: [TW, TH], tile_units: [tileW, GH], ref_units: REF};
}
