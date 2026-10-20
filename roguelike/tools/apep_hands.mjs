// HANDS region of the 아펩의 오아시스 파수꾼 rig (plan R8: the hands change SHAPE with the stance; one display shows one model,
// so the shapes are discrete item-model variants swapped at fixed events with a 0.9 -> 1 scale pulse). 20 models:
//   A  p1_planted  3 broad pale lobed fingers on the floor, the palm sloping from the wrist, the square gold gem in a raised
//                  dark frame on the back of the hand, the gold cone on the wrist (model.md §3.3, v1 f290, v2 f2076)
//      p1_raised   the same claw hooked down like a bird head, the gem on top (v2 f417)
//      p3_fork     the forked leafy tip of the antler arm: three leaf blades + a back blade + the gold tip cone (§2.3 item 13)
//   B  p1_open     5 broad pointed petals (3 front, 2 side) arching from the ankle to the floor, raised centre vein,
//                  turned-up tips, dark outline; the cream-gold cone on a dark collar (model.md §3.4, v2 f2076, v1 f315)
//      p1_curl     the petals cupped up round the ankle (the lifted foot)
//      p3_curl     the fiddlehead foot: a frond running down to the water and curling up over itself, two side fronds,
//                  yellow tips, the cream cone (model_p3 §3 item 6, v6 f165)
//      p3_open     the big lobed leaf hand: two butter-yellow palmate leaves (lobes up, drooping forward) over the
//                  white-grey forked under-leaf fin (model_p3 §2.3 item 16, v6 f480 z_v6_0480_rhand)
//   C  p1_open / p1_curl  as B, Ø 1.5, the petals pointing back (rear feet)
//      p3_curl     the cupped leaf hand: tips up, the square-spiral glyph on its front, side walls, the cream cone (v5 f588)
// Frames (apep_pose FRAMES): world axes about the wrist joint, P1 variants as they sit in the CROUCH stance (planted on
// the floor: the A wrist 0.6 b, the B / C wrists 0.4 b up), P3 variants as they sit in the UPRIGHT stance. The P3 crawl
// orients its hands through the IK hand eulers (hf_*), so a P3 hand shows the same in the crawl as authored (the B / C
// curls are the crawl feet: their lowest point stays <= 0.45 b under the wrist).
//
// Construction: every leaf, petal and finger is a SHEET (sheet() below): a flat painted shape (alpha-cut cards on both
// faces over a greedy-meshed core) cut into bands across its run, each band turned by a multiple of 22.5 degrees about
// the sheet's across axis (one element rotation; bands past 45 degrees switch base plane), so a petal arches, a finger
// curls and a fiddlehead rolls up in 3D. Cones are square spikes (four 22.5-degree triangle cards).
import {rockBox, toUnits, mirrorX, stroke, sdUnion, sdPoly} from './mboss_shape_lib.mjs';
import {faceEl, faceOfDir, rotA} from './mboss_model_lib.mjs';
import {PART_SCALE} from './apep_pose.mjs';
import {PAL, C, clamp, smooth, mix, N as NS, lift, sink, autoSlot, sprite, r16, ramp, TRANSPARENT} from './apep_materials.mjs';

export const REGION = 'hands';
export const PARTS = ['a_hand_l', 'a_hand_r', 'b_hand_l', 'b_hand_r', 'c_hand_l', 'c_hand_r'];
export const VARIANTS = {a: ['p1_planted', 'p1_raised', 'p3_fork'], b: ['p1_open', 'p1_curl', 'p3_curl', 'p3_open'], c: ['p1_open', 'p1_curl', 'p3_curl']};
const SP = {};

// ---- vectors ---------------------------------------------------------------------------------------------------------------
const D2R = Math.PI / 180;
const AXV = s => { if (Array.isArray(s)) return s; const v = [0, 0, 0]; v['xyz'.indexOf(s[1])] = s[0] === '-' ? -1 : 1; return v; };
const add = (a, b) => a.map((x, i) => x + b[i]), sub = (a, b) => a.map((x, i) => x - b[i]), sc = (v, k) => v.map(x => x * k);
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const crs = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const axName = v => (Math.abs(v[0]) > .5 ? 'x' : Math.abs(v[1]) > .5 ? 'y' : 'z');
const clean = v => v.map(x => (Math.abs(x) < 1e-9 ? 0 : x));

// ---- sprites ---------------------------------------------------------------------------------------------------------------
// A sheet sprite: painter fn(a, s) over rect {a0, a1, s0, s1} (sprite x runs a0 -> a1, sprite y runs s1 (top) -> s0).
const sheetSprite = (name, rect, fn, ppb, forms) => {
  if (!SP[name]) { const w = r16((rect.a1 - rect.a0) * ppb), h = r16((rect.s1 - rect.s0) * ppb); SP[name] = sprite(w, h, ppb, (x, y) => fn(rect.a0 + x * (rect.a1 - rect.a0), rect.s1 - y * (rect.s1 - rect.s0)) || TRANSPARENT, forms, 'hands'); }
  return name;
};
// a small flat edge tile (the core sides of the sheets: the visible rim from oblique views)
const edgeTile = (name, R, v0, v1, forms) => { if (!SP[name]) SP[name] = sprite(16, 16, 32, (x, y) => R(clamp(v0 + (v1 - v0) * y + .08 * (NS.e(x * 9, y * 9) - .5))), forms, 'hands'); return name; };

