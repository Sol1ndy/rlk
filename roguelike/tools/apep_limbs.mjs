// LIMBS region of the 아펩의 오아시스 파수꾼 rig (plan R4 parts 22-39 minus the hands, 48-49; model_p3.md §0 item 2: the six
// phase-3 arms ARE the six phase-1 limbs): the upper and lower segments of the three limb pairs and the bead vines.
//   A (a_up, a_lo)   P1 the long pale shell arms (model.md §3.3, v1 f285 / f290, v2 f960 / f2076): one flattened shell per
//                    segment arching up along the bone, painted with nested U "wood-grain" contours in long panels, the
//                    shoulder root under a dark slate tongue (the hump colour), rows of cream leaf scales on the inner face,
//                    pale pointed shell plates laid over the top (the overlapping leaf shells); the forearm broadens into
//                    a paddle toward the claw
//                    P3 the raised "antler" arms: a leaf-painted shell clad in broad lime blades on both sides (dark backs)
//                    and across, a gold elbow cone, a white bell vine along the upper arm (model_p3 §2.3 items 13-14)
//   B (b_up, b_lo)   P1 the front legs (model.md §3.4): a dark armour shell with painted plate tongues and two leaf plates
//                    on the upper leg, the knee band and a knee guard, the lower leg's dark tongues over pale bark flaring
//                    into a root base over the petal foot
//                    P3 the middle arms: a thick leaf-painted shell, the dark glossy carapace plates on the back with the
//                    lime rim (v5 f1908), big broad lime leaves wrapped over the top-front, a pale under-leaf fringe, a gold
//                    elbow cone
//   C (c_up, c_lo)   P1 the rear legs (as B, smaller) | P3 the lower arms: thick, big lime leaves over the front and top,
//                    dark-backed leaves behind, a pale under-leaf fringe, white bell vines over the hips (v6 f480)
//   beads            P3 only: three bowed dark-green vines with rows of white lily-of-the-valley bells and small leaflets
//                    (P1: the empty model)
// Construction. Segments are SHELLS (shell(): one loft along the bone whose sections keep a constant profile and step a
// little, the steps closed by ledges) or chains of PLATES (plates(): overlapping lofts, used for the knee band), each
// showing one row of a WRAP sprite (u = round the bone, v = along the segment), so the paint knows the facet angle: theta
// 0 = model +X, 90 = model front (-Z), 180 = -X, -90 = back. Overlays (leaf blades, leaves, carapace plates) are
// two-sided cards with a front and a back sprite on one element; the P1 shell / armour plates are slabs (cards over a core
// of boxes).
// Frames (apep_pose FRAMES): every limb segment is authored in its bone frame 'y': model -Y along the bone from the joint
// toward the next joint, model -Z toward the world front at the reference stance (P1 CROUCH, P3 UPRIGHT). Measured axes
// (left side): P1 a_up +X up-out, a_lo +X out-up, b_up +X up-out, b_lo +X out, c_up +X up, c_lo +X out; P3 a_* +X
// toward the midline (the inner side of the raised arm), b_* +X up, c_up +X up, c_lo +X out-up. The right side is the
// mirror image of the left (mirrorX). Region interface: see apep_body.mjs.
import {loft, toUnits, mirrorX, registerTile, registerWrap} from './mboss_shape_lib.mjs';
import {cardX, cardZ, abox} from './mboss_model_lib.mjs';
import {PART_SCALE, J} from './apep_pose.mjs';
import {PAL, C, clamp, smooth, mix, N, lift, sink, autoSlot, sprite, onRect, spriteSize, sdLeaf, cone, cells, slab, TRANSPARENT} from './apep_materials.mjs';

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
// plates(L, list, spr, rim): a chain of overlapping plates about the bone, list of {t0, t1 (fractions of the bone length
// from the joint), r [e1+ (model +X), e2+ (front), e1-, e2- (back)], c [c1, c2] section centre, row, lip, lipF, knob}.
//   lip    (number or per-direction [e1+, e2+, e1-, e2-]) a flared RIM section at the distal end, lipF of the plate long:
//          the overlapping plate edge (a notch in the silhouette and a dark rim face at every plate). The next plate may
//          start inside the rim (t0 >= t1 - lipF * (t1 - t0)) and is then only kept GAP inside the rim, so it can be as
//          wide as the plate before it.
//   knob   a rounded band (elbow, knee, wrist): three sections, the middle one wider by `knob`.
// Caps: the distal end when the next plate is smaller (or last), the proximal end when the previous one is smaller.
const R4 = r => (Array.isArray(r) ? r : [r, r, r, r]);
const sup = r => Math.max(...R4(r));
const radd = (r, l, k = 1) => R4(r).map((x, j) => +(x + k * R4(l)[j]).toFixed(4));
// support distance of a plate's section in the facet direction theta (deg), its centre offset included (shape lib loft)
const supAt = (r, c, th) => { const a = th * Math.PI / 180, cs = Math.cos(a), sn = Math.sin(a), R = R4(r);
  return Math.hypot((cs >= 0 ? R[0] : R[2]) * cs, (sn >= 0 ? R[1] : R[3]) * sn) + c[0] * cs + c[1] * sn; };
