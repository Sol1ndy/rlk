# @s = body, at it: two block displays (a pillar and a crown; rlk_mb_aux: cleanup and /reload remove them).
kill @e[type=minecraft:block_display,tag=rlk_mb_spproto_part]
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_spproto_part"],block_state:{id:"minecraft:obsidian"},teleport_duration:1,transformation:{translation:[-0.45f,0f,-0.45f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,2.2f,0.9f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_spproto_part","rlk_mb_spproto_crown"],block_state:{id:"minecraft:sea_lantern"},brightness:{sky:15,block:15},teleport_duration:1,transformation:{translation:[-0.3f,2.3f,-0.3f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.6f,0.6f,0.6f]}}
function rlk:mboss/spproto/rig/follow
