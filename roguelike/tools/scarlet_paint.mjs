// Sprites of the 홍련 (Scarlet) rig (S:hr/PLAN.md §2.2 paint guide, §2.8 atlas share): the tiles the lofted / boxed parts
// sample at a fixed texel density (scarlet_geometry.mjs TILE_SIZES), the WRAP sprites (u round a loft, v along it) and
// the unique cards. Painted procedurally (no external art); every painter is (u, v) in 0..1, v down the sprite. Card
// conventions (mboss_model_lib / scarlet_geometry): a front card reads as painted from the front (u = her right -> her
// left = screen left -> right), a back card from behind (u = her left -> her right); v = top -> bottom.
// An ORIGINAL design (PLAN §1.5): ivory robe, ink-violet vest, crimson sash and lotus motifs, black horsehair hat with a
// crimson band, ink-black hair with a crimson ribbon, a long single-edged sword with a violet temper line and a lotus
// guard, a black-lacquer scabbard with brass lotus-leaf fittings. Lighting is not baked (the arena lights her).
import {paintSpriteSet, C, clamp, smooth, mix, fbm, TRANSPARENT} from './mboss_paint_lib.mjs';
import {TILE_SIZES, WRAP_SPRITES} from './scarlet_geometry.mjs';

export const TEX_DIR = 'assets/rlk/textures/mboss/scarlet';
export const spriteId = n => `rlk:mboss/scarlet/${n}`;
const T = TRANSPARENT;
const fr = x => x - Math.floor(x);
const N = {a: fbm(7101), b: fbm(7213), c: fbm(7307), d: fbm(7411), e: fbm(7529)};
const lift = (c, k) => mix(c, [255, 252, 246, 255], clamp(k));
const sink = (c, k) => mix(c, [8, 6, 10, 255], clamp(k));
const withA = (c, a) => [c[0], c[1], c[2], Math.round(clamp(a) * 255)];

// ---- palette (PLAN §2.2; base / shade / highlight). The robe base sits a little warmer than the guide's #EDE6D6 so every
// base keeps CIE76 dE >= 10 from the original's values of the same role (PLAN §1.5; test_rig.py checks it) -------------------
export const PAL = {
  robe: [C('#EAE0CB'), C('#C9BDA2'), C('#FAF5EA')], collar: [C('#F8F6F0'), C('#D8D2C4')],
  vest: [C('#2A2033'), C('#1A1420'), C('#4A3A5A')], thread: C('#B89A5A'),
  crimson: [C('#9E1F35'), C('#6E1222'), C('#C8354F')],
  lotus: [C('#C8304A'), C('#8E1C30'), C('#F08AA0')], gold: C('#C9A45C'),
  trouser: [C('#3A3340'), C('#26212B'), C('#55495C')], boot: [C('#1C1A1E'), C('#0F0E10'), C('#3A3640')], sole: C('#E8E4DC'),
  leather: [C('#4A3428'), C('#2E2018'), C('#6E5040')], skin: [C('#F1D5C4'), C('#D4AE9C'), C('#FBE8DE')],
  hair: [C('#15121A'), C('#0A080D'), C('#4B3A66')], iris: C('#C98A3A'), irisRing: C('#5A3A1A'), lips: C('#C46A70'),
  weave: [C('#1E1A24'), C('#0E0C12'), C('#5A4A70')], crown: C('#141118'), knot: [C('#D23A55'), C('#FF5A78'), C('#8E1C30'), C('#FF9AB0')],
  jasper: C('#7A1E2A'), amber: C('#E3C27A'), blade: [C('#CCC8D2'), C('#9C7BC8'), C('#F4F2F8'), C('#6E6874')],
  iron: C('#2E2A30'), brass: [C('#B8924A'), C('#7E6230'), C('#E0C27A')], cord: C('#3E2A55'), ray: C('#E8E2D4'),
  scab: [C('#141216'), C('#7A1622'), C('#4A4652')], porcelain: C('#F4F2EC'), cobalt: C('#2B4A9A'),
  ghost: [C('#C97EDD'), C('#9A4FB8'), C('#F0C8FA')],
};
// the base paints per role, for the palette-distance check (test_rig.py reads the manifest's `paint_roles`)
export const PAINT_ROLES = {hat_top: '#1E1A24', bodysuit: '#EAE0CB', thigh_highs: ['#3A3340', '#EAE0CB'], tasset: ['#2A2033', '#9E1F35'],
  gold_strip: '#B8924A', hair: '#15121A'};

