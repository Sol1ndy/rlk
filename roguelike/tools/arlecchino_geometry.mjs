// Models and hulls of the 아를레키노 (Arlecchino) rig (S:ar/PLAN.md §2.1-2.2; API tools/arlecchino_rig_api.md).
//
// Phase 1 shows the player avatar's own item models rlk:player_motion/arle/<part> (written by tools/build_player_rig.mjs
// from rlk:skin/arlecchino; this file never writes or copies them) and the avatar's scythe rlk:player_motion/weapons/scythe.
// Phase 2 builds ten part models from the embedded skin_33 (arlecchino_skin_p2.mjs) with the avatar's skinFaces layout and
// overlay inflation, copied below, but with CLASSIC 4-px arms (skin_33's arm columns are 4 px; the avatar skin is slim).
// The rig's own small models: the six wing / blade-leg segment cards (P1 crimson feather wings, P2 crimson blade legs),
// the cup and saucer of the intro, and an empty model (a part hidden by a look).
//
// Model frame (item_display, display context none): the joint pivot is model [8, 8, 8]; the client turns the model 180
// degrees about Y and the rig writes z-mirrored transforms, so in the rig's authoring frame (+X her left, +Y up, -Z forward)
// a model point (x, y, z) px sits at ((8 - x), (y - 8), (z - 8)) / 16 (modelPoints below): model -X is authored +X.
import {buildScytheGeometry} from './scythe_geometry.mjs';

export const NS_RP = 'rlk:mboss/arlecchino';
export const itemId = n => `${NS_RP}/${n}`;          // rlk:mboss/arlecchino/<model>
export const AVATAR = n => `rlk:player_motion/arle/${n}`;
export const SCYTHE = 'rlk:player_motion/weapons/scythe';
export const BODY = ['head', 'body', 'right_arm', 'right_forearm', 'left_arm', 'left_forearm', 'right_leg', 'right_shin', 'left_leg', 'left_shin'];
export const LEGS = [1, 2, 3, 4, 5, 6].flatMap(i => [`leg_${i}a`, `leg_${i}b`]);
export const PART_NAMES = [...BODY, 'scythe_r', 'scythe_l', ...LEGS, 'cup', 'saucer'];

// ---- the avatar's body boxes (tools/build_player_rig.mjs bodyModels(), copied; slim 3-px arms) and the P2 classic layout --
const SLIM = {
  head: {from: [4, 8, 4], to: [12, 16, 12], uv: [0, 0, 8, 8, 8], over: [32, 0, 8, 8, 8], start: 0, end: 8, inflate: .5},
  body: {from: [4, -4, 6], to: [12, 8, 10], uv: [16, 16, 8, 12, 4], over: [16, 32, 8, 12, 4], start: 0, end: 12, inflate: .25},
  right_arm: {from: [6.5, 4, 6], to: [9.5, 10, 10], uv: [40, 16, 3, 12, 4], over: [40, 32, 3, 12, 4], start: 0, end: 6, inflate: .25},
  right_forearm: {from: [6.5, 2, 6], to: [9.5, 8, 10], uv: [40, 16, 3, 12, 4], over: [40, 32, 3, 12, 4], start: 6, end: 12, inflate: .25},
  left_arm: {from: [6.5, 4, 6], to: [9.5, 10, 10], uv: [32, 48, 3, 12, 4], over: [48, 48, 3, 12, 4], start: 0, end: 6, inflate: .25},
  left_forearm: {from: [6.5, 2, 6], to: [9.5, 8, 10], uv: [32, 48, 3, 12, 4], over: [48, 48, 3, 12, 4], start: 6, end: 12, inflate: .25},
  right_leg: {from: [6, 2, 6], to: [10, 8, 10], uv: [0, 16, 4, 12, 4], over: [0, 32, 4, 12, 4], start: 0, end: 6, inflate: .25},
  right_shin: {from: [6, 2, 6], to: [10, 8, 10], uv: [0, 16, 4, 12, 4], over: [0, 32, 4, 12, 4], start: 6, end: 12, inflate: .25},
  left_leg: {from: [6, 2, 6], to: [10, 8, 10], uv: [16, 48, 4, 12, 4], over: [0, 48, 4, 12, 4], start: 0, end: 6, inflate: .25},
  left_shin: {from: [6, 2, 6], to: [10, 8, 10], uv: [16, 48, 4, 12, 4], over: [0, 48, 4, 12, 4], start: 6, end: 12, inflate: .25},
};
// skin_33 is a classic skin: the arm boxes are 4 px wide with the classic UVs (right [40,16] / overlay [40,32], left
// [32,48] / overlay [48,48]); head, body and legs are identical in both layouts (PLAN §2.1)
const ARM4 = {from: [6, 4, 6], to: [10, 10, 10]}, FORE4 = {from: [6, 2, 6], to: [10, 8, 10]};
export const P2_SPECS = {
  ...SLIM,
  right_arm: {...SLIM.right_arm, ...ARM4, uv: [40, 16, 4, 12, 4], over: [40, 32, 4, 12, 4]},
  right_forearm: {...SLIM.right_forearm, ...FORE4, uv: [40, 16, 4, 12, 4], over: [40, 32, 4, 12, 4]},
  left_arm: {...SLIM.left_arm, ...ARM4, uv: [32, 48, 4, 12, 4], over: [48, 48, 4, 12, 4]},
  left_forearm: {...SLIM.left_forearm, ...FORE4, uv: [32, 48, 4, 12, 4], over: [48, 48, 4, 12, 4]},
};
export const P1_SPECS = SLIM;
// arm layout per form (api.ARM_LAYOUT): the shoulder pivot offset from the body centre (avatar units; x SIZE in the rig)
export const ARM_W = {p1: 3, p2: 4};
export const SHOULDER_X = {p1: .34375, p2: .375};

