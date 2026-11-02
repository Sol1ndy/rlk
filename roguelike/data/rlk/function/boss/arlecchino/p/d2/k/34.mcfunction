# D2 pattern tick 34
function rlk:boss/arlecchino/p/d2/decide
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
execute at @s run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
