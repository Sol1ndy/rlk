// Painted sprites for the Corrupted Guardian (파수꾼・타락) rig: tools/build_mboss_guardian_rig.mjs.
// Written to assets/rlk/textures/mboss/guardian/<name>.png and merged into the item atlas.
//
// Every sprite here is drawn in card units, as seen from the front of the boss (X = screen
// right = her LEFT, Y up), on the rectangle CARD[name] that the geometry places it on. The
// palette and proportions follow scratchpad mboss/understand/model.md (ref.png, the guide.pdf
// render and the m1-m4 frames): white lanceolate feathers with grey-violet outlines, cream-gold
// coverts, champagne-gold armour with dark grooves, crimson voxel corruption with glowing
// cracks, a gold spear whose head glows white-hot, and a gold halo.
//
// Sprites (opaque = alpha-cut, glow = translucent):
//   gd_wing_pri / gd_wing_sec / gd_wing_cov   the three wing tiers (one fan, her left)
//   gd_shield / gd_shield_eye                 the eye shield (gold frame) / its gem+iris+field
//                                             painted in luminance for element tints
//   gd_spear_head / gd_spear_head_e           spear head (gold) / enchanted luminance version
//   gd_spear_edge, gd_spear_gem, gd_spear_star, gd_shaft   spear details
//   gd_halo (opaque ring) / gd_halo_glow (glow)
//   gd_crest / gd_crest_side                  winged crest with the red diamond face and eye
//   gd_belt, gd_skirt_front, gd_skirt_side, gd_hip_wing, gd_tail, gd_skirt_back
//   gd_chest, gd_chest_back, gd_collar        torso cards
//   gd_corrupt, gd_corrupt_b, gd_vox, gd_vox_rune, gd_white, gd_sleeve, gd_gold, gd_gold_dark,
//   gd_gauntlet, gd_redstar, gd_blackstar, gd_joint, gd_talon, gd_talon_gold, gd_pauldron
//   gd_spear_glow, gd_trail                   (glow) aura and afterimage cards
import fs from 'node:fs';
import path from 'node:path';
import {png, paint, ramp} from './weapon_paint.mjs';
import {
  rng, C, hex, clamp, smooth, mix, fbm, TRANSPARENT, paintT, onCard, cubic, spline, Path, Shape, mirrorX, star4in,
  Feather, bladeProfile, roundProfile, featherPath, featherColour, firstHit, FEATHER_WHITE, FEATHER_CREAM, inPoly, distPoly,
} from './guardian_paint_lib.mjs';

const PAL = {
  goldHi: C('#f8efcc'), goldLit: C('#dfc88e'), goldMid: C('#bb9c60'), goldDark: C('#8e6c3a'), goldDeep: C('#503518'), goldLine: C('#26150a'),
  spCore: C('#fff8de'), spLit: C('#f9e7a6'), spMid: C('#f0c878'), spEdge: C('#d99a4e'), barb: C('#b96b22'), shaft: C('#c9a35e'),
  gem: C('#c83a28'), gemDark: C('#5a0f0a'), glint: C('#fff4e0'), butt: C('#d8553a'),
  eyeCore: C('#fff6e2'), bezel: C('#f2a060'), iris: C('#f7bc5c'), field: C('#4a1703'),
  cor1: C('#a93b27'), cor2: C('#812e21'), cor3: C('#5f1d13'), cor4: C('#2a1418'), crack: C('#ff5a3c'),
  vox1: C('#481e1c'), vox2: C('#330f21'), vox3: C('#782824'), voxEdge: C('#ee485a'), rune: C('#fc5454'),
  red: C('#c21f2a'), redDark: C('#6e0001'), face: C('#b8402a'), eye: C('#f8f2a8'),
  haloCore: C('#feeac3'), haloRing: C('#f7e2a6'), haloSpike: C('#f3d978'), haloGlow: C('#ead561'),
  gl1: C('#fbdfd4'), gl2: C('#f2ab76'), gl3: C('#e4833c'),
  white: C('#f7efec'), whiteShade: C('#cfc3c1'), line: C('#6e6370'),
};
export const GD_PAL = PAL;
const grainW = fbm(311), grainG = fbm(97), grainR = fbm(523);

// ---- gold material helpers ---------------------------------------------------------------
// e = distance to the shape edge (card units), band = bevel width: bright rim, mid body, dark
// groove line just inside the rim.
function goldAt(e, band, x, y, {dark = 0, hi = 1} = {}) {
  const k = clamp(e / band);
  let c = mix(PAL.goldHi, PAL.goldLit, smooth(0, .35, k));
  c = mix(c, PAL.goldMid, smooth(.35, 1, k) * .7);
  c = mix(c, PAL.goldDark, dark);
  c = mix(c, PAL.goldDeep, (grainG(x * 3, y * 3) - .5) * .25);
  c = mix(c, [255, 250, 235, 255], Math.pow(Math.max(0, Math.sin((x * .35 + y * .55) * 2.2)), 18) * .25 * hi);
  return c;
}
const outlineMix = (c, edge, px, col = PAL.goldLine, w = 1.2) => (edge < px * w ? mix(c, col, .8) : c);

// =============================================================================================
// WING (her left): one fan in wing space (8 units per block, root at 0,0, +X outward = her left,
// as seen from the front). Each tier is a separate display pivoting at the root; at rest the
// tiers compose this picture, and the poses rotate the tiers apart (guard, spread) or together.
// [root x, root y, angle from straight down (deg, + outward), length, half width]
const WR = rng(9127);
const jit = (v, k) => v * (1 + (WR() - .5) * 2 * k);
// primaries: inner ones shorter, the outer edge longest; secondaries hang nearer vertical
const WING_PRI = Array.from({length: 8}, (_, i) => [2.0 + .7 * i + (WR() - .5) * .3, 1.9 - .14 * i, 20 + 4.3 * i + (WR() - .5) * 2.5, jit(12.6 + .72 * i, .04), jit(1.32, .07)]);
const WING_SEC = Array.from({length: 8}, (_, i) => [.1 + .4 * i + (WR() - .5) * .2, .45 + .14 * i, 4 + 3.0 * i + (WR() - .5) * 2, jit(9.2 + .45 * i, .05), jit(1.25, .07)]);
const WING_COV = Array.from({length: 8}, (_, i) => [.3 + .62 * i, 2.2 + .3 * i, 8 + 5.5 * i + (WR() - .5) * 3, jit(3.4 + .12 * i, .06), jit(1.05, .06)]);
function wingFeathers(list, kind) {
  return list.map(([x, y, a, L, w], i) => {
    const bend = kind === 'cov' ? [0, .02, .04] : kind === 'sec' ? [-.02, -.01, .03] : [-.035, -.025, .045];
    const prof = kind === 'cov' ? roundProfile({w, lead: .5}) : bladeProfile({w, lead: .44, root: .5, peak: .25, tip: kind === 'pri' ? .52 : .6, tipPow: 1.25});
    const notches = kind === 'cov' ? [] : kind === 'pri'
      ? [[.5 + .05 * (i % 3), -1, .9, .12], [.72 + .03 * (i % 2), 1, .6, .1]]
      : [[.58 + .04 * (i % 2), -1, .8, .12]];
    return {f: new Feather(featherPath([x, y], a, L, bend), prof, {notches}), i};
  });
}
// Draw order: outer feathers in front (first in the hit list).
const WF = {
  pri: wingFeathers(WING_PRI, 'pri').reverse(),
  sec: wingFeathers(WING_SEC, 'sec').reverse(),
  cov: wingFeathers(WING_COV, 'cov').reverse(),
};
function boxOf(list, pad = .4) {
  const b = [Infinity, Infinity, -Infinity, -Infinity];
  for (const {f} of list) { b[0] = Math.min(b[0], f.box[0]); b[1] = Math.min(b[1], f.box[1]); b[2] = Math.max(b[2], f.box[2]); b[3] = Math.max(b[3], f.box[3]); }
  return {X0: b[0] - pad, X1: b[2] + pad, Y0: b[1] - pad, Y1: b[3] + pad};
}
function wingSprite(kind) {
  const list = WF[kind], card = CARD['gd_wing_' + kind], pal = kind === 'cov' ? FEATHER_CREAM : FEATHER_WHITE;
  const px = (card.X1 - card.X0) / SIZE['gd_wing_' + kind][0];
  return onCard(card, (x, y) => firstHit(list.map(it => ({f: it.f, col: h => {
    let c = featherColour(h, pal, {px, trail: -1, grain: grainW, gx: x * .8, gy: y * .8, sky: kind === 'pri' ? .18 : .1});
    // the root zone under the shield is warmer (gold bounce)
    if (kind !== 'cov') c = mix(c, C('#efd7b4'), (1 - smooth(.0, .28, h.t)) * .45);
    return c;
  }})), x, y, kind === 'cov' ? .35 : .55));
}

