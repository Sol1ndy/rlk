# t33: the ring stops = lock 1 (L1); shell 1 r 3.6 (tell 12, light KB, 52 %) with the
# held target disc of the keep row; the history goes.
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p33r,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p33","rlk_mb_ap_p33a"]}
function rlk:boss/apep/fx/tele/mring_end {id:0}
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p33q]
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p33a,limit=1] run function rlk:boss/apep/p/shells/hz1
