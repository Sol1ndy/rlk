# Lump 2 leaves 2 t after lump 0 (FIX STATE-2: the launch spread over three ticks).
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xlwt2,limit=1] at @s run function rlk:mboss/azhdaha/xl/u/lump_hz2
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_xlwp2,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_az_xlwt2,limit=1] run function rlk:mboss/azhdaha/xl/u/lump_fly2
playsound minecraft:entity.blaze.shoot hostile @a[tag=player] ~ ~ ~ 0.6 0.7 0.2
scoreboard players set #azAftF mb 12
scoreboard players set #azAftD mb 12
function rlk:mboss/azhdaha/aft/new
scoreboard players set #azAftF mb 13
scoreboard players set #azAftD mb 24
function rlk:mboss/azhdaha/aft/new
