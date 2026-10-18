// HEAD region of the 야타용왕 (Azhdaha) rig (model.md §0, §3.1, §3.2): the dark faceted rock mask with the grey-brown
// keel blade, the radiating brow spikes and crest plates, the brow ridges over the red slit eyes (their own bright part),
// the meander ear plates (回), the upper teeth and palate; the jaw with the cream chin shield (serrated upper edge =
// the closed mouth line), lower teeth, two fangs and the tongue; the two composite horns (gold sleeve C with the
// meander inlay and the round knob, the near-black horn growing out of its top); the layered cream beard plates.
// Region interface: see azhdaha_body.mjs. Frames (azhdaha_pose.mjs): head = the atlas J.head, rest = the head-low
// idle; jaw = the hinge J.jaw; horn_* = HORN.at in the head frame turned by HORN.e (the C lies in its own YZ plane);
// beard1 / beard2 = J.beard1 / J.beard2.
import {loft, slab, crossCards, rockBox, toUnits, retex, mirrorX, stroke, sdPoly, registerTile, hash} from './azhdaha_shape.mjs';
import {PART_SCALE, J} from './azhdaha_pose.mjs';
import {PAL, C, clamp, smooth, mix, lift, sink, N, spriteSize, onRect, TRANSPARENT, creamPx, goldPx, bevelLight, cells} from './azhdaha_materials.mjs';
const cellsAt = (x, y) => cells(x, y, 41);
import {cardZ, rotA} from './mboss_model_lib.mjs';

export const REGION = 'head';
export const PARTS = [
  ['head', 'head', 13], ['jaw', 'jaw', 13], ['eyes', 'eyes', 15], ['horn_l', 'horn_l', 14], ['horn_r', 'horn_r', 14],
  ['beard1', 'beard1', 13], ['beard2', 'beard2', 13],
];
registerTile('mask', 64, 64, 48);
registerTile('teeth', 16, 16, 48);
registerTile('tongue', 32, 32, 48);
const sinD = th => Math.sin(th * Math.PI / 180), cosD = th => Math.cos(th * Math.PI / 180);
// head frame stations from WORLD rows [z, half width, top y, bottom y, box] (the atlas J.head at the origin)
const st = (o, rows) => rows.map(([z, w, top, bot, box = .3]) => ({a: z - o[2], r: [w, (top - bot) / 2, w, (top - bot) / 2], c: [0, (top + bot) / 2 - o[1]], box}));

