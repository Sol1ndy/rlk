# Missile 5 at its apex (clock 14): the late lock under the player (walk disc; kept as rlk_mb_fg_p4t4), its hazard
# (tell 14, its volley group = the missile's mbS; no decal: rule 10-20), the nose turns onto it at once.
function rlk:mboss/fieldgen/u/lockw
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p4t4]
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_kept
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_p4t4
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p4t4] remove rlk_mb_fg_lock
scoreboard players operation #hzGrp mb = @s mbS
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 41
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p4t4,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:15,tell:14,dmg:165}
data merge entity @s {teleport_duration:1}
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p4t4,limit=1] feet run tp @s ~ ~ ~ ~ ~
