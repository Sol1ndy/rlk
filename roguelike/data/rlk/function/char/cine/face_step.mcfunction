# Internal: one step of the face turn (the short way round), the parts take the root's yaw.
execute store result score #y cine run data get entity @e[type=minecraft:marker,tag=rlk_cine_root,limit=1] Rotation[0] 100
scoreboard players operation #dy cine = #cavFy cine
scoreboard players operation #dy cine -= #y cine
scoreboard players set #c36000 cine 36000
scoreboard players add #dy cine 18000
scoreboard players operation #dy cine %= #c36000 cine
scoreboard players remove #dy cine 18000
scoreboard players operation #dy cine /= #cavF cine
scoreboard players operation #y cine += #dy cine
execute as @e[type=minecraft:marker,tag=rlk_cine_root,limit=1] store result entity @s Rotation[0] float 0.01 run scoreboard players get #y cine
scoreboard players remove #cavF cine 1
execute as @e[type=minecraft:marker,tag=rlk_cine_root,limit=1] at @s run tp @e[type=minecraft:item_display,tag=rlk_cine_part] ~ ~ ~ ~ 0
