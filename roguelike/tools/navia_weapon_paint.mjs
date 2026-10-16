// Painted sprites for Navia's weapons: the gold-and-navy halberd of images/4.png and her
// parasol gun (closed and open). Pure Node, sharing the colour helpers, PNG writer and
// atlas merge of weapon_paint.mjs; paintWeaponTextures() there calls naviaWeaponSprites().
//
// Halberd sprites (prefix nv_). The head art is traced from the straightened reference
// (navia/understand/weapon_ref/straight_v2.png): shapes below are in reference pixels (u = px
// from the shaft axis, negative = the big-crescent side; y = px down from the spear apex) and
// map to the model frame by X = 8 + u*K, Y = 8 + (350 - y)*K (nvX / nvY), so the grip [8,8,8]
// sits on the handle just under the lower gold ring and the apex is at Y 31.9.
//   nv_head      alpha-cut head on three stacked cards spanning NV_HEAD: the pale-gold crescent
//                axe (lemon bands, ivory panel with taupe engravings), the back fin with its
//                violet gem, and the champagne C/S scroll frame. Outline and colour zones are
//                traced polygons; the fine scrolls (volutes, eye curl, right frame) are lit
//                gold tubes drawn over them
//   nv_tip       spear point with fleur-de-lis curls, two crossed cards spanning NV_TIP
//   nv_crystal   elongated light-blue hexagonal crystal with one glint (crossed cards)
//   nv_crystal_core  plain opaque facets for the crystal's core box (no cut-out, no glint)
//   nv_socket    violet-navy socket with a gold centre ridge, v along the box
//   nv_shaft1    indigo shaft with lavender edges and a silver centre strip (upper section)
//   nv_shaft2    indigo shaft with a lavender diamond lattice fading to dark (lower section)
//   nv_collar    silver chevron collar with a blue diamond
//   nv_sleeve    faceted champagne sleeve: pointed cap, stacked chevrons, v along the box
//   nv_sleeve_crown  the lower chevron of the 45-degree inner crown that fills the cap's corners
//   nv_guard     alpha-cut crossguard knot with two down-swept spikes (crossed cards, NV_GUARD)
//   nv_wrap      espresso handle with an oxblood spiral wrap and three pearl studs
//   nv_butt      alpha-cut two-lobed gold finial (crossed cards, NV_BUTT)
//   nv_gold / nv_rose  champagne fittings and the gold rose emblem
//
// Parasol sprites (prefix np_), after the umbrella gun in the reference videos (v1, v2, v4, v5):
//   np_top / np_lining  the open canopy's rim disc: the gathered ruffle top / the gold lining
//                with orange-red paisley, dark ribs, hub and the ruffle's underside
//   np_dome0..10 the stacked discs of the dome's cap, painted in model units (crown light,
//                ribs; emblems and filigree crests on one disc only)
//   np_drum_rib / np_drum_emb / np_drum_fil  the dome's flank (sixteen cards): rib, gold
//                blue-gem emblem and filigree panels
//   np_profile   the cap's side view for the four crossed cards (navy, rib line on the edge)
//   np_ruffle_u / np_ruffle_ub / np_ruffle_l  the two hanging ruffle tiers (upper with bows)
//   np_finial    the slim gold finial (the muzzle)
//   np_crosette / np_bundle / np_ctip  closed parasol: ruffle rosette, folded black-indigo
//                bundle with the thin lace collar, short gold tip (crossed cards)
//   np_fold / np_ruffle / np_rosette  the closed bundle's and rosette's core boxes and discs
//   np_handle    black crook handle with a gold cap (stacked cards)
//   np_shaft / np_gshaft / np_gold / np_cog / np_plaque / np_hub  black and gold shafts,
//                fittings, gear, gem plaque, the runner under the lining
import {hex, clamp, smooth, mix, ramp, fbm, TRANSPARENT} from './weapon_paint.mjs';

// ---- reference frame ----------------------------------------------------------------------
export const NV_K = 0.0683;
export const nvX = u => 8 + u * NV_K;
export const nvY = y => 8 + (350 - y) * NV_K;
const refU = X => (X - 8) / NV_K, refY = Y => 350 - (Y - 8) / NV_K;
// Card boxes (model units). The head card leaves the shaft column transparent.
export const NV_HEAD = {X0: 2.0, X1: 13.7, Y0: 17.5, Y1: 31.4};
export const NV_TIP = {HW: 0.95, Y0: 27.85, Y1: 31.92};
export const NV_CRYSTAL = {HW: 0.65, Y0: 22.35, Y1: 24.95};
export const NV_GUARD = {HW: 1.92, Y0: 10.5, Y1: 12.3};
export const NV_BUTT = {HW: 0.7, Y0: 1.5, Y1: 4.3};
// Sleeve box: faces cut to a pointed cap (apex Y1 mid-face, SHOULDER at the corners).
export const NV_SLEEVE = {HW: 0.75, Y0: 11.6, Y1: 15.25, SHOULDER: 14.35, APEX2: 15.0};

// ---- small vector toolkit (reference px) ----------------------------------------------------
// Points may carry a third entry 'c' to keep a sharp corner; other points are joined by a
// Catmull-Rom spline sampled n times per segment.
function spline(pts, n = 8) {
  const P = pts.map(p => [p[0], p[1]]), out = [];
  for (let i = 0; i < P.length - 1; i++) {
    const p0 = P[Math.max(0, i - 1)], p1 = P[i], p2 = P[i + 1], p3 = P[Math.min(P.length - 1, i + 2)];
    for (let k = 0; k < n; k++) {
      const t = k / n, t2 = t * t, t3 = t2 * t;
      out.push([0, 1].map(a => .5 * (2 * p1[a] + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t2 + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t3)));
    }
  }
  out.push([P[P.length - 1][0], P[P.length - 1][1]]);
  return out;
}
// Smooth an open path, restarting the spline at every corner point.
function smoothPath(pts, n) {
  const out = [];
  let run = [pts[0]];
  for (let i = 1; i < pts.length; i++) {
    run.push(pts[i]);
    if (pts[i][2] === 'c' || i === pts.length - 1) {
      const s = spline(run, n);
      out.push(...(out.length ? s.slice(1) : s));
      run = [pts[i]];
    }
  }
  return out;
}
// Segment list with a coarse grid for nearest-distance queries.
class Segs {
  constructor(pts, closed, cell = 4) {
    this.cell = cell;
    const P = closed ? [...pts, pts[0]] : pts;
    this.s = [];
    let L = 0;
    for (let i = 0; i < P.length - 1; i++) {
      const [ax, ay] = P[i], [bx, by] = P[i + 1], len = Math.hypot(bx - ax, by - ay);
      this.s.push({ax, ay, bx, by, l0: L, len});
      L += len;
    }
    this.len = L;
    this.grid = new Map();
    for (const [k, sg] of this.s.entries()) {
      const x0 = Math.floor(Math.min(sg.ax, sg.bx) / cell), x1 = Math.floor(Math.max(sg.ax, sg.bx) / cell);
      const y0 = Math.floor(Math.min(sg.ay, sg.by) / cell), y1 = Math.floor(Math.max(sg.ay, sg.by) / cell);
      for (let gx = x0; gx <= x1; gx++) for (let gy = y0; gy <= y1; gy++) {
        const key = gx * 100003 + gy;
        if (!this.grid.has(key)) this.grid.set(key, []);
        this.grid.get(key).push(k);
      }
    }
  }
  // Nearest point within R: {d, t (0..1 along the path), nx, ny (unit vector from the path
  // to the query point)}; d = R when nothing is closer.
  near(x, y, R) {
    const c = this.cell, gx0 = Math.floor((x - R) / c), gx1 = Math.floor((x + R) / c);
    const gy0 = Math.floor((y - R) / c), gy1 = Math.floor((y + R) / c);
    let best = {d: R, t: 0, nx: 0, ny: 0};
    const seen = new Set();
    for (let gx = gx0; gx <= gx1; gx++) for (let gy = gy0; gy <= gy1; gy++) {
      const list = this.grid.get(gx * 100003 + gy);
      if (!list) continue;
      for (const k of list) {
        if (seen.has(k)) continue;
        seen.add(k);
        const sg = this.s[k], dx = sg.bx - sg.ax, dy = sg.by - sg.ay;
        const q = sg.len > 0 ? clamp(((x - sg.ax) * dx + (y - sg.ay) * dy) / (sg.len * sg.len)) : 0;
        const px = sg.ax + dx * q, py = sg.ay + dy * q, d = Math.hypot(x - px, y - py);
        if (d < best.d) best = {d, t: (sg.l0 + q * sg.len) / this.len, nx: d > 0 ? (x - px) / d : 0, ny: d > 0 ? (y - py) / d : 0};
      }
    }
    return best;
  }
}
// Closed region: inside test by row crossings (cached per row) and distance to the outline.
class Region {
  constructor(pts, n = 8) {
    this.p = smoothPath([...pts, pts[0]], n).slice(0, -1);
    this.edge = new Segs(this.p, true);
    const xs = this.p.map(p => p[0]), ys = this.p.map(p => p[1]);
    this.box = [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)];
    this.rows = new Map();
  }
  inside(x, y) {
    const [x0, y0, x1, y1] = this.box;
    if (x < x0 || x > x1 || y < y0 || y > y1) return false;
    let cr = this.rows.get(y);
    if (!cr) {
      cr = [];
      const P = this.p;
      for (let i = 0, j = P.length - 1; i < P.length; j = i++) {
        const [xi, yi] = P[i], [xj, yj] = P[j];
        if ((yi > y) !== (yj > y)) cr.push(xi + (y - yi) * (xj - xi) / (yj - yi));
      }
      cr.sort((a, b) => a - b);
      if (this.rows.size > 64) this.rows.clear();
      this.rows.set(y, cr);
    }
    let n = 0;
    for (const c of cr) { if (c < x) n++; else break; }
    return (n & 1) === 1;
  }
  dist(x, y, R = 8) { return this.edge.near(x, y, R).d; }
}
// Open stroke with a width profile w(t) (px), drawn as a lit tube.
class Stroke {
  constructor(pts, w, n = 8, closed = false) {
    this.p = closed ? smoothPath([...pts, pts[0]], n) : smoothPath(pts, n);
    this.c = new Segs(this.p, false);
    this.w = typeof w === 'function' ? w : () => w;
    const xs = this.p.map(p => p[0]), ys = this.p.map(p => p[1]), m = 6;
    this.box = [Math.min(...xs) - m, Math.min(...ys) - m, Math.max(...xs) + m, Math.max(...ys) + m];
  }
  // {e: 0 on the centre line .. 1 at the edge, lx, ly: outward unit vector} or null.
  hit(x, y) {
    const [x0, y0, x1, y1] = this.box;
    if (x < x0 || x > x1 || y < y0 || y > y1) return null;
    const r = this.c.near(x, y, 6);
    const h = this.w(r.t) / 2;
    if (r.d > h) return null;
    return {e: r.d / h, lx: r.nx, ly: r.ny, t: r.t};
  }
}
const taper = (...stops) => t => {
  // stops: [[t, w], ...]
  if (t <= stops[0][0]) return stops[0][1];
  for (let i = 1; i < stops.length; i++) if (t <= stops[i][0]) {
    const a = stops[i - 1], b = stops[i], k = (t - a[0]) / (b[0] - a[0]);
    return a[1] + (b[1] - a[1]) * k;
  }
  return stops[stops.length - 1][1];
};

