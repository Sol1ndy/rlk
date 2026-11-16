# @s = body, at it: the two display parts (rlk_mb_aux: cleanup and /reload remove them).
kill @e[type=minecraft:block_display,tag=rlk_mb_cproto_part]
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_cproto_part","rlk_mb_cproto_core"],block_state:{id:"minecraft:lodestone"},teleport_duration:1,transformation:{translation:[-0.8f,0f,-0.8f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.6f,2.2f,1.6f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_cproto_part","rlk_mb_cproto_tail"],block_state:{id:"minecraft:polished_deepslate"},teleport_duration:1,transformation:{translation:[-0.5f,0f,-2.9f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
execute unless score @s mbS matches 1.. run scoreboard players set @s mbS 1
execute unless score @s mbT matches -1.. run scoreboard players set @s mbT -1
function rlk:mboss/cproto/rig/follow
