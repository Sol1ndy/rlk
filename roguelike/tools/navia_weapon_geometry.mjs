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
 * with gold fittings and a gold cog. Closed (18 units, after v4 f342 / v2 f291-f297): a gold
 * shaft from the cog to a wide ruffle rosette, the folded black-indigo bundle with a gem plaque
 * tapering to a thin lace collar, and a short gold tip, as crossed cards round core boxes and
 * discs. Open (about 18 across, after v2 f273-f279): a convex eight-rib dome, its flank sixteen
 * tangential cards (gold blue-gem emblems on alternate panels), its cap stacked discs painted
 * in model units with four crossed profile cards (the ribs) for the side view; the gold lining
 * with orange-red paisley under it, a two-tier hanging gold ruffle and a slim gold finial.
 *
 * Model frame (as the other rig weapons; the motion clips rely on it): grip [8,8,8], shaft
 * along +Y, broad faces of the halberd head facing +-Z, its crescent toward -X; the parasol's
 * muzzle and canopy point to +Y. Every coordinate stays within -16..32 and rotations are single
 * axis about Y, 22.5 or 45 degrees.
 */
import {paintedBox, plate, card, cardX} from './weapon_faces.mjs';
import {NV_HEAD, NV_TIP, NV_CRYSTAL, NV_GUARD, NV_BUTT, NV_SLEEVE, NP} from './navia_weapon_paint.mjs';

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
  // Lower ring, crossguard and the faceted sleeve. The sleeve's faces are cut to a pointed cap
  // and a waist (open top; a gold floor inside closes it where the navy shaft enters).
  e.push(gold([7.42, 9.35, 7.42], [8.58, 10.65, 8.58]));
  e.push(...crossed(NV_GUARD.HW, NV_GUARD.Y0, NV_GUARD.Y1, 'nv_guard'));
  const S = NV_SLEEVE, sleeve = fitting('nv_sleeve', 'nv_gold')([8 - S.HW, S.Y0, 8 - S.HW], [8 + S.HW, S.Y1, 8 + S.HW]);
  delete sleeve.faces.up;
  e.push(sleeve);
  // Inner crown turned 45 degrees (half-diagonal 0.735, inside the sleeve faces): its faces
  // carry a lower chevron (nv_sleeve_crown) that fills the notch at the sleeve's corners.
  const cw = .52, crown = paintedBox([8 - cw, 13.5, 8 - cw], [8 + cw, S.APEX2, 8 + cw], {
    front: {sprite: 'nv_sleeve_crown', u: ['x', 8 - cw, 8 + cw], v: ['y', S.APEX2, 13.5]},
    side: {sprite: 'nv_sleeve_crown', u: ['z', 8 - cw, 8 + cw], v: ['y', S.APEX2, 13.5]},
    cap: {sprite: 'nv_gold', uv: [.2, .2, .8, .8]},
  }, {origin: [8, 14, 8], axis: 'y', angle: 45});
  delete crown.faces.up;
  e.push(crown);
  const floor = gold([8 - S.HW + .02, S.SHOULDER - .06, 8 - S.HW + .02], [8 + S.HW - .02, S.SHOULDER + .01, 8 + S.HW - .02]);
  for (const f of ['north', 'south', 'east', 'west', 'down']) delete floor.faces[f];
  e.push(floor);
  // Navy shaft, silver collar, navy shaft with the silver strip.
  e.push(fitting('nv_shaft2', 'nv_gold')([7.5, 14.8, 7.5], [8.5, 17.5, 8.5]));
  e.push(fitting('nv_collar', 'nv_gold')([7.28, 17.4, 7.28], [8.72, 19.1, 8.72]));
  e.push(fitting('nv_shaft1', 'nv_gold')([7.48, 19.0, 7.48], [8.52, 21.2, 8.52]));
  // Gold rose boss with the rose on all four faces.
  e.push(gold([7.5, 21.15, 7.5], [8.5, 22.4, 8.5]));
  e.push(plate(8, 21.78, 1.15, 7.46, 'nv_rose'), plate(8, 21.78, 1.15, 8.54, 'nv_rose'));
  e.push(cardX([7.425, 21.205], [8.575, 22.355], 7.46, 'nv_rose'), cardX([7.425, 21.205], [8.575, 22.355], 8.54, 'nv_rose'));
  // Crystal: two crossed silhouette cards draw the pointed hexagon; a plain opaque core with a
  // diamond cross-section (half-diagonal 0.49) fills it where the hexagon is wider than 0.5.
  e.push(fitting('nv_crystal_core', 'nv_crystal_core', [.3, .3, .7, .5])([7.65, 23.05, 7.65], [8.35, 24.38, 8.35], {origin: [8, 23.7, 8], axis: 'y', angle: 45}));
  e.push(...crossed(NV_CRYSTAL.HW, NV_CRYSTAL.Y0, NV_CRYSTAL.Y1, 'nv_crystal'));
  // Bell collar, socket and the spear point.
  e.push(gold([7.42, 24.75, 7.42], [8.58, 25.15, 8.58]), gold([7.58, 25.1, 7.58], [8.42, 25.5, 8.42]));
  e.push(fitting('nv_socket', 'nv_gold')([7.62, 25.45, 7.62], [8.38, 27.95, 8.38]));
  e.push(...crossed(NV_TIP.HW, NV_TIP.Y0, NV_TIP.Y1, 'nv_tip'));
  // The head on three stacked cards (front, middle, back; weapon.md §11.3).
  for (const z of [7.64, 8.0, 8.36]) e.push(card([NV_HEAD.X0, NV_HEAD.Y0], [NV_HEAD.X1, NV_HEAD.Y1], z, 'nv_head'));
  return e;
}

