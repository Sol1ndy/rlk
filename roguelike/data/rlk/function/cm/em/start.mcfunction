scoreboard players set @s cmS 1
scoreboard players operation @s cmT = #c3W_em tmp
tag @s add rlk_c3fresh
scoreboard players operation @s cmCd = #c3Cd_em tmp
scoreboard players operation #cid tmp = @s cmId
execute as @e[tag=rlk_c3glow,tag=rlk_em_pt,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:1b,glow_color_override:16757606}
particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.2 ~ 0.3 0.05 0.3 0.1 8 normal
execute unless score #c3emcrouch snd matches 1 run function rlk:cm/c3/snd/emcrouch
execute unless score #c3emglint snd matches 1 run function rlk:cm/c3/snd/emglint
