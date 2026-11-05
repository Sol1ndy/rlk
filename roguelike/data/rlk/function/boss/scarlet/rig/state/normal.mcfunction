# Visible again. From hidden: the current clip restarts from its tick 0 at the next rig/tick (its keys show every part);
# already visible: nothing changes (pattern cancels call it freely). @s = the boss.
execute if score @s hrRigS matches 1 run scoreboard players set @s hrRigT -1
scoreboard players set @s hrRigS 0
