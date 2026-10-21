# STUB rig (tools/mboss_apep/stub_rig_rt.py; ap_contract 0.4.9): the real rig (wip/ap-rig) replaces it per function.
# Unparked: the stored channels again, the parts follow.
scoreboard players set @s apRigPark 0
function rlk:mboss/apep/rig_stub/look_apply
execute rotated as @s rotated ~ 0 run function rlk:mboss/apep/rig_stub/follow
