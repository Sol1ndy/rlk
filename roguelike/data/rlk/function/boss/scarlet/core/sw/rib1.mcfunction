# @s = the growing ribbon, at it, facing the marker rlk_hr_trt: turn there; its length = (marker - here) . the aim (x 1000).
tp @s ~ ~ ~ ~ ~
execute positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_hr_tru","rlk_room","rlk_mb_aux"]}
execute store result score #sw_x hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_trt,limit=1] Pos[0] 1000
execute store result score #sw_y hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_trt,limit=1] Pos[1] 1000
execute store result score #sw_z hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_trt,limit=1] Pos[2] 1000
execute store result score #sw_n hr run data get entity @s Pos[0] 1000
scoreboard players operation #sw_x hr -= #sw_n hr
execute store result score #sw_u hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_tru,limit=1] Pos[0] 1000
scoreboard players operation #sw_u hr -= #sw_n hr
scoreboard players operation #sw_x hr *= #sw_u hr
execute store result score #sw_n hr run data get entity @s Pos[1] 1000
scoreboard players operation #sw_y hr -= #sw_n hr
execute store result score #sw_u hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_tru,limit=1] Pos[1] 1000
scoreboard players operation #sw_u hr -= #sw_n hr
scoreboard players operation #sw_y hr *= #sw_u hr
execute store result score #sw_n hr run data get entity @s Pos[2] 1000
scoreboard players operation #sw_z hr -= #sw_n hr
execute store result score #sw_u hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_tru,limit=1] Pos[2] 1000
scoreboard players operation #sw_u hr -= #sw_n hr
scoreboard players operation #sw_z hr *= #sw_u hr
kill @e[type=minecraft:marker,tag=rlk_hr_tru]
scoreboard players operation #sw_x hr += #sw_y hr
scoreboard players operation #sw_x hr += #sw_z hr
execute if score #sw_x hr matches ..0 run return 0
execute store result entity @s transformation.scale[2] float 0.000001 run scoreboard players get #sw_x hr
