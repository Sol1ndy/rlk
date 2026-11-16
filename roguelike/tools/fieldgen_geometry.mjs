// Part models of the experimental field generator (실험성 역장 발생 장치) rig, used by build_mboss_fieldgen_rig.mjs.
//
// Authoring frame ("A-frame", the rig's frame): +X = the device's LEFT, +Y up, -Z forward (the keystone iris side);
// units are model units relative to the display pivot (model [8,8,8]); 16 units = the part's display scale in blocks
// (fieldgen_pose.mjs PART_SCALE). Paired parts are authored for the left (+X) side and mirrored for the right
// (mboss_model_lib.mjs mirrorModel).
//
// Construction (scratchpad mb3/understand/model.md §7): the device is a set of free bodies round one root. Round
// things are lathes of flat facets (16 by default) under per-facet tile textures (lathe tile option), with flat
// annulus segments (annulus, staggered against z-fighting) or one polar card for their faces; the light is baked into
// the textures per facet azimuth (fieldgen_paint.mjs LEVELS). Gold spearheads are stepped 8-facet cones with
// alternating facets; glows are translucent cards or turned shells. Constraints: coordinates within -16..32 (reach
// <= 24 units from the pivot), single-axis element rotations in 22.5 degree steps within +-45 (checkBounds / rotM).
import {abox, cardZ, cardX, cardY, faceEl, lathe, annulus, turned, stations, disc, mirrorModel, checkBounds, rotA, D2R, DK} from './mboss_model_lib.mjs';
import {LEVELS} from './fieldgen_paint.mjs';

export {checkBounds};
// ---- light levels baked per facet (the facets are unshaded) ----------------------------------------------------------
// The light comes from the front, upper right of the device (the upper left as the player sees it: the device turns
// to face the player). az = facet normal azimuth in degrees from the front (-Z) toward the device's left (+X).
const LIGHT_AZ = -40;
const level = az => { const c = Math.cos((az - LIGHT_AZ) * D2R); return c > .55 ? 'a' : c > 0 ? 'b' : c > -.55 ? 'c' : 'd'; };
const azOf = (k, n = 16) => k * 360 / n;
if (Object.keys(LEVELS).join() !== 'a,b,c,d') throw new Error('light levels');

// A box built in the frame of lathe facet k about Y (d = radial, t = tangential), then turned to its azimuth:
// rad [r0, r1], s [s0, s1] along the tangent, y [y0, y1].
function segBox(k, [r0, r1], [s0, s1], [y0, y1], tex, n = 16, axisC = [0, 0, 0]) {
  const phi = k * 360 / n, q = Math.round(phi / 90), g = phi - 90 * q;
  const dirs = [[0, 0, -1], [1, 0, 0], [0, 0, 1], [-1, 0, 0]], d = dirs[((q % 4) + 4) % 4], t = dirs[(((q + 1) % 4) + 4) % 4];
  const P = (r, s, y) => [axisC[0] + d[0] * r + t[0] * s, y, axisC[2] + d[2] * r + t[2] * s];
  const a = P(r0, s0, y0), b = P(r1, s1, y1);
  const sg = rotA('y', 10, d)[0] * t[0] + rotA('y', 10, d)[2] * t[2] > 0 ? 1 : -1;
  return abox(a, b, tex, {rot: g ? ['y', sg * g, [axisC[0], (y0 + y1) / 2, axisC[2]]] : undefined});
}
// The same for a lathe about Z (a vertical ring in the XY plane): facet k at azimuth from +Y toward +X.
function segBoxZ(k, [r0, r1], [s0, s1], [z0, z1], tex, c = [0, 0, 0], n = 16) {
  const phi = k * 360 / n, q = Math.round(phi / 90), g = phi - 90 * q;
  const dirs = [[0, 1, 0], [1, 0, 0], [0, -1, 0], [-1, 0, 0]], d = dirs[((q % 4) + 4) % 4], t = dirs[(((q + 1) % 4) + 4) % 4];
  const P = (r, s, z) => [c[0] + d[0] * r + t[0] * s, c[1] + d[1] * r + t[1] * s, z];
  const a = P(r0, s0, z0), b = P(r1, s1, z1);
  const rd = rotA('z', 10, d), sg = rd[0] * t[0] + rd[1] * t[1] > 0 ? 1 : -1;
  return abox(a, b, tex, {rot: g ? ['z', sg * g, [c[0], c[1], (z0 + z1) / 2]] : undefined});
}
// A square face in the frame of facet k about Y, centred at radius rad, height y, facing up or down (port discs).
function segSquare(k, rad, y, half, face, tex, n = 16) {
  const phi = k * 360 / n, q = Math.round(phi / 90), g = phi - 90 * q;
  const dirs = [[0, 0, -1], [1, 0, 0], [0, 0, 1], [-1, 0, 0]], d = dirs[((q % 4) + 4) % 4], t = dirs[(((q + 1) % 4) + 4) % 4];
  const P = (r, s) => [d[0] * r + t[0] * s, y, d[2] * r + t[2] * s];
  const a = P(rad - half, -half), b = P(rad + half, half);
  const lo = [Math.min(a[0], b[0]), y, Math.min(a[2], b[2])], hi = [Math.max(a[0], b[0]), y, Math.max(a[2], b[2])];
  const fn = ([X, , Z]) => [16 * (X - lo[0]) / (hi[0] - lo[0]), 16 * (Z - lo[2]) / (hi[2] - lo[2])];
  const sg = rotA('y', 10, d)[0] * t[0] + rotA('y', 10, d)[2] * t[2] > 0 ? 1 : -1;
  return faceEl([lo, hi], {[face]: {tex, fn}}, {shade: false, rot: g ? ['y', sg * g, [0, y, 0]] : undefined});
}
// Horizontal polar card (both faces) at height y, radius R, optional tilt about X (degrees, multiple of 22.5).
function polarCard(sprite, y, R, tilt = 0) {
  const fn = ([X, , Z]) => [16 * (X + R) / (2 * R), 16 * (Z + R) / (2 * R)];
  return faceEl([[-R, y, -R], [R, y, R]], {up: {tex: sprite, fn}, down: {tex: sprite, fn}}, {shade: false, rot: tilt ? ['x', tilt, [0, y, 0]] : undefined});
}
// Card in the plane Z = z centred on (cx, cy) with half size h (both sides), or crossed with a card in X = cx.
const squareZ = (sprite, cx, cy, h, z, opt) => cardZ(sprite, z, {X0: cx - h, X1: cx + h, Y0: cy - h, Y1: cy + h}, opt);

