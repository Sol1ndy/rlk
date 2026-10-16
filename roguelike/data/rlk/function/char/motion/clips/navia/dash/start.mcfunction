# @s player. Existing avatar remains the gameplay body.
function rlk:char/motion/release
scoreboard players set @s pmBlend 0
scoreboard players set @s pmWeapon -1
scoreboard players set @s pmActive 1
scoreboard players set @s pmTick 0
scoreboard players set @s pmLen 12
scoreboard players set @s pmChar 6
scoreboard players set @s pmSpeed 100
execute if score @s pmSpeed matches ..24 run scoreboard players set @s pmSpeed 25
execute if score @s pmSpeed matches 501.. run scoreboard players set @s pmSpeed 500
scoreboard players set @s pmAcc 0
scoreboard players set @s pmStep 99
scoreboard players operation @s pmStep += @s pmSpeed
scoreboard players operation @s pmStep /= @s pmSpeed
data modify storage rlk:player_motion active set value {char:"navia",clip:"dash",step:1,loop:0b,lockedYaw:1b}
execute store result storage rlk:player_motion active.step int 1 run scoreboard players get @s pmStep
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_pet","rlk_pm_basis"]}
execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run tp @e[tag=rlk_pm_basis,limit=1] ~ ~ ~ ~ 0
execute unless score @s pmRigChar = #charN tmp run kill @e[tag=rlk_pm]
execute if entity @e[tag=rlk_av,limit=1] unless entity @e[tag=rlk_pm] at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/clips/navia/dash/spawn
execute if entity @e[tag=rlk_pm] run scoreboard players set @s pmVisible 1
scoreboard players operation @s pmRigChar = #charN tmp
# Where a drawn weapon is before frame zero moves it to the back (the stow sparkle).
execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] run function rlk:char/motion/sheath/mark
# Reuse the displayed last pose when chaining an attack; interpolate into frame zero.
data modify storage rlk:player_motion active.step set value 2
execute if entity @e[tag=rlk_pm] run function rlk:char/motion/clips/navia/dash/pose/0 with storage rlk:player_motion active
execute store result storage rlk:player_motion active.step int 1 run scoreboard players get @s pmStep
execute at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0
# Sheathed: the weapon stays on the back (quick stow from the position marked before frame zero if it was
# drawn); loco/weapon picks the variant.
execute unless score @s pmWAt matches 1 run function rlk:char/motion/sheath/snap
scoreboard players set @s pmWAt 1
function rlk:char/motion/sheath/stow_marked
function rlk:char/motion/loco/weapon
execute if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/hide_avatar
execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/navia_fx/dash
execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/event
return 1
