// The 8 cinematic clips of the 홍련 (Scarlet) rig (OWNER: S2b; S:hr/PLAN.md §3.1-§3.7, the shot lists of
// S:hr/understand/cutscenes.md; contract tools/mboss_scarlet/api.py CLIPS: names, lengths and event ticks are frozen, this
// file only authors the motion). tools/build_scarlet_rig.mjs imports it (export CLIPS = exactly the clips api.CLIP_OWNER gives
// S2b) and checks / compiles them like S2a's clips (keys 0..len, the floor at every compiled tick, <= 120 degrees per tick,
// the culling box). Format, pose channels and helpers: tools/scarlet_rig_api.md §5-§6, tools/scarlet_pose.mjs.
//
// Root motion is never in a clip: the sequences (tools/mboss_scarlet/seq.py) move and turn the body (mboss/mv/*, rig face/*);
// the clips pose her about the anchor, time their motion to the contract events and key the hat / sword / scabbard / face /
// hands / cup / bottle states at their own ticks. Walks are walks in place whose planted foot travels back at the body's glide
// speed (linear keys). Hand-overs: intro 554 = intro_end 0; cs1 213 = sq1 0; repel starts in LOCK (g_deflect's end) and ends
// lying like DOWN (the down window's clip); lead_down starts in DOWN; sq1 / lead_down / lead_stand end in g_brim's hold (the
// gauntlet's g_tell starts from it); ending ends exactly in H_POSE (= tick 0 of ev_give / ev_toast).
import {K, B, SW, ST, ST2, CROUCH, LOW, AIR, LOCK, DOWN, H_POSE, DEFAULT_POSE, F_ST, F_WIDE, F_LUNGE, F_TOG} from './scarlet_clips.mjs';
import {hipDirChannels} from './scarlet_retarget.mjs';

const DEG = Math.PI / 180;
// a flip about her centre of mass (c b above the pelvis pivot): the pelvis offset keeping it in place at pitch pt; y0 lifts it
const flipPos = (pt, c = .5, y0 = 0) => [0, +(y0 + c * (1 - Math.cos(pt * DEG))).toFixed(3), +(-c * Math.sin(pt * DEG)).toFixed(3)];
const FULL = p => ({...DEFAULT_POSE, ...p});        // a key that resets every channel (hand-over poses)

// a key list built in any order, sorted by tick; duplicate ticks merge (later wins per channel)
function Keys() {
  const m = new Map();
  const api = {
    k(t, pose, ease = 'io') {
      if (!Number.isInteger(t) || t < 0) throw new Error(`key tick ${t}`);
      const o = m.get(t);
      m.set(t, o ? [t, {...o[1], ...pose}, ease] : [t, pose, ease]);
      return api;
    },
    all(list) { for (const [t, p, e] of list) api.k(t, p, e); return api; },
    done(len) {
      const ks = [...m.values()].sort((a, b) => a[0] - b[0]);
      if (ks[0][0] !== 0 || ks[ks.length - 1][0] !== len) throw new Error(`keys must run 0..${len}`);
      return ks;
    },
  };
  return api;
}

// ---- shared pieces -----------------------------------------------------------------------------------------------------------
// the sheathed sword at the right hip, the left arm free
const SHEATHED = {hold: 0, sword: 'sheathed', scab: 'hip', hL: 'open'};
// the sheathed sword carried in the right hand by the throat (the mouth / hilt forward of the hand), trailing back at her side
const CARRY = {scab: 'hand', hR: 'grip', scB: 172, scE: -16, scR: 0, scOff: .2, aR: [14, 16, .95], hsR: 0, pR: [.55, -.35, .75]};
// raised upright before her right shoulder (hilt up; PLAN §3.1 E10 = intro_end 0)
const UPRIGHT = {scab: 'hand', hR: 'grip', scB: 18, scE: -68, scR: 0, scOff: .25, aR: [84, -8, .62], pR: [.6, -.4, .4], hsR: 0};
// the hip scabbard (scarlet_pose SK.scabHipDir, edge up) as a hand bearing / elevation / roll and the throat grip: the hip <->
// hand hand-over key (S2d: derived from the skeleton, scarlet_retarget.mjs hipDirChannels, so the hand-overs have no jump)
const HIP_DIR = hipDirChannels();
// g_brim's hold (the right hand at the brim; S2a's BR) = the end pose of sq1 / lead_down / lead_stand (g_tell starts from it)
const BRIM_R = {...ST2, hR: 'brim', bwR: 1, bzR: 30, pR: [.8, -.2, .3], head: [-8, -6, 0], hat: 'worn'};
// the iai stance under the brim (CS1 C4-C5): the left hand on the sheathed hilt at the right hip, the right on the throat
const IAI = {...ST, pos: [0, -.26, 0], ...F_WIDE, fL: [.27, .1, -.34], fR: [-.25, .1, .3], tor: [-18, -22, 0], head: [-20, 18, 0],
  ...SHEATHED, hL: 'grip', hR: 'grip', hiL: 1, hsR: 1, aL: [40, 10, .8], aR: [20, 10, .8], skF: 1.1};
// the twisted post-slash crouch of 홍련일섬 (CS1 C8 = sq1 0): the blade swept out low to her left, the body twisted
const SLASHED = {...ST, pos: [0, -.42, 0], fL: [.32, .1, -.4], fR: [-.26, .1, .36], tor: [-24, -44, 0], head: [-4, 30, 0], hold: 1,
  sword: 'hand', scab: 'hip', hL: 'grip', hR: 'open', gF: 0, gB: -112, gE: -28, gD: .72, cB: -118, cR: 0, th: -14, ed: -1, tw: 0, rh: 0,
  aR: [40, 40, .9], hiL: 0, hsR: 0, hairS: -.3, skW: .3};

// a walk in place over (t0, t1] (the sequence glides the body at 2 s / (P / 2) b/t): contacts every P / 2 (left foot forward at
// t0), keys every P / 4, linear so a planted foot travels back at the glide speed; the free left arm swings against the legs
function walk(t0, t1, {P = 16, s = .6, armL = true, lean = -4} = {}) {
  const q = P / 4, out = [];
  for (let i = 1, t = t0 + q; t <= t1; i++, t += q) {
    const ph = i % 4;
    const legs = [
      {fL: [.12, .1, -s], fR: [-.12, .12, s * .85], pos: [0, -.07, 0], rot: [0, -3, 0]},
      {fL: [.12, .1, 0], fR: [-.12, .27, -.05], pos: [0, -.02, 0], rot: [0, 0, 0]},
      {fL: [.12, .12, s * .85], fR: [-.12, .1, -s], pos: [0, -.07, 0], rot: [0, 3, 0]},
      {fL: [.12, .27, -.05], fR: [-.12, .1, 0], pos: [0, -.02, 0], rot: [0, 0, 0]},
    ][ph];
    const sw = [-1, 0, 1, 0][ph];
    out.push([t, {...legs, tor: [lean, 4 * sw, 0], ...(armL ? {aL: [16 * sw, 8, .97]} : {})}, 'l']);
  }
  return out;
}
// side steps to her right (dir -1) or left (1) over (t0, t1], one step every P / 2 (the sequence glides the body sideways)
function side(t0, t1, {P = 16, w = .34, dir = -1} = {}) {
  const q = P / 4, out = [];
  const lead = dir < 0 ? 'fR' : 'fL', trail = dir < 0 ? 'fL' : 'fR', sx = dir;
  for (let i = 1, t = t0 + q; t <= t1; i++, t += q) {
    const ph = i % 4;
    const k = [
      {[lead]: [sx * .14, .1, 0], [trail]: [-sx * .14, .1, 0], pos: [0, -.08, 0]},                 // together
      {[lead]: [sx * (.14 + w), .2, 0], [trail]: [-sx * (.14 - w / 2), .1, 0], pos: [0, -.05, 0]},  // the lead foot steps out
      {[lead]: [sx * (.14 + w / 2), .1, 0], [trail]: [-sx * (.14 + w / 2), .1, 0], pos: [0, -.1, 0]}, // wide (both planted)
      {[lead]: [sx * (.14 - w / 2), .1, 0], [trail]: [-sx * (.14 - w), .2, 0], pos: [0, -.05, 0]},  // the trail foot closes
    ][ph];
    out.push([t, k, 'l']);
  }
  return out;
}
// every tick from t0 to t1 (inclusive) a pose from f(u) (u 0..1): big swings keyed every tick
function every(t0, t1, f, ease = 'l') {
  const out = [];
  for (let t = t0; t <= t1; t++) out.push([t, f((t - t0) / Math.max(1, t1 - t0)), ease]);
  return out;
}
const lerp = (a, b, u) => a + (b - a) * u;
const lerp3 = (a, b, u) => a.map((x, i) => +(x + (b[i] - x) * u).toFixed(3));
const sm = u => u * u * (3 - 2 * u);

