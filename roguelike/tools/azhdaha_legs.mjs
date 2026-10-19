// LEGS region of the 야타용왕 (Azhdaha) rig (model.md §3.7, §3.8, §4.2, §7.3 option 2; R2 rebuild after
// az/rigwork/r1_critique.md §4):
//   fore   uarm_*   the upper-arm muscle mass (pebble hide), shoulder -> into the bracer crown
//          bracer_* the octagonal carved stone column (8 staves, ragged crown, painted gold studs, flared foot rim)
//                   with 4 amber hexagonal crystals jutting back and up from the elbow
//          paw_*    pale knuckle pad, 4 toes with 4 big conical black talons, a dew claw on the inside
//   hind   thigh_*  the haunch mass (pebble hide) hiding the knee and the shin
//          gaiter_* the shin (knee -> hock), a short hide segment: it only shows when the leg stretches
//          foot_*   the near-vertical ribbed gaiter column (the metatarsus, hock 1.5 b -> 0.35 b): dark collar with the
//                   orange heel spur and two gold knobs, 4 stone rings on a darker core, the carved plinth, 3 toes with
//                   big talons + a small inner one
//   glow   glow_bracer_*, glow_gaiter_* (the latter follows foot_*): white line masks 0.025 b proud, tinted per element
// Paired parts are authored for the LEFT leg (+X = outer) and mirrored for the right (azhdaha_shape mirrorX).
//
// Part frames (azhdaha_pose.mjs solve): uarm / thigh are REST-ALIGNED (the rig axes of the rest pose about the shoulder /
// hip); bracer / gaiter are bone-aligned (-Y from the elbow / knee toward the wrist / hock, front -Z); paw / foot sit at
// the wrist / hock with their eulers (rest: rig axes; soles at y SOLE.paw / SOLE.foot).
//
// Element economy: lofts are built without the 16-quad ledge rings and caps of azhdaha_shape.loft; steps and ends are
// closed by cut-out DISCS instead (one quad per quadrant showing an alpha-cut n-gon sprite that meets the facets).
import {loft, rockBox, toUnits, mirrorX, stroke, bez, registerTile, registerWrap, hash} from './azhdaha_shape.mjs';
import {PART_SCALE, ARM, LEG, J} from './azhdaha_pose.mjs';
import {PAL, LOOK_PAL, TILES, C, clamp, smooth, mix, lift, sink, scale, N, TRANSPARENT, ramp, hidePx} from './azhdaha_materials.mjs';
import {cardX, cardZ, faceEl, faceOfDir} from './mboss_model_lib.mjs';

export const REGION = 'legs';
export const PARTS = [
  ['uarm_l', 'uarm_l', 13], ['bracer_l', 'bracer_l', 13], ['paw_l', 'paw_l', 13],
  ['uarm_r', 'uarm_r', 13], ['bracer_r', 'bracer_r', 13], ['paw_r', 'paw_r', 13],
  ['thigh_l', 'thigh_l', 13], ['gaiter_l', 'gaiter_l', 13], ['foot_l', 'foot_l', 13],
  ['thigh_r', 'thigh_r', 13], ['gaiter_r', 'gaiter_r', 13], ['foot_r', 'foot_r', 13],
  ['glow_bracer_l', 'empty', 15], ['glow_bracer_r', 'empty', 15], ['glow_gaiter_l', 'empty', 15], ['glow_gaiter_r', 'empty', 15],
];
const LOOKS_EL = ['hydro', 'pyro'];
const sfx = look => (look ? '_' + look : '');
const ALL = [null, ...LOOKS_EL];
for (const l of ALL.map(sfx)) {
  for (const n of ['bracer', 'crown', 'gaiter', 'plinth', 'collar']) registerWrap(n + l);
  registerTile('toestone' + l, 64, 64, 32); registerTile('gcore' + l, 32, 32, 32);
  registerTile('claw' + l, 32, 32, 48);
}
for (const n of ['bracer_mask', 'gaiter_mask']) registerWrap(n);
registerTile('crystal', 32, 32, 48);
const add = (a, b) => a.map((x, i) => x + b[i]), sc = (v, s) => v.map(x => x * s), dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];

// ---- solids: facet lofts closed by cut-out discs -----------------------------------------------------------------------
const FRAME = {y: {A: [0, 1, 0], e1: [1, 0, 0], e2: [0, 0, -1]}, z: {A: [0, 0, 1], e1: [1, 0, 0], e2: [0, 1, 0]}, x: {A: [1, 0, 0], e1: [0, 0, -1], e2: [0, 1, 0]}};
const R4 = r => (Array.isArray(r) ? r : [r, r, r, r]);
// A flat cut-out disc across the axis at a with a loft section's profile (r = [e1+, e2+, e1-, e2-], centre c): 1, 2 or 4
// quads (split where the profile is not symmetric) showing the matching quarter of a disc sprite painted as the regular
// n-gon of the loft (circumradius = the quad edge), so its outline meets the facets. side: '+', '-' or '+-'.
function disc(axis, a, r, c, sprite, side, n = 16) {
  const {A, e1, e2} = FRAME[axis], k = 1 / Math.cos(Math.PI / n), R = R4(r).map(x => x * k);
  const O = add(sc(A, a), add(sc(e1, c[0]), sc(e2, c[1])));
  const sp1 = Math.abs(R[0] - R[2]) < 1e-6 ? [[-1, 1]] : [[-1, 0], [0, 1]], sp2 = Math.abs(R[1] - R[3]) < 1e-6 ? [[-1, 1]] : [[-1, 0], [0, 1]];
  const P = (s1, s2) => add(O, add(sc(e1, s1 >= 0 ? s1 * R[0] : s1 * R[2]), sc(e2, s2 >= 0 ? s2 * R[1] : s2 * R[3])));
  const fn = X => { const d = [X[0] - O[0], X[1] - O[1], X[2] - O[2]], d1 = dot(d, e1), d2 = dot(d, e2);
    return [8 + 8 * (d1 >= 0 ? d1 / R[0] : d1 / R[2]), 8 - 8 * (d2 >= 0 ? d2 / R[1] : d2 / R[3])]; };
  const els = [];
  for (const [p0, p1] of sp1) for (const [q0, q1] of sp2) {
    const faces = {};
    for (const sd of side) faces[faceOfDir(sc(A, sd === '+' ? 1 : -1))] = {tex: sprite, fn};
    els.push(faceEl([P(p0, q0), P(p1, q1)], faces, {shade: true}));
  }
  return els;
}
// Section profiles of a loft (each section = the mean of its two stations, as azhdaha_shape.loft builds them).
const sections = st => st.slice(0, -1).map((s0, i) => { const s1 = st[i + 1], m = (x, y) => (x + y) / 2, r0 = R4(s0.r), r1 = R4(s1.r), c0 = s0.c || [0, 0], c1 = s1.c || [0, 0];
  return {a0: s0.a, a1: s1.a, r: r0.map((x, j) => m(x, r1[j])), c: [m(c0[0], c1[0]), m(c0[1], c1[1])]}; });
