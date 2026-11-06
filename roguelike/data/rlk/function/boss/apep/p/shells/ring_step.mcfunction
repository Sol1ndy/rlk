# Every 2 t to t32: the ring to the feet of 6 t ago (the kit moves it over 2 t).
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p33q,scores={apT=6..},limit=1] at @s run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p33r,limit=1] ~ ~ ~
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p33r,limit=1] run function rlk:boss/apep/fx/tele/mring_move {id:0,t:2}
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p33q,scores={apT=6..}]
