scoreboard players set @s infuse 4
scoreboard players set @s infuseT 160
data modify storage rlk:hud inf set from storage rlk:elem byid."ice".tag
execute at @e[tag=rlk_body,limit=1] run particle minecraft:snowflake ~ ~1 ~ 0.3 0.5 0.3 0.03 10