// ---- material helpers -----------------------------------------------------------------------------------------------------
function cloth(c3, u, v, {k = 1, twill = 10, folds = 2, seed = 'a'} = {}) {
  const [b, s, h] = c3;
  let c = mix(b, s, .35 * N[seed](u * 3, v * 3) * k);
  const tw = Math.abs(fr((u + v) * twill) - .5) * 2;                      // a faint diagonal twill
  c = mix(c, s, .1 * (tw > .8 ? 1 : 0) * k);
  const fold = Math.sin((u * folds + .3 * N.b(u * 2, v * 2)) * Math.PI * 2);
  c = fold > 0 ? mix(c, h, .18 * fold * k) : mix(c, s, -.22 * fold * k);
  return c;
}
const sheen = (c3, u, v, k = 1) => { const [b, s, h] = c3; const x = Math.sin((u * 1.3 + v * .4) * Math.PI * 2); return x > 0 ? mix(b, h, .5 * x * x * k) : mix(b, s, -.5 * x * k); };
// a stylised red lotus (five petals with pink tips round a gold-thread centre) inside a roundel of radius 1 at (dx, dy)
function lotusAt(dx, dy, {petals = 5, rot = -90, ring = true, bg = null} = {}) {
  const r = Math.hypot(dx, dy);
  if (r > 1) return null;
  const ang = Math.atan2(dy, dx) * 180 / Math.PI - rot, seg = 360 / petals;
  const a = ((ang % seg) + seg) % seg - seg / 2;                          // angle to the nearest petal's axis
  const pw = .58 * Math.cos(Math.min(Math.PI / 2, Math.abs(a) * Math.PI / seg));
  if (ring && r > .88) return mix(PAL.gold, PAL.brass[2], .3);
  if (r < .2) return mix(PAL.gold, PAL.brass[2], .4 * (1 - r / .2));
  const t = (r - .2) / .62;
  if (t < 1 && Math.abs(a) / (seg / 2) < pw * (1 - .35 * t) + .25 * (1 - t)) {
    let c = mix(PAL.lotus[1], PAL.lotus[0], smooth(0, .5, t));
    c = mix(c, PAL.lotus[2], smooth(.62, 1, t));
    if (Math.abs(a) < 2.5) c = mix(c, PAL.lotus[1], .35);
    return c;
  }
  return bg;
}

// ---- tiles ----------------------------------------------------------------------------------------------------------------
const TILE_PAINT = {
  robe: (u, v) => cloth(PAL.robe, u, v, {k: .7, twill: 16}),
  robe_in: (u, v) => mix(PAL.robe[1], PAL.robe[0], .25 * N.c(u * 4, v * 4)),
  vest: (u, v) => { let c = sheen(PAL.vest, u, v, .5); const d = Math.abs(fr(u * 4) - .5) + Math.abs(fr(v * 4) - .5); if (Math.abs(d - .35) < .04) c = mix(c, PAL.vest[2], .25); return c; },
  crimson: (u, v) => sheen(PAL.crimson, u, v, .7),
  trouser: (u, v) => mix(PAL.trouser[0], PAL.trouser[1], .4 * N.d(u * 3, v * 6) + .15 * (Math.abs(fr(u * 6) - .5) < .08 ? 1 : 0)),
  boot: (u, v) => sheen(PAL.boot, u, v, .6),
  sole: (u, v) => mix(PAL.sole, C('#BDB8AE'), fr(v * 4) < .18 ? .5 : .1 * N.a(u * 6, v * 6)),
  skin: (u, v) => mix(PAL.skin[0], PAL.skin[2], .25 * N.e(u * 3, v * 3)),
  hair: (u, v) => { const st = Math.abs(Math.sin((u * 9 + .6 * N.a(u * 2, v * 3)) * Math.PI)); let c = mix(PAL.hair[1], PAL.hair[0], st);
    if (st > .92 && fr(v * 2 + u) < .5) c = mix(c, PAL.hair[2], .55); return c; },
  brass: (u, v) => mix(PAL.brass[0], v < .3 ? PAL.brass[2] : PAL.brass[1], v < .3 ? .4 * (1 - v / .3) : .35 * (v - .3) / .7),
  iron: (u, v) => mix(PAL.iron, C('#4A4550'), .3 * N.b(u * 4, v * 4)),
  lacquer: (u, v) => mix(PAL.scab[0], PAL.scab[2], .35 * Math.pow(Math.max(0, Math.sin((u * .8 + v * .3) * Math.PI * 2)), 6)),
  steel: (u, v) => mix(PAL.blade[0], PAL.blade[2], .3 * Math.abs(Math.sin(u * 7 + v * 2))),
  porcelain: (u, v) => mix(PAL.porcelain, C('#E2E6F0'), .25 * N.c(u * 3, v * 3)),
};
// ---- WRAP sprites (u round the loft: 0..1 = facet 0..n; v along the loft: 0 = its first station) -------------------------------
const WRAP_PAINT = {
  // 행전: ivory leg wraps, diagonal wrap folds, two crimson ties (v 0.16 and 0.74)
  wrap: (u, v) => { let c = cloth(PAL.robe, u, v, {k: .6, twill: 12});
    const wl = fr(v * 7 + u * .8); if (wl < .12) c = mix(c, PAL.robe[1], .5);
    for (const tv of [.16, .74]) if (Math.abs(v - tv) < .045) { c = sheen(PAL.crimson, u * 2, v, .8); if (Math.abs(v - tv) > .035) c = sink(c, .3); }
    return c; },
  // 토시: dark-brown leather arm guards bound by three crimson cords (v 0.18 / 0.5 / 0.82)
  guard_arm: (u, v) => { let c = mix(PAL.leather[0], PAL.leather[1], .45 * N.d(u * 5, v * 5));
    if (v < .05 || v > .95) c = mix(c, PAL.leather[2], .5);
    for (const tv of [.18, .5, .82]) { const d = Math.abs(v - tv); if (d < .045) { const tw = fr(u * 16 + v * 8); c = mix(PAL.crimson[0], tw < .5 ? PAL.crimson[2] : PAL.crimson[1], .45); if (d > .034) c = sink(c, .35); } }
    return c; },
  // the sash: crimson silk, lengthwise folds
  sash: (u, v) => { let c = sheen(PAL.crimson, u * 3, v, .6); const f = fr(v * 3); if (f < .1) c = mix(c, PAL.crimson[1], .6); else if (f < .2) c = mix(c, PAL.crimson[2], .25); return c; },
  // the crown: lacquer black with one highlight stripe; the crimson silk band at the bottom (v > 0.81)
  crown: (u, v) => { if (v > .81) { let c = sheen(PAL.crimson, u * 4, v, .7); if (v < .83 || v > .985) c = sink(c, .35); return c; }
    let c = mix(PAL.crown, PAL.weave[1], .3 * N.a(u * 8, v * 3));
    const s = Math.abs(fr(u) - .58); if (s < .025) c = mix(c, PAL.weave[2], .65 * (1 - s / .025) * (.6 + .4 * (1 - v)));
    if (v < .03) c = mix(c, PAL.weave[2], .3);
    return c; },
  // the grip: violet cord in a diamond pattern over ivory ray skin
  grip: (u, v) => { const a = fr(u * 4 + v * 6), b = fr(u * 4 - v * 6); const cord = Math.min(Math.abs(a - .5), Math.abs(b - .5)) > .32;
    let c = cord ? mix(PAL.cord, C('#5A4478'), .3 * N.b(u * 8, v * 8)) : mix(PAL.ray, C('#C8C2B4'), .4 * N.c(u * 12, v * 12));
    if (!cord && fr(u * 24) < .12) c = mix(c, C('#B0AA9C'), .3); return c; },
};