// tools/build_player_rig.mjs skinFaces / skinBox, copied (the avatar's UV layout: u, v, w, h, d of a skin box, rows
// start..end of its height)
function skinFaces(u, v, w, h, d, start = 0, end = h) {
  const face = (a, b, c, e) => ({uv: [a / 4, b / 4, c / 4, e / 4], texture: '#skin'});
  return {east: face(u, v + d + start, u + d, v + d + end), north: face(u + d, v + d + start, u + d + w, v + d + end), west: face(u + d + w, v + d + start, u + 2 * d + w, v + d + end),
    south: face(u + 2 * d + w, v + d + start, u + 2 * d + 2 * w, v + d + end), up: face(u + d, v, u + d + w, v + d), down: face(u + d + w, v + d, u + d + 2 * w, v)};
}
const skinBox = (from, to, uv, start, end, inflate = 0) => ({from: from.map(x => x - inflate), to: to.map(x => x + inflate), faces: skinFaces(...uv, start, end)});
export const bodyElements = s => [skinBox(s.from, s.to, s.uv, s.start, s.end), skinBox(s.from, s.to, s.over, s.start, s.end, s.inflate)];

// ---- card helpers --------------------------------------------------------------------------------------------------------
const r4 = v => Math.round(v * 1e4) / 1e4;
// a two-sided card in the model XY plane at z (north / south faces), sprite u along +x (north face as seen from -z)
function card(sprite, [x0, y0], [x1, y1], z = 8) {
  return {from: [r4(x0), r4(y0), z], to: [r4(x1), r4(y1), z], faces: {
    north: {uv: [0, 0, 16, 16], texture: '#' + sprite},
    south: {uv: [16, 0, 0, 16], texture: '#' + sprite}}};
}
const solid = (from, to, sprite, uv = [0, 0, 16, 16], drop = []) => ({from: from.map(r4), to: to.map(r4),
  faces: Object.fromEntries(['north', 'south', 'east', 'west', 'up', 'down'].filter(f => !drop.includes(f)).map(f => [f, {uv, texture: '#' + sprite}]))});

// Segment cards (authoring frame after the client mirror: the segment hangs along -Y from the pivot; the feather / blade
// body spreads toward model +X = authored -X, which the pose turns to the trailing side). Lengths in avatar units (16 px):
// wing a 0.8 + b 1.0, leg a 0.82 + b 1.06 (x SIZE 1.4 in the rig: 1.1 + 1.4 b, 1.15 + 1.5 b).
export const SEG = {
  wing_a: {sprite: 'wing_a', w: [-1.6, 6.4], y: [-12.8, 1.2], len: .8},
  wing_b: {sprite: 'wing_b', w: [-1.6, 6.4], y: [-16, 1.2], len: 1.0},
  leg_a: {sprite: 'leg_a', w: [-1.6, 2.4], y: [-13.1, 1.4], len: .82},
  leg_b: {sprite: 'leg_b', w: [-1.6, 2.4], y: [-17, 1.4], len: 1.06},
};
// sprite sizes (w x h px): cards 1 : 2 (wings) / 1 : 4 (legs)
export const SPRITES = {wing_a: [96, 176], wing_b: [96, 192], leg_a: [48, 176], leg_b: [48, 192], cup: [16, 16], saucer: [16, 16]};

