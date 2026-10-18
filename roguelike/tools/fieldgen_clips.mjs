// Motion clips of the experimental field generator (실험성 역장 발생 장치) rig: the pattern timelines of scratchpad
// mb3/plan.md (Rotation) and model.md §5 (motion, the core flip-up, the transitions) and §8 (the rest poses of the
// seven forms). Format and sampling: mboss_rig_clips.mjs; channels: fieldgen_pose.mjs.
//
// Rules every clip keeps (checked by build_mboss_fieldgen_rig.mjs):
//   * no horizontal root travel: pos x / z stay 0 (the module moves the body; the clips carry heights, tilts, rolls
//     and the stack spacing);
//   * spinners (halo, inner ring, brim, medallions, drill pods, tower tiers, the arch gyroscope in the field, the
//     plates) turn at rate channels w*; per clip each spinner's integrated angle is scaled to a whole number of turns
//     (0 turns = it holds still for that clip), so every clip starts and ends with every spinner at its rest angle
//     and no blend ever unwinds a spin;
//   * the pendulum hangs plumb and lags the root (swing keys 2-4 t after the root moves);
//   * the lowest point (pendulum tip, drill tips, the ring) stays over the floor.
import {accumulate as accumulateClip, sampleClip as sampleAt} from './mboss_rig_clips.mjs';
import {DEFAULT_POSE, FORMS, CRUISE, FIELD, DORMANT, COREUP, TOWER, LASER, DEPLOYED, RATES, DOCK, spikes, medals, FACE_FRONT} from './fieldgen_pose.mjs';

const k = (t, pose = {}, e) => [t, pose, e];
const STILL = Object.fromEntries(Object.keys(RATES).map(n => [n, 0]));
const HALF = Object.fromEntries(Object.entries(RATES).map(([n, v]) => [n, v * .25]));
// a sine wave sampled every `step` ticks (linear segments): [[t, value], ...]
const waveKeys = (len, period, amp, phase = 0, step = 10, base = 0) =>
  Array.from({length: Math.floor(len / step) + 1}, (_, i) => [i * step, base + amp * Math.sin(2 * Math.PI * (i * step / period) + phase)]);
// merge keyed channel tracks [[t, {ch: v}], ...] into clip keys (same tick merges; ease applies to all). Within each
// track, a channel missing at a merged tick between two of its own keys is interpolated linearly there, so a sparse
// track (an orbit keyed only at its ends) is not held by the other tracks' keys.
const lerpV = (a, b, u) => (typeof a === 'number' ? a + (b - a) * u : Array.isArray(a) ? a.map((x, i) => x + (b[i] - x) * u) : a);
function track(...lists) {
  const m = new Map();
  for (const [list, ease] of lists) for (const [t, pose] of list) {
    if (!m.has(t)) m.set(t, [t, {}, ease]);
    Object.assign(m.get(t)[1], pose);
  }
  const ticks = [...m.keys()].sort((a, b) => a - b);
  for (const [list] of lists) {
    const chans = new Set(list.flatMap(([, p]) => Object.keys(p)));
    for (const ch of chans) {
      const own = list.filter(([, p]) => ch in p).sort((a, b) => a[0] - b[0]);
      for (const t of ticks) {
        if (ch in m.get(t)[1]) continue;
        const i = own.findIndex(([tt]) => tt > t);
        if (i <= 0) continue;
        const [t0, p0] = own[i - 1], [t1, p1] = own[i];
        m.get(t)[1][ch] = lerpV(p0[ch], p1[ch], (t - t0) / (t1 - t0));
      }
    }
  }
  return ticks.map(t => m.get(t));
}
// the hover of a form: bob (pos y), a slow pitch / roll wobble on a second harmonic, the pendulum lagging 3 t
function hover(form, len, {bob = .12, period = 80, wob = 1.5, swing = 2, arch = null} = {}) {
  const H = form.pos[1], ys = waveKeys(len, period, bob, 0, 10, H);
  const out = ys.map(([t, y]) => {
    const w = 2 * Math.PI * t / len;
    const pose = {pos: [0, y, 0], rot: [form.rot[0] + wob * Math.sin(2 * w), form.rot[1], form.rot[2] + wob * .7 * Math.sin(2 * w + 1.3)],
      pdSw: [-swing * Math.sin(2 * w - .3), -swing * .7 * Math.sin(2 * w + 1.0)]};
    if (arch) pose.arch = [arch[0] + arch[1] * Math.sin(2 * Math.PI * t / period), 0, 0];
    return [t, pose];
  });
  return out.map(([t, p]) => [t, p, 'l']);
}
const loopClip = (name, form, len, opt = {}, extra = {}) => ({
  name, len, loop: true, keys: hover(form, len, opt).map(([t, p, e], i) => [t, i === 0 ? {...form, ...extra, ...p} : p, e]),
  note: opt.note || '',
});

