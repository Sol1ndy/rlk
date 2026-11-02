# C2 pattern tick 78
function rlk:boss/arlecchino/rig_stub/look/wings/open
function rlk:boss/arlecchino/rig_stub/look/glow/crimson
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.2 1 1.2 0 30 force @a[tag=player]
execute at @s run playsound minecraft:entity.phantom.flap hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
execute at @s run playsound minecraft:item.elytra.flying hostile @a[tag=player] ~ ~ ~ 0.4 1.6 0.13
