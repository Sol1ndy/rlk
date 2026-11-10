# FN-cam: the camera stands gone (a module's sequence end / cancel / cleanup). A player still spectating one falls back
# to their own view by the game itself; rlk:tick's release (the request has stopped) puts them back in their body.
kill @e[type=minecraft:armor_stand,tag=rlk_mb_cam]
