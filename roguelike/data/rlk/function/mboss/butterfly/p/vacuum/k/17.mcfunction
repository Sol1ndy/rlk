# vacuum clock 17
scoreboard players set #pjKB mb 3
scoreboard players set #pjShape mb 1
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p4b,limit=1] at @s run function rlk:mboss/pj/launch {spd:7,life:60,dmg:120,hr:15}
playsound minecraft:entity.breeze.wind_burst hostile @a[tag=player] ~ ~ ~ 0.8 1 0.27
playsound minecraft:item.trident.riptide_2 hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
