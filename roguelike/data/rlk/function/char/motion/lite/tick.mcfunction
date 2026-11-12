# @s = player, once per game tick while the stand-in rig plays (player/def/beat/post, after the avatar moved).
execute unless entity @e[tag=rlk_av,limit=1] run return run function rlk:char/motion/lite/stop
execute unless entity @e[tag=rlk_pl,limit=1] run return run function rlk:char/motion/lite/stop
execute if score @s dead matches 1 run return run function rlk:char/motion/lite/stop
execute if score @s pkMode matches 1.. run return run function rlk:char/motion/lite/stop
scoreboard players add @s plTick 1
execute if score @s plTick > @s plLen run return run function rlk:char/motion/lite/stop
function rlk:char/motion/lite/hide
execute at @e[tag=rlk_av,limit=1] rotated as @e[tag=rlk_pl_basis,limit=1] rotated ~ 0 run tp @e[tag=rlk_pl] ~ ~ ~ ~ 0
execute if score @s plClip matches 1 run return run function rlk:char/motion/lite/p/pose
execute if score @s plClip matches 3 run return run function rlk:char/motion/lite/f/pose
function rlk:char/motion/lite/d/pose
