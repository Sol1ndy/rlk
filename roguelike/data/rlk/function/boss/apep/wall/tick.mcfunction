# Any executor, every phase-2 tick: the blade clips (om/wall/tick) and each group's clock: stand 40 t, then its blocks go
# (exactly the recorded ones) and the blades dissolve (8 t, motes).
execute if entity @e[type=minecraft:item_display,tag=rlk_mb_ap_wall_blade,limit=1] run function rlk:boss/apep/om/wall/tick
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_wall] run function rlk:boss/apep/wall/group
