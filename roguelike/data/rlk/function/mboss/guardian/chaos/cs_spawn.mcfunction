# @s = body: a new cube stream (at most 3) from around her, homing on the floor near the player.
execute store result score #gdR mb run random value 18..30
scoreboard players operation #gdCsT mb = #gdR mb
scoreboard players set #gdCsN mb 0
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs] run scoreboard players add #gdCsN mb 1
execute if score #gdCsN mb matches 3.. run return 0
summon minecraft:block_display ~ ~4.6 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_fx","rlk_mb_gd_cs","rlk_mb_gd_csnew"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gold_block"},teleport_duration:1,view_range:2f,transformation:{translation:[-0.22f,-0.22f,-0.22f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.44f,0.44f,0.44f]}}
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_csnew,limit=1] store result entity @s Rotation[0] float 1 run random value 0..359
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_csnew,limit=1] run data modify entity @s Rotation[1] set value -35.0f
scoreboard players set @e[type=minecraft:block_display,tag=rlk_mb_gd_csnew,limit=1] mbT 0
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_csnew,limit=1] store result score @s mbS run random value 1..2
tag @e[type=minecraft:block_display,tag=rlk_mb_gd_csnew] remove rlk_mb_gd_csnew
playsound minecraft:entity.blaze.shoot hostile @a[tag=player] ~ ~ ~ 0.25 0.6 0.3
