# A4 월하 낙참 · 공중 원륜: one pattern tick (#pt hr = 1..46); events in k/<t>.
execute if score #pt hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 6..11 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 21..26 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 35..45 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 39..45 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/a4/k/2
execute if score #pt hr matches 4 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:15}
execute if score #pt hr matches 6 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:15}
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/a4/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/a4/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/a4/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/a4/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/a4/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/a4/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/a4/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/a4/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/a4/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/a4/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/a4/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/a4/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/a4/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/a4/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/a4/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/a4/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/a4/k/24
execute if score #pt hr matches 25 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a420_19]
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/a4/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/a4/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/a4/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/a4/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/a4/k/30
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/a4/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/a4/k/32
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/a4/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/a4/k/34
execute if score #pt hr matches 35 run function rlk:boss/scarlet/p/a4/k/35
execute if score #pt hr matches 36 run function rlk:boss/scarlet/p/a4/k/36
execute if score #pt hr matches 37 run function rlk:boss/scarlet/p/a4/k/37
execute if score #pt hr matches 38 run function rlk:boss/scarlet/p/a4/k/38
execute if score #pt hr matches 39 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a434_33]
execute if score #pt hr matches 40 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a434_34]
execute if score #pt hr matches 46 run scoreboard players set #done hr 1
