# @s = invisible swordsman husk, at @s. Actual AI and damage remain in cm/sw.
function rlk:cm/sw/rig/select
execute store result score #swCount tmp if entity @e[tag=rlk_sw_this]
execute unless score #swCount tmp matches 8 run function rlk:cm/sw/rig/rebuild
execute unless score #swCount tmp matches 8 run function rlk:cm/sw/rig/select
tag @e[tag=rlk_sw_this] add rlk_cmsync
# The anchor and all joints share the same feet origin and yaw; never copy camera pitch.
execute facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_sw_this] run tp @s ~ ~ ~ ~ 0
execute store result score #swX tmp run data get entity @s Pos[0] 1000
execute store result score #swZ tmp run data get entity @s Pos[2] 1000
scoreboard players operation #swDX tmp = #swX tmp
scoreboard players operation #swDZ tmp = #swZ tmp
scoreboard players operation #swDX tmp -= @s cmAX
scoreboard players operation #swDZ tmp -= @s cmAZ
scoreboard players set #swNeg tmp -1
execute if score #swDX tmp matches ..-1 run scoreboard players operation #swDX tmp *= #swNeg tmp
execute if score #swDZ tmp matches ..-1 run scoreboard players operation #swDZ tmp *= #swNeg tmp
scoreboard players operation #swMove tmp = #swDX tmp
scoreboard players operation #swMove tmp += #swDZ tmp
scoreboard players operation @s cmAX = #swX tmp
scoreboard players operation @s cmAZ = #swZ tmp
execute if score @s cmAH matches 1 as @e[tag=rlk_sw_this,tag=rlk_sw_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
# Freeze preserves the current client pose and pauses the visual timers.
execute if score @s frzT matches 1.. run return run function rlk:cm/sw/rig/frozen
scoreboard players add @s cmAF 1
execute if score @s cmAF matches 48.. run scoreboard players set @s cmAF 0
scoreboard players operation #swFrame tmp = @s cmAF
scoreboard players set #swDiv tmp 12
scoreboard players operation #swFrame tmp /= #swDiv tmp
scoreboard players operation #swPose tmp = #swFrame tmp
execute if score #swMove tmp matches 8.. run function rlk:cm/sw/rig/walk
# Recovery is visual only; the original AI/cooldown/attack range are unchanged.
execute if score @s cmAR matches 9.. run scoreboard players set #swPose tmp 30
execute if score @s cmAR matches 6..8 run scoreboard players set #swPose tmp 31
execute if score @s cmAR matches 3..5 run scoreboard players set #swPose tmp 32
execute if score @s cmAR matches 1..2 run scoreboard players set #swPose tmp 33
execute if score @s cmS matches 1 run function rlk:cm/sw/rig/wind
execute if score @s cmAH matches 4.. run scoreboard players set #swPose tmp 40
execute if score @s cmAH matches 1..3 run scoreboard players set #swPose tmp 41
execute unless score @s cmAP = #swPose tmp run function rlk:cm/sw/rig/apply
scoreboard players operation @s cmAP = #swPose tmp
execute if score @s cmAR matches 1.. run scoreboard players remove @s cmAR 1
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_sw_this] remove rlk_sw_this