// support distance of a section profile along the facet normal at theta (deg), centre offset included
const supp = (s, th) => { const c = Math.cos(th * Math.PI / 180), si = Math.sin(th * Math.PI / 180), a = c >= 0 ? s.r[0] : s.r[2], b = si >= 0 ? s.r[1] : s.r[3];
  return Math.hypot(a * c, b * si) + c * s.c[0] + si * s.c[1]; };
const inside = (s, t, n) => { for (let k = 0; k < n; k++) if (supp(s, k * 360 / n) > supp(t, k * 360 / n) + 1e-4) return false; return true; };
// A closed solid: the loft facets (no ledge rings, no 16-quad caps) + disc ledges at every step (only the visible
// side of a step: a section's disc faces away from it, skipped where the section is inside its neighbour) + end discs.
// skipSec(i): sections left out (their steps then get no discs either; the caller closes them).
function solid(axis, st, {n = 16, tex, discTex, seed = 0, caps = '-+', skip = null, skipSec = null}) {
  const els = loft(axis, st, {n, tex, seed, ledges: false, caps: '', skip: (k, th, i) => (skipSec && skipSec(i)) || (skip && skip(k, th, i))});
  const S = sections(st), dir = Math.sign(st[st.length - 1].a - st[0].a), sideOf = s => (s > 0 ? '+' : '-');
  for (let i = 0; i < S.length - 1; i++) {
    if (skipSec && (skipSec(i) || skipSec(i + 1))) continue;
    const a = S[i].a1;
    if (!inside(S[i], S[i + 1], n)) els.push(...disc(axis, a, S[i].r, S[i].c, discTex, sideOf(dir), n));
    if (!inside(S[i + 1], S[i], n)) els.push(...disc(axis, a, S[i + 1].r, S[i + 1].c, discTex, sideOf(-dir), n));
  }
  if (caps.includes('-')) els.push(...disc(axis, S[0].a0, S[0].r, S[0].c, discTex, sideOf(-dir), n));
  if (caps.includes('+')) { const s = S[S.length - 1]; els.push(...disc(axis, s.a1, s.r, s.c, discTex, sideOf(dir), n)); }
  return els;
}
// Light-corrected solids (the haunch, the upper arm): the big rounded masses. A stack of loft prisms shows terraces
// because the game lights every facet and ledge by its own normal (item displays: two world-fixed lights, ambient 0.4;
// a ledge facing up gets 1.0, a side about 0.62 averaged over the yaw, a down face 0.4): the R1 "stacked drums". These
// sprites carry a correction instead: albedo x F(n of the smooth surface through the stations) / F(n of the face), so
// a ledge is darkened and an upper facet brightened to the light the rounded mass would get. One wrap sprite (u =
// azimuth, continuous across facets; v = along the solid) and one small polar sprite per disc. F(ny) is the game light
// averaged over the yaw.
const FL = ny => (ny >= 0 ? .62 + .38 * ny : .62 + .22 * ny);
const LIGHT = (nySmooth, nyFace) => clamp(FL(nySmooth) / FL(nyFace), .55, 1.6);
function baked(name, st, {axis = 'y', n = 16, W = 128, H = 64, seed = 1, per = 9}) {
  const {A: AX, e1, e2} = FRAME[axis];
  const S = sections(st), A = st.map(x => x.a), aMax = Math.max(...A), aMin = Math.min(...A);
  const lerp = (x, y, f) => x + (y - x) * f;
  const prof = a => {
    a = Math.max(aMin, Math.min(aMax, a));
    for (let i = 0; i < st.length - 1; i++) {
      const s0 = st[i], s1 = st[i + 1], lo = Math.min(s0.a, s1.a), hi = Math.max(s0.a, s1.a);
      if (a >= lo - 1e-9 && a <= hi + 1e-9) { const f = (a - s0.a) / (s1.a - s0.a), r0 = R4(s0.r), r1 = R4(s1.r), c0 = s0.c || [0, 0], c1 = s1.c || [0, 0];
        return {r: r0.map((x, j) => lerp(x, r1[j], f)), c: [lerp(c0[0], c1[0], f), lerp(c0[1], c1[1], f)]}; }
    }
    return S[0];
  };
  // the smooth surface's normal at azimuth th (deg, from e1 toward e2) and axial position a: {ny (up), nf (front)}
  const normal = (th, a) => { const d = .14, dh = (supp(prof(a + d), th) - supp(prof(a - d), th)) / (2 * d), c = Math.cos(th * Math.PI / 180), si = Math.sin(th * Math.PI / 180);
    const nv = [0, 1, 2].map(i => c * e1[i] + si * e2[i] - dh * AX[i]), L = Math.hypot(...nv); return {ny: nv[1] / L, nf: -nv[2] / L}; };
  const aOf = v => (axis === 'y' ? aMax - v * (aMax - aMin) : aMin + v * (aMax - aMin));   // the loft's wrap v (azhdaha_shape loft)
  const dir = Math.sign(st[st.length - 1].a - st[0].a), sideOf = x => (x > 0 ? '+' : '-');
  const discs = [];
  for (let i = 0; i < S.length - 1; i++) {
    if (!inside(S[i], S[i + 1], n)) discs.push({a: S[i].a1, sec: S[i], side: sideOf(dir)});
    if (!inside(S[i + 1], S[i], n)) discs.push({a: S[i].a1, sec: S[i + 1], side: sideOf(-dir)});
  }
  discs.push({a: S[0].a0, sec: S[0], side: sideOf(-dir), cap: -dir}, {a: S[S.length - 1].a1, sec: S[S.length - 1], side: sideOf(dir), cap: dir});
  discs.forEach((d, i) => { d.sprite = `${name}_d${i}`; });
  registerWrap(name);
  const albedo = (x, y) => hidePx(x, y, {per, cell: W / per, seed});
  return {
    name, W, H,
    els: () => [...loft(axis, st, {n, tex: name, ledges: false, caps: '', seed}), ...discs.flatMap(d => disc(axis, d.a, d.sec.r, d.sec.c, d.sprite, d.side, n))],
    sprites: () => {
      // a facet's own normal is its azimuth k (flat), the smooth one turns continuously across it
      const out = {[name]: [W, H, (u, v) => { const k = Math.floor(u * n) % n, thk = k * 360 / n, th = (u * n - .5) * 360 / n, nn = normal(th, aOf(v));
        const nyFace = Math.cos(thk * Math.PI / 180) * e1[1] + Math.sin(thk * Math.PI / 180) * e2[1]; return scale(albedo(u * W, v * H), LIGHT(nn.ny, nyFace)); }, false]};
      for (const d of discs) {
        const k = 1 / Math.cos(Math.PI / n), R = d.sec.r.map(x => x * k);
        out[d.sprite] = [32, 32, (u, v) => {
          if (ngonEdge(u, v, n) < 0) return TRANSPARENT;
          const p = 2 * u - 1, q = 1 - 2 * v, x = p * (p >= 0 ? R[0] : R[2]), y = q * (q >= 0 ? R[1] : R[3]);
          const th = Math.atan2(y, x) * 180 / Math.PI, side = normal(th, d.a);
          const capN = d.cap ? d.cap * AX[1] : 0, rho = Math.min(1, Math.hypot(p, q));
          const ny = d.cap ? lerp(capN, side.ny, rho * rho) : side.ny, nyFace = (d.side === '+' ? 1 : -1) * AX[1];
          return scale(albedo(64 + x * 24, 64 + y * 24), LIGHT(ny, nyFace));
        }, false];
      }
      return out;
    },
  };
}
// zero-thickness facet elements made two-sided (the crown staves are seen from inside over the upper arm)
const OPP = {north: 'south', south: 'north', east: 'west', west: 'east', up: 'down', down: 'up'};
const twoSided = els => els.map(e => ({...e, faces: {...e.faces, ...Object.fromEntries(Object.entries(e.faces).map(([f, v]) => [OPP[f], {...v}]))}}));

