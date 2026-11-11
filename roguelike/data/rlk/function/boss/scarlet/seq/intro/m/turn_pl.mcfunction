# The body turns at most 4.5 degrees toward the avatar this tick, yaw only (@s = the body).
execute store result score #sq_y0 hr run data get entity @s Rotation[0] 100
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] ~ ~ ~ ~ 0
execute store result score #sq_y1 hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Rotation[0] 100
kill @e[type=minecraft:marker,tag=rlk_hr_sqh]
scoreboard players operation #sq_y1 hr -= #sq_y0 hr
scoreboard players add #sq_y1 hr 90000
scoreboard players operation #sq_y1 hr %= #c36000 mb
scoreboard players remove #sq_y1 hr 18000
execute if score #sq_y1 hr matches 451.. run scoreboard players set #sq_y1 hr 450
execute if score #sq_y1 hr matches ..-451 run scoreboard players set #sq_y1 hr -450
scoreboard players operation #sq_y0 hr += #sq_y1 hr
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #sq_y0 hr
