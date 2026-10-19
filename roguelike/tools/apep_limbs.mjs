// LIMBS region of the 아펩의 오아시스 파수꾼 rig (plan R4 parts 22-39 minus the hands, 48-49; model_p3.md §0 item 2: the six
// phase-3 arms ARE the six phase-1 limbs): the upper and lower segments of the three limb pairs and the bead vines.
//   A (a_up, a_lo)   P1 the long pale shell arms (model.md §3.3): overlapping pale shell plates with dark contour rims (a
//                    beetle leg / folded leaf), a raised inner panel, rows of cream leaf scales on the inner face, the
//                    shoulder plate darkening into the hump; the forearm broadens into a paddle toward the claw (v1 f290)
//                    P3 the raised "antler" arms: a slim shell clad in lime leaf blades on both sides (dark backs), a gold
//                    elbow cone, a white bell vine along the upper arm (model_p3 §2.3 items 13-14, v6 f480)
//   B (b_up, b_lo)   P1 the front legs (model.md §3.4): dark armour plates on the upper leg fading to pale bark at the
//                    foot, overlapping leaf plates, a knee guard turned out, an ankle cuff over the petal foot
//                    P3 the middle arms: a tall section, the dark glossy carapace on the top and back with a lime rim
//                    (v5 f1908), lime leaf scales in front with grey-lilac under-leaves, a gold elbow cone
//   C (c_up, c_lo)   P1 the rear legs (as B, smaller) | P3 the lower arms: broad, shaggy with flared lime leaf scales over
//                    a pale shell, white bell vines over the hips (v6 f480)
//   beads            P3 only: two thin dark-green vines with rows of white lily-of-the-valley bells and small leaflets
//                    (P1: the empty model)
// Construction. Every segment is a chain of PLATES: short 16-gon prisms (one loft section each) about the bone, each a
// little inside its neighbour, with a dark rim cap at the step (the plate edges). Each plate shows one row of a WRAP
// sprite (u = round the bone, v = along the plate), so the paint knows the facet angle: theta 0 = model +X, 90 = model
// front (-Z), 180 = -X, -90 = back. Overlays (leaf blades, carapace plates, knee guards) are two-sided cards with a
// front and a back sprite on one element.
// Frames (apep_pose FRAMES): every limb segment is authored in its bone frame 'y': model -Y along the bone from the joint
// toward the next joint, model -Z toward the world front at the reference stance (P1 CROUCH, P3 UPRIGHT). Measured axes
// (left side): P1 a_up +X up-out, a_lo +X out-up, b_up +X up-out, b_lo +X out, c_up +X up, c_lo +X out; P3 a_* +X
// toward the midline (the inner side of the raised arm), b_* +X up, c_up +X up, c_lo +X out-up. The right side is the
// mirror image of the left (mirrorX). Region interface: see apep_body.mjs.
import {loft, toUnits, mirrorX, registerTile, registerWrap} from './mboss_shape_lib.mjs';
import {cardX, cardZ, abox} from './mboss_model_lib.mjs';
import {PART_SCALE, J} from './apep_pose.mjs';
import {PAL, C, clamp, smooth, mix, N, lift, sink, autoSlot, sprite, onRect, spriteSize, sdLeaf, cone, cells, TRANSPARENT} from './apep_materials.mjs';

export const REGION = 'limbs';
export const PARTS = ['a_up_l', 'a_up_r', 'a_lo_l', 'a_lo_r', 'b_up_l', 'b_up_r', 'b_lo_l', 'b_lo_r', 'c_up_l', 'c_up_r', 'c_lo_l', 'c_lo_r', 'beads_l', 'beads_r'];
const dist = (a, b) => Math.hypot(...a.map((v, i) => v - b[i]));
const LEN = {};
for (const L of ['a', 'b', 'c']) { LEN[`${L}_up`] = dist(J[`${L}_up_l`], J[`${L}_lo_l`]); LEN[`${L}_lo`] = dist(J[`${L}_lo_l`], J[`${L}_hand_l`]); }
const SP = {};