// =====================================================================================================================
// Ring (scale 2.4: 1 unit = 0.15 b; outer radius 3.5 b, D = 7.0 b)
// =====================================================================================================================
export const RING = {
  rOut: 23.0, rIn: 17.5,                  // band outer / inner wall (facet inradius)
  yTop: 2.3, yBot: -2.1,                  // band (0.66 b)
  rTierO: 21.0, rTierI: 15.5, yTier: -4.1, // lower tier (toothed ring under the band)
  gaps: [4, 12],                          // facets left open at +X (k 4) and -X (k 12): the medallion docks
};
// the two arcs of facets between the dock gaps: k -3..3 (the front) and 5..11 (the back)
const ARCS = [[-3, 4], [5, 12]];
function ring() {
  const R = RING, els = [], O = [0, 0, 0];
  for (const range of ARCS) {
    // band walls (tile per facet, light level per azimuth)
    els.push(...lathe('y', O, [{a: [R.yBot, R.yTop], r: R.rOut, tex: k => 'band_' + level(azOf(k))}], {vFrom: R.yTop, vTo: R.yBot, tile: true, range}));
    els.push(...lathe('y', O, [{a: [R.yBot, R.yTop], r: R.rIn, tex: k => 'bandin_' + level(azOf(k) + 180)}], {vFrom: R.yTop, vTo: R.yBot, tile: true, inward: true, range}));
    // top face, the underside strip outside the tier, the tier walls, its underside and the strip inside the band
    els.push(...annulus('y', O, R.yTop, R.rIn, R.rOut, '+', 'rtop', {stagger: .04, range, shade: false}));
    els.push(...annulus('y', O, R.yBot, R.rTierO, R.rOut, '-', 'rbot', {stagger: .04, range, shade: false}));
    els.push(...lathe('y', O, [{a: [R.yTier, R.yBot], r: R.rTierO, tex: k => 'tier_' + level(azOf(k))}], {vFrom: R.yBot, vTo: R.yTier, tile: true, range}));
    els.push(...lathe('y', O, [{a: [R.yTier, R.yBot], r: R.rTierI, tex: k => 'tier_' + level(azOf(k) + 180)}], {vFrom: R.yBot, vTo: R.yTier, tile: true, inward: true, range}));
    els.push(...annulus('y', O, R.yTier, R.rTierI, R.rTierO, '-', 'tbot', {stagger: .04, range, shade: false}));
    els.push(...annulus('y', O, R.yBot, R.rTierI, R.rIn, '+', 'rbot', {stagger: .04, range, shade: false}));
    for (let k = range[0]; k < range[1]; k++) {
      // raised teeth on the top edge: a wide block and a narrow one per facet (blocky crenellation)
      if (k !== 0 && k !== 8) {
        const odd = ((k % 2) + 2) % 2;
        els.push(odd ? segBox(k, [20.4, 23.3], [-2.2, 2.2], [R.yTop - .1, R.yTop + 1.05], {all: 'tooth', up: 'tooth_top'})
          : segBox(k, [21.4, 23.3], [-3.6, -1.2], [R.yTop - .1, R.yTop + .6], {all: 'tooth', up: 'tooth_top'}));
      }
      // a gear rib on the tier wall (the lower tier reads as a gear)
      els.push(segBox(k, [20.4, 21.7], [-1.1, 1.1], [R.yTier + .4, R.yBot - .3], {all: 'tooth', up: 'bronze', down: 'bronze'}));
    }
  }
  // the dock posts either side of each gap (they close the band ends; the medallion sits between them)
  for (const sx of [1, -1]) for (const sz of [1, -1]) {
    const x0 = sx > 0 ? R.rTierI - .3 : -(R.rOut + .2), x1 = sx > 0 ? R.rOut + .2 : -(R.rTierI - .3);
    els.push(abox([x0, R.yTier - .3, sz * 3.15], [x1, R.yTop + .7, sz * 4.95], {all: 'bronze', front: 'engraved', back: 'engraved', up: 'tooth_top'}));
    // a cream block capping the post
    const c0 = sx > 0 ? 19.6 : -23.7, c1 = sx > 0 ? 23.7 : -19.6;
    els.push(abox([c0, R.yTop + .7, sz * 3.0], [c1, R.yTop + 1.9, sz * 5.1], 'tooth'));
  }
  // back keystone (+Z): the cream T block straddling the band, two grid panels and the stepped bronze bell under it
  els.push(abox([-1.9, R.yBot - .3, 16.6], [1.9, R.yTop + 2.9, 23.9], {all: 'cream', front: 'pillar', back: 'pillar'}));
  els.push(abox([-2.6, R.yTop + 2.9, 16.3], [2.6, R.yTop + 3.6, 24.0], {all: 'tooth', up: 'tooth_top'}));
  for (const s of [1, -1]) els.push(abox([s * 1.9, -1.4, 16.95], [s * 5.4, R.yTop + 1.3, 23.6], {all: 'cream', front: 'kgrid', back: 'kgrid'}));
  els.push(abox([-3.8, R.yTier - 1.0, 17.8], [3.8, R.yTier, 23.1], 'bell'));
  els.push(abox([-2.7, R.yTier - 2.1, 18.6], [2.7, R.yTier - 1.0, 22.4], 'bell'));
  els.push(abox([-1.6, R.yTier - 3.0, 19.4], [1.6, R.yTier - 2.1, 21.6], 'bell'));
  els.push(abox([-.7, R.yTier - 3.6, 20.0], [.7, R.yTier - 3.0, 21.0], 'gold'));
  // front keystone: the socket of the iris (the iris is hub_eye), with brackets either side
  els.push(abox([-2.9, R.yBot - .2, -23.7], [2.9, R.yTop + .5, -22.4], {all: 'cream', front: 'kgrid'}));
  for (const s of [1, -1]) els.push(abox([s * 2.9, -1.6, -23.5], [s * 4.3, R.yTop + .2, -21.0], 'bronze'));
  // top eye-ports (dark red, orange rims) near -60 / +120 degrees, and the 8 bomb ports underneath
  for (const k of [-3, 5]) els.push(segSquare(k, 20.25, R.yTop + .06, 1.5, 'up', 'port'));
  for (let k = 1; k < 16; k += 2) els.push(segSquare(k, 18.25, R.yTier - .06, 1.45, 'down', 'bport'));
  return els;
}
// The glow strips of the ring (brightness 15, look idle / hot / off): the seam cards just outside both band walls,
// the eye-port rims and the bomb-port rims and embers.
function ringGlow(look) {
  const R = RING, els = [], O = [0, 0, 0];
  for (const range of ARCS) {
    els.push(...lathe('y', O, [{a: [R.yBot, R.yTop], r: R.rOut + .09, tex: 'seam_' + look}], {vFrom: R.yTop, vTo: R.yBot, tile: true, range}));
    els.push(...lathe('y', O, [{a: [R.yBot, R.yTop], r: R.rIn - .09, tex: 'seam_' + look}], {vFrom: R.yTop, vTo: R.yBot, tile: true, inward: true, range}));
  }
  for (const k of [-3, 5]) els.push(segSquare(k, 20.25, R.yTop + .14, 1.5, 'up', 'prim_' + look));
  for (let k = 1; k < 16; k += 2) {
    els.push(segSquare(k, 18.25, R.yTier - .14, 1.45, 'down', 'brim_' + look));
    els.push(segSquare(k, 18.25, R.yTier - .1, 1.45, 'down', 'bcore_' + look));
  }
  return els;
}

