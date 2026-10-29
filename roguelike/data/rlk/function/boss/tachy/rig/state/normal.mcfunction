# Visible again. From hidden: the current clip restarts from its tick 0 at the next rig/tick (its keys show every part);
# already visible: nothing changes (pattern cancels call it freely). @s = the boss.
execute if score @s tkRigS matches 1 run scoreboard players set @s tkRigT -1
scoreboard players set @s tkRigS 0