// ---- the clips ------------------------------------------------------------------------------------------------------
export const CLIPS = [];
const add = c => { CLIPS.push(c); return c; };

// form holds (form/<name> queues these)
add(loopClip('idle_cruise', CRUISE, 160, {arch: [-35, 20], note: 'Cruise hover: bob +-0.12 b over 80 t, a +-1.5 degree wobble, the arch tilted 35 and rocking +-20 degrees, the pendulum lagging; halo 2.25, inner ring -4.5, brim 4.5, medallions 4.5 / -6.75, pods 11.25 degrees per tick (whole turns per loop).'}));
add(loopClip('field_idle', FIELD, 240, {bob: .1, period: 120, arch: null, note: 'Field hover: the stack spread, the pods orbiting 1.5 degrees per tick, the arch turning round the hanging core like a gyroscope, the violet column and link beams.'}));
CLIPS[1].keys = track([[[0, {drAz: 0}], [240, {drAz: 360}]], 'l'], [CLIPS[1].keys.map(([t, p]) => [t, p]), 'l']);
CLIPS[1].keys[0][1] = {...FIELD, ...CLIPS[1].keys[0][1]};
add({name: 'idle_dormant', len: 40, loop: true, keys: [k(0, {...DORMANT}), k(40, {})], note: 'Dormant: folded on the floor, still.'});
add(loopClip('hold_coreup', COREUP, 80, {bob: .05, note: 'Core-up rest pose (form/coreup).'}));
add(loopClip('hold_tower', TOWER, 80, {bob: .06, note: 'Tower rest pose (form/tower).'}));
{
  const c = add(loopClip('hold_laser', LASER, 72, {bob: .05, note: 'Laser rest pose (form/laser): the medallions counter-orbit at 5 degrees per tick with their beams.'}));
  c.keys = track([[[0, {meAz: 90, mgAz: -90}], [72, {meAz: 90 - 360, mgAz: -90 + 360}]], 'l'], [c.keys.map(([t, p]) => [t, p]), 'l']);
  c.keys[0][1] = {...LASER, ...c.keys[0][1]};
}
add(loopClip('hold_deployed', DEPLOYED, 80, {bob: .08, note: 'Deployed rest pose (form/deployed): the lances far out.'}));
add({name: 'glide', len: 40, loop: true, note: 'Travel: nose down 6 degrees, the pendulum swung back 10 degrees, the pods trailing a little.',
  keys: [k(0, {...CRUISE, rot: [-6, 0, 0], pdSw: [8, 0], drY: -1.05}), k(10, {pos: [0, 4.56, 0], pdSw: [11, 1]}, 'io'), k(20, {pos: [0, 4.5, 0], pdSw: [9, 0]}, 'io'),
    k(30, {pos: [0, 4.44, 0], pdSw: [11, -1]}, 'io'), k(40, {pos: [0, 4.5, 0], pdSw: [8, 0]}, 'io')]});

