# kick clock 26
execute at @s rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:0.7} ^-0.55 ^0.001 ^-0.719 0.1 0.1 0.1 0 2 force @a[tag=player]
function rlk:mboss/butterfly/rig/face/player
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p1b]
scoreboard players set #bfDMax mb 35
scoreboard players set #bfDKeep mb 12
function rlk:mboss/butterfly/u/dest
tag @e[type=minecraft:marker,tag=rlk_mb_bf_dest] add rlk_mb_bf_p1b
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p1b] remove rlk_mb_bf_dest
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:50,a:90,tell:14,dmg:120}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/tele/sector {r:50,a:90,tell:14,el:7,hold:3}
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:60,w:20,tell:14,dmg:120}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/tele/line {len:60,w:20,back:0,tell:14,el:7,hold:3}
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.35 1.5 0.12
