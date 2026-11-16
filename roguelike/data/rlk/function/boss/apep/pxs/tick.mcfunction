# @s = body, after the rig tick: the px set of the clip tick shown now (#apStance mirrors the rig).
scoreboard players operation #apStance mb = @s apRigStance
execute if score @s apRigC matches 0..17 run return run function rlk:boss/apep/pxs/d0_17
execute if score @s apRigC matches 18..35 run return run function rlk:boss/apep/pxs/d18_35
