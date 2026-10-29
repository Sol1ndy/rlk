# B1 날개 가리기 2연격: one pattern tick (#pt tk = 1..50); events in k/<t>.
execute if score #pt tk matches 1..20 at @s unless entity @e[tag=rlk_body,distance=..3,limit=1] run function rlk:mboss/mv/toward {d:0.12}
execute if score #pt tk matches 1..16 run function rlk:mboss/mv/turn {max:6}
execute if score #pt tk matches 26..31 at @s unless entity @e[tag=rlk_body,distance=..2,limit=1] run function rlk:mboss/mv/step {d:0.17}
execute if score #pt tk matches 25..32 run function rlk:mboss/mv/turn {max:6}
execute if score #pt tk matches 22 at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run function rlk:boss/tachy/fx/p/wing_flare
execute if score #pt tk matches 23 run function rlk:boss/tachy/p/b1/k/23
execute if score #pt tk matches 24 run function rlk:boss/tachy/p/b1/k/24
execute if score #pt tk matches 39 run function rlk:boss/tachy/p/b1/k/39
execute if score #pt tk matches 40 run function rlk:boss/tachy/p/b1/k/40
execute if score #pt tk matches 50 run scoreboard players set #done tk 1
