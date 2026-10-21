# A new hexagram under the player (lump 3): to the end of the pattern.
kill @e[type=minecraft:marker,tag=rlk_mb_az_p46h]
function rlk:boss/azhdaha/u/lockp
kill @e[type=minecraft:marker,tag=rlk_mb_az_p46h]
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_p46h
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46h] add rlk_mb_az_pat
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46h] add rlk_mb_az_p46
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46h] remove rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_p46h] remove rlk_mb_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p46h,limit=1] run function rlk:boss/azhdaha/fx/tele/hexagram_o {r:48,tell:13,el:3,hold:66}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p46h,limit=1] run function rlk:boss/azhdaha/fx/snd/hex_draw
