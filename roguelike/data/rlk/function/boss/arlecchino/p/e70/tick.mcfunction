# E70 재가 된 만상: one pattern tick (#pt kn = 1..110); events in k/<t>.
execute if score #pt kn matches 20 at @s positioned ~ ~1 ~ run function rlk:mboss/mv/glide {t:10}
execute if score #pt kn matches 40 run function rlk:boss/arlecchino/p/e70/k/40
execute if score #pt kn matches 44 at @s positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.44 0.02 1.44 0 40 force @a[tag=player]
execute if score #pt kn matches 48 at @s positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 2.16 0.02 2.16 0 40 force @a[tag=player]
execute if score #pt kn matches 52 at @s positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 2.88 0.02 2.88 0 40 force @a[tag=player]
execute if score #pt kn matches 56 at @s positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 3.6 0.02 3.6 0 40 force @a[tag=player]
execute if score #pt kn matches 60 at @s positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 4.32 0.02 4.32 0 40 force @a[tag=player]
execute if score #pt kn matches 64 at @s positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 5.04 0.02 5.04 0 40 force @a[tag=player]
execute if score #pt kn matches 68 at @s positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 5.76 0.02 5.76 0 40 force @a[tag=player]
execute if score #pt kn matches 70 run function rlk:boss/arlecchino/p/e70/k/70
execute if score #pt kn matches 74 run function rlk:boss/arlecchino/p/e70/k/74
execute if score #pt kn matches 88 at @s positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:8}
execute if score #pt kn matches 96 run function rlk:boss/arlecchino/p/e70/k/96
execute if score #pt kn matches 110 run scoreboard players set #done kn 1
