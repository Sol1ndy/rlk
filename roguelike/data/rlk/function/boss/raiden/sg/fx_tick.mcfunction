# sg/tick: the switch after-effect runs until the next transformation (stuns included), not during 5 or 7.
scoreboard players add @s rdSgFxT 1
execute if score @s rdSgFx matches 2 if score @s rdSgFxT matches 8 as @e[tag=rlk_rd_sgfx] at @s run function rlk:boss/raiden/fx/star
execute if score @s rdSgFx matches 2 if score @s rdSgFxT matches 14 run kill @e[tag=rlk_rd_sgfx]
execute if score @s rdPat matches 5 run return 0
execute if score @s rdPat matches 7 run return 0
execute if score @s rdSgFx matches 1 if score @s rdSgFxT matches 80.. run function rlk:boss/raiden/sg/fx6
execute if score @s rdSgFx matches 2 if score @s rdSgFxT matches 60.. run function rlk:boss/raiden/sg/fx6b
