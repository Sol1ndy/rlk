# @s = living brain. Existing gameplay timers are read, not changed, by this rig.
function rlk:cm/im/rig/select
execute store result score #imCount tmp if entity @e[tag=rlk_im_this]
execute unless score #imCount tmp matches 8 run function rlk:cm/im/rig/rebuild
execute unless score #imCount tmp matches 8 run function rlk:cm/im/rig/select
# Preserve ALL owner-linked projectiles and telegraph attachments, in addition to the rig.
execute as @e[tag=rlk_cmlink] if score @s cmId = #imId tmp run tag @s add rlk_cmsync
execute facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_im_this] run tp @s ~ ~ ~ ~ 0
execute store result score #imX tmp run data get entity @s Pos[0] 1000
execute store result score #imZ tmp run data get entity @s Pos[2] 1000
scoreboard players operation #imDX tmp = #imX tmp
scoreboard players operation #imDZ tmp = #imZ tmp
scoreboard players operation #imDX tmp -= @s cmAX
scoreboard players operation #imDZ tmp -= @s cmAZ
scoreboard players set #imNeg tmp -1
execute if score #imDX tmp matches ..-1 run scoreboard players operation #imDX tmp *= #imNeg tmp
execute if score #imDZ tmp matches ..-1 run scoreboard players operation #imDZ tmp *= #imNeg tmp
scoreboard players operation #imMove tmp = #imDX tmp
scoreboard players operation #imMove tmp += #imDZ tmp
scoreboard players operation @s cmAX = #imX tmp
scoreboard players operation @s cmAZ = #imZ tmp
execute if score @s cmAH matches 1 as @e[tag=rlk_im_this,tag=rlk_im_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s frzT matches 1.. run return run function rlk:cm/im/rig/frozen
scoreboard players add @s cmAF 1
execute if score @s cmAF matches 48.. run scoreboard players set @s cmAF 0
scoreboard players operation #imFrame tmp = @s cmAF
scoreboard players set #imDiv tmp 12
scoreboard players operation #imFrame tmp /= #imDiv tmp
scoreboard players operation #imPose tmp = #imFrame tmp
execute if score #imMove tmp matches 8.. run function rlk:cm/im/rig/walk
execute if score @s cmS matches 1 run function rlk:cm/im/rig/charge
# A confirmed launch/cast sets cmAR; visual recoil is synced to that same tick.
execute if score @s cmAR matches 10.. run scoreboard players set #imPose tmp 40
execute if score @s cmAR matches 7..9 run scoreboard players set #imPose tmp 41
execute if score @s cmAR matches 4..6 run scoreboard players set #imPose tmp 42
execute if score @s cmAR matches 1..3 run scoreboard players set #imPose tmp 43
# Charge immunity also suppresses visual interruption; the red flash still appears.
execute unless entity @s[tag=rlk_cmch] unless score @s cmAR matches 1.. if score @s cmAH matches 4.. run scoreboard players set #imPose tmp 50
execute unless entity @s[tag=rlk_cmch] unless score @s cmAR matches 1.. if score @s cmAH matches 1..3 run scoreboard players set #imPose tmp 51
execute unless score @s cmAP = #imPose tmp run function rlk:cm/im/rig/apply
scoreboard players operation @s cmAP = #imPose tmp
execute if score @s cmAR matches 1.. run scoreboard players remove @s cmAR 1
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_im_this] remove rlk_im_this
