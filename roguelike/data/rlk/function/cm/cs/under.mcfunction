# the trail: one walked 0.5 b step per tick toward the body's feet (two with haste); a blocked step tries +-45 deg
scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
execute if entity @e[tag=rlk_body,distance=..0.9] run return run function rlk:cm/cs/m_start
summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2cur"]}
scoreboard players set #wK tmp 0
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 as @e[tag=rlk_c2cur,limit=1] run tp @s ~ ~ ~ ~ 0
scoreboard players operation #wN tmp = #eStep tmp
execute as @e[tag=rlk_c2cur,limit=1] at @s run function rlk:cm/cs/lib/walk_step
execute if score #wK tmp matches 0 facing entity @e[tag=rlk_body,limit=1] feet rotated ~45 0 as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/cs/u_try
execute if score #wK tmp matches 0 facing entity @e[tag=rlk_body,limit=1] feet rotated ~-45 0 as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/cs/u_try
execute if score #wK tmp matches 1.. run tp @s @e[tag=rlk_c2cur,limit=1]
execute if score #wK tmp matches 0 run scoreboard players add @s cmN 1
kill @e[tag=rlk_c2cur]
execute at @s run particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.15 ~ 0.3 0.08 0.3 0 7
execute at @s run particle minecraft:falling_dust{block_state:"minecraft:red_sand"} ~ ~0.35 ~ 0.25 0.1 0.25 0 2
execute store result score #c2t tmp run scoreboard players get @s cmT
scoreboard players operation #c2t tmp %= #3 tmp
execute if score #c2t tmp matches 0 at @s run playsound minecraft:block.sand.hit master @a ~ ~ ~ 0.8 0.7
execute if score @s cmN matches 6.. run return run function rlk:cm/cs/m_start
execute if score @s cmT matches ..0 run function rlk:cm/cs/m_start
