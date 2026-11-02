# Q4 stage shot tick 20
function rlk:boss/arlecchino/core/lockp
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.6 1.6 0.2
execute at @s run playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.4 1.8 0.13
function rlk:boss/arlecchino/p/q4/f/aim
