# Hook spawn (@s = the arena marker at the centre of fl_ruins). The body (mboss/body: husk scale 1.4, click
# shield 1.2 x 2.9, no proxies) stands at the centre facing south (yaw 0), toward the player arriving at the
# south edge; rlk_mb_inv until the intro ends.
execute rotated 0 0 run function rlk:mboss/body
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/arlecchino/core/setup
