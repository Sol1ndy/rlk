function rlk:cm/cn/rig/select
execute store result score #cnCount tmp if entity @e[tag=rlk_cn_this]
execute unless score #cnCount tmp matches 11 run function rlk:cm/cn/rig/rebuild
execute unless score #cnCount tmp matches 11 run function rlk:cm/cn/rig/select
execute unless score @s cmS matches 2 unless score @s cmAR matches 1.. facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 as @e[tag=rlk_cn_this] run tp @s ~ ~ ~ ~ 0
execute as @e[tag=rlk_cmlink] if score @s cmId = #cnId tmp run tag @s add rlk_cmsync
execute if score @s cmAH matches 1 as @e[tag=rlk_cn_this,tag=rlk_cn_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
execute if score @s frzT matches 1.. run return run function rlk:cm/cn/rig/frozen
scoreboard players add @s cmAF 1
execute if score @s cmAF matches 48.. run scoreboard players set @s cmAF 0
scoreboard players operation #cnPose tmp = @s cmAF
scoreboard players set #cnDiv tmp 12
scoreboard players operation #cnPose tmp /= #cnDiv tmp
execute if score @s cmS matches 1 run function rlk:cm/cn/rig/wind
execute if score @s cmS matches 2 run scoreboard players set #cnPose tmp 20
execute if score @s cmAR matches 10.. run scoreboard players set #cnPose tmp 30
execute if score @s cmAR matches 8..9 run scoreboard players set #cnPose tmp 31
execute if score @s cmAR matches 5..7 run scoreboard players set #cnPose tmp 32
execute if score @s cmAR matches 1..4 run scoreboard players set #cnPose tmp 33
execute unless score @s cmAP = #cnPose tmp run function rlk:cm/cn/rig/apply
scoreboard players operation @s cmAP = #cnPose tmp
execute if score @s cmAR matches 1.. run scoreboard players remove @s cmAR 1
tag @e[tag=rlk_cn_this] remove rlk_cn_this
