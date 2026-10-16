/**
 * Navia's weapons for the articulated rig.
 *
 * navia_halberd: the gold-and-navy halberd of images/4.png, which stands in for her claymore
 * (the head is the "blade" of the claymore swings). From the butt up: a two-lobed gold finial,
 * the espresso handle with an oxblood wrap and three pearl studs (the hand), the lower gold
 * ring, a crossguard with down-swept spikes, the faceted champagne sleeve, navy shaft with a
 * silver chevron collar, the gold rose boss, the light-blue crystal, a gold bell collar, the
 * violet-navy socket and the fleur-de-lis spear point. The head (big pale-gold crescent axe on
 * model -X, the back fin with its violet gem on +X, champagne C/S scrolls framing the crystal)
 * is painted on three stacked alpha-cut cards, traced from the reference (navia_weapon_paint.mjs).
 *
 * navia_parasol / navia_parasol_open: her parasol gun, closed and open. A black crook handle
 * with gold fittings and a gold cog, a black shaft and a gold muzzle ferrule. Closed: a gold
 * ruffle collar and the folded black-indigo canopy with a gem plaque and white lace, as four
 * crossed profile cards around stepped core boxes. Open: an eight-rib canopy about 18.6 units
 * across, whose lining (gold with orange-red paisley) and outer face are the cap faces of thin
 * discs stacked into a shallow dome, with crossed profile cards for the side view.
 *
 * Model frame (as the other rig weapons; the motion clips rely on it): grip [8,8,8], shaft
 * along +Y, broad faces of the halberd head facing +-Z, its crescent toward -X; the parasol's
 * muzzle and canopy point to +Y. Every coordinate stays within -16..32 and rotations are single
 * axis, 45 degrees.
 */
import {paintedBox, plate, card, cardX} from './weapon_faces.mjs';
import {NV_HEAD, NV_TIP, NV_CRYSTAL, NV_GUARD, NV_BUTT, NP} from './navia_weapon_paint.mjs';

// A box whose front/side faces map the sprite along the box, caps from the sprite's middle.
const fitting = (sprite, capSprite = sprite, capUV = [.2, .2, .8, .8]) => (from, to, rotation) => paintedBox(from, to, {
  front: {sprite, u: ['x', from[0], to[0]], v: ['y', to[1], from[1]]},
  side: {sprite, u: ['z', from[2], to[2]], v: ['y', to[1], from[1]]},
  cap: {sprite: capSprite, uv: capUV},
}, rotation);
// Crossed cards through the shaft axis: XY and ZY planes.
const crossed = (hw, y0, y1, sprite) => [card([8 - hw, y0], [8 + hw, y1], 8, sprite), cardX([8 - hw, y0], [8 + hw, y1], 8, sprite)];
// Four cards through the axis (0, 90 and +-45 degrees about Y), for round props seen from any side.
const star = (hw, y0, y1, sprite) => [...crossed(hw, y0, y1, sprite),
  ...[45, -45].map(angle => card([8 - hw, y0], [8 + hw, y1], 8, sprite, [0, 0, 1, 1], {origin: [8, (y0 + y1) / 2, 8], axis: 'y', angle}))];
// Horizontal disc of radius r at height y: only the cap faces (alpha-cut round sprites).
function disc(r, y, up, down) {
  const from = [8 - r, y, 8 - r], to = [8 + r, y, 8 + r];
  const spec = {front: {sprite: up || down, uv: [0, 0, 1, 1]}};
  if (up) spec.up = {sprite: up, u: ['x', from[0], to[0]], v: ['z', from[2], to[2]]};
  if (down) spec.down = {sprite: down, u: ['x', from[0], to[0]], v: ['z', from[2], to[2]]};
  const el = paintedBox(from, to, spec);
  for (const f of ['north', 'south', 'east', 'west']) delete el.faces[f];
  if (!up) delete el.faces.up;
  if (!down) delete el.faces.down;
  return el;
}

