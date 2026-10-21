// The Tenma puppet armour of the Raiden rig (악요의 요고우 텐마; 10-22c "갑주" polish): the giant arm (shoulder, upper arm,
// forearm, fist), the naginata, the three thin arms with their hands and the kunai, the two bronze gauntlet hands and
// the disc halo with its crescent horns. raiden_geometry.mjs owns the part table, the pivots and the forward
// kinematics; this module only builds the part models (A-frame of mboss_model_lib.mjs: +X her LEFT, +Y up, -Z forward,
// model units about the display pivot, within -24..24). References: scratchpad rd/src/user_refs/tenma_*.png and
// rd/frames/B (lilac lacquer plates with violet tomoe / eye sigils and dark joints, a dark naginata with gold fittings
// and a long curved blade with a glowing magenta edge, bronze gauntlets with articulated fingers and violet jewels).
//
// Shapes are rounded from box plates: ring() is a closed band of n thick plates about an axis (overlapping bands read
// as lacquered lames), ball() a faceted joint ball, shell() a curved plate of alpha-cut cards (the big outline plates:
// pauldron, vambrace, elbow cop). The painted sprites (raiden_paint.mjs) carry the rims, bevels and sigils; the game's
// face lighting (shade on) does the rest, so the armour reads from every side as the arms swing.
import {abox, cardZ, cardX, cardY, faceEl, rotA, faceOfDir, vadd, vsub, vsc, vdot, mirrorModel} from './mboss_model_lib.mjs';

const AX = {x: [1, 0, 0], y: [0, 1, 0], z: [0, 0, 1]};
const AZ = {y: [[0, 0, -1], [1, 0, 0]], x: [[0, 0, -1], [0, 1, 0]], z: [[0, 1, 0], [1, 0, 0]]};
const cardinal = (axis, phi) => {
  const [e0, e1] = AZ[axis], dirs = [e0, e1, vsc(e0, -1), vsc(e1, -1)], q = Math.round(phi / 90), g = phi - 90 * q;
  return {d: dirs[((q % 4) + 4) % 4], t: dirs[(((q + 1) % 4) + 4) % 4], g};
};
const turnSign = (axis, d, t) => (vdot(rotA(axis, 10, d), t) > 0 ? 1 : -1);

