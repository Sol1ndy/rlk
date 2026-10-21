# @s = body: R's re-emerge point (2 b before the player on the boss -> player line, clamp r 14).
function rlk:mboss/apep/u/lockb {d:2}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] run tp @s ~ 201 ~
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
