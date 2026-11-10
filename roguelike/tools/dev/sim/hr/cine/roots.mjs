// roots.mjs: her root per sequence tick ([r, u, f, yaw] in the stage frame) from scarlet_cine.mjs rootAt, as JSON (for shots.py).
//   node tools/dev/sim/hr/cine/roots.mjs > roots.json      (run from roguelike/)
import {rootAt, CONTRACT, SEQ_OF} from '../../../../scarlet_cine.mjs';
const out = {};
for (const [clip, s] of Object.entries(SEQ_OF)) {
  out[s.seq] = out[s.seq] || [];
  for (let t = 0; t <= CONTRACT[clip].len; t++) { const r = rootAt(clip, t); out[s.seq][s.t0 + t] = [...r.p.map(x => +x.toFixed(4)), +r.yaw.toFixed(2)]; }
}
process.stdout.write(JSON.stringify(out));