// Closed band of n plates about `axis` through c, from a0 to a1 along the axis, inner radius r, thickness th. The outer
// face of every plate shows the whole sprite (u across the plate, v from a1 (top of the sprite) to a0); the sides and
// ends take `rim`. tex may be a function (k, outward dir) -> sprite (a sigil on one plate).
export function ring(axis, c, a0, a1, r, th, tex, {n = 8, rim = 'sw_jointdk', ends = true, phase = 0, wScale = 1} = {}) {
  const A = AX[axis], R = r + th, w = 2 * R * Math.tan(Math.PI / n) * wScale, els = [];
  for (let k = 0; k < n; k++) {
    const {d, t, g} = cardinal(axis, k * 360 / n + phase);
    const P = (rad, s, a) => vadd(c, vadd(vadd(vsc(d, rad), vsc(t, s)), vsc(A, a)));
    const fn = X => { const rel = vsub(X, c); return [16 * (.5 + vdot(rel, t) / w), 16 * (a1 - vdot(rel, A)) / (a1 - a0)]; };
    const out = g ? rotA(axis, turnSign(axis, d, t) * g, d) : d;                              // the plate's true outward direction
    const faces = {[faceOfDir(d)]: {tex: typeof tex === 'function' ? tex(k, out) : tex, fn}};
    for (const sd of [t, vsc(t, -1)]) faces[faceOfDir(sd)] = {tex: rim};
    if (ends) for (const sd of [A, vsc(A, -1)]) faces[faceOfDir(sd)] = {tex: rim};
    els.push(faceEl([P(r, -w / 2, a0), P(R, w / 2, a1)], faces, {rot: g ? [axis, turnSign(axis, d, t) * g, vadd(c, vsc(A, (a0 + a1) / 2))] : undefined}));
  }
  return els;
}
// Octagonal rod (a square and the same square turned 45 degrees) along `axis` through c, a0..a1, half-size r.
export function octo(axis, c, a0, a1, r, tex) {
  const A = AX[axis], [e0, e1] = AZ[axis];
  const P = (s0, s1, a) => vadd(c, vadd(vadd(vsc(e0, s0), vsc(e1, s1)), vsc(A, a)));
  const lo = P(-r, -r, a0), hi = P(r, r, a1), mid = vadd(c, vsc(A, (a0 + a1) / 2));
  return [abox(lo, hi, tex), abox(lo, hi, tex, {rot: [axis, 45, mid]})];
}
// Faceted joint ball of radius R at c: a 16-plate belt round `axis` and two narrower 8-plate rings above and below it.
export function ball(c, R, tex, {axis = 'y', capTex = tex} = {}) {
  const h = R * .38;
  return [...ring(axis, c, -h, h, R * .78, R * .22, tex, {n: 16, rim: capTex}),
    ...ring(axis, c, h * .9, R * .8, R * .5, R * .26, capTex, {rim: capTex}),
    ...ring(axis, c, -R * .8, -h * .9, R * .5, R * .26, capTex, {rim: capTex})];
}
// Small rounded knob (three crossed boxes) for the thin joints.
export function knob(c, R, tex, k = .66) {
  const b = (x, y, z) => abox([c[0] - x, c[1] - y, c[2] - z], [c[0] + x, c[1] + y, c[2] + z], tex);
  return [b(R, R * k, R * k), b(R * k, R, R * k), b(R * k, R * k, R)];
}
// Curved plate about the Y axis (through c): a centre card facing `side` ('-x', '+x', '-z', '+z') at distance R and
// width wc, flanked by cards of width ws turned in by 22.5 degrees (and a second pair by 45 with ws2): one alpha-cut
// sprite spread across the cards (u along the unrolled width, v from y1 (top) to y0). Every card shows both faces.
export function shell(sprite, side, R, wc, ws, y0, y1, {c = [0, 0, 0], ws2 = 0, flipU = false} = {}) {
  const sgn = side[0] === '-' ? -1 : 1, ax = side[1], d = ax === 'x' ? [sgn, 0, 0] : [0, 0, sgn];
  const t = ax === 'x' ? [0, 0, -sgn] : [sgn, 0, 0];         // u runs along t (left to right seen from outside)
  const W = wc + 2 * ws + 2 * ws2, els = [], O = vadd(c, vsc(d, R));
  const card = (s0, s1, rot) => {
    const fn = X => { const s = vdot(vsub(X, O), t); const u = (s + W / 2) / W; return [16 * (flipU ? 1 - u : u), 16 * (y1 - (X[1] - c[1])) / (y1 - y0)]; };
    const P = (s, y) => vadd(O, vadd(vsc(t, s), [0, y, 0]));
    return faceEl([P(s0, y0), P(s1, y1)], {[faceOfDir(d)]: {tex: sprite, fn}, [faceOfDir(vsc(d, -1))]: {tex: sprite, fn}}, {shade: true, rot});
  };
  els.push(card(-wc / 2, wc / 2));
  for (const e of [1, -1]) {
    // hinge at the centre card's edge; the side card lies on in the plane, then turns in toward the axis
    const hinge = vadd(O, vsc(t, e * wc / 2)), ym = c[1] + (y0 + y1) / 2;
    const sg = vdot(rotA('y', 10, vsc(t, e)), vsc(d, -1)) > 0 ? 1 : -1;
    els.push(card(e > 0 ? wc / 2 : -wc / 2 - ws, e > 0 ? wc / 2 + ws : -wc / 2, ['y', sg * 22.5, [hinge[0], ym, hinge[2]]]));
    if (ws2) {
      // the outer pair: its hinge is the turned card's far edge, turned 45 degrees in all
      const far = vadd(hinge, vadd(vsc(vsc(t, e), ws * Math.cos(Math.PI / 8)), vsc(d, -ws * Math.sin(Math.PI / 8))));
      const O2 = far, t2 = vsc(t, e), d2 = d;
      const fn2 = X => { const s = e * (wc / 2 + ws) + e * vdot(vsub(X, O2), t2); const u = (s + W / 2) / W; return [16 * (flipU ? 1 - u : u), 16 * (y1 - (X[1] - c[1])) / (y1 - y0)]; };
      const P2 = (s, y) => vadd(O2, vadd(vsc(t2, s), [0, y, 0]));
      els.push(faceEl([P2(0, y0), P2(ws2, y1)], {[faceOfDir(d2)]: {tex: sprite, fn: fn2}, [faceOfDir(vsc(d2, -1))]: {tex: sprite, fn: fn2}},
        {shade: true, rot: ['y', sg * 45, [far[0], ym, far[2]]]}));
    }
  }
  return els;
}
// A finger (or thumb) of box segments from p along dir0 (width along wv, thickness along hv), every segment turned
// about `axis` through its own start: the first by `base` degrees, each next one `curl` further (a chain of hinges,
// segment i starts where segment i-1 ends; the turns stay within +-45). Dark joint collars between the segments.
function finger(p, lens, w, h, tex, {axis, base = 0, curl = [], joint = null, taper = .9, dir0, wv, hv}) {
  const els = [];
  let start = p, ang = base, ww = w, hh = h;
  lens.forEach((L, i) => {
    if (i > 0) ang += curl[i - 1] || 0;
    if (Math.abs(ang) > 45) throw new Error('finger turn ' + ang);
    const rot = ang ? {rot: [axis, ang, start]} : {};
    els.push(abox(vadd(start, vadd(vsc(wv, -ww / 2), vsc(hv, -hh / 2))), vadd(start, vadd(vsc(dir0, L), vadd(vsc(wv, ww / 2), vsc(hv, hh / 2)))), tex, rot));
    if (joint && i > 0) els.push(abox(vadd(start, vadd(vsc(dir0, -.25), vadd(vsc(wv, -ww * .56), vsc(hv, -hh * .56)))),
      vadd(start, vadd(vsc(dir0, .45), vadd(vsc(wv, ww * .56), vsc(hv, hh * .56)))), joint, rot));
    start = vadd(start, rotA(axis, ang, vsc(dir0, L)));
    ww *= taper; hh *= taper;
  });
  return els;
}

