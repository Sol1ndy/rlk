# Q5B stage main: tick 0 (@s = body), clip q5b.
scoreboard players set #q5b_s kn 1
scoreboard players set #q5b_c kn 0
function rlk:boss/arlecchino/rig_stub/play/q5b
function rlk:mboss/mv/face
function rlk:boss/arlecchino/rig_stub/look/glow/crimson
execute at @s run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.23
execute at @s run playsound minecraft:entity.wither.shoot hostile @a[tag=player] ~ ~ ~ 0.4 0.6 0.13
