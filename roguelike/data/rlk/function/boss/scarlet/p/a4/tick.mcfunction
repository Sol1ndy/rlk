# A4 월하 낙참 · 공중 원륜: one pattern tick (#pt hr = 1..46); events in k/<t>.
execute if score #pt hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 6..11 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 21..26 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 35..45 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/a4/k/2
execute if score #pt hr matches 4 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:15}
execute if score #pt hr matches 6 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:15}
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/a4/k/7
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/a4/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/a4/k/13
execute if score #pt hr matches 16 positioned as @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run function rlk:mboss/mv/glide {t:4}
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/a4/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/a4/k/20
execute if score #pt hr matches 25 at @s rotated as @s rotated ~ 0 positioned ^ ^1.2 ^1.5 run function rlk:boss/scarlet/fx/p/qi_line {len:30}
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/a4/k/28
execute if score #pt hr matches 30 at @s run function rlk:boss/scarlet/fx/snd/a5_spin
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/a4/k/33
execute if score #pt hr matches 34 at @s positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:4}
execute if score #pt hr matches 46 run scoreboard players set #done hr 1
