# burrow3 #azPT 418
function rlk:mboss/azhdaha/px/normal
function rlk:mboss/azhdaha/svc/floor_0
scoreboard players set #azBur mb 0
scoreboard players set #azSkipF mb 1
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] if score @s mhpC matches ..1 run function rlk:mboss/azhdaha/p/burrow3/last
