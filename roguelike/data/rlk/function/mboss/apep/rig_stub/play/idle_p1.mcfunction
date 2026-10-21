# STUB rig (tools/mboss_apep/stub_rig_rt.py; ap_contract 0.4.9): the real rig (wip/ap-rig) replaces it per function.
# Play idle_p1 (60 t, stub id 1001) from its tick 0 at the next rig tick (the
# stance of its first pose at once).
scoreboard players set @s apRigC 1001
scoreboard players set @s apRigT -1
function rlk:mboss/apep/rig_stub/stance/crouch
