// HEAD region of the 야타용왕 (Azhdaha) rig (model.md §0, §3.1, §3.2; R2 rebuild against v2 f0750, v2 f0870, v4 f2160,
// v3 f2280, v1 f2370, v1 f2352, v2 f0546, v2 f0840):
//   head    the dark faceted rock mask as a forward V wedge (two half plates meeting in a midline ridge), a dark brow
//           ledge over each slit eye, the umber brow wings and the grey-brown keel blade rising between them, the
//           crown (a tall gold-rimmed central blade, a fanned pair, a second rank turned out 45 deg and a plate leaning
//           far back, plus side-facing crest fins), the cheek guards, the meander ear plates (回) on their mounts, the
//           rounded skull with the palate underneath, the upper teeth;
//   jaw     the cream V chin shield (its serrated top edge is the closed mouth line; a broad rounded V), the lower jaw
//           as a V wedge behind it (two cream cheek plates leaning in toward the chin over a tilted underside plate),
//           the mouth floor, lower teeth, two fangs, the tongue;
//   eyes    the red slits (their own bright part);
//   horn_*  one composite horn per side: the broad gold sleeve band bent into a C that opens forward (raised outer
//           rim wrapped round its rounded lower end, orange-brown meander face), a gold dome stud on the band's outer
//           face beside the mouth (the knob), the long dark horn (painted cards over a tapering core) growing out of
//           the sleeve mouth and curling forward;
//   beard*  two layered cream stone bibs hanging under the jaw (a front facet and two side facets turned 45 deg back,
//           serrated lower edges).
// Region interface: see azhdaha_body.mjs. Frames (azhdaha_pose.mjs): head / eyes = the atlas J.head, jaw = the hinge
// J.jaw, horn_* = HORN.at in the head frame turned by HORN.e (the C lies in the horn frame's YZ plane), beard1 /
// beard2 = J.beard1 / J.beard2. Every shape below is given in the AUTHORING frame: the rig's rest frame with the head
// joints at their R1 places (A0 below: atlas 0,2.05,-3.3); each part is authored relative to its A0 joint, so the model
// rides with its joint (R2 moved the atlas, jaw and beard joints 0.4 b forward in azhdaha_pose.mjs J).
import {loft, slab, rockBox, toUnits, mirrorX, stroke, sdPoly, registerTile, hash} from './azhdaha_shape.mjs';
import {PART_SCALE} from './azhdaha_pose.mjs';
import {PAL, C, clamp, smooth, mix, lift, sink, N, spriteSize, onRect, TRANSPARENT, creamPx, goldPx, cells} from './azhdaha_materials.mjs';
import {cardZ} from './mboss_model_lib.mjs';

export const REGION = 'head';
export const PARTS = [
  ['head', 'head', 13], ['jaw', 'jaw', 13], ['eyes', 'eyes', 15], ['horn_l', 'horn_l', 13], ['horn_r', 'horn_r', 13],
  ['beard1', 'beard1', 13], ['beard2', 'beard2', 13],
];
registerTile('mask', 64, 64, 48);
registerTile('teeth', 16, 16, 48);
registerTile('tongue', 32, 32, 48);
registerTile('knob', 16, 16, 48);      // the dome stud: one even polished gold (its tiers read by their shading alone)
const D2R = Math.PI / 180, sinD = th => Math.sin(th * D2R), tan22 = Math.tan(22.5 * D2R);
const A0 = {head: [0, 2.05, -3.3], jaw: [0, 1.3, -3.6], beard1: [0, 1.05, -3.5], beard2: [0, .72, -3.55]};
const JH = A0.head, JJ = A0.jaw;
// world rest point -> joint frame; (u, world y) polygon -> (u, frame y)
const fr = (f, [x, y, z]) => [x - f[0], y - f[1], z - f[2]];
const inF = (f, P) => P.map(([u, y]) => [u, y - f[1]]);
const rectOf = (P, pad = .03) => ({u0: Math.min(...P.map(p => p[0])) - pad, u1: Math.max(...P.map(p => p[0])) + pad,
  v0: Math.min(...P.map(p => p[1])) - pad, v1: Math.max(...P.map(p => p[1])) + pad});
// head frame stations from WORLD rows [z, half width, top y, bottom y, box]
const st = (o, rows) => rows.map(([z, w, top, bot, box = .3]) => ({a: z - o[2], r: [w, (top - bot) / 2, w, (top - bot) / 2], c: [0, (top + bot) / 2 - o[1]], box}));
// One half (the boss's left) of a wedge plate: polygon P (u = distance from the midline along the plate, frame y) in
// the plane z = zw (WORLD) turned about Y round the midline by rotY (-22.5: the outer edge goes back).
function half(f, P, zw, rotY, o) {
  const at = zw - f[2];
  return slab({plane: 'z', at, rect: o.rect || rectOf(P), sd: o.sd || sdPoly(P), half: o.h, sprite: o.sprite, edge: o.edge, cell: o.cell || .07,
    inset: o.inset ?? .6, core: o.core ?? true, rot: rotY ? ['y', rotY, [o.px || 0, 0, at]] : null});
}
// world point on a half plate turned by -22.5 round the midline at zw: (u, y) -> [x, y, z]
const onWedge = (u, y, zw) => [u * Math.cos(22.5 * D2R), y, zw + u * Math.sin(22.5 * D2R)];

// ---- face (head part) ---------------------------------------------------------------------------------------------------
// Planes (world z of the midline): the beak (jaw) stands in front of the mask, the keel in front of everything.
const FZ = -4.42;             // the dark mask half plates
const LEDGE_Z = FZ - .1;      // the dark brow ledges over the eyes
const WING_Z = FZ - .05;      // the grey-brown brow wings
const KEEL_Z = FZ - .22;      // the keel blade (mid-plane at its foot), tilted back 22.5 about the foot
const BEAK_Z = -4.62;         // the cream chin shield (jaw)
const TEETH_Z = -4.47;        // upper and lower teeth rows, just behind the shield (hidden when the mouth is closed)
// mouth line (the mask's lower edge): y(u) along the half plate, a shallow V
const mouthY = u => 1.1 + .2 * clamp(u / .68);
// eye slit on the mask half plate: centre, length, height, slant (inner end lower)
export const EYE = {u: .46, y: 1.5, len: .44, h: .14, slope: .48};
const eyeY = u => EYE.y + (u - EYE.u) * EYE.slope;
const MASK_W = [[0, 1.8], [.24, 2.02], [.46, 2.12], [.76, 1.97], [.86, 1.64], [.82, 1.42], [.68, mouthY(.68)], [.36, mouthY(.36)], [0, mouthY(0)]];
const MASK_P = inF(JH, MASK_W), maskSd = sdPoly(MASK_P);
const LEDGE_W = [[.05, eyeY(.05) + .06], [.3, eyeY(.3) + .085], [.62, eyeY(.62) + .09], [.8, eyeY(.8) + .1], [.9, 1.86], [.74, 1.88], [.4, 1.76], [.05, 1.66]];
const LEDGE_P = inF(JH, LEDGE_W), ledgeSd = sdPoly(LEDGE_P);
const WING_W = [[.14, 1.73], [.55, 1.9], [.88, 2.25], [1.04, 2.8], [.74, 2.52], [.42, 2.24], [.12, 2.02]];
const WING_P = inF(JH, WING_W), wingSd = sdPoly(WING_P);
// keel: a long diamond from its foot between the eyes (y 1.58) to its tip (1.44 above, before the 22.5 tilt)
const KEEL_FOOT = 1.58, KEEL_L = 1.46, KEEL_HW = .2;
const keelSdW = (x, y) => { const t = (y - KEEL_FOOT) / KEEL_L, w = t < .42 ? KEEL_HW * (t / .42) ** .8 : KEEL_HW * ((1 - t) / .58) ** .9; return t < 0 || t > 1 ? 1 : Math.abs(x) - w; };
const keelSd = (u, v) => keelSdW(u, v + JH[1]);
const KEEL = {u0: -.2, u1: .2, v0: KEEL_FOOT - JH[1] - .02, v1: KEEL_FOOT + KEEL_L - JH[1] + .02};
// cheek guard: a dark plate from the face edge out to the horn sleeve, turned 22.5 (its own u from x .74 / z -4.06)
const CHEEK_O = [.74, -4.03];      // (its front card .03 behind the brow ledge's and the ear plate's back cards)
const CHEEK_W = [[0, 1.28], [.3, 1.08], [.78, 1.12], [.98, 1.5], [.86, 1.9], [.4, 2.02], [0, 1.98]];
const CHEEK_P = inF(JH, CHEEK_W).map(([u, v]) => [u + CHEEK_O[0], v]), cheekSd = sdPoly(CHEEK_P);
// ear plate (回) at the temple, facing forward (turned 22.5 out), on a dark mount
const EAR_C = [1.16, 2.3, -3.93], EAR_HW = .28, EAR_HH = .26;
const EAR = {u0: EAR_C[0] - EAR_HW - .02, u1: EAR_C[0] + EAR_HW + .02, v0: EAR_C[1] - JH[1] - EAR_HH - .02, v1: EAR_C[1] - JH[1] + EAR_HH + .02};
const earSd = (u, v) => Math.max(Math.abs(u - EAR_C[0]) - EAR_HW, Math.abs(v - (EAR_C[1] - JH[1])) - EAR_HH);