// ---- talons ---------------------------------------------------------------------------------------------------------------
// A talon: side profile = a quadratic Bezier from the root (0, 0) over ctrl to the tip, in (z, y) blocks; w0 = width at
// the root. Geometry: two crossed cut-out cards through the claw axis: the side card (the hooked outline, dark with a pale
// tip, the upper edge lit) and a card tilted 45 degrees along the root -> tip chord (the tapering kite seen from the
// front and from above, a lit and a shaded half either side of the ridge: the conical claw of the footage), over a thin
// core box on the chord.
const CLAWS = {
  big: {ctrl: [-.21, -.02], tip: [-.44, -.42], w0: .46},      // the 4 fore talons, the 3 big hind ones
  small: {ctrl: [-.11, -.02], tip: [-.22, -.26], w0: .26},    // the fore dew claw, the small inner hind claw
};
for (const c of Object.values(CLAWS)) {
  c.pts = bez([0, 0], c.ctrl, c.tip, 20);
  c.core = t => (c.w0 / 2) * (1 - .8 * t);
  c.hs = t => c.core(t) + .02;
  c.S = stroke(c.pts, c.hs);
  const zs = c.pts.map(p => p[0]), ys = c.pts.map(p => p[1]), m = c.w0 / 2 + .04;
  c.rect = {z0: Math.min(...zs) - .04, z1: Math.max(...zs) + m, y0: Math.min(...ys) - .03, y1: Math.max(...ys) + m};
  c.at = t => { const i = Math.min(19, Math.floor(t * 20)), f = t * 20 - i, a = c.pts[i], b = c.pts[i + 1]; return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f]; };
  c.L = Math.hypot(c.tip[0], c.tip[1]) + .06;                  // the tilted card's length along the chord (root a little inside the toe)
}
function claw(kind, [x, y, z], look) {
  const c = CLAWS[kind], s = sfx(look), r = c.rect, els = [];
  els.push(cardX(`claw_${kind}${s}`, x, {Z0: z + r.z0, Z1: z + r.z1, Y0: y + r.y0, Y1: y + r.y1}));
  // the chord card: unrotated it stands in the plane z = zc (root up, tip down); turned +45 about X it lies along the chord
  const zc = z + c.tip[0] / 2, yc = y + c.tip[1] / 2, P = [x, yc, zc];
  els.push(cardZ(`clawk_${kind}${s}`, zc, {X0: x - c.w0 / 2 - .02, X1: x + c.w0 / 2 + .02, Y0: yc - c.L / 2, Y1: yc + c.L / 2}, {rot: ['x', 45, P]}));
  const e = .22 * c.w0;
  els.push(rockBox([x - e, yc - c.L * .1, zc - e], [x + e, yc + c.L * .42, zc + e], 'claw' + s, {rot: ['x', 45, P], seed: x * 7 + z}));
  return els;
}

// ---- fore leg -----------------------------------------------------------------------------------------------------------------
// Upper arm (rest-aligned, origin at the shoulder): the muscle mass bulges out above the bracer and sinks into its crown.
// Stations: a = height below the shoulder, r = [outer +X, front -Z, inner -X, back +Z], c = [x, forward].
const UARM = [{a: .32, r: [.42, .46, .4, .46], c: [.1, .02]}, {a: .06, r: [.76, .78, .64, .76], c: [.2, .05]}, {a: -.3, r: [.92, .9, .74, .88], c: [.34, .07]},
  {a: -.75, r: [.93, .86, .74, .84], c: [.48, .1]}, {a: -1.15, r: [.76, .74, .68, .74], c: [.64, .13]}, {a: -1.5, r: [.6, .6, .56, .6], c: [.7, .15]}];
