# @s = crescent 1 of swing 1, at it: its flame tail (p/barrage/tail), then its helper follows it.
tag @s add rlk_mb_bf_p12qy
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12q11] add rlk_mb_bf_p12qx
function rlk:mboss/butterfly/p/barrage/tail
tag @s remove rlk_mb_bf_p12qy
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p12qx] remove rlk_mb_bf_p12qx
execute at @s run tp @e[type=minecraft:marker,tag=rlk_mb_bf_p12q11,limit=1] ~ ~ ~
