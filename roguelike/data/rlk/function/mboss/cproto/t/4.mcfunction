# test 4 (@s = body, at it)
function rlk:mboss/mv/lockv {lead:10}
execute at @e[type=minecraft:marker,tag=rlk_mb_lock,limit=1] positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:30,tell:20,dmg:100}
