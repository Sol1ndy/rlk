# A3 오연 반월: one pattern tick (#pt hr = 1..96); events in k/<t>.
execute if score #pt hr matches 1..13 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 1..7 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 15..23 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 16..25 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 26..29 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.375}
execute if score #pt hr matches 31..38 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 32..43 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 46..50 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 47..55 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 58..62 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 59..67 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 1 if score #ph hr matches 7 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:42}
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/a3/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/a3/k/14
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/a3/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/a3/k/30
execute if score #pt hr matches 44 run function rlk:boss/scarlet/p/a3/k/44
execute if score #pt hr matches 45 run function rlk:boss/scarlet/p/a3/k/45
execute if score #pt hr matches 56 run function rlk:boss/scarlet/p/a3/k/56
execute if score #pt hr matches 57 run function rlk:boss/scarlet/p/a3/k/57
execute if score #pt hr matches 68 run function rlk:boss/scarlet/p/a3/k/68
execute if score #pt hr matches 69 run function rlk:boss/scarlet/p/a3/k/69
execute if score #pt hr matches 96 run scoreboard players set #done hr 1
