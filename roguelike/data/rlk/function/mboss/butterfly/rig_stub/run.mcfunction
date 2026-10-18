# STUB rig (tools/mboss_butterfly/stub_rig.py): replaced by the real rig at merge time.
# Clip end: loop, next clip or hold; the clips' form switches (manifest "forms").
execute if score @s bfStubC matches 0 if score @s bfStubT matches 40.. run scoreboard players set @s bfStubT 0
execute if score @s bfStubC matches 1 if score @s bfStubT matches 16.. run scoreboard players set @s bfStubT 0
execute if score @s bfStubC matches 2 if score @s bfStubT matches 8.. run scoreboard players set @s bfStubT 0
execute if score @s bfStubC matches 3 if score @s bfStubT matches 12.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_h
execute if score @s bfStubC matches 4 if score @s bfStubT matches 24.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_h
execute if score @s bfStubC matches 5 if score @s bfStubT matches 51.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_h
execute if score @s bfStubC matches 6 if score @s bfStubT matches 65.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_h
execute if score @s bfStubC matches 7 if score @s bfStubT matches 50.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_h
execute if score @s bfStubC matches 8 if score @s bfStubT matches 41.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_h
execute if score @s bfStubC matches 9 if score @s bfStubT matches 40.. run scoreboard players set @s bfStubT 0
execute if score @s bfStubC matches 10 if score @s bfStubT matches 106.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_h
execute if score @s bfStubC matches 11 if score @s bfStubT matches 30.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_b
execute if score @s bfStubC matches 12 if score @s bfStubT matches 22.. run scoreboard players set @s bfStubT 0
execute if score @s bfStubC matches 13 if score @s bfStubT matches 16.. run scoreboard players set @s bfStubT 0
execute if score @s bfStubC matches 14 if score @s bfStubT matches 55.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_b
execute if score @s bfStubC matches 15 if score @s bfStubT matches 117.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_b
execute if score @s bfStubC matches 16 if score @s bfStubT matches 59.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_b
execute if score @s bfStubC matches 17 if score @s bfStubT matches 76.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_b
execute if score @s bfStubC matches 18 if score @s bfStubT matches 96.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_h
execute if score @s bfStubC matches 19 if score @s bfStubT matches 43.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_h
execute if score @s bfStubC matches 21 if score @s bfStubT matches 18.. run return run function rlk:mboss/butterfly/rig_stub/play/idle_h
execute if score @s bfStubC matches 11 if score @s bfStubT matches 4 run function rlk:mboss/butterfly/rig_stub/form/butterfly
execute if score @s bfStubC matches 18 if score @s bfStubT matches 92 run function rlk:mboss/butterfly/rig_stub/form/human
execute if score @s bfStubC matches 19 if score @s bfStubT matches 39 run function rlk:mboss/butterfly/rig_stub/form/human
execute if score @s bfStubC matches 10 if score @s bfStubT matches 79 run function rlk:mboss/butterfly/rig_stub/show