// =============================================================================================
// SHIELD: the "eye" of 개안자, long axis horizontal, centre at 0,0 (16 units per block). The
// left end carries the long frame spike; the rig tilts the shield so it points toward her head.
const SH = (() => {
  const lens = (L, R, up, dn, n = 48) => {
    const P = [];
    for (let i = 0; i <= n; i++) { const t = i / n; P.push([lerpN(L[0], R[0], t), lerpN(L[1], R[1], t) + up * Math.sin(Math.PI * t) ** .8]); }
    for (let i = n - 1; i > 0; i--) { const t = i / n; P.push([lerpN(L[0], R[0], t), lerpN(L[1], R[1], t) - dn * Math.sin(Math.PI * t) ** .8]); }
    return P;
  };
  const almond = lens([-11.4, .7], [11.0, -.9], 6.7, 5.9);
  const inner = lens([-8.6, .5], [8.7, -.7], 4.5, 3.8);
  // the long frame spike continues the left point up and out
  const spike = spline([[-6.8, 5.4], [-11.0, 4.6], [-15.3, 4.9, 'c'], [-11.6, 2.2], [-9.6, -.4], [-7.6, 2.0]], 8);
  return {almond: new Shape(almond), inner: new Shape(inner), spike: new Shape(spike)};
})();
function lerpN(a, b, t) { return a + (b - a) * t; }
// Hollow 4-point star frame centred at SC: long points left/right, the vertical points poke out
// through the almond; outer and inner concave stars bound the gold band.
const SC = [-2.3, -.1];
const STAR = {L: 9.4, R: 8.2, U: 8.9, D: 8.3, p: .78, k: .7};
function starBand(x, y) {
  const dx = x - SC[0], dy = y - SC[1];
  const rx = dx < 0 ? STAR.L : STAR.R, ry = dy > 0 ? STAR.U : STAR.D;
  const f = (Math.abs(dx) / rx) ** STAR.p + (Math.abs(dy) / ry) ** STAR.p;   // 1 on the outer star
  const g = (Math.abs(dx) / (rx * STAR.k)) ** STAR.p + (Math.abs(dy) / (ry * STAR.k)) ** STAR.p;
  return {outer: f, inner: g, band: f <= 1 && g >= 1, inside: g < 1};
}
// cream-gold blade feathers on the trailing (lower right) rim, one on the upper right
const SH_BLADES = [[2.8, -4.6, 44, 6.8, .95], [5.4, -4.0, 54, 6.6, .9], [7.6, -2.9, 63, 6.0, .8], [9.4, -1.6, 72, 5.0, .7], [3.6, 5.4, 140, 5.2, .8]].map(([x, y, a, L, w]) =>
  new Feather(featherPath([x, y], a, L, [-.02, .0, .06]), bladeProfile({w, lead: .5, root: .75, peak: .25, tip: .55, tipPow: 1.2})));
const GEM = [-2.0, .0];
function shieldSprite(eyeOnly = false, colour = false) {
  const name = eyeOnly ? 'gd_shield_eye' : 'gd_shield', card = CARD[name];
  const px = (card.X1 - card.X0) / SIZE[name][0];
  return onCard(card, (x, y) => {
    const dA = SH.almond.sd(x, y, 3), dI = SH.inner.sd(x, y, 3), dS = SH.spike.sd(x, y, 1);
    const st = starBand(x, y);
    const gr = Math.hypot(x - GEM[0], y - GEM[1]);
    if (eyeOnly) {
      // eye: gem (core + bezel), the iris crescent hugging the right end, a dark field.
      // colour = the Geo look; otherwise luminance for the element tints.
      if (dI > .1 || st.band) return null;
      const col = (lum, c) => (colour ? C(c) : [lum, lum, lum, 255]);
      if (gr < 2.4) {
        if (gr < 1.25) return colour ? mix(C('#ffffff'), PAL.eyeCore, gr / 1.25) : mix([255, 255, 255, 255], [238, 238, 238, 255], gr / 1.25);
        if (gr < 1.5) return col(120, '#b8561e');
        if (gr < 2.15) return colour ? mix(C('#ffc890'), PAL.bezel, (gr - 1.5) / .65) : mix([222, 222, 222, 255], [170, 170, 170, 255], (gr - 1.5) / .65);
        return col(70, '#7a2a08');
      }
      const ix = (x - 2.6) / 6.4, iy = (y + .2) / 4.4, ir = Math.hypot(ix, iy);
      const cut = Math.hypot((x - .6) / 5.6, (y + .2) / 4.2);
      if (ir < 1 && cut > 1) {
        const k = smooth(0, 1, clamp((cut - 1) / .35)) * (1 - smooth(.85, 1, ir)) + .2;
        return colour ? mix(C('#c47a22'), PAL.iris, k) : mix([170, 170, 170, 255], [250, 250, 250, 255], k);
      }
      const spill = Math.exp(-((gr - 2.4) ** 2) / 5) * .5;
      return colour ? mix(PAL.field, C('#a8481a'), spill) : mix([58, 58, 58, 255], [140, 140, 140, 255], spill);
    }
    const inAlmond = dA < 0, inSpike = dS < 0;
    let blade = null;
    if (!inAlmond) for (const f of SH_BLADES) { const h = f.sample(x, y); if (h) { blade = h; break; } }
    if (st.band) {
      // bevelled star band: lit outer half, darker inner half, dark lines at both borders
      const k = clamp((1 - st.outer) / (1 - Math.pow(STAR.k, STAR.p)));
      let c = mix(PAL.goldHi, PAL.goldLit, smooth(0, .45, k));
      c = mix(c, PAL.goldDark, smooth(.5, 1, k) * .6);
      c = mix(c, PAL.goldDeep, (grainG(x * 3, y * 3) - .5) * .22);
      const lineW = px * 1.6 / 6;
      if (1 - st.outer < lineW * 1.2 || st.inner - 1 < lineW) c = mix(c, PAL.goldLine, .8);
      return c;
    }
    if (inAlmond && dI < 0) return null;            // the opening: the eye card fills it
    if (inAlmond || inSpike) {
      const e = inAlmond ? Math.min(-dA, Math.max(dI, 0)) : -dS;
      let c = goldAt(inAlmond ? -dA : -dS, 1.2, x, y);
      if (inAlmond) {
        const band = -dA + dI;                         // ~ band thickness here
        const k = -dA / Math.max(band, .1);
        if (Math.abs(k - .55) < .07) c = mix(c, PAL.goldDeep, .7);      // engraved groove
        if (k > .85) c = mix(c, PAL.goldDark, .5);                        // inner lip shadow
      }
      return outlineMix(c, inAlmond ? Math.min(-dA, Math.abs(dI)) : -dS, px, PAL.goldLine, 1.3);
    }
    if (blade) {
      let c = mix(C('#f4e8c8'), PAL.goldLit, (1 - blade.e) * .75);
      if (blade.e > .65) c = mix(c, C('#fff8e4'), .35);
      return outlineMix(c, blade.edge, px, PAL.goldDeep, 1.4);
    }
    return null;
  });
}