const clips = [];
const C = (name, len, keys, extra = {}) => clips.push({name, keys: keys.done(len), ...extra});

// =================================================================================================================================
// intro (554 t; PLAN §3.1 E0-E10, wiki lines 1-10; staged from the poem's meaning — the footage skips it: v1s_intro_stairs)
// Seated on the kit's seat_rock (the core turns the body to the moon; her back to the arriving player), the cup in her right hand,
// the sheathed sword at her right hip. E1 the bottle from the rock in her left hand (24, the kit rock look bare), pours 30-44,
// back 52; E2 the cup to her lips 70, sips 78-86, down 94; E3 the cup raised to the moon 110-140; E4 she looks down at her shadow
// on her right 160-180; E5 the cup set down 206 (the rock look set), rises 214-244, turns (248-268: the sequence turns the body;
// the feet step), the laughing head tilt 270-290; E6 the scabbard from the hip into the right hand 292-310, walks 312-396 (16-t
// cycle, 0.15 b/t); E8 stops, the open left hand sweeps from the moon (behind her) across the field 402-432; E9 walks 444-490;
// E10 stops, raises the scabbard upright before her right shoulder 510 (= intro_end 0).
{
  // sitting at her knee height (the stone's top ~0.75 b): the pelvis 0.96 b, the knees forward over the planted feet
  const SEAT = {...ST, pos: [0, -.40, .10], rot: [0, 0, 0], tor: [-6, 0, 0], head: [-6, 0, 0], fL: [.12, .1, -.30], fR: [-.12, .1, -.26],
    kL: [.08, 0, -1], kR: [-.08, 0, -1], ...SHEATHED, hR: 'grip', aR: [70, 12, .55], aL: [35, 8, .62], pL: [.55, -.35, .75],
    pR: [.55, -.35, .75], cup: 'hand', bottle: 'none', cupT: 0, botT: 0, skG: .6, plwL: 0, plwR: 0, hsR: 0, hiL: 0};
  const k = Keys().k(0, FULL(SEAT)).k(10, {tor: [-5, 0, 1]}).k(20, {tor: [-6, 0, 0]});
  // E1: the bottle (on the rock at her left) — reach 20-24, lift 24-30, pour 30-44, back 46-52
  k.k(23, {aL: [24, 34, .8], tor: [-9, -10, -4], head: [-12, -16, 0]}, 'o')
    .k(24, {hL: 'grip', bottle: 'hand', plL: [.5, .84, .04], plwL: 1, tor: [-11, -14, -6]})
    .k(29, {plwL: 0, aL: [72, -32, .6], tor: [-8, -4, 0], head: [-14, -4, 0], botT: -20}, 'o')
    .k(32, {aL: [76, -36, .58], botT: -58}).k(44, {aL: [78, -38, .58], botT: -72, head: [-16, -2, 0]})
    .k(47, {botT: -6, aL: [56, -10, .62]}).k(51, {plwL: 1, plL: [.5, .84, .04], tor: [-11, -14, -6], head: [-12, -16, 0]}, 'i')
    .k(52, {bottle: 'none', hL: 'open', botT: 0}).k(58, {plwL: 0, aL: [35, 8, .62], tor: [-6, 0, 0], head: [-6, 0, 0]});
  // E2: the cup to her lips 62-70, sips 78-86, lowered 94
  k.k(62, {}).k(70, {aR: [116, -36, .44], cupT: 18, head: [2, 2, 0]}).k(78, {aR: [120, -36, .43], cupT: 38, head: [10, 2, 0]})
    .k(86, {cupT: 38, head: [10, 2, 0]}).k(94, {aR: [70, 12, .55], cupT: 0, head: [-6, 0, 0]}).k(102, {});
  // E3: raised to the moon 110-140
  k.k(110, {aR: [150, 10, .95], head: [22, 0, 0], tor: [6, 4, 0], cupT: 8}).k(125, {head: [24, -2, 0], tor: [7, 4, 1]})
    .k(140, {aR: [152, 8, .96], head: [24, -2, 0], tor: [6, 4, 0]});
  // E4: lowered, the look down at her shadow on her right 160-180, a slow sway
  k.k(146, {}).k(160, {aR: [64, 14, .55], cupT: 0, head: [-24, 30, 0], tor: [-8, 10, 2]}).k(170, {tor: [-8, 12, -2], head: [-23, 32, 0]})
    .k(180, {head: [-22, 34, 0], tor: [-8, 10, 2]}).k(196, {head: [-6, 4, 0], tor: [-6, 2, 0]});
  // E5: the cup set down at her right 200-206, back up 212; rises 214-244
  k.k(200, {aR: [40, 30, .8], tor: [-8, 8, 2]}).k(205, {plR: [-.5, .84, .06], plwR: 1, tor: [-10, 14, 6], head: [-10, 16, 0]}, 'i')
    .k(206, {cup: 'none', hR: 'open'}).k(212, {plwR: 0, aR: [24, 12, .7], tor: [-10, 4, 0], head: [-8, 2, 0]})
    .k(216, {tor: [-24, 0, 0], head: [-2, 0, 0], aL: [40, 6, .62], aR: [40, 6, .62]})
    .k(226, {pos: [0, -.26, .04], tor: [-22, 0, 0], fL: [.13, .1, -.18], fR: [-.13, .1, -.14], skG: .3}, 'io')
    .k(240, {pos: [0, -.08, 0], tor: [-8, 0, 0], head: [-6, 0, 0], fL: [.13, .1, -.12], fR: [-.14, .1, .1], kL: [.12, 0, -1],
      kR: [-.12, 0, -1], aL: [0, 8, .97], aR: [6, 10, .96], skG: 0}, 'io')
    .k(244, {pos: [0, -.04, 0], tor: [-4, 0, 0], head: [-4, 0, 0]});
  // the turn (248-268, the body turned by the sequence): the feet step
  k.k(248, {}).k(252, {fL: [.13, .24, -.1], pos: [0, -.02, 0]}).k(256, {fL: [.13, .1, -.1], pos: [0, -.05, 0]})
    .k(260, {fR: [-.14, .24, .08], pos: [0, -.02, 0]}).k(264, {fR: [-.14, .1, .1], pos: [0, -.04, 0]}).k(268, {});
  // the laughing head tilt 270-290 (her pun, line 5's tail)
  k.k(270, {face: 'smile', head: [2, -6, 10], tor: [2, 0, 2]}).k(280, {head: [4, -8, 12]}).k(290, {head: [-2, -4, 2], tor: [-4, 0, 0]});
  // E6: the right hand to the hip scabbard's throat 292, takes it 300 (scabbard hand), brings it round to the carry 310
  k.k(296, {face: 'calm', hR: 'grip', hsR: 1, tor: [-6, 8, 0], head: [-6, -6, 0]}).k(300, {scab: 'hand', ...HIP_DIR, hsR: 1})
    .k(310, {...CARRY, tor: [-4, 0, 0], head: [-6, 0, 0]});
  // walks 312-396 carrying it (16-t cycle, 0.15 b/t)
  k.k(312, {...F_ST, pos: [0, -.04, 0]}).all(walk(312, 396, {lean: -5})).k(398, {...F_ST, pos: [0, -.04, 0], rot: [0, 0, 0], tor: [-4, 0, 0], aL: [2, 8, .97]});
  // E8: the open left hand from the moon (behind her left) across the field 402-432
  k.k(402, {aL: [205, -42, .95], tor: [-2, -40, 0], head: [10, -56, 0], hL: 'open'}).k(414, {aL: [120, 30, .95], tor: [-2, -22, 0], head: [2, -30, 0]})
    .k(432, {aL: [50, 86, .95], tor: [-4, 6, 0], head: [-2, 10, 0]}).k(442, {aL: [4, 10, .97], tor: [-4, 0, 0], head: [-8, 0, 0]});
  // E9: walks on 444-490 looking from under the brim
  k.k(444, {...F_ST, pos: [0, -.04, 0], head: [-10, 0, 0]}).all(walk(444, 492, {lean: -6}))
    .k(494, {...F_ST, pos: [0, -.04, 0], rot: [0, 0, 0], tor: [-4, 0, 0], aL: [2, 8, .97], head: [-10, 0, 0]});
  // E10: stops; the scabbard raised upright before her right shoulder 504-510, holds
  k.k(502, {}).k(510, {...UPRIGHT, tor: [-4, -6, 0], head: [-6, -4, 0]}).k(530, {tor: [-3, -6, 1]}).k(554, {tor: [-4, -6, 0]});
  C('intro', 554, k, {src: 'staged (v1s_intro_stairs: the far figure; PLAN §3.1 E0-E10); E10 v1 4.8-5.8 (v1s_intro_keys: the scabbard upright, hilt up)'});
}
const INTRO_END0 = {...ST, pos: [0, -.04, 0], tor: [-4, -6, 0], head: [-6, -4, 0], ...F_ST, ...SHEATHED, ...UPRIGHT, aL: [2, 8, .97],
  face: 'calm', hat: 'worn', cup: 'none', bottle: 'none', skG: 0, plwL: 0, plwR: 0, hiL: 0};

