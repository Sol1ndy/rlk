# Keep every telegraph and strike alive, even with a too-short caller life.
scoreboard players set #rdOne rd 1
scoreboard players operation @s rdWind > #rdOne rd
scoreboard players operation #rdMinLife rd = @s rdWind
scoreboard players add #rdMinLife rd 10
execute if score @s rdShape matches 11 run scoreboard players add #rdMinLife rd 24
scoreboard players operation @s rdHLife > #rdMinLife rd
# Cache the local-forward vector without trigonometric runtime functions.
execute positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_haxis","rlk_raiden_aux","rlk_room"]}
execute store result score #rdOX rd run data get entity @s Pos[0] 1000
execute store result score #rdOZ rd run data get entity @s Pos[2] 1000
execute store result score @s rdFX run data get entity @e[tag=rlk_rd_haxis,limit=1] Pos[0] 1000
execute store result score @s rdFZ run data get entity @e[tag=rlk_rd_haxis,limit=1] Pos[2] 1000
scoreboard players operation @s rdFX -= #rdOX rd
scoreboard players operation @s rdFZ -= #rdOZ rd
kill @e[tag=rlk_rd_haxis]
function rlk:boss/raiden/hazard/vfx_init