// ---- disc halo and the crescent horns (scale 1; pivot behind the head; the disc faces -Z) ------------------------------
function discModel() {
  return [
    cardZ('halo_ring', 1.6, {X0: -17.4, X1: 17.4, Y0: -17.4, Y1: 17.4}),                       // thin outer ring, 2.2 b
    cardZ('disc', -.45, {X0: -11.2, X1: 11.2, Y0: -11.2, Y1: 11.2}),                           // tomoe-eye disc, 1.4 b
    ...ring('z', [0, 0, 0], -.35, .55, 10.2, .9, 'sw_discrim', {n: 16, rim: 'sw_violet'}),      // its rim
    cardZ('disc_back', .5, {X0: -10.6, X1: 10.6, Y0: -10.6, Y1: 10.6}),                       // dark round back
    cardZ('horn', 1.0, {X0: -17.5, X1: -5.0, Y0: -6, Y1: 23.5}, {flipU: true}), cardZ('horn', 1.3, {X0: -17.3, X1: -5.2, Y0: -5.7, Y1: 23.2}, {flipU: true}),
    cardZ('horn', 1.0, {X0: 5.0, X1: 17.5, Y0: -6, Y1: 23.5}), cardZ('horn', 1.3, {X0: 5.2, X1: 17.3, Y0: -5.7, Y1: 23.2}),
  ];
}

