scoreboard players set @s cmS 1
scoreboard players set @s cmAR 0
scoreboard players operation @s cmT = #c2W_ns tmp
tag @s add rlk_c2fresh
scoreboard players operation @s cmCd = #c2Cd_ns tmp
scoreboard players operation #cid tmp = @s cmId
execute as @e[tag=rlk_ns_katana,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:1b,glow_color_override:16775885}
particle minecraft:electric_spark ~ ~2.0 ~ 0.25 0.3 0.25 0.05 6 normal
execute unless score #c2nsraise snd matches 1 run function rlk:cm/c2/snd/nsraise
execute unless score #c2nsglint snd matches 1 run function rlk:cm/c2/snd/nsglint
