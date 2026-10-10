function rlk:char/motion/loco/context
execute unless entity @e[tag=rlk_pm] at @e[tag=rlk_av,limit=1] run function rlk:char/motion/loco/ensure
function rlk:char/motion/hide_avatar
# Follow the smoothed body heading, including sideways and backward travel.
execute at @e[tag=rlk_av,limit=1] rotated ~ 0 run tp @e[tag=rlk_pm] ~ ~ ~ ~ 0
function rlk:char/motion/loco/weapon
execute unless score @s pmLocMode = @s pmWantMode run return run function rlk:char/motion/loco/begin
execute if score @s pmBlend matches 1.. run return run scoreboard players remove @s pmBlend 1
scoreboard players set #pmInterp tmp 99
scoreboard players operation #pmInterp tmp += @s pmLocSpeed
scoreboard players operation #pmInterp tmp /= @s pmLocSpeed
execute store result storage rlk:player_motion loco.step int 1 run scoreboard players get #pmInterp tmp
scoreboard players operation @s pmLocAcc += @s pmLocSpeed
execute if score @s pmLocAcc matches 100.. run function rlk:char/motion/loco/advance
