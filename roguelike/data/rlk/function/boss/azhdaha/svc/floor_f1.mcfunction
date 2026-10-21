# #mbFloor = ceil(mhpM x 2 / 3) (the end of phase 1).
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run scoreboard players operation #mbFloor mb = @s mhpM
scoreboard players operation #mbFloor mb *= #c2 mb
scoreboard players add #mbFloor mb 2
scoreboard players set #azX mb 3
scoreboard players operation #mbFloor mb /= #azX mb
