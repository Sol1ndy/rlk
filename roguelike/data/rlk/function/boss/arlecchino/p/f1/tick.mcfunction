# F1 붉은 피의 연회: one pattern tick (#pt kn = 1..232); events in k/<t>.
execute if score #pt kn matches 57..152 run function rlk:mboss/mv/turn {max:6}
execute if score #pt kn matches 6 at @e[tag=rlk_body,limit=1] run function rlk:boss/arlecchino/fx/p/brand_ring
execute if score #pt kn matches 22 run function rlk:boss/arlecchino/bond/force
execute if score #pt kn matches 40 positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:16}
execute if score #pt kn matches 110 run function rlk:boss/arlecchino/p/f1/k/110
execute if score #pt kn matches 159 run function rlk:boss/arlecchino/p/f1/k/159
execute if score #pt kn matches 160 run function rlk:boss/arlecchino/p/f1/k/160
execute if score #pt kn matches 166 run function rlk:boss/arlecchino/p/f1/k/166
execute if score #pt kn matches 195 run function rlk:boss/arlecchino/p/f1/k/195
execute if score #pt kn matches 196 run function rlk:boss/arlecchino/p/f1/k/196
execute if score #pt kn matches 200 at @s positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:10}
execute if score #pt kn matches 222 run function rlk:boss/arlecchino/rig/look/wings/off
execute if score #pt kn matches 232 run scoreboard players set #done kn 1
