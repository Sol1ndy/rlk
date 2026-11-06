# Internal: brightness from apRigBright x apRigForm, then the core glow.
execute if score @s apRigBright matches 1 run function rlk:boss/apep/rig/look/r/bright/all_15
execute if score @s apRigBright matches 0 if score @s apRigForm matches 0 run function rlk:boss/apep/rig/look/r/bright/p1_13
execute if score @s apRigBright matches 0 if score @s apRigForm matches 1 run function rlk:boss/apep/rig/look/r/bright/p3_13
execute if score @s apRigGlow matches 0 if score @s apRigBright matches 0 run data merge entity 524c4b4d-4150-4400-8000-000000000005 {brightness:{block:12,sky:15}}
execute if score @s apRigGlow matches 1 run data merge entity 524c4b4d-4150-4400-8000-000000000005 {brightness:{block:15,sky:15}}
execute if score @s apRigBright matches 1 run data merge entity 524c4b4d-4150-4400-8000-000000000005 {brightness:{block:15,sky:15}}
