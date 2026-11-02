# Q3 stage whip: tick 0 (@s = body), clip q3.
scoreboard players set #q3_s kn 1
scoreboard players set #q3_c kn 0
function rlk:boss/arlecchino/rig_stub/play/q3
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
execute at @s run playsound minecraft:entity.phantom.flap hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
execute at @s positioned ~ ~1.6 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.2 0.8 1.2 0 24 force @a[tag=player]
