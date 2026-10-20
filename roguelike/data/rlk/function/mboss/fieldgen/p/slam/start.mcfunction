# C2 내려찍기 (clip slam; @s = body): face, lock + glide 10 t, slam r 5 at 17.
function rlk:mboss/fieldgen/rig/face/player
function rlk:mboss/fieldgen/u/lockb
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p2a]
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_kept
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_p2a
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p2a] remove rlk_mb_fg_lock
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p2a,limit=1] add rlk_mb_fg_pat
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 21
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 20
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p2a,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:50,tell:17,dmg:270}
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_fg_p2a,limit=1] run function rlk:mboss/mv/glide {t:10}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/snd/column_tell
