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
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/a3s/k/7
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/a3s/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/a3s/k/14
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/a3s/k/23
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/a3s/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/a3s/k/30
execute if score #pt hr matches 34 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 40 run scoreboard players set #done hr 1