// ---- the bent sheet ------------------------------------------------------------------------------------------------------
// Flat coordinates (a across, s along the run): the unbent point is o + U a + R s; N (default U x R) is the sheet's
// normal. bands [{s, ang, half, core}]: band k runs from bands[k].s to bands[k + 1].s (the last to rect.s1); ang = the
// band's direction in degrees from R toward -N (multiples of 22.5, any size: 0 flat, 90 turned onto -N, 180 back),
// half = half thickness, off = the mid-plane's offset along the band normal (a cover plate on a base sheet). Cards on both faces show the sprite (alpha-cut); core boxes (the eroded shape) carry the edge
// tile on their sides. Interior band ends overlap by the bevel wedge so the joints never open. Frames of the bands are
// pushed to `frames` (for attachments: frame.X(a, s, h) = the posed point before the band's rotation, frame.rot).
function sheet({o = [0, 0, 0], U, R, N = null, rect, sd, tex, texM = null, edge, bands, cell = .07, inset = .55, eps = .01, seed = 0, shade = false, frames = null, anchor = 0}) {
  U = AXV(U); R = AXV(R); N = N ? AXV(N) : crs(U, R);
  if (bands[0].s < rect.s0 - 1e-9) throw new Error('sheet: first band before the sprite rect');
  const els = [];
  // band start points (the anchor band starts at its unbent place o + R s)
  const dirOf = th => add(sc(R, Math.cos(th * D2R)), sc(N, -Math.sin(th * D2R)));
  const starts = [add(o, sc(R, bands[0].s))];
  for (let k = 0; k + 1 < bands.length; k++) starts.push(add(starts[k], sc(dirOf(bands[k].ang || 0), bands[k + 1].s - bands[k].s)));
  const shift = sub(add(o, sc(R, bands[anchor].s)), starts[anchor]);
  bands.forEach((b, k) => {
    const P = add(starts[k], shift);
    const s0 = b.s, s1 = k + 1 < bands.length ? bands[k + 1].s : rect.s1, th = b.ang || 0, h = b.half ?? .05;
    const tb = Math.round(th / 90) * 90, rho = th - tb, cb = Math.round(Math.cos(tb * D2R)), sb = Math.round(Math.sin(tb * D2R));
    const Db = clean(add(sc(R, cb), sc(N, -sb))), Nb = clean(add(sc(R, sb), sc(N, cb)));
    const t = th * D2R, Dk = add(sc(R, Math.cos(t)), sc(N, -Math.sin(t)));
    let rot = null;
    if (Math.abs(rho) > 1e-6) {
      const ax = axName(U), ok = d => Math.hypot(...sub(rotA(ax, d, Db), Dk)) < 1e-6;
      const deg = ok(rho) ? rho : ok(-rho) ? -rho : null;
      if (deg === null) throw new Error('sheet: no rotation for ' + th);
      rot = [ax, deg, P.slice()];
    }
    const thP = k > 0 ? bands[k - 1].ang || 0 : th, thN = k + 1 < bands.length ? bands[k + 1].ang || 0 : th;
    const off = b.off || 0;
    const ovL = k > 0 ? (h + Math.abs(off) + eps) * Math.tan(Math.abs(th - thP) * D2R / 2) + .004 : 0;
    const ovR = k + 1 < bands.length ? (h + Math.abs(off) + eps) * Math.tan(Math.abs(thN - th) * D2R / 2) + .004 : 0;
    const sa = Math.max(rect.s0, s0 - ovL), sz = Math.min(rect.s1, s1 + ovR), Pk = P.slice();
    const X = (a, s, hh) => add(add(add(Pk, sc(U, a)), sc(Db, s - s0)), sc(Nb, hh + off));
    if (frames) frames.push({s0, s1, P: Pk, Db, Nb, U, rot, h, X, ang: th});
    // the shape's across extent in this band
    let amin = Infinity, amax = -Infinity;
    const da = (rect.a1 - rect.a0) / 200;
    for (let j = 0; j <= 12; j++) {
      const s = sa + (sz - sa) * j / 12;
      for (let i = 0; i <= 200; i++) { const a = rect.a0 + i * da; if (sd(a, s) < da) { if (a < amin) amin = a; if (a > amax) amax = a; } }
    }
    if (amin < amax) {
      amin = Math.max(rect.a0, amin - da); amax = Math.min(rect.a1, amax + da);
      const fn = p => { const d = sub(p, Pk), a = dot(d, U), s = s0 + dot(d, Db); return [16 * (a - rect.a0) / (rect.a1 - rect.a0), 16 * (rect.s1 - s) / (rect.s1 - rect.s0)]; };
      // the +N card shows tex, the -N card texM (the leaf's underside; default the same sprite)
      const card = (hh, dirs) => faceEl([X(amin, sa, hh), X(amax, sz, hh)], Object.fromEntries(dirs.map(([d, tx]) => [faceOfDir(d), {tex: tx, fn}])), {rot, shade});
      const tM = texM || tex;
      if (b.core === false) els.push(card(0, [[Nb, tex], [sc(Nb, -1), tM]]));
      else {
        els.push(card(h + eps, [[Nb, tex]]), card(-h - eps, [[sc(Nb, -1), tM]]));
        const er = inset * cell, na = Math.max(1, Math.round((amax - amin) / cell)), ns = Math.max(1, Math.round((sz - sa) / cell));
        const ca = (amax - amin) / na, cs = (sz - sa) / ns;
        const inside = Array.from({length: ns}, (_, j) => Array.from({length: na}, (_, i) => sd(amin + (i + .5) * ca, sa + (j + .5) * cs) < -er));
        const used = inside.map(r => r.map(() => false));
        let n = 0;
        for (let j = 0; j < ns; j++) for (let i = 0; i < na; i++) {
          if (!inside[j][i] || used[j][i]) continue;
          let i1 = i; while (i1 + 1 < na && inside[j][i1 + 1] && !used[j][i1 + 1]) i1++;
          let j1 = j; const rowOk = jj => { for (let x = i; x <= i1; x++) if (!inside[jj][x] || used[jj][x]) return false; return true; };
          while (j1 + 1 < ns && rowOk(j1 + 1)) j1++;
          for (let jj = j; jj <= j1; jj++) for (let x = i; x <= i1; x++) used[jj][x] = true;
          const lo = X(amin + i * ca, sa + j * cs, -h), hi = X(amin + (i1 + 1) * ca, sa + (j1 + 1) * cs, h);
          els.push(rockBox(lo, hi, edge, {rot, seed: seed * 97 + k * 13 + (n++), drop: [faceOfDir(Nb), faceOfDir(sc(Nb, -1))]}));
        }
      }
    }
    void Dk;
  });
  return els;
}
// a box on a sheet band (band-local a / s ranges, h0..h1 off the mid-plane), turned with the band
const boxOn = (f, a0, a1, s0, s1, h0, h1, tex, seed = 0) => rockBox(f.X(a0, s0, h0), f.X(a1, s1, h1), tex, {rot: f.rot, seed});
const posed = (f, p) => (f.rot ? add(f.rot[2], rotA(f.rot[0], f.rot[1], sub(p, f.rot[2]))) : p);
const frameAt = (frames, s) => frames.find(f => s >= f.s0 - 1e-9 && s <= f.s1 + 1e-9) || frames[frames.length - 1];

// scale a finished element list by f about the point c (blocks, hand frame): grows a hand without touching its part scale
const scaleEls = (els, f, c = [0, 0, 0]) => {
  const m = v => v.map((x, i) => { const ci = i === 0 ? 8 - c[0] : 8 + c[i]; return Math.round((ci + (x - ci) * f) * 1e4) / 1e4; });
  return els.map(e => { const o = {...e, from: m(e.from), to: m(e.to)}; if (e.rotation) o.rotation = {...e.rotation, origin: m(e.rotation.origin)}; return o; });
};

// ---- square spikes (the cones) --------------------------------------------------------------------------------------------
// Four triangle cards leaning 22.5 degrees round axis A ('x' | 'y' | 'z', dir +-1) from the base centre c; base half
// width b, height b / tan 22.5. The sprite is the cone painted apex up.
const TAN22 = Math.tan(22.5 * D2R), SLANT = 1 / Math.sin(22.5 * D2R);
function spike(c, b, tex, {axis = 'y', dir = 1} = {}) {
  const iA = 'xyz'.indexOf(axis), others = [0, 1, 2].filter(i => i !== iA), els = [], sl = b * SLANT;
  const eA = [0, 0, 0]; eA[iA] = dir;
  for (const iB of others) for (const sg of [1, -1]) {
    const iC = others.find(i => i !== iB), cName = 'xyz'[iC];
    const eB = [0, 0, 0]; eB[iB] = sg;
    const deg = [22.5, -22.5].find(d => dot(rotA(cName, d, eA), eB) < 0);
    const p0 = c.slice(), p1 = c.slice();
    p0[iB] = p1[iB] = c[iB] + sg * b; p0[iC] = c[iC] - b; p1[iC] = c[iC] + b; p1[iA] = c[iA] + dir * sl;
    const piv = c.slice(); piv[iB] = c[iB] + sg * b;
    const fn = p => [16 * (p[iC] - (c[iC] - b)) / (2 * b), 16 * (1 - Math.abs(p[iA] - c[iA]) / sl)];
    els.push(faceEl([p0, p1], {[faceOfDir(eB)]: {tex, fn}}, {rot: [cName, deg, piv], shade: true}));
  }
  return els;
}
const spikeSprite = (name, R, forms) => {
  if (!SP[name]) SP[name] = sprite(32, 64, 48, (x, y) => {
    const half = .5 * y; if (Math.abs(x - .5) > half + .01) return TRANSPARENT;
    const u = (x - .5) / Math.max(.02, half);       // -1 .. 1 across the face
    let c = R(clamp(.1 + .45 * y + .22 * (u + 1) / 2 + .05 * (NS.b(x * 9, y * 9) - .5)));
    if (u < -.55 && y > .15) c = lift(c, .3);        // the lit edge
    if (Math.abs(u) > .9 && y > .1) c = sink(c, .25);
    return c;
  }, forms, 'hands');
  return name;
};

// ---- painters ----------------------------------------------------------------------------------------------------------------
// local frame of a painted leaf / petal / finger: base point (a, s), unit direction (da, ds), length L
const along = (ax, a, s) => { const ra = a - ax.a, rs = s - ax.s; return {t: (ra * ax.da + rs * ax.ds) / ax.L, x: ra * ax.ds - rs * ax.da}; };
// P1 pale petal: light centre, darker flanks, a raised centre vein (lit flank + shadow flank), side veins, a pale rim
// inside the dark outline, the root shaded under the ankle
const petalPaint = (sd, ax, {R = PAL.p1_bark, line = PAL.p1_line, root = .22, base = .1, seed = 'c', soft = false} = {}) => (a, s) => {
  const d = sd(a, s); if (d > 0) return null;
  const {t, x} = along(ax, a, s), w = Math.max(.03, Math.abs(x) - d), xn = clamp(x / w, -1, 1);
  let v = base + .2 * xn * xn + .1 * (NS[seed](a * 6, s * 6) - .5) + .3 * clamp(1 - t / root) ** 2 + .1 * clamp((t - .75) / .25);
  if (t > .1 && t < .88) { if (xn > -.1 && xn <= .0) v -= .08; else if (xn > 0 && xn < .1) v += .16; }
  const sv = Math.abs(((t * 5 - Math.abs(xn) * 1.6) % 1 + 1) % 1 - .5);
  if (sv < .05 && Math.abs(xn) > .2 && Math.abs(xn) < .8 && t > .2) v += .08;
  let c = R(clamp(v));
  if (soft) { if (d > -.03) c = mix(c, R(.55), .55 + .35 * clamp(-xn)); else if (d > -.055) c = lift(c, .3); }   // a raised plate: shadowed rim, lit bevel
  else if (d > -.028) c = mix(c, line(.8), .92); else if (d > -.05) c = lift(c, .35);
  return c;
};
// P3 leaf (yellow lobed hands, fronds): lighter lobes, veins from the base, a lime band inside the dark outline
const leafPaint = (sd, ax, {R = PAL.p3_leafhand, line = PAL.p3_line, rim = PAL.p3_lime, base = .12, tipK = .2, veins = 7, seed = 'd', tipCol = null} = {}) => (a, s) => {
  const d = sd(a, s); if (d > 0) return null;
  const {t, x} = along(ax, a, s);
  let v = base + .22 * clamp(1 - t * 1.4) + .12 * (NS[seed](a * 5, s * 5) - .5) - tipK * clamp(t - .55);
  const ang = Math.atan2(x, Math.max(.02, t * ax.L)), vs = Math.abs(((ang * veins / Math.PI) % 1 + 1) % 1 - .5);
  let c = R(clamp(v));
  if (Math.abs(x) < .018 && t > .02) c = mix(c, line(.3), .55);
  else if (vs < .06 && t > .12) c = mix(c, line(.35), .35);
  if (tipCol && t > .8) c = mix(c, tipCol, clamp((t - .8) / .15) * .75);
  if (d > -.025) c = mix(c, line(.75), .92); else if (d > -.06) c = mix(c, rim(.35), .55);
  return c;
};

