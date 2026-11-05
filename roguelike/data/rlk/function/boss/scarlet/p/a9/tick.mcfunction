# A9 황광 원참: one pattern tick (#pt hr = 1..64); events in k/<t>.
execute if score #pt hr matches 1..20 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 40..63 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 4 at @s rotated as @s rotated ~ 0 positioned ~ ~0.8 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 1.4 0.05 1.4 0 24 force @a[tag=player]
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/a9/k/8
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/a9/k/17
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/a9/k/21
execute if score #pt hr matches 24 at @s run playsound minecraft:entity.illusioner.cast_spell hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/a9/dash
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/a9/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/a9/k/28
execute if score #pt hr matches 29 run kill @e[type=minecraft:marker,tag=rlk_hr_a9s]
execute if score #pt hr matches 64 run scoreboard players set #done hr 1
