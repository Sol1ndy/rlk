# @s = a melee basic: at most 3 basics hold an attack slot (rlk_mb_ap_tok); the lowest free cradle socket (r 3.4).
execute store result score #apX mb if entity @e[type=minecraft:husk,tag=rlk_mb_ap_tok]
execute if score #apX mb matches 3.. run return fail
execute unless entity @e[type=minecraft:husk,tag=rlk_mb_ap_sk0] run return run function rlk:boss/apep/org/basic/take0
execute unless entity @e[type=minecraft:husk,tag=rlk_mb_ap_sk1] run return run function rlk:boss/apep/org/basic/take1
execute unless entity @e[type=minecraft:husk,tag=rlk_mb_ap_sk2] run return run function rlk:boss/apep/org/basic/take2
return fail
