# vacuum clock 7
function rlk:mboss/butterfly/rig_stub/face/player
execute rotated as @s rotated ~ 0 positioned ^ ^0.9 ^1.0 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p4","rlk_mb_bf_p4b"],teleport_duration:1,brightness:{block:15,sky:15},item:{id:"minecraft:lime_stained_glass_pane",count:1},transformation:{translation:[0f,1.1f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[3f,4f,0.3f]}}
execute rotated as @s rotated ~ 0 positioned ^ ^0.9 ^1.0 run tp @e[type=minecraft:item_display,tag=rlk_mb_bf_p4b,limit=1] ~ ~ ~ ~ 0
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_bf_p4b] mbId 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzCol mb 7
execute rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:300,w:30,tell:10,dmg:0}
playsound minecraft:block.amethyst_cluster.hit hostile @a[tag=player] ~ ~ ~ 0.7 1.8 0.23