// ---- palette (weapon.md §10.2) --------------------------------------------------------------
// Built on first use: weapon_paint.mjs imports this module, so its helpers are not ready while
// this module loads.
let PAL;
function pal() {
  return PAL || (PAL = {
    outline: hex('#48361f'),
    // Champagne ornament gold: lit tube shading across a stroke (-1 shade side .. +1 lit side).
    // Warm mid tones (#c9a466 / #d9b77e, shade #9c7a48); near-white only on the narrow highlight.
    goldTube: ramp([[-1, '#6e5230'], [-.55, '#9c7a48'], [-.1, '#c9a466'], [.35, '#d9b77e'], [.72, '#f0d9aa'], [1, '#e2c893']]),
    // Flat champagne fittings across a face: lit edge .. shade.
    goldFace: ramp([[0, '#eed6a6'], [.25, '#d9b77e'], [.6, '#c09c62'], [1, '#8f6e40']]),
  });
}
// Light comes from the upper left of the reference (reference y points down).
const LX = -.55, LY = -.83;

// ---- halberd head ------------------------------------------------------------------------------
// Outlines traced from the straightened reference (reference px, "u,y" pairs): the head
// silhouette (crescent, scroll frame with its loops and eye curls, back fin; even-odd, so the
// loops stay open), the pale lemon bands (crescent outer and upper inner band, fin bands) and
// the ivory panel of the crescent. Everything else inside the silhouette is champagne gold.
const NV_HEAD_SIL = [
  '-30.9,12.9 -30.1,12.7 -29,14.4 -25.8,24.4 -24.3,32.6 -24.6,36.1 -23.6,38.9 -23.1,44.4 -24.9,56.4 -26.2,59.9 -28.6,63.5 -33.1,67.6 -34.7,70.1 -33.9,70.7 -30.9,70.6 -25.1,67.7 -20.4,64.2 -18.1,61.8 -17.4,61.7 -17.1,62.6 -19,68.9 -22.1,74.5 -25.6,78.8 -32.6,84.2 -33.2,85.4 -28.4,88.4 -25.6,91.4 -23.1,96.1 -22.4,102.9 -21.4,103 -17.4,100.9 -14.1,100.8 -10.7,102.1 -8.1,104.3 -6.2,107.9 -6.5,110.6 -6,113.1 -6,127.9 -7.7,132.4 -6.8,134.6 -6.1,140.1 -6.9,140.9 -10.2,141.4 -10.5,146.1 -11.1,147.2 -15.6,148 -18.6,146.7 -20.8,144.1 -21.4,140.9 -21.1,138.9 -20.3,137.6 -18.9,137 -15.9,137.4 -14.8,138.9 -14.9,141.4 -14.4,141.8 -12.7,139.6 -12.6,136.1 -14.2,132.4 -17.4,128.3 -18.6,127.6 -19.4,129.4 -20.6,129.2 -21.8,127.4 -21.6,125.4 -23.1,124.3 -26.1,124.3 -28.1,125 -28.8,123.6 -29.9,123.5 -35.4,124.5 -36.9,125.2 -38.4,127 -41.4,127.5 -46.2,131.9 -49.9,140.4 -49.7,145.9 -47.8,151.1 -44.4,155.3 -38.6,160.5 -35.1,161.7 -29.6,162.2 -24.6,161.5 -20.6,159.2 -19.9,159.9 -20.4,162.4 -21.6,164.7 -23.6,166.9 -28.4,170.6 -25.4,179.1 -23.9,186.9 -27.1,204.6 -27.7,206.4 -28.4,207 -28.9,206.4 -29.3,202.4 -31.3,195.4 -34.3,189.1 -36.9,185.2 -41.9,179.8 -63.4,161.2 -70.9,153.9 -80,140.4 -81.2,138.4 -85,127.6 -86.2,123.1 -86.9,116.1 -86.2,107.1 -84.5,98.9 -82.3,92.4 -77,81.9 -73.8,77.4 -64.6,67.8 -48,52.4 -39.4,42.9 -34.9,34.6 -32.6,27.9 -31.3,21.4',
  '38.4,65.1 39.4,66.1 41.1,72.6 43.8,76.9 47.9,80.6 54.1,85.1 58.9,90.1 64,97.4 68.6,105.6 71.1,108.6 78.4,112.7 79.8,114.4 79.3,115.1 72.7,118.6 69.1,121.8 67.2,124.4 63.5,132.1 60.4,137.1 57,141.1 44.7,151.6 40.6,157.9 38,164.9 37.4,165.3 36,162.6 35,156.9 35.2,151.1 36.2,147.1 38.2,142.9 37.9,141.9 36.5,140.4 37.6,138.1 41.9,136.6 45.6,132.4 46.1,129.4 44.9,126.6 41.6,122.8 35.1,120.3 27.9,120.9 23.6,123 19.4,126.1 15.7,130.6 14.2,133.9 13.8,137.6 14.1,140.4 15.6,141.7 16.1,141.1 15.9,138.6 16.6,137.3 18.4,136.8 20.6,137.7 22.2,139.9 22,144.1 20.9,145.4 18.1,147 13.9,147.5 10.7,145.4 10.1,141.3 6.4,140.4 7.2,139.1 7.5,135.1 6.7,130.6 7.5,129.4 6.4,129.4 6,128.4 6,114.1 6.3,112.6 7.4,112.4 7.7,111.9 7.3,109.4 7.7,105.9 6.9,104.6 7,103.9 8.9,102.7 14.1,102.2 14.9,96 15.9,96.2 18.6,98.9 18.4,99.6 17,100.4 19.6,101 22.1,102.6 24.1,105.4 24.9,105.1 25.3,101.6 26.6,101 30.1,106.4 35.1,108.9 38.6,108.6 43.6,105.4 45,102.9 45.9,98.3 46.6,97.7 48.5,99.4 50.9,99.7 51.6,100.6 51.7,101.9 50.9,105.9 49.8,108.4 48.2,110.6 45,113.6 44.8,114.6 49.6,121.6 50.9,127.4 51.6,127.9 52.3,127.4 53.6,121.9 50.1,114.4 53.1,109.1 53.6,101.6 52.6,99.2 49.2,95.4 42.1,89.5 41.1,89.7 40.6,91.4 37.4,90.6 33.1,91.7 32.1,91.1 33.1,89.1 35.9,88.5 36.9,87.4 35,76.4 36.4,69.1',
  '-43.9,91.6 -46.9,91.9 -54.5,97.6 -59,102.9 -61.8,109.9 -63.5,119.4 -62.8,122.4 -62.8,125.9 -61.4,131.3 -58.9,132.6 -59.6,136.1 -58.8,138.6 -57.4,140.1 -56.5,139.4 -58.5,132.9 -57.9,127.9 -56.1,121.6 -53.1,117 -49.2,113.1 -45.6,111.2 -44.6,111.2 -39.9,113.2 -37.4,113.1 -36.4,112.4 -36.9,111.9 -39.6,111.4 -43.7,108.4 -45.8,107.9 -45.4,106.1 -46.4,104.1 -45.2,100.1 -44.6,99.7 -44.2,100.1 -43.5,103.1 -41.9,105.4 -38.6,107 -35.6,106.7 -33.9,105.7 -32.5,104.4 -30.9,101.1 -31.1,97.9 -34.4,93.5 -38.4,92.2',
  '14.9,109.1 13.4,110 12.3,112.1 13.1,117.9 12.9,123.4 10.4,125.8 9.7,125.6 9.4,124.4 8.6,125.6 8.5,127.1 9.6,128.1 9.2,130.1 9.6,130.7 11.9,128.1 14.1,124.1 17.3,120.4 20.3,113.6 20,112.4 18.5,110.4 16.1,109.2',
];
// The crescent's outer edge (part of the silhouette's first loop, lower tip round to the upper
// horn) and the width of the pale band measured in from it (reference px by y): about 0.55
// units near the horns, 0.8 around Y 22-26, closing at both tips.
const nvOuterEdge = () => {
  const l = loops([NV_HEAD_SIL[0]])[0], i = l.findIndex(([u, y]) => u === -28.4 && y === 207);
  return new Segs([...l.slice(i), l[0]], false);
};
const NV_BAND_W = (() => {
  const w = [[12, 1.5], [24, 6], [40, 8], [70, 10.5], [86, 11.8], [145, 11.8], [165, 10.5], [185, 8.5], [198, 6], [207, 2.5]];
  return y => {
    if (y <= w[0][0]) return w[0][1];
    for (let i = 1; i < w.length; i++) if (y <= w[i][0]) return w[i - 1][1] + (w[i][1] - w[i - 1][1]) * (y - w[i - 1][0]) / (w[i][0] - w[i - 1][0]);
    return w[w.length - 1][1];
  };
})();
// Inner prong band (the crescent's upper inner horn) and the fin's two bands; the crescent's
// outer band is NV_BAND_W in from nvOuterEdge.
const NV_HEAD_LEMON = [
  '-26.1,43.4 -25.4,43.3 -24.7,44.4 -24.3,47.9 -25.8,56.6 -27.8,60.9 -34.1,67.5 -42.4,73.1 -46.9,78.2 -51.4,80.8 -56.5,85.6 -60.9,91.4 -63.4,95.8 -69.1,98.2 -69.4,97.1 -68.2,94.1 -61.5,83.9 -54.4,75.8 -41.6,64.7 -36.1,58.7 -31.3,52.4',
  '40.2,73.6 41.1,74 44.9,78.8 52.4,85.3 61,96.6 64.7,100.4 67.4,105.4 70.1,108.5 76.6,112.6 77.4,114.1 76.9,115.4 71.6,118.8 67.5,123.1 62.4,133.4 58.2,139.1 46,149.6 43.1,152.9 41.9,153.4 40.9,153 40.6,151.9 43.6,146.4 52,137.9 63.4,120.6 68.1,117.2 72.9,114.9 71.9,114.5 70.4,115.8 64.4,118.4 60.4,121.4 59.4,121.2 59.6,120.2 63.6,117.4 64.1,115.1 59.9,110 56.4,108.1 55.8,103.4 52.8,96.6 54.3,96.9 56.6,100.7 57.1,101 57.4,100.4 54.2,95.1 48.6,89.7 47.8,89.9 50,92.6 49.4,93.6 44.4,89.4 44,88.1 44.6,86.6 40.9,79.1 39.8,74.6',
];
const NV_HEAD_IVORY = [
  '-29.5,69.9 -26.1,70 -23.9,71.9 -23.3,74.6 -25,78.1 -33.1,84.4 -51.1,92.4 -58.6,102.4 -60.6,106.4 -62.9,114.1 -63.5,119.9 -62.5,127.6 -57.2,142.4 -58.3,145.1 -60.9,145.3 -65.2,140.9 -72.6,125.9 -73.2,120.9 -71.5,113.1 -72,106.6 -70.9,101.4 -69.4,98.8 -63.2,95.6 -56.1,85.4 -51.1,80.6 -43.6,78 -37.1,72.1',
  '-33.5,113.9 -29.1,114.2 -22.2,116.6 -20.1,120.1 -21.2,123.1 -23.4,124.2 -27.6,124.2 -29.6,123.5 -34.6,124.3 -41.6,127 -44.4,126.9 -45.9,126 -46.7,124.6 -46.6,122.6 -44,118.9 -38.6,115.3',
  '-55.4,150.4 -50.4,151.4 -38.6,160.5 -33.6,162.1 -31.4,163.8 -25.8,178.4 -25.5,181.4 -26.3,182.9 -27.9,183.1 -29.5,182.1 -38.8,172.1 -54,157.9 -56.8,153.1 -56.6,151.4',
];
const loops = list => list.map(s => s.split(' ').map(p => p.split(',').map(Number)));
// Even-odd area over several closed loops, with distance to any of their edges.
class Area {
  constructor(list) { this.r = loops(list).map(l => new Region(l, 1)); }
  inside(x, y) { let k = false; for (const r of this.r) if (r.inside(x, y)) k = !k; return k; }
  near(x, y, R) { let b = {d: R, nx: 0, ny: 0}; for (const r of this.r) { const q = r.edge.near(x, y, b.d); if (q.d < b.d) b = q; } return b; }
}
export const NV_FIN_GEM = [55.6, 114.2, 2.5];
// The fleur-de-lis volutes flanking the crystal and the upper-left eye curl, drawn over the
// trace as lit gold tubes. A volute runs from a short leg beside the crystal over an arched
// head, down the long body toward the rose and out into a small eye curl; a teardrop slot
// stays open under each head.
const VOLUTE = [[10.6, 114], [10, 107.5], [12, 102.6], [16, 100.4], [20.2, 102.4], [22.2, 107.5], [22, 115], [20.4, 123],
  [17.8, 130], [15, 135.5], [13.4, 141], [15.2, 145.8], [19.4, 147], [22.2, 143.6], [21, 139.6], [17.8, 139.6], [17.4, 142.4]];
