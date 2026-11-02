# G1 죽음의 칼날: one pattern tick (#pt kn = 1..140); events in k/<t>.
execute if score #pt kn matches 1..5 run function rlk:mboss/mv/turn {max:12}
execute if score #pt kn matches 6 run function rlk:boss/arlecchino/p/g1/k/6
execute if score #pt kn matches 10 run function rlk:boss/arlecchino/p/g1/strips
execute if score #pt kn matches 14 run function rlk:boss/arlecchino/p/g1/strips
execute if score #pt kn matches 18 run function rlk:boss/arlecchino/p/g1/strips
execute if score #pt kn matches 22 run function rlk:boss/arlecchino/p/g1/strips
execute if score #pt kn matches 26 run function rlk:boss/arlecchino/p/g1/strips
execute if score #pt kn matches 30 run function rlk:boss/arlecchino/p/g1/strips
execute if score #pt kn matches 33 run function rlk:boss/arlecchino/p/g1/k/33
execute if score #pt kn matches 34 run function rlk:boss/arlecchino/p/g1/k/34
execute if score #pt kn matches 40 run function rlk:boss/arlecchino/p/g1/k/40
execute if score #pt kn matches 44 run function rlk:boss/arlecchino/p/g1/strips
execute if score #pt kn matches 48 run function rlk:boss/arlecchino/p/g1/strips
execute if score #pt kn matches 52 run function rlk:boss/arlecchino/p/g1/strips
execute if score #pt kn matches 56 run function rlk:boss/arlecchino/p/g1/strips
execute if score #pt kn matches 60 run function rlk:boss/arlecchino/p/g1/strips
execute if score #pt kn matches 61 run function rlk:boss/arlecchino/p/g1/k/61
execute if score #pt kn matches 62 run function rlk:boss/arlecchino/p/g1/k/62
execute if score #pt kn matches 66 run kill @e[type=minecraft:item_display,tag=rlk_kn_blade,tag=rlk_kn_p_g1]
execute if score #pt kn matches 70 run function rlk:boss/arlecchino/p/g1/k/70
execute if score #pt kn matches 74 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 2.54 0.02 2.54 0 90 force @a[tag=player]
execute if score #pt kn matches 78 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 3.81 0.02 3.81 0 90 force @a[tag=player]
execute if score #pt kn matches 82 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 5.08 0.02 5.08 0 90 force @a[tag=player]
execute if score #pt kn matches 86 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 6.35 0.02 6.35 0 90 force @a[tag=player]
execute if score #pt kn matches 90 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 7.62 0.02 7.62 0 90 force @a[tag=player]
execute if score #pt kn matches 94 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 8.89 0.02 8.89 0 90 force @a[tag=player]
execute if score #pt kn matches 98 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 10.16 0.02 10.16 0 90 force @a[tag=player]
execute if score #pt kn matches 102 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.44 0.02 11.44 0 90 force @a[tag=player]
execute if score #pt kn matches 103 run function rlk:boss/arlecchino/p/g1/k/103
execute if score #pt kn matches 104 run function rlk:boss/arlecchino/p/g1/k/104
execute if score #pt kn matches 112 run kill @e[type=minecraft:item_display,tag=rlk_kn_blade,tag=rlk_kn_p_g1]
execute if score #pt kn matches 140 run scoreboard players set #done kn 1
