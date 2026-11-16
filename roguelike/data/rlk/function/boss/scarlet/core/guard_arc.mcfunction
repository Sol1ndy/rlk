# @s = the body in a leap (mboss/mv/leap: the arc of mbMvH): the arc is kept; its end (mbMvX1 / Z1) inside 1.6 b of the
# avatar on the floor plane moves straight away from the avatar to 1.7 b (when mv/ok passes there).
kill @e[type=minecraft:marker,tag=rlk_hr_bxn]
execute positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_hr_bxn","rlk_room","rlk_mb_aux"]}
execute store result entity @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1] Pos[0] double 0.001 run scoreboard players get @s mbMvX1
execute store result entity @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1] Pos[2] double 0.001 run scoreboard players get @s mbMvZ1
execute at @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1] unless entity @e[tag=rlk_body,distance=..1.6] run return run kill @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1]
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ facing entity @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1] feet rotated ~ 0 positioned ^ ^ ^1.7 if function rlk:mboss/mv/ok run tp @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1] ~ ~ ~
execute at @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1] if entity @e[tag=rlk_body,distance=..1.6] run return run kill @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1]
execute store result score @s mbMvX1 run data get entity @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1] Pos[0] 1000
execute store result score @s mbMvZ1 run data get entity @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1] Pos[2] 1000
kill @e[type=minecraft:marker,tag=rlk_hr_bxn,limit=1]
