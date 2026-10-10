scoreboard players add #rl tmp 1
execute if score #rl tmp matches 48.. run return 0
execute positioned ^ ^ ^0.5 if block ~ ~ ~ #rlk:cm_pass run function rlk:cm/ray
