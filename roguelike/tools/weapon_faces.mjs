// UV-mapped boxes for the painted player weapons (see weapon_paint.mjs).
// box(from, to, spec): spec.front (faces facing +-Z), spec.side (+-X) and spec.cap (+-Y) are
// {sprite, u:[axis, a, b], v:[axis, a, b]} — texture u runs from 0 at model coordinate a to
// 1 at b along that in-plane axis (v likewise); a spec may instead give uv:[u0,v0,u1,v1]
// directly (fractions) for a fixed sub-rectangle. Missing groups fall back to spec.front's
// sprite with a fixed full-texture mapping. rotation is the usual element rotation object.
const FACES = {z: ['north', 'south'], x: ['east', 'west'], y: ['up', 'down']};
const corners = (face, [x0, y0, z0], [x1, y1, z1]) => ({
  north: [[x1, y1, z0], [x0, y1, z0], [x0, y0, z0], [x1, y0, z0]],
  south: [[x0, y1, z1], [x1, y1, z1], [x1, y0, z1], [x0, y0, z1]],
  east: [[x1, y1, z1], [x1, y1, z0], [x1, y0, z0], [x1, y0, z1]],
  west: [[x0, y1, z0], [x0, y1, z1], [x0, y0, z1], [x0, y0, z0]],
  up: [[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]],
  down: [[x0, y0, z1], [x1, y0, z1], [x1, y0, z0], [x0, y0, z0]],
})[face];
const r4 = v => Math.round(v * 1e4) / 1e4;
// Face uv + rotation so every corner shows fn(corner) (vanilla corner order / uv rotation).
function solveUV(face, lo, hi, fn) {
  const D = corners(face, lo, hi).map(fn), eq = (a, b) => Math.abs(a - b) < 1e-6;
  for (let k = 0; k < 4; k++) {
    const u = [0, 1, 2, 3].map(j => D[(j + k) % 4]);
    if (eq(u[0][1], u[1][1]) && eq(u[1][0], u[2][0]) && eq(u[2][1], u[3][1]) && eq(u[3][0], u[0][0]))
      return [[u[0][0], u[0][1], u[2][0], u[2][1]].map(r4), k * 90];
  }
  throw new Error('no uv solution for ' + face);
}
const AX = {x: 0, y: 1, z: 2};
export function paintedBox(from, to, spec, rotation) {
  const faces = {};
  for (const [group, normal] of [['front', 'z'], ['side', 'x'], ['cap', 'y']]) {
    for (const face of FACES[normal]) {
      // Per-face overrides (spec.up, spec.east, ...) win over the group spec.
      const s = spec[face] || spec[group] || {sprite: spec.front.sprite, uv: [0, 0, 1, 1]};
      let fn;
      if (s.uv) {
        // Fixed sub-rectangle: pick the two in-plane axes in x, y, z order.
        const plane = [0, 1, 2].filter(i => i !== AX[normal]);
        fn = p => [16 * (s.uv[0] + (s.uv[2] - s.uv[0]) * (p[plane[0]] - from[plane[0]]) / (to[plane[0]] - from[plane[0]] || 1)),
          16 * (s.uv[1] + (s.uv[3] - s.uv[1]) * (1 - (p[plane[1]] - from[plane[1]]) / (to[plane[1]] - from[plane[1]] || 1)))];
      } else {
        const [ua, u0, u1] = s.u, [va, v0, v1] = s.v;
        fn = p => [16 * (p[AX[ua]] - u0) / (u1 - u0), 16 * (p[AX[va]] - v0) / (v1 - v0)];
      }
      const lo = from.map(r4), hi = to.map(r4);
      const [uv, rot] = solveUV(face, lo, hi, fn);
      faces[face] = {texture: '#' + s.sprite, uv: uv.map(v => r4(Math.min(16, Math.max(0, v)))), ...(rot ? {rotation: rot} : {})};
    }
  }
  return {from: from.map(r4), to: to.map(r4), faces, ...(rotation ? {rotation} : {})};
}
// Zero-thickness rectangle in the XY plane at z (both faces) showing the sub-rectangle uv
// (fractions, u left -> right along +X, v top -> bottom along -Y) of an alpha-cut sprite:
// the painted silhouette, not the element, defines the outline.
export function card([x0, y0], [x1, y1], z, sprite, uv = [0, 0, 1, 1], rotation) {
  const lo = [x0, y0, z], hi = [x1, y1, z];
  const fn = p => [16 * (uv[0] + (uv[2] - uv[0]) * (p[0] - x0) / (x1 - x0)),
    16 * (uv[1] + (uv[3] - uv[1]) * (1 - (p[1] - y0) / (y1 - y0)))];
  const faces = {};
  for (const face of ['north', 'south']) {
    const [fuv, rot] = solveUV(face, lo.map(r4), hi.map(r4), fn);
    faces[face] = {texture: '#' + sprite, uv: fuv.map(v => r4(Math.min(16, Math.max(0, v)))), ...(rot ? {rotation: rot} : {})};
  }
  return {from: lo.map(r4), to: hi.map(r4), faces, ...(rotation ? {rotation} : {})};
}
// The same card in the ZY plane at x (east/west faces): u along +Z, v top -> bottom along -Y.
export function cardX([z0, y0], [z1, y1], x, sprite, uv = [0, 0, 1, 1]) {
  const lo = [x, y0, z0], hi = [x, y1, z1];
  const fn = p => [16 * (uv[0] + (uv[2] - uv[0]) * (p[2] - z0) / (z1 - z0)),
    16 * (uv[1] + (uv[3] - uv[1]) * (1 - (p[1] - y0) / (y1 - y0)))];
  const faces = {};
  for (const face of ['east', 'west']) {
    const [fuv, rot] = solveUV(face, lo.map(r4), hi.map(r4), fn);
    faces[face] = {texture: '#' + sprite, uv: fuv.map(v => r4(Math.min(16, Math.max(0, v)))), ...(rot ? {rotation: rot} : {})};
  }
  return {from: lo.map(r4), to: hi.map(r4), faces};
}
// Zero-thickness plate in the XY plane at z (both faces), e.g. an alpha-cut emblem.
export function plate(cx, cy, size, z, sprite, rotation) {
  const h = size / 2, lo = [cx - h, cy - h, z], hi = [cx + h, cy + h, z];
  const fn = p => [16 * (p[0] - lo[0]) / size, 16 * (1 - (p[1] - lo[1]) / size)];
  const faces = {};
  for (const face of ['north', 'south']) {
    const [uv, rot] = solveUV(face, lo, hi, fn);
    faces[face] = {texture: '#' + sprite, uv, ...(rot ? {rotation: rot} : {})};
  }
  return {from: lo.map(r4), to: hi.map(r4), faces, ...(rotation ? {rotation} : {})};
}