// =====================================================================================================================
// Keystone iris + its gold spike (hub_eye, scale 1: pivot on the band front, the spike hangs along -Y)
// =====================================================================================================================
function goldCone(axis, base, tip, r0, nSec, {n = 8, collar = null, close = true} = {}) {
  // stepped cone of n facets from a (base) to b (tip) along +axis or -axis; gold8 wrap, alternating facets
  const up = tip > base, at = stations(Math.min(base, tip), Math.max(base, tip), nSec);
  const prof = a => { const f = Math.abs(a - base) / Math.abs(tip - base); return Math.max(.12, r0 * Math.pow(1 - f, .92)); };
  return turned(axis, [0, 0, 0], at, prof, 'gold8', 'ledge_gold', {vFrom: base, vTo: tip, n}, close ? (up ? '-' : '+') : '');
}
function hubEye(look) {
  const els = [];
  els.push(...lathe('z', [0, 0, 0], [{a: [-1.6, .4], r: 8.0, tex: 'bronze'}], {vFrom: -1.6, vTo: .4, tile: true}));
  els.push(squareZ('iris_' + look, 0, 0, 9.4, -1.7));
  // the collar and the big gold spike under the iris (0.16 D = 1.1 b)
  els.push(...lathe('y', [0, 0, 0], [{a: [-8.6, -6.9], r: 4.9, tex: 'collar'}], {vFrom: -6.9, vTo: -8.6, tile: true}));
  els.push(disc('y', [0, 0, 0], -6.9, 4.9 * DK, '+', 'ledge_gold', true));
  els.push(...goldCone('y', -8.6, -23.8, 4.5, 11));
  // the small spike above it
  els.push(...lathe('y', [0, 0, 0], [{a: [7.6, 8.8], r: 2.2, tex: 'collar'}], {vFrom: 8.8, vTo: 7.6, tile: true}));
  els.push(...goldCone('y', 8.8, 13.6, 1.8, 3));
  return els;
}