// ---- cards ----------------------------------------------------------------------------------------------------------------------
// torso front: X -0.2..0.2 (u 0 = her right), Y 0.52 (v 0, the neck base) .. 0 (v 1, the waist). The robe body; its crossed
// collar (the left lapel over the right: the white collar band runs from her left neck down to her right); the vest's open
// front edges at |X| > 0.12 with the brass thread; the small lotus roundel on her left breast (X 0.155, Y 0.33)
function torsoFront(u, v) {
  const X = -.2 + .4 * u, Y = .52 - .52 * v;
  let c = cloth(PAL.robe, u, v, {k: .55, twill: 18, folds: 1.5});
  // the collar: the lapel bands (0.035 wide) from the neck's sides converging to the crossing at Y 0.27
  const lapL = (Y - .27) / .25, xl = .07 - .14 * (1 - clamp(lapL)) + .0;    // the outer (left) lapel edge: x from +0.07 at the neck to -0.07
  const outer = X - (-.075 + .145 * clamp((Y - .25) / .27));             // signed distance to her left lapel's line (in x)
  const inner = X - (.075 - .145 * clamp((Y - .25) / .27));
  if (Y > .25 && Math.abs(inner) < .022 && outer < -.01) c = mix(PAL.robe[1], PAL.collar[1], .5);       // the under lapel (partly hidden)
  if (Y > .25 && outer > -.032 && outer < .012) c = outer > -.006 ? PAL.collar[0] : mix(PAL.collar[0], PAL.collar[1], .35);   // the white 동정 on the top lapel
  if (Y > .25 && outer > .012 && outer < .016) c = mix(c, PAL.robe[1], .7);
  void xl;
  // the neck opening above the crossing
  if (Y > .47 && Math.abs(X) < .055 - (Y - .47) * .2 && outer < -.032) c = PAL.skin[1];
  // the vest's open front edges (ink violet beyond |X| 0.125, brass thread 0.006 inside the edge)
  const ve = Math.abs(X) - (.125 + .012 * (1 - v));
  if (ve > 0) { c = sheen(PAL.vest, u * 1.4, v, .45); if (ve < .009) c = mix(PAL.thread, PAL.brass[2], .3); }
  // the small roundel on her left breast (on the vest)
  const lo = lotusAt((X - .158) / .036, (Y - .33) / .036, {bg: null});
  if (lo) c = lo;
  return c;
}
// torso back: X +0.2..-0.2 (u 0 = her left), Y 0.52..0. The vest (ink violet) with the red-lotus roundel (D 0.20) between the
// shoulder blades (Y 0.34); the robe's collar band at the neck
function torsoBack(u, v) {
  const X = .2 - .4 * u, Y = .52 - .52 * v;
  let c = sheen(PAL.vest, u * 1.2, v * .8, .45);
  const d = Math.abs(fr(u * 5) - .5) + Math.abs(fr(v * 6) - .5);
  if (Math.abs(d - .35) < .03) c = mix(c, PAL.vest[2], .2);
  if (Y > .47 && Math.abs(X) < .085) c = Y > .505 ? PAL.collar[0] : PAL.robe[0];
  const lo = lotusAt(X / .1, (Y - .34) / .1, {petals: 8, rot: -90});
  if (lo) c = lo;
  else if (Math.abs(Math.hypot(X, Y - .34) - .115) < .006) c = PAL.thread;
  return c;
}
// fringe: X -0.15..0.15, Y 0.47 (v 0) .. 0.30 (v 1): hair over the crown front, blunt bangs ending at Y ~0.335 (a soft
// jagged edge), longer strands framing the face at |X| > 0.1 reaching the card's bottom
function fringe(u, v) {
  const X = -.15 + .3 * u, Y = .47 - .17 * v, ax = Math.abs(X);
  const edge = ax < .1 ? .335 + .006 * Math.sin(X * 140) + .004 * N.a(u * 9, 0) : .3 + .02 * smooth(.15, .1, ax);
  if (Y < edge) return T;
  const st = Math.abs(Math.sin((u * 26 + .5 * N.b(u * 3, v * 2)) * Math.PI));
  let c = mix(PAL.hair[1], PAL.hair[0], st);
  if (st > .9 && v > .25 && v < .6) c = mix(c, PAL.hair[2], .5);
  if (Y < edge + .012) c = mix(c, PAL.hair[1], .5);
  return c;
}
// face (64 x 64 over X -0.12..0.12, Y 0.38 (v 0) .. 0.12 (v 1)): young and calm, almond eyes with amber irises and a dark ring,
// thin dark brows at the bangs' edge, a small nose, soft rose lips. expr calm / smile (closed-lip) / closed (eyes closed)
const FACE_SH = {skin: C('#F6DDCE'), skin2: C('#E8C2B0'), skin3: C('#D4A694'), blush: C('#F2A0A0'), lash: C('#1A1216'), white: C('#FBF7F6'),
  whiteSh: C('#DCCFD6'), brow: C('#2A2026'), crease: C('#C99A8C'), shine: C('#FFFFFF'), lipLine: C('#9A3E48')};