// ---- the giant arm (her RIGHT: outward = -X). Scale 1.5 (1 unit = 0.094 b); upper arm and forearm 21.3 units --------
const LAME = 'lac_lame', SIG = 'lac_lame_sig', JOINT = 'sw_jointdk';
// a plate band whose outward plate (the one facing `out`) carries the sigil
const sigOn = out => (k, d) => (vdot(d, out) > .98 ? SIG : LAME);
function giantUpper() {
  return [
    ...ball([0, 0, 0], 4.4, 'lac_joint', {capTex: JOINT}),                                        // shoulder ball
    ...ring('y', [0, 0, 0], 1.6, 4.6, 5.0, 1.0, LAME, {rim: JOINT, n: 16}),                       // shoulder cap, domed:
    ...ring('y', [0, 0, 0], 4.4, 5.6, 3.6, 1.1, LAME, {rim: 'sw_lacquer', n: 16}),                // a narrower ring and a lid
    ...octo('y', [0, 0, 0], 5.4, 6.2, 3.1, 'sw_lacquer'),
    ...octo('y', [0, 0, 0], -21.3, 1.0, 3.3, JOINT),                                              // core (seen in the seams)
    ...ring('y', [0, 0, 0], -7.4, 2.0, 5.6, 1.1, LAME, {n: 16}),                                  // upper arm lames, the upper
    ...ring('y', [0, 0, 0], -13.4, -6.8, 4.7, .9, LAME, {n: 16}),                                 // one over the lower one
    ...ring('y', [0, 0, 0], -18.6, -12.8, 3.9, .8, LAME, {n: 16}),
    // the great pauldron: a crested plate hugging the front and the outer side of the upper arm (her facing side,
    // toward her right), its crest rising over the shoulder, and a lateral plate on the outer side under it
    ...shell('lac_shell', '-z', 7.2, 5.6, 4.2, -17, 14, {c: [-1.2, 0, 0], ws2: 4.4}),
    ...shell('lac_shell2', '-x', 7.4, 6.4, 3.8, -19, -1),
  ];
}
function giantFore() {
  return [
    ...ball([0, 0, 0], 3.7, 'lac_joint', {capTex: JOINT}),                                        // elbow ball
    ...shell('lac_cop', '-x', 5.4, 6.4, 4.2, -5.5, 6.5),                                            // elbow cop (outer)
    ...octo('y', [0, 0, 0], -21.3, -2.0, 2.9, JOINT),                                             // core
    ...ring('y', [0, 0, 0], -8.6, -2.6, 4.6, .9, LAME, {n: 16}),                                  // vambrace lames, narrowing
    ...ring('y', [0, 0, 0], -14.2, -8.0, 3.8, .8, sigOn([0, 0, -1]), {n: 16}),
    ...ring('y', [0, 0, 0], -19.4, -13.6, 3.1, .7, LAME, {n: 16}),
    ...shell('lac_guard', '-x', 6.2, 6.0, 4.0, -19.6, -4.4),                                       // long outer guard plate
  ];
}
// Fist round the shaft: the shaft runs along X at Y -7.09 (gWrist 0.62 b at scale 1.4), Z 0; +Y is the wrist.
function giantFist() {
  const sy = -7.09, e = [];
  e.push(...ring('y', [0, 0, 0], -1.6, 1.4, 3.2, .9, 'lac_lame', {rim: JOINT}));                  // wrist cuff
  e.push(abox([-4.7, -5.2, -2.9], [4.7, -1.2, 2.9], {all: 'lac_hand', up: JOINT}));              // hand body
  e.push(abox([-4.3, -4.6, -3.25], [4.3, -1.8, -2.9], 'lac_lame_sig'));                          // back-of-hand plate
  for (let i = 0; i < 4; i++) {
    const x = -3.45 + i * 2.3, w = 2.05;
    e.push(abox([x - w / 2, -9.0, -3.1], [x + w / 2, -4.8, -1.1], {all: 'lac_hand', down: JOINT}));   // front phalanges, down past the shaft
    e.push(abox([x - w * .55, -6.0, -3.35], [x + w * .55, -4.6, -2.0], JOINT));                         // knuckle
    e.push(abox([x - w / 2, -10.3, -2.6], [x + w / 2, -8.7, 1.2], 'lac_hand'));                         // under the shaft
    e.push(abox([x - w * .45, -9.6, 1.2], [x + w * .45, sy + .2, 2.6], 'lac_hand'));                    // curled behind
  }
  e.push(abox([2.4, -6.8, 1.2], [4.8, -3.6, 3.6], 'lac_hand'), abox([1.0, sy + 1.6, .6], [4.0, sy + 3.2, 2.8], 'lac_hand'));   // thumb over the shaft
  return e;
}