const UARM_B = baked('uarm_hide', UARM, {seed: 61, W: 128, H: 48});
const uarm = () => UARM_B.els();
// Bracer (bone-aligned, origin at the elbow, the column down to the wrist at -ARM[1]): a regular octagon (8 staves),
// the body r .78 from the elbow down, a flared foot rim r .86; above, the crown band of ragged pointed stave tips
// (cut-out wrap sprite, two-sided). The 8-sided wrap sprite carries the carved lines and the gold studs.
const BR_TOP = .08, BR_BOT = -ARM[1] - .24, BR_FLARE = -ARM[1] + .32, BR_TEETH = .13;
const BRACER = [{a: BR_TOP, r: .78}, {a: BR_FLARE + .3, r: .78}, {a: BR_FLARE - .05, r: .85}, {a: BR_BOT, r: .9}];
const CROWN = {top: .46, bot: .04, r: .83};
function bracer(look) {
  const s = sfx(look);
  // the foot rim is serrated (cut-out points over the claws, v2 f0600 / v4 f1680): the bottom lid sits above the points
  const els = solid('y', BRACER, {n: 8, tex: 'bracer' + s, discTex: 'disc8_pawstone' + s, seed: 71, caps: ''});
  els.push(...disc('y', BR_BOT + BR_TEETH, .9 * .97, [0, 0], 'disc8_pawstone' + s, '-', 8));
  els.push(...twoSided(loft('y', [{a: CROWN.top, r: CROWN.r}, {a: CROWN.bot, r: CROWN.r}], {n: 8, tex: 'crown' + s, ledges: false, seed: 73})));
  els.push(...disc('y', BR_TOP - .015, CROWN.r, [0, 0], 'disc8_pawstone' + s, '+-', 8));
  els.push(...elbowCrystals());
  return els;
}
// Amber hexagonal prisms: two crossed cut-out cards (the side profile and the face-on card) round a core box, all
// leaning back (+Z) by `lean` degrees (45: the elbow crystals, painted side card; 22.5: the near-upright heel spur).
// (Element rotation +deg about X tips the top toward +Z, the back; R1 tilted the face card and box forward by mistake.)
function prism([x, y, z], L, w, lean = 45) {
  const els = [], P = [x, y, z];
  if (lean === 45) els.push(cardX('crystal_lean', x, {Z0: z - .15 * L, Z1: z + .85 * L, Y0: y, Y1: y + .85 * L}));
  else els.push(cardX('crystal_up', x, {Z0: z - w / 2, Z1: z + w / 2, Y0: y, Y1: y + L}, {rot: ['x', lean, P]}));
  els.push(cardZ('crystal_up', z, {X0: x - w / 2, X1: x + w / 2, Y0: y, Y1: y + L}, {rot: ['x', lean, P]}));
  els.push(rockBox([x - w * .3, y, z - w * .3], [x + w * .3, y + L * .8, z + w * .3], 'crystal', {rot: ['x', lean, P]}));
  return els;
}
const elbowCrystals = () => [...prism([.3, .05, .62], 1.0, .3), ...prism([-.12, .12, .66], .88, .28), ...prism([.62, -.25, .42], .78, .26), ...prism([.08, -.32, .74], .66, .24)];
// Paw (origin at the wrist, sole at -0.5): the pale knuckle pad under the bracer rim, 4 toes (octagonal knuckles) with
// the 4 talons, the dew claw high on the inner side.
const PAW = [{a: .44, r: [.48, .08, .48, .28], c: [0, -.2]}, {a: .16, r: [.76, .24, .76, .3], c: [0, -.2]}, {a: -.55, r: [.92, .26, .92, .3], c: [0, -.2]}];
const TOES = [.62, .21, -.21, -.62];
function paw(look) {
  const s = sfx(look);
  const els = solid('z', PAW, {tex: 'toestone' + s, discTex: 'disc16_toestone' + s, seed: 81});
  TOES.forEach((x, i) => {
    const front = [-.72, -.79, -.76, -.7][i];
    els.push(...solid('z', [{a: -.3, r: [.21, .18, .21, .18], c: [x, -.31]}, {a: front, r: [.21, .18, .21, .18], c: [x, -.31]}], {n: 8, tex: 'toestone' + s, discTex: 'disc8_toestone' + s, seed: 83 + i, caps: '+'}));
    els.push(...claw('big', [x, -.08, front + .06], look));
  });
  els.push(...claw('small', [-.88, -.06, -.28], look));
  return els;
}

// ---- hind leg -----------------------------------------------------------------------------------------------------------------
// Haunch (rest-aligned, origin at the hip): a big rounded mass lofted ACROSS the body (x, from inside the pelvis out to the
// lateral bulge), so its side outline is the smooth 16-gon; it hides the knee and the shin, and its underside sits on the
// gaiter collar (the hock is hip-relative (0.5, -1.5, 0.45)). Stations: a = x, r = [front, up, back, down], c = [fwd, up].
// The lateral bulge sits low (centre ~2.3 b up) so its top runs into the flank instead of standing out as a wheel.
const THIGH = [{a: -.55, r: [.9, .9, .9, .8], c: [-.05, -.5]}, {a: .15, r: [1.12, 1.1, 1.08, .95], c: [-.05, -.55]}, {a: .55, r: [1.1, .97, 1.06, .96], c: [-.05, -.61]},
  {a: .82, r: [1.0, .8, .97, .9], c: [-.05, -.68]}, {a: 1.03, r: [.86, .64, .84, .8], c: [-.05, -.74]}, {a: 1.2, r: [.66, .5, .64, .62], c: [-.05, -.79]},
  {a: 1.32, r: [.44, .34, .43, .42], c: [-.05, -.82]}, {a: 1.39, r: [.22, .18, .22, .2], c: [-.05, -.83]}];
