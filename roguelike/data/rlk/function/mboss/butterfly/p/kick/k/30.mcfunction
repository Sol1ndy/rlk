# kick clock 30
function rlk:mboss/butterfly/rig_stub/face/player
scoreboard players set #bfDMax mb 30
scoreboard players set #bfDKeep mb 10
function rlk:mboss/butterfly/u/dest
tag @e[type=minecraft:marker,tag=rlk_mb_bf_dest] add rlk_mb_bf_p1b
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p1b] remove rlk_mb_bf_dest
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 2
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:50,a:90,tell:10,dmg:120}
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:60,w:20,tell:10,dmg:120}