// =============================================================================================
// SPEAR HEAD (spear units, 7.27 per block; tip at Y 31.4, shaft axis X = 0). The head lies in
// one plane: leaf blade, two back-swept barbs, oval ring framing a red 4-point star gem,
// collar, and the crescent of two mirrored swept-back wing-blades whose tips sit by the grip.
const SP = (() => {
  // blade outline (right half), from the root at the ring top to the tip
  const half = spline([[.32, 19.0], [.95, 20.0], [1.12, 21.4], [1.02, 23.6], [.8, 26.0], [.48, 28.6], [.16, 30.6], [0, 31.45, 'c']], 10);
  const blade = [...half, ...mirrorX(half).reverse()];
  // barb: from the blade root out and back toward the butt, notched
  const barbR = spline([[.6, 19.6], [1.6, 19.9], [2.6, 19.75], [3.25, 19.0, 'c'], [2.5, 19.15], [1.7, 19.15], [1.05, 18.9]], 8);
  // crescent wing-blade (right): sweeps out from the collar and back toward the butt, its tip
  // the outermost point (m3 f1148); a shorter inner prong splits off at the notch
  const outer = spline([[.45, 14.8], [1.4, 14.25], [2.45, 13.15], [3.35, 11.75], [3.98, 10.45], [4.28, 9.3, 'c']], 10);
  const inner = spline([[4.28, 9.3], [3.72, 10.25], [3.08, 11.3], [2.3, 12.4], [1.4, 13.2], [.3, 13.75]], 10);
  const cres = [...outer, ...inner];
  const prong = spline([[.45, 13.3], [1.15, 12.65], [1.72, 11.75], [2.05, 10.7, 'c'], [1.62, 11.55], [1.0, 12.25], [.35, 12.75]], 8);
  return {
    blade: new Shape(blade), bladeHalf: half,
    barbs: [new Shape(barbR), new Shape(mirrorX(barbR))],
    cres: [new Shape(cres), new Shape(mirrorX(cres))],
    prongs: [new Shape(prong), new Shape(mirrorX(prong))],
  };
})();
export const SPEAR = {TIP: 31.4, GRIP: 8.0, RING: [0, 17.0], RING_R: [2.0, 2.2], COLLAR: [14.25, 15.05], SHAFT: [2.3, 14.3], BUTT: [-.4, 2.6]};
function spearHead(enchanted = false) {
  const card = CARD.gd_spear_head, px = (card.X1 - card.X0) / SIZE.gd_spear_head[0];
  // enchanted head is luminance-only: the item tint gives the element colour
  const L = c => { const v = (c[0] * .3 + c[1] * .59 + c[2] * .11); const w = Math.min(255, v * 1.08 + 20); return [w, w, w, 255]; };
  const out = c => (enchanted ? L(c) : c);
  return onCard(card, (x, y) => {
    const [rcx, rcy] = SPEAR.RING, [rx, ry] = SPEAR.RING_R;
    const ex = (x - rcx) / rx, ey = (y - rcy) / ry, er = Math.hypot(ex, ey);
    // ring band
    if (er < 1 && er > .76) {
      const k = (er - .76) / .24;
      let c = mix(PAL.spLit, C('#dc9256'), Math.abs(k - .4) * 1.4);
      if (k < .12 || k > .88) c = mix(c, PAL.goldDeep, .6);
      return out(c);
    }
    // gem inside the ring: red/black 4-point star with a white glint
    if (er <= .76) {
      const s = star4in(x - rcx, y - rcy, 1.5, 1.72, .02);
      if (s > 0) {
        let c = mix(PAL.gemDark, PAL.gem, smooth(0, .55, s));
        c = mix(c, C('#ff8a5a'), smooth(.55, .9, s) * .5);
        const gl = Math.hypot(x - rcx + .2, y - rcy - .25);
        if (gl < .32) c = mix(c, PAL.glint, 1 - gl / .32);
        if (s < .08) c = mix(c, PAL.goldDeep, .7);
        return enchanted ? c : c;   // the gem stays red in every variant
      }
      // dark maroon field around the gem (glows warmer near the star)
      const glowK = Math.max(0, 1 - er / .76);
      return mix(C('#3c0d08'), C('#8a2a14'), glowK * .7);
    }
    // collar
    if (y > SPEAR.COLLAR[0] && y < SPEAR.COLLAR[1] && Math.abs(x) < .72 - (y - SPEAR.COLLAR[0]) * .2) {
      return out(mix(PAL.goldHi, PAL.goldMid, Math.abs(x) / .7));
    }
    // ring pointed joins
    if (y >= 18.8 && y < 19.4 && Math.abs(x) < (19.4 - y) * 1.1 + .25) return out(PAL.spMid);
    if (y > 15.0 && y < 15.6 && Math.abs(x) < (y - 15.0) * 1.0 + .3) return out(PAL.spMid);
    // blade
    const db = SP.blade.sd(x, y, .5);
    if (db < 0) {
      const half = SP.bladeHalfWidth(y), r = Math.abs(x) / Math.max(half, .05);
      let c = mix(PAL.spCore, PAL.spLit, smooth(.08, .5, r));
      c = mix(c, PAL.spMid, smooth(.5, .9, r));
      // central ridge line and a faint facet on one side
      if (r < .06) c = mix(c, [255, 255, 250, 255], .8);
      if (x < 0 && r > .1 && r < .9) c = mix(c, PAL.spEdge, .12);
      c = mix(c, PAL.spEdge, smooth(.85, 1, r) * .8);
      // engraved swirl line near the root
      const sw = Math.abs(Math.sin((y - 20) * 1.3) * .55 - x);
      if (y < 23.5 && y > 19.8 && sw < .07) c = mix(c, PAL.spEdge, .5);
      return out(outlineMix(c, -db, px, PAL.goldDeep, 1.2));
    }
    // barbs
    for (const s of SP.barbs) {
      const d = s.sd(x, y, .3);
      if (d < 0) {
        let c = mix(C('#d58d3c'), PAL.barb, smooth(.0, .5, -d));
        c = mix(c, PAL.spLit, smooth(.25, 0, -d) * .55);
        return out(outlineMix(c, -d, px, PAL.goldDeep, 1.2));
      }
    }
    // crescent blades and prongs
    for (const s of [...SP.cres, ...SP.prongs]) {
      const d = s.sd(x, y, .3);
      if (d < 0) {
        let c = mix(PAL.spLit, PAL.spCore, smooth(.0, .45, -d) * .7);
        c = mix(c, PAL.spMid, smooth(.0, .12, .12 + d) * .5);
        // notch line on the blade
        if (Math.abs(y - 11.0 + (Math.abs(x) - 3.0) * .9) < .09 && Math.abs(x) > 2.8 && Math.abs(x) < 3.7) c = mix(c, PAL.spEdge, .7);
        return out(outlineMix(c, -d, px, PAL.spEdge, 1.3));
      }
    }
    return null;
  });
}
SP.bladeHalfWidth = y => {
  let best = 0;
  const h = SP.bladeHalf;
  for (let i = 0; i < h.length - 1; i++) {
    const [x0, y0] = h[i], [x1, y1] = h[i + 1];
    if ((y - y0) * (y - y1) <= 0 && y1 !== y0) best = Math.max(best, x0 + (x1 - x0) * (y - y0) / (y1 - y0));
  }
  return best;
};
// Edge-on profile of the head for the crossed card: thin lens, ring as a bar, crescent lines.
function spearEdge(enchanted = false) {
  const card = CARD.gd_spear_edge;
  return onCard(card, (x, y) => {
    let hw = 0;
    if (y > 19 && y < 31.4) hw = .32 * Math.pow(1 - (y - 19) / 12.4, .6) + .02;
    else if (y >= 14.3 && y <= 19.2) hw = .38;
    else if (y > 8.4 && y < 14.3) hw = .2;
    if (Math.abs(x) > hw) return null;
    const c = mix(PAL.spCore, PAL.spMid, Math.abs(x) / Math.max(hw, .01));
    if (enchanted) { const v = c[0] * .3 + c[1] * .59 + c[2] * .11 + 20; return [Math.min(255, v), Math.min(255, v), Math.min(255, v), 255]; }
    return c;
  });
}
// Red 4-point star with facets (butt finial, orbit star, red ornaments).
function facetStar(base, dark, light, k = .1) {
  return (u, v) => {
    const x = (u - .5) * 2, y = (.5 - v) * 2;
    const s = star4in(x, y, .98, .98, k);
    if (s <= 0) return TRANSPARENT;
    // four facets per arm: lit toward the upper left
    const q = (x >= 0) === (y >= 0) ? 1 : -1;
    const side = Math.sign(Math.abs(x) - Math.abs(y)) * q;
    let c = mix(base, side > 0 ? light : dark, .45);
    c = mix(c, light, smooth(.55, 1, s) * .5);
    if (s < .07) c = mix(c, C('#2a0a06'), .7);
    return c;
  };
}

