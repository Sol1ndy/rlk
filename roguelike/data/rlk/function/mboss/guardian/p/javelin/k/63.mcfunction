# javelin clip tick 63
kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p2s]
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"star",pos:"^-0.462 ^6.587 ^0.058",rot:"~ ~",bb:"center",roll:0,spin:45,s0:0.2,s1:1,move:"0f,0f,0f",life:5,fade:2}
execute at @s rotated as @s rotated ~ 0 positioned ^-0.3 ^3.35 ^0.22 run particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:1} ~ ~ ~ 0.25 0.25 0.25 0 8 force @a[tag=player]
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.5 0.6 0.3
playsound minecraft:item.armor.equip_netherite hostile @a[tag=player] ~ ~ ~ 0.4 1.3 0.3
