# B1 붉은 달의 낫: one pattern tick (#pt kn = 1..60); events in k/<t>.
execute if score #pt kn matches 1..20 run function rlk:mboss/mv/turn {max:10}
execute if score #pt kn matches 10 run function rlk:boss/arlecchino/p/b1/k/10
execute if score #pt kn matches 28 run function rlk:boss/arlecchino/p/b1/k/28
execute if score #pt kn matches 29 as @e[type=minecraft:item_display,tag=rlk_kn_p_b1,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #pt kn matches 31 as @e[type=minecraft:item_display,tag=rlk_kn_p_b1,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #pt kn matches 33 as @e[type=minecraft:item_display,tag=rlk_kn_p_b1,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #pt kn matches 35 as @e[type=minecraft:item_display,tag=rlk_kn_p_b1,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #pt kn matches 37 as @e[type=minecraft:item_display,tag=rlk_kn_p_b1,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #pt kn matches 39 as @e[type=minecraft:item_display,tag=rlk_kn_p_b1,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #pt kn matches 41 as @e[type=minecraft:item_display,tag=rlk_kn_p_b1,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #pt kn matches 43 as @e[type=minecraft:item_display,tag=rlk_kn_p_b1,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #pt kn matches 45 as @e[type=minecraft:item_display,tag=rlk_kn_p_b1,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #pt kn matches 47 as @e[type=minecraft:item_display,tag=rlk_kn_p_b1,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #pt kn matches 49 as @e[type=minecraft:item_display,tag=rlk_kn_p_b1,tag=rlk_kn_wheel] at @s run particle minecraft:flame ~ ~ ~ 0.5 0.6 0.5 0.02 6 force @a[tag=player]
execute if score #pt kn matches 51 run function rlk:boss/arlecchino/p/b1/k/51
execute if score #pt kn matches 52 run function rlk:boss/arlecchino/rig_stub/look/weapon_r/hand
execute if score #pt kn matches 60 run scoreboard players set #done kn 1
