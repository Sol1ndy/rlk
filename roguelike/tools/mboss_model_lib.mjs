// Item-model geometry helpers shared by the mid-boss display-entity rigs (Corrupted Guardian, Moonlit
// Butterfly, Field Generator). Moved out of guardian_geometry.mjs unchanged; the Guardian keeps thin wrappers for its defaults
// (the CARD rectangle of a sprite, its gold ledge/knob textures).
//
// Authoring frame ("A-frame", the rig's frame): +X = her LEFT (screen right in a front view),
// +Y up, -Z forward; units are model units relative to the display pivot (model [8,8,8]).
// Item models render x-mirrored in that frame (see build_raiden_rig.mjs), so every element is
// converted with model = (8 - X, 8 + Y, 8 + Z); element rotations about y/z flip sign. Cards
// show their sprite as painted (front view) from -Z; texture coordinates are solved per face
// from the A-frame position of each corner, so the conversion never mirrors a sprite.
//
// Constraints kept by every model: coordinates within -16..32 (checkBounds), element rotations
// single-axis in 22.5 degree steps within +-45 (rotM throws otherwise).
export const r4 = v => Math.round(v * 1e4) / 1e4;
export const toM = ([X, Y, Z]) => [8 - X, 8 + Y, 8 + Z];
export const FACE_OF = {front: 'north', back: 'south', left: 'west', right: 'east', up: 'up', down: 'down'};
const corners = (face, [x0, y0, z0], [x1, y1, z1]) => ({
  north: [[x1, y1, z0], [x0, y1, z0], [x0, y0, z0], [x1, y0, z0]],
  south: [[x0, y1, z1], [x1, y1, z1], [x1, y0, z1], [x0, y0, z1]],
  east: [[x1, y1, z1], [x1, y1, z0], [x1, y0, z0], [x1, y0, z1]],
  west: [[x0, y1, z0], [x0, y1, z1], [x0, y0, z1], [x0, y0, z0]],
  up: [[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]],
  down: [[x0, y0, z1], [x1, y0, z1], [x1, y0, z0], [x0, y0, z0]],
})[face];
export function solveUV(face, lo, hi, fn) {
  const D = corners(face, lo, hi).map(fn), eq = (a, b) => Math.abs(a - b) < 1e-5;
  for (let k = 0; k < 4; k++) {
    const u = [0, 1, 2, 3].map(j => D[(j + k) % 4]);
    if (eq(u[0][1], u[1][1]) && eq(u[1][0], u[2][0]) && eq(u[2][1], u[3][1]) && eq(u[3][0], u[0][0]))
      return [[u[0][0], u[0][1], u[2][0], u[2][1]].map(v => r4(Math.min(16, Math.max(0, v)))), k * 90];
  }
  throw new Error('no uv solution for ' + face);
}
export const rotM = rot => {
  if (!rot) return undefined;
  const [axis, angle, origin] = rot;
  if (![-45, -22.5, 22.5, 45].includes(angle)) throw new Error('element rotation ' + angle);
  return {origin: toM(origin).map(r4), axis, angle: axis === 'x' ? angle : -angle};
};
// Box in the A-frame. tex: sprite name, or {all, front, back, left, right, up, down, uv}.
export function abox(a, b, tex, {rot, shade = true, uv = [0, 0, 16, 16], drop = []} = {}) {
  const lo = a.map((v, i) => Math.min(v, b[i])), hi = a.map((v, i) => Math.max(v, b[i]));
  const from = [8 - hi[0], 8 + lo[1], 8 + lo[2]].map(r4), to = [8 - lo[0], 8 + hi[1], 8 + hi[2]].map(r4);
  const spec = typeof tex === 'string' ? {all: tex} : tex;
  const faces = {};
  for (const [af, mf] of Object.entries(FACE_OF)) {
    if (drop.includes(af)) continue;
    const t = spec[af] || spec.all;
    if (!t) continue;
    faces[mf] = {texture: '#' + t, uv: (spec.uv && spec.uv[af]) || uv};
  }
  const el = {from, to, faces};
  if (!shade) el.shade = false;
  const r = rotM(rot);
  if (r) el.rotation = r;
  return el;
}
// Card in the plane Z = z, spanning rect {X0,X1,Y0,Y1} (A-frame, required), sprite as painted, seen from -Z.
// uvr = sprite sub-rectangle [u0, v0, u1, v1] in 0..1; flipU mirrors the sprite left-right.
export function cardZ(sprite, z, rect, {uvr = [0, 0, 1, 1], flipU = false, rot, shade = false, tint = false} = {}) {
  const {X0, X1, Y0, Y1} = rect;
  const from = [8 - X1, 8 + Y0, 8 + z].map(r4), to = [8 - X0, 8 + Y1, 8 + z].map(r4);
  const fn = p => {
    const X = 8 - p[0], Y = p[1] - 8;
    let s = (X - X0) / (X1 - X0);
    if (flipU) s = 1 - s;
    const t = (Y1 - Y) / (Y1 - Y0);
    return [16 * (uvr[0] + (uvr[2] - uvr[0]) * s), 16 * (uvr[1] + (uvr[3] - uvr[1]) * t)];
  };
  const faces = {};
  for (const f of ['north', 'south']) {
    const [uv, r] = solveUV(f, from, to, fn);
    faces[f] = {texture: '#' + sprite, uv, ...(r ? {rotation: r} : {}), ...(tint ? {tintindex: 0} : {})};
  }
  const el = {from, to, faces};
  if (!shade) el.shade = false;
  const r = rotM(rot);
  if (r) el.rotation = r;
  return el;
}
// Card in the plane X = x: u runs along +Z (toward her back) over Z0..Z1, v top to bottom.
export function cardX(sprite, x, {Z0, Z1, Y0, Y1}, {uvr = [0, 0, 1, 1], flipU = false, rot, shade = false, tint = false} = {}) {
  const from = [8 - x, 8 + Y0, 8 + Z0].map(r4), to = [8 - x, 8 + Y1, 8 + Z1].map(r4);
  const fn = p => {
    const Z = p[2] - 8, Y = p[1] - 8;
    let s = (Z - Z0) / (Z1 - Z0);
    if (flipU) s = 1 - s;
    const t = (Y1 - Y) / (Y1 - Y0);
    return [16 * (uvr[0] + (uvr[2] - uvr[0]) * s), 16 * (uvr[1] + (uvr[3] - uvr[1]) * t)];
  };
  const faces = {};
  for (const f of ['east', 'west']) {
    const [uv, r] = solveUV(f, from, to, fn);
    faces[f] = {texture: '#' + sprite, uv, ...(r ? {rotation: r} : {}), ...(tint ? {tintindex: 0} : {})};
  }
  const el = {from, to, faces};
  if (!shade) el.shade = false;
  const r = rotM(rot);
  if (r) el.rotation = r;
  return el;
}
export const shiftRect = (r, dx = 0, dy = 0) => ({X0: r.X0 + dx, X1: r.X1 + dx, Y0: r.Y0 + dy, Y1: r.Y1 + dy});
export const mirrorRect = r => ({X0: -r.X1, X1: -r.X0, Y0: r.Y0, Y1: r.Y1});
export const plate = (sprite, cx, cy, size, z, opt) => cardZ(sprite, z, {X0: cx - size / 2, X1: cx + size / 2, Y0: cy - size / 2, Y1: cy + size / 2}, opt);
export const cube = (c, s, tex, rot) => abox([c[0] - s / 2, c[1] - s / 2, c[2] - s / 2], [c[0] + s / 2, c[1] + s / 2, c[2] + s / 2], tex, {rot: rot ? [rot[0], rot[1], c] : undefined});