function skull() {
  const els = [];
  // skull: behind the face plates, a rounded mass widest at the temples (reaching in toward the sleeve backs), the
  // palate underneath (only the bottom facets red: seen when the jaw opens, never from the side)
  els.push(...loft('z', st(JH, [[-4.06, .7, 2.2, 1.12, .25], [-3.75, 1.15, 2.4, 1.08, .2], [-3.4, 1.38, 2.47, 1.1, .15], [-3.0, 1.18, 2.42, 1.2, .15], [-2.62, .8, 2.26, 1.38, .15]]),
    {tex: (k, th, i) => (sinD(th) < -.92 && i < 2 ? 'mouth' : 'mask'), ledgeTex: 'mask', caps: '-+', seed: 401}));
  // the ear mounts: dark blocks behind the 回 plates, jutting out like ears
  const temple = [rockBox(fr(JH, [EAR_C[0] - .22, EAR_C[1] - .2, EAR_C[2] + .06]), fr(JH, [EAR_C[0] + .22, EAR_C[1] + .2, -3.55]), 'mask', {seed: 19})];
  // the left half of the face: mask plate, brow ledge, brow wing, cheek guard, ear plate; mirrored for the right
  const L = [];
  L.push(...half(JH, MASK_P, FZ, -22.5, {h: .07, sprite: 'face', edge: 'mask', rect: rectOf(MASK_P), sd: maskSd}));
  L.push(...half(JH, LEDGE_P, LEDGE_Z, -22.5, {h: .055, sprite: 'ledge', edge: 'mask', cell: .05}));
  L.push(...half(JH, WING_P, WING_Z, -22.5, {h: .05, sprite: 'wing', edge: 'mask', cell: .06}));
  L.push(...slab({plane: 'z', at: CHEEK_O[1] - JH[2], rect: rectOf(CHEEK_P), sd: cheekSd, half: .06, sprite: 'cheek', edge: 'mask', cell: .08,
    rot: ['y', -22.5, [CHEEK_O[0], 0, CHEEK_O[1] - JH[2]]]}));
  L.push(...slab({plane: 'z', at: EAR_C[2] - JH[2], rect: EAR, sd: earSd, half: .05, sprite: 'ear', edge: 'gold_dk', cell: .07,
    rot: ['y', -22.5, [EAR_C[0], 0, EAR_C[2] - JH[2]]]}));
  // dark crown spikes behind the wings, fanning up and out (front view), and the crest plates leaning back
  // upper teeth hanging from the mouth line (hidden behind the chin shield when the mouth is closed)
  for (const [u, w, hgt] of [[.07, .14, .2], [.23, .14, .19], [.39, .13, .17], [.55, .12, .15]]) {
    const [x, , z] = onWedge(u, 0, TEETH_Z), y = mouthY(u);
    L.push(rockBox(fr(JH, [x - w / 2, y - hgt, z - .05]), fr(JH, [x + w / 2, y + .03, z + .05]), {all: 'teeth', up: 'mouth'}, {seed: u * 40, rot: ['y', -22.5, fr(JH, [x, y, z])]}));
  }
  // two more along each side of the upper jaw, between the lower side teeth (the open mouth reads as a row from the side)
  for (const [z, hgt] of [[-4.14, .15], [-3.94, .13]]) L.push(rockBox(fr(JH, [.52, 1.3 - hgt, z - .05]), fr(JH, [.64, 1.33, z + .05]), {all: 'teeth', up: 'mouth'}, {seed: z * 7}));
  els.push(...L, ...mirrorX(L), ...temple, ...mirrorX(temple));
  // keel blade: front-facing diamond, tilted back about its foot, thick (the raised blade)
  const keelAt = KEEL_Z - JH[2];
  els.push(...slab({plane: 'z', at: keelAt, rect: KEEL, sd: keelSd, half: .1, sprite: 'keel', edge: 'mask', cell: .06,
    rot: ['x', 22.5, [0, KEEL_FOOT - JH[1], keelAt]]}));
  // crest plates on the crown: a central fin behind the keel and a pair beside it, leaning back over the occiput
  for (const [x, y, z, len, k, rx] of [[0, 2.25, -3.7, 1.0, 1, 22.5], [.44, 2.3, -3.45, .9, 0, 45]])
    for (const s of x ? [1, -1] : [1]) els.push(...mspike('x', [s * x, y, z], len, k, rx, s));
  // the dark crown behind the keel: a tall central blade leaning back and a pair fanning out, gold-rimmed (v2 f0750)
  els.push(...crest(0, [0, 2.25, -4.0], 1.5, .74, 0, 22.5));
  const side = crest(1, [.4, 2.2, -3.92], 1.3, .6, -22.5, 0);
  // a second rank over the skull: two blades a side turned out 45 deg (they read from the side and the 3/4 too) and a
  // central plate leaning far back, so the crown is a layered fan from every side rather than a row of front cards
  side.push(...crest(1, [.66, 2.25, -3.62], 1.05, .52, 0, 0, -45), ...crest(1, [1.0, 2.12, -3.3], .85, .46, 0, 0, -45));
  els.push(...side, ...mirrorX(side), ...crest(0, [0, 2.32, -3.42], 1.05, .56, 0, 45));
  return els;
}
// crest blade: sheet cell k (0 symmetric, 1 leaning out, gold rim on its outer edge), root [x, y, z] (authoring), front
// facing; rz fans it out (about z), rx leans it back (about x)
const CREST_SD = [
  (x, y) => Math.abs(x) - .5 * (1 - y) ** .9 * (y < .12 ? .7 + 2.5 * y : 1),
  (x, y) => { const c = .12 * y * y; return Math.abs(x - c) - .5 * (1 - y) ** .85 * (y < .12 ? .7 + 2.5 * y : 1); },
];
function crest(k, w, L, W, rz, rx, ry = 0) {
  const [x, y, z] = fr(JH, w);
  const rect = {u0: x - W / 2, u1: x + W / 2, v0: y, v1: y + L};
  const sd = (u, v) => CREST_SD[k]((u - x) / W, (v - y) / L) * W;
  const els = slab({plane: 'z', at: z, rect, sd, half: .055, sprite: 'crest', edge: 'mask', cell: .08,
    rot: rz ? ['z', rz, [x, y, z]] : rx ? ['x', rx, [x, y, z]] : ry ? ['y', ry, [x, y, z]] : null});
  for (const e of els) for (const f of Object.values(e.faces)) if (f.texture === '#crest') {
    const [a, b, c2, d] = f.uv;
    f.uv = [k * 8 + a / 2, b, k * 8 + c2 / 2, d].map(v => +v.toFixed(4));
  }
  return els;
}
// dark spikes / crest plates (2 shapes in a 2-cell sheet): plane 'z' faces front (rot about z fans it out), 'x' faces
// the side (rot about x leans it back). [x, y, z] = the root (WORLD), len = length.
const MSP = [{c: [.45, .5], t: [.55, 1], w: .42}, {c: [.4, .55], t: [.8, .95], w: .44}];
const MS = MSP.map(b => { const pts = Array.from({length: 11}, (_, i) => { const t = i / 10; return [0, 1].map(k => (1 - t) ** 2 * [.5, 0][k] + 2 * (1 - t) * t * b.c[k] + t * t * b.t[k]); }).map(([x, y]) => [x / 2, y]);
  return {...b, S: stroke(pts, t => b.w / 2 * (1 - t) ** .8)}; });