// =============================================================================================
// HALO (16 units per block, ring centre 0,0): ring + faint inner ring + tall top spike + two
// short lower spikes + thin rays. The glow card is a separate translucent sprite.
function haloSprite() {
  const card = CARD.gd_halo;
  return onCard(card, (x, y) => {
    const r = Math.hypot(x, y), a = Math.atan2(y, x);
    // outer ring
    if (r > 4.95 && r < 5.62) {
      const k = (r - 4.95) / .67;
      return mix(PAL.haloCore, PAL.haloRing, Math.abs(k - .45) * 1.6);
    }
    if (r > 3.55 && r < 3.78) return mix(PAL.haloRing, PAL.haloCore, .4);
    // top spike: slender diamond from y 4.6 to 9.4
    if (y > 4.2 && y < 9.5) {
      const t = (y - 4.2) / 5.3, hw = t < .2 ? .55 * t / .2 + .1 : .65 * Math.pow(1 - (t - .2) / .8, 1.1);
      if (Math.abs(x) < hw) return mix(PAL.haloCore, PAL.haloSpike, Math.abs(x) / Math.max(hw, .01));
    }
    // lower spikes at 4 and 8 o'clock
    for (const deg of [-35, -145]) {
      const d = deg * Math.PI / 180, ux = Math.cos(d), uy = Math.sin(d);
      const along = x * ux + y * uy, across = Math.abs(-x * uy + y * ux);
      if (along > 5.2 && along < 8.0) {
        const t = (along - 5.2) / 2.8, hw = .42 * (1 - t);
        if (across < hw) return mix(PAL.haloCore, PAL.haloSpike, across / Math.max(hw, .01));
      }
    }
    // thin rays
    for (const deg of [20, 55, 125, 160, -10, 190, -90]) {
      const d = deg * Math.PI / 180, ux = Math.cos(d), uy = Math.sin(d);
      const along = x * ux + y * uy, across = Math.abs(-x * uy + y * ux);
      const len = deg === -90 ? 7.2 : 8.4;
      if (along > 5.6 && along < len && across < .13 * (1 - (along - 5.6) / (len - 5.6)) + .04) return mix(PAL.haloCore, PAL.haloRing, .4);
    }
    return null;
  });
}
function haloGlow() {
  const card = CARD.gd_halo_glow;
  return onCard(card, (x, y) => {
    const r = Math.hypot(x, y), R = card.X1;
    const ring = Math.exp(-(((r - 5.3) / 1.5) ** 2));
    const core = Math.exp(-((r / 3.2) ** 2));
    const ray = Math.max(0, Math.cos(Math.atan2(y, x) * 4)) ** 12 * Math.exp(-r / 7) * .5;
    const fade = 1 - smooth(R * .78, R * .98, r);
    const a = clamp((.55 * ring + .45 * core + ray) * fade);
    const c = mix(PAL.haloGlow, PAL.haloCore, clamp(core + ring * .4));
    return [c[0], c[1], c[2], a * 255 < 3 ? 0 : a * 235];
  });
}

// =============================================================================================
// HEAD: winged crest framing the red diamond face with one eye (16 units per block, origin
// at the neck; eye at Y 2.1).
const CREST = (() => {
  const hornR = spline([[.35, 2.6], [.75, 3.6], [1.15, 4.8], [1.2, 5.8], [.95, 6.6, 'c'], [.72, 5.6], [.55, 4.5], [.2, 3.4]], 8);
  const wingFeathersR = [
    [[1.0, 2.5], 118, 4.4, .62], [[1.0, 2.2], 108, 4.0, .58], [[1.1, 1.9], 98, 3.4, .52],
  ].map(([r, a, L, w]) => new Feather(featherPath(r, a, L, [.03, .06, .12]), bladeProfile({w, lead: .45, root: .7, peak: .2, tip: .6})));
  const wingFeathersL = wingFeathersR.map(f => new Feather(mirrorX(f.path.p), t => { const [l, r] = f.prof(t); return [r, l]; }));
  return {horns: [new Shape(hornR), new Shape(mirrorX(hornR))], wings: [...wingFeathersR, ...wingFeathersL]};
})();
function crestSprite(back = false) {
  const card = CARD.gd_crest, px = (card.X1 - card.X0) / SIZE.gd_crest[0];
  return onCard(card, (x, y) => {
    // eye: pale yellow ring + dot, dark surround (the back of the head shows the dark shell)
    const ey = y - 2.1, er = Math.hypot(x, ey);
    if (back && Math.abs(x) / 1.35 + Math.abs(ey) / 2.1 < 1) {
      let c = mix(PAL.cor3, PAL.cor4, smooth(0, 1.2, Math.abs(x)));
      if (Math.abs(x) < .1) c = mix(c, PAL.goldMid, .6);
      return c;
    }
    if (er < .78) {
      if (er < .26) return PAL.eye;
      if (er < .5) return mix(C('#3a1a10'), C('#20100a'), .5);
      if (er < .7) return PAL.eye;
      return C('#1c0c08');
    }
    // face diamond (dark red to orange) with a gold rim
    const dd = Math.abs(x) / 1.25 + Math.abs(ey) / (ey > 0 ? 2.0 : 1.9);
    if (dd < 1) {
      let c = mix(C('#e07a3a'), PAL.face, smooth(.2, .7, dd));
      c = mix(c, PAL.redDark, smooth(.7, .95, dd));
      if (dd > .9) c = mix(c, PAL.goldLit, .7);
      return c;
    }
    // gold trim under the diamond (V)
    if (y < .55 && y > -.35 && Math.abs(x) < 1.4 - (.55 - y) * .6 && y > -.35 + Math.abs(x) * .45) return goldAt(.3, 1, x, y);
    // horns
    for (const s of CREST.horns) {
      const d = s.sd(x, y, .2);
      if (d < 0) {
        let c = mix(FEATHER_WHITE.light, FEATHER_WHITE.shadeC, smooth(0, .35, -d) * .6);
        if (Math.abs(x) < .9 && y < 5) c = mix(c, FEATHER_WHITE.shadeC, .3);
        return outlineMix(c, -d, px, FEATHER_WHITE.line, 1.3);
      }
    }
    // side wings (3 feathers each)
    for (const f of CREST.wings) {
      const h = f.sample(x, y);
      if (h) return featherColour(h, FEATHER_WHITE, {px, trail: -1, barbs: false});
    }
    // head shell behind (dark crimson) visible around the diamond
    if (Math.abs(x) < 1.35 && y > -.6 && y < 3.9 && Math.abs(x) / 1.35 + Math.abs(y - 1.7) / 2.3 < 1.12) return mix(PAL.cor4, PAL.cor3, .4);
    return null;
  });
}
// Side view of the crest: the horn feathers and wings seen edge-on, a slim white profile.
function crestSide() {
  const card = CARD.gd_crest_side, px = (card.X1 - card.X0) / SIZE.gd_crest_side[0];
  const horn = new Shape(spline([[-.4, 2.4], [-.1, 3.8], [.2, 5.2], [.15, 6.4, 'c'], [-.15, 5.3], [-.55, 4.0], [-.9, 2.8]], 8));
  const wing = new Feather(featherPath([-.2, 2.5], 160, 3.8, [.02, .05, .1]), bladeProfile({w: .45, lead: .5, root: .7, peak: .2, tip: .6}));
  return onCard(card, (x, y) => {
    const d = horn.sd(x, y, .2);
    if (d < 0) return outlineMix(mix(FEATHER_WHITE.light, FEATHER_WHITE.shadeC, .3), -d, px, FEATHER_WHITE.line, 1.3);
    const h = wing.sample(x, y);
    if (h) return featherColour(h, FEATHER_WHITE, {px, barbs: false});
    return null;
  });
}