const THIGH_B = baked('thigh_hide', THIGH, {axis: 'x', seed: 91, W: 128, H: 48});
const thigh = () => THIGH_B.els();
// Shin (bone-aligned, origin at the knee, down to the hock at -LEG[1]): an octagonal hide limb.
const shin = () => solid('y', [{a: .3, r: .42}, {a: -.55, r: .42}, {a: -.62, r: .36}, {a: -LEG[1] - .1, r: .34}], {n: 8, tex: 'hide', discTex: 'disc8_hide', seed: 101});
// Foot (origin at the hock, 1.5 b up; sole at -1.5): the gaiter column. Collar a +.22 .. -.3 (dark carved stone, the
// spur and two gold knobs at the back), core r .6 (the dark grooves), 4 rings, the plinth, 3 toes + 1.
const RING = {top: -.32, h: .17, gap: .055, n: 4, r0: .675, dr: .016};
RING.bot = RING.top - RING.n * RING.h - (RING.n - 1) * RING.gap;
const RING_ST = (() => { const out = []; for (let k = 0; k < RING.n; k++) { const a = RING.top - k * (RING.h + RING.gap), r = RING.r0 + RING.dr * k; out.push({a, r}, {a: a - RING.h, r}); } return out; })();
const ringSec = i => i % 2 === 1;   // the odd sections of RING_ST are the grooves (the core shows there)
const COLLAR = [{a: .24, r: [.76, .7, .72, .84]}, {a: -.3, r: [.76, .7, .72, .84]}];
const PLINTH = [{a: RING.bot + .03, r: [.8, .74, .76, .7], c: [0, .02]}, {a: -1.47, r: [.82, .78, .78, .72], c: [0, .04]}];
const HTOES = [[.47, -.84], [0, -.9], [-.47, -.84]];
function foot(look) {
  const s = sfx(look), els = [];
  els.push(...solid('y', COLLAR, {tex: 'collar' + s, discTex: 'disc16_pawstone' + s, seed: 105}));
  els.push(...prism([0, .06, .66], .95, .32, 22.5));
  for (const x of [-.3, .3]) els.push(rockBox([x - .07, -.14, .8], [x + .07, 0, .9], 'gold', {seed: 7 + x}));
  els.push(...loft('y', [{a: .16, r: .62}, {a: RING.bot - .02, r: .62}], {tex: 'gcore' + s, ledges: false, seed: 107}));
  // the rings: one loft over all ring stations (the wrap sprite runs down the whole column), grooves left out; each ring
  // gets an up disc (seen from above) and a down disc (seen when the foot is lifted), except where collar / plinth cover
  els.push(...loft('y', RING_ST, {tex: 'gaiter' + s, ledges: false, seed: 109, skip: (k, th, i) => ringSec(i)}));
  for (let k = 0; k < RING.n; k++) {
    const a = RING.top - k * (RING.h + RING.gap), r = RING.r0 + RING.dr * k;
    if (k > 0) els.push(...disc('y', a, r, [0, 0], 'disc16_toestone' + s, '+'));
    if (k < RING.n - 1) els.push(...disc('y', a - RING.h, r, [0, 0], 'disc16_toestone' + s, '-'));
  }
  els.push(...solid('y', PLINTH, {tex: 'plinth' + s, discTex: 'disc16_toestone' + s, seed: 111}));
  HTOES.forEach(([x, front], i) => {
    els.push(...solid('z', [{a: -.25, r: [.21, .2, .21, .2], c: [x, -1.28]}, {a: front, r: [.21, .2, .21, .2], c: [x, -1.28]}], {n: 8, tex: 'toestone' + s, discTex: 'disc8_toestone' + s, seed: 113 + i, caps: '+'}));
    els.push(...claw('big', [x, -1.08, front + .06], look));
  });
  els.push(...solid('z', [{a: -.1, r: [.15, .14, .15, .14], c: [-.76, -1.34]}, {a: -.5, r: [.15, .14, .15, .14], c: [-.76, -1.34]}], {n: 8, tex: 'toestone' + s, discTex: 'disc8_toestone' + s, seed: 117, caps: '+'}));
  els.push(...claw('small', [-.76, -1.22, -.46], look));
  return els;
}

// ---- glow overlays (tinted white line masks 0.025 b proud, front and sides only) -------------------------------------------
const glowBracer = () => loft('y', BRACER, {n: 8, tex: 'bracer_mask', grow: .025, ledges: false, tint: true, skip: k => k >= 5});
const glowGaiter = () => loft('y', RING_ST, {tex: 'gaiter_mask', grow: .025, ledges: false, tint: true, skip: (k, th, i) => ringSec(i) || (k >= 10 && k <= 14)});

// ---- region exports -------------------------------------------------------------------------------------------------------------
const U = (part, els) => toUnits(els, PART_SCALE[part]);
export function models() {
  const M = {};
  const pair = (name, els) => { M[name + '_l'] = U(name + '_l', els); M[name + '_r'] = U(name + '_r', mirrorX(els)); };
  pair('uarm', uarm()); pair('thigh', thigh()); pair('gaiter', shin());
  for (const look of ALL) {
    const s = sfx(look);
    for (const [n, f] of [['bracer', bracer], ['paw', paw], ['foot', foot]]) {
      const els = f(look);
      M[n + '_l' + s] = U(n + '_l', els); M[n + '_r' + s] = U(n + '_r', mirrorX(els));
    }
  }
  pair('glow_bracer', glowBracer()); pair('glow_gaiter', glowGaiter());
  return M;
}
const legLook = p => ({geo: p, hydro: p + '_hydro', pyro: p + '_pyro'});
export const LOOKS = {
  legs: Object.fromEntries([...['bracer', 'paw', 'foot'].flatMap(n => [n + '_l', n + '_r']).map(p => [p, legLook(p)]),
    ...['glow_bracer_l', 'glow_bracer_r', 'glow_gaiter_l', 'glow_gaiter_r'].map(p => [p, {geo: 'empty', hydro: p + '_hydro', pyro: p + '_pyro'}])]),
};
export const TINTED = Object.fromEntries(['glow_bracer_l', 'glow_bracer_r', 'glow_gaiter_l', 'glow_gaiter_r'].flatMap(p => LOOKS_EL.map(l => [p + '_' + l, [p, LOOK_PAL[l].tint]])));
export const LOOK_BRIGHT = {legs: {hydro: {}, pyro: {}}};

