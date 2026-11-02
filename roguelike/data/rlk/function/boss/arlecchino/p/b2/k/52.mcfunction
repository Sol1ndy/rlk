# B2 pattern tick 52
function rlk:mboss/mv/lockv {lead:6}
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
