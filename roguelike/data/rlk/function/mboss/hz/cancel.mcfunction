# Cancels the hazard with id #hzLast mb (or any: set #hzLast mb before the call). Module visuals get event 2.
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb at @s rotated as @s run function rlk:mboss/hz/expire
