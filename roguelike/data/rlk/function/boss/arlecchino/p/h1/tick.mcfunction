# H1 연옥 그림자 분신: one pattern tick (#pt kn = 1..156); events in k/<t>.
execute if score #pt kn matches 1..20 run function rlk:mboss/mv/turn {max:20}
execute if score #pt kn matches 35..96 run function rlk:mboss/mv/turn {max:10}
execute if score #pt kn matches 97..102 run function rlk:mboss/mv/turn {max:20}
execute if score #pt kn matches 105..109 run function rlk:mboss/mv/turn {max:14}
execute if score #pt kn matches 105..110 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt kn matches 10 run function rlk:boss/arlecchino/p/h1/k/10
execute if score #pt kn matches 20 run function rlk:boss/arlecchino/p/h1/k/20
execute if score #pt kn matches 21 as @e[type=minecraft:item_display,tag=rlk_kn_clone,tag=rlk_kn_p_h1] at @s run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.3 0.6 0.3 0 8 force @a[tag=player]
execute if score #pt kn matches 23 as @e[type=minecraft:item_display,tag=rlk_kn_clone,tag=rlk_kn_p_h1] at @s run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.3 0.6 0.3 0 8 force @a[tag=player]
execute if score #pt kn matches 25 as @e[type=minecraft:item_display,tag=rlk_kn_clone,tag=rlk_kn_p_h1] at @s run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.3 0.6 0.3 0 8 force @a[tag=player]
execute if score #pt kn matches 27 as @e[type=minecraft:item_display,tag=rlk_kn_clone,tag=rlk_kn_p_h1] at @s run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.3 0.6 0.3 0 8 force @a[tag=player]
execute if score #pt kn matches 29 as @e[type=minecraft:item_display,tag=rlk_kn_clone,tag=rlk_kn_p_h1] at @s run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.3 0.6 0.3 0 8 force @a[tag=player]
execute if score #pt kn matches 31 as @e[type=minecraft:item_display,tag=rlk_kn_clone,tag=rlk_kn_p_h1] at @s run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.3 0.6 0.3 0 8 force @a[tag=player]
execute if score #pt kn matches 33 run function rlk:boss/arlecchino/p/h1/k/33
execute if score #pt kn matches 34 run function rlk:boss/arlecchino/p/h1/k/34
execute if score #pt kn matches 36 run kill @e[type=minecraft:item_display,tag=rlk_kn_clone,tag=rlk_kn_p_h1]
execute if score #pt kn matches 90 run function rlk:boss/arlecchino/p/h1/k/90
execute if score #pt kn matches 96 run function rlk:boss/arlecchino/p/h1/k/96
execute if score #pt kn matches 103 run function rlk:boss/arlecchino/p/h1/k/103
execute if score #pt kn matches 104 run function rlk:boss/arlecchino/p/h1/k/104
execute if score #pt kn matches 111 run function rlk:boss/arlecchino/p/h1/k/111
execute if score #pt kn matches 112 run function rlk:boss/arlecchino/p/h1/k/112
execute if score #pt kn matches 140 run function rlk:boss/arlecchino/rig_stub/look/wings/off
execute if score #pt kn matches 156 run scoreboard players set #done kn 1
