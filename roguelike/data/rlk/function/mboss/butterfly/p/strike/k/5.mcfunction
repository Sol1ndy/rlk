# strike clock 5
function rlk:mboss/butterfly/rig_stub/face/player
scoreboard players set #bfDMax mb 60
scoreboard players set #bfDKeep mb 15
function rlk:mboss/butterfly/u/dest
tag @e[type=minecraft:marker,tag=rlk_mb_bf_dest] add rlk_mb_bf_p11a
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p11a] remove rlk_mb_bf_dest
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 2
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11a,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:40,a:80,tell:10,dmg:130}
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzBack mb 20
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11a,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:40,w:20,tell:10,dmg:130}