// =============================================================================================
// LOWER BODY (skirt units: 12.8 per block, origin at the belt centre; X = her left).
// Front: the tabard with three red 4-point stars over two long front panels of layered
// feathers with jagged notches; a dark slit between them.
const SKF = (() => {
  const panels = [];
  // each front panel: a long inner feather and a slightly shorter outer one, notched edges
  for (const side of [-1, 1]) {
    const specs = [[.95, -2.6, 1.0, 18.8, 1.08, [.42, .66, .83]], [2.15, -2.4, 4.5, 17.4, 1.02, [.5, .74]]];
    for (const [x, y, a, L, w, nt] of specs) {
      const p = featherPath([side * x, y], side * a, L, [0, side * .004, side * -.012]);
      const notches = nt.map((t, i) => [t, i % 2 ? -side : side, 1.0, .14]);
      panels.push(new Feather(p, bladeProfile({w, lead: .5, root: .95, peak: .12, tip: .8, tipPow: 1.35}), {notches}));
    }
  }
  // tabard: a broad bib under the belt with a jagged hem of four points
  const hem = [[-2.2, .4, 'c'], [-2.6, -1.6], [-3.0, -3.3], [-2.7, -4.9, 'c'], [-1.9, -3.9], [-1.15, -5.7, 'c'], [-.55, -4.5], [0, -6.5, 'c'], [.55, -4.5], [1.15, -5.7, 'c'], [1.9, -3.9], [2.7, -4.9, 'c'], [3.0, -3.3], [2.6, -1.6], [2.2, .4, 'c']];
  return {panels: panels.reverse(), bib: new Shape(spline(hem, 6))};
})();
function skirtFront() {
  const card = CARD.gd_skirt_front, px = (card.X1 - card.X0) / SIZE.gd_skirt_front[0];
  return onCard(card, (x, y) => {
    // three red stars across the top of the tabard and the red line under the centre star
    for (const [sx, sy, r] of [[0, -1.8, 1.45], [-1.7, -1.4, .8], [1.7, -1.4, .8]]) {
      const st = star4in(x - sx, y - sy, r * .8, r, .02);
      if (st > 0) return mix(mix(PAL.redDark, PAL.red, smooth(0, .4, st)), C('#ff7a4a'), smooth(.5, .9, st) * .6);
    }
    const db = SKF.bib.sd(x, y, .3);
    if (db < 0) {
      if (Math.abs(x) < .12 && y < -3.0 && y > -5.6) return PAL.red;
      let c = mix(FEATHER_WHITE.light, FEATHER_WHITE.shadeC, smooth(0, 1, (-y - 1) / 5) * .55);
      // soft feather strokes
      const k = Math.abs(((x * 1.1 + 40) % 1.15) - .57);
      if (k < .05 && y < -2.4) c = mix(c, FEATHER_WHITE.shadeC, .45);
      c = mix(c, FEATHER_WHITE.deep, (grainW(x, y) - .5) * .12);
      return outlineMix(c, -db, px, FEATHER_WHITE.line, 1.3);
    }
    for (const f of SKF.panels) {
      const h = f.sample(x, y);
      if (h) return featherColour(h, FEATHER_WHITE, {px, trail: -1, grain: grainW, gx: x, gy: y, sky: .12});
    }
    if (Math.abs(x) < .95 && y < -3 && y > -15.5) return mix(PAL.cor3, PAL.cor4, smooth(-4, -14, y));
    return null;
  });
}
// Outer flared panel (her right as drawn; the left one is the uv-mirrored card): long
// feathers from the hip that sweep down and flare outward at the hem like hakama spikes.
const SKS = [[.2, -.4, 7, 18.8, 1.15, [-.03, -.03, .13]], [1.5, -1.0, 15, 16.0, 1.0, [-.04, -.02, .17]], [-.7, -.3, 2.5, 17.2, .95, [-.02, -.01, .05]]]
  .map(([x, y, a, L, w, b], i) => new Feather(featherPath([x, y], a, L, b), bladeProfile({w, lead: .45, root: .8, peak: .2, tip: .7, tipPow: 1.25}),
    {notches: [[.48 + .05 * i, -1, 1.0, .14], [.74, 1, .8, .12]]}));
function skirtSide() {
  const card = CARD.gd_skirt_side, px = (card.X1 - card.X0) / SIZE.gd_skirt_side[0];
  return onCard(card, (x, y) => {
    for (const f of SKS) { const h = f.sample(x, y); if (h) return featherColour(h, FEATHER_WHITE, {px, trail: 1, grain: grainW, gx: x, gy: y, sky: .15}); }
    return null;
  });
}
// Back panel: broad layered feathers.
const SKB = Array.from({length: 5}, (_, i) => [-3.8 + i * 1.9, -.3, -7 + i * 3.5, [16.2, 17.8, 18.6, 17.4, 15.8][i], 1.35])
  .map(([x, y, a, L, w]) => new Feather(featherPath([x, y], a, L, [0, .01, -.01]), bladeProfile({w, lead: .5, root: .9, peak: .15, tip: .75, tipPow: 1.2}),
    {notches: [[.55, 1, 1.1, .14], [.78, -1, .9, .12]]}));
function skirtBack() {
  const card = CARD.gd_skirt_back, px = (card.X1 - card.X0) / SIZE.gd_skirt_back[0];
  return onCard(card, (x, y) => {
    for (const f of SKB) { const h = f.sample(x, y); if (h) return featherColour(h, FEATHER_WHITE, {px, trail: -1, grain: grainW, gx: x, gy: y, sky: .1}); }
    return null;
  });
}
// Hip feather-wing (her right as drawn): 5 feathers fanning out and up from under the belt.
const HIPW = Array.from({length: 3}, (_, i) => new Feather(featherPath([0, 0], -(100 + i * 16), 4.6 - i * .8, [-.02, -.05, -.1]),
  bladeProfile({w: .62, lead: .45, root: .7, peak: .2, tip: .6}), {notches: [[.7, -1, .4, .08]]}));
