execute if entity @s[tag=rlk_c3a] run return run function rlk:cm/c3/vis
execute if entity @s[tag=rlk_cm_ci] run return run function rlk:cm/ci/rig/tick
execute if entity @s[tag=rlk_cm_cc] run return run function rlk:cm/cc/rig/tick
execute if entity @s[tag=rlk_cm_nj] run return run function rlk:cm/nj/rig/tick
execute if entity @s[tag=rlk_cm_kr] run return run function rlk:cm/kr/rig/tick
execute if entity @s[tag=rlk_c2a] run return run function rlk:cm/c2/vis
execute if entity @s[tag=rlk_cm_sw] run return run function rlk:cm/sw/rig/tick
execute if entity @s[tag=rlk_cm_ar] at @s run return run function rlk:cm/ar/rig/tick
execute if entity @s[tag=rlk_cm_fm] at @s run return run function rlk:cm/fm/rig/tick
execute if entity @s[tag=rlk_cm_im] at @s run return run function rlk:cm/im/rig/tick
execute if entity @s[tag=rlk_cm_sh] at @s run return run function rlk:cm/sh/rig/tick
execute if entity @s[tag=rlk_cm_cn] at @s run return run function rlk:cm/cn/rig/tick
# 모습을 두뇌 위치로. cmF 0 = 몸을 바라봄, 2 = cmYaw 방향(방패병)
execute if score @s cmF matches 0 positioned ~ ~1.5 ~ facing entity @e[tag=rlk_cmaim,limit=1] feet positioned ~ ~-1.5 ~ as @e[tag=rlk_cmv,distance=..5] if score @s cmId = #cid tmp run tp @s ~ ~ ~ ~ ~
execute if score @s cmF matches 2 store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
execute if score @s cmF matches 2 rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 as @e[tag=rlk_cmv,distance=..5] if score @s cmId = #cid tmp run tp @s ~ ~ ~ ~ ~
execute as @e[tag=rlk_cmlink,distance=..10] if score @s cmId = #cid tmp run tag @s add rlk_cmsync
