# @s = the body, the avatar (almost) on her centre: the way out is her facing.
kill @e[type=minecraft:marker,tag=rlk_hr_bxn]
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_hr_bxn","rlk_room","rlk_mb_aux"]}
execute store result score #bx_ux hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1] Pos[0] 1000
execute store result score #bx_uz hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1] Pos[2] 1000
kill @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1]
scoreboard players operation #bx_ux hr -= #bx_px hr
scoreboard players operation #bx_uz hr -= #bx_pz hr
function rlk:boss/scarlet/core/sep_go