function halberd() {
  const gold = fitting('nv_gold');
  const e = [];
  // Handle and butt.
  e.push(paintedBox([7.6, 4.1, 7.6], [8.4, 9.45, 8.4], {
    front: {sprite: 'nv_wrap', u: ['x', 7.6, 8.4], v: ['y', 9.45, 4.1]},
    side: {sprite: 'nv_wrap', u: ['z', 7.6, 8.4], v: ['y', 9.45, 4.1]},
    cap: {sprite: 'nv_gold', uv: [.2, .2, .8, .8]},
  }));
  e.push(...crossed(NV_BUTT.HW, NV_BUTT.Y0, NV_BUTT.Y1, 'nv_butt'));
  e.push(gold([7.75, 2.2, 7.75], [8.25, 4.15, 8.25], {origin: [8, 3.2, 8], axis: 'y', angle: 45}));
  // Lower ring, crossguard and the faceted sleeve.
  e.push(gold([7.42, 9.35, 7.42], [8.58, 10.65, 8.58]));
  e.push(...crossed(NV_GUARD.HW, NV_GUARD.Y0, NV_GUARD.Y1, 'nv_guard'));
  e.push(fitting('nv_sleeve', 'nv_gold')([7.25, 11.6, 7.25], [8.75, 14.9, 8.75]));
  e.push(gold([7.4, 12.4, 7.4], [8.6, 14.2, 8.6], {origin: [8, 13.3, 8], axis: 'y', angle: 45}));
  // Navy shaft, silver collar, navy shaft with the silver strip.
  e.push(fitting('nv_shaft2', 'nv_gold')([7.5, 14.8, 7.5], [8.5, 17.5, 8.5]));
  e.push(fitting('nv_collar', 'nv_gold')([7.28, 17.4, 7.28], [8.72, 19.1, 8.72]));
  e.push(fitting('nv_shaft1', 'nv_gold')([7.48, 19.0, 7.48], [8.52, 21.2, 8.52]));
  // Gold rose boss with the rose on all four faces.
  e.push(gold([7.5, 21.15, 7.5], [8.5, 22.4, 8.5]));
  e.push(plate(8, 21.78, 1.15, 7.46, 'nv_rose'), plate(8, 21.78, 1.15, 8.54, 'nv_rose'));
  e.push(cardX([7.425, 21.205], [8.575, 22.355], 7.46, 'nv_rose'), cardX([7.425, 21.205], [8.575, 22.355], 8.54, 'nv_rose'));
  // Crystal: a faceted core (diamond cross-section) inside two crossed silhouette cards.
  e.push(fitting('nv_crystal', 'nv_crystal', [.3, .4, .7, .6])([7.55, 22.6, 7.55], [8.45, 24.7, 8.45], {origin: [8, 23.65, 8], axis: 'y', angle: 45}));
  e.push(...crossed(NV_CRYSTAL.HW, NV_CRYSTAL.Y0, NV_CRYSTAL.Y1, 'nv_crystal'));
  // Bell collar, socket and the spear point.
  e.push(gold([7.42, 24.75, 7.42], [8.58, 25.15, 8.58]), gold([7.58, 25.1, 7.58], [8.42, 25.5, 8.42]));
  e.push(fitting('nv_socket', 'nv_gold')([7.62, 25.45, 7.62], [8.38, 27.95, 8.38]));
  e.push(...crossed(NV_TIP.HW, NV_TIP.Y0, NV_TIP.Y1, 'nv_tip'));
  // The head on three stacked cards (front, middle, back).
  for (const z of [7.73, 8.0, 8.27]) e.push(card([NV_HEAD.X0, NV_HEAD.Y0], [NV_HEAD.X1, NV_HEAD.Y1], z, 'nv_head'));
  return e;
}