// entrance (model.md §5.4; E0 = the clank at 16): pods drop, halo and arch rise out of the hole, plate and pendulum drop,
// the eye opens, the arch turns, the rise 2.15 -> 4.5 b, settled for the turn to the player
add({name: 'entrance', len: 130, next: 'idle_cruise', events: {clank: 16, pods: 24, unfold: 30, eye: 54, turn: 60, rise: 80, risen: 110, face: 115},
  forms: [[0, 'dormant'], [110, 'cruise']],
  note: 'Dormant -> cruise (untargetable until about 110): clank (16), pods drop and the device lifts to 2.6 b (24-30), halo / inner ring / core rise out of the hole and the plates and pendulum drop while it lifts to 3.0 b (30-48), the eye opens (54, iris and slit idle), the arch turns 90 degrees (60-78), the rise 3.0 -> 4.5 b with the stack settling to cruise spacing (80-110), settled (115).',
  keys: [k(0, {...DORMANT, lk: 'off'}), k(15, {}), k(16, {pos: [0, 2.05, 0], rot: [0, 0, -1.5]}, 'i'), k(19, {pos: [0, 2.15, 0], rot: [0, 0, 1]}, 'o'),
    k(24, {rot: [0, 0, 0], drS: .72}), k(30, {pos: [0, 2.6, 0], drR: 2.95, drY: -.95, drS: 1, drSp: 45, wDrill: 11.25, pdY: -.3}, 'o'),
    k(34, {plY: -.9}), k(48, {pos: [0, 3.0, 0], haloO: [0, 1.6, 0], haloS: 1, halo2O: [0, 1.35, 0], halo2S: 1, coreO: [0, 0, 0], coreS: 1, plY: -1.1, plS: 1, pl2Y: -.98, pl2S: 1, pdY: -.75,
      wHalo: 2.25, wHalo2: -4.5, wBrim: 4.5, wMedE: 4.5, wMedG: -6.75, wPlate: .75, brim: [-16, 14]}, 'o'),
    k(53, {lk: 'off'}), k(54, {lk: 'el', pdSw: [-4, 0]}), k(60, {arch: [90, 0, 0], pdSw: [3, 0]}), k(78, {arch: [-35, 0, 0], pdSw: [0, 0]}),
    k(80, {pos: [0, 3.0, 0]}), k(110, {pos: [0, 4.5, 0], plY: -1.57, pl2Y: -1.45, pdY: -1.85, pdSw: [-6, 0]}, 'io'), k(118, {pdSw: [3, 0]}), k(130, {pdSw: [0, 0]})]});

// 일점 상쇄 (C1): turn and nose down, ports hot, the bombing run (the module glides the body and drops the bombs),
// level out into the slam's first pose (the module plays slam at the end for the finisher)
add({name: 'bomb_run', len: 58, next: 'idle_cruise', events: {turn: 0, ports: 10, run: 12, end: 56},
  note: 'C1 bombing run: nose down 18 degrees (0-10, slit hot), ports glowing (10), bombs from 12 to 56 at port_0..7 (the module drops them along its glide), level out (56-58) into the first pose of slam, which the module plays at 58 for the finisher (column, plunge, impact).',
  keys: [k(0, {...CRUISE}), k(10, {rot: [-18, 0, 0], lk: 'charge', pdSw: [10, 0]}), k(56, {rot: [-16, 0, 0], pdSw: [12, 0]}),
    k(58, {rot: [0, 0, 0], pdSw: [-6, 0]}, 'io')]});
// 내려찍기 (C2): the slam alone
add({name: 'slam', len: 45, next: 'idle_cruise', events: {column: 0, plunge: 13, impact: 16, rise: 23},
  note: 'C2 slam: the core face down and the gold column to the floor (0-13, 13 t tell), the plunge 4.5 -> 2.3 b (13-16, ease in, stack compressed), slam (16), sit 7 t, rise (23-44).',
  keys: [k(0, {...CRUISE, lk: 'charge'}), k(4, {eye: [-90, 0], arch: [90, 0, 0], colLen: 4.3, colW: .9}, 'o'), k(13, {colLen: 4.4}),
    k(16, {pos: [0, 2.3, 0], colLen: 2.25, pdY: .1, plY: -.8, pl2Y: -.7, drY: -.6, drR: 3.1, haloO: [0, 1.25, 0], halo2O: [0, 1.05, 0]}, 'i'),
    k(18, {colLen: 0, rot: [0, 0, -1.5]}), k(23, {rot: [0, 0, 0], lk: 'el'}),
    k(44, {pos: [0, 4.5, 0], eye: [0, 0], arch: [-35, 0, 0], pdY: -1.85, plY: -1.55, pl2Y: -1.42, drY: -.95, drR: 2.95, haloO: [0, 1.6, 0], halo2O: [0, 1.35, 0], pdSw: [-5, 0]}, 'o'),
    k(45, {pdSw: [-4, 0]})]});
