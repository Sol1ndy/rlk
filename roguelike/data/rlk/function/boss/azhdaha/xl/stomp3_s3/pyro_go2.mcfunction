# Lump 2 leaves 2 t after lump 0 (FIX STATE-2: the launch spread over three ticks).
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xltt2,limit=1] at @s run function rlk:boss/azhdaha/xl/u/lump_hz2
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_xltp2,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_az_xltt2,limit=1] run function rlk:boss/azhdaha/xl/u/lump_fly2
playsound minecraft:entity.blaze.shoot hostile @a[tag=player] ~ ~ ~ 0.6 0.7 0.2
scoreboard players set #azAftF mb 26
scoreboard players set #azAftD mb 12
function rlk:boss/azhdaha/aft/new
scoreboard players set #azAftF mb 27
scoreboard players set #azAftD mb 24
function rlk:boss/azhdaha/aft/new