// ---- palette -------------------------------------------------------------------------------------------------------------------
// The leg stone per look: Geo red-brown bracer stone; Hydro navy-black (model.md §4.2); Pyro a deep red-brown (the
// footage reads darker and browner than the LOOK_PAL ramp; the glow is carried by the lines, r1_critique §4.5).
const PYRO_STONE = ramp(['#9C3A2A', '#7A2A1F', '#5C1F17', '#42150F', '#2A0D09']);
const STONE = {null: PAL.bracer, hydro: LOOK_PAL.hydro.stone, pyro: PYRO_STONE};
const STONE_T = {null: .42, hydro: .62, pyro: .5};
// pale knuckle / gaiter stone per look (Geo grey-cream gaiter ramp; Hydro and Pyro the element stone, a step lighter)
const PALE = {null: PAL.gaiter, hydro: ramp(['#6E809C', '#566982', '#3F5472', '#302F4B', '#202036']), pyro: ramp(['#B04A36', '#8E3626', '#6E281D', '#501C14', '#34110C'])};
const PALE_T = {null: .32, hydro: .45, pyro: .5};
const TALON = {null: PAL.talon, hydro: ramp(['#5A6478', '#3A4258', '#262C40', '#181C2A', '#0E1018']), pyro: ramp(['#6E342A', '#4E221B', '#361713', '#240F0C', '#160A08'])};
const TIP = {null: ramp(['#C9BFAE', '#A89E8C', '#7E7466', '#554C43']), hydro: ramp(['#B8C8E0', '#8A9AB8', '#5A6478', '#3A4258']), pyro: ramp(['#D8A27A', '#A8705A', '#6E342A', '#4E221B'])};

