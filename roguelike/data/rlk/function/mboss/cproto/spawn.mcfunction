# Hook spawn (@s = the arena marker at the centre of cp_test): the chapter body at POINTS spawn, facing south.
execute positioned 540 201 8 rotated 0 0 run function rlk:mboss/cb/body
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cproto/reload
scoreboard players set #cpPh mb 1
