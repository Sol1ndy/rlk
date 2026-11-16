# Once per tick while walls stand: every blade runs its clip.
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_wall_blade,scores={apOI=0..}] run function rlk:boss/apep/om/wall/d/wall_blade/tick
