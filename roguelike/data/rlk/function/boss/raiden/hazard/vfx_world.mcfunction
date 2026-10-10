# Call after hazard updates and from pause: removes canceled/orphan effects immediately.
execute as @e[type=minecraft:item_display,tag=rlk_rd_hvfx] run function rlk:boss/raiden/hazard/vfx_tick