// =====================================================================================================================
// Core assembly (core, core_eye, core_arch, core_brim, core_glow, core_shell; one pivot = the sphere centre)
// =====================================================================================================================
export const CORE_R = 20;                 // sphere radius (scale 1: 1.25 b, D 0.36)
function core() {
  const R = CORE_R, els = [...sphere(R, 'shell', 'ledge_plum', 28)];
  // dark-red side cushions with cream straps
  for (const s of [1, -1]) {
    els.push(abox([s * 16.6, -6.2, -7.2], [s * 20.6, 6.2, 7.2], 'red'));
    els.push(abox([s * 18.6, -4.8, -5.8], [s * 21.4, 4.8, 5.8], 'red'));
    for (const y of [-3.2, 2.4]) els.push(abox([s * 16.4, y - .7, -7.6], [s * 21.8, y + .7, 7.6], 'clamp'));
  }
  // cream Y bracket and the gold stud at the bottom
  els.push(abox([-1.3, -22.0, -1.3], [1.3, -18.4, 1.3], 'cream'));
  for (const s of [1, -1]) els.push(abox([s * 1.0, -21.0, -1.1], [s * 6.2, -19.6, 1.1], 'cream', {rot: ['z', s * 22.5, [s * 1.0, -20.3, 0]]}));
  els.push(abox([-.9, -22.6, -.9], [.9, -22.0, .9], 'gold'));
  return els;
}
function coreEye(look) {
  // the eye frame: a cream gear-tooth ring standing off the sphere (tube + toothed face) and the glow card inside
  const els = [];
  els.push(...lathe('z', [0, 0, 0], [{a: [-21.7, -16.6], r: 9.0, tex: 'cream'}], {vFrom: -16.6, vTo: -21.7, tile: true}));
  els.push(...annulus('z', [0, 0, 0], -21.75, 6.9, 10.6, '-', 'eyeframe', {stagger: .03, shade: false}));
  els.push(squareZ('eye_' + look, 0, 0, 7.4, -21.35));
  return els;
}
function coreArch() {
  // vertical gear ring (scale 1.1): bronze outer wall, dark-red lining, bronze sides, 8 cream clamps
  const O = [0, 0, 0], els = [];
  els.push(...lathe('z', O, [{a: [-2.5, 2.5], r: 22.2, tex: 'arch_out'}], {vFrom: -2.5, vTo: 2.5, tile: true}));
  els.push(...lathe('z', O, [{a: [-2.5, 2.5], r: 19.6, tex: 'arch_in'}], {vFrom: -2.5, vTo: 2.5, tile: true, inward: true}));
  els.push(...annulus('z', O, -2.5, 19.6, 22.2, '-', 'dbronze', {stagger: .03, shade: false}));
  els.push(...annulus('z', O, 2.5, 19.6, 22.2, '+', 'dbronze', {stagger: .03, shade: false}));
  for (let k = 0; k < 16; k += 2) els.push(segBoxZ(k, [19.0, 23.1], [-1.2, 1.2], [-3.1, 3.1], 'clamp'));
  return els;
}
export const BRIM_Y = 4.3;               // brim plane above the core centre (core_brim units, 0.35 b)
function coreBrim() {
  // tilted grooved brim (scale 1.3; the tilt is the part's), set 0.35 b above the sphere's equator like a hat brim,
  // its edge, the orbit wire in its own plane through the centre and the bead
  const B = BRIM_Y, els = [polarCard('brimc', B, 20.6)];
  els.push(...lathe('y', [0, 0, 0], [{a: [B - .75, B + .75], r: 20.4, tex: 'brim_edge'}], {vFrom: B + .75, vTo: B - .75, tile: true}));
  els.push(polarCard('wire', 0, 22.6, -22.5));
  // the gold bead rides the wire 40 degrees to the device's right of the front (beside the eye, as in the PDF)
  const ba = 40 * D2R, bx = -Math.sin(ba) * 22.6, bz = -Math.cos(ba) * 22.6;
  els.push(abox([bx - 1.5, -1.5, bz - 1.5], [bx + 1.5, 1.5, bz + 1.5], 'gold', {rot: ['x', -22.5, [0, 0, 0]]}));
  return els;
}
// Glow looks of core_glow (scale 1): the charge sphere and the white-gold flash are crossed radial cards; the exposed
// gold sphere is a turned shell with the glyph.
function crossGlow(sprite, R) {
  const r = {X0: -R, X1: R, Y0: -R, Y1: R}, c = [0, 0, 0];
  return [cardZ(sprite, 0, r), cardX(sprite, 0, {Z0: -R, Z1: R, Y0: -R, Y1: R}), cardY(sprite, 0, {X0: -R, X1: R, Z0: -R, Z1: R}),
    cardZ(sprite, 0, r, {rot: ['y', 45, c]}), cardZ(sprite, 0, r, {rot: ['y', -45, c]})];
}
// A turned sphere of nb bands of equal angle (smoother than knob's 12): the core shell and the glow shells.
export function sphere(R, tex, ledge, nb = 16) {
  const at = Array.from({length: nb + 1}, (_, i) => R * Math.sin((-90 + 180 * i / nb) * D2R));
  return turned('y', [0, 0, 0], at, a => R * Math.sqrt(Math.max(0, 1 - (a / R) ** 2)), tex, ledge, {vFrom: R, vTo: -R}, '-+');
}
const shellSphere = (sprite, ledge, R) => sphere(R, sprite, ledge, 12);

