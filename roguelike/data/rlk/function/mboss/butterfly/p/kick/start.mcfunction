# H1 달빛 발차기 (STUB; lead 2: start at clock -2, clip kick_combo at 0, hits 8 / 40).
function rlk:mboss/butterfly/rig_stub/face/player
scoreboard players set #bfDMax mb 40
scoreboard players set #bfDKeep mb 15
function rlk:mboss/butterfly/u/dest
tag @e[type=minecraft:marker,tag=rlk_mb_bf_dest] add rlk_mb_bf_p1a
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p1a] remove rlk_mb_bf_dest
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 2
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1a,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:40,a:75,tell:10,dmg:100}
