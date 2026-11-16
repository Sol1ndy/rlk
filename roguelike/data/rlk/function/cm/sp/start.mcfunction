scoreboard players set @s cmS 1
scoreboard players operation @s cmT = #c2W_sp tmp
tag @s add rlk_c2fresh
scoreboard players operation @s cmCd = #c2Cd_sp tmp
scoreboard players operation #cid tmp = @s cmId
execute as @e[tag=rlk_sp_yari,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:1b,glow_color_override:16772710,brightness:{sky:15,block:15}}
execute unless score #c2spready snd matches 1 run function rlk:cm/c2/snd/spready
execute unless score #c2spglint snd matches 1 run function rlk:cm/c2/snd/spglint