// ---- A phase 1: the claw (flat coords a = Z across, s = X outward from the wrist; normal +Y) ---------------------------------
// three long pointed fingers fanned from the knuckle line over a palm that starts under the forearm's end, a back-of-hand
// shell plate with a knuckle tongue over each finger root, and a wrist cuff plate over the palm root: the overlapping pale
// plates with dark contour rims of model.md §3.3 (v1 f285 / f290, v2 f2076: long flat blades, sharp tips, deep notches)
// a pointed blade: widest at m (fraction of L), the root r0 x W wide; the end a point (q = 1 straight, q < 1 rounded);
// hook bends the centre line sideways near the tip (fraction of L at the tip)
const bladeW = (t, W, m, r0, p, q) => (t < 0 || t > 1 ? -1 : t < m ? W * (r0 + (1 - r0) * Math.sin(Math.PI / 2 * t / m) ** .9) : W * Math.max(0, 1 - ((t - m) / (1 - m)) ** p) ** q);
const bladeShape = (L, W, phi = 0, {m = .4, r0 = .7, p = 1.4, q = .9, hook = 0} = {}) => {
  const cs = Math.cos(phi), sn = Math.sin(phi);
  return (a, s) => {
    const v = a * sn + s * cs, t = v / L, u = a * cs - s * sn - hook * L * clamp((t - .55) / .45) ** 2;
    const out = t < 0 ? -v : t > 1 ? v - L : 0, w = bladeW(clamp(t), W, m, r0, p, q);
    return out > 0 ? Math.max(out, Math.abs(u) - Math.max(0, w)) : Math.abs(u) - w;
  };
};
// [a, s at the knuckle, fan (deg toward +a), length, half width, hook]
const FING = [[.25, .28, 7, 1.16, .15, -.05], [-.03, .31, -4, 1.24, .17, 0], [-.31, .27, -15, 1.1, .16, .05]];
const clawParts = k => {
  const F = FING.map(([a0, s0, deg, L, W, hook]) => { const sd = bladeShape(L * k, W, deg * D2R, {hook}); return {a0, s0, deg, L: L * k, sd: (a, s) => sd(a - a0, s - s0)}; });
  const palm = sdPoly([[-.18, -.3], [.14, -.3], [.24, .2], [.3, .55], [-.46, .55], [-.4, .18]]);
  const T = FING.map(([a0, s0, deg, , W]) => { const sd = bladeShape(.3 * k + .08, .7 * W, deg * D2R, {m: .3, r0: .9, p: 2, q: .6}); return (a, s) => sd(a - a0, s - s0 + .12); });
  const back = sdPoly([[-.25, .02], [.22, .02], [.28, .4], [-.37, .4]]);
  const cuff = sdPoly([[-.17, -.24], [.13, -.24], [.2, .12], [-.26, .12]]);
  return {F, sd: sdUnion((a, s) => palm(a, s) - .05, ...F.map(f => f.sd)), cover: sdUnion((a, s) => back(a, s) - .05, ...T), cuff: (a, s) => cuff(a, s) - .05};
};
// pale bark: each finger folded along its axis (a lit half, a shaded half, a dark crease), contour lines running inside
// the outline (the plate rims), rings on the palm and the plates, the root shaded under the forearm
const clawPaint = (F, sd, top) => (a, s) => {
  const d = sd(a, s); if (d > 0) return null;
  let best = null;
  for (const f of F) { const p = f.deg * D2R, ra = a - f.a0, rs = s - f.s0, t = (ra * Math.sin(p) + rs * Math.cos(p)) / f.L, x = ra * Math.cos(p) - rs * Math.sin(p); if (t > -.1 && (!best || Math.abs(x) < Math.abs(best.x))) best = {t, x}; }
  let v = (top ? .06 : .14) + .07 * (NS.a(a * 7, s * 7) - .5) + .22 * clamp((.0 - s) / .3);
  if (!top && best && best.t > .02 && s > .45) {
    const w = Math.max(.03, Math.abs(best.x) - d), xn = clamp(best.x / w, -1, 1);
    v += xn < 0 ? .03 + .1 * xn * xn : .2 + .06 * xn;                  // the lit half (-x of the axis) and the shaded half
    v += .08 * clamp((best.t - .75) / .25);
    if (Math.abs(xn) < .09 && best.t < .9) v += .16;                     // the crease
  } else { const r = Math.hypot(a * 1.2 + .05, s - .22), ring = Math.abs(((r * 9 + .8 * NS.b(a * 3, s * 3)) % 1) - .5); if (ring < .06 && r > .07) v += .14; }
  let c = PAL.p1_bark(clamp(v));
  if (d > -.026) c = mix(c, PAL.p1_line(.8), .92);
  else if (d > -.048) c = lift(c, .32);
  else if (Math.abs(d + .095) < .011) c = mix(c, PAL.p1_bark(.85), .6);   // the inner contour rim
  return c;
};
const EDGE_P1 = () => edgeTile('h_edge_p1d', PAL.p1_bark, .5, .8, 'p1');
// the planted claw is drawn along the forearm: the forearm reaches the wrist heading ~30 degrees forward of +X (CROUCH), so
// the flat design (fingers along +s) is turned by CLAW_TURN toward -a (the model's -Z is the boss's front) before it is cut
// into bands along X
const CLAW_TURN = -30 * D2R;
const turnFlat = (f, th = CLAW_TURN) => { const c = Math.cos(th), n = Math.sin(th); return (a, s) => f(a * c - s * n, a * n + s * c); };
const turnPt = (a, s, th = CLAW_TURN) => { const c = Math.cos(th), n = Math.sin(th); return [a * c + s * n, -a * n + s * c]; };
function clawPlanted() {
  const {F, sd: sd0, cover: cover0, cuff: cuff0} = clawParts(1);
  const sd = turnFlat(sd0), cover = turnFlat(cover0), cuff = turnFlat(cuff0);
  const rect = {a0: -1.2, a1: .8, s0: -.5, s1: 1.45};
  const tex = sheetSprite('h_claw', rect, turnFlat(clawPaint(F, sd0, false)), 40, 'p1');
  const texC = sheetSprite('h_clawc', {...rect, s1: .9}, turnFlat(clawPaint(F, cover0, true)), 40, 'p1');
  const texK = sheetSprite('h_clawk', {...rect, s1: .3}, turnFlat(clawPaint(F, cuff0, true)), 40, 'p1');
  const edge = EDGE_P1();
  const B = [[-.5, 45, .1], [.02, 22.5, .085], [.3, 0, .068]];
  const o = [0, -.02, 0], fr = [];
  const els = sheet({o, U: '+z', R: '+x', rect, sd, tex, edge: edgeTile('h_edge_p1l', PAL.p1_line, .35, .6, 'p1'), seed: 401, cell: .075, inset: 1.3, bands: B.map(([s, ang, half]) => ({s, ang, half}))});
  els.push(...sheet({o, U: '+z', R: '+x', rect: {...rect, s1: .9}, sd: cover, tex: texC, edge, seed: 405, frames: fr, cell: .08, inset: .8,
    bands: B.filter(b => b[0] < .9).map(([s, ang, half]) => ({s, ang, half: .03, off: half + .036}))}));
  els.push(...sheet({o, U: '+z', R: '+x', rect: {...rect, s1: .3}, sd: cuff, tex: texK, edge, seed: 406, cell: .09, inset: .8,
    bands: B.filter(b => b[0] < .3).map(([s, ang, half]) => ({s, ang, half: .028, off: half + .1}))}));
  // the square gold gem in a raised dark frame on the knuckles, the gold cone on a dark collar on the back of the wrist
  // (it stands out of the forearm's end, v1 f290)
  const [ag, sg] = turnPt(-.03, .54), fg = frameAt(fr, sg), hh = fg.h + .008;
  els.push(boxOn(fg, ag - .15, ag + .15, sg - .14, sg + .14, hh, hh + .05, 'g_plate', 402), boxOn(fg, ag - .095, ag + .095, sg - .095, sg + .095, hh + .05, hh + .1, 'p1_gem', 403));
  const [ac, sc0] = turnPt(-.06, .22), fc = frameAt(fr, sc0), top = posed(fc, fc.X(ac, sc0, fc.h + .04));
  els.push(rockBox([top[0] - .16, top[1] - .03, top[2] - .16], [top[0] + .16, top[1] + .05, top[2] + .16], 'g_plate', {seed: 404}));
  els.push(...spike([top[0], top[1] + .05, top[2]], .155, spikeSprite('h_spk_gold1', PAL.p1_gold, 'p1')));
  return els;
}
// the raised claw: the hand hooked down like a bird head (v2 f417): the back of the hand runs on out of the forearm and
// rolls over the knuckles, the three fingers hang down and curl in; the gem sits on the crown of the roll like an eye
function clawRaised() {
  const k = .78, {F, sd, cover} = clawParts(k);
  const rect = {a0: -.72, a1: .56, s0: -.3, s1: 1.26};
  const tex = sheetSprite('h_claw_r', rect, clawPaint(F, sd, false), 40, 'p1');
  const texC = sheetSprite('h_clawc_r', {...rect, s1: .82}, clawPaint(F, cover, true), 40, 'p1');
  const edge = EDGE_P1();
  const B = [[-.3, -22.5, .1], [.12, 22.5, .09], [.36, 67.5, .075], [.58, 112.5, .06], [.88, 135, .05]];
  const o = [0, .1, 0], fr = [];
  const els = sheet({o, U: '+z', R: '+x', rect, sd, tex, edge: edgeTile('h_edge_p1l', PAL.p1_line, .35, .6, 'p1'), seed: 407, cell: .07, inset: .9, bands: B.map(([s, ang, half]) => ({s, ang, half}))});
  els.push(...sheet({o, U: '+z', R: '+x', rect: {...rect, s1: .82}, sd: cover, tex: texC, edge, seed: 408, frames: fr, cell: .08, inset: .8,
    bands: B.filter(b => b[0] < .8).map(([s, ang, half]) => ({s, ang, half: .03, off: half + .036}))}));
  const sg = .3, fg = frameAt(fr, sg), hh = fg.h + .008;
  els.push(boxOn(fg, -.15, .15, sg - .13, sg + .13, hh, hh + .05, 'g_plate', 409), boxOn(fg, -.095, .095, sg - .09, sg + .09, hh + .05, hh + .1, 'p1_gem', 410));
  const sc0 = -.12, fc = frameAt(fr, sc0), top = posed(fc, fc.X(-.02, sc0, fc.h + .04));
  els.push(rockBox([top[0] - .13, top[1] - .03, top[2] - .13], [top[0] + .13, top[1] + .05, top[2] + .13], 'g_plate', {seed: 411}));
  els.push(...spike([top[0], top[1] + .05, top[2]], .12, spikeSprite('h_spk_gold1', PAL.p1_gold, 'p1')));
  return els;
}

