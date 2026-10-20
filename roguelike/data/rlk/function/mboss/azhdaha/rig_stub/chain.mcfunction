# STUB rig (tools/mboss_azhdaha/stub_rig.py, manifest.md 8): the real rig (wip/az-rig) replaces it per function.
# Loop / next / hold of the stub clips (ids >= 1000); also called after a real rig tick (api.rig_tick).
execute unless score @s azRigC matches 1000.. run return 0
execute if score @s azRigC matches 1028 if score @s azRigT matches 40 run function rlk:mboss/azhdaha/rig_stub/state/burrowed
execute if score @s azRigC matches 1030 if score @s azRigT matches 8 run function rlk:mboss/azhdaha/rig_stub/state/normal
execute if score @s azRigC matches 1030 if score @s azRigT matches 30 run function rlk:mboss/azhdaha/rig_stub/state/burrowed
execute if score @s azRigC matches 1031 if score @s azRigT matches 24 run function rlk:mboss/azhdaha/rig_stub/state/normal
execute if score @s azRigC matches 1035 if score @s azRigT matches 40 run function rlk:mboss/azhdaha/rig_stub/state/tail_only
execute if score @s azRigC matches 1038 if score @s azRigT matches 18 run function rlk:mboss/azhdaha/rig_stub/state/burrowed
execute if score @s azRigC matches 1000 if score @s azRigT matches 80.. run scoreboard players set @s azRigT 0
execute if score @s azRigC matches 1001 if score @s azRigT matches 40.. run scoreboard players set @s azRigT 0
execute if score @s azRigC matches 1002 if score @s azRigT matches 16.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1003 if score @s azRigT matches 24.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1004 if score @s azRigT matches 24.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1005 if score @s azRigT matches 36.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1006 if score @s azRigT matches 36.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1007 if score @s azRigT matches 60.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1008 if score @s azRigT matches 150.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1009 if score @s azRigT matches 20.. run scoreboard players set @s azRigT 0
execute if score @s azRigC matches 1010 if score @s azRigT matches 40.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1011 if score @s azRigT matches 82.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1012 if score @s azRigT matches 65.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1013 if score @s azRigT matches 53.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1014 if score @s azRigT matches 26.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1015}
execute if score @s azRigC matches 1015 if score @s azRigT matches 12.. run scoreboard players set @s azRigT 0
execute if score @s azRigC matches 1016 if score @s azRigT matches 21.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1017 if score @s azRigT matches 40.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1018 if score @s azRigT matches 63.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1019 if score @s azRigT matches 63.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1020 if score @s azRigT matches 63.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1021 if score @s azRigT matches 63.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1022 if score @s azRigT matches 85.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1023 if score @s azRigT matches 85.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1024 if score @s azRigT matches 50.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1025 if score @s azRigT matches 64.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1026 if score @s azRigT matches 64.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1027 if score @s azRigT matches 70.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1028 if score @s azRigT matches 40.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1029}
execute if score @s azRigC matches 1029 if score @s azRigT matches 20.. run scoreboard players set @s azRigT 0
execute if score @s azRigC matches 1030 if score @s azRigT matches 36.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1029}
execute if score @s azRigC matches 1031 if score @s azRigT matches 53.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1032 if score @s azRigT matches 203.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1033 if score @s azRigT matches 94.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1034 if score @s azRigT matches 52.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1035 if score @s azRigT matches 66.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1036}
execute if score @s azRigC matches 1036 if score @s azRigT matches 80.. run scoreboard players set @s azRigT 0
execute if score @s azRigC matches 1037 if score @s azRigT matches 24.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1036}
execute if score @s azRigC matches 1038 if score @s azRigT matches 20.. run scoreboard players set @s azRigT 19
execute if score @s azRigC matches 1039 if score @s azRigT matches 34.. run return run function rlk:mboss/azhdaha/rig_stub/chain_to {c:1000}
execute if score @s azRigC matches 1040 if score @s azRigT matches 120.. run scoreboard players set @s azRigT 119
