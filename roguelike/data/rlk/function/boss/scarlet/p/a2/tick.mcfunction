# A2 역습 일섬: one pattern tick (#pt hr = 1..30); events in k/<t>.
execute if score #pt hr matches 1..5 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 4 at @s run function rlk:boss/scarlet/fx/snd/a2_draw
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/a2/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/a2/k/12
execute if score #pt hr matches 30 run scoreboard players set #done hr 1
