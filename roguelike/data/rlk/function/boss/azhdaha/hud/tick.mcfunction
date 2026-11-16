# @s = body: the floor popups, the lines every 4 t or on request.
scoreboard players remove @e[type=minecraft:text_display,tag=rlk_mb_az_pop] azT 1
kill @e[type=minecraft:text_display,tag=rlk_mb_az_pop,scores={azT=..0}]
execute if score #azHudQ mb matches 1 run return run function rlk:boss/azhdaha/hud/refresh
execute if score #azQ4 mb matches 0 run function rlk:boss/azhdaha/hud/refresh
