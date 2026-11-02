# The three wisps over their rim posts (@s any; idempotent): white, wisps 1 and 2 red from P2 on (PLAN §8.4; the
# same two seq/t_p2 turns red).
kill @e[type=minecraft:item_display,tag=rlk_kn_wisp]
execute positioned 760.5 204.6 -20.5 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_wisp","rlk_kn_wisp0"]}
execute as @e[type=minecraft:item_display,tag=rlk_kn_wisp0] run function rlk:boss/arlecchino/fx/prop/wisp {c:1}
execute positioned 774.5 204.6 32.5 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_wisp","rlk_kn_wisp1"]}
execute unless score #ph kn matches 5 as @e[type=minecraft:item_display,tag=rlk_kn_wisp1] run function rlk:boss/arlecchino/fx/prop/wisp {c:1}
execute if score #ph kn matches 5 as @e[type=minecraft:item_display,tag=rlk_kn_wisp1] run function rlk:boss/arlecchino/fx/prop/wisp {c:2}
execute positioned 745.5 204.6 32.5 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_wisp","rlk_kn_wisp2"]}
execute unless score #ph kn matches 5 as @e[type=minecraft:item_display,tag=rlk_kn_wisp2] run function rlk:boss/arlecchino/fx/prop/wisp {c:1}
execute if score #ph kn matches 5 as @e[type=minecraft:item_display,tag=rlk_kn_wisp2] run function rlk:boss/arlecchino/fx/prop/wisp {c:2}
