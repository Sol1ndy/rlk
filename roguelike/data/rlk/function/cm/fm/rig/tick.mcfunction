# @s = living brain. Existing gameplay timers are read, not changed, by this rig.
function rlk:cm/fm/rig/select
execute store result score #fmCount tmp if entity @e[tag=rlk_fm_this]
execute unless score #fmCount tmp matches 8 run function rlk:cm/fm/rig/rebuild
execute unless score #fmCount tmp matches 8 run function rlk:cm/fm/rig/select
# Preserve ALL owner-linked projectiles and telegraph attachments, in addition to the rig.
execute as @e[tag=rlk_cmlink] if score @s cmId = #fmId tmp run tag @s add rlk_cmsync
execute facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_fm_this] run tp @s ~ ~ ~ ~ 0
execute store result score #fmX tmp run data get entity @s Pos[0] 1000
execute store result score #fmZ tmp run data get entity @s Pos[2] 1000
scoreboard players operation #fmDX tmp = #fmX tmp
scoreboard players operation #fmDZ tmp = #fmZ tmp
scoreboard players operation #fmDX tmp -= @s cmAX
scoreboard players operation #fmDZ tmp -= @s cmAZ
scoreboard players set #fmNeg tmp -1
execute if score #fmDX tmp matches ..-1 run scoreboard players operation #fmDX tmp *= #fmNeg tmp
execute if score #fmDZ tmp matches ..-1 run scoreboard players operation #fmDZ tmp *= #fmNeg tmp
scoreboard players operation #fmMove tmp = #fmDX tmp
scoreboard players operation #fmMove tmp += #fmDZ tmp
scoreboard players operation @s cmAX = #fmX tmp
scoreboard players operation @s cmAZ = #fmZ tmp
execute if score @s cmAH matches 1 as @e[tag=rlk_fm_this,tag=rlk_fm_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s frzT matches 1.. run return run function rlk:cm/fm/rig/frozen
scoreboard players add @s cmAF 1
execute if score @s cmAF matches 48.. run scoreboard players set @s cmAF 0
scoreboard players operation #fmFrame tmp = @s cmAF
scoreboard players set #fmDiv tmp 12
scoreboard players operation #fmFrame tmp /= #fmDiv tmp
scoreboard players operation #fmPose tmp = #fmFrame tmp
execute if score #fmMove tmp matches 8.. run function rlk:cm/fm/rig/walk
execute if score @s cmS matches 1 run function rlk:cm/fm/rig/charge
execute if score @s cmS matches 2 run function rlk:cm/fm/rig/volley
# A confirmed launch/cast sets cmAR; visual recoil is synced to that same tick.
execute if score @s cmAR matches 10.. run scoreboard players set #fmPose tmp 40
execute if score @s cmAR matches 7..9 run scoreboard players set #fmPose tmp 41
execute if score @s cmAR matches 4..6 run scoreboard players set #fmPose tmp 42
execute if score @s cmAR matches 1..3 run scoreboard players set #fmPose tmp 43
execute if score @s cmS matches 2 if score @s cmAR matches 1.. run function rlk:cm/fm/rig/volley_recover
# Charge immunity also suppresses visual interruption; the red flash still appears.
execute unless entity @s[tag=rlk_cmch] unless score @s cmAR matches 1.. if score @s cmAH matches 4.. run scoreboard players set #fmPose tmp 50
execute unless entity @s[tag=rlk_cmch] unless score @s cmAR matches 1.. if score @s cmAH matches 1..3 run scoreboard players set #fmPose tmp 51
execute unless score @s cmAP = #fmPose tmp run function rlk:cm/fm/rig/apply
scoreboard players operation @s cmAP = #fmPose tmp
execute if score @s cmAR matches 1.. run scoreboard players remove @s cmAR 1
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_fm_this] remove rlk_fm_this
