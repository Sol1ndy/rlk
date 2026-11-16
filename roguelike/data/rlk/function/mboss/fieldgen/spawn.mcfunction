# Hook spawn (@s = arena marker at the centre, rotated north). The body stands on the centre facing south
# (the arriving player); intro/setup builds the rig in its dormant form and plays the entrance.
execute rotated 0 0 run function rlk:mboss/body
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/fieldgen/intro/setup
