scoreboard players set #mbHzOn mb 0
# re-arm clock of #hzRearm hazards (advances only while hazards are scanned, so a paused fight freezes it too)
scoreboard players add #mbHzClk mb 1
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] at @s rotated as @s run function rlk:mboss/hz/tick
