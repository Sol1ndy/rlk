# Landing of lump 1 (t92): its fireball + fire field, then its prop and target go; lump 2 lands 1 t later (I2 perf stagger).
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xltt1,limit=1] at @s run function rlk:mboss/azhdaha/xl/u/lump_land
kill @e[tag=rlk_mb_az_xltp1]
kill @e[tag=rlk_mb_az_xltt1]
scoreboard players set #azAftF mb 29
scoreboard players set #azAftD mb 1
function rlk:mboss/azhdaha/aft/new
