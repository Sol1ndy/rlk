// Clips of the Apep phase-2 objects (plan §5.1-§5.3; names, lengths, loop / next and events frozen by the day-0 org
// manifest stub, ap_contract.md §0.5.5). Used by build_mboss_apep_org.mjs.
//
// A pose is {display: {t: [x, y, z] (blocks, added to the display's joint, parent frame), r: [x, y, z] (euler degrees,
// mboss_rig_math q(): +x pitch leans back / -x bows forward, +y turns left, +z rolls), spin (degrees about the display's
// spinAxis in its parent frame, applied after r), s: number | [sx, sy, sz] (local scale; 0 = hidden), look}}.
// Keys are sparse and merge onto the accumulated pose ([tick, pose, ease]; ease io / i / o / l as mboss_rig_clips.mjs).
// A look change cuts the display's interpolation at that tick (the new model appears in its new transform, no
// one-tick slide of the old one); `cuts` adds explicit cut ticks; `cut0` snaps tick 0 (symmetric loops that wrap).
// Clip extras: displays (objects: the displays the clip drives; every display keeps its own clock), force (looks
// written at tick 0 even when unchanged), lead (none needed: each display chains itself into `next` when it is one
// of next's displays, else it stops).
import {accumulate, sampleClip} from './mboss_rig_clips.mjs';
import {q, mul, rot, aimQ, add, sub, len, toDisplayT, toDisplayQ} from './mboss_rig_math.mjs';
import {ORG, RIDE_Y, restJoint, BAG_POSE as BP} from './apep_org_geometry.mjs';

const S = k => [k, k, k];
const sq = (k, w = 1 / Math.sqrt(k)) => [w, k, w];         // volume-keeping squash / stretch along y
const PI2 = Math.PI * 2;
// a periodic channel sampled into keys every `step` ticks over [0, len]: f(t) -> pose fragment
const wave = (len, step, f) => { const out = []; for (let t = 0; t <= len; t += step) out.push([t, f(t), 'l']); if (out[out.length - 1][0] !== len) out.push([len, f(len), 'l']); return out; };
const merge = (...lists) => { const m = new Map(); for (const l of lists) for (const [t, p, e] of l) { const o = m.get(t) || [t, {}, e]; for (const [d, v] of Object.entries(p)) o[1][d] = {...(o[1][d] || {}), ...v}; if (e) o[2] = e; m.set(t, o); } return [...m.values()].sort((a, b) => a[0] - b[0]); };

// ---- the Heart scene: hang heights (the egg's lowest point above the floor, footprint.hang) and the vine ----------------
export const HANG = {entrance: 9.0, canopy: 20.0, lowered: 3.0, cs: 10.0};
const EGG = {k: .7, half: 1.6 * .7};          // the upright arrival egg: pose scale 0.7; half its length
const eggC = h => h + EGG.half;                 // the egg centre for a hang height
const wristOf = h => h + 2 * EGG.half + .12;    // the vine hand's wrist just above the egg top
const ANCHOR = [4.6, 27.5, -2.2];               // where the vine leaves the canopy rim (object frame)
// bulb + hand pose for an egg hanging at height h with a sideways sway (dx, dz) and a tilt (deg)
const hangPose = (h, dx = 0, dz = 0, tilt = 0) => ({heart_bulb: {t: [dx, eggC(h) - 1.6, dz], r: [90, 0, tilt], s: EGG.k}, vine_hand: {t: [dx * 1.05, wristOf(h) - 11.2, dz * 1.05], s: 1}});
const sunk = {heart_cradle: {t: [0, -4.6, 0]}, heart_arms: {t: [0, -4.8, 0]}, heart_tips: {t: [0, -4.8, 0]}};
const STEMS = ['vine_stem_0', 'vine_stem_1', 'vine_stem_2', 'vine_stem_3'];
const EGGSET = ['heart_bulb', 'vine_hand', ...STEMS];

