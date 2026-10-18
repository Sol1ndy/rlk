# [c_redraw] After a pause (the core cleared every kit decal): each live quiet hazard of this pattern (hz_vis
# 61..62) that has not struck yet gets its decal again with the ticks it has left (review FX-1).
execute as @e[type=minecraft:marker,tag=rlk_mb_hzq,scores={mbHzV=61..62}] if score @s mbHzT < @s mbHzW at @s run function rlk:mboss/fieldgen/p/rock/redraw1
