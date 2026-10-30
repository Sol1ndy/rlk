# @s player. Existing avatar remains the gameplay body.
function rlk:char/motion/release
scoreboard players set @s pmBlend 0
scoreboard players set @s pmWeapon -1
scoreboard players set @s pmActive 1
scoreboard players set @s pmTick 0
scoreboard players set @s pmLen 23
scoreboard players set @s pmChar 3
scoreboard players set @s pmSpeed 100
execute if score @s pmSpeed matches ..24 run scoreboard players set @s pmSpeed 25
execute if score @s pmSpeed matches 501.. run scoreboard players set @s pmSpeed 500
scoreboard players set @s pmAcc 0
scoreboard players set @s pmStep 99
scoreboard players operation @s pmStep += @s pmSpeed
scoreboard players operation @s pmStep /= @s pmSpeed
data modify storage rlk:player_motion active set value {char:"skirk",clip:"burst_jin",step:1,loop:0b,lockedYaw:1b}
execute store result storage rlk:player_motion active.step int 1 run scoreboard players get @s pmStep
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_pet","rlk_pm_basis"]}
execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run tp @e[tag=rlk_pm_basis,limit=1] ~ ~ ~ ~ 0
execute unless score @s pmRigChar = #charN tmp run kill @e[tag=rlk_pm]
execute if entity @e[tag=rlk_av,limit=1] unless entity @e[tag=rlk_pm] at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/clips/skirk/burst_jin/spawn
execute if entity @e[tag=rlk_pm] run scoreboard players set @s pmVisible 1
scoreboard players operation @s pmRigChar = #charN tmp
# The displayed model (pmWModel) before frame zero sets it: another model snaps instead of blending.
scoreboard players set #pmWNew tmp 0
execute unless score @s pmWModel matches 4 run scoreboard players set #pmWNew tmp 1
# Reuse the displayed last pose when chaining an attack; interpolate into frame zero.
data modify storage rlk:player_motion active.step set value 2
execute if entity @e[tag=rlk_pm] run function rlk:char/motion/clips/skirk/burst_jin/pose/0 with storage rlk:player_motion active
execute store result storage rlk:player_motion active.step int 1 run scoreboard players get @s pmStep
execute at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0
# Drawn: instant draw (snap, no flight) with a gold sparkle at the hand unless it was already drawn
# (from the back, or out of the put-away clip where it may be dissolved or floating). A drawn weapon of
# another model (#pmWNew, read before frame zero) snaps and sparkles the same way.
execute unless score @s pmWAt matches 0 run function rlk:char/motion/sheath/snap
execute if score #pmWNew tmp matches 1 run function rlk:char/motion/sheath/snap
scoreboard players set @s pmWAt 0
execute unless score @s pmSheath matches 0 run scoreboard players set #pmWNew tmp 1
execute if score #pmWNew tmp matches 1 if entity @e[tag=rlk_pm_weapon] at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 positioned ^-0.686 ^1.132 ^0.141 run function rlk:char/motion/sheath/fx_hand
function rlk:char/motion/sheath/draw
execute if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/hide_avatar
execute store result score #pmFxFP tmp unless score @s pmVisible matches 1
execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/skirk_fx/burst_jin
scoreboard players set #pmFxFP tmp 0
execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/event
return 1
