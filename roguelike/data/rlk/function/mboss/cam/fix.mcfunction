# FN-cam (@s = a camera a module has just placed AT a viewpoint and aimed): mboss/cam/grid, and on every other placement
# OnGround false (a teleport sets it true): the flag then differs from the one last sent, which makes the server send the
# float position-sync packet instead of the byte move packet. Nothing depends on it: the rotation is on the byte grid.
function rlk:mboss/cam/grid
execute if entity @s[tag=rlk_mb_camg] run return run tag @s remove rlk_mb_camg
tag @s add rlk_mb_camg
data merge entity @s {OnGround:0b}
