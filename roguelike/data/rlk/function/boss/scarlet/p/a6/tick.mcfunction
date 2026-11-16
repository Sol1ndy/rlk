# A6 후방 섬보: one pattern tick (#pt hr = 1..16); events in k/<t>.
execute if score #pt hr matches 5..10 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 3 at @s run function rlk:boss/scarlet/fx/snd/a6_arrive
execute if score #pt hr matches 4 run function rlk:mboss/mv/face
execute if score #pt hr matches 12 run function rlk:boss/scarlet/fx/hud/line {id:12}
execute if score #pt hr matches 16 run scoreboard players set #done hr 1