// ---- clip tables ---------------------------------------------------------------------------------------------------
const C = (name, len, o) => ({name, len, loop: false, next: null, events: {}, keys: [], ...o});
export const CLIPS = {
  basic: [
    C('org_spawn', 20, {next: 'basic_bob', force: ['bulb'], note: 'emergence pop 0.85 -> 1.06 -> 1 (the spawn scale-in)',
      keys: [[0, {bulb: {s: S(.85), look: 'bell'}, crown: {s: 0}, shield: {s: 1}}], [4, {bulb: {s: [.96, 1.12, .96]}}, 'o'], [9, {bulb: {s: [1.07, .9, 1.07]}}], [14, {bulb: {s: S(1)}}], [20, {}]]}),
    C('basic_bob', 24, {loop: true, note: 'two hop-slides: squash 0.92 / stretch 1.1, up 0.15',
      keys: [[0, {bulb: {s: sq(.92), t: [0, 0, 0], r: [0, 0, 0]}, crown: {s: 0}}], [4, {bulb: {s: sq(1.1), t: [0, .1, -.02], r: [-6, 0, 0]}}, 'o'], [6, {bulb: {t: [0, .15, -.03]}}],
        [9, {bulb: {s: sq(1.03), t: [0, .07, -.01], r: [-2, 0, 0]}}], [12, {bulb: {s: sq(.92), t: [0, 0, 0], r: [0, 0, 0]}}, 'i'],
        [16, {bulb: {s: sq(1.1), t: [0, .1, -.02], r: [-6, 0, 0]}}, 'o'], [18, {bulb: {t: [0, .15, -.03]}}], [21, {bulb: {s: sq(1.03), t: [0, .07, -.01], r: [-2, 0, 0]}}],
        [24, {bulb: {s: sq(.92), t: [0, 0, 0], r: [0, 0, 0]}}, 'i']]}),
    C('basic_melee', 14, {next: 'basic_bob', events: {hit: 10}, note: 'lean back 0-5, bump 0.4 forward, hit 10, settle',
      keys: [[0, {bulb: {s: S(1), t: [0, 0, 0], r: [0, 0, 0]}}], [5, {bulb: {s: sq(.94), t: [0, 0, .06], r: [14, 0, 0]}}, 'o'], [9, {bulb: {s: sq(1.08), t: [0, .04, -.36], r: [-20, 0, 0]}}, 'i'],
        [10, {bulb: {s: sq(.96), t: [0, 0, -.42], r: [-24, 0, 0]}}], [14, {bulb: {s: S(1), t: [0, 0, 0], r: [0, 0, 0]}}, 'o']]}),
    C('basic_lie', 10, {events: {bag: 10}, note: 'bell -> bag: bows 0-3, tips over backward 3-9 (the skirt becomes the neck), the bag model at 10 (cut), crown out',
      keys: [[0, {bulb: {s: S(1), t: [0, 0, 0], r: [0, 0, 0]}, crown: {s: 0}}], [3, {bulb: {s: sq(.94), r: [-8, 0, 0]}}], [9, {bulb: {s: S(1), t: [0, .42, .12], r: [66, 0, 0]}}, 'i'],
        [10, {bulb: {s: [1.03, 1.03, .95], t: [0, BP.t, 0], r: [BP.r, 0, 0], look: 'bag'}, crown: {s: .8, r: [BP.crownR, 0, 0], look: 'closed'}}]]}),
    C('basic_ranged', 20, {events: {open: 0, fire: 12}, note: 'bag: squash 0-3, crown glow 3, petals open 5-12, launch 12, recoil, close 14-20',
      // (the bag's scales keep x = y: bulb_x, the bag's diagonal facets, is the bulb rolled 45 degrees about the bag axis)
      keys: [[0, {bulb: {s: S(1), t: [0, BP.t, 0], r: [BP.r, 0, 0], look: 'bag'}, crown: {s: 1, r: [BP.crownR, 0, 0], look: 'closed'}}], [3, {bulb: {s: [1.04, 1.04, .93]}, crown: {s: .92, look: 'open'}}],
        [6, {bulb: {s: [.98, .98, 1.05]}, crown: {s: 1.08}}, 'o'], [11, {crown: {s: 1.22, r: [BP.crownR + 4, 0, 0]}}], [12, {bulb: {s: [1.02, 1.02, .97]}, crown: {s: 1.28}}],
        [13, {bulb: {s: [.97, .97, 1.05], t: [0, BP.t, .1]}, crown: {r: [BP.crownR + 14, 0, 0]}}, 'o'], [16, {bulb: {s: S(1), t: [0, BP.t, 0]}, crown: {s: 1.0, r: [BP.crownR, 0, 0]}}],
        [17, {crown: {look: 'closed'}}], [20, {}]]}),
    C('org_die', 10, {events: {gone: 10}, force: ['bulb'], note: 'dying look (the bag keeps its form), squash, shrink to nothing',
      // (uniform scales: the clip serves the bell and the bag, whose diagonal halves turn about Y / Z)
      keys: [[0, {bulb: {look: 'dying'}}], [3, {bulb: {s: S(1.1)}, crown: {s: 0}, shield: {s: 0}}, 'o'], [7, {bulb: {s: S(.5), t: [0, -.05, 0]}}], [10, {bulb: {s: 0, t: [0, -.1, 0]}}, 'i']]}),
  ],
  nurt: [
    C('nurt_idle', 40, {loop: true, breaks: [4], note: 'stalk sway, the hood nods with a lag, the orb breathes',
      keys: merge(wave(40, 5, t => ({stalk: {r: [0, 0, 2 * Math.sin(PI2 * t / 40)]}, cap: {r: [4 * Math.sin(PI2 * (t - 6) / 40), 0, 2 * Math.sin(PI2 * (t - 6) / 40)]},
        orb: {s: S(1 + .07 * (1 - Math.cos(PI2 * t / 20)) / 2), t: [0, .03 * Math.sin(PI2 * t / 40), 0]}})))}),
    C('nurt_buff', 20, {next: 'nurt_idle', events: {tilt: 0, tethers: 8}, note: 'the hood tilts toward the targets 0-8 and opens (tilt), the orb flares at 8',
      keys: [[0, {stalk: {r: [0, 0, 0]}, cap: {r: [0, 0, 0], look: 'idle'}, orb: {s: S(1)}}], [2, {cap: {look: 'tilt'}}], [8, {stalk: {r: [-6, 0, 0]}, cap: {r: [-24, 0, 0]}, orb: {s: S(1.35), t: [0, -.02, -.06]}}, 'o'],
        [12, {orb: {s: S(1.12)}}], [17, {cap: {r: [-10, 0, 0]}}], [18, {cap: {look: 'idle'}}], [20, {stalk: {r: [0, 0, 0]}, cap: {r: [0, 0, 0]}, orb: {s: S(1), t: [0, 0, 0]}}]]}),
    C('nurt_die', 17, {events: {gone: 17}, note: 'the orb bursts, the ring goes, the stalk droops and the hood falls, shrink to nothing',
      keys: [[0, {}], [3, {orb: {s: S(1.8)}, ring: {s: 0}, stalk: {r: [0, 0, -6]}}, 'o'], [6, {orb: {s: 0}}], [11, {stalk: {r: [-8, 0, -28], s: S(.8)}, cap: {t: [.3, -.9, 0], r: [-60, 0, 20]}}, 'i'],
        [17, {stalk: {s: 0}, cap: {s: 0, t: [.4, -1.4, 0]}}, 'i']]}),
  ],
  guard: [
    C('guard_idle', 60, {loop: true, breaks: [4], note: 'the orb bobs and turns; the spire sways a little',
      keys: wave(60, 5, t => ({spire: {r: [0, 0, 1.5 * Math.sin(PI2 * t / 60)]}, orb: {t: [0, .1 * Math.sin(PI2 * t / 60), 0], r: [0, 90 * Math.sin(PI2 * t / 60), 0]}}))}),
    C('guard_cast', 30, {next: 'guard_idle', events: {collapse: 0, bud: 7, regrow: 16, regrow_end: 24, shields: 30}, note: 'collapse 0-7, bud 7-16 (glowing slit), regrow 16-24, the orb flares at the shields',
      keys: [[0, {spire: {s: S(1), t: [0, 0, 0], r: [0, 0, 0], look: 'spire'}, orb: {t: [0, 0, 0], s: S(1)}}], [6, {spire: {s: [1.08, .5, 1.08], t: [0, -1.1, 0]}, orb: {t: [0, -2.45, 0]}}, 'i'],
        [7, {spire: {look: 'bud', s: [1.06, .9, 1.06], t: [0, 0, 0]}, orb: {t: [0, -2.55, 0], s: S(.8)}}], [11, {spire: {s: [.98, 1.05, .98]}}, 'o'], [15, {spire: {s: S(1)}}],
        [16, {spire: {look: 'spire', s: [1.0, .48, 1.0], t: [0, -1.14, 0]}}], [24, {spire: {s: S(1), t: [0, 0, 0]}, orb: {t: [0, 0, 0], s: S(1)}}, 'o'], [28, {orb: {s: S(1.6)}}], [30, {orb: {s: S(1)}}]]}),
    C('guard_die', 17, {events: {gone: 17}, note: 'shudder, the black wisp at 3 (red embers: kit), fades up',
      keys: [[0, {spire: {s: S(1)}}], [2, {spire: {s: [1.06, .96, 1.06]}, orb: {s: 0}}], [3, {spire: {look: 'wisp', s: S(1), t: [0, 0, 0]}}], [10, {spire: {s: S(.9), t: [0, .25, 0]}}],
        [17, {spire: {s: 0, t: [0, .6, 0]}}, 'i']]}),
  ],
  nest: [
    C('nest_fly', 14, {loop: true, breaks: [4], note: 'wings flap V (up 28) <-> wide arch (down 14), the body bobs',
      keys: wave(14, 1, t => { const a = 7 + 21 * Math.cos(PI2 * t / 14); return {cap: {t: [0, .1 * Math.sin(PI2 * (t - 2) / 14), 0], r: [3 * Math.sin(PI2 * t / 14), 0, 0]}, wing_l: {r: [0, 0, a]}, wing_r: {r: [0, 0, -a]}}; })}),
    C('nest_cast', 12, {next: 'nest_fly', events: {walls: 12}, note: 'the wings curl up into a vertical loop round the orb, the body rises',
      keys: [[0, {cap: {t: [0, 0, 0], r: [0, 0, 0]}, wing_l: {r: [0, 0, 28]}, wing_r: {r: [0, 0, -28]}}], [8, {cap: {t: [0, .22, 0], r: [10, 0, 0]}, wing_l: {r: [0, 0, 102]}, wing_r: {r: [0, 0, -102]}}, 'o'],
        [11, {wing_l: {r: [0, 0, 110]}, wing_r: {r: [0, 0, -110]}}], [12, {cap: {t: [0, .16, 0]}}]]}),
    C('nest_blink', 6, {next: 'nest_fly', events: {out: 0, in: 3}, note: 'out 0-2 (the module moves the husk at 3), back in 3-6',
      keys: [[0, {cap: {s: S(1)}}], [2, {cap: {s: [.2, 1.6, .2]}}, 'i'], [3, {cap: {s: 0}}], [4, {cap: {s: [.3, 1.4, .3]}}], [6, {cap: {s: S(1)}}, 'o']]}),
    C('org_die', 12, {events: {gone: 12}, note: 'the wings droop, it falls to the ground and shrinks',
      keys: [[0, {}], [4, {wing_l: {r: [0, 0, -50]}, wing_r: {r: [0, 0, 50]}, cap: {r: [-20, 0, 10]}}], [9, {cap: {t: [0, -1.05, 0], r: [-50, 0, 25], s: S(.85)}}, 'i'], [12, {cap: {s: 0, t: [0, -1.15, 0]}}]]}),
  ],
  destr: [
    C('destr_roll', 32, {loop: true, cut0: true, breaks: [4], note: 'rolls on its side (face to the left), one turn per 32 t',
      keys: [[0, {shell: {r: [0, -90, 0], spin: 0}, face: {r: [0, -90, 0], spin: 0, s: S(1)}}], [32, {shell: {spin: -360}, face: {spin: -360}}, 'l']]}),
    C('destr_fuse', 56, {next: 'destr_suck', events: {pulse_1: 0, pulse_2: 9, pulse_3: 18, pulse_4: 27, pulse_5: 36, fast: 36}, note: 'upright, face to the Heart; pulses every 9 t, every 4 t from 36',
      keys: merge([[0, {shell: {r: [0, 0, 0], spin: 0, s: S(1)}, face: {r: [0, 0, 0], spin: 0, s: S(1)}}], [4, {shell: {r: [-6, 0, 0]}, face: {r: [-6, 0, 0]}}, 'o']],
        ...[0, 9, 18, 27, 36, 40, 44, 48, 52].map(p => [[p, {face: {s: S(1)}, shell: {s: S(1)}}], [p + 2, {face: {s: S(p >= 36 ? 1.36 : 1.25)}, shell: {s: S(1.04)}}, 'o'], [Math.min(56, p + 4), {face: {s: S(1)}, shell: {s: S(1)}}, 'i']]))}),
    C('destr_suck', 5, {next: 'destr_blast', note: 'shrinks white-hot', keys: [[0, {shell: {s: S(1)}, face: {s: S(1)}}], [5, {shell: {s: S(.85)}, face: {s: S(.7)}}, 'i']]}),
    C('destr_blast', 1, {events: {blast: 1}, note: 'flash; the split husk at 1 (the module then plays org_die)', keys: [[0, {shell: {s: S(1.15)}, face: {s: S(1.3)}}], [1, {shell: {look: 'husk', s: S(1)}, face: {s: 0}}]]}),
    C('org_die', 10, {events: {gone: 10}, force: ['shell'], note: 'the blackened split husk tumbles back to the ground and fades',
      keys: [[0, {shell: {look: 'husk'}, face: {s: 0}}], [6, {shell: {t: [0, -.3, .7], r: [60, 0, 0], s: S(.95)}}, 'o'], [10, {shell: {t: [0, -.45, .9], r: [80, 0, 0], s: 0}}, 'i']]}),
  ],
  pred: [
    C('pred_swim', 16, {loop: true, breaks: [4], note: 'tail fin yaw +-25, body +-8 with a 3 t lag, a slow bob',
      keys: wave(16, 1, t => ({body: {r: [2 * Math.sin(PI2 * t / 16), 8 * Math.sin(PI2 * (t - 3) / 16), 0], t: [0, .07 * Math.sin(PI2 * t / 16), 0], s: S(1), look: 'fish'}, fin: {r: [0, 25 * Math.sin(PI2 * t / 16), 0], s: S(1)},
        jaw: {r: [-3 - 3 * Math.sin(PI2 * t / 16), 0, 0], s: S(1)}, core: {s: S(1)}}))}),
    C('pred_swallow', 24, {next: 'pred_bud', events: {eat: 12, bud: 14}, note: 'rears 0-6, scoops 6-12 (eat), closes into the bud at 14',
      keys: [[0, {body: {r: [0, 0, 0], t: [0, 0, 0]}, jaw: {r: [0, 0, 0]}, fin: {r: [0, 0, 0]}}], [6, {body: {r: [34, 0, 0], t: [0, .45, .2]}, jaw: {r: [-32, 0, 0]}}, 'o'],
        [11, {body: {r: [-40, 0, 0], t: [0, -.55, -.6]}, jaw: {r: [-42, 0, 0]}}, 'i'], [12, {jaw: {r: [-4, 0, 0]}}], [13, {body: {r: [-20, 0, 0], t: [0, -.3, -.3]}}],
        [14, {body: {look: 'bud', r: [0, 0, 0], t: [0, .1, 0], s: S(.8)}, jaw: {s: 0}, fin: {s: 0}, core: {s: S(1.2)}}], [20, {body: {s: S(1.05)}}, 'o'], [24, {body: {s: S(1), t: [0, .2, 0]}, core: {s: S(1)}}]]}),
    C('pred_bud', 20, {loop: true, cut0: true, note: 'spins 45 degrees per loop (8-fold), bobs over the gold swirl; the core pulses',
      keys: merge(wave(20, 5, t => ({body: {look: 'bud', r: [0, 45 * t / 20, 0], t: [0, .2 + .08 * Math.sin(PI2 * t / 20), 0], s: S(1)}, core: {s: S(1 + .15 * Math.sin(Math.PI * t / 10) ** 2)}, jaw: {s: 0}, fin: {s: 0}})))}),
    C('pred_inflate', 10, {next: 'pred_burst', force: ['body'], note: 'the pod grows from the ground (its own model) over 8 t',
      keys: [[0, {body: {look: 'pod', r: [0, 0, 0], s: S(.55), t: [0, -1.3 * .45, 0]}, jaw: {s: 0}, fin: {s: 0}, core: {s: S(.9), t: [0, -.55, 0]}}], [8, {body: {s: S(1.04), t: [0, 0, 0]}, core: {s: S(1.3), t: [0, -.45, -.1]}}, 'o'],
        [10, {body: {s: S(1)}}]]}),
    C('pred_burst', 10, {next: 'pred_swim', events: {hit: 0, fish: 2}, note: 'the pod bursts (hit 0), the fish again at 2',
      keys: [[0, {body: {s: S(1.12)}, core: {s: S(1.6)}}], [2, {body: {look: 'fish', s: S(.9), t: [0, 0, 0], r: [0, 0, 0]}, jaw: {s: S(.9), r: [-20, 0, 0]}, fin: {s: S(.9)}, core: {s: S(1), t: [0, 0, 0]}}],
        [6, {body: {s: S(1.03)}, jaw: {s: S(1), r: [-4, 0, 0]}, fin: {s: S(1)}}, 'o'], [10, {body: {s: S(1)}}]]}),
    C('pred_bite', 6, {next: 'pred_swim', events: {open: 0, hit: 4}, note: 'jaw open 0-3 with the spikes flared, snap 4 (the module lunges the husk)',
      keys: [[0, {body: {r: [0, 0, 0], look: 'fish'}, jaw: {r: [-4, 0, 0]}}], [2, {body: {look: 'fish_flare'}}], [3, {body: {r: [6, 0, 0]}, jaw: {r: [-38, 0, 0]}}, 'o'], [4, {body: {r: [-12, 0, 0]}, jaw: {r: [0, 0, 0]}}, 'i'],
        [5, {body: {look: 'fish'}}], [6, {body: {r: [0, 0, 0]}}]]}),
    C('pred_bite_chain', 38, {next: 'pred_swim', events: {hit_1: 4, hit_2: 10, hit_3: 16, hit_4: 22}, note: '4 snaps 6 t apart (the module starts it 8 t before the first sector strike)',
      keys: merge([[0, {body: {look: 'fish', r: [0, 0, 0]}, jaw: {r: [-4, 0, 0]}}], [2, {body: {look: 'fish_flare'}}], [24, {body: {look: 'fish'}}], [38, {body: {r: [0, 0, 0]}, jaw: {r: [-4, 0, 0]}}, 'o']],
        ...[4, 10, 16, 22].map(h => [[h - 3, {body: {r: [6, 0, 0]}, jaw: {r: [-36, 0, 0]}}, 'o'], [h, {body: {r: [-12, 0, 0]}, jaw: {r: [0, 0, 0]}}, 'i']]))}),
    C('org_die', 12, {events: {gone: 12}, note: 'the core flashes out, the fish sinks to the ground nose first and shrinks',
      keys: [[0, {}], [2, {core: {s: S(1.6)}, jaw: {r: [-30, 0, 0]}}], [5, {core: {s: 0}}], [9, {body: {r: [-35, 0, 12], t: [0, -1.1, 0], s: S(.9)}}, 'i'], [12, {body: {s: 0, t: [0, -1.2, 0]}, jaw: {s: 0}, fin: {s: 0}}]]}),
  ],
  heart: [
    C('heart_hang', 80, {loop: true, displays: EGGSET, note: 'the egg hangs in the canopy (hang canopy_y), swaying',
      keys: wave(80, 4, t => hangPose(HANG.canopy, .7 * Math.sin(PI2 * t / 80), .35 * Math.sin(2 * PI2 * t / 80), -6 * Math.sin(PI2 * t / 80)))}),
    C('heart_up', 30, {next: 'heart_hang', displays: EGGSET, note: 'drawn up from the entrance height (9 b) into the canopy',
      keys: [[0, hangPose(HANG.entrance)], [30, hangPose(HANG.canopy)]]}),
    C('heart_lower', 50, {displays: EGGSET, note: 'lowered from the canopy to the lowered height, swaying 1-2 b and calming',
      keys: wave(50, 5, t => { const u = t / 50, e = u * u * (3 - 2 * u), sw = 1.1 * (1 - u); return hangPose(HANG.canopy + (HANG.lowered - HANG.canopy) * e, sw * Math.sin(PI2 * t / 34), .4 * sw * Math.sin(PI2 * t / 21), -5 * (1 - u) * Math.sin(PI2 * t / 34)); })}),
    C('heart_drop', 30, {next: 'heart_idle', displays: [...EGGSET, 'heart_cradle', 'heart_tips'], events: {land: 6, beam: 6, beam_end: 16},
      note: 'released at 0, falls 0-5, lands 6 (pitches to lying, 0.7 -> 1, squash), settles; the hand rises away; the cradle full at 6',
      keys: [[0, {...hangPose(HANG.lowered), heart_cradle: {t: [0, 0, 0], look: 'pedestal'}, heart_tips: {r: [0, 0, 0]}}],
        [5, {heart_bulb: {t: [0, 1.25, 0], r: [70, 0, 0], s: .8}, vine_hand: {t: [0, wristOf(HANG.lowered) - 11.2 + .3, 0]}}, 'i'],
        [6, {heart_bulb: {t: [0, -.12, 0], r: [0, 0, 0], s: [1.08, .86, 1.08]}, heart_cradle: {look: 'full', s: [1.02, .95, 1.02]}, heart_tips: {r: [0, 4, 0]}}],
        [9, {heart_bulb: {t: [0, .04, 0], s: [.98, 1.04, .98]}, heart_cradle: {s: S(1)}, heart_tips: {r: [0, -3, 0]}}, 'o'], [13, {heart_bulb: {t: [0, 0, 0], s: S(1)}, heart_tips: {r: [0, 0, 0]}}],
        [30, {vine_hand: {t: [0, wristOf(HANG.canopy) - 11.2 + 3, 0], s: 0}}, 'i']]}),
    C('heart_idle', 40, {loop: true, displays: ['heart_bulb', 'heart_tips'], note: 'the bulb breathes 1.00 <-> 1.03, the sprouts sway',
      keys: wave(40, 5, t => ({heart_bulb: {t: [0, 0, 0], r: [0, 0, 0], s: S(1 + .015 * (1 - Math.cos(PI2 * t / 20)))}, heart_tips: {r: [0, 3 * Math.sin(PI2 * t / 40), 0], s: S(1 + .02 * Math.sin(PI2 * t / 20))}}))}),
    C('heart_hit', 6, {next: 'heart_idle', displays: ['heart_bulb', 'heart_tips'], note: 'a flinch',
      keys: [[0, {heart_bulb: {s: S(1), t: [0, 0, 0]}}], [1, {heart_bulb: {s: [1.05, .93, 1.05], t: [.05, -.04, 0]}, heart_tips: {r: [0, 3, 0]}}, 'o'], [3, {heart_bulb: {s: [.98, 1.03, .98], t: [-.03, 0, 0]}, heart_tips: {r: [0, -2, 0]}}],
        [6, {heart_bulb: {s: S(1), t: [0, 0, 0]}, heart_tips: {r: [0, 0, 0]}}, 'o']]}),
    C('heart_gain', 8, {next: 'heart_idle', displays: ['heart_bulb', 'heart_tips'], note: 'a bright swell',
      keys: [[0, {heart_bulb: {s: S(1)}, heart_tips: {s: S(1)}}], [2, {heart_bulb: {s: S(1.07)}, heart_tips: {s: S(1.12)}}, 'o'], [8, {heart_bulb: {s: S(1)}, heart_tips: {s: S(1)}}, 'io']]}),
    C('heart_wither', 30, {displays: ['heart_bulb', 'heart_tips'], force: ['heart_bulb'], note: 'the withered look at 0, sags and shrinks a little, the sprouts droop',
      keys: [[0, {heart_bulb: {look: 'withered', s: S(1)}}], [4, {heart_bulb: {s: [1.05, .9, 1.05]}}], [30, {heart_bulb: {s: S(.92), t: [0, -.16, 0]}, heart_tips: {s: S(.6), t: [0, -.9, 0]}}, 'o']]}),
    C('heart_blaze', 24, {displays: ['heart_bulb', 'heart_tips'], force: ['heart_bulb'], note: 'blazes (CS 0-24): bright look, swelling pulses',
      keys: [[0, {heart_bulb: {look: 'blaze', s: S(1)}, heart_tips: {s: S(1)}}], [6, {heart_bulb: {s: S(1.08)}, heart_tips: {s: S(1.3)}}, 'o'], [10, {heart_bulb: {s: S(1.03)}}], [16, {heart_bulb: {s: S(1.12)}}, 'o'], [24, {heart_bulb: {s: S(1.08)}, heart_tips: {s: S(1.2)}}]]}),
    C('heart_lift', 46, {displays: EGGSET, force: ['heart_bulb', 'vine_hand'], note: 'golden egg lifts out of the cradle (0-30) to hang cs_y, the vine hand comes down 20-40 and wraps at 40',
      keys: [[0, {heart_bulb: {look: 'egg_gold', t: [0, 0, 0], r: [0, 0, 0], s: S(1.08)}, vine_hand: {t: [0, wristOf(HANG.canopy) - 11.2, 0], s: 0, look: 'idle'}}],
        [20, {heart_bulb: {t: [0, eggC(HANG.cs) - 1.6 - 1.2, 0], r: [90, 0, 0], s: EGG.k}}, 'io'], [21, {vine_hand: {s: 1}}], [30, {heart_bulb: {t: [0, eggC(HANG.cs) - 1.6, 0]}}, 'o'],
        [40, {vine_hand: {t: [0, wristOf(HANG.cs) - 11.2, 0]}}, 'o'], [41, {vine_hand: {look: 'wrap'}}], [46, {}]]}),
    C('cradle_rise', 20, {displays: ['heart_cradle', 'heart_arms', 'heart_tips'], force: ['heart_cradle'], note: 'the cradle (pedestal look), arms and sprouts rise out of the ground',
      keys: [[0, {...sunk, heart_cradle: {t: [0, -4.6, 0], look: 'pedestal'}}], [14, {heart_cradle: {t: [0, .15, 0]}, heart_arms: {t: [0, .15, 0]}, heart_tips: {t: [0, .15, 0]}}, 'o'],
        [20, {heart_cradle: {t: [0, 0, 0]}, heart_arms: {t: [0, 0, 0]}, heart_tips: {t: [0, 0, 0]}}, 'io']]}),
    C('cradle_sink', 10, {displays: ['heart_cradle', 'heart_arms', 'heart_tips'], note: 'back into the ground',
      keys: [[0, {heart_cradle: {t: [0, 0, 0]}, heart_arms: {t: [0, 0, 0]}, heart_tips: {t: [0, 0, 0]}}], [10, sunk, 'i']]}),
  ],
  dome: [
    C('dome_rise', 10, {next: 'dome_idle', displays: ['dome_shell', 'dome_decor'], note: 'grows up from the footprint, a small overshoot',
      keys: [[0, {dome_shell: {s: [.35, .02, .35]}, dome_decor: {s: [.35, .02, .35]}}], [5, {dome_shell: {s: [1.05, .72, 1.05]}, dome_decor: {s: [1.05, .7, 1.05]}}, 'o'],
        [8, {dome_shell: {s: [1.01, 1.05, 1.01]}, dome_decor: {s: [1.01, 1.05, 1.01]}}], [10, {dome_shell: {s: S(1)}, dome_decor: {s: S(1)}}]]}),
    C('dome_idle', 40, {loop: true, displays: ['dome_shell', 'dome_decor'], note: 'a faint breath', keys: wave(40, 10, t => ({dome_shell: {s: S(1)}, dome_decor: {s: S(1 + .012 * Math.sin(PI2 * t / 40))}}))}),
    C('dome_pop', 6, {displays: ['dome_shell', 'dome_decor'], note: 'swells and pops (shards: kit)', keys: [[0, {dome_shell: {s: S(1)}, dome_decor: {s: S(1)}}], [2, {dome_shell: {s: S(1.07)}, dome_decor: {s: S(1.07)}}, 'o'], [6, {dome_shell: {s: 0}, dome_decor: {s: 0}}, 'i']]}),
  ],
  wall: [
    C('wall_rise', 5, {displays: ['wall_blade'], note: 'shoots up from the ground', keys: [[0, {wall_blade: {s: [.6, .05, .6]}}], [3, {wall_blade: {s: [1, 1.08, 1]}}, 'o'], [5, {wall_blade: {s: S(1)}}]]}),
    C('wall_fade', 8, {displays: ['wall_blade'], note: 'shrinks into the ground (motes: kit)', keys: [[0, {wall_blade: {s: S(1), t: [0, 0, 0]}}], [8, {wall_blade: {s: [.75, 0, .75], t: [0, -.3, 0]}}, 'i']]}),
  ],
  stalk: [
    C('leg_rise', 10, {displays: ['stalk_low', 'stalk_high', 'stalk_tip'], note: 'bursts up from below the floor, leaning back from the lock, the upper segments whip',
      keys: [[0, {stalk_low: {t: [0, -6.4, 0], r: [0, 0, 0]}, stalk_high: {r: [10, 0, 0]}, stalk_tip: {r: [25, 0, 0]}}], [7, {stalk_low: {t: [0, .12, 0], r: [10, 0, 0]}, stalk_high: {r: [-6, 0, 0]}, stalk_tip: {r: [-18, 0, 0]}}, 'o'],
        [10, {stalk_low: {t: [0, 0, 0], r: [8, 0, 0]}, stalk_high: {r: [12, 0, 0]}, stalk_tip: {r: [-10, 0, 0]}}]]}),
    C('leg_slam', 6, {displays: ['stalk_low', 'stalk_high', 'stalk_tip'], events: {hit: 4}, note: 'slams forward onto the ground toward the lock (hit 4), a bounce',
      keys: [[0, {stalk_low: {r: [8, 0, 0], t: [0, 0, 0]}, stalk_high: {r: [12, 0, 0]}, stalk_tip: {r: [-10, 0, 0]}}], [1, {stalk_low: {r: [14, 0, 0]}, stalk_high: {r: [18, 0, 0]}}, 'o'],
        [4, {stalk_low: {r: [-84, 0, 0]}, stalk_high: {r: [-4, 0, 0]}, stalk_tip: {r: [8, 0, 0]}}, 'i'], [5, {stalk_low: {r: [-79, 0, 0]}, stalk_high: {r: [-8, 0, 0]}}], [6, {stalk_low: {r: [-84, 0, 0]}, stalk_high: {r: [-2, 0, 0]}}]]}),
    C('leg_sink', 10, {displays: ['stalk_low', 'stalk_high', 'stalk_tip'], note: 'sinks back through the floor',
      keys: [[0, {stalk_low: {t: [0, 0, 0], r: [-84, 0, 0]}, stalk_high: {r: [-2, 0, 0]}}], [10, {stalk_low: {t: [0, -1.7, 0], s: S(.9)}}, 'i']]}),
  ],
  seed: [],
};
// frozen ids (stub order): kinds then objects, clips in table order
let NEXT_ID = 0;
for (const o of ['basic', 'nurt', 'guard', 'nest', 'destr', 'pred', 'heart', 'dome', 'wall', 'stalk', 'seed']) for (const c of CLIPS[o]) c.id = NEXT_ID++;