const NV_HEAD_TUBES = () => [...[-1, 1].map(s => new Stroke(VOLUTE.map(([u, y]) => [s * u, y]),
  taper([0, 4.6], [.15, 6], [.3, 6.6], [.5, 7.4], [.66, 6.4], [.8, 5], [.92, 3.6], [1, 2]))),
  // Upper-left eye curl: over the top from the volute's head, round the left and into the eye.
  new Stroke([[-24.6, 102], [-26.2, 95], [-30.6, 90.2], [-36.4, 88.6], [-42.4, 90.6], [-46, 96], [-45.8, 102.6], [-42, 107.6],
    [-36.2, 108.4], [-32.6, 105], [-33.6, 101.2]], taper([0, 4], [.25, 5.4], [.5, 6.4], [.7, 6.8], [.88, 4.4], [1, 2.2])),
  // Right frame (the trace merges it): the C ring opening to the upper left, and the big arc
  // from the volute's body over the lower loop into the fin.
  new Stroke([[32.6, 89.4], [38.4, 88.4], [43.8, 90.6], [47.6, 95.6], [48.2, 101.6], [44.6, 106.6], [38, 109.4], [31.6, 108.2], [27.8, 104.2],
    [26.4, 99]], taper([0, 1.6], [.2, 4.6], [.5, 6.6], [.8, 5], [1, 1.4])),
  new Stroke([[18.8, 125], [21.4, 120.4], [26.4, 117.4], [33, 116.6], [40, 118.2], [45.4, 122.4], [48.6, 128.6], [49.6, 133]],
    taper([0, 6], [.3, 6.6], [.7, 6.8], [1, 6]))];
// Where the right frame replaces the trace (reference px box).
const RIGHT_FRAME = [9.5, 46, 92, 131];
const NV_HEAD_CUTS = () => [-1, 1].map(s => new Stroke([[15.8, 106.5], [16.2, 114], [15.6, 121.5], [14.6, 126.5]].map(([u, y]) => [s * u, y]),
  taper([0, 2.6], [.35, 4.4], [1, 1.6])));

