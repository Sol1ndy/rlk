# Visual javelin: a block-display prop that flies 0.25 b sub-steps forward, then back to the body (pj/launch,
# #pjRet 1). The damage belongs to the line hazard created at the start of the pattern (K23 style).
execute rotated as @s rotated ~ 0 positioned ^-0.6 ^1.5 ^0.8 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_proto_jav"],block_state:{id:"minecraft:stripped_dark_oak_log"},teleport_duration:1,transformation:{translation:[-0.08f,-0.08f,-1.0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.16f,0.16f,2.0f]}}
scoreboard players set #pjRet mb 1
execute rotated as @s rotated ~ 0 positioned ^-0.6 ^1.5 ^0.8 as @e[tag=rlk_mb_proto_jav,tag=!rlk_mb_pj,limit=1] run function rlk:mboss/pj/launch {spd:30,life:9,dmg:0,hr:6}
playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 0.7 0.3
