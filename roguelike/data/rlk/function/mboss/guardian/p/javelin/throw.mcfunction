# @s = body: the visual spear (rig prop/spear, tip turned forward) at L flies down the lane at 5 b/t,
# harmless (dmg 0, K23: the lane is the damage), stops at the wall and is kept (pj_end) until the return.
kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p2s]
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] run function rlk:mboss/guardian/rig/prop/spear
tag @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] add rlk_mb_gd_p2
tag @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] add rlk_mb_gd_p2s
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] {transformation:{translation:[0f,0f,0f],left_rotation:[0.7071f,0f,0f,0.7071f],scale:[2.2f,2.2f,2.2f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] mbId 2
# flight time = the lane length at 5 b/t (the wall check stays on)
execute if score #gp2Len mb matches 1..50 as @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] at @s run function rlk:mboss/pj/launch {spd:50,life:1,dmg:0,hr:5}
execute if score #gp2Len mb matches 51..100 as @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] at @s run function rlk:mboss/pj/launch {spd:50,life:2,dmg:0,hr:5}
execute if score #gp2Len mb matches 101..150 as @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] at @s run function rlk:mboss/pj/launch {spd:50,life:3,dmg:0,hr:5}
execute if score #gp2Len mb matches 151..200 as @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] at @s run function rlk:mboss/pj/launch {spd:50,life:4,dmg:0,hr:5}
execute if score #gp2Len mb matches 201..250 as @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] at @s run function rlk:mboss/pj/launch {spd:50,life:5,dmg:0,hr:5}
execute if score #gp2Len mb matches 251..300 as @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] at @s run function rlk:mboss/pj/launch {spd:50,life:6,dmg:0,hr:5}
execute if score #gp2Len mb matches 301..350 as @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] at @s run function rlk:mboss/pj/launch {spd:50,life:7,dmg:0,hr:5}
execute if score #gp2Len mb matches 351..400 as @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] at @s run function rlk:mboss/pj/launch {spd:50,life:8,dmg:0,hr:5}
execute if score #gp2Len mb matches 401..450 as @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] at @s run function rlk:mboss/pj/launch {spd:50,life:9,dmg:0,hr:5}
