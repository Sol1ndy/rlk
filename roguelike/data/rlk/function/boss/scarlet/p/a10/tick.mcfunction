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
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/a10/k/14
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/a10/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/a10/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/a10/k/22
execute if score #pt hr matches 26 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 32 run scoreboard players set #done hr 1
