# sink_revive: 60 t, holds the last pose. @s = rig anchor.
execute if score @s apRigT matches 61.. run return run scoreboard players set @s apRigT 61
execute if score @s apRigT matches ..23 run return run function rlk:mboss/apep/rig/c/sink_revive/b/0_23
function rlk:mboss/apep/rig/c/sink_revive/b/24_59
