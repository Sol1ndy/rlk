# @s = body: fire crescent 3 of swing 1 at her wing root (60 degrees), a pj prop (harmless until it
# lands; the swing's volley group), then the fan-out glide (5 t, rising); the dive starts in fly at age 5.
kill @e[type=minecraft:item_display,tag=rlk_mb_bf_p12c13]
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p12q13]
execute rotated as @s rotated ~ 0 positioned ^2.078 ^3.6 ^1.2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12c","rlk_mb_bf_p12c13","rlk_mb_bf_p12n"],teleport_duration:1,brightness:{block:15,sky:15}}
execute rotated as @s rotated ~ 0 positioned ^2.078 ^3.6 ^1.2 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","rlk_mb_bf_p12q","rlk_mb_bf_p12q13"]}
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p12n] run function rlk:mboss/butterfly/fx/prop/fire
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_bf_p12n] mbId 12
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_bf_p12n] mbT 0
scoreboard players set #pjEl mb 1
scoreboard players set #pjKB mb 2
scoreboard players set #pjWall mb 0
scoreboard players operation #pjGrp mb = #mbGrp mb
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p12n,limit=1] at @s rotated ~ -90 run function rlk:mboss/pj/launch {spd:2,life:68,dmg:0,hr:12}
# its landing age mbS = 5 + D; the pj life ends the tick after
scoreboard players operation @e[type=minecraft:item_display,tag=rlk_mb_bf_p12n] mbS = #bp12D13 mb
scoreboard players add @e[type=minecraft:item_display,tag=rlk_mb_bf_p12n] mbS 5
scoreboard players operation @e[type=minecraft:item_display,tag=rlk_mb_bf_p12n] mbPjL = @e[type=minecraft:item_display,tag=rlk_mb_bf_p12n,limit=1] mbS
scoreboard players add @e[type=minecraft:item_display,tag=rlk_mb_bf_p12n] mbPjL 1
execute rotated as @s rotated ~ 0 positioned ^4.207 ^5.321 ^2.429 as @e[type=minecraft:item_display,tag=rlk_mb_bf_p12n,limit=1] run function rlk:mboss/mv/glide {t:5}
execute at @e[type=minecraft:item_display,tag=rlk_mb_bf_p12n,limit=1] run function rlk:mboss/butterfly/fx/p/fire_spawn
tag @e[type=minecraft:item_display,tag=rlk_mb_bf_p12n] remove rlk_mb_bf_p12n