function cardModel(k) {
  const s = SEG[k];
  // two parallel cards 0.15 px apart (both two-sided) so a card seen exactly edge-on still shows a line
  return {textures: {[s.sprite]: itemId(s.sprite), particle: itemId(s.sprite)},
    elements: [card(s.sprite, [8 + s.w[0], 8 + s.y[0]], [8 + s.w[1], 8 + s.y[1]], 7.93), card(s.sprite, [8 + s.w[0], 8 + s.y[0]], [8 + s.w[1], 8 + s.y[1]], 8.07)]};
}
// the teacup (white porcelain, a gold rim band, a red line; 0.2 b at the boss scale) and its saucer; pivot = the hand point
function cupModel() {
  return {textures: {cup: itemId('cup'), particle: itemId('cup')}, elements: [
    solid([6.6, 8.2, 6.6], [9.4, 10.6, 9.4], 'cup', [0, 3, 16, 16], ['up']),
    solid([6.9, 10.1, 6.9], [9.1, 10.3, 9.1], 'cup', [0, 0, 4, 4], ['down']),           // the tea surface (dark amber)
    solid([9.4, 9.0, 7.75], [10.4, 9.25, 8.25], 'cup', [12, 0, 16, 2]),                 // handle
    solid([10.15, 9.0, 7.75], [10.4, 10.1, 8.25], 'cup', [12, 0, 16, 2]),
    solid([9.4, 9.85, 7.75], [10.4, 10.1, 8.25], 'cup', [12, 0, 16, 2])]};
}
function saucerModel() {
  return {textures: {saucer: itemId('saucer'), particle: itemId('saucer')}, elements: [
    solid([5.3, 8.0, 5.3], [10.7, 8.35, 10.7], 'saucer'), solid([6.4, 8.35, 6.4], [9.6, 8.5, 9.6], 'saucer', [4, 4, 12, 12], ['down'])]};
}

// ---- all rig-owned models: name -> {textures, elements} (written as rlk:item/mboss/arlecchino/<name>) -----------------------
export function rigModels() {
  const M = {};
  for (const p of BODY) M[`p2/${p}`] = {textures: {skin: itemId('skin_p2'), particle: itemId('skin_p2')}, elements: bodyElements(P2_SPECS[p])};
  for (const k of Object.keys(SEG)) M[k] = cardModel(k);
  M.cup = cupModel();
  M.saucer = saucerModel();
  M.empty = {textures: {particle: itemId('cup')}, elements: []};
  for (const [n, m] of Object.entries(M)) for (const e of m.elements) for (const v of [...e.from, ...e.to]) if (v < -16 || v > 32) throw new Error(`model ${n}: element outside -16..32`);
  return M;
}

// ---- hulls: authored-frame corner points (avatar units, part scale 1) of every model a part can show ------------------------
export function modelPoints(els) {
  const out = [];
  for (const e of els) {
    const [x0, y0, z0] = e.from, [x1, y1, z1] = e.to;
    for (const x of [x0, x1]) for (const y of [y0, y1]) for (const z of [z0, z1]) {
      let P = [x, y, z];
      if (e.rotation) {
        const {origin: O, axis, angle} = e.rotation, a = angle * Math.PI / 180, c = Math.cos(a), s = Math.sin(a);
        const d = [P[0] - O[0], P[1] - O[1], P[2] - O[2]];
        const r = axis === 'x' ? [d[0], d[1] * c - d[2] * s, d[1] * s + d[2] * c] : axis === 'y' ? [d[0] * c + d[2] * s, d[1], -d[0] * s + d[2] * c] : [d[0] * c - d[1] * s, d[0] * s + d[1] * c, d[2]];
        P = [r[0] + O[0], r[1] + O[1], r[2] + O[2]];
      }
      out.push([(8 - P[0]) / 16, (P[1] - 8) / 16, (P[2] - 8) / 16]);
    }
  }
  const seen = new Set();
  return out.filter(P => { const k = P.map(v => v.toFixed(4)).join(); if (seen.has(k)) return false; seen.add(k); return true; });
}
let HULLS = null;
// hull points by full item id (rlk:...): the avatar's boxes (slim), the P2 boxes, the scythe, the rig's own models
export function hulls() {
  if (HULLS) return HULLS;
  HULLS = {};
  for (const p of BODY) HULLS[AVATAR(p)] = modelPoints(bodyElements(SLIM[p]));
  HULLS[SCYTHE] = modelPoints(buildScytheGeometry().scythe);
  for (const [n, m] of Object.entries(rigModels())) HULLS[itemId(n)] = modelPoints(m.elements);
  return HULLS;
}
// the scythe's crescent mid point and edge sample (authored frame, avatar units): the anchor blade_* and the edge check
export const CRESCENT_MID = (() => { const th = 135 * Math.PI / 180, x = 5.0 + 13.2 * Math.cos(th), y = 15.5 + 11.2 * Math.sin(th); return [(8 - x) / 16, (y - 8) / 16, 0]; })();
