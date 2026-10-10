# @s = living brain. Existing gameplay timers are read, not changed, by this rig.
function rlk:cm/ar/rig/select
execute store result score #arCount tmp if entity @e[tag=rlk_ar_this]
execute unless score #arCount tmp matches 11 run function rlk:cm/ar/rig/rebuild
execute unless score #arCount tmp matches 11 run function rlk:cm/ar/rig/select
# Preserve ALL owner-linked projectiles and telegraph attachments, in addition to the rig.
execute as @e[tag=rlk_cmlink] if score @s cmId = #arId tmp run tag @s add rlk_cmsync
execute unless score @s cmAR matches 1.. facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_ar_this] run tp @s ~ ~ ~ ~ 0
# Keep the released arrow heading through recoil, while still following the brain position.
execute if score @s cmAR matches 1.. as @e[tag=rlk_ar_this] rotated as @s run tp @s ~ ~ ~ ~ 0
# The final draw follows the already-locked projectile heading.
execute if score @s cmS matches 1 if score @s cmT <= #cmW_arL tmp as @e[tag=rlk_cmline,distance=..8] if score @s cmId = #arId tmp rotated as @s rotated ~ 0 as @e[tag=rlk_ar_this] run tp @s ~ ~ ~ ~ 0
execute store result score #arX tmp run data get entity @s Pos[0] 1000
execute store result score #arZ tmp run data get entity @s Pos[2] 1000
scoreboard players operation #arDX tmp = #arX tmp
scoreboard players operation #arDZ tmp = #arZ tmp
scoreboard players operation #arDX tmp -= @s cmAX
scoreboard players operation #arDZ tmp -= @s cmAZ
scoreboard players set #arNeg tmp -1
execute if score #arDX tmp matches ..-1 run scoreboard players operation #arDX tmp *= #arNeg tmp
execute if score #arDZ tmp matches ..-1 run scoreboard players operation #arDZ tmp *= #arNeg tmp
scoreboard players operation #arMove tmp = #arDX tmp
scoreboard players operation #arMove tmp += #arDZ tmp
scoreboard players operation @s cmAX = #arX tmp
scoreboard players operation @s cmAZ = #arZ tmp
execute if score @s cmAH matches 1 as @e[tag=rlk_ar_this,tag=rlk_ar_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s frzT matches 1.. run return run function rlk:cm/ar/rig/frozen
scoreboard players add @s cmAF 1
execute if score @s cmAF matches 48.. run scoreboard players set @s cmAF 0
scoreboard players operation #arFrame tmp = @s cmAF
scoreboard players set #arDiv tmp 12
scoreboard players operation #arFrame tmp /= #arDiv tmp
scoreboard players operation #arPose tmp = #arFrame tmp
execute if score #arMove tmp matches 8.. run function rlk:cm/ar/rig/walk
execute if score @s cmS matches 1 run function rlk:cm/ar/rig/charge
# A confirmed launch/cast sets cmAR; visual recoil is synced to that same tick.
execute if score @s cmAR matches 10.. run scoreboard players set #arPose tmp 40
execute if score @s cmAR matches 7..9 run scoreboard players set #arPose tmp 41
execute if score @s cmAR matches 4..6 run scoreboard players set #arPose tmp 42
execute if score @s cmAR matches 1..3 run scoreboard players set #arPose tmp 43
# Charge immunity also suppresses visual interruption; the red flash still appears.
execute unless entity @s[tag=rlk_cmch] unless score @s cmAR matches 1.. if score @s cmAH matches 4.. run scoreboard players set #arPose tmp 50
execute unless entity @s[tag=rlk_cmch] unless score @s cmAR matches 1.. if score @s cmAH matches 1..3 run scoreboard players set #arPose tmp 51
execute unless score @s cmAP = #arPose tmp run function rlk:cm/ar/rig/apply
scoreboard players operation @s cmAP = #arPose tmp
execute if score @s cmAR matches 1.. run scoreboard players remove @s cmAR 1
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_ar_this] remove rlk_ar_this