// ---- skull / face mask ------------------------------------------------------------------------------------------------------------
// The skull is a loft (snout, cheeks, crest, occiput); the face front is two painted half-mask plates meeting in a
// ridge on the midline and turned back 22.5 degrees (a forward-pointing wedge), the eyes on them (the eyes part), the
// keel blade in front of the ridge, a crown of dark spikes radiating from the plates' top edge.
const FACE_Z = -1.02;                       // the half-mask plane (head frame), turned about (0, y, FACE_Z)
const FACE = {u0: 0, u1: 1.02, v0: -1.02, v1: .82};
const FACE_P = [[0, -1.02], [.2, -1.0], [.44, -.84], [.72, -.55], [.95, -.2], [1.0, .15], [.86, .45], [.52, .7], [.15, .8], [0, .64]];   // a wedge: narrow at the snout, widest at the brow
const faceSd = sdPoly(FACE_P);
export const EYE = {x: .42, y: -.52, w: .5, h: .24};
function skull() {
  const H = J.head;
  // the snout stays under the eyes (top 1.25) in front of the half-mask plane; the crest grows behind it
  const els = loft('z', st(H, [[-5.02, .42, 1.1, .8, .45], [-4.75, .55, 1.2, .76], [-4.45, .64, 1.25, .77], [-4.2, .72, 1.28, .78], [-3.95, .95, 2.3, .86],
    [-3.5, 1.12, 2.6, .98], [-3.0, 1.1, 2.62, 1.15], [-2.55, .85, 2.45, 1.35, .2]]),
  {tex: (k, th, i) => (sinD(th) < -.6 && i < 4 ? 'mouth' : 'mask'), caps: '-+', seed: 401});
  // left half: the face plate, the crown spikes along its top edge (mirrored for the right)
  const half = [...slab({plane: 'z', at: FACE_Z, rect: FACE, sd: faceSd, half: .08, sprite: 'face', edge: 'mask', cell: .1, rot: ['y', -22.5, [0, 0, FACE_Z]]})];
  const CROWN = [[.16, .5, 1.2, 0, 0], [.46, .42, 1.15, -22.5, 1], [.76, .18, 1.0, -45, 0], [.95, -.15, .8, -45, 1]];
  for (const [x, y, L, rz, k] of CROWN) {
    const z = FACE_Z + .06 + x * .41;       // just behind the turned plate
    half.push(...mspike('z', [x, y, z], L, k, rz, 1));
  }
  els.push(...half, ...mirrorX(half));
  // keel blade: a front-facing grey-brown diamond up the forehead, tilted back with the slope, a ridge core behind
  els.push(...slab({plane: 'z', at: -1.14, rect: KEEL, sd: keelSd, half: .1, sprite: 'keel', edge: 'mask', cell: .1, rot: ['x', 22.5, [0, -.4, -1.14]]}));
  // crest plates leaning back over the crown into the neck ruff
  for (const [x, y, z, L, k, sp] of [[0, .45, -.25, 1.0, 1, 0], [.42, .38, -.05, .85, 0, -22.5], [.78, .18, .15, .7, 1, -45], [0, .35, .3, .8, 0, 0]])
    for (const s of x ? [1, -1] : [1]) els.push(...mspike('x', [s * x, y, z], L, k, sp * s, s));
  // the meander ear plates (回) on dark mounts behind the sleeves, facing out and forward
  const ear = [rockBox([1.05, -.42, -.32], [1.42, .2, .12], 'mask', {seed: 7}),
    ...slab({plane: 'z', at: -.38, rect: EAR, sd: earSd, half: .06, sprite: 'ear', edge: 'gold', cell: .08, rot: ['y', 45, [1.3, -.1, -.38]]})];
  els.push(...ear, ...mirrorX(ear));
  // upper teeth along the front of the palate (blocky, 0.15-0.2 b) behind the closed-mouth line
  for (const [x, z] of UPPER_TEETH) for (const s of x ? [1, -1] : [1]) els.push(rockBox([s * x - .08, -1.47, z - .07], [s * x + .08, -1.25, z + .07], 'teeth', {seed: x * 30 + z}));
  return els;
}
const UPPER_TEETH = [[.1, -1.62], [.28, -1.52], [.42, -1.32], [.52, -1.08], [.58, -.82]];
// ear plate shape: a square with a notched corner (plane z: u = X, v = Y), centred on (1.3, -0.1)
const EAR = {u0: 1.0, u1: 1.6, v0: -.38, v1: .18};
const earSd = (u, v) => Math.max(Math.abs(u - 1.3) - .29, Math.abs(v + .1) - .27);
// keel: diamond from the nose bridge (y -0.95) to a point above the crest (y +0.75), widest 0.24 half at y -0.15
const KEEL = {u0: -.34, u1: .34, v0: -1.12, v1: 1.06};
const keelSd = (u, v) => { const t = v < -.05 ? (v + 1.12) / 1.07 : (1.06 - v) / 1.11; return Math.abs(u) - .3 * clamp(t) ** .75 + (v < -1.12 || v > 1.06 ? 1 : 0); };
// dark mask spikes (2 shapes in a 2-cell sheet, cells 32 x 64): plane 'z' faces front, 'x' faces the side
const MSP = [{c: [.45, .5], t: [.55, 1], w: .42}, {c: [.4, .55], t: [.8, .95], w: .44}];
const MS = MSP.map(b => { const pts = Array.from({length: 11}, (_, i) => { const t = i / 10; return [0, 1].map(k => (1 - t) ** 2 * [.5, 0][k] + 2 * (1 - t) * t * b.c[k] + t * t * b.t[k]); }).map(([x, y]) => [x / 2, y]);
  return {...b, S: stroke(pts, t => b.w / 2 * (1 - t) ** .8)}; });
