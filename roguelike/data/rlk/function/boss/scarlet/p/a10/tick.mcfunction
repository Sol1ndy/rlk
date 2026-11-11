# A10 황광 낙참: one pattern tick (#pt hr = 1..32); events in k/<t>.
execute if score #pt hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 9..13 run function rlk:boss/scarlet/p/a10/drift
execute if score #pt hr matches 9..13 run function rlk:mboss/mv/turn {max:20}
execute if score #pt hr matches 23..31 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 27..31 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/a10/k/2
execute if score #pt hr matches 5 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:15}
execute if score #pt hr matches 8 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:15}
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/a10/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/a10/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/a10/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/a10/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/a10/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/a10/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/a10/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/a10/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/a10/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/a10/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/a10/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/a10/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/a10/k/22
execute if score #pt hr matches 23 as @e[type=minecraft:item_display,tag=rlk_hr_sw_a1022_21] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/a10/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/a10/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/a10/k/26
execute if score #pt hr matches 27 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a1022_21]
execute if score #pt hr matches 28 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a1022_22]
execute if score #pt hr matches 32 run scoreboard players set #done hr 1