// 코어 / 레이저 빔 (C3): the medallions drop (4 t), charge (19 t), the beams fire at 25 and counter-orbit at exactly
// 5 degrees per tick for 133 t (the eye medallion from +X toward the front, the gear from -X toward the front: the spots
// meet in front 18 t after the start, then every 36 t, back and front), beams off, the medallions retract 16 t (finishing
// their second turn) and re-dock
add({name: 'laser', len: 175, next: 'idle_cruise', events: {drop: 0, charge: 4, aim: 23, fire: 25, off: 158, retract: 159},
  forms: [[4, 'laser'], [175, 'cruise']],
  note: 'C3 lasers: medallions drop to r 2.8, y -2.0 (0-4), charge (4-23, medals hot), beams extend 0 -> 3.74 b over 23-25 (48 degrees from vertical: floor spots on r 5.5 at H 4.5), from 25 they orbit at exactly 5 degrees per tick for 133 t (eye: az 90 -> -575; gear: -90 -> 575; the spots meet in front at 43, then every 36 t, back and front), beams off at 158-160, retract and re-dock (159-175). The module aims its line hazards at the same yaw every tick (manifest orbit).',
  orbit: {from: 25, to: 158, rate: 5, medal_eye: {az0: 90, sense: -1}, medal_gear: {az0: -90, sense: 1}, beam: {from_down: 48, length: 3.74, spot_r: 5.58}},
  keys: [k(0, {...CRUISE}), k(4, {...medals(90, 2.8, -2.0, [-42, 0, 0]), lk: 'charge'}, 'o'), k(22, {}),
    k(23, {blLen: 0, brLen: 0, blW: .7, brW: .7}), k(25, {blLen: 3.74, brLen: 3.74}, 'o'),
    k(158, {meAz: 90 - 665, mgAz: -90 + 665, blLen: 3.74, brLen: 3.74}, 'l'), k(160, {blLen: 0, brLen: 0, lk: 'el'}),
    k(175, {...medals(90 - 720, DOCK[0], DOCK[1], FACE_FRONT, {az: -90 + 720})}, 'o')]});
// 바위 폭탄 / 미사일 (C4): spike tips flare (the module's fx at spike_tip_l/r), the eye turns up and the vent shaft (the
// gold column up), 10 missiles from the top ports over 14 t
add({name: 'missiles', len: 64, next: 'idle_cruise', events: {flare: 0, vent: 8, launch: 22, last: 35},
  note: 'C4 missiles: slit hot and the spikes tip up 10 degrees (0-8, flare at the tips), the eye up and the arch flat, the gold vent column up 6 b (8-21), launches 22-35 at vent_l / vent_r, column off (38), back (64).',
  keys: [k(0, {...CRUISE, lk: 'charge'}), k(8, {...spikes(DOCK, [0, 0, 10]), eye: [90, 0], arch: [90, 0, 0], colDir: 'up', colLen: 0, colW: 1.5}, 'o'),
    k(14, {colLen: 6.0}, 'o'), k(22, {pos: [0, 4.62, 0]}), k(36, {pos: [0, 4.5, 0]}), k(38, {colLen: 0, lk: 'el'}),
    k(64, {...spikes(DOCK), eye: [0, 0], arch: [-35, 0, 0], colDir: 'down'}, 'o')]});
// 파쇄 / 바위 날리기 (C6): dip and roll 12 t, vent: column up + medallions flung up 8 t, the tower telescopes up 18 t,
// flame band 17 t, 8 bursts 6 t apart from 55, slab throws, revert 15 t with a roll wobble
add({name: 'tower_throw', len: 157, next: 'idle_cruise', events: {dip: 0, vent: 12, tower: 20, band: 38, burst: 55, throw: 95, revert: 142},
  forms: [[38, 'tower'], [157, 'cruise']],
  note: 'C6 rock throw: dip to 2.8 b with a 27 degree roll (0-12), vent column up and the medallions flung to +-5.5 b (12-20), rise and level while the tower telescopes up (20-38: tiers +1.35 / +2.0, halo x1.7 at +3.2, spikes and iris spike up), flame band 38-55 (fx), bursts from 55 every 6 t, throws from 95 every 8 t, revert (142-157) with a 20 degree roll wobble.',
  keys: [k(0, {...CRUISE}), k(12, {pos: [0, 2.8, 0], rot: [0, 0, 27], pdSw: [0, -14], pdY: -.45, plY: -1.15, pl2Y: -1.02, drY: -.8}, 'io'),
    k(14, {colDir: 'up', colLen: 0, colW: 1.2, lk: 'charge'}), k(17, {colLen: 4.5}, 'o'),
    k(20, {...medals(90, 5.5, 2.2, FACE_FRONT), pdSw: [0, 8]}, 'o'), k(22, {colLen: 0}),
    k(38, {...TOWER, pos: [0, 4.5, 0], rot: [0, 0, 0], pdSw: [0, 0], colDir: 'up', colLen: 0, lk: 'el'}, 'io'),
    k(142, {}), k(147, {rot: [0, 0, -20], pdSw: [0, 10]}, 'o'), k(152, {rot: [0, 0, 8]}),
    k(157, {...CRUISE, colDir: 'down'}, 'io')]});
