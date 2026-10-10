# As the boss, reformed on the real illusion's spot: the existing stagger window.
function rlk:boss/raiden/illusion/reset
function rlk:boss/raiden/object/clear
scoreboard players set @s rdPat 99
scoreboard players set @s rdTime 0
scoreboard players set @s rdAnim 18
scoreboard players remove @s rdRage 120
execute if score @s rdRage matches ..0 run scoreboard players set @s rdRage 0
playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 0.8 0.65 0.2
