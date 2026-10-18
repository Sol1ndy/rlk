# STUB rig (tools/mboss_fieldgen/stub_rig.py): replaced by the real rig (wip/fg-rig) at merge time.
# Starts wave (36 t) at the next rig tick.
scoreboard players set @s fgRigC 11
scoreboard players set @s fgRigT -1
execute if score @s fgRigV matches 1 run function rlk:mboss/fieldgen/rig_stub/show
