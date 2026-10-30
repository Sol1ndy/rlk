# jump #azPT 21
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p2l,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p2l,limit=1] run function rlk:boss/azhdaha/p/jump/l/21
scoreboard players set #azNoPush mb 1
scoreboard players set #azLeap mb 0
function rlk:boss/azhdaha/px/normal