function mspike(plane, [x, y, z], L, k, rotDeg, side) {
  const W = L * .5, c = plane === 'x' ? z : x, flip = plane === 'z' && side < 0;
  const rect = {u0: c - .5 * W, u1: c + .5 * W, v0: y, v1: y + L};
  const sd = (u, v) => { let nu = (u - rect.u0) / W; if (flip) nu = 1 - nu; return MS[k].S.sd(nu / 2, (v - y) / L) * L; };
  const els = slab({plane, at: plane === 'x' ? x : z, rect, sd, half: .06, sprite: 'mspikes', edge: 'mask', cell: .09, core: L > .5,
    rot: rotDeg ? [plane === 'x' ? 'z' : 'z', rotDeg, [x, y, z]] : null});
  for (const e of els) for (const f of Object.values(e.faces)) if (f.texture === '#mspikes') {
    let [a, b, c2, d] = f.uv; if (flip) [a, c2] = [16 - a, 16 - c2];
    f.uv = [k * 8 + a / 2, b, k * 8 + c2 / 2, d].map(v => +v.toFixed(4));
  }
  return els;
}

// ---- jaw: cream chin shield and lower jaw, lower teeth, fangs, tongue -----------------------------------------------------------
function jaw() {
  const Jw = J.jaw;
  const els = loft('z', st(Jw, [[-5.0, .3, .74, .3, .4], [-4.85, .48, .76, .2], [-4.4, .7, .8, .3], [-3.9, .86, .9, .45], [-3.4, .95, 1.32, .62, .35], [-3.15, .8, 1.4, .8, .2]]),
    {tex: (k, th) => (sinD(th) > .6 ? 'mouth' : 'cream'), caps: '-+', seed: 431});
  // the chin shield: a front-facing cream plate with the serrated top edge (the closed mouth line), wrapping the chin
  els.push(...slab({plane: 'z', at: -1.42, rect: BEAK, sd: beakSd, half: .07, sprite: 'beak', edge: 'cream', cell: .08}));
  for (const s of [1, -1]) els.push(...slab({plane: 'z', at: -1.42, rect: BEAK, sd: beakSd, half: .07, sprite: 'beak', edge: 'cream', cell: .08,
    clip: s > 0 ? {u0: .38} : {u1: -.38}, rot: ['y', s * 45, [s * .38, -.8, -1.42]]}));
  // lower teeth rising from the jaw rim, two big fangs at the corners, the tongue
  for (const [x, z] of [[.12, -1.3], [.3, -1.18], [.5, -.62], [.56, -.3]]) for (const s of [1, -1]) els.push(rockBox([s * x - .08, -.6, z - .07], [s * x + .08, -.4, z + .07], 'teeth', {seed: x * 20 + z}));
  for (const s of [1, -1]) els.push(rockBox([s * .4 - .1, -.62, -1.0], [s * .4 + .1, -.22, -.82], 'teeth', {seed: 5 * s}), rockBox([s * .4 - .06, -.22, -.95], [s * .4 + .06, -.08, -.86], 'teeth', {seed: 6 * s}));
  els.push(rockBox([-.42, -.66, -1.15], [.42, -.56, -.05], {all: 'tongue', down: 'mouth'}, {seed: 9}));
  return els;
}
// beak (chin shield): plane z in the jaw frame, u = X, v = Y; serrated top at y -0.42, point at y -1.2
const BEAK = {u0: -.62, u1: .62, v0: -1.25, v1: -.32};
const beakTop = u => -.44 + .07 * Math.abs(((u * 5.2) % 1 + 1) % 1 - .5) * 2;
const beakSd = (u, v) => Math.max(v - beakTop(u), Math.abs(u) - (.56 - .5 * clamp((-.44 - v) / .78) ** 1.25), -1.22 - v);   // a V-shaped chin

// ---- eyes (bright part, brightness 15): slanted red slits on the mask's front-side facets ----------------------------------------
function eyes() {
  const z = FACE_Z - .08 - .012 - .02;      // just in front of the half-mask card, turned with it
  const e = [cardZ('eye', z, {X0: EYE.x - EYE.w / 2, X1: EYE.x + EYE.w / 2, Y0: EYE.y - EYE.h / 2, Y1: EYE.y + EYE.h / 2}, {rot: ['y', -22.5, [0, 0, FACE_Z]]})];
  return [...e, ...mirrorX(e)];
}

