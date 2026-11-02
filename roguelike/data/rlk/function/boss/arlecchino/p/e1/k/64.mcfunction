# E1 pattern tick 64
function rlk:boss/arlecchino/core/lockp
function rlk:boss/arlecchino/core/lock_short
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s run playsound minecraft:entity.ravager.roar hostile @a[tag=player] ~ ~ ~ 0.4 1.8 0.13
execute at @s run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.5 1.2 0.17
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run particle minecraft:end_rod ~ ~ ~ 0.2 0.2 0.2 0.02 6 force @a[tag=player]
