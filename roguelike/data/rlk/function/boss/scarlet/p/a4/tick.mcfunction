# A4 월하 낙참 · 공중 원륜: one pattern tick (#pt hr = 1..60); events in k/<t>.
execute if score #pt hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 6..11 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 21..26 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/a4/k/2
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/a4/k/7
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/a4/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/a4/k/13
execute if score #pt hr matches 16 positioned as @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run function rlk:mboss/mv/glide {t:4}
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/a4/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/a4/k/20
execute if score #pt hr matches 25 at @s rotated as @s rotated ~ 0 positioned ^ ^0.95 ^1.5 run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.6 0.1 0.6 0 10 force @a[tag=player]
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/a4/k/28
execute if score #pt hr matches 30 at @s run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.5 1.5 0.17
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/a4/k/33
execute if score #pt hr matches 34 at @s positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:4}
execute if score #pt hr matches 60 run scoreboard players set #done hr 1