// ---- B / C phase 1: the petal hand ------------------------------------------------------------------------------------------
// one petal: flat coords along its run R (s from the ankle out), across U, normal +Y; W = the widest half width. Broad and
// spoon-like (v2 f2076 / f417): widest past the middle, a blunt rounded end with a small point
const petalW = (t, W) => (t < 0 || t > 1 ? -1 : W * Math.pow(Math.sin(Math.PI * (.14 + .86 * t)), .42));
const petalShape = (L, W, phi = 0) => {
  const cs = Math.cos(phi), sn = Math.sin(phi);
  return (a, s) => { const u = a * cs - s * sn, v = a * sn + s * cs, t = (v - .02) / L, out = t < 0 ? -t * L : t > 1 ? (t - 1) * L : 0; return out > 0 ? Math.max(out, Math.abs(u) - Math.max(0, petalW(clamp(t), W))) : Math.abs(u) - petalW(t, W); };
};
// the narrow lanceolate shape of leaf blades, bracts and tips (P3) and the raised petal ridge
const lanceW = (t, W) => (t < 0 || t > 1 ? -1 : W * Math.pow(Math.sin(Math.PI * (.16 + .84 * t)), .62));
const tipShape = (L, W, phi = 0) => {
  const cs = Math.cos(phi), sn = Math.sin(phi);
  return (a, s) => { const u = a * cs - s * sn, v = a * sn + s * cs, t = (v - .02) / L, out = t < 0 ? -t * L : t > 1 ? (t - 1) * L : 0; return out > 0 ? Math.max(out, Math.abs(u) - Math.max(0, lanceW(clamp(t), W))) : Math.abs(u) - lanceW(t, W); };
};
// petal runs per direction: [U, R] with the normal forced to +Y (mirrored runs reuse the sprite)
const RUNS = {f: ['+x', '-z'], b: ['-x', '+z'], l: ['+z', '+x'], r: ['+z', '-x']};
function petalFoot(k, back, curl) {
  // k = size (B 1.0, C 0.83); back = the petals point back (+Z: the rear feet); curl = cupped up (the lifted foot)
  // the core sides read as the petals' dark contour from low views (v2 f2076: dark outlines), not as pale steps
  const L = 1.04 * k, edge = edgeTile('h_edge_p1l', PAL.p1_line, .35, .6, 'p1'), els = [];
  const fwd = back ? 'b' : 'f', fr = [], cz = (back ? .2 : -.2) * k;
  // [run, phi (deg, toward +a), W, mid-plane lift of the root (layering)]
  // (the three forward petals share a frame: distinct root lifts keep their overlapping roots from z-fighting)
  const P = [[fwd, 0, .34, .075], [fwd, 40, .3, .015], [fwd, -40, .3, .037], ['l', back ? 24 : -24, .27, 0], ['r', back ? 24 : -24, .27, .022]];
  for (const [run, phiDeg, W0, dy] of P) {
    const phi = phiDeg * D2R, W = W0 * k, cs = Math.cos(phi);
    const sd = petalShape(L, W, phi), ext = L * cs + W * Math.abs(Math.sin(phi)) + .04;
    const rect = {a0: -(W + L * Math.abs(Math.sin(phi)) + .04), a1: W + L * Math.abs(Math.sin(phi)) + .04, s0: 0, s1: ext};
    const ax = {a: 0, s: .02, da: Math.sin(phi), ds: cs, L};
    const name = `h_petal${k < 1 ? 'c' : 'b'}${phiDeg ? (Math.abs(phiDeg) === 40 ? '_d' : '_s') : ''}`;
    // one sprite per petal kind: the mirrored runs (right side) reuse the left one through a negative phi on the same U
    const sdS = phiDeg < 0 ? petalShape(L, W, -phi) : sd;
    const tex = sheetSprite(name, rect, petalPaint(sdS, phiDeg < 0 ? {...ax, da: -ax.da} : ax, {seed: k < 1 ? 'd' : 'c'}), 40, 'p1');
    const [U, R] = RUNS[run];
    const mirrorU = phiDeg < 0;   // mirror the across axis instead of the sprite
    const f = x => x * ext;
    // open: the root drops steeply out of the ankle collar, the petal flattens onto the floor, the tip turns up
    const bands = curl
      ? [{s: 0, ang: 22.5, half: .05}, {s: f(.24), ang: -22.5, half: .05}, {s: f(.44), ang: -67.5, half: .045}, {s: f(.68), ang: -90, half: .04}]
      : [{s: 0, ang: 45, half: .05}, {s: f(.22), ang: 22.5, half: .05}, {s: f(.46), ang: 0, half: .045}, {s: f(.8), ang: -22.5, half: .04}];
    // the root height: the lowest joint 0.02 b over the floor 0.4 b under the wrist
    let drop = 0, low = 0; for (let i = 0; i < bands.length; i++) { const L_ = (i + 1 < bands.length ? bands[i + 1].s : ext) - bands[i].s; drop += L_ * Math.sin(bands[i].ang * D2R); low = Math.max(low, drop); }
    const y = curl ? -.12 + dy : -.38 + .06 + low + dy;
    const Uu = mirrorU ? sc(AXV(U), -1) : U;
    els.push(...sheet({o: [0, y, cz], U: Uu, R, N: '+y', rect, sd: sdS, tex, edge, bands, seed: 421 + els.length, frames: fr, cell: .08, inset: 1.0}));
    // the raised centre ridge (the petal's convex middle and its vein): a narrow blade laid along the petal's axis
    const sdC = tipShape(.8 * L, .32 * W, phiDeg < 0 ? -phi : phi);
    const texC = sheetSprite(name + '_c', rect, petalPaint(sdC, phiDeg < 0 ? {...ax, da: -ax.da, L: .8 * L} : {...ax, L: .8 * L}, {seed: k < 1 ? 'd' : 'c', base: .02, root: .3, soft: true}), 32, 'p1');
    els.push(...sheet({o: [0, y, cz], U: Uu, R, N: '+y', rect, sd: sdC, tex: texC, edge: edgeTile('h_edge_p1', PAL.p1_bark, .3, .55, 'p1'), cell: .1, seed: 471 + els.length, bands: bands.map(b => ({...b, half: .022, off: b.half + .026}))}));
  }
  // the ankle: a pale palm disc closing the centre between the petal roots, a dark collar ring under the cream-gold cone
  const cc = cz + (back ? .14 : -.14) * k;
  const disc = (a, s) => Math.hypot(a, s) - .3 * k;
  els.push(...sheet({o: [0, curl ? -.02 : .0, cz], U: '+x', R: '-z', N: '+y', rect: {a0: -.32 * k, a1: .32 * k, s0: -.32 * k, s1: .32 * k}, sd: disc,
    tex: sheetSprite(`h_palm${k < 1 ? 'c' : 'b'}`, {a0: -.32 * k, a1: .32 * k, s0: -.32 * k, s1: .32 * k}, petalPaint(disc, {a: 0, s: -.3 * k, da: 0, ds: 1, L: .6 * k}, {root: .01, base: .2}), 40, 'p1'),
    edge, bands: [{s: -.32 * k, ang: 0, half: .05}], seed: 431, cell: .1}));
  els.push(rockBox([-.14 * k, .03, cc - .14 * k], [.14 * k, .1, cc + .14 * k], 'g_plate', {seed: 432}));
  els.push(...spike([0, .1, cc], .14 * k, spikeSprite('h_spk_cream1', PAL.p1_cone, 'p1')));
  return els;
}