// ---- the naginata (scale 3.6: 1 unit = 0.225 b). Grip at the pivot, shaft along +Y, blade toward +Y with the edge
// toward +X; butt -7.1, blade 10.2..21.9 (tip at about [1.4, 21.8] as before). ----------------------------------------
function glaiveModel() {
  const e = [...octo('y', [0, 0, 0], -6.6, 10.4, .44, 'glaive_shaft')];
  for (const [y0, y1] of [[-6.9, -6.1], [-2.5, -2.0], [2.0, 2.5], [6.6, 7.1]]) e.push(...octo('y', [0, 0, 0], y0, y1, .62, 'sw_gold'));
  e.push(...octo('y', [0, 0, 0], -8.0, -6.9, .5, 'sw_golddk'), abox([-.2, -8.9, -.2], [.2, -8.0, .2], 'sw_gold'));   // butt cap and spike
  e.push(...octo('y', [0, 0, 0], 9.2, 10.4, .72, 'sw_gold'));                                                        // collar
  e.push(cardZ('glaive_guard', -.02, {X0: -1.6, X1: 1.6, Y0: 8.4, Y1: 11.6}), cardX('glaive_guard', 0, {Z0: -1.6, Z1: 1.6, Y0: 8.4, Y1: 11.6}));
  e.push(cardZ('glaive_blade', 0, {X0: -.7, X1: 2.9, Y0: 10.2, Y1: 22.0}));                                           // the curved blade
  e.push(abox([-.62, 10.2, -.16], [-.12, 15.2, .16], 'sw_bladespine'));                                            // spine near the collar
  return e;
}
const glaiveFx = () => [cardZ('glaive_glow', -.13, {X0: .9, X1: 3.7, Y0: 10.6, Y1: 22.2}), cardX('glaive_glow', 2.3, {Z0: -1.4, Z1: 1.4, Y0: 10.6, Y1: 22.2})];

