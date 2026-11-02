# The break window closes (its end, a cancel, the break; @s any).
execute unless score #win kn matches 1 run return 0
tag @e[tag=rlk_kn_win] remove rlk_kn_win
scoreboard players set #win kn 0