// ---- turned (lathe) geometry --------------------------------------------------------------
// A round section is a ring of n flat facets (16 by default) about an axis. Each facet is a
// one-face card turned to its azimuth (single-axis element rotations in 22.5 degree steps), so
// the outline is round from every side. The facets are unshaded: their wrap-round texture
// carries the light (a metal highlight toward the side most views see), like the painted cards,
// so the gold keeps its colour instead of the game's dim side-face shading. All facets of one
// lathe share that texture: u = azimuth (facet k shows [k/n, (k+1)/n] of
// the sprite, azimuth 0 = e0 below), v = position along the axis (vFrom -> 0, vTo -> 1).
export const AXV = {x: [1, 0, 0], y: [0, 1, 0], z: [0, 0, 1]};
export const AZV = {y: [[0, 0, -1], [1, 0, 0]], x: [[0, 0, -1], [0, 1, 0]], z: [[0, 1, 0], [1, 0, 0]]};
export const D2R = Math.PI / 180;
export const vadd = (a, b) => a.map((x, i) => x + b[i]), vsub = (a, b) => a.map((x, i) => x - b[i]);
export const vsc = (v, s) => v.map(x => x * s), vdot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
// Right-handed rotation about an A-frame axis (the sense of `rot` in abox / cardZ / cardX).
export function rotA(axis, deg, [x, y, z]) {
  const c = Math.cos(deg * D2R), s = Math.sin(deg * D2R);
  if (axis === 'x') return [x, y * c - z * s, y * s + z * c];
  if (axis === 'y') return [x * c + z * s, y, -x * s + z * c];
  return [x * c - y * s, x * s + y * c, z];
}
export const faceOfDir = d => (d[0] > .5 ? 'left' : d[0] < -.5 ? 'right' : d[1] > .5 ? 'up' : d[1] < -.5 ? 'down' : d[2] > .5 ? 'back' : 'front');
// Element spanning the A-frame points pts, with only the listed faces; a face's fn(P) maps its
// A-frame corner points (before the element rotation) to texture [u, v] in 0..16.
export function faceEl(pts, faces, {rot, shade = true} = {}) {
  const lo = [0, 1, 2].map(i => Math.min(...pts.map(p => p[i]))), hi = [0, 1, 2].map(i => Math.max(...pts.map(p => p[i])));
  const from = [8 - hi[0], 8 + lo[1], 8 + lo[2]].map(r4), to = [8 - lo[0], 8 + hi[1], 8 + hi[2]].map(r4);
  const out = {};
  for (const [af, {tex, fn, uv}] of Object.entries(faces)) {
    const mf = FACE_OF[af];
    if (fn) {
      const [u, r] = solveUV(mf, from, to, p => fn([8 - p[0], p[1] - 8, p[2] - 8]));
      out[mf] = {texture: '#' + tex, uv: u, ...(r ? {rotation: r} : {})};
    } else out[mf] = {texture: '#' + tex, uv: uv || [0, 0, 16, 16]};
  }
  const el = {from, to, faces: out};
  if (!shade) el.shade = false;
  const r = rotM(rot);
  if (r) el.rotation = r;
  return el;
}
// sections: [{a: [a0, a1] along the axis from c, r: facet inradius, tex}]
// Options (all off by default; the defaults reproduce the original facets exactly):
//   tile    every facet shows the whole sprite width (u = 16 (.5 + s / w)) instead of its 1/n slice of a wrap-round
//           sprite: a repeating band (a square-wave seam, block joints) needs only one small tile;
//   inward  the facets face the axis (an inner wall seen from inside the ring); u runs so that the sprite reads
//           unmirrored from the inside, and a wrap-round sprite keeps its order round the ring;
//   range   [k0, k1): only facets k0 <= k < k1 (k may be negative), for arcs (a protractor, a curved bracket);
//   phase   degrees added to every facet azimuth (the facet rotation must stay a multiple of 22.5 within +-45,
//           e.g. a 4-facet diamond with phase 45);
// and a section's tex may be a function k -> sprite (per-facet variants, e.g. a light level baked per azimuth).
export function lathe(axis, c, sections, {vFrom, vTo, n = 16, tile = false, inward = false, range = null, phase = 0}) {
  const A = AXV[axis], [e0, e1] = AZV[axis], dirs = [e0, e1, vsc(e0, -1), vsc(e1, -1)], els = [];
  const [k0, k1] = range || [0, n], sgn = inward ? -1 : 1;
  for (const {a: [a0, a1], r, tex} of sections) {
    const w = 2 * r * Math.tan(Math.PI / n);
    for (let k = k0; k < k1; k++) {
      const phi = k * 360 / n + phase, q = Math.round(phi / 90), g = phi - 90 * q, d = dirs[((q % 4) + 4) % 4], t = dirs[(((q + 1) % 4) + 4) % 4];
      const P = (a, s) => vadd(vadd(c, vsc(A, a)), vadd(vsc(d, r), vsc(t, s)));
      const kk = inward ? n - 1 - k : k, tx = typeof tex === 'function' ? tex(k) : tex;
      const fn = X => { const rel = vsub(X, c), s = sgn * vdot(rel, t) / w, v = 16 * (vdot(rel, A) - vFrom) / (vTo - vFrom);
        return [tile ? 16 * (.5 + s) : 16 * (kk + .5 + s) / n, v]; };
      const sg = vdot(rotA(axis, 10, d), t) > 0 ? 1 : -1;
      els.push(faceEl([P(a0, -w / 2), P(a1, w / 2)], {[faceOfDir(inward ? vsc(d, -1) : d)]: {tex: tx, fn}},
        {shade: false, rot: g ? [axis, sg * g, vadd(c, vsc(A, (a0 + a1) / 2))] : undefined}));
    }
  }
  return els;
}
// Flat annulus across the axis at a (r0..r1), as n segment quads that match the facets of a lathe of inradius r1
// (the outer edge is the same n-gon; each quad spans r0..r1 radially and the outer facet width tangentially, so
// neighbours overlap in a thin wedge near the inner edge). side '+', '-' or '+-' (faces toward +axis / -axis).
// Options:
//   stagger  offset of the odd segments along the axis (toward the face side): the overlapping wedges of
//            neighbouring quads never z-fight;
//   tile     (default) every quad shows the whole sprite: u across the segment, v from the outer edge (0) to the
//            inner edge (1); seen from either side the sprite reads unmirrored. tile false: one wrap-round sprite,
//            u = azimuth slice k/n..(k+1)/n as lathe();
//   range    [k0, k1) segments only; shade (default true) the game's face shading; tex may be a function k -> sprite.
export function annulus(axis, c, a, r0, r1, side, tex, {n = 16, stagger = 0, tile = true, range = null, shade = true} = {}) {
  const A = AXV[axis], [e0, e1] = AZV[axis], dirs = [e0, e1, vsc(e0, -1), vsc(e1, -1)], els = [];
  const [k0, k1] = range || [0, n], w = 2 * r1 * Math.tan(Math.PI / n);
  for (let k = k0; k < k1; k++) {
    const phi = k * 360 / n, q = Math.round(phi / 90), g = phi - 90 * q, d = dirs[((q % 4) + 4) % 4], t = dirs[(((q + 1) % 4) + 4) % 4];
    const sg = vdot(rotA(axis, 10, d), t) > 0 ? 1 : -1;
    const odd = ((k % 2) + 2) % 2 === 1;
    const lift = odd ? stagger * (side === '-' ? -1 : 1) : 0, O = vadd(c, vsc(A, a + lift));
    const P = (rad, s) => vadd(O, vadd(vsc(d, rad), vsc(t, s)));
    const faces = {};
    for (const sd of side) {
      const m = sd === '+' ? 1 : -1;
      const fn = X => { const rel = vsub(X, O), s = vdot(rel, t) / w, rad = vdot(rel, d);
        return [tile ? 16 * (.5 + m * s) : 16 * (k + .5 + m * s) / n, 16 * (r1 - rad) / (r1 - r0)]; };
      faces[faceOfDir(vsc(A, m))] = {tex: typeof tex === 'function' ? tex(k) : tex, fn};
    }
    els.push(faceEl([P(r0, -w / 2), P(r1, w / 2)], faces, {shade, rot: g ? [axis, sg * g, O] : undefined}));
  }
  return els;
}
// Round end/ledge disc across the axis at a; side '+', '-' or '+-'. Discs are inscribed in the
// ring they close (R = its facet inradius x 0.995) so they never show past the facets from the
// side. A plain disc (gold sprite, game-shaded) closes a real armour step; a polar disc is
// unshaded and maps its sprite so that the sprite angle atan2(u - .5, v - .5) is the lathe
// azimuth, so a polar sprite painted per azimuth matches the facets beside it.
export function disc(axis, c, a, R, side, tex, polar = false) {
  const A = AXV[axis], [e0, e1] = AZV[axis], O = vadd(c, vsc(A, a));
  const P = (i, j) => vadd(O, vadd(vsc(e0, i * R), vsc(e1, j * R)));
  const fn = polar ? X => { const rel = vsub(X, O); return [16 * (.5 + vdot(rel, e1) / (2 * R)), 16 * (.5 + vdot(rel, e0) / (2 * R))]; } : undefined;
  const faces = {};
  for (const sd of side) faces[faceOfDir(vsc(A, sd === '+' ? 1 : -1))] = {tex, fn};
  return faceEl([P(-1, -1), P(1, 1)], faces, {shade: !polar});
}
export const DK = .995;
// Smooth turned solid: the radius profile prof(a) sampled on the stations `at` (ascending along
// the axis). Section i spans [at[i], at[i+1]] at the radius of its midpoint and reaches 0.02 into
// a wider neighbour; each step is closed by a polar ledge disc painted like the surface, so the
// steps vanish and the outline follows the profile. ends '-' / '+' close the first / last station.
export function turned(axis, c, at, prof, tex, ledge, V, ends = '') {
  const rs = at.slice(1).map((x, i) => prof((at[i] + x) / 2)), secs = [], els = [];
  rs.forEach((r, i) => secs.push({a: [at[i] - (i > 0 && rs[i - 1] > r ? .02 : 0), at[i + 1] + (i < rs.length - 1 && rs[i + 1] > r ? .02 : 0)], r, tex}));
  for (let i = 0; i < rs.length - 1; i++) if (Math.abs(rs[i] - rs[i + 1]) > 1e-3)
    els.push(disc(axis, c, at[i + 1], Math.max(rs[i], rs[i + 1]) * DK, rs[i] > rs[i + 1] ? '+' : '-', ledge, true));
  if (ends.includes('-')) els.push(disc(axis, c, at[0], rs[0] * DK, '-', ledge, true));
  if (ends.includes('+')) els.push(disc(axis, c, at[at.length - 1], rs[rs.length - 1] * DK, '+', ledge, true));
  return [...lathe(axis, c, secs, V), ...els];
}
export const stations = (a0, a1, n) => Array.from({length: n + 1}, (_, i) => a0 + (a1 - a0) * i / n);
// Turned knob: a sphere of radius R in twelve bands of equal angle (shoulder, elbow).
export function knob(axis, c, R, tex, ledge) {
  const at = Array.from({length: 13}, (_, i) => R * Math.sin((-90 + 15 * i) * D2R));
  return turned(axis, c, at, a => R * Math.sqrt(Math.max(0, 1 - (a / R) ** 2)), tex, ledge, {vFrom: R, vTo: -R}, '-+');
}
// Straight taper along Y from radius r0 at y0 down to r1 at y1 in n sections.
export const taperY = (y0, y1, r0, r1, n, tex, ledge, V) => turned('y', [0, 0, 0], stations(y1, y0, n), y => r1 + (r0 - r1) * (y - y1) / (y0 - y1), tex, ledge, V);

