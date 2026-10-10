# Separate cinematic camera; never use the camera position for boss target/damage.
execute unless entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=80..173},limit=1] run return run function rlk:boss/raiden/camera/end
execute unless entity @e[tag=rlk_rd_cam_anchor,limit=1] run return run function rlk:boss/raiden/camera/end
execute unless entity @e[tag=rlk_av,limit=1] run return run function rlk:boss/raiden/camera/end
execute if score @s dead matches 1 run return run function rlk:boss/raiden/camera/end
execute if score @s rnDie matches 1.. run return run function rlk:boss/raiden/camera/end
execute if score @s pkMode matches 1.. run return run function rlk:boss/raiden/camera/end
scoreboard players set @s dashMoveT 0
scoreboard players set @s stepT 0
scoreboard players set @s rcU 0
scoreboard players set @s rcT 0
scoreboard players set @s pmAtkPending 0
kill @e[tag=rlk_plkb]
execute at @e[tag=rlk_rd_cam_anchor,limit=1] rotated as @e[tag=rlk_rd_cam_anchor,limit=1] run tp @e[tag=rlk_av,limit=1] ~ ~ ~ ~ ~
data merge entity @e[tag=rlk_av,limit=1] {Motion:[0d,0d,0d]}
# Eye at (0,204,13), aimed above the orb toward the rift and sword.
tp @e[tag=rlk_camv,limit=1] 0 202.98 13 180 -10
rotate @s 180 -10
execute if predicate rlk:in_sneak run tp @s 0 202.73 13 180 -10
execute unless predicate rlk:in_sneak run ride @s mount @e[tag=rlk_camv,limit=1]
function rlk:view/hand_wrap
