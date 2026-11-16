// Sprites of the 아를레키노 (Arlecchino) rig (S:ar/PLAN.md §2.2): the P1 crimson feather-wing segments (v1 36.6-39.6,
// ref/p1_C_wing.jpg: blade-like crimson feathers on a dark spine), the P2 crimson blade-leg segments (v4 20.8-21.2,
// ref/model_p2_closeup.jpg: dark crimson chitin with a glowing scarlet edge and spikes), the intro's teacup and saucer
// (white porcelain, gold rim). The P2 skin is not painted: build_arlecchino_rig.mjs writes the embedded skin_33 bytes.
//
// Card layout (arlecchino_geometry.mjs SEG): a segment hangs from its pivot at the top of the sprite; the pivot line sits at
// u = 0.8 (wings) / 0.6 (legs) on both card faces, the feathers / the blade body spread toward u = 0, the tip at v = 1.
import {hex, clamp, mix, fbm, TRANSPARENT, paintSpriteSet} from './mboss_paint_lib.mjs';
import {SPRITES, SEG} from './arlecchino_geometry.mjs';

export const spriteId = n => `rlk:mboss/arlecchino/${n}`;
export const TEX_DIR = 'assets/rlk/textures/mboss/arlecchino';
const T = TRANSPARENT;
const C = {black: hex('#14030a'), dark: hex('#3a0712'), deep: hex('#6e0d1c'), crim: hex('#c21a2e'), red: hex('#e0303a'),
  hot: hex('#ff5a52'), pale: hex('#ffb0a0'), bone: hex('#24060d')};
const segD = (px, py, ax, ay, bx, by) => { const dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy || 1e-9, t = clamp(((px - ax) * dx + (py - ay) * dy) / l2); return [Math.hypot(px - ax - t * dx, py - ay - t * dy), t]; };
const ramp = (stops, x) => { x = clamp(x); for (let i = 1; i < stops.length; i++) if (x <= stops[i][0]) { const [a, ca] = stops[i - 1], [b, cb] = stops[i]; return mix(ca, cb, (x - a) / (b - a || 1)); } return stops[stops.length - 1][1]; };

// card units: X across (0 = the far feather edge, 1 = beyond the spine), Y down the segment (0 = the root, 1 = the tip)
function wingPainter(kind) {
  const spineU = .8, n = fbm(kind === 'a' ? 31 : 47);
  // feathers: blades hanging from the spine, swept down and out; [root v, angle (deg from straight down toward u 0), length, half-width]
  const F = kind === 'a'
    ? [[.08, 52, .62, .085], [.2, 46, .66, .09], [.33, 40, .68, .095], [.46, 34, .66, .095], [.6, 28, .6, .09], [.74, 22, .5, .085], [.86, 16, .4, .08]]
    : [[.06, 44, .66, .085], [.18, 38, .7, .09], [.31, 32, .72, .095], [.45, 26, .7, .09], [.59, 20, .62, .085], [.72, 14, .52, .08], [.84, 8, .42, .07]];
  return (u, v) => {
    // the spine: a tapered dark bone along u = spineU (the outer segment narrows to a point at the tip)
    const taper = kind === 'b' ? 1 - .7 * v : 1 - .3 * v;
    const sd = Math.abs(u - spineU) - .07 * taper;
    let col = null, depth = -1;
    if (sd < 0 && v > .02 && v < (kind === 'b' ? .97 : .995)) { const k = -sd / (.07 * taper); col = mix(C.bone, C.deep, .3 + .5 * k); depth = 9; if (Math.abs(u - spineU) < .012) col = mix(col, C.red, .6); }
    // feathers (later ones in front)
    for (let i = 0; i < F.length; i++) {
      const [v0, ang, L, w] = F[i], a = ang * Math.PI / 180;
      const ax = spineU - .02, ay = v0, bx = ax - Math.sin(a) * L * (.55), by = ay + Math.cos(a) * L;
      const [d, t] = segD(u * .55, v, ax * .55, ay, bx * .55, by);
      const half = w * (t < .15 ? .55 + 3 * t : Math.pow(1 - t, .7)) * .55;
      if (d < half && by <= 1.02 && i >= depth - 8) {
        const e = d / half;                    // 0 = the rachis .. 1 = the edge
        let c = ramp([[0, C.dark], [.25, C.deep], [.62, C.crim], [.86, C.red], [1, C.hot]], e * .85 + .15 * t);
        if (e < .12) c = mix(c, C.black, .6);
        c = mix(c, C.black, (n(u * 24, v * 24) - .5) * .35 + .12 * (1 - t));
        col = c; depth = i;
      }
    }
    return col ? [col[0], col[1], col[2], 255] : T;
  };
}