// ---- wrap sprites: rows of plate paint (u round the bone, v along one plate) -------------------------------------------------
// theta of a sprite column s (0..1): facet k spans s in [k / 16, (k + 1) / 16] and faces theta = k * 22.5 deg
const thOf = s => { let th = s * 360 - 11.25; if (th > 180) th -= 360; return th; };
// A wrap sprite of `rows` plate variants (each W x Hr px), painted by fn(theta, t (0 proximal .. 1 distal), row) -> rgba
function wrapSprite(name, W, Hr, rows, fn, forms, use = 'unique') {
  registerTile(name, W, Hr * rows, 32); registerWrap(name);
  SP[name] = sprite(W, Hr * rows, 32, (s, t) => { const r = Math.min(rows - 1, Math.floor(t * rows)); return fn(thOf(s), t * rows - r, r) || TRANSPARENT; }, forms, 'limbs', {use});
  return {name, rows};
}
// remap the v range of every face showing `spr` to row `row` (wrap facets use the whole v range 0..16)
function toRow(els, spr, row) {
  const k = 16 / spr.rows, v0 = row * k;
  for (const e of els) for (const f of Object.values(e.faces)) if (f.texture === '#' + spr.name) { f.uv = [f.uv[0], +(v0 + f.uv[1] / spr.rows).toFixed(4), f.uv[2], +(v0 + f.uv[3] / spr.rows).toFixed(4)]; }
  return els;
}
// a small tile (rims, caps, edges)
function tile(name, w, h, ppb, fn, forms, use = 'unique') { registerTile(name, w, h, ppb); SP[name] = sprite(w, h, ppb, (s, t) => fn(s, t) || TRANSPARENT, forms, 'limbs', {use}); return name; }
// a card sprite over a shape rect (blocks; painter in rect coordinates, v up)
function card(name, rect, ppb, fn, forms) { const [w, h] = spriteSize(rect, ppb); SP[name] = sprite(w, h, ppb, onRect(rect, fn), forms, 'limbs'); return name; }

// ---- plates ---------------------------------------------------------------------------------------------------------------
// plates(L, list, spr, rim): list of {t0, t1 (fractions of the bone length from the joint), r [e1+ (model +X), e2+ (front),
// e1-, e2- (back)], c [c1, c2] section centre, row}. Caps: the distal end when the next plate is smaller (or last), the
// proximal end when the previous one is smaller.
const R4 = r => (Array.isArray(r) ? r : [r, r, r, r]);
const sup = r => Math.max(...R4(r));
function plates(L, list, spr, rim, {seed = 0, tex = null, lastCap = true} = {}) {
  const els = [];
  list.forEach((p, i) => {
    const prev = list[i - 1], next = list[i + 1];
    let caps = '';
    if (prev && sup(prev.r) < sup(p.r) - .005) caps += '-';
    if (next ? sup(next.r) < sup(p.r) + .005 : lastCap) caps += '+';
    const st = [{a: -p.t0 * L, r: R4(p.r), c: p.c || [0, 0]}, {a: -p.t1 * L, r: R4(p.r), c: p.c || [0, 0]}];
    const e = loft('y', st, {n: 16, tex: tex || spr.name, caps, ledgeTex: rim, seed: seed + i * 7});
    els.push(...toRow(e, spr, p.row || 0));
  });
  return els;
}
// a two-sided card (one element): plane 'z' rect {u0, u1 = X, v0, v1 = Y}, `front` on the -Z face; plane 'x' rect {u0, u1
// = Z, v0, v1 = Y}, `front` on the +X face. rot [axis, deg, pivot] (A-frame, 22.5 deg steps).
function card2(plane, at, rect, front, back, rot = null, {flipU = false} = {}) {
  const el = plane === 'z' ? cardZ(front, at, {X0: rect.u0, X1: rect.u1, Y0: rect.v0, Y1: rect.v1}, {rot, shade: true, flipU})
    : cardX(front, at, {Z0: rect.u0, Z1: rect.u1, Y0: rect.v0, Y1: rect.v1}, {rot, shade: true, flipU});
  el.faces[plane === 'z' ? 'south' : 'east'].texture = '#' + back;
  return el;
}

// ---- paint helpers --------------------------------------------------------------------------------------------------------
const line = (d, w) => clamp(1 - Math.abs(d) / w);          // 1 on a line of half width w, 0 off it
// staggered scale rows: (x, y) in scale cells, pointing toward +y; returns {inside, edge, w, fy, id, fx}
function scale(x, y, {p = .8, wid = .48} = {}) {
  const r = Math.floor(y), xo = x + (r % 2 ? .5 : 0), ci = Math.floor(xo), fx = xo - ci, fy = y - r;
  const w = wid * Math.pow(Math.max(0, Math.sin(Math.PI * Math.min(1, fy * .9 + .1))), p);
  const dx = Math.abs(fx - .5);
  return {inside: dx < w, edge: w - dx, w, fy, fx, id: (((ci * 7 + r * 13) % 11) + 11) % 11 / 11};
}