// objects' spawn states: {state: {display: [clip, tick] | pose fragment}} (the initial transforms and looks)
export const SPAWN = {
  heart: {
    entrance: {note: 'E: the egg held by the vine hand at the entrance height, the cradle under the floor', from: {...Object.fromEntries(EGGSET.map(d => [d, ['heart_up', 0]])), heart_cradle: ['cradle_rise', 0], heart_arms: ['cradle_rise', 0], heart_tips: ['cradle_rise', 0]}},
    canopy: {note: 'phase 1 (and a reload in P1): hanging in the canopy', from: {...Object.fromEntries(EGGSET.map(d => [d, ['heart_hang', 0]])), heart_cradle: ['cradle_rise', 0], heart_arms: ['cradle_rise', 0], heart_tips: ['cradle_rise', 0]}},
    play: {note: 'phase 2 (and a reload in T1 / P2): lying in the full cradle; the hand and the stems gone', from: {heart_bulb: ['heart_idle', 0], heart_cradle: ['heart_drop', 30], heart_arms: ['cradle_rise', 20], heart_tips: ['heart_idle', 0],
      vine_hand: ['heart_drop', 30], ...Object.fromEntries(STEMS.map(d => [d, ['heart_drop', 30]]))}},
  },
};

// ---- sampling ---------------------------------------------------------------------------------------------------------
const vec3 = v => (typeof v === 'number' ? [v, v, v] : v);
function defaults(owner) {
  const o = {};
  for (const d of ORG[owner].displays) { o[d.name + '.t'] = [0, 0, 0]; o[d.name + '.r'] = [0, 0, 0]; o[d.name + '.s'] = [1, 1, 1]; o[d.name + '.spin'] = 0; o[d.name + '.look'] = d.def; }
  return o;
}
const flatten = pose => { const o = {}; for (const [d, v] of Object.entries(pose)) for (const [k, x] of Object.entries(v)) o[d + '.' + k] = k === 's' ? vec3(x) : x; return o; };
export function clipKeys(owner, c) {
  const defs = defaults(owner);
  return accumulate({...c, keys: c.keys.length ? c.keys.map(([t, p, e]) => [t, flatten(p), e]) : [[0, {}]]}, defs);
}
// the pose channels at tick t (structured per display)
export function poseAt(owner, c, t, ks = clipKeys(owner, c)) {
  const p = sampleClip(c, t, ks, {defaults: defaults(owner), discrete: ORG[owner].displays.map(d => d.name + '.look')});
  const out = {};
  for (const d of ORG[owner].displays) out[d.name] = {t: p[d.name + '.t'], r: p[d.name + '.r'], s: p[d.name + '.s'], spin: p[d.name + '.spin'], look: p[d.name + '.look']};
  // a display with lookOf shows its leader's look (the same look names)
  for (const d of ORG[owner].displays) if (d.lookOf) out[d.name].look = out[d.lookOf].look;
  return out;
}
const AXQ = (axis, deg) => q(axis === 'x' ? [deg, 0, 0] : axis === 'y' ? [0, deg, 0] : [0, 0, deg]);
// world transforms (object frame) of every display: {name: {t, q, s (vec3), look}}
export function solve(owner, pose) {
  const W = {};
  for (const d of ORG[owner].displays) {
    // a follow display copies its parent's transform (scale included) turned by follow(look) in the parent's frame; the
    // parent's scales must commute with that turn (x = z for a turn about Y, x = y for one about Z: clipCheck)
    if (d.follow) { const par = W[d.parent], look = pose[d.name].look; W[d.name] = {t: par.t, q: mul(par.q, q(d.follow(look))), k: par.k, s: par.s.slice(), look}; continue; }
    const P = pose[d.name], par = d.parent ? W[d.parent] : {t: [0, 0, 0], q: [0, 0, 0, 1], k: 1};
    let R = q(P.r);
    if (d.spinAxis || P.spin) R = mul(AXQ(d.spinAxis || 'x', P.spin || 0), R);
    const T = add(d.joint, P.t);
    const t = add(par.t, rot(par.q, T.map(x => x * par.k))), Q = mul(par.q, R), k = par.k * P.s[0];
    W[d.name] = {t, q: Q, k, s: P.s.map(x => x * par.k), look: P.look};
  }
  if (owner === 'heart') vineStems(W);
  return W;
}
// the Heart's vine stems hang from the canopy rim to the hand's wrist along a quadratic curve; each segment display is
// aimed down its chord and stretched to its length (the stem model is 6.2 b long)
function vineStems(W) {
  const hand = W.vine_hand, shown = hand.s[1] > 1e-3, A = ANCHOR, Wr = add(hand.t, [0, .05, 0]);
  const Cc = [(A[0] + Wr[0]) / 2 + .9, (A[1] + Wr[1]) / 2 + 1.2, (A[2] + Wr[2]) / 2];
  const P = u => [0, 1, 2].map(i => (1 - u) ** 2 * A[i] + 2 * (1 - u) * u * Cc[i] + u * u * Wr[i]);
  STEMS.forEach((n, k) => {
    const a = P(k / 4), b = P((k + 1) / 4), d = sub(b, a), L = len(d);
    W[n] = {t: a, q: aimQ(d, [0, 0, -1]), k: 1, s: shown ? [1, L / 6.2, 1] : [0, 0, 0], look: W[n].look};
  });
}
// the display transform (display space, as written into the NBT): organisms hang from the passenger point
export function displayXf(owner, name, w) {
  const d = ORG[owner].displays.find(x => x.name === name), base = ORG[owner].type === 'kind' ? [0, RIDE_Y, 0] : [0, 0, 0];
  return {t: toDisplayT(sub(w.t, base)), q: toDisplayQ(w.q), s: w.s.map(x => x * d.scale)};
}
export {restJoint};