function mspike(plane, w, L, k, rotDeg, side) {
  const [x, y, z] = fr(JH, w);
  const W = L * .5, c = plane === 'x' ? z : x, flip = plane === 'z' && side < 0;
  const rect = {u0: c - .5 * W, u1: c + .5 * W, v0: y, v1: y + L};
  const sd = (u, v) => { let nu = (u - rect.u0) / W; if (flip) nu = 1 - nu; return MS[k].S.sd(nu / 2, (v - y) / L) * L; };
  const els = slab({plane, at: plane === 'x' ? x : z, rect, sd, half: .06, sprite: 'mspikes', edge: 'mask', cell: .08, core: L > .5,
    rot: rotDeg ? [plane === 'x' ? 'x' : 'z', rotDeg, [x, y, z]] : null});
  for (const e of els) for (const f of Object.values(e.faces)) if (f.texture === '#mspikes') {
    let [a, b, c2, d] = f.uv; if (flip) [a, c2] = [16 - a, 16 - c2];
    f.uv = [k * 8 + a / 2, b, k * 8 + c2 / 2, d].map(v => +v.toFixed(4));
  }
  return els;
}

// ---- jaw: the cream V chin shield, the lower jaw, teeth, fangs, tongue ------------------------------------------------------
// shield half plate: serrated top edge (the closed mouth line, overlapping the mask's lower edge), a broad rounded V to
// the chin (v2 f0870, v2 f0750: a wide U with a blunt point)
const beakTopW = u => mouthY(u) + .04 + .1 * Math.max(0, 1 - Math.abs(((u * 3.9 + .5) % 1 + 1) % 1 - .5) * 3.2);
// (R3b, r3_critique 2.3: a broad V narrowing evenly from 0.55 b half-width at the mouth line to 0.1 b at the chin)
const BEAK_W = [[0, mouthY(0) + .2], [.62, mouthY(.62) + .2], [.62, 1.16], [.38, .72], [.11, .27], [0, .25]];
const BEAK_P = inF(JJ, BEAK_W), beakPoly = sdPoly(BEAK_P);
const beakSd = (u, v) => Math.max(beakPoly(u, v), v + JJ[1] - beakTopW(u));
// The lower jaw behind the shield is a V wedge too: two cream cheek plates (x = +-JSIDE_X at the lip line, leaning
// in 22.5 deg toward the chin so they stay inside the shield's outline from the front) over a tilted underside plate
// rising 22.5 deg from the chin to the throat. (z, y) of the cheek outline are AUTHORING coordinates on the plate
// before the lean (the lean shortens heights by cos 22.5 about the lip line JSIDE_TOP).
const JSIDE_X = .56, JSIDE_TOP = 1.2, LEAN = Math.cos(22.5 * D2R);   // (R3b: narrower, inside the V beak)
const underY = z => .3 + (z + 4.5) * Math.tan(22.5 * D2R);                      // the underside line (world y at z)
const unlean = y => JSIDE_TOP + (y - JSIDE_TOP) / LEAN;                          // world y -> plate y before the lean
const JSIDE_W = [[-4.36, 1.17], [-3.75, 1.2], [-3.28, 1.18], [-3.2, 1.02], [-3.24, unlean(underY(-3.24) - .04)],
  [-3.8, unlean(underY(-3.8) - .04)], [-4.36, unlean(underY(-4.36) - .04)]];
const JSIDE_P = JSIDE_W.map(([z, y]) => [z - JJ[2], y - JJ[1]]), jsideSd = sdPoly(JSIDE_P);
// underside: a 'y' plate (x, z) from the chin back, before its 22.5 deg tilt about the chin line
const UNDER_L = 1.22, UNDER_P = [[-.3, -4.5], [.3, -4.5], [.5, -4.5 + UNDER_L], [-.5, -4.5 + UNDER_L]], underSd = sdPoly(UNDER_P.map(([x, z]) => [x, z - JJ[2]]));
function jaw() {
  const els = [];
  const L = [];
  L.push(...half(JJ, BEAK_P, BEAK_Z, -22.5, {h: .07, sprite: 'beak', edge: 'cream', sd: beakSd, rect: rectOf(BEAK_P), cell: .06}));
  // the cheek plate (left; mirrored)
  L.push(...slab({plane: 'x', at: JSIDE_X, rect: rectOf(JSIDE_P), sd: jsideSd, half: .05, sprite: 'jside', edge: 'cream', cell: .07,
    rot: ['z', -22.5, [JSIDE_X, JSIDE_TOP - JJ[1], 0]]}));
  // lower teeth behind the shield's top edge, a big fang at each front corner, two more along the cheek's lip line
  for (const [u, w, hgt] of [[.1, .13, .17], [.26, .13, .16], [.58, .12, .15]]) {
    const [x, , z] = onWedge(u, 0, TEETH_Z + .03), y = mouthY(u) + .05;
    L.push(rockBox(fr(JJ, [x - w / 2, y - hgt, z - .05]), fr(JJ, [x + w / 2, y, z + .05]), {all: 'teeth', down: 'mouth'}, {seed: u * 30, rot: ['y', -22.5, fr(JJ, [x, y, z])]}));
  }
  for (const [z, hgt] of [[-4.04, .13], [-3.84, .11]]) L.push(rockBox(fr(JJ, [JSIDE_X - .2, 1.14, z - .06]), fr(JJ, [JSIDE_X - .07, 1.14 + hgt, z + .06]), {all: 'teeth', down: 'mouth'}, {seed: z * 10}));
  {
    const [x, , z] = onWedge(.43, 0, TEETH_Z + .045), y = mouthY(.43);
    L.push(rockBox(fr(JJ, [x - .075, y - .3, z - .06]), fr(JJ, [x + .075, y - .02, z + .06]), 'teeth', {seed: 5, rot: ['y', -22.5, fr(JJ, [x, y, z])]}),
      rockBox(fr(JJ, [x - .045, y - .02, z - .035]), fr(JJ, [x + .045, y + .06, z + .035]), 'teeth', {seed: 6, rot: ['y', -22.5, fr(JJ, [x, y, z])]}));
  }
  els.push(...L, ...mirrorX(L));
  // the underside plate, tilted up toward the throat about the chin line
  const ch = fr(JJ, [0, .3, -4.5]);
  els.push(...slab({plane: 'y', at: ch[1], rect: rectOf(UNDER_P.map(([x, z]) => [x, z - JJ[2]]), .02), sd: underSd, half: .05, sprite: 'junder', edge: 'cream', cell: .08,
    rot: ['x', -22.5, ch]}));
  // the floor of the mouth (red on top, seen when the jaw opens) and the tongue
  els.push(rockBox(fr(JJ, [-.55, .78, -4.37]), fr(JJ, [.55, 1.06, -3.3]), {all: 'cream', up: 'mouth'}, {seed: 8}));
  els.push(rockBox(fr(JJ, [-.34, 1.04, -4.3]), fr(JJ, [.34, 1.13, -3.75]), {all: 'tongue', down: 'mouth'}, {seed: 9}));
  return els;
}

