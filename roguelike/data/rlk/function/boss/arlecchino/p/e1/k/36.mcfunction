# E1 pattern tick 36
function rlk:boss/arlecchino/p/e1/zig_l
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run particle minecraft:dust{color:[1.0,0.55,0.16],scale:1.4} ~ ~ ~ 0.8 0.3 0.8 0 14 force @a[tag=player]
execute at @s run playsound minecraft:entity.phantom.swoop hostile @a[tag=player] ~ ~ ~ 0.5 1.8 0.17
