# Hook spawn (@s = the arena marker at the centre = POINTS spawn, rotated 180). The body (cb/body: no miniboss,
# rlk_mb_big, rlk_mb_noshield; husk scale 0.1) faces south (yaw 0) toward the arrival; intro/setup builds the rest.
execute rotated 0 0 run function rlk:mboss/cb/body
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/azhdaha/intro/setup
