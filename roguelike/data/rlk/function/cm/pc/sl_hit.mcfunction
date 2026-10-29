execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^ ^1 if entity @e[tag=rlk_body,distance=..2.5] run function rlk:cm/pc/sl_dmg
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^0.2 ^1 run particle minecraft:explosion ~ ~ ~ 0 0 0 0 1
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^0.2 ^1 run particle minecraft:block{block_state:"minecraft:smooth_quartz"} ~ ~ ~ 1.2 0.1 1.2 0 40
playsound minecraft:entity.iron_golem.attack master @a ~ ~ ~ 1 0.6
playsound minecraft:entity.generic.explode master @a ~ ~ ~ 0.4 1.3
scoreboard players set @s cmS 4
scoreboard players set @s cmT 8
tag @s remove rlk_cmch
