# E70 pattern tick 74
function rlk:boss/arlecchino/rig_stub/look/wings/open
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.4 1 1.4 0 40 force @a[tag=player]
execute at @s run playsound minecraft:entity.phantom.flap hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
execute at @s run playsound minecraft:item.elytra.flying hostile @a[tag=player] ~ ~ ~ 0.4 1.6 0.13
