# Locomotion mode 0 (0 stand, 1 walk, 2 back off, 3 strafe, 4 glide in, 5 glide out).
scoreboard players set #bfMv mb 0
scoreboard players set #bfMvT mb 0
execute if score #bfForm mb matches 1 run function rlk:mboss/butterfly/rig_stub/play/idle_h
execute if score #bfForm mb matches 2 run function rlk:mboss/butterfly/rig_stub/play/idle_b
