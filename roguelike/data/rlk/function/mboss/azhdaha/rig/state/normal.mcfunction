# Normal body state (the clip keys show every part). @s = rig anchor. The parts are brought to the anchor at once
# (follow_now): a module state change (a cancelled burrow, px/state normal) shows them right after this.
scoreboard players set @s azRigState 0
scoreboard players set @s azRigFl 0
scoreboard players reset @s azRigQx
data merge entity 524c4b4d-415a-4400-8000-000000000040 {shadow_radius:4.5f}
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/azhdaha/rig/follow_now