function nvHead() {
  const sil = new Area(NV_HEAD_SIL), lemon = new Area(NV_HEAD_LEMON), ivory = new Area(NV_HEAD_IVORY), outer = nvOuterEdge();
  const n = fbm(37), {outline: OUTLINE} = pal();
  // Taupe engravings on the ivory panel (S-swirls and a vine).
  const engr = [
    new Stroke([[-55, 89], [-51, 85], [-46.5, 83.4], [-43, 85.2], [-44.4, 88], [-47.2, 87]], 1.3),
    new Stroke([[-38.5, 81], [-34.5, 77.2], [-30, 76.2], [-27.4, 78], [-29, 80.4], [-31.6, 79.6]], 1.2),
    new Stroke([[-66.5, 101], [-69, 109], [-69.2, 118], [-67.6, 127], [-65, 135]], 1.1),
    new Stroke([[-68.9, 109.5], [-65.6, 108], [-64.6, 110.6], [-66.6, 111.8]], 1.0),
    new Stroke([[-67.8, 126], [-64.8, 123.6], [-63.6, 126.2], [-65.6, 127.6]], 1.0),
    new Stroke([[-44, 166], [-39.5, 170.5], [-35, 172.4], [-31.6, 171], [-32.8, 168.6]], 1.1),
  ];
  // Champagne scroll frame (warm mid tones, near-white only on the lit bevel).
  const gold = ramp([[-1, '#6a4e2c'], [-.5, '#9c7a48'], [0, '#c9a466'], [.45, '#dbba82'], [.8, '#eed5a5'], [1, '#f7e7c4']]);
  // Pale lemon blade bands, outer edge -> inner seam (weapon.md §10.2, §11.4).
  const band = ramp([[0, '#fefdc8'], [.45, '#f9f6b3'], [1, '#ecd7a9']]);
  const finBand = ramp([[0, '#fdfdcd'], [.5, '#f9f1b8'], [1, '#ecd7a9']]);
  const tubes = NV_HEAD_TUBES(), cuts = NV_HEAD_CUTS(), {goldTube} = pal();
  const [gx, gy, gr] = NV_FIN_GEM;
  return (u, v) => {
    const X = NV_HEAD.X0 + u * (NV_HEAD.X1 - NV_HEAD.X0), Y = NV_HEAD.Y1 - v * (NV_HEAD.Y1 - NV_HEAD.Y0);
    const x = refU(X), y = refY(Y);
    // The shaft column and the crystal stay clear (their own boxes and cards draw them). The
    // crystal gap is a head texel wider than the crystal cards (|X-8| <= 0.65), so no head
    // texel shares the z=8 plane with an opaque crystal texel.
    if (Math.abs(x) < 6.6 || (y > 98 && y < 142 && Math.abs(x) < 10.2)) return TRANSPARENT;
    if (cuts.some(c => c.hit(x, y))) return TRANSPARENT;
    let tube = null;
    for (const t of tubes) { const h = t.hit(x, y); if (h && (!tube || h.e < tube.e)) tube = h; }
    const [fx0, fx1, fy0, fy1] = RIGHT_FRAME;
    const inSil = sil.inside(x, y) && !(x > fx0 && x < fx1 && y > fy0 && y < fy1 && !lemon.inside(x, y));
    if (!inSil && !tube) return TRANSPARENT;
    const ds = sil.near(x, y, 6), grain = (n(x * .35, y * .35) - .5) * .1;
    // The crescent's outer band: everything within NV_BAND_W of its outer edge.
    const W = NV_BAND_W(y), dOut = x < 0 && inSil ? outer.near(x, y, 16).d : 99;
    let col;
    if (tube) {
      const lit = (tube.lx * LX + tube.ly * LY) * Math.sqrt(1 - Math.pow(1 - tube.e, 2));
      col = goldTube(clamp(lit * 1.1 + (1 - tube.e) * .3, -1, 1));
      if (tube.e > .8) col = mix(col, OUTLINE, smooth(.8, .98, tube.e) * .7);
    } else if (dOut < W) {
      // Polished pale band ramping across its whole width; only the lower third of the
      // crescent warms toward saturated gold.
      col = mix(band(clamp(dOut / W)), hex('#eed17f'), smooth(150, 198, y) * .5);
      if (W > 6 && W - dOut < .8) col = mix(col, hex('#8a6c44'), .55);
    } else if (lemon.inside(x, y)) {
      // Inner prong band (crescent side) and the fin's bands; the fin's lower band warms.
      const dz = lemon.near(x, y, 8), t = clamp(ds.d / 7);
      col = x < 0 ? band(t) : mix(finBand(t), hex('#f4dd8e'), smooth(112, 126, y) * .5);
      if (dz.d < ds.d - .3 && dz.d < .55) col = mix(col, hex('#8a6c44'), .5);
    } else if (ivory.inside(x, y)) {
      const dz = ivory.near(x, y, 8);
      col = mix(hex('#fff4e2'), hex('#f3e2c8'), smooth(0, 7, dz.d) * .4 + smooth(3, 0, dz.d) * .45);
      for (const e of engr) { const h = e.hit(x, y); if (h) col = mix(col, hex('#b69d6d'), .8 * (1 - h.e * .5)); }
      if (dz.d < .55) col = mix(col, hex('#a88a62'), .45);
    } else {
      // Champagne ornament: bevel lit from the upper left along every edge of the gold area.
      let b = ds;
      for (const z of [lemon, ivory]) { const q = z.near(x, y, b.d); if (q.d < b.d) b = q; }
      const lit = -(b.nx * LX + b.ny * LY), k = 1 - smooth(0, 5, b.d);
      col = gold(clamp(lit * k * 1.35 + (k - .5) * .12, -1, 1));
      if (b !== ds && b.d < .5) col = mix(col, hex('#7a6040'), .4);
    }
    // Violet gem in the fin.
    const dg = Math.hypot(x - gx, y - gy);
    if (dg < gr) {
      col = mix(hex('#5c4470'), hex('#b89ad0'), smooth(gr * .5, gr, dg));
      if (Math.hypot(x - gx + .7, y - gy + .7) < .75) col = mix(col, hex('#ffe9db'), .9);
    }
    if (!tube && ds.d < .75) col = mix(col, OUTLINE, .7);
    return mix(col, grain > 0 ? hex('#ffffff') : hex('#000000'), Math.abs(grain));
  };
}

