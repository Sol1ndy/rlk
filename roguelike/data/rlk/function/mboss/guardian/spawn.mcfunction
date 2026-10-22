# Hook spawn (@s = arena marker at the centre, rotated north). The body stands on the centre star facing
# south (the arriving player); the rig spawns hidden and the entrance clip brings it in (intro_tick).
execute rotated 0 0 run function rlk:mboss/body
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/guardian/intro/setup