// ---- the thin arms (her LEFT). Upper arm scale 1 (20.8 units = 1.3 b); forearm + hand scale 1.25 --------------------
function thinUpper() {
  return [...knob([0, 0, 0], 2.1, 'lac_joint'),
    ...octo('y', [0, 0, 0], -20.8, -1.0, .95, JOINT),
    ...ring('y', [0, 0, 0], -9.4, -1.2, 1.55, .6, LAME),                                         // one plate, tapering
    ...ring('y', [0, 0, 0], -17.6, -9.0, 1.2, .55, sigOn([0, 0, -1]))];
}
// forearm (elbow at the pivot) and hand; kind: 'kunai' (fist round a kunai pointing on past it), 'open' (splayed),
// 'reach' (splayed, fingers bent forward)
function thinFore(kind) {
  const e = [...knob([0, 0, 0], 1.85, 'lac_joint'),
    ...shell('lac_cop', '-z', 1.9, 2.4, 1.6, -2.6, 2.4),                                              // elbow cop
    ...octo('y', [0, 0, 0], -11.4, -1.0, .8, JOINT),
    ...ring('y', [0, 0, 0], -10.6, -1.4, 1.2, .55, sigOn([0, 0, -1]))];
  const wy = -11.8;
  e.push(...knob([0, wy, 0], 1.2, 'lac_joint'));
  if (kind === 'kunai') {
    e.push(abox([-1.7, wy - 4.6, -1.0], [1.7, wy - .8, 1.1], 'lac_hand'));                         // fist
    for (let i = 0; i < 4; i++) { const x = -1.27 + i * .85; e.push(abox([x - .38, wy - 4.4, -1.55], [x + .38, wy - 1.4, -.9], {all: 'lac_hand', front: JOINT})); }
    e.push(abox([1.4, wy - 3.2, -.9], [2.1, wy - 1.0, .6], 'lac_hand'));                            // thumb
    // the kunai: grip through the fist, ring pommel behind it, the blade on past the fist
    e.push(...octo('y', [0, 0, 0], wy - 5.4, wy + .6, .32, 'glaive_shaft'));
    e.push(abox([-.75, wy + .6, -.18], [.75, wy + 1.9, .18], 'sw_gold'));
    e.push(...octo('y', [0, 0, 0], wy - 6.0, wy - 5.2, .62, 'sw_gold'));
    e.push(cardZ('kunai', 0, {X0: -1.7, X1: 1.7, Y0: -24, Y1: wy - 5.6}), cardX('kunai', 0, {Z0: -1.7, Z1: 1.7, Y0: -24, Y1: wy - 5.6}));
    return e;
  }
  // open hand: palm, four splayed two-segment fingers, the thumb out to the side
  e.push(abox([-1.75, wy - 4.4, -.6], [1.75, wy - .7, .65], {all: 'lac_hand', front: 'lac_palm'}));
  const fx = [-1.3, -.44, .44, 1.3], H = {dir0: [0, -1, 0], wv: [1, 0, 0], hv: [0, 0, 1], joint: JOINT};
  fx.forEach((x, i) => {
    const outer = i === 0 || i === 3, L = [[2.9, 2.3], [3.3, 2.6], [3.4, 2.7], [3.0, 2.4]][i];
    // open: the four fingers splay (the outer two turned 22.5 degrees out); reach: the middle two bend forward
    if (kind === 'reach' && !outer) e.push(...finger([x, wy - 4.3, 0], L, .72, .8, 'lac_hand', {...H, axis: 'x', base: 22.5, curl: [22.5]}));
    else e.push(...finger([x, wy - 4.3, 0], L, .72, .8, 'lac_hand', {...H, axis: 'z', base: outer ? (i ? 22.5 : -22.5) : 0}));
  });
  e.push(...finger([1.7, wy - 1.8, 0], [2.2, 1.8], .7, .75, 'lac_hand', {...H, axis: 'z', base: 45, curl: [-22.5]}));
  return e;
}