// Every element must stay within the item-model range -16..32.
export function checkBounds(name, els) {
  for (const e of els) for (const v of [...e.from, ...e.to]) if (v < -16 || v > 32) throw new Error(`model ${name} leaves -16..32: ${e.from} ${e.to}`);
}

// Mirror image of a model in X (model x -> 16 - x): her left side's part becomes her right side's. Faces swap
// east/west and every texture is flipped across the mirrored direction (u for UV rotation 0/180, v for 90/270),
// element rotations about y and z change sign. No negative display scale is needed.
export function mirrorModel(els) {
  return els.map(e => {
    const faces = {};
    for (const [f, face] of Object.entries(e.faces)) {
      const uv = face.uv.slice(), rot = face.rotation || 0;
      if (rot === 0 || rot === 180) [uv[0], uv[2]] = [uv[2], uv[0]]; else [uv[1], uv[3]] = [uv[3], uv[1]];
      faces[f === 'east' ? 'west' : f === 'west' ? 'east' : f] = {...face, uv};
    }
    const out = {...e, from: [r4(16 - e.to[0]), e.from[1], e.from[2]], to: [r4(16 - e.from[0]), e.to[1], e.to[2]], faces};
    if (e.rotation) out.rotation = {...e.rotation, origin: [r4(16 - e.rotation.origin[0]), e.rotation.origin[1], e.rotation.origin[2]],
      angle: e.rotation.axis === 'x' ? e.rotation.angle : -e.rotation.angle};
    return out;
  });
}
// Horizontal card in the plane Y = y over {X0, X1, Z0, Z1} (A-frame): the sprite's u runs along +X, v along +Z
// (toward her back), seen from above and below.
export function cardY(sprite, y, {X0, X1, Z0, Z1}, {shade = false, tint = false} = {}) {
  const fn = ([X, , Z]) => [16 * (X - X0) / (X1 - X0), 16 * (Z - Z0) / (Z1 - Z0)];
  const el = faceEl([[X0, y, Z0], [X1, y, Z1]], {up: {tex: sprite, fn}, down: {tex: sprite, fn}}, {shade});
  if (tint) for (const f of Object.values(el.faces)) f.tintindex = 0;
  return el;
}
// Moves every element of a model by d (A-frame units).
export function shiftModel(els, [dx, dy, dz]) {
  return els.map(e => {
    const out = {...e, from: [r4(e.from[0] - dx), r4(e.from[1] + dy), r4(e.from[2] + dz)], to: [r4(e.to[0] - dx), r4(e.to[1] + dy), r4(e.to[2] + dz)]};
    if (e.rotation) out.rotation = {...e.rotation, origin: [r4(e.rotation.origin[0] - dx), r4(e.rotation.origin[1] + dy), r4(e.rotation.origin[2] + dz)]};
    return out;
  });
}