function hipWing() {
  const card = CARD.gd_hip_wing, px = (card.X1 - card.X0) / SIZE.gd_hip_wing[0];
  return onCard(card, (x, y) => {
    for (const f of HIPW) { const h = f.sample(x, y); if (h) return featherColour(h, FEATHER_WHITE, {px, trail: -1, barbs: false}); }
    return null;
  });
}
// Tail streamer (her left hip; tail units 10.67 per block): an S-curved band ending in a broad
// paddle that tapers to a point.
const TAIL = new Feather(spline([[0, 0], [.8, -3], [2.6, -6.5], [2.4, -10.5], [.4, -14.0], [-.6, -16.6], [-.2, -19.2]], 12),
  t => { const w = t < .55 ? .9 + .3 * t : t < .82 ? 1.07 + 1.3 * Math.sin((t - .55) / .27 * Math.PI / 2) : 2.37 * Math.pow(1 - (t - .82) / .18, .9); return [w * .9, w * 1.1]; },
  {notches: [[.86, 1, 1.0, .14], [.92, -1, .8, .12]]});
function tailSprite() {
  const card = CARD.gd_tail, px = (card.X1 - card.X0) / SIZE.gd_tail[0];
  return onCard(card, (x, y) => {
    const h = TAIL.sample(x, y);
    if (h) return featherColour(h, FEATHER_WHITE, {px, trail: -1, grain: grainW, gx: x, gy: y, sky: .1});
    return null;
  });
}
// Gold crown-belt (16 per block, origin at the belt centre): a V pointing down at the front with
// up-swept spikes on each side and the red 4-point star in the middle.
const BELT = (() => {
  const halfOut = spline([[0, -2.2], [1.3, -1.3], [2.5, .0], [3.2, 1.5], [3.8, 3.3, 'c'], [3.0, 2.2], [2.3, 1.3], [1.6, 1.6], [1.9, 2.9, 'c'], [1.15, 1.5], [.0, .7]], 8);
  const P = [...halfOut, ...mirrorX(halfOut).reverse()];
  return new Shape(P);
})();
function beltSprite() {
  const card = CARD.gd_belt, px = (card.X1 - card.X0) / SIZE.gd_belt[0];
  return onCard(card, (x, y) => {
    const s = star4in(x, y + .5, 1.1, 1.45, .02);
    if (s > 0) return mix(mix(PAL.redDark, PAL.red, smooth(0, .4, s)), C('#ff8a5a'), smooth(.55, .95, s) * .5);
    const d = BELT.sd(x, y, .3);
    if (d < 0) return outlineMix(goldAt(-d, .9, x, y), -d, px);
    return null;
  });
}

// =============================================================================================
// TORSO cards (16 per block; origin at the waist; neck at Y 12.2). Front: a slim red-black core
// with gold trims, the white collar feathers sweeping down her right side, the red ring gem
// on the left collar and the gold pauldron edge.
const CHEST = (() => {
  const body = new Shape(spline([[-2.0, 0], [-2.3, 3], [-2.9, 7.5], [-3.9, 10.4], [-1.8, 11.6], [0, 12.0], [1.8, 11.6], [3.9, 10.4], [2.9, 7.5], [2.3, 3], [2.0, 0, 'c']], 8));
  const collarFeathers = [[-.3, 12.6, -10, 8.2, 1.05], [-1.2, 12.3, -22, 8.0, 1.0], [-2.1, 11.8, -34, 7.2, .95], [-2.9, 11.0, -46, 5.8, .85], [-3.5, 10.0, -58, 4.2, .75],
    [.5, 12.6, 14, 6.4, .95], [1.3, 12.2, 26, 5.6, .9], [2.0, 11.6, 38, 4.6, .8]]
    .map(([x, y, a, L, w]) => new Feather(featherPath([x, y], a, L, [-.02, -.02, .03]), bladeProfile({w, lead: .5, root: .8, peak: .2, tip: .6}), {notches: [[.7, 1, .5, .1]]}));
  return {body, collarFeathers};
})();
function chestSprite(back = false) {
  const card = CARD.gd_chest, px = (card.X1 - card.X0) / SIZE.gd_chest[0];
  return onCard(card, (x, y) => {
    if (!back) {
      // red ring gem on the left collar
      const gr = Math.hypot(x - 2.1, y - 8.2);
      if (gr < 1.1) return gr < .42 ? C('#ffb090') : gr < .78 ? PAL.red : mix(PAL.goldLit, PAL.goldDeep, .3);
      for (const f of CHEST.collarFeathers) { const h = f.sample(x, y); if (h) return featherColour(h, FEATHER_WHITE, {px, trail: -1, barbs: false}); }
    }
    const d = CHEST.body.sd(x, y, .3);
    if (d < 0) {
      // slim crimson core: white-gold plates at the sides, a red-black V down the middle
      const centre = Math.abs(x) < 1.0 + Math.max(0, y - 4) * .22;
      let c = centre ? mix(PAL.cor2, PAL.cor4, smooth(0, 2.0, -d) * .6) : mix(C('#eae2da'), C('#c9bcb4'), smooth(2, 9, y));
      if (back) c = mix(PAL.cor2, PAL.cor4, smooth(0, 2.5, -d) * .7);
      // red diamond on the sternum
      if (!back && Math.abs(x) / 1.0 + Math.abs(y - 6.2) / 1.8 < 1) c = mix(PAL.red, C('#ff7a4a'), smooth(.6, 1, 1 - Math.abs(x) / 1.0 - Math.abs(y - 6.2) / 1.8 + .6) * .5);
      // gold trims: a V across the chest, the borders of the centre band and the rim
      const v = Math.abs(y - (3.0 + Math.abs(x) * 1.25));
      if (v < .32) c = goldAt(.32 - v, .32, x, y);
      if (!centre && Math.abs(Math.abs(x) - (1.0 + Math.max(0, y - 4) * .22)) < .28 && !back) c = goldAt(.3, .4, x, y);
      if (-d < .45) c = goldAt(-d, .45, x, y);
      if (!back && x > .9 && y > 8.6 && y < 11.4) c = goldAt(1, 1, x, y);     // left pauldron edge
      return c;
    }
    return null;
  });
}
function collarSprite() {
  const card = CARD.gd_collar, px = (card.X1 - card.X0) / SIZE.gd_collar[0];
  // jagged white/black zig-zag feather plates, small black 4-point stars
  return onCard(card, (x, y) => {
    const zig = Math.abs(((x * .9) % 2 + 2) % 2 - 1);
    const top = 1.2 + zig * 1.4;
    if (y > top || y < -1.4) return null;
    for (const sx of [-3.2, 0, 3.2]) { const s = star4in(x - sx, y - .1, .7, .9, .02); if (s > 0) return C('#1a1416'); }
    const k = (y + 1.4) / (top + 1.4);
    let c = mix(FEATHER_WHITE.shadeC, FEATHER_WHITE.light, k);
    if (top - y < px * 1.4) c = mix(c, FEATHER_WHITE.line, .8);
    if (y < -1.0) c = mix(c, C('#2a2026'), .7);
    return c;
  });
}

