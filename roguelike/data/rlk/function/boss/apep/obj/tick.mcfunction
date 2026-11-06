# Any executor, once per module tick (E, phases 1-3, D; frozen while paused): every org object's clip step
# (om/<object>/tick; RORG-3, AP-I2 requests RP1-2 / RP3-4 / RREV-1), each object only while its displays
# exist. Before the stage and the main slot: a clip played in tick T shows its key 0 at T + 1.
execute if entity @e[type=minecraft:item_display,tag=rlk_mb_ap_heart_bulb,limit=1] run function rlk:boss/apep/om/heart/tick
execute if entity @e[type=minecraft:item_display,tag=rlk_mb_ap_dome_shell,limit=1] run function rlk:boss/apep/om/dome/tick
execute if entity @e[type=minecraft:item_display,tag=rlk_mb_ap_stalk_low,limit=1] run function rlk:boss/apep/om/stalk/tick
execute if entity @e[type=minecraft:item_display,tag=rlk_mb_ap_wall_blade,limit=1] run function rlk:boss/apep/om/wall/tick