function faceHalf(v) { if (v > .985) return 0; const t = clamp((v - .45) / .535); let hw = .98 - .74 * Math.pow(t, 1.55); if (v > .93) hw *= .5 + .5 * Math.sqrt(Math.max(0, 1 - ((v - .93) / .055) ** 2)); return hw; }
function face(expr) {
  return (u, v) => {
    const X = (u - .5) * 2, ax = Math.abs(X), hw = faceHalf(v);
    if (ax > hw) return T;
    let c = FACE_SH.skin;
    const rim = smooth(hw - .22, hw, ax);
    c = mix(c, FACE_SH.skin2, Math.max(.7 * rim, .55 * smooth(.2, .02, v)));
    c = mix(c, FACE_SH.skin3, .4 * smooth(hw - .08, hw, ax) * smooth(.5, .85, v));
    const bl = ((ax - .52) / .2) ** 2 + ((v - .47) / .06) ** 2;
    if (bl < 1) c = mix(c, FACE_SH.blush, .3 * (1 - bl));
    // brows: thin, gently arched, at v 0.17 (just under the bangs' edge)
    const bx = (ax - .14) / .52;
    if (bx > 0 && bx < 1) { const by = .175 - .03 * Math.sin(Math.PI * Math.pow(bx, .8)), bw = .016 * (1 - .45 * bx); if (Math.abs(v - by) < bw) c = mix(c, FACE_SH.brow, .85 - .3 * bx); }
    // eyes: centre |X| 0.4, v 0.29; almond, the outer corner lifted
    const ex = (ax - .4) / .23, ey = (v - .29) / .058;
    if (expr === 'closed') {
      const ly = .25 * ex * ex - .05;                                         // a closed lid: a soft downward arc with lashes
      if (ex > -1 && ex < 1.12 && Math.abs(ey - ly) < .28 + .14 * smooth(0, 1, ex)) c = FACE_SH.lash;
      else if (ex > -.9 && ex < 1 && Math.abs(ey - (ly - .8)) < .1) c = mix(c, FACE_SH.crease, .45);
    } else if (ex > -1.25 && ex < 1.5 && ey > -1.9 && ey < 1.4) {
      const e2 = Math.max(-1, Math.min(1, ex));
      const up = -.9 + .6 * e2 * e2 - .22 * e2, lo = .74 - .45 * e2 * e2 - .2 * e2;
      const th = .3 + .25 * smooth(-.3, 1, ex);
      if (ex >= -1 && ex <= 1 && ey > up - th && ey < up + .12) c = FACE_SH.lash;
      else if (ex > .95 && ex < 1.45 && Math.abs(ey - (up - .1 + (1 - ex) * .5)) < .26 * (1 - smooth(1, 1.45, ex))) c = FACE_SH.lash;
      else if (ex > -.5 && ex < .85 && Math.abs(ey - (up - .72)) < .09) c = mix(c, FACE_SH.crease, .5);
      else if (ex >= -1 && ex <= 1 && ey >= up && ey <= lo) {
        const ix = (ax - .41) / .14, iy = (v - .296) / .052, ir = Math.hypot(ix, iy);
        if (ir < 1) {
          c = ir > .82 ? PAL.irisRing : iy < 0 ? mix(PAL.irisRing, PAL.iris, smooth(-.9, 0, iy)) : mix(PAL.iris, C('#E6B060'), smooth(0, .8, iy) * .6);
          if (Math.hypot(ix, iy) < .38) c = mix(C('#2A1608'), c, .2);
          const sx = X < 0 ? -1 : 1;
          if (Math.hypot(ix + .35 * sx, iy + .4) < .28) c = FACE_SH.shine;
          c = mix(c, FACE_SH.lash, .3 * smooth(-.25, -.95, iy));
        } else c = mix(FACE_SH.white, FACE_SH.whiteSh, smooth(up + .6, up + .05, ey));
        if (ex < -.84) c = mix(c, C('#E6A8A4'), .6);
      } else if (ex > .05 && ex < 1.02 && ey > lo && ey < lo + .18) c = mix(c, C('#5A3A40'), .45);
    }
    // nose: a soft shade under the tip (v 0.62)
    if (ax < .06 && Math.abs(v - .625) < .014) c = mix(c, FACE_SH.skin3, .55 * (1 - ax / .06));
    if (ax < .025 && v > .5 && v < .61) c = mix(c, FACE_SH.skin2, .25);
    // mouth (v 0.79): small rose lips; smile = the corners turned up, closed-lip
    const mw = .17, mx = ax / mw;
    if (mx < 1) {
      const curve = expr === 'smile' || expr === 'closed' ? -.022 * mx * mx : .006 * (1 - mx * mx);
      const ly = .79 + curve;
      if (Math.abs(v - ly) < .007 + .004 * (1 - mx)) c = FACE_SH.lipLine;
      else if (v > ly && v < ly + .032 * (1 - mx * mx)) c = mix(PAL.lips, C('#E6A0A6'), smooth(ly, ly + .03, v) * .4);
      else if (v < ly && v > ly - .018 * (1 - mx * mx)) c = mix(c, PAL.lips, .65);
    }
    if (expr === 'smile' && ax > .14 && ax < .2 && Math.abs(v - .77) < .01) c = mix(c, FACE_SH.skin3, .35);
    return c;
  };
}
// hair cards: ponytail halves (X -0.078..0.078, v down the tail), side lock, the ribbon
function tail(i) {
  return (u, v) => {
    const half = i === 1 ? .5 - .06 * v : .5 - .38 * Math.pow(v, 1.6);
    const ax = Math.abs(u - .5);
    if (ax > half) return T;
    if (i === 2 && v > .96) return T;
    const st = Math.abs(Math.sin(((u - .5) / Math.max(.05, half) * 3.2 + .4 * N.a(u * 2, v * 4)) * Math.PI));
    let c = mix(PAL.hair[1], PAL.hair[0], st);
    if (st > .88 && Math.abs(fr(v * 1.5 + u) - .3) < .2) c = mix(c, PAL.hair[2], .55);
    if (ax > half - .06) c = mix(c, PAL.hair[1], .5);
    return c;
  };
}
function lockSpr(u, v) {
  const half = .45 - .3 * Math.pow(v, 2.2);
  if (Math.abs(u - .5) > half || v > .97) return T;
  const st = Math.abs(Math.sin((u * 5 + .5 * N.b(u, v * 3)) * Math.PI));
  let c = mix(PAL.hair[1], PAL.hair[0], st);
  if (st > .9 && v < .6) c = mix(c, PAL.hair[2], .5);
  return c;
}
function ribbon(u, v) {
  if (v > .9 && Math.abs(u - .5) < (v - .9) * 4) return T;                     // the forked end
  let c = sheen(PAL.crimson, u, v * 2, .6);
  if (Math.abs(fr(v * 6) - .5) < .12 && Math.abs(u - .5) < .22) c = mix(c, PAL.gold, .75);   // the small gold stamp
  if (u < .1 || u > .9) c = sink(c, .25);
  return c;
}
// skirt panels (u across the panel's two facets, v down from the belt to the hem): knife pleats, the crimson lotus band at
// the hem (the bottom 10 %); the back panels carry the vest's long back hem (ink violet, brass edge) over v < 0.56
function pleats(u, v) {
  const p = fr(u * 7), c0 = PAL.robe;
  let c = p < .62 ? mix(c0[0], c0[2], .25 * (1 - p / .62)) : mix(c0[1], c0[0], (p - .62) / .38 * .6);
  c = mix(c, c0[1], .15 * N.a(u * 3, v * 4));
  return c;
}
function hemBand(u, v, c) {
  if (v > .885 && v < .99) {
    let b = sheen(PAL.crimson, u * 2, v, .5);
    const lx = fr(u * 4) - .5, ly = (v - .937) / .045;
    const lo = lotusAt(lx / .38, ly, {petals: 5, ring: false, bg: null});
    if (lo) b = lo;
    if (v < .893 || v > .982) b = mix(PAL.gold, PAL.brass[1], .3);
    return b;
  }
  return c;
}
const skirtF = (u, v) => (v > .99 ? T : hemBand(u, v, pleats(u, v)));
function skirtB(u, v) {
  if (v > .99) return T;
  if (v < .56) { let c = sheen(PAL.vest, u * 1.3, v, .4); if (v > .54) c = mix(PAL.thread, PAL.brass[2], .3); if (u < .025 || u > .975) c = PAL.thread; return c; }
  return hemBand(u, v, pleats(u, v));
}
function sashTail(p2) {
  return (u, v) => {
    if (v > .985) return T;
    let c = sheen(PAL.crimson, u, v * 2, .6);
    if (Math.abs(fr(v * 5) - .5) < .06) c = mix(c, PAL.crimson[1], .4);
    if (u < .14 || u > .86) c = p2 ? mix(PAL.knot[1], C('#FFC0CC'), .25) : sink(c, .25);
    return c;
  };
}
// the brim (128 x 128 over X, Z -0.8..0.8, translucent): black horsehair weave, concentric rings and radial ribs, a faint
// lilac sheen on the outer rim; ONLY the corner wedges (|angle - 45 - 90 n| <= 11.25) and the 1.2-px ribs on their
// boundaries are painted (the four squares tile the disc); the centre r < 0.2 is clear. Coverage is decided at the pixel
// centre (hard edges, no seam of partial alpha); the weave alpha 215, the ribs and the rim opaque.
const BRIM_PX = 128, BRIM_R = .8;
// coverage of a brim square at (u, v) on a px x px grid, decided at the pixel centre: 'weave', 'rib' (the 1.2-px radial rib
// on a wedge boundary, painted by both neighbours), 'rim' (the opaque inner / outer bands) or null (clear)
function brimMask(u, v, px) {
  const pxu = (Math.floor(u * px) + .5) / px, pxv = (Math.floor(v * px) + .5) / px;
  const X = (pxu - .5) * 2 * BRIM_R, Z = (pxv - .5) * 2 * BRIM_R, r = Math.hypot(X, Z);
  if (r > BRIM_R - .004 || r < .2) return null;
  const ang = ((Math.atan2(Z, X) * 180 / Math.PI) % 360 + 360) % 360;
  const off = ((ang - 45) % 90 + 90) % 90, d = Math.min(off, 90 - off);
  const perp = Math.abs(Math.sin((d - 11.25) * Math.PI / 180)) * r * px / (2 * BRIM_R);
  const inWedge = d <= 11.25, onRib = Math.abs(d - 11.25) < 3 && perp < 1.2;
  if (!inWedge && !onRib) return null;
  if (onRib) return 'rib';
  return r > BRIM_R - .022 || r < .225 ? 'rim' : 'weave';
}
// the brim (128 x 128 over X, Z -0.8..0.8, translucent): black horsehair weave, concentric rings and radial ribs, a faint
// lilac sheen on the outer rim; ONLY the corner wedges (|angle - 45 - 90 n| <= 11.25) and the 1.2-px ribs on their
// boundaries are painted (the four squares tile the disc); the centre r < 0.2 is clear. Coverage is decided at the pixel
// centre (hard edges, no seam of partial alpha); the weave alpha 215, the ribs and the rim opaque.
function brim(u, v) {
  const m = brimMask(u, v, BRIM_PX);
  if (!m) return T;
  const pxPerB = BRIM_PX / (2 * BRIM_R);
  const Xs = (u - .5) * 2 * BRIM_R, Zs = (v - .5) * 2 * BRIM_R, rs = Math.hypot(Xs, Zs), as = Math.atan2(Zs, Xs);
  let c = mix(PAL.weave[0], PAL.weave[1], .35 * N.c(Xs * 9, Zs * 9));
  const ring = Math.abs(fr(rs * pxPerB / 8) - .5);
  if (ring < .12) c = mix(c, C('#2E2836'), .6);
  const rib = Math.abs(fr(as / (2 * Math.PI) * 64) - .5);
  if (rib > .42) c = mix(c, C('#08070A'), .55);
  if (rs > BRIM_R - .03) c = mix(c, PAL.weave[2], .55 * smooth(BRIM_R - .03, BRIM_R - .005, rs));
  if (m === 'rib') return mix(C('#0A090D'), PAL.weave[0], .25);
  if (m === 'rim') return c;
  return withA(c, 215 / 255);
}
// the knot at the back of the hatband: five crimson petals with pink tips round a gold-thread centre (P2 brighter)
function knot(p2) { return (u, v) => { const r = Math.hypot(u - .5, v - .5) * 2, lo = lotusAt((u - .5) * 2.1, (v - .5) * 2.1, {petals: 5, ring: false, bg: null});
  if (!lo) return p2 && r < 1 ? mix(PAL.knot[1], C('#FFE0E8'), .3) : T;
  return p2 ? mix(mix(lo, PAL.knot[1], .55), C('#FFF0F4'), .35 * smooth(.6, 0, r)) : lo; }; }