// =================================================================================================================================
// intro_end (86 t = CS0 554-640, the skip's target; v1 2.2-8.05: v1s_intro_keys, mg_v1_hands_zoom, cr_v1_stance_hand)
// Line 11 from 0, the smile 2-34 (the face reveal), the head lowered 36, turns away 44-50 and spins on 50-56 (one turn to her
// left, keyed every tick), the cross-draw at 56 (the left hand from the hilt of the scabbard in her right), the stance 60 facing
// the player (arms spread, the scabbard low in the right hand tip down-and-out, the sword arm out to her left), the right hand
// drops and the left (sword) hand rises to the brim 62-70, the scabbard to the right hip 70-76 (tuck), into the guard 76-86.
{
  const k = Keys().k(0, FULL(INTRO_END0)).k(2, {face: 'smile', head: [-4, -2, 2]}).k(20, {head: [-2, 0, 3]}).k(34, {head: [-4, -2, 1]})
    .k(36, {face: 'calm', head: [-24, 0, 0], tor: [-8, -4, 0]}).k(42, {head: [-26, 0, 0]});
  // turns away 44-50, spins on 50-56 (rot yaw 0 -> -360, to her left), the left hand to the hilt 52-55
  k.all(every(44, 56, u => ({rot: [0, -360 * u, 0], tor: [-8, -10 * Math.sin(u * Math.PI), 0], head: [lerp(-26, -8, u), 0, 0],
    hairS: .5 * Math.sin(u * Math.PI), skW: -.5 * Math.sin(u * Math.PI)})));
  k.k(52, {hiL: .5, hL: 'grip'}).k(55, {hiL: 1, scE: -60, aR: [70, -14, .6]});
  // the draw 56-59: the sword pulled up out of the (hilt-up) scabbard, tip down (sh / shW blended off over 2 t), then swept out to
  // her left
  k.k(56, {sword: 'hand', hold: 1, hiL: 0, shW: 1, sh: 1, gF: 0, gB: -20, gE: 20, gD: .58, cB: -20, cR: 0, th: -80, ed: -1, tw: 0, rh: 0})
    .k(57, {shW: .65, sh: .6, gB: -22, gE: 22, gD: .6, cB: -26, th: -74}, 'l')
    .k(58, {shW: .3, sh: .25, gB: -32, gE: 16, gD: .64, cB: -38, th: -62}, 'l')
    .k(59, {shW: 0, sh: 0, gB: -46, gE: 6, gD: .68, cB: -54, th: -48}, 'l')
    .k(60, {gB: -62, gE: -6, gD: .72, cB: -72, th: -36}, 'l');
  // the stance 60: facing the player, arms spread, the scabbard low in the right hand (tip down-and-out), the sword out left
  const STANCE = {pos: [0, -.1, 0], rot: [0, -360, 0], ...F_WIDE, tor: [-6, 0, 0], head: [-6, 0, 0], gB: -82, gE: -18, gD: .75, cB: -96,
    cR: 0, th: -26, ed: -1, aR: [30, 34, .95], scB: 58, scE: -36, scOff: .18, hairS: 0, skW: 0};
  k.k(62, STANCE, 'o');
  // the right hand drops, the left (sword) hand rises to the brim 62-70 (the grip at the brim's left front, the blade up and out)
  k.k(68, {aR: [16, 30, .96], scB: 52, scE: -28, gB: -36, gE: 46, gD: .58, cB: -60, cR: 0, th: 118, head: [-10, 4, 0]}, 'io')
    .k(70, {gE: 48});
  // the scabbard to the right hip 70-76 (tuck: the right hand to the hip, the scabbard turned to the hip's direction)
  k.k(75, {hsR: 1, ...HIP_DIR, aR: [10, 16, .9]}, 'io').k(76, {scab: 'hip', hsR: 1, hR: 'open'})
    .k(80, {hsR: 0, aR: [6, 10, .96], gB: -50, gE: -20, gD: .64, cB: 20, th: -30, head: [-6, -2, 0]}, 'io');
  k.k(86, {...ST, rot: [0, -360, 0], hiL: 0, hsR: 0, shW: 0, sh: 0});
  C('intro_end', 86, k, {src: 'v1 2.2-8.05 (v1s_intro_keys: smile, head down, turn away, spin; mg_v1_hands_zoom / cr_v1_stance_hand: the draw and the stance)'});
}

