kill @e[tag=rlk_rd_hazard]
function rlk:boss/raiden/object/clear
scoreboard players set @s rdPat 99
scoreboard players set @s rdTime 0
scoreboard players set @s rdAnim 18
scoreboard players remove @s rdRage 120
execute if score @s rdRage matches ..0 run scoreboard players set @s rdRage 0
playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ .8 .65 .3
