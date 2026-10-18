# @s = body: orb 2 (her right side), a pj prop in its own volley group, aimed at
# the player; its two gyroscope rings follow it (p/coco/orb).
kill @e[tag=rlk_mb_bf_p14o1]
kill @e[tag=rlk_mb_bf_p14r1]
kill @e[tag=rlk_mb_bf_p14v1]
execute rotated as @s rotated ~ 0 positioned ^-1.2 ^3 ^0.8 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p14","rlk_mb_bf_p14o","rlk_mb_bf_p14o1","rlk_mb_bf_p14n"],teleport_duration:1}
execute rotated as @s rotated ~ 0 positioned ^-1.2 ^3 ^0.8 run function rlk:mboss/butterfly/rig/prop/orb
tag @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_new] add rlk_mb_bf_p14v1
tag @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_new] add rlk_mb_bf_p14
tag @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_new] remove rlk_mb_bf_prop_new
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n] mbId 14
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n] mbT 0
function rlk:mboss/grp_new
scoreboard players set #pjEl mb 7
scoreboard players set #pjKB mb 2
scoreboard players operation #pjGrp mb = #mbGrp mb
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:mboss/pj/launch {spd:2,life:40,dmg:120,hr:8}
execute at @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n,limit=1] run function rlk:mboss/butterfly/fx/p/orb_launch
tag @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n] remove rlk_mb_bf_p14n
function rlk:mboss/butterfly/fx/snd/orb_launch
playsound minecraft:entity.allay.item_thrown hostile @a[tag=player] ~ ~ ~ 0.5 0.8 0.17
