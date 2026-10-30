# A random yaw and the distance fg.fz.d from the player: a marker, pulled into the walk disc; the quiet hazard
# and the dark disc decal there (same tell). The event's first disc carries its sounds.
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p11d]
execute store result storage rlk:mboss fg.fz.a double 1 run random value 0..359
function rlk:mboss/fieldgen/p/fzone/place with storage rlk:mboss fg.fz
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p11d] run function rlk:mboss/fieldgen/u/clamp_w
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 111
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p11d,limit=1] run function rlk:mboss/hz/disc {r:28,tell:15,dmg:75}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p11z
execute if score #fq11F mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p11f
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p11d,limit=1] rotated ~ 0 run function rlk:mboss/fieldgen/fx/tele/dark {r0:28,r:28,grow:1,tell:15,hold:0}
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p11d,limit=1] run function rlk:mboss/fieldgen/fx/p/erupt_tell
execute if score #fq11F mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_fg_p11d,limit=1] run function rlk:mboss/fieldgen/fx/snd/erupt_tell
scoreboard players set #fq11F mb 0
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p11d]