// ---- parasol -----------------------------------------------------------------------------------
function handle() {
  const gold = fitting('np_gold');
  return [
    // Black crook below the hand (three stacked cards, plus one edge-on card through the bend
    // so the crook keeps its depth from the side), the grip, gold collar and cog.
    ...[7.74, 8.0, 8.26].map(z => card([NP.CROOK.X0, NP.CROOK.Y0], [NP.CROOK.X1, NP.CROOK.Y1], z, 'np_handle')),
    cardX([7.74, 5.3], [8.26, 6.45], 7.85, 'np_shaft'),
    fitting('np_shaft', 'np_gold')([7.66, 6.4, 7.66], [8.34, 9.6, 8.34]),
    gold([7.55, 9.5, 7.55], [8.45, 10.1, 8.45]),
    gold([7.6, 10.05, 7.6], [8.4, 10.55, 8.4], {origin: [8, 10.3, 8], axis: 'y', angle: 45}),
    disc(NP.COG, 10.32, 'np_cog', 'np_cog'),
  ];
}
function parasolClosed() {
  const fold = fitting('np_fold', 'np_fold', [.3, .1, .7, .3]);
  const {ROSETTE: R, BUNDLE: B, TIP: T} = NP;
  return [
    ...handle(),
    // Gold shaft from the cog into the ruffle rosette (about 30% of the hand-to-tip length).
    fitting('np_gshaft', 'np_gold')([7.7, 10.5, 7.7], [8.3, 12.7, 8.3]),
    // The rosette: a wide scalloped ruffle (four crossed cards), its core and three discs.
    ...star(R.HW, R.Y0, R.Y1, 'np_crosette'),
    fitting('np_ruffle', 'np_gold')([7.65, 12.6, 7.65], [8.35, 15.0, 8.35]),
    disc(1.5, 12.5, null, 'np_rosette'), disc(2.4, 13.9, 'np_rosette', 'np_rosette'), disc(1.95, 15.28, 'np_rosette', null),
    // The folded canopy: stepped core inside four crossed profile cards, the gem plaque, the
    // thin lace collar (on the cards) and the short gold tip.
    fold([6.98, 15.3, 6.98], [9.02, 17.3, 9.02]),
    fold([7.16, 17.25, 7.16], [8.84, 19.0, 8.84]),
    fold([7.36, 18.95, 7.36], [8.64, 20.4, 8.64]),
    fold([7.56, 20.35, 7.56], [8.44, 21.4, 8.44]),
    fold([7.7, 21.35, 7.7], [8.3, 22.0, 8.3]),
    ...star(B.HW, B.Y0, B.Y1, 'np_bundle'),
    plate(8, 16.7, 1.2, 6.93, 'np_plaque'),
    ...star(T.HW, T.Y0, T.Y1, 'np_ctip'),
  ];
}
// Sixteen tangential cards round the axis at distance D, every 22.5 degrees about Y: XY cards
// at z = 8 -+ D turned 0, +-22.5 and +-45 degrees, ZY cards at x = 8 -+ D turned 0 and +-22.5.
// pick(kind) names the sprite: 'rib' for the eight cards centred on a rib (0, 45, ... degrees),
// 'a' / 'b' for the panel-centre cards turned +22.5 / -22.5 (they alternate round the ring).
function ring16({D, HW, Y0, Y1}, pick) {
  const o = {origin: [8, (Y0 + Y1) / 2, 8], axis: 'y'}, kind = a => a === 22.5 ? 'a' : a === -22.5 ? 'b' : 'rib', out = [];
  for (const angle of [0, 22.5, -22.5, 45, -45]) for (const z of [8 - D, 8 + D])
    out.push(card([8 - HW, Y0], [8 + HW, Y1], z, pick(kind(angle)), [0, 0, 1, 1], angle ? {...o, angle} : undefined));
  for (const angle of [0, 22.5, -22.5]) for (const x of [8 - D, 8 + D]) {
    const el = cardX([8 - HW, Y0], [8 + HW, Y1], x, pick(kind(angle)));
    if (angle) el.rotation = {...o, angle};
    out.push(el);
  }
  return out;
}
function parasolOpen() {
  const C = NP.CANOPY, gold = fitting('np_gold');
  return [
    ...handle(),
    fitting('np_shaft', 'np_gold')([7.72, 10.5, 7.72], [8.28, 18.9, 8.28]),
    // Runner under the lining; the rim disc (ruffle top up, lining down).
    fitting('np_hub', 'np_gold')([7.36, 13.4, 7.36], [8.64, 15.1, 8.64]),
    disc(C.R, C.RIM, 'np_top', 'np_lining'),
    // The dome: drum flank (emblem / filigree / rib cards), the elliptic cap as stacked discs
    // painted in model units, and four profile cards (the eight ribs) for its side view.
    ...ring16(C.DRUM, k => ({rib: 'np_drum_rib', a: 'np_drum_emb', b: 'np_drum_fil'})[k]),
    ...C.STEPS.map(([r, y], k) => disc(r, y, 'np_dome' + k, null)),
    ...star(C.PROFILE.HW, C.PROFILE.Y0, C.PROFILE.Y1, 'np_profile'),
    // The two-tier ruffle: the long lower tier flares out beyond the upper one, which carries
    // a bow at each rib.
    ...ring16(C.RUFFLE_L, () => 'np_ruffle_l'),
    ...ring16(C.RUFFLE_U, k => k === 'rib' ? 'np_ruffle_ub' : 'np_ruffle_u'),
    // Finial collar on the crown and the slim gold finial (the muzzle).
    gold([7.62, 19.5, 7.62], [8.38, 19.9, 8.38]),
    ...star(C.FINIAL.HW, C.FINIAL.Y0, C.FINIAL.Y1, 'np_finial'),
  ];
}

export function buildNaviaWeaponGeometry() {
  return {navia_halberd: halberd(), navia_parasol: parasolClosed(), navia_parasol_open: parasolOpen()};
}
