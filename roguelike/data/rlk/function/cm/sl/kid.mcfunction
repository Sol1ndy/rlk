scoreboard players set #c2ok tmp 0
execute positioned ^0 ^ ^0.5 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^0 ^ ^0.5 run function rlk:cm/spawn/ss
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/ss
execute as @e[tag=rlk_newmob,tag=rlk_cm_ss] run function rlk:cm/sl/kid_go
