function rlk:mboss/spproto/rig/follow
execute if score #spFlash mb matches 1.. run scoreboard players remove #spFlash mb 1
execute if score #spFlash mb matches 0 run function rlk:mboss/spproto/rig/unglow
execute if score #spFlash mb matches 0 run scoreboard players set #spFlash mb -1