// ---- halberd: point, crystal, shaft sections, fittings -----------------------------------------
// Half-width profile (reference px) by linear interpolation over [y, w] stops.
const profile = stops => y => {
  if (y <= stops[0][0]) return stops[0][1];
  for (let i = 1; i < stops.length; i++) if (y <= stops[i][0]) {
    const [y0, w0] = stops[i - 1], [y1, w1] = stops[i];
    return w0 + (w1 - w0) * (y - y0) / (y1 - y0);
  }
  return stops[stops.length - 1][1];
};
// Champagne metal across a profile: x/w in -1..1, lit from the left, ridge highlight.
function champagne(t, e) {
  const {outline} = pal();
  let c = mix(hex('#dcbd86'), hex('#9c7a48'), smooth(-.2, 1, t));
  c = mix(c, hex('#f4e0b6'), Math.max(0, 1 - Math.abs(t + .25) / .22) * .75);
  if (e > .84) c = mix(c, outline, smooth(.84, 1, e) * .9);
  return c;
}
// Spear point with fleur-de-lis curls (crossed cards spanning NV_TIP).
function nvTip() {
  const w = profile([[0, 0], [8, 2.6], [20, 5.6], [32.5, 8.5], [36, 6.5], [39, 4.2], [46, 4.0], [50, 3.4], [59.6, 3.2]]);
  const curls = [-1, 1].map(s => new Stroke([[3.2, 44.5], [6.8, 49.6], [10.6, 53.6], [13, 54.2], [13.4, 52]].map(([u, y]) => [s * u, y]),
    taper([0, 3.8], [.55, 2.8], [1, 1.2])));
  return (u, v) => {
    const X = 8 - NV_TIP.HW + u * 2 * NV_TIP.HW, Y = NV_TIP.Y1 - v * (NV_TIP.Y1 - NV_TIP.Y0);
    const x = refU(X), y = refY(Y), hw = w(y);
    let col = null;
    if (Math.abs(x) <= hw) {
      const t = x / Math.max(hw, .01);
      col = champagne(t, Math.abs(t));
      // Bronze groove down the axis of the leaf.
      const gw = Math.max(0, 1.6 * Math.sin(Math.PI * clamp((y - 17) / 19)));
      if (Math.abs(x) < gw) col = mix(hex('#5b4227'), hex('#4b2f16'), Math.abs(x) / Math.max(gw, .01));
      if (y > 36 && y < 38.5) col = mix(col, pal().outline, .6);
    }
    for (const c of curls) {
      const h = c.hit(x, y);
      if (!h) continue;
      const lit = (h.lx * LX + h.ly * LY) * Math.sqrt(1 - Math.pow(1 - h.e, 2));
      col = pal().goldTube(clamp(lit * 1.1 + .1, -1, 1));
      if (h.e > .75) col = mix(col, pal().outline, smooth(.75, .97, h.e) * .9);
    }
    return col || TRANSPARENT;
  };
}
// Light-blue crystal: an elongated hexagon pointed at both ends, on the two crossed cards. A
// single white glint sits in the upper point, above the core box.
function nvCrystal() {
  const w = profile([[100.6, 0], [113, 9.5], [127, 9.5], [138.6, 0]]);
  return (u, v) => {
    const X = 8 - NV_CRYSTAL.HW + u * 2 * NV_CRYSTAL.HW, Y = NV_CRYSTAL.Y1 - v * (NV_CRYSTAL.Y1 - NV_CRYSTAL.Y0);
    const x = refU(X), y = refY(Y), hw = w(y);
    if (Math.abs(x) > hw) return TRANSPARENT;
    const t = x / Math.max(hw, .01);
    let c = t < 0 ? mix(hex('#b3d3f2'), hex('#7ea4e4'), smooth(0, .9, -t)) : mix(hex('#b3d3f2'), hex('#93c0f2'), smooth(0, .9, t));
    c = mix(c, hex('#c8ecff'), smooth(120, 102, y) * .85);
    c = mix(c, hex('#eef9ff'), Math.max(0, 1 - Math.hypot(x / 5, (y - 120) / 11)) * .9);
    if (Math.hypot((x + 2.5) / .8, y - 106.5) < 1.7) c = mix(c, hex('#ffffff'), .95);
    if (Math.abs(t) > .85) c = mix(c, hex('#6f7593'), smooth(.85, 1, Math.abs(t)) * .8);
    return c;
  };
}
// The crystal's core box (rotated 45 degrees inside the crossed cards): plain opaque facets,
// luminous in the middle, no cut-out and no glint, so the cards alone draw the outline.
const nvCrystalCore = () => (u, v) => {
  let c = mix(hex('#d9f0ff'), hex('#97bfee'), smooth(0, 1, Math.abs(u - .5) * 2) * .85);
  c = mix(c, hex('#eef9ff'), smooth(.55, 0, v) * .35);
  return mix(c, hex('#86b2ea'), smooth(.5, 1, v) * .35);
};
// Violet-navy socket under the point: a gold ridge rising to a point, gold bands at the ends.
const nvSocket = () => (u, v) => {
  if (v < .1 || v > .93) return pal().goldFace(clamp(Math.abs(u - .35) * 1.6));
  const ridge = .06 + .2 * (v - .1) / .83;
  if (Math.abs(u - .5) < ridge) return mix(hex('#efd9ac'), hex('#c09c62'), Math.abs(u - .5) / ridge);
  return mix(hex('#553d5e'), hex('#301737'), smooth(0, .5, Math.abs(u - .3)));
};
// Navy shaft, upper section: lavender edges and a silver strip widening downward.
const nvShaft1 = () => (u, v) => {
  const r = Math.abs(u - .5) * 2;
  let c = mix(hex('#4a44a0'), hex('#241e48'), smooth(.35, 1, r));
  c = mix(c, hex('#8e8cd0'), Math.max(0, 1 - Math.abs(r - .7) / .12) * .8);
  if (r < .1 + .14 * v) c = mix(hex('#dfdad5'), hex('#c5c0be'), r / (.1 + .14 * v));
  return c;
};
// Navy shaft, lower section: a lavender diamond lattice over the top half, then plain navy.
const nvShaft2 = () => (u, v) => {
  const r = Math.abs(u - .5) * 2;
  let c = mix(hex('#3d3a86'), hex('#1f1a3c'), smooth(.35, 1, r));
  c = mix(c, hex('#2e2230'), smooth(.45, .75, v) * .7);
  const a = (u * 2 + v * 4) % 1, b = (-u * 2 + v * 4 + 10) % 1, band = Math.min(Math.abs(a - .5), Math.abs(b - .5));
  if (band < .09) c = mix(c, hex(band < .045 ? '#9a9ad8' : '#6a6ab0'), (1 - smooth(.35, .6, v)) * .9);
  return c;
};
// Silver chevron collar with a blue diamond and a dark core.
const nvCollar = () => (u, v) => {
  const dx = Math.abs(u - .5), dy = v - .5;
  let c = mix(hex('#dfdad5'), hex('#b5a5a8'), smooth(0, 1, v * .7 + dx));
  if (Math.abs(v - .25 - dx * .6) < .05) c = mix(c, hex('#8d8790'), .7);
  const dd = dx + Math.abs(dy) * .8;
  if (dd < .3) c = mix(hex('#585584'), hex('#3e3c72'), dd / .3);
  if (dd < .12) c = hex('#1e1d3a');
  if (Math.abs(dd - .3) < .03) c = mix(c, hex('#f2efea'), .8);
  return c;
};
// Faceted champagne sleeve (box faces spanning NV_SLEEVE, v down the box): a pointed cap whose
// chevron outline rises to the middle of each face, stacked chevrons, a light centre diamond,
// and a waist above the guard knot suggested by shading (an alpha waist would open a hole at
// the box corners in three-quarter views).
const nvSleeve = () => (u, v) => {
  const S = NV_SLEEVE, Y = S.Y1 - v * (S.Y1 - S.Y0), a = Math.abs(u - .5) * 2;
  const top = S.Y1 - (S.Y1 - S.SHOULDER) * a;
  if (Y > top) return TRANSPARENT;
  const {goldFace, outline} = pal();
  const waist = Math.max(0, 1 - Math.abs(Y - 12.5) / .9);
  let c = goldFace(clamp(.12 + smooth(.1, 1, a) * (.6 + waist * .35) + (S.Y1 - Y) / (S.Y1 - S.Y0) * .25));
  const k = (((top - Y) / .95) % 1 + 1) % 1;
  if (k < .09) c = mix(c, hex('#5a4224'), .7 * (1 - k / .09));
  else if (k < .2) c = mix(c, hex('#f0d9aa'), .55);
  if (a * .8 + Math.abs(Y - 14.55) * .55 < .2) c = mix(c, hex('#f6e4bd'), .8);
  if (top - Y < .06) c = mix(c, outline, .75);
  else if (a > .94) c = mix(c, outline, .3);
  return c;
};
// The inner crown's faces (Y 13.5..APEX2): a lower chevron in the same gold and grooves.
const nvSleeveCrown = () => (u, v) => {
  const S = NV_SLEEVE, Y = S.APEX2 - v * (S.APEX2 - 13.5), a = Math.abs(u - .5) * 2;
  const top = S.APEX2 - (S.APEX2 - S.SHOULDER) * a;
  if (Y > top) return TRANSPARENT;
  let c = pal().goldFace(clamp(.15 + a * .45 + (S.APEX2 - Y) * .12));
  const k = (((top - Y) / .95) % 1 + 1) % 1;
  if (k < .09) c = mix(c, hex('#5a4224'), .7 * (1 - k / .09));
  else if (k < .2) c = mix(c, hex('#f0d9aa'), .55);
  if (top - Y < .06) c = mix(c, pal().outline, .75);
  return c;
};
// Crossguard: a central knot and two thin spikes sweeping out and down (crossed cards).
function nvGuard() {
  const spikes = [-1, 1].map(s => new Stroke([[7, 292], [13, 296.5], [19.5, 302.5], [24.5, 308], [27, 312]].map(([u, y]) => [s * u, y]),
    taper([0, 8.4], [.45, 5.4], [1, 1.2])));
  const knot = profile([[287, 7], [292, 10.4], [300, 11.2], [307, 9], [313.4, 6.5]]);
  return (u, v) => {
    const X = 8 - NV_GUARD.HW + u * 2 * NV_GUARD.HW, Y = NV_GUARD.Y1 - v * (NV_GUARD.Y1 - NV_GUARD.Y0);
    const x = refU(X), y = refY(Y);
    let col = null;
    if (Math.abs(x) <= knot(y)) col = champagne(x / knot(y), Math.abs(x / knot(y)));
    for (const s of spikes) {
      const h = s.hit(x, y);
      if (!h) continue;
      const lit = (h.lx * LX + h.ly * LY) * Math.sqrt(1 - Math.pow(1 - h.e, 2));
      col = pal().goldTube(clamp(lit * 1.2 + .1, -1, 1));
      if (h.e > .75) col = mix(col, pal().outline, smooth(.75, .97, h.e) * .9);
    }
    return col || TRANSPARENT;
  };
}
// Espresso handle with an oxblood spiral wrap and three pearl studs (v down the handle,
// Y 9.45 -> 4.1).
const nvWrap = () => (u, v) => {
  const r = Math.abs(u - .5) * 2;
  let c = mix(hex('#412829'), hex('#231314'), smooth(.2, 1, r));
  const k = ((u * .7 + v * 9) % 1 + 1) % 1;
  if (k < .3) c = mix(c, hex(k < .15 ? '#5e3f3c' : '#4a322a'), .85);
  c = mix(c, hex('#72563b'), Math.max(0, 1 - Math.abs(u - .3) / .08) * .5);
  for (const Y of [7.73, 6.54, 5.34]) {
    const sv = (9.45 - Y) / 5.35, d = Math.hypot((u - .55) / .16, (v - sv) / .023);
    if (d < 1) c = d < .45 ? hex('#fbf3ee') : mix(hex('#e2cbc3'), hex('#b49f97'), smooth(.45, 1, d));
  }
  return c;
};
// Two-lobed faceted gold finial ending in a spike (crossed cards spanning NV_BUTT).
function nvButt() {
  const w = profile([[404, 4.6], [408, 7], [412, 10], [418, 6], [423, 4], [427, 7], [429.5, 9], [434, 5.5], [440, 2.6], [445, 0]]);
  return (u, v) => {
    const X = 8 - NV_BUTT.HW + u * 2 * NV_BUTT.HW, Y = NV_BUTT.Y1 - v * (NV_BUTT.Y1 - NV_BUTT.Y0);
    const x = refU(X), y = refY(Y), hw = w(y);
    if (Math.abs(x) > hw) return TRANSPARENT;
    const t = x / Math.max(hw, .01);
    return champagne(t, Math.abs(t));
  };
}
const nvGold = () => (u, v) => mix(pal().goldFace(smooth(.05, .95, Math.abs(u - .3) * 1.3 + v * .25)), hex('#6a4c28'), smooth(.85, 1, Math.max(Math.abs(u - .5), Math.abs(v - .5)) * 2) * .6);
// Gold rose emblem (alpha-cut): three petal rings around a bud.
const nvRose = () => (u, v) => {
  const dx = u - .5, dy = v - .5, r = Math.hypot(dx, dy) * 2, a = Math.atan2(dy, dx);
  const edge = .86 + .1 * Math.cos(a * 5);
  if (r > edge) return TRANSPARENT;
  const ring = r < .3 ? 0 : r < .58 ? 1 : 2;
  let c = [hex('#dcc08e'), hex('#ecd4a6'), hex('#c6a671')][ring];
  const petal = Math.cos(a * (ring === 2 ? 5 : 4) + ring) * .5 + .5;
  c = mix(c, hex('#8a6c42'), (1 - petal) * .45);
  if (r > edge - .1 || Math.abs(r - .3) < .03 || Math.abs(r - .58) < .03) c = mix(c, hex('#48361f'), .7);
  return c;
};