// 지면 충격 / 중력 폭발 (C5): the core flip-up (model.md §5.3)
add({name: 'coreup', len: 130, next: 'idle_cruise', events: {spark: 0, eye: 1, rim: 3, lift: 5, up: 16, beam: 29, column: 41, blast: 48, sink: 81},
  forms: [[15, 'coreup'], [128, 'cruise']],
  note: 'C5 core flip-up: spark (0), the eye out (1-4), gold flash and lift (5-15: core to +2.8 b, arch upright, brim 25, spikes up and the medallions to the ring ends facing forward, iris spike up, roll 10), hold (16-28), the up-beam (29-40, column up 6 b), the core drops back toward the ring with the column down to the floor (40-44), blast (48), hold, settle back (81-130).',
  keys: [k(0, {...CRUISE, lk: 'charge'}), k(4, {eye: [-20, 0]}), k(5, {glowS: 0, glowLook: 'flash'}),
    k(7, {glowS: 1.2}, 'o'), k(9, {glowS: .6}),
    k(15, {pos: [0, 5.0, 0], rot: [0, 0, 10], coreO: [0, 2.8, 0], eye: [0, 0], arch: [0, 0, 0], brim: [-22, -12], hub: 180,
      ...spikes([3.6, .3, 0], [0, 0, 90]), ...medals(90, 3.6, .3), drR: 2.4, drY: -1.0, plY: -2.95, pl2Y: -2.75, pdY: -2.6, pglow: 1, glowS: 0}, 'o'),
    k(28, {colDir: 'up', colLen: 0, colW: 1.3, glowLook: 'gold'}), k(32, {colLen: 6.0, glowS: 1.08}, 'o'), k(40, {colLen: 6.0}),
    k(41, {colDir: 'down', colLen: 0}), k(44, {coreO: [0, .6, 0], colLen: 5.6, glowS: 0}, 'i'), k(50, {colLen: 5.6}), k(53, {colLen: 0}),
    k(81, {}), k(128, {...CRUISE, glowLook: 'charge'}, 'io'), k(130, {})]});
// field opener, two clips (the module teleports the body between them): warp_out = the halo flip and nose-up, then
// hidden (vis 0 from 12, before the module's warp at 13); warp_in_field = shown again at the new spot, the unfold
add({name: 'warp_out', len: 34, next: null, events: {flip: 0, hide: 12, out: 13}, hidden: [12, -1],
  note: 'Warp out: the halo flips upright and spins while the device pitches nose-up 35 degrees (0-11), vis 1 -> 0 in 1 t (11-12), hidden from 12 to the end (the module flashes and moves the body to the arena centre at 13, then plays warp_in_field at 34).',
  keys: [k(0, {...CRUISE}), k(11, {rot: [35, 0, 0], haloE: [90, 0, 0], haloO: [0, 1.8, 0], pdSw: [-14, 0], wHalo: 9, vis: 1}, 'io'),
    k(12, {vis: 0}, 'i'), k(34, {vis: 0})]});
add({name: 'warp_in_field', len: 24, next: 'field_idle', events: {in: 0, unfold: 1, field: 17, banner: 22}, hidden: [-1, 1], forms: [[17, 'field']],
  note: 'Warp in at the new spot: vis 0 -> 1 (0-2) at ring centre 5.8 b, the unfold to the field form in 16 t (1-17), the link beams and the violet column (17-21). Call look/field at unfold.',
  keys: [k(0, {...CRUISE, ...STILL, vis: 0, haloE: [0, 0, 0], pos: [0, 5.8, 0]}), k(2, {vis: 1, ...RATES}, 'o'),
    k(17, {...FIELD, blLen: 0, brLen: 0, colLen: 0}, 'io'), k(21, {blLen: 2.5, brLen: 2.5, colLen: 1.15}, 'o'), k(24, {})]});
