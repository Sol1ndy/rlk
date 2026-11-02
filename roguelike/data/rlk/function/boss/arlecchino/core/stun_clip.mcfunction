# The stun clip of the form (@s = body).
execute if score #ph kn matches 5 run return run function rlk:boss/arlecchino/rig_stub/play/stun2
function rlk:boss/arlecchino/rig_stub/play/stun
execute at @s run playsound minecraft:entity.iron_golem.damage hostile @a[tag=player] ~ ~ ~ 0.6 0.6 0.2
