scoreboard players set @s cmS 1
scoreboard players operation @s cmT = #c3W_fu tmp
scoreboard players operation @s cmCd = #c3Cd_fu tmp
scoreboard players operation #cid tmp = @s cmId
execute as @e[tag=rlk_fu_glow,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:1b,glow_color_override:9502608}
particle minecraft:composter ~ ~1.2 ~ 0.3 0.25 0.3 0.05 8 normal
execute unless score #c3fuswell snd matches 1 run function rlk:cm/c3/snd/fuswell
execute unless score #c3fuhum snd matches 1 run function rlk:cm/c3/snd/fuhum
