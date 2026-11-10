# A2 역습 일섬: one pattern tick (#pt hr = 1..22); events in k/<t>.
execute if score #pt hr matches 1..5 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 13..14 if score #pp hr matches 1 run function rlk:boss/scarlet/core/pp
execute if score #pt hr matches 13..21 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 17..21 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 4 at @s run function rlk:boss/scarlet/fx/snd/a2_draw
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/a2/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/rig/look/blade/lilac
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/a2/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/a2/k/12
execute if score #pt hr matches 16 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 22 run scoreboard players set #done hr 1
