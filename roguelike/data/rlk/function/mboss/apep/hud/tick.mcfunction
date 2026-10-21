# @s = body: the floor popups age; the lines every 4 t or on request.
scoreboard players remove @e[type=minecraft:text_display,tag=rlk_mb_ap_pop] apT 1
kill @e[type=minecraft:text_display,tag=rlk_mb_ap_pop,scores={apT=..0}]
execute if score #apHudQ mb matches 1 run return run function rlk:mboss/apep/hud/refresh
scoreboard players operation #apM mb = #apFc mb
scoreboard players operation #apM mb %= #apK4 mb
execute if score #apM mb matches 0 run function rlk:mboss/apep/hud/refresh