// =====================================================================================================================
// Halo pair
// =====================================================================================================================
function halo(v) {
  const O = [0, 0, 0], s = v ? '_v' : '', els = [];
  els.push(...lathe('y', O, [{a: [-.9, .9], r: 19.6, tex: 'halo_out' + s}], {vFrom: .9, vTo: -.9, tile: true}));
  els.push(...lathe('y', O, [{a: [-.9, .9], r: 16.6, tex: 'halo_in' + s}], {vFrom: .9, vTo: -.9, tile: true, inward: true}));
  els.push(...annulus('y', O, .9, 16.6, 19.6, '+', 'halo_face' + s, {stagger: .03, shade: false}));
  els.push(...annulus('y', O, -.9, 16.6, 19.6, '-', 'halo_face' + s, {stagger: .03, shade: false}));
  return els;
}
function halo2(v) {
  const s = v ? '_v' : '';
  return [polarCard('ring2' + s, 0, 19.2), ...lathe('y', [0, 0, 0], [{a: [-.8, .8], r: 17.1, tex: 'ring2_band' + s}], {vFrom: .8, vTo: -.8, tile: true})];
}

// =====================================================================================================================
// Rim spikes (scale 1.4; pivot = the dock point at the ring end, +X outward): the X frame round the medallion, the
// shaft, the ribbed collar and the 8-facet gold spearhead (tip 2.05 b out: 10.1 b tip to tip)
// =====================================================================================================================
export const SPIKE_TIP = 19.8;          // cone tip, spike model units along +X
function spike() {
  const O = [0, 0, 0], els = [];
  els.push(...lathe('z', O, [{a: [-1.0, 1.0], r: 7.2, tex: 'bronze'}], {vFrom: -1, vTo: 1, tile: true}));
  els.push(...lathe('z', O, [{a: [-1.0, 1.0], r: 6.4, tex: 'red'}], {vFrom: -1, vTo: 1, tile: true, inward: true}));
  els.push(...annulus('z', O, -1.0, 6.4, 7.2, '-', 'bronze', {stagger: .03, shade: false}));
  els.push(...annulus('z', O, 1.0, 6.4, 7.2, '+', 'bronze', {stagger: .03, shade: false}));
  // four gold prongs at the diagonals gripping the medallion rim, and lugs on the frame
  for (const k of [2, 6, 10, 14]) els.push(segBoxZ(k, [5.9, 7.6], [-.75, .75], [-1.4, 1.4], 'gold'));
  for (const k of [0, 8]) els.push(segBoxZ(k, [6.8, 8.4], [-1.3, 1.3], [-1.2, 1.2], 'bronze'));
  // shaft and collar (along +X)
  els.push(...lathe('x', O, [{a: [6.9, 8.4], r: 2.0, tex: 'engraved'}], {vFrom: 6.9, vTo: 8.4, tile: true, n: 8}));
  els.push(...lathe('x', O, [{a: [8.0, 9.4], r: 4.3, tex: 'collar'}], {vFrom: 8.0, vTo: 9.4, tile: true}));
  els.push(disc('x', O, 8.0, 4.3 * DK, '-', 'ledge_gold', true));
  els.push(...goldCone('x', 9.4, SPIKE_TIP, 3.9, 12));
  return els;
}

