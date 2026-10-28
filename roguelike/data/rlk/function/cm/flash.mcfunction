execute if entity @s[tag=rlk_cm_ci] run return run function rlk:cm/ci/rig/hurt
execute if entity @s[tag=rlk_cm_cc] run return run function rlk:cm/cc/rig/hurt
execute if entity @s[tag=rlk_cm_nj] run return run function rlk:cm/nj/rig/hurt
execute if entity @s[tag=rlk_cm_kr] run return run function rlk:cm/kr/rig/hurt
execute if entity @s[tag=rlk_c2a] run return run function rlk:cm/c2/hurt
execute if entity @s[tag=rlk_cm_sw] run return run function rlk:cm/sw/rig/hurt
execute if entity @s[tag=rlk_cm_ar] run return run function rlk:cm/ar/rig/hurt
execute if entity @s[tag=rlk_cm_fm] run return run function rlk:cm/fm/rig/hurt
execute if entity @s[tag=rlk_cm_im] run return run function rlk:cm/im/rig/hurt
execute if entity @s[tag=rlk_cm_sh] run return run function rlk:cm/sh/rig/hurt
execute if entity @s[tag=rlk_cm_cn] run return run function rlk:cm/cn/rig/hurt
# 두뇌가 맞음 → 모습이 붉게 번쩍 (@s = 두뇌)
scoreboard players operation #fid tmp = @s cmId
execute as @e[tag=rlk_cmv,distance=..5] if score @s cmId = #fid tmp run function rlk:cm/flash2
