# @s = body (t73): hit 3, the low spin: a disc r 7.2 about the body, jumpable (#hzY1 7),
# tell 10 (none row: the twist from t73), 90 %.
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 7
execute at @s positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:72,tell:10,dmg:90}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p6