// =====================================================================================================================
// Medallions (scale 1; Ø 1.0 b, 0.33 b thick, face -Z): the eye medallion and the gear medallion
// =====================================================================================================================
function medalEye(hot) {
  const O = [0, 0, 0], els = [];
  els.push(...lathe('z', O, [{a: [-2.6, 2.6], r: 7.3, tex: 'bronze'}], {vFrom: -2.6, vTo: 2.6, tile: true}));
  for (let k = 0; k < 16; k++) els.push(segBoxZ(k, [7.0, 8.2], [-.85, .85], [-1.9, 1.9], 'gold'));
  els.push(squareZ(hot ? 'medal_eye_hot' : 'medal_eye', 0, 0, 7.9, -2.7));
  els.push(squareZ('medal_back', 0, 0, 7.9, 2.7));
  return els;
}
function medalGear(hot) {
  const O = [0, 0, 0], els = [];
  els.push(...lathe('z', O, [{a: [-2.4, 2.4], r: 6.0, tex: 'dbronze'}], {vFrom: -2.4, vTo: 2.4, tile: true}));
  for (let k = 0; k < 16; k++) els.push(segBoxZ(k, [5.6, 8.1], [-1.05, 1.05], [-2.2, 2.2], k % 2 ? 'bronze' : 'gold'));
  els.push(squareZ(hot ? 'medal_gear_hot' : 'medal_gear', 0, 0, 7.9, -2.5));
  els.push(squareZ('medal_back', 0, 0, 7.9, 2.5));
  return els;
}

// =====================================================================================================================
// Drill pods (scale 1; 1.25 b tall; pivot at the gear disc centre): cog cap, gear disc, glowing collar, striped cone
// =====================================================================================================================
function drill() {
  const at = [-16.1, -13.95, -11.8, -9.65, -7.5, -5.35, -3.2, -1.6, 1.6, 4.0];
  const prof = y => (y > 1.6 ? 3.4 : y > -1.6 ? 7.0 : y > -3.2 ? 5.3 : .5 + 4.4 * (y + 16.1) / 12.9);
  const els = turned('y', [0, 0, 0], at, prof, 'drill', 'ledge_dbronze', {vFrom: 4, vTo: -16, tile: true});
  els.push(disc('y', [0, 0, 0], 4.0, 3.4 * DK, '+', 'drill_top', true));
  for (let k = 0; k < 16; k += 2) els.push(segBox(k, [6.4, 8.2], [-1.25, 1.25], [-1.45, 1.45], {all: 'tooth', up: 'tooth_top'}));
  for (let k = 1; k < 16; k += 4) els.push(segBox(k, [1.0, 3.0], [-.9, .9], [3.9, 5.2], 'tooth'));
  return els;
}

