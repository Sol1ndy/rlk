/**
 * Skirk's sword after her signature weapon 창백한 섬광 (Azurelight): "once pure and pristine as
 * a white dawn star, since tinted a deep, dark blue". When she wields it, wings grow at the
 * grip, so the guard is a pair of swept, layered feather wings.
 *
 * The outlines are painted (weapon_paint.mjs) and shown on alpha-cut cards, so the point,
 * the taper and the feathers are smooth curves instead of stepped boxes:
 *  - blade: a card on each broad face (silhouette, silver edges, deep-blue body, dawn-white
 *    fuller and root, star glints) around a thin core of boxes that gives it thickness;
 *  - guard: three stacked wing cards around a small navy hub, a dawn-star gem on each face;
 *  - grip: navy wrap with silver diamonds and ferrules; pommel: a star gem in a navy diamond.
 *
 * Model frame (unchanged; the motion clips rely on it): grip [8,8,8], blade along +Y, broad
 * faces facing +-Z, the two edges at +-X. The ice-infused form (cryo_sword) shares the
 * silhouette with brighter, colder sprites.
 */
import {paintedBox, plate, card} from './weapon_faces.mjs';
import {SK, skProfile, WING} from './weapon_paint.mjs';

export function buildSkirkWeaponGeometry() {
  function build(cryo) {
    const S = n => (cryo && ['sk_blade', 'sk_side', 'sk_star', 'sk_wing'].includes(n) ? n + '_cryo' : n);
    const e = [];
    const metal = (from, to, rotation) => e.push(paintedBox(from, to, {
      front: {sprite: 'sk_guard', u: ['x', from[0], to[0]], v: ['y', to[1], from[1]]},
      side: {sprite: 'sk_guard', u: ['z', from[2], to[2]], v: ['y', to[1], from[1]]},
      cap: {sprite: 'sk_guard', u: ['x', from[0], to[0]], v: ['z', from[2], to[2]]},
    }, rotation));

    // Grip: navy wrap with silver diamonds; silver ferrules at both ends.
    e.push(paintedBox([7.45, 3.2, 7.45], [8.55, 10.0, 8.55], {
      front: {sprite: 'sk_grip', u: ['x', 7.45, 8.55], v: ['y', 10.0, 3.2]},
      side: {sprite: 'sk_grip', u: ['z', 7.45, 8.55], v: ['y', 10.0, 3.2]},
      cap: {sprite: 'sk_guard', uv: [.3, .3, .7, .7]},
    }));
    metal([7.3, 9.55, 7.3], [8.7, 10.25, 8.7]);
    metal([7.3, 2.75, 7.3], [8.7, 3.35, 8.7]);
    // Pommel: a dawn-star gem set in a small diamond of navy steel.
    metal([7.25, 1.15, 7.42], [8.75, 2.65, 8.58], {origin: [8, 1.9, 8], axis: 'z', angle: 45});
    e.push(plate(8, 1.9, 1.55, 7.38, S('sk_star'), {origin: [8, 1.9, 7.38], axis: 'z', angle: 45}));
    e.push(plate(8, 1.9, 1.55, 8.62, S('sk_star'), {origin: [8, 1.9, 8.62], axis: 'z', angle: 45}));

    // Blade. Core: thin boxes inside the painted outline (62% of its width), their broad faces
    // mapped exactly like the cards; the cards sit just outside and draw the true silhouette.
    const {CX, HM, ROOT, TIP} = SK;
    const DEPTH = .085, CARD_Z = .1;
    const bladeMap = {sprite: S('sk_blade'), u: ['x', CX - HM, CX + HM], v: ['y', TIP, ROOT]};
    const n = 10, end = .9;
    for (let i = 0; i < n; i++) {
      const t0 = end * i / n, t1 = end * (i + 1) / n;
      const half = .62 * HM * Math.min(skProfile(t0), skProfile(t1));
      const y0 = ROOT + (TIP - ROOT) * t0 - (i ? .02 : 0), y1 = ROOT + (TIP - ROOT) * t1 + .02;
      const depth = DEPTH * (1 - .35 * t0);
      e.push(paintedBox([CX - half, y0, 8 - depth], [CX + half, y1, 8 + depth], {
        front: bladeMap,
        side: {sprite: S('sk_side'), u: ['z', 8 - depth, 8 + depth], v: ['y', TIP, ROOT]},
        cap: {sprite: S('sk_side'), uv: [0, .9, 1, 1]},
      }));
    }
    e.push(card([CX - HM, ROOT], [CX + HM, TIP], 8 - CARD_Z, S('sk_blade')));
    e.push(card([CX - HM, ROOT], [CX + HM, TIP], 8 + CARD_Z, S('sk_blade')));

    // Guard: a small navy hub and collar, the wings on three stacked cards (front, middle,
    // back) so they keep some body from an angle, and the star gem crowning each face.
    metal([6.95, 10.05, 7.62], [9.05, 11.75, 8.38]);
    metal([7.2, 11.6, 7.7], [8.8, 12.2, 8.3]);
    for (const z of [7.58, 8.0, 8.42]) e.push(card([WING.X0, WING.Y0], [WING.X1, WING.Y1], z, S('sk_wing')));
    metal([6.95, 9.75, 7.16], [9.05, 11.85, 8.84], {origin: [8, 10.8, 8], axis: 'z', angle: 45});
    e.push(plate(8, 10.8, 2.2, 7.12, S('sk_star'), {origin: [8, 10.8, 7.12], axis: 'z', angle: 45}));
    e.push(plate(8, 10.8, 2.2, 8.88, S('sk_star'), {origin: [8, 10.8, 8.88], axis: 'z', angle: 45}));
    return e;
  }
  return {sword: build(false), cryo_sword: build(true)};
}
