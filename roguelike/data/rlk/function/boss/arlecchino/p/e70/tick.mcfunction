# E70 재가 된 만상: one pattern tick (#pt kn = 1..110); events in k/<t>.
execute if score #pt kn matches 20 at @s positioned ~ ~1 ~ run function rlk:mboss/mv/glide {t:10}
execute if score #pt kn matches 40 run function rlk:boss/arlecchino/p/e70/k/40
execute if score #pt kn matches 70 run function rlk:boss/arlecchino/p/e70/k/70
execute if score #pt kn matches 74 run function rlk:boss/arlecchino/p/e70/k/74
execute if score #pt kn matches 88 at @s positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:8}
execute if score #pt kn matches 96 run function rlk:boss/arlecchino/p/e70/k/96
execute if score #pt kn matches 110 run scoreboard players set #done kn 1
