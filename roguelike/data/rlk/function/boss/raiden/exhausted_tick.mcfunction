# Phase 3, as the boss: kneel loop after the collapse, stand up, then the Shogun returns.
execute if score @s rdTime matches 46 at @s rotated as @s run function rlk:boss/raiden/rig/start/exhausted
execute if score @s rdTime matches 272 at @s rotated as @s run function rlk:boss/raiden/rig/start/recover
execute if score @s rdTime matches 300 at @s rotated as @s run function rlk:boss/raiden/normal_return
