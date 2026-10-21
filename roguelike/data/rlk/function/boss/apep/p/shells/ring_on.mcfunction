# t10: the target ring (keep row: the pale disc the footage shows under the player) at the feet of 6 t
# ago (the oldest sample), and the ring position marker.
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p33q,scores={apT=6..},limit=1] at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p33","rlk_mb_ap_p33r"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p33r,limit=1] run function rlk:boss/apep/fx/tele/mring {id:0,r:36,el:22}
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p33q,scores={apT=6..}]
