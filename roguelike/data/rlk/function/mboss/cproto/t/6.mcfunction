# test 6 (@s = body, at it)
execute at @s positioned ~ ~1.2 ~ facing entity @e[tag=rlk_body,limit=1] feet run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_cproto_pj"],block_state:{id:"minecraft:magma_block"},teleport_duration:1,transformation:{translation:[-0.25f,-0.25f,-0.25f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.5f,0.5f,0.5f]}}
scoreboard players set #pjNoDodge mb 1
execute at @s positioned ~ ~1.2 ~ facing entity @e[tag=rlk_body,limit=1] feet as @e[tag=rlk_mb_cproto_pj,tag=!rlk_mb_pj,limit=1] run function rlk:mboss/pj/launch {spd:5,life:60,dmg:100,hr:5}
