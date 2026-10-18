# @s = body: orb 1 (her chest, ahead), a pj prop in its own volley group, aimed at
# the player; its two gyroscope rings follow it (p/coco/orb).
kill @e[tag=rlk_mb_bf_p14o0]
kill @e[tag=rlk_mb_bf_p14r0]
kill @e[tag=rlk_mb_bf_p14v0]
execute rotated as @s rotated ~ 0 positioned ^0 ^3 ^1.2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p14","rlk_mb_bf_p14o","rlk_mb_bf_p14o0","rlk_mb_bf_p14n"],teleport_duration:1,brightness:{block:15,sky:15}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n] run function rlk:mboss/butterfly/fx/prop/orb
execute rotated as @s rotated ~ 0 positioned ^0 ^3 ^1.2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p14","rlk_mb_bf_p14r","rlk_mb_bf_p14r0","rlk_mb_bf_p14r0a","rlk_mb_bf_p14m"],teleport_duration:1,Rotation:[0f,0f]}
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14m] run function rlk:mboss/butterfly/fx/prop/orb_ring
tag @e[type=minecraft:item_display,tag=rlk_mb_bf_p14m] remove rlk_mb_bf_p14m
execute rotated as @s rotated ~ 0 positioned ^0 ^3 ^1.2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p14","rlk_mb_bf_p14r","rlk_mb_bf_p14r0","rlk_mb_bf_p14r0b","rlk_mb_bf_p14m"],teleport_duration:1,Rotation:[30f,55f]}
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14m] run function rlk:mboss/butterfly/fx/prop/orb_ring
tag @e[type=minecraft:item_display,tag=rlk_mb_bf_p14m] remove rlk_mb_bf_p14m
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n] mbId 14
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n] mbT 0
function rlk:mboss/grp_new
scoreboard players set #pjEl mb 7
scoreboard players set #pjKB mb 2
scoreboard players operation #pjGrp mb = #mbGrp mb
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:mboss/pj/launch {spd:2,life:40,dmg:150,hr:8}
execute at @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n,limit=1] run function rlk:mboss/butterfly/fx/p/orb_launch
tag @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n] remove rlk_mb_bf_p14n
function rlk:mboss/butterfly/fx/snd/orb_launch
playsound minecraft:entity.allay.item_thrown hostile @a[tag=player] ~ ~ ~ 0.5 0.8 0.17