// ---- phase 1 paint --------------------------------------------------------------------------------------------------------
// The pale shell plate (A arms): each plate row is a broad tongue pointing down the bone over the top / outer face (its
// tip reaches the plate's distal step on the top, its sides sweep back toward the seam), outlined dark with a light
// bevel inside the outline and a raised panel framed by a groove; the next plate's root shows in shadow past the
// outline. The inner face carries rows of cream leaf scales. Rows: 0 the plain plate, 1 the shoulder plate darkening
// into the hump, 2 the elbow / wrist knob (a plain rounded band). Bark ramp index: 0 light .. 1 dark.
const bark = (k, n = 0) => PAL.p1_bark(clamp(k + n));
const SEAM = 124;
function p1ArmPaint(th, t, row) {
  const ath = Math.abs(th), nz = N.a(th / 40 + row * 3, t * 2.5) - .5;
  let c;
  if (row < 2 && ath > SEAM + 3) {
    // the inner face: rows of cream leaf scales pointing along the bone, bold dark wedges between them, a vein in each
    const S = scale((th + 180) / 30 + .5, t * 2.2 + .35, {p: .8, wid: .46});
    if (S.inside) {
      c = bark(.0 + .26 * (1 - S.fy) + .07 * S.id, .07 * nz);
      if (Math.abs(S.fx - .5) < .035 && S.fy > .3) c = mix(c, PAL.p1_line(.4), .5);
      if (S.edge < .06) c = mix(c, PAL.p1_bark(.7), .8);
    } else c = mix(PAL.p1_bark(.75), PAL.p1_line(.6), .4 + .3 * nz);
    c = sink(c, .2 * (1 - smooth(0, .15, t)));
  } else if (row === 2) {
    // the knob: a pale rounded band, light across its middle, dark contour at both ends
    c = bark(.12 + .2 * Math.abs(t - .5) * 2 + .06 * (ath / 180) + .08 * nz);
    if (t < .06 || t > .94) c = mix(PAL.p1_bark(.7), PAL.p1_line(.6), .4);
  } else {
    const tb = ath < SEAM ? .985 - .44 * Math.pow(ath / SEAM, 1.6) : .54;            // the tongue outline
    if (t < tb) {
      let k = .12 + .05 * (ath / SEAM) + .09 * nz;
      const sw = Math.abs(Math.sin((N.c(th / 55 + row, t * 1.6) * 7 + th / 90) * Math.PI));   // wood-grain contour swirls
      if (sw < .09) k += .16 * (1 - sw / .09);
      const ti = tb - .25, inPanel = t > .1 && t < ti && ath < 78;
      if (inPanel) k -= .06;
      c = bark(k);
      // the groove round the raised panel (dark line with a light lip)
      const gq = Math.min(t > .1 && ath < 80 ? Math.abs(t - ti) : 9, t > .1 && t < ti ? Math.abs(ath - 79) / 40 : 9);
      if (gq < .02) c = mix(c, PAL.p1_bark(.6), .7); else if (gq < .042) c = lift(c, .22);
      const d = tb - t;                                                               // inside the outline
      if (d < .045) c = mix(PAL.p1_bark(.72), PAL.p1_line(.6), .5 + .3 * nz);
      else if (d < .11) c = lift(c, .3 * line(d - .08, .03));
      c = sink(c, .32 * (1 - smooth(0, .14, t)));                                     // under the previous tongue
    } else {
      // the next plate's root, in the shadow of this tongue
      c = sink(bark(.2 + .08 * nz), .35 - .2 * smooth(0, .25, t - tb));
    }
    if (ath > SEAM - 3 && ath <= SEAM + 3) c = PAL.p1_line(.7);                         // the seam to the scale rows
  }
  if (row === 1) c = mix(c, PAL.p1_slate(.45 + .15 * nz), .72 * Math.pow(1 - smooth(.1, .95, t), 1.1));
  return c;
}
// Leg plates: rows 0 dark armour (three broad plate tongues round the leg, light bevel rims, dark gaps), 1 the transition
// (dark tongues reaching over pale bark), 2 pale bark (bold grain contours along the leg), 3 the knee band.
function p1LegPaint(th, t, row) {
  const nz = N.b(th / 45 + row * 5, t * 2) - .5;
  const barkC = () => {
    // pale bark: long flowing grain contours down the leg (about six round), a lighter ridge beside each, faint swirls
    const wob = .9 * (N.c(th / 120 + row * .7, t * .45) - .5) + .12 * Math.sin(t * 3.2 + th / 40);
    const g = Math.abs(Math.sin((th / 80 + wob) * Math.PI));
    let k = .15 + .09 * nz + .07 * (Math.abs(th) / 180);
    const sw = Math.abs(Math.sin((N.d(th / 45, t * 1.8) * 5) * Math.PI));
    if (sw < .06) k += .08;
    let c = bark(k);
    if (g < .12) c = mix(c, PAL.p1_line(.6 + .1 * nz), .78 * Math.min(1, 1.6 * (1 - g / .12)));
    else if (g < .26) c = lift(c, .18 * line(g - .19, .07));
    return c;
  };
  const tongue = (tt, ph) => {
    const x = (th + 180) / 120 + ph, ci = Math.floor(x), fx = x - ci, w = .49 * Math.pow(Math.max(0, 1 - Math.pow(tt, 1.8)), .5), e = w - Math.abs(fx - .5);
    if (e < 0) return null;
    const id = ((ci * 7) % 5 + 5) % 5 / 5;
    let c = PAL.p1_slate(clamp(.38 + .22 * tt + .1 * nz + .08 * id - .12 * line(fx - .4, .12)));
    if (tt < .14) c = mix(c, PAL.p1_slate(0), .8 * (1 - tt / .14));
    if (e < .04) c = PAL.p1_slate(.97);
    else if (e < .085) c = mix(c, PAL.p1_slate(.02), .5);
    return c;
  };
  let c;
  if (row === 0) c = tongue(t, 0) || PAL.p1_slate(.95);
  else if (row === 1) { c = t < .82 ? tongue(t / .82, .5) : null; if (!c) c = t < .18 ? PAL.p1_slate(.95) : sink(barkC(), .3 * (1 - smooth(.0, .3, t - .15))); }
  else if (row === 2) c = barkC();
  else {
    c = mix(PAL.p1_slate(.5 + .12 * nz), PAL.p1_slate(.15), smooth(.2, .7, 1 - Math.abs(t - .45) * 2));
    if (Math.abs(t - .45) < .04) c = mix(c, PAL.p1_slate(.0), .6);
    if (t > .9) c = PAL.p1_slate(.95);
  }
  c = sink(c, .2 * (1 - smooth(0, .12, t)));
  return c;
}
// ---- phase 3 paint --------------------------------------------------------------------------------------------------------
// The P3 plate (B / C / A cores): the dark glossy carapace (bottle green toward slate) over the top and back, the lime
// rim along its edge, broad lime leaf scales in front, the pale grey-lilac shell underneath. Rows: 0 carapace on the top
// and back (B: theta -165 .. 14), 1 carapace on the back only (A, C: theta -150 .. -35), 2 leaf scales and shell only.
const LILAC = C('#C4C3CC');
const caraC = (k) => mix(PAL.p3_bottle(clamp(k)), PAL.p1_slate(clamp(k * .9)), .3);
function p3PlatePaint(th, t, row) {
  const nz = N.e(th / 40 + row * 4, t * 2.2) - .5;
  const e0 = row === 0 ? 14 : -35, e1 = row === 0 ? -165 : -150;
  const cara = row < 2 && th < e0 && th > e1;
  let c;
  if (cara) {
    const hi = row === 0 ? -20 : -95;
    c = caraC(.6 + .1 * nz - .28 * line(th - hi, 26) * (1 - .5 * t));                         // the glossy highlight
    const seg = Math.abs(Math.sin((th / 50 + .4 * t) * Math.PI));
    if (seg < .06) c = caraC(.95);                                                            // plate seams
    if (t > .2 && t < .8 && Math.abs(th - (hi - 35)) < 3) c = mix(c, PAL.p3_rim(.4), .55);      // a lime line highlight
    if (th > e0 - 9) c = PAL.p3_rim(clamp(.08 + .25 * (e0 - th) / 9));                        // the lime rim
    else if (th < e1 + 4) c = PAL.p3_line(.85);
  } else if (Math.abs(th) > 140) {
    c = mix(PAL.p3_pale(clamp(.12 + .1 * nz + .1 * t)), LILAC, .4);
    const sw = Math.abs(Math.sin((N.c(th / 50, t * 1.5) * 6 + th / 80) * Math.PI));
    if (sw < .08) c = mix(c, PAL.p3_pale(.65), .55);
    if (Math.abs(Math.abs(th) - 140) < 3) c = PAL.p3_line(.6);
  } else {
    // broad lime leaf scales pointing down the limb, soft vein lines, pale tips
    const S = scale((th + 180) / 36 + .5, t * 1.7 + .25, {p: .65, wid: .48});
    if (S.inside) {
      c = PAL.p3_lime(clamp(.08 + .26 * S.fy + .1 * S.id + .07 * nz));
      if (Math.abs(S.fx - .5) < .025 && S.fy > .15) c = mix(c, PAL.p3_line(.3), .45);
      const vs = Math.abs(((S.fy * 4 + Math.abs(S.fx - .5) * 3) % 1) - .5);
      if (vs < .05 && Math.abs(S.fx - .5) > .05) c = mix(c, PAL.p3_line(.35), .25);
      if (S.edge < .045) c = mix(c, PAL.p3_line(.5), .55);
      if (S.fy > .75) c = mix(c, PAL.p3_leafhand(.05), .4 * (S.fy - .75) / .25);
    } else c = PAL.p3_line(.55 + .15 * nz);
  }
  c = sink(c, .28 * (1 - smooth(0, .16, t)));
  if (t > .95) c = mix(c, PAL.p3_line(.8), .6);
  return c;
}