// the bead strings (32 x 64): the V from the top corners to the loop (v 0.6), then one strand to the bottom; jasper and
// amber beads with black spacers
function strings(u, v) {
  const bead = (t, s) => { const k = Math.floor(t * 18 + s); return k % 3 === 2 ? C('#141216') : k % 3 === 0 ? PAL.jasper : PAL.amber; };
  const at = (cx, t, s, w = .045) => { const d = Math.abs(u - cx), ph = fr(t * 18), r = Math.abs(ph - .5) * 2;
    return d < w * (1 - .45 * r * r) ? mix(bead(t, s), C('#FFFFFF'), .18 * (1 - r)) : null; };
  if (v <= .75) {
    // the two strands: straight down beside the cheeks (v < 0.5), then converging to the loop under the chin (v 0.5-0.75)
    const t = v / .75, k = smooth(.62, 1, t);
    for (const s of [0, 1]) { const cx = s ? .955 - .455 * k : .045 + .455 * k, c = at(cx, t, s); if (c) return c; }
    return T;
  }
  const t = (v - .75) / .25;
  return t < .95 ? (at(.5, t * .6, 0, .32) || T) : T;
}
// the lotus guard seen along the blade (32 x 32): eight dark-iron petals with a brass rim, the blade slot in the middle
function guardSpr(u, v) {
  const dx = (u - .5) * 2, dy = (v - .5) * 2, r = Math.hypot(dx, dy), a = Math.atan2(dy, dx), seg = Math.PI / 4;
  const k = ((a % seg) + seg) % seg - seg / 2, pr = .72 + .26 * Math.cos(k * 4);
  if (r > pr) return T;
  if (Math.abs(dx) < .09 && Math.abs(dy) < .55) return C('#0A090B');
  let c = mix(PAL.iron, C('#4A4452'), .35 * N.a(u * 6, v * 6));
  if (r > pr - .1) c = mix(PAL.brass[0], PAL.brass[2], .3);
  if (Math.abs(k) < .03) c = mix(c, PAL.brass[1], .5);
  return c;
}
// blade flats (16 x 128): u 0 = the edge (-Z) .. 1 = the spine; v 0 = the tip .. 1 = the guard. A 환도 point; the bright edge,
// the violet temper line (a soft wave), the steel body, the darker spine
function blade(u, v) {
  const w = v < .07 ? smooth(0, .07, v) : 1;
  const e0 = (1 - w) * .62;                                                    // the point: the edge curves up to the spine
  if (u < e0 || (v < .02 && u < .9)) return T;
  let c = mix(PAL.blade[0], PAL.blade[2], .25 * Math.abs(Math.sin(v * 40)));
  const hm = .2 + .05 * Math.sin(v * 70) + .03 * Math.sin(v * 23);
  if (u < e0 + .08) c = PAL.blade[2];
  else if (u < hm + e0 * .5) c = mix(PAL.blade[1], PAL.blade[2], .25);
  else if (u < hm + e0 * .5 + .05) c = mix(PAL.blade[1], PAL.blade[0], .5);
  if (u > .84) c = PAL.blade[3];
  if (Math.abs(u - .72) < .02 && v > .1) c = mix(c, PAL.blade[3], .4);         // the fuller line
  return c;
}
// the glow overlays (16 x 128, translucent): the edge side bright, fading to the spine
function glowSpr(col, core = '#FFFFFF') {
  return (u, v) => {
    const a = Math.pow(clamp(1 - u * 1.25), 1.5) * smooth(0, .06, v) * smooth(0, .03, 1 - v);
    return withA(mix(C(core), C(col), clamp(u * 2.2)), a * .92);
  };
}
// scabbard flats (16 x 128): u 0 = the edge side .. 1 = the spine; v 0 = the tip .. 1 = the mouth. Black lacquer, the red
// lacquer line along the spine, a soft gloss stripe, brass lotus-leaf fittings at the tip, the middle and the mouth
function scabSpr(u, v) {
  let c = mix(PAL.scab[0], PAL.scab[2], .5 * Math.pow(Math.max(0, 1 - Math.abs(u - .3) / .12), 2));
  if (Math.abs(u - .86) < .04) c = PAL.scab[1];
  const leaf = (v0, v1, up) => { if (v < v0 || v > v1) return false; const t = (v - v0) / (v1 - v0), x = Math.abs(u - .5) * 2; const tt = up ? t : 1 - t; return x < .25 + .75 * Math.sin(Math.PI * Math.min(1, tt * 1.2)); };
  if (leaf(0, .07, false) || leaf(.64, .69, true) || leaf(.955, 1, true)) { c = mix(PAL.brass[0], PAL.brass[2], .25 * Math.abs(Math.sin(u * 9))); if (Math.abs(u - .5) < .03) c = PAL.brass[1]; }
  return c;
}
// cup / bottle: white porcelain with blue (the cup's inside, its blue rim; the bottle's cobalt lotus scroll)
const cupIn = (u, v) => mix(C('#E8E2D8'), C('#A8C0D8'), .3 * smooth(.6, 0, Math.hypot(u - .5, v - .5)));
const cupRim = (u, v) => (v < .5 ? PAL.cobalt : mix(PAL.porcelain, PAL.cobalt, .3));
function bottleSpr(u, v) {
  let c = mix(PAL.porcelain, C('#E6EAF2'), .2 * N.d(u * 4, v * 4));
  if (v < .1 || (v > .82 && v < .86)) c = mix(c, PAL.cobalt, .7);
  const sc = Math.abs(Math.sin(u * Math.PI * 6 + Math.sin(v * 9) * 1.2) - (v - .45) * 4);
  if (v > .3 && v < .78 && sc < .25) c = mix(c, PAL.cobalt, .75);
  const lo = lotusAt((fr(u * 3) - .5) * 4, (v - .55) * 8, {petals: 6, ring: false, bg: null});
  if (lo) c = mix(lo, PAL.cobalt, .85);
  return c;
}
// the ghost texture (96 x 32, alpha 200; PLAN §2.2: core #9A4FB8 -> body #C97EDD -> rim #F0C8FA). Three regions, so every ghost
// twin uses this one texture and keeps its silhouette: u 0..1/3 the body gradient (every face), 1/3..2/3 the brim's wedge mask
// (the four brim squares of the hat), 2/3..1 the bead strings' mask (scarlet_geometry.allModels remaps the UVs)
function ghostGrad(u, v) { const d = Math.max(Math.abs(u - .5), Math.abs(v - .5)) * 2;
  return d < .35 ? mix(PAL.ghost[1], PAL.ghost[0], d / .35) : mix(PAL.ghost[0], PAL.ghost[2], smooth(.55, 1, d)); }
