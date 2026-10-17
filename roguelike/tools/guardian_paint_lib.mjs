// Shared 2D painting toolkit for the Corrupted Guardian (파수꾼・타락) sprites.
// Pure Node. Builds on the PNG writer and colour helpers of weapon_paint.mjs.
//
// Coordinates: every sprite is painted in "card units" (X to the right as seen from the front,
// Y up), and the geometry places a card on exactly the same rectangle. Feathers, panels and
// blades are vector shapes (cubic paths with width profiles, polygons, arcs) sampled per pixel
// with 4x supersampling. Opaque sprites are alpha-cut at 0.5 (paint); glow sprites keep their
// alpha (paintT).
import {hex, clamp, smooth, mix, fbm, TRANSPARENT} from './weapon_paint.mjs';

export {hex, clamp, smooth, mix, fbm, TRANSPARENT};
export const C = s => (typeof s === 'string' ? hex(s) : s);
export const shade = (c, k) => [c[0] * k, c[1] * k, c[2] * k, c[3] ?? 255];
export const lerp = (a, b, t) => a + (b - a) * t;

// Translucent painter: averages premultiplied colour and keeps fractional alpha (glow cards).
export function paintT(w, h, fn, ss = 3) {
  const buf = Buffer.alloc(w * h * 4);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const acc = [0, 0, 0, 0];
    for (let j = 0; j < ss; j++) for (let i = 0; i < ss; i++) {
      const c = fn((x + (i + .5) / ss) / w, (y + (j + .5) / ss) / h);
      const a = c[3] / 255;
      acc[0] += c[0] * a; acc[1] += c[1] * a; acc[2] += c[2] * a; acc[3] += a;
    }
    const o = (y * w + x) * 4, n = ss * ss, alpha = acc[3] / n;
    buf[o + 3] = Math.round(clamp(alpha) * 255);
    for (let k = 0; k < 3; k++) buf[o + k] = Math.round(clamp(acc[3] > 0 ? acc[k] / acc[3] : 0, 0, 255));
  }
  return buf;
}

// Sprite on a card rectangle: X0..X1 left to right, Y0 (bottom)..Y1 (top) in card units.
// fn(X, Y) returns rgba or null. The result is the (u, v) painter expected by paint().
export const onCard = ({X0, X1, Y0, Y1}, fn) => (u, v) => fn(X0 + u * (X1 - X0), Y1 - v * (Y1 - Y0)) || TRANSPARENT;

