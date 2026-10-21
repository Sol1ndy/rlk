# @s = body: turn toward the arena centre by <= 12 degrees (mboss/mv/turn with the centre as the target).
execute store result score #apq32Y0 mb run data get entity @s Rotation[0] 100
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p32","rlk_mb_ap_p32y"]}
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] feet run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p32y,limit=1] ~ ~ ~ ~ 0
execute store result score #apq32Y1 mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_ap_p32y,limit=1] Rotation[0] 100
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p32y]
scoreboard players operation #apq32Y1 mb -= #apq32Y0 mb
scoreboard players add #apq32Y1 mb 90000
scoreboard players operation #apq32Y1 mb %= #c36000 mb
scoreboard players remove #apq32Y1 mb 18000
execute if score #apq32Y1 mb matches 1201.. run scoreboard players set #apq32Y1 mb 1200
execute if score #apq32Y1 mb matches ..-1201 run scoreboard players set #apq32Y1 mb -1200
scoreboard players operation #apq32Y0 mb += #apq32Y1 mb
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #apq32Y0 mb
