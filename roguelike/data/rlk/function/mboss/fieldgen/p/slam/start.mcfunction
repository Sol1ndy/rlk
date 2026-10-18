# C2 내려찍기 (clip slam; @s = body): lock + glide 10 t, slam r 5 at 17.
function rlk:mboss/fieldgen/u/lockb
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p2a]
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_kept
tag @e[type=minecraft:marker,tag=rlk_mb_fg_lock] add rlk_mb_fg_p2a
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p2a] remove rlk_mb_fg_lock
tag @e[type=minecraft:marker,tag=rlk_mb_fg_p2a,limit=1] add rlk_mb_fg_pat
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_fg_p2a,limit=1] run function rlk:mboss/mv/glide {t:10}
scoreboard players set #hzKB mb 4
scoreboard players set #hzVis mb 21
scoreboard players set #hzY1 mb 20
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p2a,limit=1] run function rlk:mboss/hz/disc {r:50,tell:17,dmg:140}
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.9 0.7 0.3
playsound minecraft:block.piston.extend hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p2a,limit=1] run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1.6} ~ ~4.2 ~ 0.12 0.05 0.12 0 2 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p2a,limit=1] run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1.6} ~ ~3.15 ~ 0.12 0.05 0.12 0 2 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p2a,limit=1] run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1.6} ~ ~2.1 ~ 0.12 0.05 0.12 0 2 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p2a,limit=1] run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1.6} ~ ~1.05 ~ 0.12 0.05 0.12 0 2 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_fg_p2a,limit=1] run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1.6} ~ ~0.21 ~ 0.12 0.05 0.12 0 2 force @a[tag=player]
