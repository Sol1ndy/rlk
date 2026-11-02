# Q4 stage shot: tick 0 (@s = body), clip q4_shot.
scoreboard players set #q4_s kn 2
scoreboard players set #q4_c kn 0
function rlk:boss/arlecchino/rig_stub/play/q4_shot
scoreboard players add #q4_k kn 1
function rlk:boss/arlecchino/rig_stub/look/glow/crimson
execute at @s run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.6 1.6 0.2
execute at @s run playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.4 1.8 0.13
function rlk:boss/arlecchino/p/q4/f/aim
