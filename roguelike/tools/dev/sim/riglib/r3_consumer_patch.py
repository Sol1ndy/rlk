#!/usr/bin/env python3
"""r3_consumer_patch.py <tools dir>: switches the R1 Azhdaha builder (7c3e9fe) to the RIGLIB runtime helpers
(summonPart, summonShadow, createRigFollow in the classic one-list form). The outputs stay byte-identical; R3 can
start from this when it adds the per-state lists, the sink offsets and the static skip."""
import sys, pathlib
p = pathlib.Path(sys.argv[1]) / 'build_mboss_azhdaha_rig.mjs'
s = p.read_text()
rep = [
  ("import {createRigCompiler, nbt} from './mboss_rig_compile.mjs';",
   "import {createRigCompiler, nbt, summonPart, summonShadow, createRigFollow} from './mboss_rig_compile.mjs';"),
  ("const summon = ([n, model, bright], pose) => `summon minecraft:item_display ~ ~ ~ {UUID:${uuidInts(n)},Tags:${TAGS(n)},billboard:\"fixed\",item_display:\"none\",interpolation_duration:1,teleport_duration:1,view_range:${VIEW_RANGE}f,width:${CULL.width}f,height:${CULL.height}f,shadow_radius:0f,brightness:{block:${bright},sky:15},transformation:${nbt(pose)},item:{id:\"minecraft:paper\",count:1,components:{\"minecraft:item_model\":\"${itemId(model)}\"}}}`;",
   "const summon = ([n, model, bright], pose) => summonPart({uuid: uuidInts(n), tags: TAGS(n), item: itemId(model), brightness: bright, pose, viewRange: VIEW_RANGE, cull: CULL});"),
  ("const shadowSummon = `summon minecraft:item_display ~ ~ ~ {UUID:${SHADOW_INTS},Tags:[\"rlk_room\",\"rlk_mb_aux\",\"rlk_mb_azhdaha_part\",\"rlk_mb_az_shadow\"],billboard:\"fixed\",item_display:\"none\",teleport_duration:1,view_range:${VIEW_RANGE}f,width:${CULL.width}f,height:${CULL.height}f,shadow_radius:4.5f,shadow_strength:.8f,item:{id:\"minecraft:paper\",count:1,components:{\"minecraft:item_model\":\"${itemId(EMPTY)}\"}}}`;",
   "const shadowSummon = summonShadow({uuid: SHADOW_INTS, tags: ['rlk_room', 'rlk_mb_aux', 'rlk_mb_azhdaha_part', 'rlk_mb_az_shadow'], item: itemId(EMPTY), radius: 4.5, strength: .8, viewRange: VIEW_RANGE, cull: CULL});"),
  ("fn('follow', ['# Parts (and the shadow helper) follow the executor position and yaw (run rotated as the anchor, pitch 0).', ...PARTS.map(([n]) => `tp ${uuidOf(n)} ~ ~ ~ ~ ~`), `tp ${SHADOW_UUID} ~ ~ ~ ~ ~`]);",
   "createRigFollow({ns: NS, obj: 'azRig', fn, uuidOf: n => (n === 'shadow' ? SHADOW_UUID : uuidOf(n)), lists: {all: PARTS.map(([n]) => n)}, fixed: ['shadow'],\n  comment: '# Parts (and the shadow helper) follow the executor position and yaw (run rotated as the anchor, pitch 0).'}).write();"),
]
for a, b in rep:
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
p.write_text(s)
print('patched', p)
