# NB 낙월 사선: one pattern tick (#pt hr = 1..52); events in k/<t>.
execute if score #pt hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 8..12 run function rlk:mboss/mv/turn {max:20}
execute if score #pt hr matches 21..22 run function rlk:mboss/mv/turn {max:20}
execute if score #pt hr matches 31..32 run function rlk:mboss/mv/turn {max:20}
execute if score #pt hr matches 41..51 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 47..51 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/nb/k/2
execute if score #pt hr matches 5 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:15}
execute if score #pt hr matches 8 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:15}
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/nb/k/13
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/nb/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/nb/k/20
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/nb/k/23
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/nb/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/nb/k/30
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/nb/k/33
execute if score #pt hr matches 39 run function rlk:boss/scarlet/p/nb/k/39
execute if score #pt hr matches 40 run function rlk:boss/scarlet/p/nb/k/40
execute if score #pt hr matches 46 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 52 run scoreboard players set #done hr 1
