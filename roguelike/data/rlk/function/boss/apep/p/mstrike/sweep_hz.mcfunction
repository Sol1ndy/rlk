# At E (t48): the 360-degree tail whip r 12.0 low (#hzY1 0.7: a jump clears it), tell
# 21 (hit t69), quiet; the slam's volley group (one hit at most).
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 7
scoreboard players operation #hzGrp mb = #apq31G mb
function rlk:mboss/hz/disc {r:120,tell:21,dmg:60}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p31h
