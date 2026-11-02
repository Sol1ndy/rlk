# The three wisps at their rim posts (@s any; idempotent): white, two of them red from P2 on (PLAN §8.4).
kill @e[type=minecraft:item_display,tag=rlk_kn_wisp]
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] rotated 180 0 positioned ^ ^ ^28 positioned ~ 202 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_wisp","rlk_kn_wisp0"]}
execute unless score #ph kn matches 5 as @e[type=minecraft:item_display,tag=rlk_kn_wisp0] run function rlk:boss/arlecchino/fx/prop/wisp {c:1}
execute if score #ph kn matches 5 as @e[type=minecraft:item_display,tag=rlk_kn_wisp0] run function rlk:boss/arlecchino/fx/prop/wisp {c:2}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] rotated 330 0 positioned ^ ^ ^28 positioned ~ 202 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_wisp","rlk_kn_wisp1"]}
execute unless score #ph kn matches 5 as @e[type=minecraft:item_display,tag=rlk_kn_wisp1] run function rlk:boss/arlecchino/fx/prop/wisp {c:1}
execute if score #ph kn matches 5 as @e[type=minecraft:item_display,tag=rlk_kn_wisp1] run function rlk:boss/arlecchino/fx/prop/wisp {c:2}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] rotated 390 0 positioned ^ ^ ^28 positioned ~ 202 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_wisp","rlk_kn_wisp2"]}
execute as @e[type=minecraft:item_display,tag=rlk_kn_wisp2] run function rlk:boss/arlecchino/fx/prop/wisp {c:1}