// ---- horns: the gold sleeve C (two arcs: the upper one in the horn plane, the lower turned 22.5 more so the knob comes
// in beside the mouth) and the dark horn growing out of its top, curling forward (model.md §3.1) ----------------------------------
// C centreline in the horn plane (u = Z, v = Y; the pivot = the widest point at eye height)
const C_UP = [[0, 0], [-.04, .45], [-.12, .95], [-.3, 1.4]];
const C_LO = [[0, 0], [-.12, -.32], [-.38, -.6], [-.66, -.74], [-.88, -.78]];
const SLV = (() => {
  const pts = [...C_LO.slice().reverse(), ...C_UP.slice(1)];        // knob -> top
  const S = stroke(pts, t => .36 - .08 * t);
  return {S, pts};
})();
const SLEEVE_RECT = {u0: -1.35, u1: .5, v0: -1.2, v1: 1.75};
const sleeveSd = (u, v) => SLV.S.sd(u, v);
const knobAt = [0, -.8, -.98];
const DH = (() => { const pts = Array.from({length: 13}, (_, i) => { const t = i / 12; return [0, 1].map(k => (1 - t) ** 2 * [-.28, 1.25][k] + 2 * (1 - t) * t * [-.32, 2.45][k] + t * t * [-1.15, 2.6][k]); }); return {pts, S: stroke(pts, t => .3 * (1 - t) ** .8 + .02)}; })();
const DHORN_RECT = {u0: -1.35, u1: .1, v0: 1.0, v1: 2.75};
function horn() {
  const els = [];
  // upper arc (in the plane), lower arc turned 22.5 about Y round the pivot (its knob end swings inward)
  els.push(...slab({plane: 'x', at: 0, rect: SLEEVE_RECT, sd: sleeveSd, half: {along: 'v', bands: 3, h: t => .3 - .07 * t}, sprite: 'sleeve', edge: 'gold', cell: .08}));
  // the knob: a round gold bulb at the lower end
  const k = knobAt;
  els.push(...loft('z', [{a: k[2] - .3, r: .13, c: [k[0], k[1]]}, {a: k[2] - .18, r: .26, c: [k[0], k[1]]}, {a: k[2] + .04, r: .3, c: [k[0], k[1]]}, {a: k[2] + .24, r: .24, c: [k[0], k[1]]}],
    {tex: 'gold', caps: '-+', seed: 451}));
  // dark horn: tapering thickness bands up the curl
  els.push(...slab({plane: 'x', at: 0, rect: DHORN_RECT, sd: (u, v) => DH.S.sd(u, v), half: {along: 'v', bands: 3, h: t => .22 - .14 * t}, sprite: 'dhorn', edge: 'horn', cell: .08}));
  return els;
}

// ---- beard: layered cream plates (front-facing, hanging from the throat) ------------------------------------------------------
const BEARD1 = {u0: -.85, u1: .85, v0: -.75, v1: .05};
const beard1Sd = (u, v) => Math.max(v - .02, Math.min(...[-.5, 0, .5].map(c => { const a = Math.abs(u - c); return a * 1.3 - (v + .72) * .95; })), Math.abs(u) - .82);
const BEARD2 = {u0: -.65, u1: .65, v0: -.68, v1: .05};
const beard2Sd = (u, v) => Math.max(v - .02, Math.min(...[-.3, .3].map(c => Math.abs(u - c) * 1.2 - (v + .65) * 1.05)), Math.abs(u) - .62);
function beard(rect, sd, sprite, z) {
  return [...slab({plane: 'z', at: z, rect, sd, half: .07, sprite, edge: 'cream', cell: .09}),
    ...slab({plane: 'z', at: z + .18, rect, sd: (u, v) => sd(u * 1.12, v * 1.05), half: .06, sprite, edge: 'cream', cell: .1, rot: ['x', 22.5, [0, 0, z + .18]]})];
}

// ---- region exports ------------------------------------------------------------------------------------------------------------
const U = (part, els) => toUnits(els, PART_SCALE[part]);
export function models() {
  const h = horn();
  return {
    head: U('head', skull()), jaw: U('jaw', jaw()), eyes: U('eyes', eyes()),
    horn_l: U('horn_l', h), horn_r: U('horn_r', mirrorX(h)),
    beard1: U('beard1', beard(BEARD1, beard1Sd, 'beard1', -.15)), beard2: U('beard2', beard(BEARD2, beard2Sd, 'beard2', -.1)),
  };
}
export const LOOKS = {};
export const TINTED = {};
export const LOOK_BRIGHT = {};