// 「인력 충격파」: charge sphere with 4 pulses (24 t; 40 t for the third), a 1 t beam down, the burst flare; the third
// wave drops onto the floor with the stack compressed
const WAVE_POSE = {...FIELD};
function waveClip(name, charge, note) {
  const keys = [k(0, {...WAVE_POSE, glowS: 0, glowLook: 'charge', lk: 'charge'})];
  for (let i = 0; i < 4; i++) {
    const t0 = Math.round(charge * i / 4), t1 = Math.round(charge * (i + .5) / 4), g = .3 + .7 * (i + 1) / 4;
    keys.push(k(t1, {glowS: g * 1.08}, 'o'), k(Math.round(charge * (i + 1) / 4), {glowS: g}, 'i'));
  }
  keys.push(k(charge + 1, {colLen: 3.6, colW: .5, colLook: 'gold', glowS: 1.25}, 'o'), k(charge + 2, {colLen: 1.15, colW: .75, colLook: 'violet', glowS: 0}),
    k(charge + 4, {lk: 'el'}), k(charge + 16, {}));
  return {name, len: charge + 16, next: 'field_idle', events: {charge: 0, beam: charge + 1, impact: charge + 1}, note, keys};
}
add(waveClip('wave', 24, '「인력 충격파」: the charge sphere grows with 4 pulses (0-24), the 1 t gold beam down and the burst flare at 25 (impact: the front leaves the axis; the module runs it).'));
add(waveClip('wave_long', 40, 'The third 「인력 충격파」: a 40 t charge, the beam and impact at 41.'));
add({name: 'wave_drop', len: 84, next: 'field_idle', events: {charge: 0, drop: 36, land: 40, beam: 40, impact: 40, lift: 60, risen: 80},
  note: 'The third wave with the drop: the charge sinks the device 0.5 b (0-36), the drop -2.9 b in 4 t onto the floor with the stack compressed (ring centre 2.4 b, the core on the floor; 36-40), the beam and burst on landing (40-41), grounded 19 t, the lift-off pulse (60) and the rise (60-80).',
  keys: [k(0, {...FIELD, glowS: 0, glowLook: 'charge', lk: 'charge'}), k(18, {glowS: .7}), k(36, {pos: [0, 5.3, 0], pdY: -3.0, glowS: 1.0}),
    k(40, {pos: [0, 2.4, 0], coreO: [0, -1.15, 0], plY: -1.9, pl2Y: -1.65, pdY: -.2, drY: -1.2, ...medals(90, 3.6, -1.15), colLen: 0, blLen: 2.3, brLen: 2.3, glowS: 1.25}, 'i'),
    k(41, {glowS: 0, rot: [0, 0, 1.5]}), k(44, {rot: [0, 0, 0], lk: 'el'}), k(59, {}), k(60, {pos: [0, 2.55, 0], glowS: .6, glowLook: 'flash'}), k(63, {glowS: 0}),
    k(80, {...FIELD, glowLook: 'charge'}, 'io'), k(84, {})]});
// 감소 영역 (F1) in the field form: the arch stops and faces the front, the eye out, the eruption pulse, back
add({name: 'field_erupt', len: 40, next: 'field_idle', events: {activate: 0, lock: 12, erupt: 22},
  note: 'F1 감소 영역 activation: the arch slows and locks facing the front and the eye looks out (0-12, slit hot), the gold eruption pulse from the core (22: glow flash, the device bobs up 0.15 b), back to the field hover (22-40). The module runs the 9 eruption events on its own clock (play it again for a later activation).',
  keys: [k(0, {...FIELD, lk: 'charge'}), k(12, {arch: [0, 0, 0], wArch: 0, eye: [0, 0]}, 'o'), k(20, {glowS: 0, glowLook: 'flash'}),
    k(22, {glowS: 1.1, pos: [0, 5.95, 0]}, 'o'), k(25, {glowS: 0, lk: 'el'}), k(40, {...FIELD, glowLook: 'charge'}, 'io')]});
// 파쇄 in the field form (no tower build-up): vent, flame band, bursts and throws from the centre
add({name: 'frock', len: 110, next: 'field_idle', events: {vent: 0, flame: 8, burst: 25, throw: 65, end: 100},
  note: 'F2 rock throw in the field form: the vent column up (0-8), the flame band (8-25, fx), bursts from 25, throws from 65, back (100-110).',
  keys: [k(0, {...FIELD, lk: 'charge'}), k(4, {colDir: 'up', colLen: 0, colW: 1.2, colLook: 'gold'}), k(8, {colLen: 4.0, rot: [0, 0, 6]}, 'o'), k(12, {colLen: 0}), k(13, {colDir: 'down', colLook: 'violet', colW: .62}),
    k(25, {rot: [0, 0, 0]}), k(100, {lk: 'el'}), k(110, {...FIELD}, 'io')]});
