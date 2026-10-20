# jump #azPT 12
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p2l,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p2l,limit=1] run function rlk:mboss/azhdaha/p/jump/l/12
scoreboard players set #azNoPush mb 1
function rlk:mboss/mv/turn {max:6}