// =================================================================================================================================
// cs1 (213 t; PLAN §3.2; v1 37.28 → v2 6.92: v1s_cs_keys, v2f_cs_keys1/2, v2f_cs_hat, cr_v2_petalcut, cr_v2_a11)
// C0 the lunge 0-10 (the sequence glides her to 1.8 b before the player); C1 the blade lock 10-32 (both hands, the blade crossed
// vertically, pushing 24-30); C2 the push-off 32, the leap back 36-52 (the sequence leaps the body 6 b), the hat onto her back
// 40, the landing in a low ready stance 52; C3 the low stance held 54-100 (hat on her back, the blade low pointing to her left;
// glint 96); C4 under the black 100-110: the hat back on and the sword sheathed at 104, into the iai stance (the left hand on
// the hilt, the right on the throat); C5 the iai stance under the brim 110-161; C6-C7 the draw under the overlays 161-169 (keyed
// every tick); C8 홍련일섬 169: the twisted post-slash crouch, the hat swung onto her back 176, held to 213 (= sq1 0).
{
  const DASH = {pos: [0, -.18, 0], rot: [-24, 0, 0], tor: [-14, 4, 0], head: [10, -2, 0], fL: [.14, .16, -.5], fR: [-.14, .3, .4], lf: .3,
    ...B(0, 70, -150, 1, {gL: .6}), aR: [-40, 20, .95], hairS: -.8, skW: 1};
  const LOWR = {...ST, ...LOW, rot: [0, 0, 0], lf: 0, pos: [0, -.38, 0], fL: [.3, .1, -.36], fR: [-.28, .1, .34], tor: [-22, 14, 0], head: [6, -10, 0],
    hold: 1, sword: 'hand', hL: 'grip', hR: 'open', gF: 0, gB: -60, gE: -38, gD: .66, cB: -84, cR: 0, th: -24, ed: -1, rh: 0, aR: [30, 40, .9],
    hairS: 0, skW: 0, hat: 'back'};
  const k = Keys().k(0, {...ST, hat: 'worn', scab: 'hip', sword: 'hand'}).k(3, DASH, 'o').k(5, {rot: [-28, 0, 0], tor: [-16, 4, 0]});
  k.all(every(6, 9, u => ({rot: [+lerp(-28, -6, u).toFixed(1), 0, 0], lf: +lerp(.3, 0, u).toFixed(2), tor: [-15, +lerp(4, -4, u).toFixed(1), 0],
    ...B(0, +lerp(70, 10, u).toFixed(1), +lerp(-150, 70, sm(u)).toFixed(1), +lerp(1, -1, u).toFixed(2), {gL: .6}), gF: +lerp(1, .3, u).toFixed(2), gB: -8, gE: 4, gD: .52,
    rh: +lerp(0, .7, u).toFixed(2), aR: [+lerp(-40, 50, u).toFixed(1), 10, .9], hairS: +lerp(-.8, -.3, u).toFixed(2), skW: +lerp(1, .3, u).toFixed(2)})));
  k.k(10, {...LOCK, rot: [0, 0, 0], lf: 0, hairS: -.2, skW: .2}, 'io').k(16, {...LOCK, hairS: 0, skW: 0})
    .k(24, {pos: [0, -.18, -.06], tor: [-18, -8, 0], head: [-10, 8, 0]}).k(30, {pos: [0, -.2, -.08], tor: [-20, -6, 0]})
    .k(32, {pos: [0, -.1, .02], tor: [-4, -4, 0], head: [-4, 4, 0], rh: .4}, 'o');
  // the leap back 36-52 (airborne, legs tucked, the hat swings onto her back at 40) and the landing 52
  k.k(36, {...CROUCH, pos: [0, -.26, 0], tor: [-12, 0, 0], rh: 0}).k(40, {...AIR, hat: 'back', pos: [0, .06, .04], rot: [10, 0, 0], tor: [-2, 6, 0],
    fL: [.13, .55, -.25], fR: [-.13, .5, -.1], lf: .8, ...B(-40, 0, 40, -1, {gL: .58}), aR: [60, 50, .9], hairS: .5, skW: -.6}, 'o')
    .k(46, {rot: [6, 0, 0], fL: [.13, .45, -.3], fR: [-.13, .4, -.15]}).k(52, {...LOWR}, 'i').k(56, {pos: [0, -.4, 0]})
    .k(76, {pos: [0, -.37, 0], tor: [-21, 15, 0]}).k(94, {pos: [0, -.39, 0], tor: [-22, 14, 0], th: -22}).k(96, {th: -26});
  // C4 under the black: up into the iai stance, the hat back on and the sword sheathed at 104
  k.k(100, {}).k(102, {pos: [0, -.3, 0], tor: [-16, 0, 0], gB: 0, gE: -36, gD: .6, cB: 30, th: -40}, 'io')
    .k(103, {pos: [0, -.24, 0], tor: [-14, -10, 0], gB: 40, gE: -26, gD: .52, cB: 120, th: -50}, 'io')
    .k(104, {...IAI, hat: 'worn'}).k(110, {head: [-22, 18, 0]}).k(135, {head: [-20, 16, 0], tor: [-17, -22, 0]}).k(158, {head: [-22, 18, 0], tor: [-19, -22, 0]})
    .k(161, {pos: [0, -.3, 0], tor: [-20, -26, 0]});
  // the draw / the slash under the overlays 162-169 (every tick): the blade out of the hip scabbard, sweeping round to her left
  k.k(162, {sword: 'hand', hold: 1, hiL: 0, shW: 1, sh: 1, gF: 0, gB: 40, gE: -24, gD: .5, cB: 150, cR: 0, th: -10, ed: -1, rh: 0, hsR: 1}, 'l');
  k.all(every(163, 168, u => ({shW: +lerp(.7, 0, Math.min(1, u * 1.3)).toFixed(2), sh: +lerp(.5, 0, Math.min(1, u * 2)).toFixed(2),
    gB: +lerp(20, -100, u).toFixed(1), gE: -26, gD: +lerp(.55, .7, u).toFixed(2), cB: +lerp(110, -110, u).toFixed(1), th: -12,
    tor: [-22, +lerp(-24, -40, u).toFixed(1), 0], pos: [0, +lerp(-.32, -.4, u).toFixed(3), 0], hsR: +lerp(1, 0, u).toFixed(2)})));
  k.k(169, {...SLASHED, hat: 'worn', shW: 0, sh: 0}, 'o').k(174, {tor: [-24, -48, 0]}).k(176, {hat: 'back', head: [-2, 32, 0]})
    .k(190, {pos: [0, -.41, 0], tor: [-23, -46, 0]}).k(213, {pos: [0, -.42, 0], tor: [-24, -44, 0], head: [-4, 30, 0]});
  C('cs1', 213, k, {cuts: [104], src:'v1 37.28-39.2 (v1s_cs_keys: lunge, lock, apart, the hat on her back), v2 0-6.9 (v2f_cs_keys1/2, v2f_cs_hat, cr_v2_a11: the iai, 홍련일섬)'});
}
const SQ1_0 = {...SLASHED, hat: 'back'};

// =================================================================================================================================
// sq1 (60 t; PLAN §3.3; v2 6.93-9.70: v2f_a_boss_far_01, cr_pretell_hand): from the twisted crouch (hat on her back) she straightens
// 6-10, re-hats (the right hand lifts the hat off her back 10-20: hat hand 12, onto her head 22-30: worn 28), stands off 30-42
// (still, facing the player, the blade low), the right hand rises to the brim 46-52 and stays (g_brim's hold; A8's T0 at 60).
{
  const k = Keys().k(0, FULL(SQ1_0)).k(6, {}).k(10, {...ST2, hat: 'back', hR: 'open', aR: [150, -20, .8], pR: [.5, .3, -.3]}, 'io')
    .k(12, {hat: 'hand', hR: 'grip', hhB: 180, hhE: 40, hhN: [180, -10], aR: [160, -24, .82]})
    .k(20, {hhB: 120, hhE: 50, hhN: [90, 40], aR: [168, -10, .86], head: [-4, -4, 0]}, 'io')
    .k(26, {hhB: 20, hhE: 30, hhN: [0, 85], aR: [150, 10, .9]}, 'io')
    .k(28, {hat: 'worn', hR: 'brim', bwR: 1, bzR: 20, aR: [120, 30, .9]}).k(32, {...ST2, hR: 'open', bwR: 0, aR: [10, 14, .95]}, 'io')
    .k(42, {pos: [0, -.13, 0]}).k(46, {}).k(52, {...BRIM_R}, 'o').k(56, {...BRIM_R, head: [-9, -7, 0], pos: [0, -.13, 0]}).k(60, {...BRIM_R});
  C('sq1', 60, k, {src: 'v2 6.93-9.70 (v2f_a_boss_far_01: the re-hat; cr_pretell_hand: the hand to the brim from T0 - 14)'});
}