// ---- bronze gauntlets (scale 2: 1 unit = 0.125 b). Pivot at the palm centre, palm up (+Y), fingers forward (-Z), the
// wrist toward +Z; her LEFT hand (the thumb out to +X); the right one is the mirror image. ----------------------------
function gauntletModel() {
  const BR = 'bronze', BD = 'sw_bronzedk', e = [];
  e.push(abox([-3.5, -1.7, -3.1], [3.5, 0, 2.5], {all: BR, up: 'bronze_palm'}));                   // palm slab
  e.push(abox([-3.2, -2.3, -2.7], [3.2, -1.6, 2.2], BD));                                          // back plate
  e.push(abox([1.3, -1.3, -.6], [3.75, .7, 2.6], BR), abox([-3.7, -1.3, .2], [-1.6, .45, 2.5], BR));   // thumb and heel mounds
  e.push(...ring('z', [0, -.25, 0], 2.3, 7.8, 1.5, .55, k => (k === 0 ? 'bronze_jewel' : BR), {rim: BD}));   // wrist cuff
  e.push(...ring('z', [0, -.25, 0], 6.9, 8.2, 1.85, .45, BD, {rim: BD}));
  e.push(...ring('z', [0, -.25, 0], 2.0, 3.0, 1.85, .4, BD, {rim: BD}));
  e.push(...octo('z', [0, -.25, 0], 7.6, 8.4, 1.6, BD));                                            // the cuff's end
  e.push(abox([-.85, 1.75, 3.6], [.85, 2.5, 5.4], 'jewel'));                                       // the wrist jewel
  const fx = [-2.6, -.87, .87, 2.6], lens = [[3.2, 2.5, 2.0], [3.6, 2.8, 2.2], [3.4, 2.7, 2.1], [2.8, 2.2, 1.8]];
  const F = {dir0: [0, 0, -1], wv: [1, 0, 0], hv: [0, 1, 0], joint: BD, taper: .92};
  fx.forEach((x, i) => e.push(...finger([x, -.85, -3.0], lens[i], 1.55, 1.5, BR, {...F, axis: 'x', base: 0, curl: [22.5, 22.5]})));
  e.push(...finger([3.4, -.4, -.4], [2.6, 2.2], 1.45, 1.4, BR, {...F, axis: 'y', base: -45, curl: [22.5]}));
  e.push(cardY('sigil', .07, {X0: -2.2, X1: 2.2, Z0: -2.6, Z1: 1.8}));                             // palm eye
  return e;
}

export function tenmaModels() {
  const M0 = {};
  M0.disc = discModel();
  M0.g_upper = giantUpper();
  M0.g_fore = giantFore();
  M0.g_hand = giantFist();
  M0.glaive = glaiveModel();
  M0.glaive_fx = glaiveFx();
  M0.ra_up = thinUpper();
  M0.ra1_fo = thinFore('kunai');
  M0.ra2_fo = thinFore('open');
  M0.ra3_fo = thinFore('reach');
  M0.gaunt_l = gauntletModel();
  M0.gaunt_r = mirrorModel(gauntletModel());
  return M0;
}
// The puppet's outline for the blink silhouettes (build_raiden_movement.py reads it from the manifest, where
// build_raiden_rig.mjs writes these points solved in the Tenma rest pose): polylines of [part, A-frame model point] with
// the fragment thickness in blocks, and the disc halo (its pivot and radius).
export const GHOST = {
  limbs: [
    {pts: [['g_upper', [0, 0, 0]], ['g_fore', [0, 0, 0]], ['g_hand', [0, -6, 0]]], th: .55},          // giant arm
    {pts: [['g_upper', [-1.2, 12, -7.2]], ['g_upper', [-1.2, -14, -7.2]]], th: .9},                 // the pauldron
    {pts: [['glaive', [0, -8.9, 0]], ['glaive', [0, 10.3, 0]]], th: .12},                          // shaft
    {pts: [['glaive', [0, 10.3, 0]], ['glaive', [1.0, 16.6, 0]], ['glaive', [.35, 21.95, 0]]], th: .26},   // blade
    {pts: [['ra1_up', [0, 0, 0]], ['ra1_fo', [0, 0, 0]], ['ra1_fo', [0, -24, 0]]], th: .16},        // thin arms (kunai)
    {pts: [['ra2_up', [0, 0, 0]], ['ra2_fo', [0, 0, 0]], ['ra2_fo', [0, -19, 0]]], th: .16},
    {pts: [['ra3_up', [0, 0, 0]], ['ra3_fo', [0, 0, 0]], ['ra3_fo', [0, -19, 0]]], th: .16},
    {pts: [['gaunt_l', [0, 0, 8]], ['gaunt_l', [0, 0, -2]], ['gaunt_l', [0, 1, -9]]], th: .55},     // gauntlets
    {pts: [['gaunt_r', [0, 0, 8]], ['gaunt_r', [0, 0, -2]], ['gaunt_r', [0, 1, -9]]], th: .55},
  ],
  disc: {part: 'disc', radius: .78},
};
