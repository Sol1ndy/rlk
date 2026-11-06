# Lump 1 leaves 1 t after lump 0 (FIX STATE-2: the launch spread over three ticks).
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xlst1,limit=1] at @s run function rlk:boss/azhdaha/xl/u/lump_hz1
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_xlsp1,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_az_xlst1,limit=1] run function rlk:boss/azhdaha/xl/u/lump_fly1
playsound minecraft:entity.blaze.shoot hostile @a[tag=player] ~ ~ ~ 0.6 0.7 0.2
scoreboard players set #azAftF mb 18
scoreboard players set #azAftD mb 1
function rlk:boss/azhdaha/aft/new