// ---- card painters ---------------------------------------------------------------------------------------------------------
// leaf pointing down (-v): base at v1, tip at v0, half width w; painted with a midrib, side veins, an outline
const LEAF_R = {u0: -.2, u1: .2, v0: -1, v1: 0};
const leafSd = sdLeaf(0, -1, 0, .18, {p: .85});
function leafPaint(R, line0, {vein = true, dark = false, rim = null} = {}) {
  return (u, v) => {
    const d = leafSd(u, v);
    if (d > 0) return null;
    const along = -v, nz = N.a(u * 8, v * 8) - .5;
    let c = R(clamp((dark ? .55 : .14) + .3 * (1 - along) * (dark ? .3 : 1) + .1 * nz));
    if (vein && Math.abs(u) < .016 + .01 * (1 - along)) c = mix(c, line0(.35), .65);
    if (vein) { const s = Math.abs(((along * 7 + Math.abs(u) * 3.2) % 1) - .5); if (s < .05 && Math.abs(u) > .03) c = mix(c, line0(.4), .35); }
    if (rim && d > -.035) c = rim;
    else if (d > -.02) c = mix(c, line0(.75), .85);
    return c;
  };
}
// the P3 carapace plate card (B backs): a long rounded plate, dark glossy bottle green, the lime rim on its upper edge
const CARA_R = {u0: -.42, u1: .5, v0: -1, v1: 0};
const caraSd = (u, v) => { const t = clamp(-v), top = .5 - .12 * Math.pow(t, 3), bot = -.42 + .25 * Math.pow(t, 2.2); return Math.max(u - top, bot - u, v, -1 - v); };
const caraPaint = (u, v) => {
  const d = caraSd(u, v);
  if (d > 0) return null;
  const t = clamp(-v), top = .5 - .12 * Math.pow(t, 3), nz = N.d(u * 5, v * 5) - .5;
  let c = PAL.p3_bottle(clamp(.6 + .12 * nz - .3 * line(u - .15, .1)));
  if (top - u < .07) c = PAL.p3_rim(clamp(.1 + 2 * (top - u)));
  else if (top - u < .1) c = PAL.p3_line(.6);
  if (d > -.025) c = mix(c, PAL.p3_bottle(1), .8);
  if (t > .02 && t < .07) c = lift(c, .2);
  return c;
};
// the P1 dark slate leaf plate (leg armour overlays): light bevel rim, dark outline, a faint midline
const PLATE_R = {u0: -.4, u1: .4, v0: -1, v1: 0};
const plateSd = (u, v) => { const t = clamp(-v), w = .38 * Math.pow(Math.sin(Math.PI * Math.min(1, .35 + .65 * t)), .7); return Math.max(Math.abs(u) - w, v, -1 - v); };
const platePaint = (u, v) => {
  const d = plateSd(u, v);
  if (d > 0) return null;
  const nz = N.b(u * 6, v * 6) - .5;
  let c = PAL.p1_slate(clamp(.45 + .15 * nz + .2 * clamp(-v)));
  if (d > -.07) c = mix(c, PAL.p1_slate(.02), .8 * clamp((d + .07) / .04));
  if (d > -.025) c = PAL.p1_slate(.97);
  if (Math.abs(u) < .015 && v < -.15) c = mix(c, PAL.p1_slate(.85), .5);
  return c;
};
// rim tiles (plate steps and caps)
const rimP1 = tile('l1_rim', 32, 32, 32, (s, t) => mix(PAL.p1_bark(.62), PAL.p1_line(.55), .5 + .5 * Math.sin(t * 9 + s * 3)), 'p1');
const rimP1d = tile('l1_rimd', 32, 32, 32, (s, t) => mix(PAL.p1_slate(.95), PAL.p1_slate(.7), .5 + .5 * Math.sin(t * 9 + s * 3)), 'p1');
const rimP3 = tile('l3_rim', 32, 32, 32, (s, t) => mix(PAL.p3_line(.85), PAL.p3_bottle(.85), .5 + .5 * Math.sin(t * 9 + s * 3)), 'p3');

