# bomb clock 57
function rlk:mboss/fieldgen/rig/play/slam
function rlk:mboss/fieldgen/u/lockb
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p1f]
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_kept
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_p1f
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p1f] remove rlk_mb_fg_lock
execute at @s run function rlk:mboss/fieldgen/p/bomb/dst
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 12
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 20
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p1d,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:50,tell:17,dmg:180}
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p1d,limit=1] positioned ~ 201 ~ rotated ~ 0 run function rlk:mboss/fieldgen/fx/tele/disc {r:50,tell:17,el:5,hold:3}
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_fg_p1d,limit=1] run function rlk:mboss/mv/glide {t:10}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/snd/column_tell
