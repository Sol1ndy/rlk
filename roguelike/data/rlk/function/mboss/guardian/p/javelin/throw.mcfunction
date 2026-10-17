# @s = body: the visual spear (rig prop, tip turned forward) flies 3 b/t for 9 t and returns (pj, harmless).
execute at @s rotated as @s rotated ~ 0 positioned ^-0.5 ^1.6 ^0.8 run function rlk:mboss/guardian/rig/prop/spear
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] {transformation:{left_rotation:[0.7071f,0f,0f,0.7071f]}}
tag @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] add rlk_mb_gd_p2
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] mbId 2
scoreboard players set #pjRet mb 1
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] at @s run function rlk:mboss/pj/launch {spd:30,life:9,dmg:0,hr:6}
playsound minecraft:item.trident.riptide_2 hostile @a[tag=player] ~ ~ ~ 0.6 1 0.3
