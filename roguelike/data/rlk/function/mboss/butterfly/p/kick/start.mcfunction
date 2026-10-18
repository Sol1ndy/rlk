# H1 달빛 발차기 (lead 2: start at clock -2, clip kick_combo at 0). Hit 1 8: the strip (lane
# 4.5 x 2.4 from 0.5 behind A + splash r 1.5, one group, decals from -2); kick 2 locked at 26, the leap
# at 32, hit 2 40: half disc r 5 + ground wave 6 x 2 at B (one group); 1.0 / 1.2 Dendro.
function rlk:mboss/butterfly/rig/face/player
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p1a]
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p1b]
scoreboard players set #bfDMax mb 45
scoreboard players set #bfDKeep mb 15
function rlk:mboss/butterfly/u/dest
tag @e[type=minecraft:marker,tag=rlk_mb_bf_dest] add rlk_mb_bf_p1a
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p1a] remove rlk_mb_bf_dest
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzBack mb 5
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1a,limit=1] rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:40,w:24,tell:10,dmg:100}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1a,limit=1] rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/tele/line {len:40,w:24,back:5,tell:10,el:7,hold:3}
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1a,limit=1] rotated ~ 0 positioned ^ ^ ^1.2 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:15,tell:10,dmg:100}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1a,limit=1] rotated ~ 0 positioned ^ ^ ^1.2 positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/tele/disc {r:15,tell:10,el:7,hold:3}
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.35 1.6 0.12