// =================================================================================================================================
// repel (104 t; PLAN §3.4 = CS2 / CS3; v2f_c1/c2/c_keys1/2/c_hat/c_throw, v3r_c_*): R0 the blade lock (LOCK) 0-8; R1 the hat swings
// onto her back 8, the sword arm jerked up and held (caught), on her toes, turned sideways 8-24; R2 she reels from the burst on
// the hat 24-28; R3 swung round the player (the sequence moves the body on a half circle): a back flip about her centre, the
// boots high 28-44; R4 back to back 44-58 (both turn); R5 thrown over the player's shoulder (the sequence leaps the body): the
// body diagonal, legs up 58-68, the hat off at 60 flying aside (world, keyed every tick), falling upside down onto her back 68-75;
// R6 flat on her back 75; R7 lying 78-102 (the hat beside her: DOWN); R8 the kick 102 (the head snaps aside) -> 104 like DOWN.
{
  const k = Keys().k(0, FULL(LOCK)).k(4, {pos: [0, -.16, -.05], tor: [-15, -6, 0]})
    .k(8, {hat: 'back', pos: [0, -.05, 0], tor: [-6, 30, 0], head: [-6, -26, 0], ...F_ST, rh: 0, gF: 0, gB: -20, gE: 64, gD: .62,
      cB: -10, cR: 0, th: 150, ed: -1, aR: [40, 50, .9]}, 'o')
    .k(14, {pos: [0, .02, 0], fL: [.13, .16, -.1], fR: [-.14, .16, .1], tor: [-2, 44, 0], head: [-8, -36, 0], gE: 70})
    .k(22, {pos: [0, .04, 0], tor: [0, 48, 0], gE: 72}).k(24, {tor: [-16, 40, 0], head: [-20, -30, 0], pos: [0, -.02, -.04]}, 'i')
    .k(28, {tor: [-6, 30, 0], head: [-8, -20, 0], pos: [0, 0, 0]}, 'o');
  // R3: a back flip about her centre 28-44 (every tick), the boots high, the arms flung
  k.all(every(29, 43, u => {
    const pt = 360 * sm(u);
    return {rot: [+pt.toFixed(1), 0, 0], pos: flipPos(pt, .5, .25 * Math.sin(Math.PI * u)), lf: +(.9 * Math.sin(Math.PI * u)).toFixed(2),
      fL: [.13, .5, -.2], fR: [-.13, .46, -.05], tor: [-10, 20, 0], gE: 40, th: 120, aR: [120, 70, .9], hairF: +(.5 * Math.sin(Math.PI * u)).toFixed(2)};
  }));
  k.k(44, {rot: [360, 0, 0], pos: [0, -.06, 0], lf: 0, ...F_ST, tor: [-4, 10, 0], head: [-4, -10, 0], gE: 20, th: 100, aR: [20, 30, .9], hairF: 0}, 'o')
    .k(50, {tor: [-2, 30, 0], head: [-6, -20, 0]}).k(58, {tor: [-6, 40, 0], head: [-10, -26, 0], pos: [0, -.1, 0]}, 'io');
  // R5 thrown: diagonal, legs up, then upside down onto her back (pitch 360 -> 360 + 128 -> 360 + 88); the hat off at 60
  const HAT_PATH = [[0, 1.85, .32], [-.15, 2.25, .3], [-.32, 2.55, .2], [-.48, 2.75, .08], [-.62, 2.85, -.05], [-.74, 2.85, -.16], [-.84, 2.75, -.26],
    [-.92, 2.55, -.34], [-.98, 2.25, -.4], [-1.02, 1.85, -.45], [-1.04, 1.38, -.48], [-1.05, .9, -.49], [-1.05, .48, -.5], [-1.05, .2, -.5], [-1.05, .05, -.5],
    [-1.05, .02, -.5]];
  k.all(every(59, 75, u => {
    const pt = u < .55 ? lerp(0, 128, sm(u / .55)) : lerp(128, 88, sm((u - .55) / .45)), v = Math.min(1, u * 2.2);
    return {rot: [+(360 + pt).toFixed(1), 0, 0], pos: [0, +(lerp(-.1, -1.04, sm(u)) + .26 * Math.sin(Math.PI * Math.min(1, u * 1.08))).toFixed(3), +lerp(0, .08, u).toFixed(3)],
      lf: +Math.min(1, u * 2).toFixed(2), fL: [.15, .1, -.06], fR: [-.15, .1, -.02], tor: [+lerp(-6, 2, u).toFixed(1), +lerp(40, 0, u).toFixed(1), 0],
      head: [-12, +lerp(-26, 24, u).toFixed(1), 0], gB: +lerp(-20, -90, v).toFixed(1), gE: +lerp(20, -58, u).toFixed(1), gD: .62, cB: +lerp(-10, 0, v).toFixed(1),
      cR: +lerp(0, 90, v).toFixed(1), th: +lerp(100, 6, v).toFixed(1), ed: -1, aR: [+lerp(60, 6, u).toFixed(1), 24, 1], hairF: +Math.max(0, (u - .75) * 4).toFixed(2),
      skG: +(u * .5).toFixed(2), skIB: +(u * .08).toFixed(3), scHip: [+lerp(0, -70, Math.min(1, u * 2)).toFixed(1), 0]};
  }));
  k.k(60, {hat: 'world', hwP: HAT_PATH[0], hwE: [90, 0, 0]});
  HAT_PATH.forEach((p, i) => { const w = Math.min(1, i / 11);
    k.k(60 + i, {hwP: p, hwE: [+lerp(90, 0, w).toFixed(1), +lerp(0, 30, i / 15).toFixed(1), +(25 * Math.sin(w * Math.PI)).toFixed(1)]}, 'l'); });
  k.k(76, {...FULL(DOWN), rot: [448, 0, 0], pos: [0, -1.0, .02]}, 'o').k(78, {...FULL(DOWN), rot: [448, 0, 0]})
    .k(90, {tor: [3, 0, 0], head: [-12, 22, 0]}).k(101, {tor: [2, 0, 0], head: [-12, 24, 0]})
    .k(102, {head: [-20, 50, 0], tor: [6, 6, 0], pos: [0, -1.0, .02]}, 'o').k(104, {head: [-14, 34, 0], tor: [3, 2, 0], pos: [0, -1.04, 0]});
  C('repel', 104, k, {cuts: [60], src:'v2 19.72-24.95 / v3 21.10-26.25 (v2f_c1, v2f_c2, v2f_c_keys1/2, v2f_c_hat, v2f_c_throw, v3r_c_flip): lock, grab, clash on the hat, flip, back to back, throw, lying, the kick'});
}

// =================================================================================================================================
// lead_down (82 t; PLAN §3.5; v3 4.10-8.18: v3r_a_kipup, v3r_a_5to8, cr_pretell_v3): from DOWN the legs swing up 0-4, the kip 4-7
// (upright 7), the right hand takes the hat from the ground 7-10 while the left raises the sword vertical above her 10, the hat at
// head height in the right hand 12, side steps to her right 12-48 holding it at shoulder height (the sequence glides the body
// 2 b), the hat lifted over her head 42 and put on 48, the low-blade guard 48-65, the right hand to the brim 65 (T0 - 17), held.
{
  const k = Keys().k(0, FULL(DOWN)).k(3, {...DOWN, lf: 1, fL: [.13, .9, -.4], fR: [-.13, .86, -.3], tor: [-20, 0, 0], head: [-20, 10, 0], pos: [0, -1.12, 0]}, 'o')
    .k(5, {rot: [40, 0, 0], pos: [0, -.8, 0], lf: .6, tor: [-30, 0, 0], fL: [.13, .5, -.5], fR: [-.13, .46, -.4], hairF: .6, skG: .3, gE: -40, th: 0}, 'i')
    .k(7, {...ST2, rot: [0, 0, 0], lf: 0, pos: [0, -.44, 0], tor: [-28, -10, 0], head: [6, 10, 0], hat: 'world', hwP: [-1.05, .02, -.5], hwE: [0, 30, 0],
      hR: 'grip', plR: [-.95, .12, -.5], plwR: 1, hairF: .2, skG: 0, skIB: 0, scHip: [0, 0], gF: 0, gB: -60, gE: -20, gD: .62, cB: -30, cR: 40, th: -10, ed: -1}, 'o')
    .k(9, {hat: 'hand', hhB: 90, hhE: 0, hhN: [0, 90], plR: [-.6, .5, -.5], plwR: 1, pos: [0, -.3, 0], gB: -30, gE: 36, gD: .62, cB: -10, cR: 10, th: 64}, 'io')
    .k(10, {plwR: .4, aR: [100, 46, .9], hhB: 70, hhE: 6, hhN: [60, 50], gB: -10, gE: 70, gD: .62, cB: 0, cR: 0, th: 92, tor: [-10, -6, 0], pos: [0, -.18, 0]}, 'io')
    .k(11, {plwR: 0}, 'io')
    .k(12, {hat: 'hand', hR: 'grip', aR: [96, 52, .9], hhB: 70, hhE: 12, hhN: [90, 20], pos: [0, -.1, 0], tor: [-6, -6, 0], head: [-6, 4, 0], gE: 64, th: 86})
    .k(18, {gF: 0, gB: -40, gE: -42, gD: .7, cB: 52, cR: 0, th: -30, ed: -1, tor: [-9, 4, 0]}, 'io');
  k.all(side(12, 48, {P: 12, w: .3, dir: -1})).k(42, {aR: [170, 10, .9], hhB: 0, hhE: 30, hhN: [0, 70], head: [-2, 0, 0]})
    .k(47, {hhB: 0, hhE: 15, hhN: [0, 88], aR: [150, 20, .9]}).k(48, {hat: 'worn', hR: 'brim', bwR: 1, bzR: 24, aR: [120, 30, .9]})
    .k(54, {...ST2, hR: 'open', bwR: 0, aR: [10, 14, .95]}, 'io').k(65, {pos: [0, -.13, 0]}).k(71, {...BRIM_R}, 'o').k(76, {...BRIM_R, head: [-9, -7, 0], pos: [0, -.13, 0]})
    .k(82, {...BRIM_R});
  C('lead_down', 82, k, {src: 'v3 4.10-8.18 (v3r_a_kipup, cr_v3_kipup: the kip-up, the sword vertical; v3r_a_5to8: the hat at shoulder height, side steps; cr_pretell_v3: the hand to the brim)'});
}

