# Hook tick (@s = body, at it): displays, flash, then idle / pattern.
function rlk:mboss/spproto/rig/follow
execute if score #spFlash mb matches 1.. run scoreboard players remove #spFlash mb 1
execute if score #spFlash mb matches 0 run function rlk:mboss/spproto/rig/unglow
execute if score #spFlash mb matches 0 run scoreboard players set #spFlash mb -1
execute unless score #mbSt mb matches 1 run return 0
execute if score #spPat mb matches 1.. run return run function rlk:mboss/spproto/pattern
execute if score #spCool mb matches 1.. run scoreboard players remove #spCool mb 1
function rlk:mboss/mv/turn {max:8}
execute if score #spCool mb matches ..0 run scoreboard players set #spCool mb 60
execute if score #spCool mb matches 60 run function rlk:mboss/spproto/choose
