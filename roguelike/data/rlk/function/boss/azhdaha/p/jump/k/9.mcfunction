# jump #azPT 9
scoreboard players set #azNoPush mb 1
function rlk:mboss/mv/turn {max:6}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p2l,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/azhdaha/p/jump/ax_land
