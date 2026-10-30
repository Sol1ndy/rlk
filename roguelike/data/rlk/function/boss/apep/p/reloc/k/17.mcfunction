# reloc #apPT 17
function rlk:boss/apep/u/lockb {d:2}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] run tp @s ~ 201 ~
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
