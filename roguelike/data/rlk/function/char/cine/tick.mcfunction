# @s = the player, once per tick of a locked sequence, after the module wrote the clip tick into #cavT cine: shows that
# tick of the selected clip (past the length: the last frame). Without an actor it restores the avatar (stop).
execute unless entity @e[type=minecraft:marker,tag=rlk_cine_root,limit=1] run return run function rlk:char/cine/stop
function rlk:char/cine/hide
execute if score #cavF cine matches 1.. run function rlk:char/cine/face_step
execute if score #cavC cine matches 1 run return run function rlk:char/cine/c/cs0/run
execute if score #cavC cine matches 2 run return run function rlk:char/cine/c/cs1/run
execute if score #cavC cine matches 3 run return run function rlk:char/cine/c/repel/run
execute if score #cavC cine matches 4 run return run function rlk:char/cine/c/ending/run
execute if score #cavC cine matches 5 run return run function rlk:char/cine/c/coda/run
