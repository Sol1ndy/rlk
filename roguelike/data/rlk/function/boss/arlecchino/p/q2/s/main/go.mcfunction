# Q2 stage main: tick 0 (@s = body), clip q2.
scoreboard players set #q2_s kn 1
scoreboard players set #q2_c kn 0
function rlk:boss/arlecchino/rig_stub/play/q2
function rlk:mboss/mv/face
execute at @s run playsound minecraft:item.trident.riptide_2 hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
execute at @s run playsound minecraft:block.fire.ambient hostile @a[tag=player] ~ ~ ~ 0.6 1 0.2
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run particle minecraft:flame ~ ~ ~ 0.4 0.6 0.4 0.03 10 force @a[tag=player]
