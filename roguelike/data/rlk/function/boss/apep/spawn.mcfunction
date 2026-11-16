# Hook spawn (@s = the arena marker at the centre): the chapter body (cb/body: no miniboss, rlk_mb_big, the torso
# click shield {'w': 2.6, 'h': 3.6}) at POINTS spawn facing south (yaw 0) toward the arrival; intro/setup.
execute positioned 440 201 8 rotated 0 0 run function rlk:mboss/cb/body
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:boss/apep/intro/setup