function ghost(u, v) {
  const a = 200 / 255;
  if (u < 1 / 3) return withA(ghostGrad(u * 3, v), a);
  if (u < 2 / 3) {
    const uu = (u - 1 / 3) * 3, c = brimMask(uu, v, 32);
    if (!c) return T;
    const r = Math.hypot(uu - .5, v - .5) * 2;
    return withA(mix(PAL.ghost[0], PAL.ghost[2], smooth(.8, .98, r) + .25 * (c === 'rib' ? 1 : 0)), a);
  }
  const c = strings((u - 2 / 3) * 3, v);
  return c === T || c[3] === 0 ? T : withA(mix(PAL.ghost[0], PAL.ghost[2], .4), a);
}
// ---- sprite table: name -> [w, h, painter, translucent] ----------------------------------------------------------------------
export function scarletSprites() {
  const S = {};
  for (const [n, [w, h]] of Object.entries(TILE_SIZES)) S[n] = [w, h, TILE_PAINT[n], false];
  for (const [n, [w, h]] of Object.entries(WRAP_SPRITES)) S[n] = [w, h, WRAP_PAINT[n], false];
  Object.assign(S, {
    torso_front: [64, 64, torsoFront, false], torso_back: [64, 64, torsoBack, false], fringe: [64, 48, fringe, false],
    face_calm: [64, 64, face('calm'), false], face_smile: [64, 64, face('smile'), false], face_closed: [64, 64, face('closed'), false],
    tail_1: [32, 64, tail(1), false], tail_2: [32, 64, tail(2), false], lock: [16, 64, lockSpr, false], ribbon: [16, 64, ribbon, false],
    skirt_f: [32, 64, skirtF, false], skirt_b: [32, 64, skirtB, false], sash_tail: [16, 64, sashTail(false), false], sash_tail_p2: [16, 64, sashTail(true), false],
    brim: [BRIM_PX, BRIM_PX, brim, true], knot_p1: [16, 16, knot(false), false], knot_p2: [16, 16, knot(true), false], strings: [32, 64, strings, false],
    guard: [32, 32, guardSpr, false], blade: [16, 128, blade, false], scab: [16, 128, scabSpr, false],
    glow_lilac: [16, 128, glowSpr('#C97EDD', '#FFE6FA'), true], glow_pink: [16, 128, glowSpr('#FF5AB4', '#FFE0F0'), true],
    glow_violet: [16, 128, glowSpr('#8A4CFF', '#E8DCFF'), true], glow_gold: [16, 128, glowSpr('#FFC83A', '#FFF6D0'), true],
    cup_in: [16, 16, cupIn, false], cup_rim: [16, 16, cupRim, false], bottle: [32, 32, bottleSpr, false], ghost: [96, 32, ghost, true],
  });
  return S;
}
export function paintScarlet(rp, sprites = scarletSprites()) {
  return paintSpriteSet(rp, TEX_DIR, sprites, spriteId);
}