// =================================================================================================================================
// lead_stand (70 t; PLAN §3.5: the 5 % floor reached standing, or a gauntlet restart): a staggering step back 0-8, the hat off into
// her right hand 8, side steps to her right 10-30 (the sequence glides the body 2 b), the hat over her head 30, on 36, the guard,
// the right hand to the brim 53 (T0 - 17), held to 70.
{
  const k = Keys().k(0, {...ST2, hat: 'worn'}).k(3, {pos: [0, -.06, .1], tor: [6, 8, 0], head: [8, -8, 0], fR: [-.14, .1, .32], fL: [.14, .2, -.02]}, 'o')
    .k(6, {pos: [0, -.14, .12], tor: [-6, 6, 0], fL: [.15, .1, .16], fR: [-.15, .1, .34], aR: [120, 30, .9], hR: 'open'}, 'io')
    .k(8, {hat: 'hand', hR: 'grip', hhB: 20, hhE: 40, hhN: [0, 70], aR: [150, 20, .9], head: [-2, -4, 0]})
    .k(10, {...ST2, hat: 'hand', hR: 'grip', aR: [96, 52, .9], hhB: 70, hhE: 12, hhN: [90, 20], pos: [0, -.1, 0]}, 'io');
  k.all(side(10, 30, {P: 12, w: .4, dir: -1})).k(30, {aR: [170, 10, .9], hhB: 0, hhE: 30, hhN: [0, 70], head: [-2, 0, 0]})
    .k(35, {hhB: 0, hhE: 15, hhN: [0, 88], aR: [150, 20, .9]}).k(36, {hat: 'worn', hR: 'brim', bwR: 1, bzR: 24, aR: [120, 30, .9]})
    .k(42, {...ST2, hR: 'open', bwR: 0, aR: [10, 14, .95]}, 'io').k(53, {pos: [0, -.13, 0]}).k(59, {...BRIM_R}, 'o').k(64, {...BRIM_R, head: [-9, -7, 0], pos: [0, -.13, 0]})
    .k(70, {...BRIM_R});
  C('lead_stand', 70, k, {src: 'PLAN §3.5 (the lead_down beats from standing; v3r_a_5to8, cr_pretell_v3)'});
}

