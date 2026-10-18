# A random yaw and the distance fg.fz.d from the player: a marker, pulled into the walk disc, the disc there.
execute store result storage rlk:mboss fg.fz.a double 1 run random value 0..359
function rlk:mboss/fieldgen/p/fzone/place with storage rlk:mboss fg.fz
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p11d] run function rlk:mboss/fieldgen/u/clamp_w
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzVis mb 111
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p11d,limit=1] run function rlk:mboss/hz/disc {r:28,tell:15,dmg:120}
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p11d,limit=1] run particle minecraft:dust{color:[0.18f,0.12f,0.22f],scale:1.6} ~ ~0.1 ~ 1.2 0.02 1.2 0 10 force @a[tag=player]
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p11d]
