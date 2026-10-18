# STUB rig (tools/mboss_fieldgen/stub_rig.py): replaced by the real rig (wip/fg-rig) at merge time.
# Clip end: loop, next clip or hold; the clips' form switches and hidden spans (manifest "forms", "hidden").
execute if score @s fgRigC matches 0 if score @s fgRigT matches 80.. run scoreboard players set @s fgRigT 0
execute if score @s fgRigC matches 1 if score @s fgRigT matches 20.. run scoreboard players set @s fgRigT 0
execute if score @s fgRigC matches 2 if score @s fgRigT matches 112.. run return run function rlk:mboss/fieldgen/rig_stub/play/idle_cruise
execute if score @s fgRigC matches 3 if score @s fgRigT matches 58.. run return run function rlk:mboss/fieldgen/rig_stub/play/idle_cruise
execute if score @s fgRigC matches 4 if score @s fgRigT matches 45.. run return run function rlk:mboss/fieldgen/rig_stub/play/idle_cruise
execute if score @s fgRigC matches 5 if score @s fgRigT matches 174.. run return run function rlk:mboss/fieldgen/rig_stub/play/idle_cruise
execute if score @s fgRigC matches 6 if score @s fgRigT matches 70.. run return run function rlk:mboss/fieldgen/rig_stub/play/idle_cruise
execute if score @s fgRigC matches 7 if score @s fgRigT matches 110.. run return run function rlk:mboss/fieldgen/rig_stub/play/idle_cruise
execute if score @s fgRigC matches 8 if score @s fgRigT matches 157.. run return run function rlk:mboss/fieldgen/rig_stub/play/idle_cruise
execute if score @s fgRigC matches 10 if score @s fgRigT matches 24.. run return run function rlk:mboss/fieldgen/rig_stub/play/field_idle
execute if score @s fgRigC matches 11 if score @s fgRigT matches 36.. run return run function rlk:mboss/fieldgen/rig_stub/play/field_idle
execute if score @s fgRigC matches 12 if score @s fgRigT matches 80.. run scoreboard players set @s fgRigT 0
execute if score @s fgRigC matches 13 if score @s fgRigT matches 40.. run return run function rlk:mboss/fieldgen/rig_stub/play/field_idle
execute if score @s fgRigC matches 14 if score @s fgRigT matches 78.. run return run function rlk:mboss/fieldgen/rig_stub/play/idle_cruise
execute if score @s fgRigC matches 15 if score @s fgRigT matches 34.. run return run function rlk:mboss/fieldgen/rig_stub/play/groggy
execute if score @s fgRigC matches 16 if score @s fgRigT matches 40.. run scoreboard players set @s fgRigT 0
execute if score @s fgRigC matches 17 if score @s fgRigT matches 15.. run return run function rlk:mboss/fieldgen/rig_stub/play/idle_cruise
execute if score @s fgRigC matches 2 if score @s fgRigT matches 0 run function rlk:mboss/fieldgen/rig_stub/form/dormant
execute if score @s fgRigC matches 2 if score @s fgRigT matches 28 run function rlk:mboss/fieldgen/rig_stub/form/cruise
execute if score @s fgRigC matches 5 if score @s fgRigT matches 0 run function rlk:mboss/fieldgen/rig_stub/form/laser
execute if score @s fgRigC matches 5 if score @s fgRigT matches 172 run function rlk:mboss/fieldgen/rig_stub/form/cruise
execute if score @s fgRigC matches 7 if score @s fgRigT matches 7 run function rlk:mboss/fieldgen/rig_stub/form/coreup
execute if score @s fgRigC matches 7 if score @s fgRigT matches 108 run function rlk:mboss/fieldgen/rig_stub/form/cruise
execute if score @s fgRigC matches 8 if score @s fgRigT matches 20 run function rlk:mboss/fieldgen/rig_stub/form/tower
execute if score @s fgRigC matches 8 if score @s fgRigT matches 154 run function rlk:mboss/fieldgen/rig_stub/form/cruise
execute if score @s fgRigC matches 10 if score @s fgRigT matches 1 run function rlk:mboss/fieldgen/rig_stub/form/field
execute if score @s fgRigC matches 14 if score @s fgRigT matches 22 run function rlk:mboss/fieldgen/rig_stub/form/deployed
execute if score @s fgRigC matches 14 if score @s fgRigT matches 76 run function rlk:mboss/fieldgen/rig_stub/form/cruise
execute if score @s fgRigC matches 17 if score @s fgRigT matches 14 run function rlk:mboss/fieldgen/rig_stub/form/cruise
execute if score @s fgRigC matches 9 if score @s fgRigT matches 13 run function rlk:mboss/fieldgen/rig_stub/hide
execute if score @s fgRigC matches 10 if score @s fgRigT matches 0 run function rlk:mboss/fieldgen/rig_stub/show
