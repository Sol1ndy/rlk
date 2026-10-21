# @s = body: the surfacing point (9 b from the player toward the boss, clamp r 14).
function rlk:boss/apep/u/lockb {d:9}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] run tp @s ~ 201 ~
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