// ---- parasol gun -----------------------------------------------------------------------------
// Model-unit layout shared with navia_weapon_geometry.mjs (grip [8,8,8], muzzle toward +Y).
// Open canopy (about 0.28 D deep, after v2 f273-f279): a drum of sixteen tangential cards (DRUM,
// radius D) under a convex elliptic cap (DOME: semi-axes A across and B up from Y, so the cap
// leaves the drum's top edge at about 47 degrees). The cap shows from above as stacked discs on
// the ellipse (STEPS: [radius, height]) and from the side as four profile cards through the
// axis (PROFILE). The lining is the underside of the rim disc (radius R at
// RIM). The ruffle hangs from the rim in two staggered tiers of sixteen cards: the upper one
// just outside the drum, the longer lower one flaring further out (about 0.17 D in all).
// The rim disc sits level with the lower tier's top edge (the upper tier hangs through it).
// FINIAL is the slim gold muzzle on the crown. Panels are 45 degrees wide with the ribs on the
// X and Z axes and the diagonals; EMBLEM_FLANK / EMBLEM_TOP are the panel-centre directions
// (degrees, atan2(z - 8, x - 8)) whose drum card / dome top carries the gold blue-gem emblem,
// alternating so no panel shows two (the drum card at +22.5 degrees about Y faces -22.5).
const r2 = v => Math.round(v * 100) / 100;
// Cap: h(r) = Y + B * sqrt(1 - (r / A)^2), cut by the drum at r = DRUM.D (where it is 16.95).
const DOME = {A: 9.3, B: 5.2, Y: 14.55}, domeH = r => DOME.Y + DOME.B * Math.sqrt(1 - (r / DOME.A) ** 2);
// Disc radii: small steps (risers 0.1-0.4) so the rib cards stand only a little above each
// disc, and one wider ring (4.6..5.8, the MOTIF_DISC) for the emblems and crests on top.
const DRUM_D = 8.25, STEP_R = [DRUM_D, 7.85, 7.4, 6.9, 6.35, 5.8, 4.6, 3.9, 3.1, 2.2, 1.2];
export const NP = {
  CROOK: {X0: 5.2, X1: 8.7, Y0: 4.9, Y1: 8.6},
  COG: .95,
  // Closed: gold shaft from the cog into the ruffle rosette, the folded bundle and a small tip.
  ROSETTE: {HW: 2.55, Y0: 12.35, Y1: 15.3},
  BUNDLE: {HW: 2.0, Y0: 15.3, Y1: 22.05},
  TIP: {HW: .3, Y0: 22.05, Y1: 22.9},
  CANOPY: {
    RIM: 13.97, R: 8.9, DOME,
    DRUM: {D: DRUM_D, HW: 1.69, Y0: 13.97, Y1: r2(domeH(DRUM_D))},
    STEPS: STEP_R.map(r => [r, r2(domeH(r))]),
    PROFILE: {HW: 8.15, Y0: 13.97, Y1: 19.75},
    RUFFLE_U: {D: 8.42, HW: 1.73, Y0: 13.6, Y1: 15.05},
    RUFFLE_L: {D: 8.92, HW: 1.83, Y0: 11.85, Y1: 13.97},
    FINIAL: {HW: .34, Y0: 19.9, Y1: 22.15},
    EMBLEM_FLANK: [-22.5, 67.5, 157.5, 247.5], EMBLEM_TOP: [22.5, 112.5, 202.5, 292.5],
  },
};
// Colours from the reference videos (v1, v2, v4, v5).
const NPC = () => ({
  navy: hex('#272437'), navyDeep: hex('#191937'), navyLit: hex('#3d3a58'), crown: hex('#37334f'),
  rib: hex('#5a557f'), ribEdge: hex('#110f20'),
  frill: hex('#e9c766'), frillShade: hex('#a87a38'),
  ruf: hex('#ebc35e'), rufLit: hex('#fde492'), rufShade: hex('#b0802e'), rufDeep: hex('#7a5419'),
  lining: hex('#d3b163'), liningLit: hex('#f0c860'), liningShade: hex('#b78c40'),
  paisley: hex('#c8642a'), paisleyDeep: hex('#a8441c'), hub: hex('#181423'),
  fil: hex('#a88b52'), emb: hex('#e8c672'), embLit: hex('#fdeaa8'), embShade: hex('#8a652c'),
  gem: hex('#a4ccff'), gemDeep: hex('#2a4ab8'),
});
const sameDeg = (a, b) => Math.abs(((a - b) % 360 + 540) % 360 - 180) < .5;
// The canopy emblem: a gold lozenge frame with drop finials and side curls round a dark inlay
// and a blue gem. p across, q up (toward the crown), model units; null outside. About 1.85
// tall (0.1 D).
function emblem(c, p, q) {
  const ap = Math.abs(p), d = ap / .58 + Math.abs(q) / .78;
  const drop = Math.hypot(p, q - .87) < .09 || Math.hypot(p, (q + .9) / 1.3) < .1;
  const curl = ap > .58 && Math.abs(Math.hypot(ap - .7, q) - .12) < .045;
  if (d > 1 && !drop && !curl) return null;
  if (d > 1) return mix(c.emb, c.embShade, .3);
  if (d > .76) {
    let col = mix(c.embShade, c.embLit, clamp(.55 - p * .45 + q * .35));
    if (d > .95 || Math.abs(d - .79) < .03) col = mix(col, c.embShade, .65);
    return col;
  }
  const g = ap / .32 + Math.abs(q) / .48;
  if (g < 1) {
    let col = mix(c.gem, c.gemDeep, smooth(0, 1, g * .75 + (p - q) * .3 + .15));
    if (Math.hypot(p + .08, q - .13) < .07) col = hex('#ffffff');
    return col;
  }
  if (Math.abs(g - 1.22) < .08) return mix(c.emb, c.embShade, .35);
  return mix(c.navyDeep, hex('#0b0a16'), .5);
}
// Muted gold filigree on the other panels: mirrored open C-scrolls with eye curls, a stem with
// a fleur on top and lower sweeps. Coverage 0..1 at (p across, q up), model units.
function filigree(p, q) {
  const ap = Math.abs(p), line = (d, w) => Math.max(0, 1 - Math.abs(d) / w);
  let k = 0;
  const ang = Math.atan2(q - .15, ap - .72);
  if (ang > -1.1 || ang < -2.9) k = Math.max(k, line(Math.hypot(ap - .72, q - .15) - .4, .055));
  if (ap < .68) k = Math.max(k, line(Math.hypot(ap - .5, q + .1) - .13, .05));
  if (q > -.95 && q < .75) k = Math.max(k, line(ap, .05));
  if (q > .72) k = Math.max(k, line(Math.hypot(ap - .2, q - .95) - .2, .05));
  if (q < -.25 && ap < 1.25) k = Math.max(k, line(Math.hypot(ap - 1.25, q + .3) - .7, .055));
  return k;
}
// Outer face of the dome at (x, z) from the axis: lighter crown darkening toward the shoulder,
// raised ribs, and per panel an emblem (EMBLEM_TOP panels) or a filigree crest. The discs sit at
// different heights, so a motif crossing a disc edge, or repeated on the disc below (seen under
// the next disc's edge), would split apart in oblique views: the motifs are painted on one disc
// only (MOTIF_DISC), inside its visible ring and scaled to its width. The rest is painted in
// model units, so every stacked disc agrees and the steps leave no rings.
const MOTIF_DISC = 5;
function domeTop(c, x, z, disc) {
  const C = NP.CANOPY, rho = Math.hypot(x, z), q45 = Math.PI / 4, phi = Math.atan2(z, x);
  const seg = ((phi / q45) % 1 + 1) % 1, centre = (Math.floor(phi / q45) + .5) * 45;
  const p = (seg - .5) * rho * q45, dRib = (.5 - Math.abs(seg - .5)) * rho * q45;
  let col = mix(c.crown, c.navy, smooth(0, 8.4, rho));
  col = mix(col, c.navyLit, (1 - smooth(.04, .7, dRib)) * .3);
  const r0 = C.STEPS[MOTIF_DISC + 1][0], r1 = C.STEPS[MOTIF_DISC][0], k = (r1 - r0 - .1) / 1.9;
  if (disc === MOTIF_DISC && rho > r0 + .05 && rho < r1 - .05) {
    const mp = p / k, mq = ((r0 + r1) / 2 - rho) / k;
    if (C.EMBLEM_TOP.some(a => sameDeg(a, centre))) { const e = emblem(c, mp, mq); if (e) col = e; }
    else col = mix(col, c.fil, filigree(mp, mq) * .8);
  }
  if (dRib < .06 && rho > .5) col = c.rib;
  else if (dRib < .1 && rho > .5) col = mix(col, c.ribEdge, .5);
  if (rho < .45 && disc === C.STEPS.length - 1) col = mix(c.emb, c.embShade, smooth(.2, .45, rho));
  return col;
}
const npDome = k => {
  const c = NPC(), r = NP.CANOPY.STEPS[k][0];
  return (u, v) => {
    const x = (u - .5) * 2 * r, z = (v - .5) * 2 * r;
    return Math.hypot(x, z) > r ? TRANSPARENT : domeTop(c, x, z, k);
  };
};
// Drum cards (the dome's steep flank above the ruffle): 'rib' cards are centred on a rib, 'a'
// panel cards carry the emblem, 'b' panel cards the filigree.
function npDrum(kind) {
  const c = NPC(), D = NP.CANOPY.DRUM, yc = 15.98;
  return (u, v) => {
    const p = (u - .5) * 2 * D.HW, Y = D.Y1 - v * (D.Y1 - D.Y0);
    let col = mix(c.navy, c.navyLit, smooth(15.2, D.Y1, Y) * .45);
    col = mix(col, c.navyDeep, (1 - smooth(14.6, 15.4, Y)) * .5);
    if (kind === 'rib') {
      const d = Math.abs(p);
      col = mix(col, c.navyLit, (1 - smooth(.04, .7, d)) * .3);
      if (d < .06) col = c.rib; else if (d < .1) col = mix(col, c.ribEdge, .5);
    } else if (kind === 'a') { const e = emblem(c, p, Y - yc); if (e) col = e; }
    else col = mix(col, c.fil, filigree(p, Y - yc) * .8);
    return col;
  };
}
// Side view of the cap (four cards through the axis): the elliptic crown in the dome's navy,
// lit toward the top, with the rib line along its edge.
function npProfile() {
  const c = NPC(), {PROFILE: P, DOME: {A}} = NP.CANOPY;
  return (u, v) => {
    const X = 8 - P.HW + u * 2 * P.HW, Y = P.Y1 - v * (P.Y1 - P.Y0), r = Math.abs(X - 8);
    const h = domeH(Math.min(r, A));
    if (r > P.HW || Y > h) return TRANSPARENT;
    let col = mix(c.crown, c.navy, smooth(0, 8.4, r));
    col = mix(col, c.navyLit, .3 + smooth(h - .8, h, Y) * .3);
    return h - Y < .09 ? c.rib : col;
  };
}
// Gathered ruffle seen from above or below: t 0 at the drum .. 1 at the scalloped edge.
function ruffleTop(c, t, a) {
  const f = Math.cos(a * 64);
  let col = mix(c.rufShade, c.ruf, smooth(-.7, .8, f) * .75 + .15);
  col = mix(col, c.rufLit, Math.max(0, f - .4) * smooth(.2, .8, t) * .8);
  col = mix(col, c.rufDeep, (1 - smooth(0, .25, t)) * .6);
  return t > .9 ? mix(col, c.rufShade, .45) : col;
}
// Scalloped edge of the rim disc, inside the lower ruffle tier and level with its top, so it
// never shows edge-on beyond the frill.
const rimEdge = a => 8.7 + .2 * Math.sqrt(Math.abs(Math.cos(a * 16)));
// Upper face of the rim disc: the ruffle's gathered top between the drum and the scalloped edge.
function npTop() {
  const c = NPC(), R = NP.CANOPY.R;
  return (u, v) => {
    const x = (u - .5) * 2 * R, z = (v - .5) * 2 * R, rho = Math.hypot(x, z), a = Math.atan2(z, x), edge = rimEdge(a);
    if (rho > edge) return TRANSPARENT;
    return rho < 8.2 ? c.navyDeep : ruffleTop(c, (rho - 8.2) / (edge - 8.2), a);
  };
}
// Lining: gold panels with orange-red paisley, dark ribs, a dark hub; beyond the drum the
// ruffle's shaded underside.
function npLining() {
  const c = NPC(), n = fbm(71), R = NP.CANOPY.R, LR = NP.CANOPY.DRUM.D, S = LR / .89;
  const drops = [];
  for (let k = 0; k < 8; k++) {
    const mid = (k + .5) * Math.PI / 4;
    drops.push([mid + .12, .52, .1, mid], [mid - .18, .76, .085, mid + 1.4]);
  }
  return (u, v) => {
    const X = (u - .5) * 2 * R, Z = (v - .5) * 2 * R, rho = Math.hypot(X, Z), a = Math.atan2(Z, X), edge = rimEdge(a);
    if (rho > edge) return TRANSPARENT;
    if (rho > LR) return mix(ruffleTop(c, (rho - LR) / (edge - LR), a), c.rufShade, .3);
    // The concave lining (r, x, z in units of S): brighter mid-panel, shaded toward ribs and hub.
    const x = X / S, z = Z / S, r = rho / S;
    const seg = ((a / (Math.PI / 4)) % 1 + 1) % 1, ribd = Math.min(seg, 1 - seg) * r * Math.PI / 4;
    let col = mix(c.liningShade, c.lining, smooth(.1, .6, r) * smooth(0, .12, ribd));
    col = mix(col, c.liningLit, Math.max(0, Math.sin(seg * Math.PI)) * smooth(.35, .8, r) * .45);
    for (const [da, dr, sz, rot] of drops) {
      const px = dr * Math.cos(da), pz = dr * Math.sin(da), dx = x - px, dz = z - pz;
      const lx = dx * Math.cos(rot) + dz * Math.sin(rot), lz = -dx * Math.sin(rot) + dz * Math.cos(rot);
      const tail = lx > 0 ? lx / (sz * 2.2) : 0;
      const d = Math.hypot(lx / (sz * (lx > 0 ? 2.2 : 1)), (lz - tail * tail * sz * .9) / (sz * (1 - tail * .8)));
      if (d < 1) col = mix(c.paisley, c.paisleyDeep, smooth(.4, 1, d)), col = d > .82 ? mix(col, c.liningShade, .5) : col;
    }
    col = mix(col, hex('#000000'), (n(x * 6 + 9, z * 6) - .5) * .12);
    if (ribd < .016 && r > .12) col = hex('#2a2030');
    if (r > .87) col = mix(col, c.frillShade, .8);
    if (r < .16) col = r < .11 ? mix(c.hub, hex('#3a3346'), smooth(.11, 0, r) * .4) : mix(c.frill, c.frillShade, (r - .11) / .05);
    return col;
  };
}
// A small gold bow (two loops, a knot, two tails); p across, q up from its centre.
function bow(c, p, q) {
  const ap = Math.abs(p), loop = Math.hypot((ap - .3) / .27, q / .19), knot = Math.hypot(p / .09, q / .11);
  if (knot < 1) return mix(c.rufLit, c.ruf, knot);
  if (loop < 1) return loop > .8 ? c.rufDeep : mix(c.rufLit, c.rufShade, smooth(.2, .9, loop) * .7);
  if (q < 0 && q > -.4 && Math.abs(ap - (.07 - q * .4)) < .06) return c.rufShade;
  return null;
}
// Hanging ruffle cards: gathered gold folds puffing out toward a rolled hem with rounded
// scallops, shaded where they tuck under the rim; the upper tier's rib cards carry a bow.
function npRuffle(T, lobes, withBow) {
  const c = NPC();
  return (u, v) => {
    const p = (u - .5) * 2 * T.HW, Y = T.Y1 - v * (T.Y1 - T.Y0), H = T.Y1 - T.Y0;
    const s = 2 * (((u * lobes) % 1 + 1) % 1) - 1;
    const hem = T.Y0 + H * .17 * (1 - Math.sqrt(Math.max(0, 1 - s * s)));
    if (Y < hem) return TRANSPARENT;
    const f = -Math.cos(Math.PI * s) * .75 + Math.cos(2 * Math.PI * s) * .25, t = (Y - hem) / H;
    let col = mix(c.rufShade, c.ruf, smooth(-.8, .7, f) * .8 + .12);
    col = mix(col, c.rufLit, Math.max(0, f - .25) * (1 - t) * .9);
    col = mix(col, c.rufDeep, smooth(.6, 1, t) * .6);
    if (Y - hem < .07) col = mix(col, c.rufShade, .6);
    else if (Y - hem < .16) col = mix(col, c.rufLit, .45);
    if (withBow) { const b = bow(c, p, Y - (T.Y0 + H * .58)); if (b) col = b; }
    return col;
  };
}
// The open parasol's slim gold finial (the muzzle) above its collar box: neck, bulb, ring,
// knob and point.
function npFinial() {
  const F = NP.CANOPY.FINIAL;
  const w = profile([[19.9, .16], [20.1, .13], [20.5, .3], [20.85, .26], [20.95, .16], [21.07, .21], [21.19, .12], [21.53, .2], [21.85, .12], [22.15, 0]]);
  return (u, v) => {
    const x = (u - .5) * 2 * F.HW, Y = F.Y1 - v * (F.Y1 - F.Y0), hw = w(Y);
    if (Math.abs(x) > hw) return TRANSPARENT;
    const t = x / Math.max(hw, .01);
    const col = pal().goldTube(clamp(-t * .9 + .15, -1, 1));
    return Math.abs(t) > .82 ? mix(col, pal().outline, smooth(.82, 1, Math.abs(t)) * .6) : col;
  };
}
// Closed parasol: the gathered ruffle rosette round the shaft (four crossed cards), wider than
// the bundle, two scalloped tiers.
function npRosetteSide() {
  const c = NPC(), T = NP.ROSETTE;
  const w = profile([[12.35, .45], [12.6, 1.3], [13.0, 2.15], [13.5, 2.5], [14.2, 2.45], [14.8, 2.2], [15.3, 1.9]]);
  return (u, v) => {
    const x = (u - .5) * 2 * T.HW, Y = T.Y1 - v * (T.Y1 - T.Y0), ax = Math.abs(x);
    const lobe = Math.abs(Math.sin((Y - 12.35) * Math.PI / .5)), hw = w(Y) * (1 - .06 * (1 - lobe));
    if (ax > hw) return TRANSPARENT;
    const f = Math.cos(x / hw * Math.PI * 2.5);
    let col = mix(c.rufShade, c.ruf, smooth(-.8, .7, f) * .8 + .15);
    col = mix(col, c.rufLit, Math.max(0, f - .3) * .8 * smooth(1, .3, ax / hw));
    if (Math.abs(Y - 13.8) < .09) col = mix(col, c.rufDeep, .55);
    return mix(col, c.rufDeep, smooth(.75, 1, ax / hw) * .45 + smooth(12.9, 12.35, Y) * .35);
  };
}
// Closed canopy (four crossed cards): the folded black-indigo bundle, bulbous over the rosette
// and tapering to a thin white lace collar under the tip.
const bundleW = Y => Y < 15.7 ? 1.75 + .15 * smooth(15.3, 15.7, Y) : Y < 16.5 ? 1.9 - .05 * smooth(15.7, 16.5, Y)
  : Math.max(.42, 1.85 * (1 - Math.pow((Y - 16.5) / 5.9, 1.5)));
