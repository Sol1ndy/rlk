function rlk:mboss/proto/rig/follow
execute if score #prFlash mb matches 1.. run scoreboard players remove #prFlash mb 1
execute if score #prFlash mb matches 0 run function rlk:mboss/proto/rig/unglow
execute if score #prFlash mb matches 0 run scoreboard players set #prFlash mb -1