// =================================================================================================================================
// ending (1042 t = H; PLAN §3.7 std profile; v3 26.27 → v5 21.65: v3r_e_shots1-4, v3r_e_slash_2f, v4k_c*, v4k_s4_sheathe, v4k_s5_face,
// v5e_s1_*, v5e_s2_*, v5e_s3_keys1-3). The sequence moves / turns the body (the duel distances, the dash past, the aerial hang, the
// landing, the walk-in to 4.5 b, the turn toward the moon 506-526 and back 794-815); every strike stops at the player (no hit).
{
  const LY = {...FULL(DOWN), pos: [0, -1.01, 0], hat: 'world', hwP: [0, .52, .96], hwE: [6, 0, 0], head: [-6, 10, 0]};
  const k = Keys().k(0, LY).k(1, {}).k(14, {tor: [3, 0, 0]});
  // E1b the ground slash 16-28: the sword arm sweeps the blade flat from her left across (every tick 19-26)
  k.k(18, {gB: -110, gE: -40, gD: .6, cB: -100, cR: 90, th: 20, tor: [4, -6, 0]}, 'io');
  k.all(every(19, 26, u => ({gB: +lerp(-110, 30, u).toFixed(1), gE: +lerp(-40, -10, u).toFixed(1), cB: +lerp(-100, 60, u).toFixed(1), cR: 90, th: +lerp(20, -20, u).toFixed(1),
    tor: [4, +lerp(-6, 8, u).toFixed(1), 0]})));
  // E2 the kip-up 28-38 (the hat knocked up off her face, caught 40, on 44), standing 3 b off with arms spread, the sword raised 48
  k.k(28, {gB: 0, gE: -20, cB: 0, cR: 90, th: 0, lf: 1, tor: [-6, 0, 0], hwP: [0, .7, .9], hwE: [10, 0, 0]}, 'io')
    .k(31, {lf: 1, fL: [.13, .9, -.4], fR: [-.13, .86, -.3], tor: [-20, 0, 0], head: [-20, 10, 0], pos: [0, -1.12, 0], hwP: [0, 1.5, .6], hwE: [30, 0, 15]}, 'o')
    .k(34, {rot: [40, 0, 0], pos: [0, -.8, 0], lf: .6, tor: [-30, 0, 0], fL: [.13, .5, -.5], fR: [-.13, .46, -.4], hairF: .6, skG: .3, hwP: [-.1, 2.3, 0], hwE: [60, 0, 20]}, 'i')
    .k(37, {...ST, rot: [0, 0, 0], lf: 0, pos: [0, -.3, 0], ...F_WIDE, tor: [-16, 0, 0], head: [10, 0, 0], hold: 1, sword: 'hand', hL: 'grip', hR: 'open',
      ...B(-60, 0, -20, -1, {gL: .58}), aR: [110, 30, .9], hairF: 0, skG: 0, skIB: 0, hat: 'world', hwP: [-.15, 2.8, -.6], hwE: [50, 0, 10]}, 'o')
    .k(39, {pos: [0, -.12, 0], aR: [160, 10, .92], hwP: [-.17, 2.94, -1.0], hwE: [40, 0, 0]})
    .k(40, {hat: 'hand', hR: 'grip', hhB: 0, hhE: 40, hhN: [180, 80], aR: [168, 6, .92]})
    .k(43, {hhB: 0, hhE: 15, hhN: [0, 88], aR: [150, 20, .9]}).k(44, {hat: 'worn', hR: 'brim', bwR: 1, bzR: 24, aR: [120, 30, .9]})
    .k(45, {gF: 0, gB: -60, gE: 0, gD: .66, cB: -50, cR: 0, th: 40, ed: -1}, 'io')
    .k(48, {...ST, pos: [0, -.06, 0], ...F_WIDE, tor: [-4, 0, 0], head: [-4, 0, 0], hR: 'open', bwR: 0, aR: [40, 70, .95], gF: 0, gB: -60, gE: 40, gD: .7,
      cB: -40, cR: 0, th: 130, ed: -1, rh: 0}, 'o')
    .k(55, {gE: 44, th: 136}).k(57, {gB: -10, gE: 30, gD: .62, cB: 0, th: 70}, 'i').k(58, {gB: 0, gE: 4, gD: .66, cB: 0, th: 8, tor: [-10, 0, 0], ...F_LUNGE}, 'l');
  // E3-E5 the blade lock 62-80 (1.2 b off); E6 slides back into a side-on stance 80-92
  k.k(62, {...LOCK}, 'o').k(70, {pos: [0, -.18, -.06], tor: [-17, -8, 0]}).k(78, {pos: [0, -.14, -.04], tor: [-14, -6, 0]})
    .k(84, {...ST, pos: [0, -.2, .06], rot: [0, 50, 0], tor: [-8, -30, 0], head: [-4, -40, 0], ...F_WIDE, ...B(-40, 0, 20, -1, {gL: .6}), aR: [30, 50, .9],
      hR: 'open', rh: 0, skW: -.4}, 'o')
    .k(92, {pos: [0, -.24, 0], rot: [0, 54, 0], tor: [-10, -34, 0], skW: 0});
  // E7 the lunge 92-96 (the big clash 96), three strikes 108 / 116 / 124 stopping at the player (every tick through each cut)
  k.k(94, {rot: [0, 20, 0], tor: [-14, -10, 0], ...F_LUNGE, ...B(0, 0, 120, -1, {gL: .5}), rh: .6}, 'i')
    .k(96, {rot: [0, 0, 0], tor: [-18, 0, 0], head: [-6, 0, 0], pos: [0, -.22, -.06], ...B(0, 0, 10, -1, {gL: .62}), rh: .8}, 'l')
    .k(100, {pos: [0, -.16, -.04], tor: [-14, 0, 0], ...B(0, 0, 40, -1, {gL: .58})}).k(103, {rh: .3, ...B(0, -20, 90, -1, {gL: .54}), tor: [-8, 12, 0]}, 'io')
    .k(106, {pos: [0, -.12, 0], ...B(0, -45, 140, -1, {gL: .5}), rh: 0, tor: [-4, 24, 0]}, 'io');
  const cut = (t, from, to, cR, x = {}) => k.all(every(t - 3, t, u => ({...B(0, cR, +lerp(from, to, u).toFixed(1), -1, {gL: +lerp(.5, .64, u).toFixed(2)}),
    tor: [+lerp(-4, -16, u).toFixed(1), +lerp(cR < 0 ? 24 : -24, cR < 0 ? -10 : 10, u).toFixed(1), 0], ...x})));
  cut(108, 140, -10, -45); k.k(112, {...B(0, 45, 130, -1, {gL: .5}), tor: [-4, -24, 0]});
  cut(116, 130, -20, 45); k.k(120, {...B(0, 0, 140, -1, {gL: .48}), rh: .7, tor: [6, 0, 0]});
  cut(124, 140, 0, 0, {rh: .8}); k.k(126, {});
  // E8 the pass: crouched low, the sword back 130-140; the dash past 140-146 (the passing strike 143, every tick 140-146); the turn
  // (the sequence turns the body 150-160), the hold 160-170
  k.k(130, {...LOW, ...ST2, pos: [0, -.4, 0], tor: [-24, 10, 0], head: [8, -8, 0], ...F_WIDE, ...SW(150, 10, -1, 125, -30, .6), rh: 0, aR: [40, 40, .9]}, 'io')
    .k(139, {pos: [0, -.42, 0], tor: [-26, 12, 0]});
  k.all(every(140, 146, u => ({rot: [-18 * Math.sin(Math.PI * u), 0, 0], ...SW(+lerp(150, -120, u).toFixed(1), 8, -1, +lerp(125, -110, u).toFixed(1), -28, .64),
    tor: [-14, +lerp(30, -30, u).toFixed(1), 0], pos: [0, -.26, -.04], fL: [.16, .16, -.5], fR: [-.14, .3, .4], hairS: -.7, skW: .9})));
  k.k(150, {...ST2, pos: [0, -.2, 0], rot: [0, 0, 0], ...SW(-110, 20, -1, -100, -30, .6), tor: [-10, -24, 0], hairS: 0, skW: 0}, 'o')
    .k(160, {...ST2}).k(170, {pos: [0, -.14, 0]});
  // E9 the dash back 170-174 (strike 174), blades crossed 176-186, the second flash 188
  k.k(166, {...B(0, 20, 50, -1, {gL: .56}), rh: .2, tor: [-8, 6, 0]}, 'io').k(170, {...B(0, 0, 110, -1, {gL: .5}), rh: .5, tor: [-6, 0, 0]}, 'io')
    .k(171, {rot: [-20, 0, 0], ...B(0, 0, 130, -1, {gL: .5}), rh: .6, tor: [-6, 0, 0], hairS: -.6, skW: .8}, 'io');
  k.all(every(172, 174, u => ({rot: [+lerp(-20, 0, u).toFixed(1), 0, 0], ...B(0, 0, +lerp(110, 12, u).toFixed(1), -1, {gL: +lerp(.52, .6, u).toFixed(2)}), rh: .8, tor: [+lerp(-8, -16, u).toFixed(1), 0, 0]})));
  k.k(176, {...LOCK, hairS: 0, skW: 0}, 'io').k(186, {pos: [0, -.16, -.06], tor: [-16, -8, 0]}).k(188, {pos: [0, -.08, .02], tor: [-6, -4, 0]}, 'o');
  // E10-S3 the aerial exchange: the leap up and back 190-198 (the sequence lifts the body), the hang 198-238 with the sword out to
  // her left; strikes 204 / 216 (overhead, the biggest) / 228 (every tick into each); the blade lock in the air 232-238
  const HANG = {...ST, ...AIR, pos: [0, .1, 0], rot: [0, 0, 0], lf: .85, tor: [-6, 8, 0], head: [-6, -4, 0], fL: [.13, .5, -.25], fR: [-.13, .44, -.05],
    gF: 0, gB: -80, gE: 0, gD: .74, cB: -90, cR: 0, th: 0, ed: -1, rh: 0, aR: [70, 60, .9], hairS: .3, skW: -.4};
  k.k(190, {...CROUCH, pos: [0, -.3, 0], tor: [-16, 0, 0], hairS: 0, skW: 0}).k(194, {...HANG, rot: [12, 0, 0]}, 'o').k(197, {...HANG}, 'o');
  const airCut = (t, big) => {
    const up = big ? 168 : 150;
    k.k(t - 5, {gF: 0, gB: -10, gE: 62, gD: .56, cB: 0, cR: 0, th: up, rh: 0, tor: [6, 0, 0]}, 'io');
    k.all(every(t - 2, t, u => ({gF: 0, gB: +lerp(-10, 0, u).toFixed(1), gE: +lerp(62, -6, u).toFixed(1), gD: +lerp(.56, .7, u).toFixed(2), cB: 0, cR: 0,
      th: +lerp(up, 4, u).toFixed(1), tor: [+lerp(6, -14, u).toFixed(1), 0, 0]})));
    k.k(t + 4, {...HANG}, 'io'); };
  airCut(204, false); airCut(216, true); airCut(228, false);
  k.k(232, {...HANG, ...LOCK, ...AIR, lf: .85, pos: [0, .1, 0], fL: [.13, .5, -.25], fR: [-.13, .44, -.05], hairS: .2}, 'o').k(238, {pos: [0, .12, -.03]});
  // S4 flies back in a long arc (the sequence) 238-258 and lands crouched 258; holds the crouch to 268 (petal streaks)
  k.k(244, {...HANG, rot: [18, 0, 0], tor: [4, 0, 0], aR: [90, 70, .9], gE: 10, th: -10, hairS: .6, skW: -.7}, 'o')
    .k(254, {rot: [6, 0, 0], fL: [.13, .3, -.2], fR: [-.13, .26, .05], lf: .4}, 'io')
    .k(258, {...LOW, ...ST2, rot: [0, 0, 0], lf: 0, pos: [0, -.44, 0], ...F_WIDE, tor: [-26, 6, 0], head: [10, -6, 0], gF: 0, gB: -100, gE: -40, gD: .66,
      cB: -110, cR: 0, th: -30, ed: -1, rh: 0, aR: [20, 50, .9], hairS: 0, skW: 0}, 'i').k(268, {pos: [0, -.42, 0]});
  // S5 rises and turns 268-272, walks in 272-296 (0.23 b/t; the blade low in her left hand); the scabbard from the hip into the
  // right hand 280-284, brought forward low past her right side and up to upright 284-296; 297-304 (every tick) the scabbard swings
  // down to her right (the mouth at her right hip, its body out to her right 25 deg down) while the left hand lifts the sword up and
  // out to her left, the blade hanging down across her front to the mouth (v4k_s4_sheathe f645-f684); the blade onto the scabbard's
  // axis 304-306 (the tip already in the mouth: the sword is longer than her arms can span), slid in 306-318, seated 320 (the click)
  const L1 = (a, b, u) => +lerp(a, b, u).toFixed(1), L2 = (a, b, u) => +lerp(a, b, u).toFixed(2);
  const SH0 = {gF: 0, gB: -58.4, gE: 21.3, gD: 1.01, cB: 90, cR: 0, th: -25, ed: -1, tw: -60};   // the free blade = the on-axis pose at sh .22
  k.k(272, {...ST, pos: [0, -.04, 0], tor: [-4, 0, 0], head: [-4, 0, 0]}, 'io').all(walk(272, 284, {P: 12, s: .7, armL: false, lean: -6}))
    .k(280, {hR: 'grip', hsR: 1}).k(284, {scab: 'hand', ...HIP_DIR, hsR: 1}).all(walk(284, 296, {P: 12, s: .7, armL: false, lean: -6}))
    .k(288, {hsR: 0, scB: 95, scE: -32, scR: -80, scOff: .2, aR: [28, 34, .8], pR: [.6, -.4, .4]})
    .k(292, {scB: 40, scE: 24, scR: -20, scOff: .28, aR: [62, 18, .72]})
    .k(296, {...F_ST, pos: [0, -.04, 0], rot: [0, 0, 0], tor: [-4, 0, 0], aR: [84, 10, .66], scB: 20, scE: 76, scR: 0, scOff: .3, sh: .22});
  k.all(every(297, 304, u => { const s = sm(u);
    return {scB: L1(20, 90, s), scE: L1(76, -25, s), aR: [L1(84, 40, u), L1(10, 50, u), L2(.66, .95, u)], scOff: L2(.3, .12, u), gF: 0, gB: L1(-32, SH0.gB, s),
      gE: L1(-50, SH0.gE, s), gD: L2(.6, SH0.gD, s), cB: L1(38, SH0.cB, s), cR: 0, th: L1(-40, SH0.th, s), ed: -1, tw: L1(0, SH0.tw, s),
      pL: [L2(.55, .9, u), L2(-.35, .3, u), L2(.75, .2, u)], tor: [-4, 0, 0]}; }));
  // the left hand stays on the seated hilt at the click (320) and lets go at 321 (the free target = the hilt, 0.07 b)
  k.k(306, {shW: 1, sh: .22}, 'io').k(318, {sh: .97}, 'io').k(320, {sword: 'sheathed', sh: 1}).k(321, {hold: 0, hL: 'open', aL: [34, -70, 1]}, 'l')
    .k(326, {aR: [20, 14, .92], scB: 8, scE: -22, scOff: .2, aL: [4, 10, .97], pL: [.55, -.35, .75], shW: 0, sh: 0, tor: [-3, 0, 0], head: [-6, 0, 0]}, 'io')
    .k(330, {...F_TOG, pos: [0, -.02, 0]});
  // S6 the smile 330-440 (head slightly tilted)
  k.k(332, {face: 'smile', head: [-4, -4, 6]}).k(380, {head: [-3, -6, 7]}).k(436, {head: [-4, -4, 6]}).k(442, {face: 'calm', head: [-6, 0, 2]});
  // S8 the head lowered, the brim over her eyes 494-506; the turn toward the moon 506-526 (the sequence turns the body; the feet
  // step); her face over her left shoulder 600-612, one open hand chest-high 612-628, the smile 628-650
  k.k(494, {}).k(506, {head: [-22, 0, 0], tor: [-6, 0, 0]}).k(510, {fL: [.13, .24, -.1]}).k(514, {fL: [.13, .1, -.06]}).k(518, {fR: [-.13, .24, .08]})
    .k(522, {fR: [-.13, .1, .04]}).k(526, {...F_TOG, head: [-10, 0, 0]}).k(560, {head: [-6, 0, 0]}).k(600, {})
    .k(612, {head: [-4, -70, 0], tor: [-3, -20, 0]}).k(628, {hL: 'open', aL: [70, -10, .62], frL: 60, pL: [.6, -.4, .5]})
    .k(630, {face: 'smile'}).k(650, {}).k(660, {face: 'calm', head: [-4, 0, 0], tor: [-2, 0, 0], aL: [4, 10, .97], frL: 0}, 'io');
  // S10-C1 the moon gaze: head up 690-770, the hat dips to her right 786-794
  k.k(690, {head: [15, 0, 0]}).k(770, {head: [16, 2, 0]}).k(786, {head: [8, 4, 2]}).k(794, {head: [-2, 10, 9], tor: [-3, 6, 2]});
  // C2 the pivot (794-815, the sequence turns the body): the feet step, the sheathed sword sweeps flat behind her legs 801-810
  k.k(798, {fL: [.13, .24, -.08]}).k(801, {fL: [.13, .1, -.04], scB: 40, scE: -14, aR: [10, 20, .94]});
  k.all(every(802, 810, u => ({scB: +lerp(40, 178, u).toFixed(1), scE: -12, aR: [+lerp(10, -20, u).toFixed(1), +lerp(20, 24, u).toFixed(1), .94]})));
  k.k(812, {fR: [-.13, .24, .06]}).k(815, {fR: [-.13, .1, .04], head: [-4, 0, 0], tor: [-2, 0, 0]}).k(822, {scB: 8, scE: -22, aR: [14, 14, .94]}, 'io');
  // the open-palm "let me see" gesture 860-900, the closed-lip smile 920-934
  k.k(856, {}).k(866, {hL: 'open', aL: [70, 6, .7], frL: 90, pL: [.6, -.4, .5], head: [-2, -4, 3]}, 'io').k(894, {aL: [74, 4, .72]})
    .k(904, {aL: [6, 10, .97], frL: 0, head: [-4, 0, 0]}, 'io').k(920, {face: 'smile'}).k(934, {});
  // C3 the hat-tip: eyes closed 936, the left hand open-palm to the brim 936-944, speaks; grips and pulls the hat down with a 10-degree
  // bow 980-992, eyes hidden 992-1020, the face rises under the held brim, eyes open 1030, holds = H_POSE 1030-1042
  k.k(936, {face: 'closed'}).k(944, {hL: 'brim', bwL: 1, bzL: 40, aL: [120, 30, .9], pL: [.7, -.2, .2], frL: 0, head: [-4, 0, 0]}, 'o')
    .k(980, {}).k(992, {tor: [-10, 0, 0], head: [-16, 0, 0], bzL: 24, pos: [0, -.04, 0]}, 'io').k(1020, {tor: [-10, 0, 0], head: [-15, 0, 0]})
    .k(1030, {face: 'calm', tor: [-2, 0, 0], head: [-6, 0, 0], bzL: 40, pos: [0, -.02, 0]}, 'io').k(1042, FULL(H_POSE));
  C('ending', 1042, k, {cuts: [1], src: 'v3 26.27-40.3 (v3r_e_shots1-4, v3r_e_slash_2f), v4 (v4k_c*, v4k_s4_sheathe, v4k_s5_face), v5 (v5e_s1_*, v5e_s2_turn*, v5e_s3_keys1-3)'});
}

// ---- export ------------------------------------------------------------------------------------------------------------------
const ORDER = ['intro', 'intro_end', 'cs1', 'sq1', 'repel', 'lead_down', 'lead_stand', 'ending'];
export const CLIPS = ORDER.map(n => clips.find(c => c.name === n));
void SW; void F_TOG;