// =====================================================================================================================
// Plates (scale 1.25): bronze discs with a glowing groove (lower plate) / an engraved ring (upper small disc)
// =====================================================================================================================
function plateModel(sprite, R, t) {
  const O = [0, 0, 0];
  return [polarCard(sprite, t, R), polarCard(sprite, -t, R),
    ...lathe('y', O, [{a: [-t, t], r: R * .985, tex: 'plate_rim'}], {vFrom: t, vTo: -t, tile: true})];
}

// =====================================================================================================================
// Pendulum (scale 1.6; pivot = the hang point at the top of the cog): silver cog with a keyhole, bronze spindle,
// cream-gold protractor arc (concave up, 135 degrees, chord 1.54 b), gold dagger (tip 2.1 b below the hang point)
// =====================================================================================================================
export const PEND = {cogY: -2.6, arcC: -1.0, arcRo: 8.6, arcRi: 7.1, tipY: -21.0};
function pendulum() {
  const els = [], {cogY, arcC, arcRo, arcRi} = PEND, A = [0, arcC, 0];
  // cog: two face cards and a hub drum
  els.push(squareZ('cog', 0, cogY, 3.3, -.55), squareZ('cog', 0, cogY, 3.3, .55));
  els.push(...lathe('z', [0, cogY, 0], [{a: [-.5, .5], r: 2.3, tex: 'silver'}], {vFrom: -.5, vTo: .5, tile: true, n: 8}));
  // spindle from the cog through the arc to the dagger
  els.push(...lathe('y', [0, 0, 0], [{a: [-11.2, cogY - 2.0], r: .7, tex: 'engraved'}], {vFrom: cogY - 2.0, vTo: -11.2, tile: true, n: 8}));
  // protractor arc: facets k 6..10 of a ring about Z (azimuth from +Y toward +X), the lower 135 degrees
  const range = [6, 11];
  els.push(...lathe('z', A, [{a: [-.75, .75], r: arcRo, tex: 'arc_edge'}], {vFrom: -.75, vTo: .75, tile: true, range}));
  els.push(...lathe('z', A, [{a: [-.75, .75], r: arcRi, tex: 'arc_edge'}], {vFrom: -.75, vTo: .75, tile: true, inward: true, range}));
  els.push(...annulus('z', A, -.75, arcRi, arcRo, '-', 'arc_face', {stagger: .03, range, shade: false}));
  els.push(...annulus('z', A, .75, arcRi, arcRo, '+', 'arc_face', {stagger: .03, range, shade: false}));
  // square end caps at both ends (facets 6 and 10 centred at 135 / 225 degrees: the ends at about +-123.75)
  for (const s of [1, -1]) els.push(segBoxZ(s > 0 ? 6 : 10, [arcRi - .3, arcRo + .5], s > 0 ? [-4.0, -2.4] : [2.4, 4.0], [-1.0, 1.0], 'gold', A));
  // a hub where the spindle crosses the arc, then the dagger (crossed cards)
  els.push(abox([-1.2, -11.0, -1.2], [1.2, -9.4, 1.2], 'gold'));
  const D = {X0: -1.9, X1: 1.9, Y0: PEND.tipY, Y1: -9.8};
  els.push(cardZ('dagger', 0, D), cardX('dagger', 0, {Z0: -1.9, Z1: 1.9, Y0: D.Y0, Y1: D.Y1}));
  return els;
}
function pendGlow() {
  // the Ousia flame: four crossed translucent cards round the cog, licking up
  const r = {X0: -3.8, X1: 3.8, Y0: PEND.cogY - 3.8, Y1: PEND.cogY + 7.6}, c = [0, PEND.cogY, 0];
  return [cardZ('ousia', 0, r), cardX('ousia', 0, {Z0: -3.8, Z1: 3.8, Y0: r.Y0, Y1: r.Y1}),
    cardZ('ousia', 0, r, {rot: ['y', 45, c]}), cardZ('ousia', 0, r, {rot: ['y', -45, c]})];
}

