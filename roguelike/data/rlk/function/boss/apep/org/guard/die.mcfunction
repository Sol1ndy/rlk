# @s = a 수호 broken: guard_die (17 t), red embers + the black wisp; with no other 수호 alive every shield goes.
function rlk:boss/apep/om/guard/play/guard_die
execute at @s positioned ~ ~1.5 ~ run function rlk:boss/apep/fx/p/guard_death
execute at @s run function rlk:boss/apep/fx/snd/o3_death
execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_guard,tag=!rlk_mb_ap_dying] run return 0
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=rlk_mb_ap_shd] run function rlk:boss/apep/org/basic/shd_pop
