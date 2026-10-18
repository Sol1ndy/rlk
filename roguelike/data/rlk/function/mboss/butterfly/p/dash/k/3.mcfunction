# dash clock 3
particle minecraft:dust{color:[0.78f,0.859f,0.459f],scale:0.6} ~ ~1.0 ~ 0.9 0.9 0.9 0 3 force @a[tag=player]
particle minecraft:end_rod ~ ~1.0 ~ 0.8 0.6 0.8 0.02 1 force @a[tag=player]
function rlk:mboss/butterfly/rig/face/player
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p3a]
scoreboard players set #bfDMax mb 70
scoreboard players set #bfDKeep mb 15
function rlk:mboss/butterfly/u/dest
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p3a]
tag @e[type=minecraft:marker,tag=rlk_mb_bf_dest] add rlk_mb_bf_p3a
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p3a] add rlk_mb_bf_kept
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p3a] remove rlk_mb_bf_dest
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] rotated ~ 0 positioned ^ ^ ^1.2 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:15,tell:12,dmg:130}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] rotated ~ 0 positioned ^ ^ ^1.2 positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/tele/disc {r:15,tell:12,el:7,hold:3}
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 3
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:35,tell:16,dmg:130}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/tele/disc {r:35,tell:16,el:7,hold:3}
function rlk:mboss/butterfly/p/dash/dist
function rlk:mboss/butterfly/p/dash/lane
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.35 1.6 0.12