// =====================================================================================================================
// Beams and the column (scale 1: 1 b long along -Y from the pivot, 1 b wide; the part's scale sets length and width)
// =====================================================================================================================
function beamModel(sprite) {
  const r = {X0: -8, X1: 8, Y0: -16, Y1: 0};
  return [cardZ(sprite, 0, r), cardX(sprite, 0, {Z0: -8, Z1: 8, Y0: -16, Y1: 0}), cardZ(sprite, 0, r, {rot: ['y', 45, [0, -8, 0]]}), cardZ(sprite, 0, r, {rot: ['y', -45, [0, -8, 0]]})];
}

// =====================================================================================================================
// Tower (파쇄): the telescoping column (scale 2.0, pivot at its base) and the two tier discs
// =====================================================================================================================
function towerCol() {
  const O = [0, 0, 0], els = [];
  els.push(...lathe('y', O, [{a: [0, 21.4], r: 5.6, tex: 'tower_col'}], {vFrom: 0, vTo: 21.4, tile: true}));
  for (const [a0, a1] of [[0, 1.2], [10.2, 11.2], [20.2, 21.8]]) els.push(...lathe('y', O, [{a: [a0, a1], r: 6.3, tex: 'collar'}], {vFrom: a1, vTo: a0, tile: true}));
  els.push(disc('y', O, 21.8, 6.3 * DK, '+', 'ledge_cream', true));
  return els;
}
function towerTier(sprite, R, rim, t) {
  return [polarCard(sprite, t, R), polarCard(sprite, -t, R), ...lathe('y', [0, 0, 0], [{a: [-t, t], r: R * .985, tex: rim}], {vFrom: t, vTo: -t, tile: true})];
}

// =====================================================================================================================
// Props (not rig parts): the falling bomb and the gold drill missile
// =====================================================================================================================
function bomb() {
  const els = sphere(5.0, 'bomb', 'ledge_dbronze', 8);
  els.push(...lathe('y', [0, 0, 0], [{a: [-1.1, 1.1], r: 5.3, tex: 'collar'}], {vFrom: 1.1, vTo: -1.1, tile: true}));
  return els;
}
function missile() {
  // tip down (-Y): collar, striped body, gold point
  const els = [...lathe('y', [0, 0, 0], [{a: [-1.6, 1.6], r: 3.6, tex: 'collar'}], {vFrom: 1.6, vTo: -1.6, tile: true})];
  els.push(disc('y', [0, 0, 0], 1.6, 3.6 * DK, '+', 'ledge_gold', true));
  els.push(...goldCone('y', -1.6, -20.5, 3.2, 7));
  for (const k of [0, 4, 8, 12]) els.push(segBox(k, [2.6, 5.4], [-.5, .5], [-.5, 3.4], 'gold'));
  return els;
}

// =====================================================================================================================
// name -> elements. Variants share the display of their part (item-model swaps).
// =====================================================================================================================
export const EMPTY = 'none';
export function partModels() {
  const m = {
    ring: ring(), ring_glow_idle: ringGlow('idle'), ring_glow_hot: ringGlow('hot'), ring_glow_off: ringGlow('off'),
    hub_shut: hubEye('shut'), hub_open: hubEye('open'), hub_hot: hubEye('hot'),
    halo: halo(false), halo_v: halo(true), halo2: halo2(false), halo2_v: halo2(true),
    core: core(), core_arch: coreArch(), core_brim: coreBrim(),
    glow_charge: crossGlow('glow_charge', 22), glow_flash: crossGlow('glow_flash', 22), glow_gold: shellSphere('gold_shell', 'bubble_ledge', 21.2),
    spike_l: spike(), spike_r: mirrorModel(spike()),
    medal_eye: medalEye(false), medal_eye_hot: medalEye(true), medal_gear: medalGear(false), medal_gear_hot: medalGear(true),
    drill: drill(), plate: plateModel('plate_disc', 17.0, .6), plate2: plateModel('plate2_disc', 13.4, .5),
    pendulum: pendulum(), pend_glow: pendGlow(),
    beam_gold: beamModel('beam_gold'), beam_link: beamModel('beam_link'), col_gold: beamModel('col_gold'), col_violet: beamModel('col_violet'),
    tower_col: towerCol(), tower_t1: towerTier('tower_t1', 22.6, 'bronze', .75), tower_t2: towerTier('tower_t2', 22.2, 'tower_rim', .6),
    bomb: bomb(), missile: missile(),
    [EMPTY]: [],
  };
  for (const look of ['idle', 'charge', 'field', 'dim']) m['eye_' + look] = coreEye(look);
  for (const s of [0, 1, 2, 3]) m['bubble_' + s] = shellSphere('bubble_' + s, 'bubble_ledge', 22.4);
  m.bubble_burst = shellSphere('bubble_burst', 'bubble_ledge', 22.4);
  return m;
}
