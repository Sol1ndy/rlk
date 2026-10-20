# icicle #azBgTT 200
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p43s,limit=1] run function rlk:mboss/azhdaha/fx/p/ice_sphere
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p43s,limit=1] run particle minecraft:snowflake ~ ~ ~ 0.8 0.8 0.8 0.05 20 force @a[tag=player]
kill @e[tag=rlk_mb_az_p43]
function rlk:mboss/azhdaha/bg/end_t
