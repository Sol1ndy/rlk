# Q4 stage up: tick 0 (@s = body), clip q4_up.
scoreboard players set #q4_s kn 1
scoreboard players set #q4_c kn 0
function rlk:boss/arlecchino/rig_stub/play/q4_up
function rlk:mboss/mv/face
function rlk:boss/arlecchino/p/q4/f/spot
execute at @s run playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.23
execute at @s run playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.2
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.3 ~ run particle minecraft:crimson_spore ~ ~ ~ 0.6 0.3 0.6 0.05 16 force @a[tag=player]
