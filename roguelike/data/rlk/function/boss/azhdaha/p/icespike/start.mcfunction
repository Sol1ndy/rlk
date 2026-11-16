# 45 천동만상 – 얼음 가시 (Cryo, replaces P4 in phase 3): the back glows t0-22; 3 dark spikes up at t14; the star
# fields at t26 (keep: star seal + rune, plan Change note 1) with their bursts at [68, 74, 80] (the
# spike lands 1 t before), r 4.0, 1.0 Cryo + stack, own group each; hail in F1 / F2 for 100 t.
function rlk:boss/azhdaha/rig/glow/gold_on
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^4 ^-0.2 run particle minecraft:snowflake ~ ~ ~ 1.2 0.6 1.2 0.02 10 force @a[tag=player]
execute unless entity @e[type=minecraft:marker,tag=rlk_mb_az_p45h,limit=1] run scoreboard players set #aq45H mb 0
