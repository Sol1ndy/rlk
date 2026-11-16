# Hook spawn (@s = the arena marker at the centre of tk_lift). The body (mboss/body: husk scale 1.25, click shield,
# miniboss economy) stands at the centre facing south (yaw 0), toward the player arriving at the south edge.
execute rotated 0 0 run function rlk:mboss/body
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/tachy/core/setup
