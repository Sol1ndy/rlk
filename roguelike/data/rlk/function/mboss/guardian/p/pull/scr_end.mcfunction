# Ends the screen overlay at once (fizzle, refused pull, pause, cancel): an empty title over it, the F5
# crosshair title back (view/xhair) for a player on the seat.
scoreboard players set @a[tag=player] vBig 0
title @a[tag=player] times 0 1 2
title @a[tag=player] title ""
execute as @a[tag=player] if score #on view matches 1 if score #vmode view matches 2 if entity @e[tag=rlk_vseat,limit=1] run function rlk:view/xhair