// =============================================================================================
// Small tiling materials (32x32 unless noted). Faces of voxel boxes use the whole texture.
const tile = fn => (u, v) => fn(u, v);
function corrupt(seed) {
  const n = fbm(seed), m = fbm(seed + 7);
  return tile((u, v) => {
    let c = mix(PAL.cor2, PAL.cor4, clamp(n(u * 3, v * 3) * 1.4 - .2));
    c = mix(c, PAL.cor1, smooth(.6, .85, m(u * 2 + 3, v * 2)) * .7);
    // glowing cracks: thin ridges of a second noise
    const r = Math.abs(m(u * 4.2, v * 4.2) - .5);
    if (r < .025) c = mix(PAL.crack, [255, 190, 150, 255], .2);
    else if (r < .05) c = mix(c, PAL.crack, .55);
    // bevel edge
    const e = Math.min(u, v, 1 - u, 1 - v);
    if (e < .06) c = mix(c, PAL.cor4, .5);
    return c;
  });
}
function voxel(rune) {
  const n = fbm(rune ? 77 : 71);
  return tile((u, v) => {
    const e = Math.min(u, v, 1 - u, 1 - v);
    let c = mix(PAL.vox1, PAL.vox2, n(u * 3, v * 3));
    c = mix(c, PAL.vox3, smooth(.6, 1, n(u * 2 + 9, v * 2)) * .45);
    if (e < .045) return mix(PAL.voxEdge, C('#ff9a80'), .2);
    if (e < .085) c = mix(c, PAL.voxEdge, .3);
    if (rune) {
      // faint circuit/rune lines: a ring and two crossing strokes
      const r = Math.hypot(u - .5, v - .5);
      if (Math.abs(r - .25) < .018) c = mix(c, PAL.rune, .75);
      if (Math.abs(u - v) < .02 && r < .25 && r > .1) c = mix(c, PAL.rune, .55);
      if (Math.abs(v - .72) < .016 && u > .2 && u < .5) c = mix(c, PAL.rune, .5);
    }
    return c;
  });
}
const flat = (c1, c2, seed = 3) => { const n = fbm(seed); return tile((u, v) => mix(C(c1), C(c2), n(u * 3, v * 3))); };
function goldTile(dark = false) {
  return tile((u, v) => {
    const e = Math.min(u, v, 1 - u, 1 - v);
    let c = mix(goldAt(e * 8, 1, u * 9, v * 9), C('#e8c070'), .35);
    if (dark) c = mix(c, PAL.goldDark, .45);
    if (e < .05) c = mix(c, PAL.goldLine, .6);
    return c;
  });
}
function gauntlet() {
  return tile((u, v) => {
    // gold with an amber glowing strip along the length (v), engraved swirl
    let c = goldAt(Math.min(u, 1 - u) * 6, 1, u * 7, v * 14);
    const s = Math.abs(u - .5);
    if (s < .2) {
      c = mix(PAL.gl3, PAL.gl2, 1 - s / .2);
      c = mix(c, PAL.gl1, Math.max(0, 1 - s / .07) * .8);
      const sw = Math.abs(Math.sin(v * 18) * .1 - (u - .5));
      if (sw < .02) c = mix(c, PAL.gl1, .8);
    }
    if (Math.min(u, 1 - u) < .04) c = mix(c, PAL.goldLine, .6);
    return c;
  });
}
function sleeve() {
  const n = fbm(13);
  return tile((u, v) => {
    let c = mix(PAL.white, PAL.whiteShade, n(u * 2, v * 4) * .6);
    const e = Math.min(u, 1 - u);
    if (e < .06) c = mix(c, PAL.whiteShade, .6);
    return c;
  });
}
function jointRing() {
  return (u, v) => {
    const r = Math.hypot(u - .5, v - .5) * 2;
    if (r > 1) return TRANSPARENT;
    if (r < .38) return mix(C('#2a1a12'), C('#4a3020'), r / .38);
    if (r < .5) return PAL.goldLine;
    return goldAt((1 - r) * 3, 1, u * 5, v * 5);
  };
}
function talon(gold = false) {
  return (u, v) => {
    const hw = .5 * Math.pow(1 - v, .8);
    if (Math.abs(u - .5) > hw) return TRANSPARENT;
    if (gold) return mix(PAL.goldHi, PAL.goldMid, Math.abs(u - .5) / Math.max(hw, .01));
    return mix(C('#ff6a4a'), PAL.cor3, Math.abs(u - .5) / Math.max(hw, .01) * .8 + v * .2);
  };
}
// Glow cards (translucent): luminance gradients, tinted per element by the item definition.
function spearGlow() {
  const card = CARD.gd_spear_glow;
  return onCard(card, (x, y) => {
    // aura hugging the blade (Y 19..31.4) and a thin streak down the shaft
    let a = 0;
    if (y > 18.5 && y < 32.2) {
      const t = (y - 18.5) / 13.7, hw = 1.9 * Math.pow(Math.max(0, 1 - t), .7) + .25;
      a = Math.max(a, Math.exp(-((x / hw) ** 2) * 2.2) * (.75 - .25 * t));
    }
    if (y > 2 && y <= 18.5) a = Math.max(a, Math.exp(-((x / .55) ** 2) * 2.5) * .45 * smooth(2, 9, y));
    const ring = Math.hypot(x / 2.6, (y - 17) / 2.4);
    a = Math.max(a, Math.exp(-(((ring - .95) / .25) ** 2)) * .12);
    const fade = (1 - smooth(31, 33.4, y)) * smooth(1.2, 3.5, y) * (1 - smooth(card.X1 * .8, card.X1, Math.abs(x)));
    a = clamp(a * fade);
    const w = 255 * (0.82 + .18 * clamp(a * 1.4));
    return a < .012 ? null : [w, w, w, a * 255];
  });
}
function trailSprite() {
  const card = CARD.gd_trail;
  return onCard(card, (x, y) => {
    // afterimage ribbon: brightest along the blade line, tapering to the butt
    const t = clamp((y - card.Y0) / (card.Y1 - card.Y0));
    const hw = .4 + 1.8 * t;
    const a = clamp(Math.exp(-((x / hw) ** 2) * 2.4) * (.15 + .6 * t * t) * (1 - smooth(.94, 1, t)));
    return a < .012 ? null : [255, 246, 220, a * 255];
  });
}

