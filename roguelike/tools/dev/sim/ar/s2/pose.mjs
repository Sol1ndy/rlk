// node pose.mjs <name> <form> '<json overrides>' [base: p1|p2]  -> dbg kn_dbg/p/<name> (solved pose, models)
import fs from 'node:fs';
import {solve, toDisplay} from '../wt_s2/roguelike/tools/arlecchino_pose.mjs';
import {DEFAULT_POSE, P2_POSE} from '../wt_s2/roguelike/tools/arlecchino_clips.mjs';
import {nbt, written} from '../wt_s2/roguelike/tools/mboss_rig_compile.mjs';
import {PART_NAMES} from '../wt_s2/roguelike/tools/arlecchino_geometry.mjs';
const [name, form, js, b] = process.argv.slice(2);
const base = (b || form) === 'p2' ? P2_POSE : DEFAULT_POSE;
const p = {...base, ph: 0, ...(0, eval)("(" + (js || "{}") + ")")};
const r = solve(p, form);
const NN = n => PART_NAMES.indexOf(n);
const uuid = n => `524c4b4d-4b4e-4100-8000-${NN(n).toString(16).padStart(12, '0')}`;
const L = [];
for (const n of PART_NAMES) { const d = toDisplay(r.parts[n]); L.push(`data merge entity ${uuid(n)} {start_interpolation:0,interpolation_duration:0,transformation:${nbt(written(d))}}`);
  L.push(`data modify entity ${uuid(n)} item.components."minecraft:item_model" set value "${r.parts[n].model}"`); }
fs.mkdirSync('dbg/data/rlk/function/kn_dbg/p', {recursive: true});
fs.writeFileSync(`dbg/data/rlk/function/kn_dbg/p/${name}.mcfunction`, L.join('\n') + '\n');
console.log('guards', JSON.stringify(r.guards), 'lift', r.lift.toFixed(3), 'blade_r', r.anchors.blade_r.map(x => x.toFixed(2)).join(','));
