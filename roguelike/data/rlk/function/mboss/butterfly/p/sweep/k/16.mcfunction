# sweep clock 16
# the lock: the slam point P (dest 3 b, 2.5 b short of the player; body clamp), the aim at the player,
# the flame fan (half disc r 4.5 ahead of P, 2.5 tall, active 5 t) with its Pyro decal
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p13p]
function rlk:mboss/butterfly/rig/face/player
scoreboard players set #bfDMax mb 30
scoreboard players set #bfDKeep mb 25
function rlk:mboss/butterfly/u/dest
tag @e[type=minecraft:marker,tag=rlk_mb_bf_dest] add rlk_mb_bf_p13p
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p13p] remove rlk_mb_bf_dest
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p13p,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_b
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p13p,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ 201 ~ ~ 0
scoreboard players set #hzAct mb 5
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 25
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p13p,limit=1] run function rlk:mboss/hz/sector {r:45,a:90,tell:12,dmg:160}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p13p,limit=1] run function rlk:mboss/butterfly/fx/tele/sector {r:45,a:90,tell:12,el:1,hold:5}
# the Pyro tell cue
playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.35 1.6 0.12