function npBundle() {
  const c = NPC(), B = NP.BUNDLE;
  return (u, v) => {
    const X = 8 - B.HW + u * 2 * B.HW, Y = B.Y1 - v * (B.Y1 - B.Y0), x = X - 8, ax = Math.abs(x);
    if (Y > 21.85) {
      const w = .5 - .08 * Math.abs(Math.sin(x * 14));
      if (ax > w) return TRANSPARENT;
      return mix(hex('#f6f2ec'), hex('#b9b0b8'), Math.abs(Math.sin(x * 9)) * .4 + smooth(.3, .5, ax) * .4);
    }
    const w = bundleW(Y);
    if (ax > w) return TRANSPARENT;
    const f = x / w;
    let col = mix(c.navyDeep, c.navy, Math.cos(f * Math.PI * 2.5) * .5 + .5);
    col = mix(col, c.navyLit, Math.max(0, Math.cos(f * Math.PI * 2.5 - .8)) * .5);
    if (Math.abs(f) > .85) col = mix(col, hex('#0e0c18'), .6);
    return Y < 15.5 ? mix(col, c.navyDeep, .5) : col;
  };
}
// Closed tip: a short gold ferrule and point (crossed cards spanning NP.TIP).
function npClosedTip() {
  const T = NP.TIP, w = profile([[22.05, .26], [22.22, .26], [22.3, .16], [22.56, .2], [22.9, 0]]);
  return (u, v) => {
    const x = (u - .5) * 2 * T.HW, Y = T.Y1 - v * (T.Y1 - T.Y0), hw = w(Y);
    if (Math.abs(x) > hw) return TRANSPARENT;
    return pal().goldTube(clamp(-x / Math.max(hw, .01) * .9 + .15, -1, 1));
  };
}
// Ruffle rosette core: vertical gold folds, shaded toward the bottom.
const npRuffleCore = () => (u, v) => {
  const c = NPC(), k = Math.cos(u * Math.PI * 6);
  return mix(mix(c.rufShade, c.rufLit, smooth(-.7, .9, k) * .85), c.rufShade, smooth(.5, 1, v) * .5);
};
const npFold = () => (u, v) => {
  const c = NPC();
  return mix(mix(c.navyDeep, c.navy, Math.cos(u * Math.PI * 5) * .5 + .5), c.navyLit, Math.max(0, Math.cos(u * Math.PI * 5 - .8)) * .4);
};
// The gathered rosette seen from above or below.
const npRosette = () => (u, v) => {
  const c = NPC(), x = (u - .5) * 2, z = (v - .5) * 2, r = Math.hypot(x, z), a = Math.atan2(z, x);
  if (r > .9 + .1 * Math.cos(a * 12)) return TRANSPARENT;
  if (r < .2) return c.hub;
  return ruffleTop(c, r, a / 4 * 3);
};
// Black crook handle with a gold cap (stacked cards spanning NP.CROOK), drawn in sprite px.
function npHandle() {
  const K = NP.CROOK, sx = X => (X - K.X0) / (K.X1 - K.X0) * 64, sy = Y => (K.Y1 - Y) / (K.Y1 - K.Y0) * 64;
  const pts = [[8, 8.6], [8, 7.4], [8, 6.3]];
  for (let k = 1; k <= 8; k++) { const t = -Math.PI * k / 8; pts.push([7.0 + Math.cos(t), 6.3 + Math.sin(t)]); }
  pts.push([6.0, 6.8]);
  const crook = new Stroke(pts.map(([X, Y]) => [sx(X), sy(Y)]), 11.5);
  return (u, v) => {
    const h = crook.hit(u * 64, v * 64);
    if (!h) return TRANSPARENT;
    const lit = (h.lx * LX + h.ly * LY) * Math.sqrt(1 - Math.pow(1 - h.e, 2));
    let col = mix(hex('#15111d'), hex('#4a4560'), clamp(lit * .9 + .15));
    if (h.t > .9 || h.t < .06) col = pal().goldTube(clamp(lit * 1.1 + .1, -1, 1));
    if (h.e > .8) col = mix(col, hex('#07050a'), .7);
    return col;
  };
}
const npShaft = () => (u, v) => mix(mix(hex('#2a2536'), hex('#0e0b14'), smooth(0, .5, Math.abs(u - .35))), hex('#5a5470'), Math.max(0, 1 - Math.abs(u - .32) / .06) * .5);
// Closed parasol's gold shaft between the cog and the rosette: a lit tube with a fine spiral.
const npGoldShaft = () => (u, v) => {
  let col = pal().goldTube(clamp(.55 - Math.abs(u - .3) * 2.6, -1, 1));
  if (((u * .8 + v * 3) % 1 + 1) % 1 < .12) col = mix(col, hex('#7a5a2a'), .45);
  return col;
};
const npGold = () => (u, v) => mix(mix(hex('#f6e3a2'), hex('#ac8048'), smooth(.05, .95, Math.abs(u - .3) * 1.3 + v * .25)), hex('#7a5a2a'), smooth(.85, 1, Math.max(Math.abs(u - .5), Math.abs(v - .5)) * 2) * .5);
const npCog = () => (u, v) => {
  const x = (u - .5) * 2, z = (v - .5) * 2, r = Math.hypot(x, z), a = Math.atan2(z, x);
  const tooth = smooth(-.1, .3, Math.cos(a * 10));
  if (r > .74 + .26 * tooth) return TRANSPARENT;
  let col = mix(hex('#f6e3a2'), hex('#ac8048'), smooth(-.5, 1, x * .6 + z * .8));
  if (r > .66 + .26 * tooth || Math.abs(r - .45) < .05) col = mix(col, hex('#7a5a2a'), .6);
  if (r < .3) col = mix(hex('#15111d'), hex('#ac8048'), smooth(.22, .3, r));
  return col;
};
const npPlaque = () => (u, v) => {
  const dx = Math.abs(u - .5) * 2, dy = Math.abs(v - .5) * 2, d = dx + dy;
  const spike = Math.max(0, 1 - Math.min(dx, dy) / .06) * (d < 1 ? 1 : 0);
  if (d > .78 && !spike) return TRANSPARENT;
  if (d > .56) return mix(hex('#f6e3a2'), hex('#ac8048'), smooth(.56, 1, d));
  let col = mix(hex('#9cc4ff'), hex('#2a4ab8'), smooth(0, .56, d + (u - .5) * .4));
  if (Math.hypot(u - .42, v - .4) < .07) col = hex('#ffffff');
  return col;
};
const npHub = () => (u, v) => (Math.abs(v - .12) < .06 || Math.abs(v - .88) < .06) ? npGold()(u, v) : mix(hex('#2a2438'), hex('#181423'), smooth(0, .5, Math.abs(u - .35)));