// ---- card rectangles (card units) and sprite sizes ---------------------------------------
export const CARD = {
  gd_wing_pri: boxOf(WF.pri), gd_wing_sec: boxOf(WF.sec), gd_wing_cov: boxOf(WF.cov),
  gd_shield: {X0: -15.6, X1: 15.6, Y0: -11.7, Y1: 11.7},
  gd_shield_eye: {X0: -10, X1: 10, Y0: -6, Y1: 6},
  gd_spear_head: {X0: -4.5, X1: 4.5, Y0: 8.2, Y1: 31.6},
  gd_spear_edge: {X0: -.4, X1: .4, Y0: 8.2, Y1: 31.6},
  gd_halo: {X0: -9.6, X1: 9.6, Y0: -9.6, Y1: 9.6},
  gd_halo_glow: {X0: -12, X1: 12, Y0: -12, Y1: 12},
  gd_crest: {X0: -5.4, X1: 5.4, Y0: -.8, Y1: 7.3},
  gd_crest_side: {X0: -3.2, X1: 1.6, Y0: 1.8, Y1: 6.6},
  gd_skirt_front: {X0: -4.6, X1: 4.6, Y0: -20.0, Y1: .8},
  gd_skirt_side: {X0: -2.2, X1: 8.2, Y0: -20.0, Y1: .8},
  gd_skirt_back: {X0: -6.2, X1: 6.2, Y0: -19.0, Y1: .5},
  gd_hip_wing: {X0: -7.2, X1: .8, Y0: -1.5, Y1: 4.5},
  gd_tail: {X0: -4.4, X1: 5.0, Y0: -20.2, Y1: 1.0},
  gd_belt: {X0: -4.2, X1: 4.2, Y0: -2.5, Y1: 3.6},
  gd_chest: {X0: -6.4, X1: 6.4, Y0: -.4, Y1: 13.0},
  gd_collar: {X0: -4.8, X1: 4.8, Y0: -1.6, Y1: 2.8},
  gd_spear_glow: {X0: -3.2, X1: 3.2, Y0: 1.0, Y1: 33.0},
  gd_trail: {X0: -3.0, X1: 3.0, Y0: 1.0, Y1: 32.0},
};
// [width, height] px; multiples of 16.
export const SIZE = {
  gd_wing_pri: [320, 320], gd_wing_sec: [224, 256], gd_wing_cov: [176, 128],
  gd_shield: [384, 288], gd_shield_eye: [160, 96],
  gd_spear_head: [160, 416], gd_spear_edge: [16, 416],
  gd_halo: [256, 256], gd_halo_glow: [128, 128],
  gd_crest: [256, 192], gd_crest_side: [96, 96],
  gd_skirt_front: [112, 256], gd_skirt_side: [128, 256], gd_skirt_back: [144, 224],
  gd_hip_wing: [128, 96], gd_tail: [112, 256], gd_belt: [128, 96],
  gd_chest: [160, 160], gd_collar: [128, 64],
  gd_spear_glow: [64, 320], gd_trail: [64, 320],
};
// Fix the aspect of auto-sized cards (wing tiers) so pixels stay square.
for (const k of ['gd_wing_pri', 'gd_wing_sec', 'gd_wing_cov']) {
  const c = CARD[k], [w, h] = SIZE[k], ppu = Math.min(w / (c.X1 - c.X0), h / (c.Y1 - c.Y0));
  const cx = (c.X0 + c.X1) / 2, cy = (c.Y0 + c.Y1) / 2, hw = w / ppu / 2, hh = h / ppu / 2;
  CARD[k] = {X0: cx - hw, X1: cx + hw, Y0: cy - hh, Y1: cy + hh};
}

// name -> [w, h, painter, translucent]
export function guardianSprites() {
  return {
    gd_wing_pri: [...SIZE.gd_wing_pri, wingSprite('pri')],
    gd_wing_sec: [...SIZE.gd_wing_sec, wingSprite('sec')],
    gd_wing_cov: [...SIZE.gd_wing_cov, wingSprite('cov')],
    gd_shield: [...SIZE.gd_shield, shieldSprite(false)],
    gd_shield_eye: [...SIZE.gd_shield_eye, shieldSprite(true, false)],
    gd_shield_eye_geo: [...SIZE.gd_shield_eye, shieldSprite(true, true)],
    gd_core: [32, 32, (u, v) => { const r = Math.hypot(u - .5, v - .5) * 2; return r > 1 ? TRANSPARENT : mix(C('#ffffff'), C('#fff1d8'), r); }],
    gd_spear_head: [...SIZE.gd_spear_head, spearHead(false)],
    gd_spear_head_e: [...SIZE.gd_spear_head, spearHead(true)],
    gd_spear_edge: [...SIZE.gd_spear_edge, spearEdge(false)],
    gd_spear_edge_e: [...SIZE.gd_spear_edge, spearEdge(true)],
    gd_spear_star: [64, 64, facetStar(PAL.butt, C('#8a2a1a'), C('#ff9a70'), .1)],
    gd_redstar: [64, 64, facetStar(PAL.red, PAL.redDark, C('#ff7a5a'), .02)],
    gd_blackstar: [64, 64, facetStar(C('#24181c'), C('#0c0608'), C('#5a4a50'), .02)],
    gd_spear_gem: [64, 64, facetStar(PAL.gem, PAL.gemDark, C('#ff8a5a'), .02)],
    gd_halo: [...SIZE.gd_halo, haloSprite()],
    gd_halo_glow: [...SIZE.gd_halo_glow, haloGlow(), true],
    gd_crest: [...SIZE.gd_crest, crestSprite()],
    gd_crest_back: [...SIZE.gd_crest, crestSprite(true)],
    gd_crest_side: [...SIZE.gd_crest_side, crestSide()],
    gd_skirt_front: [...SIZE.gd_skirt_front, skirtFront()],
    gd_skirt_side: [...SIZE.gd_skirt_side, skirtSide()],
    gd_skirt_back: [...SIZE.gd_skirt_back, skirtBack()],
    gd_hip_wing: [...SIZE.gd_hip_wing, hipWing()],
    gd_tail: [...SIZE.gd_tail, tailSprite()],
    gd_belt: [...SIZE.gd_belt, beltSprite()],
    gd_chest: [...SIZE.gd_chest, chestSprite(false)],
    gd_chest_back: [...SIZE.gd_chest, chestSprite(true)],
    gd_collar: [...SIZE.gd_collar, collarSprite()],
    gd_corrupt: [32, 32, corrupt(5)], gd_corrupt_b: [32, 32, corrupt(19)],
    gd_vox: [32, 32, voxel(false)], gd_vox_rune: [32, 32, voxel(true)],
    gd_white: [32, 32, flat('#f7efec', '#e6dbd8', 4)], gd_sleeve: [32, 32, sleeve()],
    gd_gold: [32, 32, goldTile(false)], gd_gold_dark: [32, 32, goldTile(true)],
    gd_gauntlet: [32, 64, gauntlet()],
    gd_joint: [32, 32, jointRing()],
    gd_talon: [16, 64, talon(false)], gd_talon_gold: [16, 64, talon(true)],
    gd_shaft: [16, 128, (u, v) => { let c = mix(C('#fff4cc'), C('#e2be78'), Math.abs(u - .5) * 1.8); if ((v * 24) % 1 < .07) c = mix(c, PAL.goldMid, .45); return c; }],
    gd_redcore: [32, 32, flat('#8a2418', '#5a120c', 21)],
    gd_dark: [32, 32, flat('#2a1418', '#1a0c10', 23)],
    gd_eye: [16, 16, () => PAL.eye],
    gd_spear_glow: [...SIZE.gd_spear_glow, spearGlow(), true],
    gd_trail: [...SIZE.gd_trail, trailSprite(), true],
  };
}

export const spriteId = name => 'rlk:mboss/guardian/' + name;
// Paint every sprite into the resource pack and merge them into the item atlas.
export function paintGuardianTextures(rp, only = null) {
  const dir = path.join(rp, 'assets/rlk/textures/mboss/guardian');
  fs.mkdirSync(dir, {recursive: true});
  const sprites = guardianSprites();
  for (const [name, [w, h, fn, translucent]] of Object.entries(sprites)) {
    if (only && !only.includes(name)) continue;
    fs.writeFileSync(path.join(dir, name + '.png'), png(w, h, translucent ? paintT(w, h, fn) : paint(w, h, fn)));
  }
  const atlasPath = path.join(rp, 'assets/minecraft/atlases/items.json');
  const atlas = fs.existsSync(atlasPath) ? JSON.parse(fs.readFileSync(atlasPath, 'utf8')) : {sources: []};
  const known = new Set(atlas.sources.map(s => s.sprite || s.resource));
  for (const name of Object.keys(sprites)) {
    const id = spriteId(name);
    if (!known.has(id)) atlas.sources.push({type: 'minecraft:single', resource: id});
  }
  fs.mkdirSync(path.dirname(atlasPath), {recursive: true});
  fs.writeFileSync(atlasPath, JSON.stringify(atlas, null, 2) + '\n');
  return Object.keys(sprites);
}
