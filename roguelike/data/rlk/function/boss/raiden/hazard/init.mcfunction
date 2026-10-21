# @s = the new hazard at its origin. Clamp tell/life, cache the forward vector, number it, size it, decal it.
scoreboard players operation @s rdWind > #rdOne rd
scoreboard players operation @s rdHEv > #rdOne rd
scoreboard players operation #rdMinLife rd = @s rdWind
scoreboard players add #rdMinLife rd 10
execute if score @s rdHK matches 5..7 run scoreboard players operation #rdMinLife rd = @s rdWind
execute if score @s rdHK matches 5..7 run scoreboard players operation #rdMinLife rd += @s rdHF
execute if score @s rdHK matches 5..7 run scoreboard players add #rdMinLife rd 2
scoreboard players operation @s rdHLife > #rdMinLife rd
execute positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_haxis","rlk_raiden_aux","rlk_room"]}
execute store result score #rdOX rd run data get entity @s Pos[0] 1000
execute store result score #rdOZ rd run data get entity @s Pos[2] 1000
execute store result score @s rdFX run data get entity @e[tag=rlk_rd_haxis,limit=1] Pos[0] 1000
execute store result score @s rdFZ run data get entity @e[tag=rlk_rd_haxis,limit=1] Pos[2] 1000
scoreboard players operation @s rdFX -= #rdOX rd
scoreboard players operation @s rdFZ -= #rdOZ rd
kill @e[tag=rlk_rd_haxis]
scoreboard players add #rdHazardSerial rd 1
scoreboard players operation @s rdHId = #rdHazardSerial rd
execute if score @s rdHK matches 4 run function rlk:boss/raiden/hazard/k/to_wall_len
execute if score @s rdHGrp matches 1 run scoreboard players operation @s rdHGrp = #rdGrpSerial rd
execute unless score @s rdHDk matches 1.. run tag @s add rlk_rd_quiet
execute if score @s rdHDk matches 1.. run function rlk:boss/raiden/hazard/vis/decal
