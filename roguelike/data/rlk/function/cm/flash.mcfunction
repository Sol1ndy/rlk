execute if entity @s[tag=rlk_cm_sw] run return run function rlk:cm/sw/rig/hurt
execute if entity @s[tag=rlk_cm_ar] run return run function rlk:cm/ar/rig/hurt
execute if entity @s[tag=rlk_cm_fm] run return run function rlk:cm/fm/rig/hurt
execute if entity @s[tag=rlk_cm_im] run return run function rlk:cm/im/rig/hurt
execute if entity @s[tag=rlk_cm_sh] run return run function rlk:cm/sh/rig/hurt
execute if entity @s[tag=rlk_cm_cn] run return run function rlk:cm/cn/rig/hurt
# 두뇌가 맞음 → 모습이 붉게 번쩍 (@s = 두뇌)
scoreboard players operation #fid tmp = @s cmId
execute as @e[tag=rlk_cmv,distance=..5] if score @s cmId = #fid tmp run function rlk:cm/flash2
