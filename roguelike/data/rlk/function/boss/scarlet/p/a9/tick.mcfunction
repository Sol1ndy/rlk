# A9 황광 원참: one pattern tick (#pt hr = 1..40); events in k/<t>.
execute if score #pt hr matches 1..20 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 29..39 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 4 at @s rotated as @s rotated ~ 0 positioned ~ ~1.0 ~ run function rlk:boss/scarlet/fx/p/qi_ring {r:35,c:1}
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/a9/k/8
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/a9/k/17
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/a9/k/21
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/a9/k/24
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/a9/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/a9/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/a9/k/28
execute if score #pt hr matches 29 run kill @e[type=minecraft:marker,tag=rlk_hr_a9s]
execute if score #pt hr matches 40 run scoreboard players set #done hr 1