// ---- P3 leaf shapes ----------------------------------------------------------------------------------------------------------
// a rounded lobe with a small apex (the lobes of the leaf hands): flat coords from its base, along phi (rad, toward +a)
const lobeW = (t, W) => (t < 0 || t > 1 ? -1 : W * Math.pow(Math.sin(Math.PI * (.08 + .92 * Math.pow(t, .8))), .45));
const lobeShape = (L, W, phi = 0) => {
  const cs = Math.cos(phi), sn = Math.sin(phi);
  return (a, s) => { const u = a * cs - s * sn, v = a * sn + s * cs, t = v / L, out = t < 0 ? -v : t > 1 ? v - L : 0; return out > 0 ? Math.max(out, Math.abs(u) - Math.max(0, lobeW(clamp(t), W))) : Math.abs(u) - lobeW(t, W); };
};
// a palmate leaf: lobes radiating from the base point b, joined by a fan polygon; flat coords a = X, s = Y
const palmate = (b, lobes, fan) => {
  const L = lobes.map(([deg, len, w]) => { const p = deg * D2R; return {p, len, w, sd: lobeShape(len, w, p)}; });
  const core = sdPoly(fan);
  return {b, L, sd: (a, s) => Math.min(core(a, s) - .03, ...L.map(l => l.sd(a - b[0], s - b[1])))};
};
// butter-yellow lobes: veins from the base along each lobe, lighter lobe ends, a lime band inside the dark outline
function lobedPaint(P, {R = PAL.p3_leafhand, pale = false} = {}) {
  return (a, s) => {
    const d = P.sd(a, s); if (d > 0) return null;
    const ra = a - P.b[0], rs = s - P.b[1], r = Math.hypot(ra, rs);
    let bx = Infinity, bt = 0, bsx = 0;
    for (const l of P.L) { const da = Math.sin(l.p), ds = Math.cos(l.p), t = (ra * da + rs * ds) / l.len, x = ra * ds - rs * da; if (Math.abs(x) < bx && t > -.05) { bx = Math.abs(x); bsx = x; bt = t; } }
    let v = (pale ? .02 : .1) + .2 * clamp(.55 - r / 1.6) + .08 * (NS.d(a * 5, s * 5) - .5) - .12 * clamp(bt - .55) + .08 * clamp(bx / .3);
    let c = R(clamp(v));
    if (bx < .022 && bt > .02 && bt < .9) c = mix(c, PAL.p3_line(.3), .6);
    else if (bsx > 0 && bx < .05 && bt > .05 && bt < .85) c = lift(c, .2);   // the lit flank of the vein ridge
    else { const side = Math.abs(((bt * 6 - bx * 3.5) % 1 + 1) % 1 - .5); if (side < .04 && bx < .22 && bt > .12 && bt < .9) c = mix(c, PAL.p3_line(.35), .28); }
    if (r < .16) c = mix(c, PAL.p3_lime(.3), .45);
    if (d > -.026) c = mix(c, PAL.p3_line(.75), .92); else if (d > -.065) c = mix(c, PAL.p3_lime(.25), .45);
    return c;
  };
}
const lineLeafPaint = (sd, axis, {R = PAL.p3_lime, base = .12, tip = null, glyph = false} = {}) => (a, s) => {
  const d = sd(a, s); if (d > 0) return null;
  const n = axis.near(a, s), t = n.t, w = Math.max(.03, n.d - d), xn = clamp(n.s / w, -1, 1);
  let v = base + .16 * xn * xn + .09 * (NS.a(a * 6, s * 6) - .5) + .05 * t;
  let c = R(clamp(v));
  if (Math.abs(xn) < .07 && t < .93) c = mix(c, PAL.p3_line(.3), .55);
  else if (xn > .07 && xn < .2) c = lift(c, .15);
  else { const sv = Math.abs(((t * 8 - Math.abs(xn) * 1.4) % 1 + 1) % 1 - .5); if (sv < .045 && Math.abs(xn) < .8) c = mix(c, PAL.p3_line(.35), .3); }
  if (tip && t > .7) c = mix(c, tip, clamp((t - .7) / .2) * .7);
  if (glyph) c = glyphOn(c, a, s);
  if (d > -.024) c = mix(c, PAL.p3_line(.75), .92); else if (d > -.05) c = mix(c, PAL.p3_rim(.3), .45);
  return c;
};

// ---- A phase 3: the forked leafy tip (UPRIGHT: the arm runs up and out, 30 deg off vertical) ----------------------------------
// three long pointed blades fanned from the arm's end (up, up-out, out) + a small lower blade, the gold tip cone on top
function forkP3() {
  const els = [], edge = edgeTile('h_edge_p3', PAL.p3_line, .12, .38, 'p3');
  const BL = [[8, .84, .14, -.05, 1], [36, .96, .16, 0, 1], [64, .8, .14, .05, -1], [102, .44, .1, .09, -1]];
  for (const [deg, L, W, dz, curl] of BL) {
    const p = deg * D2R, axis = stroke([[0, .02], [Math.sin(p) * L, .02 + Math.cos(p) * L]], () => 0), sd = tipShape(L, W, p);
    const hi = Math.max(.12, Math.cos(p) * L + W * Math.sin(p) + .06), lo = Math.min(-.12, Math.cos(p) * L - W);
    const rect = {a0: -W - .04, a1: Math.sin(p) * L + W + .05, s0: lo, s1: hi};
    const top = lineLeafPaint(sd, axis, {R: PAL.p3_leafhand, base: .14, tip: PAL.p3_rim(.15)}), under = lineLeafPaint(sd, axis, {R: P3_UNDER, base: .2});
    // blades that run up bend about X (their tips curl toward the viewer; the front is the -N card); blades that run out
    // bend about Y (sweep back; the front is the +N card); the backs are the pale undersides
    if (deg < 45) els.push(...sheet({o: [0, -.02, dz], U: '+x', R: '+y', rect, sd, tex: sheetSprite(`h_fork${deg}_b`, rect, under, 24, 'p3'), texM: sheetSprite(`h_fork${deg}`, rect, top, 40, 'p3'), edge, seed: 411 + deg,
      bands: [{s: rect.s0, ang: 0, half: .04}, {s: hi * .55, ang: 22.5 * curl, half: .035}, {s: hi * .82, ang: 45 * curl, half: .025}]}));
    else {
      const rx = {a0: rect.s0, a1: rect.s1, s0: rect.a0, s1: rect.a1}, T = f => (a, s) => f(s, a);
      els.push(...sheet({o: [0, -.02, dz], U: '+y', R: '+x', rect: rx, sd: (a, s) => sd(s, a), tex: sheetSprite(`h_forkx${deg}`, rx, T(top), 40, 'p3'), texM: sheetSprite(`h_forkx${deg}_b`, rx, T(under), 24, 'p3'), edge, seed: 417 + deg,
        bands: [{s: rx.s0, ang: 0, half: .04}, {s: rx.s1 * .5, ang: 22.5, half: .035}, {s: rx.s1 * .8, ang: 45, half: .025}]}));
    }
  }
  // the wrist: a small core wrapped by two pointed bracts (front and back) that clasp the blade roots
  els.push(rockBox([-.09, -.14, -.085], [.09, .05, .085], 'p3_lime', {seed: 413}));
  const BR = tipLeaf(.5, .17, 0, 0, -.28), rBr = {a0: -.2, a1: .2, s0: -.28, s1: .24};
  const brT = sheetSprite('h_fork_br', rBr, lineLeafPaint(BR.sd, BR.axis, {R: PAL.p3_lime, base: .22}), 32, 'p3');
  for (const [z, sg] of [[-.15, 1], [.16, -1]]) els.push(...sheet({o: [.01, 0, z], U: '+x', R: '+y', rect: rBr, sd: BR.sd, tex: brT, edge, seed: 414, anchor: 1,
    bands: [{s: rBr.s0, ang: 0, half: .025}, {s: -.02, ang: -22.5 * sg, half: .022}]}));
  els.push(...spike([.1, .1, -.1], .095, spikeSprite('h_spk_gold3', PAL.p3_cone_gold, 'p3')));
  return scaleEls(els, 1.18);
}