// ---- sprites -----------------------------------------------------------------------------------------------------------------
const ARM1 = wrapSprite('l1_arm', 128, 64, 3, p1ArmPaint, 'p1');
const LEG1 = wrapSprite('l1_leg', 128, 48, 4, p1LegPaint, 'p1');
const PL3 = wrapSprite('l3_plate', 128, 48, 3, p3PlatePaint, 'p3');
const LEAF = card('l3_leaf', LEAF_R, 64, leafPaint(PAL.p3_lime, PAL.p3_line), 'p3');
const LEAF_U = card('l3_leafu', LEAF_R, 48, leafPaint(t => mix(PAL.p3_pale(t * .7), LILAC, .3), t => mix(PAL.p3_line(t), LILAC, .35)), 'p3');
const LEAF_D = card('l3_leafd', LEAF_R, 48, leafPaint(PAL.p3_bottle, PAL.p3_line, {dark: true}), 'p3');
const CARA = card('l3_cara', CARA_R, 48, caraPaint, 'p3');
const PLATE1 = card('l1_plate', PLATE_R, 48, platePaint, 'p1');
const BUD = tile('l3_bud', 16, 16, 64, (s, t) => { const r = Math.hypot(s - .5, t - .45); let c = PAL.p3_beads(clamp(.02 + .5 * r + .25 * t * t)); if (t > .82) c = PAL.p3_beads(.55); return c; }, 'p3');
const VINE = tile('l3_vine', 16, 16, 64, (s, t) => PAL.p3_beads(clamp(.78 + .15 * Math.sin(t * 12 + s * 4))), 'p3');

