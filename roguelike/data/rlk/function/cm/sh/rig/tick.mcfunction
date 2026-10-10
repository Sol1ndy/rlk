# @s = the shield soldier brain, at @s. Keep actual turn rate and rush facing.
function rlk:cm/sh/rig/select
execute store result score #shCount tmp if entity @e[tag=rlk_sh_this]
execute unless score #shCount tmp matches 8 run function rlk:cm/sh/rig/rebuild
execute unless score #shCount tmp matches 8 run function rlk:cm/sh/rig/select
tag @e[tag=rlk_sh_this] add rlk_cmsync
execute as @e[tag=rlk_cmlink,distance=..10] if score @s cmId = #shId tmp run tag @s add rlk_cmsync
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 as @e[tag=rlk_sh_this] run tp @s ~ ~ ~ ~ 0
execute if score @s cmSh matches ..0 unless entity @e[tag=rlk_sh_this,tag=rlk_sh_broken] run function rlk:cm/sh/rig/hide_shield
execute store result score #shX tmp run data get entity @s Pos[0] 1000
execute store result score #shZ tmp run data get entity @s Pos[2] 1000
scoreboard players operation #shDX tmp = #shX tmp
scoreboard players operation #shDZ tmp = #shZ tmp
scoreboard players operation #shDX tmp -= @s cmAX
scoreboard players operation #shDZ tmp -= @s cmAZ
scoreboard players set #shNeg tmp -1
execute if score #shDX tmp matches ..-1 run scoreboard players operation #shDX tmp *= #shNeg tmp
execute if score #shDZ tmp matches ..-1 run scoreboard players operation #shDZ tmp *= #shNeg tmp
scoreboard players operation #shMove tmp = #shDX tmp
scoreboard players operation #shMove tmp += #shDZ tmp
scoreboard players operation @s cmAX = #shX tmp
scoreboard players operation @s cmAZ = #shZ tmp
execute if score @s cmAH matches 1 as @e[tag=rlk_sh_this,tag=rlk_sh_part,tag=!rlk_sh_broken] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s frzT matches 1.. run return run function rlk:cm/sh/rig/frozen
scoreboard players add @s cmAF 1
execute if score @s cmAF matches 48.. run scoreboard players set @s cmAF 0
scoreboard players operation #shFrame tmp = @s cmAF
scoreboard players set #shDiv tmp 12
scoreboard players operation #shFrame tmp /= #shDiv tmp
scoreboard players operation #shPose tmp = #shFrame tmp
execute if score #shMove tmp matches 8.. run function rlk:cm/sh/rig/walk
execute if score @s cmAR matches 7.. run scoreboard players set #shPose tmp 60
execute if score @s cmAR matches 4..6 run scoreboard players set #shPose tmp 61
execute if score @s cmAR matches 1..3 run scoreboard players set #shPose tmp 62
execute if score @s cmS matches 1 run function rlk:cm/sh/rig/bash_wind
execute if score @s cmS matches 2 run function rlk:cm/sh/rig/rush_wind
execute if score @s cmS matches 3 run function rlk:cm/sh/rig/rush_pose
execute if score @s cmS matches 4 run function rlk:cm/sh/rig/rush_bash
execute unless entity @s[tag=rlk_cmch] if score @s cmAH matches 4.. run scoreboard players set #shPose tmp 70
execute unless entity @s[tag=rlk_cmch] if score @s cmAH matches 1..3 run scoreboard players set #shPose tmp 71
execute unless score @s cmAP = #shPose tmp run function rlk:cm/sh/rig/apply
scoreboard players operation @s cmAP = #shPose tmp
execute if score @s cmAR matches 1.. run scoreboard players remove @s cmAR 1
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_sh_this] remove rlk_sh_this