// ---- B phase 3 open: the big lobed leaf hand (UPRIGHT; the arm comes in along -X, the boss's front is -Z) --------------
// model_p3 §2.3 item 16, v6 f480 (z_v6_0480_rhand), v5 f1074, v5 f1908: butter-yellow palmate leaves over a white-grey
// under-leaf that sticks out past the lobes as a forked pointed fin. The front leaf (5 lobes, up -> out) is cupped: its
// lower part leans back so the palm faces forward-up, the lobe tips curl toward the viewer. The outer leaf (3 lobes) and
// the under-leaf run outward and sweep back. Every leaf has a pale grey-lilac underside (from behind the hand reads grey,
// v5 f1908); the gold cone stands on the wrist.
const P3_UNDER = ramp(['#F1F0F4', '#DCDBE3', '#C4C3CC', '#A8A8B2', '#8A8A94', '#62626C']);
// front leaf: flat a = X, s = Y (U +x, R +y; its front is the -N card)
const LEAF1 = palmate([.34, -.22], [[-32, 1.0, .29], [-2, 1.34, .34], [28, 1.44, .36], [58, 1.32, .34], [88, 1.06, .3]],
  [[.34, -.32], [-.06, .28], [.3, .78], [1.0, .74], [1.3, .22], [1.22, -.32]]);
// outer leaf: flat a = Y, s = X (U +y, R +x; its front is the +N card)
const LEAF2 = palmate([.04, .95], [[-38, .98, .3], [-4, 1.3, .35], [32, 1.08, .31]], [[.04, .85], [-.42, 1.35], [.05, 1.8], [.5, 1.4]]);
// the under-leaf: flat a = Y, s = X; a long blade forked at the tip (the upper tip curving up), two lower serrations
const UNDER = (() => {
  const a = stroke([[-.12, .12], [-.22, 1.2], [-.1, 2.05], [.2, 2.7]], t => .42 * Math.sin(Math.PI * Math.min(1, .18 + .82 * t)) ** .8 + .012);
  const b = stroke([[-.3, 1.7], [-.56, 2.2], [-.72, 2.48]], t => .2 * Math.sin(Math.PI * Math.min(1, .22 + .78 * t)) + .01);
  const c = stroke([[-.34, 1.05], [-.66, 1.42], [-.8, 1.62]], t => .13 * Math.sin(Math.PI * Math.min(1, .25 + .75 * t)) + .01);
  return {sd: sdUnion(a.sd, b.sd, c.sd), a};
})();
// the pale underside of a palmate leaf: lilac grey, darker veins along the lobes, the outline
function undersidePaint(P, {R = P3_UNDER} = {}) {
  return (a, s) => {
    const d = P.sd(a, s); if (d > 0) return null;
    const ra = a - P.b[0], rs = s - P.b[1], r = Math.hypot(ra, rs);
    let bx = Infinity, bt = 0;
    for (const l of P.L) { const da = Math.sin(l.p), ds = Math.cos(l.p), t = (ra * da + rs * ds) / l.len, x = Math.abs(ra * ds - rs * da); if (x < bx && t > -.05) { bx = x; bt = t; } }
    let v = .22 + .14 * clamp(r / 1.4) + .08 * (NS.e(a * 5, s * 5) - .5) + .1 * clamp(bx / .32);
    let c = R(clamp(v));
    if (bx < .03 && bt > .02 && bt < .92) c = mix(c, R(.62), .7);                       // the raised rib
    else { const side = Math.abs(((bt * 6 - bx * 3.5) % 1 + 1) % 1 - .5); if (side < .035 && bx < .24 && bt > .12 && bt < .9) c = mix(c, R(.55), .4); }
    if (r < .2) c = mix(c, PAL.p3_lime(.35), .5);
    if (d > -.024) c = mix(c, PAL.p3_line(.7), .9); else if (d > -.05) c = mix(c, R(.1), .5);
    return c;
  };
}
// the under-leaf: front white-grey with a lime-yellow flush at its base and grey veins, back lilac grey
const underPaint = back => (a, s) => {
  const d = UNDER.sd(a, s); if (d > 0) return null;
  const n = UNDER.a.near(a, s), R = back ? P3_UNDER : PAL.p3_pale;
  let v = (back ? .2 : .06) + .18 * clamp(n.d / .36) + .08 * (NS.e(a * 6, s * 6) - .5) + .06 * n.t;
  let c = R(clamp(v));
  if (!back && n.t < .35) c = mix(c, PAL.p3_leafhand(.25), .55 * clamp((.35 - n.t) / .25));
  if (n.d < .016 && n.t < .96) c = mix(c, R(.6), .7);
  else { const vs = Math.abs(((n.t * 10 - n.d * 4) % 1 + 1) % 1 - .5); if (vs < .045 && n.d < .3) c = mix(c, R(.5), .45); }
  if (d > -.024) c = mix(c, PAL.p3_line(.7), .9); else if (d > -.05) c = lift(c, .4);
  return c;
};
function openP3() {
  const els = [], edgeY = edgeTile('h_edge_p3y', PAL.p3_line, .12, .38, 'p3'), edgeG = edgeTile('h_edge_p3g', PAL.p3_pale, .55, .78, 'p3');
  const R1 = {a0: -.62, a1: 1.86, s0: -.46, s1: 1.2}, R2 = {a0: -.68, a1: .82, s0: .62, s1: 2.32}, RF = {a0: -.96, a1: .5, s0: .02, s1: 2.76};
  // the under-leaf behind, sweeping back as it runs out (its front is the +N card)
  els.push(...sheet({o: [0, -.02, .2], U: '+y', R: '+x', rect: RF, sd: UNDER.sd, tex: sheetSprite('h_underleaf', RF, underPaint(false), 48, 'p3'),
    texM: sheetSprite('h_underleaf_b', RF, underPaint(true), 32, 'p3'), edge: edgeG, seed: 451, cell: .1,
    bands: [{s: RF.s0, ang: 0, half: .03}, {s: 1.25, ang: 22.5, half: .03}, {s: 1.8, ang: 45, half: .025}, {s: 2.3, ang: 67.5, half: .022}]}));
  // the outer leaf: three lobes out past the front leaf, sweeping back with the under-leaf
  els.push(...sheet({o: [0, .02, .06], U: '+y', R: '+x', rect: R2, sd: LEAF2.sd, tex: sheetSprite('h_leaf2', R2, lobedPaint(LEAF2), 56, 'p3'),
    texM: sheetSprite('h_leaf2_b', R2, undersidePaint(LEAF2), 40, 'p3'), edge: edgeY, seed: 452, cell: .1,
    bands: [{s: R2.s0, ang: 0, half: .04}, {s: 1.25, ang: 22.5, half: .035}, {s: 1.8, ang: 45, half: .03}]}));
  // the front leaf, cupped: the palm leans back, the lobe tips curl forward (its front is the -N card)
  els.push(...sheet({o: [0, 0, -.13], U: '+x', R: '+y', rect: R1, sd: LEAF1.sd, tex: sheetSprite('h_leaf1_b', R1, undersidePaint(LEAF1), 40, 'p3'),
    texM: sheetSprite('h_leaf1', R1, lobedPaint(LEAF1), 56, 'p3'), edge: edgeY, seed: 453, cell: .1, anchor: 1,
    bands: [{s: R1.s0, ang: -22.5, half: .045}, {s: .28, ang: 0, half: .045}, {s: .72, ang: 22.5, half: .04}, {s: 1.0, ang: 45, half: .035}]}));
  // the wrist: a small core clasped by two lime bracts (front and back) where the leaves spring, the gold cone on top
  els.push(rockBox([-.14, -.15, -.12], [.18, .1, .16], 'p3_lime', {seed: 454}));
  // (the bract shape and sprite are the fork's: tipLeaf(.5, .17) over the same rect)
  const BR = tipLeaf(.5, .17, 0, 0, -.28), rBr = {a0: -.2, a1: .2, s0: -.28, s1: .24}, edgeL = edgeTile('h_edge_p3', PAL.p3_line, .12, .38, 'p3');
  const brT = sheetSprite('h_fork_br', rBr, lineLeafPaint(BR.sd, BR.axis, {R: PAL.p3_lime, base: .22}), 32, 'p3');
  for (const [z, sg] of [[-.17, 1], [.1, -1]]) els.push(...sheet({o: [.03, 0, z], U: '+x', R: '+y', rect: rBr, sd: BR.sd, tex: brT, edge: edgeL, seed: 455, anchor: 1,
    bands: [{s: rBr.s0, ang: 0, half: .025}, {s: -.02, ang: -22.5 * sg, half: .022}]}));
  els.push(...spike([.02, .16, -.02], .11, spikeSprite('h_spk_gold3', PAL.p3_cone_gold, 'p3')));
  return scaleEls(els, 1.1);
}