export const PLATE_WARN = [];
const GAP = .025;
function plates(L, list0, spr, rim, {seed = 0, tex = null, lastCap = true, firstCap = false} = {}) {
  const els = [];
  const list = list0.map(p => ({...p, r: R4(p.r).slice(), c: p.c || [0, 0], lip: R4(p.lip || 0), lipF: p.lipF ?? .14}));
  for (const p of list) { p.tl = p.lip.some(x => x > 0) ? p.t1 - p.lipF * (p.t1 - p.t0) : p.t1; p.rl = radd(p.r, p.lip); }
  // overlapping neighbours must not share a facet plane (z-fighting): where two plates overlap, every facet of the next
  // one is moved GAP inside (or outside, for a bigger knob / cuff) the previous one's by growing / shrinking its radii
  list.forEach((p, i) => {
    const q = list[i + 1];
    if (!q || q.t0 >= p.t1) return;
    const rp = q.t0 >= p.tl - 1e-6 ? p.rl : p.r;
    const d = Array.from({length: 16}, (_, k) => supAt(rp, p.c, k * 22.5) - supAt(q.r, q.c, k * 22.5));
    const mean = d.reduce((x, y) => x + y) / 16;
    const delta = mean >= 0 ? Math.max(0, GAP - Math.min(...d)) : -Math.max(0, GAP + Math.max(...d));
    if (Math.abs(delta) > 1e-6) { q.r = q.r.map(x => +(x - delta).toFixed(4)); q.rl = radd(q.r, q.lip); }
    if (Math.abs(delta) > .03) PLATE_WARN.push(`${spr.name} seed ${seed} plates ${i}/${i + 1}: radii moved ${(-delta).toFixed(3)} b`);
  });
  list.forEach((p, i) => {
    const prev = list[i - 1], next = list[i + 1];
    let caps = '';
    if (prev ? sup(prev.rl) < sup(p.r) - .005 : firstCap) caps += '-';
    if (next ? sup(next.r) < sup(p.rl) + .005 : lastCap) caps += '+';
    // sections of constant profile (the loft's section profile is the mean of its two stations)
    const secs = [];
    if (p.knob) { const tm = (p.t1 - p.t0) * .28; secs.push([p.t0, p.t0 + tm, p.r], [p.t0 + tm, p.t1 - tm, radd(p.r, p.knob)], [p.t1 - tm, p.t1, p.r]); }
    else { secs.push([p.t0, p.tl, p.r]); if (p.tl < p.t1) secs.push([p.tl, p.t1, p.rl]); }
    const st = [{a: -secs[0][0] * L, r: secs[0][2], c: p.c}];
    for (const [, t1, r] of secs) { const pr = st[st.length - 1].r; st.push({a: -t1 * L, r: r.map((x, j) => +(2 * x - pr[j]).toFixed(4)), c: p.c}); }
    const e = loft('y', st, {n: 16, tex: tex || spr.name, caps, ledgeTex: rim, seed: seed + i * 7});
    els.push(...toRow(e, spr, p.row || 0));
  });
  return els;
}
// shell(L, [t0, t1], sections [[t end, r, c]], spr, row, rim): ONE loft along the bone from t0 to t1 (bone fractions) whose
// sections keep a constant profile (the loft's section profile is the mean of its two stations), steps closed by ledges;
// the whole loft shows one row of the wrap sprite (v 0 at t0 .. 1 at t1). Caps at both ends.
function shell(L, [t0], secs, spr, row, rim, {seed = 0, caps = '-+'} = {}) {
  const st = [{a: -t0 * L, r: secs[0][1], c: secs[0][2]}];
  for (const [t1, r, c] of secs) { const p = st[st.length - 1]; st.push({a: -t1 * L, r: r.map((x, j) => +(2 * x - p.r[j]).toFixed(4)), c: c.map((x, j) => +(2 * x - p.c[j]).toFixed(4))}); }
  return toRow(loft('y', st, {n: 16, tex: spr.name, caps, ledgeTex: rim, seed}), spr, row);
}
// a two-sided card (one element): plane 'z' rect {u0, u1 = X, v0, v1 = Y}, `front` on the -Z face; plane 'x' rect {u0, u1
// = Z, v0, v1 = Y}, `front` on the +X face. rot [axis, deg, pivot] (A-frame, 22.5 deg steps).
function card2(plane, at, rect, front, back, rot = null, {flipU = false, shade = true} = {}) {
  const el = plane === 'z' ? cardZ(front, at, {X0: rect.u0, X1: rect.u1, Y0: rect.v0, Y1: rect.v1}, {rot, shade, flipU})
    : cardX(front, at, {Z0: rect.u0, Z1: rect.u1, Y0: rect.v0, Y1: rect.v1}, {rot, shade, flipU});
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
// The shell arm (A arms, v1 f285 / f290, v2 f960 / f2076): each segment is ONE long flat shell (a paddle section, a few
// sections stepping out a little toward the claw), painted per segment (row 0 the upper arm, 1 the forearm; ARM_T maps
// the row's v to the bone fraction). The top face is pale bark with a raised panel and nested "wood-grain" contour lines
// that run along the arm parallel to the long sides and turn across in pointed arches at the panel ends (a dark line with
// a light lip inside each), so the plates read as long overlapping leaf shells; the paddle edges (|theta| 50-120) fall
// off into grey shade with a dark contour along the seam; the inner face (|theta| > SEAM) carries rows of cream leaf
// scales on a dark ground. The upper arm starts under a dark slate shoulder plate (the hump colour) whose tongue reaches
// down the top face; the forearm has two panels (an overlap at the bone middle). Bark ramp index: 0 light .. 1 dark.
const bark = (k, n = 0) => PAL.p1_bark(clamp(k + n));
const SEAM = 122, PE = 80, ARCH = .38, SPAN = .7;
export const ARM_T = [[-.1, 1.03], [-.08, 1.02]];                  // per row: the bone fraction at v = 0 and v = 1
// the panels of a row: the bone fraction of each panel's tip (its arch on the top face)
const ARM_PANELS = [[.97], [.56, .99]];
function p1ArmPaint(th, v, row) {
  const ath = Math.abs(th), [T0, T1] = ARM_T[row], L = row ? LEN.a_lo : LEN.a_up, t = T0 + v * (T1 - T0);
  const nz = N.a(th / 40 + row * 3, t * 3) - .5;
  const shade = smooth(48, 118, ath);
  let c;
  if (ath > SEAM + 3) {
    // the inner face: rows of cream leaf scales pointing along the bone, bold dark wedges between them, a vein in each
    const S = scale((th + 180) / 30 + .5, t * L * 2.1 + .35, {p: .8, wid: .44});
    if (S.inside) {
      c = bark(.08 + .3 * (1 - S.fy) + .08 * S.id, .07 * nz);
      if (Math.abs(S.fx - .5) < .035 && S.fy > .3) c = mix(c, PAL.p1_line(.45), .5);
      if (S.edge < .06) c = mix(c, PAL.p1_bark(.8), .8);
    } else c = mix(PAL.p1_bark(.85), PAL.p1_line(.7), .45 + .3 * nz);
  } else {
    // the panel the texel lies in (the top face, |theta| < PE): panel i ends in a pointed arch (its tip on the top at
    // ARM_PANELS[i], the ends sweeping back ARCH b along the panel's long sides); the next panel's root lies in the shadow
    // of that tip. d = the distance (b) to the panel's outline (the arch and the long sides, radius ~0.45 b). Between the
    // panel and the seam (PE .. SEAM) the paddle edge falls off into grey shade with two long lines along it.
    const P = ARM_PANELS[row], arch = ARCH / L * (1 - Math.pow(Math.min(1, ath / PE), 1.5));
    let i = P.findIndex(p1 => t <= p1 - ARCH / L + arch), past = false;
    if (i < 0) { i = P.length - 1; past = true; }
    const a1 = P[i] - ARCH / L + arch, a0 = i ? P[i - 1] - ARCH / L + arch : -9;
    const root = (t - a0) * L;
    let k = .25 + .05 * nz + .38 * shade;
    const sw = Math.abs(Math.sin((N.c(th / 55 + row, t * 2) * 6 + th / 90) * Math.PI));   // faint grain swirls
    if (sw < .06) k += .07 * (1 - sw / .06);
    if (ath > PE) {
      // the paddle edge: shade, two long grain lines, the dark seam toward the scale rows
      c = bark(k + .06);
      const q = (ath - PE) / (SEAM - PE), wob = .05 * (N.d(th / 20, t * 5) - .5);
      if (Math.abs(q - .38 - wob) < .05 || Math.abs(q - .7 - wob) < .04) c = mix(c, PAL.p1_line(.55), .55);
      if (q > .9) c = mix(c, PAL.p1_line(.75), .7);
      if (ath - PE < 5) c = lift(c, .2);
    } else if (past) {
      // past the last arch: the shell curving under the end rim (shade)
      c = sink(bark(.3 + .1 * nz + .25 * shade), .15);
    } else {
      // nested U contours: g = 1 on the panel outline, falling to 0 toward the spine (q across the top face, along the
      // bone over the last SPAN b before the arch), lines at fixed g; d = the distance to the outline (b)
      const q = ath / PE, g = Math.max(q, 1 - (a1 - t) * L / SPAN);
      const d = Math.min((a1 - t) * L, (PE - ath) * Math.PI / 180 * .45);
      if (g < .55) k -= .08;                                                          // the raised panel
      c = bark(k);
      const wob = .02 * Math.sin(th / 23 + t * 9 + row * 2) + .035 * (N.d(th / 30, t * 4) - .5);
      for (const [gc, w, s0] of [[.84, .03, .85], [.64, .026, .72], [.44, .022, .55]]) {
        const e = Math.abs(g - gc - wob);
        if (e < w) c = mix(c, PAL.p1_line(.6), s0);
        else if (e < w + .045 && g < gc + wob) c = lift(c, .26);                      // a light lip inside each line
      }
      if (d < .028) c = mix(PAL.p1_bark(.8), PAL.p1_line(.8), .6 + .3 * nz);         // the dark contour of the panel
      else if (d < .06) c = lift(c, .3 * line(d - .045, .018));
      if (root < .16) c = sink(c, .32 * (1 - root / .16));                             // under the previous panel's tip
    }
    if (row === 0) {
      // the shoulder plate: dark slate over the root, its tongue reaching down the top face to t ~ 0.42, a light bevel
      // stripe along the top and a dark outline with a light lip along the tongue's edge
      const tg = .56 - .34 * Math.pow(ath / SEAM, 1.6);
      if (t < tg) {
        let sl = PAL.p1_slate(clamp(.42 + .1 * nz + .3 * shade + .12 * (1 - smooth(0, .25, t))));
        if (Math.abs(th - 20) < 9 && t < tg - .08) sl = mix(sl, PAL.p1_slate(.02), .5 * (1 - Math.abs(th - 20) / 9));
        const e = (tg - t) * L;
        if (e < .035) sl = PAL.p1_slate(.97);
        else if (e < .075) sl = mix(sl, PAL.p1_slate(.02), .45);
        c = sl;
      } else if ((t - tg) * L < .06) c = sink(c, .3);                                 // its shadow on the shell
    }
  }
  if (t > T1 - .025) c = mix(PAL.p1_bark(.85), PAL.p1_line(.8), .5);                 // the end rim
  return mix(c, PAL.p1_slate(.1), .26);                                              // the grey-green cast of the arm shell
}
// Legs (B / C, model.md §3.4: dark armour on the upper leg fading to pale bark at the foot, v1 f315, v2 f870 / f2076).
// Each segment is ONE shell (a few sections, a gentle taper / flare); the plates are painted on it. Rows (v along the
// whole segment): 0 the upper leg (three staggered tiers of broad dark plate tongues pointing down the leg, each with a
// light bevel rim and a dark outline, deeper slate in the gaps), 1 the lower leg (a tier of dark tongues reaching down
// over pale bark, then pale bark with bold grain contours flowing down the leg into the flared root base), 2 the knee band.
function p1LegPaint(th, t, row) {
  const nz = N.b(th / 45 + row * 5, t * 2) - .5;
  const barkC = (tb) => {
    // pale bark: long flowing grain contours down the leg (about six round), a lighter ridge beside each, faint swirls
    const wob = .9 * (N.c(th / 120 + row * .7, tb * .8) - .5) + .12 * Math.sin(tb * 5 + th / 40);
    const g = Math.abs(Math.sin((th / 80 + wob) * Math.PI));
    let k = .2 + .09 * nz + .1 * (Math.abs(th) / 180);
    const sw = Math.abs(Math.sin((N.d(th / 45, tb * 3) * 5) * Math.PI));
    if (sw < .06) k += .08;
    let c = bark(k);
    if (g < .12) c = mix(c, PAL.p1_line(.6 + .1 * nz), .8 * Math.min(1, 1.6 * (1 - g / .12)));
    else if (g < .26) c = lift(c, .18 * line(g - .19, .07));
    return mix(c, PAL.p1_slate(.1), .12);
  };
  // one tier of plate tongues: tt 0 (the tier's root) .. 1 (the tongue tips), ph the stagger; null between the tongues
  const tongue = (tt, ph, n = 3) => {
    const x = (th + 180) / (360 / n) + ph, ci = Math.floor(x), fx = x - ci, w = .5 * Math.pow(Math.max(0, 1 - Math.pow(tt, 1.6)), .45), e = w - Math.abs(fx - .5);
    if (e < 0) return null;
    const id = ((ci * 7) % 5 + 5) % 5 / 5;
    let c = PAL.p1_slate(clamp(.34 + .2 * tt + .1 * nz + .08 * id - .16 * line(fx - .38, .12)));
    if (Math.abs(fx - .5) < .012 && tt > .15 && tt < .8) c = mix(c, PAL.p1_slate(.95), .5);    // a faint midline
    if (e < .035) c = PAL.p1_slate(.97);
    else if (e < .075) c = mix(c, PAL.p1_slate(.02), .55);
    return c;
  };
  let c;
  if (row === 0) {
    // three tiers (each the next one's root in the shadow of the tier above)
    const T = [[-.02, .45, 0], [.28, .74, .5], [.58, 1.02, .2]];
    c = null;
    for (let i = T.length - 1; i >= 0 && !c; i--) {
      const [t0, t1, ph] = T[i];
      if (t >= t0 && t <= t1) { c = tongue((t - t0) / (t1 - t0), ph); if (c && i < T.length - 1) c = sink(c, .25 * (1 - smooth(0, .12, t - t0))); }
    }
    if (!c) c = sink(PAL.p1_slate(.9), .1);
    c = sink(c, .18 * (1 - smooth(0, .1, t)));
  } else if (row === 1) {
    // the transition tier (dark tongues over the bark), then the bark; the root base darkens a little toward the foot
    c = t < .44 ? tongue(t / .44, .5) : null;
    if (!c) c = sink(barkC(t), .3 * (1 - smooth(0, .12, t - .05)) + .1 * smooth(.8, 1, t));
    if (t < .05) c = PAL.p1_slate(.95);
  } else {
    c = mix(PAL.p1_slate(.5 + .12 * nz), PAL.p1_slate(.15), smooth(.2, .7, 1 - Math.abs(t - .45) * 2));
    if (Math.abs(t - .45) < .04) c = mix(c, PAL.p1_slate(.0), .6);
    if (t > .9 || t < .06) c = PAL.p1_slate(.95);
  }
  return c;
}
// ---- phase 3 paint --------------------------------------------------------------------------------------------------------
// The P3 arm shell (model_p3 §2.3, v6 f480, v5 f1908): each segment is one shell painted over its whole length with BIG
// lime leaves lying along the arm (two staggered tiers per segment, five leaves round, pointing down the arm toward the
// hand; the proximal tier overlaps the distal one; a dark outline, a midrib and chevron side veins, yellower tips, a soft
// shadow round each leaf), the pale grey-lilac shell with wood-grain swirls showing between them, and per row the dark
// glossy carapace: row 0 the B arms (carapace over the back half with the lime rim along its top edge, v5 f1908), row 1
// the C arms (a carapace strip on the back), row 2 the A arms (leaves all round, a lime-dark back strip).
const LILAC = C('#C4C3CC');
const caraC = (k) => mix(PAL.p3_bottle(clamp(k)), PAL.p1_slate(clamp(k * .9)), .3);
const P3_CARA = [[-172, -8], [-150, -38], null];
function p3ArmPaint(th, t, row) {
  const nz = N.e(th / 40 + row * 4, t * 3) - .5, ath = Math.abs(th);
  const cr = P3_CARA[row];
  if (cr && th > cr[0] && th < cr[1]) {
    const hi = (cr[0] + cr[1]) / 2 + 25;
    let c = caraC(.62 + .1 * nz - .3 * line(th - hi, 22) * (1 - .4 * t));               // the glossy highlight
    const seg = Math.abs(Math.sin((th / 45 + .5 * t + .2) * Math.PI));
    if (seg < .05) c = caraC(.95);                                                      // plate seams
    if (t > .15 && t < .85 && Math.abs(th - (hi - 30)) < 2.5) c = mix(c, PAL.p3_rim(.4), .55);   // a lime line highlight
    if (th > cr[1] - 10) c = PAL.p3_rim(clamp(.06 + .3 * (cr[1] - th) / 10));         // the lime rim (top edge)
    else if (th < cr[0] + 5) c = PAL.p3_line(.85);
    return c;
  }
  // the leaves: tier i spans t in T[i], its five leaves centred every 72 deg (staggered 36 deg per tier)
  const T = [[-.04, .62, 0], [.36, 1.04, 36]];
  for (let i = 0; i < T.length; i++) {
    const [t0, t1, ph] = T[i], tl = (t - t0) / (t1 - t0);
    if (tl < 0 || tl > 1) continue;
    const x = (th + 180 + ph) / 72, ci = Math.floor(x), fx = (x - ci - .5) * 2;          // fx -1..1 across the leaf
    const w = 1.12 * Math.pow(Math.sin(Math.PI * Math.min(1, .16 + .84 * tl)), .7), e = w - Math.abs(fx);
    if (e < 0) continue;
    const id = (((ci * 7 + i * 3) % 5) + 5) % 5 / 5;
    let c = PAL.p3_lime(clamp(.08 + .3 * (1 - e / Math.max(.05, w)) * .5 + .22 * tl + .1 * id + .06 * nz));
    if (tl > .55) c = mix(c, PAL.p3_leafhand(.05), .45 * (tl - .55) / .45);              // yellower tips
    if (Math.abs(fx) < .045 && tl > .06 && tl < .92) c = mix(c, PAL.p3_line(.3), .55);   // the midrib
    const vs = Math.abs(((tl * 5 - Math.abs(fx) * 1.6) % 1 + 1) % 1 - .5);
    if (vs < .06 && Math.abs(fx) > .08 && e > .08) c = mix(c, PAL.p3_line(.4), .3);       // chevron side veins
    if (e < .06) c = mix(c, PAL.p3_line(.72), .85);                                     // the outline
    else if (e < .12) c = lift(c, .12);
    if (i > 0 && t < T[0][1] + .05) c = sink(c, .18 * (1 - smooth(0, .1, t - T[0][1] + .05)));   // under the tier above
    return c;
  }
  // between the leaves on the top / front: the deep green shadow under the leaf edges; underneath (|theta| > 125): the pale
  // grey-lilac shell with wood-grain swirls
  if (ath < 125 && !(row === 2 && th < -120)) return mix(PAL.p3_line(clamp(.55 + .1 * nz)), PAL.p3_lime(.85), .35);
  let c = mix(PAL.p3_pale(clamp(.14 + .1 * nz + .12 * smooth(100, 180, ath))), LILAC, .35);
  const sw = Math.abs(Math.sin((N.c(th / 50, t * 2.5) * 6 + th / 70) * Math.PI));
  if (sw < .07) c = mix(c, PAL.p3_pale(.6), .5);
  if (row === 2 && th < -120) c = mix(c, PAL.p3_line(.6), .5);                           // the A arm's dark back strip
  return sink(c, .12);
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
  if (top - u < .12) c = PAL.p3_rim(clamp(.04 + 2.2 * (top - u)));                     // the lime rim (v5 f1908)
  else if (top - u < .15) c = PAL.p3_line(.6);
  if (d > -.025) c = mix(c, PAL.p3_bottle(1), .8);
  if (t > .02 && t < .07) c = lift(c, .2);
  return c;
};
// the broad P3 leaf (B / C cladding, v6 f480): a broad pointed leaf with a few shallow lobes, pointing down (-v: base at v1,
// tip at v0), a midrib and pinnate veins angled toward the tip, a dark outline; yellower toward the tip
const BROAD_R = {u0: -.5, u1: .5, v0: -1, v1: 0};
const broadW = t => .47 * Math.pow(Math.sin(Math.PI * Math.min(1, .1 + .9 * t)), .62) * (1 - (t > .15 && t < .8 ? .1 * Math.pow(Math.max(0, Math.sin(t * Math.PI * 5 + .6)), 3) : 0));
const broadSd = (u, v) => { const t = clamp(-v), out = v > 0 ? v : v < -1 ? -1 - v : 0; return Math.max(Math.abs(u) - broadW(t), out > 0 ? out : -1e9); };
function broadPaint(R, line0, {dark = false, tipC = null} = {}) {
  return (u, v) => {
    const d = broadSd(u, v);
    if (d > 0) return null;
    const t = clamp(-v), nz = N.b(u * 6, v * 6) - .5, w = Math.max(.05, broadW(t));
    let c = R(clamp((dark ? .55 : .08) + (dark ? .12 : .26) * t + (dark ? .1 : .22) * Math.abs(u) / w + .07 * nz));
    if (tipC && t > .55) c = mix(c, tipC, .5 * (t - .55) / .45);
    if (Math.abs(u) < .018 + .014 * (1 - t) && t < .93) c = mix(c, line0(.35), .65);          // the midrib
    const vs = Math.abs(((t * 6 - Math.abs(u) * 4.5) % 1 + 1) % 1 - .5);
    if (vs < .045 && Math.abs(u) > .035 && d < -.04) c = mix(c, line0(.4), .38);               // pinnate veins
    if (d > -.03) c = mix(c, line0(.75), .85);
    else if (d > -.06) c = lift(c, .1);
    return c;
  };
}
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
// the P1 pale shell plate (A arm overlays, v1 f290): pale bark, two nested contour lines following the pointed outline, a
// light bevel inside the dark outline, shaded toward the tip
const platePalePaint = (u, v) => {
  const d = plateSd(u, v);
  if (d > 0) return null;
  const nz = N.c(u * 6, v * 6) - .5, t = clamp(-v);
  let c = bark(.16 + .1 * nz + .22 * t + .18 * Math.abs(u) / .4);
  for (const dc of [.07, .14]) if (Math.abs(-d - dc - .01 * Math.sin(v * 17)) < .009) c = mix(c, PAL.p1_line(.55), .7);
  if (d > -.025) c = mix(PAL.p1_bark(.85), PAL.p1_line(.8), .6);
  else if (d > -.05) c = lift(c, .3);
  return mix(c, PAL.p1_slate(.08), .2);
};
// rim tiles (plate steps and caps)
const rimP1 = tile('l1_rim', 32, 32, 32, (s, t) => mix(PAL.p1_bark(.62), PAL.p1_line(.55), .5 + .5 * Math.sin(t * 9 + s * 3)), 'p1');
const rimP1d = tile('l1_rimd', 32, 32, 32, (s, t) => mix(PAL.p1_slate(.95), PAL.p1_slate(.7), .5 + .5 * Math.sin(t * 9 + s * 3)), 'p1');
const rimBark = tile('l1_rimb', 32, 32, 32, (s, t) => mix(PAL.p1_bark(.45), PAL.p1_bark(.7), .5 + .5 * Math.sin(t * 9 + s * 3)), 'p1');
const rimP3 = tile('l3_rim', 32, 32, 32, (s, t) => mix(PAL.p3_line(.85), PAL.p3_bottle(.85), .5 + .5 * Math.sin(t * 9 + s * 3)), 'p3');

// a pointed dark leaf plate with thickness (the P1 leg overlays): a slab with the plate sprite on both faces over a core
// of boxes, plane 'x' (u = Z) or 'z' (u = X), the tip at v0
function leafPlate(plane, at, kr, rot, spr = PLATE1, edge = 'l1_rimd') {
  const sd = (u, v) => plateSd((u - (kr.u0 + kr.u1) / 2) * PLATE_R.u1 * 2 / (kr.u1 - kr.u0), (v - kr.v1) / (kr.v1 - kr.v0)) * (kr.v1 - kr.v0);
  return slab({plane, at, rect: kr, sd, half: .04, sprite: spr, edge, cell: .09, inset: .8, rot});
}
// ---- sprites -----------------------------------------------------------------------------------------------------------------
const ARM1 = wrapSprite('l1_arm', 192, 96, 2, p1ArmPaint, 'p1');
const LEG1 = wrapSprite('l1_leg', 128, 64, 3, p1LegPaint, 'p1');
const ARM3 = wrapSprite('l3_arm', 128, 80, 3, p3ArmPaint, 'p3');
const LEAF = card('l3_leaf', LEAF_R, 64, leafPaint(PAL.p3_lime, PAL.p3_line), 'p3');
const LEAF_U = card('l3_leafu', LEAF_R, 48, leafPaint(t => mix(mix(PAL.p3_pale(t * .55), LILAC, .25), C('#FAFAF6'), .25), t => mix(PAL.p3_line(t), LILAC, .45)), 'p3');
const LEAF_D = card('l3_leafd', LEAF_R, 48, leafPaint(PAL.p3_bottle, PAL.p3_line, {dark: true}), 'p3');
const CARA = card('l3_cara', CARA_R, 48, caraPaint, 'p3');
const LEAFW = card('l3_leafw', BROAD_R, 64, broadPaint(PAL.p3_lime, PAL.p3_line, {tipC: PAL.p3_leafhand(.05)}), 'p3');
const LEAFW_D = card('l3_leafwd', BROAD_R, 48, broadPaint(PAL.p3_bottle, PAL.p3_line, {dark: true}), 'p3');
// the pale under-leaf turned sideways (pointing -u: the fringe hanging under the B / C arms)
const paleLeaf = leafPaint(t => mix(mix(PAL.p3_pale(t * .55), LILAC, .25), C('#FAFAF6'), .25), t => mix(PAL.p3_line(t), LILAC, .45));
const LEAF_UD = card('l3_leafud', {u0: -1, u1: 0, v0: -.22, v1: .22}, 48, (u, v) => paleLeaf(v * .2 / .22, u), 'p3');
// its back (seen from behind the arm): a shaded grey-green
const LEAF_UDB = card('l3_leafudb', {u0: -1, u1: 0, v0: -.22, v1: .22}, 32, (u, v) => { const c = paleLeaf(v * .2 / .22, u); return c && mix(c, PAL.p3_line(.7), .55); }, 'p3');
const PLATE1 = card('l1_plate', PLATE_R, 48, platePaint, 'p1');
const PLATE1P = card('l1_platep', PLATE_R, 48, platePalePaint, 'p1');
const BUD = tile('l3_bud', 16, 16, 64, (s, t) => { const r = Math.hypot(s - .5, t - .45); let c = PAL.p3_beads(clamp(.02 + .5 * r + .25 * t * t)); if (t > .82) c = PAL.p3_beads(.55); return c; }, 'p3');
const VINE = tile('l3_vine', 16, 16, 64, (s, t) => PAL.p3_beads(clamp(.78 + .15 * Math.sin(t * 12 + s * 4))), 'p3');

// ---- phase 1 models -------------------------------------------------------------------------------------------------------
// radii [top / outer (+X), front, under / inner (-X), back]
function p1(seg) {
  const L = LEN[seg];
  switch (seg) {
    // the flattened shell arm: radii [top, front edge, under, back edge], one loft per segment whose sections step out a
    // little toward the claw (each step a thin ledge: the overlap of two shell plates); the upper arm's end flares over
    // the forearm's root at the elbow; the forearm broadens into the paddle under the claw
    case 'a_up': return shell(L, ARM_T[0], [
      [.15, [.34, .46, .28, .44], [.02, 0]],                 // the shoulder root (under the hump)
      [.32, [.33, .5, .27, .48], [.08, 0]],                  // the section centres arch up (+X) along the segment
      [.5, [.32, .53, .26, .51], [.13, 0]],
      [.68, [.31, .55, .25, .53], [.14, 0]],
      [.86, [.31, .57, .25, .55], [.1, 0]],
      [1.03, [.31, .58, .24, .56], [.05, 0]],                // the elbow end over the forearm root
    ], ARM1, 0, rimP1, {seed: 300}).concat(
      // a pale shell plate laid over the top of the arch, its tip toward the elbow (the overlapping leaf shells)
      leafPlate('x', .52, {u0: -.46, u1: .46, v0: -.8 * L, v1: -.34 * L}, null, PLATE1P, 'l1_rim'));
    case 'a_lo': return shell(L, ARM_T[1], [
      [.18, [.29, .53, .22, .51], [.06, 0]],
      [.36, [.29, .56, .22, .54], [.09, 0]],
      [.56, [.28, .59, .21, .57], [.1, 0]],                  // the second panel (the overlap past the bone middle)
      [.74, [.27, .62, .2, .6], [.08, 0]],
      [.88, [.26, .65, .19, .63], [.05, 0]],
      [1.02, [.25, .67, .18, .65], [.03, 0]],                // the paddle under the claw
    ], ARM1, 1, rimP1, {seed: 320}).concat(
      // two pale shell plates over the forearm's top, overlapping toward the claw
      leafPlate('x', .44, {u0: -.5, u1: .5, v0: -.5 * L, v1: -.02 * L}, null, PLATE1P, 'l1_rim'),
      leafPlate('x', .4, {u0: -.56, u1: .56, v0: -.9 * L, v1: -.46 * L}, null, PLATE1P, 'l1_rim'));
    case 'b_up': case 'c_up': {
      // the upper leg: one dark armour shell (the plates painted on it, a slight taper) and two pointed leaf plates laid
      // over its top / outer side and its front (the layered armour of model.md §3.4)
      const k = seg === 'b_up' ? 1 : .9, R = (a, b, c, d) => [a * k, b * k, c * k, d * k];
      const els = shell(L, [-.12], [[.45, R(.6, .6, .55, .58), [0, 0]], [1.06, R(.58, .58, .53, .56), [0, 0]]], LEG1, 0, rimP1d, {seed: 340 + k * 10, caps: ''});
      els.push(...leafPlate('x', .6 * k + .07, {u0: -.34 * k, u1: .34 * k, v0: -.95 * L, v1: -.08 * L}, null));
      els.push(...leafPlate('z', -(.6 * k + .07), {u0: -.3 * k, u1: .3 * k, v0: -.82 * L, v1: -.16 * L}, null));
      return els;
    }
    case 'b_lo': case 'c_lo': {
      // the lower leg: the knee band (rounded), then one shell: the dark transition tongues over pale bark, flaring out
      // toward the petal foot like a trunk's root base
      const k = seg === 'b_lo' ? 1 : .9, R = (a, b, c, d) => [a * k, b * k, c * k, d * k];
      const els = plates(L, [{t0: -.1, t1: .21, r: R(.58, .58, .54, .57), knob: R(.04, .05, .02, .04), row: 2}], LEG1, rimP1d, {seed: 360 + k * 10});
      els.push(...shell(L, [.15], [
        [.62, R(.53, .53, .5, .53), [.02, -.01]],
        [.86, R(.56, .57, .53, .56), [.01, 0]],
        [1.0, R(.6, .62, .57, .6), [0, 0]],
        [1.13, R(.65, .67, .62, .65), [0, 0]],                                                 // the root base over the petal foot
      ], LEG1, 1, rimBark, {seed: 370 + k * 10, caps: '+'}));                                  // closed under the foot
      // the knee guard on the outer side: a pointed dark leaf plate with thickness, its top standing out
      els.push(...leafPlate('x', .6 * k, {u0: -.32 * k, u1: .32 * k, v0: -.66 * k, v1: .24 * k}, ['z', -22.5, [.6 * k, -.66 * k, 0]]));
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
function bellVine(x, z, y0, y1, {n = 6, out = [1, 0], seed = 0, bow = 0, bell = 1} = {}) {
  const els = [], step = (y0 - y1) / n;
  for (let i = 0; i < n; i++) {
    const ya = y0 - i * step, yb = ya - step - .02, wob = .03 * Math.sin(i * 2.1 + seed) + bow * Math.sin(Math.PI * (i + .5) / n);
    els.push(abox([x - .028 + wob, yb, z - .028], [x + .028 + wob, ya, z + .028], 'l3_vine'));
    const sgn = i % 2 ? 1 : -1, bx = x + wob + sgn * .11, bz = z + out[1] * -.04, by = ya - step * .5, q = bell;
    els.push(abox([bx - .055 * q, by - .13 * q, bz - .055 * q], [bx + .055 * q, by - .02, bz + .055 * q], 'l3_bud'));     // the bell
    els.push(abox([bx - .08 * q, by - .165 * q, bz - .08 * q], [bx + .08 * q, by - .12 * q, bz + .08 * q], 'l3_bud'));   // its flared mouth
    els.push(abox([bx - .012, by - .02, bz - .012], [bx + .012, by + .05, bz + .012], 'l3_vine'));                       // the stalk
  }
  return els;
}
function p3(seg) {
  const L = LEN[seg];
  switch (seg) {
    case 'a_up': case 'a_lo': {
      // the antler arm (v6 f480): a slim leaf-painted shell clad in broad lime blades on both sides (dark backs) pointing up
      // the arm, staggered and fanned (some flare toward the front), a gold elbow cone, a white bell vine along the arm
      const up = seg === 'a_up', r0 = up ? .3 : .26;
      const els = shell(L, [up ? -.08 : -.05], [
        [.5, [r0, r0 - .02, r0, r0 - .02], [0, 0]],
        [up ? 1.05 : 1.03, [r0 - .03, r0 - .05, r0 - .03, r0 - .05], [0, 0]],
      ], ARM3, 2, rimP3, {seed: 400 + (up ? 0 : 20), caps: up ? '' : '-+'});
      const B = up ? [[.02, 1.15, 1, .03], [.2, 1.08, -1, .08], [.42, 1.05, 1, .05], [.6, .98, -1, .1], [.78, .8, 1, .04]]
        : [[.04, 1.05, -1, .06], [.24, 1.0, 1, .03], [.46, .92, -1, .08], [.64, .82, 1, .05], [.8, .66, -1, .02]];
      for (const [t, h, sd, dz] of B) {
        const x = sd * r0 * .45;
        els.push(bladeZ(x, -t * L, h, sd, sd > 0 ? -dz : dz, LEAF, LEAF_D, {w: 1.8, tilt: 22.5}));
      }
      // blades across (plane x, alternately fanned) so the arm is leafy from the side as well
      for (const [t, h, sd] of up ? [[.12, .95, -1], [.3, .9, 1], [.5, .85, -1], [.66, .78, 1]] : [[.14, .88, 1], [.36, .8, -1], [.6, .7, 1]]) {
        els.push(card2('x', 0, {u0: -.2 * h * 1.4, u1: .2 * h * 1.4, v0: -t * L - h, v1: -t * L}, LEAF, LEAF_D, ['x', sd * 22.5, [0, -t * L, 0]]));
      }
      if (!up) els.push(...cone([-(r0 - .02), -.12, 0], .13, .45, 'p3_gold', {axis: 'x', sign: -1, seed: 440}));
      if (up) els.push(...bellVine(-.05, -(r0 + .04), -.15 * L, -.9 * L, {n: 6, out: [0, 1], seed: 1}));
      return els;
    }
    case 'b_up': case 'b_lo': {
      // the middle arm (v6 f480 / v5 f1908): a thick leaf-painted shell (about 1.1 b tall), the dark carapace plates over
      // the back with the lime rim proud of the top, three big broad lime leaves per segment wrapped over the top-front
      // (folded back over the top, overlapping, pointing toward the hand), a fringe of pale pointed under-leaves hanging
      // under the front
      const up = seg === 'b_up', k = up ? 1 : .9;
      const rt = .58 * k, rf = .42 * k, ru = .5 * k, rb = .44 * k;
      const els = shell(L, [up ? -.1 : -.06], [
        [.5, [rt, rf, ru, rb], [0, 0]],
        [up ? 1.05 : 1.03, [rt - .04, rf - .03, ru - .04, rb - .03], [0, 0]],
      ], ARM3, 0, rimP3, {seed: 460 + (up ? 0 : 20), caps: up ? '' : '-+'});
      for (const [t0, t1, dz] of [[-.06, .6, .08], [.4, 1.04, .045]]) {
        els.push(card2('z', rb + dz, {u0: -(ru + .06), u1: rt + .1, v0: -t1 * L, v1: -t0 * L}, CARA, CARA));
      }
      const z0 = -(rf + .05);
      for (let i = 0; i < 3; i++) {
        const v = [[0, 1, 0], [.06, .9, .05], [.03, 1.04, -.03]][(i + (up ? 0 : 1)) % 3];
        const t = -.03 + i * .33 + v[0], y0 = -t * L, h = .62 * L * v[1], u0 = -.22 + v[2];
        els.push(card2('z', z0 - .014 * (i % 2), {u0, u1: u0 + 1.05 * k, v0: y0 - h, v1: y0}, LEAFW, LEAF_U, ['y', -22.5, [u0, y0, z0 - .014 * (i % 2)]]));
        // two pale under-leaves per lime leaf hanging below the front edge (sizes and fold angles vary; the second one sits
        // in its own plane so the two never share a face plane)
        for (const [dt, dl, dw, ang, dz] of [[.04, (i % 2) * .1, 0, 22.5, .03], [.21, .12 - (i % 2) * .1, .06, 45, .05]]) {
          const yu = y0 - dt * L, uu = -(ru - .25);
          els.push(card2('z', z0 + dz, {u0: uu - .58 - dl, u1: uu, v0: yu - .36 - dw, v1: yu}, LEAF_UD, LEAF_UDB, ['y', ang, [uu, yu, z0 + dz]], {shade: false}));
        }
      }
      if (!up) els.push(...cone([rt - .06, -.12, .05], .14, .5, 'p3_gold', {axis: 'x', sign: 1, seed: 480}));
      return els;
    }
    case 'c_up': case 'c_lo': {
      // the lower arm (v6 f480): thick and broad, a leaf-painted shell covered with big broad lime leaves wrapped over the
      // front and top (dark-backed leaves behind), a pale under-leaf fringe, white bell vines over the hips
      const up = seg === 'c_up', r0 = up ? .52 : .47;
      const els = shell(L, [up ? -.1 : -.06], [
        [.5, [r0, r0 - .04, r0 - .04, r0 - .04], [0, 0]],
        [up ? 1.05 : 1.03, [r0 - .06, r0 - .09, r0 - .09, r0 - .09], [0, 0]],
      ], ARM3, 1, rimP3, {seed: 500 + (up ? 0 : 20), caps: up ? '' : '-+'});
      for (let i = 0; i < 3; i++) {
        const t = -.02 + i * .32, y0 = -t * L, h = (up ? .58 : .55) * L * (1 - .06 * i), r = r0 - .03 * i, z0 = -(r + .04), sh = (i % 2) ? .08 : -.05;
        els.push(card2('z', z0, {u0: -.3 + sh, u1: .78 + sh, v0: y0 - h, v1: y0}, LEAFW, LEAF_U, ['y', -22.5, [-.3 + sh, y0, z0]]));
        els.push(card2('z', z0 + .03, {u0: -(r + .45), u1: -(r - .25), v0: y0 - .1 * L - .36, v1: y0 - .1 * L}, LEAF_UD, LEAF_UDB, ['y', 22.5, [-(r - .25), y0 - .1 * L, z0 + .03]], {shade: false}));
        if (i < 2) els.push(card2('z', r + .03, {u0: -.42 - sh, u1: .42 - sh, v0: y0 - h * .9, v1: y0 - .04}, LEAFW_D, LEAFW_D, ['x', -22.5, [0, y0 - .04, r + .03]]));
      }
      if (up) els.push(...bellVine(.14, -(r0 + .05), -.1 * L, -.85 * L, {n: 5, out: [0, 1], seed: 3}));
      return els;
    }
  }
  return [];
}
// ---- bead vine (P3): three bowed vines hanging from the B upper arm, rows of white bells, small leaflets --------------------------------
const BEAD_L = dist(J.beads_l, [1.81, 1.35, -.69]);
const BLEAF_R = {u0: -.09, u1: .09, v0: -.3, v1: 0};
const BLEAF = card('l3_bleaf', BLEAF_R, 64, (u, v) => { const d = sdLeaf(0, -.3, 0, .08, {p: .8})(u, v); if (d > 0) return null; let c = PAL.p3_beads(clamp(.62 + .2 * -v)); if (d > -.012) c = PAL.p3_beads(.9); return c; }, 'p3');
function beads() {
  const els = [];
  for (const [x, z, len, n, seed, bow] of [[0, 0, BEAD_L, 9, 0, .1], [.16, .09, BEAD_L * .74, 7, 2, -.08], [-.13, -.07, BEAD_L * .5, 5, 4, .06]]) {
    els.push(...bellVine(x, z, .05, -len, {n, out: [1, 0], seed, bow}));
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
