# A new hexagram under the player (lump 2): to the end of the pattern.
kill @e[type=minecraft:marker,tag=rlk_mb_az_p46h]
function rlk:mboss/azhdaha/u/lockp
kill @e[type=minecraft:marker,tag=rlk_mb_az_p46h]
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_p46h
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46h] add rlk_mb_az_pat
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46h] add rlk_mb_az_p46
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46h] remove rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46h] remove rlk_mb_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p46h,limit=1] run function rlk:mboss/azhdaha/fx/tele/hexagram {r:48,tell:13,el:3,hold:86}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p46h,limit=1] run function rlk:mboss/azhdaha/fx/snd/hex_draw