// ---- parasol -----------------------------------------------------------------------------------
function handle() {
  const gold = fitting('np_gold');
  return [
    // Black crook below the hand (three stacked cards), the grip, gold collar and cog.
    ...[7.74, 8.0, 8.26].map(z => card([NP.CROOK.X0, NP.CROOK.Y0], [NP.CROOK.X1, NP.CROOK.Y1], z, 'np_handle')),
    fitting('np_shaft', 'np_gold')([7.66, 6.4, 7.66], [8.34, 9.6, 8.34]),
    gold([7.55, 9.5, 7.55], [8.45, 10.1, 8.45]),
    gold([7.6, 10.05, 7.6], [8.4, 10.55, 8.4], {origin: [8, 10.3, 8], axis: 'y', angle: 45}),
    disc(NP.COG, 10.32, 'np_cog', 'np_cog'),
  ];
}
function muzzle(y0) {
  const gold = fitting('np_gold');
  return [
    fitting('np_ferrule', 'np_gold')([7.58, y0, 7.58], [8.42, y0 + 1.8, 8.42]),
    paintedBox([7.48, y0 + 1.7, 7.48], [8.52, y0 + 2.3, 8.52], {
      front: {sprite: 'np_gold', u: ['x', 7.48, 8.52], v: ['y', y0 + 2.3, y0 + 1.7]},
      side: {sprite: 'np_gold', u: ['z', 7.48, 8.52], v: ['y', y0 + 2.3, y0 + 1.7]},
      cap: {sprite: 'np_gold', uv: [.2, .2, .8, .8]},
      up: {sprite: 'np_bore', u: ['x', 7.48, 8.52], v: ['z', 7.48, 8.52]},
    }),
    gold([7.62, y0 - .3, 7.62], [8.38, y0 + .05, 8.38]),
  ];
}
function parasolClosed() {
  const fold = fitting('np_fold', 'np_fold', [.3, .1, .7, .3]);
  const B = NP.BUNDLE;
  return [
    ...handle(),
    fitting('np_shaft', 'np_gold')([7.72, 10.5, 7.72], [8.28, 13.2, 8.28]),
    // Folded canopy: stepped core inside four crossed profile cards, the ruffle rosettes, the
    // gem plaque and the lace collar under the muzzle.
    fitting('np_ruffle', 'np_gold')([7.1, 11.15, 7.1], [8.9, 13.1, 8.9]),
    fold([6.98, 13.05, 6.98], [9.02, 15.2, 9.02]),
    fold([7.14, 15.15, 7.14], [8.86, 17.2, 8.86]),
    fold([7.32, 17.15, 7.32], [8.68, 19.0, 8.68]),
    fold([7.5, 18.95, 7.5], [8.5, 20.3, 8.5]),
    ...star(B.HW, B.Y0, B.Y1, 'np_bundle'),
    disc(2.05, 13.25, 'np_rosette', null), disc(1.95, 11.05, null, 'np_rosette'),
    plate(8, 14.6, 1.25, 6.93, 'np_plaque'),
    fitting('np_lace')([7.42, 20.15, 7.42], [8.58, 20.65, 8.58]),
    ...muzzle(20.6),
  ];
}
// Eight tangential cards around the axis at distance D (0, 90 and +-45 degrees about Y).
function skirt({D, HW, Y0, Y1}) {
  const yc = (Y0 + Y1) / 2, out = [];
  for (const z of [8 - D, 8 + D]) out.push(card([8 - HW, Y0], [8 + HW, Y1], z, 'np_skirt'));
  for (const x of [8 - D, 8 + D]) out.push(cardX([8 - HW, Y0], [8 + HW, Y1], x, 'np_skirt'));
  for (const angle of [45, -45]) for (const z of [8 - D, 8 + D])
    out.push(card([8 - HW, Y0], [8 + HW, Y1], z, 'np_skirt', [0, 0, 1, 1], {origin: [8, yc, 8], axis: 'y', angle}));
  return out;
}
function parasolOpen() {
  const C = NP.CANOPY;
  return [
    ...handle(),
    fitting('np_shaft', 'np_gold')([7.72, 10.5, 7.72], [8.28, 20.4, 8.28]),
    // Hub and runner under the lining.
    fitting('np_hub', 'np_gold')([7.36, 13.4, 7.36], [8.64, 15.1, 8.64]),
    // Rim disc: outer face (frill, black-indigo panels) up, lining down; the dome above it is
    // stacked smaller discs, its side view four crossed profile cards (eight ribs).
    disc(C.R, C.RIM, 'np_top', 'np_lining'),
    ...C.STEPS.map(([r, y]) => disc(r, y, 'np_dome', 'np_dome')),
    ...star(C.R, C.Y0, C.Y1, 'np_profile'),
    ...skirt(C.SKIRT),
    ...muzzle(20.3),
  ];
}

export function buildNaviaWeaponGeometry() {
  return {navia_halberd: halberd(), navia_parasol: parasolClosed(), navia_parasol_open: parasolOpen()};
}