// ---- B phase 3 curl: the fiddlehead foot (UPRIGHT world axes; the crawl wrist 0.4 b over the water) -------------------------
// a broad frond runs down from the wrist, forward along the water and rolls up and back over itself; two side fronds
// splay out and curl up; yellow tips, the cream cone on the wrist
const frondW = (s, L, W) => (s < 0 || s > L ? -1 : (W * Math.pow(1 - s / L, .7) + .03) * (1 + .1 * Math.sin(s * 20)));
const frondSd = (L, W) => (a, s) => { const out = s < 0 ? -s : s > L ? s - L : 0; const w = Math.max(.0, frondW(clamp(s, 0, L), L, W)); return Math.max(Math.abs(a) - w, out > 0 ? out : -1e9); };
const frondPaint = (L, W) => {
  const sd = frondSd(L, W);
  return (a, s) => {
    const d = sd(a, s); if (d > 0) return null;
    const t = s / L, w = Math.max(.03, frondW(s, L, W)), xn = clamp(a / w, -1, 1);
    let v = .1 + .14 * xn * xn + .1 * (NS.a(a * 6, s * 6) - .5) + .05 * t;
    let c = PAL.p3_leafhand(clamp(v));
    if (Math.abs(a) < .018) c = mix(c, PAL.p3_line(.3), .55);
    else if (a > .018 && a < .05) c = lift(c, .18);
    else { const sv = Math.abs(((s * 6 - Math.abs(a) * 3) % 1 + 1) % 1 - .5); if (sv < .045) c = mix(c, PAL.p3_line(.35), .3); }
    if (t > .6) c = mix(c, C('#F2EE7A'), clamp((t - .6) / .2) * .7);
    if (d > -.024) c = mix(c, PAL.p3_line(.75), .92); else if (d > -.05) c = mix(c, PAL.p3_lime(.3), .5);
    return c;
  };
};
// a broad leaf with three rounded lobes at its end (rolled into the fiddlehead foot)
// (it narrows toward the rolled end, so the curled walls read as tongues round a ball rather than the sides of a box)
const rollSd = (L, W) => {
  const lobes = [-.42, 0, .42].map(x => sdCircleF(x * W, L - .1 - Math.abs(x) * .1, .3 * W));
  return (a, s) => { const t = clamp(s / L); const w = W * (.8 + .2 * Math.sin(Math.PI * t * .9)) * (1 - .42 * clamp((t - .45) / .55) ** 1.3) * (1 + .06 * Math.sin(s * 19)); return Math.min(Math.max(Math.abs(a) - w, s - (L - .12), -s), ...lobes.map(f => f(a, s))); };
};
const sdCircleF = (cx, cy, r) => (a, s) => Math.hypot(a - cx, s - cy) - r;
const rollPaint = (L, W) => {
  const sd = rollSd(L, W);
  return (a, s) => {
    const d = sd(a, s); if (d > 0) return null;
    const t = s / L, xn = clamp(a / W, -1, 1);
    let v = .1 + .14 * xn * xn + .1 * (NS.a(a * 6, s * 6) - .5) + .04 * t;
    let c = PAL.p3_leafhand(clamp(v));
    if (Math.abs(a) < .018) c = mix(c, PAL.p3_line(.3), .55);
    else if (a > .018 && a < .05) c = lift(c, .18);
    else { const sv = Math.abs(((s * 5.5 - Math.abs(a) * 2.6) % 1 + 1) % 1 - .5); if (sv < .04) c = mix(c, PAL.p3_line(.35), .3); }
    if (t > .72) c = mix(c, C('#F2EE7A'), clamp((t - .72) / .18) * .7);
    if (d > -.024) c = mix(c, PAL.p3_line(.75), .92); else if (d > -.055) c = mix(c, PAL.p3_lime(.3), .5);
    return c;
  };
};
// the curled leaf hand (the crawl foot, the fold): a closed rosette of lobed yellow leaves cupped up and in round the wrist
// (a leafy ball, v6 f528 / f165): an outer ring of four big leaves and an inner ring of four smaller, tighter ones
const rosLeaf = (L, W, phi) => { const sd = rollSd(L, W), cs = Math.cos(phi), sn = Math.sin(phi); return (a, s) => sd(a * cs - s * sn, a * sn + s * cs); };
function curlB() {
  const els = [], edge = edgeTile('h_edge_p3y', PAL.p3_line, .12, .38, 'p3');
  const RING = [
    {L: 1.0, W: .34, phi: 12, y: -.12, name: 'h_ros_o', bands: [[0, 22.5, .055], [.26, -22.5, .05], [.5, -45, .045], [.72, -67.5, .04]]},
    {L: .86, W: .28, phi: -24, y: -.05, name: 'h_ros_i', bands: [[0, -22.5, .045], [.2, -45, .04], [.44, -67.5, .035], [.68, -90, .03]]},
  ];
  // the outer leaves differ per direction (the front one longest, the back one short and tight) so the ball is not square
  const KR = {f: 1.14, l: .94, b: .78, r: 1.04};
  for (const r of RING) for (const run of ['f', 'l', 'b', 'r']) {
    const k = r.name === 'h_ros_o' ? KR[run] : 1, L = r.L * k;
    const p = r.phi * D2R, ext = L * Math.cos(p) + r.W * Math.abs(Math.sin(p)) + .06, wd = r.W + L * Math.abs(Math.sin(p)) + .06;
    const rect = {a0: -wd, a1: wd, s0: 0, s1: ext}, sd = rosLeaf(L, r.W, p);
    const rp = rollPaint(L, r.W), cs = Math.cos(p), sn = Math.sin(p);
    const tex = sheetSprite(k === 1 ? r.name : `${r.name}_${run}`, rect, (a, s) => rp(a * cs - s * sn, a * sn + s * cs), 40, 'p3');
    const [U, R] = RUNS[run];
    els.push(...sheet({o: [0, r.y, 0], U, R, N: '+y', rect, sd, tex, edge, seed: 441 + els.length,
      bands: r.bands.map(([f, ang, half]) => ({s: f * ext, ang, half}))}));
  }
  els.push(rockBox([-.17, -.16, -.15], [.19, .14, .19], 'p3_lime', {seed: 442}));
  els.push(...spike([.02, .14, -.05], .1, spikeSprite('h_spk_cream3', PAL.p3_cone, 'p3')));
  return els;
}