// ---- phase 1 models -------------------------------------------------------------------------------------------------------
// radii [top / outer (+X), front, under / inner (-X), back]
function p1(seg) {
  const L = LEN[seg];
  switch (seg) {
    case 'a_up': return plates(L, [
      {t0: -.1, t1: .36, r: [.38, .46, .3, .43], c: [.02, 0], row: 1},      // the shoulder plate (darkening into the hump)
      {t0: .33, t1: .67, r: [.35, .44, .28, .41], c: [.07, .01]},
      {t0: .64, t1: .93, r: [.32, .41, .26, .38], c: [.06, 0]},
      {t0: .89, t1: 1.08, r: [.33, .39, .27, .36], row: 2},                // the elbow knob
    ], ARM1, rimP1, {seed: 300});
    case 'a_lo': return plates(L, [
      {t0: -.06, t1: .34, r: [.28, .36, .23, .34], c: [.03, 0]},
      {t0: .31, t1: .66, r: [.27, .4, .22, .38], c: [.07, .01]},
      {t0: .63, t1: .91, r: [.25, .45, .2, .43], c: [.05, 0]},                          // the paddle broadens toward the claw
      {t0: .88, t1: 1.04, r: [.27, .47, .22, .45], row: 2},                // the wrist cuff
    ], ARM1, rimP1, {seed: 320});
    case 'b_up': case 'c_up': {
      const k = seg === 'b_up' ? 1 : .9;
      const els = plates(L, [
        {t0: -.12, t1: .38, r: [.62 * k, .62 * k, .56 * k, .6 * k]},
        {t0: .34, t1: .72, r: [.58 * k, .6 * k, .53 * k, .57 * k]},
        {t0: .68, t1: 1.06, r: [.55 * k, .57 * k, .51 * k, .54 * k]},
      ], LEG1, rimP1d, {seed: 340 + k * 10});
      return els;
    }
    case 'b_lo': case 'c_lo': {
      const k = seg === 'b_lo' ? 1 : .9;
      const els = plates(L, [
        {t0: -.08, t1: .22, r: [.58 * k, .56 * k, .52 * k, .55 * k], row: 3},      // the knee
        {t0: .19, t1: .5, r: [.5 * k, .5 * k, .47 * k, .5 * k], c: [.02, -.01], row: 1},
        {t0: .47, t1: .8, r: [.46 * k, .47 * k, .44 * k, .46 * k], c: [.0, .01], row: 2},
        {t0: .77, t1: 1.03, r: [.47 * k, .48 * k, .45 * k, .47 * k], row: 2},      // the ankle cuff over the petal foot
      ], LEG1, rimP1d, {seed: 360 + k * 10});
      // the knee guards (their tops stand out, pivoting on the lower tip): one on the outer side, one over the front
      els.push(card2('x', .6 * k, {u0: -.34 * k, u1: .34 * k, v0: -.62 * k, v1: .26 * k}, PLATE1, PLATE1, ['z', -22.5, [.6 * k, -.62 * k, 0]]));
      els.push(card2('z', -.58 * k, {u0: -.3 * k, u1: .3 * k, v0: -.55 * k, v1: .24 * k}, PLATE1, PLATE1, ['x', -22.5, [0, -.55 * k, -.58 * k]]));
      return els;
    }
  }
  return [];
}
// ---- phase 3 models -------------------------------------------------------------------------------------------------------
// a leaf blade pointing down the bone, base at (x, y0), length h; side s = +1 / -1 flares toward +X / -X; plane 'z'
function bladeZ(x, y0, h, s, z, front, back, {w = 1, tilt = 22.5} = {}) {
  const k = h, hw = .2 * k * w;
  return card2('z', z, {u0: x - hw, u1: x + hw, v0: y0 - h, v1: y0}, front, back, tilt ? ['z', s * tilt, [x, y0, z]] : null);
}
// a white bell vine laid along the bone at (x, z) from y0 to y1 (y0 > y1): a thin vine of boxes with bells on alternate sides
function bellVine(x, z, y0, y1, {n = 6, out = [1, 0], seed = 0} = {}) {
  const els = [], step = (y0 - y1) / n;
  for (let i = 0; i < n; i++) {
    const ya = y0 - i * step, yb = ya - step - .02, wob = .03 * Math.sin(i * 2.1 + seed);
    els.push(abox([x - .028 + wob, yb, z - .028], [x + .028 + wob, ya, z + .028], 'l3_vine'));
    const sgn = i % 2 ? 1 : -1, bx = x + sgn * .1, bz = z + out[1] * -.04, by = ya - step * .5;
    els.push(abox([bx - .05, by - .12, bz - .05], [bx + .05, by - .02, bz + .05], 'l3_bud'));            // the bell
    els.push(abox([bx - .075, by - .15, bz - .075], [bx + .075, by - .11, bz + .075], 'l3_bud'));        // its flared mouth
    els.push(abox([bx - .012, by - .02, bz - .012], [bx + .012, by + .05, bz + .012], 'l3_vine'));      // the stalk
  }
  return els;
}
function p3(seg) {
  const L = LEN[seg];
  switch (seg) {
    case 'a_up': case 'a_lo': {
      // the antler arm: a slim shell, broad lime blades flared on both sides (frontal plane, dark backs)
      const up = seg === 'a_up', r0 = up ? .25 : .2, dr = up ? .02 : .025;
      const els = plates(L, [
        {t0: up ? -.08 : -.05, t1: .37, r: [r0, r0 - .02, r0, r0 - .02], row: 1},
        {t0: .34, t1: .7, r: [r0 - dr, r0 - dr - .02, r0 - dr, r0 - dr - .02], row: 1},
        {t0: .67, t1: up ? 1.05 : 1.03, r: [r0 - 2 * dr, r0 - 2 * dr - .02, r0 - 2 * dr, r0 - 2 * dr - .02], row: 1},
      ], PL3, rimP3, {seed: 400 + (up ? 0 : 20)});
      for (let i = 0; i < 2; i++) {
        const t = .05 + i * .45, h = (up ? 1.1 : 1.0) * (1 - .12 * i);
        els.push(bladeZ(r0 * .5, -t * L, h, 1, -.012, LEAF, LEAF_D, {w: 1.05}));
        els.push(bladeZ(-r0 * .5, -(t + .2) * L, h * .94, -1, .012, LEAF, LEAF_D, {w: 1.05}));
      }
      if (!up) els.push(...cone([-(r0 - .02), -.12, 0], .13, .45, 'p3_gold', {axis: 'x', sign: -1, seed: 440}));
      if (up) els.push(...bellVine(-.05, -(r0 + .04), -.15 * L, -.9 * L, {n: 6, out: [0, 1], seed: 1}));
      return els;
    }
    case 'b_up': case 'b_lo': {
      // the middle arm: tall section, the dark carapace plates over the back with the lime rim proud of the top, broad lime
      // leaves wrapped over the top-front (turned to face front-up), grey-lilac under-leaves wrapped under (front-down)
      const up = seg === 'b_up', k = up ? 1 : .92;
      const R = (a, b, c, d) => [a * k, b * k, c * k, d * k];
      const els = plates(L, [
        {t0: up ? -.1 : -.06, t1: .37, r: R(.42, .31, .36, .33)},
        {t0: .34, t1: .71, r: R(.4, .3, .34, .32)},
        {t0: .68, t1: up ? 1.05 : 1.03, r: R(.38, .29, .33, .31)},
      ], PL3, rimP3, {seed: 460 + (up ? 0 : 20)});
      for (const [t0, t1, dz] of [[-.06, .6, .08], [.4, 1.04, .045]]) {
        els.push(card2('z', .33 * k + dz, {u0: -.56 * k, u1: .62 * k, v0: -t1 * L, v1: -t0 * L}, CARA, CARA));
      }
      const z0 = -(.33 * k + .05);
      for (let i = 0; i < 3; i++) {
        const t = -.04 + i * .34, y0 = -t * L, h = (.66 - .04 * i) * L, sh = (i % 2) * .04;
        // the pale under-leaf (wrapped under), then the lime leaf over it (wrapped over the top)
        els.push(card2('z', z0 + .02, {u0: -.72 * k - sh, u1: -.02, v0: y0 - h * .95 - .1, v1: y0 - .1}, LEAF_U, LEAF_U, ['y', 22.5, [-.02, y0, z0 + .02]]));
        els.push(card2('z', z0, {u0: -.12 + sh, u1: .62 * k + sh, v0: y0 - h, v1: y0}, LEAF, LEAF_U, ['y', -22.5, [-.12 + sh, y0, z0]]));
      }
      if (!up) els.push(...cone([.34 * k, -.12, .05], .14, .5, 'p3_gold', {axis: 'x', sign: 1, seed: 480}));
      return els;
    }
    case 'c_up': case 'c_lo': {
      // the lower arm: broad, covered with big leaves wrapped round it (lime over the front and top, grey-lilac under,
      // dark-backed behind), two staggered rows per segment, over the pale shell
      const up = seg === 'c_up', r0 = up ? .4 : .36;
      const els = plates(L, [
        {t0: up ? -.1 : -.06, t1: .37, r: [r0, r0 - .02, r0 - .02, r0 - .02], row: 1},
        {t0: .34, t1: .71, r: [r0 - .03, r0 - .05, r0 - .05, r0 - .05], row: 1},
        {t0: .68, t1: up ? 1.05 : 1.03, r: [r0 - .06, r0 - .08, r0 - .08, r0 - .08], row: 1},
      ], PL3, rimP3, {seed: 500 + (up ? 0 : 20)});
      for (let i = 0; i < 2; i++) {
        const t = .0 + i * .45, y0 = -t * L, h = (up ? .98 : 1.02) * (1 - .06 * i), r = r0 - .035 * i, z0 = -(r + .04), sh = i ? .06 : -.04;
        els.push(card2('z', z0 + .02, {u0: -.66 + sh, u1: .02 + sh, v0: y0 - h * .95 - .08, v1: y0 - .08}, LEAF_U, LEAF_U, ['y', 22.5, [sh, y0, z0 + .02]]));
        els.push(card2('z', z0, {u0: -.08 + sh, u1: .6 + sh, v0: y0 - h, v1: y0}, LEAF, LEAF_U, ['y', -22.5, [-.08 + sh, y0, z0]]));
        els.push(card2('z', r + .03, {u0: -.3 - sh, u1: .3 - sh, v0: y0 - h * .9, v1: y0 - .04}, LEAF_U, LEAF_D, ['x', -22.5, [0, y0 - .04, r + .03]]));
      }
      if (up) els.push(...bellVine(.12, -(r0 + .04), -.1 * L, -.85 * L, {n: 5, out: [0, 1], seed: 3}));
      return els;
    }
  }
  return [];
}
// ---- bead vine (P3): two vines hanging from the B upper arm, rows of white bells, small leaflets --------------------------------
const BEAD_L = dist(J.beads_l, [1.81, 1.35, -.69]);
const BLEAF_R = {u0: -.09, u1: .09, v0: -.3, v1: 0};
const BLEAF = card('l3_bleaf', BLEAF_R, 64, (u, v) => { const d = sdLeaf(0, -.3, 0, .08, {p: .8})(u, v); if (d > 0) return null; let c = PAL.p3_beads(clamp(.62 + .2 * -v)); if (d > -.012) c = PAL.p3_beads(.9); return c; }, 'p3');
function beads() {
  const els = [];
  for (const [x, z, len, n, seed] of [[0, 0, BEAD_L, 9, 0], [.14, .08, BEAD_L * .72, 6, 2]]) {
    els.push(...bellVine(x, z, .05, -len, {n, out: [1, 0], seed}));
    for (let i = 1; i < n; i += 2) {
      const y = .05 - i * (len / n);
      els.push(card2('z', z, {u0: x + BLEAF_R.u0, u1: x + BLEAF_R.u1, v0: y + BLEAF_R.v0, v1: y}, BLEAF, BLEAF, ['z', i % 4 === 1 ? 45 : -45, [x, y, z]]));
    }
  }
  return els;
}
// ---- region interface ------------------------------------------------------------------------------------------------------
const SEGS = ['a_up', 'a_lo', 'b_up', 'b_lo', 'c_up', 'c_lo'];
let built = null;
export function models() {
  if (built) return built;
  const out = {};
  for (const seg of SEGS) for (const [f, fn] of [['p1', p1], ['p3', p3]]) {
    const L = toUnits(autoSlot(fn(seg)), PART_SCALE[`${seg}_l`]);
    out[`${seg}_l_${f}`] = L; out[`${seg}_r_${f}`] = mirrorX(L);
  }
  const b = toUnits(autoSlot(beads()), PART_SCALE.beads_l);
  out.beads_l_p3 = b; out.beads_r_p3 = mirrorX(b);
  return (built = out);
}
export const FORM_MODELS = {
  ...Object.fromEntries(SEGS.flatMap(seg => ['l', 'r'].map(s => [`${seg}_${s}`, {p1: `${seg}_${s}_p1`, p3: `${seg}_${s}_p3`}]))),
  beads_l: {p1: 'empty', p3: 'beads_l_p3'}, beads_r: {p1: 'empty', p3: 'beads_r_p3'},
};
export function sprites() { models(); return {...SP}; }
void [cells, C];
