# A3S 쌍월참: one pattern tick (#pt hr = 1..40); events in k/<t>.
execute if score #pt hr matches 1..13 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 1..7 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 15..23 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 16..25 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 26..29 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.375}
execute if score #pt hr matches 31..32 if score #pp hr matches 1 run function rlk:boss/scarlet/core/pp
execute if score #pt hr matches 31..39 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 35..39 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 1 if score #ph hr matches 7 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:42}
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/a3s/k/2
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/a3s/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/a3s/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/a3s/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/a3s/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/a3s/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/a3s/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/a3s/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/a3s/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/a3s/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/a3s/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/a3s/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/a3s/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/a3s/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/a3s/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/a3s/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/a3s/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/a3s/k/19
execute if score #pt hr matches 20 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a314_14]
execute if score #pt hr matches 21 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a314_15]
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/a3s/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/a3s/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/a3s/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/a3s/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/a3s/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/a3s/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/a3s/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/a3s/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/a3s/k/30
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/a3s/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/a3s/k/32
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/a3s/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/a3s/k/34
execute if score #pt hr matches 35 run function rlk:boss/scarlet/p/a3s/k/35
execute if score #pt hr matches 36 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a330_30]
execute if score #pt hr matches 37 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a330_31]
execute if score #pt hr matches 40 run scoreboard players set #done hr 1
