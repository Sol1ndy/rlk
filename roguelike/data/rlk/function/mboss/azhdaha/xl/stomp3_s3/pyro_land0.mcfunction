# Landing of lump 0 (t91): its fireball + fire field, then its prop and target go; lump 1 lands 1 t later (I2 perf stagger).
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xltt0,limit=1] at @s run function rlk:mboss/azhdaha/xl/u/lump_land
kill @e[tag=rlk_mb_az_xltp0]
kill @e[tag=rlk_mb_az_xltt0]
scoreboard players set #azAftF mb 20
scoreboard players set #azAftD mb 1
function rlk:mboss/azhdaha/aft/new
