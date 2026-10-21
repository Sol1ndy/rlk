# @s = body, after the rig tick: the px set of the clip tick shown now (#apStance mirrors the rig).
scoreboard players operation #apStance mb = @s apRigStance
execute if score @s apRigC matches 1000..1017 run return run function rlk:mboss/apep/pxs/d1000_1017
execute if score @s apRigC matches 1018..1035 run return run function rlk:mboss/apep/pxs/d1018_1035