function legPainter(kind) {
  const ax = .6, n = fbm(kind === 'a' ? 53 : 71);
  return (u, v) => {
    // half-width profile along the segment; the blade leans its body toward u 0 (the cutting side) with spikes
    const w = kind === 'a' ? .22 + .12 * Math.sin(Math.PI * Math.min(1, v * 1.2)) : (v < .12 ? .26 + .5 * v : .32 * Math.pow(Math.max(0, 1 - (v - .12) / .86), .9));
    const off = u - ax;
    // spikes on the cutting side (u < ax)
    let spike = 0;
    if (off < 0) for (const s0 of (kind === 'a' ? [.3, .55, .8] : [.22, .42, .6, .76])) { const dv = v - s0; if (dv > -.06 && dv < .02) spike = Math.max(spike, (dv + .06) / .08 * .22); }
    const left = w + spike, right = w * .45;
    if (off < -left || off > right || v < .01 || v > .995) return T;
    const e = off < 0 ? -off / left : off / right;          // 0 = the axis .. 1 = the edge
    let c = ramp([[0, C.black], [.35, C.bone], [.7, C.dark], [.88, C.crim], [1, C.hot]], e);
    if (off < 0 && e > .82) c = mix(c, C.hot, .5);            // the glowing cutting edge
    if (Math.abs(off) < .025) c = mix(c, C.red, .5);          // a seam of crimson light along the axis
    if (kind === 'a' && v < .1 && Math.hypot(off, v - .05) < .12) c = mix(C.deep, C.red, .4);   // the joint knob
    c = mix(c, C.black, (n(u * 18, v * 30) - .5) * .3);
    return [c[0], c[1], c[2], 255];
  };
}

function cupPainter() {
  const porcelain = hex('#f4f0ea'), gold = hex('#d9b24c'), tea = hex('#6b2a10'), red = hex('#b3192a');
  return (u, v) => {
    const x = Math.floor(u * 16), y = Math.floor(v * 16);
    if (y < 3) return x < 4 ? tea : gold;
    if (y <= 4) return gold;
    if (y === 7) return red;
    const k = 1 - .12 * (y - 5) / 11;
    return [porcelain[0] * k, porcelain[1] * k, porcelain[2] * k, 255];
  };
}
function saucerPainter() {
  const porcelain = hex('#f4f0ea'), gold = hex('#d9b24c'), red = hex('#b3192a');
  return (u, v) => {
    const r = Math.max(Math.abs(u - .5), Math.abs(v - .5)) * 2;
    if (r > .88) return gold;
    if (r > .74 && r < .8) return red;
    return porcelain;
  };
}

export function arlecchinoSprites() {
  return {
    wing_a: [...SPRITES.wing_a, wingPainter('a'), false], wing_b: [...SPRITES.wing_b, wingPainter('b'), false],
    leg_a: [...SPRITES.leg_a, legPainter('a'), false], leg_b: [...SPRITES.leg_b, legPainter('b'), false],
    cup: [...SPRITES.cup, cupPainter(), false], saucer: [...SPRITES.saucer, saucerPainter(), false],
  };
}
export function paintArlecchino(rp, sprites = arlecchinoSprites()) {
  void SEG;
  return paintSpriteSet(rp, TEX_DIR, sprites, spriteId);
}
