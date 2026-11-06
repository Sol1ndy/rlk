# Hook spawn (@s = the arena marker of cp_test): the body (mboss/body: miniboss, the registry's scale / shield / RES) at
# the arena's spawn point, facing the arrival.
execute positioned 540 201 8 rotated 0 0 run function rlk:mboss/body
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/spproto/reload