// ---- eyes (bright part, brightness 15): slanted red slits on the mask plates, under the brow ledges ---------------------------
const EYE_R = {u0: EYE.u - .25, u1: EYE.u + .25, v0: EYE.y - .17 - JH[1], v1: EYE.y + .17 - JH[1]};
function eyes() {
  const at = FZ - JH[2] - .07 - .012 - .012;
  const e = [cardZ('eye', at, {X0: EYE_R.u0, X1: EYE_R.u1, Y0: EYE_R.v0, Y1: EYE_R.v1}, {rot: ['y', -22.5, [0, 0, at]]})];
  return [...e, ...mirrorX(e)];
}

// ---- horns ---------------------------------------------------------------------------------------------------------------------
// Authored in the horn frame (HORN: origin HORN.at in the head frame, yaw HORN.e: its -Z points forward-inward, its +X
// outward-forward). The C lies in the plane x = 0: (u, v) = (local z, local y); -u is forward(-inward).
// Sleeve centre line from the knob (front, low, beside the mouth) back and up round the C to the sleeve mouth.
// Catmull-Rom through control points -> dense polyline
function spline(P, n = 8) {
  const out = [];
  for (let i = 0; i < P.length - 1; i++) {
    const p0 = P[Math.max(0, i - 1)], p1 = P[i], p2 = P[i + 1], p3 = P[Math.min(P.length - 1, i + 2)];
    for (let j = 0; j < n; j++) {
      const t = j / n, t2 = t * t, t3 = t2 * t;
      out.push([0, 1].map(k => .5 * (2 * p1[k] + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2 + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3)));
    }
  }
  out.push(P[P.length - 1]);
  return out;
}
// the sleeve band: from its rounded lower end beside the mouth (the dome knob sits on its outer face just behind the end)
// back and up round the C to the sleeve mouth at the top; broadest round the knob (model.md 0.75 b), 0.6 b at the mouth
// (R3b, r3_critique 2.2: the gold ends at brow height, 0.3 b lower than R2; the band 0.44 b thick)
const SLEEVE_C = spline([[-1.24, -.93], [-1.05, -.81], [-.86, -.68], [-.57, -.45], [-.29, -.15], [-.08, .22], [.02, .62], [.0, .95], [-.04, 1.12]], 8);
const SLEEVE_W = t => (t < .3 ? .74 + .33 * t : .84 - .3 * (t - .3)), SLEEVE_H = .22;
// the dark horn (R3b, r3_critique 2.2): out of the sleeve mouth it rises up and back 2.8 b along the curve (the tallest
// element of the head, top 5.6-5.8 b), 0.5 b at the mouth; only its last 0.3 b curls forward. In this plane +u is back
// and OUTWARD (the C plane is yawed 53 deg), so the tips flare a little outward in the front view instead of leaning in.
const DHORN_C = spline([[-.05, .98], [-.01, 1.45], [.1, 1.95], [.22, 2.45], [.32, 2.92], [.38, 3.32], [.36, 3.6], [.27, 3.76]], 8);
const DHORN_W = t => .5 * (1 - t) ** .9 + .035;
const SLV = stroke(SLEEVE_C, t => SLEEVE_W(t) / 2), DHS = stroke(DHORN_C, t => DHORN_W(t) / 2);
// point at arc length l (blocks) along a polyline, and its unit direction
function along(pts, l) {
  for (let i = 1; i < pts.length; i++) {
    const a = pts[i - 1], b = pts[i], d = Math.hypot(b[0] - a[0], b[1] - a[1]);
    if (l <= d || i === pts.length - 1) { const f = Math.min(1, l / d); return {p: [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f], d: [(b[0] - a[0]) / d, (b[1] - a[1]) / d]}; }
    l -= d;
  }
}
// the knob (R3b, r3_critique 2.2): a gold BALL at the band's lower end, about as wide as the band, pointing forward and
// down beside the beak (v3 f2280): its centre just past the end along the band's axis
const KNOB_DIR = (() => { const [a, b] = SLEEVE_C, l = Math.hypot(a[0] - b[0], a[1] - b[1]); return [(a[0] - b[0]) / l, (a[1] - b[1]) / l]; })();
const KNOB = [SLEEVE_C[0][0] + .08 * KNOB_DIR[0], SLEEVE_C[0][1] + .08 * KNOB_DIR[1]], KNOB_R = .3;
const DH_RECT = rectOf(DHORN_C, .24);   // (the horn part reaches 3 b up: the card stays inside)
// dark horn half thickness at height v (the horn rises monotonically): the arc fraction of the nearest centre point
const dhT = v => { let best = 0, bd = 9; DHORN_C.forEach((p, i) => { const d = Math.abs(p[1] - v); if (d < bd) { bd = d; best = i; } }); return DHS.near(DHORN_C[best][0], DHORN_C[best][1]).t; };
const SLEEVE_RECT = (() => { const r = rectOf(SLEEVE_C, .4); return r; })();
// Runs of a polyline whose tangent stays within +-11.25 deg of one 22.5-degree direction -> boxes along their chords,
// rotated about X (in the plane x = x0). w(t) = width in the plane, h(t) = half thickness along x.
function chain(pts, {w, h, tex, x0 = 0, ext = .03, seed = 0, shrink = 0, maxLen = 9}) {
  const L = [0];
  for (let i = 1; i < pts.length; i++) L.push(L[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  const T = L.map(l => l / L[L.length - 1]);
  const ang = i => { const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)]; return Math.atan2(b[1] - a[1], b[0] - a[0]) / D2R; };
  let prev = null, unw = 0;
  const q = [];
  for (let i = 0; i < pts.length; i++) {
    let a = ang(i);
    if (prev !== null) { while (a - prev > 180) a -= 360; while (a - prev < -180) a += 360; }
    prev = a; q.push(Math.round(a / 22.5));
  }
  const runs = [];
  let s = 0;
  for (let i = 1; i <= pts.length; i++) if (i === pts.length || q[i] !== q[s] || L[i] - L[s] > maxLen) { runs.push([s, Math.min(i, pts.length - 1), q[s]]); s = i; }
  const els = [];
  runs.forEach(([i0, i1, qi], r) => {
    if (i1 <= i0) return;
    const P0 = pts[i0], P1 = pts[i1], M = [(P0[0] + P1[0]) / 2, (P0[1] + P1[1]) / 2], tm = (T[i0] + T[i1]) / 2;
    const len = Math.hypot(P1[0] - P0[0], P1[1] - P0[1]) + 2 * ext, wd = w(tm) - shrink, hh = h(tm, r);
    let phi = qi * 22.5;
    while (phi > 90) phi -= 180;
    while (phi <= -90) phi += 180;
    let lo, hi, g;
    if (phi >= -45 && phi <= 45) { g = -phi; lo = [x0 - hh, M[1] - wd / 2, M[0] - len / 2]; hi = [x0 + hh, M[1] + wd / 2, M[0] + len / 2]; }
    else { if (phi < 0) phi += 180; g = 90 - phi; lo = [x0 - hh, M[1] - len / 2, M[0] - wd / 2]; hi = [x0 + hh, M[1] + len / 2, M[0] + wd / 2]; }
    els.push(rockBox(lo, hi, tex, {seed: seed + r * 7.7, rot: g ? ['x', g, [x0, M[1], M[0]]] : undefined}));
  });
  return els;
}
// offset polyline: each point moved by d(t) along the in-plane normal (+ = left of the direction = the C's inside)
function offset(pts, d) {
  const L = [0];
  for (let i = 1; i < pts.length; i++) L.push(L[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  return pts.map((p, i) => {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1;
    const k = d(L[i] / L[L.length - 1]);
    return [p[0] - dy / l * k, p[1] + dx / l * k];
  });
}
// Regular n-gon prism (n 8 or 16) along `axis` through c: inradius r, axial range a0..a1 (absolute). A union of n / 2
// thin boxes at 360 / n degree steps (each a single-axis rotation within +-45 in 22.5 steps): every outer facet is the
// end of one box. phase 22.5 turns an octagon by half a facet. The far end steps by .003 per box (no coplanar caps).
function ngon(axis, c, r, a0, a1, tex, {n = 8, phase = 0, seed = 0} = {}) {
  const ai = {x: 0, y: 1, z: 2}[axis], [p, q] = [[1, 2], [0, 2], [0, 1]][ai], t = r * Math.tan(Math.PI / n);
  const set = n === 16 ? [['w', 0], ['w', 22.5], ['w', -22.5], ['w', 45], ['w', -45], ['t', 0], ['t', 22.5], ['t', -22.5]]
    : phase ? [['w', 22.5], ['w', -22.5], ['t', 22.5], ['t', -22.5]] : [['w', 0], ['w', 45], ['w', -45], ['t', 0]];
  return set.map(([k, g], i) => {
    const lo = c.slice(), hi = c.slice(), hp = k === 'w' ? r : t, hq = k === 'w' ? t : r;
    lo[p] -= hp; hi[p] += hp; lo[q] -= hq; hi[q] += hq;
    lo[ai] = Math.min(a0, a1); hi[ai] = Math.max(a0, a1);
    if (a1 > a0) hi[ai] -= i * .003; else lo[ai] += i * .003;
    return rockBox(lo, hi, tex, {seed: seed + i * 3.1, rot: g ? [axis, g, c] : undefined});
  });
}
function horn() {
  const els = [];
  // the sleeve band: painted cards (outline + meander face) over a chain of boxes following the C
  for (const sgn of [1, -1]) els.push(...slab({plane: 'x', at: 0, rect: SLEEVE_RECT, sd: (u, v) => SLV.sd(u, v), half: SLEEVE_H, sprite: sgn > 0 ? 'sleeve' : 'sleeve_in',
    edge: 'gold', core: false, cards: sgn > 0 ? '+' : '-'}));
  els.push(...chain(SLEEVE_C, {w: SLEEVE_W, h: () => SLEEVE_H, tex: 'gold_dk', shrink: .03, seed: 3}));
  // the rounded lower end of the band: an octagonal core under the cards
  const [e0, e1] = SLEEVE_C, W0 = SLEEVE_W(0) / 2;
  els.push(...ngon('x', [0, e0[1], e0[0]], W0 * .86, -SLEEVE_H + .01, SLEEVE_H - .01, 'gold_dk', {seed: 67}));
  // the raised outer rim along the convex (back / lower) edge, proud of both faces, and wrapped round the lower end;
  // alternate depths so overlaps never coincide
  const RIM = offset(SLEEVE_C, t => -(SLEEVE_W(t) / 2 - .055));
  els.push(...chain(RIM, {w: () => .13, h: (t, r) => SLEEVE_H + .045 + (r % 2) * .008, tex: 'gold', ext: .025, seed: 11}));
  {
    const l = Math.hypot(e1[0] - e0[0], e1[1] - e0[1]), d = [(e1[0] - e0[0]) / l, (e1[1] - e0[1]) / l], nl = [-d[1], d[0]], R = W0 - .055;
    const arc = Array.from({length: 13}, (_, i) => { const f = (-90 + i * 15) * D2R; return [0, 1].map(k => e0[k] + R * (-Math.cos(f) * d[k] + Math.sin(f) * nl[k])); });
    els.push(...chain(arc, {w: () => .13, h: (t, r) => SLEEVE_H + .038 + (r % 2) * .01, tex: 'gold', ext: .03, seed: 15}));
  }
  // the inner edge bevelled like the outer one: a rounded rim chain proud of both faces along the concave edge
  const LIP = offset(SLEEVE_C, t => SLEEVE_W(t) / 2 - .05);
  els.push(...chain(LIP.slice(5, -2), {w: () => .11, h: (t, r) => SLEEVE_H + .03 + (r % 2) * .007, tex: 'gold_dk', ext: .02, seed: 13}));
  // the sleeve mouth: a gold collar at the top end, the dark horn grows out of it
  const top = SLEEVE_C[SLEEVE_C.length - 1];
  els.push(rockBox([-SLEEVE_H - .07, top[1] - .21, top[0] - .31], [SLEEVE_H + .07, top[1] + .025, top[0] + .31], 'gold', {seed: 21, rot: ['x', -22.5, [0, top[1], top[0]]]}));
  // the knob: a ball from three crossed octagonal prisms (across the band, along it and upright), so its outline is round
  // from the front, the side and below; a smaller cap a little forward of it
  const kc = [0, KNOB[1], KNOB[0]], R = KNOB_R;
  els.push(...ngon('x', kc, R, -R * .82, R * .82, 'knob', {seed: 61}),
    ...ngon('z', kc, R * .97, kc[2] - R * .84, kc[2] + R * .8, 'knob', {phase: 22.5, seed: 63}),
    ...ngon('y', kc, R * .93, kc[1] - R * .86, kc[1] + R * .82, 'knob', {seed: 65}));
  // the dark horn: painted cards (the exact curled outline, shaded) on both faces over an octagonal tapering core
  const hv = tb => { const v = DH_RECT.v1 - Math.min(1, tb + 1 / 12) * (DH_RECT.v1 - DH_RECT.v0); return .42 * DHORN_W(dhT(v)) + .01; };
  // (clipped at the collar: the horn grows out of the sleeve mouth, its round foot stays inside)
  els.push(...slab({plane: 'x', at: 0, rect: DH_RECT, sd: (u, v) => DHS.sd(u, v), half: {along: 'v', bands: 6, h: hv}, sprite: 'dhorn', edge: 'horn', core: false,
    clip: {v0: SLEEVE_C[SLEEVE_C.length - 1][1] - .05}}));
  els.push(...chain(DHORN_C, {w: t => DHORN_W(t) * .9, h: t => DHORN_W(t) * .28, tex: 'horn', seed: 41, maxLen: .22}));
  els.push(...chain(DHORN_C, {w: t => DHORN_W(t) * .6, h: t => DHORN_W(t) * .4, tex: 'horn', ext: .025, seed: 43, maxLen: .22}));
  return els;
}

// ---- beard: two layered cream stone bibs hanging from under the jaw (model.md 3.2: 1.6 b wide, triangular, layered).
// Each bib: a front facet (|x| <= BIB_F) and two side facets turned 45 deg back, so it reads as a hanging plate from
// the front, the side and below; the lower edge is serrated and rises toward the sides. Outline in UNROLLED (u, world y)
// coordinates: u = distance from the midline along the bib surface.
const BIB_F = .36;
function bibPoly(top, bot, U, k = 7) {
  const P = [[0, top], [U, top], [U, top - (top - bot) * .22]];
  for (let i = k; i >= 0; i--) { const u = U * i / k; P.push([u, bot + (top - bot) * .62 * (u / U) ** 1.25 + (i % 2 ? .055 : 0)]); }
  return P;
}
const BEARDS = {
  beard1: {f: A0.beard1, zw: -3.8, P: bibPoly(.8, .34, .98)},
  beard2: {f: A0.beard2, zw: -3.55, P: bibPoly(.66, .2, .86)},
};
for (const b of Object.values(BEARDS)) { b.Pf = inF(b.f, b.P); b.sd = sdPoly(b.Pf); b.R = rectOf(b.Pf); }
function bib(name) {
  const {f, zw, sd, R} = BEARDS[name], at = zw - f[2];
  // (R3b, r3_critique 2.4: alpha-cut cards only, the serrated hem painted on them; the 0.07 b core cells stair-stepped the
  // outline. 0.04 b of thickness along the straight top edge only.)
  const front = slab({plane: 'z', at, rect: {u0: -BIB_F - .05, u1: BIB_F + .05, v0: R.v0, v1: R.v1}, sd: (u, v) => sd(Math.abs(u), v), half: .03,
    sprite: name + 'f', core: false});
  const side = slab({plane: 'z', at, rect: {u0: BIB_F, u1: R.u1, v0: R.v0, v1: R.v1}, sd, half: .03, sprite: name + 's', core: false,
    rot: ['y', -45, [BIB_F, 0, at]]});
  const top = BEARDS[name].Pf[0][1];
  const lip = [rockBox([-BIB_F, top - .05, at - .03], [BIB_F, top, at + .03], 'cream', {seed: 3})];
  const lipS = [rockBox([BIB_F, top - .05, at - .03], [R.u1 - .04, top, at + .03], 'cream', {seed: 5, rot: ['y', -45, [BIB_F, 0, at]]})];
  return [...front, ...side, ...mirrorX(side), ...lip, ...lipS, ...mirrorX(lipS)];
}

// ---- region exports ------------------------------------------------------------------------------------------------------------
const U = (part, els) => toUnits(els, PART_SCALE[part]);
export function models() {
  const h = horn();
  return {
    head: U('head', skull()), jaw: U('jaw', jaw()), eyes: U('eyes', eyes()),
    horn_l: U('horn_l', h), horn_r: U('horn_r', mirrorX(h)),
    beard1: U('beard1', bib('beard1')), beard2: U('beard2', bib('beard2')),
  };
}
export const LOOKS = {};
export const TINTED = {};
export const LOOK_BRIGHT = {};

// ---- sprites ----------------------------------------------------------------------------------------------------------------
// facet field: jittered cells (big facets), each a slightly different value, lit edges toward the upper left
function facets(u, v, scale, seed) {
  const c = cells(u * scale + 3, v * scale + 3, seed);
  return {id: c.id, edge: c.d2 - c.d1};
}
function maskTile(s, t) {
  // dark faceted rock: stretched angular facets (each a slightly different value), thin dark seams, faint grain
  const u = s * 64, v = t * 64;
  const c0 = cells(u / 26, v / 13, 41, 0, .95), c1 = cells(u / 9 + 5, v / 6, 43, 0, .9);
  let c = PAL.mask(.44 + .2 * (c0.id - .5) + .08 * (c1.id - .5) + .06 * (N.a(u * .2, v * .05) - .5));
  if (c0.d2 - c0.d1 < .045) c = PAL.mask(.82);
  else if (c0.d2 - c0.d1 < .09) c = mix(c, PAL.mask(.2), .35);
  if (Math.abs(N.d(u * .05, v * .025) - .5) < .01) c = sink(c, .4);
  return c;
}
// the dark mask half: spiky facets radiating from the eye (dark, sharp, lit on their upper-left edges), a dark socket,
// the midline ridge, a faint red glow spill under the slit
function facePaint(u, v) {
  const d = maskSd(u, v);
  if (d > 0) return null;
  const y = v + JH[1];
  const dx = u - EYE.u, dy = y - EYE.y, r = Math.hypot(dx, dy), th = Math.atan2(dy, dx);
  const K = 13, sec = (th / (2 * Math.PI) + 1) * K, k = Math.floor(sec), f = sec - k;
  const sh = hash(k % K, 3.1);
  // radial blades: each sector a spike, lit along one side
  let c = PAL.mask(.5 + .28 * (sh - .5) + .22 * clamp(r - .2));
  if (f < .22) c = mix(c, PAL.mask(.18), .55 * (1 - f / .22));                 // the lit flank of each blade
  if (f > .9) c = mix(c, PAL.mask(.95), .6);                                     // the shadowed seam
  const fc = facets(u, y, 6, 7);
  if (fc.edge < .06) c = mix(c, PAL.mask(.9), .4);
  // socket: dark round the slit, red spill below it
  const es = Math.hypot(dx / .26, (y - eyeY(u)) / .1);
  if (es < 1) c = mix(c, PAL.mask(1), .7 * (1 - es));
  if (es < 1.9) c = mix(c, PAL.eye(.82), .42 * (1 - es / 1.9) ** 1.5);             // the red glow spill round the slit
  if (u < .025) c = mix(c, PAL.mask(.12), .7);                                     // the midline ridge, lit
  if (d > -.022) c = sink(c, .4);
  return c;
}
function ledgePaint(u, v) {
  const d = ledgeSd(u, v);
  if (d > 0) return null;
  const y = v + JH[1], below = y - eyeY(u);
  let c = PAL.mask(.62 + .2 * (hash(Math.floor(u * 9), 2) - .5));
  if (below < .14) c = mix(c, PAL.mask(.98), .5);                                // the overhang's shadowed lip
  if (Math.abs(((u * 9) % 1 + 1) % 1 - .5) < .06) c = mix(c, PAL.mask(.95), .5);  // spiky facet seams
  if (d > -.02 && y > eyeY(u) + .1) c = mix(c, PAL.mask(.15), .6);               // lit upper rim
  return c;
}
// grey-brown keel / wing stone: model.md keel #8A6650 / #6A4A3A with a cool grey lift
const KEELC = t => mix(PAL.mask(clamp(t)), C('#9A8A7A'), .5);
function wingPaint(u, v) {
  const d = wingSd(u, v);
  if (d > 0) return null;
  const y = v + JH[1];
  // along the blade: from the root (u .06, y 1.8) to the tip (1.02, 2.72); the upper flank lit, a groove down the middle
  const ax = [.96, .92], ox = u - .06, oy = y - 1.8, along = ox * ax[0] / 1.33 + oy * ax[1] / 1.33, across = (ox * -ax[1] + oy * ax[0]) / 1.33;
  // umber plates (darker than the grey-brown keel, v2 f0750 / v4 f2160): the upper flank lit, the lower in shadow
  let c = mix(PAL.mask(.32 + .3 * clamp(-across * 7) + .1 * (N.a(u * 20, y * 20) - .5)), KEELC(.15), .22 * clamp(across * 8));
  if (Math.abs(across - .03 - .02 * along) < .012) c = mix(c, PAL.mask(.9), .55);
  if (d > -.022) c = mix(c, across > 0 ? PAL.mask(.05) : PAL.mask(.85), .55);
  return c;
}
function keelPaint(u, v) {
  const d = keelSd(u, v);
  if (d > 0) return null;
  const y = v + JH[1], t = (y - KEEL_FOOT) / KEEL_L;
  let c = KEELC(u < 0 ? .12 + .2 * t : .42 + .15 * t);                         // the lit left flank, the shaded right flank
  c = mix(c, KEELC(.25), .2 * N.b(u * 30, y * 12));
  if (Math.abs(u) < .012) c = lift(c, .25);                                       // the ridge line
  if (t > .25 && t < .8 && Math.abs(Math.abs(u) - .06 * (1 - Math.abs(t - .52) * 2.5)) < .01) c = mix(c, PAL.mask(.9), .5);   // carved inner diamond
  if (d > -.02) c = mix(c, PAL.mask(.95), .45);
  return c;
}
function cheekPaint(u, v) {
  const d = cheekSd(u, v);
  if (d > 0) return null;
  const y = v + JH[1], x = u - CHEEK_O[0];
  // dark blades radiating from the eye corner out to the sleeve, each lit on its upper flank
  const th = Math.atan2(y - 1.5, x + .3), K = 9, sec = (th / Math.PI * K + 20) % 1, k = Math.floor(th / Math.PI * K + 20);
  let c = PAL.mask(.55 + .25 * (hash(k, 4.2) - .5) - .12 * clamp((y - 1.1) * 1.2));
  if (sec < .2) c = mix(c, PAL.mask(.22), .5 * (1 - sec / .2));
  if (sec > .9) c = mix(c, PAL.mask(.97), .55);
  if (d > -.025) c = mix(c, PAL.mask(.2), .5);
  return c;
}
// crest sheet: two blade cells (64 x 128 each); dark umber with a gold rim (the brow edging) and an amber base
function crestSheet(s, t) {
  const k = s < .5 ? 0 : 1, x = (s * 2 - k) - .5, y = 1 - t;
  const d = CREST_SD[k](x, y);
  if (d > 0) return TRANSPARENT;
  const c0 = k ? .12 * y * y : 0, side = x - c0;
  let c = PAL.plate(.5 + .25 * clamp(side * 3) + .1 * (N.a(x * 30, y * 6) - .5));
  if (y < .25) c = mix(c, PAL.plateOr(.55 + 1.6 * y), .55 * (1 - y / .25));
  if (Math.abs(side) < .012 && y > .1) c = mix(c, PAL.plate(.1), .5);                // the mid rib
  const rimSide = k ? side > 0 : true;
  if (d > -.045 && rimSide && y > .15) c = goldPx(.12 + .3 * y, x * 90, y * 90);       // gold edging
  else if (d > -.02) c = sink(c, .35);
  return c;
}
function mspikeSheet(s, t) {
  const k = s < .5 ? 0 : 1, x = s * 2 - k, y = 1 - t, b = MS[k];
  const d = b.S.sd(x / 2, y);
  if (d > 0) return TRANSPARENT;
  const n = b.S.near(x / 2, y);
  let c = PAL.mask(n.s > 0 ? .3 : .58);
  if (d > -.02) c = n.s > 0 ? lift(c, .12) : sink(c, .3);
  if (y < .3) c = mix(c, PAL.mask(.9), .35 * (1 - y / .3));
  if (Math.abs(n.s) < .008 && y > .15) c = mix(c, PAL.mask(.1), .4);
  return c;
}
function beakPaint(u, v) {
  const d = beakSd(u, v);
  if (d > 0) return null;
  const y = v + JJ[1], top = beakTopW(u), base = mouthY(u) + .04;
  // grey-cream stone, darker toward the cheek and under the chin; a deep V groove inside the outline
  let c = creamPx(u * 60 + 7, y * 60 + 3, PAL.cream, .35);
  c = mix(c, PAL.cream(.42), .35);
  c = mix(c, PAL.cream(.7), .5 * clamp(u / .78) ** 1.4);
  c = mix(c, PAL.cream(.78), .45 * clamp((.65 - y) / .45));
  const g = Math.abs(beakPoly(u, v) + .13);
  if (g < .022) c = mix(c, PAL.groove(.55), .8);
  else if (g < .04) c = mix(c, PAL.cream(.15), .35);                           // the lit lip of the groove
  if (u < .018 && y < base - .25) c = mix(c, PAL.groove(.4), .5);
  if (y > base) c = mix(PAL.teeth(.1), PAL.teeth(1), clamp((top - y) / .12));    // the tooth points of the closed mouth
  else if (y > base - .04) c = mix(c, PAL.groove(.6), .7);
  if (d > -.016) c = sink(c, .3);
  return c;
}
function earPaint(u, v) {
  if (earSd(u, v) > 0) return null;
  const x = (u - EAR_C[0]) / EAR_HW, y = (v - (EAR_C[1] - JH[1])) / EAR_HH;
  const m = Math.max(Math.abs(x), Math.abs(y));
  if (m > .88) return PAL.mask(.35);                                              // the dark mount border
  // 回: square spiral grooves on gold
  const ring = Math.abs(m - .64) < .075 || Math.abs(m - .32) < .075 || (Math.abs(x - .32) < .075 && y > -.64 && y < .32) || (Math.abs(y + .64) < .075 && x > -.32 && x < .64);
  let c = goldPx(.18 + .3 * (1 - (y + 1) / 2) + .12 * (x + 1) / 2, u * 90, v * 90);
  if (m > .78) c = PAL.gold(.08);
  if (ring) c = PAL.inlay(.55);
  return c;
}
function eyePaint(s, t) {
  const u = EYE_R.u0 + s * (EYE_R.u1 - EYE_R.u0), y = EYE_R.v1 + JH[1] - t * (EYE_R.v1 - EYE_R.v0);
  const a = (u - EYE.u) / (EYE.len / 2), off = y - eyeY(u), hh = EYE.h / 2 * (1 - a * a) ** .6 * (a < 0 ? 1 - .25 * -a : 1);
  if (Math.abs(a) > 1 || Math.abs(off) > hh) return TRANSPARENT;
  const e = Math.max(Math.abs(off) / Math.max(hh, 1e-3), Math.abs(a) ** 2);
  // (R3b, r3_critique 2.6: saturated red #F04352 with a hot #FFE0E0 core line and a thin #C81A2C halo, no pink)
  return e < .2 ? PAL.eye(0) : e < .82 ? PAL.eye(.38 + (e - .2) * .06) : PAL.eye(.6);
}
// the sleeve faces (R3b, r3_critique 2.1): overwhelmingly bright gold: a lit field gold(.15-.45) graded from the lit top
// to a deeper underside, thin low-contrast orange-brown inlay lines (1-2 px, <= 12 % of the face), a bright outer rim
// band, a darker bevelled inner lip; the inner card a shade deeper
const meander = (p, q, lw = .045) => {
  // one cell of a square-key line (p along 0..1, q across 0..1)
  const seg = [[.1, .15, .1, .85], [.1, .85, .9, .85], [.9, .85, .9, .35], [.9, .35, .45, .35], [.45, .35, .45, .6]];
  return seg.some(([x0, y0, x1, y1]) => p >= Math.min(x0, x1) - lw && p <= Math.max(x0, x1) + lw && q >= Math.min(y0, y1) - lw && q <= Math.max(y0, y1) + lw);
};
function sleevePaint(inner) {
  return (u, v) => {
    const d = SLV.sd(u, v);
    if (d > 0) return null;
    const n = SLV.near(u, v), w = SLEEVE_W(n.t) / 2, a = n.s / w;              // a: -1 (convex, outer rim) .. +1 (concave edge)
    const lit = clamp((v + 1.0) / 2.1), deep = inner ? .08 : 0;                // 0 at the lower end .. 1 at the mouth
    let c;
    if (a < -.55) c = goldPx(.06 + .12 * (1 - lit) + deep, u * 70, v * 70);      // the bright outer rim
    else if (a > .7) c = mix(PAL.gold(.5 + .12 * (1 - lit) + deep), PAL.inlay(.2), .25);   // the darker inner lip
    else {
      c = goldPx(.16 + .28 * (1 - lit) + deep + .05 * Math.abs(a), u * 70, v * 70);
      const L = n.t * SLV.L, p = ((L / .34) % 1 + 1) % 1, q = (a + .45) / 1.1;
      if (n.t > .1 && n.t < .97 && q > 0 && q < 1 && meander(p, q)) c = mix(c, PAL.inlay(.05), .75);
      if (Math.abs(a + .55) < .025 || Math.abs(a - .7) < .025) c = mix(c, PAL.inlay(.2), .7);   // fine grooves bounding the face
    }
    if (d > -.014) c = sink(c, .25);
    return c;
  };
}
// the dark horn: near-black brown, a faint warm sheen along the convex (back / upper) flank, fine growth ridges across,
// the concave flank and the outline deeper, a slightly worn paler tip
function dhornPaint(u, v) {
  const d = DHS.sd(u, v);
  if (d > 0) return null;
  const n = DHS.near(u, v), w = DHORN_W(n.t) / 2, a = clamp(n.s / Math.max(w, 1e-3), -1, 1);   // a < 0: convex flank
  let c = PAL.horn(.62 + .22 * a + .08 * (N.a(u * 30, v * 30) - .5));
  if (a < -.35) c = mix(c, PAL.horn(.12), .55 * clamp((-a - .35) / .4));
  if (a < -.55 && a > -.85) c = mix(c, C('#7A5A44'), .22);                         // the warm sheen
  const L = n.t * DHS.L;
  if (((L / .17) % 1 + 1) % 1 < .12 && n.t < .85) c = sink(c, .3);                // growth ridges
  if (n.t > .82) c = mix(c, PAL.horn(.05), .5 * (n.t - .82) / .18);                // worn tip
  if (d > -.016) c = sink(c, .35);
  return c;
}
// bib: layered cream stone, grooves parallel to the serrated lower edge, the lower rim lit, darker up under the jaw and
// on the side facets (turned away)
function bibPaint(name, side) {
  const {f, sd, R} = BEARDS[name];
  return (u, v) => {
    const au = Math.abs(u), d = sd(au, v);
    if (d > 0) return null;
    const t = clamp((v - R.v0) / (R.v1 - R.v0));
    let c = creamPx(au * 70 + 31, v * 70, PAL.cream, .4);
    c = mix(c, PAL.cream(.72), .15 + .45 * t ** 1.5 + (side ? .12 : 0));
    const g = (((-d) / .13) % 1 + 1) % 1;
    if (g > .82 && -d > .05) c = mix(c, PAL.groove(.5), .55);                       // the layer seams
    else if (g < .12 && -d > .05) c = mix(c, PAL.cream(.08), .3);                   // each layer's lit lip
    if (au < .02 && !side) c = mix(c, PAL.groove(.4), .4);
    if (d > -.03) c = mix(c, PAL.cream(.05), .45);
    if (d > -.012) c = sink(c, .3);
    return c;
  };
}
// cheek plate of the lower jaw: the beak's cream stone continued, an engraved groove inset along its outline (like the
// shield's V groove), a darker hinge end, the upper margin tucked under the mask in shadow
function jsidePaint(u, v) {
  const d = jsideSd(u, v);
  if (d > 0) return null;
  const z = u + JJ[2], y = v + JJ[1];
  let c = creamPx(z * 60 + 11, y * 60 + 5, PAL.cream, .35);
  c = mix(c, PAL.cream(.42), .35);
  c = mix(c, PAL.cream(.75), .45 * clamp((z + 3.75) / .5));                     // toward the hinge
  c = mix(c, PAL.cream(.7), .3 * clamp((y - .95) / .2));                          // under the mask
  const g = Math.abs(d + .12);
  if (g < .02 && z < -3.45) c = mix(c, PAL.groove(.55), .75);
  else if (g < .036 && z < -3.45) c = mix(c, PAL.cream(.15), .3);
  if (d > -.016) c = sink(c, .3);
  return c;
}
function junderPaint(x, zl) {
  const d = underSd(x, zl);
  if (d > 0) return null;
  const z = zl + JJ[2];
  let c = creamPx(x * 70 + 41, z * 70, PAL.cream, .4);
  c = mix(c, PAL.cream(.6), .3);
  if (((((z + 4.5) / .2) % 1) + 1) % 1 > .85) c = mix(c, PAL.groove(.5), .45);   // transverse plates
  if (Math.abs(x) < .015) c = mix(c, PAL.groove(.4), .35);
  if (d > -.02) c = sink(c, .25);
  return c;
}
export function sprites() {
  const S = {};
  const card = (name, rect, ppb, fn) => { const [w, h] = spriteSize(rect, ppb); S[name] = [w, h, onRect(rect, fn), false]; };
  S.mask = [64, 64, maskTile, false];
  S.teeth = [16, 16, (s, t) => PAL.teeth(.15 + .7 * t), false];
  S.knob = [16, 16, (s, t) => goldPx(.2, s * 16, t * 16), false];
  S.tongue = [32, 32, (s, t) => mix(PAL.tongue, PAL.gum(.6), .4 * N.a(s * 5, t * 5)), false];
  S.mspikes = [64, 64, mspikeSheet, false];
  S.crest = [128, 128, crestSheet, false];
  card('face', rectOf(MASK_P), 112, facePaint);
  card('ledge', rectOf(LEDGE_P), 96, ledgePaint);
  card('wing', rectOf(WING_P), 96, wingPaint);
  card('keel', KEEL, 96, keelPaint);
  card('cheek', rectOf(CHEEK_P), 64, cheekPaint);
  card('beak', rectOf(BEAK_P), 112, beakPaint);
  card('ear', EAR, 96, earPaint);
  S.eye = [64, 32, eyePaint, false];
  card('sleeve', SLEEVE_RECT, 80, sleevePaint(false));
  card('sleeve_in', SLEEVE_RECT, 48, sleevePaint(true));
  card('dhorn', DH_RECT, 64, dhornPaint);
  for (const n of Object.keys(BEARDS)) {
    const R = BEARDS[n].R;
    card(n + 'f', {u0: -BIB_F - .05, u1: BIB_F + .05, v0: R.v0, v1: R.v1}, 64, bibPaint(n, false));
    card(n + 's', {u0: BIB_F, u1: R.u1, v0: R.v0, v1: R.v1}, 64, bibPaint(n, true));
  }
  card('jside', rectOf(JSIDE_P), 64, jsidePaint);
  {
    // a 'y' plane card maps the sprite's t along +Z (the slab convention), not down the v axis as onRect does
    const R = rectOf(UNDER_P.map(([x, z]) => [x, z - JJ[2]]), .02), [w, h] = spriteSize(R, 48);
    S.junder = [w, h, (s, t) => junderPaint(R.u0 + s * (R.u1 - R.u0), R.v0 + t * (R.v1 - R.v0)) || TRANSPARENT, false];
  }
  return S;
}