// ---- curves -------------------------------------------------------------------------------
export function cubic(p0, p1, p2, p3, n = 28) {
  const out = [];
  for (let i = 0; i <= n; i++) {
    const t = i / n, a = (1 - t) ** 3, b = 3 * (1 - t) ** 2 * t, c = 3 * (1 - t) * t * t, d = t ** 3;
    out.push([a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]]);
  }
  return out;
}
// Catmull-Rom through the points; a point with a third entry 'c' keeps a sharp corner.
export function spline(pts, n = 8) {
  const out = [];
  const flush = P => {
    for (let i = 0; i < P.length - 1; i++) {
      const p0 = P[Math.max(0, i - 1)], p1 = P[i], p2 = P[i + 1], p3 = P[Math.min(P.length - 1, i + 2)];
      for (let k = 0; k < n; k++) {
        if (k === 0 && i === 0 && out.length) continue;
        const t = k / n, t2 = t * t, t3 = t2 * t;
        out.push([0, 1].map(a => .5 * (2 * p1[a] + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t2 + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t3)));
      }
    }
    out.push([P[P.length - 1][0], P[P.length - 1][1]]);
  };
  let run = [pts[0]];
  for (let i = 1; i < pts.length; i++) {
    run.push(pts[i]);
    if (pts[i][2] === 'c' || i === pts.length - 1) { flush(run); run = [pts[i]]; }
  }
  return out;
}
// Polyline with arc length, nearest-point queries and a bounding box.
export class Path {
  constructor(pts) {
    this.p = pts;
    this.seg = [];
    let L = 0;
    for (let i = 0; i < pts.length - 1; i++) {
      const [ax, ay] = pts[i], [bx, by] = pts[i + 1], len = Math.hypot(bx - ax, by - ay) || 1e-9;
      this.seg.push({ax, ay, dx: (bx - ax) / len, dy: (by - ay) / len, len, l0: L});
      L += len;
    }
    this.L = L;
    const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
    this.box = [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)];
  }
  // {d: distance, t: 0..1 arc fraction, s: signed offset (+ = left of travel), tx, ty: tangent}
  near(x, y) {
    let best = null;
    for (const g of this.seg) {
      const qx = x - g.ax, qy = y - g.ay;
      const a = Math.max(0, Math.min(g.len, qx * g.dx + qy * g.dy));
      const ex = qx - a * g.dx, ey = qy - a * g.dy, d2 = ex * ex + ey * ey;
      if (!best || d2 < best.d2) best = {d2, l: g.l0 + a, s: g.dx * qy - g.dy * qx, tx: g.dx, ty: g.dy, a, g};
    }
    // Beyond the ends: extend along the end tangents so profiles close cleanly.
    return {d: Math.sqrt(best.d2), t: best.l / this.L, s: best.s, tx: best.tx, ty: best.ty};
  }
  at(t) {
    const l = clamp(t) * this.L;
    for (const g of this.seg) if (l <= g.l0 + g.len + 1e-9) {
      const a = l - g.l0;
      return [g.ax + g.dx * a, g.ay + g.dy * a, g.dx, g.dy];
    }
    const g = this.seg[this.seg.length - 1];
    return [g.ax + g.dx * g.len, g.ay + g.dy * g.len, g.dx, g.dy];
  }
}
export function inPoly(P, x, y) {
  let c = false;
  for (let i = 0, j = P.length - 1; i < P.length; j = i++) {
    const [xi, yi] = P[i], [xj, yj] = P[j];
    if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c;
  }
  return c;
}
export function distPoly(P, x, y, closed = true) {
  let d = Infinity;
  const n = P.length;
  for (let i = 0; i < (closed ? n : n - 1); i++) {
    const [ax, ay] = P[i], [bx, by] = P[(i + 1) % n];
    const dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy || 1e-12;
    const t = clamp(((x - ax) * dx + (y - ay) * dy) / l2);
    d = Math.min(d, Math.hypot(x - ax - t * dx, y - ay - t * dy));
  }
  return d;
}
// Signed distance to a closed polygon (negative inside) with a cached bounding box.
export class Shape {
  constructor(P) {
    this.P = P;
    const xs = P.map(p => p[0]), ys = P.map(p => p[1]);
    this.box = [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)];
  }
  sd(x, y, pad = 0) {
    const [a, b, c, d] = this.box;
    if (x < a - pad || x > c + pad || y < b - pad || y > d + pad) return Infinity;
    const e = distPoly(this.P, x, y);
    return inPoly(this.P, x, y) ? -e : e;
  }
}
// Mirror a point list in X (about x = 0).
export const mirrorX = P => P.map(([x, y, k]) => (k ? [-x, y, k] : [-x, y]));
// Four-pointed star: signed "inside" measure (>0 inside), r = point length, k = waist (0..1).
export function star4in(dx, dy, rx, ry = rx, k = .28) {
  const ax = Math.abs(dx) / rx, ay = Math.abs(dy) / ry;
  // Concave diamond: |x|^p + |y|^p <= 1 with p < 1 gives the concave-sided 4-point star.
  const p = .55 + k;
  return 1 - (Math.pow(ax, p) + Math.pow(ay, p));
}

// Deterministic PRNG (mulberry32) for jittered feather layouts.
export function rng(seed) {
  let a = seed >>> 0;
  return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}

// ---- feathers -----------------------------------------------------------------------------
// A feather is a centre path (root -> tip) with a half-width profile on each side.
//   prof(t) -> [left, right] half widths (left = to the left of travel)
//   notches: [[t, side(+1 left / -1 right), depth, width]] thin slits cut from the edge
//            inward and back toward the root (torn-feather look); depth/width in card units
// sample(x, y, extra) returns null or {t, s, e (0 at the edge .. 1 on the rachis), side, edge, w};
// extra > 0 grows the feather (used to cast soft shadows of the feathers in front).
export class Feather {
  constructor(path, prof, {notches = []} = {}) {
    this.path = path instanceof Path ? path : new Path(path);
    this.prof = prof;
    this.notches = notches;
    let wmax = 0;
    for (let i = 0; i <= 20; i++) { const [l, r] = prof(i / 20); wmax = Math.max(wmax, l, r); }
    const [a, b, c, d] = this.path.box;
    this.box = [a - wmax - 1, b - wmax - 1, c + wmax + 1, d + wmax + 1];
  }
  sample(x, y, extra = 0) {
    const [a, b, c, d] = this.box;
    if (x < a - extra || x > c + extra || y < b - extra || y > d + extra) return null;
    const n = this.path.near(x, y);
    if (n.t <= 0 && n.d > 1e-6) {
      const [rl, rr] = this.prof(0);
      if (n.d > Math.max(rl, rr) * .6 + extra) return null;
    }
    if (n.t >= 1 - 1e-6 && n.d > 1e-3 + extra) return null;
    const side = n.s >= 0 ? 1 : -1;
    const [wl, wr] = this.prof(n.t);
    const w = (side > 0 ? wl : wr) + extra;
    const off = Math.abs(n.s);
    if (off > w) return null;
    const edge = w - off;
    if (!extra) {
      for (const [nt, ns, depth, width] of this.notches) {
        if (ns !== side || edge > depth) continue;
        const u = (n.t - nt) * this.path.L, uc = -edge * 1.25;
        if (Math.abs(u - uc) < width * (1 - edge / depth) + .02) return null;
      }
    }
    return {t: n.t, s: n.s, e: 1 - off / Math.max(w, 1e-6), side, edge, w};
  }
}
// Standard lanceolate profile: narrow root, broad body, long point.
export function bladeProfile({w = 1, lead = .42, root = .45, peak = .3, tip = .72, tipPow = 1.15} = {}) {
  return t => {
    let k;
    if (t < peak) k = root + (1 - root) * Math.sin(t / peak * Math.PI / 2);
    else if (t < tip) k = 1 - .08 * (t - peak) / (tip - peak);
    else k = .92 * Math.pow(Math.max(0, 1 - (t - tip) / (1 - tip)), tipPow);
    return [w * k * lead * 2, w * k * (1 - lead) * 2];
  };
}
// Rounded scale (coverts): broad, round end.
export function roundProfile({w = 1, lead = .5} = {}) {
  return t => {
    const k = t < .75 ? .55 + .45 * Math.sin(Math.min(1, t / .5) * Math.PI / 2) : Math.sqrt(Math.max(0, 1 - ((t - .75) / .25) ** 2));
    return [w * k * lead * 2, w * k * (1 - lead) * 2];
  };
}
// Feather path from a root, an angle (degrees from straight down, + toward +X) and a bend.
export function featherPath(root, angDeg, L, bend = [0, 0, 0], n = 24) {
  const a = angDeg * Math.PI / 180, dir = [Math.sin(a), -Math.cos(a)], perp = [Math.cos(a), Math.sin(a)];
  const P = (f, b) => [root[0] + dir[0] * L * f + perp[0] * L * b, root[1] + dir[1] * L * f + perp[1] * L * b];
  return cubic(root, P(1 / 3, bend[0]), P(2 / 3, bend[1]), P(1, bend[2]), n);
}