// ---- sprites ----------------------------------------------------------------------------------------------------------------
function maskTile(s, t) {
  // faceted dark rock: large flat facets (each a slightly different value), lit facet edges, a few cracks
  const u = s * 64, v = t * 64;
  const c0 = cellsAt(u / 22, v / 22);
  let c = PAL.mask(.38 + .22 * (c0.id - .5));
  if (c0.d2 - c0.d1 < .05) c = PAL.mask(.12);
  else if (c0.d2 - c0.d1 < .1) c = mix(c, PAL.mask(.2), .5);
  if (Math.abs(N.d(u * .05, v * .025) - .5) < .012) c = sink(c, .45);
  return c;
}
function facePaint(u, v) {
  const d = faceSd(u, v);
  if (d > 0) return null;
  // facets radiating from the eye toward the edges, the eye socket a dark recess, a heavy brow above it
  const c0 = cellsAt(u * 3.2 + 3, v * 3.2 + 3);
  let c = PAL.mask(.48 + .22 * (c0.id - .5) - .1 * clamp(1 - Math.hypot(u - .45, v + .1) / .9));
  if (c0.d2 - c0.d1 < .045) c = PAL.mask(.18 + .1 * c0.id);
  const ex = (u - EYE.x) / (EYE.w * .62), ey = (v - EYE.y - .25 * (u - EYE.x)) / (EYE.h * .9);
  const er = Math.hypot(ex, ey);
  if (er < 1) c = mix(PAL.mask(.95), PAL.eye(.75), .5 * (1 - er) ** .5);       // the socket, red glow spill
  const brow = v - (EYE.y + .2 + .25 * (u - EYE.x));
  if (brow > 0 && brow < .12 && u > .1 && u < .85) c = mix(c, PAL.mask(.05), .55 * (1 - brow / .12));   // brow ridge lit edge
  if (d > -.025) c = PAL.mask(.75);
  if (u < .03) c = PAL.mask(.15);                                                 // the midline ridge
  return c;
}
function keelPaint(u, v) {
  const d = keelSd(u, v);
  if (d > 0) return null;
  let c = PAL.mask(u < 0 ? .02 : .2);
  c = mix(c, C('#9A7A62'), .35 * (1 - Math.abs(u) / .3));
  if (Math.abs(u) < .015) c = lift(c, .2);
  if (d > -.025) c = sink(c, .35);
  return c;
}
function mspikeSheet(s, t) {
  const k = s < .5 ? 0 : 1, x = s * 2 - k, y = 1 - t, b = MS[k];
  const d = b.S.sd(x / 2, y);
  if (d > 0) return TRANSPARENT;
  const n = b.S.near(x / 2, y);
  let c = PAL.mask(n.s > 0 ? .25 : .5);
  if (d > -.02) c = sink(c, .3);
  if (y > .7) c = mix(c, PAL.mask(.05), .3);
  return c;
}
function beakPaint(u, v) {
  const d = beakSd(u, v);
  if (d > 0) return null;
  let c = creamPx(u * 60 + 7, v * 60 + 3);
  c = mix(c, PAL.cream(.5), .4 * Math.abs(u) / .6);
  // engraved lines: a V following the outline and a vertical centre groove
  const g = Math.min(Math.abs(d + .1), Math.abs(u) + (v < -.62 ? 0 : 9));
  if (g < .016) c = mix(c, PAL.groove(.4), .7);
  if (v > beakTop(u) - .05) c = lift(c, .2);             // the tooth tips of the closed mouth
  if (d > -.02) c = sink(c, .25);
  return c;
}
function earPaint(u, v) {
  if (earSd(u, v) > 0) return null;
  const x = (u - 1.3) / .29, y = (v + .1) / .27;      // -1..1
  const m = Math.max(Math.abs(x), Math.abs(y));
  if (m > .86) return PAL.mask(.3);                    // the dark mount border
  // 回: square spiral grooves on gold
  const ring = Math.abs(m - .62) < .07 || Math.abs(m - .3) < .07 || (Math.abs(x - .3) < .07 && y > -.62 && y < .3) || (Math.abs(y + .62) < .07 && x > -.3 && x < .62);
  let c = goldPx(.2 + .25 * (y + 1) / 2, u * 90, v * 90);
  if (ring) c = PAL.inlay(.6);
  return c;
}
function eyePaint(s, t) {
  // a slanted slit, inner end (u 0) lower: hot core, red body, soft falloff
  const x = s * 2 - 1, y = (1 - t) * 2 - 1, slit = y - .32 * x;
  const e = Math.hypot(x / 1.0, slit / (.36 * (1 - .35 * x * x)));
  if (e > 1) return TRANSPARENT;
  return e < .4 ? PAL.eye(0) : e < .72 ? PAL.eye(.18 + (e - .4) * .8) : PAL.eye(.45 + (e - .72) * 1.2);
}
function sleevePaint(u, v) {
  const d = sleeveSd(u, v);
  if (d > 0) return null;
  const n = SLV.S.near(u, v), w = .36 - .08 * n.t, a = n.s / w;           // a: -1 .. 1 across the band (+ = outer edge)
  let c = goldPx(.22 + .18 * (1 - n.t) - .15 * a, u * 70, v * 70);
  if (a > .62) c = PAL.gold(a > .8 ? .05 : .3);                          // the raised outer rim, bright
  if (a < -.8) c = PAL.gold(.7);                                         // dark amber inner edge
  // orange-brown meander inlay along the band: a stepped key pattern between a -.45 and .45
  const L = n.t * SLV.S.L, p = ((L / .3) % 1 + 1) % 1, step = Math.floor(L / .3) % 2;
  const yk = step ? (p < .5 ? .35 : -.35) : (p < .5 ? -.35 : .35);
  const onLine = Math.abs(a - yk) < .09 || (Math.abs(p - .5) < .06 && Math.abs(a) < .4) || Math.abs(Math.abs(a) - .52) < .045;
  if (onLine && n.t > .06 && n.t < .97) c = PAL.inlay(.4 + .3 * (a + 1) / 2);
  if (d > -.02) c = sink(c, .3);
  return c;
}
function dhornPaint(u, v) {
  const d = DH.S.sd(u, v);
  if (d > 0) return null;
  const n = DH.S.near(u, v), a = n.s / (.3 * (1 - n.t) ** .8 + .02);
  let c = PAL.horn(.45 + .25 * n.t - .25 * a);
  if (a > .55) c = mix(c, PAL.horn(.0), .5);                              // the warm highlight edge
  if (Math.abs(N.a(u * 18, v * 6) - .5) < .02) c = sink(c, .3);
  return c;
}
function beardPaint(sd) {
  return (u, v) => {
    const d = sd(u, v);
    if (d > 0) return null;
    let c = creamPx(u * 70 + 31, v * 70);
    const g = Math.abs(((u * 4.2) % 1 + 1) % 1 - .5);
    if (g < .05) c = mix(c, PAL.groove(.3), .45);                        // vertical striations of the stone plates
    if (d > -.025) c = sink(c, .25);
    return c;
  };
}
export function sprites() {
  const S = {};
  const card = (name, rect, ppb, fn, tr = false) => { const [w, h] = spriteSize(rect, ppb); S[name] = [w, h, onRect(rect, fn), tr]; };
  S.mask = [64, 64, maskTile, false];
  S.teeth = [16, 16, (s, t) => PAL.teeth(.2 + .6 * t), false];
  S.tongue = [32, 32, (s, t) => mix(PAL.tongue, PAL.gum(.6), .4 * N.a(s * 5, t * 5)), false];
  S.mspikes = [64, 64, mspikeSheet, false];
  card('keel', KEEL, 96, keelPaint);
  card('face', FACE, 112, facePaint);
  card('beak', BEAK, 96, beakPaint);
  card('ear', EAR, 96, earPaint);
  S.eye = [64, 32, eyePaint, false];
  card('sleeve', SLEEVE_RECT, 96, sleevePaint);
  card('dhorn', DHORN_RECT, 64, dhornPaint);
  card('beard1', BEARD1, 64, beardPaint(beard1Sd));
  card('beard2', BEARD2, 64, beardPaint(beard2Sd));
  return S;
}
