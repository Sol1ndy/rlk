# The rig crack look of #fgCrack (0-3 the meter stages, 4 burst).
execute if score #fgCrack mb matches 0 run return run function rlk:mboss/fieldgen/rig_stub/crack/0
execute if score #fgCrack mb matches 1 run return run function rlk:mboss/fieldgen/rig_stub/crack/1
execute if score #fgCrack mb matches 2 run return run function rlk:mboss/fieldgen/rig_stub/crack/2
execute if score #fgCrack mb matches 3 run return run function rlk:mboss/fieldgen/rig_stub/crack/3
execute if score #fgCrack mb matches 4 run return run function rlk:mboss/fieldgen/rig_stub/crack/4