// the field closes unbroken: lift-off flash, rise, lances (the spikes and medallions far out), the pack-up roll, dock
add({name: 'field_end', len: 102, next: 'idle_cruise', events: {lift: 0, rise: 2, lances: 20, horiz: 40, pack: 50, dock: 72, packed: 96},
  forms: [[40, 'deployed'], [96, 'cruise']],
  note: 'Unbroken field end: lift-off flash (0) and a 20 t rise, the lances out (20-40: the spikes and medallions to +-5.6 b, first vertical down, then horizontal at 40), the pack-up roll and rock (50-72), the lances dock and the core swings up into the hole, the pods tuck, violet fades (72-96; call look/idle at 72).',
  keys: [k(0, {...FIELD, glowS: 0, glowLook: 'flash'}), k(2, {glowS: 1.0}, 'o'), k(6, {glowS: 0}),
    k(20, {pos: [0, 6.2, 0], blLen: 0, brLen: 0, colLen: 0, ...spikes(DOCK, [0, 0, -90])}, 'io'),
    k(30, {...spikes([5.6, -.6, 0], [0, 0, -90]), ...medals(90, 5.6, -.6)}, 'o'),
    k(40, {...spikes([5.6, -.6, 0], [0, 0, 0])}, 'io'),
    k(50, {rot: [0, 0, 24]}), k(58, {rot: [0, 0, -16]}), k(64, {rot: [0, 0, 9]}),
    k(72, {...spikes(DOCK), ...medals(90, DOCK[0], DOCK[1]), rot: [0, 0, 0], pos: [0, 5.0, 0], pdY: -2.6, plY: -2.5, pl2Y: -2.3}, 'io'),
    k(81, {coreO: [0, 0, 0], arch: [-35, 0, 0], wArch: 0, pdY: -2.2, plY: -1.9, pl2Y: -1.78}, 'io'),
    k(96, {...CRUISE}, 'io'), k(102, {})]});
// 20 hits: the break (bubble burst, tilt, wobble), the groggy slump, the recovery (re-level, the core flips to the top)
const GROGGY = {...CRUISE, ...HALF, pos: [0, 3.3, 0], rot: [8, 0, 25], haloO: [.6, 1.4, 0], haloE: [0, 0, 30], coreO: [0, -.9, 0], arch: [0, 0, 0], eye: [-25, 0],
  drY: -.9, drR: 2.6, plY: -1.12, plS: .9, pl2Y: -.98, pl2S: .8, pdY: -.9, pglow: 0, ...medals(90, 3.2, -1.0), wHalo: .56, wArch: 0};
add({name: 'break', len: 34, next: 'groggy', events: {bubble: 0, burst: 5, tilt: 5, wobble: 14, sink: 34},
  note: '역장 붕괴 (the 20th hit; call crack/4 first): the bubble flares (0-5), bursts (5-7: scale 1 -> 1.6 -> 0), the whole device tilts 28 degrees in 9 t (5-14), a damped wobble +-8 -> 0 (14-34) while it sinks toward the groggy slump; link beams, violet column and the Ousia flame go out.',
  keys: [k(0, {...FIELD, shellS: 1, lk: 'el'}), k(5, {shellS: 1.12}), k(7, {shellS: 1.6, blLen: 0, brLen: 0, colLen: 0, pglow: 0}, 'o'), k(8, {shellS: 0}),
    k(14, {rot: [6, 0, 28], pos: [0, 5.0, 0], pdY: -2.5, plY: -2.6, pl2Y: -2.45, pdSw: [0, -18], lk: 'groggy'}, 'o'), k(19, {rot: [8, 0, 20], pdSw: [0, 10]}), k(24, {rot: [7, 0, 30], pdSw: [0, -8]}),
    k(29, {rot: [8, 0, 23]}), k(34, {...GROGGY, shellS: 1, pdSw: [0, 4]}, 'io')]});
add({...loopClip('groggy', GROGGY, 160, {bob: .06, period: 80, wob: 3, swing: 12}), note: 'Groggy slump: ring centre 3.3 b, roll 25 and pitch 8, the stack compressed round the sunk core, slit off / eye dim (look/groggy), halo slid and tilted, pods slow, the pendulum swinging +-12, a slow +-3 wobble. Hittable, no attacks.'});
add({name: 'recover', len: 15, next: 'idle_cruise', events: {relevel: 0, flip: 6, done: 15}, forms: [[15, 'cruise']],
  note: 'Recovery: re-level 6 t, the core flips to the top 9 t (the arch swings over), back to cruise (call look/idle at 0).',
  keys: [k(0, {...GROGGY}), k(6, {rot: [0, 0, 0], pos: [0, 4.2, 0], haloO: [0, 1.6, 0], haloE: [0, 0, 0], ...RATES}, 'io'),
    k(10, {coreO: [0, -.5, 0], arch: [90, 0, 0]}), k(15, {...CRUISE}, 'o')]});
