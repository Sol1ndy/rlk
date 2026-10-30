# Hook tick (@s = body, at it): rig, flash, cine clock, the phase switch, the push request, then idle / pattern.
function rlk:mboss/cproto/rig/tick
execute if score #cpFlash mb matches 1.. run scoreboard players remove #cpFlash mb 1
execute if score #cpFlash mb matches 0 run function rlk:mboss/cproto/rig/unglow
execute if score #cpFlash mb matches 0 run scoreboard players set #cpFlash mb -1
execute if score #cpCine mb matches 1.. run scoreboard players remove #cpCine mb 1
execute if score #cpCine mb matches 0 if score #mbCine mb matches 1 run function rlk:mboss/cine/end
execute if score #cpPh mb matches 1 if score #mbFloorHit mb matches 1 run function rlk:mboss/cproto/phase2
execute if score #cpPush mb matches 1 run scoreboard players set #mbPushOn mb 1
execute if score #mbCine mb matches 1 run return 0
execute unless score #mbSt mb matches 1 run return 0
execute if score #cpPat mb matches 1.. run return run function rlk:mboss/cproto/pattern
execute if score #cpCool mb matches 1.. run scoreboard players remove #cpCool mb 1
function rlk:mboss/mv/turn {max:8}
execute if score #cpCool mb matches ..0 run scoreboard players set #cpCool mb 70
execute if score #cpCool mb matches 70 run function rlk:mboss/cproto/choose
