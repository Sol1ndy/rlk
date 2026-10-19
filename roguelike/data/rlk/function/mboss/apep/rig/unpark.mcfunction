# Unpark: re-apply the form, the stance, every look and the follow. @s = rig anchor, at its feet.
scoreboard players set @s apRigPark 0
execute unless entity 524c4b4d-4150-4400-8000-000000000003 run function rlk:mboss/apep/rig/spawn
data merge entity 524c4b4d-4150-4400-8000-000000000040 {shadow_radius:4.5f}
function rlk:mboss/apep/rig/look_apply
function rlk:mboss/apep/rig/stance/apply
scoreboard players set @s apRigState 0
scoreboard players set @s apRigFl 0
scoreboard players reset @s apRigQx
scoreboard players set @s apRigT -1
execute rotated as @s rotated ~ 0 run function rlk:mboss/apep/rig/follow_now
