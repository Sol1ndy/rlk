# @s = body: a lime orb (1.7 b) at her chest, aimed at the player, launched slow (0.35 b/t) as a pj prop in its own group.
execute rotated as @s rotated ~ 0 positioned ^ ^2.2 ^1.2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p14","rlk_mb_bf_p14o","rlk_mb_bf_p14n"],teleport_duration:1,billboard:"center",Glowing:1b,glow_color_override:11985754,brightness:{block:15,sky:15},item:{id:"minecraft:slime_ball",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.7f,1.7f,1.7f]}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ ~
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n] mbId 14
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n] mbT 0
function rlk:mboss/grp_new
scoreboard players set #pjEl mb 7
scoreboard players set #pjKB mb 2
scoreboard players operation #pjGrp mb = #mbGrp mb
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n,limit=1] at @s run function rlk:mboss/pj/launch {spd:4,life:50,dmg:150,hr:8}
tag @e[type=minecraft:item_display,tag=rlk_mb_bf_p14n] remove rlk_mb_bf_p14n
playsound minecraft:block.conduit.activate hostile @a[tag=player] ~ ~ ~ 0.5 1.6 0.17
playsound minecraft:entity.breeze.shoot hostile @a[tag=player] ~ ~ ~ 0.5 1.2 0.17