// death (model.md §9): the seam flickers out, the halo drops and rolls off, the pods stop and fall, the spikes droop,
// the ring tilts 40 and sinks to the floor, the medallions clatter down, then everything scales out
add({name: 'death', len: 110, events: {flicker: 0, drop: 20, sink: 40, land: 60, out: 70, gone: 110},
  note: 'Death: the seam flickers hot / off three times (0-18), the eye fades; the halo drops and rolls off, the pods stop and fall, the spikes droop 45, the ring tilts 30 and sinks until its low rim rests on the floor (ring centre 2.45 b) over 40 t (20-60), the pendulum topples over, the medallions clatter down; vis scales out (70-110). Call kill after 110.',
  keys: [k(0, {...CRUISE, lk: 'charge'}), k(3, {lk: 'off'}), k(6, {lk: 'charge'}), k(9, {lk: 'off'}), k(12, {lk: 'charge'}), k(18, {lk: 'off', ...STILL}),
    k(20, {}), k(40, {haloO: [1.6, -1.2, .8], haloE: [0, 0, 70], halo2S: 0, drY: -2.6, drR: 3.0, drS: .75}, 'i'),
    k(60, {pos: [0, 2.45, 0], rot: [6, 0, 30], haloO: [2.2, -1.9, 1.0], haloE: [10, 0, 80], coreO: [0, -.6, 0], eye: [-30, 0],
      ...spikes(DOCK, [0, 0, -45]), ...medals(90, 3.4, -1.1, [-60, 90, 0]), drY: 0, drR: 2.6, plY: -1.5, pl2Y: -1.38, pdY: -1.4, pdSw: [0, -78]}, 'i'),
    k(64, {rot: [5, 0, 27]}), k(70, {}), k(110, {vis: 0}, 'i')]});

for (const c of CLIPS) if (!c.events) c.events = {};

// ---- sampling -------------------------------------------------------------------------------------------------------
export const DISCRETE = ['colDir', 'lk', 'glowLook', 'beamLook', 'colLook'];
export const accumulate = clip => accumulateClip(clip, DEFAULT_POSE);
const SPIN = {halo: 'wHalo', halo2: 'wHalo2', brim: 'wBrim', medE: 'wMedE', medG: 'wMedG', drill: 'wDrill', t1: 'wT1', t2: 'wT2', arch: 'wArch', plate: 'wPlate'};
// Integrated spin angles per tick, scaled per spinner to a whole number of turns over the clip.
const spinCache = new WeakMap();
function spinTable(clip, ks) {
  if (spinCache.has(clip)) return spinCache.get(clip);
  const rates = Array.from({length: clip.len + 1}, (_, t) => sampleAt(clip, t, ks, {defaults: DEFAULT_POSE, discrete: DISCRETE}));
  const tab = {}, turns = {};
  for (const [sp, ch] of Object.entries(SPIN)) {
    const a = [0];
    for (let t = 1; t <= clip.len; t++) a.push(a[t - 1] + (rates[t - 1][ch] + rates[t][ch]) / 2);
    const total = a[clip.len], n = Math.round(total / 360);
    const sc = n === 0 || Math.abs(total) < 1e-9 ? 0 : n * 360 / total;
    tab[sp] = a.map(x => x * sc);
    turns[sp] = n;
  }
  const out = {tab, turns};
  spinCache.set(clip, out);
  return out;
}
export function sampleClip(clip, t, ks = accumulate(clip)) {
  const p = sampleAt(clip, t, ks, {defaults: DEFAULT_POSE, discrete: DISCRETE});
  const {tab} = spinTable(clip, ks), tt = Math.max(0, Math.min(clip.len, t)), i = Math.min(clip.len - 1, Math.floor(tt)), f = tt - i;
  p.spin = Object.fromEntries(Object.keys(SPIN).map(sp => [sp, clip.len ? tab[sp][i] + (tab[sp][Math.min(clip.len, i + 1)] - tab[sp][i]) * f : 0]));
  return p;
}
export const spinTurns = clip => spinTable(clip, accumulate(clip)).turns;
// Rest pose of a form (form/<name>, the debug renders): the form's channels with the spinners at their rest angle.
export const restPose = name => ({...FORMS[name], spin: {}});
export const FORM_HOLD = {dormant: 'idle_dormant', cruise: 'idle_cruise', field: 'field_idle', coreup: 'hold_coreup', tower: 'hold_tower', laser: 'hold_laser', deployed: 'hold_deployed'};