export function naviaWeaponSprites() {
  return {
    nv_head: [288, 336, nvHead()],
    nv_tip: [48, 128, nvTip()], nv_crystal: [48, 96, nvCrystal()], nv_crystal_core: [16, 48, nvCrystalCore()], nv_socket: [16, 64, nvSocket()],
    nv_shaft1: [32, 64, nvShaft1()], nv_shaft2: [32, 64, nvShaft2()], nv_collar: [32, 32, nvCollar()],
    nv_sleeve: [32, 96, nvSleeve()], nv_sleeve_crown: [16, 32, nvSleeveCrown()], nv_guard: [96, 48, nvGuard()], nv_wrap: [32, 128, nvWrap()],
    nv_butt: [48, 96, nvButt()], nv_gold: [32, 32, nvGold()], nv_rose: [32, 32, nvRose()],
    np_top: [256, 256, npTop()], np_lining: [256, 256, npLining()], np_profile: [256, 96, npProfile()],
    ...Object.fromEntries(NP.CANOPY.STEPS.map(([r], k) => ['np_dome' + k, [Math.max(64, Math.ceil(r * 28 / 16) * 16), Math.max(64, Math.ceil(r * 28 / 16) * 16), npDome(k)]])),
    np_drum_rib: [96, 80, npDrum('rib')], np_drum_emb: [96, 80, npDrum('a')], np_drum_fil: [96, 80, npDrum('b')],
    np_ruffle_u: [64, 32, npRuffle(NP.CANOPY.RUFFLE_U, 5, false)], np_ruffle_ub: [64, 32, npRuffle(NP.CANOPY.RUFFLE_U, 5, true)],
    np_ruffle_l: [64, 48, npRuffle(NP.CANOPY.RUFFLE_L, 4, false)], np_finial: [16, 64, npFinial()],
    np_crosette: [80, 48, npRosetteSide()], np_bundle: [64, 112, npBundle()], np_ctip: [16, 32, npClosedTip()],
    np_fold: [32, 64, npFold()], np_ruffle: [32, 32, npRuffleCore()], np_rosette: [64, 64, npRosette()],
    np_handle: [64, 64, npHandle()], np_shaft: [16, 64, npShaft()], np_gshaft: [16, 32, npGoldShaft()], np_gold: [32, 32, npGold()],
    np_cog: [64, 64, npCog()], np_plaque: [32, 32, npPlaque()], np_hub: [16, 32, npHub()],
  };
}
