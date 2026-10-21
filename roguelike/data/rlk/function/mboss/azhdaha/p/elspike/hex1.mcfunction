# t26: the hexagram at the predictive lock (lead 10); it stays to the end of the pattern.
kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]
function rlk:mboss/mv/lockv {lead:10}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] remove rlk_mb_lock
kill @e[type=minecraft:marker,tag=rlk_mb_az_p46h]
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_p46h
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46h] add rlk_mb_az_pat
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46h] add rlk_mb_az_p46
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46h] remove rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46h] remove rlk_mb_lock
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p46h,limit=1] run function rlk:mboss/azhdaha/u/clamp_w
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p46h,limit=1] run function rlk:mboss/azhdaha/fx/tele/hexagram_o {r:48,tell:18,el:3,hold:96}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p46h,limit=1] run function rlk:mboss/azhdaha/fx/snd/hex_draw
