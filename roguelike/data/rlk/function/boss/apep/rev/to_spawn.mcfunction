scoreboard players set #apToT mb 0
execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_destr,tag=!rlk_mb_ap_dying,limit=1] run return 0
execute if entity @e[type=minecraft:marker,tag=rlk_mb_ap_ospawn,scores={apK=5}] run return 0
function rlk:boss/apep/rev/cands
function rlk:boss/apep/rev/mk_destr
kill @e[type=minecraft:marker,tag=rlk_mb_ap_cand]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_cused]