// ---- sprites ----------------------------------------------------------------------------------------------------------------------
// Wrap sprites: u = azimuth / 360 from the outer side (+X) through the front (u .25), the inner side (u .5) and the back
// (u .75); v from the top of the loft down. Carved lines are dark grooves with a lit lower lip (Geo) or the element glow.
const glowOf = look => (look ? LOOK_PAL[look].glow : null);
// bracer body (a BR_TOP .. BR_BOT): x / y in blocks round the octagon / down the column
const BR_H = BR_TOP - BR_BOT, BR_C = 8 * 2 * .78 * Math.tan(Math.PI / 8);
function bracerLine(u, v) {
  const x = u * BR_C, y = v * BR_H;
  let d = Math.min(Math.abs(y - .22), Math.abs(y - (BR_H - .5)));                     // rim lines (top, above the flare)
  const zz = .78 + .14 * (Math.abs(((x * 1.6) % 1 + 1) % 1 - .5) * 4 - 1);              // zigzag band round the column
  d = Math.min(d, Math.abs(y - zz), Math.abs(y - (zz + .5)));
  const fx = x - BR_C / 4, fy = y - 1.32, dia = Math.abs(fx) * 1.1 + Math.abs(fy);      // the diamond glyph on the front
  d = Math.min(d, Math.abs(dia - .4), Math.abs(dia - .2));
  for (const cx of [0, BR_C / 2, BR_C]) {                                              // square meander hooks outside / inside
    const hx = x - cx, hy = y - 1.38, sq = Math.max(Math.abs(hx), Math.abs(hy));
    if (sq < .3) d = Math.min(d, Math.abs(sq - .26), Math.abs(sq - .13) + (hx > 0 && hy < 0 ? 1 : 0));
  }
  // the lower band: a row of chevrons over the paw (v4 f1680)
  const cy = BR_H - .3, ch = Math.abs(((x * 2.2) % 1 + 1) % 1 - .5) * .32;
  d = Math.min(d, Math.abs(y - (cy - .08 + ch)));
  return d;
}
const STUDS = [[BR_C / 4 - .42, .13], [BR_C / 4, .11], [BR_C / 4 + .42, .13], [BR_C / 4 - .9, .16], [BR_C / 4 + .9, .16]];
function bracerPaint(look) {
  const R = STONE[look], G = glowOf(look), t0 = STONE_T[look];
  return (s, t) => {
    const x = s * BR_C, y = t * BR_H, f = (s * 8) % 1;
    const tooth = BR_H - BR_TEETH * (1 - Math.abs(((s * 16) % 1) - .5) * 2);      // the serrated foot: points between the claws
    if (y > tooth + .002) return TRANSPARENT;
    let c = R(t0 + .18 * (N.a(x * 4, y * 4) - .5) + .1 * (N.c(x * 14, y * 14) - .5));
    if (tooth - y < .025) c = sink(c, .35);
    c = mix(c, R(.08), .22 * smooth(.3, 0, Math.abs(f - .35)));                     // each stave lit left of its middle
    if (f < .035 || f > .965) c = sink(c, .5);                                         // the joints between the staves
    else if (f < .07) c = lift(c, .1);
    c = sink(c, .25 * smooth(.6, 1, t));                                               // darker toward the foot
    if (y < .06) c = lift(c, .22);                                                     // the lit top rim
    const d = bracerLine(s, t);
    if (d < .03) c = G ? G(.08 + d * 10) : mix(sink(c, .55), PAL.bracer(.95), .4);
    else if (d < .055) c = G ? mix(c, G(.6), .5 * (1 - (d - .03) / .025)) : lift(c, .2 * (1 - (d - .03) / .025));
    if (Math.abs(N.e(x * 2.2, y * 1.6) - .5) < .01) c = G ? mix(c, G(.4), .5) : sink(c, .45);   // cracks
    for (const [sx, sy] of STUDS) {                                                    // flush gold studs (painted)
      const r = Math.hypot(x - sx, (y - sy) * 1.1);
      if (r < .075) c = PAL.gold(clamp(.25 + r * 6 - (x - sx + sy - y) * 4));
      else if (r < .095) c = sink(c, .5);
    }
    return c;
  };
}
// crown: 8 stave tips above the body, cut out to ragged points (height .42 b round the octagon)
const CR_H = CROWN.top - CROWN.bot;
function crownTop(s) {
  const k = Math.floor(s * 8) % 8, f = (s * 8) % 1, peak = .3 + .4 * hash(k, 3), H = .22 + .2 * hash(k, 7);
  const tooth = H * Math.max(0, 1 - Math.abs(f - peak) / (.42 + .1 * hash(k, 11)));
  const notch = .04 * Math.sin(f * 17 + k);
  return .1 + tooth + notch;                                                           // height above the crown bottom
}
function crownPaint(look) {
  const R = STONE[look], G = glowOf(look), t0 = STONE_T[look];
  return (s, t) => {
    const y = (1 - t) * CR_H, top = crownTop(s), f = (s * 8) % 1;
    if (y > top) return TRANSPARENT;
    let c = R(t0 - .04 + .16 * (N.a(s * 30, y * 8) - .5));
    c = mix(c, R(.08), .2 * smooth(.3, 0, Math.abs(f - .35)));
    if (top - y < .035) c = lift(c, .35);                                               // lit broken edge
    if (f < .035 || f > .965) c = sink(c, .5);
    if (G && Math.abs(y - .12) < .018) c = G(.2);
    return c;
  };
}
const linesMask = (lineFn, w = .03) => (s, t) => { const d = lineFn(s, t); return d < w ? [255, 255, 255, 255] : d < 2 * w ? [255, 255, 255, Math.round(255 * (1 - (d - w) / w))] : TRANSPARENT; };
// gaiter rings: v over the ring loft (RING.top .. RING.bot); per ring a local r 0 (top) .. 1 (bottom)
const RSPAN = RING.top - RING.bot;
const ringAt = v => { const a = RING.top - v * RSPAN, k = Math.max(0, Math.min(RING.n - 1, Math.floor((RING.top - a) / (RING.h + RING.gap)))); return {k, r: (RING.top - k * (RING.h + RING.gap) - a) / RING.h}; };
function gaiterLine(u, v) {
  const {k, r} = ringAt(v), x = u * 2 * Math.PI * .7;
  if (r < .14 || r > .86) return 9;
  const yy = (r - .5) * RING.h, zz = .06 * (Math.abs(((x * 1.3 + k * .5) % 1 + 1) % 1 - .5) * 4 - 1);
  let d = Math.abs(yy - zz);
  if (k % 2 && Math.abs(((x * .8 + k * .3) % 1 + 1) % 1 - .5) < .16) d = Math.min(d, Math.abs(Math.abs(yy) - .045));
  return d / 1.6;
}
function gaiterPaint(look) {
  const R = PALE[look], G = glowOf(look), t0 = PALE_T[look];
  return (s, t) => {
    const {k, r} = ringAt(t), x = s * 4.4, y = t * RSPAN;
    let c = R(t0 + .12 * (N.b(x * 5, y * 9) - .5) + .06 * (N.d(x * 20, y * 20) - .5) + .03 * k);
    c = lift(c, .3 * smooth(.25, 0, r));                                                  // lit upper edge of the ring
    c = sink(c, .4 * smooth(.6, 1.05, r));                                                // its shaded underside
    c = mix(c, R(.9), .25 * Math.max(0, Math.cos((s - .78) * Math.PI * 2)) * .6);         // the back (toward the tail) duller
    const d = gaiterLine(s, t);
    if (d < .009) c = G ? G(.1 + d * 40) : mix(c, PAL.bracer(.75), .8);
    else if (d < .018) c = G ? mix(c, G(.6), .45) : lift(c, .15);
    if (Math.abs(N.f(x * 3, y * 6) - .5) < .01) c = sink(c, .35);
    return c;
  };
}
// plinth (the carved foot block under the rings, a RING.bot .. -1.47): a meander band, a spiral glyph on the heel
const PL_H = RING.bot + .03 + 1.47;
function plinthLine(u, v) {
  const x = u * 4.6, y = v * PL_H;
  let d = Math.abs(y - .08);
  const mq = ((x * 3) % 1 + 1) % 1, my = y - .2;
  if (my > -.06 && my < .06) d = Math.min(d, Math.abs(mq - .5) < .32 ? Math.abs(Math.abs(my) - .05) : Math.abs(mq - .5) - .3);
  const hx = (u - .75) * 4.6, hy = y - .26, rr = Math.hypot(hx, hy * 1.4), an = Math.atan2(hy, hx);
  if (rr < .36) d = Math.min(d, Math.abs(((rr - an * .04) % .1 + .1) % .1 - .05));
  return d;
}
function plinthPaint(look) {
  const R = PALE[look], G = glowOf(look), t0 = PALE_T[look];
  return (s, t) => {
    const x = s * 4.6, y = t * PL_H;
    let c = R(t0 + .04 + .12 * (N.b(x * 5, y * 5) - .5));
    c = lift(c, .2 * smooth(.08, 0, y));
    c = sink(c, .3 * smooth(.6, 1, t));
    const d = plinthLine(s, t);
    if (d < .014) c = G ? G(.15 + d * 20) : mix(c, PAL.bracer(.75), .75);
    return c;
  };
}
// collar (the dark cuff round the hock, a +.24 .. -.3): carved stone, a lit top rim, the lower edge broken into tongues
const CO_H = .54;
function collarPaint(look) {
  const R = STONE[look], G = glowOf(look), t0 = STONE_T[look] + .05;
  return (s, t) => {
    const y = (1 - t) * CO_H, k = Math.floor(s * 16), f = (s * 16) % 1;
    const edge = .06 + .1 * hash(k, 5) + .07 * Math.abs(Math.sin((f + hash(k, 9)) * Math.PI));
    if (y < edge) return TRANSPARENT;
    let c = R(t0 + .16 * (N.a(s * 20, y * 9) - .5) + .08 * (N.c(s * 60, y * 30) - .5));
    if (y - edge < .03) c = sink(c, .35);
    if (y > CO_H - .05) c = lift(c, .25);
    const ln = Math.abs(y - (.36 + .03 * Math.sin(s * Math.PI * 12)));
    if (ln < .012) c = G ? G(.2) : sink(c, .45);
    else if (ln < .022 && !G) c = lift(c, .12);
    return c;
  };
}
// painters: dark carved stone (the collar / bracer discs), pale knuckle stone (toes, pads; a tile), dark groove stone (the
// gaiter core; a tile)
function pawstone(look) {
  const R = STONE[look], G = glowOf(look), t0 = STONE_T[look] + .12;
  return (s, t) => { let c = R(t0 + .2 * (N.d(s * 6, t * 6) - .5)); const cr = Math.abs(N.f(s * 2.5, t * 2.5) - .5); if (cr < .02) c = G ? G(.3) : sink(c, .4); return c; };
}
function toestone(look) {
  const R = PALE[look], G = glowOf(look), t0 = PALE_T[look] + .05;
  return (s, t) => {
    let c = R(t0 + .14 * (N.d(s * 5, t * 5) - .5) + .06 * (N.a(s * 18, t * 18) - .5));
    const cr = Math.abs(N.c(s * 2.2, t * 2.2) - .5);
    if (cr < .015) c = G ? G(.25) : sink(c, .3);
    return c;
  };
}
const gcore = look => (s, t) => sink(PALE[look](PALE_T[look] + .25 + .12 * (N.e(s * 6, t * 6) - .5)), .25);
// cut-out discs: the material inside the regular n-gon (flats facing the axes), the rim slightly darker
const ngonEdge = (s, t, n) => { const x = (s - .5) * 2, y = (t - .5) * 2; let m = -9; for (let i = 0; i < n; i++) { const th = i * 2 * Math.PI / n; m = Math.max(m, x * Math.cos(th) + y * Math.sin(th)); } return Math.cos(Math.PI / n) - m; };
const discPaint = (n, base) => (s, t) => { const e = ngonEdge(s, t, n); if (e < 0) return TRANSPARENT; const c = base(s, t); return e < .1 ? sink(c, .22 * (1 - e / .1)) : c; };
// talon side cards: the hooked outline, root dark, pale tip, the upper face lit, a dark edge line
function clawCard(kind, look) {
  const c = CLAWS[kind], r = c.rect, R = TALON[look], T = TIP[look];
  return (s, t) => {
    const z = r.z0 + s * (r.z1 - r.z0), y = r.y1 - t * (r.y1 - r.y0), n = c.S.near(z, y);
    if (n.d > c.hs(n.t)) return TRANSPARENT;
    const w = n.d / c.hs(n.t);
    let col = R(.25 + .25 * n.t + .12 * (N.a(s * 6, t * 6) - .5));
    if (n.s > 0) col = lift(col, .14 * (1 - w));
    else col = sink(col, .2 * w);
    if (n.t > .7) col = mix(col, T(.2), smooth(.7, 1, n.t) * .85);
    if (w > .82) col = sink(col, .35);
    return col;
  };
}
// the chord card: root at the top (width w0), the point at the bottom; the left half lit, the right half shaded, a dark
// rim, the pale tip
function clawKite(kind, look) {
  const c = CLAWS[kind], R = TALON[look], T = TIP[look], W = c.w0 + .04;
  return (s, t) => {
    const x = (s - .5) * W, f = t, half = (c.w0 / 2) * Math.pow(Math.max(0, 1 - f * 1.03), .75) * (f < .08 ? .75 + f * 3.1 : 1);
    if (Math.abs(x) > half || f > .99) return TRANSPARENT;
    const w = Math.abs(x) / Math.max(half, 1e-3);
    let col = R(.28 + .22 * f + .1 * (N.c(s * 5, t * 7) - .5));
    col = x < 0 ? lift(col, .16 * (1 - w)) : sink(col, .18 * w);
    if (Math.abs(x) < .012) col = lift(col, .2);
    if (f > .62) col = mix(col, T(.2), smooth(.62, .98, f) * .85);
    if (w > .8) col = sink(col, .3);
    return col;
  };
}
function crystalCard(lean) {
  return (s, t) => {
    const y = 1 - t, x = lean ? s - .15 - .7 * y : s - .5;
    const w = .22 * (y < .78 ? 1 : (1 - y) / .22);
    if (Math.abs(x) > w || y < 0) return TRANSPARENT;
    let c = PAL.crystal(clamp(.9 - y * .95));
    if (x > 0) c = sink(c, .18);
    if (Math.abs(x) < w * .12) c = lift(c, .3);
    if (w - Math.abs(x) < .03) c = PAL.crystal(.95);
    return c;
  };
}
export function sprites() {
  const S = {};
  for (const look of ALL) {
    const s = sfx(look);
    S['bracer' + s] = [256, 112, bracerPaint(look), false];
    S['crown' + s] = [128, 32, crownPaint(look), false];
    S['gaiter' + s] = [256, 48, gaiterPaint(look), false];
    S['plinth' + s] = [256, 32, plinthPaint(look), false];
    S['collar' + s] = [128, 32, collarPaint(look), false];
    S['toestone' + s] = [64, 64, toestone(look), false];
    S['gcore' + s] = [32, 32, gcore(look), false];
    S['claw' + s] = [32, 32, (u, v) => TALON[look](.3 + .35 * v + .1 * (N.b(u * 6, v * 6) - .5)), false];
    for (const k of Object.keys(CLAWS)) { S[`claw_${k}${s}`] = [48, 32, clawCard(k, look), false]; S[`clawk_${k}${s}`] = [32, 48, clawKite(k, look), false]; }
    S['disc16_pawstone' + s] = [48, 48, discPaint(16, pawstone(look)), false];
    S['disc8_pawstone' + s] = [48, 48, discPaint(8, pawstone(look)), false];
    S['disc16_toestone' + s] = [48, 48, discPaint(16, toestone(look)), false];
    S['disc8_toestone' + s] = [32, 32, discPaint(8, toestone(look)), false];
  }
  Object.assign(S, UARM_B.sprites(), THIGH_B.sprites());
  S.disc8_hide = [32, 32, discPaint(8, TILES.hide[3]), false];
  S.bracer_mask = [256, 112, linesMask(bracerLine), true];
  S.gaiter_mask = [256, 48, linesMask(gaiterLine, .009), true];
  S.crystal_lean = [32, 64, crystalCard(true), false];
  S.crystal_up = [32, 64, crystalCard(false), false];
  S.crystal = [32, 32, (u, v) => PAL.crystal(.3 + .4 * v), false];
  return S;
}
