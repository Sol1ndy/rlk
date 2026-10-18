# vacuum clock 17
execute rotated as @s rotated ~ 0 positioned ^ ^0.9 ^1 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p4","rlk_mb_bf_p4b","rlk_mb_bf_p4n","rlk_mb_bf_p4g"],teleport_duration:1,interpolation_duration:3,billboard:"fixed",view_range:1.5f,shadow_radius:0f,brightness:{block:15,sky:15},item:{id:"minecraft:paper",count:1},transformation:{translation:[-0.57f,-0.324f,0f],left_rotation:[0.5f,0.5f,0.5f,0.5f],scale:[1.32f,0.3f,2.04f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 positioned ^ ^0.9 ^1 run tp @e[type=minecraft:item_display,tag=rlk_mb_bf_p4n,limit=1] ~ ~ ~ ~ 0
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p4n,limit=1] run function rlk:mboss/butterfly/fx/look {kind:"cres_lime",col:16777215}
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_bf_p4n,limit=1] mbId 4
scoreboard players set #pjKB mb 3
scoreboard players set #pjWall mb 1
scoreboard players set #pjShape mb 1
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p4n,limit=1] at @s run function rlk:mboss/pj/launch {spd:7,life:60,dmg:120,hr:15}
tag @e[type=minecraft:item_display,tag=rlk_mb_bf_p4n] remove rlk_mb_bf_p4n
scoreboard players set #bp4B mb 1
function rlk:mboss/butterfly/fx/snd/vacuum_blade
playsound minecraft:block.azalea_leaves.break hostile @a[tag=player] ~ ~ ~ 0.6 0.9 0.2
execute at @s rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.788f,0.949f,0.678f],scale:0.7} ^0 ^2.436 ^0.154 0.15 0.15 0.15 0 1 force @a[tag=player]
