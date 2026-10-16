# @s player. Existing avatar remains the gameplay body.
function rlk:char/motion/release
scoreboard players set @s pmBlend 0
scoreboard players set @s pmWeapon -1
scoreboard players set @s pmActive 1
scoreboard players set @s pmTick 0
scoreboard players set @s pmLen 10
scoreboard players set @s pmChar 3
scoreboard players set @s pmSpeed 100
execute if score @s atkSpeed matches 1.. run scoreboard players operation @s pmSpeed = @s atkSpeed
execute if score @s pmSpeed matches ..24 run scoreboard players set @s pmSpeed 25
execute if score @s pmSpeed matches 501.. run scoreboard players set @s pmSpeed 500
scoreboard players set @s pmAcc 0
scoreboard players set @s pmStep 99
scoreboard players operation @s pmStep += @s pmSpeed
scoreboard players operation @s pmStep /= @s pmSpeed
data modify storage rlk:player_motion active set value {char:"skirk",clip:"physical_2",step:1,loop:0b,lockedYaw:0b}
execute store result storage rlk:player_motion active.step int 1 run scoreboard players get @s pmStep
execute unless score @s pmRigChar = #charN tmp run kill @e[tag=rlk_pm]
execute if entity @e[tag=rlk_av,limit=1] unless entity @e[tag=rlk_pm] at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/clips/skirk/physical_2/spawn
execute if entity @e[tag=rlk_pm] run scoreboard players set @s pmVisible 1
scoreboard players operation @s pmRigChar = #charN tmp
# Reuse the displayed last pose when chaining an attack; interpolate into frame zero.
data modify storage rlk:player_motion active.step set value 2
execute if entity @e[tag=rlk_pm] run function rlk:char/motion/clips/skirk/physical_2/pose/0 with storage rlk:player_motion active
execute store result storage rlk:player_motion active.step int 1 run scoreboard players get @s pmStep
execute at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0
# Drawn: instant draw from the back (snap, no flight) with a gold sparkle at the hand.
execute unless score @s pmWAt matches 0 run function rlk:char/motion/sheath/snap
scoreboard players set @s pmWAt 0
execute if score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 positioned ^-0.665 ^0.921 ^0.239 run function rlk:char/motion/sheath/fx_hand
function rlk:char/motion/sheath/draw
execute if entity @e[tag=rlk_av,limit=1] run function rlk:char/motion/hide_avatar
execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/skirk_fx/physical_2
execute at @e[tag=rlk_body,limit=1] rotated as @s rotated ~ 0 run function rlk:char/motion/event
return 1
