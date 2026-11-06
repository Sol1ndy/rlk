/**
 * Arlecchino's scythe after her signature weapon 붉은 달의 형상 (Crimson Moon's Semblance), which
 * she wields as a dark-red great scythe: a black lacquered haft with crimson pinstripes and
 * dark silver fittings; at the head the crimson moon (an eclipsed blood-red disc in a gold
 * ring) ringed by eight radiating crimson blades on a black sunburst, crowned by a gold point;
 * and a great crescent running from an engraved black spine through deep crimson to a
 * scarlet cutting edge. The infused form (scythe) is larger and its edge burns orange-gold.
 *
 * Outlines are painted (weapon_paint.mjs) and shown on alpha-cut cards: the crescent is one
 * smooth curve on three stacked cards (front, middle, back) instead of a chain of rotated
 * boxes, and the crown is a card on each face of the socket plus one through it.
 *
 * Model frame (unchanged; the motion clips rely on it): grip [8,8,8], shaft along +Y, the
 * hook reaches toward -X, the cutting edge is the lower/inner outline.
 */
import {paintedBox, card, cardX} from './weapon_faces.mjs';
import {CRES, CROWN, TIP} from './weapon_paint.mjs';

export function buildScytheGeometry() {
  const fitting = sprite => (from, to, rotation) => paintedBox(from, to, {
    front: {sprite, u: ['x', from[0], to[0]], v: ['y', to[1], from[1]]},
    side: {sprite, u: ['z', from[2], to[2]], v: ['y', to[1], from[1]]},
    cap: {sprite, uv: [.2, .2, .8, .8]},
  }, rotation);
  const metal = fitting('ar_metal'), gold = fitting('ar_gold'), gem = fitting('ar_gem');

  const shaft = () => [
    paintedBox([7.5, -9, 7.5], [8.5, 23.6, 8.5], {
      front: {sprite: 'ar_shaft', u: ['x', 7.5, 8.5], v: ['y', 23.6, -9]},
      side: {sprite: 'ar_shaft', u: ['z', 7.5, 8.5], v: ['y', 23.6, -9]},
      cap: {sprite: 'ar_metal', uv: [.3, .3, .7, .7]},
    }),
    // Hand wrap and silver ferrules.
    metal([7.32, 5.4, 7.32], [8.68, 6.0, 8.68]),
    metal([7.32, 10.0, 7.32], [8.68, 10.6, 8.68]),
    metal([7.36, 18.8, 7.36], [8.64, 19.3, 8.64]),
    metal([7.3, -7.6, 7.3], [8.7, -6.9, 8.7]),
    // Butt: a tapering silver spike with a blood-red stone.
    metal([7.62, -10.3, 7.62], [8.38, -9, 8.38]),
    metal([7.8, -11.6, 7.8], [8.2, -10.25, 8.2]),
    gem([7.7, -8.95, 7.7], [8.3, -8.35, 8.3], {origin: [8, -8.65, 8], axis: 'y', angle: 45}),
  ];

  // The crescent, scaled by k about its joint with the socket (the smaller physical form).
  const JX = 8.6, JY = 27.9;
  function crescent(k, fire) {
    const sprite = fire ? 'ar_crescent_fire' : 'ar_crescent';
    const sx = x => JX + (x - JX) * k, sy = y => JY + (y - JY) * k;
    return [7.62, 8.0, 8.38].map(z => card([sx(CRES.X0), sy(CRES.Y0)], [sx(CRES.X1), sy(CRES.Y1)], z, sprite));
  }

  function head(fire) {
    const crown = fire ? 'ar_crown_fire' : 'ar_crown', h = CROWN.S / 2;
    const at = z => card([8 - h, CROWN.Y - h], [8 + h, CROWN.Y + h], z, crown);
    return [
      // Socket joining haft and crescent; the crimson moon on both faces and through it.
      metal([6.55, 23.4, 7.1], [9.45, 27.2, 8.9]),
      at(7.04), at(8.0), at(8.96),
      // Gold collar and the gold lance point (two crossed cards), and the rear spur.
      gold([7.3, 26.9, 7.4], [8.7, 27.9, 8.6]),
      card([8 - TIP.HW, TIP.Y0], [8 + TIP.HW, TIP.Y1], 8, 'ar_tip'),
      cardX([8 - TIP.HW, TIP.Y0], [8 + TIP.HW, TIP.Y1], 8, 'ar_tip'),
      // Rear spur: a short silver lug ending in a gold thorn swept back and up.
      metal([8.7, 25.3, 7.5], [10.0, 27.0, 8.5]),
      card([9.2, 25.4], [fire ? 10.8 : 10.4, fire ? 30.2 : 29.0], 8, 'ar_tip', [0, 0, 1, 1],
        {origin: [9.6, 26.0, 8], axis: 'z', angle: -45}),
    ];
  }

  return {
    spear: [...shaft(), ...crescent(.8, false), ...head(false)],
    scythe: [...shaft(), ...crescent(1, true), ...head(true)],
  };
}