// ---- C phase 3 curl: the folded leaf hand (UPRIGHT; v5 f588, v6 f480 z_v6_0480_rhand) ------------------------------------
// a tulip of leaves round the wrist: the front bowl leaf rolled under at its foot (the canoe of v5 f588) carrying the
// square-spiral glyph, two tall pointed tips rising behind it (the outer one taller), a side leaf on each side flaring at
// the foot and curling in at the top, a back leaf, a pale under-leaf showing inside; yellow-lime outside, pale lilac grey
// inside; the cream cone points out and down. Lowest point 0.35 b under the wrist (the crawl wrist is 0.4 b up).
const GLYPH = (() => {
  const pts = [[0, 0]]; let x = 0, y = 0; const st = [[1, 0], [0, 1], [-1, 0], [0, -1]];
  for (let i = 0; i < 7; i++) { const n = Math.ceil((i + 1) / 2), [dx, dy] = st[i % 4]; x += dx * n; y += dy * n; pts.push([x, y]); }
  return stroke(pts.map(([px, py]) => [.12 + px * .07, -.08 + py * .07]), () => .026);
})();
const glyphOn = (c, a, s) => { const g = GLYPH.sd(a, s); if (g < 0) return mix(PAL.p3_line(.55), c, .12); if (g < .024) return mix(c, C('#F4F2B0'), .5); return c; };
const BOWL = (() => {
  const sd = (a, s) => { const t = (s + .42) / .82; if (t < 0) return Math.max(-t * .82, Math.abs(a - .08) - .44); if (t > 1) return (t - 1) * .82; const w = .5 * Math.pow(Math.sin(Math.PI * (.3 + .7 * t)), .6) + .005; return Math.abs(a - .08) - w; };
  return {sd, axis: stroke([[.08, -.42], [.08, .4]], () => 0)};
})();
const tipLeaf = (L, W, phi, a0, s0) => { const sd = tipShape(L, W, phi * D2R); return {sd: (a, s) => sd(a - a0, s - s0), axis: stroke([[a0, s0], [a0 + Math.sin(phi * D2R) * L, s0 + Math.cos(phi * D2R) * L]], () => 0)}; };
const TIP_I = tipLeaf(1.02, .21, -10, -.2, -.12), TIP_O = tipLeaf(1.3, .23, 9, .36, -.12);
const SIDE = tipLeaf(.9, .4, 90, -.32, 0), BACKL = tipLeaf(.92, .36, 0, .08, -.36);
const INNER = tipLeaf(1.0, .3, 4, .1, -.2);
function curlC() {
  const els = [], edge = edgeTile('h_edge_p3y', PAL.p3_line, .12, .38, 'p3');
  const yel = (L, o = {}) => lineLeafPaint(L.sd, L.axis, {R: PAL.p3_leafhand, base: .08, tip: C('#F2EE7A'), ...o});
  const pale = L => lineLeafPaint(L.sd, L.axis, {R: P3_UNDER, base: .16});
  // the back leaf (outside to the back) and the pale inner leaf
  const rB = {a0: -.34, a1: .5, s0: -.36, s1: .6};
  els.push(...sheet({o: [0, 0, .3], U: '+x', R: '+y', rect: rB, sd: BACKL.sd, tex: sheetSprite('h_cupb_o', rB, yel(BACKL, {base: .16}), 40, 'p3'),
    texM: sheetSprite('h_cupb_i', rB, pale(BACKL), 32, 'p3'), edge, seed: 466, anchor: 2,
    bands: [{s: rB.s0, ang: -45, half: .03}, {s: -.18, ang: -22.5, half: .03}, {s: .05, ang: 0, half: .03}, {s: .38, ang: -22.5, half: .025}]}));
  const rI = {a0: -.24, a1: .48, s0: -.2, s1: .84};
  els.push(...sheet({o: [0, 0, .15], U: '+x', R: '+y', rect: rI, sd: INNER.sd, tex: sheetSprite('h_cup_in', rI, pale(INNER), 40, 'p3'), edge, seed: 463,
    bands: [{s: rI.s0, ang: 0, half: .025}, {s: .4, ang: -22.5, half: .022}]}));
  // the two tall tips: pale-based fronts, yellow ends, yellow-lime backs; they lean back above the bowl
  for (const [T, nm, rr, sd0] of [[TIP_I, 'i', {a0: -.6, a1: .1, s0: -.12, s1: .92}, 467], [TIP_O, 'o', {a0: .1, a1: .82, s0: -.12, s1: 1.2}, 468]]) {
    const front = (a, s) => { const c = yel(T)(a, s); if (!c) return c; const t = (s + .12) / 1.1; return t < .45 ? mix(c, P3_UNDER(.18), .55 * clamp((.45 - t) / .3)) : c; };
    els.push(...sheet({o: [0, 0, .06], U: '+x', R: '+y', rect: rr, sd: T.sd, tex: sheetSprite(`h_ctip${nm}_b`, rr, yel(T, {base: .2}), 32, 'p3'),
      texM: sheetSprite(`h_ctip${nm}`, rr, front, 40, 'p3'), edge, seed: sd0, bands: [{s: rr.s0, ang: 0, half: .03}, {s: .38, ang: -22.5, half: .028}, {s: .74, ang: 0, half: .024}]}));
  }
  // the side walls: a leaf wrapped round each side of the cup from the bowl to the back leaf (it runs front -> back and
  // bends about Y, so it shows a broad face from the front quarter), its point rising in the middle (+N = +X)
  const rS = {a0: -.34, a1: .6, s0: -.42, s1: .42};
  const texSo = sheetSprite('h_cups_o', rS, yel(SIDE), 40, 'p3'), texSi = sheetSprite('h_cups_i', rS, pale(SIDE), 32, 'p3');
  for (const [x, sg] of [[.6, -1], [-.44, 1]]) els.push(...sheet({o: [x, 0, 0], U: '+y', R: '+z', rect: rS, sd: SIDE.sd, tex: sg < 0 ? texSo : texSi, texM: sg < 0 ? texSi : texSo, edge, seed: 465, anchor: 2,
    bands: [{s: rS.s0, ang: 45 * sg, half: .028}, {s: -.26, ang: 22.5 * sg, half: .028}, {s: -.1, ang: 0, half: .028}, {s: .12, ang: -22.5 * sg, half: .028}, {s: .27, ang: -45 * sg, half: .026}]}));
  // the front bowl with the glyph, rolled under at its foot (anchored at its upright band)
  const rect = {a0: -.44, a1: .6, s0: -.42, s1: .42};
  els.push(...sheet({o: [0, -.08, -.3], U: '+x', R: '+y', rect, sd: BOWL.sd, tex: sheetSprite('h_cup_i', rect, lineLeafPaint(BOWL.sd, BOWL.axis, {R: PAL.p3_lime, base: .3}), 32, 'p3'),
    texM: sheetSprite('h_cup', rect, yel(BOWL, {glyph: true}), 56, 'p3'), edge, seed: 461, anchor: 3,
    bands: [{s: -.42, ang: 67.5, half: .04}, {s: -.28, ang: 45, half: .04}, {s: -.1, ang: 22.5, half: .04}, {s: .08, ang: 0, half: .04}, {s: .26, ang: -22.5, half: .035}]}));
  els.push(rockBox([-.15, -.115, -.13], [.17, .12, .15], 'p3_lime', {seed: 462}));
  els.push(...spike([.6, -.24, -.12], .09, spikeSprite('h_spk_cream3', PAL.p3_cone, 'p3'), {axis: 'x', dir: 1}));
  return scaleEls(els, 1.2, [0, -.3, 0]);
}

// ---- region interface ------------------------------------------------------------------------------------------------------
const BUILD = {
  a: {p1_planted: clawPlanted, p1_raised: clawRaised, p3_fork: forkP3},
  b: {p1_open: () => petalFoot(1, false, false), p1_curl: () => petalFoot(1, false, true), p3_curl: curlB, p3_open: openP3},
  c: {p1_open: () => petalFoot(.83, true, false), p1_curl: () => petalFoot(.83, true, true), p3_curl: curlC},
};
let built = null;
export function models() {
  if (built) return built;
  const out = {};
  for (const [L, vars] of Object.entries(BUILD)) for (const [v, fn] of Object.entries(vars)) {
    const m = toUnits(autoSlot(fn()), PART_SCALE[`${L}_hand_l`]);
    out[`${L}_hand_l_${v}`] = m; out[`${L}_hand_r_${v}`] = mirrorX(m);
  }
  return (built = out);
}
// the form look's default hand per form (the sets p1_rest / p3_open of the contract; hands.sets in the manifest)
export const FORM_MODELS = Object.fromEntries(PARTS.map(n => { const L = n[0]; return [n, {p1: `${n}_${L === 'a' ? 'p1_planted' : 'p1_open'}`, p3: `${n}_${L === 'a' ? 'p3_fork' : L === 'b' ? 'p3_open' : 'p3_curl'}`}]; }));
export function sprites() { models(); return {...SP}; }
void [smooth, sink];
