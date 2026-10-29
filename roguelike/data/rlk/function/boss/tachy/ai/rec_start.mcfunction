# Recovery start (@s = body, after a pattern / swap / stagger / transition): idle 18-26 t (P3 12-18) of slow prowl
# facing the player: walk in when farther than 6 b, else strafe (random side) - the punish window.
execute if score #ai_fp tk matches 1 store result score #rec tk run random value 18..26
execute if score #ai_fp tk matches 2 store result score #rec tk run random value 18..26
execute if score #ai_fp tk matches 3 store result score #rec tk run random value 12..18
execute if score #ai_d2 tk matches 360001.. run scoreboard players set #ai_mv tk 1
execute if score #ai_d2 tk matches 360001.. run return run function rlk:boss/tachy/rig/play/walk
execute store result score #ai_mv tk run random value 2..3
execute if score #ai_mv tk matches 2 run function rlk:boss/tachy/rig/play/strafe_l
execute if score #ai_mv tk matches 3 run function rlk:boss/tachy/rig/play/strafe_r
