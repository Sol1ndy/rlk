# #mbFloor = ceil(mhpM x 1 / 100) (the P1 pool's 1 %, plan 7.2; framework clamp, cm.md 7.2).
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run scoreboard players operation #mbFloor mb = @s mhpM
scoreboard players add #mbFloor mb 99
scoreboard players operation #mbFloor mb /= #c100 mb
