# 새 커스텀 몹 두뇌 (@s, at @s)
tag @s remove rlk_cmnew
scoreboard players set @s cmS 0
scoreboard players set @s cmF 0
execute store result score @s cmCd run random value 20..50
scoreboard players set @s cmCd2 60
execute store result score @s cmYaw run random value -18000..18000
execute if entity @s[tag=rlk_cm_sh] run scoreboard players set @s cmF 2
scoreboard players operation #cid tmp = @s cmId
execute if entity @s[tag=rlk_cm_cn] run function rlk:cm/cn/build
execute if entity @s[tag=rlk_cm_sw] run function rlk:cm/sw/rig/rebuild

execute if entity @s[tag=rlk_cm_ar] run function rlk:cm/ar/rig/rebuild

execute if entity @s[tag=rlk_cm_fm] run function rlk:cm/fm/rig/rebuild

execute if entity @s[tag=rlk_cm_im] run function rlk:cm/im/rig/rebuild

execute if entity @s[tag=rlk_cm_sh] run function rlk:cm/sh/rig/rebuild
