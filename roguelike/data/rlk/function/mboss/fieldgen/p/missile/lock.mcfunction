# @s = a missile at its apex: the late lock under the player (walk disc), its decal (tell 13), the dive.
function rlk:mboss/fieldgen/u/lockw
scoreboard players operation #hzGrp mb = @s mbS
scoreboard players set #hzKB mb 3
scoreboard players set #hzVis mb 41
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_lock,limit=1] run function rlk:mboss/hz/disc {r:15,tell:13,dmg:90}
data merge entity @s {teleport_duration:12}
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_lock,limit=1] run tp @s ~ ~0.6 ~
kill @e[type=minecraft:marker,tag=rlk_mb_fg_lock]
playsound minecraft:entity.breeze.wind_burst hostile @a[tag=player] ~ ~ ~ 0.4 1.6 0.13