// Shading of a white feather: rachis, barbs, trailing-vane shade, outline, sky bounce.
export const FEATHER_WHITE = {
  base: C('#f5f1f0'), light: C('#ffffff'), shadeC: C('#d5cfd6'), deep: C('#a49ca8'), line: C('#6a6170'), sky: C('#bcc4da'),
};
export const FEATHER_CREAM = {
  base: C('#f6e6c2'), light: C('#fff6df'), shadeC: C('#e2c58e'), deep: C('#c9a86e'), line: C('#7a5a34'), sky: C('#e9d7b0'),
};
export function featherColour(h, pal = FEATHER_WHITE, {px = .06, rachis = true, barbs = true, trail = -1, grain = null, gx = 0, gy = 0, sky = 0} = {}) {
  // h from Feather.sample; px = card units per pixel (outline width)
  let c = pal.base;
  const e = h.e;
  // trailing vane (side == trail) is shaded toward its edge, the leading vane stays light
  if (h.side === trail) c = mix(c, pal.shadeC, (1 - e) * .75);
  else c = mix(c, pal.light, .35 * e);
  c = mix(c, pal.shadeC, smooth(.55, 1, h.t) * .25);
  if (sky) c = mix(c, pal.sky, sky * smooth(.3, 1, h.t));
  if (barbs) {
    // fine barbs slanting toward the tip
    const off = Math.abs(h.s), ph = (h.t * 22 - off * 3.2) % 1;
    const bl = Math.abs(ph - .5);
    if (bl < .06) c = mix(c, pal.shadeC, .28 * (1 - e * .5));
  }
  if (rachis && h.t < .93) {
    const r = Math.abs(h.s) / Math.max(h.w, 1e-6);
    if (r < .07) c = mix(c, pal.light, .8);
    else if (r < .13 && h.s < 0) c = mix(c, pal.shadeC, .55);
  }
  if (grain) c = mix(c, pal.deep, (grain(gx, gy) - .5) * .18);
  // outline (about 1.3 px)
  if (h.edge < px * 1.3) c = mix(c, pal.line, .85);
  else if (h.edge < px * 2.4) c = mix(c, pal.deep, .35);
  return c;
}
// Composite a list of {f: Feather, col: h => rgba} front-to-back: the first hit wins.
export function firstHit(list, x, y, shadow = 0) {
  for (let i = 0; i < list.length; i++) {
    const h = list[i].f.sample(x, y);
    if (!h) continue;
    let c = list[i].col(h, x, y);
    if (shadow > 0) {
      // soft contact shadow where a feather in front lies within `shadow` units
      for (let j = 0; j < i; j++) {
        const g = list[j].f.sample(x, y, shadow);
        if (g) { const k = 1 - Math.min(1, -g.edge / shadow + 1); c = mix(c, [120, 110, 125, 255], .32 * (1 - Math.abs(g.edge) / shadow)); break; }
      }
    }
    return c;
  }
  return null;
}
